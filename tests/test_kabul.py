"""Kabul tablosu: 6 ölçüt, Ölçülemedi yolu, portföy kuralı, aile durumu (TASARIM 5.12 ve "Ölçütlerin uygulanışı")."""

import numpy as np
import pandas as pd
import pytest

from tansu import istatistik

# Özkaynak: 01.01.2016 100 → 01.03 90 (düşüş %10) → 01.09 100,5 (toparlandı; 244 gün altında) → 01.01.2017 120.
OZ = pd.Series(
    [100.0, 90.0, 100.5, 120.0],
    index=pd.to_datetime(["2016-01-01", "2016-03-01", "2016-09-01", "2017-01-01"]),
)
# Tamamlanmış yıllar 2016-2019: +0,05; -0,01; +0,02; +0,03 -> 3/4 = %75. Yarım yıllar 2015 ve 2020 (-1) paydadan çıkar:
# dahil olsaydı 3/6 = %50 olurdu.
YILLIK = pd.Series([-1.0, 0.05, -0.01, 0.02, 0.03, -1.0], index=range(2015, 2021))


def girdi(**degisim):
    g = {
        "fazla": {0.003: 0.01, 0.005: 0.005},
        "p": 0.02,
        "portfoy": {0.003: 1e-4, 0.005: 5e-5},
        "yillik": YILLIK,
        "bas": pd.Timestamp("2015-12-01"),
        "bitis": pd.Timestamp("2020-03-01"),
        "islem_yok": [],
        "islem_fazla": np.array([0.1] + [0.01] * 19),
        "islem": 120,
        "gun": 70,
        "mde": 0.06,
        "islem_yil": 12.0,
        "ozkaynak": OZ,
        "saglamlik": 0.7,
    }
    g.update(degisim)
    return g


def durumlar(k):
    return [s["durum"] for s in k["satirlar"]]


def test_tum_olcutler_gecer_alti_satir_kagit_durumu():
    # 6. ölçüt (kâğıt dönemi) henüz yok -> Ölçülemedi; ilk beşi Geçti -> durum Kâğıt, genel Ölçülemedi (Geçti değil).
    k = istatistik.kabul(girdi())
    assert [s["no"] for s in k["satirlar"]] == [1, 2, 3, 4, 5, 6]
    assert durumlar(k) == ["Geçti"] * 5 + ["Ölçülemedi"]
    assert (k["durum"], k["genel"], k["ret"], k["olculemedi"]) == (
        "Kâğıt",
        "Ölçülemedi",
        False,
        False,
    )


def test_holm_p_buyukse_olcut_bir_ve_uc_gecmez_durum_deneme():
    k = istatistik.kabul(girdi(p=0.2))
    assert durumlar(k)[:5] == ["Geçmedi", "Geçti", "Geçmedi", "Geçti", "Geçti"]
    assert (k["durum"], k["genel"]) == ("Deneme", "Geçmedi")


def test_yarim_yillar_paydadan_cikar_ve_islem_yok_yili_da():
    # Tamamlanmış 2016-2019: 3/4 pozitif -> Geçti. 2016'yı "işlem yok" yaparsak 2017-2019: 2/3 = %66,7 -> yine Geçti;
    # 2019 da çıkarsa 1/2 = %50 -> Geçmedi.
    assert durumlar(istatistik.kabul(girdi()))[3] == "Geçti"
    assert durumlar(istatistik.kabul(girdi(islem_yok=[2016])))[3] == "Geçti"
    assert durumlar(istatistik.kabul(girdi(islem_yok=[2016, 2019])))[3] == "Geçmedi"


def test_en_iyi_yuzde_bes_atilinca_sonuc_pozitif_olmali():
    # n = 20: ⌈0,05·20⌉ = 1 işlem atılır. [1,0] + 19 × (−0,01): ortalama +0,0405 > 0 ama atılınca −0,01 -> Geçmedi.
    k = istatistik.kabul(girdi(islem_fazla=np.array([1.0] + [-0.01] * 19)))
    assert durumlar(k)[3] == "Geçmedi"


def test_ornek_yetmezse_olculemedi_gecmedi_degil():
    # 80 işlem < 100: örneklem sağlanmıyor -> ölçüt 5 ve genel Ölçülemedi; durum Deneme.
    k = istatistik.kabul(girdi(islem=80))
    assert durumlar(k)[4] == "Ölçülemedi" and (
        k["genel"],
        k["olculemedi"],
        k["durum"],
    ) == ("Ölçülemedi", True, "Deneme")
    # 60 farklı gün şartı: 59 gün -> yine Ölçülemedi.
    assert istatistik.kabul(girdi(gun=59))["olculemedi"]


def test_saptanabilir_etki_masrafin_gidis_donusunden_buyukse_olculemedi():
    # 0,06 / 12 işlem = 0,005 ≤ 0,01 -> ölçülür. 0,24 / 12 = 0,02 > 0,01 (%0,5 masrafın gidiş-dönüşü) -> Ölçülemedi.
    assert not istatistik.kabul(girdi(mde=0.06))["olculemedi"]
    k = istatistik.kabul(girdi(mde=0.24))
    assert k["olculemedi"] and k["genel"] == "Ölçülemedi"


def test_saglamlik_yoksa_olculemedi_dusukse_gecmedi():
    assert durumlar(istatistik.kabul(girdi(saglamlik=None)))[4] == "Ölçülemedi"
    assert istatistik.kabul(girdi(saglamlik=None))["durum"] == "Deneme"
    k = istatistik.kabul(girdi(saglamlik=0.5))
    assert durumlar(k)[4] == "Geçmedi" and k["durum"] == "Deneme"


def test_p_yoksa_olcut_bir_ve_uc_olculemedi():
    assert durumlar(istatistik.kabul(girdi(p=None)))[:3:2] == [
        "Ölçülemedi",
        "Ölçülemedi",
    ]


def test_masraf_yuzde_yarimda_negatifse_olcut_uc_gecmez():
    k = istatistik.kabul(girdi(fazla={0.003: 0.01, 0.005: -0.001}))
    assert durumlar(k)[:3] == ["Geçti", "Geçti", "Geçmedi"]


def test_portfoy_kurali_dusus_yuzde_yirmi_besi_asarsa_reddeder():
    # 100 → 70: düşüş %30 > %25 -> ret; diğer ölçütler geçse de genel Geçmedi, durum Deneme.
    oz = pd.Series(
        [100.0, 70.0, 130.0],
        index=pd.to_datetime(["2016-01-01", "2016-02-01", "2016-03-01"]),
    )
    k = istatistik.kabul(girdi(ozkaynak=oz))
    assert k["ret"] and k["genel"] == "Geçmedi" and k["durum"] == "Deneme"
    assert k["dusus"][0] == pytest.approx(0.30)


def test_portfoy_kurali_dususte_kalma_oniki_ayi_asarsa_reddeder():
    # Zirve 01.01.2016; 01.02.2017'ye dek (397 gün > 365) altında: düşüş yalnız %5 olsa da ret.
    oz = pd.Series(
        [100.0, 95.0, 99.0, 101.0],
        index=pd.to_datetime(["2016-01-01", "2016-06-01", "2017-01-15", "2017-02-01"]),
    )
    k = istatistik.kabul(girdi(ozkaynak=oz))
    assert k["ret"] and k["dusus"][1] == 397
    assert not istatistik.kabul(girdi())["ret"]  # OZ: %10 düşüş, 244 gün
