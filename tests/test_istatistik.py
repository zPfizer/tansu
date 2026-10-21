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


def test_blok_bootstrap_yuzde_95_aralik_uclari_elle():
    # TASARIM 5.9: tohum 3, blok 2 başlangıçları (1,0), (0,0), (0,1), (1,1).
    # Üç günlük örnekler: [0,01; 0,03; 0], [0; 0,01; 0],
    # [0; 0,01; 0,01], [0,01; 0,03; 0,01]. Yıllık ortalamalar: 3,36; 0,84; 1,68; 4,20.
    # Sıralı uçlarda %7,5 ara değer: 0,84 + 0,075*0,84 = 0,903;
    # 4,20 - 0,075*0,84 = 4,137. 5/95 yüzdelikleri bu aralığı daraltır.
    assert istatistik.blok_aralik(
        [0.0, 0.01, 0.03], blok=2, tekrar=4, tohum=3
    ) == pytest.approx((0.903, 4.137))


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
    # (b) 15 tekrar son gün alıp aynı gün çıkar: gerçeğin altında. Öteki 5 tekrarda istatistik NaN; eski sayım NaN'ı
    # "kötü" sayıp k=0 (1/21) veriyordu. TASARIM 5.7 (vekil kararı 15.10): NaN tekrar iyi sayılır, k=5 -> 6/21.
    # Ek kol T1/T2'nin +3 trendidir: her tekrar gerçeğin üstünde, k=20 -> 1.
    assert k["p_b"] == pytest.approx(6 / 21)
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


def test_rastgele_tekrarda_nan_gercege_esit_ya_da_iyi_sayilir():
    # TASARIM 5.7: NaN tekrar p'yi düşürmez. Gerçek 0,3; tekrarlar [NaN, 0,5, 0,1]: k = 1 (NaN) + 1 (0,5) = 2; p = (1+2)/(1+3) = 3/4.
    assert istatistik.p_deger(0.3, [float("nan"), 0.5, 0.1]) == pytest.approx(0.75)


def s11_egri(satirlar=None, **degisiklik):
    return (
        dict(
            tur="tani_net_r",
            satirlar=satirlar
            if satirlar is not None
            else [
                {"an": "2025-01-03", "deger": 2.0},
                {"an": "2025-01-05", "deger": 1.0},
                {"an": "2025-01-07", "deger": 3.0},
            ],
            baslangic_degeri=0.0,
            baslangic_ani="2025-01-01",
            baslangic_politikasi="acik",
            tarih_temeli="takvim_gunu",
            normalizasyon="ilk_planlanan_risk",
            birim="R",
            muhasebe_politikasi="tani_net_r_v1",
            referanslar=["elle-egri"],
        )
        | degisiklik
    )


def test_s11_baslangic_dahil_mutlak_r_dususu_ve_takvim_suresi():
    sonuc = istatistik.egri_dususu(s11_egri())
    assert sonuc.get("derinlik") == {"deger": 1.0, "birim": "R", "bos_nedeni": None}
    assert sonuc["sure"] == {"deger": 4, "birim": "takvim_gunu", "bos_nedeni": None}


def test_s11_ilk_kapanis_ve_eklenen_bir_farkli_politikadir():
    import pandas as pd
    from tansu import tansusinama

    kapanis = pd.Series([0.9, 1.0], index=pd.to_datetime(["2025-01-01", "2025-01-02"]))
    assert istatistik.dusus(kapanis) == (0.0, 1)
    assert tansusinama.olculer([], [], kapanis, 0)["max_dd"] == pytest.approx(-0.1)
    sonuc = istatistik.egri_dususu(
        s11_egri(
            [{"an": "2025-01-03", "deger": -2.0}],
        )
    )
    assert sonuc["derinlik"]["deger"] == 2.0
    assert sonuc["sure"]["deger"] == 2


