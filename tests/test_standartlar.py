import ast
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def test_modul_bagimliliklari_tek_yonlu_geri_import_yok():
    # TASARIM 4: bağımlılık sırasındaki modüller yalnız önceki katmanları ithal eder.
    katmanlar = (
        ("kaynak",),
        ("veri",),
        ("evren", "gostergeler"),
        ("katalog",),
        ("aileler", "cift"),
        ("motor",),
        ("simulator",),
        ("ciftbolme",),
        ("istatistik",),
        ("saglamlik",),
        ("rapor",),
        ("kayit",),
        ("gunluk", "denetim"),
        ("__main__",),
    )
    sira = {ad: i for i, katman in enumerate(katmanlar) for ad in katman}
    kok = Path(__file__).resolve().parents[1] / "tansu"
    for ad in sira:
        agac = ast.parse((kok / f"{ad}.py").read_text(encoding="utf-8"))
        for dugum in ast.walk(agac):
            hedefler = []
            if isinstance(dugum, ast.ImportFrom):
                if dugum.module == "tansu" or (dugum.level == 1 and not dugum.module):
                    hedefler = [n.name for n in dugum.names]
                elif (dugum.module or "").startswith("tansu."):
                    hedefler = [dugum.module.split(".")[1]]
                elif dugum.level == 1 and dugum.module:
                    hedefler = [dugum.module.split(".")[0]]
            elif isinstance(dugum, ast.Import):
                hedefler = [
                    n.name.split(".")[1]
                    for n in dugum.names
                    if n.name.startswith("tansu.")
                ]
            for hedef in hedefler:
                if hedef in sira:
                    assert sira[hedef] < sira[ad], (ad, hedef, dugum.lineno)


def _bolum(yol, baslik):
    # Başlık satırından sonraki `## ` başlığa kadar olan satırlar (başlık satırı dahil).
    satirlar = (KOK / yol).read_text(encoding="utf-8").splitlines()
    ilk = next(i for i, s in enumerate(satirlar) if s.startswith(baslik))
    son = next(
        (i for i in range(ilk + 1, len(satirlar)) if satirlar[i].startswith("## ")),
        len(satirlar),
    )
    return satirlar[ilk:son]


def test_dizin_kaynak_degerini_yinelemez():
    # KURALLAR 2: "bu dizin kaynak değerini yinelemez"; parametre değeri A–E bölümünde durur.
    desen = re.compile(
        r"\b\d+ ?(?:bar|günlük|haftalık|aylık|yıllık)\b|\d+(?:[.,]\d+)? ?ATR\b"
    )
    bulunan = [
        satir
        for satir in _bolum("docs/KURALLAR.md", "## 2. Dizin")
        if desen.search(satir)
    ]
    assert bulunan == []


def test_coding_standards_atif_ve_tansu_kurallari():
    # Karar S1 (Levent 17.10): genel kurallar ortak dosyada durur; bu dosya yalnız Tansu kurallarını taşır.
    metin = (KOK / "CODING_STANDARDS.md").read_text(encoding="utf-8")
    eski = [
        s
        for s in metin.splitlines()
        if s.startswith(("## Rules", "## Mistakes", "## Seen once"))
    ]
    assert eski == []
    assert "kod-standartlari-genel.md" in metin
    tansu = "\n".join(_bolum("CODING_STANDARDS.md", "## Tansu"))
    assert "Read the whole note" in tansu
    assert "Define the boundary before the code" in tansu


def test_settings_deny_okuma_kabuklarini_engeller():
    ayar = json.loads((KOK / ".claude" / "settings.json").read_text(encoding="utf-8"))
    deny = ayar["permissions"]["deny"]
    for kural in ("Bash(cat *)", "Bash(sed -n*)", "Bash(sed -i*)"):
        assert kural in deny


def test_okuyucu_araclari_yalniz_okur():
    metin = (KOK / ".claude" / "agents" / "okuyucu.md").read_text(encoding="utf-8")
    araclar = [s for s in metin.splitlines() if s.startswith("tools:")]
    assert araclar == ["tools: Read, Grep, Glob"]
