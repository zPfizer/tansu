"""`kosu()` yüzü, simülatör ve rapor (TASARIM 5.6 simülatör kuralları, 5.7 K2, 6.8 rapor).

Sentetik anlık görüntü, hepsi `kayit.kosu` üzerinden. Temel seri (tests/test_motor.py'deki elle hesap):
26.01.2026'dan 8 işlem günü, kapanış = AOF = [100,100,100,100,100,103,104,105], yüksek [100,5 ... 105,5],
düşük = kapanış - 0,5. Sinyal 02.02 (gün 5), giriş 03.02 AOF 104, çıkış 04.02 kapanış 105 (veri sonu).
ATR(2) gün 5 = 2,28125, stop mesafesi 4,5625. Simülasyon 02.02'de başlar; ilk özkaynak 1.000.000 TL.
Masraf %0,3. Faiz aksi söylenmedikçe 0. Beklenen değerler elle hesaplanmıştır (her testin yorumunda).
"""

import datetime as dt
import re

import pandas as pd
import pytest

from tansu import aileler, kayit, rapor, simulator, veri
from tests.test_veri import SahteBorsapy, SahteKaynak, satir

P = aileler.Parametre(
    periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=4, sma_n=2
)
ATR_N = 2
BAS = "2026-02-02"
KAP = [100.0] * 5 + [103.0, 104.0, 105.0]
YUK = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5]
M3 = 0.003


def mum(gun, kapanis, yuksek=None, dusuk=None, hacim=1e9, pd_=1e12):
    s = satir(gun, kapanis, kapanis)
    yuksek, dusuk = yuksek or kapanis, dusuk or kapanis
    s.update(
        yuksek=yuksek,
        ham_yuksek=yuksek,
        dusuk=dusuk,
        ham_dusuk=dusuk,
        hacim=hacim,
        pd=pd_,
    )
    return s


def sinyalli(olcek=1.0, hacim=1e9, genis=0.5):
    """Temel seri; `genis` düşüğün kapanıştan uzaklığı (ATR'yi büyütür, sinyali değiştirmez)."""
    return [
        mum(g, k * olcek, y * olcek, (k - genis) * olcek, hacim)
        for g, k, y in zip(pd.bdate_range("2026-01-26", periods=8), KAP, YUK)
    ]


def duz(hacim, adet=8, bas="2026-01-26"):
    return [
        mum(g, 100.0, 100.0, 100.0, hacim) for g in pd.bdate_range(bas, periods=adet)
    ]


def kos(tmp_path, seriler, faiz=0.0, bas=BAS):
    k = SahteKaynak(seriler, {s: [] for s in seriler})
    b = SahteBorsapy([("2025-01-01", faiz)], {s: "X" for s in seriler})
    kimlik = veri.indir(
        list(seriler), tmp_path, k, simdi=dt.datetime(2026, 10, 5, 19, 30), borsapy=b
    )
    kayit.kayitla(P, ATR_N)
    return kimlik, kayit.kosu(
        kimlik, tmp_path, p=P, atr_n=ATR_N, git=lambda: ("abc", False), bas=bas
    )


def sim(sonuc, masraf=M3):
    return sonuc["sim"]["masraf"][masraf]


@pytest.mark.parametrize("dosya", ["rapor", "csv"])
def test_rapor_ayni_kosu_kimliginde_onceki_dosyanin_ustune_yazmaz(tmp_path, dosya):
    # TASARIM 6.8: ikinci yazım reddedilebilir ya da yeni dosya kullanabilir; ilki değişmez.
    _, ilk = kos(tmp_path / "ilk", {"A": sinyalli()})
    yol = ilk[dosya]
    once = yol.read_bytes()
    fiyat = sinyalli()
    fiyat[-1] = mum(pd.Timestamp("2026-02-04"), 106, 106.5, 105.5)
    kimlik, ikinci = kos(tmp_path / "ikinci", {"A": fiyat})
    # İki boş işlem listesi sahte yeşil vermez.
    assert ikinci[dosya].read_bytes() != once
    try:
        rapor.yaz(
            ikinci["sim"],
            {"kosu_id": ilk["kosu_id"], "anlik": kimlik, "kod_hash": "abc123"},
            cift=ikinci["cift"],
        )
    except FileExistsError:
        pass  # Aynı kimlikte yazımı reddetmek sözleşmeye uygundur; dosya yine denetlenir.
    assert yol.read_bytes() == once


