import ast
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest


_yol = Path(__file__).resolve().parents[1] / ".github" / "dod_kontrol.py"
_tanim = importlib.util.spec_from_file_location("dod_kontrol", _yol)
_modul = importlib.util.module_from_spec(_tanim)
_tanim.loader.exec_module(_modul)
hatalar = _modul.hatalar

GECERLI = """## Ne değişti
Değişiklik.
Closes #49
## Kabul ölçütleri (Levent kontrol eder)
- [X] İstenen davranış sağlandı.
- [x] İkinci ölçüt.
## Gerçek veri kanıtı
```text
Gerçek koşu çıktısı
```
## Bağımsız inceleme
Denetçi: Ayşe
Denetlenen commit: 0123456789abcdef0123456789abcdef01234567
Sonuç: GEÇTİ
"""
BASLIK = "#49 · Başlık"
R6 = "Kural 6: PR başlığı #<N> · ile başlamalı ve N, Closes #<N> satırındaki sayı olmalı."
SHA = "0123456789abcdef0123456789abcdef01234567"
SHA_BASKA = "fedcba9876543210fedcba9876543210fedcba98"
R1 = "Kural 1: PR gövdesinde Closes #<issue> satırı olmalı."
R2 = "Kural 2: ## Kabul ölçütleri bölümünde en az bir kutu olmalı ve her kutu işaretli olmalı."
R3 = "Kural 3: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu olmalı."
R4 = "Kural 4: ## Bağımsız inceleme: {}."


def test_gecerli():
    assert hatalar(GECERLI, baslik=BASLIK) == []
    assert hatalar(GECERLI.replace("\n", "\r\n"), baslik=BASLIK) == []


@pytest.mark.parametrize("govde", [None, "", " \r\n "])
def test_bos_govde(govde):
    assert hatalar(govde, baslik=BASLIK) == [
        R1,
        R2,
        R3,
        R4.format("bölüm yok"),
        "Kural 5: PR gövdesinde Denetlenen commit: <40 küçük harfli onaltılı hane> "
        "satırı tek olmalı (0 satır var).",
        R6,
    ]


@pytest.mark.parametrize(
    "satir",
    [
        "Closes #49",
        "closes #49",
        "Close #1",
        "FIXES #7",
        "Resolved #12",
        "  Resolves #123  ",
    ],
)
def test_kural_1_kapatma_satiri_gecer(satir):
    assert hatalar(GECERLI.replace("Closes #49", satir), baslik=BASLIK) == (
        [] if satir.lower() == "closes #49" else [R6]
    )


@pytest.mark.parametrize(
    "satir",
    [
        "",
        "Closes #<issue>",
        "Closes 49",
        "Closes: #49",
        "Closes #",
        "Closes #49 ve #50",  # tek satır tek issue: GitHub her issue için ayrı anahtar sözcük ister
        "Bu PR Closes #49",
        "<!-- Closes #49 -->",  # CI yorumu siler
    ],
)
def test_kural_1_kapatma_satiri_eksik_ya_da_bozuk(satir):
    assert hatalar(GECERLI.replace("Closes #49", satir), baslik=BASLIK) == [R1, R6]


@pytest.mark.parametrize(
    "yeni",
    [
        "## Kabul\n- [x] İstenen davranış sağlandı.\n",  # başlık yok
        "## Kabul ölçütleri\nkutu yok\n",
        "## Kabul ölçütleri\n- [ ] İstenen davranış sağlandı.\n",
    ],
)
def test_kural_2_kabul(yeni):
    govde = GECERLI.replace(
        "## Kabul ölçütleri (Levent kontrol eder)\n- [X] İstenen davranış sağlandı.\n"
        "- [x] İkinci ölçüt.\n",
        yeni,
    )
    assert hatalar(govde, baslik=BASLIK) == [R2]


def test_kural_2_isaretsiz_ikinci_kutu_ve_yorumdaki_kutu():
    assert hatalar(GECERLI.replace("- [x] İkinci", "- [ ] İkinci"), baslik=BASLIK) == [
        R2
    ]
    assert (
        hatalar(GECERLI.replace("- [x] İkinci", "<!-- - [ ] İkinci -->"), baslik=BASLIK)
        == []
    )


@pytest.mark.parametrize("kod", ["```\n\n```", "Gerçek koşu çıktısı", "```\nçıktı"])
def test_kural_3_kod_kaniti_yok(kod):
    govde = GECERLI.replace("```text\nGerçek koşu çıktısı\n```", kod)
    assert hatalar(govde, baslik=BASLIK) == [R3]


