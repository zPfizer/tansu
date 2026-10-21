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


def s10_kayitli(tmp_path, monkeypatch, *, sinyal=False, limit=True, varyant="bugun"):
    """E1 sözleşme verisi; E2, E3, E4 ve E5 gerçek hesap/yazma yolundadır."""
    import datetime as dt
    from decimal import Decimal
    from hashlib import sha256
    from tansu import deneme, katalog
    from tests.test_kayit import pilot_deneme

    gunler = [
        f"{y}-{a}"
        for y in range(2021, 2026)
        for a in ("01-04", "01-05", "12-30", "12-31")
    ]
    donemler = [
        dict(
            ad=str(y),
            baslangic=dt.date(y, 1, 1),
            bitis=dt.date(y, 12, 31),
            isinma_baslangici=dt.date(2018, 1, 1),
            sinir_surumu="bagimsiz_donem_v1",
        )
        for y in range(2025, 2020, -1)
    ]
    donemler.append(dict(donemler[-1], ad="birlesik", bitis=dt.date(2025, 12, 31)))
    klasor = tmp_path / "ag" / "s10"
    klasor.mkdir(parents=True)
    manifest = klasor / "manifest.json"
    manifest.write_text('{"kimlik":"s10","dosyalar":{}}', encoding="utf-8")
    v = dict(
        veri_referanslari=["s10"],
        manifest_ozeti=sha256(manifest.read_bytes()).hexdigest(),
        uyelik_surumu="bist30_2021_2025_v1",
        uyelik_ozeti="uyelik-fixture",
        evren_politikasi="donemsel_bist30_v1",
        kaynak="is_yatirim",
        kalite_surumu="legacy_tansu_v1",
        duzeltme_surumu="is_yatirim",
        takvim_ref="xu100",
        takvim=dict(
            baslangic=dt.date(2021, 1, 1),
            bitis=dt.date(2025, 12, 31),
            seanslar=tuple(gunler),
            kaynak_ref="sentetik E1 takvim kanıtı",
        ),
    )
    y = dict(
        yontem="kayitli_donem_v1",
        tekrar=0,
        yurutme_surumu="bagimsiz_islem_v1",
        fiyat_politikasi="aof_v1",
        muhasebe_politikasi="tani_referans_v1",
    )
    depo = deneme.PilotKayit(tmp_path / "pilot.jsonl")
    makbuz = pilot_deneme(
        depo,
        katalog.legacy_coz(varyant),
        donemler=donemler,
        veri_ayarlari=v,
        yontem_ayarlari=y,
        risk_ayarlari=dict(
            risk_surumu="bagimsiz_risk_v1", nominal_tutar=Decimal("100000")
        ),
        masraf_ayarlari=dict(masraf_surumu="komisyon_bsmv_v1"),
    )
    gun = [
        *map(lambda t: str(t.date()), pd.bdate_range("2018-01-01", periods=510)),
        *gunler,
    ]
    piyasa = []
    for t in gun:
        fiyat = (
            110.0
            if sinyal and t == "2021-12-30"
            else 112.0
            if sinyal and t >= "2021-12-31"
            else 100.0
        )
        piyasa.append(
            dict(
                sembol="TEST",
                tarih=t,
                islem=True,
                kalite_bayraklari=[],
                **{
                    f"duzeltilmis_{ad}": dict(deger=fiyat + fark)
                    for ad, fark in (
                        ("aof", 0),
                        ("kapanis", 0),
                        ("yuksek", 1),
                        ("dusuk", -1),
                    )
                },
                ham_yuksek=dict(deger=fiyat + 1),
                ham_dusuk=dict(deger=fiyat - 1),
                hacim_tl=dict(deger=100.0),
                **(
                    dict(
                        tavan=dict(deger=200.0),
                        taban=dict(deger=50.0),
                        limit_kaniti="sentetik açık limit kanıtı",
                    )
                    if limit
                    else {}
                ),
            )
        )

    def uyelik(istek):
        return dict(
            gunler={
                t: dict(
                    semboller=["TEST"],
                    kanitlar=[dict(kayit_id="uye-TEST", sembol="TEST")],
                )
                for t in istek.tarihler
            },
            evren_politikasi=v["evren_politikasi"],
            uyelik_surumu=v["uyelik_surumu"],
            tablo_parmak_izi=v["uyelik_ozeti"],
        )

    def paket(istek, kimlik, kok):
        assert any(o["kayit_turu"] == "baslangic" for o in depo.oku()), (
            "E1 başlangıç makbuzundan önce çağrıldı"
        )
        secilen = [
            r for r in piyasa if istek.isinma_donemi[0] <= r["tarih"] <= istek.bitis
        ]
        return dict(
            semboller=["TEST"],
            piyasa=secilen,
            gunler=[r["tarih"] for r in secilen],
            uyelik=uyelik(
                veri.UyelikIstegi(
                    tuple(t for t in gunler if istek.baslangic <= t <= istek.bitis),
                    v["evren_politikasi"],
                    v["uyelik_surumu"],
                )
            ),
            referans=dict(
                kayit_id="s10/veri/legacy_tansu_v1",
                goruntu_id="s10",
                manifest_parmak_izi=v["manifest_ozeti"],
                uyelik_tablo_parmak_izi=v["uyelik_ozeti"],
                istenen_donem=dict(baslangic=istek.baslangic, bitis=istek.bitis),
            ),
            kalite=dict(bozuk_satirlar=[], hata_nedenleri=[], uyarilar=[]),
        )

    monkeypatch.setattr(veri, "uyelik_hazirla", uyelik)
    monkeypatch.setattr(veri, "veri_hazirla", paket)
    return depo, makbuz, piyasa


def test_s10_alti_bagimsiz_donem_ve_sinyalsiz_makbuz(tmp_path, monkeypatch):
    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)
    sonuc = ts.kayitli_calistir(
        depo,
        makbuz.deneme_id,
        veri_koku=tmp_path,
        mod="gelistirme",
        isci=1,
        ilerleme=None,
    )
    assert len(sonuc["donemler"]) == 6, "Kayıtlı deneme altı dönem sonucu üretmeli"
    assert [s["donem"]["ad"] for s in sonuc["donemler"]] == [
        "2025",
        "2024",
        "2023",
        "2022",
        "2021",
        "birlesik",
    ]
    assert sonuc["durum"] == "tamamlandi"
    assert all(
        s["adaylar"] == [] and s["islem_referanslari"] == [] for s in sonuc["donemler"]
    )
    for s in sonuc["donemler"]:
        iz = depo.izle(s["makbuz"].olay_id)
        assert iz["sonuc"]["sonuc_turu"] == "donem_v1"
        assert "sinyal_id" not in iz["sonuc"]
        assert iz["deneme"]["deneme_id"] == makbuz.deneme_id
        assert iz["baslangic"]["ayar_parmak_izi"] == makbuz.ayar_ozeti
        assert iz["durum"] == "tamamlandi"
    assert all(o["kayit_turu"] != "islem" for o in depo.oku())
    from hashlib import sha256
    from pathlib import Path

    baslangic = depo.izle(sonuc["donemler"][0]["makbuz"].olay_id)["baslangic"]
    assert baslangic["kod_kimligi"].startswith("kayitli_donem_v1:sha256:")
    assert (
        baslangic["ortam"]["kod_dosyalari"]["tansusinama.py"]
        == sha256(Path(ts.__file__).read_bytes()).hexdigest()
    )
    assert (
        baslangic["ortam"]["git_commit"],
        baslangic["ortam"]["kirli"],
    ) == kayit._git()
    assert baslangic["ortam"]["isci_politikasi"] == dict(yontem="spawn", isci=1)


def s10_calistir(depo, makbuz, kok, isci=1):
    return ts.kayitli_calistir(
        depo,
        makbuz.deneme_id,
        veri_koku=kok,
        mod="gelistirme",
        isci=isci,
        ilerleme=None,
    )


def s10_hesap_ozeti(deger):
    if isinstance(deger, dict):
        return {
            k: s10_hesap_ozeti(v)
            for k, v in deger.items()
            if k
            not in {
                "kosu_id",
                "islem_id",
                "dolum_id",
                "olusturma_zamani",
                "butunluk",
                "son_girdi",
                "isci_pid",
                "makbuz",
                "cikti_parmak_izi",
                "islem_referanslari",
            }
        }
    if isinstance(deger, list):
        return [s10_hesap_ozeti(v) for v in deger]
    return deger


def s10_revizyon(depo, makbuz, **degisiklik):
    d = depo.deneme_oku(makbuz.deneme_id)
    alanlar = {
        a: d[a]
        for a in (
            "donemler",
            "veri_ayarlari",
            "yontem_ayarlari",
            "risk_ayarlari",
            "masraf_ayarlari",
            "eski_referans",
        )
    }
    return depo.deneme_kaydet(
        d["strateji"],
        aktor="test",
        gerekce="sınır örneği",
        ust_deneme=makbuz.deneme_id,
        **(alanlar | degisiklik),
    )


def s11_kayitli(tmp_path, monkeypatch, *, eksenler=None, **secenekler):
    depo, eski, piyasa = s10_kayitli(tmp_path, monkeypatch, **secenekler)
    y = depo.deneme_oku(eski.deneme_id)["yontem_ayarlari"]
    makbuz = s10_revizyon(
        depo,
        eski,
        yontem_ayarlari=dict(
            yontem="kayitli_izgara_v1",
            tekrar=0,
            secim_politikasi="genis_bolge_net_r_v1",
            olcu_politikasi="bagimsiz_olcu_v1",
            eksenler=eksenler
            if eksenler is not None
            else [dict(ad="min_gun", birim="gun", degerler=[2, 3, 5])],
            hucre_yontemi=y,
        ),
    )
    return depo, makbuz, piyasa


def s11_calistir(depo, makbuz, kok, **secenekler):
    return ts.kayitli_izgara_calistir(
        depo,
        makbuz.deneme_id,
        veri_koku=kok,
        mod="gelistirme",
        isci=1,
        ilerleme=None,
        **secenekler,
    )


def s13_yontem(kaynak):
    return dict(
        yontem="kayitli_monte_carlo_v1",
        tekrar=1000,
        kontrol_noktalari=[1000],
        calisma_turu="on_gosterim",
        tohum=42,
        uretec="PCG64DXSM_SeedSequence_pool4_v1",
        akis_surumu="indeksli_v1",
        muhasebe_politikasi="kapali_gerceklesme_gunluk_r_v1",
        hassasiyet_r=0.01,
        deneyler=[
            "sira_v1",
            "yerine_koyma_v1",
            "ortak_tarih_blok_v1",
            "islem_kacirma_v1",
            "ayar_komsulugu_v1",
        ],
        kaynak=kaynak,
    )


def s13_kayitli(tmp_path, monkeypatch, *, sinyalli=True, eksenler=None):
    """E1 sözleşme verisi; kaynak WF ile MC hesap/kayıt sahipleri gerçektir."""
    import datetime as dt
    from tansu import deneme

    depo, wf, piyasa = (s12_sinyalli if sinyalli else s12_kayitli)(
        tmp_path, monkeypatch
    )
    if eksenler is not None:
        y = depo.deneme_oku(wf.deneme_id)["yontem_ayarlari"] | dict(eksenler=eksenler)
        wf = s10_revizyon(depo, wf, yontem_ayarlari=y)
    sonuc = s12_calistir(depo, wf, tmp_path)
    assert sonuc["durum"] == "tamamlandi", (
        "MC örneği tamamlanmış gerçek WF yürütmesi gerektirir."
    )
    kaynak = dict(
        deneme_id=wf.deneme_id,
        kosu_id=sonuc["kosu_id"],
        sonuc_ref=sonuc["sonuc_makbuzu"].olay_id,
        bitis_ref=sonuc["bitis_makbuzu"].olay_id,
        icerik_ozeti="00" * 32,
    )
    kabul, hata = None, None
    try:
        kabul = deneme._mc_kaynagi(depo.oku(), kaynak, ozet_denetle=False)
    except deneme.PilotHatasi as yakalanan:
        hata = yakalanan
    assert kabul is not None, (
        f"Tamamlanmış WF'nin gerçek makbuzları MC kaynağı olmalıdır: {hata}"
    )
    kaynak["icerik_ozeti"] = kabul["icerik_ozeti"]
    donemler = [
        dict(
            ad=str(y),
            baslangic=dt.date(y, 1, 1),
            bitis=dt.date(y, 12, 31),
            isinma_baslangici=dt.date(2018, 1, 1),
            sinir_surumu="surekli_ileri_v1",
        )
        for y in range(2022, 2026)
    ]
    donemler.append(dict(donemler[0], ad="birlesik", bitis=dt.date(2025, 12, 31)))
    mc = s10_revizyon(depo, wf, donemler=donemler, yontem_ayarlari=s13_yontem(kaynak))
    return depo, mc, piyasa, kabul


