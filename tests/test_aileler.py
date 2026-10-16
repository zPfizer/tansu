"""`aileler` yüzü: EMA sıkışması giriş sinyali (KURALLAR §3 madde 2). Beklenen değerler elle hesaplandı."""

from dataclasses import asdict

import numpy as np
import pandas as pd
import pytest

from tansu import aileler, gostergeler
from tansu.aileler import (
    Parametre,
    on_sart,
    pencere_gunleri,
    sikismasiz_kirilim,
    sinyal,
)


def _fiyat(kapanis, yuksek=None):
    gun = pd.bdate_range("2026-03-02", periods=len(kapanis))
    return pd.DataFrame(
        {
            "kapanis": [float(k) for k in kapanis],
            "yuksek": yuksek or [k + 0.5 for k in kapanis],
        },
        index=gun,
    )


def test_sikismadan_sonra_pencerede_ilk_kirilim_tek_giris():
    # Küçük parametre: periyotlar (1, 2) -> EMA1 = kapanış, EMA2 alfa=2/3; eşik 0,005; en az 3 gün; pencere 3.
    # Kapanış [100x5, 103, 104, 105]. Gün 0-4: oran 0 -> sıkışma dönemi (5 gün), en yüksek yüksek = 101 (gün 2).
    # Gün 5: EMA2 = 100 + 3*2/3 = 102, oran = (103-102)/102 = 0,0098 > 0,005 -> dönem gün 4'te biter.
    # Pencere = gün 5, 6, 7. Gün 5 kapanışı 103 > 101 -> sinyal. Gün 6 ve 7 de 101'in üstünde ama
    # dönem başına tek giriş. Isınma 6: gün 5'te 6 gün dolmuş (izin). SMA(2) gün 5 = 101,5 <= 103.
    yuksek = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5]
    f = _fiyat([100, 100, 100, 100, 100, 103, 104, 105], yuksek)
    p = Parametre(
        periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=6, sma_n=2
    )
    assert list(sinyal(f, p)) == [f.index[5]]


def test_isinma_dolmadan_sinyal_yok_dolunca_pencerede_ilk_gun():
    # Aynı veri. Isınma 7: gün 5'te yalnız 6 gün var, sinyal yok; gün 6'da 7 gün dolu ve 104 > 101 -> sinyal.
    # Isınma 9: pencere (gün 5-7) bitene kadar hiç izin yok -> sinyal yok.
    yuksek = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5]
    f = _fiyat([100, 100, 100, 100, 100, 103, 104, 105], yuksek)
    ortak = dict(periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, sma_n=2)
    assert list(sinyal(f, Parametre(isinma=7, **ortak))) == [f.index[6]]
    assert list(sinyal(f, Parametre(isinma=9, **ortak))) == []


def test_kapanis_sma_altindaysa_sinyal_yok():
    # Kapanış [200x4, 100x7, 105, 106, 107] (gün 0-13), yüksek = kapanış + 0,5, eşik 0,005, en az 3 gün.
    # EMA2 (alfa 2/3) düşüşten sonra aralıkları üçte birine indirir: gün 4'te 33,33; gün 7'de 1,235
    # (oran 0,0122 > eşik); gün 8'de 0,4115 (oran 0,0041 <= eşik). Gün 8-10: dönem (3 gün), en yüksek yüksek 100,5.
    # Gün 11: kapanış 105 -> oran (105-103,35)/103,35 = 0,016 > eşik, dönem gün 10'da biter, 105 > 100,5.
    # SMA(2) gün 11 = (100+105)/2 = 102,5 <= 105 -> sinyal gün 11.
    # SMA(12) gün 11 = (4*200 + 7*100 + 105)/12 = 133,75 > 105 -> sinyal yok. Gün 12 ve 13 de SMA(12) üstünde
    # (125,9 ve 118,2). Gün 0-3 dönemi (sabit 200): sonrasında kapanış 200,5'i geçmez.
    kapanis = [200] * 4 + [100] * 7 + [105, 106, 107]
    f = _fiyat(kapanis)
    ortak = dict(periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=4)
    assert list(sinyal(f, Parametre(sma_n=2, **ortak))) == [f.index[11]]
    assert list(sinyal(f, Parametre(sma_n=12, **ortak))) == []


def test_on_sart_pencere_gunleri_ve_sikismasiz_kirilim():
    # Aynı veri (ilk test): pencere gün 5, 6, 7; hepsi SMA(2) üstünde. Isınma 6: gün 5'te dolu -> hepsi ön şartlı.
    # Isınma 7: gün 5'te yalnız 6 gün var -> gün 6, 7. Sıkışmasız kırılım: üç günün üçü de pencere içinde -> yok.
    yuksek = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5]
    f = _fiyat([100, 100, 100, 100, 100, 103, 104, 105], yuksek)
    ortak = dict(periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, sma_n=2)
    assert list(on_sart(f, Parametre(isinma=6, **ortak))) == [False] * 5 + [True] * 3
    assert list(on_sart(f, Parametre(isinma=7, **ortak))) == [False] * 6 + [True] * 2
    assert not sikismasiz_kirilim(f, Parametre(isinma=6, **ortak), 3).any()


