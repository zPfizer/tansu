"""Tansu sınaması yüzü (TASARIM 5.14): işlem getirisi, Tansu ölçüleri, sağlam bölge, ileri yürüme, işçi sayısı, koşu.

Masraf m = 0,001 (her yönde %0,10). Beklenen değerler elle hesaplanmıştır (her testin yorumunda).

EMA verisi: tests/test_saglamlik.py'deki seri (26.01.2026'dan 8 gün; son kapanış 110). Sinyal gün 5 (02.02, kapanış 103),
giriş 03.02 AOF 104, çıkış 04.02 son kapanış 110 (veri sonu). Dönem 02.02-04.02 (3 gün).
Çift verisi: A, B, C 270 işlem günü (2025-01-01'den). B ve C 100'de sabit; A 255-261. günler 95, sonra 100.
"""

import dataclasses
import json
import re

import numpy as np
import pandas as pd
import pytest

from tansu import __main__ as komut
from tansu import aileler, kayit, motor, veri
from tansu import tansusinama as ts
from tests.test_k1 import anlik_hazirla
from tests.test_simulator import BAS, KAP, P, YUK, duz, mum

KAP_A = KAP[:7] + [110.0]
YUK_A = YUK[:7] + [110.5]
EMA_IZGARA = {"esik": [0.005], "min_gun": [3], "pencere": [3]}
CIFT_IZGARA = {"z_pencere": [5], "z_esik": [1.0, 1.5]}


def risk_satiri(**degisiklik):
    return dict(
        giris_fiyat=100.0,
        cikis_fiyat=80.0,
        ilk_stop=90.0,
        nominal_tutar=100_000.0,
        risk_surumu="bagimsiz_risk_v1",
        masraf_surumu="komisyon_bsmv_v1",
        aile="ema_sikismasi",
        **degisiklik,
    )


def test_s08_butce_es_zamanli_islemlerden_ve_sonuclarindan_bagimsiz():
    t = pd.DataFrame(
        [
            risk_satiri(sinyal_id=str(i), giris_tarih=pd.Timestamp("2026-10-05"))
            for i in range(12)
        ]
    )
    s = ts._getirili(t)
    assert s.get("risk_butcesi", pd.Series(dtype=float)).tolist() == [2000.0] * 12
    assert s.sinyal_id.tolist() == [str(i) for i in range(12)]
    assert s.adet.tolist() == [194] * 12
    assert s.risk_nedeni.tolist() == [None] * 12
    assert (s.adet * s.giris_fiyat).sum() == 232_800
    assert s.planlanan_risk.tolist() == pytest.approx([1998.0545] * 12)
    t.loc[0, "cikis_fiyat"] = 200.0
    pd.testing.assert_frame_equal(s, ts._getirili(t).assign(cikis_fiyat=80.0))
    t["dolumlar"] = [
        [
            dict(dolum_id="al", yon="alis", adet=194, fiyat=100),
            dict(dolum_id="sat", yon="satis", adet=194, fiyat=80),
        ]
        for _ in range(12)
    ]
    zararli = ts._getirili(t)
    assert zararli.iloc[0].net_sonuc == pytest.approx(-3934.999)
    t.at[0, "dolumlar"][1]["fiyat"] = 200
    karli = ts._getirili(t)
    assert karli.iloc[0].net_sonuc == pytest.approx(19308.335)
    pd.testing.assert_frame_equal(zararli.iloc[1:], karli.iloc[1:])


def test_s08_komisyon_bsmv_ve_stop_otesi_kayip_ayri_alanlar():
    dolumlar = [
        dict(dolum_id="al", yon="alis", adet=100, fiyat=100),
        dict(dolum_id="sat", yon="satis", adet=100, fiyat=80),
    ]
    s = ts._getirili(pd.DataFrame([risk_satiri(dolumlar=dolumlar)])).iloc[0]
    # 10.000 alış: 15 + 0,75; 8.000 satış: 12 + 0,60.
    assert s.get("gerceklesen_maliyet") == pytest.approx(28.35)
    assert s.alis_maliyeti == pytest.approx(15.75)
    assert s.satis_maliyeti == pytest.approx(12.60)
    assert s.gerceklesen_kayip == 2000.0
    assert s.net_sonuc == pytest.approx(-2028.35)
    assert s.planlanan_risk == pytest.approx(1998.0545)
    assert s.net_r == pytest.approx(-1.0151624993212147)
    assert s.net_sonuc < -s.risk_butcesi
    assert s.referans_getirisi == pytest.approx(-0.0202835)
    assert s.net_fiyat_getirisi == pytest.approx(-0.202516037241345)


def test_s08_kismi_satis_gerceklesen_adet_ve_tekrar_dolum():
    al = dict(dolum_id="al", yon="alis", adet=100, fiyat=100)
    yari = dict(dolum_id="yari", yon="satis", adet=40, fiyat=110)
    dolumlar = [al, yari, yari.copy()]
    ilk = ts._getirili(pd.DataFrame([risk_satiri(dolumlar=dolumlar)])).iloc[0]
    assert ilk.get("gerceklesen_maliyet") == pytest.approx(22.68)
    assert ilk.net_sonuc == pytest.approx(386.77)
    assert ilk.kalan_adet == 60
    assert ilk.kalan_alis_maliyeti == pytest.approx(9.45)
    assert pd.isna(ilk.net_fiyat_getirisi)
    assert pd.isna(ilk.referans_getirisi), (
        "Açık işlemin nihai referans getirisi boş kalmalı"
    )
    assert pd.isna(ilk.net_r), "Açık işlemin nihai R sonucu boş kalmalı"
    assert ilk.bos_nedenleri == dict.fromkeys(
        ("net_fiyat_getirisi", "referans_getirisi", "net_r"), "islem_acik"
    )
    kismi = ilk.gerceklesen_kismi_sonuclar
    assert len(kismi) == 1  # Aynı dolum kimliğinin tekrarı kısmi sonuç da eklemez.
    assert kismi[0]["dolum_id"] == "yari" and kismi[0]["adet"] == 40
    assert kismi[0]["net_sonuc"] == pytest.approx(386.77)
    assert kismi[0]["referans_getirisi"] == pytest.approx(0.0038677)
    assert kismi[0]["net_r"] == pytest.approx(0.19357329842604393)
    dolumlar.append(dict(dolum_id="son", yon="satis", adet=60, fiyat=90))
    son = ts._getirili(pd.DataFrame([risk_satiri(dolumlar=dolumlar)])).iloc[0]
    assert son.gerceklesen_maliyet == pytest.approx(31.185)
    assert son.net_sonuc == pytest.approx(-231.185)
    assert son.kalan_adet == 0
    assert son.referans_getirisi == pytest.approx(-0.00231185)
    assert son.net_r == pytest.approx(-0.11570505208942001)
    assert son.bos_nedenleri == {}
    assert son.gerceklesen_kismi_sonuclar == kismi


def test_s08_dolumlu_ve_dolumsuz_satirlar_ayni_tabloda():
    t = pd.DataFrame(
        [
            risk_satiri(sinyal_id="aday"),
            risk_satiri(
                sinyal_id="dolu",
                dolumlar=[
                    dict(dolum_id="al", yon="alis", adet=194, fiyat=100),
                    dict(dolum_id="sat", yon="satis", adet=194, fiyat=80),
                ],
            ),
            risk_satiri(sinyal_id="bos_liste", dolumlar=[]),
            risk_satiri(sinyal_id="none", dolumlar=None),
        ]
    )
    hata = None
    try:
        s = ts._getirili(t).set_index("sinyal_id")
    except TypeError as exc:
        hata = str(exc)
    assert hata is None, f"Geçerli karma dolum tablosu hesaplanmalı: {hata}"
    assert s.adet.tolist() == [194] * 4
    assert pd.isna(s.loc["aday", "gerceklesen_maliyet"])
    assert pd.isna(s.loc["none", "gerceklesen_maliyet"])
    assert s.loc["bos_liste", "gerceklesen_maliyet"] == 0
    assert pd.isna(s.loc["bos_liste", "net_r"])
    assert s.loc["bos_liste", "bos_nedenleri"]["net_r"] == "giris_dolumu_yok"
    assert s.loc["dolu", "net_sonuc"] == pytest.approx(-3934.999)
    assert s.loc["dolu", "net_r"] == pytest.approx(-1.9694152486831565)


@pytest.mark.parametrize(
    ("alan", "deger", "neden"),
    [
        ("ilk_stop", 100, "gecersiz_risk_girdisi"),
        ("ilk_stop", 101, "gecersiz_risk_girdisi"),
        ("ilk_stop", 0, "gecersiz_risk_girdisi"),
        ("ilk_stop", None, "gecersiz_risk_girdisi"),
        ("giris_fiyat", float("inf"), "gecersiz_risk_girdisi"),
        ("nominal_tutar", float("nan"), "gecersiz_risk_girdisi"),
        ("nominal_tutar", -1, "gecersiz_risk_girdisi"),
        ("aile", "cift_rotasyonu", "risk_dayanagi_eksik"),
    ],
)
def test_s08_gecersiz_girdi_ve_cift_gerekceli_bos(alan, deger, neden):
    r = risk_satiri()
    r[alan] = deger
    s = ts._getirili(pd.DataFrame([r])).iloc[0]
    assert s.get("risk_nedeni") == neden
    assert pd.isna(s.adet) and pd.isna(s.ilk_risk) and pd.isna(s.net_r)


def test_s08_legacy_getiri_ve_adet_korunur():
    s = ts._getirili(pd.DataFrame([dict(giris_fiyat=100, cikis_fiyat=110, adet=7)]))
    assert s.adet.tolist() == [7]
    assert s.getiri.tolist() == pytest.approx([0.0978021978021979])


IZGARA = {"ema_sikismasi": EMA_IZGARA, "cift_rotasyonu": CIFT_IZGARA}
GUNLER = pd.bdate_range("2025-01-01", periods=270)


def uyelikli_veri(tmp_path, bas="2021-03-24", uzat=False):
    kap, yuk = KAP_A + ([111.0] if uzat else []), YUK_A + ([111.5] if uzat else [])
    gunler = pd.bdate_range(bas, periods=len(kap))
    seri = [
        mum(g, k, y, k - 0.5, 1e9) for g, k, y in zip(gunler, kap, yuk, strict=True)
    ]
    a = anlik_hazirla(tmp_path, {s: seri for s in ("AKBNK", "MGROS", "SASA")})
    istek = veri.VeriIstegi(
        ("AKBNK", "MGROS", "SASA"),
        str(gunler[0].date()),
        str(gunler[-1].date()),
        "kayitli",
        "legacy_portfoy_v1",
        "bist30_2021_2025_v1",
        "duzeltme_v1",
        "takvim_v1",
        evren_politikasi="donemsel_bist30_v1",
    )
    return a, veri.veri_hazirla(istek, a.kimlik, tmp_path)


