import pandas as pd
import pytest

from tansu.stratejiler import STRATEJILER
from tests.sentetik import gartley_yolu, gun_tablosu, ortalama_yolu

YOLLAR = {"gartley": gartley_yolu, "ortalama-kesisim": ortalama_yolu}


def test_her_kayitli_stratejinin_sentetik_yolu_var():
    assert set(YOLLAR) == set(STRATEJILER)


@pytest.mark.parametrize("ad", sorted(STRATEJILER))
def test_t_gunu_ciktisi_sonraki_gunlerden_bagimsiz(ad):
    strateji = STRATEJILER[ad]
    gun = gun_tablosu(YOLLAR[ad]())
    tam = strateji.sinyal(gun, {})
    assert tam["giris"].any()
    for t in range(60, len(gun), 7):
        kesik = strateji.sinyal(gun.iloc[: t + 1], {})
        pd.testing.assert_frame_equal(kesik, tam.iloc[: t + 1])
