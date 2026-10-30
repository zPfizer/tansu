"""`gostergeler` yüzü: EMA, sıkışma oranı, sıkışma dönemleri. Beklenen değerler elle hesaplandı."""

import pandas as pd
import pytest

from tansu import gostergeler


def test_ema_adjust_false():
    # span=3 -> alfa=2/(3+1)=0,5. e0=10; e1=0,5*12+0,5*10=11; e2=0,5*11+0,5*11=11; e3=0,5*13+0,5*11=12.
    sonuc = gostergeler.ema(pd.Series([10.0, 12.0, 11.0, 13.0]), 3)
    assert sonuc.tolist() == pytest.approx([10.0, 11.0, 11.0, 12.0], abs=1e-12)


def test_sikisma_orani_en_buyuk_eksi_en_kucuk_bolu_en_yavas_ema():
    # Periyot 1 = kapanışın kendisi; periyot 3 EMA'sı yukarıdaki gibi [10; 11; 11; 12].
    # Oran = (en büyük - en küçük) / EMA3: gün0 0/10=0; gün1 (12-11)/11; gün2 0/11=0; gün3 (13-12)/12.
    oran = gostergeler.sikisma_orani(
        pd.Series([10.0, 12.0, 11.0, 13.0]), periyotlar=(1, 3)
    )
    # 1/11 = 0.09090909090909091; 1/12 = 0.08333333333333333
    assert oran.tolist() == pytest.approx(
        [0.0, 0.09090909090909091, 0.0, 0.08333333333333333], abs=1e-12
    )


def test_sikisma_donemleri_en_az_3_gun_ve_esik_dahil():
    # Eşik 0,012 (dahil). İndeks 1-3: 0,010; 0,011; 0,012 -> 3 gün, dönem. İndeks 4 (0,013) dönemi bitirir.
    # İndeks 5-6: yalnız 2 gün -> dönem değil. Dönem ortalaması (0,010+0,011+0,012)/3 = 0,011.
    oran = pd.Series(
        [0.05, 0.010, 0.011, 0.012, 0.013, 0.010, 0.010, 0.2],
        index=pd.bdate_range("2026-01-05", periods=8),
    )
    donemler = gostergeler.sikisma_donemleri(oran)
    assert len(donemler) == 1
    d = donemler[0]
    assert (d["bas"], d["bit"], d["gun"]) == (
        pd.Timestamp("2026-01-06"),
        pd.Timestamp("2026-01-08"),
        3,
    )
    assert d["ortalama"] == pytest.approx(0.011, abs=1e-12)


def test_sma_hareketli_ortalama():
    # n=3, [1; 2; 3; 4; 6]: ilk iki değer NaN; (1+2+3)/3=2; (2+3+4)/3=3; (3+4+6)/3=13/3.
    sonuc = gostergeler.sma(pd.Series([1.0, 2.0, 3.0, 4.0, 6.0]), 3)
    assert sonuc.isna().tolist() == [True, True, False, False, False]
    # 13 / 3 = 4.333333333333333
    assert sonuc.iloc[2:].tolist() == pytest.approx(
        [2.0, 3.0, 4.333333333333333], abs=1e-12
    )


def test_wma_agirliklar_bir_den_n_ye_en_yeni_en_agir():
    sonuc = gostergeler.wma(pd.Series([1.0, 2.0, 3.0, 4.0, 6.0]), 3)
    assert sonuc.isna().tolist() == [True, True, False, False, False]
    assert sonuc.iloc[2:].tolist() == pytest.approx([14 / 6, 20 / 6, 29 / 6], abs=1e-12)


def test_wma_nan_iceren_pencere_nan_ve_kisa_seri_hep_nan():
    sonuc = gostergeler.wma(pd.Series([1.0, 2.0, float("nan"), 4.0, 6.0, 8.0]), 3)
    assert sonuc.isna().tolist() == [True] * 5 + [False]
    assert sonuc.iloc[5] == pytest.approx(40 / 6, abs=1e-12)
    assert gostergeler.wma(pd.Series([1.0, 2.0]), 3).isna().all()