def test_s05_giris_gunu_uyeligi_sinyalden_ayri_denetlenir(tmp_path):
    # Sinyal 31 Mart, dolum 1 Nisan: MGROS çıkar, SASA ancak dolum günü üyedir.
    a, paket = uyelikli_veri(tmp_path)
    eski, _ = motor.sinama(a, P)
    assert set(eski["sembol"]) == {"AKBNK", "MGROS", "SASA"}
    sonuc, dusen = motor.sinama(a, P, veri_paketi=paket)
    assert set(sonuc["sembol"]) == {"AKBNK"}
    assert dusen == 2
    giris = sonuc.iloc[0]
    assert str(giris.sinyal_tarih.date()) == "2021-03-31"
    assert str(giris.giris_tarih.date()) == "2021-04-01"
    assert giris.uyelik_kaniti["kaynak_id"] == "A001"
    assert giris.uyelik_kaniti["sembol"] == "AKBNK"
    assert sonuc.attrs["uyelik_surumu"] == "bist30_2021_2025_v1"
    assert sonuc.attrs["veri_referanslari"] == [paket["referans"]]
    retler = {r["sembol"]: r for r in sonuc.attrs["uyelik_retleri"]}
    assert retler["MGROS"]["neden"] == "giris_gununde_uye_degil"
    assert retler["SASA"]["neden"] == "sinyal_gununde_uye_degil"
    assert retler["MGROS"]["giris_tarih"] == "2021-04-01"


def test_s05_e1_veri_referansi_uyelik_kanitina_baglanir(tmp_path):
    _, paket = uyelikli_veri(tmp_path)
    assert "uyelik" in paket
    assert (
        paket["referans"]["uyelik_tablo_parmak_izi"]
        == paket["uyelik"]["tablo_parmak_izi"]
    )
    assert paket["referans"]["evren_politikasi"] == "donemsel_bist30_v1"
    assert paket["referans"]["goruntu_id"]
    assert paket["referans"]["manifest_parmak_izi"]


@pytest.mark.parametrize("eksik", ["gun", "uye"])
def test_s05_eksik_kanit_motor_kosusunu_durdurur(tmp_path, eksik):
    a, paket = uyelikli_veri(tmp_path)
    if eksik == "gun":
        del paket["uyelik"]["gunler"]["2021-04-01"]
    else:
        paket["uyelik"]["gunler"]["2021-04-01"]["semboller"].remove("AKBNK")
    with pytest.raises(veri.UyelikKapsamHatasi) as hata:
        motor.sinama(a, P, veri_paketi=paket)
    assert hata.value.eksik_tarihler == ["2021-04-01"]
    assert hata.value.uyelik_surumu == "bist30_2021_2025_v1"


def test_s05_uyelikten_cikis_acik_islemi_kapatmaz(tmp_path):
    # Sinyal 30 Mart, giriş 31 Mart; MGROS 1 Nisan'da çıkar, 2 Nisan'a dek tutulur.
    a, paket = uyelikli_veri(tmp_path, "2021-03-23", uzat=True)
    eski, _ = motor.sinama(a, P)
    sonuc, _ = motor.sinama(a, P, veri_paketi=paket)
    r = sonuc.set_index("sembol").loc["MGROS"]
    once = eski.set_index("sembol").loc["MGROS"]
    assert r.giris_tarih == pd.Timestamp("2021-03-31")
    assert r.cikis_tarih == once.cikis_tarih == pd.Timestamp("2021-04-02")
    assert r.neden == once.neden == "veri_sonu"
    assert r.uyelik_kaniti["yururluk_bitisi"] == "2021-03-31"


def seri_a():
    return [
        mum(g, k, y, k - 0.5, 1e9)
        for g, k, y in zip(
            pd.bdate_range("2026-01-26", periods=8), KAP_A, YUK_A, strict=True
        )
    ]


def ema_anlik(tmp_path, b=None, a=None):
    return anlik_hazirla(tmp_path, {"A": a or seri_a(), "B": b or duz(1e9)})


def cift_anlik(tmp_path, a_satir=None, ek=None, b_gun=270):
    """`a_satir`: A'nın dizin → alan değişiklikleri (ham alanlar kilit ve karantinayı sürer, Z düzeltilmiş kapanıştan
    hesaplanır); değer None ise A'nın o günü satırı yoktur. `ek`: ek hisse serileri; `b_gun`: B'nin satır sayısı."""
    a = [95.0 if 255 <= i < 262 else 100.0 for i in range(270)]
    sabit = [mum(g, 100.0) for g in GUNLER]
    a_mum = [mum(g, k) for g, k in zip(GUNLER, a, strict=True)]
    for i, alan in (a_satir or {}).items():
        if alan is not None:
            a_mum[i].update(alan)
    a_mum = [m for i, m in enumerate(a_mum) if (a_satir or {}).get(i, 1) is not None]
    seriler = {"A": a_mum, "B": sabit[:b_gun], "C": sabit, **(ek or {})}
    return anlik_hazirla(tmp_path, seriler)


def sade(sonuc):
    """Süre ve makine alanları çıkarılmış sonuç: işçi sayısından bağımsız olmalı."""
    return json.dumps(
        {k: v for k, v in sonuc.items() if k not in ("kosu_id", "makine")},
        sort_keys=True,
        allow_nan=False,
    )


def hisse(sonuc, aile, ad):
    return next(h for h in sonuc["aileler"][aile]["hisseler"] if h["hisse"] == ad)


def test_islem_getirisi_masrafli_cikis_bolu_giris():
    # 110·0,999 / (100·1,001) − 1 = 109,89 / 100,1 − 1 = 0,0978022
    assert ts.islem_getirisi(100, 110) == pytest.approx(0.0978022, abs=1e-7)


def test_olculer_uc_islem_tansu_tablosu_sutunlari():
    # İşlemler +%10, −%5, +%2; tutma 2, 1, 3 gün. Özkaynak eğrisi 6 gün (başlangıç 1):
    # [1,0; 1,1; 1,045; 1,045; 1,0659; 1,0659]; pozisyonda 4 gün.
    # net = 1,1·0,95·1,02 − 1 = 0,0659; kazanma 2/3; kâr çarpanı (0,10+0,02)/0,05 = 2,4;
    # ortalama işlem 0,07/3 = 0,0233333; medyan 0,02; kazanç/kayıp = ((0,10+0,02)/2)/0,05 = 1,2.
    # Günlük getiri [0; 0,10; −0,05; 0; 0,02; 0]: ortalama 0,0116667, sapma (ddof 1) 0,0491596;
    # Sharpe = 0,0116667/0,0491596·√252 = 3,767374. En büyük düşüş = 1,045/1,1 − 1 = −0,05.
    # Calmar = (1,0659^(252/6) − 1)/0,05 = 271,8243. Ortalama tutma 2; maruziyet 4/6.
    o = ts.olculer(
        [0.10, -0.05, 0.02], [2, 1, 3], [1.0, 1.1, 1.045, 1.045, 1.0659, 1.0659], 4
    )
    assert (o["islem"], o["kazanan"], o["kaybeden"]) == (3, 2, 1)
    assert o["kazanma"] == pytest.approx(2 / 3)
    assert o["kar_carpani"] == pytest.approx(2.4)
    assert o["ort_islem"] == pytest.approx(0.0233333, abs=1e-7)
    assert o["medyan_islem"] == pytest.approx(0.02)
    assert o["net"] == pytest.approx(0.0659)
    assert o["max_dd"] == pytest.approx(-0.05)
    assert o["sharpe"] == pytest.approx(3.767374, abs=1e-5)
    assert o["calmar"] == pytest.approx(271.8243, abs=1e-3)
    assert o["ort_tutma"] == pytest.approx(2.0)
    assert o["maruziyet"] == pytest.approx(4 / 6)
    assert o["kazanc_kayip"] == pytest.approx(1.2)
    assert o["bayraklar"] == ["az işlem"]


def test_olculer_islem_yoksa_net_sifir_ve_oranlar_yok():
    # Düz eğri: günlük getiri sapması 0 → Sharpe yok; en büyük düşüş 0 → Calmar yok; 0 işlem → net 0,0.
    o = ts.olculer([], [], [1.0] * 6, 0)
    assert (o["islem"], o["net"], o["maruziyet"]) == (0, 0.0, 0.0)
    for anahtar in (
        "kazanma",
        "kar_carpani",
        "ort_islem",
        "medyan_islem",
        "sharpe",
        "calmar",
        "ort_tutma",
        "kazanc_kayip",
    ):
        assert o[anahtar] is None
    assert o["max_dd"] == 0.0
    assert o["bayraklar"] == ["az işlem"]


def test_bayraklar_asiri_uyum_az_islem_ve_temiz():
    # 10 işlemin 10'u kazanan: kazanma 1,0 ≥ 0,90 → şüpheli; işlem 10 ≥ 5 → az işlem yok. Kaybeden yok → kâr çarpanı yok.
    on = ts.olculer([0.01] * 10, [1] * 10, [1.0] * 10, 10)
    assert on["bayraklar"] == ["şüpheli: aşırı uyum"]
    assert on["kar_carpani"] is None and on["kazanc_kayip"] is None
    # 4 işlem, 2 kazanan: kazanma 0,5 → şüpheli değil; işlem 4 < 5 → az işlem.
    dort = ts.olculer([0.02, -0.01, 0.02, -0.01], [1] * 4, [1.0] * 4, 4)
    assert dort["bayraklar"] == ["az işlem"]
    # 5 işlem, 3 kazanan: kazanma 0,6; işlem 5 ≥ 5 → bayrak yok. Sınır: 9 kazanan / 10 = 0,9 şüpheli sayılır.
    bes = ts.olculer([0.02, -0.01, 0.02, -0.01, 0.02], [1] * 5, [1.0] * 5, 5)
    assert bes["bayraklar"] == []
    sinir = ts.olculer([0.01] * 9 + [-0.01], [1] * 10, [1.0] * 10, 10)
    assert sinir["bayraklar"] == ["şüpheli: aşırı uyum"]


def test_saglam_bolge_tek_nokta_tuzak_sagliksiz():
    # Yalnız orta hücre kârlı (+%5), bütün komşuları zararda: hiçbir hücrenin komşuları kârlı değil → sağlam bölge yok.
    # En iyi = orta hücre (düz sıra 4); seçilen yok; en iyi kârlı olduğundan para çıkmaz değil.
    net = np.full((3, 3), -0.01)
    net[1, 1] = 0.05
    r = ts.saglam_bolge(net)
    assert r["saglam"].shape == (3, 3) and not r["saglam"].any()
    assert r["secilen"] is None
    assert r["en_iyi"] == 4
    assert not r["para_cikmaz"]


