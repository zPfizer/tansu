import ast
from pathlib import Path

import pytest


def _satirlar(yol):
    return yol.read_text(encoding="utf-8").splitlines()


def _genel_standart_basta(ad):
    kaynak = Path.home() / "Desktop" / "YONETIM" / ad
    if not kaynak.exists():
        pytest.skip(f"Evde {ad} yok.")
    genel = _satirlar(kaynak)
    kopya = _satirlar(Path(__file__).resolve().parents[1] / ad)
    assert kopya[: len(genel)] == genel
    ek = kopya[len(genel) :]
    assert ek == [] or (ek[0] == "" and ek[1] == "## Tansu")


def test_kodlama_standartlari_genel_standartla_baslar():
    _genel_standart_basta("CODING_STANDARDS.md")


def test_bitis_olcutleri_genel_standartla_baslar():
    _genel_standart_basta("DEFINITION_OF_DONE.md")


def test_modul_bagimliliklari_tek_yonlu_geri_import_yok():
    # TASARIM 4: bağımlılık sırasındaki modüller yalnız önceki katmanları ithal eder.
    katmanlar = (
        ("kaynak",),
        ("veri",),
        ("evren", "gostergeler"),
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
