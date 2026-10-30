"""`kaynak` adaptörü: alan eşleme, şema denetimi, yeniden deneme. Sahte HTTP oturumuyla, ağsız."""

import ast
import datetime as dt
import logging
import re
from pathlib import Path

import borsapy
import pandas as pd
import pytest
import requests

from tansu import kaynak
from tansu.__main__ import main

HAM = {
    "HGDG_TARIH": "13-08-2024",
    "HG_KAPANIS": 69.35,
    "HG_AOF": 69.85,
    "HG_MAX": 71.9,
    "HG_MIN": 68.55,
    "HG_HACIM": 360894374.0,
    "HGDG_KAPANIS": 66.8037,
    "HGDG_AOF": 67.28,
    "HGDG_MAX": 69.26,
    "HGDG_MIN": 66.03,
    "PD": 1.0,
    "HAO_PD": 2.0,
    "SERMAYE": 3.0,
    "END_DEGER": 9999.5,
}


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
        y = self.yanitlar.pop(0)
        if isinstance(y, Exception):
            raise y
        return y

    post = get


def test_fiyat_alanlari_proje_adlarina_cevrilir():
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"value": [HAM]})]), bekleme=0)
    f = k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))
    assert f.loc[0, "tarih"] == pd.Timestamp("2024-08-13")
    assert (
        f.loc[0, "ham_kapanis"],
        f.loc[0, "kapanis"],
        f.loc[0, "ham_aof"],
        f.loc[0, "xu100"],
    ) == (69.35, 66.8037, 69.85, 9999.5)
    assert f.loc[0, "hacim"] == 360894374.0


def test_eksik_alan_sema_hatasidir():
    eksik = {k: v for k, v in HAM.items() if k != "HG_AOF"}
    k = kaynak.IsYatirim(
        oturum=SahteOturum([Yanit(200, {"value": [eksik]})]), bekleme=0
    )
    with pytest.raises(kaynak.KaynakHatasi):
        k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))


def test_sonraki_kayitta_eksik_alan_da_sema_hatasidir():
    eksik = {k: v for k, v in HAM.items() if k != "HGDG_KAPANIS"}
    k = kaynak.IsYatirim(
        oturum=SahteOturum([Yanit(200, {"value": [HAM, eksik]})]), bekleme=0
    )
    with pytest.raises(kaynak.KaynakHatasi):
        k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 14))


OLAY = '[{"SHT_KODU": "02", "SHHE_TARIH": 1723496400000, "SHHE_FIYAT_AYAR_OR": 0.09090909138724523}]'


def test_olaylar_d_metnini_ham_listeye_cevirir():
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"d": OLAY})]), bekleme=0)
    assert k.olaylar("CCOLA") == [
        {
            "SHT_KODU": "02",
            "SHHE_TARIH": 1723496400000,
            "SHHE_FIYAT_AYAR_OR": 0.09090909138724523,
        }
    ]


def test_olay_kaydinda_eksik_alan_sema_hatasidir():
    k = kaynak.IsYatirim(
        oturum=SahteOturum([Yanit(200, {"d": '[{"SHT_KODU": "02"}]'})]), bekleme=0
    )
    with pytest.raises(kaynak.KaynakHatasi):
        k.olaylar("CCOLA")


def test_sunucu_hatasinda_yeniden_dener():
    oturum = SahteOturum([Yanit(503), Yanit(429), Yanit(200, {"value": [HAM]})])
    k = kaynak.IsYatirim(oturum=oturum, bekleme=0, deneme_bekleme=(0, 0, 0))
    assert len(k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))) == 1
    assert oturum.cagri == 3


def test_kopan_baglantida_yeniden_dener():
    # Bütün BIST indirmesi A1CAP'ta yanıt gövdesi yarıda kopunca durdu (28.10.2026).
    kopan = requests.exceptions.ChunkedEncodingError("Connection broken")
    oturum = SahteOturum([kopan, Yanit(200, {"value": [HAM]})])
    k = kaynak.IsYatirim(oturum=oturum, bekleme=0, deneme_bekleme=(0, 0, 0))
    assert len(k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))) == 1
    assert oturum.cagri == 2


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
        return pd.DataFrame(
            {"borrowing": [None, None], "lending": [50.0, 47.5]},
            index=pd.DatetimeIndex(["2024-03-22", "2024-12-27"], name="date"),
        )


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
            return pd.DataFrame(
                {"tarih": pd.to_datetime(["2024-08-13"]), "ham_kapanis": [1.5]}
            )

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


