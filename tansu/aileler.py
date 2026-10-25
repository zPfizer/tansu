"""Aileler: EMA sıkışması kırılım sinyali ve kurulum bilgisi (KURALLAR §3 madde 2 ve "Modül 1"; TASARIM 5.1 ısınma, 5.3 SMA250 şartı)."""

from dataclasses import asdict
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from tansu import gostergeler

from tansu.katalog import (
    ATR_N,
    BOLGE_GUN,
    DUSUS_ATR,
    DUSUS_GUN,
    HACIM_GUN,
    KIRILIM_GUN,
    RETEST_GUN,
    STOP_KAT as _KATALOG_STOP_KAT,
    TREND_GUN,
    YAKIN,
    Parametre as Parametre,
    SECENEKLER as SECENEKLER,
    eski_parametreler,
    legacy_coz as legacy_coz,
)

VARYANTLAR = eski_parametreler()
STOP_KAT = dict(_KATALOG_STOP_KAT)


def ortak_kurulum(veri_paketi, tarih, strateji):
    """E1 ve çözülmüş stratejiden günün EMA kayıtları (TASARIM 5.15)."""
    p = _ortak_ayar(strateji)
    tarih = pd.Timestamp(tarih)
    donem = veri_paketi["referans"]["istenen_donem"]
    if not pd.Timestamp(donem["baslangic"]) <= tarih <= pd.Timestamp(donem["bitis"]):
        raise ValueError("Değerlendirme tarihi istenen dönemin dışında")
    meta = _kurulum_meta(veri_paketi, strateji)
    sonuc = {"gostergeler": [], "sinyaller": [], "isinma": {}}
    for s in veri_paketi["semboller"]:
        f = _piyasa_mumlari(veri_paketi["piyasa"], s, tarih)
        temiz = f.dropna(subset=["kapanis"])
        sonuc["isinma"][s] = {
            "gozlem": len(temiz),
            "gerekli": p.isinma,
            "tamam": len(temiz) >= p.isinma,
        }
        if tarih not in f.index:
            continue
        g = _ortak_gostergeler(f, p)
        for ad in g:
            sonuc["gostergeler"].append(
                {
                    **meta,
                    "kayit_id": f"{s}:{tarih.date()}:{ad}:{strateji.ayar_parmak_izi}",
                    "kayit_turu": "gosterge",
                    "sembol": s,
                    "tarih": str(tarih.date()),
                    "ad": ad,
                    **gostergeler.deger_kaydi(
                        g.at[tarih, ad],
                        "birimsiz"
                        if ad
                        in ("rsi", "adx", "stokastik_k", "stokastik_d", "sikisma_orani")
                        else "TL/adet",
                        "eksik_veri"
                        if f.loc[:tarih, ["kapanis", "yuksek", "dusuk"]]
                        .isna()
                        .any()
                        .any()
                        else "isinma_veya_tanimsiz",
                    ),
                }
            )
        for i, (t, satir) in enumerate(kurulum(temiz, p).iterrows()):
            if t == tarih:
                sonuc["sinyaller"].append(
                    _sinyal_kaydi(s, t, i, satir, g.at[t, "atr"], p, strateji, meta)
                )
    return sonuc


def _ortak_ayar(strateji):
    beklenen = legacy_coz(
        strateji.varyant,
        strateji.katalog_surumu,
        sayisal_ayarlar={
            a.ad: a.deger for a in strateji.parametreler if a.koken == "legacy_izgara"
        },
    )
    if any(
        getattr(strateji, a) != getattr(beklenen, a)
        for a in (
            "aile",
            "parametreler",
            "sabitler",
            "gosterge_ayarlari",
            "ayar_parmak_izi",
            "dolum_surumu",
            "risk_surumu",
            "masraf_surumu",
            "muhasebe_surumu",
            "donem_surumu",
        )
    ):
        raise ValueError("Çözülmüş strateji katalogla uyuşmuyor")
    return Parametre(**{a.ad: a.deger for a in strateji.parametreler})


