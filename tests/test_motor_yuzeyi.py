"""`kanit/` altındaki Gartley betikleri tansu'nun bu adlarını kullanır."""

import inspect
from collections import Counter
from datetime import tzinfo
from functools import reduce
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from tansu import gostergeler, islem, kaynak, sinama, strateji, veri, yapi
from tansu.stratejiler import gartley
from tests.sentetik import gartley_yolu, gun_tablosu
from tests.test_islem import CIKIS, maliyetli, sinyal
from tests.test_veri_gunluk import sentetik_anlik

MODULLER = {
    m.__name__.rsplit(".", 1)[-1]: m
    for m in (gostergeler, islem, kaynak, sinama, strateji, veri, yapi, gartley)
}
OZETLENEN_MODULLER = (gostergeler, islem, sinama, strateji, veri, yapi, gartley)
BETIK_CAGRILARI = [
    ("veri.indir", 3, ("bas", "kapanan")),
    ("veri.oku", 2, ()),
    ("sinama.gunler", 1, ()),
    ("sinama.Donem", 2, ()),
    ("kaynak.kapanan_kodlar", 1, ()),
    ("kaynak.sirket_kodlari", 0, ()),
    ("kaynak.IsYatirim", 0, ()),
    ("kaynak.IsYatirim.fiyat", 4, ()),
    ("kaynak.IsYatirim.olaylar", 2, ()),
    ("kaynak.Artimli", 2, ()),
    ("kaynak.Borsapy", 0, ()),
    ("kaynak.Borsapy.faiz", 1, ()),
    ("strateji.bos_sinyal", 1, ()),
    ("gostergeler.rsi", 2, ()),
    ("gostergeler.sma", 2, ()),
    ("gostergeler.atr_basit", 3, ()),
    ("yapi.sag_bar_pivotlari", 3, ()),
    ("yapi.ardisik", 1, ()),
    ("gartley.STRATEJI.sinyal", 2, ()),
    ("gartley.uyar", 4, ()),
]
GARTLEY_P = {**gartley.STRATEJI.varsayilan, "rr_min": "kapali"}
GUN_SUTUNLARI = {
    "atr",
    "uye",
    "kapanis",
    "yuksek",
    "dusuk",
    "hacim",
    "ham_kapanis",
    "xu100",
}
SINYAL_SUTUNLARI = {
    "giris",
    "giris_tur",
    "seviye",
    "gecerlilik",
    "stop",
    "hedef1",
    "hedef2",
    "hedef3",
    "kural_durumu",
    "tekrar",
}
ADIM_BEKLENEN = [
    (19.99, 0.01, 0.01),
    (20.0, 0.02, 0.02),
    (49.99, 0.02, 0.02),
    (50.0, 0.05, 0.05),
    (99.99, 0.05, 0.05),
    (100.0, 0.1, 0.1),
    (249.99, 0.1, 0.1),
    (250.0, 0.25, 0.1),
    (499.99, 0.25, 0.1),
    (500.0, 0.5, 0.1),
    (999.99, 0.5, 0.1),
    (1000.0, 1.0, 0.1),
    (2499.99, 1.0, 0.1),
    (2500.0, 2.5, 0.1),
]


def nesne(ad):
    ilk, *kalan = ad.split(".")
    return reduce(getattr, kalan, MODULLER[ilk])


def tablo(gunler=(0,), karantinali=()):
    g = gun_tablosu(
        [11, 10.2, 12.2, 13.2, 13.2, 11, 11, 11],
        yuksek=[11.1, 10.5, 12.5, 13.5, 13.3, 11.05, 11.05, 11.05],
        dusuk=[10.9, 9.8, 10.3, 12.3, 13.1, 10.95, 10.95, 10.95],
    )
    g.iloc[list(karantinali), g.columns.get_loc("karantina")] = True
    return g, sinyal(g, gunler=gunler)