class Akan:
    """Sahte kaynak: `tablo` kaynağın bugünkü bütün geçmişidir; istenen aralığı verir, istekleri yazar."""

    def __init__(self, tablo):
        self.tablo, self.istekler, self.olay_istegi = tablo, [], 0

    def fiyat(self, sembol, bas, son):
        self.istekler.append(bas)
        t = self.tablo
        return t[t["tarih"].between(pd.Timestamp(bas), pd.Timestamp(son))].reset_index(
            drop=True
        )

    def olaylar(self, sembol):
        self.olay_istegi += 1
        return [{"SHT_KODU": "02", "n": self.olay_istegi}]


def gecmis(n, carpan=1.0):
    t = pd.bdate_range("2024-01-01", periods=n)
    return pd.DataFrame(
        {"tarih": t, "ham_kapanis": 10.0 + pd.RangeIndex(n), "kapanis": carpan * 10.0}
    )


BAS, SON = dt.date(2019, 1, 1), dt.date(2030, 1, 1)


def test_artimli_kaynak_ikinci_kosuda_yalniz_son_gunleri_ister(tmp_path):
    ilk = Akan(gecmis(30))
    i = kaynak.Artimli(ilk, tmp_path)
    ilk_f, _ = i.fiyat("AKBNK", BAS, SON), i.olaylar("AKBNK")
    assert ilk.istekler == [BAS] and len(ilk_f) == 30 and i.sayac == {"tam": 1}

    yeni = gecmis(32)
    yeni.loc[29, "ham_kapanis"] = (
        99.0  # önbelleğin son günü seans içiydi; kaynak düzeltti
    )
    ikinci = Akan(yeni)
    a = kaynak.Artimli(ikinci, tmp_path)
    f = a.fiyat("AKBNK", BAS, SON)
    assert ikinci.istekler == [ilk_f["tarih"].iloc[-kaynak.Artimli.ORTUSME].date()]
    pd.testing.assert_frame_equal(f, yeni)
    assert a.olaylar("AKBNK") == [{"SHT_KODU": "02", "n": 1}]  # önbellekten
    assert ikinci.olay_istegi == 0 and a.sayac == {"artimli": 1}


def test_artimli_kaynak_gecmis_degisince_butun_gecmisi_ve_olaylari_yeniden_ister(
    tmp_path,
):
    ilk = kaynak.Artimli(Akan(gecmis(30)), tmp_path)
    ilk.fiyat("AKBNK", BAS, SON), ilk.olaylar("AKBNK")
    # yeni temettü düzeltilmiş geçmişi değiştirir
    duzeltilmis = Akan(gecmis(31, carpan=0.9))
    a = kaynak.Artimli(duzeltilmis, tmp_path)
    f = a.fiyat("AKBNK", BAS, SON)
    assert duzeltilmis.istekler[-1] == BAS
    pd.testing.assert_frame_equal(f, gecmis(31, carpan=0.9))
    assert a.olaylar("AKBNK") == [{"SHT_KODU": "02", "n": 1}]
    assert duzeltilmis.olay_istegi == 1 and a.sayac == {"tam": 1}
    b = kaynak.Artimli(Akan(gecmis(31, carpan=0.9)), tmp_path)
    pd.testing.assert_frame_equal(b.fiyat("AKBNK", BAS, SON), f)  # önbellek güncellendi
    assert b.sayac == {"artimli": 1}


def onbellekle(tmp_path, tablo):
    a = kaynak.Artimli(Akan(tablo), tmp_path)
    a.fiyat("AKBNK", BAS, SON), a.olaylar("AKBNK")


class KisaBos(Akan):
    """Kısa aralığa boş yanıt (ALARK benzeri kaynak aksaklığı); bütün geçmiş isteği çalışır."""

    def fiyat(self, sembol, bas, son):
        f = super().fiyat(sembol, bas, son)
        return f if bas == BAS else f.iloc[:0]


