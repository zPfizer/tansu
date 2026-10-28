"""Strateji arayüzü (SPEC 4)."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

from tansu.islem import HEDEFLER, Cikis


@dataclass(frozen=True)
class Strateji:
    ad: str
    tur: Literal["giris", "suzgec"]
    sinif: Literal["a", "b"]
    zaman: Literal["gunluk", "haftalik", "aylik"]
    kaynaklar: tuple[
        str, ...
    ]  # Tansu notları yerel kural kartında (SPEC Ek B #12 açık)
    varsayilan: Mapping[str, float | str]
    aralik: Mapping[str, tuple[float | str, ...]]
    seviye_param: tuple[str, ...]
    cikis: Cikis | None
    hesapla: Callable[[pd.DataFrame, Mapping[str, float | str]], pd.DataFrame]

    def sinyal(self, gun: pd.DataFrame, p: Mapping[str, float | str]) -> pd.DataFrame:
        return self.hesapla(gun, {**self.varsayilan, **p})

    @property
    def olcu(self) -> Literal["R", "net_yuzde"]:
        """Bir kurulumun sonucunu tutan işlem kaydı sütunu (SPEC 5.2)."""
        if self.sinif == "a":
            return "R"
        if self.cikis is None:
            raise NotImplementedError(f"{self.ad}: çıkışsız sınıf (b) faz 8'de")
        return "net_yuzde"


def bos_sinyal(index: pd.Index) -> pd.DataFrame:
    """Her gün bir satır; giriş yok (SPEC 4 sütunları)."""
    s = pd.DataFrame(index=index)
    s["giris"] = False
    s["giris_tur"] = ""
    s["seviye"] = np.nan
    s["gecerlilik"] = 0
    s["stop"] = np.nan
    for h in HEDEFLER:
        s[h] = np.nan
    s["durum"] = ""
    s["kural_durumu"] = ""
    s["tekrar"] = 0
    s["cikis_sinyali"] = False
    return s
