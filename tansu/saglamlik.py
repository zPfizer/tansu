"""Sağlamlık ızgarası: önceden yazılmış hücreler birlikte oynatılır (TASARIM 5.10, KURALLAR §3).

Pozitif hücre: K1'e göre işlem başına ortalama fazla getiri > 0, %0,3 masrafla; p aranmaz, en iyi hücre seçilmez.
Hücre başına sonuç: `{"hucre": parametreler, "islem": n, "fazla": ortalama (işlem yoksa NaN), "pozitif": bool}`.
"""

import functools
import itertools
from dataclasses import replace

import numpy as np
import pandas as pd

from tansu import aileler, ciftbolme, istatistik, motor, simulator

MASRAF = 0.003  # TASARIM 5.10
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
    fazla = istatistik.ortalama_fazla(tablo)
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
            t, _ = zincir.calistir(
                m.index.get_indexer(sig[sig.isin(uye_gun[s])]),
                motor.kurulum_bilgisi(f, pc),
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