def s11_islem(*, acik=False):
    from tansu import islem_riski

    dolumlar = [
        dict(dolum_id="alis", yon="alis", fiyat=100.0, adet=100),
        dict(dolum_id="yari", yon="satis", fiyat=110.0, adet=50),
    ]
    if not acik:
        dolumlar.append(dict(dolum_id="son", yon="satis", fiyat=90.0, adet=50))
    sonuc = islem_riski.hesapla(
        dict(
            giris_fiyat=100.0,
            ilk_stop=90.0,
            nominal_tutar=100000.0,
            aile="ema_sikismasi",
            risk_surumu="bagimsiz_risk_v1",
            masraf_surumu="komisyon_bsmv_v1",
            dolumlar=dolumlar,
        )
    )
    return dict(islem_id="acik" if acik else "kapali", sonuc=sonuc)


def test_s11_nihai_sonuca_kismi_kar_ikinci_kez_eklenmez():
    sonuc = istatistik.olc(
        [s11_islem(), s11_islem(acik=True)], politika="bagimsiz_olcu_v1"
    )
    assert sonuc.get("olculer", {}).get("net_sonuc") == {
        "deger": pytest.approx(-31.5),
        "birim": "TL",
        "bos_nedeni": None,
    }
    assert sonuc["olculer"]["masraf"]["deger"] == pytest.approx(31.5)
    assert sonuc["olculer"]["islem"]["deger"] == 1
    assert sonuc["acik_kismi"][0]["olculer"]["net_sonuc"]["deger"] == pytest.approx(
        483.4625
    )
    assert sonuc["acik_kismi"][0]["olculer"]["kalan_adet"]["deger"] == 50
    assert sonuc["islemler"][0]["paydalar"]["ilk_risk"] == 1998.0545
    assert sonuc["olculer"]["sharpe"]["deger"] is None
    assert sonuc["olculer"]["sharpe"]["bos_nedeni"]


@pytest.mark.parametrize("ariza", [None, "payda", "kaynak", "tarih", "tek", "sabit"])
def test_s11_sharpe_yalniz_hizali_kaynakli_gunluk_fark(ariza):
    karsilastirma = dict(
        politika="gunluk_fark_252_v1",
        kaynak_ref="tarihli-faiz",
        payda="onceki_gun_ozkaynak",
        referanslar=["gunluk-degerleme"],
        getiriler=[
            {"an": "2025-01-02", "deger": 0.02},
            {"an": "2025-01-03", "deger": 0.04},
        ],
        risksiz=[
            {"an": "2025-01-02", "deger": 0.01},
            {"an": "2025-01-03", "deger": 0.01},
        ],
    )
    if ariza in ("payda", "kaynak"):
        karsilastirma["payda" if ariza == "payda" else "kaynak_ref"] = None
    elif ariza == "tarih":
        karsilastirma["risksiz"][1]["an"] = "2025-01-04"
    elif ariza == "tek":
        karsilastirma["getiriler"] = karsilastirma["getiriler"][:1]
        karsilastirma["risksiz"] = karsilastirma["risksiz"][:1]
    elif ariza == "sabit":
        karsilastirma["getiriler"][1]["deger"] = 0.02
    sonuc = istatistik.olc([], politika="bagimsiz_olcu_v1", karsilastirma=karsilastirma)
    s = sonuc["olculer"]["sharpe"]
    if ariza is None:
        # Farklar 0,01 ve 0,03: ortalama 0,02; örnek varyansı 0,0002.
        assert s == dict(
            deger=pytest.approx(22.44994432064365), birim="oran", bos_nedeni=None
        )
    else:
        assert s["deger"] is None and s["bos_nedeni"]


@pytest.mark.parametrize("deger", [True, "1", float("inf"), None])
def test_s11_gecersiz_gozlem_gerekceli_bos_kalir(deger):
    i = s11_islem()
    i["sonuc"]["net_r"] = deger
    sonuc, hata = None, None
    try:
        sonuc = istatistik.olc([i], politika="bagimsiz_olcu_v1")
    except (ValueError, TypeError) as yakalanan:
        hata = yakalanan
    assert hata is None, "Geçersiz ölçü gözlemi nedenli boş olarak korunmalı"
    assert sonuc["olculer"]["net_r"]["deger"] is None
    assert sonuc["olculer"]["net_r"]["bos_nedeni"]
    egri = istatistik.egri_dususu(s11_egri([dict(an="2025-01-02", deger=deger)]))
    assert egri["derinlik"]["deger"] is None and egri["derinlik"]["bos_nedeni"]


