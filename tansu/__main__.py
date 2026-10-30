"""Komut girişi: `python -m tansu <komut>` (docs/SPEC.md bölüm 7)."""

import argparse
import datetime as dt
import shutil
import sys
import webbrowser
from pathlib import Path

import pandas as pd

from tansu import ayar, durum, kaynak, rapor, sinama, veri
from tansu.stratejiler import STRATEJILER

VERI_KOKU = Path("veri")
VERI_BASLANGIC = dt.date(2019, 1, 1)  # 2019-2020 yalnız ısınma (SPEC 3.4)
SAKLANAN_GORUNTU = 10


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


def _yazilanlar(yol, json_yolu) -> str:
    yazilan = [str(p) for p in (yol and yol.parent, json_yolu) if p]
    return f" Bu koşunun yeni yazdıkları: {', '.join(yazilan)}." if yazilan else ""


def _kos(a, *, ayarla: bool) -> int:
    """`sina` ve `ayarla` için tek akış; farkları json yazımı ve durum geçişi (SPEC 4, 5.7)."""
    komut: durum.Komut = "ayarla" if ayarla else "sina"
    strateji = STRATEJILER.get(a.ad)
    if strateji is None:
        print(f"tansu {komut}: bilinmeyen strateji {a.ad}", file=sys.stderr)
        return 2
    yol = json_yolu = None
    try:
        satirlar = durum.oku()
        onceki = durum.durumu(satirlar, a.ad)
        if durum.reddeder(komut, onceki):
            print(
                f"tansu {komut}: {a.ad} {onceki}; önce taslak olmalı", file=sys.stderr
            )
            return 1
        okunan = None if ayarla else ayar.oku(strateji)
        anlik = son_anlik(a.kok)
        s = rapor.hazirla(
            strateji,
            sinama.gunler(anlik),
            kimlik=anlik.kimlik,
            sinanan=durum.sinanan(satirlar, a.ad),
            ayarla=ayarla,
            okunan=okunan,
        )
        yol = rapor.yaz(s)
        if ayarla:  # json rapordan sonra: yarıda kalan koşu onaysız parametre bırakmaz
            json_yolu = ayar.yaz(strateji, s.yuruyus.son, veri_kimligi=s.kimlik)
        yeni_durum = durum.gec(a.ad, komut, puanli=s.yuruyus.son.puanli)
    except veri.VeriHatasi as hata:
        print(f"tansu {komut}: {hata}{_yazilanlar(yol, json_yolu)}", file=sys.stderr)
        return 1
    except PermissionError as hata:
        hedef = hata.filename2 or hata.filename or hata
        print(
            f"tansu {komut}: {hedef} için erişim engellendi; dosya başka bir programda açıksa kapatıp yeniden çalıştır. durum.csv değişmedi.{_yazilanlar(yol, json_yolu)}",
            file=sys.stderr,
        )
        return 1
    for satir in rapor.konsol(s):
        print(satir)
    if json_yolu:
        print(f"ayar: {json_yolu}")
    print(f"rapor: {yol}; durum: {yeni_durum}")
    if durum.yeniden_onay(komut, onceki):
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
