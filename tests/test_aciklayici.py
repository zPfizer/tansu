"""Modül 1 açıklayıcısının okuyucuya görünen sözleşmesi (#72)."""

from html.parser import HTMLParser
from pathlib import Path


class Sayfa(HTMLParser):
    def __init__(self):
        super().__init__()
        self.govdede = False
        self.baslikta = False
        self.metin = []
        self.basliklar = []
        self.bolumler = []
        self.dis_kaynaklar = []

    def handle_starttag(self, tag, attrs):
        alanlar = dict(attrs)
        if tag == "body":
            self.govdede = True
        if tag == "h2":
            self.baslikta = True
        if tag == "section":
            self.bolumler.append(alanlar.get("id"))
        if tag in ("script", "link", "iframe") or "src" in alanlar:
            self.dis_kaynaklar.append(tag)

    def handle_endtag(self, tag):
        if tag == "body":
            self.govdede = False
        if tag == "h2":
            self.baslikta = False

    def handle_data(self, data):
        if self.govdede:
            self.metin.append(data)
        if self.baslikta:
            self.basliklar.append(data.strip())


def test_modul1_aciklayici_bolumleri_ve_sade_metin():
    yol = Path(__file__).resolve().parents[1] / "docs/aciklayici/modul-1.html"
    assert yol.is_file(), "Modül 1 açıklayıcı sayfası yok"
    # Strict UTF-8 decoding also rejects damaged Turkish bytes.
    html = yol.read_text(encoding="utf-8")
    sayfa = Sayfa()
    sayfa.feed(html)
    sayfa.close()
    assert sayfa.basliklar == [
        "Veri",
        "Aday seçimi",
        "Giriş kuralları",
        "Stop: zararı kesme seviyesi",
        "Hedefler",
        "Pozisyon büyüklüğü: kaç hisse alınır?",
        "Çıkış",
        "24 seçenek",
        "Raporlar",
    ]
    assert sayfa.bolumler == [
        "veri",
        "aday",
        "giris",
        "stop",
        "hedef",
        "buyukluk",
        "cikis",
        "secenekler",
        "raporlar",
    ]
    assert not sayfa.dis_kaynaklar, "Sayfa dış kaynak olmadan açılmalı"
    gorunen = " ".join(sayfa.metin)
    for isaret in ("_", "/", "\\", ".py", ".md", ".html", "\ufffd"):
        assert isaret not in gorunen, (
            f"Görünen metinde teknik ad veya bozuk karakter: {isaret}"
        )
    assert "Modül 1" in gorunen
    assert "henüz yok" in gorunen
    assert "#76" in gorunen
    assert all(harf in gorunen for harf in "ı ş ğ ü ö ç İ ·".split())
