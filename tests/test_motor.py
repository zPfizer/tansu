"""Adım/Motor yüzü: TASARIM 5.3'teki 14 motor durumu ve veri sonu / eksik gün, sentetik mumlarla.

Beklenen değerleri kodu görmemiş ayrı bir ajan yalnız kural metninden ve bu senaryo verisinden elle hesapladı
(bilet 08). Hesabın özeti her senaryonun yorumundadır. Adet = 1; boyutlandırma bilet 10'dadır.
Kural özeti: sinyal kapanışta, giriş ertesi gün AOF'ta; stop = giriş - 2 ATR; giriş günü yalnız stop;
dolum min(stop, AOF); kilitli tavanda giriş yok (sinyal düşer); kilitli tabanda çıkış kayar;
kapanış < SMA250 -> ertesi gün AOF'ta çıkış; veri bitince son kapanıştan çıkış.
Satır: (AOF, yüksek, düşük, kapanış, bayraklar). Beklenen: (giriş günü, giriş, çıkış günü, çıkış, neden,
planlanan risk, gerçekleşen kayıp).
"""

import pandas as pd
import pytest

from tansu import aileler, motor

GUNLER = pd.bdate_range("2026-03-02", periods=10)
STD = (100, 101, 99, 100)


def r(a, y, d, k, **bayrak):
    return dict(aof=a, yuksek=y, dusuk=d, kapanis=k, **bayrak)


EKSIK = dict(aof=None, yuksek=None, dusuk=None, kapanis=None, islem=False)

