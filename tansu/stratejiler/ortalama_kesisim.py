"""Ortalama kesişimi, karşılaştırma tabanı (SPEC 11 madde 15). Kural ve varsayımlar yerel kartta: `stratejiler/ortalama-kesisim.md`."""

from collections.abc import Mapping

import pandas as pd

from tansu import gostergeler
from tansu.islem import Cikis
from tansu.strateji import Strateji, bos_sinyal

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
    """Yukarı kesişimde `piyasa` girişi, aşağı kesişimde `cikis_sinyali`. Gün t yalnız t'ye kadar olan satırlara bağlıdır.
    Kesişim ve teyit hissenin fiyatlı günlerinde sayılır; fiyatsız satır kesişimi bölmez."""
    s = bos_sinyal(gun.index)
    kapanis = gun["kapanis"].dropna()
    tur, cift, k = p["ortalama"], str(p["cift"]), int(p["teyit_gun"])
    kisa, uzun = (ortalama(kapanis, tur, int(n)) for n in cift.split("/"))
    gecerli = kisa.notna() & uzun.notna()
    ust = (kisa > uzun) & gecerli
    kesisim = ust & (gecerli & ~ust).shift(1, fill_value=False)
    tutuyor = ust.astype(float).rolling(k + 1).min() == 1
    kapanis_ustte = (kapanis > uzun).astype(float).rolling(k).min() == 1 if k else True
    giris = kesisim.shift(k, fill_value=False) & tutuyor & kapanis_ustte
    cikis = gecerli & ~ust & ust.shift(1, fill_value=False)
    s["giris"] = giris.reindex(gun.index, fill_value=False)
    s["cikis_sinyali"] = cikis.reindex(gun.index, fill_value=False)
    s.loc[s["giris"], ["giris_tur", "gecerlilik", "durum"]] = [
        "piyasa",
        1,
        "TETIKLENDI",
    ]
    kesisim_gunu = pd.Series(kapanis.index, index=kapanis.index).shift(k)
    for t in giris.index[giris]:
        s.loc[t, "kural_durumu"] = (
            f"{tur} {cift} yukarı kesişim {kesisim_gunu[t].date()}, teyit_gun {k}"
        )
    return s


STRATEJI = Strateji(
    ad="ortalama-kesisim",
    tur="giris",
    sinif="b",
    zaman="gunluk",
    kaynaklar=("stratejiler/ortalama-kesisim.md",),
    kaynak_tarihleri=(
        "2024-02-23",
        "2024-03-03",
        "2024-03-23",
        "2024-08-31",
        "2024-09-21",
        "2024-10-16",
        "2024-10-18",
        "2024-10-30",
    ),
    varsayilan={"ortalama": "EMA", "cift": "50/200", "teyit_gun": 0},
    aralik={
        "ortalama": ("EMA", "SMA", "WMA"),
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
