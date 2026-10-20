"""Atıf testi (bilet 08): belge ve koddaki atıflar var olan bir bölüme ya da karara gider.

Bölüm atıfları (`TASARIM 5.1`, `TASARIM §5.1`, `KURALLAR §3`) docs/TASARIM.md ve docs/KURALLAR.md
başlıklarına bakar. Karar etiketleri (İ:, B-, C-, S2-) yerel docs/sorgu/ klasörüne bakar; klasör
git'te olmadığı için CI'da etiket testi atlanır, yerel test kapısı denetler.
"""

import json
import subprocess

import pytest

from atif_araclari import (
    KOK,
    alinti_sorunlari,
    atif_kirikleri,
    belge_alinti_sorunlari,
    bolum_numaralari,
    etiket_kirikleri,
    izlenen_dosyalar,
    kacisli_etiketler,
    kisaltma_kirikleri,
    main,
    parti_entegre,
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
        "CODING_STANDARDS.md",
        "DEFINITION_OF_DONE.md",
        "tansu/kayit.py",
        ".claude/skills/tansu-grill/SKILL.md",
        ".claude/skills/tansu-yeni-is/SKILL.md",
        "docs/agents/is-kurallari.md",
        ".github/pull_request_template.md",
    } <= adlar
    # .scratch/ ve arsiv/ yerel tarihsel metindir; git ve güncel atıf taraması dışında.
    assert not any(ad.startswith((".scratch/", "arsiv/")) for ad in adlar)


def test_tasima_sonrasi_silinen_izlenen_dosya_taranmaz(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    eski = docs / "eski.md"
    yeni = docs / "yeni.md"
    for yol in (eski, yeni):
        yol.write_text("## 1. Kural\n", encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "docs/eski.md", "docs/yeni.md")
    eski.unlink()
    assert izlenen_dosyalar(tmp_path) == [yeni]


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


@pytest.mark.parametrize(
    "ad", ["AGENTS.md", "CODING_STANDARDS.md", "DEFINITION_OF_DONE.md"]
)
def test_kok_belgelerinde_kirik_karar_etiketi_yakalanir(tmp_path, ad):
    # Kök belgeler izlenen dosya kümesindedir; etiket taraması onları atlamaz.
    sorgu = _sorgu(tmp_path)
    (tmp_path / ad).write_text("Not\nB-99999\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", ad], check=True)
    assert etiket_kirikleri(tmp_path, izlenen_dosyalar(tmp_path), sorgu) == [
        f"{ad}:2: B-99999"
    ]


# --- alıntı denetimi (retro 16.10): kayıttaki tırnaklı metin notun Ham ya da Görsel metni bölümünde geçer ---


def _not(havuz, ad, ham="", gorsel="", ozet=""):
    havuz.mkdir(exist_ok=True)
    (havuz / f"{ad}.md").write_text(
        f"# Tansu\n\n## Ham\n\n{ham}\n\n## Görsel metni\n\n### G1 (a.png)\n\n{gorsel}\n\n## Özet\n\n{ozet}\n",
        encoding="utf-8",
    )


def _jsonl(yol, *kayitlar):
    yol.write_text(
        "\n".join(json.dumps(k, ensure_ascii=False) for k in kayitlar) + "\n",
        encoding="utf-8",
    )
    return yol


HAM = "Aslolan para girişidir. Para yoksa gerisine bakmaya gerek yok."


def _alinti(tmp_path, kayit, **bolumler):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", **bolumler)
    yol = _jsonl(tmp_path / "k.jsonl", {"not": "tweet-a-1", **kayit})
    return alinti_sorunlari(havuz, [yol])


