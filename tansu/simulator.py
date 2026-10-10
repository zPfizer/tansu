"""Simülatör: tek hisse bölmesi (boyutlandırma, faiz, sermaye eğrisi) ve K2 sepeti (TASARIM 5.6, 5.7, 5.13).

Girdi motorun işlem tablosudur (`motor.sinama`). Evren süzgeci, kapanma (−%100), likidite, boyutlandırma,
faiz ve maruziyet eşleşmeli K2 burada uygulanır. Kurallar TASARIM 5.6 "Simülatör kuralları"nda.
"""

import numpy as np
import pandas as pd

from tansu import evren as evren_modulu

SERMAYE = 1_000_000.0
RISK, TAVAN, LIKIDITE, EN_FAZLA = 0.01, 0.10, 0.02, 10  # TASARIM 5.6
LIKIDITE_GUN = 10  # TASARIM 5.4
K2_MASRAF = 0.003  # TASARIM 5.7: sepet dengelemesi her zaman %0,3
MASRAFLAR = (0.001, 0.003, 0.005)  # TASARIM 5.4
BASLANGIC = "2015-12-01"  # TASARIM 5.6 simülatör kuralları
AILE = "ema_sikismasi"
SINIRLAR = ("risk", "tavan", "likidite", "nakit")  # eşitlikte bu sıra


def evrenler(anlik, bas, son) -> dict:
    """Ay → evren listesi (`evren.evren`), `bas` ayından `son` ayına."""
    return {
        ay: evren_modulu.evren(anlik, ay.to_timestamp())
        for ay in pd.period_range(pd.Timestamp(bas), pd.Timestamp(son), freq="M")
    }


def uyeler(anlik, evr, bas) -> pd.DataFrame:
    """Evren üyesi hisse-günler (sembol, tarih): hissenin o ayın evreninde olduğu fiyat satırları (TASARIM 5.13)."""
    cift = pd.DataFrame(
        [(s, ay) for ay, liste in evr.items() for s in liste], columns=["sembol", "ay"]
    )
    f = anlik.fiyat.loc[anlik.fiyat["tarih"] >= bas, ["sembol", "tarih"]]
    f = f.assign(ay=f["tarih"].dt.to_period("M")).merge(cift, on=["sembol", "ay"])
    return f[["sembol", "tarih"]].reset_index(drop=True)


def _oran(x, y):
    with np.errstate(divide="ignore", invalid="ignore"):
        r = x / y
    return np.where(np.isfinite(r) & (y > 0), r, 1.0)


def _sepet(gunler, days, evr, kapanma, C, A):
    """K2 sepet endeksi (başlangıç 1): ay başı AOF'ta eşit ağırlığa dengelenir, %0,3 devir masrafı (TASARIM 5.7)."""
    kol = {s: i for i, s in enumerate(C.columns)}
    Cn, An = C.to_numpy(), A.to_numpy()
    pos = gunler.get_indexer(days)
    V, nakit, B = np.zeros(len(kol)), 1.0, []
    for i, d in enumerate(days):
        c = Cn[pos[i]]
        a = np.where(np.isnan(An[pos[i]]), c, An[pos[i]])
        onceki = Cn[pos[i] - 1] if pos[i] > 0 else c
        if i == 0 or d.month != days[i - 1].month or d.year != days[i - 1].year:
            V = V * _oran(a, onceki)
            toplam = V.sum() + nakit
            uye = [kol[s] for s in evr.get(d.to_period("M"), []) if s in kol]
            yeni = np.zeros(len(kol))
            yeni[uye] = 1 / len(uye) if uye else 0.0
            toplam *= 1 - K2_MASRAF * np.abs(yeni - V / toplam).sum()
            V, nakit = yeni * toplam, 0.0 if uye else toplam
            V = V * _oran(c, a)
        else:
            V = V * _oran(c, onceki)
        for s in kapanma.get(d, ()):
            V[kol[s]] = 0.0
        B.append(V.sum() + nakit)
    return pd.Series(B, index=days)


