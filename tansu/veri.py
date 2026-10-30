"""Veri deposu: indirme → değişmez anlık görüntü → doğrulanmış okuma; olay denetimi (TASARIM 4, 5.1)."""

import datetime as dt
import hashlib
import json
import os
import shutil
from io import BytesIO
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
KARANTINA_GUN = 250  # TASARIM 5.1: karantinadan sonra yeni sinyal yok
YUVARLAMA = 1e-4  # TASARIM 5.13: düzeltilmiş seri 4 ondalığa yuvarlı
YARIM_BIRIM = 5e-5  # 4 ondalık yuvarlamanın mutlak farkı; 0,5 TL altındaki fiyatta bağıl pay bunu karşılamaz
LIMIT_DEGISIM = pd.Timestamp("2020-03-13")  # ±%20 → ±%10
# Tek seans: öncesi iki seans, seans başına ±%10, sınırlar dışa yuvarlı (BİST duyurusu 11699; BISTECH 2.1.2).
# SPEC 3.9 istisnası, Levent 30.10.2026.
TEK_SEANS = pd.Timestamp("2015-11-30")
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
    "bist30_2026_v1": "1768ebf77b9dc4ac180962848782a92b9c6b7885e9a5e3132fd0f00ebbfd8274",
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


# Her üyelik sürümü kendi tarih aralığını taşır; boş `bitis` aralığın son günü demektir (SPEC 3.2).
UYELIK_SURUMLERI = {
    "bist30_2021_2025_v1": (pd.Timestamp("2021-01-01"), pd.Timestamp("2025-12-31")),
    "bist30_2026_v1": (pd.Timestamp("2026-01-01"), pd.Timestamp("2026-12-31")),
}


