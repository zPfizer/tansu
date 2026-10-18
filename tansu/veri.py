"""Veri deposu: indirme → değişmez anlık görüntü → doğrulanmış okuma; olay denetimi (TASARIM 4, 5.1)."""

import datetime as dt
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from tansu.kaynak import KaynakHatasi

ISTANBUL = ZoneInfo("Europe/Istanbul")
BASLANGIC = dt.date(2010, 1, 1)
OLAY_TOLERANS = 0.005  # TASARIM 5.1: olay denetiminde %0,5
LIMIT_TOLERANS = 0.005  # TASARIM 5.1: karantina için limit aşımı payı
YUVARLAMA = 1e-4  # TASARIM 5.13: düzeltilmiş seri 4 ondalığa yuvarlı
LIMIT_DEGISIM = pd.Timestamp("2020-03-13")  # ±%20 → ±%10
ADIM_DEGISIM = pd.Timestamp("2023-11-06")  # fiyat adımı tablosu değişti
ADIM_ESIK = [20, 50, 100, 250, 500, 1000, 2500]  # TASARIM 5.1 tablosu, alt sınır dahil
ADIM_ESKI = [0.01, 0.02, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1]
ADIM_YENI = [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
FIYAT_SUTUNLARI = [
    "ham_kapanis",
    "ham_aof",
    "ham_yuksek",
    "ham_dusuk",
    "kapanis",
    "aof",
    "yuksek",
    "dusuk",
    "hacim",
]
KARANTINA_ESIK, DENETIM_ESIK, INMEYEN_ESIK = 0.01, 0.02, 5  # TASARIM 5.13
KAYNAK_GUNU_EN_AZ = 20  # TASARIM 5.13: kaynak günü hatası için en az satır


class VeriHatasi(Exception):
    pass


class KaynakYok(VeriHatasi):
    """Hiçbir sembol inmedi: kaynağa ulaşılamıyor (günlük koşuda VERİ YOK)."""


@dataclass(frozen=True)
class VeriIstegi:
    """Kayıtlı yerel veri isteği; sürümler çağırana aittir (TASARIM 5.15)."""

    semboller: tuple[str, ...]
    baslangic: str
    bitis: str
    kaynak: str
    kalite_surumu: str
    uyelik_surumu: str
    duzeltme_surumu: str
    takvim_ref: str
    isinma_donemi: tuple[str, str] | None = None


def veri_hazirla(istek: VeriIstegi, kimlik, kok) -> dict:
    """Doğrulanmış yerel görüntüyü E1 kayıtlarına uyarlar (TASARIM 5.15)."""
    bas, son, kapsam_bas = _istek_donemi(istek)
    a = oku(kimlik, kok)
    gunler = a.gunler[a.gunler <= son]
    semboller = list(istek.semboller)
    f = a.fiyat[a.fiyat["sembol"].isin(semboller)]
    C, A = (
        f.pivot(index="tarih", columns="sembol", values=ad)
        .reindex(index=gunler, columns=semboller)
        .to_numpy()
        for ad in ("kapanis", "aof")
    )
    # Kaynak günü kararı bütün görüntüde verilir; alt küme bunu değiştirmez.
    g = a.gun_tablosu
    d = cift_girdileri(
        gunler, C, A, cift_bayraklari(g, gunler, semboller), istek.kalite_surumu
    )
    kaynaklar = [
        {
            "tur": "yerel_goruntu",
            "konum": str(Path(kok) / "ag" / kimlik),
            "tarih": dt.datetime.now(ISTANBUL).date().isoformat(),
            "alinti": None,
            "bos_nedenleri": {"alinti": "veri_kaynagi"},
            "karar_durumu": "manifest_dogrulandi",
            "kaynak": istek.kaynak,
        }
    ]
    meta = {
        "sema_surumu": "s04_v1",
        "olusturma_zamani": dt.datetime.now(dt.UTC).isoformat(),
        "kaynaklar": kaynaklar,
    }
    secilen = gunler >= kapsam_bas
    olaylar = [
        {
            "sembol": r.sembol,
            "tarih": _tarih(r.tarih),
            "kod": r.kod,
            "carpan": float(r.carpan),
            "olay_ref": f"{kimlik}/olay/{i}",
        }
        for i, r in enumerate(a.olaylar.itertuples())
        if r.sembol in semboller and kapsam_bas <= r.tarih <= son
    ]
    piyasa = _piyasa_satirlari(istek, kimlik, f, g, d, secilen, olaylar, meta)
    hatalar = [
        {
            "sembol": r["sembol"],
            "tarih": r["tarih"],
            "nedenler": r["kalite_bayraklari"].copy(),
        }
        for r in piyasa
        if {"eksik", "karantina"}.intersection(r["kalite_bayraklari"])
    ]
    fiili = f[f["tarih"].between(kapsam_bas, son)]["tarih"]
    return {
        "piyasa": piyasa,
        "olaylar": olaylar,
        "kaynaklar": kaynaklar,
        "semboller": semboller,
        "gunler": [_tarih(t) for t in gunler[secilen]],
        "referans": _veri_referansi(istek, kimlik, kok, meta, fiili),
        "kalite": {
            "bozuk_satirlar": hatalar,
            "karantina_araliklari": _karantina_araliklari(d, semboller, secilen),
            "hata_nedenleri": sorted({n for h in hatalar for n in h["nedenler"]}),
            "uyarilar": ["istenen_donem_tam_degil"]
            if fiili.empty or fiili.min() > bas or fiili.max() < son
            else [],
        },
    }


def _istek_donemi(istek):
    _kalite_surumu(istek.kalite_surumu)
    if not istek.semboller or len(set(istek.semboller)) != len(istek.semboller):
        raise VeriHatasi("istekte semboller boş veya tekrarlı")
    if any(
        not getattr(istek, ad)
        for ad in ("kaynak", "uyelik_surumu", "duzeltme_surumu", "takvim_ref")
    ):
        raise VeriHatasi("veri isteğinin kaynak/sürüm referansı boş")
    bas, son = pd.Timestamp(istek.baslangic), pd.Timestamp(istek.bitis)
    if pd.isna(bas) or pd.isna(son) or bas > son:
        raise VeriHatasi("istenen dönem geçersiz")
    kapsam_bas = bas
    if istek.isinma_donemi is not None:
        ib, is_ = map(pd.Timestamp, istek.isinma_donemi)
        if pd.isna(ib) or pd.isna(is_) or ib > is_ or is_ >= bas:
            raise VeriHatasi("ısınma dönemi geçersiz")
        kapsam_bas = ib
    return bas, son, kapsam_bas


def _veri_referansi(istek, kimlik, kok, meta, fiili):
    return {
        **meta,
        "kayit_id": f"{kimlik}/veri/{istek.kalite_surumu}",
        "kayit_turu": "veri_referansi",
        "goruntu_id": kimlik,
        "manifest_parmak_izi": _sha256(Path(kok) / "ag" / kimlik / "manifest.json"),
        **{
            ad: getattr(istek, ad)
            for ad in (
                "uyelik_surumu",
                "kalite_surumu",
                "duzeltme_surumu",
                "takvim_ref",
            )
        },
        "istenen_donem": _donem(istek.baslangic, istek.bitis),
        "fiili_donem": _donem(fiili.min(), fiili.max()),
        "isinma_donemi": _donem(*istek.isinma_donemi) if istek.isinma_donemi else None,
        "bos_nedenleri": {} if istek.isinma_donemi else {"isinma_donemi": "istenmedi"},
    }


def _piyasa_satirlari(istek, kimlik, f, g, d, secilen, olaylar, meta):
    fiyat = f.set_index(["tarih", "sembol"])
    kalite = g.set_index(["tarih", "sembol"])
    olay_ref = {}
    for o in olaylar:
        olay_ref.setdefault((o["tarih"], o["sembol"]), []).append(o["olay_ref"])
    piyasa = []
    for q in np.flatnonzero(secilen):
        t = d["gunler"][q]
        for j, s in enumerate(istek.semboller):
            anahtar = (t, s)
            r = fiyat.loc[anahtar] if anahtar in fiyat.index else pd.Series(dtype=float)
            k = (
                kalite.loc[anahtar]
                if anahtar in kalite.index
                else pd.Series(dtype=bool)
            )
            piyasa.append(
                _piyasa_satiri(istek, kimlik, s, t, r, k, d, q, j, olay_ref, meta)
            )
    return piyasa


def _piyasa_satiri(istek, kimlik, s, t, r, k, d, q, j, olay_ref, meta):
    bayraklar = [
        ad
        for ad in ("eksik", "karantina", "kilit_tavan", "kilit_taban")
        if k.get(ad, False)
    ]
    if r.empty and "eksik" not in bayraklar:
        bayraklar.append("eksik")
    if d["Kar"][q, j] and "karantina" not in bayraklar:
        bayraklar.append("karantina")
    if d["E"][q, j]:
        bayraklar.append("giris_engelli")
    satir = {
        **meta,
        "kayit_id": f"{kimlik}/{s}/{t.date()}/{istek.kalite_surumu}",
        "kayit_turu": "piyasa_satiri",
        "sembol": s,
        "tarih": _tarih(t),
        "kalite_bayraklari": bayraklar,
        "islem": bool(d["I"][q, j]),
        "olay_ref": ",".join(olay_ref.get((_tarih(t), s), [])) or None,
        "son_gecerli_fiyat_tarihi": _tarih(d["son_gecerli_fiyat_tarihi"][q, j]),
    }
    satir["bos_nedenleri"] = {
        ad: neden
        for ad, neden in (
            ("olay_ref", "olay_yok"),
            ("son_gecerli_fiyat_tarihi", "gecerli_fiyat_yok"),
        )
        if satir[ad] is None
    }
    for ad in ("acilis", "yuksek", "dusuk", "kapanis", "aof"):
        satir[f"ham_{ad}"] = _deger(r.get(f"ham_{ad}"), "TL/adet")
        satir[f"duzeltilmis_{ad}"] = _deger(r.get(ad), "TL/adet")
    satir["hacim_tl"] = _deger(r.get("hacim"), "TL/seans")
    return satir


def _karantina_araliklari(d, semboller, secilen):
    araliklar = []
    for j, s in enumerate(semboller):
        engel = np.flatnonzero(d["E"][:, j] & secilen)
        for grup in np.split(engel, np.where(np.diff(engel) > 1)[0] + 1):
            if len(grup):
                araliklar.append(
                    {
                        "sembol": s,
                        "baslangic": _tarih(d["gunler"][grup[0]]),
                        "bitis": _tarih(d["gunler"][grup[-1]]),
                    }
                )
    return araliklar


def _tarih(deger):
    return None if pd.isna(deger) else pd.Timestamp(deger).date().isoformat()


def _donem(bas, son):
    return {
        "baslangic": _tarih(bas),
        "bitis": _tarih(son),
        "isinma_baslangici": None,
        "bos_nedenleri": {
            "isinma_baslangici": "ayri_referans",
            **(
                {"baslangic": "gozlem_yok", "bitis": "gozlem_yok"}
                if pd.isna(bas)
                else {}
            ),
        },
        "sinir_surumu": "s04_dahil",
    }


def _deger(deger, birim):
    neden = "kaynakta_yok" if deger is None or pd.isna(deger) else None
    if neden is None and not np.isfinite(deger):
        neden = "sonlu_degil"
    if neden is None and birim == "TL/adet" and deger <= 0:
        neden = "pozitif_degil"
    return {
        "deger": None if neden else float(deger),
        "birim": birim,
        "bos_nedeni": neden,
    }


@dataclass(frozen=True)
class Anlik:
    kimlik: str
    fiyat: pd.DataFrame  # uzun biçim: sembol, tarih, ham_* ve düzeltilmiş sütunlar
    olaylar: pd.DataFrame  # sembol, tarih, kod, carpan
    faiz: pd.DataFrame = None  # tarih, faiz (yüzde); yalnız değişim günleri
    sektor: dict = None  # sembol → KAP sektörü
    inmeyen: tuple = ()  # indirilemeyen semboller
    bos: tuple = ()  # kaynağın veri döndürmediği semboller (hata değil: pay olmayan kod, işlem görmemiş)

    @cached_property  # sinama sembol başına çağırır; bir kez hesaplanır
    def gun_tablosu(self) -> pd.DataFrame:
        """Sembol × takvim günü: islem, eksik, limit, tavan, taban, kilit_*, karantina (TASARIM 5.1)."""
        takvim = pd.DatetimeIndex(sorted(self.fiyat["tarih"].unique()))
        parcalar = [
            _gunler(f, self.olaylar[self.olaylar["sembol"] == s], takvim).assign(
                sembol=s
            )
            for s, f in self.fiyat.groupby("sembol", sort=False)
        ]
        g = pd.concat(parcalar).rename_axis("tarih").reset_index()
        d = g[~g["eksik"]].groupby("tarih")["karantina"].agg(["sum", "size"])
        kaynak = g["tarih"].isin(
            d.index[(d["size"] >= KAYNAK_GUNU_EN_AZ) & (d["sum"] * 2 >= d["size"])]
        )
        g.loc[kaynak, ["eksik", "karantina"]] = [
            True,
            False,
        ]  # TASARIM 5.13: kaynak günü hatası = eksik gün
        g.loc[
            kaynak,
            [
                "islem",
                "kilit_tavan",
                "kilit_taban",
                "kilit_tavan_duyarli",
                "kilit_taban_duyarli",
            ],
        ] = False
        return g

    @cached_property
    def kaynak_gunleri(self) -> list:
        """Kaynak günü hatası olan günler (TASARIM 5.13): sembollerin hepsi eksik, gün takvimde var."""
        e = self.gun_tablosu.groupby("tarih")["eksik"].all()
        return list(e.index[e])

    def oranlar(self, uye=None) -> tuple:
        """(karantina oranı, olay denetimi farkı oranı, hisse-gün sayısı).

        `uye`: (sembol, tarih) tablosu; verilirse yalnız o hisse-günler sayılır (TASARIM 5.13, evren üyeleri)."""
        g = self.gun_tablosu
        satirlar = {
            "hepsi": self.fiyat[["sembol", "tarih"]],
            "kar": g.loc[g["karantina"], ["sembol", "tarih"]],
            "olay": self.olay_uyarilari.reindex(columns=["sembol", "tarih"]),
        }
        if uye is not None:
            satirlar = {
                k: v.merge(uye[["sembol", "tarih"]], on=["sembol", "tarih"])
                for k, v in satirlar.items()
            }
        n = len(satirlar["hepsi"])
        return (
            (len(satirlar["kar"]) / n, len(satirlar["olay"]) / n, n)
            if n
            else (0.0, 0.0, 0)
        )

    def _sorunlar(self, uye) -> list:
        karantina, olay, _ = self.oranlar(uye)
        sonuc = []
        if karantina > KARANTINA_ESIK:
            sonuc.append("karantina oranı > %1")
        if olay > DENETIM_ESIK:
            sonuc.append("olay denetimi farkı olan gün oranı > %2")
        sonuc += [f"kaynak günü hatası: {t.date()}" for t in self.kaynak_gunleri]
        if len(self.inmeyen) > INMEYEN_ESIK:
            sonuc.append(f"{len(self.inmeyen)} hisse inmedi")
        return sonuc

    @property
    def sorunlar(self) -> list:
        """Oran eşiklerini aşan kapılar, bütün hisse-günlerde (TASARIM 5.13); boş liste = veri temiz."""
        return self._sorunlar(None)

    def sorunlar_uye(self, uye) -> list:
        """Aynı kapılar yalnız evren üyesi hisse-günlerde: sınama kararı bunlarla verilir (TASARIM 5.13)."""
        return self._sorunlar(uye)

    @cached_property
    def gunler(self) -> pd.DatetimeIndex:
        """Takvim: XU100 kapanışı olan günler (TASARIM 4)."""
        f = self.fiyat
        return pd.DatetimeIndex(sorted(f.loc[f["xu100"] > 0, "tarih"].unique()))

    @property
    def faiz_son_degisim(self) -> pd.Timestamp:
        return self.faiz["tarih"].max()

    def faiz_gunluk(self, bas, son) -> pd.Series:
        """Günlük (takvim günü) faiz: değişim günlerinden ileri doldurulur, bir gün gecikmeli (TASARIM 5.6).

        Seri boşsa ya da istenen aralığın başını kapsamıyorsa VeriHatasi (koşu SORUNLU olur).
        """
        if self.faiz is None or self.faiz.empty:
            raise VeriHatasi("faiz serisi boş")
        degisim = self.faiz.set_index("tarih")["faiz"].sort_index()
        gun = pd.date_range(degisim.index[0], pd.Timestamp(son))
        gecikmeli = degisim.reindex(gun).ffill().shift(1)
        s = gecikmeli.reindex(pd.date_range(pd.Timestamp(bas), pd.Timestamp(son)))
        if s.isna().any():
            raise VeriHatasi(
                f"faiz serisi {s.index[s.isna()][0].date()} gününü kapsamıyor"
            )
        return s

    @cached_property
    def olay_uyarilari(self) -> pd.DataFrame:
        parcalar = [
            _olay_denetimi(f, self.olaylar[self.olaylar["sembol"] == s]).assign(
                sembol=s
            )
            for s, f in self.fiyat.groupby("sembol", sort=False)
        ]
        return pd.concat(parcalar, ignore_index=True) if parcalar else pd.DataFrame()


def indir(semboller, kok, kaynak, simdi=None, bas=BASLANGIC, borsapy=None) -> str:
    """Sembollerin fiyat ve olaylarını indirir, anlık görüntüyü yazar, kimliğini döndürür.

    `borsapy` verilirse faiz ve sektör tabloları da anlık görüntüye girer; boş faiz serisi hatadır."""
    simdi = simdi or dt.datetime.now(ISTANBUL)
    kimlik = simdi.strftime("%Y%m%d-%H%M")
    ag = Path(kok) / "ag"
    hedef, gecici = ag / kimlik, ag / f"_gecici-{kimlik}"
    if hedef.exists():
        raise VeriHatasi(f"anlık görüntü zaten var: {kimlik}")
    fiyatlar, ham_olaylar, inmeyen, bos = [], {}, [], []
    for s in semboller:
        try:
            f, ham_olaylar[s] = (
                kaynak.fiyat(s, bas, simdi.date()).assign(sembol=s),
                kaynak.olaylar(s),
            )
        except KaynakHatasi:
            ham_olaylar.pop(s, None)
            inmeyen.append(s)
            continue
        if not f.empty:  # hacmi ve ham alanları NaN/0 olan satır işlem yapılmamış gündür; aynı tekrar satır tek sayılır
            f = f.drop_duplicates(subset=["tarih", *FIYAT_SUTUNLARI])
            f = f[~(f[[*FIYAT_SUTUNLARI[:4], "hacim"]].fillna(0) == 0).all(axis=1)]
        if f.empty:
            del ham_olaylar[s]
            bos.append(s)
            continue
        _yapi_denetimi(s, f)
        fiyatlar.append(f)
    if not fiyatlar:
        raise KaynakYok("hiçbir sembol inmedi")
    if borsapy:
        faiz = borsapy.faiz()
        if faiz.empty:
            raise VeriHatasi("faiz serisi boş")
        sektor = {}
        for f in fiyatlar:
            s = f["sembol"].iloc[0]
            try:
                sektor[s] = borsapy.sektor(s)
            except (
                KaynakHatasi
            ):  # sektörü olmayan hisse çifte girmez (TASARIM 5.2); indirme durmaz
                pass
    shutil.rmtree(gecici, ignore_errors=True)
    gecici.mkdir(parents=True)
    if borsapy:
        faiz.to_parquet(gecici / "faiz.parquet", index=False)
        (gecici / "sektor.json").write_text(
            json.dumps(sektor, ensure_ascii=False), encoding="utf-8"
        )
    pd.concat(fiyatlar, ignore_index=True).to_parquet(
        gecici / "fiyat.parquet", index=False
    )
    (gecici / "olaylar.json").write_text(
        json.dumps(ham_olaylar, ensure_ascii=False), encoding="utf-8"
    )
    manifest = {
        "kimlik": kimlik,
        "semboller": [s for s in semboller if s not in inmeyen + bos],
        "inmeyen": inmeyen,
        "bos": bos,
        "dosyalar": {p.name: _sha256(p) for p in sorted(gecici.iterdir())},
    }
    (gecici / "manifest.json").write_text(
        json.dumps(manifest, indent=1), encoding="utf-8"
    )
    os.replace(gecici, hedef)
    return kimlik


def sektor_tamamla(kimlik, kok, kap, hedefler, simdi=None, art_arda=5) -> tuple:
    """Eksik sektörleri `kap.sektor` ile okur; bitince yeni anlık görüntü yazar (eskisi değişmez, TASARIM 4).

    Önbellek `onbellek/sektor-<kimlik>.jsonl` (sembol → ad ya da null = KAP listesinde yok). Art arda `art_arda` hatada
    durur ve (None, kapsam) döndürür. Sonda (yeni kimlik, kapsam): hedef, var, listede_yok, alinamayan.
    """
    kok = Path(kok)
    eski = oku(kimlik, kok)  # manifest doğrulanır
    var = dict(eski.sektor or {})
    onbellek = kok / "onbellek" / f"sektor-{kimlik}.jsonl"
    onbellek.parent.mkdir(parents=True, exist_ok=True)
    bilinen = {}
    if onbellek.exists():
        for satir in onbellek.read_text(encoding="utf-8").splitlines():
            ad = json.loads(satir)
            bilinen[ad["sembol"]] = ad["sektor"]
    alinamayan, hata = [], 0
    for s in hedefler:
        if s in var or s in bilinen:
            continue
        try:
            bilinen[s] = kap.sektor(s)
        except KaynakHatasi:
            alinamayan.append(s)
            hata += 1
            if hata >= art_arda:
                break
            continue
        hata = 0
        with onbellek.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps({"sembol": s, "sektor": bilinen[s]}, ensure_ascii=False)
                + "\n"
            )
    var.update({s: ad for s, ad in bilinen.items() if ad})
    kapsam = {
        "hedef": len(hedefler),
        "var": sum(s in var for s in hedefler),
        "listede_yok": [s for s in hedefler if s in bilinen and bilinen[s] is None],
        "alinamayan": [s for s in hedefler if s not in var and s not in bilinen],
    }
    if hata >= art_arda:
        return None, kapsam
    simdi = simdi or dt.datetime.now(ISTANBUL)
    yeni = simdi.strftime("%Y%m%d-%H%M")
    ag = kok / "ag"
    hedef, gecici = ag / yeni, ag / f"_gecici-{yeni}"
    if hedef.exists():
        raise VeriHatasi(f"anlık görüntü zaten var: {yeni}")
    shutil.rmtree(gecici, ignore_errors=True)
    gecici.mkdir(parents=True)
    manifest = json.loads((ag / kimlik / "manifest.json").read_text(encoding="utf-8"))
    for ad in manifest["dosyalar"]:
        if ad != "sektor.json":
            shutil.copy2(ag / kimlik / ad, gecici / ad)
    (gecici / "sektor.json").write_text(
        json.dumps(var, ensure_ascii=False), encoding="utf-8"
    )
    manifest.update(
        kimlik=yeni,
        kaynak=kimlik,
        sektor_kapsam=kapsam,
        dosyalar={p.name: _sha256(p) for p in sorted(gecici.iterdir())},
    )
    (gecici / "manifest.json").write_text(
        json.dumps(manifest, indent=1), encoding="utf-8"
    )
    os.replace(gecici, hedef)
    return yeni, kapsam


