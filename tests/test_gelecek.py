"""Geleceği görmeme testi (TASARIM 5.12, B-18): veriyi t'de kes; t öncesi çıktılar değişmesin.

Tek parametrik test: bileşen × kesim günü. Sentetik dünya (`denetim.dunya`, 24 hisse, 900 gün; 02.01.2012'den). Kesilen
anlık görüntüde t'den sonraki fiyat satırları ve faiz değişimleri yoktur; tam görüntünün t'ye kadarki çıktısı aynı olmalı.
Kapsam: evren, göstergeler, EMA ve çift sinyalleri, çift seçimi, likidite medyanı, faiz hizalaması (ve K2 sepeti), Tansu
sınaması (EMA hücre işlemleri ve ileri yürüme seçimleri).
Modül 1: yeni göstergeler (RSI, momentum squeeze, ADX, MACD, PSAR, stokastik) ve EMA kurulumu (varyant örnekleri: kutu, hedef,
`arz` ve `ucgen` girişleri, düşüş süzgeci; arz ve talep bölgeleri) ve çıkış paketi (`motor.sinama` ile `tansu` ve `cikis_rsi70`:
yarı satış sütunları, `Pozisyon.kar`).
"""

from copy import deepcopy
from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from tansu import (
    aileler,
    cift,
    ciftbolme,
    denetim,
    evren,
    gostergeler,
    motor,
    simulator,
    tansusinama,
    veri,
)

KESIM = [
    "2014-09-30",
    "2015-01-15",
    "2015-03-02",
    "2014-12-31",  # yılın son işlem günü: biten yıl 2014 karşılaştırılır (yillik_fazla_)
]  # tam veri 2015-06'ya dek; ısınma (500 gün) 2013-11'de biter
BAS = "2013-12-02"


def test_ortak_ema_kurulumu_gelecek_fiyat_degisiminden_etkilenmez(monkeypatch):
    gunler = pd.bdate_range("2021-01-04", periods=520)
    kap = [100.0] * 510 + [110.0, 112.0] + [114.0] * 8
    fiyat = pd.DataFrame(
        {
            "tarih": gunler,
            "sembol": "TEST",
            "xu100": 1000.0,
            "kapanis": kap,
            "aof": kap,
            "yuksek": np.asarray(kap) + 1,
            "dusuk": np.asarray(kap) - 1,
            "hacim": 100.0,
        }
    )
    for ad in ("kapanis", "aof", "yuksek", "dusuk"):
        fiyat[f"ham_{ad}"] = fiyat[ad]
    anlik = veri.Anlik(
        "test", fiyat, pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    )
    monkeypatch.setattr(veri, "oku", lambda *a: anlik)
    # E1 manifest okuması bu sentetik görüntü için yapılmaz; gerçek veri kanıtı ayrı koşudur.
    monkeypatch.setattr(
        veri,
        "_veri_referansi",
        lambda *a: {
            "kayit_id": "test",
            "istenen_donem": {
                "baslangic": str(gunler[500].date()),
                "bitis": str(gunler[-1].date()),
            },
        },
    )
    paket = veri.veri_hazirla(
        veri.VeriIstegi(
            ("TEST",),
            str(gunler[500].date()),
            str(gunler[-1].date()),
            "sentetik",
            "legacy_portfoy_v1",
            "legacy",
            "legacy",
            "test",
            (str(gunler[0].date()), str(gunler[499].date())),
        ),
        "test",
        ".",
    )
    tarih = gunler[511]
    strateji = aileler.legacy_coz("bugun")
    once = aileler.ortak_kurulum(paket, tarih, strateji)
    assert len(once["sinyaller"]) == 1
    degisen = deepcopy(paket)
    for r in degisen["piyasa"]:
        if pd.Timestamp(r["tarih"]) > tarih:
            for ad in ("kapanis", "aof", "yuksek", "dusuk"):
                r[f"duzeltilmis_{ad}"]["deger"] *= 50
    sonra = aileler.ortak_kurulum(degisen, tarih, strateji)
    for sonuc in (once, sonra):
        for grup in ("gostergeler", "sinyaller"):
            for kayit in sonuc[grup]:
                kayit.pop("olusturma_zamani")
    assert once == sonra


