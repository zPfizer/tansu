"""Sadakat kontrolü: Tansu'nun kendi çıktı rakamlarını ham seriden yeniden üretir (KURALLAR §4). Getiriye bakılmaz."""

import datetime as dt
import json
from pathlib import Path

import pandas as pd

from tansu import gostergeler, veri

# Tansu'nun KRDMD ekranı (docs/kurallar/B-momentum-sikisma.md §1). Tolerans: gösterilen son hanenin yarısı.
SEMBOL = "KRDMD"
RAPOR_TARIHI = pd.Timestamp("2026-04-09")
PENCERE = 130  # "Son 130 Mum"
DONEM = (pd.Timestamp("2025-12-17"), pd.Timestamp("2026-01-14"))
DONEM_GUN = 20
ORTALAMA_YUZDE = 0.64
EMALAR = (31.92, 30.74, 29.58, 28.43)
TOLERANS = 0.005
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
    return "\n".join(satirlar)


def calistir(kimlik, kok, rapor_yolu, gunluk_yolu) -> str:
    anlik = veri.oku(kimlik, kok)
    metin = rapor_metni(anlik)
    Path(rapor_yolu).write_text(metin, encoding="utf-8")
    gunluk = Path(gunluk_yolu)
    gunluk.parent.mkdir(parents=True, exist_ok=True)
    satir = {"tur": "sadakat", "tarih": dt.datetime.now(dt.timezone.utc).isoformat(), "anlik": kimlik,
             "aile": "ema_sikismasi"}
    with gunluk.open("a", encoding="utf-8") as f:  # yalnız ekleme; Holm yalnız tur=deneme sayar
        f.write(json.dumps(satir, ensure_ascii=False) + "\n")
    return metin
