"""Gartley para katmanı: 100.000 TL, bütün BIST, maliyet + kayma, boş nakde gecelik faiz (Levent 29.10.2026).

Sinyal, dolum ve çıkış motordan gelir (`tansu.islem`, `tansu.stratejiler.gartley`); bu betik ayar seçeneklerini ve para
katmanını ekler. Ayar yalnız 2015-2022'de yapılır; 2023-2025 tek kez, dondurulmuş ayar dosyasının SHA-256'sı ile koşar.

Kullanım:
  para.py ayar <gunler.pkl> <faiz.parquet> <ayar.json> <kayıt.tsv> <etiket> [a.b=json ...] -> 2015-2022, kayda bir satır
  para.py test <gunler.pkl> <faiz.parquet> <ayar.json> <çıktı klasörü> -> 2023-2025, yalnız dondurulmuş ayarla, bir kez
  para.py denetim <gunler-2025.pkl> <faiz.parquet>                     -> paper trade 2021-2025 eşitliği
"""

import datetime as dt
import hashlib
import json
import math
import sys
import tempfile
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

from tansu import gostergeler, islem, sinama, strateji, veri, yapi
from tansu.stratejiler import gartley

DONDURULMUS_AYAR_SHA = "118ad754930a67cb70f4ace06de0981142e1a5539dcdfe15ca6e2eb0d43e32e6"  # kanit/gartley-para/ayar.json; başka dosyayla test koşmaz
TEST_KILIDI = Path(tempfile.gettempdir()) / "tansu-gartley-para-20261029" / "test-kilidi.txt"
KOD = {Path(m.__file__).name: m.__file__ for m in (gostergeler, islem, sinama, strateji, veri, yapi, gartley)}
KOD["para.py"] = __file__
KOD_OZETI = {ad: hashlib.sha256(Path(yol).read_bytes()).hexdigest() for ad, yol in sorted(KOD.items())}
IZINLI = {
    "desen": {"pivotlar", "tolerans", "okuma", "gecerlilik", "stop", "rr_min"},
    "cikis": {"tur", "iz_atr", "basabas", "acilis_stopu"},
    "boyut": {"risk", "poz_ust", "toplam_ust", "nakit_yetmezse", "likidite_pay"},
    "nakit": {"faiz", "kesinti"},
    "maliyet": {"komisyon", "kayma_tik", "kayma_en_az"},
}

SERMAYE = 100_000.0
YIL_GUN = 252
AYAR_DONEMI = sinama.Donem(pd.Timestamp("2015-01-01"), pd.Timestamp("2022-12-31"))
YARILAR = (pd.Timestamp("2018-12-31"),)  # 2015-2018 | 2019-2022
TEST_DONEMI = sinama.Donem(pd.Timestamp("2023-01-01"), pd.Timestamp("2025-12-31"))
PAPER_DONEMI = sinama.Donem(sinama.ILK_GIRIS, sinama.KESIM)

_GUNLER: dict[str, pd.DataFrame] = {}
_ACIK_GUN = islem._acik_gun
_UYAR = gartley.uyar


# --- Motor: sembol başına işlem kaydı (işçi süreçte) ---


def _yukle(pkl: str, son: str) -> None:
    global _GUNLER
    _, g = pd.read_pickle(pkl)
    _GUNLER = {s: t.loc[:son] for s, t in g.items() if not t.loc[:son].empty}


def _uyar_mutlak(ab, bc, cd, tol):
    """Oran payının öbür okunuşu: mutlak ± `tol` (az-işlem raporu H2)."""
    return (
        abs(ab - gartley.AB_XA) <= tol
        and gartley.BC_AB[0] - tol <= bc <= gartley.BC_AB[1] + tol
        and gartley.CD_BC[0] - tol <= cd <= gartley.CD_BC[1] + tol
    )


