"""Komut girişi: `python -m tansu <komut>` (docs/SPEC.md bölüm 7)."""

import argparse
import csv
import datetime as dt
import shutil
import sys
import webbrowser
from collections.abc import Collection
from pathlib import Path

import numpy as np
import pandas as pd

from tansu import ayar, kaynak, rapor, sinama, veri
from tansu.stratejiler import STRATEJILER

VERI_KOKU = Path("veri")
VERI_BASLANGIC = dt.date(2019, 1, 1)  # 2019-2020 yalnız ısınma (SPEC 3.4)
SAKLANAN_GORUNTU = 10
DURUM_DOSYASI = Path("stratejiler/durum.csv")
DURUMLAR = (
    "taslak",
    "beklemede",
    "sinandi",
    "ayarlandi",
    "yetersiz-ornek",
    "sinyalde",
)


def son_anlik(kok: Path = VERI_KOKU) -> veri.Anlik:
    klasorler = sorted(p.name for p in (kok / "ag").glob("2*"))
    if not klasorler:
        raise veri.VeriHatasi("anlık görüntü yok: önce `tansu veri` çalıştır")
    return veri.oku(klasorler[-1], kok)


def goruntuleri_buda(kok: Path, saklanan: int = SAKLANAN_GORUNTU) -> list[str]:
    eskiler = sorted((kok / "ag").glob("2*"))[:-saklanan]
    for klasor in eskiler:
        shutil.rmtree(klasor)
    return [p.name for p in eskiler]


def _veri(a) -> int:
    try:
        # Evren bütün BIST: bugünkü KAP listesi ve veri başlangıcından beri kapanan kodlar (SPEC 2, 3.4)
        kapanan = kaynak.kapanan_kodlar()
        kapanan = kapanan[~(kapanan["tarih"] < pd.Timestamp(VERI_BASLANGIC))]
        semboller = sorted(
            {*kaynak.sirket_kodlari().astype(str).str.strip(), *kapanan["kod"]}
        )
        k = kaynak.Artimli(
            kaynak.IsYatirim(), a.kok / "onbellek" / f"fiyat-{VERI_BASLANGIC:%Y%m%d}"
        )
        kimlik = veri.indir(semboller, a.kok, k, bas=VERI_BASLANGIC, kapanan=kapanan)
    except (veri.VeriHatasi, kaynak.KaynakHatasi) as hata:
        print(f"tansu veri: {hata}", file=sys.stderr)
        return 1
    silinen = goruntuleri_buda(a.kok)
    anlik = veri.oku(kimlik, a.kok)
    son_seans = anlik.gunler[-1]
    print(
        f"anlık görüntü {kimlik}; silinen eski görüntü: {len(silinen)}; "
        f"önbellek: {k.sayac['artimli']} artımlı, {k.sayac['tam']} tam"
    )
    print("sembol  ilk_tarih   son_tarih   satir  durum")
    tarihler = anlik.fiyat.groupby("sembol")["tarih"].agg(["min", "max", "size"])
    for s in semboller:
        if s in tarihler.index:
            ilk, son, n = tarihler.loc[s]
            durum = "tamam" if son >= son_seans else "son gün eksik"
            print(f"{s:<7} {ilk.date()}  {son.date()}  {n:>5}  {durum}")
        else:
            durum = "inmedi" if s in anlik.inmeyen else "kaynak boş"
            print(f"{s:<7} {'-':<10}  {'-':<10}  {0:>5}  {durum}")
    return 0


def _durum_satirlari(yol: Path = DURUM_DOSYASI) -> list[dict]:
    with yol.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _satir(satirlar: list[dict], ad: str) -> dict:
    satir = next((r for r in satirlar if r["ad"] == ad), None)
    if satir is None:
        raise veri.VeriHatasi(f"{ad}: durum.csv içinde yok")
    return satir


def durum_gecisi(
    ad: str, eski: Collection[str], yeni: str, yol: Path = DURUM_DOSYASI
) -> str:
    """`durum.csv` satırını durumu `eski` içindeyse `yeni` yapar; son durumu döndürür (SPEC 4)."""
    satirlar = _durum_satirlari(yol)
    satir = _satir(satirlar, ad)
    if satir["durum"] in eski:
        satir.update(durum=yeni, tarih=dt.date.today().isoformat())
        with yol.open("w", encoding="utf-8", newline="") as f:
            yazici = csv.DictWriter(
                f, ["ad", "durum", "tarih", "not"], lineterminator="\n"
            )
            yazici.writeheader()
            yazici.writerows(satirlar)
    return satir["durum"]


