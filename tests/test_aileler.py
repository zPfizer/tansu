"""`aileler` yüzü: EMA sıkışması giriş sinyali (KURALLAR §3 madde 2). Beklenen değerler elle hesaplandı."""

from dataclasses import asdict

import numpy as np
import pandas as pd
import pytest

from tansu import aileler, gostergeler, motor
from tansu.aileler import (
    Parametre,
    on_sart,
    pencere_gunleri,
    sikismasiz_kirilim,
    sinyal,
)


# Issue #83: bağımsız eski tanımlar; katalogdan beklenen değer türetilmez.
ESKI_TABAN = dict(
    periyotlar=(20, 50, 100, 200),
    esik=0.012,
    min_gun=3,
    pencere=10,
    isinma=500,
    sma_n=250,
    giris="kutu",
    hacim_kat=0.0,
    momentum=False,
    teyit="yok",
    stop="atr2",
    hedef="yok",
    rr_min=2.0,
    cikis="yok",
    kutu_ust="yuksek",
    dusus=False,
)
ESKI_TANSU = dict(
    ESKI_TABAN,
    giris="mum",
    hacim_kat=2.0,
    momentum=True,
    stop="kutu",
    hedef="tansu",
    cikis="atr3",
)
ESKI_DEGISIKLIKLER = {
    "tansu": {},
    "ema_5_8_13": {"periyotlar": (5, 8, 13)},
    "ema_20_50_100": {"periyotlar": (20, 50, 100)},
    "ema_10_20_50": {"periyotlar": (10, 20, 50)},
    "ema_50_100_200": {"periyotlar": (50, 100, 200)},
    "giris_kutu": {"giris": "kutu"},
    "giris_ema": {"giris": "ema"},
    "giris_retest": {"giris": "retest"},
    "giris_agresif": {"giris": "agresif"},
    "giris_arz": {"giris": "arz"},
    "giris_ucgen": {"giris": "ucgen"},
    "kutu_govde": {"kutu_ust": "govde"},
    "hacim_yok": {"hacim_kat": 0.0},
    "hacim_3": {"hacim_kat": 3.0},
    "momentum_kapali": {"momentum": False},
    "dusus_sonrasi": {"dusus": True},
    "teyit_acik": {"teyit": "gosterge"},
    "teyit_trend": {"teyit": "trend"},
    "stop_atr15": {"stop": "atr15"},
    "stop_atr2": {"stop": "atr2"},
    "cikis_dip": {"cikis": "dip"},
    "cikis_rsi70": {"cikis": "rsi70"},
    "cikis_rsi50": {"cikis": "rsi50"},
}
ESKI_TANIMLAR = {"bugun": ESKI_TABAN} | {
    ad: ESKI_TANSU | fark for ad, fark in ESKI_DEGISIKLIKLER.items()
}


def _ortak_paket(f):
    return {
        "semboller": ["TEST"],
        "referans": {
            "kayit_id": "test-veri",
            "istenen_donem": {
                "baslangic": str(f.index[500].date()),
                "bitis": str(f.index[-1].date()),
            },
        },
        "piyasa": [
            {
                "sembol": "TEST",
                "tarih": str(t.date()),
                "kalite_bayraklari": [],
                **{
                    f"duzeltilmis_{ad}": {"deger": r[ad]}
                    for ad in ("kapanis", "yuksek", "dusuk", "aof")
                },
                "hacim_tl": {"deger": r["hacim"]},
            }
            for t, r in f.iterrows()
        ],
    }


def test_ortak_kurulum_tarihli_degerler_ve_stop_girdileri():
    f = _mumlar(
        [100.0] * 510 + [110.0, 112.0],
        [101.0] * 510 + [111.0, 113.0],
        [99.0] * 510 + [100.0, 110.0],
        [100.0] * 512,
    )
    f["aof"] = f["kapanis"]
    strateji = aileler.legacy_coz("bugun")
    sonuc = aileler.ortak_kurulum(_ortak_paket(f), f.index[-1], strateji)
    assert len(sonuc["sinyaller"]) == 1, "Tarihli kurulum sinyalle taşınmadı"
    s = sonuc["sinyaller"][0]
    assert s["tarih"] == str(f.index[-1].date())
    assert s["kutu_alt"]["deger"] == 99.0
    assert s["kutu_ust"]["deger"] == 111.0
    assert s["hedef"] == {"deger": None, "birim": "TL/adet", "bos_nedeni": "uygulanmaz"}
    assert s["ilk_stop"]["bos_nedeni"] == "dolum_bekleniyor"
    assert s["baglar"]["ayar_parmak_izi"] == strateji.ayar_parmak_izi
    girdiler = {a["ad"]: a["deger"] for a in s["kurulum_girdileri"]}
    assert girdiler["stop_kati"] == 2.0
    assert girdiler["atr"] == pytest.approx(2.6683673469387754)
    gost = {g["ad"]: g for g in sonuc["gostergeler"]}
    assert gost["sma250"]["deger"] == pytest.approx(100.088)
    assert gost["sma250"]["tarih"] == s["tarih"]
    assert sonuc["isinma"]["TEST"] == {"gozlem": 512, "gerekli": 500, "tamam": True}


@pytest.mark.parametrize("varyant", ["bugun", "tansu", "giris_agresif", "teyit_acik"])
def test_ortak_kurulum_eski_uyarlayicilarla_eslesir(varyant):
    f = _mumlar(
        [100.0] * 510 + [110.0, 112.0],
        [101.0] * 510 + [111.0, 113.0],
        [99.0] * 510 + [100.0, 110.0],
        [100.0] * 510 + [500.0] * 2,
    )
    f["aof"] = f["kapanis"]
    p = aileler.VARYANTLAR[varyant]
    sonuc = aileler.ortak_kurulum(
        _ortak_paket(f), f.index[-1], aileler.legacy_coz(varyant)
    )
    eski = aileler.kurulum(f, p)
    eski = eski.loc[eski.index == f.index[-1]]
    assert [s["tarih"] for s in sonuc["sinyaller"]] == [
        str(t.date()) for t in eski.index
    ]
    for yeni, (_, satir) in zip(sonuc["sinyaller"], eski.iterrows(), strict=True):
        for ad in ("kutu_alt", "kutu_ust", "hedef"):
            assert yeni[ad]["deger"] == (None if pd.isna(satir[ad]) else satir[ad])
    g = {r["ad"]: r["deger"] for r in sonuc["gostergeler"]}
    assert g["ema20"] == gostergeler.ema(f.kapanis, 20).iloc[-1]
    assert g["atr"] == gostergeler.atr(f.yuksek, f.dusuk, f.kapanis).iloc[-1]


@pytest.mark.parametrize("gozlenen", [None, 50.0])
def test_ortak_kurulum_eksik_gun_ve_isinma(gozlenen):
    f = _mumlar([100.0] * 512, [101.0] * 512, [99.0] * 512, [100.0] * 512)
    f["aof"] = f["kapanis"]
    paket = _ortak_paket(f)
    paket["referans"]["istenen_donem"]["baslangic"] = str(f.index[0].date())
    strateji = aileler.legacy_coz("bugun")
    ilk = aileler.ortak_kurulum(paket, f.index[0], strateji)
    assert ilk["isinma"]["TEST"] == {"gozlem": 1, "gerekli": 500, "tamam": False}
    assert ilk["sinyaller"] == []
    sma = next(g for g in ilk["gostergeler"] if g["ad"] == "sma250")
    assert sma["deger"] is None and sma["bos_nedeni"] == "isinma_veya_tanimsiz"
    for ad in ("kapanis", "yuksek", "dusuk", "aof"):
        paket["piyasa"][-1][f"duzeltilmis_{ad}"]["deger"] = gozlenen
    if gozlenen is not None:
        paket["piyasa"][-1]["kalite_bayraklari"] = ["eksik"]
    eksik = aileler.ortak_kurulum(paket, f.index[-1], strateji)
    assert eksik["sinyaller"] == []
    assert eksik["isinma"]["TEST"] == {"gozlem": 511, "gerekli": 500, "tamam": True}
    sma = next(g for g in eksik["gostergeler"] if g["ad"] == "sma250")
    assert sma["deger"] is None and sma["bos_nedeni"] == "eksik_veri"


def test_ortak_kurulum_degistirilmis_stratejiyi_reddeder():
    from dataclasses import replace

    strateji = aileler.legacy_coz("bugun")
    with pytest.raises(ValueError, match="katalogla uyuşmuyor"):
        aileler.ortak_kurulum(
            {}, "2024-01-01", replace(strateji, aile="cift_rotasyonu")
        )


@pytest.mark.parametrize("ad,beklenen", ESKI_TANIMLAR.items())
def test_katalog_eski_24_tanim_ve_hesap_ciktilari_korunur(ad, beklenen):
    assert callable(getattr(aileler, "legacy_coz", None)), "Katalog uyarlayıcısı yok"
    kayit = aileler.legacy_coz(ad)
    assert {p.ad: p.deger for p in kayit.parametreler} == beklenen
    assert asdict(aileler.VARYANTLAR[ad]) == beklenen
    assert asdict(Parametre()) == ESKI_TABAN
    f = _mumlar(
        [100.0] * 510 + [110.0, 112.0, 114.0, 116.0, 118.0],
        [101.0] * 510 + [111.0, 113.0, 115.0, 117.0, 119.0],
        [99.0] * 510 + [100.0, 110.0, 112.0, 114.0, 116.0],
        [100.0] * 510 + [500.0] * 5,
    )
    eski = Parametre(**beklenen)
    yeni = aileler.VARYANTLAR[ad]
    pd.testing.assert_frame_equal(aileler.kurulum(f, eski), aileler.kurulum(f, yeni))
    pd.testing.assert_index_equal(sinyal(f, eski), sinyal(f, yeni))
    if ad == "bugun":
        assert list(sinyal(f, yeni)) == [f.index[511]]