def oku(kimlik, kok) -> Anlik:
    """Manifesti doğrular; uyuşmazlık VeriHatasi'dır."""
    klasor = Path(kok) / "ag" / kimlik
    manifest = json.loads((klasor / "manifest.json").read_text(encoding="utf-8"))
    for ad, ozet in manifest["dosyalar"].items():
        if _sha256(klasor / ad) != ozet:
            raise VeriHatasi(f"manifest uyuşmuyor: {kimlik}/{ad}")
    ham = json.loads((klasor / "olaylar.json").read_text(encoding="utf-8"))
    olaylar = pd.DataFrame(
        [
            {
                "sembol": s,
                "tarih": _olay_tarihi(o["SHHE_TARIH"]),
                "kod": o["SHT_KODU"],
                "carpan": float(o["SHHE_FIYAT_AYAR_OR"]),
            }
            for s, liste in ham.items()
            for o in liste
            if o["SHHE_TARIH"] > 0 and o["SHHE_FIYAT_AYAR_OR"] > 0
        ],  # yer tutucu kayıt düzeltme taşımaz
        columns=["sembol", "tarih", "kod", "carpan"],
    )
    faiz = (
        pd.read_parquet(klasor / "faiz.parquet")
        if "faiz.parquet" in manifest["dosyalar"]
        else None
    )
    sektor = (
        json.loads((klasor / "sektor.json").read_text(encoding="utf-8"))
        if "sektor.json" in manifest["dosyalar"]
        else None
    )
    return Anlik(
        kimlik,
        pd.read_parquet(klasor / "fiyat.parquet"),
        olaylar,
        faiz,
        sektor,
        tuple(manifest.get("inmeyen", [])),
        tuple(manifest.get("bos", [])),
    )