@pytest.mark.parametrize("karar", ["geçti", "GEÇTİ", "NOTLU GEÇTİ"])
def test_kural_4_kabul_edilen_kararlar(karar):
    assert (
        hatalar(GECERLI.replace("Sonuç: GEÇTİ", f"Sonuç: {karar}"), baslik=BASLIK) == []
    )


@pytest.mark.parametrize(
    ("eski", "yeni", "ayrinti"),
    [
        ("Denetçi: Ayşe", "Denetçi: ", "Denetçi: alanı boş veya eksik"),
        ("Sonuç: GEÇTİ", "Sonuç: Geçti", "Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik"),
        ("Sonuç: GEÇTİ", "Sonuç: KALDI", "Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik"),
        ("Sonuç: GEÇTİ", "", "Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik"),
        (
            "Sonuç: GEÇTİ",
            "Sonuç: GEÇTİ\nSonuç: GEÇTİ",
            "Sonuç: satırı tek olmalı (2 satır var)",
        ),
    ],
)
def test_kural_4_inceleme(eski, yeni, ayrinti):
    assert hatalar(GECERLI.replace(eski, yeni), baslik=BASLIK) == [R4.format(ayrinti)]


def test_kural_4_yorumdaki_sonuc_satir_sayilmaz():
    govde = GECERLI.replace("Sonuç: GEÇTİ", "<!-- Sonuç: KALDI -->\nSonuç: GEÇTİ")
    assert hatalar(govde, baslik=BASLIK) == []


DENETLENEN = f"Denetlenen commit: {SHA}\n"
R5_SATIR = (
    "Kural 5: PR gövdesinde Denetlenen commit: <40 küçük harfli onaltılı hane> "
    "satırı tek olmalı ({} satır var)."
)
R5_DEGER = "Kural 5: Denetlenen commit: değeri 40 küçük harfli onaltılı hane olmalı."
R5_TABAN = "Kural 5: Denetlenen commit PR başı değil ve taban dal bilinmiyor."
R5_BIRLESME = (
    "Kural 5: Denetlenen commit ({}) PR başı ({}) değil; "
    "sonraki commit'ler temiz bir taban birleştirmesi değil."
)


@pytest.mark.parametrize(
    ("yeni", "sayi"), [("", 0), (DENETLENEN * 2, 2), (DENETLENEN * 3, 3)]
)
def test_kural_5_satir_tek_olmali(yeni, sayi):
    assert hatalar(GECERLI.replace(DENETLENEN, yeni), baslik=BASLIK) == [
        R5_SATIR.format(sayi)
    ]


@pytest.mark.parametrize(
    "deger", ["", "yok", SHA.upper(), SHA[:39], SHA + "0", "g" * 40, "`" + SHA + "`"]
)
def test_kural_5_deger_40_kucuk_onaltili_olmali(deger):
    govde = GECERLI.replace(DENETLENEN, f"Denetlenen commit: {deger}\n")
    assert hatalar(govde, baslik=BASLIK) == [R5_DEGER]


def test_kural_5_yorumdaki_satir_sayilmaz():
    govde = GECERLI.replace(DENETLENEN, DENETLENEN + "<!--\n" + DENETLENEN + "-->\n")
    assert hatalar(govde, baslik=BASLIK) == []
    assert hatalar(
        GECERLI.replace(DENETLENEN, "<!-- " + DENETLENEN + "-->\n"), baslik=BASLIK
    ) == [R5_SATIR.format(0)]


def test_kural_5_pr_basi_esit_ya_da_taban_bilinmiyor():
    assert hatalar(GECERLI, SHA, baslik=BASLIK) == []
    assert hatalar(GECERLI, None, baslik=BASLIK) == []
    assert hatalar(GECERLI, SHA_BASKA, baslik=BASLIK) == [R5_TABAN]