def test_sikismasiz_kirilim_onceki_l_gunun_yuksegini_asan_pencere_disi_gun():
    # Kapanış [100,103,106,109,112,115], yüksek = kapanış + 0,5: EMA2 gecikmesi 1,5 -> oran > 0,005, sıkışma dönemi yok.
    # Gün i >= 3: kapanış > önceki 3 günün en yüksek yükseği (örn. gün 3: 109 > 106,5). Isınma 4 -> gün 3, 4, 5; isinma 5 -> 4, 5.
    f = _fiyat([100, 103, 106, 109, 112, 115])
    ortak = dict(periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, sma_n=2)
    assert not pencere_gunleri(f, Parametre(isinma=4, **ortak)).any()
    assert (
        list(sikismasiz_kirilim(f, Parametre(isinma=4, **ortak), 3))
        == [False] * 3 + [True] * 3
    )
    assert (
        list(sikismasiz_kirilim(f, Parametre(isinma=5, **ortak), 3))
        == [False] * 4 + [True] * 2
    )


# --- Modül 1 (KURALLAR §3 "Modül 1"): kurulum, giriş türleri, süzgeçler, bölgeler, hedef, varyantlar ---


def _mumlar(kapanis, yuksek=None, dusuk=None, hacim=None):
    gun = pd.bdate_range("2026-03-02", periods=len(kapanis))
    return pd.DataFrame(
        {
            "kapanis": [float(k) for k in kapanis],
            "yuksek": [float(y) for y in yuksek or [k + 1 for k in kapanis]],
            "dusuk": [float(d) for d in dusuk or [k - 1 for k in kapanis]],
            "hacim": [float(h) for h in hacim or [100] * len(kapanis)],
        },
        index=gun,
    )


def _gunler(f, p):
    """Kurulum sinyal günlerinin `f` içindeki konumları."""
    return [f.index.get_loc(g) for g in aileler.kurulum(f, p).index]


# Küçük ayar: EMA2 (alfa 2/3) ve EMA3 (alfa 1/2); sıkışma eşiği 0,004; en az 3 gün; pencere 3; ısınma yok; SMA2.
KUCUK = dict(periyotlar=(2, 3), esik=0.004, min_gun=3, pencere=3, isinma=1, sma_n=2)
# Düz 14 günden sonra ilk gün: oran 0,003 ila 0,0065 (EMA2 ile EMA3 farkı); eşik 0,002 dönemi bitirir. SMA10.
MUM = dict(KUCUK, esik=0.002, sma_n=10)


def test_parametre_yeni_alanlar_varsayilani_bugunku_kurali_korur():
    p = Parametre()
    assert (p.giris, p.hacim_kat, p.momentum, p.teyit) == ("kutu", 0.0, False, "yok")
    assert (p.stop, p.hedef, p.rr_min, p.cikis) == ("atr2", "yok", 2.0, "yok")


@pytest.mark.parametrize(
    "alan, deger",
    [
        ("giris", "kutuu"),
        ("teyit", "evet"),
        ("stop", "atr3"),
        ("hedef", "var"),
        ("cikis", "atr2"),
    ],
)
def test_parametre_tanimsiz_secenek_hata_verir(alan, deger):
    # Sessiz düzeltme yok (CODING_STANDARDS "Fail loud"): bilinmeyen seçenek sessizce başka kurala düşmez.
    with pytest.raises(ValueError, match=alan):
        Parametre(**{alan: deger})


def test_kurulum_sinyal_gunu_kutu_alt_kutu_ust_ve_hedef_sutunlari():
    # İlk testin verisi. Gün 0-4 sıkışma dönemi. Kutu üstü = dönemin en yüksek yükseği = 101 (gün 2).
    # Kutu altı = dönemin en düşük düşüğü = 99 (gün 1). Gün 5 kapanışı 103 > 101 -> sinyal. Hedef yok -> NaN.
    f = _mumlar(
        [100, 100, 100, 100, 100, 103, 104, 105],
        [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5],
        [99.5, 99, 99.5, 99.5, 99.5, 102.5, 103.5, 104.5],
    )
    p = Parametre(
        periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=6, sma_n=2
    )
    k = aileler.kurulum(f, p)
    assert list(k.columns) == ["kutu_alt", "kutu_ust", "hedef"]
    assert list(k.index) == [f.index[5]]
    assert list(sinyal(f, p)) == list(k.index)
    assert (k.iloc[0]["kutu_alt"], k.iloc[0]["kutu_ust"]) == (99.0, 101.0)
    assert np.isnan(k.iloc[0]["hedef"])
    # Yalnız kapanış ve yüksek sütunu olan çerçeve: varsayılan kural çalışır, kutu altı bilinmez.
    k2 = aileler.kurulum(f[["kapanis", "yuksek"]], p)
    assert list(k2.index) == [f.index[5]]
    assert np.isnan(k2.iloc[0]["kutu_alt"]) and k2.iloc[0]["kutu_ust"] == 101.0


def test_giris_ema_kapanis_en_buyuk_emanin_ustunde_kutu_tepesini_beklemez():
    # Kapanış [100x5, 103, 104, 105]; gün 2 yükseği 104 (kutu üstü 104). Gün 5: EMA2 = 102, EMA3 = 101,5,
    # oran 0,5/101,5 = 0,0049 > 0,004 -> dönem gün 4'te biter. Pencere gün 5, 6, 7.
    # "kutu": 103 > 104 hayır; 104 > 104 hayır; 105 > 104 evet -> gün 7.
    # "ema": gün 5 kapanışı 103 > en büyük EMA (102) -> gün 5.
    f = _mumlar(
        [100, 100, 100, 100, 100, 103, 104, 105],
        [100.5, 100.5, 104, 100.5, 100.5, 103.5, 104.5, 105.5],
    )
    assert _gunler(f, Parametre(giris="kutu", **KUCUK)) == [7]
    assert _gunler(f, Parametre(giris="ema", **KUCUK)) == [5]


