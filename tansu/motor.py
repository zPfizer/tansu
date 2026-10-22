"""Motor: saf Adım fonksiyonu ve sinyallerden işlem listesi (TASARIM 5.3, 5.5; çıkış paketi KURALLAR §3 "Modül 1").

Fiyatlar düzeltilmiş seriden; kilit ve karantina bayrakları ham seriden gelir (`veri.Anlik.gun_tablosu`).
Mum: tarih, aof, yuksek, dusuk, kapanis, sma250, atr, islem, karantina, kilit_tavan, kilit_taban.
Yalnız etkin kuralın okuduğu sütunlar: hacim (kurulum), rsi, onceki_rsi, sma50, onceki_dusuk.
"""

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
import math

import pandas as pd

from tansu import aileler, gostergeler, islem_riski
from tansu.veri import KARANTINA_GUN, YUVARLAMA, UyelikKapsamHatasi, VeriHatasi

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
    uyelik_kaniti: dict | None = None  # TASARIM 5.15: yalnız tarihli üyelik yolunda
    risk_girdisi: dict | None = None  # TASARIM 5.15 S08: açık risk/maliyet isteği
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


def adim(p: Pozisyon, m, *, karar=True) -> Pozisyon:
    """(pozisyon, bugünkü mum) → pozisyon. Saf; kurallar TASARIM 5.3 ve 5.5, KURALLAR §3 Modül 1."""
    if p.durum == "kapali":
        return p
    ilk_gun = p.durum == "bekliyor"
    if ilk_gun:
        p = _giris_adimi(p, m)
        if p.durum == "kapali":
            return p
    else:
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
    return p if ilk_gun else _gun(p, m, karar=karar)


def _giris_adimi(p, m):
    kutu = p.ayar.stop == "kutu" and p.kutu_alt is not None
    if (
        m["karantina"]
        or not m["islem"]
        or m["kilit_tavan"]
        or (kutu and m["aof"] <= p.kutu_alt)
    ):
        return _kapat(p, m["tarih"], None, "iptal")
    stop = (
        p.kutu_alt
        if kutu
        else m["aof"]
        - aileler.STOP_KAT.get(p.ayar.stop, aileler.STOP_KAT["atr2"]) * p.atr
    )
    return replace(
        p,
        durum="acik",
        giris_tarih=m["tarih"],
        giris_fiyat=m["aof"],
        stop=stop,
        ilk_stop=stop,
    )


def _gun(p, m, *, karar=True):
    """Stopa dokunmayan, tam çıkışı beklemeyen açık gün (giriş günü hariç): KURALLAR §3 gün sırası."""
    p = _gun_ici_cikis(p, m)
    if p.durum == "kapali" or p.bekleyen == "hedef":
        return p
    if karar is False:
        return _merdiven(p, m) if p.ayar.cikis != "yok" else p
    if (karar is True or "sma250" in karar) and m["kapanis"] < m["sma250"]:
        p = replace(p, bekleyen="sma250")
    else:
        p = _cikis_kurali(p, m, karar=karar)
    return _merdiven(p, m) if p.ayar.cikis != "yok" else p


def _gun_ici_cikis(p, m):
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
    return p


def _cikis_kurali(p, m, *, karar=True):
    """`dip`, `rsi70`, `rsi50`: tetikler kapanışta bakılır, yarı satış ve tam çıkış ertesi AOF'ta dolar.
    `rsi70` yarı satışı için önşart `kar`: girişten sonra önceki bir günün kapanışı giriş fiyatının ve SMA50'nin üstündedir."""
    c = p.ayar.cikis
    if c in ("yok", "atr3"):
        return p
    izin = {"dip", "rsi70", "rsi50", "sma50", "kar"} if karar is True else karar
    alti = "dip" in izin and m["kapanis"] < m["onceki_dusuk"]
    senaryo = _cikis_tetikleri(p, m, izin, alti)
    gorulen = p.senaryo | senaryo
    # rsi50: ikinci farklı senaryo tam çıkış. rsi70: yarı satıştan sonra ilk dip kapanışı (yarı satış günü dahil).
    tam = len(gorulen) > 1 or (c == "rsi70" and p.yari_tarih is not None and alti)
    yari = bool(senaryo) and not p.senaryo  # ilk senaryo yarı satış verir
    p = _cikis_onsartlari(p, m, izin, gorulen)
    if tam:
        return replace(p, bekleyen="cikis_kurali")
    return replace(p, yari_bekleyen=True) if yari else p


