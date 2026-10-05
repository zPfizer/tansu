"""Kanıt raporu: her aileyi bütün evrende sınar, rastgele girişle ve ayrılmış dönemle karşılaştırır.

Çalıştırma: python -m tansu.rapor  ->  rapor/kanit-<tarih>.md
"""
import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd

from tansu import veri
from tansu.aileler import AILELER
from tansu.kanit import islemler, ozet
from tansu.nabiz import BEKLE, nabiz

AYRILMIS = pd.Timestamp("2023-01-01")
RASTGELE_TEKRAR = 5
KLASOR = Path(__file__).resolve().parent.parent / "rapor"


def rastgele_sinyal(sinyal: pd.Series, izin: pd.Series, tohum: int) -> pd.Series:
    """Ailenin her dönemdeki sinyal sayısı kadar, izinli günlerden rastgele gün seçer."""
    rng = np.random.default_rng(tohum)
    sonuc = pd.Series(False, index=sinyal.index)
    for donem in (sinyal.index < AYRILMIS, sinyal.index >= AYRILMIS):
        adet = int(sinyal[donem].sum())
        aday = sinyal.index[donem & izin.values]
        if adet and len(aday):
            sonuc[rng.choice(aday, size=min(adet, len(aday)), replace=False)] = True
    return sonuc


def sina(fiyatlar: dict[str, pd.DataFrame], durum: pd.Series) -> pd.DataFrame:
    satirlar = []
    for aile in AILELER.values():
        for sembol, f in fiyatlar.items():
            izin = (durum.reindex(f.index).fillna(BEKLE) != BEKLE) & f["Close"].rolling(200).count().eq(200)
            sinyal = aile.sinyal(f) & izin
            for tur, s in [("aile", sinyal)] + [
                ("rastgele", rastgele_sinyal(sinyal, izin, t)) for t in range(RASTGELE_TEKRAR)
            ]:
                t = islemler(f, s)
                t["aile"], t["sembol"], t["tur"] = aile.ad, sembol, tur
                satirlar.append(t)
    return pd.concat(satirlar, ignore_index=True)


def tablo(tum: pd.DataFrame) -> str:
    kapali = tum[~tum["acik"]]
    satir = ["| Aile | Dönem | Tür | İşlem | Kazanma | Ort. getiri | Kâr faktörü | Ort. R |", "|---|---|---|---|---|---|---|---|"]
    for aile in AILELER:
        for donem, maske in [("2015-2022", kapali["giris"] < AYRILMIS), ("2023+ (ayrılmış)", kapali["giris"] >= AYRILMIS)]:
            for tur in ("aile", "rastgele"):
                d = kapali[maske & (kapali["aile"] == aile) & (kapali["tur"] == tur)]
                o = ozet(d)
                satir.append(
                    f"| {aile} | {donem} | {tur} | {o['islem']} | {o['kazanma_orani']:.1%} | "
                    f"{o['ortalama_getiri']:.2%} | {o['kar_faktoru']:.2f} | {d['r'].mean():.2f} |"
                )
    return "\n".join(satir)


def main() -> None:
    semboller = veri.evren()
    fiyatlar = {s: veri.fiyat(s) for s in semboller}
    fiyatlar = {s: f for s, f in fiyatlar.items() if len(f) >= 250}
    durum = nabiz(veri.fiyat(veri.ENDEKS))
    tum = sina(fiyatlar, durum)
    KLASOR.mkdir(exist_ok=True)
    yol = KLASOR / f"kanit-{dt.date.today():%Y%m%d}.md"
    gun_sayisi = durum.value_counts(normalize=True)
    yol.write_text(
        f"# Kanıt raporu {dt.date.today()}\n\n"
        f"Evren: bugünkü BIST100, {len(fiyatlar)} hisse (bugünkü listeyle geçmiş sınanır: hayatta kalan yanlılığı var).\n"
        f"Masraf her yönde %0,2. Rastgele: aynı günlerde izinli, aynı sayıda rastgele giriş, {RASTGELE_TEKRAR} tekrar.\n"
        f"Piyasa Nabzı gün payı: " + ", ".join(f"{k} {v:.0%}" for k, v in gun_sayisi.items()) + "\n\n"
        + tablo(tum) + "\n",
        encoding="utf-8",
    )
    tum.to_parquet(KLASOR / f"islemler-{dt.date.today():%Y%m%d}.parquet")
    print(yol)


if __name__ == "__main__":
    main()
