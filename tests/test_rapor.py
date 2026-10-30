from collections import Counter

import numpy as np
import pandas as pd
import pytest

from tansu import ayar, montecarlo, rapor, sinama

OLUMLU_GIRDI = dict(
    r=[2.0] * 22 + [-1.0] * 18,
    rastgele=97.0,
    p5=3.0,
    sakli=(1.0, -0.5),
    puan=0.4,
    semboller={"S0": 3.0, "S1": 3.0, "S2": 4.0},
)
UYARI_GIRDI = dict(
    r=[1.0] * 38 + [-1.0] * 2,
    rastgele=50.0,
    p5=-1.0,
    sakli=(-0.5,),
    puan=-0.2,
    semboller={"S0": 5.0, "S1": 1.0},
)
AZ_GIRDI = dict(r=[1.0] * 10, semboller={"S0": -1.0})


def bayrak_olcumu(r, *, rastgele=None, p5=None, sakli=(), puan=None, semboller):
    bos = pd.DataFrame(columns=["sembol", "tarih"])

    def kosu(islemler):
        return sinama.Kosu(islemler, bos, Counter(), "R")

    mc = montecarlo.MonteCarlo(
        tohum=montecarlo.TOHUM,
        tekrar=montecarlo.TEKRAR,
        n=len(r),
        bootstrap_toplam=None if p5 is None else (p5, p5 + 1, p5 + 2),
        bootstrap_dusus=None,
        batma=None,
        karistirma_dusus=None,
        rastgele=None
        if rastgele is None
        else montecarlo.Rastgele(
            strateji_ort=0.0, ortalamalar=(0, 0, 0), yuzdelik=rastgele
        ),
    )
    p = np.array([np.nan if puan is None else puan])
    secim = ayar.Secim(
        nokta=0,
        parametre={},
        puan=p,
        saglam=p,
        n=np.array([77]),
        puanli=puan is not None,
    )
    gecmis = pd.DataFrame({"sembol": list(semboller), "R": list(semboller.values())})
    return rapor.bayrak_olc(
        mc,
        kosu(pd.DataFrame({"R": r})),
        kosu(pd.DataFrame({"R": list(sakli)})),
        kosu(gecmis),
        secim,
    )


def bayrak_tablosu(**girdi):
    olcum = bayrak_olcumu(**girdi)
    return [(s["Değer"], s["N"]) for s in rapor.bayrak_satirlari(olcum, "R")]


@pytest.mark.parametrize(
    ("bayrak", "olumlu", "uyari"),
    [
        (rapor.Bayrak.DIS_BEKLENTI, True, True),
        (rapor.Bayrak.RASTGELE, True, False),
        (rapor.Bayrak.BOOTSTRAP, True, False),
        (rapor.Bayrak.SAKLI, True, False),
        (rapor.Bayrak.KAZANMA_90, False, True),
        (rapor.Bayrak.KAZANMA_BANT, False, True),
        (rapor.Bayrak.SECIM_PUANI, False, True),
        (rapor.Bayrak.SEMBOL, False, True),
    ],
)
def test_bayrak_kurali_karar_verir_ya_da_karar_verilemez(bayrak, olumlu, uyari):
    assert bayrak_olcumu(**OLUMLU_GIRDI)[bayrak].kosul is olumlu
    assert bayrak_olcumu(**UYARI_GIRDI)[bayrak].kosul is uyari
    assert bayrak_olcumu(**AZ_GIRDI)[bayrak].kosul is None


def test_bayraklar_olumlu_strateji():
    assert bayrak_tablosu(**OLUMLU_GIRDI) == [
        ("evet (0.65 R)", 40),
        ("evet (yüzdelik 97.0)", 40),
        ("evet (3.00 R)", 40),
        ("evet (0.50 R)", 2),
        ("hayır (55%)", 40),
        ("hayır (55%)", 40),
        ("hayır (0.40 R)", 77),
        ("hayır (S2 40%)", 3),
    ]


def test_bayraklar_uyarilari():
    assert bayrak_tablosu(**UYARI_GIRDI) == [
        ("evet (0.90 R)", 40),
        ("hayır (yüzdelik 50.0)", 40),
        ("hayır (-1.00 R)", 40),
        ("hayır (-0.50 R)", 1),
        ("evet (95%)", 40),
        ("evet (95%)", 40),
        ("evet (-0.20 R)", 77),
        ("evet (S0 83%)", 2),
    ]


def test_bayraklar_ornek_az_ve_tanimsiz_degerler():
    az = ("örnek az (N = 10)", 10)
    assert bayrak_tablosu(**AZ_GIRDI) == [
        az,
        ("n/a (N = 10)", 10),
        ("n/a (N = 10)", 10),
        ("n/a (N = 0)", 0),
        az,
        az,
        ("puanlı nokta yok", 77),
        ("n/a (toplam 0 ya da altında, pay tanımsız)", 1),
    ]


def test_bayrak_rastgele_kiyas_yapilamadiysa_nedeni_yazar():
    satir = bayrak_tablosu(r=[1.0] * 40, p5=1.0, semboller={"S0": 1.0})[1]
    assert satir == ("n/a (uygun rastgele gün ya da şablon yok)", 40)
