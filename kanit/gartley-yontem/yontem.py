"""Gartley yöntem işi: ön kayıtlı deneyler (`kanit/gartley-yontem/plan.md`, 8304d6d).

Veri şekli: aday başına bir sinyal tablosu (sinyal başına bir satır: sembol, sinyal günü, desen noktaları, D, stop,
hedef1). Tablo iki yere gider: (a) sinyal düzeyi R, her sinyal tek başına, para katmanı yok; (b) motor işlemleri
(`tansu.islem.simule`) ve `kanit/gartley-para/para.py` para katmanı (`portfoy`). Değerler plan.md'den gelir.

Kullanım (PYTHONPATH = worktree kökü):
  yontem.py kontrol                              -> kendi kendine sınamalar (assert); deftere yazmaz
  yontem.py sinyal <aday> ayar                   -> sinyal düzeyi R, ayar grubu, 2015-2022
  yontem.py para <aday> ayar                     -> para katmanı, ayar grubu, 2015-2022
  yontem.py placebo                              -> sahte oran sınaması, 100 çekiliş, ayar grubu
  yontem.py sinav <aday> <yontem.py SHA-256>     -> ayrık grup, aday başına bir kez (kilit dosyası)
  yontem.py prova <aday>                         -> `sinav` ile aynı işlev, ayar grubunda; kilit yok, defterde "Prova" satırı
Adaylar: gartley, gt, gt-teyit, gt-teyit-sure, abcd, geri, gt-k, abcd-k, gartley-kapisiz (yalnız placebo).
`sinav` ve `prova` yalnız gt-k, abcd-k, gartley kabul eder. Ayrık grubu yalnız `sinav` kabul eder.
"""

import datetime as dt
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

import tansu
from tansu import gostergeler, islem, yapi
from tansu.strateji import bos_sinyal
from tansu.stratejiler import gartley

W = Path(__file__).resolve().parents[2]
if not Path(tansu.__file__).resolve().is_relative_to(W):
    raise SystemExit(f"yanlış tansu: {tansu.__file__} (PYTHONPATH={W} olmalı)")

_spec = importlib.util.spec_from_file_location(
    "para", W / "kanit" / "gartley-para" / "para.py"
)
para = importlib.util.module_from_spec(_spec)
sys.modules["para"] = (
    para  # para.islemler'in Pool işçileri `para._sembol`'ü adıyla bulur (kontrol 1)
)
_spec.loader.exec_module(para)

J = Path(tempfile.gettempdir()) / "tansu-gartley-yontem-20261030"
PKL = J / "veri" / "gunler-2014-2025-A.pkl"
PKL_SHA = "0fdd99a7f672247063b1ea32bfee24c8e72c956b0ef202559bec4c55e8f66d66"  # plan.md "Veri ve gruplar"
FAIZ = W.parents[2] / "veri" / "ag" / "20261005-1949" / "faiz.parquet"
FAIZ_SHA = "d1c45da232e620359a317a12e38536824d8f235fac13218a532f576e7d5f9168"  # ayar.json ve para.py ile aynı dosya
# hisse-gruplari.csv İÇERİK özeti: sıralı "sembol,grup" satırları "\n" ile birleşik. plan.md dosya SHA'sı CRLF kopyasından alındı.
GRUP_SHA = "21539588b310723b6a959b8d79e5ede882199d018a87928521954caa16069f40"
KAYNAK_SHA = hashlib.sha256(
    Path(__file__).read_bytes()
).hexdigest()  # içe aktarmada bir kez: bellekteki kodun özeti
GRUPLAR = W / "kanit" / "gartley-yontem" / "hisse-gruplari.csv"
DEFTER = W / "kanit" / "gartley-yontem" / "deneme-defteri.tsv"
AYAR_YOL = W / "kanit" / "gartley-para" / "ayar.json"
KILIT_KLASORU = J
SONUC = J / "sonuc"

AYAR = para.ayar_oku(str(AYAR_YOL))
if hashlib.sha256(AYAR_YOL.read_bytes()).hexdigest() != para.DONDURULMUS_AYAR_SHA:
    raise SystemExit("ayar.json dondurulmuş dosya değil")
DONEM = para.AYAR_DONEMI  # 2015-01-01 - 2022-12-31; 2014 ısınma
P_GARTLEY = {
    "pivot": AYAR["desen"]["pivotlar"][0],
    **{a: AYAR["desen"][a] for a in ("tolerans", "gecerlilik", "stop", "rr_min")},
}
DONMUS_ORAN = (gartley.AB_XA, gartley.D_XA)
KOMISYON = AYAR["maliyet"]["komisyon"]

# plan.md Adım 2-3 ve Adım 1 madde 2; değerler ön kayıttan, ayarlanmaz.
EMIR_GUN = int(AYAR["desen"]["gecerlilik"])  # 20
TEYIT_GUN, RR_KAPI, SURE_GUN, HACIM_N = 10, 1.40, 10, 10
ABCD_Q, ABCD_STOP_ATR, ABCD_HEDEF = (0.382, 0.886), 2.0, 0.618
GERI_SMA, GERI_RSI_N, GERI_RSI_ESIK, GERI_STOP_ATR, GERI_CIKIS_SMA = 200, 2, 10, 2.0, 5
PLACEBO_N, PLACEBO_TOHUM, PLACEBO_AB, PLACEBO_D_FARK, PLACEBO_D_UST, EN_AZ_DOLUM = (
    100,
    20261031,
    (0.45, 0.85),
    0.08,
    0.95,
    30,
)
BOOT_N, BOOT_TOHUM = 10_000, 20261030
SURE_STOPU = "süre stopu"
ISCI = min(24, os.cpu_count() or 1)


class Aday(NamedTuple):
    desen: str  # "gartley" | "abcd" | "geri"
    teyit: bool  # dokunuş + teyit penceresi + ertesi gün AOF girişi
    kapi: bool  # R/R kapısı (tc kapanışı)
    sure: bool  # 10 günlük süre stopu
    adim: str
    kural: str
    rr_kapali: bool = False  # dondurulmuş Gartley'nin kendi R/R kapısı (rr_min) kapalı; yalnız sahte oran sınaması (Değişiklik 1)


ADAYLAR = {
    "gartley": Aday(
        "gartley",
        False,
        False,
        False,
        "Adım 1.3",
        "dondurulmuş Gartley: limit D, stop X, iz 3 ATR, açılış stopu",
    ),
    "gt": Aday(
        "gartley",
        True,
        True,
        True,
        "Adım 2",
        "G-T: dokunuş, 10 gün teyit, R/R >= 1,40, ertesi gün AOF, süre stopu 10",
    ),
    "gt-teyit": Aday(
        "gartley",
        True,
        False,
        False,
        "Adım 2 bilgi",
        "G-T yalnız teyit (kapı ve süre stopu yok)",
    ),
    "gt-teyit-sure": Aday(
        "gartley",
        True,
        False,
        True,
        "Adım 2 bilgi",
        "G-T teyit + süre stopu (kapı yok)",
    ),
    "abcd": Aday(
        "abcd",
        True,
        True,
        True,
        "Adım 3",
        "AB=CD alış: q 0,382-0,886, D = C - AB, stop D - 2 ATR, hedef1 0,618",
    ),
    "geri": Aday(
        "geri",
        False,
        False,
        False,
        "Adım 1.2 geri",
        "kapanış > SMA200 ve RSI(2) < 10; stop giriş - 2 ATR; çıkış kapanış > SMA5",
    ),
    # Değişiklik 1 (plan.md): R/R kapısı kaldırıldı
    "gt-k": Aday(
        "gartley",
        True,
        False,
        True,
        "Değişiklik 1",
        "G-T, R/R kapısı yok: dokunuş, 10 gün teyit, ertesi gün AOF, süre stopu 10",
    ),
    "abcd-k": Aday(
        "abcd",
        True,
        False,
        True,
        "Değişiklik 1",
        "AB=CD alış, R/R kapısı yok: q 0,382-0,886, D = C - AB, stop D - 2 ATR, hedef1 0,618",
    ),
    "gartley-kapisiz": Aday(
        "gartley",
        False,
        False,
        False,
        "Değişiklik 1 placebo",
        "dondurulmuş Gartley, R/R kapısı kapalı",
        rr_kapali=True,
    ),
}
SINAV_ADAYLARI = ("gt-k", "abcd-k", "gartley")
K_SINAV = 3  # plan.md Değişiklik 1 madde 4: üç aday da sayılır; baraj p < 0,05 / 3


class Kurulum(NamedTuple):
    t: int  # desenin bilindiği gün (C onayı)
    D: float
    stop: float
    h1: float
    h2: float
    h3: float
    ust: float  # geçilirse kurulum düşer (AB=CD'de A); Gartley'de yok
    nokta: str


# --- Sinyal tablosu ---


