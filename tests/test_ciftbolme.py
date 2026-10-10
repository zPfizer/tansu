"""`kosu()` yüzü, çift bölmesi (TASARIM 5.6 "Çift bölmesi kuralları", 5.7 K2 ve tanısal 50/50).

Sentetik anlık görüntü, hepsi `kayit.kosu` üzerinden; sonuç `kosu(...)["cift"]`. Veri 01.12.2014 – 31.03.2017 iş günleri;
2016'nın ilk işlem günü S16 (01.01.2016, konum 284), 2017'nin ilki S17 (02.01.2017, konum 545). Faiz 0. Fiyat adımı,
kilit ve karantina bayrakları gerçek `veri` koduyla hesaplanır. EMA ailesi sinyal vermesin diye ısınma çok büyüktür.

Sabit çift (VAKBN–GARAN): GARAN(t) = 100 + 5 sin(t/15), VAKBN = GARAN · exp(s), s(t) = 0,001·(−1)^t + 0,0003 sin(t/3,7)
(sınırlı gürültü: tek başına |Z| < 2) ve elle konan sıçramalar. Z penceresi 60, ddof 1. Elle hesap, t0 = 289:
- t0'da s = −0,05 (başka gün ≈ 0): pencerede tek büyük değer a için σ ≈ |a|/√60 → Z(t0) ≈ −7,4; ΔZ < 0, Z ≥ 2 değil: sinyal yok.
- t0+1'de s = −0,02: ortalama ≈ −0,0012, σ ≈ 0,0070 → Z ≈ −2,7 ≤ −2; ΔZ ≈ +4,7 > 0 → hedef Y; geçiş t0+2'de AOF'tan.
- t1 = t0+70'te (t0 sıçramaları pencereden çıktı) simetri: Z(t1+1) ≈ +2,7, ΔZ ≈ −4,7 < 0 → hedef X; geçiş t1+2'de.
Başka gün |Z| < 2 (gürültü tek başına |Z| ≤ 1,3; sıçrama pencerede iken σ büyür, Z daha da küçülür).
"""

import datetime as dt

import numpy as np
import pandas as pd
import pytest

from tansu import aileler, kayit, veri
from tansu.kaynak import KaynakHatasi
from tests.test_simulator import mum
from tests.test_veri import SahteBorsapy, SahteKaynak

GUN = pd.bdate_range("2014-12-01", "2017-03-31")
T = np.arange(len(GUN))
S16, S17 = (
    GUN.get_loc(pd.Timestamp("2016-01-01")),
    GUN.get_loc(pd.Timestamp("2017-01-02")),
)
ILK = GUN.get_loc(pd.Timestamp("2015-12-01"))
SON = len(GUN) - 1
P, ATR_N = aileler.Parametre(isinma=100_000), 14
T0, T1 = S16 + 5, S16 + 75


class SektorBorsapy(SahteBorsapy):
    def sektor(self, sembol):
        if sembol not in self._sektor:
            raise KaynakHatasi(sembol)
        return self._sektor[sembol]


def seri(fiyat, bas=0, son=None, hacim=1e9):
    return [
        mum(g, float(f), hacim=hacim)
        for g, f in zip(GUN[bas:son], np.asarray(fiyat)[bas:son])
    ]


def kos(tmp_path, fiyatlar, sektor=None, tam=False):
    """`fiyatlar`: sembol → fiyat dizisi ya da (dizi, bas, son, hacim)."""
    seriler = {}
    for s, f in fiyatlar.items():
        seriler[s] = seri(*f) if isinstance(f, tuple) else seri(f)
    k = SahteKaynak(seriler, {s: [] for s in seriler})
    kimlik = veri.indir(
        list(seriler),
        tmp_path,
        k,
        simdi=dt.datetime(2026, 10, 5, 19, 30),
        borsapy=SektorBorsapy([("2014-01-01", 0.0)], sektor or {}),
    )
    kayit.kayitla(P, ATR_N)
    s = kayit.kosu(kimlik, tmp_path, p=P, atr_n=ATR_N, git=lambda: ("abc", False))
    return s if tam else s["cift"]