def _fiyat(kapanis, yuksek=None):
    gun = pd.bdate_range("2026-03-02", periods=len(kapanis))
    return pd.DataFrame(
        {
            "kapanis": [float(k) for k in kapanis],
            "yuksek": yuksek or [k + 0.5 for k in kapanis],
        },
        index=gun,
    )


def _katalog_istegi():
    return {
        "aile": "ema_sikisma",
        "varyant": "tansu",
        "katalog_surumu": "s02_v1",
        "islem_ayarlari": dict.fromkeys(
            (
                "dolum_surumu",
                "risk_surumu",
                "masraf_surumu",
                "muhasebe_surumu",
                "donem_surumu",
            ),
            "legacy_portfoy_v1",
        ),
    }


@pytest.mark.parametrize(
    "fark,kod",
    [
        ({}, "desteklenmeyen_bilesim"),
        ({"izin_durumu": "izinli"}, "bilinmeyen_alan"),
        ({"katalog_surumu": "s02_v2"}, "bilinmeyen_surum"),
        ({"varyant": "giris_ema+stop_atr15"}, "desteklenmeyen_bilesim"),
        ({"sayisal_ayarlar": {"esik": 0.02}}, "duzenlenemez_alan"),
        ({"sayisal_ayarlar": {"uydurma": 1}}, "bilinmeyen_alan"),
        ({"islem_ayarlari": {}}, "eksik_islem_ayari"),
        ({"islem_ayarlari": {"kayma": 0}}, "bilinmeyen_alan"),
    ],
)
def test_katalog_panel_cli_ayni_hata_ve_izin_atlama_yok(fark, kod, capsys):
    import json
    from tansu import katalog

    assert callable(getattr(katalog, "secim_dogrula", None)), "Seçim doğrulayıcısı yok"
    istek = _katalog_istegi() | fark
    with pytest.raises(katalog.KatalogHatasi) as hata:
        katalog.panel_komutu(istek)
    assert hata.value.kod == kod
    assert katalog.cli(["coz", json.dumps(istek)]) == 2
    assert json.loads(capsys.readouterr().err)["hata"] == kod


def test_katalog_tam_sabitler_koken_degismezlik_ve_liste(capsys):
    from dataclasses import FrozenInstanceError
    from tansu import katalog

    assert callable(getattr(katalog, "cli", None)), "Katalog komutu yok"
    k = katalog.legacy_coz("tansu")
    assert {a.ad: a.deger for a in k.sabitler} == {
        "KIRILIM_GUN": 20,
        "ATR_N": 14,
        "HACIM_GUN": 20,
        "RETEST_GUN": 5,
        "BOLGE_GUN": 3,
        "TREND_GUN": 5,
        "YAKIN": 1.01,
        "DUSUS_GUN": 20,
        "DUSUS_ATR": 3.0,
        "STOP_KAT": (("atr2", 2.0), ("atr15", 1.5)),
    }
    for a in (*k.parametreler, *k.sabitler, *k.gosterge_ayarlari):
        assert a.tur and a.birim and a.kaynaklar
        assert a.koken in ("Tansu", "sahip kararı", "YORUM")
        assert a.onayli_aralik is None
    assert k.eski_karsilastirma and k.izin_durumu == "izinsiz"
    assert not k.izin_kaynaklari
    assert k.ayar_parmak_izi == katalog.legacy_coz("tansu").ayar_parmak_izi
    assert k.ayar_parmak_izi != katalog.legacy_coz("stop_atr15").ayar_parmak_izi
    with pytest.raises(FrozenInstanceError):
        k.varyant = "bugun"
    with pytest.raises(FrozenInstanceError):
        k.parametreler[0].deger = (5, 8, 13)
    assert katalog.cli(["liste"]) == 0
    satirlar = capsys.readouterr().out.splitlines()
    assert [s.split("\t")[0] for s in satirlar] == list(ESKI_TANIMLAR)
    assert all(s.endswith("\tizinsiz\teski_karsilastirma") for s in satirlar)


@pytest.mark.parametrize(
    "varyant,ad,koken,son,tarih",
    [
        (
            "ema_5_8_13",
            "periyotlar",
            "Tansu",
            "tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127.md:35",
            "2025-12-19",
        ),
        (
            "ema_20_50_100",
            "periyotlar",
            "Tansu",
            "tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127.md:35",
            "2025-12-19",
        ),
        (
            "ema_50_100_200",
            "periyotlar",
            "Tansu",
            "tweet-ema-sikismasi-ucgen-kirilim-hacim-1954300245707497649.md:24",
            "2025-08-09",
        ),
        (
            "bugun",
            "periyotlar",
            "Tansu",
            "gorsel-paket-67-krdmd-ema-sikisma-ratio-formasyon.md:23",
            "2026-08-28",
        ),
        (
            "bugun",
            "esik",
            "Tansu",
            "gorsel-paket-67-krdmd-ema-sikisma-ratio-formasyon.md:23",
            "2026-08-28",
        ),
        (
            "bugun",
            "min_gun",
            "Tansu",
            "gorsel-paket-67-krdmd-ema-sikisma-ratio-formasyon.md:23",
            "2026-08-28",
        ),
        (
            "tansu",
            "hacim_kat",
            "Tansu",
            "tweet-qullamaggie-tarzi-hacimli-breakout-tarama-1979546907505545421.md:29",
            "2025-10-18",
        ),
        (
            "hacim_3",
            "hacim_kat",
            "Tansu",
            "tweet-qullamaggie-tarzi-hacimli-breakout-tarama-1979546907505545421.md:29",
            "2025-10-18",
        ),
        ("tansu", "rr_min", "sahip kararı", "docs/KURALLAR.md:319", "2026-10-16"),
    ],
)
def test_katalog_alan_kaynagi_bilesim_izni_degildir(varyant, ad, koken, son, tarih):
    from tansu import katalog

    kayit = katalog.legacy_coz(varyant)
    alan = next(a for a in kayit.parametreler if a.ad == ad)
    assert alan.koken == koken
    kaynak = next(k for k in alan.kaynaklar if k.konum.endswith(son))
    assert kaynak.tarih == tarih
    assert kaynak in kayit.kaynaklar
    if son.startswith("gorsel-paket-67"):
        assert "Ham'da yazar yok" in kaynak.karar_durumu
        assert "kayıt tarihi" in kaynak.karar_durumu
    if ad == "periyotlar":
        gosterge = next(a for a in kayit.gosterge_ayarlari if a.ad == "ema_periyotlar")
        assert (gosterge.koken, gosterge.kaynaklar) == (alan.koken, alan.kaynaklar)
    assert next(a for a in kayit.parametreler if a.ad == "pencere").koken == "YORUM"
    assert next(a for a in kayit.sabitler if a.ad == "HACIM_GUN").koken == "YORUM"
    assert kayit.izin_durumu == "izinsiz" and not kayit.izin_kaynaklari
    with pytest.raises(katalog.KatalogHatasi, match="desteklenmeyen_bilesim"):
        katalog.secim_dogrula(_katalog_istegi() | {"varyant": varyant})


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
        *([(100, 101, 99, 100)] * on + [(104, 104.5, 100, mum_hacmi)] + satirlar),
        strict=True,
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


ARTAN = [0, 1, 2, 3, 4, 5, 6, 7]  # her gün bir öncekinden büyük


# Aynı veri. Gösterge teyidi beş şartı birlikte arar: MACD histogramı artıyor (h_t > h_{t-1}), PSAR < kapanış, %K > %D,
# momentum artıyor, ADX artıyor. Bu test ilk üçünü değiştirir; momentum ve ADX her gün artan verilir (iki şart sağlanır).
# Hepsi sağlanır -> gün 5. MACD histogramı düşüyor, PSAR üstte (200 > 103), %K <= %D -> her biri tek başına yok.
# Momentum ve ADX şartları `test_gosterge_teyidi_momentum_ve_adx_artisi_da_ister` testindedir.
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
def test_gosterge_teyidi_macd_psar_stokastik_sartlari_momentum_ve_adx_artarken(
    monkeypatch, hist, psar, k, d, beklenen
):
    f = _mumlar([100, 100, 100, 100, 100, 103, 104, 105])
    seri = lambda v: pd.Series(v, index=f.index, dtype=float)  # noqa: E731
    monkeypatch.setattr(gostergeler, "macd_histogram", lambda *a, **kw: seri(hist))
    monkeypatch.setattr(gostergeler, "psar", lambda *a, **kw: seri(psar))
    monkeypatch.setattr(gostergeler, "stokastik", lambda *a, **kw: (seri(k), seri(d)))
    # Bilet 05: gösterge teyidi momentum ve ADX artışını da ister (KURALLAR §3 "Modül 1"); bu test ikisini her gün artan verir.
    monkeypatch.setattr(gostergeler, "momentum_squeeze", lambda *a, **kw: seri(ARTAN))
    monkeypatch.setattr(gostergeler, "adx", lambda *a, **kw: seri(ARTAN))
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
    # Hedef bulunmaz -> kapı uygulanmaz: `rr_min` varsayılan 2 olsa da gün 13 sinyal. Hedef sütunu NaN.
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


