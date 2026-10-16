"""SessionStart kancası: temiz ana depoyu (master) kaynak/master'a ilerletir.

Yalnız ana çalışma ağacında ve yalnız `git merge --ff-only` ile çalışır. Bağlı çalışma ağacına, izlenen dosyası değişmiş ağaca
(izlenmeyen dosyalar sayılmaz) ve başka dala dokunmaz; bu durumlarda yalnız uyarı satırı yazar. Oturumu hiçbir zaman bozmaz: hata olursa sessiz kalır.
"""

import os
import subprocess
import sys
from pathlib import Path


def _git(kok, *args, zaman=12):
    """git çıktısını (strip) döner; komut başarısızsa ya da git yoksa None."""
    try:
        s = subprocess.run(
            ["git", "-C", str(kok), *args],
            capture_output=True,
            encoding="utf-8",
            timeout=zaman,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
    except OSError, subprocess.SubprocessError:
        return None
    return s.stdout.strip() if s.returncode == 0 else None


def _ana_agac_mi(kok):
    dizin, ortak = (
        _git(kok, "rev-parse", "--git-dir"),
        _git(kok, "rev-parse", "--git-common-dir"),
    )
    return (
        dizin is not None
        and ortak is not None
        and (Path(kok) / dizin).resolve() == (Path(kok) / ortak).resolve()
    )


def guncelle(kok):
    """Uyarı satırını ("" = uyarı yok) döner; hata fırlatmaz."""
    if not _ana_agac_mi(kok) or "kaynak" not in (_git(kok, "remote") or "").split():
        return ""
    # Fetch başarısızsa eldeki kaynak/master ile devam edilir.
    _git(kok, "fetch", "-q", "kaynak")
    geride = _git(kok, "rev-list", "--count", "master..kaynak/master")
    if not geride or geride == "0":
        return ""
    uyari = f"TANSU master kaynak/master'ın {geride} kayıt gerisinde; kurallar eski olabilir"
    if (
        _git(kok, "branch", "--show-current") == "master"
        and _git(kok, "status", "--porcelain", "--untracked-files=no") == ""
        and _git(kok, "merge", "--ff-only", "-q", "kaynak/master") is not None
    ):
        return ""
    return uyari


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        satir = guncelle(Path.cwd())
    except Exception:  # noqa: BLE001 - kanca oturumu bozmamalı
        satir = ""
    if satir:
        print(satir)
