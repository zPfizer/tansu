"""E3 dolum kimliği ve para girdisi sınırları (TASARIM 5.15 S08)."""

import pytest

from tansu import islem_riski


@pytest.mark.parametrize(
    "dolumlar",
    [
        [dict(dolum_id="x", yon="alis", adet=0, fiyat=100)],
        [dict(dolum_id="x", yon="alis", adet=1, fiyat=float("inf"))],
        [dict(dolum_id="x", yon="alis", adet=1e308, fiyat=1e308)],
        [dict(dolum_id="", yon="alis", adet=1, fiyat=100)],
        [dict(dolum_id="x", yon="satis", adet=1, fiyat=100)],
        [
            dict(dolum_id="x", yon="alis", adet=1, fiyat=100),
            dict(dolum_id="y", yon="satis", adet=2, fiyat=100),
        ],
        [
            dict(dolum_id="x", yon="alis", adet=1, fiyat=100),
            dict(dolum_id="x", yon="alis", adet=2, fiyat=100),
        ],
    ],
)
def test_bozuk_dolum_ve_celiskili_tekrar_hata_verir(dolumlar):
    with pytest.raises(ValueError):
        islem_riski.maliyet_hesapla(dolumlar, masraf_surumu="komisyon_bsmv_v1")


def test_bilinmeyen_surum_sessizce_eski_politikaya_donmez():
    with pytest.raises(ValueError, match="risk sürümü"):
        islem_riski.boyutla(100, 90, 100_000, aile="ema_sikismasi", risk_surumu="yok")
    with pytest.raises(ValueError, match="masraf sürümü"):
        islem_riski.maliyet_hesapla([], masraf_surumu="yok")


def test_s08_masraf_butcenin_icinde_tam_adet_ve_kalan_butce():
    s = islem_riski.boyutla(
        100, 90, 100_000, aile="ema_sikismasi", risk_surumu="bagimsiz_risk_v1"
    )
    # Bir adet: 10 TL fiyat riski + 0,1575 alış + 0,14175 stop masrafı.
    # 194 adet: 1.940 + 30,555 + 27,4995 = 1.998,0545. 195 adet: 2.008,35375.
    assert s["adet"] == 194
    assert s["birim_risk"] == pytest.approx(10.29925)
    assert s["planlanan_giris_maliyeti"] == pytest.approx(30.555)
    assert s["planlanan_stop_maliyeti"] == pytest.approx(27.4995)
    assert s["planlanan_risk"] == pytest.approx(1998.0545)
    assert s["ilk_risk"] == s["planlanan_risk"]
    assert s["kullanilmayan_butce"] == pytest.approx(1.9455)
    assert s["planlanan_risk"] <= s["risk_butcesi"] == 2000
    assert s["risk_nedeni"] is None


@pytest.mark.parametrize(
    "nominal,adet,kalan,neden",
    [
        (100, 0, 2, "butce_yetersiz"),
        (514.9625, 1, 0, None),
        (514.96249, 0, 10.2992498, "butce_yetersiz"),
    ],
)
def test_s08_bir_adet_butce_siniri(nominal, adet, kalan, neden):
    s = islem_riski.boyutla(
        100, 90, nominal, aile="ema_sikismasi", risk_surumu="bagimsiz_risk_v1"
    )
    assert s["adet"] == adet
    assert s["kullanilmayan_butce"] == pytest.approx(kalan)
    assert s["risk_nedeni"] == neden
    assert s["planlanan_risk"] <= s["risk_butcesi"]
    if adet == 0:
        assert s["planlanan_risk"] == 0
        assert s["ilk_risk"] is None and s["net_r"] is None


@pytest.mark.parametrize(
    "cikis,net,kayip,net_r",
    [(90, -1998.0545, 1940, -1), (80, -3934.999, 3880, -1.9694152486831565)],
)
def test_s08_ilk_risk_sabittir_stop_otesi_sonuc_kesilmez(cikis, net, kayip, net_r):
    s = islem_riski.hesapla(
        dict(
            giris_fiyat=100,
            ilk_stop=90,
            nominal_tutar=100_000,
            aile="ema_sikismasi",
            risk_surumu="bagimsiz_risk_v1",
            masraf_surumu="komisyon_bsmv_v1",
            dolumlar=[
                dict(dolum_id="al", yon="alis", adet=194, fiyat=100),
                dict(dolum_id="sat", yon="satis", adet=194, fiyat=cikis),
            ],
        )
    )
    assert s["planlanan_risk"] == pytest.approx(1998.0545)
    assert s["ilk_risk"] == s["planlanan_risk"]
    assert s["gerceklesen_kayip"] == kayip
    assert s["net_sonuc"] == pytest.approx(net)
    assert s["net_r"] == pytest.approx(net_r)
    if cikis == 80:
        assert s["gerceklesen_maliyet"] == pytest.approx(54.999)
        assert s["gerceklesen_kayip_r"] == pytest.approx(1.9418889724979974)
        assert s["gerceklesen_kayip"] > s["planlanan_risk"]
        assert s["net_r"] < -1


def test_s08_cift_boyutu_ve_r_bos_fiyat_sonucu_korunur():
    s = islem_riski.hesapla(
        dict(
            giris_fiyat=100,
            ilk_stop=None,
            nominal_tutar=100_000,
            aile="cift_rotasyonu",
            risk_surumu="bagimsiz_risk_v1",
            masraf_surumu="komisyon_bsmv_v1",
            dolumlar=[
                dict(dolum_id="al", yon="alis", adet=100, fiyat=100),
                dict(dolum_id="sat", yon="satis", adet=100, fiyat=80),
            ],
        )
    )
    assert s["adet"] is None and s["ilk_risk"] is None and s["net_r"] is None
    assert s["planlanan_risk"] is None
    assert s["risk_nedeni"] == "risk_dayanagi_eksik"
    assert s["net_sonuc"] == pytest.approx(-2028.35)