def _kural(t, days, gunler, g, C, Lq, masraf):
    """Tek sürekli portföy: (alınan {satır: (adet, bağlayıcı sınır, planlanan risk / özkaynak)}, özkaynak, pay, reddedilen)."""
    kol = {s: i for i, s in enumerate(C.columns)}
    Cn = C.to_numpy()
    pos = gunler.get_indexer(days)
    giris = {d: grup.index.tolist() for d, grup in t.groupby("giris_tarih")}
    cikis = {}
    for k, d in t["cikis_tarih"].items():
        cikis.setdefault(d, []).append(k)
    # K1 bu işlevi tekrar tekrar çağırır: pandas skaler erişimi yerine sütunlar bir kez sözlüğe alınır (sonuç aynı).
    sembol, gfiyat, cfiyat = (
        t[c].to_dict() for c in ("sembol", "giris_fiyat", "cikis_fiyat")
    )
    adet0, risk0 = t["adet"].to_dict(), t["planlanan_risk"].to_dict()
    satir = Lq.index.get_indexer(t["sinyal_tarih"])
    if (satir < 0).any():
        raise KeyError("sinyal günü likidite tablosunda yok")
    lq = dict(
        zip(t.index, Lq.to_numpy()[satir, [Lq.columns.get_loc(s) for s in t["sembol"]]])
    )
    acik, alinan, reddedilen = {}, {}, 0
    nakit, ozk_onceki, ozk, pay = SERMAYE, SERMAYE, [], []

    def cik(d):
        nonlocal nakit
        for k in cikis.get(d, ()):
            if k in acik:
                nakit += acik.pop(k) * cfiyat[k] * (1 - masraf)

    for i, d in enumerate(days):
        nakit *= 1 + g[i]
        cik(d)
        adaylar = sorted(giris.get(d, ()), key=lambda k: (-lq[k], sembol[k]))
        for k in adaylar:
            sinir = [
                RISK * ozk_onceki / (risk0[k] / adet0[k]),
                TAVAN * ozk_onceki / gfiyat[k],
                LIKIDITE * lq[k] / gfiyat[k],
                nakit / (gfiyat[k] * (1 + masraf)),
            ]
            adet = int(np.floor(min(sinir)))
            if len(acik) >= EN_FAZLA or adet < 1:
                reddedilen += 1
                continue
            nakit -= adet * gfiyat[k] * (1 + masraf)
            acik[k] = adet
            alinan[k] = (
                adet,
                SINIRLAR[int(np.argmin(sinir))],
                adet * risk0[k] / adet0[k] / ozk_onceki,
            )
        cik(d)  # aynı gün girip çıkan (giriş günü stop) işlemler
        fiyat = [Cn[pos[i], kol[sembol[k]]] for k in acik]
        mv = sum(
            a * (p if np.isfinite(p) else gfiyat[k])
            for (k, a), p in zip(acik.items(), fiyat)
        )
        ozk_onceki = nakit + mv
        ozk.append(ozk_onceki)
        pay.append(mv / ozk_onceki)
    return alinan, np.array(ozk), np.array(pay), reddedilen


def _alinanlar(t, alinan, masraf) -> pd.DataFrame:
    """Alınan işlem tablosu: motor satırı + adet, bağlayıcı sınır, getiri (masraf dahil)."""
    s = t.loc[list(alinan)].copy()
    adet = pd.Series({k: v[0] for k, v in alinan.items()})
    s["planlanan_risk"] = adet * s["planlanan_risk"] / s["adet"]
    s["adet"], s["bagli"] = adet, pd.Series({k: v[1] for k, v in alinan.items()})
    s["gerceklesen_kayip"] = s["adet"] * (s["giris_fiyat"] - s["cikis_fiyat"]).clip(
        lower=0
    )
    s["getiri"] = (
        s["cikis_fiyat"] * (1 - masraf) / (s["giris_fiyat"] * (1 + masraf)) - 1
    )
    s["aile"] = AILE
    return s[
        [
            "sembol",
            "aile",
            "sinyal_tarih",
            "giris_tarih",
            "giris_fiyat",
            "cikis_tarih",
            "cikis_fiyat",
            "neden",
            "adet",
            "getiri",
            "planlanan_risk",
            "gerceklesen_kayip",
            "bagli",
        ]
    ].reset_index(drop=True)


def _yillik(ozk, k2) -> pd.DataFrame:
    """Yıl sonu özkaynaklarından yıllık getiri; ilk yıl SERMAYE'den (TASARIM 5.7)."""

    def getiri(s):
        son = s.groupby(s.index.year).last()
        return son / son.shift(1, fill_value=SERMAYE) - 1

    y = pd.DataFrame({"kural": getiri(ozk), "k2": getiri(k2)})
    return y.assign(fazla=y["kural"] - y["k2"])


