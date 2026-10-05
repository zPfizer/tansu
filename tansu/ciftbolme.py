"""Çift bölmesi: yıllık çift seçimi, Z geçişleri ve rotasyon simülasyonu (TASARIM 5.6 "Çift bölmesi kuralları").

Girdi `veri.Anlik` ve `simulator.evrenler` çıktısıdır. Fiyatlar düzeltilmiş seriden; kilit, karantina ve işlem
bayrakları ham seriden gelir (`veri.Anlik.gun_tablosu`). K2 ve faiz `simulator.zemin`'den, aynı kuralla.
"""

import itertools
from dataclasses import dataclass

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint

from tansu import cift, evren, motor, simulator

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


def secim_gunleri(gunler, ilk_konum) -> dict:
    """Yıl → yılın ilk işlem gününün konumu; yalnız simülatör başlangıcından sonraki (dahil) yıllar."""
    ilk = pd.Series(np.arange(len(gunler)), index=gunler).groupby(gunler.year).first()
    return {int(y): int(s) for y, s in ilk.items() if s >= ilk_konum}


def secim(Kc, uye, sektor, s, p=Parametre()) -> pd.DataFrame:
    """`s` konumundaki kapanışta seçilen çiftler: sektor, y, x, p, beta. `Kc`: düzeltilmiş kapanış (gün × sembol)."""
    pencere = Kc.iloc[max(0, s - p.secim_gun + 1): s + 1]
    bos = pd.DataFrame(columns=["sektor", "y", "x", "p", "beta"])
    if len(pencere) < p.secim_gun:
        return bos
    adaylar = sorted(h for h in uye if h in sektor and h in pencere.columns and pencere[h].notna().all())
    L = np.log(pencere[adaylar])
    aday_cift = []
    for ad, grup in itertools.groupby(sorted(adaylar, key=lambda h: (sektor[h], h)), key=lambda h: sektor[h]):
        for y, x in itertools.combinations(sorted(grup), 2):  # Y = sembol sırasına göre ilk
            beta = L[y].cov(L[x]) / L[x].var()
            if beta > 0:
                pv = coint(L[y].to_numpy(), L[x].to_numpy())[1]
                if pv < p.p_esik:
                    aday_cift.append((pv, y, x, ad, beta))
    secilen, kullanilan, sektor_sayisi = [], set(), {}
    for pv, y, x, ad, beta in sorted(aday_cift, key=lambda c: c[:3]):
        if len(secilen) == p.en_fazla:
            break
        if {y, x} & kullanilan or sektor_sayisi.get(ad, 0) >= p.sektor_basina:
            continue
        secilen.append({"sektor": ad, "y": y, "x": x, "p": pv, "beta": beta})
        kullanilan |= {y, x}
        sektor_sayisi[ad] = sektor_sayisi.get(ad, 0) + 1
    return pd.DataFrame(secilen, columns=bos.columns)


def hedef(Kc, y, x, p=Parametre()) -> np.ndarray:
    """Her kapanışta hedef bacak: +1 = Y (Z ≤ −eşik ve ΔZ > 0), −1 = X (Z ≥ +eşik ve ΔZ < 0), 0 = sinyal yok."""
    z = cift.z_skor(Kc[y], Kc[x], p.z_pencere)
    dz = cift.dz(z)
    return np.where((z <= -p.z_esik) & (dz > 0), 1, np.where((z >= p.z_esik) & (dz < 0), -1, 0))


def _bayrak(g, ad, gunler, kolonlar) -> pd.DataFrame:
    return g.pivot(index="tarih", columns="sembol", values=ad).reindex(index=gunler, columns=kolonlar).fillna(False).astype(bool)