def test_atr_wilder_ilk_deger_ilk_n_tr_ortalamasi():
    # n=3. yüksek [12;13;14;12;15], düşük [10;11;12;10;11], kapanış [11;12;13;11;14].
    # TR0 = 12-10 = 2 (önceki kapanış yok). TR1 = max(2; |13-11|; |11-11|) = 2.
    # TR2 = max(2; |14-12|; |12-12|) = 2. TR3 = max(2; |12-13|=1; |10-13|=3) = 3.
    # TR4 = max(4; |15-11|=4; |11-11|=0) = 4.
    # ATR2 = (2+2+2)/3 = 2 (ilk değer). ATR3 = (2*2+3)/3 = 7/3. ATR4 = (7/3*2+4)/3 = 26/9.
    atr = gostergeler.atr(
        pd.Series([12.0, 13, 14, 12, 15]),
        pd.Series([10.0, 11, 12, 10, 11]),
        pd.Series([11.0, 12, 13, 11, 14]),
        3,
    )
    assert atr.isna().tolist() == [True, True, False, False, False]
    # 7 / 3 = 2.3333333333333335; 26 / 9 = 2.888888888888889
    assert atr.iloc[2:].tolist() == pytest.approx(
        [2.0, 2.3333333333333335, 2.888888888888889], abs=1e-12
    )


def test_atr_bas_nan_satirlar_tohum_n_1_konumunda_nan_atlanarak():
    # n=3, ilk iki satır NaN. Gerçek aralıklar: NaN; NaN; 4; 2; 6; 3.
    # Gün 2: yüksek 14, düşük 10 (önceki kapanış yok) -> 4. Gün 3: yüksek 13, düşük 11, önceki kapanış 12 -> 2.
    # Gün 4: yüksek 15, düşük 9 -> 6. Gün 5: yüksek 13,5, düşük 10,5 -> 3.
    # Tohum konum n-1 = 2: ilk üç gerçek aralığın ortalaması, NaN atlanır = 4. ATR3 = (4*2+2)/3 = 10/3.
    # ATR4 = (10/3*2+6)/3 = 38/9. ATR5 = (38/9*2+3)/3 = 103/27.
    nan = float("nan")
    atr = gostergeler.atr(
        pd.Series([nan, nan, 14.0, 13, 15, 13.5]),
        pd.Series([nan, nan, 10.0, 11, 9, 10.5]),
        pd.Series([nan, nan, 12.0, 12, 12, 12]),
        3,
    )
    assert atr.isna().tolist() == [True, True, False, False, False, False]
    # 10 / 3 = 3.3333333333333335; 38 / 9 = 4.222222222222222; 103 / 27 = 3.814814814814815
    assert atr.iloc[2:].tolist() == pytest.approx(
        [4.0, 3.3333333333333335, 4.222222222222222, 3.814814814814815]
    )


def test_piyasa_durumu_kapanis_sma_ustunde_mi():
    # SMA(2): [nan, 1,5, 2,5, 2,5, 1,5]; 2 > 1,5 evet; 3 > 2,5 evet; 2 > 2,5 hayır; 1 > 1,5 hayır; ilk gün SMA yok -> hayır.
    assert list(gostergeler.piyasa_durumu(pd.Series([1.0, 2.0, 3.0, 2.0, 1.0]), 2)) == [
        False,
        True,
        True,
        False,
        False,
    ]


def test_piyasa_durumu_sma_esitliginde_olumlu_degil():
    # TASARIM 6.3: sabit 100 serisinde dolu SMA da 100; eşitlik olumlu piyasa değildir.
    assert gostergeler.piyasa_durumu(pd.Series([100.0] * 3), 2).tolist() == [
        False,
        False,
        False,
    ]


