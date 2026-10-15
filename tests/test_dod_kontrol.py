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
- [x] Tansu: `## Tansu` maddeleri — kanıt: çıktı
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
        ("Sonuç: GEÇTİ", "Sonuç: kaldı", "Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik"),
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
        "Kural 5: ## Bağımsız inceleme bölümünde Denetçi: ve Sonuç: geçti ya da NOTLU GEÇTİ yok.",
        "Kural 6: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu yok.",
    ]


@pytest.mark.parametrize("karar", ["geçti", "GEÇTİ", "NOTLU GEÇTİ"])
def test_kural_5_kabul_edilen_kararlar(karar):
    assert hatalar(GECERLI.replace("Sonuç: GEÇTİ", "Sonuç: " + karar)) == []


@pytest.mark.parametrize(
    "karar",
    ["KALDI", "kaldı", "notlu geçti", "Notlu Geçti", "NOTLU", "Geçti", "NOTLU GEÇTI"],
)
def test_kural_5_reddedilen_kararlar(karar):
    assert hatalar(GECERLI.replace("Sonuç: GEÇTİ", "Sonuç: " + karar)) == [
        "Kural 5: ## Bağımsız inceleme bölümünde Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik."
    ]


TANSU_HATASI = "Tansu: satırı işaretli ve kanıtlı olmalı"
TANSU_SATIRI = "- [x] Tansu: `## Tansu` maddeleri — kanıt: çıktı\n"


@pytest.mark.parametrize(
    ("yeni", "ayrinti"),
    [
        ("- [x] Belgeleme — kanıt: çıktı\n", TANSU_HATASI),
        (
            "- [x] Tansu: `## Tansu` maddeleri — kanıt: \n",
            "kanıt eksik; satır: 13; " + TANSU_HATASI,
        ),
        ("- [x] Tansu `## Tansu` maddeleri — kanıt: çıktı\n", TANSU_HATASI),
    ],
)
def test_kural_4_tansu_satiri_isaretli_ve_kanitli(yeni, ayrinti):
    assert hatalar(GECERLI.replace(TANSU_SATIRI, yeni)) == [
        "Kural 4: ## Definition of Done bölümünde " + ayrinti + "."
    ]


def test_kural_4_tansu_satiri_isaretsiz():
    govde = GECERLI.replace(
        TANSU_SATIRI, "- [ ] Tansu: `## Tansu` maddeleri — kanıt: çıktı\n"
    )
    assert hatalar(govde) == [
        "Kural 2: işaretsiz kutu var; satır: 13.",
        "Kural 4: ## Definition of Done bölümünde en az 10 işaretli satır olmalı; "
        + TANSU_HATASI
        + ".",
    ]


@pytest.mark.parametrize(
    "ek",
    [
        "Sonuç: KALDI\nSonuç: GEÇTİ",
        "Sonuç: kaldı\nSonuç: geçti",
        "Sonuç: GEÇTİ\nSonuç: GEÇTİ",
        "Sonuç: GEÇTİ\n  Sonuç: NOTLU GEÇTİ",
        "Sonuç: GEÇTİ\nSonuç:",
    ],
)
def test_kural_5_sonuc_satiri_tek_olmali(ek):
    govde = GECERLI.replace("Sonuç: GEÇTİ", ek)
    assert hatalar(govde) == [
        "Kural 5: ## Bağımsız inceleme bölümünde Sonuç: satırı tek olmalı ("
        + str(len(ek.splitlines()))
        + " satır var)."
    ]


def test_kural_5_sonuc_sablon_yorumu_satir_sayilmaz():
    yorum = '<!-- CI accepts only the exact text "Sonuç: geçti". -->\n'
    govde = GECERLI.replace("Sonuç: GEÇTİ", yorum + "Sonuç: GEÇTİ")
    assert hatalar(govde) == []
