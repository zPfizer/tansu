"""Kurulum aileleri. Her aile günlük fiyattan sinyal günlerini çıkarır.

Yeni aile eklemek: bir sinyal fonksiyonu yaz, AILELER'e kaydet. Çıkış kuralları (stop, hedef,
bozulma) bütün ailelerde ortaktır ve kanit.py'dedir.
"""
from dataclasses import dataclass
from typing import Callable

import pandas as pd


@dataclass(frozen=True)
class Aile:
    ad: str
    aciklama: str
    sinyal: Callable[[pd.DataFrame], pd.Series]  # Fiyat -> gün başına True/False


def ema(seri: pd.Series, gun: int) -> pd.Series:
    return seri.ewm(span=gun, adjust=False, min_periods=gun).mean()


def sikisma_kirilimi(f: pd.DataFrame) -> pd.Series:
    """EMA20/50/100/200 en az 3 gün %1,2 bandında sıkışır; fiyat 20 günlük tepeyi hacimle kırar."""
    ortalamalar = pd.concat([ema(f["Close"], g) for g in (20, 50, 100, 200)], axis=1)
    bant = (ortalamalar.max(axis=1) - ortalamalar.min(axis=1)) / f["Close"]
    sikisma = (bant <= 0.012).rolling(10).sum() >= 3
    kirilim = f["Close"] > f["High"].shift(1).rolling(20).max()
    hacimli = f["Volume"] > 1.5 * f["Volume"].shift(1).rolling(20).median()
    return (sikisma & kirilim & hacimli).fillna(False)


def trend_geri_cekilme(f: pd.DataFrame) -> pd.Series:
    """Yükselen trendde (EMA50 > EMA200) fiyat son 3 günde EMA20'ye değer, EMA50 üstünde kalır ve
    yeşil mumla önceki günün tepesini aşar."""
    e20, e50, e200 = ema(f["Close"], 20), ema(f["Close"], 50), ema(f["Close"], 200)
    trend = (e50 > e200) & (f["Close"] > e50)
    degdi = f["Low"].rolling(3).min() <= e20
    tepki = (f["Close"] > f["High"].shift(1)) & (f["Close"] > f["Open"])
    return (trend & degdi & tepki).fillna(False)


AILELER: dict[str, Aile] = {
    a.ad: a
    for a in [
        Aile("sikisma_kirilimi", "Sıkışmadan hacimli kırılım", sikisma_kirilimi),
        Aile("trend_geri_cekilme", "Trend içinde EMA20'ye geri çekilme ve tepki", trend_geri_cekilme),
    ]
}
