"""Sadakat kontrolü: Tansu'nun kendi çıktı rakamlarını ham seriden yeniden üretir (KURALLAR §4). Getiriye bakılmaz."""

import datetime as dt
import json
from pathlib import Path

import numpy as np
import pandas as pd

from tansu import cift, gostergeler, veri

# Tansu'nun KRDMD ekranı (docs/kurallar/B-momentum-sikisma.md §1). Tolerans: gösterilen son hanenin yarısı.
SEMBOL = "KRDMD"
RAPOR_TARIHI = pd.Timestamp("2026-04-09")
PENCERE = 130  # "Son 130 Mum"
DONEM = (pd.Timestamp("2025-12-17"), pd.Timestamp("2026-01-14"))
DONEM_GUN = 20
ORTALAMA_YUZDE = 0.64
EMALAR = (31.92, 30.74, 29.58, 28.43)
TOLERANS = 0.005
# Çift Z'si (docs/kurallar/D-cift-portfoy-nabiz.md): Y = VAKBN, X = GARAN.
CIFT_Y, CIFT_X = "VAKBN", "GARAN"
CIFT_Z = (-3.108, -3.404)  # (Z_t, Z_{t-1})
CIFT_BETA, CIFT_KORELASYON = 1.675, 0.731
CIFT_TOLERANS = 0.0005  # gösterilen son hanenin yarısı
CIFT_GEVSEK = 0.05  # yalnız tek aday kalırsa
CIFT_PENCERELER = range(10, 401)
CIFT_DDOF = (0, 1)
SEMBOLLER = (SEMBOL, CIFT_Y, CIFT_X)
# Tansu'nun yfinance geçmiş uzunluğu bilinmiyor; EMA200 başlangıca duyarlı. None = bütün geçmiş.
GECMIS_ADAYLARI = (None, 3, 2)


def ema_sikismasi(anlik, sembol=SEMBOL, rapor=RAPOR_TARIHI, gecmis_yil=None) -> dict:
    f = anlik.fiyat[anlik.fiyat["sembol"] == sembol].sort_values("tarih").set_index("tarih")
    kapanis = f["ham_kapanis"].loc[:rapor]
    if gecmis_yil:
        kapanis = kapanis.loc[rapor - pd.DateOffset(years=gecmis_yil):]
    oran = gostergeler.sikisma_orani(kapanis)
    return {"donemler": gostergeler.sikisma_donemleri(oran.iloc[-PENCERE:]),
            "emalar": [float(gostergeler.ema(kapanis, p).iloc[-1]) for p in gostergeler.SIKISMA_PERIYOTLAR]}


def _bolum(anlik, gecmis_yil) -> list:
    s = ema_sikismasi(anlik, gecmis_yil=gecmis_yil)
    ad = "bütün geçmiş" if gecmis_yil is None else f"son {gecmis_yil} yıl"
    satirlar = [f"### Aday: {ad}", "", "| Ölçü | Tansu | Bizim | Sonuç |", "|---|---|---|---|"]
    d = next(iter(s["donemler"]), None)
    if d:
        gun = d["gun"]
        ort = d["ortalama"] * 100
        satirlar += [
            f"| Dönem | {DONEM[0].date()} – {DONEM[1].date()} | {d['bas'].date()} – {d['bit'].date()} | "
            f"{'üretti' if (d['bas'], d['bit']) == DONEM else 'üretmedi'} |",
            f"| Gün | {DONEM_GUN} | {gun} | {'üretti' if gun == DONEM_GUN else 'üretmedi'} |",
            f"| Dönem ortalaması % | {ORTALAMA_YUZDE} | {ort:.3f} | "
            f"{'üretti' if abs(ort - ORTALAMA_YUZDE) <= TOLERANS else 'üretmedi'} |"]
    else:
        satirlar.append("| Dönem | " f"{DONEM[0].date()} – {DONEM[1].date()} | yok | üretmedi |")
    for p, t, b in zip(gostergeler.SIKISMA_PERIYOTLAR, EMALAR, s["emalar"]):
        satirlar.append(f"| EMA{p} ({RAPOR_TARIHI.date()}) | {t} | {b:.4f} | "
                        f"{'üretti' if abs(b - t) <= TOLERANS else 'üretmedi'} |")
    if len(s["donemler"]) > 1:
        satirlar += ["", f"Pencerede {len(s['donemler'])} dönem bulundu; ilki karşılaştırıldı."]
    return satirlar + [""]


def cift_ara(y, x, hedef=CIFT_Z, tolerans=CIFT_TOLERANS, pencereler=CIFT_PENCERELER) -> list:
    """(Z_t, Z_{t-1}) çiftini bütün adaylarda ve bütün günlerde arar: [(mod, pencere, ddof, tarih)]."""
    sonuc = []
    for mod in cift.MODLAR:
        for pencere in pencereler:
            for ddof in CIFT_DDOF:
                z = cift.z_skor(y, x, pencere, ddof, mod)
                tuttu = ((z - hedef[0]).abs() <= tolerans) & ((z.shift() - hedef[1]).abs() <= tolerans)
                sonuc += [(mod, pencere, ddof, g) for g in z.index[tuttu]]
    return sonuc