def test_ortak_cift_kurulumu_gelecek_fiyat_degisiminden_etkilenmez():
    from tests.test_cift import cift_paketi

    paket = cift_paketi()
    tarih = paket["piyasa"][-1]["tarih"]
    strateji = ciftbolme.strateji_coz("Y", "X")
    once = ciftbolme.ortak_kurulum(paket, tarih, strateji)
    assert len(once["sinyaller"]) == 1
    degisen = deepcopy(paket)
    gelecek = (pd.Timestamp(tarih) + pd.Timedelta(days=1)).date().isoformat()
    for r in paket["piyasa"][-2:]:
        r = deepcopy(r)
        r["tarih"] = gelecek
        r["duzeltilmis_kapanis"]["deger"] *= 50 if r["sembol"] == "Y" else 0.01
        degisen["piyasa"].append(r)
    sonra = ciftbolme.ortak_kurulum(degisen, tarih, strateji)
    for sonuc in (once, sonra):
        for grup in ("gostergeler", "sinyaller"):
            for kayit in sonuc[grup]:
                kayit.pop("olusturma_zamani")
    assert once == sonra


def test_bist30_gelecekteki_uyelik_degisse_de_onceki_liste_degismez(monkeypatch):
    istek = veri.UyelikIstegi(
        ("2021-02-05", "2021-04-01"), "donemsel_bist30_v1", "bist30_2021_2025_v1"
    )
    once = veri.uyelik_hazirla(istek)
    oku = pd.read_csv

    def gelecek_degisti(*args, **kwargs):
        t = oku(*args, **kwargs)
        t.loc[t["sembol"] == "ASTOR", "sembol"] = "GELECEK"
        return t

    monkeypatch.setattr(pd, "read_csv", gelecek_degisti)
    sonra = veri.uyelik_hazirla(istek)
    assert (
        "GELECEK"
        in veri.uyelik_hazirla(
            veri.UyelikIstegi(
                ("2023-07-03",), istek.evren_politikasi, istek.uyelik_surumu
            )
        )["gunler"]["2023-07-03"]["semboller"]
    )
    for tarih in istek.tarihler:
        assert once["gunler"][tarih]["semboller"] == sonra["gunler"][tarih]["semboller"]
        assert [k["kayit_id"] for k in once["gunler"][tarih]["kanitlar"]] == [
            k["kayit_id"] for k in sonra["gunler"][tarih]["kanitlar"]
        ]


@pytest.mark.parametrize("politika", ["legacy_portfoy_v1", "legacy_tansu_v1"])
def test_veri_motoru_cift_girdileri_onek_degismez(politika):
    gunler = pd.date_range("2024-01-01", periods=5)
    C = np.array(
        [[10.0, 20.0], [np.nan, 21.0], [np.inf, 22.0], [13.0, 0.0], [14.0, 24.0]]
    )
    A = C.copy()
    F = {"I": np.ones((5, 2), dtype=bool)}
    F.update({k: np.zeros((5, 2), dtype=bool) for k in ("T", "B", "Kar")})
    F["I"][1, 0] = False
    F["Kar"][3, 1] = True
    tam = veri.cift_girdileri(gunler, C, A, F, politika)
    for son in range(1, 6):
        kesik = veri.cift_girdileri(
            gunler[:son], C[:son], A[:son], {k: v[:son] for k, v in F.items()}, politika
        )
        for ad in (
            "C",
            "A",
            "I",
            "T",
            "B",
            "Kar",
            "G",
            "E",
            "SA",
            "Cf",
            "son_gecerli_fiyat_tarihi",
        ):
            np.testing.assert_array_equal(kesik[ad], tam[ad][:son], err_msg=ad)


@pytest.fixture(scope="module")
def tam():
    return denetim.dunya(11, hisse=24, gun=900)


def kes(a, t):
    return veri.Anlik(
        a.kimlik,
        a.fiyat[a.fiyat["tarih"] <= t],
        a.olaylar,
        a.faiz[a.faiz["tarih"] <= t],
        a.sektor,
    )