def _kurulum_meta(veri_paketi, strateji):
    return {
        "sema_surumu": "kurulum_s06_v1",
        "olusturma_zamani": datetime.now(timezone.utc).isoformat(),
        "kaynaklar": [asdict(k) for k in strateji.kaynaklar],
        "baglar": {
            "deneme_id": None,
            "kosu_id": None,
            "ayar_parmak_izi": strateji.ayar_parmak_izi,
            "politika_surumu": strateji.risk_surumu,
            "veri_ref_id": veri_paketi["referans"]["kayit_id"],
            "bos_nedenleri": {
                "deneme_id": "hesap_onizlemesi",
                "kosu_id": "hesap_onizlemesi",
            },
        },
    }


def ortak_donem_kurulumu(veri_paketi, strateji):
    """TASARIM 5.15 S10: her sembol/dönemde ortak E2 hesabını bir kez kur."""
    p = _ortak_ayar(strateji)
    donem = veri_paketi["referans"]["istenen_donem"]
    bas, son = pd.Timestamp(donem["baslangic"]), pd.Timestamp(donem["bitis"])
    if pd.isna(bas) or pd.isna(son) or bas > son:
        raise ValueError("Kurulum dönemi geçersiz")
    meta = _kurulum_meta(veri_paketi, strateji)
    sonuc = {}
    for sembol in veri_paketi["semboller"]:
        f = _piyasa_mumlari(veri_paketi["piyasa"], sembol, son)
        g = _ortak_gostergeler(f, p)
        k = kurulum(f.dropna(subset=["kapanis"]), p)
        sonuc[sembol] = dict(
            mumlar=f.join(g),
            kurulum=k.loc[(k.index >= bas) & (k.index <= son)],
            isinma=f.kapanis.notna().cumsum(),
            sinyaller=[
                _sinyal_kaydi(sembol, t, i, r, g.at[t, "atr"], p, strateji, meta)
                for i, (t, r) in enumerate(k.iterrows())
                if bas <= t <= son
            ],
        )
    return sonuc


def _piyasa_mumlari(satirlar, sembol, tarih):
    satirlar = [
        r
        for r in satirlar
        if r["sembol"] == sembol and pd.Timestamp(r["tarih"]) <= tarih
    ]
    indeks = pd.DatetimeIndex([r["tarih"] for r in satirlar])
    if not indeks.is_monotonic_increasing or indeks.has_duplicates:
        raise ValueError("Piyasa tarihleri sıralı ve tekil olmalı")
    f = pd.DataFrame(
        {
            ad: [r[f"duzeltilmis_{ad}"]["deger"] for r in satirlar]
            for ad in ("kapanis", "yuksek", "dusuk", "aof")
        },
        index=indeks,
        dtype=float,
    )
    f["hacim"] = [r["hacim_tl"]["deger"] for r in satirlar]
    f.loc[["eksik" in r["kalite_bayraklari"] for r in satirlar], :] = (
        np.nan
    )  # TASARIM 5.13
    return f


def _ortak_gostergeler(f, p):
    g = gostergeler.tablo(f, p.sma_n, ATR_N)
    k, y, d = f["kapanis"], f["yuksek"], f["dusuk"]
    for n in p.periyotlar:
        g[f"ema{n}"] = gostergeler.ema(k, n)
    g["sikisma_orani"] = gostergeler.sikisma_orani(k, p.periyotlar)
    g["momentum"] = gostergeler.momentum_squeeze(y, d, k)
    g["macd_histogram"] = gostergeler.macd_histogram(k)
    g["adx"] = gostergeler.adx(y, d, k)
    g["psar"] = gostergeler.psar(y, d)
    g["stokastik_k"], g["stokastik_d"] = gostergeler.stokastik(y, d, k)
    return g