def _fiyatli(gun: pd.DataFrame) -> np.ndarray:
    return (
        gun["kapanis"].notna() & gun["yuksek"].notna() & gun["dusuk"].notna()
    ).to_numpy(bool)


def _teyit_dizisi(gun: pd.DataFrame, fiyatli: np.ndarray) -> np.ndarray:
    """Teyit günü şartı (Adım 2): kapanış > önceki işlem gününün yükseği, RSI(14) > 50, TL hacim > önceki 10 işlem
    gününün ortalaması. Göstergeler yalnız fiyatlı günlerde (ATR gibi eksik gün atlanır)."""
    t = gun[fiyatli]
    teyit = (
        (t["kapanis"] > t["yuksek"].shift(1))
        & (gostergeler.rsi(t["kapanis"], 14) > 50)
        & (t["hacim"] > t["hacim"].rolling(HACIM_N).mean().shift(1))
    )
    return teyit.reindex(gun.index, fill_value=False).to_numpy(bool)


def _gartley_kurulumlari(
    gun: pd.DataFrame, rr_kapali: bool = False
) -> tuple[pd.DataFrame, list[Kurulum]]:
    s = gartley.STRATEJI.sinyal(
        gun, {**P_GARTLEY, "rr_min": "kapali"} if rr_kapali else P_GARTLEY
    )
    kur = [
        Kurulum(
            int(t),
            *(
                float(s[a].iat[t])
                for a in ("seviye", "stop", "hedef1", "hedef2", "hedef3")
            ),
            np.inf,
            s["kural_durumu"].iat[t],
        )
        for t in np.flatnonzero(s["giris"].to_numpy(bool))
    ]
    return s, kur


def _abcd_kurulumlari(gun: pd.DataFrame) -> list[Kurulum]:
    """Adım 3: A tepe, B dip, C tepe (sag_bar_12, onay sırası), C < A, q = BC/AB içinde; D = C - (A - B) < B."""
    atr = gostergeler.atr_basit(gun["yuksek"], gun["dusuk"], gun["kapanis"]).to_numpy()
    tarih = gun.index
    kur = []
    for sira in yapi.ardisik(
        yapi.sag_bar_pivotlari(
            gun["yuksek"], gun["dusuk"], int(P_GARTLEY["pivot"].rsplit("_", 1)[1])
        )
    ):
        if len(sira) < 3:
            continue
        A, B, C = sira[-3:]
        if (A.tur, B.tur, C.tur) != ("T", "D", "T") or not B.fiyat < C.fiyat < A.fiyat:
            continue
        q = (C.fiyat - B.fiyat) / (A.fiyat - B.fiyat)
        d = C.fiyat - (A.fiyat - B.fiyat)
        t = C.onay_gun
        if not (ABCD_Q[0] <= q <= ABCD_Q[1] and d < B.fiyat and np.isfinite(atr[t])):
            continue
        nokta = ", ".join(
            f"{ad} {p.fiyat:.4f} ({tarih[p.pivot_gun].date()})"
            for ad, p in zip("ABC", (A, B, C), strict=True)
        )
        kur.append(
            Kurulum(
                t,
                d,
                d - ABCD_STOP_ATR * atr[t],
                d + ABCD_HEDEF * (A.fiyat - d),
                np.nan,
                np.nan,
                A.fiyat,
                f"{nokta}; q {q:.3f}",
            )
        )
    return kur


def _teyitli(gun: pd.DataFrame, kurulumlar: list[Kurulum], kapi: bool) -> pd.DataFrame:
    """Dokunuş (t0): emir süresinde düşük <= D olan ilk gün. Teyit: t0 dahil 10 işlem günü; teyitten önce (tc günü dahil,
    gün içi düşük kapanıştan önce) düşük <= stop ya da yüksek > üst sınır olursa kurulum düşer. Sinyal tc günü `piyasa`:
    giriş ertesi fiyatlı günün AOF'si; `seviye` = tc kapanışı (adet bununla)."""
    s = bos_sinyal(gun.index)
    s["D"], s["oruntu_gunu"] = np.nan, pd.NaT
    fiyatli = _fiyatli(gun)
    teyit = _teyit_dizisi(gun, fiyatli)
    gunler = np.flatnonzero(fiyatli)
    yuk, dus, kap = (gun[a].to_numpy(float) for a in ("yuksek", "dusuk", "kapanis"))
    tarih = gun.index
    huni = s.attrs["huni"] = Counter(
        kurulum=len(kurulumlar)
    )  # dönem süzgecinden önce, 2014 dahil
    for k in kurulumlar:
        t0 = None
        for j in range(k.t + 1, min(k.t + EMIR_GUN, len(gun) - 1) + 1):
            if not fiyatli[j]:
                continue
            if yuk[j] > k.ust:
                break
            if dus[j] <= k.D:
                t0 = j
                break
        if t0 is None:
            continue
        huni["dokundu"] += 1
        tc = None
        for j in gunler[gunler >= t0][:TEYIT_GUN]:
            if dus[j] <= k.stop or yuk[j] > k.ust:
                huni["teyitten_once_bozuldu"] += 1
                break
            if teyit[j]:
                tc = int(j)
                break
        if tc is None:
            continue
        huni["teyit"] += 1
        if kapi and (k.h1 - kap[tc]) / (kap[tc] - k.stop) < RR_KAPI:
            huni["kapi_reddi"] += 1
            continue
        if s["giris"].iat[
            tc
        ]:  # aynı gün ikinci kurulum: Gartley'deki gibi D'si yüksek olan kalır
            s.iat[tc, s.columns.get_loc("tekrar")] += 1
            if k.D <= s["D"].iat[tc]:
                continue
        s.loc[
            tarih[tc], ["giris", "giris_tur", "seviye", "gecerlilik", "stop", "D"]
        ] = [True, "piyasa", kap[tc], 1, k.stop, k.D]
        s.loc[tarih[tc], ["hedef1", "hedef2", "hedef3"]] = [k.h1, k.h2, k.h3]
        s.loc[tarih[tc], "oruntu_gunu"] = tarih[k.t]
        s.loc[tarih[tc], "kural_durumu"] = (
            f"{k.nokta}; t0 {tarih[t0].date()}, tc {tarih[tc].date()}, D {k.D:.4f}"
        )
    return s


def _geri(gun: pd.DataFrame) -> pd.DataFrame:
    """Adım 1.2 geri çekilme: kapanış > SMA(200) ve RSI(2) < 10 -> ertesi gün AOF alış; stop giriş - 2 ATR(14) (ATR sinyal
    günü); kapanış > SMA(5) -> ertesi gün AOF çıkış (motorun çıkış sinyali)."""
    fiyatli = _fiyatli(gun)
    k = gun.loc[fiyatli, "kapanis"]
    atr = gun["atr"]
    giris = (
        (k > gostergeler.sma(k, GERI_SMA))
        & (gostergeler.rsi(k, GERI_RSI_N) < GERI_RSI_ESIK)
    ).reindex(gun.index, fill_value=False)
    giris &= atr.notna()
    s = bos_sinyal(gun.index)
    s["D"], s["oruntu_gunu"] = np.nan, pd.NaT
    s["stop_atr"] = GERI_STOP_ATR * atr
    s.loc[giris, ["giris", "giris_tur", "gecerlilik"]] = [True, "piyasa", 1]
    s.loc[giris, "seviye"] = gun.loc[giris, "kapanis"]
    s.loc[giris, "stop"] = (
        gun.loc[giris, "kapanis"] - s.loc[giris, "stop_atr"]
    )  # geçici; dolumda giriş - 2 ATR olur
    s["cikis_sinyali"] = (k > gostergeler.sma(k, GERI_CIKIS_SMA)).reindex(
        gun.index, fill_value=False
    )
    return s


def sinyaller(gun: pd.DataFrame, aday: Aday) -> pd.DataFrame:
    """Adayın günlük sinyal çerçevesi (`bos_sinyal` sütunları + D, örüntü günü). Dönem ve üyelik süzgeci dışarıda."""
    if aday.desen == "geri":
        return _geri(gun)
    if aday.desen == "gartley":
        s, kur = _gartley_kurulumlari(gun, aday.rr_kapali)
        if not aday.teyit:
            s["D"], s["oruntu_gunu"] = (
                s["seviye"],
                pd.Series(gun.index, gun.index).where(s["giris"]),
            )
            return s
        return _teyitli(gun, kur, aday.kapi)
    return _teyitli(gun, _abcd_kurulumlari(gun), aday.kapi)


# --- Çıkış: para.py iz stop ve açılış stopu + adayın eki ---


