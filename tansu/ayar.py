"""Ayar, ileri yürüme ve parametre dosyası (SPEC 4, 5.7). Dosya yazan tek yer `yaz`."""

import datetime as dt
import json
import multiprocessing
import os
import subprocess
import threading
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

from tansu import dosya, sinama, veri
from tansu.strateji import Strateji

ISCI = min(16, os.cpu_count() or 1)
AYAR_KOKU = Path("stratejiler/ayarlar")
TEST_YIL = 0.5


class Pencere(NamedTuple):
    """İleri yürümenin bir adımı: eğitim 04.01.2021'den `test_bas`ın önceki gününe (çapalı), test sinyal tarihine göre."""

    ad: str
    test_bas: pd.Timestamp
    test_son: pd.Timestamp

    @property
    def egitim_son(self) -> pd.Timestamp:
        return self.test_bas - pd.Timedelta(days=1)

    @property
    def egitim_yil(self) -> float:
        """Eğitimin tam ay sayısı / 12: ilk adım 2,0, sonra her adım +0,5."""
        bas, son = sinama.ILK_GIRIS, self.egitim_son
        return ((son.year - bas.year) * 12 + son.month - bas.month + 1) / 12


PENCERELER = (
    Pencere("2023H1", pd.Timestamp("2023-01-01"), pd.Timestamp("2023-06-30")),
    Pencere("2023H2", pd.Timestamp("2023-07-01"), pd.Timestamp("2023-12-31")),
    Pencere("2024H1", pd.Timestamp("2024-01-01"), pd.Timestamp("2024-06-30")),
    Pencere("2024H2", pd.Timestamp("2024-07-01"), pd.Timestamp("2024-12-31")),
    Pencere("2025H1", pd.Timestamp("2025-01-01"), pd.Timestamp("2025-06-30")),
    Pencere("2025H2", pd.Timestamp("2025-07-01"), pd.Timestamp("2025-12-31")),
)


@dataclass(frozen=True)
class Izgara:
    """`aralik` eksenlerinin çarpımı, listelenen sırayla; nokta satır öncelikli sıra numarasıdır."""

    strateji: Strateji

    def __post_init__(self):
        for k, degerler in self.strateji.aralik.items():
            if self.strateji.varsayilan[k] not in degerler:
                raise ValueError(f"{self.strateji.ad}: varsayılan {k} ızgarada yok")

    @property
    def sekil(self) -> tuple[int, ...]:
        return tuple(len(v) for v in self.strateji.aralik.values())

    def __len__(self) -> int:
        return int(np.prod(self.sekil))

    def eksenler(self, i: int) -> dict[str, float | str]:
        sira = np.unravel_index(i, self.sekil)
        return {
            k: v[int(j)]
            for (k, v), j in zip(self.strateji.aralik.items(), sira, strict=True)
        }

    def parametre(self, i: int) -> dict[str, float | str]:
        return {**self.strateji.varsayilan, **self.eksenler(i)}

    @property
    def varsayilan_nokta(self) -> int:
        v = self.strateji.varsayilan
        sira = tuple(d.index(v[k]) for k, d in self.strateji.aralik.items())
        return int(np.ravel_multi_index(sira, self.sekil))

    def komsular(self, i: int) -> list[int]:
        """Tek eksende ±1 adım; kategorik eksende listelenen sıra; çapraz yok (SPEC 5.7)."""
        sira = np.unravel_index(i, self.sekil)
        sonuc = []
        for eksen, boy in enumerate(self.sekil):
            for adim in (-1, 1):
                j = int(sira[eksen]) + adim
                if 0 <= j < boy:
                    yeni = list(sira)
                    yeni[eksen] = j
                    sonuc.append(int(np.ravel_multi_index(yeni, self.sekil)))
        return sonuc


@dataclass(frozen=True)
class Secim:
    """Bir eğitim sonundaki seçim. `puan`, `saglam`, `n` ızgara sırasında; NaN puansız."""

    nokta: int
    parametre: dict[str, float | str]
    puan: np.ndarray
    saglam: np.ndarray
    n: np.ndarray
    puanli: bool

    @property
    def puanli_sayisi(self) -> int:
        return int(np.isfinite(self.puan).sum())


@dataclass(frozen=True)
class Adim:
    pencere: Pencere
    secim: Secim
    ic_n: int
    ic_yillik: float
    test: sinama.Kosu
    dis_yillik: float
    verim: float | None


@dataclass(frozen=True)
class Yuruyus:
    izgara: Izgara
    adimlar: tuple[Adim, ...]
    dis_ornek: sinama.Kosu
    verim: float | None
    verim_adim: int
    son: Secim


