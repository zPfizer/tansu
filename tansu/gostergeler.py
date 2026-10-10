"""Göstergeler: vektörel, kütüphanesiz (TASARIM 3). İlk hal: EMA ve EMA sıkışması (KURALLAR §3, §4)."""

import pandas as pd

SIKISMA_PERIYOTLAR = (20, 50, 100, 200)
SIKISMA_ESIK = 0.012  # %1,2, dahil
SIKISMA_MIN_GUN = 3


def ema(seri: pd.Series, periyot: int) -> pd.Series:
    return seri.ewm(span=periyot, adjust=False).mean()


def sma(seri: pd.Series, periyot: int) -> pd.Series:
    return seri.rolling(periyot).mean()


def piyasa_durumu(xu100: pd.Series, n: int = 50) -> pd.Series:
    """Piyasa durumu: XU100 kapanış > SMA(n) (YORUM, TASARIM 6.3). SMA yoksa yanlış."""
    return xu100 > sma(xu100, n)


def atr(yuksek: pd.Series, dusuk: pd.Series, kapanis: pd.Series, n: int = 14) -> pd.Series:
    """Wilder ATR: ilk değer ilk n gerçek aralığın ortalaması, sonra (önceki*(n-1) + TR)/n (TASARIM 5.5)."""
    onceki = kapanis.shift(1)
    tr = pd.concat([yuksek - dusuk, (yuksek - onceki).abs(), (dusuk - onceki).abs()], axis=1).max(axis=1)
    tohum = tr.copy()
    tohum.iloc[: n - 1] = float("nan")
    if len(tr) >= n:
        tohum.iloc[n - 1] = tr.iloc[:n].mean()
    return tohum.ewm(alpha=1 / n, adjust=False).mean()


def sikisma_orani(kapanis: pd.Series, periyotlar=SIKISMA_PERIYOTLAR) -> pd.Series:
    """(en büyük EMA - en küçük EMA) / en yavaş EMA (KRDMD sadakatiyle çözüldü: EMA200)."""
    emalar = pd.concat([ema(kapanis, p) for p in periyotlar], axis=1)
    return (emalar.max(axis=1) - emalar.min(axis=1)) / emalar.iloc[:, -1]


def sikisma_donemleri(oran: pd.Series, esik=SIKISMA_ESIK, min_gun=SIKISMA_MIN_GUN) -> list:
    """Oranın <= eşik olduğu art arda en az `min_gun` gün. Eşiği aşan ilk gün dönemi bitirir."""
    donemler, bas = [], None
    for i, ici in enumerate([*(oran <= esik), False]):  # sondaki False açık dönemi kapatır
        if ici and bas is None:
            bas = i
        elif not ici and bas is not None:
            if i - bas >= min_gun:
                kesit = oran.iloc[bas:i]
                donemler.append({"bas": kesit.index[0], "bit": kesit.index[-1], "gun": len(kesit),
                                 "ortalama": float(kesit.mean())})
            bas = None
    return donemler