def _sikismadan_mum(c, y, d, tepe=101.0):
    """14 düz gün (100; 101; 99), sonra tek mum (kapanış c, yüksek y, düşük d), iki gün aynı kapanış."""
    yuk = [101.0] * 14 + [y, c + 0.5, c + 0.5]
    yuk[2] = tepe
    return _mumlar([100.0] * 14 + [c, c, c], yuk, [99.0] * 14 + [d, c - 0.5, c - 0.5])


# Düz 14 günün ATR'si 2 (her gerçek aralık 2). Kutu üstü = tepe (gün 2 yükseği), kutu altı 99. Mum günü 14.
# 1) 104; 104,5; 100: yeşil (104 > 100); aralık 4,5 >= ATR (26+4,5)/14 = 2,18; (104-100)/4,5 = 0,89 >= 2/3; 104 > 101 -> gün 14.
# 2) 102; 102; 100,2: GR = max(1,8; 2; 0,2) = 2, ATR = 2; aralık 1,8 < 2 -> uzun değil.
# 3) 102; 104; 100: GR = 4, ATR = 30/14 = 2,14; aralık 4 >= ATR; (102-100)/4 = 0,5 < 2/3 -> güçlü değil.
# 4) 104; 104,5; 100 ama kutu üstü 105: 104 > 105 hayır -> kutudan yukarı değil.
@pytest.mark.parametrize(
    "c, y, d, tepe, beklenen",
    [
        (104.0, 104.5, 100.0, 101.0, [14]),
        (102.0, 102.0, 100.2, 101.0, []),
        (102.0, 104.0, 100.0, 101.0, []),
        (104.0, 104.5, 100.0, 105.0, []),
    ],
    ids=["gecer", "uzun-degil", "guclu-degil", "kutu-ustunde-degil"],
)
def test_giris_mum_yesil_uzun_guclu_ve_kutudan_yukari(c, y, d, tepe, beklenen):
    f = _sikismadan_mum(c, y, d, tepe)
    p = Parametre(giris="mum", **MUM)
    assert _gunler(f, p) == beklenen
    if beklenen:
        k = aileler.kurulum(f, p).iloc[0]
        assert (k["kutu_alt"], k["kutu_ust"]) == (99.0, tepe)


def _mum_sonrasi(satirlar, on=14, mum_hacmi=100.0):
    """`on` düz gün (100; 101; 99; hacim 100), güçlü mum günü (104; 104,5; 100), sonra `satirlar` (kapanış, yüksek, düşük, hacim)."""
    k, y, d, h = zip(
        *([(100, 101, 99, 100)] * on + [(104, 104.5, 100, mum_hacmi)] + satirlar)
    )
    return _mumlar(k, y, d, h)


# Mum günü k = 14 (kutu üstü 101). j = k+1 ... k+5 içinde düşüğü <= 101 olan ilk gün; kapanışı > 101 ise sinyal j.
# A) gün 15: düşük 100,8 <= 101, kapanış 102 > 101 -> sinyal 15 (SMA10 = 100,6 <= 102).
# B) gün 15: düşük 100,5, kapanış 100,9 <= 101 -> bu dönemde sinyal yok (gün 16 aranmaz).
# C) gün 15-18 düşük 103 (geri çekilme yok); gün 19 = k+5: düşük 100,5, kapanış 103 -> sinyal 19 (SMA10 = 102,5 <= 103).
# D) geri çekilme gün 20 = k+6 -> yok.
@pytest.mark.parametrize(
    "satirlar, beklenen",
    [
        ([(102, 103, 100.8, 100)], [15]),
        ([(100.9, 103, 100.5, 100), (102, 103, 101.5, 100)], []),
        ([(104.5, 105, 103, 100)] * 4 + [(103, 104, 100.5, 100)], [19]),
        ([(104.5, 105, 103, 100)] * 5 + [(103, 104, 100.5, 100)], []),
    ],
    ids=["gecer", "kapanis-kutu-altinda", "k5-gun", "k6-gun"],
)
def test_giris_retest_mum_sonrasi_kucuk_geri_cekilme(satirlar, beklenen):
    f = _mum_sonrasi(satirlar)
    assert _gunler(f, Parametre(giris="retest", **MUM)) == beklenen


# 20 düz gün (hacim 100, ortalama 100); mum günü 20, geri çekilme günü 21 (hacim 10).
# Hacim şartı mum gününde aranır: 250 >= 2*100 -> sinyal gün 21 (gün 21'in hacmi 10 şart değil). 150 < 200 -> yok.
@pytest.mark.parametrize("mum_hacmi, beklenen", [(250.0, [21]), (150.0, [])])
def test_retest_hacim_sarti_mum_gununde_aranir(mum_hacmi, beklenen):
    f = _mum_sonrasi([(102, 103, 100.8, 10)], on=20, mum_hacmi=mum_hacmi)
    p = Parametre(giris="retest", hacim_kat=2.0, **MUM)
    assert _gunler(f, p) == beklenen


AGRESIF = dict(KUCUK, sma_n=1)  # SMA1 = kapanış: SMA şartı hep sağlanır


