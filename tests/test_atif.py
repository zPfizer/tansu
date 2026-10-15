"""Atıf testi (bilet 08): belge ve koddaki atıflar var olan bir bölüme ya da karara gider.

Bölüm atıfları (`TASARIM 5.1`, `TASARIM §5.1`, `KURALLAR §3`) docs/TASARIM.md ve docs/KURALLAR.md
başlıklarına bakar. Karar etiketleri (İ:, B-, C-, S2-) yerel docs/sorgu/ klasörüne bakar; klasör
git'te olmadığı için CI'da etiket testi atlanır, yerel test kapısı denetler.
"""

import pytest

from atif_araclari import (
    KOK,
    atif_kirikleri,
    bolum_numaralari,
    etiket_kirikleri,
    izlenen_dosyalar,
)


def test_bolum_atiflari_var_olan_basliga_gider():
    assert atif_kirikleri(KOK, izlenen_dosyalar(KOK)) == []


def test_tarama_kumesi_bilinen_dosyalari_icerir():
    adlar = {yol.relative_to(KOK).as_posix() for yol in izlenen_dosyalar(KOK)}
    assert {
        "docs/TASARIM.md",
        "docs/KURALLAR.md",
        "AGENTS.md",
        "CLAUDE.md",
        "GLOSSARY.md",
        "tansu/kayit.py",
        ".claude/skills/tansu-grill/SKILL.md",
        ".github/pull_request_template.md",
    } <= adlar
    # .scratch tarihsel metindir (biletler, arşiv); bilerek dışarıda
    assert not any(ad.startswith(".scratch/") for ad in adlar)


def test_karar_etiketleri_sorguda_tanimli():
    sorgu = KOK / "docs" / "sorgu"
    if not sorgu.exists():
        pytest.skip("docs/sorgu yok (yerel dosya, git'te değil).")
    assert etiket_kirikleri(KOK, izlenen_dosyalar(KOK), sorgu) == []


def _belgeler(kok):
    docs = kok / "docs"
    docs.mkdir()
    (docs / "TASARIM.md").write_text(
        "## 5. Sınama\n### 5.1 Veri\nHash\nkapsamı burada.\n### 5.2 Kural kaydı\ngövde\n"
        "```\n# kod yorumu başlık değil\n```\nfence-sonrası terim\n"
        "## 6. Günlük\n1. bir terim\n2. iki\n"
        "## 8. Açık\n1. a\n2. b\n## Ek A: Eleştiri\nKüçükler burada\n",
        encoding="utf-8",
    )
    (docs / "KURALLAR.md").write_text(
        "## 1. Ana bulgular\n1. a\n2. b\n", encoding="utf-8"
    )
    return docs


