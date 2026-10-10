"""Aileler: EMA sıkışması kırılım sinyali (KURALLAR §3 madde 2; TASARIM 5.1 ısınma, 5.3 SMA250 şartı)."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from tansu import gostergeler


@dataclass(frozen=True)
class Parametre:
    periyotlar: tuple = gostergeler.SIKISMA_PERIYOTLAR
    esik: float = gostergeler.SIKISMA_ESIK
    min_gun: int = gostergeler.SIKISMA_MIN_GUN
    pencere: int = 10  # YORUM: dönem bittikten sonra giriş penceresi (gün)
    isinma: int = 500  # TASARIM 5.1: hissenin ilk gününden bu kadar işlem günü dolmadan sinyal yok
    sma_n: int = 250


KIRILIM_GUN = 20  # YORUM (KURALLAR §3): sıkışmasız kırılım kolunda önceki gün sayısı


def pencere_gunleri(f: pd.DataFrame, p: Parametre = Parametre()) -> np.ndarray:
    """Sıkışma dönemi bitmiş, giriş penceresi açık günler (bool, `f` sırasında)."""
    oran = gostergeler.sikisma_orani(f["kapanis"], p.periyotlar)
    acik = np.zeros(len(f), dtype=bool)
    for d in gostergeler.sikisma_donemleri(oran, p.esik, p.min_gun):
        bit = f.index.get_loc(d["bit"])
        acik[bit + 1 : bit + 1 + p.pencere] = True
    return acik


def uygun_gunler(f, p) -> np.ndarray:
    """Kapanış ≥ SMA250 (NaN ise yanlış) ve ısınma tamam."""
    return (f["kapanis"] >= gostergeler.sma(f["kapanis"], p.sma_n)).to_numpy() & (
        np.arange(len(f)) + 1 >= p.isinma
    )


def on_sart(f: pd.DataFrame, p: Parametre = Parametre()) -> np.ndarray:
    """K1 ön şartlı günler (KURALLAR §3 madde 2): pencere açık, SMA250 üstü, ısınma tamam. Gerçek sinyal günleri bunun parçasıdır."""
    return pencere_gunleri(f, p) & uygun_gunler(f, p)


def sikismasiz_kirilim(
    f: pd.DataFrame, p: Parametre = Parametre(), gun: int = KIRILIM_GUN
) -> np.ndarray:
    """K1 ek kolu: kapanış önceki `gun` günün en yüksek yükseğinin üstünde, sıkışma penceresinde değil."""
    onceki = f["yuksek"].shift(1).rolling(gun).max()
    return (
        (f["kapanis"] > onceki).to_numpy() & uygun_gunler(f, p) & ~pencere_gunleri(f, p)
    )


def sinyal(f: pd.DataFrame, p: Parametre = Parametre()) -> pd.DatetimeIndex:
    """`f`: tarih indeksli, `kapanis` ve `yuksek` (düzeltilmiş) sütunları. Sinyal günleri (kapanış günü)."""
    oran = gostergeler.sikisma_orani(f["kapanis"], p.periyotlar)
    sma = gostergeler.sma(f["kapanis"], p.sma_n)
    uygun = (f["kapanis"] >= sma).to_numpy()  # SMA250 NaN ise False
    gunler = []
    for d in gostergeler.sikisma_donemleri(oran, p.esik, p.min_gun):
        bit = f.index.get_loc(d["bit"])
        tavan = f["yuksek"].iloc[f.index.get_loc(d["bas"]) : bit + 1].max()
        for i in range(bit + 1, min(bit + 1 + p.pencere, len(f))):
            if f["kapanis"].iloc[i] > tavan and uygun[i] and i + 1 >= p.isinma:
                gunler.append(f.index[i])
                break
    return pd.DatetimeIndex(gunler)