def _cikis_kur(c: dict):
    """Çıkış seçeneği -> (motor Cikis, açık gün sarmalayıcısı). Sarmalayıcı yalnız o günün kapanışına kadar bilinenle
    yarının stopunu kurar; açılış stopun altındaysa çıkış açılıştan olur (gerçek stop emri gibi)."""
    hedef = {
        "tp12": (("hedef1", 0.5), ("hedef2", 0.5)),
        "tp1": (("hedef1", 1.0),),
        "tp2": (("hedef2", 1.0),),
        "iz": (),
        "tp1_iz": (("hedef1", 0.5),),
    }[c["tur"]]
    iz = c.get("iz_atr") if c["tur"] in ("iz", "tp1_iz") else None  # TP seçeneklerinde ayarda kalan iz değeri çalışmaz
    basabas, acilis = c.get("basabas", False), c.get("acilis_stopu", True)

    def acik_gun(e, i, g, cikis):
        if acilis and i > e.dolum_i and not g.taban_kilit[i] and not e.bekleyen and g.aof[i] < e.stop:
            return islem._kapat(e, i, g.aof[i], "stop (açılış)")
        kapandi = _ACIK_GUN(e, i, g, cikis)
        if kapandi:
            return True
        if iz and np.isfinite(g.atr[i]):
            e.stop = max(e.stop, np.nanmax(g.kap[e.dolum_i : i + 1]) - iz * g.atr[i])
        if basabas and any(n == "hedef1" for *_, n in e.parcalar):
            e.stop = max(e.stop, e.giris)
        return False

    return islem.Cikis("dokunus", hedef), acik_gun


def _sembol(arg) -> list[dict]:
    sembol, p, okuma, c, bas, son = arg
    gartley.uyar = _uyar_mutlak if okuma == "mutlak" else _UYAR
    cikis, acik_gun = _cikis_kur(c)
    islem._acik_gun = acik_gun
    gun = _GUNLER[sembol].loc[:son]
    s = gartley.STRATEJI.sinyal(gun, p)
    disarida = (gun.index < bas) | ~gun["uye"]
    s.loc[disarida, ["giris", "tekrar"]] = [False, 0]
    kayit, _ = islem.simule(gun, s, cikis, sembol=sembol, strateji="gartley", sinif="a")
    for k in kayit:  # kayıttaki stop iz süren stopun son hâlidir; boyut sinyal günkü stopla
        k["son_stop"], k["stop"] = k["stop"], s.at[k["sinyal_tarihi"], "stop"]
        taban = islem.RISK_TABANI * gun.at[k["sinyal_tarihi"], "atr"]
        k["risk"] = max(k["dolum_fiyati"] - k["stop"], taban)
        k["risk_emir"] = max(k["seviye"] - k["stop"], taban)  # adet emir verilirken D ile hesaplanır
        k["pivot"] = p["pivot"]
    return kayit


def islemler(pkl: str, ayar: dict, donem: sinama.Donem, onbellek: Path) -> pd.DataFrame:
    """Desen ve çıkış ayarının motor işlemleri; birden çok pivot birleşir. Önbellek anahtarı ayarın ilgili kısmıdır."""
    d, c = ayar["desen"], ayar["cikis"]
    anahtar = hashlib.sha256(
        json.dumps([d, c, str(donem.bas.date()), str(donem.son.date()), pkl, KOD_OZETI], sort_keys=True).encode()
    ).hexdigest()[:16]
    yol = onbellek / f"{anahtar}.pkl"
    if yol.exists():
        return pd.read_pickle(yol)
    son = str(donem.son.date())
    _, g = pd.read_pickle(pkl)
    semboller = sorted(s for s, t in g.items() if not t.loc[:son].empty)
    del g
    parcalar = []
    with Pool(24, initializer=_yukle, initargs=(pkl, son)) as havuz:
        for pivot in d["pivotlar"]:
            p = {
                "pivot": pivot,
                "tolerans": d["tolerans"],
                "gecerlilik": d["gecerlilik"],
                "stop": d["stop"],
                "rr_min": d["rr_min"],
            }
            argl = [(s, p, d.get("okuma", "oran"), c, donem.bas, donem.son) for s in semboller]
            parcalar += [k for liste in havuz.map(_sembol, argl, chunksize=8) for k in liste]
    isl = pd.DataFrame(parcalar)
    if len(isl):
        isl = isl.sort_values(["dolum_tarihi", "sinyal_tarihi", "sembol", "pivot"], kind="stable")
        isl = isl.drop_duplicates(["sembol", "dolum_tarihi", "seviye"]).reset_index(drop=True)
    onbellek.mkdir(parents=True, exist_ok=True)
    isl.to_pickle(yol)
    return isl