@pytest.mark.parametrize(
    ("kayit", "bolumler", "beklenen"),
    [
        # birebir alıntı
        (
            {"satir": 'İlke: "Para yoksa gerisine bakmaya gerek yok." (Ham).'},
            {"ham": HAM},
            [],
        ),
        # Görsel metni bölümünden alıntı
        (
            {"satir": 'Etiket "STOP: 0.86 / ATR: 0.39" (görsel metni).'},
            {"gorsel": "STOP: 0.86\nATR: 0.39"},
            [],
        ),
        # yeni_metin ve parametre alanları da taranır
        ({"yeni_metin": '- Ifade: "gerek yok" (Ham)'}, {"ham": HAM}, []),
        ({"parametre": 'EMA = 5 ("EMA 5")'}, {"ham": "EMA 5"}, []),
        # çıkarma: … ve ... ile kesilen alıntı, her parça kaynakta geçmeli
        ({"satir": 'a "Aslolan para … gerek yok" b'}, {"ham": HAM}, []),
        ({"satir": 'a "Aslolan para... gerek yok" b'}, {"ham": HAM}, []),
        ({"satir": 'a "…gerisine bakmaya…" b'}, {"ham": HAM}, []),
        # eğri tırnak
        ({"satir": "a “bakmaya gerek” b"}, {"ham": HAM}, []),
        # normalleştirme: eğri kesme, \\#, **, blok alıntı, ` / `, Türkçe büyük harf
        ({"satir": 'a "EMA5\'den büyük"'}, {"ham": "EMA5’den büyük"}, []),
        ({"satir": 'a "‘kod’ #BIST"'}, {"ham": "'kod' \\#BIST"}, []),
        ({"satir": 'a "fiyat EMA5 üstünde"'}, {"ham": "fiyat **EMA5** üstünde"}, []),
        (
            {"satir": 'a "ilk satır ikinci satır"'},
            {"ham": "> ilk satır\n> ikinci satır"},
            [],
        ),
        (
            {"satir": 'a "EMA5 > EMA20 / EMA10 > EMA20"'},
            {"ham": "EMA5 > EMA20\nEMA10 > EMA20"},
            [],
        ),
        ({"satir": 'a "işte ILIK"'}, {"ham": "İŞTE ılık"}, []),
        # tırnaksız alanlarda ve tırnaksız satırda sorun yok
        ({"satir": "alıntı yok, yalnız yorum"}, {"ham": HAM}, []),
        # paraphrase: kaynakta birebir yok
        (
            {"satir": 'İlke: "para girişi esastır" (Ham).'},
            {"ham": HAM},
            ["k.jsonl:1: tweet-a-1: para girişi esastır"],
        ),
        # … ile kesilen alıntının bir parçası kaynakta yok
        (
            {"satir": 'a "Aslolan para … başka şey" b'},
            {"ham": HAM},
            ["k.jsonl:1: tweet-a-1: Aslolan para … başka şey"],
        ),
        # ikinci el bölümden alıntı sayılmaz
        (
            {"satir": 'a "yalnız özette geçer" b'},
            {"ham": HAM, "ozet": "yalnız özette geçer"},
            ["k.jsonl:1: tweet-a-1: yalnız özette geçer"],
        ),
        # `\#` alanda yasak
        (
            {"satir": "etiket \\#BIST"},
            {"ham": HAM},
            ["k.jsonl:1: tweet-a-1: \\# in satir"],
        ),
        (
            {"yeni_metin": "- x \\#BIST", "parametre": "p \\#x"},
            {"ham": HAM},
            [
                "k.jsonl:1: tweet-a-1: \\# in yeni_metin",
                "k.jsonl:1: tweet-a-1: \\# in parametre",
            ],
        ),
    ],
)
def test_alinti_sorunlari(tmp_path, kayit, bolumler, beklenen):
    assert _alinti(tmp_path, kayit, **bolumler) == beklenen


@pytest.mark.parametrize(
    ("satir", "ham", "beklenen"),
    [
        # parçalar kaynakta ileri sırayla geçer
        ('a "SAT ... AL" b', "AL sonra SAT", ["k.jsonl:1: tweet-a-1: SAT ... AL"]),
        ('a "SAT … AL" b', "AL sonra SAT", ["k.jsonl:1: tweet-a-1: SAT … AL"]),
        ('a "SAT ... AL" b', "SAT sonra AL", []),
        ('a "SAT … AL" b', "önce SAT sonra AL", []),
        # ikinci parça birincinin bittiği yerden sonra başlar
        ('a "ab … ab" b', "ab", ["k.jsonl:1: tweet-a-1: ab … ab"]),
        ('a "ab … ab" b', "ab x ab", []),
        # ` / ` iki yanı da boşluğa çevrilmez: kaynaktaki eğik çizgi kalır
        ('a "10 2" b', "10 / 2", ["k.jsonl:1: tweet-a-1: 10 2"]),
        ('a "10 / 2" b', "10 / 2", []),
        # alıntıdaki ` / ` satır sonu işaretidir: parçalar ileri sırayla, kaynakta satır sonuyla geçer
        ('a "EMA5 > EMA20 / EMA10 > EMA20" b', "EMA5 > EMA20\nEMA10 > EMA20", []),
        (
            'a "Bravo / Alfa" b',
            "Alfa\nBravo",
            ["k.jsonl:1: tweet-a-1: Bravo / Alfa"],
        ),
        # satır sonu içeren alıntı da denetlenir
        ('a "kaynakta\nyok" b', HAM, ["k.jsonl:1: tweet-a-1: kaynakta yok"]),
        ('a "Para yoksa\ngerisine" b', HAM, []),
    ],
)
def test_alinti_parcalari_ileri_sirayla_tek_kaynakta(tmp_path, satir, ham, beklenen):
    assert _alinti(tmp_path, {"satir": satir}, ham=ham) == beklenen