def _cift_serileri(anlik):
    f = anlik.fiyat.pivot(index="tarih", columns="sembol", values="ham_kapanis")[[CIFT_Y, CIFT_X]].dropna()
    return f[CIFT_Y], f[CIFT_X]


def _ols_z(y, x, pencere, ddof, dun=False):
    """Pencerenin kendi OLS kalıntılarından Z; dun=True ise uyum ve sapma t−1'de biter."""
    ry, rx = y.rolling(pencere), x.rolling(pencere)
    h = ry.cov(x) / rx.var()
    ort_y, ort_x = ry.mean(), rx.mean()
    varyans = ry.var(ddof=ddof) - h * ry.cov(x, ddof=ddof)
    if dun:
        h, ort_y, ort_x, varyans = h.shift(), ort_y.shift(), ort_x.shift(), varyans.shift()
    # Sabit terimli OLS'de pencerenin kalıntı ortalaması sıfırdır.
    kalinti = (y - ort_y) - h * (x - ort_x)
    return kalinti / np.sqrt(varyans.where(varyans > 0))


def _ek_z(y, x, aile, mod, pencere, ddof):
    if aile == "fiyat_ols":
        return _ols_z(y, x, pencere, ddof)
    ly, lx = np.log(y), np.log(x)
    s = ly - lx
    if aile == "sabit_std":
        e = s - s.rolling(pencere).mean()
        return e / e.std(ddof=ddof)
    if mod == "kalinti":
        return _ols_z(ly, lx, pencere, ddof, dun=True)
    ort = s.rolling(pencere).mean().shift()
    sapma = s.rolling(pencere).std(ddof=ddof).shift()
    return (s - ort) / sapma


def ek_aday_ara(y, x, hedef=CIFT_Z, tolerans=CIFT_TOLERANS, pencereler=CIFT_PENCERELER) -> list:
    """Bütün günlerde ek adayları arar: [(aile, mod, pencere, ddof, isaret, tarih)]."""
    sonuc = []
    for aile, mod in [("fiyat_ols", "kalinti"), ("sabit_std", "log_oran")] + [
            ("dun_pencere", m) for m in cift.MODLAR]:
        for pencere in pencereler:
            for ddof in CIFT_DDOF:
                z = _ek_z(y, x, aile, mod, pencere, ddof)
                for isaret in (1, -1):
                    tuttu = ((isaret * z - hedef[0]).abs() <= tolerans) & (
                        (isaret * z.shift() - hedef[1]).abs() <= tolerans)
                    sonuc += [(aile, mod, pencere, ddof, isaret, g) for g in z.index[tuttu]]
    return sonuc


def _cift_bolumu(anlik) -> list:
    y, x = _cift_serileri(anlik)
    giris = [
        f"## Çift Z ({CIFT_Y}–{CIFT_X})", "",
        f"Anlık görüntü: `{anlik.kimlik}`. Ham kapanış, Y = {CIFT_Y}, X = {CIFT_X}, {len(y)} ortak işlem günü "
        f"({y.index[0].date()} – {y.index[-1].date()}). Hedef: Z_t {CIFT_Z[0]}, Z_{{t−1}} {CIFT_Z[1]}.", "",
        "Aday kümesi önceden yazılıdır: spread = log oran ya da β'lı kalıntı "
        "(`log Y − a − b·log X`, pencere içi OLS); pencere 10–400 işlem günü; ddof {0; 1}; ham fiyat. "
        f"Tolerans ±{CIFT_TOLERANS}; gevşek bant ±{CIFT_GEVSEK} yalnız tek aday kalırsa. "
        "Rapor tarihi bilinmediği için çift bütün işlem günlerinde aranır. Getiri hesaplanmaz.", "",
        f"{len(cift.MODLAR) * len(CIFT_PENCERELER) * len(CIFT_DDOF)} aday denendi.", ""]
    sik = cift_ara(y, x)
    if sik:
        satirlar = ["Sıkı toleransta eşleşen (aday, gün):", ""]
        satirlar += [f"- {m}, pencere {p}, ddof {d}: {g.date()}" for m, p, d, g in sik]
        return giris + satirlar + [""]
    gevsek = cift_ara(y, x, tolerans=CIFT_GEVSEK)
    adaylar = sorted({g[:3] for g in gevsek})
    if len(adaylar) == 1:
        m, p, d = adaylar[0]
        gunler = ", ".join(str(g[3].date()) for g in gevsek)
        return giris + [f"Sıkı toleransta eşleşme yok. Gevşek bantta tek aday kaldı: {m}, pencere {p}, ddof {d}; "
                        f"günler: {gunler}.", ""]
    return giris + [f"Sıkı toleransta eşleşme yok. Gevşek bantta {len(adaylar)} aday ({len(gevsek)} gün) "
                    "eşleşti: tek aday kalmadığı için **üretmedi**. Kural YORUM kalır: log oran, 60 gün.", ""]


