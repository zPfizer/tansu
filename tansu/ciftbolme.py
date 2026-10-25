"""Çift bölmesi: yıllık çift seçimi, Z geçişleri ve rotasyon simülasyonu (TASARIM 5.6 "Çift bölmesi kuralları").

Girdi `veri.Anlik` ve `simulator.evrenler` çıktısıdır. Fiyatlar düzeltilmiş seriden; kilit, karantina ve işlem
bayrakları ham seriden gelir (`veri.Anlik.gun_tablosu`). K2 ve faiz `simulator.zemin`'den, aynı kuralla.
"""

import itertools
import hashlib
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint

from tansu import cift, evren, gostergeler, simulator, veri

AILE = "cift_rotasyonu"


@dataclass(frozen=True)
class Parametre:
    z_pencere: int = 60  # KURALLAR §3 madde 1 (YORUM)
    z_esik: float = 2.0
    secim_gun: int = 252  # TASARIM 5.6 çift seçimi (YORUM)
    p_esik: float = 0.05
    en_fazla: int = 5
    sektor_basina: int = 2
    sabit: tuple = ("VAKBN", "GARAN")  # Tansu'nun çifti: (Y, X)


def strateji_coz(y="VAKBN", x="GARAN", p=Parametre()):
    """Katalog dışı mevcut çift ayarlarını çözer (TASARIM 5.15)."""
    if not y or not x or y == x:
        raise ValueError("Çift iki farklı sembol gerektirir")
    ayarlar = {**asdict(p), "ddof": 1, "mod": "log_oran"}
    icerik = json.dumps(ayarlar, sort_keys=True, ensure_ascii=False)
    parmak_izi = hashlib.sha256(icerik.encode("utf-8")).hexdigest()
    kaynaklar = [
        {
            "tur": "mevcut_kod",
            "konum": "tansu/ciftbolme.py:Parametre; tansu/cift.py:z_skor",
            "tarih": "2026-10-18",
            "alinti": None,
            "bos_nedenleri": {"alinti": "mevcut_kod_ayari"},
            "karar_durumu": "mevcut_ayar",
        },
        {
            "tur": "tasarim",
            "konum": "docs/TASARIM.md:488-498",
            "tarih": "2026-10-18",
            "alinti": None,
            "bos_nedenleri": {"alinti": "mevcut_kural_referansi"},
            "karar_durumu": "mevcut_kural",
        },
    ]
    birimler = {
        "z_pencere": "seans",
        "secim_gun": "seans",
        "sabit": "sembol",
        "mod": "birimsiz",
    }
    parametreler = [
        {
            "ad": ad,
            "deger": deger,
            "tur": "liste"
            if isinstance(deger, tuple)
            else "metin"
            if isinstance(deger, str)
            else "tam"
            if isinstance(deger, int)
            else "sayi",
            "birim": birimler.get(ad, "birimsiz"),
            "kaynaklar": kaynaklar,
        }
        for ad, deger in ayarlar.items()
    ]
    return {
        "kayit_id": f"cift_rotasyonu:{parmak_izi}",
        "kayit_turu": "tam_cozulmus_strateji",
        "sema_surumu": "kurulum_s06_v1",
        "olusturma_zamani": datetime.now(timezone.utc).isoformat(),
        "aile": AILE,
        "varyant": "log_oran",
        "katalog_surumu": "",
        "katalog_gerekcesi": "s02_v1 yalnız ema_sikisma içerir; çift ailesi katalogda yok",
        "semboller": [y, x],
        "parametreler": parametreler,
        "gosterge_ayarlari": [
            a for a in parametreler if a["ad"] in ("z_pencere", "ddof", "mod")
        ],
        "bilesim_id": "legacy_cift_log_oran",
        "izin_durumu": "legacy_karsilastirma",
        "dolum_surumu": "legacy_aof_5_3",
        "risk_surumu": "legacy_cift_5_6",
        "masraf_surumu": "legacy_masraf_5_4",
        "muhasebe_surumu": "legacy_cift_5_6",
        "donem_surumu": "legacy_donem_5_8",
        "ayar_parmak_izi": parmak_izi,
        "politika_surumu": "legacy_cift_5_6",
        "kaynaklar": kaynaklar,
    }


