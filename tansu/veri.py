"""Veri deposu: indirme → değişmez anlık görüntü → doğrulanmış okuma; olay denetimi (TASARIM 4, 5.1)."""

import datetime as dt
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
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
FIYAT_SUTUNLARI = ["ham_kapanis", "ham_aof", "ham_yuksek", "ham_dusuk", "kapanis", "aof", "yuksek", "dusuk", "hacim"]
KARANTINA_ESIK, DENETIM_ESIK, INMEYEN_ESIK = 0.01, 0.02, 5  # TASARIM 5.13


class VeriHatasi(Exception):
    pass


@dataclass(frozen=True)
class Anlik:
    kimlik: str
    fiyat: pd.DataFrame  # uzun biçim: sembol, tarih, ham_* ve düzeltilmiş sütunlar
    olaylar: pd.DataFrame  # sembol, tarih, kod, carpan
    faiz: pd.DataFrame = None  # tarih, faiz (yüzde); yalnız değişim günleri
    sektor: dict = None  # sembol → KAP sektörü
    inmeyen: tuple = ()  # indirilemeyen semboller
    bos: tuple = ()  # kaynağın veri döndürmediği semboller (hata değil: pay olmayan kod, işlem görmemiş)

    @property
    def gun_tablosu(self) -> pd.DataFrame:
        """Sembol × takvim günü: islem, eksik, limit, tavan, taban, kilit_*, karantina (TASARIM 5.1)."""
        takvim = pd.DatetimeIndex(sorted(self.fiyat["tarih"].unique()))
        parcalar = [
            _gunler(f, self.olaylar[self.olaylar["sembol"] == s], takvim).assign(sembol=s)
            for s, f in self.fiyat.groupby("sembol", sort=False)
        ]
        return pd.concat(parcalar).rename_axis("tarih").reset_index()

    @property
    def sorunlar(self) -> list:
        """Oran eşiklerini aşan kapılar (TASARIM 5.13); boş liste = veri temiz."""
        n, sonuc = len(self.fiyat), []
        if self.gun_tablosu["karantina"].sum() / n > KARANTINA_ESIK:
            sonuc.append("karantina oranı > %1")
        if len(self.olay_uyarilari) / n > DENETIM_ESIK:
            sonuc.append("olay denetimi farkı olan gün oranı > %2")
        if len(self.inmeyen) > INMEYEN_ESIK:
            sonuc.append(f"{len(self.inmeyen)} hisse inmedi")
        return sonuc

    @property
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
            raise VeriHatasi(f"faiz serisi {s.index[s.isna()][0].date()} gününü kapsamıyor")
        return s

    @property
    def olay_uyarilari(self) -> pd.DataFrame:
        parcalar = [
            _olay_denetimi(f, self.olaylar[self.olaylar["sembol"] == s]).assign(sembol=s)
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
            f, ham_olaylar[s] = kaynak.fiyat(s, bas, simdi.date()).assign(sembol=s), kaynak.olaylar(s)
        except KaynakHatasi:
            ham_olaylar.pop(s, None)
            inmeyen.append(s)
            continue
        if not f.empty:  # hacmi ve ham alanları NaN/0 olan satır işlem yapılmamış gündür; aynı tekrar satır tek sayılır
            f = f.drop_duplicates()
            f = f[~(f[[*FIYAT_SUTUNLARI[:4], "hacim"]].fillna(0) == 0).all(axis=1)]
        if f.empty:
            del ham_olaylar[s]
            bos.append(s)
            continue
        _yapi_denetimi(s, f)
        fiyatlar.append(f)
    if not fiyatlar:
        raise VeriHatasi("hiçbir sembol inmedi")
    if borsapy:
        faiz = borsapy.faiz()
        if faiz.empty:
            raise VeriHatasi("faiz serisi boş")
        sektor = {}
        for f in fiyatlar:
            s = f["sembol"].iloc[0]
            try:
                sektor[s] = borsapy.sektor(s)
            except KaynakHatasi:  # sektörü olmayan hisse çifte girmez (TASARIM 5.2); indirme durmaz
                pass
    shutil.rmtree(gecici, ignore_errors=True)
    gecici.mkdir(parents=True)
    if borsapy:
        faiz.to_parquet(gecici / "faiz.parquet", index=False)
        (gecici / "sektor.json").write_text(json.dumps(sektor, ensure_ascii=False), encoding="utf-8")
    pd.concat(fiyatlar, ignore_index=True).to_parquet(gecici / "fiyat.parquet", index=False)
    (gecici / "olaylar.json").write_text(json.dumps(ham_olaylar, ensure_ascii=False), encoding="utf-8")
    manifest = {"kimlik": kimlik, "semboller": [s for s in semboller if s not in inmeyen + bos], "inmeyen": inmeyen,
                "bos": bos,
                "dosyalar": {p.name: _sha256(p) for p in sorted(gecici.iterdir())}}
    (gecici / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    os.replace(gecici, hedef)
    return kimlik


def oku(kimlik, kok) -> Anlik:
    """Manifesti doğrular; uyuşmazlık VeriHatasi'dır."""
    klasor = Path(kok) / "ag" / kimlik
    manifest = json.loads((klasor / "manifest.json").read_text(encoding="utf-8"))
    for ad, ozet in manifest["dosyalar"].items():
        if _sha256(klasor / ad) != ozet:
            raise VeriHatasi(f"manifest uyuşmuyor: {kimlik}/{ad}")
    ham = json.loads((klasor / "olaylar.json").read_text(encoding="utf-8"))
    olaylar = pd.DataFrame(
        [{"sembol": s, "tarih": _olay_tarihi(o["SHHE_TARIH"]), "kod": o["SHT_KODU"],
          "carpan": float(o["SHHE_FIYAT_AYAR_OR"])} for s, liste in ham.items() for o in liste
         if o["SHHE_TARIH"] > 0 and o["SHHE_FIYAT_AYAR_OR"] > 0],  # yer tutucu kayıt düzeltme taşımaz
        columns=["sembol", "tarih", "kod", "carpan"])
    faiz = pd.read_parquet(klasor / "faiz.parquet") if "faiz.parquet" in manifest["dosyalar"] else None
    sektor = (json.loads((klasor / "sektor.json").read_text(encoding="utf-8"))
              if "sektor.json" in manifest["dosyalar"] else None)
    return Anlik(kimlik, pd.read_parquet(klasor / "fiyat.parquet"), olaylar, faiz, sektor,
                 tuple(manifest.get("inmeyen", [])), tuple(manifest.get("bos", [])))


def _sha256(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()


def _olay_tarihi(ms) -> pd.Timestamp:
    return pd.Timestamp(dt.datetime.fromtimestamp(ms / 1000, ISTANBUL).date())


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
        if len(gunler) == 0 or tarih < gunler[0]:  # pencereden önceki olay hiçbir satırı etkilemez
            continue
        i = gunler.searchsorted(tarih)  # olay tarihine eşit ya da sonraki ilk işlem günü
        if i < len(gunler):  # pencereden sonraki olay bütün satırlara uygulanır, kaydırılmaz
            adaylar = [j for j in (i - 1, i, i + 1) if 1 <= j < len(gunler)]
            if adaylar:
                i = min(adaylar, key=lambda j: abs(oran[j - 1] / oran[j] / carpan - 1))
        beklenen[beklenen.index < i] *= carpan
    fark = oran / beklenen.to_numpy() - 1
    uyari = abs(fark) > OLAY_TOLERANS
    return pd.DataFrame({"tarih": f["tarih"][uyari], "gozlenen": oran[uyari],
                         "beklenen": beklenen[uyari], "fark": fark[uyari]}).reset_index(drop=True)


def adim(fiyat, tarih):
    """Fiyat adımı (TASARIM 5.1 tablosu); fiyat ve tarih dizi olabilir."""
    i = np.searchsorted(ADIM_ESIK, fiyat, side="right")
    return np.where(np.asarray(tarih) >= ADIM_DEGISIM, np.array(ADIM_YENI)[i], np.array(ADIM_ESKI)[i])


def _yapi_denetimi(sembol, f):
    """Bozuk sıra, tekrar eden gün ya da ortada NaN indirmeyi durdurur (TASARIM 5.13)."""
    if not f["tarih"].is_monotonic_increasing:
        raise VeriHatasi(f"{sembol}: tarih sırası bozuk")
    if f["tarih"].duplicated().any():
        raise VeriHatasi(f"{sembol}: tekrar eden gün")
    if f[FIYAT_SUTUNLARI].isna().any().any():
        raise VeriHatasi(f"{sembol}: ortada NaN")


def _gunler(fiyat, olaylar, takvim):
    f = fiyat.sort_values("tarih").set_index("tarih")
    f = f.reindex(takvim[(takvim >= f.index[0]) & (takvim <= f.index[-1])])
    var = f["ham_kapanis"].notna()  # eksik gün NaN kalır, doldurulmaz
    islem = var & (f["hacim"] > 0)
    bozuk = var & ~(
        (f[FIYAT_SUTUNLARI[:8]] > 0).all(axis=1)
        & (f["ham_dusuk"] <= f["ham_aof"]) & (f["ham_aof"] <= f["ham_yuksek"])
        & (f["ham_dusuk"] <= f["ham_kapanis"]) & (f["ham_kapanis"] <= f["ham_yuksek"])
        & (f["dusuk"] * (1 - YUVARLAMA) <= f["aof"]) & (f["aof"] <= f["yuksek"] * (1 + YUVARLAMA))
        & (f["dusuk"] * (1 - YUVARLAMA) <= f["kapanis"]) & (f["kapanis"] <= f["yuksek"] * (1 + YUVARLAMA)))
    ok = islem & ~bozuk
    onceki = f["ham_kapanis"].where(ok).ffill().shift(1)
    carpan = pd.Series(1.0, index=f.index)
    oran = (f["kapanis"] / f["ham_kapanis"]).where(ok)  # düzeltme oranı; sıçradığı gün gerçek olay günüdür
    oran_onceki = oran.ffill().shift(1)
    gunler = f.index[islem.to_numpy()]
    for tarih, grup in olaylar.groupby("tarih"):
        c = grup["carpan"].prod()
        i = gunler.searchsorted(tarih)  # olay gününe eşit ya da sonraki işlem günü
        if i < len(gunler):
            if c != 1:  # tablo tarihi bir işlem günü kayabilir (5.1): kapanışı en iyi tutan gün seçilir
                adaylar = [j for j in (i, i - 1, i + 1) if 0 <= j < len(gunler)]
                fark = {j: abs(oran_onceki[gunler[j]] / oran[gunler[j]] / c - 1) for j in adaylar}
                if fark[i] > OLAY_TOLERANS:  # tablo günü oranı tutmuyorsa (NaN: bilinmiyor, kaydırma yok)
                    i = min(adaylar, key=lambda j: np.inf if np.isnan(fark[j]) else fark[j])
            carpan[gunler[i]] *= c
    limit = pd.Series(np.where(f.index >= LIMIT_DEGISIM, 0.10, 0.20), index=f.index)
    ref = onceki * carpan
    tavan, taban, kapanis = ref * (1 + limit), ref * (1 - limit), f["ham_kapanis"]
    asim = (kapanis > tavan * (1 + LIMIT_TOLERANS)) | (kapanis < taban * (1 - LIMIT_TOLERANS))
    karantina = bozuk | (ok & asim)
    temiz = ok & ~karantina
    kilit_tavan = temiz & (kapanis >= tavan - adim(tavan, f.index) - 1e-9)
    kilit_taban = temiz & (kapanis <= taban + adim(taban, f.index) + 1e-9)
    duyarli = f["ham_dusuk"] == f["ham_yuksek"]
    return pd.DataFrame({
        "islem": islem, "eksik": ~var, "limit": limit, "tavan": tavan, "taban": taban,
        "kilit_tavan": kilit_tavan, "kilit_taban": kilit_taban,
        "kilit_tavan_duyarli": kilit_tavan & duyarli, "kilit_taban_duyarli": kilit_taban & duyarli,
        "karantina": karantina})
