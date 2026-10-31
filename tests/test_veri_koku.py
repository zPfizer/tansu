import datetime as dt
import msvcrt
import os
from pathlib import Path

import pytest

from tansu import kaynak, veri
from tansu.__main__ import ayristirici, main, son_anlik, veri_koku
from tests.test_veri_gunluk import SahteKaynak


@pytest.fixture
def olmayan_kok(monkeypatch, tmp_path):
    kok = tmp_path / "yok"
    monkeypatch.setenv("TANSU_VERI", str(kok))
    monkeypatch.setattr(
        kaynak, "kapanan_kodlar", lambda: pytest.fail("indirme denendi")
    )
    return kok


def test_sina_kok_yoksa_klasoru_adlandirip_1_doner_ve_klasor_acmaz(
    olmayan_kok, monkeypatch, tmp_path, capsys
):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "stratejiler").mkdir()
    (tmp_path / "stratejiler" / "durum.csv").write_text(
        "ad,durum,tarih,not\ngartley,taslak,2026-10-26,\n", encoding="utf-8"
    )
    assert main(["sina", "gartley"]) == 1
    hata = capsys.readouterr().err
    assert str(olmayan_kok) in hata and "TANSU_VERI" in hata
    assert not olmayan_kok.exists()


def test_veri_kok_yoksa_indirmeden_1_doner_ve_klasor_acmaz(olmayan_kok, capsys):
    assert main(["veri"]) == 1
    hata = capsys.readouterr().err
    assert str(olmayan_kok) in hata and "TANSU_VERI" in hata
    assert not olmayan_kok.exists()


def test_ikinci_veri_kosusu_kilitte_durur_goruntu_yazmaz(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("TANSU_VERI", str(tmp_path))
    monkeypatch.setattr(
        kaynak, "kapanan_kodlar", lambda: pytest.fail("indirme denendi")
    )
    tutamak = os.open(tmp_path / "tansu-veri.kilit", os.O_RDWR | os.O_CREAT)
    msvcrt.locking(tutamak, msvcrt.LK_NBLCK, 1)
    try:
        assert main(["veri"]) == 1
    finally:
        msvcrt.locking(tutamak, msvcrt.LK_UNLCK, 1)
        os.close(tutamak)
    assert (
        f"başka bir `tansu veri` koşusu sürüyor: {tmp_path}" in capsys.readouterr().err
    )
    assert not (tmp_path / "ag").exists()


def test_kok_verilmeyen_komut_ortak_kokteki_en_yeni_goruntuyu_okur(
    monkeypatch, tmp_path
):
    monkeypatch.setenv("TANSU_VERI", str(tmp_path))
    for gun in (dt.datetime(2024, 2, 1, 18, 0), dt.datetime(2024, 1, 1, 18, 0)):
        veri.indir(["AKBNK"], tmp_path, SahteKaynak(), simdi=gun)
    a = ayristirici().parse_args(["sina", "gartley"])
    assert son_anlik(a.kok).kimlik == "20240201-1800"


def test_ortam_degiskeni_yoksa_kok_masaustundeki_tansu_veri(monkeypatch, tmp_path):
    monkeypatch.delenv("TANSU_VERI")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert veri_koku() == tmp_path / "Desktop" / "TANSU-veri"


def test_suren_veri_kosusunun_yarim_goruntusu_okunmaz(tmp_path):
    veri.indir(["AKBNK"], tmp_path, SahteKaynak(), simdi=dt.datetime(2024, 1, 1, 18, 0))
    yarim = tmp_path / "ag" / "_gecici-20990101-0000"
    yarim.mkdir()
    (yarim / "fiyat.parquet").write_bytes(b"yarim")
    assert son_anlik(tmp_path).kimlik == "20240101-1800"
