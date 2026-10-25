"""Veri deposu: indirme → değişmez anlık görüntü → doğrulanmış okuma; olay denetimi (TASARIM 4, 5.1)."""

import datetime as dt
import hashlib
import json
import os
import shutil
from io import BytesIO
from dataclasses import dataclass, replace
from copy import deepcopy
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
KARANTINA_GUN = 250  # TASARIM 5.1: karantinadan sonra yeni sinyal yok
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
LIMIT_OLAY_KODLARI = frozenset(
    {"01", "02", "03", "04", "05", "06", "08", "09", "78"}
)  # TASARIM 5.1
# TASARIM 5.15 #167: saklı metne yetkiyi çağıranın özeti değil yayımlanmış kaynak verir.
_YAYIMLANMIS_KAYNAK_OZETLERI = {
    "bist30_2021_2025_v1": "6e9ff3cd4a9ce4f2fe9a9ef9f77c36694f563bebe1ca2ba4f924643ce904ad07",
    "pay_kimligi_v1": "128cb4fdd2f310b3703d1e90dd6d83718b3a14185cd22c9a4bee6fd1190ea45d",
    "ilk_islem_v1": "8a678750c0ebfbfebe730fc8b4f53eaeaac0f622111d1dcf095cfa054589f4f1",
}


class VeriHatasi(Exception):
    pass


class KaynakYok(VeriHatasi):
    """Hiçbir sembol inmedi: kaynağa ulaşılamıyor (günlük koşuda VERİ YOK)."""


@dataclass(frozen=True)
class UyelikIstegi:
    """Değerlendirme günleri ve açık politika/sürüm seçimi (TASARIM 5.15)."""

    tarihler: tuple[str, ...]
    evren_politikasi: str
    uyelik_surumu: str


class UyelikKapsamHatasi(VeriHatasi):
    """Eksik değerlendirme günleri koşuyu durdurur (TASARIM 5.15)."""

    def __init__(self, surum, tarihler):
        self.uyelik_surumu = surum
        self.eksik_tarihler = sorted(set(tarihler))
        super().__init__(
            f"{surum}: üyelik kapsamı eksik: {', '.join(self.eksik_tarihler)}"
        )


