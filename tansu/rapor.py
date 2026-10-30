"""Sınama raporu: `rapor/<ad>/sinama.html`, `ozet.md`, `islemler.csv` (SPEC 5.6, 5.10). Grafikler satır içi SVG."""

import datetime as dt
import enum
import html
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, assert_never

import numpy as np
import pandas as pd

from tansu import ayar, montecarlo, sinama
from tansu.strateji import Strateji

RAPOR_KOKU = Path("rapor")
VARSAYIM = (
    "Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; "
    "veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV."
)
UYARI = "Bu rapor seviye ölçümüdür; alım-satım talimatı değildir."
TARIH_TABANI = (
    "Yıl tabloları, ayar ve ileri yürüme 31.12.2025 sonrasındaki fiyatı kullanmaz; o gün açık kalan kurulum "
    "o günün kapanışıyla açık işaretlenir. Dönemler sinyal tarihine göredir."
)
ORNEK_AZ = "Örnek az; bu strateji için onay bayrağı çıkmayabilir."
ACIKLAMA = "Kural ve varsayılanlar, test ve saklı dönem içinde tarihli Tansu gönderilerinden alındı"
ONAY_YOK = "Program hiçbir stratejiyi kendisi onaylamaz; bu bayraklar yalnız Levent'in kararına yardım eder."
RASTGELE = (
    "Her koşu, her test penceresinde gerçek kurulum sayısı kadar rastgele üye günde piyasa girişi açar; "
    "stop ve hedef uzaklıkları gerçek bir kurulumdan sinyal günü ATR(14) katı olarak kopyalanır, çıkış kuralları aynıdır."
)


@dataclass(frozen=True)
class Sinama:
    """Bir raporun bütün girdisi; `sina` ve `ayarla` aynı değeri kurar."""

    strateji: Strateji
    parametre: dict[str, float | str]
    ayar_tarihi: str | None
    kimlik: str
    gecmis: sinama.Kosu
    yuruyus: ayar.Yuruyus
    sakli: sinama.Kosu
    sakli_son: pd.Timestamp
    sinanan: int
    mc: montecarlo.MonteCarlo


def hazirla(
    strateji: Strateji,
    gunler: sinama.Gunler,
    *,
    kimlik: str,
    sinanan: int,
    ayarla: bool,
    okunan: ayar.Okunan | None,
) -> Sinama:
    """Dosya yazmaz."""
    yuruyus = ayar.yuru(strateji, gunler)
    mc = montecarlo.hesapla(strateji, gunler, yuruyus)
    if ayarla:
        p, ayar_tarihi = yuruyus.son.parametre, dt.date.today().isoformat()
    elif okunan:
        p, ayar_tarihi = okunan.parametreler, okunan.tarih
    else:
        p, ayar_tarihi = dict(strateji.varsayilan), None
    gecmis = sinama.calistir(strateji, gunler, p, sinama.GECMIS)
    sakli_son = sinama.sakli_son(gunler)
    sakli = sinama.calistir(
        strateji, gunler, p, sinama.Donem(sinama.ILK_GIRIS, sakli_son)
    ).kes(sinama.SAKLI_BAS, sakli_son)
    return Sinama(
        strateji=strateji,
        parametre=p,
        ayar_tarihi=ayar_tarihi,
        kimlik=kimlik,
        gecmis=gecmis,
        yuruyus=yuruyus,
        sakli=sakli,
        sakli_son=sakli_son,
        sinanan=sinanan,
        mc=mc,
    )


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


def _tarih(t: pd.Timestamp) -> str:
    return f"{t:%d.%m.%Y}"


def _deger(x: float | None) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{x:.2f}"


def _eksen(izgara: ayar.Izgara, i: int) -> str:
    return ", ".join(f"{k} = {v}" for k, v in izgara.eksenler(i).items())


