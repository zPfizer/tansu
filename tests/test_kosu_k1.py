"""`kosu()` yüzü: K1 p'si, Holm, kabul tablosu, durum yazımı (TASARIM 5.7, 5.11, 5.12).

Veri: tests/test_k1.py'deki sentetik anlık görüntü (S1, S2 sinyalli; T1, T2 trend; D1 düşük hacim). Ek kolun önceki-gün
sayısı 3'e indirilir (8 günlük veride 20 gün olmaz). Çift bölmesi bu veride çift seçemez: işlem yok.
"""

import datetime as dt
import json
import re

import numpy as np
import pytest

from tansu import aileler, kayit, istatistik, veri
from tests.test_k1 import trend
from tests.test_simulator import ATR_N, BAS, P, duz, sinyalli
from tests.test_veri import SahteBorsapy, SahteKaynak

TEMIZ = lambda: ("abc", False)  # noqa: E731
KIRLI = lambda: ("abc", True)  # noqa: E731


@pytest.fixture(autouse=True)
def kirilim_3(monkeypatch):
    monkeypatch.setattr(aileler, "KIRILIM_GUN", 3)


def hazirla(tmp_path):
    seriler = {"S1": sinyalli(), "S2": sinyalli(), "T1": trend(), "T2": trend(), "D1": duz(1e3)}
    k = SahteKaynak(seriler, {s: [] for s in seriler})
    kimlik = veri.indir(list(seriler), tmp_path, k, simdi=dt.datetime(2026, 10, 5, 19, 30),
                        borsapy=SahteBorsapy([("2025-01-01", 0.0)], {s: "X" for s in seriler}))
    kayit.kayitla(P, ATR_N)
    return kimlik


def kos(tmp_path, kimlik, **kw):
    kw.setdefault("git", TEMIZ)
    kw.setdefault("tekrar", 5)
    return kayit.kosu(kimlik, tmp_path, p=P, atr_n=ATR_N, bas=BAS, **kw)


def tum_satirlar():
    yol = kayit.KAYIT_DIZINI / "deneme.jsonl"
    return [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines()]


def satirlar():
    """`tur=destek` (ızgara hücreleri, denetim) satırları hariç: bunlar Holm'a ve koşu satırı dizisine girmez (TASARIM 5.11)."""
    return [s for s in tum_satirlar() if s["tur"] != "destek"]


def deneme(kural, aile, p, resmi=True, kosu_id=None):
    """Günlüğe elle bir resmi koşu (basladi + bitti) yazar."""
    kosu_id = kosu_id or f"{kural}-{aile}"
    kayit._yaz({"tur": "deneme", "olay": "basladi", "kosu_id": kosu_id, "kural_id": kural, "resmi": resmi})
    kayit._yaz({"tur": "deneme", "olay": "bitti", "kosu_id": kosu_id, "kural_id": kural, "k1": {aile: {"p": p}}})


def test_holm_gunlukteki_ilk_resmi_p_lerle_elle_ornek():
    # Günlükte üç resmi p: 0,01; 0,04; 0,03. Yeni p 0,005 -> [0,01; 0,04; 0,03; 0,005] Holm -> [0,03; 0,06; 0,06; 0,02]:
    # yeni p'nin düzeltilmişi 0,02, m = 4 (TASARIM ticket 12 elle örneği).
    deneme("K1", "ema_sikismasi", 0.01)
    deneme("K2", "ema_sikismasi", 0.04)
    deneme("K3", "ema_sikismasi", 0.03)
    h = kayit.holm_hesapla("K4", {"ema_sikismasi": 0.005}, resmi=True)["ema_sikismasi"]
    assert (h["holm_p"], h["holm_m"], h["varsayimsal"]) == (pytest.approx(0.02), 4, False)
    g = kayit.holm_hesapla("K4", {"ema_sikismasi": 0.005}, resmi=False)["ema_sikismasi"]  # geliştirme: aynı hesap, varsayımsal
    assert (g["holm_p"], g["holm_m"], g["varsayimsal"]) == (pytest.approx(0.02), 4, True)


def test_ayni_kural_yeniden_kosulursa_ilk_resmi_p_kalir_ve_m_artmaz():
    deneme("K1", "ema_sikismasi", 0.01)
    deneme("K2", "ema_sikismasi", 0.04)
    h = kayit.holm_hesapla("K1", {"ema_sikismasi": 0.5}, resmi=True)["ema_sikismasi"]  # yeni p 0,5 yok sayılır: ilk p 0,01
    assert (h["holm_p"], h["holm_m"]) == (pytest.approx(0.02), 2)  # Holm [0,01; 0,04] -> [0,02; 0,04]


