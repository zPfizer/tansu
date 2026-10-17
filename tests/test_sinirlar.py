"""Bilet 08 iddia denetimi: biletteki "Tanınan biçimler ve sınırlar" cümlelerinin her biri bir testtir.

Okunmaz diye yazılan biçim gerçekten okunmaz (kırık sayı yazılsa da hata çıkmaz); okunur diye yazılan biçim
gerçekten okunur. Bir cümle yanlışsa test kırılır ve cümle düzeltilir.
"""

import re
import subprocess

import pytest
from test_atif import _belgeler, _sorgu
from test_sahipler import _depo, _yaz

from atif_araclari import (
    KOK,
    atif_kirikleri,
    etiket_kirikleri,
    havuz_sorunlari,
    yol_kirikleri,
)


def _atif(tmp_path, metin):
    _belgeler(tmp_path)
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    return atif_kirikleri(tmp_path, [tmp_path / "not.md"])


@pytest.mark.parametrize(
    "metin",
    [
        "TASARIM'ın §99",
        "TASARIM bölüm 99",
        "tasarım 99 ve Tasarım §99",
        "TASARIM § 99",
        "TASARIM\n§99",
        "TASARIM 5.1 ile §99",
        "TASARIM 5.1 veya §99",
        "TASARIM 5.1; §99",
        "TASARIM §5.1—5.99",
        "TASARIM 5.1, 99",
        "TASARIM 5 madde 1",  # 5.1 başlığı vardır: alt başlıklı bölümde madde atfı başlıkla karışır
    ],
)
def test_tanimsiz_atif_bicimleri_okunmaz(tmp_path, metin):
    assert _atif(tmp_path, metin) == []


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        (
            "TASARIM 5.1.4",
            ["not.md:1: TASARIM 5.1.4"],
        ),  # üç düzey numara başlık değildir: hata
        ("TASARIM 5.1 ve §99", ["not.md:1: TASARIM §99"]),
        (
            "TASARIM §5.1 – 99",
            ["not.md:1: TASARIM §99"],
        ),  # en-dash aralığı, düz uç dahil
        (
            "TASARIM §5.1 - 5.99",
            ["not.md:1: TASARIM §5.99"],
        ),  # tire yalnız noktalı uçta
        ("TASARIM 5 madde 99", ["not.md:1: TASARIM §5.99"]),
    ],
)
def test_tanimli_atif_bicimleri_okunur(tmp_path, metin, beklenen):
    assert _atif(tmp_path, metin) == beklenen


@pytest.mark.parametrize(
    "metin",
    [
        '"Hash kapsamı" (TASARIM 5.2)',  # atıftan önce gelen başlık
        "TASARIM 5.2 'Hash kapsamı'",  # ASCII tek tırnak
        'TASARIM 5.1, 5.2 "Hash kapsamı"',  # liste sonrası alıntı
        'TASARIM 5.2, 5.1 "Kural kaydı"',
    ],
)
def test_alinti_okunmayan_bicimler(tmp_path, metin):
    assert _atif(tmp_path, metin) == []


@pytest.mark.parametrize(
    "metin",
    ["B-1/99", "B-1–99", "İ: 08-027 ve 08-999", "B-3b", "P3 M1 Sorgu S13", "B-n"],
)
def test_okunmayan_karar_etiketi_bicimleri(tmp_path, metin):
    sorgu = _sorgu(tmp_path)
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    assert etiket_kirikleri(tmp_path, [tmp_path / "not.md"], sorgu) == []


