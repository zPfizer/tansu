"""K1 yüzü (TASARIM 5.7 "K1 uygulama kuralları"): sepete göre fazla getiri, EMA ve çift rastgele kolları.

Veri: tests/test_simulator.py'deki temel seri (26.01.2026'dan 8 gün; sinyal gün 5 = 02.02, giriş 03.02 AOF 104,
çıkış 04.02 kapanış 105 veri sonu) ve `kos` ile aynı sentetik anlık görüntü.
"""

import datetime as dt

import numpy as np
import pandas as pd
import pytest

from tansu import cift, ciftbolme, istatistik, motor, simulator, veri
from tests.test_ciftbolme import SektorBorsapy, dummy, kur_yil_gecisi, seri
from tests.test_simulator import ATR_N, BAS, P, duz, mum, sinyalli
from tests.test_veri import SahteBorsapy, SahteKaynak

M3 = 0.003


def anlik_hazirla(tmp_path, seriler, faiz=0.0):
    k = SahteKaynak(seriler, {s: [] for s in seriler})
    b = SahteBorsapy([("2025-01-01", faiz)], {s: "X" for s in seriler})
    kimlik = veri.indir(list(seriler), tmp_path, k, simdi=dt.datetime(2026, 10, 5, 19, 30), borsapy=b)
    return veri.oku(kimlik, tmp_path)


def trend():
    """Her gün +3 kapanış (100, 103, ... 121), yüksek = kapanış + 0,5: sıkışma dönemi yok; gün i >= 3 önceki 3 günün
    yükseğini aşar (sıkışmasız kırılım, L=3)."""
    return [mum(g, 100.0 + 3 * i, 100.5 + 3 * i, 99.5 + 3 * i, 1e9)
            for i, g in enumerate(pd.bdate_range("2026-01-26", periods=8))]


def ema_kur(tmp_path, p=P):
    """İki sinyalli (S1, S2: sinyal gün 5, pencere gün 5-7), iki trend (T1, T2) ve bir düşük hacimli hisse (D1, evrenden elenir)."""
    seriler = {"S1": sinyalli(), "S2": sinyalli(), "T1": trend(), "T2": trend(), "D1": duz(1e3)}
    anlik = anlik_hazirla(tmp_path, seriler)
    ilk = simulator.ilk_gun(anlik, BAS)
    evr = simulator.evrenler(anlik, ilk, anlik.gunler[-1])
    return anlik, evr, istatistik.EmaK1(anlik, p, ATR_N, simulator.uyeler(anlik, evr, ilk), kirilim=3)


def test_ema_k1_gercek_sinyaller_motorla_ayni_tabloyu_verir(tmp_path):
    anlik, evr, k = ema_kur(tmp_path)
    ilk = simulator.ilk_gun(anlik, BAS)
    beklenen, _ = motor.sinama(anlik, P, ATR_N, simulator.uyeler(anlik, evr, ilk))
    tablo, _ = k.tablo(k.gercek)
    pd.testing.assert_frame_equal(tablo.reset_index(drop=True), beklenen.sort_values("sembol").reset_index(drop=True),
                                  check_dtype=False)
    assert k.gercek == {"S1": [5], "S2": [5]}


def test_ema_k1_a_ayni_gun_ayni_sayida_hisse_gunun_havuzundan(tmp_path):
    # Gün 5'te iki gerçek sinyal; o günün ön şartlı havuzu (pencere gün 5-7, evren üyesi) yalnız S1 ve S2 -> ikisi de çekilir.
    _, _, k = ema_kur(tmp_path)
    assert k.cek("a", np.random.default_rng(0)) == {"S1": [5], "S2": [5]}