def test_saglam_bolge_blok_secim_maksimin_ve_esitlikte_ilk():
    # Izgara (3×3), komşu = tek eksende bir adım (köşegen yok):
    #   0,01  0,02 -0,01
    #   0,03  0,05  0,03
    #   0,03  0,04  0,06
    # Sağlam: (0,1) komşusu (0,2) zararda → değil; (1,2) komşusu (0,2) zararda → değil; (0,2) zararda. Köşegen sayılsaydı
    # (1,1) de elenirdi (köşegeni (0,2) zararda): (1,1) komşuları 0,02, 0,04, 0,03, 0,03 kârlı → sağlam.
    # Komşuluk (kendisi dahil) en küçük net: (0,0) 0,01; (1,0) 0,01; (1,1) 0,02; (2,0) min(0,03; 0,03; 0,04) = 0,03;
    # (2,1) min(0,04; 0,05; 0,03; 0,06) = 0,03; (2,2) min(0,06; 0,03; 0,04) = 0,03.
    # En büyük 0,03: üç hücre eşit → düz sıradaki ilk: (2,0) = 6. En iyi tek hücre = 0,06 → 8.
    net = np.array([[0.01, 0.02, -0.01], [0.03, 0.05, 0.03], [0.03, 0.04, 0.06]])
    r = ts.saglam_bolge(net)
    assert r["saglam"].ravel().tolist() == [
        True,
        False,
        False,
        True,
        True,
        False,
        True,
        True,
        True,
    ]
    assert r["secilen"] == 6
    assert r["en_iyi"] == 8
    assert not r["para_cikmaz"]


def test_saglam_bolge_hepsi_zararda_para_cikmaz():
    # En iyi = en az zararlı: (1,1) = −0,01 → düz sıra 4. Hiçbir hücre kârlı değil → sağlam yok, seçilen yok, para çıkmaz.
    r = ts.saglam_bolge(np.array([[-0.05, -0.02, -0.04], [-0.03, -0.01, -0.06]]))
    assert not r["saglam"].any()
    assert r["secilen"] is None and r["en_iyi"] == 4 and r["para_cikmaz"]


def test_saglam_bolge_sifir_net_kar_sayilmaz():
    # Net 0,0 (işlem yok) pozitif değildir: en iyi = 0,0 (ilk, düz sıra 0) ≤ 0 → para çıkmaz.
    r = ts.saglam_bolge(np.zeros(3))
    assert not r["saglam"].any()
    assert r["secilen"] is None and r["en_iyi"] == 0 and r["para_cikmaz"]


def test_saglam_bolge_uc_eksen_komsu_sayisi():
    # 3×3×3, yalnız (0,0,0) = −0,01; ötekiler 0,01. Köşenin üç komşusu ((1,0,0), (0,1,0), (0,0,1)) komşusu zararlı hücre
    # olduğundan sağlam değil; köşe de zararda: 27 − 1 − 3 = 23 sağlam hücre. Hepsinin komşuluk en küçüğü 0,01 → eşitlikte
    # düz sıradaki ilk sağlam hücre: (0,0,2) = 2 ((0,0,1) sağlam değil). En iyi: 0,01 eşit → ilk = (0,0,1) = 1.
    net = np.full((3, 3, 3), 0.01)
    net[0, 0, 0] = -0.01
    r = ts.saglam_bolge(net)
    assert r["saglam"].shape == (3, 3, 3) and r["saglam"].sum() == 23
    assert r["secilen"] == 2
    assert r["en_iyi"] == 1


@pytest.mark.parametrize(
    "cekirdek, bos_gb, is_sayisi, isci_gb, beklenen",
    [
        (32, 10.0, 99, 0.5, 16),  # bellek bağlar: int(10·0,8/0,5) = 16
        (32, 64.0, 5, 0.5, 5),  # iş sayısı bağlar: min(32, 102, 5)
        (4, 0.1, 99, 0.5, 1),  # int(0,08/0,5) = 0 → en az 1
        (8, 100.0, 99, 0.5, 8),  # çekirdek bağlar
    ],
)
def test_isci_sayisi_en_kucuk_sinir_en_az_bir(
    cekirdek, bos_gb, is_sayisi, isci_gb, beklenen
):
    assert ts.isci_sayisi(cekirdek, bos_gb, is_sayisi, isci_gb) == beklenen


def test_makine_cekirdek_bellek_ve_gpu():
    m = ts.makine()
    assert m["cekirdek"] >= 1
    assert 1 <= m["fiziksel_cekirdek"] <= m["cekirdek"]
    assert 0 < m["bellek_bos_gb"] <= m["bellek_toplam_gb"]
    assert m["gpu"] is None or isinstance(m["gpu"], str)


def yillik(*getiriler):
    """2016-2021 yıllık işlem: 03.02 giriş, 03.10 çıkış."""
    return [
        (f"{y}-03-02", f"{y}-03-10", r)
        for y, r in zip(range(2016, 2022), getiriler, strict=True)
    ]


def tablo(satirlar):
    return pd.DataFrame(
        [(pd.Timestamp(g), pd.Timestamp(c), r) for g, c, r in satirlar],
        columns=["giris_tarih", "cikis_tarih", "getiri"],
    )


def hucre_tablolari(h0_2020=-0.02):
    return [
        tablo(yillik(0.10, 0.05, 0.08, -0.20, h0_2020, 0.10)),
        tablo(
            yillik(0.04, 0.04, -0.01, 0.04, 0.04, 0.10)
            + [("2018-12-20", "2019-01-15", 0.05)]
        ),
        tablo(
            yillik(0.03, 0.03, 0.02, 0.03, 0.03, 0.10)
            + [("2019-01-10", "2019-01-12", 0.50)]
        ),
        tablo(yillik(0.02, 0.06, 0.02, 0.02, -0.50, 0.10)),
    ]


def test_ileri_yil_yil_secim_nakit_yili_ve_dikis():
    # Izgara 2×2: düz sıra 0=(0,0), 1=(0,1), 2=(1,0), 3=(1,1); komşular 0:{1,2}, 1:{0,3}, 2:{0,3}, 3:{1,2}.
    # bas 2016-01-01 → ilk tam yıl 2016, en az 2 eğitim yılı → test yılları 2018-2021. Seçim, Y'den önce kapanmış işlemlerle.
    # 2018 (2016-17): net [1,1·1,05−1 = 0,155; 1,04²−1 = 0,0816; 1,03²−1 = 0,0609; 1,02·1,06−1 = 0,0812]: hepsi sağlam.
    #   komşuluk en küçüğü [0,0609; 0,0812; 0,0609; 0,0609] → hücre 1. Girişi 2018'de: −%1 (03.02), +%5 (20.12).
    # 2019 (2016-18; hücre 1'in 20.12 işlemi 2019-01-15'te kapanır → eğitime girmez, hücre 2'nin 12.01 işlemi de):
    #   net [0,2474; 1,04²·0,99−1 = 0,070784; 1,03²·1,02−1 = 0,082118; 1,02·1,06·1,02−1 = 0,102824]; hepsi sağlam.
    #   komşuluk en küçüğü [0,070784; 0,070784; 0,082118; 0,070784] → hücre 2. Girişi 2019'da: 10.01 (+%50) önceki işlem
    #   (2019-01-15'te kapanan) kapanmadan girdiği için atılır; 02.03 (+%3) alınır.
    # 2020 (2016-19): net [−0,00208; ...; ...; 0,12488]: hücre 0 zararda → 1 ve 2'nin komşusu zararda; yalnız 3 sağlam. +(−%50).
    # 2021 (2016-20): hücre 0: 0,99792·0,98−1 = −0,0220 ve hücre 3: 1,12488·0,5−1 = −0,4376 zararda → sağlam hücre yok → nakit.
    # Dikiş: 0,99·1,05·1,03·0,5 − 1 = −0,4646575; işlem 4.
    r = ts.ileri(
        hucre_tablolari(),
        (2, 2),
        pd.Timestamp("2016-01-01"),
        pd.Timestamp("2021-12-31"),
    )
    assert r["yillar"] == [
        {"yil": 2018, "hucre": 1},
        {"yil": 2019, "hucre": 2},
        {"yil": 2020, "hucre": 3},
        {"yil": 2021, "hucre": None},
    ]
    assert r["islem"] == 4
    assert r["net"] == pytest.approx(-0.4646575, abs=1e-7)


def test_ileri_gelecege_bakmaz_eski_yil_sonraki_secimi_degistirir_oncekini_degil():
    # Hücre 0'ın 2020 işlemi +%50 olursa 2021 eğitiminde net 0,99792·1,5 − 1 = 0,49688 > 0: hücre 0 komşuları (1 ve 2)
    # kârlı → sağlam; hücre 1 ve 2'nin komşusu 3 zararda → yalnız hücre 0 sağlam. 2021'de hücre 0 alınır (+%10).
    # 2018-2020 aynı kalır (2020 işlemi o yılların eğitimine girmez). Net: 0,5353425·1,1 − 1 = −0,41112325; işlem 5.
    r = ts.ileri(
        hucre_tablolari(0.50),
        (2, 2),
        pd.Timestamp("2016-01-01"),
        pd.Timestamp("2021-12-31"),
    )
    assert [y["hucre"] for y in r["yillar"]] == [1, 2, 3, 0]
    assert r["islem"] == 5
    assert r["net"] == pytest.approx(-0.41112325, abs=1e-7)


def test_ileri_bas_yil_basi_degilse_ilk_tam_yil_bir_sonraki():
    # bas 2016-01-02 → ilk tam yıl 2017 → test yılları 2019-2021. 2019 ilk test yılı: önceki işlem yok → 10.01 (+%50) atılmaz.
    # Hücre 2: 10.01 (+%50) ve 02.03 (+%3); 2020 hücre 3 (−%50); 2021 nakit. Net: 1,5·1,03·0,5 − 1 = −0,2275; işlem 3.
    r = ts.ileri(
        hucre_tablolari(),
        (2, 2),
        pd.Timestamp("2016-01-02"),
        pd.Timestamp("2021-12-31"),
    )
    assert [(y["yil"], y["hucre"]) for y in r["yillar"]] == [
        (2019, 2),
        (2020, 3),
        (2021, None),
    ]
    assert r["islem"] == 3
    assert r["net"] == pytest.approx(-0.2275, abs=1e-7)


