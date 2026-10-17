"""Test kapısı (`kurulum/kapi.ps1`): kapı doğrulanmamış adıma güvenmez, hata yazar ve 1 ile durur."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]


def _kapi_calistir(tmp_path, python, beklenen=None, betik=None, npx=None):
    pwsh = shutil.which("pwsh")
    assert pwsh is not None
    env = dict(
        os.environ,
        USERPROFILE=str(tmp_path),
        HOME=str(tmp_path),
        TANSU_PY=str(python),
    )
    env.pop("TANSU_BEKLENEN_ACIK", None)
    if beklenen is not None:
        env["TANSU_BEKLENEN_ACIK"] = beklenen
    if npx is not None:
        # Sahte npx klasörü PATH başına girer: gerçek npx'e ağ için çıkılmaz.
        env["PATH"] = str(npx.parent) + os.pathsep + env["PATH"]
    # -Belge: düzeltme öncesi betik kapıyı sürdürse bile bu dosyayı yeniden koşmaz (özyineleme olmaz).
    return subprocess.run(
        [
            pwsh,
            "-NoProfile",
            "-File",
            str(betik or KOK / "kurulum" / "kapi.ps1"),
            "-Belge",
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )


def _sahte_yorumlayici(tmp_path, metin):
    # Sahte yorumlayıcı sabit bir metin yazar ve 0 ile çıkar.
    if os.name == "nt":
        yol = tmp_path / "sahte.cmd"
        yol.write_text(
            f"@echo {metin}\n" if metin else "@exit /b 0\n", encoding="utf-8"
        )
    else:
        yol = tmp_path / "sahte.sh"
        yol.write_text(
            f"#!/bin/sh\necho {metin}\n" if metin else "#!/bin/sh\nexit 0\n",
            encoding="utf-8",
        )
        yol.chmod(0o755)
    return yol


def _sahte_npx(tmp_path, kod):
    # Sahte npx argümanlarını yazar ve verilen kodla çıkar.
    klasor = tmp_path / "bin"
    klasor.mkdir()
    if os.name == "nt":
        yol = klasor / "npx.cmd"
        yol.write_text(f"@echo npx %*\n@exit /b {kod}\n", encoding="utf-8")
    else:
        yol = klasor / "npx"
        yol.write_text(f'#!/bin/sh\necho npx "$@"\nexit {kod}\n', encoding="utf-8")
        yol.chmod(0o755)
    return yol


def _gecici_depo(tmp_path):
    # Kapı kendi deponun kökünde çalışır: git'li bir kopya, kaynak/master = HEAD (fark yok).
    depo = tmp_path / "depo"
    (depo / "kurulum").mkdir(parents=True)
    betik = depo / "kurulum" / "kapi.ps1"
    shutil.copy(KOK / "kurulum" / "kapi.ps1", betik)
    for arg in (
        ("init", "-q"),
        ("add", "kurulum/kapi.ps1"),
        ("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "x"),
        ("update-ref", "refs/remotes/kaynak/master", "HEAD"),
    ):
        subprocess.run(["git", "-C", str(depo), *arg], check=True, capture_output=True)
    return betik


@pytest.mark.parametrize("kod", [0, 1])
def test_kapi_driftlint_kodu_yazilir_ve_hata_kapiyi_durdurur(tmp_path, kod):
    sonuc = _kapi_calistir(
        tmp_path,
        _sahte_yorumlayici(tmp_path, "0"),
        betik=_gecici_depo(tmp_path),
        npx=_sahte_npx(tmp_path, kod),
    )
    satirlar = sonuc.stdout.splitlines()
    assert "npx --yes @alifurkangokce/driftlint@0.19.0 ." in satirlar
    assert satirlar.index(f"kapi: driftlint -> {kod}") == (
        satirlar.index("kapi: git diff --check -> 0") + 1
    )
    assert sonuc.returncode == kod


def test_kapi_ve_ci_ayni_driftlint_surumunu_kullanir():
    desen = r"@alifurkangokce/driftlint@\d+\.\d+\.\d+"
    kapi = re.findall(desen, (KOK / "kurulum" / "kapi.ps1").read_text(encoding="utf-8"))
    ci = re.findall(
        desen, (KOK / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    )
    assert len(ci) == 1
    assert kapi == ci


@pytest.mark.parametrize("beklenen", [None, "5"])
def test_kapi_havuz_yoksa_durur(tmp_path, beklenen):
    sonuc = _kapi_calistir(tmp_path, Path(sys.executable).resolve(), beklenen)
    assert sonuc.returncode == 1
    assert "kapi: acik havuz notu = HATA" in sonuc.stdout
    assert "acik-sayi: havuz klasoru yok:" in sonuc.stderr
    assert "kapi: pytest" not in sonuc.stdout


def test_kapi_python_yoksa_durur(tmp_path):
    sonuc = _kapi_calistir(tmp_path, tmp_path / "yok" / "python.exe")
    assert sonuc.returncode == 1
    assert "kapi: python yok:" in sonuc.stdout
    assert "kapi: pytest" not in sonuc.stdout


@pytest.mark.parametrize("metin", ["bozuk", ""])
def test_kapi_gecersiz_sayida_durur(tmp_path, metin):
    sonuc = _kapi_calistir(tmp_path, _sahte_yorumlayici(tmp_path, metin))
    assert sonuc.returncode == 1
    assert "gecersiz sayi" in sonuc.stdout
    assert "kapi: pytest" not in sonuc.stdout
