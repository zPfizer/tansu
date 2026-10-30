import fnmatch
import json
from pathlib import Path

import pytest

from kurulum.birlestir import engeller, yontem

SHA = "0436c58" + "a" * 33
DENETIMLER = [
    {"name": ad, "status": "COMPLETED", "conclusion": "SUCCESS"}
    for ad in ("testler", "acik-depo", "pr-iddia")
]
PR = {
    "state": "OPEN",
    "baseRefName": "yeniden-kurulus",
    "headRefOid": SHA,
    "statusCheckRollup": DENETIMLER,
    "comments": [{"body": f"İncelenen commit: {SHA}\nSonuç: NOTLU GEÇTİ"}],
}
AYAR = Path(__file__).resolve().parents[1] / ".claude" / "settings.json"


@pytest.mark.parametrize(
    ("main_basta", "main_tabanda", "beklenen"),
    [
        (True, False, "--merge"),  # main'i getiren PR (PR 277, PR 278)
        (False, False, "--squash"),
        (True, True, "--squash"),  # eşitlemeden sonra açılan iş dalı (PR 273)
        (False, True, "--squash"),
    ],
)
def test_yontem_yalniz_main_getiren_pra_merge_verir(main_basta, main_tabanda, beklenen):
    assert yontem(main_basta, main_tabanda) == beklenen


def test_kural_saglaninca_engel_yok():
    assert engeller(PR) == []


@pytest.mark.parametrize(
    ("degisiklik", "engel"),
    [
        ({"baseRefName": "main"}, "taban main"),
        ({"state": "MERGED"}, "PR durumu MERGED"),
        ({"statusCheckRollup": []}, "denetim yok"),
        (
            {
                "statusCheckRollup": [
                    *DENETIMLER[:2],
                    {**DENETIMLER[2], "conclusion": "FAILURE"},
                ]
            },
            "denetim pr-iddia: FAILURE",
        ),
        (
            {
                "statusCheckRollup": [
                    {"name": "testler", "status": "IN_PROGRESS", "conclusion": ""}
                ]
            },
            "denetim testler: IN_PROGRESS",
        ),
        ({"comments": []}, "inceleme yorumu yok"),
        (
            {"comments": [{"body": f"İncelenen commit: {SHA}\nSonuç: GEÇMEDİ"}]},
            "inceleme yorumu yok",
        ),
        (
            {"comments": [{"body": "İncelenen commit: 366c578\nSonuç: GEÇTİ"}]},
            "inceleme yorumu yok",
        ),
    ],
)
def test_kural_bozulunca_birlestirmez(degisiklik, engel):
    assert any(engel in e for e in engeller({**PR, **degisiklik}))


@pytest.mark.parametrize("arac", ["Bash", "PowerShell"])
@pytest.mark.parametrize(
    "komut",
    [
        "gh pr merge 273 --merge",
        "gh pr merge 278 --squash --match-head-commit abc",
        "cd x && gh pr merge 1",
        "gh api -X PUT repos/zPfizer/tansu/pulls/273/merge",
    ],
)
def test_ciplak_birlestirme_komutu_yasak(arac, komut):
    """Yöntemi `kurulum/birlestir.py` seçer; PR 273 çıplak komutla merge commit'iyle birleşmişti (retro 31.10)."""
    yasak = json.loads(AYAR.read_text(encoding="utf-8"))["permissions"]["deny"]
    desenler = [d[len(arac) + 1 : -1] for d in yasak if d.startswith(f"{arac}(")]
    assert any(fnmatch.fnmatchcase(komut, d) for d in desenler)
    assert not any(
        fnmatch.fnmatchcase("python -X utf8 kurulum/birlestir.py 278", d)
        for d in desenler
    )
