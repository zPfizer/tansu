"""Geçici kayıt sınırı (TASARIM 5.15); kalıcı bayt biçimi #97'dir."""

from datetime import date, datetime, timezone
from decimal import Decimal
from contextlib import contextmanager, nullcontext
from copy import deepcopy
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


class PilotDayaniklilikHatasi(PilotYazmaHatasi):
    """S03 WF aktarımı doğrulanamadı; görünür makbuz geri alınamaz."""

    def __init__(self, makbuz):
        self.kayit_id = makbuz.olay_id
        super().__init__(f"WF dayanıklılığı belirsiz: {self.kayit_id}")


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
    if str(kayit["yontem_ayarlari"].get("yontem", "")).startswith(
        "kayitli_monte_carlo"
    ):
        _mc_yontemi(kayit["yontem_ayarlari"])
    # TASARIM 5.15 #178: kayıtlı yöntem/veri çifti E1 öncesi doğrulanır.
    from tansu.tansusinama import _isinma_secimi_dogrula

    if not str(kayit["yontem_ayarlari"].get("yontem", "")).startswith(
        "kayitli_monte_carlo"
    ):
        _isinma_secimi_dogrula(kayit["veri_ayarlari"], kayit["yontem_ayarlari"])
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


def _mc_alanlar(kayit, alanlar):
    if not isinstance(kayit, dict) or set(kayit) != set(alanlar.split()):
        raise PilotHatasi(f"MC alanları eksik veya bilinmeyen: {alanlar}")


def _mc_ozet(kayit):
    return sha256(kanonik(kayit)).hexdigest()


def _mc_ozet_dogrula(ozet):
    if (
        not isinstance(ozet, str)
        or len(ozet) != 64
        or any(c not in "0123456789abcdef" for c in ozet)
    ):
        raise PilotHatasi("MC içerik özeti SHA-256 olmalıdır.")


def _mc_yontemi(y):
    """TASARIM 5.15 S13: ayrı, tam yöntem şeması; legacy yöntemler değişmez."""
    from tansu.istatistik import MC_DENEYLER, MC_NOKTALAR, MC_URETEC

    _mc_alanlar(
        y,
        "yontem tekrar kontrol_noktalari calisma_turu tohum uretec akis_surumu muhasebe_politikasi hassasiyet_r deneyler kaynak",
    )
    on_gosterim = y["calisma_turu"] == "on_gosterim"
    if y["calisma_turu"] not in ("on_gosterim", "nihai") or y != dict(
        yontem="kayitli_monte_carlo_v1",
        tekrar=1000 if on_gosterim else 100000,
        kontrol_noktalari=[1000] if on_gosterim else list(MC_NOKTALAR),
        calisma_turu=y["calisma_turu"],
        tohum=y["tohum"],
        uretec=MC_URETEC,
        akis_surumu="indeksli_v1",
        muhasebe_politikasi="kapali_gerceklesme_gunluk_r_v1",
        hassasiyet_r=0.01,
        deneyler=list(MC_DENEYLER),
        kaynak=y["kaynak"],
    ):
        raise PilotHatasi("Desteklenmeyen MC yöntem ayarı.")
    if (
        type(y["tohum"]) is not int
        or y["tohum"] < 0
        or type(y["tekrar"]) is not int
        or any(type(n) is not int for n in y["kontrol_noktalari"])
    ):
        raise PilotHatasi("MC tohumu ve bütçesi tamsayı olmalıdır.")
    _mc_alanlar(y["kaynak"], "deneme_id kosu_id sonuc_ref bitis_ref icerik_ozeti")
    for ad in ("deneme_id", "kosu_id", "sonuc_ref", "bitis_ref"):
        _metin(y["kaynak"][ad])
    _mc_ozet_dogrula(y["kaynak"]["icerik_ozeti"])


def _mc_baslangic_mi(olaylar, o):
    from tansu.istatistik import MC_URETEC

    return o["kayit_turu"] == "baslangic" and (
        str(o.get("kod_kimligi", "")).startswith("kayitli_monte_carlo")
        or o.get("ureteci_surumu") == MC_URETEC
        or any(
            e["kayit_turu"] == "deneme"
            and str(e["yontem_ayarlari"].get("yontem", "")).startswith(
                "kayitli_monte_carlo"
            )
            and (
                e["deneme_id"] == o.get("deneme_id")
                or e["ayar_parmak_izi"] == o.get("ayar_parmak_izi")
            )
            for e in olaylar
        )
    )


def _mc_baslangic_dogrula(olaylar, o):
    _mc_alanlar(
        o,
        "kayit_id sema_surumu olusturma_zamani kayit_turu deneme_id kosu_id ayar_parmak_izi mod anlik_goruntu manifest_ozeti uyelik_surumu kod_kimligi ortam bagimlilik_ozeti tohum ureteci_surumu is_listesi kaynaklar bos_nedenleri",
    )
    d = _bul(olaylar, o["deneme_id"], "deneme", "deneme_id")
    y, v = d["yontem_ayarlari"], d["veri_ayarlari"]
    _mc_yontemi(y)
    _mc_ayni_kosu(o, d, o)
    _kosu_meta_dogrula(
        tuple(
            o[k]
            for k in (
                "mod",
                "anlik_goruntu",
                "manifest_ozeti",
                "uyelik_surumu",
                "kod_kimligi",
                "bagimlilik_ozeti",
            )
        ),
        o["ortam"],
        o["tohum"],
        o["ureteci_surumu"],
    )
    _is_listesi_dogrula(o["is_listesi"])
    if (
        o["tohum"] != y["tohum"]
        or o["ureteci_surumu"] != y["uretec"]
        or o["manifest_ozeti"] != v.get("manifest_ozeti")
        or o["anlik_goruntu"] not in v["veri_referanslari"]
        or o["uyelik_surumu"] != v.get("uyelik_surumu")
        or o["kaynaklar"] != d["kaynaklar"]
        or o["bos_nedenleri"] != {}
        or not o["kod_kimligi"].startswith("kayitli_monte_carlo_v1:sha256:")
        or any(
            e["kayit_turu"] == "baslangic" and e["kosu_id"] == o["kosu_id"]
            for e in olaylar
        )
    ):
        raise PilotHatasi(
            "MC başlangıcının değişmez yöntem, veri veya koşu bağı uyuşmuyor."
        )
    _mc_ozet_dogrula(o["kod_kimligi"].removeprefix("kayitli_monte_carlo_v1:sha256:"))
    if v.get("ilk_islem") is not None:
        from tansu.tansusinama import _ileri_uyelik_kaniti_dogrula

        kaynak = _mc_isinma_kaynagi(olaylar, d)
        bas = _bul(olaylar, y["kaynak"]["kosu_id"], "baslangic", "kosu_id")
        _mc_ayni_kosu(bas, kaynak, bas)
        _ileri_uyelik_kaniti_dogrula(v, bas.get("uyelik_kaniti"))


def _mc_ayni_kosu(o, d, b):
    if (b["deneme_id"], b["ayar_parmak_izi"]) != (
        d["deneme_id"],
        d["ayar_parmak_izi"],
    ) or (o["deneme_id"], o["kosu_id"], o["ayar_parmak_izi"]) != (
        d["deneme_id"],
        b["kosu_id"],
        d["ayar_parmak_izi"],
    ):
        raise PilotHatasi("MC başvurusu başka koşuya veya ayara bağlı.")


def _mc_kaynagi(olaylar, kaynak, *, ozet_denetle=True):
    """TASARIM 5.15 S13: yalnız gerçek tamamlanmış WF olaylarının kayıt bağları."""
    from tansu import motor

    try:
        d = _bul(olaylar, kaynak["deneme_id"], "deneme", "deneme_id")
        b = _bul(olaylar, kaynak["kosu_id"], "baslangic", "kosu_id")
        s = _bul(olaylar, kaynak["sonuc_ref"], "sonuc")
        f = _bul(olaylar, kaynak["bitis_ref"], "bitis")
    except (PilotHatasi, KeyError) as hata:
        raise PilotHatasi(f"kaynak_wf_yok: {hata}") from hata
    if (
        d["yontem_ayarlari"].get("yontem") != "kayitli_ileri_v1"
        or s.get("sonuc_turu") != "ileri_v1"
    ):
        raise PilotHatasi("MC kaynağı kayıtlı WF birleşik sonucu olmalıdır.")
    _ileri_ust(d)
    if _ayar_ozeti(_ayarlar(d)) != d["ayar_parmak_izi"]:
        raise PilotHatasi("WF kaynak tam ayar özeti uyuşmuyor.")
    for o in (b, s, f):
        _mc_ayni_kosu(o, d, b)
    k = s["kayit"]
    isler = [x["ad"] for x in d["donemler"]] + ["birlesik"]
    if (
        (k["tur"], k["bolum_id"], k["durum"], f["durum"])
        != ("birlesik", "birlesik", "tamamlandi", "tamamlandi")
        or f["tamamlanan"] != isler
        or f["basarisiz"]
        or f["cikti_referanslari"] != [s["kayit_id"]]
        or b["is_listesi"] != isler
    ):
        raise PilotHatasi("WF kaynak kapsamı ve bitişi tamamlanmış değil.")
    m = Makbuz(b["kayit_id"], d["deneme_id"], b["kosu_id"], d["ayar_parmak_izi"])
    _ileri_sonucu_dogrula(olaylar[: olaylar.index(s)], d, m, k)
    bolumler = [_bul(olaylar, r, "sonuc") for r in k["bolum_refleri"]]
    if [o["kayit"]["bolum_id"] for o in bolumler] != isler[:-1] or len(
        {o["kayit_id"] for o in bolumler}
    ) != 16:
        raise PilotHatasi("WF kaynak bölümleri eksik veya yinelenmiş.")
    secimler = []
    for o in bolumler:
        _mc_ayni_kosu(o, d, b)
        q = o["kayit"]
        if (
            o.get("sonuc_turu") != "ileri_v1"
            or q["tur"] != "bolum"
            or q["durum"] != "tamamlandi"
        ):
            raise PilotHatasi("WF kaynak bölümünün türü veya durumu geçersiz.")
        on = olaylar[: olaylar.index(o)]
        _ileri_sonucu_dogrula(on, d, m, q)
        _isinma_olayi_dogrula(on, o)
        donem = next(x for x in d["donemler"] if x["ad"] == q["bolum_id"])
        gunler = [
            t
            for t in d["veri_ayarlari"]["takvim"]["seanslar"]
            if donem["baslangic"].isoformat() <= t <= donem["bitis"].isoformat()
        ]
        uyelik = q["uyelik"]
        if (
            set(uyelik["gunler"]) != set(gunler)
            or uyelik["tablo_parmak_izi"] != d["veri_ayarlari"]["uyelik_ozeti"]
            or q["veri_referansi"]["manifest_parmak_izi"]
            != d["veri_ayarlari"]["manifest_ozeti"]
            or q["hatalar"]
            or (
                d["veri_ayarlari"].get("ilk_islem") is None
                and any(not x["tamam"] for x in q["isinma"].values())
            )
        ):
            raise PilotHatasi("WF günlük veri, üyelik, ısınma veya hata kapsamı eksik.")
        for secim in q["secimler"]:
            e = _bul(olaylar, secim["secim_ref"], "ileri_secim")
            _mc_ayni_kosu(e, d, b)
            if e.get("surum") != "ileri_secim_v1" or e["kayit"] != {
                a: v for a, v in secim.items() if a != "secim_ref"
            }:
                raise PilotHatasi("WF seçim açıklaması gerçek makbuzla uyuşmuyor.")
            _ileri_secimi_dogrula(olaylar[: olaylar.index(e)], d, m, e["kayit"])
            secimler.append(e)
    if len({(e["bolum_id"], e["sembol"]) for e in secimler}) != len(secimler):
        raise PilotHatasi("WF kaynak seçimi yinelenmiş.")
    sinyaller = [
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_sinyal" and o["kosu_id"] == b["kosu_id"]
    ]
    for o in sinyaller:
        _mc_ayni_kosu(o, d, b)
        secim, cocuk = _ileri_sinyal_bagi(olaylar, d, m, o["secim_ref"])
        if (
            o.get("surum") != "ileri_sinyal_v1"
            or secim not in secimler
            or (
                o["test_deneme_id"],
                o["deneme_ayar_parmak_izi"],
                o["strateji_ayar_parmak_izi"],
                o["sembol"],
                o["karar_bolumu"],
            )
            != (
                cocuk["deneme_id"],
                cocuk["ayar_parmak_izi"],
                cocuk["strateji"]["ayar_parmak_izi"],
                secim["sembol"],
                secim["bolum_id"],
            )
        ):
            raise PilotHatasi("WF kaynak sinyalinin seçim veya ayar bağı uyuşmuyor.")
        p = motor._duz({a["ad"]: a["deger"] for a in cocuk["strateji"]["parametreler"]})
        if o["sinyal"]["parametreler"] != p or (
            o["sinyal"]["sembol"],
            o["sinyal"]["tarih"],
        ) != (o["sembol"], o["tarih"]):
            raise PilotHatasi("WF kaynak sinyalinin tam parametresi uyuşmuyor.")
    islemler = [_bul(olaylar, r["kayit_ref"], "islem") for r in k["islem_refleri"]]
    yayinlar = [
        o
        for o in olaylar
        if o["kayit_turu"] == "islem"
        and o.get("kosu_id") == b["kosu_id"]
        and o.get("islem_turu") == "ileri_islem_v1"
    ]
    if {o["kayit_id"] for o in yayinlar} != {o["kayit_id"] for o in islemler} or len(
        {o["islem_id"] for o in yayinlar}
    ) != len(yayinlar):
        raise PilotHatasi("WF nihai işlem yayını eksik veya yinelenmiş.")
    nufus, acik, anlam = [], [], []
    for o in islemler:
        _mc_ayni_kosu(o, d, b)
        i = o["olaylar"][0]
        p, r = i["pozisyon"], i["sonuc"]
        sinyal = _ileri_pozisyon_bagi(olaylar, d, m, p)
        if (o["sinyal_id"], o["islem_id"], o["sembol"], o["karar_bolumu"]) != (
            sinyal["kayit_id"],
            p["risk_girdisi"]["islem_id"],
            sinyal["sembol"],
            sinyal["karar_bolumu"],
        ):
            raise PilotHatasi("WF işlem sahibinin sinyal bağı uyuşmuyor.")
        if o["rol"] == "tamamlanmis_islem":
            if (
                r["kalan_adet"] != 0
                or not r["alinan_adet"] > 0
                or any(
                    type(r[a]) not in (int, float) or not math.isfinite(r[a])
                    for a in ("ilk_risk", "net_r")
                )
                or r["ilk_risk"] <= 0
                or not i["dolumlar"]
                or i["dolumlar"][0]["yon"] != "alis"
            ):
                raise PilotHatasi(
                    "WF kapalı işlemin gerçek giriş veya nihai R dayanağı eksik."
                )
            nufus.append(
                dict(
                    islem_ref=o["kayit_id"],
                    islem_id=o["islem_id"],
                    sembol=o["sembol"],
                    giris_tarih=p["giris_tarih"],
                    cikis_tarih=p["cikis_tarih"],
                    net_r=r["net_r"],
                    ilk_risk=r["ilk_risk"],
                    giris_kohortu=o["giris_kohortu"],
                    karar_bolumu=o["karar_bolumu"],
                )
            )
        elif o["rol"] == "acik_ufuk" and r["kalan_adet"] > 0 and r["net_r"] is None:
            acik.append(o["kayit_id"])
        else:
            raise PilotHatasi("WF açık/kapalı rolü sonuçla uyuşmuyor.")
        anlam.append(
            dict(
                sembol=o["sembol"],
                rol=o["rol"],
                giris=p["giris_tarih"],
                cikis=p["cikis_tarih"],
                karar_bolumu=o["karar_bolumu"],
                giris_kohortu=o["giris_kohortu"],
                parametreler=sinyal["sinyal"]["parametreler"],
                sonuc={a: v for a, v in r.items() if a != "gerceklesen_kismi_sonuclar"}
                | dict(
                    gerceklesen_kismi_sonuclar=[
                        {a: v for a, v in z.items() if a != "dolum_id"}
                        for z in r.get("gerceklesen_kismi_sonuclar", [])
                    ]
                ),
                dolumlar=[
                    {a: v for a, v in z.items() if a != "dolum_id"}
                    for z in i["dolumlar"]
                ],
            )
        )
    kontroller = [
        _bul(olaylar, r["kayit_ref"], "ileri_kontrol") for r in k["kontrol_refleri"]
    ]
    for o in kontroller:
        _mc_ayni_kosu(o, d, b)
        if o.get("surum") != "ileri_kontrol_v1":
            raise PilotHatasi("WF kaynak checkpoint türü uyuşmuyor.")
        motor._durumu_oku(o["durum"], o["durum"]["yurutme"])
        p = o["durum"]["pozisyon"]
        if p:
            _ileri_pozisyon_bagi(olaylar, d, m, p)
    nufus.sort(
        key=lambda r: (r["cikis_tarih"], r["sembol"], r["giris_tarih"], r["islem_id"])
    )
    secim_anlami = []
    for e in sorted(secimler, key=lambda e: (e["bolum_id"], e["sembol"])):
        q = e["kayit"]
        test = (
            _bul(olaylar, q["test_deneme_id"], "deneme", "deneme_id")
            if q["test_deneme_id"]
            else None
        )
        secim_anlami.append(
            dict(
                bolum=e["bolum_id"],
                sembol=e["sembol"],
                durum=q["durum"],
                strateji=_ayarlar(test)["strateji"] if test else None,
            )
        )
    icerik = dict(
        ayarlar=_ayarlar(d),
        secimler=secim_anlami,
        islemler=sorted(
            anlam, key=lambda x: (x["sembol"], x["giris"] or "", x["cikis"] or "")
        ),
    )
    ozet = _mc_ozet(icerik)
    if ozet_denetle and kaynak["icerik_ozeti"] != ozet:
        raise PilotHatasi("WF kaynak içerik özeti uyuşmuyor.")
    return dict(
        deneme=d,
        baslangic=b,
        sonuc=s,
        bitis=f,
        nufus=nufus,
        acik=acik,
        secimler=secimler,
        sinyaller=sinyaller,
        kontroller=kontroller,
        icerik_ozeti=ozet,
    )


_MC_ALANLAR = {
    "mc_girdi": "kaynak kaynak_ozeti nufus acik_referanslari secim_referanslari sinyal_referanslari kontrol_referanslari seanslar semboller gunluk_r gunluk_islemler kapsam isler",
    "mc_plan": "girdi_ref anahtar indeks cekilis stres_cocuklari",
    "mc_sinyal": "plan_ref secim_ref deneme_id bolum sembol tarih sinyal",
    "mc_senaryo": "plan_ref durum olculer sembol_olculeri yeniden_sinama sonuc_referanslari asama neden",
    "mc_kontrol": "girdi_ref anahtar onceki_ref sonuc_referanslari tani",
    "mc_ozet": "girdi_ref isler uyarilar",
    "mc_parti": "kayitlar",
}


def _mc_olculer(o):
    _mc_alanlar(o, "toplam_r dusus_r ortalama_r islem_sayisi kayip_serisi")
    for ad, birim in (
        ("toplam_r", "R"),
        ("dusus_r", "R"),
        ("ortalama_r", "R"),
        ("islem_sayisi", "adet"),
        ("kayip_serisi", o["kayip_serisi"]["birim"]),
    ):
        v = o[ad]
        _mc_alanlar(v, "deger birim bos_nedeni")
        if (
            v["birim"] != birim
            or (
                v["deger"] is None
                and (ad != "ortalama_r" or v["bos_nedeni"] != "islem_yok")
            )
            or (
                v["deger"] is not None
                and (
                    type(v["deger"]) not in (int, float)
                    or not math.isfinite(v["deger"])
                    or v["bos_nedeni"] is not None
                )
            )
        ):
            raise PilotHatasi(
                "MC ölçüsünün birimi, değeri veya boşluk nedeni geçersiz."
            )
    if o["kayip_serisi"]["birim"] not in ("islem", "seans"):
        raise PilotHatasi("MC kayıp serisinin birimi geçersiz.")
    if o["dusus_r"]["deger"] < 0 or any(
        type(o[a]["deger"]) is not int or o[a]["deger"] < 0
        for a in ("islem_sayisi", "kayip_serisi")
    ):
        raise PilotHatasi("MC düşüşü ve sayıları negatif olamaz.")


def _mc_onek(olaylar=()):
    """TASARIM 5.15 S13: yalnız bu okumanın doğrulanmış önceki kayıtları."""
    onek = dict(
        kimlikler=set(),
        baglar={},
        roller={},
        isler={},
        sonuc_planlari=set(),
        sirali_sonuc_isleri=set(),
    )
    for o in olaylar:
        _mc_onege_ekle(onek, o)
    return onek


def _mc_onege_ekle(onek, o):
    tur = o["kayit_turu"]
    for alan in ("kayit_id", "deneme_id", "kosu_id"):
        if alan == "deneme_id" and tur != "deneme":
            continue
        if alan == "kosu_id" and tur != "baslangic":
            continue
        if isinstance(o.get(alan), str):
            onek["baglar"].setdefault((alan, tur, o[alan]), o)
    if isinstance(o.get("kayit_id"), str):
        onek["kimlikler"].add(o["kayit_id"])
    kosu = o.get("kosu_id")
    if not isinstance(kosu, str):
        return
    onek["roller"].setdefault((tur, kosu), []).append(o)
    if tur in ("mc_plan", "mc_kontrol"):
        onek["isler"].setdefault((tur, kosu, o["kayit"]["anahtar"]), []).append(o)
        if tur == "mc_plan" and not isinstance(o["kayit_id"], str):
            onek["sirali_sonuc_isleri"].add((kosu, o["kayit"]["anahtar"]))
    elif tur == "mc_senaryo":
        ref = o["kayit"]["plan_ref"]
        p = (
            onek["baglar"][("kayit_id", "mc_plan", ref)]
            if isinstance(ref, str)
            else next(
                p for p in onek["roller"][("mc_plan", kosu)] if p["kayit_id"] == ref
            )
        )
        onek["isler"].setdefault((tur, kosu, p["kayit"]["anahtar"]), []).append(o)
        if isinstance(ref, str):
            onek["sonuc_planlari"].add(ref)


def _mc_bul(olaylar, kimlik, tur, alan="kayit_id", *, onek=None):
    if onek is None or not isinstance(kimlik, str):
        return _bul(olaylar, kimlik, tur, alan)
    try:
        return onek["baglar"][(alan, tur, kimlik)]
    except KeyError:
        raise PilotHatasi(f"Kayıt bağı bulunamadı: {kimlik}") from None


def _mc_kimlik_var(olaylar, kimlik, onek):
    if isinstance(kimlik, str):
        return kimlik in onek["kimlikler"]
    return any(o["kayit_id"] == kimlik for o in olaylar)


