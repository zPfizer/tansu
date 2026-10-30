import numpy as np
import pytest

from tansu.stratejiler import gartley
from tests.sentetik import gartley_yolu, gun_tablosu

# Seviye testleri kapısız koşar; kapı ayrı testte.
P = {**gartley.STRATEJI.varsayilan, "rr_min": "kapali"}


def test_d_formulu_tansu_tarama_ornegi():
    # Golden olgu sayıları: X 10.20, A 21.20, 0.786 seviyesi 12.55 (SPEC 11 madde 1).
    assert gartley.oranlar(10.20, 21.20, 14.40, 17.00)[3] == pytest.approx(12.554)


def test_gartley_c_onayinda_limit_d_stop_x_ve_hedefler_verir():
    gun = gun_tablosu(gartley_yolu())
    s = gartley.STRATEJI.sinyal(gun, P)
    girisler = s[s["giris"]]
    assert len(girisler) == 1
    r = girisler.iloc[0]
    assert gun.index.get_loc(r.name) == 80 + 15  # C 80. gün, 15 gün sonra onay
    x, a = 10.0 - 0.05, 20.0 + 0.05
    d = a - 0.786 * (a - x)
    assert r["giris_tur"] == "limit" and r["seviye"] == pytest.approx(d)
    assert r["stop"] == pytest.approx(x)
    assert r["hedef1"] == pytest.approx(d + 0.382 * (a - d))
    assert r["hedef2"] == pytest.approx(d + 0.618 * (a - d))
    assert r["durum"] == "AKTIF"


def test_ab_orani_tutmazsa_sinyal_yok():
    gun = gun_tablosu(gartley_yolu(ab=0.5))
    assert not gartley.STRATEJI.sinyal(gun, P)["giris"].any()


def yol(duraklar):
    """(gün, fiyat) duraklarını doğrusal bacaklarla birleştirir."""
    fiyat = [duraklar[0][1]]
    for (g0, f0), (g1, f1) in zip(duraklar, duraklar[1:], strict=False):
        fiyat += list(np.linspace(f0, f1, g1 - g0 + 1)[1:])
    return np.array(fiyat)


def test_b_bacagin_en_dusugu_degilse_sinyal_yok():
    # A, X'ten 6 gün sonra; A'dan 3 gün sonraki dip (12,95) B'den (13,77) düşük ama X 15 gün içinde olduğu için pivot
    # değil. Gerçek bacak ucuyla AB/XA 0,703, tolerans dışı; B'yle ölçülen 0,622 deseni yanlış geçirir.
    x, a = 10.0, 20.0
    b = a - 0.618 * (a - x)
    c = b + 0.618 * (a - b)
    d = a - 0.786 * (a - x)
    duraklar = [(0, 15), (20, x), (26, a), (29, 13.0), (40, 16), (55, b), (75, c)]
    gun = gun_tablosu(yol([*duraklar, (95, d - 0.1), (115, a)]))
    assert not gartley.STRATEJI.sinyal(gun, P)["giris"].any()


def test_x_kirilmasi_altina_inmektir_esit_dip_bozmaz():
    # Kural kartı: X'in altına inen fiyat deseni bozar. Eşit dip ne X ile C arasında ne C'den sonra bozar.
    def sinyal_var(gun_no, fark):
        gun = gun_tablosu(gartley_yolu())
        gun.iloc[gun_no, gun.columns.get_loc("dusuk")] = gun["dusuk"].iat[20] + fark
        return gartley.STRATEJI.sinyal(gun, P)["giris"].any()

    # X 20. gün, C 80. gün, onay 95. gün.
    assert sinyal_var(21, 0.0) and sinyal_var(90, 0.0)
    assert not sinyal_var(90, -0.01)


def test_stop_secenegi_x_eksi_iki_atr():
    gun = gun_tablosu(gartley_yolu())
    s = gartley.STRATEJI.sinyal(gun, {**P, "stop": "X-2ATR"})
    r = s[s["giris"]].iloc[0]
    assert r["stop"] < 10.0 - 0.05


def test_rr_kapisi_hedef1_ile_olculur_varsayilan_1_4_gecirir_1_5_eler():
    # Stop X: hedef1 oranı 0.382 × 0.786 ÷ 0.214 ≈ 1.403; Tansu'nun kendi kurulumları 1.30-1.42 (Ek B #13).
    gun = gun_tablosu(gartley_yolu())
    assert gartley.STRATEJI.sinyal(gun, {})["giris"].any()
    assert not gartley.STRATEJI.sinyal(gun, {"rr_min": 1.5})["giris"].any()
