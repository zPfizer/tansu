"""Boru hattı denetimi: sentetik boş veriyle yanlış kabul, enjekte edilmiş etkiyle güç (TASARIM 5.12, B-18).

Boş dünya: sürekli getirileri bağımsız (piyasa + sektör + hisse payı), ne EMA sıkışması ne çift dönüşü getiri öngörür.
Gerçek veriye bağlı değildir; ağa ve gerçek `kayit/`'a çıkmaz. Her tekrar aynı `kayit.hesapla` yolundan (motor, simülatör,
K1, ızgara, Holm, kabul tablosu) geçer; Holm m = 2'dir (iki aile; resmi koşuda m ≥ 2, yani denetim en gevşek durumdur).
"""

import dataclasses
import datetime as dt
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from tansu import aileler, ciftbolme, istatistik, kayit, motor, rapor, simulator, veri

DOCS = Path("docs")  # testte conftest yönlendirir
BASLANGIC = "2012-01-02"  # sentetik takvim; 500 günlük ısınma 2013-11'de biter
BAS = "2013-12-02"  # sentetik dünyada simülasyon başlangıcı (gerçek koşu 2015-12-01)
SEKTOR = 4  # sektör sayısı
ESIK = 0.05  # yanlış kabul üst sınırı (TASARIM 5.12)
TEKRAR = 200  # her tekrarda K1 B (geliştirme sayısı; p tabanı 1/201 Holm m = 2 eşiği 0,025'in altında)
ETKILER = (
    0.05,
    0.10,
)  # her sinyalde kuralın dolum fiyatındaki avantaj (TASARIM: "her sinyalden sonra +%5")
HISSE, GUN = (
    125,
    2000,
)  # 125 hisse, likidite eleğinden sonra gerçek koşudaki gibi 100'lük evren


def dunya(tohum, hisse=40, gun=2000) -> veri.Anlik:
    """Sentetik anlık görüntü: `hisse` sembol, `gun` iş günü, düzeltilmiş = ham fiyat, olay yok, faiz tablosu ve sektörler var.

    Günlük getiri = piyasa payı · β + sektör payı + hisse payı (kalın kuyruklu t(5), ±%7'ye kırpılır: limit ve kilit olmaz).
    Aynı tohum aynı dünya."""
    r = np.random.default_rng(tohum)
    takvim = pd.bdate_range(BASLANGIC, periods=gun)
    t5 = lambda *boyut: r.standard_t(5, boyut) / np.sqrt(5 / 3)  # noqa: E731  # birim varyans
    sektor = np.arange(hisse) % SEKTOR
    getiri = np.clip(
        t5(gun, 1) * 0.008 * r.uniform(0.7, 1.3, hisse)
        + t5(gun, SEKTOR)[:, sektor] * 0.007
        + t5(gun, hisse) * 0.015,
        -0.07,
        0.07,
    )
    kapanis = r.uniform(20, 200, hisse) * np.exp(np.cumsum(getiri, axis=0))
    onceki = np.vstack([kapanis[:1] / np.exp(getiri[:1]), kapanis[:-1]])
    aof = onceki * np.exp(0.5 * getiri + 0.002 * r.standard_normal((gun, hisse)))
    yuksek = np.maximum.reduce([onceki, kapanis, aof]) * (
        1 + 0.003 * r.random((gun, hisse))
    )
    dusuk = np.minimum.reduce([onceki, kapanis, aof]) * (
        1 - 0.003 * r.random((gun, hisse))
    )
    hacim = np.exp(
        r.uniform(16, 20, hisse) + 0.3 * r.standard_normal((gun, hisse))
    )  # TL, ~1e7 – 5e8
    lot = r.uniform(1e8, 1e10, hisse)
    xu = 1000 * np.exp(np.cumsum(getiri.mean(axis=1)))
    adlar = [f"S{i:03d}" for i in range(hisse)]
    f = pd.DataFrame({"tarih": np.tile(takvim, hisse), "sembol": np.repeat(adlar, gun)})
    for ad, m in (
        ("kapanis", kapanis),
        ("aof", aof),
        ("yuksek", yuksek),
        ("dusuk", dusuk),
    ):
        f[ad] = m.T.ravel()
        f["ham_" + ad] = f[ad]
    f["hacim"] = hacim.T.ravel()
    f["pd"] = (kapanis * lot).T.ravel()
    f["hao_pd"], f["sermaye"] = np.nan, np.repeat(lot, gun)
    f["xu100"] = np.tile(xu, hisse)
    faiz = pd.DataFrame(
        {
            "tarih": pd.to_datetime(
                ["2011-06-01", "2013-09-02", "2015-03-02", "2017-06-01", "2018-10-01"]
            ),
            "faiz": [8.0, 10.0, 9.0, 12.0, 15.0],
        }
    )
    bos = pd.DataFrame(
        {
            "sembol": pd.Series(dtype=str),
            "tarih": pd.Series(dtype="datetime64[s]"),
            "kod": pd.Series(dtype=str),
            "carpan": pd.Series(dtype=float),
        }
    )
    return veri.Anlik(
        kimlik=f"sentetik-{tohum}",
        fiyat=f,
        olaylar=bos,
        faiz=faiz,
        sektor={a: f"K{s}" for a, s in zip(adlar, sektor)},
    )