def _mc_rol_kayitlari(olaylar, tur, kosu_id, *, anahtar=None, onek=None):
    if onek is not None and isinstance(kosu_id, str):
        if anahtar is not None:
            return onek["isler"].get((tur, kosu_id, anahtar), [])
        return onek["roller"].get((tur, kosu_id), [])
    return [
        o
        for o in olaylar
        if o["kayit_turu"] == tur
        and o.get("kosu_id") == kosu_id
        and (anahtar is None or o["kayit"]["anahtar"] == anahtar)
    ]


def _mc_ref(olaylar, ref, tur, d, b, *, onek=None):
    o = _mc_bul(olaylar, ref, tur, onek=onek)
    _mc_ayni_kosu(o, d, b)
    return o["kayit"]


def _mc_girdi_dogrula(olaylar, d, b, k, *, onek=None):
    from tansu.istatistik import mc_isleri

    kaynak = _mc_kaynagi(olaylar, d["yontem_ayarlari"]["kaynak"])
    for a in ("strateji", "veri_ayarlari", "risk_ayarlari", "masraf_ayarlari"):
        if kanonik(_ayarlar(d)[a]) != kanonik(_ayarlar(kaynak["deneme"])[a]):
            raise PilotHatasi(f"MC kaynakla aynı donmuş ayarı kullanmalıdır: {a}")
    if (
        k["kaynak"] != d["yontem_ayarlari"]["kaynak"]
        or k["kaynak_ozeti"] != kaynak["icerik_ozeti"]
        or k["nufus"] != kaynak["nufus"]
        or k["acik_referanslari"] != kaynak["acik"]
    ):
        raise PilotHatasi("MC girdi nüfusu gerçek WF kaynağıyla uyuşmuyor.")
    for alan, tur in (
        ("secim_referanslari", "secimler"),
        ("sinyal_referanslari", "sinyaller"),
        ("kontrol_referanslari", "kontroller"),
    ):
        if k[alan] != [o["kayit_id"] for o in kaynak[tur]]:
            raise PilotHatasi("MC kaynak başvuruları eksik veya sırası farklı.")
    _mc_alanlar(k["kapsam"], "baslangic bitis muhasebe_politikasi")
    if k["kapsam"] != dict(
        baslangic="2022-01-01",
        bitis="2025-12-31",
        muhasebe_politikasi="kapali_gerceklesme_gunluk_r_v1",
    ):
        raise PilotHatasi("MC OOS kapsamı geçersiz.")
    seanslar = [
        t
        for t in kaynak["deneme"]["veri_ayarlari"]["takvim"]["seanslar"]
        if "2022-01-01" <= t <= "2025-12-31"
    ]
    semboller = sorted(
        {o["sembol"] for o in kaynak["secimler"]}
        | {o["sembol"] for o in kaynak["kontroller"]}
    )
    if k["seanslar"] != seanslar or k["semboller"] != semboller:
        raise PilotHatasi("MC günlük takvim veya hisse kapsamı eksik.")
    degerler = [[0.0 for _ in semboller] for _ in seanslar]
    refler = [[[] for _ in semboller] for _ in seanslar]
    for r in k["nufus"]:
        i, j = seanslar.index(r["cikis_tarih"]), semboller.index(r["sembol"])
        degerler[i][j] += r["net_r"]
        refler[i][j].append(r["islem_ref"])
    if (k["gunluk_r"], k["gunluk_islemler"]) != (degerler, refler):
        raise PilotHatasi("MC günlük kapalı gerçekleşme kaynakla uyuşmuyor.")
    anahtarlar = []
    for is_ in k["isler"]:
        _mc_alanlar(
            is_, "anahtar tanim deney dilim sembol blok durum neden blok_tahmini"
        )
        if is_["deney"] == "ortak_tarih_blok_v1":
            _mc_alanlar(is_["blok_tahmini"], "yontem ham uzunluklar neden girdi_ozeti")
            _mc_ozet_dogrula(is_["blok_tahmini"]["girdi_ozeti"])
        elif is_["blok_tahmini"] is not None:
            raise PilotHatasi("MC blok tahmini yalnız tarih blok işine aittir.")
        t = is_["tanim"]
        _mc_alanlar(t, "yontem kaynak_ozeti nufus_kurali kapsam dilim deney varyant")
        _mc_alanlar(t["varyant"], "blok")
        if t != dict(
            yontem="kayitli_monte_carlo_v1",
            kaynak_ozeti=k["kaynak_ozeti"],
            nufus_kurali="nihai_kapanis_dilimi_v1",
            kapsam=is_["sembol"],
            dilim=dict(
                ad=is_["dilim"],
                baslangic=next(
                    x["baslangic"] for x in d["donemler"] if x["ad"] == is_["dilim"]
                ),
                bitis=next(
                    x["bitis"] for x in d["donemler"] if x["ad"] == is_["dilim"]
                ),
                kesim=next(
                    (t for t in reversed(seanslar) if t[:4] == is_["dilim"]),
                    seanslar[-1],
                ),
            ),
            deney=is_["deney"],
            varyant=dict(blok=is_["blok"]),
        ) or is_["anahtar"] != _mc_ozet(t):
            raise PilotHatasi("MC anlamsal deney anahtarı uyuşmuyor.")
        if (
            is_["deney"] not in d["yontem_ayarlari"]["deneyler"]
            or is_["dilim"] not in [x["ad"] for x in d["donemler"]]
            or is_["sembol"] not in [*semboller, "eklemeli"]
            or is_["durum"] not in ("hazir", "olculemedi")
            or (is_["durum"] == "hazir") != (is_["neden"] is None)
        ):
            raise PilotHatasi("MC iş kapsamı veya kullanılabilirlik durumu geçersiz.")
        anahtarlar.append(is_["anahtar"])
    if anahtarlar != b["is_listesi"] or len(set(anahtarlar)) != len(anahtarlar):
        raise PilotHatasi("MC gerekli iş listesi başlangıçla uyuşmuyor.")
    for dilim in d["donemler"]:
        if {x["deney"] for x in k["isler"] if x["dilim"] == dilim["ad"]} != set(
            d["yontem_ayarlari"]["deneyler"]
        ):
            raise PilotHatasi("MC diliminde gerekli deney eksik.")
    if kanonik(k["isler"]) != kanonik(
        mc_isleri(
            k,
            d["donemler"],
            secim_var=any(o["kayit"]["durum"] == "secildi" for o in kaynak["secimler"]),
        )
    ):
        raise PilotHatasi(
            "MC gerekli hisse/dilim/blok işleri veya kullanılabilirlik gerekçesi eksik."
        )


def _mc_plan_dogrula(olaylar, d, b, k, *, onek=None):
    from tansu.istatistik import mc_plan

    g = _mc_ref(olaylar, k["girdi_ref"], "mc_girdi", d, b, onek=onek)
    is_ = next((i for i in g["isler"] if i["anahtar"] == k["anahtar"]), None)
    if (
        is_ is None
        or is_["durum"] != "hazir"
        or type(k["indeks"]) is not int
        or not 0 <= k["indeks"] < d["yontem_ayarlari"]["tekrar"]
    ):
        raise PilotHatasi("MC planının kayıtlı işi veya indeksi geçersiz.")
    onceki = _mc_rol_kayitlari(
        olaylar, "mc_plan", b["kosu_id"], anahtar=k["anahtar"], onek=onek
    )
    if k["indeks"] != len(onceki):
        raise PilotHatasi("MC plan indeksi yinelenmiş veya öneği kesiyor.")
    if any(
        o["kayit"]["durum"] == "hata"
        for o in _mc_is_sonuclari(olaylar, b["kosu_id"], k["anahtar"], onek=onek)
    ):
        raise PilotHatasi("MC başarısız indeks sonrasında yeni plan çekilemez.")
    _mc_alanlar(k["cekilis"], "indeksler maske demet_indeksleri")
    if not isinstance(k["stres_cocuklari"], list):
        raise PilotHatasi("MC stres çocukları liste olmalıdır.")
    if is_["deney"] != "ayar_komsulugu_v1":
        if k["stres_cocuklari"]:
            raise PilotHatasi("Bu MC deneyinde stres çocuğu olamaz.")
        dilim = next(x for x in d["donemler"] if x["ad"] == is_["dilim"])
        seans = [
            t
            for t in g["seanslar"]
            if dilim["baslangic"].isoformat() <= t <= dilim["bitis"].isoformat()
        ]
        nufus = [
            r
            for r in g["nufus"]
            if r["cikis_tarih"] in seans
            and (is_["sembol"] == "eklemeli" or r["sembol"] == is_["sembol"])
        ]
        n = len(seans) if is_["deney"] == "ortak_tarih_blok_v1" else len(nufus)
        beklenen = mc_plan(
            is_["deney"],
            k["anahtar"],
            k["indeks"],
            n=n,
            tohum=d["yontem_ayarlari"]["tohum"],
            blok=is_["blok"],
        )
        if k["cekilis"] != beklenen:
            raise PilotHatasi("MC kayıtlı çekilişi indeksli üreteçle uyuşmuyor.")
    else:
        _mc_stres_cocuklari(olaylar, d, b, g, is_, k)


def _mc_senaryo_dogrula(olaylar, d, b, k, *, onek=None):
    p = _mc_ref(olaylar, k["plan_ref"], "mc_plan", d, b, onek=onek)
    onceki = _mc_is_sonuclari(olaylar, b["kosu_id"], p["anahtar"], onek=onek)
    if p["indeks"] != len(onceki) or any(o["kayit"]["durum"] == "hata" for o in onceki):
        raise PilotHatasi("MC sonuçları tamamlanmış öneği korumalıdır.")
    yinelenen = (
        k["plan_ref"] in onek["sonuc_planlari"]
        if onek is not None and isinstance(k["plan_ref"], str)
        else any(
            o["kayit_turu"] == "mc_senaryo" and o["kayit"]["plan_ref"] == k["plan_ref"]
            for o in olaylar
        )
    )
    if yinelenen:
        raise PilotHatasi("MC planının sonucu zaten yayımlandı.")
    if k["durum"] not in ("tamamlandi", "hata"):
        raise PilotHatasi("MC senaryo durumu geçersiz.")
    if k["durum"] == "tamamlandi":
        _mc_olculer(k["olculer"])
        if k["asama"] is not None or k["neden"] is not None:
            raise PilotHatasi("MC tamamlanmış sonuç hata taşıyamaz.")
        for o in k["sembol_olculeri"].values():
            _mc_olculer(o)
        _mc_sonuc_kaniti(olaylar, d, b, p, k, onek=onek)
    elif (
        k["olculer"]
        or k["sembol_olculeri"]
        or k["yeniden_sinama"]
        or k["sonuc_referanslari"]
        or not k["asama"]
        or not k["neden"]
    ):
        raise PilotHatasi("MC hatası aşama ve neden taşımalıdır.")


def _mc_komsular(olaylar, g):
    kaynak = _bul(olaylar, g["kaynak"]["deneme_id"], "deneme", "deneme_id")
    eksenler = kaynak["yontem_ayarlari"]["eksenler"]
    sonuc = []
    secimler = [_bul(olaylar, ref, "ileri_secim") for ref in g["secim_referanslari"]]
    for o in sorted(secimler, key=lambda o: (o["bolum_id"], o["sembol"])):
        if o["kayit"]["durum"] != "secildi":
            continue
        secilen = _bul(olaylar, o["kayit"]["test_deneme_id"], "deneme", "deneme_id")
        p = {a["ad"]: a["deger"] for a in secilen["strateji"]["parametreler"]}
        degerler = []
        for e in eksenler:
            i = e["degerler"].index(p[e["ad"]])
            degerler.append(e["degerler"][max(0, i - 1) : i + 2])
        demetler = []
        for demet in product(*degerler):
            sayisal = {e["ad"]: v for e, v in zip(eksenler, demet, strict=True)}
            try:
                katalog.legacy_coz(
                    secilen["strateji"]["varyant"],
                    secilen["strateji"]["katalog_surumu"],
                    sayisal_ayarlar=sayisal,
                )
            except ValueError:
                continue
            demetler.append(sayisal)
        if not demetler:
            raise PilotHatasi("MC seçimin izinli komşu demeti yok.")
        sonuc.append(dict(secim=o, taban=secilen, demetler=demetler))
    return sonuc


def _mc_stres_cocuklari(olaylar, d, b, g, is_, k):
    from tansu.istatistik import mc_plan

    komsular = _mc_komsular(olaylar, g)
    cekilis = mc_plan(
        "ayar_komsulugu_v1",
        k["anahtar"],
        k["indeks"],
        n=len(komsular),
        tohum=d["yontem_ayarlari"]["tohum"],
        komsu_sayilari=[len(q["demetler"]) for q in komsular],
    )
    if k["cekilis"] != cekilis or len(k["stres_cocuklari"]) != len(komsular):
        raise PilotHatasi("MC stres çekilişi veya tam çocuk listesi uyuşmuyor.")
    for c, q, i in zip(
        k["stres_cocuklari"], komsular, cekilis["demet_indeksleri"], strict=True
    ):
        _mc_alanlar(
            c,
            "bolum sembol secim_ref deneme_id ayar_parmak_izi strateji_ayar_parmak_izi demet",
        )
        secim, taban = q["secim"], q["taban"]
        cocuk = _bul(olaylar, c["deneme_id"], "deneme", "deneme_id")
        if (
            c["bolum"],
            c["sembol"],
            c["secim_ref"],
            c["demet"],
            c["ayar_parmak_izi"],
            c["strateji_ayar_parmak_izi"],
        ) != (
            secim["bolum_id"],
            secim["sembol"],
            secim["kayit_id"],
            q["demetler"][i],
            cocuk["ayar_parmak_izi"],
            cocuk["strateji"]["ayar_parmak_izi"],
        ):
            raise PilotHatasi("MC stres çocuğunun demeti veya seçim bağı uyuşmuyor.")
        y = dict(
            yontem="mc_stres_cocuk_v1",
            tekrar=0,
            bolum_id=c["bolum"],
            sembol=c["sembol"],
            secim_ref=c["secim_ref"],
            hucre_yontemi=taban["yontem_ayarlari"]["hucre_yontemi"],
        )
        if (
            cocuk["ust_deneme_id"] != d["deneme_id"]
            or cocuk["baglar"] != dict(izgara_ust_deneme=d["deneme_id"])
            or cocuk["yontem_ayarlari"] != y
        ):
            raise PilotHatasi("MC stres revizyonu üstüne veya planına bağlı değil.")
        for a in ("donemler", "veri_ayarlari", "risk_ayarlari", "masraf_ayarlari"):
            if kanonik(cocuk[a]) != kanonik(taban[a]):
                raise PilotHatasi(f"MC stres revizyonu ayarı değiştirmiş: {a}")
        _strateji_kaydi(cocuk["strateji"])
        if _ayar_ozeti(_ayarlar(cocuk)) != cocuk["ayar_parmak_izi"]:
            raise PilotHatasi("MC stres revizyonu tam ayar özeti uyuşmuyor.")
        p = {a["ad"]: a["deger"] for a in taban["strateji"]["parametreler"]} | c[
            "demet"
        ]
        if {a["ad"]: a["deger"] for a in cocuk["strateji"]["parametreler"]} != p or (
            cocuk["strateji"]["varyant"],
            cocuk["strateji"]["katalog_surumu"],
        ) != (taban["strateji"]["varyant"], taban["strateji"]["katalog_surumu"]):
            raise PilotHatasi("MC stres giriş dışındaki ayarları değiştirmiş.")


def _mc_sinyal_dogrula(olaylar, d, b, k, *, onek=None):
    from tansu import motor

    p = _mc_ref(olaylar, k["plan_ref"], "mc_plan", d, b, onek=onek)
    c = next(
        (
            c
            for c in p["stres_cocuklari"]
            if (c["secim_ref"], c["deneme_id"], c["bolum"], c["sembol"])
            == (k["secim_ref"], k["deneme_id"], k["bolum"], k["sembol"])
        ),
        None,
    )
    if c is None:
        raise PilotHatasi("MC sinyali planın dondurulmuş stres çocuğuna bağlı değil.")
    cocuk = _bul(olaylar, k["deneme_id"], "deneme", "deneme_id")
    sinyal = k["sinyal"]
    _mc_alanlar(sinyal, "sembol tarih kaynak_sinyal parametreler veri_ref")
    if (sinyal["sembol"], sinyal["tarih"]) != (k["sembol"], k["tarih"]) or sinyal[
        "parametreler"
    ] != motor._duz({a["ad"]: a["deger"] for a in cocuk["strateji"]["parametreler"]}):
        raise PilotHatasi("MC sinyalinin tam parametresi veya tarihi uyuşmuyor.")
    donem = cocuk["donemler"][0]
    if (
        not donem["baslangic"].isoformat() <= k["tarih"] <= donem["bitis"].isoformat()
        or not sinyal["veri_ref"]
        or sinyal["kaynak_sinyal"]["semboller"] != [k["sembol"]]
        or sinyal["kaynak_sinyal"]["tarih"] != k["tarih"]
        or sinyal["kaynak_sinyal"]["baglar"]["ayar_parmak_izi"]
        != cocuk["strateji"]["ayar_parmak_izi"]
        or sinyal["veri_ref"]["manifest_parmak_izi"] != b["manifest_ozeti"]
        or sinyal["veri_ref"].get("pay_kimligi")
        != d["veri_ayarlari"].get("pay_kimligi")
        or sinyal["kaynak_sinyal"]["baglar"]["veri_ref_id"]
        != sinyal["veri_ref"]["kayit_id"]
    ):
        raise PilotHatasi("MC sinyali dönem/veri/E2 kaynağıyla uyuşmuyor.")
    if d["veri_ayarlari"].get("ilk_islem") is not None:
        from tansu import veri
        from tansu.tansusinama import (
            _dogal_bekleyis,
            _donem_uyeligi,
            _ilk_islem_kayitlari,
            _isinma_referansi_dogrula,
        )

        try:
            bas = _mc_bul(
                olaylar,
                d["yontem_ayarlari"]["kaynak"]["kosu_id"],
                "baslangic",
                "kosu_id",
                onek=onek,
            )
            kanit = bas["uyelik_kaniti"]
            v, ref = d["veri_ayarlari"], sinyal["veri_ref"]
            kayitlar = _ilk_islem_kayitlari(v, uyelik_kaniti=kanit)
            _, _, uyeler, _, son = _donem_uyeligi(
                cocuk, dict(donem=donem), uyelik_kaniti=kanit
            )
            # Taşıma üyeleri sonuçta kesinleşir; burada bütün verilen bağlar ve üyeler gerekir.
            gereken = set(uyeler) | set(ref["gecmis_kaniti"])
            _isinma_referansi_dogrula(v, ref, donem, gereken, kayitlar)
            gerekli = next(
                a["deger"]
                for a in cocuk["strateji"]["parametreler"]
                if a["ad"] == "isinma"
            )
            bag = _dogal_bekleyis(
                v, ref, k["sembol"], k["tarih"], son, gerekli, kayitlar
            )
            if bag is not None and bag[0] < gerekli:
                raise ValueError(
                    "kaynaklı ilk 500 gözlem dolmadan sinyal kabul edilemez"
                )
        except (veri.VeriHatasi, ValueError, KeyError, TypeError) as hata:
            raise PilotHatasi(
                f"MC ilk işlem/ısınma sinyal bağı geçersiz: {hata}"
            ) from hata
    if any(
        o["kayit_turu"] == "mc_sinyal"
        and o["kosu_id"] == b["kosu_id"]
        and (o["kayit"]["plan_ref"], o["kayit"]["sembol"], o["kayit"]["tarih"])
        == (k["plan_ref"], k["sembol"], k["tarih"])
        for o in olaylar
    ):
        raise PilotHatasi("MC sinyal kabulü yinelenmiş.")


def _mc_durum_kaniti(olaylar, d, b, k, sembol, durum, yurutme_d):
    from tansu import motor
    from tansu.tansusinama import _ileri_yurutme

    motor._durumu_oku(durum, _ileri_yurutme(yurutme_d, b["kosu_id"], sembol))
    pozisyonlar = [i["pozisyon"] for i in durum["islemler"]]
    if durum["pozisyon"]:
        pozisyonlar.append(durum["pozisyon"])
    for poz in pozisyonlar:
        risk = poz["risk_girdisi"]
        sinyal = _bul(olaylar, risk["sinyal_id"], "mc_sinyal")
        motor.hedef_kaniti_dogrula(poz, sinyal["kayit"]["sinyal"])
        _mc_ayni_kosu(sinyal, d, b)
        if (
            sinyal["kayit"]["plan_ref"] != k["plan_ref"]
            or poz["ayar"] != sinyal["kayit"]["sinyal"]["parametreler"]
            or poz["sinyal_tarih"] != sinyal["kayit"]["tarih"]
            or risk["ayar_parmak_izi"] != motor._iz_kodu(poz["ayar"])
        ):
            raise PilotHatasi(
                "MC yeniden sınama işlemi özgün plan veya sinyal ayarını kaybetmiş."
            )


def _mc_bolum_durumunu_ac(kayit, nihai):
    """TASARIM 5.15 S13/#178: özgün E3 durumu, ortak ayrıştırıcıdan önce geri kurulur."""
    _mc_alanlar(kayit, "durum gecmis_onekleri")
    uzunluklar = kayit["gecmis_onekleri"]
    _mc_alanlar(uzunluklar, "iz islemler retler")
    durum = kayit["durum"]
    if not isinstance(durum, dict) or set(durum) != set(nihai) - set(uzunluklar):
        raise PilotHatasi("MC bölüm durumunun tam geçmiş dışı alanları gerekli.")
    sonuc = deepcopy(durum)
    for alan, n in uzunluklar.items():
        if type(n) is not int or not 0 <= n <= len(nihai[alan]):
            raise PilotHatasi("MC bölüm geçmiş öneğinin uzunluğu geçersiz.")
        sonuc[alan] = deepcopy(nihai[alan][:n])
    return sonuc


