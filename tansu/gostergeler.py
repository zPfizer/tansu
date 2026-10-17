"""Göstergeler: vektörel, kütüphanesiz (TASARIM 3). İlk hal: EMA ve EMA sıkışması (KURALLAR §3, §4)."""

import numpy as np
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


def _gercek_aralik(
    yuksek: pd.Series, dusuk: pd.Series, kapanis: pd.Series, skipna: bool = True
) -> pd.Series:
    """Gerçek aralık (TASARIM 5.5). İlk günde önceki kapanış yoktur: `skipna` ise yüksek - düşük, değilse NaN."""
    onceki = kapanis.shift(1)
    return pd.concat(
        [yuksek - dusuk, (yuksek - onceki).abs(), (dusuk - onceki).abs()], axis=1
    ).max(axis=1, skipna=skipna)


def atr(
    yuksek: pd.Series, dusuk: pd.Series, kapanis: pd.Series, n: int = 14
) -> pd.Series:
    """Wilder ATR: ilk değer ilk n gerçek aralığın ortalaması, sonra (önceki*(n-1) + TR)/n (TASARIM 5.5)."""
    tr = _gercek_aralik(yuksek, dusuk, kapanis)
    tohum = tr.copy()
    tohum.iloc[: n - 1] = float("nan")
    if len(tr) >= n:
        tohum.iloc[n - 1] = tr.iloc[:n].mean()
    return tohum.ewm(alpha=1 / n, adjust=False).mean()


def _wilder_rsi(x: pd.Series, n: int) -> pd.Series:
    """RSI ve ADX için Wilder ortalaması: ilk değer, ilk n dolu değerin ortalaması (`atr` tohumundan ayrıdır: baştaki NaN satırlar sayılmaz)."""
    ilk = int(x.notna().to_numpy().argmax())
    tohum = x.copy()
    tohum.iloc[: ilk + n - 1] = float("nan")
    if len(x) >= ilk + n:
        tohum.iloc[ilk + n - 1] = x.iloc[ilk : ilk + n].mean()
    return tohum.ewm(alpha=1 / n, adjust=False).mean()


def rsi(kapanis: pd.Series, n: int = 14) -> pd.Series:
    """Wilder RSI: kazanç ve kayıp ortalamaları Wilder ortalamasıyla (KURALLAR §3 Modül 1, `rsi70`, `rsi50`)."""
    d = kapanis.diff()
    kazanc, kayip = _wilder_rsi(d.clip(lower=0), n), _wilder_rsi((-d).clip(lower=0), n)
    return 100 * kazanc / (kazanc + kayip)


def adx(
    yuksek: pd.Series, dusuk: pd.Series, kapanis: pd.Series, n: int = 14
) -> pd.Series:
    """Wilder ADX (Wilder 1978; KURALLAR §3 Modül 1, gösterge teyidi; gerçek aralık TASARIM 5.5): +DM, -DM ve gerçek aralık Wilder ortalamasıyla yumuşatılır;
    DX = 100 × |+DI − −DI| / (+DI + −DI), +DI + −DI = 0 ise 0 (yönlü hareket yok; ATR = 0 dahil); ADX, DX'in Wilder
    ortalamasıdır. İlk ADX 0 tabanlı 2n−1 konumunda (2n. gün) gelir, öncesi NaN."""
    yukari, asagi = yuksek.diff(), -dusuk.diff()
    arti = yukari.where((yukari > asagi) & (yukari > 0), 0.0).where(yukari.notna())
    eksi = asagi.where((asagi > yukari) & (asagi > 0), 0.0).where(yukari.notna())
    # ilk günde önceki kapanış yok: NaN (DM ile aynı tohum günü)
    tr = _gercek_aralik(yuksek, dusuk, kapanis, skipna=False)
    tr, arti, eksi = (_wilder_rsi(x, n) for x in (tr, arti, eksi))
    di_arti, di_eksi = 100 * arti / tr, 100 * eksi / tr
    dx = 100 * (di_arti - di_eksi).abs() / (di_arti + di_eksi)
    return _wilder_rsi(dx.where(arti + eksi != 0, 0.0), n)  # ATR = 0: DI = 0/0 = NaN


