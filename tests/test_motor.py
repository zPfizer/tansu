"""Adım/Motor yüzü: TASARIM 5.3 eski senaryoları ve 5.15 S09 geçişi, sentetik mumlarla.

Eski senaryoların beklenen değerlerini kodu görmemiş ayrı bir ajan yalnız kural metninden ve bu senaryo verisinden elle hesapladı
(bilet 08). Hesabın özeti her senaryonun yorumundadır. Adet = 1; boyutlandırma bilet 10'dadır.
Eski politika özeti: sinyal kapanışta, giriş ertesi gün AOF'ta; stop = giriş - 2 ATR; giriş günü yalnız stop;
dolum min(stop, AOF); kilitli tavanda giriş yok (sinyal düşer); kilitli tabanda çıkış kayar;
kapanış < SMA250 -> ertesi gün AOF'ta çıkış; veri bitince son kapanıştan çıkış.
Satır: (AOF, yüksek, düşük, kapanış, bayraklar). Beklenen: (giriş günü, giriş, çıkış günü, çıkış, neden,
planlanan risk, gerçekleşen kayıp).
"""

from dataclasses import replace
import json

import numpy as np
import pandas as pd
import pytest

from tansu import aileler, denetim, gostergeler, motor, veri

GUNLER = pd.bdate_range("2026-03-02", periods=10)
STD = (100, 101, 99, 100)


def s09_istek(**degisiklik):
    return (
        dict(
            surum="bagimsiz_islem_v1",
            aile="ema_sikismasi",
            strateji_id="ema-test",
            strateji_surumu="v1",
            deneme_id="deneme-1",
            kosu_id="kosu-1",
            veri_ref_id="veri-1",
            sembol="TEST",
            nominal_tutar=8000,
            risk_surumu="bagimsiz_risk_v1",
            masraf_surumu="komisyon_bsmv_v1",
            fiyat_politikasi="aof_v1",
        )
        | degisiklik
    )


def s09_mumlar(satirlar=None):
    df = _mumlar(satirlar or [r(*STD), r(*STD)], 5)
    df = df.astype({k: float for k in ("aof", "yuksek", "dusuk", "kapanis")})
    df["ham_yuksek"] = df.yuksek
    df["ham_dusuk"] = df.dusuk
    df["tavan"] = 200.0
    df["taban"] = 50.0
    df["limit_kaniti"] = "sentetik-tarihli-limit"
    return df


@pytest.mark.parametrize("kilit_politikasi", [None, "ham_aralik_v1"])
def test_s09_sonraki_seansta_bagimsiz_risk_adediyle_girer(kilit_politikasi):
    m = s09_mumlar()
    secim = {}
    if kilit_politikasi is not None:
        secim["kilit_politikasi"] = kilit_politikasi
        m = m.drop(columns=["tavan", "taban", "limit_kaniti"])
    sonuc = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek(**secim))
    assert [(d["yon"], d["adet"], d["fiyat"]) for d in sonuc["dolumlar"]] == [
        ("alis", 15, 100)
    ]
    assert sonuc["durum"] == "acik_son"
    assert sonuc["sonuc"]["ilk_risk"] == pytest.approx(154.48875)
    assert sonuc["sonuc"]["net_r"] is None
    assert sonuc["pozisyon"]["cikis_fiyat"] is None
    assert sonuc["iz"][-1]["egri_turu"] == "tani_referans"
    assert sonuc["iz"][-1]["nominal_tutar"] == 8000


def test_s09_toplu_ve_json_gunluk_ayni_ve_tekrar_idempotent():
    m = s09_mumlar([r(*STD), r(*STD), r(80, 82, 79, 81)])
    sinyaller = {m.index[0]: "sinyal-1"}
    toplu = motor.tara(m, sinyaller, yurutme=s09_istek())
    gunluk = None
    for t, satir in m.iterrows():
        once = json.loads(json.dumps(gunluk))
        mum = dict(satir) | {"tarih": t}
        gunluk = motor.islem_adimi(once, mum, sinyaller.get(t), yurutme=s09_istek())
        assert (
            motor.islem_adimi(gunluk, mum, sinyaller.get(t), yurutme=s09_istek())
            == gunluk
        )
    assert gunluk == toplu
    assert [d["adet"] for d in toplu["islemler"][0]["dolumlar"]] == [15, 15]
    assert toplu["islemler"][0]["sonuc"]["net_sonuc"] == pytest.approx(-304.2525)
    with pytest.raises(ValueError, match="çelişkili"):
        motor.islem_adimi(gunluk, mum | {"aof": 81}, yurutme=s09_istek())
    with pytest.raises(ValueError, match="uyuşmuyor"):
        motor.islem_adimi(gunluk, mum, yurutme=s09_istek(veri_ref_id="farkli"))
    bozuk = json.loads(json.dumps(gunluk))
    bozuk["islemler"][0]["dolumlar"][0]["adet"] = 1000
    with pytest.raises(ValueError, match="uyuşmuyor"):
        motor.islem_adimi(bozuk, mum, yurutme=s09_istek())


@pytest.mark.parametrize("ilk_satir", [1, 2], ids=["bekleyen", "acik"])
def test_s09_kayitli_bimas_yuvarlama_payi_fiyat_ve_kimligi_degistirmez(ilk_satir):
    m = s09_mumlar([r(32, 33, 31, 32)] * ilk_satir)
    m["sma250"] = 20.0
    m["taban"] = 10.0
    yurutme = s09_istek(sembol="BIMAS")
    ilk = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=yurutme)
    assert ilk["pozisyon"]["durum"] == ("bekliyor" if ilk_satir == 1 else "acik")
    once = json.loads(json.dumps(ilk))
    mum = dict(m.iloc[-1]) | dict(
        tarih=GUNLER[ilk_satir],
        aof=32.209248,
        yuksek=32.538864,
        dusuk=31.968382,
        kapanis=32.5389,
        ham_yuksek=77.0,
        ham_dusuk=75.65,
    )
    girdi = dict(mum)
    hata = None
    try:
        son = motor.islem_adimi(ilk, mum, yurutme=yurutme)
    except ValueError as exc:
        hata = str(exc)
    assert hata is None, f"Kayıtlı yuvarlama payı reddedildi: {hata}"
    assert mum == girdi
    assert ilk == once
    assert son["degerleme"]["fiyat"] == 32.5389
    assert son["yurutme"] == ilk["yurutme"]
    for alan, deger in ilk["pozisyon"]["risk_girdisi"].items():
        assert son["pozisyon"]["risk_girdisi"][alan] == deger
    assert [d["fiyat"] for d in son["dolumlar"]] == [
        32.209248 if ilk_satir == 1 else 32.0
    ]
    assert motor.islem_adimi(json.loads(json.dumps(son)), mum, yurutme=yurutme) == son


