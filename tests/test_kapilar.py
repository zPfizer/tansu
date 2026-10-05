"""`veri` yüzü: fiyat limiti, kilit, karantina, eksik gün, yapısal ihlal, oran eşikleri (TASARIM 5.1, 5.13).

Fiyatlar uydurmadır; beklenen değerler elle hesaplandı (yorumlarda). Olay tarihi ms epoch, İstanbul.
"""

import datetime as dt

import numpy as np
import pandas as pd
import pytest

from tansu import veri
from tansu.kaynak import KaynakHatasi

SIMDI = dt.datetime(2026, 10, 5, 19, 30)


def epoch(gun):
    return int(dt.datetime(gun.year, gun.month, gun.day, tzinfo=dt.timezone(dt.timedelta(hours=3))).timestamp() * 1000)


def satir(tarih, kapanis, hacim=1000.0, dusuk=None, yuksek=None, **ek):
    """Düzeltmesiz satır: ham = düzeltilmiş. dusuk/yuksek verilmezse kapanışın ±0,01'i."""
    d, y = dusuk or kapanis - 0.01, yuksek or kapanis + 0.01
    s = {"tarih": pd.Timestamp(tarih), "ham_kapanis": kapanis, "kapanis": kapanis, "ham_aof": kapanis,
         "aof": kapanis, "ham_yuksek": y, "yuksek": y, "ham_dusuk": d, "dusuk": d, "hacim": hacim}
    return {**s, **ek}


class SahteKaynak:
    def __init__(self, fiyatlar, olaylar=None, bozuk=()):
        self.fiyatlar, self.olaylar_, self.bozuk = fiyatlar, olaylar or {}, bozuk

    def fiyat(self, sembol, bas, son):
        if sembol in self.bozuk:
            raise KaynakHatasi(sembol)
        return pd.DataFrame(self.fiyatlar[sembol])

    def olaylar(self, sembol):
        return self.olaylar_.get(sembol, [])


def anlik(tmp_path, fiyatlar, olaylar=None, bozuk=()):
    if isinstance(fiyatlar, list):
        fiyatlar = {"A": fiyatlar}
    k = SahteKaynak(fiyatlar, olaylar, bozuk)
    return veri.oku(veri.indir(list(fiyatlar), tmp_path, k, simdi=SIMDI), tmp_path)


def gun(a, tarih, sembol="A"):
    g = a.gun_tablosu
    return g[(g["sembol"] == sembol) & (g["tarih"] == pd.Timestamp(tarih))].iloc[0]


def test_normal_gun_limiti(tmp_path):
    # 2024: ±%10. Önceki ham kapanış 100 → tavan 110, taban 90.
    g = gun(anlik(tmp_path, [satir("2024-01-02", 100.0), satir("2024-01-03", 105.0)]), "2024-01-03")
    assert (g["limit"], g["tavan"], g["taban"]) == (0.10, pytest.approx(110.0), pytest.approx(90.0))
    assert not g["karantina"]


def test_olay_gunu_tabani_carpanla_olcekli(tmp_path):
    # Önceki kapanış 100, çarpan 0,5 → taban 50; tavan 50 × 1,1 = 55, alt 45. Ham kapanış 55 = tavan.
    olay = {"A": [{"SHT_KODU": "02", "SHHE_TARIH": epoch(dt.date(2024, 1, 3)), "SHHE_FIYAT_AYAR_OR": 0.5}]}
    g = gun(anlik(tmp_path, [satir("2024-01-02", 100.0), satir("2024-01-03", 55.0)], olay), "2024-01-03")
    assert (g["tavan"], g["taban"]) == (pytest.approx(55.0), pytest.approx(45.0))
    assert not g["karantina"] and g["kilit_tavan"]


def test_limit_13_mart_2020de_yuzde_yirmiden_ona_gecer(tmp_path):
    # 12.03.2020 ±%20: tavan 120. 13.03.2020 ±%10: tavan 110.
    a = anlik(tmp_path, [satir("2020-03-11", 100.0), satir("2020-03-12", 100.0), satir("2020-03-13", 100.0)])
    assert (gun(a, "2020-03-12")["limit"], gun(a, "2020-03-12")["tavan"]) == (0.20, pytest.approx(120.0))
    assert (gun(a, "2020-03-13")["limit"], gun(a, "2020-03-13")["tavan"]) == (0.10, pytest.approx(110.0))