def test_varyantlar_24_ad_temelden_tek_boyut_degisir():
    # Bilet 06 (KURALLAR §3 "Modül 1" Varyantlar, 667a0fd): 20 varyanta `giris_arz`, `giris_ucgen`, `dusus_sonrasi` eklendi.
    # KURALLAR §3 "Modül 1" Varyantlar tablosu 24 ad sayar; `ema_20_50_100` yalnız periyotları değiştirir.
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
        "ema_20_50_100": ("periyotlar", (20, 50, 100)),
        "ema_10_20_50": ("periyotlar", (10, 20, 50)),
        "ema_50_100_200": ("periyotlar", (50, 100, 200)),
        "giris_kutu": ("giris", "kutu"),
        "giris_ema": ("giris", "ema"),
        "giris_retest": ("giris", "retest"),
        "giris_agresif": ("giris", "agresif"),
        "giris_arz": ("giris", "arz"),
        "giris_ucgen": ("giris", "ucgen"),
        "kutu_govde": ("kutu_ust", "govde"),
        "hacim_yok": ("hacim_kat", 0.0),
        "hacim_3": ("hacim_kat", 3.0),
        "momentum_kapali": ("momentum", False),
        "dusus_sonrasi": ("dusus", True),
        "teyit_acik": ("teyit", "gosterge"),
        "teyit_trend": ("teyit", "trend"),
        "stop_atr15": ("stop", "atr15"),
        "stop_atr2": ("stop", "atr2"),
        "cikis_dip": ("cikis", "dip"),
        "cikis_rsi70": ("cikis", "rsi70"),
        "cikis_rsi50": ("cikis", "rsi50"),
    }
    assert set(aileler.VARYANTLAR) == {"bugun", "tansu", *tek}
    assert len(aileler.VARYANTLAR) == 24
    temel_alanlar = asdict(temel)
    for ad, (alan, deger) in tek.items():
        alanlar = asdict(aileler.VARYANTLAR[ad])
        assert {a for a in alanlar if alanlar[a] != temel_alanlar[a]} == {alan}, ad
        assert alanlar[alan] == deger, ad


def test_stop_kat_atr2_ve_atr15_tek_yerde_motor_ile_ayni():
    # TASARIM 5.5 acil stop 2 ATR; KURALLAR §3 Modül 1 atr15 = 1,5 ATR.
    assert aileler.STOP_KAT == {"atr2": 2.0, "atr15": 1.5}
    assert aileler.STOP_KAT["atr2"] == motor.STOP_ATR


def test_stop_kutu_dusuk_sutununu_ister():
    # Kutu stopu kutu altından gelir; `dusuk` yoksa NaN doldurulmaz, KeyError verilir (sessiz düzeltme yok).
    f = _mumlar([100, 100, 100, 100, 100, 103, 104, 105])[["kapanis", "yuksek"]]
    with pytest.raises(KeyError, match="dusuk"):
        aileler.kurulum(f, Parametre(stop="kutu", **KUCUK))
    assert _gunler(f, Parametre(stop="atr2", **KUCUK)) == [
        5
    ]  # varsayılan kural dusuk istemez


# Retest: gün 19 = k+5, pencere (gün 14-16) dışında kalır, ama on_sart günüdür (`retest` penceresi 3 + 5 = 8 gün açıktır: gün 14-21).
# Agresif: sıkışma sürerken pencere yoktur; gün 5, t-1'de biten koşu 5 gün (>= 3) olduğu için on_sart günüdür.
# Elle hesap: aynı veriler yukarıdaki retest "k5-gun" ve agresif testlerindedir; sinyal günleri 19 ve 5.
def test_retest_ve_agresif_sinyal_gunleri_on_sart_gunudur():
    f1 = _mum_sonrasi([(104.5, 105, 103, 100)] * 4 + [(103, 104, 100.5, 100)])
    p1 = Parametre(giris="retest", **MUM)
    f2 = _mumlar(
        [100] * 8,
        [100.5, 100.5, 100.5, 101, 100.5, 100.5, 100.5, 100.5],
        [99.5, 99.5, 99, 99.5, 99.5, 98.8, 98.5, 99.5],
    )
    p2 = Parametre(giris="agresif", **AGRESIF)
    for f, p, gun in ((f1, p1, 19), (f2, p2, 5)):
        assert _gunler(f, p) == [gun]
        assert on_sart(f, p)[gun]
        assert on_sart(f, p).sum() >= 1


# --- Düzeltme turu C: kutu altı kapanış iptali, yeni varyantlar, gövde ucu (KURALLAR §3 "Modül 1") ---


def _tansu(**alan):
    """`tansu` varyantı; küçük ayar: periyotlar (2, 3), eşik 0,004, en az 3 gün, pencere 3, SMA1, hacim ve momentum kapalı."""
    kucuk = dict(KUCUK, sma_n=1, hacim_kat=0.0, momentum=False)
    return Parametre(**{**asdict(aileler.VARYANTLAR["tansu"]), **kucuk, **alan})


# 20 gün: kapanış 100, yüksek 101, düşük 99 (oran 0): dönem gün 0-19, kutu alt 99, kutu üst 101.
# Gün 20: kapanış 97, yüksek 100, düşük 96. EMA2 = 100 - 3*2/3 = 98, EMA3 = 100 - 3/2 = 98,5; oran 0,5/98,5 = 0,0051 > 0,004
# -> dönem gün 19'da biter. 97 < 99: kutu altı kapanış. Gün 21: kapanış 104, yüksek 104,5, düşük 100.
# Gün 21 mum: yeşil (104 > 97), ATR21 = ((26 + 4) / 14 * 13 + 7,5) / 14 = 2,53 <= aralık 4,5, (104 - 100) / 4,5 = 0,89 >= 2/3,
# 104 > 101; ema: 104 > EMA2 102; kutu: 104 > 101. Arz bölgesi ve üçgen yok -> hedef yok, R/R kapısı geçer.
# stop kutu: gün 20'nin kapanışı 97 < 99 -> kurulum iptal, sinyal yok. stop atr2: gün 21 sinyal.
@pytest.mark.parametrize("giris", ["kutu", "ema", "mum"])
def test_kutu_altinda_kapanis_kutu_stopunda_donemi_iptal_eder_atr2_de_etmez(giris):
    f = _mumlar(
        [100.0] * 20 + [97.0, 104.0],
        [101.0] * 20 + [100.0, 104.5],
        [99.0] * 20 + [96.0, 100.0],
    )
    assert _gunler(f, _tansu(giris=giris, stop="atr2")) == [21]
    assert _gunler(f, _tansu(giris=giris, stop="kutu")) == []
    assert _gunler(f, _tansu(giris=giris, stop="atr15")) == [21]


# Gün 0-19 aynı; gün 20 kapanış 97 (kutu altı), gün 21 mum (104; 104,5; 100), gün 22 geri çekilme (102; 103; 100,8).
# Dönem gün 19'da biter (yukarıdaki gibi); pencere gün 20-22; ilk mum k = 21; j = 22 (düşük 100,8 <= 101, kapanış 102 > 101).
# stop atr2: sinyal gün 22. stop kutu: gün 20 kapanışı 97 < 99 (k'dan önce) -> iptal.
def test_kutu_altinda_kapanis_retest_icin_mumdan_once_de_iptal_eder():
    f = _mumlar(
        [100.0] * 20 + [97.0, 104.0, 102.0],
        [101.0] * 20 + [100.0, 104.5, 103.0],
        [99.0] * 20 + [96.0, 100.0, 100.8],
    )
    assert _gunler(f, _tansu(giris="retest", stop="atr2")) == [22]
    assert _gunler(f, _tansu(giris="retest", stop="kutu")) == []


# Kapanış [100, 101, 100, 100, 100, 103, 104, 105]: oran gün 0-4 <= 0,004 (en büyüğü gün 1: 0,1667/100,5 = 0,0017), gün 5
# 0,4769/101,53 = 0,0047 > 0,004 -> dönem gün 0-4. Yüksek [100,5; 101,5; 104; 100,5; 100,5; ...]: en yüksek gün 2 (104).
# Gün 2 gövde ucu = max(önceki kapanış 101, kapanış 100) = 101 (kapanış tek başına 100 olurdu).
# yuksek: kutu üstü 104; 103 > 104 hayır, 104 > 104 hayır, 105 > 104 -> gün 7. govde: kutu üstü 101; 103 > 101 -> gün 5.
def test_kutu_ust_govde_en_yuksek_gunun_govde_ucu_giris_tetigini_ve_sutunu_degistirir():
    f = _mumlar(
        [100, 101, 100, 100, 100, 103, 104, 105],
        [100.5, 101.5, 104, 100.5, 100.5, 103.5, 104.5, 105.5],
    )
    yuksek = Parametre(giris="kutu", kutu_ust="yuksek", **KUCUK)
    govde = Parametre(giris="kutu", kutu_ust="govde", **KUCUK)
    assert _gunler(f, yuksek) == [7]
    assert _gunler(f, govde) == [5]
    assert aileler.kurulum(f, yuksek).iloc[0]["kutu_ust"] == 104.0
    assert aileler.kurulum(f, govde).iloc[0]["kutu_ust"] == 101.0
    assert Parametre().kutu_ust == "yuksek"
    with pytest.raises(ValueError, match="kutu_ust"):
        Parametre(kutu_ust="gövde")


# `_mum_sonrasi`: gün 0-13 düz (kapanış 100, yüksek 101); gün 0 en yüksek gün (eşitlikte ilk) ve önceki kapanış yok -> gövde
# ucu = kapanış 100. Mum günü 14 (104). Gün 15: düşük 100,8, kapanış 102. Gün 16: düşük 99,8, kapanış 101,5.
# yuksek: kutu üstü 101 -> j = 15 (100,8 <= 101), 102 > 101 -> sinyal 15. govde: kutu üstü 100 -> 100,8 <= 100 hayır;
# j = 16 (99,8 <= 100), 101,5 > 100 -> sinyal 16. SMA10 gün 15 = 100,6; gün 16 = 100,75 (ikisi de kapanışın altında).
def test_kutu_ust_govde_retest_seviyesini_degistirir():
    f = _mum_sonrasi([(102, 103, 100.8, 100), (101.5, 102, 99.8, 100)])
    yuksek = Parametre(giris="retest", kutu_ust="yuksek", **MUM)
    govde = Parametre(giris="retest", kutu_ust="govde", **MUM)
    assert _gunler(f, yuksek) == [15]
    assert _gunler(f, govde) == [16]
    assert aileler.kurulum(f, govde).iloc[0]["kutu_ust"] == 100.0


