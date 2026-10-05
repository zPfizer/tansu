import socket

import pytest

from tansu import denetim, kayit, rapor


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


@pytest.fixture(autouse=True)
def rapor_yonlendir(monkeypatch, tmp_path):
    """Gerçek `rapor/` klasörüne yazılmaz."""
    monkeypatch.setattr(rapor, "RAPOR_DIZINI", tmp_path / "rapor")


@pytest.fixture(autouse=True)
def docs_yonlendir(monkeypatch, tmp_path):
    """Gerçek `docs/denetim.md` dosyasına yazılmaz."""
    monkeypatch.setattr(denetim, "DOCS", tmp_path / "docs")