def test_alinti_parcalari_iki_notta_dagilamaz(tmp_path):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham="birinci")
    _not(havuz, "tweet-b-2", ham="ikinci")
    yol = _jsonl(
        tmp_path / "k.jsonl",
        {"not": "tweet-a-1", "satir": 'x `tweet-b-2` "birinci … ikinci"'},
        {"not": "tweet-b-2", "satir": 'x `tweet-a-1` "birinci / ikinci"'},
    )
    assert alinti_sorunlari(havuz, [yol]) == [
        "k.jsonl:1: tweet-a-1: birinci … ikinci",
        "k.jsonl:2: tweet-b-2: birinci / ikinci",
    ]


def test_alinti_adayi_kayit_notu_ve_alandaki_not_adlaridir(tmp_path):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham="birinci not")
    _not(havuz, "tweet-b-2", ham="ikinci not")
    yol = _jsonl(
        tmp_path / "k.jsonl",
        {"not": "tweet-a-1", "satir": 'a "birinci" ve `tweet-b-2` "ikinci not"'},
        {"not": "tweet-a-1", "satir": 'a "ikinci not" ve `tweet-b-2.md`'},
        {"not": "tweet-a-1", "satir": 'a "ikinci not"'},
    )
    assert alinti_sorunlari(havuz, [yol]) == ["k.jsonl:3: tweet-a-1: ikinci not"]


def test_alinti_eksik_not_dosyasi_hatadir(tmp_path):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham="metin")
    yol = _jsonl(
        tmp_path / "k.jsonl",
        {"not": "tweet-yok-9", "sonuc": "yok", "neden": "sohbet"},
        {"not": "tweet-a-1", "satir": 'a "metin" `tweet-kayip-8`'},
    )
    assert alinti_sorunlari(havuz, [yol]) == [
        "k.jsonl:1: tweet-yok-9: not dosyası yok",
        "k.jsonl:2: tweet-kayip-8: not dosyası yok",
    ]


def test_alinti_satir_numarasi_ve_dosya_adi(tmp_path):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham="tamam")
    yol = _jsonl(
        tmp_path / "E99.jsonl",
        {"not": "tweet-a-1", "satir": 'a "tamam"'},
        {"not": "tweet-a-1", "satir": 'a "değil"'},
    )
    assert alinti_sorunlari(havuz, [yol]) == ["E99.jsonl:2: tweet-a-1: değil"]


# --- kaçışlı etiket ve kırık kısaltma ---


def test_kacisli_etiket_satiri_yakalanir(tmp_path):
    temiz = tmp_path / "temiz.md"
    kirli = tmp_path / "kirli.md"
    temiz.write_text("#BIST ve # başlık\n", encoding="utf-8")
    kirli.write_text("ok\n  \\#BIST etiketi\n", encoding="utf-8")
    assert kacisli_etiketler([temiz]) == []
    assert kacisli_etiketler([temiz, kirli]) == [
        f"{kirli.as_posix()}:2: \\#BIST etiketi"
    ]


def _docs_md():
    return [
        yol
        for yol in izlenen_dosyalar(KOK)
        if yol.suffix == ".md" and yol.relative_to(KOK).parts[0] == "docs"
    ]


def test_belgelerde_kacisli_etiket_yok():
    assert kacisli_etiketler(_docs_md()) == []


