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
Denetçi kararı (aynen): GEÇTİ, bulgu yok.
Yanlış iddia sayısı: 0
İkinci geçiş: yok
Bulgu sayısı: 0
Sonuç: GEÇTİ
## Gerçek veri kanıtı
```text
Gerçek koşu çıktısı
```
kapi: pytest -> 0
kapi: ruff check -> 0
kapi: ruff format -> 0
kapi: git diff --check -> 0
kapi: driftlint -> 0
kapi: HEAD 0123456789abcdef0123456789abcdef01234567 temiz
Akış: tansu-yeni-is
Çağrılan beceriler: tansu-yeni-is, verification-before-completion, mattpocock-skills:pr, mattpocock-skills:code-review
Denetlenen commit: 0123456789abcdef0123456789abcdef01234567
## Risk
Küçük risk.
## Nasıl geri alınır
PR geri alınır.
## Bulgu yanıtları
bulgu yok
## Açık sorular
yok
"""
SHA = "0123456789abcdef0123456789abcdef01234567"
SHA_BASKA = "fedcba9876543210fedcba9876543210fedcba98"
BECERI_SATIRI = (
    "Çağrılan beceriler: tansu-yeni-is, verification-before-completion, "
    "mattpocock-skills:pr, mattpocock-skills:code-review\n"
)
TUM_BECERILER = (
    "verification-before-completion, mattpocock-skills:pr, "
    "mattpocock-skills:code-review, mattpocock-skills:writing-for-agents, "
    "mattpocock-skills:domain-modeling, asd-ste100"
)
KARAR_SATIRI = "Denetçi kararı (aynen): GEÇTİ, bulgu yok.\n"
AKIS_SATIRI = "Akış: tansu-yeni-is\n"
AKIS_HATASI = (
    "Kural 7: PR gövdesinde Akış: <ad> satırı olmalı; "
    "<ad> tansu-yeni-is, tansu-hata, tansu-belge, tansu-karar ya da tansu-eval olmalı."
)


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
    assert hatalar(
        GECERLI.replace(AKIS_SATIRI, "  - [ ] Bekliyor\n" + AKIS_SATIRI)
    ) == ["Kural 2: işaretsiz kutu var; satır: 31."]


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
        "Kural 8: gövde boş; Çağrılan beceriler: satırı yok.",
        "Kural 9: gövde boş; ## Bağımsız inceleme bölümünde Denetçi kararı (aynen):, "
        "Yanlış iddia sayısı: ve İkinci geçiş: satırı yok.",
        "Kural 10: gövde boş; ## Gerçek veri kanıtı bölümünde kapi: satırları yok.",
    ]


@pytest.mark.parametrize("karar", ["geçti", "GEÇTİ", "NOTLU GEÇTİ"])
def test_kural_5_kabul_edilen_kararlar(karar):
    govde = GECERLI.replace("Sonuç: GEÇTİ", "Sonuç: " + karar)
    govde = govde.replace("(aynen): GEÇTİ", "(aynen): " + karar)
    assert hatalar(govde) == []


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
        "Kural 5: ## Bağımsız inceleme bölümünde Sonuç: satırı tek olmalı (2 satır var)."
    ]


@pytest.mark.parametrize(
    "ad",
    ["tansu-yeni-is", "tansu-hata", "tansu-belge", "tansu-karar", "tansu-eval"],
)
@pytest.mark.parametrize("sarmal", ["{}", "`{}`"])
def test_kural_7_akis_adi_kabul_edilir(ad, sarmal):
    satir = "Akış: " + sarmal.format(ad) + "\n"
    govde = GECERLI.replace(AKIS_SATIRI, satir)
    govde = govde.replace(BECERI_SATIRI, f"Çağrılan beceriler: {ad}, {TUM_BECERILER}\n")
    assert hatalar(govde) == []


@pytest.mark.parametrize(
    "yeni",
    [
        "",
        "Akış: \n",
        "Akış:\n",
        "Akış: tansu-bilinmeyen\n",
        "Akış: yeni-is\n",
        "Akış: `tansu-yeni-is\n",
        "Akış: tansu-yeni-is tansu-hata\n",
        "Akış: tansu-yeni-is, tansu-hata\n",
        "Akis: tansu-yeni-is\n",
    ],
)
def test_kural_7_akis_satiri_eksik_ya_da_yanlis(yeni):
    assert hatalar(GECERLI.replace(AKIS_SATIRI, yeni)) == [AKIS_HATASI]


@pytest.mark.parametrize(
    "ek",
    [
        "Akış: tansu-hata\n",
        "Akış: tansu-bilinmeyen\n",
    ],
)
def test_kural_7_ikinci_akis_satiri_reddedilir(ek):
    assert hatalar(GECERLI + ek) == [AKIS_HATASI]


def test_kural_5_sonuc_sablon_yorumu_satir_sayilmaz():
    yorum = '<!-- CI accepts only the exact text "Sonuç: geçti". -->\n'
    govde = GECERLI.replace("Sonuç: GEÇTİ", yorum + "Sonuç: GEÇTİ")
    assert hatalar(govde) == []


R8_TEK = "Kural 8: PR gövdesinde Çağrılan beceriler: satırı tek olmalı ({} satır var)."
R8_BOS = "Kural 8: Çağrılan beceriler: listesi boş."
R8_EKSIK = "Kural 8: Çağrılan beceriler: listesinde eksik: {}."
ORTAK = "verification-before-completion, mattpocock-skills:pr, mattpocock-skills:code-review"
BELGE_EK = "mattpocock-skills:writing-for-agents, mattpocock-skills:domain-modeling, asd-ste100"


def _akis(ad, beceriler):
    govde = GECERLI.replace(AKIS_SATIRI, f"Akış: {ad}\n")
    return govde.replace(BECERI_SATIRI, f"Çağrılan beceriler: {beceriler}\n")


@pytest.mark.parametrize(
    ("ad", "beceriler", "beklenen"),
    [
        ("tansu-karar", "tansu-karar", []),
        ("tansu-eval", "tansu-eval", []),
        ("tansu-eval", "baska", [R8_EKSIK.format("tansu-eval")]),
        ("tansu-yeni-is", "tansu-yeni-is", [R8_EKSIK.format(ORTAK)]),
        ("tansu-hata", "tansu-hata, " + ORTAK, []),
        ("tansu-hata", "tansu-hata", [R8_EKSIK.format(ORTAK)]),
        ("tansu-yeni-is", "`tansu-yeni-is` , `" + ORTAK.replace(", ", "`,`") + "`", []),
        (
            "tansu-yeni-is",
            "tansu-yeni-is, mattpocock-skills:pr",
            [
                R8_EKSIK.format(
                    "verification-before-completion, mattpocock-skills:code-review"
                )
            ],
        ),
        ("tansu-belge", f"tansu-belge, {ORTAK}", [R8_EKSIK.format(BELGE_EK)]),
        ("tansu-belge", f"tansu-belge, {ORTAK}, {BELGE_EK}", []),
        ("tansu-belge", f"tansu-belge, {ORTAK}, toplu havuz okuma", []),
        (
            "tansu-belge",
            "toplu havuz okuma",
            [R8_EKSIK.format("tansu-belge, " + ORTAK)],
        ),
        ("tansu-yeni-is", "tansu-yeni-is, " + ORTAK + ", toplu havuz okuma", []),
    ],
)
def test_kural_8_beceri_listesi(ad, beceriler, beklenen):
    assert hatalar(_akis(ad, beceriler)) == beklenen


@pytest.mark.parametrize("beceriler", ["", " ", ",", " , ,", "``"])
def test_kural_8_liste_bos(beceriler):
    govde = GECERLI.replace(BECERI_SATIRI, f"Çağrılan beceriler:{beceriler}\n")
    assert hatalar(govde) == [R8_BOS]


def test_kural_8_satir_yok_ya_da_cift():
    assert hatalar(GECERLI.replace(BECERI_SATIRI, "")) == [R8_TEK.format(0)]
    assert hatalar(GECERLI + BECERI_SATIRI) == [R8_TEK.format(2)]


def test_kural_8_gecersiz_akista_yalniz_satir_ve_bos_kontrolu():
    govde = GECERLI.replace(AKIS_SATIRI, "Akış: yok\n")
    assert hatalar(govde) == [AKIS_HATASI]
    govde = govde.replace(BECERI_SATIRI, "Çağrılan beceriler:\n")
    assert hatalar(govde) == [AKIS_HATASI, R8_BOS]


R9 = "Kural 9: ## Bağımsız inceleme bölümünde {}."


@pytest.mark.parametrize(
    ("yeni", "ayrinti"),
    [
        ("GEÇTİ, KALDI olabilir.", "Denetçi kararı KALDI içeriyor"),
        ("GEÇTİ, kaldı gibi.", "Denetçi kararı KALDI içeriyor"),
        ("GEÇTİ", None),
        ("geçti, bulgu yok.", None),
        ("bulgu yok.", "Denetçi kararında GEÇTİ ya da NOTLU GEÇTİ sözcüğü yok"),
        (
            "NOTLU GEÇTİ, bulgu var.",
            "Denetçi kararındaki sözcük (NOTLU GEÇTİ) Sonuç: değerinden (GEÇTİ) farklı",
        ),
        (
            "NOTLU GEÇTİ ve GEÇTİ.",
            "Denetçi kararındaki sözcük (NOTLU GEÇTİ, GEÇTİ) Sonuç: değerinden (GEÇTİ) farklı",
        ),
        ("", "Denetçi kararı (aynen): metni boş"),
        ("   ", "Denetçi kararı (aynen): metni boş"),
    ],
)
def test_kural_9_karar_metni(yeni, ayrinti):
    govde = GECERLI.replace(KARAR_SATIRI, f"Denetçi kararı (aynen): {yeni}\n")
    assert hatalar(govde) == ([] if ayrinti is None else [R9.format(ayrinti)])


def test_kural_9_sonuc_notlu_gecti_ister_notlu_karar():
    govde = GECERLI.replace("Sonuç: GEÇTİ", "Sonuç: NOTLU GEÇTİ")
    assert hatalar(govde) == [
        R9.format(
            "Denetçi kararındaki sözcük (GEÇTİ) Sonuç: değerinden (NOTLU GEÇTİ) farklı"
        )
    ]


def test_kural_9_kaldi_tam_sozcuk_olarak_aranir():
    govde = GECERLI.replace("Sonuç: GEÇTİ", "Sonuç: NOTLU GEÇTİ")
    govde = govde.replace(
        "(aynen): GEÇTİ, bulgu yok.", "(aynen): NOTLU GEÇTİ, iki not kaldırıldı"
    )
    assert hatalar(govde) == []
    govde = GECERLI.replace(
        "(aynen): GEÇTİ, bulgu yok.", "(aynen): GEÇTİ (KALDI olabilir)"
    )
    assert hatalar(govde) == [R9.format("Denetçi kararı KALDI içeriyor")]


def test_kural_9_karar_satiri_tek_olmali():
    assert hatalar(GECERLI.replace(KARAR_SATIRI, "")) == [
        R9.format("Denetçi kararı (aynen): satırı tek olmalı (0 satır var)")
    ]
    assert hatalar(GECERLI.replace(KARAR_SATIRI, KARAR_SATIRI * 2)) == [
        R9.format("Denetçi kararı (aynen): satırı tek olmalı (2 satır var)")
    ]


@pytest.mark.parametrize(
    ("eski", "yeni", "ayrinti"),
    [
        (
            "Yanlış iddia sayısı: 0\n",
            "",
            "Yanlış iddia sayısı: satırı tek olmalı (0 satır var)",
        ),
        (
            "Yanlış iddia sayısı: 0\n",
            "Yanlış iddia sayısı: 0\nYanlış iddia sayısı: 0\n",
            "Yanlış iddia sayısı: satırı tek olmalı (2 satır var)",
        ),
        (
            "Yanlış iddia sayısı: 0",
            "Yanlış iddia sayısı: ",
            "Yanlış iddia sayısı: değeri tam sayı olmalı",
        ),
        (
            "Yanlış iddia sayısı: 0",
            "Yanlış iddia sayısı: iki",
            "Yanlış iddia sayısı: değeri tam sayı olmalı",
        ),
        (
            "Yanlış iddia sayısı: 0",
            "Yanlış iddia sayısı: -1",
            "Yanlış iddia sayısı: değeri tam sayı olmalı",
        ),
        ("İkinci geçiş: yok\n", "", "İkinci geçiş: satırı tek olmalı (0 satır var)"),
        (
            "İkinci geçiş: yok\n",
            "İkinci geçiş: yok\nİkinci geçiş: yok\n",
            "İkinci geçiş: satırı tek olmalı (2 satır var)",
        ),
        ("İkinci geçiş: yok", "İkinci geçiş: ", "İkinci geçiş: yok ya da geçti olmalı"),
    ],
)
def test_kural_9_sayi_ve_ikinci_gecis(eski, yeni, ayrinti):
    assert hatalar(GECERLI.replace(eski, yeni)) == [R9.format(ayrinti)]


def test_kural_9_ikinci_gecis_alaninda_suphe_sozcugu():
    govde = GECERLI.replace("İkinci geçiş: yok", "İkinci geçiş: belki")
    assert hatalar(govde) == [
        R9.format(
            "Bağımsız inceleme bölümünde şüphe sözcüğü var "
            "(olabilir, belki, şüphe, emin değil); "
            "İkinci geçiş: yok ya da geçti olmalı"
        )
    ]


@pytest.mark.parametrize("ikinci", ["yok", "geçti"])
@pytest.mark.parametrize("sayi", ["1", "2"])
def test_kural_9_yanlis_iddia_varken_karar_gecemez(sayi, ikinci):
    govde = GECERLI.replace("Yanlış iddia sayısı: 0", f"Yanlış iddia sayısı: {sayi}")
    govde = govde.replace("İkinci geçiş: yok", f"İkinci geçiş: {ikinci}")
    assert hatalar(govde) == [
        R9.format("Yanlış iddia sayısı: yanlış iddia varken karar geçemez")
    ]


def test_kural_9_ikinci_gecis_yok_ve_gecti_sifirla_kabul_edilir():
    assert hatalar(GECERLI) == []
    assert hatalar(GECERLI.replace("İkinci geçiş: yok", "İkinci geçiş: geçti")) == []


SABLON_YORUMU = (
    "<!-- CI kuralları: Denetçi kararı satırı, denetçinin karar satırının kelimesi kelimesine "
    'kopyasıdır. CI, kopya KALDI sözcüğünü içeriyorsa PR\'ı reddeder. "KALDI olabilir" gibi '
    'bir şüphe de KALDI sayılır (AGENTS.md "Auditor and rounds"). Kopyadaki karar sözcüğü '
    'Sonuç satırındakiyle aynı olmalıdır. CI, "İNCELEME" yer tutucusunu reddeder. -->\n'
)
SONUC_YORUMU = (
    "<!-- CI accepts exactly one Sonuç line, and only one of these three exact texts: "
    '"Sonuç: geçti", "Sonuç: GEÇTİ", "Sonuç: NOTLU GEÇTİ". CI rejects "Geçti", KALDI, '
    "and a second Sonuç line. -->\n"
)
IKINCI_SATIRI = "İkinci geçiş: yok\n"


def test_kural_9_ve_11_sablon_yorumlari_gecer():
    govde = GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + SABLON_YORUMU + SONUC_YORUMU)
    assert hatalar(govde) == []
    assert hatalar(GECERLI + SABLON_YORUMU) == []


def test_kural_9_ve_11_cok_satirli_yorum_gecer():
    yorum = "<!-- ilk satır\nKALDI olabilir\nİNCELEME -->\n"
    assert hatalar(GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + yorum)) == []
    assert hatalar(GECERLI + yorum) == []


def test_yorum_inceleme_bolumunde_kaldi_satiri_gecer():
    govde = GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + "<!--\nSonuç: KALDI\n-->\n")
    assert hatalar(govde) == []


def test_yorum_icindeki_kapi_satirlari_sayilmaz():
    blok = (
        "kapi: pytest -> 0\n"
        "kapi: ruff check -> 0\n"
        "kapi: ruff format -> 0\n"
        "kapi: git diff --check -> 0\n"
        "kapi: driftlint -> 0\n"
        "kapi: HEAD 0123456789abcdef0123456789abcdef01234567 temiz\n"
    )
    govde = GECERLI.replace(blok, "<!--\n" + blok + "-->\n")
    assert hatalar(govde) == [
        "Kural 10: ## Gerçek veri kanıtı bölümünde eksik satır: "
        "kapi: pytest -> 0 ya da kapi: pytest (belge) -> 0; "
        "kapi: ruff check -> 0; kapi: ruff format -> 0; "
        "kapi: git diff --check -> 0; kapi: driftlint -> 0; "
        "kapi: HEAD <40 küçük harfli onaltılı hane> temiz."
    ]


def test_yorum_icindeki_isaretsiz_kutu_sayilmaz():
    govde = GECERLI.replace(AKIS_SATIRI, "<!--\n- [ ] Bekliyor\n-->\n" + AKIS_SATIRI)
    assert hatalar(govde) == []


def test_yorumdan_sonra_kural_2_satir_numarasi_dogru_kalir():
    govde = GECERLI.replace(
        AKIS_SATIRI, "<!--\nuc satirli\nyorum-->\n  - [ ] Bekliyor\n" + AKIS_SATIRI
    )
    assert hatalar(govde) == ["Kural 2: işaretsiz kutu var; satır: 34."]


def test_kural_9_suphe_bolumun_baska_satirinda():
    govde = GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + "Olabilir; kesin değil.\n")
    assert hatalar(govde) == [
        R9.format(
            "Bağımsız inceleme bölümünde şüphe sözcüğü var "
            "(olabilir, belki, şüphe, emin değil)"
        )
    ]
    govde = GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + "<!-- belki -->\n")
    assert hatalar(govde) == []


def test_kural_9_suphe_karar_satirindan_sonraki_satira_bolunur():
    govde = GECERLI.replace(
        KARAR_SATIRI, "Denetçi kararı (aynen): GEÇTİ, emin\ndeğil.\n"
    )
    assert hatalar(govde) == [
        R9.format(
            "Bağımsız inceleme bölümünde şüphe sözcüğü var "
            "(olabilir, belki, şüphe, emin değil)"
        )
    ]


def test_kural_9_kaldi_bolumun_baska_satirinda():
    govde = GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + "KALDI olabilir.\n")
    assert hatalar(govde) == [
        R9.format("Bağımsız inceleme bölümünde KALDI sözcüğü var")
    ]
    govde = GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + "Not: kaldı.\n")
    assert hatalar(govde) == [
        R9.format("Bağımsız inceleme bölümünde KALDI sözcüğü var")
    ]
    govde = GECERLI.replace(IKINCI_SATIRI, IKINCI_SATIRI + "Not: kaldırıldı.\n")
    assert hatalar(govde) == []


@pytest.mark.parametrize(
    "yeni",
    [
        "GEÇTİ olabilir.",
        "GEÇTİ, belki.",
        "GEÇTİ, Belki bir not.",
        "GEÇTİ, şüphe yok sayıldı.",
        "GEÇTİ, ŞÜPHE var.",
        "GEÇTİ, emin değil.",
        "GEÇTİ, EMİN DEĞİL.",
    ],
)
def test_kural_9_suphe_sozcugu_reddedilir(yeni):
    govde = GECERLI.replace(KARAR_SATIRI, f"Denetçi kararı (aynen): {yeni}\n")
    assert hatalar(govde) == [
        R9.format(
            "Denetçi kararı şüphe sözcüğü içeriyor (olabilir, belki, şüphe, emin değil)"
        )
    ]


R10 = "Kural 10: ## Gerçek veri kanıtı bölümünde {}."
KAPI_PYTEST = "kapi: pytest -> 0 ya da kapi: pytest (belge) -> 0"
KAPI_HEAD = "kapi: HEAD <40 küçük harfli onaltılı hane> temiz"
KAPI_SATIRLARI = (
    ("kapi: pytest -> 0\n", KAPI_PYTEST),
    ("kapi: ruff check -> 0\n", "kapi: ruff check -> 0"),
    ("kapi: ruff format -> 0\n", "kapi: ruff format -> 0"),
    ("kapi: git diff --check -> 0\n", "kapi: git diff --check -> 0"),
    ("kapi: driftlint -> 0\n", "kapi: driftlint -> 0"),
    (f"kapi: HEAD {SHA} temiz\n", KAPI_HEAD),
)


@pytest.mark.parametrize(("satir", "etiket"), KAPI_SATIRLARI)
def test_kural_10_satir_eksik(satir, etiket):
    assert hatalar(GECERLI.replace(satir, "")) == [R10.format("eksik satır: " + etiket)]


@pytest.mark.parametrize(
    ("satir", "yeni"),
    [
        ("kapi: pytest -> 0", "kapi: pytest -> 1"),
        ("kapi: pytest -> 0", "kapi: pytest -> 0 fazla"),
        ("kapi: ruff check -> 0", "kapi: ruff check -> 2"),
        ("kapi: ruff format -> 0", "kapi: ruff format -> 1"),
        ("kapi: git diff --check -> 0", "kapi: git diff --check -> 1"),
        ("kapi: driftlint -> 0", "kapi: driftlint -> 1"),
        ("kapi: driftlint -> 0", "kapi: driftlint -> 0 fazla"),
        (f"kapi: HEAD {SHA} temiz", f"kapi: HEAD {SHA} kirli"),
        (f"kapi: HEAD {SHA} temiz", f"kapi: HEAD {SHA[:39]} temiz"),
        (f"kapi: HEAD {SHA} temiz", f"kapi: HEAD {SHA.upper()} temiz"),
    ],
)
def test_kural_10_satir_yanlis(satir, yeni):
    etiket = dict((s.rstrip("\n"), e) for s, e in KAPI_SATIRLARI)[satir]
    assert hatalar(GECERLI.replace(satir, yeni)) == [
        R10.format("eksik satır: " + etiket)
    ]


def test_kural_10_pytest_belge_ve_bosluk_kabul_edilir():
    govde = GECERLI.replace("kapi: pytest -> 0", "kapi: pytest (belge) -> 0  ")
    assert hatalar(govde) == []
    assert hatalar(govde.replace("\n", " \r\n")) == []


def test_kural_10_head_pr_basi_ile_eslesir():
    assert hatalar(GECERLI, SHA) == []
    assert hatalar(GECERLI, None) == []
    govde = GECERLI.replace(DENETLENEN, f"Denetlenen commit: {SHA_BASKA}\n")
    assert hatalar(govde, SHA_BASKA) == [
        R10.format(
            f"kapi: HEAD değeri PR başından farklı; beklenen: {SHA_BASKA}, bulunan: {SHA}"
        )
    ]


def test_kural_10_her_onek_tam_bir_kez():
    eski = (
        "kapi: pytest -> 0\n"
        "kapi: ruff check -> 0\n"
        "kapi: ruff format -> 0\n"
        "kapi: git diff --check -> 0\n"
        "kapi: driftlint -> 0\n"
        "kapi: HEAD fedcba9876543210fedcba9876543210fedcba98 temiz\n"
    )
    yeni = (
        "kapi: pytest -> 1\n"
        "kapi: ruff check -> 0\n"
        "kapi: ruff format -> 0\n"
        "kapi: git diff --check -> 0\n"
        "kapi: driftlint -> 1\n"
        "kapi: HEAD 0123456789abcdef0123456789abcdef01234567 temiz\n"
    )
    govde = GECERLI.replace(
        "kapi: pytest -> 0\nkapi: ruff check -> 0\nkapi: ruff format -> 0\n"
        "kapi: git diff --check -> 0\nkapi: driftlint -> 0\n"
        "kapi: HEAD 0123456789abcdef0123456789abcdef01234567 temiz\n",
        eski + yeni,
    )
    assert hatalar(govde) == [
        R10.format(
            "birden çok satır: kapi: pytest; kapi: ruff check; kapi: ruff format; "
            "kapi: git diff --check; kapi: driftlint; kapi: HEAD"
        )
    ]


def test_kural_10_ikinci_pytest_satiri_reddedilir():
    govde = GECERLI.replace(
        "kapi: pytest -> 0\n", "kapi: pytest -> 0\nkapi: pytest -> 0\n"
    )
    assert hatalar(govde) == [R10.format("birden çok satır: kapi: pytest")]
    govde = GECERLI.replace(
        "kapi: pytest -> 0\n", "kapi: pytest -> 0\nkapi: pytest (belge) -> 0\n"
    )
    assert hatalar(govde) == [R10.format("birden çok satır: kapi: pytest")]


def test_kural_10_ikinci_head_satiri_reddedilir():
    ek = f"kapi: HEAD {SHA_BASKA} temiz\n"
    govde = GECERLI.replace(
        f"kapi: HEAD {SHA} temiz\n", f"kapi: HEAD {SHA} temiz\n{ek}"
    )
    assert hatalar(govde) == [R10.format("birden çok satır: kapi: HEAD")]


def test_kural_10_kod_var_ise_belge_pytest_reddedilir():
    belge = GECERLI.replace("kapi: pytest -> 0", "kapi: pytest (belge) -> 0")
    assert hatalar(belge, kod_var=True) == [
        R10.format("kod değişti; tam pytest gerekir")
    ]
    assert hatalar(belge, kod_var=False) == []
    assert hatalar(belge) == []
    assert hatalar(GECERLI, kod_var=True) == []


def test_kural_10_kod_var_ve_eksik_satir_birlikte():
    govde = GECERLI.replace("kapi: pytest -> 0", "kapi: pytest (belge) -> 0")
    govde = govde.replace("kapi: ruff check -> 0\n", "")
    assert hatalar(govde, kod_var=True) == [
        R10.format(
            "eksik satır: kapi: ruff check -> 0; kod değişti; tam pytest gerekir"
        )
    ]


def test_kural_11_inceleme_yer_tutucusu():
    assert hatalar(GECERLI + "İNCELEME\n") == [
        "Kural 11: PR gövdesinde İNCELEME yer tutucusu kalmış."
    ]
    assert hatalar(GECERLI + "<!-- İNCELEME -->\nİNCELEME\n") == [
        "Kural 11: PR gövdesinde İNCELEME yer tutucusu kalmış."
    ]


DENETLENEN = f"Denetlenen commit: {SHA}\n"
R12_SATIR = (
    "Kural 12: PR gövdesinde Denetlenen commit: <40 küçük harfli onaltılı hane> "
    "satırı tek olmalı ({} satır var)."
)
R12_DEGER = "Kural 12: Denetlenen commit: değeri 40 küçük harfli onaltılı hane olmalı."
R12_TABAN = "Kural 12: Denetlenen commit PR başı değil ve taban dal bilinmiyor."
R12_BIRLESME = (
    "Kural 12: Denetlenen commit ({}) PR başı ({}) değil; "
    "sonraki commit'ler temiz bir taban birleştirmesi değil."
)


@pytest.mark.parametrize(
    ("yeni", "sayi"), [("", 0), (DENETLENEN * 2, 2), (DENETLENEN * 3, 3)]
)
def test_kural_12_satir_tek_olmali(yeni, sayi):
    assert hatalar(GECERLI.replace(DENETLENEN, yeni)) == [R12_SATIR.format(sayi)]


@pytest.mark.parametrize(
    "deger", ["", "yok", SHA.upper(), SHA[:39], SHA + "0", "g" * 40, "`" + SHA + "`"]
)
def test_kural_12_deger_40_kucuk_onaltili_olmali(deger):
    govde = GECERLI.replace(DENETLENEN, f"Denetlenen commit: {deger}\n")
    assert hatalar(govde) == [R12_DEGER]


def test_kural_12_yorumdaki_satir_sayilmaz():
    govde = GECERLI.replace(DENETLENEN, DENETLENEN + "<!--\n" + DENETLENEN + "-->\n")
    assert hatalar(govde) == []
    assert hatalar(GECERLI.replace(DENETLENEN, "<!-- " + DENETLENEN + "-->\n")) == [
        R12_SATIR.format(0)
    ]


def test_kural_12_pr_basi_esit_ya_da_taban_bilinmiyor():
    assert hatalar(GECERLI, SHA) == []
    assert hatalar(GECERLI, None) == []
    assert hatalar(GECERLI, SHA_BASKA) == [
        R10.format(
            f"kapi: HEAD değeri PR başından farklı; beklenen: {SHA_BASKA}, bulunan: {SHA}"
        ),
        R12_TABAN,
    ]


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


def _govde_git(denetlenen, bas):
    govde = GECERLI.replace(DENETLENEN, f"Denetlenen commit: {denetlenen}\n")
    return govde.replace(f"kapi: HEAD {SHA}", f"kapi: HEAD {bas}")


def test_kural_12_temiz_taban_birlestirmesi_gecer(depo):
    dizin, b, m = depo
    assert hatalar(_govde_git(b, m), m, taban="master", dizin=dizin) == []


def test_kural_12_denetlenen_pr_basi_ise_git_gerekmez(depo):
    dizin, _, m = depo
    assert hatalar(_govde_git(m, m), m, taban="master", dizin=dizin) == []


def test_kural_12_duz_commit_reddedilir(depo):
    dizin, b, _ = depo
    d = _commit(dizin, "d.txt", "D")
    assert hatalar(_govde_git(b, d), d, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, d)
    ]


def test_kural_12_elle_degisen_birlestirme_reddedilir(depo):
    dizin, b, _ = depo
    _git(dizin, "checkout", "-b", "kotu", b)
    _git(dizin, "merge", "--no-commit", "--no-ff", "master")
    (dizin / "b.txt").write_text("elle", encoding="utf-8")
    _git(dizin, "add", "b.txt")
    _git(dizin, "commit", "--no-edit")
    kotu = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(_govde_git(b, kotu), kotu, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, kotu)
    ]


def test_kural_12_taban_disi_ikinci_ebeveyn_reddedilir(depo):
    dizin, b, _ = depo
    _git(dizin, "checkout", "-b", "yan", "master")
    _commit(dizin, "y.txt", "Y")
    _git(dizin, "checkout", "-b", "baska", b)
    _git(dizin, "merge", "--no-edit", "yan")
    baska = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(_govde_git(b, baska), baska, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, baska)
    ]


def test_kural_12_bilinmeyen_sha_reddedilir(depo):
    dizin, _, m = depo
    assert hatalar(_govde_git(SHA_BASKA, m), m, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(SHA_BASKA, m)
    ]


def test_kural_12_elle_cozulen_celiski_taban_ozelligiyle_gizlenmez(depo):
    dizin, _, _ = depo
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
    m = _git(dizin, "rev-parse", "HEAD")
    _git(dizin, "checkout", "master")
    _commit(dizin, ".gitattributes", "*.txt merge=union\n")
    assert hatalar(_govde_git(b, m), m, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, m)
    ]


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


def test_kural_12_info_attributes_celiskiyi_gizlemez(depo):
    dizin, _, _ = depo
    b, m = _celiski_birlesmesi(dizin)
    (dizin / ".git" / "info" / "attributes").write_text(
        "*.txt merge=union\n", encoding="utf-8"
    )
    assert hatalar(_govde_git(b, m), m, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, m)
    ]


def test_kural_12_ayni_dosyada_iki_taraf_degisirse_reddedilir(depo):
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
    assert hatalar(_govde_git(b, m), m, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, m)
    ]


def test_kural_12_silme_ve_yeniden_adlandirma_gecer(depo):
    dizin, b, _ = depo
    _git(dizin, "checkout", "master")
    _git(dizin, "rm", "a.txt")
    _git(dizin, "commit", "-m", "sil")
    _git(dizin, "mv", "c.txt", "d.txt")
    _git(dizin, "commit", "-m", "ad")
    _git(dizin, "checkout", "-b", "yan4", b)
    _git(dizin, "merge", "--no-edit", "master")
    m = _git(dizin, "rev-parse", "HEAD")
    assert hatalar(_govde_git(b, m), m, taban="master", dizin=dizin) == []


def _kotu_birlesme(dizin, b, degistir):
    _git(dizin, "checkout", "-b", "kotu", b)
    _git(dizin, "merge", "--no-commit", "--no-ff", "master")
    degistir(dizin)
    _git(dizin, "add", "-A")
    _git(dizin, "commit", "--no-edit")
    return _git(dizin, "rev-parse", "HEAD")


@pytest.mark.parametrize("dosya", ["fazla.txt", "c.txt"])
def test_kural_12_fazla_dosya_ya_da_dusen_dosya_reddedilir(depo, dosya):
    dizin, b, _ = depo

    def degistir(dizin):
        if dosya == "c.txt":
            (dizin / dosya).unlink()
        else:
            (dizin / dosya).write_text("x", encoding="utf-8")

    kotu = _kotu_birlesme(dizin, b, degistir)
    assert hatalar(_govde_git(b, kotu), kotu, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, kotu)
    ]


def test_kural_12_capraz_birlesme_reddedilir(depo):
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
    assert hatalar(_govde_git(a1, x), x, taban="cb", dizin=dizin) == [
        R12_BIRLESME.format(a1, x)
    ]


@pytest.mark.parametrize("taban", ["yok-dal", "master^{tree}"])
def test_kural_12_taban_gecersizse_reddedilir(depo, taban):
    dizin, b, m = depo
    assert hatalar(_govde_git(b, m), m, taban=taban, dizin=dizin) == [
        R12_BIRLESME.format(b, m)
    ]


def test_kural_12_denetlenen_agac_ya_da_etiket(depo):
    dizin, b, m = depo
    agac = _git(dizin, "rev-parse", f"{b}^{{tree}}")
    assert hatalar(_govde_git(agac, m), m, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(agac, m)
    ]
    _git(dizin, "tag", "-a", "-m", "e", "etiket", b)
    etiket = _git(dizin, "rev-parse", "etiket")
    assert hatalar(_govde_git(etiket, m), m, taban="master", dizin=dizin) == []


@pytest.mark.parametrize("alt", ["rev-list", "merge-base", "diff-tree"])
def test_kural_12_git_donus_kodu_hatasi_reddedilir(depo, monkeypatch, alt):
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
    assert hatalar(_govde_git(b, m), m, taban="master", dizin=dizin) == [
        R12_BIRLESME.format(b, m)
    ]


RISK = "## Risk\nKüçük risk.\n"
GERI = "## Nasıl geri alınır\nPR geri alınır.\n"
YANIT = "## Bulgu yanıtları\nbulgu yok\n"


@pytest.mark.parametrize(
    ("eski", "baslik"),
    [(RISK, "## Risk"), (GERI, "## Nasıl geri alınır"), (YANIT, "## Bulgu yanıtları")],
)
def test_kural_13_baslik_eksik(eski, baslik):
    assert hatalar(GECERLI.replace(eski, "")) == [
        f"Kural 13: eksik başlıklar: {baslik}."
    ]


@pytest.mark.parametrize(
    ("eski", "yeni", "baslik"),
    [
        (RISK, "## Risk\n", "## Risk"),
        (RISK, "## Risk\n  \n", "## Risk"),
        (GERI, "## Nasıl geri alınır\n<!-- komut -->\n", "## Nasıl geri alınır"),
        (GERI, "## Nasıl geri alınır\n<!--\nçok\nsatır\n-->\n", "## Nasıl geri alınır"),
    ],
)
def test_kural_13_bolum_bos(eski, yeni, baslik):
    assert hatalar(GECERLI.replace(eski, yeni)) == [f"Kural 13: boş bölüm: {baslik}."]


def test_kural_13_eksik_ve_bos_birlikte():
    govde = GECERLI.replace(RISK, "").replace(GERI, "## Nasıl geri alınır\n")
    assert hatalar(govde) == [
        "Kural 13: eksik başlıklar: ## Risk; boş bölüm: ## Nasıl geri alınır."
    ]


R14_TEK = "Kural 14: Bulgu sayısı: satırı tek olmalı ({} satır var)."
R14_SAYI = "Kural 14: Bulgu sayısı: değeri tam sayı olmalı."
R14_SAYIM = "Kural 14: Bulgu yanıtları tablosunda {} satır olmalı ({} satır var)."
R14_SATIR = "Kural 14: Bulgu yanıtları satırı geçersiz: {}."
R14_YOK = (
    'Kural 14: Bulgu sayısı 0 ise Bulgu yanıtları bölümünde yalnız "bulgu yok" '
    "satırı olur."
)
R14_DISI = "Kural 14: Bulgu yanıtları bölümünde tablo dışı satır var."
R14_BASLIK = "Kural 14: Bulgu yanıtları tablosunda başlık ve ayraç satırı olmalı."
BULGU = "Bulgu sayısı: 0\n"
TABLO = "| Bulgu | Yanıt | Commit ya da neden |\n|---|---|---|\n"


def _bulgular(sayi, yanit):
    govde = GECERLI.replace(BULGU, f"Bulgu sayısı: {sayi}\n")
    return govde.replace(YANIT, "## Bulgu yanıtları\n" + yanit)


def test_kural_14_sayi_satiri_eksik_ya_da_cift():
    assert hatalar(GECERLI.replace(BULGU, "")) == [R14_TEK.format(0)]
    assert hatalar(GECERLI.replace(BULGU, BULGU * 2)) == [R14_TEK.format(2)]


@pytest.mark.parametrize("deger", ["", "iki", "-1", "1.5"])
def test_kural_14_sayi_tam_sayi_olmali(deger):
    govde = GECERLI.replace(BULGU, f"Bulgu sayısı: {deger}\n")
    assert hatalar(govde) == [R14_SAYI]


def test_kural_14_iki_gecerli_satir_gecer():
    tablo = TABLO + "| a | düzeltildi | abc1234 |\n| b | `bilerek` | neden |\n"
    assert hatalar(_bulgular(2, tablo)) == []
    tablo = TABLO + "| a | yanlış | x |\n| b | önemsiz | y |\n"
    assert hatalar(_bulgular(2, tablo)) == []


def test_kural_14_satir_sayisi_sayiya_esit_olmali():
    tablo = TABLO + "| a | düzeltildi | abc1234 |\n"
    assert hatalar(_bulgular(2, tablo)) == [R14_SAYIM.format(2, 1)]
    assert hatalar(_bulgular(1, tablo + tablo[len(TABLO) :])) == [
        R14_SAYIM.format(1, 2)
    ]
    assert hatalar(_bulgular(1, TABLO)) == [R14_SAYIM.format(1, 0)]


@pytest.mark.parametrize(
    ("satirlar", "numaralar"),
    [
        ("| a | düzeltildi | x |\n| b | tamam | y |\n", "2"),
        ("| a | düzeltildi |  |\n| b | yanlış | y |\n", "1"),
        ("|  | düzeltildi | x |\n| b | yanlış | y |\n", "1"),
        ("| a | düzeltildi |  |\n|  | yanlış | y |\n", "1, 2"),
        ("| a | düzeltildi |\n| b | yanlış | y | z |\n", "1, 2"),
        ("| a | Düzeltildi | x |\n| b | yanlış | y |\n", "1"),
    ],
)
def test_kural_14_gecersiz_satir(satirlar, numaralar):
    assert hatalar(_bulgular(2, TABLO + satirlar)) == [R14_SATIR.format(numaralar)]


@pytest.mark.parametrize(
    "satir",
    ["|| A | düzeltildi | x |\n", "| A | düzeltildi | x ||\n"],
)
def test_kural_14_fazla_boru_hucre_silmez(satir):
    assert hatalar(_bulgular(1, TABLO + satir)) == [R14_SATIR.format("1")]


@pytest.mark.parametrize(
    "satir",
    [
        "| A\\| düzeltildi | x |\n",
        "| A | düzeltildi | x\n",
        "| A | düzeltildi | x \\|\n",
        "|---|---|---|\n",
    ],
)
def test_kural_14_kacis_ve_eksik_boru_gecersiz_satirdir(satir):
    assert hatalar(_bulgular(1, TABLO + satir)) == [R14_SATIR.format("1")]


def test_kural_14_tablo_disi_satir_reddedilir():
    satir = "| A | düzeltildi | x |\nB | yanlış | y\n"
    assert hatalar(_bulgular(1, TABLO + satir)) == [R14_DISI]
    assert hatalar(_bulgular(1, TABLO + "bulgu yok\n| A | yanlış | y |\n")) == [
        R14_DISI
    ]


@pytest.mark.parametrize(
    "yanit",
    [
        "| Bulgu | Yanıt | Commit ya da neden |\n| a | düzeltildi | x |\n",
        "| Bulgu | Yanıt | Commit ya da neden |\n",
        "| Bulgu | Yanıt |\n|---|---|---|\n| a | düzeltildi | x |\n",
        "| Bulgu | Yanıt | Commit ya da neden\n|---|---|---|\n| a | yanlış | x |\n",
        "| Bulgu | Yanıt | Commit ya da neden |\n|---|---|\n| a | yanlış | x |\n",
        "|---|---|---|\n|---|---|---|\n| a | yanlış | x |\n",
        "| a | yanlış | x |\n",
    ],
)
def test_kural_14_baslik_ve_ayrac_olmali(yanit):
    assert hatalar(_bulgular(1, yanit)) == [R14_BASLIK]


def test_kural_14_sifir_bulgu_baslik_ayrac_ister():
    assert hatalar(_bulgular(0, "| a | b | c |\nbulgu yok\n")) == [R14_BASLIK]


def test_kural_14_crlf_bosluk_ve_kesme_isareti_kabul_edilir():
    tablo = TABLO + "  | a | ` düzeltildi ` | x |  \n| b | yanlış | y |\n"
    assert hatalar(_bulgular(2, tablo.replace("\n", "\r\n"))) == []
    assert hatalar(_bulgular(0, TABLO + "  bulgu yok  \n")) == []


def test_kural_14_ikinci_tablo_ve_fazla_sutun_reddedilir():
    ikinci = TABLO + "| a | yanlış | x |\n" + TABLO
    assert hatalar(_bulgular(1, ikinci)) == [
        R14_SAYIM.format(1, 3),
        R14_SATIR.format("2, 3"),
    ]
    assert hatalar(_bulgular(1, TABLO + "| a | yanlış | x | y |\n")) == [
        R14_SATIR.format("1")
    ]


def test_kural_14_sifir_bulgu():
    assert hatalar(_bulgular(0, "bulgu yok\n")) == []
    assert hatalar(_bulgular(0, TABLO + "bulgu yok\n")) == []
    assert hatalar(_bulgular(0, "yok\n")) == [R14_YOK]
    assert hatalar(_bulgular(0, "")) == [R14_YOK]
    govde = _bulgular(0, "bulgu yok\n" + TABLO + "| a | düzeltildi | x |\n")
    assert hatalar(govde) == [R14_YOK]


def test_kural_14_bolum_yoksa_tablo_denetlenmez():
    govde = GECERLI.replace(BULGU, "Bulgu sayısı: 3\n").replace(YANIT, "")
    assert hatalar(govde) == ["Kural 13: eksik başlıklar: ## Bulgu yanıtları."]


R15 = (
    "Kural 15: Dal adı geçersiz: {!r}; biçim pr/<sayı>-<ad> olmalı "
    "(ad: küçük harf, rakam ve tire)."
)


@pytest.mark.parametrize(
    "dal", [None, "pr/43-retro-duzeltme-2", "pr/1-x", "pr/007-a1-b2"]
)
def test_kural_15_gecerli_dal(dal):
    assert hatalar(GECERLI, dal=dal) == []


@pytest.mark.parametrize(
    "dal",
    [
        "master",
        "",
        "pr/x-ad",
        "pr/43",
        "pr/43-",
        "pr/43-Ad",
        "pr/43-ad_x",
        "pr/43-ad/alt",
        "feature/pr/43-x",
        "pr/43-ad\n",
        "pr/４３-x",
    ],
)
def test_kural_15_gecersiz_dal(dal):
    assert hatalar(GECERLI, dal=dal) == [R15.format(dal)]


def test_kural_15_bos_govdede_de_dal_denetlenir():
    assert hatalar("", dal="master")[-1] == R15.format("master")


def test_kural_15_komut_satiri_pr_dal_okur():
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("PR_DAL", "PR_BAS_SHA", "PR_KOD_VAR", "GITHUB_BASE_REF")
    }
    env |= {"PR_GOVDE": GECERLI, "PYTHONIOENCODING": "utf-8"}

    def calistir(**ek):
        return subprocess.run(
            [sys.executable, str(_yol)],
            env=env | ek,
            capture_output=True,
            encoding="utf-8",
        )

    kotu = calistir(PR_DAL="master")
    assert kotu.returncode == 1
    assert R15.format("master") in kotu.stdout.splitlines()
    assert calistir(PR_DAL="pr/43-retro-duzeltme-2").returncode == 0
    assert calistir().returncode == 0


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
        "PR_DAL: ${{ github.event.pull_request.head.ref }}",
        "PR_KOD_VAR",
        "fetch-depth: 0",
        "set -eu",
        "BASE: ${{ github.base_ref }}",
        "$GITHUB_ENV",
    ):
        assert parca in metin


def test_kapi_betigi():
    yol = Path(__file__).resolve().parents[1] / "kurulum" / "kapi.ps1"
    metin = yol.read_bytes().decode("ascii")
    for parca in (
        "-m pytest -q",
        "ruff check .",
        "ruff format --check .",
        "git diff --check kaynak/master",
        "kapi: HEAD",
        "temiz",
        "kirli",
    ):
        assert parca in metin
    assert "--untracked-files=no" not in metin