def test_artimli_kaynak_bos_yanitta_tam_iner_bos_sutunda_artimli_kalir(tmp_path):
    onbellekle(tmp_path, gecmis(30))
    a = kaynak.Artimli(KisaBos(gecmis(31)), tmp_path)
    assert len(a.fiyat("AKBNK", BAS, SON)) == 31 and a.sayac == {"tam": 1}

    onbellekle(
        tmp_path / "b", gecmis(30).assign(pd=None)
    )  # ince hissede bütünüyle boş alan
    b = kaynak.Artimli(Akan(gecmis(31).assign(pd=None)), tmp_path / "b")
    assert len(b.fiyat("AKBNK", BAS, SON)) == 31 and b.sayac == {"artimli": 1}


class OlaySiz(Akan):
    def olaylar(self, sembol):
        raise kaynak.KaynakHatasi(f"{sembol}: olay yok")


def test_artimli_kaynak_olay_alinamazsa_fiyat_onbellegi_eskide_kalir(tmp_path):
    onbellekle(tmp_path, gecmis(30))
    a = kaynak.Artimli(OlaySiz(gecmis(31, carpan=0.9)), tmp_path)
    a.fiyat("AKBNK", BAS, SON)
    with pytest.raises(kaynak.KaynakHatasi):
        a.olaylar("AKBNK")
    b = kaynak.Artimli(Akan(gecmis(31, carpan=0.9)), tmp_path)
    b.fiyat("AKBNK", BAS, SON)
    assert b.sayac == {"tam": 1}  # bölünme olayı yeniden istenir, eski olay kalmaz
    assert b.olaylar("AKBNK") == [{"SHT_KODU": "02", "n": 1}]
    assert not list(tmp_path.glob("*.tmp"))


def test_kapanan_tablo_yalniz_pay_kodlarini_2010_ve_sonrasini_alir():
    # Borsa İstanbul IslemSirasiKapananSirketler.xls düzeni: 4 başlık satırı, sonra kod/ad/tarih/açıklama.
    ham = pd.DataFrame(
        [
            ["İŞLEM SIRASI KAPANAN ŞİRKETLER", None, None, None],
            ["COMPANIES WITH EQUITIES DELISTED PERMANENTLY", None, None, None],
            ["PAY KODU", "PAY ADI", "KAPANMA TARİHİ", "AÇIKLAMA"],
            ["CODE", "EQUITY NAME", "DELISTING DATE", "EXPLANATION"],
            [
                "ROYAL.E",
                "ROYAL",
                pd.Timestamp("2026-04-17"),
                None,
            ],  # pay: .E sonekini at
            ["ALBTS.F1", "FON", pd.Timestamp("2026-03-18"), None],  # fon: alma
            ["OLMK.E", "MONDI", pd.Timestamp("2022-10-20"), "birleşmiştir"],
            [
                "ESKI",
                "ESKI SIRKET",
                pd.Timestamp("2009-12-31"),
                None,
            ],  # 2010 öncesi: alma
            [
                "TARIHSIZ",
                "TARIHSIZ SIRKET",
                pd.NaT,
                None,
            ],  # tarihi yok: al (indirmede boş çıkabilir)
        ]
    )
    t = kaynak.kapanan_tablo(ham)
    assert list(t["kod"]) == ["ROYAL", "OLMK", "TARIHSIZ"]
    assert list(t["aciklama"].fillna("")) == ["", "birleşmiştir", ""]


class KopukOturum:
    def __init__(self, hata):
        self.hata = hata

    def get(self, url, timeout=None, headers=None):
        raise self.hata


@pytest.mark.parametrize(
    "hata",
    [requests.ConnectionError("bağlantı koptu"), requests.Timeout("zaman aşımı")],
)
def test_kapanan_kodlar_ag_hatasini_kaynak_hatasina_cevirir(hata):
    with pytest.raises(
        kaynak.KaynakHatasi, match=re.escape(kaynak.KAPANAN_URL)
    ) as bilgi:
        kaynak.kapanan_kodlar(KopukOturum(hata))
    assert bilgi.value.__cause__ is hata


