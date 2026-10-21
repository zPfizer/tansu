"""Sağlamlık ızgarası: önceden yazılmış hücreler birlikte oynatılır (TASARIM 5.10, KURALLAR §3).

Pozitif hücre: K1'e göre işlem başına ortalama fazla getiri > 0, %0,3 masrafla; p aranmaz, en iyi hücre seçilmez.
Hücre başına sonuç: `{"hucre": parametreler, "islem": n, "fazla": ortalama (işlem yoksa NaN), "pozitif": bool}`.
"""

import functools
import itertools
import math
from collections import deque
from dataclasses import replace

import numpy as np
import pandas as pd

from tansu import aileler, ciftbolme, istatistik, motor, simulator

MASRAF = 0.003  # TASARIM 5.10


def sec(izgara, hucreler, *, politika):
    """TASARIM 5.15 S11: dondurulmuş alanda sürümlü saf seçim."""
    if politika == "eksen_maksimin_legacy_v1":
        return _eksen_sec(hucreler) | dict(politika=politika)
    if politika == "pozitif_fazla_legacy_v1":
        pozitif = [bool(h["fazla"] > 0) for h in hucreler]
        return dict(
            politika=politika,
            secilen=None,
            pozitif=pozitif,
            oran=float(np.mean(pozitif)) if pozitif else float("nan"),
        )
    if politika != "genis_bolge_net_r_v1":
        raise ValueError(f"Bilinmeyen seçim politikası: {politika}")
    return _genis_bolge(izgara, hucreler) | dict(politika=politika)


def _eksen_sec(net):
    """TASARIM 5.14: eski tek eksenli maksimin ve C sırası korunur."""
    net = np.asarray(net, dtype=float)
    komsuluk = net.copy()
    for eksen, yon in itertools.product(range(net.ndim), (1, -1)):
        hedef = [slice(None)] * net.ndim
        kaynak = [slice(None)] * net.ndim
        hedef[eksen], kaynak[eksen] = (
            (slice(None, -1), slice(1, None))
            if yon == 1
            else (slice(1, None), slice(None, -1))
        )
        hedef, kaynak = tuple(hedef), tuple(kaynak)
        komsuluk[hedef] = np.minimum(komsuluk[hedef], net[kaynak])
    saglam = komsuluk > 0
    secilen = (
        int(np.argmax(np.where(saglam, komsuluk, -np.inf).ravel()))
        if saglam.any()
        else None
    )
    en_iyi = int(np.argmax(net.ravel()))
    return dict(
        saglam=saglam,
        secilen=secilen,
        en_iyi=en_iyi,
        para_cikmaz=bool(net.ravel()[en_iyi] <= 0),
    )


def _eksen_boyutlari(eksenler):
    if not eksenler:
        raise ValueError("Sayısal eksen gerekli.")
    for e in eksenler:
        v = e["degerler"]
        if not v or not all(_sonlu_sayi(x) for x in v):
            raise ValueError("Eksen değerleri sonlu sayılar olmalıdır.")
        if v != sorted(set(v)):
            raise ValueError("Eksen değerleri artan ve tekil olmalıdır.")
    return tuple(len(e["degerler"]) for e in eksenler)


def _sonlu_sayi(x):
    return type(x) in (int, float) and math.isfinite(x)


def _hucre_ozeti_dogrula(h):
    sayi, net = h["kapali_islem_sayisi"], h["toplam_net_r"]
    if sayi is None:
        if h["durum"] in ("tamamlandi", "islemsiz"):
            raise ValueError("Ölçülmüş hücrenin kapalı işlem sayısı boş olamaz.")
    elif type(sayi) is not int or sayi < 0:
        raise ValueError("Kapalı işlem sayısı negatif olmayan tamsayı olmalıdır.")
    if net is not None and not _sonlu_sayi(net):
        raise ValueError("Toplam net R sonlu sayı veya gerekçeli boş olmalıdır.")
    if h["durum"] not in {
        "tamamlandi",
        "islemsiz",
        "eksik",
        "hesap_hatasi",
        "kayit_hatasi",
        "baslamadi",
        "alan_disi",
    }:
        raise ValueError("Tanımsız hücre durumu.")


def _secim_alani(sekil, hucreler):
    alan = {
        i: dict(
            indeks=list(i), durum="eksik", kapali_islem_sayisi=None, toplam_net_r=None
        )
        for i in np.ndindex(*sekil)
    }
    gorulen = set()
    for h in hucreler:
        i = tuple(h["indeks"])
        if i not in alan or i in gorulen or any(type(k) is not int for k in i):
            raise ValueError("Hücre indeksi alan dışında veya yinelenmiş.")
        _hucre_ozeti_dogrula(h)
        gorulen.add(i)
        alan[i] = dict(h)
    return alan