def etki_ekle(anlik, aile, etki=ETKILER[0], bas=BAS) -> veri.Anlik:
    """Kuralın her sinyalinde dolum fiyatına `etki` avantajı gömer (TASARIM 5.12: bilinen etki, pozitif kontrol).

    Sinyaller boş dünyadan hesaplanır (EMA: `aileler.sinyal`; çift: yıllık seçim ve `ciftbolme.hedef`). Sinyali izleyen gün
    (giriş günü) sinyalin hissesinin (çiftte geçilen bacağın) AOF'u `1 + etki`'ye bölünür; kapanış ve sonraki günler aynıdır.
    Böylece kural işlem başına yaklaşık `etki` kazanır, rastgele girişler (K1) kazanmaz: kalıcı fiyat kayması olsaydı
    sinyalden önceki günde giren rastgele işlem de aynı kazancı alırdı ve K1 etkiyi görmezdi."""
    gunler = anlik.gunler
    konum = pd.Series(np.arange(len(gunler)), index=gunler)
    sinyal = {}  # sembol → sinyal günü (kapanış) konumları
    if aile == simulator.AILE:
        for s, f in anlik.fiyat.groupby("sembol"):
            sinyal[s] = konum.reindex(
                aileler.sinyal(f.set_index("tarih")[["kapanis", "yuksek"]])
            ).to_numpy()
    else:
        evr = simulator.evrenler(anlik, simulator.ilk_gun(anlik, bas), gunler[-1])
        h = ciftbolme.hazirla(anlik, evr, bas)
        bitis = [*(st["bas"] for st in h["setler"][1:]), len(gunler) + 1]
        for st, son in zip(h["setler"], bitis):
            for y, x in st["ciftler"]:
                hedef = ciftbolme.hedef(h["Kc"], y, x, h["p"])
                for j in range(st["bas"] - 1, min(son - 1, len(gunler))):
                    if hedef[j]:
                        sinyal.setdefault(y if hedef[j] > 0 else x, []).append(j)
    f = anlik.fiyat
    giris = {
        (s, gunler[j + 1])
        for s, js in sinyal.items()
        for j in js
        if j + 1 < len(gunler)
    }
    sec = pd.MultiIndex.from_arrays([f["sembol"], f["tarih"]]).isin(list(giris))
    yeni = {}
    for on in ("", "ham_"):
        aof = np.where(sec, f[on + "aof"] / (1 + etki), f[on + "aof"])
        yeni[on + "aof"], yeni[on + "dusuk"] = (
            aof,
            np.minimum(f[on + "dusuk"], aof),
        )  # düşük ≤ AOF korunur
    return dataclasses.replace(anlik, fiyat=f.assign(**yeni))


