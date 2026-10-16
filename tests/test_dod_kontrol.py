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
Denetçi kararı (aynen): GEÇTİ, bulgu yok.
Yanlış iddia sayısı: 0
İkinci geçiş: yok
Sonuç: GEÇTİ
## Gerçek veri kanıtı
```text
Gerçek koşu çıktısı
```
kapi: pytest -> 0
kapi: ruff check -> 0
kapi: ruff format -> 0
kapi: git diff --check -> 0
kapi: HEAD 0123456789abcdef0123456789abcdef01234567 temiz
Çağrılan beceriler: tansu-yeni-is, verification-before-completion, mattpocock-skills:pr, mattpocock-skills:code-review
Akış: tansu-yeni-is
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
    ) == ["Kural 2: işaretsiz kutu var; satır: 30."]


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
        (
            "İkinci geçiş: yok",
            "İkinci geçiş: belki",
            "İkinci geçiş: yok ya da geçti olmalı",
        ),
        ("İkinci geçiş: yok", "İkinci geçiş: ", "İkinci geçiş: yok ya da geçti olmalı"),
    ],
)
def test_kural_9_sayi_ve_ikinci_gecis(eski, yeni, ayrinti):
    assert hatalar(GECERLI.replace(eski, yeni)) == [R9.format(ayrinti)]


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
    assert hatalar(GECERLI, SHA_BASKA) == [
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
        "kapi: HEAD fedcba9876543210fedcba9876543210fedcba98 temiz\n"
    )
    yeni = (
        "kapi: pytest -> 1\n"
        "kapi: ruff check -> 0\n"
        "kapi: ruff format -> 0\n"
        "kapi: git diff --check -> 0\n"
        "kapi: HEAD 0123456789abcdef0123456789abcdef01234567 temiz\n"
    )
    govde = GECERLI.replace(
        "kapi: pytest -> 0\nkapi: ruff check -> 0\nkapi: ruff format -> 0\n"
        "kapi: git diff --check -> 0\n"
        "kapi: HEAD 0123456789abcdef0123456789abcdef01234567 temiz\n",
        eski + yeni,
    )
    assert hatalar(govde) == [
        R10.format(
            "birden çok satır: kapi: pytest; kapi: ruff check; kapi: ruff format; "
            "kapi: git diff --check; kapi: HEAD"
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


def test_dod_yml_taslak_ve_sha():
    yol = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "dod.yml"
    metin = yol.read_text(encoding="utf-8")
    for parca in (
        "draft == false",
        "ready_for_review",
        "PR_BAS_SHA: ${{ github.event.pull_request.head.sha }}",
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
