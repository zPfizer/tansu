"""Geçmiş sınama: evrenin bütün sembollerinde strateji, motor ve dönem ölçüleri (SPEC 2, 5.1-5.7)."""

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, NamedTuple

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


class Ozet(NamedTuple):
    """Bir dönemin SPEC 5.6 sayıları."""

    sinyal: int
    dolum: int
    kazanma: float
    ort_kazanc: float
    ort_kayip: float
    beklenti: float
    medyan: float
    toplam: float
    kar_faktoru: float
    sharpe: float
    sortino: float
    dusus: float
    toplam_dusus: float
    tutma: float
    kayip_serisi: int
    acik: int
    dolumda_stop: int
    risk_tabanli: int


class Kosu(NamedTuple):
    """Bir parametre setinin bir koşusu: işlem kaydı, sinyal günleri, düşen sinyal sayaçları ve ölçü sütunu."""

    islemler: pd.DataFrame
    sinyaller: pd.DataFrame
    sayac: Counter
    olcu: Literal["R", "net_yuzde"]

    def kes(self, bas: pd.Timestamp, son: pd.Timestamp) -> "Kosu":
        """Sinyal tarihi [bas, son] içinde olan kurulumlar ve sinyaller; kurulum kendi çıkışını korur.
        Sayaçlar tarihsiz olduğu için dilimde boştur."""
        i, s = self.islemler, self.sinyaller
        return Kosu(
            i[i["sinyal_tarihi"].between(bas, son)],
            s[s["tarih"].between(bas, son)],
            Counter(),
            self.olcu,
        )

    def yil(self, y: int) -> "Kosu":
        """Sinyal günü `y` takvim yılında olan dilim."""
        return self.kes(pd.Timestamp(y, 1, 1), pd.Timestamp(y, 12, 31))

    @property
    def toplam(self) -> float:
        """`olcu` toplamı; boş koşuda 0.0."""
        return float(self.islemler[self.olcu].sum())

    def ozet(self) -> Ozet:
        return ozet(self.islemler, len(self.sinyaller), self.olcu)


def gunler(anlik: veri.Anlik) -> dict[str, pd.DataFrame]:
    """Anlık görüntüdeki her sembolün (bütün BIST evreni) günlük tablosu ve `atr`'si; komut başına bir kez."""
    sonuc = {}
    for sembol in sorted(anlik.fiyat["sembol"].unique()):
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
        tavan = gun["tavan_kapanis"]
        sinyal_gunleri += [(sembol, t, bool(tavan.at[t])) for t in s.index[s["giris"]]]
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
    islemler = islem.kayit_tablosu(kayitlar, strateji.cikis)
    sinyaller = pd.DataFrame(
        sinyal_gunleri, columns=["sembol", "tarih", "tavan_kapanis"]
    )
    return Kosu(islemler, sinyaller, sayac, strateji.olcu)


def sirala(islemler: pd.DataFrame) -> pd.DataFrame:
    """Eğri ve düşüş sırası: çıkış tarihi, sonra dolum tarihi ve sembol (kararlı)."""
    return islemler.sort_values(
        ["cikis_tarihi", "dolum_tarihi", "sembol"], kind="stable"
    )


def dusus(r: ArrayLike) -> float | np.ndarray:
    """Son eksende kümülatif eğrinin en büyük düşüşü; tepe 0'dan başlar. 1-B girdi float, 2-B girdi satır başına bir değer
    verir; NaN değer atlanır (SPEC 5.6, 5.8)."""
    birikim = np.nancumsum(np.asarray(r, float), axis=-1)
    tepe = np.maximum.accumulate(np.maximum(birikim, 0.0), axis=-1)
    d = (tepe - birikim).max(axis=-1, initial=0.0)
    return float(d) if d.ndim == 0 else d


def en_uzun_kayip(r: pd.Series) -> int:
    seri = en_uzun = 0
    for x in r:
        seri = seri + 1 if x <= 0 else 0
        en_uzun = max(en_uzun, seri)
    return en_uzun


