"""Monte Carlo ve rastgele giriş kıyası (SPEC 5.8), dikişli örneklem dışı kurulumlarda; tohumlu."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike

from tansu import ayar, islem, sinama
from tansu.strateji import Strateji

TOHUM = 20261028  # sabit, rapora yazılır (SPEC 5.8)
TEKRAR = 1000
BATMA_R = 25.0  # batma riski: düşüş >= 25 R, yalnız sınıf (a), varsayım (SPEC 5.8)


def akis(*anahtar: int) -> np.random.Generator:
    """Tablo başına ayrı alt akış; sonuç çağrı sırasına ve işçi sayısına bağlı olmaz."""
    return np.random.default_rng(np.random.SeedSequence(TOHUM, spawn_key=anahtar))


def bootstrap(
    x: ArrayLike, rng: np.random.Generator, tekrar: int = TEKRAR
) -> tuple[np.ndarray, np.ndarray]:
    """(toplamlar, düşüşler): `tekrar` kez len(x) değer yerine koyarak, çekiliş sırasıyla."""
    x = np.asarray(x, float)
    ornek = x[rng.integers(0, len(x), size=(tekrar, len(x)))]
    return ornek.sum(axis=-1), sinama.dusus(ornek)


def karistir(
    x: ArrayLike, rng: np.random.Generator, tekrar: int = TEKRAR
) -> np.ndarray:
    """`tekrar` rastgele sıralamanın düşüşleri."""
    x = np.asarray(x, float)
    return sinama.dusus(rng.permuted(np.tile(x, (tekrar, 1)), axis=-1))


Yuzdelik = tuple[float, float, float]  # p5, p50, p95


def yuzdelik(a: ArrayLike) -> Yuzdelik:
    p5, p50, p95 = np.percentile(a, [5, 50, 95])
    return float(p5), float(p50), float(p95)


@dataclass(frozen=True)
class Rastgele:
    strateji_ort: float  # dikişli örneklem dışı kurulum başına ortalama
    ortalamalar: Yuzdelik  # rastgele koşu ortalamalarının yüzdelikleri
    yuzdelik: float  # strateji ortalamasının koşular içindeki yüzdeliği, 0-100


@dataclass(frozen=True)
class MonteCarlo:
    """`n` < `sinama.EN_AZ` ise bütün tablolar None; rapor `n/a (N = n)` yazar (SPEC 5.8)."""

    tohum: int
    tekrar: int
    n: int
    olcu: str
    bootstrap_toplam: Yuzdelik | None
    bootstrap_dusus: Yuzdelik | None
    # düşüşü >= BATMA_R olan bootstrap koşularının payı; sınıf (b) için None
    batma: float | None
    karistirma_dusus: Yuzdelik | None
    rastgele: Rastgele | None


def hesapla(
    strateji: Strateji,
    gunler: sinama.Gunler,
    yuruyus: ayar.Yuruyus,
    *,
    tekrar: int = TEKRAR,
) -> MonteCarlo:
    """SPEC 5.8'in üç tablosu; değerler `strateji.olcu`, çıkış tarihi sırasıyla."""
    olcu = strateji.olcu
    islemler = yuruyus.dis_ornek.islemler
    n = len(islemler)
    if n < sinama.EN_AZ:
        return MonteCarlo(TOHUM, tekrar, n, olcu, None, None, None, None, None)
    x = sinama.sirala(islemler)[olcu].to_numpy(float)
    toplam, dusus = bootstrap(x, akis(0), tekrar)
    return MonteCarlo(
        TOHUM,
        tekrar,
        n,
        olcu,
        bootstrap_toplam=yuzdelik(toplam),
        bootstrap_dusus=yuzdelik(dusus),
        batma=float((dusus >= BATMA_R).mean()) if strateji.sinif == "a" else None,
        karistirma_dusus=yuzdelik(karistir(x, akis(1), tekrar)),
        rastgele=_rastgele(strateji, gunler, yuruyus, float(x.mean()), tekrar),
    )


