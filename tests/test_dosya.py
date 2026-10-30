import os

import pytest

from tansu import dosya


def test_atomik_basarida_hedefi_yazar_gecici_dosya_kalmaz(tmp_path):
    yol = tmp_path / "a.txt"
    yol.write_bytes(b"eski")
    with dosya.atomik(yol) as gecici:
        gecici.write_bytes(b"yeni")
    assert yol.read_bytes() == b"yeni"
    assert not list(tmp_path.glob("*.tmp"))


def test_atomik_blokta_hata_olursa_hedef_ayni_kalir_hata_gecer(tmp_path):
    yol = tmp_path / "a.txt"
    yol.write_bytes(b"eski")
    with pytest.raises(RuntimeError, match="yarıda"), dosya.atomik(yol) as gecici:
        gecici.write_bytes(b"yari")
        raise RuntimeError("yarıda")
    assert yol.read_bytes() == b"eski"
    assert not list(tmp_path.glob("*.tmp"))


def test_atomik_degistirme_reddedilirse_gecici_dosya_kalmaz_hata_gecer(
    tmp_path, monkeypatch
):
    yol = tmp_path / "a.txt"
    yol.write_bytes(b"eski")

    def reddet(kaynak, hedef):
        raise PermissionError("dosya başka programda açık")

    monkeypatch.setattr(os, "replace", reddet)
    with (
        pytest.raises(PermissionError, match="başka programda"),
        dosya.atomik(yol) as gecici,
    ):
        gecici.write_bytes(b"yeni")
    assert yol.read_bytes() == b"eski"
    assert not list(tmp_path.glob("*.tmp"))