def _oran(deger: float, n: int, bicim: str = "{:.2f}") -> str:
    if n < sinama.EN_AZ:
        return f"n/a (N = {n})"
    return "n/a" if not np.isfinite(deger) else bicim.format(deger)


def _ozet_sutunu(o: sinama.Ozet, b: str) -> dict[str, str | int]:
    n = o.dolum
    dusen = o.sinyal - n
    return {
        "Sinyal": o.sinyal,
        "Dolum": n,
        "Düşen": f"{dusen} ({dusen / o.sinyal:.0%})" if o.sinyal else "0",
        "Kazanma oranı": _oran(o.kazanma, n, "{:.0%}"),
        f"Ortalama kazanç {b}": _oran(o.ort_kazanc, n),
        f"Ortalama kayıp {b}": _oran(o.ort_kayip, n),
        f"Beklenti (ortalama {b})": _oran(o.beklenti, n),
        f"Medyan {b}": _oran(o.medyan, n),
        f"Toplam {b}": f"{o.toplam:.2f}",
        "Kâr faktörü": _oran(o.kar_faktoru, n),
        "Sharpe (kurulum başı)": _oran(o.sharpe, n),
        "Sortino (kurulum başı)": _oran(o.sortino, n),
        f"En büyük düşüş {b}": f"{o.dusus:.2f}",
        "Toplam / düşüş": _oran(o.toplam_dusus, n),
        "Ortalama tutma günü": f"{o.tutma:.1f}" if n else "-",
        "En uzun kayıp serisi": str(o.kayip_serisi),
        "Açık işlem": o.acik,
        "Dolumda stop": o.dolumda_stop,
        "Risk tabanı uygulanan": o.risk_tabanli,
    }


def _donem_tablosu(donem: dict[str, dict]) -> str:
    return _tablo(pd.DataFrame(donem).rename_axis("Ölçü").reset_index())


def _gun(x: float | None) -> str:
    return "-" if x is None else f"{x:.0f}"


def _isabet_satiri(i: sinama.Isabet) -> dict[str, str]:
    return {
        "Hedef": i.hedef,
        "Stoptan önce ulaştı": _oran(i.ulasti, i.n, "{:.0%}"),
        "Önce stop": _oran(i.stop_once, i.n, "{:.0%}"),
        "Medyan gün (hedef)": _gun(i.gun_hedef),
        "Medyan gün (stop)": _gun(i.gun_stop),
    }


def _ileri_satiri(i: sinama.Ileri) -> dict[str, str | int]:
    return {
        "Ufuk (gün)": f"Medyan {i.ufuk} % (10 gün)"
        if isinstance(i.ufuk, str)
        else i.ufuk,
        "N": i.n,
        "Ortalama net %": "-" if i.ortalama is None else _oran(i.ortalama, i.n),
        "Medyan net %": _oran(i.medyan, i.n),
        "Pozitif payı": "-" if i.pozitif is None else _oran(i.pozitif, i.n, "{:.0%}"),
    }


def _ileri_tablosu(kosular: dict[str, sinama.Kosu]) -> str:
    """Sınıf (b) ileri getiri tablosu, dönem başına (SPEC 5.6)."""
    return _tablo(
        [
            {"Dönem": ad, **_ileri_satiri(i)}
            for ad, k in kosular.items()
            for i in sinama.ileri_tablo(k.islemler)
        ]
    )


def parametre_satiri(s: Sinama) -> str:
    """Seviye parametresi Tansu'nun değerinden farklıysa ikisi birlikte; ayarlı olan `varsayım` (SPEC 1)."""
    st = s.strateji
    kaynak = "varsayılan" if s.ayar_tarihi is None else f"ayarlı, {s.ayar_tarihi}"
    metin = ", ".join(f"{k} = {v}" for k, v in s.parametre.items())
    farkli = [
        f"{k} = {s.parametre[k]} (varsayım), Tansu'nun değeri {st.varsayilan[k]}"
        for k in st.seviye_param
        if s.parametre[k] != st.varsayilan[k]
    ]
    ek = f" Seviye parametresi farklı: {'; '.join(farkli)}." if farkli else ""
    return f"Parametreler ({kaynak}): {metin}.{ek}"