def test_kilitli_tavan_ve_taban(tmp_path):
    # Önceki 100; tavan 110, taban 90; 2024'te 90–110 arası adım 0,05 (50–100) ve 0,10 (100–250).
    # 110,0: tavan. 109,95: tavan − 0,10 içinde → kilit. 109,8: değil.
    # 90,0 taban; 90,04: taban + 0,05 içinde → kilit; 90,2: değil.
    fiyat = []
    for kapanis in (110.0, 109.95, 109.8, 90.0, 90.04, 90.2):
        fiyat += [satir("2024-01-02", 100.0), satir("2024-01-03", kapanis, dusuk=kapanis, yuksek=kapanis)]
    beklenen = [(True, False), (True, False), (False, False), (False, True), (False, True), (False, False)]
    for i, (tavan, taban) in enumerate(beklenen):
        g = gun(anlik(tmp_path / str(i), fiyat[2 * i:2 * i + 2]), "2024-01-03")
        assert (g["kilit_tavan"], g["kilit_taban"]) == (tavan, taban), fiyat[2 * i + 1]["ham_kapanis"]


def test_duyarlilik_surumu_dusuk_esit_yuksek_ister(tmp_path):
    # Önceki 100, kapanış 110 tavan. Düşük = yüksek = 110 → duyarlı kilit. Düşük 109 → kilit ama duyarlı değil.
    kilit = anlik(tmp_path / "a", [satir("2024-01-02", 100.0), satir("2024-01-03", 110.0, dusuk=110.0, yuksek=110.0)])
    gevsek = anlik(tmp_path / "b", [satir("2024-01-02", 100.0), satir("2024-01-03", 110.0, dusuk=109.0, yuksek=110.0)])
    assert gun(kilit, "2024-01-03")["kilit_tavan_duyarli"]
    g = gun(gevsek, "2024-01-03")
    assert g["kilit_tavan"] and not g["kilit_tavan_duyarli"]


def test_limiti_asan_gun_karantinaya_girer(tmp_path):
    # Tavan 110; pay %0,5 → 110,55. 111 aşar → karantina. 110,5 aşmaz.
    asan = anlik(tmp_path / "a", [satir("2024-01-02", 100.0), satir("2024-01-03", 111.0)])
    sinirda = anlik(tmp_path / "b", [satir("2024-01-02", 100.0), satir("2024-01-03", 110.5)])
    assert gun(asan, "2024-01-03")["karantina"] and not gun(sinirda, "2024-01-03")["karantina"]


def test_carpani_bir_olan_ya_da_bilinmeyen_kodlu_kayit_istisna_degildir(tmp_path):
    # Çarpan 1 → taban değişmez (100); kapanış 111 limiti aşar, kod "99" bilinmese de karantina.
    olay = {"A": [{"SHT_KODU": "99", "SHHE_TARIH": epoch(dt.date(2024, 1, 3)), "SHHE_FIYAT_AYAR_OR": 1.0}]}
    a = anlik(tmp_path, [satir("2024-01-02", 100.0), satir("2024-01-03", 111.0)], olay)
    assert gun(a, "2024-01-03")["karantina"]


def test_bozuk_satirlar_karantinaya_girer(tmp_path):
    # Düşük 101 > AOF 100; kapanış 103 > yüksek 102 (düzeltilmiş); ham kapanış 0.
    fiyat = [satir("2024-01-02", 100.0), satir("2024-01-03", 100.0, ham_dusuk=101.0),
             satir("2024-01-04", 100.0, yuksek=99.0, ham_kapanis=100.0, ham_yuksek=100.01),
             satir("2024-01-05", 100.0, ham_kapanis=0.0, ham_aof=0.0, ham_yuksek=0.0, ham_dusuk=0.0),
             satir("2024-01-08", 100.0)]
    g = anlik(tmp_path, fiyat).gun_tablosu.set_index("tarih")["karantina"]
    assert list(g) == [False, True, True, True, False]


