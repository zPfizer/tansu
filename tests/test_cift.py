"""`cift` çekirdeği: Z ve ΔZ, elle hesaplı küçük seriler.

Log oranlı Z: X = 1 (log 0), log Y = [0, 2, 4, 6]. Pencere 3, son üç değer [2, 4, 6]:
ortalama 4, sapma kareleri toplamı 8 → ddof 1 std = 2 → Z = (6-4)/2 = 1; ddof 0 std = sqrt(8/3) = 1,63299 → Z = 1,224745.
[0, 2, 4] penceresi de aynı: Z_{t-1} = 1 (ddof 1), ΔZ = 0.

β'lı kalıntı: log X = [0, 1, 2], log Y = [0, 2, 3]. Ortalamalar 1 ve 5/3; sapmalar [-1, 0, 1] ve [-5/3, 1/3, 4/3];
sxy = 3, sxx = 2 → β = 1,5. Kalıntılar [-1/6, 1/3, -1/6]; kareler toplamı 1/6.
Son kalıntı -1/6: ddof 1 std = sqrt(1/12) → Z = -1/sqrt(3) = -0,577350; ddof 0 std = sqrt(1/18) → Z = -0,707107.
Korelasyon = sxy / sqrt(sxx * syy); syy = 25/9 + 1/9 + 16/9 = 42/9 → r = 3 / sqrt(2*42/9) = 0,981981.
"""

import numpy as np
import pandas as pd
import pytest

from tansu import cift, ciftbolme


def seri(log_degerler):
    gunler = pd.bdate_range("2025-01-01", periods=len(log_degerler))
    return pd.Series(np.exp(log_degerler), index=gunler)


def test_log_oran_z_ddof_1_ve_0():
    y, x = seri([0, 2, 4, 6]), seri([0, 0, 0, 0])
    z1 = cift.z_skor(y, x, 3, ddof=1, mod="log_oran")
    z0 = cift.z_skor(y, x, 3, ddof=0, mod="log_oran")
    assert z1.iloc[-1] == pytest.approx(1.0)
    assert z0.iloc[-1] == pytest.approx(1.224745, abs=1e-6)
    assert z1.iloc[:2].isna().all()


def test_dz_ardisik_farktir():
    y, x = seri([0, 2, 4, 6]), seri([0, 0, 0, 0])
    dz = cift.dz(cift.z_skor(y, x, 3, ddof=1, mod="log_oran"))
    assert dz.iloc[-1] == pytest.approx(0.0)
    assert dz.iloc[:3].isna().all()


def test_kalinti_z_beta_ile():
    y, x = seri([0, 2, 3]), seri([0, 1, 2])
    assert cift.z_skor(y, x, 3, ddof=1, mod="kalinti").iloc[-1] == pytest.approx(
        -0.577350, abs=1e-6
    )
    assert cift.z_skor(y, x, 3, ddof=0, mod="kalinti").iloc[-1] == pytest.approx(
        -0.707107, abs=1e-6
    )


def test_beta_ve_korelasyon():
    y, x = seri([0, 2, 3]), seri([0, 1, 2])
    assert cift.beta(y, x, 3).iloc[-1] == pytest.approx(1.5)
    assert cift.korelasyon(y, x, 3).iloc[-1] == pytest.approx(0.981981, abs=1e-6)


def cift_paketi():
    """60 satır 0, sonra log oran 0,05 ve 0,02: X'e dönüş sinyali."""
    gunler = pd.bdate_range("2025-01-01", periods=62)
    satirlar = []
    for i, gun in enumerate(gunler):
        for sembol, fiyat in (("Y", np.exp([0.0] * 60 + [0.05, 0.02])[i]), ("X", 1.0)):
            satirlar.append(
                {
                    "sembol": sembol,
                    "tarih": str(gun.date()),
                    "duzeltilmis_kapanis": {"deger": fiyat},
                }
            )
    return {
        "piyasa": satirlar,
        "gunler": list(map(str, gunler.date)),
        "semboller": ["Y", "X"],
        "referans": {
            "kayit_id": "sentetik",
            "istenen_donem": {
                "baslangic": "2025-01-01",
                "bitis": str(gunler[-1].date()),
            },
        },
    }


