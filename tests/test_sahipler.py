"""Sahip dosyaları testi (bilet 08): AGENTS.md "Belgeler ve sahipleri" tablosundaki her dosya taranır.

Depo yolları vardır (git'e girmeyen yerel dosyalar CI'da yoksa atlanır, yerelde denetlenir);
`TASARIM §` ve `KURALLAR §` atıfları var olan bölüme gider; beyin kaynak yolları
(`gorsel-paket-*`, `kaynak-*`, `tweet-*`, `assets/…`) beyin havuzunda vardır (beyin yoksa atlanır).
Çalışma çıktısı adları (`durum.txt`, `manifest.json`, `kartlar.jsonl`) yol sayılmaz: tablo onları içermez.
"""

import pytest

from atif_araclari import (
    BEYIN,
    HAVUZ,
    KOK,
    KOK_DOSYASI,
    atif_kirikleri,
    beyin_kirikleri,
    sahip_dosyalari,
    sahip_tablosu,
    yerel_kok_adi,
    yerel_kok_yok,
    yol_kirikleri,
)

TABLO = """# X
## Documents and owners (Belgeler ve sahipleri)

| File | Fact that the file owns |
|---|---|
| `a.md` | bir |
| brain (beyin): `kisisel/300-Projects/Tansu X Veri Havuzu/` (outside) | ham |
| `docs/kurallar/A-x.md` … `E-y.md` | okuma |
| `docs/taslak/` (yerel) | taslak |

Metin | `yok.md` | tablo dışı
## Sonraki
| `b.md` | tablo dışı |
"""


def test_tablo_yollari_ayiklanir(tmp_path):
    (tmp_path / "AGENTS.md").write_text(TABLO, encoding="utf-8")
    assert sahip_tablosu(tmp_path / "AGENTS.md") == (
        [
            "a.md",
            "docs/kurallar/A-x.md",
            "docs/kurallar/E-y.md",
            "docs/kurallar",
            "docs/taslak/",
        ],
        ["kisisel/300-Projects/Tansu X Veri Havuzu/"],
    )


DEPO_YOLLARI = sahip_tablosu(KOK / "AGENTS.md")[0]
# Yerel dosyalar (.gitignore kökleri) CI'da yoktur: her biri kendi testinde, yoksa adıyla atlanır.
YEREL_YOLLAR = [y for y in DEPO_YOLLARI if yerel_kok_adi(KOK, y)]
GIT_YOLLARI = [y for y in DEPO_YOLLARI if y not in YEREL_YOLLAR]


def _yerel_yoksa_atla(yol):
    kok_adi = yerel_kok_adi(KOK, yol)
    if not (KOK / kok_adi).exists():
        pytest.skip(f"{yol}: yerel dosya bu makinede yok ({kok_adi} git'te değil).")


def test_tablodaki_depo_yollari_var():
    depo, beyin = sahip_tablosu(KOK / "AGENTS.md")
    # Başlık ya da tablo biçimi değişirse ayrıştırma sessizce boşalmasın.
    assert "docs/TASARIM.md" in depo
    assert "docs/kurallar/A-yapi-bolge.md" in depo
    assert len(beyin) == 1
    assert [y for y in GIT_YOLLARI if not (KOK / y).exists()] == []


@pytest.mark.parametrize("yol", YEREL_YOLLAR)
def test_tablodaki_yerel_dosya_var(yol):
    _yerel_yoksa_atla(yol)
    assert (KOK / yol).exists()


def test_tablodaki_dosyalarin_ve_docs_agents_in_depo_yollari_var():
    # driftlint docs/agents/*.md dosyalarını bulmaz; ölü yol denetimi bu testle yapılır.
    dosyalar = sahip_dosyalari(KOK, GIT_YOLLARI + ["docs/agents"])
    assert any(y.parent.name == "agents" for y in dosyalar)
    assert yol_kirikleri(KOK, dosyalar) == []