def ortak_kurulum(veri_paketi, tarih, strateji):
    """E1 çift hesabı; ısınma geçmişinden yalnız değerlendirme günü çıkar (TASARIM 5.15)."""
    y, x = strateji["semboller"]
    ayarlar = {a["ad"]: a["deger"] for a in strateji["parametreler"]}
    p = Parametre(**{ad: ayarlar[ad] for ad in Parametre.__dataclass_fields__})
    beklenen = strateji_coz(y, x, p)
    if any(
        strateji.get(ad) != deger
        for ad, deger in beklenen.items()
        if ad != "olusturma_zamani"
    ):
        raise ValueError("Çözülmüş çift stratejisi mevcut ayarlarla uyuşmuyor")
    tarih = pd.Timestamp(tarih)
    donem = veri_paketi["referans"]["istenen_donem"]
    if not pd.Timestamp(donem["baslangic"]) <= tarih <= pd.Timestamp(donem["bitis"]):
        raise ValueError("Değerlendirme tarihi istenen dönemin dışında")
    Kc = _piyasa_kapanislari(veri_paketi, tarih, (y, x))
    g = cift.hesapla(
        Kc[y], Kc[x], p.z_pencere, ayarlar["ddof"], ayarlar["mod"], p.z_esik
    )
    ad = f"{y}-{x}"
    sonuc = {
        "gostergeler": [],
        "sinyaller": [],
        "isinma": {
            ad: {
                "gozlem": int(Kc.notna().all(axis=1).sum()),
                "gerekli": p.z_pencere + 1,
                "tamam": bool(len(g) and pd.notna(g["dz"].iloc[-1])),
            }
        },
    }
    if tarih not in g.index:
        return sonuc
    meta = {
        "sema_surumu": "kurulum_s06_v1",
        "olusturma_zamani": datetime.now(timezone.utc).isoformat(),
        "kaynaklar": strateji["kaynaklar"],
        "baglar": {
            "deneme_id": None,
            "kosu_id": None,
            "ayar_parmak_izi": strateji["ayar_parmak_izi"],
            "politika_surumu": strateji["politika_surumu"],
            "veri_ref_id": veri_paketi["referans"]["kayit_id"],
            "bos_nedenleri": {
                "deneme_id": "hesap_onizlemesi",
                "kosu_id": "hesap_onizlemesi",
            },
        },
    }
    for gosterge in ("z", "dz"):
        sonuc["gostergeler"].append(
            {
                **meta,
                "kayit_id": f"{ad}:{tarih.date()}:{gosterge}:{strateji['ayar_parmak_izi']}",
                "kayit_turu": "gosterge",
                "sembol": ad,
                "tarih": str(tarih.date()),
                "ad": gosterge,
                **gostergeler.deger_kaydi(
                    g.at[tarih, gosterge],
                    "birimsiz",
                    "eksik_veri" if Kc.isna().any().any() else "isinma_veya_tanimsiz",
                ),
            }
        )
    hedef_bacak = int(g.at[tarih, "hedef"])
    if hedef_bacak:
        sonuc["sinyaller"].append(_sinyal_kaydi(strateji, tarih, hedef_bacak, meta))
    return sonuc


def _piyasa_kapanislari(paket, tarih, semboller):
    gunler = pd.DatetimeIndex(paket["gunler"])
    if not gunler.is_monotonic_increasing or gunler.has_duplicates:
        raise ValueError("Piyasa tarihleri sıralı ve tekil olmalı")
    Kc = pd.DataFrame(index=gunler[gunler <= tarih], columns=semboller, dtype=float)
    for sembol in semboller:
        satirlar = [
            r
            for r in paket["piyasa"]
            if r["sembol"] == sembol and pd.Timestamp(r["tarih"]) <= tarih
        ]
        indeks = pd.DatetimeIndex([r["tarih"] for r in satirlar])
        if not indeks.is_monotonic_increasing or indeks.has_duplicates:
            raise ValueError("Piyasa tarihleri sıralı ve tekil olmalı")
        Kc[sembol] = pd.Series(
            [
                np.nan
                if "eksik" in r.get("kalite_bayraklari", ())
                else r["duzeltilmis_kapanis"]["deger"]
                for r in satirlar
            ],  # TASARIM 5.13: E1 gözlemi hesapta eksik gün olarak kalır.
            index=indeks,
            dtype=float,
        )
    return Kc