def _cikis(aday: Aday):
    """para.py `_cikis_kur` (iz 3 ATR, açılış stopu) üstüne: geri çekilmede dolum günü stop = giriş - 2 ATR; süre stopunda
    girişten 10 işlem günü sonra o güne kadarki kapanışların hiçbiri hedef1'e ulaşmadıysa ertesi gün AOF'den çıkış."""
    cikis, para_gunu = para._cikis_kur(AYAR["cikis"])

    def acik_gun(e, i, g, c):
        if aday.desen == "geri" and i == e.dolum_i:
            e.stop = e.giris - float(e.satir["stop_atr"])
            e.risk = max(e.giris - e.stop, e.risk_tabani)
        if para_gunu(e, i, g, c):
            return True
        if (
            aday.sure
            and not e.bekleyen
            and np.isfinite(g.kap[e.dolum_i + 1 : i + 1]).sum() == SURE_GUN
        ):
            if np.nanmax(g.kap[e.dolum_i : i + 1]) < float(e.satir["hedef1"]):
                e.bekleyen = SURE_STOPU
        return False

    return cikis, acik_gun


# --- İşçi: sembol başına sinyal düzeyi kayıtlar ve motor işlemleri ---


def _sinyal_duzeyi(sembol, gun, s, cikis, piyasa, aday_adi, aday) -> list[dict]:
    """Her sinyal tek başına (açık işlem kuralı yok, para yok). R = (çıkış - giriş - komisyon ve kayma) / risk; risk motorun
    `max(giriş - stop, 0,5 ATR)`'si. `R_ham` aynı pay / (giriş - stop), giriş > stop iken."""
    g = islem.Gun(gun, s)
    tarih = gun.index
    m = AYAR["maliyet"]
    satirlar = []
    for i in np.flatnonzero(s["giris"].to_numpy(bool)):
        satir = s.iloc[i]
        k = {
            "aday": aday_adi,
            "sembol": sembol,
            "sinyal_tarihi": tarih[i],
            "oruntu_gunu": satir["oruntu_gunu"],
            "giris_tur": satir["giris_tur"],
            "D": satir["D"],
            "seviye": satir["seviye"],
            "stop": satir["stop"],
            "hedef1": satir["hedef1"],
            "oruntu": satir["kural_durumu"],
        }
        neden = islem._red_nedeni(satir, gun.iloc[i], False, cikis)
        if neden:
            satirlar.append({**k, "sonuc": neden})
            continue
        sayac = Counter()
        e, _ = islem.oyna(
            g, int(i), satir, cikis, islem.RISK_TABANI * float(g.atr[i]), sayac
        )
        if e is None:
            satirlar.append({**k, "sonuc": next(iter(sayac))})
            continue
        stop0 = (
            e.giris - float(satir["stop_atr"])
            if aday.desen == "geri"
            else float(satir["stop"])
        )
        alis = (
            e.giris
            * (1 + piyasa.kayma(sembol, tarih[e.dolum_i], e.giris, m))
            * (1 + KOMISYON)
        )
        satis = sum(
            pay * f * (1 - piyasa.kayma(sembol, tarih[j], f, m)) * (1 - KOMISYON)
            for j, f, pay, _ in e.parcalar
        )
        son_i, son_f, _, son_neden = e.parcalar[-1]
        satirlar.append(
            {
                **k,
                "sonuc": "dolum",
                "dolum_tarihi": tarih[e.dolum_i],
                "dolum_fiyati": e.giris,
                "stop_giris": stop0,
                "cikis_tarihi": tarih[son_i],
                "cikis_fiyati": son_f,
                "cikis_nedeni": son_neden,
                "tutma_gun": son_i - e.dolum_i,
                "risk": e.risk,
                "taban_bagladi": bool(e.giris - stop0 < e.risk_tabani),
                "R": (satis - alis) / e.risk,
                "R_ham": (satis - alis) / (e.giris - stop0)
                if e.giris > stop0
                else np.nan,
                "R_motor": islem.sonuc(e).R,
            }
        )
    return satirlar


def _motor(sembol, gun, s, cikis, aday_adi) -> list[dict]:
    """Para katmanının işlem kaydı: para.py `_sembol` ile aynı (motor açık işlem kuralı, boyut için sinyal günkü stop)."""
    kayit, _ = islem.simule(gun, s, cikis, sembol=sembol, strateji=aday_adi, sinif="a")
    for k in kayit:
        k["son_stop"], k["stop"] = k["stop"], s.at[k["sinyal_tarihi"], "stop"]
        taban = islem.RISK_TABANI * gun.at[k["sinyal_tarihi"], "atr"]
        k["risk"] = max(k["dolum_fiyati"] - k["stop"], taban)
        k["risk_emir"] = max(k["seviye"] - k["stop"], taban)
        k["pivot"] = P_GARTLEY["pivot"]
    return kayit


def _sembol(arg):
    sembol, gun, isler, bas, para_da = arg
    piyasa = para.Piyasa({sembol: gun}, [sembol], gun.index)
    disarida = (gun.index < bas) | ~gun["uye"].to_numpy(bool)
    sonuc = []
    for aday_adi, oran in isler:
        gartley.AB_XA, gartley.D_XA = oran
        aday = ADAYLAR[aday_adi]
        s = sinyaller(gun, aday)
        s.loc[disarida, ["giris", "tekrar"]] = [False, 0]
        cikis, acik_gun = _cikis(aday)
        islem._acik_gun = acik_gun
        sonuc.append(
            (
                _sinyal_duzeyi(sembol, gun, s, cikis, piyasa, aday_adi, aday),
                _motor(sembol, gun, s, cikis, aday_adi) if para_da else [],
                Counter(s.attrs.get("huni", {})),
            )
        )
    return sonuc


def kos(
    gunler: dict, isler: list, para_da: bool = True, bas: pd.Timestamp = DONEM.bas
) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """İş başına (sinyal düzeyi tablo, motor işlemleri). Motor işlemleri para.py `islemler` sırası ve tekilleştirmesiyle."""
    if _TUM_ACIK and any(a != "gartley" or o != DONMUS_ORAN for a, o in isler):
        raise SystemExit("bütün semboller yalnız dondurulmuş Gartley içindir")
    argl = [(s, gunler[s], isler, bas, para_da) for s in sorted(gunler)]
    with ProcessPoolExecutor(ISCI) as havuz:
        parca = list(havuz.map(_sembol, argl, chunksize=4))
    cikti = []
    for j in range(len(isler)):
        sin = pd.DataFrame([r for p in parca for r in p[j][0]])
        isl = pd.DataFrame([r for p in parca for r in p[j][1]])
        if len(isl):
            isl = isl.sort_values(
                ["dolum_tarihi", "sinyal_tarihi", "sembol", "pivot"], kind="stable"
            )
            isl = isl.drop_duplicates(["sembol", "dolum_tarihi", "seviye"]).reset_index(
                drop=True
            )
        sin.attrs["huni"] = dict(
            sum((p[j][2] for p in parca), Counter())
        )  # teyitli adaylarda kurulum hunisi
        cikti.append((sin, isl))
    return cikti


# --- Veri ve gruplar ---


_SINAV_ACIK = False
_TUM_ACIK = False  # yalnız `_kontrol_tum_semboller`: bütün semboller ve yalnız dondurulmuş Gartley


def gruplar() -> pd.DataFrame:
    g = pd.read_csv(GRUPLAR, encoding="utf-8")
    sayi = g["grup"].value_counts().to_dict()
    if sayi != {"ayar": 371, "ayrik": 185} or not g["sembol"].is_unique:
        raise SystemExit(f"hisse-gruplari.csv beklenmeyen: {sayi}")
    icerik = hashlib.sha256(
        "\n".join(
            sorted(f"{s},{k}" for s, k in zip(g["sembol"], g["grup"], strict=True))
        ).encode("utf-8")
    ).hexdigest()
    if icerik != GRUP_SHA:
        raise SystemExit(f"hisse-gruplari.csv içeriği değişmiş: {icerik}")
    return g


def girdi_ozetleri() -> dict:
    """Sınav ve prova girdileri: grup listesi (içerik), faiz dosyası, veri dosyası. Uyuşmazlıkta SystemExit. Veriyi yüklemez."""
    gruplar()
    o = {"gruplar_icerik_sha256": GRUP_SHA}
    for ad, yol, beklenen in (("faiz", FAIZ, FAIZ_SHA), ("veri", PKL, PKL_SHA)):
        sha = hashlib.sha256(yol.read_bytes()).hexdigest() if yol.is_file() else None
        if sha != beklenen:
            raise SystemExit(f"{ad} dosyası değişmiş ya da yok: {sha}")
        o[f"{ad}_sha256"] = sha
    return o