def _mc_isinma_bolumleri_dogrula(olaylar, d, b, k, *, donemler, kanit, yurutme_d):
    """TASARIM 5.15 S13/#178: yalnız kesin üst/kaynak bağından sonraki saf kanıt."""
    from tansu import veri
    from tansu.tansusinama import (
        _donem_uyeligi,
        _ileri_tasinanlar,
        _isinma_sonucu_dogrula,
    )

    tekrar = k["yeniden_sinama"]
    onceki = {}
    sinyaller = {
        o["kayit_id"]: o["kayit"]
        for o in olaylar
        if o["kayit_turu"] == "mc_sinyal"
        and o["kosu_id"] == b["kosu_id"]
        and o["kayit"]["plan_ref"] == k["plan_ref"]
    }
    try:
        for q, donem in zip(tekrar["bolumler"], donemler, strict=True):
            _mc_alanlar(q, "bolum durum hatalar donem veri_referansi isinma durumlar")
            if (
                q["bolum"] != donem["ad"]
                or kanonik(q["donem"]) != kanonik(donem)
                or q["durum"] != "tamamlandi"
                or q["hatalar"]
            ):
                raise ValueError("bölümün kayıtlı dönem veya başarı bağı uyuşmuyor")
            gunler, _, uyeler, _, son = _donem_uyeligi(
                d, dict(donem=donem), uyelik_kaniti=kanit
            )
            gereken = set(uyeler) | _ileri_tasinanlar(onceki)
            if set(q["durumlar"]) != gereken:
                raise ValueError(
                    "bölümün tarihli üye/taşıma iş kümesi eksik veya fazla"
                )
            adaylar = [
                x["sinyal"]["kaynak_sinyal"]
                for x in sinyaller.values()
                if x["bolum"] == q["bolum"]
            ]
            _isinma_sonucu_dogrula(d, q | dict(adaylar=adaylar), kanit, gereken)
            durumlar = {
                sembol: _mc_bolum_durumunu_ac(kayit, tekrar["durumlar"][sembol])
                for sembol, kayit in q["durumlar"].items()
            }
            for sembol, durum in durumlar.items():
                _mc_durum_kaniti(olaylar, d, b, k, sembol, durum, yurutme_d)
                final = tekrar["durumlar"][sembol]
                if durum["son_tarih"] != gunler[-1]:
                    raise ValueError("bölüm durumu son kayıtlı seansında değil")
                gecmis = onceki.get(sembol, {})
                tarihler = [x["tarih"] for x in gecmis.get("iz", [])] + gunler
                if [x["tarih"] for x in durum["iz"]] != tarihler:
                    raise ValueError(
                        "bölüm geçmişi önceki durum ve tam seans önekini korumuyor"
                    )
                for alan in ("iz", "retler", "islemler"):
                    beklenen = [
                        x
                        for x in final[alan]
                        if (
                            x["pozisyon"]["cikis_tarih"]
                            if alan == "islemler"
                            else x["tarih"]
                        )
                        <= son
                    ]
                    if durum[alan] != beklenen:
                        raise ValueError(
                            "ara bölüm geçmişi nihai durumun özgün öneki değil"
                        )
                pozisyonlar = [x["pozisyon"] for x in final["islemler"]]
                if final["pozisyon"] is not None:
                    pozisyonlar.append(final["pozisyon"])
                aktif = [
                    x
                    for x in pozisyonlar
                    if x["sinyal_tarih"] <= son
                    and (x["cikis_tarih"] is None or x["cikis_tarih"] > son)
                ]
                # Sonraki bölümde giriş yapmadan düşen bekleyen sinyal, işlem listesinde yoktur.
                dusenler = {
                    x["sinyal_id"]
                    for x in final["retler"]
                    if x["tur"] == "dusen_sinyal"
                    and x["tarih"] > son
                    and x["sinyal_id"] in sinyaller
                    and sinyaller[x["sinyal_id"]]["sembol"] == sembol
                    and sinyaller[x["sinyal_id"]]["tarih"] <= son
                }
                poz = durum["pozisyon"]
                beklenen = len(aktif) + len(dusenler)
                if beklenen > 1 or (poz is None) != (beklenen == 0):
                    raise ValueError(
                        "ara bölüm açık/bekleyen taşıma durumunu kaybetmiş"
                    )
                risk = {}
                bekliyor = False
                if aktif:
                    risk = dict(aktif[0]["risk_girdisi"])
                    giris = aktif[0]["giris_tarih"]
                    bekliyor = giris is None or giris > son
                    if bekliyor:
                        # E3 bu iki alanı ancak giriş dolumunda ekler.
                        risk.pop("giris_fiyat", None)
                        risk.pop("ilk_stop", None)
                if poz is not None and (
                    (
                        aktif
                        and (
                            any(poz[a] != aktif[0][a] for a in ("ayar", "sinyal_tarih"))
                            or poz["risk_girdisi"] != risk
                            or (poz["durum"] == "bekliyor") != bekliyor
                            or (not bekliyor and poz["giris_tarih"] != giris)
                        )
                    )
                    or (
                        dusenler
                        and (
                            poz["durum"] != "bekliyor"
                            or poz["risk_girdisi"]["sinyal_id"] not in dusenler
                        )
                    )
                ):
                    raise ValueError(
                        "ara bölüm özgün giriş sinyalini veya ayarını kaybetmiş"
                    )
                kalan = (durum["sonuc"] or {}).get("kalan_adet", 0)
                if durum["iz"][-1]["kalan_adet"] != kalan:
                    raise ValueError(
                        "ara bölüm pozisyonu ve son gözlem adedi uyuşmuyor"
                    )
            onceki.update(durumlar)
        if kanonik(onceki) != kanonik(tekrar["durumlar"]):
            raise ValueError("son bölüm gözlemleri nihai durumlarla uyuşmuyor")
    except (veri.VeriHatasi, ValueError, KeyError, TypeError, IndexError) as hata:
        raise PilotHatasi(f"MC bölüm/ısınma kanıtı geçersiz: {hata}") from hata


def _mc_sonuc_kaniti(olaylar, d, b, p, k, *, onek=None):
    from tansu.istatistik import mc_senaryo_olculeri

    g = _mc_ref(olaylar, p["girdi_ref"], "mc_girdi", d, b, onek=onek)
    is_ = next(i for i in g["isler"] if i["anahtar"] == p["anahtar"])
    if is_["deney"] == "ayar_komsulugu_v1":
        kaynak = _mc_bul(
            olaylar, g["kaynak"]["deneme_id"], "deneme", "deneme_id", onek=onek
        )
        yurutme_d = d | dict(yontem_ayarlari=kaynak["yontem_ayarlari"])
        tekrar = k["yeniden_sinama"]
        _mc_alanlar(tekrar, "durumlar bolumler")
        alanlar = "bolum durum hatalar"
        if d["veri_ayarlari"].get("ilk_islem") is not None:
            alanlar += " donem veri_referansi isinma durumlar"
        for bolum in tekrar["bolumler"]:
            if d["veri_ayarlari"].get("ilk_islem") is not None and set(bolum) != set(
                alanlar.split()
            ):
                raise PilotHatasi("MC bölüm/ısınma alanları eksik veya fazla.")
            _mc_alanlar(bolum, alanlar)
            if bolum["hatalar"]:
                raise PilotHatasi("MC yeniden sınama hata taşıyor.")
        beklenen = {
            _bul(olaylar, ref, "ileri_kontrol")["sembol"]
            for ref in g["kontrol_referanslari"]
        }
        if set(tekrar["durumlar"]) != beklenen:
            raise PilotHatasi("MC yeniden sınama gerekli hisseyi eksiltemez.")
        if [q["bolum"] for q in tekrar["bolumler"]] != [
            f"{y}Q{q}" for y in range(2022, 2026) for q in range(1, 5)
        ] or any(q["durum"] != "tamamlandi" for q in tekrar["bolumler"]):
            raise PilotHatasi("MC gerçek yeniden sınama OOS kapsamı eksik.")
        if d["veri_ayarlari"].get("ilk_islem") is not None:
            bas = _mc_bul(
                olaylar, g["kaynak"]["kosu_id"], "baslangic", "kosu_id", onek=onek
            )
            _mc_isinma_bolumleri_dogrula(
                olaylar,
                d,
                b,
                k,
                donemler=kaynak["donemler"],
                kanit=bas["uyelik_kaniti"],
                yurutme_d=yurutme_d,
            )
        for sembol, durum in tekrar["durumlar"].items():
            _mc_durum_kaniti(olaylar, d, b, k, sembol, durum, yurutme_d)
        if k["sonuc_referanslari"] != [
            o["kayit_id"]
            for o in olaylar
            if o["kayit_turu"] == "mc_sinyal"
            and o["kosu_id"] == b["kosu_id"]
            and o["kayit"]["plan_ref"] == k["plan_ref"]
        ]:
            raise PilotHatasi("MC yeniden sınama sinyal başvuruları eksik.")
    elif k["yeniden_sinama"] or k["sonuc_referanslari"]:
        raise PilotHatasi("Saf MC örneği yeniden sınama sonucu taşıyamaz.")
    olculer = mc_senaryo_olculeri(
        g, is_, p["cekilis"], durumlar=k["yeniden_sinama"].get("durumlar")
    )
    if kanonik(olculer) != kanonik(
        dict(olculer=k["olculer"], sembol_olculeri=k["sembol_olculeri"])
    ):
        raise PilotHatasi(
            "MC ölçüleri kayıtlı örnek veya gerçek yeniden sınamayla uyuşmuyor."
        )


def _mc_kontrol_dogrula(olaylar, d, b, k, *, onek=None):
    from tansu.istatistik import mc_kontrol

    g = _mc_ref(olaylar, k["girdi_ref"], "mc_girdi", d, b, onek=onek)
    if k["anahtar"] not in [i["anahtar"] for i in g["isler"]]:
        raise PilotHatasi("MC kontrol işi kayıtlı değil.")
    sonuclar = _mc_is_sonuclari(olaylar, b["kosu_id"], k["anahtar"], onek=onek)
    if k["sonuc_referanslari"] != [o["kayit_id"] for o in sonuclar] or any(
        o["kayit"]["durum"] != "tamamlandi" for o in sonuclar
    ):
        raise PilotHatasi("MC kontrolü tamamlanmış öneğin tümünü gerektirir.")
    kontroller = _mc_rol_kayitlari(
        olaylar, "mc_kontrol", b["kosu_id"], anahtar=k["anahtar"], onek=onek
    )
    onceki = kontroller[-1] if kontroller else None
    if k["onceki_ref"] != (onceki["kayit_id"] if onceki else None):
        raise PilotHatasi("MC önceki kontrol bağı uyuşmuyor.")
    noktalar = d["yontem_ayarlari"]["kontrol_noktalari"]
    if len(kontroller) >= len(noktalar) or len(sonuclar) != noktalar[len(kontroller)]:
        raise PilotHatasi("MC kalıcı kontrolü sonraki kayıtlı noktayı gerektirir.")
    tani = mc_kontrol(
        [o["kayit"]["olculer"] for o in sonuclar],
        onceki=onceki["kayit"]["tani"] if onceki else None,
    )
    if kanonik(k["tani"]) != kanonik(tani):
        raise PilotHatasi(
            "MC kontrol sayıları veya sayısal tanısı sonuçlarla uyuşmuyor."
        )


def _mc_is_sonuclari(olaylar, kosu_id, anahtar, *, onek=None):
    if (
        onek is not None
        and isinstance(kosu_id, str)
        and (kosu_id, anahtar) not in onek["sirali_sonuc_isleri"]
    ):
        return onek["isler"].get(("mc_senaryo", kosu_id, anahtar), [])
    planlar = {
        o["kayit_id"]: o["kayit"]
        for o in olaylar
        if o["kayit_turu"] == "mc_plan"
        and o["kosu_id"] == kosu_id
        and o["kayit"]["anahtar"] == anahtar
    }
    return sorted(
        [
            o
            for o in olaylar
            if o["kayit_turu"] == "mc_senaryo" and o["kayit"]["plan_ref"] in planlar
        ],
        key=lambda o: planlar[o["kayit"]["plan_ref"]]["indeks"],
    )


def _mc_ozet_dogrula_kaydi(olaylar, d, b, k, *, onek=None):
    g = _mc_ref(olaylar, k["girdi_ref"], "mc_girdi", d, b, onek=onek)
    if [i["anahtar"] for i in k["isler"]] != b["is_listesi"]:
        raise PilotHatasi("MC özeti her gerekli işi bir kez içermelidir.")
    for i, is_ in zip(k["isler"], g["isler"], strict=True):
        _mc_alanlar(
            i,
            "anahtar durum neden istenen denenen tamamlanan hatali baslamayan durma_nedeniyle_istenmedi basarisiz_indeks sonuc_referanslari kontrol_referanslari",
        )
        sonuc = _mc_is_sonuclari(olaylar, b["kosu_id"], i["anahtar"], onek=onek)
        planlar = _mc_rol_kayitlari(
            olaylar, "mc_plan", b["kosu_id"], anahtar=i["anahtar"], onek=onek
        )
        kontrol = _mc_rol_kayitlari(
            olaylar, "mc_kontrol", b["kosu_id"], anahtar=i["anahtar"], onek=onek
        )
        n, h, a = (
            sum(o["kayit"]["durum"] == "tamamlandi" for o in sonuc),
            sum(o["kayit"]["durum"] == "hata" for o in sonuc),
            len(sonuc),
        )
        durma = bool(
            kontrol
            and kontrol[-1]["kayit"]["tani"]["durum"] == "sayisal_kararlilik_gozlendi"
        )
        butce = d["yontem_ayarlari"]["tekrar"]
        basarisiz = n if h else None
        durum = (
            "olculemedi"
            if is_["durum"] == "olculemedi"
            else "eksik"
            if h or n != a or (n < butce and not durma)
            else "on_gosterim"
            if butce == 1000
            else "sayisal_kararlilik_gozlendi"
            if durma
            else "sinirda_kararsiz"
        )
        beklenen = dict(
            anahtar=i["anahtar"],
            durum=durum,
            neden=is_["neden"]
            if durum == "olculemedi"
            else sonuc[-1]["kayit"]["neden"]
            if h
            else "tamamlanmamis_butce"
            if durum == "eksik"
            else None,
            istenen=butce,
            denenen=a,
            tamamlanan=n,
            hatali=h,
            baslamayan=0 if durma else butce - a,
            durma_nedeniyle_istenmedi=butce - n if durma else 0,
            basarisiz_indeks=basarisiz,
            sonuc_referanslari=[o["kayit_id"] for o in sonuc],
            kontrol_referanslari=[o["kayit_id"] for o in kontrol],
        )
        if (
            i != beklenen
            or h > 1
            or (len(planlar) > len(sonuc) and not h)
            or (n == butce and not kontrol)
            or (is_["durum"] == "olculemedi" and a)
        ):
            raise PilotHatasi(
                "MC özet durumu veya bütçe sayımı gerçek kayıtlarla uyuşmuyor."
            )


def _mc_isareti(o):
    return (
        str(o.get("kayit_turu", "")).startswith("mc_")
        or str(o.get("surum", "")).startswith("mc_")
        or str(o.get("yontem_surumu", "")).startswith("kayitli_monte_carlo")
    )


def _mc_kayit_dogrula(olaylar, o, *, onek=None):
    """S13: okuyucu/yazıcının doğruladığı kesin önekte olay bağını denetle."""
    if onek is None:
        onek = _mc_onek(olaylar)
    tur = o["kayit_turu"]
    alanlar = "kayit_id sema_surumu olusturma_zamani kayit_turu deneme_id kosu_id ayar_parmak_izi kaynaklar surum yontem_surumu icerik_ozeti kayit"
    _mc_alanlar(o, alanlar + (" parti_ref" if "parti_ref" in o else ""))
    if _mc_kimlik_var(olaylar, o["kayit_id"], onek):
        raise PilotHatasi("MC kayıt kimliği yinelenmiş.")
    if "parti_ref" in o:
        parti = _mc_bul(olaylar, o["parti_ref"], "mc_parti", onek=onek)
        kayitlar = parti["kayit"]["kayitlar"]
        if (parti["kosu_id"], parti["deneme_id"]) != (
            o["kosu_id"],
            o["deneme_id"],
        ) or not (
            any(k is o for k in kayitlar)
            or any(kanonik(k) == kanonik(o) for k in kayitlar)
        ):
            raise PilotHatasi("MC iç kaydı başka partiye bağlı.")
    if (
        tur not in _MC_ALANLAR
        or o["sema_surumu"] != SURUM
        or o["surum"] != f"{tur}_v1"
        or o["yontem_surumu"] != "kayitli_monte_carlo_v1"
        or o["icerik_ozeti"] != _mc_ozet(o["kayit"])
    ):
        raise PilotHatasi("MC sabit türü, yöntemi veya içerik özeti uyuşmuyor.")
    k = o["kayit"]
    _mc_alanlar(k, _MC_ALANLAR[tur])
    d = _mc_bul(olaylar, o["deneme_id"], "deneme", "deneme_id", onek=onek)
    b = _mc_bul(olaylar, o["kosu_id"], "baslangic", "kosu_id", onek=onek)
    _mc_yontemi(d["yontem_ayarlari"])
    _mc_ayni_kosu(o, d, b)
    if (
        b["tohum"] != d["yontem_ayarlari"]["tohum"]
        or b["ureteci_surumu"] != d["yontem_ayarlari"]["uretec"]
        or b["manifest_ozeti"] != d["veri_ayarlari"]["manifest_ozeti"]
        or b["anlik_goruntu"] != d["veri_ayarlari"]["veri_referanslari"][0]
    ):
        raise PilotHatasi("MC başlangıcının üreteç veya veri bağı uyuşmuyor.")
    if o["kaynaklar"] != d["kaynaklar"] or _mc_rol_kayitlari(
        olaylar, "bitis", b["kosu_id"], onek=onek
    ):
        raise PilotHatasi("MC kaynak veya açık koşu bağı uyuşmuyor.")
    if tur in ("mc_girdi", "mc_ozet") and _mc_rol_kayitlari(
        olaylar, tur, b["kosu_id"], onek=onek
    ):
        raise PilotHatasi("MC girdi veya özet zaten yayımlandı.")
    {
        "mc_girdi": _mc_girdi_dogrula,
        "mc_plan": _mc_plan_dogrula,
        "mc_sinyal": _mc_sinyal_dogrula,
        "mc_senaryo": _mc_senaryo_dogrula,
        "mc_kontrol": _mc_kontrol_dogrula,
        "mc_ozet": _mc_ozet_dogrula_kaydi,
        "mc_parti": _mc_parti_dogrula,
    }[tur](olaylar, d, b, k, onek=onek)


def _mc_parti_dogrula(olaylar, d, b, k, *, onek=None):
    if not isinstance(k["kayitlar"], list) or not 1 <= len(k["kayitlar"]) <= 32:
        raise PilotHatasi("MC kalıcı partisi 1–32 iç kayıt gerektirir.")
    if len({o["kayit_turu"] for o in k["kayitlar"]}) != 1 or k["kayitlar"][0][
        "kayit_turu"
    ] not in ("mc_plan", "mc_senaryo", "mc_sinyal", "deneme"):
        raise PilotHatasi("MC partisi yalnız bir dar kayıt rolü içerebilir.")
    tur = k["kayitlar"][0]["kayit_turu"]
    if tur == "mc_plan":
        planlar = [o["kayit"] for o in k["kayitlar"]]
        ilk = planlar[0]["indeks"]
        sinir = next(
            (n for n in d["yontem_ayarlari"]["kontrol_noktalari"] if n > ilk), None
        )
        if sinir is None or any(
            p["anahtar"] != planlar[0]["anahtar"]
            or p["girdi_ref"] != planlar[0]["girdi_ref"]
            or p["indeks"] >= sinir
            for p in planlar
        ):
            raise PilotHatasi("MC plan partisi deney veya kontrol sınırını aşamaz.")
    if tur == "mc_sinyal" and len({o["kayit"]["plan_ref"] for o in k["kayitlar"]}) != 1:
        raise PilotHatasi("MC sinyal partisi tek plana bağlı olmalıdır.")


def _mc_cocuk_dogrula(olaylar, o, parti):
    _mc_alanlar(
        o,
        "kayit_id sema_surumu olusturma_zamani kayit_turu deneme_id kosu_id kimlik_bicimi_surumu olusturan neden strateji donemler veri_ayarlari yontem_ayarlari risk_ayarlari masraf_ayarlari ust_deneme_id eski_referans baglar kaynaklar bos_nedenleri ayar_parmak_izi parti_ref",
    )
    if (
        o["parti_ref"] != parti["kayit_id"]
        or o["sema_surumu"] != SURUM
        or o["kimlik_bicimi_surumu"] != SURUM
        or o["kosu_id"] != parti["kosu_id"]
        or o["ust_deneme_id"] != parti["deneme_id"]
        or o["baglar"] != dict(izgara_ust_deneme=parti["deneme_id"])
        or any(
            e.get("deneme_id") == o["deneme_id"] and e["kayit_turu"] == "deneme"
            for e in olaylar
        )
    ):
        raise PilotHatasi(
            "MC stres revizyonu parti/üst bağını veya tekilliğini kaybetmiş."
        )
    g = next(
        e["kayit"]
        for e in olaylar
        if e["kayit_turu"] == "mc_girdi" and e["kosu_id"] == parti["kosu_id"]
    )
    y = o["yontem_ayarlari"]
    _mc_alanlar(y, "yontem tekrar bolum_id sembol secim_ref hucre_yontemi")
    q = next(
        (
            q
            for q in _mc_komsular(olaylar, g)
            if q["secim"]["kayit_id"] == y["secim_ref"]
        ),
        None,
    )
    if q is None or y != dict(
        yontem="mc_stres_cocuk_v1",
        tekrar=0,
        bolum_id=q["secim"]["bolum_id"],
        sembol=q["secim"]["sembol"],
        secim_ref=q["secim"]["kayit_id"],
        hucre_yontemi=q["taban"]["yontem_ayarlari"]["hucre_yontemi"],
    ):
        raise PilotHatasi("MC stres revizyonu donmuş WF seçimine bağlı değil.")
    _strateji_kaydi(o["strateji"])
    if _ayar_ozeti(_ayarlar(o)) != o["ayar_parmak_izi"]:
        raise PilotHatasi("MC stres revizyonunun tam ayar özeti geçersiz.")
    p = {a["ad"]: a["deger"] for a in o["strateji"]["parametreler"]}
    eski = {a["ad"]: a["deger"] for a in q["taban"]["strateji"]["parametreler"]}
    if not any(p == eski | v for v in q["demetler"]):
        raise PilotHatasi("MC stres revizyonu izinli giriş komşuluğu dışında.")
    if (o["strateji"]["varyant"], o["strateji"]["katalog_surumu"]) != (
        q["taban"]["strateji"]["varyant"],
        q["taban"]["strateji"]["katalog_surumu"],
    ):
        raise PilotHatasi("MC stres revizyonu başka stratejiye dönüştürülemez.")
    for a in (
        "donemler",
        "veri_ayarlari",
        "risk_ayarlari",
        "masraf_ayarlari",
        "eski_referans",
    ):
        if kanonik(o[a]) != kanonik(q["taban"][a]):
            raise PilotHatasi(f"MC stres revizyonunda değişmez ayar değişmiş: {a}")


def _mc_partiyi_ac(olaylar, parti, *, onek=None):
    if onek is None:
        onek = _mc_onek(olaylar)
    _mc_kayit_dogrula(olaylar, parti, onek=onek)
    sonuc = [parti]
    _mc_onege_ekle(onek, parti)
    for o in parti["kayit"]["kayitlar"]:
        onceki = olaylar + sonuc
        if o.get("parti_ref") != parti["kayit_id"] or _mc_kimlik_var(
            onceki, o.get("kayit_id"), onek
        ):
            raise PilotHatasi("MC iç kayıt kimliği veya zarf bağı uyuşmuyor.")
        if o["kayit_turu"] == "deneme":
            _mc_cocuk_dogrula(onceki, o, parti)
        else:
            _mc_kayit_dogrula(onceki, o, onek=onek)
        _mc_onege_ekle(onek, o)
        sonuc.append(o)
    return sonuc


