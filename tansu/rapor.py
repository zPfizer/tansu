"""Rapor: tek dosya HTML ve işlem CSV'si (TASARIM 6.8). Sayı biçimi tek yardımcıdan gelir."""

import html
from pathlib import Path

from tansu.simulator import SERMAYE

RAPOR_DIZINI = Path("rapor")  # testte conftest yönlendirir
UYARI = "Tansu'dan esinlenen yorum. Tansu'nun kendi kuralı değildir; yatırım tavsiyesi değildir. Karar ve para sizindir."


def _kac(metin):
    return html.escape(str(metin), quote=False)


def yuzde(x) -> str:
    return f"%{x * 100:.2f}".replace(".", ",")


def tl(x) -> str:
    return f"{x:,.0f}".replace(",", ".")


def _tablo(baslik, satirlar) -> str:
    ust = "".join(f"<th>{_kac(b)}</th>" for b in baslik)
    ic = "".join("<tr>" + "".join(f"<td>{_kac(h)}</td>" for h in s) + "</tr>" for s in satirlar)
    return f"<table><tr>{ust}</tr>{ic}</table>"


def _egri(sim_m) -> str:
    """Özkaynak ve K2 eğrisi, satır içi SVG."""
    oz, k2 = sim_m["ozkaynak"], sim_m["k2"]
    if len(oz) < 2:
        return ""
    en, boy = 800, 240
    alt, ust = min(oz.min(), k2.min()), max(oz.max(), k2.max())
    nokta = lambda s: " ".join(  # noqa: E731
        f"{en * i / (len(s) - 1):.1f},{boy - boy * (v - alt) / ((ust - alt) or 1):.1f}" for i, v in enumerate(s))
    return (f'<svg width="{en}" height="{boy}" viewBox="0 0 {en} {boy}">'
            f'<polyline fill="none" stroke="#1b6ca8" points="{nokta(oz)}"/>'
            f'<polyline fill="none" stroke="#999" points="{nokta(k2)}"/></svg>'
            f"<p>Mavi: kural özkaynağı. Gri: K2 (maruziyeti eşleşmiş evren sepeti). Başlangıç {tl(SERMAYE)} TL.</p>")



def _uyarilar(sim, bilgi) -> list:
    b, m = sim["bilgi"], sim["masraf"][0.003]
    n = len(m["islemler"])
    pay = lambda k: yuzde(m["bagli"][k] / n) if n else yuzde(0)  # noqa: E731
    sorun = ("VERİ SORUNLU: " + "; ".join(b["sorunlar"])) if b["sorunlar"] else "Veri kapıları (evren üyesi hisse-günler) temiz."
    return [
        f"{sorun} Karantina oranı {yuzde(b['oran_uye'][0])} (eşik %1,00), olay denetimi farkı oranı "
        f"{yuzde(b['oran_uye'][1])} (eşik %2,00); {tl(b['uye_gun'])} üye hisse-günü, {b['uye_sembol']} sembol.",
        f"Tüm evren (üye olmayanlar dahil) oranları: karantina {yuzde(b['oran_tum'][0])}, olay denetimi "
        f"{yuzde(b['oran_tum'][1])}. Kapı kararı üye oranlarıyla verilir.",
        f"Olay tablosu boş dönen üye sembol: {b['olay_bos_uye_sembol']}. Üye hisse-günlerindeki "
        f"{tl(b['olay_uyari_uye'])} olay denetimi farkının {tl(b['olay_uyari_bos_tablo'])} tanesi bu sembollerdedir.",
        f"Karantina nedeniyle kapanan pozisyon (%0,3): {m['karantina_cikisi']}.",
        f"Bağlayıcı sınır (alınan {n} işlem, %0,3): tavan {pay('tavan')}, likidite {pay('likidite')}, "
        f"risk {pay('risk')}, nakit {pay('nakit')}. Ortalama planlanan risk / özkaynak {yuzde(m['ort_risk'])}.",
        f"İptal edilen sinyal (kilitli tavan ya da giriş günü yok; tüm semboller): {b['iptal']}.",
        f"Reddedilen sinyal (yer ya da nakit yetmedi; %0,3): {m['reddedilen']}.",
        f"İşlemi kapanan hisse sayısı {b['kapananlar']}. Kapanma nedeni bağlı değil: her kapanma −%100 sayılır; "
        f"bu kuralla kapanan işlem {b['kapanma']} (alınan {m['kapanma']}).",
        f"Faiz: borsapy TCMB politika faizi, son değişim {b['faiz_son_degisim'].date()}.",
        "Vergi sınamaya girmez.",
    ]


def yaz(sim, bilgi, dizin=None) -> tuple:
    """`bilgi`: kosu_id, anlik, kod_hash. (html yolu, csv yolu) döndürür."""
    dizin = Path(dizin or RAPOR_DIZINI)
    dizin.mkdir(parents=True, exist_ok=True)
    m3, b = sim["masraf"][0.003], sim["bilgi"]
    durum = "SORUNLU" if b["sorunlar"] else "TAMAM"
    sonuc = [(yuzde(m), tl(s["ozkaynak"].iloc[-1]), yuzde(s["ozkaynak"].iloc[-1] / 1e6 - 1),
              yuzde(s["k2"].iloc[-1] / 1e6 - 1), len(s["islemler"]), s["reddedilen"])
             for m, s in sim["masraf"].items()]
    yillar = sorted(m3["yillik"].index)
    yillik = [(y, yuzde(m3["yillik"].at[y, "kural"]), yuzde(m3["yillik"].at[y, "k2"]),
               *(yuzde(sim["masraf"][m]["yillik"].at[y, "fazla"]) for m in (0.001, 0.003, 0.005))) for y in yillar]
    govde = [
        "<h1>TANSU sınama raporu</h1>",
        f"<p><b>{_kac(UYARI)}</b></p>",
        _tablo(["Alan", "Değer"], [("Koşu", bilgi["kosu_id"]), ("Anlık görüntü", bilgi["anlik"]),
                                    ("Kod hash'i", bilgi["kod_hash"]), ("Dönem", f"{b['basla'].date()} - {b['bitis'].date()}"),
                                    ("Veri durumu", durum)]),
        "<h2>Sonuç</h2>",
        _tablo(["Masraf", "Son özkaynak TL", "Kural getirisi", "K2 getirisi", "İşlem", "Reddedilen"], sonuc),
        _egri(m3),
        "<h2>Yıllık fazla getiri</h2>",
        "<p>Fazla getiri = yıllık kural getirisi − yıllık K2 getirisi (yüzde puan). Henüz p değeri yoktur.</p>",
        _tablo(["Yıl", "Kural %0,3", "K2", "Fazla %0,1", "Fazla %0,3", "Fazla %0,5"], yillik),
        "<h2>Uyarılar</h2>",
        "<ul>" + "".join(f"<li>{_kac(u)}</li>" for u in _uyarilar(sim, bilgi)) + "</ul>",
    ]
    yol = dizin / f"rapor-{bilgi['kosu_id']}.html"
    csv = dizin / f"islemler-{bilgi['kosu_id']}.csv"
    yol.write_text('<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><title>TANSU</title></head><body>'
                   + "\n".join(govde) + "</body></html>", encoding="utf-8")
    m3["islemler"].to_csv(csv, index=False, encoding="utf-8")
    return yol, csv
