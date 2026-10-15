"""CI `kayit/ yalnız eklenir` adımı (bilet 08): ci.yml'deki betik geçici git deposunda gerçekten koşar.

Betik ci.yml'den okunur; test onu `bash` ile `origin/<taban>` olan bir klon içinde çalıştırır.
Ağa çıkmaz. bash yoksa atlanır.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

CI = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"


def _bash():
    git = shutil.which("git")
    if (
        git and os.name == "nt"
    ):  # PATH'teki bash.exe WSL olabilir; Git'in kendi bash'ini kullan
        adaylar = [p / "bin" / "bash.exe" for p in Path(git).parents]
    else:
        adaylar = [Path(shutil.which("bash") or "/yok")]
    return next((str(a) for a in adaylar if a.exists()), None)


def _betik():
    satirlar = CI.read_text(encoding="utf-8").splitlines()
    basla = next(
        i for i, s in enumerate(satirlar) if "name: kayit/ yalnız eklenir" in s
    )
    run = next(
        i for i in range(basla, len(satirlar)) if satirlar[i].strip() == "run: |"
    )
    govde = []
    for satir in satirlar[run + 1 :]:
        if satir.strip() and not satir.startswith(" " * 10):
            break
        govde.append(satir[10:])
    return "\n".join(govde) + "\n"


def _git(cwd, *args):
    subprocess.run(
        ["git", "-c", "core.autocrlf=false", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


@pytest.fixture
def klon(tmp_path):
    kaynak = tmp_path / "kaynak"
    kaynak.mkdir()
    _git(kaynak, "init", "-q", "-b", "master")
    _git(kaynak, "config", "user.email", "a@b.c")
    _git(kaynak, "config", "user.name", "n")
    (kaynak / "kayit").mkdir()
    (kaynak / "kayit" / "x.jsonl").write_text("a\nb\n", encoding="utf-8", newline="\n")
    (kaynak / "kayit" / "bos.jsonl").write_text("", encoding="utf-8")
    (kaynak / "kayit" / "ikili.bin").write_bytes(b"a\x00b\x00")
    _git(kaynak, "add", "kayit")
    _git(kaynak, "commit", "-q", "-m", "taban")
    hedef = tmp_path / "klon"
    subprocess.run(
        ["git", "-c", "core.autocrlf=false", "clone", "-q", str(kaynak), str(hedef)],
        check=True,
    )
    _git(hedef, "config", "user.email", "a@b.c")
    _git(hedef, "config", "user.name", "n")
    _git(hedef, "checkout", "-q", "-b", "dal")
    return hedef


def _kos(klon, taban="master"):
    bash = _bash()
    if bash is None:
        pytest.skip("bash yok.")
    return subprocess.run(
        [bash, "-c", _betik()],
        cwd=klon,
        env={**os.environ, "BASE": taban},
        capture_output=True,
        encoding="utf-8",
    )


def _kaydet(klon):
    _git(klon, "add", "-A", "--", "kayit")
    _git(klon, "commit", "-q", "-m", "dal")


def test_betik_pipefail_ve_no_renames_icerir():
    betik = _betik()
    assert "set -eu" in betik
    assert "set -o pipefail" in betik
    assert "--no-renames" in betik
    assert "rev-parse --verify" in betik


def test_satir_eklemek_gecer(klon):
    with (klon / "kayit" / "x.jsonl").open("a", encoding="utf-8", newline="\n") as f:
        f.write("c\n")
    _kaydet(klon)
    sonuc = _kos(klon)
    assert sonuc.returncode == 0, sonuc.stdout + sonuc.stderr


def test_yeni_dosya_eklemek_gecer(klon):
    (klon / "kayit" / "yeni.jsonl").write_text("a\n", encoding="utf-8", newline="\n")
    _kaydet(klon)
    assert _kos(klon).returncode == 0


def test_satir_degistirmek_kirmizi(klon):
    (klon / "kayit" / "x.jsonl").write_text("a\nB\n", encoding="utf-8", newline="\n")
    _kaydet(klon)
    sonuc = _kos(klon)
    assert sonuc.returncode == 1
    assert "yalnız satır ekler" in sonuc.stdout


def test_dosya_silmek_kirmizi(klon):
    (klon / "kayit" / "x.jsonl").unlink()
    _kaydet(klon)
    assert _kos(klon).returncode == 1


def test_dosya_yeniden_adlandirmak_kirmizi(klon):
    _git(klon, "mv", "kayit/x.jsonl", "kayit/y.jsonl")
    _kaydet(klon)
    assert _kos(klon).returncode == 1


def test_taban_bulunamazsa_kirmizi(klon):
    sonuc = _kos(klon, taban="yok-dal")
    assert sonuc.returncode == 1
    assert "origin/yok-dal bulunamadı" in sonuc.stdout


def test_bos_dosya_silmek_gecer_bilinen_sinir(klon):
    # Sınır (bilet 08 notu): numstat silinen satır sayar; satırı olmayan dosyanın silinmesi 0 görünür.
    (klon / "kayit" / "bos.jsonl").unlink()
    _kaydet(klon)
    assert _kos(klon).returncode == 0


def test_ikili_dosya_silmek_kirmizi(klon):
    # numstat ikili dosyada `-` yazar; adım bunu 1 silinen satır sayar
    (klon / "kayit" / "ikili.bin").unlink()
    _kaydet(klon)
    assert _kos(klon).returncode == 1
