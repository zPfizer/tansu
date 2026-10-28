"""Dolum, çıkış, maliyet ve R (SPEC 5.1-5.5). Para ve adet yok: her kurulum kendi başına ölçülür."""

from collections import Counter
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import pandas as pd

KOMISYON, BSMV = 0.0015, 0.05
MALIYET = KOMISYON * (1 + BSMV)  # taraf başına, fiyatın payı (SPEC 5.3)
RISK_TABANI = 0.5  # ATR(14) katı, varsayım (SPEC 5.2)
ILERI_GUNLER = (1, 3, 5, 10)
HEDEFLER = ("hedef1", "hedef2", "hedef3", "hedef4")

# Düşen sinyal nedenleri (SPEC 5.5).
UYE_DEGIL = "BIST 30 üyesi değil"
KALITE = "kalite kuralı (karantina)"
ACIK_VAR = "açık işlem veya bekleyen emir"
STOP_USTTE = "stop girişin altında değil"
HEDEF_YOK = "hedef yok"
SURE_DOLDU = "emir süresi doldu"
STOP_KAPANISI = "dolumdan önce stop altında kapanış"
VERI_SONU = "veri sonunda bekleyen emir"
AYNI_GUN = "aynı gün tekrar"
TAVAN_KILIDI = "üst limit kilidi (piyasa dolumu yok)"

CIKIS_SINYALI = "çıkış sinyali"


@dataclass(frozen=True)
class Cikis:
    """SPEC 5.4 çıkış verisi. Yalnız stop biçimini ve hedef paylarını kurar; `hedef` boşsa motor hedefi yoktur."""

    stop_mod: Literal["dokunus", "kapanis"] = "dokunus"
    hedef: tuple[tuple[str, float], ...] = ()


def maliyet(giris: float, cikis: float) -> float:
    return (giris + cikis) * MALIYET


@dataclass
class _Islem:
    sinyal_i: int
    satir: pd.Series
    stop: float
    risk_tabani: float
    dolum_i: int = -1
    giris: float = np.nan
    risk: float = np.nan
    kalan: float = 1.0
    bekleyen: str | None = None  # ilk kilitsiz günün AOF'sinden çıkış nedeni
    parcalar: list = field(default_factory=list)  # (gün, fiyat, pay, neden)


class _Gun:
    def __init__(self, gun: pd.DataFrame, sinyal: pd.DataFrame):
        self.aof, self.yuk, self.dus, self.kap = (
            gun[a].to_numpy(float) for a in ("aof", "yuksek", "dusuk", "kapanis")
        )
        self.tavan_kilit = gun["kilit_tavan"].to_numpy(bool)
        self.taban_kilit = gun["kilit_taban"].to_numpy(bool)
        self.cikis_sinyali = sinyal["cikis_sinyali"].to_numpy(bool)


def simule(
    gun: pd.DataFrame,
    sinyal: pd.DataFrame,
    cikis: Cikis,
    *,
    sembol: str,
    strateji: str,
    sinif: str,
    risk_tabani: float = RISK_TABANI,
) -> tuple[list[dict], Counter]:
    """Bir sembolün sinyallerini SPEC 5.1 ve 5.4 kurallarıyla işletir.

    `gun`: `veri.gunluk` ve `atr` sütunu. `sinyal`: stratejinin çıktısı, aynı indeks.
    Dönen: işlem kayıtları ve düşen sinyal sayaçları."""
    g = _Gun(gun, sinyal)
    sayac: Counter = Counter()
    sayac[AYNI_GUN] += int(sinyal["tekrar"].sum())
    kayitlar: list[dict] = []
    aktif: _Islem | None = None
    girisler = set(np.flatnonzero(sinyal["giris"].to_numpy(bool)))
    for i in range(len(gun)):
        if aktif is not None and aktif.dolum_i < 0:
            aktif = _emir_gunu(aktif, i, g, sayac)
        if aktif is not None and aktif.dolum_i >= 0 and np.isfinite(g.kap[i]):
            if _acik_gun(aktif, i, g, cikis):
                kayitlar.append(_kayit(aktif, gun, cikis, sembol, strateji, sinif))
                aktif = None
        if i in girisler:
            satir = sinyal.iloc[i]
            neden = _red_nedeni(satir, gun.iloc[i], aktif is not None, cikis)
            if neden:
                sayac[neden] += 1
                continue
            if satir["giris_tur"] not in ("limit", "piyasa"):
                raise ValueError(f"giriş türü henüz yok: {satir['giris_tur']}")
            taban = risk_tabani * float(gun["atr"].iloc[i])
            aktif = _Islem(i, satir, float(satir["stop"]), taban)
    if aktif is not None and aktif.dolum_i >= 0:
        son = int(np.flatnonzero(np.isfinite(g.kap))[-1])
        aktif.parcalar.append((son, g.kap[son], aktif.kalan, "açık"))
        kayitlar.append(_kayit(aktif, gun, cikis, sembol, strateji, sinif))
    elif aktif is not None:
        sayac[VERI_SONU] += 1
    return kayitlar, sayac


