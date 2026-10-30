from collections import Counter

import numpy as np
import pandas as pd
import pytest

from tansu import islem, rapor, sinama
from tansu.strateji import Strateji, bos_sinyal
from tests.sentetik import gun_tablosu


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
    dilim = sinama.Kosu(islemler, sinyaller, Counter(a=1), "R").kes(
        pd.Timestamp("2023-01-01"), pd.Timestamp("2023-06-30")
    )
    assert list(dilim.islemler["cikis_tarihi"]) == [pd.Timestamp("2023-08-15")]
    assert len(dilim.sinyaller) == 1 and dilim.sayac == Counter()
    assert dilim.olcu == "R"


def test_yil_takvim_yilinin_ilk_ve_son_gununu_icerir_komsu_yillari_dislar():
    gunler = pd.to_datetime(["2022-12-31", "2023-01-01", "2023-12-31", "2024-01-01"])
    islemler = pd.DataFrame({"sinyal_tarihi": gunler, "R": [1.0, 2.0, 4.0, 8.0]})
    sinyaller = pd.DataFrame({"sembol": "A", "tarih": gunler})
    yil = sinama.Kosu(islemler, sinyaller, Counter(), "R").yil(2023)
    assert list(yil.islemler["R"]) == [2.0, 4.0]
    assert list(yil.sinyaller["tarih"]) == list(gunler[1:3])
    assert yil.olcu == "R"


def test_toplam_olcu_sutununun_toplami_bos_kosuda_sifir():
    islemler = pd.DataFrame({"R": [1.0, 2.5], "net_yuzde": [10.0, 20.0]})
    bos = pd.DataFrame(columns=["sembol", "tarih"])
    assert sinama.Kosu(islemler, bos, Counter(), "net_yuzde").toplam == 30.0
    kayit = islem.kayit_tablosu([], islem.Cikis())
    assert sinama.Kosu(kayit, bos, Counter(), "R").toplam == 0.0


def tavansiz_satir_icin_piyasa():
    dolan = gun_tablosu(
        [11, 10.2, 12.2, 13.2, 13.2],
        yuksek=[11.1, 10.5, 12.5, 13.5, 13.3],
        dusuk=[10.9, 9.8, 10.3, 12.3, 13.1],
    )
    dolmayan = gun_tablosu([11, 10.5, 10.6, 10.7, 10.7])
    piyasa = {
        "tavan_dolan": dolan.copy(),
        "tavan_dolmayan": dolmayan,
        "siradan": dolan.copy(),
    }
    for sembol in ("tavan_dolan", "tavan_dolmayan"):
        piyasa[sembol].iloc[0, piyasa[sembol].columns.get_loc("tavan_kapanis")] = True
    return piyasa


def ilk_gun_limit_stratejisi():
    cikis = islem.Cikis("dokunus", (("hedef1", 0.5), ("hedef2", 0.5)))

    def hesapla(gun, p):
        s = bos_sinyal(gun.index)
        s.iloc[
            0, s.columns.get_indexer(["giris", "giris_tur", "seviye", "gecerlilik"])
        ] = [True, "limit", 10.0, 2]
        s.iloc[0, s.columns.get_indexer(["stop", "hedef1", "hedef2"])] = [
            9.0,
            12.0,
            13.0,
        ]
        return s

    return Strateji("t", "giris", "a", "gunluk", (), (), {}, {}, (), cikis, hesapla)


def test_uye_olmayan_gundeki_sinyal_ne_sinyal_ne_islem_olur():
    dolan = tavansiz_satir_icin_piyasa()["siradan"]
    piyasa = {"uye": dolan.copy(), "disari": dolan.copy()}
    piyasa["disari"].iloc[0, piyasa["disari"].columns.get_loc("uye")] = False

    k = sinama.calistir(ilk_gun_limit_stratejisi(), piyasa, {}, sinama.GECMIS)

    assert list(k.sinyaller["sembol"]) == ["uye"]
    assert list(k.islemler["sembol"]) == ["uye"]
    assert sum(k.sayac.values()) == 0


