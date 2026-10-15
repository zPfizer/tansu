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
    yerel_mi,
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
    eksik = [y for y in depo if not (KOK / y).exists() and not yerel_mi(KOK, y)]
    assert eksik == []


def test_yerel_yol_ile_yazim_hatasi_ayrilir(tmp_path):
    assert yerel_mi(KOK, "docs/sorgu/sonuc-3-4.md")
    assert not yerel_mi(KOK, "docs/TASARIM.md")
    assert not yerel_mi(
        tmp_path, "docs/sorgu/sonuc-3-4.md"
    )  # git deposu değil: yerel sayılmaz


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