@pytest.mark.parametrize("yol", YEREL_YOLLAR)
def test_tablodaki_yerel_dosyanin_depo_yollari_var(yol):
    _yerel_yoksa_atla(yol)
    assert yol_kirikleri(KOK, sahip_dosyalari(KOK, [yol])) == []


def test_yerel_kok_yalniz_kok_yoksa_atlar(tmp_path):
    (tmp_path / ".gitignore").write_text(
        "/docs/sorgu/\n/veri/\n*.pyc\n", encoding="utf-8"
    )
    assert yerel_kok_yok(tmp_path, "docs/sorgu/sonuc-3-4.md")  # kök yok: CI
    assert yerel_kok_yok(tmp_path, "veri/")
    assert not yerel_kok_yok(tmp_path, "docs/TASARIM.md")  # yerel kök değil
    (tmp_path / "docs" / "sorgu").mkdir(parents=True)
    assert not yerel_kok_yok(
        tmp_path, "docs/sorgu/olmayan.md"
    )  # kök var: eksik dosya hata


def _depo(kok):
    (kok / "tansu").mkdir()
    (kok / ".scratch").mkdir()
    (kok / "tansu" / "kayit.py").write_text("x", encoding="utf-8")
    (kok / "docs").mkdir()
    (kok / "docs" / "TASARIM.md").write_text("x", encoding="utf-8")
    (kok / "GLOSSARY.md").write_text("x", encoding="utf-8")
    (kok / ".gitignore").write_text("/docs/sorgu/\n/rapor/\n", encoding="utf-8")


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        (
            "`tansu/kayit.py` `tansu/kayit.py:42` `tansu/kayit.py::test_x` `tansu/kayit.py (açıklama)` "
            "`tansu/` `GLOSSARY.md` `TASARIM.md` `docs/TASARIM.md`",
            [],
        ),
        ("`tansu/olmayan_denetim.py`", ["not.md:1: tansu/olmayan_denetim.py"]),
        ("a\n`tansu/olmayan.py:7`", ["not.md:2: tansu/olmayan.py"]),
        (
            "`tests/test_yok.py` `docs/yok.md`",
            ["not.md:1: tests/test_yok.py", "not.md:1: docs/yok.md"],
        ),
        ("`KURALLAR.md`", ["not.md:1: KURALLAR.md"]),
        (
            "`tansu/*.py` `tests/test_<modül>.py` `docs/kurallar/A–E` `rapor/rapor-x.html`",
            [],
        ),
        ("`rapor/durum.txt` `veri/anlik/` `gunluk/x.log`", []),
        ("`durum.txt` `manifest.json` `kartlar.jsonl` `kaynak-x.md` `Levent`", []),
        (
            "`TODO.md` `GLOSSARY-MAP.md`",
            ["not.md:1: TODO.md", "not.md:1: GLOSSARY-MAP.md"],
        ),
        ("`docs/sorgu/sonuc-3-4.md`", []),  # yerel kök yok: CI
    ],
)
def test_depo_yolu_denetimi(tmp_path, metin, beklenen):
    _depo(tmp_path)
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    assert yol_kirikleri(tmp_path, [tmp_path / "not.md"]) == beklenen


def test_yerel_kok_varken_eksik_dosya_hatadir(tmp_path):
    _depo(tmp_path)
    (tmp_path / "docs" / "sorgu").mkdir()
    (tmp_path / "not.md").write_text("`docs/sorgu/olmayan.md`", encoding="utf-8")
    assert yol_kirikleri(tmp_path, [tmp_path / "not.md"]) == [
        "not.md:1: docs/sorgu/olmayan.md"
    ]


def test_tablodaki_dosyalarin_bolum_atiflari_var_olana_gider():
    assert atif_kirikleri(KOK, sahip_dosyalari(KOK, GIT_YOLLARI)) == []