def _olculmus_hucre(h):
    return (
        h["durum"] == "tamamlandi"
        and h["kapali_islem_sayisi"] > 0
        and h["toplam_net_r"] is not None
    )


def _eksen_uzakligi(i, j):
    return sum(abs(a - b) for a, b in zip(i, j, strict=True))


def _tarama_sinir_uzakligi(i, sekil):
    return min(min(a, n - 1 - a) for a, n in zip(i, sekil, strict=True))


def _komsu_mu(i, j):
    return i != j and all(abs(a - b) <= 1 for a, b in zip(i, j, strict=True))


def _komsu_bilgisi(i, alan, izinli, olculen):
    cevre = sorted(j for j in alan if _komsu_mu(i, j))
    komsular = [j for j in cevre if j in izinli]
    return dict(
        komsular=[list(j) for j in komsular],
        alan_disi_komsular=[list(j) for j in cevre if j not in izinli],
        eksik_komsular=[list(j) for j in komsular if j not in olculen],
    )


def _merkez_bilgisi(i, komsular, sekil, karli, olculen):
    sinir_uzakligi = _tarama_sinir_uzakligi(i, sekil)
    uygun = i in karli and sinir_uzakligi > 0 and all(j in karli for j in komsular)
    uzakliklar = [_eksen_uzakligi(i, j) for j in olculen.keys() - karli]
    return dict(
        karli=i in karli,
        sinir=sinir_uzakligi == 0,
        uygun_merkez=uygun,
        uzaklik=min([sinir_uzakligi, *uzakliklar]),
        en_kotu_komsu=min(olculen[j] for j in [i, *komsular]) if uygun else None,
    )


def _bagli_hucreler(ilk, kalan):
    kuyruk, bolge = deque([ilk]), {ilk}
    kalan.remove(ilk)
    while kuyruk:
        i = kuyruk.popleft()
        for j in sorted(kalan):
            if _eksen_uzakligi(i, j) == 1:
                bolge.add(j)
                kuyruk.append(j)
                kalan.remove(j)
    return sorted(bolge)


def _karli_bolgeler(alan, karli, olculen):
    bolgeler, kalan = [], set(karli)
    while kalan:
        bolge = _bagli_hucreler(min(kalan), kalan)
        bolgeler.append(
            dict(
                indeksler=[list(i) for i in bolge],
                buyukluk=len(bolge),
                medyan_net_r=float(np.median([olculen[i] for i in bolge])),
                uygun_merkezler=[list(i) for i in bolge if alan[i]["uygun_merkez"]],
                kanonik_indeks=list(bolge[0]),
            )
        )
    return bolgeler


def _bolge_merkezi(bolgeler, alan):
    uygun = [b for b in bolgeler if b["uygun_merkezler"]]
    if not uygun:
        return None
    bolge = min(
        uygun, key=lambda b: (-b["buyukluk"], -b["medyan_net_r"], b["kanonik_indeks"])
    )
    return min(
        bolge["uygun_merkezler"],
        key=lambda i: (-alan[tuple(i)]["uzaklik"], -alan[tuple(i)]["en_kotu_komsu"], i),
    )


def _en_iyi_hucre(olculen, secilen):
    if not olculen:
        return None
    indeks = list(min(olculen, key=lambda i: (-olculen[i], i)))
    return dict(indeks=indeks, secildi=indeks == secilen)


def _genis_bolge(izgara, hucreler):
    sekil = _eksen_boyutlari(izgara["eksenler"])
    alan = _secim_alani(sekil, hucreler)
    izinli = {i for i, h in alan.items() if h["durum"] != "alan_disi"}
    olculen = {i: h["toplam_net_r"] for i, h in alan.items() if _olculmus_hucre(h)}
    karli = {i for i, v in olculen.items() if v > 0}
    for i, h in alan.items():
        h.update(_komsu_bilgisi(i, alan, izinli, olculen))
        komsular = list(map(tuple, h["komsular"]))
        h.update(_merkez_bilgisi(i, komsular, sekil, karli, olculen))
    bolgeler = _karli_bolgeler(alan, karli, olculen)
    secilen = _bolge_merkezi(bolgeler, alan)
    return dict(
        secilen=secilen,
        neden=None if secilen is not None else "uygun_merkez_yok",
        en_iyi=_en_iyi_hucre(olculen, secilen),
        hucreler=list(alan.values()),
        bolgeler=bolgeler,
    )


