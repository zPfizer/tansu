"""Tansu sınaması yüzü (TASARIM 5.14): işlem getirisi, Tansu ölçüleri, sağlam bölge, ileri yürüme, işçi sayısı, koşu.

Masraf m = 0,001 (her yönde %0,10). Beklenen değerler elle hesaplanmıştır (her testin yorumunda).

EMA verisi: tests/test_saglamlik.py'deki seri (26.01.2026'dan 8 gün; son kapanış 110). Sinyal gün 5 (02.02, kapanış 103),
giriş 03.02 AOF 104, çıkış 04.02 son kapanış 110 (veri sonu). Dönem 02.02-04.02 (3 gün).
Çift verisi: A, B, C 270 işlem günü (2025-01-01'den). B ve C 100'de sabit; A 255-261. günler 95, sonra 100.
"""

import json
import re

import numpy as np
import pandas as pd
import pytest

from tansu import __main__ as komut
from tansu import kayit
from tansu import tansusinama as ts
from tests.test_k1 import anlik_hazirla
from tests.test_simulator import BAS, KAP, P, YUK, duz, mum

KAP_A = KAP[:7] + [110.0]
YUK_A = YUK[:7] + [110.5]
EMA_IZGARA = {"esik": [0.005], "min_gun": [3], "pencere": [3]}
CIFT_IZGARA = {"z_pencere": [5], "z_esik": [1.0, 1.5]}
IZGARA = {"ema_sikismasi": EMA_IZGARA, "cift_rotasyonu": CIFT_IZGARA}
GUNLER = pd.bdate_range("2025-01-01", periods=270)


def seri_a():
    return [
        mum(g, k, y, k - 0.5, 1e9)
        for g, k, y in zip(pd.bdate_range("2026-01-26", periods=8), KAP_A, YUK_A)
    ]


def ema_anlik(tmp_path):
    return anlik_hazirla(tmp_path, {"A": seri_a(), "B": duz(1e9)})


def cift_anlik(tmp_path):
    a = [95.0 if 255 <= i < 262 else 100.0 for i in range(270)]
    sabit = [mum(g, 100.0) for g in GUNLER]
    seriler = {"A": [mum(g, k) for g, k in zip(GUNLER, a)], "B": sabit, "C": sabit}
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
        (f"{y}-03-02", f"{y}-03-10", r) for y, r in zip(range(2016, 2022), getiriler)
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
    # günü 02.02) − 1 = 104/103 − 1 = 0,0097087; 3 ve 5 gün: satır yok. (Önceki spec bir önceki kapanışa bölüyordu: 104/100 − 1.)
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
    assert f["eksenler"] == EMA_IZGARA
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
    assert b["etiket"] == "Para çıkmaz: en iyi ayar bile zararda."
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
    assert f["eksenler"] == CIFT_IZGARA
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
    assert h["etiket"] == "Sağlam bölge yok: kârlı ayarın yanı zararda (tuzak)."
    assert h["al_tut"] == pytest.approx(-0.001998, abs=1e-6)
    assert h["altut_gecti"] is True
    assert h["ileri"] == {"net": 0.0, "islem": 0, "yillar": []}
    o = h["olcu"]
    assert o["hucre"] == {"z_pencere": 5, "z_esik": 1.0} and o["secildi"] is False
    assert (o["islem"], o["kazanan"], o["kaybeden"], o["kazanma"]) == (2, 1, 1, 0.5)
    assert o["net"] == pytest.approx(0.0484295, abs=1e-7)
    assert o["kar_carpani"] == pytest.approx(25.2895, abs=1e-3)
    assert o["ort_tutma"] == pytest.approx(6.0)
    assert o["maruziyet"] == pytest.approx(12 / 19)
    assert o["max_dd"] == pytest.approx(-0.002996, abs=1e-6)
    assert o["bayraklar"] == ["az işlem"]


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