def test_s11_bilinmeyen_r_ve_tekrar_islem_riski_degistirmez():
    i = s11_islem()
    i["sonuc"].update(ilk_risk=None, net_r=None, risk_nedeni="risk_dayanagi_eksik")
    i["sonuc"]["bos_nedenleri"]["net_r"] = "risk_dayanagi_eksik"
    sonuc = istatistik.olc([i, i.copy()], politika="bagimsiz_olcu_v1")
    assert sonuc["olculer"]["islem"]["deger"] == 1
    assert sonuc["islemler"][0]["olculer"]["net_r"] == dict(
        deger=None, birim="R", bos_nedeni="risk_dayanagi_eksik"
    )
    assert sonuc["olculer"]["net_sonuc"]["deger"] == pytest.approx(-31.5)
    from copy import deepcopy

    farkli = deepcopy(i)
    farkli["sonuc"]["net_sonuc"] = 123.0
    with pytest.raises(ValueError, match="Çelişkili"):
        istatistik.olc([i, farkli], politika="bagimsiz_olcu_v1")


@pytest.mark.parametrize("gun", ["2025-02-30", "bilinmiyor", 1, None])
def test_s11_sharpe_gecersiz_tarih_icin_yilliklastirma_yapmaz(gun):
    karsilastirma = dict(
        politika="gunluk_fark_252_v1",
        kaynak_ref="tarihli-faiz",
        payda="onceki_gun_ozkaynak",
        referanslar=["gunluk-degerleme"],
        getiriler=[dict(an="2025-01-02", deger=0.02), dict(an=gun, deger=0.04)],
        risksiz=[dict(an="2025-01-02", deger=0.01), dict(an=gun, deger=0.01)],
    )
    sonuc = None
    try:
        sonuc = istatistik.olc(
            [], politika="bagimsiz_olcu_v1", karsilastirma=karsilastirma
        )
    except ValueError, TypeError:
        pass
    assert sonuc is not None, "Geçersiz günlük tarih gerekçeli boş sonuç vermeli"
    assert sonuc["olculer"]["sharpe"]["deger"] is None
    assert sonuc["olculer"]["sharpe"]["bos_nedeni"]


def test_s13_sira_her_kaynagi_bir_kez_kullanir_ve_el_toplamini_korur():
    plan = istatistik.mc_plan("sira_v1", "00" * 32, 0, n=3)
    assert sorted(plan.get("indeksler", [])) == [0, 1, 2]
    r = [2.0, -3.0, 1.0]
    assert sum(r[i] for i in plan["indeksler"]) == 0.0


def test_s13_sabit_akis_ve_uzayan_butce_oneki():
    ilk = [istatistik.mc_plan("yerine_koyma_v1", "00" * 32, i, n=5) for i in range(3)]
    uzun = [istatistik.mc_plan("yerine_koyma_v1", "00" * 32, i, n=5) for i in range(7)]
    assert ilk[0]["indeksler"] == [3, 1, 1, 4, 2]
    assert ilk == uzun[:3]
    assert istatistik.mc_plan("sira_v1", "00" * 32, 0, n=5)["indeksler"] == [
        2,
        0,
        1,
        4,
        3,
    ]
    assert istatistik.mc_plan(
        "ayar_komsulugu_v1", "00" * 32, 0, n=5, komsu_sayilari=[2, 3, 1, 2, 3]
    )["demet_indeksleri"] == [1, 0, 0, 0, 2]


def test_s13_ortak_blok_tek_indeks_yoluyla_sutunlari_hizalar():
    p = istatistik.mc_plan("ortak_tarih_blok_v1", "00" * 32, 0, n=5, blok=2)
    assert p["indeksler"] == [3, 4, 1, 4, 0]
    kaynak = np.array([[1.0, -1.0], [2.0, -2.0], [3.0, -3.0], [4.0, -4.0], [5.0, -5.0]])
    assert kaynak[p["indeksler"]].tolist() == [
        [4.0, -4.0],
        [5.0, -5.0],
        [2.0, -2.0],
        [5.0, -5.0],
        [1.0, -1.0],
    ]


