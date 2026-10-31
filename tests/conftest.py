import socket

import pytest

from tansu import __main__ as komut
from tansu import ayar
from tansu.__main__ import veri_koku


@pytest.fixture(scope="session")
def gercek_veri():
    return veri_koku()


@pytest.fixture(autouse=True)
def gecici_veri_koku(monkeypatch, tmp_path_factory):
    monkeypatch.setenv("TANSU_VERI", str(tmp_path_factory.mktemp("veri")))


@pytest.fixture(autouse=True)
def gecici_proje(monkeypatch, tmp_path):
    """`main` durum.csv, ayar ve raporu deponun yerine testin klasöründe okur ve yazar."""
    monkeypatch.setattr(komut, "PROJE", tmp_path)


@pytest.fixture(autouse=True)
def tek_isci(monkeypatch):
    monkeypatch.setattr(ayar, "ISCI", 1)


@pytest.fixture(autouse=True)
def ag_kapali(monkeypatch):
    def engel(*a, **k):
        raise RuntimeError("testte ağ yok")

    monkeypatch.setattr(socket, "socket", engel)
    monkeypatch.setattr(socket, "create_connection", engel)