def _mc_bitis_dogrula(
    olaylar,
    kosu_id,
    durum,
    tamamlanan,
    basarisiz,
    referanslar,
    *,
    yontemler,
    olculer,
    ozetler,
    onek=None,
):
    """TASARIM 5.15 S13: bitiş iddiası güncel doğrulanmış öneğe bağlıdır."""
    if onek is None:
        onek = _mc_onek(olaylar)
    b = _mc_bul(olaylar, kosu_id, "baslangic", "kosu_id", onek=onek)
    d = _mc_bul(olaylar, b["deneme_id"], "deneme", "deneme_id", onek=onek)
    bildirilen = tamamlanan + basarisiz
    if (
        durum not in ("tamamlandi", "hata", "iptal")
        or len(set(bildirilen)) != len(bildirilen)
        or set(bildirilen) != set(b["is_listesi"])
        or any(o["kayit_turu"] == "bitis" and o["kosu_id"] == kosu_id for o in olaylar)
    ):
        raise PilotHatasi(
            "MC bitişinde durum, tekillik veya tam iş muhasebesi geçersiz."
        )
    ozet_kayitlari = _mc_rol_kayitlari(olaylar, "mc_ozet", kosu_id, onek=onek)
    if not ozet_kayitlari:
        if any(
            i["deneme_yayin_belirsiz"] for i in _mc_kurtarma(olaylar, kosu_id)["isler"]
        ):
            raise PilotHatasi(
                "MC belirsiz girişim/yayın aralığı varken özetsiz bitiş yapılamaz."
            )
        if durum == "tamamlandi" or tamamlanan or referanslar:
            raise PilotHatasi("MC özeti olmadan iş tamamlanamaz.")
    else:
        o = ozet_kayitlari[-1]
        _mc_ozet_dogrula_kaydi(olaylar, d, b, o["kayit"], onek=onek)
        biten = [
            i["anahtar"]
            for i in o["kayit"]["isler"]
            if i["durum"]
            in ("sayisal_kararlilik_gozlendi", "sinirda_kararsiz", "on_gosterim")
        ]
        if (
            tamamlanan != biten
            or referanslar != [o["kayit_id"]]
            or (durum == "tamamlandi") != (len(biten) == len(o["kayit"]["isler"]))
        ):
            raise PilotHatasi(
                "MC bitişi gerekli anahtarların gerçek durumuyla uyuşmuyor."
            )
    yontem = d["yontem_ayarlari"]["yontem"]
    calisma = d["yontem_ayarlari"]["calisma_turu"]
    izinli_yontemler = [[yontem, calisma]]
    if durum != "tamamlandi":
        izinli_yontemler.extend([[], [yontem]])
    tam_alanlar = {"calisma_turu", "yontem_tamamlandi"}
    alanlar = set(ozetler) if isinstance(ozetler, dict) else None
    izinli_alanlar = [tam_alanlar]
    if durum != "tamamlandi":
        izinli_alanlar.extend([set(), {"hata"}, tam_alanlar | {"hata"}])
    if (
        not isinstance(yontemler, list)
        or yontemler not in izinli_yontemler
        or olculer != {}
        or alanlar not in izinli_alanlar
    ):
        raise PilotHatasi("MC bitiş yöntemi, ölçüleri veya üstveri alanları geçersiz.")
    if "hata" in ozetler and not isinstance(ozetler["hata"], str):
        raise PilotHatasi("MC bitiş hata bilgisi metin olmalıdır.")
    if tam_alanlar <= alanlar and (
        ozetler["calisma_turu"] != calisma
        or type(ozetler["yontem_tamamlandi"]) is not bool
        or ozetler["yontem_tamamlandi"]
        != (calisma == "nihai" and durum == "tamamlandi")
    ):
        raise PilotHatasi(
            "MC bitiş üstverisi gerçek çalışma türü ve tamamlanmayla uyuşmuyor."
        )


def _mc_kurtarma(olaylar, kosu_id):
    b = _bul(olaylar, kosu_id, "baslangic", "kosu_id")
    d = _bul(olaylar, b["deneme_id"], "deneme", "deneme_id")
    isler = []
    for anahtar in b["is_listesi"]:
        planlar = [
            o
            for o in olaylar
            if o["kayit_turu"] == "mc_plan"
            and o["kosu_id"] == kosu_id
            and o["kayit"]["anahtar"] == anahtar
        ]
        sonuc = _mc_is_sonuclari(olaylar, kosu_id, anahtar)
        hata = any(o["kayit"]["durum"] == "hata" for o in sonuc)
        aralik = (
            [len(sonuc), len(planlar) - 1]
            if len(planlar) > len(sonuc) and not hata
            else None
        )
        isler.append(
            dict(
                anahtar=anahtar,
                denenen=None if aralik else len(sonuc),
                kesin_tamamlanan=sum(
                    o["kayit"]["durum"] == "tamamlandi" for o in sonuc
                ),
                deneme_yayin_belirsiz=aralik,
                baslamayan_kanitli=d["yontem_ayarlari"]["tekrar"]
                - (len(sonuc) if hata else len(planlar)),
            )
        )
    return dict(kosu_id=kosu_id, isler=isler)


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


def _donem_hedef_kaniti_dogrula(icerik, deneme):
    """TASARIM 5.15: isteğe bağlı yeni kanıt özgün dönem adayına bağlıdır."""
    from tansu import motor

    try:
        for durum in icerik.get("durumlar", {}).values():
            # TASARIM 5.15: eski dönem özeti tam E3 durumu değildir.
            if isinstance(durum, dict) and not any(
                a in durum for a in ("surum", "pozisyon", "islemler")
            ):
                continue
            pozisyonlar = [
                durum["pozisyon"],
                *(i["pozisyon"] for i in durum["islemler"]),
            ]
            pozisyonlar = [
                p
                for p in pozisyonlar
                if p is not None
                and (
                    "hedef_yok_kaniti" in p["risk_girdisi"]
                    or (p["ayar"]["hedef"] == "tansu" and p["hedef"] is None)
                )
            ]
            if not pozisyonlar:
                continue
            motor._durumu_oku(durum, durum["yurutme"])
            for p in pozisyonlar:
                parametreler = motor._duz(
                    {a["ad"]: a["deger"] for a in deneme["strateji"]["parametreler"]}
                )
                if (
                    kanonik(p["ayar"]) != kanonik(parametreler)
                    or durum["yurutme"]["strateji_ayar_parmak_izi"]
                    != deneme["strateji"]["ayar_parmak_izi"]
                    or icerik["veri_referansi"]["manifest_parmak_izi"]
                    != deneme["veri_ayarlari"]["manifest_ozeti"]
                    or icerik["veri_referansi"]["goruntu_id"]
                    not in deneme["veri_ayarlari"]["veri_referanslari"]
                ):
                    raise ValueError(
                        "hedef yokluğu kayıtlı denemenin ayar veya verisiyle uyuşmuyor"
                    )
                risk = p["risk_girdisi"]
                adaylar = [
                    s for s in icerik["adaylar"] if s["kayit_id"] == risk["sinyal_id"]
                ]
                if (
                    len(adaylar) != 1
                    or adaylar[0]["baglar"]["ayar_parmak_izi"]
                    != durum["yurutme"]["strateji_ayar_parmak_izi"]
                ):
                    raise ValueError("özgün E2 adayı veya ayarı uyuşmuyor")
                motor.hedef_kaniti_dogrula(
                    p,
                    dict(
                        sembol=risk["sembol"],
                        tarih=p["sinyal_tarih"],
                        kaynak_sinyal=adaylar[0],
                        parametreler=parametreler,
                        veri_ref=icerik["veri_referansi"],
                    ),
                )
    except (KeyError, TypeError, ValueError) as hata:
        raise PilotHatasi("Dönem hedef yokluğu kanıtı uyuşmuyor.") from hata


def _donem_ciktisi_dogrula(
    durum, birimler, icerik, islem_ref, uyarilar, cikti_ref, deneme
):
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
    _donem_hedef_kaniti_dogrula(icerik, deneme)


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
    from tansu.tansusinama import _kayitli_hucre_yontemi

    y = ust["yontem_ayarlari"]
    beklenen = dict(
        yontem="kayitli_izgara_v1",
        tekrar=0,
        secim_politikasi="genis_bolge_net_r_v1",
        olcu_politikasi="bagimsiz_olcu_v1",
        eksenler=y.get("eksenler"),
        hucre_yontemi=_kayitli_hucre_yontemi(y.get("hucre_yontemi")),
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
    _arama_olcu_baglari(olaylar, d, sonuc)


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


def _arama_olcu_baglari(olaylar, d, sonuc):
    """TASARIM 5.15 S11: hisse kimliğini gerçek dönem ve işleme bağla."""
    semboller = [s["sembol"] for s in d["semboller"]]
    if len(set(semboller)) != len(semboller) or set(semboller) != set(
        sonuc["icerik"]["durumlar"]
    ):
        raise PilotHatasi("Ölçülerin hisse kümesi gerçek dönemle uyuşmuyor.")
    olculen = []
    for s in d["semboller"]:
        dogal = (
            sonuc["icerik"].get("isinma", {}).get(s["sembol"], {}).get("dogal_bekleyis")
        )
        if s.get("dogal_bekleyis") != dogal or (
            "dogal_bekleyis" in s and dogal is None
        ):
            raise PilotHatasi("Arama doğal ısınma özeti gerçek çocukla uyuşmuyor.")
        o = s["olcu"]
        refs = _arama_olculen_islemler(olaylar, s)
        olculen.extend(refs)
        egri = o.get("egri_tanimi")
        if egri is not None and not set(egri["referanslar"]) <= set(refs):
            raise PilotHatasi("Eğri başka işlem referansına bağlı.")
    if len(set(olculen)) != len(olculen) or set(olculen) != set(
        d["islem_referanslari"]
    ):
        raise PilotHatasi("Ölçülerin işlem referansları dönemle uyuşmuyor.")


def _arama_olculen_islemler(olaylar, sembol):
    olcu = sembol["olcu"]
    if olcu["politika"] != "bagimsiz_olcu_v1":
        raise PilotHatasi("Arama ölçü politikası uyuşmuyor.")
    refs = []
    for i in olcu["islemler"] + olcu["acik_kismi"]:
        islem = _bul(olaylar, i["islem_ref"], "islem")
        risk = islem["olaylar"][0]["pozisyon"]["risk_girdisi"]
        if (risk["islem_id"], risk["sembol"]) != (i["islem_id"], sembol["sembol"]):
            raise PilotHatasi("Ölçünün gerçek işlem veya hisse kimliği uyuşmuyor.")
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
        _arama_secilen_aciklamasi(b)


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
    if any(i not in c["indeksler"] for i in c["uygun_merkezler"]):
        raise PilotHatasi("Bileşenin uygun merkezi kendi üyesi olmalıdır.")


def _arama_secilen_aciklamasi(bolge):
    """TASARIM 5.15 S11: seçilen merkez açıklamasındaki başvuruları doğrula."""
    secilen = bolge["secilen"]
    if secilen is None:
        return
    h = next(h for h in bolge["hucreler"] if h["indeks"] == secilen)
    if (
        h["karli"] is not True
        or h["uygun_merkez"] is not True
        or h["sinir"] is not False
        or h["eksik_komsular"]
    ):
        raise PilotHatasi("Seçilen hücrenin uygun merkez açıklaması çelişkili.")
    _arama_merkez_bileseni(bolge["bolgeler"], secilen)


def _arama_merkez_bileseni(bolgeler, secilen):
    uyeler = [c for c in bolgeler if secilen in c["indeksler"]]
    merkezler = [c for c in bolgeler if secilen in c["uygun_merkezler"]]
    if len(uyeler) != 1 or merkezler != uyeler:
        raise PilotHatasi("Seçilen merkez tek bir uygun bileşene bağlı olmalıdır.")


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


def _ileri_ust(d):
    # TASARIM 5.15 S12: eski sonuç doğrulayıcılarını değiştirmeyen ayrı sınır.
    from tansu.tansusinama import _ileri_istek

    _ileri_istek(d)


def _ileri_devam_surumu(ortam):
    if "ileri_devam_surumu" not in ortam:
        return None
    surum = ortam["ileri_devam_surumu"]
    if surum != "ileri_devam_v1":
        raise PilotHatasi("Bilinmeyen WF devam sürümü.")
    return surum


def _ileri_bolum(d, kimlik):
    b = next((b for b in d["donemler"] if b["ad"] == kimlik), None)
    if b is None:
        raise PilotHatasi("WF bölümü kayıtlı yöntemde yok.")
    return b


def _ileri_tekil(olaylar, kosu_id, tur, **alanlar):
    if any(
        o["kayit_turu"] == tur
        and o.get("kosu_id") == kosu_id
        and all(o.get(k) == v for k, v in alanlar.items())
        for o in olaylar
    ):
        raise PilotHatasi("WF kaydı zaten yayımlandı.")


def _ileri_ayni_kosu(o, m):
    if (o["deneme_id"], o["kosu_id"], o["ayar_parmak_izi"]) != (
        m.deneme_id,
        m.kosu_id,
        m.ayar_ozeti,
    ):
        raise PilotHatasi("WF başvurusu başka koşuya veya ayara bağlı.")


def _ileri_sonucsuz_cocuk_var(olaylar, ust_kosu_id):
    cocuklar = {
        o["deneme_id"]
        for o in olaylar
        if o["kayit_turu"] == "deneme"
        and o.get("baglar", {}).get("ileri_ust_kosu") == ust_kosu_id
    }
    baslayanlar = {
        o["kosu_id"]
        for o in olaylar
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] in cocuklar
    }
    sonuclar = {o["kosu_id"] for o in olaylar if o["kayit_turu"] == "sonuc"}
    return bool(baslayanlar - sonuclar)


def _ileri_cocuk_bagi(olaylar, ust, b, kimlik, rol):
    d = _bul(olaylar, kimlik, "deneme", "deneme_id")
    donem = (
        b["egitim"]
        if rol == "egitim"
        else {k: v for k, v in b.items() if k != "egitim"}
    )
    y = dict(
        yontem=f"ileri_{rol}_v1",
        tekrar=0,
        bolum_id=b["ad"],
        rol=rol,
        hucre_yontemi=ust["yontem_ayarlari"]["hucre_yontemi"],
    )
    baslangiclar = [
        o
        for o in olaylar
        if o["kayit_turu"] == "baslangic"
        and o["deneme_id"] == ust["deneme_id"]
        and o["kosu_id"] == d["baglar"].get("ileri_ust_kosu")
    ]
    yeni = (
        len(baslangiclar) == 1
        and _ileri_devam_surumu(baslangiclar[0]["ortam"]) == "ileri_devam_v1"
    )
    if (
        d["ust_deneme_id"] != ust["deneme_id"]
        or d["baglar"]
        != dict(
            izgara_ust_deneme=ust["deneme_id"],
            **({"ileri_ust_kosu": baslangiclar[0]["kosu_id"]} if yeni else {}),
        )
        or kanonik(d["donemler"]) != kanonik([donem])
        or d["yontem_ayarlari"] != y
    ):
        raise PilotHatasi("WF çocuk rolü, dönemi veya üst bağı uyuşmuyor.")
    for k in ("veri_ayarlari", "risk_ayarlari", "masraf_ayarlari"):
        if kanonik(d[k]) != kanonik(ust[k]):
            raise PilotHatasi(f"WF çocuk ayarı uyuşmuyor: {k}")
    eksenler = {e["ad"]: e["degerler"] for e in ust["yontem_ayarlari"]["eksenler"]}
    eski = {a["ad"]: a["deger"] for a in ust["strateji"]["parametreler"]}
    if any(
        a["deger"] not in eksenler.get(a["ad"], [eski[a["ad"]]])
        for a in d["strateji"]["parametreler"]
    ):
        raise PilotHatasi("WF çocuk ayarı dondurulmuş alan dışında.")
    if (d["strateji"]["varyant"], d["strateji"]["katalog_surumu"]) != (
        ust["strateji"]["varyant"],
        ust["strateji"]["katalog_surumu"],
    ):
        raise PilotHatasi("WF çocuk stratejisi uyuşmuyor.")
    return d


def _ileri_yeni_cocuk_dogrula(olaylar, o):
    """TASARIM 5.15 S12: çocuk bağı seçimden önce de doğrulanır."""
    if o["kayit_turu"] not in ("deneme", "baslangic", "sonuc", "bitis"):
        return
    if o["kayit_turu"] == "deneme":
        d = o
    else:
        d = next(
            (
                x
                for x in olaylar
                if x["kayit_turu"] == "deneme" and x["deneme_id"] == o.get("deneme_id")
            ),
            None,
        )
    if d is None or "ileri_ust_kosu" not in d.get("baglar", {}):
        return
    if d["yontem_ayarlari"].get("yontem") not in (
        "ileri_egitim_v1",
        "ileri_test_v1",
    ):
        raise PilotHatasi("WF çocuk yöntemi geçersiz.")
    ust_kosu = _bul(olaylar, d["baglar"]["ileri_ust_kosu"], "baslangic", "kosu_id")
    if _ileri_devam_surumu(ust_kosu["ortam"]) != "ileri_devam_v1":
        raise PilotHatasi("WF çocuk eski veya başka üst koşuya bağlı.")
    if any(
        x["kayit_turu"] == "bitis" and x.get("kosu_id") == ust_kosu["kosu_id"]
        for x in olaylar
    ):
        raise PilotHatasi("Bitmiş WF koşusuna çocuk olayı eklenemez.")
    ust = _bul(olaylar, ust_kosu["deneme_id"], "deneme", "deneme_id")
    _ileri_ust(ust)
    bolum = _ileri_bolum(ust, d["yontem_ayarlari"]["bolum_id"])
    rol = d["yontem_ayarlari"]["rol"]
    _ileri_cocuk_bagi(
        olaylar + ([o] if o["kayit_turu"] == "deneme" else []),
        ust,
        bolum,
        d["deneme_id"],
        rol,
    )
    if o["kayit_turu"] == "deneme":
        eksenler = ust["yontem_ayarlari"]["eksenler"]
        p = {a["ad"]: a["deger"] for a in d["strateji"]["parametreler"]}
        koordinat = tuple(ex["degerler"].index(p[ex["ad"]]) for ex in eksenler)
        sayisal = {
            a["ad"]: a["deger"]
            for a in ust["strateji"]["parametreler"]
            if a["koken"] == "legacy_izgara"
        }
        sayisal.update({ex["ad"]: p[ex["ad"]] for ex in eksenler})
        strateji = katalog.legacy_coz(
            ust["strateji"]["varyant"],
            ust["strateji"]["katalog_surumu"],
            sayisal_ayarlar=sayisal,
        )
        beklenen = _ayarlar(
            ust
            | dict(
                strateji=asdict(strateji),
                donemler=d["donemler"],
                yontem_ayarlari=d["yontem_ayarlari"],
            )
        )
        if kanonik(_ayarlar(d)) != kanonik(beklenen):
            raise PilotHatasi("WF çocuk tam ayarı izinli koordinatla uyuşmuyor.")
        for eski in olaylar:
            if (
                eski["kayit_turu"] != "deneme"
                or eski.get("baglar", {}).get("ileri_ust_kosu") != ust_kosu["kosu_id"]
            ):
                continue
            ey = eski["yontem_ayarlari"]
            ep = {a["ad"]: a["deger"] for a in eski["strateji"]["parametreler"]}
            if (
                ey["bolum_id"],
                ey["rol"],
                tuple(ex["degerler"].index(ep[ex["ad"]]) for ex in eksenler),
            ) == (bolum["ad"], rol, koordinat):
                raise PilotHatasi("WF çocuk koordinatı yinelenmiş.")
    elif o["kayit_turu"] == "baslangic":
        if any(
            x["kayit_turu"] == "baslangic" and x["deneme_id"] == d["deneme_id"]
            for x in olaylar
        ):
            raise PilotHatasi("WF çocuk başlangıcı yinelenmiş.")
        if (
            o["mod"] != ust_kosu["mod"]
            or o["kod_kimligi"] != ust_kosu["kod_kimligi"]
            or o["ortam"]
            != {k: v for k, v in ust_kosu["ortam"].items() if k != "ileri_devam_surumu"}
            or o["bagimlilik_ozeti"] != ust_kosu["bagimlilik_ozeti"]
            or o["is_listesi"] != [f"donem:{d['donemler'][0]['ad']}"]
        ):
            raise PilotHatasi("WF çocuk başlangıcı üst yürütmeye bağlı değil.")
    elif o["kayit_turu"] == "sonuc":
        from tansu import motor, veri
        from tansu.tansusinama import _donem_islemleri, _donem_yurutme

        bas = _bul(olaylar, o["kosu_id"], "baslangic", "kosu_id")
        if (
            bas["deneme_id"] != d["deneme_id"]
            or o.get("sonuc_turu") != "donem_v1"
            or o["is_id"] != f"donem:{d['donemler'][0]['ad']}"
            or kanonik(o["donem"]) != kanonik(d["donemler"][0])
            or o["durum"] != o["icerik"]["durum"]
        ):
            raise PilotHatasi("WF çocuk sonucu kayıtlı iş ve döneme bağlı değil.")
        _donem_yayini_dogrula(olaylar, o["kosu_id"], o["is_id"], o["donem"])
        _donem_ciktisi_dogrula(
            o["durum"],
            o["birimler"],
            o["icerik"],
            o["islem_referanslari"],
            o["uyarilar"],
            o["cikti_referanslari"],
            d,
        )
        icerik = dict(o["icerik"])
        ozet = icerik.pop("cikti_parmak_izi", None)
        if ozet != sha256(kanonik(icerik)).hexdigest():
            raise PilotHatasi("WF çocuk sonuç içeriği değişmiş.")
        islemler = [
            x
            for x in olaylar
            if x["kayit_turu"] == "islem" and x.get("kosu_id") == o["kosu_id"]
        ]
        if [x["kayit_id"] for x in islemler] != o["islem_referanslari"] or o["icerik"][
            "islem_referanslari"
        ] != o["islem_referanslari"]:
            raise PilotHatasi("WF çocuk işlemleri sonuçta eksik veya sırasız.")
        if len(islemler) != len(list(_donem_islemleri(o["icerik"]))) or any(
            kanonik(kayit["olaylar"][0]) != kanonik(gercek)
            for kayit, (_, gercek) in zip(
                islemler, _donem_islemleri(o["icerik"]), strict=True
            )
        ):
            raise PilotHatasi("WF çocuk işlemleri mühürlü sonuçla uyuşmuyor.")
        v = d["veri_ayarlari"]
        ref = o["icerik"].get("veri_referansi")
        if ref is None:
            if o["icerik"]["durumlar"]:
                raise PilotHatasi("WF çocuk E3 durumu E1 referansı olmadan yazılamaz.")
        elif (
            not isinstance(ref, dict)
            or ref.get("kayit_id")
            != veri._veri_kayit_id(
                v["veri_referanslari"][0],
                v["kalite_surumu"],
                pay_kimligi=v.get("pay_kimligi"),
                ilk_islem=v.get("ilk_islem"),
            )
            or ref.get("goruntu_id") != v["veri_referanslari"][0]
            or ref.get("manifest_parmak_izi") != v["manifest_ozeti"]
            or ref.get("pay_kimligi") != v.get("pay_kimligi")
            or ref.get("ilk_islem") != v.get("ilk_islem")
        ):
            raise PilotHatasi("WF çocuk E1 kimliği kayıtlı seçimle uyuşmuyor.")
        yurutme_d = d | dict(yontem_ayarlari=d["yontem_ayarlari"]["hucre_yontemi"])
        s = d["strateji"]
        strateji = katalog.legacy_coz(
            s["varyant"],
            s["katalog_surumu"],
            sayisal_ayarlar={
                a["ad"]: a["deger"]
                for a in s["parametreler"]
                if a["koken"] == "legacy_izgara"
            },
        )
        if (
            strateji.kayit_id != s["kayit_id"]
            or strateji.ayar_parmak_izi != s["ayar_parmak_izi"]
        ):
            raise PilotHatasi("WF çocuk stratejisi katalogla uyuşmuyor.")
        for sembol, durum in o["icerik"]["durumlar"].items():
            motor._durumu_oku(
                durum,
                _donem_yurutme(
                    yurutme_d, o["kosu_id"], sembol, ref["kayit_id"], strateji
                ),
            )
    else:
        sonuclar = [
            x
            for x in olaylar
            if x["kayit_turu"] == "sonuc" and x.get("kosu_id") == o["kosu_id"]
        ]
        if len(sonuclar) != 1 or any(
            x["kayit_turu"] == "bitis" and x.get("kosu_id") == o["kosu_id"]
            for x in olaylar
        ):
            raise PilotHatasi("WF çocuk bitişi tek sonuç gerektirir.")
        r = sonuclar[0]
        bas = _bul(olaylar, o["kosu_id"], "baslangic", "kosu_id")
        beklenen = dict(
            durum=r["durum"],
            tamamlanan=bas["is_listesi"] if r["durum"] == "tamamlandi" else [],
            basarisiz=[] if r["durum"] == "tamamlandi" else bas["is_listesi"],
            yontemler=["kayitli_ileri_v1", "bagimsiz_islem_v1"],
            olculer={},
            cikti_referanslari=[r["kayit_id"]],
            ozetler=dict(hatalar=r["icerik"]["hatalar"]),
        )
        if kanonik({a: o[a] for a in beklenen}) != kanonik(beklenen):
            raise PilotHatasi("WF çocuk bitişi gerçek sonuçla uyuşmuyor.")