def _sinyal_kaydi(strateji, tarih, hedef_bacak, meta):
    y, x = strateji["semboller"]
    ayarlar = {a["ad"]: a["deger"] for a in strateji["parametreler"]}
    bos = gostergeler.deger_kaydi
    return {
        **meta,
        "kayit_id": f"{y}-{x}:{tarih.date()}:{strateji['ayar_parmak_izi']}",
        "kayit_turu": "sinyal",
        "semboller": [y, x],
        "tarih": str(tarih.date()),
        **{
            ad: strateji[ad]
            for ad in ("aile", "varyant", "katalog_surumu", "katalog_gerekcesi")
        },
        "strateji_id": strateji["kayit_id"],
        "yon": "al",
        "aday_durumu": "legacy_sinyal",
        "kutu_alt": bos(None, "TL/adet", "cift_ailesinde_kutu_yok"),
        "kutu_ust": bos(None, "TL/adet", "cift_ailesinde_kutu_yok"),
        "hedef": bos(hedef_bacak, "bacak"),
        "hedef_sembol": y if hedef_bacak == 1 else x,
        "kar_hedefi": bos(None, "TL/adet", "cift_ailesinde_kar_hedefi_yok"),
        "ilk_stop": bos(None, "TL/adet", "cift_ailesinde_stop_yok"),
        "kurulum_girdileri": {
            ad: bos(ayarlar[ad], birim)
            for ad, birim in (
                ("z_pencere", "seans"),
                ("z_esik", "birimsiz"),
                ("ddof", "sayi"),
            )
        },
        "kural_kaniti": strateji["kaynaklar"],
    }


def secim_gunleri(gunler, ilk_konum) -> dict:
    """Yıl → yılın ilk işlem gününün konumu; yalnız simülatör başlangıcından sonraki (dahil) yıllar."""
    ilk = pd.Series(np.arange(len(gunler)), index=gunler).groupby(gunler.year).first()
    return {int(y): int(s) for y, s in ilk.items() if s >= ilk_konum}


def adaylar(Kc, uye, sektor, s, p=Parametre()) -> list:
    """`s` konumundaki kapanışta eşbütünleşme p < `p.p_esik` olan aynı sektör çiftleri: (p, y, x, sektor, beta), (p, y, x) sırasıyla.
    Çift seçimi (`sec`) bu listenin önekidir: daha dar bir `p_esik` için eşbütünleşme yeniden hesaplanmaz."""
    pencere = Kc.iloc[max(0, s - p.secim_gun + 1) : s + 1]
    if len(pencere) < p.secim_gun:
        return []
    aday = sorted(
        h
        for h in uye
        if h in sektor and h in pencere.columns and pencere[h].notna().all()
    )
    L = np.log(pencere[aday])
    aday_cift = []
    for ad, grup in itertools.groupby(
        sorted(aday, key=lambda h: (sektor[h], h)), key=lambda h: sektor[h]
    ):
        for y, x in itertools.combinations(
            sorted(grup), 2
        ):  # Y = sembol sırasına göre ilk
            beta = L[y].cov(L[x]) / L[x].var()
            if beta > 0:
                pv = coint(L[y].to_numpy(), L[x].to_numpy())[1]
                if pv < p.p_esik:
                    aday_cift.append((pv, y, x, ad, beta))
    return sorted(aday_cift, key=lambda c: c[:3])


