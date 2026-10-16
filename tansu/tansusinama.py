"""Tansu sınaması (TASARIM 5.14): Tansu'nun kendi sınama yöntemi.

Her hisse (çift ailesinde her çift) kendi ızgarasıyla, bütün dönemde, masraf %0,10 ile koşulur. Sağlam bölge seçilir,
sonuç al-tut ve Tansu'nun tablo ölçüleriyle yan yana verilir. Kabul kararına girmez (5.12), kart üretmez, m'yi artırmaz
(5.11). Hash dışıdır (`kayit.HASH_DISI`). İş birimi bir hisse ya da bir çifttir; sonuç işçi sayısından bağımsızdır.
"""

import concurrent.futures
import datetime as dt
import itertools
import json
import os
import shutil
import subprocess
import time
import uuid
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import psutil

from tansu import aileler as aileler_
from tansu import ciftbolme, kayit, motor, rapor, saglamlik, simulator, veri

MASRAF = 0.001  # TASARIM 5.14: her yönde %0,10, kayma yok
SUPHELI_KAZANMA = 0.90  # TASARIM 5.14: kazanma oranı bu değerden küçük değilse "şüpheli: aşırı uyum" (YORUM)
AZ_ISLEM = 5  # TASARIM 5.14: Tansu'nun tablosundaki süzgeç "İşlem >= 5"
ISCI_BELLEK_GB = 0.25  # ölçülen işçi başı tepe bellek 0,17 GB + pay (TASARIM 5.14 Makine ve paralellik)
BASLANGIC = simulator.BASLANGIC
EGITIM_YIL = 2  # TASARIM 5.14 ileri yürüme: en az 2 tam eğitim yılı
CIFT_ISINMA = 252  # TASARIM 5.14 Dönem: çiftte ısınma 252 işlem günü
AILELER = (simulator.AILE, ciftbolme.AILE)
IZGARA = {
    simulator.AILE: saglamlik.IZGARA[simulator.AILE],
    ciftbolme.AILE: {"z_pencere": [60, 120], "z_esik": [1.5, 2.0, 2.5]},
}


def islem_getirisi(giris, cikis, m=MASRAF) -> float:
    return float(cikis * (1 - m) / (giris * (1 + m)) - 1)