def seri(a, s, sutun="kapanis"):
    return a.fiyat[a.fiyat["sembol"] == s].set_index("tarih")[sutun]


def kapanislar(a):
    return a.fiyat.pivot(index="tarih", columns="sembol", values="kapanis")


def evren_(tam, kes_, t):
    for ay in pd.period_range("2013-01", t.to_period("M"), freq="M"):
        assert evren.evren(kes_, ay.to_timestamp()) == evren.evren(
            tam, ay.to_timestamp()
        )


def gostergeler_(tam, kes_, t):
    for s in ("S000", "S007"):
        for ad, f in {
            "ema": lambda a, s=s: gostergeler.ema(seri(a, s), 20),
            "sma": lambda a, s=s: gostergeler.sma(seri(a, s), 50),
            "atr": lambda a, s=s: gostergeler.atr(
                seri(a, s, "yuksek"), seri(a, s, "dusuk"), seri(a, s), 14
            ),
            "sikisma": lambda a, s=s: gostergeler.sikisma_orani(seri(a, s)),
            "rsi": lambda a, s=s: gostergeler.rsi(seri(a, s), 14),
            "momentum": lambda a, s=s: gostergeler.momentum_squeeze(
                seri(a, s, "yuksek"), seri(a, s, "dusuk"), seri(a, s)
            ),
            "adx": lambda a, s=s: gostergeler.adx(
                seri(a, s, "yuksek"), seri(a, s, "dusuk"), seri(a, s)
            ),
            "macd": lambda a, s=s: gostergeler.macd_histogram(seri(a, s)),
            "psar": lambda a, s=s: gostergeler.psar(
                seri(a, s, "yuksek"), seri(a, s, "dusuk")
            ),
            "stokastik_k": lambda a, s=s: gostergeler.stokastik(
                seri(a, s, "yuksek"), seri(a, s, "dusuk"), seri(a, s)
            )[0],
            "stokastik_d": lambda a, s=s: gostergeler.stokastik(
                seri(a, s, "yuksek"), seri(a, s, "dusuk"), seri(a, s)
            )[1],
        }.items():
            pd.testing.assert_series_equal(f(tam).loc[:t], f(kes_), obj=f"{s} {ad}")
    xu = lambda a: a.fiyat.groupby("tarih")["xu100"].first()  # noqa: E731
    pd.testing.assert_series_equal(
        gostergeler.piyasa_durumu(xu(tam)).loc[:t], gostergeler.piyasa_durumu(xu(kes_))
    )


def ema_sinyal_(tam, kes_, t):
    toplam = 0
    for s in sorted(tam.fiyat["sembol"].unique()):
        ft, fk = (
            a.fiyat[a.fiyat["sembol"] == s].set_index("tarih")[["kapanis", "yuksek"]]
            for a in (tam, kes_)
        )
        sig = aileler.sinyal(ft)
        pd.testing.assert_index_equal(sig[sig <= t], aileler.sinyal(fk), exact=False)
        n = len(fk)
        for ad in ("on_sart", "uygun_gunler", "pencere_gunleri"):
            fonk = getattr(aileler, ad)
            np.testing.assert_array_equal(
                fonk(ft, aileler.Parametre())[:n],
                fonk(fk, aileler.Parametre()),
                err_msg=f"{s} {ad}",
            )
        np.testing.assert_array_equal(
            aileler.sikismasiz_kirilim(ft)[:n], aileler.sikismasiz_kirilim(fk)
        )
        toplam += len(sig[sig <= t])
    assert toplam > 0 or t < pd.Timestamp(
        "2014-06-01"
    )  # sınama boş değil: t öncesinde sinyal var


