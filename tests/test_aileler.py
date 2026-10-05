import numpy as np
import pandas as pd

from tansu.aileler import AILELER


def fiyat(kapanis, hacim=None, yuksek=None, acilis=None):
    kapanis = np.asarray(kapanis, dtype=float)
    gun = pd.bdate_range("2020-01-01", periods=len(kapanis))
    yuksek = kapanis if yuksek is None else np.asarray(yuksek, dtype=float)
    acilis = kapanis if acilis is None else np.asarray(acilis, dtype=float)
    hacim = np.full(len(kapanis), 1000.0) if hacim is None else np.asarray(hacim, dtype=float)
    return pd.DataFrame(
        {"Open": acilis, "High": yuksek, "Low": np.minimum(acilis, kapanis), "Close": kapanis, "Volume": hacim},
        index=gun,
    )


def test_trend_geri_cekilme_tepki_gununde_sinyal_verir():
    yukselis = list(np.linspace(100, 250, 300))
    dusus = [247.5, 245.0, 242.5, 240.0]
    kapanis = yukselis + dusus + [243.0]
    acilis = yukselis + dusus + [240.0]
    sinyal = AILELER["trend_geri_cekilme"].sinyal(fiyat(kapanis, acilis=acilis))
    assert sinyal.iloc[-1]
    assert not sinyal.iloc[:-1].any()


def test_sikisma_kirilimi_hacimli_kirilim_gununde_sinyal_verir():
    kapanis = [100.0] * 250 + [105.0]
    yuksek = [100.0] * 250 + [106.0]
    hacim = [1000.0] * 250 + [3000.0]
    sinyal = AILELER["sikisma_kirilimi"].sinyal(fiyat(kapanis, hacim, yuksek))
    assert sinyal.iloc[-1]
    assert not sinyal.iloc[:-1].any()


def test_sikisma_kirilimi_hacimsiz_kirilimda_sinyal_vermez():
    kapanis = [100.0] * 250 + [105.0]
    yuksek = [100.0] * 250 + [106.0]
    sinyal = AILELER["sikisma_kirilimi"].sinyal(fiyat(kapanis, yuksek=yuksek))
    assert not sinyal.any()


def test_sikisma_kirilimi_sikisma_olmadan_sinyal_vermez():
    kapanis = list(np.linspace(50, 150, 250)) + [160.0]
    hacim = [1000.0] * 250 + [3000.0]
    sinyal = AILELER["sikisma_kirilimi"].sinyal(fiyat(kapanis, hacim))
    assert not sinyal.any()
