"""Veri deposu: indirme → değişmez anlık görüntü → doğrulanmış okuma; olay denetimi (TASARIM 4, 5.1)."""

import datetime as dt
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ISTANBUL = ZoneInfo("Europe/Istanbul")
BASLANGIC = dt.date(2010, 1, 1)
OLAY_TOLERANS = 0.005  # TASARIM 5.1: olay denetiminde %0,5


class VeriHatasi(Exception):
    pass


@dataclass(frozen=True)
class Anlik:
    kimlik: str
    fiyat: pd.DataFrame  # uzun biçim: sembol, tarih, ham_* ve düzeltilmiş sütunlar
    olaylar: pd.DataFrame  # sembol, tarih, kod, carpan
    faiz: pd.DataFrame = None  # tarih, faiz (yüzde); yalnız değişim günleri
    sektor: dict = None  # sembol → KAP sektörü

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
    fiyatlar, ham_olaylar = [], {}
    for s in semboller:
        fiyatlar.append(kaynak.fiyat(s, bas, simdi.date()).assign(sembol=s))
        ham_olaylar[s] = kaynak.olaylar(s)
    if borsapy:
        faiz = borsapy.faiz()
        if faiz.empty:
            raise VeriHatasi("faiz serisi boş")
        sektor = {s: borsapy.sektor(s) for s in semboller}
    shutil.rmtree(gecici, ignore_errors=True)
    gecici.mkdir(parents=True)
    if borsapy:
        faiz.to_parquet(gecici / "faiz.parquet", index=False)
        (gecici / "sektor.json").write_text(json.dumps(sektor, ensure_ascii=False), encoding="utf-8")
    pd.concat(fiyatlar, ignore_index=True).to_parquet(gecici / "fiyat.parquet", index=False)
    (gecici / "olaylar.json").write_text(json.dumps(ham_olaylar, ensure_ascii=False), encoding="utf-8")
    manifest = {"kimlik": kimlik, "semboller": list(semboller),
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
          "carpan": float(o["SHHE_FIYAT_AYAR_OR"])} for s, liste in ham.items() for o in liste],
        columns=["sembol", "tarih", "kod", "carpan"])
    faiz = pd.read_parquet(klasor / "faiz.parquet") if "faiz.parquet" in manifest["dosyalar"] else None
    sektor = (json.loads((klasor / "sektor.json").read_text(encoding="utf-8"))
              if "sektor.json" in manifest["dosyalar"] else None)
    return Anlik(kimlik, pd.read_parquet(klasor / "fiyat.parquet"), olaylar, faiz, sektor)


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