def s13_kosu(depo, makbuz, kaynak):
    d = depo.deneme_oku(makbuz.deneme_id)
    v, y = d["veri_ayarlari"], d["yontem_ayarlari"]
    g = ts._mc_girdi(d, kaynak)
    ctx = depo.kosu(
        d["deneme_id"],
        mod="gelistirme",
        anlik_goruntu=v["veri_referanslari"][0],
        manifest_ozeti=v["manifest_ozeti"],
        uyelik_surumu=v["uyelik_surumu"],
        kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
        ortam=dict(python="fixture"),
        bagimlilik_ozeti="fixture",
        tohum=y["tohum"],
        ureteci_surumu=y["uretec"],
        is_listesi=[i["anahtar"] for i in g["isler"]],
    )
    return ctx, d, g


def s13_plan(depo, kosu, d, g, *, deney="ayar_komsulugu_v1", sayi=1):
    from tansu import deneme

    gm = kosu.mc_girdi_kaydet(kayit=g)
    is_ = next(
        i
        for i in g["isler"]
        if i["dilim"] == "2022" and i["deney"] == deney and i["durum"] == "hazir"
    )
    komsular = deneme._mc_komsular(depo.oku(), g)
    planlar = ts._mc_planlar(depo, kosu, d, g, gm.olay_id, is_, 0, sayi, komsular, {})
    return is_, planlar


def test_s13_wf_bos_nufus_bes_deneyi_sifir_risk_diye_tamamlamaz(tmp_path, monkeypatch):
    depo, m, _, _ = s13_kayitli(tmp_path, monkeypatch, sinyalli=False)
    sonuc = ts.kayitli_monte_carlo_calistir(
        depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=None
    )
    assert sonuc["durum"] == "eksik" and sonuc["yontem_tamamlandi"] is False
    assert len(sonuc["isler"]) == 25
    assert all(
        i["durum"] == "olculemedi"
        and i["neden"] == "kapali_islem_yok"
        and i["denenen"] == i["tamamlanan"] == 0
        for i in sonuc["isler"]
    )
    assert not any(o["kayit_turu"] in ("mc_plan", "mc_senaryo") for o in depo.oku())
    assert depo.izle(sonuc["sonuc_makbuzu"].olay_id)["durum"] == "hata"


def test_s13_wf_gercek_ayar_stresi_kendi_sinyalini_ceyrekler_arasi_korur(
    tmp_path, monkeypatch
):
    from copy import deepcopy
    from tansu import deneme, istatistik

    depo, m, _, kaynak = s13_kayitli(tmp_path, monkeypatch)
    ctx, d, g = s13_kosu(depo, m, kaynak)
    asil = ts._ileri_test_sembolu
    tasima = {}

    def hesap(*a, **kw):
        durum = asil(*a, **kw)
        if a[3]["is_id"] in ("2022Q1", "2022Q2", "2022Q3"):
            tasima[a[3]["is_id"]] = deepcopy(durum)
        return durum

    monkeypatch.setattr(ts, "_ileri_test_sembolu", hesap)
    with ctx as kosu:
        is_, [(p, pm)] = s13_plan(depo, kosu, d, g)
        secim = next(o for o in kaynak["secimler"] if o["bolum_id"] == "2022Q1")
        secim = secim["kayit"] | dict(secim_ref=secim["kayit_id"])
        cocuk = next(c for c in p["stres_cocuklari"] if c["bolum"] == "2022Q1")
        r = ts._kayitli_sonuc(
            d, kosu.makbuz.kosu_id, "2022Q1", kaynak["deneme"]["donemler"][0]
        )
        paket = ts._ileri_test_paketi(d, r, tmp_path, {})
        sira = next(
            i for i in g["isler"] if i["dilim"] == "2022" and i["deney"] == "sira_v1"
        )
        _, baska_plan = ts._mc_planlar(
            depo, kosu, d, g, p["girdi_ref"], sira, 0, 1, [], {}
        )[0]
        with monkeypatch.context() as probe:
            probe.setattr(
                aileler,
                "ortak_donem_kurulumu",
                lambda *a, **kw: pytest.fail("Yanlış MC bağı E2'ye ulaştı."),
            )
            for ayar in (
                dict(mc_plan_ref=pm.olay_id),
                dict(mc_cocuk_id=cocuk["deneme_id"]),
                dict(mc_plan_ref="kayitsiz-plan", mc_cocuk_id=cocuk["deneme_id"]),
                dict(mc_plan_ref=baska_plan.olay_id, mc_cocuk_id=cocuk["deneme_id"]),
                dict(mc_plan_ref=pm.olay_id, mc_cocuk_id=secim["test_deneme_id"]),
            ):
                with pytest.raises(deneme.PilotHatasi):
                    asil(
                        depo,
                        d,
                        kosu,
                        r,
                        paket,
                        "TEST",
                        secim,
                        None,
                        r["uyelik"],
                        **ayar,
                    )
            baska_ctx, _, _ = s13_kosu(depo, m, kaynak)
            with baska_ctx as baska_kosu:
                with pytest.raises(deneme.PilotHatasi, match="başka koşuya"):
                    asil(
                        depo,
                        d,
                        baska_kosu,
                        r,
                        paket,
                        "TEST",
                        secim,
                        None,
                        r["uyelik"],
                        mc_plan_ref=pm.olay_id,
                        mc_cocuk_id=cocuk["deneme_id"],
                    )
        tekrar, refler = ts._mc_ayar_yeniden_sina(
            depo, d, kosu, kaynak, p, pm.olay_id, tmp_path
        )
        olcu = istatistik.mc_senaryo_olculeri(
            g, is_, p["cekilis"], durumlar=tekrar["durumlar"]
        )
        sm = kosu.mc_senaryo_sonucu_kaydet(
            kayit=dict(
                plan_ref=pm.olay_id,
                durum="tamamlandi",
                **olcu,
                yeniden_sinama=tekrar,
                sonuc_referanslari=refler,
                asama=None,
                neden=None,
            )
        )
    q1, q2, q3 = (tasima[q] for q in ("2022Q1", "2022Q2", "2022Q3"))
    assert q1["durum"] == "bekliyor" and q2["durum"] == "acik_son"
    assert (
        q1["pozisyon"]["ayar"]
        == q2["pozisyon"]["ayar"]
        == q3["islemler"][0]["pozisyon"]["ayar"]
    )
    sinyal_id = q1["pozisyon"]["risk_girdisi"]["sinyal_id"]
    assert sinyal_id == q2["pozisyon"]["risk_girdisi"]["sinyal_id"]
    olaylar = depo.oku()
    sinyal = deneme._bul(olaylar, sinyal_id, "mc_sinyal")
    assert sinyal["kayit"]["plan_ref"] == pm.olay_id
    assert sinyal["kayit"]["sinyal"]["parametreler"] == q1["pozisyon"]["ayar"]
    assert q3["islemler"][0]["pozisyon"]["cikis_tarih"] == "2022-07-04"
    assert (
        len(tekrar["bolumler"]) == 16 and olcu["olculer"]["islem_sayisi"]["deger"] == 1
    )
    assert (
        deneme._bul(olaylar, sm.olay_id, "mc_senaryo")["kayit"]["yeniden_sinama"]
        == tekrar
    )


def test_s13_wf_stres_revizyonu_degisen_girisi_yamasiz_e2_ve_e3e_tasir(
    tmp_path, monkeypatch
):
    from tansu import deneme, katalog, saglamlik
    from tests.test_aileler import _mumlar, _ortak_paket
    from tests.test_motor import s09_istek

    gercek_kurulum = aileler.kurulum
    depo, m, _, kaynak = s13_kayitli(
        tmp_path,
        monkeypatch,
        eksenler=[dict(ad="esik", birim="oran", degerler=[0.010, 0.012, 0.015])],
    )
    ctx, d, g = s13_kosu(depo, m, kaynak)
    # This is an independent candle calculation, not a second market replay.
    kapanis = (
        [180.0] * 510
        + [185.0, 100.0]
        + [100.0] * 510
        + [108.0, 110.0, 112.0, 114.0, 120.0, 100.0]
    )
    yuksek, dusuk, hacim = (
        [k + 1 for k in kapanis],
        [k - 1 for k in kapanis],
        [100.0] * len(kapanis),
    )
    for j in range(len(kapanis) - 6, len(kapanis) - 1):
        yuksek[j], dusuk[j], hacim[j] = kapanis[j] + 0.1, kapanis[j - 1] - 0.1, 10000.0
    f = _mumlar(kapanis, yuksek, dusuk, hacim)
    f["aof"] = f.kapanis
    paket = _ortak_paket(f)
    for r in paket["piyasa"]:
        r.update(
            islem=True,
            ham_yuksek=r["duzeltilmis_yuksek"],
            ham_dusuk=r["duzeltilmis_dusuk"],
            tavan=dict(deger=1000.0),
            taban=dict(deger=1.0),
            limit_kaniti="Sentetik açık limit kanıtı.",
        )
    sonuclar = []
    with ctx as kosu:
        kosu.mc_girdi_kaydet(kayit=g)
        komsular = deneme._mc_komsular(depo.oku(), g)
        for esik in (0.012, 0.015):
            indeksler = [
                next(
                    i for i, demet in enumerate(q["demetler"]) if demet["esik"] == esik
                )
                for q in komsular
            ]
            cocuklar = ts._mc_stres_revizyonlari(depo, kosu, komsular, indeksler, {})
            c = next(c for c in cocuklar if c["bolum"] == "2022Q1")
            cocuk = depo.deneme_oku(c["deneme_id"])
            s = cocuk["strateji"]
            strateji = katalog.legacy_coz(
                s["varyant"],
                s["katalog_surumu"],
                sayisal_ayarlar={
                    a["ad"]: a["deger"]
                    for a in s["parametreler"]
                    if a["koken"] == "legacy_izgara"
                },
            )
            p = aileler.Parametre(**{a.ad: a.deger for a in strateji.parametreler})
            with monkeypatch.context() as hesap_kapisi:
                hesap_kapisi.setattr(aileler, "kurulum", gercek_kurulum)
                hesap = aileler.ortak_donem_kurulumu(paket, strateji)["TEST"]
            assert len(hesap["sinyaller"]) == 1
            mumlar = ts._s10_mumlar(paket, "TEST", hesap)
            durum = saglamlik.ema_hucre_calistir(
                mumlar,
                p,
                kurulum=hesap["kurulum"],
                sinyal_konumlari={
                    pd.Timestamp(s["tarih"]): s["kayit_id"] for s in hesap["sinyaller"]
                },
                yurutme=s09_istek(
                    strateji_id=strateji.kayit_id,
                    strateji_surumu=strateji.katalog_surumu,
                ),
            )
            sonuclar.append((hesap["sinyaller"][0]["kutu_ust"]["deger"], durum))
    assert [k for k, _ in sonuclar] == [108.1, 110.1]
    for _, durum in sonuclar:
        assert any(
            d["yon"] == "alis" and d["fiyat"] == 100.0 for d in durum["dolumlar"]
        )
        assert durum["pozisyon"]["ayar"]["esik"] in (0.012, 0.015)
    assert [durum["pozisyon"]["ayar"]["esik"] for _, durum in sonuclar] == [
        0.012,
        0.015,
    ]