def veri_yukle(
    grup: str | None, son: pd.Timestamp = DONEM.son
) -> dict[str, pd.DataFrame]:
    """`grup` None: bütün semboller (yalnız kontrol 0-1, dondurulmuş Gartley). Ayrık grup yalnız sınav kapısından sonra."""
    if grup not in ("ayar", "ayrik", None):
        raise SystemExit(f"bilinmeyen grup: {grup}")
    if grup == "ayrik" and not _SINAV_ACIK:
        raise SystemExit("ayrık grup yalnız sınavda")
    if grup is None and not _TUM_ACIK:
        raise SystemExit("bütün semboller yalnız kontrol 0-1'de (dondurulmuş Gartley)")
    sha = hashlib.sha256(PKL.read_bytes()).hexdigest()
    if sha != PKL_SHA:
        raise SystemExit(f"veri dosyası değişmiş: {sha}")
    _, g = pd.read_pickle(PKL)
    semboller = (
        None if grup is None else set(gruplar().query("grup == @grup")["sembol"])
    )
    return {
        s: t.loc[:son]
        for s, t in g.items()
        if (semboller is None or s in semboller) and not t.loc[:son].empty
    }


# --- Ölçüler ---


def hafta(tarih: pd.Series) -> pd.Series:
    iso = tarih.dt.isocalendar()
    return iso["year"].astype(str) + "-" + iso["week"].astype(str).str.zfill(2)


def istatistik(R: pd.Series, kume: pd.Series) -> dict:
    """n, ortalama, ortanca; tek yönlü p: haftalık kümelerle 10.000 tekrarlı yeniden örneklemede ortalamanın <= 0 payı."""
    if not len(R):
        return {"n": 0}
    kod, _ = pd.factorize(kume)
    top, say = np.bincount(kod, R.to_numpy(float)), np.bincount(kod)
    sec = np.random.default_rng(BOOT_TOHUM).integers(
        0, len(top), size=(BOOT_N, len(top))
    )
    ort = top[sec].sum(axis=1) / say[sec].sum(axis=1)
    return {
        "n": int(len(R)),
        "hafta": int(len(top)),
        "ort_R": float(R.mean()),
        "ortanca_R": float(R.median()),
        "p_tek_yonlu": float((ort <= 0).mean()),
        "ort_R_yuzde_5_95": [
            float(np.quantile(ort, 0.05)),
            float(np.quantile(ort, 0.95)),
        ],
    }


def sinyal_ozeti(sin: pd.DataFrame) -> dict:
    d = sin[sin["sonuc"] == "dolum"] if len(sin) else sin
    o = {
        "sinyal": int(len(sin)),
        "sonuc": dict(Counter(sin["sonuc"])) if len(sin) else {},
    }
    o |= istatistik(d["R"], hafta(d["dolum_tarihi"])) if len(d) else {"n": 0}
    if len(d):
        o["cikis_nedeni"] = dict(Counter(d["cikis_nedeni"]))
        o["taban_bagladi"] = int(d["taban_bagladi"].sum())
        o["ort_R_ham"] = float(d["R_ham"].mean())
        o["ort_R_motor_kaymasiz"] = float(d["R_motor"].mean())
    return o


def para_katmani(isl: pd.DataFrame, gunler: dict, donem=DONEM):
    """para.py `kos` ile aynı sıra; takvim ve BIST 100 yalnız verilen sembollerden. Üç parça + yalnız nakit kasası."""
    xu = para.xu100(gunler)
    takvim = xu.index[(xu.index >= donem.bas) & (xu.index <= donem.son)]
    onceki = xu.index[xu.index < takvim[0]][-1]
    rf = para.gunluk_faiz(pd.read_parquet(FAIZ), takvim, onceki)
    piyasa = para.Piyasa(gunler, isl["sembol"].unique() if len(isl) else [], takvim)
    gun, durum, akis, adet, faiz_top = para.portfoy(isl, piyasa, takvim, rf, AYAR)
    o = para.olc(gun, durum, akis, faiz_top, onceki)
    pnl = pd.Series(
        {k: akis[k] for k, d in durum.items() if d == "alındı"}, dtype=float
    )
    son = float(gun["ozkaynak"].iloc[-1])
    nakit = para.SERMAYE * float((1 + rf * (1 - AYAR["nakit"]["kesinti"])).prod())
    assert abs(para.SERMAYE + faiz_top + pnl.sum() - son) < 1e-6 * son, (
        "kasa = sermaye + faiz + işlem kârı tutmadı"
    )
    o["uc_parca"] = {
        "faiz_geliri_tl": round(faiz_top, 2),
        "islem_kari_tl": round(float(pnl.sum()), 2),
        "en_iyi_uc_olmadan_islem_kari_tl": round(
            float(pnl.sum() - pnl.nlargest(3).sum()), 2
        ),
        "son_kasa_tl": round(son, 2),
        "yalniz_nakit_kasasi_tl": round(nakit, 2),
        "fark_tl": round(son - nakit, 2),
    }
    o["motor"] = {
        "dolum": len(isl),
        "ortalama_R": round(float(isl["R"].mean()), 3) if len(isl) else None,
    }
    return o, gun, durum, akis, adet


# --- Defter ve çıktı ---


def defter_satirlari() -> list[str]:
    satirlar = DEFTER.read_text(encoding="utf-8").splitlines()
    if satirlar[0].split("\t") != [
        "no",
        "tarih",
        "adim",
        "aday",
        "kural",
        "deger",
        "veri",
        "donem",
        "gecme_sarti",
        "sonuc",
        "karar",
    ]:
        raise SystemExit("deneme-defteri.tsv başlığı beklenmeyen")
    return satirlar


def deftere_yaz(adim, aday, kural, deger, grup, gecme, sonuc, karar):
    satirlar = defter_satirlari()
    alanlar = [
        len(satirlar),
        dt.datetime.now().isoformat(timespec="seconds"),
        adim,
        aday,
        kural,
        deger,
        f"gunler-2014-2025-A.pkl {PKL_SHA[:12]}, grup {grup}",
        f"{DONEM.bas.date()} - {DONEM.son.date()}",
        gecme,
        sonuc,
        karar,
    ]
    alanlar = [str(a).replace("\t", " ").replace("\n", " ") for a in alanlar]
    with open(DEFTER, "a", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(alanlar) + "\n")


def _klasor(ad: str) -> Path:
    k = SONUC / ad
    k.mkdir(parents=True, exist_ok=True)
    return k


def _yaz_json(yol: Path, o: dict):
    yol.write_text(
        json.dumps(o, ensure_ascii=False, indent=1, default=str), encoding="utf-8"
    )


def _aday_degeri(aday_adi: str) -> str:
    a = ADAYLAR[aday_adi]
    iz = f"iz {AYAR['cikis']['iz_atr']} ATR, açılış stopu"
    if a.desen == "geri":  # Gartley desen değerleri geri çekilmeye ait değil
        return f"SMA{GERI_SMA}, RSI({GERI_RSI_N}) < {GERI_RSI_ESIK}, stop giriş - {GERI_STOP_ATR:g} ATR(14), çıkış kapanış > SMA{GERI_CIKIS_SMA}, {iz}"
    deger = f"pivot {P_GARTLEY['pivot']}, emir {EMIR_GUN} gün, {iz}"
    if a.rr_kapali:
        deger += ", R/R kapısı kapalı"
    if a.teyit:
        deger += f", teyit {TEYIT_GUN} gün, RSI14>50, hacim>{HACIM_N}g ort"
    if a.kapi:
        deger += f", R/R >= {RR_KAPI}"
    if a.sure:
        deger += f", süre stopu {SURE_GUN} gün"
    return deger


def calistir_sinyal(aday_adi: str, grup: str, defter: bool = True, on: str = ""):
    t0 = time.time()
    gunler = veri_yukle(grup)
    sin, _ = kos(gunler, [(aday_adi, DONMUS_ORAN)], para_da=False)[0]
    o = {
        "aday": aday_adi,
        "grup": grup,
        "sembol": len(gunler),
        "huni": sin.attrs["huni"],
        **sinyal_ozeti(sin),
        "sure_sn": round(time.time() - t0, 1),
    }
    k = _klasor(f"{on}sinyal-{aday_adi}-{grup}")
    sin.to_csv(k / "sinyaller.csv", index=False, encoding="utf-8")
    _yaz_json(k / "ozet.json", o)
    a = ADAYLAR[aday_adi]
    o["defter"] = (
        f"sinyal {o['sinyal']}, dolum {o['n']}, ort R {o.get('ort_R', float('nan')):.3f}, "
        f"ortanca {o.get('ortanca_R', float('nan')):.3f}, p {o.get('p_tek_yonlu', float('nan')):.4f}"
    )
    if defter:
        deftere_yaz(
            a.adim,
            aday_adi,
            f"sinyal düzeyi R: {a.kural}",
            _aday_degeri(aday_adi),
            grup,
            "ayar grubu: yalnız bilgi ve hata ayıklama",
            o["defter"],
            "bilgi",
        )
    print(json.dumps(o, ensure_ascii=False, default=str))
    return o