def sec(aday, p=Parametre()) -> pd.DataFrame:
    """`adaylar` listesinden çift seçimi: sektor, y, x, p, beta; en küçük p önce, en fazla `p.en_fazla`, sektör başına `p.sektor_basina`."""
    bos = pd.DataFrame(columns=["sektor", "y", "x", "p", "beta"])
    secilen, kullanilan, sektor_sayisi = [], set(), {}
    for pv, y, x, ad, beta in (c for c in aday if c[0] < p.p_esik):
        if len(secilen) == p.en_fazla:
            break
        if {y, x} & kullanilan or sektor_sayisi.get(ad, 0) >= p.sektor_basina:
            continue
        secilen.append({"sektor": ad, "y": y, "x": x, "p": pv, "beta": beta})
        kullanilan |= {y, x}
        sektor_sayisi[ad] = sektor_sayisi.get(ad, 0) + 1
    return pd.DataFrame(secilen, columns=bos.columns)


def secim(Kc, uye, sektor, s, p=Parametre()) -> pd.DataFrame:
    """`s` konumundaki kapanışta seçilen çiftler: sektor, y, x, p, beta. `Kc`: düzeltilmiş kapanış (gün × sembol)."""
    return sec(adaylar(Kc, uye, sektor, s, p), p)


def hedef(Kc, y, x, p=Parametre()) -> np.ndarray:
    """Her kapanışta hedef bacak: +1 = Y (Z ≤ −eşik ve ΔZ > 0), −1 = X (Z ≥ +eşik ve ΔZ < 0), 0 = sinyal yok."""
    return cift.hesapla(Kc[y], Kc[x], p.z_pencere, esik=p.z_esik)["hedef"].to_numpy()


def _rotasyon(M, setler, slot_sayisi, m) -> tuple:
    """Tek sürekli rotasyon portföyü: (tutuş dönemleri, özkaynak dizisi, hisse payı dizisi)."""
    days, pos, g, kol = M["days"], M["pos"], M["g"], M["kol"]
    C, A, Lq, I, T, B, E, SA, Kar = (
        M[k] for k in ("C", "A", "Lq", "I", "T", "B", "E", "SA", "Kar")
    )
    setler = [dict(s) for s in setler]
    serbest, slotlar, islemler, ozk, pay = simulator.SERMAYE, [], [], [], []

    def sat(s, tarih, fiyat, neden):
        s["nakit"] += s["adet"] * fiyat * (1 - m)
        islemler.append(
            {
                "cift": f"{s['y']}-{s['x']}",
                "sembol": s["tutulan"],
                "giris_tarih": s["giris"][0],
                "giris_fiyat": s["giris"][1],
                "cikis_tarih": tarih,
                "cikis_fiyat": fiyat,
                "neden": neden,
                "adet": s["adet"],
                "getiri": fiyat * (1 - m) / (s["giris"][1] * (1 + m)) - 1,
            }
        )
        s["tutulan"], s["adet"] = None, 0

    for i, d in enumerate(days):
        q = pos[i]
        serbest *= 1 + g[i]
        for s in slotlar:
            s["nakit"] *= 1 + g[i]
        if (
            setler and setler[0]["bas"] == q
        ):  # yıl geçişi: seçimden sonraki ilk işlem günü AOF'u
            yeni = setler.pop(0)["ciftler"]
            for s in [s for s in slotlar if (s["y"], s["x"]) not in yeni]:
                if s["tutulan"]:
                    a = A[q, kol[s["tutulan"]]]
                    sat(
                        s,
                        d,
                        a if np.isfinite(a) else C[q, kol[s["tutulan"]]],
                        "yil_gecisi",
                    )
                serbest += s["nakit"]
                slotlar.remove(s)
            devam = {(s["y"], s["x"]) for s in slotlar}
            yeniler = [c for c in yeni if c not in devam]
            bos = slot_sayisi - len(devam)
            for y, x in yeniler:
                slotlar.append(
                    {
                        "y": y,
                        "x": x,
                        "nakit": serbest / bos,
                        "tutulan": None,
                        "adet": 0,
                        "olu": False,
                        "hedef": M["hedef"](y, x),
                    }
                )
            serbest -= len(yeniler) * (serbest / bos) if bos else 0.0
        for s in slotlar:
            iy, ix = kol[s["y"]], kol[s["x"]]
            if (
                s["olu"]
                or M["olu"].get(s["y"], np.inf) <= q
                or M["olu"].get(s["x"], np.inf) <= q
            ):
                s["olu"] = True
                if (
                    s["tutulan"] and M["olu"].get(s["tutulan"], np.inf) <= q
                ):  # kapanma: −%100 (TASARIM 5.2)
                    sat(s, d, 0.0, "kapanma")
                continue
            if (
                s["tutulan"] and Kar[q, kol[s["tutulan"]]]
            ):  # karantina: son temiz AOF, karantina günü
                sat(s, d, SA[q, kol[s["tutulan"]]], "karantina")
                continue
            h = s["hedef"][q - 1]
            if h == 0:
                continue
            istenen = s["y"] if h > 0 else s["x"]
            if (
                istenen == s["tutulan"]
                or not (I[q, iy] and I[q, ix])
                or any(k[q, j] for k in (T, B, E) for j in (iy, ix))
            ):
                continue  # engel: işlem yok, kilit ya da karantina penceresi; sinyal taşınmaz
            if s["tutulan"]:
                sat(s, d, A[q, kol[s["tutulan"]]], "gecis")
            a = A[q, kol[istenen]]
            adet = int(
                np.floor(
                    min(
                        s["nakit"] / (a * (1 + m)),
                        simulator.LIKIDITE * Lq[q - 1, kol[istenen]] / a,
                    )
                )
            )
            if adet >= 1:
                s["nakit"] -= adet * a * (1 + m)
                s.update(tutulan=istenen, adet=adet, giris=(d, a))
        mv = sum(s["adet"] * C[q, kol[s["tutulan"]]] for s in slotlar if s["tutulan"])
        ozk.append(serbest + sum(s["nakit"] for s in slotlar) + mv)
        pay.append(mv / ozk[-1])
    for s in slotlar:  # veri sonu: son kapanıştan çıkış (özkaynağı değiştirmez)
        if s["tutulan"]:
            nakit = s["nakit"]
            sat(s, days[-1], C[pos[-1], kol[s["tutulan"]]], "veri_sonu")
            s["nakit"] = nakit
    return islemler, np.array(ozk), np.array(pay)


