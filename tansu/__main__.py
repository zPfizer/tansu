"""Komut girişi: `python -m tansu sadakat | kayit | sinama | tansu-sinama | denetim | evren-indir | sektor-indir | gunluk [tarih] [--kok veri] [--kimlik KIMLIK] [--resmi] [--son] [--isci N] [--hisse N] [--aile AILE] [--sektor-kok veri]` (TASARIM 3, 5.14)."""

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

from tansu import (
    ciftbolme,
    denetim,
    evren,
    gunluk,
    kayit,
    kaynak,
    sadakat,
    simulator,
    tansusinama,
    veri,
)


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
    kapanan = kaynak.kapanan_kodlar()
    semboller = evren.tum_semboller(kaynak.sirket_kodlari(), kapanan)
    onbellek = kok / "onbellek" / dt.date.today().strftime("%Y%m%d")
    kimlik = veri.indir(
        semboller,
        kok,
        kaynak.Onbellekli(kaynak.IsYatirim(), onbellek),
        borsapy=kaynak.Borsapy(),
    )
    kapanan.to_csv(
        kok / "ag" / kimlik / "kapanan.csv", index=False, encoding="utf-8-sig"
    )
    return kimlik


def _sektor_indir(kok: Path, kimlik: str) -> str:
    """Eksik KAP sektörlerini yavaş ve devam edilebilir okur; hedef evren üyeleridir (TASARIM 4). Yeni kimlik ya da uyarı."""
    anlik = veri.oku(kimlik, kok)
    uye = sorted(
        {
            s
            for liste in simulator.evrenler(
                anlik, simulator.BASLANGIC, anlik.gunler[-1]
            ).values()
            for s in liste
        }
    )
    yeni, kapsam = veri.sektor_tamamla(kimlik, kok, kaynak.KapSektor(), uye)
    ozet = f"hedef {kapsam['hedef']}, var {kapsam['var']}, listede yok {len(kapsam['listede_yok'])}, alınamayan {len(kapsam['alinamayan'])}"
    return (
        f"Yeni anlık görüntü {yeni}: {ozet}"
        if yeni
        else f"Art arda hata, durdu (yeniden çalıştır): {ozet}"
    )


def _en_yeni(kok: Path) -> str:
    klasorler = sorted(p.name for p in (kok / "ag").glob("2*"))
    if not klasorler:
        raise veri.VeriHatasi("anlık görüntü yok: önce veriyi indir")
    return klasorler[-1]


def _denetim(n, tekrar) -> int:
    """Boru hattı denetimi (TASARIM 5.12): sonuç docs/denetim.md, rapor ve günlükte (`tur=destek`); yanlış kabul > %5 ise çıkış 1."""
    s = denetim.calistir(n=n, tekrar=tekrar)
    yol, html = denetim.yaz(s)
    kayit.denetim_yaz(s)
    for aile, y in s["yanlis_kabul"].items():
        guc = "; ".join(
            f"etki {e:.0%}: {g['olcut_1_4']['adet']}/{g['olcut_1_4']['n']} (Kâğıt {g['kagit']['adet']})"
            for e, g in s["guc"][aile].items()
        )
        print(
            f"{aile}: yanlış kabul {y['olcut_1_4']['adet']}/{y['olcut_1_4']['n']} (Kâğıt {y['kagit']['adet']}), güç {guc}"
        )
    print(f"Boru hattı denetimi {'geçti' if s['gecti'] else 'KALDI'}: {yol}, {html}")
    if not s["gecti"]:
        print(
            "Yanlış kabul > %5: ilk resmi koşu yapılmaz (TASARIM 5.12).",
            file=sys.stderr,
        )
    return 0 if s["gecti"] else 1


