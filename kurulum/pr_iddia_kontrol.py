"""PR gövdesindeki dosya, satır ve test sayısı iddialarını GitHub'daki gerçek değerlerle karşılaştırır.

Denetim:
- Değişen her dosya gövdede backtick içinde geçer: tam yol, `klasor/` ya da `tests/test_*.py` gibi bir desen.
  Adı değişen dosyalar arasında tek olan dosya klasörsüz adıyla da yazılabilir.
- Dosya adının hemen ardındaki `+E -S` o dosyanın eklenen ve silinen satırıdır.
- Dosya adına bağlı olmayan `+E -S` ve `N files changed` PR toplamıdır. `N dosya` yalnız aynı satırda
  `+E -S` ya da `Toplam` varsa dosya sayısıdır.
- `pytest` geçen satırdaki test sayılarının toplamı, baş commit'in `ci` koşusundaki geçen ya da bütün test
  sayısıdır (yerelde koşan altın test CI'da atlanır). Satırda `tests/`, `test_x`, `::` ya da `-k` varsa
  kısmi koşudur, denetlenmez. CI bitmediyse ya da günlüğü okunamadıysa test sayısı denetlenmez.

Kullanım: python -X utf8 kurulum/pr_iddia_kontrol.py <PR> [--repo sahip/ad]  (varsayılan zPfizer/tansu)
Çıkış kodu: 0 iddialar uyuşuyor, 1 uyuşmazlık var.
"""

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

_SAYI = r"(\d[\d.]*)"
_ARTI_EKSI = rf"\+{_SAYI}\s*[,/]?\s*[-−–]{_SAYI}"
YOLLU = re.compile(rf"`([^`\n]+)`[\s:]*\(?\s*{_ARTI_EKSI}")
TOPLAM = re.compile(_ARTI_EKSI)
GIT_STAT = re.compile(r"(\d+) insertions?\(\+\)|(\d+) deletions?\(-\)")
DOSYA_SAYISI = re.compile(r"(?<![\w.])(\d+) (?:dosya|files? changed)(?!\w)", re.I)
DEGISEN_DOSYA = re.compile(r"(?<![\w.])(\d+) files? changed", re.I)
BACKTICK = re.compile(r"`([^`\n]+)`")
TEST_IDDIASI = re.compile(
    r"(\d[\d.]*) (?:tests? )?"
    r"(?:geçti|passed|atlandı|skipped|kaldı|başarısız|failed|hata|errors?)\b",
    re.I,
)
KISMI = re.compile(r"tests/|\btest_\w+|::|\s-k\s")
PYTEST_OZET = re.compile(r"(\d+) (passed|failed|skipped|errors?|xfailed|xpassed)\b")


def _sayi(metin):
    return int(metin.replace(".", ""))


def _kapsar(aday, yol, tek_adlar):
    if "/" not in aday and aday in tek_adlar:
        return PurePosixPath(yol).name == aday
    if aday.endswith("/"):
        return yol.startswith(aday)
    if any(isaret in aday for isaret in "*?["):
        return fnmatch.fnmatchcase(yol, aday)
    return aday == yol