def makine() -> dict:
    """Mantıksal ve fiziksel çekirdek, boş ve toplam bellek (GB), GPU adı (nvidia-smi yoksa ya da yanıt vermezse None);
    TASARIM 5.14 Makine ve paralellik."""
    bellek = psutil.virtual_memory()
    gpu, smi = None, shutil.which("nvidia-smi")
    if smi:
        try:
            cikti = subprocess.run(
                [smi, "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            gpu = cikti.stdout.strip() or None
        except OSError, subprocess.TimeoutExpired:
            gpu = None
    return {
        "cekirdek": os.cpu_count(),
        "fiziksel_cekirdek": psutil.cpu_count(logical=False) or os.cpu_count(),
        "bellek_bos_gb": round(bellek.available / 2**30, 2),
        "bellek_toplam_gb": round(bellek.total / 2**30, 2),
        "gpu": gpu,
    }


def isci_sayisi(
    cekirdek, bellek_bos_gb, is_sayisi, isci_bellek_gb=ISCI_BELLEK_GB
) -> int:
    """min(çekirdek (`calistir` fiziksel çekirdeği verir), boş bellek × 0,8 / işçi başı bellek, iş sayısı); en az 1 (TASARIM 5.14)."""
    return max(1, min(cekirdek, int(bellek_bos_gb * 0.8 / isci_bellek_gb), is_sayisi))


def olculer(getiriler, tutma, egri, pozisyonda) -> dict:
    """Tansu'nun tablo sütunları (TASARIM 5.14).

    `getiriler`: işlem getirileri; `tutma`: işlem başına tutma günü; `egri`: dönemin her günü için kapanış özkaynağı
    (başlangıç değeri 1); `pozisyonda`: pozisyonda kapanan gün sayısı."""
    r = np.asarray(getiriler, dtype=float)
    deger = np.concatenate(([1.0], np.asarray(egri, dtype=float)))
    gunluk = deger[1:] / deger[:-1] - 1
    kazanc, kayip = r[r > 0], r[r <= 0]
    n = len(r)
    sapma = gunluk.std(ddof=1) if len(gunluk) > 1 else 0.0
    max_dd = float((deger / np.maximum.accumulate(deger) - 1).min())
    kazanma = len(kazanc) / n if n else None
    bayraklar = []
    if kazanma is not None and kazanma >= SUPHELI_KAZANMA:
        bayraklar.append("şüpheli: aşırı uyum")
    if n < AZ_ISLEM:
        bayraklar.append("az işlem")
    return {
        "islem": n,
        "kazanma": kazanma,
        "kazanan": len(kazanc),
        "kaybeden": len(kayip),
        "kar_carpani": float(kazanc.sum() / abs(kayip.sum()))
        if kayip.sum() != 0
        else None,
        "ort_islem": float(r.mean()) if n else None,
        "medyan_islem": float(np.median(r)) if n else None,
        "net": float(np.prod(1 + r) - 1),
        "max_dd": max_dd,
        "sharpe": float(gunluk.mean() / sapma * np.sqrt(252)) if sapma > 0 else None,
        "calmar": float((deger[-1] ** (252 / len(gunluk)) - 1) / abs(max_dd))
        if max_dd < 0
        else None,
        "ort_tutma": float(np.mean(tutma)) if n else None,
        "maruziyet": pozisyonda / len(gunluk),
        "kazanc_kayip": float(kazanc.mean() / abs(kayip.mean()))
        if len(kazanc) and len(kayip) and kayip.mean() != 0
        else None,
        "bayraklar": bayraklar,
    }


def saglam_bolge(net) -> dict:
    """Sağlam bölge (TASARIM 5.14): hücre ve bütün komşuları (tek eksende bir adım) net > 0.

    `saglam`: ızgara biçiminde bool; `secilen`: sağlam hücreler içinde komşuluğunun (kendisi dahil) en küçük neti en büyük
    olan, eşitlikte düz sıradaki (C sırası) ilk, yoksa None; `en_iyi`: en büyük net, eşitlikte ilk; `para_cikmaz`: en iyi ≤ 0."""
    net = np.asarray(net, dtype=float)
    komsuluk = net.copy()  # kendisi ve komşuları üzerinde en küçük net
    for eksen, yon in itertools.product(range(net.ndim), (1, -1)):
        hedef = [slice(None)] * net.ndim
        kaynak = [slice(None)] * net.ndim
        hedef[eksen], kaynak[eksen] = (
            (slice(None, -1), slice(1, None))
            if yon == 1
            else (slice(1, None), slice(None, -1))
        )
        hedef, kaynak = tuple(hedef), tuple(kaynak)
        komsuluk[hedef] = np.minimum(komsuluk[hedef], net[kaynak])
    saglam = komsuluk > 0
    secilen = (
        int(np.argmax(np.where(saglam, komsuluk, -np.inf).ravel()))
        if saglam.any()
        else None
    )
    en_iyi = int(np.argmax(net.ravel()))
    return {
        "saglam": saglam,
        "secilen": secilen,
        "en_iyi": en_iyi,
        "para_cikmaz": bool(net.ravel()[en_iyi] <= 0),
    }


def ileri(islemler_hucre, sekil, bas, son) -> dict:
    """İleri yürüme (TASARIM 5.14, ikinci mod). Test yılları: ilk tam takvim yılı (`bas` 1 Ocak ise o yıl, değilse
    sonraki yıl) + 2 eğitim yılı ile `son` yılı arası. Her test yılı Y için seçim, `cikis_tarih` Y-01-01'den önce olan
    bütün işlemlerle yapılır; seçilen hücrenin giriş günü Y'de olan işlemleri alınır, önceki işlem kapanmadan giren
    işlem atılır. Sağlam bölge yoksa yıl nakittir. `islemler_hucre`: düz ızgara sırasında, giris_tarih, cikis_tarih
    ve getiri sütunlu tablolar."""
    bas, son = pd.Timestamp(bas), pd.Timestamp(son)
    ilk_tam = bas.year if (bas.month, bas.day) == (1, 1) else bas.year + 1
    tablolar = [t.sort_values("giris_tarih") for t in islemler_hucre]
    getiriler, yillar, son_cikis = [], [], None
    for yil in range(ilk_tam + EGITIM_YIL, son.year + 1):
        bas_yil, son_yil = pd.Timestamp(yil, 1, 1), pd.Timestamp(yil + 1, 1, 1)
        net = np.array(
            [
                np.prod(1 + t.loc[t["cikis_tarih"] < bas_yil, "getiri"].to_numpy(float))
                - 1
                for t in tablolar
            ]
        ).reshape(sekil)
        secilen = saglam_bolge(net)["secilen"]
        yillar.append({"yil": yil, "hucre": secilen})
        if secilen is None:
            continue
        t = tablolar[secilen]
        for i in t[
            (t["giris_tarih"] >= bas_yil) & (t["giris_tarih"] < son_yil)
        ].itertuples():
            if son_cikis is not None and i.giris_tarih < son_cikis:
                continue
            getiriler.append(i.getiri)
            son_cikis = i.cikis_tarih
    return {
        "net": float(np.prod(1 + np.array(getiriler)) - 1),
        "islem": len(getiriler),
        "yillar": yillar,
    }


def _hucreler(izgara) -> list:
    return [dict(zip(izgara, v)) for v in itertools.product(*izgara.values())]


def _sonraki(seriler) -> dict:
    """Sinyal günü ya da önceki son geçerli fiyat gününün kapanışından, sonraki k. geçerli fiyat gününün kapanışına getirinin
    medyanı, k = 1, 3, 5 (TASARIM 5.14 Ölçüler). `seriler`: işlem başına (geçerli fiyat günlerinin kapanış dizisi, taban
    günün bu dizideki konumu)."""
    sonuc = {}
    for k in (1, 3, 5):
        v = [c[s + k] / c[s] - 1 for c, s in seriler if s + k < len(c)]
        sonuc[f"ileri_{k}"] = float(np.median(v)) if v else None
    return sonuc


def _durum(b) -> tuple:
    if b["para_cikmaz"]:
        return "para_cikmaz", "Para çıkmaz: en iyi ayar bile kâr etmiyor."
    if b["secilen"] is None:
        return (
            "saglam_bolge_yok",
            "Sağlam bölge yok: kârlı ayarın yanında kâr etmeyen ayar var (tuzak).",
        )
    return (
        "saglam_bolge_var",
        f"Sağlam bölge var: {int(b['saglam'].sum())} ayar kârlı ve komşuları da kârlı.",
    )


def _sonuc(kimlik, izgara, tablolar, hucre_raporu, al_tut, bas, son) -> dict:
    """Bir hissenin ya da çiftin sonucu; `donem`: dönem başı ve dönemin son günü (TASARIM 5.14 Dönem).
    `hucre_raporu(i)`: hücre `i` için (özkaynak eğrisi, pozisyonda gün, tutma, ileri bakış)."""
    hucreler = _hucreler(izgara)
    sekil = tuple(len(v) for v in izgara.values())
    net = np.array([np.prod(1 + t["getiri"].to_numpy(float)) - 1 for t in tablolar])
    b = saglam_bolge(net.reshape(sekil))
    i = b["en_iyi"] if b["secilen"] is None else b["secilen"]
    egri, pozisyonda, tutma, bakis = hucre_raporu(i)
    olcu = olculer(tablolar[i]["getiri"], tutma, egri, pozisyonda)
    olcu.update(
        bakis,
        hucre=hucreler[i],
        secildi=b["secilen"] is not None,
        fark=olcu["net"] - al_tut,
    )
    durum, etiket = _durum(b)
    return {
        **kimlik,
        "donem": {"bas": str(bas.date()), "son": str(son.date())},
        "net": [round(float(x), 6) for x in net],
        "saglam": b["saglam"].ravel().tolist(),
        "secilen": b["secilen"],
        "en_iyi": b["en_iyi"],
        "durum": durum,
        "etiket": etiket,
        "olcu": olcu,
        "al_tut": al_tut,
        "altut_gecti": bool(olcu["net"] > al_tut),
        "bayraklar": olcu["bayraklar"],
        "ileri": ileri(tablolar, sekil, bas, son),
    }


def _fiyat_gecerli(x):
    """Fiyat sıfırdan büyük ve sonlu (TASARIM 5.14 Geçerli fiyat günü)."""
    return (x > 0) & np.isfinite(x)


def _gecerli(islem, karantina, aof, kapanis):
    """Geçerli fiyat günü (TASARIM 5.14 Geçerli fiyat günü): `islem` doğru, karantina yanlış, AOF ve kapanış sıfırdan büyük
    ve sonlu. Seri ya da dizi alır. Yalnız bu modülün fiyat okumaları içindir; sinyal ve ısınma sayımını değiştirmez."""
    return islem & ~karantina & _fiyat_gecerli(aof) & _fiyat_gecerli(kapanis)


def _ema_donem(m, p, bas):
    """(dönem başı, dönemin son günü) ya da None (TASARIM 5.14 Dönem). Başı: `bas` ile ısınmanın bittiği günün geç olanından
    başlayarak (o gün dahil) ilk geçerli fiyat günü. Isınma sayımı kapanışı olan günlerdir (5.1). Isınma dolmuyorsa ya da dönem
    başı bulunmuyorsa None. Son gün: `m`'nin son satırı; fiyatı geçerli olmak zorunda değildir."""
    f = m.dropna(subset=["kapanis"])
    if len(f) < p.isinma:
        return None
    bas = max(pd.Timestamp(bas), f.index[p.isinma - 1])
    uygun = m.index[
        (m.index >= bas) & _gecerli(m["islem"], m["karantina"], m["aof"], m["kapanis"])
    ]
    return (uygun[0], m.index[-1]) if len(uygun) else None


def _ema_egri(t, kap, bas):
    """Hücrenin işlemleri için günlük özkaynak (başlangıç 1), pozisyonda gün sayısı ve tutma günleri (TASARIM 5.14)."""
    gun = kap.index[kap.index >= bas]
    c = kap.loc[gun].to_numpy()
    carpan, pozisyonda, tutma = np.ones(len(gun)), np.zeros(len(gun), dtype=bool), []
    for r in t.itertuples():
        g, x = gun.get_loc(r.giris_tarih), gun.get_loc(r.cikis_tarih)
        if x == g:
            carpan[g] *= r.cikis_fiyat * (1 - MASRAF) / (r.giris_fiyat * (1 + MASRAF))
        else:
            carpan[g] *= c[g] / r.giris_fiyat / (1 + MASRAF)
            carpan[g + 1 : x] *= c[g + 1 : x] / c[g : x - 1]
            carpan[x] *= r.cikis_fiyat / c[x - 1] * (1 - MASRAF)
        pozisyonda[g:x] = True
        tutma.append(x - g)
    return np.cumprod(carpan), int(pozisyonda.sum()), tutma


def _getirili(t) -> pd.DataFrame:
    return t.assign(
        getiri=[
            islem_getirisi(g, c) for g, c in zip(t["giris_fiyat"], t["cikis_fiyat"])
        ]
    )


def ema_tablolari(m, p, izgara, bas) -> list:
    """Bir hissenin ızgara hücrelerinin işlem tabloları (düz ızgara sırasında, `getiri` sütunlu); dönem `_ema_donem`'dir."""
    bas, _ = _ema_donem(m, p, bas)
    f = m.dropna(subset=["kapanis"])
    zincir = motor.Zincir(m)
    tablolar = []
    for h in _hucreler(izgara):
        sig = aileler_.sinyal(f, replace(p, **h))
        t, _ = zincir.calistir(m.index.get_indexer(sig[sig >= bas]))
        tablolar.append(_getirili(t))
    return tablolar


def _ema_is(ad, m, p, izgara, bas) -> dict:
    tablolar = ema_tablolari(m, p, izgara, bas)
    bas, son = _ema_donem(m, p, bas)
    gecerli = _gecerli(m["islem"], m["karantina"], m["aof"], m["kapanis"])
    # değerleme: son geçerli kapanış ileri taşınır
    kap = m["kapanis"].where(gecerli).ffill()
    # k işlem günü: hissenin geçerli fiyat günleri
    f = m["kapanis"][gecerli]
    c = f.to_numpy()

    def hucre_raporu(i):
        egri, pozisyonda, tutma = _ema_egri(tablolar[i], kap, bas)
        # taban: sinyal günü ya da önceki geçerli gün
        sinyaller = [
            (c, f.index.searchsorted(s, side="right") - 1)
            for s in tablolar[i]["sinyal_tarih"]
        ]
        return egri, pozisyonda, tutma, _sonraki(sinyaller)

    return _sonuc(
        {"hisse": ad},
        izgara,
        tablolar,
        hucre_raporu,
        islem_getirisi(float(m.loc[bas, "aof"]), float(kap.iloc[-1])),
        bas,
        son,
    )


def _cift_simule(hedef, bas_k, d) -> tuple:
    """Bir hücrenin çift simülasyonu (TASARIM 5.14, 5.6 engelleri): (işlem tablosu, günlük özkaynak, tutuş günleri)."""
    n, gunler = len(d["G"]), d["gunler"]
    nakit, tutulan, islemler = 1.0, None, []
    egri = np.ones(n - bas_k)

    def kapat(q, fiyat, neden):
        nonlocal nakit, tutulan
        nakit = tutulan["birim"] * fiyat * (1 - MASRAF)
        islemler.append(
            {
                "sinyal_tarih": gunler[tutulan["sinyal"]],
                "giris_tarih": gunler[tutulan["giris"]],
                "giris_fiyat": tutulan["fiyat"],
                "cikis_tarih": gunler[q],
                "cikis_fiyat": fiyat,
                "neden": neden,
                "bacak": tutulan["bacak"],
                "sinyal_konum": tutulan["sinyal"],
                "tutma": q - tutulan["giris"],
            }
        )
        tutulan = None

    for q in range(bas_k + 1, n):
        if tutulan is not None and d["Kar"][q, tutulan["bacak"]]:
            kapat(q, d["SA"][q, tutulan["bacak"]], "karantina")
        h = hedef[q - 1]
        if h != 0:
            istenen = 0 if h > 0 else 1
            if (
                (tutulan is None or tutulan["bacak"] != istenen)
                and d["G"][q].all()
                and not (d["T"][q].any() or d["B"][q].any() or d["E"][q].any())
            ):
                if tutulan is not None:
                    kapat(q, d["A"][q, tutulan["bacak"]], "gecis")
                fiyat = d["A"][q, istenen]
                tutulan = {
                    "birim": nakit / (fiyat * (1 + MASRAF)),
                    "bacak": istenen,
                    "giris": q,
                    "sinyal": q - 1,
                    "fiyat": fiyat,
                }
                nakit = 0.0
        egri[q - bas_k] = (
            nakit
            if tutulan is None
            else tutulan["birim"] * d["Cf"][q, tutulan["bacak"]]
        )
    # veri sonu: son geçerli kapanıştan çıkış (son gün karantinalıysa karantina kuralı çıkarmıştır)
    if tutulan is not None:
        kapat(n - 1, d["Cf"][n - 1, tutulan["bacak"]], "veri_sonu")
        egri[-1] = nakit
    sutunlar = [
        "sinyal_tarih",
        "giris_tarih",
        "giris_fiyat",
        "cikis_tarih",
        "cikis_fiyat",
        "neden",
        "bacak",
        "sinyal_konum",
        "tutma",
    ]
    return _getirili(pd.DataFrame(islemler, columns=sutunlar)), egri


def cift_tablolari(y, x, gunler, C, A, F, bas_k, izgara) -> tuple:
    """Bir çiftin ızgara hücrelerinin (düz ızgara sırasında) işlem tabloları ve günlük özkaynakları; `cift_isleri` girdisiyle.
    `G`: bacak başına geçerli fiyat günü (TASARIM 5.14); `Cf`, `SA`: son geçerli kapanış ve son temiz AOF, ileri taşınır."""
    G = _gecerli(F["I"], F["Kar"], A, C)
    d = {
        "gunler": gunler,
        "C": C,
        "G": G,
        "Cf": pd.DataFrame(C).where(G).ffill().to_numpy(),
        "A": A,
        "T": F["T"],
        "B": F["B"],
        "Kar": F["Kar"],
        "E": pd.DataFrame(F["Kar"].astype(float))
        .rolling(motor.KARANTINA_GUN, min_periods=1)
        .max()
        .to_numpy()
        .astype(bool),
        "SA": pd.DataFrame(A).where(G).ffill().to_numpy(),
    }
    Kc = pd.DataFrame(C, index=gunler, columns=[y, x])
    tablolar, egriler = [], []
    for h in _hucreler(izgara):
        hedef = ciftbolme.hedef(Kc, y, x, ciftbolme.Parametre(**h))
        t, egri = _cift_simule(hedef, bas_k, d)
        tablolar.append(t)
        egriler.append(egri)
    return tablolar, egriler, d


def _cift_is(ad, y, x, sektor, gunler, C, A, F, bas_k, izgara) -> dict:
    tablolar, egriler, d = cift_tablolari(y, x, gunler, C, A, F, bas_k, izgara)
    n = len(gunler)

    def hucre_raporu(i):
        t = tablolar[i]
        sinyaller = []
        for r in t.itertuples():  # alınan bacağın geçerli fiyat günleri sayılır
            var = d["G"][:, r.bacak]
            sinyaller.append(
                (d["C"][var, r.bacak], int(var[: r.sinyal_konum + 1].sum()) - 1)
            )
        return (
            egriler[i],
            int(t["tutma"].sum()),
            t["tutma"].tolist(),
            _sonraki(sinyaller),
        )

    # Al-tut 50/50: dönem başı satırı iki bacak için de geçerli fiyat günüdür (`cift_isleri`); satış son geçerli kapanıştadır.
    al_tut = float(
        np.mean([islem_getirisi(A[bas_k, j], d["Cf"][n - 1, j]) for j in (0, 1)])
    )
    return _sonuc(
        {"hisse": ad, "sektor": sektor},
        izgara,
        tablolar,
        hucre_raporu,
        al_tut,
        gunler[bas_k],
        gunler[n - 1],
    )


def _is_calistir(girdi) -> tuple:
    aile, ad, *args = girdi
    return aile, ad, (_ema_is if aile == simulator.AILE else _cift_is)(ad, *args)


def _ema_isleri(anlik, semboller, p, izgara, bas) -> tuple:
    """(işler, atlanan adlar): ısınması dolmayan hisse sınanmaz (TASARIM 5.14 Dönem)."""
    isler, atlanan = [], []
    for s in semboller:
        m = motor.mumlar(anlik, s, p, motor.ATR_N)
        if _ema_donem(m, p, bas) is None:
            atlanan.append(s)
        else:
            isler.append((simulator.AILE, s, m, p, izgara, bas))
    return isler, atlanan


def cift_isleri(anlik, sektor, semboller, bas, izgara) -> tuple:
    """(işler, atlanan adlar): aynı sektördeki çiftler (TASARIM 5.14). Dönemin son günü: iki bacağın son satırlarının erken
    olanı. Dönem başı: `bas` ve 252. ortak kapanış gününden geç olanından başlayarak (o gün dahil) iki bacağın da geçerli
    fiyat günü olduğu ilk gün; son güne dek yoksa, ya da 252 ortak gün yoksa çift sınanmaz."""
    gunler = anlik.gunler
    f = anlik.fiyat[anlik.fiyat["sembol"].isin(semboller)]
    C = f.pivot(index="tarih", columns="sembol", values="kapanis").reindex(gunler)
    A = f.pivot(index="tarih", columns="sembol", values="aof").reindex(gunler)
    g = anlik.gun_tablosu
    g = g[g["sembol"].isin(semboller)]
    F = {
        ad: g.pivot(index="tarih", columns="sembol", values=sutun)
        .reindex(index=gunler, columns=C.columns)
        .fillna(False)
        .astype(bool)
        .to_numpy()
        for ad, sutun in (
            ("I", "islem"),
            ("T", "kilit_tavan"),
            ("B", "kilit_taban"),
            ("Kar", "karantina"),
        )
    }
    kol = {s: j for j, s in enumerate(C.columns)}
    var = C.notna().to_numpy()
    gecerli = _gecerli(F["I"], F["Kar"], A.to_numpy(), C.to_numpy())
    # bacağın `gun_tablosu`ndaki son satırı
    son_gun = g.groupby("sembol")["tarih"].max()
    bas_konum = int(gunler.searchsorted(pd.Timestamp(bas)))
    gruplar = {}
    for s in C.columns:
        if s in sektor:
            gruplar.setdefault(sektor[s], []).append(s)
    isler, atlanan = [], []
    for sek, liste in sorted(gruplar.items()):
        for y, x in itertools.combinations(liste, 2):
            j = [kol[y], kol[x]]
            ortak = np.flatnonzero(var[:, j[0]] & var[:, j[1]])
            if len(ortak) < CIFT_ISINMA:  # 252 işlem günü verisi yok (TASARIM 5.6)
                atlanan.append(f"{y}-{x}")
                continue
            # dönemin son günü: iki bacağın son satırlarının erken olanı
            son_k = int(
                min(gunler.searchsorted(son_gun[s], side="right") - 1 for s in (y, x))
            )
            ilk = max(bas_konum, int(ortak[CIFT_ISINMA - 1]))
            uygun = np.flatnonzero(gecerli[ilk : son_k + 1][:, j].all(axis=1))
            if not len(uygun):  # son güne dek geçerli dönem başı yok
                atlanan.append(f"{y}-{x}")
                continue
            bas_k = ilk + int(uygun[0])  # en çok son_k: tek günlük dönem sınanır
            kes = slice(0, son_k + 1)
            isler.append(
                (
                    ciftbolme.AILE,
                    f"{y}-{x}",
                    y,
                    x,
                    sek,
                    gunler[kes],
                    C.to_numpy()[kes][:, j],
                    A.to_numpy()[kes][:, j],
                    {k: v[kes][:, j] for k, v in F.items()},
                    bas_k,
                    izgara,
                )
            )
    return isler, sorted(atlanan)


def _ilerle(ilerleme, bitti, toplam, t0) -> None:
    gecen = time.monotonic() - t0
    kalan = gecen / bitti * (toplam - bitti)
    ilerleme(
        f"{bitti}/{toplam} iş · geçen {gecen:.0f} sn · kalan ~{kalan:.0f} sn · CPU %{psutil.cpu_percent():.0f}"
    )


def _kos(isler, isci, ilerleme, t0) -> dict:
    """İşleri `isci` süreçte koşar; ilerleme en çok saniyede bir ve sonda yazılır. Anahtar: (aile, ad)."""
    sonuc, son_yazim, toplam = {}, 0.0, len(isler)
    psutil.cpu_percent()  # ilk çağrı yalnız ölçümü başlatır

    def kaydet(aile, ad, s):
        nonlocal son_yazim
        sonuc[(aile, ad)] = s
        if len(sonuc) == toplam or time.monotonic() - son_yazim >= 1:
            son_yazim = time.monotonic()
            _ilerle(ilerleme, len(sonuc), toplam, t0)

    if isci == 1 or not isler:
        for girdi in isler:
            kaydet(*_is_calistir(girdi))
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=isci) as havuz:
            vadeler = [havuz.submit(_is_calistir, girdi) for girdi in isler]
            for v in concurrent.futures.as_completed(vadeler):
                kaydet(*v.result())
    return sonuc


def _ozet(hisseler) -> dict:
    secilen = [h for h in hisseler if h["secilen"] is not None]
    return {
        "toplam": len(hisseler),
        "saglam_bolge_var": sum(h["durum"] == "saglam_bolge_var" for h in hisseler),
        "saglam_bolge_yok": sum(h["durum"] == "saglam_bolge_yok" for h in hisseler),
        "para_cikmaz": sum(h["durum"] == "para_cikmaz" for h in hisseler),
        "altut_gecen": sum(h["altut_gecti"] for h in secilen),
    }


def _ek_kontrol(aile):
    """Ailenin son resmi `durum` satırı (TASARIM 5.14 "Bizim ek kontrolümüz"); yoksa None."""
    satirlar = kayit.resmi_durumlar(aile)
    if not satirlar:
        return None
    return {
        k: satirlar[-1].get(k)
        for k in ("aile", "genel", "durum", "holm_p", "olcutler", "kosu_id")
    }


def calistir(
    anlik,
    sektor,
    aileler=AILELER,
    isci=None,
    hisse=None,
    p=aileler_.Parametre(),
    bas=BASLANGIC,
    ilerleme=print,
    izgara=None,
) -> dict:
    """Bütün koşu (TASARIM 5.14). `hisse`: adına göre ilk N hisse (çiftte: iki bacağı da bunların içinde olan çiftler);
    `izgara`: aile → ızgara (varsayılan `IZGARA`); `isci`: yoksa makineye göre `isci_sayisi`."""
    t0 = time.monotonic()
    izgara = {**IZGARA, **(izgara or {})}
    semboller = sorted(anlik.fiyat["sembol"].unique())[:hisse]
    isler, atlanan = [], {}
    if simulator.AILE in aileler:
        yeni, atlanan[simulator.AILE] = _ema_isleri(
            anlik, semboller, p, izgara[simulator.AILE], bas
        )
        isler += yeni
    if ciftbolme.AILE in aileler:
        yeni, atlanan[ciftbolme.AILE] = cift_isleri(
            anlik, sektor, semboller, bas, izgara[ciftbolme.AILE]
        )
        isler += yeni
    mak = makine()
    isci = isci or isci_sayisi(
        mak["fiziksel_cekirdek"], mak["bellek_bos_gb"], len(isler)
    )
    sonuc = _kos(isler, isci, ilerleme, t0)
    ailelerin = {}
    for aile in aileler:
        hisseler = sorted(
            (s for (a, _), s in sonuc.items() if a == aile), key=lambda s: s["hisse"]
        )
        ailelerin[aile] = {
            "eksenler": izgara[aile],
            "hisseler": hisseler,
            "atlanan": atlanan[aile],
            "ozet": _ozet(hisseler),
        }
    return kayit._temiz(
        {
            "kosu_id": f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}",
            "anlik": anlik.kimlik,
            "makine": {
                **mak,
                "isci": isci,
                "sure_sn": round(time.monotonic() - t0, 2),
            },
            "masraf": MASRAF,
            "aileler": ailelerin,
            "ek_kontrol": {aile: _ek_kontrol(aile) for aile in aileler},
        }
    )


