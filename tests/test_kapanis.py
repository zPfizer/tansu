"""Kapanış betiği (`kurulum/kapanis.py`): birleşen PR'ın iş klasörünü kapatır.

Testler gerçek git depoları kurar: uzak (bare, adı `origin`), ana depo (main) ve `1-x` dalındaki iş klasörü.
"""

import subprocess
import sys
from pathlib import Path

import pytest

BETIK = Path(__file__).resolve().parents[1] / "kurulum" / "kapanis.py"


@pytest.fixture(autouse=True)
def _git_kimlik(monkeypatch):
    for ad in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{ad}_NAME", "Test")
        monkeypatch.setenv(f"GIT_{ad}_EMAIL", "test@example.com")
    monkeypatch.setenv("GIT_CONFIG_COUNT", "2")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "commit.gpgsign")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "false")
    monkeypatch.setenv("GIT_CONFIG_KEY_1", "core.autocrlf")
    monkeypatch.setenv("GIT_CONFIG_VALUE_1", "false")


def _git(klasor, *args):
    return subprocess.run(
        ["git", "-C", str(klasor), *args],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.strip()


def _kayit(klasor, ad):
    (klasor / "a.txt").write_text(ad, encoding="utf-8")
    _git(klasor, "add", "a.txt")
    _git(klasor, "commit", "-q", "-m", ad)


def _kapanis(is_klasoru, cwd=None):
    return subprocess.run(
        [sys.executable, "-I", "-X", "utf8", str(BETIK), str(is_klasoru)],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
    )


@pytest.fixture
def depo(tmp_path):
    """PR uzakta main dalına birleşti (ff); uzak dal henüz silinmedi. Döner: (ana, is, birleşen sha)."""
    uzak, ana, is_ = tmp_path / "uzak.git", tmp_path / "ana", tmp_path / "is"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(uzak)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(ana)], check=True)
    _kayit(ana, "bir")
    _git(ana, "remote", "add", "origin", str(uzak))
    _git(ana, "push", "-q", "origin", "main")
    _git(ana, "worktree", "add", "-q", "-b", "1-x", str(is_))
    _kayit(is_, "iki")
    _git(is_, "push", "-q", "origin", "1-x")
    _git(is_, "push", "-q", "origin", "1-x:main")
    return ana, is_, _git(is_, "rev-parse", "HEAD")


def test_kapanis_uc_kanit_satiri(depo):
    ana, is_, sha = depo
    _git(ana, "push", "-q", "origin", "--delete", "1-x")
    sonuc = _kapanis(is_)
    assert sonuc.stdout.splitlines() == [
        f"kapanis: ana HEAD {sha} = origin/main",
        "kapanis: is klasoru yok",
        "kapanis: uzak dal yok",
    ]
    assert sonuc.returncode == 0
    assert not is_.exists()
    assert _git(ana, "branch", "--list", "1-x") == ""
    assert _git(ana, "rev-parse", "HEAD") == sha


def test_kapanis_uzak_dal_duruyorsa_durur(depo):
    ana, is_, sha = depo
    sonuc = _kapanis(is_)
    assert sonuc.stdout.splitlines() == [
        f"kapanis: ana HEAD {sha} = origin/main",
        "kapanis: is klasoru yok",
    ]
    assert "kapanis: uzak dal var: 1-x" in sonuc.stderr
    assert sonuc.returncode == 1


def test_kapanis_ana_klasor_main_degilse_hic_degistirmeden_durur(depo):
    ana, is_, _ = depo
    _git(ana, "switch", "-q", "-c", "baska")
    sonuc = _kapanis(is_)
    assert sonuc.stdout == ""
    assert "kapanis: ana klasor main uzerinde degil" in sonuc.stderr
    assert sonuc.returncode == 1
    assert is_.exists()


def test_kapanis_kirli_is_klasorunu_silmez(depo):
    ana, is_, _ = depo
    (is_ / "yeni.txt").write_text("kayip olmasin", encoding="utf-8")
    sonuc = _kapanis(is_)
    assert sonuc.stdout == ""
    assert "untracked" in sonuc.stderr
    assert sonuc.returncode == 1
    assert (is_ / "yeni.txt").exists()


@pytest.mark.parametrize("alt", ["", "alt"])
def test_kapanis_is_klasoru_icinden_calisirsa_hic_degistirmeden_durur(depo, alt):
    # Windows cannot delete a folder that is the working directory of a process.
    ana, is_, sha = depo
    (is_ / "alt").mkdir()
    sonuc = _kapanis(is_, cwd=is_ / alt)
    assert sonuc.stdout == ""
    assert sonuc.stderr.startswith("kapanis: ")
    assert "ana klasorden" in sonuc.stderr
    assert sonuc.returncode == 1
    assert is_.exists()
    assert _git(ana, "branch", "--list", "1-x") != ""
    assert _git(ana, "rev-parse", "main") != sha


def test_kapanis_dalsiz_is_klasorunde_durur(depo):
    ana, is_, _ = depo
    _git(is_, "switch", "-q", "--detach")
    sonuc = _kapanis(is_)
    assert sonuc.stdout == ""
    assert "kapanis: is klasoru bir dal uzerinde degil" in sonuc.stderr
    assert sonuc.returncode == 1
    assert is_.exists()