def test_tavan_baglar_ve_nakit_hesabi(tmp_path):
    # E = 1.000.000, giriş 104. Risk adedi 10000/4,5625 = 2191; tavan 100000/104 = 961; likidite 0,02*1e9/104 = 192307;
    # nakit 1e6/(104*1,003) = 9586. En küçük 961 (tavan). Giriş 961*104*1,003 = 100.243,832; çıkış 961*105*0,997 = 100.602,285.
    # Son nakit = 1.000.000 - 100.243,832 + 100.602,285 = 1.000.358,453.
    _, s = kos(tmp_path, {"A": sinyalli()})
    t = sim(s)["islemler"]
    assert len(t) == 1
    a = t.iloc[0]
    assert (a.sembol, a.adet, a.bagli, a.giris_fiyat, a.cikis_fiyat) == (
        "A",
        961,
        "tavan",
        104.0,
        105.0,
    )
    assert sim(s)["ozkaynak"].iloc[-1] == pytest.approx(1000358.453, abs=1e-3)
    assert sim(s)["reddedilen"] == 0


def test_likidite_baglar(tmp_path):
    # Hacim 1e6 TL/gün: 0,02*1e6/104 = 192,3 → 192 (tavan 961, risk 2191).
    _, s = kos(tmp_path, {"A": sinyalli(hacim=1e6)})
    a = sim(s)["islemler"].iloc[0]
    assert (a.adet, a.bagli) == (192, "likidite")


def test_risk_baglar(tmp_path):
    # Düşük = kapanış - 8: TR = [8,5; 8,5; 9; 8,5; 8,5; 8,5] (gün 0-5), ATR(2): g1 = 8,5; g2 = 8,75; g3 = 8,625; g4 = 8,5625;
    # g5 = 8,53125. Stop = 104 - 17,0625 = 86,9375 (giriş günü düşüğü 96, dokunmaz).
    # Risk adedi 10000/17,0625 = 586,08 → 586; tavan 961. Planlanan risk 586*17,0625 = 9998,625.
    _, s = kos(tmp_path, {"A": sinyalli(genis=8)})
    a = sim(s)["islemler"].iloc[0]
    assert (a.adet, a.bagli) == (586, "risk")
    assert a.planlanan_risk == pytest.approx(9998.625, abs=1e-9)


def test_nakit_baglar_en_likit_once_ve_yer_yetmeyen_reddedilir(tmp_path):
    # 11 sinyalli hisse S01..S11 (hacim 1,9e9 .. 0,9e9, S01 en likit) + 2 sinyalsiz D1, D2 (hacim 1e3).
    # Evren: 13 hisse, en düşük %20 = int(2,6) = 2 elenir (D1, D2); 11 üye.
    # Her giriş 961 adet = 100.243,832 TL. İlk dokuz: 902.194,488; nakit 97.805,512.
    # Onuncu: nakit adedi 97.805,512 / 104,312 = 937,6 → 937 (tavan 961), bağlayıcı nakit.
    # On pozisyon dolu: S11 (en az likit) reddedilir.
    seriler = {f"S{i:02d}": sinyalli(hacim=2e9 - i * 1e8) for i in range(1, 12)}
    seriler |= {"D1": duz(1e3), "D2": duz(1e3)}
    _, s = kos(tmp_path, seriler)
    t = sim(s)["islemler"].sort_values("sembol")
    assert list(t.sembol) == [f"S{i:02d}" for i in range(1, 11)]
    assert list(t.adet) == [961] * 9 + [937]
    assert list(t.bagli) == ["tavan"] * 9 + ["nakit"]
    assert sim(s)["reddedilen"] == 1