def test_giris_agresif_sikisma_surerken_kutu_altina_degip_altinda_kapanmayan_gun():
    # Kapanış 100 x 8: gün 0-7 hepsi sıkışma (oran 0); dönem hiç bitmiyor, "kutu" girişi sinyal vermez.
    # Düşük [99,5; 99,5; 99; 99,5; 99,5; 98,8; 98,5; 99,5]; yüksek gün 3 = 101, öbürleri 100,5.
    # t=2: düşük 99 <= 99,5 ve kapanış 100 >= 99,5, ama t-1'de biten koşu yalnız 2 gün (< 3) -> yok.
    # t=3 ve 4: önceki en düşük düşük 99; düşük 99,5 > 99 -> yok.
    # t=5: koşu gün 0-4 (5 gün), önceki en düşük düşük 99; düşük 98,8 <= 99 ve kapanış 100 >= 99 -> sinyal.
    #   Kutu altı = 98,8 (t dahil en düşük), kutu üstü = 101 (t dahil en yüksek).
    # t=6: düşük 98,5 <= 98,8 ama koşu başına tek sinyal -> yok.
    f = _mumlar(
        [100] * 8,
        [100.5, 100.5, 100.5, 101, 100.5, 100.5, 100.5, 100.5],
        [99.5, 99.5, 99, 99.5, 99.5, 98.8, 98.5, 99.5],
    )
    assert _gunler(f, Parametre(giris="kutu", **AGRESIF)) == []
    p = Parametre(giris="agresif", **AGRESIF)
    assert _gunler(f, p) == [5]
    k = aileler.kurulum(f, p).iloc[0]
    assert (k["kutu_alt"], k["kutu_ust"]) == (98.8, 101.0)


@pytest.mark.parametrize("kapanis_5, beklenen", [(99.0, [5]), (98.9, [])])
def test_agresif_kutu_altinda_kapanis_analizi_iptal_eder(kapanis_5, beklenen):
    # Gün 0-4 kapanış 100, düşük [99,5; 99,5; 99; 99,5; 99,5]; gün 5 düşüğü 98,8 kutu altına (99) değer.
    # Kapanış 99 >= 99 -> değdi, altında kapanmadı -> sinyal. Kapanış 98,9 < 99 -> altında kapandı -> yok.
    f = _mumlar(
        [100] * 5 + [kapanis_5],
        [100.5] * 6,
        [99.5, 99.5, 99, 99.5, 99.5, 98.8],
    )
    assert _gunler(f, Parametre(giris="agresif", **AGRESIF)) == beklenen


# Kapanış [100x20, 103, 104, 105, 106]; kutu üstü 101; gün 20-22 pencere. Hacim [100x20, 150, 206, 100, 100].
# Ortalama = önceki 20 günün hacim ortalaması, t hariç.
# Gün 20: ortalama 100. Gün 21: gün 1-20 = (19*100+150)/20 = 102,5; 206 >= 2*102,5 = 205 evet.
#   (Gün 21 ortalamaya girseydi ortalama 107,8, eşik 215,6 olurdu ve 206 geçmezdi.)
# Gün 22: gün 2-21 = (18*100+150+206)/20 = 107,8; 100 < 3*107,8 hayır.
# kat 0: gün 20. kat 2: gün 20 için 150 < 200 hayır; gün 21 evet -> 21. kat 3: gün 21 için 206 < 307,5; gün 22 hayır -> yok.
@pytest.mark.parametrize("kat, beklenen", [(0.0, [20]), (2.0, [21]), (3.0, [])])
def test_hacim_suzgeci_onceki_20_gunun_ortalamasinin_kati_t_haric(kat, beklenen):
    f = _mumlar(
        [100] * 20 + [103, 104, 105, 106],
        [101] * 20 + [103.5, 104.5, 105.5, 106.5],
        [99] * 20 + [102.5, 103.5, 104.5, 105.5],
        [100] * 20 + [150, 206, 100, 100],
    )
    assert _gunler(f, Parametre(hacim_kat=kat, **KUCUK)) == beklenen


# Kapanış [100x5, 103, 104, 105], kutu üstü 101: gün 5, 6, 7 kutu tetiğini sağlar. Momentum değerleri verilir (hesap göstergelerde sınanır).
# 1) gün 4 -1, gün 5 -2: negatif ve düşüyor -> gün 5 aday değil. Gün 6: -1,5 < -2 değil -> aday -> 6.
# 2) gün 4 -2, gün 5 -1: negatif ama yükseliyor -> gün 5.
# 3) gün 4 +2, gün 5 +1: düşüyor ama pozitif -> gün 5.
# 4) süzgeç kapalı: 1. durumdaki değerler yok sayılır -> gün 5.
@pytest.mark.parametrize(
    "val, momentum, beklenen",
    [
        ([0, 0, 0, 0, -1, -2, -1.5, -1.5], True, [6]),
        ([0, 0, 0, 0, -2, -1, -1, -1], True, [5]),
        ([0, 0, 0, 0, 2, 1, 1, 1], True, [5]),
        ([0, 0, 0, 0, -1, -2, -1.5, -1.5], False, [5]),
    ],
    ids=["negatif-dusuyor", "negatif-yukseliyor", "pozitif-dusuyor", "kapali"],
)
def test_momentum_suzgeci_negatif_ve_dusen_gun_aday_degil(
    monkeypatch, val, momentum, beklenen
):
    f = _mumlar([100, 100, 100, 100, 100, 103, 104, 105])
    seri = pd.Series(val, index=f.index, dtype=float)
    monkeypatch.setattr(gostergeler, "momentum_squeeze", lambda *a, **k: seri)
    assert _gunler(f, Parametre(momentum=momentum, **KUCUK)) == beklenen


