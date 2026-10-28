"""Geçmiş sınama: bütün BIST 30 sembollerinde strateji, motor ve dönem ölçüleri (SPEC 5.1-5.7)."""

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import NamedTuple

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike

from tansu import gostergeler, islem, veri
from tansu.strateji import Strateji

ILK_GIRIS = pd.Timestamp("2021-01-04")  # 2019-2020 yalnız ısınma (SPEC 3.4)
KESIM = pd.Timestamp("2025-12-31")
SAKLI_BAS = pd.Timestamp("2026-01-01")
YILLAR = (2021, 2022, 2023, 2024, 2025)
EN_AZ = 30  # oranlar için en az kurulum (SPEC 5.6)
BIRIM = {"R": "R", "net_yuzde": "%"}  # ölçü sütunu -> etiket birimi

Gunler = Mapping[str, pd.DataFrame]


@dataclass(frozen=True)
class Donem:
    """Bir koşunun sınırı: sinyal yalnız [bas, son] içindeki üye günlerde sayılır; motor `son`dan sonraki fiyatı görmez,
    o gün açık kalan kurulum o günün kapanışıyla `acik` işaretlenir."""

    bas: pd.Timestamp
    son: pd.Timestamp


GECMIS = Donem(ILK_GIRIS, KESIM)


class Kosu(NamedTuple):
    """Bir parametre setinin bir koşusu: işlem kaydı, sinyal günleri, düşen sinyal sayaçları."""

    islemler: pd.DataFrame
    sinyaller: pd.DataFrame
    sayac: Counter

    def kes(self, bas: pd.Timestamp, son: pd.Timestamp) -> "Kosu":
        """Sinyal tarihi [bas, son] içinde olan kurulumlar ve sinyaller; kurulum kendi çıkışını korur.
        Sayaçlar tarihsiz olduğu için dilimde boştur."""
        i, s = self.islemler, self.sinyaller
        if len(i):
            i = i[i["sinyal_tarihi"].between(bas, son)]
        return Kosu(i, s[s["tarih"].between(bas, son)], Counter())


def gunler(anlik: veri.Anlik) -> dict[str, pd.DataFrame]:
    """Anlık görüntüdeki her BIST 30 sembolünün günlük tablosu ve `atr`'si; komut başına bir kez."""
    semboller = sorted(
        set(veri.uyelik_araliklari()["sembol"]) & set(anlik.fiyat["sembol"])
    )
    sonuc = {}
    for sembol in semboller:
        gun = veri.gunluk(anlik, sembol)
        gun["atr"] = gostergeler.atr_basit(gun["yuksek"], gun["dusuk"], gun["kapanis"])
        sonuc[sembol] = gun
    return sonuc


def sakli_son(gunler: Gunler) -> pd.Timestamp:
    """Saklı dönemin sonu: verinin son tam ayının son günü (SPEC 5.7). Veri ayın son iş gününe ulaştıysa ay tamdır."""
    son = max(g.index[-1] for g in gunler.values()).normalize()
    if son.is_month_end or pd.offsets.BMonthEnd().is_on_offset(son):
        return son
    return son - pd.offsets.MonthEnd(1)


def calistir(
    strateji: Strateji, gunler: Gunler, p: Mapping[str, float | str], donem: Donem
) -> Kosu:
    """Fiyat `donem.son`da kesilir, sonra sinyal hesaplanır; giriş yalnız dönem içindeki üye günlerde sayılır."""
    kayitlar, sinyal_gunleri, sayac = [], [], Counter()
    for sembol in sorted(gunler):
        gun = gunler[sembol].loc[: donem.son]
        if gun.empty:
            continue
        s = strateji.sinyal(gun, p)
        disarida = (gun.index < donem.bas) | ~gun["uye"]
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
    return Kosu(islemler, sinyaller, sayac)


def sirala(islemler: pd.DataFrame) -> pd.DataFrame:
    """Eğri ve düşüş sırası: çıkış tarihi, sonra dolum tarihi ve sembol (kararlı)."""
    return islemler.sort_values(
        ["cikis_tarihi", "dolum_tarihi", "sembol"], kind="stable"
    )


def _oran(deger: float, n: int, bicim: str = "{:.2f}") -> str:
    if n < EN_AZ:
        return f"n/a (N = {n})"
    return "n/a" if not np.isfinite(deger) else bicim.format(deger)


def dusus(r: ArrayLike) -> float | np.ndarray:
    """Son eksende kümülatif eğrinin en büyük düşüşü; tepe 0'dan başlar. 1-B girdi float, 2-B girdi satır başına bir değer
    verir; rapor ve Monte Carlo aynı tanımı kullanır (SPEC 5.6, 5.8)."""
    birikim = np.cumsum(np.asarray(r, float), axis=-1)
    tepe = np.maximum.accumulate(np.maximum(birikim, 0.0), axis=-1)
    d = (tepe - birikim).max(axis=-1, initial=0.0)
    return float(d) if d.ndim == 0 else d


def en_uzun_kayip(r: pd.Series) -> int:
    seri = en_uzun = 0
    for x in r:
        seri = seri + 1 if x <= 0 else 0
        en_uzun = max(en_uzun, seri)
    return en_uzun


