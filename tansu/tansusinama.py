"""Tansu sınaması (TASARIM 5.14): Tansu'nun kendi sınama yöntemi.

Her hisse (çift ailesinde her çift) kendi ızgarasıyla, bütün dönemde, masraf %0,10 ile koşulur. Sağlam bölge seçilir,
sonuç al-tut ve Tansu'nun tablo ölçüleriyle yan yana verilir. Kabul kararına girmez (5.12), kart üretmez, m'yi artırmaz
(5.11). Hash dışıdır (`kayit.HASH_DISI`). İş birimi bir hisse ya da bir çifttir; sonuç işçi sayısından bağımsızdır.
"""

import concurrent.futures
from collections import Counter
import datetime as dt
from importlib import metadata
import itertools
import json
import logging
import multiprocessing
import os
import platform
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import replace
from dataclasses import asdict
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
from pathlib import Path

import numpy as np
import pandas as pd
import psutil

from tansu import aileler as aileler_
from tansu import (
    ciftbolme,
    deneme as deneme_,
    islem_riski,
    istatistik,
    katalog,
    kayit,
    motor,
    rapor,
    saglamlik,
    simulator,
    veri,
)

MASRAF = 0.001  # TASARIM 5.14: her yönde %0,10, kayma yok
SUPHELI_KAZANMA = istatistik.SUPHELI_KAZANMA  # TASARIM 5.14: eski dış yüz korunur.
AZ_ISLEM = istatistik.AZ_ISLEM
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
    return float(islem_riski.fiyat_getirisi(giris, cikis, m))


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
    return istatistik.olc(
        dict(getiriler=getiriler, tutma=tutma, egri=egri, pozisyonda=pozisyonda),
        politika="eksen_maksimin_legacy_v1",
    )["legacy"]


def saglam_bolge(net) -> dict:
    """Sağlam bölge (TASARIM 5.14): hücre ve bütün komşuları (tek eksende bir adım) net > 0.

    `saglam`: ızgara biçiminde bool; `secilen`: sağlam hücreler içinde komşuluğunun (kendisi dahil) en küçük neti en büyük
    olan, eşitlikte düz sıradaki (C sırası) ilk, yoksa None; `en_iyi`: en büyük net, eşitlikte ilk; `para_cikmaz`: en iyi ≤ 0."""
    sonuc = saglamlik.sec(None, net, politika="eksen_maksimin_legacy_v1")
    return {k: v for k, v in sonuc.items() if k != "politika"}


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
    return [
        dict(zip(izgara, v, strict=True)) for v in itertools.product(*izgara.values())
    ]


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
    # TASARIM 5.15 S08: yeni politika açıkça istenir; eski hücreler yeniden etiketlenmez.
    if "risk_surumu" in t:
        return simulator.risk_tablosu(t)
    return t.assign(
        getiri=[
            islem_getirisi(g, c)
            for g, c in zip(t["giris_fiyat"], t["cikis_fiyat"], strict=True)
        ]
    )


def ema_tablolari(
    m, p, izgara, bas, *, aktarimlar=None, sembol=None, baglar=None
) -> list:
    """Bir hissenin ızgara hücrelerinin işlem tabloları (düz ızgara sırasında, `getiri` sütunlu); dönem `_ema_donem`'dir.
    Düzeltilmiş AOF'u ya da kapanışı sonsuz gün motora karantina günü olarak verilir (TASARIM 5.14 uç durum 2); `m` değişmez."""
    bas, _ = _ema_donem(m, p, bas)
    f = m.dropna(subset=["kapanis"])
    mumlar = m.assign(
        karantina=m["karantina"] | np.isinf(m["aof"]) | np.isinf(m["kapanis"])
    )
    tablolar = []
    for i, h in enumerate(_hucreler(izgara)):
        # TASARIM 5.14: hücre ayarı, kurulum ve işlem önbelleği birlikte kalır.
        pc = replace(p, **h)
        aktarim = aktarimlar[i] if aktarimlar is not None else None
        if aktarim is not None:
            aktarim.ayar_dogrula(pc)
            pc = aktarim.p
        kurulum = aileler_.kurulum(f, pc)
        if aktarim is not None and kurulum is None:
            aktarim.sinyaller(mumlar, kurulum, sembol)
        if aktarim is None:
            sig = kurulum.index
            t, _ = saglamlik.ema_hucre_calistir(
                mumlar,
                pc,
                kurulum=kurulum,
                sinyal_konumlari=m.index.get_indexer(sig[sig >= bas]),
            )
        else:
            t, _, referanslar = aktarim.ema(
                mumlar, kurulum.loc[kurulum.index >= bas], sembol
            )
            if baglar is not None:
                baglar.append((aktarim, referanslar))
        tablolar.append(_getirili(t))
    return tablolar


def _ema_is(ad, m, p, izgara, bas, aktarimlar=None) -> dict:
    baglar = []
    tablolar = ema_tablolari(
        m, p, izgara, bas, aktarimlar=aktarimlar, sembol=ad, baglar=baglar
    )
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

    sonuc = _sonuc(
        {"hisse": ad},
        izgara,
        tablolar,
        hucre_raporu,
        islem_getirisi(float(m.loc[bas, "aof"]), float(kap.iloc[-1])),
        bas,
        son,
    )
    for i, (aktarim, referanslar) in enumerate(baglar):
        aktarim.sonuc({"hisse": ad, "hucre": i, "net": sonuc["net"][i]}, referanslar)
    return sonuc


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
    `G`: bacak başına geçerli fiyat günü (TASARIM 5.14); `Cf`, `SA`: son geçerli kapanış ve son temiz AOF, ileri taşınır.
    Düzeltilmiş AOF'u ya da kapanışı sonsuz bacak günü karantina günüdür (uç durum 2): `Kar`, `SA` ve `E` onu görür."""
    d = veri.cift_girdileri(gunler, C, A, F, "legacy_tansu_v1")
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


def _ema_isleri(anlik, semboller, p, izgara, bas, aktarimlar=None) -> tuple:
    """(işler, atlanan adlar): ısınması dolmayan hisse sınanmaz (TASARIM 5.14 Dönem)."""
    isler, atlanan = [], []
    for s in semboller:
        m = motor.mumlar(anlik, s, p, motor.ATR_N)
        if _ema_donem(m, p, bas) is None:
            atlanan.append(s)
        else:
            isler.append((simulator.AILE, s, m, p, izgara, bas, aktarimlar))
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
    F = veri.cift_bayraklari(g, gunler, C.columns)
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
        # TASARIM 5.14 Makine ve paralellik: işçiler her platformda `spawn` ile başlar
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=isci, mp_context=multiprocessing.get_context("spawn")
        ) as havuz:
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
    aktarim=None,
) -> dict:
    """Bütün koşu (TASARIM 5.14). `hisse`: adına göre ilk N hisse (çiftte: iki bacağı da bunların içinde olan çiftler);
    `izgara`: aile → ızgara (varsayılan `IZGARA`); `isci`: yoksa makineye göre `isci_sayisi`."""
    t0 = time.monotonic()
    izgara = {**IZGARA, **(izgara or {})}
    if aktarim is not None:
        aktarim.aile_dogrula(aileler)
        aktarim.veri_bagla(anlik.kimlik)
        p = aktarim.p
    semboller = sorted(anlik.fiyat["sembol"].unique())[:hisse]
    isler, atlanan = [], {}
    if simulator.AILE in aileler:
        yeni, atlanan[simulator.AILE] = _ema_isleri(
            anlik,
            semboller,
            p,
            izgara[simulator.AILE],
            bas,
            [aktarim.cocuk(h) for h in _hucreler(izgara[simulator.AILE])]
            if aktarim is not None
            else None,
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
            "kosu_id": aktarim.kosu_id
            if aktarim is not None
            else f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}",
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
    commit, kirli = kayit._git()
    dizin = Path(kok or rapor.RAPOR_DIZINI)
    dizin.mkdir(parents=True, exist_ok=True)
    yol = dizin / f"tansu-sinama-{sonuc['kosu_id']}.json"
    yol.write_text(
        json.dumps(sonuc, ensure_ascii=False, allow_nan=False), encoding="utf-8"
    )
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


def grup_kod_ozeti():
    """TASARIM 5.15 Küçük grup hazırlığı: geçici tam paket içerik bağı."""
    dosyalar = {
        yol.name: sha256(yol.read_bytes()).hexdigest()
        for yol in sorted(kayit.PAKET.glob("*.py"))
    }
    return sha256(deneme_.kanonik(dosyalar)).hexdigest()


def _grup_dosyasini_dogrula(ref, alan, engeller):
    if ref is None:
        engeller.append(dict(alan=alan, neden="Dosya başvurusu eksik."))
        return None
    yol = Path(ref["yol"])
    try:
        if sha256(yol.read_bytes()).hexdigest() != ref["sha256"]:
            raise ValueError("Dosya özeti değişmiş.")
        return yol
    except (OSError, ValueError) as hata:
        engeller.append(dict(alan=alan, neden=str(hata)))
        return None


def _grup_stratejilerini_dogrula(depo, stratejiler, engeller):
    if not stratejiler:
        engeller.append(
            dict(alan="strateji_revizyonlari", neden="Strateji seçimi eksik.")
        )
    for s in stratejiler:
        alan = f"strateji_revizyonlari.{s['revizyon_ref']}"
        _grup_dosyasini_dogrula(s.get("kaynak"), f"{alan}.kaynak", engeller)
        if s.get("yayim_tarihi") is None:
            engeller.append(
                dict(alan=f"{alan}.yayim_tarihi", neden="Kaynak tarihi eksik.")
            )
        for eksik in s.get("eksik_alanlar", []):
            engeller.append(
                dict(alan=f"{alan}.{eksik}", neden="Kaynak tanımı çözülmemiş.")
            )
        if not s.get("deneme_id"):
            engeller.append(
                dict(
                    alan=f"{alan}.deneme_id",
                    neden="Tam çözülmüş kaynak strateji revizyonu yok.",
                )
            )
            continue
        try:
            d = depo.deneme_oku(s["deneme_id"])
            if d["strateji"]["izin_durumu"] == "izinsiz":
                raise ValueError("Kayıtlı legacy tanım kaynak seçim izni taşımaz.")
        except (deneme_.PilotHatasi, ValueError) as hata:
            engeller.append(dict(alan=f"{alan}.deneme_id", neden=str(hata)))


def _grup_takvimini_dogrula(tanim, engeller):
    ref = tanim.get("referanslar", {})
    yol = _grup_dosyasini_dogrula(ref.get("takvim"), "referanslar.takvim", engeller)
    if yol is None:
        return []
    try:
        takvim = json.loads(yol.read_text(encoding="utf-8"))
        for ad in ("baslangic", "bitis"):
            deneme_._grup_tarihi(takvim[ad])
            takvim[ad] = dt.date.fromisoformat(takvim[ad])
        deneme_._metin(takvim.get("kaynak_ref"))
        gunler = list(_takvim_seanslari(takvim))
        secim = tanim.get("seanslar", [])
        if secim and [t for t in gunler if secim[0] <= t <= secim[-1]] != secim:
            raise ValueError(
                "Kesin seans seçimi takvimle uyuşmuyor; dönem daraltılmaz."
            )
        isinma = tanim.get("isinma_baslangici")
        if isinma and secim and takvim["baslangic"] > dt.date.fromisoformat(isinma):
            raise ValueError("Takvim ısınma kapsamını taşımıyor.")
        return gunler
    except (OSError, ValueError, KeyError, TypeError) as hata:
        engeller.append(dict(alan="referanslar.takvim", neden=str(hata)))
        return []


def _grup_anlik_goruntusu(ref, veri_koku, engeller):
    kimlik = ref.get("anlik_goruntu")
    if not kimlik:
        engeller.append(
            dict(alan="referanslar.anlik_goruntu", neden="Anlık görüntü eksik.")
        )
        return None
    if Path(kimlik).name != kimlik or kimlik in (".", ".."):
        raise deneme_.PilotHatasi("Tek yerel görüntü kimliği gerekli.")
    try:
        anlik = veri.oku(kimlik, veri_koku)
        manifest = Path(veri_koku) / "ag" / kimlik / "manifest.json"
        if sha256(manifest.read_bytes()).hexdigest() != ref.get("manifest_ozeti"):
            raise ValueError("Manifest özeti eksik veya değişmiş.")
        return anlik
    except (OSError, veri.VeriHatasi, ValueError, KeyError) as hata:
        engeller.append(dict(alan="referanslar.anlik_goruntu", neden=str(hata)))
        return None


def _grup_uyeligi(tanim, engeller, politika=None):
    kural = tanim.get("hisse_kurali", {})
    semboller = kural.get("semboller", [])
    if not semboller:
        engeller.append(
            dict(alan="hisse_kurali.semboller", neden="Açık hisse seçimi eksik.")
        )
    try:
        uyelik = veri.uyelik_hazirla(
            veri.UyelikIstegi(
                tuple(tanim.get("seanslar", [])),
                kural.get("evren_politikasi"),
                kural.get("uyelik_surumu"),
            )
        )
        if uyelik["tablo_parmak_izi"] != tanim.get("referanslar", {}).get(
            "uyelik_ozeti"
        ):
            raise ValueError("Üyelik özeti eksik veya değişmiş.")
        if politika is not None:
            uyelik = veri.pay_uyeligi(uyelik, politika)
            semboller = veri.pay_sembolleri(semboller, politika)
        return [
            dict(sembol=s, tarih=t, neden="bist30_uyesi_degil")
            for t, gun in uyelik["gunler"].items()
            for s in semboller
            if s not in gun["semboller"]
        ]
    except (OSError, veri.VeriHatasi, ValueError) as hata:
        engeller.append(dict(alan="hisse_kurali.uyelik", neden=str(hata)))
        return []


def _grup_veri_kapsami(tanim, anlik, takvim, engeller, politika=None):
    seanslar = tanim.get("seanslar", [])
    isinma = tanim.get("isinma_baslangici")
    if anlik is None or not seanslar or not isinma or not takvim:
        engeller.append(
            dict(
                alan="veri_kapsami", neden="Kesin veri ve ısınma kapsamı doğrulanamadı."
            )
        )
        return
    gerekli = {t for t in takvim if isinma <= t <= seanslar[-1]}
    semboller = tanim.get("hisse_kurali", {}).get("semboller", [])
    if politika is not None:
        semboller = veri.pay_sembolleri(semboller, politika)
    for sembol in semboller:
        mevcut = {
            t.date().isoformat()
            for t in anlik.fiyat.loc[anlik.fiyat["sembol"] == sembol, "tarih"]
        }
        eksik = sorted(gerekli - mevcut)
        if eksik:
            engeller.append(
                dict(
                    alan=f"veri_kapsami.{sembol}",
                    neden=f"Gerekli seans verisi eksik: {', '.join(eksik)}",
                )
            )


def _grup_pay_kimligi(ref, anlik, engeller):
    """TASARIM 5.15 #167: statik eşleme kalite veya gösterge hesabı çağırmaz."""
    secim = ref.get("pay_kimligi")
    if secim is None:
        return anlik, None
    try:
        politika = veri.pay_kimligi_hazirla(
            secim,
            kaynak=secim["kaynak"],
            goruntu_id=ref["anlik_goruntu"],
            manifest_ozeti=ref["manifest_ozeti"],
        )
        if anlik is not None:
            anlik = veri.pay_kimligi_uygula(anlik, politika)
        return anlik, politika
    except (OSError, veri.VeriHatasi, ValueError) as hata:
        engeller.append(dict(alan="referanslar.pay_kimligi", neden=str(hata)))
        return None, None


def grup_hazirla(depo, tanim, *, veri_koku):
    """TASARIM 5.15 Küçük grup hazırlığı: statik kontrol ve E5 olayı."""
    tanim = deepcopy(tanim)
    deneme_._grup_tanimi_dogrula(tanim)
    engeller = []
    for ad in ("soru", "isinma_baslangici", "durdurma_kurali"):
        if not tanim.get(ad):
            engeller.append(dict(alan=ad, neden="Zorunlu hazırlık alanı eksik."))
    if tanim.get("gozlem_durumu") not in ("kesif", "gorulmedi"):
        engeller.append(
            dict(alan="gozlem_durumu", neden="Keşif veya görülmedi seçimi gerekli.")
        )
    seanslar = tanim.get("seanslar", [])
    if not seanslar:
        engeller.append(dict(alan="seanslar", neden="Kesin seans seçimi eksik."))
    elif seanslar[-1] >= dt.datetime.now(veri.ISTANBUL).date().isoformat():
        engeller.append(
            dict(alan="seanslar", neden="Tamamlanmamış seans kabul edilmez.")
        )
    if (
        seanslar
        and tanim.get("isinma_baslangici")
        and tanim["isinma_baslangici"] >= seanslar[0]
    ):
        engeller.append(
            dict(
                alan="isinma_baslangici",
                neden="Isınma ilk seansın öncesinde olmalıdır.",
            )
        )
    _grup_stratejilerini_dogrula(depo, tanim.get("strateji_revizyonlari", []), engeller)
    ref = tanim.get("referanslar", {})
    for ad in ("yontem", "risk", "masraf"):
        _grup_dosyasini_dogrula(ref.get(ad), f"referanslar.{ad}", engeller)
    if ref.get("kod_ozeti") != grup_kod_ozeti():
        engeller.append(
            dict(alan="referanslar.kod_ozeti", neden="Kod özeti eksik veya değişmiş.")
        )
    takvim = _grup_takvimini_dogrula(tanim, engeller)
    anlik = _grup_anlik_goruntusu(ref, veri_koku, engeller)
    anlik, politika = _grup_pay_kimligi(ref, anlik, engeller)
    dislamalar = _grup_uyeligi(tanim, engeller, politika)
    _grup_veri_kapsami(tanim, anlik, takvim, engeller, politika)
    makbuz = depo.grup_hazirligi_kaydet(
        tanim=tanim, engeller=engeller, dislamalar=dislamalar
    )
    return depo.grup_hazirligi_oku(makbuz.olay_id, tanim=tanim)


# TASARIM 5.15 S10: bu kimlik eski HASH_DISI sınıflamasını değiştirmez.
KAYITLI_SURUM = "kayitli_donem_v1"
ARAMA_SURUM = "kayitli_izgara_v1"
KAYITLI_YONTEM = dict(
    yontem=KAYITLI_SURUM,
    tekrar=0,
    yurutme_surumu="bagimsiz_islem_v1",
    fiyat_politikasi="aof_v1",
    muhasebe_politikasi="tani_referans_v1",
)
DONEM_BIRIMLERI = {
    "net_sonuc": "TL",
    "kalan_adet": "adet",
    "degerleme": "TL/adet",
    "nominal_tutar": "TL",
    "net_r": "R",
    "referans_sonucu": "oran",
}


def _kayitli_istek(deneme):
    """TASARIM 5.15 S10: kayıtlı ayar dışında hesap varsayımı üretme."""
    _yurutme_ayarlari(deneme)
    _kayitli_veri_ayarlari(deneme["veri_ayarlari"])
    _isinma_secimi_dogrula(deneme["veri_ayarlari"], deneme["yontem_ayarlari"])
    _kayitli_donemler(deneme["donemler"])
    _kayitli_takvim(deneme["veri_ayarlari"].get("takvim", {}))


def _kayitli_hucre_yontemi(yontem):
    """TASARIM 5.15 #176: isteğe bağlı kilit seçimi eski sözlüğe eklenmez."""
    beklenen = KAYITLI_YONTEM
    if isinstance(yontem, dict) and "isinma_politikasi" in yontem:
        beklenen = beklenen | dict(isinma_politikasi="kaynakli_isinma_v1")
    if isinstance(yontem, dict) and "kilit_politikasi" in yontem:
        beklenen = beklenen | dict(kilit_politikasi="ham_aralik_v1")
    if not isinstance(yontem, dict) or deneme_.kanonik(yontem) != deneme_.kanonik(
        beklenen
    ):
        raise deneme_.PilotHatasi("Desteklenmeyen yürütme ayarı.")
    return beklenen


def _yurutme_ayarlari(deneme):
    _kayitli_hucre_yontemi(deneme["yontem_ayarlari"])
    if deneme["masraf_ayarlari"] != {"masraf_surumu": islem_riski.MASRAF_SURUMU}:
        raise deneme_.PilotHatasi("Desteklenmeyen masraf ayarı.")
    if deneme["strateji"]["aile"] != katalog.AILE:
        raise deneme_.PilotHatasi("Desteklenmeyen aile; çift için risk_dayanagi_eksik.")
    _kayitli_risk(deneme["risk_ayarlari"])