def _cikis_tetikleri(p, m, izin, alti):
    c = p.ayar.cikis
    senaryo = set()
    if c != "rsi70" and p.aktif and alti:
        senaryo.add("dip")
    if c == "rsi70":
        if "rsi70" in izin and p.kar and m["onceki_rsi"] >= 70 > m["rsi"]:
            senaryo.add("rsi70")
    elif c == "rsi50":
        if "rsi50" in izin and m["onceki_rsi"] >= 50 > m["rsi"]:
            senaryo.add("rsi50")
        if "sma50" in izin and m["yuksek"] >= m["sma50"] > m["kapanis"]:
            senaryo.add("sma50")
    return senaryo


def _cikis_onsartlari(p, m, izin, gorulen):
    return replace(
        p,
        aktif=p.aktif or _ulasti(m["yuksek"], p.giris_fiyat + ETKIN_ATR * p.atr),
        senaryo=gorulen,
        # önşart bugünün tetiğinden sonra güncellenir: tetik yalnız u <= t-1 günlerine bakar (giriş günü hariç, `_gun` çağrılmaz)
        kar=p.kar
        or (
            p.ayar.cikis == "rsi70"
            and "kar" in izin
            and m["kapanis"] > p.giris_fiyat
            and m["kapanis"] > m["sma50"]
        ),
    )


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


def kurulum_bilgisi(f: pd.DataFrame, p: aileler.Parametre, *, hesaplanan=None):
    """Kutu stopu ya da hedef kullanan ayar için `aileler.kurulum`; yoksa None (aynı gün tekrarını `_kutu_hedef` ayıklar)."""
    if p.stop != "kutu" and p.hedef == "yok":
        return None
    return aileler.kurulum(f, p) if hesaplanan is None else hesaplanan


def tara(
    mumlar: pd.DataFrame,
    sinyaller,
    ayar: aileler.Parametre = aileler.Parametre(),
    kurulum=None,
    *,
    yurutme=None,
    onceki_durum=None,
) -> tuple | dict:
    """Tek Adım döngüsü (`islemler` ve günlük kart ortak kullanır).

    `kurulum`: `aileler.kurulum` tablosu (indeks sinyal günleri; kutu_alt, hedef); satırı olmayan sinyal günü kutusuz ve hedefsizdir.
    (iptal dışı kapanmış pozisyonlar, düşen sinyal sayısı, veri sonunda kapanmamış pozisyon ya da None,
    son mumda kapanan pozisyon ya da None; iptal dahil).
    Açık `yurutme` isteğinde S09 sözlüğü döner; `islem_adimi` ile aynı geçiş kullanılır."""
    if yurutme is not None:
        return _islem_tara(mumlar, sinyaller, ayar, kurulum, yurutme, onceki_durum)
    if onceki_durum is not None:
        raise ValueError("önceki durum açık yürütme isteği gerektirir")
    return _legacy_tara(mumlar, sinyaller, ayar, kurulum)


def _legacy_tara(mumlar, sinyaller, ayar, kurulum):
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


def _islem_tara(mumlar, sinyaller, ayar, kurulum, yurutme, durum):
    if not isinstance(sinyaller, dict):
        raise ValueError("yeni yürütmede sinyaller tarih-kimlik eşlemesi olmalı")
    if mumlar.empty:
        raise ValueError("yeni yürütmede en az bir mum gerekli")
    if not mumlar.index.is_unique or not mumlar.index.is_monotonic_increasing:
        raise ValueError("mum tarihleri artan ve tekil olmalı")
    gun_sinyalleri = {_gun_tarihi(t): kimlik for t, kimlik in sinyaller.items()}
    if len(gun_sinyalleri) != len(sinyaller):
        raise ValueError("aynı güne birden çok sinyal kimliği verildi")
    kb = _islem_kurulumu(kurulum)
    for tarih, satir in mumlar.iterrows():
        alt, hedef = kb.get(_gun_tarihi(tarih), (None, None))
        durum = islem_adimi(
            durum,
            {**satir.to_dict(), "tarih": tarih},
            gun_sinyalleri.get(_gun_tarihi(tarih)),
            yurutme=yurutme,
            ayar=ayar,
            kutu_alt=alt,
            hedef=hedef,
        )
    return durum