def test_simule_red_nedenini_ve_oynayi_modul_adiyla_sirayla_cagirir(monkeypatch):
    g, s = tablo(gunler=(0, 5), karantinali=(5,))
    cagrilar = []
    gercek_red, gercek_oyna = islem._red_nedeni, islem.oyna

    def red_kaydi(*arg):
        cagrilar.append(("red", arg))
        return gercek_red(*arg)

    def oyna_kaydi(*arg):
        cagrilar.append(("oyna", arg))
        return gercek_oyna(*arg)

    monkeypatch.setattr(islem, "_red_nedeni", red_kaydi)
    monkeypatch.setattr(islem, "oyna", oyna_kaydi)
    kayitlar, sayac = islem.simule(g, s, CIKIS, sembol="AAA", strateji="t", sinif="a")

    assert [
        (ad, arg[0].name if ad == "red" else arg[2].name) for ad, arg in cagrilar
    ] == [
        ("red", g.index[0]),
        ("oyna", g.index[0]),
        ("red", g.index[5]),
    ]
    for ad, arg in cagrilar:
        if ad == "red":
            satir, gun_satiri, acik_var, cikis = arg
            assert isinstance(satir, pd.Series) and satir["giris"]
            assert isinstance(gun_satiri, pd.Series) and gun_satiri.name == satir.name
            assert isinstance(acik_var, bool | np.bool_) and not acik_var
            assert cikis is CIKIS
    motor, i, satir, cikis, taban, oyna_sayac = cagrilar[1][1]
    assert isinstance(motor, islem.Gun) and i == 0 and cikis is CIKIS
    assert isinstance(satir, pd.Series) and satir["giris"]
    assert taban == pytest.approx(islem.RISK_TABANI * 0.1)
    assert oyna_sayac is sayac and len(kayitlar) == 1
    assert sayac[islem.KALITE] == 1
    kayit = kayitlar[0]
    assert kayit["sinyal_tarihi"] == g.index[0]
    assert (kayit["stop"], kayit["dolum_fiyati"], kayit["seviye"]) == (9.0, 10.0, 10.0)


def test_red_nedeni_dogrudan_cagrida_str_ya_da_none_verir():
    g, s = tablo(gunler=(0, 5), karantinali=(5,))
    temiz = islem._red_nedeni(s.iloc[0], g.iloc[0], False, CIKIS)
    karantina = islem._red_nedeni(s.iloc[5], g.iloc[5], False, CIKIS)
    acik = islem._red_nedeni(s.iloc[0], g.iloc[0], True, CIKIS)
    assert temiz is None
    assert karantina == islem.KALITE and isinstance(karantina, str)
    assert acik == islem.ACIK_VAR and isinstance(acik, str)


@pytest.mark.parametrize(
    ("gecerlilik", "neden"),
    [(2, islem.SURE_DOLDU), (10, islem.VERI_SONU)],
    ids=["sure-doldu", "veri-sonu"],
)
def test_oyna_emir_dusunce_tam_bir_sayac_artar(gecerlilik, neden):
    g = gun_tablosu([11, 10.5, 10.6, 10.7, 10.7])
    s = sinyal(g, gecerlilik=gecerlilik)
    sayac = Counter()
    e, son = islem.oyna(islem.Gun(g, s), 0, s.iloc[0], CIKIS, 0.05, sayac)
    assert e is None and isinstance(son, int)
    assert sum(sayac.values()) == 1 and sayac[neden] == 1


def test_acik_gun_kancasi_satiri_yazilabilir_alanlari_ve_kapatmayi_gorur(monkeypatch):
    g, s = tablo()
    s["stop_atr"] = 1.5
    cagrilar, islemler = [], []

    def kanca(e, i, gun, cikis):
        cagrilar.append((i, gun, cikis))
        islemler.append(e)
        assert set(s.columns) <= set(e.satir.index)
        assert e.satir["stop_atr"] == 1.5 and e.satir["hedef1"] == 12.0
        if len(cagrilar) == 1:
            e.stop, e.risk, e.bekleyen = 9.5, 2.0, "kanca"
            return False
        assert e.stop == 9.5 and e.risk == 2.0 and e.bekleyen == "kanca"
        return islem._kapat(e, i, 10.5, e.bekleyen)

    monkeypatch.setattr(islem, "_acik_gun", kanca)
    (k,), _ = islem.simule(g, s, CIKIS, sembol="AAA", strateji="t", sinif="a")

    assert [i for i, _, _ in cagrilar] == [1, 2]
    assert all(isinstance(gun, islem.Gun) and c is CIKIS for _, gun, c in cagrilar)
    assert all(e is islemler[0] and isinstance(e, islem._Islem) for e in islemler)
    assert k["stop"] == 9.5 and k["cikis_nedeni"] == "kanca"
    assert k["cikis_fiyati"] == 10.5
    assert k["R"] == pytest.approx(maliyetli(10.0, 10.5) / 2.0)
    assert islem.sonuc(islemler[0]).R == pytest.approx(k["R"])


