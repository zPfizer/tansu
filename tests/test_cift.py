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

from tansu import cift


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