def ema_hucre_calistir(mumlar, p, *, kurulum, sinyal_konumlari, yurutme=None):
    """TASARIM 5.15 S11: her hücrenin gerçek E3 çağrısı ve kendi ayarı."""
    if yurutme is None:
        return motor.Zincir(mumlar, p, kurulum).calistir(sinyal_konumlari)
    if isinstance(yurutme, motor.Zincir):
        ortak = replace(
            p, **{ad: getattr(yurutme.ayar, ad) for ad in IZGARA["ema_sikismasi"]}
        )
        if yurutme.mumlar is not mumlar or ortak != yurutme.ayar:
            raise ValueError("Eski hücre önbelleğinin mum veya çıkış ayarı uyuşmuyor.")
        return yurutme.calistir(sinyal_konumlari, kurulum)
    return motor.tara(mumlar, sinyal_konumlari, p, kurulum, yurutme=yurutme)


IZGARA = {
    "ema_sikismasi": {
        "esik": [0.010, 0.012, 0.015],
        "min_gun": [2, 3, 5],
        "pencere": [5, 10, 20],
    },
    "cift_rotasyonu": {
        "z_pencere": [60, 120],
        "z_esik": [1.5, 2.0, 2.5],
        "p_esik": [0.01, 0.05, 0.10],
    },
}


def _hucre(parametre, tablo) -> dict:
    sonuc = istatistik.olc(tablo, politika="pozitif_fazla_legacy_v1")
    fazla = sonuc["olculer"]["fazla"]["deger"]
    fazla = float("nan") if fazla is None else fazla
    return {
        "hucre": parametre,
        "islem": len(tablo),
        "fazla": fazla,
        "pozitif": bool(fazla > 0),
    }


def oran(hucreler) -> float:
    """Pozitif hücre oranı (bir olasılık değildir; hücreler birbirine bağımlıdır, TASARIM 5.10)."""
    return (
        float(np.mean([h["pozitif"] for h in hucreler])) if hucreler else float("nan")
    )


def ema(anlik, b, p, atr_n, uye, izgara=IZGARA["ema_sikismasi"]) -> list:
    """EMA ızgarası; `b`: `simulator.k1_baglam`, `uye`: `simulator.uyeler`. Mum tablosu ve tek işlem önbelleği hücreler arası paylaşılır."""
    hucreler = [
        dict(zip(izgara, v, strict=True)) for v in itertools.product(*izgara.values())
    ]
    parametreler = [replace(p, **h) for h in hucreler]
    uye_gun = uye.groupby("sembol")["tarih"].agg(list)
    parcalar = [[] for _ in hucreler]
    for s in sorted(uye_gun.index):
        m = motor.mumlar(anlik, s, p, atr_n)
        f, zincir = m.dropna(subset=["kapanis"]), motor.Zincir(m, p)
        for i, pc in enumerate(parametreler):
            sig = aileler.sinyal(f, pc)
            t, _ = ema_hucre_calistir(
                m,
                pc,
                sinyal_konumlari=m.index.get_indexer(sig[sig.isin(uye_gun[s])]),
                kurulum=motor.kurulum_bilgisi(f, pc),
                yurutme=zincir,
            )
            if len(t):
                parcalar[i].append(t.assign(sembol=s))
    bos = motor._tablo([]).assign(sembol=[])
    return [
        _hucre(
            h,
            simulator.k1_islemler(
                pd.concat(x, ignore_index=True) if x else bos, b, MASRAF
            ),
        )
        for h, x in zip(hucreler, parcalar, strict=True)
    ]


def cift(anlik, evr, b, bas, p, izgara=IZGARA["cift_rotasyonu"], h=None) -> list:
    """Çift ızgarası. Eşbütünleşme bir kez, en geniş `p_esik` için hesaplanır; dar `p_esik` hücreleri aynı adaylardan seçer
    (`ciftbolme.setler_sec`); Z penceresi ve eşiği hedefi değiştirir. `h`: en az `max(p_esik)` adaylı `ciftbolme.hazirla` çıktısı."""
    h = h or ciftbolme.hazirla(anlik, evr, bas, p, aday_esik=max(izgara["p_esik"]))
    sonuc = []
    for pe in izgara["p_esik"]:
        setler = ciftbolme.setler_sec(h, replace(p, p_esik=pe))[1]
        for zp, ze in itertools.product(izgara["z_pencere"], izgara["z_esik"]):
            pc = replace(p, p_esik=pe, z_pencere=zp, z_esik=ze)
            hedef = functools.cache(
                lambda y, x, pc=pc: ciftbolme.hedef(h["Kc"], y, x, pc)
            )
            islemler = ciftbolme._rotasyon(
                {**h["M"], "hedef": hedef}, setler, pc.en_fazla, MASRAF
            )[0]
            sonuc.append(
                _hucre(
                    {"z_pencere": zp, "z_esik": ze, "p_esik": pe},
                    istatistik.cift_tablo(islemler, b),
                )
            )
    return sonuc