def _islem_kurulumu(kurulum):
    if kurulum is None:
        return {}
    gunler = [_gun_tarihi(t) for t in kurulum.index]
    if len(set(gunler)) != len(gunler):
        raise ValueError("kurulum günleri tekil olmalı")
    return {
        gun: tuple(None if pd.isna(x) else float(x) for x in (alt, hedef))
        for gun, alt, hedef in zip(
            gunler, kurulum["kutu_alt"], kurulum["hedef"], strict=True
        )
    }


def _duz(deger):
    """JSON durumu için tarihler ve sayısal skalerler (TASARIM 5.15 S09)."""
    if isinstance(deger, dict):
        return {k: _duz(v) for k, v in deger.items()}
    if isinstance(deger, (set, frozenset)):
        deger = sorted(deger)
    if isinstance(deger, (tuple, list)):
        return [_duz(v) for v in deger]
    if isinstance(deger, pd.Timestamp):
        return deger.date().isoformat()
    if hasattr(deger, "item"):
        deger = deger.item()
    if isinstance(deger, float) and not math.isfinite(deger):
        return None
    return deger


def _gun_tarihi(tarih):
    t = pd.Timestamp(tarih)
    if pd.isna(t) or t != t.normalize():
        raise ValueError("mum tarihi geçerli bir takvim günü olmalı")
    return t.date().isoformat()