def _sinyal_kaydi(sembol, tarih, sira, satir, atr, p, strateji, meta):
    deger = gostergeler.deger_kaydi
    stop = satir.kutu_alt if p.stop == "kutu" else None
    girdiler = [
        asdict(a) for a in strateji.parametreler if a.ad in ("stop", "cikis", "rr_min")
    ]
    girdiler += [
        {
            "ad": "atr",
            "tur": "sayi",
            "kaynaklar": meta["kaynaklar"],
            **deger(atr, "TL/adet"),
        },
        {
            "ad": "stop_kati",
            "tur": "sayi",
            "kaynaklar": meta["kaynaklar"],
            **deger(STOP_KAT.get(p.stop), "ATR", "kutu_stopu"),
        },
    ]
    return {
        **meta,
        "kayit_id": f"{sembol}:{tarih.date()}:{sira}:{strateji.ayar_parmak_izi}",
        "kayit_turu": "sinyal",
        "semboller": [sembol],
        "tarih": str(tarih.date()),
        "strateji_id": strateji.kayit_id,
        "aile": strateji.aile,
        "varyant": strateji.varyant,
        "katalog_surumu": strateji.katalog_surumu,
        "yon": "al",
        "aday_durumu": "legacy_sinyal",
        "kutu_alt": deger(satir.kutu_alt, "TL/adet"),
        "kutu_ust": deger(satir.kutu_ust, "TL/adet"),
        "hedef": deger(
            satir.hedef,
            "TL/adet",
            "uygulanmaz" if p.hedef == "yok" else "hedef_bulunamadi",
        ),
        "ilk_stop": deger(stop, "TL/adet", "dolum_bekleniyor"),
        "kurulum_girdileri": girdiler,
        "kural_kaniti": meta["kaynaklar"],
    }


def _kosu_basi(f: pd.DataFrame, p: Parametre) -> np.ndarray:
    """Agresif giriş için: t günü, t-1'de biten sıkışma koşusunun ilk günü (konum); koşu yoksa ya da `min_gun` günden kısaysa -1."""
    sikisik = (
        gostergeler.sikisma_orani(f["kapanis"], p.periyotlar) <= p.esik
    ).to_numpy()
    basi, bas = np.full(len(f), -1), -1
    for t in range(1, len(f)):
        bas = (bas if bas >= 0 else t - 1) if sikisik[t - 1] else -1
        if bas >= 0 and t - bas >= p.min_gun:
            basi[t] = bas
    return basi


def pencere_gunleri(f: pd.DataFrame, p: Parametre = Parametre()) -> np.ndarray:
    """Giriş penceresi açık günler (bool, `f` sırasında). Sıkışma dönemi bitmiş, `pencere` gün (`arz` ve `ucgen` de `kutu` gibi); `retest` için `RETEST_GUN` gün daha. `agresif` için pencere yoktur: t-1'de biten koşu en az `min_gun` gündür."""
    if p.giris == "agresif":
        return _kosu_basi(f, p) >= 0
    oran = gostergeler.sikisma_orani(f["kapanis"], p.periyotlar)
    acik = np.zeros(len(f), dtype=bool)
    uzun = p.pencere + (RETEST_GUN if p.giris == "retest" else 0)
    for d in gostergeler.sikisma_donemleri(oran, p.esik, p.min_gun):
        bit = f.index.get_loc(d["bit"])
        acik[bit + 1 : bit + 1 + uzun] = True
    return acik


def uygun_gunler(f, p) -> np.ndarray:
    """Kapanış ≥ SMA250 (NaN ise yanlış) ve ısınma tamam."""
    return (f["kapanis"] >= gostergeler.sma(f["kapanis"], p.sma_n)).to_numpy() & (
        np.arange(len(f)) + 1 >= p.isinma
    )


def on_sart(f: pd.DataFrame, p: Parametre = Parametre()) -> np.ndarray:
    """K1 ön şartlı günler (KURALLAR §3 madde 2): pencere açık (`pencere_gunleri`), SMA250 üstü, ısınma tamam. Her giriş türünde gerçek sinyal günleri bunun parçasıdır."""
    return pencere_gunleri(f, p) & uygun_gunler(f, p)


def sikismasiz_kirilim(
    f: pd.DataFrame, p: Parametre = Parametre(), gun: int = KIRILIM_GUN
) -> np.ndarray:
    """K1 ek kolu: kapanış önceki `gun` günün en yüksek yükseğinin üstünde, sıkışma penceresinde değil."""
    onceki = f["yuksek"].shift(1).rolling(gun).max()
    return (
        (f["kapanis"] > onceki).to_numpy() & uygun_gunler(f, p) & ~pencere_gunleri(f, p)
    )