@pytest.mark.parametrize("alan", ["aof", "kapanis"])
@pytest.mark.parametrize(
    "fiyat,gecerli",
    [(99.99, True), (100.01, True), (99.9899, False), (100.0101, False)],
)
def test_s09_duzeltilmis_fiyat_yuvarlama_siniri(alan, fiyat, gecerli):
    m = s09_mumlar([r(100, 100, 100, 100)] * 2)
    m.at[m.index[1], alan] = fiyat
    if not gecerli:
        with pytest.raises(ValueError, match="mum fiyat sırası geçersiz"):
            motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
        return
    son = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
    assert [d["fiyat"] for d in son["dolumlar"]] == [fiyat if alan == "aof" else 100.0]
    assert son["degerleme"]["fiyat"] == (fiyat if alan == "kapanis" else 100.0)


@pytest.mark.parametrize("kapanis,gecerli", [(0.4082, True), (0.4076, False)])
def test_s09_dusuk_fiyatta_yarim_birim_yuvarlama_payi(kapanis, gecerli):
    # TASARIM 5.13 (#267): düşük 0,408246, kapanış 0,4082 (4 ondalık, fark 4,6e-5 < 5e-5) geçerlidir; bağıl 1e-4
    # pay yalnız 4,1e-5 tanır. 0,4076 (düşükten %0,16 aşağı) gerçek ihlaldir.
    m = s09_mumlar([r(0.408246, 0.421968, 0.408246, 0.408246)] * 2)
    m["tavan"], m["taban"], m["atr"], m["sma250"] = 1.0, 0.1, 0.01, 0.2
    m.at[m.index[1], "kapanis"] = kapanis
    if not gecerli:
        with pytest.raises(ValueError, match="mum fiyat sırası geçersiz"):
            motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
        return
    son = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
    assert [d["fiyat"] for d in son["dolumlar"]] == [0.408246]
    assert son["degerleme"]["fiyat"] == 0.4082


@pytest.mark.parametrize("secim", [{}, {"kilit_politikasi": "ham_aralik_v1"}])
def test_s09_ham_limit_sirasina_yuvarlama_payi_uygulanmaz(secim):
    m = s09_mumlar()
    m.at[m.index[1], "tavan"] = 100.9999
    with pytest.raises(ValueError, match="ham fiyat veya limit sırası geçersiz"):
        motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek(**secim))


@pytest.mark.parametrize("secim", [{}, {"kilit_politikasi": "ham_aralik_v1"}])
@pytest.mark.parametrize(
    "nominal, miktarlar, fiyatlar, masraf, net",
    [
        (8000, [15, 7, 8], [100, 115, 80], 4.638375, -59.638375),
        (600, [1, 1], [100, 80], 0.2835, -20.2835),
    ],
)
def test_s09_yari_adet_asagi_kalan_korunur(
    nominal, miktarlar, fiyatlar, masraf, net, secim
):
    m = s09_mumlar(
        [
            r(*STD),
            r(*STD),
            r(114, 115, 110, 114),
            r(118, 120, 116, 118),
            r(80, 82, 79, 81),
        ]
    )
    if secim:
        m = m.drop(columns=["tavan", "taban", "limit_kaniti"])
    sonuc = motor.tara(
        m,
        {m.index[0]: "sinyal-1"},
        replace(aileler.Parametre(), cikis="atr3"),
        yurutme=s09_istek(nominal_tutar=nominal, **secim),
    )
    islem = sonuc["islemler"][0]
    assert [d["adet"] for d in islem["dolumlar"]] == miktarlar
    assert [d["fiyat"] for d in islem["dolumlar"]] == fiyatlar
    assert islem["sonuc"]["gerceklesen_maliyet"] == pytest.approx(masraf)
    assert islem["sonuc"]["net_sonuc"] == pytest.approx(net)
    assert islem["sonuc"]["kalan_adet"] == 0
    assert islem["pozisyon"]["ilk_stop"] == 90
    if nominal == 600:
        assert islem["pozisyon"]["yari_tarih"] is None
        assert islem["pozisyon"]["yari_fiyat"] is None
        assert "yari_adet_sifir" in [r["neden"] for r in sonuc["retler"]]
    else:
        assert islem["sonuc"]["gerceklesen_kismi_sonuclar"][0][
            "net_sonuc"
        ] == pytest.approx(102.629625)


@pytest.mark.parametrize(
    "engel,neden",
    [
        ("ust", "kilitli_tavan"),
        ("bilinmiyor", "limit_bilinmiyor"),
        ("gecersiz", "gecersiz_fiyat"),
        ("eksik", "gecersiz_fiyat"),
        ("nan", "gecersiz_fiyat"),
        ("sifir", "gecersiz_fiyat"),
        ("negatif", "gecersiz_fiyat"),
        ("karantina", "karantina"),
        ("islem_yok", "islem_yok"),
    ],
)
@pytest.mark.parametrize("secim", [{}, {"kilit_politikasi": "ham_aralik_v1"}])
def test_s09_giris_engeli_dolum_uretmez(engel, neden, secim):
    m = s09_mumlar()
    t = m.index[1]
    if engel == "ust":
        m.loc[t, ["ham_yuksek", "ham_dusuk", "tavan"]] = 110
    elif engel == "bilinmiyor":
        m["limit_kaniti"] = m["limit_kaniti"].astype(object)
        m.loc[t, "limit_kaniti"] = None
    elif engel == "gecersiz":
        m.loc[t, "aof"] = float("inf")
    elif engel == "eksik":
        m = m.drop(columns=["aof"])
    elif engel in ("nan", "sifir", "negatif"):
        m.loc[t, "aof"] = {"nan": float("nan"), "sifir": 0, "negatif": -1}[engel]
    elif engel == "karantina":
        m.loc[t, "karantina"] = True
    else:
        m.loc[t, "islem"] = False
    sonuc = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek(**secim))
    assert sonuc["dolumlar"] == []
    assert sonuc["pozisyon"] is None
    assert sonuc["retler"][0]["neden"] == neden
    assert sonuc["dusen_sinyal_sayisi"] == 1
    assert sonuc["retler"][0]["sinyal_id"] == "sinyal-1"


def test_s09_eski_kapanis_bayragi_tam_gun_kilidi_sayilmaz():
    m = s09_mumlar()
    m.loc[m.index[1], "kilit_tavan"] = True
    sonuc = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
    assert sonuc["sonuc"]["alinan_adet"] == 15