# --- Para katmanı ---


def bacaklar(t) -> list[tuple[pd.Timestamp, float, float, str, bool]]:
    """Motor kaydından çıkış parçaları: (gün, fiyat, pay, neden, son mu)."""
    b = []
    if isinstance(t["kismi"], str) and t["kismi"]:
        for parca in t["kismi"].split("; "):
            tarih, ad, fiyat, pay = parca.split()
            b.append((pd.Timestamp(tarih), float(fiyat), float(pay[1:]), ad, False))
    b.append((t["cikis_tarihi"], float(t["cikis_fiyati"]), 1 - sum(x[2] for x in b), t["cikis_nedeni"], True))
    return b


def gunluk_faiz(faiz: pd.DataFrame, takvim: pd.DatetimeIndex, onceki: pd.Timestamp) -> pd.Series:
    """İşlem gününe düşen faiz payı: bir gün gecikmeli politika faizi x önceki işlem gününden bu yana takvim günü / 365
    (paper trade ile aynı yöntem)."""
    oran = faiz.set_index("tarih")["faiz"].sort_index()
    gecen = pd.Series(takvim, takvim).diff().dt.days.fillna((takvim[0] - onceki).days)
    dun = takvim - pd.Timedelta(days=1)
    yuruyen = oran.reindex(oran.index.union(dun)).ffill().reindex(dun).to_numpy()
    return pd.Series(yuruyen / 100 * gecen.to_numpy() / 365, takvim)


class Piyasa:
    """Para katmanının okuduğu günlük diziler: düzeltilmiş kapanış, ham/düzeltilmiş oranı, likidite (dünkü 20 günlük
    ortanca TL hacim). Hepsi o güne kadar bilinen veriden."""

    def __init__(self, gunler: dict, semboller, takvim: pd.DatetimeIndex):
        self.kap, self.oran, self.lik = {}, {}, {}
        for s in semboller:
            g = gunler[s]
            self.kap[s] = g["kapanis"].reindex(takvim).ffill()
            self.oran[s] = (g["ham_kapanis"] / g["kapanis"]).ffill()
            tl = g["hacim"]
            self.lik[s] = tl.rolling(20, min_periods=5).median().shift(1)

    def kayma(self, s: str, gun: pd.Timestamp, fiyat: float, m: dict) -> float:
        """Taraf başına kayma payı: ham fiyatta `kayma_tik` fiyat adımı, en az `kayma_en_az`."""
        ham = fiyat * float(self.oran[s].asof(gun))
        tablo = veri.ADIM_YENI if gun >= veri.ADIM_DEGISIM else veri.ADIM_ESKI
        tik = tablo[np.searchsorted(veri.ADIM_ESIK, ham, side="right")]
        return max(m["kayma_tik"] * tik / ham, m["kayma_en_az"])


