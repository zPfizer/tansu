"""`gunluk(tarih)` yüzü: durum.txt dört durum, bugün koşulduysa çıkış, kart CSV biçimi, Excel kilidi (TASARIM 6).

Veri: tests/test_kayit.py'deki 8 günlük serinin ilk 6 günü (28.09–05.10.2026). Sinyal son çubuk olan gün 5'tedir.
Elle hesap (ATR(2), Wilder; gerçek aralık gün 0-5 = 1; 1; 1,5; 1; 1; 3,5):
  ATR gün 1 = 1; gün 2 = 0,5·1 + 0,5·1,5 = 1,25; gün 3 = 1,125; gün 4 = 1,0625; gün 5 = 0,5·1,0625 + 0,5·3,5 = 2,28125.
  Referans 103; tahmini stop = 103 − 2·2,28125 = 98,4375 -> "98,44". Birim risk 4,5625.
  Hacim 4.000.000 TL: likidite sınırı = %2 · 4.000.000 = 80.000 TL.
  Adet = taban(min(10.000/4,5625 = 2191,8; 100.000/103 = 970,9; 80.000/103 = 776,7)) = 776.
  Pozisyon = 776·103/1.000.000 = %7,99; fiili risk = 776·4,5625/1.000.000 = %0,35.
"""

import csv
import datetime as dt
import json
import os
import subprocess
import sys
import threading
import time
from dataclasses import replace
from types import SimpleNamespace

import pandas as pd
import pytest

from tansu import aileler, gunluk, kayit, motor, rapor, veri
from tansu.kaynak import KaynakHatasi
from tests.test_veri import SahteKaynak, satir

P = aileler.Parametre(
    periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=4, sma_n=2
)
TARIH = dt.date(2026, 10, 5)
SIMDI = dt.datetime(2026, 10, 5, 19, 30)
BASLIK = [
    "tarih",
    "hisse",
    "aile",
    "durum",
    "referans",
    "stop",
    "pozisyon_yuzde",
    "adet",
    "fiili_risk",
    "likidite_siniri_tl",
    "kanit",
    "kaynak",
]


@pytest.mark.parametrize(
    "stop,nominal,adet",
    [(90.0, 100_000.0, 194), (99.0, 10_000.0, 152), (90.0, 100.0, 0)],
)
def test_s08_gunluk_ve_sinama_ayni_sayisal_miktari_kullanir(stop, nominal, adet):
    from tansu import tansusinama
    from tests.test_tansusinama import risk_satiri

    gun = pd.Timestamp("2026-10-05")
    anlik = SimpleNamespace(
        kimlik="sentetik",
        fiyat=pd.DataFrame(
            [dict(tarih=gun, sembol="A", ham_kapanis=100, kapanis=100, hacim=1)]
        ),
    )
    girdi = risk_satiri()
    girdi.update(ilk_stop=stop, nominal_tutar=nominal)
    p = replace(motor.bekleyen(5, gun), risk_girdisi=girdi)
    kart = gunluk._kart(anlik, "A", pd.DataFrame(index=[gun]), p, "kanıt")
    assert kart["adet"] == adet
    s = tansusinama._getirili(pd.DataFrame([girdi])).iloc[0]
    assert kart["risk_butcesi"] == s.risk_butcesi == nominal * 0.02
    assert kart["adet"] == s.adet
    assert kart["risk_nedeni"] == s.risk_nedeni
    assert kart["planlanan_risk"] == s.planlanan_risk
    assert kart["kullanilmayan_butce"] == s.kullanilmayan_butce


def fiyatlar(bozuk=False):
    kap = [100.0] * 5 + [103.0]
    yuk = [100.5, 100.5, 101, 100.5, 100.5, 103.5]
    sonuc = []
    for g, k, y in zip(pd.bdate_range("2026-09-28", periods=6), kap, yuk, strict=True):
        s = satir(g, k, k)
        s.update(
            yuksek=y, ham_yuksek=y, dusuk=k - 0.5, ham_dusuk=k - 0.5, hacim=4_000_000.0
        )
        sonuc.append(s)
    if bozuk:
        sonuc[3].update(
            ham_dusuk=200.0, dusuk=200.0
        )  # düşük > yüksek: bozuk satır, 1/6 > %1
    return sonuc


class Sayacli(SahteKaynak):
    cagri = 0

    def fiyat(self, sembol, bas, son):
        self.cagri += 1
        return super().fiyat(sembol, bas, son)


class Yok:
    def fiyat(self, sembol, bas, son):
        raise KaynakHatasi("ağ yok")

    olaylar = fiyat


def kaynak(**kw):
    return Sayacli({"XXXX": fiyatlar(**kw)}, {"XXXX": []})


def kos(tmp_path, k=None, tarih=TARIH, simdi=SIMDI):
    return gunluk.gunluk(
        tarih,
        tmp_path,
        simdi=simdi,
        kaynak=k or kaynak(),
        semboller=["XXXX"],
        p=P,
        atr_n=2,
    )


def durum_satirlari():
    return (rapor.RAPOR_DIZINI / "durum.txt").read_text(encoding="utf-8").splitlines()


def kagit_aile():
    kayit._yaz(
        {
            "tur": "durum",
            "olay": "durum",
            "tarih": "2026-07-05T10:00:00+00:00",
            "aile": "ema_sikismasi",
            "durum": "Kâğıt",
            "resmi": True,
            "kanit": {"islem": 148, "fazla": 0.009, "ci": [0.002, 0.016]},
        }
    )


def test_tamam_kart_csv_ve_durum(tmp_path):
    kagit_aile()
    assert kos(tmp_path) == 0
    d = durum_satirlari()
    assert d[0] == "TAMAM"
    assert d[1:5] == [
        "Son başarılı koşu: 2026-10-05 19:30",
        "Anlık görüntü: 20261005-1930",
        "Son çubuk: 2026-10-05",
        "Sembol sayısı: 1",
    ]
    assert "kartlar-20261005.csv" in d[5] and len(d) == 6
    ham = (rapor.RAPOR_DIZINI / "kartlar-20261005.csv").read_bytes()
    assert ham.startswith(b"\xef\xbb\xbf")
    satirlar = list(csv.reader(ham.decode("utf-8-sig").splitlines(), delimiter=";"))
    kanit = (
        "Kâğıt · 148 işlem · sepete göre işlem başına fazla getiri +%0,90 (%0,3 masraf) · "
        "portföy fazla getirisi (K2'ye göre, yıllık, blok bootstrap %95 aralık +%0,20 ile +%1,60) · kâğıt dönem 3/6 ay"
    )
    assert satirlar == [
        BASLIK,
        [
            "2026-10-05",
            "XXXX",
            "EMA sıkışması",
            "AKTİF",
            "103,00",
            "98,44 (tahmini)",
            "%7,99",
            "776",
            "%0,35",
            "80000",
            kanit,
            "Tansu'dan esinlenen yorum · İş Yatırım 20261005-1930",
        ],
    ]


def test_sinyal_yoksa_yalniz_baslik(tmp_path):
    assert kos(tmp_path) == 0  # aile Deneme: kart yok
    satirlar = (
        (rapor.RAPOR_DIZINI / "kartlar-20261005.csv")
        .read_bytes()
        .decode("utf-8-sig")
        .splitlines()
    )
    assert satirlar == [";".join(BASLIK)]
    assert durum_satirlari()[0] == "TAMAM"