def _git(dizin, *arg):
    return subprocess.run(
        ["git", *arg],
        cwd=dizin,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def _commit(dizin, dosya, metin):
    (dizin / dosya).write_text(metin, encoding="utf-8")
    _git(dizin, "add", dosya)
    _git(dizin, "commit", "-m", metin)
    return _git(dizin, "rev-parse", "HEAD")


@pytest.fixture
def depo(tmp_path):
    for arg in (
        ("init", "-b", "master"),
        ("config", "user.name", "Deneme"),
        ("config", "user.email", "deneme@example.com"),
        ("config", "commit.gpgsign", "false"),
        ("config", "core.autocrlf", "false"),
    ):
        _git(tmp_path, *arg)
    _commit(tmp_path, "a.txt", "A")
    _git(tmp_path, "checkout", "-b", "pr")
    b = _commit(tmp_path, "b.txt", "B")
    _git(tmp_path, "checkout", "master")
    _commit(tmp_path, "c.txt", "C")
    _git(tmp_path, "checkout", "pr")
    _git(tmp_path, "merge", "--no-edit", "master")
    return tmp_path, b, _git(tmp_path, "rev-parse", "HEAD")


def _govde_git(denetlenen):
    return GECERLI.replace(DENETLENEN, f"Denetlenen commit: {denetlenen}\n")


def test_kural_5_temiz_taban_birlestirmesi_gecer(depo):
    dizin, b, m = depo
    assert hatalar(_govde_git(b), m, taban="master", dizin=dizin, baslik=BASLIK) == []


def test_kural_5_denetlenen_pr_basi_ise_git_gerekmez(depo):
    dizin, _, m = depo
    assert hatalar(_govde_git(m), m, taban="master", dizin=dizin, baslik=BASLIK) == []


def test_kural_5_duz_commit_reddedilir(depo):
    dizin, b, _ = depo
    d = _commit(dizin, "d.txt", "D")
    assert hatalar(_govde_git(b), d, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, d)
    ]


def test_kural_5_elle_degisen_birlestirme_reddedilir(depo):
    dizin, b, _ = depo
    _git(dizin, "checkout", "-b", "kotu", b)
    _git(dizin, "merge", "--no-commit", "--no-ff", "master")
    (dizin / "b.txt").write_text("elle", encoding="utf-8")
    _git(dizin, "add", "b.txt")
    _git(dizin, "commit", "--no-edit")
    kotu = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(_govde_git(b), kotu, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, kotu)
    ]


def test_kural_5_taban_disi_ikinci_ebeveyn_reddedilir(depo):
    dizin, b, _ = depo
    _git(dizin, "checkout", "-b", "yan", "master")
    _commit(dizin, "y.txt", "Y")
    _git(dizin, "checkout", "-b", "baska", b)
    _git(dizin, "merge", "--no-edit", "yan")
    baska = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(
        _govde_git(b), baska, taban="master", dizin=dizin, baslik=BASLIK
    ) == [R5_BIRLESME.format(b, baska)]


def test_kural_5_bilinmeyen_sha_reddedilir(depo):
    dizin, _, m = depo
    assert hatalar(
        _govde_git(SHA_BASKA), m, taban="master", dizin=dizin, baslik=BASLIK
    ) == [R5_BIRLESME.format(SHA_BASKA, m)]


def _celiski_birlesmesi(dizin):
    _git(dizin, "checkout", "master")
    _commit(dizin, "s.txt", "a\n")
    _git(dizin, "checkout", "-b", "yan2")
    b = _commit(dizin, "s.txt", "b\n")
    _git(dizin, "checkout", "master")
    _commit(dizin, "s.txt", "c\n")
    _git(dizin, "checkout", "yan2")
    with pytest.raises(subprocess.CalledProcessError):
        _git(dizin, "merge", "--no-edit", "master")
    (dizin / "s.txt").write_text("b\nc\n", encoding="utf-8")
    _git(dizin, "add", "s.txt")
    _git(dizin, "commit", "--no-edit")
    return b, _git(dizin, "rev-parse", "HEAD")


def test_kural_5_elle_cozulen_celiski_taban_ozelligiyle_gizlenmez(depo):
    dizin, _, _ = depo
    b, m = _celiski_birlesmesi(dizin)
    _git(dizin, "checkout", "master")
    _commit(dizin, ".gitattributes", "*.txt merge=union\n")
    assert hatalar(_govde_git(b), m, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, m)
    ]


def test_kural_5_info_attributes_celiskiyi_gizlemez(depo):
    dizin, _, _ = depo
    b, m = _celiski_birlesmesi(dizin)
    (dizin / ".git" / "info" / "attributes").write_text(
        "*.txt merge=union\n", encoding="utf-8"
    )
    assert hatalar(_govde_git(b), m, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, m)
    ]