def _isinma_secimi_dogrula(v, y):
    """TASARIM 5.15 #178: eşleşmiş opt-in, hesap veya canlı kaynak gerektirmez."""
    hucre = y.get("hucre_yontemi", y)
    if (
        "ilk_islem" not in v
        and "isinma_politikasi" not in y
        and (not isinstance(hucre, dict) or "isinma_politikasi" not in hucre)
    ):
        return False
    secim = v.get("ilk_islem")
    if (
        not isinstance(hucre, dict)
        or ("hucre_yontemi" in y and "isinma_politikasi" in y)
        or hucre.get("isinma_politikasi") != "kaynakli_isinma_v1"
        or secim is None
    ):
        raise deneme_.PilotHatasi(
            "İlk işlem kaynağı ve ısınma politikası birlikte seçilmelidir."
        )
    try:
        veri.ilk_islem_secimi_dogrula(secim)
    except veri.VeriHatasi as hata:
        raise deneme_.PilotHatasi(str(hata)) from hata
    if any(
        secim[a] != deger
        for a, deger in dict(
            kaynak=v["kaynak"],
            goruntu_id=v["veri_referanslari"][0],
            manifest_ozeti=v["manifest_ozeti"],
        ).items()
    ):
        raise deneme_.PilotHatasi("İlk işlem seçimi kayıtlı veri bağıyla uyuşmuyor.")
    return True


def _ilk_islem_kayitlari(v, *, uyelik_kaniti=None):
    politika = None
    if v.get("pay_kimligi") is not None:
        politika = veri.pay_kimligi_hazirla(
            v["pay_kimligi"],
            kaynak=v["kaynak"],
            goruntu_id=v["veri_referanslari"][0],
            manifest_ozeti=v["manifest_ozeti"],
            **(
                {}
                if uyelik_kaniti is None
                else dict(tablo_metni=uyelik_kaniti["pay_kimligi_tablo_metni"])
            ),
        )
    return veri.ilk_islem_hazirla(
        v["ilk_islem"],
        kaynak=v["kaynak"],
        goruntu_id=v["veri_referanslari"][0],
        manifest_ozeti=v["manifest_ozeti"],
        pay_kimligi=politika,
        **(
            {}
            if uyelik_kaniti is None
            else dict(tablo_metni=uyelik_kaniti["ilk_islem_tablo_metni"])
        ),
    )


def _dogal_bekleyis(v, ref, sembol, ilk, son, gerekli, kayitlar):
    """TASARIM 5.15 #178: E2 sayacını değiştirmeden kaynak/takvim bağı türet."""
    kaynak = kayitlar.get(sembol)
    if kaynak is None:
        return None
    gunler = v["takvim"]["seanslar"]
    kanit = veri.ilk_islem_gecmis_kaniti(kaynak, gunler, son)
    if (
        ref.get("ilk_islem") != v["ilk_islem"]
        or ref.get("gecmis_kaniti", {}).get(sembol) != kanit
    ):
        raise ValueError("E1 ilk işlem geçmiş kanıtı kayıtlı takvimle uyuşmuyor.")
    if kaynak["yayim_tarihi"] > ilk:
        raise ValueError("İlk işlem kaynağı değerlendirme gününden sonra yayımlanmış.")
    gozlemler = [t for t in gunler if kaynak["ilk_islem_gunu"] <= t <= son]
    ilk_sayi = sum(t <= ilk for t in gozlemler)
    tamam = gozlemler[gerekli - 1] if len(gozlemler) >= gerekli else None
    neden = dict(
        neden="dogal_isinma",
        ilk_gun=ilk,
        ilk_islem_gunu=kaynak["ilk_islem_gunu"],
        kaynak_id=kaynak["kaynak_id"],
        isinma_tamamlanma_gunu=tamam,
        e1_ref=ref["kayit_id"],
    )
    return ilk_sayi, neden if ilk_sayi < gerekli else None


def _isinma_kaydet(deneme, sonuc, paket, sembol, hesap, ilk, gerekli):
    sayi = int(hesap["isinma"].at[pd.Timestamp(ilk)])
    kayit = dict(gozlem=sayi, gerekli=gerekli, tamam=sayi >= gerekli)
    sonuc["isinma"][sembol] = kayit
    if deneme["veri_ayarlari"].get("ilk_islem") is not None:
        bag = _dogal_bekleyis(
            deneme["veri_ayarlari"],
            paket["referans"],
            sembol,
            ilk,
            sonuc["donem"]["bitis"].isoformat(),
            gerekli,
            paket["ilk_islem_kayitlari"],
        )
        if bag is not None:
            if bag[0] != sayi:
                raise ValueError(
                    "E2 ısınma sayacı ilk işlem geçmiş kanıtıyla uyuşmuyor."
                )
            if bag[1] is not None:
                kayit["dogal_bekleyis"] = bag[1]
    if sayi < gerekli and "dogal_bekleyis" not in kayit:
        _kayitli_hata(
            sonuc,
            "isinma",
            f"{sembol}: {sayi}/{gerekli} gözlem",
            sembol=sembol,
            tarih=ilk,
        )
    return sayi


def _isinma_referansi_dogrula(v, ref, donem, gereken, kayitlar):
    """TASARIM 5.15 #178: E1 bağı ve kesim aynı saf sahipten doğrulanır."""
    if (
        ref.get("ilk_islem") != v["ilk_islem"]
        or ref.get("manifest_parmak_izi") != v["manifest_ozeti"]
        or ref.get("goruntu_id") != v["veri_referanslari"][0]
        or ref.get("pay_kimligi") != v.get("pay_kimligi")
    ):
        raise ValueError("İlk işlem sonucu E1 kaynak bağı uyuşmuyor.")
    ilk, son = donem["baslangic"].isoformat(), donem["bitis"].isoformat()
    if ref.get("istenen_donem") != veri._donem(ilk, son) or ref.get(
        "isinma_donemi"
    ) != veri._donem(
        donem["isinma_baslangici"],
        donem["baslangic"] - dt.timedelta(days=1),
    ):
        raise ValueError(
            "E1 ilk işlem dönem/ısınma kesimi kayıtlı sınırlarla uyuşmuyor."
        )
    beklenen = {
        pay: veri.ilk_islem_gecmis_kaniti(kayitlar[pay], v["takvim"]["seanslar"], son)
        for pay in gereken & kayitlar.keys()
    }
    if ref.get("gecmis_kaniti") != beklenen:
        raise ValueError("E1 ilk işlem geçmiş kanıtı kayıtlı kesimle uyuşmuyor.")
    return ilk, son


def _isinma_sonucu_dogrula(d, r, kanit, gereken):
    """TASARIM 5.15 #178: E5 saklı girdilerden sonuç bağını doğrular, hesap yapmaz."""
    v = d["veri_ayarlari"]
    kayitlar = _ilk_islem_kayitlari(v, uyelik_kaniti=kanit)
    isinma = r.get("isinma", {})
    ref = r.get("veri_referansi")
    if ref is None:
        if r["durum"] != "hata" or not r.get("hatalar") or isinma:
            raise ValueError(
                "İlk işlem sonucu E1 geçmiş kanıtı olmadan başarılı olamaz."
            )
        return
    ilk, son = _isinma_referansi_dogrula(v, ref, r["donem"], gereken, kayitlar)
    if (
        not isinstance(isinma, dict)
        or set(isinma) - gereken
        or (r["durum"] == "tamamlandi" and set(isinma) != gereken)
    ):
        raise ValueError("İlk işlem sonucu gerekli tarihli üyeleri içermiyor.")
    gerekli = next(
        a["deger"] for a in d["strateji"]["parametreler"] if a["ad"] == "isinma"
    )
    uyelik = _kayitli_uyelik(
        v, [t for t in v["takvim"]["seanslar"] if ilk <= t <= son], uyelik_kaniti=kanit
    )
    for pay, x in isinma.items():
        if (
            not isinstance(x, dict)
            or set(x) - {"gozlem", "gerekli", "tamam", "dogal_bekleyis"}
            or type(x.get("gozlem")) is not int
            or x["gozlem"] < 0
            or type(x.get("gerekli")) is not int
            or x["gerekli"] != gerekli
            or type(x.get("tamam")) is not bool
            or x["tamam"] != (x["gozlem"] >= gerekli)
        ):
            raise ValueError("İlk işlem ısınma sayısı veya türü geçersiz.")
        ilk_gun = next(
            (t for t, g in uyelik["gunler"].items() if pay in g["semboller"]),
            next(t for t in v["takvim"]["seanslar"] if ilk <= t <= son),
        )
        bag = _dogal_bekleyis(v, ref, pay, ilk_gun, son, gerekli, kayitlar)
        dogal = bag[1] if bag else None
        if (
            (bag and bag[0] != x["gozlem"])
            or x.get("dogal_bekleyis") != dogal
            or ("dogal_bekleyis" in x and dogal is None)
        ):
            raise ValueError(
                "Doğal ısınma nedeni, sayısı veya tamamlanma günü uyuşmuyor."
            )
        if (
            not x["tamam"]
            and dogal is None
            and (
                r["durum"] != "hata"
                or not any(h.get("asama") == "isinma" for h in r.get("hatalar", []))
            )
        ):
            raise ValueError("Kaynağı bilinmeyen ısınma eksikliği başarı olamaz.")
        tamam = dogal["isinma_tamamlanma_gunu"] if dogal else None
        if dogal and any(
            pay in a["semboller"] and (tamam is None or a["tarih"] < tamam)
            for a in r.get("adaylar", [])
        ):
            raise ValueError("Doğal ısınma dolmadan sinyal üretilmiş.")


def _kayitli_risk(risk):
    if set(risk) != {"risk_surumu", "nominal_tutar"}:
        raise deneme_.PilotHatasi("Risk sürümü ve açık nominal_tutar gerekli.")
    nominal = risk["nominal_tutar"]
    if risk["risk_surumu"] != islem_riski.RISK_SURUMU:
        raise deneme_.PilotHatasi("Desteklenmeyen risk sürümü.")
    if type(nominal) is not Decimal or not nominal.is_finite() or nominal <= 0:
        raise deneme_.PilotHatasi("Nominal tutar sonlu ve pozitif ondalık olmalıdır.")
    sayisal = float(nominal)
    if not 0 < sayisal < float("inf"):
        raise deneme_.PilotHatasi("Nominal tutar hesap aralığı dışında.")
    if Decimal(str(sayisal)) != nominal:
        raise deneme_.PilotHatasi(
            "Nominal tutar mevcut sayı yüzüne kayıpsız aktarılamıyor."
        )


def _kayitli_veri_ayarlari(v):
    for alan, deger in dict(
        uyelik_surumu="bist30_2021_2025_v1",
        evren_politikasi="donemsel_bist30_v1",
        kalite_surumu="legacy_tansu_v1",
        duzeltme_surumu="is_yatirim",
        takvim_ref="xu100",
    ).items():
        if v.get(alan) != deger:
            raise deneme_.PilotHatasi(f"Desteklenmeyen veri politikası: {alan}")
    for alan in ("kaynak", "manifest_ozeti", "uyelik_ozeti"):
        if not isinstance(v.get(alan), str) or not v[alan].strip():
            raise deneme_.PilotHatasi(f"Eksik veri ayarı: {alan}")
    if v.get("pay_kimligi") is not None:
        veri.pay_kimligi_secimi_dogrula(v["pay_kimligi"])
        if any(
            v["pay_kimligi"][a] != deger
            for a, deger in dict(
                kaynak=v["kaynak"],
                goruntu_id=v["veri_referanslari"][0],
                manifest_ozeti=v["manifest_ozeti"],
            ).items()
        ):
            raise deneme_.PilotHatasi("Pay kimliği kayıtlı veri bağıyla uyuşmuyor.")
    ref = v["veri_referanslari"]
    if len(ref) != 1 or Path(ref[0]).name != ref[0] or ref[0] in (".", ".."):
        raise deneme_.PilotHatasi("Tek yerel görüntü kimliği gerekli.")


def _kayitli_donemler(donemler):
    beklenen = [
        (str(yil), dt.date(yil, 1, 1), dt.date(yil, 12, 31))
        for yil in range(2025, 2020, -1)
    ]
    beklenen.append(("birlesik", dt.date(2021, 1, 1), dt.date(2025, 12, 31)))
    if len(donemler) != len(beklenen):
        raise deneme_.PilotHatasi("Altı kayıtlı dönem gerekli.")
    for d, sinir in zip(donemler, beklenen, strict=True):
        if (d.get("ad"), d["baslangic"], d["bitis"]) != sinir or d[
            "sinir_surumu"
        ] != "bagimsiz_donem_v1":
            raise deneme_.PilotHatasi("Dönem sırası veya sınırı geçersiz.")
        if (
            type(d["isinma_baslangici"]) is not dt.date
            or d["isinma_baslangici"] >= d["baslangic"]
        ):
            raise deneme_.PilotHatasi("Dönem öncesinde açık ısınma başlangıcı gerekli.")


def _kayitli_takvim(takvim):
    if not isinstance(takvim, dict):
        raise deneme_.PilotHatasi("Takvim nesnesi gerekli.")
    if (takvim.get("baslangic"), takvim.get("bitis")) != (
        dt.date(2021, 1, 1),
        dt.date(2025, 12, 31),
    ):
        raise deneme_.PilotHatasi("Takvim 2021–2025 kapsamını taşımalıdır.")
    if (
        not isinstance(takvim.get("kaynak_ref"), str)
        or not takvim["kaynak_ref"].strip()
    ):
        raise deneme_.PilotHatasi("Takvim kaynak_ref gerekli.")
    gunler = _takvim_seanslari(takvim)
    if {t[:4] for t in gunler} != {"2021", "2022", "2023", "2024", "2025"}:
        raise deneme_.PilotHatasi("Takvim her yılın seanslarını içermelidir.")


def _takvim_seanslari(takvim):
    gunler = takvim.get("seanslar")
    if not isinstance(gunler, (list, tuple)) or not gunler:
        raise deneme_.PilotHatasi("Takvim seans listesi gerekli.")
    for t in gunler:
        if type(t) is not str:
            raise deneme_.PilotHatasi("Takvim günü ISO tarih metni olmalıdır.")
        gun = dt.date.fromisoformat(t)
        if t != gun.isoformat() or not takvim["baslangic"] <= gun <= takvim["bitis"]:
            raise deneme_.PilotHatasi("Takvim günü kapsam dışında veya geçersiz.")
    if list(gunler) != sorted(set(gunler)):
        raise deneme_.PilotHatasi("Takvim seansları sıralı ve tekil olmalıdır.")
    return gunler


def _kayitli_kimlik(commit, kirli, isci):
    dosyalar = {
        ad: sha256((kayit.PAKET / ad).read_bytes()).hexdigest()
        for ad in sorted(set(kayit.KOD_DOSYALARI) | {"tansusinama.py", "deneme.py"})
    }
    ortam = kayit._ortam() | dict(
        git_commit=commit,
        kirli=kirli,
        kod_dosyalari=dosyalar,
        isci_politikasi=dict(yontem="spawn", isci=isci),
    )
    kod = f"{KAYITLI_SURUM}:sha256:{sha256(deneme_.kanonik(dosyalar)).hexdigest()}"
    return kod, ortam


def _kayitli_sonuc(deneme, kosu_id, is_id, donem):
    return dict(
        is_id=is_id,
        donem=donem,
        deneme_id=deneme["deneme_id"],
        kosu_id=kosu_id,
        ayar_parmak_izi=deneme["ayar_parmak_izi"],
        strateji_ayar_parmak_izi=deneme["strateji"]["ayar_parmak_izi"],
        durum="tamamlandi",
        asama=None,
        neden=None,
        hatalar=[],
        adaylar=[],
        durumlar={},
        islem_referanslari=[],
        veri_referansi=None,
        uyelik=None,
        kalite=None,
        isinma={},
        isci_pid=None,
        yontemler=dict(
            deneme["yontem_ayarlari"],
            risk_surumu=deneme["risk_ayarlari"]["risk_surumu"],
            masraf_surumu=deneme["masraf_ayarlari"]["masraf_surumu"],
        ),
    )


def _kayitli_hata(sonuc, asama, hata, **baglar):
    sonuc["hatalar"].append(
        dict(asama=asama, neden=str(hata), is_id=sonuc["is_id"], **baglar)
    )
    sonuc.update(
        durum="hata", asama=sonuc["asama"] or asama, neden=sonuc["neden"] or str(hata)
    )


def _kayitli_uyelik(v, gunler, *, uyelik_kaniti=None):
    """TASARIM 5.15 #167: S10/S12 aynı kayıtlı pay anahtarını kullanır."""
    istek = veri.UyelikIstegi(tuple(gunler), v["evren_politikasi"], v["uyelik_surumu"])
    sakli = (
        {}
        if uyelik_kaniti is None
        else dict(tablo_metni=uyelik_kaniti["uyelik_tablo_metni"])
    )
    uyelik = veri.uyelik_hazirla(istek, **sakli)
    if uyelik["tablo_parmak_izi"] != v["uyelik_ozeti"]:
        raise ValueError("Üyelik parmak izi kayıtlı denemeyle uyuşmuyor.")
    if v.get("pay_kimligi") is not None:
        sakli = (
            {}
            if uyelik_kaniti is None
            else dict(tablo_metni=uyelik_kaniti["pay_kimligi_tablo_metni"])
        )
        politika = veri.pay_kimligi_hazirla(
            v["pay_kimligi"],
            kaynak=v["kaynak"],
            goruntu_id=v["veri_referanslari"][0],
            manifest_ozeti=v["manifest_ozeti"],
            **sakli,
        )
        uyelik = veri.pay_uyeligi(uyelik, politika)
    return uyelik


def _donem_uyeligi(deneme, sonuc, *, uyelik_kaniti=None):
    v, d = deneme["veri_ayarlari"], sonuc["donem"]
    bas, son = d["baslangic"].isoformat(), d["bitis"].isoformat()
    gunler = [t for t in v["takvim"]["seanslar"] if bas <= t <= son]
    uyelik = _kayitli_uyelik(v, gunler, uyelik_kaniti=uyelik_kaniti)
    sonuc["uyelik"] = uyelik
    semboller = sorted({s for t in gunler for s in uyelik["gunler"][t]["semboller"]})
    return gunler, uyelik, semboller, bas, son


def _donem_veri_istegi(v, d, semboller, bas, son):
    return veri.VeriIstegi(
        tuple(semboller),
        bas,
        son,
        v["kaynak"],
        v["kalite_surumu"],
        v["uyelik_surumu"],
        v["duzeltme_surumu"],
        v["takvim_ref"],
        (
            d["isinma_baslangici"].isoformat(),
            (d["baslangic"] - dt.timedelta(days=1)).isoformat(),
        ),
        v["evren_politikasi"],
        v.get("pay_kimligi"),
        v.get("ilk_islem"),
    )


def _donem_paketi(deneme, sonuc, veri_koku, hazirlik, kapsam):
    gunler, uyelik, semboller, bas, son = kapsam
    v, d = deneme["veri_ayarlari"], sonuc["donem"]
    istek = _donem_veri_istegi(v, d, semboller, bas, son)
    ilk_islem = _ilk_islem_kayitlari(v) if v.get("ilk_islem") is not None else None
    # TASARIM 5.15 S11: tam E1 isteği ve kaynaklar aramaya özel anahtardadır.
    anahtar = None
    if hazirlik is not None:
        anahtar = sha256(
            deneme_.kanonik(
                dict(
                    istek=asdict(istek),
                    veri=v,
                    donem=d,
                    uyelik=uyelik,
                    kok=str(Path(veri_koku).resolve()),
                )
            )
        ).hexdigest()
    if hazirlik is not None and anahtar in hazirlik:
        paket = deepcopy(hazirlik[anahtar])
    else:
        paket = veri.veri_hazirla(istek, v["veri_referanslari"][0], veri_koku)
    sonuc["veri_referansi"], sonuc["kalite"] = paket["referans"], paket["kalite"]
    if (
        paket["referans"]["manifest_parmak_izi"] != v["manifest_ozeti"]
        or paket["uyelik"]["tablo_parmak_izi"] != v["uyelik_ozeti"]
        or paket["referans"].get("pay_kimligi") != v.get("pay_kimligi")
        or paket["uyelik"].get("pay_kimligi") != v.get("pay_kimligi")
        or paket["referans"].get("ilk_islem") != v.get("ilk_islem")
    ):
        raise ValueError("E1 veri/üyelik referansı kayıtlı denemeyle uyuşmuyor.")
    if ilk_islem is not None:
        beklenen = {
            pay: veri.ilk_islem_gecmis_kaniti(
                ilk_islem[pay], v["takvim"]["seanslar"], son
            )
            for pay in set(semboller) & ilk_islem.keys()
        }
        if paket["referans"].get("gecmis_kaniti") != beklenen:
            raise ValueError("E1 ilk işlem geçmiş kanıtı önbellek öncesi uyuşmuyor.")
        paket["ilk_islem_kayitlari"] = ilk_islem
    if hazirlik is not None and anahtar not in hazirlik:
        hazirlik[anahtar] = deepcopy(paket)
    _donem_kapsami(paket, gunler, uyelik, semboller, bas, son)
    return paket