def test_s13_wf_genel_giris_iki_ucuz_anahtarin_binlik_onekini_dogal_hesaplar(
    tmp_path, monkeypatch
):
    from tansu import deneme

    depo, m, _, _ = s13_kayitli(tmp_path, monkeypatch)
    kaydet = deneme._Kosu.mc_kontrol_kaydet
    kontrol_sayisi = 0

    def kaydet_ve_dur(kosu, *, kayit):
        nonlocal kontrol_sayisi
        makbuz = kaydet(kosu, kayit=kayit)
        kontrol_sayisi += 1
        if kontrol_sayisi == 2:
            raise KeyboardInterrupt(
                "İki doğal binlik anahtar kaydından sonra kontrollü kesinti."
            )
        return makbuz

    monkeypatch.setattr(deneme._Kosu, "mc_kontrol_kaydet", kaydet_ve_dur)
    with pytest.raises(KeyboardInterrupt, match="kontrollü kesinti"):
        ts.kayitli_monte_carlo_calistir(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=None
        )
    olaylar = depo.oku()
    girdi = next(o["kayit"] for o in olaylar if o["kayit_turu"] == "mc_girdi")
    kontroller = [o["kayit"] for o in olaylar if o["kayit_turu"] == "mc_kontrol"]
    assert len(kontroller) == 2
    kaynak_r = [
        r["net_r"] for r in girdi["nufus"] if r["cikis_tarih"].startswith("2022-")
    ]
    assert len(kaynak_r) == 1
    for kontrol, deney in zip(kontroller, ("sira_v1", "yerine_koyma_v1"), strict=True):
        is_ = next(i for i in girdi["isler"] if i["anahtar"] == kontrol["anahtar"])
        assert is_["deney"] == deney and is_["dilim"] == "2022"
        planlar = [
            o
            for o in olaylar
            if o["kayit_turu"] == "mc_plan" and o["kayit"]["anahtar"] == is_["anahtar"]
        ]
        assert [o["kayit"]["indeks"] for o in planlar] == list(range(1000))
        assert all(o["kayit"]["cekilis"]["indeksler"] == [0] for o in planlar)
        sonuclar = [
            deneme._bul(olaylar, ref, "mc_senaryo")["kayit"]
            for ref in kontrol["sonuc_referanslari"]
        ]
        assert len(sonuclar) == 1000
        assert all(
            r["durum"] == "tamamlandi"
            and r["olculer"]["toplam_r"]["deger"] == kaynak_r[0]
            for r in sonuclar
        )
        assert (
            kontrol["tani"]["tekrar"] == 1000
            and kontrol["tani"]["durum"] == "on_gosterim"
        )
    kurtarma = depo.kurtar()["mc_belirsiz_kosular"][0]["isler"]
    assert sum(i["kesin_tamamlanan"] for i in kurtarma) == 2000
    assert all(i["deneme_yayin_belirsiz"] is None for i in kurtarma)
    assert not any(
        o["kayit_turu"] in ("mc_ozet", "bitis") and o.get("deneme_id") == m.deneme_id
        for o in olaylar
    )


def test_s13_wf_sinyal_partisi_yazilamazsa_e3_baslamaz(tmp_path, monkeypatch):
    from tansu import deneme, saglamlik

    depo, m, _, kaynak = s13_kayitli(tmp_path, monkeypatch)
    ctx, d, g = s13_kosu(depo, m, kaynak)
    e3 = []
    asil = saglamlik.ema_hucre_calistir

    def hesap(*a, **kw):
        e3.append(kw)
        return asil(*a, **kw)

    with ctx as kosu:
        _, [(p, pm)] = s13_plan(depo, kosu, d, g)
        monkeypatch.setattr(saglamlik, "ema_hucre_calistir", hesap)

        def yaz(*a, **kw):
            raise deneme.PilotYazmaHatasi("MC sinyal diski")

        monkeypatch.setattr(kosu, "mc_sinyalleri_kaydet", yaz)
        with pytest.raises(deneme.PilotYazmaHatasi, match="MC sinyal diski"):
            ts._mc_ayar_yeniden_sina(depo, d, kosu, kaynak, p, pm.olay_id, tmp_path)
    assert e3 == []
    kurtarma = depo.kurtar()["mc_belirsiz_kosular"][0]["isler"]
    is_ = next(i for i in kurtarma if i["deneme_yayin_belirsiz"])
    assert is_["denenen"] is None and is_["kesin_tamamlanan"] == 0
    assert is_["deneme_yayin_belirsiz"] == [0, 0]


def test_s13_gercek_wf_kaynagi_yoksa_plan_ve_hesap_baslamaz(tmp_path, monkeypatch):
    import datetime as dt
    from tansu import deneme

    depo, eski, _ = s10_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(eski.deneme_id)
    kaynak = dict(
        deneme_id=eski.deneme_id,
        kosu_id="olmayan-wf",
        sonuc_ref="olmayan-ozet",
        bitis_ref="olmayan-bitis",
        icerik_ozeti="00" * 32,
    )
    donemler = sorted(
        [q for q in d["donemler"] if q["ad"] not in ("2021", "birlesik")],
        key=lambda q: q["ad"],
    )
    donemler.append(dict(d["donemler"][-1], baslangic=dt.date(2022, 1, 1)))
    m = s10_revizyon(depo, eski, donemler=donemler, yontem_ayarlari=s13_yontem(kaynak))
    once, hesap = depo.yol.read_bytes(), []
    monkeypatch.setattr(veri, "veri_hazirla", lambda *a: hesap.append(a))
    hata = None
    try:
        ts.kayitli_monte_carlo_calistir(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=None
        )
    except deneme.PilotHatasi as yakalanan:
        hata = yakalanan
    assert hata is not None, "MC kayıtsız WF kaynağıyla hesap veya plan üretemez."
    assert "kaynak_wf_yok" in str(hata)
    assert hesap == [] and depo.yol.read_bytes() == once


def test_s13_onaysiz_plan_yeniden_sinama_baslatmaz(tmp_path, monkeypatch):
    from tansu import deneme

    depo = deneme.PilotKayit(tmp_path / "mc.jsonl")
    hesap = []
    monkeypatch.setattr(veri, "uyelik_hazirla", lambda *a: hesap.append(a))
    hata = None
    try:
        ts._mc_ayar_yeniden_sina(
            depo, None, None, None, {}, "kesinlesmemis-plan", tmp_path
        )
    except deneme.PilotHatasi as yakalanan:
        hata = yakalanan
    assert hata is not None, "Kesinleşmiş plan olmadan yeniden sınama başlayamaz."
    assert "kesinlesmemis-plan" in str(hata)
    assert hesap == [] and not depo.yol.exists()


def test_s11_kayitli_hucreler_alti_donemi_korur_ve_e1_paylasir(tmp_path, monkeypatch):
    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    hazirla = veri.veri_hazirla
    istekler = []

    def hesap(*a):
        olaylar = depo.oku()
        baslangic = [o for o in olaylar if o["kayit_turu"] == "baslangic"][-1]
        assert baslangic["deneme_id"] != makbuz.deneme_id
        d = depo.deneme_oku(baslangic["deneme_id"])
        assert d["ust_deneme_id"] == makbuz.deneme_id
        assert baslangic["ayar_parmak_izi"] == d["ayar_parmak_izi"]
        istekler.append(a[0])
        return hazirla(*a)

    monkeypatch.setattr(veri, "veri_hazirla", hesap)
    s = s11_calistir(depo, makbuz, tmp_path)
    assert len(s.get("hucreler", [])) == 3, "Arama her kayıtlı koordinatı korumalı"
    assert len(istekler) == 6
    assert [h["indeks"] for h in s["hucreler"]] == [[0], [1], [2]]
    assert all(len(h["donemler"]) == 6 for h in s["hucreler"])
    assert all(h["durum"] == "islemsiz" for h in s["hucreler"])
    assert all(b["secilen"] is None for b in s["bolgeler"])
    iz = depo.izle(s["sonuc_makbuzu"].olay_id)
    assert iz["sonuc"]["sonuc_turu"] == "arama_v1"
    assert len(iz["sonuc"]["hucreler"]) == 3
    assert "sinyal_id" not in iz["sonuc"]


def test_s11_cocuk_kayit_hatasi_hesap_baslatmaz_tum_yuvalari_korur(
    tmp_path, monkeypatch
):
    from tansu import deneme

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    kaydet = depo.deneme_kaydet
    hesaplar = []

    def kayit(*a, **k):
        if k.get("ust_deneme") == makbuz.deneme_id:
            raise deneme.PilotYazmaHatasi("çocuk kaydı yazılamadı")
        return kaydet(*a, **k)

    monkeypatch.setattr(depo, "deneme_kaydet", kayit)
    monkeypatch.setattr(veri, "veri_hazirla", lambda *a: hesaplar.append(a))
    hata = None
    try:
        s11_calistir(depo, makbuz, tmp_path)
    except deneme.PilotYazmaHatasi as yakalanan:
        hata = yakalanan
    assert hata is not None, "Kayıt hatası çağırana ulaşmalı"
    assert hesaplar == []
    assert len(hata.sonuc["hucreler"]) == 3
    assert hata.sonuc["hucreler"][0]["durum"] == "kayit_hatasi"
    assert all(len(h["donemler"]) == 6 for h in hata.sonuc["hucreler"])
    assert all(h["deneme_id"] is None for h in hata.sonuc["hucreler"])
    assert hata.sonuc["baslangic_makbuzu"].ayar_ozeti == makbuz.ayar_ozeti


@pytest.mark.parametrize(
    "eksen",
    [
        dict(ad="stop", birim="metin", degerler=["atr2"]),
        dict(ad="min_gun", birim="gun", degerler=[3, 2]),
        dict(ad="min_gun", birim="gun", degerler=[2, 2]),
        dict(ad="min_gun", birim="gun", degerler=[1]),
        dict(ad="esik", birim="gun", degerler=[0.010]),
    ],
)
def test_s11_izinsiz_eksen_hesap_ve_cocuk_kaydindan_once_reddedilir(
    tmp_path, monkeypatch, eksen
):
    from tansu import deneme

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch, eksenler=[eksen])
    once = depo.yol.read_bytes()
    hesap = []
    monkeypatch.setattr(veri, "veri_hazirla", lambda *a: hesap.append(a))
    hata = None
    try:
        s11_calistir(depo, makbuz, tmp_path)
    except deneme.PilotHatasi as yakalanan:
        hata = yakalanan
    assert hata is not None, "İzinsiz eksen hesap öncesinde reddedilmeli"
    assert hesap == [] and depo.yol.read_bytes() == once


@pytest.mark.parametrize("hedef", ["ust", "cocuk"])
def test_s11_baslangicta_tam_ayar_degismesi_hesabi_engeller(
    tmp_path, monkeypatch, hedef
):
    from contextlib import contextmanager
    from dataclasses import replace
    from tansu import deneme

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    kosu = depo.kosu
    hesap = []

    @contextmanager
    def degisen(deneme_id, **k):
        with kosu(deneme_id, **k) as handle:
            if (deneme_id == makbuz.deneme_id) == (hedef == "ust"):
                handle.makbuz = replace(handle.makbuz, ayar_ozeti="degisen-tam-ayar")
            yield handle

    monkeypatch.setattr(depo, "kosu", degisen)
    monkeypatch.setattr(veri, "veri_hazirla", lambda *a: hesap.append(a))
    hata = None
    try:
        s = s11_calistir(depo, makbuz, tmp_path)
    except deneme.PilotHatasi as yakalanan:
        hata = yakalanan
    assert hesap == []
    if hedef == "ust":
        assert hata is not None, "Üst başlangıç makbuzu tam ayarı doğrulamalı"
    else:
        assert all(h["durum"] == "hesap_hatasi" for h in s["hucreler"])
        assert all(h["neden"] for h in s["hucreler"])


def test_s11_bir_donem_hatasi_18_yuvayi_ve_gercek_makbuzlari_korur(
    tmp_path, monkeypatch
):
    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    hazirla = veri.veri_hazirla

    def eksik(istek, *a):
        if istek.baslangic == "2024-01-01":
            raise veri.VeriHatasi("2024 fiyatı eksik")
        return hazirla(istek, *a)

    monkeypatch.setattr(veri, "veri_hazirla", eksik)
    s = s11_calistir(depo, makbuz, tmp_path)
    assert len(s["hucreler"]) == 3
    for h in s["hucreler"]:
        assert len(h["donemler"]) == 6
        assert h["donemler"][1]["durum"] == "eksik"
        assert "2024 fiyatı eksik" in h["donemler"][1]["neden"]
        assert all(d["sonuc_ref"] for d in h["donemler"])
    assert s["durum"] == "hata"
    assert all(b["secilen"] is None for b in s["bolgeler"])