def _elli_elli(M, setler, slot_sayisi, m) -> np.ndarray:
    """Tanısal: seçimden sonraki ilk işlem günü AOF'unda her payın yarısı Y'ye, yarısı X'e; yıl sonuna dek tutulur."""
    days, pos, g, kol = M["days"], M["pos"], M["g"], M["kol"]
    C, A, I = M["C"], M["A"], M["I"]
    setler, nakit, tutulan, ozk = [dict(s) for s in setler], simulator.SERMAYE, {}, []
    for i, d in enumerate(days):
        q = pos[i]
        nakit *= 1 + g[i]
        tutulan = {h: n for h, n in tutulan.items() if M["olu"].get(h, np.inf) > q}
        if setler and setler[0]["bas"] == q:
            for h, n in tutulan.items():
                a = A[q, kol[h]]
                nakit += n * (a if np.isfinite(a) else C[q, kol[h]]) * (1 - m)
            tutulan = {}
            pay = nakit / slot_sayisi
            for h in (h for c in setler.pop(0)["ciftler"] for h in c):
                a = A[q, kol[h]]
                adet = (
                    int(np.floor(pay / 2 / (a * (1 + m))))
                    if I[q, kol[h]] and np.isfinite(a)
                    else 0
                )
                if adet >= 1:
                    nakit -= adet * a * (1 + m)
                    tutulan[h] = adet
        ozk.append(nakit + sum(n * C[q, kol[h]] for h, n in tutulan.items()))
    return np.array(ozk)