def test_duzeltilmis_seride_yuvarlama_farki_bozuk_sayilmaz(tmp_path):
    # Gerçek THYAO 2010-01-13: kapanış 3,4421 > yüksek 3,442062; bağıl fark 1,1e-5 < 1e-4 → temiz.
    # Kapanış 100,5 > yüksek 100: bağıl fark 5e-3 > 1e-4 → karantina.
    fiyat = [satir("2024-01-02", 100.0), {**satir("2024-01-03", 100.0, yuksek=100.0), "kapanis": 100.00001},
             {**satir("2024-01-04", 100.0, yuksek=100.0), "kapanis": 100.5}]
    assert list(anlik(tmp_path, fiyat).gun_tablosu["karantina"]) == [False, False, True]


@pytest.mark.parametrize("bozuk", ["tekrar", "sira", "nan"])
def test_yapisal_ihlal_indirmeyi_durdurur(tmp_path, bozuk):
    fiyat = [satir("2024-01-02", 100.0), satir("2024-01-03", 100.0), satir("2024-01-04", 100.0)]
    if bozuk == "tekrar":
        fiyat[2] = satir("2024-01-03", 101.0)  # aynı gün, farklı alanlar (birebir aynı tekrar ihlal değil, 5.13)
    elif bozuk == "sira":
        fiyat[1], fiyat[2] = fiyat[2], fiyat[1]
    else:
        fiyat[1]["ham_kapanis"] = np.nan
    with pytest.raises(veri.VeriHatasi):
        anlik(tmp_path, fiyat)
    assert not (tmp_path / "ag").exists() or not any((tmp_path / "ag").iterdir())


def test_eksik_gun_nan_kalir_hacimsiz_gun_islem_gunu_degildir(tmp_path):
    # B 03.01'i hiç getirmez (A getirir); A 04.01'de hacim 0.
    gunler = ["2024-01-02", "2024-01-03", "2024-01-04"]
    a = anlik(tmp_path, {
        "A": [satir(g, 100.0, hacim=0.0 if g == "2024-01-04" else 1000.0) for g in gunler],
        "B": [satir("2024-01-02", 100.0), satir("2024-01-04", 100.0)]})
    eksik = gun(a, "2024-01-03", "B")
    assert eksik["eksik"] and not eksik["islem"] and not eksik["kilit_tavan"]
    assert (gun(a, "2024-01-04", "A")["eksik"], gun(a, "2024-01-04", "A")["islem"]) == (False, False)
    assert gun(a, "2024-01-04", "B")["islem"]


def test_fiyat_adimi_tablosu_06_kasim_2023te_degisir():
    tarih = pd.to_datetime(["2023-11-03", "2023-11-06"])
    assert list(veri.adim(np.array([19.99, 300.0]), tarih)) == [0.01, 0.25]
    assert list(veri.adim(np.array([20.0, 300.0]), tarih)) == [0.02, 0.25]
    assert list(veri.adim(np.array([300.0, 3000.0]), tarih[:1])) == [0.1, 0.1]
    assert list(veri.adim(np.array([2500.0]), tarih[1:])) == [2.5]


def test_karantina_orani_birin_ustundeyse_veri_sorunlu(tmp_path):
    # 200 hisse-gün. 2 karantina = %1,0 (eşik aşılmaz). 3 = %1,5 → sorunlu.
    # Her karantina günü 100 → 111 sıçrar, sonraki gün 111'den geri 111 (limit içinde) kalır.
    def seri(n_bozuk):
        tarihler = pd.bdate_range("2024-01-02", periods=200)
        s = [satir(t, 100.0) for t in tarihler]
        for i in range(n_bozuk):
            s[10 + 50 * i] = satir(tarihler[10 + 50 * i], 100.0, ham_dusuk=101.0)  # bozuk satır
        return s
    assert anlik(tmp_path / "a", seri(2)).sorunlar == []
    assert anlik(tmp_path / "b", seri(3)).sorunlar == ["karantina oranı > %1"]


def test_eksik_indirme_bes_hisseden_fazlaysa_veri_sorunlu(tmp_path):
    # 8 sembol, 5 inmez → sorunlu değil; 6 inmez → sorunlu.
    seri = [satir("2024-01-02", 100.0), satir("2024-01-03", 100.0)]
    hepsi = {f"S{i}": seri for i in range(8)}
    bes = anlik(tmp_path / "a", hepsi, bozuk=[f"S{i}" for i in range(5)])
    alti = anlik(tmp_path / "b", hepsi, bozuk=[f"S{i}" for i in range(6)])
    assert (bes.inmeyen, bes.sorunlar) == (tuple(f"S{i}" for i in range(5)), [])
    assert alti.sorunlar == ["6 hisse inmedi"]