def aciklama(strateji: Strateji, sakli_son: pd.Timestamp) -> str:
    """SPEC 5.6 açıklaması: ileri yürüme test pencereleri ya da saklı dönem içindeki kaynak tarihleri."""
    bas, son = ayar.PENCERELER[0].test_bas, max(sinama.KESIM, sakli_son)
    tarihler = [
        _tarih(t)
        for t in map(pd.Timestamp, strateji.kaynak_tarihleri)
        if bas <= t <= son
    ]
    if not tarihler:
        return "Kural ve varsayılanların kaynak gönderilerinden hiçbiri test ve saklı dönem içinde tarihli değil."
    return (
        f"{ACIKLAMA}: {', '.join(tarihler)}. "
        "Bu dönemler kural seçimi için tam örneklem dışı değildir."
    )


def _izgara_bolumu(y: ayar.Yuruyus, b: str) -> str:
    iz, son = y.izgara, y.son
    metin = (
        f"<p>Denenen nokta: {len(iz)}. 31.12.2025 eğitim sonunda puanlı nokta: "
        f"{int(np.isfinite(son.puan).sum())}.</p>"
    )
    if son.puanli:
        i = son.nokta
        metin += (
            f"<p>Seçilen nokta: {html.escape(_eksen(iz, i))}; puan {son.puan[i]:.2f} {b}, "
            f"sağlam puan {son.saglam[i]:.2f} {b}, N = {son.n[i]}.</p>"
        )
    else:
        metin += f"<p><b>{ORNEK_AZ}</b> Seçim: varsayılanlar.</p>"
    v = iz.varsayilan_nokta
    metin += f"<p>Varsayılan nokta: puan {_deger(son.puan[v])} {b}, N = {son.n[v]}.</p>"
    ilk = sorted(
        np.flatnonzero(np.isfinite(son.saglam)),
        key=lambda i: (-son.saglam[i], -son.puan[i], i),
    )[:10]
    satirlar = [
        {
            **iz.eksenler(i),
            f"Puan {b}": f"{son.puan[i]:.2f}",
            f"Sağlam puan {b}": f"{son.saglam[i]:.2f}",
            "N": son.n[i],
        }
        for i in ilk
    ]
    return f"{metin}<h3>Sağlam puana göre ilk 10 nokta</h3>{_tablo(satirlar)}"


def _yuruyus_tablosu(y: ayar.Yuruyus, b: str) -> str:
    satirlar = [
        {
            "Pencere": a.pencere.ad,
            "Eğitim": f"{_tarih(sinama.ILK_GIRIS)}-{_tarih(a.pencere.egitim_son)}",
            "Seçim": _eksen(y.izgara, a.secim.nokta)
            if a.secim.puanli
            else "varsayılan (puanlı nokta yok)",
            "Eğitim N": a.ic_n,
            f"Eğitim toplam / yıl {b}": f"{a.ic_yillik:.2f}",
            "Test N": len(a.test.islemler),
            f"Test toplam / yıl {b}": f"{a.dis_yillik:.2f}",
            "Verim": _deger(a.verim),
        }
        for a in y.adimlar
    ]
    return (
        f"{_tablo(satirlar)}<p>Ortalama verim: {_deger(y.verim)} "
        f"({y.verim_adim}/{len(y.adimlar)} adım; eğitim toplamı 0 ya da altındaysa adım n/a).</p>"
    )


def _evet(kosul: bool, deger: str) -> str:
    return f"{'evet' if kosul else 'hayır'} ({deger})"


