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
    atif_kirikleri,
    beyin_kirikleri,
    sahip_dosyalari,
    sahip_tablosu,
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


def test_tablodaki_depo_yollari_var():
    depo, _ = sahip_tablosu(KOK / "AGENTS.md")
    eksik = [y for y in depo if not (KOK / y).exists() and not yerel_kok_yok(KOK, y)]
    assert eksik == []


def test_tablodaki_dosyalarin_ve_docs_agents_in_depo_yollari_var():
    # driftlint docs/agents/*.md dosyalarını bulmaz; ölü yol denetimi bu testle yapılır.
    depo, _ = sahip_tablosu(KOK / "AGENTS.md")
    dosyalar = sahip_dosyalari(KOK, depo + ["docs/agents"])
    assert any(y.parent.name == "agents" for y in dosyalar)
    assert yol_kirikleri(KOK, dosyalar) == []


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
            "`AKIS.md` `TODO.md` `GLOSSARY-MAP.md`",
            ["not.md:1: AKIS.md", "not.md:1: TODO.md", "not.md:1: GLOSSARY-MAP.md"],
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
    depo, _ = sahip_tablosu(KOK / "AGENTS.md")
    assert atif_kirikleri(KOK, sahip_dosyalari(KOK, depo)) == []


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
        ("CODING_STANDARDS.md", "the session review in `AKIS.md` (flows)", []),
        ("docs/agents/domain.md", "- `GLOSSARY.md` root (no `GLOSSARY-MAP.md`)", []),
        ("docs/sorgu/izleme/karar.md", "`.scratch/` yerine `TODO.md`", []),
        # başka dosyada aynı cümle istisna değildir
        ("docs/x.md", "the session review in `AKIS.md`", ["docs/x.md:1: AKIS.md"]),
        ("docs/x.md", "no `GLOSSARY-MAP.md`", ["docs/x.md:1: GLOSSARY-MAP.md"]),
        ("docs/x.md", "yerine `TODO.md`", ["docs/x.md:1: TODO.md"]),
        # doğru dosya, başka anış
        ("CODING_STANDARDS.md", "bkz `AKIS.md`", ["CODING_STANDARDS.md:1: AKIS.md"]),
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
