"""Geçici kayıt sınırı (TASARIM 5.15); kalıcı bayt biçimi #97'dir."""

from datetime import date, datetime, timezone
from decimal import Decimal
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from hashlib import sha256
from itertools import product
import json
import math
import os
from pathlib import Path
from uuid import uuid4

from tansu import katalog

SURUM = "pilot_s03_v1"
_KESIK = b"\t#pilot_s03_v1_kesik\n"


class PilotHatasi(ValueError):
    """Kayıt veya bağ hatası; çağıran başarı gösteremez."""


class PilotYazmaHatasi(OSError):
    """Kalıcı yazma makbuzu alınamadı."""


class PilotBelirsizHatasi(PilotYazmaHatasi):
    """Yayın sonucu doğrulanamadı; kimliklerle yeni okuyucudan kurtarın."""

    def __init__(self, makbuz):
        self.kayit_id = makbuz.olay_id
        self.kosu_id = makbuz.kosu_id
        self.deneme_id = makbuz.deneme_id
        super().__init__(f"Pilot yayın sonucu belirsiz: {self.kayit_id}")


def _icerik_yaz(fd, satir):
    if os.write(fd, satir) != len(satir):
        raise OSError("Eksik satır yazıldı.")
    os.fsync(fd)


def _lf_yaz(fd, beklenen_son):
    """TASARIM 5.15: görünürlük True, False veya doğrulanamayan None olur."""
    try:
        if os.write(fd, b"\n") == 1:
            return True, None
        hata = OSError("Satır sonu yazılamadı.")
    except OSError as yazma_hatasi:
        hata = yazma_hatasi
    try:
        return os.fstat(fd).st_size == beklenen_son, hata
    except OSError as denetim_hatasi:
        return None, denetim_hatasi


def _kodla(deger):
    if deger is None:
        return ["bos"]
    tur = type(deger)
    if tur is bool:
        return ["bayrak", deger]
    if tur is int:
        return ["tam", str(deger)]
    if tur is float:
        if not math.isfinite(deger):
            raise ValueError("Sonlu sayı gerekli.")
        return ["sayi", deger.hex()]
    if tur is Decimal:
        if not deger.is_finite():
            raise ValueError("Sonlu ondalık gerekli.")
        return ["ondalik", format(deger, "f")]
    if tur is str:
        return ["metin", deger]
    if tur is datetime:
        if deger.tzinfo is None or deger.utcoffset() is None:
            raise ValueError("Saat dilimi gerekli.")
        return ["zaman", deger.astimezone(timezone.utc).isoformat()]
    if tur is date:
        return ["tarih", deger.isoformat()]
    if tur in (list, tuple):
        return ["liste" if tur is list else "demet", [_kodla(v) for v in deger]]
    if tur is dict:
        if any(type(k) is not str or k.startswith("$") for k in deger):
            raise ValueError("Anahtar, $ ile başlamayan metin olmalıdır.")
        return ["sozluk", [[k, _kodla(deger[k])] for k in sorted(deger)]]
    raise ValueError(f"Desteklenmeyen tür: {tur.__name__}")


def kanonik(deger):
    """S03 v1 tür etiketli UTF-8 JSON; anahtarlar Unicode sırasındadır."""
    return json.dumps(_kodla(deger), ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )


def _coz(kayit):
    tur, *kalan = kayit
    if tur == "bos":
        return None
    deger = kalan[0]
    donusum = {
        "tam": int,
        "sayi": float.fromhex,
        "ondalik": Decimal,
        "tarih": date.fromisoformat,
        "zaman": datetime.fromisoformat,
        "bayrak": bool,
        "metin": str,
    }
    if tur in donusum:
        return donusum[tur](deger)
    if tur == "sozluk":
        return {k: _coz(v) for k, v in deger}
    if tur in ("liste", "demet"):
        sonuc = [_coz(v) for v in deger]
        return tuple(sonuc) if tur == "demet" else sonuc
    raise PilotHatasi("Bilinmeyen tür etiketi.")


def _metin(deger):
    if not isinstance(deger, str) or not deger.strip():
        raise PilotHatasi("Boş olmayan metin gerekli.")


def _ondaliklar(deger):
    if type(deger) in (int, float):
        raise PilotHatasi("Risk ve masraf sayıları Decimal olmalıdır.")
    if isinstance(deger, dict):
        for v in deger.values():
            _ondaliklar(v)
    elif isinstance(deger, (tuple, list)):
        for v in deger:
            _ondaliklar(v)


def _donem(donem):
    for ad in ("baslangic", "bitis", "isinma_baslangici", "sinir_surumu"):
        if ad not in donem:
            raise PilotHatasi(f"Eksik dönem alanı: {ad}")
    if any(type(donem[a]) is not date for a in ("baslangic", "bitis")):
        raise PilotHatasi("Dönem sınırı tarih olmalıdır.")
    if donem["baslangic"] > donem["bitis"]:
        raise PilotHatasi("Dönem ters.")
    _metin(donem["sinir_surumu"])
    if donem["isinma_baslangici"] is None:
        _metin(donem.get("bos_nedenleri", {}).get("isinma_baslangici"))
    elif (
        type(donem["isinma_baslangici"]) is not date
        or donem["isinma_baslangici"] > donem["baslangic"]
    ):
        raise PilotHatasi("Isınma başlangıcı geçersiz.")


def _strateji_kaydi(girdi):
    """TASARIM 5.15 S07: aynı kayıt girişi, katalog veya çözülmüş eski hücre."""
    if isinstance(girdi, str):
        return asdict(katalog.legacy_coz(girdi))
    s = asdict(girdi) if isinstance(girdi, katalog.StratejiKaydi) else girdi
    if not isinstance(s, dict) or not isinstance(s.get("parametreler"), (list, tuple)):
        raise PilotHatasi("Strateji nesnesi ve parametre listesi gerekli.")
    for a in s["parametreler"]:
        if not isinstance(a, dict) or not {"ad", "deger", "koken"} <= a.keys():
            raise PilotHatasi(
                "Parametre öğesi ad, değer ve köken içeren nesne olmalıdır."
            )
        _metin(a["ad"])
    sayisal = {
        a["ad"]: a["deger"]
        for a in s["parametreler"]
        if a.get("koken") == "legacy_izgara"
    }
    beklenen = asdict(
        katalog.legacy_coz(s["varyant"], s["katalog_surumu"], sayisal_ayarlar=sayisal)
    )

    def icerik(kayit):
        return {k: v for k, v in kayit.items() if k != "olusturma_zamani"}

    if kanonik(icerik(s)) != kanonik(icerik(beklenen)):
        raise PilotHatasi("Tam çözülmüş strateji katalog/ızgara kaydıyla uyuşmuyor.")
    return s


def _veri_kapsamini_dogrula(donemler, referanslar):
    if not isinstance(donemler, list) or not donemler:
        raise PilotHatasi("Dönem listesi gerekli.")
    for donem in donemler:
        if not isinstance(donem, dict):
            raise PilotHatasi("Dönem nesne olmalıdır.")
        _donem(donem)
    if not isinstance(referanslar, (list, tuple)) or not referanslar:
        raise PilotHatasi("Veri referans listesi gerekli.")
    for ref in referanslar:
        _metin(ref)