def test_gelistirme_kosusunun_p_si_gunlukte_holm_a_girmez():
    deneme("K1", "ema_sikismasi", 0.01, resmi=False)
    assert kayit.holm_hesapla("K2", {"ema_sikismasi": 0.04}, resmi=True)["ema_sikismasi"]["holm_m"] == 1


def test_tekrar_sayisi_gelistirmede_200_tamda_en_az_bin_ve_200_kati():
    assert kayit.tekrar_sayisi(False) == 200
    assert kayit.tekrar_sayisi(True) == 1000  # m = 0 + 2 aile
    for i in range(4):
        deneme(f"K{i}", "ema_sikismasi", 0.5)
        deneme(f"K{i}", "cift_rotasyonu", 0.5)
    assert kayit.tekrar_sayisi(True) == 2000  # m = 8 günlükte + bu kuralın 2 ailesi = 10; 200 · 10


def test_kosu_k1_p_tabani_durum_satirlari_ve_kabul_tablosu(tmp_path):
    # Dev koşusu (resmi değil), B = 5: p tabanı 1/6. EMA: 2 işlem (< 100) -> Ölçülemedi. Çift: bu veride çift seçilmez,
    # işlem yok -> p = 1 (gerçek istatistik yok), Ölçülemedi. İkisi de Deneme; Holm varsayımsal m = 2.
    kimlik = hazirla(tmp_path)
    s = kos(tmp_path, kimlik)
    ema, cift = s["k1"]["ema_sikismasi"], s["k1"]["cift_rotasyonu"]
    assert 1 / 6 <= ema["p"] <= 1.0 and ema["p"] == max(ema["p_a"], ema["p_b"]) and ema["tekrar"] == 5
    assert ema["sinyal"] == 2
    assert (cift["p"], cift["gecis"]) == (1.0, 0)
    assert [s["kabul"][a]["genel"] for a in ("ema_sikismasi", "cift_rotasyonu")] == ["Ölçülemedi", "Ölçülemedi"]
    assert [r["durum"] for r in s["kabul"]["ema_sikismasi"]["satirlar"]][4] == "Ölçülemedi"
    kayit_s, basladi, bitti, d1, d2 = satirlar()
    assert bitti["k1"]["ema_sikismasi"]["p"] == ema["p"] and bitti["tekrar"] == 5
    assert set(bitti["k1"]["ema_sikismasi"]) >= {"p_a", "p_b", "p_ek", "gercek"}
    assert [(r["tur"], r["aile"], r["durum"], r["resmi"], r["varsayimsal"], r["holm_m"]) for r in (d1, d2)] == [
        ("durum", "ema_sikismasi", "Deneme", False, True, 2), ("durum", "cift_rotasyonu", "Deneme", False, True, 2)]
    assert kayit.durum_oku("ema_sikismasi") == "Deneme"
    assert d1["kanit"]["islem"] == 2 and set(d1["kanit"]) == {"islem", "fazla", "ci"}  # kart kanıt satırı için (bilet 14)


def test_kosu_rapor_kabul_tablosu_m_ve_holm_tarihi_yasakli_sozcuk_yok(tmp_path):
    kimlik = hazirla(tmp_path)
    html = kos(tmp_path, kimlik)["rapor"].read_text(encoding="utf-8")
    for beklenen in ("Kabul tablosu", "Holm m = 2", "Holm tarihi", "Ölçülemedi", "Güven aralığı", "Saptanabilir en küçük etki"):
        assert beklenen in html
    assert html.count("<h2>Uyarılar</h2>") == 1
    assert not re.search(r"\b(AL|SAT|ÖNERİ)\b|Tansu'nun sistemi", html)


def test_ayni_tohum_ayni_ozet(tmp_path):
    kimlik = hazirla(tmp_path)
    assert kos(tmp_path, kimlik, tohum=3)["ozet"] == kos(tmp_path, kimlik, tohum=3)["ozet"]


def test_resmi_kosu_tam_tekrardan_azsa_durur_ve_resmi_p_holm_a_girer(tmp_path, monkeypatch):
    kimlik = hazirla(tmp_path)
    with pytest.raises(kayit.KayitHatasi, match="tekrar"):
        kos(tmp_path, kimlik, resmi=True)  # B = 5 < 1000
    assert [r["olay"] for r in satirlar()] == ["kayit"]  # hiçbir koşu satırı yazılmadı
    monkeypatch.setattr(kayit, "TAM_TABAN", 5)
    monkeypatch.setattr(kayit, "TAM_CARPAN", 1)
    kayit.denetim_yaz({"gecti": True}, P, ATR_N)  # ilk resmi koşu için geçen denetim şart
    s = kos(tmp_path, kimlik, resmi=True)
    assert [r["holm_m"] for r in (satirlar()[-2], satirlar()[-1])] == [2, 2]
    assert not satirlar()[-1]["varsayimsal"] and satirlar()[-1]["resmi"]
    # İkinci resmi koşu aynı kural: m artmaz, ilk resmi p kalır.
    kos(tmp_path, kimlik, resmi=True, tohum=9)
    assert [r["holm_m"] for r in satirlar()[-2:]] == [2, 2]
    assert [r["holm_p"] for r in satirlar()[-2:]] == [r["holm_p"] for r in satirlar()[-6:-4]]
    assert s["k1"]["ema_sikismasi"]["p"] >= 1 / 6


