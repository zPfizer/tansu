"""Motor: saf Adım fonksiyonu ve sinyallerden işlem listesi (TASARIM 5.3, 5.5; çıkış paketi KURALLAR §3 "Modül 1").

Fiyatlar düzeltilmiş seriden; kilit ve karantina bayrakları ham seriden gelir (`veri.Anlik.gun_tablosu`).
Mum: tarih, aof, yuksek, dusuk, kapanis, sma250, atr, islem, karantina, kilit_tavan, kilit_taban.
Yalnız etkin kuralın okuduğu sütunlar: hacim (kurulum), rsi, onceki_rsi, sma50, onceki_dusuk.
"""

from dataclasses import dataclass, replace

import pandas as pd

from tansu import aileler, gostergeler
from tansu.veri import KARANTINA_GUN

STOP_ATR = 2.0  # TASARIM 5.5: acil stop = giriş - 2 ATR
ETKIN_ATR = 1.5  # `dip` kuralı giriş + 1,5 ATR görülünce etkin olur
YARI_ATR = 3.0  # `atr3` yarı satış seviyesi: giriş + 3 ATR
BASABAS_R = 1.5  # yüksek giriş + 1,5 R görülünce stop girişe çıkar
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
    cikis_fiyat: float = (
        None  # yarı satış varsa yalnız son çıkışın fiyatı; ortalama `_tablo`'da
    )
    neden: str = None  # kapalıysa: stop | sma250 | hedef | cikis_kurali | karantina | veri_sonu | iptal
    ayar: aileler.Parametre = aileler.Parametre()
    kutu_alt: float = None  # sinyal günü kutu altı (kutu stopu); None: kutu yok
    hedef: float = None  # sinyal günü hedef fiyatı; None: hedef yok
    ilk_stop: float = None  # planlanan risk ve R buradan (stop yükselse de değişmez)
    yari_tarih: object = None
    yari_fiyat: float = None
    aktif: bool = False  # `dip`: yüksek giriş + 1,5 ATR görüldü
    senaryo: frozenset = (
        frozenset()
    )  # tetiklenmiş farklı senaryolar (`dip`, `rsi70`, `rsi50`, `sma50`)
    yari_bekleyen: bool = False  # yarı satış tetiklendi, ertesi AOF'ta dolar
    kar: bool = False  # `rsi70` önşartı (KURALLAR §3 Modül 1, rsi70 "Etkinleşme önşartı"): girişten sonra bir kapanış hem giriş fiyatının hem SMA50'nin üstünde oldu; giriş günü sayılmaz


def bekleyen(
    atr: float,
    sinyal_tarih=None,
    ayar: aileler.Parametre = aileler.Parametre(),
    kutu_alt=None,
    hedef=None,
) -> Pozisyon:
    """Sinyal günü kapanışında oluşan, ertesi gün girecek pozisyon."""
    return Pozisyon(
        "bekliyor",
        atr=atr,
        sinyal_tarih=sinyal_tarih,
        ayar=ayar,
        kutu_alt=kutu_alt,
        hedef=hedef,
    )


def _ulasti(yuksek, seviye) -> bool:
    """yüksek >= seviye; kayan nokta hatası tam eşiği kaçırmasın diye 9 ondalığa yuvarlanır (KURALLAR §3 ATR merdiveni)."""
    return round(yuksek - seviye, 9) >= 0


def _kapat(p, tarih, fiyat, neden):
    return replace(p, durum="kapali", cikis_tarih=tarih, cikis_fiyat=fiyat, neden=neden)


def adim(p: Pozisyon, m) -> Pozisyon:
    """(pozisyon, bugünkü mum) → pozisyon. Saf; kurallar TASARIM 5.3 ve 5.5, KURALLAR §3 Modül 1."""
    if p.durum == "kapali":
        return p
    if p.durum == "bekliyor":
        kutu = p.ayar.stop == "kutu" and p.kutu_alt is not None
        if (
            m["karantina"]
            or not m["islem"]
            or m["kilit_tavan"]
            or (kutu and m["aof"] <= p.kutu_alt)  # kutu altına sarkan giriş iptal
        ):
            return _kapat(p, m["tarih"], None, "iptal")
        stop = (
            p.kutu_alt
            if kutu
            else m["aof"]
            - aileler.STOP_KAT.get(p.ayar.stop, aileler.STOP_KAT["atr2"]) * p.atr
        )
        p = replace(
            p,
            durum="acik",
            giris_tarih=m["tarih"],
            giris_fiyat=m["aof"],
            stop=stop,
            ilk_stop=stop,
        )
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
    return p if ilk_gun else _gun(p, m)


