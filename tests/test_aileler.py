"""`aileler` yüzü: EMA sıkışması giriş sinyali (KURALLAR §3 madde 2). Beklenen değerler elle hesaplandı."""

import pandas as pd

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