def _red_nedeni(satir, gun_satiri, acik_var: bool, cikis: Cikis) -> str | None:
    if not gun_satiri["uye"]:
        return UYE_DEGIL
    if gun_satiri["karantina"]:
        return KALITE
    if acik_var:
        return ACIK_VAR
    referans = (
        satir["seviye"] if satir["giris_tur"] != "piyasa" else gun_satiri["kapanis"]
    )
    if not np.isnan(satir["stop"]) and not satir["stop"] < referans:
        return STOP_USTTE
    if cikis.hedef and all(np.isnan(satir[h]) for h, _ in cikis.hedef):
        return HEDEF_YOK
    return None


def _emir_gunu(e: _Islem, i: int, g: _Gun, sayac: Counter) -> _Islem | None:
    """Bekleyen emir (SPEC 5.1): `limit` t+1'den `gecerlilik` gün; `piyasa` t+1'den sonraki ilk fiyatlı gün."""
    piyasa = e.satir["giris_tur"] == "piyasa"
    if not piyasa and i - e.sinyal_i > int(e.satir["gecerlilik"]):
        sayac[SURE_DOLDU] += 1
        return None
    if not np.isfinite(g.kap[i]) or (piyasa and np.isnan(g.aof[i])):
        return e
    if piyasa:
        if g.tavan_kilit[i]:
            sayac[TAVAN_KILIDI] += 1
            return None
        dolum = g.aof[i]
    else:
        seviye = float(e.satir["seviye"])
        dolum = np.nan
        if not g.tavan_kilit[i]:
            if g.yuk[i] < seviye:
                dolum = g.aof[i]
            elif g.dus[i] <= seviye:
                dolum = seviye
        if np.isnan(dolum):
            if g.kap[i] < e.stop:
                sayac[STOP_KAPANISI] += 1
                return None
            return e
    e.dolum_i, e.giris = i, float(dolum)
    e.risk = np.nan if np.isnan(e.stop) else max(e.giris - e.stop, e.risk_tabani)
    return e


def _kapanis_nedeni(e: _Islem, i: int, g: _Gun, cikis: Cikis) -> str | None:
    """i. günün kapanışından sonra yarın için bekleyen kapanışa bağlı çıkış (SPEC 5.4 adım 6): önce stop, sonra çıkış sinyali."""
    if cikis.stop_mod == "kapanis" and g.kap[i] < e.stop:
        return "stop (kapanış)"
    return CIKIS_SINYALI if g.cikis_sinyali[i] else None


def _acik_gun(e: _Islem, i: int, g: _Gun, cikis: Cikis) -> bool:
    """Açık işlemin bir günü, SPEC 5.4 sırasıyla. İşlem kapanınca True."""
    nedeni = _kapanis_nedeni(e, i, g, cikis)
    dolumda_stop = i == e.dolum_i and e.giris <= e.stop
    if g.taban_kilit[i]:  # satış yok; çıkış ilk kilitsiz güne kalır (adım 1)
        if dolumda_stop:
            e.bekleyen = "stop (dolumda)"
        elif nedeni and e.bekleyen is None:
            e.bekleyen = nedeni
        return False
    if dolumda_stop:
        return _kapat(e, i, e.giris, "stop (dolumda)")
    if i == e.dolum_i:  # dolum günü yalnız stop
        if cikis.stop_mod == "dokunus" and g.dus[i] <= e.stop:
            return _kapat(e, i, e.stop, "stop")
        e.bekleyen = nedeni
        return False
    if e.bekleyen:
        return _kapat(e, i, g.aof[i], e.bekleyen)
    if cikis.stop_mod == "dokunus":
        if g.yuk[i] < e.stop:
            return _kapat(e, i, g.aof[i], "stop")
        if g.dus[i] <= e.stop:
            return _kapat(e, i, e.stop, "stop")
    dolan = {n for _, _, _, n in e.parcalar}
    for ad, pay in cikis.hedef:
        seviye = float(e.satir[ad])
        if ad in dolan or np.isnan(seviye):
            continue
        if g.dus[i] > seviye:
            fiyat = g.aof[i]
        elif g.yuk[i] >= seviye:
            fiyat = seviye
        else:
            break
        pay = min(pay, e.kalan)
        e.kalan -= pay
        e.parcalar.append((i, float(fiyat), pay, ad))
        if e.kalan <= 1e-12:
            return True
    e.bekleyen = nedeni
    return False


