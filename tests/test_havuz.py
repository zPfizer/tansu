"""Havuz testi (bilet 08): beyindeki Tansu havuzunun her notu A–E'de atıflı ya da "kural içermez" listesinde.

Havuza yeni not gelince test kırmızı olur. Beyin yoksa (CI) atlanır, yerel test kapısı denetler.
Havuz yalnız okunur; test hiçbir şey yazmaz.
"""

import pytest

from atif_araclari import HAVUZ, KOK, kapsanmayan_notlar


def test_havuzdaki_her_not_atifli_ya_da_kural_icermez_listesinde():
    if not HAVUZ.exists():
        pytest.skip("Evde beyin havuzu yok.")
    assert kapsanmayan_notlar(KOK, HAVUZ) == []


def _depo(kok, kurallar, a):
    (kok / "docs" / "kurallar").mkdir(parents=True)
    (kok / "docs" / "KURALLAR.md").write_text(kurallar, encoding="utf-8")
    (kok / "docs" / "kurallar" / "A.md").write_text(a, encoding="utf-8")


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
    assert kapsanmayan_notlar(tmp_path, _havuz(tmp_path, NOTLAR)) == []


def test_yeni_not_gelince_kirmizi_olur(tmp_path):
    _depo(tmp_path, "## Kural içermeyen notlar\n", "G12\n")
    havuz = _havuz(tmp_path, NOTLAR[:1])
    assert kapsanmayan_notlar(tmp_path, havuz) == []
    (havuz / "gorsel-paket-99-yeni.md").write_text("not", encoding="utf-8")
    assert kapsanmayan_notlar(tmp_path, havuz) == ["gorsel-paket-99-yeni"]


def test_tam_ad_listesi_tek_basina_atif_sayilmaz(tmp_path):
    _depo(
        tmp_path,
        "## Kısa atıfların tam adları\n\ngorsel-paket-12-ad-bir\n",
        "G13\n",
    )
    assert kapsanmayan_notlar(tmp_path, _havuz(tmp_path, NOTLAR[:2])) == [
        "gorsel-paket-12-ad-bir"
    ]


def test_kisa_ad_uzun_adin_basi_degilse_kapsamaz(tmp_path):
    # `tweet-atr-risk-butcesi` yazılı; `tweet-atr` adlı not ayrıca atıf ister.
    _depo(tmp_path, "## X\n", "tweet-atr-risk-butcesi G12\n")
    havuz = _havuz(
        tmp_path, ["tweet-atr", "tweet-atr-risk-butcesi", "gorsel-paket-12-a"]
    )
    assert kapsanmayan_notlar(tmp_path, havuz) == ["tweet-atr"]
