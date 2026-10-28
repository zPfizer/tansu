"""Monte Carlo (SPEC 5.8 madde 1-2): bootstrap ve sıra karıştırma; saf, vektörel, tohumlu."""

import numpy as np
from numpy.typing import ArrayLike

TOHUM = 20261028  # sabit, rapora yazılır (SPEC 5.8)
TEKRAR = 1000
BATMA_R = 25.0  # batma riski: düşüş >= 25 R, yalnız sınıf (a), varsayım (SPEC 5.8)


def akis(*anahtar: int) -> np.random.Generator:
    """Tablo başına ayrı alt akış; sonuç çağrı sırasına ve işçi sayısına bağlı olmaz."""
    return np.random.default_rng(np.random.SeedSequence(TOHUM, spawn_key=anahtar))


def dususler(m: ArrayLike) -> np.ndarray:
    """Son eksende kümülatif eğrinin en büyük düşüşü; tepe 0'dan başlar (`sinama.dusus` tanımı)."""
    birikim = np.cumsum(m, axis=-1)
    tepe = np.maximum.accumulate(np.maximum(birikim, 0.0), axis=-1)
    return (tepe - birikim).max(axis=-1, initial=0.0)


def bootstrap(
    x: ArrayLike, rng: np.random.Generator, tekrar: int = TEKRAR
) -> tuple[np.ndarray, np.ndarray]:
    """(toplamlar, düşüşler): `tekrar` kez len(x) değer yerine koyarak, çekiliş sırasıyla."""
    x = np.asarray(x, float)
    ornek = x[rng.integers(0, len(x), size=(tekrar, len(x)))]
    return ornek.sum(axis=-1), dususler(ornek)


def karistir(
    x: ArrayLike, rng: np.random.Generator, tekrar: int = TEKRAR
) -> np.ndarray:
    """`tekrar` rastgele sıralamanın düşüşleri."""
    x = np.asarray(x, float)
    return dususler(rng.permuted(np.tile(x, (tekrar, 1)), axis=-1))


def yuzdelik(a: ArrayLike) -> tuple[float, float, float]:
    p5, p50, p95 = np.percentile(a, [5, 50, 95])
    return float(p5), float(p50), float(p95)
