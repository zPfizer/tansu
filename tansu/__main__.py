"""Komut girişi: `python -m tansu sadakat | kayit | sinama [--kok veri] [--kimlik KIMLIK] [--resmi]` (TASARIM 3)."""

import argparse
import json
import sys
from pathlib import Path

from tansu import kayit, kaynak, sadakat, veri


def _kimlik_bul(kok: Path) -> str:
    """Üç sembolü de içeren en yeni anlık görüntü; yoksa indirir."""
    for klasor in sorted((kok / "ag").glob("2*"), reverse=True):
        manifest = json.loads((klasor / "manifest.json").read_text(encoding="utf-8"))
        if set(sadakat.SEMBOLLER) <= set(manifest["semboller"]):
            return klasor.name
    return veri.indir(list(sadakat.SEMBOLLER), kok, kaynak.IsYatirim())


def _en_yeni(kok: Path) -> str:
    klasorler = sorted(p.name for p in (kok / "ag").glob("2*"))
    if not klasorler:
        raise veri.VeriHatasi("anlık görüntü yok: önce veriyi indir")
    return klasorler[-1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="tansu")
    ap.add_argument("komut", choices=["sadakat", "kayit", "sinama"])
    ap.add_argument("--kok", default="veri")
    ap.add_argument("--kimlik")
    ap.add_argument("--resmi", action="store_true")
    a = ap.parse_args(argv)
    kok = Path(a.kok)
    try:
        if a.komut == "kayit":
            print("Kural kaydı yazıldı:", kayit.kayitla()["kural_id"])
        elif a.komut == "sinama":
            s = kayit.kosu(a.kimlik or _en_yeni(kok), kok, resmi=a.resmi)
            print(f"Koşu {s['kosu_id']}: {len(s['islemler'])} işlem, {s['dusen']} düşen sinyal, özet {s['ozet'][:12]}")
        else:
            kimlik = a.kimlik or _kimlik_bul(kok)
            print(sadakat.calistir(kimlik, kok, Path("docs") / "sadakat.md", kayit.KAYIT_DIZINI / "deneme.jsonl"))
    except (kayit.KayitHatasi, veri.VeriHatasi) as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