def _donem_verisi(deneme, sonuc, veri_koku, hazirlik=None):
    asama = "uyelik"
    try:
        kapsam = _donem_uyeligi(deneme, sonuc)
        asama = "veri"
        return _donem_paketi(deneme, sonuc, veri_koku, hazirlik, kapsam)
    except (
        veri.VeriHatasi,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        AttributeError,
        ArithmeticError,
        OSError,
    ) as hata:
        _kayitli_hata(sonuc, asama, hata)
        return None


def _donem_kapsami(paket, gunler, uyelik, semboller, bas, son):
    fiili = [t for t in paket["gunler"] if bas <= t <= son]
    if fiili != gunler:
        raise ValueError(
            f"İstenen seans kapsamı uyuşmuyor; eksik={sorted(set(gunler) - set(fiili))}; fazla={sorted(set(fiili) - set(gunler))}"
        )
    satirlar = {(r["sembol"], r["tarih"]): r for r in paket["piyasa"]}
    eksik = [
        (s, t)
        for t in gunler
        for s in uyelik["gunler"][t]["semboller"]
        if (s, t) not in satirlar or "eksik" in satirlar[s, t]["kalite_bayraklari"]
    ]
    if eksik:
        raise ValueError(f"Tarihli üyelerin fiyat kapsamı eksik: {eksik}")
    if set(paket["semboller"]) != set(semboller):
        raise ValueError("E1 gerekli tarihli üyeleri içermiyor.")


def _s10_mumlar(paket, sembol, hesap, *, kilit_politikasi=None):
    m = hesap["mumlar"].copy()
    m["onceki_rsi"] = m["rsi"].ffill().shift(1)
    m["onceki_dusuk"] = m["dusuk"].ffill().shift(1)
    satirlar = [r for r in paket["piyasa"] if r["sembol"] == sembol]
    for alan in ("ham_yuksek", "ham_dusuk", "tavan", "taban", "limit_kaniti"):
        degerler = [
            r.get(alan, {}).get("deger")
            if isinstance(r.get(alan, {}), dict)
            else r.get(alan)
            for r in satirlar
        ]
        # TASARIM 5.15 #176: yalnız açık politikada None ile NaN ayrılır.
        # Seçenek yokken eski pandas gösterimi ve gün/durum özetleri korunur.
        if kilit_politikasi == "ham_aralik_v1" and alan in (
            "tavan",
            "taban",
            "limit_kaniti",
        ):
            m[alan] = pd.Series(degerler, index=m.index, dtype=object)
        else:
            m[alan] = degerler
    m["islem"] = [r["islem"] for r in satirlar]
    m["karantina"] = ["karantina" in r["kalite_bayraklari"] for r in satirlar]
    return m


def _donem_yurutme(deneme, kosu_id, sembol, veri_ref_id, strateji):
    return dict(
        surum="bagimsiz_islem_v1",
        aile=simulator.AILE,
        strateji_id=strateji.kayit_id,
        strateji_surumu=strateji.katalog_surumu,
        deneme_id=deneme["deneme_id"],
        kosu_id=kosu_id,
        veri_ref_id=veri_ref_id,
        sembol=sembol,
        nominal_tutar=float(deneme["risk_ayarlari"]["nominal_tutar"]),
        risk_surumu=deneme["risk_ayarlari"]["risk_surumu"],
        masraf_surumu=deneme["masraf_ayarlari"]["masraf_surumu"],
        fiyat_politikasi=deneme["yontem_ayarlari"]["fiyat_politikasi"],
        **{
            k: deneme["yontem_ayarlari"][k]
            for k in ("kilit_politikasi",)
            if k in deneme["yontem_ayarlari"]
        },
        strateji_ayar_parmak_izi=strateji.ayar_parmak_izi,
        deneme_ayar_parmak_izi=deneme["ayar_parmak_izi"],
    )


def _donem_sembolu(deneme, sonuc, paket, sembol, hesap, strateji, p):
    d = sonuc["donem"]
    bas, son = d["baslangic"].isoformat(), d["bitis"].isoformat()
    gunler = [t for t in paket["gunler"] if bas <= t <= son]
    uyelik = sonuc["uyelik"]["gunler"]
    ilk_uye = next(t for t in gunler if sembol in uyelik[t]["semboller"])
    _isinma_kaydet(deneme, sonuc, paket, sembol, hesap, ilk_uye, p.isinma)
    m = _s10_mumlar(
        paket,
        sembol,
        hesap,
        kilit_politikasi=deneme["yontem_ayarlari"].get("kilit_politikasi"),
    )
    secilen = _aile_kurulum_secimi(hesap, sembol)
    sinyaller = _donem_sinyalleri(
        deneme, sonuc, paket, sembol, hesap, m, gunler, secilen
    )
    yurutme = _donem_yurutme(
        deneme, sonuc["kosu_id"], sembol, paket["referans"]["kayit_id"], strateji
    )
    kabuller = {}
    for s in hesap["sinyaller"]:
        if s["kayit_id"] in sinyaller.values():
            if s["baglar"]["ayar_parmak_izi"] != strateji.ayar_parmak_izi:
                raise ValueError("E2 kurulumunun seçilen ayar bağı uyuşmuyor")
            kabuller[s["kayit_id"]] = dict(
                sembol=sembol,
                tarih=s["tarih"],
                kaynak_sinyal=s,
                parametreler=motor._duz(asdict(p)),
                veri_ref=paket["referans"],
            )
    durum = saglamlik.ema_hucre_calistir(
        m.loc[bas:son],
        p,
        kurulum_kanitlari=motor.hedef_yoklugu_kanitlari(kabuller),
        sinyal_konumlari=sinyaller,
        kurulum=_kabul_kurulumu(hesap, secilen, sinyaller.values()),
        yurutme=yurutme,
    )
    sonuc["durumlar"][sembol] = durum
    for ret in durum["retler"]:
        asama = _eksik_islem_girdisi(ret, m)
        if asama is not None:
            _kayitli_hata(sonuc, asama, ret["neden"], sembol=sembol, tarih=ret["tarih"])


def _eksik_islem_girdisi(ret, mumlar):
    asamalar = {
        "limit_bilinmiyor": "limit_kaniti",
        "kurulum_eksik": "kurulum",
        "gosterge_eksik": "gosterge",
    }
    if ret["neden"] in asamalar:
        return asamalar[ret["neden"]]
    if ret["neden"] == "gecersiz_risk_girdisi":
        atr = mumlar.at[pd.Timestamp(ret["tarih"]), "atr"]
        if pd.isna(atr) or not np.isfinite(atr) or atr < 0:
            return "gosterge"
    return None


def _sinyal_uygunlugu(sembol, t, uyelik, sonraki, engeller, m):
    if sembol not in uyelik[t]["semboller"]:
        return "sinyal_gunu_uye_degil"
    if t in sonraki and sembol not in uyelik[sonraki[t]]["semboller"]:
        return "giris_gunu_uye_degil"
    if "giris_engelli" in engeller[t] or "karantina" in engeller[t]:
        return "karantina_penceresi"
    if not bool(m.at[pd.Timestamp(t), "islem"]):
        return "islem_yok"
    return None


def _aile_kurulum_secimi(hesap, sembol):
    """Aile kuralları §3 Modül 1: ilk özgün dönem satırı ve kimliği birlikte kalır."""
    kurulum, sinyaller = hesap["kurulum"], hesap["sinyaller"]
    if len(kurulum) != len(sinyaller):
        raise ValueError("E2 kurulum satırı ve sinyal sayısı uyuşmuyor")
    secilen, gunler, kimlikler = {}, set(), set()
    for i, ((t, satir), sinyal) in enumerate(
        zip(kurulum.iterrows(), sinyaller, strict=True)
    ):
        kimlik = sinyal["kayit_id"]
        if (
            sinyal["semboller"] != [sembol]
            or sinyal["tarih"] != pd.Timestamp(t).date().isoformat()
            or kimlik in kimlikler
            or not kimlik.startswith(f"{sembol}:{sinyal['tarih']}:")
            or not kimlik.endswith(":" + sinyal["baglar"]["ayar_parmak_izi"])
        ):
            raise ValueError(
                "E2 kurulum satırının özgün kimlik veya gün bağı uyuşmuyor"
            )
        for ad in ("kutu_alt", "kutu_ust", "hedef"):
            deger = satir[ad]
            if sinyal[ad]["birim"] != "TL/adet" or (
                sinyal[ad]["deger"] != (None if pd.isna(deger) else deger)
            ):
                raise ValueError("E2 kurulum satırı ve özgün değer kaydı uyuşmuyor")
        kimlikler.add(kimlik)
        if t not in gunler:
            secilen[kimlik] = i
            gunler.add(t)
    return secilen


def _kabul_kurulumu(hesap, secilen, kimlikler):
    return (
        hesap["kurulum"]
        .iloc[[i for kimlik, i in secilen.items() if kimlik in kimlikler]]
        .copy()
    )


def _donem_sinyalleri(deneme, sonuc, paket, sembol, hesap, m, gunler, secilen):
    uyelik = sonuc["uyelik"]["gunler"]
    engeller = {
        r["tarih"]: r["kalite_bayraklari"]
        for r in paket["piyasa"]
        if r["sembol"] == sembol
    }
    sonraki = dict(zip(gunler, gunler[1:], strict=False))
    sinyaller = {}
    for s in hesap["sinyaller"]:
        t = s["tarih"]
        neden = _sinyal_uygunlugu(sembol, t, uyelik, sonraki, engeller, m)
        aday = s | dict(
            yurutme_nedeni=neden
            or ("sonraki_seans_ufuk_disinda" if t not in sonraki else None)
        )
        aday["baglar"] = s["baglar"] | dict(
            deneme_id=deneme["deneme_id"],
            kosu_id=sonuc["kosu_id"],
            deneme_ayar_parmak_izi=deneme["ayar_parmak_izi"],
            bos_nedenleri={},
        )
        sonuc["adaylar"].append(aday)
        if neden is None and s["kayit_id"] in secilen:
            sinyaller[pd.Timestamp(t)] = s["kayit_id"]
    return sinyaller


def _kayitli_donem(girdi):
    deneme, sonuc, paket = girdi
    sonuc["isci_pid"] = os.getpid()
    asama = "kurulum"
    try:
        s = deneme["strateji"]
        strateji = aileler_.legacy_coz(
            s["varyant"],
            s["katalog_surumu"],
            sayisal_ayarlar={
                a["ad"]: a["deger"]
                for a in s["parametreler"]
                if a["koken"] == "legacy_izgara"
            },
        )
        if strateji.ayar_parmak_izi != s["ayar_parmak_izi"]:
            raise ValueError("Kayıtlı strateji parmak izi uyuşmuyor.")
        p = aileler_.Parametre(**{a.ad: a.deger for a in strateji.parametreler})
        hesaplar = aileler_.ortak_donem_kurulumu(paket, strateji)
        asama = "islem"
        for sembol, hesap in hesaplar.items():
            _donem_sembolu(deneme, sonuc, paket, sembol, hesap, strateji, p)
    except (
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        AttributeError,
        ArithmeticError,
        OSError,
    ) as hata:
        _kayitli_hata(sonuc, asama, hata)
    return sonuc


def _donem_islemleri(sonuc):
    for sembol, durum in sonuc["durumlar"].items():
        for islem in durum["islemler"]:
            yield sembol, islem
        if durum["pozisyon"] is not None and any(
            d["yon"] == "alis" for d in durum["dolumlar"]
        ):
            yield (
                sembol,
                dict(
                    pozisyon=durum["pozisyon"],
                    dolumlar=durum["dolumlar"],
                    sonuc=durum["sonuc"],
                    durum=durum["durum"],
                    degerleme=durum["degerleme"],
                ),
            )


def _donem_yaz(kosu, sonuc, onceki):
    donem = sonuc["donem"]
    for _, islem in _donem_islemleri(sonuc):
        makbuz = kosu.islem_kaydet(
            sinyal_id=islem["pozisyon"]["risk_girdisi"]["sinyal_id"],
            donem=donem,
            birimler=DONEM_BIRIMLERI,
            muhasebe_politikasi="tani_referans_v1",
            uyarilar=[],
            cikti_referanslari=[],
            olaylar=[islem],
        )
        sonuc["islem_referanslari"].append(makbuz.olay_id)
    refs = [s["makbuz"].olay_id for s in onceki] if donem["ad"] == "birlesik" else []
    sonuc["cikti_parmak_izi"] = sha256(deneme_.kanonik(sonuc)).hexdigest()
    makbuz = kosu.donem_sonucu_kaydet(
        is_id=sonuc["is_id"],
        donem=donem,
        durum=sonuc["durum"],
        islem_referanslari=sonuc["islem_referanslari"],
        birimler=DONEM_BIRIMLERI,
        muhasebe_politikasi="tani_referans_v1",
        uyarilar=sonuc["hatalar"],
        cikti_referanslari=refs,
        icerik=sonuc,
    )
    return sonuc | {"makbuz": makbuz}


def _kayitli_isci(isci):
    if isci is not None and (type(isci) is not int or isci < 1):
        raise deneme_.PilotHatasi("İşçi sayısı pozitif tamsayı olmalıdır.")
    isci = min(
        6,
        isci
        if isci is not None
        else isci_sayisi(
            psutil.cpu_count(logical=False) or 1,
            psutil.virtual_memory().available / 2**30,
            6,
        ),
    )
    return isci


def _kayitli_baslangic(depo, deneme_id, veri_koku, mod, isci, *, arama=False):
    if mod not in ("gelistirme", "resmi"):
        raise deneme_.PilotHatasi("Koşu modu açıkça gelistirme veya resmi olmalıdır.")
    commit, kirli = kayit._git()
    if mod == "resmi" and kirli:
        raise kayit.KayitHatasi("Kirli ağaçta resmi koşu yapılamaz.")
    deneme = depo.deneme_oku(deneme_id)
    if arama:
        _arama_istegi(deneme)
    else:
        _kayitli_istek(deneme)
    isci = _kayitli_isci(isci)
    v = deneme["veri_ayarlari"]
    manifest = Path(veri_koku) / "ag" / v["veri_referanslari"][0] / "manifest.json"
    if sha256(manifest.read_bytes()).hexdigest() != v["manifest_ozeti"]:
        raise deneme_.PilotHatasi("Manifest parmak izi kayıtlı denemeyle uyuşmuyor.")
    kod, ortam = _kayitli_kimlik(commit, kirli, isci)
    if arama:
        dosyalar = ortam["kod_dosyalari"] | {
            "aktarim.py": sha256((kayit.PAKET / "aktarim.py").read_bytes()).hexdigest(),
        }
        ortam["kod_dosyalari"] = dict(sorted(dosyalar.items()))
        kod = f"{ARAMA_SURUM}:sha256:{sha256(deneme_.kanonik(dosyalar)).hexdigest()}"
    return deneme, kod, ortam, isci


def _isci_baslat(havuz, deneme, sonuc, veri_koku, hazirlik=None):
    paket = _donem_verisi(deneme, sonuc, veri_koku, hazirlik)
    if paket is None:
        return None
    try:
        return havuz.submit(_kayitli_donem, (deneme, sonuc, paket))
    except (OSError, RuntimeError) as hata:
        _kayitli_hata(sonuc, "isci", hata)
        return None


def _isci_sonucu(sonuc, gelecek):
    if gelecek is not None:
        try:
            return gelecek.result()
        except Exception as hata:
            logging.exception("Dönem işçisi tamamlanamadı: %s", sonuc["is_id"])
            _kayitli_hata(sonuc, "isci", hata)
    return sonuc


def _kayitli_isleri_yurut(deneme, kosu, veri_koku, isci, ilerleme, hazirlik=None):
    sonuclar, bekleyen = [], []
    try:
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=isci, mp_context=multiprocessing.get_context("spawn")
        ) as havuz:
            donemler = iter(deneme["donemler"])
            while True:
                for donem in itertools.islice(donemler, isci - len(bekleyen)):
                    sonuc = _kayitli_sonuc(
                        deneme, kosu.makbuz.kosu_id, f"donem:{donem['ad']}", donem
                    )
                    bekleyen.append(
                        (sonuc, _isci_baslat(havuz, deneme, sonuc, veri_koku, hazirlik))
                    )
                if not bekleyen:
                    break
                sonuc, gelecek = bekleyen.pop(0)
                sonuc = _isci_sonucu(sonuc, gelecek)
                sonuclar.append(_donem_yaz(kosu, sonuc, sonuclar))
                if ilerleme is not None:
                    ilerleme(f"{sonuc['donem']['ad']}: {sonuc['durum']}")
    except deneme_.PilotYazmaHatasi as hata:
        hata.donem_sonuclari = sonuclar
        hata.yazilamayan_donem = sonuc
        raise
    except Exception as hata:
        try:
            _, hata.bitis_makbuzu = _kayitli_bitir(kosu, deneme, sonuclar, hata)
        except Exception as bitis_hatasi:
            bitis_hatasi.donem_sonuclari = sonuclar
            raise
        hata.donem_sonuclari = sonuclar
        raise
    return sonuclar


def _kayitli_bitir(kosu, deneme, sonuclar, hata=None):
    tamamlanan = [s["is_id"] for s in sonuclar if s["durum"] == "tamamlandi"]
    isler = [f"donem:{d['ad']}" for d in deneme["donemler"]]
    basarisiz = [is_id for is_id in isler if is_id not in tamamlanan]
    durum = "hata" if basarisiz or hata is not None else "tamamlandi"
    ozet = _donem_cikti_ozeti(sonuclar)
    if hata is not None:
        ozet["hatalar"].append(
            dict(asama="koordinator", neden=str(hata), etkilenen_isler=basarisiz)
        )
    bitis = kosu.bitir(
        durum=durum,
        tamamlanan=tamamlanan,
        basarisiz=basarisiz,
        yontemler=[KAYITLI_SURUM, "bagimsiz_islem_v1"],
        olculer={},
        cikti_referanslari=[s["makbuz"].olay_id for s in sonuclar],
        ozetler=ozet,
    )
    return durum, bitis


def _donem_cikti_ozeti(sonuclar):
    return dict(
        hatalar=[h for s in sonuclar for h in s["hatalar"]],
        cikti_parmak_izleri={s["is_id"]: s["cikti_parmak_izi"] for s in sonuclar},
    )


def kayitli_calistir(depo, deneme_id, *, veri_koku, mod, isci=None, ilerleme=print):
    """TASARIM 5.15 S10: kayıtlı denemenin altı bağımsız dönem işini yürüt."""
    return _kayitli_yurut(depo, deneme_id, veri_koku, mod, isci, ilerleme)


def _kayitli_yurut(
    depo,
    deneme_id,
    veri_koku,
    mod,
    isci,
    ilerleme,
    *,
    hazirlik=None,
    beklenen=None,
    ayar_ozeti=None,
):
    deneme, kod, ortam, isci = _kayitli_baslangic(depo, deneme_id, veri_koku, mod, isci)
    if ayar_ozeti is not None and deneme["ayar_parmak_izi"] != ayar_ozeti:
        raise deneme_.PilotHatasi("Toplu karşılaştırmanın kayıtlı ayarı değişti.")
    if beklenen is not None:
        _cocuk_ayari_dogrula(beklenen, deneme)
    v = deneme["veri_ayarlari"]
    isler = [f"donem:{d['ad']}" for d in deneme["donemler"]]
    with depo.kosu(
        deneme_id,
        mod=mod,
        anlik_goruntu=v["veri_referanslari"][0],
        manifest_ozeti=v["manifest_ozeti"],
        uyelik_surumu=v["uyelik_surumu"],
        kod_kimligi=kod,
        ortam=ortam,
        bagimlilik_ozeti=ortam["lock_sha256"],
        tohum=None,
        is_listesi=isler,
        **(
            {"uyelik_kaniti": _ileri_uyelik_kaniti(v)}
            if v.get("ilk_islem") is not None
            else {}
        ),
    ) as kosu:
        sonuclar = []
        try:
            if kosu.makbuz.ayar_ozeti != deneme["ayar_parmak_izi"]:
                raise deneme_.PilotHatasi("Başlangıç makbuzu hesap ayarıyla uyuşmuyor.")
            sonuclar = _kayitli_isleri_yurut(
                deneme, kosu, veri_koku, isci, ilerleme, hazirlik
            )
            durum, bitis = _kayitli_bitir(kosu, deneme, sonuclar)
        except Exception as hata:
            hata.baslangic_makbuzu = kosu.makbuz
            if not hasattr(hata, "donem_sonuclari"):
                hata.donem_sonuclari = sonuclar
            raise
    return dict(
        surum=KAYITLI_SURUM,
        deneme_id=deneme_id,
        kosu_id=kosu.makbuz.kosu_id,
        ayar_parmak_izi=deneme["ayar_parmak_izi"],
        durum=durum,
        donemler=sonuclar,
        baslangic_makbuzu=kosu.makbuz,
        bitis_makbuzu=bitis,
    )