def _ayarlar(kayit):
    # TASARIM 5.15 S07: özet eşitliği, yapısal geçerliliğin yerine geçmez.
    for ad in (
        "strateji",
        "veri_ayarlari",
        "yontem_ayarlari",
        "risk_ayarlari",
        "masraf_ayarlari",
        "eski_referans",
    ):
        if not isinstance(kayit[ad], dict):
            raise PilotHatasi(f"{ad} nesne olmalıdır.")
    _veri_kapsamini_dogrula(
        kayit["donemler"], kayit["veri_ayarlari"]["veri_referanslari"]
    )
    tekrar = kayit["yontem_ayarlari"].get("tekrar", 0)
    if type(tekrar) is not int or tekrar < 0:
        raise PilotHatasi("Tekrar negatif olmayan tamsayı olmalıdır.")
    _ondaliklar(kayit["risk_ayarlari"])
    _ondaliklar(kayit["masraf_ayarlari"])
    for ad, deger in kayit["eski_referans"].items():
        if deger is None:
            nedenler = kayit["eski_referans"].get("bos_nedenleri", {})
            if not isinstance(nedenler, dict):
                raise PilotHatasi("Eski referansın boşluk nedenleri nesne olmalıdır.")
            _metin(nedenler.get(ad))
    return {
        "strateji": {
            k: v for k, v in kayit["strateji"].items() if k != "olusturma_zamani"
        },
        **{
            a: kayit[a]
            for a in (
                "donemler",
                "veri_ayarlari",
                "yontem_ayarlari",
                "risk_ayarlari",
                "masraf_ayarlari",
            )
        },
    }


def _ayar_ozeti(ayarlar):
    return f"{SURUM}:sha256:{sha256(kanonik(ayarlar)).hexdigest()}"


def _kosu_meta_dogrula(kimlikler, ortam, tohum, ureteci_surumu):
    for deger in kimlikler:
        _metin(deger)
    if not isinstance(ortam, dict) or not ortam:
        raise PilotHatasi("Ortam gerekli.")
    if tohum is not None and (type(tohum) is not int or not ureteci_surumu):
        raise PilotHatasi("Tohum tamsayı ve üreteç sürümü gerekli.")


def _is_listesi_dogrula(is_listesi):
    if not isinstance(is_listesi, list) or not is_listesi:
        raise PilotHatasi("İş listesi boş veya yinelenmiş.")
    for is_id in is_listesi:
        _metin(is_id)
    if len(set(is_listesi)) != len(is_listesi):
        raise PilotHatasi("İş listesi boş veya yinelenmiş.")
    return list(is_listesi)


def _donem_ciktisi_dogrula(durum, birimler, icerik, islem_ref, uyarilar, cikti_ref):
    if durum not in ("tamamlandi", "hata"):
        raise PilotHatasi("Dönem durumu tanımsız.")
    if not isinstance(birimler, dict) or not birimler or not isinstance(icerik, dict):
        raise PilotHatasi("Dönem birimleri ve içeriği gerekli.")
    if any(not isinstance(x, list) for x in (islem_ref, uyarilar, cikti_ref)):
        raise PilotHatasi("Dönem referansları ve uyarılar liste olmalıdır.")
    for ref in islem_ref + cikti_ref:
        _metin(ref)
    if len(set(islem_ref)) != len(islem_ref):
        raise PilotHatasi("İşlem referansı yinelenmiş.")


def _donem_yayini_dogrula(olaylar, kosu_id, is_id, donem):
    for o in olaylar:
        if (o["kayit_turu"], o.get("sonuc_turu"), o.get("kosu_id")) != (
            "sonuc",
            "donem_v1",
            kosu_id,
        ):
            continue
        if o["is_id"] == is_id or kanonik(o["donem"]) == kanonik(donem):
            raise PilotHatasi("Dönem işi sonucu zaten kayıtlı.")


def _donem_islem_baglari(olaylar, kosu_id, donem, referanslar):
    for ref in referanslar:
        islem = _bul(olaylar, ref, "islem")
        if islem["kosu_id"] != kosu_id or kanonik(islem["donem"]) != kanonik(donem):
            raise PilotHatasi("İşlem başka koşuya veya döneme bağlı.")


def _cocuk_sonuc_baglari(olaylar, kosu_id, referanslar):
    for ref in referanslar:
        sonuc = _bul(olaylar, ref, "sonuc")
        if (sonuc["kosu_id"], sonuc.get("sonuc_turu")) != (kosu_id, "donem_v1"):
            raise PilotHatasi("Çocuk sonucu başka koşuya veya sonuç türüne bağlı.")


def _arama_yontemi(ust, politika):
    """TASARIM 5.15 S11: kayıt sınırında yalnız dondurulmuş yöntem geçerlidir."""
    y = ust["yontem_ayarlari"]
    beklenen = dict(
        yontem="kayitli_izgara_v1",
        tekrar=0,
        secim_politikasi="genis_bolge_net_r_v1",
        olcu_politikasi="bagimsiz_olcu_v1",
        eksenler=y.get("eksenler"),
        hucre_yontemi=dict(
            yontem="kayitli_donem_v1",
            tekrar=0,
            yurutme_surumu="bagimsiz_islem_v1",
            fiyat_politikasi="aof_v1",
            muhasebe_politikasi="tani_referans_v1",
        ),
    )
    if kanonik(y) != kanonik(beklenen) or politika != y["secim_politikasi"]:
        raise PilotHatasi("Arama yöntemi veya seçim politikası uyuşmuyor.")
    eksenler = y["eksenler"]
    if not isinstance(eksenler, list) or not eksenler:
        raise PilotHatasi("Arama eksenleri gerekli.")
    for eksen in eksenler:
        _arama_ekseni(eksen)
    adlar = [e["ad"] for e in eksenler]
    if adlar != sorted(set(adlar)):
        raise PilotHatasi("Arama eksen sırası veya tekilliği geçersiz.")
    return eksenler


def _arama_ekseni(eksen):
    izinli = {
        "esik": [0.010, 0.012, 0.015],
        "min_gun": [2, 3, 5],
        "pencere": [5, 10, 20],
    }
    if not isinstance(eksen, dict) or set(eksen) != {"ad", "birim", "degerler"}:
        raise PilotHatasi("Arama ekseni ad, birim ve değerler içermelidir.")
    ad, degerler = eksen["ad"], eksen["degerler"]
    if ad not in izinli or eksen["birim"] != ("oran" if ad == "esik" else "gun"):
        raise PilotHatasi("Arama ekseni veya birimi izinli değil.")
    if not isinstance(degerler, list) or not degerler:
        raise PilotHatasi("Arama eksen değerleri gerekli.")
    if degerler != sorted(set(degerler)) or not set(degerler) <= set(izinli[ad]):
        raise PilotHatasi("Arama eksen değerleri izinli, artan ve tekil olmalıdır.")


def _arama_tam_ayari(ust, ayarlar):
    s = ust["strateji"]
    sabit = {
        a["ad"]: a["deger"] for a in s["parametreler"] if a["koken"] == "legacy_izgara"
    }
    try:
        strateji = katalog.legacy_coz(
            s["varyant"],
            s["katalog_surumu"],
            sayisal_ayarlar=sabit | ayarlar,
        )
    except katalog.KatalogHatasi, OverflowError:
        return None
    return _ayarlar(
        ust
        | dict(
            strateji=asdict(strateji),
            yontem_ayarlari=ust["yontem_ayarlari"]["hucre_yontemi"],
        )
    )


def _arama_makbuzu(olaylar, makbuz, tur, deneme_id, kosu_id, ozet):
    olay = _bul(olaylar, makbuz["olay_id"], tur)
    beklenen = (deneme_id, kosu_id, ozet)
    if (makbuz["deneme_id"], makbuz["kosu_id"], makbuz["ayar_ozeti"]) != beklenen:
        raise PilotHatasi("Arama makbuzu çocuk kimliği veya ayar özetiyle uyuşmuyor.")
    if (
        olay.get("deneme_id"),
        olay.get("kosu_id"),
        olay.get("ayar_parmak_izi"),
    ) != beklenen:
        raise PilotHatasi("Arama makbuzunun gerçek kaydı uyuşmuyor.")
    return olay


