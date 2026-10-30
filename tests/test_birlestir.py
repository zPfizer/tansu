import fnmatch
import json
from pathlib import Path

import pytest

from kurulum import birlestir
from kurulum.birlestir import engeller, main_getiriyor

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
GITHUB = {  # gh api yanıtları, 31.10.2026: baş...main ortak atası, taban...ortak durumu
    "compare/0a89983...main": "da7aed5",
    "compare/084b9aa...da7aed5": "diverged",
    "compare/0436c58...main": "b2e89db",
    "compare/366c578...b2e89db": "diverged",
    "compare/18e907c...main": "3778a1c",
    "compare/c403eb0...3778a1c": "behind",
    "compare/c834575...main": "da7aed5",
    "compare/366c578...da7aed5": "behind",
}


@pytest.mark.parametrize(
    ("bas", "taban", "getiriyor"),
    [
        ("0a89983", "084b9aa", True),  # PR 277: dal açıldıktan sonra main ilerledi
        ("0436c58", "366c578", True),  # PR 278
        (
            "18e907c",
            "c403eb0",
            False,
        ),  # PR 273: iş dalı, merge commit'iyle yanlış birleşti
        ("c834575", "366c578", False),  # PR 280: sıradan iş dalı
    ],
)
def test_yalniz_main_getiren_pr_merge_ile_birlesir(monkeypatch, bas, taban, getiriyor):
    monkeypatch.setattr(
        birlestir, "_gh", lambda *a: GITHUB[a[1].split("/", 3)[3]] + "\n"
    )
    assert main_getiriyor("zPfizer/tansu", bas, taban) is getiriyor


def test_kural_saglaninca_engel_yok():
    assert engeller(PR) == []


def test_yeniden_kosan_denetimin_yalniz_sonuncusu_sayilir():
    """PR 279 inceleme turu 2: gövde düzelince `pr-iddia` yeniden koştu; eski FAILURE engel değildir."""
    eski, yeni = (
        {**DENETIMLER[2], "workflowName": "denetim", "conclusion": c, "startedAt": t}
        for c, t in (
            ("FAILURE", "2026-10-30T22:56:13Z"),
            ("SUCCESS", "2026-10-30T22:56:36Z"),
        )
    )
    assert engeller({**PR, "statusCheckRollup": [*DENETIMLER[:2], yeni, eski]}) == []
    tersi = [{**eski, "conclusion": "SUCCESS"}, {**yeni, "conclusion": "FAILURE"}]
    assert engeller({**PR, "statusCheckRollup": [*DENETIMLER[:2], *tersi]}) == [
        "denetim pr-iddia: FAILURE"
    ]


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
            "son inceleme kararı GEÇMEDİ",
        ),
        (  # PR 279 inceleme turu 1: olumsuz yorumdaki "GEÇTİ" sözcükleri onay sayılmaz
            {"comments": [{"body": f"{SHA} için GEÇTİ kararı VERİLMEDİ"}]},
            "inceleme yorumu yok",
        ),
        (
            {
                "comments": [
                    {"body": f"İncelenen commit: {SHA}\nSonuç: GEÇMEDİ\n- pytest GEÇTİ"}
                ]
            },
            "son inceleme kararı GEÇMEDİ",
        ),
        (
            {
                "comments": [
                    *PR["comments"],
                    {"body": f"İncelenen commit: {SHA}\nSonuç: GEÇMEDİ (tur 2)"},
                ]
            },
            "son inceleme kararı GEÇMEDİ",
        ),
        (
            {"comments": [{"body": "İncelenen commit: 366c578\nSonuç: GEÇTİ"}]},
            "inceleme yorumu yok",
        ),
        (  # PR 279 inceleme turu 2: karar yalnız baş SHA bloğundan okunur
            {
                "comments": [
                    {
                        "body": "İncelenen commit: 366c578\nSonuç: GEÇTİ\n\n"
                        f"İncelenen commit: {SHA}\nSonuç: GEÇMEDİ"
                    }
                ]
            },
            "son inceleme kararı GEÇMEDİ",
        ),
        (
            {
                "comments": [
                    {
                        "body": f"Tur 1:\nSonuç: GEÇTİ\n\nİncelenen commit: {SHA}\nSonuç: GEÇMEDİ"
                    }
                ]
            },
            "son inceleme kararı GEÇMEDİ",
        ),
        (
            {
                "comments": [
                    *PR["comments"],
                    {"body": f"İncelenen commit: {SHA}\n**Sonuç:** GEÇMEDİ"},
                ]
            },
            "son inceleme kararı okunamadı",
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
        "gh pr -R zPfizer/tansu merge 279",
        "gh pr --repo zPfizer/tansu merge",
        "gh api graphql -f query='mutation{mergePullRequest(input:{}){clientMutationId}}'",
        "gh -R zPfizer/tansu pr merge 279",
        "gh.exe pr merge 279",
        "gh  pr merge 279",
    ],
)
def test_ciplak_birlestirme_komutu_yasak(arac, komut):
    """Yöntemi `kurulum/birlestir.py` seçer; PR 273 çıplak komutla merge commit'iyle birleşmişti (retro 31.10)."""
    yasak = json.loads(AYAR.read_text(encoding="utf-8"))["permissions"]["deny"]
    desenler = [d[len(arac) + 1 : -1] for d in yasak if d.startswith(f"{arac}(")]
    assert any(fnmatch.fnmatchcase(komut, d) for d in desenler)
    for izinli in (
        "python -X utf8 kurulum/birlestir.py 278",
        "gh pr view 278 --repo zPfizer/tansu --json state,mergedAt",
        "gh pr view 278 --json mergedAt,mergeable",
        "gh -R zPfizer/tansu pr view 279 --json state,mergedAt",
    ):
        assert not any(fnmatch.fnmatchcase(izinli, d) for d in desenler), izinli
