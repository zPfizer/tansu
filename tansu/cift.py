"""Çift çekirdeği: Z ve ΔZ (TASARIM 3). Vektörel. Y = ilk bacak (VAKBN), X = referans bacak (GARAN)."""

import numpy as np
import pandas as pd

MODLAR = ("log_oran", "kalinti")


def hesapla(y, x, pencere=60, ddof=1, mod="log_oran", esik=2.0):
    """Tarih hizalı Z, ΔZ ve hedef bacak (TASARIM 5.6, 5.15)."""
    z = z_skor(y, x, pencere, ddof, mod)
    fark = dz(z)
    return pd.DataFrame(
        {
            "z": z,
            "dz": fark,
            "hedef": np.where(
                (z <= -esik) & (fark > 0), 1, np.where((z >= esik) & (fark < 0), -1, 0)
            ),
        },
        index=z.index,
    )


def z_skor(
    y: pd.Series, x: pd.Series, pencere: int, ddof: int = 1, mod: str = "log_oran"
) -> pd.Series:
    """Kayan pencerede Z. `log_oran`: s = log(Y/X). `kalinti`: s = pencere içi OLS kalıntısı log Y - a - b log X.
    Kalıntı penceresinin ortalaması 0'dır; Z_t = kalıntı_t / std(kalıntı)."""
    ly, lx = np.log(y), np.log(x)
    if mod == "log_oran":
        s = ly - lx
        return (s - s.rolling(pencere).mean()) / s.rolling(pencere).std(ddof=ddof)
    if mod != "kalinti":
        raise ValueError(f"bilinmeyen mod: {mod}")
    r = lambda s: s.rolling(pencere)
    b = beta(y, x, pencere)
    kalinti = (ly - r(ly).mean()) - b * (lx - r(lx).mean())
    # kalıntı varyansı = vyy - b * cxy (aynı ddof ile)
    sapma = np.sqrt(r(ly).var(ddof=ddof) - b * r(ly).cov(lx, ddof=ddof))
    return kalinti / sapma


def dz(z: pd.Series) -> pd.Series:
    return z.diff()


def beta(y: pd.Series, x: pd.Series, pencere: int) -> pd.Series:
    """log Y'nin log X'e kayan OLS eğimi."""
    ly, lx = np.log(y), np.log(x)
    return ly.rolling(pencere).cov(lx) / lx.rolling(pencere).var()


def korelasyon(y: pd.Series, x: pd.Series, pencere: int) -> pd.Series:
    return np.log(y).rolling(pencere).corr(np.log(x))