def _gun(p, m):
    """Stopa dokunmayan, tam çıkışı beklemeyen açık gün (giriş günü hariç): KURALLAR §3 gün sırası."""
    t, aof, taban = m["tarih"], m["aof"], m["kilit_taban"]
    if p.yari_bekleyen and not taban:  # kilitli taban: AOF dolumu kayar
        p = replace(p, yari_bekleyen=False, yari_tarih=t, yari_fiyat=aof)
    if p.hedef is not None and m["yuksek"] >= p.hedef:
        if taban:  # kilitli taban: tam çıkış ertesi kilitsiz günün AOF'unda, stop gibi (TASARIM 5.3)
            return replace(p, bekleyen="hedef")
        return _kapat(p, t, p.hedef if m["dusuk"] <= p.hedef else aof, "hedef")
    seviye = p.giris_fiyat + YARI_ATR * p.atr
    if p.ayar.cikis == "atr3" and p.yari_tarih is None and _ulasti(m["yuksek"], seviye):
        if taban:  # kilitli taban: yarı satış ertesi kilitsiz günün AOF'unda; yari_tarih o zamana dek boş, tek sefer
            p = replace(p, yari_bekleyen=True)
        else:
            p = replace(
                p, yari_tarih=t, yari_fiyat=seviye if m["dusuk"] <= seviye else aof
            )
    if m["kapanis"] < m["sma250"]:  # SMA250 tam çıkışı önce gelir
        p = replace(p, bekleyen="sma250")
    else:
        p = _cikis_kurali(p, m)
    return _merdiven(p, m) if p.ayar.cikis != "yok" else p


def _cikis_kurali(p, m):
    """`dip`, `rsi70`, `rsi50`: tetikler kapanışta bakılır, yarı satış ve tam çıkış ertesi AOF'ta dolar.
    `rsi70` yarı satışı için önşart `kar`: girişten sonra önceki bir günün kapanışı giriş fiyatının ve SMA50'nin üstündedir."""
    c = p.ayar.cikis
    if c in ("yok", "atr3"):
        return p
    alti = m["kapanis"] < m["onceki_dusuk"]  # kapanış önceki gün düşüğünün altında
    senaryo = {
        ad
        for ad, ok in (
            ("dip", c != "rsi70" and p.aktif and alti),  # etkinlik önceki günlerden
            ("rsi70", c == "rsi70" and p.kar and m["onceki_rsi"] >= 70 > m["rsi"]),
            ("rsi50", c == "rsi50" and m["onceki_rsi"] >= 50 > m["rsi"]),
            ("sma50", c == "rsi50" and m["yuksek"] >= m["sma50"] > m["kapanis"]),
        )
        if ok
    }
    gorulen = p.senaryo | senaryo
    # rsi50: ikinci farklı senaryo tam çıkış. rsi70: yarı satıştan sonra ilk dip kapanışı (yarı satış günü dahil).
    tam = len(gorulen) > 1 or (c == "rsi70" and p.yari_tarih is not None and alti)
    yari = bool(senaryo) and not p.senaryo  # ilk senaryo yarı satış verir
    p = replace(
        p,
        aktif=p.aktif or _ulasti(m["yuksek"], p.giris_fiyat + ETKIN_ATR * p.atr),
        senaryo=gorulen,
        # önşart bugünün tetiğinden sonra güncellenir: tetik yalnız u <= t-1 günlerine bakar (giriş günü hariç, `_gun` çağrılmaz)
        kar=p.kar
        or (
            c == "rsi70" and m["kapanis"] > p.giris_fiyat and m["kapanis"] > m["sma50"]
        ),
    )
    if tam:
        return replace(p, bekleyen="cikis_kurali")
    return replace(p, yari_bekleyen=True) if yari else p