def kurulum_varyantlari():
    """Örnek varyantlar; ısınma, SMA ve sıkışma ayarı gevşek (900 günlük dünyada çok sinyal çıksın). Her biri sıkı ve kapıları gevşek (hacim, momentum, R/R yok)."""
    ornek = {}
    for ad in (
        "tansu",
        "giris_ema",
        "giris_retest",
        "giris_agresif",
        "teyit_acik",
        "teyit_trend",
    ):
        p = replace(
            aileler.VARYANTLAR[ad],
            isinma=60,
            sma_n=50,
            esik=0.03,
            min_gun=2,
            pencere=30,
        )
        ornek[ad] = p
        ornek[ad + "_gevsek"] = replace(p, hacim_kat=0.0, momentum=False, rr_min=0.0)
    # bilet 04 ve 05: yeni giriş türleri (üst kutu, üst çizgi) ve düşüş süzgeci; `tansu` temelinden tek alan (`dusus_agresif`: iki alan, `giris` ve `dusus`)
    for ad, alan in (
        ("giris_arz", dict(giris="arz")),
        ("giris_ucgen", dict(giris="ucgen")),
        ("dusus_sonrasi", dict(dusus=True)),
        ("dusus_agresif", dict(giris="agresif", dusus=True)),
    ):
        p = replace(
            aileler.VARYANTLAR["tansu"],
            isinma=60,
            sma_n=50,
            esik=0.03,
            min_gun=2,
            pencere=30,
            **alan,
        )
        ornek[ad] = p
        ornek[ad + "_gevsek"] = replace(p, hacim_kat=0.0, momentum=False, rr_min=0.0)
    return ornek


def kurulum_(tam, kes_, t):
    """EMA kurulumu (kutu, hedef; varyant örnekleri) ve arz/talep bölgeleri: t'den sonrası t öncesini değiştirmez."""
    sinyal_sayisi = hedef_sayisi = bolge_sayisi = 0
    varyantlar = kurulum_varyantlari()
    for s in sorted(tam.fiyat["sembol"].unique()):
        ft, fk = (
            a.fiyat[a.fiyat["sembol"] == s].set_index("tarih")[
                ["kapanis", "yuksek", "dusuk", "hacim"]
            ]
            for a in (tam, kes_)
        )
        for ad, p in varyantlar.items():
            ktam, kkes = aileler.kurulum(ft, p), aileler.kurulum(fk, p)
            pd.testing.assert_frame_equal(ktam[ktam.index <= t], kkes, obj=f"{s} {ad}")
            sinyal_sayisi += len(kkes)
            hedef_sayisi += int(kkes["hedef"].notna().sum())
        for yon in ("arz", "talep"):
            zt, zk = aileler.bolgeler(ft, yon), aileler.bolgeler(fk, yon)
            zt = zt[zt["bilinen"] <= t].reset_index(drop=True)
            # t'den sonraki bozulma t'de bilinmez; temas sayısı t'den sonraki günleri de sayar, karşılaştırılmaz
            zt["bitis"] = zt["bitis"].where(zt["bitis"] <= t)
            pd.testing.assert_frame_equal(
                zt.drop(columns="temas"),
                zk.drop(columns="temas"),
                obj=f"{s} {yon}",
            )
            bolge_sayisi += len(zk)
    # sınama boş değil: kesimde sinyal, hedef ve bölge var
    assert sinyal_sayisi > 0 and hedef_sayisi > 0 and bolge_sayisi > 0


def cikis_ayari(ad):
    """Çıkış paketi varyantı; ısınma, SMA ve sıkışma ayarı gevşek, hacim, momentum ve R/R kapıları kapalı (çok işlem çıksın)."""
    return replace(
        aileler.VARYANTLAR[ad],
        isinma=60,
        sma_n=50,
        esik=0.03,
        min_gun=2,
        pencere=30,
        hacim_kat=0.0,
        momentum=False,
        rr_min=0.0,
    )


def cikis_paketi_(tam, kes_, t):
    """Modül 1 çıkış paketi: `tansu` (kutu stopu, hedef, `atr3` yarı satışı) ve `cikis_rsi70` (`Pozisyon.kar` önşartı) ile
    `motor.sinama` işlemleri, `yari_tarih` ve `yari_fiyat` dahil: t'den önce kapananlar kesilmişle tam görüntüde aynıdır.
    Kesilmişte t'de veri sonu çıkışı olabilir: t'de ve sonrasında kapananlar karşılaştırılmaz."""
    toplam = yari = 0
    for ad in ("tansu", "cikis_rsi70"):
        p = cikis_ayari(ad)
        tb, kb = (
            x[x["cikis_tarih"] < t].reset_index(drop=True)
            for x in (motor.sinama(tam, p)[0], motor.sinama(kes_, p)[0])
        )
        pd.testing.assert_frame_equal(tb, kb, obj=ad, check_dtype=False)
        toplam += len(kb)
        yari += int(kb["yari_tarih"].notna().sum())
    assert toplam > 0 and yari > 0  # sınama boş değil: işlem ve yarı satış var