def _uyelik_tablosu(yol):
    tablo = pd.read_csv(yol, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    if set(tablo.columns) != {"sembol", "baslangic", "bitis", "kaynak_id"}:
        raise VeriHatasi("üyelik tablosu sütunları geçersiz")
    if tablo[["sembol", "baslangic", "kaynak_id"]].eq("").any().any():
        raise VeriHatasi("üyelik tablosunda zorunlu alan boş")
    try:
        tablo["bas"] = pd.to_datetime(tablo["baslangic"], format="%Y-%m-%d")
        tablo["son"] = pd.to_datetime(
            tablo["bitis"].replace("", "2026-01-01"), format="%Y-%m-%d"
        ) - pd.Timedelta(days=1)
    except ValueError as hata:
        raise VeriHatasi("üyelik tablosunda tarih geçersiz") from hata
    if (tablo["bas"] > tablo["son"]).any():
        raise VeriHatasi("üyelik aralığı ters")
    for _, grup in tablo.sort_values("bas").groupby("sembol"):
        if (grup["bas"] <= grup["son"].cummax().shift()).any():
            raise VeriHatasi("aynı sembolde çakışan üyelik aralığı")
    return tablo


def uyelik_hazirla(istek: UyelikIstegi, *, tablo_metni=None) -> dict:
    """Tarihli üyelik yanıtı (TASARIM 5.15)."""
    if (istek.evren_politikasi, istek.uyelik_surumu) != (
        "donemsel_bist30_v1",
        "bist30_2021_2025_v1",
    ):
        raise VeriHatasi("bilinmeyen evren politikası/üyelik sürümü")
    yol = Path(__file__).parent / "referans" / istek.uyelik_surumu / "uyelik.csv"
    if tablo_metni is not None and hashlib.sha256(
        tablo_metni.encode("utf-8")
    ).hexdigest() != _YAYIMLANMIS_KAYNAK_OZETLERI.get(istek.uyelik_surumu):
        raise VeriHatasi("üyelik sürümünün onaylı kaynak özeti uyuşmuyor")
    # TASARIM 5.15 #167: kayıtlı kaynak aynı parserdan dosyasız geçer.
    tablo = _uyelik_tablosu(
        yol if tablo_metni is None else BytesIO(tablo_metni.encode("utf-8"))
    )
    gunler, eksik = {}, []
    for tarih in istek.tarihler:
        t = pd.Timestamp(tarih)
        if pd.isna(t) or t != t.normalize() or t.tzinfo is not None:
            raise VeriHatasi("üyelik isteği gün olmalıdır")
        kayitlar = []
        for r in tablo.itertuples():
            bas, son = r.bas, r.son
            if bas <= t <= son:
                kayitlar.append(
                    {
                        "kayit_id": f"{istek.uyelik_surumu}/{r.sembol}/{r.baslangic}",
                        "kayit_turu": "uyelik_araligi",
                        "sema_surumu": "s05_v1",
                        "olusturma_zamani": dt.datetime.now(dt.UTC).isoformat(),
                        "sembol": r.sembol,
                        "endeks": "BIST30",
                        "uyelik_surumu": istek.uyelik_surumu,
                        "yururluk_baslangici": bas.date().isoformat(),
                        "yururluk_bitisi": son.date().isoformat(),
                        "kaynak_id": r.kaynak_id,
                        "duyuru_zamani": None,
                        "bos_nedenleri": {"duyuru_zamani": "saat_kaniti_yok"},
                        "kaynaklar": [
                            {
                                "tur": "uyelik_kaynagi",
                                "konum": yol.with_name("kaynaklar.md").as_posix(),
                                "kaynak_id": r.kaynak_id,
                                "tarih": dt.datetime.now(ISTANBUL).date().isoformat(),
                                "alinti": None,
                                "bos_nedenleri": {"alinti": "tablo_kaynagi"},
                                "karar_durumu": "dogrulandi",
                            }
                        ],
                    }
                )
        gunler[t.date().isoformat()] = {
            "semboller": sorted(r["sembol"] for r in kayitlar),
            "kanitlar": kayitlar,
        }
        if (
            not pd.Timestamp("2021-01-01") <= t <= pd.Timestamp("2025-12-31")
            or len(kayitlar) != 30
        ):
            eksik.append(t.date().isoformat())
    if eksik:
        raise UyelikKapsamHatasi(istek.uyelik_surumu, eksik)
    return {
        "gunler": gunler,
        "evren_politikasi": istek.evren_politikasi,
        "uyelik_surumu": istek.uyelik_surumu,
        "tablo_parmak_izi": _sha256(yol)
        if tablo_metni is None
        else hashlib.sha256(tablo_metni.encode("utf-8")).hexdigest(),
    }


PAY_KIMLIGI_KOKU = Path(__file__).parent / "referans"


def _kaynak_secimi_dogrula(secim, surum, ad):
    alanlar = {"surum", "tablo_ozeti", "kaynak", "goruntu_id", "manifest_ozeti"}
    if not isinstance(secim, dict) or set(secim) != alanlar:
        raise VeriHatasi(f"{ad} seçiminin alanları geçersiz")
    if secim["surum"] != surum:
        raise VeriHatasi(f"bilinmeyen {ad} sürümü")
    if any(not isinstance(secim[a], str) or not secim[a].strip() for a in alanlar):
        raise VeriHatasi(f"{ad} seçiminin bağı boş")
    if any(
        len(secim[a]) != 64 or set(secim[a]) - set("0123456789abcdef")
        for a in ("tablo_ozeti", "manifest_ozeti")
    ):
        raise VeriHatasi(f"{ad} özeti geçersiz")


def pay_kimligi_secimi_dogrula(secim):
    """TASARIM 5.15 #167: yalnız yapı denetimi; dosya veya piyasa okunmaz."""
    _kaynak_secimi_dogrula(secim, "pay_kimligi_v1", "pay kimliği")


ILK_ISLEM_KOKU = Path(__file__).parent / "referans"


def ilk_islem_secimi_dogrula(secim):
    """TASARIM 5.15 #178: kaynak seçimi yalnız yayımlanmış sürüme bağlıdır."""
    _kaynak_secimi_dogrula(secim, "ilk_islem_v1", "ilk işlem")
    if secim["tablo_ozeti"] != _YAYIMLANMIS_KAYNAK_OZETLERI["ilk_islem_v1"]:
        raise VeriHatasi("ilk işlem sürümünün onaylı kaynak özeti uyuşmuyor")


def ilk_islem_hazirla(
    secim, *, kaynak, goruntu_id, manifest_ozeti, pay_kimligi=None, tablo_metni=None
):
    """TASARIM 5.15 #178: E1 ve tarihsel E5 aynı saf kaynak parserını kullanır."""
    ilk_islem_secimi_dogrula(secim)
    bag = dict(kaynak=kaynak, goruntu_id=goruntu_id, manifest_ozeti=manifest_ozeti)
    if any(secim[a] != v for a, v in bag.items()):
        raise VeriHatasi("ilk işlem kaynak/görüntü/manifest bağı uyuşmuyor")
    bayt = (
        (ILK_ISLEM_KOKU / secim["surum"] / "ilk_islem.csv").read_bytes()
        if tablo_metni is None
        else tablo_metni.encode("utf-8")
    )
    if hashlib.sha256(bayt).hexdigest() != secim["tablo_ozeti"]:
        raise VeriHatasi("ilk işlem tablo özeti uyuşmuyor")
    tablo = pd.read_csv(
        BytesIO(bayt), encoding="utf-8-sig", dtype=str, keep_default_na=False
    )
    alanlar = {
        "kaynak",
        "kaynak_sembolu",
        "borsa_kodu",
        "unvan",
        "ilk_islem_gunu",
        "yayim_tarihi",
        "kaynak_id",
        "kaynak_url",
        "goruntu_id",
        "manifest_ozeti",
    }
    if (
        set(tablo.columns) != alanlar
        or tablo.empty
        or tablo.apply(lambda x: x.str.strip()).eq("").any().any()
    ):
        raise VeriHatasi("ilk işlem tablosunun alanları geçersiz")
    if any(not tablo[a].eq(v).all() for a, v in bag.items()):
        raise VeriHatasi("ilk işlem tablosunun kaynak/görüntü/manifest bağı uyuşmuyor")
    kayitlar = {}
    for r in tablo.to_dict("records"):
        for ad in ("ilk_islem_gunu", "yayim_tarihi"):
            if dt.date.fromisoformat(r[ad]).isoformat() != r[ad]:
                raise VeriHatasi("ilk işlem kaynağında tarih geçersiz")
        pay = (
            pay_sembolleri([r["kaynak_sembolu"]], pay_kimligi)[0]
            if pay_kimligi
            else r["kaynak_sembolu"]
        )
        kod = _borsa_kodu(pay, r["ilk_islem_gunu"], pay_kimligi) if pay_kimligi else pay
        if pay in kayitlar or kod != r["borsa_kodu"]:
            raise VeriHatasi("ilk işlem kaynağında tekrarlı veya çelişkili pay")
        kayitlar[pay] = r
    return kayitlar


def ilk_islem_gecmis_kaniti(kayit, gunler, bitis):
    """TASARIM 5.15 #178: bağlı takvimin kesilmiş öneki; fiyat hesabı değildir."""
    ilk = kayit["ilk_islem_gunu"]
    gunler = list(gunler)
    if gunler != sorted(set(gunler)) or ilk not in gunler or ilk > bitis:
        raise VeriHatasi("ilk işlem için kayıtlı takvim öneki eksik")
    ozet = hashlib.sha256(
        "".join(t + "\n" for t in gunler if ilk <= t <= bitis).encode("utf-8")
    ).hexdigest()
    return dict(
        kaynak_id=kayit["kaynak_id"], ilk_islem_gunu=ilk, bitis=bitis, gozlem_ozeti=ozet
    )


def _ilk_islem_gozlemleri(istek, kayitlar, f, gunler, son, kapsam_bas):
    kanit = {}
    for pay in set(istek.semboller) & kayitlar.keys():
        r = kayitlar[pay]
        ilk = r["ilk_islem_gunu"]
        if kapsam_bas > pd.Timestamp(ilk):
            raise VeriHatasi(f"{pay}: ilk işlem geçmişi kırpılmış")
        kanit[pay] = ilk_islem_gecmis_kaniti(r, gunler, _tarih(son))
        beklenen = [t for t in gunler if ilk <= t <= _tarih(son)]
        g = f[(f["sembol"] == pay) & (f["tarih"] <= son)].sort_values("tarih")
        if list(g["tarih"].map(_tarih)) != beklenen or any(
            not np.isfinite(g[ad]).all() or not g[ad].gt(0).all()
            for ad in ("kapanis", "ham_kapanis")
        ):
            raise VeriHatasi(f"{pay}: ilk işlem geçmişi eksik veya geçersiz")
    return kanit


def pay_kimligi_hazirla(secim, *, kaynak, goruntu_id, manifest_ozeti, tablo_metni=None):
    """TASARIM 5.15 #167: yalnız kanıtlı sağlayıcı/görüntü için eşleme."""
    pay_kimligi_secimi_dogrula(secim)
    bag = dict(kaynak=kaynak, goruntu_id=goruntu_id, manifest_ozeti=manifest_ozeti)
    if any(secim[a] != deger for a, deger in bag.items()):
        raise VeriHatasi("pay kimliği kaynak/görüntü/manifest bağı uyuşmuyor")
    yol = PAY_KIMLIGI_KOKU / secim["surum"] / "eslemeler.csv"
    # TASARIM 5.15 #167: tarihsel kayıt aynı kaynak baytlarını saklar.
    bayt = yol.read_bytes() if tablo_metni is None else tablo_metni.encode("utf-8")
    if tablo_metni is not None and hashlib.sha256(
        bayt
    ).hexdigest() != _YAYIMLANMIS_KAYNAK_OZETLERI.get(secim["surum"]):
        raise VeriHatasi("pay kimliği sürümünün onaylı kaynak özeti uyuşmuyor")
    if hashlib.sha256(bayt).hexdigest() != secim["tablo_ozeti"]:
        raise VeriHatasi("pay kimliği tablo özeti uyuşmuyor")
    tablo = pd.read_csv(
        BytesIO(bayt), encoding="utf-8-sig", dtype=str, keep_default_na=False
    )
    if (
        set(tablo.columns)
        != {
            "pay_id",
            "kaynak",
            "kaynak_sembolu",
            "borsa_kodu",
            "baslangic",
            "bitis",
            "goruntu_id",
            "manifest_ozeti",
            "kaynak_id",
        }
        or tablo.empty
    ):
        raise VeriHatasi("pay kimliği tablosunun alanları geçersiz")
    if any(not tablo[a].eq(v).all() for a, v in bag.items()):
        raise VeriHatasi(
            "pay kimliği tablosunun kaynak/görüntü/manifest bağı uyuşmuyor"
        )
    zorunlu = ["pay_id", "kaynak_sembolu", "borsa_kodu", "kaynak_id"]
    if tablo[zorunlu].apply(lambda x: x.str.strip()).eq("").any().any():
        raise VeriHatasi("pay kimliği tablosunda zorunlu alan boş")
    kayitlar, etiketler = [], {}
    for r in tablo.to_dict("records"):
        try:
            for ad in ("baslangic", "bitis"):
                r[ad] = dt.date.fromisoformat(r[ad]) if r[ad] else None
        except ValueError as hata:
            raise VeriHatasi("pay kimliği aralığında tarih geçersiz") from hata
        if r["baslangic"] and r["bitis"] and r["baslangic"] >= r["bitis"]:
            raise VeriHatasi("pay kimliği aralığı ters")
        for etiket in (r["kaynak_sembolu"], r["borsa_kodu"], r["pay_id"]):
            if etiket in etiketler and etiketler[etiket] != r["pay_id"]:
                raise VeriHatasi("pay kimliği etiketi iki paya bağlı")
            etiketler[etiket] = r["pay_id"]
        kayitlar.append(r)
    for pay in tablo["pay_id"].unique():
        araliklar = sorted(
            (r for r in kayitlar if r["pay_id"] == pay),
            key=lambda r: r["baslangic"] or dt.date.min,
        )
        if len({r["kaynak_sembolu"] for r in araliklar}) != 1:
            raise VeriHatasi("bir payın birden fazla kaynak sembolü var")
        if (
            araliklar[0]["baslangic"] is not None
            or araliklar[-1]["bitis"] is not None
            or any(
                a["bitis"] is None or a["bitis"] != b["baslangic"]
                for a, b in zip(araliklar, araliklar[1:], strict=False)
            )
        ):
            raise VeriHatasi("pay kimliği aralıkları eksik veya çakışıyor")
    return dict(secim=deepcopy(secim), kayitlar=kayitlar, etiketler=etiketler)


def pay_sembolleri(semboller, politika):
    """TASARIM 5.15 #167: açık seçimde bir pay iki kez istenemez."""
    sonuc = [politika["etiketler"].get(s, s) for s in semboller]
    if len(set(sonuc)) != len(sonuc):
        raise VeriHatasi("pay kimliği isteğinde tekrarlı pay")
    return sonuc


def _borsa_kodu(pay, tarih, politika):
    tarih = pd.Timestamp(tarih).date()
    for r in politika["kayitlar"]:
        if (
            r["pay_id"] == pay
            and (r["baslangic"] is None or r["baslangic"] <= tarih)
            and (r["bitis"] is None or tarih < r["bitis"])
        ):
            return r["borsa_kodu"]
    return pay


def pay_uyeligi(uyelik, politika):
    """TASARIM 5.15 #167: özgün üyelik kanıtı korunur; yalnız pay anahtarı eklenir."""
    sonuc = deepcopy(uyelik)
    for tarih, gun in sonuc["gunler"].items():
        if (
            len(gun["semboller"]) != 30
            or len(gun["kanitlar"]) != 30
            or set(gun["semboller"]) != {k["sembol"] for k in gun["kanitlar"]}
        ):
            raise VeriHatasi("üyelikte 30 ayrı pay ve eşleşen kanıt gerekli")
        gun["semboller"] = sorted(pay_sembolleri(gun["semboller"], politika))
        for kanit in gun["kanitlar"]:
            pay = politika["etiketler"].get(kanit["sembol"], kanit["sembol"])
            if _borsa_kodu(pay, tarih, politika) != kanit["sembol"]:
                raise VeriHatasi("üyelik borsa kodu pay kimliği tarihiyle uyuşmuyor")
            kanit["pay_id"] = pay
    sonuc["pay_kimligi"] = deepcopy(politika["secim"])
    return sonuc


def pay_kimligi_uygula(anlik, politika):
    """TASARIM 5.15 #167: bütün görüntü fiyat/olay anahtarları kalite öncesi çözülür."""
    kaynaklar = pd.concat([anlik.fiyat["sembol"], anlik.olaylar["sembol"]]).unique()
    pay_sembolleri(kaynaklar, politika)
    beklenen = {r["pay_id"]: r["kaynak_sembolu"] for r in politika["kayitlar"]}
    for s in kaynaklar:
        pay = politika["etiketler"].get(s, s)
        if pay in beklenen and s != beklenen[pay]:
            raise VeriHatasi("pay kimliğinin kaynak sembolü uyuşmuyor")

    def yansit(tablo):
        t = tablo.copy()
        t["kaynak_sembolu"] = t["sembol"]
        t["sembol"] = t["sembol"].map(lambda s: politika["etiketler"].get(s, s))
        t["borsa_kodu"] = t["sembol"]
        for r in politika["kayitlar"]:
            maske = t["sembol"].eq(r["pay_id"])
            if r["baslangic"] is not None:
                maske &= t["tarih"] >= pd.Timestamp(r["baslangic"])
            if r["bitis"] is not None:
                maske &= t["tarih"] < pd.Timestamp(r["bitis"])
            t.loc[maske, "borsa_kodu"] = r["borsa_kodu"]
        return t

    fiyat, olaylar = yansit(anlik.fiyat), yansit(anlik.olaylar)
    if fiyat.duplicated(["sembol", "tarih"]).any():
        raise VeriHatasi("pay kimliğinde tekrarlı fiyat günü")
    return replace(anlik, fiyat=fiyat, olaylar=olaylar)


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
    evren_politikasi: str | None = None
    pay_kimligi: dict | None = None
    ilk_islem: dict | None = None


def veri_hazirla(istek: VeriIstegi, kimlik, kok) -> dict:
    """Doğrulanmış yerel görüntüyü E1 kayıtlarına uyarlar (TASARIM 5.15)."""
    bas, son, kapsam_bas = _istek_donemi(istek)
    a = oku(kimlik, kok)
    politika = None
    if istek.pay_kimligi is not None:
        politika = pay_kimligi_hazirla(
            istek.pay_kimligi,
            kaynak=istek.kaynak,
            goruntu_id=kimlik,
            manifest_ozeti=_sha256(Path(kok) / "ag" / kimlik / "manifest.json"),
        )
        a = pay_kimligi_uygula(a, politika)
        istek = replace(
            istek, semboller=tuple(pay_sembolleri(istek.semboller, politika))
        )
    ilk_islem = None
    if istek.ilk_islem is not None:
        ilk_islem = ilk_islem_hazirla(
            istek.ilk_islem,
            kaynak=istek.kaynak,
            goruntu_id=kimlik,
            manifest_ozeti=_sha256(Path(kok) / "ag" / kimlik / "manifest.json"),
            pay_kimligi=politika,
        )
    gunler = a.gunler[a.gunler <= son]
    uyelik = None
    if istek.evren_politikasi is not None:
        uyelik = uyelik_hazirla(
            UyelikIstegi(
                tuple(
                    dict.fromkeys(
                        [_tarih(bas), *map(_tarih, gunler[gunler >= bas]), _tarih(son)]
                    )
                ),
                istek.evren_politikasi,
                istek.uyelik_surumu,
            )
        )
    if uyelik is not None and politika is not None:
        uyelik = pay_uyeligi(uyelik, politika)
    semboller = list(istek.semboller)
    f = a.fiyat[a.fiyat["sembol"].isin(semboller)]
    hesap = a.hesap_fiyati[a.hesap_fiyati["sembol"].isin(semboller)]
    C, A = (
        hesap.pivot(index="tarih", columns="sembol", values=ad)
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
            **(
                dict(kaynak_sembolu=r.kaynak_sembolu, borsa_kodu=r.borsa_kodu)
                if politika is not None
                else {}
            ),
        }
        for i, r in enumerate(a.olaylar.itertuples())
        if r.sembol in semboller and kapsam_bas <= r.tarih <= son
    ]
    piyasa = _piyasa_satirlari(istek, kimlik, f, g, d, secilen, olaylar, meta, politika)
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
    referans = _veri_referansi(istek, kimlik, kok, meta, fiili)
    if uyelik is not None:
        referans.update(
            evren_politikasi=istek.evren_politikasi,
            uyelik_tablo_parmak_izi=uyelik["tablo_parmak_izi"],
        )
    if politika is not None:
        referans["pay_kimligi"] = deepcopy(istek.pay_kimligi)
        ozet = hashlib.sha256(
            json.dumps(istek.pay_kimligi, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest()
        referans["kayit_id"] += f"/{ozet}"
    if ilk_islem is not None:
        referans["ilk_islem"] = deepcopy(istek.ilk_islem)
        referans["gecmis_kaniti"] = _ilk_islem_gozlemleri(
            istek, ilk_islem, f, list(map(_tarih, gunler)), son, kapsam_bas
        )
        ozet = hashlib.sha256(
            json.dumps(istek.ilk_islem, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest()
        referans["kayit_id"] += f"/{ozet}"
    return {
        **({"uyelik": uyelik} if uyelik is not None else {}),
        "piyasa": piyasa,
        "olaylar": olaylar,
        "kaynaklar": kaynaklar,
        "semboller": semboller,
        "gunler": [_tarih(t) for t in gunler[secilen]],
        "referans": referans,
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
    if istek.ilk_islem is not None:
        ilk_islem_secimi_dogrula(istek.ilk_islem)
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


def _piyasa_satirlari(istek, kimlik, f, g, d, secilen, olaylar, meta, politika=None):
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
                _piyasa_satiri(
                    istek, kimlik, s, t, r, k, d, q, j, olay_ref, meta, politika
                )
            )
    return piyasa


def _piyasa_satiri(istek, kimlik, s, t, r, k, d, q, j, olay_ref, meta, politika=None):
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
    pay_alanlari = {}
    if politika is not None:
        kaynak = next(
            (r["kaynak_sembolu"] for r in politika["kayitlar"] if r["pay_id"] == s), s
        )
        pay_alanlari = dict(
            kaynak_sembolu=kaynak, borsa_kodu=_borsa_kodu(s, t, politika)
        )
    satir = {
        **meta,
        "kayit_id": f"{kimlik}/{s}/{t.date()}/{istek.kalite_surumu}",
        "kayit_turu": "piyasa_satiri",
        "sembol": s,
        **pay_alanlari,
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
    def hesap_fiyati(self) -> pd.DataFrame:
        """Eksik günün hesap girdisi NaN'dır; gözlenmiş fiyat korunur (TASARIM 5.13)."""
        f = self.fiyat.copy()
        eksik = self.gun_tablosu.set_index(["sembol", "tarih"])["eksik"]
        maske = eksik.reindex(
            pd.MultiIndex.from_frame(f[["sembol", "tarih"]])
        ).to_numpy()
        alanlar = f.columns.intersection([*FIYAT_SUTUNLARI, "ham_acilis", "acilis"])
        f.loc[maske, alanlar] = np.nan
        return f

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


def indir(
    semboller,
    kok,
    kaynak,
    simdi=None,
    bas=BASLANGIC,
    borsapy=None,
    *,
    kapanan: pd.DataFrame | None = None,
) -> str:
    """Sembollerin fiyat ve olaylarını indirir, anlık görüntüyü yazar, kimliğini döndürür.

    `borsapy` verilirse faiz ve sektör tabloları da anlık görüntüye girer; boş faiz serisi hatadır.
    `kapanan` verilirse kanıt yayın öncesinde manifeste girer (TASARIM 4)."""
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
    if kapanan is not None:
        kapanan.to_csv(gecici / "kapanan.csv", index=False, encoding="utf-8-sig")
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
        try:
            gercek_ozet = _sha256(klasor / ad)
        except FileNotFoundError as hata:
            raise VeriHatasi(f"manifest dosyası eksik: {kimlik}/{ad}") from hata
        if gercek_ozet != ozet:
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
        & f[
            "hacim"
        ].notna()  # TASARIM 5.13: hacim NaN kısmi satır ihlalidir, 0 değildir.
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
    for tarih, grup in olaylar[olaylar["kod"].isin(LIMIT_OLAY_KODLARI)].groupby(
        "tarih"
    ):
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
