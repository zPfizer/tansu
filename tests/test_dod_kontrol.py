import importlib.util
from pathlib import Path

import pytest


_yol = Path(__file__).resolve().parents[1] / ".github" / "dod_kontrol.py"
_tanim = importlib.util.spec_from_file_location("dod_kontrol", _yol)
_modul = importlib.util.module_from_spec(_tanim)
_tanim.loader.exec_module(_modul)
hatalar = _modul.hatalar

GECERLI = """## Kabul ölçütleri (Levent kontrol eder)
- [X] İstenen davranış sağlandı.
## Definition of Done
- [x] Doğruluk — kanıt: çıktı
- [x] Gerçek veri — kanıt: çıktı
- [x] Yeni test — kanıt: çıktı
- [x] Eski testler — kanıt: çıktı
- [x] Kenar durumlar — kanıt: çıktı
- [x] Adlar — kanıt: çıktı
- [x] Ölü kod — kanıt: çıktı
- [x] Kalite — kanıt: çıktı
- [x] Entegrasyon — kanıt: çıktı
- [x] Belgeleme — kanıt: çıktı
## Bağımsız inceleme
Denetçi: Ayşe
Sonuç: GEÇTİ
## Gerçek veri kanıtı
```text
Gerçek koşu çıktısı
```
"""


def test_gecerli():
    assert hatalar(GECERLI.replace("\n", "\r\n")) == []


@pytest.mark.parametrize(
    "baslik",
    [
        "## Kabul ölçütleri (Levent kontrol eder)",
        "## Definition of Done",
        "## Bağımsız inceleme",
        "## Gerçek veri kanıtı",
    ],
)
def test_kural_1_baslik_eksik(baslik):
    assert hatalar(GECERLI.replace(baslik + "\n", "")) == [
        "Kural 1: eksik başlıklar: " + baslik.split(" (")[0] + "."
    ]


def test_kural_2_isaretsiz_kutu():
    assert hatalar(GECERLI + "  - [ ] Bekliyor\n") == [
        "Kural 2: işaretsiz kutu var; satır: 21."
    ]


def test_kural_3_kabul_kutusu_yok():
    assert hatalar(GECERLI.replace("- [X] İstenen", "İstenen")) == [
        "Kural 3: ## Kabul ölçütleri bölümünde en az bir işaretli kutu olmalı."
    ]


@pytest.mark.parametrize(
    ("eski", "yeni", "ayrinti"),
    [
        ("kanıt: çıktı", "kanıt: ", "kanıt eksik; satır: 4"),
        ("- [x] Doğruluk — kanıt: çıktı\n", "", "en az 10 işaretli satır olmalı"),
    ],
)
def test_kural_4_dod_eksik(eski, yeni, ayrinti):
    assert hatalar(GECERLI.replace(eski, yeni, 1)) == [
        "Kural 4: ## Definition of Done bölümünde " + ayrinti + "."
    ]


@pytest.mark.parametrize(
    ("eski", "yeni", "ayrinti"),
    [
        ("Denetçi: Ayşe", "Denetçi: ", "Denetçi: alanı boş veya eksik"),
        ("Sonuç: GEÇTİ", "Sonuç: kaldı", "Sonuç: geçti satırı eksik"),
    ],
)
def test_kural_5_inceleme_eksik(eski, yeni, ayrinti):
    assert hatalar(GECERLI.replace(eski, yeni)) == [
        "Kural 5: ## Bağımsız inceleme bölümünde " + ayrinti + "."
    ]


@pytest.mark.parametrize("kod", ["```\n\n```", "Gerçek koşu çıktısı", "```\nçıktı"])
def test_kural_6_kod_kaniti_yok(kod):
    govde = GECERLI.replace("```text\nGerçek koşu çıktısı\n```", kod)
    assert hatalar(govde) == [
        "Kural 6: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu olmalı."
    ]


@pytest.mark.parametrize("govde", [None, "", " \r\n "])
def test_bos_govde(govde):
    assert hatalar(govde) == [
        "Kural 1: gövde boş; gerekli dört başlık yok.",
        "Kural 2: gövde boş; işaretsiz kutu kontrolü yapılamadı.",
        "Kural 3: ## Kabul ölçütleri bölümünde işaretli kutu yok.",
        "Kural 4: ## Definition of Done bölümünde 10 kanıtlı işaretli satır yok.",
        "Kural 5: ## Bağımsız inceleme bölümünde Denetçi: ve Sonuç: geçti yok.",
        "Kural 6: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu yok.",
    ]