def test_rsi_wilder_ilk_deger_ilk_n_degisimin_ortalamasi():
    # n=3, kapanış [10; 11; 10; 12; 11; 13]. Değişimler: +1; -1; +2; -1; +2.
    # İlk üç değişim (+1; -1; +2): kazanç ortalaması (1+0+2)/3 = 1; kayıp ortalaması (0+1+0)/3 = 1/3.
    # RSI3 = 100 * 1 / (1 + 1/3) = 75.
    # Gün 4 (değişim -1): kazanç (1*2+0)/3 = 2/3; kayıp (1/3*2+1)/3 = 5/9; RSI = 100 * (6/9) / (6/9 + 5/9) = 600/11.
    # Gün 5 (değişim +2): kazanç (2/3*2+2)/3 = 10/9; kayıp (5/9*2)/3 = 10/27; RSI = 100 * (30/27) / (40/27) = 75.
    sonuc = gostergeler.rsi(pd.Series([10.0, 11, 10, 12, 11, 13]), 3)
    assert sonuc.isna().tolist() == [True, True, True, False, False, False]
    # 600 / 11 = 54.54545454545455
    assert sonuc.iloc[3:].tolist() == pytest.approx(
        [75.0, 54.54545454545455, 75.0], abs=1e-9
    )


def test_momentum_squeeze_linreg_son_nokta():
    # n=3. yüksek [11;12;13;14;16;17], düşük [9;10;11;12;13;15], kapanış [10;11;12;13;15;14].
    # Gün 2: en yüksek 13, en düşük 9 -> ort 11; SMA3 = 11; orta = 11; kaynak = 12-11 = 1.
    # Gün 3: en yüksek 14, en düşük 10 -> 12; SMA3 = 12; orta = 12; kaynak = 13-12 = 1.
    # Gün 4: en yüksek 16, en düşük 11 -> 13,5; SMA3 = 40/3; orta = (13,5+40/3)/2 = 161/12; kaynak = 15-161/12 = 19/12.
    # Gün 5: en yüksek 17, en düşük 12 -> 14,5; SMA3 = 14; orta = 14,25; kaynak = 14-14,25 = -1/4.
    # Gün 4 değeri: kaynak [1; 1; 19/12], x = 0,1,2. Eğim = (y2-y0)/2 = 7/24; ortalama = 43/36;
    #   son noktadaki doğru değeri = 43/36 + 7/24 = 107/72.
    # Gün 5 değeri: kaynak [1; 19/12; -1/4]. Eğim = (-1/4-1)/2 = -5/8; ortalama = 7/9; değer = 7/9 - 5/8 = 11/72.
    sonuc = gostergeler.momentum_squeeze(
        pd.Series([11.0, 12, 13, 14, 16, 17]),
        pd.Series([9.0, 10, 11, 12, 13, 15]),
        pd.Series([10.0, 11, 12, 13, 15, 14]),
        3,
    )
    assert sonuc.isna().tolist() == [True, True, True, True, False, False]
    # 107 / 72 = 1.4861111111111112; 11 / 72 = 0.1527777777777778
    assert sonuc.iloc[4:].tolist() == pytest.approx(
        [1.4861111111111112, 0.1527777777777778], abs=1e-9
    )


def test_macd_histogram_makd_eksi_sinyal():
    # hızlı 2 (alfa 2/3), yavaş 3 (alfa 1/2), sinyal 2 (alfa 2/3); kapanış [10; 12; 11; 13].
    # EMA2: 10; 34/3; 100/9; 334/27. EMA3: 10; 11; 11; 12. MACD: 0; 1/3; 1/9; 10/27.
    # Sinyal (MACD'nin EMA2'si): 0; 2/9; 4/27; 8/27. Histogram = MACD - sinyal: 0; 1/9; -1/27; 2/27.
    sonuc = gostergeler.macd_histogram(pd.Series([10.0, 12, 11, 13]), 2, 3, 2)
    # 1 / 9 = 0.1111111111111111; -1 / 27 = -0.037037037037037035; 2 / 27 = 0.07407407407407407
    assert sonuc.tolist() == pytest.approx(
        [0.0, 0.1111111111111111, -0.037037037037037035, 0.07407407407407407],
        abs=1e-9,
    )


