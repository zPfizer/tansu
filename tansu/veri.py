"""Veri: evren (bugünkü BIST100) ve günlük fiyatlar.

Fiyat kaynağı Yahoo (yfinance, temettü ve bölünme düzeltmeli). Evren kaynağı borsapy. İkisi de
resmî değildir; kişisel kullanım içindir. Fiyatlar veri/ klasöründe parquet olarak saklanır;
aynı gün ikinci kez indirilmez.
"""
import datetime as dt
from pathlib import Path

import pandas as pd
import yfinance as yf

KLASOR = Path(__file__).resolve().parent.parent / "veri"
ENDEKS = "XU100"
BASLANGIC = "2015-01-01"


def evren() -> list[str]:
    import borsapy as bp

    return sorted(c["symbol"] for c in bp.Index(ENDEKS).components)


BOSLUK = 0.25  # BIST günlük limiti %10; bundan büyük açılış boşluğu bedelsiz ya da bölünmedir


def temizle(f: pd.DataFrame) -> pd.DataFrame:
    """Kapanışı boş ya da hacmi sıfır olan günleri atar. Yahoo'nun düzeltmediği bedelsiz
    boşluklarını, önceki fiyatları boşluk oranıyla çarparak düzeltir (hacim ters oranla)."""
    f = f.dropna(subset=["Close"])
    if "Volume" in f:
        f = f[f["Volume"] > 0]
    f = f.astype(float)
    oran =f["Open"] / f["Close"].shift(1)
    for gun in oran.index[(oran - 1).abs() > BOSLUK]:
        once = f.index < gun
        f.loc[once, ["Open", "High", "Low", "Close"]] *= oran[gun]
        f.loc[once, "Volume"] /= oran[gun]
    return f


def fiyat(sembol: str) -> pd.DataFrame:
    """Bir hissenin (ya da XU100'ün) günlük fiyatı. Yahoo kodu: <sembol>.IS"""
    KLASOR.mkdir(exist_ok=True)
    yol = KLASOR / f"{sembol}.parquet"
    if yol.exists() and dt.date.fromtimestamp(yol.stat().st_mtime) == dt.date.today():
        return pd.read_parquet(yol)
    f = yf.download(f"{sembol}.IS", start=BASLANGIC, auto_adjust=True, progress=False, threads=False)
    f.columns = f.columns.get_level_values(0)
    f = f[["Open", "High", "Low", "Close", "Volume"]]
    if sembol != ENDEKS:
        f = temizle(f)
    else:
        f = f.dropna(subset=["Close"])
    f.to_parquet(yol)
    return f
