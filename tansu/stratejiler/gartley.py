"""Gartley, boğa (SPEC 11 madde 1). Kural, kaynaklar ve çatışmalar yerel kartta: `stratejiler/gartley.md`."""

from collections.abc import Mapping

import numpy as np
import pandas as pd

from tansu import gostergeler, yapi
from tansu.islem import Cikis
from tansu.strateji import Strateji, bos_sinyal

AB_XA = 0.618
BC_AB = (0.382, 0.886)
CD_BC = (1.272, 1.618)
D_XA = 0.786  # D = A - 0.786 x (A - X)
HEDEF_ORAN = (0.382, 0.618)  # A-D hareketinin payı


def _pivotlar(gun: pd.DataFrame, p) -> list[yapi.Pivot]:
    """`pivot` = "<mod>_<değer>": tek eksen, böylece etkisiz eksen ızgarada aynı noktaları çoğaltmaz (SPEC 5.7)."""
    mod, deger = str(p["pivot"]).rsplit("_", 1)
    if mod == "sag_bar":
        return yapi.sag_bar_pivotlari(gun["yuksek"], gun["dusuk"], int(deger))
    if mod == "zigzag":
        return yapi.zigzag_pivotlari(gun["yuksek"], gun["dusuk"], float(deger))
    raise ValueError(f"bilinmeyen pivot: {p['pivot']}")


def oranlar(
    x: float, a: float, b: float, c: float
) -> tuple[float, float, float, float]:
    """(AB/XA, BC/AB, CD/BC, D) boğa XABC için."""
    d = a - D_XA * (a - x)
    return (a - b) / (a - x), (c - b) / (a - b), (c - d) / (c - b), d


def uyar(ab: float, bc: float, cd: float, tol: float) -> bool:
    """Carney oranları, oranın `tol` payı içinde (SPEC 11 madde 1)."""
    return (
        abs(ab - AB_XA) <= tol * AB_XA
        and BC_AB[0] * (1 - tol) <= bc <= BC_AB[1] * (1 + tol)
        and CD_BC[0] * (1 - tol) <= cd <= CD_BC[1] * (1 + tol)
    )


def hesapla(gun: pd.DataFrame, p: Mapping[str, float | str]) -> pd.DataFrame:
    s = bos_sinyal(gun.index)
    atr = gostergeler.atr_basit(gun["yuksek"], gun["dusuk"], gun["kapanis"]).to_numpy()
    dusuk = gun["dusuk"].to_numpy(float)
    tarih = gun.index
    tol = float(p["tolerans"])
    for sira in yapi.ardisik(_pivotlar(gun, p)):
        if len(sira) < 4:
            continue
        X, A, B, C = sira[-4:]
        tur = (X.tur, A.tur, B.tur, C.tur)
        if tur != ("D", "T", "D", "T") or not X.fiyat < B.fiyat < C.fiyat < A.fiyat:
            continue
        ab, bc, cd, d = oranlar(X.fiyat, A.fiyat, B.fiyat, C.fiyat)
        if not uyar(ab, bc, cd, tol):
            continue
        t = C.onay_gun
        sonra = dusuk[C.pivot_gun + 1 : t + 1]
        en_dusuk = np.nanmin(sonra) if np.isfinite(sonra).any() else np.inf
        if en_dusuk <= X.fiyat:  # BOZULDU: onaydan önce X kırıldı
            continue
        stop = X.fiyat if p["stop"] == "X" else X.fiyat - 2 * atr[t]
        h1, h2 = (d + r * (A.fiyat - d) for r in HEDEF_ORAN)
        if p["rr_min"] != "kapali" and (h1 - d) / (d - stop) < float(p["rr_min"]):
            continue
        if s.iat[t, s.columns.get_loc("giris")]:
            s.iat[t, s.columns.get_loc("tekrar")] += 1
            if d <= s.iat[t, s.columns.get_loc("seviye")]:
                continue
        nokta = ", ".join(
            f"{ad} {q.fiyat:.2f} ({tarih[q.pivot_gun].date()})"
            for ad, q in zip("XABC", (X, A, B, C), strict=True)
        )
        s.loc[tarih[t], ["giris", "giris_tur", "seviye", "gecerlilik", "stop"]] = [
            True,
            "limit",
            d,
            int(p["gecerlilik"]),
            stop,
        ]
        s.loc[tarih[t], ["hedef1", "hedef2", "hedef3"]] = [h1, h2, C.fiyat]
        s.loc[tarih[t], "durum"] = "TAMAMLANDI" if en_dusuk <= d else "AKTIF"
        s.loc[tarih[t], "kural_durumu"] = (
            f"{nokta}; AB/XA {ab:.3f}, BC/AB {bc:.3f}, CD/BC {cd:.3f}"
        )
    return s


STRATEJI = Strateji(
    ad="gartley",
    tur="giris",
    sinif="a",
    zaman="gunluk",
    kaynaklar=("stratejiler/gartley.md",),
    kaynak_tarihleri=("2025-12-02", "2025-12-13", "2026-08-20", "2026-08-23"),
    varsayilan={
        "pivot": "sag_bar_15",
        "tolerans": 0.05,
        "gecerlilik": 10,
        "stop": "X",
        "rr_min": 1.4,  # Ek B #13: stop X iken hedef1 oranı 1.403; 1.403 üstü her kurulumu eler
    },
    aralik={
        "pivot": ("sag_bar_10", "sag_bar_12", "sag_bar_15", "sag_bar_20"),
        "tolerans": (0.03, 0.04, 0.05),
        "gecerlilik": (5, 10, 20),
        "stop": ("X",),  # X-2ATR hesapla'da kalır; kapı 1.4 onu her kurulumda eler
    },
    seviye_param=("stop",),
    cikis=Cikis("dokunus", (("hedef1", 0.5), ("hedef2", 0.5))),
    hesapla=hesapla,
)
