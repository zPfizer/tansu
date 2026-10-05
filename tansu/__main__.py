"""Komut girişi: `python -m tansu sadakat [--kok veri] [--kimlik KIMLIK]` (TASARIM 3)."""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from tansu import evren, kaynak, sadakat, veri


def _kimlik_bul(kok: Path) -> str:
    """Üç sembolü de içeren en yeni anlık görüntü; yoksa indirir."""
    for klasor in sorted((kok / "ag").glob("2*"), reverse=True):
        manifest = json.loads((klasor / "manifest.json").read_text(encoding="utf-8"))
        if set(sadakat.SEMBOLLER) <= set(manifest["semboller"]):
            return klasor.name
    return veri.indir(list(sadakat.SEMBOLLER), kok, kaynak.IsYatirim())


def _evren_indir(kok: Path) -> str:
    """Bütün bugünkü paylar + işlemi kapanmış kodlar. Saatler sürer; yarıda kalırsa aynı gün yeniden
    çalıştırılınca `onbellek/<gün>` klasöründeki tamamlanan semboller tekrar istenmez."""
    import borsapy
    kapanan = kaynak.kapanan_kodlar()
    semboller = evren.tum_semboller(borsapy.companies()["ticker"], kapanan)
    onbellek = kok / "onbellek" / dt.date.today().strftime("%Y%m%d")
    kimlik = veri.indir(semboller, kok, kaynak.Onbellekli(kaynak.IsYatirim(), onbellek), borsapy=kaynak.Borsapy())
    kapanan.to_csv(kok / "ag" / kimlik / "kapanan.csv", index=False, encoding="utf-8-sig")
    return kimlik


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="tansu")
    ap.add_argument("komut", choices=["sadakat", "evren-indir"])
    ap.add_argument("--kok", default="veri")
    ap.add_argument("--kimlik")
    a = ap.parse_args(argv)
    kok = Path(a.kok)
    if a.komut == "evren-indir":
        print(_evren_indir(kok))
        return 0
    kimlik = a.kimlik or _kimlik_bul(kok)
    print(sadakat.calistir(kimlik, kok, Path("docs") / "sadakat.md", Path("kayit") / "deneme.jsonl"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