def test_kisaltma_kirigi_yakalanir(tmp_path):
    temiz = tmp_path / "temiz.md"
    kirli = tmp_path / "kirli.md"
    temiz.write_text("(Araç, G45/g1) ve Rota ayrı yazılır\n", encoding="utf-8")
    kirli.write_text("a\nkaynak Rota/g2 notu\nbu bir kısaltması\n", encoding="utf-8")
    assert kisaltma_kirikleri([temiz]) == []
    assert kisaltma_kirikleri([kirli]) == [
        f"{kirli.as_posix()}:2: Rota/g2",
        f"{kirli.as_posix()}:3: kısaltması",
    ]


def test_belgelerde_kirik_kisaltma_yok():
    assert kisaltma_kirikleri(_docs_md()) == []


# --- parti_entegre: ek ve yok kayıtlarını belgelere yazar ---

E_METNI = (
    "## K1. Stop\n- Kaynak: x\n- Ek kaynaklar (X arşivi, 15.10):\n  - `tweet-eski-1` — eski satır.\n\n"
    "## K2. Çıkış\n- Kaynak: y\n\n- Kaynak güveni: orta\n\n"
    "## K3. Son\n- Kaynak: z\n"
)
KURALLAR_METNI = (
    "## 4. Önceki\nmetin\n\n"
    "## Kural içermeyen notlar (bilet 04)\n\n"
    "Girdiler. Biçim: dosya adı · gerekçe.\n\n"
    "tweet-bir-1 · sohbet\ntweet-iki-2 · haber\n\n"
    "## Kısa atıfların tam adları\n\ntweet-bir-1\n"
)


def _kok(tmp_path, e=E_METNI, kurallar=KURALLAR_METNI, eol="\n"):
    (tmp_path / "docs" / "kurallar").mkdir(parents=True)
    for yol, metin in (
        (tmp_path / "docs" / "kurallar" / "E-risk.md", e),
        (tmp_path / "docs" / "KURALLAR.md", kurallar),
    ):
        yol.write_bytes(metin.replace("\n", eol).encode("utf-8"))
    return tmp_path


def _ek(not_adi, bolum, **ek):
    return {
        "not": not_adi,
        "sonuc": "ek",
        "dosya": "E",
        "bolum": bolum,
        "satir": "yeni satır.",
        **ek,
    }


def _oku(kok, ad):
    return (kok / ad).read_bytes().decode("utf-8")


E = "docs/kurallar/E-risk.md"
K = "docs/KURALLAR.md"


def test_ek_kaydi_var_olan_bloka_eklenir(tmp_path):
    kok = _kok(tmp_path)
    yol = _jsonl(
        tmp_path / "k.jsonl",
        _ek("tweet-yeni-2", "## K1. Stop", parametre="p = 1 (Ham)"),
        _ek("tweet-yeni-3", "## K1. Stop"),
    )
    assert parti_entegre([yol], kok, "16.10") == {E: 2}
    assert _oku(kok, E) == E_METNI.replace(
        "  - `tweet-eski-1` — eski satır.\n",
        "  - `tweet-eski-1` — eski satır.\n"
        "  - `tweet-yeni-2` — yeni satır. Parametre: p = 1 (Ham).\n"
        "  - `tweet-yeni-3` — yeni satır.\n",
    )


def test_ek_kaydi_blok_yoksa_bolum_sonunda_blok_acar(tmp_path):
    kok = _kok(tmp_path)
    yol = _jsonl(
        tmp_path / "k.jsonl",
        _ek("tweet-yeni-2", "## K2. Çıkış"),
        _ek("tweet-yeni-4", "## K3. Son"),
    )
    assert parti_entegre([yol], kok, "16.10") == {E: 2}
    assert _oku(kok, E) == E_METNI.replace(
        "- Kaynak güveni: orta\n",
        "- Kaynak güveni: orta\n- Ek kaynaklar (X arşivi, 16.10):\n  - `tweet-yeni-2` — yeni satır.\n",
    ).replace(
        "- Kaynak: z\n",
        "- Kaynak: z\n- Ek kaynaklar (X arşivi, 16.10):\n  - `tweet-yeni-4` — yeni satır.\n",
    )