def calistir_para(aday_adi: str, grup: str, defter: bool = True, on: str = ""):
    t0 = time.time()
    gunler = veri_yukle(grup)
    _, isl = kos(gunler, [(aday_adi, DONMUS_ORAN)], para_da=True)[0]
    o, gun, durum, akis, adet = para_katmani(isl, gunler)
    o = {
        "aday": aday_adi,
        "grup": grup,
        "sembol": len(gunler),
        **o,
        "sure_sn": round(time.time() - t0, 1),
    }
    k = _klasor(f"{on}para-{aday_adi}-{grup}")
    gun.to_csv(k / "gunluk-kasa.csv", encoding="utf-8", float_format="%.2f")
    isl.assign(
        durum=[durum.get(i, "") for i in isl.index],
        adet=[adet.get(i, 0) for i in isl.index],
        kar_tl=[round(akis[i], 2) if i in adet else None for i in isl.index],
    ).to_csv(k / "islemler.csv", index=False, encoding="utf-8")
    _yaz_json(k / "ozet.json", o)
    u = o["uc_parca"]
    o["defter"] = (
        f"son {u['son_kasa_tl']:.2f}, nakit {u['yalniz_nakit_kasasi_tl']:.2f}, fark {u['fark_tl']:.2f}, "
        f"faiz {u['faiz_geliri_tl']:.2f}, işlem kârı {u['islem_kari_tl']:.2f}, "
        f"en iyi 3 hariç {u['en_iyi_uc_olmadan_islem_kari_tl']:.2f}, işlem {o['islem']}"
    )
    a = ADAYLAR[aday_adi]
    if defter:
        deftere_yaz(
            a.adim,
            aday_adi,
            f"para katmanı: {a.kural}",
            _aday_degeri(aday_adi) + ", ayar.json para",
            grup,
            "ayar grubu: yalnız bilgi ve hata ayıklama",
            o["defter"],
            "bilgi",
        )
    print(json.dumps(o, ensure_ascii=False, default=str))
    return o


def gecme(s: dict, p: dict, k: int = K_SINAV) -> dict:
    """plan.md "Sınav ve geçme şartı": üç şart. s = sinyal özeti, p = para özeti (`uc_parca` ile)."""
    u = p["uc_parca"]
    sart = {
        "1_ortR_pozitif_ve_p": bool(
            s.get("n", 0) > 0 and s["ort_R"] > 0 and s["p_tek_yonlu"] < 0.05 / k
        ),
        "2_en_iyi_uc_olmadan_islem_kari_pozitif": u["en_iyi_uc_olmadan_islem_kari_tl"]
        > 0,
        "3_son_kasa_nakit_ustu": u["son_kasa_tl"] > u["yalniz_nakit_kasasi_tl"],
    }
    return {**sart, "k": k, "baraj_p": 0.05 / k, "EVET": all(sart.values())}


def calistir_sinav(aday_adi: str, prova: bool = False):
    """Sınav (ayrık grup) ve prova (ayar grubu) tek gövde: 2015-2022, sinyal düzeyi ve para katmanı, defterde tek satır, geçme
    sonucu k = K_SINAV ile. Grubu `prova` bayrağı seçer; çağıran grup veremez. Sonuç dosyaya, deftere yazılmadan önce yazılır."""
    grup, on, etiket = (
        ("ayar", f"prova-{aday_adi}/", "Prova") if prova else ("ayrik", "", "Sınav")
    )
    s = calistir_sinyal(aday_adi, grup, defter=False, on=on)
    p = calistir_para(aday_adi, grup, defter=False, on=on)
    a = ADAYLAR[aday_adi]
    g = gecme(s, p)
    print(json.dumps({"aday": aday_adi, "grup": grup, "gecme": g}, ensure_ascii=False))
    _yaz_json(
        _klasor(f"{on}gecme-{aday_adi}-{grup}") / "ozet.json",
        {"aday": aday_adi, "grup": grup, "gecme": g, "sinyal": s, "para": p},
    )
    evet = "EVET" if g["EVET"] else "HAYIR"
    deftere_yaz(
        f"{etiket} ({a.adim})",
        aday_adi,
        f"{etiket.lower()}: {a.kural}",
        _aday_degeri(aday_adi) + ", ayar.json para",
        grup,
        f"{'prova (ayar grubu, karar değil): ' if prova else ''}ort R > 0 ve p < 0,05/{K_SINAV}; en iyi 3 hariç işlem kârı > 0; "
        "son kasa > yalnız nakit",
        f"{s['defter']}; {p['defter']}",
        f"prova: {evet}" if prova else evet,
    )


def placebo_cekilisleri() -> list[tuple[float, float]]:
    """Adım 1.2: AB_XA ~ U(0,45; 0,85), sonra D_XA ~ U(AB_XA + 0,08; 0,95); çekiliş başına bu sırayla."""
    rng = np.random.default_rng(PLACEBO_TOHUM)
    cek = []
    for _ in range(PLACEBO_N):
        ab = float(rng.uniform(*PLACEBO_AB))
        cek.append((ab, float(rng.uniform(ab + PLACEBO_D_FARK, PLACEBO_D_UST))))
    return cek


def calistir_placebo():
    t0 = time.time()
    gunler = veri_yukle("ayar")
    cek = placebo_cekilisleri()
    sonuc = kos(
        gunler,
        [("gartley-kapisiz", DONMUS_ORAN)] + [("gartley-kapisiz", c) for c in cek],
        para_da=False,
    )  # Değişiklik 1: kapı hepsinde kapalı
    satir = []
    for no, ((sin, _), (ab, dx)) in enumerate(
        zip(sonuc, [DONMUS_ORAN, *cek], strict=True)
    ):
        d = sin[sin["sonuc"] == "dolum"] if len(sin) else sin
        satir.append(
            {
                "cekilis": no,
                "AB_XA": ab,
                "D_XA": dx,
                "sinyal": len(sin),
                "dolum": len(d),
                "ort_R": float(d["R"].mean()) if len(d) else np.nan,
                "atildi": len(d) < EN_AZ_DOLUM,
            }
        )
    t = pd.DataFrame(satir)
    gartley_R = float(t.at[0, "ort_R"])
    gecerli = t.iloc[1:][~t.iloc[1:]["atildi"]]
    yuzdelik = (
        float((gecerli["ort_R"] < gartley_R).mean() * 100)
        if len(gecerli)
        else float("nan")
    )
    o = {
        "gartley_ort_R": gartley_R,
        "gartley_dolum": int(t.at[0, "dolum"]),
        "cekilis": PLACEBO_N,
        "atilan": int(t.iloc[1:]["atildi"].sum()),
        "gecerli": int(len(gecerli)),
        "gartley_yuzdelik": yuzdelik,
        "atilan_neden": {
            "sinyal_yok": int(((t["sinyal"] == 0) & t["atildi"])[1:].sum()),
            "sinyal_var_dolum_30dan_az": int(
                ((t["sinyal"] > 0) & t["atildi"])[1:].sum()
            ),
        },
        "rr_kapisi": "kapali",
        "gecerli_ort_R_dagilim": gecerli["ort_R"].describe().to_dict()
        if len(gecerli)
        else {},
        "geometri_katkisi": bool(yuzdelik > 95),
        "sure_sn": round(time.time() - t0, 1),
    }
    k = _klasor(
        "placebo-kapisiz-ayar"
    )  # eski kapılı koşunun klasörüne (placebo-gartley-ayar) dokunma
    t.to_csv(k / "cekilisler.csv", index=False, encoding="utf-8")
    _yaz_json(k / "ozet.json", o)
    deftere_yaz(
        "Değişiklik 1 placebo",
        "gartley-kapisiz",
        "sahte oran: AB_XA ~ U(0,45;0,85), D_XA ~ U(AB_XA+0,08;0,95), R/R kapısı bütün çekilişlerde kapalı, diğer kurallar dondurulmuş",
        f"{PLACEBO_N} çekiliş, tohum {PLACEBO_TOHUM}, en az {EN_AZ_DOLUM} dolum, R/R kapısı kapalı",
        "ayar",
        "Gartley ort R çekilişlerin %95'inden yüksek",
        f"çekiliş {PLACEBO_N}, atılan {o['atilan']} ({o['atilan_neden']['sinyal_yok']} sinyalsiz, "
        f"{o['atilan_neden']['sinyal_var_dolum_30dan_az']} dolum<{EN_AZ_DOLUM}), geçerli {o['gecerli']}, "
        f"Gartley ({int(t.at[0, 'dolum'])} dolum) ort R {gartley_R:.3f}, yüzdelik {yuzdelik:.1f}",
        "geometri katkısı var" if o["geometri_katkisi"] else "geometri katkısı yok",
    )
    print(json.dumps(o, ensure_ascii=False, default=str))
    return o


# --- Sınav kapısı ---