def test_s11_iki_gercek_cagiran_ayni_elle_para_sonucunu_olcer():
    from tansu import istatistik, saglamlik
    from tests.test_motor import STD, r, s09_istek, s09_mumlar

    m = s09_mumlar(
        [
            r(*STD),
            r(*STD),
            r(114, 115, 110, 114),
            r(118, 120, 116, 118),
            r(80, 82, 79, 81),
        ]
    )
    durum = saglamlik.ema_hucre_calistir(
        m,
        dataclasses.replace(aileler.Parametre(), cikis="atr3"),
        kurulum=None,
        sinyal_konumlari={m.index[0]: "sinyal-1"},
        yurutme=s09_istek(),
    )
    dolumlar = [
        dict(dolum_id="al", yon="alis", adet=15, fiyat=100),
        dict(dolum_id="yari", yon="satis", adet=7, fiyat=115),
        dict(dolum_id="son", yon="satis", adet=8, fiyat=80),
    ]
    girdi = risk_satiri(dolumlar=dolumlar)
    girdi["nominal_tutar"] = 8000.0
    tablo = ts._getirili(pd.DataFrame([girdi]))
    bir = istatistik.olc(durum["islemler"], politika="bagimsiz_olcu_v1")
    iki = istatistik.olc(
        [dict(islem_id="elle", sonuc=tablo.iloc[0].to_dict())],
        politika="bagimsiz_olcu_v1",
    )
    # 1500 TL alış, 1445 TL satış. İki yönde masraf 4,638375 TL; net -59,638375 TL.
    for sonuc in (bir, iki):
        assert sonuc["olculer"]["net_sonuc"] == dict(
            deger=pytest.approx(-59.638375), birim="TL", bos_nedeni=None
        )
        assert sonuc["olculer"]["masraf"] == dict(
            deger=pytest.approx(4.638375), birim="TL", bos_nedeni=None
        )
        assert sonuc["olculer"]["islem"]["deger"] == 1
        assert sonuc["islemler"][0]["paydalar"]["ilk_risk"] == pytest.approx(154.48875)
    assert bir["olculer"] == iki["olculer"]


def test_s11_tum_alan_hesap_oncesi_cozulur_alan_disi_hucre_korunur(
    tmp_path, monkeypatch
):
    from tansu import katalog

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    coz, hazirla = katalog.legacy_coz, veri.veri_hazirla
    cozulmus = set()

    def sinirli(*a, **k):
        h = k.get("sayisal_ayarlar") or {}
        if "min_gun" in h:
            cozulmus.add(h["min_gun"])
            if h["min_gun"] == 3:
                raise katalog.KatalogHatasi("GECERSIZ_BILESIM", "birleşim izinli değil")
        return coz(*a, **k)

    def hesap(*a):
        assert cozulmus == {2, 3, 5}, (
            "İlk E1 çağrısı bütün alanın çözülmesini beklemeli"
        )
        return hazirla(*a)

    monkeypatch.setattr(katalog, "legacy_coz", sinirli)
    monkeypatch.setattr(veri, "veri_hazirla", hesap)
    s = s11_calistir(depo, makbuz, tmp_path)
    assert [h["indeks"] for h in s["hucreler"]] == [[0], [1], [2]]
    assert s["hucreler"][1]["durum"] == "alan_disi"
    assert "birleşim izinli değil" in s["hucreler"][1]["neden"]
    assert s["hucreler"][1]["deneme_id"] is None
    assert all(h["deneme_id"] for h in (s["hucreler"][0], s["hucreler"][2]))


def test_s11_yayin_hatasi_dogrulanmis_makbuzlari_ve_yuvalari_korur(
    tmp_path, monkeypatch
):
    from tansu import deneme

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    ekle = depo._ekle

    def yaz(olay, *a):
        if olay.get("sonuc_turu") == "arama_v1":
            raise deneme.PilotYazmaHatasi("üst sonuç yazılamadı")
        return ekle(olay, *a)

    monkeypatch.setattr(depo, "_ekle", yaz)
    with pytest.raises(ts.AramaYazmaHatasi, match="üst sonuç yazılamadı") as hata:
        s11_calistir(depo, makbuz, tmp_path)
    s = hata.value.sonuc
    assert s["sonuc_makbuzu"] is None and s["bitis_makbuzu"] is None
    assert len(s["hucreler"]) == 3
    assert sum(len(h["donemler"]) for h in s["hucreler"]) == 18
    assert all(
        h["kayit_makbuzu"] and h["baslangic_makbuzu"] and h["bitis_makbuzu"]
        for h in s["hucreler"]
    )
    assert all(
        depo.izle(d["sonuc_ref"])["sonuc"]["deneme_id"] == h["deneme_id"]
        for h in s["hucreler"]
        for d in h["donemler"]
    )
    assert not any(
        o["kayit_turu"] == "bitis" and o["kosu_id"] == s["kosu_id"] for o in depo.oku()
    )


def test_s10_bir_ve_iki_spawn_isci_sayisal_sonucu_degistirmez(tmp_path, monkeypatch):
    import os

    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch, sinyal=True)
    ilk = s10_calistir(depo, makbuz, tmp_path, 1)
    ikinci = s10_calistir(depo, makbuz, tmp_path, 2)
    assert ilk["durum"] == ikinci["durum"] == "tamamlandi"
    assert ilk["kosu_id"] != ikinci["kosu_id"]
    assert ilk["deneme_id"] == ikinci["deneme_id"] == makbuz.deneme_id
    assert ilk["ayar_parmak_izi"] == ikinci["ayar_parmak_izi"] == makbuz.ayar_ozeti
    assert s10_hesap_ozeti(ilk["donemler"]) == s10_hesap_ozeti(ikinci["donemler"])
    assert len({s["isci_pid"] for s in ilk["donemler"]}) == 1
    assert len({s["isci_pid"] for s in ikinci["donemler"]}) == 2
    assert os.getpid() not in {
        s["isci_pid"] for s in ilk["donemler"] + ikinci["donemler"]
    }
    yil = ilk["donemler"][4]
    assert yil["durumlar"]["TEST"]["durum"] == "bekliyor"
    assert yil["islem_referanslari"] == []
    assert yil["adaylar"][-1]["yurutme_nedeni"] == "sonraki_seans_ufuk_disinda"
    birlesik = ilk["donemler"][5]
    durum = birlesik["durumlar"]["TEST"]
    assert durum["durum"] == "acik_son"
    assert [(d["tarih"], d["yon"], d["fiyat"]) for d in durum["dolumlar"]] == [
        ("2022-01-04", "alis", 112.0)
    ]
    assert durum["sonuc"]["net_r"] is None
    assert durum["sonuc"]["net_fiyat_getirisi"] is None
    assert durum["degerleme"] == dict(tarih="2025-12-31", fiyat=112.0)
    assert all(
        s["durumlar"]["TEST"]["iz"][0]["tarih"].startswith(s["donem"]["ad"])
        for s in ilk["donemler"][:5]
    )
    bag = depo.izle(birlesik["makbuz"].olay_id)["sonuc"]
    assert bag["cikti_referanslari"] == [
        s["makbuz"].olay_id for s in ilk["donemler"][:5]
    ]
    assert len([o for o in depo.oku() if o["kayit_turu"] == "deneme"]) == 1
    assert {o["donem"]["ad"] for o in depo.oku() if o["kayit_turu"] == "islem"} == {
        "birlesik"
    }


def test_s10_limit_bilinmiyor_sifir_dolumu_basari_yapmaz(tmp_path, monkeypatch):
    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch, sinyal=True, limit=False)
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    birlesik = sonuc["donemler"][5]
    assert sonuc["durum"] == "hata"
    assert birlesik["asama"] == "limit_kaniti"
    assert birlesik["adaylar"]
    assert birlesik["durumlar"]["TEST"]["dolumlar"] == []
    assert "limit_bilinmiyor" in [
        r["neden"] for r in birlesik["durumlar"]["TEST"]["retler"]
    ]
    assert all(o["kayit_turu"] != "islem" for o in depo.oku())
    assert sonuc["donemler"][4]["durum"] == "tamamlandi"
    bitis = depo.oku()[-1]
    assert bitis["durum"] == "hata" and bitis["basarisiz"] == ["donem:birlesik"]


@pytest.mark.parametrize("asama", ["veri", "kurulum"])
def test_s10_cocuk_hatasi_diger_makbuzlari_korur(tmp_path, monkeypatch, asama):
    from copy import deepcopy

    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)
    hazirla = veri.veri_hazirla

    def arizali(istek, *a):
        if istek.baslangic == "2024-01-01":
            if asama == "veri":
                raise veri.VeriHatasi("2024 veri arızası")
            paket = deepcopy(hazirla(istek, *a))
            paket["piyasa"][0]["hacim_tl"] = None
            return paket
        return hazirla(istek, *a)

    monkeypatch.setattr(veri, "veri_hazirla", arizali)
    sonuc = s10_calistir(depo, makbuz, tmp_path, 2)
    assert sonuc["durum"] == "hata"
    assert [
        (s["donem"]["ad"], s["asama"])
        for s in sonuc["donemler"]
        if s["durum"] == "hata"
    ] == [("2024", asama)]
    assert len([s for s in sonuc["donemler"] if s["durum"] == "tamamlandi"]) == 5
    bitis = depo.oku()[-1]
    assert bitis["basarisiz"] == ["donem:2024"]
    assert set(bitis["tamamlanan"]) == {
        "donem:2025",
        "donem:2023",
        "donem:2022",
        "donem:2021",
        "donem:birlesik",
    }
    assert len(bitis["cikti_referanslari"]) == 6


@pytest.mark.parametrize("ariza", ["baslangic", "sonuc"])
def test_s10_yazma_arizasi_hesabi_ve_sahte_basarili_bitisi_engeller(
    tmp_path, monkeypatch, ariza
):
    from tansu import deneme

    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)
    ekle = depo._ekle
    hazirla = veri.veri_hazirla
    hesaplar, sonuclar = [], []

    def hesap(*a):
        hesaplar.append(True)
        return hazirla(*a)

    def yaz(olay, *a):
        if olay["kayit_turu"] == "sonuc":
            sonuclar.append(olay)
        if (ariza == "baslangic" and olay["kayit_turu"] == "baslangic") or (
            ariza == "sonuc" and len(sonuclar) == 2
        ):
            raise deneme.PilotYazmaHatasi("disk arızası")
        return ekle(olay, *a)

    monkeypatch.setattr(depo, "_ekle", yaz)
    monkeypatch.setattr(veri, "veri_hazirla", hesap)
    with pytest.raises(deneme.PilotYazmaHatasi, match="disk arızası"):
        s10_calistir(depo, makbuz, tmp_path)
    tekrar = deneme.PilotKayit(depo.yol)
    olaylar = tekrar.oku()
    assert not any(
        o["kayit_turu"] == "bitis" and o["durum"] == "tamamlandi" for o in olaylar
    )
    if ariza == "baslangic":
        assert hesaplar == []
        assert [o["kayit_turu"] for o in olaylar] == ["deneme"]
    else:
        kalici = [o for o in olaylar if o["kayit_turu"] == "sonuc"]
        assert len(kalici) == 1 and kalici[0]["donem"]["ad"] == "2025"
        assert tekrar.izle(kalici[0]["kayit_id"])["durum"] == "cozumsuz"


@pytest.mark.parametrize(
    "ariza", ["manifest", "mod", "nominal", "politika", "takvim", "donem"]
)
def test_s10_gecersiz_istekte_baslangic_ve_hesap_yok(tmp_path, monkeypatch, ariza):
    from decimal import Decimal
    from tansu import deneme

    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(makbuz.deneme_id)
    degisiklik = {}
    if ariza == "manifest":
        (tmp_path / "ag" / "s10" / "manifest.json").write_text("{}", encoding="utf-8")
    elif ariza == "nominal":
        degisiklik["risk_ayarlari"] = d["risk_ayarlari"] | dict(
            nominal_tutar=Decimal("0")
        )
    elif ariza == "politika":
        degisiklik["yontem_ayarlari"] = d["yontem_ayarlari"] | dict(
            fiyat_politikasi="legacy"
        )
    elif ariza == "takvim":
        d["veri_ayarlari"]["takvim"]["seanslar"] = ("2025-12-31", "2021-01-04")
        degisiklik["veri_ayarlari"] = d["veri_ayarlari"]
    elif ariza == "donem":
        degisiklik["donemler"] = d["donemler"][1:]
    if degisiklik:
        makbuz = s10_revizyon(depo, makbuz, **degisiklik)
    hesaplar = []
    monkeypatch.setattr(veri, "veri_hazirla", lambda *a: hesaplar.append(True))
    with pytest.raises(deneme.PilotHatasi):
        ts.kayitli_calistir(
            depo,
            makbuz.deneme_id,
            veri_koku=tmp_path,
            mod="sessiz" if ariza == "mod" else "gelistirme",
            isci=1,
            ilerleme=None,
        )
    assert hesaplar == []
    assert not any(o["kayit_turu"] == "baslangic" for o in depo.oku())


