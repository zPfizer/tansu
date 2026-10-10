from pathlib import Path

import pytest


def _satirlar(yol):
    return yol.read_text(encoding="utf-8").splitlines()


def _genel_standart_basta(ad):
    kaynak = Path.home() / ".claude" / ad
    if not kaynak.exists():
        pytest.skip(f"Evde {ad} yok.")
    genel = _satirlar(kaynak)
    kopya = _satirlar(Path(__file__).resolve().parents[1] / ad)
    assert kopya[: len(genel)] == genel
    ek = kopya[len(genel) :]
    assert ek == [] or (ek[0] == "" and ek[1] == "## Tansu")


def test_kodlama_standartlari_genel_standartla_baslar():
    _genel_standart_basta("CODING_STANDARDS.md")


def test_bitis_olcutleri_genel_standartla_baslar():
    _genel_standart_basta("DEFINITION_OF_DONE.md")