@pytest.mark.parametrize("yol", YEREL_YOLLAR)
def test_tablodaki_yerel_dosyanin_bolum_atiflari_var_olana_gider(yol):
    _yerel_yoksa_atla(yol)
    assert atif_kirikleri(KOK, sahip_dosyalari(KOK, [yol])) == []


def test_tablodaki_dosyalarin_beyin_yollari_havuzda_var():
    if not HAVUZ.exists():
        pytest.skip("Evde beyin havuzu yok.")
    depo, beyin = sahip_tablosu(KOK / "AGENTS.md")
    assert [y for y in beyin if not (BEYIN / y).is_dir()] == []
    assert beyin_kirikleri(KOK, sahip_dosyalari(KOK, depo), HAVUZ) == []


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        (
            "`gorsel-paket-01` `gorsel-paket-01-ilk.md` `kaynak-a-b` `tweet-x-y.md` "
            "`assets/gorsel-paket-01/g.png` `assets/gorsel-paket-01` "
            + r"`assets\gorsel-paket-01\g.png`",
            [],
        ),
        (
            "`tweet-X` `gorsel-paket-NN-*.md` `kaynak-x-<no>` `assets/` "
            + r"`assets/gorsel-paket-01-...\g.png`",
            [],
        ),
        ("`durum.txt` `manifest.json` `kartlar.jsonl` `tansu/veri.py`", []),
        ("`gorsel-paket-02`", ["not.md:1: gorsel-paket-02"]),
        ("a\n`kaynak-a-c.md`", ["not.md:2: kaynak-a-c.md"]),
        ("`tweet-y`", ["not.md:1: tweet-y"]),
        ("`assets/gorsel-paket-09/g.png`", ["not.md:1: assets/gorsel-paket-09/g.png"]),
        # sondaki açıklama, satır eki ve parça şablon ya da yol sayılmaz; yalnız ad denetlenir
        ("`gorsel-paket-02 (NN numaralı not)`", ["not.md:1: gorsel-paket-02"]),
        ("`kaynak-a-c.md:12 <açıklama> *`", ["not.md:1: kaynak-a-c.md"]),
        # kesik kimlik not adı sayılmaz (ad başı yalnız tire sınırında)
        ("`kaynak-a-b-12`", ["not.md:1: kaynak-a-b-12"]),
        ("`kaynak-a-b-1`", ["not.md:1: kaynak-a-b-1"]),
        ("`gorsel-paket-0`", ["not.md:1: gorsel-paket-0"]),
        ("`gorsel-paket-011-x`", ["not.md:1: gorsel-paket-011-x"]),
        ("`tweet-x-`", ["not.md:1: tweet-x-"]),
        ("`tweet-y#bolum` `tweet-x-y.md:3` `kaynak-a-b (NN)`", ["not.md:1: tweet-y"]),
        (
            "`assets/gorsel-paket-01/yok.png`",
            ["not.md:1: assets/gorsel-paket-01/yok.png"],
        ),
        (
            r"`assets\gorsel-paket-09\g.png`",
            [r"not.md:1: assets\gorsel-paket-09\g.png"],
        ),
    ],
)
def test_kirik_beyin_yolu_yakalanir(tmp_path, metin, beklenen):
    havuz = tmp_path / "havuz"
    (havuz / "assets" / "gorsel-paket-01").mkdir(parents=True)
    (havuz / "assets" / "gorsel-paket-01" / "g.png").write_text("x", encoding="utf-8")
    for ad in ("gorsel-paket-01-ilk", "kaynak-a-b-123", "tweet-x-y"):
        (havuz / f"{ad}.md").write_text("n", encoding="utf-8")
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    assert beyin_kirikleri(tmp_path, [tmp_path / "not.md"], havuz) == beklenen


def test_taslak_dosyalar_beyin_denetimine_girmez(tmp_path):
    (tmp_path / "docs" / "strateji-taslak").mkdir(parents=True)
    taslak = tmp_path / "docs" / "strateji-taslak" / "t.md"
    taslak.write_text("`gorsel-paket-26`", encoding="utf-8")
    assert beyin_kirikleri(tmp_path, [taslak], tmp_path) == []


