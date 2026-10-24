"""Tansu sınaması yüzü (TASARIM 5.14): işlem getirisi, Tansu ölçüleri, sağlam bölge, ileri yürüme, işçi sayısı, koşu.

Masraf m = 0,001 (her yönde %0,10). Beklenen değerler elle hesaplanmıştır (her testin yorumunda).

EMA verisi: tests/test_saglamlik.py'deki seri (26.01.2026'dan 8 gün; son kapanış 110). Sinyal gün 5 (02.02, kapanış 103),
giriş 03.02 AOF 104, çıkış 04.02 son kapanış 110 (veri sonu). Dönem 02.02-04.02 (3 gün).
Çift verisi: A, B, C 270 işlem günü (2025-01-01'den). B ve C 100'de sabit; A 255-261. günler 95, sonra 100.
"""

import dataclasses
import datetime as dt
from decimal import Decimal
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


def s10_kayitli(
    tmp_path,
    monkeypatch,
    *,
    sinyal=False,
    limit=True,
    varyant="bugun",
    kilit_politikasi=None,
):
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
    if kilit_politikasi is not None:
        y["kilit_politikasi"] = kilit_politikasi
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


def s13_kayitli(
    tmp_path,
    monkeypatch,
    *,
    sinyalli=True,
    eksenler=None,
    kilit_politikasi=None,
    hedef_yoklugu=False,
    ayni_gun=False,
):
    """E1 sözleşme verisi; kaynak WF ile MC hesap/kayıt sahipleri gerçektir."""
    import datetime as dt
    from tansu import deneme

    depo, wf, piyasa = (s12_sinyalli if sinyalli else s12_kayitli)(
        tmp_path,
        monkeypatch,
        kilit_politikasi=kilit_politikasi,
        **(dict(hedef_yoklugu=hedef_yoklugu, ayni_gun=ayni_gun) if sinyalli else {}),
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
    gm = kosu.mc_girdi_kaydet(kayit=g)
    is_ = next(
        i
        for i in g["isler"]
        if i["dilim"] == "2022" and i["deney"] == deney and i["durum"] == "hazir"
    )
    komsular = depo.mc_komsular(gm.olay_id)
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


def test_s13_mc_kosusu_dis_yaziciyi_baglam_boyunca_engeller(tmp_path, monkeypatch):
    import ctypes
    import os
    import subprocess
    import sys
    from ctypes import wintypes

    depo, m, _, _ = s13_kayitli(tmp_path, monkeypatch, sinyalli=False)
    korunabilir = False
    if os.name == "nt":
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetVolumePathNameW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            wintypes.DWORD,
        )
        kernel.GetVolumePathNameW.restype = wintypes.BOOL
        kernel.GetDriveTypeW.argtypes = (wintypes.LPCWSTR,)
        kernel.GetDriveTypeW.restype = wintypes.UINT
        kernel.GetVolumeInformationW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPWSTR,
            wintypes.DWORD,
        )
        kernel.GetVolumeInformationW.restype = wintypes.BOOL
        root = ctypes.create_unicode_buffer(1024)
        assert kernel.GetVolumePathNameW(str(depo.yol), root, len(root))
        drive = kernel.GetDriveTypeW(root.value)
        assert drive not in (0, 1)
        if drive == 3:
            fs = ctypes.create_unicode_buffer(64)
            assert kernel.GetVolumeInformationW(
                root.value, None, 0, None, None, None, fs, len(fs)
            )
            korunabilir = fs.value == "NTFS"
    probe = (
        "import os,sys\n"
        "try:\n"
        "    fd=os.open(sys.argv[1],os.O_RDWR)\n"
        "except PermissionError:\n"
        "    sys.exit(0)\n"
        "except OSError as error:\n"
        "    print(error)\n"
        "    sys.exit(2)\n"
        "else:\n"
        "    os.close(fd)\n"
        "    sys.exit(1)\n"
    )
    attempts = []

    def observe(_):
        if not attempts:
            result = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", "-c", probe, str(depo.yol)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
                check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            attempts.append((result.returncode, result.stdout, result.stderr))

    result = ts.kayitli_monte_carlo_calistir(
        depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=observe
    )
    assert result["durum"] == "eksik"
    assert attempts == [(0 if korunabilir else 1, "", "")], (
        "MC koşusu sırasında başka süreç günlüğü yazmak için açmamalıdır.",
        attempts,
    )


def test_s13_mc_gecersiz_yazim_hatasi_senaryo_kaydi_ile_degistirilmez(monkeypatch):
    from types import SimpleNamespace
    from tansu import deneme as deneme_

    hata = deneme_.PilotHatasi("MC fiziksel yayın geri okuması uyuşmuyor.")
    yayinlar = []
    depo = SimpleNamespace(_mc_baglam=SimpleNamespace(gecersiz=True))
    kosu = SimpleNamespace(mc_sonuclari_kaydet=lambda **_: yayinlar.append(True))
    monkeypatch.setattr(
        ts,
        "_mc_planlar",
        lambda *args: [({"cekilis": {}}, SimpleNamespace(olay_id="plan"))],
    )

    def bozuk_okuma(*args):
        raise hata

    monkeypatch.setattr(ts, "_mc_ayar_yeniden_sina", bozuk_okuma)
    with pytest.raises(deneme_.PilotHatasi) as yakalanan:
        ts._mc_isi_yurut(
            depo,
            kosu,
            {"yontem_ayarlari": {"tekrar": 1, "kontrol_noktalari": [1]}},
            {},
            {},
            "girdi",
            {"durum": "olculebilir", "deney": "ayar_komsulugu_v1"},
            "kok",
            [],
            {},
        )
    assert yakalanan.value is hata
    assert yayinlar == []


