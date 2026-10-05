"""`sadakat` komutu: sahte KRDMD anlık görüntüsüyle, ağsız, aynı rakamları yeniden üretir.

Sahte seri: 2026-04-09'da biten 260 iş günü; ilk 220 gün kapanış 10, son 40 gün 20.
Elle hesap: 10 sabitken bütün EMA'lar 10, oran 0 (<= %1,2). Sıçramadan sonra EMA20 - EMA200 farkı
%1,2'nin çok üstüne çıkar (ilk gün EMA20 = 10 + 10*2/21 = 10,95; EMA200 = 10 + 10*2/201 = 10,0995).
Dizin 219 (220. gün) son sıkışık gündür: 2026-04-09 dizin 259; 40 iş günü = 8 hafta geri -> 2026-02-12.
Tarama penceresi son 130 gün = dizin 130..259; dizin 130 = 2026-04-09'dan 129 iş günü geri = 2025-10-10.
Dönem 2025-10-10 .. 2026-02-12, 90 gün (dizin 130..219), ortalama %0.
"""

import datetime as dt
import json

import pandas as pd

from tansu import sadakat, veri
from tests.test_veri import SahteKaynak, satir


def hazirla(tmp_path):
    gunler = pd.bdate_range(end="2026-04-09", periods=260)
    fiyat = [satir(g, 10.0 if i < 220 else 20.0, 10.0 if i < 220 else 20.0) for i, g in enumerate(gunler)]
    kaynak = SahteKaynak({"KRDMD": fiyat}, {"KRDMD": []})
    return veri.indir(["KRDMD"], tmp_path, kaynak, simdi=dt.datetime(2026, 10, 5, 19, 30))


def test_sikisma_donemi_ham_seriden_bulunur(tmp_path):
    anlik = veri.oku(hazirla(tmp_path), tmp_path)
    sonuc = sadakat.ema_sikismasi(anlik)
    assert len(sonuc["donemler"]) == 1
    d = sonuc["donemler"][0]
    assert (d["bas"], d["bit"], d["gun"], d["ortalama"]) == (
        pd.Timestamp("2025-10-10"), pd.Timestamp("2026-02-12"), 90, 0.0)


def test_komut_iki_kosuda_ayni_rakamlari_verir_ve_deneme_gunlugune_yazar(tmp_path):
    kimlik = hazirla(tmp_path)
    rapor, gunluk = tmp_path / "sadakat.md", tmp_path / "kayit" / "deneme.jsonl"
    ilk = sadakat.calistir(kimlik, tmp_path, rapor, gunluk)
    ikinci = sadakat.calistir(kimlik, tmp_path, rapor, gunluk)
    assert ilk == ikinci
    assert "2025-10-10" in ilk and "2026-02-12" in ilk
    assert rapor.read_text(encoding="utf-8") == ikinci
    satirlar = [json.loads(s) for s in gunluk.read_text(encoding="utf-8").splitlines()]
    assert [s["tur"] for s in satirlar] == ["sadakat", "sadakat"]
    assert all(s["anlik"] == kimlik for s in satirlar)