def donem_ozeti(islemler: pd.DataFrame, sinyal_n: int, olcu: str) -> dict:
    """SPEC 5.6 ölçüleri, yalnız `olcu` sütunundan ("R" ya da "net_yuzde"); 30 kurulumun altında oranlar `n/a (N = x)`."""
    b = BIRIM[olcu]
    n = len(islemler)
    r = sirala(islemler)[olcu] if n else pd.Series(dtype=float)
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
        f"Ortalama kazanç {b}": _oran(kazanc.mean(), n),
        f"Ortalama kayıp {b}": _oran(kayip.mean(), n),
        f"Beklenti (ortalama {b})": _oran(r.mean(), n),
        f"Medyan {b}": _oran(r.median(), n),
        f"Toplam {b}": f"{toplam:.2f}",
        "Kâr faktörü": _oran(
            kazanc.sum() / -kayip.sum() if kayip.sum() < 0 else np.inf, n
        ),
        "Sharpe (kurulum başı)": _oran(r.mean() / r.std() if n > 1 else np.nan, n),
        "Sortino (kurulum başı)": _oran(r.mean() / asagi if asagi else np.nan, n),
        f"En büyük düşüş {b}": f"{dd:.2f}",
        "Toplam / düşüş": _oran(toplam / dd if dd else np.nan, n),
        "Ortalama tutma günü": f"{islemler['tutma_gun'].mean():.1f}" if n else "-",
        "En uzun kayıp serisi": str(en_uzun_kayip(r)),
        "Açık işlem": int(islemler["acik"].sum()) if n else 0,
        "Dolumda stop": int(islemler["dolumda_stop"].sum()) if n else 0,
        "Risk tabanı uygulanan": int(islemler["risk_tabanli"].sum()) if n else 0,
    }


def donemler(
    islemler: pd.DataFrame, sinyaller: pd.DataFrame, olcu: str
) -> dict[str, dict]:
    """Her yıl ve bütün yıllar; yıl sinyal tarihine göre (`GECMIS` koşusu)."""
    yil_i = (
        pd.DatetimeIndex(islemler["sinyal_tarihi"]).year
        if len(islemler)
        else pd.Index([])
    )
    yil_s = pd.DatetimeIndex(sinyaller["tarih"]).year
    sonuc = {
        str(y): donem_ozeti(islemler[yil_i == y], int((yil_s == y).sum()), olcu)
        for y in YILLAR
    }
    sonuc["Bütün yıllar"] = donem_ozeti(islemler, len(sinyaller), olcu)
    if len(islemler):  # tavanda kapanan sinyal günleri çıkarılmış hali (SPEC 5.1)
        tavansiz = islemler[~islemler["tavan_kapanis"].astype(bool)]
        sonuc["Bütün yıllar, tavan kapanışsız"] = donem_ozeti(
            tavansiz, len(sinyaller) - (len(islemler) - len(tavansiz)), olcu
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


def sembol_tablosu(islemler: pd.DataFrame, olcu: str) -> pd.DataFrame:
    """Sembol başına kurulum ve toplam `olcu`; toplamın %40'ından fazlası işaretlenir (varsayım)."""
    sutun = f"toplam_{olcu}"
    if not len(islemler):
        return pd.DataFrame(columns=["sembol", "kurulum", sutun, "pay", "isaret"])
    t = (
        islemler.groupby("sembol")[olcu]
        .agg(kurulum="size", **{sutun: "sum"})
        .reset_index()
    )
    toplam = t[sutun].sum()
    t["pay"] = t[sutun] / toplam if toplam > 0 else np.nan
    t["isaret"] = t["pay"] > 0.4
    return t.sort_values(sutun, ascending=False)


def ileri_tablo(islemler: pd.DataFrame) -> list[dict]:
    """Sınıf (b) ileri getiri tablosu (SPEC 5.2, 5.6): 1, 3, 5, 10 gün net % ve 10 günlük MFE/MAE medyanı.
    Her ufuk kendi N'siyle sayılır (veri sonuna yakın dolumların ufku boştur); 30'un altında oranlar `n/a (N = x)`."""

    def sutun(ad: str) -> pd.Series:
        return islemler[ad].dropna() if len(islemler) else pd.Series(dtype=float)

    satirlar = []
    for gun in islem.ILERI_GUNLER:
        x = sutun(f"getiri_{gun}")
        n = len(x)
        satirlar.append(
            {
                "Ufuk (gün)": gun,
                "N": n,
                "Ortalama net %": _oran(x.mean(), n),
                "Medyan net %": _oran(x.median(), n),
                "Pozitif payı": _oran((x > 0).mean() if n else np.nan, n, "{:.0%}"),
            }
        )
    for ad, etiket in (("mfe_yuzde", "Medyan MFE %"), ("mae_yuzde", "Medyan MAE %")):
        x = sutun(ad)
        satirlar.append(
            {
                "Ufuk (gün)": f"{etiket} (10 gün)",
                "N": len(x),
                "Ortalama net %": "-",
                "Medyan net %": _oran(x.median(), len(x)),
                "Pozitif payı": "-",
            }
        )
    return satirlar
