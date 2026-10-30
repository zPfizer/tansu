import dataclasses
import json
from collections import Counter
from itertools import pairwise

import numpy as np
import pandas as pd
import pytest

from tansu import ayar, sinama, veri
from tansu.stratejiler import STRATEJILER, ortalama_kesisim
from tests.sentetik import piyasa

KESISIM = dataclasses.replace(
    ortalama_kesisim.STRATEJI,
    varsayilan={"ortalama": "SMA", "cift": "9/21", "teyit_gun": 0},
    aralik={
        "ortalama": ("EMA", "SMA"),
        "cift": ("5/20", "9/21", "20/50"),
        "teyit_gun": (0, 2),
    },
)
OYUNCAK = dataclasses.replace(
    ortalama_kesisim.STRATEJI,
    varsayilan={"a": 1, "b": 1},
    aralik={"a": (1, 2, 3), "b": (1, 2, 3)},
)
T = pd.Timestamp


def kosu(puan: float) -> sinama.Kosu:
    n = sinama.EN_AZ - 1 if np.isnan(puan) else sinama.EN_AZ
    islemler = pd.DataFrame(
        {
            "sinyal_tarihi": T("2021-03-01"),
            "cikis_tarihi": T("2021-04-01"),
            "acik": False,
            "net_yuzde": [0.0 if np.isnan(puan) else puan] * n,
        }
    )
    return sinama.Kosu(
        islemler, pd.DataFrame(columns=["sembol", "tarih"]), Counter(), "net_yuzde"
    )


def sec(strateji, puanlar) -> ayar.Secim:
    izgara = ayar.Izgara(strateji)
    return ayar.sec(izgara, [kosu(p) for p in puanlar], sinama.KESIM, "net_yuzde")


@pytest.fixture(scope="module")
def yuruyus():
    return ayar.yuru(KESISIM, piyasa(), isci=1)


def test_pencereler_alti_ardisik_yarim_yil_ve_capali_egitim():
    p = ayar.PENCERELER
    assert [w.ad for w in p] == [
        "2023H1",
        "2023H2",
        "2024H1",
        "2024H2",
        "2025H1",
        "2025H2",
    ]
    assert p[0].test_bas == T("2023-01-01") and p[0].egitim_son == T("2022-12-31")
    assert p[-1].test_son == sinama.KESIM
    assert all(b.test_bas == a.test_son + pd.Timedelta(days=1) for a, b in pairwise(p))
    assert [w.egitim_yil for w in p] == [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]


def test_egitim_yalniz_icerde_kapanan_kurulumlari_alir():
    son = T("2022-12-31")
    islemler = pd.DataFrame(
        {
            "ad": ["icerde", "sonra kapanan", "acik", "tam sonda"],
            "sinyal_tarihi": [
                T("2022-03-01"),
                T("2022-11-01"),
                T("2022-12-01"),
                T("2022-12-01"),
            ],
            "cikis_tarihi": [T("2022-06-01"), T("2023-01-15"), T("2022-12-20"), son],
            "acik": [False, False, True, False],
        }
    )
    assert list(ayar.egitim(islemler, son)["ad"]) == ["icerde", "tam sonda"]


def test_saglam_puan_tek_tepe_yerine_plato_secer_esitlikte_yuksek_kendi_puani():
    nan = np.nan
    s = sec(OYUNCAK, [9, nan, nan, nan, 3, 4, nan, 4, 5])
    np.testing.assert_allclose(
        s.saglam, [3, nan, nan, nan, 4, 4, nan, 4, 4], equal_nan=True
    )
    assert s.puanli and s.nokta == 8 and s.parametre == {"a": 3, "b": 3}


def test_saglam_puan_tam_esitlikte_dusuk_sira_kazanir():
    tek_eksen = dataclasses.replace(
        OYUNCAK, varsayilan={"a": 1}, aralik={"a": (1, 2, 3)}
    )
    s = sec(tek_eksen, [2.0, 2.0, 2.0])
    assert s.nokta == 0 and list(s.saglam) == [2.0, 2.0, 2.0]


def test_puanli_nokta_yoksa_varsayilanlar_ve_puanli_false():
    s = sec(OYUNCAK, [np.nan] * 9)
    assert not s.puanli and s.nokta == 0 and s.parametre == OYUNCAK.varsayilan
    assert np.isnan(s.saglam).all()


def test_az_kurulumlu_pazarda_her_adim_varsayilan_ve_verim_yok():
    y = ayar.yuru(KESISIM, piyasa(sembol=1, son="2022-06-30"), isci=1)
    assert not y.son.puanli and y.son.parametre == KESISIM.varsayilan
    assert all(not a.secim.puanli and a.verim is None for a in y.adimlar)
    assert y.verim is None and y.verim_adim == 0


