import socket

import pytest

from tansu import kayit


@pytest.fixture(autouse=True)
def ag_kapali(monkeypatch):
    def engel(*a, **k):
        raise RuntimeError("testte ağ yok")

    monkeypatch.setattr(socket, "socket", engel)
    monkeypatch.setattr(socket, "create_connection", engel)


@pytest.fixture(autouse=True)
def kayit_yonlendir(monkeypatch, tmp_path):
    """Gerçek `kayit/` dosyalarına yazılmaz (AGENTS test kapısı)."""
    monkeypatch.setattr(kayit, "KAYIT_DIZINI", tmp_path / "kayit")
