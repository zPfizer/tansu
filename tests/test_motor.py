"""Adım/Motor yüzü: TASARIM 5.3'teki 14 motor durumu ve veri sonu / eksik gün, sentetik mumlarla.

Beklenen değerleri kodu görmemiş ayrı bir ajan yalnız kural metninden ve bu senaryo verisinden elle hesapladı
(bilet 08). Hesabın özeti her senaryonun yorumundadır. Adet = 1; boyutlandırma bilet 10'dadır.
Kural özeti: sinyal kapanışta, giriş ertesi gün AOF'ta; stop = giriş - 2 ATR; giriş günü yalnız stop;
dolum min(stop, AOF); kilitli tavanda giriş yok (sinyal düşer); kilitli tabanda çıkış kayar;
kapanış < SMA250 -> ertesi gün AOF'ta çıkış; veri bitince son kapanıştan çıkış.
Satır: (AOF, yüksek, düşük, kapanış, bayraklar). Beklenen: (giriş günü, giriş, çıkış günü, çıkış, neden,
planlanan risk, gerçekleşen kayıp).
"""

from dataclasses import replace

import pandas as pd
import pytest

from tansu import aileler, gostergeler, motor, veri

GUNLER = pd.bdate_range("2026-03-02", periods=10)
STD = (100, 101, 99, 100)


def r(a, y, d, k, **bayrak):
    return dict(aof=a, yuksek=y, dusuk=d, kapanis=k, **bayrak)


EKSIK = dict(aof=None, yuksek=None, dusuk=None, kapanis=None, islem=False)

# ad: (sinyal günleri, ATR, satırlar, beklenen işlemler, düşen sinyal sayısı)
SENARYO = {
    # Stop 96. d2 düşük 97 > 96. d3 düşük 95 <= 96 -> dolum min(96, 97) = 96.
    "stopta_cikis": (
        [0],
        2,
        [r(*STD), r(100, 102, 98.5, 101), r(99, 100, 97, 98), r(97, 98, 95, 96)],
        [(1, 100, 3, 96, "stop", 4, 4)],
        0,
    ),
    # d2 yüksek 95 < stop: boşluk. Dolum min(96, 93) = 93.
    "bosluklu_stop": (
        [0],
        2,
        [r(*STD), r(*STD), r(93, 95, 92, 94)],
        [(1, 100, 2, 93, "stop", 4, 7)],
        0,
    ),
    # Giriş günü düşük 95 <= 96: aynı gün çıkış, min(96, 100) = 96.
    "giris_gunu_stop": (
        [0],
        2,
        [r(*STD), r(100, 100.5, 95, 97)],
        [(1, 100, 1, 96, "stop", 4, 4)],
        0,
    ),
    # d1 kilitli tavan: sinyal düşer, d2'ye kaymaz.
    "kilitli_tavan_girisi": (
        [0],
        2,
        [r(*STD), r(110, 110, 110, 110, kilit_tavan=True), r(109, 111, 108, 109)],
        [],
        1,
    ),
    # d2 kilitli taban, düşük 90 <= 96: çıkış kayar. d3 AOF 91 -> dolum 91.
    "kilitli_taban_cikisi": (
        [0],
        2,
        [r(*STD), r(*STD), r(90, 90, 90, 90, kilit_taban=True), r(91, 92, 89, 90)],
        [(1, 100, 3, 91, "stop", 4, 9)],
        0,
    ),
    # d2 ve d3 kilitli taban: çıkış iki gün kayar; d4 düşük 83 <= 96 -> min(96, 84) = 84.
    "ardisik_kilit": (
        [0],
        2,
        [
            r(*STD),
            r(*STD),
            r(90, 90, 90, 90, kilit_taban=True),
            r(85, 85, 85, 85, kilit_taban=True),
            r(84, 86, 83, 85),
        ],
        [(1, 100, 4, 84, "stop", 4, 16)],
        0,
    ),
    # d1 (giriş günü) kapanış 99 < SMA 100: bakılmaz. d2 100,5 >= 100. d3 98 < 100: bekleyen çıkış.
    # d4 AOF 97 (düşük 97 > 96) -> çıkış 97, sma250.
    "sma250_cikisi": (
        [0],
        2,
        [
            r(*STD),
            r(100, 101, 99, 99, sma250=100),
            r(100, 101, 99, 100.5, sma250=100),
            r(100, 100, 98, 98, sma250=100),
            r(97, 99, 97, 98),
        ],
        [(1, 100, 4, 97, "sma250", 4, 3)],
        0,
    ),
    # d2 sinyali pozisyon açıkken; d3 sinyali bekleyen SMA çıkışı varken: ikisi de yok sayılır, düşen sayılmaz.
    "acik_pozisyonda_yeni_sinyal": (
        [0, 2, 3],
        2,
        [
            r(*STD),
            r(*STD),
            r(*STD),
            r(100, 100, 98, 98, sma250=100),
            r(97, 99, 97, 98),
            r(98, 99, 97, 98),
        ],
        [(1, 100, 4, 97, "sma250", 4, 3)],
        0,
    ),
    # Sinyal son günde: ertesi gün yok, işlem yok, düşer.
    "sinyalden_sonra_veri_yok": ([2], 2, [r(*STD), r(*STD), r(*STD)], [], 1),
    # Düşük = stop (96): dokunmuş sayılır, dolum min(96, 98) = 96.
    "stop_kenari_dusuk_esit": (
        [0],
        2,
        [r(*STD), r(*STD), r(98, 99, 96, 98)],
        [(1, 100, 2, 96, "stop", 4, 4)],
        0,
    ),
    # Düşük 96,01 > 96: dokunmaz. Veri biter: son kapanış 98'den çıkış.
    "stop_kenari_dusuk_ustte": (
        [0],
        2,
        [r(*STD), r(*STD), r(98, 99, 96.01, 98)],
        [(1, 100, 2, 98, "veri_sonu", 4, 2)],
        0,
    ),
    # Yüksek = stop (96), bütün gün stop altında: min(96, 95) = 95.
    "stop_kenari_yuksek_esit": (
        [0],
        2,
        [r(*STD), r(*STD), r(95, 96, 94, 95)],
        [(1, 100, 2, 95, "stop", 4, 5)],
        0,
    ),
    # Lot yuvarlama (adet = 1, yalnız fiyat yolu): ATR 1,37 -> stop 52,35 - 2,74 = 49,61.
    # d2 düşük 49,6 <= 49,61 -> min(49,61; 50,0) = 49,61. Risk 2,74.
    "lot_yuvarlama_fiyat_yolu": (
        [0],
        1.37,
        [r(50, 51, 49, 50), r(52.35, 53, 51.5, 52.5), r(50.0, 51, 49.6, 50.5)],
        [(1, 52.35, 2, 49.61, "stop", 2.74, 2.74)],
        0,
    ),
    # %10 tavan (adet = 1): d2 kilitli tavan açık pozisyonu etkilemez. d3 kapanış 106 < SMA 108 -> d4 AOF 105.
    # Kâr: gerçekleşen kayıp 0.
    "yuzde10_tavan_fiyat_yolu": (
        [0],
        2,
        [
            r(*STD),
            r(*STD),
            r(110, 110, 110, 110, kilit_tavan=True),
            r(110, 111, 105, 106, sma250=108),
            r(105, 107, 104, 105),
        ],
        [(1, 100, 4, 105, "sma250", 4, 0)],
        0,
    ),
    # Olay günü (d2): düzeltilmiş seri kesintisiz, ham düşüş mumda yok. Pozisyon sürer; d3 düşük 95,5 -> 96.
    "olay_gununde_acik_pozisyon": (
        [0],
        2,
        [r(*STD), r(*STD), r(99, 100, 98, 99), r(97, 98, 95.5, 96)],
        [(1, 100, 3, 96, "stop", 4, 4)],
        0,
    ),
    # d3 karantina: çıkış son temiz AOF'ta (d2: 101), çöp fiyatlar yok sayılır.
    "karantinada_acik_pozisyon": (
        [0],
        2,
        [r(*STD), r(*STD), r(101, 102, 100, 101), r(500, 500, 1, 300, karantina=True)],
        [(1, 100, 3, 101, "karantina", 4, 0)],
        0,
    ),
    # Giriş günü karantina: sinyal düşer.
    "karantinada_giris_gunu": (
        [0],
        2,
        [r(*STD), r(500, 500, 1, 300, karantina=True), r(*STD)],
        [],
        1,
    ),
    # Stop hiç dokunmaz, veri biter: son kapanış 103,5.
    "veri_sonu_cikisi": (
        [0],
        2,
        [r(*STD), r(*STD), r(100, 103, 99, 102), r(103, 104, 101, 103.5)],
        [(1, 100, 3, 103.5, "veri_sonu", 4, 0)],
        0,
    ),
    # d2 eksik gün: açık pozisyon aynen taşınır. d3 düşük 94 -> min(96, 95) = 95.
    "eksik_gunde_acik_pozisyon": (
        [0],
        2,
        [r(*STD), r(*STD), EKSIK, r(95, 96, 94, 95)],
        [(1, 100, 3, 95, "stop", 4, 5)],
        0,
    ),
    # Giriş günü eksik: sinyal düşer, d2'ye kaymaz.
    "eksik_giris_gunu": ([0], 2, [r(*STD), EKSIK, r(*STD)], [], 1),
}


