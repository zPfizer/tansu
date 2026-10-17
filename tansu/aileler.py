"""Aileler: EMA sıkışması kırılım sinyali ve kurulum bilgisi (KURALLAR §3 madde 2 ve "Modül 1"; TASARIM 5.1 ısınma, 5.3 SMA250 şartı)."""

from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

from tansu import gostergeler

SECENEKLER = {  # KURALLAR §3 Modül 1: her alanın izinli değerleri
    "giris": ("kutu", "ema", "mum", "retest", "agresif", "arz", "ucgen"),
    "teyit": ("yok", "gosterge", "trend"),
    "stop": ("atr2", "atr15", "kutu"),
    "hedef": ("yok", "tansu"),
    "cikis": ("yok", "atr3", "dip", "rsi70", "rsi50"),
    "kutu_ust": ("yuksek", "govde"),
}


@dataclass(frozen=True)
class Parametre:
    periyotlar: tuple = gostergeler.SIKISMA_PERIYOTLAR
    esik: float = gostergeler.SIKISMA_ESIK
    min_gun: int = gostergeler.SIKISMA_MIN_GUN
    pencere: int = 10  # YORUM: dönem bittikten sonra giriş penceresi (gün)
    isinma: int = 500  # TASARIM 5.1: hissenin ilk gününden bu kadar işlem günü dolmadan sinyal yok
    sma_n: int = 250
    giris: str = "kutu"  # KURALLAR §3 Modül 1: giriş türü
    hacim_kat: float = (
        0.0  # 0: süzgeç yok; yoksa hacim >= kat × önceki 20 günün ortalaması
    )
    momentum: bool = False
    teyit: str = "yok"
    stop: str = (
        "atr2"  # başlangıç stopu: R/R kapısı burada, giriş stopu `motor`'da okur
    )
    hedef: str = "yok"
    rr_min: float = 2.0
    cikis: str = "yok"  # `motor` okur
    kutu_ust: str = "yuksek"  # KURALLAR §3 Modül 1 Kutu: yuksek = gün yüksekliği, govde = en yüksek günün gövde ucu
    dusus: bool = False  # KURALLAR §3 Modül 1 Düşüş: açıkken güçlü düşüşten sonra gelmeyen dönem sayılmaz

    def __post_init__(self):
        for alan, izinli in SECENEKLER.items():
            if getattr(self, alan) not in izinli:
                raise ValueError(
                    f"Parametre {alan}: {getattr(self, alan)!r} tanımsız; izinli: {izinli}"
                )
        if self.dusus and self.giris == "agresif":
            raise ValueError(
                "Parametre dusus: agresif girişle tanımsız (KURALLAR §3 Modül 1: düşüş şartı sıkışma dönemi başına bakar)"
            )


KIRILIM_GUN = 20  # YORUM (KURALLAR §3): sıkışmasız kırılım kolunda önceki gün sayısı
ATR_N = 14  # TASARIM 5.5; `motor.ATR_N` ile aynı (`motor` bu modüle dayanır, geri import yok)
HACIM_GUN = 20  # YORUM (KURALLAR §3 Modül 1): hacim ortalaması günü
RETEST_GUN = 5  # YORUM: güçlü mumdan sonra geri çekilme aranan gün
BOLGE_GUN = 3  # YORUM: bölgenin onaylanması için bakılan gün (b+1 ... b+3)
TREND_GUN = 5  # YORUM: yükselen trende temas aranan gün (t-5 ... t)
YAKIN = 1.01  # YORUM: "yakın" = %1 (üçgen tepeleri, trend teması)
DUSUS_GUN = 20  # YORUM (KURALLAR §3 Modül 1 Düşüş): dönem başından önceki bakılan gün
DUSUS_ATR = (
    3.0  # YORUM: düşüş = en yüksek yüksek >= kutu alt + 3 × ATR14 (dönem başı günü)
)
STOP_KAT = {  # başlangıç stopu ATR katı: TASARIM 5.5 (2 ATR), KURALLAR §3 Modül 1 `atr15` (1,5 ATR)
    "atr2": 2.0,
    "atr15": 1.5,
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

    konumlar, satirlar = [], []
    if p.giris == "agresif":  # sıkışma sürerken: pencere yok, koşu başına tek sinyal
        kosu_basi, kullanilan = _kosu_basi(f, p), set()
        for t in range(1, n):
            bas = kosu_basi[t]  # t-1'de biten koşunun ilk günü (yoksa ya da kısaysa -1)
            if bas < 0 or bas in kullanilan:
                continue
            if not (dus[t] <= dus[bas:t].min() <= kap[t]) or not aday(t, hacim=False):
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
            if p.dusus and not (
                bas >= DUSUS_GUN
                and yuk[bas - DUSUS_GUN : bas].max() >= alt + DUSUS_ATR * atr[bas]
            ):
                continue  # güçlü düşüşten sonra gelmeyen dönem sayılmaz (yalnız dönem başından önceki günler)
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
                    seviye = lambda i: distal
            elif p.giris == "ucgen":
                # üst çizgi: ilk ve son salınım tepesinden geçer, gün sırasıyla uzar
                u = _ucgen(yuk[bas : bit + 1], dus[bas : bit + 1])
                if u is not None:
                    tepe2 = bas + u[0][[0, -1]]
                    seviye = lambda i: _dogru(yuk, tepe2, i)
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


# KURALLAR §3 Modül 1: Tansu'nun söylediği kuralların birleşimi (YORUM)
_TANSU = Parametre(
    giris="mum",
    hacim_kat=2.0,
    momentum=True,
    stop="kutu",
    hedef="tansu",
    cikis="atr3",
)
# KURALLAR §3 Modül 1 varyant tablosu: temelden tek boyut değişir; `bugun` karşılaştırma tabanıdır
VARYANTLAR = {
    "bugun": Parametre(),
    "tansu": _TANSU,
    "ema_5_8_13": replace(_TANSU, periyotlar=(5, 8, 13)),
    "ema_20_50_100": replace(_TANSU, periyotlar=(20, 50, 100)),
    "ema_10_20_50": replace(_TANSU, periyotlar=(10, 20, 50)),
    "ema_50_100_200": replace(_TANSU, periyotlar=(50, 100, 200)),
    "giris_kutu": replace(_TANSU, giris="kutu"),
    "giris_ema": replace(_TANSU, giris="ema"),
    "giris_retest": replace(_TANSU, giris="retest"),
    "giris_agresif": replace(_TANSU, giris="agresif"),
    "giris_arz": replace(_TANSU, giris="arz"),
    "giris_ucgen": replace(_TANSU, giris="ucgen"),
    "kutu_govde": replace(_TANSU, kutu_ust="govde"),
    "hacim_yok": replace(_TANSU, hacim_kat=0.0),
    "hacim_3": replace(_TANSU, hacim_kat=3.0),
    "momentum_kapali": replace(_TANSU, momentum=False),
    "dusus_sonrasi": replace(_TANSU, dusus=True),
    "teyit_acik": replace(_TANSU, teyit="gosterge"),
    "teyit_trend": replace(_TANSU, teyit="trend"),
    "stop_atr15": replace(_TANSU, stop="atr15"),
    "stop_atr2": replace(_TANSU, stop="atr2"),
    "cikis_dip": replace(_TANSU, cikis="dip"),
    "cikis_rsi70": replace(_TANSU, cikis="rsi70"),
    "cikis_rsi50": replace(_TANSU, cikis="rsi50"),
}