def _sha256(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()


def cift_girdileri(gunler, C, A, F, kalite_surumu) -> dict:
    """Eski çift yollarının politika seçimi (TASARIM 5.15, S04)."""
    from tansu.motor import KARANTINA_GUN

    _kalite_surumu(kalite_surumu)
    C, A = np.asarray(C), np.asarray(A)
    bayrak = {k: np.asarray(F[k], dtype=bool) for k in ("I", "T", "B", "Kar")}
    if C.shape != A.shape or C.ndim != 2 or C.shape[0] != len(gunler):
        raise VeriHatasi("çift fiyatlarının tarih/boyut uyuşmazlığı")
    if any(v.shape != C.shape for v in bayrak.values()):
        raise VeriHatasi("çift bayraklarının boyut uyuşmazlığı")
    if kalite_surumu == "legacy_tansu_v1":
        bayrak["Kar"] = bayrak["Kar"] | np.isinf(C) | np.isinf(A)
    G = bayrak["I"] & ~bayrak["Kar"]
    if kalite_surumu == "legacy_tansu_v1":
        G = G & np.isfinite(C) & (C > 0) & np.isfinite(A) & (A > 0)
    tarihler = pd.DataFrame(np.broadcast_to(np.asarray(gunler)[:, None], C.shape))
    return {
        "gunler": gunler,
        "C": C,
        "A": A,
        **bayrak,
        "G": G,
        "Cf": pd.DataFrame(C).where(G).ffill().to_numpy(),
        "SA": pd.DataFrame(A).where(G).ffill().to_numpy(),
        "E": pd.DataFrame(bayrak["Kar"].astype(float))
        .rolling(KARANTINA_GUN, min_periods=1)
        .max()
        .to_numpy()
        .astype(bool),
        "son_gecerli_fiyat_tarihi": tarihler.where(G).ffill().to_numpy(),
    }


def _kalite_surumu(surum):
    if surum not in ("legacy_portfoy_v1", "legacy_tansu_v1"):
        raise VeriHatasi(f"bilinmeyen kalite sürümü: {surum}")


def cift_bayraklari(g, gunler, semboller) -> dict:
    """Aynı tarih/sembol sırasındaki eski işlem ve kilit bayrakları (TASARIM 5.15)."""
    return {
        k: g.pivot(index="tarih", columns="sembol", values=ad)
        .reindex(index=gunler, columns=semboller)
        .fillna(False)
        .astype(bool)
        .to_numpy()
        for k, ad in (
            ("I", "islem"),
            ("T", "kilit_tavan"),
            ("B", "kilit_taban"),
            ("Kar", "karantina"),
        )
    }


def _olay_tarihi(ms) -> pd.Timestamp:
    return pd.Timestamp(dt.datetime.fromtimestamp(ms / 1000, ISTANBUL).date())


def _olay_konumu(oran, i, carpan) -> int:
    """Tablo tarihinin konumu `i`; ±1 işlem günü içinde düzeltme oranı sıçraması çarpana en yakın olan gün (TASARIM 5.1)."""
    adaylar = [j for j in (i - 1, i, i + 1) if 1 <= j < len(oran)]
    with np.errstate(all="ignore"):
        fark = {j: abs(oran[j - 1] / oran[j] / carpan - 1) for j in adaylar}
    return min(adaylar, key=lambda j: np.nan_to_num(fark[j], nan=np.inf), default=i)


def _olay_denetimi(fiyat: pd.DataFrame, olaylar: pd.DataFrame) -> pd.DataFrame:
    """Gözlenen düzeltme oranını (düzeltilmiş/ham) olay çarpanlarından beklenenle karşılaştırır.

    Çarpan, olay gününden önceki satırlara uygulanır. Tablo tarihi gerçek adımdan bir işlem günü
    kayabilir (HEKTS 2015-11-26): her olay grubu ±1 işlem günü içinde en iyi tutan güne yerleştirilir.
    """
    f = fiyat.sort_values("tarih").reset_index(drop=True)
    f = f[(f["ham_kapanis"] > 0) & (f["kapanis"] > 0)].reset_index(drop=True)
    gunler = pd.DatetimeIndex(f["tarih"])
    oran = (f["kapanis"] / f["ham_kapanis"]).to_numpy()
    beklenen = pd.Series(1.0, index=f.index)
    for tarih, grup in olaylar.groupby("tarih"):
        carpan = grup["carpan"].prod()
        if (
            len(gunler) == 0 or tarih < gunler[0]
        ):  # pencereden önceki olay hiçbir satırı etkilemez
            continue
        i = gunler.searchsorted(
            tarih
        )  # olay tarihine eşit ya da sonraki ilk işlem günü
        if i < len(
            gunler
        ):  # pencereden sonraki olay bütün satırlara uygulanır, kaydırılmaz
            i = _olay_konumu(oran, i, carpan)
        beklenen[beklenen.index < i] *= carpan
    fark = oran / beklenen.to_numpy() - 1
    uyari = abs(fark) > OLAY_TOLERANS
    return pd.DataFrame(
        {
            "tarih": f["tarih"][uyari],
            "gozlenen": oran[uyari],
            "beklenen": beklenen[uyari],
            "fark": fark[uyari],
        }
    ).reset_index(drop=True)


def adim(fiyat, tarih):
    """Fiyat adımı (TASARIM 5.1 tablosu); fiyat ve tarih dizi olabilir."""
    i = np.searchsorted(ADIM_ESIK, fiyat, side="right")
    return np.where(
        np.asarray(tarih) >= ADIM_DEGISIM,
        np.array(ADIM_YENI)[i],
        np.array(ADIM_ESKI)[i],
    )


def _yapi_denetimi(sembol, f):
    """Bozuk sıra, tekrar eden gün ya da ortada NaN indirmeyi durdurur (TASARIM 5.13)."""
    if not f["tarih"].is_monotonic_increasing:
        raise VeriHatasi(f"{sembol}: tarih sırası bozuk")
    if f["tarih"].duplicated().any():
        raise VeriHatasi(f"{sembol}: tekrar eden gün")


def _gunler(fiyat, olaylar, takvim):
    f = fiyat.sort_values("tarih").set_index("tarih")
    f = f.reindex(takvim[(takvim >= f.index[0]) & (takvim <= f.index[-1])])
    var = f["ham_kapanis"].notna()  # eksik gün NaN kalır, doldurulmaz
    islem = var & (f["hacim"] > 0)
    bozuk = var & ~(
        (f[FIYAT_SUTUNLARI[:8]] > 0).all(axis=1)
        & (f["ham_dusuk"] <= f["ham_aof"])
        & (f["ham_aof"] <= f["ham_yuksek"])
        & (f["ham_dusuk"] <= f["ham_kapanis"])
        & (f["ham_kapanis"] <= f["ham_yuksek"])
        & (f["dusuk"] * (1 - YUVARLAMA) <= f["aof"])
        & (f["aof"] <= f["yuksek"] * (1 + YUVARLAMA))
        & (f["dusuk"] * (1 - YUVARLAMA) <= f["kapanis"])
        & (f["kapanis"] <= f["yuksek"] * (1 + YUVARLAMA))
    )
    ok = islem & ~bozuk
    onceki = f["ham_kapanis"].where(ok).ffill().shift(1)
    carpan = pd.Series(1.0, index=f.index)
    gunler = f.index[islem.to_numpy()]
    getiri = (
        f["ham_kapanis"] / onceki
    ).to_numpy()  # günün ham kapanışı / önceki tutarlı kapanış (5.13)
    for tarih, grup in olaylar.groupby("tarih"):
        if len(gunler) == 0 or tarih < gunler[0]:
            continue
        i = gunler.searchsorted(tarih)  # olay gününe eşit ya da sonraki işlem günü (t)
        c = grup["carpan"].prod()
        for j in (
            i,
            i + 1,
        ):  # gün başına, aday seçimi yok: adım t'yi t-1 ya da t tarihli olay açıklar (5.1)
            if j < len(gunler):
                k = f.index.get_loc(gunler[j])
                with np.errstate(all="ignore"):
                    adim_mi = abs(np.log(getiri[k] / c)) < abs(np.log(getiri[k]))
                if adim_mi:  # NaN (önceki gün yok) karşılaştırması yanlıştır
                    carpan.iloc[k] *= c
    limit = pd.Series(np.where(f.index >= LIMIT_DEGISIM, 0.10, 0.20), index=f.index)
    ref = onceki * carpan
    tavan, taban, kapanis = ref * (1 + limit), ref * (1 - limit), f["ham_kapanis"]
    asim = (kapanis > tavan * (1 + LIMIT_TOLERANS)) | (
        kapanis < taban * (1 - LIMIT_TOLERANS)
    )
    karantina = bozuk | (ok & asim)
    temiz = ok & ~karantina
    kilit_tavan = temiz & (kapanis >= tavan - adim(tavan, f.index) - 1e-9)
    kilit_taban = temiz & (kapanis <= taban + adim(taban, f.index) + 1e-9)
    duyarli = f["ham_dusuk"] == f["ham_yuksek"]
    return pd.DataFrame(
        {
            "islem": islem,
            "eksik": ~var,
            "limit": limit,
            "tavan": tavan,
            "taban": taban,
            "kilit_tavan": kilit_tavan,
            "kilit_taban": kilit_taban,
            "kilit_tavan_duyarli": kilit_tavan & duyarli,
            "kilit_taban_duyarli": kilit_taban & duyarli,
            "karantina": karantina,
        }
    )