@pytest.mark.parametrize("ariza", ["seans", "uye", "isinma"])
def test_s10_eksik_kapsam_sessizce_kisalmaz(tmp_path, monkeypatch, ariza):
    from copy import deepcopy

    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)
    hazirla = veri.veri_hazirla

    def eksik(istek, *a):
        paket = deepcopy(hazirla(istek, *a))
        if istek.baslangic == "2023-01-01":
            if ariza == "seans":
                paket["gunler"].remove("2023-12-31")
            elif ariza == "uye":
                for r in paket["piyasa"]:
                    r["kalite_bayraklari"] = ["eksik"]
            else:
                paket["piyasa"] = [
                    r for r in paket["piyasa"] if r["tarih"] >= "2023-01-01"
                ]
                paket["gunler"] = [r["tarih"] for r in paket["piyasa"]]
        return paket

    monkeypatch.setattr(veri, "veri_hazirla", eksik)
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    s = sonuc["donemler"][2]
    assert s["durum"] == "hata" and s["asama"] == (
        "isinma" if ariza == "isinma" else "veri"
    )
    assert s["donem"]["bitis"].isoformat() == "2023-12-31"
    assert len([s for s in sonuc["donemler"] if s["durum"] == "tamamlandi"]) == 5


@pytest.mark.parametrize("cikis_gunu", ["2022-01-04", "2022-01-05"])
def test_s10_uyelik_girisi_engeller_acik_islemi_kapatmaz(
    tmp_path, monkeypatch, cikis_gunu
):
    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch, sinyal=True)
    uyelik = veri.uyelik_hazirla

    def degisen(istek):
        sonuc = uyelik(istek)
        if cikis_gunu in sonuc["gunler"]:
            sonuc["gunler"][cikis_gunu] = dict(semboller=[], kanitlar=[])
        return sonuc

    monkeypatch.setattr(veri, "uyelik_hazirla", degisen)
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    birlesik = sonuc["donemler"][5]
    assert sonuc["durum"] == "tamamlandi"
    if cikis_gunu == "2022-01-04":
        assert birlesik["islem_referanslari"] == []
        assert birlesik["adaylar"][0]["yurutme_nedeni"] == "giris_gunu_uye_degil"
    else:
        assert birlesik["durumlar"]["TEST"]["durum"] == "acik_son"
        assert len(birlesik["islem_referanslari"]) == 1


def test_s10_isinma_sinyali_yila_giris_acmaz(tmp_path, monkeypatch):
    depo, makbuz, piyasa = s10_kayitli(tmp_path, monkeypatch)
    for i, r in enumerate(piyasa):
        if i < 508:
            continue
        fiyat = 110.0 if i == 508 else 112.0
        for ad, fark in (("aof", 0), ("kapanis", 0), ("yuksek", 1), ("dusuk", -1)):
            r[f"duzeltilmis_{ad}"]["deger"] = fiyat + fark
        r["ham_yuksek"]["deger"] = fiyat + 1
        r["ham_dusuk"]["deger"] = fiyat - 1
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    assert sonuc["durum"] == "tamamlandi"
    assert all(
        s["adaylar"] == [] and s["islem_referanslari"] == [] for s in sonuc["donemler"]
    )
    assert all(
        s["durumlar"]["TEST"]["iz"][0]["net_sonuc"] == 0 for s in sonuc["donemler"]
    )


def test_s10_acik_yil_sonu_kismi_satisi_ve_kalani_ayri_korur(tmp_path, monkeypatch):
    depo, makbuz, piyasa = s10_kayitli(tmp_path, monkeypatch, varyant="stop_atr2")
    for i, r in enumerate(piyasa):
        fiyat = {30: 150.0, 31: 160.0, 32: 140.0, 33: 130.0}.get(i, 100.0)
        if r["tarih"] >= "2021-01-01":
            fiyat = (
                110.0
                if r["tarih"] == "2021-01-04"
                else 112.0
                if r["tarih"] < "2021-12-31"
                else 122.0
            )
        dusuk = {"2021-01-04": 100.0, "2021-01-05": 110.0}.get(r["tarih"], fiyat - 1)
        for ad, deger in (
            ("aof", fiyat),
            ("kapanis", fiyat),
            ("yuksek", fiyat + 1),
            ("dusuk", dusuk),
        ):
            r[f"duzeltilmis_{ad}"]["deger"] = deger
        r["ham_yuksek"]["deger"] = fiyat + 1
        r["ham_dusuk"]["deger"] = dusuk
        r["hacim_tl"]["deger"] = (
            500.0 if r["tarih"] in ("2021-01-04", "2021-01-05") else 100.0
        )
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    yil, birlesik = (sonuc["donemler"][i]["durumlar"]["TEST"] for i in (4, 5))
    assert sonuc["durum"] == "tamamlandi"
    assert yil["durum"] == birlesik["durum"] == "acik_son"
    assert [(d["tarih"], d["yon"], d["adet"]) for d in yil["dolumlar"]] == [
        ("2021-12-30", "alis", 352),
        ("2021-12-31", "satis", 176),
    ]
    assert yil["sonuc"]["kalan_adet"] == birlesik["sonuc"]["kalan_adet"] == 176
    assert yil["sonuc"]["net_sonuc"] == pytest.approx(1695.1352)
    assert yil["sonuc"]["net_sonuc"] == birlesik["sonuc"]["net_sonuc"]
    assert (
        len(yil["sonuc"]["gerceklesen_kismi_sonuclar"])
        == len(birlesik["sonuc"]["gerceklesen_kismi_sonuclar"])
        == 1
    )
    assert yil["sonuc"]["net_r"] is None and yil["sonuc"]["net_fiyat_getirisi"] is None
    assert yil["islemler"] == []
    assert yil["degerleme"] == dict(tarih="2021-12-31", fiyat=122.0)
    assert birlesik["degerleme"] == dict(tarih="2025-12-31", fiyat=122.0)
    kayit = depo.izle(sonuc["donemler"][4]["islem_referanslari"][0])["sonuc"]
    assert kayit["olaylar"][0]["sonuc"]["kalan_adet"] == 176
    assert kayit["olaylar"][0]["durum"] == "acik_son"


@pytest.mark.parametrize("ariza", ["git", "resmi", "deneme"])
def test_s10_kimlik_hatasi_hesap_ve_baslangic_yazmaz(tmp_path, monkeypatch, ariza):
    from tansu import deneme

    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)
    if ariza == "git":

        def git_hatasi():
            raise kayit.KayitHatasi("Git kaynağı yok")

        monkeypatch.setattr(kayit, "_git", git_hatasi)
    elif ariza == "resmi":
        commit, _ = kayit._git()
        monkeypatch.setattr(kayit, "_git", lambda: (commit, True))
    hesap = []
    monkeypatch.setattr(veri, "veri_hazirla", lambda *a: hesap.append(True))
    with pytest.raises((kayit.KayitHatasi, deneme.PilotHatasi)):
        ts.kayitli_calistir(
            depo,
            "kayitsiz" if ariza == "deneme" else makbuz.deneme_id,
            veri_koku=tmp_path,
            mod="resmi" if ariza == "resmi" else "gelistirme",
            isci=1,
            ilerleme=None,
        )
    assert hesap == []
    assert not any(o["kayit_turu"] == "baslangic" for o in depo.oku())


def test_s10_tarihli_uyelik_acigi_ilgili_cocugu_durdurur(tmp_path, monkeypatch):
    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)
    uyelik = veri.uyelik_hazirla

    def eksik(istek):
        if "2023-01-04" in istek.tarihler:
            raise veri.UyelikKapsamHatasi(istek.uyelik_surumu, ["2023-01-04"])
        return uyelik(istek)

    monkeypatch.setattr(veri, "uyelik_hazirla", eksik)
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    assert [
        (s["donem"]["ad"], s["asama"])
        for s in sonuc["donemler"]
        if s["durum"] == "hata"
    ] == [("2023", "uyelik"), ("birlesik", "uyelik")]
    assert depo.oku()[-1]["basarisiz"] == ["donem:2023", "donem:birlesik"]


def test_s10_eksik_gerekli_hedef_sinyali_basarili_bos_donem_yapmaz(
    tmp_path, monkeypatch
):
    depo, makbuz, piyasa = s10_kayitli(
        tmp_path, monkeypatch, sinyal=True, varyant="tansu"
    )
    for r in piyasa:
        if r["tarih"] == "2021-12-31":
            r["duzeltilmis_dusuk"]["deger"] = 110.0
            r["ham_dusuk"]["deger"] = 110.0
            r["hacim_tl"]["deger"] = 500.0
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    yil = sonuc["donemler"][4]
    assert yil["adaylar"], "Gerekli hedefi eksik olan gerçek E2 sinyali korunmalı"
    assert yil["durum"] == "hata", "Eksik kurulum kanıtı tamamlanmış sonuç değildir"
    assert yil["asama"] == "kurulum"
    assert yil["islem_referanslari"] == []
    assert "kurulum_eksik" in [r["neden"] for r in yil["durumlar"]["TEST"]["retler"]]


def test_s10_ilerleme_hatasi_tamamlanan_makbuzu_yok_saymaz(tmp_path, monkeypatch):
    depo, makbuz, _ = s10_kayitli(tmp_path, monkeypatch)

    def durdur(mesaj):
        raise RuntimeError("ilerleme arızası")

    with pytest.raises(RuntimeError, match="ilerleme arızası"):
        ts.kayitli_calistir(
            depo,
            makbuz.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            isci=1,
            ilerleme=durdur,
        )
    bitis = depo.oku()[-1]
    assert bitis["durum"] == "hata"
    assert bitis["tamamlanan"] == ["donem:2025"], "Yayımlanmış dönem hatada kaybolamaz"
    assert len(bitis["cikti_referanslari"]) == 1
    assert bitis["basarisiz"] == [
        "donem:2024",
        "donem:2023",
        "donem:2022",
        "donem:2021",
        "donem:birlesik",
    ]


def test_s10_kayipli_nominal_baslangic_ve_hesaptan_once_reddedilir(
    tmp_path, monkeypatch
):
    from decimal import Decimal
    from tansu import deneme

    depo, ilk, _ = s10_kayitli(tmp_path, monkeypatch)
    makbuz = s10_revizyon(
        depo,
        ilk,
        risk_ayarlari=dict(
            risk_surumu="bagimsiz_risk_v1",
            nominal_tutar=Decimal("1029.92499999999999999999"),
        ),
    )
    hazirla = veri.veri_hazirla
    hesaplar = []

    def hesap(*args):
        hesaplar.append(args[0].baslangic)
        return hazirla(*args)

    monkeypatch.setattr(veri, "veri_hazirla", hesap)
    hata = None
    try:
        s10_calistir(depo, makbuz, tmp_path)
    except deneme.PilotHatasi as yakalanan:
        hata = yakalanan
    assert hesaplar == [], "Kayıplı nominal aktarımında E1 hesabı başlayamaz"
    assert isinstance(hata, deneme.PilotHatasi)
    assert "nominal" in str(hata).lower()
    assert [o["kayit_turu"] for o in depo.oku()] == ["deneme", "deneme"]


@pytest.mark.parametrize("kayitli, beklenen", [("1029.925000", 1029.925), ("0.1", 0.1)])
def test_s10_kayipsiz_ondalik_kayitli_degeriyle_yurutulur(
    tmp_path, monkeypatch, kayitli, beklenen
):
    from decimal import Decimal

    depo, ilk, _ = s10_kayitli(tmp_path, monkeypatch, sinyal=True)
    makbuz = s10_revizyon(
        depo,
        ilk,
        risk_ayarlari=dict(
            risk_surumu="bagimsiz_risk_v1", nominal_tutar=Decimal(kayitli)
        ),
    )
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    assert sonuc["durum"] == "tamamlandi"
    assert sonuc["ayar_parmak_izi"] == makbuz.ayar_ozeti
    assert depo.deneme_oku(makbuz.deneme_id)["risk_ayarlari"][
        "nominal_tutar"
    ] == Decimal(kayitli)
    for donem in sonuc["donemler"]:
        assert donem["durumlar"]["TEST"]["yurutme"]["nominal_tutar"] == beklenen
        iz = depo.izle(donem["makbuz"].olay_id)
        assert (
            iz["baslangic"]["ayar_parmak_izi"]
            == iz["sonuc"]["ayar_parmak_izi"]
            == makbuz.ayar_ozeti
        )