def test_cift_ortak_kurulum_hedef_bacak_ve_gerekceli_bos_alanlar():
    paket = cift_paketi()
    strateji = ciftbolme.strateji_coz("Y", "X")
    sonuc = ciftbolme.ortak_kurulum(paket, paket["gunler"][-1], strateji)
    assert len(sonuc["sinyaller"]) == 1
    sinyal = sonuc["sinyaller"][0]
    assert sinyal["hedef"] == {"deger": -1.0, "birim": "bacak", "bos_nedeni": None}
    assert sinyal["hedef_sembol"] == "X"
    assert sinyal["kutu_alt"]["deger"] is None
    assert sinyal["kutu_alt"]["bos_nedeni"] == "cift_ailesinde_kutu_yok"
    assert sinyal["kar_hedefi"]["bos_nedeni"] == "cift_ailesinde_kar_hedefi_yok"
    assert sinyal["ilk_stop"]["bos_nedeni"] == "cift_ailesinde_stop_yok"
    assert sinyal["katalog_surumu"] == ""
    assert sinyal["kurulum_girdileri"]["z_esik"]["deger"] == 2.0


@pytest.mark.parametrize(
    "gun,eksik,beklenen_neden",
    [(0, False, "isinma_veya_tanimsiz"), (61, True, "eksik_veri")],
)
def test_cift_ortak_kurulum_isinma_ve_eksik_veri(gun, eksik, beklenen_neden):
    paket = cift_paketi()
    if eksik:
        paket["piyasa"][-2]["duzeltilmis_kapanis"]["deger"] = None
    sonuc = ciftbolme.ortak_kurulum(
        paket, paket["gunler"][gun], ciftbolme.strateji_coz("Y", "X")
    )
    assert sonuc["sinyaller"] == []
    assert len(sonuc["gostergeler"]) == 2
    assert all(
        r["deger"] is None and r["bos_nedeni"] == beklenen_neden
        for r in sonuc["gostergeler"]
    )
    assert not sonuc["isinma"]["Y-X"]["tamam"]


def test_cift_ortak_deger_tarih_eski_uyarlayiciyla_ayni():
    paket = cift_paketi()
    tarih = paket["gunler"][-1]
    sonuc = ciftbolme.ortak_kurulum(paket, tarih, ciftbolme.strateji_coz("Y", "X"))
    # Son pencere: 58 sıfır, 0,05 ve 0,02. Toplam 0,07; kare toplamı 0,0029.
    # Önceki pencere tek sıçrama: Z = 59/sqrt(60).
    degerler = {r["ad"]: r["deger"] for r in sonuc["gostergeler"]}
    assert degerler["z"] == pytest.approx(2.72494047844687)
    assert degerler["dz"] == pytest.approx(-4.8919267690943835)
    assert {r["tarih"] for r in sonuc["gostergeler"]} == {tarih}
    Kc = pd.DataFrame(
        {"Y": np.exp([0.0] * 60 + [0.05, 0.02]), "X": 1.0},
        index=pd.DatetimeIndex(paket["gunler"]),
    )
    eski_z = cift.z_skor(Kc["Y"], Kc["X"], 60)
    assert degerler["z"] == eski_z.iloc[-1]
    assert degerler["dz"] == cift.dz(eski_z).iloc[-1]
    assert sonuc["sinyaller"][0]["hedef"]["deger"] == ciftbolme.hedef(Kc, "Y", "X")[-1]


def test_cift_strateji_uyusmazligi_ve_donem_disi_hata():
    paket = cift_paketi()
    strateji = ciftbolme.strateji_coz("Y", "X")
    with pytest.raises(ValueError, match="dönemin dışında"):
        ciftbolme.ortak_kurulum(paket, "2024-12-31", strateji)
    next(p for p in strateji["parametreler"] if p["ad"] == "z_esik")["deger"] = 3.0
    with pytest.raises(ValueError, match="uyuşmuyor"):
        ciftbolme.ortak_kurulum(paket, paket["gunler"][-1], strateji)


def test_cift_cozulmus_ayarlar_birim_ve_kaynak_tasir():
    strateji = ciftbolme.strateji_coz("Y", "X")
    assert isinstance(strateji["parametreler"], list)
    z = next(p for p in strateji["parametreler"] if p["ad"] == "z_pencere")
    assert z["deger"] == 60 and z["birim"] == "seans"
    assert z["kaynaklar"][0]["tarih"]
    assert strateji["izin_durumu"] == "legacy_karsilastirma"
