import dataclasses
from collections import Counter

import numpy as np
import pandas as pd
import pytest

from tansu import ayar, islem, sinama
from tansu import montecarlo as mc
from tansu.strateji import bos_sinyal
from tansu.stratejiler import ortalama_kesisim
from tests.sentetik import gun_tablosu, piyasa

KESISIM = dataclasses.replace(
    ortalama_kesisim.STRATEJI,
    varsayilan={"ortalama": "SMA", "cift": "9/21", "teyit_gun": 0},
    aralik={"teyit_gun": (0, 2)},
)
TEKRAR = 40


@pytest.fixture(scope="module")
def pazar():
    gunler = piyasa(sembol=3)
    return gunler, ayar.yuru(KESISIM, gunler, isci=1)


def test_sabit_seride_toplam_her_yuzdelikte_30_dusus_0():
    toplam, dusus = mc.bootstrap(np.ones(30), mc.akis(0))
    assert mc.yuzdelik(toplam) == (30.0, 30.0, 30.0)
    assert mc.yuzdelik(dusus) == (0.0, 0.0, 0.0)
    assert len(toplam) == len(dusus) == mc.TEKRAR


def test_ayni_tohum_ayni_dizi_farkli_akis_farkli_dizi():
    x = np.random.default_rng(1).normal(0.2, 1.0, 40)
    a, b, c = (mc.bootstrap(x, mc.akis(k)) for k in (0, 0, 1))
    np.testing.assert_array_equal(a[0], b[0])
    np.testing.assert_array_equal(a[1], b[1])
    assert not np.array_equal(a[0], c[0])
    np.testing.assert_array_equal(
        mc.karistir(x, mc.akis(2)), mc.karistir(x, mc.akis(2))
    )


def test_karistirma_degerleri_korur_dususu_degistirir():
    tek_kayip = np.r_[np.ones(29), -5.0]
    assert (mc.karistir(tek_kayip, mc.akis(0)) == 5.0).all()
    karisik = np.tile([1.0, -1.0, 2.0, -1.5], 8)
    assert np.ptp(mc.karistir(karisik, mc.akis(0))) > 0


def test_dusus_iki_boyutta_satir_satir_seriyle_ayni():
    m = np.random.default_rng(3).normal(0.0, 1.0, (50, 30))
    m[0] = np.abs(m[0])
    iki = sinama.dusus(m)
    assert iki.shape == (50,)
    for satir, d in zip(m, iki, strict=True):
        assert sinama.dusus(pd.Series(satir)) == d
        assert isinstance(sinama.dusus(satir), float)
    assert iki[0] == 0.0
    assert sinama.dusus([]) == 0.0
    assert sinama.dusus([2.0, -1.0, -3.0, 1.0]) == 4.0


def test_batma_payi_hep_dusen_seride_1_yukselen_seride_0():
    _, dusus = mc.bootstrap(np.full(30, -1.0), mc.akis(0))
    assert (dusus >= mc.BATMA_R).mean() == 1.0
    _, dusus = mc.bootstrap(np.ones(30), mc.akis(0))
    assert (dusus >= mc.BATMA_R).mean() == 0.0


def test_piyasada_uc_tablo_yuzdelik_0_100_ayni_tohum_ayni_sonuc(pazar):
    gunler, y = pazar
    a = mc.hesapla(KESISIM, gunler, y, tekrar=TEKRAR)
    assert a.n == len(y.dis_ornek.islemler) >= sinama.EN_AZ
    assert a.tohum == mc.TOHUM and a.olcu == "net_yuzde" and a.batma is None
    for tablo in (a.bootstrap_toplam, a.bootstrap_dusus, a.karistirma_dusus):
        assert tablo[0] <= tablo[1] <= tablo[2]
    assert 0 <= a.rastgele.yuzdelik <= 100
    assert a.rastgele.strateji_ort == pytest.approx(
        y.dis_ornek.islemler["net_yuzde"].mean()
    )
    assert np.ptp(a.rastgele.ortalamalar) > 0
    assert mc.hesapla(KESISIM, gunler, y, tekrar=TEKRAR) == a