# ad: (sinyal günleri, ATR, satırlar, beklenen işlemler, düşen sinyal sayısı)
SENARYO = {
    # Stop 96. d2 düşük 97 > 96. d3 düşük 95 <= 96 -> dolum min(96, 97) = 96.
    "stopta_cikis": ([0], 2, [r(*STD), r(100, 102, 98.5, 101), r(99, 100, 97, 98), r(97, 98, 95, 96)],
                     [(1, 100, 3, 96, "stop", 4, 4)], 0),
    # d2 yüksek 95 < stop: boşluk. Dolum min(96, 93) = 93.
    "bosluklu_stop": ([0], 2, [r(*STD), r(*STD), r(93, 95, 92, 94)],
                      [(1, 100, 2, 93, "stop", 4, 7)], 0),
    # Giriş günü düşük 95 <= 96: aynı gün çıkış, min(96, 100) = 96.
    "giris_gunu_stop": ([0], 2, [r(*STD), r(100, 100.5, 95, 97)],
                        [(1, 100, 1, 96, "stop", 4, 4)], 0),
    # d1 kilitli tavan: sinyal düşer, d2'ye kaymaz.
    "kilitli_tavan_girisi": ([0], 2, [r(*STD), r(110, 110, 110, 110, kilit_tavan=True), r(109, 111, 108, 109)],
                             [], 1),
    # d2 kilitli taban, düşük 90 <= 96: çıkış kayar. d3 AOF 91 -> dolum 91.
    "kilitli_taban_cikisi": ([0], 2, [r(*STD), r(*STD), r(90, 90, 90, 90, kilit_taban=True), r(91, 92, 89, 90)],
                             [(1, 100, 3, 91, "stop", 4, 9)], 0),
    # d2 ve d3 kilitli taban: çıkış iki gün kayar; d4 düşük 83 <= 96 -> min(96, 84) = 84.
    "ardisik_kilit": ([0], 2, [r(*STD), r(*STD), r(90, 90, 90, 90, kilit_taban=True),
                               r(85, 85, 85, 85, kilit_taban=True), r(84, 86, 83, 85)],
                      [(1, 100, 4, 84, "stop", 4, 16)], 0),
    # d1 (giriş günü) kapanış 99 < SMA 100: bakılmaz. d2 100,5 >= 100. d3 98 < 100: bekleyen çıkış.
    # d4 AOF 97 (düşük 97 > 96) -> çıkış 97, sma250.
    "sma250_cikisi": ([0], 2, [r(*STD), r(100, 101, 99, 99, sma250=100), r(100, 101, 99, 100.5, sma250=100),
                               r(100, 100, 98, 98, sma250=100), r(97, 99, 97, 98)],
                      [(1, 100, 4, 97, "sma250", 4, 3)], 0),
    # d2 sinyali pozisyon açıkken; d3 sinyali bekleyen SMA çıkışı varken: ikisi de yok sayılır, düşen sayılmaz.
    "acik_pozisyonda_yeni_sinyal": ([0, 2, 3], 2, [r(*STD), r(*STD), r(*STD), r(100, 100, 98, 98, sma250=100),
                                                  r(97, 99, 97, 98), r(98, 99, 97, 98)],
                                    [(1, 100, 4, 97, "sma250", 4, 3)], 0),
    # Sinyal son günde: ertesi gün yok, işlem yok, düşer.
    "sinyalden_sonra_veri_yok": ([2], 2, [r(*STD), r(*STD), r(*STD)], [], 1),
    # Düşük = stop (96): dokunmuş sayılır, dolum min(96, 98) = 96.
    "stop_kenari_dusuk_esit": ([0], 2, [r(*STD), r(*STD), r(98, 99, 96, 98)],
                               [(1, 100, 2, 96, "stop", 4, 4)], 0),
    # Düşük 96,01 > 96: dokunmaz. Veri biter: son kapanış 98'den çıkış.
    "stop_kenari_dusuk_ustte": ([0], 2, [r(*STD), r(*STD), r(98, 99, 96.01, 98)],
                                [(1, 100, 2, 98, "veri_sonu", 4, 2)], 0),
    # Yüksek = stop (96), bütün gün stop altında: min(96, 95) = 95.
    "stop_kenari_yuksek_esit": ([0], 2, [r(*STD), r(*STD), r(95, 96, 94, 95)],
                                [(1, 100, 2, 95, "stop", 4, 5)], 0),
    # Lot yuvarlama (adet = 1, yalnız fiyat yolu): ATR 1,37 -> stop 52,35 - 2,74 = 49,61.
    # d2 düşük 49,6 <= 49,61 -> min(49,61; 50,0) = 49,61. Risk 2,74.
    "lot_yuvarlama_fiyat_yolu": ([0], 1.37, [r(50, 51, 49, 50), r(52.35, 53, 51.5, 52.5), r(50.0, 51, 49.6, 50.5)],
                                 [(1, 52.35, 2, 49.61, "stop", 2.74, 2.74)], 0),
    # %10 tavan (adet = 1): d2 kilitli tavan açık pozisyonu etkilemez. d3 kapanış 106 < SMA 108 -> d4 AOF 105.
    # Kâr: gerçekleşen kayıp 0.
    "yuzde10_tavan_fiyat_yolu": ([0], 2, [r(*STD), r(*STD), r(110, 110, 110, 110, kilit_tavan=True),
                                          r(110, 111, 105, 106, sma250=108), r(105, 107, 104, 105)],
                                 [(1, 100, 4, 105, "sma250", 4, 0)], 0),
    # Olay günü (d2): düzeltilmiş seri kesintisiz, ham düşüş mumda yok. Pozisyon sürer; d3 düşük 95,5 -> 96.
    "olay_gununde_acik_pozisyon": ([0], 2, [r(*STD), r(*STD), r(99, 100, 98, 99), r(97, 98, 95.5, 96)],
                                   [(1, 100, 3, 96, "stop", 4, 4)], 0),
    # d3 karantina: çıkış son temiz AOF'ta (d2: 101), çöp fiyatlar yok sayılır.
    "karantinada_acik_pozisyon": ([0], 2, [r(*STD), r(*STD), r(101, 102, 100, 101),
                                           r(500, 500, 1, 300, karantina=True)],
                                  [(1, 100, 3, 101, "karantina", 4, 0)], 0),
    # Giriş günü karantina: sinyal düşer.
    "karantinada_giris_gunu": ([0], 2, [r(*STD), r(500, 500, 1, 300, karantina=True), r(*STD)], [], 1),
    # Stop hiç dokunmaz, veri biter: son kapanış 103,5.
    "veri_sonu_cikisi": ([0], 2, [r(*STD), r(*STD), r(100, 103, 99, 102), r(103, 104, 101, 103.5)],
                         [(1, 100, 3, 103.5, "veri_sonu", 4, 0)], 0),
    # d2 eksik gün: açık pozisyon aynen taşınır. d3 düşük 94 -> min(96, 95) = 95.
    "eksik_gunde_acik_pozisyon": ([0], 2, [r(*STD), r(*STD), EKSIK, r(95, 96, 94, 95)],
                                  [(1, 100, 3, 95, "stop", 4, 5)], 0),
    # Giriş günü eksik: sinyal düşer, d2'ye kaymaz.
    "eksik_giris_gunu": ([0], 2, [r(*STD), EKSIK, r(*STD)], [], 1),
}