def _ileri_egitim_bagi(olaylar, ust, b, sembol, h):
    d = _ileri_cocuk_bagi(olaylar, ust, b, h["deneme_id"], "egitim")
    p = {a["ad"]: a["deger"] for a in d["strateji"]["parametreler"]}
    eksenler = ust["yontem_ayarlari"]["eksenler"]
    if len(h["indeks"]) != len(eksenler) or any(
        type(i) is not int
        or not 0 <= i < len(e["degerler"])
        or p[e["ad"]] != e["degerler"][i]
        for e, i in zip(eksenler, h["indeks"], strict=True)
    ):
        raise PilotHatasi("WF eğitim koordinatı kayıtlı parametreyle uyuşmuyor.")
    for alan, tur in (
        ("kayit_ref", "deneme"),
        ("baslangic_ref", "baslangic"),
        ("sonuc_ref", "sonuc"),
        ("bitis_ref", "bitis"),
    ):
        o = _bul(olaylar, h[alan], tur)
        if (o["deneme_id"], o["ayar_parmak_izi"]) != (
            d["deneme_id"],
            d["ayar_parmak_izi"],
        ) or (tur != "deneme" and o["kosu_id"] != h["kosu_id"]):
            raise PilotHatasi("WF eğitim makbuzu başka revizyona veya koşuya bağlı.")
    r = _bul(olaylar, h["sonuc_ref"], "sonuc")
    if r.get("sonuc_turu") != "donem_v1" or kanonik(r["donem"]) != kanonik(b["egitim"]):
        raise PilotHatasi("WF eğitim sonucu türü veya kesimi uyuşmuyor.")
    if (h["ayar_parmak_izi"], h["strateji_ayar_parmak_izi"]) != (
        d["ayar_parmak_izi"],
        d["strateji"]["ayar_parmak_izi"],
    ):
        raise PilotHatasi("WF eğitim ayar özetleri uyuşmuyor.")
    dogal = r["icerik"].get("isinma", {}).get(sembol, {}).get("dogal_bekleyis")
    if h.get("dogal_bekleyis") != dogal or ("dogal_bekleyis" in h and dogal is None):
        raise PilotHatasi("WF doğal ısınma özeti gerçek çocukla uyuşmuyor.")
    durum = r["icerik"]["durumlar"].get(sembol, {})
    kapali = durum.get("islemler", [])
    if any(
        not b["egitim"]["baslangic"].isoformat()
        <= i["pozisyon"]["giris_tarih"]
        <= i["pozisyon"]["cikis_tarih"]
        <= b["egitim"]["bitis"].isoformat()
        for i in kapali
    ):
        raise PilotHatasi("WF eğitiminde kesim dışı işlem puanlanamaz.")
    n = len(kapali)
    net = (
        sum(i["sonuc"]["net_r"] for i in kapali)
        if kapali and all(i["sonuc"]["net_r"] is not None for i in kapali)
        else None
    )
    beklenen = "tamamlandi" if n else "islemsiz"
    if r["durum"] != "tamamlandi":
        beklenen = (
            "eksik"
            if r["icerik"]["asama"]
            in ("veri", "uyelik", "isinma", "limit_kaniti", "kurulum", "gosterge")
            else "hesap_hatasi"
        )
    if kanonik([h["durum"], h["kapali_islem_sayisi"], h["toplam_net_r"]]) != kanonik(
        [beklenen, n, net]
    ):
        raise PilotHatasi("WF eğitim özeti gerçek kapanmış sonuçla uyuşmuyor.")
    p = durum.get("pozisyon")
    dislanan = (
        []
        if p is None
        else [
            dict(
                sinyal_id=p["risk_girdisi"]["sinyal_id"],
                durum=p["durum"],
                neden="egitim_kesiminde_kapanmadi",
            )
        ]
    )
    if h["dislanan"] != dislanan:
        raise PilotHatasi("WF açık eğitim sonucu dışlanmamış.")
    if h["uyarilar"] != (["egitim_120_alti"] if n < 120 else []):
        raise PilotHatasi("WF eğitim uyarısı gerçek örneklemle uyuşmuyor.")
    return d


def _ileri_secimi_dogrula(olaylar, ust, m, k):
    from tansu import saglamlik

    if set(k) != {
        "bolum_id",
        "sembol",
        "egitim_donemi",
        "test_donemi",
        "egitim_kesimi",
        "secim_zamani_simule",
        "egitim_cocuklari",
        "bolge",
        "durum",
        "neden",
        "test_deneme_id",
        "test_kayit_ref",
        "strateji_ayar_parmak_izi",
        "deneme_ayar_parmak_izi",
    }:
        raise PilotHatasi("WF seçim içeriğinin alanları geçersiz.")
    b = _ileri_bolum(ust, k["bolum_id"])
    _metin(k["sembol"])
    _ileri_tekil(
        olaylar, m.kosu_id, "ileri_secim", bolum_id=b["ad"], sembol=k["sembol"]
    )
    if (
        kanonik(k["egitim_donemi"]) != kanonik(b["egitim"])
        or kanonik(k["test_donemi"])
        != kanonik({a: v for a, v in b.items() if a != "egitim"})
        or k["egitim_kesimi"]
        != max(
            date.fromisoformat(t)
            for t in ust["veri_ayarlari"]["takvim"]["seanslar"]
            if b["egitim"]["baslangic"].isoformat()
            <= t
            <= b["egitim"]["bitis"].isoformat()
        )
        or k["secim_zamani_simule"] != b["egitim"]["bitis"]
    ):
        raise PilotHatasi("WF seçim kesimi veya dönemi uyuşmuyor.")
    cocuklar = {}
    for h in k["egitim_cocuklari"]:
        if set(h) - (
            {"dogal_bekleyis"}
            if ust["veri_ayarlari"].get("ilk_islem") is not None
            else set()
        ) != {
            "deneme_id",
            "kosu_id",
            "ayar_parmak_izi",
            "strateji_ayar_parmak_izi",
            "kayit_ref",
            "baslangic_ref",
            "sonuc_ref",
            "bitis_ref",
            "indeks",
            "durum",
            "kapali_islem_sayisi",
            "toplam_net_r",
            "dislanan",
            "uyarilar",
        }:
            raise PilotHatasi("WF eğitim kanıtının alanları geçersiz.")
        indeks = tuple(h["indeks"])
        if indeks in cocuklar:
            raise PilotHatasi("WF eğitim koordinatı yinelenmiş.")
        cocuklar[indeks] = _ileri_egitim_bagi(olaylar, ust, b, k["sembol"], h)
    bolge = k["bolge"]
    beklenen = set(
        product(
            *(range(len(e["degerler"])) for e in ust["yontem_ayarlari"]["eksenler"])
        )
    )
    alan = {tuple(h["indeks"]): h for h in bolge["hucreler"]}
    if set(alan) != beklenen or len(alan) != len(bolge["hucreler"]):
        raise PilotHatasi("WF seçim alanı eksik veya yinelenmiş.")
    ozetler = []
    for indeks in sorted(beklenen):
        ayarlar = {
            e["ad"]: e["degerler"][i]
            for e, i in zip(ust["yontem_ayarlari"]["eksenler"], indeks, strict=True)
        }
        tam = _arama_tam_ayari(ust, ayarlar)
        if tam is None:
            if indeks in cocuklar:
                raise PilotHatasi("WF alan dışı hücresi çalıştırılmış.")
            ozetler.append(
                dict(
                    indeks=list(indeks),
                    deneme_id=None,
                    durum="alan_disi",
                    kapali_islem_sayisi=None,
                    toplam_net_r=None,
                )
            )
            continue
        if indeks not in cocuklar:
            raise PilotHatasi("WF izinli eğitim hücresi eksik.")
        if kanonik(_ayarlar(cocuklar[indeks])["strateji"]) != kanonik(tam["strateji"]):
            raise PilotHatasi("WF eğitim stratejisi kayıtlı koordinatla uyuşmuyor.")
        kaynak = next(x for x in k["egitim_cocuklari"] if tuple(x["indeks"]) == indeks)
        ozetler.append(
            dict(
                indeks=list(indeks),
                **{
                    a: kaynak[a]
                    for a in (
                        "deneme_id",
                        "durum",
                        "kapali_islem_sayisi",
                        "toplam_net_r",
                    )
                },
            )
        )
    gercek_bolge = saglamlik.sec(
        dict(eksenler=ust["yontem_ayarlari"]["eksenler"]),
        ozetler,
        politika=ust["yontem_ayarlari"]["secim_politikasi"],
    )
    if kanonik(bolge) != kanonik(gercek_bolge):
        raise PilotHatasi(
            "WF seçim bölgesi gerçek eğitim ve kayıtlı seçiciyle uyuşmuyor."
        )
    secilen = None if bolge["secilen"] is None else tuple(bolge["secilen"])
    if secilen is None:
        eksik = any(
            h["durum"] not in ("alan_disi", "tamamlandi", "islemsiz")
            for h in alan.values()
        )
        if (
            k["durum"] != ("eksik" if eksik else "secim_yok")
            or k["neden"] != ("egitim_eksik" if eksik else bolge["neden"])
            or any(
                k[a] is not None
                for a in (
                    "test_deneme_id",
                    "test_kayit_ref",
                    "strateji_ayar_parmak_izi",
                    "deneme_ayar_parmak_izi",
                )
            )
        ):
            raise PilotHatasi("WF seçimsiz kayıt bir test revizyonu taşıyamaz.")
        return
    if (
        k["durum"] != "secildi"
        or k["neden"] is not None
        or not alan[secilen]["uygun_merkez"]
    ):
        raise PilotHatasi("WF seçimi uygun merkeze bağlı değil.")
    test = _ileri_cocuk_bagi(olaylar, ust, b, k["test_deneme_id"], "test")
    kayit = _bul(olaylar, k["test_kayit_ref"], "deneme")
    if (
        kayit["deneme_id"] != test["deneme_id"]
        or k["deneme_ayar_parmak_izi"] != test["ayar_parmak_izi"]
        or k["strateji_ayar_parmak_izi"] != test["strateji"]["ayar_parmak_izi"]
        or kanonik(_ayarlar(cocuklar[secilen])["strateji"])
        != kanonik(_ayarlar(test)["strateji"])
    ):
        raise PilotHatasi("WF test revizyonu seçilen eğitim ayarıyla uyuşmuyor.")


def _ileri_sinyal_bagi(olaylar, ust, m, ref):
    secim = _bul(olaylar, ref, "ileri_secim")
    _ileri_ayni_kosu(secim, m)
    if secim["kayit"]["durum"] != "secildi":
        raise PilotHatasi("WF sinyali seçilmiş revizyon gerektirir.")
    test = _ileri_cocuk_bagi(
        olaylar,
        ust,
        _ileri_bolum(ust, secim["bolum_id"]),
        secim["kayit"]["test_deneme_id"],
        "test",
    )
    return secim, test


def _ileri_pozisyon_bagi(olaylar, ust, m, p):
    from tansu import motor
    from tansu.tansusinama import _ileri_yurutme

    risk = p["risk_girdisi"]
    sinyal = _bul(olaylar, risk["sinyal_id"], "ileri_sinyal")
    motor.hedef_kaniti_dogrula(p, sinyal["sinyal"])
    _ileri_ayni_kosu(sinyal, m)
    y = _ileri_yurutme(ust, m.kosu_id, sinyal["sembol"])
    if (
        any(risk.get(a) != v for a, v in y.items())
        or p["ayar"] != sinyal["sinyal"]["parametreler"]
        or risk["ayar_parmak_izi"] != motor._iz_kodu(p["ayar"])
        or p["sinyal_tarih"] != sinyal["tarih"]
    ):
        raise PilotHatasi("WF pozisyonunun özgün sinyal veya ayar bağı uyuşmuyor.")
    return sinyal


def _ileri_tur_baglari(olaylar, m, k):
    for alan in ("islem_refleri", "kontrol_refleri"):
        idler = [r["kayit_ref"] for r in k[alan]]
        if len(set(idler)) != len(idler):
            raise PilotHatasi("WF sonuç başvurusu yinelenmiş.")
        for r in k[alan]:
            tur = "ileri_kontrol" if r["rol"] == "acik_kontrol" else "islem"
            o = _bul(olaylar, r["kayit_ref"], tur)
            _ileri_ayni_kosu(o, m)
            if r["sembol"] != o["sembol"] or (
                tur == "ileri_kontrol" and alan != "kontrol_refleri"
            ):
                raise PilotHatasi("WF kontrol rolü veya sembolü uyuşmuyor.")
            if tur == "islem" and (
                alan != "islem_refleri"
                or o.get("islem_turu") != "ileri_islem_v1"
                or r["rol"] != o["rol"]
                or r["islem_id"] != o["islem_id"]
            ):
                raise PilotHatasi("WF işlem rolü veya kimliği uyuşmuyor.")
    tarihler = [(x["tarih"], x["olay_id"]) for x in k["olaylar"]]
    if tarihler != sorted(tarihler) or len({i for _, i in tarihler}) != len(tarihler):
        raise PilotHatasi("WF olayları kronolojik ve tekil olmalıdır.")
    if any(not "2022-01-01" <= t <= "2025-12-31" for t, _ in tarihler):
        raise PilotHatasi("WF olayı OOS ufku dışında.")
    from tansu.tansusinama import _ileri_olaylar

    durumlar = {
        o["sembol"]: o["durum"]
        for o in olaylar
        if o["kayit_turu"] == "ileri_kontrol" and o["kosu_id"] == m.kosu_id
    }
    if kanonik(k["olaylar"]) != kanonik(_ileri_olaylar(durumlar)):
        raise PilotHatasi("WF olayları gerçek E3 kontrol noktalarıyla uyuşmuyor.")


def _ileri_sinyali_dogrula(olaylar, ust, m, baslangic, secim_ref, sinyal):
    from tansu import motor

    secim, test = _ileri_sinyal_bagi(olaylar, ust, m, secim_ref)
    b = _ileri_bolum(ust, secim["bolum_id"])
    p = {a["ad"]: a["deger"] for a in test["strateji"]["parametreler"]}
    if (
        sinyal["sembol"] != secim["sembol"]
        or not b["baslangic"] <= date.fromisoformat(sinyal["tarih"]) <= b["bitis"]
        or sinyal["parametreler"] != motor._duz(p)
        or sinyal["kaynak_sinyal"]["baglar"]["ayar_parmak_izi"]
        != test["strateji"]["ayar_parmak_izi"]
        or sinyal["veri_ref"]["manifest_parmak_izi"] != baslangic["manifest_ozeti"]
        or sinyal["veri_ref"].get("pay_kimligi")
        != ust["veri_ayarlari"].get("pay_kimligi")
    ):
        raise PilotHatasi("WF sinyalinin tarih, parametre veya veri bağı uyuşmuyor.")
    _ileri_tekil(
        olaylar,
        m.kosu_id,
        "ileri_sinyal",
        secim_ref=secim_ref,
        sembol=sinyal["sembol"],
        tarih=sinyal["tarih"],
    )


def _ileri_kontrolu_dogrula(olaylar, ust, m, bolum_id, sembol, durum, onceki_ref):
    from tansu import motor
    from tansu.tansusinama import _ileri_yurutme

    b = _ileri_bolum(ust, bolum_id)
    d = motor._durumu_oku(durum, _ileri_yurutme(ust, m.kosu_id, sembol))
    son = max(
        t
        for t in ust["veri_ayarlari"]["takvim"]["seanslar"]
        if b["baslangic"].isoformat() <= t <= b["bitis"].isoformat()
    )
    if d["son_tarih"] != son:
        raise PilotHatasi("WF kontrolü bölümün son seansında değil.")
    _ileri_tekil(
        olaylar,
        m.kosu_id,
        "ileri_kontrol",
        bolum_id=bolum_id,
        sembol=sembol,
    )
    oncekiler = [
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_kontrol"
        and o["kosu_id"] == m.kosu_id
        and o["sembol"] == sembol
    ]
    if (oncekiler[-1]["kayit_id"] if oncekiler else None) != onceki_ref:
        raise PilotHatasi("WF kontrol zinciri önceki duruma bağlı değil.")
    if oncekiler:
        eski = oncekiler[-1]["durum"]
        for alan in ("islemler", "iz", "retler"):
            if d[alan][: len(eski[alan])] != eski[alan]:
                raise PilotHatasi("WF geçmiş durumu değiştirilmiş.")
    for p in [i["pozisyon"] for i in d["islemler"]] + (
        [d["pozisyon"]] if d["pozisyon"] else []
    ):
        _ileri_pozisyon_bagi(olaylar, ust, m, p)


def _ileri_islemi_dogrula(olaylar, ust, m, islem, ufuk):
    from tansu.tansusinama import _ileri_ufuk

    p = islem["pozisyon"]
    kimlik = p["risk_girdisi"]["islem_id"]
    rol = "tamamlanmis_islem" if islem["sonuc"]["kalan_adet"] == 0 else "acik_ufuk"
    sinyal = _bul(olaylar, p["risk_girdisi"]["sinyal_id"], "ileri_sinyal")
    if kanonik(ufuk) != kanonik(_ileri_ufuk(ust)):
        raise PilotHatasi("WF işlem ufku kayıtlı yöntemle uyuşmuyor.")
    _ileri_pozisyon_bagi(olaylar, ust, m, p)
    _ileri_tekil(olaylar, m.kosu_id, "islem", islem_id=kimlik)
    if (
        not p["giris_tarih"]
        or not "2022-01-01" <= p["giris_tarih"] <= "2025-12-31"
        or (
            rol == "tamamlanmis_islem"
            and (
                p["durum"] != "kapali"
                or not p["cikis_tarih"]
                or p["cikis_tarih"] > "2025-12-31"
            )
        )
    ):
        raise PilotHatasi("WF nihai işlem tarihi veya durumu geçersiz.")
    kontroller = [
        o
        for o in olaylar
        if o["kayit_turu"] == "ileri_kontrol"
        and o["kosu_id"] == m.kosu_id
        and o["sembol"] == sinyal["sembol"]
    ]
    if not kontroller:
        raise PilotHatasi("WF işleminde gerçek E3 kontrolü gerekli.")
    durum = kontroller[-1]["durum"]
    gercek = next(
        (
            i
            for i in durum["islemler"]
            if i["pozisyon"]["risk_girdisi"]["islem_id"] == kimlik
        ),
        None,
    )
    if rol == "acik_ufuk":
        if kontroller[-1]["bolum_id"] != "2025Q4" or durum["pozisyon"] != p:
            raise PilotHatasi("WF açık işlem yalnız son ufukta yayımlanır.")
        gercek = {
            a: durum[a] for a in ("pozisyon", "dolumlar", "sonuc", "durum", "degerleme")
        }
    if kanonik(gercek) != kanonik(islem):
        raise PilotHatasi("WF işlem sonucu gerçek E3 kontrolüyle uyuşmuyor.")


def _ileri_kayitlari(olaylar, m, tur):
    return [
        o for o in olaylar if o["kayit_turu"] == tur and o.get("kosu_id") == m.kosu_id
    ]


def _ileri_islem_refi(o):
    return {a: o[a] for a in ("rol", "islem_id", "sembol")} | dict(
        kayit_ref=o["kayit_id"]
    )


def _ileri_kontrol_refi(o):
    return dict(rol="acik_kontrol", kayit_ref=o["kayit_id"], sembol=o["sembol"])


def _ileri_bolum_kayitlari(olaylar, m):
    return [
        o
        for o in _ileri_kayitlari(olaylar, m, "sonuc")
        if o.get("sonuc_turu") == "ileri_v1" and o["kayit"]["tur"] == "bolum"
    ]


def _ileri_bolum_kontrolleri(olaylar, ust, m, b):
    from tansu.tansusinama import _donem_uyeligi, _ileri_tasinanlar

    kontroller = _ileri_kayitlari(olaylar, m, "ileri_kontrol")
    onceki = {o["sembol"]: o for o in kontroller if o["bolum_id"] < b["ad"]}
    guncel = {o["sembol"]: o for o in kontroller if o["bolum_id"] == b["ad"]}
    sakli = {}
    if (
        ust["veri_ayarlari"].get("pay_kimligi") is not None
        or ust["veri_ayarlari"].get("ilk_islem") is not None
    ):
        baslangic = _bul(olaylar, m.kosu_id, "baslangic", "kosu_id")
        sakli["uyelik_kaniti"] = baslangic["uyelik_kaniti"]
    _, _, uyeler, _, _ = _donem_uyeligi(ust, dict(donem=b), **sakli)
    gereken = set(uyeler) | _ileri_tasinanlar(
        {s: o["durum"] for s, o in onceki.items()}
    )
    if set(guncel) - gereken or any(o["bolum_id"] > b["ad"] for o in kontroller):
        raise PilotHatasi("WF güncel kontrol kümesi tarihli yürütme kapsamı dışında.")
    return guncel, onceki | guncel, gereken