def test_kural_5_ayni_dosyada_iki_taraf_degisirse_reddedilir(depo):
    dizin, _, _ = depo
    _git(dizin, "checkout", "master")
    _commit(dizin, "f.txt", "1\n2\n3\n4\n5\n6\n7\n8\n")
    _git(dizin, "checkout", "-b", "yan3")
    b = _commit(dizin, "f.txt", "0\n1\n2\n3\n4\n5\n6\n7\n8\n")
    _git(dizin, "checkout", "master")
    _commit(dizin, "f.txt", "1\n2\n3\n4\n5\n6\n7\n8\n9\n")
    _git(dizin, "checkout", "yan3")
    _git(dizin, "merge", "--no-edit", "master")
    m = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(_govde_git(b), m, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, m)
    ]


@pytest.mark.parametrize(
    ("surucu", "elle_degistir", "kip", "gecerli"),
    [
        ("union", False, "100644", True),
        ("text", False, "100644", False),
        ("union", True, "100644", False),
        ("union", False, "100755", False),
        ("union", False, "120000", False),
    ],
)
def test_kural_5_union_ortak_dosyanin_icerigini_dogrular(
    depo, surucu, elle_degistir, kip, gecerli
):
    dizin, _, _ = depo
    _git(dizin, "checkout", "master")
    _commit(dizin, ".gitattributes", f"CHANGELOG.md merge={surucu}\n")
    _commit(dizin, "CHANGELOG.md", "- Eski.\n")
    _git(dizin, "checkout", "-b", "union-dal")
    b = _commit(dizin, "CHANGELOG.md", "- Dal.\n- Eski.\n")
    _git(dizin, "checkout", "master")
    _commit(dizin, "CHANGELOG.md", "- Taban.\n- Eski.\n")
    _git(dizin, "checkout", "union-dal")
    if surucu == "union":
        _git(dizin, "merge", "--no-commit", "--no-ff", "master")
    else:
        with pytest.raises(subprocess.CalledProcessError):
            _git(dizin, "merge", "--no-commit", "--no-ff", "master")
        (dizin / "CHANGELOG.md").write_text(
            "- Dal.\n- Taban.\n- Eski.\n", encoding="utf-8"
        )
    assert (dizin / "CHANGELOG.md").read_text(encoding="utf-8") == (
        "- Dal.\n- Taban.\n- Eski.\n"
    )
    if elle_degistir:
        (dizin / "CHANGELOG.md").write_text(
            "- Dal.\n- Taban.\n- Eski.\n- Elle.\n", encoding="utf-8"
        )
    _git(dizin, "add", "CHANGELOG.md")
    blob = _git(dizin, "rev-parse", ":CHANGELOG.md")
    _git(dizin, "update-index", "--cacheinfo", f"{kip},{blob},CHANGELOG.md")
    _git(dizin, "commit", "--no-edit")
    m = _git(dizin, "rev-parse", "HEAD")
    assert _git(dizin, "ls-tree", m, "--", "CHANGELOG.md") == (
        f"{kip} blob {blob}\tCHANGELOG.md"
    )
    assert hatalar(_govde_git(b), m, taban="master", dizin=dizin, baslik=BASLIK) == (
        [] if gecerli else [R5_BIRLESME.format(b, m)]
    )


def test_kural_5_silme_ve_yeniden_adlandirma_gecer(depo):
    dizin, b, _ = depo
    _git(dizin, "checkout", "master")
    _git(dizin, "rm", "a.txt")
    _git(dizin, "commit", "-m", "sil")
    _git(dizin, "mv", "c.txt", "d.txt")
    _git(dizin, "commit", "-m", "ad")
    _git(dizin, "checkout", "-b", "yan4", b)
    _git(dizin, "merge", "--no-edit", "master")
    m = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(_govde_git(b), m, taban="master", dizin=dizin, baslik=BASLIK) == []


def _kotu_birlesme(dizin, b, degistir):
    _git(dizin, "checkout", "-b", "kotu", b)
    _git(dizin, "merge", "--no-commit", "--no-ff", "master")
    degistir(dizin)
    _git(dizin, "add", "-A")
    _git(dizin, "commit", "--no-edit")
    return _git(dizin, "rev-parse", "HEAD")