def egitim(islemler: pd.DataFrame, son: pd.Timestamp) -> pd.DataFrame:
    """İçeride kapanan kurulumlar (SPEC 5.7): sinyal ve çıkış `son`a kadar ve `acik` değil."""
    return islemler[
        (islemler["sinyal_tarihi"] <= son)
        & ~islemler["acik"].astype(bool)
        & (islemler["cikis_tarihi"] <= son)
    ]


def saglam(puan: np.ndarray, izgara: Izgara) -> np.ndarray:
    """Sağlam puan: puanlı noktanın kendisi ve puanlı komşularının medyanı; ikiden az puanlı komşu: ızgaranın en düşük puanı."""
    sonuc = np.full(len(puan), np.nan)
    if np.isnan(puan).all():
        return sonuc
    en_dusuk = np.nanmin(puan)
    for i in np.flatnonzero(~np.isnan(puan)):
        komsu = [puan[j] for j in izgara.komsular(i) if not np.isnan(puan[j])]
        sonuc[i] = np.median([puan[i], *komsu]) if len(komsu) >= 2 else en_dusuk
    return sonuc


def sec(
    izgara: Izgara, kosular: list[sinama.Kosu], son: pd.Timestamp, olcu: str
) -> Secim:
    """En iyi sağlam puan; eşitlikte yüksek kendi puanı, sonra düşük sıra. Puanlı nokta yoksa varsayılanlar."""
    satirlar = [egitim(k.islemler, son) for k in kosular]
    n = np.array([len(x) for x in satirlar])
    puan = np.array(
        [x[olcu].mean() if len(x) >= sinama.EN_AZ else np.nan for x in satirlar]
    )
    s = saglam(puan, izgara)
    puanli = bool(np.isfinite(s).any())
    nokta = (
        min(np.flatnonzero(np.isfinite(s)), key=lambda i: (-s[i], -puan[i], i))
        if puanli
        else izgara.varsayilan_nokta
    )
    return Secim(int(nokta), izgara.parametre(nokta), puan, s, n, puanli)


def _adim(
    izgara: Izgara, kosular: list[sinama.Kosu], pencere: Pencere, olcu: str
) -> Adim:
    secim = sec(izgara, kosular, pencere.egitim_son, olcu)
    kosu = kosular[secim.nokta]
    ic = egitim(kosu.islemler, pencere.egitim_son)
    test = kosu.kes(pencere.test_bas, pencere.test_son)
    ic_yillik = float(ic[olcu].sum()) / pencere.egitim_yil
    dis_yillik = test.toplam / TEST_YIL
    verim = dis_yillik / ic_yillik if secim.puanli and ic_yillik > 0 else None
    return Adim(pencere, secim, len(ic), ic_yillik, test, dis_yillik, verim)


_GUNLER: sinama.Gunler | None = None


def _hazirla(gunler: sinama.Gunler) -> None:
    global _GUNLER
    _GUNLER = gunler
    # Ebeveyn ölünce işçi kendini kapatır; yoksa Windows'ta yetim kalır (denetim 31.10.2026).
    ebeveyn = multiprocessing.parent_process()
    threading.Thread(target=lambda: (ebeveyn.join(), os._exit(1)), daemon=True).start()


def _nokta(arg: tuple[Strateji, dict]) -> sinama.Kosu:
    strateji, p = arg
    return sinama.calistir(strateji, _GUNLER, p, sinama.GECMIS)


def _kos(
    strateji: Strateji, gunler: sinama.Gunler, izgara: Izgara, isci: int
) -> list[sinama.Kosu]:
    """Her ızgara noktası için bir `GECMIS` koşusu, ızgara sırasında. Çağıran `if __name__ == "__main__"` arkasında olmalı."""
    ps = [izgara.parametre(i) for i in range(len(izgara))]
    isci = min(isci, len(ps))
    if isci == 1:
        return [sinama.calistir(strateji, gunler, p, sinama.GECMIS) for p in ps]
    with ProcessPoolExecutor(isci, initializer=_hazirla, initargs=(gunler,)) as ex:
        return list(ex.map(_nokta, [(strateji, p) for p in ps]))


def yuru(strateji: Strateji, gunler: sinama.Gunler, isci: int | None = None) -> Yuruyus:
    """Izgara bir kez `GECMIS` üzerinde koşar (31.12.2025 sonrası fiyat yok), sonra dilimlenir. Dosya yazmaz."""
    izgara = Izgara(strateji)
    olcu = strateji.olcu
    kosular = _kos(strateji, gunler, izgara, isci or ISCI)
    adimlar = tuple(_adim(izgara, kosular, pw, olcu) for pw in PENCERELER)
    dis_ornek = sinama.Kosu(
        pd.concat(
            [a.test.islemler.assign(pencere=a.pencere.ad) for a in adimlar],
            ignore_index=True,
        ),
        pd.concat([a.test.sinyaller for a in adimlar], ignore_index=True),
        Counter(),
        olcu,
    )
    verimler = [a.verim for a in adimlar if a.verim is not None]
    return Yuruyus(
        izgara,
        adimlar,
        dis_ornek,
        float(np.mean(verimler)) if verimler else None,
        len(verimler),
        sec(izgara, kosular, sinama.KESIM, olcu),
    )