def test_s10_baslangic_makbuzu_farkli_ayara_bagliysa_hesap_baslamaz(
    tmp_path, monkeypatch
):
    from decimal import Decimal
    from tansu import deneme

    depo, ilk, _ = s10_kayitli(tmp_path, monkeypatch)
    yeni = s10_revizyon(
        depo,
        ilk,
        risk_ayarlari=dict(
            risk_surumu="bagimsiz_risk_v1", nominal_tutar=Decimal("200000")
        ),
    )
    yeni_ayar = depo.deneme_oku(yeni.deneme_id)["risk_ayarlari"]
    oku = depo.deneme_oku
    hazirla = veri.veri_hazirla
    okumalar, hesaplar = [], []

    def degisen_kayit(deneme_id):
        kayit = oku(deneme_id)
        okumalar.append(kayit["ayar_parmak_izi"])
        if len(okumalar) == 1:
            olaylar = depo.oku()
            for olay in olaylar:
                if (
                    olay["kayit_turu"] == "deneme"
                    and olay["deneme_id"] == ilk.deneme_id
                ):
                    olay["risk_ayarlari"] = yeni_ayar
                    olay["ayar_parmak_izi"] = yeni.ayar_ozeti
            depo.yol.write_bytes(b"".join(deneme.kanonik(o) + b"\n" for o in olaylar))
        return kayit

    def hesap(*args):
        hesaplar.append(args[0].baslangic)
        return hazirla(*args)

    monkeypatch.setattr(depo, "deneme_oku", degisen_kayit)
    monkeypatch.setattr(veri, "veri_hazirla", hesap)
    hata = None
    try:
        s10_calistir(depo, ilk, tmp_path)
    except deneme.PilotHatasi as yakalanan:
        hata = yakalanan
    assert okumalar == [ilk.ayar_ozeti, yeni.ayar_ozeti]
    assert hesaplar == [], "Başlangıç makbuzuyla uyuşmayan ayar hesaplanamaz"
    assert isinstance(hata, deneme.PilotHatasi)
    olaylar = deneme.PilotKayit(depo.yol).oku()
    assert [o["kayit_turu"] for o in olaylar] == [
        "deneme",
        "deneme",
        "baslangic",
        "bitis",
    ]
    assert olaylar[-2]["ayar_parmak_izi"] == yeni.ayar_ozeti
    assert olaylar[-1]["durum"] == "hata"
    assert olaylar[-1]["tamamlanan"] == []
    assert olaylar[-1]["basarisiz"] == [
        "donem:2025",
        "donem:2024",
        "donem:2023",
        "donem:2022",
        "donem:2021",
        "donem:birlesik",
    ]