def _sonuc(M, setler, slot_sayisi, m) -> dict:
    islemler, ozk, pay = _rotasyon(M, setler, slot_sayisi, m)
    days = M["days"]
    ozk, k2 = (
        pd.Series(ozk, index=days),
        pd.Series(simulator.k2_egri(pay, M["rb"], M["g"]), index=days),
    )
    elli = pd.Series(_elli_elli(M, setler, slot_sayisi, m), index=days)
    yillik = simulator._yillik(ozk, k2).assign(
        elli_elli=simulator._yillik(elli, k2)["kural"]
    )
    sutunlar = [
        "cift",
        "sembol",
        "giris_tarih",
        "giris_fiyat",
        "cikis_tarih",
        "cikis_fiyat",
        "neden",
        "adet",
        "getiri",
    ]
    return {
        "islemler": pd.DataFrame(islemler, columns=sutunlar).assign(aile=AILE),
        "ozkaynak": ozk,
        "k2": k2,
        "elli_elli": elli,
        "yatirim": pd.Series(pay, index=days),
        "yillik": yillik,
    }


POOL_ESIK = 3000  # yıllık eşbütünleşme sınamaları bu çift sayısından çoksa yıllar ayrı süreçlerde koşar (sonuç aynı)


def _adaylar_yil(arg) -> list:
    pencere, uye, sektor, p = arg
    return adaylar(pencere, uye, sektor, len(pencere) - 1, p)


def _adaylar_yillar(Kc, evr, gunler, yillar, sektor, p) -> dict:
    """Yıl → (seçim günü konumu, `adaylar` listesi). Eşbütünleşme çift başına ~10 ms: gerçek veride yılda ~1.000 çift."""
    isler = []
    for yil, s in yillar.items():
        uye = [
            h
            for h in evr.get(gunler[s].to_period("M"), [])
            if h in sektor and h in Kc.columns
        ]
        isler.append(
            (Kc.iloc[max(0, s - p.secim_gun + 1) : s + 1][uye], uye, sektor, p)
        )
    sayi = sum(
        k * (k - 1) // 2
        for _, uye, sek, _ in isler
        for k in Counter(sek[h] for h in uye).values()
    )
    if sayi > POOL_ESIK:
        with ProcessPoolExecutor() as havuz:
            sonuc = list(havuz.map(_adaylar_yil, isler))
    else:
        sonuc = list(map(_adaylar_yil, isler))
    return {yil: (s, a) for (yil, s), a in zip(yillar.items(), sonuc, strict=True)}


def setler_sec(h, p) -> tuple:
    """(seçimler tablosu, yıl setleri): `hazirla` çıktısının aday listelerinden `p` kuralıyla çift seçimi (ızgara için)."""
    satirlar, setler = [], []
    for yil, (s, aday) in h["aday"].items():
        c = sec(aday, p).assign(yil=yil)
        satirlar.append(c)
        if s + 1 < len(h["gunler"]):
            setler.append(
                {
                    "bas": s + 1,
                    "yil": yil,
                    "ciftler": list(zip(c["y"], c["x"], strict=True)),
                }
            )
    secimler = (
        pd.concat(satirlar, ignore_index=True)
        if satirlar
        else pd.DataFrame(columns=["sektor", "y", "x", "p", "beta", "yil"])
    )
    return secimler[["yil", "sektor", "y", "x", "p", "beta"]], setler