class Bayrak(enum.Enum):
    """SPEC 5.9 bayrakları."""

    DIS_BEKLENTI = enum.auto()
    RASTGELE = enum.auto()
    BOOTSTRAP = enum.auto()
    SAKLI = enum.auto()
    KAZANMA_90 = enum.auto()
    KAZANMA_BANT = enum.auto()
    SECIM_PUANI = enum.auto()
    SEMBOL = enum.auto()


class Olcum(NamedTuple):
    kosul: bool | None
    deger: float | None
    n: int
    sembol: str | None = None


def bayrak_olc(
    mc: montecarlo.MonteCarlo,
    dis: sinama.Kosu,
    sakli: sinama.Kosu,
    gecmis: sinama.Kosu,
    son: ayar.Secim,
) -> dict[Bayrak, Olcum]:
    """SPEC 5.9 bayrakları. `dis`: dikişli örneklem dışı, `sakli`: saklı dönem, `gecmis`: yıl tablolarının koşusu;
    `son`: 31.12.2025 ayar seçimi."""
    x = dis.islemler[dis.olcu]
    n = len(x)

    def oran(kosul: bool, deger: float) -> Olcum:
        return Olcum(None if n < sinama.EN_AZ else bool(kosul), deger, n)

    r, bt = mc.rastgele, mc.bootstrap_toplam
    kazanma = (x > 0).mean()
    secim_n = int(son.n[son.nokta])
    puan = son.puan[son.nokta]
    semboller = sinama.sembol_tablosu(gecmis.islemler, gecmis.olcu)
    gecmis_n = len(gecmis.islemler)
    if semboller["pay"].isna().all():
        sembol = Olcum(None, None, gecmis_n)
    else:
        ilk = semboller.iloc[0]
        sembol = Olcum(bool(ilk["isaret"]), ilk["pay"], gecmis_n, ilk["sembol"])
    return {
        Bayrak.DIS_BEKLENTI: oran(x.mean() > 0, x.mean()),
        Bayrak.RASTGELE: Olcum(None, None, mc.n)
        if r is None
        else Olcum(bool(r.yuzdelik >= 95), r.yuzdelik, mc.n),
        Bayrak.BOOTSTRAP: Olcum(None, None, mc.n)
        if bt is None
        else Olcum(bool(bt[0] > 0), bt[0], mc.n),
        Bayrak.SAKLI: Olcum(bool(sakli.toplam > 0), sakli.toplam, len(sakli.islemler))
        if len(sakli.islemler)
        else Olcum(None, None, 0),
        Bayrak.KAZANMA_90: oran(kazanma >= 0.9, kazanma),
        Bayrak.KAZANMA_BANT: oran(not 0.4 <= kazanma <= 0.6, kazanma),
        Bayrak.SECIM_PUANI: Olcum(bool(puan <= 0), puan, secim_n)
        if son.puanli
        else Olcum(None, None, secim_n),
        Bayrak.SEMBOL: sembol,
    }