def _iz_kodu(deger):
    return sha256(
        json.dumps(deger, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()
    ).hexdigest()


def _yurutme_dogrula(y):
    for alan in (
        "strateji_id",
        "strateji_surumu",
        "deneme_id",
        "kosu_id",
        "veri_ref_id",
        "sembol",
    ):
        if not isinstance(y.get(alan), str) or not y[alan].strip():
            raise ValueError(f"yürütme kimliği eksik: {alan}")
    for alan, deger in (
        ("surum", "bagimsiz_islem_v1"),
        ("fiyat_politikasi", "aof_v1"),
        ("risk_surumu", islem_riski.RISK_SURUMU),
        ("masraf_surumu", islem_riski.MASRAF_SURUMU),
    ):
        if y.get(alan) != deger:
            raise ValueError(f"bilinmeyen yürütme politikası: {alan}")
    # TASARIM 5.15 #176: yalnız açık sürüm; eski kimliğe varsayılan ekleme.
    if "kilit_politikasi" in y and y["kilit_politikasi"] != "ham_aralik_v1":
        raise ValueError("bilinmeyen yürütme politikası: kilit_politikasi")
    if y.get("aile") == "cift_rotasyonu":
        raise ValueError("risk_dayanagi_eksik")
    if y.get("aile") != "ema_sikismasi":
        raise ValueError("bilinmeyen yürütme ailesi")
    if not _pozitif_sayi(y.get("nominal_tutar")):
        raise ValueError("nominal_tutar sonlu ve pozitif olmalı")


def _pozitif_sayi(x):
    return (
        isinstance(x, (int, float))
        and not isinstance(x, bool)
        and math.isfinite(x)
        and x > 0
    )


def _pozisyon_oku(d):
    if d is None:
        return None
    d = dict(d)
    ayar = dict(d["ayar"])
    ayar["periyotlar"] = tuple(ayar["periyotlar"])
    return Pozisyon(
        **(d | {"ayar": aileler.Parametre(**ayar), "senaryo": frozenset(d["senaryo"])})
    )


def _olay(d, tarih, neden, sinyal=None, *, tur="bilgi"):
    d["retler"].append(dict(tarih=tarih, neden=neden, sinyal_id=sinyal, tur=tur))


def _dolum(d, p, tarih, yon, adet, fiyat, neden):
    if adet:
        d["dolumlar"].append(
            dict(
                dolum_id=f"{p.risk_girdisi['islem_id']}:{tarih}:{neden}",
                islem_id=p.risk_girdisi["islem_id"],
                sinyal_id=p.risk_girdisi["sinyal_id"],
                tarih=tarih,
                tur="model_dolumu",
                yon=yon,
                adet=adet,
                fiyat=fiyat,
                neden=neden,
            )
        )


def _hesap(d, p):
    return islem_riski.hesapla(p.risk_girdisi | {"dolumlar": d["dolumlar"]})


def _fiyat_engeli(m):
    if m["karantina"]:
        return "karantina"
    if not m["islem"]:
        return "islem_yok"
    if not all(_pozitif_sayi(m.get(k)) for k in ("aof", "yuksek", "dusuk", "kapanis")):
        return "gecersiz_fiyat"
    if not (  # TASARIM 5.13: düzeltilmiş serinin mevcut yuvarlama payı
        m["dusuk"] * (1 - YUVARLAMA) <= m["aof"]
        and m["aof"] <= m["yuksek"] * (1 + YUVARLAMA)
        and m["dusuk"] * (1 - YUVARLAMA) <= m["kapanis"]
        and m["kapanis"] <= m["yuksek"] * (1 + YUVARLAMA)
    ):
        raise ValueError("mum fiyat sırası geçersiz")
    return None


def _limitler(m, kilit_politikasi=None):
    bilinen = (
        isinstance(m.get("limit_kaniti"), str)
        and bool(m["limit_kaniti"].strip())
        and all(
            _pozitif_sayi(m.get(k))
            for k in ("ham_yuksek", "ham_dusuk", "tavan", "taban")
        )
    )
    if not bilinen:
        # TASARIM 5.15 #176: aralık kilidi dışlar; sayısal limit üretmez.
        kilit_cozuldu = (
            kilit_politikasi == "ham_aralik_v1"
            and all(m.get(k) is None for k in ("tavan", "taban", "limit_kaniti"))
            and all(_pozitif_sayi(m.get(k)) for k in ("ham_yuksek", "ham_dusuk"))
            and m["ham_yuksek"] > m["ham_dusuk"]
        )
        return kilit_cozuldu, False, False
    if not m["taban"] <= m["ham_dusuk"] <= m["ham_yuksek"] <= m["tavan"]:
        raise ValueError("ham fiyat veya limit sırası geçersiz")
    return (
        True,
        m["ham_yuksek"] == m["ham_dusuk"] == m["tavan"],
        m["ham_yuksek"] == m["ham_dusuk"] == m["taban"],
    )


def _karar_gostergeleri(p, m):
    gerekli = {"sma250": ("sma250",)}
    if p.ayar.cikis in ("dip", "rsi70", "rsi50"):
        gerekli["dip"] = ("onceki_dusuk",)
    if p.ayar.cikis in ("rsi70", "rsi50"):
        gerekli[p.ayar.cikis] = ("onceki_rsi", "rsi")
        gerekli["kar" if p.ayar.cikis == "rsi70" else "sma50"] = ("sma50",)
    izin = {
        ad
        for ad, alanlar in gerekli.items()
        if all(
            isinstance(m.get(k), (int, float)) and math.isfinite(m[k]) for k in alanlar
        )
    }
    return izin, izin != gerekli.keys()


def _yurut_gun(d, p, m):
    t = m["tarih"]
    engel = _fiyat_engeli(m)
    if engel:
        return _engelli_gun(d, p, t, engel)
    kilit_cozuldu, ust, alt = _limitler(m, d["yurutme"].get("kilit_politikasi"))
    if p.durum == "bekliyor" and (not kilit_cozuldu or ust):
        _olay(
            d,
            t,
            "kilitli_tavan" if ust else "limit_bilinmiyor",
            p.risk_girdisi["sinyal_id"],
            tur="dusen_sinyal",
        )
        return None
    # Değerleme, dolum kanıtına bağlı değildir; yalnız temiz işlem fiyatını taşır.
    d["degerleme"] = dict(tarih=t, fiyat=m["kapanis"])
    if not kilit_cozuldu:
        _olay(d, t, "limit_bilinmiyor")
    m = m | {"kilit_tavan": bool(ust), "kilit_taban": bool(alt or not kilit_cozuldu)}
    karar, eksik = _karar_gostergeleri(p, m)
    if eksik:
        _olay(d, t, "gosterge_eksik")
    p = _dolumlu_adim(d, p, m, karar)
    _satis_engelini_kaydet(d, p, m)
    return p


def _satis_engelini_kaydet(d, p, m):
    if p is not None and m["kilit_taban"] and (p.bekleyen or p.yari_bekleyen):
        _olay(d, m["tarih"], "satis_engeli", tur="ertelenen_satis")


def _engelli_gun(d, p, t, engel):
    if p.durum == "bekliyor":
        _olay(d, t, engel, p.risk_girdisi["sinyal_id"], tur="dusen_sinyal")
        return None
    if engel == "karantina":
        _olay(d, t, "karantina_cikis_bekliyor", tur="ertelenen_satis")
        return replace(p, bekleyen="karantina")
    tur = "ertelenen_satis" if p.bekleyen or p.yari_bekleyen else "bilgi"
    _olay(d, t, engel, tur=tur)
    return p


def _girisi_boyutla(d, p, t):
    if p.giris_fiyat is None:
        _olay(d, t, "gecersiz_giris", p.risk_girdisi["sinyal_id"], tur="dusen_sinyal")
        return None
    risk = p.risk_girdisi | dict(giris_fiyat=p.giris_fiyat, ilk_stop=p.ilk_stop)
    plan = islem_riski.hesapla(risk)
    if plan["risk_nedeni"]:
        _olay(d, t, plan["risk_nedeni"], risk["sinyal_id"], tur="dusen_sinyal")
        return None
    p = replace(p, adet=plan["adet"], risk_girdisi=risk)
    _dolum(d, p, t, "alis", plan["adet"], p.giris_fiyat, "giris")
    return p


def _yari_dolum(d, p, t):
    kalan = _hesap(d, p)["kalan_adet"]
    adet = int(kalan) // 2
    _dolum(d, p, t, "satis", adet, p.yari_fiyat, "yari")
    d["yari_islenen"] = True
    if adet:
        return p
    _olay(d, t, "yari_adet_sifir")
    return replace(p, yari_tarih=None, yari_fiyat=None)


def _dolumlu_adim(d, p, m, karar):
    t = m["tarih"]
    once = p
    if d["yari_islenen"] and p.yari_tarih is None:
        p = replace(p, yari_tarih="islenmis")
    p = adim(p, m, karar=karar)
    if p.yari_tarih == "islenmis":
        p = replace(p, yari_tarih=None)
    if once.durum == "bekliyor":
        p = _girisi_boyutla(d, p, t)
        if p is None:
            return None
    if p.yari_tarih == t and once.yari_tarih is None and not d["yari_islenen"]:
        p = _yari_dolum(d, p, t)
    if p.durum == "kapali":
        _dolum(
            d, p, t, "satis", int(_hesap(d, p)["kalan_adet"]), p.cikis_fiyat, p.neden
        )
        d["islemler"].append(
            dict(pozisyon=_duz(asdict(p)), dolumlar=d["dolumlar"], sonuc=_hesap(d, p))
        )
        d["dolumlar"] = []
        return None
    return p


def _durumu_oku(durum, y):
    if durum is None:
        return dict(
            surum="islem_durumu_v1",
            yurutme=y,
            son_tarih=None,
            son_girdi=None,
            pozisyon=None,
            dolumlar=[],
            islemler=[],
            retler=[],
            iz=[],
            degerleme=None,
            karantina_kalan=0,
            yari_islenen=False,
        )
    d = json.loads(json.dumps(durum, allow_nan=False))
    kod = d.pop("butunluk", None)
    if kod != _iz_kodu(d) or d["surum"] != "islem_durumu_v1" or d["yurutme"] != y:
        raise ValueError("önceki durum veya yürütme bağı uyuşmuyor")
    return d


def _sinyali_al(d, p, m, sinyal, ayar, kutu_alt, hedef):
    if sinyal is None:
        return p
    if p is not None:
        _olay(d, m["tarih"], "acik_islem", sinyal, tur="reddedilen_sinyal")
        return p
    if d["karantina_kalan"]:
        _olay(d, m["tarih"], "karantina_penceresi", sinyal, tur="reddedilen_sinyal")
        return None
    if not _atr_gecerli(m.get("atr")):
        _olay(d, m["tarih"], "gecersiz_risk_girdisi", sinyal, tur="dusen_sinyal")
        return None
    if _kurulum_eksik(ayar, kutu_alt, hedef):
        _olay(d, m["tarih"], "kurulum_eksik", sinyal, tur="dusen_sinyal")
        return None
    d["yari_islenen"] = False
    return replace(
        bekleyen(m["atr"], m["tarih"], ayar, kutu_alt, hedef),
        risk_girdisi=d["yurutme"]
        | {
            "sinyal_id": sinyal,
            "ayar_parmak_izi": _iz_kodu(_duz(asdict(ayar))),
            "islem_id": _iz_kodu(
                [d["yurutme"], sinyal, m["tarih"], _duz(asdict(ayar)), kutu_alt, hedef]
            ),
        },
    )


def _kurulum_eksik(ayar, kutu_alt, hedef):
    for deger in (kutu_alt, hedef):
        if deger is not None and not _pozitif_sayi(deger):
            raise ValueError("kurulum fiyatı sonlu ve pozitif olmalı")
    return (ayar.stop == "kutu" and kutu_alt is None) or (
        ayar.hedef != "yok" and hedef is None
    )


def _atr_gecerli(atr):
    return (
        isinstance(atr, (int, float))
        and not isinstance(atr, bool)
        and math.isfinite(atr)
        and atr >= 0
    )


def _durumu_tamamla(d, p, tarih, girdi):
    d["pozisyon"] = _duz(asdict(p)) if p is not None else None
    d["sonuc"] = _hesap(d, p) if p is not None else None
    durumlar = {"acik": "acik_son", "bekliyor": "bekliyor"}
    d["durum"] = durumlar[p.durum] if p else "bos"
    net = sum(i["sonuc"]["net_sonuc"] for i in d["islemler"])
    net += (d["sonuc"] or {}).get("net_sonuc", 0)
    d["iz"].append(
        dict(
            tarih=tarih,
            egri_turu="tani_referans",
            nominal_tutar=d["yurutme"]["nominal_tutar"],
            net_sonuc=net,
            referans_sonucu=net / d["yurutme"]["nominal_tutar"],
            kalan_adet=(d["sonuc"] or {}).get("kalan_adet", 0),
            degerleme=d["degerleme"],
        )
    )
    d["dusen_sinyal_sayisi"] = sum(r["tur"] == "dusen_sinyal" for r in d["retler"])
    d["ertelenen_satis_gunu_sayisi"] = len(
        {r["tarih"] for r in d["retler"] if r["tur"] == "ertelenen_satis"}
    )
    d["son_tarih"], d["son_girdi"] = tarih, girdi
    return d | {"butunluk": _iz_kodu(d)}


def _mum_dogrula(mum, sinyal):
    tarih = _gun_tarihi(mum["tarih"])
    m = _duz(dict(mum)) | {"tarih": tarih}
    for alan in ("islem", "karantina"):
        if type(m.get(alan)) is not bool:
            raise ValueError(f"mum bayrağı eksik: {alan}")
    if sinyal is not None and (not isinstance(sinyal, str) or not sinyal.strip()):
        raise ValueError("sinyal kimliği boş olamaz")
    return m


def islem_adimi(
    durum,
    mum,
    sinyal=None,
    *,
    yurutme,
    ayar=aileler.Parametre(),
    kutu_alt=None,
    hedef=None,
):
    """TASARIM 5.15 S09: saf, JSON ile geri okunabilir tek hisse geçişi."""
    y = _duz(yurutme)
    _yurutme_dogrula(y)
    if y.get("kilit_politikasi") == "ham_aralik_v1":
        # _duz sonlu olmayanı None yapmadan, bozuk kanıtın yok sayılmasını engelle.
        for alan in ("tavan", "taban", "limit_kaniti"):
            deger = mum.get(alan)
            if deger is None:
                continue
            gecerli = _pozitif_sayi(deger)
            if alan == "limit_kaniti":
                gecerli = isinstance(deger, str) and bool(deger.strip())
            if not gecerli:
                raise ValueError("geçersiz sayısal limit girdisi")
    m = _mum_dogrula(mum, sinyal)
    tarih = m["tarih"]
    girdi = _iz_kodu([m, sinyal, _duz(asdict(ayar)), _duz(kutu_alt), _duz(hedef)])
    d = _durumu_oku(durum, y)
    if d["son_tarih"] is not None and tarih <= d["son_tarih"]:
        if tarih == d["son_tarih"] and girdi == d["son_girdi"]:
            return d | {"butunluk": _iz_kodu(d)}
        raise ValueError("tekrarlanan veya geriye giden mum çelişkili")
    p = _pozisyon_oku(d["pozisyon"])
    if p is not None:
        if p.ayar != ayar:
            _olay(d, tarih, "ayar_degisti")
        p = _yurut_gun(d, p, m)
    d["karantina_kalan"] = (
        KARANTINA_GUN if m["karantina"] else max(0, d["karantina_kalan"] - 1)
    )
    p = _sinyali_al(d, p, m, sinyal, ayar, kutu_alt, hedef)
    return _durumu_tamamla(d, p, tarih, girdi)


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
        *,
        uyelik=None,
        sembol=None,
    ):
        self.mumlar, self.ayar, self.kurulum = mumlar, ayar, kurulum
        self.uyelik, self.sembol = uyelik, sembol
        self.uyelik_retleri = []
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
        self.uyelik_retleri = []
        for i in sorted(set(konumlar)):
            if i < blok or self.engelli[i]:
                continue
            kanit, ret = self._uyelik_girisi(i)
            if ret is not None:
                self.uyelik_retleri.append(ret)
                dusen += 1
                blok = i + 1
                continue
            p, j = self.tek(i, kb.get(self.satirlar[i]["tarih"], (None, None)))
            if p is None or p.neden == "iptal":
                dusen += 1
                blok = len(self.satirlar) if p is None else j
            else:
                if kanit is not None:
                    p = replace(p, uyelik_kaniti=kanit)
                kapali.append(p)
                blok = len(self.satirlar) + 1 if j is None else j
        return kapali, dusen

    def _uyelik_girisi(self, i):
        """Sinyal ve giriş günü ayrı kalır; çıkışa uygulanmaz (TASARIM 5.15)."""
        if self.uyelik is None or i + 1 == len(self.satirlar):
            return None, None
        sinyal, giris = (
            self.satirlar[j]["tarih"].date().isoformat() for j in (i, i + 1)
        )
        for tarih, neden in (
            (sinyal, "sinyal_gununde_uye_degil"),
            (giris, "giris_gununde_uye_degil"),
        ):
            gun = self.uyelik["gunler"][tarih]
            if self.sembol not in gun["semboller"]:
                return None, {
                    "sembol": self.sembol,
                    "sinyal_tarih": sinyal,
                    "giris_tarih": giris,
                    "neden": neden,
                    "uyelik_surumu": self.uyelik["uyelik_surumu"],
                    "uyelik_kaniti": gun,
                }
        return next(k for k in gun["kanitlar"] if k["sembol"] == self.sembol), None

    def calistir(self, konumlar, kurulum=None) -> tuple:
        """(işlem tablosu, düşen sinyal sayısı); `islemler(mumlar, sinyaller, ayar, kurulum)` ile aynı."""
        kapali, dusen = self.kapali(konumlar, kurulum)
        tablo = _tablo(kapali)
        if self.uyelik is not None:
            tablo["uyelik_kaniti"] = [p.uyelik_kaniti for p in kapali]
        return tablo, dusen


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
    m = m.join(gostergeler.tablo(m, p.sma_n, atr_n))
    # önceki gün = son dolu gün (eksik gün atlanır)
    m["onceki_rsi"] = m["rsi"].ffill().shift(1)
    m["onceki_dusuk"] = m["dusuk"].ffill().shift(1)
    for ad in ("islem", "karantina", "kilit_tavan", "kilit_taban"):
        m[ad] = g[ad].astype(bool)
    return m