def momentum_squeeze(
    yuksek: pd.Series, dusuk: pd.Series, kapanis: pd.Series, n: int = 20
) -> pd.Series:
    """LazyBear Squeeze Momentum: n günlük doğrunun son nokta değeri (KURALLAR §3 Modül 1, momentum squeeze)."""
    orta = (
        (yuksek.rolling(n).max() + dusuk.rolling(n).min()) / 2 + sma(kapanis, n)
    ) / 2
    # en küçük kareler doğrusunun son noktadaki değeri, pencere değerlerinin ağırlıklı toplamıdır
    x = np.arange(n) - (n - 1) / 2
    agirlik = 1 / n + x * ((n - 1) / 2) / (x @ x)
    return (kapanis - orta).rolling(n).apply(lambda w: w @ agirlik, raw=True)


def macd_histogram(
    kapanis: pd.Series, hizli: int = 12, yavas: int = 26, sinyal: int = 9
) -> pd.Series:
    """MACD histogramı: MACD - sinyal çizgisi; EMA'lar `ema` ile (KURALLAR §3 Modül 1, gösterge teyidi)."""
    macd = ema(kapanis, hizli) - ema(kapanis, yavas)
    return macd - ema(macd, sinyal)


def psar(
    yuksek: pd.Series, dusuk: pd.Series, adim: float = 0.02, tavan: float = 0.2
) -> pd.Series:
    """Parabolic SAR, Wilder 1978 (KURALLAR §3 Modül 1, gösterge teyidi)."""
    h, d = yuksek.to_numpy(float), dusuk.to_numpy(float)
    sar = d.copy()
    # ponytail: ilk gün yükselen trend kabul edilir (SAR = ilk düşük); yanlışsa birkaç günde döner.
    yukari, ep, af = True, h[0], adim
    for i in range(1, len(h)):
        s = sar[i - 1] + af * (ep - sar[i - 1])
        # SAR, son iki günün düşüğünün (yükselenken) ya da yükseğinin (düşerken) ötesine geçmez
        son_iki = slice(max(i - 2, 0), i)
        if yukari:
            s = min(s, d[son_iki].min())
            if d[i] < s:
                yukari, s, ep, af = False, ep, d[i], adim
            elif h[i] > ep:
                ep, af = h[i], min(af + adim, tavan)
        else:
            s = max(s, h[son_iki].max())
            if h[i] > s:
                yukari, s, ep, af = True, ep, h[i], adim
            elif d[i] < ep:
                ep, af = d[i], min(af + adim, tavan)
        sar[i] = s
    return pd.Series(sar, index=yuksek.index)


def stokastik(
    yuksek: pd.Series, dusuk: pd.Series, kapanis: pd.Series, n: int = 14, d: int = 3
) -> tuple[pd.Series, pd.Series]:
    """Stokastik %K (n gün) ve %D (%K'nın d günlük SMA'sı) (KURALLAR §3 Modül 1, gösterge teyidi)."""
    alt = dusuk.rolling(n).min()
    k = 100 * (kapanis - alt) / (yuksek.rolling(n).max() - alt)
    return k, sma(k, d)


def sikisma_orani(kapanis: pd.Series, periyotlar=SIKISMA_PERIYOTLAR) -> pd.Series:
    """(en büyük EMA - en küçük EMA) / en yavaş EMA (KRDMD sadakatiyle çözüldü: EMA200)."""
    emalar = pd.concat([ema(kapanis, p) for p in periyotlar], axis=1)
    return (emalar.max(axis=1) - emalar.min(axis=1)) / emalar.iloc[:, -1]


def sikisma_donemleri(
    oran: pd.Series, esik=SIKISMA_ESIK, min_gun=SIKISMA_MIN_GUN
) -> list:
    """Oranın <= eşik olduğu art arda en az `min_gun` gün. Eşiği aşan ilk gün dönemi bitirir."""
    donemler, bas = [], None
    for i, ici in enumerate(
        [*(oran <= esik), False]
    ):  # sondaki False açık dönemi kapatır
        if ici and bas is None:
            bas = i
        elif not ici and bas is not None:
            if i - bas >= min_gun:
                kesit = oran.iloc[bas:i]
                donemler.append(
                    {
                        "bas": kesit.index[0],
                        "bit": kesit.index[-1],
                        "gun": len(kesit),
                        "ortalama": float(kesit.mean()),
                    }
                )
            bas = None
    return donemler
