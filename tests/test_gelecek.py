import pandas as pd
import pytest

from tansu.stratejiler import STRATEJILER
from tests.sentetik import SABIT, YOLLAR, gun_tablosu


@pytest.mark.parametrize("ad", sorted(STRATEJILER))
def test_t_gunu_ciktisi_sonraki_gunlerden_bagimsiz(ad):
    strateji = STRATEJILER[ad]
    gun = gun_tablosu(YOLLAR[ad]())
    tam = strateji.sinyal(gun, SABIT[ad])
    assert tam["giris"].any()
    for t in range(60, len(gun), 7):
        kesik = strateji.sinyal(gun.iloc[: t + 1], SABIT[ad])
        pd.testing.assert_frame_equal(kesik, tam.iloc[: t + 1])