def test_faiz_bir_gun_gecikmeli_gece_basina_tahakkuk_eder(tmp_path):
    # Yıllık %36,5 → gece başına 0,001. 02.02: faiz yok. 03.02: 1.000.000 * 0,001 → nakit 1.001.000;
    # giriş 100.243,832 (adet 961: boyutlandırma özkaynağı önceki kapanış 1.000.000) → 900.756,168.
    # 04.02: 900.756,168 * 0,001 = 900,756168 → 901.656,924168; çıkış +100.602,285 → 1.002.259,209168.
    _, s = kos(tmp_path, {"A": sinyalli()}, faiz=36.5)
    oz = sim(s)["ozkaynak"]
    assert list(oz.index) == list(
        pd.to_datetime(["2026-02-02", "2026-02-03", "2026-02-04"])
    )
    assert oz.iloc[0] == pytest.approx(1000000.0, abs=1e-6)
    assert oz.iloc[1] == pytest.approx(
        900756.168 + 99944.0, abs=1e-3
    )  # 961 adet kapanış 104
    assert oz.iloc[2] == pytest.approx(1002259.209168, abs=1e-3)


def test_k2_maruziyet_kuralinkine_esit(tmp_path):
    # Tek üye A. Sepet: 02.02 AOF 103'ten alınır (kuruluş masrafı 0,003) → 0,997; 03.02 ×104/103; 04.02 ×105/104.
    # Kuralın kapanış payı: 02.02 0; 03.02 99.944 / (1.000.000 - 100.243,832 + 99.944) = 99.944/999.700,168; 04.02 0.
    # K2: 02.02 1e6; 03.02 1e6 * (1 + pay * (104/103 - 1)) = 1.000.970,6211; 04.02 pay 0 → değişmez.
    _, s = kos(tmp_path, {"A": sinyalli()})
    k2, sepet = sim(s)["k2"], sim(s)["sepet"]
    assert list(sepet.round(6)) == [
        0.997,
        round(0.997 * 104 / 103, 6),
        round(0.997 * 105 / 103, 6),
    ]
    assert list(k2.iloc[:2].round(4)) == [1000000.0, 1000970.6211]
    assert k2.iloc[2] == pytest.approx(1000970.6211, abs=1e-4)


def test_k2_ay_basi_dengelemesi_masraf_oder(tmp_path):
    # Beş hisse A..E, tarihler 30.01, 02.02, 03.02, 27.02, 02.03, 03.03. C 27.02'de 100 → 110, öteki hisseler 100.
    # Şubat evreni (referans 30.01, medyan hacim A 10, B 20, C 30, D 40, E 50): A elenir → B, C, D, E.
    # Mart evreni (referans 27.02, 4 günlük pencere): A [10,100,100,100] medyan 100; B [20,5,5,5] medyan 5 → B elenir → A, C, D, E.
    # Sepet: 02.02 kuruluş masrafı 0,003 → 0,997; 03.02 aynı; 27.02 ×(3 + 1,1)/4 = 1,025 → 1,021925.
    # 02.03: eski ağırlıklar B, D, E = 1/4,1; C = 1,1/4,1; yeni A, C, D, E = 0,25. Devir = B çıkar 1/4,1 + A girer 0,25
    # + C azalır (1,1/4,1 - 0,25) + D ve E artar 2*(0,25 - 1/4,1) = 0,5 + 0,1/4,1 = 0,5243902.
    # Masraf 0,003 * 0,5243902 = 0,0015731707 → 1,021925 * (1 - 0,0015731707) = 1,0203173375.
    gun = pd.to_datetime(
        [
            "2026-01-30",
            "2026-02-02",
            "2026-02-03",
            "2026-02-27",
            "2026-03-02",
            "2026-03-03",
        ]
    )
    hacim = {
        "A": [10, 100, 100, 100, 100, 100],
        "B": [20, 5, 5, 5, 5, 5],
        "C": [30] * 6,
        "D": [40] * 6,
        "E": [50] * 6,
    }
    fiyat = {"C": [100, 100, 100, 110, 110, 110]}

    def uret(ad):
        return [
            mum(g, float(fiyat.get(ad, [100] * 6)[i]), hacim=float(hacim[ad][i]))
            for i, g in enumerate(gun)
        ]

    _, s = kos(tmp_path, {ad: uret(ad) for ad in "ABCDE"})
    sepet = sim(s)["sepet"]
    assert list(sepet.index) == list(gun[1:])
    assert list(sepet.round(9)) == [0.997, 0.997, 1.021925, 1.020317338, 1.020317338]


