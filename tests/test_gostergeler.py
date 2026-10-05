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
    oran = gostergeler.sikisma_orani(pd.Series([10.0, 12.0, 11.0, 13.0]), periyotlar=(1, 3))
    assert oran.tolist() == pytest.approx([0.0, 1 / 11, 0.0, 1 / 12], abs=1e-12)


def test_sikisma_donemleri_en_az_3_gun_ve_esik_dahil():
    # Eşik 0,012 (dahil). İndeks 1-3: 0,010; 0,011; 0,012 -> 3 gün, dönem. İndeks 4 (0,013) dönemi bitirir.
    # İndeks 5-6: yalnız 2 gün -> dönem değil. Dönem ortalaması (0,010+0,011+0,012)/3 = 0,011.
    oran = pd.Series([0.05, 0.010, 0.011, 0.012, 0.013, 0.010, 0.010, 0.2],
                     index=pd.bdate_range("2026-01-05", periods=8))
    donemler = gostergeler.sikisma_donemleri(oran)
    assert len(donemler) == 1
    d = donemler[0]
    assert (d["bas"], d["bit"], d["gun"]) == (pd.Timestamp("2026-01-06"), pd.Timestamp("2026-01-08"), 3)
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
    atr = gostergeler.atr(pd.Series([12.0, 13, 14, 12, 15]), pd.Series([10.0, 11, 12, 10, 11]),
                          pd.Series([11.0, 12, 13, 11, 14]), 3)
    assert atr.isna().tolist() == [True, True, False, False, False]
    assert atr.iloc[2:].tolist() == pytest.approx([2.0, 7 / 3, 26 / 9], abs=1e-12)