def cift_sinyal_(tam, kes_, t):
    kt, kk = kapanislar(tam), kapanislar(kes_)
    for y, x in (("S000", "S004"), ("S001", "S005"), ("S002", "S006")):  # aynı sektör
        np.testing.assert_array_equal(
            ciftbolme.hedef(kt, y, x)[: len(kk)], ciftbolme.hedef(kk, y, x)
        )
        pd.testing.assert_series_equal(
            cift.z_skor(kt[y], kt[x], 60).loc[:t], cift.z_skor(kk[y], kk[x], 60)
        )


def cift_secimi_(tam, kes_, t):
    kt, kk = kapanislar(tam), kapanislar(kes_)
    uye = sorted(tam.fiyat["sembol"].unique())
    for s in (len(kk) - 1, len(kk) - 31):
        pd.testing.assert_frame_equal(
            ciftbolme.secim(kt, uye, tam.sektor, s),
            ciftbolme.secim(kk, uye, tam.sektor, s),
        )


def zemin_(tam, kes_, t):
    """Likidite medyanı, faiz hizalaması (günlük gecelik getiri) ve K2 sepeti: tam görüntüde t'den sonraki günler de var."""
    sonuc = []
    for a, son in ((tam, tam.gunler[-1]), (kes_, t)):
        ilk = simulator.ilk_gun(a, BAS)
        evr = simulator.evrenler(a, ilk, son)
        days = a.gunler[(a.gunler >= ilk) & (a.gunler <= son)]
        sonuc.append(simulator.zemin(a, evr, days, set(), {}))
    n = len(sonuc[1]["g"])
    pd.testing.assert_frame_equal(sonuc[0]["Lq"].loc[:t], sonuc[1]["Lq"])
    np.testing.assert_array_equal(sonuc[0]["g"][:n], sonuc[1]["g"])
    np.testing.assert_allclose(
        sonuc[0]["sepet"].to_numpy()[:n], sonuc[1]["sepet"].to_numpy(), rtol=1e-12
    )


def yillik_fazla_(tam, kes_, t):
    """Yıllık fazla getiri (TASARIM 5.8, günlük fazla getirilerin yıllık toplamı): t'den önce biten yıllar değişmez."""
    sonuc = []
    for a in (tam, kes_):
        ilk = simulator.ilk_gun(a, BAS)
        evr = simulator.evrenler(a, ilk, a.gunler[-1])
        islemler, dusen = motor.sinama(a, uye=simulator.uyeler(a, evr, ilk))
        sim = simulator.calistir(a, islemler, dusen, BAS, evr=evr)
        sonuc.append(sim["masraf"][0.003]["yillik"])
    yil_sonu = (
        tam.gunler[tam.gunler.year == t.year][-1] == t
    )  # t yılın son işlem günüyse t.year da biter
    biten = sonuc[1].index[sonuc[1].index < t.year + int(yil_sonu)]
    assert len(biten) > 0  # sınama boş değil: t'den önce biten yıl var
    pd.testing.assert_frame_equal(sonuc[0].loc[biten], sonuc[1].loc[biten])