def test_ema_k1_b_ayni_hisse_pencere_icinde_baska_gun(tmp_path):
    # Piyasa durumu bilinmiyor (XU100 SMA50 yok) her gün aynı. Her hissede gün 5 dışında ön şartlı gün: 6 ve 7.
    _, _, k = ema_kur(tmp_path)
    secim = k.cek("b", np.random.default_rng(0))
    assert sorted(secim) == ["S1", "S2"] and all(len(v) == 1 and v[0] in (6, 7) for v in secim.values())


def test_ema_k1_ek_kol_sikismasiz_kirilim_havuzu(tmp_path):
    # T1 ve T2 her gün (i >= 3) önceki 3 günün yükseğini aşar ve pencere dışıdır; gün 5'te iki sinyal -> ikisi de çekilir.
    _, _, k = ema_kur(tmp_path)
    assert k.cek("ek", np.random.default_rng(0)) == {"T1": [5], "T2": [5]}


def test_ema_k1_ek_kol_havuzu_yetmezse_havuz_kadar_ceker_ve_eksigi_sayar(tmp_path):
    # Gün 5'te iki gerçek sinyal (S1, S2); sıkışmasız kırılım havuzu yalnız T1 (D2 düz, kırılım yok; D1 likidite eleğinde).
    # Ek kol raporluk: koşu durmaz, T1 çekilir, 2 − 1 = 1 eksik sinyal sayılır. (a) havuzu gerçek hisseler: eksik yok.
    seriler = {"S1": sinyalli(), "S2": sinyalli(), "T1": trend(), "D1": duz(1e3), "D2": duz(1e9)}
    anlik = anlik_hazirla(tmp_path, seriler)
    ilk = simulator.ilk_gun(anlik, BAS)
    evr = simulator.evrenler(anlik, ilk, anlik.gunler[-1])
    uye = simulator.uyeler(anlik, evr, ilk)
    k = istatistik.EmaK1(anlik, P, ATR_N, uye, kirilim=3)
    assert k.cek("ek", np.random.default_rng(0)) == {"T1": [5]}
    assert k.ek_eksik == 1
    b = simulator.k1_baglam(anlik, evr, BAS)
    assert istatistik.ema_k1(anlik, b, P, ATR_N, uye, tekrar=3, kirilim=3)["ek_eksik"] == 1


def test_ema_k1_p_alt_siniri_ayni_tohum_ayni_sonuc_ve_a_turu_birdir(tmp_path):
    anlik, evr, _ = ema_kur(tmp_path)
    b = simulator.k1_baglam(anlik, evr, BAS)
    ilk = b["ilk"]
    uye = simulator.uyeler(anlik, evr, ilk)
    bir = istatistik.ema_k1(anlik, b, P, ATR_N, uye, tekrar=20, tohum=7, kirilim=3)
    iki = istatistik.ema_k1(anlik, b, P, ATR_N, uye, tekrar=20, tohum=7, kirilim=3)
    assert bir == iki
    assert bir["p_a"] == 1.0  # havuz = gerçek hisseler: her tekrar gerçeğin aynısı, k = B
    assert 1 / 21 <= bir["p_b"] <= 1.0 and bir["p"] == max(bir["p_a"], bir["p_b"])
    assert bir["tekrar"] == 20 and bir["sinyal"] == 2 and bir["komsusuz"] == 0


def test_ema_k1_uygun_gun_yetmezse_hata(tmp_path):
    # Isınma 8: hisse düzeyi uygun gün yalnız gün 7 (i + 1 >= 8); sinyal gün 7'de (pencere 5-7), başka uygun gün yok.
    import dataclasses
    with pytest.raises(istatistik.K1Hatasi, match="başka uygun gün"):
        ema_kur(tmp_path, dataclasses.replace(P, isinma=8))