@pytest.mark.parametrize("dosya", ["fazla.txt", "c.txt"])
def test_kural_5_fazla_dosya_ya_da_dusen_dosya_reddedilir(depo, dosya):
    dizin, b, _ = depo

    def degistir(dizin):
        if dosya == "c.txt":
            (dizin / dosya).unlink()
        else:
            (dizin / dosya).write_text("x", encoding="utf-8")

    kotu = _kotu_birlesme(dizin, b, degistir)
    assert hatalar(_govde_git(b), kotu, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, kotu)
    ]


def test_kural_5_capraz_birlesme_reddedilir(depo):
    dizin, _, _ = depo
    _git(dizin, "checkout", "-b", "ca", "master")
    a1 = _commit(dizin, "a1.txt", "1")
    _git(dizin, "checkout", "-b", "cb", "master")
    _commit(dizin, "b1.txt", "2")
    _git(dizin, "checkout", "ca")
    _git(dizin, "merge", "--no-edit", "cb")
    _git(dizin, "checkout", "cb")
    _git(dizin, "merge", "--no-edit", a1)
    _git(dizin, "checkout", "ca")
    _git(dizin, "merge", "--no-edit", "cb")
    x = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(_govde_git(a1), x, taban="cb", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(a1, x)
    ]


@pytest.mark.parametrize("taban", ["yok-dal", "master^{tree}"])
def test_kural_5_taban_gecersizse_reddedilir(depo, taban):
    dizin, b, m = depo
    assert hatalar(_govde_git(b), m, taban=taban, dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, m)
    ]


def test_kural_5_denetlenen_agac_ya_da_etiket(depo):
    dizin, b, m = depo
    agac = _git(dizin, "rev-parse", f"{b}^{{tree}}")
    assert hatalar(_govde_git(agac), m, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(agac, m)
    ]
    _git(dizin, "tag", "-a", "-m", "e", "etiket", b)
    etiket = _git(dizin, "rev-parse", "etiket")
    assert (
        hatalar(_govde_git(etiket), m, taban="master", dizin=dizin, baslik=BASLIK) == []
    )


@pytest.mark.parametrize("alt", ["rev-list", "merge-base", "diff-tree"])
def test_kural_5_git_donus_kodu_hatasi_reddedilir(depo, monkeypatch, alt):
    dizin, b, m = depo
    gercek = subprocess.run

    def sahte(arg, **kw):
        sonuc = gercek(arg, **{**kw, "check": False})
        if alt in arg[:3]:
            if kw.get("check"):
                raise subprocess.CalledProcessError(128, arg, sonuc.stdout)
            sonuc.returncode = 128
        return sonuc

    monkeypatch.setattr(_modul.subprocess, "run", sahte)
    assert hatalar(_govde_git(b), m, taban="master", dizin=dizin, baslik=BASLIK) == [
        R5_BIRLESME.format(b, m)
    ]


def test_sablon_gecerli_govdeye_doldurulunca_gecer():
    yol = Path(__file__).resolve().parents[1] / ".github" / "pull_request_template.md"
    sablon = yol.read_text(encoding="utf-8")
    govde = (
        sablon.replace("Closes #<issue>", "Closes #49")
        .replace("- [ ]", "- [x] Ölçüt.")
        .replace("Denetçi: ", "Denetçi: Ayşe", 1)
        .replace("Denetlenen commit: ", DENETLENEN.rstrip("\n"), 1)
        .replace("Sonuç: \n", "Sonuç: GEÇTİ\n")
        .replace("## Bağımsız inceleme", "```text\nçıktı\n```\n## Bağımsız inceleme")
    )
    assert hatalar(govde, SHA, baslik=BASLIK) == []
    assert len(hatalar(sablon, baslik=BASLIK)) == 6


def test_dod_kontrol_python_312_soz_dizimi():
    # dod.yml uses the runner's default python (no setup-python).
    metin = _yol.read_text(encoding="utf-8")
    ast.parse(metin, feature_version=(3, 12))


def test_dod_yml_taslak_ve_sha():
    yol = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "dod.yml"
    metin = yol.read_text(encoding="utf-8")
    for parca in (
        "draft == false",
        "ready_for_review",
        "PR_BAS_SHA: ${{ github.event.pull_request.head.sha }}",
        "fetch-depth: 0",
        "PR_BASLIK: ${{ github.event.pull_request.title }}",
    ):
        assert parca in metin


def test_kapi_betigi():
    yol = Path(__file__).resolve().parents[1] / "kurulum" / "kapi.ps1"
    metin = yol.read_bytes().decode("ascii")
    for parca in (
        "-m pytest -q",
        "ruff check .",
        "ruff format --check .",
        "git diff --check origin/master",
        "kapi: HEAD",
        "temiz",
        "kirli",
    ):
        assert parca in metin
    assert "--untracked-files=no" not in metin


