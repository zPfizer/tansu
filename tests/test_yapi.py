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