def test_s13_el_dususu_ve_tamamen_kacirilan_islemler():
    sonuc = istatistik.mc_olc([2.0, -3.0, 1.0])
    assert sonuc["toplam_r"]["deger"] == 0.0
    assert sonuc["dusus_r"]["deger"] == 3.0
    assert sonuc["kayip_serisi"]["deger"] == 1
    bos = istatistik.mc_olc([], islem_r=[])
    assert bos["toplam_r"]["deger"] == 0.0
    assert bos["dusus_r"]["deger"] == 0.0
    assert bos["ortalama_r"] == dict(deger=None, birim="R", bos_nedeni="islem_yok")
    assert bos["islem_sayisi"]["deger"] == 0
    with pytest.raises(ValueError, match="Boş"):
        istatistik.mc_plan("islem_kacirma_v1", "00" * 32, 0, n=0)


def s13_kapanis_girdisi():
    return dict(
        kaynak_ozeti="00" * 32,
        seanslar=["2022-12-30", "2023-01-02", "2023-01-03"],
        semboller=["A", "B"],
        nufus=[
            dict(
                islem_ref="r1",
                sembol="A",
                giris_tarih="2022-12-01",
                cikis_tarih="2022-12-30",
                net_r=2.0,
            ),
            dict(
                islem_ref="r2",
                sembol="A",
                giris_tarih="2022-12-30",
                cikis_tarih="2023-01-02",
                net_r=-3.0,
            ),
            dict(
                islem_ref="r3",
                sembol="B",
                giris_tarih="2023-01-02",
                cikis_tarih="2023-01-03",
                net_r=1.0,
            ),
        ],
        gunluk_r=[[2.0, 0.0], [-3.0, 0.0], [0.0, 1.0]],
        gunluk_islemler=[[["r1"], []], [["r2"], []], [[], ["r3"]]],
    )


def test_s13_yil_kapanisa_gore_onceki_girisi_alir_ve_bos_kapsami_korur():
    from datetime import date

    g = s13_kapanis_girdisi()
    donemler = [
        dict(ad=str(y), baslangic=date(y, 1, 1), bitis=date(y, 12, 31))
        for y in (2022, 2023, 2024)
    ]
    isler = istatistik.mc_isleri(g, donemler, secim_var=True)
    assert {i["deney"] for i in isler} == set(istatistik.MC_DENEYLER)
    is_ = next(
        i
        for i in isler
        if (i["dilim"], i["deney"], i["sembol"]) == ("2023", "sira_v1", "A")
    )
    olcu = istatistik.mc_senaryo_olculeri(g, is_, dict(indeksler=[0]))
    assert olcu["olculer"]["toplam_r"]["deger"] == -3.0
    assert is_["tanim"]["dilim"]["kesim"] == "2023-01-03"
    assert all(
        i["durum"] == "olculemedi" and i["neden"] == "kapali_islem_yok"
        for i in isler
        if i["dilim"] == "2024"
    )
    assert all(
        i["neden"] == "blok_boyu_belirsiz"
        for i in isler
        if i["deney"] == "ortak_tarih_blok_v1" and i["dilim"] != "2024"
    )


def test_s13_takvim_tanisi_ortak_satirlari_ve_kacirma_masrafini_korur():
    from datetime import date

    g = s13_kapanis_girdisi()
    ortak = dict(
        tanim=dict(dilim=dict(baslangic=date(2023, 1, 1), bitis=date(2023, 12, 31))),
        sembol="eklemeli",
    )
    blok = istatistik.mc_senaryo_olculeri(
        g, ortak | dict(deney="ortak_tarih_blok_v1"), dict(indeksler=[1, 0])
    )
    assert blok["olculer"]["toplam_r"]["deger"] == -2.0
    assert blok["olculer"]["dusus_r"]["deger"] == 3.0
    assert blok["olculer"]["islem_sayisi"]["deger"] == 2
    assert blok["sembol_olculeri"]["A"]["toplam_r"]["deger"] == -3.0
    assert blok["sembol_olculeri"]["B"]["toplam_r"]["deger"] == 1.0
    atlanan = istatistik.mc_senaryo_olculeri(
        g, ortak | dict(deney="islem_kacirma_v1"), dict(maske=[False, True])
    )
    assert atlanan["olculer"]["toplam_r"]["deger"] == 1.0
    assert atlanan["olculer"]["dusus_r"]["deger"] == 0.0
    assert atlanan["olculer"]["islem_sayisi"]["deger"] == 1
    assert atlanan["sembol_olculeri"]["A"]["ortalama_r"]["bos_nedeni"] == "islem_yok"