def _mumlar(satirlar, atr):
    df = pd.DataFrame(satirlar, index=GUNLER[: len(satirlar)])
    df["atr"] = float(atr)
    for ad, varsayilan in (("islem", True), ("karantina", False), ("kilit_tavan", False),
                           ("kilit_taban", False), ("sma250", 50.0)):
        df[ad] = varsayilan if ad not in df else df[ad].fillna(varsayilan).astype(type(varsayilan))
    return df


@pytest.mark.parametrize("ad", SENARYO)
def test_motor_senaryosu(ad):
    sinyaller, atr, satirlar, beklenen, iptal = SENARYO[ad]
    islemler, dusen = motor.islemler(_mumlar(satirlar, atr), GUNLER[sinyaller])
    gercek = [(GUNLER.get_loc(t.giris_tarih), t.giris_fiyat, GUNLER.get_loc(t.cikis_tarih), t.cikis_fiyat,
               t.neden, t.planlanan_risk, t.gerceklesen_kayip) for t in islemler.itertuples()]
    assert len(gercek) == len(beklenen)
    for g, b in zip(gercek, beklenen):
        assert g[:5] == (b[0], pytest.approx(b[1]), b[2], pytest.approx(b[3]), b[4])
        assert g[5:] == (pytest.approx(b[5]), pytest.approx(b[6]))
    assert dusen == iptal
    assert (islemler["adet"] == 1).all()


@pytest.mark.parametrize("ad", SENARYO)
def test_zincir_islemler_ile_ayni_tabloyu_verir(ad):
    # K1 zinciri (tek işlem önbelleği + açık/bekleyen pozisyon bloğu) gerçek motorla bire bir aynıdır.
    sinyaller, atr, satirlar, _, _ = SENARYO[ad]
    m = _mumlar(satirlar, atr)
    beklenen, beklenen_dusen = motor.islemler(m, GUNLER[sinyaller])
    z = motor.Zincir(m)
    for _ in range(2):  # ikinci çağrı önbellekten
        tablo, dusen = z.calistir(sinyaller)
        pd.testing.assert_frame_equal(tablo, beklenen, check_dtype=False)
        assert dusen == beklenen_dusen


def test_zincir_karantina_penceresindeki_sinyal_engelli_ve_ayni_gun_yeniden_giris():
    # d3 karantina: d5 sinyali engelli (işlem yok, düşen yok). Ayrı veri: d1 giriş, d2 stop (düşük 95 <= 96) ->
    # pozisyon d2'de kapanır; d2 sinyali aynı gün serbest, d3 girişi AOF 100 (d3 düşük 99 > stop 96) veri sonu d3 kapanış 100.
    karantinali = [r(*STD)] * 3 + [r(500, 500, 1, 300, karantina=True)] + [r(*STD)] * 3
    tablo, dusen = motor.Zincir(_mumlar(karantinali, 2)).calistir([5])
    assert (len(tablo), dusen) == (0, 0)
    tablo, dusen = motor.Zincir(_mumlar([r(*STD), r(*STD), r(97, 98, 95, 96), r(*STD)], 2)).calistir([0, 2])
    assert [(t.sinyal_tarih, t.giris_tarih, t.cikis_tarih, t.neden) for t in tablo.itertuples()] == [
        (GUNLER[0], GUNLER[1], GUNLER[2], "stop"), (GUNLER[2], GUNLER[3], GUNLER[3], "veri_sonu")]
    assert dusen == 0


def test_adim_saf_girdiyi_degistirmez():
    p = motor.bekleyen(atr=2.0)
    m = {"tarih": GUNLER[1], **r(100, 101, 99, 100), "islem": True, "karantina": False,
         "kilit_tavan": False, "kilit_taban": False, "sma250": 50.0}
    yeni = motor.adim(p, m)
    assert (p.durum, yeni.durum, yeni.giris_fiyat, yeni.stop) == ("bekliyor", "acik", 100, 96)
    assert motor.adim(p, m) == yeni


def test_karantinadan_sonraki_250_gunde_sinyal_yok():
    # Karantina günü d3'te. 250 gün içindeki d5 sinyali yok sayılır (TASARIM 5.1): işlem yok, düşen yok.
    satirlar = [r(*STD)] * 3 + [r(500, 500, 1, 300, karantina=True)] + [r(*STD)] * 3
    islemler, dusen = motor.islemler(_mumlar(satirlar, 2), GUNLER[[5]])
    assert (len(islemler), dusen) == (0, 0)


