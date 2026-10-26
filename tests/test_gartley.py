import pytest

from tansu.stratejiler import gartley
from tests.sentetik import gartley_yolu, gun_tablosu

P = dict(gartley.STRATEJI.varsayilan)


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


def test_stop_secenegi_x_eksi_iki_atr():
    gun = gun_tablosu(gartley_yolu())
    s = gartley.STRATEJI.sinyal(gun, {**P, "stop": "X-2ATR"})
    r = s[s["giris"]].iloc[0]
    assert r["stop"] < 10.0 - 0.05


def test_rr_kapisi_hedef2_ile_olculur():
    gun = gun_tablosu(gartley_yolu())
    assert gartley.STRATEJI.sinyal(gun, {**P, "rr_min": 2.0})["giris"].any()
    assert not gartley.STRATEJI.sinyal(gun, {**P, "rr_min": 3.0})["giris"].any()