def _paketle(t, days, g, rb, sepet, kural, masraf) -> dict:
    alinan, ozk, pay, reddedilen = kural
    ozk, k2 = pd.Series(ozk, index=days), pd.Series(k2_egri(pay, rb, g), index=days)
    islem = _alinanlar(t, alinan, masraf)
    return {
        "islemler": islem,
        "ozkaynak": ozk,
        "k2": k2,
        "sepet": sepet,
        "yatirim": pd.Series(pay, index=days),
        "yillik": _yillik(ozk, k2),
        "reddedilen": reddedilen,
        "bagli": islem["bagli"]
        .value_counts()
        .reindex(SINIRLAR, fill_value=0)
        .to_dict(),
        "ort_risk": float(np.mean([v[2] for v in alinan.values()])) if alinan else 0.0,
        "kapanma": int((islem["neden"] == "kapanma").sum()),
        "karantina_cikisi": int((islem["neden"] == "karantina").sum()),
    }


def zemin(anlik, evr, days, ekstra, kg) -> dict:
    """İki bölmenin ortak girdisi: fiyat matrisleri, günlük faiz ve K2 sepeti (`days` üzerinde; `kg`: kapanan hisseler)."""
    gunler = anlik.gunler
    kapanma = {}
    for s, (_, gun) in kg.items():
        kapanma.setdefault(gun, []).append(s)
    semboller = sorted({s for liste in evr.values() for s in liste} | set(ekstra))
    f = anlik.fiyat[anlik.fiyat["sembol"].isin(semboller)]
    kolon = lambda alan: f.pivot(index="tarih", columns="sembol", values=alan).reindex(  # noqa: E731
        index=gunler, columns=semboller
    )
    C, A = kolon("kapanis").ffill(), kolon("aof")
    Lq = kolon("hacim").fillna(0).rolling(LIKIDITE_GUN, min_periods=1).median()
    kapanma = {d: [s for s in l if s in C.columns] for d, l in kapanma.items()}
    # faiz: her gece, önceki işlem gününden bu güne (TASARIM 5.6)
    oran = anlik.faiz_gunluk(days[0], days[-1]) / 36500
    onceki = oran.cumsum().shift(1, fill_value=0.0)
    g = np.concatenate(
        [
            [0.0],
            (
                onceki.reindex(days[1:]).to_numpy()
                - onceki.reindex(days[:-1]).to_numpy()
            ),
        ]
    )
    sepet = _sepet(gunler, days, evr, kapanma, C, A)
    rb = sepet.to_numpy() / np.concatenate([[1.0], sepet.to_numpy()[:-1]]) - 1
    return {
        "C": C,
        "A": A,
        "Lq": Lq,
        "g": g,
        "sepet": sepet,
        "rb": rb,
        "kapanma": kapanma,
    }


def k2_egri(pay, rb, g, baslangic=SERMAYE) -> np.ndarray:
    """K2 özkaynağı: her gün sepet getirisi hisse payı kadar, kalanı gecelik faiz (TASARIM 5.7)."""
    k2, e = [], baslangic
    for p, r, gece in zip(pay, rb, g):
        e *= 1 + p * r + (1 - p) * gece
        k2.append(e)
    return np.array(k2)


def ilk_gun(anlik, bas=BASLANGIC):
    gunler = anlik.gunler
    return gunler[gunler >= pd.Timestamp(bas)][0]


def _suzgec(islemler, evr, ilk, kg) -> tuple:
    """(işlem tablosu, kapanma sayısı): evren süzgeci ve kapanan hisse (TASARIM 5.2, 5.6). Gerçek koşu ve K1 aynı yolu kullanır."""
    islemler = islemler.astype(
        {a: "datetime64[ns]" for a in ("sinyal_tarih", "giris_tarih", "cikis_tarih")}
    )
    t = islemler.loc[islemler["sinyal_tarih"] >= ilk].copy()
    ay = t["sinyal_tarih"].dt.to_period("M")
    t = t.loc[
        np.array([s in evr.get(a, ()) for s, a in zip(t["sembol"], ay)], dtype=bool)
    ].reset_index(drop=True)
    sayi = 0
    for (
        k,
        r,
    ) in (
        t.iterrows()
    ):  # kapanan hisse (TASARIM 5.2): açık pozisyon kapanma gününde 0 fiyatla kapanır
        if r.sembol in kg:
            son, gun = kg[r.sembol]
            if r.giris_tarih <= gun and (r.cikis_tarih > son or r.neden == "veri_sonu"):
                t.loc[k, ["cikis_tarih", "cikis_fiyat", "neden"]] = [
                    gun,
                    0.0,
                    "kapanma",
                ]
                sayi += 1
    return t, sayi