def test_30_kurulumdan_azsa_tablolar_yok_n_yazilir():
    gunler = piyasa(sembol=1, son="2023-03-31")
    y = ayar.yuru(KESISIM, gunler, isci=1)
    a = mc.hesapla(KESISIM, gunler, y, tekrar=TEKRAR)
    assert 0 < a.n == len(y.dis_ornek.islemler) < sinama.EN_AZ
    assert a.bootstrap_toplam is a.bootstrap_dusus is a.karistirma_dusus is None
    assert a.batma is a.rastgele is None


def test_2026_fiyati_monte_carloyu_degistirmez(pazar):
    gunler, y = pazar
    rng = np.random.default_rng(5)
    bozuk = {}
    for s, g in gunler.items():
        g = g.copy()
        sonra = g.index >= sinama.SAKLI_BAS
        for c in ("aof", "yuksek", "dusuk", "kapanis", "atr"):
            g.loc[sonra, c] = rng.uniform(1, 1000, sonra.sum())
        g.loc[sonra, "kilit_tavan"] = rng.random(sonra.sum()) < 0.5
        bozuk[s] = g
    a = mc.hesapla(KESISIM, gunler, y, tekrar=TEKRAR)
    b = mc.hesapla(KESISIM, bozuk, ayar.yuru(KESISIM, bozuk, isci=1), tekrar=TEKRAR)
    assert a == b


def test_rastgele_giris_seviyeleri_sablonun_atr_uzakligi():
    """Tek uygun gün t ve tek şablon: her koşu aynı kurulumu açar.
    Şablon: dolum 50, stop 48, hedef1 54, sinyal günü ATR 2; yani stop 1 ATR altta, hedef1 2 ATR üstte.
    Rastgele: dolum AOF(t+1) = 101, stop 101 - 2 = 99, hedef1 101 + 4 = 105; t+2 günü yüksek 106 hedefi alır."""
    kapanis = np.full(10, 100.0)
    yuksek, dusuk, aof = kapanis + 0.5, kapanis - 0.5, kapanis.copy()
    aof[6], yuksek[6], dusuk[6] = 101.0, 101.5, 100.5
    yuksek[7], dusuk[7] = 106.0, 100.0
    g = gun_tablosu(kapanis, yuksek, dusuk, aof, bas="2022-12-26").assign(atr=2.0)
    t = pd.Timestamp("2023-01-02")
    g["uye"] = g.index == t
    oyuncak = dataclasses.replace(
        KESISIM,
        sinif="a",
        varsayilan={},
        aralik={},
        cikis=islem.Cikis("dokunus", (("hedef1", 1.0),)),
        hesapla=lambda gun, p: bos_sinyal(gun.index),
    )
    gercek = pd.DataFrame(
        {
            "sembol": "S00",
            "sinyal_tarihi": t,
            "dolum_tarihi": t,
            "cikis_tarihi": t,
            "dolum_fiyati": 50.0,
            "stop": 48.0,
            "hedef1": 54.0,
            **{h: np.nan for h in islem.HEDEFLER[1:]},
            "R": np.full(sinama.EN_AZ, 1.0),
        }
    )
    kosu = sinama.Kosu(gercek, pd.DataFrame(columns=["sembol", "tarih"]), Counter())
    secim = ayar.Secim(
        0, {}, np.full(1, np.nan), np.full(1, np.nan), np.zeros(1), False
    )
    adim = ayar.Adim(ayar.PENCERELER[0], secim, 0, 0.0, kosu, 0.0, None)
    y = ayar.Yuruyus(ayar.Izgara(oyuncak), (adim,), kosu, None, 0, secim)
    a = mc.hesapla(oyuncak, {"S00": g}, y, tekrar=TEKRAR)
    beklenen = (105 - 101 - islem.maliyet(101, 105)) / 2  # risk = 101 - 99
    assert a.rastgele.ortalamalar == pytest.approx((beklenen,) * 3)
    assert a.rastgele.strateji_ort == 1.0 and a.rastgele.yuzdelik == 0.0
    assert a.batma == 0.0