def test_veri_donmeyen_sembol_bos_sayilir_inmeyen_degil(tmp_path):
    # İş Yatırım şirket kodu için boş liste döner (pay değil ya da hiç işlem görmemiş): hata değil.
    seri = [satir("2024-01-02", 100.0), satir("2024-01-03", 100.0)]
    hepsi = {"A": seri, **{f"S{i}": [] for i in range(8)}}
    a = anlik(tmp_path, hepsi)
    assert (a.bos, a.inmeyen, a.sorunlar) == (tuple(f"S{i}" for i in range(8)), (), [])
    assert list(a.fiyat["sembol"].unique()) == ["A"]


@pytest.mark.parametrize("olay_gunu", [dt.date(2024, 1, 2), dt.date(2024, 1, 3), dt.date(2024, 1, 4)])
def test_olay_tablosu_bir_gun_kaysa_da_sahte_karantina_olmaz(tmp_path, olay_gunu):
    # 2:1 bölünme (çarpan 0,5): ham kapanış 100 → 50, gerçek düzeltme günü 03.01. Tablo 02.01 (bir gün erken)
    # ya da 04.01 (bir gün geç) yazsa da 50 / (100 × 0,5) = 1 → hiçbir gün limiti aşmaz.
    olay = {"A": [{"SHT_KODU": "02", "SHHE_TARIH": epoch(olay_gunu), "SHHE_FIYAT_AYAR_OR": 0.5}]}
    # Düzeltilmiş seri (HGDG) bölünmeyi 03.01'den önceki günlere uygular: 100 → 50.
    yari = {"kapanis": 50.0, "aof": 50.0, "yuksek": 50.01, "dusuk": 49.99}
    fiyat = [{**satir("2023-12-29", 100.0), **yari}, {**satir("2024-01-02", 100.0), **yari},
             satir("2024-01-03", 50.0), satir("2024-01-04", 51.0)]
    assert not anlik(tmp_path, fiyat, olay).gun_tablosu["karantina"].any()


def test_ham_fiyati_ve_hacmi_bos_satir_islem_yapilmamis_gundur_atilir(tmp_path):
    # Gerçek BERDN 30.01.2012: ham alanların hepsi ve hacim NaN, düzeltilmiş alanlar dolu.
    bos = {**satir("2024-01-03", 100.0), "ham_kapanis": np.nan, "ham_aof": np.nan, "ham_yuksek": np.nan,
           "ham_dusuk": np.nan, "hacim": np.nan}
    a = anlik(tmp_path, [satir("2024-01-02", 100.0), bos, satir("2024-01-04", 100.0)])
    assert list(a.fiyat["tarih"]) == [pd.Timestamp("2024-01-02"), pd.Timestamp("2024-01-04")]


def test_birebir_ayni_tekrar_satir_tek_sayilir_farkli_tekrar_ihlaldir(tmp_path):
    # Gerçek BYDNR 23.08.2023: aynı satır iki kez geldi.
    ayni = [satir("2024-01-02", 100.0), satir("2024-01-03", 100.0), satir("2024-01-03", 100.0)]
    assert list(anlik(tmp_path / "a", ayni).fiyat["tarih"]) == [pd.Timestamp("2024-01-02"), pd.Timestamp("2024-01-03")]
    farkli = [satir("2024-01-02", 100.0), satir("2024-01-03", 100.0), satir("2024-01-03", 101.0)]
    with pytest.raises(veri.VeriHatasi):
        anlik(tmp_path / "b", farkli)


def test_hacmi_sifir_ve_ham_alanlari_nan_ya_da_sifir_satir_atilir(tmp_path):
    # Gerçek ISATR 23.06.2010: ham kapanış NaN, diğer ham alanlar ve hacim 0.
    bos = {**satir("2024-01-03", 100.0), "ham_kapanis": np.nan, "ham_aof": 0.0, "ham_yuksek": 0.0,
           "ham_dusuk": 0.0, "hacim": 0.0}
    a = anlik(tmp_path, [satir("2024-01-02", 100.0), bos, satir("2024-01-04", 100.0)])
    assert list(a.fiyat["tarih"]) == [pd.Timestamp("2024-01-02"), pd.Timestamp("2024-01-04")]
