"""Geçmiş sınama: bütün BIST 30 sembollerinde strateji, motor ve dönem ölçüleri (SPEC 5.1-5.6)."""

from collections import Counter

import numpy as np
import pandas as pd

from tansu import gostergeler, islem, veri
from tansu.strateji import Strateji

ILK_GIRIS = pd.Timestamp("2021-01-04")  # 2019-2020 yalnız ısınma (SPEC 3.4)
SAKLI_BAS = pd.Timestamp("2026-01-01")  # saklı dönem faz 4'te (SPEC 5.7)
YILLAR = (2021, 2022, 2023, 2024, 2025)
EN_AZ = 30  # oranlar için en az kurulum (SPEC 5.6)


def calistir(
    strateji: Strateji, anlik: veri.Anlik, p=None
) -> tuple[pd.DataFrame, pd.Series, Counter]:
    """(işlem kaydı, sinyal günleri, düşen sinyal sayaçları). Yalnız üye günlerin sinyalleri sayılır."""
    kayitlar, sinyal_gunleri, sayac = [], [], Counter()
    semboller = sorted(
        set(veri.uyelik_araliklari()["sembol"]) & set(anlik.fiyat["sembol"])
    )
    for sembol in semboller:
        gun = veri.gunluk(anlik, sembol)
        gun["atr"] = gostergeler.atr_basit(gun["yuksek"], gun["dusuk"], gun["kapanis"])
        s = strateji.sinyal(gun, p or {})
        disarida = (gun.index < ILK_GIRIS) | (gun.index >= SAKLI_BAS) | ~gun["uye"]
        s.loc[disarida, ["giris", "tekrar"]] = [False, 0]
        sinyal_gunleri += [(sembol, t) for t in s.index[s["giris"]]]
        k, c = islem.simule(
            gun,
            s,
            strateji.cikis,
            sembol=sembol,
            strateji=strateji.ad,
            sinif=strateji.sinif,
        )
        kayitlar += k
        sayac += c
    islemler = pd.DataFrame(kayitlar)
    sinyaller = pd.DataFrame(sinyal_gunleri, columns=["sembol", "tarih"])
    return islemler, sinyaller, sayac


def sirala(islemler: pd.DataFrame) -> pd.DataFrame:
    """Eğri ve düşüş sırası: çıkış tarihi, sonra dolum tarihi ve sembol (kararlı)."""
    return islemler.sort_values(
        ["cikis_tarihi", "dolum_tarihi", "sembol"], kind="stable"
    )


def _oran(deger: float, n: int, bicim: str = "{:.2f}") -> str:
    if n < EN_AZ:
        return f"n/a (N = {n})"
    return "n/a" if not np.isfinite(deger) else bicim.format(deger)


def dusus(r: pd.Series) -> float:
    """Kümülatif R eğrisinde en büyük düşüş (çıkış tarihi sırasıyla)."""
    birikim = r.cumsum()
    return float((birikim.cummax().clip(lower=0) - birikim).max()) if len(r) else 0.0


def en_uzun_kayip(r: pd.Series) -> int:
    seri = en_uzun = 0
    for x in r:
        seri = seri + 1 if x <= 0 else 0
        en_uzun = max(en_uzun, seri)
    return en_uzun


