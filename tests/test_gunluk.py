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

import pandas as pd
import pytest

from tansu import aileler, gunluk, kayit, rapor, veri
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


def fiyatlar(bozuk=False):
    kap = [100.0] * 5 + [103.0]
    yuk = [100.5, 100.5, 101, 100.5, 100.5, 103.5]
    sonuc = []
    for g, k, y in zip(pd.bdate_range("2026-09-28", periods=6), kap, yuk):
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


def test_gunluk_anlik_goruntuler_30_gun_sonra_silinir_denemede_gecenler_kalir(tmp_path):
    ag = tmp_path / "gunluk" / "ag"
    for ad in ("20260801-1930", "20260802-1930", "20260904-1930", "20260906-1930"):
        (ag / ad).mkdir(parents=True)
    kayit._yaz({"tur": "deneme", "olay": "basladi", "anlik": "20260802-1930"})
    kos(tmp_path)
    # 05.10 − 04.09 = 31 gün (silinir); 05.10 − 06.09 = 29 gün (kalır); 02.08 denemede geçiyor (kalır).
    assert sorted(p.name for p in ag.iterdir()) == [
        "20260802-1930",
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
            ["AKTİF", "AKTİF", "BOZULDU", "BOZULDU", None],
            0,
        ),
        (
            [(113.3, 112.8, 113.3), (113, 112.5, 113.5)],
            ["AKTİF", "BOZULDU", None],
            0,
        ),
        (
            [(104, 103.5, 104.5), (105, 200, 105.5), (106, 105.5, 106.5)],
            ["AKTİF", "AKTİF", "BOZULDU", None],
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
        pd.bdate_range("2026-10-06", periods=len(devam)), devam
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
        {"XXXX": fiyatlar(), "YYYY": fiyatlar(), "ZZZZ": fiyatlar()},
        {"XXXX": [], "YYYY": [], "ZZZZ": []},
    )
    veri.indir(
        ["XXXX"], tmp_path, k, simdi=dt.datetime(2026, 10, 4, 19, 30)
    )  # evren tabanı
    k.istenen.clear()
    hisse, durum = anahtarlar
    satir = {
        "tarih": "2026-10-02",
        "anlik": "20261002-1930",
        "kartlar": [
            {hisse: "YYYY", durum: "AKTİF"},
            {hisse: "ZZZZ", durum: "STOP"},
        ],
    }
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(satir) + "\n", encoding="utf-8")
    gunluk.gunluk(TARIH, tmp_path, simdi=SIMDI, kaynak=k, p=P, atr_n=2)
    assert "YYYY" in k.istenen and "ZZZZ" not in k.istenen
