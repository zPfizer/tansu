"""Günlük koşu: indir, kapılardan geçir, kartları ve `durum.txt`'yi yaz (TASARIM 6)."""

import csv
import datetime as dt
import json
import math
import os
import shutil
from pathlib import Path

import pandas as pd

from tansu import aileler, ciftbolme, evren, kayit, kaynak as kaynak_modulu, motor, rapor, simulator, veri

ERKEN = dt.time(18, 15)  # TASARIM 6.2: bundan önce çubuk yarım olabilir
SAKLA_GUN = 30  # TASARIM 6.2: günlük anlık görüntü ömrü
KAGIT_AY = 6  # TASARIM 5.8: en az kâğıt dönem
BASARILI = ("TAMAM", "BUGÜN ÇUBUK YOK")
KARTLI = ("Kâğıt", "Canlı")
SUTUNLAR = ["Tarih", "Hisse", "Aile", "Durum", "Referans", "Stop", "Pozisyon %", "Adet", "Fiili risk",
            "Likidite sınırı TL", "Kanıt", "Kaynak"]
AILE_ADI = {simulator.AILE: "EMA sıkışması"}


def _sayi(x) -> str:
    return f"{x:.2f}".replace(".", ",")


def _isaretli(x) -> str:
    return ("+" if x >= 0 else "−") + rapor.yuzde(abs(x))


def _kanit(aile, tarih) -> str:
    """Ailenin kanıt satırı: son resmi `durum` satırındaki `kanit` alanından (TASARIM 6.5)."""
    satirlar = [s for s in kayit._oku() if s["olay"] == "durum" and s["aile"] == aile and s["resmi"]]
    bas = satirlar[-1]
    for s in reversed(satirlar):
        if s["durum"] not in KARTLI:
            break
        bas = s
    ay = (tarih.date() - dt.date.fromisoformat(bas["tarih"][:10])).days // 30
    k = satirlar[-1].get("kanit")
    if not k or None in (k["fazla"], *k["ci"]):
        return f"{satirlar[-1]['durum']} · kanıt kaydı yok · kâğıt dönem {ay}/{KAGIT_AY} ay"
    alt, ust = k["ci"]
    aralik = "sıfırı içeriyor: ayırt edilemiyor" if alt <= 0 <= ust else f"{_isaretli(alt)} ile {_isaretli(ust)}"
    return (f"{satirlar[-1]['durum']} · {k['islem']} işlem · rastgele kurala göre işlem başına fazla getiri "
            f"{_isaretli(k['fazla'])} (%0,3 masraf) · portföy fazla getirisi (K2'ye göre, yıllık, blok bootstrap "
            f"%95 aralık {aralik}) · kâğıt dönem {ay}/{KAGIT_AY} ay")


def _son(m, sinyaller) -> tuple:
    """`motor.islemler` ile aynı döngü (aynı Adım); (kapanmamış pozisyon, son çubukta kapanan pozisyon)."""
    sinyaller, p, kapanan, son_karantina = set(sinyaller), None, None, None
    for i, (tarih, satir) in enumerate(zip(m.index, m.to_dict("records"))):
        satir["tarih"], kapanan = tarih, None
        if p is not None:
            p = motor.adim(p, satir)
            if p.durum == "kapali":
                kapanan, p = p, None
        if satir["karantina"]:
            son_karantina = i
        engelli = son_karantina is not None and i - son_karantina < motor.KARANTINA_GUN
        if p is None and tarih in sinyaller and not engelli:
            p = motor.bekleyen(satir["atr"], tarih)
    return p, kapanan


def _durum(p) -> str:
    """AKTİF: bekleyen giriş ya da açık pozisyon. STOP: stop değdi. BOZULDU: SMA250 altı, karantina ya da iptal."""
    if p.durum == "kapali":
        return "STOP" if p.neden == "stop" else "BOZULDU"
    return {"stop": "STOP", "sma250": "BOZULDU"}.get(p.bekleyen, "AKTİF")


def _kart(anlik, s, m, p, tarih, atr_n, kanit) -> list:
    f = anlik.fiyat[anlik.fiyat["sembol"] == s].set_index("tarih")
    sinyal = p.sinyal_tarih
    ref, oran = f.at[sinyal, "ham_kapanis"], f.at[sinyal, "ham_kapanis"] / f.at[sinyal, "kapanis"]
    atr = p.atr * oran
    stop = p.stop * oran if p.stop is not None else ref - motor.STOP_ATR * atr
    lq = f["hacim"].reindex(m.index).fillna(0).rolling(simulator.LIKIDITE_GUN, min_periods=1).median().at[sinyal]
    ozk = simulator.SERMAYE
    adet = int(math.floor(min(simulator.RISK * ozk / (motor.STOP_ATR * atr), simulator.TAVAN * ozk / ref,
                              simulator.LIKIDITE * lq / ref)))
    return [sinyal.date().isoformat(), s, AILE_ADI[simulator.AILE], _durum(p), _sayi(ref),
            _sayi(stop) + (" (tahmini)" if p.stop is None else ""), rapor.yuzde(adet * ref / ozk), adet,
            rapor.yuzde(adet * max(0.0, ref - stop) / ozk), f"{simulator.LIKIDITE * lq:.0f}", kanit,
            f"İş Yatırım {anlik.kimlik}"]


