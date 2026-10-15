"""İstatistik yüzü: Holm, p tabanı, blok bootstrap, saptanabilir en küçük etki (TASARIM 5.7, 5.9, 5.11)."""

import numpy as np
import pytest

from tansu import istatistik, simulator


def test_holm_elle_ornek():
    # sıralı p: 0,005 (×4) 0,01 (×3) 0,03 (×2) 0,04 (×1) → 0,02; 0,03; 0,06; 0,04→ en büyüğe çekilir 0,06
    assert istatistik.holm([0.01, 0.04, 0.03, 0.005]) == pytest.approx(
        [0.03, 0.06, 0.06, 0.02]
    )


def test_p_degeri_gercek_kadar_iyi_rastgele_sayilir():
    # k = 0,3'e eşit ya da üstü: 0,5 ve 0,3 → k=2; B=4 → 3/5
    assert istatistik.p_deger(0.3, [0.1, 0.5, 0.3, 0.0]) == pytest.approx(0.6)


def test_p_tabani_bir_bolu_bir_arti_b():
    assert istatistik.p_deger(9.0, [0.0] * 199) == pytest.approx(1 / 200)


def test_gercek_istatistik_yoksa_p_bir():
    assert istatistik.p_deger(float("nan"), [0.0] * 9) == 1.0


def test_saptanabilir_en_kucuk_etki_elle():
    # g = ±0,01 dört gün: sd(ddof=1) = 0,0115470; (1,645+0,842)·sd/√4·252 = 3,6184
    assert istatistik.saptanabilir_etki(
        np.array([0.01, -0.01, 0.01, -0.01])
    ) == pytest.approx(3.6184, rel=1e-3)


def test_blok_bootstrap_sabit_seride_dar_aralik_ve_ayni_tohum_ayni_sonuc():
    g = np.full(100, 0.001)
    assert istatistik.blok_aralik(g, 20) == pytest.approx((0.252, 0.252))
    g = np.sin(np.arange(200)) * 0.01
    assert istatistik.blok_aralik(g, 20, tohum=3) == istatistik.blok_aralik(
        g, 20, tohum=3
    )
    alt, ust = istatistik.blok_aralik(g, 20)
    assert alt < g.mean() * 252 < ust


def test_blok_uzunlugu_en_az_yirmi():
    assert istatistik.blok_uzunlugu(5.0) == 20
    assert istatistik.blok_uzunlugu(37.4) == 38


def test_ek_kol_ailenin_p_degerine_girmez(tmp_path):
    # TASARIM 5.7: ek kol yalnız rapordur; aile p'si yalnız a ve b'den gelir.
    from tests.test_k1 import anlik_hazirla, trend
    from tests.test_simulator import ATR_N, BAS, P, duz, mum, sinyalli

    aday = sinyalli()
    aday[4].update(yuksek=105.0, ham_yuksek=105.0)  # Ön şart var, kırılım sinyali yok.
    aday[6:] = [
        mum("2026-02-03", 100.0, 100.5, 99.5),
        mum("2026-02-04", 100.0, 100.5, 99.5),
    ]
    a = anlik_hazirla(
        tmp_path,
        {
            "S1": sinyalli(),
            "S2": sinyalli(),
            "S3": aday,
            "T1": trend(),
            "T2": trend(),
            "D1": duz(1e3),
        },
    )
    ilk = simulator.ilk_gun(a, BAS)
    evr = simulator.evrenler(a, ilk, a.gunler[-1])
    b = simulator.k1_baglam(a, evr, BAS)
    k = istatistik.ema_k1(
        a, b, P, ATR_N, simulator.uyeler(a, evr, ilk), tekrar=20, tohum=7, kirilim=3
    )
    # (b) her seferinde son gün alıp aynı gün çıkar: gerçeğin altında, k=0 -> 1/21.
    # Ek kol T1/T2'nin +3 trendidir: her tekrar gerçeğin üstünde, k=20 -> 1.
    assert k["p_b"] == pytest.approx(0.047619047619047616)
    assert k["p_ek"] == 1.0
    assert k["p_b"] <= k["p_a"] < 1.0
    assert k["p"] == k["p_a"]


def _ema_k1_tek_hisse(tmp_path, gunler):
    import pandas as pd

    from tests.test_k1 import anlik_hazirla
    from tests.test_simulator import ATR_N, P, sinyalli

    a = anlik_hazirla(tmp_path, {"A": sinyalli()})
    uye = pd.DataFrame({"sembol": "A", "tarih": pd.to_datetime(gunler)})
    return istatistik.EmaK1(a, P, ATR_N, uye, kirilim=3)


def test_ema_k1_iki_gunluk_uyelik_sinyal_gunu_gercege_girer(tmp_path):
    # Bilet 07b: A yalnız 02.02 ve 03.02 üye; tek sinyal 02.02: gerçek sinyal kümesi yalnız A'da ve tek gün.
    k = _ema_k1_tek_hisse(tmp_path, ["2026-02-02", "2026-02-03"])
    assert list(k.gercek) == ["A"] and len(k.gercek["A"]) == 1


def test_ema_k1_tek_gunluk_uyelik_typeerror_degil_k1_hatasi_verir(tmp_path):
    # Bilet 07b: tek üyelik günü olan sembolde `agg(DatetimeIndex)` Timestamp döndürüp `isin`i TypeError ile kırıyordu.
    # Tek gün: tür (b) için ±20 günde başka uygun gün yok; tasarlanmış hata K1Hatasi (TASARIM 5.7, sessizce kırpılmaz).
    with pytest.raises(istatistik.K1Hatasi, match=r"tür \(b\)"):
        _ema_k1_tek_hisse(tmp_path, ["2026-02-02"])