@pytest.mark.parametrize(
    "metin",
    [
        "tansu/yok.py",  # backtick dışındaki çıplak metin
        "bkz tansu/yok.py ve docs/yok.md.",
        "`./tansu/yok.py`",  # ./ öneki
        '<a href="docs/yok.md">x</a> <img src="docs/yok.png">',  # HTML bağlantıları
        "`tansu/kayit.py tansu/yok.py`",  # ilk sözcükten sonrası
        "```\ntansu/yok.py\ndocs/yok.md\n```",  # çitli blokta çıplak satırlar
        "`veri/yok.x` `rapor/yok.x` `gunluk/yok.x`",  # çalışma çıktısı klasörleri
        "`tansu/yok_<x>.py` `docs/yok_*.md` `tests/yokNN.py`",  # şablon işaretli yol
        "`docs/sorgu/yok.md`",  # yerel kök bu depoda yok (CI durumu)
    ],
)
def test_okunmayan_yol_bicimleri(tmp_path, metin):
    _depo(tmp_path)
    yol = _yaz(tmp_path, "docs/agents/y.md", metin)
    assert yol_kirikleri(tmp_path, [yol]) == []


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        (r"`tests\yok.py`", ["docs/agents/y.md:1: tests/yok.py"]),
        (
            r"`.github\workflows\yok.yml`",
            ["docs/agents/y.md:1: .github/workflows/yok.yml"],
        ),
        (r"`kayit\yok.jsonl:7`", ["docs/agents/y.md:1: kayit/yok.jsonl"]),
        ("[x](./yok.md)", ["docs/agents/y.md:1: docs/agents/yok.md"]),
        (
            "```\n`tansu/yok.py`\n```",
            ["docs/agents/y.md:2: tansu/yok.py"],
        ),  # çit içinde backtick'li aralık okunur
        (
            "`tansu/yok.py::test_x` `tansu/yok2.py#bolum`",
            ["docs/agents/y.md:1: tansu/yok.py", "docs/agents/y.md:1: tansu/yok2.py"],
        ),
    ],
)
def test_okunan_yol_bicimleri(tmp_path, metin, beklenen):
    _depo(tmp_path)
    yol = _yaz(tmp_path, "docs/agents/y.md", metin)
    assert yol_kirikleri(tmp_path, [yol]) == beklenen


def _havuz(kok, adlar, *, alt=()):
    havuz = kok / "havuz"
    havuz.mkdir()
    for ad in adlar:
        (havuz / f"{ad}.md").write_text("not", encoding="utf-8")
    for goreli in alt:
        yol = havuz / goreli
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text("x", encoding="utf-8")
    return havuz


def _kurallar(kok, metin):
    (kok / "docs" / "kurallar").mkdir(parents=True)
    (kok / "docs" / "KURALLAR.md").write_text("## X\n", encoding="utf-8")
    (kok / "docs" / "kurallar" / "A-x.md").write_text(metin, encoding="utf-8")


def test_havuz_alt_klasor_ve_md_olmayan_dosya_sayilmaz(tmp_path):
    _kurallar(tmp_path, "not-bir\n")
    havuz = _havuz(
        tmp_path,
        ["not-bir"],
        alt=["assets/not-iki.md", "not-uc.txt", "alt/gorsel-paket-1-x.md"],
    )
    assert havuz_sorunlari(tmp_path, havuz) == []


def test_havuz_duz_sozcuklu_ad_yalniz_tam_adla_kapsanir(tmp_path):
    _kurallar(tmp_path, "not-bir\n")
    havuz = _havuz(tmp_path, ["not-bir-iki", "tansu-calisma-kurallari"])
    assert havuz_sorunlari(tmp_path, havuz) == [
        "not-bir-iki",
        "tansu-calisma-kurallari",
    ]


def test_havuz_eksi_sayi_gevsek_sekilde_numarali_notu_sayar(tmp_path):
    _kurallar(tmp_path, "eşikler (60, -60)\n")
    assert havuz_sorunlari(tmp_path, _havuz(tmp_path, ["gorsel-paket-60-x"])) == []


def test_havuz_hicbir_nota_gitmeyen_kisa_atif_yok_sayilir(tmp_path):
    _kurallar(tmp_path, "kaynak-zz G999 gp-998 T-yok gorsel-paket-997\n")
    assert havuz_sorunlari(tmp_path, _havuz(tmp_path, [])) == []


