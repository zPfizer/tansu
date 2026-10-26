"""Salınım pivotları (SPEC 4, `yapi.py`). Her pivot onay gününden önce bilinmez."""

from collections.abc import Iterator
from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view


@dataclass(frozen=True)
class Pivot:
    tur: str  # "T" tepe, "D" dip
    pivot_gun: int  # satır konumu
    onay_gun: int
    fiyat: float


def sag_bar_pivotlari(yuksek: pd.Series, dusuk: pd.Series, k: int) -> list[Pivot]:
    """Tepe: yüksek, [i-k, i+k] penceresinin en büyüğü (eşitlikte ilki); dip ayna. Onay günü i+k."""
    y = np.nan_to_num(yuksek.to_numpy(float), nan=-np.inf)
    d = np.nan_to_num(dusuk.to_numpy(float), nan=np.inf)
    if len(y) < 2 * k + 1:
        return []
    tepe = np.flatnonzero(sliding_window_view(y, 2 * k + 1).argmax(axis=1) == k) + k
    dip = np.flatnonzero(sliding_window_view(d, 2 * k + 1).argmin(axis=1) == k) + k
    pivotlar = [Pivot("T", int(i), int(i) + k, float(y[i])) for i in tepe]
    pivotlar += [Pivot("D", int(i), int(i) + k, float(d[i])) for i in dip]
    return sorted(pivotlar, key=lambda p: (p.onay_gun, p.pivot_gun, p.tur))


def zigzag_pivotlari(yuksek: pd.Series, dusuk: pd.Series, yuzde: float) -> list[Pivot]:
    """Yüzde zigzag: tepe, fiyat en yüksekten `yuzde` kadar düşünce onaylanır; dip ayna."""
    y, d = yuksek.to_numpy(float), dusuk.to_numpy(float)
    oran = yuzde / 100
    pivotlar, yon = [], 0  # 1: son onay dip (tepe aranıyor), -1: son onay tepe
    tepe_i = dip_i = None
    for i in range(len(y)):
        if not (np.isfinite(y[i]) and np.isfinite(d[i])):
            continue
        if yon >= 0 and (tepe_i is None or y[i] > y[tepe_i]):
            tepe_i = i
        if yon <= 0 and (dip_i is None or d[i] < d[dip_i]):
            dip_i = i
        if yon >= 0 and tepe_i < i and d[i] <= y[tepe_i] * (1 - oran):
            pivotlar.append(Pivot("T", tepe_i, i, float(y[tepe_i])))
            yon, dip_i = -1, tepe_i + 1 + int(np.nanargmin(d[tepe_i + 1 : i + 1]))
        elif yon <= 0 and dip_i < i and y[i] >= d[dip_i] * (1 + oran):
            pivotlar.append(Pivot("D", dip_i, i, float(d[dip_i])))
            yon, tepe_i = 1, dip_i + 1 + int(np.nanargmax(y[dip_i + 1 : i + 1]))
    return pivotlar


def ardisik(pivotlar: list[Pivot]) -> Iterator[tuple[Pivot, ...]]:
    """Onay sırasıyla tepe-dip sırası; aynı türden ikinci pivot daha uçtaysa öncekinin yerine geçer.

    Her değişiklikte o anki sırayı verir; son eleman yeni onaylanan pivottur."""
    sira: list[Pivot] = []
    for p in pivotlar:
        if sira and sira[-1].tur == p.tur:
            once = sira[-1].fiyat
            if (p.tur == "T" and p.fiyat <= once) or (p.tur == "D" and p.fiyat >= once):
                continue
            sira[-1] = p
        else:
            sira.append(p)
        yield tuple(sira)