def test_yok_kaydi_son_girdiden_sonra_gelir_giris_paragrafi_girdi_degildir(tmp_path):
    kok = _kok(tmp_path)
    yol = _jsonl(
        tmp_path / "k.jsonl",
        {"not": "tweet-uc-3", "sonuc": "yok", "neden": "vaat"},
        {"not": "tweet-dort-4", "sonuc": "yok", "neden": "eğitim"},
    )
    assert parti_entegre([yol], kok, "16.10") == {K: 2}
    assert _oku(kok, K) == KURALLAR_METNI.replace(
        "tweet-iki-2 · haber\n",
        "tweet-iki-2 · haber\ntweet-uc-3 · vaat\ntweet-dort-4 · eğitim\n",
    )


def test_crlf_dosya_crlf_kalir(tmp_path):
    kok = _kok(tmp_path, eol="\r\n")
    yol = _jsonl(
        tmp_path / "k.jsonl",
        _ek("tweet-yeni-2", "## K2. Çıkış"),
        {"not": "tweet-uc-3", "sonuc": "yok", "neden": "vaat"},
    )
    assert parti_entegre([yol], kok, "16.10") == {E: 1, K: 1}
    for ad in (E, K):
        metin = _oku(kok, ad)
        assert metin.count("\n") == metin.count("\r\n")
    assert "tweet-uc-3 · vaat\r\n" in _oku(kok, K)
    assert "  - `tweet-yeni-2` — yeni satır.\r\n" in _oku(kok, E)


def test_lf_dosya_lf_kalir(tmp_path):
    kok = _kok(tmp_path)
    yol = _jsonl(tmp_path / "k.jsonl", _ek("tweet-yeni-2", "## K2. Çıkış"))
    parti_entegre([yol], kok, "16.10")
    assert "\r" not in _oku(kok, E)


def test_ek_kaydinda_bolum_yoksa_hata(tmp_path):
    kok = _kok(tmp_path)
    yol = _jsonl(tmp_path / "k.jsonl", _ek("tweet-yeni-2", "## K9. Yok"))
    with pytest.raises(ValueError, match="K9"):
        parti_entegre([yol], kok, "16.10")
    assert _oku(kok, E) == E_METNI


def test_tekrar_calistirma_hicbir_sey_eklemez(tmp_path):
    kok = _kok(tmp_path)
    yol = _jsonl(
        tmp_path / "k.jsonl",
        _ek("tweet-yeni-2", "## K1. Stop"),
        _ek("tweet-yeni-4", "## K3. Son"),
        {"not": "tweet-uc-3", "sonuc": "yok", "neden": "vaat"},
    )
    assert parti_entegre([yol], kok, "16.10") == {E: 2, K: 1}
    once = (_oku(kok, E), _oku(kok, K))
    assert parti_entegre([yol], kok, "16.10") == {}
    assert (_oku(kok, E), _oku(kok, K)) == once


def test_bolumde_zaten_gecen_not_eklenmez_yeni_kaydi_atlanir(tmp_path):
    kok = _kok(tmp_path)
    yol = _jsonl(
        tmp_path / "k.jsonl",
        _ek("tweet-eski-1", "## K1. Stop"),
        {"not": "tweet-bir-1", "sonuc": "yok", "neden": "sohbet"},
        {"not": "tweet-yeni-7", "sonuc": "yeni", "dosya": "E", "satir": "x"},
    )
    assert parti_entegre([yol], kok, "16.10") == {}
    assert (_oku(kok, E), _oku(kok, K)) == (E_METNI, KURALLAR_METNI)


# --- komut satırı ---


def test_main_alinti_sorun_varsa_1_doner(tmp_path, capsys):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham="tamam")
    iyi = _jsonl(tmp_path / "iyi.jsonl", {"not": "tweet-a-1", "satir": 'a "tamam"'})
    kotu = _jsonl(tmp_path / "kotu.jsonl", {"not": "tweet-a-1", "satir": 'a "değil"'})
    assert main(["alinti", str(iyi)], havuz=havuz) == 0
    assert capsys.readouterr().out == ""
    assert main(["alinti", str(kotu)], havuz=havuz) == 1
    assert capsys.readouterr().out == "kotu.jsonl:1: tweet-a-1: değil\n"