def ozet(islemler: pd.DataFrame, sinyal_n: int, olcu: str) -> Ozet:
    """SPEC 5.6 ölçüleri."""
    n = len(islemler)
    r = sirala(islemler)[olcu]
    kazanc, kayip = r[r > 0], r[r <= 0]
    asagi = np.sqrt((np.minimum(r, 0) ** 2).mean())
    dd = dusus(r)
    toplam = float(r.sum())
    return Ozet(
        sinyal=sinyal_n,
        dolum=n,
        kazanma=len(kazanc) / n if n else np.nan,
        ort_kazanc=kazanc.mean(),
        ort_kayip=kayip.mean(),
        beklenti=r.mean(),
        medyan=r.median(),
        toplam=toplam,
        kar_faktoru=kazanc.sum() / -kayip.sum() if kayip.sum() < 0 else np.inf,
        sharpe=r.mean() / r.std() if n > 1 else np.nan,
        sortino=r.mean() / asagi if asagi else np.nan,
        dusus=dd,
        toplam_dusus=toplam / dd if dd else np.nan,
        tutma=islemler["tutma_gun"].mean(),
        kayip_serisi=en_uzun_kayip(r),
        acik=int(islemler["acik"].sum()),
        dolumda_stop=int(islemler["dolumda_stop"].sum()),
        risk_tabanli=int(islemler["risk_tabanli"].sum()),
    )


def donemler(k: Kosu) -> dict[str, Ozet]:
    """Her yıl ve bütün yıllar; yıl sinyal tarihine göre (`GECMIS` koşusu)."""
    sonuc = {str(y): k.yil(y).ozet() for y in YILLAR}
    sonuc["Bütün yıllar"] = k.ozet()
    if len(k.islemler):
        tavansiz = k.islemler[~k.islemler["tavan_kapanis"].astype(bool)]
        tavansiz_sinyal = (~k.sinyaller["tavan_kapanis"]).sum()
        sonuc["Bütün yıllar, tavan kapanışsız"] = ozet(
            tavansiz, int(tavansiz_sinyal), k.olcu
        )
    return sonuc


class Isabet(NamedTuple):
    hedef: str
    n: int
    ulasti: float
    stop_once: float
    gun_hedef: float | None
    gun_stop: float | None


def isabet(islemler: pd.DataFrame, hedefler: tuple[str, ...]) -> list[Isabet]:
    """Her hedef için stoptan önce ulaşma payı, önce stop payı ve medyan gün (SPEC 5.5)."""
    satirlar = []
    for h in hedefler:
        ulasti = islemler[f"{h}_gun"].notna()
        stop_once = islemler["stop_gun"].notna() & ~ulasti
        satirlar.append(
            Isabet(
                hedef=h,
                n=len(islemler),
                ulasti=ulasti.mean(),
                stop_once=stop_once.mean(),
                gun_hedef=islemler.loc[ulasti, f"{h}_gun"].median()
                if ulasti.any()
                else None,
                gun_stop=islemler.loc[stop_once, "stop_gun"].median()
                if stop_once.any()
                else None,
            )
        )
    return satirlar


def sembol_tablosu(islemler: pd.DataFrame, olcu: str) -> pd.DataFrame:
    """Sembol başına kurulum ve toplam `olcu`; toplamın %40'ından fazlası işaretlenir (varsayım)."""
    sutun = f"toplam_{olcu}"
    t = (
        islemler.groupby("sembol")[olcu]
        .agg(kurulum="size", **{sutun: "sum"})
        .reset_index()
    )
    toplam = t[sutun].sum()
    t["pay"] = t[sutun] / toplam if toplam > 0 else np.nan
    t["isaret"] = t["pay"] > 0.4
    return t.sort_values(sutun, ascending=False)


class Ileri(NamedTuple):
    ufuk: int | Literal["MFE", "MAE"]
    n: int
    ortalama: float | None
    medyan: float
    pozitif: float | None


def ileri_tablo(islemler: pd.DataFrame) -> list[Ileri]:
    """Sınıf (b) ileri getiri tablosu (SPEC 5.2, 5.6): 1, 3, 5, 10 gün net % ve 10 günlük MFE/MAE medyanı."""
    satirlar = []
    for gun in islem.ILERI_GUNLER:
        x = islemler[f"getiri_{gun}"].dropna()
        n = len(x)
        pozitif = (x > 0).mean() if n else np.nan
        satirlar.append(Ileri(gun, n, x.mean(), x.median(), pozitif))
    for ad, ufuk in (("mfe_yuzde", "MFE"), ("mae_yuzde", "MAE")):
        x = islemler[ad].dropna()
        satirlar.append(Ileri(ufuk, len(x), None, x.median(), None))
    return satirlar