def test_ema_uctan_uca_tek_hisse_tek_hucre(tmp_path):
    # A: giriş 03.02 AOF 104, çıkış 04.02 kapanış 110 (veri sonu). Getiri = 110·0,999/(104·1,001) − 1 = 0,0555790.
    # Al-tut: ilk geçerli AOF 02.02 = 103 → 110: 110·0,999/(103·1,001) − 1 = 0,0658274. Strateji al-tutu geçemez.
    # Özkaynak (dönem 02.02, 03.02, 04.02): 1,0; 1/1,001 = 0,999001; 0,999001·(110/104)·0,999 = 1,055579.
    # En büyük düşüş = 1/1,001 − 1 = −0,000999. Tutma 1 gün; maruziyet 1/3 (yalnız 03.02 kapanışı pozisyonda).
    # Sinyalden sonraki 1 gün (TASARIM 5.14: sinyal günü kapanışından k gün sonraki kapanışa): kapanış(03.02) / kapanış(sinyal
    # günü 02.02) − 1 = 104/103 − 1 = 0,0097087; 3 ve 5 gün: satır yok.
    # B düz 100: sinyal yok → net 0,0 → para çıkmaz; al-tut 0,999/1,001 − 1 = −0,001998.
    kayit._yaz(
        {
            "tur": "durum",
            "olay": "durum",
            "tarih": "2026-10-01T00:00:00+00:00",
            "kosu_id": "K1",
            "kural_id": "x",
            "aile": "ema_sikismasi",
            "durum": "Deneme",
            "genel": "Geçmedi",
            "holm_p": 0.5,
            "holm_m": 2,
            "varsayimsal": False,
            "resmi": True,
            "olcutler": [[1, "Geçti"], [2, "Geçmedi"]],
        }
    )
    kayit._yaz(
        {
            "tur": "durum",
            "olay": "durum",
            "aile": "ema_sikismasi",
            "resmi": False,
            "durum": "Kâğıt",
        }
    )
    anlik = ema_anlik(tmp_path)
    mesajlar = []
    s = ts.calistir(
        anlik,
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=P,
        bas=BAS,
        ilerleme=mesajlar.append,
        izgara=IZGARA,
    )
    assert s["masraf"] == 0.001 and s["anlik"] == anlik.kimlik
    assert s["makine"]["isci"] == 1
    assert re.fullmatch(r"\d{8}T\d{6}-[0-9a-f]{6}", s["kosu_id"])
    assert s["ek_kontrol"] == {
        "ema_sikismasi": {
            "aile": "ema_sikismasi",
            "genel": "Geçmedi",
            "durum": "Deneme",
            "holm_p": 0.5,
            "olcutler": [[1, "Geçti"], [2, "Geçmedi"]],
            "kosu_id": "K1",
        }
    }
    f = s["aileler"]["ema_sikismasi"]
    assert f["eksenler"] == EMA_IZGARA and f["atlanan"] == []
    assert [h["hisse"] for h in f["hisseler"]] == ["A", "B"]
    assert f["ozet"] == {
        "toplam": 2,
        "saglam_bolge_var": 1,
        "saglam_bolge_yok": 0,
        "para_cikmaz": 1,
        "altut_gecen": 0,
    }
    a = hisse(s, "ema_sikismasi", "A")
    assert a["net"] == [0.055579] and a["saglam"] == [True]
    assert (a["secilen"], a["en_iyi"], a["durum"]) == (0, 0, "saglam_bolge_var")
    assert a["etiket"] == "Sağlam bölge var: 1 ayar kârlı ve komşuları da kârlı."
    assert a["al_tut"] == pytest.approx(0.0658274, abs=1e-7)
    assert a["altut_gecti"] is False
    assert a["ileri"] == {"net": 0.0, "islem": 0, "yillar": []}
    o = a["olcu"]
    assert o["hucre"] == {"esik": 0.005, "min_gun": 3, "pencere": 3}
    assert o["secildi"] is True
    assert (o["islem"], o["kazanan"], o["kaybeden"], o["kazanma"]) == (1, 1, 0, 1.0)
    assert o["net"] == pytest.approx(0.0555790, abs=1e-7)
    assert o["fark"] == pytest.approx(-0.0102483, abs=1e-7)  # 0,0555790 − 0,0658274
    assert o["max_dd"] == pytest.approx(-0.000999, abs=1e-6)
    assert o["ort_tutma"] == pytest.approx(1.0)
    assert o["maruziyet"] == pytest.approx(1 / 3)
    assert o["kar_carpani"] is None
    assert o["ileri_1"] == pytest.approx(0.0097087, abs=1e-7) and o["ileri_3"] is None
    assert o["ileri_5"] is None
    assert "şüpheli: aşırı uyum" in o["bayraklar"] and "az işlem" in o["bayraklar"]
    assert a["bayraklar"] == o["bayraklar"]
    b = hisse(s, "ema_sikismasi", "B")
    assert b["net"] == [0.0] and b["saglam"] == [False] and b["secilen"] is None
    assert (b["en_iyi"], b["durum"]) == (0, "para_cikmaz")
    # Net tam 0,0 (işlem yok, başa baş): TASARIM "en iyi ≤ 0" başa başı da kapsar; etiket "zararda" demez.
    assert b["etiket"] == "Para çıkmaz: en iyi ayar bile kâr etmiyor."
    assert b["olcu"]["secildi"] is False and b["olcu"]["islem"] == 0
    assert b["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert b["altut_gecti"] is True
    assert mesajlar[-1].startswith("2/2 iş")


def test_hisse_siniri_ilk_n_hisse_ada_gore(tmp_path):
    s = ts.calistir(
        ema_anlik(tmp_path),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        hisse=1,
        p=P,
        bas=BAS,
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    assert [h["hisse"] for h in s["aileler"]["ema_sikismasi"]["hisseler"]] == ["A"]


def test_cift_uctan_uca_bir_gecis(tmp_path):
    # Dönem başı: Y ve X'in ikisinin de kapanışı olan 252. satır (dizin 251); satır 269 son. A (Y) 255-261. günler 95.
    # log(A/B) pencere 5: 255. gün [0,0,0,0,a] z = −1,7889 (önceki z yok → ΔZ yok); 256. gün [0,0,0,a,a] z = −1,0954,
    # ΔZ = +0,69 > 0 → hedef A (eşik 1,0). 262. gün s: a → 0; 263. gün [a,a,a,0,0] z = +1,0954, ΔZ = −0,69 < 0 → hedef B.
    # Eşik 1,5: |z| en çok 1,7889 ama ΔZ yok / z < eşik → sinyal yok.
    # Hedef gününden sonraki gün AOF'unda: 257. gün A'yı 95'ten al; 264. gün A'yı 100'den sat, B'yi 100'den al; son kapanış 100.
    # r_A = 100·0,999/(95·1,001) − 1 = 0,0505284; r_B = 100·0,999/(100·1,001) − 1 = −0,0019980.
    # Net = 1,0505284·0,998002 − 1 = 0,0484295. Tutma (A) 264−257 = 7, (B) 269−264 = 5 → ortalama 6.
    # Maruziyet: A 257-263 (7 gün) + B 264-268 (5 gün) = 12 gün / dönem 251-269 = 19 gün. Kâr çarpanı 0,0505284/0,001998 = 25,2895.
    # En büyük düşüş: tepe 263. gün (1/1,001)·(100/95); 264. gün ·0,999/1,001; 269. gün ·0,999 → 0,998002·0,999 − 1 = −0,002996.
    # Al-tut 50/50, ilk AOF 100 → son kapanış 100: 0,999/1,001 − 1 = −0,001998. Hücre (5; 1,0) kârlı ama komşusu (5; 1,5) 0,0.
    sektor = {"A": "X", "B": "X", "C": "Y"}
    s = ts.calistir(
        cift_anlik(tmp_path),
        sektor,
        aileler=("cift_rotasyonu",),
        isci=1,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    f = s["aileler"]["cift_rotasyonu"]
    assert f["eksenler"] == CIFT_IZGARA and f["atlanan"] == []
    assert [h["hisse"] for h in f["hisseler"]] == ["A-B"]  # C başka sektör
    assert f["ozet"] == {
        "toplam": 1,
        "saglam_bolge_var": 0,
        "saglam_bolge_yok": 1,
        "para_cikmaz": 0,
        "altut_gecen": 0,
    }
    h = f["hisseler"][0]
    assert h["sektor"] == "X"
    assert h["net"] == [0.048429, 0.0] and h["saglam"] == [False, False]
    assert (h["secilen"], h["en_iyi"], h["durum"]) == (None, 0, "saglam_bolge_yok")
    # Komşu hücre net tam 0,0: "kâr etmeyen" (TASARIM sağlamlık şartı: komşu net > 0 olmalı).
    assert (
        h["etiket"]
        == "Sağlam bölge yok: kârlı ayarın yanında kâr etmeyen ayar var (tuzak)."
    )
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert h["altut_gecti"] is True
    assert h["ileri"] == {"net": 0.0, "islem": 0, "yillar": []}
    o = h["olcu"]
    assert o["hucre"] == {"z_pencere": 5, "z_esik": 1.0} and o["secildi"] is False
    assert (o["islem"], o["kazanan"], o["kaybeden"], o["kazanma"]) == (2, 1, 1, 0.5)
    assert o["net"] == pytest.approx(0.0484295, abs=1e-7)
    assert o["fark"] == pytest.approx(0.0504275, abs=1e-7)  # 0,0484295 + 0,0019980
    assert o["kar_carpani"] == pytest.approx(25.2895, abs=1e-3)
    assert o["ort_tutma"] == pytest.approx(6.0)
    assert o["maruziyet"] == pytest.approx(12 / 19)
    assert o["max_dd"] == pytest.approx(-0.002996, abs=1e-6)
    assert o["bayraklar"] == ["az işlem"]


TEK_HUCRE = {"cift_rotasyonu": {"z_pencere": [5], "z_esik": [1.0]}}
SEKTOR_ABC = {"A": "X", "B": "X", "C": "Y"}


def tek_hucreli_cift(tmp_path, a_satir):
    s = ts.calistir(
        cift_anlik(tmp_path, a_satir),
        SEKTOR_ABC,
        aileler=("cift_rotasyonu",),
        isci=1,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )
    return hisse(s, "cift_rotasyonu", "A-B")


def test_cift_kilit_gecisi_engeller_sinyal_tasinmaz(tmp_path):
    # Hedef günleri test_cift_uctan_uca_bir_gecis ile aynı: 256. gün hedef A, 263. gün hedef B (Z düzeltilmiş kapanıştan).
    # A'nın ham serisinde 257. gün 95'in %10 üstüne (104,5; fiyat adımı 0,1 → 104,5 ≥ 104,4) çıkar: tavan kilidi, A'nın
    # düzeltilmiş AOF'u 95 kalır. 257. gün geçiş yapılmaz; sinyal ertesi güne taşınmaz (258. günün hedefi 0) → A hiç alınmaz.
    # 264. gün B'ye geçiş açık: B 100'den alınır, son kapanış 100: tek işlem, getiri 100·0,999/(100·1,001) − 1 = −0,001998.
    # Tutma 269 − 264 = 5; maruziyet 5/19 (264-268 / dönem 251-269). Net ≤ 0 → para çıkmaz.
    kilit = {
        "ham_kapanis": 104.5,
        "ham_aof": 104.5,
        "ham_yuksek": 104.5,
        "ham_dusuk": 104.5,
    }
    h = tek_hucreli_cift(tmp_path, {257: kilit})
    o = h["olcu"]
    assert h["durum"] == "para_cikmaz" and o["islem"] == 1
    assert o["net"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["ort_tutma"] == pytest.approx(5.0)
    assert o["maruziyet"] == pytest.approx(5 / 19)


def test_cift_karantina_son_temiz_aofta_cikar_pencere_boyunca_girmez(tmp_path):
    # Kilitsiz seri: 257. gün A 95'ten alınır. 260. gün A'nın AOF'u 90 (düşük 95'in altında → satır bozuk → karantina).
    # Çıkış son temiz AOF'ta: 259. gün AOF 95 (karantina günü AOF'u 90 değil): getiri 95·0,999/(95·1,001) − 1 = −0,001998.
    # 263. gün hedef B'nin 264. gün geçişi karantina penceresinde (250 satır) olduğu için yapılmaz; veri sonuna dek nakit.
    # Tek işlem; tutma 260 − 257 = 3; maruziyet 3/19 (257-259 / dönem 251-269).
    h = tek_hucreli_cift(tmp_path, {260: {"aof": 90.0, "ham_aof": 90.0}})
    o = h["olcu"]
    assert h["durum"] == "para_cikmaz" and o["islem"] == 1
    assert o["net"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["ort_tutma"] == pytest.approx(3.0)
    assert o["maruziyet"] == pytest.approx(3 / 19)


def test_cift_donem_basi_iki_bacagin_kapanisi_ve_aofu_olan_gun(tmp_path):
    # `bas` 260. gün; A'nın 260. günü satırı yok (B'nin var). Dönem başı: 260 ve 252. ortak kapanış günü (251) içinden geç
    # olanından sonraki, iki bacağın da kapanışı ve AOF'u olan ilk gün = 261. gün. Z pencere 5'te 260-264. günlerde NaN
    # olduğundan hedef yok → işlem yok, net 0,0. Al-tut 50/50, 261. gün AOF'u A 95, B 100; son kapanış 100:
    # r_A = 100·0,999/(95·1,001) − 1 = 0,0505284; r_B = 100·0,999/(100·1,001) − 1 = −0,0019980; ortalama 0,0242652.
    # Fark = 0 − 0,0242652. (260. günün AOF'u olmadığından eski kural NaN verirdi.)
    s = ts.calistir(
        cift_anlik(tmp_path, {260: None}),
        SEKTOR_ABC,
        aileler=("cift_rotasyonu",),
        isci=1,
        bas=str(GUNLER[260].date()),
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )
    h = hisse(s, "cift_rotasyonu", "A-B")
    assert h["al_tut"] == pytest.approx(0.0242652, abs=1e-7)
    assert h["olcu"]["islem"] == 0 and h["olcu"]["net"] == 0.0
    assert h["olcu"]["fark"] == pytest.approx(-0.0242652, abs=1e-7)


def test_sonraki_hissenin_kendi_kapanisi_olan_gunler_sayilir(tmp_path):
    # A: sinyal günü 02.02 kapanış 103; sonraki kapanışlar 03.02 104, 04.02 yok (satır yok), 05.02 110, 06.02 111.
    # k işlem günü = hissenin kapanışı olan k gün: 1. gün 104, 3. gün 111 (eksik gün sayılmaz).
    # ileri_1 = 104/103 − 1 = 0,0097087; ileri_3 = 111/103 − 1 = 0,0776699; 5. gün yok.
    gun = list(pd.bdate_range("2026-01-26", periods=10))
    kap = [100.0] * 5 + [103.0, 104.0, None, 110.0, 111.0]
    yuk = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, None, 110.5, 111.5]
    a = [
        mum(g, k, y, k - 0.5, 1e9)
        for g, k, y in zip(gun, kap, yuk, strict=True)
        if k is not None
    ]
    s = ts.calistir(
        ema_anlik(tmp_path, duz(1e9, adet=10), a),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=P,
        bas=BAS,
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    o = hisse(s, "ema_sikismasi", "A")["olcu"]
    assert o["islem"] == 1
    assert o["ileri_1"] == pytest.approx(0.0097087, abs=1e-7)
    assert o["ileri_3"] == pytest.approx(0.0776699, abs=1e-7)
    assert o["ileri_5"] is None


def test_sonraki_cift_alinan_bacagin_kapanisi_olan_gunler(tmp_path):
    # A'nın 258. günü satırı yok: Z 258-262. günlerde NaN, 263. günün hedefi yok; yalnız 256. gün hedefi A (257. gün alım).
    # A'nın sinyal günü (256) sonrası kapanışları: 257: 95, 259: 95, 260: 95, 261: 95, 262: 100 (258 sayılmaz).
    # ileri_1 = 95/95 − 1 = 0; ileri_3 (260. gün) = 0; ileri_5 (262. gün) = 100/95 − 1 = 0,0526316.
    h = tek_hucreli_cift(tmp_path, {258: None})
    o = h["olcu"]
    assert o["islem"] == 1
    assert o["ileri_1"] == pytest.approx(0.0) and o["ileri_3"] == pytest.approx(0.0)
    assert o["ileri_5"] == pytest.approx(0.0526316, abs=1e-7)


def ema_tek(tmp_path, a, p=P):
    s = ts.calistir(
        ema_anlik(tmp_path, a=a),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=p,
        bas=BAS,
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    return s["aileler"]["ema_sikismasi"]


def test_ema_son_satir_karantina_nan_kapanis_cikis_donemde(tmp_path):
    # seri_a() ama son satırın (04.02) düzeltilmiş kapanışı NaN: satır bozuk → karantina. Giriş 03.02 AOF 104; karantina
    # çıkışı 04.02 günü, son temiz AOF 104'te: getiri 104·0,999/(104·1,001) − 1 = −0,001998. Son geçerli kapanış 03.02 (104).
    # Dönem satırları 02.02, 03.02, 04.02 (kapanış ileri doldurulur): özkaynak 1,0; 1/1,001 = 0,999001; ·0,999 = 0,998002.
    # En büyük düşüş −0,001998; tutma 1; maruziyet 1/3. Al-tut 02.02 AOF 103'ten son geçerli kapanış 104'e:
    # 104·0,999/(103·1,001) − 1 = 0,0076913; fark = −0,001998 − 0,0076913 = −0,0096893.
    a = seri_a()
    a[7]["kapanis"] = float("nan")
    f = ema_tek(tmp_path, a)
    h = f["hisseler"][0]
    o = h["olcu"]
    assert f["atlanan"] == [] and h["hisse"] == "A" and o["islem"] == 1
    assert o["net"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["max_dd"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["ort_tutma"] == pytest.approx(1.0) and o["maruziyet"] == pytest.approx(
        1 / 3
    )
    assert h["al_tut"] == pytest.approx(0.0076913, abs=1e-7)
    assert o["fark"] == pytest.approx(-0.0096893, abs=1e-7)


def test_ema_aofu_olmayan_hisse_atlanir_tek_gunluk_donem_calisir(tmp_path):
    # Isınma 8 gün: dönem başı 8. satır (04.02). A'nın o satırında AOF yok → dönem başından itibaren AOF yok → A sınanmaz
    # ve `atlanan` listesindedir. B (düz 100): dönem tek gün; işlem yok (sinyalden sonra gün yok), net 0,0; tek özkaynak
    # değeri 1,0: Sharpe ve Calmar yok, maruziyet 0/1 = 0,0. Al-tut 100'den 100'e: 0,999/1,001 − 1 = −0,001998;
    # Fark: strateji 0,0 eksi al-tut (−0,001998) = +0,001998.
    a = seri_a()
    a[7]["aof"] = a[7]["ham_aof"] = float("nan")
    f = ema_tek(tmp_path, a, dataclasses.replace(P, isinma=8))
    assert f["atlanan"] == ["A"] and [h["hisse"] for h in f["hisseler"]] == ["B"]
    h = f["hisseler"][0]
    o = h["olcu"]
    assert (o["islem"], o["net"], o["maruziyet"]) == (0, 0.0, 0.0)
    assert o["sharpe"] is None and o["calmar"] is None
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["fark"] == pytest.approx(0.001998, abs=1e-6)


def test_cift_tam_252_ortak_gun_tek_gunluk_donem_sinanir(tmp_path):
    # A ve B 252 satır, ikisi de sabit 100: 252. ortak gün son gün; dönem başı = dönem sonu (tek gün). İşlem yok, net 0,0;
    # maruziyet 0,0, Sharpe ve Calmar yok. Al-tut 50/50: 100'den 100'e: 0,999/1,001 − 1 = −0,001998; fark +0,001998.
    sabit = [mum(g, 100.0) for g in GUNLER[:252]]
    s = ts.calistir(
        anlik_hazirla(tmp_path, {"A": sabit, "B": sabit}),
        {"A": "X", "B": "X"},
        aileler=("cift_rotasyonu",),
        isci=1,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )
    f = s["aileler"]["cift_rotasyonu"]
    assert f["atlanan"] == [] and [h["hisse"] for h in f["hisseler"]] == ["A-B"]
    h = f["hisseler"][0]
    o = h["olcu"]
    assert (o["islem"], o["net"], o["maruziyet"]) == (0, 0.0, 0.0)
    assert o["sharpe"] is None and o["calmar"] is None
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["fark"] == pytest.approx(0.001998, abs=1e-6)


def test_cift_donem_basi_veri_sonundan_sonra_ise_atlanir(tmp_path):
    # `bas` 269. gün; A'nın o günü satırı yok (son geçerli kapanışı 268) → iki bacağın da kapanışı ve AOF'u olan gün yok.
    s = ts.calistir(
        cift_anlik(tmp_path, {269: None}),
        SEKTOR_ABC,
        aileler=("cift_rotasyonu",),
        isci=1,
        bas=str(GUNLER[269].date()),
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )
    f = s["aileler"]["cift_rotasyonu"]
    assert f["atlanan"] == ["A-B"] and f["hisseler"] == []


def test_cift_alinan_bacagin_son_gun_kapanisi_yoksa_onceki_kapanisla_cikar(tmp_path):
    # A'nın 262. ve 268. günü satırı yok; B 269 satır (son 268). Z 262-266'da NaN → 263. gün hedefi yok, geçiş yok: A 257.
    # günde 95'ten alınır ve tutulur. Veri sonu 268 (iki bacağın son kapanışlarının küçüğü); A'nın o günü satırı yok →
    # kapanış ileri doldurulur: 267. gün 100. Çıkış 268. gün 100'den: 100·0,999/(95·1,001) − 1 = 0,0505284.
    # Tutma 268 − 257 = 11; maruziyet 11 gün (257-267) / dönem 251-268 = 18 gün.
    kayit_ = {262: None, 268: None}
    s = ts.calistir(
        cift_anlik(tmp_path, kayit_, b_gun=269),
        SEKTOR_ABC,
        aileler=("cift_rotasyonu",),
        isci=1,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )
    h = hisse(s, "cift_rotasyonu", "A-B")
    o = h["olcu"]
    assert o["islem"] == 1 and o["net"] == pytest.approx(0.0505284, abs=1e-7)
    assert o["ort_tutma"] == pytest.approx(11.0)
    assert o["maruziyet"] == pytest.approx(11 / 18)


def cift_calistir(anlik, bas="2015-12-01"):
    return ts.calistir(
        anlik,
        SEKTOR_ABC,
        aileler=("cift_rotasyonu",),
        isci=1,
        bas=bas,
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )


def donem(bas, son):
    return {"bas": str(GUNLER[bas].date()), "son": str(GUNLER[son].date())}


def test_cift_son_satir_karantina_karantina_cikisi_veri_sonu_degil(tmp_path):
    # TASARIM 5.14, dönemin son günü: çiftte dönemin son günü iki bacağın son satırlarının erken olanıdır; fiyatı
    # geçerli olmak zorunda değildir. A'nın 262. günü satırı yok (Z 262-266 NaN, 263. gün geçişi yok): A 257. günde
    # 95'ten alınır ve tutulur. 268. gün A temiz: AOF 99 (düşük 99 ≤ AOF ≤ yüksek 100). 269. gün (A ve B'nin son satırı) A'nın
    # düzeltilmiş kapanışı NaN → satır bozuk → karantina. Açık pozisyon 269. gün karantina kuralıyla son temiz AOF'tan
    # (268. gün, 99) çıkar; "veri sonu" çıkışı (268. gün kapanış 100) olmaz.
    # Getiri = 99·0,999/(95·1,001) − 1 = 98,901/95,095 − 1 = 0,0400231. Tutma 269 − 257 = 12.
    # Maruziyet: 257-268 = 12 gün / dönem 251-269 = 19 gün.
    temiz_99 = {"aof": 99.0, "ham_aof": 99.0, "dusuk": 99.0, "ham_dusuk": 99.0}
    s = cift_calistir(
        cift_anlik(tmp_path, {262: None, 268: temiz_99, 269: {"kapanis": float("nan")}})
    )
    h = hisse(s, "cift_rotasyonu", "A-B")
    o = h["olcu"]
    assert o["islem"] == 1 and o["net"] == pytest.approx(0.0400231, abs=1e-7)
    assert o["ort_tutma"] == pytest.approx(12.0)
    assert o["maruziyet"] == pytest.approx(12 / 19)
    assert h["donem"] == donem(251, 269)


def test_ema_ileri_son_yil_donemin_son_gunu(tmp_path):
    # Düz 100 kapanışlı seri, 2023-01-02 .. 2026-01-01 (iş günleri). Isınma 4 kapanış günü (P): dönem başı 4. gün =
    # 2023-01-05 (Pzt 02, Sal 03, Çar 04, Per 05). 1 Ocak değil → ilk tam takvim yılı 2024; + 2 eğitim yılı → ilk test yılı 2026.
    # A'nın son satırının (2026-01-01) kapanışı NaN → karantina; dönemin son günü yine 2026-01-01 → son test yılı 2026.
    # Kontrol B: aynı günler, son kapanış geçerli → son test yılı 2026. İşlem yok → sağlam bölge yok → yıl nakit (hücre None).
    gun = pd.bdate_range("2023-01-02", "2026-01-01")
    a = [mum(g, 100.0) for g in gun]
    a[-1]["kapanis"] = float("nan")
    b = [mum(g, 100.0) for g in gun]
    s = ts.calistir(
        anlik_hazirla(tmp_path, {"A": a, "B": b}),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=P,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    for ad in ("B", "A"):
        h = hisse(s, "ema_sikismasi", ad)
        assert h["ileri"]["yillar"] == [{"yil": 2026, "hucre": None}], ad
        assert h["donem"] == {"bas": "2023-01-05", "son": "2026-01-01"}, ad


def test_ema_al_tut_donem_basi_aof_sifir_sonraki_gecerli_gun(tmp_path):
    # seri_a() ama dönem başı satırının (02.02) AOF'u 0 → satır bozuk → karantina → geçerli fiyat günü değil (AOF > 0 şartı).
    # Dönem başı sonraki geçerli fiyat günü 03.02 (AOF 104); son gün 04.02, son kapanış 110. Sinyal günü 02.02 dönem
    # başından önce → işlem yok, net 0,0, maruziyet 0,0.
    # Al-tut: 03.02 AOF 104'ten 110'a: 110·0,999/(104·1,001) − 1 = 109,89/104,104 − 1 = 0,0555790.
    a = seri_a()
    a[5]["aof"] = a[5]["ham_aof"] = 0.0
    h = ema_tek(tmp_path, a)["hisseler"][0]
    o = h["olcu"]
    assert h["hisse"] == "A" and h["al_tut"] == pytest.approx(0.0555790, abs=1e-7)
    assert h["donem"] == {"bas": "2026-02-03", "son": "2026-02-04"}
    assert (o["islem"], o["net"], o["maruziyet"]) == (0, 0.0, 0.0)


def test_ema_al_tut_son_kapanis_sonsuz_son_gecerli_kapanis(tmp_path):
    # seri_a() ama son satırın (04.02) kapanışı (ham dahil) sonsuz → ham kapanış > ham yüksek → bozuk → karantina.
    # Giriş 03.02 AOF 104; 04.02 karantina çıkışı son temiz AOF 104'te: 104·0,999/(104·1,001) − 1 = −0,001998.
    # Al-tut: dönem başı 02.02 AOF 103; son geçerli kapanış 03.02 = 104: 104·0,999/(103·1,001) − 1 = 0,0076913
    # (sonsuz kapanış yok sayılır). Fark = −0,001998 − 0,0076913 = −0,0096893. Çıktıda sonsuz ya da NaN yok.
    a = seri_a()
    a[7]["kapanis"] = a[7]["ham_kapanis"] = float("inf")
    f = ema_tek(tmp_path, a)
    h = f["hisseler"][0]
    o = h["olcu"]
    assert h["hisse"] == "A" and o["islem"] == 1
    assert h["al_tut"] == pytest.approx(0.0076913, abs=1e-7)
    assert o["net"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["fark"] == pytest.approx(-0.0096893, abs=1e-7)
    assert h["donem"] == {"bas": "2026-02-02", "son": "2026-02-04"}
    json.dumps(f, allow_nan=False)


def test_ema_donem_basi_sifir_aof_tek_gun_atlanir(tmp_path):
    # Isınma 8 gün: dönem başı 8. satır (04.02), dönemin son günü de o. A'nın o satırında AOF 0 → geçerli fiyat günü yok →
    # dönem başı dönemin son gününe dek bulunmaz → A sınanmaz ve `atlanan` listesindedir (AOF'u NaN olan durumun sıfır eşi).
    a = seri_a()
    a[7]["aof"] = a[7]["ham_aof"] = 0.0
    f = ema_tek(tmp_path, a, dataclasses.replace(P, isinma=8))
    assert f["atlanan"] == ["A"] and [h["hisse"] for h in f["hisseler"]] == ["B"]


def test_sonraki_gecersiz_gun_sayilmaz(tmp_path):
    # A: sinyal günü 02.02 kapanış 103; sonraki satırlar 03.02 104, 04.02 kapanış 0 (ham dahil → bozuk → karantina),
    # 05.02 110, 06.02 111. 04.02 geçerli fiyat günü değil, sayılmaz: 1. gün 104, 2. gün 110, 3. gün 111.
    # Giriş 03.02 AOF 104; 04.02 karantina çıkışı (1 işlem). ileri_1 = 104/103 − 1 = 0,0097087;
    # ileri_3 = 111/103 − 1 = 0,0776699 (0'lı gün sayılsaydı 110/103 − 1 = 0,0679612); 5. gün yok.
    gun = list(pd.bdate_range("2026-01-26", periods=10))
    kap = [100.0] * 5 + [103.0, 104.0, 105.0, 110.0, 111.0]
    yuk = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5, 110.5, 111.5]
    a = [mum(g, k, y, k - 0.5, 1e9) for g, k, y in zip(gun, kap, yuk, strict=True)]
    a[7].update(kapanis=0.0, ham_kapanis=0.0)
    s = ts.calistir(
        ema_anlik(tmp_path, duz(1e9, adet=10), a),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=P,
        bas=BAS,
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    o = hisse(s, "ema_sikismasi", "A")["olcu"]
    assert o["islem"] == 1
    assert o["ileri_1"] == pytest.approx(0.0097087, abs=1e-7)
    assert o["ileri_3"] == pytest.approx(0.0776699, abs=1e-7)
    assert o["ileri_5"] is None


def test_cift_sonsuz_son_kapanis_son_gecerli_fiyat_ve_karantina_cikisi(tmp_path):
    # B'nin son satırının (269) kapanışı (ham dahil) sonsuz → ham kapanış > ham yüksek → bozuk → karantina. Dönem son günü 269.
    # Hedef günleri test_cift_uctan_uca_bir_gecis ile aynı: 257. gün A 95'ten, 264. gün B 100'den alınır. B'yi 269. gün karantina
    # kuralıyla son temiz AOF'tan (268. gün, 100) çıkar; "veri sonu" çıkışı (sonsuz kapanış) olmaz.
    # r_A = 100·0,999/(95·1,001) − 1 = 0,0505284; r_B = 100·0,999/(100·1,001) − 1 = −0,0019980; net = 1,0505284·0,998002 − 1 = 0,0484295.
    # Tutma (A) 264−257 = 7, (B) 269−264 = 5 → ortalama 6; maruziyet 12 gün / dönem 251-269 = 19 gün.
    # Al-tut 50/50: A son geçerli kapanış 100 (269. gün), B 100 (268. gün; sonsuz yok sayılır): 0,999/1,001 − 1 = −0,001998.
    b = [mum(g, 100.0) for g in GUNLER]
    b[269].update(kapanis=float("inf"), ham_kapanis=float("inf"))
    s = cift_calistir(cift_anlik(tmp_path, ek={"B": b}))
    h = hisse(s, "cift_rotasyonu", "A-B")
    o = h["olcu"]
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["islem"] == 2 and o["net"] == pytest.approx(0.0484295, abs=1e-7)
    assert o["ort_tutma"] == pytest.approx(6.0) and o["maruziyet"] == pytest.approx(
        12 / 19
    )
    assert h["donem"] == donem(251, 269)
    sade(s)


@pytest.mark.parametrize(
    "bozuk_satir",
    [
        pytest.param({"aof": 0.0, "ham_aof": 0.0}, id="aof_sifir"),
        pytest.param(
            {
                "ham_kapanis": 110.6,
                "ham_aof": 110.6,
                "ham_yuksek": 110.6,
                "ham_dusuk": 110.6,
            },
            id="limit_asimi",
        ),
    ],
)
def test_cift_donem_basi_gecersiz_gun_sonraki_gune_kayar(tmp_path, bozuk_satir):
    # İki durumda da A'nın 251. günü (ilk aday: 252. ortak kapanış günü) karantinalı, kapanışı ve AOF'u (sıfır durumunda
    # AOF 0) vardır: AOF 0 → bozuk; ham kapanış 110,6 > 100·1,1·1,005 = 110,55 (önceki ham kapanış 100, ±%10) → limit aşımı.
    # Geçerli fiyat günü değil → dönem başı 252. gün (iki bacak geçerli: A'nın 252. günü AOF 99, düşük 99, kapanış 100).
    # Karantina 250 satır sinyal engeller (E): işlem yok, net 0,0. Dönemin son günü 269.
    # Al-tut 50/50 252. gün AOF'undan, son geçerli kapanış 100: r_A = 100·0,999/(99·1,001) − 1 = 0,0080828;
    # r_B = 100·0,999/(100·1,001) − 1 = −0,0019980; ortalama = 0,0030424.
    temiz_99 = {"aof": 99.0, "ham_aof": 99.0, "dusuk": 99.0, "ham_dusuk": 99.0}
    s = cift_calistir(cift_anlik(tmp_path, {251: bozuk_satir, 252: temiz_99}))
    h = hisse(s, "cift_rotasyonu", "A-B")
    assert h["al_tut"] == pytest.approx(0.0030424, abs=1e-7)
    assert h["donem"] == donem(252, 269)
    assert h["olcu"]["islem"] == 0 and h["olcu"]["net"] == 0.0


def test_cift_son_gun_limit_asimi_karantina_cikisi(tmp_path):
    # Test 1 ile aynı kurulum (262. gün A'da yok: A 257. günde 95'ten alınır ve tutulur; 268. gün A temiz, AOF 99). 269. gün
    # (son satır) A'nın ham kapanışı 110,6 > 100·1,1·1,005 = 110,55 (önceki ham kapanış 100, ±%10) → limit aşımı → karantina;
    # kapanış sonlu. Düzeltilmiş kapanış 105 (yüksek 105: satır tutarlı): geçerli kapanış sayılsaydı al-tut ve veri sonu
    # çıkışı bunu okurdu. Açık pozisyon 269. gün karantina kuralıyla son temiz AOF'tan (268. gün, 99) çıkar, "veri sonu" olmaz.
    # Getiri = 99·0,999/(95·1,001) − 1 = 98,901/95,095 − 1 = 0,0400231. Tutma 269 − 257 = 12; maruziyet 12 gün (257-268) /
    # dönem 251-269 = 19 gün. Al-tut 50/50: A 251. gün AOF 100'den son geçerli kapanışa (268. gün, 100), B 100'den 100'e:
    # ikisi de 0,999/1,001 − 1 = −0,001998 (269. gün 105 okunsaydı A için 105·0,999/(100·1,001) − 1 = +0,0479).
    temiz_99 = {"aof": 99.0, "ham_aof": 99.0, "dusuk": 99.0, "ham_dusuk": 99.0}
    asim = {
        "kapanis": 105.0,
        "yuksek": 105.0,
        "ham_kapanis": 110.6,
        "ham_aof": 110.6,
        "ham_yuksek": 110.6,
        "ham_dusuk": 110.6,
    }
    s = cift_calistir(cift_anlik(tmp_path, {262: None, 268: temiz_99, 269: asim}))
    h = hisse(s, "cift_rotasyonu", "A-B")
    o = h["olcu"]
    assert o["islem"] == 1 and o["net"] == pytest.approx(0.0400231, abs=1e-7)
    assert o["ort_tutma"] == pytest.approx(12.0)
    assert o["maruziyet"] == pytest.approx(12 / 19)
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert h["donem"] == donem(251, 269)


def test_ema_son_gun_limit_asimi_karantina_cikisi(tmp_path):
    # seri_a() ama son satırın (04.02) ham alanları 116: ham kapanış 116 > 104·1,1·1,005 = 114,97 (önceki ham kapanış 104,
    # ±%10) → limit aşımı → karantina; kapanış sonlu (düzeltilmiş 110). Giriş 03.02 AOF 104; 04.02 karantina çıkışı son
    # temiz AOF 104'te (veri sonu çıkışı 110 olmaz): 104·0,999/(104·1,001) − 1 = −0,001998.
    # Al-tut: 02.02 AOF 103'ten son geçerli kapanışa (03.02, 104): 104·0,999/(103·1,001) − 1 = 0,0076913.
    a = seri_a()
    a[7].update(ham_kapanis=116.0, ham_aof=116.0, ham_yuksek=116.0, ham_dusuk=116.0)
    h = ema_tek(tmp_path, a)["hisseler"][0]
    o = h["olcu"]
    assert h["hisse"] == "A" and o["islem"] == 1
    assert o["net"] == pytest.approx(-0.001998, abs=1e-6)
    assert h["al_tut"] == pytest.approx(0.0076913, abs=1e-7)
    assert h["donem"] == {"bas": "2026-02-02", "son": "2026-02-04"}


def test_sonraki_cift_gecersiz_gun_sayilmaz(tmp_path):
    # A'nın 259, 260 ve 261. günlerinde hacim 0 (satır var, kapanış 95; işlem görmeyen gün → geçerli fiyat günü değil).
    # Z düzeltilmiş kapanıştan hesaplanır, değişmez: 256. gün hedef A (257. gün alım, 95), 263. gün hedef B. B'nin 264. günü
    # hacim 0 → geçiş yapılmaz; sonraki günlerde |z| < 1 (264. gün z = 0,73; 265. gün z = 0,45) → sinyal yok. Tek işlem: A,
    # veri sonuna dek tutulur. A'nın sinyal günü (256) sonrası geçerli kapanışları: 257: 95, 258: 95, 262: 100, 263: 100,
    # 264: 100 (259-261 sayılmaz). Sinyal günü kapanışı 95.
    # ileri_1 (257) = 95/95 − 1 = 0; ileri_3 (262) = 100/95 − 1 = 0,0526316; ileri_5 (264) = 100/95 − 1 = 0,0526316.
    # (Geçersiz günler sayılsaydı: 3. gün 259 → 0; 5. gün 261 → 0.)
    b = [mum(g, 100.0) for g in GUNLER]
    b[264]["hacim"] = 0.0
    sifir = {"hacim": 0.0}
    s = cift_calistir(
        cift_anlik(tmp_path, {259: sifir, 260: dict(sifir), 261: dict(sifir)}, {"B": b})
    )
    o = hisse(s, "cift_rotasyonu", "A-B")["olcu"]
    assert o["islem"] == 1
    assert o["ileri_1"] == pytest.approx(0.0)
    assert o["ileri_3"] == pytest.approx(0.0526316, abs=1e-7)
    assert o["ileri_5"] == pytest.approx(0.0526316, abs=1e-7)


def test_ema_sonsuz_duzeltilmis_fiyat_karantina_gunu(tmp_path):
    # seri_a() ama son satırın (04.02) düzeltilmiş AOF, kapanış, yüksek ve düşüğü sonsuz (ham alanlar aynı: veri katmanı
    # karantinaya almaz). TASARIM 5.14 uç durum 2: düzeltilmiş fiyatı sonsuz gün bu modülde karantina günüdür.
    # Giriş 03.02 AOF 104; 04.02 karantina çıkışı son temiz AOF 104'te: 104·0,999/(104·1,001) − 1 = −0,001998.
    # Tutma 1; maruziyet 1/3 (yalnız 03.02 pozisyonda; dönem 02.02-04.02). Al-tut: 02.02 AOF 103'ten son geçerli
    # kapanışa (03.02, 104): 104·0,999/(103·1,001) − 1 = 0,0076913. Çıktıda sonsuz ya da NaN yok.
    a = seri_a()
    a[7].update(aof=float("inf"), kapanis=float("inf"))
    a[7].update(yuksek=float("inf"), dusuk=float("inf"))
    f = ema_tek(tmp_path, a)
    h = f["hisseler"][0]
    o = h["olcu"]
    assert h["hisse"] == "A" and o["islem"] == 1
    assert o["net"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["ort_tutma"] == pytest.approx(1.0)
    assert o["maruziyet"] == pytest.approx(1 / 3)
    assert h["al_tut"] == pytest.approx(0.0076913, abs=1e-7)
    assert h["donem"] == {"bas": "2026-02-02", "son": "2026-02-04"}
    json.dumps(f, allow_nan=False)


def test_cift_sonsuz_duzeltilmis_fiyat_karantina_gunu(tmp_path):
    # A'nın 258. günü düzeltilmiş AOF, kapanış, yüksek ve düşük sonsuz (ham alanlar aynı) → bu modülde karantina günü.
    # 256. gün hedef A: 257. gün A 95'ten alınır. 258. gün karantina: açık pozisyon son temiz AOF'tan (257. gün, 95) çıkar:
    # 95·0,999/(95·1,001) − 1 = −0,001998; tutma 258 − 257 = 1; maruziyet 1 gün (257) / dönem 251-269 = 19 gün.
    # Sonrası: Z 258-262'de NaN, 263. günün hedefi yok, sonraki günlerde |z| < 1 → başka işlem yok (karantina ayrıca
    # 250 satır giriş açmaz). Al-tut 50/50, sonsuz gün yok sayılır: ikisi de 100'den 100'e: 0,999/1,001 − 1 = −0,001998.
    sonsuz = float("inf")
    satir = {"aof": sonsuz, "kapanis": sonsuz, "yuksek": sonsuz, "dusuk": sonsuz}
    s = cift_calistir(cift_anlik(tmp_path, {258: satir}))
    h = hisse(s, "cift_rotasyonu", "A-B")
    o = h["olcu"]
    assert o["islem"] == 1 and o["net"] == pytest.approx(-0.001998, abs=1e-6)
    assert o["ort_tutma"] == pytest.approx(1.0)
    assert o["maruziyet"] == pytest.approx(1 / 19)
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert h["donem"] == donem(251, 269)
    sade(s)


@pytest.mark.parametrize(
    "sonsuz, girisler",
    [(False, [256, 266]), (True, [266])],
    ids=["temiz", "sonsuz"],
)
def test_ema_sonsuz_duzeltilmis_fiyat_giris_engeli_250_satir(
    tmp_path, sonsuz, girisler
):
    # TASARIM 5.14: 14. dizindeki sonsuz fiyat 14-263 aralığında giriş açtırmaz.
    # Temiz seride 255 ve 265 sinyalleri ertesi gün giriş açar; engel yalnız ilkini önler.
    a = duz(1e9, adet=270)
    # İlk örüntü sonsuz yükseği içeren sıkışmayı sınama döneminden önce bitirir.
    for bas in (30, 250, 260):
        for i, satir in enumerate(seri_a(), start=bas):
            a[i] = {**satir, "tarih": a[i]["tarih"]}
    if sonsuz:
        a[14].update(dict.fromkeys(("aof", "kapanis", "yuksek", "dusuk"), float("inf")))
    m = motor.mumlar(ema_anlik(tmp_path, a=a), "A", P)
    assert not m["karantina"].iloc[14]  # Ham fiyatlar temiz: veri katmanı engellemez.
    sinyaller = aileler.sinyal(m, P)
    assert sinyaller[sinyaller >= m.index[250]].tolist() == m.index[[255, 265]].tolist()
    tablolar = ts.ema_tablolari(m, P, EMA_IZGARA, m.index[250])
    assert tablolar[0]["giris_tarih"].tolist() == m.index[girisler].tolist()


@pytest.mark.parametrize(
    "sonsuz, girisler",
    [(False, [257, 264]), (True, [264])],
    ids=["temiz", "sonsuz"],
)
def test_cift_sonsuz_duzeltilmis_fiyat_giris_engeli_250_satir(
    tmp_path, sonsuz, girisler
):
    # TASARIM 5.14: 14. dizindeki sonsuz fiyat 14-263 aralığında giriş açtırmaz.
    # 257. gün A girişi engellenir; 264. gün B girişi engelden sonraki ilk satırdadır.
    satir = dict.fromkeys(("aof", "kapanis", "yuksek", "dusuk"), float("inf"))
    anlik = cift_anlik(tmp_path, {14: satir} if sonsuz else None)
    isler, atlanan = ts.cift_isleri(
        anlik, {"A": "X", "B": "X"}, ["A", "B"], "2015-12-01", CIFT_IZGARA
    )
    assert atlanan == []
    _, _, y, x, _, gunler, C, A, F, bas_k, izgara = isler[0]
    assert not F["Kar"][14].any()  # Ham fiyatlar temiz: veri katmanı engellemez.
    tablolar, _, _ = ts.cift_tablolari(y, x, gunler, C, A, F, bas_k, izgara)
    assert tablolar[0]["giris_tarih"].tolist() == gunler[girisler].tolist()


def test_cift_tek_gunluk_donem_gecersiz_fiyat_atlanir(tmp_path):
    # A ve B 252 satır: tek aday gün 252. (dizin 251). A'nın o günü AOF'u 0 → bozuk → geçerli fiyat günü değil →
    # dönemin son gününe dek dönem başı bulunmaz → çift sınanmaz, `atlanan` listesinde.
    a = [mum(g, 100.0) for g in GUNLER[:252]]
    a[251].update(aof=0.0, ham_aof=0.0)
    b = [mum(g, 100.0) for g in GUNLER[:252]]
    s = ts.calistir(
        anlik_hazirla(tmp_path, {"A": a, "B": b}),
        {"A": "X", "B": "X"},
        aileler=("cift_rotasyonu",),
        isci=1,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )
    f = s["aileler"]["cift_rotasyonu"]
    assert f["atlanan"] == ["A-B"] and f["hisseler"] == []


def test_cift_tek_gunluk_donem_donem_alani(tmp_path):
    # A ve B 252 satır, ikisi de sabit 100: dönem başı = dönemin son günü = 252. gün (dizin 251). `donem` alanı iki ucu da
    # aynı günü yazar. İşlem yok; al-tut aynı günün AOF'undan alıp kapanışından satar: 0,999/1,001 − 1 = −0,001998.
    sabit = [mum(g, 100.0) for g in GUNLER[:252]]
    s = ts.calistir(
        anlik_hazirla(tmp_path, {"A": sabit, "B": sabit}),
        {"A": "X", "B": "X"},
        aileler=("cift_rotasyonu",),
        isci=1,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=TEK_HUCRE,
    )
    h = hisse(s, "cift_rotasyonu", "A-B")
    assert h["donem"] == donem(251, 251)
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)


def test_atlanan_isinmasi_dolmayan_hisse_ve_kisa_cift(tmp_path):
    # EMA: isınma 6 gün; A 8 satır sınanır, B 5 satır (< 6) sınanmaz ve adı `atlanan` listesindedir.
    s = ts.calistir(
        ema_anlik(tmp_path / "e", duz(1e9, adet=5)),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=dataclasses.replace(P, isinma=6),
        bas=BAS,
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    f = s["aileler"]["ema_sikismasi"]
    assert f["atlanan"] == ["B"]
    assert [h["hisse"] for h in f["hisseler"]] == ["A"] and f["ozet"]["toplam"] == 1
    # Çift: D yalnız 100 gün (< 252 ortak gün): A-D ve B-D sınanmaz, A-B sınanır.
    d = [mum(g, 100.0) for g in GUNLER[:100]]
    s = ts.calistir(
        cift_anlik(tmp_path / "c", ek={"D": d}),
        {**SEKTOR_ABC, "D": "X"},
        aileler=("cift_rotasyonu",),
        isci=1,
        bas="2015-12-01",
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    f = s["aileler"]["cift_rotasyonu"]
    assert f["atlanan"] == ["A-D", "B-D"]
    assert [h["hisse"] for h in f["hisseler"]] == ["A-B"] and f["ozet"]["toplam"] == 1


def test_yaz_m_yi_artirmaz_ve_kart_yazmaz(tmp_path):
    # Yarıda kalmış resmi koşu m'ye 2 aile sayar (TASARIM 5.11); Tansu sınaması satırı (tur=destek) m'yi değiştirmez
    # ve kart dosyası üretmez (TASARIM 5.14).
    kayit._yaz(
        {
            "tur": "deneme",
            "olay": "basladi",
            "kosu_id": "R1",
            "kural_id": "x",
            "resmi": True,
        }
    )
    assert kayit.deneme_sayisi() == 2
    s = ts.calistir(
        ema_anlik(tmp_path),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=P,
        bas=BAS,
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )
    ts.yaz(s)
    assert any(r["olay"] == "tansu_sinama" for r in kayit._oku())
    assert kayit.deneme_sayisi() == 2
    assert not list((tmp_path / "rapor").glob("kartlar-*.csv"))
    assert not (tmp_path / "kayit" / "kartlar.jsonl").exists()


def test_1_ve_2_iscide_ayni_sonuc(tmp_path):
    anlik = cift_anlik(tmp_path)
    sektor = {"A": "X", "B": "X", "C": "Y"}
    sonuclar, mesajlar = {}, {}
    for isci in (1, 2):
        mesajlar[isci] = []
        sonuclar[isci] = ts.calistir(
            anlik,
            sektor,
            isci=isci,
            p=P,
            bas="2015-12-01",
            ilerleme=mesajlar[isci].append,
            izgara=IZGARA,
        )
        assert sonuclar[isci]["makine"]["isci"] == isci
    assert sade(sonuclar[1]) == sade(sonuclar[2])
    assert sonuclar[1]["aileler"]["cift_rotasyonu"]["ozet"]["toplam"] == 1
    assert sonuclar[1]["aileler"]["ema_sikismasi"]["ozet"]["toplam"] == 3
    for mesaj in mesajlar.values():  # 3 EMA hissesi + 1 çift = 4 iş
        assert re.fullmatch(
            r"4/4 iş · geçen [\d.]+ sn · kalan ~[\d.]+ sn · CPU %[\d.]+", mesaj[-1]
        )


def test_sektor_oku_en_yeni_sektorlu_anlik_goruntu(tmp_path):
    # 02.01 ve 02.02 sektörlü; 03.01 günlük görüntü (sektor.json yok) → 02.02 okunur, adlar sıralı.
    for kimlik, sektor in (
        ("20260101-1000", {"B": "S", "A": "S"}),
        ("20260201-1000", {"B": "T", "A": "S"}),
        ("20260301-1000", None),
    ):
        klasor = tmp_path / "ag" / kimlik
        klasor.mkdir(parents=True)
        if sektor:
            (klasor / "sektor.json").write_text(json.dumps(sektor), encoding="utf-8")
    sozluk, kimlik = ts.sektor_oku(tmp_path)
    assert kimlik == "20260201-1000"
    assert sozluk == {"A": "S", "B": "T"} and list(sozluk) == ["A", "B"]


def test_komut_yardim_cikis_sifir():
    with pytest.raises(SystemExit) as e:
        komut.main(["tansu-sinama", "--help"])
    assert e.value.code == 0


def test_komut_uctan_uca_rapor_ve_gunluk_satiri(tmp_path, capsys):
    cift_anlik(tmp_path)
    assert (
        komut.main(
            [
                "tansu-sinama",
                "--kok",
                str(tmp_path),
                "--isci",
                "1",
                "--aile",
                "cift_rotasyonu",
            ]
        )
        == 0
    )
    cikti = capsys.readouterr().out
    dosyalar = list((tmp_path / "rapor").glob("tansu-sinama-*.json"))
    assert (
        len(dosyalar) == 1 and str(dosyalar[0]) in cikti and "cift_rotasyonu" in cikti
    )
    assert "atlanan 0" in cikti
    sonuc = json.loads(dosyalar[0].read_text(encoding="utf-8"))
    satir = next(s for s in kayit._oku() if s["olay"] == "tansu_sinama")
    assert dosyalar[0].name == f"tansu-sinama-{sonuc['kosu_id']}.json"
    assert (satir["tur"], satir["resmi"], satir["kosu_id"]) == (
        "destek",
        False,
        sonuc["kosu_id"],
    )
    assert satir["anlik"] == sonuc["anlik"] and re.fullmatch(
        r"[0-9a-f]{64}", satir["manifest_sha256"]
    )
    assert isinstance(satir["kirli"], bool) and "git_commit" in satir
    assert satir["makine"]["isci"] == 1 and "cift_rotasyonu" in satir["ozet"]


def test_yaz_git_hatasinda_sonuc_ve_kayit_yazmaz(tmp_path, monkeypatch):
    sonuc = ts.calistir(
        ema_anlik(tmp_path),
        {},
        aileler=("ema_sikismasi",),
        isci=1,
        p=P,
        bas=BAS,
        ilerleme=lambda m: None,
        izgara=IZGARA,
    )

    def git_hatasi():
        raise kayit.KayitHatasi("Git bilgisi doğrulanamadı.")

    monkeypatch.setattr(kayit, "_git", git_hatasi)
    with pytest.raises(kayit.KayitHatasi, match="Git"):
        ts.yaz(sonuc)
    assert not (tmp_path / "rapor").exists()
    assert not (kayit.KAYIT_DIZINI / "deneme.jsonl").exists()