def _kos(a, *, ayarla: bool) -> int:
    """`sina` ve `ayarla` için tek akış; farkları json yazımı ve durum geçişi (SPEC 4, 5.7)."""
    komut = "ayarla" if ayarla else "sina"
    strateji = STRATEJILER.get(a.ad)
    if strateji is None:
        print(f"tansu {komut}: bilinmeyen strateji {a.ad}", file=sys.stderr)
        return 2
    try:
        satirlar = _durum_satirlari()
        onceki = _satir(satirlar, a.ad)["durum"]
        if ayarla and onceki == "beklemede":
            print(
                f"tansu ayarla: {a.ad} beklemede; önce taslak olmalı", file=sys.stderr
            )
            return 1
        okunan = None if ayarla else ayar.oku(strateji)
        anlik = son_anlik(a.kok)
        s = rapor.hazirla(
            strateji,
            sinama.gunler(anlik),
            kimlik=anlik.kimlik,
            sinanan=sum(
                r["durum"] not in ("taslak", "beklemede") or r["ad"] == a.ad
                for r in satirlar
            ),
            ayarla=ayarla,
            okunan=okunan,
        )
        yol = rapor.yaz(s)
        json_yolu = None
        if ayarla:  # json rapordan sonra: yarıda kalan koşu onaysız parametre bırakmaz
            json_yolu = ayar.yaz(strateji, s.yuruyus.son, veri_kimligi=s.kimlik)
            yeni = "ayarlandi" if s.yuruyus.son.puanli else "yetersiz-ornek"
            durum = durum_gecisi(a.ad, set(DURUMLAR) - {"beklemede"}, yeni)
        else:
            durum = durum_gecisi(a.ad, {"taslak"}, "sinandi")
    except veri.VeriHatasi as hata:
        print(f"tansu {komut}: {hata}", file=sys.stderr)
        return 1
    gecmis, yuruyus, sakli, sakli_son, mc = (
        s.gecmis,
        s.yuruyus,
        s.sakli,
        s.sakli_son,
        s.mc,
    )
    olcu = strateji.olcu
    b = sinama.BIRIM[olcu]
    son, iz = yuruyus.son, yuruyus.izgara
    toplam = gecmis.toplam
    secim = (
        f"seçim {' '.join(f'{k}={v}' for k, v in iz.eksenler(son.nokta).items())} "
        f"(sağlam {son.saglam[son.nokta]:.2f} {b}, N = {son.n[son.nokta]})"
        if son.puanli
        else "puanlı nokta yok, varsayılanlar"
    )
    verim = "n/a" if yuruyus.verim is None else f"{yuruyus.verim:.2f}"
    print(
        f"{a.ad}: {len(gecmis.sinyaller)} sinyal, {len(gecmis.islemler)} dolum, "
        f"toplam {toplam:.2f} {b}"
    )
    print(
        f"{a.ad}: ızgara {len(iz)} nokta, puanlı {int(np.isfinite(son.puan).sum())}; {secim}"
    )
    print(
        f"ileri yürüme: örneklem dışı N = {len(yuruyus.dis_ornek.islemler)}, "
        f"ortalama verim {verim} ({yuruyus.verim_adim}/{len(yuruyus.adimlar)} adım)"
    )
    print(
        f"saklı dönem {sinama.SAKLI_BAS:%d.%m.%Y}-{sakli_son:%d.%m.%Y}: N = {len(sakli.islemler)}"
        if sakli_son >= sinama.SAKLI_BAS
        else "saklı dönem: veri saklı döneme ulaşmıyor"
    )
    rastgele = (
        f"n/a (N = {mc.n})" if mc.rastgele is None else f"{mc.rastgele.yuzdelik:.1f}"
    )
    print(
        f"Monte Carlo: tohum {mc.tohum}, N = {mc.n}, rastgele giriş yüzdeliği {rastgele}"
    )
    if json_yolu:
        print(f"ayar: {json_yolu}")
    print(f"rapor: {yol}; durum: {durum}")
    if ayarla and onceki == "sinyalde":
        print(f"Levent yeniden onaylamalı: tansu onayla {a.ad}")
    if a.ac:
        webbrowser.open(yol.resolve().as_uri())
    return 0


def _sina(a) -> int:
    return _kos(a, ayarla=False)


def _ayarla(a) -> int:
    return _kos(a, ayarla=True)


def _henuz_yok(a) -> int:
    print(f"tansu {a.komut}: henüz yapılmadı (docs/SPEC.md bölüm 12).", file=sys.stderr)
    return 2


def ayristirici() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="tansu",
        description="Tansu stratejilerinin giriş, stop ve hedef seviyeleri. Alım-satım talimatı vermez.",
    )
    alt = ap.add_subparsers(dest="komut", required=True, metavar="komut")

    p = alt.add_parser("veri", help="veriyi indir veya güncelle")
    p.add_argument("--kok", type=Path, default=VERI_KOKU, help=argparse.SUPPRESS)
    p.set_defaults(calistir=_veri)

    p = alt.add_parser("sina", help="stratejiyi geçmiş veride sına, rapor yaz")
    p.add_argument("ad")
    p.add_argument("--ac", action="store_true", help="raporu tarayıcıda aç")
    p.add_argument("--kok", type=Path, default=VERI_KOKU, help=argparse.SUPPRESS)
    p.set_defaults(calistir=_sina)

    p = alt.add_parser("ayarla", help="2021-2025 üzerinde parametre ayarla")
    p.add_argument("ad")
    p.add_argument("--kok", type=Path, default=VERI_KOKU, help=argparse.SUPPRESS)
    p.set_defaults(calistir=_ayarla, ac=False)

    p = alt.add_parser("onayla", help="stratejiyi akşam sinyaline al (yalnız Levent)")
    p.add_argument("ad")
    p.add_argument("--suzgec", action="append", default=[])
    p.add_argument("--liste-cikisi", action="store_true")
    p.set_defaults(calistir=_henuz_yok)

    p = alt.add_parser("tara", help="akşam taraması ve seviye listesi")
    p.add_argument("--oturum", help="YYYY-AA-GG")
    p.add_argument("--gonderme", action="store_true", help="Telegram'a gönderme")
    p.add_argument("--bekleme-yok", action="store_true", help="veri için bekleme")
    p.set_defaults(calistir=_henuz_yok)

    p = alt.add_parser("durum", help="stratejilerin sınıfı ve durumu")
    p.set_defaults(calistir=_henuz_yok)
    return ap


def main(argv=None) -> int:
    a = ayristirici().parse_args(argv)
    return a.calistir(a)


if __name__ == "__main__":
    sys.exit(main())