def kayitli_izgara_calistir(
    depo, arama_deneme_id, *, veri_koku, mod, isci=None, ilerleme=print
):
    """TASARIM 5.15 S11: kayıtlı aramanın bütün hücrelerini koru."""
    d, kod, ortam, isci = _kayitli_baslangic(
        depo, arama_deneme_id, veri_koku, mod, isci, arama=True
    )
    hucreler = _arama_alani(d)
    sonuc = dict(
        surum=ARAMA_SURUM,
        deneme_id=arama_deneme_id,
        kosu_id=None,
        ayar_parmak_izi=d["ayar_parmak_izi"],
        manifest=deepcopy(deneme_._ayarlar(d)),
        hucreler=hucreler,
        bolgeler=[],
        durum="baslamadi",
        baslangic_makbuzu=None,
        sonuc_makbuzu=None,
        bitis_makbuzu=None,
    )
    v = d["veri_ayarlari"]
    isler = ["arama", *(h["is_id"] for h in hucreler if h["durum"] != "alan_disi")]
    try:
        with depo.kosu(
            arama_deneme_id,
            mod=mod,
            anlik_goruntu=v["veri_referanslari"][0],
            manifest_ozeti=v["manifest_ozeti"],
            uyelik_surumu=v["uyelik_surumu"],
            kod_kimligi=kod,
            ortam=ortam,
            bagimlilik_ozeti=ortam["lock_sha256"],
            tohum=None,
            is_listesi=isler,
            **(
                {"uyelik_kaniti": _ileri_uyelik_kaniti(v)}
                if v.get("ilk_islem") is not None
                else {}
            ),
        ) as kosu:
            sonuc["baslangic_makbuzu"] = kosu.makbuz
            sonuc["kosu_id"] = kosu.makbuz.kosu_id
            if kosu.makbuz.ayar_ozeti != d["ayar_parmak_izi"]:
                raise deneme_.PilotHatasi(
                    "Üst başlangıç makbuzu arama ayarıyla uyuşmuyor."
                )
            try:
                _arama_hucrelerini_yurut(depo, d, sonuc, veri_koku, mod, isci, ilerleme)
                sonuc["bolgeler"] = _arama_bolgeleri(d, hucreler)
                sonuc["sonuc_makbuzu"] = _arama_yayinla(kosu, d, sonuc)
                _arama_bitir(kosu, sonuc, isler)
            except deneme_.PilotYazmaHatasi:
                kosu._yazma_hatasi = True
                raise
    except deneme_.PilotYazmaHatasi as hata:
        sonuc["durum"] = "kayit_hatasi"
        raise AramaYazmaHatasi(sonuc, hata) from hata
    return sonuc


class AramaYazmaHatasi(deneme_.PilotYazmaHatasi):
    """TASARIM 5.15 S11: doğrulanmış makbuzlar ve yazılamayan yuvalar korunur."""

    def __init__(self, sonuc, hata):
        self.sonuc, self.yazma_hatasi = sonuc, hata
        super().__init__(str(hata))


def _arama_eksen_degerleri(ad, degerler):
    if not isinstance(degerler, list) or not degerler:
        raise deneme_.PilotHatasi(f"Boş olmayan eksen değerleri gerekli: {ad}")
    turler = (int, float) if ad == "esik" else (int,)
    for x in degerler:
        if type(x) not in turler or x not in saglamlik.IZGARA[simulator.AILE][ad]:
            raise deneme_.PilotHatasi(f"İzin verilmeyen eksen değeri: {ad}")
    if degerler != sorted(set(degerler)):
        raise deneme_.PilotHatasi(f"Eksen değerleri artan ve tekil olmalıdır: {ad}")


def _arama_eksenleri(eksenler):
    if not isinstance(eksenler, list) or not eksenler:
        raise deneme_.PilotHatasi("Boş olmayan sayısal eksen listesi gerekli.")
    adlar = []
    for e in eksenler:
        if not isinstance(e, dict) or set(e) != {"ad", "birim", "degerler"}:
            raise deneme_.PilotHatasi("Eksen ad, birim ve değerler içermelidir.")
        ad = e["ad"]
        if ad not in saglamlik.IZGARA[simulator.AILE]:
            raise deneme_.PilotHatasi(f"İzin verilmeyen eksen: {ad}")
        if e["birim"] != ("oran" if ad == "esik" else "gun"):
            raise deneme_.PilotHatasi(f"İzin verilmeyen eksen birimi: {ad}")
        _arama_eksen_degerleri(ad, e["degerler"])
        adlar.append(ad)
    if adlar != sorted(set(adlar)):
        raise deneme_.PilotHatasi("Eksen adları kanonik sırada ve tekil olmalıdır.")


def _arama_istegi(d):
    y = d["yontem_ayarlari"]
    if set(y) != {
        "yontem",
        "tekrar",
        "secim_politikasi",
        "olcu_politikasi",
        "eksenler",
        "hucre_yontemi",
    } or (y["yontem"], y["tekrar"], y["secim_politikasi"], y["olcu_politikasi"]) != (
        ARAMA_SURUM,
        0,
        "genis_bolge_net_r_v1",
        "bagimsiz_olcu_v1",
    ):
        raise deneme_.PilotHatasi("Desteklenmeyen arama yöntemi.")
    # Yalnız doğrulanmış üst zarf kendi tam S10 çocuk yöntemini türetebilir.
    _kayitli_istek(d | dict(yontem_ayarlari=y["hucre_yontemi"]))
    _arama_eksenleri(y["eksenler"])
    return y["eksenler"]


def _bos_hucre_donemleri(d, neden="hucre_baslamadi"):
    return [
        dict(
            donem=deepcopy(x),
            durum="baslamadi",
            neden=neden,
            asama=None,
            is_id=f"donem:{x['ad']}",
            sonuc_ref=None,
            islem_referanslari=[],
            semboller=[],
            beklenen_semboller=[],
        )
        for x in d["donemler"]
    ]


def _arama_alani(d):
    eksenler = d["yontem_ayarlari"]["eksenler"]
    s = d["strateji"]
    sabit = {
        a["ad"]: a["deger"] for a in s["parametreler"] if a["koken"] == "legacy_izgara"
    }
    hucreler = []
    for indeks in itertools.product(*(range(len(e["degerler"])) for e in eksenler)):
        h = {e["ad"]: e["degerler"][i] for e, i in zip(eksenler, indeks, strict=True)}
        yuva = dict(
            indeks=list(indeks),
            is_id="hucre:" + ":".join(map(str, indeks)),
            ayarlar=h,
            ust_deneme_id=d["deneme_id"],
            deneme_id=None,
            kosu_id=None,
            ayar_parmak_izi=None,
            strateji_ayar_parmak_izi=None,
            tam_ayarlar=None,
            kayit_makbuzu=None,
            baslangic_makbuzu=None,
            bitis_makbuzu=None,
            durum="baslamadi",
            neden="hucre_baslamadi",
            donemler=_bos_hucre_donemleri(d),
        )
        try:
            strateji = katalog.legacy_coz(
                s["varyant"], s["katalog_surumu"], sayisal_ayarlar=sabit | h
            )
            tam = deneme_._ayarlar(
                d
                | dict(
                    strateji=asdict(strateji),
                    yontem_ayarlari=d["yontem_ayarlari"]["hucre_yontemi"],
                )
            )
            yuva.update(
                tam_ayarlar=tam, strateji_ayar_parmak_izi=strateji.ayar_parmak_izi
            )
        except (katalog.KatalogHatasi, ValueError, OverflowError) as hata:
            yuva.update(
                durum="alan_disi",
                neden=str(hata),
                donemler=_bos_hucre_donemleri(d, "alan_disi"),
            )
        hucreler.append(yuva)
    return hucreler


def _cocuk_ayari_dogrula(h, d):
    if (
        d["ust_deneme_id"] != h["ust_deneme_id"]
        or d["baglar"].get("izgara_ust_deneme") != h["ust_deneme_id"]
        or d["strateji"]["ayar_parmak_izi"] != h["strateji_ayar_parmak_izi"]
        or deneme_.kanonik(deneme_._ayarlar(d)) != deneme_.kanonik(h["tam_ayarlar"])
        or (
            h["ayar_parmak_izi"] is not None
            and d["ayar_parmak_izi"] != h["ayar_parmak_izi"]
        )
    ):
        raise deneme_.PilotHatasi(
            "Çocuk tam ayarı veya üst bağı dondurulmuş hücreyle uyuşmuyor."
        )


def _arama_hucre_durumu(h):
    hatali = [x for x in h["donemler"] if x["durum"] not in ("tamamlandi", "islemsiz")]
    if hatali:
        h.update(durum=hatali[0]["durum"], neden=hatali[0]["neden"])
        return
    durum = (
        "tamamlandi"
        if any(x["durum"] == "tamamlandi" for x in h["donemler"])
        else "islemsiz"
    )
    h.update(durum=durum, neden=None)


def _arama_hucrelerini_kaydet(aktarim, hucreler):
    for h in hucreler:
        if h["durum"] == "alan_disi":
            continue
        try:
            cocuk = aktarim.cocuk(h["ayarlar"])
            h.update(
                deneme_id=cocuk.deneme_id,
                ayar_parmak_izi=cocuk.kayit_makbuzu.ayar_ozeti,
                kayit_makbuzu=asdict(cocuk.kayit_makbuzu),
            )
            _cocuk_ayari_dogrula(h, cocuk.kayit)
        except deneme_.PilotYazmaHatasi as hata:
            _arama_hucresi_hatasi(h, hata, "kayit_hatasi")
            raise
        except Exception as hata:
            logging.exception("Arama hücresi kaydedilemedi: %s", h["is_id"])
            _arama_hucresi_hatasi(h, hata, "kayit_hatasi")
            return False
    return True


def _arama_hucresi_yurut(depo, h, veri_koku, mod, isci, ilerleme, hazirlik):
    r = _kayitli_yurut(
        depo,
        h["deneme_id"],
        veri_koku,
        mod,
        isci,
        ilerleme,
        hazirlik=hazirlik,
        beklenen=h,
    )
    h.update(
        kosu_id=r["kosu_id"],
        baslangic_makbuzu=asdict(r["baslangic_makbuzu"]),
        bitis_makbuzu=asdict(r["bitis_makbuzu"]),
    )
    _arama_donemlerini_aktar(h, r["donemler"])
    _arama_hucre_durumu(h)


def _arama_hucrelerini_yurut(depo, d, sonuc, veri_koku, mod, isci, ilerleme):
    from tansu.aktarim import AyarAktarimi

    aktarim = AyarAktarimi(depo, d["deneme_id"])
    if aktarim.ozet != d["ayar_parmak_izi"]:
        raise deneme_.PilotHatasi("Üst arama tam ayarı değişti.")
    if not _arama_hucrelerini_kaydet(aktarim, sonuc["hucreler"]):
        return
    hazirlik = {}
    for h in sonuc["hucreler"]:
        if h["durum"] == "alan_disi":
            continue
        try:
            _arama_hucresi_yurut(depo, h, veri_koku, mod, isci, ilerleme, hazirlik)
        except deneme_.PilotYazmaHatasi as hata:
            _arama_hucresi_hatasi(h, hata, "kayit_hatasi")
            raise
        except Exception as hata:
            logging.exception("Arama hücresi tamamlanamadı: %s", h["is_id"])
            _arama_hucresi_hatasi(h, hata, "hesap_hatasi")


def _arama_hucresi_hatasi(h, hata, durum):
    h.update(durum=durum, neden=str(hata))
    kayit_makbuzu = getattr(hata, "kayit_makbuzu", None)
    if kayit_makbuzu is not None:
        h.update(
            deneme_id=kayit_makbuzu.deneme_id,
            ayar_parmak_izi=kayit_makbuzu.ayar_ozeti,
            kayit_makbuzu=asdict(kayit_makbuzu),
        )
    makbuz = getattr(hata, "baslangic_makbuzu", None)
    if makbuz is not None:
        h["kosu_id"] = makbuz.kosu_id
        alan = (
            "baslangic_makbuzu"
            if makbuz.ayar_ozeti == h["ayar_parmak_izi"]
            else "reddedilen_baslangic_makbuzu"
        )
        h[alan] = asdict(makbuz)
    bitis = getattr(hata, "bitis_makbuzu", None)
    if bitis is not None:
        h["bitis_makbuzu"] = asdict(bitis)
    sonuclar = getattr(hata, "donem_sonuclari", [])
    if sonuclar:
        _arama_donemlerini_aktar(h, sonuclar)
    yazilamayan = getattr(hata, "yazilamayan_donem", None)
    for x in h["donemler"]:
        if x["durum"] == "baslamadi":
            x["neden"] = str(hata)
        if yazilamayan is not None and x["donem"] == yazilamayan["donem"]:
            x.update(
                durum="kayit_hatasi",
                neden=str(hata),
                islem_referanslari=list(yazilamayan["islem_referanslari"]),
            )


def _arama_islem_baglari(r):
    islemler = list(_donem_islemleri(r))
    refs = r["islem_referanslari"]
    if len(islemler) != len(refs):
        raise deneme_.PilotHatasi("Gerçek işlem ve makbuz sayısı uyuşmuyor.")
    semboller = {s: [] for s in r["durumlar"]}
    for (sembol, islem), ref in zip(islemler, refs, strict=True):
        semboller[sembol].append(islem | dict(islem_ref=ref))
    return semboller


def _arama_sembol_olculeri(r):
    semboller = []
    for sembol, islemler in _arama_islem_baglari(r).items():
        egri = istatistik.kapali_r_egrisi(islemler, r["donem"])
        olcu = istatistik.olc(islemler, politika="bagimsiz_olcu_v1", egri=egri)
        durum = _arama_donem_durumu(r, olcu["olculer"]["islem"]["deger"])
        dogal = r["isinma"].get(sembol, {}).get("dogal_bekleyis")
        semboller.append(
            dict(
                sembol=sembol,
                durum=durum,
                olcu=olcu,
                **({"dogal_bekleyis": deepcopy(dogal)} if dogal is not None else {}),
            )
        )
    return semboller


def _arama_donemlerini_aktar(h, sonuclar):
    for r in sonuclar:
        yuva = next(x for x in h["donemler"] if x["donem"] == r["donem"])
        semboller = _arama_sembol_olculeri(r)
        uyeler = sorted(
            {
                s
                for gun in (r["uyelik"] or {}).get("gunler", {}).values()
                for s in gun["semboller"]
            }
        )
        sayi = sum(s["olcu"]["olculer"]["islem"]["deger"] for s in semboller)
        yuva.update(
            durum=_arama_donem_durumu(r, sayi),
            neden=r["neden"],
            asama=r["asama"],
            sonuc_ref=r["makbuz"].olay_id,
            islem_referanslari=list(r["islem_referanslari"]),
            semboller=semboller,
            beklenen_semboller=uyeler,
            veri_referansi=r["veri_referansi"],
            hatalar=r["hatalar"],
        )


def _arama_donem_durumu(r, sayi):
    if r["durum"] == "tamamlandi":
        return "tamamlandi" if sayi else "islemsiz"
    return (
        "eksik"
        if r["asama"]
        in ("veri", "uyelik", "isinma", "limit_kaniti", "kurulum", "gosterge")
        else "hesap_hatasi"
    )


def _arama_secim_ozeti(h, no, sembol):
    r = h["donemler"][no]
    s = next((s for s in r["semboller"] if s["sembol"] == sembol), None)
    o = s["olcu"]["olculer"] if s is not None else {}
    durum = s["durum"] if s else r["durum"]
    if h["durum"] == "alan_disi":
        durum = "alan_disi"
    return dict(
        indeks=h["indeks"],
        deneme_id=h["deneme_id"],
        durum=durum,
        kapali_islem_sayisi=o.get("islem", {}).get("deger"),
        toplam_net_r=o.get("net_r", {}).get("deger"),
    )


def _arama_sembol_bolgesi(d, hucreler, no, sembol):
    ozetler = [_arama_secim_ozeti(h, no, sembol) for h in hucreler]
    b = saglamlik.sec(
        dict(eksenler=d["yontem_ayarlari"]["eksenler"]),
        ozetler,
        politika="genis_bolge_net_r_v1",
    )
    secilen = next((h for h in hucreler if h["indeks"] == b["secilen"]), None)
    return b | dict(
        donem=d["donemler"][no],
        sembol=sembol,
        strateji_id=d["strateji"]["kayit_id"],
        secilen_deneme_id=secilen["deneme_id"] if secilen is not None else None,
    )


def _arama_bolgeleri(d, hucreler):
    bolgeler = []
    for no, _ in enumerate(d["donemler"]):
        semboller = sorted(
            {s for h in hucreler for s in h["donemler"][no]["beklenen_semboller"]}
        )
        for sembol in semboller or [None]:
            bolgeler.append(_arama_sembol_bolgesi(d, hucreler, no, sembol))
    return bolgeler


def _arama_yayinla(kosu, d, sonuc):
    hucreler = sonuc["hucreler"]
    return kosu.arama_sonucu_kaydet(
        is_id="arama",
        hucreler=hucreler,
        bolgeler=sonuc["bolgeler"],
        politika_surumu=d["yontem_ayarlari"]["secim_politikasi"],
        birimler=DONEM_BIRIMLERI | dict(masraf="TL", net_fiyat_getirisi="oran"),
        uyarilar=[
            dict(is_id=h["is_id"], neden=h["neden"]) for h in hucreler if h["neden"]
        ],
        cikti_referanslari=[
            r["sonuc_ref"] for h in hucreler for r in h["donemler"] if r["sonuc_ref"]
        ],
    )


def _arama_bitir(kosu, sonuc, isler):
    tamamlanan = [
        "arama",
        *(
            h["is_id"]
            for h in sonuc["hucreler"]
            if h["durum"] in ("tamamlandi", "islemsiz")
        ),
    ]
    basarisiz = [i for i in isler if i not in tamamlanan]
    sonuc["durum"] = "hata" if basarisiz else "tamamlandi"
    sonuc["bitis_makbuzu"] = kosu.bitir(
        durum=sonuc["durum"],
        tamamlanan=tamamlanan,
        basarisiz=basarisiz,
        yontemler=[ARAMA_SURUM, "bagimsiz_olcu_v1", "genis_bolge_net_r_v1"],
        olculer={},
        cikti_referanslari=[sonuc["sonuc_makbuzu"].olay_id],
        ozetler=dict(
            manifest=sonuc["manifest"],
            hucre_durumlari=[
                dict(is_id=h["is_id"], durum=h["durum"], neden=h["neden"])
                for h in sonuc["hucreler"]
            ],
        ),
    )


# TASARIM 5.15 Kayıtlı varyant karşılaştırması: yalnız mevcut adlandırılmış tanımlar.
def _varyant_kayitlarini_dogrula(depo, esleme):
    if not isinstance(esleme, dict) or set(esleme) != set(aileler_.VARYANTLAR):
        raise deneme_.PilotHatasi("Mevcut varyantların tam ad→deneme eşlemesi gerekli.")
    ids = list(esleme.values())
    if any(type(i) is not str or not i.strip() for i in ids) or len(set(ids)) != len(
        ids
    ):
        raise deneme_.PilotHatasi("Deneme kimlikleri dolu metin ve tekil olmalıdır.")
    kayitlar, ortak = [], None
    for ad in aileler_.VARYANTLAR:
        d = depo.deneme_oku(esleme[ad])
        _kayitli_istek(d)
        s = d["strateji"]
        if (
            s["varyant"] != ad
            or s["ayar_parmak_izi"] != katalog.legacy_coz(ad).ayar_parmak_izi
        ):
            raise deneme_.PilotHatasi(
                f"{ad}: kayıt mevcut adlandırılmış varyantla uyuşmuyor."
            )
        girdi = deneme_.kanonik(
            {
                a: d[a]
                for a in (
                    "donemler",
                    "veri_ayarlari",
                    "yontem_ayarlari",
                    "risk_ayarlari",
                    "masraf_ayarlari",
                )
            }
        )
        if ortak is not None and ortak != girdi:
            raise deneme_.PilotHatasi(f"{ad}: karşılaştırma girdileri farklı.")
        ortak = girdi
        kayitlar.append(d)
    return kayitlar