def _ileri_bolum_kaniti(olaylar, ust, m, b):
    """TASARIM 5.15 S12: çeyrek gözlemi yalnız önceki gerçek makbuzlardan gelir."""
    from tansu import istatistik
    from tansu.tansusinama import DONEM_BIRIMLERI, _ileri_olaylar

    onceki = _ileri_bolum_kayitlari(olaylar, m)
    if (
        len(onceki) >= len(ust["donemler"])
        or ust["donemler"][len(onceki)]["ad"] != b["ad"]
    ):
        raise PilotHatasi("WF bölüm sonucu kayıtlı sırada değil.")
    secimler = [
        o["kayit"] | dict(secim_ref=o["kayit_id"])
        for o in _ileri_kayitlari(olaylar, m, "ileri_secim")
        if o["bolum_id"] == b["ad"]
    ]
    _, kontroller, _ = _ileri_bolum_kontrolleri(olaylar, ust, m, b)
    eski = {r["kayit_ref"] for o in onceki for r in o["kayit"]["islem_refleri"]}
    islemler = [
        o
        for o in _ileri_kayitlari(olaylar, m, "islem")
        if o.get("islem_turu") == "ileri_islem_v1" and o["kayit_id"] not in eski
    ]
    son = {
        o["sembol"]: o["durum"] for o in _ileri_kayitlari(olaylar, m, "ileri_kontrol")
    }
    sayimlar = {
        s: istatistik.ileri_kontrol_sayimi(o["durum"], b)
        for s, o in sorted(kontroller.items())
    }
    return dict(
        tur="bolum",
        bolum_id=b["ad"],
        donem=b,
        birimler=DONEM_BIRIMLERI,
        muhasebe_politikasi="tani_referans_v1",
        secimler=secimler,
        kontrol_refleri=[_ileri_kontrol_refi(o) for _, o in sorted(kontroller.items())],
        islem_refleri=[_ileri_islem_refi(o) for o in islemler],
        sayimlar=sayimlar,
        uyarilar=[
            dict(sembol=s, neden="test_30_alti")
            for s, n in sayimlar.items()
            if n["kapali_islem"] < 30
        ],
        olaylar=_ileri_olaylar(son),
    )


def _ileri_birlesik_kaniti(olaylar, ust, m):
    """TASARIM 5.15 S12: değişmez nihai işlemlerin eksiksiz kaynak izdüşümü."""
    from tansu import istatistik
    from tansu.tansusinama import DONEM_BIRIMLERI, _ileri_olaylar, _ileri_ufuk

    bolumler = _ileri_bolum_kayitlari(olaylar, m)
    son = {o["sembol"]: o for o in _ileri_kayitlari(olaylar, m, "ileri_kontrol")}
    islemler = [
        o
        for o in _ileri_kayitlari(olaylar, m, "islem")
        if o.get("islem_turu") == "ileri_islem_v1"
    ]
    kohortlar = {}
    for o in islemler:
        kohortlar.setdefault(o["giris_kohortu"], []).append(_ileri_islem_refi(o))
    ufuk = _ileri_ufuk(ust)
    return dict(
        tur="birlesik",
        bolum_id="birlesik",
        donem=ufuk,
        durum="tamamlandi"
        if len(bolumler) == 16
        and all(o["kayit"]["durum"] == "tamamlandi" for o in bolumler)
        else "hata",
        bolum_refleri=[o["kayit_id"] for o in bolumler],
        islem_refleri=[_ileri_islem_refi(o) for o in islemler],
        kontrol_refleri=[_ileri_kontrol_refi(o) for _, o in sorted(son.items())],
        olaylar=_ileri_olaylar({s: o["durum"] for s, o in son.items()}),
        veri_gorulme_durumu="incelenmis_gecmis",
        birimler=DONEM_BIRIMLERI,
        muhasebe_politikasi="tani_referans_v1",
        giris_kohortlari=dict(sorted(kohortlar.items())),
        **istatistik.ileri_ozeti(
            [o["olaylar"][0] | dict(islem_ref=o["kayit_id"]) for o in islemler],
            semboller=son,
            donem=ufuk,
            bolumler=ust["donemler"],
        ),
    )


def _ileri_bitis_kaniti(olaylar, ust, m):
    """TASARIM 5.15 S12: iş muhasebesi doğrulanmış gerçek çeyreklerden gelir."""
    bolumler = _ileri_bolum_kayitlari(olaylar, m)
    birlesik = [
        o
        for o in _ileri_kayitlari(olaylar, m, "sonuc")
        if o.get("sonuc_turu") == "ileri_v1" and o["kayit"]["tur"] == "birlesik"
    ]
    tamamlanan = [
        o["bolum_id"] for o in bolumler if o["kayit"]["durum"] == "tamamlandi"
    ]
    durum = birlesik[-1]["kayit"]["durum"] if birlesik else "hata"
    if durum == "tamamlandi":
        tamamlanan.append("birlesik")
    return dict(
        durum=durum,
        tamamlanan=tamamlanan,
        basarisiz=[b["ad"] for b in ust["donemler"] if b["ad"] not in tamamlanan]
        + ([] if durum == "tamamlandi" else ["birlesik"]),
        yontemler=["kayitli_ileri_v1"],
        olculer={},
        cikti_referanslari=[birlesik[-1]["kayit_id"]] if birlesik else [],
        ozetler=dict(
            tamamlanan=len(tamamlanan),
            denenen=len(bolumler),
            basarisiz=sum(o["kayit"]["durum"] == "hata" for o in bolumler),
            baslamayan=16 - len(bolumler),
        ),
    )


def _ileri_sonucu_dogrula(olaylar, ust, m, kayit):
    _ileri_tekil(
        olaylar,
        m.kosu_id,
        "sonuc",
        sonuc_turu="ileri_v1",
        bolum_id=kayit["bolum_id"],
    )
    _ileri_tur_baglari(olaylar, m, kayit)
    if kayit["tur"] == "bolum":
        b = _ileri_bolum(ust, kayit["bolum_id"])
        if kanonik(kayit["donem"]) != kanonik(b):
            raise PilotHatasi("WF sonuç bölümü uyuşmuyor.")
        for s in kayit["secimler"]:
            secim = _bul(olaylar, s["secim_ref"], "ileri_secim")
            _ileri_ayni_kosu(secim, m)
            if secim["bolum_id"] != b["ad"]:
                raise PilotHatasi("WF sonuç seçimi başka bölümde.")
        gercek = _ileri_bolum_kaniti(olaylar, ust, m, b)
        if kanonik({a: kayit[a] for a in gercek}) != kanonik(gercek):
            raise PilotHatasi(
                "WF çeyrek içeriği gerçek seçim, kontrol ve sayımlarla uyuşmuyor."
            )
        ek = {"veri_referansi", "uyelik", "kalite", "isinma", "adaylar"}
        if set(kayit) - (set(gercek) | ek | {"durum", "neden", "hatalar"}):
            raise PilotHatasi("WF çeyrek içeriğinde bilinmeyen alan var.")
        if not isinstance(kayit["hatalar"], list) or any(
            not isinstance(h, dict)
            or not isinstance(h.get("neden"), str)
            or not h["neden"]
            for h in kayit["hatalar"]
        ):
            raise PilotHatasi("WF çeyrek hatasının türü geçersiz.")
        for a in ek & kayit.keys():
            if kayit[a] is not None and not isinstance(
                kayit[a], list if a == "adaylar" else dict
            ):
                raise PilotHatasi("WF çeyrek veri kanıtının türü geçersiz.")
        guncel, _, gereken = _ileri_bolum_kontrolleri(olaylar, ust, m, b)
        tam = (
            bool(gercek["secimler"])
            and not kayit["hatalar"]
            and all(s["durum"] != "eksik" for s in gercek["secimler"])
            and gereken <= {s["sembol"] for s in gercek["secimler"]}
            and gereken == set(guncel)
        )
        if kayit["durum"] != ("tamamlandi" if tam else "hata") or (
            tam and kayit["neden"] is not None
        ):
            raise PilotHatasi(
                "WF çeyrek başarı durumu gerçek eğitim ve test kanıtıyla uyuşmuyor."
            )
        if not tam:
            _metin(kayit["neden"])
    elif kayit["tur"] == "birlesik":
        refs = kayit["bolum_refleri"]
        if len(refs) != len(set(refs)):
            raise PilotHatasi("WF bölüm sonucu yinelenmiş.")
        bolumler = []
        for ref in refs:
            o = _bul(olaylar, ref, "sonuc")
            _ileri_ayni_kosu(o, m)
            if o.get("sonuc_turu") != "ileri_v1" or o["kayit"]["tur"] != "bolum":
                raise PilotHatasi("WF birleşik kaydı bölüm sonucu gerektirir.")
            bolumler.append(o["kayit"])
        if [b["bolum_id"] for b in bolumler] != [
            b["ad"] for b in ust["donemler"][: len(bolumler)]
        ]:
            raise PilotHatasi("WF birleşik bölüm sırası geçersiz.")
        if kayit["durum"] == "tamamlandi" and (
            len(bolumler) != 16 or any(b["durum"] != "tamamlandi" for b in bolumler)
        ):
            raise PilotHatasi("WF eksik dönemler tam başarı olamaz.")
        if kayit["veri_gorulme_durumu"] != "incelenmis_gecmis":
            raise PilotHatasi("WF tarihsel veri görülmüşlüğü değiştirilemez.")
        gercek_refs = {
            o["kayit_id"]
            for o in olaylar
            if o["kayit_turu"] == "islem"
            and o.get("islem_turu") == "ileri_islem_v1"
            and o["kosu_id"] == m.kosu_id
        }
        if {r["kayit_ref"] for r in kayit["islem_refleri"]} != gercek_refs:
            raise PilotHatasi("WF birleşik sonucu nihai işlem kayıtlarını eksiltemez.")
        kohort_refs = [r for refs in kayit["giris_kohortlari"].values() for r in refs]
        if (
            len(kohort_refs) != len(kayit["islem_refleri"])
            or {r["kayit_ref"] for r in kohort_refs} != gercek_refs
        ):
            raise PilotHatasi(
                "WF giriş kohortları her nihai sonucu bir kez taşımalıdır."
            )
        nihai = {r["kayit_ref"]: r for r in kayit["islem_refleri"]}
        for kohort, refler in kayit["giris_kohortlari"].items():
            for r in refler:
                o = _bul(olaylar, r["kayit_ref"], "islem")
                if kohort != o["giris_kohortu"] or kanonik(r) != kanonik(
                    nihai[r["kayit_ref"]]
                ):
                    raise PilotHatasi(
                        "WF giriş kohortu gerçek nihai işlemle uyuşmuyor."
                    )
        if kanonik(kayit) != kanonik(_ileri_birlesik_kaniti(olaylar, ust, m)):
            raise PilotHatasi(
                "WF birleşik içerik, ölçü, kohort sayımı veya ufuk gerçek kayıtlarla uyuşmuyor."
            )
    else:
        raise PilotHatasi("WF sonuç türü tanımsız.")


def _ileri_kaydi_mi(olaylar, o):
    if o.get("kayit_turu") == "deneme":
        y = o.get("yontem_ayarlari")
        return isinstance(y, dict) and str(y.get("yontem", "")).startswith(
            "kayitli_ileri_"
        )
    if (
        isinstance(o.get("yontemler"), list)
        and len(o["yontemler"]) == 1
        and any(
            isinstance(y, str) and y.startswith("kayitli_ileri_")
            for y in o["yontemler"]
        )
    ):
        return True
    if any(
        str(o.get(a, "")).startswith("ileri_")
        for a in ("kayit_turu", "islem_turu", "sonuc_turu", "surum")
    ):
        return True
    baslangiclar = (
        [o]
        if o.get("kayit_turu") == "baslangic"
        else [
            b
            for b in olaylar
            if b["kayit_turu"] == "baslangic" and b["kosu_id"] == o.get("kosu_id")
        ]
    )
    for b in baslangiclar:
        if not str(b.get("kod_kimligi", "")).startswith("kayitli_ileri_"):
            continue
        cocuk = next(
            (
                d
                for d in olaylar
                if d["kayit_turu"] == "deneme" and d["deneme_id"] == b.get("deneme_id")
            ),
            None,
        )
        if not (
            cocuk is not None
            and isinstance(cocuk.get("yontem_ayarlari"), dict)
            and cocuk["yontem_ayarlari"].get("yontem") == "ileri_egitim_v1"
            and cocuk["ayar_parmak_izi"] == b.get("ayar_parmak_izi")
            and o.get("deneme_id") == b.get("deneme_id")
            and o.get("ayar_parmak_izi") == b.get("ayar_parmak_izi")
            and b.get("is_listesi") == [f"donem:{d['ad']}" for d in cocuk["donemler"]]
        ):
            return True
    return any(
        d["kayit_turu"] == "deneme"
        and isinstance(d.get("yontem_ayarlari"), dict)
        and d["yontem_ayarlari"].get("yontem") == "kayitli_ileri_v1"
        and any(
            d["deneme_id"] == aday.get("deneme_id")
            or d["ayar_parmak_izi"] == aday.get("ayar_parmak_izi")
            or (
                aday.get("kayit_turu") == "baslangic"
                and aday.get("is_listesi")
                == [b["ad"] for b in d["donemler"]] + ["birlesik"]
            )
            for aday in [o, *baslangiclar]
        )
        for d in olaylar
    )


def _ileri_bitisini_dogrula(olaylar, ust, m, baslangic, o):
    beklenen = _ileri_bitis_kaniti(olaylar, ust, m)
    if not beklenen["cikti_referanslari"] and "hata" in o["ozetler"]:
        _metin(o["ozetler"]["hata"])
        beklenen["ozetler"]["hata"] = o["ozetler"]["hata"]
    if (
        type(o["bitis_zamani"]) is not datetime
        or set(beklenen["tamamlanan"] + beklenen["basarisiz"])
        != set(baslangic["is_listesi"])
        or kanonik({a: o[a] for a in beklenen}) != kanonik(beklenen)
    ):
        raise PilotHatasi(
            "WF bitişi gerçek bölüm sonuçları ve iş muhasebesiyle uyuşmuyor."
        )


def _mc_isinma_kaynagi(olaylar, d):
    """TASARIM 5.15 S13: saf ayar özeti yerine kesin kayıt önekinde eşleştir."""
    from tansu.tansusinama import _isinma_secimi_dogrula

    y, v = d["yontem_ayarlari"], d["veri_ayarlari"]
    _mc_yontemi(y)
    kaynak = next(
        (
            x
            for x in olaylar
            if x.get("kayit_turu") == "deneme"
            and x["deneme_id"] == y["kaynak"]["deneme_id"]
        ),
        None,
    )
    if "ilk_islem" not in v and (
        kaynak is None or "ilk_islem" not in kaynak["veri_ayarlari"]
    ):
        return None
    if kaynak is None or kaynak["yontem_ayarlari"].get("yontem") != "kayitli_ileri_v1":
        raise PilotHatasi("MC ısınma kaynağı önceki kayıtlı WF denemesi olmalıdır.")
    _ileri_ust(kaynak)
    if kanonik(v) != kanonik(kaynak["veri_ayarlari"]) or not _isinma_secimi_dogrula(
        kaynak["veri_ayarlari"], kaynak["yontem_ayarlari"]
    ):
        raise PilotHatasi("MC ısınma kaynağının tam veri ve hücre seçimi uyuşmuyor.")
    return kaynak


def _isinma_olayi_dogrula(olaylar, o):
    """TASARIM 5.15 #178: aynı yeni kaynak sınırı ekleme ve taze okumada uygulanır."""
    from tansu import veri
    from tansu.tansusinama import (
        _isinma_secimi_dogrula,
        _isinma_sonucu_dogrula,
        _ileri_uyelik_kaniti_dogrula,
        _donem_uyeligi,
    )

    try:
        d = (
            o
            if o.get("kayit_turu") == "deneme"
            else next(
                (
                    x
                    for x in olaylar
                    if x.get("kayit_turu") == "deneme"
                    and x.get("deneme_id") == o.get("deneme_id")
                ),
                None,
            )
        )
        if d is None:
            return
        if str(d["yontem_ayarlari"].get("yontem", "")).startswith(
            "kayitli_monte_carlo"
        ):
            if o["kayit_turu"] == "deneme":
                kaynak = _mc_isinma_kaynagi(olaylar, d)
                if (
                    kaynak is not None
                    and _ayar_ozeti(_ayarlar(d)) != d["ayar_parmak_izi"]
                ):
                    raise PilotHatasi("MC ısınma kaydının tam ayar özeti uyuşmuyor.")
            # Diğer MC rolleri, doğrulanmış üst ve kaynak bağını kendi sahibinde denetler.
            return
        if not _isinma_secimi_dogrula(d["veri_ayarlari"], d["yontem_ayarlari"]):
            return
        if _ayar_ozeti(_ayarlar(d)) != d["ayar_parmak_izi"]:
            raise PilotHatasi("İlk işlem kaydının tam ayar özeti uyuşmuyor.")
        if o["kayit_turu"] == "deneme":
            return
        v = d["veri_ayarlari"]
        bas = (
            o
            if o["kayit_turu"] == "baslangic"
            else _bul(olaylar, o["kosu_id"], "baslangic", "kosu_id")
        )
        if (
            bas["deneme_id"] != d["deneme_id"]
            or bas["ayar_parmak_izi"] != d["ayar_parmak_izi"]
            or bas["anlik_goruntu"] != v["veri_referanslari"][0]
            or bas["manifest_ozeti"] != v["manifest_ozeti"]
        ):
            raise PilotHatasi("İlk işlem başlangıcının kayıtlı veri bağı uyuşmuyor.")
        if o["kayit_turu"] == "baslangic":
            _ileri_uyelik_kaniti_dogrula(v, bas.get("uyelik_kaniti"))
        elif o["kayit_turu"] == "sonuc":
            if o.get("sonuc_turu") == "arama_v1":
                _arama_yayini(
                    olaylar,
                    Makbuz(
                        bas["kayit_id"],
                        d["deneme_id"],
                        bas["kosu_id"],
                        d["ayar_parmak_izi"],
                    ),
                    o,
                )
                return
            r = o.get("icerik") if o.get("sonuc_turu") == "donem_v1" else o.get("kayit")
            if r is None or (
                o.get("sonuc_turu") == "ileri_v1" and r.get("tur") != "bolum"
            ):
                return
            kanit = bas["uyelik_kaniti"]
            if o.get("sonuc_turu") == "donem_v1":
                if (
                    kanonik(o["donem"]) != kanonik(r["donem"])
                    or o["durum"] != r["durum"]
                    or not any(kanonik(r["donem"]) == kanonik(x) for x in d["donemler"])
                ):
                    raise PilotHatasi(
                        "İlk işlem dönem sonucu kayıtlı dönemle uyuşmuyor."
                    )
                gereken = set(
                    _donem_uyeligi(d, dict(donem=r["donem"]), uyelik_kaniti=kanit)[2]
                )
            else:
                _, _, gereken = _ileri_bolum_kontrolleri(
                    olaylar,
                    d,
                    Makbuz(
                        bas["kayit_id"],
                        d["deneme_id"],
                        bas["kosu_id"],
                        d["ayar_parmak_izi"],
                    ),
                    r["donem"],
                )
            _isinma_sonucu_dogrula(d, r, kanit, gereken)
    except (
        veri.VeriHatasi,
        ValueError,
        KeyError,
        TypeError,
        IndexError,
        AttributeError,
        StopIteration,
    ) as hata:
        raise PilotHatasi(f"Kaynaklı ısınma kanıtı geçersiz: {hata}") from hata