def bayrak_satirlari(olcum: dict[Bayrak, Olcum], b: str) -> list[dict]:
    satirlar = []
    for bayrak in Bayrak:
        o = olcum[bayrak]
        az, yok, birimli = f"örnek az (N = {o.n})", f"n/a (N = {o.n})", f"{{:.2f}} {b}"
        match bayrak:
            case Bayrak.DIS_BEKLENTI:
                ad = f"Örneklem dışı beklenti 0'ın üstünde ({b})"
                bicim, neden = birimli, az
            case Bayrak.RASTGELE:
                ad = "Strateji rastgele girişlerin 95. yüzdeliğinde ya da üstünde"
                bicim, neden = "yüzdelik {:.1f}", _rastgele_yok(o.n)
            case Bayrak.BOOTSTRAP:
                ad = "Bootstrap toplamının 5. yüzdeliği 0'ın üstünde"
                bicim, neden = birimli, yok
            case Bayrak.SAKLI:
                ad = "Saklı dönem toplamı 0'ın üstünde (bilgi)"
                bicim, neden = birimli, yok
            case Bayrak.KAZANMA_90:
                ad = "Uyarı: kazanma oranı %90 ya da üstü (örneklem dışı)"
                bicim, neden = "{:.0%}", az
            case Bayrak.KAZANMA_BANT:
                ad = "Uyarı: kazanma payı %40-60 dışında (örneklem dışı, varsayım)"
                bicim, neden = "{:.0%}", az
            case Bayrak.SECIM_PUANI:
                ad = "Uyarı: seçilen ızgara noktasının kendi puanı 0 ya da altında"
                bicim, neden = birimli, "puanlı nokta yok"
            case Bayrak.SEMBOL:
                ad = (
                    "Uyarı: bir sembol toplamın %40'ından fazlasını veriyor (2021-2025)"
                )
                bicim = "{s} {:.0%}"
                neden = "n/a (toplam 0 ya da altında, pay tanımsız)"
            case _:
                assert_never(bayrak)
        deger = (
            neden
            if o.kosul is None
            else _evet(o.kosul, bicim.format(o.deger, s=o.sembol))
        )
        satirlar.append({"Bayrak": ad, "Değer": deger, "N": o.n})
    return satirlar


def _rastgele_yok(n: int) -> str:
    if n < sinama.EN_AZ:
        return f"n/a (N = {n})"
    return "n/a (uygun rastgele gün ya da şablon yok)"


def _uclu(y: montecarlo.Yuzdelik | None, n: int) -> str:
    return f"n/a (N = {n})" if y is None else " / ".join(f"{v:.2f}" for v in y)


def _mc_tablosu(mc: montecarlo.MonteCarlo, sutunlar: dict) -> str:
    if any(v is None for v in sutunlar.values()):
        return f"<p>n/a (N = {mc.n})</p>"
    return _tablo(
        [
            {"Yüzdelik": ad, **{k: f"{v[i]:.2f}" for k, v in sutunlar.items()}}
            for i, ad in enumerate(("p5", "p50", "p95"))
        ]
    )


def _mc_bolumu(mc: montecarlo.MonteCarlo, sinif: str) -> str:
    b = sinama.BIRIM[mc.olcu]
    r = mc.rastgele
    metin = (
        f"<p>Tohum: {mc.tohum}. Koşu: {mc.tekrar}. Girdi: dikişli örneklem dışı kurulumlar, "
        f"N = {mc.n}, çıkış tarihi sırasıyla.</p>"
        "<h3>Bootstrap (yerine koyarak çekiliş)</h3>"
        + _mc_tablosu(
            mc,
            {
                f"Toplam {b}": mc.bootstrap_toplam,
                f"En büyük düşüş {b}": mc.bootstrap_dusus,
            },
        )
    )
    if sinif == "a":
        batma = f"n/a (N = {mc.n})" if mc.batma is None else f"{mc.batma:.1%}"
        metin += (
            f"<p>Batma riski (düşüş ≥ {montecarlo.BATMA_R:g} R, varsayım): {batma}.</p>"
        )
    metin += "<h3>Sıra karıştırma</h3>" + _mc_tablosu(
        mc, {f"En büyük düşüş {b}": mc.karistirma_dusus}
    )
    metin += f"<h3>Rastgele giriş kıyası</h3><p>{RASTGELE}</p>"
    if r is None:
        return metin + f"<p>{_rastgele_yok(mc.n)}</p>"
    return (
        metin
        + _mc_tablosu(mc, {f"Koşu ortalaması {b}": r.ortalamalar})
        + f"<p>Strateji ortalaması {r.strateji_ort:.2f} {b}; rastgele koşu ortalamaları içinde "
        f"yüzdelik {r.yuzdelik:.1f}.</p>"
    )


