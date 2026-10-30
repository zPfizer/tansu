import csv
import datetime as dt
import os
from pathlib import Path
from typing import Literal, assert_never, get_args

from tansu import veri

Durum = Literal[
    "taslak", "beklemede", "sinandi", "ayarlandi", "yetersiz-ornek", "sinyalde"
]
Komut = Literal["sina", "ayarla"]
DURUMLAR: tuple[Durum, ...] = get_args(Durum)
DOSYA = Path("stratejiler/durum.csv")
SUTUNLAR = ("ad", "durum", "tarih", "not")

GECIS: dict[Komut, frozenset[str]] = {
    "sina": frozenset({"taslak"}),
    "ayarla": frozenset(DURUMLAR) - {"beklemede"},
}


def hedef(komut: Komut, puanli: bool) -> Durum:
    match komut:
        case "sina":
            return "sinandi"
        case "ayarla":
            return "ayarlandi" if puanli else "yetersiz-ornek"
        case _:
            assert_never(komut)


def sonraki(komut: Komut, eski: str, puanli: bool) -> str:
    return hedef(komut, puanli) if eski in GECIS[komut] else eski


def reddeder(komut: Komut, eski: str) -> bool:
    return komut == "ayarla" and eski == "beklemede"


def yeniden_onay(komut: Komut, eski: str) -> bool:
    return komut == "ayarla" and eski == "sinyalde"


def sinanan(satirlar: list[dict[str, str]], ad: str) -> int:
    return sum(
        r["durum"] not in ("taslak", "beklemede") or r["ad"] == ad for r in satirlar
    )


def oku(yol: Path = DOSYA) -> list[dict[str, str]]:
    with yol.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _satir(satirlar: list[dict[str, str]], ad: str) -> dict[str, str]:
    satir = next((r for r in satirlar if r["ad"] == ad), None)
    if satir is None:
        raise veri.VeriHatasi(f"{ad}: durum.csv içinde yok")
    return satir


def durumu(satirlar: list[dict[str, str]], ad: str) -> str:
    return _satir(satirlar, ad)["durum"]


def gec(ad: str, komut: Komut, *, puanli: bool, yol: Path = DOSYA) -> str:
    """Dosyayı yeniden okur: ızgara sürerken başka koşu satırları değiştirmiş olabilir."""
    satirlar = oku(yol)
    satir = _satir(satirlar, ad)
    eski = satir["durum"]
    if eski in GECIS[komut]:
        satir.update(
            durum=sonraki(komut, eski, puanli), tarih=dt.date.today().isoformat()
        )
        gecici = yol.with_name(yol.name + ".tmp")
        with gecici.open("w", encoding="utf-8", newline="") as f:
            yazici = csv.DictWriter(f, SUTUNLAR, lineterminator="\n")
            yazici.writeheader()
            yazici.writerows(satirlar)
        os.replace(gecici, yol)
    return satir["durum"]
