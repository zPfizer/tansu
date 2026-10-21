"""STE farkı (kurulum/ste_fark.py): yönerge dosyalarına eklenen satırlar linter'a gider.

Testler betiği alt süreç olarak çalıştırır; beklenen değerler sabittir.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

BETIK = Path(__file__).resolve().parents[1] / "kurulum" / "ste_fark.py"

SAHTE_LINTER = (
    "import sys\n"
    "metin = sys.stdin.read()\n"
    "print('linter girdisi:', metin.strip())\n"
    "sys.exit(1 if ';' in metin else 0)\n"
)


def _kos(*argv, cwd=None, env=None):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(BETIK), *argv],
        capture_output=True,
        encoding="utf-8",
        cwd=cwd,
        env=env,
    )


def _git(kok, *args):
    subprocess.run(
        ["git", "-c", "user.name=T", "-c", "user.email=t@example.com"]
        + ["-c", "commit.gpgsign=false", "-C", str(kok), *args],
        check=True,
        capture_output=True,
        encoding="utf-8",
    )


@pytest.fixture
def depo(tmp_path):
    """Eski AGENTS.md satırında noktalı virgül var; hepsi kayıtlı."""
    kok = tmp_path / "depo"
    kok.mkdir()
    _git(kok, "init", "-q", "-b", "main")
    (kok / "AGENTS.md").write_text("eski; satir\n", encoding="utf-8")
    (kok / "docs").mkdir()
    (kok / "docs" / "TASARIM.md").write_text("tasarim\n", encoding="utf-8")
    _git(kok, "add", "AGENTS.md", "docs/TASARIM.md")
    _git(kok, "commit", "-q", "-m", "ilk")
    return kok


@pytest.fixture
def linter(tmp_path):
    yol = tmp_path / "sahte_linter.py"
    yol.write_text(SAHTE_LINTER, encoding="utf-8")
    return yol


def _fark(depo, linter):
    return _kos("HEAD", str(linter), cwd=depo)


@pytest.mark.parametrize("satir", ["yeni; satir", "++ Check the file; run the gate."])
def test_ste_fark_eklenen_noktali_virgulde_kalir(depo, linter, satir):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write(satir + "\n")
    s = _fark(depo, linter)
    assert s.returncode == 1
    assert "ste-fark: eklenen satir = 1" in s.stdout
    assert f"linter girdisi: {satir}" in s.stdout


def test_ste_fark_eski_noktali_virgul_ve_temiz_ekleme_gecer(depo, linter):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("yeni temiz satir\n")
    s = _fark(depo, linter)
    assert "ste-fark: eklenen satir = 1" in s.stdout
    assert "linter girdisi: yeni temiz satir" in s.stdout
    assert "eski" not in s.stdout
    assert s.returncode == 0


def test_ste_fark_yonerge_disi_dosya_sayilmaz(depo, linter):
    (depo / "docs" / "TASARIM.md").write_text("tasarim; degisti\n", encoding="utf-8")
    s = _fark(depo, linter)
    assert (s.returncode, s.stdout) == (0, "ste-fark: eklenen satir = 0\n")


def test_ste_fark_linter_dosyasi_yoksa_kalir(depo, tmp_path):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("yeni temiz satir\n")
    yok = tmp_path / "yok.py"
    s = _fark(depo, yok)
    assert s.returncode == 1
    assert f"ste-fark: linter yok: {yok}" in s.stdout


def test_ste_fark_varsayilan_linter_ev_klasorundedir(depo, tmp_path):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("yeni temiz satir\n")
    ev = tmp_path / "ev"
    ev.mkdir()
    env = {**os.environ, "USERPROFILE": str(ev), "HOME": str(ev)}
    s = _kos("HEAD", cwd=depo, env=env)
    beklenen = ev / ".claude" / "skills" / "asd-ste100" / "scripts" / "ste-lint.py"
    assert s.returncode == 1
    assert f"ste-fark: linter yok: {beklenen}" in s.stdout


def test_ste_fark_taban_dal_noktasindan_sonra_ilerlediyse_dal_eklemez(depo, linter):
    (depo / "AGENTS.md").write_text("eski temiz satir\n", encoding="utf-8")
    _git(depo, "commit", "-q", "-am", "temiz satir")
    _git(depo, "switch", "-q", "-c", "dal")
    _git(depo, "switch", "-q", "main")
    (depo / "AGENTS.md").write_text("main yeni satir\n", encoding="utf-8")
    _git(depo, "commit", "-q", "-am", "main ilerler")
    _git(depo, "switch", "-q", "dal")
    s = _kos("main", str(linter), cwd=depo)
    assert (s.returncode, s.stdout) == (0, "ste-fark: eklenen satir = 0\n")


def test_ste_fark_ikinci_dosya_basligini_lintera_gondermez(depo, linter):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("++ Check the file; run the gate.\n")
    (depo / "CLAUDE.md").write_text("Read the file.\n", encoding="utf-8")
    _git(depo, "add", "CLAUDE.md")
    s = _fark(depo, linter)
    assert s.returncode == 1
    assert s.stdout == (
        "ste-fark: eklenen satir = 2\n"
        "linter girdisi: ++ Check the file; run the gate.\nRead the file.\n"
    )
