"""Havuz testi (bilet 08): beyindeki Tansu havuzunun her notu A–E'de atıflı ya da "kural içermez" listesinde.

Havuza yeni not gelince test kırmızı olur. Beyin yoksa (CI) atlanır, yerel test kapısı denetler.
Havuz yalnız okunur; test hiçbir şey yazmaz.

Parti işi sırasında iki ortam değişkeni testi ayarlar (parti işi bitince ikisi de boş kalır):
- `TANSU_BEKLENEN_ACIK=<n>`: havuzda henüz atıfsız `n` not beklenir (varsayılan 0: hiç not açık olamaz).
  `n` > 0 iken test, açık not sayısının tam `n` olduğunu ve her açık maddenin düz not adı olduğunu
  ("belirsiz atıf" satırı olmadığını) denetler.
- `TANSU_PARTI=E09,E10`: virgüllü parti kimlikleri; her kimlik `PARTI_KLASORU/<kimlik>.txt` dosyasıdır.
  Bu dosyalardaki her not havuzda olmalı ve belgede atıfı olmalıdır (`parti_sorunlari`). Parti dosyası
  yoksa test kırmızı olur.
"""

import os

import pytest

from atif_araclari import (
    HAVUZ,
    KOK,
    PARTI_KLASORU,
    havuz_sorunlari,
    main,
    parti_sorunlari,
)


def test_havuzdaki_her_not_atifli_ya_da_kural_icermez_listesinde():
    if not HAVUZ.exists():
        pytest.skip("Evde beyin havuzu yok.")
    beklenen = int(os.environ.get("TANSU_BEKLENEN_ACIK", "0"))
    if beklenen == 0:
        assert havuz_sorunlari(KOK, HAVUZ) == []
    else:
        acik = havuz_sorunlari(KOK, HAVUZ)
        assert len(acik) == beklenen
        assert not [s for s in acik if s.startswith("belirsiz atıf")]
    kimlikler = [k.strip() for k in os.environ.get("TANSU_PARTI", "").split(",")]
    dosyalar = [PARTI_KLASORU / f"{k}.txt" for k in kimlikler if k]
    if dosyalar:
        assert parti_sorunlari(KOK, HAVUZ, dosyalar) == []


def _depo(kok, kurallar, a):
    (kok / "docs" / "kurallar").mkdir(parents=True)
    (kok / "docs" / "KURALLAR.md").write_text(kurallar, encoding="utf-8")
    (kok / "docs" / "kurallar" / "A-x.md").write_text(a, encoding="utf-8")


def _havuz(kok, adlar):
    havuz = kok / "havuz"
    havuz.mkdir()
    for ad in adlar:
        (havuz / f"{ad}.md").write_text("not", encoding="utf-8")
    return havuz


NOTLAR = [
    "gorsel-paket-12-ad-bir",
    "gorsel-paket-13-ad-iki",
    "gorsel-paket-14-ad-uc",
    "gorsel-paket-15-ad-dort",
    "gorsel-paket-16-ad-bes",
    "tweet-atr-risk-butcesi",
    "kaynak-akfis-retest-2095",
    "not-bir",
    "tweet-liste-notu",
]


def test_her_atif_bicimi_notu_kapsar(tmp_path):
    _depo(
        tmp_path,
        "## Kural içermeyen notlar\n\ntweet-liste-notu · kural yok\n\n"
        "## Kısa atıfların tam adları\n\n" + "\n".join(NOTLAR) + "\n",
        "G12, gp-13, G-14, gorsel-paket-15, T-atr, kaynak-akfis-retest, `not-bir.md`, x -16 (`a.png`)\n",
    )
    assert havuz_sorunlari(tmp_path, _havuz(tmp_path, NOTLAR)) == []


def test_yeni_not_gelince_kirmizi_olur(tmp_path):
    _depo(tmp_path, "## Kural içermeyen notlar\n", "G12\n")
    havuz = _havuz(tmp_path, NOTLAR[:1])
    assert havuz_sorunlari(tmp_path, havuz) == []
    (havuz / "gorsel-paket-99-yeni.md").write_text("not", encoding="utf-8")
    assert havuz_sorunlari(tmp_path, havuz) == ["gorsel-paket-99-yeni"]


