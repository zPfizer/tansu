"""Komut girişi: `python -m tansu sadakat | kayit | sinama | evren-indir [--kok veri] [--kimlik KIMLIK] [--resmi] [--son]` (TASARIM 3)."""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from tansu import evren, kayit, kaynak, sadakat, simulator, veri


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


def _sektor_indir(kok: Path, kimlik: str) -> str:
    """Eksik KAP sektörlerini yavaş ve devam edilebilir okur; hedef evren üyeleridir (TASARIM 4). Yeni kimlik ya da uyarı."""
    anlik = veri.oku(kimlik, kok)
    uye = sorted({s for liste in simulator.evrenler(anlik, simulator.BASLANGIC, anlik.gunler[-1]).values() for s in liste})
    yeni, kapsam = veri.sektor_tamamla(kimlik, kok, kaynak.KapSektor(), uye)
    ozet = f"hedef {kapsam['hedef']}, var {kapsam['var']}, listede yok {len(kapsam['listede_yok'])}, alınamayan {len(kapsam['alinamayan'])}"
    return f"Yeni anlık görüntü {yeni}: {ozet}" if yeni else f"Art arda hata, durdu (yeniden çalıştır): {ozet}"


def _en_yeni(kok: Path) -> str:
    klasorler = sorted(p.name for p in (kok / "ag").glob("2*"))
    if not klasorler:
        raise veri.VeriHatasi("anlık görüntü yok: önce veriyi indir")
    return klasorler[-1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="tansu")
    ap.add_argument("komut", choices=["sadakat", "kayit", "sinama", "evren-indir", "sektor-indir"])
    ap.add_argument("--kok", default="veri")
    ap.add_argument("--kimlik")
    ap.add_argument("--resmi", action="store_true")
    ap.add_argument("--son", action="store_true", help="tam K1 tekrarı: max(1.000, 200·m); yoksa geliştirme (200)")
    a = ap.parse_args(argv)
    kok = Path(a.kok)
    try:
        if a.komut == "evren-indir":
            print(_evren_indir(kok))
        elif a.komut == "sektor-indir":
            print(_sektor_indir(kok, a.kimlik or _en_yeni(kok)))
        elif a.komut == "kayit":
            print("Kural kaydı yazıldı:", kayit.kayitla()["kural_id"])
        elif a.komut == "sinama":
            s = kayit.kosu(a.kimlik or _en_yeni(kok), kok, resmi=a.resmi, tekrar=kayit.tekrar_sayisi(a.son), son=a.son)
            print(f"Koşu {s['kosu_id']}: {len(s['islemler'])} işlem, {s['dusen']} düşen sinyal, özet {s['ozet'][:12]}")
            for aile, k in s["kabul"].items():
                print(f"K1 {aile}: p {k['k1']['p']:.4f} (B {k['k1']['tekrar']}), Holm p {k['holm']['holm_p']:.4f} "
                      f"(m {k['holm']['holm_m']}{', varsayımsal' if k['holm']['varsayimsal'] else ''}), "
                      f"sonuç {k['genel']}, durum {k['durum']}")
            b = s["sim"]["bilgi"]
            print("Veri kapıları (evren üyeleri):", "; ".join(b["sorunlar"]) or "temiz",
                  f"| kapanma (−%100): {b['kapanma']} | rapor: {s['rapor']}")
            c = s["cift"]
            print(f"Çift bölmesi: {len(c['secim'])} çift seçildi, {c['bilgi']['gecis']} tutuş dönemi, işlem yok yılları: {c['islem_yok'] or 'yok'}")
        else:
            kimlik = a.kimlik or _kimlik_bul(kok)
            print(sadakat.calistir(kimlik, kok, Path("docs") / "sadakat.md", kayit.KAYIT_DIZINI / "deneme.jsonl"))
    except (kayit.KayitHatasi, veri.VeriHatasi) as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