def _kartlar(anlik, tarih, p, atr_n) -> list:
    """Kâğıt ve Canlı ailelerin kartları; her gün sinyal gününden itibaren Adım ile yeniden hesaplanır (TASARIM 6.6)."""
    if ciftbolme.AILE in {a for a in kayit.AILELER if kayit.durum_oku(a) in KARTLI}:
        raise kayit.KayitHatasi("çift ailesi Kâğıt: çift kartı henüz yazılmadı")
    if kayit.durum_oku(simulator.AILE) not in KARTLI:
        return []
    kanit, kartlar = _kanit(simulator.AILE, tarih), []
    for s in sorted(anlik.fiyat["sembol"].unique()):
        m = motor.mumlar(anlik, s, p, atr_n)
        poz, kapanan = _son(m, aileler.sinyal(m.dropna(subset=["kapanis"]), p))
        kartlar += [_kart(anlik, s, m, x, tarih, atr_n, kanit) for x in (poz, kapanan) if x is not None]
    return kartlar


def _yaz(yol: Path, yaz_fn) -> None:
    """Geçici dosyaya yazıp `os.replace` ile taşır (TASARIM 6.7)."""
    gecici = yol.with_name(yol.name + ".gecici")
    yol.parent.mkdir(parents=True, exist_ok=True)
    with gecici.open("w", encoding="utf-8-sig" if yol.suffix == ".csv" else "utf-8", newline="") as f:
        yaz_fn(f)
    try:
        os.replace(gecici, yol)
    except PermissionError:
        gecici.unlink(missing_ok=True)
        raise


def _kart_gunlugu(tarih, kimlik, kartlar) -> None:
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    yol.parent.mkdir(parents=True, exist_ok=True)
    gun = tarih.date().isoformat()
    if yol.exists() and any(json.loads(s)["tarih"] == gun for s in yol.read_text(encoding="utf-8").splitlines() if s):
        return
    with yol.open("a", encoding="utf-8") as f:  # yalnız ekleme
        f.write(json.dumps({"tarih": gun, "anlik": kimlik, "kartlar": [dict(zip(SUTUNLAR, k)) for k in kartlar]},
                           ensure_ascii=False, sort_keys=True) + "\n")


def _acik_hisseler() -> set:
    """Dünkü açık kartların hisseleri: evrenden çıksalar da pozisyon açık kalır (TASARIM 5.2)."""
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    if not yol.exists():
        return set()
    satirlar = [s for s in yol.read_text(encoding="utf-8").splitlines() if s]
    return {k["Hisse"] for k in json.loads(satirlar[-1])["kartlar"] if k["Durum"] == "AKTİF"} if satirlar else set()


def _semboller(kok: Path, tarih) -> list:
    """Bugünkü evren (en çok sembollü son tam anlık görüntüden) ve açık kartların hisseleri (TASARIM 6.2)."""
    klasorler = sorted((kok / "ag").glob("2*"))
    if not klasorler:
        raise veri.VeriHatasi("evren için tam anlık görüntü yok: önce `python -m tansu evren-indir` çalıştır")
    taban = veri.oku(klasorler[-1].name, kok)
    ay = min(tarih, taban.gunler[-1])  # taban eskiyse tabanın son ayının evreni (YORUM)
    return sorted(set(evren.evren(taban, ay)) | _acik_hisseler())


def _temizle(kok: Path, simdi) -> None:
    """30 günden eski günlük anlık görüntüler silinir; deneme günlüğünde adı geçenler silinmez (TASARIM 6.2)."""
    ag = kok / "gunluk" / "ag"
    if not ag.exists():
        return
    yol = kayit.KAYIT_DIZINI / "deneme.jsonl"
    metin = yol.read_text(encoding="utf-8") if yol.exists() else ""
    for d in ag.iterdir():
        if d.name.startswith("_gecici"):
            shutil.rmtree(d, ignore_errors=True)
        elif d.name[:8].isdigit():
            yas = (simdi.date() - dt.datetime.strptime(d.name[:8], "%Y%m%d").date()).days
            if yas > SAKLA_GUN and d.name not in metin:
                shutil.rmtree(d, ignore_errors=True)