def test_s09_ardisik_taban_satisi_bekletir_her_gunu_sayar():
    m = s09_mumlar(
        [
            r(*STD),
            r(*STD),
            r(90, 90, 90, 90),
            r(85, 85, 85, 85),
            r(80, 82, 79, 81),
        ]
    )
    m.loc[m.index[2:4], "taban"] = [90, 85]
    sonuc = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
    islem = sonuc["islemler"][0]
    assert [d["fiyat"] for d in islem["dolumlar"]] == [100, 80]
    assert len([r for r in sonuc["retler"] if r["neden"] == "satis_engeli"]) == 2
    assert sonuc["ertelenen_satis_gunu_sayisi"] == 2
    assert islem["sonuc"]["ilk_risk"] == pytest.approx(154.48875)


def test_s09_karantina_degerleme_satis_degil_ayar_donuk():
    m = s09_mumlar(
        [
            r(*STD),
            r(*STD),
            r(1, 2, 1, 1, karantina=True),
            r(101, 102, 100, 101),
        ]
    )
    ilk = motor.tara(m.iloc[:2], {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
    ara = motor.tara(
        m.iloc[2:3],
        {m.index[2]: "sinyal-2"},
        replace(aileler.Parametre(), stop="atr15"),
        yurutme=s09_istek(),
        onceki_durum=ilk,
    )
    assert len(ara["dolumlar"]) == 1
    assert ara["degerleme"] == {"tarih": "2026-03-03", "fiyat": 100}
    assert ara["pozisyon"]["ayar"]["stop"] == "atr2"
    assert (
        ara["pozisyon"]["risk_girdisi"]["ayar_parmak_izi"]
        == ilk["pozisyon"]["risk_girdisi"]["ayar_parmak_izi"]
    )
    assert ara["pozisyon"]["bekleyen"] == "karantina"
    assert [r["neden"] for r in ara["retler"]] == [
        "ayar_degisti",
        "karantina_cikis_bekliyor",
        "acik_islem",
    ]
    son = motor.tara(m.iloc[3:], {}, yurutme=s09_istek(), onceki_durum=ara)
    assert son["islemler"][0]["dolumlar"][-1]["fiyat"] == 101
    assert son["islemler"][0]["pozisyon"]["neden"] == "karantina"


def test_s09_son_gun_sinyali_bekler_butce_ve_cift_engeli():
    m = s09_mumlar()
    son = motor.tara(m.iloc[:1], {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
    assert son["durum"] == "bekliyor"
    assert son["dolumlar"] == []
    yetersiz = motor.tara(
        m,
        {m.index[0]: "sinyal-1"},
        yurutme=s09_istek(nominal_tutar=1),
    )
    assert yetersiz["retler"][0]["neden"] == "butce_yetersiz"
    assert yetersiz["dolumlar"] == []
    with pytest.raises(ValueError, match="risk_dayanagi_eksik"):
        motor.tara(m, {}, yurutme=s09_istek(aile="cift_rotasyonu"))
    with pytest.raises(ValueError, match="nominal_tutar"):
        motor.tara(m, {}, yurutme=s09_istek(nominal_tutar=None))


def test_s09_bilinmeyen_limit_stop_dolumunu_erteleyip_izi_korur():
    m = s09_mumlar(
        [
            r(*STD),
            r(*STD),
            r(80, 82, 79, 81),
            r(85, 87, 84, 86),
        ]
    )
    m.loc[m.index[2], "limit_kaniti"] = None
    sonuc = motor.tara(m, {m.index[0]: "sinyal-1"}, yurutme=s09_istek())
    dolumlar = sonuc["islemler"][0]["dolumlar"]
    assert [d["fiyat"] for d in dolumlar] == [100, 85]
    assert dolumlar[-1]["tarih"] == "2026-03-05"
    assert [r["neden"] for r in sonuc["retler"]] == [
        "limit_bilinmiyor",
        "satis_engeli",
    ]


def test_s09_karantina_penceresi_json_durumunda_tasinir():
    m = s09_mumlar([r(*STD, karantina=True)] + [r(*STD)] * 251)
    sinyaller = {m.index[249]: "erken", m.index[250]: "izinli"}
    sonuc = motor.tara(m, sinyaller, yurutme=s09_istek())
    assert [(r["sinyal_id"], r["neden"]) for r in sonuc["retler"]] == [
        ("erken", "karantina_penceresi")
    ]
    assert sonuc["dolumlar"][0]["sinyal_id"] == "izinli"
    assert sonuc["dolumlar"][0]["tarih"] == m.index[251].date().isoformat()


def test_s09_json_sinyal_tarihi_ve_sembol_dolum_kimligi():
    m = s09_mumlar()
    sinyaller = {"2026-03-02": "ortak-sinyal-etiketi"}
    a = motor.tara(m, sinyaller, yurutme=s09_istek(sembol="A"))
    b = motor.tara(m, sinyaller, yurutme=s09_istek(sembol="B"))
    assert a["sonuc"]["alinan_adet"] == b["sonuc"]["alinan_adet"] == 15
    assert a["dolumlar"][0]["dolum_id"] != b["dolumlar"][0]["dolum_id"]
    assert a["dolumlar"][0]["islem_id"] != b["dolumlar"][0]["islem_id"]
    with pytest.raises(ValueError, match="takvim günü"):
        motor.islem_adimi(
            None,
            dict(m.iloc[0]) | {"tarih": pd.Timestamp("2026-03-02 12:00")},
            yurutme=s09_istek(),
        )


def test_s09_atr_sifir_kutu_stopuyla_gecerli_riski_engellemez():
    m = s09_mumlar()
    m["atr"] = 0.0
    kurulum = pd.DataFrame({"kutu_alt": [90], "hedef": [None]}, index=m.index[:1])
    sonuc = motor.tara(
        m,
        {m.index[0]: "sinyal-1"},
        replace(aileler.Parametre(), stop="kutu"),
        kurulum,
        yurutme=s09_istek(),
    )
    assert sonuc["sonuc"]["alinan_adet"] == 15
    assert sonuc["sonuc"]["ilk_risk"] == pytest.approx(154.48875)


def test_s09_bekleyen_yari_dolum_yeni_gosterge_istemeden_islenir():
    m = s09_mumlar(
        [
            r(*STD),
            r(*STD),
            r(109, 110, 108, 109),
            r(105, 106, 104, 105),
            r(106, 107, 105, 106),
        ]
    )
    m["rsi"] = 60.0
    m["onceki_rsi"] = 60.0
    m["sma50"] = 100.0
    m["onceki_dusuk"] = 106.0
    m.loc[m.index[-1], "rsi"] = float("nan")
    sonuc = motor.tara(
        m,
        {m.index[0]: "sinyal-1"},
        replace(aileler.Parametre(), cikis="dip"),
        yurutme=s09_istek(),
    )
    assert [(d["yon"], d["adet"], d["fiyat"]) for d in sonuc["dolumlar"]] == [
        ("alis", 15, 100),
        ("satis", 7, 106),
    ]
    assert sonuc["sonuc"]["kalan_adet"] == 8


@pytest.mark.parametrize("stoplar", [[90, 95], [95, 90], [90, 90]])
def test_s09_tekrarlanan_kurulum_gunu_reddedilir(stoplar):
    m = s09_mumlar()
    k = pd.DataFrame(
        {"kutu_alt": stoplar, "hedef": [None, None]}, index=[m.index[0]] * 2
    )
    hata = None
    try:
        motor.tara(
            m,
            {m.index[0]: "s"},
            replace(aileler.Parametre(), stop="kutu"),
            k,
            yurutme=s09_istek(),
        )
    except ValueError as exc:
        hata = str(exc)
    assert hata is not None and "kurulum" in hata


@pytest.mark.parametrize(
    "cikis,eksik,beklenen",
    [
        ("dip", ["rsi", "onceki_rsi", "sma50"], [("alis", 15, 100), ("satis", 7, 106)]),
        ("dip", ["sma250"], [("alis", 15, 100), ("satis", 7, 106)]),
        ("rsi70", ["rsi"], [("alis", 15, 100), ("satis", 15, 105)]),
        ("rsi50", ["rsi"], [("alis", 15, 100), ("satis", 7, 105)]),
    ],
)
def test_s09_bagimsiz_karar_eksik_ilgisiz_gostergeyle_engellenmez(
    cikis, eksik, beklenen
):
    m = s09_mumlar(
        [
            r(*STD),
            r(*STD),
            r(109, 110, 108, 109),
            r(105, 106, 104, 105),
            r(106, 107, 105, 106),
        ]
    )
    m["rsi"] = 60.0
    m["onceki_rsi"] = 60.0
    m["sma50"] = 100.0
    m["onceki_dusuk"] = 106.0
    if cikis == "rsi70":
        m["sma250"] = 120.0
        m = m.iloc[:4]
    if cikis == "rsi50":
        m["sma50"] = 109.5
        m = m.iloc[:4]
    m = m.drop(columns=eksik)
    d = motor.tara(
        m,
        {m.index[0]: "s"},
        replace(aileler.Parametre(), cikis=cikis),
        yurutme=s09_istek(),
    )
    dolumlar = d["islemler"][0]["dolumlar"] if d["islemler"] else d["dolumlar"]
    assert [(x["yon"], x["adet"], x["fiyat"]) for x in dolumlar] == beklenen


@pytest.mark.parametrize(
    "ayar",
    [
        replace(aileler.Parametre(), stop="kutu"),
        replace(aileler.Parametre(), hedef="tansu"),
        replace(aileler.Parametre(), stop="kutu", hedef="tansu"),
    ],
)
def test_s09_gerekli_kurulum_eksikse_dolum_yok(ayar):
    m = s09_mumlar()
    d = motor.tara(m, {m.index[0]: "s"}, ayar, yurutme=s09_istek())
    assert d["dolumlar"] == []
    assert d["retler"][0]["neden"] == "kurulum_eksik"
    k = pd.DataFrame({"kutu_alt": [90], "hedef": [120]}, index=["2026-03-02"])
    gecerli = motor.tara(m, {m.index[0]: "s"}, ayar, k, yurutme=s09_istek())
    assert gecerli["sonuc"]["alinan_adet"] == 15
    assert gecerli["pozisyon"]["kutu_alt"] == 90
    assert gecerli["pozisyon"]["hedef"] == 120


@pytest.mark.parametrize("deger", [0, -1, float("inf"), float("nan")])
def test_s09_bozuk_kurulum_fiyati_giris_uretemez(deger):
    m = s09_mumlar()
    k = pd.DataFrame({"kutu_alt": [deger], "hedef": [120]}, index=m.index[:1])
    try:
        d = motor.tara(
            m,
            {m.index[0]: "s"},
            replace(aileler.Parametre(), stop="kutu"),
            k,
            yurutme=s09_istek(),
        )
    except ValueError as exc:
        assert "kurulum fiyatı" in str(exc)
        return
    assert d["dolumlar"] == []
    assert d["retler"][0]["neden"] == "kurulum_eksik"


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
    df = pd.DataFrame(satirlar, index=pd.bdate_range(GUNLER[0], periods=len(satirlar)))
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
    for g, b in zip(gercek, beklenen, strict=True):
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


def test_karantina_249_gunu_engeller_250_gunu_serbest_birakir():
    # TASARIM 5.1: 249. satır engelli; 250. satır sinyali 251'de 100'den girip veri sonunda 100'den çıkar.
    mumlar = _mumlar([r(*STD, karantina=True)] + [r(*STD)] * 251, 2)
    canli, dusen = motor.islemler(mumlar, mumlar.index[[249, 250]])
    onbellek, zincir_dusen = motor.Zincir(mumlar).calistir([249, 250])
    for tablo in (canli, onbellek):
        assert [
            (
                mumlar.index.get_loc(t.sinyal_tarih),
                mumlar.index.get_loc(t.giris_tarih),
                mumlar.index.get_loc(t.cikis_tarih),
                t.giris_fiyat,
                t.cikis_fiyat,
                t.neden,
            )
            for t in tablo.itertuples()
        ] == [(250, 251, 251, 100.0, 100.0, "veri_sonu")]
    assert (dusen, zincir_dusen) == (0, 0)
    pd.testing.assert_frame_equal(canli, onbellek)


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
        aileler,
        "kurulum",
        lambda m, p: pd.DataFrame(
            index=pd.DatetimeIndex([gun[2], gun[5]]),
            columns=["kutu_alt", "kutu_ust", "hedef"],
        ),
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
        aileler,
        "kurulum",
        lambda m, p: pd.DataFrame(
            index=pd.DatetimeIndex([gun[2], gun[5]]),
            columns=["kutu_alt", "kutu_ust", "hedef"],
        ),
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


def _ozet(satirlar, ayar, kurulum=None, atr=2):
    t, dusen = motor.islemler(_mumlar(satirlar, atr), GUNLER[[0]], ayar, kurulum)
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
    # rsi70 (bilet 05: etkinleşme önşartı). Gün 2 kapanış 102 > giriş 100 ve > SMA50 90: kâr bölgesi (u = 2 <= t - 1).
    # Gün 3 RSI 72 -> 69 (70'in altında): tetik. Gün 4 AOF 100,5 yarı satış (kapanış 100 < önceki düşük 100? hayır).
    # Gün 5 kapanış 99 < önceki düşük 99,5 ve yarı satış yapılmış -> kalanın tamamı ertesi AOF'ta. Gün 6 AOF 98,5
    # (düşük 97,5 > 96), neden cikis_kurali. Ortalama (100,5 + 98,5) / 2 = 99,5; kayıp 0,5.
    "rsi70_yari_sonra_kalan": (
        Parametre(cikis="rsi70"),
        [
            S0,
            r(100, 101, 99, 100, rsi=55, onceki_rsi=54, sma50=90, onceki_dusuk=0),
            r(101, 102.5, 100.5, 102, rsi=72, onceki_rsi=55, sma50=90, onceki_dusuk=99),
            r(101, 102, 100, 101, rsi=69, onceki_rsi=72, sma50=90, onceki_dusuk=100.5),
            r(100.5, 101, 99, 100, rsi=60, onceki_rsi=69, sma50=90, onceki_dusuk=100),
            r(100, 100.5, 98.5, 99, rsi=55, onceki_rsi=60, sma50=90, onceki_dusuk=99.5),
            r(98.5, 99, 97.5, 98, rsi=50, onceki_rsi=55, sma50=90, onceki_dusuk=98.5),
        ],
        (1, 100, 6, 99.5, "cikis_kurali", 4, 0.5),
    ),
}


@pytest.mark.parametrize("ad", YARI)
def test_yari_satis_kurallari(ad):
    ayar, satirlar, beklenen = YARI[ad]
    assert _ozet(satirlar, ayar) == _ak(beklenen)


def test_islem_tablosu_yari_satis_tarihini_ve_fiyatini_tasir_yoksa_bos():
    # TASARIM 5.5 "Yarı satışlı işlem". atr3_gun_ici: yarı satış gün 2'de seviye 100 + 3*2 = 106'da.
    ayar, satirlar, _ = YARI["atr3_gun_ici"]
    t, _ = motor.islemler(_mumlar(satirlar, 2), GUNLER[[0]], ayar)
    assert (t.iloc[0].yari_tarih, t.iloc[0].yari_fiyat) == (GUNLER[2], 106.0)
    # stopta_cikis: yarı satış kuralı yok (cikis "yok"): iki sütun da boş.
    sinyaller, atr, satirlar, _, _ = SENARYO["stopta_cikis"]
    t, _ = motor.islemler(_mumlar(satirlar, atr), GUNLER[sinyaller])
    assert pd.isna(t.iloc[0].yari_tarih) and pd.isna(t.iloc[0].yari_fiyat)
    # İşlemsiz tabloda da sütunlar vardır.
    sinyaller, atr, satirlar, _, _ = SENARYO["kilitli_tavan_girisi"]
    t, _ = motor.islemler(_mumlar(satirlar, atr), GUNLER[sinyaller])
    assert len(t) == 0 and {"yari_tarih", "yari_fiyat"} <= set(t.columns)


@pytest.mark.parametrize("cikis", ["dip", "rsi70"])
def test_dip_etkinlesmeden_ve_rsi70_yarisindan_once_kapanis_dusuk_alti_satis_vermez(
    cikis,
):
    # Gün 2 kapanış 99 < önceki düşük 99,5 ama yüksek 101 < 103 (dip etkin değil) ve RSI reddi yok (60, 60): satış yok.
    # Gün 3 veri sonu 99,5. Çıkış fiyatı ortalama değil: 99,5; kayıp 0,5.
    satirlar = [
        S0,
        r(100, 101, 99, 100, rsi=60, onceki_rsi=60, sma50=90, onceki_dusuk=0),
        r(100, 101, 98, 99, rsi=60, onceki_rsi=60, sma50=90, onceki_dusuk=99.5),
        r(99, 100, 98, 99.5, rsi=60, onceki_rsi=60, sma50=90, onceki_dusuk=98),
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


# rsi70 etkinleşme önşartı (bilet 05, KURALLAR §3 "Modül 1"): RSI70 yarı satışı yalnız girişten sonra bir u <= t - 1 gününde
# kapanış > giriş fiyatı ve kapanış > SMA50 olmuşsa sayılır. Giriş 100 (gün 1), stop 96. Gün 3 RSI 72 -> 69 (reddi) ve kapanış
# 101 > 100 ve > SMA50 90: bugünün kendisi koşulu sağlar, ama u <= t - 1 olmalı. Gün 2 kapanış K, SMA50 M.
# Gün 4 AOF 101, gün 5 veri sonu kapanış 102,5 (düşük 101 > stop).
# K=101, M=90: gün 2 koşulu sağlar -> yarı satış gün 4 AOF 101; ortalama (101 + 102,5) / 2 = 101,75.
# K=101, M=105: kapanış SMA50'nin altında -> önşart yok -> satış yok, çıkış 102,5.
# K=100, M=90: kapanış giriş fiyatına eşit (> değil) -> satış yok, çıkış 102,5.
# K=99,5, M=90: kapanış giriş fiyatının altında -> satış yok, çıkış 102,5.
@pytest.mark.parametrize(
    "kapanis_2, sma50_2, beklenen",
    [
        (101.0, 90.0, (1, 100, 5, 101.75, "veri_sonu", 4, 0)),
        (101.0, 105.0, (1, 100, 5, 102.5, "veri_sonu", 4, 0)),
        (100.0, 90.0, (1, 100, 5, 102.5, "veri_sonu", 4, 0)),
        (99.5, 90.0, (1, 100, 5, 102.5, "veri_sonu", 4, 0)),
    ],
    ids=["onsart-var", "sma50-altinda", "girise-esit", "giris-altinda"],
)
def test_rsi70_yari_satis_onsart_onceki_gun_kapanis_giris_ve_sma50_ustunde(
    kapanis_2, sma50_2, beklenen
):
    satirlar = [
        S0,
        r(100, 101, 99, 100, rsi=55, onceki_rsi=54, sma50=90, onceki_dusuk=0),
        r(
            100.5,
            101.5,
            99.5,
            kapanis_2,
            rsi=72,
            onceki_rsi=55,
            sma50=sma50_2,
            onceki_dusuk=99,
        ),
        r(100.5, 101, 100, 101, rsi=69, onceki_rsi=72, sma50=90, onceki_dusuk=99.5),
        r(101, 102, 100.5, 101.5, rsi=60, onceki_rsi=69, sma50=90, onceki_dusuk=100),
        r(102, 103, 101, 102.5, rsi=60, onceki_rsi=60, sma50=90, onceki_dusuk=100.5),
    ]
    assert _ozet(satirlar, Parametre(cikis="rsi70")) == _ak(beklenen)


# rsi70 önşartında giriş günü sayılmaz (KURALLAR §3 "Modül 1": "giriş günü sayılmaz"). Giriş 100 (gün 1), stop 96.
# Gün 1 (giriş günü): kapanış 101 > giriş fiyatı 100 ve > SMA50 90 (giriş günü sayılsaydı önşart sağlanırdı).
# Gün 2: kapanış 99,5 <= 100 -> önşart sağlanmaz; RSI 72 -> 69 reddi var, ama önşart yok -> yarı satış yok.
# Gün 3: AOF 100,2; veri sonu kapanışı 100,5 (düşük 99,5 > stop). Yarı satış yok -> çıkış 100,5; risk 4, kayıp 0.
# (Giriş günü sayılsaydı gün 2 yarı satış verir, gün 3 AOF 100,2'de dolar; çıkış (100,2 + 100,5) / 2 = 100,35.)
def test_rsi70_onsart_giris_gunu_sayilmaz_sonraki_gun_saglamazsa_yari_satis_yok():
    satirlar = [
        S0,
        r(100, 101, 99, 101, rsi=55, onceki_rsi=54, sma50=90, onceki_dusuk=0),
        r(100, 100.5, 99, 99.5, rsi=69, onceki_rsi=72, sma50=90, onceki_dusuk=0),
        r(100.2, 101, 99.5, 100.5, rsi=60, onceki_rsi=69, sma50=90, onceki_dusuk=99),
    ]
    assert _ozet(satirlar, Parametre(cikis="rsi70")) == _ak(
        (1, 100, 3, 100.5, "veri_sonu", 4, 0)
    )


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


def test_sinama_modul_1_varyanti_kutu_stopu_ve_hedef_cikisi(monkeypatch):
    hesaplanan = []
    hesapla = aileler.kurulum

    def sayilan_kurulum(*args, **kwargs):
        sonuc = hesapla(*args, **kwargs)
        hesaplanan.append(sonuc)
        return sonuc

    monkeypatch.setattr(aileler, "kurulum", sayilan_kurulum)
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
    assert len(hesaplanan) == 1, "Sinyalin kurulumu yeniden hesaplandı"
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


# KURALLAR §3 "Modül 1" Varyantlar tablosunun 24 adı (literal). Her varyant, sentetik dünyada (8 hisse, 700 gün; ısınma,
# SMA ve sıkışma ayarı gevşek) motordan hatasız geçer: bir kez kendi kapılarıyla, bir kez kapılar (hacim, momentum, R/R) gevşekken.
# Her koşu motor tablosunun sütunlarını verir; çıkış nedenleri tanımlı kümededir; fiyatlar sonlu ve pozitiftir. Bütün koşuların
# TOPLAM işlem sayısı sıfırdan büyüktür (sınama boş değil); kendi kapılarıyla 7 koşu boştur; kapılar gevşekken yalnız `giris_ucgen` boştur (bu dünyada işlem üretmez).
VARYANT_ADLARI = [
    "bugun",
    "tansu",
    "ema_5_8_13",
    "ema_20_50_100",
    "ema_10_20_50",
    "ema_50_100_200",
    "giris_kutu",
    "giris_ema",
    "giris_retest",
    "giris_agresif",
    "giris_arz",
    "giris_ucgen",
    "kutu_govde",
    "hacim_yok",
    "hacim_3",
    "momentum_kapali",
    "dusus_sonrasi",
    "teyit_acik",
    "teyit_trend",
    "stop_atr15",
    "stop_atr2",
    "cikis_dip",
    "cikis_rsi70",
    "cikis_rsi50",
]


def test_her_varyant_motordan_gecer_kisa_sentetik_seride_hata_yok():
    assert len(VARYANT_ADLARI) == 24
    dunya = denetim.dunya(11, hisse=8, gun=700)
    nedenler = {"stop", "sma250", "hedef", "cikis_kurali", "karantina", "veri_sonu"}
    sutunlar = [
        "sinyal_tarih",
        "giris_tarih",
        "giris_fiyat",
        "cikis_tarih",
        "cikis_fiyat",
        "neden",
        "adet",
        "planlanan_risk",
        "gerceklesen_kayip",
        "yari_tarih",
        "yari_fiyat",
        "sembol",
    ]
    toplam = 0
    for ad in VARYANT_ADLARI:
        p = replace(
            aileler.VARYANTLAR[ad],
            isinma=60,
            sma_n=50,
            esik=0.03,
            min_gun=2,
            pencere=30,
        )
        for ayar in (p, replace(p, hacim_kat=0.0, momentum=False, rr_min=0.0)):
            islemler, _ = motor.sinama(dunya, ayar)
            assert list(islemler.columns) == sutunlar, ad
            assert set(islemler["neden"]) <= nedenler, ad
            assert (islemler[["giris_fiyat", "cikis_fiyat"]] > 0).all().all(), ad
            toplam += len(islemler)
    assert toplam > 0


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


# --- Düzeltme turu C: kilitli tabanda hedef ve yarı satış, eşik karşılaştırmasında kayan nokta (TASARIM 5.3) ---

KILITLI = {
    # hedef 110, stop 96. Gün 2 kilitli taban: yüksek 112 >= 110, düşük 99,9 > 96 -> o gün çıkış yok.
    # Gün 3 kilitsiz: ertesi gün AOF 105, neden hedef. Risk 4, kayıp 0.
    "hedef_ertesi_kilitsiz_gun_aof": (
        Parametre(hedef="tansu"),
        _kurulum(hedef=110.0),
        [
            S0,
            r(100, 111, 99, 111),
            r(99.9, 112, 99.9, 99.9, kilit_taban=True),
            r(105, 108, 104, 106),
        ],
        (1, 100, 3, 105, "hedef", 4, 0),
    ),
    # Gün 2 ve gün 3 kilitli taban (gün 3 yüksek 99,5 < hedef, düşük 99,5 > 96): bekleyen hedef kayar. Gün 4 AOF 104.
    "hedef_iki_kilitli_gun": (
        Parametre(hedef="tansu"),
        _kurulum(hedef=110.0),
        [
            S0,
            r(100, 111, 99, 111),
            r(99.9, 112, 99.9, 99.9, kilit_taban=True),
            r(99.5, 99.5, 99.5, 99.5, kilit_taban=True),
            r(104, 106, 103, 105),
        ],
        (1, 100, 4, 104, "hedef", 4, 0),
    ),
}


@pytest.mark.parametrize("ad", KILITLI)
def test_hedef_kilitli_taban_gununde_ertesi_kilitsiz_gunun_aofunda_dolar(ad):
    ayar, kurulum, satirlar, beklenen = KILITLI[ad]
    assert _ozet(satirlar, ayar, kurulum) == _ak(beklenen)


def test_atr3_yari_satis_kilitli_taban_gununde_ertesi_aofa_kayar_ve_tek_seferdir():
    # Giriş 104, ATR 2: stop 100, seviye 110. Gün 2 kilitli taban, her fiyat 112,86 >= 110: yarı satış o gün yok.
    # Merdiven: n = ⌊8,86 / 2⌋ = 4 -> stop 108. Gün 3 kilitsiz: yarı satış AOF 113 (düşük 112 > 108).
    # Yüksek 120: n = 8 -> stop 116. Gün 4 ve 5 yüksek >= 110 yine, ama yarı satış tek sefer; düşük 116,5 ve 117 > 116.
    # Veri sonu 120. Ortalama (113 + 120) / 2 = 116,5 (gün 2'de AOF 112,86 dolsaydı 116,43).
    satirlar = [
        S0,
        r(104, 105, 103, 104),
        r(112.86, 112.86, 112.86, 112.86, kilit_taban=True),
        r(113, 120, 112, 118),
        r(117, 119, 116.5, 118),
        r(119, 121, 117, 120),
    ]
    assert _ozet(satirlar, Parametre(cikis="atr3")) == _ak(
        (1, 104, 5, 116.5, "veri_sonu", 4, 0)
    )


def _ozet_atr(satirlar, ayar, atr):
    # Fiyatlar 5-10 arası; varsayılan SMA250 (50) SMA250 çıkışı verirdi. SMA250 = 1: kapanış hep üstünde.
    satirlar = [{"sma250": 1.0, **s} for s in satirlar]
    t, dusen = motor.islemler(_mumlar(satirlar, atr), GUNLER[[0]], ayar)
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


@pytest.mark.parametrize(
    "yuksek, beklenen",
    [
        # Giriş 10, ATR 0,2, ilk stop 9,6. Gün 2 yüksek 10,6: (10,6 - 10) / 0,2 = 3 tam (kayan nokta 2,999...): n = 3,
        # stop = 10 + 1 * 0,2 = 10,2. Gün 3 düşük 9,95 <= 10,2 -> min(10,2; 10,3) = 10,2. Risk 0,4, kayıp 0.
        (10.6, (1, 10, 3, 10.2, "stop", 0.4, 0)),
        # Yüksek 10,5999: oran 2,9995 -> n = 2, stop = 10. Gün 3 düşük 9,95 <= 10 -> min(10; 10,3) = 10.
        (10.5999, (1, 10, 3, 10.0, "stop", 0.4, 0)),
    ],
)
def test_merdiven_tam_esikte_kayan_nokta_basamagi_dusurmez(yuksek, beklenen):
    satirlar = [
        r(10, 10.1, 9.9, 10),
        r(10, 10.1, 9.9, 10, onceki_dusuk=0),
        r(10.3, yuksek, 10.1, 10.4, onceki_dusuk=0),
        r(10.3, 10.4, 9.95, 10.3, onceki_dusuk=0),
    ]
    assert _ozet_atr(satirlar, Parametre(cikis="dip"), 0.2) == _ak(beklenen)


def test_atr3_seviyesi_tam_esikte_kayan_nokta_yuzunden_kacmaz():
    # Giriş 5,2, ATR 0,2, stop 4,8. Seviye 5,2 + 3 * 0,2 = 5,8 (kayan nokta 5,800000000000001). Gün 2 yüksek 5,8,
    # düşük 5,3 <= seviye -> yarı satış 5,8. n = ⌊0,6 / 0,2⌋ = 3 -> stop 5,4 (gün 3 düşük 5,5 > 5,4). Veri sonu 5,7.
    # Ortalama (5,8 + 5,7) / 2 = 5,75 (yarı satış kaçsaydı 5,7).
    satirlar = [
        r(5.2, 5.3, 5.1, 5.2),
        r(5.2, 5.3, 5.1, 5.2),
        r(5.5, 5.8, 5.3, 5.6),
        r(5.7, 5.8, 5.5, 5.7),
    ]
    assert _ozet_atr(satirlar, Parametre(cikis="atr3"), 0.2) == _ak(
        (1, 5.2, 3, 5.75, "veri_sonu", 0.4, 0)
    )


def test_dip_etkinligi_tam_esikte_kayan_nokta_yuzunden_kacmaz():
    # Giriş 5,2, ATR 0,4, stop 4,4. Etkinlik 5,2 + 1,5 * 0,4 = 5,8 (kayan nokta 5,800000000000001). Gün 2 yüksek 5,8 -> etkin.
    # Gün 3 kapanış 5,25 < önceki düşük 5,3 -> tetik; gün 4 AOF 5,1 yarı satış. Veri sonu 5,3.
    # Ortalama (5,1 + 5,3) / 2 = 5,2 (etkinlik kaçsaydı satış olmaz, 5,3). Risk 0,8.
    satirlar = [
        r(5.2, 5.4, 5.0, 5.2),
        r(5.2, 5.4, 5.0, 5.2, onceki_dusuk=0),
        r(5.4, 5.8, 5.3, 5.6, onceki_dusuk=5.0),
        r(5.4, 5.5, 5.2, 5.25, onceki_dusuk=5.3),
        r(5.1, 5.4, 5.0, 5.3, onceki_dusuk=5.2),
    ]
    assert _ozet_atr(satirlar, Parametre(cikis="dip"), 0.4) == _ak(
        (1, 5.2, 4, 5.2, "veri_sonu", 0.8, 0)
    )


@pytest.mark.parametrize(
    "yuksek, beklenen",
    [
        # KURALLAR §3 ATR merdiveni: ATR_sinyal = 0 ise n tanımsızdır, merdiven basamağı yoktur.
        # Kutu alt 95 -> ilk stop 95, giriş 100, R = 5; başabaş eşiği 100 + 1,5 * 5 = 107,5. Gün 2 yüksek 105 < 107,5:
        # stop 95 kalır; gün 3 düşük 99,5 > 95; veri sonu kapanışı 101. Risk 5, kayıp max(0, 100 - 101) = 0.
        (105, (1, 100, 3, 101, "veri_sonu", 5, 0)),
        # Gün 2 yüksek 108 >= 107,5: başabaş sayıyla aynen çalışır, stop 100 olur. Gün 3 düşük 99,5 <= 100 -> min(100, 102) = 100.
        (108, (1, 100, 3, 100, "stop", 5, 0)),
    ],
)
def test_atr_sifirken_merdiven_basamagi_yok_motor_cokmez(yuksek, beklenen):
    satirlar = [
        S0,
        GIRIS,
        r(101, yuksek, 100.5, 104, onceki_dusuk=0),
        r(102, 103, 99.5, 101, onceki_dusuk=0),
    ]
    assert _ozet(
        satirlar, Parametre(stop="kutu", cikis="dip"), _kurulum(95.0), atr=0
    ) == _ak(beklenen)


DUZ = dict(periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=15, sma_n=2)


def test_duz_seride_agresif_sinyal_atr_sifir_motor_merdiven_basamagi_yok():
    # KURALLAR §3 ATR merdiveni, düz seri: 15 gün kapanış = yüksek = düşük = 100 (gerçek aralık 0, ATR14 gün 13'ten 0). Isınma 15 ->
    # agresif sinyal ilk kez gün 14'te (koşu gün 0'dan beri; `kurulum` ATR14'ü hep 0 görür). Motor: giriş günü 15 AOF 100, ATR_sinyal 0
    # -> ilk stop 100 - 2 * 0 = 100. Gün 15 düşük 101 > 100 (açık kalır). Gün 16 yüksek 110: ATR 0 olmasa n = ⌊10 / ATR⌋ olurdu;
    # n tanımsızdır, basamak yok, stop 100 kalır (başabaş eşiği 100 + 1,5 * 0 = 100, stop = max(100, 100)). Gün 17 düşük 99 <= 100,
    # AOF 100,5: dolum min(100, 100,5) = 100, neden stop. Risk 100 - 100 = 0, kayıp 0.
    satirlar = (
        [r(100, 100, 100, 100)] * 15
        + [r(100, 102, 101, 101, onceki_dusuk=0)]
        + [r(105, 110, 104, 108, onceki_dusuk=0)]
        + [r(100.5, 101, 99, 100, onceki_dusuk=104)]
    )
    m = _mumlar(satirlar, 0)
    ayar = Parametre(giris="agresif", cikis="dip", **DUZ)
    k = aileler.kurulum(m.iloc[:15].assign(hacim=100.0), ayar)
    assert list(k.index) == [
        m.index[14]
    ]  # düz seride tek agresif sinyal, ATR14 = 0 günü
    assert gostergeler.atr(m["yuksek"], m["dusuk"], m["kapanis"]).iloc[14] == 0
    t, dusen = motor.islemler(m, k.index, ayar, k)
    assert dusen == 0 and len(t) == 1
    x = t.iloc[0]
    assert (
        m.index.get_loc(x.giris_tarih),
        x.giris_fiyat,
        m.index.get_loc(x.cikis_tarih),
        x.cikis_fiyat,
        x.neden,
        x.planlanan_risk,
        x.gerceklesen_kayip,
    ) == _ak((15, 100, 17, 100, "stop", 0, 0))


def test_eski_motor_pay_kimligi_paketini_acikca_reddeder():
    from tansu import veri

    with pytest.raises(veri.VeriHatasi, match="eski motor pay kimliği"):
        motor.sinama(
            None,
            veri_paketi=dict(
                uyelik={}, referans=dict(pay_kimligi=dict(surum="pay_kimligi_v1"))
            ),
        )


@pytest.mark.parametrize(
    "girdi,dolar",
    [
        ({}, True),
        ({"ham_yuksek": 100.0, "ham_dusuk": 100.0}, False),
        ({"ham_yuksek": None}, False),
        ({"ham_yuksek": float("inf")}, False),
        ({"ham_dusuk": 0.0}, False),
        ({"ham_dusuk": -1.0}, False),
        ({"ham_yuksek": True}, False),
        ({"ham_yuksek": 98.0}, False),
        ({"tavan": 200.0}, False),
        ({"taban": 50.0}, False),
        ({"limit_kaniti": "eksik-sinir"}, False),
        ({"tavan": 200.0, "taban": 50.0}, False),
        (
            {
                "tavan": 200.0,
                "taban": 50.0,
                "limit_kaniti": "bilinen",
                "ham_yuksek": 100.0,
                "ham_dusuk": 100.0,
            },
            True,
        ),
    ],
)
def test_s09_ham_aralik_yalniz_tamamen_yok_sayisal_kanitta_kilidi_dislar(girdi, dolar):
    m = s09_mumlar().drop(columns=["tavan", "taban", "limit_kaniti"])
    y = s09_istek(kilit_politikasi="ham_aralik_v1")
    ilk = motor.tara(m.iloc[:1], {m.index[0]: "sinyal-1"}, yurutme=y)
    mum = dict(m.iloc[1]) | dict(tarih=m.index[1]) | girdi
    once = dict(mum)
    son = motor.islem_adimi(ilk, mum, yurutme=y)
    assert bool(son["dolumlar"]) is dolar
    assert mum == once
    assert son["yurutme"] == y
    if not dolar:
        assert son["retler"][-1]["neden"] == "limit_bilinmiyor"
    with pytest.raises(ValueError, match="uyuşmuyor"):
        motor.islem_adimi(ilk, mum, yurutme=s09_istek())


@pytest.mark.parametrize(
    "girdi",
    [
        {"tavan": float("nan")},
        {"taban": float("inf")},
        {"tavan": np.float32("nan")},
        {"taban": np.float32("inf")},
        {"tavan": np.bool_(True)},
        {"limit_kaniti": np.bool_(False)},
        {"tavan": 0},
        {"taban": -1},
        {"limit_kaniti": ""},
        {"limit_kaniti": False},
        {"tavan": 100.0, "taban": 50.0, "limit_kaniti": "bilinen"},
    ],
)
def test_s09_ham_aralik_bozuk_sayisal_kaniti_atlamaz(girdi):
    m = s09_mumlar().drop(columns=["tavan", "taban", "limit_kaniti"])
    with pytest.raises(ValueError, match="limit"):
        motor.tara(
            m.assign(**girdi),
            {m.index[0]: "sinyal-1"},
            yurutme=s09_istek(kilit_politikasi="ham_aralik_v1"),
        )


@pytest.mark.parametrize("politika", [None, "", "baska_v1", False])
def test_s09_bilinmeyen_kilit_politikasi_reddedilir(politika):
    with pytest.raises(ValueError, match="kilit_politikasi"):
        motor.tara(s09_mumlar(), {}, yurutme=s09_istek(kilit_politikasi=politika))


@pytest.mark.parametrize(
    "sayi", [int, float, np.int64, np.int32, np.uint64, np.float32, np.float64]
)
@pytest.mark.parametrize("politika", [None, "ham_aralik_v1"])
def test_s09_bilinen_limit_desteklenen_skalerle_ayni_dolumu_verir(sayi, politika):
    # TASARIM 5.15: temsil türü bilinen sınırın geçerliliğini değiştirmez.
    y = s09_istek(**({} if politika is None else dict(kilit_politikasi=politika)))
    m = s09_mumlar()
    ilk = motor.tara(m.iloc[:1], {m.index[0]: "s"}, yurutme=y)
    satir = dict(m.iloc[1]) | dict(tarih=m.index[1], tavan=sayi(110), taban=sayi(90))
    once = dict(satir)
    hata = None
    try:
        sonuc = motor.islem_adimi(ilk, satir, yurutme=y)
    except ValueError as exc:
        hata = str(exc)
    assert hata is None, hata
    assert [(d["yon"], d["adet"], d["fiyat"]) for d in sonuc["dolumlar"]] == [
        ("alis", 15, 100)
    ]
    assert satir == once
    assert sonuc["yurutme"] == y