def _ileri_olayi_dogrula(olaylar, o):
    """S12 yayını ve okuyucu aynı doğrulanmış önceki kayıtları kullanır."""
    try:
        from tansu.tansusinama import _ileri_kohort

        if (
            not {"kayit_id", "sema_surumu", "olusturma_zamani"} <= o.keys()
            or type(o["olusturma_zamani"]) is not datetime
            or o["sema_surumu"] != SURUM
        ):
            raise PilotHatasi("WF olay üst bilgisi eksik veya geçersiz.")
        _metin(o["kayit_id"])
        _metin(o["deneme_id"])
        if o["kayit_turu"] != "deneme":
            _metin(o["kosu_id"])
        if o.get("kayit_id") is not None and any(
            x["kayit_id"] == o["kayit_id"] for x in olaylar
        ):
            raise PilotHatasi("WF olay kimliği yinelenmiş.")
        ust = (
            o
            if o["kayit_turu"] == "deneme"
            else _bul(olaylar, o["deneme_id"], "deneme", "deneme_id")
        )
        _ileri_ust(ust)
        _strateji_kaydi(ust["strateji"])
        if _ayar_ozeti(_ayarlar(ust)) != ust["ayar_parmak_izi"]:
            raise PilotHatasi("WF üst revizyonunun tam ayarı bozuk.")
        if o["kayit_turu"] == "deneme":
            alanlar = {
                "kayit_id",
                "sema_surumu",
                "olusturma_zamani",
                "kayit_turu",
                "deneme_id",
                "kimlik_bicimi_surumu",
                "olusturan",
                "neden",
                "strateji",
                "donemler",
                "veri_ayarlari",
                "yontem_ayarlari",
                "risk_ayarlari",
                "masraf_ayarlari",
                "ust_deneme_id",
                "eski_referans",
                "baglar",
                "kaynaklar",
                "bos_nedenleri",
                "ayar_parmak_izi",
            }
            if (
                set(o) != alanlar
                or o["kimlik_bicimi_surumu"] != SURUM
                or o["kaynaklar"] != o["strateji"]["kaynaklar"]
            ):
                raise PilotHatasi(
                    "WF üst revizyonunun tür, sürüm veya kaynak alanları geçersiz."
                )
            _ileri_tekil(olaylar, None, "deneme", deneme_id=o["deneme_id"])
            if o["ust_deneme_id"] is not None:
                _bul(olaylar, o["ust_deneme_id"], "deneme", "deneme_id")
            return
        if o["kayit_turu"] == "baslangic":
            alanlar = {
                "kayit_id",
                "sema_surumu",
                "olusturma_zamani",
                "kayit_turu",
                "deneme_id",
                "kosu_id",
                "ayar_parmak_izi",
                "mod",
                "anlik_goruntu",
                "manifest_ozeti",
                "uyelik_surumu",
                "kod_kimligi",
                "ortam",
                "bagimlilik_ozeti",
                "tohum",
                "ureteci_surumu",
                "is_listesi",
                "kaynaklar",
                "bos_nedenleri",
            }
            if (
                ust["veri_ayarlari"].get("pay_kimligi") is not None
                or ust["veri_ayarlari"].get("ilk_islem") is not None
            ):
                from tansu.tansusinama import _ileri_uyelik_kaniti_dogrula

                alanlar.add("uyelik_kaniti")
                _ileri_uyelik_kaniti_dogrula(
                    ust["veri_ayarlari"], o.get("uyelik_kaniti")
                )
            if set(o) != alanlar or o["is_listesi"] != [
                b["ad"] for b in ust["donemler"]
            ] + ["birlesik"]:
                raise PilotHatasi("WF başlangıç alanları veya iş listesi geçersiz.")
            if any(
                x["kayit_turu"] == "baslangic" and x["kosu_id"] == o["kosu_id"]
                for x in olaylar
            ):
                raise PilotHatasi("WF başlangıç kimliği yinelenmiş.")
            if _ileri_devam_surumu(o["ortam"]):
                ortam = o["ortam"]
                alanlar = {
                    "git_commit",
                    "kirli",
                    "kod_dosyalari",
                    "lock_sha256",
                    "bagimliliklar",
                    "python_uygulamasi",
                    "python_surumu",
                    "platform",
                    "mimari",
                }
                if (
                    not alanlar <= ortam.keys()
                    or type(ortam["kirli"]) is not bool
                    or not isinstance(ortam["kod_dosyalari"], dict)
                    or "__main__.py" not in ortam["kod_dosyalari"]
                    or not isinstance(ortam["bagimliliklar"], dict)
                    or not ortam["bagimliliklar"]
                    or o["bagimlilik_ozeti"] != ortam["lock_sha256"]
                    or o["kod_kimligi"]
                    != "kayitli_ileri_v1:sha256:"
                    + sha256(kanonik(ortam["kod_dosyalari"])).hexdigest()
                ):
                    raise PilotHatasi(
                        "WF devam başlangıcının kimliği eksik veya bozuk."
                    )
            _kosu_meta_dogrula(
                (
                    o["mod"],
                    o["anlik_goruntu"],
                    o["manifest_ozeti"],
                    o["uyelik_surumu"],
                    o["kod_kimligi"],
                    o["bagimlilik_ozeti"],
                ),
                o["ortam"],
                o["tohum"],
                o["ureteci_surumu"],
            )
            _is_listesi_dogrula(o["is_listesi"])
            if (
                o["ayar_parmak_izi"] != ust["ayar_parmak_izi"]
                or o["manifest_ozeti"] != ust["veri_ayarlari"]["manifest_ozeti"]
                or o["anlik_goruntu"] not in ust["veri_ayarlari"]["veri_referanslari"]
                or o["uyelik_surumu"] != ust["veri_ayarlari"]["uyelik_surumu"]
                or o["kaynaklar"] != ust["kaynaklar"]
            ):
                raise PilotHatasi("WF başlangıcı kayıtlı üst revizyonla uyuşmuyor.")
            return
        baslangic = _bul(olaylar, o["kosu_id"], "baslangic", "kosu_id")
        m = Makbuz(
            baslangic["kayit_id"],
            baslangic["deneme_id"],
            baslangic["kosu_id"],
            baslangic["ayar_parmak_izi"],
        )
        _ileri_ayni_kosu(o, m)
        if (
            m.deneme_id != ust["deneme_id"]
            or m.ayar_ozeti != ust["ayar_parmak_izi"]
            or baslangic["manifest_ozeti"] != ust["veri_ayarlari"]["manifest_ozeti"]
            or baslangic["anlik_goruntu"]
            not in ust["veri_ayarlari"]["veri_referanslari"]
            or any(
                x["kayit_turu"] == "bitis" and x["kosu_id"] == m.kosu_id
                for x in olaylar
            )
        ):
            raise PilotHatasi(
                "WF olayının başlangıç, veri veya açık koşu bağı geçersiz."
            )
        tur = o["kayit_turu"]
        if tur == "ileri_secim":
            k = o["kayit"]
            _ileri_secimi_dogrula(olaylar, ust, m, k)
            alanlar = dict(
                surum="ileri_secim_v1",
                bolum_id=k["bolum_id"],
                sembol=k["sembol"],
                kayit=k,
            )
        elif tur == "ileri_sinyal":
            _ileri_sinyali_dogrula(
                olaylar, ust, m, baslangic, o["secim_ref"], o["sinyal"]
            )
            secim = _bul(olaylar, o["secim_ref"], "ileri_secim")
            sinyal = o["sinyal"]
            alanlar = dict(
                surum="ileri_sinyal_v1",
                secim_ref=o["secim_ref"],
                karar_bolumu=secim["bolum_id"],
                **{
                    a: secim["kayit"][a]
                    for a in (
                        "test_deneme_id",
                        "strateji_ayar_parmak_izi",
                        "deneme_ayar_parmak_izi",
                    )
                },
                sembol=sinyal["sembol"],
                tarih=sinyal["tarih"],
                sinyal=sinyal,
            )
        elif tur == "ileri_kontrol":
            _ileri_kontrolu_dogrula(
                olaylar, ust, m, o["bolum_id"], o["sembol"], o["durum"], o["onceki_ref"]
            )
            alanlar = dict(
                surum="ileri_kontrol_v1",
                **{a: o[a] for a in ("bolum_id", "sembol", "durum", "onceki_ref")},
            )
        elif tur == "islem":
            if o.get("islem_turu") != "ileri_islem_v1" or len(o["olaylar"]) != 1:
                raise PilotHatasi("Bilinmeyen WF nihai işlem türü.")
            islem = o["olaylar"][0]
            _ileri_islemi_dogrula(olaylar, ust, m, islem, o["donem"])
            p = islem["pozisyon"]
            sinyal = _bul(olaylar, p["risk_girdisi"]["sinyal_id"], "ileri_sinyal")
            alanlar = dict(
                islem_turu="ileri_islem_v1",
                islem_id=p["risk_girdisi"]["islem_id"],
                rol="tamamlanmis_islem"
                if islem["sonuc"]["kalan_adet"] == 0
                else "acik_ufuk",
                sinyal_id=sinyal["kayit_id"],
                sembol=sinyal["sembol"],
                karar_bolumu=_bul(olaylar, sinyal["secim_ref"], "ileri_secim")[
                    "bolum_id"
                ],
                giris_kohortu=_ileri_kohort(p["giris_tarih"]),
                donem=o["donem"],
                olaylar=[islem],
                birimler=dict(net_r="R", net_sonuc="TL", kalan_adet="adet"),
                veri_ref_id=baslangic["anlik_goruntu"],
            )
        elif tur == "sonuc":
            if o.get("sonuc_turu") != "ileri_v1" or o["kayit"]["durum"] not in (
                "tamamlandi",
                "hata",
            ):
                raise PilotHatasi("Bilinmeyen WF sonuç türü veya durumu.")
            _ileri_sonucu_dogrula(olaylar, ust, m, o["kayit"])
            alanlar = dict(
                sonuc_turu="ileri_v1",
                bolum_id=o["kayit"]["bolum_id"],
                kayit=o["kayit"],
                veri_ref_id=baslangic["anlik_goruntu"],
            )
        elif tur == "bitis":
            _ileri_bitisini_dogrula(olaylar, ust, m, baslangic, o)
            alanlar = {
                a: o[a]
                for a in (
                    "durum",
                    "tamamlanan",
                    "basarisiz",
                    "yontemler",
                    "olculer",
                    "cikti_referanslari",
                    "ozetler",
                    "bitis_zamani",
                )
            }
        else:
            raise PilotHatasi("Bilinmeyen WF olay türü.")
        beklenen = dict(
            kayit_turu=tur,
            deneme_id=m.deneme_id,
            kosu_id=m.kosu_id,
            ayar_parmak_izi=m.ayar_ozeti,
            kaynaklar=ust["kaynaklar"],
            **alanlar,
        )
        meta = {"kayit_id", "sema_surumu", "olusturma_zamani"}
        if meta & o.keys():
            if not meta <= o.keys() or type(o["olusturma_zamani"]) is not datetime:
                raise PilotHatasi("WF olay üst bilgisi eksik veya geçersiz.")
            _metin(o["kayit_id"])
        if kanonik({k: v for k, v in o.items() if k not in meta}) != kanonik(beklenen):
            raise PilotHatasi(
                "WF olayının tür, rol, sürüm veya sahip alanları uyuşmuyor."
            )
    except (KeyError, TypeError, AttributeError, IndexError, StopIteration) as hata:
        raise PilotHatasi(f"WF olay bağı eksik veya geçersiz: {hata}") from hata


def _grup_tanimi_dogrula(tanim):
    """TASARIM 5.15 Küçük grup hazırlığı: hesap alanı kabul edilmez."""
    alanlar = {
        "grup_id",
        "revizyon",
        "soru",
        "strateji_revizyonlari",
        "seanslar",
        "isinma_baslangici",
        "hisse_kurali",
        "referanslar",
        "gozlem_durumu",
        "durdurma_kurali",
    }
    if not isinstance(tanim, dict) or tanim.keys() - alanlar:
        raise PilotHatasi("Bilinmeyen grup tanımı alanı.")
    for ad in ("grup_id", "revizyon"):
        _metin(tanim.get(ad))
    for ad in ("soru", "gozlem_durumu", "durdurma_kurali"):
        if tanim.get(ad) is not None:
            _metin(tanim[ad])
    if tanim.get("isinma_baslangici") is not None:
        _grup_tarihi(tanim["isinma_baslangici"])
    seanslar = tanim.get("seanslar", [])
    if not isinstance(seanslar, list) or len(seanslar) > 60:
        raise PilotHatasi("Grup en fazla 60 seans içermelidir.")
    for gun in seanslar:
        _grup_tarihi(gun)
    if seanslar != sorted(set(seanslar)):
        raise PilotHatasi("Grup seansları sıralı ve tekil olmalıdır.")
    stratejiler = tanim.get("strateji_revizyonlari", [])
    if not isinstance(stratejiler, list) or len(stratejiler) > 3:
        raise PilotHatasi("Grup en fazla üç strateji revizyonu içermelidir.")
    for strateji in stratejiler:
        if not isinstance(strateji, dict) or strateji.keys() - {
            "revizyon_ref",
            "kaynak",
            "yayim_tarihi",
            "deneme_id",
            "eksik_alanlar",
        }:
            raise PilotHatasi("Strateji hazırlık başvurusu geçersiz.")
        _metin(strateji.get("revizyon_ref"))
        if strateji.get("deneme_id") is not None:
            _metin(strateji["deneme_id"])
        if strateji.get("yayim_tarihi") is not None:
            _grup_tarihi(strateji["yayim_tarihi"])
        eksik = strateji.get("eksik_alanlar", [])
        if not isinstance(eksik, list):
            raise PilotHatasi("Eksik alanlar liste olmalıdır.")
        for alan in eksik:
            _metin(alan)
        _grup_dosya_basvurusu(strateji.get("kaynak"))
    if len({s["revizyon_ref"] for s in stratejiler}) != len(stratejiler):
        raise PilotHatasi("Strateji revizyonu yinelenmiş.")
    kural = tanim.get("hisse_kurali", {})
    if not isinstance(kural, dict) or kural.keys() - {
        "semboller",
        "evren_politikasi",
        "uyelik_surumu",
    }:
        raise PilotHatasi("Hisse kuralı geçersiz.")
    semboller = kural.get("semboller", [])
    if not isinstance(semboller, list):
        raise PilotHatasi("Açık sembol listesi gerekli.")
    for sembol in semboller:
        _metin(sembol)
    if len(set(semboller)) != len(semboller):
        raise PilotHatasi("Sembol yinelenmiş.")
    ref = tanim.get("referanslar", {})
    if not isinstance(ref, dict) or ref.keys() - {
        "anlik_goruntu",
        "manifest_ozeti",
        "uyelik_ozeti",
        "kod_ozeti",
        "takvim",
        "yontem",
        "risk",
        "masraf",
        "pay_kimligi",
    }:
        raise PilotHatasi("Grup başvuruları geçersiz.")
    for ad in ("anlik_goruntu", "manifest_ozeti", "uyelik_ozeti", "kod_ozeti"):
        if ref.get(ad) is not None:
            _metin(ref[ad])
    for ad in ("takvim", "yontem", "risk", "masraf"):
        _grup_dosya_basvurusu(ref.get(ad))
    if "pay_kimligi" in ref:
        # TASARIM 5.15 #167: geçmiş kayıt yalnız seçimin yapısına bağlıdır.
        from tansu.veri import VeriHatasi, pay_kimligi_secimi_dogrula

        try:
            pay_kimligi_secimi_dogrula(ref["pay_kimligi"])
        except VeriHatasi as hata:
            raise PilotHatasi(str(hata)) from hata
        if ref["pay_kimligi"]["goruntu_id"] != ref.get("anlik_goruntu") or ref[
            "pay_kimligi"
        ]["manifest_ozeti"] != ref.get("manifest_ozeti"):
            raise PilotHatasi("Pay kimliği grup veri bağıyla uyuşmuyor.")


def _grup_tarihi(gun):
    try:
        if not isinstance(gun, str) or date.fromisoformat(gun).isoformat() != gun:
            raise ValueError("ISO tarih gerekli.")
    except ValueError as hata:
        raise PilotHatasi("Grup günü ISO tarih metni olmalıdır.") from hata


def _grup_dosya_basvurusu(ref):
    if ref is None:
        return
    if not isinstance(ref, dict) or set(ref) != {"yol", "sha256"}:
        raise PilotHatasi("Dosya başvurusu yol ve sha256 içermelidir.")
    _metin(ref["yol"])
    ozet = ref["sha256"]
    if (
        not isinstance(ozet, str)
        or len(ozet) != 64
        or any(c not in "0123456789abcdef" for c in ozet)
    ):
        raise PilotHatasi("Dosya sha256 özeti geçersiz.")