def test_tam_ad_listesi_tek_basina_atif_sayilmaz(tmp_path):
    _depo(
        tmp_path,
        "## Kısa atıfların tam adları\n\ngorsel-paket-12-ad-bir\n",
        "G13\n",
    )
    assert havuz_sorunlari(tmp_path, _havuz(tmp_path, NOTLAR[:2])) == [
        "gorsel-paket-12-ad-bir"
    ]


def test_kisa_ad_uzun_adin_basi_degilse_kapsamaz(tmp_path):
    # `tweet-atr-risk-butcesi` yazılı; `tweet-atr` adlı not ayrıca atıf ister.
    _depo(tmp_path, "## X\n", "tweet-atr-risk-butcesi G12\n")
    havuz = _havuz(
        tmp_path, ["tweet-atr", "tweet-atr-risk-butcesi", "gorsel-paket-12-a"]
    )
    assert havuz_sorunlari(tmp_path, havuz) == ["tweet-atr"]


def test_belirsiz_kisa_ad_hatadir(tmp_path):
    # `T-atr` iki tweet notunun başı: hiçbirini kapsamaz, belirsiz atıf hatasıdır.
    _depo(tmp_path, "## X\n", "T-atr\n")
    havuz = _havuz(tmp_path, ["tweet-atr-risk-butcesi", "tweet-atr-yeni-not"])
    assert havuz_sorunlari(tmp_path, havuz) == [
        "belirsiz atıf tweet-atr: tweet-atr-risk-butcesi, tweet-atr-yeni-not",
        "tweet-atr-risk-butcesi",
        "tweet-atr-yeni-not",
    ]


def test_ayni_numarali_iki_not_belirsizdir(tmp_path):
    _depo(tmp_path, "## X\n", "G12 gorsel-paket-12-ad-bir\n")
    havuz = _havuz(tmp_path, ["gorsel-paket-12-ad-bir", "gorsel-paket-12-yeni-not"])
    assert havuz_sorunlari(tmp_path, havuz) == [
        "belirsiz atıf gorsel-paket-12: gorsel-paket-12-ad-bir, gorsel-paket-12-yeni-not",
        "gorsel-paket-12-yeni-not",
    ]


def test_tam_ad_belirsiz_kisa_adi_cozer(tmp_path):
    # Tam ad ya da tam kısa ad (`tweet-atr` adlı not var) tek nota gider.
    _depo(tmp_path, "## X\n", "tweet-atr tweet-atr-risk-butcesi\n")
    havuz = _havuz(tmp_path, ["tweet-atr", "tweet-atr-risk-butcesi"])
    assert havuz_sorunlari(tmp_path, havuz) == []


@pytest.mark.parametrize(
    ("notlar", "metin"),
    [
        # tam adlardaki numara kısa atıf sayılmaz (aynı sayısal değer: 1 ve 01)
        (
            ["gorsel-paket-1-ad-a", "gorsel-paket-01-ad-b"],
            "gorsel-paket-1-ad-a gorsel-paket-01-ad-b",
        ),
        (["kaynak-x-123", "kaynak-x-456"], "`kaynak-x-123.md` `kaynak-x-456.md`"),
        (["tweet-atr", "tweet-atr-risk"], "tweet-atr, tweet-atr-risk"),
        (["gorsel-paket-12-ad-bir"], "assets/gorsel-paket-12-ad-bir/g.png"),
        (
            ["gorsel-paket-12-ad-bir", "gorsel-paket-13-ad-iki"],
            "gorsel-paket-12-ad-bir -13-ad",
        ),
    ],
)
def test_tam_adlar_kisa_atif_olarak_yeniden_okunmaz(tmp_path, notlar, metin):
    _depo(tmp_path, "## X\n", metin + "\n")
    assert havuz_sorunlari(tmp_path, _havuz(tmp_path, notlar)) == []


def test_tam_ad_ve_ayni_numaraya_kisa_atif_belirsizdir(tmp_path):
    _depo(tmp_path, "## X\n", "gorsel-paket-12-ad-bir G12\n")
    havuz = _havuz(tmp_path, ["gorsel-paket-12-ad-bir", "gorsel-paket-012-yeni"])
    assert havuz_sorunlari(tmp_path, havuz) == [
        "belirsiz atıf gorsel-paket-12: gorsel-paket-012-yeni, gorsel-paket-12-ad-bir",
        "gorsel-paket-012-yeni",
    ]