def _merdiven(p, m):
    """ATR merdiveni ve başabaş (çıkış paketi): ertesi gün için stop, yalnız yukarı gider.
    ATR_sinyal = 0 ise n tanımsızdır, merdiven basamağı yoktur (KURALLAR §3 ATR merdiveni); başabaş aynen çalışır."""
    n = (
        round((m["yuksek"] - p.giris_fiyat) / p.atr, 9) // 1 if p.atr else 0
    )  # tam basamak kayan nokta hatasıyla düşmesin
    stop = max(p.stop, p.giris_fiyat + (n - 2) * p.atr) if n >= 2 else p.stop
    if _ulasti(m["yuksek"], p.giris_fiyat + BASABAS_R * (p.giris_fiyat - p.ilk_stop)):
        stop = max(stop, p.giris_fiyat)
    return replace(p, stop=stop)


def _kutu_hedef(kurulum) -> dict:
    """Sinyal günü → (kutu_alt, hedef); NaN None olur (kutu yoksa `atr2` yedeği, hedef yoksa hedef çıkışı yok)."""
    if kurulum is None:
        return {}
    kurulum = kurulum[~kurulum.index.duplicated()]  # aynı güne iki dönem: ilki kazanır
    return {
        t: tuple(None if pd.isna(x) else float(x) for x in (a, h))
        for t, a, h in zip(
            kurulum.index, kurulum["kutu_alt"], kurulum["hedef"], strict=True
        )
    }


def kurulum_bilgisi(f: pd.DataFrame, p: aileler.Parametre):
    """Kutu stopu ya da hedef kullanan ayar için `aileler.kurulum`; yoksa None (aynı gün tekrarını `_kutu_hedef` ayıklar)."""
    if p.stop != "kutu" and p.hedef == "yok":
        return None
    return aileler.kurulum(f, p)


def tara(
    mumlar: pd.DataFrame,
    sinyaller,
    ayar: aileler.Parametre = aileler.Parametre(),
    kurulum=None,
) -> tuple:
    """Tek Adım döngüsü (`islemler` ve günlük kart ortak kullanır).

    `kurulum`: `aileler.kurulum` tablosu (indeks sinyal günleri; kutu_alt, hedef); satırı olmayan sinyal günü kutusuz ve hedefsizdir.
    (iptal dışı kapanmış pozisyonlar, düşen sinyal sayısı, veri sonunda kapanmamış pozisyon ya da None,
    son mumda kapanan pozisyon ya da None; iptal dahil)."""
    sinyaller, kb = set(sinyaller), _kutu_hedef(kurulum)
    kapali, dusen, p, son_karantina, kapanan = [], 0, None, None, None
    for i, (tarih, satir) in enumerate(mumlar.iterrows()):
        m = {**satir.to_dict(), "tarih": tarih}
        kapanan = None
        if p is not None:
            p = adim(p, m)
            if p.durum == "kapali":
                dusen += p.neden == "iptal"
                if p.neden != "iptal":
                    kapali.append(p)
                kapanan, p = p, None
        if m["karantina"]:
            son_karantina = i
        engelli = son_karantina is not None and i - son_karantina < KARANTINA_GUN
        if p is None and tarih in sinyaller and not engelli:
            p = bekleyen(m["atr"], tarih, ayar, *kb.get(tarih, (None, None)))
    return kapali, dusen, p, kapanan


def islemler(
    mumlar: pd.DataFrame,
    sinyaller,
    ayar: aileler.Parametre = aileler.Parametre(),
    kurulum=None,
) -> tuple:
    """Tek hissenin mumları (tarih indeksli) ve sinyal günlerinden (işlem listesi, düşen sinyal sayısı)."""
    kapali, dusen, p, _ = tara(mumlar, sinyaller, ayar, kurulum)
    if p is not None and p.durum == "bekliyor":
        dusen += 1  # sinyalden sonra veri yok
    elif p is not None:
        gecerli = mumlar["kapanis"].dropna()
        kapali.append(_kapat(p, gecerli.index[-1], gecerli.iloc[-1], "veri_sonu"))
    return _tablo(kapali), dusen