# Aynı veri. Üç gösterge teyidi birlikte aranır: MACD histogramı artıyor (h_t > h_{t-1}), PSAR < kapanış, %K > %D.
# Hepsi sağlanır -> gün 5. MACD histogramı düşüyor, PSAR üstte (200 > 103), %K <= %D -> her biri tek başına yok.
# Histogram [0,0,0,0,0,0,1,1]: gün 5 için 0 > 0 hayır; gün 6 için 1 > 0 evet -> 6.
@pytest.mark.parametrize(
    "hist, psar, k, d, beklenen",
    [
        ([0, 0, 0, 0, 0, 1, 2, 3], 99.0, 50.0, 40.0, [5]),
        ([0, 0, 0, 0, 0, -1, -2, -3], 99.0, 50.0, 40.0, []),
        ([0, 0, 0, 0, 0, 0, 1, 1], 99.0, 50.0, 40.0, [6]),
        ([0, 0, 0, 0, 0, 1, 2, 3], 200.0, 50.0, 40.0, []),
        ([0, 0, 0, 0, 0, 1, 2, 3], 99.0, 30.0, 40.0, []),
    ],
    ids=["hepsi", "macd-dusuyor", "macd-gun-6", "psar-ustte", "stokastik-asagida"],
)
def test_gosterge_teyidi_macd_psar_ve_stokastik_birlikte(
    monkeypatch, hist, psar, k, d, beklenen
):
    f = _mumlar([100, 100, 100, 100, 100, 103, 104, 105])
    seri = lambda v: pd.Series(v, index=f.index, dtype=float)  # noqa: E731
    monkeypatch.setattr(gostergeler, "macd_histogram", lambda *a, **kw: seri(hist))
    monkeypatch.setattr(gostergeler, "psar", lambda *a, **kw: seri(psar))
    monkeypatch.setattr(gostergeler, "stokastik", lambda *a, **kw: (seri(k), seri(d)))
    assert _gunler(f, Parametre(teyit="gosterge", **KUCUK)) == beklenen


def _trend_cercevesi(yuksek, dusuk, n):
    """Kapanış: 9 gün 90/100 salınımı (salınım noktaları burada), 7 düz gün 100 (sıkışma, gün 12-15), sonra 103; 106; 109."""
    kap = [90, 100, 90, 100, 90, 100, 90, 100, 90] + [100] * 7 + [103, 106, 109]
    return _mumlar(kap[:n], yuksek[:n], dusuk[:n])


# Salınım tepeleri gün 2 (110) ve gün 6 (109) (yüksek [100,102,110,102,100,102,109,103,101] sonra artan). Doğru: eğim -1/4,
# değeri t'de 109 - (t-6)/4: gün 16 106,5; gün 17 106,25; gün 18 106. Kutu üstü 100,5; kapanış 103 / 106 / 109.
# Teyit yok: gün 16. Teyit trend: 103 > 106,5 hayır; 106 > 106,25 hayır; 109 > 106 evet -> gün 18.
# Düşükler tek yönlü azalır -> salınım dibi yok (yükselen trend kolu kapalı). Gün 16-18 tepeleri artan -> salınım tepesi yok.
def _dusen_trend_cercevesi():
    yuksek = [100, 102, 110, 102, 100, 102, 109, 103, 101]
    yuksek += [100.0, 100.05, 100.1, 100.2, 100.3, 100.4, 100.5]
    yuksek += [103.5, 106.5, 109.5]
    return _trend_cercevesi(yuksek, [89 - 0.1 * i for i in range(19)], 19)


def test_teyit_trend_dusen_trend_kirilimi():
    f = _dusen_trend_cercevesi()
    assert _gunler(f, Parametre(**KUCUK)) == [16]
    assert _gunler(f, Parametre(teyit="trend", **KUCUK)) == [18]


def _yukselen_trend_cercevesi(x, n):
    dusuk = [95, 93, 90, 93, 95, 94, 91, 93, 94]
    dusuk += [95.0, 95.1, 95.2, 95.3, 95.4, 95.5, 95.6]
    dusuk += [x, 96.0, 96.0]
    return _trend_cercevesi([101 + 0.1 * i for i in range(19)], dusuk, n)


# Salınım dipleri gün 2 (90) ve gün 6 (91) (düşük [95,93,90,93,95,94,91,93,94] sonra artan). Doğru d(x) = 90 + (x-2)/4:
# d(16) = 93,5. Yüksekler artan -> düşen trend kolu kapalı. Gün 16 düşüğü X; kapanışlar 103 (gün 16), 106 (gün 17).
# Gün 16: son 5 gün düşükleri 95'in üstünde, d(u)*1,01 < 94,2 -> temas yok; u=16 için kapanış_t > kapanış_u hayır -> geçmez.
# Gün 17: u=16: X <= 93,5*1,01 = 94,435 ve 103 >= 93,5 ve 106 > 103 -> X = 94,4 geçer (sinyal 17); X = 94,5 geçmez.
@pytest.mark.parametrize("x, beklenen", [(94.4, [17]), (94.5, [])])
def test_teyit_trend_yukselen_trende_temas_ve_tepki(x, beklenen):
    f = _yukselen_trend_cercevesi(x, 18)
    assert _gunler(f, Parametre(**KUCUK)) == [16]
    assert _gunler(f, Parametre(teyit="trend", **KUCUK)) == beklenen