def _holm_iki(ps) -> dict:
    """Holm m = 2 (iki aile), günlüksüz: gerçek koşuda m ≥ 2 olduğundan denetim en gevşek durumdur."""
    return {
        a: {"holm_p": h, "holm_m": len(ps), "varsayimsal": True, "donmus": False}
        for a, h in zip(ps, istatistik.holm(list(ps.values())))
    }


def tekil(tohum, etkili=None, etki=0.0, tekrar=TEKRAR, hisse=HISSE, gun=GUN) -> dict:
    """Bir sentetik dünyada boru hattını koşar; aile → {kagit, olcut_1_4, p, holm_p, genel, islem}.

    `etkili`: etkinin gömüleceği aile (None: boş dünya). `olcut_1_4`: ölçüt 1–4 Geçti ve portföy kuralı reddetmedi
    (örneklem ve sağlamlık şartından bağımsız kabul); `kagit`: ölçüt 1–5'in hepsi, yani aile Kâğıt'a geçer."""
    a = dunya(tohum, hisse, gun)
    if etkili:
        a = etki_ekle(a, etkili, etki)
    h = kayit.hesapla(
        a, aileler.Parametre(), motor.ATR_N, BAS, tekrar, tohum, _holm_iki
    )
    return {
        aile: {
            "kagit": k["durum"] == "Kâğıt",
            "olcut_1_4": not k["ret"]
            and all(r["durum"] == istatistik.GECTI for r in k["satirlar"][:4]),
            "p": h["k1"][aile]["p"],
            "holm_p": k["holm"]["holm_p"],
            "genel": k["genel"],
            "islem": k["satirlar"][4]["ham"][0][1],
        }
        for aile, k in h["kabul"].items()
    }


def _is(arg) -> dict:
    """İşçi girişi: tekrarlar zaten süreçlere bölünür, iç içe süreç havuzu (eşbütünleşme) kapatılır."""
    eski, ciftbolme.POOL_ESIK = ciftbolme.POOL_ESIK, float("inf")
    try:
        return tekil(*arg)
    finally:
        ciftbolme.POOL_ESIK = eski


def _oran(sonuclar, aile, anahtar) -> dict:
    s = [r[aile][anahtar] for r in sonuclar]
    return {
        "n": len(s),
        "adet": int(sum(s)),
        "oran": float(np.mean(s)) if s else float("nan"),
    }


