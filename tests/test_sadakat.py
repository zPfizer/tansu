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

import numpy as np
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


def test_sadakat_gunlugunun_her_satirinda_olay_var(tmp_path):
    gunluk = tmp_path / "deneme.jsonl"
    sadakat.calistir(hazirla(tmp_path), tmp_path, tmp_path / "sadakat.md", gunluk)
    for satir in gunluk.read_text(encoding="utf-8").splitlines():
        assert "olay" in json.loads(satir)


def test_cift_z_aramasi_tum_gunlerde_ve_adaylarda():
    # Elle: X = 1, log Y = [0, 2, 4, 6]; pencere 3, ddof 1, log oran: Z_{t-1} = Z_t = 1 (tests/test_cift.py).
    gunler = pd.bdate_range("2025-01-01", periods=4)
    y = pd.Series(np.exp([0, 2, 4, 6]), index=gunler)
    x = pd.Series([1.0] * 4, index=gunler)
    sonuc = sadakat.cift_ara(y, x, hedef=(1.0, 1.0), tolerans=0.0005, pencereler=range(3, 4))
    assert sonuc == [("log_oran", 3, 1, gunler[-1])]


def test_ek_fiyat_ols_pencerenin_kendi_kalintilarini_kullanir():
    # Elle: Y = 2X+1+[0,0,0,2]; h=2,6, a=0; s=[0,4;-0,2;-0,8;0,6], var_0=0,3; Z=0,6/√0,3.
    x = pd.Series([1.0, 2.0, 3.0, 4.0])
    y = pd.Series([3.0, 5.0, 7.0, 11.0])
    z = sadakat._ek_z(y, x, "fiyat_ols", "kalinti", 4, 0)
    assert z.iloc[:3].isna().all()
    assert abs(z.iloc[-1] - 1.0954451150103321) < 1e-12
    z = sadakat._ek_z(y, x, "fiyat_ols", "kalinti", 4, 1)
    assert abs(z.iloc[-1] - 0.9486832980505138) < 1e-12


def test_ek_sabit_std_butun_seride_tek_sapma_kullanir():
    # Elle: d=[0,0,0,3,0,6], w=3; e=[0,2,-1,3], ort=1; std_0=√2,5; Z_3=2/√2,5.
    y = pd.Series(np.exp([0.0, 0.0, 0.0, 3.0, 0.0, 6.0]))
    x = pd.Series([1.0] * 6)
    z = sadakat._ek_z(y, x, "sabit_std", "log_oran", 3, 0)
    assert z.iloc[:2].isna().all()
    assert abs(z.iloc[2]) < 1e-12
    assert abs(z.iloc[3] - 1.2649110640673518) < 1e-12
    np.testing.assert_allclose([2 / z.iloc[3], -1 / z.iloc[4], 3 / z.iloc[5]],
                               [1.5811388300841898] * 3, rtol=0, atol=1e-12)
    z = sadakat._ek_z(y, x, "sabit_std", "log_oran", 3, 1)
    assert abs(z.iloc[3] - 1.0954451150103321) < 1e-12


def test_ek_dun_pencere_bugunu_dislar():
    # Elle: d=[0,1,2,4,3]; t=3 için önceki [0,1,2], ort=1, std_0=√(2/3); Z=3/√(2/3).
    y = pd.Series(np.exp([0.0, 1.0, 2.0, 4.0, 3.0]))
    x = pd.Series([1.0] * 5)
    z = sadakat._ek_z(y, x, "dun_pencere", "log_oran", 3, 0)
    assert z.iloc[:3].isna().all()
    assert abs(z.iloc[3] - 3.6742346141747673) < 1e-12
    z = sadakat._ek_z(y, x, "dun_pencere", "log_oran", 3, 1)
    assert abs(z.iloc[3] - 3.0) < 1e-12
    # Log OLS, önceki [0,1,2] → [1,3,6]: h=2,5, a=5/6, var_0=1/18; Z_3=(2/3)/√(1/18).
    y = pd.Series(np.exp([1.0, 3.0, 6.0, 9.0, 10.0]))
    x = pd.Series(np.exp([0.0, 1.0, 2.0, 3.0, 4.0]))
    z = sadakat._ek_z(y, x, "dun_pencere", "kalinti", 3, 0)
    assert z.iloc[:3].isna().all()
    assert abs(z.iloc[3] - 2.8284271247461903) < 1e-12


def test_ek_aday_ara_isaret_cevirerek_ara_gunde_cifti_bulur():
    # Elle: d=[0,1,2,4,3,10], w=3, ddof=1; Z_3=3; Z_4=(3-7/3)/√(7/3)=2/√21; -Z hedefi tutar.
    gunler = pd.bdate_range("2025-01-01", periods=6)
    y = pd.Series(np.exp([0.0, 1.0, 2.0, 4.0, 3.0, 10.0]), index=gunler)
    x = pd.Series([1.0] * 6, index=gunler)
    sonuc = sadakat.ek_aday_ara(y, x, hedef=(-0.4364357804719848, -3.0), pencereler=range(3, 4))
    assert sonuc == [("dun_pencere", "log_oran", 3, 1, -1, gunler[4])]
