"""PR gövdesindeki dosya, satır ve test sayısı iddialarını GitHub'daki gerçek değerlerle karşılaştırır.

Denetim:
- Değişen her dosya gövdede backtick içinde geçer: tam yol, `klasor/` ya da `tests/test_*.py` gibi bir desen.
- Dosya adının hemen ardındaki `+E -S` o dosyanın eklenen ve silinen satırıdır.
- Dosya adına bağlı olmayan `N dosya`, `N files changed`, `+E -S` PR toplamıdır.
- `pytest` geçen satırdaki test sayılarının toplamı, baş commit'in `ci` koşusundaki pytest toplamıdır.
  Satırda `tests/`, `::` ya da `-k` varsa kısmi koşudur, denetlenmez. CI bitmediyse test sayısı denetlenmez.

Kullanım: python -X utf8 kurulum/pr_iddia_kontrol.py <PR> [--repo sahip/ad]
Çıkış kodu: 0 iddialar uyuşuyor, 1 uyuşmazlık var.
"""

import argparse
import fnmatch
import json
import re
import subprocess
import sys

_SAYI = r"(\d[\d.]*)"
_ARTI_EKSI = rf"\+{_SAYI}\s*[,/]?\s*[-−–]{_SAYI}"
YOLLU = re.compile(rf"`([^`\n]+)`[\s:]*\(?\s*{_ARTI_EKSI}")
TOPLAM = re.compile(_ARTI_EKSI)
GIT_STAT = re.compile(r"(\d+) insertions?\(\+\)|(\d+) deletions?\(-\)")
DOSYA_SAYISI = re.compile(r"(?<![\w.])(\d+) (?:dosya|files? changed)(?!\w)", re.I)
BACKTICK = re.compile(r"`([^`\n]+)`")
TEST_IDDIASI = re.compile(
    r"(\d[\d.]*) (?:geçti|passed|atlandı|skipped|kaldı|başarısız|failed|hata|errors?)\b",
    re.I,
)
PYTEST_OZET = re.compile(r"(\d+) (?:passed|failed|skipped|errors?|xfailed|xpassed)\b")


def _sayi(metin):
    return int(metin.replace(".", ""))


def _kapsar(aday, yol):
    if aday.endswith("/"):
        return yol.startswith(aday)
    if any(isaret in aday for isaret in "*?["):
        return fnmatch.fnmatchcase(yol, aday)
    return aday == yol


def denetle(govde, pr, ci_toplami):
    """(sorunlar, notlar). `pr`: gh pr view JSON'u; `ci_toplami`: CI pytest toplamı ya da None."""
    dosyalar = {d["path"]: d for d in pr["files"]}
    sorunlar, notlar = [], []
    if len(dosyalar) != pr["changedFiles"]:
        sorunlar.append(
            f"gh {len(dosyalar)} dosya verdi, PR {pr['changedFiles']}; liste denetlenemedi"
        )
    adaylar = [re.split(r"::|:\d|\s", t.strip())[0] for t in BACKTICK.findall(govde)]
    for yol in dosyalar:
        if not any(_kapsar(a, yol) for a in adaylar if a):
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
        for sayi in DOSYA_SAYISI.findall(kalan):
            if int(sayi) != pr["changedFiles"]:
                sorunlar.append(
                    f"dosya sayısı: gövde {sayi}, gerçek {pr['changedFiles']}"
                )
        iddia = TEST_IDDIASI.findall(satir)
        if "pytest" not in satir.lower() or not iddia:
            continue
        if re.search(r"tests/|::|\s-k\s", satir):
            notlar.append(f"kısmi pytest satırı denetlenmedi: {satir.strip()}")
            continue
        test_satiri = True
        toplam = sum(map(_sayi, iddia))
        if ci_toplami is not None and toplam != ci_toplami:
            sorunlar.append(f"pytest: gövde {toplam} test, CI {ci_toplami} test")
    if test_satiri and ci_toplami is None:
        notlar.append(
            "pytest sayısı denetlenmedi: baş commit'in ci koşusu yok ya da bitmedi"
        )
    return sorunlar, notlar


def _gh(*arglar):
    return subprocess.run(
        ["gh", *arglar], capture_output=True, check=True, encoding="utf-8"
    ).stdout


def ci_toplami(sha, depo):
    """Baş commit'in bitmiş `ci` koşusunda her işin son pytest özet satırının toplamı."""
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
    son = {}
    for satir in _gh(
        "run", "view", str(kosu[0]["databaseId"]), "--log", *depo
    ).splitlines():
        if re.search(r" in [\d.]+s\b", satir) and PYTEST_OZET.search(satir):
            son[satir.split("\t", 1)[0]] = sum(map(int, PYTEST_OZET.findall(satir)))
    return sum(son.values()) if son else None


def main():
    ayrac = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ayrac.add_argument("pr")
    ayrac.add_argument("--repo")
    arg = ayrac.parse_args()
    depo = ["--repo", arg.repo] if arg.repo else []
    alanlar = "body,files,additions,deletions,changedFiles,headRefOid"
    pr = json.loads(_gh("pr", "view", arg.pr, "--json", alanlar, *depo))
    sorunlar, notlar = denetle(pr["body"], pr, ci_toplami(pr["headRefOid"], depo))
    for satir in notlar:
        print(f"Not: {satir}")
    for satir in sorunlar:
        print(f"UYUŞMAZLIK: {satir}")
    print(f"PR {arg.pr}: {len(sorunlar)} uyuşmazlık.")
    return 1 if sorunlar else 0


if __name__ == "__main__":
    sys.exit(main())