def _arama_bos_hucresi(h):
    _metin(h["neden"])
    if h["durum"] not in (
        "alan_disi",
        "kayit_hatasi",
        "hesap_hatasi",
        "eksik",
        "baslamadi",
    ):
        raise PilotHatasi("Kayıtsız çocuk başarılı olamaz.")
    alanlar = (
        "kosu_id",
        "ayar_parmak_izi",
        "kayit_makbuzu",
        "baslangic_makbuzu",
        "bitis_makbuzu",
    )
    if any(h[a] is not None for a in alanlar):
        raise PilotHatasi("Kayıtsız çocuğun koşusu veya makbuzu olamaz.")


def _arama_cocuk_kaydi(olaylar, ust, baslangic, h):
    cocuk = _bul(olaylar, h["deneme_id"], "deneme", "deneme_id")
    if (cocuk["ust_deneme_id"], cocuk["baglar"].get("izgara_ust_deneme")) != (
        ust["deneme_id"],
    ) * 2:
        raise PilotHatasi("Çocuk üst aramaya bağlı değil.")
    _strateji_kaydi(cocuk["strateji"])
    ayarlar = _ayarlar(cocuk)
    if (
        kanonik(ayarlar) != kanonik(h["tam_ayarlar"])
        or _ayar_ozeti(ayarlar) != h["ayar_parmak_izi"]
    ):
        raise PilotHatasi("Çocuk tam ayarı veya ayar özeti uyuşmuyor.")
    _arama_makbuzu(
        olaylar,
        h["kayit_makbuzu"],
        "deneme",
        h["deneme_id"],
        None,
        h["ayar_parmak_izi"],
    )
    if olaylar.index(cocuk) <= olaylar.index(baslangic):
        raise PilotHatasi("Çocuk bu üst arama başlamadan kayıtlı.")
    return cocuk


def _arama_cocuk_kosusu(olaylar, baslangic, h):
    if h["kosu_id"] is None:
        _metin(h["neden"])
        if h["baslangic_makbuzu"] is not None or h["bitis_makbuzu"] is not None:
            raise PilotHatasi("Başlamayan çocuğun koşu makbuzu olamaz.")
        return
    b = _arama_cocuk_baslangici(olaylar, h)
    if olaylar.index(b) <= olaylar.index(baslangic):
        raise PilotHatasi("Çocuk koşusu üst aramadan önce başlamış.")
    isler = [f"donem:{d['ad']}" for d in h["tam_ayarlar"]["donemler"]]
    if b["is_listesi"] != isler:
        raise PilotHatasi("Çocuk dönem işleri uyuşmuyor.")
    for alan in ("anlik_goruntu", "manifest_ozeti", "uyelik_surumu"):
        if b[alan] != baslangic[alan]:
            raise PilotHatasi("Çocuk koşusunun veri kimliği üst aramayla uyuşmuyor.")
    _arama_cocuk_bitisi(olaylar, h)


def _arama_cocuk_baslangici(olaylar, h):
    if h["baslangic_makbuzu"] is not None:
        return _arama_makbuzu(
            olaylar,
            h["baslangic_makbuzu"],
            "baslangic",
            h["deneme_id"],
            h["kosu_id"],
            h["ayar_parmak_izi"],
        )
    if h["durum"] in ("tamamlandi", "islemsiz") or any(
        d["sonuc_ref"] is not None for d in h["donemler"]
    ):
        raise PilotHatasi("Başlangıç makbuzu doğrulanmadan çocuk sonucu olamaz.")
    b = _bul(olaylar, h["kosu_id"], "baslangic", "kosu_id")
    if (b["deneme_id"], b["ayar_parmak_izi"]) != (h["deneme_id"], h["ayar_parmak_izi"]):
        raise PilotHatasi("Başarısız çocuğun gerçek başlangıç bağı uyuşmuyor.")
    return b


def _arama_cocuk_bitisi(olaylar, h):
    bitis = None
    if h["bitis_makbuzu"] is not None:
        bitis = _arama_makbuzu(
            olaylar,
            h["bitis_makbuzu"],
            "bitis",
            h["deneme_id"],
            h["kosu_id"],
            h["ayar_parmak_izi"],
        )
    if h["durum"] in ("tamamlandi", "islemsiz"):
        if bitis is None or bitis["durum"] != "tamamlandi" or bitis["basarisiz"]:
            raise PilotHatasi("Başarılı çocuk için başarılı bitiş makbuzu gerekli.")
        isler = [f"donem:{d['ad']}" for d in h["tam_ayarlar"]["donemler"]]
        if bitis["tamamlanan"] != isler:
            raise PilotHatasi("Başarılı çocuk bütün dönem işlerini tamamlamalıdır.")


def _arama_hucresi(olaylar, ust, baslangic, h, ayarlar):
    if h["ust_deneme_id"] != ust["deneme_id"] or kanonik(h["ayarlar"]) != kanonik(
        ayarlar
    ):
        raise PilotHatasi("Hücre üst bağı veya eksen değeri uyuşmuyor.")
    tam = _arama_tam_ayari(ust, ayarlar)
    if kanonik(h["tam_ayarlar"]) != kanonik(tam):
        raise PilotHatasi("Hücrenin tam ayarı dondurulmuş aramayla uyuşmuyor.")
    if tam is None:
        if h["durum"] != "alan_disi" or h["deneme_id"] is not None:
            raise PilotHatasi("İzin verilmeyen hücre alan dışı kalmalıdır.")
    elif (
        h["durum"] == "alan_disi"
        or h["strateji_ayar_parmak_izi"] != tam["strateji"]["ayar_parmak_izi"]
    ):
        raise PilotHatasi("Hücre strateji özeti veya izinli alanı uyuşmuyor.")
    if h["deneme_id"] is None:
        _arama_bos_hucresi(h)
    else:
        _arama_cocuk_kaydi(olaylar, ust, baslangic, h)
        _arama_cocuk_kosusu(olaylar, baslangic, h)
    _arama_donemleri(olaylar, ust, h)


def _arama_donemleri(olaylar, ust, h):
    if h["durum"] not in (
        "tamamlandi",
        "islemsiz",
        "eksik",
        "hesap_hatasi",
        "kayit_hatasi",
        "alan_disi",
        "baslamadi",
    ):
        raise PilotHatasi("Arama hücre durumu tanımsız.")
    donemler = h["donemler"]
    if kanonik([d["donem"] for d in donemler]) != kanonik(ust["donemler"]):
        raise PilotHatasi("Hücrenin dönem yuvaları kayıtlı dönemlerle uyuşmuyor.")
    for d in donemler:
        _arama_donemi(olaylar, h, d)
    if h["durum"] in ("tamamlandi", "islemsiz"):
        if h["kosu_id"] is None or any(
            d["durum"] not in ("tamamlandi", "islemsiz") for d in donemler
        ):
            raise PilotHatasi(
                "Eksik veya başarısız dönem varken hücre başarılı olamaz."
            )
    else:
        _metin(h["neden"])


def _arama_donemi(olaylar, h, d):
    if d["is_id"] != f"donem:{d['donem']['ad']}":
        raise PilotHatasi("Dönem iş kimliği uyuşmuyor.")
    if d["durum"] not in (
        "tamamlandi",
        "islemsiz",
        "eksik",
        "hesap_hatasi",
        "kayit_hatasi",
        "baslamadi",
    ):
        raise PilotHatasi("Arama dönem durumu tanımsız.")
    refs = d["islem_referanslari"]
    if len(set(refs)) != len(refs):
        raise PilotHatasi("Arama işlem referansı yinelenmiş.")
    _arama_islem_baglari(olaylar, h, d)
    if d["sonuc_ref"] is None:
        _metin(d["neden"])
        if d["durum"] in ("tamamlandi", "islemsiz") or d["semboller"]:
            raise PilotHatasi("Yayımlanmamış dönem başarılı veya ölçülmüş olamaz.")
        return
    sonuc = _bul(olaylar, d["sonuc_ref"], "sonuc")
    _arama_donem_sonucu(h, d, sonuc)
    _cocuk_sonuc_baglari(olaylar, h["kosu_id"], sonuc["cikti_referanslari"])
    _arama_olcu_baglari(olaylar, d)