def test_kart_gunlugu_yalniz_eklenir_ve_gun_basina_bir_satir(tmp_path):
    kagit_aile()
    kos(tmp_path)
    satirlar = (
        (kayit.KAYIT_DIZINI / "kartlar.jsonl").read_text(encoding="utf-8").splitlines()
    )
    s = json.loads(satirlar[0])
    assert (
        len(satirlar) == 1
        and s["tarih"] == "2026-10-05"
        and s["anlik"] == "20261005-1930"
    )
    assert [k["hisse"] for k in s["kartlar"]] == ["XXXX"]


def test_bugun_basarili_kosu_varsa_hicbir_sey_yapmadan_cikar(tmp_path):
    k = kaynak()
    assert kos(tmp_path, k) == 0
    cagri = k.cagri
    assert kos(tmp_path, k, simdi=dt.datetime(2026, 10, 5, 20, 30)) == 0
    assert k.cagri == cagri
    assert durum_satirlari()[1] == "Son başarılı koşu: 2026-10-05 19:30"


def test_bugun_cubuk_yok_tatil_cikis_sifir(tmp_path):
    assert (
        kos(
            tmp_path, tarih=dt.date(2026, 10, 6), simdi=dt.datetime(2026, 10, 6, 19, 30)
        )
        == 0
    )
    assert durum_satirlari()[0] == "BUGÜN ÇUBUK YOK"
    assert not list(rapor.RAPOR_DIZINI.glob("kartlar-*.csv"))
    assert not (kayit.KAYIT_DIZINI / "kartlar.jsonl").exists()


def test_veri_kapisi_basarisiz_sorunlu_kart_yok(tmp_path):
    assert kos(tmp_path, kaynak(bozuk=True)) == 1
    assert durum_satirlari()[0] == "SORUNLU"
    assert not list(rapor.RAPOR_DIZINI.glob("kartlar-*.csv"))


def test_kaynak_yoksa_veri_yok_ve_cikis_sifir_degil(tmp_path):
    assert kos(tmp_path, Yok()) == 1
    d = durum_satirlari()
    assert d[0] == "VERİ YOK" and d[1] == "Son başarılı koşu: yok"
    assert not list(rapor.RAPOR_DIZINI.glob("kartlar-*.csv"))


def test_1815ten_once_kart_uretilmez_ve_kaynaga_gidilmez(tmp_path):
    k = kaynak()
    assert kos(tmp_path, k, simdi=dt.datetime(2026, 10, 5, 18, 14)) == 1
    assert k.cagri == 0 and durum_satirlari()[0] == "VERİ YOK"
    assert not list(rapor.RAPOR_DIZINI.glob("kartlar-*.csv"))
    assert (
        kos(tmp_path, k, simdi=dt.datetime(2026, 10, 5, 18, 15)) == 0
    )  # sınırda koşar


def test_basarisiz_koşudan_sonra_son_basarili_saat_korunur(tmp_path):
    kos(tmp_path, kaynak(), tarih=dt.date(2026, 10, 5), simdi=SIMDI)
    d = dt.date(2026, 10, 6)
    assert kos(tmp_path, Yok(), tarih=d, simdi=dt.datetime(2026, 10, 6, 19, 30)) == 1
    assert durum_satirlari()[:2] == ["VERİ YOK", "Son başarılı koşu: 2026-10-05 19:30"]


def test_csv_excelde_aciksa_sorunlu_ve_kapatip_yeniden_calistir(tmp_path, monkeypatch):
    gercek = os.replace

    def kilitli(kaynak_yol, hedef):
        if str(hedef).endswith(".csv"):
            raise PermissionError("açık")
        return gercek(kaynak_yol, hedef)

    monkeypatch.setattr(os, "replace", kilitli)
    assert kos(tmp_path) == 1
    d = durum_satirlari()
    assert d[0] == "SORUNLU" and "kapatıp yeniden çalıştır" in d[-1]
    assert not (kayit.KAYIT_DIZINI / "kartlar.jsonl").exists()


def test_gunluk_anlik_goruntuler_yaslari_ne_olursa_olsun_silinmez(tmp_path):
    # TASARIM 5.11 ve 6.2: `veri/` altındaki hiçbir anlık görüntü silinmez (bilet 03 kararı; bilet 07c).
    ag = tmp_path / "gunluk" / "ag"
    for ad in ("20260801-1930", "20260802-1930", "20260904-1930", "20260906-1930"):
        (ag / ad).mkdir(parents=True)
    kayit._yaz({"tur": "deneme", "olay": "basladi", "anlik": "20260802-1930"})
    kos(tmp_path)
    assert sorted(p.name for p in ag.iterdir()) == [
        "20260801-1930",
        "20260802-1930",
        "20260904-1930",
        "20260906-1930",
        "20261005-1930",
    ]


def test_cift_ailesi_kagit_olursa_gunluk_kosu_sorunludur(tmp_path):
    # TASARIM 6.5: çift ailesi Kâğıt ise çift kartı yokluğu koşuyu SORUNLU yapar.
    kayit._yaz(
        {
            "tur": "durum",
            "olay": "durum",
            "aile": "cift_rotasyonu",
            "durum": "Kâğıt",
            "resmi": True,
        }
    )
    assert kos(tmp_path) == 1
    assert durum_satirlari()[0] == "SORUNLU"
    assert "çift kartı henüz yazılmadı" in durum_satirlari()[-1]
    assert not list(rapor.RAPOR_DIZINI.glob("kartlar-*.csv"))
    assert not (kayit.KAYIT_DIZINI / "kartlar.jsonl").exists()


@pytest.mark.parametrize(
    "devam, durumlar, gecmis",
    [
        (
            [(104, 103.5, 104.5), (100, 98, 100.5), (101, 100.5, 101.5)],
            ["AKTİF", "AKTİF", "STOP", None],
            0,
        ),
        (
            [
                (104, 103.5, 104.5),
                (93.6, 93, 95),
                (100, 99.5, 100.5),
                (101, 100.5, 101.5),
            ],
            ["AKTİF", "AKTİF", "STOP", "STOP", None],
            0,
        ),
        (
            [
                (104, 103.5, 104.5),
                (100, 99.5, 100.5),
                (101, 100.5, 101.5),
                (102, 101.5, 102.5),
            ],
            ["AKTİF", "AKTİF", "GÜN SONU STOPU", "GÜN SONU STOPU", None],
            0,
        ),
        (
            [(113.3, 112.8, 113.3), (113, 112.5, 113.5)],
            ["AKTİF", "GİRİŞ İPTAL", None],
            0,
        ),
        (
            [(104, 103.5, 104.5), (105, 200, 105.5), (106, 105.5, 106.5)],
            ["AKTİF", "AKTİF", "KARANTİNA ÇIKIŞI", None],
            100,
        ),
    ],
    ids=["stop", "kilitli_tabanda_stop", "sma250", "giris_iptali", "karantina"],
)
def test_kart_durumlari_ve_kapanan_kart_yalniz_kapandigi_gun_gorunur(
    tmp_path, devam, durumlar, gecmis
):
    # TASARIM 6.5: gerçek günlük yolunda giriş, çıkış bekleme ve kapanış gününün CSV'si.
    # Sinyal 05.10; giriş 104, ATR 2,28125 -> stop 99,4375. 93,6, 104'ün tabanıdır.
    kagit_aile()
    fiyat = []
    # Karantina senaryosunda bir bozuk gün / 108 gün < %1; veri kapısı kartı engellemez.
    for tarih in pd.bdate_range(end="2026-09-25", periods=gecmis):
        s = satir(tarih, 100, 100)
        s.update(
            dusuk=99.5,
            ham_dusuk=99.5,
            yuksek=100.5,
            ham_yuksek=100.5,
            hacim=4_000_000.0,
        )
        fiyat.append(s)
    fiyat.extend(fiyatlar())
    bas_uzunluk = len(fiyat)
    for tarih, (kapanis, dusuk, yuksek) in zip(
        pd.bdate_range("2026-10-06", periods=len(devam)), devam, strict=True
    ):
        s = satir(tarih, kapanis, kapanis)
        s.update(
            dusuk=dusuk,
            ham_dusuk=dusuk,
            yuksek=yuksek,
            ham_yuksek=yuksek,
            hacim=4_000_000.0,
        )
        fiyat.append(s)
    for uzunluk, durum in enumerate(durumlar, start=bas_uzunluk):
        tarih = fiyat[uzunluk - 1]["tarih"].date()
        k = SahteKaynak({"XXXX": fiyat[:uzunluk]}, {"XXXX": []})
        assert (
            kos(
                tmp_path,
                k,
                tarih=tarih,
                simdi=dt.datetime.combine(tarih, dt.time(19, 30)),
            )
            == 0
        )
        yol = rapor.RAPOR_DIZINI / f"kartlar-{tarih:%Y%m%d}.csv"
        with yol.open(encoding="utf-8-sig", newline="") as f:
            kartlar = list(csv.DictReader(f, delimiter=";"))
        if durum is None:
            assert kartlar == []
        else:
            assert [(k["hisse"], k["tarih"], k["durum"]) for k in kartlar] == [
                ("XXXX", "2026-10-05", durum)
            ]


