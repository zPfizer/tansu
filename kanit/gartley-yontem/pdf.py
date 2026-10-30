"""Gartley PDF setup ailesi: 13 ön kayıtlı deneme (`kanit/gartley-yontem/plan-pdf.md`, ceb1e7a).

Veri şekli: aday başına bir sinyal tablosu (`bos_sinyal` sütunları + D, örüntü günü, ust = C, x_i = X satırı). Tablo
`yontem.py`'nin sinyal düzeyi R'sine (`_sinyal_duzeyi`) ve para katmanına (`_motor`, `para_katmani`) gider; veri, grup,
ölçü, defter ve geçme şartı `yontem.py`'den (değiştirilmez, SHA-256 f9d682a17676...). Değerler plan-pdf.md'den.

Kullanım (PYTHONPATH = worktree kökü):
  pdf.py kontrol                              -> kendi kendine sınamalar (assert); deftere yazmaz
  pdf.py sinyal <aday> ayar                   -> sinyal düzeyi R, ayar grubu, 2015-2022
  pdf.py para <aday> ayar                     -> para katmanı, ayar grubu, 2015-2022
  pdf.py aile                                 -> 13 aday ayar grubunda, tek özet tablo ve en iyi aday
  pdf.py dsr                                  -> Deflated Sharpe (N = 13) ve PBO (CSCV, S = 16), ayar grubu
  pdf.py prova <aday>                         -> `sinav` ile aynı işlev, ayar grubunda; kilit yok
  pdf.py sinav <aday> <pdf.py SHA-256>        -> ayrık grup, yalnız `aile`nin en iyisi, PDF ailesinde bir kez
Adaylar: S1, S1-V1, S1-V2, S1-V3, S1-V5, S1-P3, S1-T20, S1-Z10, S2-Z, S2-T, S2-V1, S3, S3-A.
"""

import datetime as dt
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from statistics import NormalDist
from typing import NamedTuple

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

import tansu
from tansu import gostergeler, islem, yapi
from tansu.strateji import bos_sinyal

_spec = importlib.util.spec_from_file_location("yontem", Path(__file__).with_name("yontem.py"))
yontem = importlib.util.module_from_spec(_spec)
sys.modules["yontem"] = yontem
_spec.loader.exec_module(yontem)
if yontem.KAYNAK_SHA != "f9d682a17676f36de2236b459b56f632dfba06040e8dc904e96ad0b230559bde":
    raise SystemExit(f"yontem.py dondurulmuş dosya değil: {yontem.KAYNAK_SHA}")
para = yontem.para

KAYNAK_SHA = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()  # içe aktarmada bir kez
SONUC = yontem.J / "sonuc-pdf"
KILIT_KLASORU = yontem.J
AILE_OZET = SONUC / "aile-ayar" / "ozet.json"
DONEM = yontem.DONEM

# plan-pdf.md "Ortak kurallar" ve aile tablosu; ayarlanmaz.
AB_XA, D_XA, S3_CD, HEDEF_CD = 0.618, 0.786, 1.272, 0.618
EN_UZUN = 100  # X'ten bu yana en çok mum (emir düşer)
TEYIT_MUM = 5  # S1-V2: dokunuştan sonraki mum sayısı
CIKIS = {"tur": "tp1", "acilis_stopu": True}  # hedef1'de tam çıkış, iz yok, açılış stopun altındaysa AOF
K_SINAV = 5  # plan-pdf.md "Değişiklik 1": önceki 3 aday + S2-Z + S3; baraj p < 0,01
SINAV_ADAYLARI = ("S2-Z", "S3")  # plan-pdf.md "Değişiklik 1": kural seçimi S2-Z, en düşük p S3; her biri bir kez
CSCV_S = 16
UZUN = "X'ten 100 mumdan fazla (emir düştü)"
C_ASILDI = "dolumdan önce yüksek > C (emir düştü)"
SURE_CIKISI = "süre çıkışı"


class Aday(NamedTuple):
    pivot: str  # "guc_<N>" simetrik güç N | "zigzag_<yüzde>"
    T: float  # mutlak oran toleransı
    giris: str  # "limit" D'de | "teyit" dokunuş + kapanış > önceki kapanış, ertesi gün AOF | "tetik" CD/BC >= 1,27 mumu, ertesi gün AOF
    bc: tuple[float, float]  # BC/AB [alt - T; üst + T]
    cd: tuple[float, float] | None  # CD/BC [alt - T; üst + T] (D formülle); tetikte alt T'siz; S3'te yok
    d: str  # "xa786" D = A - 0,786 XA | "cb1272" D = C - 1,272 BC | "mum" tetik mumunun düşüğü
    stop: str  # "X" | "atr" D - ATR(14) (C onay günü)
    hedef: str  # HEDEF anahtarı
    rr: float | None  # 0,618 (C - D) / (D - X) en az
    sure: bool  # X'ten dolum gününe kadarki mum sayısı kadar tut
    ek_kural: int  # eşitlikte "daha az kurallı" için
    kural: str
    desen: str = "pdf"  # yontem._sinyal_duzeyi okur


HEDEF = {
    "cd618": lambda x, a, c, d, atr: d + HEDEF_CD * (c - d),
    "xa127": lambda x, a, c, d, atr: x + 1.27 * (a - x),
    "ad127": lambda x, a, c, d, atr: d + 1.27 * (a - d),
    "dx25": lambda x, a, c, d, atr: d + 2.5 * (d - x),
    "atr25": lambda x, a, c, d, atr: d + 2.5 * atr,
}

_S1 = Aday("guc_7", 0.10, "limit", (0.618, 0.786), (1.27, 1.618), "xa786", "X", "cd618", None, False, 0,
           "Behle-Conway: AB/XA 0,618±T, BC/AB [0,618-T; 0,786+T], CD/BC [1,27-T; 1,618+T], limit D = A - 0,786 XA, stop X, hedef D + 0,618 (C - D)")
_S2 = _S1._replace(hedef="xa127", kural="MTI diyagram: S1 oranları, limit D, stop X, hedef X + 1,27 (A - X)")
_S3 = _S1._replace(bc=(0.382, 0.886), cd=None, d="cb1272", hedef="dx25",
                   kural="Seo X3: AB/XA 0,618±T, BC/AB [0,382-T; 0,886+T], limit D = C - 1,272 BC > X, stop X, hedef D + 2,5 (D - X)")
ADAYLAR = {
    "S1": _S1,
    "S1-V1": _S1._replace(rr=2.0, ek_kural=1, kural="S1 + R/R 0,618 (C - D) / (D - X) >= 2,0"),
    "S1-V2": _S1._replace(giris="teyit", ek_kural=1, kural="S1, teyit: dokunuştan sonraki 5 mumda kapanış > önceki kapanış, ertesi gün AOF"),
    "S1-V3": _S1._replace(sure=True, ek_kural=1, kural="S1 + X'ten dolum gününe kadarki mum sayısı kadar tut"),
    "S1-V5": _S1._replace(giris="tetik", d="mum", kural="S1, tetik: CD/BC'yi ilk kez >= 1,27 yapan mum (T yok), D = düşüğü, ertesi gün AOF"),
    "S1-P3": _S1._replace(pivot="guc_3", kural="S1, pivot gücü 3"),
    "S1-T20": _S1._replace(T=0.20, kural="S1, T = 0,20"),
    "S1-Z10": _S1._replace(pivot="zigzag_10", kural="S1, günlük %10 zigzag pivot"),
    "S2-Z": _S2,
    "S2-T": _S2._replace(bc=(0.618, 0.618), cd=(1.618, 1.618), kural="S2-Z, metin oranları BC/AB 0,618±T, CD/BC 1,618±T"),
    "S2-V1": _S2._replace(hedef="ad127", kural="S2-Z, hedef D + 1,27 (A - D)"),
    "S3": _S3,
    "S3-A": _S3._replace(stop="atr", hedef="atr25", kural="S3, stop D - ATR(14), hedef D + 2,5 ATR(14) (C onay günü)"),
}


# --- Pivot ve sinyal tablosu ---


