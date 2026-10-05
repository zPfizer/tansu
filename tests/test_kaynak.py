"""`kaynak` adaptörü: alan eşleme, şema denetimi, yeniden deneme. Sahte HTTP oturumuyla, ağsız."""

import datetime as dt

import pandas as pd
import pytest

from tansu import kaynak

HAM = {"HGDG_TARIH": "13-08-2024", "HG_KAPANIS": 69.35, "HG_AOF": 69.85, "HG_MAX": 71.9, "HG_MIN": 68.55,
       "HG_HACIM": 360894374.0, "HGDG_KAPANIS": 66.8037, "HGDG_AOF": 67.28, "HGDG_MAX": 69.26,
       "HGDG_MIN": 66.03, "PD": 1.0, "HAO_PD": 2.0, "SERMAYE": 3.0, "END_DEGER": 9999.5}


class Yanit:
    def __init__(self, durum, govde=None):
        self.status_code, self.govde = durum, govde

    def json(self):
        return self.govde


class SahteOturum:
    def __init__(self, yanitlar):
        self.yanitlar, self.cagri, self.headers = list(yanitlar), 0, {}

    def get(self, url, params=None, json=None, timeout=None):
        self.cagri += 1
        return self.yanitlar.pop(0)

    post = get


def test_fiyat_alanlari_proje_adlarina_cevrilir():
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"value": [HAM]})]), bekleme=0)
    f = k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))
    assert f.loc[0, "tarih"] == pd.Timestamp("2024-08-13")
    assert (f.loc[0, "ham_kapanis"], f.loc[0, "kapanis"], f.loc[0, "ham_aof"], f.loc[0, "xu100"]) == (69.35, 66.8037, 69.85, 9999.5)
    assert f.loc[0, "hacim"] == 360894374.0


def test_eksik_alan_sema_hatasidir():
    eksik = {k: v for k, v in HAM.items() if k != "HG_AOF"}
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"value": [eksik]})]), bekleme=0)
    with pytest.raises(kaynak.KaynakHatasi):
        k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))


def test_sonraki_kayitta_eksik_alan_da_sema_hatasidir():
    eksik = {k: v for k, v in HAM.items() if k != "HGDG_KAPANIS"}
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"value": [HAM, eksik]})]), bekleme=0)
    with pytest.raises(kaynak.KaynakHatasi):
        k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 14))


OLAY = '[{"SHT_KODU": "02", "SHHE_TARIH": 1723496400000, "SHHE_FIYAT_AYAR_OR": 0.09090909138724523}]'


def test_olaylar_d_metnini_ham_listeye_cevirir():
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"d": OLAY})]), bekleme=0)
    assert k.olaylar("CCOLA") == [{"SHT_KODU": "02", "SHHE_TARIH": 1723496400000,
                                   "SHHE_FIYAT_AYAR_OR": 0.09090909138724523}]


def test_olay_kaydinda_eksik_alan_sema_hatasidir():
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"d": '[{"SHT_KODU": "02"}]'})]), bekleme=0)
    with pytest.raises(kaynak.KaynakHatasi):
        k.olaylar("CCOLA")


def test_sunucu_hatasinda_yeniden_dener():
    oturum = SahteOturum([Yanit(503), Yanit(429), Yanit(200, {"value": [HAM]})])
    k = kaynak.IsYatirim(oturum=oturum, bekleme=0, deneme_bekleme=(0, 0, 0))
    assert len(k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))) == 1
    assert oturum.cagri == 3


def test_kalici_hatada_yeniden_denemez():
    oturum = SahteOturum([Yanit(404)])
    k = kaynak.IsYatirim(oturum=oturum, bekleme=0, deneme_bekleme=(0, 0, 0))
    with pytest.raises(kaynak.KaynakHatasi):
        k.fiyat("YOK", dt.date(2024, 8, 13), dt.date(2024, 8, 13))
    assert oturum.cagri == 1


def test_uc_denemeden_sonra_vazgecer():
    oturum = SahteOturum([Yanit(500)] * 4)
    k = kaynak.IsYatirim(oturum=oturum, bekleme=0, deneme_bekleme=(0, 0, 0))
    with pytest.raises(kaynak.KaynakHatasi):
        k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))
    assert oturum.cagri == 4


