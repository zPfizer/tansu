"""Gerçek Git birleştirmesi değişiklik günlüğünün iki ek satırını korur."""

import os
import subprocess
from pathlib import Path


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
