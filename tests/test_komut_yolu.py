"""AGENTS.md ve README.md proje araçlarını `.venv` yorumlayıcısıyla verir, çıplak `python`, `ruff` ya da `pytest` ile vermez.

Çıplak komut genel Python'u bulur: proje paketleri yoktur (`No module named 'pandas'`) ya da komut bulunmaz (31.10.2026).
`python -m venv` serbesttir, çünkü ortamı genel Python kurar.
"""

import re
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
CIPLAK = re.compile(
    r"(?:^|`)(?!python -m venv )(python3?|py|pip3?|ruff|pytest|pre-commit|uv)\s", re.M
)


def bulgular(metin):
    return [
        f"{metin.count(chr(10), 0, m.start()) + 1}: {m.group(1)}"
        for m in CIPLAK.finditer(metin)
    ]


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        ("`python -X utf8 -m tansu sina`", ["1: python"]),
        ("a\n`ruff check tansu`", ["2: ruff"]),
        ("pre-commit run\n", ["1: pre-commit"]),
        ("`../../../.venv/Scripts/python.exe -X utf8 -m pytest -q`", []),
        ("python -m venv .venv\n`-m ruff`, `py`", []),
    ],
)
def test_desen(metin, beklenen):
    assert bulgular(metin) == beklenen


@pytest.mark.parametrize("ad", ["AGENTS.md", "README.md"])
def test_belge_ciplak_arac_komutu_vermez(ad):
    bulgu = bulgular((KOK / ad).read_text(encoding="utf-8"))
    assert not bulgu, (
        f'{ad}: çıplak araç komutu; `<py> -X utf8 -m <araç>` yazın (AGENTS.md "Commands"): {bulgu}'
    )