@pytest.mark.parametrize(
    ("not_adi", "metin"),
    [
        ("kaynak-a-b-123", "kaynak-a-b-12"),  # kesik numara
        ("kaynak-a-b-123", "kaynak-a-b-1"),
        ("kaynak-abc-1", "kaynak-ab"),  # kelime ortasında kesik
        ("gorsel-paket-01-x", "gorsel-paket-0 ve G0 ve gp-0"),
        ("gorsel-paket-12-x", "gorsel-paket-1 ve G1 ve gp-1 ve -1"),
        ("gorsel-paket-12-x", "gorsel-paket-123 ve G123"),
        ("tweet-atrx-y", "T-atr"),
        ("tweet-atr-risk", "tweet-atr-ris"),
    ],
)
def test_kesik_kimlik_notu_kapsamaz(tmp_path, not_adi, metin):
    _depo(tmp_path, "## X\n", metin + "\n")
    assert havuz_sorunlari(tmp_path, _havuz(tmp_path, [not_adi])) == [not_adi]


def _kurallar_depo(kok, kurallar, dosyalar):
    (kok / "docs" / "kurallar").mkdir(parents=True)
    (kok / "docs" / "KURALLAR.md").write_text(kurallar, encoding="utf-8")
    for ad, metin in dosyalar.items():
        (kok / "docs" / "kurallar" / ad).write_text(metin, encoding="utf-8")


@pytest.mark.parametrize(
    ("kurallar", "dosyalar", "kapsanir"),
    [
        # yalnız "Kural içermeyen notlar" bölümü sayılır
        ("## Kural içermeyen notlar\n\nnot-bir · kural yok\n", {}, True),
        ("## İnceleme bekliyor\n\nnot-bir\n", {}, False),
        ("## Dizin\n\nnot-bir\n\n## Kural içermeyen notlar\n\nx\n", {}, False),
        ("## Kural içermeyen notlar\n\nx\n\n## Sonraki bölüm\n\nnot-bir\n", {}, False),
        ("## Kural içermeyen notlar\n\n### Alt başlık\n\nnot-bir\n", {}, True),
        ("## Kural içermeyen notlar\n\nx\n\n## Sonraki\n", {"A-x.md": "not-bir"}, True),
        # A–E dosyalarındaki okuma atıfları sayılır; başka dosyalar sayılmaz
        ("## X\n", {"B-y.md": "# B\n\nnot-bir", "E-z.md": "x"}, True),
        ("## X\n", {"Z-y.md": "not-bir"}, False),
        ("## X\n", {"notlar.md": "not-bir"}, False),
        ("## X\n", {"a-x.md": "not-bir"}, False),
        # tam adlar bölümü (kısa atıf listesi) sayılmaz
        ("## Kısa atıfların tam adları\n\nnot-bir\n", {}, False),
    ],
)
def test_havuz_kapsami_yalniz_a_e_ve_kural_icermez_listesidir(
    tmp_path, kurallar, dosyalar, kapsanir
):
    _kurallar_depo(tmp_path, kurallar, dosyalar)
    sonuc = havuz_sorunlari(tmp_path, _havuz(tmp_path, ["not-bir"]))
    assert sonuc == ([] if kapsanir else ["not-bir"])


def _parti(kok, *satirlar, ad="E99.txt"):
    yol = kok / ad
    yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    return yol


def test_parti_sorunlari_acik_ve_havuzda_olmayan_notlari_verir(tmp_path):
    # `not-bir` atıflı; `not-iki` açık; `not-uc` havuzda yok. Havuzdaki öbür açık not (`not-dis`) partide
    # değilse parti sorunu değildir.
    _depo(tmp_path, "## X\n", "`not-bir.md`\n")
    havuz = _havuz(tmp_path, ["not-bir", "not-iki", "not-dis"])
    parti = _parti(tmp_path, "not-bir", "", "not-iki  ", "not-uc")
    assert parti_sorunlari(tmp_path, havuz, [parti]) == [
        "E99.txt: not-iki: belgede atıf yok",
        "E99.txt: not-uc: havuzda yok",
    ]


def test_parti_sorunlari_temiz_parti_bos_doner(tmp_path):
    _depo(tmp_path, "## X\n", "`not-bir.md` `not-iki.md`\n")
    havuz = _havuz(tmp_path, ["not-bir", "not-iki", "not-dis"])
    parti = _parti(tmp_path, "not-bir", "not-iki")
    assert parti_sorunlari(tmp_path, havuz, [parti]) == []


