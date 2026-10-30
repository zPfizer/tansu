"""`kanit/` altındaki Gartley betikleri motorun bu adlarını kullanır."""

from collections import Counter

import numpy as np
import pandas as pd
import pytest

from tansu import islem
from tests.sentetik import gun_tablosu
from tests.test_islem import CIKIS, maliyetli, sinyal


def tablo(gunler=(0,), karantinali=()):
    g = gun_tablosu(
        [11, 10.2, 12.2, 13.2, 13.2, 11, 11, 11],
        yuksek=[11.1, 10.5, 12.5, 13.5, 13.3, 11.05, 11.05, 11.05],
        dusuk=[10.9, 9.8, 10.3, 12.3, 13.1, 10.95, 10.95, 10.95],
    )
    g.iloc[list(karantinali), g.columns.get_loc("karantina")] = True
    return g, sinyal(g, gunler=gunler)


def test_simule_red_nedenini_ve_oynayi_modul_adiyla_sirayla_cagirir(monkeypatch):
    g, s = tablo(gunler=(0, 5), karantinali=(5,))
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
    assert sayac[islem.KALITE] == 1
    kayit = kayitlar[0]
    assert kayit["sinyal_tarihi"] == g.index[0]
    assert (kayit["stop"], kayit["dolum_fiyati"], kayit["seviye"]) == (9.0, 10.0, 10.0)


def test_red_nedeni_dogrudan_cagrida_str_ya_da_none_verir():
    g, s = tablo(gunler=(0, 5), karantinali=(5,))
    temiz = islem._red_nedeni(s.iloc[0], g.iloc[0], False, CIKIS)
    karantina = islem._red_nedeni(s.iloc[5], g.iloc[5], False, CIKIS)
    acik = islem._red_nedeni(s.iloc[0], g.iloc[0], True, CIKIS)
    assert temiz is None
    assert karantina == islem.KALITE and isinstance(karantina, str)
    assert acik == islem.ACIK_VAR and isinstance(acik, str)


@pytest.mark.parametrize(
    ("gecerlilik", "neden"),
    [(2, islem.SURE_DOLDU), (10, islem.VERI_SONU)],
    ids=["sure-doldu", "veri-sonu"],
)
def test_oyna_emir_dusunce_tam_bir_sayac_artar(gecerlilik, neden):
    g = gun_tablosu([11, 10.5, 10.6, 10.7, 10.7])
    s = sinyal(g, gecerlilik=gecerlilik)
    sayac = Counter()
    e, son = islem.oyna(islem.Gun(g, s), 0, s.iloc[0], CIKIS, 0.05, sayac)
    assert e is None and isinstance(son, int)
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


def test_acik_gun_kancasi_islem_alanlarini_ve_parcalari_gorur(monkeypatch):
    g, s = tablo()
    gercek = islem._acik_gun
    gorulen = []

    def kanca(e, i, gun, cikis):
        once = list(e.parcalar)
        kapandi = gercek(e, i, gun, cikis)
        gorulen.append((i, e.dolum_i, e.giris, e.risk_tabani, once, list(e.parcalar)))
        return kapandi

    monkeypatch.setattr(islem, "_acik_gun", kanca)
    taban = islem.RISK_TABANI * 0.1
    e, son = islem.oyna(islem.Gun(g, s), 0, s.iloc[0], CIKIS, taban, Counter())

    assert isinstance(e, islem._Islem) and isinstance(son, int)
    hedef1, hedef2 = (2, 12.0, 0.5, "hedef1"), (3, 13.0, 0.5, "hedef2")
    assert [(i, once, sonra) for i, *_, once, sonra in gorulen] == [
        (1, [], []),
        (2, [], [hedef1]),
        (3, [hedef1], [hedef1, hedef2]),
    ]
    assert all(
        (dolum_i, giris, risk_tabani) == (1, 10.0, taban)
        for _, dolum_i, giris, risk_tabani, *_ in gorulen
    )


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