def test_varyantlar_ema_10_20_50_ve_kutu_govde_temelden_tek_boyut_degisir():
    temel = asdict(aileler.VARYANTLAR["tansu"])
    assert temel["kutu_ust"] == "yuksek"
    for ad, alan, deger in (
        ("ema_10_20_50", "periyotlar", (10, 20, 50)),
        ("kutu_govde", "kutu_ust", "govde"),
    ):
        alanlar = asdict(aileler.VARYANTLAR[ad])
        assert {a for a in alanlar if alanlar[a] != temel[a]} == {alan}, ad
        assert alanlar[alan] == deger, ad
    assert len(aileler.VARYANTLAR) == 24


# --- Modül 1 sürüm 2, bilet 04: giriş türleri `arz` ve `ucgen` (KURALLAR §3 "Modül 1", Giriş türü) ---


def _arz_cercevesi(kapanislar, ust=97.0):
    """`_arz_ve_ucgen("yok")` gün 0-32 (P1 gün 0-13, arz bölgesi gün 17'de bilinir: proximal 100, distal 113; P2 gün 20-32,
    kutu 95,95 - `ust`); sonra gün 33 ...: yüksek = kapanış + 0,5, düşük = kapanış - 1."""
    f = _arz_ve_ucgen("yok").iloc[:33]
    return _mumlar(
        [*f["kapanis"], *kapanislar],
        [*f["yuksek"][:20], *[ust] * 13, *[c + 0.5 for c in kapanislar]],
        [*f["dusuk"], *[c - 1 for c in kapanislar]],
    )


# P2 (gün 20-32, esik 0,005) gün 33'te biter (EMA2 107, EMA3 104,25: oran 0,026). Pencere gün 33, 34, 35. Kutu üstü `ust`.
# Arz bölgesi (gün 14 yeşil, gün 17'de bilinir): proximal 100, distal 113 (yüksek_b); hiçbir kapanış 113'ü geçmeden bozulmaz.
# Üst kutu: dönem bitişinde (gün 32) aktif ve proximal 100 > kutu üstü. ust 97: var. ust 101: 100 > 101 hayır -> üst kutu yok.
# P1 (gün 0-13): bölge gün 17'de bilinir, 13'te bilinmez -> üst kutu yok; `arz` P1'de sinyal vermez, `kutu` gün 14'te (112 > 101) verir.
# A) 112,5; 114; 115: 112,5 > 113 hayır; 114 > 113 evet -> gün 34 (gün 35 de üstünde ama dönem başına tek sinyal).
#    `kutu`: 112,5 > 97 -> P2 sinyali gün 33; P1 sinyali gün 14.
# B) 112,5; 113; 112: 113 > 113 hayır (distal dahil değil) -> sinyal yok.
# C) ust 101, kapanışlar A gibi: üst kutu yok -> sinyal yok (114 > 113 olsa da). `kutu`: P2 gün 33 (112,5 > 101).
@pytest.mark.parametrize(
    "kapanislar, ust, arz, kutu",
    [
        ((112.5, 114.0, 115.0), 97.0, [34], [14, 33]),
        ((112.5, 113.0, 112.0), 97.0, [], [14, 33]),
        ((112.5, 114.0, 115.0), 101.0, [], [14, 33]),
    ],
    ids=["distal-ustunde", "distalde-esit", "ust-kutu-yok"],
)
def test_giris_arz_ust_kutunun_distali_ustunda_ilk_kapanis(kapanislar, ust, arz, kutu):
    f = _arz_cercevesi(kapanislar, ust)
    assert _gunler(f, Parametre(giris="kutu", **dict(KUCUK, esik=0.005))) == kutu
    p = Parametre(giris="arz", **dict(KUCUK, esik=0.005))
    assert _gunler(f, p) == arz
    if arz:
        k = aileler.kurulum(f, p).iloc[0]
        assert (k["kutu_alt"], k["kutu_ust"]) == (95.95, ust)


def _ucgen_giris_cercevesi(kapanislar, ilk_tepe=105.0, son_tepe=105.5, dusuk=None):
    """`_ucgen_cercevesi` gibi 13 düz gün (kapanış 100; ilk salınım tepesi gün 2, son tepe gün 8; dipler 96, 97, 98 yükselen),
    sonra gün 13 ...: yüksek = kapanış + 0,5, düşük = kapanış - 1."""
    yuk = [101, 102, ilk_tepe, 102, 101, 101, 102, 102.5, son_tepe, 102, 101, 101, 101]
    dus = dusuk or [99, 99, 99, 96, 99, 99, 97, 99, 99, 98, 99, 99, 99]
    return _mumlar(
        [100.0] * 13 + list(kapanislar),
        yuk + [c + 0.5 for c in kapanislar],
        dus + [c - 1 for c in kapanislar],
    )


# Dönem gün 0-12 (kapanış 100), gün 13'te biter (EMA2 103,93, EMA3 102,95: oran 0,0096 > 0,004). Pencere gün 13, 14, 15. Kutu üstü
# = en yüksek yüksek = 105,5 (son tepe), kutu altı 96. Üçgen: tepeler gün 2 (105) ve gün 8 (105,5): 105,5 <= 105*1,01;
# dipler 96, 97, 98 yükseliyor. Üst çizgi (gün 2, 105) ile (gün 8, 105,5): eğim 0,5/6 = 1/12.
# Çizgi: gün 13 = 105,5 + 5/12 = 105,9167; gün 14 = 105,5 + 6/12 = 106; gün 15 = 105,5 + 7/12 = 106,0833.
# Kapanışlar 105,9; X; 107. Gün 13: 105,9 > 105,9167 hayır. Gün 14: X = 106,01 > 106 evet -> sinyal 14.
# X = 105,99 > 106 hayır; gün 15: 107 > 106,0833 evet -> sinyal 15. `kutu`: 105,9 > 105,5 -> gün 13 (çizgiden önce).
@pytest.mark.parametrize("x, beklenen", [(106.01, [14]), (105.99, [15])])
def test_giris_ucgen_ust_cizgi_ilk_ve_son_tepeden_gecer_dogrusal_uzar(x, beklenen):
    f = _ucgen_giris_cercevesi([105.9, x, 107.0])
    assert _gunler(f, Parametre(giris="kutu", **KUCUK)) == [13]
    p = Parametre(giris="ucgen", **KUCUK)
    assert _gunler(f, p) == beklenen
    k = aileler.kurulum(f, p).iloc[0]
    assert (k["kutu_alt"], k["kutu_ust"]) == (96.0, 105.5)


# Hafif düşen üst çizgi (simetrik üçgen): tepeler gün 2 (105,5) ve gün 8 (105): 105 <= 105,5*1,01. Eğim -0,5/6 = -1/12.
# Çizgi: gün 13 = 105 - 5/12 = 104,5833; gün 14 = 104,5; gün 15 = 104,4167. Kutu üstü 105,5 (ilk tepe).
# Kapanışlar 104,6; 104,7; 104,8. Gün 13: 104,6 > 104,5833 evet -> `ucgen` sinyal 13.
# `kutu`: üç kapanış da 105,5'in altında -> sinyal yok.
def test_giris_ucgen_hafif_dusen_ust_cizgi_kutudan_once_sinyal_verir():
    f = _ucgen_giris_cercevesi([104.6, 104.7, 104.8], ilk_tepe=105.5, son_tepe=105.0)
    assert _gunler(f, Parametre(giris="kutu", **KUCUK)) == []
    p = Parametre(giris="ucgen", **KUCUK)
    assert _gunler(f, p) == [13]
    assert aileler.kurulum(f, p).iloc[0]["kutu_ust"] == 105.5


# Düşükler düz (99): salınım dipleri eşit, "her dip bir öncekinden yüksek" sağlanmaz -> üçgen yok -> `ucgen` sinyal vermez.
# Aynı kapanışlarla (105,9; 106,01; 107) `kutu` gün 13'te sinyal verir (105,9 > 105,5).
def test_giris_ucgen_ucgen_yoksa_sinyal_yok():
    f = _ucgen_giris_cercevesi([105.9, 106.01, 107.0], dusuk=[99.0] * 13)
    assert _gunler(f, Parametre(giris="kutu", **KUCUK)) == [13]
    assert _gunler(f, Parametre(giris="ucgen", **KUCUK)) == []


# K1 havuzu (KURALLAR §3 K1 ön şartı): `arz` ve `ucgen` (a) türünde 10 günlük pencere havuzunu `kutu` gibi kullanır.
# `_arz_cercevesi` penceresi: P1 gün 14-16, P2 gün 33-35 (pencere 3) -> 6 gün. Sinyal günleri havuzdadır.
def test_arz_ve_ucgen_k1_havuzu_kutu_ile_ayni_pencere_gunleri():
    f = _arz_cercevesi((112.5, 114.0, 115.0))
    ortak = dict(KUCUK, esik=0.005)
    kutu = pencere_gunleri(f, Parametre(**ortak))
    assert kutu.sum() == 6
    p = Parametre(giris="arz", **ortak)
    np.testing.assert_array_equal(pencere_gunleri(f, p), kutu)
    assert on_sart(f, p)[34]
    fu = _ucgen_giris_cercevesi([105.9, 106.01, 107.0])
    pu = Parametre(giris="ucgen", **KUCUK)
    np.testing.assert_array_equal(
        pencere_gunleri(fu, pu), pencere_gunleri(fu, Parametre(**KUCUK))
    )
    assert on_sart(fu, pu)[14]


# Geleceği görmeme (TASARIM 5.12): veri n. günde kesilirse n'e kadarki sinyaller tam verininkiyle aynıdır.
@pytest.mark.parametrize(
    "giris, f, ayar",
    [
        ("arz", _arz_cercevesi((112.5, 114.0, 115.0)), dict(KUCUK, esik=0.005)),
        ("ucgen", _ucgen_giris_cercevesi([105.9, 106.01, 107.0]), KUCUK),
    ],
)
def test_giris_arz_ve_ucgen_t_den_sonraki_gunler_t_oncesi_karari_degistirmez(
    giris, f, ayar
):
    p = Parametre(giris=giris, **ayar)
    tam = aileler.kurulum(f, p)
    assert len(tam) == 1  # sınama boş değil
    for n in range(6, len(f) + 1):
        kesik = aileler.kurulum(f.iloc[:n], p)
        pd.testing.assert_frame_equal(tam[tam.index <= f.index[n - 1]], kesik)