# Gün 16 düşüğü (X) bir salınım dibidir, ama gün 18 verisi gelince bilinir (i+2 <= t). 19 günlük çerçevede X = 94,5:
# gün 17'de dip çifti hâlâ (2, 6) -> geçmez; gün 18'de çift (6, 16), doğru 94,5'ten geçer -> sinyal 18.
# Veri gün 17'de kesilirse (18 gün) sinyal yok; gün 18'den önceki çıktı tam veriyle aynı kalmalı.
@pytest.mark.parametrize(
    "f",
    [_dusen_trend_cercevesi(), _yukselen_trend_cercevesi(94.5, 19)],
    ids=["dusen", "yukselen"],
)
def test_teyit_trend_t_den_sonraki_gunler_t_oncesi_karari_degistirmez(f):
    p = Parametre(teyit="trend", **KUCUK)
    tam = aileler.kurulum(f, p)
    assert len(tam) == 1  # sınama boş değil
    for n in range(12, len(f) + 1):
        kesik = aileler.kurulum(f.iloc[:n], p)
        pd.testing.assert_frame_equal(tam[tam.index <= f.index[n - 1]], kesik)


def _ucgen_cercevesi(dusuk=None):
    """13 düz gün (kapanış 100) üçgen şekilli yüksek ve düşüklerle, sonra kırılım günü 13 (kapanış 108)."""
    yuk = [101, 102, 105, 102, 101, 101, 102, 102.5, 105.5, 102, 101, 101, 101, 108.5]
    dus = dusuk or [99, 99, 99, 96, 99, 99, 97, 99, 99, 98, 99, 99, 99, 107]
    return _mumlar([100.0] * 13 + [108.0], yuk, dus)


# Gün 0-12 dönem; kutu üstü 105,5, kutu altı 96. Salınım tepeleri gün 2 (105) ve gün 8 (105,5): 105,5 <= 105*1,01 = 106,05.
# Salınım dipleri gün 3 (96), gün 6 (97), gün 9 (98): yükseliyor. Hedef = 105,5 + (105 - 96) = 114,5.
# Gün 13 kapanışı 108 > 105,5 -> kutu girişi. R/R (kutu stopu): (114,5-108)/(108-96) = 6,5/12 = 0,5417.
def test_ucgen_hedefi_en_yuksek_tepe_arti_taban_yuksekligi():
    f = _ucgen_cercevesi()
    k = aileler.kurulum(f, Parametre(hedef="tansu", stop="kutu", rr_min=0.5, **KUCUK))
    assert list(k.index) == [f.index[13]]
    assert k.iloc[0]["hedef"] == pytest.approx(114.5, abs=1e-9)
    assert (k.iloc[0]["kutu_alt"], k.iloc[0]["kutu_ust"]) == (96.0, 105.5)


# Gün 13 gerçek aralığı = max(1,5; 8,5; 7) = 8,5. Gün 0-12 gerçek aralıkları yüksek - düşük: toplam 1327 - 1281 = 46.
# ATR13 = (46 + 8,5) / 14 = 54,5/14 = 3,8929. Risk ödül = (114,5 - 108) / (108 - stop tahmini):
# kutu: stop 96 -> 6,5/12 = 0,5417. atr2: stop 108 - 7,7857 = 100,2143 -> 6,5/7,7857 = 0,8349.
# atr15: stop 108 - 5,8393 = 102,1607 -> 6,5/5,8393 = 1,1131. Kapı: oran >= rr_min.
@pytest.mark.parametrize(
    "stop, rr_min, beklenen",
    [
        ("kutu", 0.5, [13]),
        ("kutu", 0.6, []),
        ("kutu", 2.0, []),
        ("atr2", 0.7, [13]),
        ("atr2", 1.0, []),
        ("atr15", 1.0, [13]),
        ("atr15", 1.2, []),
    ],
)
def test_rr_kapisi_stop_tahmini_kutu_atr15_atr2(stop, rr_min, beklenen):
    f = _ucgen_cercevesi()
    p = Parametre(hedef="tansu", stop=stop, rr_min=rr_min, **KUCUK)
    assert _gunler(f, p) == beklenen


def test_rr_kapisi_hedef_bulunmazsa_uygulanmaz_hedef_yok_iken_de():
    # Düşükler düz (99): salınım dipleri eşit, "her dip bir öncekinden yüksek" sağlanmaz -> üçgen yok; arz bölgesi yok.
    # Hedef bulunmaz -> kapı uygulanmaz: oran 0,54 < 2 olsa da gün 13 sinyal. Hedef sütunu NaN.
    # hedef "yok" iken (varsayılan) üçgen bulunsa da kapı ve hedef yok.
    f = _ucgen_cercevesi([99] * 13 + [107])
    k = aileler.kurulum(f, Parametre(hedef="tansu", stop="kutu", **KUCUK))
    assert list(k.index) == [f.index[13]] and np.isnan(k.iloc[0]["hedef"])
    k2 = aileler.kurulum(_ucgen_cercevesi(), Parametre(stop="kutu", **KUCUK))
    assert list(k2.index) == [_ucgen_cercevesi().index[13]]
    assert np.isnan(k2.iloc[0]["hedef"])