def _salinim(x: np.ndarray, tepe: bool) -> np.ndarray:
    """Salınım noktaları (pencere 2). Tepe: x[i] >= iki yanındaki ikişer günün değerlerinin hepsi. Dip: x[i] <= iki yanındaki ikişer günün değerlerinin hepsi. i+2 gününde bilinir."""
    s = np.zeros(len(x), dtype=bool)
    if len(x) >= 5:
        yan = np.stack([x[:-4], x[1:-3], x[3:-1], x[4:]])
        s[2:-2] = (x[2:-2] >= yan.max(0)) if tepe else (x[2:-2] <= yan.min(0))
    return s


def _dogru(x: np.ndarray, a, u: int) -> float:
    """İki salınım noktasından (konumlar `a`) geçen doğrunun `u` konumundaki değeri."""
    return x[a[1]] + (x[a[1]] - x[a[0]]) / (a[1] - a[0]) * (u - a[1])


def _ucgen(yuksek: np.ndarray, dusuk: np.ndarray):
    """Üçgen (KURALLAR §3 Modül 1, Üçgen hedefi maddesi): dönem içi salınım tepe ve dip konumları `(tepe, dip)`; üçgen yoksa None."""
    tepe, dip = (
        np.flatnonzero(_salinim(yuksek, True)),
        np.flatnonzero(_salinim(dusuk, False)),
    )
    if (
        len(tepe) < 2
        or len(dip) < 3
        or (yuksek[tepe[1:]] > yuksek[tepe[0]] * YAKIN).any()
        or (np.diff(dusuk[dip]) <= 0).any()
    ):
        return None
    return tepe, dip


def _ucgen_hedef(yuksek: np.ndarray, dusuk: np.ndarray) -> float:
    """Üçgen hedefi (KURALLAR §3 Modül 1): dönem içi tepe ve diplerden; üçgen yoksa NaN."""
    u = _ucgen(yuksek, dusuk)
    if u is None:
        return np.nan
    tepe, dip = yuksek[u[0]], dusuk[u[1]]
    return tepe.max() + (tepe[0] - dip[0])


def _trend_teyit(t, kap, yuk, dus, tepe, dip) -> bool:
    """Trend teyidi (KURALLAR §3 Modül 1): düşen trend kırılımı ya da yükselen trende temas ve tepki. `tepe`, `dip`: salınım konumları; yalnız i+2 <= t olanlar bilinir."""
    a = tepe[tepe <= t - 2][-2:]
    if len(a) == 2 and yuk[a[1]] < yuk[a[0]] and _dogru(yuk, a, t) < kap[t]:
        return True
    b = dip[dip <= t - 2][-2:]
    if len(b) == 2 and dus[b[1]] > dus[b[0]]:
        for u in range(max(t - TREND_GUN, 0), t + 1):
            d = _dogru(dus, b, u)
            if dus[u] <= d * YAKIN and kap[u] >= d and kap[t] > kap[u]:
                return True
    return False


def _bolge_listesi(f: pd.DataFrame, yon: str) -> list:
    """Bölgeler `(b, bilinen gün, bozulma günü, proximal, distal)`, tam sayı konumlarıyla; bozulma yoksa bozulma günü `len(f)`."""
    kap, yuk, dus = (f[s].to_numpy(float) for s in ("kapanis", "yuksek", "dusuk"))
    atr = gostergeler.atr(f["yuksek"], f["dusuk"], f["kapanis"], ATR_N).to_numpy()
    n, y = len(f), 1 if yon == "arz" else -1
    # mum > 0: bölge yönünde mum (arz: yeşil, talep: kırmızı)
    mum = y * np.diff(kap, prepend=np.nan)
    sonuc = []
    for b in range(1, n - 1):
        if not (mum[b] > 0 and not mum[b + 1] > 0):
            continue
        # gövdenin yakın ucu: yeşil mumda alt, kırmızıda üst; ikisinde de önceki kapanış
        prox = kap[b - 1]
        j = next(
            (
                j
                for j in range(b + 1, min(b + 1 + BOLGE_GUN, n))
                if y * (kap[j] - prox) <= -atr[b]
            ),
            None,
        )
        if j is None:
            continue
        distal = yuk[b] if y > 0 else dus[b]
        sonra = np.flatnonzero(y * (kap[j + 1 :] - distal) > 0)
        sonuc.append((b, j, j + 1 + sonra[0] if len(sonra) else n, prox, distal))
    return sonuc