# --- Modül 1 sürüm 2, bilet 05: gösterge teyidine momentum ve ADX artışı, düşüş süzgeci (KURALLAR §3 "Modül 1") ---

NAN = float("nan")


# Aynı veri (kapanış [100x5, 103, 104, 105], kutu tetiği gün 5, 6, 7). MACD, PSAR ve stokastik her gün geçer (histogram
# [0,0,0,0,0,1,2,3]: gün 5, 6, 7 artıyor; PSAR 99 < kapanış; %K 50 > %D 40). Momentum ve ADX değerleri verilir.
# 1) ikisi de her gün artıyor -> gün 5.
# 2) momentum [0,0,0,0,2,1,2,3]: gün 5 için 1 > 2 hayır; gün 6 için 2 > 1 evet -> gün 6.
# 3) ADX aynı dizi -> gün 6.
# 4) momentum her gün düşüyor -> sinyal yok.
# 5) ADX [NaN x6, 1, 2]: gün 5 NaN; gün 6 için 1 > NaN hayır (hesaplanamayan gün aday değil); gün 7 için 2 > 1 evet -> gün 7.
# 6) momentum aynı NaN dizisi -> gün 7.
@pytest.mark.parametrize(
    "momentum, adx, beklenen",
    [
        (ARTAN, ARTAN, [5]),
        ([0, 0, 0, 0, 2, 1, 2, 3], ARTAN, [6]),
        (ARTAN, [0, 0, 0, 0, 2, 1, 2, 3], [6]),
        ([7, 6, 5, 4, 3, 2, 1, 0], ARTAN, []),
        (ARTAN, [NAN] * 6 + [1, 2], [7]),
        ([NAN] * 6 + [1, 2], ARTAN, [7]),
    ],
    ids=[
        "ikisi-artiyor",
        "momentum-gun-6",
        "adx-gun-6",
        "momentum-dusuyor",
        "adx-nan",
        "momentum-nan",
    ],
)
def test_gosterge_teyidi_momentum_ve_adx_artisi_da_ister(
    monkeypatch, momentum, adx, beklenen
):
    f = _mumlar([100, 100, 100, 100, 100, 103, 104, 105])
    seri = lambda v: pd.Series(v, index=f.index, dtype=float)  # noqa: E731
    monkeypatch.setattr(
        gostergeler, "macd_histogram", lambda *a, **kw: seri([0, 0, 0, 0, 0, 1, 2, 3])
    )
    monkeypatch.setattr(gostergeler, "psar", lambda *a, **kw: seri(99.0))
    monkeypatch.setattr(
        gostergeler, "stokastik", lambda *a, **kw: (seri(50.0), seri(40.0))
    )
    monkeypatch.setattr(
        gostergeler, "momentum_squeeze", lambda *a, **kw: seri(momentum)
    )
    monkeypatch.setattr(gostergeler, "adx", lambda *a, **kw: seri(adx))
    assert _gunler(f, Parametre(teyit="gosterge", **KUCUK)) == beklenen


def test_parametre_dusus_varsayilani_kapali_agresifle_hata_vermez():
    # Varsayılan kural değişmez (dusus kapalı). KURALLAR §3 Modül 1 Düşüş: agresif girişte dönem başı t-1'de biten
    # koşunun ilk günüdür; birleşim parametre hatası vermez.
    assert Parametre().dusus is False
    assert aileler.VARYANTLAR["tansu"].dusus is False
    # Parametre dikişi: birleşim kurulur ve küçük seride `kurulum` hatasız bir tablo verir (sinyal değerleri aşağıdaki testlerde).
    f = _mumlar([100.0] * 10)
    assert isinstance(
        aileler.kurulum(f, Parametre(giris="agresif", dusus=True, **DUSUS)),
        pd.DataFrame,
    )


def _dusus_cercevesi(onceki, sonra, son):
    """Gün 0-21 kapanış `onceki`, gün 22-39 kapanış `sonra`, gün 40-42 kapanış `son`; yüksek = kapanış + 1, düşük = kapanış - 1."""
    return _mumlar([onceki] * 22 + [sonra] * 18 + [son] * 3)


# Ayar: periyotlar (1, 2) (EMA1 = kapanış, EMA2 alfa 2/3), oran = |kapanış - EMA2| / EMA2, eşik 0,005, en az 3 gün, pencere 3, SMA2.
# Her çerçeve: gün 0-21 düz `onceki` (dönem, 22 gün); gün 22'de `sonra`'ya sıçrama; gün 40'ta `son`. Girişler `kutu` (kutu üstü = yüksek).
# Sıçrama J = onceki - sonra. Gün 22 sonrası EMA2 = sonra + J/3^k (k = 1 gün 22); oran <= 0,005 olan ilk k dönemi başlatır:
#   J=30: k=4 (30/81 = 0,370; oran 0,00369) -> dönem başı gün 25.  J=6: k=3 (6/27 = 0,222; oran 0,0022; k=2 oran 0,0066 > eşik) -> gün 24.
#   J=4: k=2 (4/9 = 0,444; oran 0,00442) -> gün 23.
# ATR14 (Wilder): düz günlerde gerçek aralık 2, tohum 2. Gün 22'de GA = max(2, |101 - önceki|, |99 - önceki|) = J + 1 (önceki = sonra + J).
#   ATR_22 = (13*2 + J + 1)/14; sonraki günler GA 2: ATR_t - 2 = (ATR_22 - 2) * (13/14)^(t - 22).
#   J=30: ATR_22 = 57/14 = 4,071; ATR_25 = 2 + 2,071*0,8007 = 3,659. J=6: ATR_22 = 33/14 = 2,357; ATR_24 = 2 + 0,357*0,862 = 2,308.
#   J=4: ATR_22 = 31/14 = 2,214; ATR_23 = 2 + 0,214*0,929 = 2,199.
# Düşüş şartı: önceki 20 günün en yüksek yükseği M >= kutu alt + 3 ATR (kutu alt = dönem en düşük düşüğü = sonra - 1 = 99).
#   J=30: pencere gün 5-24, M = 131 (gün 5-21 yüksek 131); 99 + 3*3,659 = 109,98 <= 131 -> dönem sayılır.
#   J=6: pencere gün 4-23, M = 107; 99 + 3*2,308 = 105,92 <= 107 -> sayılır.
#   J=4: pencere gün 3-22, M = 105; 99 + 3*2,199 = 105,60 > 105 -> sayılmaz.
# Gün 0-21 dönemi (kutu üstü onceki + 1): sonrası düşük kapanışlar kutu üstünü geçmez, sinyal yok (dönem başı gün 0 de hesaplanamaz).
# Gün 40 kapanış 103: EMA2 = 102, oran 1/102 = 0,0098 > eşik -> dönem gün 39'da biter; 103 > kutu üstü 101 -> sinyal gün 40.
# Yükseliş (onceki 100, sonra 130, son 135): gün 0-21 dönemi sinyali gün 22 (130 > 101). J = -30: sıçrama yukarı, EMA2 = 130 - 30/3^k:
#   k=4 -> gün 25 dönem başı (oran 0,00286), dönem gün 25-39. ATR_25 = 3,659 (J=30 ile aynı: gün 22 GA = max(2, 31, 29) = 31);
#   pencere gün 5-24: M = 131 (gün 22-24 yüksek 131); kutu alt 129; 129 + 3*3,659 = 139,98 > 131 -> sayılmaz.
#   Gün 40 kapanış 135 > kutu üstü 131 -> `dusus` kapalıyken sinyal gün 40. `dusus` açıkken: gün 0-21 dönemi (dönem başı 0 < 20) ve
#   yükseliş sonrası dönem sayılmaz -> sinyal yok.
DUSUS = dict(periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=1, sma_n=2)


@pytest.mark.parametrize(
    "onceki, sonra, son, kapali, acik",
    [
        (130.0, 100.0, 103.0, [40], [40]),
        (106.0, 100.0, 103.0, [40], [40]),
        (104.0, 100.0, 103.0, [40], []),
        (100.0, 130.0, 135.0, [22, 40], []),
    ],
    ids=["dusus-30", "dusus-6", "dusus-4-zayif", "yukselis"],
)
def test_dusus_suzgeci_donem_basindan_onceki_20_gunun_yuksegi_kutu_alt_arti_3_atr(
    onceki, sonra, son, kapali, acik
):
    f = _dusus_cercevesi(onceki, sonra, son)
    assert _gunler(f, Parametre(dusus=False, **DUSUS)) == kapali
    assert _gunler(f, Parametre(dusus=True, **DUSUS)) == acik
    assert _gunler(f, Parametre(**DUSUS)) == kapali  # varsayılan: kapalı


# Geleceği görmeme: `dusus` yalnız dönem başından önceki günlere bakar; veri n. günde kesilirse n'e kadarki sinyaller aynıdır.
def test_dusus_t_den_sonraki_gunler_t_oncesi_karari_degistirmez():
    f = _dusus_cercevesi(130.0, 100.0, 103.0)
    p = Parametre(dusus=True, **DUSUS)
    tam = aileler.kurulum(f, p)
    assert len(tam) == 1  # sınama boş değil
    for n in range(20, len(f) + 1):
        kesik = aileler.kurulum(f.iloc[:n], p)
        pd.testing.assert_frame_equal(tam[tam.index <= f.index[n - 1]], kesik)


# --- Düşüş süzgeci agresif girişte (KURALLAR §3 Modül 1 Düşüş) ---


def _dusus_agresif_cercevesi(onceki, dusuk_26):
    """Gün 0-21 kapanış `onceki`, gün 22-39 kapanış 100, gün 40-42 kapanış 103; yüksek = kapanış + 1, düşük = kapanış - 1,
    yalnız gün 26 düşüğü `dusuk_26`."""
    kapanis = [onceki] * 22 + [100.0] * 18 + [103.0] * 3
    dusuk = [k - 1 for k in kapanis]
    dusuk[26] = dusuk_26
    return _mumlar(kapanis, dusuk=dusuk)


