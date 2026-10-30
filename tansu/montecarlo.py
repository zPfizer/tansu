"""Monte Carlo ve rastgele giriş kıyası (SPEC 5.8), dikişli örneklem dışı kurulumlarda; tohumlu."""

from dataclasses import dataclass
from typing import NamedTuple

import numpy as np
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


class Yuzdelik(NamedTuple):
    p5: float
    p50: float
    p95: float


def yuzdelik(a: ArrayLike) -> Yuzdelik:
    return Yuzdelik(*map(float, np.percentile(a, [5, 50, 95])))


@dataclass(frozen=True)
class Rastgele:
    strateji_ort: float
    ortalamalar: Yuzdelik
    yuzdelik: float  # strateji ortalamasının koşular içindeki yüzdeliği, 0-100


@dataclass(frozen=True)
class MonteCarlo:
    """`n` < `sinama.EN_AZ` ise bütün tablolar None; rapor `n/a (N = n)` yazar (SPEC 5.8)."""

    tohum: int
    tekrar: int
    n: int
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
        return MonteCarlo(TOHUM, tekrar, n, None, None, None, None, None)
    x = sinama.sirala(islemler)[olcu].to_numpy(float)
    toplam, dusus = bootstrap(x, akis(0), tekrar)
    return MonteCarlo(
        TOHUM,
        tekrar,
        n,
        bootstrap_toplam=yuzdelik(toplam),
        bootstrap_dusus=yuzdelik(dusus),
        batma=float((dusus >= BATMA_R).mean()) if strateji.sinif == "a" else None,
        karistirma_dusus=yuzdelik(karistir(x, akis(1), tekrar)),
        rastgele=_rastgele(strateji, gunler, yuruyus, float(x.mean()), tekrar),
    )


def _rastgele(
    strateji: Strateji,
    gunler: sinama.Gunler,
    yuruyus: ayar.Yuruyus,
    strateji_ort: float,
    tekrar: int,
) -> Rastgele | None:
    """Rastgele giriş kıyası (SPEC 5.8 madde 3). Şablon, sinyal günü ATR'si 0'dan büyük gerçek kurulumdur.
    Kurulumu olan bir adımda uygun gün ya da şablon yoksa kıyas yapılamaz: None."""
    kesik = {s: g.loc[: sinama.KESIM] for s, g in sorted(gunler.items())}
    kesik = {s: g for s, g in kesik.items() if not g.empty}
    motor: dict[tuple, islem.Gun] = {}
    plan = []
    for a in yuruyus.adimlar:
        test = a.test.islemler
        if not len(test):
            continue
        p = a.secim.parametre
        secenekler = []
        for s, g in kesik.items():
            anahtar = (s, frozenset(p.items()))
            if anahtar not in motor:
                motor[anahtar] = islem.Gun(g, strateji.sinyal(g, p))
            m = motor[anahtar]
            pencere = (g.index >= a.pencere.test_bas) & (g.index <= a.pencere.test_son)
            secenekler += [(m, int(t)) for t in np.flatnonzero(m.uygun & pencere)]
        atr = np.array(
            [
                gunler[s].at[t, "atr"]
                for s, t in zip(test["sembol"], test["sinyal_tarihi"], strict=True)
            ],
            float,
        )
        sablonlar = islem.sablonlar(test[atr > 0], atr[atr > 0])
        if not secenekler or not len(sablonlar):
            return None
        plan.append((secenekler, sablonlar, len(test)))
    n = sum(m for *_, m in plan)
    ortalamalar = np.empty(tekrar)
    for kosu in range(tekrar):
        rng = akis(2, kosu)
        toplam = 0.0
        for secenekler, sablonlar, m in plan:
            for i, j in zip(
                rng.integers(0, len(secenekler), m),
                rng.integers(0, len(sablonlar), m),
                strict=True,
            ):
                g, t = secenekler[i]
                toplam += islem.sablon_oyna(
                    g, t, sablonlar[j], strateji.cikis, strateji.olcu
                )
        ortalamalar[kosu] = toplam / n
    alti = (ortalamalar < strateji_ort).sum() + 0.5 * (
        ortalamalar == strateji_ort
    ).sum()
    return Rastgele(strateji_ort, yuzdelik(ortalamalar), float(100 * alti / tekrar))