def _tansu_sinama(a, kok: Path) -> int:
    """Tansu sınaması (TASARIM 5.14): koşar, `rapor/tansu-sinama-<koşu>.json` ve günlük satırını yazar, özeti basar."""
    kimlik = a.kimlik or _en_yeni(kok)
    anlik = veri.oku(kimlik, kok)
    aileler = (a.aile,) if a.aile else tansusinama.AILELER
    sektor = anlik.sektor
    if not sektor and ciftbolme.AILE in aileler:
        sektor = tansusinama.sektor_oku(a.sektor_kok)[0]
    s = tansusinama.calistir(
        anlik, sektor or {}, aileler, isci=a.isci, hisse=a.hisse, ilerleme=print
    )
    manifest = kok / "ag" / kimlik / "manifest.json"
    s["manifest_sha256"] = hashlib.sha256(manifest.read_bytes()).hexdigest()
    yol = tansusinama.yaz(s)
    for aile, f in s["aileler"].items():
        o = f["ozet"]
        print(
            f"{aile}: {o['toplam']} iş, sağlam bölge var {o['saglam_bolge_var']}, yok {o['saglam_bolge_yok']}, "
            f"para çıkmaz {o['para_cikmaz']}; seçilenlerde al-tutu geçen {o['altut_gecen']}"
        )
    print(
        f"Tansu sınaması {s['kosu_id']}: {s['makine']['isci']} işçi, {s['makine']['sure_sn']} sn, {yol}"
    )
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="tansu")
    ap.add_argument(
        "komut",
        choices=[
            "sadakat",
            "kayit",
            "sinama",
            "tansu-sinama",
            "denetim",
            "evren-indir",
            "sektor-indir",
            "gunluk",
        ],
    )
    ap.add_argument(
        "tarih", nargs="?", help="yalnız gunluk: YYYY-AA-GG (varsayılan bugün)"
    )
    ap.add_argument("--kok", default="veri")
    ap.add_argument("--kimlik")
    ap.add_argument("--resmi", action="store_true")
    ap.add_argument(
        "--son",
        action="store_true",
        help="tam K1 tekrarı: max(1.000, 200·m); yoksa geliştirme (200)",
    )
    ap.add_argument(
        "--n",
        type=int,
        default=200,
        help="denetim: boş dünya tekrarı (her etki düzeyi ve aile için n/10)",
    )
    ap.add_argument(
        "--tekrar",
        type=int,
        default=denetim.TEKRAR,
        help="denetim: her tekrarda K1 tekrarı B",
    )
    ap.add_argument(
        "--isci", type=int, help="tansu-sinama: işçi sayısı (varsayılan: makineye göre)"
    )
    ap.add_argument("--hisse", type=int, help="tansu-sinama: adına göre ilk N hisse")
    ap.add_argument(
        "--aile",
        choices=tansusinama.AILELER,
        help="tansu-sinama: tek aile (varsayılan ikisi de)",
    )
    ap.add_argument(
        "--sektor-kok",
        default="veri",
        help="tansu-sinama: günlük anlık görüntüde sektör yoksa sektörün okunacağı kök",
    )
    a = ap.parse_args(argv)
    kok = Path(a.kok)
    try:
        if a.komut == "denetim":
            return _denetim(a.n, a.tekrar)
        if a.komut == "tansu-sinama":
            return _tansu_sinama(a, kok)
        if a.komut == "gunluk":
            return gunluk.gunluk(a.tarih or dt.datetime.now(veri.ISTANBUL).date(), kok)
        if a.komut == "evren-indir":
            print(_evren_indir(kok))
        elif a.komut == "sektor-indir":
            print(_sektor_indir(kok, a.kimlik or _en_yeni(kok)))
        elif a.komut == "kayit":
            print("Kural kaydı yazıldı:", kayit.kayitla()["kural_id"])
        elif a.komut == "sinama":
            s = kayit.kosu(
                a.kimlik or _en_yeni(kok),
                kok,
                resmi=a.resmi,
                tekrar=kayit.tekrar_sayisi(a.son),
                son=a.son,
            )
            print(
                f"Koşu {s['kosu_id']}: {len(s['islemler'])} işlem, {s['dusen']} düşen sinyal, özet {s['ozet'][:12]}"
            )
            for aile, k in s["kabul"].items():
                print(
                    f"K1 {aile}: p {k['k1']['p']:.4f} (B {k['k1']['tekrar']}), Holm p {k['holm']['holm_p']:.4f} "
                    f"(m {k['holm']['holm_m']}{', varsayımsal' if k['holm']['varsayimsal'] else ''}), "
                    f"sonuç {k['genel']}, durum {k['durum']}"
                )
            b = s["sim"]["bilgi"]
            print(
                "Veri kapıları (evren üyeleri):",
                "; ".join(b["sorunlar"]) or "temiz",
                f"| kapanma (−%100): {b['kapanma']} | rapor: {s['rapor']}",
            )
            c = s["cift"]
            print(
                f"Çift bölmesi: {len(c['secim'])} çift seçildi, {c['bilgi']['gecis']} tutuş dönemi, işlem yok yılları: {c['islem_yok'] or 'yok'}"
            )
        else:
            kimlik = a.kimlik or _kimlik_bul(kok)
            print(
                sadakat.calistir(
                    kimlik,
                    kok,
                    Path("docs") / "sadakat.md",
                    kayit.KAYIT_DIZINI / "deneme.jsonl",
                )
            )
    except (kayit.KayitHatasi, veri.VeriHatasi) as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
