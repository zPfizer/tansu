"""Varsayılanların tek bekçisi. Diğer testler `SABIT` okur; varsayılan değişirse yalnız bu dosya kırılır."""

import pytest

from tansu import sinama
from tansu.stratejiler import STRATEJILER
from tests.sentetik import SABIT, YOLLAR, gun_tablosu


def test_her_kayitli_stratejinin_yolu_ve_varsayilan_anahtarli_sabiti_var():
    assert set(YOLLAR) == set(STRATEJILER) == set(SABIT)
    for ad, s in STRATEJILER.items():
        assert set(SABIT[ad]) == set(s.varsayilan), ad


@pytest.mark.parametrize("ad", sorted(STRATEJILER))
def test_varsayilan_parametreler_altin_yolda_dolan_kurulum_verir(ad):
    gun = gun_tablosu(YOLLAR[ad]())
    donem = sinama.Donem(gun.index[0], gun.index[-1])
    k = sinama.calistir(STRATEJILER[ad], {"YOL": gun}, {}, donem)
    assert len(k.sinyaller) and len(k.islemler), (
        f"{ad}: varsayılan parametreler altın yolda sıfır kurulum veriyor "
        f"({len(k.sinyaller)} sinyal, {len(k.islemler)} dolum); varsayılan {dict(STRATEJILER[ad].varsayilan)}"
    )