def cift_kur(tmp_path):
    """Yıl geçişi senaryosu (tests/test_ciftbolme.py): 2016'da A–B ve C–D, 2017'de C–D ve E–F; elle seçilmiş yapı."""
    f, sektor = kur_yil_gecisi()
    f.update(dummy(1))
    seriler = {s: seri(*x) if isinstance(x, tuple) else seri(x) for s, x in f.items()}
    k = SahteKaynak(seriler, {s: [] for s in seriler})
    kimlik = veri.indir(list(seriler), tmp_path, k, simdi=dt.datetime(2026, 10, 5, 19, 30),
                        borsapy=SektorBorsapy([("2014-01-01", 0.0)], sektor))
    anlik = veri.oku(kimlik, tmp_path)
    evr = simulator.evrenler(anlik, simulator.ilk_gun(anlik), anlik.gunler[-1])
    return anlik, simulator.k1_baglam(anlik, evr), ciftbolme.hazirla(anlik, evr)


def test_cift_k1_ayni_cift_ayni_sayida_sinyal_ilk_gun_gercege_esit_z_esigi_ustu_gunler(tmp_path):
    _, b, h = cift_kur(tmp_path)
    k = istatistik.CiftK1(h, b)
    assert len(k.gercek) > 0
    p = h["p"]
    for (y, x), g in k.gercek.groupby(["y", "x"]):
        rastgele = k.cek(np.random.default_rng(1))[(y, x)]
        konum = np.flatnonzero(rastgele)
        ilk = h["gunler"].get_loc(g["giris_tarih"].min()) - 1  # ilk giriş günü gerçeğe eşit: sinyal bir gün önce
        assert len(konum) == len(g) and konum[0] == ilk
        z = cift.z_skor(h["Kc"][y], h["Kc"][x], p.z_pencere).to_numpy()
        assert (np.abs(z[konum]) >= p.z_esik).all()
        yon = 1 if g.sort_values("giris_tarih")["sembol"].iloc[0] == y else -1  # gerçek ilk hedef
        assert list(rastgele[konum]) == [yon * (-1) ** i for i in range(len(konum))]  # sırayla öteki bacak


def test_cift_k1_p_araligi_ve_ayni_tohum_ayni_sonuc(tmp_path):
    _, b, h = cift_kur(tmp_path)
    bir = istatistik.cift_k1(h, b, tekrar=10, tohum=5)
    assert bir == istatistik.cift_k1(h, b, tekrar=10, tohum=5)
    assert 1 / 11 <= bir["p"] <= 1.0 and bir["tekrar"] == 10 and bir["gecis"] > 0


def test_sepete_gore_fazla_getiri_elle_hesap(tmp_path):
    # Tek üye A. İşlem: giriş 03.02 AOF 104, çıkış 04.02 AOF 105 (veri sonu), masraf 0,003:
    # getiri = 105*0,997 / (104*1,003) - 1 = 104,685 / 104,312 - 1 = 0,0035758.
    # Sepet endeksi (başlangıç 02.02 = 0,997; bkz. test_simulator): [0,997; 0,997*104/103; 0,997*105/103].
    # Önceki-kapanış değerleri: giriş 03.02 -> 0,997; çıkış 04.02 -> 0,997*104/103. Sepet getirisi = 104/103 - 1 = 0,0097087.
    # Fazla getiri = 0,0035758 - 0,0097087 = -0,0061329.
    anlik = anlik_hazirla(tmp_path, {"A": sinyalli()})
    evr = simulator.evrenler(anlik, simulator.ilk_gun(anlik, BAS), anlik.gunler[-1])
    b = simulator.k1_baglam(anlik, evr, BAS)
    islemler, _ = motor.sinama(anlik, P, ATR_N, simulator.uyeler(anlik, evr, b["ilk"]))
    t = simulator.k1_islemler(islemler, b, M3)
    assert len(t) == 1
    assert t["getiri"].iloc[0] == pytest.approx(0.0035758, abs=1e-6)
    assert t["fazla"].iloc[0] == pytest.approx(-0.0061329, abs=1e-6)
    assert istatistik.ortalama_fazla(t) == pytest.approx(-0.0061329, abs=1e-6)
    assert np.isnan(istatistik.ortalama_fazla(t.iloc[:0]))