@pytest.mark.parametrize(
    "ayar, kurulum_var",
    [(P, False), (replace(P, stop="kutu"), True)],
    ids=["varsayilan_cikis", "kutu_stopu"],
)
def test_kartlar_ayari_ve_kurulum_bilgisini_motora_verir(
    tmp_path, monkeypatch, ayar, kurulum_var
):
    # TASARIM 6 "Varyant": varsayılan olmayan ayar kendi çıkışlarıyla taranır; kutu stopunda kurulum tablosu da gider.
    kagit_aile()
    gelen = []
    gercek = motor.tara

    def kayitli(mumlar, sinyaller, ayar=None, kurulum=None):
        gelen.append((ayar, kurulum is not None))
        return gercek(mumlar, sinyaller, ayar, kurulum)

    monkeypatch.setattr(motor, "tara", kayitli)
    gunluk.gunluk(
        TARIH,
        tmp_path,
        simdi=SIMDI,
        kaynak=kaynak(),
        semboller=["XXXX"],
        p=ayar,
        atr_n=2,
    )
    assert gelen == [(ayar, kurulum_var)]


class Kayitli(Sayacli):
    def __init__(self, *a):
        super().__init__(*a)
        self.istenen = []

    def fiyat(self, sembol, bas, son):
        self.istenen.append(sembol)
        return super().fiyat(sembol, bas, son)


@pytest.mark.parametrize(
    "anahtarlar", [("Hisse", "Durum"), ("hisse", "durum")], ids=["eski", "yeni"]
)
def test_dunku_acik_kart_hissesi_eski_ve_yeni_anahtarla_bugun_de_indirilir(
    tmp_path, anahtarlar
):
    # TASARIM 5.2: evrenden çıksa da açık pozisyonun hissesi izlenir. Kart günlüğü yalnız eklenir (bilet 07a).
    k = Kayitli(
        {
            "XXXX": fiyatlar(),
            "YYYY": fiyatlar(),
            "ZZZZ": fiyatlar(),
            "WWWW": fiyatlar(),
        },
        {"XXXX": [], "YYYY": [], "ZZZZ": [], "WWWW": []},
    )
    veri.indir(
        ["XXXX"], tmp_path, k, simdi=dt.datetime(2026, 10, 4, 19, 30)
    )  # evren tabanı
    k.istenen.clear()
    hisse, durum = anahtarlar
    eski_satir = {
        "tarih": "2026-10-01",
        "anlik": "20261001-1930",
        "kartlar": [{hisse: "WWWW", durum: "AKTİF"}],
    }
    son_satir = {
        "tarih": "2026-10-02",
        "anlik": "20261002-1930",
        "kartlar": [
            {hisse: "ZZZZ", durum: "AKTİF"},
            {hisse: "YYYY", durum: "STOP"},
        ],
    }
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(
        "".join(json.dumps(x) + "\n" for x in (eski_satir, son_satir)),
        encoding="utf-8",
    )
    gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kaynak=k, p=P, atr_n=2)
    # En son kayıt öncekini geçersiz kılar; STOP kartın hissesi de indirilir (bilet 07c).
    assert {"ZZZZ", "YYYY"} <= set(k.istenen) and "WWWW" not in k.istenen


@pytest.mark.parametrize(
    "durum",
    ["STOP", "GÜN SONU STOPU", "KARANTİNA ÇIKIŞI", "GİRİŞ İPTAL", "BOZULDU"],
)
def test_dunku_kartin_hissesi_durumundan_bagimsiz_indirilir(tmp_path, durum):
    # TASARIM 6.2 (vekil kararı 15.10, bilet 07c): STOP ve bekleyen çıkış dolana kadar pozisyon açıktır.
    # BOZULDU eski kayıt etiketidir; eski satırlar okunmaya devam eder.
    k = Kayitli({"XXXX": fiyatlar(), "YYYY": fiyatlar()}, {"XXXX": [], "YYYY": []})
    veri.indir(["XXXX"], tmp_path, k, simdi=dt.datetime(2026, 10, 4, 19, 30))
    k.istenen.clear()
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    yol.parent.mkdir(parents=True, exist_ok=True)
    satir_ = {
        "tarih": "2026-10-02",
        "anlik": "20261002-1930",
        "kartlar": [{"hisse": "YYYY", "durum": durum}],
    }
    yol.write_text(json.dumps(satir_) + "\n", encoding="utf-8")
    gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kaynak=k, p=P, atr_n=2)
    assert "YYYY" in k.istenen


@pytest.mark.parametrize("bozuk", [False, True])
def test_sakli_komut_ag_yoluna_girmeden_disariya_yazar(tmp_path, monkeypatch, bozuk):
    from tansu import __main__ as komut
    from tansu import deneme

    kimlik = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    goruntu = tmp_path / "ag" / kimlik
    if bozuk:
        (goruntu / "olaylar.json").write_text("{}", encoding="utf-8")
    once = {p.name: p.read_bytes() for p in goruntu.iterdir()}
    cagrilar = []

    def yasak(*a, **kw):
        cagrilar.append(True)
        raise AssertionError("saklı mod ağ/temizlik yoluna girdi")

    monkeypatch.setattr(gunluk, "_temizle", yasak)
    monkeypatch.setattr(gunluk, "_semboller", yasak)
    monkeypatch.setattr(veri, "indir", yasak)
    monkeypatch.setattr(gunluk.kaynak_modulu, "IsYatirim", yasak)
    cikti = tmp_path / "disari"
    try:
        kod = komut.main(
            [
                "gunluk",
                "2026-10-05",
                "--kok",
                str(tmp_path),
                "--kimlik",
                kimlik,
                "--cikti-koku",
                str(cikti),
            ]
        )
    except SystemExit as hata:
        kod = hata.code
    assert kod == int(bozuk)
    assert cagrilar == []
    assert {p.name: p.read_bytes() for p in goruntu.iterdir()} == once
    durum = (cikti / "rapor/durum.txt").read_text(encoding="utf-8")
    assert durum.startswith("SORUNLU" if bozuk else "TAMAM")
    assert not rapor.RAPOR_DIZINI.exists()
    assert not kayit.KAYIT_DIZINI.exists()
    if bozuk:
        assert "manifest uyuşmuyor" in durum
        assert not (cikti / "kayit/kartlar.jsonl").exists()
    else:
        csv_yol = cikti / "rapor/kartlar-20261005.csv"
        assert csv_yol.read_text(encoding="utf-8-sig").splitlines() == [
            ";".join(BASLIK)
        ]
        assert str(csv_yol) in durum
        assert (
            json.loads((cikti / "kayit/kartlar.jsonl").read_text(encoding="utf-8"))[
                "anlik"
            ]
            == kimlik
        )
        bag = deneme.PilotKayit(cikti / "rapor/ayar-baglari.jsonl").oku()
        assert bag[-1]["veri_ref_id"] == kimlik