def bolgeler(f: pd.DataFrame, yon: str) -> pd.DataFrame:
    """Arz (`yon="arz"`) ya da talep bölgeleri (KURALLAR §3 Modül 1; sütunlar A §6): bas, bilinen, proximal, distal, bitis (NaT: aktif), temas, teyit."""
    yuk, dus, gun = f["yuksek"].to_numpy(float), f["dusuk"].to_numpy(float), f.index
    satirlar = []
    for b, j, k, prox, distal in _bolge_listesi(f, yon):
        gir = yuk[j + 1 : k] >= prox if yon == "arz" else dus[j + 1 : k] <= prox
        satirlar.append(
            {
                "bas": gun[b],
                "bilinen": gun[j],
                "proximal": prox,
                "distal": distal,
                "bitis": gun[k] if k < len(f) else pd.NaT,
                "temas": int(gir.sum()),
                "teyit": gun[j],  # YORUM (A §6): oluşum ve onay tarihi = bilinen gün
            }
        )
    s = pd.DataFrame(
        satirlar,
        columns=["bas", "bilinen", "proximal", "distal", "bitis", "temas", "teyit"],
    )
    for sutun in ("bas", "bilinen", "bitis", "teyit"):
        s[sutun] = pd.to_datetime(s[sutun])
    return s