def donem_ozeti(islemler: pd.DataFrame, sinyal_n: int) -> dict:
    """SPEC 5.6 sınıf (a) ölçüleri; 30 kurulumun altında oranlar `n/a (N = x)`."""
    n = len(islemler)
    r = sirala(islemler)["R"] if n else pd.Series(dtype=float)
    kazanc, kayip = r[r > 0], r[r <= 0]
    asagi = np.sqrt((np.minimum(r, 0) ** 2).mean()) if n else np.nan
    dd = dusus(r)
    toplam = float(r.sum())
    return {
        "Sinyal": sinyal_n,
        "Dolum": n,
        "Düşen": f"{sinyal_n - n} ({(sinyal_n - n) / sinyal_n:.0%})"
        if sinyal_n
        else "0",
        "Kazanma oranı": _oran(len(kazanc) / n if n else np.nan, n, "{:.0%}"),
        "Ortalama kazanç R": _oran(kazanc.mean(), n),
        "Ortalama kayıp R": _oran(kayip.mean(), n),
        "Beklenti (ortalama R)": _oran(r.mean(), n),
        "Medyan R": _oran(r.median(), n),
        "Toplam R": f"{toplam:.2f}",
        "Kâr faktörü": _oran(
            kazanc.sum() / -kayip.sum() if kayip.sum() < 0 else np.inf, n
        ),
        "Sharpe (kurulum başı)": _oran(r.mean() / r.std() if n > 1 else np.nan, n),
        "Sortino (kurulum başı)": _oran(r.mean() / asagi if asagi else np.nan, n),
        "En büyük düşüş R": f"{dd:.2f}",
        "Toplam / düşüş": _oran(toplam / dd if dd else np.nan, n),
        "Ortalama tutma günü": f"{islemler['tutma_gun'].mean():.1f}" if n else "-",
        "En uzun kayıp serisi": str(en_uzun_kayip(r)),
        "Açık işlem": int(islemler["acik"].sum()) if n else 0,
        "Dolumda stop": int(islemler["dolumda_stop"].sum()) if n else 0,
        "Risk tabanı uygulanan": int(islemler["risk_tabanli"].sum()) if n else 0,
    }


def donemler(islemler: pd.DataFrame, sinyaller: pd.DataFrame) -> dict[str, dict]:
    """Her yıl ve bütün yıllar; yıl sinyal tarihine göre."""
    yil_i = (
        pd.DatetimeIndex(islemler["sinyal_tarihi"]).year
        if len(islemler)
        else pd.Index([])
    )
    yil_s = pd.DatetimeIndex(sinyaller["tarih"]).year
    sonuc = {
        str(y): donem_ozeti(islemler[yil_i == y], int((yil_s == y).sum()))
        for y in YILLAR
    }
    sonuc["Bütün yıllar"] = donem_ozeti(islemler, len(sinyaller))
    if len(islemler):  # tavanda kapanan sinyal günleri çıkarılmış hali (SPEC 5.1)
        tavansiz = islemler[~islemler["tavan_kapanis"].astype(bool)]
        sonuc["Bütün yıllar, tavan kapanışsız"] = donem_ozeti(
            tavansiz, len(sinyaller) - (len(islemler) - len(tavansiz))
        )
    return sonuc


def isabet(islemler: pd.DataFrame, hedefler: tuple[str, ...]) -> list[dict]:
    """Her hedef için stoptan önce ulaşma payı, önce stop payı ve medyan gün (SPEC 5.5)."""
    n = len(islemler)
    satirlar = []
    for h in hedefler:
        ulasti = islemler[f"{h}_gun"].notna() if n else pd.Series(dtype=bool)
        stop_once = (
            islemler["stop_gun"].notna() & ~ulasti if n else pd.Series(dtype=bool)
        )
        satirlar.append(
            {
                "Hedef": h,
                "Stoptan önce ulaştı": _oran(
                    ulasti.mean() if n else np.nan, n, "{:.0%}"
                ),
                "Önce stop": _oran(stop_once.mean() if n else np.nan, n, "{:.0%}"),
                "Medyan gün (hedef)": f"{islemler.loc[ulasti, f'{h}_gun'].median():.0f}"
                if n and ulasti.any()
                else "-",
                "Medyan gün (stop)": f"{islemler.loc[stop_once, 'stop_gun'].median():.0f}"
                if n and stop_once.any()
                else "-",
            }
        )
    return satirlar


def sembol_tablosu(islemler: pd.DataFrame) -> pd.DataFrame:
    """Sembol başına kurulum ve toplam R; toplamın %40'ından fazlası işaretlenir (varsayım)."""
    if not len(islemler):
        return pd.DataFrame(columns=["sembol", "kurulum", "toplam_R", "pay", "isaret"])
    t = (
        islemler.groupby("sembol")["R"]
        .agg(kurulum="size", toplam_R="sum")
        .reset_index()
    )
    toplam = t["toplam_R"].sum()
    t["pay"] = t["toplam_R"] / toplam if toplam > 0 else np.nan
    t["isaret"] = t["pay"] > 0.4
    return t.sort_values("toplam_R", ascending=False)