@pytest.mark.parametrize(
    ("baslik", "kod"),
    [
        (None, 1),
        ("", 1),
        ("Başlık", 1),
        ("#49 Başlık", 1),
        ("#49 ·Başlık", 1),
        (" #49 · Başlık", 1),
        ("#50 · Başlık", 1),
        ("#49 · Başlık", 0),
    ],
)
def test_kural_6_baslik_cli(baslik, kod):
    ortam = {**os.environ, "PR_GOVDE": GECERLI, "PR_BAS_SHA": SHA}
    ortam.pop("PR_BASLIK", None)
    if baslik is not None:
        ortam["PR_BASLIK"] = baslik
    sonuc = subprocess.run(
        [sys.executable, "-X", "utf8", str(_yol)],
        env=ortam,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert sonuc.returncode == kod
    if kod:
        assert sonuc.stdout.startswith("Kural 6:")
    else:
        assert sonuc.stdout.strip() == "Definition of Done listesi tam."


@pytest.mark.parametrize(
    ("kapatma", "beklenen"),
    [
        ("Closes #49\nFixes #50", []),
        ("Closes #50\nFixes #49", [R6]),
        ("Closes #50\nCloses #49", []),
        ("Closes #50\n<!-- Closes #49 -->", [R6]),
        ("  closes #49  ", []),
    ],
)
def test_kural_6_kapatma_eslesmesi(kapatma, beklenen):
    govde = GECERLI.replace("Closes #49", kapatma)
    assert hatalar(govde, baslik=BASLIK) == beklenen


BELGE_GOVDE = GECERLI.replace(
    "Closes #49", "Issue yok: Karar gerektirmeyen belge düzeltmesi."
)
BELGE_BASLIK = "Belge · Açıklamaları düzelt"
R6_BELGE = "Kural 6: Issue'suz belge PR başlığı Belge · <başlık> biçiminde olmalı."


@pytest.fixture
def belge_depo(tmp_path):
    for arg in (
        ("init", "-b", "master"),
        ("config", "user.name", "Deneme"),
        ("config", "user.email", "deneme@example.com"),
        ("config", "commit.gpgsign", "false"),
        ("config", "core.autocrlf", "false"),
    ):
        _git(tmp_path, *arg)
    _commit(tmp_path, "README.md", "İlk açıklama")
    _git(tmp_path, "branch", "origin/master")
    _git(tmp_path, "checkout", "-b", "belge")
    sha = _commit(tmp_path, "README.md", "Düzeltilmiş açıklama")
    return tmp_path, sha


def test_issuesuz_belge_pr_gecer(belge_depo):
    dizin, sha = belge_depo
    assert (
        hatalar(
            _govde_git(sha).replace("Closes #49", "Issue yok: Belge düzeltmesi."),
            sha,
            taban="origin/master",
            dizin=dizin,
            baslik=BELGE_BASLIK,
        )
        == []
    )


@pytest.mark.parametrize(
    "satir",
    [
        "",
        "Issue yok:",
        "Issue yok:   ",
        "Issue yok: gerekçe\n<!-- açıklama -->",
        "<!-- Issue yok: gerekçe -->",
        "Bu PR için Issue yok: gerekçe",
        "Issue yok gerekçe",
    ],
)
def test_issuesuz_belge_gerekcesi(belge_depo, satir):
    dizin, sha = belge_depo
    govde = _govde_git(sha).replace("Closes #49", satir)
    beklenen = [] if satir.startswith("Issue yok: gerekçe\n") else [R1, R6]
    assert (
        hatalar(govde, sha, taban="origin/master", dizin=dizin, baslik=BELGE_BASLIK)
        == beklenen
    )


@pytest.mark.parametrize(
    "baslik",
    [
        None,
        "",
        "Başlık",
        "#49 · Başlık",
        "Belge · ",
        "Belge ·Başlık",
        " Belge · Başlık",
    ],
)
def test_issuesuz_belge_basligi(belge_depo, baslik):
    dizin, sha = belge_depo
    govde = BELGE_GOVDE.replace(SHA, sha)
    assert hatalar(govde, sha, taban="origin/master", dizin=dizin, baslik=baslik) == [
        R6_BELGE
    ]


@pytest.mark.parametrize(
    ("dosya", "beklenen"),
    [
        ("CHANGELOG.md", []),
        ("docs/açıklama.md", []),
        ("docs/.github-notlari.md", []),
        ("docs/TASARIM.md", [R1, R6]),
        ("docs/KURALLAR.md", [R1, R6]),
        ("docs/kurallar/A-yapi-bolge.md", [R1, R6]),
        ("docs/agents/issue-tracker.md", [R1, R6]),
        ("CODING_STANDARDS.md", [R1, R6]),
        ("DEFINITION_OF_DONE.md", [R1, R6]),
        ("GLOSSARY.md", [R1, R6]),
        ("tansu/a.py", [R1, R6]),
        ("tests/test_a.py", [R1, R6]),
        (".github/workflows/ci.yml", [R1, R6]),
        (".github/pull_request_template.md", [R1, R6]),
        (".claude/skills/a/SKILL.md", [R1, R6]),
        ("AGENTS.md", [R1, R6]),
        ("CLAUDE.md", [R1, R6]),
        ("docs/AGENTS.md", [R1, R6]),
        ("docs/CLAUDE.md", [R1, R6]),
        ("ayar.toml", [R1, R6]),
    ],
)
def test_issuesuz_pr_tum_dosyalari_denetler(belge_depo, dosya, beklenen):
    dizin, _ = belge_depo
    (dizin / dosya).parent.mkdir(parents=True, exist_ok=True)
    sha = _commit(dizin, dosya, "Yeni içerik")
    govde = BELGE_GOVDE.replace(SHA, sha)
    assert (
        hatalar(govde, sha, taban="origin/master", dizin=dizin, baslik=BELGE_BASLIK)
        == beklenen
    )
    # Issue bağlantısı varsa aynı dosya listesi eski denetimi değiştirmez.
    assert hatalar(_govde_git(sha), sha, dizin=dizin, baslik=BASLIK) == []


@pytest.mark.parametrize("taban", [None, "olmayan-dal", "HEAD"])
def test_issuesuz_pr_bos_ya_da_bilinmeyen_dosya_listesi_reddedilir(belge_depo, taban):
    dizin, sha = belge_depo
    assert hatalar(
        BELGE_GOVDE.replace(SHA, sha),
        sha,
        taban=taban,
        dizin=dizin,
        baslik=BELGE_BASLIK,
    ) == [R1, R6]


def test_issuesuz_pr_git_baslatilamazsa_reddedilir(belge_depo):
    dizin, sha = belge_depo
    assert hatalar(
        BELGE_GOVDE.replace(SHA, sha),
        sha,
        taban="origin/master",
        dizin=dizin / "olmayan",
        baslik=BELGE_BASLIK,
    ) == [R1, R6]


def test_issuesuz_pr_koddan_belgeye_yeniden_adlandirma_reddedilir(belge_depo):
    dizin, _ = belge_depo
    _git(dizin, "checkout", "master")
    _commit(dizin, "kod.py", "print('x')\n")
    _git(dizin, "branch", "-f", "origin/master")
    _git(dizin, "checkout", "-b", "ad-degisimi")
    _git(dizin, "mv", "kod.py", "kod.md")
    _git(dizin, "commit", "-m", "Ad değişimi")
    sha = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(
        BELGE_GOVDE.replace(SHA, sha),
        sha,
        taban="origin/master",
        dizin=dizin,
        baslik=BELGE_BASLIK,
    ) == [R1, R6]


@pytest.mark.parametrize("kod_degisti", [False, True])
def test_issuesuz_pr_cli_git_dosya_listesini_kullanir(belge_depo, kod_degisti):
    dizin, sha = belge_depo
    if kod_degisti:
        sha = _commit(dizin, "kod.py", "print('x')\n")
    ortam = {
        **os.environ,
        "PR_GOVDE": BELGE_GOVDE.replace(SHA, sha),
        "PR_BASLIK": BELGE_BASLIK,
        "PR_BAS_SHA": sha,
        "GITHUB_BASE_REF": "master",
    }
    sonuc = subprocess.run(
        [sys.executable, "-X", "utf8", str(_yol)],
        cwd=dizin,
        env=ortam,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert sonuc.returncode == (1 if kod_degisti else 0)
    assert sonuc.stdout.strip() == (
        R1 + "\n" + R6 if kod_degisti else "Definition of Done listesi tam."
    )