def _uyelik_tablosu(yol, son):
    tablo = pd.read_csv(yol, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    if set(tablo.columns) != {"sembol", "baslangic", "bitis", "kaynak_id"}:
        raise VeriHatasi("üyelik tablosu sütunları geçersiz")
    if tablo[["sembol", "baslangic", "kaynak_id"]].eq("").any().any():
        raise VeriHatasi("üyelik tablosunda zorunlu alan boş")
    try:
        tablo["bas"] = pd.to_datetime(tablo["baslangic"], format="%Y-%m-%d")
        tablo["son"] = pd.to_datetime(
            tablo["bitis"].replace("", str((son + pd.Timedelta(days=1)).date())),
            format="%Y-%m-%d",
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
    if (
        istek.evren_politikasi != "donemsel_bist30_v1"
        or istek.uyelik_surumu not in UYELIK_SURUMLERI
    ):
        raise VeriHatasi("bilinmeyen evren politikası/üyelik sürümü")
    kapsam_bas, kapsam_son = UYELIK_SURUMLERI[istek.uyelik_surumu]
    yol = Path(__file__).parent / "referans" / istek.uyelik_surumu / "uyelik.csv"
    if tablo_metni is not None and hashlib.sha256(
        tablo_metni.encode("utf-8")
    ).hexdigest() != _YAYIMLANMIS_KAYNAK_OZETLERI.get(istek.uyelik_surumu):
        raise VeriHatasi("üyelik sürümünün onaylı kaynak özeti uyuşmuyor")
    # TASARIM 5.15 #167: kayıtlı kaynak aynı parserdan dosyasız geçer.
    tablo = _uyelik_tablosu(
        yol if tablo_metni is None else BytesIO(tablo_metni.encode("utf-8")),
        kapsam_son,
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
        if not kapsam_bas <= t <= kapsam_son or len(kayitlar) != 30:
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
        """Eksik ya da bozuk (fiyat 0, tutarsız OHLC) günün hesap girdisi NaN'dır; gözlenmiş fiyat korunur
        (TASARIM 5.13). Bozuk gün karantinada kalır; motor ve göstergeler onun fiyatını görmez."""
        f = self.fiyat.copy()
        g = self.gun_tablosu.set_index(["sembol", "tarih"])
        eksik = g["eksik"] | g["bozuk"]
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


def uyelik_araliklari() -> pd.DataFrame:
    """Bütün sürümlerin BIST 30 aralıkları: sembol (İş Yatırım kodu), bas, son (dahil). Adlı katmandır; sınama
    evreni bütün BIST'tir (SPEC 2).

    Borsa kodu `pay_kimligi_v1` ile şirketin tek koduna çevrilir: KOZAL → TRALT, KOZAA → TRMET (SPEC 3.3)."""
    esleme = pd.read_csv(
        PAY_KIMLIGI_KOKU / "pay_kimligi_v1" / "eslemeler.csv",
        dtype=str,
        keep_default_na=False,
    )
    kod = dict(zip(esleme["borsa_kodu"], esleme["kaynak_sembolu"], strict=True))
    parcalar = [
        _uyelik_tablosu(Path(__file__).parent / "referans" / surum / "uyelik.csv", son)
        for surum, (_, son) in UYELIK_SURUMLERI.items()
    ]
    t = pd.concat(parcalar, ignore_index=True)
    return t.assign(sembol=t["sembol"].map(lambda s: kod.get(s, s)))[
        ["sembol", "bas", "son"]
    ]


def uyelik_bitisi() -> pd.Timestamp:
    """Üyelik tablosunun son günü (SPEC 3.2)."""
    return max(son for _, son in UYELIK_SURUMLERI.values())


def gunluk(anlik: Anlik, sembol: str) -> pd.DataFrame:
    """Bir sembolün günlük tablosu; stratejiler ve motor yalnız bunu okur (SPEC 3.7).

    Fiyatlar düzeltilmiş (`ham_*` hariç); eksik gün NaN. `kilit_*` yüksek = düşük olan limit günleri,
    `tavan_kapanis` tavanda kapanış. `karantina`: karantina gününden sonraki `KARANTINA_GUN` gün yeni sinyal yok.
    `uye`: evren bütün BIST'tir; sembol ilk ve son satırı arasındaki her gün evrendedir (SPEC 2, 3.7)."""
    g = anlik.gun_tablosu
    g = g[g["sembol"] == sembol].set_index("tarih").sort_index()
    if g.empty:
        raise VeriHatasi(f"{sembol}: anlık görüntüde yok")
    f = anlik.hesap_fiyati
    f = f[f["sembol"] == sembol].set_index("tarih").reindex(g.index)
    karantina = (
        g["karantina"]
        .astype(float)
        .rolling(KARANTINA_GUN, min_periods=1)
        .max()
        .astype(bool)
    )
    return pd.DataFrame(
        {
            "aof": f["aof"],
            "yuksek": f["yuksek"],
            "dusuk": f["dusuk"],
            "kapanis": f["kapanis"],
            "hacim": f["hacim"],
            "ham_yuksek": f["ham_yuksek"],
            "ham_dusuk": f["ham_dusuk"],
            "ham_kapanis": f["ham_kapanis"],
            "kilit_tavan": g["kilit_tavan_duyarli"].astype(bool),
            "kilit_taban": g["kilit_taban_duyarli"].astype(bool),
            "tavan_kapanis": g["kilit_tavan"].astype(bool),
            "karantina": karantina,
            "uye": True,
            "xu100": f["xu100"],
        },
        index=g.index.rename("tarih"),
    )


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
    alt = f["dusuk"] * (1 - YUVARLAMA) - YARIM_BIRIM
    ust = f["yuksek"] * (1 + YUVARLAMA) + YARIM_BIRIM
    bozuk = var & ~(
        (f[FIYAT_SUTUNLARI[:8]] > 0).all(axis=1)
        & f[
            "hacim"
        ].notna()  # TASARIM 5.13: hacim NaN kısmi satır ihlalidir, 0 değildir.
        & (f["ham_dusuk"] <= f["ham_aof"])
        & (f["ham_aof"] <= f["ham_yuksek"])
        & (f["ham_dusuk"] <= f["ham_kapanis"])
        & (f["ham_kapanis"] <= f["ham_yuksek"])
        & (alt <= f["aof"])
        & (f["aof"] <= ust)
        & (alt <= f["kapanis"])
        & (f["kapanis"] <= ust)
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
    iki_seans = f.index < TEK_SEANS
    limit = pd.Series(
        np.where((f.index >= LIMIT_DEGISIM) | iki_seans, 0.10, 0.20), index=f.index
    )
    ref = onceki * carpan
    tavan, taban, kapanis = ref * (1 + limit), ref * (1 - limit), f["ham_kapanis"]
    # İki seansta ikinci seansın sınırı birincinin sınırından ölçülür; her sınır en çok bir adım dışa yuvarlanır.
    s1, s2 = tavan + adim(tavan, f.index), taban - adim(taban, f.index)
    gun_tavan = tavan.where(~iki_seans, s1 * 1.1 + adim(s1 * 1.1, f.index))
    gun_taban = taban.where(~iki_seans, s2 * 0.9 - adim(s2 * 0.9, f.index))
    asim = (kapanis > gun_tavan * (1 + LIMIT_TOLERANS)) | (
        kapanis < gun_taban * (1 - LIMIT_TOLERANS)
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
            "bozuk": bozuk,
        }
    )