def test_veri_komutu_kapanan_kodlarda_ag_hatasi_mesaj_ve_cikis_1_verir(
    monkeypatch, tmp_path, capsys
):
    monkeypatch.setattr(
        requests, "Session", lambda: KopukOturum(requests.ConnectionError("yok"))
    )
    assert main(["veri", "--kok", str(tmp_path)]) == 1
    assert capsys.readouterr().err.startswith("tansu veri: ")
    assert list(tmp_path.iterdir()) == []


def test_fiyat_kaynak_sirasi_bozuksa_tarihe_gore_siralanir():
    sonra, once = dict(HAM, HGDG_TARIH="14-08-2024"), dict(HAM, HGDG_TARIH="13-08-2024")
    k = kaynak.IsYatirim(
        oturum=SahteOturum([Yanit(200, {"value": [sonra, once]})]), bekleme=0
    )
    f = k.fiyat("GARAN", dt.date(2024, 8, 13), dt.date(2024, 8, 14))
    assert list(f["tarih"]) == [pd.Timestamp("2024-08-13"), pd.Timestamp("2024-08-14")]
    assert list(f.index) == [0, 1]


def test_json_olmayan_yanit_gecici_hata_sayilir_yeniden_denenir():
    # Gerçek koşu (bilet 07): sunucu 200 ile boş/HTML gövde döndürdü; 900 sembollük indirme düştü.
    class Bozuk(Yanit):
        def json(self):
            raise ValueError("Expecting value: line 1 column 1 (char 0)")

    oturum = SahteOturum([Bozuk(200), Yanit(200, {"value": [HAM]})])
    k = kaynak.IsYatirim(oturum=oturum, bekleme=0, deneme_bekleme=(0, 0, 0))
    assert len(k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))) == 1
    assert oturum.cagri == 2
    uc = SahteOturum([Bozuk(200)] * 4)
    with pytest.raises(kaynak.KaynakHatasi):
        kaynak.IsYatirim(oturum=uc, bekleme=0, deneme_bekleme=(0, 0, 0)).fiyat(
            "X", dt.date(2024, 8, 13), dt.date(2024, 8, 13)
        )


class Sayfa:
    def __init__(self, durum, metin=""):
        self.status_code, self.text = durum, metin


def _kap_liste(*cift):
    # KAP Next.js verisinde tırnaklar ters bölüyle kaçırılmıştır; "GARAN, TGB" bir şirketin iki kodudur.
    return "".join(
        f'\\"mkkMemberOid\\":\\"{oid}\\",\\"kapMemberTitle\\":\\"X\\",\\"relatedMemberTitle\\":\\"\\",'
        f'\\"stockCode\\":\\"{kod}\\"'
        for oid, kod in cift
    )


def _kap_sayfa(sektor):
    return (
        f'<a href="/tr/Sektorler?sector=ABC">{sektor}</a>'
        if sektor
        else "<html>sektör yok</html>"
    )


class SahteKapOturum(SahteOturum):
    def __init__(self, yanitlar):
        super().__init__(yanitlar)
        self.adresler = []

    def get(self, url, params=None, json=None, timeout=None):
        self.adresler.append(url)
        return super().get(url)


def test_kap_sektor_liste_bir_kez_sayfa_sembol_basina_user_agent_ve_bekleme():
    oturum = SahteKapOturum(
        [
            Sayfa(200, _kap_liste(("o1", "THYAO"), ("o2", "GARAN, TGB"))),
            Sayfa(200, _kap_sayfa("ULAŞTIRMA VE DEPOLAMA")),
            Sayfa(200, _kap_sayfa("BANKA")),
        ]
    )
    k = kaynak.KapSektor(oturum=oturum, bekleme=0)
    assert (k.sektor("THYAO"), k.sektor("TGB")) == ("ULAŞTIRMA VE DEPOLAMA", "BANKA")
    assert oturum.headers["User-Agent"] == "tansu-kisisel/0.1"
    assert [a.rsplit("/", 1)[-1] for a in oturum.adresler[1:]] == ["o1", "o2"] and len(
        oturum.adresler
    ) == 3