def _varyant_donemlerini_aktar(v, sonuclar):
    _arama_donemlerini_aktar(v, sonuclar)
    for r in sonuclar:
        yuva = next(x for x in v["donemler"] if x["donem"] == r["donem"])
        yuva.update(
            kapali_islem_sayisi=(
                sum(s["olcu"]["olculer"]["islem"]["deger"] for s in yuva["semboller"])
                if r["durum"] == "tamamlandi"
                else None
            ),
            acik_islemler=[
                dict(
                    sembol=ad,
                    durum=d["durum"],
                    sonuc=d["sonuc"],
                    degerleme=d["degerleme"],
                )
                for ad, d in r["durumlar"].items()
                if d["pozisyon"] is not None
            ],
            aday_sayisi=len(r["adaylar"]),
            durum_sayilari={
                ad: sum(d["durum"] == ad for d in r["durumlar"].values())
                for ad in {d["durum"] for d in r["durumlar"].values()}
            },
            yontemler=r["yontemler"],
            cikti_parmak_izi=r["cikti_parmak_izi"],
        )
        yuva["ret_nedenleri"] = dict(
            Counter(ret["neden"] for d in r["durumlar"].values() for ret in d["retler"])
        )
        yuva["aday_nedenleri"] = dict(
            Counter(
                a["yurutme_nedeni"]
                for a in r["adaylar"]
                if a["yurutme_nedeni"] is not None
            )
        )
        if r["durum"] == "tamamlandi" and yuva["acik_islemler"]:
            yuva["durum"] = "acik_kismi"
        for sembol in yuva["semboller"]:
            if "dogal_bekleyis" in sembol:
                ilk = r["isinma"][sembol["sembol"]]
                sembol["isinma"] = {a: ilk[a] for a in ("gozlem", "gerekli", "tamam")}
            olcu = sembol["olcu"]
            if sembol["durum"] == "islemsiz" and olcu["acik_kismi"]:
                sembol["durum"] = "acik_kismi"
            sembol["olcu"] = {
                a: olcu[a] for a in ("politika", "olculer", "egri_olculeri")
            }


def varyantlari_calistir(depo, deneme_idleri, *, veri_koku, isci=None, ilerleme=print):
    """TASARIM 5.15 #57: kayıtlı varyantları destek raporu için ayrı yürüt."""
    kayitlar = _varyant_kayitlarini_dogrula(depo, deneme_idleri)
    _kayitli_isci(isci)
    sonuc = dict(
        surum="kayitli_varyantlar_v1",
        tur="destek",
        durum="baslamadi",
        deneme_dosyasi=str(depo.yol),
        varyantlar=[],
    )
    for d in kayitlar:
        s, veri = d["strateji"], d["veri_ayarlari"]
        v = {
            a: s[a]
            for a in (
                "varyant",
                "kayit_id",
                "katalog_surumu",
                "izin_durumu",
                "eski_karsilastirma",
            )
        }
        v.update(
            deneme_id=d["deneme_id"],
            kosu_id=None,
            ayar_parmak_izi=d["ayar_parmak_izi"],
            strateji_ayar_parmak_izi=s["ayar_parmak_izi"],
            veri_referanslari=veri["veri_referanslari"],
            manifest_ozeti=veri["manifest_ozeti"],
            uyelik_ozeti=veri["uyelik_ozeti"],
            uyelik_surumu=veri["uyelik_surumu"],
            birimler=DONEM_BIRIMLERI,
            yontemler=dict(
                d["yontem_ayarlari"],
                risk_surumu=d["risk_ayarlari"]["risk_surumu"],
                masraf_surumu=d["masraf_ayarlari"]["masraf_surumu"],
            ),
            nominal_tutar=d["risk_ayarlari"]["nominal_tutar"],
            durum="baslamadi",
            neden="Varyant başlamadı.",
            baslangic_makbuzu=None,
            bitis_makbuzu=None,
            donemler=_bos_hucre_donemleri(d, "Varyant başlamadı."),
        )
        for r in v["donemler"]:
            r.update(kapali_islem_sayisi=None, acik_islemler=[], aday_sayisi=None)
        sonuc["varyantlar"].append(v)
    durdur = None
    for v in sonuc["varyantlar"]:
        if durdur is not None:
            v["neden"] = durdur
            for r in v["donemler"]:
                r.update(asama="kayit", neden=durdur)
            continue
        try:
            r = _kayitli_yurut(
                depo,
                v["deneme_id"],
                veri_koku,
                "gelistirme",
                isci,
                ilerleme,
                ayar_ozeti=v["ayar_parmak_izi"],
            )
            v.update(
                kosu_id=r["kosu_id"],
                baslangic_makbuzu=asdict(r["baslangic_makbuzu"]),
                bitis_makbuzu=asdict(r["bitis_makbuzu"]),
            )
            _varyant_donemlerini_aktar(v, r["donemler"])
            v.update(
                durum=r["durum"],
                neden=next((d["neden"] for d in v["donemler"] if d["neden"]), None),
            )
            del r
        except Exception as hata:
            logging.exception("Varyant tamamlanamadı: %s", v["varyant"])
            yazma = isinstance(hata, deneme_.PilotYazmaHatasi)
            v.update(durum="kayit_hatasi" if yazma else "hesap_hatasi", neden=str(hata))
            if isinstance(hata, deneme_.PilotBelirsizHatasi):
                v["belirsiz_yayin"] = dict(
                    kayit_id=hata.kayit_id,
                    kosu_id=hata.kosu_id,
                    deneme_id=hata.deneme_id,
                )
            bas = getattr(hata, "baslangic_makbuzu", None)
            if bas is not None:
                v.update(kosu_id=bas.kosu_id, baslangic_makbuzu=asdict(bas))
            bitis = getattr(hata, "bitis_makbuzu", None)
            if bitis is not None:
                v["bitis_makbuzu"] = asdict(bitis)
            _varyant_donemlerini_aktar(v, getattr(hata, "donem_sonuclari", []))
            yazilamayan = getattr(hata, "yazilamayan_donem", None)
            for r in v["donemler"]:
                if r["durum"] == "baslamadi":
                    r.update(asama="kayit" if yazma else "baslangic", neden=str(hata))
                if yazilamayan is not None and r["donem"] == yazilamayan["donem"]:
                    r.update(
                        durum="kayit_hatasi",
                        islem_referanslari=list(yazilamayan["islem_referanslari"]),
                    )
            if yazma:
                durdur = str(hata)
    sonuc["durum"] = (
        "tamamlandi"
        if all(v["durum"] == "tamamlandi" for v in sonuc["varyantlar"])
        else "hata"
    )
    return sonuc


# TASARIM 5.15 S12: ayrı yöntem; S10/S11 kesin doğrulayıcılarını gevşetmez.
ILERI_SURUM = "kayitli_ileri_v1"


def _ileri_kimlik(commit, kirli):
    """TASARIM 5.15 S12: devam, CLI ve kilitli paketlerin aynı halini ister."""
    kod, ortam = _kayitli_kimlik(commit, kirli, 1)
    ortam["kod_dosyalari"]["__main__.py"] = sha256(
        (kayit.PAKET / "__main__.py").read_bytes()
    ).hexdigest()
    surumler = {}
    kilit = Path(__file__).resolve().parents[1] / "requirements.lock.txt"
    for satir in kilit.read_text(encoding="utf-8").splitlines():
        if satir and not satir.startswith("#"):
            ad, _ = satir.split("==", 1)
            surumler[ad] = metadata.version(ad)
    ortam.update(
        ileri_devam_surumu="ileri_devam_v1",
        isci_politikasi=dict(yontem="seri", isci=1),
        bagimliliklar=surumler,
        python_uygulamasi=platform.python_implementation(),
        python_surumu=sys.version,
        platform=platform.platform(),
        mimari=platform.machine(),
    )
    kod = f"{ILERI_SURUM}:sha256:{sha256(deneme_.kanonik(ortam['kod_dosyalari'])).hexdigest()}"
    return kod, ortam


def _ileri_istek(d):
    y = d["yontem_ayarlari"]
    beklenen = dict(
        yontem=ILERI_SURUM,
        tekrar=0,
        egitim_ay=12,
        test_ay=3,
        adim_ay=3,
        secim_politikasi="genis_bolge_net_r_v1",
        olcu_politikasi="bagimsiz_olcu_v1",
        eksenler=y.get("eksenler"),
        hucre_yontemi=y.get("hucre_yontemi"),
        veri_gorulme_durumu="incelenmis_gecmis",
    )
    if y != beklenen:
        raise deneme_.PilotHatasi("Eksik veya desteklenmeyen WF yöntem kaydı.")
    _yurutme_ayarlari(d | dict(yontem_ayarlari=y["hucre_yontemi"]))
    _kayitli_veri_ayarlari(d["veri_ayarlari"])
    _kayitli_takvim(d["veri_ayarlari"].get("takvim", {}))
    _arama_eksenleri(y["eksenler"])
    if len(d["donemler"]) != 16:
        raise deneme_.PilotHatasi("On altı kronolojik WF test dönemi gerekli.")
    for no, b in enumerate(d["donemler"]):
        yil, ay = 2022 + no // 4, 1 + 3 * (no % 4)
        bas = dt.date(yil, ay, 1)
        sonraki = dt.date(yil + (ay == 10), 1 if ay == 10 else ay + 3, 1)
        egitim = b.get("egitim", {})
        for x, ad, ilk, son in (
            (b, f"{yil}Q{no % 4 + 1}", bas, sonraki - dt.timedelta(days=1)),
            (
                egitim,
                f"{yil}Q{no % 4 + 1}:egitim",
                dt.date(yil - 1, ay, 1),
                bas - dt.timedelta(days=1),
            ),
        ):
            deneme_._donem(x)
            if (
                (x.get("ad"), x["baslangic"], x["bitis"], x["sinir_surumu"])
                != (ad, ilk, son, "surekli_ileri_v1")
                or x["isinma_baslangici"] is None
                or x["isinma_baslangici"] >= ilk
            ):
                raise deneme_.PilotHatasi(
                    "WF pencere sırası, sınırı veya ısınması geçersiz."
                )
            if not any(
                ilk.isoformat() <= t <= son.isoformat()
                for t in d["veri_ayarlari"]["takvim"]["seanslar"]
            ):
                raise deneme_.PilotHatasi(f"WF penceresinde kayıtlı seans yok: {ad}")


def _ileri_cocuk(depo, d, ust_kosu, bolum, h, rol):
    donem = (
        bolum["egitim"]
        if rol == "egitim"
        else {k: v for k, v in bolum.items() if k != "egitim"}
    )
    s = d["strateji"]
    sayisal = {
        a["ad"]: a["deger"] for a in s["parametreler"] if a["koken"] == "legacy_izgara"
    }
    strateji = katalog.legacy_coz(
        s["varyant"], s["katalog_surumu"], sayisal_ayarlar=sayisal | h["ayarlar"]
    )
    yontem = dict(
        yontem=f"ileri_{rol}_v1",
        tekrar=0,
        bolum_id=bolum["ad"],
        rol=rol,
        hucre_yontemi=d["yontem_ayarlari"]["hucre_yontemi"],
    )
    beklenen = deneme_._ayarlar(
        d | dict(strateji=asdict(strateji), donemler=[donem], yontem_ayarlari=yontem)
    )
    adaylar = [
        o
        for o in depo.oku()
        if o["kayit_turu"] == "deneme"
        and o.get("baglar", {}).get("ileri_ust_kosu") == ust_kosu.makbuz.kosu_id
        and o["yontem_ayarlari"].get("bolum_id") == bolum["ad"]
        and o["yontem_ayarlari"].get("rol") == rol
        and all(
            next(
                a["deger"] for a in o["strateji"]["parametreler"] if a["ad"] == e["ad"]
            )
            == e["degerler"][i]
            for e, i in zip(d["yontem_ayarlari"]["eksenler"], h["indeks"], strict=True)
        )
    ]
    if len(adaylar) > 1:
        raise deneme_.PilotHatasi("WF çocuk koordinatı yinelenmiş.")
    if adaylar:
        cocuk = adaylar[0]
        makbuz = deneme_.Makbuz(
            cocuk["kayit_id"], cocuk["deneme_id"], None, cocuk["ayar_parmak_izi"]
        )
    else:
        makbuz = depo.deneme_kaydet(
            strateji,
            aktor="S12",
            gerekce=f"WF {bolum['ad']} {rol}",
            donemler=[donem],
            yontem_ayarlari=yontem,
            ust_deneme=d["deneme_id"],
            baglar=dict(
                izgara_ust_deneme=d["deneme_id"],
                ileri_ust_kosu=ust_kosu.makbuz.kosu_id,
            ),
            **{
                k: d[k]
                for k in (
                    "veri_ayarlari",
                    "risk_ayarlari",
                    "masraf_ayarlari",
                    "eski_referans",
                )
            },
        )
        cocuk = depo.deneme_oku(makbuz.deneme_id)
    if (
        makbuz.ayar_ozeti != cocuk["ayar_parmak_izi"]
        or cocuk["ust_deneme_id"] != d["deneme_id"]
        or deneme_.kanonik(deneme_._ayarlar(cocuk)) != deneme_.kanonik(beklenen)
    ):
        raise deneme_.PilotHatasi("WF çocuk tam ayarı veya makbuzu uyuşmuyor.")
    return cocuk, makbuz


def _ileri_uyelik_kaniti_dogrula(v, kanit):
    """TASARIM 5.15 #167: E5 yalnız saklı kaynak ve kayıtlı bağları kullanır."""
    if v.get("ilk_islem") is not None:
        alanlar = {
            "surum",
            "uyelik_tablo_metni",
            "pay_kimligi_tablo_metni",
            "ilk_islem_tablo_metni",
        }
        if (
            not isinstance(kanit, dict)
            or set(kanit) != alanlar
            or kanit["surum"] != "uyelik_kaniti_v2"
            or any(
                not isinstance(kanit[a], str) or not kanit[a]
                for a in ("uyelik_tablo_metni", "ilk_islem_tablo_metni")
            )
            or (
                v.get("pay_kimligi") is None
                and kanit["pay_kimligi_tablo_metni"] is not None
            )
            or (
                v.get("pay_kimligi") is not None
                and (
                    not isinstance(kanit["pay_kimligi_tablo_metni"], str)
                    or not kanit["pay_kimligi_tablo_metni"]
                )
            )
        ):
            raise deneme_.PilotHatasi(
                "Üyelik kanıtı ilk işlem alanları eksik veya geçersiz."
            )
        _kayitli_uyelik(v, v["takvim"]["seanslar"], uyelik_kaniti=kanit)
        _ilk_islem_kayitlari(v, uyelik_kaniti=kanit)
        return
    alanlar = {"surum", "uyelik_tablo_metni", "pay_kimligi_tablo_metni"}
    if (
        not isinstance(kanit, dict)
        or set(kanit) != alanlar
        or kanit["surum"] != "ileri_uyelik_kaniti_v1"
        or any(not isinstance(kanit[a], str) or not kanit[a] for a in alanlar)
    ):
        raise deneme_.PilotHatasi("Üyelik kanıtı eksik veya sürüm/alanları geçersiz.")
    try:
        _kayitli_uyelik(v, v["takvim"]["seanslar"], uyelik_kaniti=kanit)
    except (veri.VeriHatasi, ValueError, TypeError, KeyError, UnicodeError) as hata:
        raise deneme_.PilotHatasi(
            f"Üyelik kanıtı kayıtlı kaynakla uyuşmuyor: {hata}"
        ) from hata


def _ileri_uyelik_kaniti(v):
    """TASARIM 5.15 #167: E4 hesap öncesi iki kaynağın tam baytlarını dondurur."""
    kok = Path(veri.__file__).parent / "referans"
    kanit = dict(
        surum="uyelik_kaniti_v2"
        if v.get("ilk_islem") is not None
        else "ileri_uyelik_kaniti_v1",
        uyelik_tablo_metni=(kok / v["uyelik_surumu"] / "uyelik.csv")
        .read_bytes()
        .decode("utf-8"),
        pay_kimligi_tablo_metni=(
            veri.PAY_KIMLIGI_KOKU / v["pay_kimligi"]["surum"] / "eslemeler.csv"
        )
        .read_bytes()
        .decode("utf-8")
        if v.get("pay_kimligi") is not None
        else None,
    )
    if v.get("ilk_islem") is not None:
        kanit["ilk_islem_tablo_metni"] = (
            (veri.ILK_ISLEM_KOKU / v["ilk_islem"]["surum"] / "ilk_islem.csv")
            .read_bytes()
            .decode("utf-8")
        )
    _ileri_uyelik_kaniti_dogrula(v, kanit)
    return kanit


def _ileri_kosu(depo, d, mod, kod, ortam, isler):
    v = d["veri_ayarlari"]
    kanit = {}
    if (
        d["yontem_ayarlari"]["yontem"] == ILERI_SURUM
        and v.get("pay_kimligi") is not None
    ) or v.get("ilk_islem") is not None:
        kanit["uyelik_kaniti"] = _ileri_uyelik_kaniti(v)
    return depo.kosu(
        d["deneme_id"],
        mod=mod,
        anlik_goruntu=v["veri_referanslari"][0],
        manifest_ozeti=v["manifest_ozeti"],
        uyelik_surumu=v["uyelik_surumu"],
        kod_kimligi=kod,
        ortam=ortam,
        bagimlilik_ozeti=ortam["lock_sha256"],
        tohum=None,
        is_listesi=isler,
        **kanit,
    )


def _ileri_egitim(depo, ust_kosu, cocuk, makbuz, kok, mod, kod, ortam, hazirlik):
    donem = cocuk["donemler"][0]
    is_id = f"donem:{donem['ad']}"
    cocuk_ortam = {k: v for k, v in ortam.items() if k != "ileri_devam_surumu"}
    baslar = [
        o
        for o in depo.oku()
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] == cocuk["deneme_id"]
    ]
    if len(baslar) > 1:
        raise deneme_.PilotHatasi("WF eğitim çocuğu birden çok kez başlamış.")
    bas = baslar[0] if baslar else None
    if bas and (
        bas["mod"] != mod
        or bas["kod_kimligi"] != kod
        or bas["ortam"] != cocuk_ortam
        or bas["ayar_parmak_izi"] != cocuk["ayar_parmak_izi"]
        or bas["is_listesi"] != [is_id]
    ):
        raise deneme_.PilotHatasi("WF eğitim çocuğunun başlangıcı değişmiş.")
    sonuc = [
        o
        for o in depo.oku()
        if bas
        and o["kayit_turu"] == "sonuc"
        and o.get("sonuc_turu") == "donem_v1"
        and o["kosu_id"] == bas["kosu_id"]
    ]
    bitisler = [
        o
        for o in depo.oku()
        if bas and o["kayit_turu"] == "bitis" and o["kosu_id"] == bas["kosu_id"]
    ]
    if len(sonuc) > 1 or len(bitisler) > 1 or (bitisler and not sonuc):
        raise deneme_.PilotHatasi("WF eğitim sonucu veya bitişi yinelenmiş.")

    def bitir(kosu, r):
        return kosu.bitir(
            durum=r["durum"],
            tamamlanan=[is_id] if r["durum"] == "tamamlandi" else [],
            basarisiz=[] if r["durum"] == "tamamlandi" else [is_id],
            yontemler=[ILERI_SURUM, "bagimsiz_islem_v1"],
            olculer={},
            cikti_referanslari=[r["makbuz"].olay_id],
            ozetler=dict(hatalar=r["hatalar"]),
        )

    if sonuc:
        kayit = sonuc[0]
        r = kayit["icerik"] | dict(
            makbuz=deneme_.Makbuz(
                kayit["kayit_id"],
                cocuk["deneme_id"],
                bas["kosu_id"],
                cocuk["ayar_parmak_izi"],
            )
        )
        if r["durum"] != "tamamlandi":
            raise deneme_.PilotHatasi("Başarısız WF eğitim çocuğu devam ettirilemez.")
        if bitisler:
            bitis = deneme_.Makbuz(
                bitisler[0]["kayit_id"],
                cocuk["deneme_id"],
                bas["kosu_id"],
                cocuk["ayar_parmak_izi"],
            )
        else:
            with depo._ileri_cocuk_devam(
                ust_kosu.makbuz.kosu_id, cocuk, bas, sonuc_hazir=True
            ) as kosu:
                bitis = bitir(kosu, r)
    else:
        baglam = (
            depo._ileri_cocuk_devam(ust_kosu.makbuz.kosu_id, cocuk, bas)
            if bas
            else _ileri_kosu(depo, cocuk, mod, kod, cocuk_ortam, [is_id])
        )
        with baglam as kosu:
            if kosu.makbuz.ayar_ozeti != cocuk["ayar_parmak_izi"]:
                raise deneme_.PilotHatasi("WF eğitim başlangıcı başka ayara bağlı.")
            r = _kayitli_sonuc(cocuk, kosu.makbuz.kosu_id, is_id, donem)
            paket = _donem_verisi(cocuk, r, kok, hazirlik)
            if paket is not None:
                r = _kayitli_donem(
                    (
                        cocuk
                        | dict(
                            yontem_ayarlari=cocuk["yontem_ayarlari"]["hucre_yontemi"]
                        ),
                        r,
                        paket,
                    )
                )
            r = _donem_yaz(kosu, r, [])
            bitis = bitir(kosu, r)
    return dict(
        deneme_id=cocuk["deneme_id"],
        kosu_id=bas["kosu_id"] if bas else kosu.makbuz.kosu_id,
        ayar_parmak_izi=cocuk["ayar_parmak_izi"],
        strateji_ayar_parmak_izi=cocuk["strateji"]["ayar_parmak_izi"],
        kayit_ref=makbuz.olay_id,
        baslangic_ref=bas["kayit_id"] if bas else kosu.makbuz.olay_id,
        sonuc_ref=r["makbuz"].olay_id,
        bitis_ref=bitis.olay_id,
        sonuc=r,
    )


