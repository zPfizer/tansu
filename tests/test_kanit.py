import numpy as np
import pandas as pd
import pytest

from tansu.kanit import MASRAF, islemler, ozet


def test_hedefe_giden_islem_masraf_dusulmus_getiriyi_verir():
    # 60 gün düz 100, gün içi aralık 2,5 (ATR 2,5). Sinyal 59. gün; giriş 60. gün açılışı 100.
    # Stop 100 - 2*2,5 = 95, hedef 100 + 4*2,5 = 110. 62. gün yüksek 111: hedefte çıkış.
    n = 70
    kapanis = np.full(n, 100.0)
    yuksek = np.full(n, 101.25)
    dusuk = np.full(n, 98.75)
    yuksek[62] = 111.0
    gun = pd.bdate_range("2021-01-01", periods=n)
    f = pd.DataFrame({"Open": kapanis, "High": yuksek, "Low": dusuk, "Close": kapanis, "Volume": 1000.0}, index=gun)
    sinyal = pd.Series(False, index=gun)
    sinyal.iloc[59] = True

    sonuc = islemler(f, sinyal)

    assert len(sonuc) == 1
    # 100'e al, 110'a sat: kâr 10; masraf alışta 0,20, satışta 0,22. Net 9,58 / 100 = %9,58.
    assert MASRAF == 0.002
    assert sonuc["getiri"].iloc[0] == pytest.approx(0.0958, rel=1e-6)
    assert sonuc["r"].iloc[0] == pytest.approx(0.0958 / 0.05, rel=1e-6)
    assert sonuc["giris"].iloc[0] == gun[60]


def test_stopa_giden_islem_iki_atr_altinda_kapanir():
    n = 70
    kapanis = np.full(n, 100.0)
    yuksek = np.full(n, 101.25)
    dusuk = np.full(n, 98.75)
    dusuk[62] = 94.0
    gun = pd.bdate_range("2021-01-01", periods=n)
    f = pd.DataFrame({"Open": kapanis, "High": yuksek, "Low": dusuk, "Close": kapanis, "Volume": 1000.0}, index=gun)
    sinyal = pd.Series(False, index=gun)
    sinyal.iloc[59] = True

    sonuc = islemler(f, sinyal)

    # 100'e al, 95'e sat: zarar 5; masraf 0,20 + 0,19. Net -5,39 / 100.
    assert sonuc["getiri"].iloc[0] == pytest.approx(-0.0539, rel=1e-6)
    assert sonuc["cikis"].iloc[0] == gun[62]


def test_ozet_kazanma_orani_ve_kar_faktoru():
    tablo = pd.DataFrame({"getiri": [0.10, -0.05, 0.02]})
    o = ozet(tablo)
    assert o["islem"] == 3
    assert o["kazanma_orani"] == pytest.approx(2 / 3)
    assert o["ortalama_getiri"] == pytest.approx(0.07 / 3)
    assert o["kar_faktoru"] == pytest.approx(2.4)