def test_main_entegre_sayilari_yazar(tmp_path, capsys):
    kok = _kok(tmp_path)
    yol = _jsonl(tmp_path / "k.jsonl", _ek("tweet-yeni-2", "## K2. Çıkış"))
    assert main(["entegre", "16.10", str(yol)], kok=kok) == 0
    assert capsys.readouterr().out == f"{E}: 1\n"


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["bilinmeyen", "x"],
        ["alinti"],
        ["parti"],
        ["entegre"],
        ["entegre", "16.10"],
        ["alinti-belge"],
        ["alinti-belge", "a", "b"],
    ],
)
def test_main_girdi_dosyasi_yoksa_2_doner(tmp_path, capsys, argv):
    assert main(argv, havuz=tmp_path, kok=tmp_path) == 2
    atilan = capsys.readouterr()
    assert atilan.out == ""
    assert atilan.err.startswith("kullanım:")


@pytest.mark.parametrize(
    ("kayit", "alan"),
    [
        (_ek("tweet-yeni-2", "## K2. Çıkış", satir="iki\nsatır"), "satir"),
        (_ek("tweet-yeni-2", "## K2. Çıkış", parametre="p\r\nq"), "parametre"),
        ({"not": "tweet-uc-3", "sonuc": "yok", "neden": "iki\nsatır"}, "neden"),
    ],
)
def test_entegre_alani_satir_sonu_icerirse_hata(tmp_path, kayit, alan):
    kok = _kok(tmp_path, eol="\r\n")
    ilk = (_oku(kok, E), _oku(kok, K))
    yol = _jsonl(tmp_path / "k.jsonl", kayit)
    with pytest.raises(ValueError, match=alan):
        parti_entegre([yol], kok, "16.10")
    assert (_oku(kok, E), _oku(kok, K)) == ilk


# --- belge_alinti_sorunlari: son belgelerdeki alıntı atıf yapılan notta geçer ---

BELGE = (
    "# Belge\n"  # 1
    "## A bölümü\n"  # 2
    '- `tweet-a-1` — "Para yoksa gerisine bakmaya gerek yok" (Ham).\n'  # 3
    '- satırda not yok: "gerek yok" (Ham).\n'  # 4
    '- `tweet-b-2` — "para girişi esastır" (Ham).\n'  # 5
    '- `tweet-b-2` — "Para yoksa" (Ham).\n'  # 6
    "\n"  # 7
    "## B bölümü\n"  # 8
    '- yetim: "yetim alıntı"\n'  # 9
    "- alıntısız satır\n"  # 10
)


def _belge_havuzu(tmp_path):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham=HAM)
    _not(havuz, "tweet-b-2", ham="başka metin")
    belge = tmp_path / "k.md"
    belge.write_text(BELGE, encoding="utf-8")
    return havuz, belge


def test_belge_alinti_adaylari_satir_sonra_bolum(tmp_path):
    havuz, belge = _belge_havuzu(tmp_path)
    # 3: satır adayı; 4: satırda not yok, bölümdeki adaylar (a-1 alıntıyı taşır); 10: alıntı yok
    assert belge_alinti_sorunlari(havuz, belge, [3, 4, 10]) == []
    # 5: paraphrase; 6: satır adayı yalnız b-2, bölümdeki a-1 sayılmaz; 9: bölümde not adı yok
    assert belge_alinti_sorunlari(havuz, belge, [3, 4, 5, 6, 9, 10]) == [
        "k.md:5: para girişi esastır",
        "k.md:6: Para yoksa",
        "k.md:9: yetim alıntı",
    ]


def test_belge_alinti_yalniz_verilen_satirlar_ve_ileri_sira(tmp_path):
    havuz, belge = _belge_havuzu(tmp_path)
    assert belge_alinti_sorunlari(havuz, belge, [3, 99]) == []
    belge.write_text(
        '`tweet-a-1` "gerek yok … Aslolan" ve "Aslolan … gerek yok"\n', encoding="utf-8"
    )
    assert belge_alinti_sorunlari(havuz, belge, [1]) == ["k.md:1: gerek yok … Aslolan"]


def _belge_iki_satir(tmp_path, alinti_ilk, alinti_son, ham=HAM):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham=ham)
    belge = tmp_path / "k.md"
    belge.write_text(
        "## A\n"  # 1
        "- `tweet-a-1` — başlık\n"  # 2
        f'- önce "{alinti_ilk}\n'  # 3
        f'{alinti_son}" (Ham).\n'  # 4
        "- sonra\n",  # 5
        encoding="utf-8",
    )
    return havuz, belge