def _kapat(e: _Islem, i: int, fiyat: float, neden: str) -> bool:
    e.parcalar.append((i, float(fiyat), e.kalan, neden))
    e.kalan = 0.0
    return True


def _kayit(e: _Islem, gun: pd.DataFrame, cikis: Cikis, sembol, strateji, sinif) -> dict:
    tarih, giris, risk, p = gun.index, e.giris, e.risk, e.parcalar
    r = sum(pay * (f - giris - maliyet(giris, f)) / risk for _, f, pay, _ in p)
    yuzde = sum(pay * (f - giris - maliyet(giris, f)) / giris for _, f, pay, _ in p)
    son_i, son_fiyat, _, son_neden = p[-1]
    kap = gun["kapanis"].to_numpy(float)
    ileri = {
        f"getiri_{n}": (kap[j] - giris - maliyet(giris, kap[j])) / giris * 100
        if (j := e.dolum_i + n) < len(kap)
        else np.nan
        for n in ILERI_GUNLER
    }
    pencere = slice(
        e.dolum_i + 1, e.dolum_i + 11
    )  # dolum günü yüksek/düşük dolumdan önce olabilir
    yuk, dus = (
        gun["yuksek"].to_numpy(float)[pencere],
        gun["dusuk"].to_numpy(float)[pencere],
    )
    tam = e.dolum_i + 10 < len(kap)  # veri sonunda yarım pencere ölçülmez
    mfe = np.nanmax(yuk) - giris if tam and np.isfinite(yuk).any() else np.nan
    mae = giris - np.nanmin(dus) if tam and np.isfinite(dus).any() else np.nan
    s = e.satir
    return {
        "strateji": strateji,
        "sinif": sinif,
        "sembol": sembol,
        "sinyal_tarihi": tarih[e.sinyal_i],
        "giris_tur": s["giris_tur"],
        "seviye": s["seviye"],
        "dolum_tarihi": tarih[e.dolum_i],
        "dolum_fiyati": giris,
        "durum": s["durum"],
        "kural_durumu": s["kural_durumu"],
        "tavan_kapanis": bool(gun["tavan_kapanis"].iloc[e.sinyal_i]),
        "stop": e.stop,
        **{h: s[h] for h in HEDEFLER},
        "kismi": "; ".join(
            f"{tarih[i].date()} {n} {f:.4f} x{pay:g}" for i, f, pay, n in p[:-1]
        ),
        **{
            f"{ad}_gun": next((i - e.dolum_i for i, _, _, n in p if n == ad), np.nan)
            for ad, _ in cikis.hedef
        },
        "stop_gun": son_i - e.dolum_i if son_neden.startswith("stop") else np.nan,
        "cikis_tarihi": tarih[son_i],
        "cikis_fiyati": son_fiyat,
        "cikis_nedeni": son_neden,
        "net_yuzde": yuzde * 100,
        "R": r,
        "tutma_gun": son_i - e.dolum_i,
        **ileri,
        "mfe_yuzde": mfe / giris * 100,
        "mae_yuzde": mae / giris * 100,
        "mfe_R": mfe / risk,
        "mae_R": mae / risk,
        "risk_tabanli": giris - e.stop < e.risk_tabani,
        "dolumda_stop": son_neden == "stop (dolumda)",
        "acik": son_neden == "açık",
    }