def test_kapanan_hisse_acik_pozisyon_eksi_yuz_sayilir(tmp_path):
    # A 04.02'de son kez işlem görür; Z 30.04'e kadar sürer (69 gün). A'nın durdurması 61 işlem günü sürer:
    # kapanma günü = 26.01'den 68. gün = 30.04. Pozisyon (961 adet, giriş 104) o gün 0 fiyatla kapanır.
    # Son nakit = 1.000.000 - 100.243,832 = 899.756,168. Z sinyalsiz.
    _, s = kos(tmp_path, {"A": sinyalli(), "Z": duz(5e8, adet=69)})
    a = sim(s)["islemler"].iloc[0]
    assert (a.neden, a.cikis_fiyat, a.cikis_tarih, a.adet) == (
        "kapanma",
        0.0,
        pd.Timestamp("2026-04-30"),
        961,
    )
    assert a.gerceklesen_kayip == pytest.approx(961 * 104.0)
    assert sim(s)["ozkaynak"].iloc[-1] == pytest.approx(899756.168, abs=1e-3)
    assert s["sim"]["bilgi"]["kapanma"] == 1


def test_evren_disi_sinyal_islem_acmaz(tmp_path):
    # Şubat evreni referansı 30.01: tek hisse hacmi 0 → evrende yok. İşlem yok.
    seri = [
        {**r, "hacim": 0.0} if r["tarih"] == pd.Timestamp("2026-01-30") else r
        for r in sinyalli()
    ]
    _, s = kos(tmp_path, {"A": seri})
    assert len(sim(s)["islemler"]) == 0


def test_rapor_baslik_uyari_yasakli_sozcuk_ve_csv_sutunlari(tmp_path):
    kimlik, s = kos(tmp_path, {"A": sinyalli()})
    html = s["rapor"].read_text(encoding="utf-8")
    kod_hash = kayit._kural(P, ATR_N)["kod_hash"]
    for beklenen in (
        s["kosu_id"],
        kimlik,
        kod_hash,
        "Tansu'dan esinlenen yorum",
        "Yıllık fazla getiri",
    ):
        assert beklenen in html
    assert html.count("<h2>Uyarılar</h2>") == 1
    assert not re.search(r"\b(AL|SAT|ÖNERİ)\b|Tansu'nun sistemi", html)
    csv = pd.read_csv(s["csv"], encoding="utf-8")
    assert list(csv.columns) == [
        "sembol",
        "aile",
        "sinyal_tarih",
        "giris_tarih",
        "giris_fiyat",
        "cikis_tarih",
        "cikis_fiyat",
        "neden",
        "adet",
        "getiri",
        "planlanan_risk",
        "gerceklesen_kayip",
        "bagli",
    ]
    assert s["csv"].name == f"islemler-{s['kosu_id']}.csv" and len(csv) == 1
    # getiri = 105*0,997 / (104*1,003) - 1 = 104,685 / 104,312 - 1 = 0,0035756
    assert csv["getiri"].iloc[0] == pytest.approx(0.0035756, abs=1e-6)


def test_kaynak_gunu_hatasi_raporu_sorunlu_yapmaz_gunu_tarihle_yazar(tmp_path):
    # 20 sembol; 29.01'de 10'unun satırı bozuk (düşük 101 > AOF 100) = yarı: kaynak günü (TASARIM 5.13). Gün eksik gün
    # olarak işlenir, karantina oranı 0; "veri sorunlu" yalnız oran eşiklerinden gelir. Gün raporda tarihle yazılır.
    gunler = pd.bdate_range("2026-01-26", periods=8)
    seriler = {
        f"S{i}": [
            mum(
                g,
                100.0,
                102.0 if (j == 3 and i < 10) else 100.0,
                101.0 if (j == 3 and i < 10) else 100.0,
            )
            for j, g in enumerate(gunler)
        ]
        for i in range(20)
    }
    _, s = kos(tmp_path, seriler)
    html = s["rapor"].read_text(encoding="utf-8")
    assert s["sim"]["bilgi"]["sorunlar"] == ["kaynak günü hatası: 2026-01-29"]
    assert "<td>Veri durumu</td><td>TAMAM</td>" in html
    assert "VERİ SORUNLU" not in html and "kaynak günü hatası: 2026-01-29" in html


