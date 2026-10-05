import numpy as np
import pandas as pd

from tansu.nabiz import BEKLE, DIKKATLI, TAM_ALIM, nabiz
from tansu.veri import temizle


def endeks(kapanis):
    kapanis = np.asarray(kapanis, dtype=float)
    gun = pd.bdate_range("2020-01-01", periods=len(kapanis))
    return pd.DataFrame({"Open": kapanis, "High": kapanis, "Low": kapanis, "Close": kapanis}, index=gun)


def test_sakin_yukselen_endeks_tam_alim():
    kapanis = 100 * np.cumprod(np.full(300, 1.002) * (1 + 0.001 * np.tile([1, -1], 150)))
    assert nabiz(endeks(kapanis)).iloc[-1] == TAM_ALIM


def test_uzun_ortalamanin_altindaki_endeks_bekle():
    kapanis = list(np.linspace(100, 200, 250)) + list(np.linspace(200, 120, 60))
    assert nabiz(endeks(kapanis)).iloc[-1] == BEKLE


def test_ani_oynaklik_sicramasi_trend_yukarida_olsa_da_bekle():
    sakin = 100 * np.cumprod(np.full(300, 1.002) * (1 + 0.001 * np.tile([1, -1], 150)))
    sok = sakin[-1] * np.cumprod(1 + 0.06 * np.tile([1, -1], 5))
    assert nabiz(endeks(list(sakin) + list(sok))).iloc[-1] == BEKLE


def test_kisa_trend_zayif_uzun_trend_saglam_dikkatli():
    kapanis = list(np.linspace(100, 200, 260)) + list(np.linspace(200, 188, 25))
    assert nabiz(endeks(kapanis)).iloc[-1] == DIKKATLI


def test_temizle_bos_kapanisi_ve_hacimsiz_gunu_atar():
    gun = pd.bdate_range("2020-01-01", periods=4)
    f = pd.DataFrame(
        {"Open": [1, 1, 1, 1.0], "High": [1, 1, 1, 1.0], "Low": [1, 1, 1, 1.0],
         "Close": [1, np.nan, 1, 1.0], "Volume": [10, 10, 0, 10.0]},
        index=gun,
    )
    assert list(temizle(f).index) == [gun[0], gun[3]]


def test_temizle_bedelsiz_boslugunu_geriye_dogru_duzeltir():
    # BIST günlük limiti %10. 3. gün açılış yarıya iner: bedelsiz bölünme. Önceki günler 0,5 ile çarpılır.
    gun = pd.bdate_range("2020-01-01", periods=4)
    f = pd.DataFrame(
        {"Open": [100, 102, 52, 53.0], "High": [101, 105, 53, 54.0], "Low": [99, 101, 51, 52.0],
         "Close": [100, 104, 52, 53.0], "Volume": [10, 10, 20, 10.0]},
        index=gun,
    )
    t = temizle(f)
    assert t["Close"].tolist() == [50, 52, 52, 53]
    assert t["Volume"].tolist() == [20, 20, 20, 10]