def test_s13_wf_gercek_ayar_stresi_kendi_sinyalini_ceyrekler_arasi_korur(
    tmp_path, monkeypatch
):
    from copy import deepcopy
    from tansu import deneme, istatistik

    depo, m, _, kaynak = s13_kayitli(
        tmp_path, monkeypatch, kilit_politikasi="ham_aralik_v1"
    )
    korunan_yol = tmp_path / "mc-korunan-es.jsonl"
    korunan_yol.write_bytes(depo.yol.read_bytes())
    korunan_depo = deneme.PilotKayit(korunan_yol)
    ctx, d, g = s13_kosu(depo, m, kaynak)
    asil = ts._ileri_test_sembolu
    tasima = {}
    sinyal_yayini = ts._mc_sinyalleri
    asil_adim = motor.islem_adimi
    adim_girdileri = {"yerel": [], "korunan": []}
    etkin_adim = [None]

    def adim(durum, mum, sinyal=None, **kwargs):
        if etkin_adim[0] is not None:
            adim_girdileri[etkin_adim[0]].append(
                [
                    motor._duz(mum),
                    sinyal,
                    motor._duz(dataclasses.asdict(kwargs["ayar"])),
                    motor._duz(kwargs["kutu_alt"]),
                    motor._duz(kwargs["hedef"]),
                    motor._duz(kwargs["kurulum_kaniti"]),
                    motor._duz(kwargs["yurutme"]),
                ]
            )
        return asil_adim(durum, mum, sinyal, **kwargs)

    monkeypatch.setattr(motor, "islem_adimi", adim)
    yanlis_secim = dict(
        surum="pay_kimligi_v1",
        tablo_ozeti="00" * 32,
        kaynak=d["veri_ayarlari"]["kaynak"],
        goruntu_id=d["veri_ayarlari"]["veri_referanslari"][0],
        manifest_ozeti=d["veri_ayarlari"]["manifest_ozeti"],
    )
    sinyal_siniri = []

    def yayin(depo, kosu, secim, secilen, plan_ref, kabuller, refler):
        if kabuller and not sinyal_siniri:
            for boz in ("pay_kimligi", "e2_bagi"):
                kabul = deepcopy(kabuller[0])
                if boz == "pay_kimligi":
                    kabul["veri_ref"]["pay_kimligi"] = yanlis_secim
                else:
                    kabul["kaynak_sinyal"]["baglar"]["veri_ref_id"] = "baska-e1"
                once = depo.yol.read_bytes()
                with pytest.raises(deneme.PilotHatasi):
                    sinyal_yayini(depo, kosu, secim, secilen, plan_ref, [kabul], refler)
                assert depo.yol.read_bytes() == once
                sinyal_siniri.append(boz)
        return sinyal_yayini(depo, kosu, secim, secilen, plan_ref, kabuller, refler)

    monkeypatch.setattr(ts, "_mc_sinyalleri", yayin)

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
            for alan in ("referans", "uyelik"):
                yanlis_paket = deepcopy(paket)
                yanlis_paket[alan]["pay_kimligi"] = yanlis_secim
                with pytest.raises(deneme.PilotHatasi):
                    asil(
                        depo,
                        d,
                        kosu,
                        r,
                        yanlis_paket,
                        "TEST",
                        secim,
                        None,
                        r["uyelik"],
                        mc_plan_ref=pm.olay_id,
                        mc_cocuk_id=cocuk["deneme_id"],
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
        tekrar, refler, hata = None, None, None
        etkin_adim[0] = "yerel"
        try:
            tekrar, refler = ts._mc_ayar_yeniden_sina(
                depo, d, kosu, kaynak, p, pm.olay_id, tmp_path
            )
        except (KeyError, deneme.PilotHatasi) as yakalanan:
            hata = yakalanan
        finally:
            etkin_adim[0] = None
        assert tekrar is not None, (
            f"MC ortak yol donmuş hücre yöntemini kullanmalıdır: {hata}"
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
    assert sinyal_siniri == ["pay_kimligi", "e2_bagi"]
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

    fiziksel = [
        deneme._coz(json.loads(s)) for s in depo.yol.read_bytes().split(b"\n") if s
    ]
    for boz in ("pay_kimligi", "e2_bagi"):
        kopya = deepcopy(fiziksel)
        parti = next(
            o
            for o in kopya
            if o["kayit_turu"] == "mc_parti"
            and o["kayit"]["kayitlar"][0]["kayit_turu"] == "mc_sinyal"
        )
        ic = parti["kayit"]["kayitlar"][0]
        if boz == "pay_kimligi":
            ic["kayit"]["sinyal"]["veri_ref"]["pay_kimligi"] = yanlis_secim
        else:
            ic["kayit"]["sinyal"]["kaynak_sinyal"]["baglar"]["veri_ref_id"] = "baska-e1"
        ic["icerik_ozeti"] = deneme._mc_ozet(ic["kayit"])
        parti["icerik_ozeti"] = deneme._mc_ozet(parti["kayit"])
        # End at the signal. A later E3 state cannot cause incidental refusal.
        yol = tmp_path / ("mc-sinyal-" + boz + ".jsonl")
        yol.write_bytes(
            b"".join(deneme.kanonik(o) + b"\n" for o in kopya[: kopya.index(parti) + 1])
        )
        with pytest.raises(deneme.PilotHatasi):
            deneme.PilotKayit(yol).oku()

    yerel_tekrar = deepcopy(tekrar)
    yerel_olcu = deepcopy(olcu)
    yerel_tasima = deepcopy(tasima)
    yerel_refler = list(refler)
    yerel_sinyaller = [deneme._bul(olaylar, r, "mc_sinyal") for r in yerel_refler]
    yerel_senaryo = deneme._bul(olaylar, sm.olay_id, "mc_senaryo")
    monkeypatch.setattr(ts, "_mc_sinyalleri", sinyal_yayini)
    tasima.clear()

    with korunan_depo.mc_yazim(m.deneme_id):
        korunan_ctx, korunan_d, korunan_g = s13_kosu(korunan_depo, m, kaynak)
        with korunan_ctx as korunan_kosu:
            korunan_is, [(korunan_plan, korunan_pm)] = s13_plan(
                korunan_depo, korunan_kosu, korunan_d, korunan_g
            )
            etkin_adim[0] = "korunan"
            try:
                korunan_tekrar, korunan_refler = ts._mc_ayar_yeniden_sina(
                    korunan_depo,
                    korunan_d,
                    korunan_kosu,
                    kaynak,
                    korunan_plan,
                    korunan_pm.olay_id,
                    tmp_path,
                )
            finally:
                etkin_adim[0] = None
            korunan_olcu = istatistik.mc_senaryo_olculeri(
                korunan_g,
                korunan_is,
                korunan_plan["cekilis"],
                durumlar=korunan_tekrar["durumlar"],
            )
            korunan_sm = korunan_kosu.mc_senaryo_sonucu_kaydet(
                kayit=dict(
                    plan_ref=korunan_pm.olay_id,
                    durum="tamamlandi",
                    **korunan_olcu,
                    yeniden_sinama=korunan_tekrar,
                    sonuc_referanslari=korunan_refler,
                    asama=None,
                    neden=None,
                )
            )
            korunan_senaryo = korunan_depo.mc_makbuzlar(
                korunan_kosu, [korunan_sm], "mc_senaryo"
            )[0]
            korunan_sinyaller = [
                korunan_depo.mc_kayit(r, "mc_sinyal") for r in korunan_refler
            ]

    assert korunan_plan["cekilis"] == p["cekilis"]
    assert korunan_olcu == yerel_olcu
    assert len(korunan_refler) == len(yerel_refler) > 0
    assert [o["kayit_id"] for o in yerel_sinyaller] == yerel_refler
    assert [o["kayit_id"] for o in korunan_sinyaller] == korunan_refler
    assert yerel_senaryo["kayit"]["sonuc_referanslari"] == yerel_refler
    assert korunan_senaryo["kayit"]["sonuc_referanslari"] == korunan_refler

    def kimlikler(plan, pm, kosu, sm, refler):
        sonuc = {
            plan["girdi_ref"]: "<GIRDI>",
            pm.olay_id: "<PLAN>",
            kosu.makbuz.kosu_id: "<KOSU>",
            sm.olay_id: "<SENARYO>",
        }
        sonuc.update({r: f"<SINYAL:{i}>" for i, r in enumerate(refler)})
        sonuc.update(
            {
                c["deneme_id"]: f"<COCUK:{c['bolum']}:{c['sembol']}>"
                for c in plan["stres_cocuklari"]
            }
        )
        return sonuc

    def ayir(deger, esleme):
        if isinstance(deger, str):
            if deger in esleme:
                return esleme[deger]
            for kimlik, etiket in esleme.items():
                if deger.startswith(kimlik + ":"):
                    return etiket + deger[len(kimlik) :]
            return deger
        if isinstance(deger, dict):
            return {k: ayir(v, esleme) for k, v in deger.items()}
        if isinstance(deger, list):
            return [ayir(v, esleme) for v in deger]
        return deger

    def muhur_haric(deger):
        if isinstance(deger, dict):
            return {k: muhur_haric(v) for k, v in deger.items() if k != "butunluk"}
        if isinstance(deger, list):
            return [muhur_haric(v) for v in deger]
        return deger

    yerel_kimlikler = kimlikler(p, pm, kosu, sm, yerel_refler)
    korunan_kimlikler = kimlikler(
        korunan_plan, korunan_pm, korunan_kosu, korunan_sm, korunan_refler
    )
    for durum in (
        *yerel_tekrar["durumlar"].values(),
        *korunan_tekrar["durumlar"].values(),
        *yerel_tasima.values(),
        *tasima.values(),
    ):
        assert motor._durumu_oku(durum, durum["yurutme"])["surum"] == "islem_durumu_v1"
    for sembol, yerel_durum in yerel_tekrar["durumlar"].items():
        korunan_durum = korunan_tekrar["durumlar"][sembol]
        assert len(yerel_durum["butunluk"]) == len(korunan_durum["butunluk"]) == 64
        assert len(yerel_durum["islemler"]) == len(korunan_durum["islemler"])
        for i, (eski_islem, yeni_islem) in enumerate(
            zip(yerel_durum["islemler"], korunan_durum["islemler"], strict=True)
        ):
            etiket = f"<ISLEM:{sembol}:{i}>"
            yerel_kimlikler.setdefault(
                eski_islem["pozisyon"]["risk_girdisi"]["islem_id"], etiket
            )
            korunan_kimlikler.setdefault(
                yeni_islem["pozisyon"]["risk_girdisi"]["islem_id"], etiket
            )
        if yerel_durum["pozisyon"] and korunan_durum["pozisyon"]:
            etiket = f"<ACIK_ISLEM:{sembol}>"
            yerel_kimlikler.setdefault(
                yerel_durum["pozisyon"]["risk_girdisi"]["islem_id"], etiket
            )
            korunan_kimlikler.setdefault(
                korunan_durum["pozisyon"]["risk_girdisi"]["islem_id"], etiket
            )

    def ilk_fark(eski, yeni, yol="$"):
        if type(eski) is not type(yeni):
            return yol, repr(eski)[:120], repr(yeni)[:120]
        if isinstance(eski, dict):
            if eski.keys() != yeni.keys():
                return yol, list(eski), list(yeni)
            for ad in eski:
                fark = ilk_fark(eski[ad], yeni[ad], f"{yol}.{ad}")
                if fark is not None:
                    return fark
        elif isinstance(eski, list):
            if len(eski) != len(yeni):
                return yol, len(eski), len(yeni)
            for i, (a, b) in enumerate(zip(eski, yeni, strict=True)):
                fark = ilk_fark(a, b, f"{yol}[{i}]")
                if fark is not None:
                    return fark
        elif eski != yeni:
            return yol, repr(eski)[:120], repr(yeni)[:120]
        return None

    assert adim_girdileri["yerel"]
    assert len(adim_girdileri["yerel"]) == len(adim_girdileri["korunan"])
    yerel_girdiler = ayir(adim_girdileri["yerel"], yerel_kimlikler)
    korunan_girdiler = ayir(adim_girdileri["korunan"], korunan_kimlikler)
    assert deneme.kanonik(yerel_girdiler) == deneme.kanonik(korunan_girdiler), ilk_fark(
        yerel_girdiler, korunan_girdiler
    )
    for sembol, yerel_durum in yerel_tekrar["durumlar"].items():
        korunan_durum = korunan_tekrar["durumlar"][sembol]
        if yerel_durum.get("son_girdi") and korunan_durum.get("son_girdi"):
            etiket = f"<SON_GIRDI:{sembol}>"
            yerel_kimlikler.setdefault(yerel_durum["son_girdi"], etiket)
            korunan_kimlikler.setdefault(korunan_durum["son_girdi"], etiket)
    for bolum, yerel_durum in yerel_tasima.items():
        korunan_durum = tasima[bolum]
        if yerel_durum.get("son_girdi") and korunan_durum.get("son_girdi"):
            etiket = f"<SON_GIRDI:{bolum}>"
            yerel_kimlikler.setdefault(yerel_durum["son_girdi"], etiket)
            korunan_kimlikler.setdefault(korunan_durum["son_girdi"], etiket)
    assert deneme.kanonik(ayir(muhur_haric(yerel_tekrar), yerel_kimlikler)) == (
        deneme.kanonik(ayir(muhur_haric(korunan_tekrar), korunan_kimlikler))
    )

    yerel_tasima_alanlari = ayir(muhur_haric(yerel_tasima), yerel_kimlikler)
    korunan_tasima_alanlari = ayir(muhur_haric(tasima), korunan_kimlikler)
    assert deneme.kanonik(yerel_tasima_alanlari) == deneme.kanonik(
        korunan_tasima_alanlari
    ), ilk_fark(yerel_tasima_alanlari, korunan_tasima_alanlari)

    def sabit_alanlar(olay):
        alanlar = {
            a: v
            for a, v in olay.items()
            if a not in ("kayit_id", "olusturma_zamani", "icerik_ozeti", "parti_ref")
        }
        if olay["kayit_turu"] == "mc_sinyal":
            alanlar = deepcopy(alanlar)
            alanlar["kayit"]["sinyal"]["kaynak_sinyal"]["olusturma_zamani"] = (
                "<URETILEN_ZAMAN>"
            )
        return alanlar

    for onceki, sonraki in zip(yerel_sinyaller, korunan_sinyaller, strict=True):
        assert deneme.kanonik(
            ayir(muhur_haric(sabit_alanlar(onceki)), yerel_kimlikler)
        ) == deneme.kanonik(
            ayir(muhur_haric(sabit_alanlar(sonraki)), korunan_kimlikler)
        )
    assert deneme.kanonik(
        ayir(muhur_haric(sabit_alanlar(yerel_senaryo)), yerel_kimlikler)
    ) == deneme.kanonik(
        ayir(muhur_haric(sabit_alanlar(korunan_senaryo)), korunan_kimlikler)
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


def test_s13_wf_genel_giris_binlik_orneklerden_sonra_ilk_gercek_streste_kesilir(
    tmp_path, monkeypatch
):
    from collections import Counter
    from hashlib import sha256
    from time import perf_counter
    from tansu import deneme, saglamlik

    depo, m, _, _ = s13_kayitli(tmp_path, monkeypatch)
    ilk_baytlar = depo.yol.stat().st_size
    sayac = Counter()
    kaydet = deneme._Kosu.mc_sonuclari_kaydet

    def gozle(nesne, ad, etiket):
        asil = getattr(nesne, ad)

        def hesap(*a, **kw):
            sayac[etiket] += 1
            return asil(*a, **kw)

        monkeypatch.setattr(nesne, ad, hesap)

    gozle(veri, "veri_hazirla", "E1_veri")
    gozle(aileler, "ortak_donem_kurulumu", "E2")
    gozle(saglamlik, "ema_hucre_calistir", "E3")
    gozle(ts, "_mc_ayar_yeniden_sina", "gercek_stres_denemesi")
    gozle(ts, "_ileri_test_paketi", "ceyrek_verisi")

    def kaydet_ve_dur(kosu, *, kayitlar):
        makbuzlar = kaydet(kosu, kayitlar=kayitlar)
        if any(k["yeniden_sinama"] for k in kayitlar):
            sayac["kalici_stres_sonucu"] += 1
            raise KeyboardInterrupt(
                "İlk kalıcı gerçek stres sonucunda kontrollü kesinti."
            )
        return makbuzlar

    monkeypatch.setattr(deneme._Kosu, "mc_sonuclari_kaydet", kaydet_ve_dur)
    baslangic = perf_counter()
    with pytest.raises(KeyboardInterrupt, match="kontrollü kesinti"):
        ts.kayitli_monte_carlo_calistir(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=None
        )
    sure = perf_counter() - baslangic
    olaylar = depo.oku()
    girdi = next(o["kayit"] for o in olaylar if o["kayit_turu"] == "mc_girdi")
    tum_kontroller = [o["kayit"] for o in olaylar if o["kayit_turu"] == "mc_kontrol"]
    kontroller = tum_kontroller[:2]
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
    tam_kurtarma = depo.kurtar()
    isler = tam_kurtarma["mc_belirsiz_kosular"][0]["isler"]
    kurtarma = [i for i in isler if i["anahtar"] in {k["anahtar"] for k in kontroller}]
    assert sum(i["kesin_tamamlanan"] for i in kurtarma) == 2000
    assert all(i["deneme_yayin_belirsiz"] is None for i in kurtarma)
    senaryolar = [o for o in olaylar if o["kayit_turu"] == "mc_senaryo"]
    stres = next(o for o in senaryolar if o["kayit"]["yeniden_sinama"])
    plan = deneme._bul(olaylar, stres["kayit"]["plan_ref"], "mc_plan")["kayit"]
    bekleyen = next(i for i in isler if i["anahtar"] == plan["anahtar"])
    kanit = dict(
        durum="ilk_kalici_stres_sonrasi_kesildi",
        piyasa_kaniti=False,
        on_gosterim_tamamlandi=False,
        nihai_butce_uygulanabilirligi=False,
        genel_giris_suresi_saniye=sure,
        kaynak_kurulumu_sureye_dahil=False,
        sayac=dict(sayac),
        kayitli_butce=depo.deneme_oku(m.deneme_id)["yontem_ayarlari"]["tekrar"],
        kaynak=girdi["kaynak"],
        kaynak_kapali_nufus=len(girdi["nufus"]),
        kaynak_seans_sayisi=len(girdi["seanslar"]),
        kesin_tamamlanan=len(senaryolar),
        hatali_senaryo=sum(o["kayit"]["durum"] != "tamamlandi" for o in senaryolar),
        kontrol_sayisi=len(tum_kontroller),
        ilk_gunluk_bayt=ilk_baytlar,
        son_gunluk_bayt=depo.yol.stat().st_size,
        gunluk_sha256=sha256(depo.yol.read_bytes()).hexdigest(),
        kurtarma={k: v for k, v in tam_kurtarma.items() if k != "olaylar"},
    )
    (tmp_path / "mc-genel-giris-kaniti.json").write_text(
        json.dumps(kanit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    assert kanit["kayitli_butce"] == 1000
    assert len(tum_kontroller) == 3
    kacirma = next(
        i for i in girdi["isler"] if i["anahtar"] == tum_kontroller[2]["anahtar"]
    )
    assert kacirma["deney"] == "islem_kacirma_v1" and kacirma["dilim"] == "2022"
    assert len(tum_kontroller[2]["sonuc_referanslari"]) == 1000
    assert len(senaryolar) == 3001 and kanit["hatali_senaryo"] == 0
    assert sayac == dict(
        E1_veri=16,
        E2=16,
        E3=16,
        gercek_stres_denemesi=1,
        ceyrek_verisi=16,
        kalici_stres_sonucu=1,
    )
    assert plan["indeks"] == 0
    assert len(stres["kayit"]["yeniden_sinama"]["bolumler"]) == 16
    assert bekleyen["kesin_tamamlanan"] == 1 and bekleyen["denenen"] is None
    assert bekleyen["deneme_yayin_belirsiz"] == [1, 31]
    assert sum(i["kesin_tamamlanan"] for i in isler) == 3001
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


def s10_kismi_piyasasi(piyasa):
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


def test_s10_acik_yil_sonu_kismi_satisi_ve_kalani_ayri_korur(tmp_path, monkeypatch):
    depo, makbuz, piyasa = s10_kayitli(tmp_path, monkeypatch, varyant="stop_atr2")
    s10_kismi_piyasasi(piyasa)
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


def s10_hedef_yoklugu(tmp_path, monkeypatch):
    depo, makbuz, piyasa = s10_kayitli(
        tmp_path, monkeypatch, sinyal=True, varyant="tansu"
    )
    for r in piyasa:
        if r["tarih"] == "2021-12-31":
            r["duzeltilmis_dusuk"]["deger"] = 110.0
            r["ham_dusuk"]["deger"] = 110.0
            r["hacim_tl"]["deger"] = 500.0
    return depo, makbuz


def test_s10_izinli_hedef_yoklugu_eksik_kurulum_degildir(tmp_path, monkeypatch):
    depo, makbuz = s10_hedef_yoklugu(tmp_path, monkeypatch)
    sonuc = s10_calistir(depo, makbuz, tmp_path)
    yil = sonuc["donemler"][4]
    assert yil["adaylar"], "İzinli hedef yokluğu olan gerçek E2 sinyali korunmalı"
    assert yil["adaylar"][0]["hedef"]["bos_nedeni"] == "hedef_bulunamadi"
    durum = yil["durumlar"]["TEST"]
    assert "kurulum_eksik" not in [r["neden"] for r in durum["retler"]], (
        "TASARIM 5.15: E2'nin izinli hedef yokluğu eksik kurulum değildir"
    )
    assert yil["durum"] == "tamamlandi"
    assert yil["islem_referanslari"] == []
    assert durum["pozisyon"]["durum"] == "bekliyor"
    assert durum["pozisyon"]["hedef"] is None
    assert durum["pozisyon"]["kutu_alt"] == yil["adaylar"][0]["kutu_alt"]["deger"]


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


def s12_kayitli(tmp_path, monkeypatch, *, varyant="bugun", **secenekler):
    """S12: gerçek E2/E3/E5; yalnız E1 piyasa sınırı sentetiktir."""
    import datetime as dt
    from copy import deepcopy
    from tests.test_kayit import pilot_deneme

    depo, eski, piyasa = s10_kayitli(
        tmp_path, monkeypatch, varyant=varyant, **secenekler
    )
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


def test_s12_biten_kosu_ayni_kimlikle_sonucu_yeniden_verir(tmp_path, monkeypatch):
    from tansu import deneme

    depo, m, _ = s12_kayitli(tmp_path, monkeypatch)
    monkeypatch.setattr(veri, "oku", lambda *_: None)
    onceki = s12_calistir(depo, m, tmp_path)
    baytlar = depo.yol.read_bytes()
    try:
        devam = ts.kayitli_ileri_calistir(
            deneme.PilotKayit(depo.yol),
            m.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            devam_kosu_id=onceki["kosu_id"],
            ilerleme=None,
        )
    except TypeError as hata:
        assert False, f"S12 kayıtlı koşuya devam yüzü gerekli: {hata}"
    assert devam == onceki
    assert depo.yol.read_bytes() == baytlar


def test_s12_cli_once_gelen_eski_secimi_yazmadan_reddeder(tmp_path, capsys):
    yol = tmp_path / "pilot.jsonl"
    kod = komut.main(
        [
            "--hisse",
            "1",
            "ileri-sinama",
            "--deneme-dosyasi",
            str(yol),
            "--deneme-id",
            "deneme",
            "--kok",
            str(tmp_path),
        ]
    )
    assert kod == 1
    assert "eski yöntem seçeneklerini kabul etmez" in capsys.readouterr().err
    assert not yol.exists()


def test_s12_kesilen_sinyal_ozgun_makbuzla_surer(tmp_path, monkeypatch):
    from tansu import deneme

    depo, m, _ = s12_sinyalli(tmp_path, monkeypatch)
    monkeypatch.setattr(veri, "oku", lambda *_: None)
    asil = deneme._Kosu.ileri_sinyal_kaydet

    def kes(kosu, **alanlar):
        asil(kosu, **alanlar)
        raise KeyboardInterrupt

    monkeypatch.setattr(deneme._Kosu, "ileri_sinyal_kaydet", kes)
    with pytest.raises(KeyboardInterrupt):
        s12_calistir(depo, m, tmp_path)
    monkeypatch.setattr(deneme._Kosu, "ileri_sinyal_kaydet", asil)
    eski = [o for o in depo.oku() if o["kayit_turu"] == "ileri_sinyal"]
    assert len(eski) == 1
    kosu_id = eski[0]["kosu_id"]
    devam = ts.kayitli_ileri_calistir(
        deneme.PilotKayit(depo.yol),
        m.deneme_id,
        veri_koku=tmp_path,
        mod="gelistirme",
        devam_kosu_id=kosu_id,
        ilerleme=None,
    )
    assert devam["durum"] == "tamamlandi"
    sinyaller = [o for o in depo.oku() if o["kayit_turu"] == "ileri_sinyal"]
    assert sinyaller[0] == eski[0]
    assert len({o["kayit_id"] for o in sinyaller}) == len(sinyaller)


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


def s12_sinyalli(
    tmp_path,
    monkeypatch,
    *,
    son_sinyal="2025-10-05",
    hedef_yoklugu=False,
    ayni_gun=False,
    **secenekler,
):
    depo, m, piyasa = s12_kayitli(
        tmp_path, monkeypatch, varyant="stop_atr2", **secenekler
    )
    tarihler = pd.DatetimeIndex(
        ["2021-01-04", "2021-10-05", "2022-01-05", "2024-10-04", son_sinyal]
    )

    def kurulum(f, p):
        t = tarihler.intersection(f.index)
        k = pd.DataFrame(dict(kutu_alt=95.0, kutu_ust=101.0, hedef=110.0), index=t)
        if hedef_yoklugu and pd.Timestamp("2022-01-05") in k.index:
            k.loc["2022-01-05", "hedef"] = float("nan")
        if ayni_gun and pd.Timestamp("2022-01-05") in k.index:
            ikinci = k.loc[["2022-01-05"]].copy()
            ikinci["kutu_alt"], ikinci["hedef"] = 96.0, 150.0
            k = pd.concat([k, ikinci])
        return k

    monkeypatch.setattr(aileler, "kurulum", kurulum)
    for r in piyasa:
        fiyat = (
            110.0 if r["tarih"] in ("2021-04-04", "2022-07-04", "2025-01-04") else 100.0
        )
        for ad, fark in (("aof", 0), ("kapanis", 0), ("yuksek", 1), ("dusuk", -1)):
            r[f"duzeltilmis_{ad}"]["deger"] = fiyat + fark
        r["ham_yuksek"]["deger"], r["ham_dusuk"]["deger"] = fiyat + 1, fiyat - 1
    return depo, m, piyasa


def s12_surec_kaynagi(kok, deneme_id):
    """Aynı sentetik E1 girdisini yeni Python sürecinde kurar."""
    from pathlib import Path

    from tansu import deneme

    kok = Path(kok)
    piyasa = json.loads((kok / "piyasa.json").read_text(encoding="utf-8"))
    depo = deneme.PilotKayit(kok / "pilot.jsonl")
    v = next(
        o["veri_ayarlari"]
        for s in depo.yol.read_text(encoding="utf-8").splitlines()
        if (o := deneme._coz(json.loads(s))).get("deneme_id") == deneme_id
        and o["kayit_turu"] == "deneme"
    )
    gunler = v["takvim"]["seanslar"]

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

    def paket(istek, kimlik, veri_koku):
        assert any(o["kayit_turu"] == "baslangic" for o in depo.oku())
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

    tarihler = pd.DatetimeIndex(
        ["2021-01-04", "2021-10-05", "2022-01-05", "2024-10-04", "2025-10-05"]
    )

    def kurulum(f, p):
        t = tarihler.intersection(f.index)
        return pd.DataFrame(dict(kutu_alt=95.0, kutu_ust=101.0, hedef=110.0), index=t)

    veri.uyelik_hazirla = uyelik
    veri.veri_hazirla = paket
    veri.oku = lambda *_: None
    aileler.kurulum = kurulum


_S12_ANLAMLI_ALANLAR = {
    "durum",
    "neden",
    "tur",
    "rol",
    "sembol",
    "yon",
    "eylem",
    "cikis_nedeni",
    "asama",
    "bolum_id",
    "tarih",
    "baslangic",
    "bitis",
    "son_tarih",
    "sinyal_tarih",
    "giris_tarih",
    "cikis_tarih",
}
_S12_ANLAMLI_LISTELER = {"hatalar", "hata_nedenleri", "uyarilar", "kalite_bayraklari"}


def s12_sonuc_alanlari(icerik, yol=()):
    if isinstance(icerik, dict):
        return {(*yol, "anahtarlar"): tuple(sorted(icerik))} | {
            k: v
            for ad, deger in icerik.items()
            for k, v in s12_sonuc_alanlari(deger, (*yol, ad)).items()
        }
    if isinstance(icerik, list):
        if icerik and all(
            isinstance(o, dict) and {"olay_id", "tur", "tarih", "sembol"} <= o.keys()
            for o in icerik
        ):
            # S12 olay kimliği koşuya bağlıdır; aynı günün olayları buna göre sıralanır.
            icerik = sorted(
                icerik,
                key=lambda o: (
                    o["tarih"],
                    o["sembol"],
                    o["tur"],
                    repr(sorted(s12_sonuc_alanlari(o).items())),
                ),
            )
        return {(*yol, "adet"): len(icerik)} | {
            k: v
            for i, deger in enumerate(icerik)
            for k, v in s12_sonuc_alanlari(deger, (*yol, i)).items()
        }
    if type(icerik) in (int, float, Decimal, bool):
        return {yol: icerik} if not yol or yol[-1] != "isci_pid" else {}
    if (
        yol
        and (
            yol[-1] in _S12_ANLAMLI_ALANLAR
            or (isinstance(yol[-1], str) and yol[-1].endswith("_tarih"))
            or any(ad in _S12_ANLAMLI_LISTELER for ad in yol)
        )
        and (icerik is None or isinstance(icerik, (str, dt.date)))
    ):
        return {yol: icerik}
    return {}


def test_s12_eski_sinyal_oneginden_secimsiz_tasinan_sembol_hesaplanir(
    tmp_path, monkeypatch
):
    from types import SimpleNamespace

    depo, makbuz, _ = s12_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(makbuz.deneme_id)
    bolum = d["donemler"][0]
    r = dict(donem=bolum, adaylar=[])
    paket = dict(gunler=[bolum["baslangic"].isoformat()], piyasa=[])
    onceki = dict(pozisyon=dict(durum="acik"), karantina_kalan=0)
    kosu = SimpleNamespace(
        makbuz=SimpleNamespace(kosu_id="eski-kosu"),
        _tekrar_adaylari=[
            dict(
                kayit_turu="ileri_sinyal",
                secim_ref="daha-once-secilen-sembol",
                sinyal=dict(kaynak_sinyal=dict(kayit_id="eski-sinyal")),
            )
        ],
    )
    monkeypatch.setattr(
        aileler,
        "ortak_donem_kurulumu",
        lambda *_: {"TEST": dict(sinyaller=[], kurulum=pd.DataFrame())},
    )
    monkeypatch.setattr(
        ts,
        "_s10_mumlar",
        lambda *_args, **_kwargs: pd.DataFrame(
            index=pd.DatetimeIndex([bolum["baslangic"].isoformat()])
        ),
    )
    monkeypatch.setattr(ts, "_isinma_kaydet", lambda *_: 0)

    def hesapla(*_args, onceki_durum, **_kwargs):
        assert onceki_durum is onceki
        return dict(retler=[], pozisyon=onceki["pozisyon"])

    monkeypatch.setattr(ts.saglamlik, "ema_hucre_calistir", hesapla)
    sonuc = ts._ileri_test_sembolu(
        depo, d, kosu, r, paket, "TEST", None, onceki, dict(gunler={})
    )
    assert sonuc["pozisyon"] == onceki["pozisyon"]


def test_s12_isci_olumu_yeni_surecte_ayni_kosuyu_tamamlar(tmp_path, monkeypatch):
    import subprocess
    import sys
    from pathlib import Path

    from tansu import deneme

    kesik_kok, tam_kok = tmp_path / "kesik", tmp_path / "tam"
    kesik_kok.mkdir()
    tam_kok.mkdir()
    kesik_depo, kesik_deneme, piyasa = s12_sinyalli(kesik_kok, monkeypatch)
    (kesik_kok / "piyasa.json").write_text(
        json.dumps(piyasa, ensure_ascii=False), encoding="utf-8"
    )
    tam_depo, tam_deneme, _ = s12_sinyalli(tam_kok, monkeypatch)
    tam = s12_calistir(tam_depo, tam_deneme, tam_kok)
    assert tam["durum"] == "tamamlandi"

    kod = """
import os, sys
from pathlib import Path
from tansu import __main__ as komut, deneme, tansusinama as ts
from tests.test_tansusinama import s12_surec_kaynagi
kok, deneme_id, rol = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
s12_surec_kaynagi(kok, deneme_id)
if rol == 'kes':
    asil = deneme._Kosu.ileri_dayaniklastir
    def kes(self, makbuz):
        asil(self, makbuz)
        o = deneme._bul(self._depo.oku(), makbuz.olay_id)
        if o['kayit_turu'] == 'sonuc' and o.get('bolum_id') == '2022Q2':
            os._exit(77)
    deneme._Kosu.ileri_dayaniklastir = kes
else:
    asil = ts._ileri_secimler
    def hesap(*a, **kw):
        print('HESAP:' + a[3]['ad'], flush=True)
        return asil(*a, **kw)
    ts._ileri_secimler = hesap
argv = ['ileri-sinama', '--deneme-dosyasi', str(kok / 'pilot.jsonl'),
        '--deneme-id', deneme_id, '--kok', str(kok)]
if rol != 'kes':
    argv += ['--devam-kosu-id', sys.argv[4]]
sys.exit(komut.main(argv))
"""
    ortak = [
        sys.executable,
        "-B",
        "-X",
        "utf8",
        "-c",
        kod,
        str(kesik_kok),
        kesik_deneme.deneme_id,
    ]
    kes = subprocess.run(
        [*ortak, "kes"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert kes.returncode == 77, (kes.stdout, kes.stderr)
    kesik_depo = deneme.PilotKayit(kesik_depo.yol)
    once = kesik_depo.oku()
    baslangiclar = [
        o
        for o in once
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] == kesik_deneme.deneme_id
    ]
    assert len(baslangiclar) == 1
    kosu_id = baslangiclar[0]["kosu_id"]
    assert [o["bolum_id"] for o in once if o.get("sonuc_turu") == "ileri_v1"] == [
        "2022Q1",
        "2022Q2",
    ]
    acik_kaynak = dict(
        deneme_id=kesik_deneme.deneme_id,
        kosu_id=kosu_id,
        sonuc_ref="tamamlanmadi",
        bitis_ref="tamamlanmadi",
        icerik_ozeti="00" * 32,
    )
    with pytest.raises(deneme.PilotHatasi):
        deneme._mc_kaynagi(once, acik_kaynak, ozet_denetle=False)
    baytlar = kesik_depo.yol.read_bytes()
    devam = subprocess.run(
        [*ortak, "devam", kosu_id],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert devam.returncode == 0, (devam.stdout, devam.stderr)
    assert "HESAP:2022Q1" not in devam.stdout
    assert "HESAP:2022Q2" not in devam.stdout
    assert "HESAP:2022Q3" in devam.stdout
    assert kesik_depo.yol.read_bytes().startswith(baytlar)
    sonra = kesik_depo.oku()
    assert sonra[: len(once)] == once
    referans = tam_depo.oku()
    assert [o["kayit_turu"] for o in sonra] == [o["kayit_turu"] for o in referans]
    assert (
        len(
            [
                o
                for o in sonra
                if o["kayit_turu"] == "baslangic"
                and o["deneme_id"] == kesik_deneme.deneme_id
            ]
        )
        == 1
    )
    assert (
        len(
            [o for o in sonra if o["kayit_turu"] == "bitis" and o["kosu_id"] == kosu_id]
        )
        == 1
    )
    child_baslar = [
        o["deneme_id"]
        for o in sonra
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] != kesik_deneme.deneme_id
    ]
    assert len(child_baslar) == len(set(child_baslar))
    birlesik = next(
        o
        for o in sonra
        if o.get("sonuc_turu") == "ileri_v1" and o["bolum_id"] == "birlesik"
    )
    bitis = next(
        o for o in sonra if o["kayit_turu"] == "bitis" and o["kosu_id"] == kosu_id
    )
    kaynak = acik_kaynak | dict(
        sonuc_ref=birlesik["kayit_id"], bitis_ref=bitis["kayit_id"]
    )
    kabul = deneme._mc_kaynagi(sonra, kaynak, ozet_denetle=False)
    assert kabul["nufus"]

    def durum_izleri(olaylar):
        bolumler = [
            (o["bolum_id"], o["kayit"]["durum"], o["kayit"].get("neden"))
            for o in olaylar
            if o.get("sonuc_turu") == "ileri_v1"
        ]
        kontroller = []
        for o in olaylar:
            if o["kayit_turu"] != "ileri_kontrol":
                continue
            d = o["durum"]
            p = d["pozisyon"]
            kontroller.append(
                (
                    o["bolum_id"],
                    o["sembol"],
                    d["durum"],
                    d["son_tarih"],
                    None
                    if p is None
                    else (
                        p["durum"],
                        p["sinyal_tarih"],
                        p["giris_tarih"],
                        p["cikis_tarih"],
                    ),
                )
            )
        return bolumler, kontroller

    assert durum_izleri(sonra) == durum_izleri(referans)

    assert s12_sonuc_alanlari(sonra) == s12_sonuc_alanlari(referans)


def test_s12_son_ceyrek_yayin_onekleri_ayni_kosuda_surer(tmp_path, monkeypatch):
    from tansu import deneme

    depo, m, _ = s12_sinyalli(tmp_path, monkeypatch)
    tam = s12_calistir(depo, m, tmp_path)
    assert tam["durum"] == "tamamlandi"
    olaylar = depo.oku()
    kosu_id = tam["kosu_id"]
    cocuk = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "deneme"
        and o.get("baglar", {}).get("ileri_ust_kosu") == kosu_id
        and o["yontem_ayarlari"].get("bolum_id") == "2025Q4"
        and o["yontem_ayarlari"].get("rol") == "egitim"
    )
    cocuk_bas = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] == cocuk["deneme_id"]
    )
    cocuk_olaylari = [o for o in olaylar if o.get("kosu_id") == cocuk_bas["kosu_id"]]
    secim = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_secim" and o["bolum_id"] == "2025Q4"
    )
    kontrol = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_kontrol" and o["bolum_id"] == "2025Q4"
    )
    ceyrek = next(
        o
        for o in olaylar
        if o.get("sonuc_turu") == "ileri_v1" and o["bolum_id"] == "2025Q4"
    )
    birlesik = next(
        o
        for o in olaylar
        if o.get("sonuc_turu") == "ileri_v1" and o["bolum_id"] == "birlesik"
    )
    ust_bitis = next(
        o for o in olaylar if o["kayit_turu"] == "bitis" and o["kosu_id"] == kosu_id
    )
    sinirlar = [
        ("cocuk-revizyon", cocuk),
        ("cocuk-baslangic", cocuk_bas),
        ("cocuk-islem", next(o for o in cocuk_olaylari if o["kayit_turu"] == "islem")),
        ("cocuk-sonuc", next(o for o in cocuk_olaylari if o["kayit_turu"] == "sonuc")),
        ("cocuk-bitis", next(o for o in cocuk_olaylari if o["kayit_turu"] == "bitis")),
        ("secim", secim),
        ("kontrol", kontrol),
        ("ceyrek", ceyrek),
        ("birlesik", birlesik),
        ("ust-bitis", ust_bitis),
    ]
    monkeypatch.setattr(veri, "oku", lambda *_: None)
    asil = ts._ileri_secimler
    hesaplanan = []

    def izle(*args, **kwargs):
        hesaplanan.append(args[3]["ad"])
        return asil(*args, **kwargs)

    monkeypatch.setattr(ts, "_ileri_secimler", izle)
    for ad, olay in sinirlar:
        sira = olaylar.index(olay)
        onek = b"".join(deneme.kanonik(o) + b"\n" for o in olaylar[: sira + 1])
        assert depo.yol.read_bytes().startswith(onek)
        yol = tmp_path / f"{ad}.jsonl"
        yol.write_bytes(onek)
        hesaplanan.clear()
        r = ts.kayitli_ileri_calistir(
            deneme.PilotKayit(yol),
            m.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            devam_kosu_id=kosu_id,
            ilerleme=None,
        )
        assert r["durum"] == "tamamlandi", ad
        assert hesaplanan == (["2025Q4"] if sira < olaylar.index(ceyrek) else []), ad
        assert yol.read_bytes().startswith(onek), ad
        tekrar = deneme.PilotKayit(yol).oku()
        assert tekrar[: sira + 1] == olaylar[: sira + 1], ad
        assert (
            len(
                [
                    o
                    for o in tekrar
                    if o["kayit_turu"] == "baslangic" and o["deneme_id"] == m.deneme_id
                ]
            )
            == 1
        ), ad
        assert (
            len(
                [
                    o
                    for o in tekrar
                    if o["kayit_turu"] == "bitis" and o["kosu_id"] == kosu_id
                ]
            )
            == 1
        ), ad
        assert s12_sonuc_alanlari(tekrar) == s12_sonuc_alanlari(olaylar), ad


@pytest.mark.parametrize(
    "secim", [{}, {"kilit_politikasi": "ham_aralik_v1", "limit": False}]
)
def test_s12_bekleyen_ve_acik_islem_secimsiz_ceyrekte_surur_tek_kohort(
    tmp_path, monkeypatch, secim
):
    depo, m, _ = s12_sinyalli(tmp_path, monkeypatch, **secim)
    r = s12_calistir(depo, m, tmp_path)
    assert r["durum"] == "tamamlandi", [
        (b["bolum_id"], b["neden"]) for b in r["bolumler"]
    ]
    olaylar = depo.oku()
    kontroller = [o for o in olaylar if o["kayit_turu"] == "ileri_kontrol"]
    q1, q2, q3 = [o["durum"] for o in kontroller[:3]]
    assert all(
        d["yurutme"].get("kilit_politikasi") == secim.get("kilit_politikasi")
        for d in (q1, q2, q3)
    )
    if not secim:
        assert all("kilit_politikasi" not in d["yurutme"] for d in (q1, q2, q3))
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
    assert r["bolumler"][1]["sayimlar"]["TEST"] == dict(
        kapali_islem=0, ayri_giris_gunu=1, acik_islem=1, bekleyen_giris=0
    )
    assert r["bolumler"][2]["sayimlar"]["TEST"] == dict(
        kapali_islem=0, ayri_giris_gunu=0, acik_islem=0, bekleyen_giris=0
    )
    assert "giris_kohort_sayimlari" in birlesik, "Nihai giriş kohortu sayımı zorunludur"
    assert birlesik["giris_kohort_sayimlari"]["2022Q2"]["TEST"] == dict(
        kapali_islem=1, ayri_giris_gunu=1, acik_islem=0
    )
    assert (
        sum(
            x["TEST"]["kapali_islem"]
            for x in birlesik["giris_kohort_sayimlari"].values()
        )
        == 1
    )


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
    from tansu import deneme

    depo, m, _ = s12_sinyalli(tmp_path, monkeypatch)
    asil = veri.veri_hazirla
    ust = depo.deneme_oku(m.deneme_id)
    test_donemleri = {
        (b["baslangic"].isoformat(), b["bitis"].isoformat()) for b in ust["donemler"]
    }
    test_istekleri = []

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
        if (istek.baslangic, istek.bitis) in test_donemleri:
            test_istekleri.append((istek.baslangic, tuple(istek.semboller)))
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

    assert ("2022-07-01", ("DIGER", "TEST")) in test_istekleri
    assert all(
        "TEST" not in semboller
        for bas, semboller in test_istekleri
        if bas >= "2022-10-01"
    ), "Boş eski üyenin geçmişi yeni fiyat veya ısınma isteği doğurmamalı"
    olaylar = deneme.PilotKayit(depo.yol).oku()
    baslangic = next(
        o for o in olaylar if o["kayit_id"] == r["baslangic_makbuzu"].olay_id
    )
    for tur in ("aktif_kontrol_eksik", "eski_kontrol", "yetim_kontrol"):
        bolum = "2022Q2" if tur == "aktif_kontrol_eksik" else "2022Q4"
        hedef = next(
            o
            for o in olaylar
            if o.get("sonuc_turu") == "ileri_v1" and o["bolum_id"] == bolum
        )
        onceki = olaylar[: olaylar.index(hedef)]
        yanlis = deepcopy(hedef["kayit"])
        if tur == "aktif_kontrol_eksik":
            onceki = [
                o
                for o in onceki
                if not (
                    o["kayit_turu"] == "ileri_kontrol"
                    and o["bolum_id"] == bolum
                    and o["sembol"] == "TEST"
                )
            ]
            yanlis.update(
                deneme._ileri_bolum_kaniti(
                    onceki, ust, r["baslangic_makbuzu"], hedef["kayit"]["donem"]
                )
            )
        else:
            ref = next(x for x in yanlis["kontrol_refleri"] if x["sembol"] == "TEST")
            assert ref["kayit_ref"] == kontroller[-1]["kayit_id"]
            ref["kayit_ref"] = (
                kontroller[0]["kayit_id"]
                if tur == "eski_kontrol"
                else "kayitsiz-kontrol"
            )
        yol = tmp_path / (tur + ".jsonl")
        baytlar = b"".join(deneme.kanonik(o) + b"\n" for o in onceki)
        yol.write_bytes(baytlar)
        kosu = deneme._Kosu(
            deneme.PilotKayit(yol), r["baslangic_makbuzu"], ust, baslangic
        )
        with pytest.raises(deneme.PilotHatasi):
            kosu.ileri_sonucu_kaydet(kayit=yanlis)
        assert yol.read_bytes() == baytlar
        yol.write_bytes(baytlar + deneme.kanonik(hedef | dict(kayit=yanlis)) + b"\n")
        with pytest.raises(deneme.PilotHatasi):
            deneme.PilotKayit(yol).oku()
    kaynak = dict(
        deneme_id=m.deneme_id,
        kosu_id=r["kosu_id"],
        sonuc_ref=r["sonuc_makbuzu"].olay_id,
        bitis_ref=r["bitis_makbuzu"].olay_id,
        icerik_ozeti="00" * 32,
    )
    kabul = deneme._mc_kaynagi(depo.oku(), kaynak, ozet_denetle=False)
    assert kabul["nufus"][0]["cikis_tarih"] == "2022-07-04"
    assert any(
        o["sembol"] == "TEST"
        and o["bolum_id"] == "2022Q3"
        and o["durum"]["son_tarih"] == "2022-07-05"
        for o in kabul["kontroller"]
    )
    boz = deepcopy(depo.oku())
    birlesik = next(o for o in boz if o["kayit_id"] == kaynak["sonuc_ref"])
    birlesik["kayit"]["giris_kohort_sayimlari"]["2022Q2"]["TEST"]["kapali_islem"] += 1
    with pytest.raises(deneme.PilotHatasi):
        deneme._mc_kaynagi(boz, kaynak, ozet_denetle=False)


@pytest.mark.parametrize("eksik", ["isinma", "limit_kaniti"])
def test_s12_eksik_egitim_basarili_secimsiz_donem_degildir(
    tmp_path, monkeypatch, eksik
):
    from tansu import deneme
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

    once = depo.yol.read_bytes()
    monkeypatch.setattr(veri, "oku", lambda *_: None)
    with pytest.raises(deneme.PilotHatasi, match="Başarısız WF"):
        ts.kayitli_ileri_calistir(
            depo,
            m.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            devam_kosu_id=r["kosu_id"],
            ilerleme=None,
        )
    assert depo.yol.read_bytes() == once


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


def varyant_kayitlari(tmp_path, monkeypatch, **secenek):
    from concurrent.futures import ThreadPoolExecutor
    from tansu import aileler, katalog
    from tests.test_kayit import pilot_deneme

    monkeypatch.setattr(
        ts.concurrent.futures,
        "ProcessPoolExecutor",
        lambda *, max_workers, mp_context: ThreadPoolExecutor(max_workers=max_workers),
    )
    depo, ilk, piyasa = s10_kayitli(tmp_path, monkeypatch, **secenek)
    d = depo.deneme_oku(ilk.deneme_id)
    ortak = {
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
    esleme = {
        ad: pilot_deneme(depo, katalog.legacy_coz(ad), **ortak).deneme_id
        for ad in aileler.VARYANTLAR
    }
    return depo, esleme, piyasa


def test_varyant_cli_butun_adlar_donemler_gercek_makbuzlar(tmp_path, monkeypatch):
    import json
    from tansu import __main__, aileler

    depo, esleme, _ = varyant_kayitlari(tmp_path, monkeypatch)
    from tansu import saglamlik

    calistir = saglamlik.ema_hucre_calistir
    kur = aileler.ortak_donem_kurulumu
    kurulumlar = {}

    def kurulum_izle(paket, strateji):
        sonuc = kur(paket, strateji)
        d = paket["referans"]["istenen_donem"]
        for ad, h in sonuc.items():
            gunler = tuple(h["mumlar"].loc[d["baslangic"] : d["bitis"]].index)
            kurulumlar[strateji.varyant, ad, gunler] = h["kurulum"].copy(deep=True)
        return sonuc

    monkeypatch.setattr(aileler, "ortak_donem_kurulumu", kurulum_izle)
    aktarilan = []

    def izle(m, p, **kw):
        ad = next(
            ad for ad, kimlik in esleme.items() if kimlik == kw["yurutme"]["deneme_id"]
        )
        assert p == aileler.VARYANTLAR[ad]
        assert set(kw["kurulum"]) >= {"kutu_alt", "hedef"}
        pd.testing.assert_frame_equal(
            kw["kurulum"], kurulumlar[ad, kw["yurutme"]["sembol"], tuple(m.index)]
        )
        aktarilan.append(ad)
        return calistir(m, p, **kw)

    monkeypatch.setattr(saglamlik, "ema_hucre_calistir", izle)
    harita = tmp_path / "esleme.json"
    harita.write_text(json.dumps(esleme), encoding="utf-8")
    cikti = tmp_path / "cikti"
    try:
        kod = __main__.main(
            [
                "varyant-sinama",
                "--varyant-denemeleri",
                str(harita),
                "--deneme-dosyasi",
                str(depo.yol),
                "--kok",
                str(tmp_path),
                "--rapor",
                str(cikti),
                "--isci",
                "1",
            ]
        )
    except SystemExit as hata:
        kod = hata.code
    assert kod == 0, "Kayıtlı bütün varyantlar destek komutuyla raporlanmalı"
    s = json.loads((cikti / "varyantlar.json").read_text(encoding="utf-8"))
    assert len(s["varyantlar"]) == 24
    assert [v["varyant"] for v in s["varyantlar"]] == list(aileler.VARYANTLAR)
    assert len({v["kosu_id"] for v in s["varyantlar"]}) == 24
    from collections import Counter

    assert Counter(aktarilan) == {ad: 6 for ad in aileler.VARYANTLAR}
    assert s["tur"] == "destek"
    for v in s["varyantlar"]:
        assert v["deneme_id"] == esleme[v["varyant"]]
        assert v["izin_durumu"] == "izinsiz" and v["eski_karsilastirma"]
        assert [d["donem"]["ad"] for d in v["donemler"]] == [
            "2025",
            "2024",
            "2023",
            "2022",
            "2021",
            "birlesik",
        ]
        for d in v["donemler"]:
            assert d["durum"] == "islemsiz"
            assert d["kapali_islem_sayisi"] == 0
            assert d["acik_islemler"] == []
            iz = depo.izle(d["sonuc_ref"])
            assert iz["deneme"]["deneme_id"] == v["deneme_id"]
            assert iz["baslangic"]["mod"] == "gelistirme"
            assert iz["sonuc"]["icerik"]["uyelik"]["gunler"]
            assert "uyelik" not in d and "kalite" not in d
    assert (cikti / "varyantlar.html").exists()
    assert not (kayit.KAYIT_DIZINI / "deneme.jsonl").exists()


@pytest.mark.parametrize(
    "ariza", ["eksik", "fazla", "tekil", "yanlis", "ortak", "izgara"]
)
def test_varyant_butun_kayitlar_hesap_oncesi_dogrulanir(tmp_path, monkeypatch, ariza):
    from decimal import Decimal
    from tansu import deneme, katalog
    from tests.test_kayit import pilot_deneme

    depo, esleme, _ = varyant_kayitlari(tmp_path, monkeypatch)
    if ariza == "eksik":
        esleme.pop("tansu")
    elif ariza == "fazla":
        esleme["yeni"] = "yok"
    elif ariza == "tekil":
        esleme["tansu"] = esleme["bugun"]
    elif ariza == "yanlis":
        esleme["tansu"], esleme["bugun"] = esleme["bugun"], esleme["tansu"]
    else:
        d = depo.deneme_oku(esleme["tansu"])
        ortak = {
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
        if ariza == "ortak":
            ortak["risk_ayarlari"] = d["risk_ayarlari"] | dict(
                nominal_tutar=Decimal("200000")
            )
        strateji = katalog.legacy_coz(
            "tansu", sayisal_ayarlar={"min_gun": 7} if ariza == "izgara" else None
        )
        esleme["tansu"] = pilot_deneme(depo, strateji, **ortak).deneme_id
    once = depo.yol.read_bytes()
    with pytest.raises(deneme.PilotHatasi):
        ts.varyantlari_calistir(depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=None)
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize("asama", ["baslangic", "sonuc", "bitis"])
def test_varyant_yazma_hatasi_onceki_makbuzlari_korur_ve_durdurur(
    tmp_path, monkeypatch, asama
):
    from tansu import deneme

    depo, esleme, _ = varyant_kayitlari(tmp_path, monkeypatch)
    hedef = esleme["tansu"]
    ekle = depo._ekle

    def yaz(olay, *a):
        if olay["deneme_id"] == hedef and olay["kayit_turu"] == asama:
            if asama != "sonuc" or olay["donem"]["ad"] == "2024":
                raise deneme.PilotYazmaHatasi("Kontrollü disk hatası")
        return ekle(olay, *a)

    monkeypatch.setattr(depo, "_ekle", yaz)
    s = ts.varyantlari_calistir(depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=None)
    assert s["durum"] == "hata" and len(s["varyantlar"]) == 24
    ilk, hatali, *sonraki = s["varyantlar"]
    assert ilk["durum"] == "tamamlandi" and len(ilk["donemler"]) == 6
    for r in ilk["donemler"]:
        assert depo.izle(r["sonuc_ref"])["durum"] == "tamamlandi"
    assert hatali["durum"] == "kayit_hatasi"
    assert (
        sum(r["sonuc_ref"] is not None for r in hatali["donemler"])
        == {
            "baslangic": 0,
            "sonuc": 1,
            "bitis": 6,
        }[asama]
    )
    assert all(v["durum"] == "baslamadi" and v["kosu_id"] is None for v in sonraki)
    assert all(
        r["sonuc_ref"] is None and r["kapali_islem_sayisi"] is None
        for v in sonraki
        for r in v["donemler"]
    )
    baslangiclar = [o for o in depo.oku() if o["kayit_turu"] == "baslangic"]
    assert len(baslangiclar) == (1 if asama == "baslangic" else 2)


def test_varyant_eksik_limit_ve_baslangic_reddi_sifir_degildir(tmp_path, monkeypatch):
    depo, esleme, piyasa = varyant_kayitlari(tmp_path, monkeypatch, limit=False)
    s10_kismi_piyasasi(piyasa)
    # İlk varyantın E1 isteği hata verir; diğerleri gerçek E2/E3 yolunu tamamlar.
    hazirla = veri.veri_hazirla

    def eksik(istek, kimlik, kok):
        if len([o for o in depo.oku() if o["kayit_turu"] == "baslangic"]) == 1:
            raise veri.VeriHatasi("TEST fiyatı eksik")
        return hazirla(istek, kimlik, kok)

    monkeypatch.setattr(veri, "veri_hazirla", eksik)
    s = ts.varyantlari_calistir(depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=None)
    assert s["durum"] == "hata"
    assert all(
        r["asama"] == "veri" and r["kapali_islem_sayisi"] is None
        for r in s["varyantlar"][0]["donemler"]
    )
    limitler = [
        r
        for v in s["varyantlar"]
        for r in v["donemler"]
        if r["asama"] == "limit_kaniti"
    ]
    assert limitler and all(
        r["durum"] == "eksik" and r["kapali_islem_sayisi"] is None for r in limitler
    )
    # Manifest değişikliği hiçbir koşu başlatmaz; beklenen yerler korunur.
    once = depo.yol.read_bytes()
    (tmp_path / "ag" / "s10" / "manifest.json").write_text("{}", encoding="utf-8")
    ret = ts.varyantlari_calistir(
        depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=None
    )
    assert ret["durum"] == "hata" and depo.yol.read_bytes() == once
    assert all(v["kosu_id"] is None for v in ret["varyantlar"])
    assert all(
        r["durum"] == "baslamadi" and r["asama"] == "baslangic"
        for v in ret["varyantlar"]
        for r in v["donemler"]
    )


def test_varyant_acik_kismi_islem_ve_tekrar_kimligi(tmp_path, monkeypatch):
    depo, esleme, piyasa = varyant_kayitlari(tmp_path, monkeypatch)
    s10_kismi_piyasasi(piyasa)
    s = ts.varyantlari_calistir(depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=None)
    v = next(v for v in s["varyantlar"] if v["varyant"] == "stop_atr2")
    yil = v["donemler"][4]
    assert yil["durum"] == "acik_kismi", (
        "Açık yarı satış sıfır işlem diye etiketlenemez"
    )
    assert yil["kapali_islem_sayisi"] == 0
    acik = yil["acik_islemler"][0]
    assert acik["sonuc"]["kalan_adet"] == 176
    assert acik["sonuc"]["net_sonuc"] == pytest.approx(1695.1352)
    assert acik["sonuc"]["net_r"] is None
    assert acik["degerleme"] == dict(tarih="2021-12-31", fiyat=122.0)
    assert "islemler" not in yil["semboller"][0]["olcu"]
    once = depo.yol.read_bytes()
    tekrar = ts.varyantlari_calistir(
        depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=None
    )
    assert depo.yol.read_bytes().startswith(once)
    assert {v["kosu_id"] for v in s["varyantlar"]}.isdisjoint(
        v["kosu_id"] for v in tekrar["varyantlar"]
    )
    assert [v["deneme_id"] for v in s["varyantlar"]] == [
        v["deneme_id"] for v in tekrar["varyantlar"]
    ]


@pytest.mark.parametrize(
    "engel",
    [
        "resmi",
        "varyant",
        "kok",
        "kopya",
        "goruntu",
        "girdi",
        "var",
        "dosya",
        "ust_dosya",
    ],
)
def test_varyant_cli_acik_girdi_ve_cikti_sinirini_hesaptan_once_korur(
    tmp_path, monkeypatch, engel
):
    from tansu import __main__

    esleme = tmp_path / "esleme.json"
    esleme.write_text(
        json.dumps({ad: ad for ad in aileler.VARYANTLAR}), encoding="utf-8"
    )
    rapor = tmp_path / "cikti"
    args = [
        "varyant-sinama",
        "--varyant-denemeleri",
        str(esleme),
        "--deneme-dosyasi",
        str(tmp_path / "pilot.jsonl"),
        "--rapor",
        str(rapor),
        "--kok",
        str(tmp_path),
    ]
    if engel == "resmi":
        args += ["--resmi"]
    elif engel == "varyant":
        args += ["--varyant", "tansu"]
    elif engel == "kok":
        args = args[:-2]
    elif engel == "kopya":
        esleme.write_text(
            esleme.read_text(encoding="utf-8")[:-1] + ', "bugun":"ikinci"}',
            encoding="utf-8",
        )
    elif engel == "goruntu":
        args[args.index("--rapor") + 1] = str(tmp_path / "ag" / "s10")
    elif engel == "girdi":
        args[args.index("--rapor") + 1] = str(tmp_path)
        args[args.index("--deneme-dosyasi") + 1] = str(tmp_path / "varyantlar.json")
    elif engel in ("dosya", "ust_dosya"):
        engel_yolu = rapor if engel == "dosya" else tmp_path / "dosya-engeli"
        engel_yolu.write_bytes(b"Onceki dosya kaniti")
        if engel == "ust_dosya":
            args[args.index("--rapor") + 1] = str(engel_yolu / "alt" / "cikti")
    else:
        rapor.mkdir()
        (rapor / "varyantlar.html").write_text("Önceki kanıt", encoding="utf-8")
    cagrilar = []

    def hesap(*a, **kw):
        cagrilar.append(True)
        return dict(durum="tamamlandi", deneme_dosyasi="pilot", varyantlar=[])

    monkeypatch.setattr(ts, "varyantlari_calistir", hesap)
    assert __main__.main(args) == 1
    assert cagrilar == []
    if engel in ("dosya", "ust_dosya"):
        assert engel_yolu.read_bytes() == b"Onceki dosya kaniti"
    if engel == "var":
        assert (rapor / "varyantlar.html").read_text(encoding="utf-8") == "Önceki kanıt"


def test_varyant_belirsiz_yayin_kurtarma_kimligini_saklar(tmp_path, monkeypatch):
    from tansu import deneme

    depo, esleme, _ = varyant_kayitlari(tmp_path, monkeypatch)
    monkeypatch.setattr(
        deneme, "_lf_yaz", lambda *a: (None, OSError("Kontrollü yayın belirsizliği"))
    )
    s = ts.varyantlari_calistir(depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=None)
    v = s["varyantlar"][0]
    assert v["durum"] == "kayit_hatasi"
    assert v["belirsiz_yayin"]["deneme_id"] == esleme["bugun"]
    assert v["belirsiz_yayin"]["kayit_id"] and v["belirsiz_yayin"]["kosu_id"]
    assert v["baslangic_makbuzu"] is None
    assert all(r["sonuc_ref"] is None for v in s["varyantlar"] for r in v["donemler"])


@pytest.mark.parametrize(
    "ad,adet", [("bugun", 15), ("tansu", 15), ("stop_atr15", 20), ("stop_atr2", 15)]
)
@pytest.mark.parametrize("yon", ["yukari", "asagi"])
def test_adlandirilmis_varyant_stop_hedef_ve_yari_dolumlari(ad, adet, yon):
    from tests.test_motor import s09_mumlar, s09_istek, r, STD

    # ATR 5, giriş 100. Kutu/2 ATR stopu 90; 1,5 ATR stopu 92,5.
    # 160 TL risk bütçesi masraf dahil 15 veya 20 adet alır.
    # 115 = giriş + 3 ATR yarıyı, 130 hedefi kalanı satar. Bugün ikisini de kullanmaz.
    satirlar = [r(*STD), r(*STD)] + (
        [r(114, 116, 110, 114), r(129, 131, 125, 129)]
        if yon == "yukari"
        else [r(94, 95, 92, 94)]
    )
    m = s09_mumlar(satirlar)
    k = pd.DataFrame(
        {"kutu_alt": [90.0], "hedef": [None if ad == "bugun" else 130.0]},
        index=m.index[:1],
    )
    d = motor.tara(m, {m.index[0]: "s"}, aileler.VARYANTLAR[ad], k, yurutme=s09_istek())
    islemler = d["islemler"]
    dolumlar = islemler[0]["dolumlar"] if islemler else d["dolumlar"]
    beklenen = [("alis", adet, 100)]
    if yon == "yukari" and ad != "bugun":
        beklenen += (
            [("satis", 10, 115), ("satis", 10, 130)]
            if adet == 20
            else [("satis", 7, 115), ("satis", 8, 130)]
        )
        assert islemler[0]["sonuc"]["net_sonuc"] == pytest.approx(
            442.99125 if adet == 20 else 339.731625
        )
    elif yon == "asagi" and ad == "stop_atr15":
        beklenen += [("satis", 20, 92.5)]
        assert islemler[0]["sonuc"]["net_sonuc"] == pytest.approx(-156.06375)
    else:
        assert d["sonuc"]["kalan_adet"] == adet and d["sonuc"]["net_r"] is None
    assert [(x["yon"], x["adet"], x["fiyat"]) for x in dolumlar] == beklenen


def test_varyant_koordinator_ve_bitis_hatasi_onceki_sonucu_kaybetmez(
    tmp_path, monkeypatch
):
    from tansu import deneme

    depo, esleme, _ = varyant_kayitlari(tmp_path, monkeypatch)
    ekle = depo._ekle

    def yaz(olay, *a):
        if olay["kayit_turu"] == "bitis":
            raise deneme.PilotYazmaHatasi("Bitiş diske yazılamadı")
        return ekle(olay, *a)

    def ilerleme(mesaj):
        raise RuntimeError("İlerleme kanalı kapandı")

    monkeypatch.setattr(depo, "_ekle", yaz)
    s = ts.varyantlari_calistir(
        depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=ilerleme
    )
    v = s["varyantlar"][0]
    assert v["durum"] == "kayit_hatasi"
    ilk = v["donemler"][0]
    assert ilk["sonuc_ref"] is not None, (
        "İkinci hata önceki gerçek dönem makbuzunu kaybettiremez"
    )
    assert depo.izle(ilk["sonuc_ref"])["durum"] == "cozumsuz"
    assert all(x["kosu_id"] is None for x in s["varyantlar"][1:])


def test_pay_kimligi_kayitli_e4_bir_payda_isinir_ve_gecmis_uyeligi_korur(
    tmp_path, monkeypatch
):
    import datetime as dt
    from decimal import Decimal
    from tansu import deneme, katalog
    from tests.test_kayit import pilot_deneme
    from tests.test_veri import pay_kimlikli_goruntu

    seanslar = sorted(
        [
            f"{y}-{a}"
            for y in range(2021, 2026)
            for a in ("01-04", "01-05", "12-30", "12-31")
        ]
        + ["2025-11-20", "2025-11-21", "2025-11-24", "2025-11-25"]
    )
    uyelik = veri.uyelik_hazirla(
        veri.UyelikIstegi(tuple(seanslar), "donemsel_bist30_v1", "bist30_2021_2025_v1")
    )
    kaynak_sembolleri = sorted(
        {
            {"KOZAA": "TRMET", "KOZAL": "TRALT"}.get(s, s)
            for g in uyelik["gunler"].values()
            for s in g["semboller"]
        }
    )
    tarihler = [
        t.date().isoformat() for t in pd.bdate_range("2018-01-01", periods=510)
    ] + seanslar
    a, secim = pay_kimlikli_goruntu(
        tmp_path, monkeypatch, tarihler=tarihler, semboller=kaynak_sembolleri
    )
    veri_ayarlari = dict(
        veri_referanslari=[a.kimlik],
        manifest_ozeti=secim["manifest_ozeti"],
        uyelik_surumu="bist30_2021_2025_v1",
        uyelik_ozeti=uyelik["tablo_parmak_izi"],
        evren_politikasi="donemsel_bist30_v1",
        kaynak="is_yatirim",
        kalite_surumu="legacy_tansu_v1",
        duzeltme_surumu="is_yatirim",
        takvim_ref="xu100",
        pay_kimligi=secim,
        takvim=dict(
            baslangic=dt.date(2021, 1, 1),
            bitis=dt.date(2025, 12, 31),
            seanslar=seanslar,
            kaynak_ref="sentetik mühürlü E1 takvimi",
        ),
    )
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
    depo = deneme.PilotKayit(tmp_path / "pay-kosusu.jsonl")
    makbuz = pilot_deneme(
        depo,
        katalog.legacy_coz("bugun"),
        donemler=donemler,
        veri_ayarlari=veri_ayarlari,
        yontem_ayarlari=ts.KAYITLI_YONTEM,
        risk_ayarlari=dict(
            risk_surumu="bagimsiz_risk_v1", nominal_tutar=Decimal("100000")
        ),
        masraf_ayarlari=dict(masraf_surumu="komisyon_bsmv_v1"),
    )
    sonuc = ts.kayitli_calistir(
        depo,
        makbuz.deneme_id,
        veri_koku=tmp_path,
        mod="gelistirme",
        isci=1,
        ilerleme=None,
    )
    assert sonuc["durum"] == "tamamlandi", sonuc["donemler"]
    ilk = sonuc["donemler"][0]
    assert "pay_kimligi_v1/p002" in ilk["durumlar"]
    assert not {"KOZAL", "TRALT"}.intersection(ilk["durumlar"])
    assert ilk["isinma"]["pay_kimligi_v1/p002"]["tamam"] is True
    assert ilk["veri_referansi"]["pay_kimligi"] == secim
    assert len(ilk["uyelik"]["gunler"]["2025-11-21"]["semboller"]) == 30
    assert len(ilk["uyelik"]["gunler"]["2025-11-24"]["semboller"]) == 30
    eski = next(
        k
        for k in ilk["uyelik"]["gunler"]["2025-11-21"]["kanitlar"]
        if k["pay_id"] == "pay_kimligi_v1/p002"
    )
    yeni = next(
        k
        for k in ilk["uyelik"]["gunler"]["2025-11-24"]["kanitlar"]
        if k["pay_id"] == "pay_kimligi_v1/p002"
    )
    assert (eski["sembol"], yeni["sembol"]) == ("KOZAL", "TRALT")
    assert depo.deneme_oku(makbuz.deneme_id)["veri_ayarlari"]["pay_kimligi"] == secim


def test_grup_pay_kimligi_statik_kapsami_cozer_hesap_cagirmaz(tmp_path, monkeypatch):
    from hashlib import sha256
    from tansu import deneme
    from tests.test_veri import pay_kimlikli_goruntu

    tanim = grup_hazirlik_girdisi(tmp_path)
    a, secim = pay_kimlikli_goruntu(tmp_path / "pay", monkeypatch)
    takvim = tmp_path / "pay-takvim.json"
    takvim.write_text(
        json.dumps(
            dict(
                baslangic="2025-11-20",
                bitis="2025-11-25",
                seanslar=["2025-11-20", "2025-11-21", "2025-11-24", "2025-11-25"],
                kaynak_ref="sentetik kesin takvim",
            )
        ),
        encoding="utf-8",
    )
    tanim["seanslar"] = ["2025-11-21", "2025-11-24", "2025-11-25"]
    tanim["isinma_baslangici"] = "2025-11-20"
    tanim["hisse_kurali"]["semboller"] = ["KOZAL"]
    tanim["referanslar"].update(
        anlik_goruntu=a.kimlik,
        manifest_ozeti=secim["manifest_ozeti"],
        pay_kimligi=secim,
        takvim=dict(yol=str(takvim), sha256=sha256(takvim.read_bytes()).hexdigest()),
    )

    def yasak(*a, **k):
        pytest.fail("Statik hazırlık E1 kalite veya gösterge hesabı çağıramaz")

    monkeypatch.setattr(veri, "veri_hazirla", yasak)
    monkeypatch.setattr(aileler, "ortak_donem_kurulumu", yasak)
    depo = deneme.PilotKayit(tmp_path / "grup-pay.jsonl")
    sonuc = ts.grup_hazirla(depo, tanim, veri_koku=tmp_path / "pay")
    assert sonuc["dislamalar"] == []
    assert {e["alan"] for e in sonuc["engeller"]} == {
        "strateji_revizyonlari.kaynak-a.deneme_id"
    }
    assert sonuc["yurutme_izni"] is False
    assert all(o["kayit_turu"] == "grup_hazirligi" for o in depo.oku())


def test_pay_kimligi_kod_sinirinda_giris_acik_ve_bekleyen_cikis_kopmaz(
    tmp_path, monkeypatch
):
    from tests.test_veri import pay_kimlikli_goruntu, satir
    from tests.test_motor import r, s09_istek, s09_mumlar

    tarihler = ["2025-11-19", "2025-11-20", "2025-11-21", "2025-11-24", "2025-11-25"]
    degerler = [
        (100, 101, 99, 100),
        (100, 101, 99, 100),
        (90, 90, 90, 90),
        (85, 85, 85, 85),
        (80, 82, 79, 81),
    ]
    fiyatlar = [
        dict(
            satir(t, k, k),
            aof=a,
            ham_aof=a,
            yuksek=y,
            ham_yuksek=y,
            dusuk=d,
            ham_dusuk=d,
        )
        for t, (a, y, d, k) in zip(tarihler, degerler, strict=True)
    ]
    a, secim = pay_kimlikli_goruntu(
        tmp_path, monkeypatch, tarihler=tarihler, ek_fiyat={"TRALT": fiyatlar}
    )
    istek = veri.VeriIstegi(
        ("KOZAL",),
        tarihler[0],
        tarihler[-1],
        "is_yatirim",
        "legacy_tansu_v1",
        "bist30_2021_2025_v1",
        "is_yatirim",
        "xu100",
        evren_politikasi="donemsel_bist30_v1",
        pay_kimligi=secim,
    )
    paket = veri.veri_hazirla(istek, a.kimlik, tmp_path)
    pay = paket["semboller"][0]
    m = s09_mumlar([r(*d) for d in degerler])
    m.index = pd.DatetimeIndex(tarihler)
    for alan in ("aof", "yuksek", "dusuk", "kapanis"):
        m[alan] = [x["duzeltilmis_" + alan]["deger"] for x in paket["piyasa"]]
    m.loc[m.index[2:4], "taban"] = [90, 85]
    yurutme = s09_istek(sembol=pay, veri_ref_id=paket["referans"]["kayit_id"])
    ara = motor.tara(m.iloc[:3], {m.index[0]: "sinyal-eski-kod"}, yurutme=yurutme)
    assert ara["pozisyon"]["bekleyen"] is not None
    son = motor.tara(m.iloc[3:], {}, yurutme=yurutme, onceki_durum=ara)
    assert len(son["islemler"]) == 1
    assert [d["tarih"] for d in son["islemler"][0]["dolumlar"]] == [
        "2025-11-20",
        "2025-11-25",
    ]
    assert son["ertelenen_satis_gunu_sayisi"] == 2
    assert son["islemler"][0]["pozisyon"]["risk_girdisi"]["sembol"] == pay
    giris = motor.tara(m.iloc[2:4], {m.index[2]: "sinyal-cuma"}, yurutme=yurutme)
    assert giris["dolumlar"][0]["tarih"] == "2025-11-24"
    assert [x["borsa_kodu"] for x in paket["piyasa"]] == ["KOZAL"] * 3 + ["TRALT"] * 2


@pytest.mark.parametrize("boz", ["surum", "fazla", "manifest", "tablo"])
def test_pay_kimligi_kayitli_hata_hesaba_ve_onbellege_girmez(
    tmp_path, monkeypatch, boz
):
    from pathlib import Path
    from hashlib import sha256
    from tansu import katalog
    from tests.test_kayit import pilot_deneme

    depo, eski, _ = s10_kayitli(tmp_path, monkeypatch)
    onceki = depo.deneme_oku(eski.deneme_id)
    v = onceki["veri_ayarlari"]
    tablo = Path(veri.__file__).parent / "referans" / "pay_kimligi_v1" / "eslemeler.csv"
    secim = dict(
        surum="pay_kimligi_v1",
        tablo_ozeti=sha256(tablo.read_bytes()).hexdigest(),
        kaynak=v["kaynak"],
        goruntu_id="s10",
        manifest_ozeti=v["manifest_ozeti"],
    )
    if boz == "surum":
        secim["surum"] = "bilinmeyen"
    elif boz == "fazla":
        secim["otomatik"] = True
    elif boz == "manifest":
        secim["manifest_ozeti"] = "e" * 64
    else:
        secim["tablo_ozeti"] = "f" * 64
    v["pay_kimligi"] = secim
    yeni = pilot_deneme(
        depo,
        katalog.legacy_coz("bugun"),
        **{
            a: onceki[a]
            for a in (
                "donemler",
                "veri_ayarlari",
                "yontem_ayarlari",
                "risk_ayarlari",
                "masraf_ayarlari",
            )
        },
    )
    assert yeni.ayar_ozeti != eski.ayar_ozeti

    def yasak(*a, **k):
        pytest.fail(
            "Hatalı kimlik E1/E2/E3 hesabına veya yeniden kullanılan pakete ulaşamaz"
        )

    monkeypatch.setattr(veri, "veri_hazirla", yasak)
    monkeypatch.setattr(aileler, "ortak_donem_kurulumu", yasak)
    monkeypatch.setattr(motor, "tara", yasak)
    if boz == "tablo":
        sonuc = ts.kayitli_calistir(
            depo,
            yeni.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            isci=1,
            ilerleme=None,
        )
        assert sonuc["durum"] == "hata"
        assert all("tablo özeti" in s["neden"] for s in sonuc["donemler"])
        assert all(s["veri_referansi"] is None for s in sonuc["donemler"])
    else:
        with pytest.raises((ValueError, veri.VeriHatasi), match="[Pp]ay kimliği"):
            ts.kayitli_calistir(
                depo,
                yeni.deneme_id,
                veri_koku=tmp_path,
                mod="gelistirme",
                isci=1,
                ilerleme=None,
            )
        assert len(depo.oku()) == 2


def test_s12_pay_kimligi_secim_sinyal_ve_tasinan_durumda_ayni_paydir(
    tmp_path, monkeypatch
):
    from copy import deepcopy
    from tansu import deneme
    from tests.test_kayit import pilot_deneme
    from tests.test_veri import pay_kimlikli_goruntu, satir

    asil_uyelik, asil_e1 = veri.uyelik_hazirla, veri.veri_hazirla
    depo, eski, _ = s12_sinyalli(tmp_path, monkeypatch)
    d = depo.deneme_oku(eski.deneme_id)
    v = d["veri_ayarlari"]
    seanslar = v["takvim"]["seanslar"]
    uyelik = asil_uyelik(
        veri.UyelikIstegi(tuple(seanslar), v["evren_politikasi"], v["uyelik_surumu"])
    )
    semboller = sorted(
        {
            {"KOZAA": "TRMET", "KOZAL": "TRALT"}.get(s, s)
            for u in uyelik["gunler"].values()
            for s in u["semboller"]
        }
    )
    tarihler = [
        t.date().isoformat() for t in pd.bdate_range("2018-01-01", periods=510)
    ] + list(seanslar)
    fiyatlar = []
    for t in tarihler:
        fiyat = 110.0 if t in ("2021-04-04", "2022-07-04") else 100.0
        fiyatlar.append(
            dict(
                satir(t, fiyat, fiyat),
                ham_yuksek=fiyat + 1,
                ham_dusuk=fiyat - 1,
                yuksek=fiyat + 1,
                dusuk=fiyat - 1,
            )
        )
    a, secim = pay_kimlikli_goruntu(
        tmp_path,
        monkeypatch,
        tarihler=tarihler,
        semboller=semboller,
        ek_fiyat={"TRALT": fiyatlar},
    )
    v.update(
        veri_referanslari=[a.kimlik],
        manifest_ozeti=secim["manifest_ozeti"],
        uyelik_ozeti=uyelik["tablo_parmak_izi"],
        pay_kimligi=secim,
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
    istekler = []

    def e1(istek, *args):
        istekler.append(istek)
        if istek.baslangic >= "2022-07-01" or istek.baslangic == "2021-07-01":
            raise ValueError("sentetik iki çeyrek sınırı")
        paket = asil_e1(istek, *args)
        # Sentetik dolum kanıtı; gerçek veri veya resmi günlük limit iddiası değildir.
        for r in paket["piyasa"]:
            r.update(
                tavan=dict(deger=200.0),
                taban=dict(deger=50.0),
                limit_kaniti="sentetik açık limit kanıtı",
            )
        return paket

    monkeypatch.setattr(veri, "uyelik_hazirla", asil_uyelik)
    monkeypatch.setattr(veri, "veri_hazirla", e1)
    sonuc = s12_calistir(depo, m, tmp_path)
    ilk, ikinci = sonuc["bolumler"][:2]
    assert ilk["durum"] == ikinci["durum"] == "tamamlandi", [
        (b["bolum_id"], b["neden"]) for b in sonuc["bolumler"][:3]
    ]
    assert istekler and all(i.pay_kimligi == secim for i in istekler)
    assert all(not {"KOZAL", "TRALT"}.intersection(i.semboller) for i in istekler)
    assert all(
        s["sembol"] != "KOZAL" and s["sembol"] != "TRALT"
        for b in (ilk, ikinci)
        for s in b["secimler"]
    )
    olaylar = depo.oku()
    sinyal = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_sinyal" and o["sembol"] == "pay_kimligi_v1/p002"
    )
    assert sinyal["sinyal"]["veri_ref"]["pay_kimligi"] == secim
    kontroller = [
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_kontrol" and o["sembol"] == "pay_kimligi_v1/p002"
    ]
    q1, q2 = [o["durum"] for o in kontroller[:2]]
    assert q1["durum"] == "bekliyor"
    assert q2["durum"] == "acik_son"
    assert q1["pozisyon"]["risk_girdisi"]["sinyal_id"] == sinyal["kayit_id"]
    assert q2["pozisyon"]["risk_girdisi"]["sinyal_id"] == sinyal["kayit_id"]
    assert kontroller[1]["onceki_ref"] == kontroller[0]["kayit_id"]

    # Gereken pay kümesi çağıranın eksilttiği güncel kayıtlardan türetilemez.
    bolum = next(
        o
        for o in olaylar
        if o.get("sonuc_turu") == "ileri_v1" and o["kayit"]["bolum_id"] == "2022Q1"
    )
    eksik = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_kontrol"
        and o["bolum_id"] == "2022Q1"
        and o["sembol"] == "AKBNK"
    )
    onceki = [o for o in olaylar[: olaylar.index(bolum)] if o is not eksik]
    yanlis = deepcopy(bolum)
    k = yanlis["kayit"]
    k["kontrol_refleri"] = [r for r in k["kontrol_refleri"] if r["sembol"] != "AKBNK"]
    del k["sayimlar"]["AKBNK"]
    k["uyarilar"] = [r for r in k["uyarilar"] if r["sembol"] != "AKBNK"]
    k["olaylar"] = [r for r in k["olaylar"] if r["sembol"] != "AKBNK"]
    yol = tmp_path / "eksik-pay-kontrolu.jsonl"
    onceki_bayt = b"".join(deneme.kanonik(o) + b"\n" for o in onceki)
    yol.write_bytes(onceki_bayt)
    baslangic = next(
        o for o in onceki if o["kayit_id"] == sonuc["baslangic_makbuzu"].olay_id
    )
    kosu = deneme._Kosu(
        deneme.PilotKayit(yol),
        sonuc["baslangic_makbuzu"],
        depo.deneme_oku(m.deneme_id),
        baslangic,
    )
    with pytest.raises(deneme.PilotHatasi, match="başarı durumu"):
        kosu.ileri_sonucu_kaydet(kayit=k)
    assert yol.read_bytes() == onceki_bayt
    yol.write_bytes(onceki_bayt + deneme.kanonik(yanlis) + b"\n")
    with pytest.raises(deneme.PilotHatasi, match="Bozuk tam satır") as hata:
        deneme.PilotKayit(yol).oku()
    assert "başarı durumu" in str(hata.value.__cause__)


@pytest.mark.parametrize("giris", ["s10", "s11"])
def test_kayitli_ham_aralik_yontemi_gercek_dolum_ve_cocukta_korunur(
    tmp_path, monkeypatch, giris
):
    hazirla, calistir = (
        (s10_kayitli, s10_calistir) if giris == "s10" else (s11_kayitli, s11_calistir)
    )
    depo, m, piyasa = hazirla(
        tmp_path,
        monkeypatch,
        sinyal=True,
        limit=False,
        kilit_politikasi="ham_aralik_v1",
    )
    # E1 karışık satırları: gerçek None, DataFrame dönüşümünde NaN kanıtı olmasın.
    piyasa[0].update(
        tavan=dict(deger=200.0),
        taban=dict(deger=50.0),
        limit_kaniti="sentetik açık limit kanıtı",
    )
    r = calistir(depo, m, tmp_path)
    assert r["durum"] == "tamamlandi"
    olaylar = depo.oku()
    durumlar = [
        d
        for o in olaylar
        if o.get("sonuc_turu") == "donem_v1"
        for d in o["icerik"]["durumlar"].values()
    ]
    assert any(d["dolumlar"] for d in durumlar)
    assert all(d["yurutme"]["kilit_politikasi"] == "ham_aralik_v1" for d in durumlar)
    for o in olaylar:
        if o["kayit_turu"] == "deneme" and o["ust_deneme_id"] == m.deneme_id:
            assert o["yontem_ayarlari"]["kilit_politikasi"] == "ham_aralik_v1"
    from tansu.deneme import PilotKayit

    assert PilotKayit(depo.yol).oku() == olaylar


@pytest.mark.parametrize("giris", ["s10", "s11", "s12"])
def test_kayitli_bilinmeyen_kilit_politikasi_baslangic_yazmaz(
    tmp_path, monkeypatch, giris
):
    from tansu.deneme import PilotHatasi

    hazirla, calistir = {
        "s10": (s10_kayitli, s10_calistir),
        "s11": (s11_kayitli, s11_calistir),
        "s12": (s12_kayitli, s12_calistir),
    }[giris]
    depo, m, _ = hazirla(tmp_path, monkeypatch)
    from copy import deepcopy

    y = deepcopy(depo.deneme_oku(m.deneme_id)["yontem_ayarlari"])
    hucre = y if giris == "s10" else y["hucre_yontemi"]
    hucre["kilit_politikasi"] = "bilinmeyen"
    if giris == "s12":
        once = depo.yol.read_bytes()
        with pytest.raises(PilotHatasi, match="yürütme ayarı"):
            s10_revizyon(depo, m, yontem_ayarlari=y)
    else:
        m = s10_revizyon(depo, m, yontem_ayarlari=y)
        once = depo.yol.read_bytes()
        with pytest.raises(PilotHatasi, match="yürütme ayarı"):
            calistir(depo, m, tmp_path)
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize("kanit", [None, float("nan"), ""])
def test_s10_ham_aralik_kismi_ve_bozuk_pandas_kaniti_basarili_yapmaz(
    tmp_path, monkeypatch, kanit
):
    depo, m, piyasa = s10_kayitli(
        tmp_path,
        monkeypatch,
        sinyal=True,
        limit=False,
        kilit_politikasi="ham_aralik_v1",
    )
    for satir in piyasa:
        if satir["tarih"] >= "2021-01-01":
            satir["tavan"] = dict(deger=200.0)
            satir["limit_kaniti"] = kanit
    r = s10_calistir(depo, m, tmp_path)
    assert r["durum"] == "hata"
    assert any(d["hatalar"] for d in r["donemler"])
    neden = "limit_bilinmiyor" if kanit is None else "geçersiz sayısal limit girdisi"
    assert any(h["neden"] == neden for d in r["donemler"] for h in d["hatalar"])
    assert not any(d["dolumlar"] for x in r["donemler"] for d in x["durumlar"].values())


def test_s10_eski_karisik_limit_gosterimi_kayitli_durum_devamini_korur(
    tmp_path, monkeypatch
):
    # TASARIM 5.15: seçenek yokken eski float/None uyarlaması ve gün özeti korunur.
    depo, m, piyasa = s10_kayitli(tmp_path, monkeypatch, sinyal=True, limit=False)
    for satir in piyasa:
        if satir["tarih"] >= "2021-01-01":
            satir.update(
                tavan=dict(deger=200),
                taban=dict(deger=50),
                limit_kaniti="sentetik kanıt",
            )
    from concurrent.futures import ThreadPoolExecutor

    # Gözlemci aynı süreçte çalışır; E2/E3/E4/E5 ve sonuçlar gerçektir.
    monkeypatch.setattr(
        ts.concurrent.futures,
        "ProcessPoolExecutor",
        lambda *, max_workers, mp_context: ThreadPoolExecutor(max_workers=max_workers),
    )
    asil = ts.saglamlik.ema_hucre_calistir
    cagrilar = []

    def izle(mumlar, p, **ayarlar):
        cagrilar.append((mumlar.copy(), p, ayarlar))
        return asil(mumlar, p, **ayarlar)

    monkeypatch.setattr(ts.saglamlik, "ema_hucre_calistir", izle)
    sonuc = s10_calistir(depo, m, tmp_path)
    assert sonuc["durum"] == "tamamlandi"
    mumlar, p, ayarlar = cagrilar[4]
    # Eski sözleşmede karışık tamsayı/None sınır sütunu float olur.
    eski = asil(mumlar.assign(tavan=200.0, taban=50.0), p, **ayarlar)

    kayitli = json.loads(json.dumps(eski))
    hata = None
    try:
        devam = asil(mumlar.iloc[-1:], p, **(ayarlar | dict(onceki_durum=kayitli)))
    except ValueError as exc:
        hata = str(exc)
    assert hata is None, hata
    assert devam == kayitli
    assert sonuc["donemler"][4]["durumlar"]["TEST"] == eski


@pytest.mark.parametrize("giris", ["s10", "s11", "s12"])
@pytest.mark.parametrize("tekrar", [False, 0.0])
def test_kayitli_yontem_tamsayi_alanini_esdeger_turle_genisletmez(
    tmp_path, monkeypatch, giris, tekrar
):
    from copy import deepcopy
    from tansu.deneme import PilotHatasi

    hazirla, calistir = {
        "s10": (s10_kayitli, s10_calistir),
        "s11": (s11_kayitli, s11_calistir),
        "s12": (s12_kayitli, s12_calistir),
    }[giris]
    depo, m, _ = hazirla(tmp_path, monkeypatch)
    y = deepcopy(depo.deneme_oku(m.deneme_id)["yontem_ayarlari"])
    hucre = y if giris == "s10" else y["hucre_yontemi"]
    hucre["tekrar"] = tekrar
    hata = None
    if giris in ("s10", "s12"):
        once = depo.yol.read_bytes()
        try:
            s10_revizyon(depo, m, yontem_ayarlari=y)
        except PilotHatasi as exc:
            hata = str(exc)
    else:
        m = s10_revizyon(depo, m, yontem_ayarlari=y)
        once = depo.yol.read_bytes()
        try:
            calistir(depo, m, tmp_path)
        except PilotHatasi as exc:
            hata = str(exc)
    assert hata is not None
    assert ("tamsayı" if giris == "s10" else "yürütme ayarı") in hata
    assert depo.yol.read_bytes() == once


def dogal_isinma_kayitli(tmp_path, monkeypatch, *, seyrek=False):
    """Mühürlü E1 girdisi; tarihli otuz üye ve gerçek E2/E3/E4/E5."""
    import datetime as dt
    from decimal import Decimal
    from hashlib import sha256
    from pathlib import Path
    from tansu import deneme, katalog
    from tests.test_kayit import pilot_deneme
    from tests.test_veri import SahteKaynak, SIMDI, satir

    gunler = sorted(
        set(
            [t.date().isoformat() for t in pd.bdate_range("2023-01-18", periods=500)]
            + [
                "2021-01-04",
                "2021-12-31",
                "2022-01-03",
                "2022-12-30",
                "2024-12-18",
                "2024-12-31",
                "2025-01-02",
                "2025-02-06",
                "2025-10-01",
                "2025-12-31",
            ]
        )
    )
    if seyrek:
        gunler = sorted(
            {
                f"{y}-{a:02d}-{g:02d}"
                for y in range(2021, 2026)
                for a in (1, 4, 7, 10)
                for g in (4, 5)
            }
            | {"2023-01-18", "2025-02-06"}
        )
    uyelik = veri.uyelik_hazirla(
        veri.UyelikIstegi(tuple(gunler), "donemsel_bist30_v1", "bist30_2021_2025_v1")
    )
    semboller = sorted({s for g in uyelik["gunler"].values() for s in g["semboller"]})
    tarihler = [
        t.date().isoformat() for t in pd.bdate_range("2018-01-01", periods=510)
    ] + gunler
    fiyat = {}
    for s in semboller:
        ilk = {"ASTOR": "2023-01-18", "DSTKF": "2025-02-06"}.get(s, "2018-01-01")
        if seyrek and s == "AKBNK":
            ilk = "2021-01-04"
        fiyat[s] = []
        for t in tarihler:
            if t < ilk:
                continue
            c = (
                110.0
                if s == "ASTOR" and t == "2024-12-16"
                else 112.0
                if s == "ASTOR" and t >= "2024-12-17"
                else 100.0
            )
            fiyat[s].append(
                satir(t, c, c)
                | dict(ham_yuksek=c + 1, ham_dusuk=c - 1, yuksek=c + 1, dusuk=c - 1)
            )
    kimlik = veri.indir(
        semboller, tmp_path, SahteKaynak(fiyat, {s: [] for s in semboller}), simdi=SIMDI
    )
    manifest = sha256(
        (tmp_path / "ag" / kimlik / "manifest.json").read_bytes()
    ).hexdigest()
    kok = tmp_path / "referans"
    hedef = kok / "ilk_islem_v1"
    hedef.mkdir(parents=True)
    depo_tablo = (
        Path(veri.__file__).parent / "referans" / "ilk_islem_v1" / "ilk_islem.csv"
    )
    tablo = pd.read_csv(depo_tablo, encoding="utf-8", dtype=str, keep_default_na=False)
    tablo["goruntu_id"], tablo["manifest_ozeti"] = kimlik, manifest
    if seyrek:
        # Yalnız sentetik kaynağın ilk gün olgusu; üretim tablosu değişmez.
        maske = tablo["kaynak_sembolu"] == "ASTOR"
        tablo.loc[
            maske,
            [
                "kaynak_sembolu",
                "borsa_kodu",
                "unvan",
                "ilk_islem_gunu",
                "yayim_tarihi",
                "kaynak_id",
                "kaynak_url",
            ],
        ] = [
            "AKBNK",
            "AKBNK",
            "Sentetik genç pay",
            "2021-01-04",
            "2021-01-03",
            "fixture-ilk-gun",
            "https://example.invalid/ilk-gun",
        ]
    tablo.to_csv(
        hedef / "ilk_islem.csv", index=False, encoding="utf-8", lineterminator="\n"
    )
    secim = dict(
        surum="ilk_islem_v1",
        tablo_ozeti=sha256((hedef / "ilk_islem.csv").read_bytes()).hexdigest(),
        kaynak="is_yatirim",
        goruntu_id=kimlik,
        manifest_ozeti=manifest,
    )
    monkeypatch.setattr(veri, "ILK_ISLEM_KOKU", kok)
    monkeypatch.setitem(
        veri._YAYIMLANMIS_KAYNAK_OZETLERI, "ilk_islem_v1", secim["tablo_ozeti"]
    )
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
    v = dict(
        veri_referanslari=[kimlik],
        manifest_ozeti=manifest,
        uyelik_surumu="bist30_2021_2025_v1",
        uyelik_ozeti=uyelik["tablo_parmak_izi"],
        evren_politikasi="donemsel_bist30_v1",
        kaynak="is_yatirim",
        kalite_surumu="legacy_tansu_v1",
        duzeltme_surumu="is_yatirim",
        takvim_ref="xu100",
        ilk_islem=secim,
        takvim=dict(
            baslangic=dt.date(2021, 1, 1),
            bitis=dt.date(2025, 12, 31),
            seanslar=gunler,
            kaynak_ref="mühürlü sentetik gözlem takvimi",
        ),
    )
    depo = deneme.PilotKayit(tmp_path / "dogal.jsonl")
    m = pilot_deneme(
        depo,
        katalog.legacy_coz("bugun"),
        donemler=donemler,
        veri_ayarlari=v,
        yontem_ayarlari=ts.KAYITLI_YONTEM
        | dict(
            isinma_politikasi="kaynakli_isinma_v1", kilit_politikasi="ham_aralik_v1"
        ),
        risk_ayarlari=dict(
            risk_surumu="bagimsiz_risk_v1", nominal_tutar=Decimal("100000")
        ),
        masraf_ayarlari=dict(masraf_surumu="komisyon_bsmv_v1"),
    )
    return depo, m, gunler


def test_s10_dogal_isinma_donem_icinde_500_olur_uyeyi_dusurmez(tmp_path, monkeypatch):
    depo, m, _ = dogal_isinma_kayitli(tmp_path, monkeypatch)
    sonuc = s10_calistir(depo, m, tmp_path)
    assert sonuc["durum"] == "tamamlandi", [
        (r["donem"]["ad"], r["hatalar"]) for r in sonuc["donemler"]
    ]
    r = sonuc["donemler"][1]
    dogal = r["isinma"]["ASTOR"]["dogal_bekleyis"]
    assert dogal["isinma_tamamlanma_gunu"] == "2024-12-17"
    assert r["isinma"]["ASTOR"]["tamam"] is False
    adaylar = [a for a in r["adaylar"] if "ASTOR" in a["semboller"]]
    assert [a["tarih"] for a in adaylar] == ["2024-12-17"]
    assert r["durumlar"]["ASTOR"]["dolumlar"][0]["tarih"] == "2024-12-18"
    son = sonuc["donemler"][0]
    assert "DSTKF" in son["durumlar"]
    assert son["isinma"]["DSTKF"]["dogal_bekleyis"]["isinma_tamamlanma_gunu"] is None
    assert son["isinma"]["DSTKF"]["gozlem"] == 2
    assert not any("DSTKF" in a["semboller"] for a in son["adaylar"])
    assert "dogal_bekleyis" not in son["isinma"]["AKBNK"]
    assert all(
        not any(h["asama"] == "isinma" for h in r["hatalar"]) for r in sonuc["donemler"]
    )


def dogal_isinma_ileri_kayitli(tmp_path, monkeypatch):
    import datetime as dt
    from tests.test_kayit import pilot_deneme

    depo, eski, _ = dogal_isinma_kayitli(tmp_path, monkeypatch, seyrek=True)
    d = depo.deneme_oku(eski.deneme_id)
    donemler = []
    for yil in range(2022, 2026):
        for q, ay in enumerate((1, 4, 7, 10), 1):
            bas = dt.date(yil, ay, 1)
            sonraki = dt.date(yil + (ay == 10), 1 if ay == 10 else ay + 3, 1)
            egitim = dict(
                ad=f"{yil}Q{q}:egitim",
                baslangic=dt.date(yil - 1, ay, 1),
                bitis=bas - dt.timedelta(days=1),
                isinma_baslangici=dt.date(2018, 1, 1),
                sinir_surumu="surekli_ileri_v1",
            )
            donemler.append(
                dict(
                    ad=f"{yil}Q{q}",
                    baslangic=bas,
                    bitis=sonraki - dt.timedelta(days=1),
                    isinma_baslangici=dt.date(2018, 1, 1),
                    sinir_surumu="surekli_ileri_v1",
                    egitim=egitim,
                )
            )
    y = dict(
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
        yontem_ayarlari=y,
        **{a: d[a] for a in ("veri_ayarlari", "risk_ayarlari", "masraf_ayarlari")},
    )
    return depo, m


def test_s12_dogal_bekleyis_diger_uyenin_egitimini_bozmaz_secim_uretmez(
    tmp_path, monkeypatch
):
    from copy import deepcopy
    from tansu import deneme as deneme_

    depo, m = dogal_isinma_ileri_kayitli(tmp_path, monkeypatch)
    asil = veri.veri_hazirla

    def sinirli(istek, *args):
        if istek.baslangic == "2022-04-01":
            raise ValueError("sentetik ikinci çeyrek veri sınırı")
        return asil(istek, *args)

    monkeypatch.setattr(veri, "veri_hazirla", sinirli)
    sonuc = s12_calistir(depo, m, tmp_path)
    ilk = sonuc["bolumler"][0]
    assert ilk["durum"] == "tamamlandi", ilk
    secimler = {s["sembol"]: s for s in ilk["secimler"]}
    genc, diger = secimler["AKBNK"], secimler["EREGL"]
    assert genc["durum"] == diger["durum"] == "secim_yok"
    assert genc["test_deneme_id"] is None and diger["test_deneme_id"] is None
    assert all(h["durum"] == "islemsiz" for h in diger["egitim_cocuklari"])
    assert all(
        h["dogal_bekleyis"]["neden"] == "dogal_isinma" for h in genc["egitim_cocuklari"]
    )
    assert ilk["isinma"]["AKBNK"]["dogal_bekleyis"]["isinma_tamamlanma_gunu"] is None
    assert not ilk["adaylar"]
    olaylar = depo.oku()
    assert not any(o["kayit_turu"] == "ileri_sinyal" for o in olaylar)
    assert sonuc["durum"] == "hata"
    assert "sentetik ikinci çeyrek veri sınırı" in str(sonuc["bolumler"][1]["hatalar"])
    # Aynı gerçek çocukla uyuşmayan özet hem ekleme hem taze okumada reddedilir.
    hedef = next(
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_secim" and o["sembol"] == "AKBNK"
    )
    on = olaylar[: olaylar.index(hedef)]
    yanlis = deepcopy(hedef)
    yanlis["kayit"]["egitim_cocuklari"][0]["dogal_bekleyis"][
        "isinma_tamamlanma_gunu"
    ] = "2025-12-31"
    yol = tmp_path / "yanlis-egitim.jsonl"
    yol.write_bytes(
        b"".join(deneme_.kanonik(o) + b"\n" for o in on)
        + deneme_.kanonik(yanlis)
        + b"\n"
    )
    with pytest.raises(deneme_.PilotHatasi, match="Bozuk tam satır"):
        deneme_.PilotKayit(yol).oku()
    yol.write_bytes(b"".join(deneme_.kanonik(o) + b"\n" for o in on))
    with pytest.raises(deneme_.PilotHatasi, match="doğal ısınma"):
        deneme_.PilotKayit(yol)._ekle(yanlis)


@pytest.mark.parametrize(
    "boz", ["kaynak_yok", "yontem_yok", "surum", "ozet", "bag", "null"]
)
def test_dogal_isinma_kayitli_secim_hesap_ve_onbellekten_once_reddedilir(
    tmp_path, monkeypatch, boz
):
    from copy import deepcopy
    from tansu import deneme

    depo, m, _ = s10_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(m.deneme_id)
    # Yayımlanmış seçimin şeması; gerçek veri bağıyla uyuşmadığı da denetlenir.
    secim = dict(
        surum="ilk_islem_v1",
        tablo_ozeti=veri._YAYIMLANMIS_KAYNAK_OZETLERI["ilk_islem_v1"],
        kaynak="is_yatirim",
        goruntu_id="s10",
        manifest_ozeti=d["veri_ayarlari"]["manifest_ozeti"],
    )
    v = deepcopy(d["veri_ayarlari"]) | dict(ilk_islem=secim)
    y = d["yontem_ayarlari"] | dict(isinma_politikasi="kaynakli_isinma_v1")
    if boz == "kaynak_yok":
        del v["ilk_islem"]
    elif boz == "yontem_yok":
        del y["isinma_politikasi"]
    elif boz == "surum":
        secim["surum"] = "bilinmeyen"
    elif boz == "ozet":
        secim["tablo_ozeti"] = "0" * 64
    elif boz == "bag":
        secim["kaynak"] = "baska"
    else:
        v["ilk_islem"] = None
    once = depo.yol.read_bytes()
    with pytest.raises(deneme.PilotHatasi, match="ilk işlem|İlk işlem"):
        s10_revizyon(depo, m, veri_ayarlari=v, yontem_ayarlari=y)
    assert depo.yol.read_bytes() == once
    assert not any(o["kayit_turu"] == "baslangic" for o in depo.oku())


def test_s11_dogal_bekleyis_ozeti_gercek_cocukla_baglidir(tmp_path, monkeypatch):
    from copy import deepcopy
    from tansu import deneme

    depo, eski, _ = dogal_isinma_kayitli(tmp_path, monkeypatch)
    hucre = depo.deneme_oku(eski.deneme_id)["yontem_ayarlari"]
    m = s10_revizyon(
        depo,
        eski,
        yontem_ayarlari=dict(
            yontem="kayitli_izgara_v1",
            tekrar=0,
            secim_politikasi="genis_bolge_net_r_v1",
            olcu_politikasi="bagimsiz_olcu_v1",
            eksenler=[dict(ad="min_gun", birim="gun", degerler=[3])],
            hucre_yontemi=hucre,
        ),
    )
    s = s11_calistir(depo, m, tmp_path)
    assert s["durum"] == "tamamlandi", s
    hedef = next(o for o in depo.oku() if o.get("sonuc_turu") == "arama_v1")
    dogal = next(
        x
        for x in hedef["hucreler"][0]["donemler"][2]["semboller"]
        if x["sembol"] == "ASTOR"
    )
    assert dogal["dogal_bekleyis"]["neden"] == "dogal_isinma"
    assert dogal["dogal_bekleyis"]["isinma_tamamlanma_gunu"] is None
    olaylar = depo.oku()
    prefix = b"".join(
        deneme.kanonik(o) + b"\n" for o in olaylar[: olaylar.index(hedef)]
    )
    yanlis = deepcopy(hedef)
    sembol = next(
        x
        for x in yanlis["hucreler"][0]["donemler"][2]["semboller"]
        if x["sembol"] == "ASTOR"
    )
    del sembol["dogal_bekleyis"]
    yol = tmp_path / "yanlis-arama.jsonl"
    yol.write_bytes(prefix + deneme.kanonik(yanlis) + b"\n")
    with pytest.raises(deneme.PilotHatasi, match="Bozuk tam satır"):
        deneme.PilotKayit(yol).oku()
    yol.write_bytes(prefix)
    with pytest.raises(deneme.PilotHatasi, match="doğal ısınma"):
        deneme.PilotKayit(yol)._ekle(yanlis)


@pytest.mark.parametrize("yuz", ["varyant", "arama"])
@pytest.mark.parametrize("asama", ["hazirlik", "ilerleme"])
def test_kayitli_koordinator_hatasinda_dogrulanmis_bitis_raporda_kalir(
    tmp_path, monkeypatch, yuz, asama
):
    from concurrent.futures import ThreadPoolExecutor
    from tansu import deneme

    if yuz == "varyant":
        depo, esleme, _ = varyant_kayitlari(tmp_path, monkeypatch)
    else:
        depo, makbuz, _ = s11_kayitli(
            tmp_path,
            monkeypatch,
            eksenler=[dict(ad="min_gun", birim="gun", degerler=[2])],
        )
        monkeypatch.setattr(
            ts.concurrent.futures,
            "ProcessPoolExecutor",
            lambda *, max_workers, mp_context: ThreadPoolExecutor(
                max_workers=max_workers
            ),
        )
    asil_veri = ts._donem_verisi
    hazirlanan = []

    def hazirla(*args, **kwargs):
        if asama == "hazirlik" or hazirlanan:
            raise RuntimeError("Kontrollü koordinatör hatası")
        hazirlanan.append(True)
        return asil_veri(*args, **kwargs)

    def ilerleme(mesaj):
        raise RuntimeError("Kontrollü koordinatör hatası")

    monkeypatch.setattr(ts, "_donem_verisi", hazirla)
    if yuz == "varyant":
        sonuc = ts.varyantlari_calistir(
            depo, esleme, veri_koku=tmp_path, isci=1, ilerleme=ilerleme
        )
        ilk = sonuc["varyantlar"][0]
    else:
        sonuc = ts.kayitli_izgara_calistir(
            depo,
            makbuz.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            isci=1,
            ilerleme=ilerleme,
        )
        ilk = sonuc["hucreler"][0]
    olaylar = deneme.PilotKayit(depo.yol).oku()
    bitisler = [
        o
        for o in olaylar
        if o["kayit_turu"] == "bitis" and o["kosu_id"] == ilk["kosu_id"]
    ]
    assert len(bitisler) == 1
    bitis = bitisler[0]
    assert bitis["durum"] == "hata"
    assert ilk["durum"] == "hesap_hatasi" and sonuc["durum"] != "tamamlandi"
    assert ilk["neden"] == "Kontrollü koordinatör hatası"
    assert ilk["bitis_makbuzu"] is not None, "Gerçek hata bitişi rapordan düşemez"
    assert ilk["bitis_makbuzu"]["olay_id"] == bitis["kayit_id"]
    refs = [d["sonuc_ref"] for d in ilk["donemler"] if d["sonuc_ref"] is not None]
    assert refs == bitis["cikti_referanslari"]
    assert len(refs) == (0 if asama == "hazirlik" else 1)
    assert all(any(o["kayit_id"] == ref for o in olaylar) for ref in refs)


def test_varyant_dogal_isinma_ozeti_s10_ilk_durumunu_korur(tmp_path, monkeypatch):
    from tansu import deneme

    depo, m, _ = dogal_isinma_kayitli(tmp_path, monkeypatch)
    sonuc = s10_calistir(depo, m, tmp_path)
    assert sonuc["durum"] == "tamamlandi"
    d = depo.deneme_oku(m.deneme_id)
    rapor = dict(donemler=ts._bos_hucre_donemleri(d, "Başlamadı."))
    ts._varyant_donemlerini_aktar(rapor, sonuc["donemler"])
    genc = next(s for s in rapor["donemler"][0]["semboller"] if s["sembol"] == "DSTKF")
    assert genc.get("isinma") == dict(gozlem=2, gerekli=500, tamam=False), (
        "Varyant raporu gerçek S10 ilk gün sayımını taşımalı"
    )
    assert (
        genc["dogal_bekleyis"]
        == sonuc["donemler"][0]["isinma"]["DSTKF"]["dogal_bekleyis"]
    )
    assert genc["dogal_bekleyis"]["isinma_tamamlanma_gunu"] is None
    astor = next(s for s in rapor["donemler"][1]["semboller"] if s["sembol"] == "ASTOR")
    assert astor["isinma"] == dict(gozlem=249, gerekli=500, tamam=False)
    assert astor["dogal_bekleyis"]["isinma_tamamlanma_gunu"] == "2024-12-17"
    assert not any(
        "isinma" in s
        for r in rapor["donemler"]
        for s in r["semboller"]
        if "dogal_bekleyis" not in s
    )
    assert all(r["durum"] == "tamamlandi" for r in sonuc["donemler"])
    once = depo.yol.read_bytes()
    olaylar = deneme.PilotKayit(depo.yol).oku()
    assert depo.yol.read_bytes() == once
    bas = next(o for o in olaylar if o["kayit_turu"] == "baslangic")
    bitis = next(o for o in olaylar if o["kayit_turu"] == "bitis")
    assert bas["uyelik_kaniti"]["surum"] == "uyelik_kaniti_v2"
    assert bas["ayar_parmak_izi"] == bitis["ayar_parmak_izi"] == m.ayar_ozeti
    assert d["yontem_ayarlari"]["kilit_politikasi"] == "ham_aralik_v1"
    assert d["yontem_ayarlari"]["isinma_politikasi"] == "kaynakli_isinma_v1"
    assert bitis["cikti_referanslari"] == [
        r["makbuz"].olay_id for r in sonuc["donemler"]
    ]


def test_s13_izinli_hedef_yoklugu_ortak_stres_ve_native_kayit(tmp_path, monkeypatch):
    from copy import deepcopy
    from tansu import deneme, istatistik, motor

    depo, m, _, kaynak = s13_kayitli(
        tmp_path, monkeypatch, hedef_yoklugu=True, ayni_gun=True
    )
    wf_sinyaller = [
        o
        for o in depo.oku()
        if o["kayit_turu"] == "ileri_sinyal" and o["tarih"] == "2022-01-05"
    ]
    assert len(wf_sinyaller) == 1
    assert wf_sinyaller[0]["sinyal"]["kaynak_sinyal"]["hedef"]["deger"] is None
    ctx, d, g = s13_kosu(depo, m, kaynak)
    with ctx as kosu:
        is_, [(plan, pm)] = s13_plan(depo, kosu, d, g)
        tekrar, refler = ts._mc_ayar_yeniden_sina(
            depo, d, kosu, kaynak, plan, pm.olay_id, tmp_path
        )
        mc_sinyaller = [
            o
            for o in depo.oku()
            if o["kayit_turu"] == "mc_sinyal" and o["kayit"]["tarih"] == "2022-01-05"
        ]
        assert len(mc_sinyaller) == 1
        assert (
            mc_sinyaller[0]["kayit"]["sinyal"]["kaynak_sinyal"]["kayit_id"].split(":")[
                2
            ]
            == wf_sinyaller[0]["sinyal"]["kaynak_sinyal"]["kayit_id"].split(":")[2]
        )
        assert (
            mc_sinyaller[0]["kayit"]["sinyal"]["kaynak_sinyal"]["hedef"]["deger"]
            is None
        )
        pozisyonlar = [
            i["pozisyon"] for s in tekrar["durumlar"].values() for i in s["islemler"]
        ]
        pozisyonlar += [
            s["pozisyon"] for s in tekrar["durumlar"].values() if s["pozisyon"]
        ]
        assert any("hedef_yok_kaniti" in p["risk_girdisi"] for p in pozisyonlar)
        olcu = istatistik.mc_senaryo_olculeri(
            g, is_, plan["cekilis"], durumlar=tekrar["durumlar"]
        )
        kayit = dict(
            plan_ref=pm.olay_id,
            durum="tamamlandi",
            **olcu,
            yeniden_sinama=tekrar,
            sonuc_referanslari=refler,
            asama=None,
            neden=None,
        )
        yanlis = deepcopy(kayit)
        for s in yanlis["yeniden_sinama"]["durumlar"].values():
            pp = [s["pozisyon"], *(i["pozisyon"] for i in s["islemler"])]
            for p in pp:
                if p and "hedef_yok_kaniti" in p["risk_girdisi"]:
                    p["risk_girdisi"]["hedef_yok_kaniti"]["kaynak_sinyal_id"] = (
                        "baska-kaynak"
                    )
            s["butunluk"] = motor._iz_kodu(
                {a: v for a, v in s.items() if a != "butunluk"}
            )
        once = depo.yol.read_bytes()
        with pytest.raises((ValueError, deneme.PilotHatasi)):
            kosu.mc_senaryo_sonucu_kaydet(kayit=yanlis)
        assert depo.yol.read_bytes() == once
        makbuz = kosu.mc_senaryo_sonucu_kaydet(kayit=kayit)
        assert depo.izle(makbuz.olay_id)["sonuc"]["kayit_id"] == makbuz.olay_id


@pytest.mark.parametrize("ilk_kutu", [26.15166, None])
def test_s10_ayni_gun_ozgun_ilk_tam_satir_ve_kimlik_korunur(
    tmp_path, monkeypatch, ilk_kutu
):
    from concurrent.futures import ThreadPoolExecutor

    monkeypatch.setattr(
        ts.concurrent.futures,
        "ProcessPoolExecutor",
        lambda *, max_workers, mp_context: ThreadPoolExecutor(max_workers=max_workers),
    )
    depo, m, _ = s10_kayitli(tmp_path, monkeypatch, varyant="ema_5_8_13")
    kaynaklar = []

    def kurulum(f, p):
        t = pd.Timestamp("2021-12-30")
        gunler = list(f.index[:9])
        if t in f.index:
            gunler += [t, t]
        k = pd.DataFrame(
            dict(kutu_alt=ilk_kutu, kutu_ust=31.23383, hedef=float("nan")), index=gunler
        )
        if t in f.index:
            k.iloc[-1] = [28.0, 32.0, 150.0]
        kaynaklar.append((k, k.copy(deep=True)))
        return k

    monkeypatch.setattr(aileler, "kurulum", kurulum)
    sonuc = s10_calistir(depo, m, tmp_path)
    yil = sonuc["donemler"][4]
    assert len(yil["adaylar"]) == 2
    assert [a["kayit_id"].split(":")[2] for a in yil["adaylar"]] == ["9", "10"]
    assert yil["adaylar"][0]["hedef"]["deger"] is None
    assert yil["adaylar"][1]["hedef"]["deger"] == 150.0
    if ilk_kutu is None:
        assert yil["durum"] == "hata"
        assert yil["islem_referanslari"] == []
        assert "TEST" not in yil["durumlar"]
        assert (
            "kutu" in yil["hatalar"][0]["neden"]
            or "kurulum" in yil["hatalar"][0]["neden"]
        )
        return
    assert yil["durum"] == "tamamlandi", yil["hatalar"]
    pozisyon = yil["durumlar"]["TEST"]["pozisyon"]
    assert pozisyon["risk_girdisi"]["sinyal_id"] == yil["adaylar"][0]["kayit_id"]
    assert pozisyon["kutu_alt"] == 26.15166
    assert pozisyon["hedef"] is None
    assert {d["sinyal_id"] for d in yil["durumlar"]["TEST"]["dolumlar"]} == {
        yil["adaylar"][0]["kayit_id"]
    }
    for k, once in kaynaklar:
        pd.testing.assert_frame_equal(k, once)


@pytest.mark.parametrize(
    "tarih,satirlar",
    [
        (
            "2023-12-19",
            [(6, 10.469618, 11.663944, None), (7, 10.903044, 11.712103, None)],
        ),
        (
            "2024-02-01",
            [(8, 11.769892, 13.08943, None), (9, 12.578952, 13.291695, None)],
        ),
    ],
)
def test_s10_ozgun_aefes_uyelik_reddi_iki_adayi_korur_sifir_kurulum_kabul_eder(
    monkeypatch, tarih, satirlar
):
    from copy import deepcopy
    import datetime as dt
    from tansu import saglamlik
    from tests.test_motor import s09_mumlar

    # V2 kaynak çıkarımı, source line 75: kimlik, tarih ve fiyatlar özgündür.
    parmak_izi = "fe2f19eb798851af4a928b054d15ecfa4db70af40e5bf8b73cb5c237a2d49f20"
    adaylar = [
        dict(
            kayit_id=f"AEFES:{tarih}:{sira}:{parmak_izi}",
            semboller=["AEFES"],
            tarih=tarih,
            baglar=dict(ayar_parmak_izi=parmak_izi),
            **{
                ad: dict(
                    deger=deger,
                    birim="TL/adet",
                    bos_nedeni="hedef_bulunamadi" if ad == "hedef" else None,
                )
                for ad, deger in zip(
                    ("kutu_alt", "kutu_ust", "hedef"), (alt, ust, hedef), strict=True
                )
            },
            yurutme_nedeni="sinyal_gunu_uye_degil",
        )
        for sira, alt, ust, hedef in satirlar
    ]
    once = deepcopy(adaylar)
    ertesi = (dt.date.fromisoformat(tarih) + dt.timedelta(days=1)).isoformat()
    m = s09_mumlar().iloc[:2].copy()
    m.index = pd.DatetimeIndex([tarih, ertesi])
    k = pd.DataFrame(
        [
            {ad: a[ad]["deger"] for ad in ("kutu_alt", "kutu_ust", "hedef")}
            for a in adaylar
        ],
        index=[pd.Timestamp(tarih)] * 2,
    )
    once_k = k.copy(deep=True)
    hesap = dict(mumlar=m, kurulum=k, sinyaller=adaylar)
    d = dict(
        deneme_id="ornek-deneme",
        ayar_parmak_izi="ornek-ayar",
        risk_ayarlari=dict(nominal_tutar=100000, risk_surumu="bagimsiz_risk_v1"),
        masraf_ayarlari=dict(masraf_surumu="komisyon_bsmv_v1"),
        yontem_ayarlari=dict(fiyat_politikasi="aof_v1"),
    )
    sonuc = dict(
        donem=dict(
            baslangic=dt.date.fromisoformat(tarih), bitis=dt.date.fromisoformat(ertesi)
        ),
        uyelik=dict(
            gunler={tarih: dict(semboller=[]), ertesi: dict(semboller=["AEFES"])}
        ),
        adaylar=[],
        durumlar={},
        kosu_id="ornek-kosu",
    )
    paket = dict(
        gunler=[tarih, ertesi],
        piyasa=[
            dict(sembol="AEFES", tarih=t, kalite_bayraklari=[]) for t in (tarih, ertesi)
        ],
        referans=dict(kayit_id="veri-1"),
    )
    strateji = aileler.legacy_coz("ema_5_8_13")
    monkeypatch.setattr(ts, "_isinma_kaydet", lambda *a: None)
    monkeypatch.setattr(ts, "_s10_mumlar", lambda *a, **kw: m)
    asil = saglamlik.ema_hucre_calistir
    girisler = []

    def izle(m, p, **kw):
        girisler.append((kw["sinyal_konumlari"], kw["kurulum"].copy()))
        return asil(m, p, **kw)

    monkeypatch.setattr(saglamlik, "ema_hucre_calistir", izle)
    ts._donem_sembolu(
        d,
        sonuc,
        paket,
        "AEFES",
        hesap,
        strateji,
        aileler.Parametre(**{a.ad: a.deger for a in strateji.parametreler}),
    )
    assert len(sonuc["adaylar"]) == 2
    assert [a["yurutme_nedeni"] for a in sonuc["adaylar"]] == [
        "sinyal_gunu_uye_degil"
    ] * 2
    assert [a["kayit_id"] for a in sonuc["adaylar"]] == [a["kayit_id"] for a in adaylar]
    assert girisler[0][0] == {} and girisler[0][1].empty
    assert sonuc["durumlar"]["AEFES"]["pozisyon"] is None
    assert sonuc["durumlar"]["AEFES"]["dolumlar"] == []
    assert adaylar == once
    pd.testing.assert_frame_equal(hesap["kurulum"], once_k)
