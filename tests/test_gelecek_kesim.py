"""Gelecek verisi yok (SPEC 4): t gününe kadarki çıktı t'den sonraki satırlara bağlı değildir."""

import numpy as np
import pandas as pd
import pytest

from tansu import sinama, veri
from tansu.stratejiler import STRATEJILER
from tests.sentetik import (
    SABIT,
    YOLLAR,
    anlik,
    gartley_tekrar,
    gun_tablosu,
    rastgele_tablo,
)

BAS = pd.Timestamp("2021-01-04")
FIYAT_ALANLARI = [
    "aof",
    "yuksek",
    "dusuk",
    "kapanis",
    "ham_aof",
    "ham_yuksek",
    "ham_dusuk",
    "ham_kapanis",
    "hacim",
]


@pytest.mark.parametrize("ad", sorted(STRATEJILER))
def test_t_gunu_ciktisi_sonraki_gunlerden_bagimsiz(ad):
    strateji = STRATEJILER[ad]
    gun = gun_tablosu(YOLLAR[ad]())
    tam = strateji.sinyal(gun, SABIT[ad])
    assert tam["giris"].any()
    for t in range(60, len(gun), 7):
        kesik = strateji.sinyal(gun.iloc[: t + 1], SABIT[ad])
        pd.testing.assert_frame_equal(kesik, tam.iloc[: t + 1])


def semboller(ad):
    return {
        "YOL": gun_tablosu(YOLLAR[ad](), bas=BAS),
        "GT": gartley_tekrar(bas=BAS),
        "R1": rastgele_tablo(1, n=700, bas=BAS),
    }


def sil(a: veri.Anlik, k) -> veri.Anlik:
    return veri.Anlik(a.kimlik, a.fiyat[a.fiyat["tarih"] <= k], a.olaylar)


def boz(a: veri.Anlik, k, tohum) -> veri.Anlik:
    """k'den sonraki satırların fiyatı ve hacmi rastgele çöp (bazısı NaN)."""
    f = a.fiyat.copy()
    sonra = (f["tarih"] > k).to_numpy()
    r = np.random.default_rng(tohum)
    for alan in FIYAT_ALANLARI:
        cop = r.uniform(0.5, 300, sonra.sum())
        cop[r.random(len(cop)) < 0.1] = np.nan
        f.loc[sonra, alan] = cop
    return veri.Anlik(a.kimlik, f, a.olaylar)


@pytest.mark.slow
def test_yukleyici_kesilen_ya_da_bozulan_gelecekte_gecmis_gun_tablosunu_degistirmez():
    # Olay karşılaştırması kilit, tavan kapanışı ve ATR sütunlarını ancak bir işlem o güne denk gelirse görür.
    tablolar = {f"R{j}": rastgele_tablo(j, n=400, bas=BAS) for j in (1, 2)}
    a = anlik(tablolar)
    tam = sinama.gunler(a)
    takvim = pd.DatetimeIndex(sorted(a.fiyat["tarih"].unique()))
    kilit_oncesi = {
        takvim[max(takvim.get_loc(d) - 1, 0)]
        for g in tablolar.values()
        for d in g.index[g["kilit_tavan"] | g["kilit_taban"]]
    }
    assert kilit_oncesi
    for j, k in enumerate(sorted(kilit_oncesi | set(takvim[40::50]))):
        for tur, kesik_anlik in (("silme", sil(a, k)), ("çöp", boz(a, k, j))):
            kesik = sinama.gunler(kesik_anlik)
            for s in tam:
                pd.testing.assert_frame_equal(
                    kesik[s].loc[:k], tam[s].loc[:k], obj=f"{s} {k.date()} {tur}"
                )


def olaylar(kosu: sinama.Kosu, k) -> tuple[list, set]:
    """k'ye kadarki sinyaller ve dolum, kısmi çıkış ve çıkış olayları. Kesik koşunun `açık` işareti olay değildir."""
    s = kosu.sinyaller
    sinyaller = [tuple(x) for x in s[s["tarih"] <= k].itertuples(index=False)]
    sonuc = set()
    for r in kosu.islemler.itertuples():
        anahtar = (r.sembol, str(r.sinyal_tarihi.date()))
        if r.dolum_tarihi <= k:
            seviyeler = map(str, (r.dolum_fiyati, r.seviye, r.stop))
            sonuc.add((*anahtar, "dolum", r.dolum_tarihi, *seviyeler))
        for parca in filter(None, r.kismi.split("; ")):
            tarih, *kalan = parca.split(" ")
            if pd.Timestamp(tarih) <= k:
                sonuc.add((*anahtar, tarih, *kalan))
        if r.cikis_tarihi <= k and r.cikis_nedeni != "açık":
            sonuc.add((*anahtar, r.cikis_nedeni, r.cikis_tarihi, str(r.cikis_fiyati)))
    return sinyaller, sonuc


@pytest.mark.slow
@pytest.mark.parametrize("ad", sorted(STRATEJILER))
def test_yukleyiciden_kesilen_ya_da_bozulan_gelecek_gecmis_olaylari_degistirmez(ad):
    strateji, p = STRATEJILER[ad], SABIT[ad]
    tam_anlik = anlik(semboller(ad))
    son = tam_anlik.fiyat["tarih"].max()
    tam = sinama.calistir(strateji, sinama.gunler(tam_anlik), p, sinama.Donem(BAS, son))
    i = tam.islemler
    assert len(tam.sinyaller) > 1 and (i["cikis_nedeni"] != "açık").any()
    if strateji.cikis.hedef:
        assert i["cikis_nedeni"].str.startswith("hedef").any(), "hedef çıkışı yok"
    takvim = pd.DatetimeIndex(sorted(tam_anlik.fiyat["tarih"].unique()))
    olay_gunleri = {*tam.sinyaller["tarih"], *i["dolum_tarihi"], *i["cikis_tarihi"]}
    olay_gunleri |= {
        pd.Timestamp(parca.split(" ")[0])
        for x in i["kismi"]
        for parca in filter(None, x.split("; "))
    }
    kesimler = sorted(
        {
            takvim[max(takvim.get_loc(d) - geri, 0)]
            for d in olay_gunleri
            for geri in (0, 1)
        }
    )
    for j, k in enumerate(kesimler):
        beklenen = olaylar(tam, k)
        for tur, a in (("silme", sil(tam_anlik, k)), ("çöp", boz(tam_anlik, k, j))):
            kesik = sinama.calistir(strateji, sinama.gunler(a), p, sinama.Donem(BAS, k))
            assert olaylar(kesik, k) == beklenen, (
                f"{ad}: {k.date()} sonrası {tur} geçmişi değiştirdi"
            )