def _mumlar(satirlar, atr):
    df = pd.DataFrame(satirlar, index=GUNLER[: len(satirlar)])
    df["atr"] = float(atr)
    for ad, varsayilan in (
        ("islem", True),
        ("karantina", False),
        ("kilit_tavan", False),
        ("kilit_taban", False),
        ("sma250", 50.0),
    ):
        df[ad] = (
            varsayilan
            if ad not in df
            else df[ad].fillna(varsayilan).astype(type(varsayilan))
        )
    return df


@pytest.mark.parametrize("ad", SENARYO)
def test_motor_senaryosu(ad):
    sinyaller, atr, satirlar, beklenen, iptal = SENARYO[ad]
    islemler, dusen = motor.islemler(_mumlar(satirlar, atr), GUNLER[sinyaller])
    gercek = [
        (
            GUNLER.get_loc(t.giris_tarih),
            t.giris_fiyat,
            GUNLER.get_loc(t.cikis_tarih),
            t.cikis_fiyat,
            t.neden,
            t.planlanan_risk,
            t.gerceklesen_kayip,
        )
        for t in islemler.itertuples()
    ]
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
    tablo, dusen = motor.Zincir(
        _mumlar([r(*STD), r(*STD), r(97, 98, 95, 96), r(*STD)], 2)
    ).calistir([0, 2])
    assert [
        (t.sinyal_tarih, t.giris_tarih, t.cikis_tarih, t.neden)
        for t in tablo.itertuples()
    ] == [
        (GUNLER[0], GUNLER[1], GUNLER[2], "stop"),
        (GUNLER[2], GUNLER[3], GUNLER[3], "veri_sonu"),
    ]
    assert dusen == 0


