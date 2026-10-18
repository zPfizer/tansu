"""Strateji kataloğu: eski tanımlar ve seçim sınırı (TASARIM 5.15)."""

from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from hashlib import sha256
import json
import argparse
import sys
import math
from types import MappingProxyType

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
    periyotlar: tuple = (20, 50, 100, 200)
    esik: float = 0.012
    min_gun: int = 3
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
_TANIMLAR = {
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


# TASARIM 5.15: sürüm içeriği değişmez; yeni kaynak yeni sürüm ister.
KATALOG_SURUMU = "s02_v1"
SEMA_SURUMU = "strateji_s02_v1"
AILE = "ema_sikisma"
_TANIMLAR = MappingProxyType(_TANIMLAR)
SECENEKLER = MappingProxyType(SECENEKLER)
STOP_KAT = MappingProxyType(STOP_KAT)


@dataclass(frozen=True)
class Kaynak:
    tur: str
    konum: str
    tarih: str
    alinti: str | None
    karar_durumu: str
    alinti_bos_nedeni: str | None = None


@dataclass(frozen=True)
class Alan:
    ad: str
    deger: str | int | float | bool | tuple
    tur: str
    birim: str
    kaynaklar: tuple[Kaynak, ...]
    koken: str = "YORUM"
    tanimsiz_esik: bool = False
    onayli_aralik: tuple[float, float] | None = None


@dataclass(frozen=True)
class StratejiKaydi:
    kayit_id: str
    kayit_turu: str
    sema_surumu: str
    olusturma_zamani: str
    kaynaklar: tuple[Kaynak, ...]
    aile: str
    varyant: str
    katalog_surumu: str
    bilesim_id: str
    izin_durumu: str
    eski_karsilastirma: bool
    temel_varyant: str | None
    parametreler: tuple[Alan, ...]
    sabitler: tuple[Alan, ...]
    gosterge_ayarlari: tuple[Alan, ...]
    dolum_surumu: str
    risk_surumu: str
    masraf_surumu: str
    muhasebe_surumu: str
    donem_surumu: str
    ayar_parmak_izi: str
    izin_kaynaklari: tuple[Kaynak, ...]
    izin_nedeni: str


_LEGACY_KAYNAK = Kaynak(
    "YORUM",
    "docs/TASARIM.md#strateji-kataloğu",
    "2026-10-18",
    None,
    "eski_tanim",
    "Eski tanımın kaydıdır; birinci el bileşim kanıtı değildir.",
)
_KAYNAKLAR = (_LEGACY_KAYNAK,)
_HAVUZ = "kisisel/300-Projects/Tansu X Veri Havuzu/"
_EMA_KAYNAK = Kaynak(
    "Tansu",
    _HAVUZ + "tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127.md:35",
    "2025-12-19",
    "EMA'ların (örneğin EMA 20, 50, 100) ... Ben 5-8-13 kullandım.",
    "Yalnız EMA periyot bileşeni; bütün katalog bileşimine izin vermez.",
)
_UCGEN_EMA_KAYNAK = Kaynak(
    "Tansu",
    _HAVUZ + "tweet-ema-sikismasi-ucgen-kirilim-hacim-1954300245707497649.md:24",
    "2025-08-09",
    "elli, yüz ve iki yüz periyotluk üssel ortalamalar",
    "Yalnız EMA periyot bileşeni; bütün katalog bileşimine izin vermez.",
)
_KRDMD_KAYNAK = Kaynak(
    "Tansu",
    _HAVUZ + "gorsel-paket-67-krdmd-ema-sikisma-ratio-formasyon.md:23",
    "2026-08-28",
    "EMA20, EMA50, EMA100, EMA200; Tolerans %1.2; Min 3 gün",
    "Görsel örneği; Ham'da yazar yok. Tarih kayıt tarihi, gönderi tarihi bilinmiyor. "
    "Bütün katalog bileşimine izin vermez.",
)
_HACIM_KAYNAK = Kaynak(
    "Tansu",
    _HAVUZ
    + "tweet-qullamaggie-tarzi-hacimli-breakout-tarama-1979546907505545421.md:29",
    "2025-10-18",
    "Breakout anında hacmin ortalamanın en az 2-3 katı olması lazım.",
    "Yalnız kat bileşeni; ortalama penceresi ve bütün katalog bileşimine izin vermez.",
)
_RR_KAYNAK = Kaynak(
    "sahip kararı",
    "docs/KURALLAR.md:319",
    "2026-10-16",
    "en az 1:2 ödül/risk, altındakiler sinyal değildir",
    "Kayıtlı sahip kararı; bütün katalog bileşimine izin vermez.",
)
_ALAN_KAYNAKLARI = MappingProxyType(
    {
        ("periyotlar", (5, 8, 13)): _EMA_KAYNAK,
        ("periyotlar", (20, 50, 100)): _EMA_KAYNAK,
        ("periyotlar", (50, 100, 200)): _UCGEN_EMA_KAYNAK,
        ("periyotlar", (20, 50, 100, 200)): _KRDMD_KAYNAK,
        ("esik", 0.012): _KRDMD_KAYNAK,
        ("min_gun", 3): _KRDMD_KAYNAK,
        ("hacim_kat", 2.0): _HACIM_KAYNAK,
        ("hacim_kat", 3.0): _HACIM_KAYNAK,
        ("rr_min", 2.0): _RR_KAYNAK,
    }
)
_SABITLER = (
    ("KIRILIM_GUN", KIRILIM_GUN, "gun"),
    ("ATR_N", ATR_N, "gun"),
    ("HACIM_GUN", HACIM_GUN, "gun"),
    ("RETEST_GUN", RETEST_GUN, "gun"),
    ("BOLGE_GUN", BOLGE_GUN, "gun"),
    ("TREND_GUN", TREND_GUN, "gun"),
    ("YAKIN", YAKIN, "oran"),
    ("DUSUS_GUN", DUSUS_GUN, "gun"),
    ("DUSUS_ATR", DUSUS_ATR, "ATR"),
    ("STOP_KAT", tuple(STOP_KAT.items()), "ATR"),
)
_POLITIKA_ALANLARI = (
    "dolum_surumu",
    "risk_surumu",
    "masraf_surumu",
    "muhasebe_surumu",
    "donem_surumu",
)
_BIRIMLER = {
    "periyotlar": "gun",
    "esik": "oran",
    "min_gun": "gun",
    "pencere": "gun",
    "isinma": "gun",
    "sma_n": "gun",
    "hacim_kat": "kat",
    "rr_min": "oran",
}


class KatalogHatasi(ValueError):
    """TASARIM 5.15: sınırdaki hata kodu panel ve CLI için aynıdır."""

    def __init__(self, kod: str, aciklama: str):
        self.kod = kod
        super().__init__(f"{kod}: {aciklama}")


def _alan(ad, deger, birim="birimsiz"):
    tur = {bool: "bayrak", int: "tam", float: "sayi", str: "metin", tuple: "liste"}
    kaynak_adi = "periyotlar" if ad == "ema_periyotlar" else ad
    kaynak = _ALAN_KAYNAKLARI.get((kaynak_adi, deger), _LEGACY_KAYNAK)
    return Alan(ad, deger, tur[type(deger)], birim, (kaynak,), kaynak.tur)


def _gostergeler(p):
    # Hesapların sürümlü ayar kopyası; hesap sahibi gostergeler/aileler/motor'dur.
    ayarlar = (
        ("ema_periyotlar", p.periyotlar, "gun"),
        ("ema_adjust", False, "birimsiz"),
        ("sma_n", p.sma_n, "gun"),
        ("atr_n", ATR_N, "gun"),
        ("atr_yontem", "wilder_ilk_n_tr_ortalama", "birimsiz"),
        ("rsi_n", 14, "gun"),
        ("rsi_yontem", "wilder_ilk_n_dolu", "birimsiz"),
        ("adx_n", 14, "gun"),
        ("adx_ilk_gun", 28, "gun"),
        ("momentum_n", 20, "gun"),
        ("momentum_yontem", "lazybear_dogrusal_son", "birimsiz"),
        ("macd_hizli", 12, "gun"),
        ("macd_yavas", 26, "gun"),
        ("macd_sinyal", 9, "gun"),
        ("stokastik_n", 14, "gun"),
        ("stokastik_d", 3, "gun"),
        ("psar_adim", 0.02, "oran"),
        ("psar_tavan", 0.2, "oran"),
        ("psar_ilk_yon", "yukari", "birimsiz"),
        ("psar_ilk_deger", "ilk_dusuk", "birimsiz"),
        ("salinim_yan_gun", 2, "gun"),
        ("isinma", p.isinma, "gun"),
        ("yakin_sama", "legacy_isinma", "birimsiz"),
    )
    return tuple(_alan(*a) for a in ayarlar)


def legacy_coz(
    varyant: str, katalog_surumu: str = KATALOG_SURUMU, *, sayisal_ayarlar=None
) -> StratejiKaydi:
    """Eski tanımı okur; bu işlem panel seçimine izin vermez (TASARIM 5.15)."""
    if katalog_surumu != KATALOG_SURUMU:
        raise KatalogHatasi("bilinmeyen_surum", "Katalog sürümü tanımsız.")
    if not isinstance(varyant, str) or varyant not in _TANIMLAR:
        raise KatalogHatasi("desteklenmeyen_bilesim", "Varyant katalogda yok.")
    p = _TANIMLAR[varyant]
    sayisal_ayarlar = {} if sayisal_ayarlar is None else sayisal_ayarlar
    _sozluk(sayisal_ayarlar, ("esik", "min_gun", "pencere"))
    for ad, deger in sayisal_ayarlar.items():
        if (
            type(deger) not in (int, float)
            or not math.isfinite(deger)
            or deger <= 0
            or (ad != "esik" and type(deger) is not int)
        ):
            raise KatalogHatasi("gecersiz_istek", f"Geçersiz eski ızgara ayarı: {ad}")
    p = replace(p, **sayisal_ayarlar)
    parametreler = tuple(
        replace(
            _alan(ad, deger, _BIRIMLER.get(ad, "birimsiz")),
            kaynaklar=(_LEGACY_KAYNAK,),
            koken="legacy_izgara",
        )
        if ad in sayisal_ayarlar
        else _alan(ad, deger, _BIRIMLER.get(ad, "birimsiz"))
        for ad, deger in asdict(p).items()
    )
    sabitler = tuple(_alan(*a) for a in _SABITLER)
    gostergeler = _gostergeler(p)
    politikalar = dict.fromkeys(_POLITIKA_ALANLARI, "legacy_portfoy_v1")
    icerik = json.dumps(
        (
            katalog_surumu,
            varyant,
            [asdict(a) for a in parametreler],
            [asdict(a) for a in sabitler],
            [asdict(a) for a in gostergeler],
            politikalar,
        ),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    parmak = sha256(icerik.encode("utf-8")).hexdigest()
    return StratejiKaydi(
        kayit_id=f"{katalog_surumu}:{varyant}",
        kayit_turu="strateji",
        sema_surumu=SEMA_SURUMU,
        olusturma_zamani=datetime.now(timezone.utc).isoformat(),
        kaynaklar=tuple(
            dict.fromkeys(
                (
                    *_KAYNAKLAR,
                    *(
                        k
                        for a in (*parametreler, *sabitler, *gostergeler)
                        for k in a.kaynaklar
                    ),
                )
            )
        ),
        aile=AILE,
        varyant=varyant,
        katalog_surumu=katalog_surumu,
        bilesim_id=f"{katalog_surumu}:{varyant}",
        izin_durumu="izinsiz",
        eski_karsilastirma=True,
        temel_varyant=None if varyant == "bugun" else "tansu",
        parametreler=parametreler,
        sabitler=sabitler,
        gosterge_ayarlari=gostergeler,
        **politikalar,
        ayar_parmak_izi=parmak,
        izin_kaynaklari=(),
        izin_nedeni="Bütün bileşimi doğrulayan birinci el kaynak yok.",
    )


def eski_parametreler() -> dict[str, Parametre]:
    """Eski aileler çağrılarının uyarlayıcısı (TASARIM 5.15)."""
    return {
        ad: Parametre(**{a.ad: a.deger for a in legacy_coz(ad).parametreler})
        for ad in _TANIMLAR
    }


def _sozluk(deger, izinli):
    if not isinstance(deger, dict):
        raise KatalogHatasi("gecersiz_istek", "İstek alanları nesne olmalıdır.")
    if deger.keys() - set(izinli):
        raise KatalogHatasi("bilinmeyen_alan", "İstek tanımsız alan içeriyor.")


def secim_dogrula(istek: dict) -> StratejiKaydi:
    """Panel/CLI seçim kapısı; legacy okuma yetkisi seçim girdisi değildir.

    TASARIM 5.15: s02_v1 için izinli bütün bileşim ve onaylı aralık yoktur.
    Yeni kaynak bu sürümün iznini değiştirmez; yeni sürüm gerekir.
    """
    _sozluk(
        istek,
        ("aile", "varyant", "katalog_surumu", "sayisal_ayarlar", "islem_ayarlari"),
    )
    kayit = legacy_coz(istek.get("varyant"), istek.get("katalog_surumu"))
    if istek.get("aile") != AILE:
        raise KatalogHatasi("desteklenmeyen_bilesim", "Aile katalogda yok.")
    sayisal = istek.get("sayisal_ayarlar", {})
    _sozluk(sayisal, (a.ad for a in kayit.parametreler))
    if sayisal:
        raise KatalogHatasi(
            "duzenlenemez_alan", "Bu sürümde onaylı sayısal aralık yok."
        )
    islem = istek.get("islem_ayarlari", {})
    _sozluk(islem, _POLITIKA_ALANLARI)
    if any(
        not isinstance(islem.get(ad), str) or not islem[ad].strip()
        for ad in _POLITIKA_ALANLARI
    ):
        raise KatalogHatasi(
            "eksik_islem_ayari", "Beş işlem politikası sürümü zorunludur."
        )
    if any(islem[ad] != getattr(kayit, ad) for ad in _POLITIKA_ALANLARI):
        raise KatalogHatasi("bilinmeyen_surum", "İşlem politikası sürümü tanımsız.")
    raise KatalogHatasi("desteklenmeyen_bilesim", kayit.izin_nedeni)


def panel_komutu(istek: dict) -> StratejiKaydi:
    """Panel bağdaştırıcısının ortak seçim komutu (TASARIM 5.15)."""
    return secim_dogrula(istek)


def cli(argv=None) -> int:
    """TASARIM 5.15: liste veya coz '<JSON istek>' komutu."""
    parser = argparse.ArgumentParser(prog="python -m tansu.katalog")
    alt = parser.add_subparsers(dest="komut", required=True)
    alt.add_parser("liste")
    alt.add_parser("coz").add_argument("istek")
    args = parser.parse_args(argv)
    if args.komut == "liste":
        for ad in _TANIMLAR:
            kayit = legacy_coz(ad)
            print(f"{ad}\t{kayit.izin_durumu}\teski_karsilastirma")
        return 0
    try:
        istek = json.loads(args.istek)
        kayit = secim_dogrula(istek)
    except json.JSONDecodeError:
        print(
            json.dumps(
                {"hata": "gecersiz_istek", "aciklama": "JSON geçersiz."},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2
    except KatalogHatasi as hata:
        print(
            json.dumps({"hata": hata.kod, "aciklama": str(hata)}, ensure_ascii=False),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(asdict(kayit), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