def test_pr_sablonu_yorumu_uc_metni_ve_tek_satiri_soyler():
    sablon = (KOK / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
    yorum = next(
        satir for satir in sablon.splitlines() if satir.startswith("<!-- CI accepts")
    )
    for metin in (
        '"Sonuç: geçti"',
        '"Sonuç: GEÇTİ"',
        '"Sonuç: NOTLU GEÇTİ"',
        '"Geçti"',
        "KALDI",
    ):
        assert metin in yorum
    assert re.search(r"exactly one Sonuç line", yorum)


def test_ci_aracleri_tam_surume_sabitli_ve_agents_bunu_soyler():
    ci = (KOK / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    araclar = re.findall(r"npx --yes (\S+)", ci)
    assert araclar
    assert all(re.fullmatch(r"@?[\w./-]+@\d+\.\d+\.\d+", arac) for arac in araclar)
    surumler = re.findall(r'node-version: "([^"]+)"', ci)
    assert surumler
    assert all(re.fullmatch(r"\d+\.\d+\.\d+", surum) for surum in surumler)
    agents = (KOK / "AGENTS.md").read_text(encoding="utf-8")
    assert (
        "A CI tool outside Python is pinned to an exact version in the workflow file."
        in agents
    )


def test_driftlint_yapilandirmasi_yalniz_scratch_ve_worktrees_i_dislar():
    yapilandirma = (KOK / ".driftlintrc.json").read_text(encoding="utf-8")
    assert re.fullmatch(
        r'\s*\{\s*"ignore":\s*\[\s*"\.scratch/\*\*"\s*,\s*"\.claude/worktrees/\*\*"\s*\]\s*\}\s*',
        yapilandirma,
    )


# Uzak depo adı origin'dir. Eski ad yalnız .scratch/ altında kalır; depo adı ve modül adı eşleşmez.
# Sözcük parçalı yazılır: bu dosya kendini bulmasın.
ESKI = "kay" + "nak"
ESKI_AD_DESENI = re.compile(
    rf"(?<![\w-]){ESKI}/master"
    rf"|\b(?:fetch|push|pull)(?: -\S+)* {ESKI}\b"
    rf"|-u {ESKI}\b"
    rf"|remotes/{ESKI}\b"
    rf"|remote add {ESKI}\b"
)


@pytest.mark.parametrize(
    ("satir", "eslesir"),
    [
        ("git fetch " + ESKI, True),
        ("git fetch -q " + ESKI, True),
        (ESKI + "/master", True),
        ("git push -q -u " + ESKI + " <dal>", True),
        ("git pull --ff-only " + ESKI + " master", True),
        ("refs/remotes/" + ESKI + "/x", True),
        ("git remote add " + ESKI + " url", True),
        ("zPfizer/tansu-" + ESKI, False),
        ("tansu/" + ESKI + ".py", False),
        ("tests/test_" + ESKI + ".py", False),
        (ESKI + "-a-b-12", False),
        ("`" + ESKI + "` modülü", False),
        ("veri " + ESKI + "ları", False),
        ("origin/master", False),
    ],
)
def test_eski_ad_deseni_yakin_kacirmalari_eslemez(satir, eslesir):
    assert bool(ESKI_AD_DESENI.search(satir)) is eslesir


def test_izlenen_dosyalar_uzak_depo_adini_eski_adla_yazmaz():
    cikti = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=KOK,
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout
    bulunan = []
    for goreli in cikti.split("\0"):
        if not goreli or goreli.startswith(".scratch/"):
            continue
        yol = KOK / goreli
        if not yol.is_file():
            continue
        veri = yol.read_bytes()
        if b"\0" in veri:
            continue
        try:
            satirlar = veri.decode("utf-8").splitlines()
        except UnicodeDecodeError as hata:
            pytest.fail(f"{goreli}: UTF-8 değil ({hata})")
        bulunan += [
            f"{goreli}:{no}"
            for no, satir in enumerate(satirlar, 1)
            if ESKI_AD_DESENI.search(satir)
        ]
    assert not bulunan, "\n".join(bulunan)
