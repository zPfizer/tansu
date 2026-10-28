import numpy as np
import pandas as pd

from tansu import montecarlo as mc
from tansu import sinama


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


def test_dususler_iki_boyutta_satir_satir_sinama_dusus_ile_ayni():
    m = np.random.default_rng(3).normal(0.0, 1.0, (50, 30))
    m[0] = np.abs(m[0])
    iki = mc.dususler(m)
    assert iki.shape == (50,)
    for satir, d in zip(m, iki, strict=True):
        assert mc.dususler(satir) == d
        assert sinama.dusus(pd.Series(satir)) == d
    assert iki[0] == 0.0


def test_batma_payi_hep_dusen_seride_1_yukselen_seride_0():
    _, dusus = mc.bootstrap(np.full(30, -1.0), mc.akis(0))
    assert (dusus >= mc.BATMA_R).mean() == 1.0
    _, dusus = mc.bootstrap(np.ones(30), mc.akis(0))
    assert (dusus >= mc.BATMA_R).mean() == 0.0