def test_belge_iki_satirli_alinti_kaynakta_yoksa_ilk_satirda_bildirilir(tmp_path):
    havuz, belge = _belge_iki_satir(tmp_path, "kaynakta", "yok")
    # alıntı 3-4. satırı kapsar: verilen satır ikisinden biri olsa yeter, bildirim ilk satırda
    assert belge_alinti_sorunlari(havuz, belge, [3]) == ["k.md:3: kaynakta yok"]
    assert belge_alinti_sorunlari(havuz, belge, [4]) == ["k.md:3: kaynakta yok"]
    assert belge_alinti_sorunlari(havuz, belge, [3, 4]) == ["k.md:3: kaynakta yok"]


def test_belge_iki_satirli_alinti_kaynaktaysa_gecer(tmp_path):
    havuz, belge = _belge_iki_satir(tmp_path, "Para yoksa", "gerisine bakmaya")
    assert belge_alinti_sorunlari(havuz, belge, [3, 4]) == []
    assert belge_alinti_sorunlari(havuz, belge, [4]) == []


def test_belge_alinti_verilen_satirlarin_disindaysa_denetlenmez(tmp_path):
    havuz, belge = _belge_iki_satir(tmp_path, "kaynakta", "yok")
    assert belge_alinti_sorunlari(havuz, belge, [1, 2, 5]) == []


def test_belge_alinti_adayi_alintinin_kapsadigi_satirlardir(tmp_path):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham=HAM)
    _not(havuz, "tweet-b-2", ham="başka metin")
    belge = tmp_path / "k.md"
    belge.write_text(
        "## A\n"  # 1
        "- `tweet-a-1` — başlık\n"  # 2
        '- `tweet-b-2` — "Para yoksa\n'  # 3
        'gerisine" (Ham).\n',  # 4
        encoding="utf-8",
    )
    # satır adayı yalnız b-2 (bölümdeki a-1 sayılmaz); 4. satırda not adı yok ama alıntı 3'ten başlar
    assert belge_alinti_sorunlari(havuz, belge, [4]) == ["k.md:3: Para yoksa gerisine"]


def _git(kok, *arg):
    subprocess.run(
        ["git", "-C", str(kok), "-c", "user.name=t", "-c", "user.email=t@t.t", *arg],
        check=True,
        capture_output=True,
    )


def test_main_alinti_belge_diffin_eklenen_satirlarini_denetler(tmp_path, capsys):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham="tamam")
    kok = tmp_path / "depo"
    (kok / "docs" / "kurallar").mkdir(parents=True)
    belge = kok / "docs" / "kurallar" / "E-x.md"

    def yaz(*alintilar):
        belge.write_bytes(
            "".join(f'- `tweet-a-1` — "{a}"\n' for a in alintilar).encode("utf-8")
        )

    yaz("eski kötü", "silinecek", "tamam", "tamam")
    _git(kok, "init", "-q")
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "x")
    # 2. satır silinir (saf silme bloğu: +1,0), sonuna kötü satır eklenir; eski kötü satır diffte değildir
    yaz("eski kötü", "tamam", "tamam", "yeni kötü")
    assert main(["alinti-belge", "HEAD"], havuz=havuz, kok=kok) == 1
    assert capsys.readouterr().out == "E-x.md:4: yeni kötü\n"
    _git(kok, "commit", "-q", "-a", "-m", "y")
    assert main(["alinti-belge", "HEAD"], havuz=havuz, kok=kok) == 0
    assert capsys.readouterr().out == ""


def test_main_alinti_belge_iki_satirli_alintiyi_denetler(tmp_path, capsys):
    havuz = tmp_path / "havuz"
    _not(havuz, "tweet-a-1", ham="tamam")
    kok = tmp_path / "depo"
    (kok / "docs" / "kurallar").mkdir(parents=True)
    belge = kok / "docs" / "kurallar" / "E-x.md"
    belge.write_bytes('- `tweet-a-1` — "tamam"\n'.encode("utf-8"))
    _git(kok, "init", "-q")
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "x")
    belge.write_bytes(
        '- `tweet-a-1` — "tamam"\n- `tweet-a-1` — "kaynakta\nyok" (Ham).\n'.encode(
            "utf-8"
        )
    )
    assert main(["alinti-belge", "HEAD"], havuz=havuz, kok=kok) == 1
    assert capsys.readouterr().out == "E-x.md:2: kaynakta yok\n"
