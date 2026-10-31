import json
import os
import sys
from pathlib import Path

import pytest

from tansu import durum
from tansu.__main__ import main


def test_yardim_alti_komutu_listeler(capsys):
    with pytest.raises(SystemExit) as cikis:
        main(["--help"])
    assert cikis.value.code == 0
    yardim = capsys.readouterr().out
    for komut in ("veri", "sina", "ayarla", "onayla", "tara", "durum", "yedekle"):
        assert komut in yardim


@pytest.fixture
def ayar_dosyasi(tmp_path):
    """`tmp_path` PROJE'dir (conftest): `gartley` ayarlı; dönen yol onun ayar dosyasıdır, henüz yazılmadı."""
    (tmp_path / "stratejiler" / "ayarlar").mkdir(parents=True)
    (tmp_path / "stratejiler" / "durum.csv").write_text(
        "ad,durum,tarih,not\ngartley,ayarlandi,2026-11-01,\n", encoding="utf-8"
    )
    return tmp_path / "stratejiler" / "ayarlar" / "gartley.json"


def arglar(komut, tmp_path):
    return {
        "sina": ["sina", "gartley"],
        "veri": ["veri"],
        "yedekle": ["yedekle", str(tmp_path)],
    }[komut]


def tek_satir(capsys, komut, *parcalar):
    hata = capsys.readouterr().err
    assert len(hata.splitlines()) == 1 and hata.startswith(f"tansu {komut}: "), hata
    assert all(str(p) in hata for p in parcalar), hata


@pytest.mark.parametrize("komut", ["sina", "veri", "yedekle"])
@pytest.mark.parametrize("bozuk", ["utf8 degil", "klasor"])
def test_okunamayan_ayar_dosyasi_tek_satir_hata_verir(
    ayar_dosyasi, tmp_path, capsys, komut, bozuk
):
    if bozuk == "klasor":
        ayar_dosyasi.mkdir()
    else:
        ayar_dosyasi.write_bytes(b'{"veri_kimligi": "\xff"}')
    assert main(arglar(komut, tmp_path)) == 1
    tek_satir(capsys, komut, ayar_dosyasi)


@pytest.mark.parametrize("komut", ["veri", "yedekle"])
@pytest.mark.parametrize(
    "kimlik",
    ["../disari", "20261028", "", 20261028],
    ids=["ust klasor", "saatsiz", "bos", "sayi"],
)
def test_gecersiz_veri_kimligi_dosyayi_soyler_ve_kopyalamaz(
    ayar_dosyasi, tmp_path, capsys, komut, kimlik
):
    ayar_dosyasi.write_text(json.dumps({"veri_kimligi": kimlik}), encoding="utf-8")
    goruntu = Path(os.environ["TANSU_VERI"]) / "ag" / "20260101-1800"
    goruntu.mkdir(parents=True)
    (goruntu / "manifest.json").write_text('{"dosyalar": {}}', encoding="utf-8")
    assert main(arglar(komut, tmp_path)) == 1
    tek_satir(capsys, komut, ayar_dosyasi, "veri_kimligi")
    assert not (tmp_path / "ag").exists()


def test_kayit_uyari_satirini_degil_hata_satirini_yazar(
    ayar_dosyasi, tmp_path, capsys, monkeypatch
):
    oku = durum.oku

    def uyarili(yol):
        print("pandas/core.py:1: FutureWarning: eski kullanım", file=sys.stderr)
        return oku(yol)

    monkeypatch.setattr(durum, "oku", uyarili)
    ayar_dosyasi.write_text("{bozuk", encoding="utf-8")
    assert main(["sina", "gartley"]) == 1
    uyari, hata = capsys.readouterr().err.splitlines()
    assert hata.startswith("tansu sina: ") and "FutureWarning" in uyari
    (satir,) = (
        (tmp_path / "kayit" / "tansu.log").read_text(encoding="utf-8").splitlines()
    )
    assert satir.endswith(hata)


def test_kayit_onekli_satir_yoksa_ilk_stderr_satirini_yazar(tmp_path, monkeypatch):
    def oneksiz(a):
        print("beklenmeyen hata", file=sys.stderr)
        return 1

    monkeypatch.setattr("tansu.__main__._sina", oneksiz)
    assert main(["sina", "gartley"]) == 1
    (satir,) = (
        (tmp_path / "kayit" / "tansu.log").read_text(encoding="utf-8").splitlines()
    )
    assert satir.endswith(" rc=1 goruntu=- beklenmeyen hata")