def _arz_ve_ucgen(ucgen):
    """P1: gün 0-13 düz 100 (ATR 2). Gün 14 arz mumu (112), gün 17 bölge bilinir (96). P2: gün 20-32 düz 96, kırılım gün 33 (99,4)."""
    p2_yuksek = [
        97.0,
        97.2,
        97.6,
        97.2,
        97.0,
        97.0,
        97.2,
        97.3,
        97.8,
        97.2,
        97.0,
        97.0,
        97.0,
    ]
    p2_dusuk = {
        "uzak": [
            95.0,
            95.0,
            95.0,
            92.0,
            95.0,
            95.0,
            92.5,
            95.0,
            95.0,
            93.0,
            95.0,
            95.0,
            95.0,
        ],
        "yakin": [
            95.95,
            95.95,
            95.95,
            95.5,
            95.95,
            95.95,
            95.7,
            95.95,
            95.95,
            95.9,
            95.95,
            95.95,
            95.95,
        ],
        "yok": [95.95] * 13,
    }[ucgen]
    if ucgen == "yok":
        p2_yuksek = [97.0] * 13
    return _mumlar(
        [100] * 14 + [112, 108, 100, 96] + [96] * 15 + [99.4],
        [101] * 14 + [113, 109, 101, 100] + [97, 97] + p2_yuksek + [99.9],
        [99] * 14 + [100, 107, 99, 95] + [95.95, 95.95] + p2_dusuk + [97.0],
    )


# Gün 14 yeşil (112 > 100), gün 15 yeşil değil; ATR14 = (26+13)/14 = 39/14 = 2,786; eşik = gövde altı (önceki kapanış 100)
# - ATR = 97,21; gün 15 (108), 16 (100) üstünde, gün 17 (96) altında -> bölge gün 17'de bilinir: proximal 100, distal 113.
# P1 (gün 0-13) sinyali gün 14: bölge henüz bilinmiyor, üçgen yok -> hedef NaN.
# Sıkışma eşiği 0,005. Gün 19 oranı 0,0071 (dönem değil), gün 20 oranı 0,0040 (dönem başlar), gün 33 oranı 0,0058 (biter):
# P2 gün 20-32; gün 33 kapanışı 99,4 > kutu üstü. "uzak": tepeler 97,6 ve 97,8, diplerin ilki 92 -> üçgen hedefi
# 97,8 + (97,6 - 92) = 103,4; arz proximal 100 daha yakın -> 100. "yakin": dip 95,5 -> 97,8 + (97,6 - 95,5) = 99,9 < 100 -> 99,9.
# "yok": üçgen yok -> yalnız arz bölgesi: 100. R/R kapısı rr_min 0 ile açık (hedef seçimi sınanıyor).
@pytest.mark.parametrize(
    "ucgen, kutu_alt, kutu_ust, hedef",
    [
        ("uzak", 92.0, 97.8, 100.0),
        ("yakin", 95.5, 97.8, 99.9),
        ("yok", 95.95, 97.0, 100.0),
    ],
)
def test_hedef_tansu_arz_bolgesi_ile_ucgen_hedefinden_yakin_olani_secer(
    ucgen, kutu_alt, kutu_ust, hedef
):
    f = _arz_ve_ucgen(ucgen)
    p = Parametre(hedef="tansu", stop="kutu", rr_min=0.0, **dict(KUCUK, esik=0.005))
    k = aileler.kurulum(f, p)
    assert list(k.index) == [f.index[14], f.index[33]]
    assert (k.iloc[0]["kutu_alt"], k.iloc[0]["kutu_ust"]) == (99.0, 101.0)
    assert np.isnan(k.iloc[0]["hedef"])
    assert (k.iloc[1]["kutu_alt"], k.iloc[1]["kutu_ust"]) == (kutu_alt, kutu_ust)
    assert k.iloc[1]["hedef"] == pytest.approx(hedef, abs=1e-9)


# 20 düz gün (kapanış 90, yüksek 91, düşük 89, hacim 100); kutu üstü 91. Gün 20 (kapanış 100) ve 21 (kapanış 105) hacim 100 < 2*100
# -> aday değil. Gün 21 yeşil, gün 22 yeşil değil (99 <= 105) -> arz bölgesi b = 21: proximal = önceki kapanış 100, distal 106.
# ATR20 = (26+11)/14 = 37/14; ATR21 = (37/14*13+6)/14 = 2,883; eşik = 100 - 2,883 = 97,12. Gün 22 (99) üstünde; gün 23 (96) altında
# -> bölge gün 23'te bilinir. Gün 22: hacim 250 >= 2*100 ve 99 > 91 -> aday. Gün 22'de bölge henüz bilinmiyor -> hedef yok,
# kapı uygulanmaz -> sinyal. (Bölge kullanılsaydı hedef 100 olurdu ve R/R = 1/10 < 2 sinyali engellerdi.)
def test_hedef_bilinen_gunden_once_arz_bolgesi_kullanilmaz():
    f = _mumlar(
        [90] * 20 + [100, 105, 99, 96],
        [91] * 20 + [101, 106, 100, 97],
        [89] * 20 + [90, 100, 98, 95],
        [100] * 20 + [100, 100, 250, 100],
    )
    p = Parametre(hedef="tansu", hacim_kat=2.0, stop="kutu", **dict(KUCUK, sma_n=5))
    k = aileler.kurulum(f, p)
    assert list(k.index) == [f.index[22]]
    assert np.isnan(k.iloc[0]["hedef"])
    z = aileler.bolgeler(f, "arz")
    assert (z.iloc[0]["bas"], z.iloc[0]["bilinen"]) == (f.index[21], f.index[23])


BOLGE_SUTUNLARI = ["bas", "bilinen", "proximal", "distal", "bitis", "temas", "teyit"]


