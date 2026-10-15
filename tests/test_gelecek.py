"""Geleceği görmeme testi (TASARIM 5.12, B-18): veriyi t'de kes; t öncesi çıktılar değişmesin.

Tek parametrik test: bileşen × kesim günü. Sentetik dünya (`denetim.dunya`, 24 hisse, 900 gün; 02.01.2012'den). Kesilen
anlık görüntüde t'den sonraki fiyat satırları ve faiz değişimleri yoktur; tam görüntünün t'ye kadarki çıktısı aynı olmalı.
Kapsam: evren, göstergeler, EMA ve çift sinyalleri, çift seçimi, likidite medyanı, faiz hizalaması (ve K2 sepeti).
"""

import numpy as np
import pandas as pd
import pytest

from tansu import aileler, cift, ciftbolme, denetim, evren, gostergeler, simulator, veri

KESIM = [
    "2014-09-30",
    "2015-01-15",
    "2015-03-02",
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


@pytest.mark.parametrize("kesim", KESIM)
@pytest.mark.parametrize(
    "bilesen",
    [evren_, gostergeler_, ema_sinyal_, cift_sinyal_, cift_secimi_, zemin_],
    ids=lambda f: f.__name__,
)
def test_t_den_sonrasi_veri_t_oncesi_ciktiyi_degistirmez(tam, bilesen, kesim):
    t = pd.Timestamp(kesim)
    bilesen(tam, kes(tam, t), t)


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
