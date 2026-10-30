"""Dolum, çıkış, maliyet ve R (SPEC 5.1-5.5). Para ve adet yok: her kurulum kendi başına ölçülür."""

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, NamedTuple

import numpy as np
import pandas as pd

KOMISYON, BSMV = 0.0015, 0.05
MALIYET = KOMISYON * (1 + BSMV)  # taraf başına, fiyatın payı (SPEC 5.3)
RISK_TABANI = 0.5  # ATR(14) katı, varsayım (SPEC 5.2)
ILERI_GUNLER = (1, 3, 5, 10)
HEDEFLER = ("hedef1", "hedef2", "hedef3", "hedef4")

# Düşen sinyal nedenleri (SPEC 5.5).
KALITE = "kalite kuralı (karantina)"
ACIK_VAR = "açık işlem veya bekleyen emir"
STOP_USTTE = "stop girişin altında değil"
HEDEF_YOK = "hedef yok"
SURE_DOLDU = "emir süresi doldu"
STOP_KAPANISI = "dolumdan önce stop altında kapanış"
VERI_SONU = "veri sonunda bekleyen emir"
AYNI_GUN = "aynı gün tekrar"
TAVAN_KILIDI = "üst limit kilidi (piyasa dolumu yok)"
ATR_YOK = "ATR tanımsız (risk tabanı yok)"

CIKIS_SINYALI = "çıkış sinyali"


@dataclass(frozen=True)
class Cikis:
    """SPEC 5.4 çıkış verisi. Yalnız stop biçimini ve hedef paylarını kurar; `hedef` boşsa motor hedefi yoktur."""

    stop_mod: Literal["dokunus", "kapanis"] = "dokunus"
    hedef: tuple[tuple[str, float], ...] = ()


class Sonuc(NamedTuple):
    """Alan adları işlem kaydının sütunlarıdır; `Strateji.olcu` birini seçer."""

    R: float
    net_yuzde: float


def maliyet(giris: float, cikis: float) -> float:
    return (giris + cikis) * MALIYET


@dataclass
class _Islem:
    sinyal_i: int
    satir: Mapping
    stop: float
    risk_tabani: float
    dolum_i: int = -1
    giris: float = np.nan
    risk: float = np.nan
    kalan: float = 1.0
    bekleyen: str | None = None  # ilk kilitsiz günün AOF'sinden çıkış nedeni
    parcalar: list = field(default_factory=list)  # (gün, fiyat, pay, neden)


class Gun:
    """Bir sembolün motor dizileri; sembol başına bir kez kurulur."""

    def __init__(self, gun: pd.DataFrame, sinyal: pd.DataFrame):
        self.tarih = gun.index
        self.aof, self.yuk, self.dus, self.kap, self.atr = (
            gun[a].to_numpy(float) for a in ("aof", "yuksek", "dusuk", "kapanis", "atr")
        )
        self.tavan_kilit = gun["kilit_tavan"].to_numpy(bool)
        self.taban_kilit = gun["kilit_taban"].to_numpy(bool)
        self.tavan_kapanis = gun["tavan_kapanis"].to_numpy(bool)
        self._uye = gun["uye"].to_numpy(bool)
        self._karantina = gun["karantina"].to_numpy(bool)
        self.cikis_sinyali = sinyal["cikis_sinyali"].to_numpy(bool)

    @cached_property
    def dolum_gunu(self) -> np.ndarray:
        """t'den sonraki ilk fiyatlı gün (sonlu kapanış ve AOF var), yoksa len(kap)."""
        yok = len(self.kap)
        fiyatli = np.append(
            np.flatnonzero(np.isfinite(self.kap) & ~np.isnan(self.aof)), yok
        )
        return fiyatli[np.searchsorted(fiyatli, np.arange(yok), side="right")]

    @cached_property
    def uygun(self) -> np.ndarray:
        """t rastgele `piyasa` sinyal günü olabilir mi (SPEC 5.8 madde 3)."""
        kilit = np.append(self.tavan_kilit, True)
        return self._uye & ~self._karantina & (self.atr > 0) & ~kilit[self.dolum_gunu]


def simule(
    gun: pd.DataFrame,
    sinyal: pd.DataFrame,
    cikis: Cikis,
    *,
    sembol: str,
    strateji: str,
    sinif: str,
) -> tuple[list[dict], Counter]:
    """Bir sembolün sinyallerini SPEC 5.1 ve 5.4 kurallarıyla işletir.

    `gun`: `veri.gunluk` ve `atr` sütunu. `sinyal`: stratejinin çıktısı, aynı indeks;
    evren ve dönem dışındaki günlerde `giris` ile `tekrar`ı çağıran temizler (`sinama.calistir` yapar).
    Dönen: işlem kayıtları ve düşen sinyal sayaçları."""
    g = Gun(gun, sinyal)
    sayac: Counter = Counter()
    sayac[AYNI_GUN] += int(sinyal["tekrar"].sum())
    kayitlar: list[dict] = []
    serbest_gun = -1
    for i in np.flatnonzero(sinyal["giris"].to_numpy(bool)):
        satir = sinyal.iloc[i]
        neden = _red_nedeni(satir, gun.iloc[i], i < serbest_gun, cikis)
        if neden:
            sayac[neden] += 1
            continue
        if satir["giris_tur"] not in ("limit", "piyasa"):
            raise ValueError(f"giriş türü henüz yok: {satir['giris_tur']}")
        e, serbest_gun = oyna(
            g, int(i), satir, cikis, RISK_TABANI * float(g.atr[i]), sayac
        )
        if e is not None:
            kayitlar.append(_kayit(e, g, cikis, sembol, strateji, sinif))
    return kayitlar, sayac


