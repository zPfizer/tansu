"""Sınama raporu: `rapor/<ad>/sinama.html`, `ozet.md`, `islemler.csv` (SPEC 5.10). Grafikler satır içi SVG."""

import html
from collections import Counter
from pathlib import Path

import pandas as pd

from tansu import sinama
from tansu.strateji import Strateji

RAPOR_KOKU = Path("rapor")
VARSAYIM = (
    "Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; "
    "veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV."
)
UYARI = "Bu rapor seviye ölçümüdür; alım-satım talimatı değildir."


def _tablo(satirlar: list[dict] | pd.DataFrame) -> str:
    t = pd.DataFrame(satirlar)
    if t.empty:
        return "<p>Kayıt yok.</p>"
    bas = "".join(f"<th>{html.escape(str(c))}</th>" for c in t.columns)
    govde = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in r) + "</tr>"
        for r in t.itertuples(index=False)
    )
    return f"<table><tr>{bas}</tr>{govde}</table>"


def egri_svg(islemler: pd.DataFrame, olcu: str, gen: int = 760, yuk: int = 240) -> str:
    """Çıkış tarihine göre kümülatif `olcu` ve düşüş."""
    if not len(islemler):
        return "<p>Eğri yok.</p>"
    b = sinama.BIRIM[olcu]
    r = sinama.sirala(islemler)[olcu].cumsum().to_numpy()
    tepe = pd.Series(r).cummax().clip(lower=0).to_numpy()
    alt, ust = min(0.0, r.min()), max(0.0, r.max(), tepe.max())
    olcek = (yuk - 20) / ((ust - alt) or 1)

    def nokta(i, v):
        x = 10 + i * (gen - 20) / max(len(r) - 1, 1)
        return f"{x:.1f},{yuk - 10 - (v - alt) * olcek:.1f}"

    egri = " ".join(nokta(i, v) for i, v in enumerate(r))
    dusus = " ".join(nokta(i, v) for i, v in enumerate(tepe))
    sifir = yuk - 10 - (0 - alt) * olcek
    return (
        f'<svg width="{gen}" height="{yuk}" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="10" x2="{gen - 10}" y1="{sifir:.1f}" y2="{sifir:.1f}" stroke="#999"/>'
        f'<polyline points="{dusus}" fill="none" stroke="#d88" stroke-dasharray="4 3"/>'
        f'<polyline points="{egri}" fill="none" stroke="#1f5fa8" stroke-width="2"/>'
        f'<text x="12" y="14" font-size="12">Kümülatif {b} (mavi), önceki tepe (kesikli); son {r[-1]:.2f} {b}</text>'
        "</svg>"
    )


def yaz(
    strateji: Strateji,
    islemler: pd.DataFrame,
    sinyaller: pd.DataFrame,
    sayac: Counter,
    *,
    kimlik: str,
    kok: Path = RAPOR_KOKU,
) -> Path:
    klasor = kok / strateji.ad
    klasor.mkdir(parents=True, exist_ok=True)
    olcu = strateji.olcu
    b = sinama.BIRIM[olcu]
    donem = sinama.donemler(islemler, sinyaller, olcu)
    hedefler = tuple(h for h, _ in strateji.cikis.hedef)
    donem_tablo = pd.DataFrame(donem).rename_axis("Ölçü").reset_index()
    nedenler = [{"Neden": k, "Adet": v} for k, v in sorted(sayac.items()) if v]
    semboller = sinama.sembol_tablosu(islemler, olcu)
    isabet_bolumu = ""
    if hedefler:
        isabet_bolumu += (
            f"<h2>Seviyelerin isabeti</h2>{_tablo(sinama.isabet(islemler, hedefler))}"
        )
    if strateji.sinif == "b":
        isabet_bolumu += f"<h2>İleri getiri (dolumdan sonra, net %)</h2>{_tablo(sinama.ileri_tablo(islemler))}"
    islemler.to_csv(klasor / "islemler.csv", index=False, encoding="utf-8")
    sinif = "a (tam seviye)" if strateji.sinif == "a" else "b (giriş taraması)"
    parametre = ", ".join(f"{k} = {v}" for k, v in strateji.varsayilan.items())
    govde = f"""<!doctype html><html lang="tr"><meta charset="utf-8">
<title>{html.escape(strateji.ad)} sınama</title>
<style>body{{font-family:sans-serif;max-width:1100px;margin:auto}}table{{border-collapse:collapse;margin:8px 0}}
td,th{{border:1px solid #ccc;padding:3px 6px;font-size:13px;text-align:right}}th{{background:#eee}}</style>
<h1>{html.escape(strateji.ad)}: geçmiş sınama</h1>
<p><b>{UYARI}</b></p>
<p>Sınıf: {sinif}. Zaman: {strateji.zaman}. Kural kartı: {", ".join(strateji.kaynaklar)} (yerel). Veri görüntüsü: {html.escape(kimlik)}.</p>
<p>Parametreler (varsayılan, ayarsız): {html.escape(parametre)}.</p>
<p>{VARSAYIM}</p>
<p>Dönem: sinyal tarihi 04.01.2021-31.12.2025, BIST 30 üyesi günler. 2026 saklı dönemdir ve bu rapora girmez.</p>
<h2>Dönem tablosu</h2>{_tablo(donem_tablo)}
{isabet_bolumu}
<h2>Kümülatif {b}</h2>{egri_svg(islemler, olcu)}
<h2>Düşen sinyaller</h2>{_tablo(nedenler)}
<h2>Sembol tablosu</h2>{_tablo(semboller)}
<p>İşlem kaydı: islemler.csv ({len(islemler)} satır).</p>
</html>"""
    (klasor / "sinama.html").write_text(govde, encoding="utf-8")
    tum = donem["Bütün yıllar"]
    satirlar = [
        f"# {strateji.ad}: sınama özeti",
        "",
        UYARI,
        "",
        f"Veri görüntüsü: {kimlik}. Dönem: 2021-2025. Parametreler varsayılan.",
        "",
        f"| Dönem | Sinyal | Dolum | Beklenti {b} | Toplam {b} | Kazanma |",
        "|---|---|---|---|---|---|",
        *(
            f"| {ad} | {d['Sinyal']} | {d['Dolum']} | {d[f'Beklenti (ortalama {b})']} | {d[f'Toplam {b}']} | {d['Kazanma oranı']} |"
            for ad, d in donem.items()
        ),
        "",
        f"Bütün yıllar: en büyük düşüş {tum[f'En büyük düşüş {b}']} {b}, açık işlem {tum['Açık işlem']}.",
        "",
        VARSAYIM,
        "",
    ]
    (klasor / "ozet.md").write_text("\n".join(satirlar), encoding="utf-8")
    return klasor / "sinama.html"