@pytest.mark.parametrize(
    "degisiklik", ["ayni", "farkli", "bozuk", "manifest", "eksik", "gecersiz"]
)
@pytest.mark.parametrize("calisma_gunu", [5, 24], ids=["bugun", "gecmis"])
@pytest.mark.parametrize("istenen_gun", [5, 6], ids=["cubuk_var", "cubuk_yok"])
def test_sakli_girdi_basarili_ayni_gun_kisa_yolundan_once_dogrulanir(
    tmp_path, degisiklik, calisma_gunu, istenen_gun
):
    kagit_aile()
    kimlik = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    tarih = TARIH.replace(day=istenen_gun)
    simdi = SIMDI.replace(day=calisma_gunu)
    cikti = tmp_path / "disari"
    assert (
        gunluk.gunluk(
            tarih, tmp_path, simdi=simdi, kimlik=kimlik, cikti_koku=cikti, p=P, atr_n=2
        )
        == 0
    )
    durum_yolu = cikti / "rapor/durum.txt"
    once = durum_yolu.read_bytes()
    gunluk_yolu = cikti / "kayit/kartlar.jsonl"
    assert gunluk_yolu.exists()
    gunluk_once = gunluk_yolu.read_bytes()
    csv_once = {p.name: p.read_bytes() for p in (cikti / "rapor").glob("*.csv")}
    if degisiklik == "farkli":
        kimlik = b
    elif degisiklik == "bozuk":
        (tmp_path / "ag" / kimlik / "olaylar.json").write_text("{}", encoding="utf-8")
    elif degisiklik == "manifest":
        (tmp_path / "ag" / kimlik / "manifest.json").write_text("{", encoding="utf-8")
    elif degisiklik == "eksik":
        kimlik = "bulunamayan"
    elif degisiklik == "gecersiz":
        kimlik = "../20261005-1930"
    assert gunluk.gunluk(
        tarih, tmp_path, simdi=simdi, kimlik=kimlik, cikti_koku=cikti
    ) == int(degisiklik != "ayni")
    if degisiklik == "ayni":
        assert durum_yolu.read_bytes() == once
    else:
        assert durum_yolu.read_text(encoding="utf-8").startswith("SORUNLU")
    assert (
        len((cikti / "kayit/kartlar.jsonl").read_text(encoding="utf-8").splitlines())
        == 1
    )
    assert [
        gunluk.gunluk(tarih, tmp_path, simdi=simdi, kimlik=b, cikti_koku=cikti)
        for _ in range(2)
    ] == [1, 1]
    assert "farklı görüntü kimliğine bağlı" in durum_yolu.read_text(encoding="utf-8")
    assert gunluk_yolu.read_bytes() == gunluk_once
    assert {p.name: p.read_bytes() for p in (cikti / "rapor").glob("*.csv")} == csv_once
    if degisiklik in ("ayni", "farkli", "eksik", "gecersiz"):
        assert (
            gunluk.gunluk(
                tarih, tmp_path, simdi=simdi, kimlik="20261005-1930", cikti_koku=cikti
            )
            == 0
        )
        assert durum_yolu.read_text(encoding="utf-8").startswith(
            "TAMAM" if istenen_gun == 5 else "BUGÜN ÇUBUK YOK"
        )
        assert gunluk_yolu.read_bytes() == gunluk_once
        assert {
            p.name: p.read_bytes() for p in (cikti / "rapor").glob("*.csv")
        } == csv_once