def guc_pivotlari(yuk: np.ndarray, dus: np.ndarray, fiyatli: np.ndarray, n: int) -> list[yapi.Pivot]:
    """Güç n: önceki n ve sonraki n fiyatlı mumun yükseği tepeninkinden düşük (eşitlik pivot değil); dip ayna.
    Onay günü pivottan sonraki n. fiyatlı mum."""
    idx = np.flatnonzero(fiyatli)
    if len(idx) < 2 * n + 1:
        return []
    pivotlar = []
    for tur, x, isaret in (("T", yuk[idx], 1.0), ("D", dus[idx], -1.0)):
        w = sliding_window_view(x * isaret, 2 * n + 1)
        diger = np.maximum(w[:, :n].max(axis=1), w[:, n + 1 :].max(axis=1))
        pivotlar += [
            yapi.Pivot(tur, int(idx[k + n]), int(idx[k + 2 * n]), float(x[k + n]))
            for k in np.flatnonzero(w[:, n] > diger)
        ]
    return sorted(pivotlar, key=lambda p: (p.onay_gun, p.pivot_gun, p.tur))


def _pivotlar(gun: pd.DataFrame, pivot: str, fiyatli: np.ndarray) -> list[yapi.Pivot]:
    mod, deger = pivot.rsplit("_", 1)
    if mod == "zigzag":
        return yapi.zigzag_pivotlari(gun["yuksek"], gun["dusuk"], float(deger))
    return guc_pivotlari(gun["yuksek"].to_numpy(float), gun["dusuk"].to_numpy(float), fiyatli, int(deger))


class _Seri(NamedTuple):
    yuk: np.ndarray
    dus: np.ndarray
    kap: np.ndarray
    gunler: np.ndarray  # fiyatlı satırlar
    say: np.ndarray  # fiyatlı mum sayacı: i ile j arası mum = say[j] - say[i]


def _teyit(v: _Seri, t, d, x, c, xi) -> tuple[int | None, str]:
    """S1-V2: t'den sonra ilk düşük <= D günü (t0); öncesinde yüksek > C ya da 100 mum aşılırsa düşer. t0'da düşük <= X ise
    düşer. t0'dan sonraki 5 fiyatlı mumda kapanış > önceki kapanış olan ilk gün tc; tc dahil düşük <= X ya da yüksek > C
    olursa düşer."""
    sonra = v.gunler[v.gunler > t]
    for k, j in enumerate(sonra):
        if v.say[j] - v.say[xi] > EN_UZUN:
            return None, "teyit: 100 mum"
        if v.yuk[j] > c:
            return None, "teyit: dokunuştan önce C aşıldı"
        if v.dus[j] <= d:
            break
    else:
        return None, "teyit: dokunuş yok"
    if v.dus[j] <= x:
        return None, "teyit: dokunuş günü X kırıldı"
    for onceki, j in itertools.pairwise(sonra[k : k + 1 + TEYIT_MUM]):
        if v.dus[j] <= x or v.yuk[j] > c:
            return None, "teyit: teyitten önce bozuldu"
        if v.kap[j] > v.kap[onceki]:
            return int(j), ""
    return None, "teyit: 5 mumda teyit yok"


def _tetik(v: _Seri, t, a: Aday, x, ap, b, c, cp, xi) -> tuple[int | None, float, str]:
    """S1-V5: C'den sonraki ilk mum düşüğü CD/BC >= 1,27 yaparsa tetik (T yok). Tetik C onayından (t) önceyse
    kaçırılmış sayılır. Tetik mumunda CD/BC <= 1,618 + T ve AD/XA 0,786 ± T olmalı; değilse kurulum düşer."""
    esik = c - a.cd[0] * (c - b)
    for j in v.gunler[v.gunler > cp]:
        if j > t and v.yuk[j] > c:
            return None, np.nan, "tetik: C aşıldı"
        if v.say[j] - v.say[xi] > EN_UZUN:
            return None, np.nan, "tetik: 100 mum"
        if v.dus[j] <= esik:
            if j <= t:
                return None, np.nan, "tetik: C onayından önce"
            d = float(v.dus[j])
            if (c - d) / (c - b) <= a.cd[1] + a.T and abs((ap - d) / (ap - x) - D_XA) <= a.T:
                return int(j), d, ""
            return None, np.nan, "tetik: oran dışı"
    return None, np.nan, "tetik: yok"


def sinyaller(gun: pd.DataFrame, a: Aday) -> pd.DataFrame:
    """Adayın günlük sinyal çerçevesi. Sinyal C'nin onay günü (limit), teyit günü ya da tetik günü doğar; o güne kadarki
    veriyle. Dönem ve üyelik süzgeci dışarıda."""
    s = bos_sinyal(gun.index)
    s["D"], s["oruntu_gunu"], s["ust"], s["x_i"] = np.nan, pd.NaT, np.nan, np.nan
    fiyatli = yontem._fiyatli(gun)
    yuk, dus, kap, atr = (gun[c].to_numpy(float) for c in ("yuksek", "dusuk", "kapanis", "atr"))
    v = _Seri(yuk, dus, kap, np.flatnonzero(fiyatli), np.cumsum(fiyatli))
    tarih = gun.index
    huni = s.attrs["huni"] = Counter()
    giris_sutun = s.columns.get_loc("giris")

    def icinde(deger, aralik):
        return aralik[0] - a.T <= deger <= aralik[1] + a.T

    for sira in yapi.ardisik(_pivotlar(gun, a.pivot, fiyatli)):
        if len(sira) < 4:
            continue
        X, A, B, C = sira[-4:]
        x, ap, b, c = X.fiyat, A.fiyat, B.fiyat, C.fiyat
        if (X.tur, A.tur, B.tur, C.tur) != ("D", "T", "D", "T") or not x < b < c < ap:
            continue
        ab, bc = (ap - b) / (ap - x), (c - b) / (ap - b)
        if not (icinde(ab, (AB_XA, AB_XA)) and icinde(bc, a.bc)):
            continue
        d = {"xa786": ap - D_XA * (ap - x), "cb1272": c - S3_CD * (c - b), "mum": np.nan}[a.d]
        if a.d == "xa786" and not icinde((c - d) / (c - b), a.cd):
            continue
        if a.d != "mum" and not x < d < b:
            continue
        huni["desen"] += 1
        t = C.onay_gun
        p = slice(C.pivot_gun + 1, t + 1)
        if (dus[p] <= x).any() or (yuk[p] > c).any():
            huni["onaydan önce X ya da C aşıldı"] += 1
            continue
        if v.say[t] - v.say[X.pivot_gun] > EN_UZUN:
            huni["onayda 100 mum"] += 1
            continue
        gi, neden = t, ""
        if a.giris == "teyit":
            gi, neden = _teyit(v, t, d, x, c, X.pivot_gun)
        elif a.giris == "tetik":
            gi, d, neden = _tetik(v, t, a, x, ap, b, c, C.pivot_gun, X.pivot_gun)
        if gi is None:
            huni[neden] += 1
            continue
        stop = x if a.stop == "X" else d - atr[t]
        h1 = HEDEF[a.hedef](x, ap, c, d, atr[t])
        if not np.isfinite(stop + h1):
            huni["ATR yok"] += 1
            continue
        if a.rr is not None and HEDEF_CD * (c - d) / (d - x) < a.rr:
            huni["R/R reddi"] += 1
            continue
        if s.iat[gi, giris_sutun]:  # aynı gün ikinci kurulum: D'si yüksek olan kalır (gartley.hesapla gibi)
            s.iat[gi, s.columns.get_loc("tekrar")] += 1
            if d <= s["D"].iat[gi]:
                continue
        limit = a.giris == "limit"
        s.loc[tarih[gi], ["giris", "giris_tur", "seviye", "gecerlilik", "stop", "hedef1", "D", "ust", "x_i"]] = [
            True,
            "limit" if limit else "piyasa",
            d if limit else kap[gi],  # piyasada adet sinyal günü kapanışıyla (okumalar 8)
            len(gun) if limit else 1,  # limitin süresi yok; düşme kuralları `_emir_gunu`'nde
            stop,
            h1,
            d,
            c if limit else np.nan,
            X.pivot_gun,
        ]
        s.loc[tarih[gi], "oruntu_gunu"] = tarih[t]
        s.loc[tarih[gi], "kural_durumu"] = (
            ", ".join(f"{ad} {q.fiyat:.4f} ({tarih[q.pivot_gun].date()})" for ad, q in zip("XABC", (X, A, B, C), strict=True))
            + f"; AB/XA {ab:.3f}, BC/AB {bc:.3f}, CD/BC {(c - d) / (c - b):.3f}, D {d:.4f}, sinyal {tarih[gi].date()}"
        )
    return s


