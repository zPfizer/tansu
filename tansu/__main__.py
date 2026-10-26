"""Komut girişi: `python -m tansu <komut>` (docs/SPEC.md bölüm 7)."""

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path

from tansu import kaynak, veri

VERI_KOKU = Path("veri")
VERI_BASLANGIC = dt.date(2019, 1, 1)  # 2019-2020 yalnız ısınma (SPEC 3.4)
ALTIN_SEMBOLLER = ("SOKE",)  # BIST 30 dışı, yalnız altın testler için (SPEC 10)
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
    semboller = sorted({*veri.uyelik_araliklari()["sembol"], *ALTIN_SEMBOLLER})
    try:
        kimlik = veri.indir(semboller, a.kok, kaynak.IsYatirim(), bas=VERI_BASLANGIC)
    except (veri.VeriHatasi, kaynak.KaynakHatasi) as hata:
        print(f"tansu veri: {hata}", file=sys.stderr)
        return 1
    silinen = goruntuleri_buda(a.kok)
    anlik = veri.oku(kimlik, a.kok)
    son_seans = anlik.gunler[-1]
    print(f"anlık görüntü {kimlik}; silinen eski görüntü: {len(silinen)}")
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
    p.set_defaults(calistir=_henuz_yok)

    p = alt.add_parser("ayarla", help="2021-2025 üzerinde parametre ayarla")
    p.add_argument("ad")
    p.set_defaults(calistir=_henuz_yok)

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
