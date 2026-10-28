import numpy as np
import pytest

from tansu import islem
from tansu.strateji import bos_sinyal
from tests.sentetik import gun_tablosu

CIKIS = islem.Cikis("dokunus", (("hedef1", 0.5), ("hedef2", 0.5)))


def sinyal(gun, gunler=(0,), seviye=10.0, stop=9.0, h1=12.0, h2=13.0, gecerlilik=5):
    s = bos_sinyal(gun.index)
    for i in gunler:
        s.iloc[
            i,
            s.columns.get_indexer(
                [
                    "giris",
                    "giris_tur",
                    "seviye",
                    "gecerlilik",
                    "stop",
                    "hedef1",
                    "hedef2",
                ]
            ),
        ] = [
            True,
            "limit",
            seviye,
            gecerlilik,
            stop,
            h1,
            h2,
        ]
    return s


def kos(gun, s, cikis=CIKIS):
    return islem.simule(gun, s, cikis, sembol="AAA", strateji="t", sinif="a")


def maliyetli(giris, cikis):
    return cikis - giris - (giris + cikis) * 0.0015 * 1.05


def test_maliyet_taraf_basina_komisyon_ve_bsmv():
    assert islem.MALIYET == pytest.approx(0.001575)
    assert islem.maliyet(10.0, 12.0) == pytest.approx(22 * 0.001575)


def test_limit_seviyede_dolar_iki_hedef_paylariyla_kapanir():
    g = gun_tablosu(
        [11, 10.2, 12.2, 13.2, 13.2],
        yuksek=[11.1, 10.5, 12.5, 13.5, 13.3],
        dusuk=[10.9, 9.8, 10.3, 12.3, 13.1],
    )
    (k,), sayac = kos(g, sinyal(g))
    assert k["dolum_fiyati"] == 10.0 and k["dolum_tarihi"] == g.index[1]
    assert k["kismi"].endswith("hedef1 12.0000 x0.5")
    assert k["cikis_nedeni"] == "hedef2" and k["cikis_fiyati"] == 13.0
    beklenen = 0.5 * maliyetli(10, 12) + 0.5 * maliyetli(10, 13)
    assert k["R"] == pytest.approx(beklenen / 1.0)
    assert k["net_yuzde"] == pytest.approx(beklenen / 10 * 100)
    assert (k["hedef1_gun"], k["hedef2_gun"]) == (1, 2)
    assert not sayac[islem.SURE_DOLDU]


def test_seviyenin_altinda_acilan_gun_aofdan_dolar():
    g = gun_tablosu([11, 9.6, 9.6], yuksek=[11.1, 9.7, 9.7], dusuk=[10.9, 9.5, 9.5])
    (k,), _ = kos(g, sinyal(g))
    assert k["dolum_fiyati"] == 9.6 and k["acik"]


def test_stopun_altinda_dolum_hemen_cikar_ve_risk_tabani_kullanilir():
    g = gun_tablosu([11, 8.8, 8.8], yuksek=[11.1, 8.9, 8.9], dusuk=[10.9, 8.7, 8.7])
    (k,), _ = kos(g, sinyal(g))
    assert k["dolumda_stop"] and k["risk_tabanli"]
    assert k["cikis_fiyati"] == 8.8 and k["tutma_gun"] == 0
    assert k["R"] == pytest.approx(maliyetli(8.8, 8.8) / (0.5 * 0.1))


def test_tavan_kilitli_gun_alis_olmaz():
    g = gun_tablosu([11, 10.0, 10.0], yuksek=[11.1, 10.1, 10.1], dusuk=[10.9, 9.9, 9.9])
    g.iloc[1, g.columns.get_loc("kilit_tavan")] = True
    (k,), _ = kos(g, sinyal(g))
    assert k["dolum_tarihi"] == g.index[2]


def test_dolum_gunu_yalniz_stop_denetlenir():
    g = gun_tablosu(
        [11, 10.5, 12.0, 12.0],
        yuksek=[11.1, 12.5, 12.1, 12.1],
        dusuk=[10.9, 9.9, 11.9, 11.9],
    )
    (k,), _ = kos(g, sinyal(g))
    assert k["hedef1_gun"] == 1 and k["kismi"].startswith(str(g.index[2].date()))


def test_ayni_gun_stop_ve_hedef_varsa_yalniz_stop():
    g = gun_tablosu([11, 10.2, 10.0], yuksek=[11.1, 10.5, 12.5], dusuk=[10.9, 9.9, 8.9])
    (k,), _ = kos(g, sinyal(g))
    assert k["cikis_nedeni"] == "stop" and k["cikis_fiyati"] == 9.0 and not k["kismi"]
    assert k["R"] == pytest.approx(maliyetli(10, 9) / 1.0)