def test_psar_wilder_yukselen_trend_sonra_donus():
    # adım 0,02; tavan 0,2. yüksek [10;11;12;13;12;10,5;10], düşük [9;10;11;12;10,5;9,5;9].
    # Gün 0: SAR = düşük = 9, yükselen, EP = 10, AF = 0,02.
    # Gün 1: 9+0,02*(10-9) = 9,02; önceki düşükten (9) yüksek olamaz -> 9. Yeni tepe 11: EP 11, AF 0,04.
    # Gün 2: 9+0,04*(11-9) = 9,08; en düşük iki önceki düşük 9 -> 9. EP 12, AF 0,06.
    # Gün 3: 9+0,06*(12-9) = 9,18 (düşükler 11 ve 10 üstünde değil). EP 13, AF 0,08.
    # Gün 4: 9,18+0,08*(13-9,18) = 9,4856. Yeni tepe yok.
    # Gün 5: 9,4856+0,08*(13-9,4856) = 9,766752; düşük 9,5 < 9,766752 -> dönüş: SAR = EP = 13, EP = 9,5, AF = 0,02.
    # Gün 6: düşen trend: 13+0,02*(9,5-13) = 12,93; üst sınırlar 10,5 ve 12 altında -> 12,93. Düşük 9 < EP: EP 9.
    sonuc = gostergeler.psar(
        pd.Series([10.0, 11, 12, 13, 12, 10.5, 10]),
        pd.Series([9.0, 10, 11, 12, 10.5, 9.5, 9]),
    )
    assert sonuc.tolist() == pytest.approx(
        [9.0, 9.0, 9.0, 9.18, 9.4856, 13.0, 12.93], abs=1e-9
    )


def test_stokastik_k_ve_d():
    # n=3, d=2. yüksek [12;13;14;13;15], düşük [10;11;12;11;12], kapanış [11;12;13;12;14].
    # Gün 2: en yüksek 14, en düşük 10 -> %K = 100*(13-10)/(14-10) = 75.
    # Gün 3: en yüksek 14, en düşük 11 -> %K = 100*(12-11)/(14-11) = 100/3.
    # Gün 4: en yüksek 15, en düşük 11 -> %K = 100*(14-11)/(15-11) = 75.
    # %D = %K'nın SMA2'si: gün 3 (75+100/3)/2 = 325/6; gün 4 (100/3+75)/2 = 325/6.
    k, d = gostergeler.stokastik(
        pd.Series([12.0, 13, 14, 13, 15]),
        pd.Series([10.0, 11, 12, 11, 12]),
        pd.Series([11.0, 12, 13, 12, 14]),
        3,
        2,
    )
    assert k.isna().tolist() == [True, True, False, False, False]
    # 100 / 3 = 33.333333333333336
    assert k.iloc[2:].tolist() == pytest.approx(
        [75.0, 33.333333333333336, 75.0], abs=1e-9
    )
    assert d.isna().tolist() == [True, True, True, False, False]
    # 325 / 6 = 54.166666666666664
    assert d.iloc[3:].tolist() == pytest.approx(
        [54.166666666666664, 54.166666666666664], abs=1e-9
    )


