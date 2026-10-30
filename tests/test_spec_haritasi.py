"""AGENTS.md "Ortam ve teslim" içindeki `docs/SPEC.md` başlık satırları gerçek satırlarla aynı kalır.

SPEC yereldir (Ek B #12) ve yalnız `yeniden-kurulus` çalışma ağacında durur; test onu orada arar, yoksa atlanır (CI).
"""

import re
import subprocess
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
HARITA = re.compile(r"`((?:\d+|Appendix [A-C])\.)` (\d+)")


def _spec():
    if (KOK / "docs" / "SPEC.md").is_file():
        return KOK / "docs" / "SPEC.md"
    agaclar = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        cwd=KOK,
        capture_output=True,
        check=True,
        encoding="utf-8",
    ).stdout.split("\n\n")
    for agac in agaclar:
        if "branch refs/heads/yeniden-kurulus" in agac.splitlines():
            yol = (
                Path(agac.splitlines()[0].removeprefix("worktree "))
                / "docs"
                / "SPEC.md"
            )
            if yol.is_file():
                return yol
    return None


def test_agents_spec_haritasi_gercek_basliklari_gosterir():
    spec = _spec()
    if spec is None:
        pytest.skip("docs/SPEC.md yerel; bu makinede yok.")
    satirlar = spec.read_text(encoding="utf-8").splitlines()
    metin = (KOK / "AGENTS.md").read_text(encoding="utf-8")
    harita = [s for s in metin.splitlines() if "heading lines for Read" in s]
    assert len(harita) == 1
    eslesme = HARITA.findall(harita[0])
    assert len(eslesme) == 16
    yanlis = [
        (etiket, no)
        for etiket, no in eslesme
        if not satirlar[int(no) - 1].startswith(f"## {etiket}")
    ]
    assert yanlis == []


def test_agents_havuz_yolu_satiri_gercek_satiri_gosterir():
    spec = _spec()
    if spec is None:
        pytest.skip("docs/SPEC.md yerel; bu makinede yok.")
    no = re.search(
        r"`docs/SPEC\.md` line (\d+)", (KOK / "AGENTS.md").read_text(encoding="utf-8")
    )
    satir = spec.read_text(encoding="utf-8").splitlines()[int(no.group(1)) - 1]
    assert "Tansu X Veri Havuzu" in satir and "beyin-arama" in satir