def portfoy(isl: pd.DataFrame, piyasa: Piyasa, takvim: pd.DatetimeIndex, rf: pd.Series, ayar: dict):
    """Gün sırası: boş nakde faiz -> girişler (dünkü özkaynakla boyut, gün başı nakit) -> çıkışlar -> kapanış değeri
    (açık pozisyon satış maliyeti ve kayması düşülerek). Kaldıraç yok, tam sayı adet, sembol başına bir pozisyon."""
    b, m, n_ = ayar["boyut"], ayar["maliyet"], ayar["nakit"]
    M = m["komisyon"]
    faiz = rf * (1 - n_["kesinti"]) if n_["faiz"] else rf * 0
    giris, cikis = defaultdict(list), defaultdict(list)
    for k, t in isl.iterrows():
        giris[t["dolum_tarihi"]].append(k)
        for x in bacaklar(t):
            cikis[x[0]].append((k, x))
    nakit = oz = SERMAYE
    adet, kalan, akis, durum, gunluk, faiz_top = {}, {}, defaultdict(float), {}, [], 0.0
    acik_sembol: dict[str, int] = {}
    deger = 0.0
    for g in takvim:
        if nakit > 0:
            faiz_top += nakit * faiz[g]
            nakit *= 1 + faiz[g]
        oz_dun, acik_deger = oz, deger
        for k in sorted(giris.pop(g, []), key=lambda k: (isl.at[k, "sinyal_tarihi"], isl.at[k, "sembol"])):
            s = isl.at[k, "sembol"]
            if s in acik_sembol:
                durum[k] = "atlandı: sembolde açık pozisyon"
                continue
            f = isl.at[k, "dolum_fiyati"]
            f_al = f * (1 + piyasa.kayma(s, g, f, m)) * (1 + M)
            d = isl.at[k, "seviye"]  # adet açılıştan önce, emir fiyatıyla; boşluk dolumu yalnız ödenen tutarı düşürür
            d_al = d * (1 + piyasa.kayma(s, g, d, m)) * (1 + M)
            lik = piyasa.lik[s].get(g, np.nan)
            sinirlar = [
                oz_dun * b["risk"] / isl.at[k, "risk_emir"],
                oz_dun * b["poz_ust"] / d_al,
                (b["toplam_ust"] * oz_dun - acik_deger) / d_al,
            ]
            if b.get("likidite_pay") and np.isfinite(lik):
                sinirlar.append(b["likidite_pay"] * lik / d)
            n = math.floor(max(min(sinirlar), 0))
            if n * d_al > nakit and b["nakit_yetmezse"] == "kucult":
                n = math.floor(nakit / d_al)
            if n < 1:
                durum[k] = "atlandı: adet 0"
            elif n * f_al > nakit:
                durum[k] = "atlandı: nakit yetmedi"
            else:
                nakit -= n * f_al
                akis[k] -= n * f_al
                acik_deger += n * f
                adet[k] = kalan[k] = n
                acik_sembol[s] = k
                durum[k] = "alındı"
        for k, (_, fiyat, pay, _, son) in cikis.pop(g, []):
            if k not in kalan:
                continue
            s = isl.at[k, "sembol"]
            n_b = kalan[k] if son else min(int(adet[k] * pay), kalan[k])
            gelir = n_b * fiyat * (1 - piyasa.kayma(s, g, fiyat, m)) * (1 - M)
            nakit += gelir
            akis[k] += gelir
            kalan[k] -= n_b
            if kalan[k] == 0:
                del kalan[k]
                del acik_sembol[s]
        deger = 0.0
        for k, n in kalan.items():
            s = isl.at[k, "sembol"]
            p = piyasa.kap[s][g]
            deger += n * p * (1 - piyasa.kayma(s, g, p, m)) * (1 - M)
        oz = nakit + deger
        gunluk.append((g, oz, nakit, deger, len(kalan)))
    assert not giris and not cikis, f"takvim dışı olay günü: {sorted(giris)[:3]} {sorted(cikis)[:3]}"
    assert not kalan, "dönem sonunda kapanmamış pozisyon"
    gun = pd.DataFrame(gunluk, columns=["tarih", "ozkaynak", "nakit", "pozisyon", "acik_sayisi"]).set_index("tarih")
    return gun, durum, akis, adet, faiz_top


def dusus(E: pd.Series) -> tuple[float, str, str]:
    d = E / E.cummax() - 1
    dip = d.idxmin()
    return float(d.min() * 100), str(E[:dip].idxmax().date()), str(dip.date())


def olc(gun: pd.DataFrame, durum: dict, akis: dict, faiz_top: float, onceki: pd.Timestamp) -> dict:
    E = pd.concat([pd.Series([SERMAYE], [onceki]), gun["ozkaynak"]])
    yil = (gun.index[-1] - onceki).days / 365.25
    alinan = [k for k, d in durum.items() if d == "alındı"]
    pnl = pd.Series({k: akis[k] for k in alinan}, dtype=float)
    dd, tepe, dip = dusus(E)
    yillik = E.groupby(E.index.year).last().pct_change().dropna() * 100
    son = float(E.iloc[-1])
    return {
        "son": round(son),
        "yillik_bilesik_yuzde": round(((son / SERMAYE) ** (1 / yil) - 1) * 100, 2),
        "en_kotu_dusus_yuzde": round(dd, 2),
        "dusus_tepe": tepe,
        "dusus_dip": dip,
        "islem": len(alinan),
        "kazanan_yuzde": round(float((pnl > 0).mean() * 100), 1) if len(pnl) else None,
        "islem_kari_tl": round(float(pnl.sum())),
        "kaybeden_islemler_tl": round(float(pnl[pnl <= 0].sum())),
        "faiz_geliri_tl": round(faiz_top),
        "atlanan": dict(pd.Series([d for d in durum.values() if d != "alındı"], dtype=str).value_counts()),
        "acik_gun_payi_yuzde": round(float((gun["acik_sayisi"] > 0).mean() * 100), 1),
        "ort_hissede_pay_yuzde": round(float((gun["pozisyon"] / gun["ozkaynak"]).mean() * 100), 1),
        "yillik_getiri_yuzde": {int(y): round(float(v), 2) for y, v in yillik.sort_index().items()},
    }


