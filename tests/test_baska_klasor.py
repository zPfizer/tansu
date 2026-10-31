"""Belgelenen komutlar başka klasörden de aynı çalışır: Levent projeleri beyin klasöründen yönetir (31.10.2026).

Komut proje dosyalarını kendi kökünden okur ve çalışılan klasöre dosya yazmaz. Yalnız `sina --help` satırı kurulu
(editable) kopyayı yükler: kurulum eski projeyi gösterirse `sina` komutu yoktur. Öteki `-m tansu` satırı bu
kopyayı `PYTHONPATH` ile yükler.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from kurulum import pr_iddia_kontrol

KOK = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("arglar", "ek_ortam", "kod", "beklenen"),
    [
        pytest.param(
            ["-m", "tansu", "sina", "--help"],
            {},
            0,
            "tansu sina",
            marks=pytest.mark.slow,
        ),
        (
            ["-m", "tansu", "sina", "gartley"],
            {"PYTHONPATH": str(KOK)},
            1,
            "anlık görüntü yok",
        ),
        pytest.param(
            ["-m", "pytest", f"{KOK}/tests/test_durum.py", "-q"],
            {},
            0,
            "passed",
            marks=pytest.mark.slow,
        ),
        (
            ["-m", "ruff", "check", "--no-cache", f"{KOK}/tansu"],
            {},
            0,
            "All checks passed",
        ),
        (
            ["-m", "ruff", "format", "--check", "--no-cache", f"{KOK}/tansu"],
            {},
            0,
            "formatted",
        ),
        ([f"{KOK}/kurulum/pr_iddia_kontrol.py", "--help"], {}, 0, "--repo"),
        ([f"{KOK}/kurulum/birlestir.py", "--help"], {}, 0, "--repo"),
    ],
)
def test_komut_baska_klasorden_calisir_ve_oraya_yazmaz(
    tmp_path, arglar, ek_ortam, kod, beklenen
):
    sonuc = subprocess.run(
        [sys.executable, "-X", "utf8", *arglar],
        cwd=tmp_path,
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, **ek_ortam},
    )
    cikti = sonuc.stdout + sonuc.stderr
    assert (sonuc.returncode, beklenen in cikti) == (kod, True), cikti
    assert "Traceback" not in cikti
    assert not list(tmp_path.iterdir())


def test_pr_iddia_kontrol_depoyu_klasorden_cikarmaz(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["pr_iddia_kontrol.py", "1"])
    cagrilar = []

    def gh(*arglar):
        cagrilar.append(arglar)
        raise subprocess.CalledProcessError(1, "gh")

    monkeypatch.setattr(pr_iddia_kontrol, "_gh", gh)
    with pytest.raises(subprocess.CalledProcessError):
        pr_iddia_kontrol.main()
    assert cagrilar[0][-2:] == ("--repo", "zPfizer/tansu")