def test_s11_bir_cocugun_bozdugu_paket_diger_cocuga_gecmez(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor

    # Aynı süreçte E2 arızası enjekte edilir; gerçek spawn yolu diğer S11 testlerindedir.
    monkeypatch.setattr(
        ts.concurrent.futures,
        "ProcessPoolExecutor",
        lambda *, max_workers, mp_context: ThreadPoolExecutor(max_workers=max_workers),
    )
    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    kurulum = aileler.ortak_donem_kurulumu
    girisler = []

    def bozulan(paket, strateji):
        min_gun = next(a.deger for a in strateji.parametreler if a.ad == "min_gun")
        girisler.append((min_gun, len(paket["piyasa"])))
        if min_gun == 2:
            paket["piyasa"].clear()
            raise ValueError("çocuk kurulumu başarısız")
        return kurulum(paket, strateji)

    monkeypatch.setattr(aileler, "ortak_donem_kurulumu", bozulan)
    sonuc = s11_calistir(depo, makbuz, tmp_path)
    assert len(girisler) == 18 and all(sayi > 0 for _, sayi in girisler)
    assert sonuc["hucreler"][0]["durum"] == "eksik"
    assert [h["durum"] for h in sonuc["hucreler"][1:]] == ["islemsiz", "islemsiz"]
    assert all(len(h["donemler"]) == 6 for h in sonuc["hucreler"])
    assert all(
        b["hucreler"][0]["kapali_islem_sayisi"] is None for b in sonuc["bolgeler"]
    )
    assert all(b["secilen"] is None for b in sonuc["bolgeler"])


def test_s11_tum_cocuk_kayitlari_ilk_baslangic_ve_e1_oncesindedir(
    tmp_path, monkeypatch
):
    from contextlib import contextmanager
    from tansu import deneme

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    kosu, hazirla = depo.kosu, veri.veri_hazirla
    baslangic_kayitlari, e1_kayitlari = [], []

    def cocuk_sayisi():
        okuyucu = deneme.PilotKayit(depo.yol)
        cocuklar = [
            o
            for o in okuyucu.oku()
            if o["kayit_turu"] == "deneme" and o["ust_deneme_id"] == makbuz.deneme_id
        ]
        assert all(
            o["baglar"]["izgara_ust_deneme"] == makbuz.deneme_id for o in cocuklar
        )
        assert len({o["deneme_id"] for o in cocuklar}) == len(cocuklar)
        return len(cocuklar)

    @contextmanager
    def baslat(deneme_id, **secenekler):
        if deneme_id != makbuz.deneme_id:
            baslangic_kayitlari.append(cocuk_sayisi())
        with kosu(deneme_id, **secenekler) as tutacak:
            yield tutacak

    def hesap(*args):
        e1_kayitlari.append(cocuk_sayisi())
        return hazirla(*args)

    monkeypatch.setattr(depo, "kosu", baslat)
    monkeypatch.setattr(veri, "veri_hazirla", hesap)
    sonuc = s11_calistir(depo, makbuz, tmp_path)
    assert baslangic_kayitlari == [3, 3, 3], (
        "Bütün çocuklar ilk çocuk koşusundan önce kaydedilmeli"
    )
    assert e1_kayitlari == [3] * 6, (
        "Bütün çocuk kayıtları ilk E1 çağrısından önce kalıcı olmalı"
    )
    assert [h["durum"] for h in sonuc["hucreler"]] == ["islemsiz"] * 3


@pytest.mark.parametrize("ariza", ["yazma", "kayit", "dogrulama", "ozet"])
def test_s11_ikinci_kayit_hatasi_tum_yurutmeyi_engeller(tmp_path, monkeypatch, ariza):
    from contextlib import contextmanager
    from copy import deepcopy
    from decimal import Decimal
    from tansu import deneme

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    kaydet, oku, kosu, hazirla = (
        depo.deneme_kaydet,
        depo.deneme_oku,
        depo.kosu,
        veri.veri_hazirla,
    )
    kayitlar, baslangiclar, hesaplar = [], [], []

    def kayit(*args, **secenekler):
        if secenekler.get("ust_deneme") == makbuz.deneme_id:
            kayitlar.append(args[0])
            if len(kayitlar) == 2 and ariza not in ("dogrulama", "ozet"):
                tur = (
                    deneme.PilotYazmaHatasi if ariza == "yazma" else deneme.PilotHatasi
                )
                raise tur("ikinci çocuk kaydı başarısız")
        return kaydet(*args, **secenekler)

    def degisen_okuma(deneme_id):
        d = oku(deneme_id)
        if d["ust_deneme_id"] == makbuz.deneme_id and ariza in ("dogrulama", "ozet"):
            min_gun = next(
                a["deger"]
                for a in d["strateji"]["parametreler"]
                if a["ad"] == "min_gun"
            )
            if min_gun == 3:
                d = deepcopy(d)
                if ariza == "dogrulama":
                    d["risk_ayarlari"]["nominal_tutar"] = Decimal("200000")
                else:
                    d["ayar_parmak_izi"] = "farkli-tam-ozet"
        return d

    @contextmanager
    def baslat(deneme_id, **secenekler):
        if deneme_id != makbuz.deneme_id:
            baslangiclar.append(deneme_id)
        with kosu(deneme_id, **secenekler) as tutacak:
            yield tutacak

    def hesap(*args):
        hesaplar.append(args[0])
        return hazirla(*args)

    monkeypatch.setattr(depo, "deneme_kaydet", kayit)
    monkeypatch.setattr(depo, "deneme_oku", degisen_okuma)
    monkeypatch.setattr(depo, "kosu", baslat)
    monkeypatch.setattr(veri, "veri_hazirla", hesap)
    sonuc, hata = None, None
    try:
        sonuc = s11_calistir(depo, makbuz, tmp_path)
    except (deneme.PilotYazmaHatasi, deneme.PilotHatasi) as yakalanan:
        hata = yakalanan
        sonuc = getattr(hata, "sonuc", None)
    assert baslangiclar == [], "Kayıt geçişi bitmeden hiçbir çocuk koşusu başlamamalı"
    assert hesaplar == [], "İkinci kayıt başarısızsa ilk çocuk da hesaplanmamalı"
    assert sonuc is not None, (
        "Kayıt geçişi hatası doğrulanmış makbuzları ve yuvaları korumalı"
    )
    assert len(sonuc["hucreler"]) == 3
    assert sum(len(h["donemler"]) for h in sonuc["hucreler"]) == 18
    assert all(h["kosu_id"] is None for h in sonuc["hucreler"])
    assert all(
        d["durum"] == "baslamadi" and d["neden"]
        for h in sonuc["hucreler"]
        for d in h["donemler"]
    )
    ilk = sonuc["hucreler"][0]
    assert ilk["kayit_makbuzu"]["deneme_id"] == ilk["deneme_id"]
    okuyucu = deneme.PilotKayit(depo.yol)
    gercek = okuyucu.deneme_oku(ilk["deneme_id"])
    assert gercek["ayar_parmak_izi"] == ilk["kayit_makbuzu"]["ayar_ozeti"]
    assert gercek["ust_deneme_id"] == makbuz.deneme_id
    assert not any(
        o["kayit_turu"] == "baslangic" and o["deneme_id"] != makbuz.deneme_id
        for o in okuyucu.oku()
    )
    if ariza == "yazma":
        assert isinstance(hata, ts.AramaYazmaHatasi)
        assert sonuc["sonuc_makbuzu"] is None and sonuc["bitis_makbuzu"] is None
    elif ariza == "dogrulama":
        assert "tam ayarı" in sonuc["hucreler"][1]["neden"]
    if ariza in ("dogrulama", "ozet"):
        assert sonuc["hucreler"][1]["kayit_makbuzu"]


@pytest.mark.parametrize("ariza", ["kapsam", "e1_hatasi", "manifest", "uyelik"])
def test_s11_eksik_kapsam_paketi_paylasilir_diger_hatalar_paylasilmaz(
    tmp_path, monkeypatch, ariza
):
    from collections import Counter
    from concurrent.futures import ThreadPoolExecutor
    from copy import deepcopy
    from tansu import deneme, saglamlik

    depo, makbuz, _ = s11_kayitli(tmp_path, monkeypatch)
    hazirla = veri.veri_hazirla
    kurulum, yurut = aileler.ortak_donem_kurulumu, saglamlik.ema_hucre_calistir
    istekler, hesaplar = [], []

    def eksik(istek, *args):
        istekler.append((istek.baslangic, istek.bitis))
        if ariza == "e1_hatasi":
            raise veri.VeriHatasi("E1 hazırlığı başarısız")
        paket = deepcopy(hazirla(istek, *args))
        if ariza == "manifest":
            paket["referans"]["manifest_parmak_izi"] = "farkli-manifest"
        elif ariza == "uyelik":
            paket["uyelik"]["tablo_parmak_izi"] = "farkli-uyelik"
        else:
            satir = next(
                r
                for r in paket["piyasa"]
                if istek.baslangic <= r["tarih"] <= istek.bitis
            )
            satir["kalite_bayraklari"] = ["eksik"]
            paket["kalite"]["hata_nedenleri"].append("gerekli fiyat satırı eksik")
        return paket

    def e2(*args, **secenekler):
        hesaplar.append("E2")
        return kurulum(*args, **secenekler)

    def e3(*args, **secenekler):
        hesaplar.append("E3")
        return yurut(*args, **secenekler)

    monkeypatch.setattr(
        ts.concurrent.futures,
        "ProcessPoolExecutor",
        lambda *, max_workers, mp_context: ThreadPoolExecutor(max_workers=max_workers),
    )
    monkeypatch.setattr(veri, "veri_hazirla", eksik)
    monkeypatch.setattr(aileler, "ortak_donem_kurulumu", e2)
    monkeypatch.setattr(saglamlik, "ema_hucre_calistir", e3)
    sonuc = s11_calistir(depo, makbuz, tmp_path)
    tekrarlar = Counter(istekler)
    assert len(istekler) == (6 if ariza == "kapsam" else 18), (
        "Yalnız kimliği doğrulanmış E1 paketi tekrar kullanılmalı"
    )
    assert len(tekrarlar) == 6
    assert set(tekrarlar.values()) == ({1} if ariza == "kapsam" else {3})
    assert hesaplar == [], "Kapsam veya kimlik geçersizken E2/E3 başlamamalı"
    assert len(sonuc["hucreler"]) == 3
    assert sum(len(h["donemler"]) for h in sonuc["hucreler"]) == 18
    okuyucu = deneme.PilotKayit(depo.yol)
    for h in sonuc["hucreler"]:
        assert h["durum"] == "eksik"
        for d in h["donemler"]:
            assert d["durum"] == "eksik" and d["asama"] == "veri"
            assert d["neden"] and not d["islem_referanslari"]
            assert okuyucu.izle(d["sonuc_ref"])["sonuc"]["deneme_id"] == h["deneme_id"]
    assert sonuc["durum"] == "hata"
    assert all(b["secilen"] is None for b in sonuc["bolgeler"])


def s12_kayitli(tmp_path, monkeypatch, *, varyant="bugun"):
    """S12: gerçek E2/E3/E5; yalnız E1 piyasa sınırı sentetiktir."""
    import datetime as dt
    from copy import deepcopy
    from tests.test_kayit import pilot_deneme

    depo, eski, piyasa = s10_kayitli(tmp_path, monkeypatch, varyant=varyant)
    d = depo.deneme_oku(eski.deneme_id)
    gunler = [
        f"{y}-{a:02d}-{g:02d}"
        for y in range(2021, 2026)
        for a in (1, 4, 7, 10)
        for g in (4, 5)
    ]
    temel = deepcopy(piyasa[0])
    piyasa[:] = [r for r in piyasa if r["tarih"] < "2021-01-01"]
    piyasa.extend(dict(deepcopy(temel), tarih=t) for t in gunler)
    d["veri_ayarlari"]["takvim"]["seanslar"] = tuple(gunler)
    donemler = []
    for y in range(2022, 2026):
        for q, a in enumerate((1, 4, 7, 10), 1):
            bas = dt.date(y, a, 1)
            sonraki = dt.date(y + (a == 10), 1 if a == 10 else a + 3, 1)
            egitim = dict(
                ad=f"{y}Q{q}:egitim",
                baslangic=dt.date(y - 1, a, 1),
                bitis=bas - dt.timedelta(days=1),
                isinma_baslangici=dt.date(2018, 1, 1),
                sinir_surumu="surekli_ileri_v1",
            )
            donemler.append(
                dict(
                    ad=f"{y}Q{q}",
                    baslangic=bas,
                    bitis=sonraki - dt.timedelta(days=1),
                    isinma_baslangici=dt.date(2018, 1, 1),
                    sinir_surumu="surekli_ileri_v1",
                    egitim=egitim,
                )
            )
    yontem = dict(
        yontem="kayitli_ileri_v1",
        tekrar=0,
        egitim_ay=12,
        test_ay=3,
        adim_ay=3,
        secim_politikasi="genis_bolge_net_r_v1",
        olcu_politikasi="bagimsiz_olcu_v1",
        eksenler=[dict(ad="min_gun", birim="gun", degerler=[2, 3, 5])],
        hucre_yontemi=d["yontem_ayarlari"],
        veri_gorulme_durumu="incelenmis_gecmis",
    )
    m = pilot_deneme(
        depo,
        d["strateji"],
        donemler=donemler,
        yontem_ayarlari=yontem,
        **{k: d[k] for k in ("veri_ayarlari", "risk_ayarlari", "masraf_ayarlari")},
    )
    return depo, m, piyasa


def s12_calistir(depo, makbuz, kok):
    giris = getattr(ts, "kayitli_ileri_calistir", None)
    assert callable(giris), "S12 genel ileri yürüme girişi gereklidir"
    return giris(depo, makbuz.deneme_id, veri_koku=kok, mod="gelistirme", ilerleme=None)


def test_s12_onalti_secimsiz_ceyrek_ve_gercek_makbuzlar(tmp_path, monkeypatch):
    depo, m, _ = s12_kayitli(tmp_path, monkeypatch)
    r = s12_calistir(depo, m, tmp_path)
    assert r["durum"] == "tamamlandi"
    assert [b["bolum_id"] for b in r["bolumler"]] == [
        "2022Q1",
        "2022Q2",
        "2022Q3",
        "2022Q4",
        "2023Q1",
        "2023Q2",
        "2023Q3",
        "2023Q4",
        "2024Q1",
        "2024Q2",
        "2024Q3",
        "2024Q4",
        "2025Q1",
        "2025Q2",
        "2025Q3",
        "2025Q4",
    ]
    assert all(s["durum"] == "secim_yok" for b in r["bolumler"] for s in b["secimler"])
    assert r["veri_gorulme_durumu"] == "incelenmis_gecmis"
    assert r["islemler"] == []
    olaylar = depo.oku()
    for b in r["bolumler"]:
        secim = next(
            o for o in olaylar if o["kayit_id"] == b["secimler"][0]["secim_ref"]
        )
        assert secim["kayit_turu"] == "ileri_secim"
        assert len(secim["kayit"]["egitim_cocuklari"]) == 3
        assert secim["kayit"]["egitim_kesimi"] < b["donem"]["baslangic"]
    bitis = next(o for o in olaylar if o["kayit_id"] == r["bitis_makbuzu"].olay_id)
    assert bitis["tamamlanan"] == [b["bolum_id"] for b in r["bolumler"]] + ["birlesik"]
    assert bitis["basarisiz"] == []


def test_s12_secim_kayit_hatasi_test_hesabini_baslatmaz(tmp_path, monkeypatch):
    from tansu import deneme

    depo, m, _ = s12_kayitli(tmp_path, monkeypatch)
    giris = getattr(ts, "kayitli_ileri_calistir", None)
    assert callable(giris), "S12 genel ileri yürüme girişi gereklidir"
    asil = depo._ekle
    test_istekleri = []
    hazirla = veri.veri_hazirla

    def yaz(o, *a):
        if o["kayit_turu"] == "ileri_secim":
            raise deneme.PilotYazmaHatasi("secim diski")
        return asil(o, *a)

    def veri_al(istek, *a):
        if istek.baslangic == "2022-01-01":
            test_istekleri.append(istek)
        return hazirla(istek, *a)

    monkeypatch.setattr(depo, "_ekle", yaz)
    monkeypatch.setattr(veri, "veri_hazirla", veri_al)
    with pytest.raises(deneme.PilotYazmaHatasi, match="secim diski") as hata:
        s12_calistir(depo, m, tmp_path)
    assert test_istekleri == []
    assert hata.value.sonuc["bolumler"][0]["durum"] == "baslamadi"
    assert any(o["kayit_turu"] == "sonuc" for o in depo.oku())


def s12_sinyalli(tmp_path, monkeypatch, *, son_sinyal="2025-10-05"):
    depo, m, piyasa = s12_kayitli(tmp_path, monkeypatch, varyant="stop_atr2")
    tarihler = pd.DatetimeIndex(
        ["2021-01-04", "2021-10-05", "2022-01-05", "2024-10-04", son_sinyal]
    )

    def kurulum(f, p):
        t = tarihler.intersection(f.index)
        return pd.DataFrame(dict(kutu_alt=95.0, kutu_ust=101.0, hedef=110.0), index=t)

    monkeypatch.setattr(aileler, "kurulum", kurulum)
    for r in piyasa:
        fiyat = (
            110.0 if r["tarih"] in ("2021-04-04", "2022-07-04", "2025-01-04") else 100.0
        )
        for ad, fark in (("aof", 0), ("kapanis", 0), ("yuksek", 1), ("dusuk", -1)):
            r[f"duzeltilmis_{ad}"]["deger"] = fiyat + fark
        r["ham_yuksek"]["deger"], r["ham_dusuk"]["deger"] = fiyat + 1, fiyat - 1
    return depo, m, piyasa


def test_s12_bekleyen_ve_acik_islem_secimsiz_ceyrekte_surur_tek_kohort(
    tmp_path, monkeypatch
):
    depo, m, _ = s12_sinyalli(tmp_path, monkeypatch)
    r = s12_calistir(depo, m, tmp_path)
    assert r["durum"] == "tamamlandi", [
        (b["bolum_id"], b["neden"]) for b in r["bolumler"]
    ]
    olaylar = depo.oku()
    kontroller = [o for o in olaylar if o["kayit_turu"] == "ileri_kontrol"]
    q1, q2, q3 = [o["durum"] for o in kontroller[:3]]
    assert q1["durum"] == "bekliyor"
    assert q2["durum"] == "acik_son"
    assert r["bolumler"][1]["secimler"][0]["durum"] == "secim_yok"
    assert (
        q1["pozisyon"]["risk_girdisi"]["sinyal_id"]
        == q2["pozisyon"]["risk_girdisi"]["sinyal_id"]
    )
    assert q1["pozisyon"]["ayar"] == q2["pozisyon"]["ayar"]
    assert q3["islemler"][0]["pozisyon"]["giris_tarih"] == "2022-04-04"
    assert q3["islemler"][0]["pozisyon"]["cikis_tarih"] == "2022-07-04"
    i = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "islem" and o.get("islem_turu") == "ileri_islem_v1"
    )
    assert (i["karar_bolumu"], i["giris_kohortu"], i["rol"]) == (
        "2022Q1",
        "2022Q2",
        "tamamlanmis_islem",
    )
    assert len([o for o in olaylar if o.get("islem_id") == i["islem_id"]]) == 1
    assert kontroller[-1]["durum"]["durum"] == "bekliyor"
    assert kontroller[-1]["durum"]["son_tarih"] == "2025-10-05"
    assert all(o["rol"] != "acik_ufuk" for o in r["islemler"])
    secim = r["bolumler"][0]["secimler"][0]
    assert secim["durum"] == "secildi"
    assert all(h["kapali_islem_sayisi"] == 1 for h in secim["egitim_cocuklari"])
    assert all(
        h["dislanan"][0]["durum"] == "bekliyor" for h in secim["egitim_cocuklari"]
    )
    ilk_test = next(o for o in olaylar if o["kayit_turu"] == "ileri_sinyal")
    assert olaylar.index(
        next(o for o in olaylar if o["kayit_id"] == secim["secim_ref"])
    ) < olaylar.index(ilk_test)
    birlesik = next(o for o in olaylar if o["kayit_id"] == r["sonuc_makbuzu"].olay_id)[
        "kayit"
    ]
    assert len({e["olay_id"] for e in birlesik["olaylar"]}) == len(birlesik["olaylar"])
    assert all(e["tarih"] <= "2025-12-31" for e in birlesik["olaylar"])


