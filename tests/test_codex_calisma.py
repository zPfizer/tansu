"""Codex yardımcı betiği (`kurulum/codex_calisma.py`): `yol` ve `denetle` komutları.

Betik, Codex ajanının yaptığı gibi `-I -X utf8` ile ayrı bir süreçte koşar.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

BETIK = Path(__file__).resolve().parents[1] / "kurulum" / "codex_calisma.py"
ORNEK_CIKTI = '{"round": 1, "verdict": "KALDI", "findings": [], "summary": "x"}'


def _calistir(*args):
    return subprocess.run(
        [sys.executable, "-I", "-X", "utf8", str(BETIK), *map(str, args)],
        capture_output=True,
        encoding="utf-8",
    )


def _surum(bin_klasoru, ad, zaman, *, host):
    klasor = bin_klasoru / ad
    klasor.mkdir(parents=True)
    dosyalar = ["codex.exe"] + (["codex-code-mode-host.exe"] if host else [])
    for dosya in dosyalar:
        (klasor / dosya).write_bytes(b"x")
    os.utime(klasor / "codex.exe", (zaman, zaman))
    return (klasor / "codex.exe").resolve().as_posix()


def test_yol_host_dosyasi_olmayan_yeni_klasoru_atlar(tmp_path):
    # Eski kural ("glob'un son öğesi") z-yeni klasörünü seçerdi: ad ve zaman olarak en yenisi.
    eski = _surum(tmp_path, "a-eski", 1_000_000_000, host=True)
    _surum(tmp_path, "z-yeni", 2_000_000_000, host=False)
    sonuc = _calistir("yol", tmp_path)
    assert sonuc.stdout.splitlines() == [eski]
    assert sonuc.returncode == 0


def test_yol_en_yeni_codex_exe_zamanini_secer(tmp_path):
    # Adı sonra gelen klasör (b) eskidir: ad sırası değil zaman kazanır.
    yeni = _surum(tmp_path, "a-yeni", 2_000_000_000, host=True)
    _surum(tmp_path, "b-eski", 1_000_000_000, host=True)
    sonuc = _calistir("yol", tmp_path)
    assert sonuc.stdout.splitlines() == [yeni]
    assert sonuc.returncode == 0


@pytest.mark.parametrize("hazirla", [False, True])
def test_yol_uygun_klasor_yoksa_durur(tmp_path, hazirla):
    if hazirla:
        _surum(tmp_path, "yalniz-codex", 1_000_000_000, host=False)
    sonuc = _calistir("yol", tmp_path)
    assert sonuc.stdout.splitlines() == ["codex: codex.exe yok"]
    assert sonuc.returncode == 1


def test_yol_klasor_yoksa_durur(tmp_path):
    sonuc = _calistir("yol", tmp_path / "yok")
    assert sonuc.stdout.splitlines() == ["codex: codex.exe yok"]
    assert sonuc.returncode == 1


def _dosyalar(tmp_path, cikti=ORNEK_CIKTI, gunluk="temiz\n"):
    cikti_yolu = tmp_path / "cikti.md"
    if cikti is not None:
        cikti_yolu.write_text(cikti, encoding="utf-8")
    gunluk_yolu = tmp_path / "log.txt"
    gunluk_yolu.write_text(gunluk, encoding="utf-8")
    return cikti_yolu, gunluk_yolu


def test_denetle_temiz_calisma_tamam(tmp_path):
    cikti, gunluk = _dosyalar(tmp_path)
    sonuc = _calistir("denetle", 0, cikti, gunluk, "--denetim")
    assert sonuc.stdout.splitlines() == ["codex: calisma tamam"]
    assert sonuc.returncode == 0


def test_denetle_17_10_ornegi_failed_to_spawn_calismadi(tmp_path):
    cikti, gunluk = _dosyalar(tmp_path, gunluk="ERROR failed to spawn code-mode host\n")
    sonuc = _calistir("denetle", 0, cikti, gunluk, "--denetim")
    assert sonuc.stdout.splitlines() == [
        "codex: denetim calismadi: log: failed to spawn"
    ]
    assert sonuc.returncode == 1


@pytest.mark.parametrize(
    ("kod", "cikti", "gunluk", "neden"),
    [
        (2, ORNEK_CIKTI, "temiz\n", "cikis kodu 2"),
        (0, "", "temiz\n", "cikti dosyasi yok ya da bos"),
        (0, None, "temiz\n", "cikti dosyasi yok ya da bos"),
        (0, "metin, JSON degil", "temiz\n", "cikti JSON degil ya da verdict yok"),
        (0, '{"round": 1}', "temiz\n", "cikti JSON degil ya da verdict yok"),
        (0, "[1, 2]", "temiz\n", "cikti JSON degil ya da verdict yok"),
        (0, "5", "temiz\n", "cikti JSON degil ya da verdict yok"),
        (0, ORNEK_CIKTI, "x os error 5 y\n", "log: os error"),
        (
            0,
            ORNEK_CIKTI,
            "CreateProcessWithLogonW failed: 1326\n",
            "log: CreateProcessWithLogonW",
        ),
        (
            0,
            ORNEK_CIKTI,
            "CreateProcessWithLogonW failed: 1909\n",
            "log: Codex sandbox account locked",
        ),
    ],
)
def test_denetle_calismadi_nedenleri(tmp_path, kod, cikti, gunluk, neden):
    cikti_yolu, gunluk_yolu = _dosyalar(tmp_path, cikti, gunluk)
    sonuc = _calistir("denetle", kod, cikti_yolu, gunluk_yolu, "--denetim")
    assert sonuc.stdout.splitlines() == ["codex: denetim calismadi: " + neden]
    assert sonuc.returncode == 1


def test_denetle_denetim_bayragi_yoksa_json_aranmaz(tmp_path):
    cikti, gunluk = _dosyalar(tmp_path, cikti="serbest metin")
    sonuc = _calistir("denetle", 0, cikti, gunluk)
    assert sonuc.stdout.splitlines() == ["codex: calisma tamam"]
    assert sonuc.returncode == 0


def test_denetle_nedenler_birlikte_yazilir(tmp_path):
    cikti, gunluk = _dosyalar(tmp_path, cikti="", gunluk="failed to spawn\n")
    sonuc = _calistir("denetle", 3, cikti, gunluk, "--denetim")
    assert sonuc.stdout.splitlines() == [
        "codex: denetim calismadi: cikis kodu 3; cikti dosyasi yok ya da bos; "
        "log: failed to spawn"
    ]
    assert sonuc.returncode == 1
