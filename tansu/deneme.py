"""Geçici kayıt sınırı (TASARIM 5.15); kalıcı bayt biçimi #97'dir."""

from datetime import date, datetime, timezone
from decimal import Decimal
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from hashlib import sha256
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
        for deger in (
            mod,
            anlik_goruntu,
            manifest_ozeti,
            uyelik_surumu,
            kod_kimligi,
            bagimlilik_ozeti,
        ):
            _metin(deger)
        if not isinstance(ortam, dict) or not ortam:
            raise PilotHatasi("Ortam gerekli.")
        if (
            not isinstance(is_listesi, list)
            or not is_listesi
            or len(set(is_listesi)) != len(is_listesi)
        ):
            raise PilotHatasi("İş listesi boş veya yinelenmiş.")
        for is_id in is_listesi:
            _metin(is_id)
        is_listesi = list(is_listesi)
        if tohum is not None and (type(tohum) is not int or not ureteci_surumu):
            raise PilotHatasi("Tohum tamsayı ve üreteç sürümü gerekli.")
        try:
            deneme = _bul(self.oku(), deneme_id, "deneme", "deneme_id")
        except OSError as hata:
            raise PilotYazmaHatasi(f"Pilot kaydı okunamadı: {hata}") from hata
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
        strateji = asdict(katalog.legacy_coz(varyant))
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
                "ayar_parmak_izi": f"{SURUM}:sha256:{sha256(kanonik(ayarlar)).hexdigest()}",
            },
            denetle,
        )


def _bul(olaylar, kimlik, tur=None, alan="kayit_id"):
    for olay in olaylar:
        if olay.get(alan) == kimlik and (tur is None or olay["kayit_turu"] == tur):
            return olay
    raise PilotHatasi("Kayıt bağı bulunamadı.")


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
        )
        self._bitti = True
        return makbuz