def denetle(govde, pr, ci):
    """(sorunlar, notlar). `pr`: gh pr view JSON'u; `ci`: CI (geçen, bütün) test sayısı ya da None."""
    dosyalar = {d["path"]: d for d in pr["files"]}
    sorunlar, notlar = [], []
    if len(dosyalar) != pr["changedFiles"]:
        sorunlar.append(
            f"gh {len(dosyalar)} dosya verdi, PR {pr['changedFiles']}; liste denetlenemedi"
        )
    adaylar = [re.split(r"::|:\d|\s", t.strip())[0] for t in BACKTICK.findall(govde)]
    adlar = [PurePosixPath(yol).name for yol in dosyalar]
    tek_adlar = {ad for ad in adlar if adlar.count(ad) == 1}
    for yol in dosyalar:
        if not any(_kapsar(a, yol, tek_adlar) for a in adaylar if a):
            sorunlar.append(f"`{yol}` değişti ama gövdede adı yok")
    test_satiri = False
    for satir in govde.splitlines():
        for m in YOLLU.finditer(satir):
            yol, arti, eksi = m.group(1), _sayi(m.group(2)), _sayi(m.group(3))
            if yol not in dosyalar:
                sorunlar.append(
                    f"`{yol}` +{arti} -{eksi} denmiş, dosya PR'da değişmemiş"
                )
                continue
            gercek = (dosyalar[yol]["additions"], dosyalar[yol]["deletions"])
            if (arti, eksi) != gercek:
                sorunlar.append(
                    f"`{yol}`: gövde +{arti} -{eksi}, gerçek +{gercek[0]} -{gercek[1]}"
                )
        kalan = YOLLU.sub("", satir)
        for m in TOPLAM.finditer(kalan):
            arti, eksi = _sayi(m.group(1)), _sayi(m.group(2))
            if (arti, eksi) != (pr["additions"], pr["deletions"]):
                sorunlar.append(
                    f"toplam: gövde +{arti} -{eksi}, gerçek +{pr['additions']} -{pr['deletions']}"
                )
        for ekle, sil in GIT_STAT.findall(kalan):
            if ekle and _sayi(ekle) != pr["additions"]:
                sorunlar.append(
                    f"toplam: gövde {ekle} ekleme, gerçek {pr['additions']}"
                )
            if sil and _sayi(sil) != pr["deletions"]:
                sorunlar.append(f"toplam: gövde {sil} silme, gerçek {pr['deletions']}")
        toplam_satiri = TOPLAM.search(kalan) or re.search(r"toplam", kalan, re.I)
        sayilar = DOSYA_SAYISI if toplam_satiri else DEGISEN_DOSYA
        for sayi in sayilar.findall(kalan):
            if int(sayi) != pr["changedFiles"]:
                sorunlar.append(
                    f"dosya sayısı: gövde {sayi}, gerçek {pr['changedFiles']}"
                )
        iddia = TEST_IDDIASI.findall(satir)
        if "pytest" not in satir.lower() or not iddia:
            continue
        if KISMI.search(satir):
            notlar.append(f"kısmi pytest satırı denetlenmedi: {satir.strip()}")
            continue
        test_satiri = True
        toplam = sum(map(_sayi, iddia))
        if ci is not None and toplam not in ci:
            sorunlar.append(
                f"pytest: gövde {toplam} test, CI {ci[0]} geçti ({ci[1]} test)"
            )
    if test_satiri and ci is None:
        notlar.append(
            "pytest sayısı denetlenmedi: baş commit'in ci koşusu yok, bitmedi ya da okunamadı"
        )
    return sorunlar, notlar


def _gh(*arglar):
    return subprocess.run(
        ["gh", *arglar], capture_output=True, check=True, encoding="utf-8"
    ).stdout


def ci_sayilari(sha, depo):
    """Baş commit'in bitmiş `ci` koşusunda (geçen, bütün) test sayısı: her işin son pytest özet satırı."""
    try:
        kosu = json.loads(
            _gh(
                "run",
                "list",
                "--commit",
                sha,
                "--workflow",
                "ci.yml",
                "--limit",
                "1",
                "--json",
                "databaseId,status",
                *depo,
            )
        )
        if not kosu or kosu[0]["status"] != "completed":
            return None
        gunluk = _gh("run", "view", str(kosu[0]["databaseId"]), "--log", *depo)
    except (
        subprocess.CalledProcessError
    ):  # gh geçici hata verdi: test sayısı denetlenmez
        return None
    son = {}
    for satir in gunluk.splitlines():
        if re.search(r" in [\d.]+s\b", satir) and PYTEST_OZET.search(satir):
            sonuc = {tur: int(n) for n, tur in PYTEST_OZET.findall(satir)}
            son[satir.split("\t", 1)[0]] = (sonuc.get("passed", 0), sum(sonuc.values()))
    if not son:
        return None
    return tuple(sum(sayilar) for sayilar in zip(*son.values(), strict=True))


def main():
    ayrac = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ayrac.add_argument("pr")
    ayrac.add_argument("--repo", default="zPfizer/tansu")
    arg = ayrac.parse_args()
    depo = ["--repo", arg.repo]
    alanlar = "body,files,additions,deletions,changedFiles,headRefOid"
    pr = json.loads(_gh("pr", "view", arg.pr, "--json", alanlar, *depo))
    sorunlar, notlar = denetle(pr["body"], pr, ci_sayilari(pr["headRefOid"], depo))
    for satir in notlar:
        print(f"Not: {satir}")
    for satir in sorunlar:
        print(f"UYUŞMAZLIK: {satir}")
    print(f"PR {arg.pr}: {len(sorunlar)} uyuşmazlık.")
    return 1 if sorunlar else 0


if __name__ == "__main__":
    sys.exit(main())