def _uygun_gunler(gun: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """(uygun, sonraki): t sinyal günü olabilir mi; t'den sonraki ilk fiyatlı gün (`islem._emir_gunu` piyasa kuralı).
    Uygun: üye, karantinasız, ATR sonlu, sonraki fiyatlı gün var ve üst limit kilitli değil."""
    son = len(gun)  # sonraki fiyatlı gün yoksa bu sıra; kilitli sayılır
    fiyatli = np.append(
        np.flatnonzero(gun["kapanis"].notna() & gun["aof"].notna()), son
    )
    sonraki = fiyatli[np.searchsorted(fiyatli, np.arange(son), side="right")]
    kilit = np.append(gun["kilit_tavan"].to_numpy(bool), True)
    uygun = (
        gun["uye"].to_numpy(bool)
        & ~gun["karantina"].to_numpy(bool)
        & np.isfinite(gun["atr"].to_numpy(float))
        & ~kilit[sonraki]
    )
    return uygun, sonraki


def _rastgele(
    strateji: Strateji,
    gunler: sinama.Gunler,
    yuruyus: ayar.Yuruyus,
    strateji_ort: float,
    tekrar: int,
) -> Rastgele:
    """Rastgele giriş kıyası (SPEC 5.8 madde 3). Her ileri yürüme adımında o adımın gerçek kurulum sayısı kadar
    rastgele uygun gün ve gerçek kurulum şablonu çekilir; seviyeler şablonun sinyal günü ATR(14) uzaklıklarıdır.
    Fiyat 31.12.2025'te kesilir. Her koşunun kendi akışı var: sonuç parçalamaya bağlı olmaz."""
    k = 0 if strateji.olcu == "R" else 1  # islem.rastgele: (R, net %)
    kesik = {s: g.loc[: sinama.KESIM] for s, g in sorted(gunler.items())}
    kesik = {s: g for s, g in kesik.items() if not g.empty}
    uygunluk = {s: _uygun_gunler(g) for s, g in kesik.items()}
    motor: dict[tuple, islem.Gun] = {}
    plan = []  # adım başına (secenekler, sablonlar)
    for a in yuruyus.adimlar:
        test = a.test.islemler
        if not len(test):
            continue
        p = a.secim.parametre
        secenekler = []  # (motor dizileri, sinyal günü, dolum fiyatı)
        for s, g in kesik.items():
            anahtar = (s, frozenset(p.items()))
            if anahtar not in motor:
                motor[anahtar] = islem.Gun(g, strateji.sinyal(g, p))
            uygun, sonraki = uygunluk[s]
            pencere = (g.index >= a.pencere.test_bas) & (g.index <= a.pencere.test_son)
            secenekler += [
                (motor[anahtar], int(t), float(g["aof"].iat[sonraki[t]]))
                for t in np.flatnonzero(uygun & pencere)
            ]
        atr = np.array(
            [
                gunler[s].at[t, "atr"]
                for s, t in zip(test["sembol"], test["sinyal_tarihi"], strict=True)
            ]
        )
        dolum = test["dolum_fiyati"].to_numpy(float)
        sablonlar = np.column_stack(
            [
                (dolum - test["stop"].to_numpy(float)) / atr,
                *((test[h].to_numpy(float) - dolum) / atr for h in islem.HEDEFLER),
            ]
        )
        plan.append((secenekler, sablonlar))
    n = sum(len(sablonlar) for _, sablonlar in plan)
    ortalamalar = np.empty(tekrar)
    for kosu in range(tekrar):
        rng = akis(2, kosu)
        toplam = 0.0
        for secenekler, sablonlar in plan:
            m = len(sablonlar)
            for i, j in zip(
                rng.integers(0, len(secenekler), m), rng.integers(0, m, m), strict=True
            ):
                g, t, dolum = secenekler[i]
                d = sablonlar[j] * g.atr[t]
                toplam += islem.rastgele(
                    g, t, dolum - d[0], tuple(dolum + d[1:]), strateji.cikis
                )[k]
        ortalamalar[kosu] = toplam / n
    alti = (ortalamalar < strateji_ort).sum() + 0.5 * (
        ortalamalar == strateji_ort
    ).sum()
    return Rastgele(strateji_ort, yuzdelik(ortalamalar), float(100 * alti / tekrar))