# Ayar: `DUSUS` (yukarıdaki oran/dönem hesabı aynıdır; SMA2: kapanış 100 >= SMA 100). Sıkışma koşuları ve ATR14 `DUSUS` testiyle aynı:
#   Gün 0-21 düz (kapanış `onceki`): koşu gün 0'da başlar, gün 21'de biter; t = 3: koşu 3 gün, düşük `onceki` - 1 <= `onceki` - 1 <= `onceki`
#   (`onceki` 130: 129 <= 129 <= 130; `onceki` 104: 103 <= 103 <= 104) -> sinyal gün 3
#   (dönem başı 0 < 20 -> `dusus` açıkken hesaplanamaz, sayılmaz).
#   J=30 (onceki 130): ikinci koşu gün 25'te başlar (k=4, oran 0,00369); t = 28 (koşu 25-27, 3 gün); düşük 99 <= 99 <= 100 -> sinyal gün 28.
#     Kutu alt = 99. ATR_25 = 3,659 (2 + 2,071 * (13/14)^3). Önceki 20 gün = gün 5-24, en yüksek yüksek 131 (gün 5-21).
#     99 + 3*3,659 = 109,98 <= 131 -> sinyal kalır.
#   J=4 (onceki 104): ikinci koşu gün 23'te başlar (k=2, oran 0,00442); t = 26 (koşu 23-25); ATR_23 = 2,199.
#     Önceki 20 gün = gün 3-22, en yüksek yüksek 105. Gün 26 düşüğü 99: kutu alt 99, 99 + 3*2,199 = 105,60 > 105 -> sinyal düşer.
#     Gün 26 düşüğü 98 (<= 99, kapanış 100 >= 99): kutu alt (koşu + t) 98, 98 + 3*2,199 = 104,60 <= 105 -> sinyal kalır.
@pytest.mark.parametrize(
    "onceki, dusuk_26, kapali, acik",
    [
        (130.0, 99.0, [3, 28], [28]),
        (104.0, 99.0, [3, 26], []),
        (104.0, 98.0, [3, 26], [26]),
    ],
    ids=["dusus-30", "dusus-4-zayif", "dusus-4-t-gunu-kutuyu-derinlestirir"],
)
def test_dusus_agresif_giriste_kosu_basindan_onceki_20_gunun_yuksegi_kutu_alt_arti_3_atr(
    onceki, dusuk_26, kapali, acik
):
    f = _dusus_agresif_cercevesi(onceki, dusuk_26)
    assert _gunler(f, Parametre(giris="agresif", dusus=False, **DUSUS)) == kapali
    assert _gunler(f, Parametre(giris="agresif", dusus=True, **DUSUS)) == acik


# Geleceği görmeme: agresif girişte `dusus` yalnız koşu başından önceki günlere ve t'de bilinen kutu altına bakar.
def test_dusus_agresif_t_den_sonraki_gunler_t_oncesi_karari_degistirmez():
    f = _dusus_agresif_cercevesi(130.0, 99.0)
    p = Parametre(giris="agresif", dusus=True, **DUSUS)
    tam = aileler.kurulum(f, p)
    assert len(tam) == 1  # sınama boş değil
    for n in range(20, len(f) + 1):
        kesik = aileler.kurulum(f.iloc[:n], p)
        pd.testing.assert_frame_equal(tam[tam.index <= f.index[n - 1]], kesik)


# --- Modül 1 sürüm 2, bilet 09: kod incelemesi düzeltmeleri (ayırt edici testler) ---


# ATR14 hesaplanamıyorsa (NaN) süzgeç hesaplanamaz ve dönem sayılmaz (KURALLAR §3 Modül 1, Düşüş). Çerçeve: "dusus-30" (yukarıdaki
# test): ATR varken dönem sayılır, sinyal gün 40. ATR her yerde NaN verilirse karşılaştırma yanlış olur, dönem sayılmaz.
def test_dusus_donem_basinda_atr_nan_ise_donem_sayilmaz(monkeypatch):
    f = _dusus_cercevesi(130.0, 100.0, 103.0)
    assert _gunler(f, Parametre(dusus=True, **DUSUS)) == [40]
    monkeypatch.setattr(
        gostergeler, "atr", lambda *a, **kw: pd.Series(np.nan, index=f.index)
    )
    assert _gunler(f, Parametre(dusus=True, **DUSUS)) == []


# --- Düşüş süzgeci sınırları: eşik eşitliği, pencere kenarları, ATR günü (KURALLAR §3 Modül 1 Düşüş) ---


def _atr_ver(monkeypatch, f, atr):
    """ATR14'ü elle verilen diziyle değiştirir: eşik tam sayıyla kurulur, kayan nokta payı kalmaz."""
    monkeypatch.setattr(
        gostergeler, "atr", lambda *a, **kw: pd.Series(atr, index=f.index)
    )


def _dusus_sinir_cercevesi(gun, yuksek):
    """Gün 0-21 kapanış 100, gün 22-39 kapanış 130, gün 40-42 kapanış 140; yüksek = kapanış + 1, düşük = kapanış - 1;
    yalnız `gun` günün yükseği `yuksek` (fitil)."""
    kapanis = [100.0] * 22 + [130.0] * 18 + [140.0] * 3
    yuk = [k + 1 for k in kapanis]
    yuk[gun] = yuksek
    return _mumlar(kapanis, yuksek=yuk)


# Çerçeve: `DUSUS` ayarı, "yukselis" çerçevesinin (yukarıda) kapanışları, gün 40-42 kapanışı 140. Dönem başı gün 25, dönem gün 25-39
# (J = -30, k = 4; yukarıdaki açıklama). Kutu alt = dönem en düşük düşüğü = 130 - 1 = 129. ATR14 elle verilir (sabit 2).
#   Eşik = kutu alt + 3 × ATR14 = 129 + 3 * 2 = 135. Pencere = dönem başından önceki 20 gün = gün 5-24 (25 - 20 = 5; son gün 24).
#   Tek fitilin yükseği pencerede tek aşan değerdir (öbür yükseklikler en çok 131 < 135). Kutu üstü 131 (fitil dönemde ise fitil);
#   gün 40 kapanış 140 üstte kalır: dönem sayılırsa sinyal gün 40, sayılmazsa sinyal yok.
# Eşik sınırı: pencere ortasında (gün 15) fitil 134 -> 134 < 135 sayılmaz; 135 -> 135 >= 135 sayılır (eşitlik); 136 -> sayılır.
@pytest.mark.parametrize(
    "yuksek, beklenen",
    [(134.0, []), (135.0, [40]), (136.0, [40])],
    ids=["esigin-altinda", "esitlik", "esigin-ustunde"],
)
def test_dusus_en_yuksek_yuksek_tam_esige_esitse_donem_sayilir(
    monkeypatch, yuksek, beklenen
):
    f = _dusus_sinir_cercevesi(15, yuksek)
    _atr_ver(monkeypatch, f, np.full(len(f), 2.0))
    assert _gunler(f, Parametre(dusus=True, **DUSUS)) == beklenen


# Pencere kenarları (fitil yüksek 135 = eşik, ATR 2): gün 5 pencerenin ilk günü -> sayılır; gün 4 pencerenin dışında -> sayılmaz;
# gün 24 pencerenin son günü -> sayılır; gün 25 dönem başı günü pencerenin dışında -> sayılmaz (pencere 20 gün: 5-24).
@pytest.mark.parametrize(
    "gun, beklenen",
    [(4, []), (5, [40]), (24, [40]), (25, [])],
    ids=["pencere-oncesi", "ilk-gun", "son-gun", "donem-basi-gunu"],
)
def test_dusus_penceresi_donem_basindan_onceki_tam_20_gun_donem_basi_gunu_haric(
    monkeypatch, gun, beklenen
):
    f = _dusus_sinir_cercevesi(gun, 135.0)
    _atr_ver(monkeypatch, f, np.full(len(f), 2.0))
    assert _gunler(f, Parametre(dusus=True, **DUSUS)) == beklenen


# ATR günü: fitil gün 15, yüksek 135. ATR14 dönem başı gününün (gün 25) değeridir; öbür günlerin ATR'si sonucu değiştirmemeli.
#   Gün 25 ATR 2, öbürleri 4: eşik 129 + 3 * 2 = 135 <= 135 -> sayılır. Gün 25 ATR 4, öbürleri 2: eşik 129 + 3 * 4 = 141 > 135 -> sayılmaz.
@pytest.mark.parametrize(
    "atr_bas, atr_diger, beklenen",
    [(2.0, 4.0, [40]), (4.0, 2.0, [])],
    ids=["bas-gunu-atr-kucuk", "bas-gunu-atr-buyuk"],
)
def test_dusus_atr_donem_basi_gununun_degeridir(
    monkeypatch, atr_bas, atr_diger, beklenen
):
    f = _dusus_sinir_cercevesi(15, 135.0)
    atr = np.full(len(f), atr_diger)
    atr[25] = atr_bas
    _atr_ver(monkeypatch, f, atr)
    assert _gunler(f, Parametre(dusus=True, **DUSUS)) == beklenen


def _dusus_agresif_sinir_cercevesi(gun, yuksek):
    """Gün 0-21 kapanış 96, gün 22-39 kapanış 100, gün 40-42 kapanış 103; yüksek = kapanış + 1, düşük = kapanış - 1;
    yalnız `gun` günün yükseği `yuksek` (fitil)."""
    kapanis = [96.0] * 22 + [100.0] * 18 + [103.0] * 3
    yuk = [k + 1 for k in kapanis]
    yuk[gun] = yuksek
    return _mumlar(kapanis, yuksek=yuk)


