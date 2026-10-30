"""Açık depo taraması: izlenen dosyalarda yerel yol, kasa yolu, Tansu kodu ve tweet kimliği olmaz.

Kural: AGENTS.md "Keep Tansu quotes, tweet ids, brain paths and local paths out of Git" (SPEC Ek B #12).
PowerShell `-EncodedCommand` değeri (base64, UTF-16LE) açılıp aynı desenlerle taranır.
Bulgu yalnız dosya, satır ve desen adını yazar; değeri yazmaz, çünkü CI günlüğü de açıktır.
`ci` iş akışı yalnız `.md` değişince atlanır; bu yüzden `denetim` iş akışı bu dosyayı tek başına koşar.
"""

import base64
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

# Karakter sınıfları bu dosyanın kendi taramasında takılmasını önler.
YASAK = re.compile(
    r"(?P<kullanici_klasoru>C:[\\/]Users)|(?P<app_data>App[D]ata)|(?P<kasa>YON[E]TIM)"
    r"|(?P<tansu_kodu>Tansu['’]nun kodu)"
    # 15+ haneli kimlik; ondalık kesrin ve SHA'nın içindeki rakam dizisi kimlik değildir.
    r"|(?P<uzun_kimlik>(?<![\w.])\d{15,}(?!\w|\.\d))",
    re.IGNORECASE,
)
# `-EncodedCommand` ve PowerShell'in kabul ettiği kısaltmaları (`-enc`, `-e`, `-ec`).
KODLU = re.compile(r"(?<![\w-])-e\w*\s+([A-Za-z0-9+/]{20,}={0,2})", re.IGNORECASE)


def _satir(metin, yer):
    return metin.count("\n", 0, yer) + 1


def dosya_bulgulari(ad, metin):
    """'ad:satır: desen' listesi; kodlu komuttaki bulgu 'kodlu desen' olarak yazılır."""
    bulgu = [
        f"{ad}:{_satir(metin, m.start())}: {m.lastgroup}" for m in YASAK.finditer(metin)
    ]
    for kod in KODLU.finditer(metin):
        try:
            acik = base64.b64decode(kod.group(1), validate=True).decode("utf-16-le")
        except ValueError:  # base64 ya da UTF-16 değil: komut değildir
            continue
        satir = _satir(metin, kod.start())
        bulgu += [f"{ad}:{satir}: kodlu {m.lastgroup}" for m in YASAK.finditer(acik)]
    return bulgu


def bulgular():
    adlar = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=KOK,
        capture_output=True,
        check=True,
        encoding="utf-8",
    ).stdout.split("\0")
    bulgu = []
    for ad in filter(None, adlar):
        yol = KOK / ad
        if yol.is_file():
            bulgu += dosya_bulgulari(ad, yol.read_bytes().decode("utf-8", "ignore"))
    return bulgu


def test_izlenen_dosyalarda_ozel_bilgi_yok():
    assert bulgular() == []


def test_kodlu_komut_acilip_taranir():
    gizli = "& 'C:" + "\\Users\\x\\a.py'"
    kod = base64.b64encode(gizli.encode("utf-16-le")).decode()
    metin = f'{{\n  "command": "powershell -NoProfile -EncodedCommand {kod}"\n}}'
    assert dosya_bulgulari("a.json", metin) == ["a.json:2: kodlu kullanici_klasoru"]


def test_uzun_kimlik_kesir_ve_sha_degildir():
    kimlik = "1" * 19
    metin = "\n".join(
        [
            f"id {kimlik}.",
            f"https://x.com/a/status/{kimlik}",
            "0." + "8" * 16,
            "1" * 20 + "ee" + "0" * 18,
            "1" * 14,
        ]
    )
    assert dosya_bulgulari("a.md", metin) == [
        "a.md:1: uzun_kimlik",
        "a.md:2: uzun_kimlik",
    ]


if __name__ == "__main__":
    kalan = bulgular()
    print("\n".join(kalan) or "Açık depo taraması temiz.")
    sys.exit(1 if kalan else 0)
