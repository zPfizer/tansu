"""Geleceği görmeme testi (TASARIM 5.12, B-18): veriyi t'de kes; t öncesi çıktılar değişmesin.

Tek parametrik test: bileşen × kesim günü. Sentetik dünya (`denetim.dunya`, 24 hisse, 900 gün; 02.01.2012'den). Kesilen
anlık görüntüde t'den sonraki fiyat satırları ve faiz değişimleri yoktur; tam görüntünün t'ye kadarki çıktısı aynı olmalı.
Kapsam: evren, göstergeler, EMA ve çift sinyalleri, çift seçimi, likidite medyanı, faiz hizalaması (ve K2 sepeti).
"""

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
    veri,
)

KESIM = [
    "2014-09-30",
    "2015-01-15",
    "2015-03-02",
    "2014-12-31",  # yılın son işlem günü: biten yıl 2014 karşılaştırılır (yillik_fazla_)
]  # tam veri 2015-06'ya dek; ısınma (500 gün) 2013-11'de biter
BAS = "2013-12-02"


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
            "ema": lambda a: gostergeler.ema(seri(a, s), 20),
            "sma": lambda a: gostergeler.sma(seri(a, s), 50),
            "atr": lambda a: gostergeler.atr(
                seri(a, s, "yuksek"), seri(a, s, "dusuk"), seri(a, s), 14
            ),
            "sikisma": lambda a: gostergeler.sikisma_orani(seri(a, s)),
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


@pytest.mark.parametrize("kesim", KESIM)
@pytest.mark.parametrize(
    "bilesen",
    [
        evren_,
        gostergeler_,
        ema_sinyal_,
        cift_sinyal_,
        cift_secimi_,
        zemin_,
        yillik_fazla_,
    ],
    ids=lambda f: f.__name__,
)
def test_t_den_sonrasi_veri_t_oncesi_ciktiyi_degistirmez(tam, bilesen, kesim):
    t = pd.Timestamp(kesim)
    bilesen(tam, kes(tam, t), t)