class Zincir:
    """Bir hissenin sinyal konumlarından `islemler` ile aynı tabloyu kurar; tek işlem sonuçlarını önbelleğe alır (K1, TASARIM 5.7).

    Aynı hissede sinyal kümesi her tekrarda değişir; her (konum, kutu alt, hedef) sinyalinin tek başına sonucu aynıdır.
    Önbellek anahtarı kurulum değerlerini içerir: sağlamlık ızgarası aynı Zincir'i, aynı konum için kutusu farklı hücrelerle
    paylaşır. Bir sinyal, önceki işlem kapanana dek (kapandığı gün hariç: kapanış gününün sinyali alınır, `islemler` gibi) ve
    karantina penceresinde (250 satır) düşer. `kurulum` ctor'da verilirse çağrıların varsayılanıdır."""

    def __init__(
        self,
        mumlar: pd.DataFrame,
        ayar: aileler.Parametre = aileler.Parametre(),
        kurulum=None,
    ):
        self.mumlar, self.ayar, self.kurulum = mumlar, ayar, kurulum
        self.satirlar = [
            {**s, "tarih": t}
            for t, s in zip(mumlar.index, mumlar.to_dict("records"), strict=True)
        ]
        kar = mumlar["karantina"].to_numpy(dtype=bool)
        son = pd.Series(range(len(kar))).where(kar).ffill().to_numpy()
        self.engelli = (
            range(len(kar)) - son
        ) < KARANTINA_GUN  # NaN (karantina yok) -> yanlış
        gecerli = mumlar["kapanis"].dropna()
        self.son = (gecerli.index[-1], gecerli.iloc[-1]) if len(gecerli) else None
        self.onbellek = {}

    def tek(self, i: int, kb: tuple = (None, None)) -> tuple:
        """(kapalı pozisyon ya da None, kapanış konumu ya da None). None kapanış konumu: pozisyon veri sonuna dek açık
        ya da sinyalden sonra veri yok (`dusen`: p None). `kb`: (kutu alt, hedef), yoksa (None, None)."""
        if (i, kb) not in self.onbellek:
            p = bekleyen(
                self.satirlar[i]["atr"],
                self.satirlar[i]["tarih"],
                self.ayar,
                *kb,
            )
            sonuc = None
            for j in range(i + 1, len(self.satirlar)):
                p = adim(p, self.satirlar[j])
                if p.durum == "kapali":
                    sonuc = (p, j)
                    break
            if sonuc is None and p.durum == "acik":
                sonuc = (_kapat(p, self.son[0], self.son[1], "veri_sonu"), None)
            self.onbellek[(i, kb)] = sonuc or (None, None)
        return self.onbellek[(i, kb)]

    def kapali(self, konumlar, kurulum=None) -> tuple:
        """(kapanmış pozisyonlar, düşen sinyal sayısı): tablo kurmadan; K1 çok hissenin pozisyonlarını tek tabloda toplar."""
        kb = _kutu_hedef(self.kurulum if kurulum is None else kurulum)
        kapali, dusen, blok = [], 0, 0
        for i in sorted(set(konumlar)):
            if i < blok or self.engelli[i]:
                continue
            p, j = self.tek(i, kb.get(self.satirlar[i]["tarih"], (None, None)))
            if p is None or p.neden == "iptal":
                dusen += 1
                blok = len(self.satirlar) if p is None else j
            else:
                kapali.append(p)
                blok = len(self.satirlar) + 1 if j is None else j
        return kapali, dusen

    def calistir(self, konumlar, kurulum=None) -> tuple:
        """(işlem tablosu, düşen sinyal sayısı); `islemler(mumlar, sinyaller, ayar, kurulum)` ile aynı."""
        kapali, dusen = self.kapali(konumlar, kurulum)
        return _tablo(kapali), dusen


def _tablo(pozisyonlar) -> pd.DataFrame:
    satirlar = []
    for p in pozisyonlar:
        # ponytail: yarı satışlı işlem tek satır, çıkış fiyatı iki yarının ortalaması; simülatör yarı satışın nakdini son
        # çıkış gününde görür (faiz ve yeniden kullanım eksik, TASARIM 5.5 "Yarı satışlı işlem"). Gün gün nakit için iki satır gerekir.
        # `yari_tarih` ve `yari_fiyat` satırda kalır: simülatör kapanan hissede yalnız kalan yarıyı sıfırlar (TASARIM 5.2).
        cikis = (
            p.cikis_fiyat
            if p.yari_fiyat is None
            else (p.yari_fiyat + p.cikis_fiyat) / 2
        )
        satirlar.append(
            {
                "sinyal_tarih": p.sinyal_tarih,
                "giris_tarih": p.giris_tarih,
                "giris_fiyat": p.giris_fiyat,
                "cikis_tarih": p.cikis_tarih,
                "cikis_fiyat": cikis,
                "neden": p.neden,
                "adet": p.adet,
                "planlanan_risk": p.adet * (p.giris_fiyat - p.ilk_stop),
                "gerceklesen_kayip": p.adet * max(0.0, p.giris_fiyat - cikis),
                "yari_tarih": p.yari_tarih,
                "yari_fiyat": p.yari_fiyat,
            }
        )
    return pd.DataFrame(
        satirlar,
        columns=[
            "sinyal_tarih",
            "giris_tarih",
            "giris_fiyat",
            "cikis_tarih",
            "cikis_fiyat",
            "neden",
            "adet",
            "planlanan_risk",
            "gerceklesen_kayip",
            "yari_tarih",
            "yari_fiyat",
        ],
    ).astype(
        {"yari_tarih": "datetime64[ns]", "yari_fiyat": float}
    )  # yarı satış yoksa NaT / NaN (TASARIM 5.5 "Yarı satışlı işlem")


