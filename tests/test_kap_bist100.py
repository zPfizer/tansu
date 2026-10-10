"""Dondurulmus KAP BIST100 dosyasinin sozlesmesi (bilet 16). Ag yok; yalniz depodaki CSV okunur."""

import csv
from pathlib import Path

KLASOR = Path(__file__).resolve().parent.parent / "docs" / "arastirma"


def oku(ad):
    with open(KLASOR / ad, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def test_basliklar_ve_kaynak_baglantisi():
    satirlar = oku("bist100_kap_degisiklik.csv")
    assert list(satirlar[0]) == ["tarih", "sembol", "yon", "duyuru_tarihi", "kaynak"]
    assert all(s["kaynak"].startswith("https://") for s in satirlar)


def test_kirk_iki_donem_ve_dengeli_giris_cikis():
    satirlar = [s for s in oku("bist100_kap_degisiklik.csv") if s["yon"] != "taban"]
    donemler = sorted({s["tarih"] for s in satirlar})
    assert len(donemler) == 42
    assert donemler[0] == "2016-07-01"
    assert donemler[-1] == "2026-10-01"
    for d in donemler:
        giris = [s for s in satirlar if s["tarih"] == d and s["yon"] == "giris"]
        cikis = [s for s in satirlar if s["tarih"] == d and s["yon"] == "cikis"]
        assert len(giris) == len(cikis) > 0


def test_taban_yuz_hisse_ve_son_donem_taban_ile_uyumlu():
    satirlar = oku("bist100_kap_degisiklik.csv")
    taban = {s["sembol"] for s in satirlar if s["yon"] == "taban"}
    assert len(taban) == 100
    son = [s for s in satirlar if s["tarih"] == "2026-10-01" and s["yon"] != "taban"]
    assert len([s for s in son if s["yon"] == "giris"]) == 27
    assert all(s["sembol"] in taban for s in son if s["yon"] == "giris")
    assert not any(s["sembol"] in taban for s in son if s["yon"] == "cikis")


def test_bosluklar_isaretli():
    b = oku("bist100_kap_bosluk.csv")
    assert list(b[0]) == ["baslangic", "bitis", "sembol", "neden"]
    assert any(r["baslangic"] == "2015-01-01" and r["bitis"] == "2016-06-30" for r in b)
    assert any(r["sembol"] == "IPEKE" for r in b)
