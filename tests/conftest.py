import socket

import pytest

from tansu import ayar


@pytest.fixture(autouse=True)
def tek_isci(monkeypatch):
    monkeypatch.setattr(ayar, "ISCI", 1)


@pytest.fixture(autouse=True)
def ag_kapali(monkeypatch):
    def engel(*a, **k):
        raise RuntimeError("testte ağ yok")

    monkeypatch.setattr(socket, "socket", engel)
    monkeypatch.setattr(socket, "create_connection", engel)