def mumlar(
    anlik, sembol: str, p: aileler.Parametre = aileler.Parametre(), atr_n: int = ATR_N
) -> pd.DataFrame:
    """Bir sembolün mum tablosu: düzeltilmiş fiyat + gösterge + ham seriden kilit/karantina (gun_tablosu).

    Tablo anlık görüntü başına bir kez kurulur (motor, K1 ve ızgara aynı tabloyu okur; değiştirilmez)."""
    onbellek = anlik.__dict__.setdefault("_mumlar", {})
    anahtar = (sembol, p.sma_n, atr_n)
    if anahtar not in onbellek:
        onbellek[anahtar] = _mumlar_kur(anlik, sembol, p, atr_n)
    return onbellek[anahtar]


def _mumlar_kur(anlik, sembol, p, atr_n) -> pd.DataFrame:
    f = (
        anlik.fiyat[anlik.fiyat["sembol"] == sembol]
        .sort_values("tarih")
        .set_index("tarih")
    )
    g = anlik.gun_tablosu
    g = g[g["sembol"] == sembol].set_index("tarih")
    m = f[["aof", "yuksek", "dusuk", "kapanis", "hacim"]].reindex(
        g.index
    )  # eksik gün NaN kalır
    m["sma250"] = gostergeler.sma(m["kapanis"], p.sma_n)
    m["atr"] = gostergeler.atr(m["yuksek"], m["dusuk"], m["kapanis"], atr_n)
    m["rsi"] = gostergeler.rsi(m["kapanis"])
    m["sma50"] = gostergeler.sma(m["kapanis"], 50)
    # önceki gün = son dolu gün (eksik gün atlanır)
    m["onceki_rsi"] = m["rsi"].ffill().shift(1)
    m["onceki_dusuk"] = m["dusuk"].ffill().shift(1)
    for ad in ("islem", "karantina", "kilit_tavan", "kilit_taban"):
        m[ad] = g[ad].astype(bool)
    return m


def sinama(
    anlik, p: aileler.Parametre = aileler.Parametre(), atr_n: int = ATR_N, uye=None
) -> tuple:
    """Anlık görüntünün sembolleri için (işlem listesi, düşen sinyal sayısı).

    `uye`: (sembol, tarih) tablosu (`simulator.uyeler`); verilirse yalnız o hisse-günlerdeki sinyaller motora girer,
    yani simülatörün alabileceği sinyaller (TASARIM 5.6 evren süzgeci). `p` aynı zamanda çıkış ayarıdır; kutu stopu
    ya da hedef kullanan ayarda kurulum bilgisi de motora girer."""
    parcalar, dusen = [], 0
    gunler = None if uye is None else uye.groupby("sembol")["tarih"].agg(list)
    for s in anlik.fiyat["sembol"].unique():
        if gunler is not None and s not in gunler.index:
            continue
        m = mumlar(anlik, s, p, atr_n)
        f = m.dropna(subset=["kapanis"])
        sig = aileler.sinyal(f, p)
        if gunler is not None:
            sig = sig[sig.isin(gunler[s])]
        # ponytail: kurulum ikinci kez hesaplanır (sinyal zaten onu hesaplamıştı); yalnız kutu stopu ve hedef varyantlarında
        t, d = Zincir(m, p).calistir(
            m.index.get_indexer(sig), kurulum_bilgisi(f, p)
        )  # `islemler` ile bire bir (test), ama tek geçişte hızlı
        if len(t):  # boş tablolar sütun türünü object'e bozar
            parcalar.append(t.assign(sembol=s))
        dusen += d
    return (
        pd.concat(parcalar, ignore_index=True)
        if parcalar
        else _tablo([]).assign(sembol=[])
    ), dusen