# --- Motor ekleri: emir düşme kuralları ve süre çıkışı ---

_EMIR_GUNU = islem._emir_gunu


def _emir_gunu(e, i, g, sayac):
    """Limit emir (yalnız `ust` taşıyan PDF satırları): fiyatlı günde, dolum denetiminden önce, X'ten bu yana 100 mum
    aşıldıysa ya da yüksek > C ise emir düşer (aynı gün dokunuş olsa da). Gerisi motorun limit kuralı."""
    s = e.satir
    if s["giris_tur"] == "limit" and np.isfinite(s.get("ust", np.nan)) and np.isfinite(g.kap[i]):
        xi = int(s["x_i"])
        fiyatli = np.isfinite(g.kap[xi + 1 : i + 1]) & np.isfinite(g.yuk[xi + 1 : i + 1]) & np.isfinite(g.dus[xi + 1 : i + 1])
        if fiyatli.sum() > EN_UZUN:
            sayac[UZUN] += 1
            return None
        if g.yuk[i] > s["ust"]:
            sayac[C_ASILDI] += 1
            return None
    return _EMIR_GUNU(e, i, g, sayac)


islem._emir_gunu = _emir_gunu  # işçi süreçler de bu modülü içe aktarır


def _cikis(a: Aday):
    """para.py `_cikis_kur` (hedef1'de tam çıkış, iz yok, açılış stopu) üstüne S1-V3 süre çıkışı: dolumdan sonra X'ten dolum
    gününe kadarki fiyatlı mum sayısı kadar mum geçince ertesi fiyatlı gün AOF'den çıkış; stop ve hedef açık kalır."""
    cikis, para_gunu = para._cikis_kur(CIKIS)
    if not a.sure:
        return cikis, para_gunu

    def acik_gun(e, i, g, c):
        if para_gunu(e, i, g, c):
            return True
        uzunluk = np.isfinite(g.kap[int(e.satir["x_i"]) + 1 : e.dolum_i + 1]).sum()
        if not e.bekleyen and np.isfinite(g.kap[e.dolum_i + 1 : i + 1]).sum() == uzunluk:
            e.bekleyen = SURE_CIKISI
        return False

    return cikis, acik_gun


# --- İşçi ve koşu ---


def _sembol(arg):
    sembol, gun, adlar, bas, para_da = arg
    piyasa = para.Piyasa({sembol: gun}, [sembol], gun.index)
    disarida = (gun.index < bas) | ~gun["uye"].to_numpy(bool)
    sonuc = []
    for ad in adlar:
        a = ADAYLAR[ad]
        s = sinyaller(gun, a)
        s.loc[disarida, ["giris", "tekrar"]] = [False, 0]
        cikis, acik_gun = _cikis(a)
        islem._acik_gun = acik_gun
        sonuc.append(
            (
                yontem._sinyal_duzeyi(sembol, gun, s, cikis, piyasa, ad, a),
                yontem._motor(sembol, gun, s, cikis, ad) if para_da else [],
                Counter(s.attrs["huni"]),
            )
        )
    return sonuc


def kos(gunler: dict, adlar: list[str], para_da: bool = True, bas: pd.Timestamp = DONEM.bas):
    """Aday başına (sinyal düzeyi tablo, motor işlemleri); motor işlemleri para.py `islemler` sırası ve tekilleştirmesiyle."""
    argl = [(s, gunler[s], adlar, bas, para_da) for s in sorted(gunler)]
    with ProcessPoolExecutor(yontem.ISCI) as havuz:
        parca = list(havuz.map(_sembol, argl, chunksize=4))
    cikti = []
    for j, ad in enumerate(adlar):
        sin = pd.DataFrame([r for p in parca for r in p[j][0]])
        isl = pd.DataFrame([r for p in parca for r in p[j][1]])
        if len(isl):
            isl = isl.sort_values(["dolum_tarihi", "sinyal_tarihi", "sembol", "pivot"], kind="stable")
            isl = isl.drop_duplicates(["sembol", "dolum_tarihi", "seviye"]).reset_index(drop=True)
            isl["pivot"] = ADAYLAR[ad].pivot
        sin.attrs["huni"] = dict(sum((p[j][2] for p in parca), Counter()))
        cikti.append((sin, isl))
    return cikti


def _klasor(ad: str) -> Path:
    k = SONUC / ad
    k.mkdir(parents=True, exist_ok=True)
    return k


def kos_yaz(adlar: list[str], grup: str, on: str | None, para_da: bool = True):
    """Veri yükle, koş, aday başına özet. `on` None ise dosya yazmaz. Dönen: [(özet, günlük kasa ya da None)], günler."""
    t0 = time.time()
    gunler = yontem.veri_yukle(grup)
    cikti = []
    for ad, (sin, isl) in zip(adlar, kos(gunler, adlar, para_da), strict=True):
        o = {"aday": ad, "grup": grup, "sembol": len(gunler), "huni": sin.attrs["huni"], **yontem.sinyal_ozeti(sin)}
        kasa = None
        if para_da:
            o["para"], gun, durum, akis, adet = yontem.para_katmani(isl, gunler)
            kasa = gun["ozkaynak"]
        o["sure_sn"] = round(time.time() - t0, 1)
        if on is not None:
            k = _klasor(f"{on}{ad}-{grup}")
            sin.to_csv(k / "sinyaller.csv", index=False, encoding="utf-8")
            if para_da:
                gun.to_csv(k / "gunluk-kasa.csv", encoding="utf-8", float_format="%.2f")
                isl.assign(
                    durum=[durum.get(i, "") for i in isl.index],
                    adet=[adet.get(i, 0) for i in isl.index],
                    kar_tl=[round(akis[i], 2) if i in adet else None for i in isl.index],
                ).to_csv(k / "islemler.csv", index=False, encoding="utf-8")
            yontem._yaz_json(k / "ozet.json", o)
        cikti.append((o, kasa))
    return cikti, gunler


def _s_defter(o: dict) -> str:
    return (
        f"sinyal {o['sinyal']}, dolum {o['n']}, ort R {o.get('ort_R', float('nan')):.3f}, "
        f"ortanca {o.get('ortanca_R', float('nan')):.3f}, p {o.get('p_tek_yonlu', float('nan')):.4f}"
    )


def _p_defter(p: dict) -> str:
    u = p["uc_parca"]
    return (
        f"son {u['son_kasa_tl']:.2f}, nakit {u['yalniz_nakit_kasasi_tl']:.2f}, fark {u['fark_tl']:.2f}, "
        f"faiz {u['faiz_geliri_tl']:.2f}, işlem kârı {u['islem_kari_tl']:.2f}, "
        f"en iyi 3 hariç {u['en_iyi_uc_olmadan_islem_kari_tl']:.2f}, işlem {p['islem']}"
    )


def _deger(ad: str) -> str:
    a = ADAYLAR[ad]
    return (
        f"pivot {a.pivot}, T {a.T:g}, giriş {a.giris}, D {a.d}, stop {a.stop}, hedef {a.hedef}"
        + (f", R/R >= {a.rr:g}" if a.rr else "")
        + (", süre çıkışı X-dolum mum sayısı" if a.sure else "")
        + f"; emir düşer: düşük <= X, yüksek > C, X'ten {EN_UZUN} mum; aynı gün önce stop; açılış stopu; iz yok"
    )


