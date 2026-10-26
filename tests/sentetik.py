"""Testlerin yapay fiyat serileri. Gerçek veri yok (SPEC 10)."""

import numpy as np
import pandas as pd


def gun_tablosu(kapanis, yuksek=None, dusuk=None, aof=None, bas="2022-01-03"):
    """`veri.gunluk` sözleşmesinde yapay tablo; `atr` sütunu 0,1."""
    kapanis = np.asarray(kapanis, float)
    yuksek = kapanis + 0.05 if yuksek is None else np.asarray(yuksek, float)
    dusuk = kapanis - 0.05 if dusuk is None else np.asarray(dusuk, float)
    aof = kapanis if aof is None else np.asarray(aof, float)
    n = len(kapanis)
    g = pd.DataFrame(
        {
            "aof": aof,
            "yuksek": yuksek,
            "dusuk": dusuk,
            "kapanis": kapanis,
            "hacim": 1e6,
            "ham_yuksek": yuksek,
            "ham_dusuk": dusuk,
            "ham_kapanis": kapanis,
            "kilit_tavan": False,
            "kilit_taban": False,
            "tavan_kapanis": False,
            "karantina": False,
            "uye": True,
            "xu100": 10000.0,
            "atr": 0.1,
        },
        index=pd.bdate_range(bas, periods=n, name="tarih"),
    )
    return g


def gartley_yolu(x=10.0, a=20.0, ab=0.618, bc=0.618, adim=20, bas=15.0):
    """Doğrusal bacaklar: başlangıç → X → A → B → C → D'nin biraz altı → A. Her bacak `adim` gün."""
    b = a - ab * (a - x)
    c = b + bc * (a - b)
    d = a - 0.786 * (a - x)
    duraklar = [bas, x, a, b, c, d - 0.1, a]
    yol = [duraklar[0]]
    for once, sonra in zip(duraklar, duraklar[1:], strict=False):
        yol += list(np.linspace(once, sonra, adim + 1)[1:])
    return np.array(yol)