def test_sinama_anlik_goruntuden_sinyal_ve_islem():
    # Elle hesap (bilet 08, ajan değil): kapanış [100x5, 103, 104, 105], AOF = kapanış, yüksek/düşük = kapanış ± 0,5
    # (yüksek gün 2: 101). Küçük parametre: periyotlar (1, 2), eşik 0,005, 3 gün, pencere 3, ısınma 4, SMA(2), ATR(2).
    # Sinyal gün 5 (bkz. test_aileler). ATR(2): TR = [1; 1; 1,5; 1; 1; 3,5] (gün 5: |103,5-100| = 3,5);
    # ATR gün 1 = 1; gün 2 = 1,25; gün 3 = 1,125; gün 4 = 1,0625; gün 5 = (1,0625+3,5)/2 = 2,28125.
    # Giriş gün 6 AOF 104; stop = 104 - 2*2,28125 = 99,4375; risk 4,5625. Stop dokunmaz (düşük 103,5 ve 104,5);
    # gün 7 kapanış 105 >= SMA(2) 104,5. Veri biter: çıkış gün 7 kapanış 105, kayıp 0.
    from tansu.veri import Anlik
    kap = [100.0] * 5 + [103.0, 104.0, 105.0]
    yuk = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5]
    f = pd.DataFrame({"sembol": "XXXX", "tarih": GUNLER[:8], "yuksek": yuk, "dusuk": [k - 0.5 for k in kap],
                      "kapanis": kap, "aof": kap, "hacim": 1e6})
    for s in ("kapanis", "aof", "yuksek", "dusuk"):
        f["ham_" + s] = f[s]
    anlik = Anlik("t", f, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"]))
    p = aileler.Parametre(periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=4, sma_n=2)
    islemler, dusen = motor.sinama(anlik, p, atr_n=2)
    assert dusen == 0 and len(islemler) == 1
    t = islemler.iloc[0]
    assert (t.sembol, t.sinyal_tarih, t.giris_tarih, t.cikis_tarih, t.neden) == (
        "XXXX", GUNLER[5], GUNLER[6], GUNLER[7], "veri_sonu")
    assert (t.giris_fiyat, t.cikis_fiyat, t.gerceklesen_kayip) == (104.0, 105.0, 0.0)
    assert t.planlanan_risk == pytest.approx(4.5625, abs=1e-9)


def test_sinama_evren_disi_sinyal_pozisyon_acmaz_sonraki_gecerli_sinyal_gecikmez(monkeypatch):
    # Bilet 11 düzeltmesi (TASARIM 5.6 evren süzgeci). Aynı seri; iki sinyal: 28.01 (üye değil) ve 02.02 (üye).
    # Süzgeçsiz motor 28.01 sinyaliyle 29.01'de pozisyon açar (stop 100 - 2*1,25 = 97,5 dokunmaz) ve 02.02 sinyali
    # açık pozisyon yüzünden düşerdi. Süzgeçle yalnız 02.02 sinyali kalır: giriş 03.02 AOF 104, çıkış 04.02 veri sonu 105.
    from tansu.veri import Anlik
    gun = pd.bdate_range("2026-01-26", periods=8)
    kap = [100.0] * 5 + [103.0, 104.0, 105.0]
    f = pd.DataFrame({"sembol": "XXXX", "tarih": gun, "yuksek": [k + 0.5 for k in kap], "dusuk": [k - 0.5 for k in kap],
                      "kapanis": kap, "aof": kap, "hacim": 1e6})
    for s in ("kapanis", "aof", "yuksek", "dusuk"):
        f["ham_" + s] = f[s]
    anlik = Anlik("t", f, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"]))
    monkeypatch.setattr(aileler, "sinyal", lambda m, p: pd.DatetimeIndex([gun[2], gun[5]]))
    uye = pd.DataFrame({"sembol": "XXXX", "tarih": gun[5:]})
    islemler, dusen = motor.sinama(anlik, aileler.Parametre(sma_n=2), atr_n=2, uye=uye)
    assert dusen == 0 and len(islemler) == 1
    t = islemler.iloc[0]
    assert (t.sinyal_tarih, t.giris_tarih, t.giris_fiyat, t.cikis_tarih, t.cikis_fiyat) == (
        gun[5], gun[6], 104.0, gun[7], 105.0)
