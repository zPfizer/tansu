"""Ortalama kesişimi, karşılaştırma tabanı (SPEC 11 madde 15). Kural ve varsayımlar yerel kartta: `stratejiler/ortalama-kesisim.md`."""

from collections.abc import Mapping

import numpy as np
import pandas as pd

from tansu import gostergeler
from tansu.islem import Cikis
from tansu.strateji import Strateji, bos_sinyal

# EMA, uzun dönemin 2,5 katı geçerli kapanıştan sonra geçerli (SPEC 3.4)
ISINMA_KATI = 2.5


def ortalama(kapanis: pd.Series, tur: str, n: int) -> pd.Series:
    """Geçerli olmayan günler NaN. SMA ve WMA n kapanıştan, EMA 2,5 n geçerli kapanıştan sonra."""
    if tur == "EMA":
        return gostergeler.ema(kapanis, n).where(
            kapanis.notna().cumsum() >= ISINMA_KATI * n
        )
    if tur == "SMA":
        return gostergeler.sma(kapanis, n)
    if tur == "WMA":
        return gostergeler.wma(kapanis, n)
    raise ValueError(f"bilinmeyen ortalama: {tur}")


def hesapla(gun: pd.DataFrame, p: Mapping[str, float | str]) -> pd.DataFrame:
    """Yukarı kesişimde `piyasa` girişi, aşağı kesişimde `cikis_sinyali`. Gün t yalnız t'ye kadar olan satırlara bağlıdır."""
    s = bos_sinyal(gun.index)
    kapanis = gun["kapanis"]
    tur, cift, k = p["ortalama"], str(p["cift"]), int(p["teyit_gun"])
    kisa, uzun = (ortalama(kapanis, tur, int(n)) for n in cift.split("/"))
    gecerli = kisa.notna() & uzun.notna() & kapanis.notna()
    ust = (kisa > uzun) & gecerli
    onceki_ust = ust.shift(1, fill_value=False)
    # kesişim günü c: ust[c] ve c-1'de kısa <= uzun (iki ortalama da geçerli)
    kesisim = ust & (gecerli & ~ust).shift(1, fill_value=False)
    tutuyor = ust.astype(float).rolling(k + 1).min() == 1  # c..t
    kapanis_ustte = (kapanis > uzun).astype(float).rolling(k).min() == 1 if k else True
    giris = kesisim.shift(k, fill_value=False) & tutuyor & kapanis_ustte
    s["giris"] = giris
    s["cikis_sinyali"] = gecerli & ~ust & onceki_ust
    s.loc[giris, "giris_tur"] = "piyasa"
    s.loc[giris, "gecerlilik"] = 1
    s.loc[giris, "durum"] = "TETIKLENDI"
    tarih = gun.index
    for t in np.flatnonzero(giris):
        s.iloc[t, s.columns.get_loc("kural_durumu")] = (
            f"{tur} {cift} yukarı kesişim {tarih[t - k].date()}, teyit_gun {k}"
        )
    return s


STRATEJI = Strateji(
    ad="ortalama-kesisim",
    tur="giris",
    sinif="b",
    zaman="gunluk",
    kaynaklar=("stratejiler/ortalama-kesisim.md",),
    varsayilan={"ortalama": "EMA", "cift": "50/200", "teyit_gun": 0},
    aralik={
        "ortalama": ("EMA", "SMA", "WMA"),
        # sıra komşuluğu belirler (SPEC 5.7): bir adım = listedeki sonraki değer
        "cift": (
            "50/200",
            "30/100",
            "48/247",
            "5/25",
            "13/60",
            "5/20",
            "20/50",
            "9/21",
            "10/100",
        ),
        "teyit_gun": (0, 2),
    },
    seviye_param=(),
    cikis=Cikis(),
    hesapla=hesapla,
)
