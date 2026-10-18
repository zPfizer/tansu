"""README yenilikleri en üst değişiklik bölümüyle aynı kalır."""

import os
import re
import subprocess
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


def test_changelog_ayni_yere_eklenen_iki_satiri_korur(tmp_path):
    """Issue #102: Gerçek Git birleştirmesi iki dalın satırlarını korur."""
    ortam = {ad: deger for ad, deger in os.environ.items() if not ad.startswith("GIT_")}
    ortam.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_ATTR_NOSYSTEM="1",
    )

    def git(*komut):
        sonuc = subprocess.run(
            [
                "git",
                "-c",
                "user.name=Tansu test",
                "-c",
                "user.email=test@example.invalid",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "core.autocrlf=false",
                "-c",
                f"core.attributesFile={os.devnull}",
                "-c",
                f"core.excludesFile={os.devnull}",
                *komut,
            ],
            cwd=tmp_path,
            env=ortam,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert sonuc.returncode == 0, sonuc.stdout + sonuc.stderr
        return sonuc.stdout

    git("init", "--initial-branch=ana", "--template=")
    kaynak = Path(__file__).resolve().parents[1] / ".gitattributes"
    (tmp_path / ".gitattributes").write_text(
        kaynak.read_text(encoding="utf-8"), encoding="utf-8"
    )
    gunluk = tmp_path / "CHANGELOG.md"
    taban = "# Değişiklik günlüğü\n\n### Eklendi\n\n- Önceki kayıt.\n"
    gunluk.write_text(taban, encoding="utf-8")
    git("add", ".gitattributes", "CHANGELOG.md")
    git("commit", "-m", "taban")
    git("branch", "yan")
    gunluk.write_text(
        taban.replace("- Önceki kayıt.", "- Birinci iş.\n- Önceki kayıt."),
        encoding="utf-8",
    )
    git("add", "CHANGELOG.md")
    git("commit", "-m", "birinci")
    git("switch", "yan")
    gunluk.write_text(
        taban.replace("- Önceki kayıt.", "- İkinci iş.\n- Önceki kayıt."),
        encoding="utf-8",
    )
    git("add", "CHANGELOG.md")
    git("commit", "-m", "ikinci")

    git("merge", "--no-edit", "ana")

    assert git("ls-files", "--unmerged") == ""
    assert sorted(gunluk.read_text(encoding="utf-8").splitlines()) == sorted(
        [
            "# Değişiklik günlüğü",
            "",
            "### Eklendi",
            "",
            "- Birinci iş.",
            "- İkinci iş.",
            "- Önceki kayıt.",
        ]
    )