def sinav_kapisi(aday_adi: str, sha: str):
    """Veriye dokunmadan önce, sırayla: aday, yontem.py SHA-256'sı, kilit yok, girdi özetleri ve deftere yazılabilirlik. Hepsi
    geçerse kilit `open(..., "x")` ile yaratılır ve girdileri yazılır; sonraki bir hata kilidi silmez (tek kullanım)."""
    global _SINAV_ACIK
    if aday_adi not in SINAV_ADAYLARI:
        raise SystemExit(f"sınav adayı değil: {aday_adi}")
    if sha != KAYNAK_SHA:
        raise SystemExit(f"yontem.py SHA-256 uyuşmuyor: {sha} != {KAYNAK_SHA}")
    kilit = KILIT_KLASORU / f"sinav-kilidi-{aday_adi}.txt"
    if kilit.exists():
        raise SystemExit(f"sınav kilidi var ({kilit}); ikinci koşu yok")
    girdiler = girdi_ozetleri()
    defter_satirlari()
    try:
        with open(kilit, "x", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "aday": aday_adi,
                        "bas": str(dt.datetime.now()),
                        "yontem_sha256": KAYNAK_SHA,
                        **girdiler,
                    }
                )
            )
    except FileExistsError:
        raise SystemExit(f"sınav kilidi var ({kilit}); ikinci koşu yok") from None
    _SINAV_ACIK = True


def prova_kapisi(aday_adi: str):
    """Prova: sınavla aynı aday listesi ve girdi özetleri; kilit yok; ayrık grup açılmaz."""
    if aday_adi not in SINAV_ADAYLARI:
        raise SystemExit(f"sınav adayı değil: {aday_adi}")
    girdi_ozetleri()
    defter_satirlari()


def ana(argv: list[str]):
    print(f"tansu: {tansu.__file__}")
    mod = argv[0] if argv else ""
    if mod == "kontrol":
        kontrol()
    elif mod in ("sinyal", "para"):
        aday_adi, grup = argv[1:3]
        if aday_adi not in ADAYLAR:
            raise SystemExit(f"bilinmeyen aday: {aday_adi}")
        if grup != "ayar":
            raise SystemExit(
                f"{mod} yalnız ayar grubunda koşar (ayrık grup yalnız sınavda): {grup}"
            )
        (calistir_sinyal if mod == "sinyal" else calistir_para)(aday_adi, grup)
    elif mod == "placebo":
        calistir_placebo()
    elif mod == "sinav":
        if len(argv) != 3:
            raise SystemExit("kullanım: sinav <aday> <yontem.py SHA-256>")
        sinav_kapisi(*argv[1:])
        calistir_sinav(argv[1])
    elif mod == "prova":
        if len(argv) != 2:
            raise SystemExit(
                "kullanım: prova <aday> (grup seçilemez; ayar grubunda koşar)"
            )
        prova_kapisi(argv[1])
        calistir_sinav(argv[1], prova=True)
    else:
        raise SystemExit(__doc__)


# --- Kontrol ---


def _yapay(
    kapanis: list[float], dusuk: dict | None = None, hacim: dict | None = None
) -> pd.DataFrame:
    """El örneği verisi: yüksek = kapanış + 0,5, düşük = kapanış - 0,5 (`dusuk` gün başına ezer), AOF = kapanış - 0,1,
    hacim 1000 (`hacim` ezer). Kilit, karantina yok; üye."""
    k = pd.Series(
        kapanis, pd.bdate_range("2016-01-04", periods=len(kapanis)), dtype=float
    )
    g = pd.DataFrame(
        {
            "aof": k - 0.1,
            "yuksek": k + 0.5,
            "dusuk": k - 0.5,
            "kapanis": k,
            "hacim": 1000.0,
        }
    )
    for i, v in (dusuk or {}).items():
        g.iloc[i, g.columns.get_loc("dusuk")] = v
    for i, v in (hacim or {}).items():
        g.iloc[i, g.columns.get_loc("hacim")] = v
    for a in ("yuksek", "dusuk", "kapanis"):
        g[f"ham_{a}"] = g[a]
    for a in ("kilit_tavan", "kilit_taban", "tavan_kapanis", "karantina"):
        g[a] = False
    g["uye"], g["xu100"] = True, 1000.0
    g["atr"] = gostergeler.atr_basit(g["yuksek"], g["dusuk"], g["kapanis"])
    return g


def _bacak(*noktalar) -> list[float]:
    """(gün, kapanış) çapaları arasında doğrusal kapanışlar."""
    k = []
    for (g0, k0), (g1, k1) in zip(noktalar, noktalar[1:], strict=False):
        k += list(np.linspace(k0, k1, g1 - g0 + 1)[:-1])
    return k + [noktalar[-1][1]]


def _kontrol_kapi():
    """4. Grup kapısı, prova ve sınav kilidi veriye dokunmadan reddeder (veri yolu yokken: hata kapının hatası olmalı)."""
    global PKL, KILIT_KLASORU, GRUPLAR, FAIZ, _TUM_ACIK
    eski = PKL, KILIT_KLASORU, GRUPLAR, FAIZ
    PKL = J / "yok" / "olmayan.pkl"

    def reddet(argv, beklenen):
        try:
            ana(argv)
        except SystemExit as h:
            assert beklenen in str(h), f"{argv}: {h}"
        else:
            raise AssertionError(f"{argv} reddedilmedi")

    try:
        for argv, beklenen in (
            (["sinyal", "gt", "ayrik"], "ayrık grup yalnız sınavda"),
            (["para", "abcd", "ayrik"], "ayrık grup yalnız sınavda"),
            (["sinav", "gt-k", "0" * 64], "SHA-256 uyuşmuyor"),
            (["sinav", "abcd-k", "0" * 64], "SHA-256 uyuşmuyor"),
            (["sinav", "gartley", "0" * 64], "SHA-256 uyuşmuyor"),
            (["sinav", "geri", "0" * 64], "sınav adayı değil"),
            (
                ["sinav", "gt", "0" * 64],
                "sınav adayı değil",
            ),  # Değişiklik 1: kapılı gt sınava girmez
            (["sinav", "abcd", "0" * 64], "sınav adayı değil"),
            (["sinav", "gt-k"], "kullanım"),
            (
                ["prova", "gt-k", "ayrik"],
                "grup seçilemez",
            ),  # prova ayrık grubu gösteremez
            (["prova", "geri"], "sınav adayı değil"),
        ):
            reddet(argv, beklenen)
        for ad in SINAV_ADAYLARI:
            assert not (eski[1] / f"sinav-kilidi-{ad}.txt").exists(), (
                "yanlış SHA kilidi yarattı"
            )
        with tempfile.TemporaryDirectory() as td:
            KILIT_KLASORU = Path(td)
            for ad in SINAV_ADAYLARI:
                (KILIT_KLASORU / f"sinav-kilidi-{ad}.txt").write_text(
                    "önceki koşu", encoding="utf-8"
                )
                reddet(["sinav", ad, KAYNAK_SHA], "sınav kilidi var")
            # değişmiş girdiler: doğru SHA ve kilit yok iken de reddeder, kilit yaratılmaz
            yeni = Path(td) / "bozuk"
            yeni.mkdir()
            KILIT_KLASORU = yeni
            g = pd.read_csv(eski[2], encoding="utf-8")
            a0, b0 = g.index[g["grup"] == "ayar"][0], g.index[g["grup"] == "ayrik"][0]
            g.loc[[a0, b0], "grup"] = ["ayrik", "ayar"]  # aynı sayılar, yer değişmiş
            GRUPLAR = Path(td) / "gruplar.csv"
            g.to_csv(GRUPLAR, index=False, encoding="utf-8", lineterminator="\r\n")
            reddet(["sinav", "gt-k", KAYNAK_SHA], "içeriği değişmiş")
            reddet(["prova", "gt-k"], "içeriği değişmiş")
            GRUPLAR = eski[2]
            FAIZ = Path(td) / "faiz.parquet"
            FAIZ.write_bytes(b"bozuk")
            reddet(["sinav", "abcd-k", KAYNAK_SHA], "faiz dosyası değişmiş")
            FAIZ = eski[3]
            reddet(
                ["sinav", "gartley", KAYNAK_SHA], "dosyası değişmiş"
            )  # veri yolu yok: kilitten önce reddeder
            assert not list(yeni.iterdir()), "reddedilen sınav kilit yarattı"
        for kapi in (
            lambda: veri_yukle("ayrik"),
            lambda: veri_yukle(None),
            lambda: veri_yukle("x"),
        ):
            try:
                kapi()
            except SystemExit:
                pass
            else:
                raise AssertionError("veri_yukle kapısız açtı")
        _TUM_ACIK = True
        try:
            for isler in ([("gt-k", DONMUS_ORAN)], [("gartley", (0.5, 0.9))]):
                try:
                    kos({}, isler)
                except SystemExit:
                    pass
                else:
                    raise AssertionError(
                        "bütün semboller dondurulmuş Gartley dışında koşabildi"
                    )
        finally:
            _TUM_ACIK = False
        assert not _SINAV_ACIK
    finally:
        PKL, KILIT_KLASORU, GRUPLAR, FAIZ = eski
    print("kontrol 4: grup kapısı, prova ve sınav kilidi veriden önce reddediyor")