def _uyelik_kosusu(anlik, paket):
    """E1 kanıtı koşunun her değerlendirme gününü kapsar (TASARIM 5.15)."""
    u, ref = paket["uyelik"], paket["referans"]
    if ref.get("pay_kimligi") is not None:
        # TASARIM 5.15 #167: eski motorun sembol anlamı örtük değişmez.
        raise VeriHatasi("eski motor pay kimliği paketini desteklemiyor")
    if (
        ref["goruntu_id"] != anlik.kimlik
        or ref["uyelik_surumu"] != u["uyelik_surumu"]
        or ref["uyelik_tablo_parmak_izi"] != u["tablo_parmak_izi"]
        or ref["evren_politikasi"] != u["evren_politikasi"]
    ):
        raise VeriHatasi("koşunun veri/üyelik referansı uyuşmuyor")
    bas, son = (pd.Timestamp(ref["istenen_donem"][ad]) for ad in ("baslangic", "bitis"))
    tarihler = anlik.gunler[(anlik.gunler >= bas) & (anlik.gunler <= son)]
    eksik = []
    for t in tarihler:
        tarih = t.date().isoformat()
        gun = u["gunler"].get(tarih, {"semboller": [], "kanitlar": []})
        semboller = set(gun["semboller"])
        if len(semboller) != 30 or semboller != {k["sembol"] for k in gun["kanitlar"]}:
            eksik.append(tarih)
    if eksik:
        raise UyelikKapsamHatasi(u["uyelik_surumu"], eksik)
    return u, bas, son


