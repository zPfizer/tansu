"""Motor: saf Adım fonksiyonu ve sinyallerden işlem listesi (TASARIM 5.3, 5.5).

Fiyatlar düzeltilmiş seriden; kilit ve karantina bayrakları ham seriden gelir (`veri.Anlik.gun_tablosu`).
Mum: tarih, aof, yuksek, dusuk, kapanis, sma250, atr, islem, karantina, kilit_tavan, kilit_taban.
"""

from dataclasses import dataclass, replace

import pandas as pd

from tansu import aileler, gostergeler

STOP_ATR = 2.0  # TASARIM 5.5: acil stop = giriş - 2 ATR
KARANTINA_GUN = 250  # TASARIM 5.1: karantinadan sonra yeni sinyal yok
ATR_N = 14


@dataclass(frozen=True)
class Pozisyon:
    durum: str  # bekliyor | acik | kapali
    atr: float = 0.0  # sinyal günü ATR
    sinyal_tarih: object = None  # simülatör evren ve likidite için sinyal gününe bakar
    adet: int = 1  # boyutlandırma bilet 10'dadır
    giris_tarih: object = None
    giris_fiyat: float = None
    stop: float = None
    bekleyen: str = None  # dolmamış çıkışın nedeni
    son_aof: float = None  # son temiz AOF (karantina çıkışı için)
    cikis_tarih: object = None
    cikis_fiyat: float = None
    neden: str = None  # kapalıysa: stop | sma250 | karantina | veri_sonu | iptal


def bekleyen(atr: float, sinyal_tarih=None) -> Pozisyon:
    """Sinyal günü kapanışında oluşan, ertesi gün girecek pozisyon."""
    return Pozisyon("bekliyor", atr=atr, sinyal_tarih=sinyal_tarih)


def _kapat(p, tarih, fiyat, neden):
    return replace(p, durum="kapali", cikis_tarih=tarih, cikis_fiyat=fiyat, neden=neden)


def adim(p: Pozisyon, m) -> Pozisyon:
    """(pozisyon, bugünkü mum) → pozisyon. Saf; kurallar TASARIM 5.3'te."""
    if p.durum == "kapali":
        return p
    if p.durum == "bekliyor":
        if m["karantina"] or not m["islem"] or m["kilit_tavan"]:
            return _kapat(p, m["tarih"], None, "iptal")
        p = replace(p, durum="acik", giris_tarih=m["tarih"], giris_fiyat=m["aof"],
                    stop=m["aof"] - STOP_ATR * p.atr)
        ilk_gun = True
    else:
        ilk_gun = False
        if m["karantina"]:
            return _kapat(p, m["tarih"], p.son_aof, "karantina")
        if not m["islem"]:
            return p
    p = replace(p, son_aof=m["aof"])
    if m["dusuk"] <= p.stop:
        if m["kilit_taban"]:
            return replace(p, bekleyen="stop")
        return _kapat(p, m["tarih"], min(p.stop, m["aof"]), "stop")
    if p.bekleyen:
        return p if m["kilit_taban"] else _kapat(p, m["tarih"], m["aof"], p.bekleyen)
    if not ilk_gun and m["kapanis"] < m["sma250"]:
        return replace(p, bekleyen="sma250")
    return p


def islemler(mumlar: pd.DataFrame, sinyaller) -> tuple:
    """Tek hissenin mumları (tarih indeksli) ve sinyal günlerinden (işlem listesi, düşen sinyal sayısı)."""
    sinyaller = set(sinyaller)
    kapali, dusen, p, son_karantina = [], 0, None, None
    for i, (tarih, satir) in enumerate(mumlar.iterrows()):
        m = {**satir.to_dict(), "tarih": tarih}
        if p is not None:
            p = adim(p, m)
            if p.durum == "kapali":
                dusen += p.neden == "iptal"
                if p.neden != "iptal":
                    kapali.append(p)
                p = None
        if m["karantina"]:
            son_karantina = i
        engelli = son_karantina is not None and i - son_karantina < KARANTINA_GUN
        if p is None and tarih in sinyaller and not engelli:
            p = bekleyen(m["atr"], tarih)
    if p is not None and p.durum == "bekliyor":
        dusen += 1  # sinyalden sonra veri yok
    elif p is not None:
        gecerli = mumlar["kapanis"].dropna()
        kapali.append(_kapat(p, gecerli.index[-1], gecerli.iloc[-1], "veri_sonu"))
    return _tablo(kapali), dusen


def _tablo(pozisyonlar) -> pd.DataFrame:
    return pd.DataFrame([{
        "sinyal_tarih": p.sinyal_tarih, "giris_tarih": p.giris_tarih, "giris_fiyat": p.giris_fiyat, "cikis_tarih": p.cikis_tarih,
        "cikis_fiyat": p.cikis_fiyat, "neden": p.neden, "adet": p.adet,
        "planlanan_risk": p.adet * (p.giris_fiyat - p.stop),
        "gerceklesen_kayip": p.adet * max(0.0, p.giris_fiyat - p.cikis_fiyat)} for p in pozisyonlar],
        columns=["sinyal_tarih", "giris_tarih", "giris_fiyat", "cikis_tarih", "cikis_fiyat", "neden", "adet",
                 "planlanan_risk", "gerceklesen_kayip"])


def mumlar(anlik, sembol: str, p: aileler.Parametre = aileler.Parametre(), atr_n: int = ATR_N) -> pd.DataFrame:
    """Bir sembolün mum tablosu: düzeltilmiş fiyat + gösterge + ham seriden kilit/karantina (gun_tablosu)."""
    f = anlik.fiyat[anlik.fiyat["sembol"] == sembol].sort_values("tarih").set_index("tarih")
    g = anlik.gun_tablosu
    g = g[g["sembol"] == sembol].set_index("tarih")
    m = f[["aof", "yuksek", "dusuk", "kapanis"]].reindex(g.index)  # eksik gün NaN kalır
    m["sma250"] = gostergeler.sma(m["kapanis"], p.sma_n)
    m["atr"] = gostergeler.atr(m["yuksek"], m["dusuk"], m["kapanis"], atr_n)
    for ad in ("islem", "karantina", "kilit_tavan", "kilit_taban"):
        m[ad] = g[ad].astype(bool)
    return m


def sinama(anlik, p: aileler.Parametre = aileler.Parametre(), atr_n: int = ATR_N) -> tuple:
    """Anlık görüntünün bütün sembolleri için (işlem listesi, düşen sinyal sayısı)."""
    parcalar, dusen = [], 0
    for s in anlik.fiyat["sembol"].unique():
        m = mumlar(anlik, s, p, atr_n)
        sig = aileler.sinyal(m.dropna(subset=["kapanis"]), p)
        t, d = islemler(m, sig)
        if len(t):  # boş tablolar sütun türünü object'e bozar
            parcalar.append(t.assign(sembol=s))
        dusen += d
    return (pd.concat(parcalar, ignore_index=True) if parcalar else _tablo([]).assign(sembol=[])), dusen
