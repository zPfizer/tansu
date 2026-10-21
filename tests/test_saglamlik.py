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
        for g, k, y in zip(
            pd.bdate_range("2026-01-26", periods=8), KAP_A, YUK_A, strict=True
        )
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


def s11_alan(sekil, degerler=None):
    hucreler = [
        dict(
            indeks=list(i), durum="tamamlandi", kapali_islem_sayisi=1, toplam_net_r=1.0
        )
        for i in np.ndindex(*sekil)
    ]
    for i, deger in (degerler or {}).items():
        hucreler[np.ravel_multi_index(i, sekil)]["toplam_net_r"] = deger
    return dict(
        eksenler=[
            dict(ad=f"eksen{i}", degerler=list(range(n))) for i, n in enumerate(sekil)
        ]
    ), hucreler


def test_s11_caprazlar_tam_cevre_ve_kenar_merkez_yasagi():
    izgara, h = s11_alan((3, 3))
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s.get("secilen") == [1, 1]
    assert len(s["hucreler"][4]["komsular"]) == 8
    assert s["hucreler"][0]["sinir"] is True
    h[0]["toplam_net_r"] = -1.0
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s["secilen"] is None
    assert s["en_iyi"]["secildi"] is False
    assert s["neden"] == "uygun_merkez_yok"


@pytest.mark.parametrize("durum", ["islemsiz", "hesap_hatasi", "eksik"])
def test_s11_eksik_hucre_karli_alandan_silinmez(durum):
    izgara, h = s11_alan((3, 3))
    h[0].update(durum=durum, kapali_islem_sayisi=0, toplam_net_r=None)
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s["secilen"] is None
    assert len(s["hucreler"]) == 9
    assert s["hucreler"][4]["eksik_komsular"] == [[0, 0]]


def test_s11_alan_disi_hucre_indeksleri_sikistirmaz():
    izgara, h = s11_alan((3, 3))
    h[0].update(durum="alan_disi", neden="izin_verilmeyen_bilesim")
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s["secilen"] == [1, 1]
    assert s["hucreler"][4]["alan_disi_komsular"] == [[0, 0]]
    assert len(s["hucreler"][4]["komsular"]) == 7


def test_s11_buyuk_bolge_medyan_mesafe_ve_kanonik_esitlik():
    izgara, h = s11_alan((9,), {(4,): -1.0})
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s["secilen"] == [2]
    assert [b["buyukluk"] for b in s["bolgeler"]] == [4, 4]
    h[6]["toplam_net_r"] = 3.0
    h[7]["toplam_net_r"] = 3.0
    assert saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")["secilen"] == [6]
    izgara, h = s11_alan((7,))
    h[1]["toplam_net_r"] = 1000.0
    assert saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")["secilen"] == [3]


def test_s11_tek_hucre_ve_eski_politikalar_secim_izni_vermez():
    izgara, h = s11_alan((1,))
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s["secilen"] is None
    eski = saglamlik.sec(
        None, [{"fazla": 1.0}, {"fazla": -1.0}], politika="pozitif_fazla_legacy_v1"
    )
    assert eski["politika"] == "pozitif_fazla_legacy_v1"
    assert eski["secilen"] is None and eski["oran"] == 0.5


def test_s11_merkez_mesafesi_alan_disi_bosluktan_gecer_ve_esitligi_cozer():
    izgara, h = s11_alan((7,))
    h[0].update(durum="alan_disi", neden="katalog")
    h[1].update(durum="alan_disi", neden="katalog")
    h[2].update(durum="alan_disi", neden="katalog")
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s["secilen"] == [3]
    assert s["hucreler"][3]["uzaklik"] == 3
    izgara, h = s11_alan((6,), {(2,): 2.0, (3,): 2.0, (4,): 2.0})
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert s["secilen"] == [3]
    assert s["hucreler"][3]["en_kotu_komsu"] == 2.0
    assert s["hucreler"][2]["uzaklik"] == s["hucreler"][3]["uzaklik"] == 2


def test_s11_capraz_karlar_tek_eksen_bolgesi_olusturmaz():
    izgara, h = s11_alan((3, 3))
    for i in (1, 2, 3, 5, 6, 7, 8):
        h[i]["toplam_net_r"] = -1.0
    s = saglamlik.sec(izgara, h, politika="genis_bolge_net_r_v1")
    assert [b["indeksler"] for b in s["bolgeler"]] == [[[0, 0]], [[1, 1]]]
    assert s["secilen"] is None