def tansusinama_(tam, kes_, t):
    """Tansu sınaması (TASARIM 5.14), EMA ailesi: t'den önce kapanan hücre işlemleri ve ileri yürüme seçimleri (yıl ≤ t.year,
    seçim Y-01-01'den önce kapanmış işlemlerle yapılır) kesilmişle tam görüntüde aynıdır. Kesilmişte t'de veri sonu çıkışı
    olabilir: t'de ve sonrasında kapananlar karşılaştırılmaz."""
    izgara = tansusinama.IZGARA["ema_sikismasi"]
    sekil = tuple(len(v) for v in izgara.values())
    bas, son = pd.Timestamp("2012-01-01"), pd.Timestamp("2015-12-31")
    sutunlar = [
        "sinyal_tarih",
        "giris_tarih",
        "cikis_tarih",
        "giris_fiyat",
        "cikis_fiyat",
    ]
    toplam, secimler = 0, [[], []]
    for s in sorted(tam.fiyat["sembol"].unique())[:8]:
        tablolar = [
            tansusinama.ema_tablolari(
                motor.mumlar(a, s), aileler.Parametre(), izgara, BAS
            )
            for a in (tam, kes_)
        ]
        for tb, kb in zip(*tablolar, strict=True):
            pd.testing.assert_frame_equal(
                tb.loc[tb["cikis_tarih"] < t, sutunlar].reset_index(drop=True),
                kb.loc[kb["cikis_tarih"] < t, sutunlar].reset_index(drop=True),
                check_dtype=False,  # boş tablonun sütunları object kalır
            )
            toplam += int((tb["cikis_tarih"] < t).sum())
        for liste, tb in zip(secimler, tablolar, strict=True):
            yillar = tansusinama.ileri(tb, sekil, bas, son)["yillar"]
            liste.append([y for y in yillar if y["yil"] <= t.year])
    assert toplam > 0 or t < pd.Timestamp("2014-06-01")  # sınama boş değil
    assert secimler[0] == secimler[1]
    assert any(secimler[0][0])  # ileri yürüme yılı var


def tansusinama_cift_(tam, kes_, t):
    """Tansu sınaması (TASARIM 5.14), çift ailesi: t'den önce kapanan hücre işlemleri ve ileri yürüme seçimleri (yıl ≤ t.year)
    kesilmişle tam görüntüde aynıdır. Kesilmişte t'de veri sonu çıkışı olabilir: t'de ve sonrasında kapananlar
    karşılaştırılmaz."""
    izgara = tansusinama.IZGARA["cift_rotasyonu"]
    sekil = tuple(len(v) for v in izgara.values())
    bas, son = pd.Timestamp("2012-01-01"), pd.Timestamp("2015-12-31")
    semboller = ["S000", "S001", "S002", "S004", "S005", "S006"]
    isler = [
        tansusinama.cift_isleri(a, a.sektor, semboller, bas, izgara)[0]
        for a in (tam, kes_)
    ]
    assert len(isler[0]) > 0
    assert [j[1] for j in isler[0]] == [j[1] for j in isler[1]]
    sutunlar = [
        "sinyal_tarih",
        "giris_tarih",
        "cikis_tarih",
        "giris_fiyat",
        "cikis_fiyat",
    ]
    toplam, secimler = 0, [[], []]
    for jt, jk in zip(*isler, strict=True):
        tablolar = [tansusinama.cift_tablolari(*j[2:4], *j[5:])[0] for j in (jt, jk)]
        for tb, kb in zip(*tablolar, strict=True):
            pd.testing.assert_frame_equal(
                tb.loc[tb["cikis_tarih"] < t, sutunlar].reset_index(drop=True),
                kb.loc[kb["cikis_tarih"] < t, sutunlar].reset_index(drop=True),
                check_dtype=False,  # boş tablonun sütunları object kalır
            )
            toplam += int((tb["cikis_tarih"] < t).sum())
        for liste, tb in zip(secimler, tablolar, strict=True):
            yillar = tansusinama.ileri(tb, sekil, bas, son)["yillar"]
            liste.append([y for y in yillar if y["yil"] <= t.year])
    assert toplam > 0 or t < pd.Timestamp("2014-06-01")  # sınama boş değil
    assert secimler[0] == secimler[1]


@pytest.mark.parametrize("kesim", KESIM)
@pytest.mark.parametrize(
    "bilesen",
    [
        evren_,
        gostergeler_,
        ema_sinyal_,
        kurulum_,
        cikis_paketi_,
        cift_sinyal_,
        cift_secimi_,
        zemin_,
        yillik_fazla_,
        tansusinama_,
        tansusinama_cift_,
    ],
    ids=lambda f: f.__name__,
)
def test_t_den_sonrasi_veri_t_oncesi_ciktiyi_degistirmez(tam, bilesen, kesim):
    t = pd.Timestamp(kesim)
    bilesen(tam, kes(tam, t), t)