def _arama_donem_sonucu(h, d, sonuc):
    beklenen = (
        "donem_v1",
        h["deneme_id"],
        h["kosu_id"],
        h["ayar_parmak_izi"],
        d["is_id"],
    )
    alanlar = ("sonuc_turu", "deneme_id", "kosu_id", "ayar_parmak_izi", "is_id")
    if tuple(sonuc.get(a) for a in alanlar) != beklenen:
        raise PilotHatasi("Dönem sonucu başka çocuk, koşu veya ayara bağlı.")
    if (
        kanonik(sonuc["donem"]) != kanonik(d["donem"])
        or sonuc["islem_referanslari"] != d["islem_referanslari"]
    ):
        raise PilotHatasi("Dönem sonucu dönem veya işlem referansıyla uyuşmuyor.")
    for alan in ("deneme_id", "kosu_id", "ayar_parmak_izi", "strateji_ayar_parmak_izi"):
        if sonuc["icerik"][alan] != h[alan]:
            raise PilotHatasi("Dönem içeriğinin çocuk veya ayar özeti uyuşmuyor.")
    basarili = d["durum"] in ("tamamlandi", "islemsiz")
    if (sonuc["durum"] == "tamamlandi") != basarili:
        raise PilotHatasi("Dönem sonucu başarı durumu uyuşmuyor.")
    if not basarili:
        _metin(d["neden"])


def _arama_islem_baglari(olaylar, h, d):
    _donem_islem_baglari(olaylar, h["kosu_id"], d["donem"], d["islem_referanslari"])
    for ref in d["islem_referanslari"]:
        islem = _bul(olaylar, ref, "islem")
        if (islem["deneme_id"], islem["ayar_parmak_izi"]) != (
            h["deneme_id"],
            h["ayar_parmak_izi"],
        ):
            raise PilotHatasi("İşlem başka çocuğa veya ayara bağlı.")


def _arama_olcu_baglari(olaylar, d):
    olculen = []
    for s in d["semboller"]:
        o = s["olcu"]
        refs = _arama_olculen_islemler(olaylar, o)
        olculen.extend(refs)
        egri = o.get("egri_tanimi")
        if egri is not None and not set(egri["referanslar"]) <= set(refs):
            raise PilotHatasi("Eğri başka işlem referansına bağlı.")
    if len(set(olculen)) != len(olculen) or set(olculen) != set(
        d["islem_referanslari"]
    ):
        raise PilotHatasi("Ölçülerin işlem referansları dönemle uyuşmuyor.")


def _arama_olculen_islemler(olaylar, olcu):
    if olcu["politika"] != "bagimsiz_olcu_v1":
        raise PilotHatasi("Arama ölçü politikası uyuşmuyor.")
    refs = []
    for i in olcu["islemler"] + olcu["acik_kismi"]:
        islem = _bul(olaylar, i["islem_ref"], "islem")
        if islem["olaylar"][0]["pozisyon"]["risk_girdisi"]["islem_id"] != i["islem_id"]:
            raise PilotHatasi("Ölçünün gerçek işlem kimliği uyuşmuyor.")
        refs.append(i["islem_ref"])
    return refs


def _arama_hucreleri(olaylar, ust, baslangic, hucreler, eksenler):
    indeksler = list(product(*(range(len(e["degerler"])) for e in eksenler)))
    if kanonik([h["indeks"] for h in hucreler]) != kanonik(
        [list(i) for i in indeksler]
    ):
        raise PilotHatasi("Arama koordinatları eksik, yinelenmiş veya sırasız.")
    isler = ["arama"]
    for h, indeks in zip(hucreler, indeksler, strict=True):
        if h["is_id"] != "hucre:" + ":".join(map(str, indeks)):
            raise PilotHatasi("Hücre iş kimliği koordinatla uyuşmuyor.")
        ayarlar = {
            e["ad"]: e["degerler"][i] for e, i in zip(eksenler, indeks, strict=True)
        }
        _arama_hucresi(olaylar, ust, baslangic, h, ayarlar)
        if h["durum"] != "alan_disi":
            isler.append(h["is_id"])
    if baslangic["is_listesi"] != isler:
        raise PilotHatasi("Üst aramanın başlangıç işleri izinli hücrelerle uyuşmuyor.")


def _arama_bolge_baglari(ust, hucreler, bolgeler, politika):
    """TASARIM 5.15 S11: açıklama ve dönem/hisse bağları seçim hesabı değildir."""
    gerekli = {
        "politika",
        "strateji_id",
        "donem",
        "sembol",
        "secilen",
        "secilen_deneme_id",
        "neden",
        "en_iyi",
        "hucreler",
        "bolgeler",
    }
    for b in bolgeler:
        if not gerekli <= b.keys():
            raise PilotHatasi("Bölgenin kimliği veya seçim açıklaması eksik.")
        if b["politika"] != politika or b["strateji_id"] != ust["strateji"]["kayit_id"]:
            raise PilotHatasi("Bölgenin politika veya strateji bağı uyuşmuyor.")
        if not any(kanonik(b["donem"]) == kanonik(d) for d in ust["donemler"]):
            raise PilotHatasi("Bölge kayıtlı döneme bağlı değil.")
        if b["sembol"] is not None:
            _metin(b["sembol"])
        _arama_bolge_aciklamasi(b, [h["indeks"] for h in hucreler])
        for h, ozet in zip(hucreler, b["hucreler"], strict=True):
            _arama_bolge_hucresi(h, b, ozet)
        _arama_secilen_cocuk(hucreler, b)


def _arama_bolge_aciklamasi(b, indeksler):
    if any(not isinstance(b[a], list) for a in ("hucreler", "bolgeler")):
        raise PilotHatasi("Bölgenin hücre ve bileşen açıklamaları liste olmalıdır.")
    if kanonik([h["indeks"] for h in b["hucreler"]]) != kanonik(indeksler):
        raise PilotHatasi("Bölgenin açıklanan hücre kimlikleri uyuşmuyor.")
    for h in b["hucreler"]:
        _arama_bolge_hucre_aciklamasi(h, indeksler)
    for c in b["bolgeler"]:
        _arama_bolge_bileseni(c, indeksler)
    _arama_en_iyi_bagi(b["en_iyi"], b["secilen"], indeksler)


def _arama_bolge_hucre_aciklamasi(h, indeksler):
    gerekli = {
        "deneme_id",
        "durum",
        "kapali_islem_sayisi",
        "toplam_net_r",
        "komsular",
        "alan_disi_komsular",
        "eksik_komsular",
        "karli",
        "sinir",
        "uygun_merkez",
        "uzaklik",
        "en_kotu_komsu",
    }
    if not gerekli <= h.keys():
        raise PilotHatasi("Bölgenin hücre veya komşuluk açıklaması eksik.")
    for ad in ("komsular", "alan_disi_komsular", "eksik_komsular"):
        if not isinstance(h[ad], list) or any(i not in indeksler for i in h[ad]):
            raise PilotHatasi("Bölgenin komşu kimlikleri uyuşmuyor.")


def _arama_en_iyi_bagi(en_iyi, secilen, indeksler):
    if en_iyi is None:
        return
    if (
        not {"indeks", "secildi"} <= en_iyi.keys()
        or en_iyi["indeks"] not in indeksler
        or type(en_iyi["secildi"]) is not bool
        or en_iyi["secildi"] != (en_iyi["indeks"] == secilen)
    ):
        raise PilotHatasi("En iyi hücrenin açıklaması veya kimliği uyuşmuyor.")