def yaz(s: Sinama, kok: Path = RAPOR_KOKU) -> Path:
    strateji, y = s.strateji, s.yuruyus
    klasor = kok / strateji.ad
    klasor.mkdir(parents=True, exist_ok=True)
    olcu = strateji.olcu
    b = sinama.BIRIM[olcu]
    islemler = s.gecmis.islemler
    donem = {ad: _ozet_sutunu(o, b) for ad, o in sinama.donemler(s.gecmis).items()}
    hedefler = tuple(h for h, _ in strateji.cikis.hedef)
    nedenler = [{"Neden": k, "Adet": v} for k, v in sorted(s.gecmis.sayac.items()) if v]
    semboller = sinama.sembol_tablosu(islemler, olcu)
    sakli_tarih = f"{_tarih(sinama.SAKLI_BAS)}-{_tarih(s.sakli_son)}"
    yillar = {str(yil): s.gecmis.yil(yil) for yil in sinama.YILLAR}

    def ileri(kosular: dict[str, sinama.Kosu]) -> str:
        if strateji.sinif != "b":
            return ""
        return f"<h3>İleri getiri (dolumdan sonra, net %)</h3>{_ileri_tablosu(kosular)}"

    isabet_bolumu = ""
    if hedefler:
        isabet = [_isabet_satiri(i) for i in sinama.isabet(islemler, hedefler)]
        isabet_bolumu = f"<h2>Seviyelerin isabeti</h2>{_tablo(isabet)}"
    # Sütunlu boş kayıt başlık satırı yazardı; kurulumsuz koşunun dosyası tek satır sonu kalır.
    (islemler if len(islemler) else pd.DataFrame()).to_csv(
        klasor / "islemler.csv", index=False, encoding="utf-8", lineterminator="\n"
    )
    mc = s.mc
    bayrak = bayrak_satirlari(bayrak_olc(mc, y.dis_ornek, s.sakli, s.gecmis, y.son), b)
    sinif = "a (tam seviye)" if strateji.sinif == "a" else "b (giriş taraması)"
    sakli_notu = (
        "" if s.sakli_son >= sinama.SAKLI_BAS else " Veri saklı döneme ulaşmıyor."
    )
    govde = f"""<!doctype html><html lang="tr"><meta charset="utf-8">
<title>{html.escape(strateji.ad)} sınama</title>
<style>body{{font-family:sans-serif;max-width:1100px;margin:auto}}table{{border-collapse:collapse;margin:8px 0}}
td,th{{border:1px solid #ccc;padding:3px 6px;font-size:13px;text-align:right}}th{{background:#eee}}</style>
<h1>{html.escape(strateji.ad)}: geçmiş sınama</h1>
<p><b>{UYARI}</b></p>
<p>Sınıf: {sinif}. Zaman: {strateji.zaman}. Kural kartı: {", ".join(strateji.kaynaklar)} (yerel). Veri görüntüsü: {html.escape(s.kimlik)}.</p>
<p>{html.escape(parametre_satiri(s))}</p>
<p>{VARSAYIM}</p>
<p>Dönem: sinyal tarihi 04.01.2021-31.12.2025. Evren: bütün BIST, kapanan paylar dahil; pay işlem gördüğü günlerde evrendedir. {TARIH_TABANI}</p>
<p>{html.escape(aciklama(strateji, s.sakli_son))}</p>
<p>Denenen parametre seti: {len(y.izgara)}. Şimdiye kadar sınanan strateji: {s.sinanan}.</p>
<h2>Dönem tablosu</h2>{_donem_tablosu(donem)}
{ileri({**yillar, "Bütün yıllar": s.gecmis})}
{isabet_bolumu}
<h2>Izgara sonucu</h2>{_izgara_bolumu(y, b)}
<h2>İleri yürüme</h2>{_yuruyus_tablosu(y, b)}
<h2>Dikişli örneklem dışı (2023H1-2025H2)</h2>{_donem_tablosu({"Örneklem dışı": _ozet_sutunu(y.dis_ornek.ozet(), b)})}
{ileri({"Örneklem dışı": y.dis_ornek})}
<h2>Saklı dönem</h2><p>Sinyal tarihi {sakli_tarih}, yukarıdaki parametrelerle tek kesintisiz koşu.{sakli_notu}</p>
{_donem_tablosu({"Saklı dönem": _ozet_sutunu(s.sakli.ozet(), b)})}
{ileri({"Saklı dönem": s.sakli})}
<h2>Monte Carlo</h2>{_mc_bolumu(mc, strateji.sinif)}
<h2>Bayraklar</h2><p><b>{ONAY_YOK}</b></p>{_tablo(bayrak)}
<h2>Kümülatif {b}</h2>{egri_svg(islemler, olcu)}
<h2>Düşen sinyaller</h2>{_tablo(nedenler)}
<h2>Sembol tablosu</h2>{_tablo(semboller)}
<p>İşlem kaydı: islemler.csv ({len(islemler)} satır).</p>
</html>"""
    (klasor / "sinama.html").write_text(govde, encoding="utf-8", newline="\n")
    tum = donem["Bütün yıllar"]
    son = y.son
    secim = (
        f"{_eksen(y.izgara, son.nokta)} (sağlam puan {son.saglam[son.nokta]:.2f} {b}, "
        f"N = {son.n[son.nokta]})"
        if son.puanli
        else f"varsayılanlar. {ORNEK_AZ}"
    )
    satirlar = [
        f"# {strateji.ad}: sınama özeti",
        "",
        UYARI,
        "",
        f"Veri görüntüsü: {s.kimlik}. Dönem: 2021-2025. {parametre_satiri(s)}",
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
        f"Izgara: {len(y.izgara)} nokta; son ayar seçimi: {secim}",
        "",
        f"Örneklem dışı (2023H1-2025H2): N = {len(y.dis_ornek.islemler)}, "
        f"toplam {y.dis_ornek.toplam:.2f} {b}; "
        f"ortalama verim {_deger(y.verim)} ({y.verim_adim}/{len(y.adimlar)} adım).",
        "",
        f"Saklı dönem {sakli_tarih}: N = {len(s.sakli.islemler)}, "
        f"toplam {s.sakli.toplam:.2f} {b}."
        if s.sakli_son >= sinama.SAKLI_BAS
        else "Saklı dönem: veri saklı döneme ulaşmıyor.",
        "",
        f"Monte Carlo (tohum {mc.tohum}, {mc.tekrar} koşu, örneklem dışı N = {mc.n}), p5 / p50 / p95:",
        "",
        f"- Bootstrap toplam {b}: {_uclu(mc.bootstrap_toplam, mc.n)}; "
        f"en büyük düşüş {b}: {_uclu(mc.bootstrap_dusus, mc.n)}"
        + (
            f"; batma riski {'n/a' if mc.batma is None else f'{mc.batma:.1%}'}"
            if strateji.sinif == "a"
            else ""
        ),
        f"- Sıra karıştırma en büyük düşüş {b}: {_uclu(mc.karistirma_dusus, mc.n)}",
        f"- Rastgele giriş koşu ortalaması {b}: "
        + (
            _rastgele_yok(mc.n)
            if mc.rastgele is None
            else f"{_uclu(mc.rastgele.ortalamalar, mc.n)}; strateji ortalaması "
            f"{mc.rastgele.strateji_ort:.2f} {b}, yüzdelik {mc.rastgele.yuzdelik:.1f}"
        ),
        "",
        f"Bayraklar. {ONAY_YOK}",
        "",
        *(f"- {r['Bayrak']}: {r['Değer']} (N = {r['N']})" for r in bayrak),
        "",
        VARSAYIM,
        "",
    ]
    (klasor / "ozet.md").write_text("\n".join(satirlar), encoding="utf-8", newline="\n")
    return klasor / "sinama.html"