def calistir(
    n=200, tekrar=TEKRAR, etkiler=ETKILER, n_etki=None, isci=None, hisse=HISSE, gun=GUN
) -> dict:
    """Boş dünyada `n` tekrar (yanlış kabul) ve her ailenin her etki düzeyinde etkisi gömülü dünyada `n_etki` tekrar (güç).

    Tohumlar sabittir (boş: 0 … n−1, etkili: 1000 …). Tekrarlar `isci` süreçte koşar (varsayılan işlemci sayısı; 1: tek süreç).
    Geçti: her ailenin yanlış kabul oranı (`olcut_1_4`) ≤ %5. `guc`: aile → etki → {ölçüt, oran}."""
    n_etki = n_etki or max(n // 10, 1)
    isler = [(i, None, 0.0, tekrar, hisse, gun) for i in range(n)]
    gruplar = [(e, aile) for e in etkiler for aile in kayit.AILELER]
    isler += [
        (1000 + i, aile, e, tekrar, hisse, gun)
        for e, aile in gruplar
        for i in range(n_etki)
    ]
    if (isci or os.cpu_count()) > 1:
        with ProcessPoolExecutor(isci) as havuz:
            sonuc = list(havuz.map(_is, isler))
    else:
        sonuc = list(map(_is, isler))
    guc = {aile: {} for aile in kayit.AILELER}
    for k, (e, aile) in enumerate(gruplar):
        guc[aile][e] = {
            a: _oran(sonuc[n + k * n_etki : n + (k + 1) * n_etki], aile, a)
            for a in ("olcut_1_4", "kagit")
        }
    yanlis = {
        aile: {a: _oran(sonuc[:n], aile, a) for a in ("olcut_1_4", "kagit")}
        for aile in kayit.AILELER
    }
    return {
        "n": n,
        "n_etki": n_etki,
        "tekrar": tekrar,
        "etkiler": list(etkiler),
        "hisse": hisse,
        "gun": gun,
        "yanlis_kabul": yanlis,
        "guc": guc,
        "esik": ESIK,
        "gecti": all(y["olcut_1_4"]["oran"] <= ESIK for y in yanlis.values()),
    }


def yaz(sonuc, docs=None, rapor_dizini=None) -> tuple:
    """Sonucu `docs/denetim.md` ve `rapor/denetim-<zaman>.html` dosyalarına yazar; yolları döndürür."""
    oz = lambda d: f"{rapor.yuzde(d['oran'])} ({d['adet']}/{d['n']})"  # noqa: E731
    etkiler = sonuc["etkiler"]
    satirlar = [
        [
            "Aile",
            "Yanlış kabul (ölçüt 1–4)",
            "Yanlış kabul (Kâğıt)",
            *(f"Güç {rapor.yuzde(e)} (ölçüt 1–4 / Kâğıt)" for e in etkiler),
        ]
    ]
    for aile, y in sonuc["yanlis_kabul"].items():
        g = sonuc["guc"][aile]
        satirlar.append(
            [
                rapor.AILE_ADI[aile],
                oz(y["olcut_1_4"]),
                oz(y["kagit"]),
                *(f"{oz(g[e]['olcut_1_4'])} / {oz(g[e]['kagit'])}" for e in etkiler),
            ]
        )
    durum = "GEÇTİ" if sonuc["gecti"] else "KALDI: ilk resmi koşu yapılmaz"
    giris = (
        f"Boş dünya {sonuc['n']} tekrar, etkili dünya (her ailenin kendi etkisi, her etki düzeyi) {sonuc['n_etki']} tekrar; "
        f"her tekrar {sonuc['hisse']} hisse × {sonuc['gun']} gün, K1 B = {sonuc['tekrar']}, Holm m = 2. Gömülü etki: "
        f"sinyal başına dolum avantajı {', '.join(rapor.yuzde(e) for e in etkiler)}. Şart: yanlış kabul ≤ "
        f"{rapor.yuzde(sonuc['esik'])}. Sonuç: **{durum}**."
    )
    md = "\n".join(
        [
            "# Boru hattı denetimi",
            "",
            "Komut: `python -m tansu denetim` (TASARIM 5.12). " + giris,
            "",
            "| " + " | ".join(satirlar[0]) + " |",
            "|" + "---|" * len(satirlar[0]),
            *("| " + " | ".join(s) + " |" for s in satirlar[1:]),
            "",
            "Yanlış kabul: boş dünyada ölçüt 1–4 geçen oran (örneklem ve sağlamlık şartı aranmaz; Kâğıt bunun alt kümesidir). "
            "Güç: etkili dünyada aynı oran.",
            "",
        ]
    )
    yol = Path(docs or DOCS) / "denetim.md"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(md, encoding="utf-8")
    dizin = Path(rapor_dizini or rapor.RAPOR_DIZINI)
    dizin.mkdir(parents=True, exist_ok=True)
    html = dizin / f"denetim-{dt.datetime.now():%Y%m%dT%H%M%S}.html"
    html.write_text(
        '<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><title>TANSU</title></head><body>'
        f"<h1>Boru hattı denetimi</h1><p>{rapor._kac(giris)}</p>{rapor._tablo(satirlar[0], satirlar[1:])}"
        "</body></html>",
        encoding="utf-8",
    )
    return yol, html
