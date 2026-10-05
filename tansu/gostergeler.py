"""Göstergeler: vektörel, kütüphanesiz (TASARIM 3). İlk hal: EMA ve EMA sıkışması (KURALLAR §3, §4)."""

import pandas as pd

SIKISMA_PERIYOTLAR = (20, 50, 100, 200)
SIKISMA_ESIK = 0.012  # %1,2, dahil
SIKISMA_MIN_GUN = 3


def ema(seri: pd.Series, periyot: int) -> pd.Series:
    return seri.ewm(span=periyot, adjust=False).mean()


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