def test_sakli_bag_baska_gunun_basarisi_ile_kaybolmaz(tmp_path):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    cikti = tmp_path / "disari"
    kodlar = [
        gunluk.gunluk(
            tarih,
            tmp_path,
            simdi=SIMDI.replace(day=24),
            kimlik=kimlik,
            cikti_koku=cikti,
        )
        for tarih, kimlik in [
            ("2026-10-05", a),
            ("2026-10-06", b),
            ("2026-10-05", b),
            ("2026-10-05", b),
        ]
    ]
    assert kodlar == [0, 0, 1, 1]
    satirlar = [
        json.loads(s)
        for s in (cikti / "kayit/kartlar.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert [(s["tarih"], s["anlik"]) for s in satirlar] == [
        ("2026-10-05", "20261005-1930"),
        ("2026-10-06", "20261005-1931"),
    ]


@pytest.mark.parametrize(
    "kartlar", [[{"hisse": "YYYY"}], []], ids=["acik", "bos_tamam"]
)
def test_sakli_cubuksuz_tamamlanma_onceki_kart_girdisini_degistirmez(tmp_path, kartlar):
    kimlik = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    yol.parent.mkdir(parents=True)
    once = (
        json.dumps({"tarih": "2026-10-04", "anlik": "eski", "kartlar": kartlar}) + "\n"
    )
    yol.write_text(once, encoding="utf-8")
    assert (
        gunluk.gunluk(
            "2026-10-06", tmp_path, simdi=SIMDI.replace(day=24), kimlik=kimlik
        )
        == 0
    )
    assert yol.read_text(encoding="utf-8").startswith(once)
    assert len(yol.read_text(encoding="utf-8").splitlines()) == 2
    k = Kayitli({"XXXX": fiyatlar(), "YYYY": fiyatlar()}, {"XXXX": [], "YYYY": []})
    assert (
        gunluk.gunluk("2026-10-07", tmp_path, simdi=SIMDI.replace(day=7), kaynak=k) == 0
    )
    assert set(k.istenen) == ({"XXXX", "YYYY"} if kartlar else {"XXXX"})


@pytest.mark.parametrize(
    "son,onceki_gunluk",
    [
        ("2026-10-05", False),
        ("2026-10-05", True),
        ("yok", False),
        ("gecersiz", False),
        ("yok", True),
        ("gecersiz", True),
    ],
)
def test_eski_tamam_eksik_gunluk_engeli_tekrarda_korunur(tmp_path, son, onceki_gunluk):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    if onceki_gunluk:
        gecmis = kayit.KAYIT_DIZINI / "kartlar.jsonl"
        gecmis.parent.mkdir(parents=True)
        gecmis.write_text(
            json.dumps({"tarih": "2026-10-05", "anlik": a, "kartlar": []}) + "\n",
            encoding="utf-8",
        )
    yol = rapor.RAPOR_DIZINI / "durum.txt"
    yol.parent.mkdir(parents=True)
    yol.write_text(
        f"TAMAM\nSon başarılı koşu: 2026-10-24 19:30\nAnlık görüntü: {b if onceki_gunluk else a}\nSon çubuk: {son}\nSembol sayısı: 1\nEylem: eski çıktı\n",
        encoding="utf-8",
    )
    assert [
        gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=k) for k in [a, b, b]
    ] == [1, 1, 1]
    assert "KART GÜNLÜĞÜ EKSİK" in yol.read_text(encoding="utf-8")
    satirlar = [
        json.loads(s)
        for s in (kayit.KAYIT_DIZINI / "kartlar.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(satirlar) == (2 if onceki_gunluk else 1)
    assert satirlar[-1]["durum"] == "KART GÜNLÜĞÜ EKSİK"
    assert satirlar[-1]["tarih"] == ("2026-10-05" if son == "2026-10-05" else None)
    assert "kartlar" not in satirlar[-1]
    assert not list(rapor.RAPOR_DIZINI.glob("kartlar-*.csv"))


def test_eski_cubuksuz_saat_anahtari_ret_sonrasinda_korunur(tmp_path):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    yol = rapor.RAPOR_DIZINI / "durum.txt"
    yol.parent.mkdir(parents=True)
    yol.write_text(
        f"BUGÜN ÇUBUK YOK\nSon başarılı koşu: 2026-10-06 19:30\nAnlık görüntü: {a}\nSon çubuk: 2026-10-05\nSembol sayısı: 1\nEylem: eski çıktı\n",
        encoding="utf-8",
    )
    assert [
        gunluk.gunluk("2026-10-06", tmp_path, simdi=SIMDI.replace(day=24), kimlik=k)
        for k in ["../gecersiz", b, b, a]
    ] == [1, 1, 1, 0]
    satirlar = [
        json.loads(s)
        for s in (kayit.KAYIT_DIZINI / "kartlar.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(satirlar) == 1
    assert satirlar[0]["tarih"] == "2026-10-06"
    assert satirlar[0]["tarih_kaynagi"] == "eski_kosu_saati"
    assert satirlar[0]["anlik"] == a
    assert yol.read_text(encoding="utf-8").startswith("BUGÜN ÇUBUK YOK")
    assert not list(rapor.RAPOR_DIZINI.glob("kartlar-*.csv"))


@pytest.mark.parametrize(
    "kimlik", ["", ".", "..", "a/b", "a\\b", "C:veri", "/veri", "a "]
)
def test_gecersiz_sakli_kimlik_indirme_yoluna_dusmez(tmp_path, monkeypatch, kimlik):
    cagrilar = []
    monkeypatch.setattr(veri, "indir", lambda *a, **kw: cagrilar.append(True))
    assert gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=kimlik) == 1
    assert "geçersiz görüntü kimliği" in durum_satirlari()[-1]
    assert cagrilar == []


def test_sakli_goruntunun_icindeki_cikti_yolu_yazmadan_reddedilir(tmp_path):
    kimlik = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    goruntu = tmp_path / "ag" / kimlik
    once = {p.name: p.read_bytes() for p in goruntu.iterdir()}
    with pytest.raises(veri.VeriHatasi, match="görüntünün içine"):
        gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=kimlik, cikti_koku=goruntu)
    assert {p.name: p.read_bytes() for p in goruntu.iterdir()} == once


def test_ayri_cikti_indirmeyi_tasir_onceki_kart_girdisini_korur(tmp_path):
    k = Kayitli({"XXXX": fiyatlar(), "YYYY": fiyatlar()}, {"XXXX": [], "YYYY": []})
    veri.indir(["XXXX"], tmp_path, k, simdi=SIMDI.replace(day=4))
    k.istenen.clear()
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    yol.parent.mkdir(parents=True)
    once = json.dumps({"tarih": "2026-10-02", "kartlar": [{"hisse": "YYYY"}]}) + "\n"
    yol.write_text(once, encoding="utf-8")
    cikti = tmp_path / "disari"
    assert gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kaynak=k, cikti_koku=cikti) == 0
    assert "YYYY" in k.istenen
    assert yol.read_text(encoding="utf-8") == once
    assert (cikti / "veri/gunluk/ag/20261005-1930/manifest.json").is_file()
    assert not (tmp_path / "gunluk").exists()
    assert not rapor.RAPOR_DIZINI.exists()
    assert (cikti / "kayit/kartlar.jsonl").is_file()


@pytest.mark.parametrize(
    "ad",
    [
        "kayit",
        "sadakat",
        "sinama",
        "tansu-sinama",
        "grup-hazirla",
        "denetim",
        "evren-indir",
        "sektor-indir",
    ],
)
def test_cikti_koku_diger_komutlarda_yan_etkiden_once_reddedilir(tmp_path, capsys, ad):
    from tansu import __main__ as komut

    with pytest.raises(SystemExit) as hata:
        komut.main([ad, "--cikti-koku", str(tmp_path / "disari")])
    assert hata.value.code == 2
    assert "yalnız gunluk" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("ekran", ["basarili", "sorunlu", "yok"])
@pytest.mark.parametrize("csv_var", [True, False], ids=["baska_kart", "eksik_csv"])
def test_eski_dolu_kart_celiskisi_tekrarda_basariya_donmez(tmp_path, ekran, csv_var):
    kagit_aile()
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    for kimlik in (a, b):
        assert (
            gunluk.gunluk(
                TARIH,
                tmp_path,
                simdi=SIMDI,
                kimlik=kimlik,
                cikti_koku=tmp_path / kimlik,
                p=P,
                atr_n=2,
            )
            == 0
        )
    cikti = tmp_path / "eski"
    rapor_yolu = cikti / "rapor"
    rapor_yolu.mkdir(parents=True)
    gunluk_yolu = cikti / "kayit/kartlar.jsonl"
    gunluk_yolu.parent.mkdir()
    once = (tmp_path / a / "kayit/kartlar.jsonl").read_bytes()
    assert len(json.loads(once)["kartlar"]) == 1
    gunluk_yolu.write_bytes(once)
    csv_yolu = rapor_yolu / "kartlar-20261005.csv"
    csv_once = (tmp_path / b / "rapor/kartlar-20261005.csv").read_bytes()
    assert b.encode() in csv_once
    if csv_var:
        csv_yolu.write_bytes(csv_once)
    if ekran != "yok":
        satirlar = (
            (tmp_path / b / "rapor/durum.txt").read_text(encoding="utf-8").splitlines()
        )
        satirlar[0] = "TAMAM" if ekran == "basarili" else "SORUNLU"
        satirlar[-1] = "Eylem: eski çıktı"
        (rapor_yolu / "durum.txt").write_text(
            "\n".join(satirlar) + "\n", encoding="utf-8"
        )
    kodlar = [
        gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=k, cikti_koku=cikti)
        for k in (a, b, a)
    ]
    assert kodlar == [1, 1, 1]
    assert gunluk_yolu.read_bytes().startswith(once)
    satirlar = [
        json.loads(s) for s in gunluk_yolu.read_text(encoding="utf-8").splitlines()
    ]
    assert len(satirlar) == 2
    assert satirlar[-1]["durum"] == (
        "KART GÜNLÜĞÜ EKSİK" if ekran == "basarili" else "KAYIT ÇELİŞKİSİ"
    )
    assert "kartlar" not in satirlar[-1]
    assert (rapor_yolu / "durum.txt").read_text(encoding="utf-8").startswith("SORUNLU")
    if csv_var:
        assert csv_yolu.read_bytes() == csv_once
    else:
        assert not csv_yolu.exists()


@pytest.mark.parametrize(
    "gun", ["2026-10-05", "2026-10-06"], ids=["kartli", "cubuksuz"]
)
def test_geri_donulen_gunun_ayni_tekrari_ekrani_ve_saati_korur(tmp_path, gun):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    cikti = tmp_path / "disari"
    for dakika, tarih, kimlik in [(30, gun, a), (31, "2026-10-07", b), (32, gun, a)]:
        assert (
            gunluk.gunluk(
                tarih,
                tmp_path,
                simdi=SIMDI.replace(day=24, minute=dakika),
                kimlik=kimlik,
                cikti_koku=cikti,
            )
            == 0
        )
    once = {
        p.relative_to(cikti): p.read_bytes() for p in cikti.rglob("*") if p.is_file()
    }
    assert (
        gunluk.gunluk(
            gun,
            tmp_path,
            simdi=SIMDI.replace(day=24, minute=33),
            kimlik=a,
            cikti_koku=cikti,
        )
        == 0
    )
    assert {
        p.relative_to(cikti): p.read_bytes() for p in cikti.rglob("*") if p.is_file()
    } == once


