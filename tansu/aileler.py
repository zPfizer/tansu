"""Aileler: EMA sıkışması kırılım sinyali (KURALLAR §3 madde 2; TASARIM 5.1 ısınma, 5.3 SMA250 şartı)."""

from dataclasses import dataclass

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


def sinyal(f: pd.DataFrame, p: Parametre = Parametre()) -> pd.DatetimeIndex:
    """`f`: tarih indeksli, `kapanis` ve `yuksek` (düzeltilmiş) sütunları. Sinyal günleri (kapanış günü)."""
    oran = gostergeler.sikisma_orani(f["kapanis"], p.periyotlar)
    sma = gostergeler.sma(f["kapanis"], p.sma_n)
    uygun = (f["kapanis"] >= sma).to_numpy()  # SMA250 NaN ise False
    gunler = []
    for d in gostergeler.sikisma_donemleri(oran, p.esik, p.min_gun):
        bit = f.index.get_loc(d["bit"])
        tavan = f["yuksek"].iloc[f.index.get_loc(d["bas"]): bit + 1].max()
        for i in range(bit + 1, min(bit + 1 + p.pencere, len(f))):
            if f["kapanis"].iloc[i] > tavan and uygun[i] and i + 1 >= p.isinma:
                gunler.append(f.index[i])
                break
    return pd.DatetimeIndex(gunler)