def test_acik_gun_kancasi_islem_alanlarini_ve_parcalari_gorur(monkeypatch):
    g, s = tablo()
    gercek = islem._acik_gun
    gorulen = []

    def kanca(e, i, gun, cikis):
        once = list(e.parcalar)
        kapandi = gercek(e, i, gun, cikis)
        gorulen.append((i, e.dolum_i, e.giris, e.risk_tabani, once, list(e.parcalar)))
        return kapandi

    monkeypatch.setattr(islem, "_acik_gun", kanca)
    taban = islem.RISK_TABANI * 0.1
    e, son = islem.oyna(islem.Gun(g, s), 0, s.iloc[0], CIKIS, taban, Counter())

    assert isinstance(e, islem._Islem) and isinstance(son, int)
    hedef1, hedef2 = (2, 12.0, 0.5, "hedef1"), (3, 13.0, 0.5, "hedef2")
    assert [(i, once, sonra) for i, *_, once, sonra in gorulen] == [
        (1, [], []),
        (2, [], [hedef1]),
        (3, [hedef1], [hedef1, hedef2]),
    ]
    assert all(
        (dolum_i, giris, risk_tabani) == (1, 10.0, taban)
        for _, dolum_i, giris, risk_tabani, *_ in gorulen
    )


def test_gun_motor_dizilerini_gun_basina_bir_ogeyle_verir():
    g = gun_tablosu([11, 10.2, 12.2, 13.2], aof=[11.5, 10.1, 12.1, 13.1])
    g["atr"] = [0.1, 0.2, 0.3, 0.4]
    g.iloc[2, g.columns.get_loc("kilit_taban")] = True
    motor = islem.Gun(g, sinyal(g))
    for ad, sutun in (("aof", "aof"), ("kap", "kapanis"), ("atr", "atr")):
        dizi = getattr(motor, ad)
        assert isinstance(dizi, np.ndarray) and dizi.shape == (len(g),)
        np.testing.assert_array_equal(dizi, g[sutun].to_numpy(float))
    assert isinstance(motor.taban_kilit, np.ndarray)
    assert motor.taban_kilit.tolist() == [False, False, True, False]


def test_betiklerin_okudugu_sabitler_ve_cikis_kurucusu_var():
    hedef = (("hedef1", 1.0),)
    cikis = islem.Cikis("dokunus", hedef)
    assert (cikis.stop_mod, cikis.hedef) == ("dokunus", hedef)
    assert islem.RISK_TABANI > 0 and islem.MALIYET > 0
    assert isinstance(islem.VERI_SONU, str)


@pytest.mark.parametrize(
    ("ad", "konumsal", "anahtar"),
    BETIK_CAGRILARI,
    ids=[c[0] for c in BETIK_CAGRILARI],
)
def test_betiklerin_cagri_bicimi_imzaya_uyar(ad, konumsal, anahtar):
    inspect.signature(nesne(ad)).bind(*[None] * konumsal, **dict.fromkeys(anahtar))


@pytest.mark.parametrize("modul", OZETLENEN_MODULLER, ids=lambda m: m.__name__)
def test_ozetlenen_modul_kendi_adli_duz_dosyadir(modul):
    assert Path(modul.__file__).name == modul.__name__.rsplit(".", 1)[-1] + ".py"


def test_betiklerin_okudugu_sabitler_var_ve_adim_tablolari_tutarli():
    assert isinstance(veri.ISTANBUL, tzinfo)
    assert isinstance(veri.ADIM_DEGISIM, pd.Timestamp)
    assert len(veri.ADIM_YENI) == len(veri.ADIM_ESKI) == len(veri.ADIM_ESIK) + 1
    assert isinstance(sinama.ILK_GIRIS, pd.Timestamp)
    assert isinstance(sinama.KESIM, pd.Timestamp) and sinama.ILK_GIRIS < sinama.KESIM
    assert isinstance(gartley.AB_XA, float) and isinstance(gartley.D_XA, float)
    assert len(gartley.BC_AB) == len(gartley.CD_BC) == 2


def test_gartley_modul_degiskenlerini_cagri_aninda_okur(monkeypatch):
    gun = gun_tablosu(gartley_yolu())
    monkeypatch.setattr(gartley, "D_XA", 0.8)
    (seviye,) = gartley.STRATEJI.sinyal(gun, GARTLEY_P).query("giris")["seviye"]
    assert seviye == pytest.approx(20.05 - 0.8 * (20.05 - 9.95))


@pytest.mark.parametrize(
    ("ad", "deger"),
    [("uyar", lambda ab, bc, cd, tol: False), ("AB_XA", 0.9)],
    ids=["uyar", "AB_XA"],
)
def test_gartley_yer_degistiren_ad_ve_sabit_sinyali_etkiler(monkeypatch, ad, deger):
    gun = gun_tablosu(gartley_yolu())
    assert gartley.STRATEJI.sinyal(gun, GARTLEY_P)["giris"].any()
    monkeypatch.setattr(gartley, ad, deger)
    assert not gartley.STRATEJI.sinyal(gun, GARTLEY_P)["giris"].any()


