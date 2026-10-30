"""`kanit/` altındaki Gartley betikleri motorun bu adlarını kullanır."""

from collections import Counter

import numpy as np
import pandas as pd
import pytest

from tansu import islem
from tests.sentetik import gun_tablosu
from tests.test_islem import CIKIS, maliyetli, sinyal


def tablo(gunler=(0,), uye_degil=()):
    g = gun_tablosu(
        [11, 10.2, 12.2, 13.2, 13.2, 11, 11, 11],
        yuksek=[11.1, 10.5, 12.5, 13.5, 13.3, 11.05, 11.05, 11.05],
        dusuk=[10.9, 9.8, 10.3, 12.3, 13.1, 10.95, 10.95, 10.95],
    )
    g.iloc[list(uye_degil), g.columns.get_loc("uye")] = False
    return g, sinyal(g, gunler=gunler)


def test_simule_red_nedenini_ve_oynayi_modul_adiyla_sirayla_cagirir(monkeypatch):
    g, s = tablo(gunler=(0, 5), uye_degil=(5,))
    cagrilar = []
    gercek_red, gercek_oyna = islem._red_nedeni, islem.oyna

    def red_kaydi(*arg):
        cagrilar.append(("red", arg))
        return gercek_red(*arg)

    def oyna_kaydi(*arg):
        cagrilar.append(("oyna", arg))
        return gercek_oyna(*arg)

    monkeypatch.setattr(islem, "_red_nedeni", red_kaydi)
    monkeypatch.setattr(islem, "oyna", oyna_kaydi)
    kayitlar, sayac = islem.simule(g, s, CIKIS, sembol="AAA", strateji="t", sinif="a")

    assert [
        (ad, arg[0].name if ad == "red" else arg[2].name) for ad, arg in cagrilar
    ] == [
        ("red", g.index[0]),
        ("oyna", g.index[0]),
        ("red", g.index[5]),
    ]
    for ad, arg in cagrilar:
        if ad == "red":
            satir, gun_satiri, acik_var, cikis = arg
            assert isinstance(satir, pd.Series) and satir["giris"]
            assert isinstance(gun_satiri, pd.Series) and gun_satiri.name == satir.name
            assert isinstance(acik_var, bool | np.bool_) and not acik_var
            assert cikis is CIKIS
    motor, i, satir, cikis, taban, oyna_sayac = cagrilar[1][1]
    assert isinstance(motor, islem.Gun) and i == 0 and cikis is CIKIS
    assert isinstance(satir, pd.Series) and satir["giris"]
    assert taban == pytest.approx(islem.RISK_TABANI * 0.1)
    assert oyna_sayac is sayac and len(kayitlar) == 1
    assert sayac[islem.UYE_DEGIL] == 1


@pytest.mark.parametrize(
    ("gecerlilik", "neden"),
    [(2, islem.SURE_DOLDU), (10, islem.VERI_SONU)],
    ids=["sure-doldu", "veri-sonu"],
)
def test_oyna_emir_dusunce_tam_bir_sayac_artar(gecerlilik, neden):
    g = gun_tablosu([11, 10.5, 10.6, 10.7, 10.7])
    s = sinyal(g, gecerlilik=gecerlilik)
    sayac = Counter()
    e, _ = islem.oyna(islem.Gun(g, s), 0, s.iloc[0], CIKIS, 0.05, sayac)
    assert e is None
    assert sum(sayac.values()) == 1 and sayac[neden] == 1


def test_acik_gun_kancasi_satiri_yazilabilir_alanlari_ve_kapatmayi_gorur(monkeypatch):
    g, s = tablo()
    s["stop_atr"] = 1.5
    cagrilar, islemler = [], []

    def kanca(e, i, gun, cikis):
        cagrilar.append((i, gun, cikis))
        islemler.append(e)
        assert set(s.columns) <= set(e.satir.index)
        assert e.satir["stop_atr"] == 1.5 and e.satir["hedef1"] == 12.0
        if len(cagrilar) == 1:
            e.stop, e.risk, e.bekleyen = 9.5, 2.0, "kanca"
            return False
        assert e.stop == 9.5 and e.risk == 2.0 and e.bekleyen == "kanca"
        return islem._kapat(e, i, 10.5, e.bekleyen)

    monkeypatch.setattr(islem, "_acik_gun", kanca)
    (k,), _ = islem.simule(g, s, CIKIS, sembol="AAA", strateji="t", sinif="a")

    assert [i for i, _, _ in cagrilar] == [1, 2]
    assert all(isinstance(gun, islem.Gun) and c is CIKIS for _, gun, c in cagrilar)
    assert all(e is islemler[0] and isinstance(e, islem._Islem) for e in islemler)
    assert k["stop"] == 9.5 and k["cikis_nedeni"] == "kanca"
    assert k["cikis_fiyati"] == 10.5
    assert k["R"] == pytest.approx(maliyetli(10.0, 10.5) / 2.0)
    assert islem.sonuc(islemler[0]).R == pytest.approx(k["R"])


def test_gun_motor_dizilerini_gun_basina_bir_ogeyle_verir():
    g = gun_tablosu([11, 10.2, 12.2, 13.2], aof=[11.5, 10.1, 12.1, 13.1])
    g["atr"] = [0.1, 0.2, 0.3, 0.4]
    g.iloc[2, g.columns.get_loc("kilit_taban")] = True
    motor = islem.Gun(g, sinyal(g))
    for ad, sutun in (("aof", "aof"), ("kap", "kapanis"), ("atr", "atr")):
        dizi = getattr(motor, ad)
        assert isinstance(dizi, np.ndarray) and dizi.shape == (len(g),)
        np.testing.assert_array_equal(dizi, g[sutun].to_numpy(float))
    assert isinstance(motor.taban_kilit, np.ndarray)
    assert motor.taban_kilit.tolist() == [False, False, True, False]


def test_betiklerin_okudugu_sabitler_ve_cikis_kurucusu_var():
    hedef = (("hedef1", 1.0),)
    cikis = islem.Cikis("dokunus", hedef)
    assert (cikis.stop_mod, cikis.hedef) == ("dokunus", hedef)
    assert islem.RISK_TABANI > 0 and islem.MALIYET > 0
    assert isinstance(islem.VERI_SONU, str)