def _gt_ornegi(son_adim: float) -> pd.DataFrame:
    """Gartley: X 99,5 (15. gün), A 150,5 (65), B 118,5 (96), C 135,5 (112, onay 124); C'den sonra 4 günde 100,6'ya iniş,
    düz bekleme, 132-134. günlerde üç `son_adim`lık çıkış; teyit hacmi yalnız 134. günde."""
    k = _bacak(
        (0, 115),
        (15, 100),
        (65, 150),
        (96, 119),
        (112, 135),
        (116, 100.6),
        (131, 100.6),
    )
    for d in [son_adim] * 3 + [0.2, -0.2] * 8:
        k.append(k[-1] + d)
    return _yapay(k, hacim={134: 2000.0})


def _abcd_ornegi(son_adim: float = 1.7) -> pd.DataFrame:
    """AB=CD: A 140,5 (40. gün), B 99,5 (80), C 120,5 (100, onay 112); C'den sonra 4 gün -8,5, sonra dalga; 131. gün
    düşük 79 (t0), 132. gün `son_adim` kadar yükseliş ve hacim 2000 (tc)."""
    k = _bacak((0, 100), (40, 140), (80, 100), (100, 120))
    for d in (
        [-8.5] * 4
        + [0.5, -0.5] * 8
        + [1, -0.3] * 5
        + [-0.3, son_adim]
        + [0.3, -0.2] * 8
    ):
        k.append(k[-1] + d)
    return _yapay(k, dusuk={131: 79.0}, hacim={132: 2000.0})


def _tek_sembol(gun: pd.DataFrame, aday_adi: str) -> tuple[pd.DataFrame, list[dict]]:
    aday = ADAYLAR[aday_adi]
    s = sinyaller(gun, aday)
    cikis, acik_gun = _cikis(aday)
    islem._acik_gun = acik_gun
    return s, _sinyal_duzeyi(
        "YAPAY",
        gun,
        s,
        cikis,
        para.Piyasa({"YAPAY": gun}, ["YAPAY"], gun.index),
        aday_adi,
        aday,
    )


def _kontrol_el():
    """3. El örnekleri: beklenen değerler elle hesaplandı (fonksiyonla değil)."""
    yakin = np.isclose
    gun = _abcd_ornegi()
    assert yakin(gun["atr"].iat[112], 47 / 14), "ATR(onay) = (2x1,5 + 4x9 + 8x1) / 14"
    s, r = _tek_sembol(gun, "abcd")
    assert list(np.flatnonzero(s["giris"])) == [132], np.flatnonzero(s["giris"])
    x = s.iloc[132]
    D, stop, h1 = (
        120.5 - (140.5 - 99.5),
        79.5 - 2 * 47 / 14,
        79.5 + 0.618 * (140.5 - 79.5),
    )
    assert yakin(x["D"], D) and yakin(x["stop"], stop) and yakin(x["hedef1"], h1), x
    assert (
        yakin(x["seviye"], gun["kapanis"].iat[132])
        and x["giris_tur"] == "piyasa"
        and x["oruntu_gunu"] == gun.index[112]
    )
    assert (
        f"t0 {gun.index[131].date()}, tc {gun.index[132].date()}" in x["kural_durumu"]
    ), x["kural_durumu"]
    assert (h1 - gun["kapanis"].iat[132]) / (gun["kapanis"].iat[132] - stop) >= RR_KAPI
    assert r[0]["dolum_tarihi"] == gun.index[133] and yakin(
        r[0]["dolum_fiyati"], gun["aof"].iat[133]
    )
    print(
        f"kontrol 3a: AB=CD D {D:.4f}, stop {stop:.4f}, hedef1 {h1:.4f}, t0 {gun.index[131].date()}, tc {gun.index[132].date()}"
    )

    gun = _abcd_ornegi(
        3.0
    )  # 3d: tc kapanışı 89,2 + 3,0 = 92,2 -> oran (117,198 - 92,2) / (92,2 - 72,7857) = 1,288 < 1,40
    assert (
        yakin(gun["kapanis"].iat[132], 92.2) and (h1 - 92.2) / (92.2 - stop) < RR_KAPI
    )
    s, r = _tek_sembol(gun, "abcd")
    assert not s["giris"].any() and not r, "kapı reddetmeliydi"
    s, r = _tek_sembol(gun, "abcd-k")
    assert (
        list(np.flatnonzero(s["giris"])) == [132]
        and yakin(s["D"].iat[132], D)
        and yakin(s["stop"].iat[132], stop)
    ), np.flatnonzero(s["giris"])
    assert yakin(s["hedef1"].iat[132], h1) and yakin(s["seviye"].iat[132], 92.2)
    assert (
        len(r) == 1
        and r[0]["dolum_tarihi"] == gun.index[133]
        and yakin(r[0]["dolum_fiyati"], gun["aof"].iat[133])
    ), r
    print(
        f"kontrol 3d: AB=CD tc kapanışı 92,2: kapı oranı {(h1 - 92.2) / (92.2 - stop):.3f} < {RR_KAPI}; abcd reddetti, "
        f"abcd-k {gun.index[132].date()} sinyali aldı, giriş {gun.index[133].date()} AOF {r[0]['dolum_fiyati']:.2f}"
    )

    gun = _gt_ornegi(3.27)
    D, X = 150.5 - 0.786 * (150.5 - 99.5), 99.5
    h1 = D + 0.382 * (150.5 - D)
    for ad in ("gt", "gt-teyit-sure", "gt-k"):
        s, r = _tek_sembol(gun, ad)
        assert (
            list(np.flatnonzero(s["giris"])) == [134]
            and yakin(s["D"].iat[134], D)
            and yakin(s["hedef1"].iat[134], h1)
        )
        assert (h1 - gun["kapanis"].iat[134]) / (gun["kapanis"].iat[134] - X) >= RR_KAPI
        (e,) = r
        assert e["dolum_tarihi"] == gun.index[135] and yakin(
            e["dolum_fiyati"], gun["aof"].iat[135]
        ), e
        assert (
            e["cikis_nedeni"] == SURE_STOPU
            and e["cikis_tarihi"] == gun.index[146]
            and yakin(e["cikis_fiyati"], gun["aof"].iat[146])
        ), e
        assert gun["kapanis"].iloc[135:147].max() < h1
    _, (e,) = _tek_sembol(gun, "gt-teyit")
    assert e["cikis_nedeni"] == "açık", e
    print(
        f"kontrol 3b: G-T D {D:.4f}, hedef1 {h1:.4f}, tc {gun.index[134].date()}, giriş {gun.index[135].date()}, "
        f"süre stopu çıkışı {gun.index[146].date()}"
    )

    gun = _gt_ornegi(3.64)
    assert (h1 - gun["kapanis"].iat[134]) / (gun["kapanis"].iat[134] - X) < RR_KAPI
    s, r = _tek_sembol(gun, "gt")
    assert not s["giris"].any() and not r, "kapı reddetmeliydi"
    for ad in ("gt-teyit", "gt-k"):
        s, r = _tek_sembol(gun, ad)
        assert list(np.flatnonzero(s["giris"])) == [134] and len(r) == 1, ad
    print(
        f"kontrol 3c: G-T kapı tc kapanışı {gun['kapanis'].iat[134]:.2f} ile reddetti (oran < {RR_KAPI}); yalnız teyit aynı günü aldı"
    )


def _kontrol_gruplar(hepsi: dict):
    evren = sorted(s for s, t in hepsi.items() if not t.loc[DONEM.bas :].empty)
    assert len(evren) == 556, len(evren)
    ayrik = set(np.random.default_rng(20261030).permutation(evren)[:185])
    g = gruplar()
    assert (
        set(g["sembol"]) == set(evren)
        and set(g.loc[g["grup"] == "ayrik", "sembol"]) == ayrik
    )
    print(
        "kontrol 0: hisse-gruplari.csv = rng(20261030).permutation(556 hisse) ilk 185 ayrık, kalan 371 ayar"
    )