def hazirla(anlik, evr, bas=simulator.BASLANGIC, p=Parametre(), aday_esik=None) -> dict:
    """Seçimler, fiyat matrisleri ve bayraklar (`M`); `calistir` ve K1 ortak kullanır.

    `aday_esik`: eşbütünleşme adayları bu p eşiğine dek tutulur (varsayılan `p.p_esik`); sağlamlık ızgarası daha geniş
    eşiği bir kez hesaplar, daha dar `p_esik` hücreleri `setler_sec` ile aynı adaylardan seçer. Matrisler geniş seçimin
    sembollerini kapsar; bir çiftin sonucu başka sembollerden bağımsızdır."""
    gunler = anlik.gunler
    ilk = simulator.ilk_gun(anlik, bas)
    days = gunler[gunler >= ilk]
    ilk_konum = gunler.get_loc(ilk)
    kap = evren.kapananlar(anlik)
    kg = dict(
        zip(
            kap["sembol"],
            zip(kap["son_islem"], kap["kapanma_gunu"], strict=True),
            strict=True,
        )
    )
    sektor = anlik.sektor or {}
    uye = {h for liste in evr.values() for h in liste}
    sabit = tuple(p.sabit) if set(p.sabit) <= set(anlik.fiyat["sembol"]) else ()
    f = anlik.hesap_fiyati[anlik.hesap_fiyati["sembol"].isin(uye | set(sabit))]
    Kc = f.pivot(index="tarih", columns="sembol", values="kapanis").reindex(gunler)
    yillar = secim_gunleri(gunler, ilk_konum)
    genis = replace(p, p_esik=max(p.p_esik, aday_esik or 0.0))
    h = {
        "aday": _adaylar_yillar(Kc, evr, gunler, yillar, sektor, genis),
        "gunler": gunler,
    }
    secimler, setler = setler_sec(h, p)
    tum = setler_sec(h, genis)[0]
    z = simulator.zemin(
        anlik, evr, days, set(tum["y"]) | set(tum["x"]) | set(sabit), kg
    )
    kol = {h: j for j, h in enumerate(z["C"].columns)}
    gt = anlik.gun_tablosu
    gt = gt[gt["sembol"].isin(kol)]
    ortak = veri.cift_girdileri(
        gunler,
        z["C"],
        z["A"],
        veri.cift_bayraklari(gt, gunler, list(kol)),
        "legacy_portfoy_v1",
    )
    onbellek = {}

    def hedef_(y, x):
        if (y, x) not in onbellek:
            onbellek[(y, x)] = hedef(Kc, y, x, p)
        return onbellek[(y, x)]

    M = {
        "days": days,
        "pos": gunler.get_indexer(days),
        "kol": kol,
        "g": z["g"],
        "rb": z["rb"],
        "C": ortak["C"],
        "A": ortak["A"],
        "Lq": z["Lq"].to_numpy(),
        **{k: ortak[k] for k in ("I", "T", "B", "Kar", "E", "SA")},
        "hedef": hedef_,
        "olu": {h: gunler.get_loc(gun) for h, (_, gun) in kg.items() if gun in gunler},
    }
    sabit_set = (
        [{"bas": ilk_konum + 1, "yil": None, "ciftler": [sabit]}] if sabit else []
    )
    return {
        "M": M,
        "setler": setler,
        "secim": secimler,
        "sabit": sabit,
        "sabit_set": sabit_set,
        "p": p,
        "Kc": Kc,
        "gunler": gunler,
        "aday": h["aday"],
    }


def calistir(
    anlik,
    evr,
    bas=simulator.BASLANGIC,
    p=Parametre(),
    masraflar=simulator.MASRAFLAR,
    h=None,
) -> dict:
    """Çift bölmesi ve VAKBN–GARAN sabit çifti, her masraf düzeyi için.

    Döner: secim (yıl, sektor, y, x, p, beta), islem_yok (çift seçilmeyen yıllar), masraf {m: sonuç}, sabit {m: sonuç}
    (sabit çiftin sembolleri yoksa boş), bilgi. `h`: `hazirla` çıktısı (K1 ile paylaşmak için)."""
    h = h or hazirla(anlik, evr, bas, p)
    M, setler, secimler, sabit, sabit_set = (
        h[k] for k in ("M", "setler", "secim", "sabit", "sabit_set")
    )
    sonuc = {
        "masraf": {m: _sonuc(M, setler, p.en_fazla, m) for m in masraflar},
        "sabit": {m: _sonuc(M, sabit_set, 1, m) for m in masraflar} if sabit else {},
    }
    islemler = sonuc["masraf"][0.003]["islemler"]
    return {
        **sonuc,
        "secim": secimler,
        "islem_yok": [s["yil"] for s in setler if not s["ciftler"]],
        "bilgi": {
            "gecis": len(islemler),
            "gecis_gun": int(islemler["giris_tarih"].nunique()),
            "yil": len(setler),
            "secilen": len(secimler),
        },
    }
