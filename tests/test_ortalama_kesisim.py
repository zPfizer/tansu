import numpy as np
import pandas as pd
import pytest

from tansu.stratejiler import ortalama_kesisim as ok
from tests.sentetik import gun_tablosu, ortalama_yolu

SMA = {"ortalama": "SMA", "cift": "5/20", "teyit_gun": 0}


def sinyal(kapanis, **p):
    return ok.STRATEJI.sinyal(gun_tablosu(kapanis), {**SMA, **p})


def gunler(s, sutun="giris"):
    return np.flatnonzero(s[sutun]).tolist()


def yukselis(dusus=()):
    """30 gün düz, 30 gün +1/gün, sonra `dusus` fiyatları."""
    return [100.0] * 30 + [100.0 + i for i in range(1, 31)] + list(dusus)


def test_dalgada_kesisimde_piyasa_girisi_verir():
    s = sinyal(ortalama_yolu())
    assert gunler(s)
    r = s[s["giris"]].iloc[0]
    assert (r["giris_tur"], r["gecerlilik"], r["durum"]) == ("piyasa", 1, "TETIKLENDI")
    assert np.isnan([r["seviye"], r["stop"], r["hedef1"]]).all()
    assert "SMA 5/20" in r["kural_durumu"] and "teyit_gun 0" in r["kural_durumu"]


def test_duz_cizgide_sinyal_yok():
    s = sinyal([100.0] * 100)
    assert not s["giris"].any() and not s["cikis_sinyali"].any()


def test_isinma_bitmeden_sinyal_yok_ve_ema_2_5_kati_gun_ister():
    yol = ortalama_yolu(80, 30)
    s = sinyal(yol, ortalama="EMA")
    assert gunler(s)  # ısınma sonrası kesişim var
    assert min(gunler(s) + gunler(s, "cikis_sinyali")) >= 51  # ilk geçerli gün 49
    assert (
        ok.ortalama(gun_tablosu(yol)["kapanis"], "EMA", 20).first_valid_index()
        == (gun_tablosu(yol).index[49])
    )


def test_isinma_biterken_zaten_ustte_olan_ortalama_giris_vermez():
    s = sinyal(np.linspace(10, 30, 120), ortalama="EMA")
    assert not s["giris"].any() and not s["cikis_sinyali"].any()


def test_teyit_gun_2_iki_gun_sonra_girer():
    yol = yukselis()
    assert gunler(sinyal(yol)) == [30]
    s2 = sinyal(yol, teyit_gun=2)
    assert gunler(s2) == [32]
    assert "teyit_gun 2" in s2["kural_durumu"].iloc[32]


def test_teyit_gun_2_kapanislar_uzun_ortalamanin_altindaysa_girmez():
    yol = [100.0] * 30 + [130.0, 90.0, 90.0, 90.0]
    assert gunler(sinyal(yol)) == [30]
    assert gunler(sinyal(yol, teyit_gun=2)) == []


def test_cikis_sinyali_yalniz_karsi_kesisimde():
    yol = yukselis(dusus=[60 - 3 * i for i in range(1, 21)])
    s = sinyal(yol)
    kapanis = pd.Series(yol)
    kisa, uzun = kapanis.rolling(5).mean(), kapanis.rolling(20).mean()
    (cikis,) = gunler(s, "cikis_sinyali")
    assert cikis >= 60  # yükselişte değil, düşüşte (zirve 59. gün)
    assert kisa[cikis] <= uzun[cikis] and kisa[cikis - 1] > uzun[cikis - 1]
    assert not s["giris"].iloc[cikis]


def test_bilinmeyen_ortalama_turu_hata_verir():
    with pytest.raises(ValueError):
        sinyal([100.0] * 30, ortalama="HMA")