def sabit(olaylar):
    """(VAKBN, GARAN) fiyat dizileri; `olaylar`: konum → s değeri."""
    garan = 100 + 5 * np.sin(T / 15)
    s = 0.001 * (-1.0) ** T + 0.0003 * np.sin(T / 3.7)
    for t, v in olaylar.items():
        s[t] = v
    return garan * np.exp(s), garan


OLAY = {T0: -0.05, T0 + 1: -0.02, T1: 0.05, T1 + 1: 0.02}


def sonuc(c, m=0.003):
    return c["sabit"][m]


def test_sabit_cift_gecis_gunleri_adet_ve_ilk_sinyale_kadar_nakit(tmp_path):
    # Geçişler: t0+2'de Y'ye (VAKBN), t1+2'de X'e (GARAN). Tek pay = 1.000.000 TL. Adet = ⌊pay / (fiyat · 1,003)⌋.
    vakbn, garan = sabit(OLAY)
    c = kos(tmp_path, {"VAKBN": vakbn, "GARAN": garan})
    t = sonuc(c)["islemler"]
    assert [
        (r.sembol, r.giris_tarih, r.cikis_tarih, r.neden) for r in t.itertuples()
    ] == [
        ("VAKBN", GUN[T0 + 2], GUN[T1 + 2], "gecis"),
        ("GARAN", GUN[T1 + 2], GUN[SON], "veri_sonu"),
    ]
    a, b = t.iloc[0], t.iloc[1]
    assert a.giris_fiyat == pytest.approx(
        vakbn[T0 + 2]
    ) and a.cikis_fiyat == pytest.approx(vakbn[T1 + 2])
    assert a.adet == int(1_000_000 // (1.003 * vakbn[T0 + 2]))
    nakit = 1_000_000 - a.adet * vakbn[T0 + 2] * 1.003 + a.adet * vakbn[T1 + 2] * 0.997
    assert b.adet == int(
        nakit // (1.003 * garan[T1 + 2])
    ) and b.giris_fiyat == pytest.approx(garan[T1 + 2])
    assert b.getiri == pytest.approx(garan[SON] * 0.997 / (garan[T1 + 2] * 1.003) - 1)
    oz = sonuc(c)["ozkaynak"]
    assert (
        oz.loc[GUN[ILK]] == 1_000_000 and oz.loc[GUN[T0 + 1]] == 1_000_000
    )  # ilk sinyale kadar nakit


def test_kilitli_bacakta_gecis_olmaz_ve_sinyal_tasinmaz(tmp_path):
    # t1+2'de VAKBN tavan kilidinde (önceki kapanışın tam %20 üstü, ±%20 rejimi). Geçiş yapılmaz. Ertesi gün VAKBN
    # önceki fiyata döner; t1+2 kapanışında s ≈ +0,20: Z ≈ +7,4, ΔZ ≈ +4,7 > 0 → X sinyali yok; sonraki günler de yok.
    # Eski sinyal (t1+1) taşınmaz: VAKBN veri sonuna kadar tutulur.
    vakbn, garan = sabit(OLAY)
    vakbn = vakbn.copy()
    vakbn[T1 + 2] = vakbn[T1 + 1] * 1.2
    vakbn[T1 + 3] = garan[T1 + 3] * np.exp(
        0.001 * (-1.0) ** (T1 + 3) + 0.0003 * np.sin((T1 + 3) / 3.7)
    )
    t = sonuc(kos(tmp_path, {"VAKBN": vakbn, "GARAN": garan}))["islemler"]
    assert [
        (r.sembol, r.giris_tarih, r.cikis_tarih, r.neden) for r in t.itertuples()
    ] == [("VAKBN", GUN[T0 + 2], GUN[SON], "veri_sonu")]


def test_kapanan_bacak_pay_nakde_gecer(tmp_path):
    # VAKBN son kez t0+10'da işlem görür; 61. işlem günü (t0+71) kapanma günüdür (TASARIM 5.2): tutulan VAKBN 0
    # fiyatla kapanır (−%100) ve pay yıl sonuna dek nakitte kalır; t1 sıçramaları geçiş doğurmaz (çift dondu).
    # Son özkaynak = 1.000.000 − adet · giriş · 1,003 (faiz 0).
    vakbn, garan = sabit(OLAY)
    c = kos(tmp_path, {"VAKBN": (vakbn, 0, T0 + 11), "GARAN": garan})
    t = sonuc(c)["islemler"]
    assert [
        (r.sembol, r.giris_tarih, r.cikis_tarih, r.cikis_fiyat, r.neden)
        for r in t.itertuples()
    ] == [("VAKBN", GUN[T0 + 2], GUN[T0 + 71], 0.0, "kapanma")]
    assert t.iloc[0].getiri == pytest.approx(-1.0)
    assert sonuc(c)["ozkaynak"].iloc[-1] == pytest.approx(
        1_000_000 - t.iloc[0].adet * vakbn[T0 + 2] * 1.003, abs=1e-6
    )


def test_tanisal_elli_elli_baslangicta_bir_kez_alinir_ve_tutulur(tmp_path):
    # İlk geçişten önceki gün (ILK) 1.000.000; ILK+1 AOF'unda her bacağa 500.000 TL: adet = ⌊500000 / (fiyat · 1,003)⌋.
    # AOF = kapanış → ILK+1 kapanış özkaynağı = 1.000.000 − 0,003 · (aV·pV + aG·pG). Sonra dengeleme yok:
    # son özkaynak = nakit + aV · VAKBN(son) + aG · GARAN(son).
    vakbn, garan = sabit(OLAY)
    e = sonuc(kos(tmp_path, {"VAKBN": vakbn, "GARAN": garan}))["elli_elli"]
    q = ILK + 1
    av, ag = int(500_000 // (1.003 * vakbn[q])), int(500_000 // (1.003 * garan[q]))
    nakit = 1_000_000 - (av * vakbn[q] + ag * garan[q]) * 1.003
    assert e.loc[GUN[ILK]] == 1_000_000
    assert e.loc[GUN[q]] == pytest.approx(
        1_000_000 - 0.003 * (av * vakbn[q] + ag * garan[q])
    )
    assert e.iloc[-1] == pytest.approx(nakit + av * vakbn[SON] + ag * garan[SON])


def test_sabit_cift_secimden_bagimsiz_ve_k2_ilk_gun_baslangic(tmp_path):
    # Sektör verilmedi: hiçbir çift seçilmez (iki yıl da "işlem yok"), ama VAKBN–GARAN yine işlem yapar.
    vakbn, garan = sabit(OLAY)
    c = kos(tmp_path, {"VAKBN": vakbn, "GARAN": garan})
    assert len(c["secim"]) == 0 and c["islem_yok"] == [2016, 2017]
    assert len(c["masraf"][0.003]["islemler"]) == 0 and len(sonuc(c)["islemler"]) == 2
    assert sonuc(c)["k2"].iloc[0] == 1_000_000
    assert set(c["masraf"]) == set(c["sabit"]) == {0.001, 0.003, 0.005}


def test_tutulan_bacakta_karantina_son_temiz_aofta_kapatir_cift_girissiz_kalir(
    tmp_path,
):
    # t0+5'te VAKBN, önceki kapanışın 1,5 katına çıkar (limit ±%20 aşıldı, olay yok) → karantina günü ve sonraki 250 satır.
    # Tutulan VAKBN karantina gününde, son temiz AOF'tan (t0+4 AOF = kapanış) kapanır. t1 sinyalleri karantina penceresinde
    # (t0+5 … t0+254) yoksayılır: tek işlem. Son özkaynak = 1.000.000 − adet · giriş · 1,003 + adet · çıkış · 0,997.
    vakbn, garan = sabit(OLAY)
    vakbn = vakbn.copy()
    vakbn[T0 + 5 :] *= 1.5
    c = kos(tmp_path, {"VAKBN": vakbn, "GARAN": garan})
    t = sonuc(c)["islemler"]
    assert [
        (r.sembol, r.giris_tarih, r.cikis_tarih, r.neden) for r in t.itertuples()
    ] == [("VAKBN", GUN[T0 + 2], GUN[T0 + 5], "karantina")]
    a = t.iloc[0]
    assert a.cikis_fiyat == pytest.approx(vakbn[T0 + 4])
    assert sonuc(c)["ozkaynak"].iloc[-1] == pytest.approx(
        1_000_000 - a.adet * vakbn[T0 + 2] * 1.003 + a.adet * vakbn[T0 + 4] * 0.997,
        abs=1e-6,
    )


def test_rapor_cift_bolumu_ve_yasakli_sozcuk_yok(tmp_path):
    import re

    vakbn, garan = sabit(OLAY)
    s = kos(tmp_path, {"VAKBN": vakbn, "GARAN": garan}, tam=True)
    html = s["rapor"].read_text(encoding="utf-8")
    for beklenen in (
        "<h2>Çift rotasyonu</h2>",
        "VAKBN–GARAN (sabit çift)",
        "50/50",
        "işlem yok",
        "K2",
    ):
        assert beklenen in html
    assert html.count("<h2>Uyarılar</h2>") == 1
    assert not re.search(r"\b(AL|SAT|ÖNERİ)\b|Tansu'nun sistemi", html)
    csv = pd.read_csv(
        s["rapor"].parent / f"cift-islemler-{s['kosu_id']}.csv", encoding="utf-8"
    )
    assert list(csv.columns) == [
        "cift",
        "sembol",
        "giris_tarih",
        "giris_fiyat",
        "cikis_tarih",
        "cikis_fiyat",
        "neden",
        "adet",
        "getiri",
        "aile",
    ]


# ---- yıllık seçim ve yıl geçişi: gerçekçi (tohumlu) veri ----


def ar1(tohum, phi=0.7, sd=0.01):
    e = np.random.default_rng(tohum).normal(0, sd, len(T))
    s = np.zeros(len(T))
    for i in range(1, len(T)):
        s[i] = phi * s[i - 1] + e[i]
    return s


def rw(tohum, sd=0.01):
    return np.random.default_rng(tohum).normal(0, sd, len(T)).cumsum()


def fiyat(log_fiyat):
    return 100 * np.exp(log_fiyat)


def dummy(adet):
    return {
        f"D{i}": (np.full(len(T), 100.0), 0, None, 1e3) for i in range(adet)
    }  # en az likit: evren elemesine girer


def test_secim_kurallari(tmp_path):
    # 14 gerçek + 3 düz hisse: evrenden en düşük hacimli int(17 · 0,2) = 3 düz hisse elenir.
    # S1: A–E aynı ortak yol + AR(1) fark: hepsi eşbütünleşik; en fazla 2 çift, hisse başına tek çift → 4 farklı hisse.
    # S2: G = 10⁴ / F (β = −1): eşbütünleşik ama β ≤ 0 → elenir. S3: H, I bağımsız yürüyüş (p > 0,05).
    # S4: K'nın verisi seçim gününden önce yalnız 100 gün (< 252) → aday değil. L (S5) ve M (S6): eşbütünleşik
    # ama sektörleri farklı. N: sektörü yok, A–E ile aynı ortak yola sahip ama aday olamaz.
    taban, taban2, taban3 = rw(1), rw(2), rw(3)
    f = {k: fiyat(taban + ar1(10 + i)) for i, k in enumerate("ABCDE")}
    f["F"] = fiyat(taban2)
    f["G"] = 1e4 / f["F"] * np.exp(ar1(30))
    f["H"], f["I"] = (
        fiyat(rw(43)),
        fiyat(rw(143)),
    )  # 2016 seçim penceresinde Engle–Granger p ≈ 0,74
    f["J"] = fiyat(taban3 + ar1(50))
    f["K"] = (fiyat(taban3 + ar1(51)), S16 - 100, None)
    f["L"], f["M"] = fiyat(taban2 + ar1(60)), fiyat(taban2 + ar1(61))
    f["N"] = fiyat(taban + ar1(70))
    f.update(dummy(3))
    sektor = {
        **dict.fromkeys("ABCDE", "S1"),
        "F": "S2",
        "G": "S2",
        "H": "S3",
        "I": "S3",
        "J": "S4",
        "K": "S4",
        "L": "S5",
        "M": "S6",
    }
    s = kos(tmp_path, f, sektor)["secim"]
    s16 = s[s["yil"] == 2016]
    assert len(s16) == 2 and set(s16["sektor"]) == {"S1"}
    hisseler = list(s16["y"]) + list(s16["x"])
    assert len(set(hisseler)) == 4 and set(hisseler) <= set("ABCDE")
    assert (
        all(y < x for y, x in zip(s16["y"], s16["x"]))
        and (s16["p"] < 0.05).all()
        and (s16["beta"] > 0).all()
    )


def kur_yil_gecisi():
    # Sektör S1: A, B 2016 seçiminde eşbütünleşik; 2016'dan sonra B bağımsız yürüyüşe geçer (S16'da süreklidir) → 2017'de
    # elenir (p ≈ 0,97). S2: C, D her iki yıl da eşbütünleşik (devam eder). S3: E, F 2015'te bağımsız yürüyüş, 2016'dan
    # sonra eşbütünleşik → yalnız 2017'de seçilir.
    t1, t2, t3 = rw(207), rw(102), rw(103)
    b_log, bagimsiz_b = t1 - ar1(110), rw(307)
    b_log = np.where(T <= S16, b_log, b_log[S16] + bagimsiz_b - bagimsiz_b[S16])
    bagimsiz, a = rw(131), ar1(132)
    f_log = np.where(
        T <= S16, bagimsiz, bagimsiz[S16] + (t3 - t3[S16]) + (a - a[S16])
    )  # S16'da süreklidir
    f = {
        "A": fiyat(t1),
        "B": fiyat(b_log),
        "C": fiyat(t2 + ar1(122)),
        "D": fiyat(t2 + ar1(123)),
        "E": fiyat(t3),
        "F": fiyat(f_log),
    }
    return f, {"A": "S1", "B": "S1", "C": "S2", "D": "S2", "E": "S3", "F": "S3"}


def test_yil_gecisi_dusen_cift_kapanir_devam_eden_islemsiz_surer_yeni_cift_esit_pay_alir(
    tmp_path,
):
    f, sektor = kur_yil_gecisi()
    f.update(dummy(1))
    c = kos(tmp_path, f, sektor)
    s = c["secim"]
    cift = lambda y: set(zip(s[s["yil"] == y]["y"], s[s["yil"] == y]["x"]))  # noqa: E731
    assert cift(2016) == {("A", "B"), ("C", "D")} and cift(2017) == {
        ("C", "D"),
        ("E", "F"),
    }
    t = c["masraf"][0.003]["islemler"]
    gecis = GUN[S17 + 1]  # seçimden sonraki ilk işlem günü
    ab = t[t["cift"] == "A-B"]
    assert (
        ab.iloc[-1].neden == "yil_gecisi" and ab.iloc[-1].cikis_tarih == gecis
    )  # düşen çift o gün AOF'ta kapanır
    cd = t[t["cift"] == "C-D"]
    assert not (cd["neden"] == "yil_gecisi").any()  # devam eden çift işlemsiz sürer
    assert ((cd["giris_tarih"] < gecis) & (cd["cikis_tarih"] > gecis)).any()
    # Paylar: ilk yıl her pay 1.000.000 / 5 = 200.000; ilk alış adedi ⌊pay / (fiyat · 1,003)⌋.
    for k in ("A-B", "C-D"):
        ilk = t[t["cift"] == k].iloc[0]
        assert ilk.adet == int(200_000 // (1.003 * ilk.giris_fiyat))
    # 2017: boşta 3 pay (600.000) + A–B payının satış sonrası nakdi, devam etmeyen 4 pay arasında eşit bölünür.
    ab_nakit = (
        200_000
        + (ab["adet"] * (ab["cikis_fiyat"] * 0.997 - ab["giris_fiyat"] * 1.003)).sum()
    )
    ef = t[t["cift"] == "E-F"].iloc[0]
    assert ef.adet == int((600_000 + ab_nakit) / 4 // (1.003 * ef.giris_fiyat))


def test_cift_cikmayan_yil_islem_yok_isaretlenir(tmp_path):
    f, sektor = kur_yil_gecisi()
    f = {k: f[k] for k in "AB"}
    c = kos(tmp_path, f, {"A": "S1", "B": "S1"})
    assert c["islem_yok"] == [2017]
    t = c["masraf"][0.003]["islemler"]
    assert t.iloc[-1].neden == "yil_gecisi" and t.iloc[-1].cikis_tarih == GUN[S17 + 1]
    assert c["masraf"][0.003]["yatirim"].iloc[-1] == 0.0  # 2017'de nakitte