def test_ilk_resmi_kosu_denetimsiz_ya_da_basarisiz_denetimle_yapilmaz(tmp_path, monkeypatch):
    # TASARIM 5.12: boru hattı denetimi ilk resmi koşudan önce geçmiş olmalı (bu kodun hash'iyle). Başarısız denetim de engeller.
    kimlik = hazirla(tmp_path)
    monkeypatch.setattr(kayit, "TAM_TABAN", 5)
    monkeypatch.setattr(kayit, "TAM_CARPAN", 1)
    with pytest.raises(kayit.KayitHatasi, match="denetim"):
        kos(tmp_path, kimlik, resmi=True)
    kayit.denetim_yaz({"gecti": False}, P, ATR_N)
    with pytest.raises(kayit.KayitHatasi, match="denetim"):
        kos(tmp_path, kimlik, resmi=True)
    assert [r["olay"] for r in tum_satirlar()] == ["kayit", "denetim"]  # hiçbir koşu satırı yazılmadı
    kayit.denetim_yaz({"gecti": True}, P, ATR_N)
    kos(tmp_path, kimlik, resmi=True)  # geçer
    assert [r["olay"] for r in satirlar()][-4:] == ["basladi", "bitti", "durum", "durum"]
    kos(tmp_path, kimlik, resmi=True, tohum=2)  # sonraki resmi koşular denetim aramaz (ilk resmi koşu geçti)


def test_izgara_hucreleri_destek_olarak_yazilir_holm_m_ye_girmez_ve_olcut_5_e_baglanir(tmp_path):
    # KURALLAR §3 ızgarası: EMA 3·3·3 = 27, çift 2·3·3 = 18 hücre; her hücre bir `destek` satırı (TASARIM 5.10, 5.11).
    kimlik = hazirla(tmp_path)
    s = kos(tmp_path, kimlik)
    d = [r for r in tum_satirlar() if r["tur"] == "destek"]
    assert [(r["olay"], r["kosu_id"]) for r in d] == [("hucre", s["kosu_id"])] * 45
    assert [r["aile"] for r in d] == ["ema_sikismasi"] * 27 + ["cift_rotasyonu"] * 18
    assert {"esik", "min_gun", "pencere"} == set(d[0]["hucre"]) and {"z_pencere", "z_esik", "p_esik"} == set(d[-1]["hucre"])
    assert all(r["pozitif"] == (r["fazla"] is not None and r["fazla"] > 0) for r in d)
    assert kayit.deneme_sayisi() == 1  # destek satırları m'ye girmez
    for aile, n in (("ema_sikismasi", 27), ("cift_rotasyonu", 18)):
        ham = s["kabul"][aile]["satirlar"][4]["ham"]  # ölçüt 5: İşlem, Farklı gün, Sağlamlık
        poz = sum(r["pozitif"] for r in d if r["aile"] == aile)
        assert ham[2][0] == "Sağlamlık" and ham[2][1] == pytest.approx(poz / n)


def test_kagit_durumu_donar_ve_durum_oku_son_resmi_satiri_okur():
    # Kâğıt'a geçmiş resmi satır: holm_p 0,001, m = 3. Sonradan başka kurallar eklense de aynı kural için bunlar kullanılır.
    kayit._yaz({"tur": "durum", "olay": "durum", "aile": "ema_sikismasi", "kural_id": "K1", "durum": "Kâğıt",
                "holm_p": 0.001, "holm_m": 3, "resmi": True, "varsayimsal": False})
    deneme("K2", "ema_sikismasi", 0.02)
    deneme("K3", "ema_sikismasi", 0.03)
    h = kayit.holm_hesapla("K1", {"ema_sikismasi": 0.5}, resmi=True)["ema_sikismasi"]
    assert (h["holm_p"], h["holm_m"], h["donmus"]) == (0.001, 3, True)
    assert kayit.durum_oku("ema_sikismasi") == "Kâğıt"
    kayit._yaz({"tur": "durum", "olay": "durum", "aile": "ema_sikismasi", "kural_id": "K9", "durum": "Kâğıt",
                "holm_p": 0.001, "holm_m": 3, "resmi": False, "varsayimsal": True})  # geliştirme satırı sayılmaz
    assert kayit.durum_oku("cift_rotasyonu") == "Deneme"
