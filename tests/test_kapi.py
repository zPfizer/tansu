"""Test kapısı (`kurulum/kapi.ps1`): havuz klasörü yoksa kapı hata yazar ve 1 ile durur."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("beklenen", [None, "5"])
def test_kapi_havuz_yoksa_durur(tmp_path, beklenen):
    pwsh = shutil.which("pwsh")
    assert pwsh is not None
    env = dict(os.environ, USERPROFILE=str(tmp_path), HOME=str(tmp_path))
    env.pop("TANSU_BEKLENEN_ACIK", None)
    if beklenen is not None:
        env["TANSU_BEKLENEN_ACIK"] = beklenen
    # -Belge: düzeltme öncesi betik kapıyı sürdürse bile bu dosyayı yeniden koşmaz (özyineleme olmaz).
    sonuc = subprocess.run(
        [pwsh, "-NoProfile", "-File", str(KOK / "kurulum" / "kapi.ps1"), "-Belge"],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    assert sonuc.returncode == 1
    assert "kapi: acik havuz notu = HATA" in sonuc.stdout
    assert "kapi: pytest" not in sonuc.stdout