def _rotasyon(M, setler, slot_sayisi, m) -> tuple:
    """Tek sürekli rotasyon portföyü: (tutuş dönemleri, özkaynak dizisi, hisse payı dizisi)."""
    days, pos, g, kol = M["days"], M["pos"], M["g"], M["kol"]
    C, A, Lq, I, T, B, E, SA, Kar = (M[k] for k in ("C", "A", "Lq", "I", "T", "B", "E", "SA", "Kar"))
    setler = [dict(s) for s in setler]
    serbest, slotlar, islemler, ozk, pay = simulator.SERMAYE, [], [], [], []

    def sat(s, tarih, fiyat, neden):
        s["nakit"] += s["adet"] * fiyat * (1 - m)
        islemler.append({"cift": f"{s['y']}-{s['x']}", "sembol": s["tutulan"], "giris_tarih": s["giris"][0],
                         "giris_fiyat": s["giris"][1], "cikis_tarih": tarih, "cikis_fiyat": fiyat, "neden": neden,
                         "adet": s["adet"], "getiri": fiyat * (1 - m) / (s["giris"][1] * (1 + m)) - 1})
        s["tutulan"], s["adet"] = None, 0

    for i, d in enumerate(days):
        q = pos[i]
        serbest *= 1 + g[i]
        for s in slotlar:
            s["nakit"] *= 1 + g[i]
        if setler and setler[0]["bas"] == q:  # yıl geçişi: seçimden sonraki ilk işlem günü AOF'u
            yeni = setler.pop(0)["ciftler"]
            for s in [s for s in slotlar if (s["y"], s["x"]) not in yeni]:
                if s["tutulan"]:
                    a = A[q, kol[s["tutulan"]]]
                    sat(s, d, a if np.isfinite(a) else C[q, kol[s["tutulan"]]], "yil_gecisi")
                serbest += s["nakit"]
                slotlar.remove(s)
            devam = {(s["y"], s["x"]) for s in slotlar}
            yeniler = [c for c in yeni if c not in devam]
            bos = slot_sayisi - len(devam)
            for y, x in yeniler:
                slotlar.append({"y": y, "x": x, "nakit": serbest / bos, "tutulan": None, "adet": 0, "olu": False,
                                "hedef": M["hedef"](y, x)})
            serbest -= len(yeniler) * (serbest / bos) if bos else 0.0
        for s in slotlar:
            iy, ix = kol[s["y"]], kol[s["x"]]
            if s["olu"] or M["olu"].get(s["y"], np.inf) <= q or M["olu"].get(s["x"], np.inf) <= q:
                s["olu"] = True
                if s["tutulan"] and M["olu"].get(s["tutulan"], np.inf) <= q:  # kapanma: −%100 (TASARIM 5.2)
                    sat(s, d, 0.0, "kapanma")
                continue
            if s["tutulan"] and Kar[q, kol[s["tutulan"]]]:  # karantina: son temiz AOF, karantina günü
                sat(s, d, SA[q, kol[s["tutulan"]]], "karantina")
                continue
            h = s["hedef"][q - 1]
            if h == 0:
                continue
            istenen = s["y"] if h > 0 else s["x"]
            if istenen == s["tutulan"] or not (I[q, iy] and I[q, ix]) or any(
                    k[q, j] for k in (T, B, E) for j in (iy, ix)):
                continue  # engel: işlem yok, kilit ya da karantina penceresi; sinyal taşınmaz
            if s["tutulan"]:
                sat(s, d, A[q, kol[s["tutulan"]]], "gecis")
            a = A[q, kol[istenen]]
            adet = int(np.floor(min(s["nakit"] / (a * (1 + m)), simulator.LIKIDITE * Lq[q - 1, kol[istenen]] / a)))
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
                adet = int(np.floor(pay / 2 / (a * (1 + m)))) if I[q, kol[h]] and np.isfinite(a) else 0
                if adet >= 1:
                    nakit -= adet * a * (1 + m)
                    tutulan[h] = adet
        ozk.append(nakit + sum(n * C[q, kol[h]] for h, n in tutulan.items()))
    return np.array(ozk)


def _sonuc(M, setler, slot_sayisi, m) -> dict:
    islemler, ozk, pay = _rotasyon(M, setler, slot_sayisi, m)
    days = M["days"]
    ozk, k2 = pd.Series(ozk, index=days), pd.Series(simulator.k2_egri(pay, M["rb"], M["g"]), index=days)
    elli = pd.Series(_elli_elli(M, setler, slot_sayisi, m), index=days)
    yillik = simulator._yillik(ozk, k2).assign(elli_elli=simulator._yillik(elli, k2)["kural"])
    sutunlar = ["cift", "sembol", "giris_tarih", "giris_fiyat", "cikis_tarih", "cikis_fiyat", "neden", "adet", "getiri"]
    return {"islemler": pd.DataFrame(islemler, columns=sutunlar).assign(aile=AILE), "ozkaynak": ozk, "k2": k2,
            "elli_elli": elli, "yatirim": pd.Series(pay, index=days), "yillik": yillik}


