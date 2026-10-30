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
    """Tepe: yüksek, fiyatlı günlerde i'nin solundaki ve sağındaki k barla birlikte en büyük (eşitlikte ilki); dip ayna.
    Fiyatsız gün (yüksek ya da düşük NaN) bar sayılmaz. Onay günü i'den sonraki k. fiyatlı gün."""
    y, d = yuksek.to_numpy(float), dusuk.to_numpy(float)
    fiyatli = np.flatnonzero(np.isfinite(y) & np.isfinite(d))
    y, d = y[fiyatli], d[fiyatli]
    if len(y) < 2 * k + 1:
        return []
    tepe = np.flatnonzero(sliding_window_view(y, 2 * k + 1).argmax(axis=1) == k) + k
    dip = np.flatnonzero(sliding_window_view(d, 2 * k + 1).argmin(axis=1) == k) + k
    pivotlar = [
        Pivot("T", int(fiyatli[i]), int(fiyatli[i + k]), float(y[i])) for i in tepe
    ]
    pivotlar += [
        Pivot("D", int(fiyatli[i]), int(fiyatli[i + k]), float(d[i])) for i in dip
    ]
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


def bacak_uclari(
    yuksek: np.ndarray, dusuk: np.ndarray, sira: tuple[Pivot, ...], t: int
) -> bool:
    """Her pivot kendi bacağının ucu mu: tepe, komşu pivotlar arasındaki (sonuncusunda t'ye dek) en yüksek, dip en düşük.
    İlk pivotun penceresi kendisinden t'ye dektir: öte bir değer deseni bozar (X kırılması: X'in altına inmek). Eşit değer
    bozmaz. Komşu pivot günlerinin barları pencereye girmez, çünkü gün içi sıra bilinmez. Pencere sabit olduğu için pivot
    olamayan bir uç (komşusu daha uç) bacağı yanlış ölçtürür; bu kontrol onu yakalar."""
    for k, p in enumerate(sira):
        if k == 0:
            pencere = slice(p.pivot_gun + 1, t + 1)
        else:
            son = sira[k + 1].pivot_gun if k + 1 < len(sira) else t + 1
            pencere = slice(sira[k - 1].pivot_gun + 1, son)
        if p.tur == "T":
            gecti = yuksek[pencere] > p.fiyat
        else:
            gecti = dusuk[pencere] < p.fiyat
        if gecti.any():
            return False
    return True


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