def test_parti_sorunlari_belirsiz_atif_partinin_notunu_acik_saymaz(tmp_path):
    # `T-atr` iki nota gider: belirsiz atıf satırı düz not adı değildir, parti sorunu sayılmaz.
    _depo(tmp_path, "## X\n", "T-atr `not-bir.md`\n")
    havuz = _havuz(tmp_path, ["tweet-atr-a", "tweet-atr-b", "not-bir"])
    parti = _parti(tmp_path, "not-bir")
    assert parti_sorunlari(tmp_path, havuz, [parti]) == []


def test_parti_dosyasi_yoksa_hata(tmp_path):
    _depo(tmp_path, "## X\n", "x\n")
    with pytest.raises(FileNotFoundError):
        parti_sorunlari(tmp_path, _havuz(tmp_path, ["not-bir"]), [tmp_path / "yok.txt"])


def test_main_parti_sorun_varsa_1_doner(tmp_path, capsys):
    _depo(tmp_path, "## X\n", "`not-bir.md`\n")
    havuz = _havuz(tmp_path, ["not-bir", "not-iki"])
    iyi = _parti(tmp_path, "not-bir", ad="iyi.txt")
    kotu = _parti(tmp_path, "not-iki", ad="kotu.txt")
    assert main(["parti", str(iyi)], havuz=havuz, kok=tmp_path) == 0
    assert capsys.readouterr().out == ""
    assert main(["parti", str(kotu)], havuz=havuz, kok=tmp_path) == 1
    assert capsys.readouterr().out == "kotu.txt: not-iki: belgede atıf yok\n"


def test_main_acik_sayi_acik_not_sayisini_yazar(tmp_path, capsys):
    # Kapı bu sayıyı TANSU_BEKLENEN_ACIK olarak kullanır. Üç nottan yalnız G12 atıflı: 2 açık.
    _depo(tmp_path, "## X\n", "G12\n")
    havuz = _havuz(tmp_path, NOTLAR[:3])
    assert main(["acik-sayi"], havuz=havuz, kok=tmp_path) == 0
    assert capsys.readouterr().out == "2\n"


@pytest.mark.parametrize(
    ("metin", "beklenen"),
    [
        (
            "## Okunmayanlar / kısmen okunanlar\n- Okunmadı (yalnız adı veya görseli): `not-bir`\n",
            "1\n",
        ),
        ("## Okunmayanlar / kısmen okunanlar\n### Liste\n- `not-bir`\n", "1\n"),
        ("- Okunmadı: `not-bir`\n", "1\n"),
        ("- Okunmadı (yalnız adı veya görseli):\n  `not-bir`\n", "1\n"),
        (
            "## Okunmayanlar / kısmen okunanlar\n- Başka not\n## Okuma\n`not-bir`\n",
            "0\n",
        ),
        (
            "## Okunmayanlar / kısmen okunanlar\n- Başka not\n# Okuma\n`not-bir`\n",
            "0\n",
        ),
        ("## Okunmayanlar / kısmen okunanlar hakkında\n`not-bir`\n", "0\n"),
        ("- `not-bir` — İki görsel açıldı; sayısal eşik okunmadı.\n", "0\n"),
        ("- Okunmadığı yer: `not-bir`\n", "0\n"),
        ("- Okunmadı: `not-bir`\n- Okundu: `not-bir`\n", "0\n"),
    ],
)
def test_main_acik_sayi_okunmayan_listesi_atif_sayilmaz(
    tmp_path, capsys, metin, beklenen
):
    _depo(tmp_path, "## X\n", metin)
    havuz = _havuz(tmp_path, ["not-bir"])
    assert main(["acik-sayi"], havuz=havuz, kok=tmp_path) == 0
    assert capsys.readouterr().out == beklenen


def test_main_acik_sayi_havuz_yoksa_hata_verir(tmp_path, capsys):
    yok = tmp_path / "yok-havuz"
    assert main(["acik-sayi"], havuz=yok, kok=tmp_path) == 1
    cikti = capsys.readouterr()
    assert cikti.out == ""
    assert cikti.err != ""


def test_main_acik_sayi_hepsi_atifliysa_sifir_yazar(tmp_path, capsys):
    _depo(tmp_path, "## X\n", "G12 G13\n")
    havuz = _havuz(tmp_path, NOTLAR[:2])
    assert main(["acik-sayi"], havuz=havuz, kok=tmp_path) == 0
    assert capsys.readouterr().out == "0\n"