def test_her_ileri_yurume_penceresinde_en_az_30_kurulum(yuruyus):
    assert len(yuruyus.izgara) == 12
    assert (
        yuruyus.izgara.parametre(yuruyus.izgara.varsayilan_nokta) == KESISIM.varsayilan
    )
    for a in yuruyus.adimlar:
        assert len(a.test.islemler) >= sinama.EN_AZ, a.pencere.ad
        assert (
            a.test.islemler["sinyal_tarihi"]
            .between(a.pencere.test_bas, a.pencere.test_son)
            .all()
        )
    oos = yuruyus.dis_ornek.islemler
    assert len(oos) >= sinama.EN_AZ
    assert list(oos["pencere"].unique()) == [w.ad for w in ayar.PENCERELER]
    assert isinstance(yuruyus.verim, float) and yuruyus.verim_adim == 6
    assert yuruyus.son.puanli


def test_2026_fiyati_ayari_ve_orneklem_disini_degistirmez(yuruyus):
    rng = np.random.default_rng(3)
    bozuk = {}
    for s, g in piyasa().items():
        g = g.copy()
        sonra = g.index >= sinama.SAKLI_BAS
        for c in (
            "aof",
            "yuksek",
            "dusuk",
            "kapanis",
            "ham_yuksek",
            "ham_dusuk",
            "ham_kapanis",
        ):
            g.loc[sonra, c] = rng.uniform(1, 1000, sonra.sum())
        bozuk[s] = g
    y = ayar.yuru(KESISIM, bozuk, isci=1)
    assert y.son.nokta == yuruyus.son.nokta
    np.testing.assert_array_equal(y.son.puan, yuruyus.son.puan)
    pd.testing.assert_frame_equal(y.dis_ornek.islemler, yuruyus.dis_ornek.islemler)


def test_iki_isci_tek_isciyle_ayni_sonucu_verir():
    kucuk = dataclasses.replace(KESISIM, aralik={"teyit_gun": (0, 2)})
    gunler = piyasa(sembol=2, son="2023-12-31")
    bir, iki = (ayar.yuru(kucuk, gunler, isci=n) for n in (1, 2))
    np.testing.assert_array_equal(bir.son.puan, iki.son.puan)
    pd.testing.assert_frame_equal(bir.dis_ornek.islemler, iki.dis_ornek.islemler)


@pytest.mark.parametrize("ad", sorted(STRATEJILER))
def test_kayitli_stratejinin_varsayilanlari_izgarada_ve_izgara_500_altinda(ad):
    assert len(ayar.Izgara(STRATEJILER[ad])) <= 500


def test_izgara_disi_varsayilan_reddedilir():
    with pytest.raises(ValueError):
        ayar.Izgara(dataclasses.replace(OYUNCAK, varsayilan={"a": 4, "b": 1}))


def json_yaz(kok, icerik):
    kok.mkdir(parents=True, exist_ok=True)
    (kok / f"{KESISIM.ad}.json").write_text(json.dumps(icerik), encoding="utf-8")


@pytest.mark.parametrize(
    "parametreler",
    [{"bilinmeyen": 1}, {"cift": "50/200"}],
    ids=["bilinmeyen anahtar", "izgara disi deger"],
)
def test_oku_bilinmeyen_anahtari_ve_izgara_disi_degeri_reddeder(tmp_path, parametreler):
    json_yaz(tmp_path, {"parametreler": parametreler})
    with pytest.raises(veri.VeriHatasi):
        ayar.oku(KESISIM, tmp_path)


def test_oku_nesne_olmayan_jsonu_reddeder(tmp_path):
    json_yaz(tmp_path, [])
    with pytest.raises(veri.VeriHatasi):
        ayar.oku(KESISIM, tmp_path)


def test_yaz_suzgecleri_ve_liste_cikisini_korur_oku_varsayilanlarin_ustune_koyar(
    tmp_path,
):
    assert ayar.oku(KESISIM, tmp_path) is None
    json_yaz(
        tmp_path, {"parametreler": {}, "suzgecler": ["nabiz"], "liste_cikisi": True}
    )
    s = sec(dataclasses.replace(KESISIM, aralik={"teyit_gun": (0, 2)}), [1.0, 1.0])
    yol = ayar.yaz(KESISIM, s, veri_kimligi="20261026-1900", kok=tmp_path)
    metin = yol.read_text(encoding="utf-8")
    icerik = json.loads(metin)
    assert icerik["suzgecler"] == ["nabiz"] and icerik["liste_cikisi"] is True
    assert icerik["puanli"] is True and icerik["n"] == 30 and icerik["puan"] == 1.0
    assert icerik["veri_kimligi"] == "20261026-1900" and icerik["kod_surumu"]
    assert metin.endswith("}\n") and "\r" not in metin
    okunan = ayar.oku(KESISIM, tmp_path)
    assert okunan.parametreler == KESISIM.varsayilan and okunan.tarih == icerik["tarih"]
