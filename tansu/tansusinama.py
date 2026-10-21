"""Tansu sınaması (TASARIM 5.14): Tansu'nun kendi sınama yöntemi.

Her hisse (çift ailesinde her çift) kendi ızgarasıyla, bütün dönemde, masraf %0,10 ile koşulur. Sağlam bölge seçilir,
sonuç al-tut ve Tansu'nun tablo ölçüleriyle yan yana verilir. Kabul kararına girmez (5.12), kart üretmez, m'yi artırmaz
(5.11). Hash dışıdır (`kayit.HASH_DISI`). İş birimi bir hisse ya da bir çifttir; sonuç işçi sayısından bağımsızdır.
"""

import concurrent.futures
from collections import Counter
import datetime as dt
import itertools
import json
import logging
import multiprocessing
import os
import shutil
import subprocess
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


def _grup_uyeligi(tanim, engeller):
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
        return [
            dict(sembol=s, tarih=t, neden="bist30_uyesi_degil")
            for t, gun in uyelik["gunler"].items()
            for s in semboller
            if s not in gun["semboller"]
        ]
    except (OSError, veri.VeriHatasi, ValueError) as hata:
        engeller.append(dict(alan="hisse_kurali.uyelik", neden=str(hata)))
        return []


def _grup_veri_kapsami(tanim, anlik, takvim, engeller):
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
    for sembol in tanim.get("hisse_kurali", {}).get("semboller", []):
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
    dislamalar = _grup_uyeligi(tanim, engeller)
    _grup_veri_kapsami(tanim, anlik, takvim, engeller)
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
    _kayitli_donemler(deneme["donemler"])
    _kayitli_takvim(deneme["veri_ayarlari"].get("takvim", {}))


def _yurutme_ayarlari(deneme):
    if deneme["yontem_ayarlari"] != KAYITLI_YONTEM:
        raise deneme_.PilotHatasi("Desteklenmeyen yürütme ayarı.")
    if deneme["masraf_ayarlari"] != {"masraf_surumu": islem_riski.MASRAF_SURUMU}:
        raise deneme_.PilotHatasi("Desteklenmeyen masraf ayarı.")
    if deneme["strateji"]["aile"] != katalog.AILE:
        raise deneme_.PilotHatasi("Desteklenmeyen aile; çift için risk_dayanagi_eksik.")
    _kayitli_risk(deneme["risk_ayarlari"])


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


def _donem_uyeligi(deneme, sonuc):
    v, d = deneme["veri_ayarlari"], sonuc["donem"]
    bas, son = d["baslangic"].isoformat(), d["bitis"].isoformat()
    gunler = [t for t in v["takvim"]["seanslar"] if bas <= t <= son]
    uyelik = veri.uyelik_hazirla(
        veri.UyelikIstegi(tuple(gunler), v["evren_politikasi"], v["uyelik_surumu"])
    )
    if uyelik["tablo_parmak_izi"] != v["uyelik_ozeti"]:
        raise ValueError("Üyelik parmak izi kayıtlı denemeyle uyuşmuyor.")
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
    )


def _donem_paketi(deneme, sonuc, veri_koku, hazirlik, kapsam):
    gunler, uyelik, semboller, bas, son = kapsam
    v, d = deneme["veri_ayarlari"], sonuc["donem"]
    istek = _donem_veri_istegi(v, d, semboller, bas, son)
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
    ):
        raise ValueError("E1 veri/üyelik referansı kayıtlı denemeyle uyuşmuyor.")
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


def _s10_mumlar(paket, sembol, hesap):
    m = hesap["mumlar"].copy()
    m["onceki_rsi"] = m["rsi"].ffill().shift(1)
    m["onceki_dusuk"] = m["dusuk"].ffill().shift(1)
    satirlar = [r for r in paket["piyasa"] if r["sembol"] == sembol]
    for alan in ("ham_yuksek", "ham_dusuk", "tavan", "taban", "limit_kaniti"):
        m[alan] = [
            r.get(alan, {}).get("deger")
            if isinstance(r.get(alan, {}), dict)
            else r.get(alan)
            for r in satirlar
        ]
    m["islem"] = [r["islem"] for r in satirlar]
    m["karantina"] = ["karantina" in r["kalite_bayraklari"] for r in satirlar]
    return m