def test_taban_kilidinde_satis_olmaz_sonraki_gun_aofdan_cikar():
    g = gun_tablosu(
        [11, 10.2, 8.5, 8.6],
        yuksek=[11.1, 10.5, 8.5, 8.7],
        dusuk=[10.9, 9.9, 8.5, 8.4],
        aof=[11, 10.2, 8.5, 8.55],
    )
    g.iloc[2, g.columns.get_loc("kilit_taban")] = True
    (k,), _ = kos(g, sinyal(g))
    assert k["cikis_tarihi"] == g.index[3] and k["cikis_fiyati"] == 8.55


def test_kapanis_stopu_ertesi_gun_aofdan_cikar():
    g = gun_tablosu(
        [11, 10.2, 8.9, 9.5], yuksek=[11.1, 10.5, 9.6, 9.6], dusuk=[10.9, 9.9, 8.8, 9.4]
    )
    cikis = islem.Cikis("kapanis", CIKIS.hedef)
    (k,), _ = kos(g, sinyal(g), cikis)
    assert k["cikis_nedeni"] == "stop (kapanış)" and k["cikis_fiyati"] == 9.5


def test_emir_suresi_ve_stop_alti_kapanis_emri_dusurur():
    g = gun_tablosu([11, 10.5, 10.6, 10.7, 10.7])
    kayit, sayac = kos(g, sinyal(g, gecerlilik=2))
    assert kayit == [] and sayac[islem.SURE_DOLDU] == 1
    g = gun_tablosu(
        [11, 10.5, 8.0],
        yuksek=[11.1, 10.6, 10.05],
        dusuk=[10.9, 10.4, 7.9],
        aof=[11, 10.5, 10.02],
    )
    g.iloc[2, g.columns.get_loc("kilit_tavan")] = True
    kayit, sayac = kos(g, sinyal(g))
    assert kayit == [] and sayac[islem.STOP_KAPANISI] == 1


def test_red_nedenleri_sayilir():
    g = gun_tablosu([11, 10.6, 10.7, 10.8, 10.9, 11.0])
    g.iloc[4, g.columns.get_loc("uye")] = False
    s = sinyal(g, gunler=(0, 1, 4), gecerlilik=2)
    s.iloc[5, s.columns.get_indexer(["giris", "giris_tur", "seviye", "stop"])] = [
        True,
        "limit",
        10.0,
        10.0,
    ]
    _, sayac = kos(g, s)
    assert sayac[islem.ACIK_VAR] == 1
    assert sayac[islem.UYE_DEGIL] == 1
    assert sayac[islem.STOP_USTTE] == 1
    s = sinyal(g, h1=np.nan, h2=np.nan)
    assert kos(g, s)[1][islem.HEDEF_YOK] == 1


def test_taban_kilidinde_kapanis_stopu_ilk_kilitsiz_gune_kalir():
    g = gun_tablosu(
        [11, 10.2, 8.5, 9.5, 9.6],
        yuksek=[11.1, 10.5, 8.5, 9.6, 9.7],
        dusuk=[10.9, 9.9, 8.5, 9.4, 9.5],
    )
    g.iloc[2, g.columns.get_loc("kilit_taban")] = True
    cikis = islem.Cikis("kapanis", CIKIS.hedef)
    (k,), _ = kos(g, sinyal(g), cikis)
    assert k["cikis_tarihi"] == g.index[3] and k["cikis_nedeni"] == "stop (kapanış)"


def test_taban_kilitli_gunde_stop_altinda_dolum_ertesi_gun_cikar():
    g = gun_tablosu(
        [11, 8.5, 8.7, 8.8],
        yuksek=[11.1, 8.5, 8.8, 8.9],
        dusuk=[10.9, 8.5, 8.6, 8.7],
        aof=[11, 8.5, 8.65, 8.8],
    )
    g.iloc[1, g.columns.get_loc("kilit_taban")] = True
    (k,), _ = kos(g, sinyal(g))
    assert k["dolum_tarihi"] == g.index[1] and k["dolum_fiyati"] == 8.5
    assert k["cikis_tarihi"] == g.index[2] and k["cikis_fiyati"] == 8.65
    assert k["dolumda_stop"]


CIKIS_B = islem.Cikis()


def piyasa(gun, giris=(0,), cikis_sinyali=(), stop=np.nan, gecerlilik=0):
    s = bos_sinyal(gun.index)
    for i in giris:
        s.iloc[i, s.columns.get_indexer(["giris", "giris_tur", "gecerlilik"])] = [
            True,
            "piyasa",
            gecerlilik,
        ]
        s.iloc[i, s.columns.get_loc("stop")] = stop
    for i in cikis_sinyali:
        s.iloc[i, s.columns.get_loc("cikis_sinyali")] = True
    return s


def kos_b(gun, s, cikis=CIKIS_B):
    return islem.simule(gun, s, cikis, sembol="AAA", strateji="t", sinif="b")