class Okunan(NamedTuple):
    parametreler: dict[str, float | str]
    tarih: str


def _json(yol: Path) -> dict:
    try:
        icerik = json.loads(yol.read_text(encoding="utf-8"))
    except json.JSONDecodeError as hata:
        raise veri.VeriHatasi(f"{yol}: geçersiz JSON ({hata})") from hata
    except UnicodeDecodeError as hata:
        raise veri.VeriHatasi(f"{yol}: UTF-8 değil ({hata})") from hata
    except OSError as hata:
        raise veri.VeriHatasi(f"{yol}: okunamadı ({hata.strerror})") from hata
    if not isinstance(icerik, dict):
        raise veri.VeriHatasi(f"{yol}: JSON nesnesi değil")
    return icerik


def oku(strateji: Strateji, kok: Path, *, gerekli: bool = False) -> Okunan | None:
    """`<kok>/<ad>.json`; dosya yoksa None, `gerekli` ise VeriHatasi.

    Her değer kendi anahtarının `aralik` ya da `secenek` kümesinde olmalı (bool değil); dışı VeriHatasi."""
    yol = kok / f"{strateji.ad}.json"
    if not yol.exists():
        if gerekli:
            raise veri.VeriHatasi(
                f"ayar dosyası yok: {yol}; dosyayı Git'ten geri al ya da `tansu ayarla {strateji.ad}` çalıştır"
            )
        return None
    icerik = _json(yol)
    p = icerik.get("parametreler")
    if not isinstance(p, dict):
        raise veri.VeriHatasi(f"{yol}: parametreler yok")
    for k, v in p.items():
        kume = strateji.aralik.get(k, strateji.secenek.get(k))
        if kume is None:
            raise veri.VeriHatasi(f"{yol}: bilinmeyen anahtar {k}")
        if isinstance(v, bool) or v not in kume:
            izinli = ", ".join(map(str, kume))
            raise veri.VeriHatasi(f"{yol}: {k} = {v!r} izinli değil ({izinli})")
    return Okunan({**strateji.varsayilan, **p}, str(icerik.get("tarih", "")))


def veri_kimlikleri(kok: Path) -> frozenset[str]:
    """`<kok>/*.json` ayarlarının `veri_kimligi` değerleri: budama bunları silmez, yedek bunları alır.

    Değer `veri.indir`in yazdığı biçimde olmalı; başkası, dosyayı söyleyen VeriHatasi'dır."""
    kimlikler = set()
    for yol in kok.glob("*.json"):
        k = _json(yol).get("veri_kimligi")
        if k is None:
            continue
        if not veri.kimlik_gecerli(k):
            raise veri.VeriHatasi(
                f"{yol}: veri_kimligi = {k!r} geçersiz; biçim YYYYMMDD-HHMM"
            )
        kimlikler.add(k)
    return frozenset(kimlikler)


def kod_surumu() -> str:
    """Kod sürümü; `tansu/` değişmişse `-kirli` ekli."""

    def git(*arg: str) -> str:
        return subprocess.run(
            ["git", *arg],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    try:
        sha, kirli = git("rev-parse", "HEAD"), git("status", "--porcelain", ".")
    except OSError, subprocess.CalledProcessError:
        return "bilinmiyor"
    return sha + ("-kirli" if kirli else "")


def _sayi(x) -> float | None:
    return float(x) if np.isfinite(x) else None


def yaz(strateji: Strateji, secim: Secim, *, veri_kimligi: str, kok: Path) -> Path:
    """Parametre dosyası (SPEC 4). `suzgecler` ve `liste_cikisi` `onayla`nındır; var olan değer korunur."""
    kok.mkdir(parents=True, exist_ok=True)
    yol = kok / f"{strateji.ad}.json"
    eski = _json(yol) if yol.exists() else {}
    icerik = {
        "parametreler": secim.parametre,
        "puanli": secim.puanli,
        "puan": _sayi(secim.puan[secim.nokta]),
        "saglam_puan": _sayi(secim.saglam[secim.nokta]),
        "n": int(secim.n[secim.nokta]),
        "kod_surumu": kod_surumu(),
        "tarih": dt.date.today().isoformat(),
        "veri_kimligi": veri_kimligi,
        "suzgecler": eski.get("suzgecler", []),
        "liste_cikisi": eski.get("liste_cikisi", False),
    }
    with dosya.atomik(yol) as gecici:
        gecici.write_text(
            json.dumps(icerik, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return yol
