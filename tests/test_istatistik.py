"""İstatistik yüzü: Holm, p tabanı, blok bootstrap, saptanabilir en küçük etki (TASARIM 5.7, 5.9, 5.11)."""

import numpy as np
import pytest

from tansu import istatistik


def test_holm_elle_ornek():
    # sıralı p: 0,005 (×4) 0,01 (×3) 0,03 (×2) 0,04 (×1) → 0,02; 0,03; 0,06; 0,04→ en büyüğe çekilir 0,06
    assert istatistik.holm([0.01, 0.04, 0.03, 0.005]) == pytest.approx([0.03, 0.06, 0.06, 0.02])


def test_p_degeri_gercek_kadar_iyi_rastgele_sayilir():
    # k = 0,3'e eşit ya da üstü: 0,5 ve 0,3 → k=2; B=4 → 3/5
    assert istatistik.p_deger(0.3, [0.1, 0.5, 0.3, 0.0]) == pytest.approx(0.6)


def test_p_tabani_bir_bolu_bir_arti_b():
    assert istatistik.p_deger(9.0, [0.0] * 199) == pytest.approx(1 / 200)


def test_gercek_istatistik_yoksa_p_bir():
    assert istatistik.p_deger(float("nan"), [0.0] * 9) == 1.0


def test_saptanabilir_en_kucuk_etki_elle():
    # g = ±0,01 dört gün: sd(ddof=1) = 0,0115470; (1,645+0,842)·sd/√4·252 = 3,6184
    assert istatistik.saptanabilir_etki(np.array([0.01, -0.01, 0.01, -0.01])) == pytest.approx(3.6184, rel=1e-3)


def test_blok_bootstrap_sabit_seride_dar_aralik_ve_ayni_tohum_ayni_sonuc():
    g = np.full(100, 0.001)
    assert istatistik.blok_aralik(g, 20) == pytest.approx((0.252, 0.252))
    g = np.sin(np.arange(200)) * 0.01
    assert istatistik.blok_aralik(g, 20, tohum=3) == istatistik.blok_aralik(g, 20, tohum=3)
    alt, ust = istatistik.blok_aralik(g, 20)
    assert alt < g.mean() * 252 < ust


def test_blok_uzunlugu_en_az_yirmi():
    assert istatistik.blok_uzunlugu(5.0) == 20
    assert istatistik.blok_uzunlugu(37.4) == 38