def _kapi_sorunlari(anlik, son) -> list:
    """Veri kapıları evren üyesi hisse-günlerde (TASARIM 5.13). Geçmişteki kaynak günleri eksik gün olarak zaten
    işlenir; yalnız bugünün kaynak günü hatası kartı durdurur."""
    f = anlik.fiyat
    uye = f.loc[f["tarih"] >= pd.Timestamp(simulator.BASLANGIC), ["sembol", "tarih"]]
    bugun = f"kaynak günü hatası: {son.date()}"
    return [x for x in anlik.sorunlar_uye(uye) if not x.startswith("kaynak günü hatası") or x == bugun]


def gunluk(tarih, kok="veri", simdi=None, kaynak=None, semboller=None, p=aileler.Parametre(),
           atr_n=motor.ATR_N) -> int:
    """Günlük koşu; çıkış kodu: TAMAM ve BUGÜN ÇUBUK YOK 0, SORUNLU ve VERİ YOK 1. `kaynak`, `semboller`, `p` testte verilir."""
    tarih, kok = pd.Timestamp(tarih), Path(kok)
    simdi = simdi or dt.datetime.now(veri.ISTANBUL)
    yol = rapor.RAPOR_DIZINI / "durum.txt"
    onceki = yol.read_text(encoding="utf-8").splitlines() if yol.exists() else []
    saat = next((x.split(": ", 1)[1] for x in onceki if x.startswith("Son başarılı koşu: ")), "yok")
    if onceki[:1] and onceki[0] in BASARILI and saat[:10] == tarih.date().isoformat():
        print("Bugünün başarılı koşusu var; bir şey yapılmadı.")
        return 0

    def bitir(durum, eylem, kimlik="yok", son="yok", sayi="yok") -> int:
        basarili = durum in BASARILI
        satirlar = [durum, f"Son başarılı koşu: {simdi:%Y-%m-%d %H:%M}" if basarili else f"Son başarılı koşu: {saat}",
                    f"Anlık görüntü: {kimlik}", f"Son çubuk: {son}", f"Sembol sayısı: {sayi}", f"Eylem: {eylem}"]
        _yaz(yol, lambda f: f.write("\n".join(satirlar) + "\n"))
        print(durum, "-", eylem)
        return 0 if basarili else 1

    kimlik = son = sayi = "yok"
    try:
        if simdi.date() == tarih.date() and simdi.time() < ERKEN:
            return bitir("VERİ YOK", "Koşu 18:15'ten önce başladı, kart üretilmedi (çubuk yarım olabilir). 18:15'ten sonra yeniden çalıştır.")
        _temizle(kok, simdi)
        semboller = semboller or _semboller(kok, tarih)
        kimlik = veri.indir(semboller, kok / "gunluk", kaynak or kaynak_modulu.IsYatirim(), simdi=simdi)
        anlik = veri.oku(kimlik, kok / "gunluk")
        son, sayi = anlik.gunler[-1], anlik.fiyat["sembol"].nunique()
        bilgi = dict(kimlik=kimlik, son=son.date().isoformat(), sayi=sayi)
        if son.date() != tarih.date():
            return bitir("BUGÜN ÇUBUK YOK", "Bugün işlem günü değil ya da çubuk yok; bir şey yapma.", **bilgi)
        sorunlar = _kapi_sorunlari(anlik, son)
        if sorunlar:
            return bitir("SORUNLU", "Kart üretilmedi: veri kapısı başarısız (" + "; ".join(sorunlar) + "). Kartlara güvenme.", **bilgi)
        kartlar = _kartlar(anlik, tarih, p, atr_n)
        csv_yol = rapor.RAPOR_DIZINI / f"kartlar-{tarih:%Y%m%d}.csv"

        def yaz_csv(f):
            w = csv.writer(f, delimiter=";")
            w.writerow(SUTUNLAR)
            w.writerows(kartlar)

        try:
            _yaz(csv_yol, yaz_csv)
        except PermissionError:
            return bitir("SORUNLU", f"Kart yazılamadı: {csv_yol.name} açık, kapatıp yeniden çalıştır.", **bilgi)
        _kart_gunlugu(tarih, kimlik, kartlar)
        return bitir("TAMAM", f"Bugün {len(kartlar)} kart var: rapor/{csv_yol.name} dosyasını aç." if kartlar
                     else "Bugün kart yok; bir şey yapma.", **bilgi)
    except veri.KaynakYok:
        return bitir("VERİ YOK", "Kaynağa ulaşılamadı, kart üretilmedi. Saat başı yeniden denenir.")
    except Exception as hata:  # noqa: BLE001 — her hata SORUNLU yazılır, çıkış kodu 1
        return bitir("SORUNLU", f"Kart üretilmedi: {hata}. Hatayı oku ve yeniden çalıştır.", kimlik, str(son)[:10] if son != "yok" else son, sayi)
