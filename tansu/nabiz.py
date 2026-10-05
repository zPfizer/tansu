"""Piyasa Nabzı: endeksin günlük durumu. "Bugün endeks bana ne anlatıyor?"

- BEKLE: kapanış SMA200 altında ya da Piyasa Şoku (10 günlük oynaklık, son 120 günün
  medyanının 2 katını aşar). Yeni giriş yapılmaz.
- TAM_ALIM: kapanış SMA50 üstünde ve SMA50 son 20 günde yükselmiş.
- DIKKATLI: ikisi de değil.
"""
import numpy as np
import pandas as pd

TAM_ALIM, DIKKATLI, BEKLE = "TAM_ALIM", "DIKKATLI", "BEKLE"


def nabiz(endeks: pd.DataFrame) -> pd.Series:
    k = endeks["Close"]
    sma50, sma200 = k.rolling(50).mean(), k.rolling(200).mean()
    oynaklik = k.pct_change().rolling(10).std()
    sok = oynaklik > 2 * oynaklik.rolling(120).median()
    durum = np.where(
        (k < sma200) | sok, BEKLE,
        np.where((k > sma50) & (sma50 > sma50.shift(20)), TAM_ALIM, DIKKATLI),
    )
    return pd.Series(durum, index=endeks.index).where(sma200.notna(), BEKLE)