def calistir_tek(ad: str, para_da: bool):
    ((o, _),), _ = kos_yaz([ad], "ayar", "para-" if para_da else "sinyal-", para_da)
    yontem.deftere_yaz(
        "PDF aile",
        ad,
        f"{'para katmanı' if para_da else 'sinyal düzeyi R'}: {ADAYLAR[ad].kural}",
        _deger(ad) + (", ayar.json boyut ve nakit" if para_da else ""),
        "ayar",
        "ayar grubu: yalnız bilgi ve hata ayıklama",
        _p_defter(o["para"]) if para_da else _s_defter(o),
        "bilgi",
    )
    print(json.dumps(o, ensure_ascii=False, default=str))
    return o


def en_iyi(ozetler: list[dict]) -> str | None:
    """plan-pdf.md "Seçim": en az 30 dolumlu (sinyal düzeyi) adaylar içinde ort R en yüksek; eşitlikte daha az kurallı."""
    aday = [o for o in ozetler if o.get("n", 0) >= yontem.EN_AZ_DOLUM]
    if not aday:
        return None
    sira = list(ADAYLAR)
    return min(aday, key=lambda o: (-o["ort_R"], ADAYLAR[o["aday"]].ek_kural, sira.index(o["aday"])))["aday"]


def _tablo_satiri(o: dict) -> dict:
    u = o["para"]["uc_parca"]
    return {
        "aday": o["aday"],
        "sinyal": o["sinyal"],
        "dolum": o["n"],
        "ort_R": round(o["ort_R"], 3) if o["n"] else None,
        "ortanca_R": round(o["ortanca_R"], 3) if o["n"] else None,
        "p": round(o["p_tek_yonlu"], 4) if o["n"] else None,
        "para_islem": o["para"]["islem"],
        "faiz_geliri": u["faiz_geliri_tl"],
        "islem_kari": u["islem_kari_tl"],
        "en_iyi_uc_olmadan": u["en_iyi_uc_olmadan_islem_kari_tl"],
        "son_kasa": u["son_kasa_tl"],
        "yalniz_nakit": u["yalniz_nakit_kasasi_tl"],
        "fark": u["fark_tl"],
    }


def calistir_aile():
    t0 = time.time()
    adlar = list(ADAYLAR)
    cikti, _ = kos_yaz(adlar, "ayar", "aile-ayar/")
    ozetler = [o for o, _ in cikti]
    tablo = pd.DataFrame([_tablo_satiri(o) for o in ozetler])
    secilen = en_iyi(ozetler)
    k = _klasor("aile-ayar")
    tablo.to_csv(k / "aile.tsv", sep="\t", index=False, encoding="utf-8")
    yontem._yaz_json(
        AILE_OZET,
        {"en_iyi": secilen, "pdf_sha256": KAYNAK_SHA, "kural": "en az 30 dolum, en yüksek sinyal düzeyi ort R; eşitlikte daha az kurallı",
         "tablo": tablo.to_dict("records"), "sure_sn": round(time.time() - t0, 1)},
    )
    yontem.deftere_yaz(
        "PDF aile",
        f"{len(adlar)} deneme",
        "plan-pdf.md aile tablosu, sinyal düzeyi R ve para katmanı",
        "aday başına değerler plan-pdf.md; " + _deger("S1").split("; ", 1)[1],
        "ayar",
        "seçim: en az 30 dolumlu adaylar içinde en yüksek sinyal düzeyi ort R",
        "; ".join(f"{r['aday']} {r['dolum']}/{r['ort_R']}/{r['fark']:.0f}" for r in tablo.to_dict("records"))
        + " (dolum/ort R/fark TL)",
        f"en iyi {secilen}",
    )
    print(tablo.to_string(index=False))
    print(json.dumps({"en_iyi": secilen, "pdf_sha256": KAYNAK_SHA, "sure_sn": round(time.time() - t0, 1)}))


# --- Deflated Sharpe ve PBO ---

_ND = NormalDist()
_EULER = 0.5772156649


def _sharpe(x: np.ndarray) -> np.ndarray:
    """Sütun başına günlük Sharpe; sapması ~0 olan sütun (işlemsiz aday = yalnız nakit) 0."""
    sd = x.std(axis=0, ddof=1)
    return np.where(sd > 1e-12, x.mean(axis=0) / np.where(sd > 1e-12, sd, 1.0), 0.0)


def deflated_sharpe(sr: float, T: int, skew: float, kurt: float, sr_var: float, N: int) -> dict:
    """Bailey ve López de Prado 2014: SR0 = beklenen en büyük SR (N deneme), DSR = Φ((SR - SR0) √(T-1) / payda)."""
    sr0 = math.sqrt(sr_var) * ((1 - _EULER) * _ND.inv_cdf(1 - 1 / N) + _EULER * _ND.inv_cdf(1 - 1 / (N * math.e)))
    payda = math.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr**2)
    return {"N": N, "sr0_gunluk": sr0, "sr0_yillik": sr0 * math.sqrt(252), "dsr": _ND.cdf((sr - sr0) * math.sqrt(T - 1) / payda),
            "psr_sifira_karsi": _ND.cdf(sr * math.sqrt(T - 1) / payda)}