def test_bolum_numaralari_baslik_ve_madde(tmp_path):
    # Alt başlığı olan bölümde madde sayılmaz; alt başlığı olmayan bölümde madde numarası sayılır.
    yol = tmp_path / "ornek.md"
    yol.write_text(
        "## 5. A\n### 5.1 B\n1. a\n2. b\n## 6. C\n1. bir\n2. iki\n", encoding="utf-8"
    )
    assert bolum_numaralari(yol) == {"5", "5.1", "6", "6.1", "6.2"}


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        ("TASARIM 5.1 ve TASARIM §6 ve TASARIM 6.2 ve KURALLAR §1", []),
        ("TASARIM 9 yok", ["not.md:1: TASARIM 9"]),
        ("a\nTASARIM §5.7 yok", ["not.md:2: TASARIM §5.7"]),
        ("TASARIM 6.3 madde yok", ["not.md:1: TASARIM 6.3"]),
        ("KURALLAR §5.1 yok", ["not.md:1: KURALLAR §5.1"]),
        ("TASARIM §5.1, §99", ["not.md:1: TASARIM §99"]),
        # `ve n` ve `/n` düz sayı listeleri; sayıdan sonra sözcük gelirse nesnedir, atıf değil
        ("TASARIM 5 ve 99", ["not.md:1: TASARIM §99"]),
        ("TASARIM 5/99", ["not.md:1: TASARIM §99"]),
        ("TASARIM 5 ve 99 ve 98)", ["not.md:1: TASARIM §99", "not.md:1: TASARIM §98"]),
        ("TASARIM 5 ve 6.", []),
        ("TASARIM 5/6;", []),
        ("TASARIM 5.1 ve 99 gün", []),
        ("TASARIM 5.1 / 99 gün", []),
        ("TASARIM 5.1, 99 gün", []),
        ("TASARIM 5 ve 99 ile", []),
        # `madde N`: bölümün N. maddesi
        ("KURALLAR §1 madde 2; TASARIM §6 madde 1; TASARIM 8 madde 2", []),
        ("TASARIM 6 madde 99", ["not.md:1: TASARIM §6.99"]),
        ("KURALLAR §1 madde 9", ["not.md:1: KURALLAR §1.9"]),
        ("a\nKURALLAR §1\n  madde 9", ["not.md:2: KURALLAR §1.9"]),
        ("TASARIM §99 madde 1", ["not.md:1: TASARIM §99", "not.md:1: TASARIM §99.1"]),
        ("TASARIM §5.1, 6 madde 2 ve KURALLAR §1 madde 3", ["not.md:1: KURALLAR §1.3"]),
        (
            "TASARIM 5.1, 5.99 ve §98",
            ["not.md:1: TASARIM §5.99", "not.md:1: TASARIM §98"],
        ),
        ("TASARIM §5.1–5.99", ["not.md:1: TASARIM §5.99"]),
        ("TASARIM §5.99–5.1", ["not.md:1: TASARIM §5.99"]),
        ("TASARIM 5.1/5.99", ["not.md:1: TASARIM §5.99"]),
        ("KURALLAR §1 ve §9", ["not.md:1: KURALLAR §9"]),
        ("TASARIM.md §99", ["not.md:1: TASARIM.md §99"]),
        ("`docs/TASARIM.md` §99", ["not.md:1: TASARIM.md` §99"]),
        ("`docs/KURALLAR.md` §5.1", ["not.md:1: KURALLAR.md` §5.1"]),
        ("TASARIM §5.1–5.2, §6 ve 5.1 / 5.2 ve `TASARIM.md` §6", []),
        ("TASARIM 5.1, 6 gün ve TASARIM 5.2 - 3 gün", []),
        ('TASARIM 8 "Küçükler"', ['not.md:1: TASARIM 8 "Küçükler" bölümde yok']),
        ('TASARIM 8.2 "Küçükler"', ['not.md:1: TASARIM 8.2 "Küçükler" bölümde yok']),
        ('TASARIM 8 "açık"', []),
        ('TASARIM 5.2 "fence-sonrası terim"', []),
    ],
)
def test_kirik_bolum_atifi_yakalanir(tmp_path, metin, beklenen):
    _belgeler(tmp_path)
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    assert atif_kirikleri(tmp_path, [tmp_path / "not.md"]) == beklenen


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        ('TASARIM 5.1 "Hash kapsamı" ve TASARIM §5.2 “Kural kaydı”', []),
        (
            'TASARIM 5.2 ‘kural KAYDI’ ve TASARIM 5.2: **Kural kaydı** ve TASARIM 5.1 ("Veri")',
            [],
        ),
        ('TASARIM 5 "Hash kapsamı" (üst bölüm alt bölümü içerir)', []),
        ('TASARIM 5.1, "Hash kapsamı" ve "Hash kapsamı"', []),
        ('TASARIM 6.1 "bir terim"', []),
        (
            'TASARIM 5.2 "Hash kapsamı"',
            ['not.md:1: TASARIM 5.2 "Hash kapsamı" bölümde yok'],
        ),
        (
            "a\nTASARIM §5.2 “Hash kapsamı”",
            ['not.md:2: TASARIM §5.2 "Hash kapsamı" bölümde yok'],
        ),
        (
            "TASARIM 5.1 ve ‘Kural kaydı’",
            ['not.md:1: TASARIM 5.1 "Kural kaydı" bölümde yok'],
        ),
        (
            "TASARIM 5.1 **Kural kaydı**",
            ['not.md:1: TASARIM 5.1 "Kural kaydı" bölümde yok'],
        ),
        (
            'TASARIM 5.2 ("Hash kapsamı")',
            ['not.md:1: TASARIM 5.2 "Hash kapsamı" bölümde yok'],
        ),
        ('TASARIM 6.2 "bir terim"', ['not.md:1: TASARIM 6.2 "bir terim" bölümde yok']),
        ('TASARIM 9 "Veri"', ["not.md:1: TASARIM 9"]),
    ],
)
def test_atiftan_sonraki_alinti_atif_yapilan_bolumde_aranir(tmp_path, metin, beklenen):
    _belgeler(tmp_path)
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    assert atif_kirikleri(tmp_path, [tmp_path / "not.md"]) == beklenen


def _sorgu(kok):
    sorgu = kok / "sorgu"
    (sorgu / "sorgu-3").mkdir(parents=True)
    (sorgu / "sonuc-3-4.md").write_text(
        "## A. Olgular\n1. olgu\n## B. Kararlar\n1. **bir**\n2. iki\n"
        "## C. Altyapı\n1. **bir**\n## D. Levent\n1. x\n",
        encoding="utf-8",
    )
    (sorgu / "sorgu-2.md").write_text("1. **soru**\n7. soru\n", encoding="utf-8")
    (sorgu / "sorgu-3" / "sorular-08-x.md").write_text(
        "08-027. soru\n**08-028** soru\n", encoding="utf-8"
    )
    return sorgu


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        ("(B-2, C-1, S2-7, İ: 08-027, 08-028) B-n C-n B-momentum", []),
        ("B-3 yok", ["not.md:1: B-3"]),
        ("C-2 yok; A-1 etiket sayılmaz; B-1 var", ["not.md:1: C-2"]),
        ("S2-8 yok", ["not.md:1: S2-8"]),
        ("(İ: 08-027, 08-999)", ["not.md:1: İ:08-999"]),
        ("(İ: 08-027,\n  09-001)", ["not.md:2: İ:09-001"]),
    ],
)
def test_kirik_karar_etiketi_yakalanir(tmp_path, metin, beklenen):
    sorgu = _sorgu(tmp_path)
    (tmp_path / "not.md").write_text(metin, encoding="utf-8")
    assert etiket_kirikleri(tmp_path, [tmp_path / "not.md"], sorgu) == beklenen