def _arama_bolge_bileseni(c, indeksler):
    gerekli = {
        "indeksler",
        "buyukluk",
        "medyan_net_r",
        "uygun_merkezler",
        "kanonik_indeks",
    }
    if not gerekli <= c.keys():
        raise PilotHatasi("Bölgenin bileşen veya eşitlik açıklaması eksik.")
    for ad in ("indeksler", "uygun_merkezler"):
        if not isinstance(c[ad], list) or any(i not in indeksler for i in c[ad]):
            raise PilotHatasi("Bölgenin bileşen kimlikleri uyuşmuyor.")
    if c["kanonik_indeks"] not in c["indeksler"]:
        raise PilotHatasi("Bileşenin kanonik kimliği uyuşmuyor.")


def _arama_bolge_hucresi(h, bolge, ozet):
    d = next(d for d in h["donemler"] if kanonik(d["donem"]) == kanonik(bolge["donem"]))
    s = next((s for s in d["semboller"] if s["sembol"] == bolge["sembol"]), None)
    durum = s["durum"] if d["durum"] == "tamamlandi" and s else d["durum"]
    if h["durum"] == "alan_disi":
        durum = "alan_disi"
    if (ozet["deneme_id"], ozet["durum"]) != (h["deneme_id"], durum):
        raise PilotHatasi("Bölgenin çocuk veya dönem/hisse durumu uyuşmuyor.")


def _arama_secilen_cocuk(hucreler, bolge):
    if bolge["secilen"] is None:
        _metin(bolge["neden"])
        if bolge["secilen_deneme_id"] is not None:
            raise PilotHatasi("Seçilmemiş bölgede çocuk kimliği olamaz.")
        return
    h = next((h for h in hucreler if h["indeks"] == bolge["secilen"]), None)
    if (
        h is None
        or h["deneme_id"] is None
        or h["deneme_id"] != bolge["secilen_deneme_id"]
    ):
        raise PilotHatasi("Seçilen çocuk bölgenin hücresine bağlı değil.")
    _arama_secilen_donemi(h, bolge)


def _arama_secilen_donemi(h, bolge):
    d = next(d for d in h["donemler"] if kanonik(d["donem"]) == kanonik(bolge["donem"]))
    semboller = [s for s in d["semboller"] if s["sembol"] == bolge["sembol"]]
    if (
        d["durum"] != "tamamlandi"
        or len(semboller) != 1
        or semboller[0]["durum"] != "tamamlandi"
    ):
        raise PilotHatasi(
            "Seçilen çocuğun aynı dönem ve hissesi tamamlanmış olmalıdır."
        )


def _arama_kosu_sonucu(olaylar, kosu_id):
    return next(
        (
            o
            for o in olaylar
            if o.get("sonuc_turu") == "arama_v1" and o.get("kosu_id") == kosu_id
        ),
        None,
    )


def _arama_yayini(olaylar, makbuz, girdi):
    ust = _bul(olaylar, makbuz.deneme_id, "deneme", "deneme_id")
    if (
        _ayar_ozeti(_ayarlar(ust)) != makbuz.ayar_ozeti
        or ust["ayar_parmak_izi"] != makbuz.ayar_ozeti
    ):
        raise PilotHatasi("Üst arama ayarı veya özeti değişmiş.")
    baslangic = _arama_makbuzu(
        olaylar,
        asdict(makbuz),
        "baslangic",
        makbuz.deneme_id,
        makbuz.kosu_id,
        makbuz.ayar_ozeti,
    )
    if girdi["is_id"] != "arama" or girdi["is_id"] not in baslangic["is_listesi"]:
        raise PilotHatasi("Arama işi başlangıç listesinde yok.")
    if _arama_kosu_sonucu(olaylar, makbuz.kosu_id) is not None:
        raise PilotHatasi("Arama sonucu zaten kayıtlı.")
    eksenler = _arama_yontemi(ust, girdi["politika_surumu"])
    _arama_hucreleri(olaylar, ust, baslangic, girdi["hucreler"], eksenler)
    _arama_sonuc_referanslari(girdi)
    _arama_bolge_baglari(
        ust, girdi["hucreler"], girdi["bolgeler"], girdi["politika_surumu"]
    )


def _arama_sonuc_referanslari(girdi):
    refs = [
        d["sonuc_ref"]
        for h in girdi["hucreler"]
        for d in h["donemler"]
        if d["sonuc_ref"] is not None
    ]
    if girdi["cikti_referanslari"] != refs or len(set(refs)) != len(refs):
        raise PilotHatasi("Arama çıktı referansları dönem sonuçlarıyla uyuşmuyor.")


def _arama_bitisini_dogrula(olaylar, kosu_id, durum, tamamlanan, referanslar):
    if durum in ("hata", "iptal") and not tamamlanan and not referanslar:
        return
    sonuc = _arama_kosu_sonucu(olaylar, kosu_id)
    if sonuc is None:
        if durum == "tamamlandi" or tamamlanan:
            raise PilotHatasi("Arama yayımlanmadan işi tamamlandı sayılamaz.")
        return
    _arama_bitis_isleri(sonuc, tamamlanan, referanslar)


def _arama_bitis_isleri(sonuc, tamamlanan, referanslar):
    beklenen = {"arama"} | {
        h["is_id"]
        for h in sonuc["hucreler"]
        if h["durum"] in ("tamamlandi", "islemsiz")
    }
    if set(tamamlanan) != beklenen or referanslar != [sonuc["kayit_id"]]:
        raise PilotHatasi("Arama bitişi kayıtlı hücre sonuçlarıyla uyuşmuyor.")


@dataclass(frozen=True)
class Makbuz:
    olay_id: str
    deneme_id: str | None
    kosu_id: str | None
    ayar_ozeti: str | None
    uyarilar: list[str] = field(default_factory=list)


