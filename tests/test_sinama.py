import numpy as np
import pandas as pd

from tansu import sinama


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