def _kontrol_gartley_para(hepsi: dict, ayar_gunleri: dict):
    """1. Dondurulmuş Gartley, 2015-2022. (a) ayar grubu: motor tablosu bütün-hisse tablosunun ayar satırlarıyla aynı ve kasa
    538.249,28 TL / 38 işlem (defter satır 15). (b) bütün hisseler: para.py işlemleriyle aynı tablo ve 517.830,85 TL / 50 işlem
    (29.10 bilinen sonuç; grup ayrımı basılmaz)."""
    t0 = time.time()
    ((_, isl),) = kos(hepsi, [("gartley", DONMUS_ORAN)])
    with tempfile.TemporaryDirectory() as td:
        referans = para.islemler(str(PKL), AYAR, DONEM, Path(td))
    pd.testing.assert_frame_equal(isl, referans, check_exact=True)
    o, gun, *_ = para_katmani(isl, hepsi)
    son = round(float(gun["ozkaynak"].iloc[-1]), 2)
    assert (
        son == 517830.85 and o["islem"] == 50 and o["en_kotu_dusus_yuzde"] == -12.03
    ), (son, o["islem"], o["en_kotu_dusus_yuzde"])
    ((_, isl_a),) = kos(ayar_gunleri, [("gartley", DONMUS_ORAN)])
    pd.testing.assert_frame_equal(
        isl_a,
        isl[isl["sembol"].isin(ayar_gunleri)].reset_index(drop=True),
        check_exact=True,
    )
    o_a, gun_a, *_ = para_katmani(isl_a, ayar_gunleri)
    son_a = round(float(gun_a["ozkaynak"].iloc[-1]), 2)
    assert son_a == 538249.28 and o_a["islem"] == 38, (son_a, o_a["islem"])
    print(
        f"kontrol 1: ayar grubu kasa {son_a:,.2f} TL, {o_a['islem']} işlem; motor işlemleri para.islemler ile birebir "
        f"({len(isl)} satır); bütün hisseler kasa {son:,.2f} TL, {o['islem']} işlem, düşüş {o['en_kotu_dusus_yuzde']} % "
        f"({time.time() - t0:.0f} sn)"
    )


def _kontrol_tum_semboller(ayar_gunleri: dict):
    """0 ve 1. Bütün semboller yalnız burada ve yalnız dondurulmuş Gartley için açılır (`veri_yukle` ve `kos` bayrağa bakar)."""
    global _TUM_ACIK
    _TUM_ACIK = True
    try:
        hepsi = veri_yukle(None)
        _kontrol_gruplar(hepsi)
        _kontrol_gartley_para(hepsi, ayar_gunleri)
    finally:
        _TUM_ACIK = False


KESIMLER = tuple(
    pd.Timestamp(t) for t in ("2016-07-15", "2018-03-15", "2019-11-15", "2021-06-15")
)
_KIMLIK = [
    "sembol",
    "sinyal_tarihi",
    "oruntu_gunu",
    "giris_tur",
    "D",
    "seviye",
    "stop",
    "hedef1",
    "oruntu",
]


def _boz(t: pd.DataFrame, kesim: pd.Timestamp, rng) -> pd.DataFrame:
    """Kesimden sonraki her hücre bozulur: sayılar U(0,5; 1,5) ile çarpılır, mantıksal sütunlar rastgele."""
    t = t.copy()
    sonra = t.index > kesim
    n = int(sonra.sum())
    for c in t.columns:
        t.loc[sonra, c] = (
            rng.random(n) < 0.5
            if t[c].dtype == bool
            else t.loc[sonra, c] * rng.uniform(0.5, 1.5, n)
        )
    return t


def _kapanmis(t: pd.DataFrame, kesim: pd.Timestamp) -> pd.DataFrame:
    if not len(t):
        return pd.DataFrame()
    if "sonuc" in t:
        t = t[t["sonuc"] == "dolum"]
    t = t[(t["cikis_tarihi"] < kesim) & (t["cikis_nedeni"] != "açık")]
    return t.sort_values(["sembol", "sinyal_tarihi"]).reset_index(drop=True)


def _kontrol_kesim(gunler: dict):
    """2. İleriye bakma: 4 kesim tarihinde veri kesilir ya da kesimden sonrası bozulur. Kesimden önce kapanan her işlem,
    kesime kadar verilen her sinyal ve kesimden önceki günlük kasa aynı kalmalı."""
    t0 = time.time()
    isler = [
        (a, DONMUS_ORAN) for a in ("gt", "gt-teyit-sure", "abcd", "gt-k", "abcd-k")
    ]  # gt-k ve abcd-k: kapısız, çok sinyalli yol
    tam = kos(gunler, isler)
    kasa = [para_katmani(isl, gunler)[1]["ozkaynak"] for _, isl in tam]
    rng = np.random.default_rng(20261030)
    for kesim in KESIMLER:
        kesik = {s: t.loc[:kesim] for s, t in gunler.items() if not t.loc[:kesim].empty}
        bozuk = {s: _boz(t, kesim, rng) for s, t in gunler.items()}
        for ad, (veri, donem) in {
            "kesik": (kesik, para.sinama.Donem(DONEM.bas, kesim)),
            "bozuk": (bozuk, DONEM),
        }.items():
            for (aday_adi, _), (sin_t, isl_t), e_t, (sin_v, isl_v) in zip(
                isler, tam, kasa, kos(veri, isler), strict=True
            ):
                kim_t, kim_v = (
                    x.loc[x["sinyal_tarihi"] <= kesim, _KIMLIK]
                    .sort_values(["sembol", "sinyal_tarihi"])
                    .reset_index(drop=True)
                    if len(x)
                    else pd.DataFrame(columns=_KIMLIK)
                    for x in (sin_t, sin_v)
                )
                a, b = _kapanmis(sin_t, kesim), _kapanmis(sin_v, kesim)
                c, d = _kapanmis(isl_t, kesim), _kapanmis(isl_v, kesim)
                for x, y in ((kim_t, kim_v), (a, b), (c, d)):
                    if len(x) or len(y):
                        pd.testing.assert_frame_equal(
                            x, y, check_exact=True, check_dtype=False
                        )
                e_v = para_katmani(isl_v, veri, donem)[1]["ozkaynak"]
                pd.testing.assert_series_equal(
                    e_t[e_t.index < kesim], e_v[e_v.index < kesim], check_exact=True
                )
                print(
                    f"kontrol 2: {aday_adi} {kesim.date()} {ad}: {len(kim_t)} sinyal, {len(a)} sinyal düzeyi işlem, "
                    f"{len(c)} motor işlemi, {int((e_t.index < kesim).sum())} gün kasa aynı"
                )
    print(f"kontrol 2 bitti ({time.time() - t0:.0f} sn)")


def _kontrol_degisiklik1(ayar_gunleri: dict):
    """5. Değişiklik 1: kapı kapalı placebo kolu gerçek Gartley'yi değiştirmez; gt-k = gt-teyit-sure; gecme() elle örnekler."""
    isler = [
        (a, DONMUS_ORAN)
        for a in ("gartley", "gartley-kapisiz", "gt-teyit-sure", "gt-k")
    ]
    (g, _), (gk, _), (ts, _), (tk, _) = kos(ayar_gunleri, isler, para_da=False)
    pd.testing.assert_frame_equal(
        g.drop(columns="aday"), gk.drop(columns="aday"), check_exact=True
    )
    pd.testing.assert_frame_equal(
        ts.drop(columns="aday"), tk.drop(columns="aday"), check_exact=True
    )
    d = g[g["sonuc"] == "dolum"]
    assert len(g) == 231 and len(d) == 39 and round(float(d["R"].mean()), 3) == 1.129, (
        len(g),
        len(d),
        d["R"].mean(),
    )
    s1 = {"n": 5, "ort_R": 0.4, "p_tek_yonlu": 0.0166}
    p1 = {
        "uc_parca": {
            "en_iyi_uc_olmadan_islem_kari_tl": 1.0,
            "son_kasa_tl": 11.0,
            "yalniz_nakit_kasasi_tl": 10.0,
        }
    }
    assert gecme(s1, p1)["EVET"] and gecme(s1, p1, 1)["EVET"]
    assert (
        not gecme({**s1, "p_tek_yonlu": 0.0168}, p1)["EVET"]
        and gecme({**s1, "p_tek_yonlu": 0.0168}, p1, 1)["EVET"]
    )  # k = 3 barajı 0,0167
    assert (
        not gecme({"n": 0}, p1)["EVET"] and not gecme({**s1, "ort_R": -0.1}, p1)["EVET"]
    )
    assert not gecme(
        s1, {"uc_parca": {**p1["uc_parca"], "en_iyi_uc_olmadan_islem_kari_tl": 0.0}}
    )["EVET"]
    assert not gecme(s1, {"uc_parca": {**p1["uc_parca"], "son_kasa_tl": 10.0}})["EVET"]
    print(
        f"kontrol 5: gartley-kapisiz = gartley (tablo birebir; {len(g)} sinyal, {len(d)} dolum, ort R {d['R'].mean():.3f}); "
        f"gt-k = gt-teyit-sure ({len(ts)} sinyal); gecme() örnekleri geçti"
    )


def kontrol():
    _kontrol_kapi()
    _kontrol_el()
    ayar_gunleri = veri_yukle("ayar")
    _kontrol_tum_semboller(ayar_gunleri)
    _kontrol_degisiklik1(ayar_gunleri)
    _kontrol_kesim(ayar_gunleri)
    print("kontrol: hepsi geçti")


if __name__ == "__main__":
    ana(sys.argv[1:])