def test_adx_wilder_dm_tr_yumusatma_dx_ve_ilk_adx():
    # n=2 (Wilder ortalaması: ilk değer ilk 2 değerin ortalaması, sonra (önceki*1 + yeni)/2).
    # yüksek [10;11;12;11,5;12;13], düşük [8;9;9,5;9;9,5;11], kapanış [9;10;11;10;11,5;12,5].
    # Gün 1..5 için yukarı = yüksek_t - yüksek_{t-1}, aşağı = düşük_{t-1} - düşük_t; +DM = yukarı (yukarı > aşağı ve > 0), -DM = aşağı (aşağı > yukarı ve > 0):
    #   gün 1: yukarı 1, aşağı -1 -> +DM 1, -DM 0.   gün 2: yukarı 1, aşağı -0,5 -> +DM 1, -DM 0.
    #   gün 3: yukarı -0,5, aşağı 0,5 -> +DM 0, -DM 0,5.   gün 4: yukarı 0,5, aşağı -0,5 -> +DM 0,5, -DM 0.
    #   gün 5: yukarı 1, aşağı -1,5 -> +DM 1, -DM 0.
    # Gerçek aralık = max(yüksek-düşük, |yüksek-önceki kapanış|, |düşük-önceki kapanış|): gün 1..5 = 2; 2,5; 2,5; 2,5; 2.
    # Wilder (gün 2'de tohum = gün 1 ve 2 ortalaması): +DM 1; 0,5; 0,5; 0,75. -DM 0; 0,25; 0,125; 0,0625.
    #   TR 2,25; 2,375; 2,4375; 2,21875 (gün 2, 3, 4, 5).
    # +DI = 100*+DM/TR: 44,444; 21,053; 20,513; 33,803. -DI: 0; 10,526; 5,128; 2,817.
    # DX = 100*|+DI - -DI|/(+DI + -DI): gün 2 = 100; gün 3 = 100*0,25/0,75 = 100/3; gün 4 = 100*0,375/0,625 = 60;
    #   gün 5 = 100*0,6875/0,8125 = 1100/13.
    # ADX: tohum gün 3 = (100 + 100/3)/2 = 200/3; gün 4 = (200/3 + 60)/2 = 190/3; gün 5 = (190/3 + 1100/13)/2 = 2885/39.
    sonuc = gostergeler.adx(
        pd.Series([10.0, 11, 12, 11.5, 12, 13]),
        pd.Series([8.0, 9, 9.5, 9, 9.5, 11]),
        pd.Series([9.0, 10, 11, 10, 11.5, 12.5]),
        2,
    )
    assert sonuc.isna().tolist() == [True, True, True, False, False, False]
    # 200 / 3 = 66.66666666666667; 190 / 3 = 63.333333333333336; 2885 / 39 = 73.97435897435898
    assert sonuc.iloc[3:].tolist() == pytest.approx(
        [66.66666666666667, 63.333333333333336, 73.97435897435898], abs=1e-9
    )


# KURALLAR §3 "Modül 1" gösterge teyidi: +DI + −DI = 0 ise DX = 0 (yönlü hareket yok; ATR = 0 dahil; YORUM, TA-Lib kuralı).
# n=2. 1) Düz hisse (yüksek = düşük = kapanış = 10, 6 gün): her +DM, −DM ve gerçek aralık 0; DX gün 2'den 0; ilk ADX gün 3 = 0.
# 2) Önce düz, sonra yukarı: yüksek [10;10;10;11;11], düşük 10, kapanış [10;10;10;10,5;10,5].
#   Gün 1, 2: yukarı 0, aşağı 0 -> +DM 0, -DM 0; gerçek aralık 0. Gün 3: yukarı 1, aşağı 0 -> +DM 1; gerçek aralık
#   max(1; |11-10|; |10-10|) = 1. Gün 4: yukarı 0, aşağı 0 -> +DM 0; gerçek aralık max(1; 0,5; 0,5) = 1.
#   Wilder (tohum gün 2 = gün 1 ve 2 ortalaması): +DM 0; 0,5; 0,25. TR 0; 0,5; 0,75. -DM hep 0.
#   DX gün 2: +DI + -DI = 0 -> 0. Gün 3: +DI 100, -DI 0 -> 100. Gün 4: +DI 100*0,25/0,75 = 100/3, -DI 0 -> 100.
#   ADX: tohum gün 3 = (0 + 100)/2 = 50; gün 4 = (50 + 100)/2 = 75.
@pytest.mark.parametrize(
    "yuksek, kapanis, beklenen",
    [
        ([10.0] * 6, [10.0] * 6, [None, None, None, 0.0, 0.0, 0.0]),
        (
            [10.0, 10, 10, 11, 11],
            [10.0, 10, 10, 10.5, 10.5],
            [None, None, None, 50.0, 75.0],
        ),
    ],
    ids=["duz-hisse", "once-duz-sonra-yukari"],
)
def test_adx_yonlu_hareket_yoksa_dx_sifir_atr_sifir_dahil(yuksek, kapanis, beklenen):
    sonuc = gostergeler.adx(
        pd.Series(yuksek), pd.Series([10.0] * len(yuksek)), pd.Series(kapanis), 2
    )
    assert sonuc.isna().tolist() == [x is None for x in beklenen]
    assert sonuc.dropna().tolist() == pytest.approx(
        [x for x in beklenen if x is not None], abs=1e-9
    )


