"""Kanıt: bir ailenin sinyallerini geçmiş fiyatta işleme çevirir ve sonucu özetler.

Ortak çıkış kuralları (bütün aileler):
- Giriş: sinyalden sonraki günün açılışı.
- Stop: girişin 2 ATR altı. Hedef: 4 ATR üstü (2R). ATR sinyal günündeki 14 günlük değerdir.
- Bozulma: kapanış EMA50 altına inerse ertesi açılışta çıkış.
- Masraf: her yönde %0,2 (komisyon ve kayma birlikte).
"""
import numpy as np
import pandas as pd
import pandas_ta_classic as ta
import vectorbt as vbt

from tansu.aileler import ema

MASRAF = 0.002
STOP_ATR = 2.0
HEDEF_ATR = 4.0


def islemler(f: pd.DataFrame, sinyal: pd.Series) -> pd.DataFrame:
    """Bir hissenin fiyatı ve sinyalleri -> işlem tablosu (giris, cikis, getiri, r)."""
    atr = ta.atr(f["High"], f["Low"], f["Close"], length=14)
    stop_orani = (STOP_ATR * atr / f["Close"]).shift(1)
    hedef_orani = (HEDEF_ATR * atr / f["Close"]).shift(1)
    giris = sinyal.shift(1, fill_value=False).astype(bool)
    bozulma = (f["Close"] < ema(f["Close"], 50)).shift(1, fill_value=False).astype(bool)
    pf = vbt.Portfolio.from_signals(
        close=f["Close"], entries=giris, exits=bozulma, price=f["Open"],
        open=f["Open"], high=f["High"], low=f["Low"],
        sl_stop=stop_orani.fillna(np.inf).values, tp_stop=hedef_orani.fillna(np.inf).values,
        fees=MASRAF, init_cash=100_000, freq="1D",
    )
    k = pf.trades.records_readable
    tablo = pd.DataFrame({
        "giris": pd.to_datetime(k["Entry Timestamp"]).values,
        "cikis": pd.to_datetime(k["Exit Timestamp"]).values,
        "getiri": k["Return"].values,
        "acik": (k["Status"] == "Open").values,
    })
    tablo["r"] = tablo["getiri"] / stop_orani.reindex(tablo["giris"]).values
    return tablo


def ozet(tablo: pd.DataFrame) -> dict:
    g = tablo["getiri"]
    kazanc, kayip = g[g > 0].sum(), -g[g < 0].sum()
    return {
        "islem": int(len(g)),
        "kazanma_orani": float((g > 0).mean()) if len(g) else float("nan"),
        "ortalama_getiri": float(g.mean()) if len(g) else float("nan"),
        "kar_faktoru": float(kazanc / kayip) if kayip else float("inf"),
    }