def test_tavansiz_satir_dolmayan_tavan_sinyalini_de_dusurur():
    k = sinama.calistir(
        ilk_gun_limit_stratejisi(), tavansiz_satir_icin_piyasa(), {}, sinama.GECMIS
    )
    donem = sinama.donemler(k)

    assert (donem["Bütün yıllar"].sinyal, donem["Bütün yıllar"].dolum) == (3, 2)
    tavansiz = donem["Bütün yıllar, tavan kapanışsız"]
    assert (tavansiz.sinyal, tavansiz.dolum) == (1, 1)
    assert rapor._ozet_sutunu(tavansiz, "R")["Düşen"] == "0 (0%)"


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


def kurulumlar(n):
    return kayitlar(n).assign(
        tutma_gun=1,
        acik=False,
        dolumda_stop=False,
        risk_tabanli=False,
        cikis_tarihi=pd.date_range("2022-01-03", periods=n),
        dolum_tarihi=pd.date_range("2022-01-03", periods=n),
        sembol="A",
    )


def test_ileri_tablo_ufuk_basina_ortalama_medyan_pozitif_pay_ve_n():
    satir = {i.ufuk: i for i in sinama.ileri_tablo(kayitlar(31))}
    assert satir[1].n == 31 and satir[10].n == 30
    assert satir[3].ortalama == pytest.approx(3 / 31)
    assert satir[1].medyan == 1.0 and satir[1].pozitif == pytest.approx(16 / 31)
    assert satir["MFE"].medyan == 4.0 and satir["MAE"].medyan == 2.0
    assert satir["MFE"].ortalama is None and satir["MFE"].pozitif is None


def test_ileri_tablo_n_ufku_dolu_kurulum_sayisi():
    assert sinama.ileri_tablo(kayitlar(5))[0].n == 5
    assert sinama.ileri_tablo(islem.kayit_tablosu([], islem.Cikis()))[0].n == 0


def test_ozet_yalniz_olcu_sutununu_okur():
    o = sinama.ozet(kurulumlar(3), 3, "net_yuzde")
    assert o.dolum == 3 and o.toplam == 1.0 and o.beklenti == pytest.approx(1 / 3)


def test_rapor_satirlari_olcuyu_bugunku_metinle_yazar():
    d = rapor._ozet_sutunu(sinama.ozet(kurulumlar(3), 3, "net_yuzde"), "%")
    assert d["Toplam %"] == "1.00" and "Toplam R" not in d
    assert d["Beklenti (ortalama %)"] == "n/a (N = 3)"
    kayipsiz = kurulumlar(30).assign(R=np.arange(1.0, 31.0))
    kazanc = rapor._ozet_sutunu(sinama.ozet(kayipsiz, 30, "R"), "R")
    assert kazanc["Kâr faktörü"] == "n/a" and kazanc["Toplam R"] == "465.00"
    bos = rapor._ozet_sutunu(
        sinama.ozet(islem.kayit_tablosu([], islem.Cikis()), 0, "R"), "R"
    )
    assert bos["Düşen"] == "0" and bos["Ortalama tutma günü"] == "-"
    assert bos["Sinyal"] == 0 and type(bos["Açık işlem"]) is int
    ileri = map(rapor._ileri_satiri, sinama.ileri_tablo(kayitlar(31)))
    satir = {s["Ufuk (gün)"]: s for s in ileri}
    assert satir[3]["Ortalama net %"] == f"{3 / 31:.2f}"
    assert satir[1]["Medyan net %"] == "1.00" and satir[1]["Pozitif payı"] == "52%"
    assert satir["Medyan MFE % (10 gün)"]["Medyan net %"] == "4.00"
    assert satir["Medyan MAE % (10 gün)"]["Pozitif payı"] == "-"
    az = rapor._ileri_satiri(sinama.ileri_tablo(kayitlar(5))[0])
    assert az["Ortalama net %"] == "n/a (N = 5)"


def test_dusus_nan_degeri_atlar():
    assert sinama.dusus([1.0, -2.0, np.nan, -1.0]) == 3.0
