from collections import Counter

import numpy as np
import pandas as pd
import pytest

from tansu import sinama


@pytest.mark.parametrize(
    ("veri_sonu", "sakli_son"),
    [
        ("2026-10-26", "2026-09-30"),
        ("2026-10-31", "2026-10-31"),
        ("2026-10-30", "2026-10-30"),
    ],
)
def test_sakli_son_verinin_son_tam_ayinin_son_gunu(veri_sonu, sakli_son):
    gunler = {
        "A": pd.DataFrame(index=pd.date_range("2026-01-01", veri_sonu)),
        "B": pd.DataFrame(index=pd.date_range("2025-01-01", "2026-03-31")),
    }
    assert sinama.sakli_son(gunler) == pd.Timestamp(sakli_son)


def test_kes_sinyal_tarihine_gore_dilimler_kurulum_kendi_cikisini_korur():
    islemler = pd.DataFrame(
        {
            "sinyal_tarihi": pd.to_datetime(["2023-06-29", "2023-07-03"]),
            "cikis_tarihi": pd.to_datetime(["2023-08-15", "2023-07-10"]),
        }
    )
    sinyaller = pd.DataFrame({"sembol": ["A", "A"], "tarih": islemler["sinyal_tarihi"]})
    dilim = sinama.Kosu(islemler, sinyaller, Counter(a=1)).kes(
        pd.Timestamp("2023-01-01"), pd.Timestamp("2023-06-30")
    )
    assert list(dilim.islemler["cikis_tarihi"]) == [pd.Timestamp("2023-08-15")]
    assert len(dilim.sinyaller) == 1 and dilim.sayac == Counter()


def kayitlar(n):
    """n kurulum; 1 günlük getiri 1, -1, 1, ... ve son kurulumun 10 günlük ufku boş."""
    yon = np.where(np.arange(n) % 2 == 0, 1.0, -1.0)
    t = pd.DataFrame(
        {
            "net_yuzde": yon,
            "R": np.nan,
            **{f"getiri_{g}": yon * g for g in (1, 3, 5, 10)},
            "mfe_yuzde": 4.0,
            "mae_yuzde": 2.0,
        }
    )
    t.loc[n - 1, "getiri_10"] = np.nan
    return t


def test_ileri_tablo_ufuk_basina_ortalama_medyan_pozitif_pay_ve_n():
    satir = {s["Ufuk (gün)"]: s for s in sinama.ileri_tablo(kayitlar(31))}
    assert satir[1]["N"] == 31 and satir[10]["N"] == 30
    assert satir[3]["Ortalama net %"] == f"{3 / 31:.2f}"
    assert satir[1]["Medyan net %"] == "1.00" and satir[1]["Pozitif payı"] == "52%"
    assert satir["Medyan MFE % (10 gün)"]["Medyan net %"] == "4.00"
    assert satir["Medyan MAE % (10 gün)"]["Medyan net %"] == "2.00"


def test_ileri_tablo_30_kurulumun_altinda_oranlar_n_a():
    satir = sinama.ileri_tablo(kayitlar(5))
    assert satir[0]["N"] == 5 and satir[0]["Ortalama net %"] == "n/a (N = 5)"
    assert sinama.ileri_tablo(pd.DataFrame())[0]["N"] == 0


def test_donem_ozeti_yalniz_olcu_sutununu_okur_ve_birimi_etikete_koyar():
    d = sinama.donem_ozeti(
        kayitlar(3).assign(
            tutma_gun=1,
            acik=False,
            dolumda_stop=False,
            risk_tabanli=False,
            cikis_tarihi=pd.date_range("2022-01-03", periods=3),
            dolum_tarihi=pd.date_range("2022-01-03", periods=3),
            sembol="A",
        ),
        3,
        "net_yuzde",
    )
    assert d["Toplam %"] == "1.00" and "Toplam R" not in d
    assert d["Beklenti (ortalama %)"] == "n/a (N = 3)"


def test_dusus_nan_degeri_atlar():
    assert sinama.dusus([1.0, -2.0, np.nan, -1.0]) == 3.0