def kurulum(f: pd.DataFrame, p: Parametre = Parametre()) -> pd.DataFrame:
    """`f`: tarih indeksli, `kapanis` ve `yuksek` (düzeltilmiş) sütunları; varyanta göre `dusuk`, `hacim`.
    Satır = sinyal günü (kapanış günü); sütunlar `kutu_alt`, `kutu_ust`, `hedef` (hedef yoksa NaN). KURALLAR §3 Modül 1.
    Satırlar dönem sırasındadır (agresifte koşu sırası); ilk satır en erken dönemin sinyalidir. Aynı gün iki dönemin
    sinyali olabilir (pencereler çakışırsa); satır tekrar eder ve `sinyal` bugünkü gibi tekrarı korur."""
    n = len(f)
    kap, yuk = f["kapanis"].to_numpy(float), f["yuksek"].to_numpy(float)
    dusuk_lazim = (
        p.giris != "kutu"
        or p.momentum
        or p.teyit != "yok"
        or p.hedef != "yok"
        or p.stop == "kutu"
        or p.dusus
    )
    # ponytail: varsayılan kural `dusuk` istemez; yoksa yalnız kutu_alt NaN kalır. Öbür varyantlar sütunu ister (yoksa KeyError).
    dus = (
        f["dusuk"].to_numpy(float)
        if dusuk_lazim or "dusuk" in f
        else np.full(n, np.nan)
    )
    atr = (
        gostergeler.atr(f["yuksek"], f["dusuk"], f["kapanis"], ATR_N).to_numpy()
        if p.giris in ("mum", "retest") or p.hedef == "tansu" or p.dusus
        else None
    )
    govde = np.fmax(
        np.r_[np.nan, kap[:-1]], kap
    )  # gövde ucu: açılış yok; ilk günde önceki kapanış yok -> kapanış

    def ust_bul(a, b):
        """Kutu üstü (gün a ... b-1): gün yüksekliklerinin en büyüğü ya da `govde`'de o günün gövde ucu (eşitlikte ilk gün)."""
        return (
            yuk[a:b].max() if p.kutu_ust == "yuksek" else govde[a + yuk[a:b].argmax()]
        )

    # her aday günün şartı: SMA250, ısınma, momentum, gösterge teyidi
    ok = uygun_gunler(f, p)
    hacim_ok = np.ones(n, dtype=bool)
    if p.hacim_kat > 0:
        ort = f["hacim"].shift(1).rolling(HACIM_GUN).mean()  # t hariç
        hacim_ok = (f["hacim"] >= p.hacim_kat * ort).to_numpy()
    if p.momentum or p.teyit == "gosterge":
        v = gostergeler.momentum_squeeze(f["yuksek"], f["dusuk"], f["kapanis"])
    if p.momentum:
        ok &= ~((v < 0) & (v < v.shift(1))).to_numpy()
    if (
        p.teyit == "gosterge"
    ):  # hesaplanamayan değer (NaN) karşılaştırmayı yanlış yapar: gün aday değil
        h = gostergeler.macd_histogram(f["kapanis"])
        k, d = gostergeler.stokastik(f["yuksek"], f["dusuk"], f["kapanis"])
        psar = gostergeler.psar(f["yuksek"], f["dusuk"])
        a = gostergeler.adx(f["yuksek"], f["dusuk"], f["kapanis"])
        ok &= (
            (h > h.shift(1))
            & (psar < f["kapanis"])
            & (k > d)
            & (v > v.shift(1))
            & (a > a.shift(1))
        ).to_numpy()
    tepe = np.flatnonzero(_salinim(yuk, True)) if p.teyit == "trend" else None
    dip = np.flatnonzero(_salinim(dus, False)) if p.teyit == "trend" else None
    arz = _bolge_listesi(f, "arz") if p.hedef == "tansu" or p.giris == "arz" else []
    emax = mum = None
    if p.giris == "ema":
        emax = (
            pd.concat([gostergeler.ema(f["kapanis"], q) for q in p.periyotlar], axis=1)
            .max(axis=1)
            .to_numpy()
        )
    if p.giris in ("mum", "retest"):
        # yeşil, uzun (>= ATR14), güçlü (kapanış üst üçte birde); açılış yok, vekil ölçü
        mum = (
            (np.diff(kap, prepend=np.nan) > 0)
            & (yuk - dus >= atr)
            & (3 * (kap - dus) >= 2 * (yuk - dus))
        )

    def aday(i, hacim=True):
        return bool(
            ok[i]
            and (hacim_ok[i] or not hacim)
            and (p.teyit != "trend" or _trend_teyit(i, kap, yuk, dus, tepe, dip))
        )

    def tetik(i, ust, seviye=None):
        if p.giris == "ema":
            return kap[i] > emax[i]
        if p.giris == "kutu":
            return kap[i] > ust
        if p.giris in ("arz", "ucgen"):
            return kap[i] > seviye(i)
        return mum[i] and kap[i] > ust

    def kapi(i, alt, ucgen):
        """(geçti, hedef): hedef, arz bölgesi ve üçgen hedeflerinden kapanışın üstünde kalanların küçüğü; R/R kapısı yalnız hedef varsa."""
        if p.hedef != "tansu":
            return True, np.nan
        adaylar = [
            x for x in (ucgen, *(z[3] for z in arz if z[1] <= i < z[2])) if x > kap[i]
        ]
        if not adaylar:
            return True, np.nan
        hedef = min(adaylar)
        stop = alt if p.stop == "kutu" else kap[i] - STOP_KAT[p.stop] * atr[i]
        return bool(
            kap[i] > stop and (hedef - kap[i]) / (kap[i] - stop) >= p.rr_min
        ), hedef

    def donem_elenir(bas, alt):
        """True: `dusus` açık ve güçlü düşüş şartı yok ya da hesaplanamıyor, dönem sayılmaz.
        Şart: `bas`'tan önceki 20 günün en yüksek yükseği >= alt + 3 × ATR14[bas] (KURALLAR §3 Modül 1 Düşüş)."""
        return p.dusus and not (
            bas >= DUSUS_GUN
            and yuk[bas - DUSUS_GUN : bas].max() >= alt + DUSUS_ATR * atr[bas]
        )

    konumlar, satirlar = [], []
    if p.giris == "agresif":  # sıkışma sürerken: pencere yok, koşu başına tek sinyal
        kosu_basi, kullanilan = _kosu_basi(f, p), set()
        for t in range(1, n):
            bas = kosu_basi[t]  # t-1'de biten koşunun ilk günü (yoksa ya da kısaysa -1)
            if bas < 0 or bas in kullanilan:
                continue
            if not (dus[t] <= dus[bas:t].min() <= kap[t]) or not aday(t, hacim=False):
                continue
            if donem_elenir(bas, dus[t]):  # agresifte kutu alt: koşu + t kutusunun altı
                continue
            ucgen = (
                _ucgen_hedef(yuk[bas:t], dus[bas:t]) if p.hedef == "tansu" else np.nan
            )
            gecti, hedef = kapi(t, dus[t], ucgen)
            if gecti:
                kullanilan.add(bas)
                konumlar.append(t)
                satirlar.append((dus[t], ust_bul(bas, t + 1), hedef))
    else:
        oran = gostergeler.sikisma_orani(f["kapanis"], p.periyotlar)
        for d in gostergeler.sikisma_donemleri(oran, p.esik, p.min_gun):
            bas, bit = f.index.get_loc(d["bas"]), f.index.get_loc(d["bit"])
            ust, alt = ust_bul(bas, bit + 1), dus[bas : bit + 1].min()
            if donem_elenir(bas, alt):
                continue
            ucgen = (
                _ucgen_hedef(yuk[bas : bit + 1], dus[bas : bit + 1])
                if p.hedef == "tansu"
                else np.nan
            )
            sira, hacim = range(bit + 1, min(bit + 1 + p.pencere, n)), True
            seviye = None  # `arz`, `ucgen`: i günü için kapanışın geçeceği seviye; yoksa bu dönemde sinyal yok
            if p.giris == "arz":
                # dönem bitişinde aktif arz bölgelerinden proximal'ı kutu üstünden büyük olanların en küçük proximal'lısı
                ustte = [z for z in arz if z[1] <= bit < z[2] and z[3] > ust]
                if ustte:
                    distal = min(ustte, key=lambda z: z[3])[4]
                    seviye = lambda i, distal=distal: distal
            elif p.giris == "ucgen":
                # üst çizgi: ilk ve son salınım tepesinden geçer, gün sırasıyla uzar
                u = _ucgen(yuk[bas : bit + 1], dus[bas : bit + 1])
                if u is not None:
                    tepe2 = bas + u[0][[0, -1]]
                    seviye = lambda i, tepe2=tepe2: _dogru(yuk, tepe2, i)
            if p.giris in ("arz", "ucgen") and seviye is None:
                sira = []
            if p.giris == "retest":
                # ilk güçlü mum k; sonra k+1 ... k+5 içinde kutu üstüne değen ilk gün j
                k = next((i for i in sira if tetik(i, ust)), None)
                j = None
                if k is not None and hacim_ok[k]:
                    j = next(
                        (
                            i
                            for i in range(k + 1, min(k + 1 + RETEST_GUN, n))
                            if dus[i] <= ust
                        ),
                        None,
                    )
                sira, hacim = ([j] if j is not None and kap[j] > ust else []), False
            for i in sira:
                if p.stop == "kutu" and (kap[bit + 1 : i] < alt).any():
                    break  # Tansu: kutu altı kapanışta analiz iptal olur (KURALLAR §3 Stop `kutu`)
                if (p.giris == "retest" or tetik(i, ust, seviye)) and aday(i, hacim):
                    gecti, hedef = kapi(i, alt, ucgen)
                    if gecti:
                        konumlar.append(i)
                        satirlar.append((alt, ust, hedef))
                        break
    return pd.DataFrame(
        satirlar,
        index=f.index.take(konumlar),
        columns=["kutu_alt", "kutu_ust", "hedef"],
        dtype=float,
    )


def sinyal(f: pd.DataFrame, p: Parametre = Parametre()) -> pd.DatetimeIndex:
    """`f`: tarih indeksli, `kapanis` ve `yuksek` (düzeltilmiş) sütunları. Sinyal günleri (kapanış günü)."""
    return kurulum(f, p).index