def _yaz(kok, goreli, metin):
    yol = kok / goreli
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(metin, encoding="utf-8")
    return yol


@pytest.mark.parametrize(
    ("goreli", "metin", "beklenen"),
    [
        # bağlı istisna: doğru dosya, doğru anış
        ("docs/agents/domain.md", "- `GLOSSARY.md` root (no `GLOSSARY-MAP.md`)", []),
        ("docs/sorgu/izleme/karar.md", "`.scratch/` yerine `TODO.md`", []),
        # başka dosyada aynı cümle istisna değildir
        ("docs/x.md", "no `GLOSSARY-MAP.md`", ["docs/x.md:1: GLOSSARY-MAP.md"]),
        ("docs/x.md", "yerine `TODO.md`", ["docs/x.md:1: TODO.md"]),
        # doğru dosya, başka anış
        (
            "docs/agents/domain.md",
            "- `GLOSSARY-MAP.md` root (no `GLOSSARY-MAP.md`)",
            ["docs/agents/domain.md:1: GLOSSARY-MAP.md"],
        ),
        (
            "docs/agents/domain.md",
            "- `TODO.md` root",
            ["docs/agents/domain.md:1: TODO.md"],
        ),
        ("docs/agents/domain.md", "no `TODO.md`", ["docs/agents/domain.md:1: TODO.md"]),
        # başka ada geçen istisna cümlesi
        (
            "CODING_STANDARDS.md",
            "the session review in `TODO.md`",
            ["CODING_STANDARDS.md:1: TODO.md"],
        ),
    ],
)
def test_ad_istisnasi_dosyaya_ve_anisa_baglidir(tmp_path, goreli, metin, beklenen):
    _depo(tmp_path)
    yol = _yaz(tmp_path, goreli, metin)
    assert yol_kirikleri(tmp_path, [yol]) == beklenen


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        (
            "`tansu/audit_missing.py (NN numaralı bölüm)`",
            ["docs/agents/y.md:1: tansu/audit_missing.py"],
        ),
        (
            "`tansu/audit_missing.py <açıklama> *` ve `tansu/…`",
            ["docs/agents/y.md:1: tansu/audit_missing.py"],
        ),
        ("`tansu/kayit.py (NN numaralı bölüm)` `tansu/kayit.py#5`", []),
        (r"`docs\AUDIT_MISSING.md`", ["docs/agents/y.md:1: docs/AUDIT_MISSING.md"]),
        (r"`docs\TASARIM.md` `tansu\kayit.py:3`", []),
        (r"`tansu\yok.py:3`", ["docs/agents/y.md:1: tansu/yok.py"]),
        (r"`C:\Users\x\docs\AUDIT_MISSING.md` `\|Z\|`", []),
        (
            "[x](../../docs/AUDIT_MISSING.md)",
            ["docs/agents/y.md:1: docs/AUDIT_MISSING.md"],
        ),
        (
            "[x](../TASARIM.md) [y](../TASARIM.md#5) [z](../TASARIM.md?a=1) [w](<../TASARIM.md>)",
            [],
        ),
        ('[x](../TASARIM.md "başlık")', []),
        ("[x](https://a/b) [y](mailto:a@b.c) [z](#bolum) [w](http://a/yok.md)", []),
        ("[x](../yok.md#5)", ["docs/agents/y.md:1: docs/yok.md"]),
        (r"[x](..\yok.md)", ["docs/agents/y.md:1: docs/yok.md"]),
        ("[x]: ../TASARIM.md\n[y]: ../yok.md", ["docs/agents/y.md:2: docs/yok.md"]),
        ("[x](../../../disarida.md)", ["docs/agents/y.md:1: ../../../disarida.md"]),
        ("![r](../yok.png)", ["docs/agents/y.md:1: docs/yok.png"]),
    ],
)
def test_yol_bicimleri_ve_baglantilar(tmp_path, metin, beklenen):
    _depo(tmp_path)
    yol = _yaz(tmp_path, "docs/agents/y.md", metin)
    assert yol_kirikleri(tmp_path, [yol]) == beklenen


