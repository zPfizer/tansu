"""Test kapısı (`kurulum/kapi.ps1`): kapı doğrulanmamış adıma güvenmez, hata yazar ve 1 ile durur."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]


def _kapi_calistir(
    tmp_path, python, beklenen=None, arg=("-Belge",), betik=None, npx=None
):
    pwsh = shutil.which("pwsh") or shutil.which("powershell")
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
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(betik or KOK / "kurulum" / "kapi.ps1"),
            *arg,
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
    klasor.mkdir(exist_ok=True)
    if os.name == "nt":
        yol = klasor / "npx.cmd"
        yol.write_text(f"@echo npx %*\n@exit /b {kod}\n", encoding="utf-8")
    else:
        yol = klasor / "npx"
        yol.write_text(f'#!/bin/sh\necho npx "$@"\nexit {kod}\n', encoding="utf-8")
        yol.chmod(0o755)
    return yol


def _gecici_depo(tmp_path):
    # Git sınırını taklit et: kapı testi gerçek bir depoyu değiştirmez.
    depo = tmp_path / "depo"
    (depo / "kurulum").mkdir(parents=True)
    betik = depo / "kurulum" / "kapi.ps1"
    shutil.copy(KOK / "kurulum" / "kapi.ps1", betik)
    klasor = tmp_path / "bin"
    klasor.mkdir(exist_ok=True)
    sha = "0123456789abcdef0123456789abcdef01234567"
    if os.name == "nt":
        (klasor / "git.cmd").write_text(
            f'@if "%1"=="rev-parse" echo {sha}\n@exit /b 0\n', encoding="utf-8"
        )
    else:
        git = klasor / "git"
        git.write_text(
            f'#!/bin/sh\nif [ "$1" = rev-parse ]; then echo {sha}; fi\nexit 0\n',
            encoding="utf-8",
        )
        git.chmod(0o755)
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


@pytest.mark.parametrize(
    ("metin", "eslesir"),
    [
        ("@alifurkangokce/driftlint@0.19.0", True),
        ("@alifurkangokce/driftlint@0.19.1", False),
        ("@alifurkangokce/driftlint", False),
        ("@alifurkangokce/driftlint@0.19.0-extra", False),
        ("@alifurkangokce/driftlint@0.19.01", False),
        ("@alifurkangokce/driftlint@0.19.0.1", False),
        ("@alifurkangokce/driftlint@0x19x0", False),
    ],
)
def test_kapi_ve_ci_ayni_driftlint_surumunu_kullanir(metin, eslesir):
    desen = r"@alifurkangokce/driftlint@0\.19\.0(?![\w.+-])"
    assert bool(re.search(desen, metin)) is eslesir
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


def test_kapi_test_secilmezse_durur(tmp_path):
    # Tam koşu yalnız CI'da (Levent 17.10): kapı test dosyası olmadan koşmaz.
    sonuc = _kapi_calistir(tmp_path, Path(sys.executable).resolve(), arg=())
    assert sonuc.returncode == 1
    assert "kapi: test secilmedi" in sonuc.stdout
    assert "kapi: pytest" not in sonuc.stdout


@pytest.mark.parametrize("metin", ["bozuk", ""])
def test_kapi_gecersiz_sayida_durur(tmp_path, metin):
    sonuc = _kapi_calistir(tmp_path, _sahte_yorumlayici(tmp_path, metin))
    assert sonuc.returncode == 1
    assert "gecersiz sayi" in sonuc.stdout
    assert "kapi: pytest" not in sonuc.stdout