def test_kap_sektor_listede_olmayan_kod_none_http_hatasi_ve_bos_sayfa_hatadir():
    oturum = SahteKapOturum(
        [
            Sayfa(200, _kap_liste(("o1", "THYAO"))),
            Sayfa(403),
            Sayfa(200, _kap_sayfa(None)),
        ]
    )
    k = kaynak.KapSektor(oturum=oturum, bekleme=0)
    assert k.sektor("KAPANMIS") is None
    with pytest.raises(kaynak.KaynakHatasi):  # engel: 403
        k.sektor("THYAO")
    with pytest.raises(
        kaynak.KaynakHatasi
    ):  # 200 ama sektör alanı yok: engel sayfası olabilir, sektörsüz diye yazılmaz
        k.sektor("THYAO")
    assert len(oturum.adresler) == 3


def test_tarih_sutunu_saat_dilimsiz_saf_tarihtir():
    # TASARIM 4: kaynak tarih sütunu saat dilimsiz saf tarihtir.
    k = kaynak.IsYatirim(oturum=SahteOturum([Yanit(200, {"value": [HAM]})]), bekleme=0)
    f = k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))
    assert f["tarih"].dt.tz is None
    assert f["tarih"].tolist() == [pd.Timestamp("2024-08-13 00:00:00")]


def test_is_yatirim_istekleri_arasinda_en_az_bir_saniye(monkeypatch):
    # TASARIM 4: İş Yatırım istekleri arasında varsayılan bekleme 1 saniyedir.
    saat = [0.0]
    anlar = []

    def bekle(sure):
        saat[0] += sure

    class Oturum(SahteOturum):
        def get(self, *args, **kwargs):
            anlar.append(saat[0])
            return super().get(*args, **kwargs)

        post = get

    monkeypatch.setattr(kaynak.time, "sleep", bekle)
    k = kaynak.IsYatirim(
        oturum=Oturum([Yanit(200, {"value": [HAM]}), Yanit(200, {"d": OLAY})])
    )
    k.fiyat("CCOLA", dt.date(2024, 8, 13), dt.date(2024, 8, 13))
    k.olaylar("CCOLA")
    assert anlar == [0.0, 1.0]


def test_hicbir_modul_yahoo_yfinance_tradingview_ithal_etmez_ve_cagirmaz():
    # TASARIM 4, 5.1: Yahoo ve TradingView veri kaynağı olarak kullanılmaz.
    yasak = re.compile(r"yahoo|yfinance|tradingview|tvdatafeed", re.IGNORECASE)
    for yol in Path(kaynak.__file__).parent.rglob("*.py"):
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for dugum in ast.walk(agac):
            if isinstance(dugum, ast.Import):
                adlar = [ad.name for ad in dugum.names]
            elif isinstance(dugum, ast.ImportFrom):
                adlar = [dugum.module or "", *(ad.name for ad in dugum.names)]
            elif isinstance(dugum, ast.Call):
                adlar = [ast.unparse(dugum.func)]
                if adlar[0].split(".")[-1] in ("__import__", "import_module"):
                    adlar += [
                        a.value
                        for a in dugum.args
                        if isinstance(a, ast.Constant) and isinstance(a.value, str)
                    ]
            elif isinstance(dugum, ast.Constant) and isinstance(dugum.value, str):
                # Sabit URL'ler de taranır; kaynak yasağını anlatan yorum/metin sayılmaz.
                adlar = re.findall(r"https?://[^\s/]+", dugum.value)
            else:
                continue
            assert not any(yasak.search(ad) for ad in adlar), (yol.name, dugum.lineno)


def test_sirket_kodlari_borsapy_sirket_listesinden_ticker_sutununu_dondurur(
    monkeypatch,
):
    monkeypatch.setattr(
        borsapy, "companies", lambda: pd.DataFrame({"ticker": ["AAA", "BBB"]})
    )
    assert list(kaynak.sirket_kodlari()) == ["AAA", "BBB"]


class BosGovde(Yanit):
    def json(self):
        raise ValueError("Expecting value: line 1 column 1 (char 0)")


