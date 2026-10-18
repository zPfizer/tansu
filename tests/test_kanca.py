"""Kanca kararları JSON girdisi ve gerçek geçici Git depolarıyla sınanır."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BETIK = Path(__file__).resolve().parents[1] / "kurulum" / "kanca.py"
MESAJ = 'Write a red test under tests/ first, then edit the code (docs/agents/kod-kurallari.md "Test first").\n'


@pytest.fixture(autouse=True)
def git_ortami(monkeypatch, tmp_path):
    for ad in os.environ:
        if ad.startswith("GIT_"):
            monkeypatch.delenv(ad)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_ATTR_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))
    (tmp_path / "iz.jsonl").write_text("", encoding="utf-8")


def _git(depo, *arg):
    return subprocess.run(
        [
            "git",
            "-c",
            "user.name=Tansu test",
            "-c",
            "user.email=test@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.autocrlf=false",
            "-c",
            f"core.attributesFile={os.devnull}",
            "-c",
            f"core.excludesFile={os.devnull}",
            *arg,
        ],
        cwd=depo,
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout.strip()


@pytest.fixture
def depo(tmp_path):
    dizin = tmp_path / "depo"
    dizin.mkdir()
    _git(dizin, "init", "-b", "master", "--template=")
    for dosya in ("tansu/a.py", "tests/test_a.py"):
        yol = dizin / dosya
        yol.parent.mkdir()
        yol.write_text("# İlk sürüm\n", encoding="utf-8")
    _git(dizin, "add", "tansu/a.py", "tests/test_a.py")
    _git(dizin, "commit", "-m", "taban")
    _git(dizin, "update-ref", "refs/remotes/origin/master", "HEAD")
    return dizin


def _kos(girdi, cwd, env=None):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(BETIK)],
        input=json.dumps(girdi),
        capture_output=True,
        encoding="utf-8",
        cwd=cwd,
        env=env,
    )


def _duzenle(depo, dosya="tansu/a.py", arac="Edit", env=None):
    return _kos(
        {
            "hook_event_name": "PreToolUse",
            "tool_name": arac,
            "tool_input": {"file_path": str(depo / dosya)},
            "transcript_path": str(depo.parent / "iz.jsonl"),
        },
        depo,
        env,
    )


@pytest.mark.parametrize("arac", ["Edit", "Write", "MultiEdit"])
@pytest.mark.parametrize("dosya", ["tansu/a.py", "kurulum/yeni/a.py", ".github/a.py"])
def test_kod_duzenleme_test_degisikligi_ister(depo, arac, dosya):
    sonuc = _duzenle(depo, dosya, arac)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (2, "", MESAJ)


@pytest.mark.parametrize("durum", ["yeni", "degisen", "staged", "commit"])
def test_test_degisikligi_kodu_acar(depo, durum):
    dosya = "tests/yeni.py" if durum == "yeni" else "tests/test_a.py"
    (depo / dosya).write_text("# Yeni test\n", encoding="utf-8")
    if durum in {"staged", "commit"}:
        _git(depo, "add", dosya)
    if durum == "commit":
        _git(depo, "commit", "-m", "test")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_baska_klasordeki_test_sayilmaz(depo):
    (depo / "test_a.py").write_text("# Test\n", encoding="utf-8")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (2, "", MESAJ)


@pytest.mark.parametrize(
    "dosya",
    [
        "tests/test_a.py",
        "AGENTS.md",
        ".scratch/x.py",
        "betik.py",
        "tansu/a.md",
        "tansu/a.ps1",
    ],
)
@pytest.mark.parametrize("git_var", [True, False])
def test_kapsam_disindaki_dosyalar_gecer(depo, dosya, git_var):
    ortam = None if git_var else {**os.environ, "PATH": ""}
    sonuc = _duzenle(depo, dosya, env=ortam)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_depo_disindaki_klasor_gecer(tmp_path):
    disari = tmp_path / "disari"
    disari.mkdir()
    sonuc = _duzenle(disari)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_git_baslatilamazsa_gecer(depo):
    sonuc = _duzenle(depo, env={**os.environ, "PATH": ""})
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


@pytest.mark.parametrize("test_degisti", [False, True])
def test_origin_master_yoksa_yalniz_calisma_agaci_sayilir(depo, test_degisti):
    _git(depo, "update-ref", "-d", "refs/remotes/origin/master")
    if test_degisti:
        (depo / "tests/test_a.py").write_text("# Yeni\n", encoding="utf-8")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (
        (0, "", "") if test_degisti else (2, "", MESAJ)
    )


def test_origin_master_bozuksa_engellemez(depo):
    (depo / ".git/refs/remotes/origin/master").write_text("bozuk\n", encoding="utf-8")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


@pytest.mark.parametrize("arac", ["Bash", "PowerShell", "Read"])
def test_baska_araclar_sessizce_gecer(tmp_path, arac):
    sonuc = _kos({"hook_event_name": "PreToolUse", "tool_name": arac}, tmp_path)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


@pytest.mark.parametrize("olay", ["SubagentStop", "Notification", "Bilinmeyen"])
def test_baska_olaylar_sessizce_gecer(tmp_path, olay):
    sonuc = _kos({"hook_event_name": olay}, tmp_path)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_gecersiz_json_engellemez(tmp_path):
    sonuc = subprocess.run(
        [sys.executable, "-X", "utf8", str(BETIK)],
        input="json degil",
        capture_output=True,
        encoding="utf-8",
        cwd=tmp_path,
    )
    assert sonuc.returncode == 1
    assert "JSONDecodeError" in sonuc.stderr
