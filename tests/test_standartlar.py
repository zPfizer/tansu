from pathlib import Path

import pytest


def _satirlar(yol):
    return yol.read_text(encoding="utf-8").splitlines()


def test_kodlama_standartlari_ayni():
    kaynak = Path.home() / ".claude" / "CODING_STANDARDS.md"
    if not kaynak.exists():
        pytest.skip("Evde kodlama standartları dosyası yok.")
    kopya = Path(__file__).resolve().parents[1] / "CODING_STANDARDS.md"
    assert _satirlar(kopya) == _satirlar(kaynak)


def test_bitis_olcutleri_ayni():
    kaynak = Path.home() / ".claude" / "DEFINITION_OF_DONE.md"
    if not kaynak.exists():
        pytest.skip("Evde Definition of Done dosyası yok.")
    kopya = Path(__file__).resolve().parents[1] / "DEFINITION_OF_DONE.md"
    assert _satirlar(kopya) == _satirlar(kaynak)