def k1_baglam(anlik, evr, bas=BASLANGIC) -> dict:
    """K1 tekrarlarının ortak girdisi: fiyat matrisleri, faiz ve K2 sepeti bir kez hesaplanır (TASARIM 5.7)."""
    gunler = anlik.gunler
    ilk = ilk_gun(anlik, bas)
    days = gunler[gunler >= ilk]  # kapanma günleri de takvimdedir
    kap = evren_modulu.kapananlar(anlik)
    kg = dict(zip(kap["sembol"], zip(kap["son_islem"], kap["kapanma_gunu"])))
    z = zemin(anlik, evr, days, set(), kg)
    onceki = np.concatenate([[1.0], z["sepet"].to_numpy()[:-1]])
    return {
        "gunler": gunler,
        "ilk": ilk,
        "days": days,
        "kg": kg,
        "z": z,
        "evr": evr,
        "sepet_onceki": pd.Series(onceki, index=days),
    }


def sepet_getirisi(b, giris, cikis) -> np.ndarray:
    """Sepet getirisi: K2 sepet endeksinin önceki-kapanış değerleri oranı (TASARIM 5.7 "K1 uygulama kuralları")."""
    so = b["sepet_onceki"]
    return (
        so.reindex(pd.DatetimeIndex(cikis)).to_numpy()
        / so.reindex(pd.DatetimeIndex(giris)).to_numpy()
        - 1
    )


def k1_islemler(islemler, b, masraf) -> pd.DataFrame:
    """Motor işlemlerinden simülatörün alacağı işlemler (`_alinanlar` sütunları) ve sepete göre `fazla` getiri."""
    t, _ = _suzgec(islemler, b["evr"], b["ilk"], b["kg"])
    z = b["z"]
    alinan = (
        _kural(t, b["days"], b["gunler"], z["g"], z["C"], z["Lq"], masraf)[0]
        if len(t)
        else {}
    )
    s = _alinanlar(t, alinan, masraf) if alinan else _alinanlar(t.iloc[:0], {}, masraf)
    return s.assign(
        fazla=s["getiri"] - sepet_getirisi(b, s["giris_tarih"], s["cikis_tarih"])
        if len(s)
        else []
    )


def calistir(
    anlik, islemler, dusen=0, bas=BASLANGIC, masraflar=MASRAFLAR, evr=None
) -> dict:
    """Motor işlemlerinden her masraf düzeyi için sermaye eğrisi ve K2; `{"masraf": {m: ...}, "bilgi": {...}}`.

    `evr`: `evrenler` çıktısı; verilmezse hesaplanır (kosu motora vermek için bir kez hesaplayıp geçirir)."""
    gunler = anlik.gunler
    ilk = ilk_gun(anlik, bas)
    days = gunler[gunler >= ilk]
    evr = evr or evrenler(anlik, ilk, days[-1])
    uye = uyeler(anlik, evr, ilk)
    bos_tablo = set(anlik.fiyat["sembol"]) - set(anlik.olaylar["sembol"])
    olay_tablo = anlik.olay_uyarilari.reindex(columns=["sembol", "tarih"]).merge(
        uye, on=["sembol", "tarih"]
    )
    bilgi = {
        "basla": ilk,
        "bitis": days[-1],
        "uye_gun": len(uye),
        "uye_sembol": uye["sembol"].nunique(),
        "oran_uye": anlik.oranlar(uye)[:2],
        "oran_tum": anlik.oranlar()[:2],
        "sorunlar": anlik.sorunlar_uye(uye),
        "sorunlar_tum": anlik.sorunlar,
        "iptal": dusen,
        "olay_bos_uye_sembol": len(bos_tablo & set(uye["sembol"])),
        "olay_uyari_uye": len(olay_tablo),
        "olay_uyari_bos_tablo": int(olay_tablo["sembol"].isin(bos_tablo).sum()),
        "faiz_son_degisim": anlik.faiz_son_degisim,
    }
    kap = evren_modulu.kapananlar(anlik)
    bilgi["kapananlar"] = len(kap)
    kg = dict(zip(kap["sembol"], zip(kap["son_islem"], kap["kapanma_gunu"])))
    t, bilgi["kapanma"] = _suzgec(islemler, evr, ilk, kg)
    days = pd.DatetimeIndex(sorted({*days, *t["giris_tarih"], *t["cikis_tarih"]}))
    z = zemin(anlik, evr, days, set(t["sembol"]), kg)
    C, Lq, g, rb, sepet = z["C"], z["Lq"], z["g"], z["rb"], z["sepet"]
    sonuc = {}
    for m in masraflar:
        sonuc[m] = _paketle(
            t, days, g, rb, sepet, _kural(t, days, gunler, g, C, Lq, m), m
        )
    return {"masraf": sonuc, "bilgi": bilgi}