def _grup_olayi_dogrula(olay):
    """TASARIM 5.15: hazırlık olayı yazılırken ve okunurken aynı sınır geçer."""
    alanlar = {
        "kayit_turu",
        "hazirlik_turu",
        "tanim",
        "tanim_ozeti",
        "engeller",
        "dislamalar",
        "hazirlik_durumu",
        "yurutme_izni",
    }
    meta = {"kayit_id", "sema_surumu", "olusturma_zamani"}
    if not isinstance(olay, dict):
        raise PilotHatasi("Hazırlık olayı nesne olmalıdır.")
    if olay.keys() & meta:
        alanlar |= meta
    if set(olay) != alanlar:
        raise PilotHatasi("Hazırlık olayının alanları geçersiz.")
    if meta <= olay.keys():
        _metin(olay["kayit_id"])
        if type(olay["olusturma_zamani"]) is not datetime:
            raise PilotHatasi("Hazırlık olayının zamanı geçersiz.")
        _kodla(olay["olusturma_zamani"])
    if (
        olay["kayit_turu"] != "grup_hazirligi"
        or olay["hazirlik_turu"] != "kucuk_grup_v1"
        or olay["yurutme_izni"] is not False
    ):
        raise PilotHatasi("Hazırlık türü veya yürütme izni geçersiz.")
    tanim, engeller, dislamalar = olay["tanim"], olay["engeller"], olay["dislamalar"]
    _grup_tanimi_dogrula(tanim)
    if not isinstance(engeller, list) or not isinstance(dislamalar, list):
        raise PilotHatasi("Hazırlık engelleri ve dışlamaları liste olmalıdır.")
    for engel in engeller:
        if not isinstance(engel, dict) or set(engel) != {"alan", "neden"}:
            raise PilotHatasi("Engel alan ve neden içermelidir.")
        _metin(engel["alan"])
        _metin(engel["neden"])
    for dislama in dislamalar:
        if not isinstance(dislama, dict) or set(dislama) != {
            "sembol",
            "tarih",
            "neden",
        }:
            raise PilotHatasi("Dışlama sembol, tarih ve neden içermelidir.")
        _metin(dislama["sembol"])
        _grup_tarihi(dislama["tarih"])
        _metin(dislama["neden"])
    if not engeller and (
        any(
            not tanim.get(a)
            for a in (
                "soru",
                "strateji_revizyonlari",
                "seanslar",
                "isinma_baslangici",
                "hisse_kurali",
                "referanslar",
                "gozlem_durumu",
                "durdurma_kurali",
            )
        )
        or any(
            not tanim.get("referanslar", {}).get(a)
            for a in (
                "anlik_goruntu",
                "manifest_ozeti",
                "uyelik_ozeti",
                "kod_ozeti",
                "takvim",
                "yontem",
                "risk",
                "masraf",
            )
        )
        or not tanim.get("hisse_kurali", {}).get("semboller")
        or any(
            not s.get("deneme_id")
            or not s.get("kaynak")
            or not s.get("yayim_tarihi")
            or s.get("eksik_alanlar")
            for s in tanim.get("strateji_revizyonlari", [])
        )
    ):
        raise PilotHatasi("Hazır hazırlık kaydında zorunlu alan eksik.")
    if olay["hazirlik_durumu"] != ("engelli" if engeller else "hazir"):
        raise PilotHatasi("Hazırlık durumu engellerle uyuşmuyor.")
    if sha256(kanonik(tanim)).hexdigest() != olay["tanim_ozeti"]:
        raise PilotHatasi("Hazırlık tanımı özeti uyuşmuyor.")


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
    def _ileri_yurutme_kilidi(self, deneme_id):
        """TASARIM 5.15 S12: WF işçisi tüm yürütme boyunca OS kilidini tutar."""
        ad = sha256(kanonik(deneme_id)).hexdigest()
        kilit = self.yol.with_name(f"{self.yol.name}.wf-{ad}.lock")
        with kilit.open("a+b") as dosya:
            dosya.seek(0)
            try:
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(dosya.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(dosya.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as hata:
                raise PilotHatasi("WF denemesi başka işçide yürütülüyor.") from hata
            try:
                yield
            finally:
                dosya.seek(0)
                if os.name == "nt":
                    msvcrt.locking(dosya.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(dosya.fileno(), fcntl.LOCK_UN)

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
        mc_onek = _mc_onek()
        for no, satir in enumerate(self.yol.read_bytes().splitlines(keepends=True), 1):
            if not satir.endswith(b"\n") or satir.endswith(_KESIK):
                uyarilar.append(f"Eksik satır: {no}")
                continue
            try:
                olay = _coz(json.loads(satir))
                if olay["sema_surumu"] != SURUM or kanonik(olay) + b"\n" != satir:
                    raise ValueError("Şema veya kodlama uyuşmuyor.")
                if olay.get("sonuc_turu") == "donem_v1":
                    _donem_hedef_kaniti_dogrula(
                        olay["icerik"],
                        next(
                            (
                                o
                                for o in olaylar
                                if o["kayit_turu"] == "deneme"
                                and o["deneme_id"] == olay["deneme_id"]
                            ),
                            None,
                        ),
                    )
                if olay.get("kayit_turu") != "grup_hazirligi":
                    _isinma_olayi_dogrula(olaylar, olay)
                if olay.get("kayit_turu") == "grup_hazirligi":
                    _grup_olayi_dogrula(olay)
                elif _ileri_kaydi_mi(olaylar, olay):
                    _ileri_olayi_dogrula(olaylar, olay)
                _ileri_yeni_cocuk_dogrula(olaylar, olay)
                if olay["kayit_turu"] == "deneme" and str(
                    olay["yontem_ayarlari"].get("yontem", "")
                ).startswith("kayitli_monte_carlo"):
                    _mc_alanlar(
                        olay,
                        "kayit_id sema_surumu olusturma_zamani kayit_turu deneme_id kimlik_bicimi_surumu olusturan neden strateji donemler veri_ayarlari yontem_ayarlari risk_ayarlari masraf_ayarlari ust_deneme_id eski_referans baglar kaynaklar bos_nedenleri ayar_parmak_izi",
                    )
                    if (
                        olay["kimlik_bicimi_surumu"] != SURUM
                        or olay["kaynaklar"] != olay["strateji"]["kaynaklar"]
                    ):
                        raise PilotHatasi(
                            "MC denemesinin kimlik sürümü veya kaynakları uyuşmuyor."
                        )
                    _strateji_kaydi(olay["strateji"])
                    if _ayar_ozeti(_ayarlar(olay)) != olay["ayar_parmak_izi"]:
                        raise PilotHatasi(
                            "MC kayıtlı denemenin tam ayar özeti uyuşmuyor."
                        )
                if _mc_baslangic_mi(olaylar, olay):
                    _mc_baslangic_dogrula(olaylar, olay)
                if olay["kayit_turu"] == "mc_parti":
                    olaylar.extend(_mc_partiyi_ac(olaylar, olay, onek=mc_onek))
                    continue
                if _mc_isareti(olay):
                    _mc_kayit_dogrula(olaylar, olay, onek=mc_onek)
                if olay["kayit_turu"] == "bitis":
                    baslangic = next(
                        (
                            o
                            for o in olaylar
                            if o["kayit_turu"] == "baslangic"
                            and o["kosu_id"] == olay["kosu_id"]
                        ),
                        None,
                    )
                    d = next(
                        (
                            o
                            for o in olaylar
                            if o["kayit_turu"] == "deneme"
                            and o["deneme_id"]
                            == (
                                baslangic["deneme_id"]
                                if baslangic
                                else olay["deneme_id"]
                            )
                        ),
                        None,
                    )
                    if (
                        d
                        and d["yontem_ayarlari"].get("yontem")
                        == "kayitli_monte_carlo_v1"
                    ):
                        _mc_alanlar(
                            olay,
                            "kayit_id sema_surumu olusturma_zamani kayit_turu deneme_id kosu_id ayar_parmak_izi kaynaklar durum tamamlanan basarisiz yontemler olculer cikti_referanslari ozetler bitis_zamani",
                        )
                        b = _bul(olaylar, olay["kosu_id"], "baslangic", "kosu_id")
                        _mc_ayni_kosu(olay, d, b)
                        if olay["kaynaklar"] != d["kaynaklar"]:
                            raise PilotHatasi("MC bitişinin kaynak bağı uyuşmuyor.")
                        _mc_bitis_dogrula(
                            olaylar,
                            olay["kosu_id"],
                            olay["durum"],
                            olay["tamamlanan"],
                            olay["basarisiz"],
                            olay["cikti_referanslari"],
                            yontemler=olay["yontemler"],
                            olculer=olay["olculer"],
                            ozetler=olay["ozetler"],
                            onek=mc_onek,
                        )
            except (ValueError, KeyError, TypeError, IndexError) as hata:
                raise PilotHatasi(f"Bozuk tam satır: {no}") from hata
            _mc_onege_ekle(mc_onek, olay)
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

    def grup_hazirligi_kaydet(self, *, tanim, engeller, dislamalar):
        """TASARIM 5.15 Küçük grup hazırlığı: ayrı olay, yürütme izni yok."""
        _grup_tanimi_dogrula(tanim)
        ozet = sha256(kanonik(tanim)).hexdigest()

        def denetle(olaylar):
            for olay in olaylar:
                if (
                    olay["kayit_turu"] == "grup_hazirligi"
                    and olay["tanim"]["grup_id"] == tanim["grup_id"]
                    and olay["tanim"]["revizyon"] == tanim["revizyon"]
                    and olay["tanim_ozeti"] != ozet
                ):
                    raise PilotHatasi("Değişen grup tanımı yeni revizyon gerektirir.")

        olay = dict(
            kayit_turu="grup_hazirligi",
            hazirlik_turu="kucuk_grup_v1",
            tanim=tanim,
            tanim_ozeti=ozet,
            engeller=engeller,
            dislamalar=dislamalar,
            hazirlik_durumu="engelli" if engeller else "hazir",
            yurutme_izni=False,
        )
        _grup_olayi_dogrula(olay)
        return self._ekle(olay, denetle)

    def grup_hazirligi_oku(self, kayit_id, *, tanim=None):
        """TASARIM 5.15: tarihçe okunur; değişen başvuru güncel kullanılamaz."""
        try:
            olaylar = self.oku()
            olay = _bul(olaylar, kayit_id, "grup_hazirligi")
            if tanim is not None:
                _grup_tanimi_dogrula(tanim)
                if sha256(kanonik(tanim)).hexdigest() != olay["tanim_ozeti"]:
                    raise PilotHatasi(
                        "Hazırlık değişen grup veya başvuru için geçersiz."
                    )
                son = next(
                    o
                    for o in reversed(olaylar)
                    if o["kayit_turu"] == "grup_hazirligi"
                    and o["tanim"]["grup_id"] == tanim["grup_id"]
                )
                if son["kayit_id"] != olay["kayit_id"]:
                    raise PilotHatasi(
                        "Hazırlık değişen grup veya başvuru için geçersiz."
                    )
            return olay
        except OSError as hata:
            raise PilotYazmaHatasi(f"{kayit_id}: {hata}") from hata

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
        uyelik_kaniti=None,
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
        if uyelik_kaniti is not None:
            baslangic["uyelik_kaniti"] = uyelik_kaniti
        wf = deneme["yontem_ayarlari"].get("yontem") == "kayitli_ileri_v1"
        if not wf and "ileri_devam_surumu" in ortam:
            raise PilotHatasi("WF devam sürümü yalnız üst koşuya aittir.")
        surum = _ileri_devam_surumu(ortam) if wf else None
        kilit = self._ileri_yurutme_kilidi(deneme_id) if surum else nullcontext()
        with kilit:
            makbuz = self._ekle(baslangic)
            kosu = _Kosu(self, makbuz, deneme, baslangic)
            try:
                yield kosu
                if kosu._yazma_hatasi:
                    raise PilotYazmaHatasi("Koşu kayıt hatasıyla durdu.")
            except Exception as hata:
                if isinstance(hata, (PilotBelirsizHatasi, PilotDayaniklilikHatasi)):
                    raise
                if "ileri_ust_kosu" in deneme.get("baglar", {}) or (
                    surum
                    and (
                        isinstance(hata, PilotHatasi)
                        or _ileri_sonucsuz_cocuk_var(self.oku(), kosu.makbuz.kosu_id)
                    )
                ):
                    raise
                if not kosu._bitti and not kosu._yazma_hatasi:
                    if deneme["yontem_ayarlari"].get(
                        "yontem"
                    ) == "kayitli_monte_carlo_v1" and any(
                        i["deneme_yayin_belirsiz"]
                        for i in _mc_kurtarma(self.oku(), kosu.makbuz.kosu_id)["isler"]
                    ):
                        raise
                    if deneme["yontem_ayarlari"].get("yontem") == "kayitli_ileri_v1":
                        bitis = _ileri_bitis_kaniti(self.oku(), deneme, makbuz)
                        if not bitis["cikti_referanslari"]:
                            bitis["ozetler"]["hata"] = str(hata)
                        kosu.bitir(**bitis)
                    else:
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

    @contextmanager
    def ileri_devam(self, kosu_id, *, mod, kod_kimligi, ortam, bagimlilik_ozeti):
        """TASARIM 5.15 S12: aynı üst koşuyu kilit altında taze günlükten bağlar."""
        baslangic = _bul(self.oku(), kosu_id, "baslangic", "kosu_id")
        deneme_id = baslangic["deneme_id"]
        with self._ileri_yurutme_kilidi(deneme_id):
            with self._kilit():
                olaylar, uyarilar = self._oku()
                baslangic = _bul(olaylar, kosu_id, "baslangic", "kosu_id")
                deneme = _bul(olaylar, deneme_id, "deneme", "deneme_id")
                _ileri_ust(deneme)
                if _ileri_devam_surumu(baslangic["ortam"]) != "ileri_devam_v1":
                    raise PilotHatasi("Eski WF koşusu devam ettirilemez.")
                if (
                    baslangic["deneme_id"] != deneme_id
                    or baslangic["ayar_parmak_izi"] != deneme["ayar_parmak_izi"]
                    or baslangic["mod"] != mod
                    or baslangic["kod_kimligi"] != kod_kimligi
                    or baslangic["ortam"] != ortam
                    or baslangic["bagimlilik_ozeti"] != bagimlilik_ozeti
                ):
                    raise PilotHatasi("WF devam kimliği veya çalışma ortamı değişmiş.")
                ham = self.yol.read_bytes()
                satirlar = ham.splitlines(keepends=True)
                if any(
                    not s.endswith(b"\n") or (s.endswith(_KESIK) and s == _KESIK)
                    for s in satirlar[:-1]
                ):
                    raise PilotHatasi("WF günlüğünde iç kesik veya belirsiz satır var.")
                if satirlar and not satirlar[-1].endswith(b"\n"):
                    if any(
                        o["kayit_turu"] == "bitis" and o.get("kosu_id") == kosu_id
                        for o in olaylar
                    ):
                        raise PilotHatasi("Bitmiş WF sonrasında belirsiz kuyruk var.")
                    fd = os.open(
                        self.yol,
                        os.O_WRONLY | os.O_APPEND | getattr(os, "O_BINARY", 0),
                    )
                    try:
                        _icerik_yaz(fd, _KESIK)
                    finally:
                        os.close(fd)
                    olaylar, uyarilar = self._oku()
            makbuz = Makbuz(
                baslangic["kayit_id"],
                deneme_id,
                kosu_id,
                deneme["ayar_parmak_izi"],
                list(uyarilar),
            )
            kosu = _Kosu(self, makbuz, deneme, baslangic)
            try:
                yield kosu
                if kosu._tekrar_sira != len(kosu._tekrar_adaylari):
                    raise PilotHatasi("WF yayımlanmış öneği tüketilmedi.")
            finally:
                kosu._etkin = False

    @contextmanager
    def _ileri_cocuk_devam(self, ust_kosu_id, cocuk, baslangic, *, sonuc_hazir=False):
        """TASARIM 5.15 S12: çocuk başlangıcı ikinci kez yayımlanmaz."""
        if cocuk["baglar"].get("ileri_ust_kosu") != ust_kosu_id:
            raise PilotHatasi("WF çocuk başka üst koşuya bağlı.")
        olaylar = self.oku()
        adaylar = [
            o
            for o in olaylar
            if o["kayit_turu"] == "baslangic" and o["deneme_id"] == cocuk["deneme_id"]
        ]
        if adaylar != [baslangic]:
            raise PilotHatasi("WF çocuk başlangıcı tekil değil.")
        makbuz = Makbuz(
            baslangic["kayit_id"],
            cocuk["deneme_id"],
            baslangic["kosu_id"],
            cocuk["ayar_parmak_izi"],
        )
        kosu = _Kosu(self, makbuz, cocuk, baslangic)
        bas = olaylar.index(baslangic)
        kosu._tekrar_adaylari = [
            o
            for o in olaylar[bas + 1 :]
            if o.get("kosu_id") == makbuz.kosu_id and o["kayit_turu"] != "bitis"
        ]
        if sonuc_hazir:
            sonuclar = [o for o in kosu._tekrar_adaylari if o["kayit_turu"] == "sonuc"]
            if len(sonuclar) != 1 or sonuclar[0] != kosu._tekrar_adaylari[-1]:
                raise PilotHatasi("WF çocuk sonuç öneği geçersiz.")
            kosu._tekrar_adaylari = []
        try:
            yield kosu
            if kosu._tekrar_sira != len(kosu._tekrar_adaylari):
                raise PilotHatasi("WF çocuk öneği tüketilmedi.")
        finally:
            kosu._etkin = False

    def izle(self, olay_id):
        olaylar = self.oku()
        sonuc = _bul(olaylar, olay_id)
        if sonuc["kayit_turu"] not in ("sonuc", "islem", "senaryo", *_MC_ALANLAR):
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
        sonuc = {
            "olaylar": olaylar,
            "uyarilar": uyarilar,
            "cozumsuz_kosular": [
                o["kosu_id"]
                for o in olaylar
                if o["kayit_turu"] == "baslangic" and o["kosu_id"] not in biten
            ],
        }
        mc = [
            b
            for b in olaylar
            if b["kayit_turu"] == "baslangic"
            and b["kosu_id"] not in biten
            and _bul(olaylar, b["deneme_id"], "deneme", "deneme_id")[
                "yontem_ayarlari"
            ].get("yontem")
            == "kayitli_monte_carlo_v1"
        ]
        if mc:
            sonuc["mc_belirsiz_kosular"] = [
                _mc_kurtarma(olaylar, b["kosu_id"]) for b in mc
            ]
        return sonuc

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
                if _mc_baslangic_mi(olaylar, olay):
                    _mc_baslangic_dogrula(olaylar, olay)
                if _mc_isareti(olay) and olay["kayit_turu"] not in _MC_ALANLAR:
                    _mc_kayit_dogrula(olaylar, olay)
                if denetle:
                    denetle(olaylar)
                _isinma_olayi_dogrula(olaylar, olay)
                if _ileri_kaydi_mi(olaylar, olay):
                    _ileri_olayi_dogrula(olaylar, olay)
                _ileri_yeni_cocuk_dogrula(olaylar, olay)
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
        if str(yontem_ayarlari.get("yontem", "")).startswith("kayitli_monte_carlo"):
            _mc_yontemi(yontem_ayarlari)
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
        if baglar.keys() - {
            "izgara_ust_deneme",
            "egitim_denemeleri",
            "test_deneme",
            "ileri_ust_kosu",
        }:
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


def _ileri_tekrar_anahtari(o):
    tur = o["kayit_turu"]
    if tur in ("ileri_secim", "ileri_kontrol"):
        return tur, o["bolum_id"], o["sembol"]
    if tur == "ileri_sinyal":
        return tur, o["secim_ref"], o["sinyal"]["kaynak_sinyal"]["kayit_id"]
    if tur == "islem":
        return tur, o["olaylar"][0]["pozisyon"]["risk_girdisi"]["islem_id"]
    if tur == "sonuc":
        return tur, o.get("sonuc_turu"), o.get("bolum_id", o.get("is_id"))
    return (tur,)


class _Kosu:
    def __init__(self, depo, makbuz, deneme, baslangic):
        self._depo, self.makbuz = depo, makbuz
        self._deneme, self._baslangic = deneme, baslangic
        self._etkin, self._bitti, self._yazma_hatasi = True, False, False
        self._tekrar_adaylari = []
        self._tekrar_sira = 0

    def _yaz(self, tur, alanlar, denetle=None):
        if not self._etkin or self._bitti or self._yazma_hatasi:
            raise PilotHatasi("Koşu kapalı veya yazma hatalı.")

        olay = {
            "kayit_turu": tur,
            "deneme_id": self.makbuz.deneme_id,
            "kosu_id": self.makbuz.kosu_id,
            "ayar_parmak_izi": self.makbuz.ayar_ozeti,
            "kaynaklar": self._deneme["kaynaklar"],
            **alanlar,
        }

        def kontrol(olaylar):
            if any(
                o["kayit_turu"] == "bitis" and o["kosu_id"] == self.makbuz.kosu_id
                for o in olaylar
            ):
                raise PilotHatasi("Koşu zaten bitti.")
            if denetle:
                denetle(olaylar)

        try:
            if self._tekrar_sira < len(self._tekrar_adaylari):
                aday = self._tekrar_adaylari[self._tekrar_sira]
                if _ileri_tekrar_anahtari(aday) != _ileri_tekrar_anahtari(olay):
                    raise PilotHatasi("WF kayıt öneği sırasız veya eşleşmedi.")
                meta = {"kayit_id", "sema_surumu", "olusturma_zamani"}
                if kanonik({k: v for k, v in aday.items() if k not in meta}) != kanonik(
                    olay
                ):
                    raise PilotHatasi("WF eski makbuzunun tam içeriği değişmiş.")
                _bul(self._depo.oku(), aday["kayit_id"], aday["kayit_turu"])
                self._tekrar_sira += 1
                return Makbuz(
                    aday["kayit_id"],
                    aday["deneme_id"],
                    aday["kosu_id"],
                    aday["ayar_parmak_izi"],
                )
            return self._depo._ekle(olay, kontrol)
        except PilotYazmaHatasi:
            self._yazma_hatasi = True
            raise

    def ileri_dayaniklastir(self, makbuz):
        """TASARIM 5.15 S03: WF başlangıç, çeyrek ve bitiş sınırını aktarır."""
        if self._baslangic["ortam"].get("ileri_devam_surumu") != "ileri_devam_v1":
            raise PilotHatasi("Dayanıklılık sınırı yalnız yeni WF koşusuna aittir.")
        with self._depo._kilit():
            olay = _bul(self._depo._oku()[0], makbuz.olay_id)
            if (
                olay["kosu_id"] != self.makbuz.kosu_id
                or olay["kayit_turu"] not in ("baslangic", "sonuc", "bitis")
                or (
                    olay["kayit_turu"] == "sonuc"
                    and (
                        olay.get("sonuc_turu") != "ileri_v1"
                        or olay["kayit"]["tur"] != "bolum"
                    )
                )
            ):
                raise PilotHatasi("WF dayanıklılık makbuzu geçersiz.")
            try:
                with self._depo.yol.open("r+b") as dosya:
                    os.fsync(dosya.fileno())
            except OSError as hata:
                raise PilotDayaniklilikHatasi(makbuz) from hata

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
            durum,
            birimler,
            icerik,
            islem_referanslari,
            uyarilar,
            cikti_referanslari,
            self._deneme,
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

    def ileri_secim_kaydet(self, *, kayit):
        """TASARIM 5.15 S12: testten önce değişmez eğitim/seçim bağı."""
        _ileri_ust(self._deneme)

        return self._yaz(
            "ileri_secim",
            dict(
                surum="ileri_secim_v1",
                bolum_id=kayit["bolum_id"],
                sembol=kayit["sembol"],
                kayit=kayit,
            ),
        )

    def ileri_sinyal_kaydet(self, *, secim_ref, sinyal):
        """TASARIM 5.15 S12: makbuz kimliği E3 sinyal_id olur."""
        _ileri_ust(self._deneme)

        secim = _bul(self._depo.oku(), secim_ref, "ileri_secim")
        return self._yaz(
            "ileri_sinyal",
            dict(
                surum="ileri_sinyal_v1",
                secim_ref=secim_ref,
                karar_bolumu=secim["bolum_id"],
                **{
                    a: secim["kayit"][a]
                    for a in (
                        "test_deneme_id",
                        "strateji_ayar_parmak_izi",
                        "deneme_ayar_parmak_izi",
                    )
                },
                sembol=sinyal["sembol"],
                tarih=sinyal["tarih"],
                sinyal=sinyal,
            ),
        )

    def ileri_kontrol_kaydet(self, *, bolum_id, sembol, durum, onceki_ref):
        """TASARIM 5.15 S12: mühürlü E3 durumu değiştirilmeden saklanır."""
        _ileri_ust(self._deneme)

        return self._yaz(
            "ileri_kontrol",
            dict(
                surum="ileri_kontrol_v1",
                bolum_id=bolum_id,
                sembol=sembol,
                durum=durum,
                onceki_ref=onceki_ref,
            ),
        )

    def ileri_islem_kaydet(self, *, islem, ufuk):
        """TASARIM 5.15 S12: nihai sonuç veya son ufukta açık sonuç bir kez."""
        _ileri_ust(self._deneme)
        from tansu.tansusinama import _ileri_kohort, _ileri_ufuk

        p = islem["pozisyon"]
        kimlik = p["risk_girdisi"]["islem_id"]
        rol = "tamamlanmis_islem" if islem["sonuc"]["kalan_adet"] == 0 else "acik_ufuk"
        sinyal = _bul(self._depo.oku(), p["risk_girdisi"]["sinyal_id"], "ileri_sinyal")
        if kanonik(ufuk) != kanonik(_ileri_ufuk(self._deneme)):
            raise PilotHatasi("WF işlem ufku kayıtlı yöntemle uyuşmuyor.")

        return self._yaz(
            "islem",
            dict(
                islem_turu="ileri_islem_v1",
                islem_id=kimlik,
                rol=rol,
                sinyal_id=sinyal["kayit_id"],
                sembol=sinyal["sembol"],
                karar_bolumu=_bul(self._depo.oku(), sinyal["secim_ref"], "ileri_secim")[
                    "bolum_id"
                ],
                giris_kohortu=_ileri_kohort(p["giris_tarih"]),
                donem=ufuk,
                olaylar=[islem],
                birimler=dict(net_r="R", net_sonuc="TL", kalan_adet="adet"),
                veri_ref_id=self._baslangic["anlik_goruntu"],
            ),
        )

    def ileri_sonucu_kaydet(self, *, kayit):
        """TASARIM 5.15 S12: nihai işlem ve kontrol noktası ayrı türdür."""
        _ileri_ust(self._deneme)

        return self._yaz(
            "sonuc",
            dict(
                sonuc_turu="ileri_v1",
                bolum_id=kayit["bolum_id"],
                kayit=kayit,
                veri_ref_id=self._baslangic["anlik_goruntu"],
            ),
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

    def _mc_yaz(self, tur, kayit):
        alanlar = dict(
            surum=f"{tur}_v1",
            yontem_surumu="kayitli_monte_carlo_v1",
            icerik_ozeti=_mc_ozet(kayit),
            kayit=kayit,
        )

        def denetle(olaylar):
            o = dict(
                kayit_id="hazirlanan_mc_kaydi",
                sema_surumu=SURUM,
                olusturma_zamani=datetime.now(timezone.utc),
                kayit_turu=tur,
                deneme_id=self.makbuz.deneme_id,
                kosu_id=self.makbuz.kosu_id,
                ayar_parmak_izi=self.makbuz.ayar_ozeti,
                kaynaklar=self._deneme["kaynaklar"],
                **alanlar,
            )
            _mc_kayit_dogrula(olaylar, o)

        return self._yaz(tur, alanlar, denetle)

    def _mc_parti_yaz(self, tur, kayitlar):
        """TASARIM 5.15 S13: yalnız MC; kalıcı zarf kesinleşmeden iç makbuz dönmez."""
        parti_id = f"{SURUM}:{uuid4()}"
        zaman = datetime.now(timezone.utc)
        ortak = dict(
            sema_surumu=SURUM,
            olusturma_zamani=zaman,
            deneme_id=self.makbuz.deneme_id,
            kosu_id=self.makbuz.kosu_id,
            ayar_parmak_izi=self.makbuz.ayar_ozeti,
            kaynaklar=self._deneme["kaynaklar"],
        )
        ic = []
        for k in kayitlar:
            if tur == "deneme":
                _mc_alanlar(
                    k,
                    "strateji donemler veri_ayarlari yontem_ayarlari risk_ayarlari masraf_ayarlari eski_referans",
                )
                strateji = _strateji_kaydi(k["strateji"])
                ayarlar = {
                    a: k[a]
                    for a in (
                        "donemler",
                        "veri_ayarlari",
                        "yontem_ayarlari",
                        "risk_ayarlari",
                        "masraf_ayarlari",
                    )
                }
                ayarlar["strateji"] = {
                    a: v for a, v in strateji.items() if a != "olusturma_zamani"
                }
                o = dict(
                    ortak,
                    kayit_turu="deneme",
                    deneme_id=f"{SURUM}:d:{uuid4()}",
                    kimlik_bicimi_surumu=SURUM,
                    olusturan="S13",
                    neden="Donmuş WF seçiminin izinli ayar stresi.",
                    **{a: v for a, v in ayarlar.items() if a != "strateji"},
                    strateji=strateji,
                    ust_deneme_id=self.makbuz.deneme_id,
                    eski_referans=k["eski_referans"],
                    baglar=dict(izgara_ust_deneme=self.makbuz.deneme_id),
                    bos_nedenleri={},
                    ayar_parmak_izi=_ayar_ozeti(ayarlar),
                    kaynaklar=strateji["kaynaklar"],
                )
            else:
                o = dict(
                    ortak,
                    kayit_turu=tur,
                    surum=f"{tur}_v1",
                    yontem_surumu="kayitli_monte_carlo_v1",
                    icerik_ozeti=_mc_ozet(k),
                    kayit=k,
                )
            ic.append(dict(o, kayit_id=f"{SURUM}:{uuid4()}", parti_ref=parti_id))
        k = dict(kayitlar=ic)
        parti = dict(
            ortak,
            kayit_id=parti_id,
            kayit_turu="mc_parti",
            surum="mc_parti_v1",
            yontem_surumu="kayitli_monte_carlo_v1",
            icerik_ozeti=_mc_ozet(k),
            kayit=k,
        )
        makbuz = self._yaz(
            "mc_parti",
            {
                a: v
                for a, v in parti.items()
                if a
                not in (
                    "kayit_turu",
                    "deneme_id",
                    "kosu_id",
                    "ayar_parmak_izi",
                    "kaynaklar",
                )
            },
            lambda olaylar: _mc_partiyi_ac(olaylar, parti),
        )
        return [
            Makbuz(
                o["kayit_id"],
                o["deneme_id"],
                o["kosu_id"],
                o["ayar_parmak_izi"],
                list(makbuz.uyarilar),
            )
            for o in ic
        ]

    def mc_planlari_kaydet(self, *, kayitlar):
        return self._mc_parti_yaz("mc_plan", kayitlar)

    def mc_sonuclari_kaydet(self, *, kayitlar):
        return self._mc_parti_yaz("mc_senaryo", kayitlar)

    def mc_sinyalleri_kaydet(self, *, kayitlar):
        return self._mc_parti_yaz("mc_sinyal", kayitlar)

    def mc_stres_revizyonlari_kaydet(self, *, kayitlar):
        return self._mc_parti_yaz("deneme", kayitlar)

    def mc_girdi_kaydet(self, *, kayit):
        """TASARIM 5.15 S13: gerçek WF nüfusu hesap öncesinde kalıcıdır."""
        return self._mc_yaz("mc_girdi", kayit)

    def mc_plan_kaydet(self, *, kayit):
        """TASARIM 5.15 S13: tam çekiliş ve stres revizyonları hesap öncesindedir."""
        return self._mc_yaz("mc_plan", kayit)

    def mc_sinyal_kaydet(self, *, kayit):
        """TASARIM 5.15 S13: E2 kaydı E3'ün değişmez sinyal sahibidir."""
        return self._mc_yaz("mc_sinyal", kayit)

    def mc_senaryo_sonucu_kaydet(self, *, kayit):
        """TASARIM 5.15 S13: bir plana bir kesin sonuç."""
        return self._mc_yaz("mc_senaryo", kayit)

    def mc_kontrol_kaydet(self, *, kayit):
        """TASARIM 5.15 S13: gerçek sonuç öneğinin sayısal tanısı."""
        return self._mc_yaz("mc_kontrol", kayit)

    def mc_ozet_kaydet(self, *, kayit):
        """TASARIM 5.15 S13: her gerekli anahtar kendi sayılarıyla görünürdür."""
        return self._mc_yaz("mc_ozet", kayit)

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
            if (
                self._deneme["yontem_ayarlari"].get("yontem")
                == "kayitli_monte_carlo_v1"
            ):
                _mc_bitis_dogrula(
                    olaylar,
                    self.makbuz.kosu_id,
                    durum,
                    tamamlanan,
                    basarisiz,
                    cikti_referanslari,
                    yontemler=yontemler,
                    olculer=olculer,
                    ozetler=ozetler,
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