def oyna(
    g: Gun, i: int, satir: Mapping, cikis: Cikis, taban: float, sayac: Counter
) -> tuple[_Islem | None, int]:
    """i. gün sinyal veren tek kurulumu i+1'den kapanana, emir düşene ya da veri bitene dek işletir.

    Dönen: dolan işlem (yoksa None) ve son gün; veri biterse `len(g.kap)`, yani sonraki her sinyali kapatır.
    Veri sonunda açık işlem son fiyatlı kapanışta `açık` işaretlenir (SPEC 5.4)."""
    e: _Islem | None = _Islem(i, satir, float(satir["stop"]), taban)
    for j in range(i + 1, len(g.kap)):
        e = _emir_gunu(e, j, g, sayac)
        if e is None:
            return None, j
        if e.dolum_i >= 0:
            return _tut(e, g, cikis)
    sayac[VERI_SONU] += 1
    return None, len(g.kap)


def _tut(e: _Islem, g: Gun, cikis: Cikis) -> tuple[_Islem, int]:
    n = len(g.kap)
    for j in range(e.dolum_i, n):
        if np.isfinite(g.kap[j]) and _acik_gun(e, j, g, cikis):
            return e, j
    son = int(np.flatnonzero(np.isfinite(g.kap))[-1])
    e.parcalar.append((son, g.kap[son], e.kalan, "açık"))
    return e, n


def _red_nedeni(satir, gun_satiri, acik_var: bool, cikis: Cikis) -> str | None:
    if gun_satiri["karantina"]:
        return KALITE
    if acik_var:
        return ACIK_VAR
    referans = (
        satir["seviye"] if satir["giris_tur"] != "piyasa" else gun_satiri["kapanis"]
    )
    if not np.isnan(satir["stop"]) and not satir["stop"] < referans:
        return STOP_USTTE
    # SPEC 5.2 taban: ATR NaN ya da 0 ise risk tabanı yoktur.
    if not np.isnan(satir["stop"]) and not gun_satiri["atr"] > 0:
        return ATR_YOK
    if cikis.hedef and all(np.isnan(satir[h]) for h, _ in cikis.hedef):
        return HEDEF_YOK
    return None


def _emir_gunu(e: _Islem, i: int, g: Gun, sayac: Counter) -> _Islem | None:
    """Bekleyen emir (SPEC 5.1): `limit` t+1'den `gecerlilik` gün; `piyasa` t+1'den sonraki ilk fiyatlı gün."""
    piyasa = e.satir["giris_tur"] == "piyasa"
    if not piyasa and i - e.sinyal_i > int(e.satir["gecerlilik"]):
        sayac[SURE_DOLDU] += 1
        return None
    if piyasa:
        if i < g.dolum_gunu[e.sinyal_i]:
            return e
        if g.tavan_kilit[i]:
            sayac[TAVAN_KILIDI] += 1
            return None
        dolum = g.aof[i]
    else:
        if not np.isfinite(g.kap[i]):
            return e
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
    return _doldur(e, i, dolum)


def _doldur(e: _Islem, i: int, fiyat: float) -> _Islem:
    e.dolum_i, e.giris = i, float(fiyat)
    e.risk = np.nan if np.isnan(e.stop) else max(e.giris - e.stop, e.risk_tabani)
    return e


def sablonlar(kurulumlar: pd.DataFrame, atr: np.ndarray) -> np.ndarray:
    """(m, 5) ATR katı uzaklıklar [stop, hedef1..hedef4], satır sırasıyla; `atr` satırların sinyal günü ATR'si. NaN hedef = yok."""
    dolum = kurulumlar["dolum_fiyati"].to_numpy(float)
    return np.column_stack(
        [
            (dolum - kurulumlar["stop"].to_numpy(float)) / atr,
            *((kurulumlar[h].to_numpy(float) - dolum) / atr for h in HEDEFLER),
        ]
    )