def kiyaslar(xu: pd.Series, rf: pd.Series, takvim: pd.DatetimeIndex) -> dict:
    """Paper trade ile aynı: BIST 100 fiyat endeksi al-tut ve brüt politika faizi."""
    onceki = xu[xu.index < takvim[0]].iloc[-1]
    x = SERMAYE * xu.reindex(takvim).ffill() / onceki
    f = SERMAYE * (1 + rf).cumprod()
    return {
        "xu100_son": round(float(x.iloc[-1])),
        "faiz_son": round(float(f.iloc[-1])),
        "xu100_dusus_yuzde": round(dusus(pd.concat([pd.Series([SERMAYE], [takvim[0] - pd.Timedelta(days=1)]), x]))[0], 2),
    }


def xu100(gunler: dict) -> pd.Series:
    x = pd.concat([g["xu100"] for g in gunler.values()])
    return x[x > 0].groupby(level=0).first().sort_index()


def kos(pkl: str, faiz_yol: str, ayar: dict, donem: sinama.Donem, onbellek: Path):
    isl = islemler(pkl, ayar, donem, onbellek)
    _, gunler = pd.read_pickle(pkl)
    gunler = {s: t.loc[: donem.son] for s, t in gunler.items()}
    xu = xu100(gunler)
    takvim = xu.index[(xu.index >= donem.bas) & (xu.index <= donem.son)]
    onceki = xu.index[xu.index < takvim[0]][-1]
    rf = gunluk_faiz(pd.read_parquet(faiz_yol), takvim, onceki)
    piyasa = Piyasa(gunler, isl["sembol"].unique() if len(isl) else [], takvim)
    gun, durum, akis, adet, faiz_top = portfoy(isl, piyasa, takvim, rf, ayar)
    sonuc = olc(gun, durum, akis, faiz_top, onceki)
    sonuc["motor"] = {
        "dolum": len(isl),
        "ortalama_R": round(float(isl["R"].mean()), 3) if len(isl) else None,
        "toplam_R": round(float(isl["R"].sum()), 2) if len(isl) else 0,
    }
    sonuc["kiyas"] = kiyaslar(xu, rf, takvim)
    return sonuc, gun, isl, durum, akis, adet


def denetle(ayar: dict) -> dict:
    """Bilinmeyen bölüm ya da alan (yazım hatası) koşuyu durdurur; `kayit` bölümü yalnız açıklamadır."""
    for bolum, alanlar in ayar.items():
        if bolum == "kayit":
            continue
        fazla = set(alanlar) - IZINLI.get(bolum, set())
        if bolum not in IZINLI or fazla:
            raise SystemExit(f"bilinmeyen ayar: {bolum} {sorted(fazla)}")
    return ayar


def ayar_oku(yol: str) -> dict:
    return denetle(json.loads(Path(yol).read_text(encoding="utf-8")))