def test_piyasa_ilk_fiyatli_gunun_aofundan_dolar_gecerlilik_yok_sayilir():
    g = gun_tablosu(
        [11, np.nan, np.nan, 12, 12, 12], aof=[11, np.nan, np.nan, 11.5, 12, 12]
    )
    (k,), sayac = kos_b(g, piyasa(g))
    assert k["dolum_tarihi"] == g.index[3] and k["dolum_fiyati"] == 11.5
    assert k["giris_tur"] == "piyasa" and k["acik"]
    assert not sayac[islem.SURE_DOLDU] and not sayac[islem.HEDEF_YOK]


def test_piyasa_ust_limit_kilidinde_dolmaz_sinyal_dusur():
    g = gun_tablosu([11, 12, 12, 12])
    g.iloc[1, g.columns.get_loc("kilit_tavan")] = True
    kayit, sayac = kos_b(g, piyasa(g))
    assert kayit == [] and sayac[islem.TAVAN_KILIDI] == 1
    assert not sayac[islem.VERI_SONU]


def test_stopsuz_kurulum_reddedilmez_stop_cikisi_yok_r_nan():
    g = gun_tablosu([11, 11, 5, 4, 4], aof=[11, 11.2, 5, 4, 4])
    s = piyasa(g)
    for cikis in (CIKIS_B, islem.Cikis("kapanis")):
        (k,), sayac = kos_b(g, s, cikis)
        assert not sayac[islem.STOP_USTTE]
        assert k["cikis_nedeni"] == "açık" and k["acik"]
        assert k["net_yuzde"] == pytest.approx(maliyetli(11.2, 4) / 11.2 * 100)
        assert np.isnan([k["R"], k["mfe_R"], k["mae_R"], k["stop"]]).all()
        assert not k["risk_tabanli"] and not k["dolumda_stop"]
        assert np.isnan(k["stop_gun"])


def test_bekleyen_piyasa_emri_varken_gelen_ikinci_sinyal_acik_var_sayilir():
    g = gun_tablosu([11, 11, 11, 11])
    (k,), sayac = kos_b(g, piyasa(g, giris=(0, 1)))
    assert k["sinyal_tarihi"] == g.index[0] and k["dolum_tarihi"] == g.index[1]
    assert sayac[islem.ACIK_VAR] == 1


def test_hedef_yok_yalniz_hedef_listesi_doluysa_sayilir():
    g = gun_tablosu([11, 11, 11])
    assert kos_b(g, piyasa(g))[1][islem.HEDEF_YOK] == 0
    s = sinyal(g, h1=np.nan, h2=np.nan)
    assert kos(g, s)[1][islem.HEDEF_YOK] == 1


def test_cikis_sinyali_ertesi_gun_aofdan_cikar():
    g = gun_tablosu(
        [11, 11, 11.5, 12, 12, 12.5, 12.5], aof=[11, 11.2, 11.5, 12, 12.2, 12.4, 12.5]
    )
    (k,), _ = kos_b(g, piyasa(g, cikis_sinyali=(3,)))
    assert k["cikis_nedeni"] == "çıkış sinyali" and not k["acik"]
    assert k["cikis_tarihi"] == g.index[4] and k["cikis_fiyati"] == 12.2
    assert k["net_yuzde"] == pytest.approx(maliyetli(11.2, 12.2) / 11.2 * 100)
    assert k["tutma_gun"] == 3


def test_cikis_sinyali_alt_limit_kilitli_gunden_sonraki_serbest_gune_kalir():
    g = gun_tablosu([11, 11, 11, 10, 10, 10], aof=[11, 11, 11, 10, 9.9, 9.8])
    g.iloc[3, g.columns.get_loc("kilit_taban")] = True
    (k,), _ = kos_b(g, piyasa(g, cikis_sinyali=(2,)))
    assert k["cikis_tarihi"] == g.index[4] and k["cikis_fiyati"] == 9.9


def test_dolum_gunu_gelen_cikis_sinyali_ertesi_gun_cikar():
    g = gun_tablosu([11, 11, 11, 11], aof=[11, 11, 10.9, 11])
    (k,), _ = kos_b(g, piyasa(g, cikis_sinyali=(1,)))
    assert k["dolum_tarihi"] == g.index[1] and k["cikis_tarihi"] == g.index[2]
    assert k["cikis_fiyati"] == 10.9


def test_kapanis_stopu_ve_cikis_sinyali_ayni_gun_stop_once_gelir():
    g = gun_tablosu(
        [11, 10.2, 8.9, 9.5, 9.5],
        yuksek=[11.1, 10.5, 9.6, 9.6, 9.6],
        dusuk=[10.9, 9.9, 8.8, 9.4, 9.4],
    )
    cikis = islem.Cikis("kapanis", CIKIS.hedef)
    s = sinyal(g)
    s.iloc[2, s.columns.get_loc("cikis_sinyali")] = True
    (k,), _ = kos(g, s, cikis)
    assert k["cikis_nedeni"] == "stop (kapanış)" and k["cikis_fiyati"] == 9.5