def hazirla(anlik, evr, bas=simulator.BASLANGIC, p=Parametre()) -> dict:
    """Seçimler, fiyat matrisleri ve bayraklar (`M`); `calistir` ve K1 ortak kullanır."""
    gunler = anlik.gunler
    ilk = simulator.ilk_gun(anlik, bas)
    days = gunler[gunler >= ilk]
    ilk_konum = gunler.get_loc(ilk)
    kap = evren.kapananlar(anlik)
    kg = dict(zip(kap["sembol"], zip(kap["son_islem"], kap["kapanma_gunu"])))
    sektor = anlik.sektor or {}
    uye = {h for liste in evr.values() for h in liste}
    sabit = tuple(p.sabit) if set(p.sabit) <= set(anlik.fiyat["sembol"]) else ()
    f = anlik.fiyat[anlik.fiyat["sembol"].isin(uye | set(sabit))]
    Kc = f.pivot(index="tarih", columns="sembol", values="kapanis").reindex(gunler)
    yillar = secim_gunleri(gunler, ilk_konum)
    satirlar, setler = [], []
    for yil, s in yillar.items():
        c = secim(Kc, evr.get(gunler[s].to_period("M"), []), sektor, s, p).assign(yil=yil)
        satirlar.append(c)
        if s + 1 < len(gunler):
            setler.append({"bas": s + 1, "yil": yil, "ciftler": list(zip(c["y"], c["x"]))})
    secimler = pd.concat(satirlar, ignore_index=True) if satirlar else pd.DataFrame(columns=["sektor", "y", "x", "p", "beta", "yil"])
    secimler = secimler[["yil", "sektor", "y", "x", "p", "beta"]]
    z = simulator.zemin(anlik, evr, days, set(secimler["y"]) | set(secimler["x"]) | set(sabit), kg)
    kol = {h: j for j, h in enumerate(z["C"].columns)}
    gt = anlik.gun_tablosu
    gt = gt[gt["sembol"].isin(kol)]
    bayrak = {k: _bayrak(gt, ad, gunler, list(kol)) for k, ad in (("I", "islem"), ("T", "kilit_tavan"),
                                                                 ("B", "kilit_taban"), ("Kar", "karantina"))}
    E = bayrak["Kar"].astype(float).rolling(motor.KARANTINA_GUN, min_periods=1).max().astype(bool)
    onbellek = {}

    def hedef_(y, x):
        if (y, x) not in onbellek:
            onbellek[(y, x)] = hedef(Kc, y, x, p)
        return onbellek[(y, x)]

    M = {"days": days, "pos": gunler.get_indexer(days), "kol": kol, "g": z["g"], "rb": z["rb"], "C": z["C"].to_numpy(),
         "A": z["A"].to_numpy(), "Lq": z["Lq"].to_numpy(), "I": bayrak["I"].to_numpy(), "T": bayrak["T"].to_numpy(),
         "B": bayrak["B"].to_numpy(), "Kar": bayrak["Kar"].to_numpy(), "E": E.to_numpy(),
         "SA": z["A"].where(bayrak["I"] & ~bayrak["Kar"]).ffill().to_numpy(), "hedef": hedef_,
         "olu": {h: gunler.get_loc(gun) for h, (_, gun) in kg.items() if gun in gunler}}
    sabit_set = [{"bas": ilk_konum + 1, "yil": None, "ciftler": [sabit]}] if sabit else []
    return {"M": M, "setler": setler, "secim": secimler, "sabit": sabit, "sabit_set": sabit_set, "p": p, "Kc": Kc,
            "gunler": gunler}


def calistir(anlik, evr, bas=simulator.BASLANGIC, p=Parametre(), masraflar=simulator.MASRAFLAR, h=None) -> dict:
    """Çift bölmesi ve VAKBN–GARAN sabit çifti, her masraf düzeyi için.

    Döner: secim (yıl, sektor, y, x, p, beta), islem_yok (çift seçilmeyen yıllar), masraf {m: sonuç}, sabit {m: sonuç}
    (sabit çiftin sembolleri yoksa boş), bilgi. `h`: `hazirla` çıktısı (K1 ile paylaşmak için)."""
    h = h or hazirla(anlik, evr, bas, p)
    M, setler, secimler, sabit, sabit_set = (h[k] for k in ("M", "setler", "secim", "sabit", "sabit_set"))
    sonuc = {"masraf": {m: _sonuc(M, setler, p.en_fazla, m) for m in masraflar},
             "sabit": {m: _sonuc(M, sabit_set, 1, m) for m in masraflar} if sabit else {}}
    islemler = sonuc["masraf"][0.003]["islemler"]
    return {**sonuc, "secim": secimler, "islem_yok": [s["yil"] for s in setler if not s["ciftler"]],
            "bilgi": {"gecis": len(islemler), "gecis_gun": int(islemler["giris_tarih"].nunique()),
                      "yil": len(setler), "secilen": len(secimler)}}