def sinama(
    anlik,
    p: aileler.Parametre = aileler.Parametre(),
    atr_n: int = ATR_N,
    uye=None,
    *,
    veri_paketi=None,
) -> tuple:
    """Anlık görüntünün sembolleri için (işlem listesi, düşen sinyal sayısı).

    `uye`: (sembol, tarih) tablosu (`simulator.uyeler`); verilirse yalnız o hisse-günlerdeki sinyaller motora girer,
    yani simülatörün alabileceği sinyaller (TASARIM 5.6 evren süzgeci). `p` aynı zamanda çıkış ayarıdır; kutu stopu
    ya da hedef kullanan ayarda kurulum bilgisi de motora girer.
    `veri_paketi`: E1 yanıtıyla tarihli üyelik denetimi (TASARIM 5.15); sonuç attrs alanı
    veri referansını ve üyelik retlerini, işlem satırı giriş kanıtını taşır."""
    parcalar, dusen, retler = [], 0, []
    uyelik = None
    if veri_paketi is not None:
        if uye is not None:
            raise VeriHatasi("eski üyelik tablosu ile E1 üyeliği birlikte seçilemez")
        uyelik, bas, son = _uyelik_kosusu(anlik, veri_paketi)
    gunler = None if uye is None else uye.groupby("sembol")["tarih"].agg(list)
    for s in anlik.fiyat["sembol"].unique():
        if veri_paketi is not None and s not in veri_paketi["semboller"]:
            continue
        if gunler is not None and s not in gunler.index:
            continue
        m = mumlar(anlik, s, p, atr_n)
        if uyelik is not None:
            m = m.loc[:son]
        f = m.dropna(subset=["kapanis"])
        kurulum = aileler.kurulum(f, p)
        sig = kurulum.index
        if uyelik is not None:
            sig = sig[sig >= bas]
        if gunler is not None:
            sig = sig[sig.isin(gunler[s])]
        zincir = Zincir(m, p, uyelik=uyelik, sembol=s)
        t, d = zincir.calistir(
            m.index.get_indexer(sig), kurulum_bilgisi(f, p, hesaplanan=kurulum)
        )  # `islemler` ile bire bir (test), ama tek geçişte hızlı
        if len(t):  # boş tablolar sütun türünü object'e bozar
            parcalar.append(t.assign(sembol=s))
        dusen += d
        retler.extend(zincir.uyelik_retleri)
    sonuc = (
        pd.concat(parcalar, ignore_index=True)
        if parcalar
        else _tablo([]).assign(sembol=[])
    )
    if uyelik is not None:
        sonuc.attrs.update(
            uyelik_surumu=uyelik["uyelik_surumu"],
            evren_politikasi=uyelik["evren_politikasi"],
            veri_referanslari=[veri_paketi["referans"]],
            uyelik_retleri=retler,
        )
    return sonuc, dusen