class PilotKayit:
    """E5 yalnız kaydeder; hesap işlevi almaz (TASARIM 5.15)."""

    def __init__(self, yol):
        self.yol = Path(yol).resolve()
        if self.yol.name == "deneme.jsonl":
            raise PilotHatasi("Eski deneme dosyası pilot alanı değildir.")

    @contextmanager
    def _kilit(self):
        self.yol.parent.mkdir(parents=True, exist_ok=True)
        with self.yol.with_suffix(self.yol.suffix + ".lock").open("a+b") as dosya:
            dosya.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(dosya.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl

                fcntl.flock(dosya.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                dosya.seek(0)
                if os.name == "nt":
                    msvcrt.locking(dosya.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(dosya.fileno(), fcntl.LOCK_UN)

    def _oku(self):
        if not self.yol.exists():
            return [], []
        olaylar, uyarilar = [], []
        for no, satir in enumerate(self.yol.read_bytes().splitlines(keepends=True), 1):
            if not satir.endswith(b"\n") or satir.endswith(_KESIK):
                uyarilar.append(f"Eksik satır: {no}")
                continue
            try:
                olay = _coz(json.loads(satir))
                if olay["sema_surumu"] != SURUM or kanonik(olay) + b"\n" != satir:
                    raise ValueError("Şema veya kodlama uyuşmuyor.")
            except (ValueError, KeyError, TypeError, IndexError) as hata:
                raise PilotHatasi(f"Bozuk tam satır: {no}") from hata
            olaylar.append(olay)
        return olaylar, uyarilar

    def oku(self):
        with self._kilit():
            return self._oku()[0]

    def deneme_oku(self, deneme_id):
        """TASARIM 5.15 S07: hesap öncesinde tam ayarı ve özgün özeti denetle."""
        try:
            kayit = _bul(self.oku(), deneme_id, "deneme", "deneme_id")
            _strateji_kaydi(kayit["strateji"])
            if _ayar_ozeti(_ayarlar(kayit)) != kayit["ayar_parmak_izi"]:
                raise PilotHatasi("Ayar özeti uyuşmuyor.")
            return kayit
        except OSError as hata:
            raise PilotYazmaHatasi(f"{deneme_id}: {hata}") from hata
        except (ValueError, KeyError, TypeError, AttributeError, OverflowError) as hata:
            raise PilotHatasi(
                f"{deneme_id}: eksik veya geçersiz ayar: {hata}"
            ) from hata

    def bag_kaydet(
        self,
        *,
        kosu_id,
        asama,
        deneme_id,
        ayar_ozeti,
        veri_ref,
        referanslar,
        icerik,
    ):
        """TASARIM 5.15 S07: çıktı biçimini değiştirmeyen ayrı bağlantı olayı."""
        if asama not in ("sinyal", "islem", "sonuc"):
            raise PilotHatasi(f"{kosu_id}: bilinmeyen aktarım aşaması")
        _metin(kosu_id)
        _metin(ayar_ozeti)
        _metin(veri_ref)
        if deneme_id is not None:
            kayit = self.deneme_oku(deneme_id)
            if kayit["ayar_parmak_izi"] != ayar_ozeti:
                raise PilotHatasi(f"{deneme_id}: ayar özeti uyuşmuyor")
        if (asama == "sinyal" and referanslar) or (
            asama == "islem" and len(referanslar) != 1
        ):
            raise PilotHatasi(f"{kosu_id}: geçersiz {asama} bağı")

        def denetle(olaylar):
            for ref in referanslar:
                onceki = _bul(olaylar, ref, "ayar_bagi")
                beklenen_asama = "sinyal" if asama == "islem" else "islem"
                if (
                    onceki["asama"] != beklenen_asama
                    or onceki["kosu_id"] != kosu_id
                    or onceki["deneme_id"] != deneme_id
                    or onceki["ayar_parmak_izi"] != ayar_ozeti
                    or onceki["veri_ref_id"] != veri_ref
                ):
                    raise PilotHatasi(f"{ref}: sinyal/işlem/sonuç ayar bağı uyuşmuyor")

        return self._ekle(
            {
                "kayit_turu": "ayar_bagi",
                "asama": asama,
                "kosu_id": kosu_id,
                "deneme_id": deneme_id,
                "ayar_parmak_izi": ayar_ozeti,
                "veri_ref_id": veri_ref,
                "referanslar": list(referanslar),
                "icerik": icerik,
                "kayit_durumu": "kayitli" if deneme_id is not None else "kayitsiz",
                "kaynaklar": kayit["kaynaklar"]
                if deneme_id is not None
                else [
                    {
                        "tur": "YORUM",
                        "konum": "docs/TASARIM.md#ayar-aktarımı",
                        "tarih": "2026-10-18",
                        "alinti": None,
                        "karar_durumu": "gecici_pilot",
                        "alinti_bos_nedeni": "S07 teknik aktarım kaydı; Tansu işlem kuralı değildir.",
                    }
                ],
                "bos_nedenleri": {"deneme_id": "kayitsiz_eski_yol"}
                if deneme_id is None
                else {},
            },
            denetle,
        )

    @contextmanager
    def kosu(
        self,
        deneme_id,
        *,
        mod,
        anlik_goruntu,
        manifest_ozeti,
        uyelik_surumu,
        kod_kimligi,
        ortam,
        bagimlilik_ozeti,
        tohum,
        is_listesi,
        ureteci_surumu=None,
    ):
        _kosu_meta_dogrula(
            (
                mod,
                anlik_goruntu,
                manifest_ozeti,
                uyelik_surumu,
                kod_kimligi,
                bagimlilik_ozeti,
            ),
            ortam,
            tohum,
            ureteci_surumu,
        )
        is_listesi = _is_listesi_dogrula(is_listesi)
        deneme = self.deneme_oku(deneme_id)
        if anlik_goruntu not in deneme["veri_ayarlari"]["veri_referanslari"]:
            raise PilotHatasi("Görüntü kayıtlı veri referansında yok.")
        if deneme["yontem_ayarlari"].get("tekrar", 0) and tohum is None:
            raise PilotHatasi("Tekrarlı yöntem için tohum gerekli.")
        baslangic = {
            "kayit_turu": "baslangic",
            "deneme_id": deneme_id,
            "kosu_id": f"{SURUM}:k:{uuid4()}",
            "ayar_parmak_izi": deneme["ayar_parmak_izi"],
            "mod": mod,
            "anlik_goruntu": anlik_goruntu,
            "manifest_ozeti": manifest_ozeti,
            "uyelik_surumu": uyelik_surumu,
            "kod_kimligi": kod_kimligi,
            "ortam": ortam,
            "bagimlilik_ozeti": bagimlilik_ozeti,
            "tohum": tohum,
            "ureteci_surumu": ureteci_surumu,
            "is_listesi": is_listesi,
            "kaynaklar": deneme["kaynaklar"],
            "bos_nedenleri": {
                "tohum": "Rastgele yöntem yok.",
                "ureteci_surumu": "Rastgele yöntem yok.",
            }
            if tohum is None
            else {},
        }
        makbuz = self._ekle(baslangic)
        kosu = _Kosu(self, makbuz, deneme, baslangic)
        try:
            yield kosu
            if kosu._yazma_hatasi:
                raise PilotYazmaHatasi("Koşu kayıt hatasıyla durdu.")
        except Exception as hata:
            if not kosu._bitti and not kosu._yazma_hatasi:
                kosu.bitir(
                    durum="hata",
                    tamamlanan=[],
                    basarisiz=is_listesi,
                    yontemler=[],
                    olculer={},
                    cikti_referanslari=[],
                    ozetler={"hata": str(hata)},
                )
            raise
        finally:
            kosu._etkin = False

    def izle(self, olay_id):
        olaylar = self.oku()
        sonuc = _bul(olaylar, olay_id)
        if sonuc["kayit_turu"] not in ("sonuc", "islem", "senaryo"):
            raise PilotHatasi("Hesap çıktısı gerekli.")
        baslangic = _bul(olaylar, sonuc["kosu_id"], "baslangic", "kosu_id")
        bitisler = [
            o
            for o in olaylar
            if o["kayit_turu"] == "bitis" and o["kosu_id"] == sonuc["kosu_id"]
        ]
        return {
            "sonuc": sonuc,
            "deneme": _bul(olaylar, sonuc["deneme_id"], "deneme", "deneme_id"),
            "baslangic": baslangic,
            "durum": bitisler[-1]["durum"] if bitisler else "cozumsuz",
            "duzeltmeler": [
                o
                for o in olaylar
                if o["kayit_turu"] == "duzeltme" and o["hedef_olay"] == olay_id
            ],
        }

    def duzelt(self, hedef_olay, *, gerekce, yeni_degerler):
        _metin(gerekce)
        if not isinstance(yeni_degerler, dict) or not yeni_degerler:
            raise PilotHatasi("Yeni değerler gerekli.")
        if yeni_degerler.keys() & {
            "kayit_id",
            "kayit_turu",
            "sema_surumu",
            "deneme_id",
            "kosu_id",
            "ayar_parmak_izi",
            "baglar",
            "strateji",
            "durum",
        }:
            raise PilotHatasi("Düzeltme kimlik, ayar veya durum değiştiremez.")
        try:
            hedef = _bul(self.oku(), hedef_olay)
        except OSError as hata:
            raise PilotYazmaHatasi(f"Pilot kaydı okunamadı: {hata}") from hata
        return self._ekle(
            {
                "kayit_turu": "duzeltme",
                "hedef_olay": hedef_olay,
                "neden": gerekce,
                "yeni_degerler": yeni_degerler,
                "deneme_id": hedef.get("deneme_id"),
                "kosu_id": hedef.get("kosu_id"),
                "ayar_parmak_izi": hedef.get("ayar_parmak_izi"),
                "kaynaklar": hedef["kaynaklar"],
                "bos_nedenleri": {"kosu_id": "Revizyon düzeltmesi."}
                if not hedef.get("kosu_id")
                else {},
            }
        )

    def kurtar(self):
        with self._kilit():
            olaylar, uyarilar = self._oku()
        biten = {o["kosu_id"] for o in olaylar if o["kayit_turu"] == "bitis"}
        return {
            "olaylar": olaylar,
            "uyarilar": uyarilar,
            "cozumsuz_kosular": [
                o["kosu_id"]
                for o in olaylar
                if o["kayit_turu"] == "baslangic" and o["kosu_id"] not in biten
            ],
        }

    def _ekle(self, olay, denetle=None):
        yayinlandi = False
        try:
            olay = {
                "kayit_id": f"{SURUM}:{uuid4()}",
                "sema_surumu": SURUM,
                "olusturma_zamani": datetime.now(timezone.utc),
                **olay,
            }
            satir = kanonik(olay)
            makbuz = Makbuz(
                olay["kayit_id"],
                olay.get("deneme_id"),
                olay.get("kosu_id"),
                olay.get("ayar_parmak_izi"),
            )
            with self._kilit():
                olaylar, _ = self._oku()
                if denetle:
                    denetle(olaylar)
                ham = self.yol.read_bytes() if self.yol.exists() else b""
                if ham and not ham.endswith(b"\n"):
                    satir = _KESIK + satir
                fd = os.open(
                    self.yol,
                    os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_BINARY", 0),
                    0o600,
                )
                try:
                    _icerik_yaz(fd, satir)
                    # TASARIM 5.15: LF yalnız aktarımı onaylanan içeriği görünür yapar.
                    yayinlandi = None
                    yayinlandi, hata = _lf_yaz(fd, len(ham) + len(satir) + 1)
                    if hata is not None:
                        raise hata
                finally:
                    os.close(fd)
        except Exception as hata:
            if yayinlandi is None:
                raise PilotBelirsizHatasi(makbuz) from hata
            if yayinlandi:
                makbuz.uyarilar.append(f"Kayıt eklendi, yazım sonrası hata: {hata}")
            elif isinstance(hata, OSError):
                raise PilotYazmaHatasi(f"Pilot kaydı yazılamadı: {hata}") from hata
            else:
                raise
        return makbuz

    def deneme_kaydet(
        self,
        varyant,
        *,
        aktor,
        gerekce,
        donemler,
        veri_ayarlari,
        yontem_ayarlari,
        risk_ayarlari,
        masraf_ayarlari,
        eski_referans,
        ust_deneme=None,
        baglar=None,
    ):
        _metin(aktor)
        _metin(gerekce)
        for ayar in (
            veri_ayarlari,
            yontem_ayarlari,
            risk_ayarlari,
            masraf_ayarlari,
            eski_referans,
        ):
            if not isinstance(ayar, dict):
                raise PilotHatasi("Ayarlar nesne olmalıdır.")
        if (
            not isinstance(donemler, list)
            or not donemler
            or not veri_ayarlari.get("veri_referanslari")
        ):
            raise PilotHatasi("Dönem ve veri referansı gerekli.")
        for donem in donemler:
            _donem(donem)
        tekrar = yontem_ayarlari.get("tekrar", 0)
        if type(tekrar) is not int or tekrar < 0:
            raise PilotHatasi("Tekrar negatif olmayan tamsayı olmalıdır.")
        for ad, deger in eski_referans.items():
            if deger is None:
                _metin(eski_referans.get("bos_nedenleri", {}).get(ad))
        _ondaliklar(risk_ayarlari)
        _ondaliklar(masraf_ayarlari)
        strateji = _strateji_kaydi(varyant)
        ayarlar = {
            "strateji": {k: v for k, v in strateji.items() if k != "olusturma_zamani"},
            "donemler": donemler,
            "veri_ayarlari": veri_ayarlari,
            "yontem_ayarlari": yontem_ayarlari,
            "risk_ayarlari": risk_ayarlari,
            "masraf_ayarlari": masraf_ayarlari,
        }
        baglar = {} if baglar is None else baglar
        if not isinstance(baglar, dict):
            raise PilotHatasi("Bağlar nesne olmalıdır.")
        if baglar.keys() - {"izgara_ust_deneme", "egitim_denemeleri", "test_deneme"}:
            raise PilotHatasi("Bilinmeyen deneme bağı.")
        if ("egitim_denemeleri" in baglar or "test_deneme" in baglar) and (
            not isinstance(baglar.get("egitim_denemeleri"), list)
            or not baglar["egitim_denemeleri"]
            or not baglar.get("test_deneme")
        ):
            raise PilotHatasi("WF eğitim ve sabit test denemeleri birlikte gereklidir.")
        referanslar = list(baglar.get("egitim_denemeleri", []))
        referanslar.extend(
            baglar[k] for k in ("izgara_ust_deneme", "test_deneme") if k in baglar
        )
        if ust_deneme:
            referanslar.append(ust_deneme)
        if "izgara_ust_deneme" in baglar and baglar["izgara_ust_deneme"] != ust_deneme:
            raise PilotHatasi("Izgara hücresi üst aramaya bağlı olmalıdır.")

        def denetle(olaylar):
            idler = {o["deneme_id"] for o in olaylar if o["kayit_turu"] == "deneme"}
            if any(r not in idler for r in referanslar):
                raise PilotHatasi("Deneme bağı bulunamadı.")

        return self._ekle(
            {
                "kayit_turu": "deneme",
                "deneme_id": f"{SURUM}:d:{uuid4()}",
                "kimlik_bicimi_surumu": SURUM,
                "olusturan": aktor,
                "neden": gerekce,
                **ayarlar,
                "strateji": strateji,
                "ust_deneme_id": ust_deneme,
                "eski_referans": eski_referans,
                "baglar": baglar,
                "kaynaklar": strateji["kaynaklar"],
                "bos_nedenleri": {"ust_deneme_id": "Kök deneme."}
                if ust_deneme is None
                else {},
                "ayar_parmak_izi": _ayar_ozeti(ayarlar),
            },
            denetle,
        )


def _bul(olaylar, kimlik, tur=None, alan="kayit_id"):
    for olay in olaylar:
        if olay.get(alan) == kimlik and (tur is None or olay["kayit_turu"] == tur):
            return olay
    raise PilotHatasi(f"Kayıt bağı bulunamadı: {kimlik}")


class _Kosu:
    def __init__(self, depo, makbuz, deneme, baslangic):
        self._depo, self.makbuz = depo, makbuz
        self._deneme, self._baslangic = deneme, baslangic
        self._etkin, self._bitti, self._yazma_hatasi = True, False, False

    def _yaz(self, tur, alanlar, denetle=None):
        if not self._etkin or self._bitti or self._yazma_hatasi:
            raise PilotHatasi("Koşu kapalı veya yazma hatalı.")

        def kontrol(olaylar):
            if any(
                o["kayit_turu"] == "bitis" and o["kosu_id"] == self.makbuz.kosu_id
                for o in olaylar
            ):
                raise PilotHatasi("Koşu zaten bitti.")
            if denetle:
                denetle(olaylar)

        try:
            return self._depo._ekle(
                {
                    "kayit_turu": tur,
                    "deneme_id": self.makbuz.deneme_id,
                    "kosu_id": self.makbuz.kosu_id,
                    "ayar_parmak_izi": self.makbuz.ayar_ozeti,
                    "kaynaklar": self._deneme["kaynaklar"],
                    **alanlar,
                },
                kontrol,
            )
        except PilotYazmaHatasi:
            self._yazma_hatasi = True
            raise

    def sonuc_kaydet(
        self,
        *,
        sinyal_id,
        islem_referanslari,
        donem,
        birimler,
        muhasebe_politikasi,
        uyarilar,
        cikti_referanslari,
        olculer,
    ):
        _metin(sinyal_id)
        _donem(donem)
        _metin(muhasebe_politikasi)
        if not isinstance(birimler, dict) or not birimler:
            raise PilotHatasi("Birimler gerekli.")
        if (
            not isinstance(islem_referanslari, list)
            or not isinstance(uyarilar, list)
            or not isinstance(cikti_referanslari, list)
        ):
            raise PilotHatasi("Sonuç referansları ve uyarılar liste olmalıdır.")

        def denetle(olaylar):
            for ref in islem_referanslari:
                islem = _bul(olaylar, ref, "islem")
                if islem["kosu_id"] != self.makbuz.kosu_id:
                    raise PilotHatasi("İşlem başka koşuya bağlı.")

        return self._yaz(
            "sonuc",
            {
                "sinyal_id": sinyal_id,
                "islem_referanslari": islem_referanslari,
                "donem": donem,
                "birimler": birimler,
                "muhasebe_politikasi": muhasebe_politikasi,
                "uyarilar": uyarilar,
                "cikti_referanslari": cikti_referanslari,
                "olculer": olculer,
                "veri_ref_id": self._baslangic["anlik_goruntu"],
            },
            denetle,
        )

    def donem_sonucu_kaydet(
        self,
        *,
        is_id,
        donem,
        durum,
        islem_referanslari,
        birimler,
        muhasebe_politikasi,
        uyarilar,
        cikti_referanslari,
        icerik,
    ):
        """TASARIM 5.15 S10: sinyalsiz dönem de kendi makbuzunu alır."""
        if is_id not in self._baslangic["is_listesi"]:
            raise PilotHatasi("Dönem işi başlangıç listesinde yok.")
        _donem(donem)
        if not any(kanonik(donem) == kanonik(d) for d in self._deneme["donemler"]):
            raise PilotHatasi("Dönem kayıtlı denemede yok.")
        _metin(muhasebe_politikasi)
        _donem_ciktisi_dogrula(
            durum, birimler, icerik, islem_referanslari, uyarilar, cikti_referanslari
        )

        def denetle(olaylar):
            kosu_id = self.makbuz.kosu_id
            _donem_yayini_dogrula(olaylar, kosu_id, is_id, donem)
            _donem_islem_baglari(olaylar, kosu_id, donem, islem_referanslari)
            _cocuk_sonuc_baglari(olaylar, kosu_id, cikti_referanslari)

        return self._yaz(
            "sonuc",
            dict(
                sonuc_turu="donem_v1",
                is_id=is_id,
                donem=donem,
                durum=durum,
                islem_referanslari=islem_referanslari,
                birimler=birimler,
                muhasebe_politikasi=muhasebe_politikasi,
                uyarilar=uyarilar,
                cikti_referanslari=cikti_referanslari,
                icerik=icerik,
                veri_ref_id=self._baslangic["anlik_goruntu"],
            ),
            denetle,
        )

    def arama_sonucu_kaydet(
        self,
        *,
        is_id,
        hucreler,
        bolgeler,
        politika_surumu,
        birimler,
        uyarilar,
        cikti_referanslari,
    ):
        """TASARIM 5.15 S11: gerçek çocuk sonuçlarını üst koşuya bağla."""
        if not isinstance(birimler, dict) or not birimler:
            raise PilotHatasi("Arama birimleri gerekli.")
        if any(
            not isinstance(v, list)
            for v in (hucreler, bolgeler, uyarilar, cikti_referanslari)
        ):
            raise PilotHatasi(
                "Arama hücreleri, bölgeleri ve referansları liste olmalıdır."
            )
        alanlar = dict(
            sonuc_turu="arama_v1",
            is_id=is_id,
            hucreler=hucreler,
            bolgeler=bolgeler,
            politika_surumu=politika_surumu,
            birimler=birimler,
            uyarilar=uyarilar,
            cikti_referanslari=cikti_referanslari,
            veri_ref_id=self._baslangic["anlik_goruntu"],
        )

        def denetle(olaylar):
            try:
                _arama_yayini(olaylar, self.makbuz, alanlar)
            except (KeyError, TypeError, AttributeError, IndexError) as hata:
                raise PilotHatasi(f"Arama bağı eksik veya geçersiz: {hata}") from hata

        return self._yaz("sonuc", alanlar, denetle)

    def islem_kaydet(
        self,
        *,
        sinyal_id,
        donem,
        birimler,
        muhasebe_politikasi,
        uyarilar,
        cikti_referanslari,
        olaylar,
    ):
        _metin(sinyal_id)
        _donem(donem)
        _metin(muhasebe_politikasi)
        if not olaylar or not birimler:
            raise PilotHatasi("İşlem olayları ve birimler gerekli.")
        return self._yaz(
            "islem",
            {
                "sinyal_id": sinyal_id,
                "donem": donem,
                "birimler": birimler,
                "muhasebe_politikasi": muhasebe_politikasi,
                "uyarilar": uyarilar,
                "cikti_referanslari": cikti_referanslari,
                "olaylar": olaylar,
                "veri_ref_id": self._baslangic["anlik_goruntu"],
            },
        )

    def senaryo_kaydet(self, *, sira, sonuc_referansi):
        tekrar = self._deneme["yontem_ayarlari"].get("tekrar", 0)
        if type(sira) is not int or not 0 <= sira < tekrar:
            raise PilotHatasi("Senaryo kayıtlı tekrar aralığında değil.")

        def denetle(olaylar):
            sonuc = _bul(olaylar, sonuc_referansi, "sonuc")
            if sonuc["kosu_id"] != self.makbuz.kosu_id:
                raise PilotHatasi("Senaryo sonucu başka koşuya bağlı.")
            if any(
                o["kayit_turu"] == "senaryo"
                and o["kosu_id"] == self.makbuz.kosu_id
                and o["sira"] == sira
                for o in olaylar
            ):
                raise PilotHatasi("Senaryo sırası yinelenmiş.")

        return self._yaz(
            "senaryo", {"sira": sira, "sonuc_referansi": sonuc_referansi}, denetle
        )

    def bitir(
        self,
        *,
        durum,
        tamamlanan,
        basarisiz,
        yontemler,
        olculer,
        cikti_referanslari,
        ozetler,
    ):
        if durum not in ("tamamlandi", "hata", "iptal"):
            raise PilotHatasi("Bitiş durumu tanımsız.")
        bildirilen = tamamlanan + basarisiz
        if len(set(bildirilen)) != len(bildirilen) or set(bildirilen) != set(
            self._baslangic["is_listesi"]
        ):
            raise PilotHatasi("Her iş bir kez muhasebeleştirilmelidir.")
        if durum == "tamamlandi" and basarisiz:
            raise PilotHatasi("Başarısız iş varken tamamlandı denemez.")

        def denetle(olaylar):
            if self._deneme["yontem_ayarlari"].get("yontem") == "kayitli_izgara_v1":
                _arama_bitisini_dogrula(
                    olaylar, self.makbuz.kosu_id, durum, tamamlanan, cikti_referanslari
                )

        makbuz = self._yaz(
            "bitis",
            {
                "durum": durum,
                "tamamlanan": tamamlanan,
                "basarisiz": basarisiz,
                "yontemler": yontemler,
                "olculer": olculer,
                "cikti_referanslari": cikti_referanslari,
                "ozetler": ozetler,
                "bitis_zamani": datetime.now(timezone.utc),
            },
            denetle,
        )
        self._bitti = True
        return makbuz