def _ek_aday_bolumu(anlik) -> list:
    y, x = _cift_serileri(anlik)
    sayi = len(CIFT_PENCERELER) * len(CIFT_DDOF) * 2
    giris = [
        "## Çift Z, ek aday turu (10.10.2026)", "",
        "- `fiyat_ols` (Tansu X403: \"spread = A - hedge_ratio * B\"): fiyat düzeyinde "
        "s_t = Y_t − a − h·X_t; a ve h, t'de biten w günlük OLS'den. "
        "Z_t = (s_t − ortalama(s)) / std(s); istatistikler aynı pencerenin kendi uyumunun kalıntılarından.",
        "- `sabit_std` (Tansu X404: log farkı, hareketli ortalama, \"Sabit standart sapma\"): "
        "d = log Y − log X; e = d − w günlük hareketli ortalama(d); Z_t = e_t / std(e). "
        "Standart sapma bütün mevcut seri için tek sabit sayıdır.",
        "- `dun_pencere` (bugünü dışlayan pencere, bilet 06 notu): `cift.z_skor` ile aynı spread "
        "(log oran veya log fiyatların OLS kalıntısı); ortalama ve standart sapma t−1'de biten w günden. "
        "Kalıntı modunda OLS uyumu da bu pencereden; Z_t = (s_t − ortalama) / std.", "",
        f"Ham kapanış, Y = {CIFT_Y}, X = {CIFT_X}; bütün işlem günleri aranır. "
        f"Hedef: Z_t {CIFT_Z[0]}, Z_{{t−1}} {CIFT_Z[1]}. "
        "Pencere 10–400; ddof {0; 1}; her adayda Z ve −Z. Getiri hesaplanmaz.",
        f"Aday sayıları (iki işaret dahil): fiyat_ols {sayi}, sabit_std {sayi}, "
        f"dun_pencere {len(cift.MODLAR) * sayi}; toplam {(2 + len(cift.MODLAR)) * sayi}. "
        f"Tolerans ±{CIFT_TOLERANS}; gevşek bant ±{CIFT_GEVSEK} yalnız tek aday kalırsa.", ""]
    sik = ek_aday_ara(y, x)
    if sik:
        return giris + ["Sıkı toleransta eşleşen (aday, gün):", ""] + [
            f"- {a}, {m}, pencere {p}, ddof {d}, işaret {i:+d}: {g.date()}"
            for a, m, p, d, i, g in sik] + [""]
    gevsek = ek_aday_ara(y, x, tolerans=CIFT_GEVSEK)
    adaylar = sorted({g[:5] for g in gevsek})
    if len(adaylar) == 1:
        a, m, p, d, i = adaylar[0]
        gunler = ", ".join(str(g[5].date()) for g in gevsek)
        return giris + [f"Sıkı toleransta eşleşme yok. Gevşek bantta tek aday kaldı: {a}, {m}, "
                        f"pencere {p}, ddof {d}, işaret {i:+d}; günler: {gunler}.", ""]
    return giris + [f"Sıkı toleransta eşleşme yok. Gevşek bantta {len(adaylar)} aday ({len(gevsek)} gün) "
                    "eşleşti: tek aday kalmadığı için **üretmedi**.",
                    "Ek tur da üretmedi. Çift Z kalıcı olarak YORUM kalır: log oran, 60 gün.", ""]


def rapor_metni(anlik) -> str:
    satirlar = [
        "# Sadakat kontrolü", "",
        "Getiriye bakılmaz. Komut: `python -m tansu sadakat`. Tolerans önceden yazılıdır: gösterilen son "
        f"hanenin yarısı (±{TOLERANS}); tarih ve gün tam eşleşir.", "",
        f"## EMA sıkışması ({SEMBOL})", "",
        f"Anlık görüntü: `{anlik.kimlik}`. Ham kapanış, EMA20/50/100/200 `ewm(adjust=False)`, oran = "
        f"(en büyük EMA − en küçük EMA) / EMA200, eşik ≤ %1,2, en az 3 gün, son {PENCERE} gün, "
        f"rapor tarihi {RAPOR_TARIHI.date()}.", ""]
    for gecmis in GECMIS_ADAYLARI:
        satirlar += _bolum(anlik, gecmis)
    if {CIFT_Y, CIFT_X} <= set(anlik.fiyat["sembol"]):
        satirlar += _cift_bolumu(anlik)
        satirlar += _ek_aday_bolumu(anlik)
    return "\n".join(satirlar)


def calistir(kimlik, kok, rapor_yolu, gunluk_yolu) -> str:
    anlik = veri.oku(kimlik, kok)
    metin = rapor_metni(anlik)
    Path(rapor_yolu).write_text(metin, encoding="utf-8")
    gunluk = Path(gunluk_yolu)
    gunluk.parent.mkdir(parents=True, exist_ok=True)
    satir = {"olay": "sadakat", "tur": "sadakat", "tarih": dt.datetime.now(dt.timezone.utc).isoformat(), "anlik": kimlik,
             "aile": "ema_sikismasi"}
    with gunluk.open("a", encoding="utf-8") as f:  # yalnız ekleme; Holm yalnız tur=deneme sayar
        f.write(json.dumps(satir, ensure_ascii=False) + "\n")
    return metin
