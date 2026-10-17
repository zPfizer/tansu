"""README yenilikleri en üst değişiklik bölümüyle aynı kalır."""

import re
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]


def _yenilikleri_dogrula(readme, changelog):
    bolumler = re.split(r"^## ", changelog, flags=re.MULTILINE)
    assert len(bolumler) > 1, "CHANGELOG sürüm bölümü eksik"
    baslik, _, govde = bolumler[1].partition("\n")
    assert re.fullmatch(
        r"\[(?:Yayımlanmamış|(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))\]"
        r"(?: — [0-9]{4}-[0-9]{2}-[0-9]{2})?",
        baslik,
    ), "CHANGELOG en üst bölüm başlığı geçersiz"
    yeni = re.search(
        r"^## Yeni olanlar\n(.*?)(?=^## |\Z)", readme, re.MULTILINE | re.DOTALL
    )
    assert yeni is not None, "README Yeni olanlar bölümü eksik"
    satirlar = [
        satir
        for satir in yeni[1].splitlines()
        if satir.strip()
        and not satir.startswith("Son sürüm: ")
        and not re.fullmatch(r"\[[^\]\n]+\]\(CHANGELOG\.md\)", satir)
    ]
    assert satirlar, "README Yeni olanlar bölümü boş"
    for satir in satirlar:
        assert satir in govde.splitlines(), f"CHANGELOG en üst bölümünde yok: {satir}"


def test_readme_yenilikleri_en_ust_changelog_bolumunden():
    _yenilikleri_dogrula(
        (KOK / "README.md").read_text(encoding="utf-8"),
        (KOK / "CHANGELOG.md").read_text(encoding="utf-8"),
    )


@pytest.mark.parametrize(
    ("readme", "changelog", "gecerli"),
    [
        ("## Yeni olanlar\n- Yeni.\n", "## [Yayımlanmamış]\n- Yeni.\n", True),
        (
            "## Yeni olanlar\nSon sürüm: v0.2.0\n[Değişiklikler](CHANGELOG.md)\n- Yeni.\n",
            "## [0.2.0] — 2026-10-18\n### Eklendi\n- Yeni.\n",
            True,
        ),
        ("## Yeni olanlar\n- Yeni\n", "## [Yayımlanmamış]\n- Yeni.\n", False),
        ("## Yeni olanlar\n- Yeni. \n", "## [Yayımlanmamış]\n- Yeni.\n", False),
        (
            "## Yeni olanlar\n- Eski.\n",
            "## [Yayımlanmamış]\n- Yeni.\n## [0.1.0]\n- Eski.\n",
            False,
        ),
        ("## Başka\n- Yeni.\n", "## [Yayımlanmamış]\n- Yeni.\n", False),
        ("## Yeni olanlar\n", "## [Yayımlanmamış]\n- Yeni.\n", False),
        ("## Yeni olanlar\n- Yeni.\n", "- Yeni.\n", False),
        ("## Yeni olanlar\n- Yeni.\n", "## [0.1]\n- Yeni.\n", False),
        ("## Yeni olanlar\n- Yeni.\n", "## [01.1.0]\n- Yeni.\n", False),
        ("## Yeni olanlar\n- Yeni.\n", "## [Yayımlanmamış]x\n- Yeni.\n", False),
        (
            "## Yeni olanlar\n[Değişiklikler](CHANGELOG.md) değişti\n",
            "## [Yayımlanmamış]\n- Yeni.\n",
            False,
        ),
    ],
)
def test_yenilik_eslesmesi_tam_satir_ve_en_ust_bolum_ister(readme, changelog, gecerli):
    if gecerli:
        _yenilikleri_dogrula(readme, changelog)
    else:
        with pytest.raises(AssertionError):
            _yenilikleri_dogrula(readme, changelog)
