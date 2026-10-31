import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest

from tansu import veri
from tansu.__main__ import main

KORUNAN, ARA, SON = "20260101-1800", "20260102-1800", "20260103-1800"


def goruntu(kok, kimlik):
    klasor = kok / "ag" / kimlik
    klasor.mkdir(parents=True)
    (klasor / "fiyat.parquet").write_bytes(f"fiyat {kimlik}".encode())
    ozet = hashlib.sha256((klasor / "fiyat.parquet").read_bytes()).hexdigest()
    (klasor / "manifest.json").write_text(
        json.dumps({"kimlik": kimlik, "dosyalar": {"fiyat.parquet": ozet}}),
        encoding="utf-8",
    )


@pytest.fixture
def kurulum(tmp_path):
    """`tmp_path` PROJE'dir (conftest); ayar KORUNAN'ı gösterir."""
    kaynak, yedek = tmp_path / "veri", tmp_path / "yedek"
    for kimlik in (KORUNAN, ARA, SON):
        goruntu(kaynak, kimlik)
    yedek.mkdir()
    ayarlar = tmp_path / "stratejiler" / "ayarlar"
    ayarlar.mkdir(parents=True)
    (ayarlar / "gartley.json").write_text(
        json.dumps({"veri_kimligi": KORUNAN}), encoding="utf-8"
    )
    return kaynak, yedek


def yedekle(kaynak, hedef):
    return main(["yedekle", str(hedef), "--kok", str(kaynak)])


def test_ayarin_ve_en_yeni_goruntuyu_yedekler_aradakini_almaz(kurulum, capsys):
    kaynak, yedek = kurulum
    assert yedekle(kaynak, yedek) == 0
    cikti = capsys.readouterr().out
    assert f"{KORUNAN}: kopyalandı" in cikti and f"{SON}: kopyalandı" in cikti
    assert sorted(p.name for p in (yedek / "ag").iterdir()) == [KORUNAN, SON]
    for kimlik in (KORUNAN, SON):
        veri.denetle(yedek / "ag" / kimlik, kimlik)


def test_ikinci_yedek_kopyalamaz_bozuk_yedegi_yeniden_kopyalar(kurulum, capsys):
    kaynak, yedek = kurulum
    assert yedekle(kaynak, yedek) == 0
    capsys.readouterr()
    assert yedekle(kaynak, yedek) == 0
    cikti = capsys.readouterr().out
    assert "kopyalandı" not in cikti
    assert f"{KORUNAN}: yedekte aynı" in cikti and f"{SON}: yedekte aynı" in cikti
    (yedek / "ag" / SON / "fiyat.parquet").write_bytes(b"bozuk")
    assert yedekle(kaynak, yedek) == 0
    cikti = capsys.readouterr().out
    assert f"{SON}: kopyalandı" in cikti and f"{KORUNAN}: yedekte aynı" in cikti
    veri.denetle(yedek / "ag" / SON, SON)


def test_bozuk_kaynak_eski_yedegin_yerine_gecmez(kurulum, capsys):
    kaynak, yedek = kurulum
    assert yedekle(kaynak, yedek) == 0
    eski = yedek / "ag" / SON / "fiyat.parquet"
    eski.write_bytes(b"eski bozuk yedek")
    (kaynak / "ag" / SON / "fiyat.parquet").write_bytes(b"bozuk kaynak")
    capsys.readouterr()
    assert yedekle(kaynak, yedek) == 1
    hata = capsys.readouterr().err
    assert len(hata.splitlines()) == 1
    assert hata.startswith(f"tansu yedekle: {SON}: manifest uyuşmuyor")
    assert eski.read_bytes() == b"eski bozuk yedek"
    veri.denetle(yedek / "ag" / KORUNAN, KORUNAN)
    assert not list((yedek / "ag").glob("_gecici-*"))


def test_hedef_klasor_yoksa_hicbir_sey_olusturmaz(kurulum, tmp_path, capsys):
    kaynak, _ = kurulum

    def dosyalar():  # kayit/ komut kaydıdır, yedek değil
        return sorted(p for p in tmp_path.rglob("*") if "kayit" not in p.parts)

    once = dosyalar()
    assert yedekle(kaynak, tmp_path / "takili-degil") == 1
    hata = capsys.readouterr().err
    assert len(hata.splitlines()) == 1 and "takili-degil" in hata
    assert dosyalar() == once


def test_geri_yukleme_ayni_komutla_roller_degisince_olur(kurulum, capsys):
    kaynak, yedek = kurulum
    assert yedekle(kaynak, yedek) == 0
    shutil.rmtree(kaynak / "ag" / KORUNAN)
    assert yedekle(yedek, kaynak) == 0
    assert f"{KORUNAN}: kopyalandı" in capsys.readouterr().out
    assert veri.denetle(kaynak / "ag" / KORUNAN, KORUNAN)["kimlik"] == KORUNAN


def test_kesilen_yer_degistirme_eski_yedegi_silmez(kurulum, monkeypatch, capsys):
    kaynak, yedek = kurulum
    assert yedekle(kaynak, yedek) == 0
    eski = yedek / "ag" / SON / "fiyat.parquet"
    eski.write_bytes(b"eski bozuk yedek")
    replace = os.replace

    def kesik(nereden, nereye):
        if Path(nereden).name.startswith("_gecici-"):
            raise OSError("elektrik kesildi")
        replace(nereden, nereye)

    monkeypatch.setattr(os, "replace", kesik)
    assert yedekle(kaynak, yedek) == 1
    assert "elektrik kesildi" in capsys.readouterr().err
    assert eski.read_bytes() == b"eski bozuk yedek"
    assert sorted(p.name for p in (yedek / "ag").iterdir()) == [KORUNAN, SON]


@pytest.mark.parametrize(
    "bozuk",
    [b'{"dosyalar": "\xff"}', b"[]", b"{}"],
    ids=["utf8 degil", "liste", "dosyalarsiz"],
)
def test_yedekteki_bozuk_manifest_yeniden_kopyalanir(kurulum, capsys, bozuk):
    kaynak, yedek = kurulum
    assert yedekle(kaynak, yedek) == 0
    (yedek / "ag" / SON / "manifest.json").write_bytes(bozuk)
    capsys.readouterr()
    assert yedekle(kaynak, yedek) == 0
    assert f"{SON}: kopyalandı" in capsys.readouterr().out
    veri.denetle(yedek / "ag" / SON, SON)


def test_kesilen_onceki_kosunun_artiklarini_toparlar(kurulum, capsys):
    kaynak, yedek = kurulum
    assert yedekle(kaynak, yedek) == 0
    ag = yedek / "ag"
    os.replace(ag / SON, ag / f"_eski-{SON}")
    shutil.copytree(kaynak / "ag" / SON, ag / f"_gecici-{SON}")
    capsys.readouterr()
    assert yedekle(kaynak, yedek) == 0
    assert f"{SON}: yedekte aynı" in capsys.readouterr().out
    assert sorted(p.name for p in ag.iterdir()) == [KORUNAN, SON]
