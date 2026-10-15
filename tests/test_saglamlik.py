"""Sağlamlık ızgarası (TASARIM 5.10, KURALLAR §3): hücre başına K1'e göre ortalama fazla getiri, %0,3 masraf, p aranmaz.

Veri: tests/test_simulator.py'deki temel seri, ama son kapanış 110 (veri sonu çıkışı). Hisse A sinyalli, B düz (100).
Elle hesap (giriş 03.02 AOF 104, çıkış 04.02 kapanış 110, masraf 0,003):
- işlem getirisi = 110·0,997 / (104·1,003) − 1 = 109,67 / 104,312 − 1 = 0,0513651
- sepet (A ve B eşit ağırlık, ilk dengeleme 0,003; K2 önceki-kapanış oranı) = ½·(104/103 − 1) = 0,0048544
- fazla getiri = 0,0513651 − 0,0048544 = 0,0465108
"""

import dataclasses

import numpy as np
import pandas as pd
import pytest

from tansu import ciftbolme, denetim, istatistik, motor, saglamlik, simulator
from tests.test_k1 import anlik_hazirla, cift_kur
from tests.test_simulator import ATR_N, BAS, KAP, P, YUK, duz, mum

KAP_A = KAP[:7] + [110.0]
YUK_A = YUK[:7] + [110.5]


def seri_a():
    return [
        mum(g, k, y, k - 0.5, 1e9)
        for g, k, y in zip(pd.bdate_range("2026-01-26", periods=8), KAP_A, YUK_A)
    ]


def kur(tmp_path):
    anlik = anlik_hazirla(tmp_path, {"A": seri_a(), "B": duz(1e9)})
    ilk = simulator.ilk_gun(anlik, BAS)
    evr = simulator.evrenler(anlik, ilk, anlik.gunler[-1])
    return (
        anlik,
        evr,
        simulator.k1_baglam(anlik, evr, BAS),
        simulator.uyeler(anlik, evr, ilk),
    )


def test_ema_izgarasi_hucre_basina_fazla_getiri_pozitiflik_ve_oran(tmp_path):
    # min_gun 3: bir işlem, fazla getiri +0,0465108 → pozitif. min_gun 6: düz dönem 5 gün, dönem yok, işlem yok → NaN,
    # pozitif değil. Oran 1/2.
    anlik, evr, b, uye = kur(tmp_path)
    izgara = {"esik": [0.005], "min_gun": [3, 6], "pencere": [3]}
    h = saglamlik.ema(anlik, b, P, ATR_N, uye, izgara)
    assert [x["hucre"] for x in h] == [
        {"esik": 0.005, "min_gun": 3, "pencere": 3},
        {"esik": 0.005, "min_gun": 6, "pencere": 3},
    ]
    assert (h[0]["islem"], h[0]["pozitif"]) == (1, True)
    assert h[0]["fazla"] == pytest.approx(0.0465108, abs=1e-6)
    assert (h[1]["islem"], h[1]["pozitif"]) == (0, False) and np.isnan(h[1]["fazla"])
    assert saglamlik.oran(h) == 0.5


def test_ema_izgarasi_hucre_tek_basina_kosulan_kuralla_ayni_fazla_getiriyi_verir(
    tmp_path,
):
    # Zincir önbelleği hücreler arası paylaşılır; hücre sonucu `motor.sinama` + `k1_islemler` yolundan farklı olmamalı.
    anlik, evr, b, uye = kur(tmp_path)
    p = dataclasses.replace(P, esik=0.005, min_gun=3, pencere=3)
    islemler, _ = motor.sinama(anlik, p, ATR_N, uye)
    beklenen = simulator.k1_islemler(islemler, b, 0.003)["fazla"].mean()
    h = saglamlik.ema(
        anlik, b, P, ATR_N, uye, {"esik": [0.005], "min_gun": [3], "pencere": [3]}
    )
    assert h[0]["fazla"] == pytest.approx(beklenen)