# Agresif giriş, aynı yardımcı (`donem_elenir`): `DUSUS` ayarı; gün 22'de sıçrama 96 -> 100: EMA2 gün 22 = 96 + 4 * 2/3 = 98,667, oran 0,0135 > eşik;
# gün 23: EMA2 = 100 - 4/9 = 99,556, oran 0,00446 <= 0,005 -> koşu başı gün 23; t = 26 (koşu 23-25, 3 gün); gün 26 düşük 99: kutu alt 99.
# ATR14 elle sabit 2: eşik = 99 + 3 * 2 = 105. Pencere = gün 3-22 (23 - 20 = 3). Fitil yüksek 105 = eşik: gün 3 ilk gün -> sayılır;
# gün 2 pencerenin dışında -> sayılmaz; gün 22 son gün -> sayılır; gün 23 koşu başı günü dışında -> sayılmaz.
# (Gün 0-21 koşusu 0'da başlar: koşu başı 0 < 20 -> `dusus` açıkken sayılmaz; sinyal yalnız gün 26'dan gelir.)
@pytest.mark.parametrize(
    "gun, beklenen",
    [(2, []), (3, [26]), (22, [26]), (23, [])],
    ids=["pencere-oncesi", "ilk-gun", "son-gun", "kosu-basi-gunu"],
)
def test_dusus_agresif_giriste_pencere_kosu_basindan_onceki_tam_20_gun(
    monkeypatch, gun, beklenen
):
    f = _dusus_agresif_sinir_cercevesi(gun, 105.0)
    _atr_ver(monkeypatch, f, np.full(len(f), 2.0))
    assert _gunler(f, Parametre(giris="agresif", dusus=True, **DUSUS)) == beklenen


# Karşı durum: agresif girişte koşu başında ATR14 hesaplanamıyorsa (NaN) süzgeç hesaplanamaz ve sinyal düşer (KURALLAR §3 Modül 1 Düşüş).
# Çerçeve "dusus-30" (agresif): ATR varken (3,659) sinyal gün 28 kalır (99 + 3 * 3,659 = 109,98 <= 131); `dusus` kapalıyken ATR NaN
# olsa da sinyaller [3, 28] aynıdır (ATR yalnız süzgeçte kullanılır); `dusus` açık ve ATR NaN: karşılaştırma yanlış, sinyal yok.
def test_dusus_agresif_giriste_kosu_basinda_atr_nan_ise_sinyal_duser(monkeypatch):
    f = _dusus_agresif_cercevesi(130.0, 99.0)
    agresif = Parametre(giris="agresif", dusus=True, **DUSUS)
    assert _gunler(f, agresif) == [28]
    _atr_ver(monkeypatch, f, np.full(len(f), np.nan))
    assert _gunler(f, Parametre(giris="agresif", dusus=False, **DUSUS)) == [3, 28]
    assert _gunler(f, agresif) == []


# Karşı durum: dönem başı tam 20. gün (konum 20) ilk günüdür ki 20 günlük pencere dolu (gün 0-19): süzgeç hesaplanır, dönem eksik gün
# yüzünden düşmez; konum 19'da pencere 19 gün olur, süzgeç hesaplanamaz ve dönem sayılmaz (KURALLAR §3 Modül 1 Düşüş).
# Çerçeve: gün 0-(a-1) kapanış 130, gün a-39 kapanış 100, gün 40-42 kapanış 103; yüksek = kapanış + 1, düşük = kapanış - 1.
# Atlama J = 30 (130 -> 100) gün a'da: EMA2 gün a+k-1 = 100 + 30/3^k; k = 4: 30/81 = 0,370, oran 0,00369 <= 0,005 (k = 3: 30/27 = 1,11,
# oran 0,011 > eşik) -> dönem başı a + 3. a = 17 -> 20; a = 16 -> 19. Kutu alt 99 (dönem düşükleri 99), kutu üstü 101; ATR14 elle sabit 2:
# eşik 99 + 3 * 2 = 105; dönem başından önceki günlerde yüksek 131 >= 105. Gün 40 kapanış 103 > 101 -> sinyal gün 40.
# (Gün 0-(a-1) düz dönemi: kapanış 130'dan sonra 100'e düşer, kutu üstünü geçmez, sinyal yok; dönem başı 0 < 20 de sayılmaz.)
@pytest.mark.parametrize(
    "atlama, beklenen",
    [(17, [40]), (16, [])],
    ids=["donem-basi-20", "donem-basi-19"],
)
def test_dusus_donem_basi_tam_20_gunden_baslar_19da_sayilmaz(
    monkeypatch, atlama, beklenen
):
    kapanis = [130.0] * atlama + [100.0] * (40 - atlama) + [103.0] * 3
    f = _mumlar(kapanis)
    _atr_ver(monkeypatch, f, np.full(len(f), 2.0))
    assert _gunler(f, Parametre(dusus=False, **DUSUS)) == [40]
    assert _gunler(f, Parametre(dusus=True, **DUSUS)) == beklenen


def _arz_secim_cercevesi():
    """48 gün; yüksek = kapanış + 1, düşük = kapanış - 1 (gün 42 yükseği 100). Gün 0-13 düz 100 (ATR 2), 14-17 yükseliş
    (105; 111; 118; 122), 18-21 düşüş (121; 113; 108; 104), 22 mum 107, 23-24 (106; 98), 25-27 yükseliş (105; 110; 114),
    28-31 (113; 104; 102; 100), 32 mum 103, 33-34 (102; 94), 35-44 düz 94, 45-47 kırılım (106; 112; 116)."""
    kapanis = [100.0] * 14
    kapanis += [105, 111, 118, 122, 121, 113, 108, 104, 107, 106, 98, 105, 110, 114]
    kapanis += [113, 104, 102, 100, 103, 102] + [94] * 11 + [106, 112, 116]
    yuksek = [k + 1 for k in kapanis]
    yuksek[42] = 100.0  # fitil: kutu üstü tam 100
    return _mumlar(kapanis, yuksek)


# Arz bölgeleri (hepsi gün 17, 22, 27, 32 mumlarından; proximal = mumdan önceki kapanış, distal = mum yüksek):
#   A: gün 17 (122), proximal 118, distal 123; ATR17 ~ 3,1 (gerçek aralıklar gün 14-17: 6, 7, 8, 5; öncesi 2): gün 19 kapanışı
#      113 <= 118 - 3,1 -> bilinen gün 19, aktif (bozulma yok).
#   C: gün 22 (107), proximal 104, distal 108; gün 24 kapanışı 98 <= 104 - ATR (ATR < 6) -> bilinen gün 24; gün 26 kapanışı 110 > 108 -> BİTER.
#   B: gün 27 (114), proximal 110, distal 115; gün 29 kapanışı 104 <= 110 - ATR (ATR < 6) -> bilinen gün 29, aktif.
#   D: gün 32 (103), proximal 100, distal 104; gün 34 kapanışı 94 <= 100 - ATR (ATR < 6) -> bilinen gün 34, aktif.
# Her mum bir önceki kapanışın üstünde (yeşil), ertesi gün kapanış yükselmez; öbür yükseliş günleri (14-16, 25-26) ertesi gün de
# yeşildir, bölge doğurmaz.
# Sıkışma dönemi: düz 94 günlerinde oran (EMA2 ile EMA3 arası) gün 38'de eşiğin (0,004) altına iner ve gün 44'e dek altındadır:
# dönem gün 38-44 (gün 45 kapanışı 106 oranı eşiğin üstüne çıkarır). Kutu üstü 100 (gün 42 fitili), kutu altı 93.
# Dönem bitişinde (gün 44) aktif: A, B, D. C bitmiştir -> yok sayılır.
# Kutu üstünden büyük proximal: A (118) ve B (110). D'nin proximal'ı 100 = kutu üstü: "büyük" değil -> yok sayılır.
# En küçük proximal: B -> distal 115. Gün 45 (106), 46 (112) <= 115; gün 47 (116) > 115 -> sinyal gün 47.
# Yanlış okumalar: C dahil -> distal 108 -> gün 46; D dahil (>=) -> distal 104 -> gün 45; en büyük proximal (A) -> 123 -> sinyal yok.
def test_giris_arz_en_kucuk_proximal_aktif_bolge_biten_ve_esit_proximal_yok_sayilir():
    f = _arz_secim_cercevesi()
    ayar = dict(KUCUK, sma_n=1)
    z = aileler.bolgeler(f, "arz")
    assert list(zip(z["proximal"], z["distal"], strict=True)) == [
        (118.0, 123.0),
        (104.0, 108.0),
        (110.0, 115.0),
        (100.0, 104.0),
    ]
    # Bitişler: A yok; C gün 26 (dönem bitişinden önce); D gün 45 ve B gün 47 (dönem bitişinden sonra, pencerede)
    bitis = [None if pd.isna(b) else f.index.get_loc(b) for b in z["bitis"]]
    assert bitis == [None, 26, 47, 45]
    assert _gunler(f, Parametre(giris="kutu", **ayar)) == [14, 45]
    p = Parametre(giris="arz", **ayar)
    assert _gunler(f, p) == [47]
    k = aileler.kurulum(f, p).iloc[0]
    assert (k["kutu_alt"], k["kutu_ust"]) == (93.0, 100.0)