def sablon_oyna(g: Gun, t: int, sablon: np.ndarray, cikis: Cikis, olcu: str) -> float:
    """Rastgele giriş kıyası (SPEC 5.8 madde 3): t günü sinyal veren, dolum gününün AOF'sinden dolan `piyasa` kurulumunun `olcu` değeri.

    Stop ve hedefler dolumdan `sablon` x ATR(t) uzakta. Ön koşul: `g.uygun[t]`."""
    j = int(g.dolum_gunu[t])
    d = sablon * g.atr[t]
    dolum = g.aof[j]
    satir = {
        "giris_tur": "piyasa",
        "stop": dolum - d[0],
        **dict(zip(HEDEFLER, dolum + d[1:], strict=True)),
    }
    e = _Islem(t, satir, float(satir["stop"]), RISK_TABANI * float(g.atr[t]))
    return getattr(sonuc(_tut(_doldur(e, j, dolum), g, cikis)[0]), olcu)


def _kapanis_nedeni(e: _Islem, i: int, g: Gun, cikis: Cikis) -> str | None:
    """i. günün kapanışından sonra yarın için bekleyen kapanışa bağlı çıkış (SPEC 5.4 adım 6): önce stop, sonra çıkış sinyali."""
    if cikis.stop_mod == "kapanis" and g.kap[i] < e.stop:
        return "stop (kapanış)"
    return CIKIS_SINYALI if g.cikis_sinyali[i] else None


def _acik_gun(e: _Islem, i: int, g: Gun, cikis: Cikis) -> bool:
    """Açık işlemin bir günü, SPEC 5.4 sırasıyla. İşlem kapanınca True."""
    nedeni = _kapanis_nedeni(e, i, g, cikis)
    dolumda_stop = i == e.dolum_i and e.giris <= e.stop
    if g.taban_kilit[i]:  # satış yok; çıkış ilk kilitsiz güne kalır (adım 1)
        if dolumda_stop:
            e.bekleyen = "stop (dolumda)"
        elif e.bekleyen is None:
            dokundu = cikis.stop_mod == "dokunus" and g.dus[i] <= e.stop
            e.bekleyen = "stop" if dokundu else nedeni
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


def sonuc(e: _Islem) -> Sonuc:
    """Kapanmış ya da `açık` işlemin değeri; kısmi çıkışlar payıyla (SPEC 5.2, 5.3)."""
    giris, p = e.giris, e.parcalar
    r = sum(pay * (f - giris - maliyet(giris, f)) / e.risk for _, f, pay, _ in p)
    yuzde = sum(pay * (f - giris - maliyet(giris, f)) / giris for _, f, pay, _ in p)
    return Sonuc(r, yuzde * 100)


def _kayit(e: _Islem, g: Gun, cikis: Cikis, sembol, strateji, sinif) -> dict:
    tarih, giris, risk, p = g.tarih, e.giris, e.risk, e.parcalar
    r, net_yuzde = sonuc(e)
    son_i, son_fiyat, _, son_neden = p[-1]
    kap = g.kap
    ileri = {
        f"getiri_{n}": (kap[j] - giris - maliyet(giris, kap[j])) / giris * 100
        if (j := e.dolum_i + n) < len(kap)
        else np.nan
        for n in ILERI_GUNLER
    }
    pencere = slice(
        e.dolum_i + 1, e.dolum_i + 11
    )  # dolum günü yüksek/düşük dolumdan önce olabilir
    yuk, dus = g.yuk[pencere], g.dus[pencere]
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
        "tavan_kapanis": bool(g.tavan_kapanis[e.sinyal_i]),
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
        "net_yuzde": net_yuzde,
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


def kayit_sutunlari(cikis: Cikis) -> dict[str, str]:
    """Boş işlem kaydının sütunları ve dtype'ları."""
    yazi, tarih, sayi, mantik = "str", "datetime64[us]", "float64", "bool"
    return {
        "strateji": yazi,
        "sinif": yazi,
        "sembol": yazi,
        "sinyal_tarihi": tarih,
        "giris_tur": yazi,
        "seviye": sayi,
        "dolum_tarihi": tarih,
        "dolum_fiyati": sayi,
        "durum": yazi,
        "kural_durumu": yazi,
        "tavan_kapanis": mantik,
        "stop": sayi,
        **dict.fromkeys(HEDEFLER, sayi),
        "kismi": yazi,
        **{f"{ad}_gun": sayi for ad, _ in cikis.hedef},
        "stop_gun": sayi,
        "cikis_tarihi": tarih,
        "cikis_fiyati": sayi,
        "cikis_nedeni": yazi,
        "net_yuzde": sayi,
        "R": sayi,
        "tutma_gun": "int64",
        **{f"getiri_{n}": sayi for n in ILERI_GUNLER},
        "mfe_yuzde": sayi,
        "mae_yuzde": sayi,
        "mfe_R": sayi,
        "mae_R": sayi,
        "risk_tabanli": mantik,
        "dolumda_stop": mantik,
        "acik": mantik,
    }


def kayit_tablosu(kayitlar: list[dict], cikis: Cikis) -> pd.DataFrame:
    """İşlem kaydı; kayıt yokken de `kayit_sutunlari(cikis)` sütunlarıyla."""
    if kayitlar:
        return pd.DataFrame(kayitlar)
    return pd.DataFrame(
        {c: pd.Series(dtype=t) for c, t in kayit_sutunlari(cikis).items()}
    )
