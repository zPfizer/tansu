"""Komut girişi: `python -m tansu <komut>` (docs/SPEC.md bölüm 7)."""

import argparse
import sys


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
    p.set_defaults(calistir=_henuz_yok)

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
