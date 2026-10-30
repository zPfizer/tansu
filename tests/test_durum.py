import datetime as dt

import pytest

from tansu import durum, veri

SATIRLAR = [
    {"ad": "a", "durum": "taslak", "tarih": "2026-10-26", "not": ""},
    {"ad": "b", "durum": "beklemede", "tarih": "2026-10-26", "not": ""},
    {"ad": "c", "durum": "sinyalde", "tarih": "2026-10-26", "not": ""},
]


@pytest.mark.parametrize("puanli", [True, False])
@pytest.mark.parametrize(
    ("komut", "eski", "beklenen"),
    [
        ("sina", "taslak", "sinandi"),
        ("sina", "beklemede", "beklemede"),
        ("sina", "sinandi", "sinandi"),
        ("sina", "ayarlandi", "ayarlandi"),
        ("sina", "yetersiz-ornek", "yetersiz-ornek"),
        ("sina", "sinyalde", "sinyalde"),
        ("sina", "bozuk", "bozuk"),
        ("ayarla", "taslak", None),
        ("ayarla", "beklemede", "beklemede"),
        ("ayarla", "sinandi", None),
        ("ayarla", "ayarlandi", None),
        ("ayarla", "yetersiz-ornek", None),
        ("ayarla", "sinyalde", None),
        ("ayarla", "bozuk", "bozuk"),
    ],
)
def test_sonraki_komut_ve_eski_duruma_gore_secer(komut, eski, beklenen, puanli):
    if beklenen is None:
        beklenen = "ayarlandi" if puanli else "yetersiz-ornek"
    assert durum.sonraki(komut, eski, puanli) == beklenen


def test_durumlar_listesi_degismedi():
    assert durum.DURUMLAR == (
        "taslak",
        "beklemede",
        "sinandi",
        "ayarlandi",
        "yetersiz-ornek",
        "sinyalde",
    )


@pytest.mark.parametrize("komut", ["sina", "ayarla"])
@pytest.mark.parametrize("eski", [*durum.DURUMLAR, "bozuk"])
def test_reddeder_ve_yeniden_onay_yalniz_ayarla_icin(komut, eski):
    ayarla = komut == "ayarla"
    assert durum.reddeder(komut, eski) is (ayarla and eski == "beklemede")
    assert durum.yeniden_onay(komut, eski) is (ayarla and eski == "sinyalde")


def test_sinanan_taslak_ve_beklemede_disindakini_ve_adi_sayar():
    assert durum.sinanan(SATIRLAR, "x") == 1
    assert durum.sinanan(SATIRLAR, "a") == 2
    assert durum.sinanan(SATIRLAR, "b") == 2
    assert durum.sinanan([], "a") == 0


def test_durumu_olmayan_adi_veri_hatasi_ile_reddeder():
    assert durum.durumu(SATIRLAR, "c") == "sinyalde"
    with pytest.raises(veri.VeriHatasi, match="yok: durum.csv içinde yok"):
        durum.durumu(SATIRLAR, "yok")


def test_gec_yalniz_hedef_satiri_yazar_diger_baytlari_korur(tmp_path):
    yol = tmp_path / "durum.csv"
    yol.write_bytes(
        b"ad,durum,tarih,not\n"
        b"a,taslak,2026-10-26,\n"
        b'b,beklemede,2026-10-25,"not, virg\xc3\xbcll\xc3\xbc"\n'
    )
    bugun = dt.date.today().isoformat()
    assert durum.gec("a", "sina", puanli=False, yol=yol) == "sinandi"
    assert yol.read_bytes() == (
        b"ad,durum,tarih,not\n"
        + f"a,sinandi,{bugun},\n".encode()
        + b'b,beklemede,2026-10-25,"not, virg\xc3\xbcll\xc3\xbc"\n'
    )


def test_gec_gecis_disindaki_durumda_dosyayi_yazmaz(tmp_path):
    yol = tmp_path / "durum.csv"
    baytlar = b"ad,durum,tarih,not\r\nb,beklemede,2026-10-25,\r\n"
    yol.write_bytes(baytlar)
    assert durum.gec("b", "ayarla", puanli=True, yol=yol) == "beklemede"
    assert yol.read_bytes() == baytlar


def test_gec_ayarlandiyi_yeniden_ayarlayinca_tarihi_yeniler(tmp_path):
    yol = tmp_path / "durum.csv"
    yol.write_bytes(b"ad,durum,tarih,not\na,ayarlandi,2026-01-01,\n")
    assert durum.gec("a", "ayarla", puanli=False, yol=yol) == "yetersiz-ornek"
    assert yol.read_bytes().endswith(
        f"a,yetersiz-ornek,{dt.date.today().isoformat()},\n".encode()
    )


def test_gec_olmayan_adi_veri_hatasi_ile_reddeder(tmp_path):
    yol = tmp_path / "durum.csv"
    yol.write_bytes(b"ad,durum,tarih,not\na,taslak,2026-10-26,\n")
    with pytest.raises(veri.VeriHatasi, match="yok: durum.csv içinde yok"):
        durum.gec("yok", "sina", puanli=True, yol=yol)