def test_adim_saf_girdiyi_degistirmez():
    p = motor.bekleyen(atr=2.0)
    m = {
        "tarih": GUNLER[1],
        **r(100, 101, 99, 100),
        "islem": True,
        "karantina": False,
        "kilit_tavan": False,
        "kilit_taban": False,
        "sma250": 50.0,
    }
    yeni = motor.adim(p, m)
    assert (p.durum, yeni.durum, yeni.giris_fiyat, yeni.stop) == (
        "bekliyor",
        "acik",
        100,
        96,
    )
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
    f = pd.DataFrame(
        {
            "sembol": "XXXX",
            "tarih": GUNLER[:8],
            "yuksek": yuk,
            "dusuk": [k - 0.5 for k in kap],
            "kapanis": kap,
            "aof": kap,
            "hacim": 1e6,
        }
    )
    for s in ("kapanis", "aof", "yuksek", "dusuk"):
        f["ham_" + s] = f[s]
    anlik = Anlik("t", f, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"]))
    p = aileler.Parametre(
        periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=4, sma_n=2
    )
    islemler, dusen = motor.sinama(anlik, p, atr_n=2)
    assert dusen == 0 and len(islemler) == 1
    t = islemler.iloc[0]
    assert (t.sembol, t.sinyal_tarih, t.giris_tarih, t.cikis_tarih, t.neden) == (
        "XXXX",
        GUNLER[5],
        GUNLER[6],
        GUNLER[7],
        "veri_sonu",
    )
    assert (t.giris_fiyat, t.cikis_fiyat, t.gerceklesen_kayip) == (104.0, 105.0, 0.0)
    assert t.planlanan_risk == pytest.approx(4.5625, abs=1e-9)


def test_sinama_evren_disi_sinyal_pozisyon_acmaz_sonraki_gecerli_sinyal_gecikmez(
    monkeypatch,
):
    # Bilet 11 düzeltmesi (TASARIM 5.6 evren süzgeci). Aynı seri; iki sinyal: 28.01 (üye değil) ve 02.02 (üye).
    # Süzgeçsiz motor 28.01 sinyaliyle 29.01'de pozisyon açar (stop 100 - 2*1,25 = 97,5 dokunmaz) ve 02.02 sinyali
    # açık pozisyon yüzünden düşerdi. Süzgeçle yalnız 02.02 sinyali kalır: giriş 03.02 AOF 104, çıkış 04.02 veri sonu 105.
    from tansu.veri import Anlik

    gun = pd.bdate_range("2026-01-26", periods=8)
    kap = [100.0] * 5 + [103.0, 104.0, 105.0]
    f = pd.DataFrame(
        {
            "sembol": "XXXX",
            "tarih": gun,
            "yuksek": [k + 0.5 for k in kap],
            "dusuk": [k - 0.5 for k in kap],
            "kapanis": kap,
            "aof": kap,
            "hacim": 1e6,
        }
    )
    for s in ("kapanis", "aof", "yuksek", "dusuk"):
        f["ham_" + s] = f[s]
    anlik = Anlik("t", f, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"]))
    monkeypatch.setattr(
        aileler, "sinyal", lambda m, p: pd.DatetimeIndex([gun[2], gun[5]])
    )
    uye = pd.DataFrame({"sembol": "XXXX", "tarih": gun[5:]})
    islemler, dusen = motor.sinama(anlik, aileler.Parametre(sma_n=2), atr_n=2, uye=uye)
    assert dusen == 0 and len(islemler) == 1
    t = islemler.iloc[0]
    assert (
        t.sinyal_tarih,
        t.giris_tarih,
        t.giris_fiyat,
        t.cikis_tarih,
        t.cikis_fiyat,
    ) == (gun[5], gun[6], 104.0, gun[7], 105.0)


@pytest.mark.parametrize("uye_gunleri", [slice(5, 6), slice(5, 7)])
def test_sinama_uyelik_tablosunda_tek_gunluk_ve_iki_gunluk_sembol(
    monkeypatch, uye_gunleri
):
    # Bilet 07b: tek üyelik günü olan sembolde `groupby.agg(DatetimeIndex)` Timestamp döndürüp `isin`i kırıyordu.
    # Aynı seri ve sinyaller (28.01, 02.02); üye günü yalnız 02.02 (ya da 02.02 ve 03.02): sinyal 02.02 alınır,
    # giriş 03.02 AOF 104, çıkış 04.02 veri sonu 105.
    from tansu.veri import Anlik

    gun = pd.bdate_range("2026-01-26", periods=8)
    kap = [100.0] * 5 + [103.0, 104.0, 105.0]
    f = pd.DataFrame(
        {
            "sembol": "XXXX",
            "tarih": gun,
            "yuksek": [k + 0.5 for k in kap],
            "dusuk": [k - 0.5 for k in kap],
            "kapanis": kap,
            "aof": kap,
            "hacim": 1e6,
        }
    )
    for s in ("kapanis", "aof", "yuksek", "dusuk"):
        f["ham_" + s] = f[s]
    anlik = Anlik("t", f, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"]))
    monkeypatch.setattr(
        aileler, "sinyal", lambda m, p: pd.DatetimeIndex([gun[2], gun[5]])
    )
    uye = pd.DataFrame({"sembol": "XXXX", "tarih": gun[uye_gunleri]})
    islemler, dusen = motor.sinama(anlik, aileler.Parametre(sma_n=2), atr_n=2, uye=uye)
    assert dusen == 0 and len(islemler) == 1
    t = islemler.iloc[0]
    assert (
        t.sinyal_tarih,
        t.giris_tarih,
        t.giris_fiyat,
        t.cikis_tarih,
        t.cikis_fiyat,
    ) == (gun[5], gun[6], 104.0, gun[7], 105.0)


def test_piyasa_durumu_motoru_ve_girisi_etkilemez():
    # TASARIM 3: piyasa durumu etiketi motorun sinyalini ve girişini değiştirmez.
    from tests.test_simulator import P, mum, sinyalli

    gunler = pd.bdate_range("2025-11-17", periods=58)
    fiyat = pd.DataFrame(
        [mum(g, 100.0, 100.5, 99.5) for g in gunler[:50]] + sinyalli()
    ).assign(sembol="A")
    sonuclar = []
    for son_endeks, etiket in ((110.0, True), (90.0, False)):
        f = fiyat.copy()
        f["xu100"] = [100.0] * 55 + [son_endeks] * 3
        assert (
            gostergeler.piyasa_durumu(f.set_index("tarih")["xu100"]).iloc[55] == etiket
        )
        a = veri.Anlik(
            "piyasa", f, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
        )
        t, dusen = motor.sinama(a, P, atr_n=2)
        assert dusen == 0
        assert t[
            ["sinyal_tarih", "giris_tarih", "giris_fiyat", "cikis_fiyat"]
        ].values.tolist() == [
            [pd.Timestamp("2026-02-02"), pd.Timestamp("2026-02-03"), 104.0, 105.0]
        ]
        sonuclar.append(t)
    pd.testing.assert_frame_equal(sonuclar[0], sonuclar[1])


def test_gostergeler_duzeltilmis_limit_ve_kilit_ham_seriden():
    # TASARIM 5.1: göstergeler HGDG'den, limit ve kilit HG'den hesaplanır.
    from tests.test_simulator import P, sinyalli

    fiyat = pd.DataFrame(sinyalli()).assign(sembol="A")
    for sutun in ("ham_kapanis", "ham_aof", "ham_yuksek", "ham_dusuk"):
        fiyat[sutun] *= 2.0
        fiyat.loc[6:, sutun] = 226.6
    a = veri.Anlik(
        "olcek", fiyat, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    )
    m = motor.mumlar(a, "A", P, atr_n=2)
    assert (m.iloc[5].sma250, m.iloc[5].atr) == (101.5, 2.28125)
    assert m.iloc[6].kilit_tavan and not m.iloc[6].karantina
    assert a.gun_tablosu.iloc[6].tavan == pytest.approx(226.6)
    # Düzeltilmiş 104, tavanda değildir; ham 226,6 tavanda olduğu için giriş düşer.
    t, dusen = motor.sinama(a, P, atr_n=2)
    assert t.empty and dusen == 1


def test_evrenden_cikan_acik_pozisyon_kendi_kuraliyla_kapanir():
    # TASARIM 5.2: üyelik yalnız yeni girişi sınırlar, açık pozisyonu kapatmaz.
    from tests.test_simulator import P, sinyalli

    fiyat = pd.DataFrame(sinyalli()).assign(sembol="A")
    a = veri.Anlik(
        "evren", fiyat, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    )
    # Sinyal günü üye; girişten itibaren evrende değil. Çıkış yine kendi veri sonu kuralı.
    # Tek satırlı üyelik motoru düşürür (bilet 07); sinyal günü ve önceki gün üye.
    uye = pd.DataFrame(
        {"sembol": ["A", "A"], "tarih": pd.to_datetime(["2026-01-30", "2026-02-02"])}
    )
    t, dusen = motor.sinama(a, P, atr_n=2, uye=uye)
    assert dusen == 0
    assert t[
        ["giris_tarih", "cikis_tarih", "cikis_fiyat", "neden"]
    ].values.tolist() == [
        [pd.Timestamp("2026-02-03"), pd.Timestamp("2026-02-04"), 105.0, "veri_sonu"]
    ]


# --- Modül 1 çıkış tarafı (KURALLAR §3 "Modül 1"; TASARIM 5.3, 5.5) ---
# Varsayılan ayar için değişmezlik: `test_motor_senaryosu` ve `test_zincir_islemler_ile_ayni_tabloyu_verir` (yukarıda) ek
# sütunsuz mumlarla ve ayarsız çağrıyla değişmeden geçer.
# Satırlar yukarıdaki gibi: sinyal günü 0 (STD, ATR 2), giriş günü 1 AOF 100. Varsayılan stop 100 - 2*2 = 96.
# Beklenen: (giriş günü, giriş, çıkış günü, çıkış, neden, planlanan risk, gerçekleşen kayıp).

Parametre = aileler.Parametre
S0 = r(*STD)
GIRIS = r(100, 101, 99, 100)  # giriş günü: düşük 99 her stopun üstünde


def _kurulum(alt=float("nan"), hedef=float("nan")):
    return pd.DataFrame({"kutu_alt": [alt], "hedef": [hedef]}, index=GUNLER[[0]])


def _ozet(satirlar, ayar, kurulum=None):
    t, dusen = motor.islemler(_mumlar(satirlar, 2), GUNLER[[0]], ayar, kurulum)
    assert dusen == 0 and len(t) == 1
    x = t.iloc[0]
    return (
        GUNLER.get_loc(x.giris_tarih),
        x.giris_fiyat,
        GUNLER.get_loc(x.cikis_tarih),
        x.cikis_fiyat,
        x.neden,
        x.planlanan_risk,
        x.gerceklesen_kayip,
    )


def _ak(beklenen):
    return tuple(x if isinstance(x, str) else pytest.approx(x) for x in beklenen)


STOP_HEDEF = {
    # atr15: stop 100 - 1,5*2 = 97. Gün 2 düşük 96 <= 97 -> min(97, 98) = 97. Risk 3, kayıp 3.
    "atr15": (
        Parametre(stop="atr15"),
        None,
        [S0, GIRIS, r(98, 99, 96, 97)],
        (1, 100, 2, 97, "stop", 3, 3),
    ),
    # kutu: stop = kutu alt 95. Gün 2 düşük 94 <= 95 -> min(95, 96) = 95. Risk 5, kayıp 5.
    "kutu": (
        Parametre(stop="kutu"),
        _kurulum(95.0),
        [S0, GIRIS, r(96, 97, 94, 95)],
        (1, 100, 2, 95, "stop", 5, 5),
    ),
    # kutu ama kurulum yok (K1 rastgele girişi): atr2 yedeği, stop 96. Gün 2 düşük 95 <= 96 -> min(96, 97) = 96.
    "kutu_kurulum_yok": (
        Parametre(stop="kutu"),
        None,
        [S0, GIRIS, r(97, 98, 95, 96)],
        (1, 100, 2, 96, "stop", 4, 4),
    ),
    # kutu ama sinyal günü kurulum satırında kutu alt NaN: aynı yedek.
    "kutu_alt_nan": (
        Parametre(stop="kutu"),
        _kurulum(),
        [S0, GIRIS, r(97, 98, 95, 96)],
        (1, 100, 2, 96, "stop", 4, 4),
    ),
    # kutu alt 99,9 < AOF 100: giriş olur. Giriş günü düşük 99 <= 99,9 -> min(99,9; 100) = 99,9. Risk 0,1, kayıp 0,1.
    "kutu_alti_aof_altinda_giris_olur": (
        Parametre(stop="kutu"),
        _kurulum(99.9),
        [S0, r(100, 100.5, 99, 100)],
        (1, 100, 1, 99.9, "stop", 0.1, 0.1),
    ),
    # hedef 106. Gün 2 yüksek 107 >= 106, düşük 101 <= 106 -> dolum hedef fiyatı 106. Risk 4 (stop 96), kayıp 0.
    "hedef_fiyatinda": (
        Parametre(hedef="tansu"),
        _kurulum(hedef=106.0),
        [S0, GIRIS, r(102, 107, 101, 106)],
        (1, 100, 2, 106, "hedef", 4, 0),
    ),
    # Gün 2 düşük 107 > 106: boşluk, dolum AOF 109.
    "hedef_aof": (
        Parametre(hedef="tansu"),
        _kurulum(hedef=106.0),
        [S0, GIRIS, r(109, 110, 107, 108)],
        (1, 100, 2, 109, "hedef", 4, 0),
    ),
    # Gün 2 hem hedefe (yüksek 108 >= 106) hem stopa (düşük 95 <= 96) dokunur: önce stop, min(96, 100) = 96.
    "stop_hedeften_once": (
        Parametre(hedef="tansu"),
        _kurulum(hedef=106.0),
        [S0, GIRIS, r(100, 108, 95, 100)],
        (1, 100, 2, 96, "stop", 4, 4),
    ),
    # Giriş günü yüksek 110 >= 106 ama giriş günü yalnız stop kontrol edilir. Gün 2 yüksek 102 < 106; veri sonu 101.
    "giris_gunu_hedef_yok": (
        Parametre(hedef="tansu"),
        _kurulum(hedef=106.0),
        [S0, r(100, 110, 99, 100), r(101, 102, 100, 101)],
        (1, 100, 2, 101, "veri_sonu", 4, 0),
    ),
}


@pytest.mark.parametrize("ad", STOP_HEDEF)
def test_baslangic_stopu_ve_hedef_cikisi(ad):
    ayar, kurulum, satirlar, beklenen = STOP_HEDEF[ad]
    assert _ozet(satirlar, ayar, kurulum) == _ak(beklenen)


@pytest.mark.parametrize("alt", [100.0, 104.0])
def test_kutu_stopu_aof_kutu_altina_esit_ya_da_altindaysa_giris_iptal(alt):
    # Giriş günü AOF 100 <= kutu alt (100 ve 104): giriş iptal, düşen sinyal 1, işlem yok.
    satirlar = [S0, GIRIS, r(101, 102, 100, 101)]
    t, dusen = motor.islemler(
        _mumlar(satirlar, 2), GUNLER[[0]], Parametre(stop="kutu"), _kurulum(alt)
    )
    assert (len(t), dusen) == (0, 1)


# Merdiven ve başabaş (cikis != yok). ATR 2, giriş 100, ilk stop 96 (R = 4), `dip` kuralı hiç tetiklenmez (onceki_dusuk 0).
MERDIVEN = {
    # Gün 2 yüksek 104,5: n = ⌊4,5/2⌋ = 2 -> stop = max(96, 100 + 0) = 100. Başabaş 106'da, yok. Gün 3 düşük 99,5 <= 100
    # -> min(100, 101) = 100. Planlanan risk yine ilk stoptan: 4. Kayıp max(0, 100 - 100) = 0.
    "n2_stop_giris": (
        [
            S0,
            r(100, 101, 99, 100, onceki_dusuk=0),
            r(101, 104.5, 100.5, 104, onceki_dusuk=0),
            r(101, 102, 99.5, 100, onceki_dusuk=0),
        ],
        (1, 100, 3, 100, "stop", 4, 0),
    ),
    # Gün 2 yüksek 106,5: n = ⌊6,5/2⌋ = 3 -> stop = 100 + 1*2 = 102 (başabaş 106'dan 100, küçük kalır).
    # Gün 3 yüksek 104,5: n = 2 -> aday 100 < 102, stop inmez; düşük 103 > 102. Gün 4 düşük 101 <= 102 -> min(102, 103) = 102.
    "n3_stop_bir_atr_ve_asagi_inmez": (
        [
            S0,
            r(100, 101, 99, 100, onceki_dusuk=0),
            r(101, 106.5, 100.5, 106, onceki_dusuk=0),
            r(104, 104.5, 103, 104, onceki_dusuk=0),
            r(103, 104, 101, 102, onceki_dusuk=0),
        ],
        (1, 100, 4, 102, "stop", 4, 0),
    ),
}


@pytest.mark.parametrize("ad", MERDIVEN)
def test_atr_merdiveni_stopu_yukseltir_planlanan_risk_ilk_stoptan(ad):
    satirlar, beklenen = MERDIVEN[ad]
    assert _ozet(satirlar, Parametre(cikis="dip")) == _ak(beklenen)


def _basabas(yuksek, ayar):
    # kutu stopu alt 98 -> R = 2; başabaş eşiği 100 + 1,5*2 = 103. Yüksek 103 için n = ⌊3/2⌋ = 1: merdiven yok.
    satirlar = [
        S0,
        r(100, 101, 99, 100, onceki_dusuk=0),
        r(101, yuksek, 100.5, 102, onceki_dusuk=0),
        r(100.5, 101, 99.5, 100, onceki_dusuk=0),
    ]
    return _ozet(satirlar, ayar, _kurulum(98.0))


@pytest.mark.parametrize(
    "yuksek, cikis, beklenen",
    [
        # 103 >= 103: stop = max(98, 100) = 100. Gün 3 düşük 99,5 <= 100 -> min(100; 100,5) = 100. Risk 2.
        (103.0, "dip", (1, 100, 3, 100, "stop", 2, 0)),
        # 102,9 < 103: stop 98 kalır; gün 3 düşük 99,5 > 98; veri sonu 100.
        (102.9, "dip", (1, 100, 3, 100, "veri_sonu", 2, 0)),
        # cikis "yok": başabaş paketi yok; yüksek 103 olsa da stop 98 kalır, veri sonu 100.
        (103.0, "yok", (1, 100, 3, 100, "veri_sonu", 2, 0)),
    ],
)
def test_basabas_1_5_r_sonrasi_stop_girise_yalniz_cikis_paketinde(
    yuksek, cikis, beklenen
):
    ayar = Parametre(stop="kutu", cikis=cikis)
    assert _basabas(yuksek, ayar) == _ak(beklenen)


# Yarı satış kuralları. ATR 2, giriş 100, stop 96. Çıkış fiyatı (yarı fiyat + son çıkış) / 2.
YARI = {
    # atr3: seviye 100 + 3*2 = 106. Gün 2 yüksek 107 >= 106, düşük 102 <= 106 -> yarı satış 106 (gün içi).
    # Merdiven stopu 102 yapar (n = 3); gün 3 düşük 105 > 102. Veri sonu 105. Ortalama (106 + 105) / 2 = 105,5.
    "atr3_gun_ici": (
        Parametre(cikis="atr3"),
        [S0, GIRIS, r(103, 107, 102, 106), r(106, 107, 105, 105)],
        (1, 100, 3, 105.5, "veri_sonu", 4, 0),
    ),
    # Gün 2 düşük 107 > 106: yarı satış AOF 108. Tek sefer: gün 3 yüksek 110 >= 106 yine, ama ikinci satış yok.
    # Veri sonu 109. Ortalama (108 + 109) / 2 = 108,5 (ikinci satış olsaydı (109 + 109) / 2).
    "atr3_aof": (
        Parametre(cikis="atr3"),
        [S0, GIRIS, r(108, 110, 107, 109), r(109, 110, 108, 109)],
        (1, 100, 3, 108.5, "veri_sonu", 4, 0),
    ),
    # dip: etkinlik 100 + 1,5*2 = 103. Gün 2 yüksek 103 -> etkin (aynı günün kapanışı 102 >= 99, tetik yok).
    # Gün 3 kapanış 100 < önceki düşük 100,5 -> tetik; gün 4 AOF 101 yarı satış. Gün 5 kapanış 99 < 100 yine tetik:
    # yarı satış zaten yapıldı, kalan yarı için kural yok. Gün 6 veri sonu 99,5 (düşük 98,5 > stop 96).
    # Ortalama (101 + 99,5) / 2 = 100,25 (ikinci satış olsaydı yarı fiyat 99: 99,25).
    "dip_tek_sefer": (
        Parametre(cikis="dip"),
        [
            S0,
            r(100, 101, 99, 100, onceki_dusuk=0),
            r(101, 103, 100.5, 102, onceki_dusuk=99),
            r(102, 102.5, 99.5, 100, onceki_dusuk=100.5),
            r(101, 102, 100, 101, onceki_dusuk=99.5),
            r(100, 101, 98, 99, onceki_dusuk=100),
            r(99, 100, 98.5, 99.5, onceki_dusuk=98),
        ],
        (1, 100, 6, 100.25, "veri_sonu", 4, 0),
    ),
    # Tablo: yarı satış 101, sonra stop. Gün 5 düşük 95 <= 96 -> min(96, 96,5) = 96. Ortalama (101 + 96) / 2 = 98,5.
    # Gerçekleşen kayıp 100 - 98,5 = 1,5. Planlanan risk 4 (ilk stop 96).
    "tablo_ortalama_cikis_fiyati": (
        Parametre(cikis="dip"),
        [
            S0,
            r(100, 101, 99, 100, onceki_dusuk=0),
            r(101, 103, 100.5, 102, onceki_dusuk=99),
            r(102, 102.5, 99.5, 100, onceki_dusuk=100.5),
            r(101, 101.5, 100.5, 100.8, onceki_dusuk=99.5),
            r(96.5, 97, 95, 96, onceki_dusuk=100),
        ],
        (1, 100, 5, 98.5, "stop", 4, 1.5),
    ),
    # Kilitli taban: gün 3 tetik, gün 4 kilitli taban (düşük 99 > 96): yarı satış kayar. Gün 5 AOF 101 -> yarı satış 101.
    # Gün 6 veri sonu 103. Ortalama (101 + 103) / 2 = 102 (kaymasaydı gün 4 AOF 99: (99 + 103) / 2 = 101).
    "dip_kilitli_taban_gunu_yari_satis_kayar": (
        Parametre(cikis="dip"),
        [
            S0,
            r(100, 101, 99, 100, onceki_dusuk=0),
            r(101, 103, 100.5, 102, onceki_dusuk=99),
            r(102, 102.5, 99.5, 100, onceki_dusuk=100.5),
            r(99, 99, 99, 99, kilit_taban=True, onceki_dusuk=99.5),
            r(101, 102, 100, 101, onceki_dusuk=99),
            r(103, 104, 102, 103, onceki_dusuk=100),
        ],
        (1, 100, 6, 102, "veri_sonu", 4, 0),
    ),
    # rsi70: gün 2 RSI 72 -> 69 (70'in altında): tetik. Gün 3 AOF 100,5 yarı satış (kapanış 100 < önceki düşük 100? hayır).
    # Gün 4 kapanış 99 < önceki düşük 99,5 ve yarı satış yapılmış -> kalanın tamamı ertesi AOF'ta. Gün 5 AOF 98,5
    # (düşük 97,5 > 96), neden cikis_kurali. Ortalama (100,5 + 98,5) / 2 = 99,5; kayıp 0,5.
    "rsi70_yari_sonra_kalan": (
        Parametre(cikis="rsi70"),
        [
            S0,
            r(100, 101, 99, 100, rsi=55, onceki_rsi=54, onceki_dusuk=0),
            r(101, 102, 100, 101, rsi=69, onceki_rsi=72, onceki_dusuk=99),
            r(100.5, 101, 99, 100, rsi=60, onceki_rsi=69, onceki_dusuk=100),
            r(100, 100.5, 98.5, 99, rsi=55, onceki_rsi=60, onceki_dusuk=99.5),
            r(98.5, 99, 97.5, 98, rsi=50, onceki_rsi=55, onceki_dusuk=98.5),
        ],
        (1, 100, 5, 99.5, "cikis_kurali", 4, 0.5),
    ),
}


@pytest.mark.parametrize("ad", YARI)
def test_yari_satis_kurallari(ad):
    ayar, satirlar, beklenen = YARI[ad]
    assert _ozet(satirlar, ayar) == _ak(beklenen)


@pytest.mark.parametrize("cikis", ["dip", "rsi70"])
def test_dip_etkinlesmeden_ve_rsi70_yarisindan_once_kapanis_dusuk_alti_satis_vermez(
    cikis,
):
    # Gün 2 kapanış 99 < önceki düşük 99,5 ama yüksek 101 < 103 (dip etkin değil) ve RSI reddi yok (60, 60): satış yok.
    # Gün 3 veri sonu 99,5. Çıkış fiyatı ortalama değil: 99,5; kayıp 0,5.
    satirlar = [
        S0,
        r(100, 101, 99, 100, rsi=60, onceki_rsi=60, onceki_dusuk=0),
        r(100, 101, 98, 99, rsi=60, onceki_rsi=60, onceki_dusuk=99.5),
        r(99, 100, 98, 99.5, rsi=60, onceki_rsi=60, onceki_dusuk=98),
    ]
    assert _ozet(satirlar, Parametre(cikis=cikis)) == _ak(
        (1, 100, 3, 99.5, "veri_sonu", 4, 0.5)
    )


def _s(r_, onceki_r, sma50, onceki_dusuk, *fiyat):
    return r(
        *fiyat, rsi=r_, onceki_rsi=onceki_r, sma50=sma50, onceki_dusuk=onceki_dusuk
    )


G1 = _s(55, 54, 90, 0, 100, 101, 99, 100)  # rsi50 giriş günü
RSI50 = {
    # Gün 2: RSI 52 -> 48 (50 reddi), SMA50 90 < kapanış: tek senaryo -> yarı satış ertesi AOF. Gün 3 AOF 100,8 yarı.
    # Gün 4: yüksek 101 >= SMA50 100,2 > kapanış 99,5 (SMA50 reddi), ikinci farklı senaryo -> tam çıkış ertesi AOF.
    # Gün 5 AOF 99,2 (düşük 98,5 > 96), cikis_kurali. Ortalama (100,8 + 99,2) / 2 = 100; kayıp 0.
    "rsi_sonra_sma50": (
        [
            S0,
            G1,
            _s(48, 52, 90, 99, 101, 102, 100, 101),
            _s(47, 48, 90, 100, 100.8, 101, 100, 100.5),
            _s(46, 47, 100.2, 99, 100, 101, 99, 99.5),
            _s(45, 46, 100, 99, 99.2, 100, 98.5, 99),
        ],
        (1, 100, 5, 100.0, "cikis_kurali", 4, 0),
    ),
    # Gün 2: RSI reddi (52 -> 48), yüksek 103,5 >= 103: dip etkin. Yarı satış gün 3 AOF 101,5.
    # Gün 3: kapanış 100 < önceki düşük 101 ve dip etkin -> ikinci farklı senaryo (1,5 ATR kârda dip) -> tam çıkış.
    # Gün 4 AOF 100 (düşük 99 > 96). Ortalama (101,5 + 100) / 2 = 100,75.
    "rsi_sonra_dip": (
        [
            S0,
            G1,
            _s(48, 52, 90, 99, 102, 103.5, 101, 102),
            _s(47, 48, 90, 101, 101.5, 102, 99, 100),
            _s(46, 47, 90, 99, 100, 100.5, 99, 99.5),
        ],
        (1, 100, 4, 100.75, "cikis_kurali", 4, 0),
    ),
    # Gün 2: RSI reddi (52 -> 48) ve SMA50 reddi (yüksek 101,5 >= 100,2 > kapanış 100) aynı gün: yarı satış yok,
    # tam çıkış gün 3 AOF 99,5 (düşük 99 > 96). Çıkış fiyatı 99,5; kayıp 0,5.
    "ayni_gun_iki_senaryo": (
        [
            S0,
            G1,
            _s(48, 52, 100.2, 99, 100.5, 101.5, 99.5, 100),
            _s(47, 48, 100, 99, 99.5, 100, 99, 99.5),
        ],
        (1, 100, 3, 99.5, "cikis_kurali", 4, 0.5),
    ),
    # Gün 2 ve gün 3: RSI reddi iki kez (52 -> 48; 50,5 -> 47) = aynı senaryo, tam çıkış yok. Yarı satış gün 3 AOF 100,8.
    # Gün 4 veri sonu 101,5. Ortalama (100,8 + 101,5) / 2 = 101,15.
    "ayni_senaryo_iki_kez_tam_cikis_yok": (
        [
            S0,
            G1,
            _s(48, 52, 90, 99, 101, 102, 100, 101),
            _s(47, 50.5, 90, 100, 100.8, 101, 100, 100.5),
            _s(48, 47, 90, 100, 101, 102, 100.5, 101.5),
        ],
        (1, 100, 4, 101.15, "veri_sonu", 4, 0),
    ),
}


@pytest.mark.parametrize("ad", RSI50)
def test_rsi50_ilk_senaryo_yari_ikinci_farkli_senaryo_tam_cikis(ad):
    satirlar, beklenen = RSI50[ad]
    assert _ozet(satirlar, Parametre(cikis="rsi50")) == _ak(beklenen)


def test_zincir_onbellek_anahtari_kurulum_degerini_icerir():
    # Aynı konum, iki kutu. Kutu alt 95: gün 2 düşük 96 > 95, dokunmaz, veri sonu 97. Kutu alt 97: 96 <= 97 -> stop 97.
    m = _mumlar([S0, GIRIS, r(98, 99, 96, 97)], 2)
    ayar = Parametre(stop="kutu")
    z = motor.Zincir(m, ayar)
    assert z.calistir([0], _kurulum(95.0))[0].neden.tolist() == ["veri_sonu"]
    assert z.calistir([0], _kurulum(97.0))[0].neden.tolist() == ["stop"]
    for alt in (95.0, 97.0):
        beklenen, _ = motor.islemler(m, GUNLER[[0]], ayar, _kurulum(alt))
        tablo, _ = motor.Zincir(m, ayar, _kurulum(alt)).calistir([0])
        pd.testing.assert_frame_equal(tablo, beklenen, check_dtype=False)


def _anlik(gun, kapanis, yuksek, dusuk, aof=None):
    f = pd.DataFrame(
        {
            "sembol": "XXXX",
            "tarih": gun,
            "yuksek": yuksek,
            "dusuk": dusuk,
            "kapanis": kapanis,
            "aof": aof or kapanis,
            "hacim": 1e6,
        }
    )
    for s in ("kapanis", "aof", "yuksek", "dusuk"):
        f["ham_" + s] = f[s]
    return veri.Anlik(
        "t", f, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    )


def test_mumlar_yeni_sutunlar_hacim_rsi_sma50_onceki_dusuk_onceki_rsi():
    # Kapanış 100 + gün sırası (60 gün): her gün +1, kazanç 1, kayıp 0 -> RSI14 = 100 (gün 14'ten); gün 13 NaN.
    # SMA50 gün 59 = (110 + ... + 159) / 50 = 134,5. Düşük = kapanış - 0,5: gün 6 önceki düşük = gün 5 düşüğü = 104,5.
    # Önceki RSI gün 15 = gün 14 RSI = 100. Hacim 1e6.
    gun = pd.bdate_range("2026-01-05", periods=60)
    kap = [100.0 + i for i in range(60)]
    a = _anlik(gun, kap, [k + 0.5 for k in kap], [k - 0.5 for k in kap])
    m = motor.mumlar(a, "XXXX", Parametre(sma_n=2), atr_n=2)
    assert m["hacim"].iloc[0] == 1e6
    assert pd.isna(m["rsi"].iloc[13]) and m["rsi"].iloc[14] == pytest.approx(100.0)
    assert m["onceki_rsi"].iloc[15] == pytest.approx(100.0)
    assert m["sma50"].iloc[59] == pytest.approx(134.5)
    assert m["onceki_dusuk"].iloc[6] == pytest.approx(104.5)
    assert pd.isna(m["onceki_dusuk"].iloc[0])


def test_sinama_modul_1_varyanti_kutu_stopu_ve_hedef_cikisi():
    # Elle hesap. İlk 14 gün test_aileler `_ucgen_cercevesi` ile aynı: gün 0-12 düz 100 (sıkışma dönemi), kutu alt 96,
    # kutu üst 105,5, üçgen hedefi 114,5 (orada hesaplı). Gün 13 kapanış 108 > 105,5: sinyal. R/R (kutu stopu) =
    # (114,5 - 108) / (108 - 96) = 0,5417 >= 0,5. Giriş gün 14 AOF 109; stop = kutu alt 96 (düşük 108 > 96); risk 13.
    # Gün 15: yüksek 116 >= 114,5, düşük 111 <= 114,5 -> dolum hedef 114,5, neden hedef. atr3 seviyesi 109 + 3*3,8929
    # = 120,68 > 116: yarı satış yok. Gerçekleşen kayıp 0.
    gun = pd.bdate_range("2026-03-02", periods=16)
    yuk = [101, 102, 105, 102, 101, 101, 102, 102.5, 105.5, 102, 101, 101, 101]
    dus = [99, 99, 99, 96, 99, 99, 97, 99, 99, 98, 99, 99, 99]
    a = _anlik(
        gun,
        [100.0] * 13 + [108.0, 109.0, 115.0],
        yuk + [108.5, 110.0, 116.0],
        dus + [107.0, 108.0, 111.0],
        aof=[100.0] * 13 + [108.0, 109.0, 112.0],
    )
    ayar = replace(
        aileler.VARYANTLAR["giris_kutu"],
        periyotlar=(2, 3),
        esik=0.004,
        min_gun=3,
        pencere=3,
        isinma=1,
        sma_n=2,
        hacim_kat=0.0,
        momentum=False,
        rr_min=0.5,
    )
    islemler, dusen = motor.sinama(a, ayar)
    assert dusen == 0 and len(islemler) == 1
    t = islemler.iloc[0]
    assert (t.sembol, t.sinyal_tarih, t.giris_tarih, t.cikis_tarih, t.neden) == (
        "XXXX",
        gun[13],
        gun[14],
        gun[15],
        "hedef",
    )
    assert (t.giris_fiyat, t.cikis_fiyat, t.gerceklesen_kayip) == (109.0, 114.5, 0.0)
    assert t.planlanan_risk == pytest.approx(13.0, abs=1e-9)


@pytest.mark.parametrize(
    "ad, kat, satir, beklenen",
    [
        # atr15 katı 1,0 olursa stop 100 - 1*2 = 98. Gün 2 düşük 97 <= 98 -> min(98, 98) = 98. Risk 2, kayıp 2.
        ("atr15", 1.0, r(98, 99, 97, 97.5), (1, 100, 2, 98, "stop", 2, 2)),
        # atr2 katı 3,0 olursa stop 100 - 3*2 = 94. Gün 2 düşük 93 <= 94 -> min(94, 96) = 94. Risk 6, kayıp 6.
        ("atr2", 3.0, r(96, 97, 93, 95), (1, 100, 2, 94, "stop", 6, 6)),
    ],
)
def test_baslangic_stopu_atr_kati_aileler_stop_kat_tablosundan_gelir(
    monkeypatch, ad, kat, satir, beklenen
):
    monkeypatch.setitem(aileler.STOP_KAT, ad, kat)
    assert _ozet([S0, GIRIS, satir], Parametre(stop=ad)) == _ak(beklenen)


def test_ayni_gune_iki_donem_sinyali_ilk_donemin_kutusu_kullanilir():
    # KURALLAR §3 Modül 1: aynı güne iki dönemin sinyali düşerse ilk dönemin kutusu kullanılır.
    # İlk satır kutu alt 95, ikinci 98. İlk kazanırsa stop 95: giriş günü düşük 99 > 95; gün 2 düşük 94 <= 95
    # -> min(95, 96) = 95. Risk 5, kayıp 5. (Son satır kazansaydı stop 98 ve dolum 96 olurdu.)
    kurulum = pd.DataFrame(
        {"kutu_alt": [95.0, 98.0], "hedef": [float("nan")] * 2},
        index=GUNLER[[0, 0]],
    )
    satirlar = [S0, GIRIS, r(96, 97, 94, 95)]
    assert _ozet(satirlar, Parametre(stop="kutu"), kurulum) == _ak(
        (1, 100, 2, 95, "stop", 5, 5)
    )
