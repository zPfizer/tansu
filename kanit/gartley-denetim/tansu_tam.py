"""Tansu-tam Gartley adayı (`kanit/gartley-tansu-kurallari.md` ön kaydı). Motorun Gartley bulucusu, Tansu'nun yazılı
kurallarına göre iki farkla: BC/AB sınırları toleranssız ve kesin, CD/BC iki noktadan birine (1,272 ya da 1,618) tolerans
içinde yakın. Çıkış: stop X dokunuş, hedef1'de %50, hedef2'de kalan; iz stop, açılış stopu ve başabaş yok.
"""

import numpy as np
import pandas as pd

from tansu.stratejiler import gartley

AD = "tg"
P = {
    "pivot": "sag_bar_15",
    "tolerans": 0.05,
    "gecerlilik": 10,
    "stop": "X",
    "rr_min": 1.4,
}
CIKIS = {"tur": "tp12", "acilis_stopu": False}
CD_NOKTA = (1.272, 1.618)


def uyar(ab, bc, cd, tol):
    return (
        abs(ab - gartley.AB_XA) <= tol * gartley.AB_XA
        and gartley.BC_AB[0] < bc < gartley.BC_AB[1]
        and any(abs(cd - n) <= tol * n for n in CD_NOKTA)
    )


def sinyaller(gun: pd.DataFrame) -> pd.DataFrame:
    eski, gartley.uyar = gartley.uyar, uyar
    try:
        s = gartley.STRATEJI.sinyal(gun, P)
    finally:
        gartley.uyar = eski
    s["D"] = s["seviye"]
    s["oruntu_gunu"] = pd.Series(gun.index, gun.index).where(s["giris"])
    return s


def kontrol():
    # BC 0,886 sınırda: motor (tol ile) geçirir, Tansu-tam geçirmez. CD 1,45: motor aralıkta geçirir, iki noktaya uzak.
    assert gartley.uyar(0.618, 0.886, 1.30, 0.05) and not uyar(0.618, 0.886, 1.30, 0.05)
    assert gartley.uyar(0.618, 0.6, 1.45, 0.05) and not uyar(0.618, 0.6, 1.45, 0.05)
    assert uyar(0.618, 0.6, 1.30, 0.05) and uyar(0.618, 0.45, 1.60, 0.05)
    assert np.isclose(
        0.382 * 0.786 / 0.214, 1.403, atol=1e-3
    )  # R/R kapısı 1,4: stop X iken her kurulum geçer
    return "tamam"