def _donem_sembolu(deneme, sonuc, paket, sembol, hesap, strateji, p):
    d = sonuc["donem"]
    bas, son = d["baslangic"].isoformat(), d["bitis"].isoformat()
    gunler = [t for t in paket["gunler"] if bas <= t <= son]
    uyelik = sonuc["uyelik"]["gunler"]
    ilk_uye = next(t for t in gunler if sembol in uyelik[t]["semboller"])
    isinma = int(hesap["isinma"].at[pd.Timestamp(ilk_uye)])
    sonuc["isinma"][sembol] = dict(
        gozlem=isinma, gerekli=p.isinma, tamam=isinma >= p.isinma
    )
    if isinma < p.isinma:
        _kayitli_hata(
            sonuc,
            "isinma",
            f"{sembol}: {isinma}/{p.isinma} gözlem",
            sembol=sembol,
            tarih=ilk_uye,
        )
    m = _s10_mumlar(paket, sembol, hesap)
    sinyaller = _donem_sinyalleri(deneme, sonuc, paket, sembol, hesap, m, gunler)
    yurutme = dict(
        surum="bagimsiz_islem_v1",
        aile=simulator.AILE,
        strateji_id=strateji.kayit_id,
        strateji_surumu=strateji.katalog_surumu,
        deneme_id=deneme["deneme_id"],
        kosu_id=sonuc["kosu_id"],
        veri_ref_id=paket["referans"]["kayit_id"],
        sembol=sembol,
        nominal_tutar=float(deneme["risk_ayarlari"]["nominal_tutar"]),
        risk_surumu=deneme["risk_ayarlari"]["risk_surumu"],
        masraf_surumu=deneme["masraf_ayarlari"]["masraf_surumu"],
        fiyat_politikasi=deneme["yontem_ayarlari"]["fiyat_politikasi"],
        strateji_ayar_parmak_izi=strateji.ayar_parmak_izi,
        deneme_ayar_parmak_izi=deneme["ayar_parmak_izi"],
    )
    durum = saglamlik.ema_hucre_calistir(
        m.loc[bas:son],
        p,
        sinyal_konumlari=sinyaller,
        kurulum=hesap["kurulum"],
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


def _donem_sinyalleri(deneme, sonuc, paket, sembol, hesap, m, gunler):
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
        if neden is None:
            if pd.Timestamp(t) in sinyaller:
                raise ValueError(f"{sembol}/{t}: birden çok günlük kurulum")
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
            _kayitli_bitir(kosu, deneme, sonuclar, hata)
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
        egri = _kapali_r_egrisi(islemler, r["donem"])
        olcu = istatistik.olc(islemler, politika="bagimsiz_olcu_v1", egri=egri)
        durum = _arama_donem_durumu(r, olcu["olculer"]["islem"]["deger"])
        semboller.append(dict(sembol=sembol, durum=durum, olcu=olcu))
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


def _kapali_r_egrisi(islemler, donem):
    gunler = {}
    refs = []
    for i in islemler:
        if i["sonuc"].get("kalan_adet") == 0:
            gun = i["pozisyon"]["cikis_tarih"][:10]
            gunler.setdefault(gun, []).append(i["sonuc"].get("net_r"))
            refs.append(i["islem_ref"])
    satirlar, toplam = [], 0.0
    for t, r in sorted(gunler.items()):
        toplam = toplam + sum(r) if toplam is not None and None not in r else None
        satirlar.append(dict(an=t, deger=toplam))
    return dict(
        tur="tani_net_r",
        satirlar=satirlar,
        baslangic_degeri=0.0,
        baslangic_ani=donem["baslangic"].isoformat(),
        baslangic_politikasi="acik",
        tarih_temeli="takvim_gunu",
        normalizasyon=dict(deger=1.0, birim="R", bos_nedeni=None),
        birim="R",
        muhasebe_politikasi="tani_net_r_v1",
        referanslar=refs,
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