def test_yari_satisli_islemin_kapandigi_gunden_sonra_kesilen_veri_islemi_degistirmez(
    tam,
):
    """Çıkış paketi (TASARIM 5.12): `KESIM` günlerinde yarı satışlı işlem azdır (`tansu` 6, `cikis_rsi70` 7, `cikis_rsi50` 26; en geç 2014-12-25'te kapanır). Burada veri, yarı satışlı bir
    işlemin kapandığı günden sonraki işlem gününde kesilir; işlem (`yari_tarih`, `yari_fiyat`, çıkış) kesilmişte aynı olmalı."""
    toplam = 0
    for ad in ("tansu", "cikis_rsi70", "cikis_rsi50"):
        p = cikis_ayari(ad)
        x = motor.sinama(tam, p)[0]
        for _, i in x[x["yari_tarih"].notna()].head(2).iterrows():
            t = tam.gunler[tam.gunler > i["cikis_tarih"]][0]
            k = motor.sinama(kes(tam, t), p)[0]
            ayni = k[
                (k["sembol"] == i["sembol"]) & (k["giris_tarih"] == i["giris_tarih"])
            ]
            assert len(ayni) == 1, (ad, i["sembol"], t)
            pd.testing.assert_series_equal(ayni.iloc[0], i, check_names=False)
            toplam += 1
    assert toplam == 6  # sınama boş değil: üç varyantta ikişer yarı satışlı işlem


def _karantina_(ham, duz, olay_tarihi, son):
    """Tek sembol, 02.01.2024'ten başlayan iş günleri; çarpan 0,5; tablo tarihi `olay_tarihi`; seri `son`'da kesilir."""
    gun = pd.bdate_range("2024-01-02", periods=len(ham))
    f = pd.DataFrame(
        {"sembol": "XXXX", "tarih": gun, "ham_kapanis": ham, "kapanis": duz}
    )
    for s in ("aof", "yuksek", "dusuk"):
        f[s], f[f"ham_{s}"] = f["kapanis"], f["ham_kapanis"]
    for s in ("hacim", "pd", "hao_pd", "sermaye", "xu100"):
        f[s] = 1.0
    f = f[f["tarih"] <= son]
    olay = pd.DataFrame(
        {"sembol": ["XXXX"], "tarih": [pd.Timestamp(olay_tarihi)], "carpan": [0.5]}
    )
    a = veri.Anlik("k", f, olay, pd.DataFrame({"tarih": gun[:1], "faiz": 0.0}), {})
    return a.gun_tablosu.set_index("tarih")["karantina"]


@pytest.mark.parametrize(
    "ham, duz, olay, beklenen",
    [
        # Adım 03.01 (51 / 100); olay 04.01 (t+1) onu açıklamaz: 03.01 karantina (baz 100, taban 90, kapanış 51). 04.01: kapanış 52 / 51 adım değil, baz 51, temiz.
        ([100, 51, 52], [50, 51, 52], "2024-01-04", [False, True, False]),
        # Adım 05.01'de (51 / 102); olay 04.01 (t-1) ya da 05.01 (t) açıklar: karantina yok.
        ([100, 101, 102, 51, 52], [50, 50.5, 51, 51, 52], "2024-01-04", [False] * 5),
        ([100, 101, 102, 51, 52], [50, 50.5, 51, 51, 52], "2024-01-05", [False] * 5),
    ],
)
def test_olay_penceresi_onek_degismez_t_den_sonraki_tablo_t_oncesi_karantinayi_degistirmez(
    ham, duz, olay, beklenen
):
    # TASARIM 5.1 karantina (vekil kararı 15.10, 07e-4) ve 5.12: seriyi her günde kes; kesilmiş serinin
    # çıktısı tam serinin kesim günü dahil aynı günlerine eşit olmalı (TASARIM 5.12).
    tam = _karantina_(ham, duz, olay, pd.Timestamp("2024-12-31"))
    assert tam.tolist() == beklenen
    for son in tam.index:
        kesik = _karantina_(ham, duz, olay, son)
        assert kesik.tolist() == tam.loc[:son].tolist(), son