def _ileri_secimler(depo, d, kosu, bolum, kok, mod, kod, ortam, semboller):
    hucreler = _arama_alani(d)
    # Bütün izinli revizyonlar doğrulanmadan hiçbir eğitim hesabı başlamaz.
    for h in hucreler:
        if h["durum"] != "alan_disi":
            h["cocuk"], h["makbuz"] = _ileri_cocuk(depo, d, kosu, bolum, h, "egitim")
    hazirlik = {}
    for h in hucreler:
        if h["durum"] != "alan_disi":
            h["egitim"] = _ileri_egitim(
                depo, kosu, h["cocuk"], h["makbuz"], kok, mod, kod, ortam, hazirlik
            )
    secimler = []
    for sembol in semboller:
        ozetler, kaynaklar = [], []
        for h in hucreler:
            o = dict(
                indeks=h["indeks"],
                deneme_id=None,
                durum="alan_disi",
                kapali_islem_sayisi=None,
                toplam_net_r=None,
            )
            if "egitim" in h:
                e = h["egitim"]
                r = e["sonuc"]
                islemler = list(_arama_islem_baglari(r).get(sembol, []))
                olcu = istatistik.olc(
                    islemler,
                    politika="bagimsiz_olcu_v1",
                    egri=istatistik.kapali_r_egrisi(islemler, r["donem"]),
                )
                n = olcu["olculer"]["islem"]["deger"]
                o.update(
                    deneme_id=e["deneme_id"],
                    durum=_arama_donem_durumu(r, n),
                    kapali_islem_sayisi=n,
                    toplam_net_r=olcu["olculer"]["net_r"]["deger"],
                )
                durum = r["durumlar"].get(sembol, {})
                pozisyon = durum.get("pozisyon")
                dislanan = (
                    []
                    if pozisyon is None
                    else [
                        dict(
                            sinyal_id=pozisyon["risk_girdisi"]["sinyal_id"],
                            durum=pozisyon["durum"],
                            neden="egitim_kesiminde_kapanmadi",
                        )
                    ]
                )
                kaynaklar.append(
                    {k: v for k, v in e.items() if k != "sonuc"}
                    | dict(
                        indeks=h["indeks"],
                        durum=o["durum"],
                        kapali_islem_sayisi=n,
                        toplam_net_r=o["toplam_net_r"],
                        dislanan=dislanan,
                        uyarilar=["egitim_120_alti"] if n < 120 else [],
                        **(
                            {
                                "dogal_bekleyis": deepcopy(
                                    r["isinma"][sembol]["dogal_bekleyis"]
                                )
                            }
                            if r["isinma"].get(sembol, {}).get("dogal_bekleyis")
                            is not None
                            else {}
                        ),
                    )
                )
            ozetler.append(o)
        bolge = saglamlik.sec(
            dict(eksenler=d["yontem_ayarlari"]["eksenler"]),
            ozetler,
            politika="genis_bolge_net_r_v1",
        )
        h = next((h for h in hucreler if h["indeks"] == bolge["secilen"]), None)
        eksik = any(
            o["durum"] not in ("alan_disi", "tamamlandi", "islemsiz") for o in ozetler
        )
        test, test_makbuz = (
            _ileri_cocuk(depo, d, kosu, bolum, h, "test") if h else (None, None)
        )
        secim = dict(
            bolum_id=bolum["ad"],
            sembol=sembol,
            egitim_donemi=bolum["egitim"],
            test_donemi={k: v for k, v in bolum.items() if k != "egitim"},
            egitim_kesimi=max(
                dt.date.fromisoformat(t)
                for t in d["veri_ayarlari"]["takvim"]["seanslar"]
                if bolum["egitim"]["baslangic"].isoformat()
                <= t
                <= bolum["egitim"]["bitis"].isoformat()
            ),
            secim_zamani_simule=bolum["egitim"]["bitis"],
            egitim_cocuklari=kaynaklar,
            bolge=bolge,
            durum="secildi" if h else "eksik" if eksik else "secim_yok",
            neden=None if h else "egitim_eksik" if eksik else bolge["neden"],
            test_deneme_id=test["deneme_id"] if test else None,
            test_kayit_ref=test_makbuz.olay_id if test_makbuz else None,
            strateji_ayar_parmak_izi=test["strateji"]["ayar_parmak_izi"]
            if test
            else None,
            deneme_ayar_parmak_izi=test["ayar_parmak_izi"] if test else None,
        )
        makbuz = kosu.ileri_secim_kaydet(kayit=secim)
        _ileri_makbuz(depo, kosu, makbuz, "ileri_secim")
        secimler.append(secim | dict(secim_ref=makbuz.olay_id))
    return secimler


def _ileri_makbuz(depo, kosu, makbuz, tur):
    o = deneme_._bul(depo.oku(), makbuz.olay_id, tur)
    if (o["deneme_id"], o["kosu_id"], o["ayar_parmak_izi"]) != (
        kosu.makbuz.deneme_id,
        kosu.makbuz.kosu_id,
        kosu.makbuz.ayar_ozeti,
    ):
        raise deneme_.PilotHatasi("WF makbuzunun koşu veya ayar bağı uyuşmuyor.")
    return o


def _ileri_yurutme(d, kosu_id, sembol):
    v, s = d["veri_ayarlari"], d["strateji"]
    return dict(
        surum="bagimsiz_islem_v1",
        aile=simulator.AILE,
        strateji_id=s["kayit_id"],
        strateji_surumu=s["katalog_surumu"],
        deneme_id=d["deneme_id"],
        kosu_id=kosu_id,
        veri_ref_id=f"{v['veri_referanslari'][0]}/veri/{v['kalite_surumu']}",
        sembol=sembol,
        nominal_tutar=float(d["risk_ayarlari"]["nominal_tutar"]),
        risk_surumu=d["risk_ayarlari"]["risk_surumu"],
        masraf_surumu=d["masraf_ayarlari"]["masraf_surumu"],
        fiyat_politikasi="aof_v1",
        **{
            k: d["yontem_ayarlari"]["hucre_yontemi"][k]
            for k in ("kilit_politikasi",)
            if k in d["yontem_ayarlari"]["hucre_yontemi"]
        },
        strateji_ayar_parmak_izi=s["ayar_parmak_izi"],
        deneme_ayar_parmak_izi=d["ayar_parmak_izi"],
    )


def _ileri_tasinanlar(durumlar):
    return {
        s
        for s, d in durumlar.items()
        if d["pozisyon"] is not None or d["karantina_kalan"]
    }


def _ileri_test_paketi(d, r, kok, durumlar):
    kapsam = _donem_uyeligi(d, r)
    gunler, uyelik, semboller, bas, son = kapsam
    tasinanlar = _ileri_tasinanlar(durumlar)
    semboller = sorted(set(semboller) | tasinanlar)
    paket = _donem_paketi(d, r, kok, None, (gunler, uyelik, semboller, bas, son))
    satirlar = {(p["sembol"], p["tarih"]): p for p in paket["piyasa"]}
    eksik = [
        (s, t)
        for s in tasinanlar
        for t in gunler
        if (s, t) not in satirlar or "eksik" in satirlar[s, t]["kalite_bayraklari"]
    ]
    if eksik:
        raise ValueError(f"Taşınan sembolün fiyat kapsamı eksik: {eksik}")
    return paket


def _ileri_test_sembolu(
    depo,
    d,
    kosu,
    r,
    paket,
    sembol,
    secim,
    onceki,
    uyelik,
    *,
    mc_plan_ref=None,
    mc_cocuk_id=None,
    mc_hucre_yontemi=None,
):
    # TASARIM 5.15 S13: MC iki değişmez bağı ortak E2/E3 hesabından önce doğrular.
    mc = mc_plan_ref is not None or mc_cocuk_id is not None
    secilen = (
        _mc_test_bagi(depo, d, kosu, secim, mc_plan_ref, mc_cocuk_id)
        if mc
        else (
            depo.deneme_oku(secim["test_deneme_id"])
            if secim and secim["test_deneme_id"]
            else None
        )
    )
    if mc and any(
        paket[alan].get("pay_kimligi") != d["veri_ayarlari"].get("pay_kimligi")
        for alan in ("referans", "uyelik")
    ):
        raise deneme_.PilotHatasi("MC E2 veri/üyelik pay kimliği kayıtla uyuşmuyor.")
    yurutme_d = d
    if d["yontem_ayarlari"].get("yontem") == MC_SURUM:
        hucre = _kayitli_hucre_yontemi(mc_hucre_yontemi)
        _isinma_secimi_dogrula(d["veri_ayarlari"], hucre)
        if secilen and deneme_.kanonik(secilen["yontem_ayarlari"]["hucre_yontemi"]) != (
            deneme_.kanonik(hucre)
        ):
            raise deneme_.PilotHatasi(
                "MC E2 hücre yöntemi donmuş stres çocuğuyla uyuşmuyor."
            )
        # TASARIM 5.15 S13: kayıtlı MC üstü değişmez; yalnız ortak yürütme bağlamı.
        yurutme_d = d | dict(yontem_ayarlari=dict(hucre_yontemi=hucre))
    elif mc_hucre_yontemi is not None:
        raise deneme_.PilotHatasi(
            "MC hücre yöntemi yalnız MC yeniden sınamasında kullanılır."
        )
    s = (secilen or d)["strateji"]
    strateji = katalog.legacy_coz(
        s["varyant"],
        s["katalog_surumu"],
        sayisal_ayarlar={
            a["ad"]: a["deger"]
            for a in s["parametreler"]
            if a["koken"] == "legacy_izgara"
        },
    )
    p = aileler_.Parametre(**{a.ad: a.deger for a in strateji.parametreler})
    hesap = aileler_.ortak_donem_kurulumu(paket | dict(semboller=[sembol]), strateji)[
        sembol
    ]
    eski_sinyaller = {
        o["sinyal"]["kaynak_sinyal"]["kayit_id"]: o["sinyal"]
        for o in kosu._tekrar_adaylari
        if not mc
        and o["kayit_turu"] == "ileri_sinyal"
        and secim is not None
        and o["secim_ref"] == secim["secim_ref"]
    }
    for sinyal in hesap["sinyaller"]:
        eski = eski_sinyaller.get(sinyal["kayit_id"])
        if eski is not None:
            sinyal["olusturma_zamani"] = eski["kaynak_sinyal"]["olusturma_zamani"]
            if deneme_.kanonik(sinyal) != deneme_.kanonik(eski["kaynak_sinyal"]):
                raise deneme_.PilotHatasi(
                    "WF eski E2 sinyali yeniden hesapla uyuşmuyor."
                )
    m = _s10_mumlar(
        paket,
        sembol,
        hesap,
        kilit_politikasi=yurutme_d["yontem_ayarlari"]["hucre_yontemi"].get(
            "kilit_politikasi"
        ),
    )
    bas, son = r["donem"]["baslangic"].isoformat(), r["donem"]["bitis"].isoformat()
    gunler = [t for t in paket["gunler"] if bas <= t <= son]
    isinma = _isinma_kaydet(d, r, paket, sembol, hesap, gunler[0], p.isinma)
    kurulum_secimi = _aile_kurulum_secimi(hesap, sembol)
    sinyaller, kabuller, kabul_gunleri = {}, [], {}
    engeller = {
        x["tarih"]: x["kalite_bayraklari"]
        for x in paket["piyasa"]
        if x["sembol"] == sembol
    }
    tum_gunler = d["veri_ayarlari"]["takvim"]["seanslar"]
    sonraki = dict(zip(tum_gunler, tum_gunler[1:], strict=False))
    if secilen and isinma >= p.isinma:
        for sinyal in hesap["sinyaller"]:
            t = sinyal["tarih"]
            neden = _sinyal_uygunlugu(sembol, t, uyelik["gunler"], sonraki, engeller, m)
            r["adaylar"].append(sinyal | dict(yurutme_nedeni=neden))
            if neden is None and sinyal["kayit_id"] in kurulum_secimi:
                kabul = dict(
                    sembol=sembol,
                    tarih=t,
                    kaynak_sinyal=sinyal,
                    parametreler=motor._duz(asdict(p)),
                    veri_ref=paket["referans"],
                )
                eski = eski_sinyaller.get(sinyal["kayit_id"])
                if eski is not None:
                    referans = deepcopy(kabul["veri_ref"])
                    for alan in ("olusturma_zamani", "kaynaklar"):
                        if (alan in referans) != (alan in eski["veri_ref"]):
                            raise deneme_.PilotHatasi(
                                "WF eski E1 kaynak alanı değişmiş."
                            )
                    if "olusturma_zamani" in referans:
                        referans["olusturma_zamani"] = eski["veri_ref"][
                            "olusturma_zamani"
                        ]
                    if "kaynaklar" in referans:
                        if len(referans["kaynaklar"]) != len(
                            eski["veri_ref"]["kaynaklar"]
                        ):
                            raise deneme_.PilotHatasi(
                                "WF eski E1 kaynak sayısı değişmiş."
                            )
                        for yeni_kaynak, eski_kaynak in zip(
                            referans["kaynaklar"],
                            eski["veri_ref"]["kaynaklar"],
                            strict=True,
                        ):
                            if (
                                yeni_kaynak.get("tur") == "yerel_goruntu"
                                and eski_kaynak.get("tur") == "yerel_goruntu"
                            ):
                                yeni_kaynak["tarih"] = eski_kaynak["tarih"]
                    if deneme_.kanonik(referans) != deneme_.kanonik(eski["veri_ref"]):
                        raise deneme_.PilotHatasi(
                            "WF eski E1 kaynağı yeniden hesapla uyuşmuyor."
                        )
                    kabul["veri_ref"] = eski["veri_ref"]
                kabul_gunleri[t] = kabul
                if mc:
                    kabuller.append(kabul)
                else:
                    makbuz = kosu.ileri_sinyal_kaydet(
                        secim_ref=secim["secim_ref"], sinyal=kabul
                    )
                    _ileri_makbuz(depo, kosu, makbuz, "ileri_sinyal")
                    sinyaller[pd.Timestamp(t)] = makbuz.olay_id
    if mc:
        sinyaller = _mc_sinyalleri(depo, kosu, secim, secilen, mc_plan_ref, kabuller)
    durum = saglamlik.ema_hucre_calistir(
        m.loc[bas:son],
        p,
        kurulum=_kabul_kurulumu(
            hesap,
            kurulum_secimi,
            {k["kaynak_sinyal"]["kayit_id"] for k in kabul_gunleri.values()},
        ),
        kurulum_kanitlari=motor.hedef_yoklugu_kanitlari(
            {
                kimlik: kabul_gunleri[t.date().isoformat()]
                for t, kimlik in sinyaller.items()
            }
        ),
        sinyal_konumlari=sinyaller,
        yurutme=_ileri_yurutme(yurutme_d, kosu.makbuz.kosu_id, sembol),
        onceki_durum=onceki,
    )
    for ret in durum["retler"]:
        if bas <= ret["tarih"] <= son:
            asama = _eksik_islem_girdisi(ret, m)
            if asama:
                _kayitli_hata(r, asama, ret["neden"], sembol=sembol, tarih=ret["tarih"])
    return durum


def _ileri_ufuk(d):
    return dict(
        ad="birlesik",
        baslangic=dt.date(2022, 1, 1),
        bitis=dt.date(2025, 12, 31),
        isinma_baslangici=d["donemler"][0]["isinma_baslangici"],
        sinir_surumu="surekli_ileri_v1",
    )


def _ileri_kohort(tarih):
    return f"{tarih[:4]}Q{(int(tarih[5:7]) - 1) // 3 + 1}"


def _ileri_islemleri_yaz(kosu, d, durumlar, yayimlanan, *, son=False):
    yeni = []
    for sembol, durum in sorted(durumlar.items()):
        islemler = list(durum["islemler"])
        if son and durum["pozisyon"] and durum["pozisyon"]["durum"] == "acik":
            islemler.append(
                dict(
                    pozisyon=durum["pozisyon"],
                    dolumlar=durum["dolumlar"],
                    sonuc=durum["sonuc"],
                    durum=durum["durum"],
                    degerleme=durum["degerleme"],
                )
            )
        for islem in islemler:
            kimlik = islem["pozisyon"]["risk_girdisi"]["islem_id"]
            if kimlik in yayimlanan:
                continue
            makbuz = kosu.ileri_islem_kaydet(islem=islem, ufuk=_ileri_ufuk(d))
            ref = dict(
                rol="tamamlanmis_islem"
                if islem["sonuc"]["kalan_adet"] == 0
                else "acik_ufuk",
                islem_id=kimlik,
                kayit_ref=makbuz.olay_id,
                sembol=sembol,
            )
            yayimlanan[kimlik] = ref
            yeni.append(ref)
    return yeni


def _ileri_olaylar(durumlar):
    olaylar = {}
    for sembol, d in sorted(durumlar.items()):
        dolumlar = [x for i in d["islemler"] for x in i["dolumlar"]] + d["dolumlar"]
        onceki = 0.0
        for tur, satirlar in (
            ("dolum", dolumlar),
            ("engel", d["retler"]),
            ("tani", d["iz"]),
        ):
            for satir in satirlar:
                kimlik = sha256(deneme_.kanonik([sembol, tur, satir])).hexdigest()
                olay = dict(
                    olay_id=kimlik,
                    sembol=sembol,
                    tur=tur,
                    tarih=satir["tarih"],
                    icerik=satir,
                )
                if tur == "tani":
                    olay["net_sonuc_degisim"] = satir["net_sonuc"] - onceki
                    onceki = satir["net_sonuc"]
                if kimlik in olaylar and olaylar[kimlik] != olay:
                    raise deneme_.PilotHatasi("Çelişen WF olay kimliği.")
                olaylar[kimlik] = olay
    return sorted(olaylar.values(), key=lambda x: (x["tarih"], x["olay_id"]))