# Düz 14 gün (100; 101; 99; ATR 2), sonra kapanış [104, 102, 99, 97, 101, 106], yüksek [105, 104, 102, 100, 102, 107],
# düşük [100, 101,5, 98,5, 96, 96,5, 100,5] (gün 14-19). Gün 14 yeşil, gün 15 yeşil değil -> b = 14.
# ATR14 = (26+5)/14 = 31/14 = 2,214; gövde altı = önceki kapanış 100; eşik 100 - 2,214 = 97,786.
# Gün 15 (102), 16 (99) üstünde; gün 17 (97) altında -> bilinen gün 17. Proximal 100, distal = yüksek_b = 105.
# Gün 18 kapanışı 101 <= 105; gün 19 kapanışı 106 > 105 -> bozulma, bitiş gün 19. Temas: gün 18 yüksek 102 >= 100 -> 1.
def test_arz_bolgesi_olusum_bilinen_gun_bozulma_ve_temas():
    f = _mumlar(
        [100] * 14 + [104, 102, 99, 97, 101, 106],
        [101] * 14 + [105, 104, 102, 100, 102, 107],
        [99] * 14 + [100, 101.5, 98.5, 96, 96.5, 100.5],
    )
    z = aileler.bolgeler(f, "arz")
    assert list(z.columns) == BOLGE_SUTUNLARI
    assert len(z) == 1
    r = z.iloc[0]
    assert (r["bas"], r["bilinen"], r["bitis"], r["teyit"]) == (
        f.index[14],
        f.index[17],
        f.index[19],
        f.index[17],
    )
    assert (r["proximal"], r["distal"], r["temas"]) == (100.0, 105.0, 1)
    # Gün 18'e kadar veri: bölge aktif (bitiş yok), temas 1. Gün 17'ye kadar: bilinen gün, temas 0.
    # Gün 16'ya kadar: bölge henüz bilinmiyor.
    aktif = aileler.bolgeler(f.iloc[:19], "arz")
    assert len(aktif) == 1 and pd.isna(aktif.iloc[0]["bitis"])
    assert aktif.iloc[0]["temas"] == 1
    assert aileler.bolgeler(f.iloc[:18], "arz").iloc[0]["temas"] == 0
    assert len(aileler.bolgeler(f.iloc[:17], "arz")) == 0


# Aynı düz 14 gün, sonra kapanış [96, 98, 101, 103, 99, 94], yüksek [100, 99, 102, 104, 101, 99,5],
# düşük [95, 96,5, 97,5, 100, 98, 93] (gün 14-19). Gün 14 kırmızı (96 < 100), gün 15 kırmızı değil (98 >= 96) -> b = 14.
# ATR14 = (26+5)/14 = 2,214; gövde üstü = önceki kapanış 100; eşik 100 + 2,214 = 102,214.
# Gün 15 (98), 16 (101) altında; gün 17 (103) üstünde -> bilinen gün 17. Proximal 100, distal = düşük_b = 95.
# Gün 18 kapanışı 99 >= 95; gün 19 kapanışı 94 < 95 -> bozulma, bitiş gün 19. Temas: gün 18 düşük 98 <= 100 -> 1.
def test_talep_bolgesi_olusum_bilinen_gun_bozulma_ve_temas():
    f = _mumlar(
        [100] * 14 + [96, 98, 101, 103, 99, 94],
        [101] * 14 + [100, 99, 102, 104, 101, 99.5],
        [99] * 14 + [95, 96.5, 97.5, 100, 98, 93],
    )
    z = aileler.bolgeler(f, "talep")
    assert list(z.columns) == BOLGE_SUTUNLARI
    assert len(z) == 1
    r = z.iloc[0]
    assert (r["bas"], r["bilinen"], r["bitis"], r["teyit"]) == (
        f.index[14],
        f.index[17],
        f.index[19],
        f.index[17],
    )
    assert (r["proximal"], r["distal"], r["temas"]) == (100.0, 95.0, 1)
    assert len(aileler.bolgeler(f.iloc[:17], "talep")) == 0


def test_varyantlar_18_ad_temelden_tek_boyut_degisir():
    temel = aileler.VARYANTLAR["tansu"]
    assert temel == Parametre(
        periyotlar=(20, 50, 100, 200),
        giris="mum",
        hacim_kat=2.0,
        momentum=True,
        teyit="yok",
        stop="kutu",
        hedef="tansu",
        rr_min=2.0,
        cikis="atr3",
    )
    assert aileler.VARYANTLAR["bugun"] == Parametre()
    tek = {
        "ema_5_8_13": ("periyotlar", (5, 8, 13)),
        "ema_50_100_200": ("periyotlar", (50, 100, 200)),
        "giris_kutu": ("giris", "kutu"),
        "giris_ema": ("giris", "ema"),
        "giris_retest": ("giris", "retest"),
        "giris_agresif": ("giris", "agresif"),
        "hacim_yok": ("hacim_kat", 0.0),
        "hacim_3": ("hacim_kat", 3.0),
        "momentum_kapali": ("momentum", False),
        "teyit_acik": ("teyit", "gosterge"),
        "teyit_trend": ("teyit", "trend"),
        "stop_atr15": ("stop", "atr15"),
        "stop_atr2": ("stop", "atr2"),
        "cikis_dip": ("cikis", "dip"),
        "cikis_rsi70": ("cikis", "rsi70"),
        "cikis_rsi50": ("cikis", "rsi50"),
    }
    assert set(aileler.VARYANTLAR) == {"bugun", "tansu", *tek}
    assert len(aileler.VARYANTLAR) == 18
    temel_alanlar = asdict(temel)
    for ad, (alan, deger) in tek.items():
        alanlar = asdict(aileler.VARYANTLAR[ad])
        assert {a for a in alanlar if alanlar[a] != temel_alanlar[a]} == {alan}, ad
        assert alanlar[alan] == deger, ad
