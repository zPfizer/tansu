"""Testlerin yapay fiyat serileri. Gerçek veri yok (SPEC 10)."""

import numpy as np
import pandas as pd

from tansu import gostergeler, veri


def gun_tablosu(kapanis, yuksek=None, dusuk=None, aof=None, bas="2022-01-03"):
    """`veri.gunluk` sözleşmesinde yapay tablo; `atr` sütunu 0,1."""
    kapanis = np.asarray(kapanis, float)
    yuksek = kapanis + 0.05 if yuksek is None else np.asarray(yuksek, float)
    dusuk = kapanis - 0.05 if dusuk is None else np.asarray(dusuk, float)
    aof = kapanis if aof is None else np.asarray(aof, float)
    n = len(kapanis)
    g = pd.DataFrame(
        {
            "aof": aof,
            "yuksek": yuksek,
            "dusuk": dusuk,
            "kapanis": kapanis,
            "hacim": 1e6,
            "ham_yuksek": yuksek,
            "ham_dusuk": dusuk,
            "ham_kapanis": kapanis,
            "kilit_tavan": False,
            "kilit_taban": False,
            "tavan_kapanis": False,
            "karantina": False,
            "uye": True,
            "xu100": 10000.0,
            "atr": 0.1,
        },
        index=pd.bdate_range(bas, periods=n, name="tarih"),
    )
    return g


def piyasa(sembol=16, donem=40, bas="2019-01-02", son="2026-09-30"):
    t = np.arange(len(pd.bdate_range(bas, son)))
    return {
        f"S{j:02d}": gun_tablosu(
            100 * (1 + 0.15 * np.sin(2 * np.pi * (t + 2.5 * j) / donem)), bas=bas
        )
        for j in range(sembol)
    }


def ortalama_yolu(gun=720, periyot=120, genlik=10.0):
    """Sinüs dalgası: EMA 50/200 ısınmadan (500 gün) sonra yukarı ve aşağı kesişir."""
    return 100 + genlik * np.sin(2 * np.pi * np.arange(gun) / periyot)


def gartley_yolu(x=10.0, a=20.0, ab=0.618, bc=0.618, adim=20, bas=15.0):
    """Doğrusal bacaklar: başlangıç → X → A → B → C → D'nin biraz altı → A. Her bacak `adim` gün."""
    b = a - ab * (a - x)
    c = b + bc * (a - b)
    d = a - 0.786 * (a - x)
    duraklar = [bas, x, a, b, c, d - 0.1, a]
    yol = [duraklar[0]]
    for once, sonra in zip(duraklar, duraklar[1:], strict=False):
        yol += list(np.linspace(once, sonra, adim + 1)[1:])
    return np.array(yol)


# Her kayıtlı stratejinin varsayılan setle sinyal veren yolu; varsayılan bekçisi (`test_varsayilan`) bunu kullanır.
YOLLAR = {"gartley": gartley_yolu, "ortalama-kesisim": ortalama_yolu}

# Testlerin sabit parametreleri, her stratejinin `varsayilan` anahtarlarıyla. Varsayılan değişikliği test düzeltmesi
# gerektirmesin diye testler varsayılanı değil bunu okur.
SABIT: dict[str, dict] = {
    "gartley": {
        "pivot": "sag_bar_15",
        "tolerans": 0.05,
        "gecerlilik": 10,
        "stop": "X",
        "rr_min": "kapali",
    },
    "ortalama-kesisim": {"ortalama": "EMA", "cift": "50/200", "teyit_gun": 0},
}


def gartley_tekrar(n=600, tohum=11, carpan=1.0, bas="2021-01-04"):
    """Gartley yolunun gürültülü tekrarı: birçok kurulum, hedef ve stop çıkışları. Her parça A'da başlar ve biter."""
    rng = np.random.default_rng(tohum)
    parcalar = []
    while sum(map(len, parcalar)) < n:
        parcalar.append(gartley_yolu(adim=int(rng.integers(12, 24)), bas=20.0))
    kap = np.concatenate(parcalar)[:n] * carpan * (1 + rng.normal(0, 0.003, n))
    return gun_tablosu(kap, bas=bas)


def rastgele_tablo(tohum, n=1500, bas="2021-01-04", bos=0.02, kilit=0.015):
    """Tohumlu rastgele yürüyüş, `gun_tablosu` sözleşmesinde; fiyatlar kuruşa yuvarlı, böylece eşit fiyatlar da olur.

    AOF ve kapanış yüksek-düşük aralığında. `bos` payı gün fiyatsız (bütün fiyatlar NaN; yürüyüş o gün durur). `kilit`
    payı gün tavan, bir o kadarı taban kilidi: getiri tam ±%10, yüksek = düşük = AOF = kapanış; `veri` yükleyicisi de
    bunları kilit görür. Diğer günlerin getirisi ±%8 içinde. `atr` ürünün ATR(14)'ü (başta ve fiyatsız günde NaN)."""
    r = np.random.default_rng(tohum)
    zar = r.random(n)
    fiyatsiz = zar < bos
    tavan = (zar >= bos) & (zar < bos + kilit)
    taban = (zar >= bos + kilit) & (zar < bos + 2 * kilit)
    getiri = np.clip(r.normal(0, 0.02, n), -0.08, 0.08)
    getiri[fiyatsiz] = 0.0
    getiri[tavan], getiri[taban] = 0.10, -0.10
    kap = np.empty(n)
    once = 50.0
    for i in range(n):
        kap[i] = once = round(once * (1 + getiri[i]), 2)
    onceki = np.r_[50.0, kap[:-1]]
    aof = np.round(onceki * (1 + np.clip(r.normal(0, 0.01, n), -0.05, 0.05)), 2)
    yuk = np.round(np.maximum(aof, kap) * (1 + np.abs(r.normal(0, 0.01, n))), 2)
    dus = np.round(np.minimum(aof, kap) * (1 - np.abs(r.normal(0, 0.01, n))), 2)
    kilitli = tavan | taban
    aof[kilitli] = yuk[kilitli] = dus[kilitli] = kap[kilitli]
    for dizi in (aof, yuk, dus, kap):
        dizi[fiyatsiz] = np.nan
    g = gun_tablosu(kap, yuksek=yuk, dusuk=dus, aof=aof, bas=bas)
    g["kilit_tavan"] = g["tavan_kapanis"] = tavan
    g["kilit_taban"] = taban
    g["atr"] = gostergeler.atr_basit(g["yuksek"], g["dusuk"], g["kapanis"])
    return g


def anlik(tablolar: dict[str, pd.DataFrame]) -> veri.Anlik:
    """`gun_tablosu` tablolarından ürünün okuduğu anlık görüntü (`sinama.gunler` ve `__main__` girdisi); olay yok.
    Bayrak ve `atr` sütunlarını ürün fiyatlardan yeniden hesaplar."""
    parcalar = []
    for sembol, g in tablolar.items():
        f = g[["aof", "yuksek", "dusuk", "kapanis", "hacim", "xu100"]].copy()
        f["ham_aof"], f["ham_yuksek"] = g["aof"], g["yuksek"]
        f["ham_dusuk"], f["ham_kapanis"] = g["dusuk"], g["kapanis"]
        parcalar.append(f.reset_index().assign(sembol=sembol))
    olaylar = pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    return veri.Anlik("20260101-0000", pd.concat(parcalar, ignore_index=True), olaylar)