def kayitli_ileri_calistir(
    depo, ileri_deneme_id, *, veri_koku, mod, devam_kosu_id=None, ilerleme=print
):
    """TASARIM 5.15 S12: seçim makbuzundan sonra tek kronolojik OOS akışı."""
    if mod not in ("gelistirme", "resmi"):
        raise deneme_.PilotHatasi("Koşu modu açıkça gelistirme veya resmi olmalıdır.")
    commit, kirli = kayit._git()
    if mod == "resmi" and kirli:
        raise kayit.KayitHatasi("Kirli ağaçta resmi koşu yapılamaz.")
    d = depo.deneme_oku(ileri_deneme_id)
    _ileri_istek(d)
    v = d["veri_ayarlari"]
    manifest = Path(veri_koku) / "ag" / v["veri_referanslari"][0] / "manifest.json"
    if sha256(manifest.read_bytes()).hexdigest() != v["manifest_ozeti"]:
        raise deneme_.PilotHatasi("WF manifest parmak izi kayıtla uyuşmuyor.")
    kod, ortam = _ileri_kimlik(commit, kirli)
    if devam_kosu_id is not None:
        baslangic = deneme_._bul(depo.oku(), devam_kosu_id, "baslangic", "kosu_id")
        if baslangic["deneme_id"] != ileri_deneme_id:
            raise deneme_.PilotHatasi("WF devam kimliği başka denemeye bağlı.")
        # TASARIM 5.15 S12: E1 manifestteki tüm görüntü baytlarını yeniden doğrular.
        veri.oku(v["veri_referanslari"][0], veri_koku)
        uyelik_kaniti = baslangic.get("uyelik_kaniti")
        if uyelik_kaniti is not None and deneme_.kanonik(
            uyelik_kaniti
        ) != deneme_.kanonik(_ileri_uyelik_kaniti(v)):
            raise deneme_.PilotHatasi("WF kaynak tabloları başlangıçla uyuşmuyor.")
        uyelik = _kayitli_uyelik(v, v["takvim"]["seanslar"])
        if uyelik["tablo_parmak_izi"] != v["uyelik_ozeti"]:
            raise deneme_.PilotHatasi("WF üyelik özeti uyuşmuyor.")
    bolumler = [
        dict(
            birimler=DONEM_BIRIMLERI,
            muhasebe_politikasi="tani_referans_v1",
            bolum_id=b["ad"],
            donem=b,
            durum="baslamadi",
            neden="onceki_bolum_baslamadi",
            secimler=[],
            kontrol_refleri=[],
            islem_refleri=[],
            sayimlar={},
            hatalar=[],
        )
        for b in d["donemler"]
    ]
    sonuc = dict(
        surum=ILERI_SURUM,
        deneme_id=ileri_deneme_id,
        kosu_id=None,
        ayar_parmak_izi=d["ayar_parmak_izi"],
        bolumler=bolumler,
        islemler=[],
        durum="baslamadi",
        veri_gorulme_durumu="incelenmis_gecmis",
        baslangic_makbuzu=None,
        sonuc_makbuzu=None,
        bitis_makbuzu=None,
    )
    durumlar, kontroller, yayimlanan = {}, {}, {}
    isler = [b["bolum_id"] for b in bolumler] + ["birlesik"]
    try:
        baglam = (
            depo.ileri_devam(
                devam_kosu_id,
                mod=mod,
                kod_kimligi=kod,
                ortam=ortam,
                bagimlilik_ozeti=ortam["lock_sha256"],
            )
            if devam_kosu_id is not None
            else _ileri_kosu(depo, d, mod, kod, ortam, isler)
        )
        with baglam as kosu:
            sonuc.update(kosu_id=kosu.makbuz.kosu_id, baslangic_makbuzu=kosu.makbuz)
            if ilerleme:
                for uyari in kosu.makbuz.uyarilar:
                    ilerleme(f"WF kayıt uyarısı: {uyari}")
            if kosu.makbuz.ayar_ozeti != d["ayar_parmak_izi"]:
                raise deneme_.PilotHatasi("WF üst başlangıç makbuzu başka ayara bağlı.")
            kosu.ileri_dayaniklastir(kosu.makbuz)
            if ilerleme:
                ilerleme(
                    f"WF koşu {kosu.makbuz.kosu_id} PID {os.getpid()} "
                    f"UTC {dt.datetime.now(dt.UTC).isoformat()} "
                    f"dayanıklı makbuz {kosu.makbuz.olay_id}"
                )
            uyelik = _kayitli_uyelik(v, v["takvim"]["seanslar"])
            if uyelik["tablo_parmak_izi"] != v["uyelik_ozeti"]:
                raise deneme_.PilotHatasi("WF üyelik özeti uyuşmuyor.")
            if devam_kosu_id is not None:
                olaylar = depo.oku()
                bas = next(
                    i
                    for i, o in enumerate(olaylar)
                    if o["kayit_id"] == kosu.makbuz.olay_id
                )
                kok_olaylar = [
                    o for o in olaylar[bas + 1 :] if o.get("kosu_id") == devam_kosu_id
                ]
                bolum_kayitlari = [
                    o
                    for o in kok_olaylar
                    if o["kayit_turu"] == "sonuc"
                    and o.get("sonuc_turu") == "ileri_v1"
                    and o["kayit"]["tur"] == "bolum"
                ]
                if [o["bolum_id"] for o in bolum_kayitlari] != [
                    b["bolum_id"] for b in bolumler[: len(bolum_kayitlari)]
                ] or any(o["kayit"]["durum"] != "tamamlandi" for o in bolum_kayitlari):
                    raise deneme_.PilotHatasi(
                        "Başarısız WF çeyreği veya sırasız sonuç devam ettirilemez."
                    )
                cocuklar = [
                    o
                    for o in olaylar
                    if o["kayit_turu"] == "deneme"
                    and o.get("baglar", {}).get("ileri_ust_kosu") == devam_kosu_id
                ]
                for cocuk in cocuklar:
                    ad = cocuk["yontem_ayarlari"]["bolum_id"]
                    sira = next(
                        i for i, b in enumerate(bolumler) if b["bolum_id"] == ad
                    )
                    if sira > len(bolum_kayitlari) or (
                        sira < len(bolum_kayitlari)
                        and olaylar.index(cocuk) > olaylar.index(bolum_kayitlari[sira])
                    ):
                        raise deneme_.PilotHatasi(
                            "WF çocuk revizyonu çeyrek sırasını aşıyor."
                        )
                if len(bolum_kayitlari) < 16:
                    simdi = bolumler[len(bolum_kayitlari)]["bolum_id"]
                    egitimler = [
                        o
                        for o in cocuklar
                        if o["yontem_ayarlari"]["bolum_id"] == simdi
                        and o["yontem_ayarlari"]["rol"] == "egitim"
                    ]
                    eksenler = d["yontem_ayarlari"]["eksenler"]
                    koordinatlar = [
                        tuple(
                            ex["degerler"].index(
                                next(
                                    a["deger"]
                                    for a in o["strateji"]["parametreler"]
                                    if a["ad"] == ex["ad"]
                                )
                            )
                            for ex in eksenler
                        )
                        for o in egitimler
                    ]
                    beklenen = [
                        tuple(h["indeks"])
                        for h in _arama_alani(d)
                        if h["durum"] != "alan_disi"
                    ]
                    if koordinatlar != beklenen[: len(koordinatlar)]:
                        raise deneme_.PilotHatasi(
                            "WF eğitim çocukları kayıt öneği değil."
                        )
                for b, o in zip(bolumler, bolum_kayitlari, strict=False):
                    b.update(o["kayit"])
                    b["sonuc_ref"] = o["kayit_id"]
                if bolum_kayitlari:
                    son = bolum_kayitlari[-1]
                    kosu.ileri_dayaniklastir(
                        deneme_.Makbuz(
                            son["kayit_id"],
                            ileri_deneme_id,
                            devam_kosu_id,
                            d["ayar_parmak_izi"],
                        )
                    )
                    for ref in son["kayit"]["kontrol_refleri"]:
                        o = deneme_._bul(olaylar, ref["kayit_ref"], "ileri_kontrol")
                        durumlar[ref["sembol"]] = o["durum"]
                        kontroller[ref["sembol"]] = o["kayit_id"]
                    for o in bolum_kayitlari:
                        for ref in o["kayit"]["islem_refleri"]:
                            yayimlanan[ref["islem_id"]] = ref
                son_sira = (
                    olaylar.index(bolum_kayitlari[-1]) if bolum_kayitlari else bas
                )
                devam_olaylari = [
                    o
                    for o in olaylar[son_sira + 1 :]
                    if o.get("kosu_id") == devam_kosu_id
                ]
                birlesikler = [
                    o
                    for o in devam_olaylari
                    if o["kayit_turu"] == "sonuc"
                    and o.get("sonuc_turu") == "ileri_v1"
                    and o["kayit"]["tur"] == "birlesik"
                ]
                bitisler = [o for o in devam_olaylari if o["kayit_turu"] == "bitis"]
                if (
                    len(birlesikler) > 1
                    or len(bitisler) > 1
                    or (birlesikler and len(bolum_kayitlari) != 16)
                ):
                    raise deneme_.PilotHatasi("WF birleşik sonuç veya bitiş sırasız.")
                if bitisler and not birlesikler:
                    raise deneme_.PilotHatasi("Başarısız WF bitişi devam ettirilemez.")
                if bitisler and bitisler[0]["durum"] != "tamamlandi":
                    raise deneme_.PilotHatasi("Başarısız WF bitişi devam ettirilemez.")
                if birlesikler:
                    if birlesikler[0]["kayit"]["durum"] != "tamamlandi":
                        raise deneme_.PilotHatasi(
                            "Başarısız WF birleşiği devam ettirilemez."
                        )
                    if devam_olaylari != birlesikler + bitisler:
                        raise deneme_.PilotHatasi(
                            "WF birleşik sonuç öncesi artan olay var."
                        )
                    sonuc["sonuc_makbuzu"] = deneme_.Makbuz(
                        birlesikler[0]["kayit_id"],
                        ileri_deneme_id,
                        devam_kosu_id,
                        d["ayar_parmak_izi"],
                    )
                else:
                    kosu._tekrar_adaylari = devam_olaylari
                if len(bolum_kayitlari) == 16:
                    sonuc["islemler"] = list(yayimlanan.values())
                    sonuc["durum"] = "tamamlandi"
                    if bitisler:
                        sonuc["bitis_makbuzu"] = deneme_.Makbuz(
                            bitisler[0]["kayit_id"],
                            ileri_deneme_id,
                            devam_kosu_id,
                            d["ayar_parmak_izi"],
                        )
                        return sonuc
                    if birlesikler:
                        sonuc["bitis_makbuzu"] = kosu.bitir(
                            **deneme_._ileri_bitis_kaniti(depo.oku(), d, kosu.makbuz)
                        )
                        kosu.ileri_dayaniklastir(sonuc["bitis_makbuzu"])
                        return sonuc
            for b in bolumler:
                if b["durum"] == "tamamlandi":
                    continue
                try:
                    bolum = b["donem"]
                    semboller = sorted(
                        _ileri_tasinanlar(durumlar)
                        | {
                            s
                            for t, u in uyelik["gunler"].items()
                            if bolum["egitim"]["baslangic"].isoformat()
                            <= t
                            <= bolum["bitis"].isoformat()
                            for s in u["semboller"]
                        }
                    )
                    b["secimler"] = _ileri_secimler(
                        depo, d, kosu, bolum, veri_koku, mod, kod, ortam, semboller
                    )
                    r = _kayitli_sonuc(d, kosu.makbuz.kosu_id, b["bolum_id"], bolum)
                    paket = _ileri_test_paketi(d, r, veri_koku, durumlar)
                    b.update(
                        {
                            a: r[a]
                            for a in (
                                "veri_referansi",
                                "uyelik",
                                "kalite",
                                "isinma",
                                "adaylar",
                            )
                        }
                    )
                    for sembol in paket["semboller"]:
                        secim = next(
                            (s for s in b["secimler"] if s["sembol"] == sembol), None
                        )
                        durum = _ileri_test_sembolu(
                            depo,
                            d,
                            kosu,
                            r,
                            paket,
                            sembol,
                            secim,
                            durumlar.get(sembol),
                            uyelik,
                        )
                        makbuz = kosu.ileri_kontrol_kaydet(
                            bolum_id=b["bolum_id"],
                            sembol=sembol,
                            durum=durum,
                            onceki_ref=kontroller.get(sembol),
                        )
                        kontroller[sembol] = makbuz.olay_id
                        durumlar[sembol] = durum
                        b["kontrol_refleri"].append(
                            dict(
                                rol="acik_kontrol",
                                sembol=sembol,
                                kayit_ref=makbuz.olay_id,
                            )
                        )
                        b["sayimlar"][sembol] = istatistik.ileri_kontrol_sayimi(
                            durum, bolum
                        )
                    b["islem_refleri"] = _ileri_islemleri_yaz(
                        kosu, d, durumlar, yayimlanan, son=b is bolumler[-1]
                    )
                    b["hatalar"] = r["hatalar"]
                    b["durum"] = (
                        "hata"
                        if r["hatalar"]
                        or any(s["durum"] == "eksik" for s in b["secimler"])
                        else "tamamlandi"
                    )
                    b["neden"] = r["neden"] or (
                        "egitim_eksik" if b["durum"] == "hata" else None
                    )
                    b["uyarilar"] = [
                        dict(sembol=s, neden="test_30_alti")
                        for s, n in b["sayimlar"].items()
                        if n["kapali_islem"] < 30
                    ]
                    kanit = deneme_._ileri_bolum_kaniti(
                        depo.oku(), d, kosu.makbuz, bolum
                    )
                    b.update(kanit)
                    makbuz = kosu.ileri_sonucu_kaydet(kayit=b)
                    b["sonuc_ref"] = makbuz.olay_id
                    kosu.ileri_dayaniklastir(makbuz)
                    if ilerleme:
                        ilerleme(f"{b['bolum_id']}: {b['durum']}")
                    if r["hatalar"]:
                        break
                except deneme_.PilotYazmaHatasi:
                    raise
                except deneme_.PilotHatasi:
                    raise
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    IndexError,
                    ArithmeticError,
                    OSError,
                ) as hata:
                    if deneme_._ileri_sonucsuz_cocuk_var(
                        depo.oku(), kosu.makbuz.kosu_id
                    ):
                        raise
                    b.update(durum="hata", neden=str(hata))
                    b["hatalar"].append(dict(asama="ileri", neden=str(hata)))
                    kanit = deneme_._ileri_bolum_kaniti(
                        depo.oku(), d, kosu.makbuz, bolum
                    )
                    b.update(kanit)
                    makbuz = kosu.ileri_sonucu_kaydet(kayit=b)
                    b["sonuc_ref"] = makbuz.olay_id
                    break
            sonuc["islemler"] = list(yayimlanan.values())
            tamamlanan = [b["bolum_id"] for b in bolumler if b["durum"] == "tamamlandi"]
            sonuc["durum"] = "tamamlandi" if len(tamamlanan) == 16 else "hata"
            birlesik = deneme_._ileri_birlesik_kaniti(depo.oku(), d, kosu.makbuz)
            sonuc["sonuc_makbuzu"] = kosu.ileri_sonucu_kaydet(kayit=birlesik)
            sonuc["bitis_makbuzu"] = kosu.bitir(
                **deneme_._ileri_bitis_kaniti(depo.oku(), d, kosu.makbuz)
            )
            kosu.ileri_dayaniklastir(sonuc["bitis_makbuzu"])
    except Exception as hata:
        hata.sonuc = sonuc
        raise
    return sonuc


MC_SURUM = "kayitli_monte_carlo_v1"
_MC_PARTI = 32


def _mc_istegi(d, kaynak):
    """TASARIM 5.15 S13: MC'nin kesin yöntemi legacy yüzlerini değiştirmez."""
    deneme_._mc_yontemi(d["yontem_ayarlari"])
    hucre = kaynak["deneme"]["yontem_ayarlari"]["hucre_yontemi"]
    _yurutme_ayarlari(d | dict(yontem_ayarlari=hucre))
    _isinma_secimi_dogrula(d["veri_ayarlari"], hucre)
    _kayitli_veri_ayarlari(d["veri_ayarlari"])
    _kayitli_takvim(d["veri_ayarlari"]["takvim"])
    beklenen = [
        (str(y), dt.date(y, 1, 1), dt.date(y, 12, 31)) for y in range(2022, 2026)
    ]
    beklenen.append(("birlesik", dt.date(2022, 1, 1), dt.date(2025, 12, 31)))
    if len(d["donemler"]) != len(beklenen):
        raise deneme_.PilotHatasi(
            "MC dört kapanış yılı ve birleşik OOS dilimi gerektirir."
        )
    for q, sinir in zip(d["donemler"], beklenen, strict=True):
        if (q["ad"], q["baslangic"], q["bitis"]) != sinir:
            raise deneme_.PilotHatasi("MC kapanış dilimi sırası veya sınırı geçersiz.")


def _mc_girdi(d, kaynak):
    seanslar = [
        t
        for t in kaynak["deneme"]["veri_ayarlari"]["takvim"]["seanslar"]
        if "2022-01-01" <= t <= "2025-12-31"
    ]
    semboller = sorted(
        {o["sembol"] for o in kaynak["secimler"]}
        | {o["sembol"] for o in kaynak["kontroller"]}
    )
    gunluk = [[0.0] * len(semboller) for _ in seanslar]
    refler = [[[] for _ in semboller] for _ in seanslar]
    for r in kaynak["nufus"]:
        i, j = seanslar.index(r["cikis_tarih"]), semboller.index(r["sembol"])
        gunluk[i][j] += r["net_r"]
        refler[i][j].append(r["islem_ref"])
    g = dict(
        kaynak=d["yontem_ayarlari"]["kaynak"],
        kaynak_ozeti=kaynak["icerik_ozeti"],
        nufus=kaynak["nufus"],
        acik_referanslari=kaynak["acik"],
        secim_referanslari=[o["kayit_id"] for o in kaynak["secimler"]],
        sinyal_referanslari=[o["kayit_id"] for o in kaynak["sinyaller"]],
        kontrol_referanslari=[o["kayit_id"] for o in kaynak["kontroller"]],
        seanslar=seanslar,
        semboller=semboller,
        gunluk_r=gunluk,
        gunluk_islemler=refler,
        kapsam=dict(
            baslangic="2022-01-01",
            bitis="2025-12-31",
            muhasebe_politikasi="kapali_gerceklesme_gunluk_r_v1",
        ),
    )
    g["isler"] = istatistik.mc_isleri(
        g,
        d["donemler"],
        secim_var=any(o["kayit"]["durum"] == "secildi" for o in kaynak["secimler"]),
    )
    return g


def _mc_makbuzlar(depo, kosu, makbuzlar, tur):
    olaylar = depo.oku()
    for m in makbuzlar:
        o = deneme_._bul(olaylar, m.olay_id, tur)
        if (o["kosu_id"], o["deneme_id"], o["ayar_parmak_izi"]) != (
            kosu.makbuz.kosu_id,
            m.deneme_id,
            m.ayar_ozeti,
        ):
            raise deneme_.PilotHatasi(
                "MC yeniden okunan makbuzun koşu veya ayar bağı uyuşmuyor."
            )
    return olaylar


def _mc_stres_revizyonlari(depo, kosu, komsular, secilenler, onbellek):
    eksik = []
    for q, i in zip(komsular, secilenler, strict=True):
        anahtar = (q["secim"]["kayit_id"], i)
        if anahtar in onbellek:
            continue
        taban, secim = q["taban"], q["secim"]
        sayisal = {
            a["ad"]: a["deger"]
            for a in taban["strateji"]["parametreler"]
            if a["koken"] == "legacy_izgara"
        } | q["demetler"][i]
        strateji = katalog.legacy_coz(
            taban["strateji"]["varyant"],
            taban["strateji"]["katalog_surumu"],
            sayisal_ayarlar=sayisal,
        )
        y = dict(
            yontem="mc_stres_cocuk_v1",
            tekrar=0,
            bolum_id=secim["bolum_id"],
            sembol=secim["sembol"],
            secim_ref=secim["kayit_id"],
            hucre_yontemi=taban["yontem_ayarlari"]["hucre_yontemi"],
        )
        eksik.append(
            (
                anahtar,
                dict(
                    strateji=asdict(strateji),
                    yontem_ayarlari=y,
                    **{
                        a: taban[a]
                        for a in (
                            "donemler",
                            "veri_ayarlari",
                            "risk_ayarlari",
                            "masraf_ayarlari",
                            "eski_referans",
                        )
                    },
                ),
            )
        )
    for bas in range(0, len(eksik), _MC_PARTI):
        parti = eksik[bas : bas + _MC_PARTI]
        makbuzlar = kosu.mc_stres_revizyonlari_kaydet(kayitlar=[k for _, k in parti])
        olaylar = _mc_makbuzlar(depo, kosu, makbuzlar, "deneme")
        for (anahtar, _), m in zip(parti, makbuzlar, strict=True):
            onbellek[anahtar] = deneme_._bul(
                olaylar, m.deneme_id, "deneme", "deneme_id"
            )
    cocuklar = []
    for q, i in zip(komsular, secilenler, strict=True):
        secim = q["secim"]
        c = onbellek[secim["kayit_id"], i]
        cocuklar.append(
            dict(
                bolum=secim["bolum_id"],
                sembol=secim["sembol"],
                secim_ref=secim["kayit_id"],
                deneme_id=c["deneme_id"],
                ayar_parmak_izi=c["ayar_parmak_izi"],
                strateji_ayar_parmak_izi=c["strateji"]["ayar_parmak_izi"],
                demet=q["demetler"][i],
            )
        )
    return cocuklar


