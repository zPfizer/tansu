import socket

import pytest


@pytest.fixture(autouse=True)
def ag_kapali(monkeypatch):
    def engel(*a, **k):
        raise RuntimeError("testte ağ yok")

    monkeypatch.setattr(socket, "socket", engel)
    monkeypatch.setattr(socket, "create_connection", engel)