@pytest.mark.parametrize(
    "ilk_sakli, ikinci_sakli",
    [(True, True), (True, False), (False, True)],
    ids=["sakli", "indirme", "indirme_sahibi"],
)
def test_ortusen_gunluk_cagrisi_sahibin_ciktisini_yazamaz(
    tmp_path, monkeypatch, ilk_sakli, ikinci_sakli
):
    kagit_aile()
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    cikti = tmp_path / "disari"
    if not ilk_sakli:
        (cikti / "rapor").mkdir(parents=True)
        (cikti / "rapor/durum.txt").write_text(
            "SORUNLU\nSon başarılı koşu: yok\nAnlık görüntü: yok\nSon çubuk: yok\nSembol sayısı: yok\nEylem: önceki hata\n",
            encoding="utf-8",
        )
    girdi, devam = threading.Event(), threading.Event()
    gercek = gunluk._kartlar
    sonuclar = []

    def duraklat(anlik, *args, **kwargs):
        if anlik.kimlik == a:
            girdi.set()
            assert devam.wait(10)
        return gercek(anlik, *args, **kwargs)

    monkeypatch.setattr(gunluk, "_kartlar", duraklat)
    isci = threading.Thread(
        target=lambda: sonuclar.append(
            gunluk.gunluk(
                TARIH,
                tmp_path,
                simdi=SIMDI,
                kimlik=a if ilk_sakli else None,
                kaynak=kaynak(),
                semboller=["XXXX"],
                cikti_koku=cikti,
                p=P,
                atr_n=2,
            )
        )
    )
    isci.start()
    try:
        assert girdi.wait(10)
        once = {
            p.relative_to(cikti): p.read_bytes()
            for p in cikti.rglob("*")
            if p.is_file() and p.suffix != ".kilit"
        }
        kod = gunluk.gunluk(
            TARIH,
            tmp_path,
            simdi=SIMDI.replace(minute=31),
            kimlik=b if ikinci_sakli else None,
            kaynak=kaynak(),
            semboller=["XXXX"],
            cikti_koku=cikti,
            p=P,
            atr_n=2,
        )
        sonra = {
            p.relative_to(cikti): p.read_bytes()
            for p in cikti.rglob("*")
            if p.is_file() and p.suffix != ".kilit"
        }
    finally:
        devam.set()
        isci.join(10)
    assert not isci.is_alive()
    assert kod == 1
    assert sonra == once
    assert sonuclar == [0]
    assert (cikti / "rapor/durum.txt").read_text(encoding="utf-8").startswith("TAMAM")
    assert f"Anlık görüntü: {a}" in (cikti / "rapor/durum.txt").read_text(
        encoding="utf-8"
    )
    assert (
        json.loads((cikti / "kayit/kartlar.jsonl").read_text(encoding="utf-8"))["anlik"]
        == a
    )
    assert a.encode() in (cikti / "rapor/kartlar-20261005.csv").read_bytes()


@pytest.mark.parametrize("eski_alanlar", [False, True], ids=["yeni", "eski"])
def test_ekransiz_tutarli_kart_gunlugu_csv_ile_basariya_doner(tmp_path, eski_alanlar):
    kagit_aile()
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    kaynak_cikti = tmp_path / "kaynak-cikti"
    assert (
        gunluk.gunluk(
            TARIH,
            tmp_path,
            simdi=SIMDI,
            kimlik=a,
            cikti_koku=kaynak_cikti,
            p=P,
            atr_n=2,
        )
        == 0
    )
    cikti = tmp_path / "disari"
    (cikti / "rapor").mkdir(parents=True)
    (cikti / "kayit").mkdir()
    csv_yolu = cikti / "rapor/kartlar-20261005.csv"
    csv_yolu.write_bytes((kaynak_cikti / "rapor/kartlar-20261005.csv").read_bytes())
    satir = json.loads(
        (kaynak_cikti / "kayit/kartlar.jsonl").read_text(encoding="utf-8")
    )
    assert len(satir["kartlar"]) == 1
    if eski_alanlar:
        satir["kartlar"] = [
            {k.capitalize(): v for k, v in kart.items()} for kart in satir["kartlar"]
        ]
    gunluk_yolu = cikti / "kayit/kartlar.jsonl"
    gunluk_yolu.write_text(
        json.dumps(satir, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    once = (csv_yolu.read_bytes(), gunluk_yolu.read_bytes())
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=SIMDI.replace(day=24), kimlik=a, cikti_koku=cikti
        )
        == 0
    )
    assert (csv_yolu.read_bytes(), gunluk_yolu.read_bytes()) == once
    assert (cikti / "rapor/durum.txt").read_text(encoding="utf-8").startswith("TAMAM")


def test_indirme_ret_sonrasi_kabul_edilen_csvyi_degistiremez(tmp_path):
    kagit_aile()
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    cikti = tmp_path / "disari"
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=SIMDI, kimlik=a, cikti_koku=cikti, p=P, atr_n=2
        )
        == 0
    )
    csv_yolu = cikti / "rapor/kartlar-20261005.csv"
    gunluk_yolu = cikti / "kayit/kartlar.jsonl"
    once = (csv_yolu.read_bytes(), gunluk_yolu.read_bytes())
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=SIMDI, kimlik="../gecersiz", cikti_koku=cikti
        )
        == 1
    )
    assert (
        gunluk.gunluk(
            TARIH,
            tmp_path,
            simdi=SIMDI.replace(minute=32),
            kaynak=kaynak(),
            semboller=["XXXX"],
            cikti_koku=cikti,
            p=P,
            atr_n=2,
        )
        == 1
    )
    assert (csv_yolu.read_bytes(), gunluk_yolu.read_bytes()) == once
    assert "farklı görüntü kimliğine bağlı" in (cikti / "rapor/durum.txt").read_text(
        encoding="utf-8"
    )


def test_ayri_rapor_ortak_gunluk_eszamanli_kabulu_paylasir(tmp_path, monkeypatch):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    girdi, devam = threading.Event(), threading.Event()
    gercek = gunluk._kartlar
    sonuc = []
    rapor_a = rapor.RAPOR_DIZINI
    rapor_b = tmp_path / "b-rapor"

    def duraklat(anlik, *args, **kwargs):
        if anlik.kimlik == a:
            girdi.set()
            assert devam.wait(10)
        return gercek(anlik, *args, **kwargs)

    monkeypatch.setattr(gunluk, "_kartlar", duraklat)
    isci = threading.Thread(
        target=lambda: sonuc.append(
            gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=a)
        )
    )
    isci.start()
    try:
        assert girdi.wait(10)
        monkeypatch.setattr(rapor, "RAPOR_DIZINI", rapor_b)
        kod = gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=b)
    finally:
        devam.set()
        isci.join(10)
    assert not isci.is_alive()
    assert kod == 1
    assert sonuc == [0]
    assert not (rapor_b / "durum.txt").exists()
    assert not list(rapor_b.glob("*.csv"))
    assert f"Anlık görüntü: {a}" in (rapor_a / "durum.txt").read_text(encoding="utf-8")
    assert (
        json.loads((kayit.KAYIT_DIZINI / "kartlar.jsonl").read_text(encoding="utf-8"))[
            "anlik"
        ]
        == a
    )