def test_uc_masraf_duzeyi_kosulur_ve_yillik_tablo_yazilir(tmp_path):
    # %0,1: 1.000.000 - 99.944*1,001 + 100.905*0,999 = 1.000.000 - 100.043,944 + 100.804,095 = 1.000.760,151.
    # %0,5: 1.000.000 - 99.944*1,005 + 100.905*0,995 = 1.000.000 - 100.443,72 + 100.400,475 = 999.956,755.
    # Yıllık: 2026 kural getirisi (%0,3) = 1.000.358,453 / 1.000.000 - 1.
    _, s = kos(tmp_path, {"A": sinyalli()})
    son = {m: s["sim"]["masraf"][m]["ozkaynak"].iloc[-1] for m in (0.001, 0.003, 0.005)}
    assert son[0.001] == pytest.approx(1000760.151, abs=1e-3)
    assert son[0.005] == pytest.approx(999956.755, abs=1e-3)
    yil = sim(s)["yillik"]
    assert list(yil.index) == [2026]
    assert yil.loc[2026, "kural"] == pytest.approx(0.000358453, abs=1e-9)


def test_yillik_fazla_getiri_gunluk_fazla_getirilerin_yillik_toplamidir(tmp_path):
    # TASARIM 5.8: yıllık fazla = o yıldaki günlük (kural - K2) getirilerin toplamı; iki yıllık getirinin farkı değil.
    # Özkaynak 1.000.000; 999.700,168; 1.000.358,453 -> günlük getiri -0,000299832 ve 658,285/999.700,168 = +0,000658482.
    # K2 1.000.000; 1.000.970,62112; aynı -> günlük 0,00097062112 ve 0. Fazla = 0,00035865 - 0,00097062112 = -0,00061197.
    # (Farkla hesap -0,00061217 verir; 2e-7 fark toleransın üstündedir.)
    _, s = kos(tmp_path, {"A": sinyalli()})
    assert sim(s)["yillik"].loc[2026, "fazla"] == pytest.approx(-0.00061197, abs=2e-9)


def bolme(islemler, hacimler=None):
    """Simülatörün dış girdisi: dört gün sabit fiyat, faizsiz anlık görüntü."""
    gunler = pd.bdate_range("2026-02-02", periods=4)
    semboller = list(islemler["sembol"].unique())
    fiyat = pd.DataFrame(
        [
            dict(mum(g, 100.0, hacim=(hacimler or {}).get(s, 1e9)), sembol=s)
            for s in semboller
            for g in gunler
        ]
    )
    anlik = veri.Anlik(
        "bolme",
        fiyat,
        pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"]),
        pd.DataFrame({"tarih": [pd.Timestamp("2026-01-01")], "faiz": [0.0]}),
    )
    return simulator.calistir(
        anlik,
        islemler,
        bas="2026-02-02",
        masraflar=(0.003,),
        evr={pd.Period("2026-02"): semboller},
    )["masraf"][0.003]


def test_ayni_gun_once_cikis_sonra_giris_sonra_degerleme():
    # TASARIM 5.3, 5.6: on dolu yer çıkışlarla boşalır; yeni giriş kapanışta değerlenir.
    t = pd.DataFrame(
        {
            "sembol": [f"A{i}" for i in range(10)] + ["Z"],
            "sinyal_tarih": [pd.Timestamp("2026-02-02")] * 10
            + [pd.Timestamp("2026-02-03")],
            "giris_tarih": [pd.Timestamp("2026-02-03")] * 10
            + [pd.Timestamp("2026-02-04")],
            "cikis_tarih": [pd.Timestamp("2026-02-04")] * 10
            + [pd.Timestamp("2026-02-05")],
            "giris_fiyat": 100.0,
            "cikis_fiyat": 100.0,
            "adet": 1,
            "planlanan_risk": 4.0,
            "neden": "sma250",
        }
    )
    s = bolme(t)
    # İlk gün 9*1000 + 970 adet; özkaynak 997009. Çıkış nakdi 994018.
    # Z: 997 adet, alış 99999,1, kapanış değeri 99700 -> özkaynak 993718,9.
    assert s["reddedilen"] == 0
    assert s["islemler"].iloc[-1][["sembol", "adet"]].tolist() == ["Z", 997]
    assert s["ozkaynak"].loc["2026-02-04"] == pytest.approx(993718.9)


