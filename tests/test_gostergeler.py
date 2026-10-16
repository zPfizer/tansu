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
    assert oran.tolist() == pytest.approx([0.0, 1 / 11, 0.0, 1 / 12], abs=1e-12)


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
    assert sonuc.iloc[2:].tolist() == pytest.approx([2.0, 3.0, 13 / 3], abs=1e-12)


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
    assert atr.iloc[2:].tolist() == pytest.approx([2.0, 7 / 3, 26 / 9], abs=1e-12)


def test_piyasa_durumu_kapanis_sma_ustunde_mi():
    # SMA(2): [nan, 1,5, 2,5, 2,5, 1,5]; 2 > 1,5 evet; 3 > 2,5 evet; 2 > 2,5 hayır; 1 > 1,5 hayır; ilk gün SMA yok -> hayır.
    from tansu.gostergeler import piyasa_durumu

    assert list(piyasa_durumu(pd.Series([1.0, 2.0, 3.0, 2.0, 1.0]), 2)) == [
        False,
        True,
        True,
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
    assert sonuc.iloc[3:].tolist() == pytest.approx([75.0, 600 / 11, 75.0], abs=1e-9)


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
    assert sonuc.iloc[4:].tolist() == pytest.approx([107 / 72, 11 / 72], abs=1e-9)


def test_macd_histogram_makd_eksi_sinyal():
    # hızlı 2 (alfa 2/3), yavaş 3 (alfa 1/2), sinyal 2 (alfa 2/3); kapanış [10; 12; 11; 13].
    # EMA2: 10; 34/3; 100/9; 334/27. EMA3: 10; 11; 11; 12. MACD: 0; 1/3; 1/9; 10/27.
    # Sinyal (MACD'nin EMA2'si): 0; 2/9; 4/27; 8/27. Histogram = MACD - sinyal: 0; 1/9; -1/27; 2/27.
    sonuc = gostergeler.macd_histogram(pd.Series([10.0, 12, 11, 13]), 2, 3, 2)
    assert sonuc.tolist() == pytest.approx([0.0, 1 / 9, -1 / 27, 2 / 27], abs=1e-9)


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
    assert k.iloc[2:].tolist() == pytest.approx([75.0, 100 / 3, 75.0], abs=1e-9)
    assert d.isna().tolist() == [True, True, True, False, False]
    assert d.iloc[3:].tolist() == pytest.approx([325 / 6, 325 / 6], abs=1e-9)