def test_cift_izgarasi_z_esigi_asilamazsa_islem_yok_pozitif_degil_esik_2_gercek_tabloyla_ayni(
    tmp_path,
):
    # Yıl geçişi senaryosu (tests/test_k1.py): elle seçilmiş çiftler. Z eşiği 100: hiçbir gün |Z| ≥ 100 değil, işlem yok,
    # fazla getiri NaN, pozitif değil. Eşik 2: gerçek koşunun (CiftK1, %0,3) tablosu: aynı işlem sayısı ve ortalama.
    anlik, b, h = cift_kur(tmp_path)
    evr = b["evr"]
    izgara = {"z_pencere": [60], "z_esik": [2.0, 100.0], "p_esik": [0.05]}
    hucreler = saglamlik.cift(
        anlik, evr, b, simulator.BASLANGIC, ciftbolme.Parametre(), izgara
    )
    assert [x["hucre"]["z_esik"] for x in hucreler] == [2.0, 100.0]
    gercek = istatistik.CiftK1(h, b, 0.003).gercek
    assert hucreler[0]["islem"] == len(gercek) > 0
    assert hucreler[0]["fazla"] == pytest.approx(gercek["fazla"].mean())
    assert (hucreler[1]["islem"], hucreler[1]["pozitif"]) == (0, False) and np.isnan(
        hucreler[1]["fazla"]
    )


def test_dar_p_esigi_genis_adaylardan_secince_dogrudan_secimle_ayni(tmp_path):
    # Çift seçimi eşbütünleşme p'si küçükten büyüğe sıralı listenin önekidir: p_esik 0,10 için bir kez hesaplanan adaylardan
    # 0,01 ve 0,05 seçimi, her eşikle ayrı hesaplanan seçimle aynı olmalı (ızgara eşbütünleşmeyi yeniden hesaplamaz).
    a = denetim.dunya(7, hisse=24, gun=700)
    Kc = a.fiyat.pivot(index="tarih", columns="sembol", values="kapanis")
    uye = sorted(a.sektor)
    p = lambda pe: dataclasses.replace(ciftbolme.Parametre(), p_esik=pe)  # noqa: E731
    genis = ciftbolme.adaylar(Kc, uye, a.sektor, 650, p(0.10))
    assert len(ciftbolme.sec(genis, p(0.05))) < len(
        ciftbolme.sec(genis, p(0.10))
    )  # eşikler gerçekten ayırıyor
    for pe in (0.01, 0.05, 0.10):
        pd.testing.assert_frame_equal(
            ciftbolme.sec(genis, p(pe)), ciftbolme.secim(Kc, uye, a.sektor, 650, p(pe))
        )


def test_hazirla_genis_aday_esigi_ana_secimi_ve_sonucu_degistirmez(tmp_path):
    anlik, b, h = cift_kur(tmp_path)
    genis = ciftbolme.hazirla(anlik, b["evr"], simulator.BASLANGIC, aday_esik=0.10)
    pd.testing.assert_frame_equal(genis["secim"], h["secim"])
    bir, iki = (
        ciftbolme.calistir(anlik, b["evr"], h=x)["masraf"][0.003]["islemler"]
        for x in (h, genis)
    )
    pd.testing.assert_frame_equal(bir, iki)


def test_oran_pozitif_hucrelerin_payi_ve_bos_izgara_nan():
    assert saglamlik.oran(
        [{"pozitif": p} for p in (True, False, False, True, True)]
    ) == pytest.approx(0.6)
    assert np.isnan(saglamlik.oran([]))


def test_varsayilan_izgara_kurallar_madde_3_ile_ayni():
    assert saglamlik.IZGARA["ema_sikismasi"] == {
        "esik": [0.010, 0.012, 0.015],
        "min_gun": [2, 3, 5],
        "pencere": [5, 10, 20],
    }
    assert saglamlik.IZGARA["cift_rotasyonu"] == {
        "z_pencere": [60, 120],
        "z_esik": [1.5, 2.0, 2.5],
        "p_esik": [0.01, 0.05, 0.10],
    }


@pytest.mark.parametrize("gunler", [["2026-02-02"], ["2026-02-02", "2026-02-03"]])
def test_ema_izgarasi_tek_gunluk_ve_iki_gunluk_uyelik_sinyal_gunu_alinir(
    tmp_path, gunler
):
    # Bilet 07b: tek üyelik günü olan sembolde `agg(DatetimeIndex)` Timestamp döndürüp `isin`i kırıyordu.
    # A yalnız 02.02 (ya da 02.02 ve 03.02) üye; sinyal 02.02: bir işlem, fazla getiri +0,0465108 (dosya başındaki elle hesap).
    anlik, evr, b, _ = kur(tmp_path)
    uye = pd.DataFrame({"sembol": "A", "tarih": pd.to_datetime(gunler)})
    h = saglamlik.ema(
        anlik, b, P, ATR_N, uye, {"esik": [0.005], "min_gun": [3], "pencere": [3]}
    )
    assert (h[0]["islem"], h[0]["pozitif"]) == (1, True)
    assert h[0]["fazla"] == pytest.approx(0.0465108, abs=1e-6)
