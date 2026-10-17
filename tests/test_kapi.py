"""Test kapısı (`kurulum/kapi.ps1`): kapı doğrulanmamış adıma güvenmez, hata yazar ve 1 ile durur."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]


def _kapi_calistir(tmp_path, python, beklenen=None):
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
    # -Belge: düzeltme öncesi betik kapıyı sürdürse bile bu dosyayı yeniden koşmaz (özyineleme olmaz).
    return subprocess.run(
        [pwsh, "-NoProfile", "-File", str(KOK / "kurulum" / "kapi.ps1"), "-Belge"],
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
