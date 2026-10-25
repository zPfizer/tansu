"""Komut çıkışı ve hata metni (TASARIM 4, sektör toplu okuma)."""

import datetime as dt
import json

import pytest

from tansu import __main__ as komut
from tansu import veri
from tansu.kaynak import KaynakHatasi
from tests.test_gunluk import fiyatlar
from tests.test_veri import SahteKaynak


@pytest.mark.parametrize("kesik", [False, True], ids=["tamam", "kesik"])
def test_sektor_indir_sonucu_komut_cikisina_tasinir(
    tmp_path, monkeypatch, capsys, kesik
):
    fiyat = {s: fiyatlar() for s in "ABCDEFG"}
    kimlik = veri.indir(
        list(fiyat),
        tmp_path,
        SahteKaynak(fiyat, {s: [] for s in fiyat}),
        simdi=dt.datetime(2026, 10, 5, 18, 0),
    )

    class SektorKaynak:
        def sektor(self, sembol):
            if kesik:
                raise KaynakHatasi("kayıtlı sağlayıcı hatası")
            return "Sanayi"

    monkeypatch.setattr(komut.kaynak, "KapSektor", SektorKaynak)
    assert komut.main(["sektor-indir", "--kok", str(tmp_path), "--kimlik", kimlik]) == (
        1 if kesik else 0
    )
    c = capsys.readouterr()
    if kesik:
        assert "Art arda hata, durdu (yeniden çalıştır)" in c.err
        assert "hedef 6, var 0, listede yok 0, alınamayan 6" in c.err
        assert len(list((tmp_path / "ag").iterdir())) == 1
    else:
        assert "Yeni anlık görüntü" in c.out
        assert "hedef 6, var 6, listede yok 0, alınamayan 0" in c.out
        yeni = next(p for p in (tmp_path / "ag").iterdir() if p.name != kimlik)
        assert json.loads((yeni / "sektor.json").read_text(encoding="utf-8")) == {
            s: "Sanayi" for s in "BCDEFG"
        }
