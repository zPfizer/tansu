"""Evren: ay başı büyük-100, likidite eleği, şirket başına tek kod, kapanma (TASARIM 5.2)."""

import numpy as np
import pandas as pd

from tansu.veri import VeriHatasi

PENCERE = 60  # likidite medyanı ve durdurma eşiği, işlem günü
# Aynı şirketin birden çok pay kodu (elle yazılmış). Kaynak: KAP şirket listesinde (borsapy 0.11.0 `companies`)
# bir satırda birden çok kod olanlar, aracı kurum üye kodları (TGB, THL...) ayıklanarak: yalnız bu ikisi pay grubu.
COKLU_KOD = [("ISCTR", "ISATR", "ISBTR", "ISKUR"), ("KRDMA", "KRDMB", "KRDMD")]


def tum_semboller(bugun, kapanan) -> list:
    """Bugünkü bütün paylar (borsapy) ve işlemi kapanmış kodlar (`kaynak.kapanan_kodlar`), tekrarsız."""
    return sorted(set(bugun) | set(kapanan["kod"]))


def evren(anlik, tarih, en_buyuk=100, elenen=0.20, coklu=COKLU_KOD) -> list:
    """`tarih`in ayında yeni giriş için taranabilecek hisseler, piyasa değerine göre büyükten küçüğe.

    Ayın ilk işlem gününden önceki son kapanışın piyasa değeri ve o güne kadarki 60 günün medyan TL
    hacmi kullanılır. Sıra: o gün işlem görmeyen düşer, şirket başına tek kod (hacmi yüksek) kalır,
    medyan hacimde en alttaki %`elenen` elenir, kalanların en büyük `en_buyuk` tanesi alınır.
    """
    gunler = anlik.gunler
    ilk = gunler[gunler >= pd.Timestamp(tarih).replace(day=1)]
    if len(ilk) == 0:
        raise VeriHatasi(f"{tarih}: ayında işlem günü yok")
    onceki = gunler[gunler < ilk[0]]
    if len(onceki) == 0:
        return []
    ref, pencere = onceki[-1], onceki[-PENCERE:]
    f = anlik.fiyat
    gun = f[f["tarih"] == ref]
    gun = gun[(gun["hacim"] > 0) & (gun["pd"] > 0)].set_index("sembol")["pd"]
    hacim = (f[f["tarih"].isin(pencere)].pivot(index="tarih", columns="sembol", values="hacim")
             .reindex(pencere).fillna(0).median())  # eksik gün hacmi 0 sayılır
    hacim = hacim.reindex(gun.index)
    for grup in coklu:
        var = [s for s in grup if s in hacim.index]
        hacim = hacim.drop([s for s in var if s != hacim[var].idxmax()]) if var else hacim
    gun = gun.reindex(hacim.index)
    hacim = hacim.sort_values(kind="stable")
    kalan = hacim.index[int(len(hacim) * elenen):]
    return list(gun[kalan].sort_values(ascending=False, kind="stable").index[:en_buyuk])


def kapananlar(anlik, nedeni_bilinen=()) -> pd.DataFrame:
    """60 işlem gününden uzun durdurulan hisseler: sembol, son_islem, kapanma_gunu, getiri.

    `kapanma_gunu` durdurmanın 61. işlem günüdür. `getiri` = −1,0 (−%100); nedeni bilinen hissede NaN,
    yani son fiyat kullanılır.
    """
    gunler = anlik.gunler
    f = anlik.fiyat[anlik.fiyat["hacim"] > 0]
    satirlar = []
    for s, g in f.groupby("sembol", sort=False):
        poz = np.unique(gunler.get_indexer(g["tarih"]))
        poz = poz[poz >= 0]
        sonraki = np.append(poz[1:], len(gunler))  # son işlemden sonra takvim sonuna kadar
        boslar = np.nonzero(sonraki - poz - 1 > PENCERE)[0]
        if len(boslar):
            i = poz[boslar[0]]
            satirlar.append({"sembol": s, "son_islem": gunler[i], "kapanma_gunu": gunler[i + PENCERE + 1],
                             "getiri": np.nan if s in nedeni_bilinen else -1.0})
    return pd.DataFrame(satirlar, columns=["sembol", "son_islem", "kapanma_gunu", "getiri"])