@pytest.mark.parametrize(
    "seri,ham,boylar",
    [
        (list(range(20)), 4.5407054019398005, [3, 5, 10]),
        ([1.0, -1.0] * 20, 14.0, [7, 14, 28]),
        ([0.0, 2.0, -1.0, 3.0, -2.0, 1.0] * 10, 4.635991196842948, [3, 5, 10]),
    ],
)
def test_s13_ppw_arch72_sabit_referanslari(seri, ham, boylar):
    # S13 referans denklemleri bağımsız skaler toplamlarla hesaplandı.
    sonuc = istatistik.mc_blok_tahmini(seri)
    assert sonuc["ham"] == pytest.approx(ham, abs=1e-12)
    assert sonuc["uzunluklar"] == boylar
    assert sonuc["neden"] is None


@pytest.mark.parametrize(
    "seri", [[], [1.0], [1.0, 2.0], [1.0] * 40, [0.0, float("nan")] * 20]
)
def test_s13_tanimsiz_blok_boyu_gizli_varsayilan_uretmez(seri):
    sonuc = istatistik.mc_blok_tahmini(seri)
    assert sonuc["ham"] is None
    assert sonuc["uzunluklar"] == []
    assert sonuc["neden"] == "blok_boyu_belirsiz"


def test_s13_sayisal_durma_ardisik_iki_nokta_ister():
    s = istatistik.mc_olc([1.0, -2.0, 3.0])
    preview = istatistik.mc_kontrol([s] * 1000)
    ilk = istatistik.mc_kontrol([s] * 10000)
    son = istatistik.mc_kontrol([s] * 20000, onceki=ilk)
    assert preview["durum"] == "on_gosterim"
    assert ilk["durum"] == "suruyor"
    assert son["durum"] == "sayisal_kararlilik_gozlendi"
    assert son["uclar"] == [2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    assert son["onceki_farklari"] == [0.0] * 6
    farkli = [
        istatistik.mc_olc([0.0]) if i % 2 else istatistik.mc_olc([1.0])
        for i in range(100000)
    ]
    kararsiz = istatistik.mc_kontrol(farkli)
    assert kararsiz["durum"] == "sinirda_kararsiz"
    assert kararsiz["tekrar"] == 100000
    assert kararsiz["bolum_gecti"] is False


def test_s13_yuzdelikler_dogrusal_ve_gecerli_sayilar_olcuye_ozgudur():
    sonuclar = []
    for i in range(1000):
        s = istatistik.mc_olc([-0.5 * i, 1.5 * i])
        if i < 7:
            s["ortalama_r"] = dict(deger=None, birim="R", bos_nedeni="islem_yok")
        sonuclar.append(s)
    tani = istatistik.mc_kontrol(sonuclar)
    assert tani["uclar"] == pytest.approx(
        [49.95, 499.5, 949.05, 24.975, 249.75, 474.525]
    )
    assert tani["gecerli_sayilar"]["ortalama_r"] == 993
    assert tani["gecerli_sayilar"]["dusus_r"] == 1000
    assert tani["durum"] == "on_gosterim"


@pytest.mark.parametrize(
    "ad,kw",
    [
        ("sira_v1", dict(n=0)),
        ("sira_v1", dict(n=True)),
        ("ortak_tarih_blok_v1", dict(n=5, blok=6)),
        ("ayar_komsulugu_v1", dict(n=2, komsu_sayilari=[0, 1])),
    ],
)
def test_s13_gecersiz_plan_sessiz_duzeltilmez(ad, kw):
    with pytest.raises(ValueError):
        istatistik.mc_plan(ad, "00" * 32, 0, **kw)