def test_surec_kilidi_ayri_ciktiyi_engellemez_olunce_birakir(tmp_path):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    cikti = tmp_path / "ortak"
    hazir = tmp_path / "surec-hazir.txt"
    kod = """
import datetime as dt
import sys
from pathlib import Path
from tansu import gunluk, kayit
kok, cikti, kimlik, hazir = sys.argv[1:]
kayit.KAYIT_DIZINI = Path(kok) / "kayit"
gercek = gunluk._kartlar
def duraklat(*a, **kw):
    Path(hazir).write_text("hazir", encoding="utf-8")
    sys.stdin.readline()
    return gercek(*a, **kw)
gunluk._kartlar = duraklat
raise SystemExit(gunluk.gunluk("2026-10-05", kok, simdi=dt.datetime(2026, 10, 24, 19, 30), kimlik=kimlik, cikti_koku=cikti))
"""
    surec = subprocess.Popen(
        [
            sys.executable,
            "-B",
            "-X",
            "utf8",
            "-c",
            kod,
            str(tmp_path),
            str(cikti),
            a,
            str(hazir),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        son = time.monotonic() + 15
        while not hazir.exists() and surec.poll() is None and time.monotonic() < son:
            time.sleep(0.02)
        assert hazir.exists(), "alt süreç kart hesabına ulaşmadı"
        assert (
            gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=b, cikti_koku=cikti) == 1
        )
        assert not (cikti / "rapor/durum.txt").exists()
        assert not (cikti / "kayit/kartlar.jsonl").exists()
        assert (
            gunluk.gunluk(
                TARIH, tmp_path, simdi=SIMDI, kimlik=b, cikti_koku=tmp_path / "ayri"
            )
            == 0
        )
    finally:
        if surec.poll() is None:
            surec.terminate()
        cikis, hata = surec.communicate(timeout=10)
    assert surec.returncode is not None, (cikis, hata)
    assert gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kimlik=b, cikti_koku=cikti) == 0
    assert (
        json.loads((cikti / "kayit/kartlar.jsonl").read_text(encoding="utf-8"))["anlik"]
        == b
    )


@pytest.mark.parametrize(
    "min_gun, cikis", [(3, 0), (100, 1)], ids=["ayni_kartlar", "farkli_kartlar"]
)
def test_ayni_kimlikli_indirme_kabul_edilen_kartlari_degistiremez(
    tmp_path, min_gun, cikis
):
    kagit_aile()
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    cikti = tmp_path / "disari"
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=SIMDI, kimlik=a, cikti_koku=cikti, p=P, atr_n=2
        )
        == 0
    )
    csv_yolu = cikti / "rapor/kartlar-20261005.csv"
    gunluk_yolu = cikti / "kayit/kartlar.jsonl"
    once = (csv_yolu.read_bytes(), gunluk_yolu.read_bytes())
    assert len(json.loads(once[1])["kartlar"]) == 1
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=SIMDI, kimlik="../gecersiz", cikti_koku=cikti
        )
        == 1
    )
    assert (
        gunluk.gunluk(
            TARIH,
            tmp_path,
            simdi=SIMDI,
            kaynak=kaynak(),
            semboller=["XXXX"],
            cikti_koku=cikti,
            p=replace(P, min_gun=min_gun),
            atr_n=2,
        )
        == cikis
    )
    assert (csv_yolu.read_bytes(), gunluk_yolu.read_bytes()) == once
    if cikis:
        assert "kabul edilen kartlarla uyuşmuyor" in (
            cikti / "rapor/durum.txt"
        ).read_text(encoding="utf-8")
    else:
        assert (
            (cikti / "rapor/durum.txt").read_text(encoding="utf-8").startswith("TAMAM")
        )


@pytest.mark.parametrize(
    "ilk_gun", ["2026-10-05", "2026-10-06"], ids=["tamam", "cubuksuz"]
)
@pytest.mark.parametrize("ayni_gun", [True, False], ids=["ayni_istek", "bugun"])
def test_seceneksiz_kisa_yol_sakli_ekranin_istenen_gununu_kullanir(
    tmp_path, ilk_gun, ayni_gun
):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    assert gunluk.gunluk(ilk_gun, tmp_path, simdi=SIMDI.replace(day=24), kimlik=a) == 0
    ekran = rapor.RAPOR_DIZINI / "durum.txt"
    once = ekran.read_bytes()
    k = kaynak()
    assert (
        gunluk.gunluk(
            ilk_gun if ayni_gun else "2026-10-24",
            tmp_path,
            simdi=SIMDI.replace(day=24, minute=31),
            kaynak=k,
            semboller=["XXXX"],
        )
        == 0
    )
    if ayni_gun:
        assert k.cagri == 0
        assert ekran.read_bytes() == once
    else:
        assert k.cagri > 0
        assert ekran.read_text(encoding="utf-8").startswith("BUGÜN ÇUBUK YOK")
        assert "Anlık görüntü: 20261024-1931" in ekran.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "sonuc, durum, cikis",
    [
        ("tamam", "TAMAM", 0),
        ("cubuksuz", "BUGÜN ÇUBUK YOK", 0),
        ("sorunlu", "SORUNLU", 1),
        ("veri_yok", "VERİ YOK", 1),
    ],
)
def test_seceneksiz_yeni_ekran_bilinen_istenen_gunu_korur(
    tmp_path, sonuc, durum, cikis
):
    # TASARIM 6 #126: yeni ekran bilinen günü düşürüp eski kısa yola dönemez.
    kagit_aile()
    simdi = SIMDI.replace(day=24)
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=simdi)
    assert a == "20261024-1930"
    cikti = tmp_path / "disari"
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=simdi, kimlik=a, cikti_koku=cikti, p=P, atr_n=2
        )
        == 0
    )
    ekran = cikti / "rapor/durum.txt"
    csv_yolu = cikti / "rapor/kartlar-20261005.csv"
    gunluk_yolu = cikti / "kayit/kartlar.jsonl"
    kabul = (csv_yolu.read_bytes(), gunluk_yolu.read_bytes())
    assert len(json.loads(kabul[1])["kartlar"]) == 1
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=simdi, kimlik="../gecersiz", cikti_koku=cikti
        )
        == 1
    )

    class ArizaliKaynak:
        cagri = 0

        def fiyat(self, sembol, bas, son):
            self.cagri += 1
            hata = ValueError if sonuc == "sorunlu" else KaynakHatasi
            raise hata("kaynak yanıtı alınamadı")

        olaylar = fiyat

    def indir(gun, k, zaman=simdi):
        return gunluk.gunluk(
            gun,
            tmp_path,
            simdi=zaman,
            kaynak=k,
            semboller=["XXXX"],
            cikti_koku=cikti,
            p=P,
            atr_n=2,
        )

    istenen_gun = "2026-10-06" if sonuc == "cubuksuz" else "2026-10-05"
    k = ArizaliKaynak() if cikis else kaynak()
    assert indir(istenen_gun, k) == cikis
    uretilen = [(istenen_gun, durum, ekran.read_text(encoding="utf-8").splitlines())]
    assert k.cagri == 1
    if cikis:
        tekrar = kaynak()
        assert indir(TARIH, tekrar) == 0
        assert tekrar.cagri == 1
        uretilen.append(
            ("2026-10-05", "TAMAM", ekran.read_text(encoding="utf-8").splitlines())
        )
    assert (csv_yolu.read_bytes(), gunluk_yolu.read_bytes()) == kabul

    bugun = kaynak()
    assert indir("2026-10-24", bugun, simdi.replace(minute=31)) == 0
    son_ekran = ekran.read_text(encoding="utf-8").splitlines()
    uretilen.append(("2026-10-24", "BUGÜN ÇUBUK YOK", son_ekran))
    son_baytlar = ekran.read_bytes()
    ayni_gun = kaynak()
    assert indir("2026-10-24", ayni_gun, simdi.replace(minute=32)) == 0
    assert ayni_gun.cagri == 0
    assert ekran.read_bytes() == son_baytlar
    for gun, beklenen, satirlar in uretilen:
        assert len(satirlar) == 6
        assert satirlar[0] == beklenen
        assert satirlar[5].startswith(f"Eylem: İstenen gün: {gun}. ")
    assert bugun.cagri == 1
    assert son_ekran[0] == "BUGÜN ÇUBUK YOK"
    assert son_ekran[2] == "Anlık görüntü: 20261024-1931"
    assert son_ekran[3] == "Son çubuk: 2026-10-05"
    assert (csv_yolu.read_bytes(), gunluk_yolu.read_bytes()) == kabul