class SahteTcmb:
    def history(self, tur):
        assert tur == "policy"
        return pd.DataFrame({"borrowing": [None, None], "lending": [50.0, 47.5]},
                            index=pd.DatetimeIndex(["2024-03-22", "2024-12-27"], name="date"))


class SahteKap:
    def get_company_details(self, sembol):
        return {"sector": "ULAŞTIRMA VE DEPOLAMA"} if sembol == "THYAO" else {}


def test_borsapy_faiz_tarih_ve_faiz_sutunlarina_cevrilir():
    f = kaynak.Borsapy(tcmb=SahteTcmb(), kap=SahteKap()).faiz()
    assert list(f.columns) == ["tarih", "faiz"]
    assert list(f["tarih"]) == [pd.Timestamp("2024-03-22"), pd.Timestamp("2024-12-27")]
    assert list(f["faiz"]) == [50.0, 47.5]


def test_borsapy_sektor_kap_alanini_dondurur_bos_yanit_hatadir():
    b = kaynak.Borsapy(tcmb=SahteTcmb(), kap=SahteKap())
    assert b.sektor("THYAO") == "ULAŞTIRMA VE DEPOLAMA"
    with pytest.raises(kaynak.KaynakHatasi):
        b.sektor("XXXXX")


def test_onbellekli_kaynak_tamamlanan_sembolu_yeniden_istemez(tmp_path):
    class Say:
        cagri = 0

        def fiyat(self, sembol, bas, son):
            self.cagri += 1
            return pd.DataFrame({"tarih": pd.to_datetime(["2024-08-13"]), "ham_kapanis": [1.5]})

        def olaylar(self, sembol):
            self.cagri += 1
            return [{"SHT_KODU": "02"}]

    ilk = Say()
    a = kaynak.Onbellekli(ilk, tmp_path)
    f1, o1 = a.fiyat("THYAO", None, None), a.olaylar("THYAO")
    assert ilk.cagri == 2
    ikinci = Say()  # süreç yeniden başlar: yeni nesne, aynı klasör
    b = kaynak.Onbellekli(ikinci, tmp_path)
    assert b.fiyat("THYAO", None, None).equals(f1) and b.olaylar("THYAO") == o1
    assert ikinci.cagri == 0


def test_kapanan_tablo_yalniz_pay_kodlarini_2010_ve_sonrasini_alir():
    # Borsa İstanbul IslemSirasiKapananSirketler.xls düzeni: 4 başlık satırı, sonra kod/ad/tarih/açıklama.
    ham = pd.DataFrame([
        ["İŞLEM SIRASI KAPANAN ŞİRKETLER", None, None, None],
        ["COMPANIES WITH EQUITIES DELISTED PERMANENTLY", None, None, None],
        ["PAY KODU", "PAY ADI", "KAPANMA TARİHİ", "AÇIKLAMA"],
        ["CODE", "EQUITY NAME", "DELISTING DATE", "EXPLANATION"],
        ["ROYAL.E", "ROYAL", pd.Timestamp("2026-04-17"), None],          # pay: .E sonekini at
        ["ALBTS.F1", "FON", pd.Timestamp("2026-03-18"), None],           # fon: alma
        ["OLMK.E", "MONDI", pd.Timestamp("2022-10-20"), "birleşmiştir"],
        ["ESKI", "ESKI SIRKET", pd.Timestamp("2009-12-31"), None],       # 2010 öncesi: alma
        ["TARIHSIZ", "TARIHSIZ SIRKET", pd.NaT, None],                   # tarihi yok: al (indirmede boş çıkabilir)
    ])
    t = kaynak.kapanan_tablo(ham)
    assert list(t["kod"]) == ["ROYAL", "OLMK", "TARIHSIZ"]
    assert list(t["aciklama"].fillna("")) == ["", "birleşmiştir", ""]


def test_fiyat_kaynak_sirasi_bozuksa_tarihe_gore_siralanir():
    sonra, once = dict(HAM, HGDG_TARIH="14-08-2024"), dict(HAM, HGDG_TARIH="13-08-2024")
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"value": [sonra, once]})]), bekleme=0)
    f = k.fiyat("GARAN", dt.date(2024, 8, 13), dt.date(2024, 8, 14))
    assert list(f["tarih"]) == [pd.Timestamp("2024-08-13"), pd.Timestamp("2024-08-14")]
    assert list(f.index) == [0, 1]