def _mc_planlar(depo, kosu, d, g, girdi_ref, is_, bas, sayi, komsular, onbellek):
    dilim = is_["tanim"]["dilim"]
    gunler = [
        t
        for t in g["seanslar"]
        if dilim["baslangic"].isoformat() <= t <= dilim["bitis"].isoformat()
    ]
    n = (
        len(gunler)
        if is_["deney"] == "ortak_tarih_blok_v1"
        else len(
            [
                r
                for r in g["nufus"]
                if r["cikis_tarih"] in gunler
                and (is_["sembol"] == "eklemeli" or r["sembol"] == is_["sembol"])
            ]
        )
    )
    planlar = []
    for indeks in range(bas, bas + sayi):
        ayar = is_["deney"] == "ayar_komsulugu_v1"
        cekilis = istatistik.mc_plan(
            is_["deney"],
            is_["anahtar"],
            indeks,
            n=len(komsular) if ayar else n,
            tohum=d["yontem_ayarlari"]["tohum"],
            blok=is_["blok"],
            komsu_sayilari=[len(q["demetler"]) for q in komsular] if ayar else None,
        )
        cocuklar = (
            _mc_stres_revizyonlari(
                depo, kosu, komsular, cekilis["demet_indeksleri"], onbellek
            )
            if ayar
            else []
        )
        planlar.append(
            dict(
                girdi_ref=girdi_ref,
                anahtar=is_["anahtar"],
                indeks=indeks,
                cekilis=cekilis,
                stres_cocuklari=cocuklar,
            )
        )
    makbuzlar = kosu.mc_planlari_kaydet(kayitlar=planlar)
    _mc_makbuzlar(depo, kosu, makbuzlar, "mc_plan")
    return list(zip(planlar, makbuzlar, strict=True))


def _mc_test_bagi(depo, d, kosu, secim, plan_ref, cocuk_id):
    """TASARIM 5.15 S13: iki özel MC girdisi E2'den önce birlikte çözülür."""
    if not plan_ref or not cocuk_id:
        raise deneme_.PilotHatasi("MC planı ve stres çocuğu birlikte gereklidir.")
    olaylar = depo.oku()
    b = deneme_._bul(olaylar, kosu.makbuz.kosu_id, "baslangic", "kosu_id")
    p = deneme_._mc_ref(olaylar, plan_ref, "mc_plan", d, b)
    if secim is None:
        raise deneme_.PilotHatasi("MC stres çocuğunun donmuş seçimi yok.")
    donmus = deneme_._bul(olaylar, secim["secim_ref"], "ileri_secim")
    if deneme_.kanonik(donmus["kayit"]) != deneme_.kanonik(
        {a: v for a, v in secim.items() if a != "secim_ref"}
    ):
        raise deneme_.PilotHatasi("MC donmuş WF seçimini değiştiremez.")
    c = next(
        (
            c
            for c in p["stres_cocuklari"]
            if (c["deneme_id"], c["secim_ref"], c["bolum"], c["sembol"])
            == (cocuk_id, secim["secim_ref"], secim["bolum_id"], secim["sembol"])
        ),
        None,
    )
    if c is None:
        raise deneme_.PilotHatasi(
            "MC stres çocuğu kesinleşmiş planın seçimine bağlı değil."
        )
    cocuk = depo.deneme_oku(cocuk_id)
    if (cocuk["ayar_parmak_izi"], cocuk["strateji"]["ayar_parmak_izi"]) != (
        c["ayar_parmak_izi"],
        c["strateji_ayar_parmak_izi"],
    ):
        raise deneme_.PilotHatasi("MC stres çocuğunun iki ayar özeti uyuşmuyor.")
    return cocuk


def _mc_sinyalleri(depo, kosu, secim, secilen, plan_ref, kabuller):
    """TASARIM 5.15 S13: gerçek E2 kabulleri kesinleşmeden E3'e kimlik verilmez."""
    sinyaller = {}
    for bas in range(0, len(kabuller), _MC_PARTI):
        parti = kabuller[bas : bas + _MC_PARTI]
        kayitlar = [
            dict(
                plan_ref=plan_ref,
                secim_ref=secim["secim_ref"],
                deneme_id=secilen["deneme_id"],
                bolum=secim["bolum_id"],
                sembol=k["sembol"],
                tarih=k["tarih"],
                sinyal=k,
            )
            for k in parti
        ]
        makbuzlar = kosu.mc_sinyalleri_kaydet(kayitlar=kayitlar)
        _mc_makbuzlar(depo, kosu, makbuzlar, "mc_sinyal")
        for k, m in zip(parti, makbuzlar, strict=True):
            sinyaller[pd.Timestamp(k["tarih"])] = m.olay_id
    return sinyaller


def _mc_bolum_durumunu_sakla(durum, nihai):
    """TASARIM 5.15 S13/#178: her gerçek ara geçmiş, yayın öncesi nihai öneğe eşittir."""
    uzunluklar = {}
    for alan in ("iz", "islemler", "retler"):
        uzunluklar[alan] = len(durum[alan])
        if deneme_.kanonik(durum[alan]) != deneme_.kanonik(
            nihai[alan][: uzunluklar[alan]]
        ):
            raise deneme_.PilotHatasi(
                "MC bölüm geçmişi nihai durumun kanonik öneği değil."
            )
    return dict(
        durum={a: deepcopy(x) for a, x in durum.items() if a not in uzunluklar},
        gecmis_onekleri=uzunluklar,
    )


def _mc_ayar_yeniden_sina(depo, d, kosu, kaynak, plan, plan_ref, kok):
    """TASARIM 5.15 S13: donmuş seçimlerle aynı WF E1/E2/E3 yolu, tek taşıma."""
    olaylar = depo.oku()
    kayitli = deneme_._bul(olaylar, plan_ref, "mc_plan")
    b = deneme_._bul(olaylar, kosu.makbuz.kosu_id, "baslangic", "kosu_id")
    deneme_._mc_ayni_kosu(kayitli, d, b)
    if deneme_.kanonik(kayitli["kayit"]) != deneme_.kanonik(plan):
        raise deneme_.PilotHatasi("MC yeniden sınama kesinleşmiş planı kullanmalıdır.")
    g = deneme_._mc_ref(olaylar, plan["girdi_ref"], "mc_girdi", d, b)
    if (
        g["kaynak"] != d["yontem_ayarlari"]["kaynak"]
        or kaynak["icerik_ozeti"] != g["kaynak_ozeti"]
    ):
        raise deneme_.PilotHatasi("MC yeniden sınama başka WF kaynağına bağlı.")
    v = d["veri_ayarlari"]
    sakli = (
        dict(uyelik_kaniti=kaynak["baslangic"]["uyelik_kaniti"])
        if v.get("ilk_islem") is not None
        else {}
    )
    uyelik = _kayitli_uyelik(v, v["takvim"]["seanslar"], **sakli)
    secimler = {
        (o["bolum_id"], o["sembol"]): o["kayit"] | dict(secim_ref=o["kayit_id"])
        for o in kaynak["secimler"]
    }
    cocuklar = {(c["bolum"], c["sembol"]): c for c in plan["stres_cocuklari"]}
    hucre = kaynak["deneme"]["yontem_ayarlari"]["hucre_yontemi"]
    durumlar, bolumler = {}, []
    for bolum in kaynak["deneme"]["donemler"]:
        r = _kayitli_sonuc(d, kosu.makbuz.kosu_id, bolum["ad"], bolum)
        paket = _ileri_test_paketi(d, r, kok, durumlar)
        for sembol in paket["semboller"]:
            secim = secimler.get((bolum["ad"], sembol))
            ayar = {}
            if secim and secim["durum"] == "secildi":
                c = cocuklar[bolum["ad"], sembol]
                ayar = dict(mc_plan_ref=plan_ref, mc_cocuk_id=c["deneme_id"])
            durumlar[sembol] = _ileri_test_sembolu(
                depo,
                d,
                kosu,
                r,
                paket,
                sembol,
                secim,
                durumlar.get(sembol),
                uyelik,
                mc_hucre_yontemi=hucre,
                **ayar,
            )
        if r["hatalar"]:
            raise ValueError(f"{bolum['ad']}: {r['neden']}")
        kanit = {}
        if v.get("ilk_islem") is not None:
            kanit = dict(
                donem=bolum,
                veri_referansi=r["veri_referansi"],
                isinma=r["isinma"],
                durumlar={s: deepcopy(durumlar[s]) for s in paket["semboller"]},
            )
        bolumler.append(
            dict(bolum=bolum["ad"], durum="tamamlandi", hatalar=[], **kanit)
        )
    if v.get("ilk_islem") is not None:
        for bolum in bolumler:
            bolum["durumlar"] = {
                s: _mc_bolum_durumunu_sakla(durum, durumlar[s])
                for s, durum in bolum["durumlar"].items()
            }
    refler = [
        o["kayit_id"]
        for o in depo.oku()
        if o["kayit_turu"] == "mc_sinyal"
        and o["kosu_id"] == b["kosu_id"]
        and o["kayit"]["plan_ref"] == plan_ref
    ]
    return dict(durumlar=durumlar, bolumler=bolumler), refler


def _mc_is_ozeti(is_, butce, sonuclar, kontroller, *, hata=None):
    n = sum(s["kayit"]["durum"] == "tamamlandi" for s in sonuclar)
    h = int(hata is not None)
    durma = bool(
        kontroller
        and kontroller[-1]["kayit"]["tani"]["durum"] == "sayisal_kararlilik_gozlendi"
    )
    durum = (
        "olculemedi"
        if is_["durum"] == "olculemedi"
        else "eksik"
        if h or (n < butce and not durma)
        else "on_gosterim"
        if butce == 1000
        else "sayisal_kararlilik_gozlendi"
        if durma
        else "sinirda_kararsiz"
    )
    return dict(
        anahtar=is_["anahtar"],
        durum=durum,
        neden=is_["neden"]
        if durum == "olculemedi"
        else str(hata)
        if h
        else "tamamlanmamis_butce"
        if durum == "eksik"
        else None,
        istenen=butce,
        denenen=n + h,
        tamamlanan=n,
        hatali=h,
        baslamayan=0 if durma else butce - n - h,
        durma_nedeniyle_istenmedi=butce - n if durma else 0,
        basarisiz_indeks=n if h else None,
        sonuc_referanslari=[s["kayit_id"] for s in sonuclar],
        kontrol_referanslari=[s["kayit_id"] for s in kontroller],
    )


def _mc_isi_yurut(depo, kosu, d, kaynak, g, girdi_ref, is_, kok, komsular, onbellek):
    butce = d["yontem_ayarlari"]["tekrar"]
    sonuclar, kontroller = [], []
    if is_["durum"] == "olculemedi":
        return _mc_is_ozeti(is_, butce, sonuclar, kontroller)
    for nokta in d["yontem_ayarlari"]["kontrol_noktalari"]:
        while len(sonuclar) < nokta:
            sayi = min(_MC_PARTI, nokta - len(sonuclar))
            planlar = _mc_planlar(
                depo,
                kosu,
                d,
                g,
                girdi_ref,
                is_,
                len(sonuclar),
                sayi,
                komsular,
                onbellek,
            )
            parti, hata = [], None
            for p, makbuz in planlar:
                kayit = dict(
                    plan_ref=makbuz.olay_id,
                    durum="tamamlandi",
                    olculer={},
                    sembol_olculeri={},
                    yeniden_sinama={},
                    sonuc_referanslari=[],
                    asama=None,
                    neden=None,
                )
                try:
                    if is_["deney"] == "ayar_komsulugu_v1":
                        tekrar, refler = _mc_ayar_yeniden_sina(
                            depo, d, kosu, kaynak, p, makbuz.olay_id, kok
                        )
                        kayit.update(yeniden_sinama=tekrar, sonuc_referanslari=refler)
                    kayit.update(
                        istatistik.mc_senaryo_olculeri(
                            g,
                            is_,
                            p["cekilis"],
                            durumlar=kayit["yeniden_sinama"].get("durumlar"),
                        )
                    )
                except deneme_.PilotYazmaHatasi:
                    raise
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    IndexError,
                    ArithmeticError,
                    OSError,
                ) as yakalanan:
                    hata = yakalanan
                    kayit.update(
                        durum="hata",
                        asama="yeniden_sinama"
                        if is_["deney"] == "ayar_komsulugu_v1"
                        else "olcum",
                        neden=str(hata),
                        olculer={},
                        sembol_olculeri={},
                        yeniden_sinama={},
                        sonuc_referanslari=[],
                    )
                parti.append(kayit)
                if hata or is_["deney"] == "ayar_komsulugu_v1":
                    makbuzlar = kosu.mc_sonuclari_kaydet(kayitlar=parti)
                    olaylar = _mc_makbuzlar(depo, kosu, makbuzlar, "mc_senaryo")
                    sonuclar.extend(
                        deneme_._bul(olaylar, m.olay_id, "mc_senaryo")
                        for m in makbuzlar
                    )
                    parti = []
                if hata:
                    return _mc_is_ozeti(is_, butce, sonuclar, kontroller, hata=hata)
            if parti:
                makbuzlar = kosu.mc_sonuclari_kaydet(kayitlar=parti)
                olaylar = _mc_makbuzlar(depo, kosu, makbuzlar, "mc_senaryo")
                sonuclar.extend(
                    deneme_._bul(olaylar, m.olay_id, "mc_senaryo") for m in makbuzlar
                )
        tani = istatistik.mc_kontrol(
            [o["kayit"]["olculer"] for o in sonuclar],
            onceki=kontroller[-1]["kayit"]["tani"] if kontroller else None,
        )
        kayit = dict(
            girdi_ref=girdi_ref,
            anahtar=is_["anahtar"],
            onceki_ref=kontroller[-1]["kayit_id"] if kontroller else None,
            sonuc_referanslari=[o["kayit_id"] for o in sonuclar],
            tani=tani,
        )
        makbuz = kosu.mc_kontrol_kaydet(kayit=kayit)
        olaylar = _mc_makbuzlar(depo, kosu, [makbuz], "mc_kontrol")
        kontroller.append(deneme_._bul(olaylar, makbuz.olay_id, "mc_kontrol"))
        if tani["durum"] == "sayisal_kararlilik_gozlendi":
            break
    return _mc_is_ozeti(is_, butce, sonuclar, kontroller)


def kayitli_monte_carlo_calistir(depo, mc_deneme_id, *, veri_koku, mod, ilerleme=print):
    """TASARIM 5.15 S13: gerçek WF kaynağından beş ayrı koşullu tanı."""
    if mod not in ("gelistirme", "resmi"):
        raise deneme_.PilotHatasi("Koşu modu açıkça gelistirme veya resmi olmalıdır.")
    commit, kirli = kayit._git()
    if mod == "resmi" and kirli:
        raise kayit.KayitHatasi("Kirli ağaçta resmi koşu yapılamaz.")
    d = depo.deneme_oku(mc_deneme_id)
    kaynak = deneme_._mc_kaynagi(depo.oku(), d["yontem_ayarlari"]["kaynak"])
    _mc_istegi(d, kaynak)
    v = d["veri_ayarlari"]
    manifest = Path(veri_koku) / "ag" / v["veri_referanslari"][0] / "manifest.json"
    if sha256(manifest.read_bytes()).hexdigest() != v["manifest_ozeti"]:
        raise deneme_.PilotHatasi("MC manifest parmak izi kayıtla uyuşmuyor.")
    g = _mc_girdi(d, kaynak)
    kod, ortam = _kayitli_kimlik(commit, kirli, 1)
    kod = kod.replace(KAYITLI_SURUM, MC_SURUM, 1)
    ortam.update(
        isci_politikasi=dict(yontem="seri", isci=1),
        numpy_surumu=np.__version__,
        numpy_derleme=np.__config__.show(mode="dicts"),
    )
    sonuc = dict(
        surum=MC_SURUM,
        deneme_id=mc_deneme_id,
        kosu_id=None,
        ayar_parmak_izi=d["ayar_parmak_izi"],
        durum="baslamadi",
        yontem_tamamlandi=False,
        calisma_turu=d["yontem_ayarlari"]["calisma_turu"],
        birimler=dict(toplam="R", dusus="R"),
        yorum="Kapalı işlem nüfusuna koşullu tanı. Gelecek kâr veya hesap güvenliği garantisi değildir.",
        isler=[],
        baslangic_makbuzu=None,
        girdi_makbuzu=None,
        sonuc_makbuzu=None,
        bitis_makbuzu=None,
    )
    try:
        with depo.kosu(
            mc_deneme_id,
            mod=mod,
            anlik_goruntu=v["veri_referanslari"][0],
            manifest_ozeti=v["manifest_ozeti"],
            uyelik_surumu=v["uyelik_surumu"],
            kod_kimligi=kod,
            ortam=ortam,
            bagimlilik_ozeti=ortam["lock_sha256"],
            tohum=d["yontem_ayarlari"]["tohum"],
            ureteci_surumu=d["yontem_ayarlari"]["uretec"],
            is_listesi=[i["anahtar"] for i in g["isler"]],
        ) as kosu:
            sonuc.update(kosu_id=kosu.makbuz.kosu_id, baslangic_makbuzu=kosu.makbuz)
            if kosu.makbuz.ayar_ozeti != d["ayar_parmak_izi"]:
                raise deneme_.PilotHatasi(
                    "MC başlangıcı kayıtlı tam ayara bağlı değil."
                )
            _mc_makbuzlar(depo, kosu, [kosu.makbuz], "baslangic")
            makbuz = kosu.mc_girdi_kaydet(kayit=g)
            sonuc["girdi_makbuzu"] = makbuz
            olaylar = _mc_makbuzlar(depo, kosu, [makbuz], "mc_girdi")
            komsular = deneme_._mc_komsular(olaylar, g)
            onbellek = {}
            for is_ in g["isler"]:
                s = _mc_isi_yurut(
                    depo,
                    kosu,
                    d,
                    kaynak,
                    g,
                    makbuz.olay_id,
                    is_,
                    veri_koku,
                    komsular,
                    onbellek,
                )
                sonuc["isler"].append(s)
                if ilerleme:
                    ilerleme(
                        f"{is_['deney']} {is_['dilim']} {is_['sembol']}: {s['durum']}"
                    )
            ozet = kosu.mc_ozet_kaydet(
                kayit=dict(
                    girdi_ref=makbuz.olay_id,
                    isler=sonuc["isler"],
                    uyarilar=[sonuc["yorum"]],
                )
            )
            _mc_makbuzlar(depo, kosu, [ozet], "mc_ozet")
            sonuc["sonuc_makbuzu"] = ozet
            tamamlanan = [
                i["anahtar"]
                for i in sonuc["isler"]
                if i["durum"]
                in ("on_gosterim", "sayisal_kararlilik_gozlendi", "sinirda_kararsiz")
            ]
            basarisiz = [
                i["anahtar"] for i in sonuc["isler"] if i["anahtar"] not in tamamlanan
            ]
            sonuc["yontem_tamamlandi"] = (
                not basarisiz and d["yontem_ayarlari"]["calisma_turu"] == "nihai"
            )
            sonuc["durum"] = (
                "eksik"
                if basarisiz
                else "tamamlandi"
                if sonuc["yontem_tamamlandi"]
                else "on_gosterim"
            )
            sonuc["bitis_makbuzu"] = kosu.bitir(
                durum="hata" if basarisiz else "tamamlandi",
                tamamlanan=tamamlanan,
                basarisiz=basarisiz,
                yontemler=[MC_SURUM, d["yontem_ayarlari"]["calisma_turu"]],
                olculer={},
                cikti_referanslari=[ozet.olay_id],
                ozetler=dict(
                    yontem_tamamlandi=sonuc["yontem_tamamlandi"],
                    calisma_turu=sonuc["calisma_turu"],
                ),
            )
    except Exception as hata:
        hata.sonuc = sonuc
        raise
    return sonuc