@pytest.mark.parametrize(
    "ilk_gun, durum", [("2026-10-05", "TAMAM"), ("2026-10-06", "BUGÜN ÇUBUK YOK")]
)
def test_eski_gun_bilgisi_olmayan_ekran_saat_kisa_yolunu_korur(
    tmp_path, ilk_gun, durum
):
    k = kaynak()
    assert kos(tmp_path, k, tarih=ilk_gun, simdi=SIMDI.replace(day=24)) == 0
    ekran = rapor.RAPOR_DIZINI / "durum.txt"
    once = ekran.read_bytes()
    satirlar = durum_satirlari()
    assert len(satirlar) == 6
    assert satirlar[0] == durum
    assert not satirlar[5].startswith("Eylem: İstenen gün: ")
    assert (
        kos(tmp_path, k, tarih="2026-10-24", simdi=SIMDI.replace(day=24, minute=31))
        == 0
    )
    assert k.cagri == 1
    assert ekran.read_bytes() == once


@pytest.mark.parametrize(
    "koken, secim, cikis",
    [
        ("indirme", "ayni", 0),
        ("indirme", "eksik", 1),
        ("sakli", "ayni", 1),
        ("benzer_isaret", "ayni", 1),
    ],
)
def test_cubuksuz_indirme_kokeni_sakli_girdi_kontrolunu_kaldirmaz(
    tmp_path, koken, secim, cikis
):
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    cikti = tmp_path / "disari"
    assert (
        gunluk.gunluk(
            TARIH, tmp_path, simdi=SIMDI.replace(day=24), kimlik=a, cikti_koku=cikti
        )
        == 0
    )
    gecmis = cikti / "kayit/kartlar.jsonl"
    kabul = gecmis.read_bytes()
    ekran = cikti / "rapor/durum.txt"
    k = kaynak()
    assert (
        gunluk.gunluk(
            "2026-10-24",
            tmp_path,
            simdi=SIMDI.replace(day=24),
            kimlik=None if koken == "indirme" else a,
            kaynak=k,
            semboller=["XXXX"],
            cikti_koku=cikti,
        )
        == 0
    )
    assert k.cagri == int(koken == "indirme")
    if koken != "indirme":
        gecmis.write_bytes(kabul)  # saklı başarının gerekli tamamlanma kaydı eksik
    if koken == "benzer_isaret":
        metin = ekran.read_text(encoding="utf-8")
        ekran.write_text(
            metin.replace(
                "İstenen gün: 2026-10-24. ",
                "İstenen gün: 2026-10-24. Girdi: indirmeX. ",
            ),
            encoding="utf-8",
        )
    assert gecmis.read_bytes() == kabul
    assert (
        gunluk.gunluk(
            "2026-10-24",
            tmp_path,
            simdi=SIMDI.replace(day=24, minute=31),
            kimlik=a if secim == "ayni" else "bulunamayan",
            kaynak=k,
            cikti_koku=cikti,
        )
        == cikis
    )
    assert k.cagri == int(koken == "indirme")
    satirlar = [json.loads(s) for s in gecmis.read_text(encoding="utf-8").splitlines()]
    son_ekran = ekran.read_text(encoding="utf-8").splitlines()
    assert len(son_ekran) == 6
    assert son_ekran[5].startswith("Eylem: İstenen gün: 2026-10-24. ")
    if koken == "indirme":
        assert not any(
            s.get("durum") in ("KART GÜNLÜĞÜ EKSİK", "KAYIT ÇELİŞKİSİ")
            for s in satirlar
        )
        if secim == "eksik":
            assert son_ekran[0] == "SORUNLU"
            assert gecmis.read_bytes() == kabul
        else:
            assert son_ekran[0] == "BUGÜN ÇUBUK YOK"
            assert satirlar[-1] == {
                "tarih": "2026-10-24",
                "anlik": "20261005-1930",
                "kartlar": [],
                "durum": "BUGÜN ÇUBUK YOK",
            }
    else:
        assert son_ekran[0] == "SORUNLU"
        assert satirlar[-1]["durum"] == "KART GÜNLÜĞÜ EKSİK"
        assert satirlar[-1]["tarih"] == "2026-10-24"


@pytest.mark.parametrize(
    "bozuk", ["eksik_csv", "farkli_csv", "eksik_gunluk", "farkli_gunluk", "ret"]
)
def test_seceneksiz_sakli_basarisi_kabul_edilen_ciktiyi_dogrular(
    tmp_path, monkeypatch, bozuk
):
    kagit_aile()
    a = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI)
    b = veri.indir(["XXXX"], tmp_path, kaynak(), simdi=SIMDI.replace(minute=31))
    for kimlik in (a, b):
        assert (
            gunluk.gunluk(
                TARIH,
                tmp_path,
                simdi=SIMDI,
                kimlik=kimlik,
                cikti_koku=tmp_path / kimlik,
                p=P,
                atr_n=2,
            )
            == 0
        )
    cikti = tmp_path / "sinanan"
    rapor_yolu, kayit_yolu = cikti / "rapor", cikti / "kayit"
    rapor_yolu.mkdir(parents=True)
    kayit_yolu.mkdir()
    (rapor_yolu / "durum.txt").write_bytes(
        (tmp_path / a / "rapor/durum.txt").read_bytes()
    )
    csv_yolu = rapor_yolu / "kartlar-20261005.csv"
    csv_once = (
        tmp_path / (b if bozuk == "farkli_csv" else a) / "rapor/kartlar-20261005.csv"
    ).read_bytes()
    if bozuk != "eksik_csv":
        csv_yolu.write_bytes(csv_once)
    gunluk_yolu = kayit_yolu / "kartlar.jsonl"
    once = (
        b""
        if bozuk == "eksik_gunluk"
        else (
            tmp_path / (b if bozuk == "farkli_gunluk" else a) / "kayit/kartlar.jsonl"
        ).read_bytes()
    )
    if bozuk == "ret":
        once += (
            json.dumps(
                {"tarih": "2026-10-05", "anlik": a, "durum": "KART GÜNLÜĞÜ EKSİK"},
                ensure_ascii=False,
            )
            + "\n"
        ).encode("utf-8")
    if once:
        gunluk_yolu.write_bytes(once)
    monkeypatch.setattr(rapor, "RAPOR_DIZINI", rapor_yolu)
    monkeypatch.setattr(kayit, "KAYIT_DIZINI", kayit_yolu)
    k = kaynak()
    assert (
        gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kaynak=k, semboller=["XXXX"]) == 1
    )
    assert k.cagri == 0
    assert gunluk_yolu.read_bytes().startswith(once)
    assert (rapor_yolu / "durum.txt").read_text(encoding="utf-8").startswith("SORUNLU")
    if bozuk == "eksik_csv":
        assert not csv_yolu.exists()
    else:
        assert csv_yolu.read_bytes() == csv_once
