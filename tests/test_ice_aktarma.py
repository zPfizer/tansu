from pathlib import Path

import tansu


def test_tansu_testi_kosan_kopyadan_gelir():
    """Ana `.venv`'deki düzenlenebilir kurulum ana kopyayı gösterir; `tansu` oradan gelirse testler bu kopyanın değil
    eski projenin kodunu sınar (retro 31.10.2026). `pyproject.toml` `pythonpath = ["."]` bu kopyayı öne koyar."""
    kok = Path(__file__).resolve().parents[1]
    assert Path(tansu.__file__).resolve().is_relative_to(kok), tansu.__file__