def test_s11_ortak_eski_hucre_onbellegi_ayar_ve_mum_sinirini_korur(tmp_path):
    anlik, _, _, _ = kur(tmp_path)
    m = motor.mumlar(anlik, "A", P, ATR_N)
    p = dataclasses.replace(P, min_gun=3)
    k = motor.kurulum_bilgisi(m.dropna(subset=["kapanis"]), p)
    konumlar = m.index.get_indexer(aileler_sinyali(m, p))
    zincir = motor.Zincir(m, P)
    beklenen = motor.Zincir(m, p, k).calistir(konumlar)
    sonuc = None
    try:
        sonuc = saglamlik.ema_hucre_calistir(
            m, p, kurulum=k, sinyal_konumlari=konumlar, yurutme=zincir
        )
    except TypeError, ValueError, AttributeError:
        pass
    assert sonuc is not None, "Uyumlu eski hücre mevcut Zincir ile yürümeli"
    pd.testing.assert_frame_equal(sonuc[0], beklenen[0])
    assert sonuc[1] == beklenen[1]
    for mumlar, ayar in ((m.copy(), p), (m, dataclasses.replace(p, stop="atr15"))):
        with pytest.raises(ValueError, match="uyuşmuyor"):
            saglamlik.ema_hucre_calistir(
                mumlar, ayar, kurulum=k, sinyal_konumlari=konumlar, yurutme=zincir
            )


def aileler_sinyali(m, p):
    from tansu import aileler

    return aileler.sinyal(m.dropna(subset=["kapanis"]), p)


@pytest.mark.parametrize(
    "alan,deger",
    [
        ("toplam_net_r", True),
        ("toplam_net_r", "1"),
        ("toplam_net_r", float("inf")),
        ("kapali_islem_sayisi", True),
    ],
)
def test_s11_sayisal_ozette_metin_ve_bayrak_kabul_edilmez(alan, deger):
    izgara, hucreler = s11_alan((3,))
    hucreler[1][alan] = deger
    hata = None
    try:
        saglamlik.sec(izgara, hucreler, politika="genis_bolge_net_r_v1")
    except ValueError as yakalanan:
        hata = yakalanan
    except TypeError:
        pass
    assert hata is not None, "Seçici bozuk sayısal özeti açık alan hatasıyla reddetmeli"


@pytest.mark.parametrize("durum", ["eksik", "hesap_hatasi", "kayit_hatasi"])
def test_s11_bilinmeyen_islem_sayisi_sifira_cevrilmez(durum):
    izgara, hucreler = s11_alan((3, 3))
    if durum == "eksik":
        hucreler.pop(0)
    else:
        hucreler[0].update(durum=durum, kapali_islem_sayisi=None, toplam_net_r=None)
    sonuc = None
    try:
        sonuc = saglamlik.sec(izgara, hucreler, politika="genis_bolge_net_r_v1")
    except ValueError:
        pass
    assert sonuc is not None, "Başarısız veya eksik hücrenin boş sayısı korunmalı"
    assert sonuc["hucreler"][0]["kapali_islem_sayisi"] is None
    assert sonuc["hucreler"][0]["toplam_net_r"] is None
    assert sonuc["secilen"] is None


def test_s11_buyuk_bolge_medyanin_onundedir():
    # Sol bölge beş, sağ bölge üç hücredir; sağın yüksek medyanı büyüklüğü geçemez.
    izgara, hucreler = s11_alan(
        (9,), {(5,): -1.0, (6,): 100.0, (7,): 100.0, (8,): 100.0}
    )
    sonuc = saglamlik.sec(izgara, hucreler, politika="genis_bolge_net_r_v1")
    assert [b["buyukluk"] for b in sonuc["bolgeler"]] == [5, 3]
    assert sonuc["secilen"] == [2]


@pytest.mark.parametrize(
    "durum,sayi,net,merkez,merkez_mesafesi,bes_mesafesi",
    [
        ("eksik", None, None, 5, 5, 5),
        ("hesap_hatasi", None, None, 5, 5, 5),
        ("kayit_hatasi", None, None, 5, 5, 5),
        ("baslamadi", None, None, 5, 5, 5),
        ("islemsiz", 0, None, 5, 5, 5),
        ("tamamlandi", 1, None, 5, 5, 5),
        ("tamamlandi", 1, 0.0, 6, 4, 3),
        ("tamamlandi", 1, -1.0, 6, 4, 3),
    ],
)
def test_s11_mesafe_hedefi_yalniz_olculmus_sifir_ve_kayiptir(
    durum, sayi, net, merkez, merkez_mesafesi, bes_mesafesi
):
    izgara, hucreler = s11_alan((11,))
    hucreler[2].update(durum=durum, kapali_islem_sayisi=sayi, toplam_net_r=net)
    sonuc = saglamlik.sec(izgara, hucreler, politika="genis_bolge_net_r_v1")
    assert sonuc["secilen"] == [merkez]
    assert sonuc["hucreler"][merkez]["uzaklik"] == merkez_mesafesi
    assert sonuc["hucreler"][5]["uzaklik"] == bes_mesafesi
    assert len(sonuc["hucreler"]) == 11
    assert sonuc["hucreler"][2]["durum"] == durum
    assert sonuc["hucreler"][2]["kapali_islem_sayisi"] == sayi
    assert sonuc["hucreler"][2]["toplam_net_r"] == net
    assert sonuc["hucreler"][2]["karli"] is False
    assert sonuc["hucreler"][3]["komsular"] == [[2], [4]]
    assert sonuc["hucreler"][3]["uygun_merkez"] is False
    assert sonuc["hucreler"][4]["uygun_merkez"] is True