def test_taslak_dosyalarin_baglantilari_taranmaz(tmp_path):
    _depo(tmp_path)
    yol = _yaz(tmp_path, "docs/strateji-taslak/x.md", "[a](../SETUP.html)")
    assert yol_kirikleri(tmp_path, [yol]) == []


@pytest.mark.parametrize(
    "kok_adi",
    [
        "tansu",
        "tests",
        "docs",
        ".github",
        "kurulum",
        "kayit",
        ".claude",
        ".scratch",
        "arsiv",
    ],
)
def test_her_depo_kokunde_olmayan_yol_yakalanir(tmp_path, kok_adi):
    _depo(tmp_path)
    (tmp_path / "not.md").write_text(f"`{kok_adi}/yok.x`", encoding="utf-8")
    assert yol_kirikleri(tmp_path, [tmp_path / "not.md"]) == [
        f"not.md:1: {kok_adi}/yok.x"
    ]


@pytest.mark.parametrize("isaret", ["<", "*", "…", "YYYY", "–", "NN"])
def test_her_sablon_isareti_yolu_atlatir_ama_yalniz_yolda(tmp_path, isaret):
    _depo(tmp_path)
    metin = f"`tansu/yok{isaret}.py` `tansu/yok2.py ({isaret})`"
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    assert yol_kirikleri(tmp_path, [tmp_path / "not.md"]) == ["not.md:1: tansu/yok2.py"]


@pytest.mark.parametrize(
    "ad",
    [
        "YOK.md",
        "YOK_BELGE.md",
        "YOK-BELGE.md",
        "pyproject.toml",
        "requirements.lock.txt",
    ],
)
def test_kok_dosyasi_adlari_taranir(tmp_path, ad):
    assert KOK_DOSYASI.fullmatch(ad)
    _depo(tmp_path)
    (tmp_path / "not.md").write_text(f"`{ad}`", encoding="utf-8")
    assert yol_kirikleri(tmp_path, [tmp_path / "not.md"]) == [f"not.md:1: {ad}"]


@pytest.mark.parametrize("ad", ["yok.md", "durum.txt", "setup.cfg", "Yok.md"])
def test_kok_dosyasi_desenine_uymayan_ad_yol_sayilmaz(tmp_path, ad):
    assert not KOK_DOSYASI.fullmatch(ad)
    _depo(tmp_path)
    (tmp_path / "not.md").write_text(f"`{ad}`", encoding="utf-8")
    assert yol_kirikleri(tmp_path, [tmp_path / "not.md"]) == []


def test_taslaklar_atif_ve_yol_denetimi_disindadir(tmp_path):
    # AGENTS.md: taslaklar kayma denetimi dışında (04c, 14.10); kod ve metin aynı şeyi söyler.
    _depo(tmp_path)
    (tmp_path / "docs" / "TASARIM.md").write_text("## 1. A\n", encoding="utf-8")
    (tmp_path / "docs" / "KURALLAR.md").write_text("## 1. A\n", encoding="utf-8")
    metin = "TASARIM §99 `tansu/yok.py` [x](yok.md)"
    taslak = _yaz(tmp_path, "docs/strateji-taslak/x.md", metin)
    taslak2 = _yaz(tmp_path, "docs/strateji-modulleri-taslak.md", metin)
    assert atif_kirikleri(tmp_path, [taslak, taslak2]) == []
    assert yol_kirikleri(tmp_path, [taslak, taslak2]) == []
    sade = _yaz(tmp_path, "docs/x.md", metin)  # taslak değilse aynı metin hatalıdır
    assert len(atif_kirikleri(tmp_path, [sade])) == 1
    assert len(yol_kirikleri(tmp_path, [sade])) == 2