# KURALLAR §3 "Modül 1" gösterge teyidi: DX = 100 × |+DI − −DI| / (+DI + −DI); −DI > +DI olan günde DX pozitiftir (mutlak değer).
# n=2. yüksek [10;9;8;7;8], düşük [8;7;6;5;6], kapanış [9;8;7;6;7].
#   Gün 1, 2, 3: yukarı -1, aşağı 1 -> +DM 0, -DM 1; gerçek aralık = max(2; |yüksek - önceki kapanış|; |düşük - önceki kapanış|) = max(2; 0; 2) = 2.
#   Gün 4: yukarı 1, aşağı -1 -> +DM 1, -DM 0; gerçek aralık max(2; |8-6| = 2; |6-6| = 0) = 2.
#   Wilder (tohum gün 2 = gün 1 ve 2 ortalaması): +DM 0; 0; 0,5 (gün 2, 3, 4). -DM 1; 1; 0,5. TR 2; 2; 2.
#   +DI = 100*+DM/TR: 0; 0; 25. -DI: 50; 50; 25.
#   DX: gün 2 = 100*50/50 = 100; gün 3 = 100; gün 4 = 100*0/50 = 0.
#   ADX: tohum gün 3 = (100 + 100)/2 = 100; gün 4 = (100 + 0)/2 = 50. Mutlak değer yoksa DX gün 2, 3 = -100 olur (ADX -100).
def test_adx_eksi_di_arti_di_den_buyukse_dx_mutlak_degerdir():
    sonuc = gostergeler.adx(
        pd.Series([10.0, 9, 8, 7, 8]),
        pd.Series([8.0, 7, 6, 5, 6]),
        pd.Series([9.0, 8, 7, 6, 7]),
        2,
    )
    assert sonuc.isna().tolist() == [True, True, True, False, False]
    assert sonuc.iloc[3:].tolist() == pytest.approx([100.0, 50.0], abs=1e-9)


def test_atr_basit_gercek_araligin_basit_ortalamasi():
    # TR: 2 (ilk gün y-d), sonra max(y-d, |y-k_1|, |d-k_1|) = 3, 4 → 3 günlük ortalama 3.
    y = pd.Series([12.0, 14.0, 16.0])
    d = pd.Series([10.0, 11.0, 12.0])
    k = pd.Series([11.0, 13.0, 15.0])
    a = gostergeler.atr_basit(y, d, k, n=3)
    assert a.iloc[:2].isna().all()
    assert a.iloc[-1] == pytest.approx(3.0)


def test_atr_basit_eksik_gunu_atlar_sonraki_gunler_tanimli_kalir():
    # Tek eksik gün eskiden n gün NaN veriyordu; ATR işlem görülen n çubuğun ortalamasıdır.
    nan = float("nan")
    y = pd.Series([12.0, 14.0, nan, 16.0, 17.0])
    d = pd.Series([10.0, 11.0, nan, 12.0, 15.0])
    k = pd.Series([11.0, 13.0, nan, 15.0, 16.0])
    a = gostergeler.atr_basit(y, d, k, n=3)
    assert a.isna().tolist() == [True, True, True, False, False]
    assert a.iloc[3] == pytest.approx(3.0)  # eksik gün yokmuş gibi: 2, 3, 4
    assert a.iloc[4] == pytest.approx((3.0 + 4.0 + 2.0) / 3)