@pytest.mark.parametrize("giris", ["kayitli_calistir", "kayitli_izgara_calistir"])
def test_s12_legacy_yuzler_ceyrek_yontemini_kabul_etmez(tmp_path, monkeypatch, giris):
    from tansu import deneme

    depo, m, _ = s12_kayitli(tmp_path, monkeypatch)
    once = depo.yol.read_bytes()
    with pytest.raises(deneme.PilotHatasi, match="Desteklenmeyen"):
        getattr(ts, giris)(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", isci=1
        )
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize("boz", ["yontem", "pencere", "takvim"])
def test_s12_eksik_yontem_baslangic_ve_hesaptan_once_reddedilir(
    tmp_path, monkeypatch, boz
):
    from tansu import deneme

    depo, m, _ = s12_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(m.deneme_id)
    if boz == "yontem":
        d["yontem_ayarlari"]["gizli"] = True
    elif boz == "pencere":
        d["donemler"][0]["egitim"]["baslangic"] = __import__("datetime").date(
            2020, 1, 1
        )
    else:
        d["veri_ayarlari"]["takvim"]["seanslar"] = tuple(
            t
            for t in d["veri_ayarlari"]["takvim"]["seanslar"]
            if not t.startswith("2022-04")
        )
    from tests.test_kayit import pilot_deneme

    once = depo.yol.read_bytes()
    with pytest.raises(deneme.PilotHatasi):
        m = pilot_deneme(
            depo,
            d["strateji"],
            **{
                k: d[k]
                for k in (
                    "donemler",
                    "yontem_ayarlari",
                    "veri_ayarlari",
                    "risk_ayarlari",
                    "masraf_ayarlari",
                )
            },
        )
        s12_calistir(depo, m, tmp_path)
    assert depo.yol.read_bytes() == once


def test_s12_uyelikten_cikan_hissenin_acik_islemi_kaybolmaz(tmp_path, monkeypatch):
    from copy import deepcopy

    depo, m, _ = s12_sinyalli(tmp_path, monkeypatch)
    asil = veri.veri_hazirla

    def uyelik(istek):
        return dict(
            gunler={
                t: dict(
                    semboller=["DIGER", "TEST"] if t < "2022-07-01" else ["DIGER"],
                    kanitlar=[],
                )
                for t in istek.tarihler
            },
            tablo_parmak_izi="uyelik-fixture",
            evren_politikasi="donemsel_bist30_v1",
            uyelik_surumu="bist30_2021_2025_v1",
        )

    def hazirla(istek, *a):
        p = asil(istek, *a)
        p["piyasa"] = [
            dict(deepcopy(r), sembol=s) for s in istek.semboller for r in p["piyasa"]
        ]
        p["semboller"] = list(istek.semboller)
        p["uyelik"] = uyelik(
            veri.UyelikIstegi(
                tuple(t for t in p["gunler"] if istek.baslangic <= t <= istek.bitis),
                istek.evren_politikasi,
                istek.uyelik_surumu,
            )
        )
        return p

    monkeypatch.setattr(veri, "uyelik_hazirla", uyelik)
    monkeypatch.setattr(veri, "veri_hazirla", hazirla)
    r = s12_calistir(depo, m, tmp_path)
    assert r["durum"] == "tamamlandi", [
        (b["bolum_id"], b["neden"]) for b in r["bolumler"]
    ]
    kontroller = [
        o
        for o in depo.oku()
        if o["kayit_turu"] == "ileri_kontrol" and o["sembol"] == "TEST"
    ]
    assert [o["bolum_id"] for o in kontroller] == ["2022Q1", "2022Q2", "2022Q3"]
    assert (
        kontroller[-1]["durum"]["islemler"][0]["pozisyon"]["cikis_tarih"]
        == "2022-07-04"
    )


@pytest.mark.parametrize("eksik", ["isinma", "limit_kaniti"])
def test_s12_eksik_egitim_basarili_secimsiz_donem_degildir(
    tmp_path, monkeypatch, eksik
):
    from tests.test_kayit import pilot_deneme

    depo, m, piyasa = s12_sinyalli(tmp_path, monkeypatch)
    piyasa[:] = [r for r in piyasa if r["tarih"] != "2022-01-04"]
    if eksik == "isinma":
        d = depo.deneme_oku(m.deneme_id)
        d["donemler"][0]["egitim"]["isinma_baslangici"] = __import__("datetime").date(
            2020, 1, 1
        )
        m = pilot_deneme(
            depo,
            d["strateji"],
            **{
                k: d[k]
                for k in (
                    "donemler",
                    "yontem_ayarlari",
                    "veri_ayarlari",
                    "risk_ayarlari",
                    "masraf_ayarlari",
                )
            },
        )
    else:
        for r in piyasa:
            r.pop("limit_kaniti", None)
    r = s12_calistir(depo, m, tmp_path)
    secim = r["bolumler"][0]["secimler"][0]
    assert secim["durum"] == "eksik"
    olaylar = depo.oku()
    for h in secim["egitim_cocuklari"]:
        sonuc = next(o for o in olaylar if o["kayit_id"] == h["sonuc_ref"])
        assert any(e["asama"] == eksik for e in sonuc["icerik"]["hatalar"])
    assert r["durum"] == "hata"


def test_grup_hazirla_komutu_eksikleri_kaydeder_sinama_baslatmaz(tmp_path, capsys):
    tanim = tmp_path / "grup.json"
    tanim.write_text(
        json.dumps({"grup_id": "ilk-grup", "revizyon": "taslak-1"}),
        encoding="utf-8",
    )
    yol = tmp_path / "grup-hazirlik.jsonl"
    try:
        kod = komut.main(
            [
                "grup-hazirla",
                "--grup-tanimi",
                str(tanim),
                "--deneme-dosyasi",
                str(yol),
                "--kok",
                str(tmp_path),
            ]
        )
    except SystemExit as hata:
        kod = hata.code
    assert kod == 1, "Engelli hazırlık kalıcı kayıtla çıkış 1 vermelidir."
    from tansu import deneme

    olaylar = deneme.PilotKayit(yol).oku()
    assert [o["kayit_turu"] for o in olaylar] == ["grup_hazirligi"]
    assert olaylar[0]["hazirlik_durumu"] == "engelli"
    assert olaylar[0]["yurutme_izni"] is False
    assert {e["alan"] for e in olaylar[0]["engeller"]} >= {
        "soru",
        "strateji_revizyonlari",
        "seanslar",
        "referanslar.anlik_goruntu",
    }
    assert json.loads(capsys.readouterr().out)["kayit_id"] == olaylar[0]["kayit_id"]


def grup_hazirlik_girdisi(tmp_path):
    from hashlib import sha256

    gunler = pd.bdate_range("2021-03-29", periods=4)
    seri = [mum(g, 100, 101, 99, 1e9) for g in gunler]
    a = anlik_hazirla(tmp_path, {s: seri for s in ("AKBNK", "MGROS", "SASA")})
    kaynak = tmp_path / "kaynak.md"
    kaynak.write_text("Kaynak tanımı eksiktir.", encoding="utf-8")
    takvim = tmp_path / "takvim.json"
    takvim.write_text(
        json.dumps(
            dict(
                baslangic="2021-03-29",
                bitis="2021-04-01",
                seanslar=["2021-03-29", "2021-03-30", "2021-03-31", "2021-04-01"],
                kaynak_ref="sentetik kesin takvim kanıtı",
            )
        ),
        encoding="utf-8",
    )

    def ref(yol):
        return dict(yol=str(yol), sha256=sha256(yol.read_bytes()).hexdigest())

    uyelik = veri.uyelik_hazirla(
        veri.UyelikIstegi(
            ("2021-03-30", "2021-03-31", "2021-04-01"),
            "donemsel_bist30_v1",
            "bist30_2021_2025_v1",
        )
    )
    return dict(
        grup_id="ilk-grup",
        revizyon="1",
        soru="İlk kaynağın açık alanları neler?",
        strateji_revizyonlari=[
            dict(
                revizyon_ref="kaynak-a",
                kaynak=ref(kaynak),
                yayim_tarihi="2025-12-19",
                deneme_id=None,
                eksik_alanlar=[],
            )
        ],
        seanslar=["2021-03-30", "2021-03-31", "2021-04-01"],
        isinma_baslangici="2021-03-29",
        hisse_kurali=dict(
            semboller=["AKBNK", "MGROS", "SASA"],
            evren_politikasi="donemsel_bist30_v1",
            uyelik_surumu="bist30_2021_2025_v1",
        ),
        referanslar=dict(
            anlik_goruntu=a.kimlik,
            manifest_ozeti=ref(tmp_path / "ag" / a.kimlik / "manifest.json")["sha256"],
            uyelik_ozeti=uyelik["tablo_parmak_izi"],
            kod_ozeti=ts.grup_kod_ozeti(),
            takvim=ref(takvim),
            yontem=ref(kaynak),
            risk=ref(kaynak),
            masraf=ref(kaynak),
        ),
        gozlem_durumu="kesif",
        durdurma_kurali="Teknik hata durdurur.",
    )


def test_grup_statik_kontrol_hesap_cagirmaz_ve_uyelik_dislamasini_korur(
    tmp_path, monkeypatch
):
    from tansu import deneme

    tanim = grup_hazirlik_girdisi(tmp_path)

    def yasak(*a, **k):
        pytest.fail("Hazırlık hesaplama, indirme veya süreç başlatamaz.")

    for nesne, ad in (
        (veri, "veri_hazirla"),
        (veri, "indir"),
        (ts, "calistir"),
        (ts, "kayitli_calistir"),
        (ts, "kayitli_izgara_calistir"),
        (aileler, "ortak_donem_kurulumu"),
        (motor, "tara"),
        (ts.subprocess, "run"),
        (deneme.PilotKayit, "kosu"),
        (deneme.PilotKayit, "deneme_kaydet"),
    ):
        monkeypatch.setattr(nesne, ad, yasak)
    depo = deneme.PilotKayit(tmp_path / "hazirlik.jsonl")
    sonuc = ts.grup_hazirla(depo, tanim, veri_koku=tmp_path)
    assert sonuc["hazirlik_durumu"] == "engelli"
    assert sonuc["engeller"] == [
        dict(
            alan="strateji_revizyonlari.kaynak-a.deneme_id",
            neden="Tam çözülmüş kaynak strateji revizyonu yok.",
        )
    ]
    assert sonuc["dislamalar"] == [
        dict(sembol="SASA", tarih="2021-03-30", neden="bist30_uyesi_degil"),
        dict(sembol="SASA", tarih="2021-03-31", neden="bist30_uyesi_degil"),
        dict(sembol="MGROS", tarih="2021-04-01", neden="bist30_uyesi_degil"),
    ]
    assert sonuc["tanim"] == tanim
    assert [o["kayit_turu"] for o in depo.oku()] == ["grup_hazirligi"]


@pytest.mark.parametrize(
    "ariza",
    [
        "takvim",
        "manifest",
        "uyelik",
        "kaynak",
        "kod",
        "eksik_veri",
        "tamamlanmamis",
        "legacy",
    ],
)
def test_grup_eksik_kaniti_adlandirir_donemi_daraltmaz(tmp_path, ariza):
    from tansu import deneme
    from tests.test_kayit import pilot_deneme

    tanim = grup_hazirlik_girdisi(tmp_path)
    depo = deneme.PilotKayit(tmp_path / "hazirlik.jsonl")
    alan = None
    if ariza == "takvim":
        tanim["seanslar"].remove("2021-03-31")
        alan = "referanslar.takvim"
    elif ariza == "manifest":
        tanim["referanslar"]["manifest_ozeti"] = "farkli"
        alan = "referanslar.anlik_goruntu"
    elif ariza == "uyelik":
        tanim["referanslar"]["uyelik_ozeti"] = "farkli"
        alan = "hisse_kurali.uyelik"
    elif ariza == "kaynak":
        tanim["strateji_revizyonlari"][0]["kaynak"]["sha256"] = "0" * 64
        alan = "strateji_revizyonlari.kaynak-a.kaynak"
    elif ariza == "kod":
        tanim["referanslar"]["kod_ozeti"] = "farkli"
        alan = "referanslar.kod_ozeti"
    elif ariza == "eksik_veri":
        tanim["hisse_kurali"]["semboller"].append("EREGL")
        alan = "veri_kapsami.EREGL"
    elif ariza == "tamamlanmamis":
        tanim["seanslar"] = ["2099-01-02"]
        alan = "seanslar"
    else:
        tanim["strateji_revizyonlari"][0]["deneme_id"] = pilot_deneme(depo).deneme_id
        alan = "strateji_revizyonlari.kaynak-a.deneme_id"
    sonuc = ts.grup_hazirla(depo, tanim, veri_koku=tmp_path)
    assert sonuc["hazirlik_durumu"] == "engelli"
    assert alan in {e["alan"] for e in sonuc["engeller"]}
    if ariza == "legacy":
        assert "kaynak seçim izni taşımaz" in sonuc["engeller"][0]["neden"]
    assert sonuc["tanim"]["seanslar"] == tanim["seanslar"]
    assert not any(
        o["kayit_turu"] in ("baslangic", "sonuc", "bitis") for o in depo.oku()
    )