def test_uzun_aralik_bos_yanit_verirse_yil_yil_ister():
    # 26.10.2026: ALARK için 2019-2026 tek isteği boş gövde döndürdü, yıllık istekler geldi.
    gun = {**HAM, "HGDG_TARIH": "02-01-2025"}
    k = kaynak.IsYatirim(
        oturum=SahteOturum(
            [BosGovde(200), Yanit(200, {"value": [HAM]}), Yanit(200, {"value": [gun]})]
        ),
        bekleme=0,
        deneme_bekleme=(),
    )
    f = k.fiyat("ALARK", dt.date(2024, 6, 1), dt.date(2025, 3, 1))
    assert list(f["tarih"].dt.strftime("%Y-%m-%d")) == ["2024-08-13", "2025-01-02"]
    assert k.oturum.cagri == 3


class PencereOturum(SahteOturum):
    """Pencerede bozuk gün varsa 'value' yok; yoksa her takvim günü için bir satır (29.10.2026: INTEK, LRSHO, LYDHO)."""

    def __init__(self, bozuk):
        super().__init__([])
        self.bozuk = {dt.date.fromisoformat(g) for g in bozuk}

    def get(self, url, params=None, json=None, timeout=None):
        self.cagri += 1
        bas, son = (
            dt.datetime.strptime(params[a], "%d-%m-%Y").date()
            for a in ("startdate", "enddate")
        )
        gunler = [bas + dt.timedelta(n) for n in range((son - bas).days + 1)]
        if self.bozuk & set(gunler):
            return Yanit(200, {})
        return Yanit(
            200,
            {"value": [{**HAM, "HGDG_TARIH": g.strftime("%d-%m-%Y")} for g in gunler]},
        )


def _bozuk_gun_kaynagi(bozuk):
    return kaynak.IsYatirim(
        oturum=PencereOturum(bozuk), bekleme=0, deneme_bekleme=(0, 0, 0)
    )


def test_bozuk_gun_pencereyi_boler_gunu_atlar_ve_bildirir(caplog):
    k = _bozuk_gun_kaynagi(["2023-03-15"])
    with caplog.at_level(logging.WARNING, logger=kaynak.__name__):
        f = k.fiyat("LRSHO", dt.date(2022, 12, 30), dt.date(2024, 1, 2))
    # 2022'den 2 gün, 2023'ten 365 - 1 gün, 2024'ten 2 gün
    assert len(f) == 368 and pd.Timestamp("2023-03-15") not in set(f["tarih"])
    assert f["tarih"].is_monotonic_increasing and f["tarih"].is_unique
    assert f.attrs["atlanan_gunler"] == ["2023-03-15"]
    assert "LRSHO" in caplog.text and "2023-03-15" in caplog.text


def test_bozuk_gunsuz_pencere_tek_istektir_ve_atlanan_yoktur():
    k = _bozuk_gun_kaynagi([])
    f = k.fiyat("THYAO", dt.date(2023, 3, 1), dt.date(2023, 3, 31))
    assert len(f) == 31 and k.oturum.cagri == 1 and "atlanan_gunler" not in f.attrs


def test_on_bozuk_gun_atlanir_on_birinci_sembolu_dusurur():
    on = [f"2023-03-{g:02d}" for g in range(1, 11)]
    f = _bozuk_gun_kaynagi(on).fiyat("X", dt.date(2023, 3, 1), dt.date(2023, 3, 31))
    assert len(f) == 21 and len(f.attrs["atlanan_gunler"]) == 10
    k = _bozuk_gun_kaynagi([*on, "2023-03-20"])
    with pytest.raises(kaynak.KaynakHatasi):
        k.fiyat("X", dt.date(2023, 3, 1), dt.date(2023, 3, 31))
    assert k.oturum.cagri < 100  # ölü sembol binlerce istek yapmaz


def test_butun_gunler_bozuksa_hata_verir():
    gunler = [f"2023-03-{g:02d}" for g in range(1, 32)]
    with pytest.raises(kaynak.KaynakHatasi):
        _bozuk_gun_kaynagi(gunler).fiyat("X", dt.date(2023, 3, 1), dt.date(2023, 3, 31))


def test_atlanan_gunler_onbellege_yazilip_okununca_korunur(tmp_path):
    o = kaynak.Onbellekli(_bozuk_gun_kaynagi(["2023-03-15"]), tmp_path)
    o.fiyat("LRSHO", dt.date(2023, 3, 1), dt.date(2023, 3, 31))
    assert o.fiyat("LRSHO", None, None).attrs["atlanan_gunler"] == ["2023-03-15"]