def cscv(X: np.ndarray, S: int = CSCV_S) -> dict:
    """PBO (Bailey ve ark. 2017): S eşit blok (en eski artan günler atılır), C(S, S/2) iç/dış bölme; iç en iyinin dış
    sırasının logiti <= 0 payı."""
    T, N = X.shape
    b = T // S
    bloklar = X[T - b * S :].reshape(S, b, N)
    logit, ic_sr, dis_sr = [], [], []
    for ic in itertools.combinations(range(S), S // 2):
        dis = [j for j in range(S) if j not in ic]
        si, so = _sharpe(bloklar[list(ic)].reshape(-1, N)), _sharpe(bloklar[dis].reshape(-1, N))
        n = int(np.argmax(si))
        sira = (so < so[n]).sum() + 1 + 0.5 * ((so == so[n]).sum() - 1)
        w = sira / (N + 1)
        logit.append(math.log(w / (1 - w)))
        ic_sr.append(si[n])
        dis_sr.append(so[n])
    logit = np.array(logit)
    return {"S": S, "blok_gun": b, "atilan_eski_gun": T - b * S, "bolme": len(logit), "pbo": float((logit <= 0).mean()),
            "logit_ortalama": float(logit.mean()), "logit_ortanca": float(np.median(logit)),
            "ic_en_iyinin_dis_sr_sifir_alti_payi": float((np.array(dis_sr) < 0).mean()),
            "ic_en_iyi_ort_sr_yillik": float(np.mean(ic_sr) * math.sqrt(252)),
            "dis_ort_sr_yillik": float(np.mean(dis_sr) * math.sqrt(252))}


def _nakit_getirisi(gunler: dict) -> pd.Series:
    """`yontem.para_katmani` ile aynı takvim ve faiz: boş nakdin günlük getirisi (kesintili)."""
    xu = para.xu100(gunler)
    takvim = xu.index[(xu.index >= DONEM.bas) & (xu.index <= DONEM.son)]
    onceki = xu.index[xu.index < takvim[0]][-1]
    rf = para.gunluk_faiz(pd.read_parquet(yontem.FAIZ), takvim, onceki)
    return rf * (1 - yontem.AYAR["nakit"]["kesinti"])


def calistir_dsr():
    t0 = time.time()
    adlar = list(ADAYLAR)
    cikti, gunler = kos_yaz(adlar, "ayar", None)
    ozetler = [o for o, _ in cikti]
    E = pd.concat([kasa.rename(o["aday"]) for o, kasa in cikti], axis=1)
    nakit = _nakit_getirisi(gunler)
    assert E.index.equals(nakit.index), "takvim uyuşmuyor"
    X = (E / E.shift(1).fillna(para.SERMAYE)).to_numpy() - 1 - nakit.to_numpy()[:, None]
    T, N = X.shape
    sr = _sharpe(X)
    secilen = en_iyi(ozetler)
    o = {"N": N, "T_gun": T, "donem": [str(E.index[0].date()), str(E.index[-1].date())], "secilen": secilen,
         "sr_yillik": {ad: round(float(v * math.sqrt(252)), 4) for ad, v in zip(adlar, sr, strict=True)},
         "sr_varyans_gunluk": float(np.var(sr, ddof=1)), "pbo": cscv(X)}
    if secilen:
        x = X[:, adlar.index(secilen)]
        m = x - x.mean()
        skew, kurt = float((m**3).mean() / (m**2).mean() ** 1.5), float((m**4).mean() / (m**2).mean() ** 2)
        o["dsr"] = {"secilen_sr_yillik": float(sr[adlar.index(secilen)] * math.sqrt(252)), "carpiklik": skew, "basiklik": kurt,
                    **deflated_sharpe(float(sr[adlar.index(secilen)]), T, skew, kurt, o["sr_varyans_gunluk"], N)}
    o["sure_sn"] = round(time.time() - t0, 1)
    yontem._yaz_json(_klasor("dsr-ayar") / "ozet.json", o)
    d = o.get("dsr", {})
    yontem.deftere_yaz(
        "PDF aile DSR",
        f"{N} deneme",
        "Deflated Sharpe (N = 13) ve PBO (CSCV, S = 16), günlük kasa getirisi eksi yalnız nakit getirisi",
        "para katmanı ayar.json, aday değerleri plan-pdf.md",
        "ayar",
        "bilgi (plan-pdf.md Seçim)",
        f"seçilen {secilen}, SR yıllık {d.get('secilen_sr_yillik', float('nan')):.3f}, DSR {d.get('dsr', float('nan')):.4f}, "
        f"PBO {o['pbo']['pbo']:.3f}",
        "bilgi",
    )
    print(json.dumps(o, ensure_ascii=False, default=str))
    return o


# --- Prova ve sınav ---


def calistir_sinav(ad: str, prova: bool = False):
    """Sınav (ayrık grup) ve prova (ayar grubu) tek gövde; grubu `prova` seçer. Sonuç deftere yazılmadan önce dosyaya."""
    grup, on, etiket = ("ayar", f"prova-{ad}/", "Prova") if prova else ("ayrik", "sinav/", "Sınav")
    ((o, _),), _ = kos_yaz([ad], grup, on)
    g = yontem.gecme(o, o["para"], K_SINAV)
    print(json.dumps({"aday": ad, "grup": grup, "gecme": g}, ensure_ascii=False))
    yontem._yaz_json(_klasor(f"{on}gecme-{ad}-{grup}") / "ozet.json", {"aday": ad, "grup": grup, "pdf_sha256": KAYNAK_SHA, "gecme": g, "ozet": o})
    evet = "EVET" if g["EVET"] else "HAYIR"
    yontem.deftere_yaz(
        f"{etiket} (PDF)",
        ad,
        f"{etiket.lower()}: {ADAYLAR[ad].kural}",
        _deger(ad) + ", ayar.json boyut ve nakit",
        grup,
        f"{'prova (ayar grubu, karar değil): ' if prova else ''}ort R > 0 ve p < 0,05/{K_SINAV}; en iyi 3 hariç işlem kârı > 0; "
        "son kasa > yalnız nakit",
        f"{_s_defter(o)}; {_p_defter(o['para'])}",
        f"prova: {evet}" if prova else evet,
    )


def _aile_en_iyisi() -> str:
    if not AILE_OZET.is_file():
        raise SystemExit(f"aile özeti yok ({AILE_OZET}); önce `aile`")
    o = json.loads(AILE_OZET.read_text(encoding="utf-8"))
    if o.get("pdf_sha256") != KAYNAK_SHA:
        raise SystemExit("aile özeti başka bir pdf.py ile yazılmış; önce `aile`")
    return o["en_iyi"]


def sinav_kapisi(ad: str, sha: str):
    """Veriye dokunmadan önce, sırayla: aday, pdf.py SHA-256'sı, bu adayın kilidi yok, `aile` özeti bu betikten, aday
    Değişiklik 1'in iki adayından biri, girdi özetleri ve deftere yazılabilirlik. Hepsi geçerse kilit
    `open(..., "x")` ile yaratılır (aday başına tek kullanım)."""
    if ad not in ADAYLAR:
        raise SystemExit(f"sınav adayı değil: {ad}")
    if sha != KAYNAK_SHA:
        raise SystemExit(f"pdf.py SHA-256 uyuşmuyor: {sha} != {KAYNAK_SHA}")
    if (KILIT_KLASORU / f"sinav-kilidi-pdf-{ad}.txt").exists():
        raise SystemExit(f"sınav kilidi var ({ad}); ikinci koşu yok")
    secilen = _aile_en_iyisi()
    if ad not in SINAV_ADAYLARI:
        raise SystemExit(f"sınav adayı değil (Değişiklik 1): {ad} (aile en iyisi {secilen})")
    girdiler = yontem.girdi_ozetleri()
    yontem.defter_satirlari()
    kilit = KILIT_KLASORU / f"sinav-kilidi-pdf-{ad}.txt"
    try:
        with open(kilit, "x", encoding="utf-8") as f:
            f.write(json.dumps({"aday": ad, "bas": str(dt.datetime.now()), "pdf_sha256": KAYNAK_SHA,
                                "yontem_sha256": yontem.KAYNAK_SHA, **girdiler}))
    except FileExistsError:
        raise SystemExit(f"sınav kilidi var ({kilit}); ikinci koşu yok") from None
    yontem._SINAV_ACIK = True


def prova_kapisi(ad: str):
    if ad not in ADAYLAR:
        raise SystemExit(f"sınav adayı değil: {ad}")
    yontem.girdi_ozetleri()
    yontem.defter_satirlari()


def ana(argv: list[str]):
    print(f"tansu: {tansu.__file__}")
    mod = argv[0] if argv else ""
    if mod == "kontrol":
        kontrol()
    elif mod in ("sinyal", "para"):
        if len(argv) != 3:
            raise SystemExit(f"kullanım: {mod} <aday> ayar")
        ad, grup = argv[1:]
        if ad not in ADAYLAR:
            raise SystemExit(f"bilinmeyen aday: {ad}")
        if grup != "ayar":
            raise SystemExit(f"{mod} yalnız ayar grubunda koşar (ayrık grup yalnız sınavda): {grup}")
        calistir_tek(ad, mod == "para")
    elif mod == "aile":
        calistir_aile()
    elif mod == "dsr":
        calistir_dsr()
    elif mod == "sinav":
        if len(argv) != 3:
            raise SystemExit("kullanım: sinav <aday> <pdf.py SHA-256>")
        sinav_kapisi(*argv[1:])
        calistir_sinav(argv[1])
    elif mod == "prova":
        if len(argv) != 2:
            raise SystemExit("kullanım: prova <aday> (grup seçilemez; ayar grubunda koşar)")
        prova_kapisi(argv[1])
        calistir_sinav(argv[1], prova=True)
    else:
        raise SystemExit(__doc__)


# --- Kontrol ---

# El örneği tabanı (kapanış; yüksek = kapanış + 0,5, düşük = kapanış - 0,5): X 99,5 (15. gün), A 150,5 (40),
# B 119 (60), C 140,5 (75, güç 7 onayı 82). AB/XA 31,5/51, BC/AB 21,5/31,5, D = 150,5 - 0,786 x 51 = 110,414.
TABAN = ((0, 115), (15, 100), (40, 150), (60, 119.5), (75, 140))
X_, A_, C_, D_ = 99.5, 150.5, 140.5, 110.414
H1_ = D_ + 0.618 * (C_ - D_)  # 129,007148


def _seri(noktalar, ek=(), dusuk=None, yuksek=None) -> pd.DataFrame:
    g = yontem._yapay(yontem._bacak(*noktalar) + list(ek), dusuk=dusuk)
    for i, v in (yuksek or {}).items():
        g.iloc[i, g.columns.get_loc("yuksek")] = g.iloc[i, g.columns.get_loc("ham_yuksek")] = v
    g["atr"] = gostergeler.atr_basit(g["yuksek"], g["dusuk"], g["kapanis"])
    return g


def _tek(gun: pd.DataFrame, ad: str) -> tuple[pd.DataFrame, list[dict]]:
    a = ADAYLAR[ad]
    s = sinyaller(gun, a)
    cikis, acik_gun = _cikis(a)
    islem._acik_gun = acik_gun
    return s, yontem._sinyal_duzeyi("YAPAY", gun, s, cikis, para.Piyasa({"YAPAY": gun}, ["YAPAY"], gun.index), ad, a)


def _gunler(s: pd.DataFrame) -> list[int]:
    return [int(i) for i in np.flatnonzero(s["giris"].to_numpy(bool))]


def _kontrol_pivot():
    y = np.array([1, 2, 3, 5, 3, 2, 1, 2, 5, 5, 2, 1, 0], float)
    d = y - 0.5
    tepe = [p for p in guc_pivotlari(y, d, np.ones(len(y), bool), 2) if p.tur == "T"]
    assert [(p.pivot_gun, p.onay_gun, p.fiyat) for p in tepe] == [(3, 5, 5.0)], tepe
    sag = [p.pivot_gun for p in yapi.sag_bar_pivotlari(pd.Series(y), pd.Series(d), 2) if p.tur == "T"]
    assert 8 in sag, sag  # sag_bar eşitlikte ilkini pivot sayar; güç N saymaz
    f = np.ones(len(y), bool)
    f[4] = False  # fiyatsız satır sayılmaz: onay 2. fiyatlı mum
    tepe = [p for p in guc_pivotlari(y, d, f, 2) if p.tur == "T"]
    assert [(p.pivot_gun, p.onay_gun) for p in tepe] == [(3, 6)], tepe
    print("kontrol 0: güç N pivot katı (eşit yükseklik pivot değil), onay N. fiyatlı mumda")


def _kontrol_el():
    """El örnekleri: beklenen değerler elle (plan formülleri, sabit sayılar)."""
    yakin = np.isclose
    hedef = _seri(TABAN + ((90, 110), (120, 134)))  # D'ye 90. gün iner (düşük 109,5), 0,8 eğimle 134'e çıkar
    s, (r,) = _tek(hedef, "S1")
    assert _gunler(s) == [82] and s["giris_tur"].iat[82] == "limit", _gunler(s)
    assert yakin(s["D"].iat[82], D_) and yakin(s["stop"].iat[82], X_) and yakin(s["hedef1"].iat[82], H1_), s.iloc[82]
    assert r["dolum_tarihi"] == hedef.index[90] and yakin(r["dolum_fiyati"], D_), r
    assert r["cikis_nedeni"] == "hedef1" and r["cikis_tarihi"] == hedef.index[114] and yakin(r["cikis_fiyati"], H1_), r
    assert yakin(r["R_motor"], (H1_ - D_ - (H1_ + D_) * islem.MALIYET) / (D_ - X_)), r["R_motor"]
    print(f"kontrol 2a: S1 sinyal 82, D {D_:.3f}, dolum 90 D'den, hedef1 {H1_:.4f} 114. gün, R motor {r['R_motor']:.4f}")

    _, (r,) = _tek(_seri(TABAN + ((90, 110), (105, 95))), "S1")
    assert r["dolum_tarihi"] == hedef.index[90] and r["cikis_nedeni"] == "stop" and r["cikis_tarihi"] == hedef.index[100]
    assert yakin(r["cikis_fiyati"], X_), r
    print("kontrol 2b: S1 stop X 99,5, 100. gün (düşük 99,5, AOF 99,9 stopun üstünde)")

    s, r = _tek(hedef, "S1-V1")
    assert not _gunler(s) and not r and (0.618 * (C_ - D_) / (D_ - X_)) < 2.0
    print(f"kontrol 2c: S1-V1 R/R {0.618 * (C_ - D_) / (D_ - X_):.3f} < 2,0 reddetti; S1 aynı seriyi aldı")

    g = _seri(TABAN + ((90, 110),), ek=[109, 108, 108.5] + list(np.linspace(109.5, 125, 20)))
    s, (r,) = _tek(g, "S1-V2")
    assert _gunler(s) == [93] and s["giris_tur"].iat[93] == "piyasa" and yakin(s["seviye"].iat[93], 108.5)
    assert yakin(s["D"].iat[93], D_) and yakin(s["stop"].iat[93], X_) and yakin(s["hedef1"].iat[93], H1_)
    assert r["dolum_tarihi"] == g.index[94] and yakin(r["dolum_fiyati"], g["aof"].iat[94]), r
    print(f"kontrol 2d: S1-V2 dokunuş 90, kapanış 108 -> 108,5 teyidi 93, giriş 94 AOF {r['dolum_fiyati']:.2f}")

    g = _seri(TABAN + ((90, 110),), ek=[112.0] * 85)
    _, (r,) = _tek(g, "S1-V3")
    assert r["dolum_tarihi"] == g.index[90] and r["cikis_nedeni"] == SURE_CIKISI and r["cikis_tarihi"] == g.index[166]
    assert yakin(r["cikis_fiyati"], 111.9), r
    _, (r,) = _tek(g, "S1")
    assert r["cikis_nedeni"] == "açık", r
    print("kontrol 2e: S1-V3 X 15 -> dolum 90 = 75 mum; 165. günden sonra 166. gün AOF 111,9 süre çıkışı; S1 açık")

    bc = C_ - 119.0
    g = _seri(TABAN + ((87, 116),), ek=[115, 115, 114.5] + list(np.linspace(115, 125, 10)),
              dusuk={88: C_ - 1.25 * bc, 90: 113.1})
    s, (r,) = _tek(g, "S1-V5")
    assert (C_ - g["dusuk"].iat[88]) / bc == 1.25 and (C_ - 113.1) / bc >= 1.27
    assert _gunler(s) == [90] and yakin(s["D"].iat[90], 113.1) and yakin(s["hedef1"].iat[90], 113.1 + 0.618 * (C_ - 113.1))
    assert r["dolum_tarihi"] == g.index[91] and yakin(r["dolum_fiyati"], 114.9), r
    print(f"kontrol 2f: S1-V5 88. gün CD/BC 1,25 tetik değil; 90. gün {(C_ - 113.1) / bc:.4f} tetik, D 113,1, giriş 91 AOF 114,9")

    s, _ = _tek(hedef, "S2-Z")
    assert _gunler(s) == [82] and yakin(s["D"].iat[82], D_) and yakin(s["hedef1"].iat[82], X_ + 1.27 * (A_ - X_))
    s, _ = _tek(hedef, "S2-V1")
    assert _gunler(s) == [82] and yakin(s["hedef1"].iat[82], D_ + 1.27 * (A_ - D_))
    s, _ = _tek(hedef, "S2-T")
    assert not _gunler(s) and not 1.618 - 0.1 <= (C_ - D_) / bc <= 1.618 + 0.1
    print(f"kontrol 2g: S2-Z hedef X + 1,27 XA = {X_ + 1.27 * (A_ - X_):.2f}; S2-V1 {D_ + 1.27 * (A_ - D_):.4f}; "
          f"S2-T CD/BC {(C_ - D_) / bc:.3f} metin aralığı dışı, sinyal yok")

    d3 = C_ - 1.272 * bc
    s, (r,) = _tek(hedef, "S3")
    assert _gunler(s) == [82] and yakin(s["D"].iat[82], d3) and yakin(s["hedef1"].iat[82], d3 + 2.5 * (d3 - X_))
    assert r["dolum_tarihi"] == hedef.index[89] and yakin(r["dolum_fiyati"], 111.9), r  # 89. gün yüksek 112,5 < D: AOF
    atr = (7 * (0.5 + 20.5 / 15) + 7 * 2.5) / 14  # 69-75 yükseliş TR 0,5 + 1,3667; 76-82 düşüş TR 2,5
    assert yakin(hedef["atr"].iat[82], atr), hedef["atr"].iat[82]
    s, (r,) = _tek(hedef, "S3-A")
    assert yakin(s["stop"].iat[82], d3 - atr) and yakin(s["hedef1"].iat[82], d3 + 2.5 * atr)
    assert r["cikis_nedeni"] == "stop (açılış)" and r["cikis_tarihi"] == hedef.index[90] and yakin(r["cikis_fiyati"], 109.9), r
    print(f"kontrol 2h: S3 D {d3:.3f}, hedef {d3 + 2.5 * (d3 - X_):.3f}, 89. gün boşlukla AOF 111,9 dolum; S3-A ATR {atr:.4f}, "
          f"stop {d3 - atr:.4f}, 90. gün AOF 109,9 açılış stopu")


def _kontrol_iptal():
    s, r = _tek(_seri(TABAN + ((90, 110), (120, 134)), dusuk={78: 99.0}), "S1")
    assert not _gunler(s) and not r, "onaydan önce düşük <= X sinyali düşürmeliydi"
    s, (r,) = _tek(_seri(TABAN + ((90, 110), (120, 134)), yuksek={85: 151.0}), "S1")
    assert _gunler(s) == [82] and r["sonuc"] == C_ASILDI, r
    for gun_, beklenen in ((115, "dolum"), (116, UZUN)):
        g = _seri(TABAN + ((90, 115),), ek=[115.0] * 45, dusuk={gun_: 110.0})
        _, (r,) = _tek(g, "S1")
        assert r["sonuc"] == beklenen, (gun_, r)
        if beklenen == "dolum":
            assert r["dolum_tarihi"] == g.index[115] and np.isclose(r["dolum_fiyati"], D_), r
    print("kontrol 3: emir düşer: C onayından önce düşük <= X (sinyal yok), dolumdan önce yüksek > C, X'ten 101. mum "
          "(100. mumda dolar)")


def _kontrol_kapi():
    """4. Grup kapısı, prova ve sınav kilidi veriye dokunmadan reddeder."""
    global KILIT_KLASORU, AILE_OZET
    eski = yontem.PKL, yontem.GRUPLAR, yontem.FAIZ, KILIT_KLASORU, AILE_OZET
    yontem.PKL = yontem.J / "yok" / "olmayan.pkl"

    def reddet(argv, beklenen):
        try:
            ana(argv)
        except SystemExit as h:
            assert beklenen in str(h), f"{argv}: {h}"
        else:
            raise AssertionError(f"{argv} reddedilmedi")

    try:
        for argv, beklenen in (
            (["sinyal", "S1", "ayrik"], "ayrık grup yalnız sınavda"),
            (["para", "S3", "ayrik"], "ayrık grup yalnız sınavda"),
            (["sinyal", "S9", "ayar"], "bilinmeyen aday"),
            (["sinav", "S1", "0" * 64], "SHA-256 uyuşmuyor"),
            (["sinav", "gt-k", KAYNAK_SHA], "sınav adayı değil"),
            (["sinav", "S1"], "kullanım"),
            (["prova", "S1", "ayrik"], "grup seçilemez"),
            (["prova", "gt-k"], "sınav adayı değil"),
        ):
            reddet(argv, beklenen)
        assert not list(eski[3].glob("sinav-kilidi-pdf-*.txt")), "PDF sınav kilidi var"
        with tempfile.TemporaryDirectory() as td_:
            td = Path(td_)
            KILIT_KLASORU = td / "kilit"
            KILIT_KLASORU.mkdir()
            AILE_OZET = td / "aile.json"
            reddet(["sinav", "S1", KAYNAK_SHA], "aile özeti yok")
            AILE_OZET.write_text(json.dumps({"en_iyi": "S1", "pdf_sha256": "0" * 64}), encoding="utf-8")
            reddet(["sinav", "S1", KAYNAK_SHA], "başka bir pdf.py")
            AILE_OZET.write_text(json.dumps({"en_iyi": "S1", "pdf_sha256": KAYNAK_SHA}), encoding="utf-8")
            reddet(["sinav", "S1", KAYNAK_SHA], "sınav adayı değil")
            AILE_OZET.write_text(json.dumps({"en_iyi": "S2-Z", "pdf_sha256": KAYNAK_SHA}), encoding="utf-8")
            g = pd.read_csv(eski[1], encoding="utf-8")
            a0, b0 = g.index[g["grup"] == "ayar"][0], g.index[g["grup"] == "ayrik"][0]
            g.loc[[a0, b0], "grup"] = ["ayrik", "ayar"]
            yontem.GRUPLAR = td / "gruplar.csv"
            g.to_csv(yontem.GRUPLAR, index=False, encoding="utf-8", lineterminator="\r\n")
            reddet(["sinav", "S2-Z", KAYNAK_SHA], "içeriği değişmiş")
            reddet(["prova", "S1"], "içeriği değişmiş")
            yontem.GRUPLAR = eski[1]
            yontem.FAIZ = td / "faiz.parquet"
            yontem.FAIZ.write_bytes(b"bozuk")
            reddet(["sinav", "S3", KAYNAK_SHA], "faiz dosyası değişmiş")
            yontem.FAIZ = eski[2]
            reddet(["sinav", "S2-Z", KAYNAK_SHA], "dosyası değişmiş")  # veri yolu yok: kilitten önce
            assert not list(KILIT_KLASORU.iterdir()), "reddedilen sınav kilit yarattı"
            for ad in SINAV_ADAYLARI:  # her aday bir kez
                (KILIT_KLASORU / f"sinav-kilidi-pdf-{ad}.txt").write_text("önceki koşu", encoding="utf-8")
                reddet(["sinav", ad, KAYNAK_SHA], "sınav kilidi var")
                (KILIT_KLASORU / f"sinav-kilidi-pdf-{ad}.txt").unlink()
        for grup in ("ayrik", None, "x"):
            try:
                yontem.veri_yukle(grup)
            except SystemExit:
                pass
            else:
                raise AssertionError(f"veri_yukle({grup}) kapısız açtı")
        assert not yontem._SINAV_ACIK
    finally:
        yontem.PKL, yontem.GRUPLAR, yontem.FAIZ, KILIT_KLASORU, AILE_OZET = eski
    print("kontrol 4: grup kapısı, prova, aile en iyisi ve sınav kilidi veriden önce reddediyor; kilit yaratılmadı")


KESIMLER = tuple(pd.Timestamp(t) for t in ("2015-09-15", "2016-07-15", "2017-05-15", "2018-03-15", "2019-11-15", "2021-06-15"))
KESIM_ADAYLARI = ("S1", "S1-V2", "S1-V5", "S2-Z", "S3")


def _kontrol_kesim(gunler: dict):
    """1. İleriye bakma: 6 kesimde veri kesilir ya da kesimden sonrası bozulur. Kesime kadar verilen sinyaller, kesimden
    önce kapanan işlemler ve kesimden önceki günlük kasa aynı kalmalı. Kesik veride açık pozisyon sembolün son fiyatlı
    gününde `açık` kapanır; kasa o günden öncesiyle kıyaslanır."""
    t0 = time.time()
    adlar = list(KESIM_ADAYLARI)
    tam = kos(gunler, adlar)
    kasa = [yontem.para_katmani(isl, gunler)[1]["ozkaynak"] for _, isl in tam]
    rng = np.random.default_rng(20261030)
    for kesim in KESIMLER:
        kesik = {s: t.loc[:kesim] for s, t in gunler.items() if not t.loc[:kesim].empty}
        bozuk = {s: yontem._boz(t, kesim, rng) for s, t in gunler.items()}
        for tur, (veri, donem) in {"kesik": (kesik, para.sinama.Donem(DONEM.bas, kesim)), "bozuk": (bozuk, DONEM)}.items():
            for ad, (sin_t, isl_t), e_t, (sin_v, isl_v) in zip(adlar, tam, kasa, kos(veri, adlar), strict=True):
                kim_t, kim_v = (
                    x.loc[x["sinyal_tarihi"] <= kesim, yontem._KIMLIK].sort_values(["sembol", "sinyal_tarihi"]).reset_index(drop=True)
                    if len(x)
                    else pd.DataFrame(columns=yontem._KIMLIK)
                    for x in (sin_t, sin_v)
                )
                a, b = yontem._kapanmis(sin_t, kesim), yontem._kapanmis(sin_v, kesim)
                c, d = (  # getiri_n, mfe, mae: motorun dolumdan sonraki ölçü sütunları, karar girdisi değil
                    x.drop(columns=[k for k in x.columns if k.startswith(("getiri_", "mfe_", "mae_"))])
                    for x in (yontem._kapanmis(isl_t, kesim), yontem._kapanmis(isl_v, kesim))
                )
                for x, y in ((kim_t, kim_v), (a, b), (c, d)):
                    if len(x) or len(y):
                        pd.testing.assert_frame_equal(x, y, check_exact=True, check_dtype=False)
                sinir = kesim
                if tur == "kesik" and len(isl_v):  # kesimin yarattığı `açık` çıkış: tam koşuda aynı çıkış yok
                    anahtar = ["sembol", "dolum_tarihi", "cikis_tarihi", "cikis_nedeni"]
                    tam_cikis = set(map(tuple, isl_t[anahtar].to_numpy())) if len(isl_t) else set()
                    yeni = [r.cikis_tarihi for r in isl_v[isl_v["cikis_nedeni"] == "açık"].itertuples()
                            if (r.sembol, r.dolum_tarihi, r.cikis_tarihi, r.cikis_nedeni) not in tam_cikis]
                    sinir = min([kesim, *yeni])
                e_v = yontem.para_katmani(isl_v, veri, donem)[1]["ozkaynak"]
                pd.testing.assert_series_equal(e_t[e_t.index < sinir], e_v[e_v.index < sinir], check_exact=True)
                print(
                    f"kontrol 1: {ad} {kesim.date()} {tur}: {len(kim_t)} sinyal, {len(a)} sinyal düzeyi işlem, "
                    f"{len(c)} motor işlemi, {int((e_t.index < sinir).sum())} gün kasa aynı"
                )
    print(f"kontrol 1 bitti ({time.time() - t0:.0f} sn)")


_NOKTA_SINYAL = ["sinyal_tarihi", "oruntu_gunu", "giris_tur", "D", "seviye", "stop", "hedef1", "oruntu", "sonuc"]
_NOKTA_ISLEM = ["dolum_tarihi", "dolum_fiyati", "cikis_tarihi", "cikis_fiyati", "cikis_nedeni", "R"]
_SINYAL_GUNU_REDDI = {islem.UYE_DEGIL, islem.KALITE, islem.STOP_USTTE, islem.HEDEF_YOK, islem.ATR_YOK}


def _sinyal_satirlari(sembol, gun, a, ad, bas) -> tuple[pd.DataFrame, list[dict]]:
    s = sinyaller(gun, a)
    s.loc[(gun.index < bas) | ~gun["uye"].to_numpy(bool), ["giris", "tekrar"]] = [False, 0]
    cikis, acik_gun = _cikis(a)
    islem._acik_gun = acik_gun
    return s, yontem._sinyal_duzeyi(sembol, gun, s, cikis, para.Piyasa({sembol: gun}, [sembol], gun.index), ad, a)


def _limit_karari(gun: pd.DataFrame, satir: pd.Series, t: int) -> tuple[int | None, str]:
    """Limit emrin karar günü, motordan bağımsız: t'den sonraki ilk fiyatlı günde X'ten 100 mum aşıldıysa ya da yüksek > C
    ise düşer; tavan kilidi yokken düşük <= D ise dolar. Hiçbiri yoksa veri sonunda bekler."""
    fiyatli = yontem._fiyatli(gun)
    say = np.cumsum(fiyatli)
    xi = int(satir["x_i"])
    for j in np.flatnonzero(fiyatli[t + 1 :]) + t + 1:
        if say[j] - say[xi] > EN_UZUN:
            return int(j), UZUN
        if gun["yuksek"].iat[j] > satir["ust"]:
            return int(j), C_ASILDI
        if gun["dusuk"].iat[j] <= satir["D"] and not gun["kilit_tavan"].iat[j]:
            return int(j), "dolum"
    return None, islem.VERI_SONU


def _sembol_nokta(arg) -> tuple[Counter, list[str]]:
    """Her sinyal satırı, sembolün verisi kendi karar günlerinde kesilince aynı çıkmalı: sinyal günü (sinyal alanları),
    dolum ya da emrin düştüğü gün (aynı sonuç; bir fiyatlı gün önce hâlâ bekleyen emir), kapanmış işlemde çıkış günü
    (dolum ve çıkış alanları). Limit emrin karar günü `_limit_karari` ile bağımsız bulunur."""
    sembol, gun, adlar, bas = arg
    say, hata = Counter(), []
    tarih = gun.index
    fiyatli_gun = tarih[yontem._fiyatli(gun)]

    def kesik(ad, a, son):
        eslesen = [x for x in _sinyal_satirlari(sembol, gun.loc[:son], a, ad, bas)[1] if x["sinyal_tarihi"] == k["sinyal_tarihi"]]
        return eslesen[0] if len(eslesen) == 1 else {}

    def ayni(x, alan):
        return pd.Series({f: x.get(f) for f in alan}).equals(pd.Series({f: k.get(f) for f in alan}))

    for ad in adlar:
        a = ADAYLAR[ad]
        s, satirlar = _sinyal_satirlari(sembol, gun, a, ad, bas)
        for k in satirlar:
            t = tarih.get_loc(k["sinyal_tarihi"])
            denetim = [(k["sinyal_tarihi"], _NOKTA_SINYAL[:-1], None)]
            karar = None
            if k["sonuc"] == "dolum":
                karar = tarih.get_loc(k["dolum_tarihi"])
                denetim.append((k["dolum_tarihi"], _NOKTA_SINYAL + _NOKTA_ISLEM[:2], None))
                if k["cikis_nedeni"] != "açık":
                    denetim.append((k["cikis_tarihi"], _NOKTA_SINYAL + _NOKTA_ISLEM, None))
            if k["giris_tur"] == "limit" and k["sonuc"] not in _SINYAL_GUNU_REDDI:
                j, beklenen = _limit_karari(gun, s.iloc[t], t)
                if k["sonuc"] != beklenen or (beklenen == "dolum" and j != karar):
                    hata.append(f"{ad} {sembol} {k['sinyal_tarihi'].date()}: sonuç {k['sonuc']}, bağımsız {beklenen} ({j})")
                if j is not None and beklenen != "dolum":
                    karar = j
                    denetim.append((tarih[j], _NOKTA_SINYAL, None))
            if karar is not None:
                once = fiyatli_gun[fiyatli_gun < tarih[karar]][-1]
                denetim.append((once, _NOKTA_SINYAL[:-1], islem.VERI_SONU))
            for son, alan, sonuc in denetim:
                x = kesik(ad, a, son)
                if not (ayni(x, alan) and (sonuc is None or x.get("sonuc") == sonuc)):
                    hata.append(f"{ad} {sembol} {k['sinyal_tarihi'].date()} kesim {son.date()}: {x.get('sonuc')}")
            say[(ad, k["sonuc"] if k["sonuc"] in ("dolum", UZUN, C_ASILDI) else "diğer")] += 1
    return say, hata


def kontrol_nokta(gunler: dict, adlar: list[str], isci: int = yontem.ISCI) -> tuple[Counter, list[str]]:
    argl = [(s, gunler[s], adlar, DONEM.bas) for s in sorted(gunler)]
    if isci <= 1:  # süreç içi (mutasyon sınaması modül yamasını görsün)
        parca = [_sembol_nokta(x) for x in argl]
    else:
        with ProcessPoolExecutor(isci) as havuz:
            parca = list(havuz.map(_sembol_nokta, argl, chunksize=4))
    return sum((p[0] for p in parca), Counter()), [h for p in parca for h in p[1]]


def kontrol():
    _kontrol_kapi()
    _kontrol_pivot()
    _kontrol_el()
    _kontrol_iptal()
    gunler = yontem.veri_yukle("ayar")
    _kontrol_kesim(gunler)
    t0 = time.time()
    say, hata = kontrol_nokta(gunler, list(ADAYLAR))
    assert not hata, hata[:10]
    print(f"kontrol 1b: her sinyal kendi gününde, her kapanmış işlem çıkış gününde kesilen veriyle aynı: "
          f"{dict(sorted(say.items()))} ({time.time() - t0:.0f} sn)")
    print(f"kontrol: hepsi geçti (pdf.py {KAYNAK_SHA})")


if __name__ == "__main__":
    ana(sys.argv[1:])