def yaz(sonuc, kok=None) -> Path:
    """`rapor/tansu-sinama-<koşu>.json` dosyasını ve deneme günlüğüne `tur=destek`, `olay=tansu_sinama` satırını yazar
    (TASARIM 5.14 "Kayıt ve çıktı"). Holm ve m bunu saymaz (5.11). Manifest sha256'sı `sonuc["manifest_sha256"]`'dadır."""
    dizin = Path(kok or rapor.RAPOR_DIZINI)
    dizin.mkdir(parents=True, exist_ok=True)
    yol = dizin / f"tansu-sinama-{sonuc['kosu_id']}.json"
    yol.write_text(
        json.dumps(sonuc, ensure_ascii=False, allow_nan=False), encoding="utf-8"
    )
    commit, kirli = kayit._git()
    kayit._yaz(
        {
            "tur": "destek",
            "olay": "tansu_sinama",
            "tarih": kayit._simdi(),
            "kosu_id": sonuc["kosu_id"],
            "anlik": sonuc["anlik"],
            "manifest_sha256": sonuc.get("manifest_sha256"),
            "git_commit": commit,
            "kirli": kirli,
            "resmi": False,
            "makine": sonuc["makine"],
            "ozet": {aile: f["ozet"] for aile, f in sonuc["aileler"].items()},
        }
    )
    return yol


def sektor_oku(kok) -> tuple:
    """(sektör sözlüğü, anlık görüntü kimliği): `<kok>/ag` altındaki `sektor.json` taşıyan en yeni anlık görüntü (TASARIM 5.14)."""
    for klasor in sorted((Path(kok) / "ag").glob("2*"), reverse=True):
        yol = klasor / "sektor.json"
        if yol.exists():
            sozluk = json.loads(yol.read_text(encoding="utf-8"))
            return dict(sorted(sozluk.items())), klasor.name
    raise veri.VeriHatasi(
        f"sektör tablosu yok: {kok}/ag altında sektor.json bulunamadı"
    )
