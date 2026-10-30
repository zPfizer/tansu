import numpy as np
import pandas as pd

from tansu import yapi


def seri(degerler):
    s = pd.Series(degerler, dtype=float)
    return s, s


def test_sag_bar_pivotu_pencere_sonunda_onaylanir():
    y, d = seri([1, 2, 5, 2, 1, 0, 1, 2, 3])
    p = yapi.sag_bar_pivotlari(y, d, 2)
    assert [(q.tur, q.pivot_gun, q.onay_gun, q.fiyat) for q in p] == [
        ("T", 2, 4, 5.0),
        ("D", 5, 7, 0.0),
    ]


def test_sag_bar_esitlikte_ilk_gunu_alir():
    y, d = seri([1, 3, 3, 1, 1, 1])
    assert [q.pivot_gun for q in yapi.sag_bar_pivotlari(y, d, 1) if q.tur == "T"] == [1]


def test_sag_bar_fiyatsiz_gunu_bar_saymaz():
    # Fiyatsız gün (NaN: eksik ya da bozuk) bar değildir. 5'in sağındaki iki bar 6 ve 4'tür: 5 tepe olmaz.
    y, d = seri([1, 2, 5, np.nan, np.nan, 6, 4, 3])
    p = yapi.sag_bar_pivotlari(y, d, 2)
    assert [(q.pivot_gun, q.onay_gun) for q in p if q.tur == "T"] == [(5, 7)]
    # Onay günü pivottan sonraki k. fiyatlı gündür, takvim günü değil.
    y, d = seri([1, 2, 5, np.nan, 2, 1])
    assert [
        (q.tur, q.pivot_gun, q.onay_gun) for q in yapi.sag_bar_pivotlari(y, d, 2)
    ] == [("T", 2, 5)]


def test_sag_bar_fiyatsiz_gunlu_seride_gelecege_bakmaz():
    # Onay günü t olan her pivot, yalnız t'ye kadarki veriyle de aynı bulunur (baş ve sondaki boşluk dahil).
    r = np.random.default_rng(7)
    y = np.round(r.normal(0, 1, 120).cumsum(), 1)
    y[r.random(120) < 0.15] = np.nan
    s = pd.Series(y)
    tam = yapi.sag_bar_pivotlari(s, s, 3)
    for t in range(len(s)):
        once = [p for p in tam if p.onay_gun <= t]
        assert [p for p in yapi.sag_bar_pivotlari(s[: t + 1], s[: t + 1], 3)] == once


def test_bacak_uclari_pencereleri():
    # X dip 0. gün 10, A tepe 3. gün 20, B dip 6. gün 14, C tepe 9. gün 17, t = 11.
    sira = (
        yapi.Pivot("D", 0, 2, 10.0),
        yapi.Pivot("T", 3, 5, 20.0),
        yapi.Pivot("D", 6, 8, 14.0),
        yapi.Pivot("T", 9, 11, 17.0),
    )

    def uc_mu(gun, yuk=None, dus=None):
        y, d = np.full(12, 15.0), np.full(12, 15.0)
        if yuk is not None:
            y[gun] = yuk
        if dus is not None:
            d[gun] = dus
        return yapi.bacak_uclari(y, d, sira, 11)

    # Her şey 15: pivotların arasında daha uç değer yok. Sonra her pencerede aşma bozar, eşitlik bozmaz.
    assert uc_mu(0)
    assert not uc_mu(2, yuk=21) and uc_mu(2, yuk=20)  # A, (X, B)
    assert not uc_mu(4, dus=13.9) and uc_mu(4, dus=14)  # B, (A, C)
    assert not uc_mu(11, yuk=17.1) and uc_mu(11, yuk=17)  # C, (B, t], t dahil
    assert not uc_mu(10, dus=9.9) and uc_mu(10, dus=10)  # X, (X, t]
    # Komşu pivot günlerinin barları pencereye girmez (gün içi sıra bilinmez).
    assert uc_mu(3, dus=13) and uc_mu(6, yuk=18)


def test_zigzag_yuzde_donuste_onaylar():
    y, d = seri([10, 11, 12, 11.7, 11.5, 12.5, 13, 12.6])
    p = yapi.zigzag_pivotlari(y, d, 3)
    assert [(q.tur, q.pivot_gun, q.onay_gun) for q in p] == [
        ("D", 0, 1),
        ("T", 2, 4),
        ("D", 4, 5),
        ("T", 6, 7),
    ]


def test_ardisik_ayni_turde_daha_uc_pivotu_tutar():
    p = [
        yapi.Pivot("D", 0, 2, 1.0),
        yapi.Pivot("T", 3, 5, 5.0),
        yapi.Pivot("T", 6, 8, 4.0),
        yapi.Pivot("T", 9, 11, 6.0),
    ]
    siralar = list(yapi.ardisik(p))
    assert len(siralar) == 3
    assert siralar[-1] == (p[0], p[3])