if __name__ == "__main__":
    mod = sys.argv[1]
    if mod == "ayar":
        pkl, faiz_yol, ayar_yol, kayit, etiket = sys.argv[2:7]
        ayar = ayar_oku(ayar_yol)
        for degis in sys.argv[7:]:  # "boyut.risk=0.02": ayar dosyası üstüne tek koşuluk değişiklik
            yol, deger = degis.split("=", 1)
            *ust, ad = yol.split(".")
            hedef = ayar
            for u in ust:
                hedef = hedef[u]
            hedef[ad] = json.loads(deger)
        denetle(ayar)
        s, gun, *_ = kos(pkl, faiz_yol, ayar, AYAR_DONEMI, Path(pkl).parent / "onbellek-islem")
        E = gun["ozkaynak"]
        s["yari_2015_2018"] = round(float(E[: YARILAR[0]].iloc[-1]))
        s["yari_2019_2022_carpan"] = round(float(E.iloc[-1] / E[: YARILAR[0]].iloc[-1]), 3)
        print(json.dumps({"etiket": etiket, **s}, ensure_ascii=False, default=str))
        yeni = not Path(kayit).exists()
        with open(kayit, "a", encoding="utf-8") as f:
            if yeni:
                f.write("etiket\tson\tdusus\tislem\tort_R\tdolum\t2015-2018\t2019-2022_carpan\tfaiz\txu100\tayar\n")
            f.write(
                f"{etiket}\t{s['son']}\t{s['en_kotu_dusus_yuzde']}\t{s['islem']}\t{s['motor']['ortalama_R']}\t"
                f"{s['motor']['dolum']}\t{s['yari_2015_2018']}\t{s['yari_2019_2022_carpan']}\t{s['kiyas']['faiz_son']}\t"
                f"{s['kiyas']['xu100_son']}\t{json.dumps(ayar, sort_keys=True)}\n"
            )
    elif mod == "test":
        pkl, faiz_yol, ayar_yol, cikti = sys.argv[2:6]
        sha = hashlib.sha256(Path(ayar_yol).read_bytes()).hexdigest()
        if DONDURULMUS_AYAR_SHA is None or sha != DONDURULMUS_AYAR_SHA:
            raise SystemExit(f"ayar dosyası dondurulmuş dosya değil: {sha} != {DONDURULMUS_AYAR_SHA}")
        TEST_KILIDI.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(TEST_KILIDI, "x", encoding="utf-8") as f:  # yoksa yaratır; varsa hata: ikinci koşu yok
                f.write(json.dumps({"ayar_sha256": sha, "kod": KOD_OZETI, "bas": str(dt.datetime.now())}, indent=1))
        except FileExistsError:
            raise SystemExit(f"2023-2025 testi zaten koştu ({TEST_KILIDI}); ikinci koşu yok") from None
        cikti = Path(cikti)
        cikti.mkdir(parents=True, exist_ok=True)
        ayar = ayar_oku(ayar_yol)
        s, gun, isl, durum, akis, adet = kos(pkl, faiz_yol, ayar, TEST_DONEMI, cikti / "onbellek-islem")
        s["ayar_sha256"], s["kod_sha256"] = sha, KOD_OZETI
        (cikti / "test-sonuc.json").write_text(json.dumps(s, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        gun.to_csv(cikti / "test-gunluk-kasa.csv", encoding="utf-8", float_format="%.2f")
        isl.assign(
            durum=[durum.get(k, "") for k in isl.index],
            adet=[adet.get(k, 0) for k in isl.index],
            kar_tl=[round(akis[k], 2) if k in adet else None for k in isl.index],
        ).to_csv(cikti / "test-islemler.csv", index=False, encoding="utf-8")
        print(json.dumps(s, ensure_ascii=False, indent=1, default=str))
    elif mod == "denetim":
        pkl, faiz_yol = sys.argv[2:4]
        ayar = {
            "desen": {"pivotlar": ["sag_bar_10"], "tolerans": 0.04, "gecerlilik": 5, "stop": "X", "rr_min": 1.4},
            "cikis": {"tur": "tp12", "acilis_stopu": False},
            "boyut": {"risk": 0.01, "poz_ust": 1e9, "toplam_ust": 1e9, "nakit_yetmezse": "atla"},
            "nakit": {"faiz": False, "kesinti": 0.0},
            "maliyet": {"komisyon": islem.MALIYET, "kayma_tik": 0, "kayma_en_az": 0.0},
        }
        s, *_ = kos(pkl, faiz_yol, ayar, PAPER_DONEMI, Path(pkl).parent.parent / "onbellek-denetim")
        print(json.dumps(s, ensure_ascii=False, default=str))