# Üçgen: dönem gün 0-12 (kapanış 100). Salınım tepeleri gün 2 (105), 6 (105,8), 10 (105,4): 105,8 ve 105,4 <= 105 * 1,01 = 106,05.
# Dipler gün 3 (96), 6 (97), 9 (98): yükseliyor. Pencere gün 13, 14, 15. Kapanışlar 105,5; 105,7; 105,9.
# İlk ve SON tepeden geçen çizgi (gün 2, 105) - (gün 10, 105,4): eğim 0,4/8 = 0,05; değer(t) = 105,4 + 0,05 (t - 10):
#   gün 13 = 105,55; gün 14 = 105,6; gün 15 = 105,65. 105,5 > 105,55 hayır; 105,7 > 105,6 evet -> sinyal gün 14.
# İlk iki tepeden geçen çizgi (gün 2) - (gün 6, 105,8): eğim 0,2; değer(t) = 105,8 + 0,2 (t - 6): gün 13 = 107,2; gün 14 = 107,4;
#   gün 15 = 107,6 -> hiçbir kapanış geçmez -> sinyal yok.
# Son iki tepeden geçen çizgi (gün 6) - (gün 10): eğim -0,4/4 = -0,1; değer(t) = 105,4 - 0,1 (t - 10): gün 13 = 105,1 -> 105,5 > 105,1 -> gün 13.
# `kutu` (kutu üstü 105,8): yalnız gün 15 (105,9 > 105,8).
def test_giris_ucgen_ust_cizgi_ilk_ve_son_tepeden_gecer_uc_tepeyle_ayirt_edilir():
    yuk = [101.0] * 13 + [106.0, 106.2, 106.4]
    yuk[2], yuk[6], yuk[10] = 105.0, 105.8, 105.4
    dus = [99.0] * 13 + [104.5, 104.7, 104.9]
    dus[3], dus[6], dus[9] = 96.0, 97.0, 98.0
    f = _mumlar([100.0] * 13 + [105.5, 105.7, 105.9], yuk, dus)
    ayar = dict(KUCUK, sma_n=1)
    assert _gunler(f, Parametre(giris="kutu", **ayar)) == [15]
    p = Parametre(giris="ucgen", **ayar)
    assert _gunler(f, p) == [14]
    k = aileler.kurulum(f, p).iloc[0]
    assert (k["kutu_alt"], k["kutu_ust"]) == (96.0, 105.8)


# Dönem başı ilk gün olup serinin ilk günü değilse gövde ucu önceki kapanışı kullanır (KURALLAR §3 Modül 1, Kutu).
# Ayar `DUSUS`: periyotlar (1, 2) (EMA1 = kapanış, EMA2 alfa 2/3), oran = |kapanış - EMA2| / EMA2, eşik 0,005, en az 3 gün, pencere 3.
# Kapanış: gün 0-21 130; gün 22-24 100; gün 25 99,9; gün 26-30 100; gün 31-33 101,6; 101,7; 101,8. Yüksek = kapanış + 1,
# düşük = kapanış - 1, ama gün 25 yükseği 102 (dönemin en yüksek günü; ilk gün).
# 130 -> 100 sıçramasında EMA2 farkı her gün üçte birine iner: gün 22 = 10; gün 23 = 3,33; gün 24 = 1,11 (EMA2 101,11).
#   Oranlar: gün 22 = 0,091; gün 23 = 0,032; gün 24 = 1,11 / 101,11 = 0,011 > 0,005. Gün 25: EMA2 = (2/3) 99,9 + (1/3) 101,11 =
#   100,3037; oran = (100,3037 - 99,9) / 100,3037 = 0,00402 <= 0,005 -> dönem başı gün 25 (serinin ilk günü değil).
# Gün 26-30 oranı daha küçük (EMA2 farkı 0,10; 0,034; 0,011; 0,0037; 0,0012). Gün 31: EMA2 = 101,6 - (101,6 - 100,0012) / 3 = 101,067;
#   oran = (101,6 - 101,067) / 101,067 = 0,00527 > 0,005 -> dönem gün 25-30'da biter. Pencere gün 31, 32, 33.
# Gövde ucu = max(önceki kapanış, kapanış) = max(100; 99,9) = 100 (kapanış tek başına 99,9 olurdu). Gün 0-21 dönemi: kutu üstü
# 130 (ilk gün: önceki kapanış yok -> kapanış), kapanışlar 100 -> sinyal yok.
# govde: kutu üstü 100; gün 31 kapanışı 101,6 > 100 -> sinyal gün 31, kutu_ust 100. yuksek: kutu üstü 102; 101,6; 101,7; 101,8 <= 102 -> yok.
def test_kutu_ust_govde_donem_ilk_gunu_serinin_ilk_gunu_degilse_onceki_kapanis_kullanilir():
    kapanis = [130.0] * 22 + [100.0] * 3 + [99.9] + [100.0] * 5 + [101.6, 101.7, 101.8]
    yuksek = [k + 1 for k in kapanis]
    yuksek[25] = 102.0
    f = _mumlar(kapanis, yuksek)
    ayar = dict(DUSUS, sma_n=1)
    assert _gunler(f, Parametre(giris="kutu", kutu_ust="yuksek", **ayar)) == []
    govde = Parametre(giris="kutu", kutu_ust="govde", **ayar)
    assert _gunler(f, govde) == [31]
    k = aileler.kurulum(f, govde).iloc[0]
    assert (k["kutu_alt"], k["kutu_ust"]) == (pytest.approx(98.9), 100.0)


@pytest.mark.parametrize("sayisal", [{}, {"esik": 0.01, "min_gun": 4, "pencere": 8}])
def test_s10_toplu_kurulum_gunluk_kurulumla_ayni(sayisal):
    f = _mumlar(
        [100.0] * 510 + [110.0, 112.0],
        [101.0] * 510 + [111.0, 113.0],
        [99.0] * 510 + [100.0, 110.0],
        [100.0] * 512,
    )
    f["aof"] = f["kapanis"]
    paket = _ortak_paket(f)
    strateji = aileler.legacy_coz("bugun", sayisal_ayarlar=sayisal)
    toplu = aileler.ortak_donem_kurulumu(paket, strateji)
    assert "TEST" in toplu, "Toplu E2 sonucu sembolün ortak hesabını taşımalı"
    for tarih in f.index[-3:]:
        gunluk = aileler.ortak_kurulum(paket, tarih, strateji)
        sinyaller = [
            s for s in toplu["TEST"]["sinyaller"] if s["tarih"] == str(tarih.date())
        ]
        for grup in (sinyaller, gunluk["sinyaller"]):
            for s in grup:
                s.pop("olusturma_zamani")
        assert sinyaller == gunluk["sinyaller"]
        for g in gunluk["gostergeler"]:
            deger = toplu["TEST"]["mumlar"].at[tarih, g["ad"]]
            assert (None if pd.isna(deger) else deger) == g["deger"]
        assert toplu["TEST"]["isinma"].at[tarih] == gunluk["isinma"]["TEST"]["gozlem"]


@pytest.mark.parametrize(
    "gunler,bas,son,secilen",
    [
        ([499, 503, 501, 501, 505, 502], 500, 507, [1, 2, 3, 4, 5]),
        ([499, 503, 501, 501, 505, 502], 501, 505, [1, 2, 3, 4, 5]),
        ([499, 503, 501, 501, 505, 502], 506, 507, []),
        ([], 500, 507, []),
        ([499, 501, 502, 503], 501, 503, [1, 2, 3]),
    ],
    ids=["eksik-sinirlar", "dahil-sinirlar", "donemde-yok", "bos", "eski-sirali"],
)
def test_ortak_donem_kurulumu_tarih_uyeligi_sira_ve_tekrari_korur(
    monkeypatch, gunler, bas, son, secilen
):
    f = _mumlar([100.0] * 512)
    f["aof"] = f["kapanis"]
    paket = _ortak_paket(f)
    paket["referans"]["istenen_donem"] = {
        "baslangic": str(f.index[bas].date()),
        "bitis": str(f.index[son].date()),
    }
    # Kurulum sahibinin dönem sırası sözleşmesi; tarih seçimi bu sınırda sınanır.
    k = pd.DataFrame(
        {
            "kutu_alt": [90.0 + i for i in range(len(gunler))],
            "kutu_ust": [110.0 + i for i in range(len(gunler))],
            "hedef": [np.nan] * len(gunler),
        },
        index=f.index[gunler],
    )
    korunacak = k.copy(deep=True)
    monkeypatch.setattr(aileler, "kurulum", lambda *a: k)
    strateji = aileler.legacy_coz("bugun")
    hata = None
    try:
        sonuc = aileler.ortak_donem_kurulumu(paket, strateji)["TEST"]
    except KeyError as exc:
        hata = exc
    assert hata is None, f"Geçerli kurulumda tarih üyeliği seçilemedi: {hata}"
    pd.testing.assert_frame_equal(sonuc["kurulum"], korunacak.iloc[secilen])
    pd.testing.assert_frame_equal(k, korunacak)
    assert [s["tarih"] for s in sonuc["sinyaller"]] == [
        str(f.index[gunler[i]].date()) for i in secilen
    ]
    assert [s["kayit_id"] for s in sonuc["sinyaller"]] == [
        f"TEST:{f.index[gunler[i]].date()}:{i}:{strateji.ayar_parmak_izi}"
        for i in secilen
    ]
    assert [s["kutu_alt"]["deger"] for s in sonuc["sinyaller"]] == [
        90.0 + i for i in secilen
    ]


@pytest.mark.parametrize(
    "bas,son",
    [("NaT", "2028-03-01"), ("2028-03-01", "NaT"), ("2028-03-02", "2028-03-01")],
)
def test_ortak_donem_kurulumu_gecersiz_donemi_reddeder(bas, son):
    f = _mumlar([100.0] * 512)
    f["aof"] = f["kapanis"]
    paket = _ortak_paket(f)
    paket["referans"]["istenen_donem"] = {"baslangic": bas, "bitis": son}
    with pytest.raises(ValueError, match="Kurulum dönemi geçersiz"):
        aileler.ortak_donem_kurulumu(paket, aileler.legacy_coz("bugun"))


@pytest.mark.parametrize("tekrar", [False, True], ids=["sirasiz", "tekrar"])
def test_ortak_donem_kurulumu_gecersiz_piyasa_tarihlerini_reddeder(tekrar):
    f = _mumlar([100.0] * 512)
    f["aof"] = f["kapanis"]
    paket = _ortak_paket(f)
    if tekrar:
        paket["piyasa"].insert(1, paket["piyasa"][0].copy())
    else:
        paket["piyasa"][0], paket["piyasa"][1] = (
            paket["piyasa"][1],
            paket["piyasa"][0],
        )
    with pytest.raises(ValueError, match="Piyasa tarihleri sıralı ve tekil olmalı"):
        aileler.ortak_donem_kurulumu(paket, aileler.legacy_coz("bugun"))
