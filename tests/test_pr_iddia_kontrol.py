from kurulum.pr_iddia_kontrol import denetle

PR = {
    "files": [
        {"path": "tansu/islem.py", "additions": 12, "deletions": 3},
        {"path": "tests/test_islem.py", "additions": 30, "deletions": 0},
        {"path": "kanit/acik-sorular.md", "additions": 2, "deletions": 1},
    ],
    "additions": 44,
    "deletions": 4,
    "changedFiles": 3,
}


def test_dogru_govde_uyusur():
    govde = (
        "- `tansu/islem.py` (+12 -3): kural.\n"
        "- `tests/test_*.py`: kırmızı test.\n"
        "- `kanit/`: kayıt.\n"
        "Toplam 3 dosya, +44 -4.\n"
        "- `pytest -q`: 235 geçti, 1 atlandı.\n"
    )
    assert denetle(govde, PR, 236) == ([], [])


def test_yanlis_sayilar_ve_eksik_dosya_bulunur():
    govde = (
        "- `tansu/islem.py` +12 -4\n"
        "- `tansu/veri.py` +1 -1\n"
        "Toplam 2 dosya, +40 -4.\n"
        "`pytest -q`: 230 geçti\n"
    )
    sorunlar, _ = denetle(govde, PR, 236)
    assert sorunlar == [
        "`tests/test_islem.py` değişti ama gövdede adı yok",
        "`kanit/acik-sorular.md` değişti ama gövdede adı yok",
        "`tansu/islem.py`: gövde +12 -4, gerçek +12 -3",
        "`tansu/veri.py` +1 -1 denmiş, dosya PR'da değişmemiş",
        "toplam: gövde +40 -4, gerçek +44 -4",
        "dosya sayısı: gövde 2, gerçek 3",
        "pytest: gövde 230 test, CI 236 test",
    ]


def test_kismi_kosu_ve_bitmemis_ci_denetlenmez():
    govde = (
        "`tansu/islem.py` `tests/test_islem.py` `kanit/acik-sorular.md`\n"
        "`pytest -q tests/test_islem.py`: 1 kaldı\n"
        "`pytest -q`: 236 geçti\n"
    )
    sorunlar, notlar = denetle(govde, PR, None)
    assert sorunlar == []
    assert notlar == [
        "kısmi pytest satırı denetlenmedi: `pytest -q tests/test_islem.py`: 1 kaldı",
        "pytest sayısı denetlenmedi: baş commit'in ci koşusu yok ya da bitmedi",
    ]


def test_git_stat_ozeti_denetlenir():
    govde = "`tansu/` `tests/` `kanit/`\n3 files changed, 44 insertions(+), 5 deletions(-)\n"
    assert denetle(govde, PR, None)[0] == ["toplam: gövde 5 silme, gerçek 4"]