def test_gosterge_ve_pivot_ciktilari_betigin_okudugu_biciminde():
    g = gun_tablosu(gartley_yolu())
    for seri in (
        gostergeler.rsi(g["kapanis"], 14),
        gostergeler.sma(g["kapanis"], 50),
        gostergeler.atr_basit(g["yuksek"], g["dusuk"], g["kapanis"]),
    ):
        assert isinstance(seri, pd.Series) and seri.index.equals(g.index)
    siralar = list(yapi.ardisik(yapi.sag_bar_pivotlari(g["yuksek"], g["dusuk"], 15)))
    assert siralar
    for sira in siralar:
        assert isinstance(sira, tuple)
        for p in sira:
            assert isinstance(p, yapi.Pivot)
            assert p.tur in ("T", "D") and p.onay_gun >= p.pivot_gun
            assert isinstance(p.fiyat, float)


def test_anlik_ve_gun_tablolari_betiklerin_okudugu_alanlari_verir():
    a = sentetik_anlik()
    assert isinstance(a.kimlik, str) and isinstance(a.gunler, pd.DatetimeIndex)
    assert "tarih" in a.fiyat and len(a.fiyat.groupby("tarih").size()) == len(a.gunler)
    assert len(a.inmeyen) == len(a.bos) == 0
    assert isinstance(a.kaynak_gunleri, list)
    tablolar = sinama.gunler(a)
    assert set(tablolar) == {"AAA", "TRALT"}
    son = a.gunler[1]
    for t in tablolar.values():
        assert GUN_SUTUNLARI <= set(t.columns)
        assert t["uye"].dtype == bool
        assert all(pd.api.types.is_float_dtype(t[a]) for a in GUN_SUTUNLARI - {"uye"})
        assert t.loc[:son].index[-1] == son
        assert np.isscalar(t.at[son, "atr"])
    donem = sinama.Donem(a.gunler[0], son)
    assert (donem.bas, donem.son) == (a.gunler[0], son)


def test_adim_esikleri_artan_sirada():
    assert veri.ADIM_ESIK == sorted(set(veri.ADIM_ESIK))


@pytest.mark.parametrize(("ham", "yeni", "eski"), ADIM_BEKLENEN)
def test_fiyat_adimi_para_katmaninin_aramasinda_esikte_ust_dilime_girer(
    ham, yeni, eski
):
    for tablo, beklenen in ((veri.ADIM_YENI, yeni), (veri.ADIM_ESKI, eski)):
        tik = tablo[np.searchsorted(veri.ADIM_ESIK, ham, side="right")]
        assert tik == beklenen


def test_gartley_sinyali_betiklerin_okudugu_sutunlari_verir():
    gun = gun_tablosu(gartley_yolu())
    s = gartley.STRATEJI.sinyal(gun, GARTLEY_P)
    for kare in (strateji.bos_sinyal(gun.index), s):
        assert SINYAL_SUTUNLARI <= set(kare.columns) and kare.index.equals(gun.index)
    assert s["giris"].dtype == bool
    (t,) = np.flatnonzero(s["giris"])
    assert s["giris_tur"].iat[t] == "limit"
    for a in ("seviye", "stop", "hedef1", "hedef2", "hedef3"):
        assert np.isfinite(float(s[a].iat[t]))
    assert isinstance(s["kural_durumu"].iat[t], str) and s["kural_durumu"].iat[t]
    s.loc[s["giris"], ["giris", "tekrar"]] = [False, 0]
    assert not s["giris"].any()


def test_kapanan_kodlar_kod_ve_tarih_sutunlarini_verir(monkeypatch):
    ham = pd.DataFrame(
        [
            ["BASLIK", None, None, None],
            ["TITLE", None, None, None],
            ["PAY KODU", "PAY ADI", "KAPANMA TARİHİ", "AÇIKLAMA"],
            ["CODE", "EQUITY NAME", "DELISTING DATE", "EXPLANATION"],
            ["ROYAL.E", "ROYAL", pd.Timestamp("2026-04-17"), None],
            ["TARIHSIZ", "TARIHSIZ SIRKET", pd.NaT, None],
        ]
    )

    class Oturum:
        def get(self, url, timeout=None, headers=None):
            return SimpleNamespace(status_code=200, content=b"")

    monkeypatch.setattr(pd, "read_excel", lambda *arg, **kw: ham)
    kapanan = kaynak.kapanan_kodlar(Oturum())
    assert {"kod", "tarih"} <= set(kapanan.columns)
    assert kapanan["kod"].tolist() == ["ROYAL", "TARIHSIZ"]
    assert pd.api.types.is_datetime64_any_dtype(kapanan["tarih"])
    sonra = kapanan[~(kapanan["tarih"] < pd.Timestamp("2024-01-01"))]
    assert sonra["kod"].tolist() == ["ROYAL", "TARIHSIZ"]