@pytest.mark.parametrize(
    "risk,hacim,onceki,beklenen,adet",
    [
        (10.0, 5000000.0, 0, "risk", 1000),
        (4.0, 5000000.0, 0, "tavan", 1000),
        (4.0, 4850448.654037888, 9, "likidite", 970),
    ],
)
def test_baglayici_sinir_esitlikte_risk_tavan_likidite_nakit_sirasi(
    risk, hacim, onceki, beklenen, adet
):
    # TASARIM 5.6: eşit sınırlar risk, tavan, likidite, nakit sırasıyla seçilir.
    t = pd.DataFrame(
        {
            "sembol": [f"A{i}" for i in range(onceki)] + ["Z"],
            "sinyal_tarih": pd.Timestamp("2026-02-02"),
            "giris_tarih": pd.Timestamp("2026-02-03"),
            "cikis_tarih": pd.Timestamp("2026-02-05"),
            "giris_fiyat": 100.0,
            "cikis_fiyat": 100.0,
            "adet": 1,
            "planlanan_risk": [4.0] * onceki + [risk],
            "neden": "veri_sonu",
        }
    )
    # Risk=tavan=likidite=1000; tavan=likidite=1000; dokuz alıştan sonra
    # nakit 97300, likidite=nakit=970,0897308075776 adet (tam lot 970).
    z = bolme(t, {"Z": hacim})["islemler"].iloc[-1]
    assert (z.sembol, z.bagli, z.adet) == ("Z", beklenen, adet)


def test_esit_likiditede_sembol_alfabetik_sirayla_girer(tmp_path):
    # TASARIM 5.6: eşit likiditedeki on bir sinyalden alfabetik ilk on alınır.
    seriler = {f"S{i:02d}": sinyalli() for i in range(11, 0, -1)}
    seriler.update({"D1": duz(1e3), "D2": duz(1e3)})
    _, s = kos(tmp_path, seriler)
    assert sim(s)["islemler"]["sembol"].tolist() == [
        "S01",
        "S02",
        "S03",
        "S04",
        "S05",
        "S06",
        "S07",
        "S08",
        "S09",
        "S10",
    ]
    assert sim(s)["reddedilen"] == 1


def test_satis_nakdi_ayni_gun_kullanilir_valor_yok():
    # TASARIM 5.4, 5.6: satış nakdi aynı gün yeni alışın nakit sınırına girer.
    t = pd.DataFrame(
        {
            "sembol": [f"A{i}" for i in range(9)] + ["Z"],
            "sinyal_tarih": [pd.Timestamp("2026-02-02")] * 9
            + [pd.Timestamp("2026-02-03")],
            "giris_tarih": [pd.Timestamp("2026-02-03")] * 9
            + [pd.Timestamp("2026-02-04")],
            "cikis_tarih": [pd.Timestamp("2026-02-04")]
            + [pd.Timestamp("2026-02-05")] * 9,
            "giris_fiyat": 100.0,
            "cikis_fiyat": 100.0,
            "adet": 1,
            "planlanan_risk": 4.0,
            "neden": "sma250",
        }
    )
    # Dokuz alış sonrası nakit 97300, özkaynak 997300. A0 satışı 99700 getirir.
    # Z tavanı 997 adet; satış ertelenirse nakit yalnız 970 adede yeter.
    z = bolme(t)["islemler"].iloc[-1]
    assert (z.sembol, z.adet, z.bagli) == ("Z", 997, "tavan")
