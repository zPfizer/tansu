"""Günlük koşu: indir, kapılardan geçir, kartları ve `durum.txt`'yi yaz (TASARIM 6)."""

import csv
import datetime as dt
import json
import math
import os
import re
import shutil
from contextlib import ExitStack, contextmanager
from pathlib import Path

import pandas as pd

from tansu import (
    aileler,
    ciftbolme,
    evren,
    islem_riski,
    kayit,
    kaynak as kaynak_modulu,
    motor,
    rapor,
    simulator,
    veri,
)

ERKEN = dt.time(18, 15)  # TASARIM 6.2: bundan önce çubuk yarım olabilir
KAGIT_AY = 6  # TASARIM 5.8: en az kâğıt dönem
BASARILI = ("TAMAM", "BUGÜN ÇUBUK YOK")
KARTLI = ("Kâğıt", "Canlı")
RET = ("KART GÜNLÜĞÜ EKSİK", "KAYIT ÇELİŞKİSİ")
SUTUNLAR = [
    "tarih",
    "hisse",
    "aile",
    "durum",
    "referans",
    "stop",
    "pozisyon_yuzde",
    "adet",
    "fiili_risk",
    "likidite_siniri_tl",
    "kanit",
    "kaynak",
]
AILE_ADI = {simulator.AILE: "EMA sıkışması"}


def _sayi(x) -> str:
    return f"{x:.2f}".replace(".", ",")


def _isaretli(x) -> str:
    return ("+" if x >= 0 else "−") + rapor.yuzde(abs(x))


def _kanit(aile, tarih) -> str:
    """Ailenin kanıt satırı: son resmi `durum` satırındaki `kanit` alanından (TASARIM 6.5)."""
    satirlar = kayit.resmi_durumlar(aile)
    bas = satirlar[-1]
    for s in reversed(satirlar):
        if s["durum"] not in KARTLI:
            break
        bas = s
    ay = (tarih.date() - dt.date.fromisoformat(bas["tarih"][:10])).days // 30
    k = satirlar[-1].get("kanit")
    if not k or None in (k["fazla"], *k["ci"]):
        return f"{satirlar[-1]['durum']} · kanıt kaydı yok · kâğıt dönem {ay}/{KAGIT_AY} ay"
    alt, ust = k["ci"]
    aralik = (
        "sıfırı içeriyor: ayırt edilemiyor"
        if alt <= 0 <= ust
        else f"{_isaretli(alt)} ile {_isaretli(ust)}"
    )
    return (
        f"{satirlar[-1]['durum']} · {k['islem']} işlem · sepete göre işlem başına fazla getiri "
        f"{_isaretli(k['fazla'])} (%0,3 masraf) · portföy fazla getirisi (K2'ye göre, yıllık, blok bootstrap "
        f"%95 aralık {aralik}) · kâğıt dönem {ay}/{KAGIT_AY} ay"
    )


ETIKET = {
    "stop": "STOP",
    "sma250": "GÜN SONU STOPU",
    "karantina": "KARANTİNA ÇIKIŞI",
    "iptal": "GİRİŞ İPTAL",
}


def _durum(p) -> str:
    """AKTİF: bekleyen giriş ya da açık pozisyon. STOP: stop değdi. Öteki üçü: SMA250 altı, karantina, iptal (TASARIM 6.6)."""
    if p.durum == "kapali":
        return ETIKET[p.neden]
    return ETIKET.get(p.bekleyen, "AKTİF")


def _kart(anlik, s, m, p, kanit) -> list | dict:
    # TASARIM 5.15 S08: açık risk isteği eski CSV/kart günlüğünü değiştirmez.
    if getattr(p, "risk_girdisi", None) is not None:
        return {"hisse": s, "kanit": kanit, **islem_riski.hesapla(p.risk_girdisi)}
    f = anlik.fiyat[anlik.fiyat["sembol"] == s].set_index("tarih")
    sinyal = p.sinyal_tarih
    ref, oran = (
        f.at[sinyal, "ham_kapanis"],
        f.at[sinyal, "ham_kapanis"] / f.at[sinyal, "kapanis"],
    )
    atr = p.atr * oran
    stop = p.stop * oran if p.stop is not None else ref - motor.STOP_ATR * atr
    lq = (
        f["hacim"]
        .reindex(m.index)
        .fillna(0)
        .rolling(simulator.LIKIDITE_GUN, min_periods=1)
        .median()
        .at[sinyal]
    )
    ozk = simulator.SERMAYE
    adet = int(
        math.floor(
            min(
                simulator.RISK * ozk / (motor.STOP_ATR * atr),
                simulator.TAVAN * ozk / ref,
                simulator.LIKIDITE * lq / ref,
            )
        )
    )
    return [
        sinyal.date().isoformat(),
        s,
        AILE_ADI[simulator.AILE],
        _durum(p),
        _sayi(ref),
        _sayi(stop) + (" (tahmini)" if p.stop is None else ""),
        rapor.yuzde(adet * ref / ozk),
        adet,
        rapor.yuzde(adet * max(0.0, ref - stop) / ozk),
        f"{simulator.LIKIDITE * lq:.0f}",
        kanit,
        f"Tansu'dan esinlenen yorum · İş Yatırım {anlik.kimlik}",
    ]


def _kartlar(anlik, tarih, p, atr_n, aktarim=None) -> list:
    """Kâğıt ve Canlı ailelerin kartları; her gün sinyal gününden itibaren Adım ile yeniden hesaplanır (TASARIM 6.6)."""
    if ciftbolme.AILE in {a for a in kayit.AILELER if kayit.durum_oku(a) in KARTLI}:
        raise kayit.KayitHatasi("çift ailesi Kâğıt: çift kartı henüz yazılmadı")
    if kayit.durum_oku(simulator.AILE) not in KARTLI:
        if aktarim is not None:
            aktarim.sonuc({"kartlar": []}, [])
        return []
    kanit, kartlar = _kanit(simulator.AILE, tarih), []
    if aktarim is not None and aktarim.deneme_id is not None:
        # TASARIM 5.15: aile kanıtı kayıtlı ayarın etkinleştirme kanıtı değildir.
        kanit = f"Kayıtlı ayar önizlemesi · etkinleştirme kanıtı değil · {aktarim.deneme_id}"
    for s in sorted(anlik.fiyat["sembol"].unique()):
        m = motor.mumlar(anlik, s, p, atr_n)
        f = m.dropna(subset=["kapanis"])
        kurulum = aileler.kurulum(f, p)
        sinyaller = None
        if aktarim is not None:
            aktarim.ayar_dogrula(p)
            sinyaller = aktarim.sinyaller(m, kurulum, s)
            for kimlik in sinyaller.values():
                aktarim._oku(kimlik)
        poz, kapanan = motor.tara(
            m, kurulum.index, p, motor.kurulum_bilgisi(f, p, hesaplanan=kurulum)
        )[2:]
        yeni = [_kart(anlik, s, m, x, kanit) for x in (poz, kapanan) if x is not None]
        kartlar += yeni
        if aktarim is not None:
            referanslar = aktarim.pozisyonlar(
                [x for x in (poz, kapanan) if x is not None], sinyaller
            )
            aktarim.sonuc({"hisse": s, "kartlar": yeni}, referanslar)
    return kartlar


def _yaz(yol: Path, yaz_fn) -> None:
    """Geçici dosyaya yazıp `os.replace` ile taşır (TASARIM 6.7)."""
    gecici = yol.with_name(yol.name + ".gecici")
    yol.parent.mkdir(parents=True, exist_ok=True)
    with gecici.open(
        "w", encoding="utf-8-sig" if yol.suffix == ".csv" else "utf-8", newline=""
    ) as f:
        yaz_fn(f)
    try:
        os.replace(gecici, yol)
    except PermissionError:
        gecici.unlink(missing_ok=True)
        raise


def _gunluk_satirlari(yol):
    return (
        [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s]
        if yol.exists()
        else []
    )


def _kart_gunlugu(
    tarih, kimlik, kartlar, yol=None, durum=None, tarih_kaynagi=None, neden=None
) -> None:
    yol = yol if yol is not None else kayit.KAYIT_DIZINI / "kartlar.jsonl"
    yol.parent.mkdir(parents=True, exist_ok=True)
    gun = tarih.date().isoformat() if tarih is not None else None
    satir = {"tarih": gun, "anlik": kimlik}
    if kartlar is not None:
        satir["kartlar"] = [dict(zip(SUTUNLAR, k, strict=True)) for k in kartlar]
    if durum is not None:
        satir["durum"] = durum
    if tarih_kaynagi is not None:
        satir["tarih_kaynagi"] = tarih_kaynagi
    if neden is not None:
        satir["neden"] = neden
    satirlar = _gunluk_satirlari(yol)
    if durum in RET:
        if satir in satirlar:
            return
    elif _gun_bagi(tarih, kimlik, satirlar) is not None:
        return
    with yol.open("a", encoding="utf-8") as f:  # yalnız ekleme
        f.write(json.dumps(satir, ensure_ascii=False, sort_keys=True) + "\n")


def _gun_bagi(tarih, kimlik, satirlar):
    """TASARIM 6 #126: ret işareti, aynı günün başarı satırından önce gelir."""
    gun = tarih.date().isoformat()
    for s in satirlar:
        if s.get("durum") in RET and s["tarih"] in (None, gun):
            raise veri.VeriHatasi(
                f"{s['durum']}: {s.get('neden', 'önceki başarının kart kaydı bulunamadı')}"
            )
    bag = next((s for s in satirlar if s["tarih"] == gun), None)
    if bag is not None and bag["anlik"] != kimlik:
        raise veri.VeriHatasi("bugünün başarılı koşusu farklı görüntü kimliğine bağlı")
    return bag


def _ekran_gunu(onceki):
    alanlar = dict(s.split(": ", 1) for s in onceki[1:] if ": " in s)
    acik_gun = re.match(
        r"İstenen gün: (\d{4}-\d{2}-\d{2})\. ", alanlar.get("Eylem", "")
    )
    gun = (
        acik_gun[1]
        if acik_gun
        else alanlar.get("Son çubuk", "")
        if onceki[:1] == ["TAMAM"]
        else ""
    )
    try:
        return pd.Timestamp(dt.date.fromisoformat(gun))
    except ValueError:
        return None


def _kart_degerleri(kartlar):
    sonuc = []
    for kart in kartlar:
        degerler = (
            [_alan(kart, s) for s in SUTUNLAR] if isinstance(kart, dict) else kart
        )
        sonuc.append(["" if v is None else str(v) for v in degerler])
    return sonuc


def _indirilen_cubuksuz(onceki):
    """TASARIM 6 #126: açık indirme kökeni tamamlanma satırı gerektirmez."""
    gun = _ekran_gunu(onceki)
    return (
        onceki[:1] == ["BUGÜN ÇUBUK YOK"]
        and gun is not None
        and any(
            s.startswith(f"Eylem: İstenen gün: {gun:%Y-%m-%d}. Girdi: indirme. ")
            for s in onceki
        )
    )


def _csv_dogrula(bag, dizin, gunluk_yolu):
    """TASARIM 6 #126: kabul edilen kartlar gerçek CSV ile birlikte doğrulanır."""
    if bag.get("durum", "TAMAM") != "TAMAM":
        return
    tarih = pd.Timestamp(bag["tarih"])
    yol = dizin / f"kartlar-{tarih:%Y%m%d}.csv"
    neden = None
    try:
        with yol.open(encoding="utf-8-sig", newline="") as f:
            satirlar = list(csv.reader(f, delimiter=";"))
        beklenen = _kart_degerleri(bag["kartlar"])
        if satirlar != [SUTUNLAR, *beklenen]:
            neden = "kart CSV içeriği kabul edilen günlükle uyuşmuyor"
    except OSError, ValueError, KeyError, TypeError, csv.Error:
        neden = "kabul edilen kart CSV veya kart alanları okunamıyor"
    if neden is not None:
        _kart_gunlugu(
            tarih, bag["anlik"], None, gunluk_yolu, "KAYIT ÇELİŞKİSİ", neden=neden
        )
        raise veri.VeriHatasi(f"KAYIT ÇELİŞKİSİ: {neden}")
    return beklenen


def _eski_durum_bagi(onceki, yol, dizin):
    """TASARIM 6 #126: eski ekran kaybolmadan uyum veya ret kaydını korur."""
    if not onceki or onceki[0] not in BASARILI or _indirilen_cubuksuz(onceki):
        return
    alanlar = dict(s.split(": ", 1) for s in onceki[1:] if ": " in s)
    kimlik = alanlar.get("Anlık görüntü", "yok")
    tarih = _ekran_gunu(onceki)
    cubuksuz = onceki[0] == "BUGÜN ÇUBUK YOK"
    eski_cubuksuz = cubuksuz and not alanlar.get("Eylem", "").startswith(
        "İstenen gün: "
    )
    if eski_cubuksuz:
        try:
            tarih = pd.Timestamp(
                dt.date.fromisoformat(alanlar.get("Son başarılı koşu", "")[:10])
            )
        except ValueError:
            tarih = None
    gun = tarih.date().isoformat() if tarih is not None else None
    satirlar = _gunluk_satirlari(yol)
    if any(s.get("durum") in RET and s["tarih"] in (None, gun) for s in satirlar):
        return
    bag = next(
        (
            s
            for s in satirlar
            if s["tarih"] == gun
            and s["anlik"] == kimlik
            and s.get("durum", "TAMAM") == onceki[0]
        ),
        None,
    )
    if bag is not None:
        _csv_dogrula(bag, dizin, yol)
        return
    if eski_cubuksuz and tarih is not None:
        if any(s["tarih"] == gun for s in satirlar):
            _kart_gunlugu(
                tarih,
                kimlik,
                None,
                yol,
                "KAYIT ÇELİŞKİSİ",
                neden="eski çubuksuz ekranın uyum anahtarı başka sonuca bağlı",
            )
        else:
            _kart_gunlugu(tarih, kimlik, [], yol, "BUGÜN ÇUBUK YOK", "eski_kosu_saati")
    else:
        _kart_gunlugu(tarih, kimlik, None, yol, "KART GÜNLÜĞÜ EKSİK")


@contextmanager
def _cikti_kilidi(dizin):
    """TASARIM 6 #126: kilit dosyası kalır; sahipliği işletim sistemi bırakır."""
    dizin.mkdir(parents=True, exist_ok=True)
    with (dizin / ".gunluk.kilit").open("a+b") as dosya:
        dosya.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(dosya.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(dosya.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            dosya.seek(0)
            if os.name == "nt":
                msvcrt.locking(dosya.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(dosya.fileno(), fcntl.LOCK_UN)


def _alan(kart, ad):
    """Kart günlüğü yalnız eklenir: eski satırlar büyük harfli anahtarla (`Hisse`) kalır (bilet 07a)."""
    return kart[ad] if ad in kart else kart[ad.capitalize()]


def _acik_hisseler() -> set:
    """Dünkü her kartın hissesi, durumundan bağımsız: evrenden çıksa da pozisyon açık kalır (TASARIM 5.2, 6.2)."""
    yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    for satir in reversed(_gunluk_satirlari(yol)):
        if satir.get("durum") not in ("BUGÜN ÇUBUK YOK", *RET):
            return {_alan(k, "hisse") for k in satir["kartlar"]}
    return set()


def _semboller(kok: Path, tarih) -> list:
    """Bugünkü evren (en çok sembollü son tam anlık görüntüden) ve açık kartların hisseleri (TASARIM 6.2)."""
    klasorler = sorted((kok / "ag").glob("2*"))
    if not klasorler:
        raise veri.VeriHatasi(
            "evren için tam anlık görüntü yok: önce `python -m tansu evren-indir` çalıştır"
        )
    taban = veri.oku(klasorler[-1].name, kok)
    ay = min(tarih, taban.gunler[-1])  # taban eskiyse tabanın son ayının evreni (YORUM)
    return sorted(set(evren.evren(taban, ay)) | _acik_hisseler())


def _temizle(kok: Path) -> None:
    """Yarım kalmış geçici indirme klasörleri silinir; anlık görüntüler silinmez (TASARIM 5.11, 6.2)."""
    ag = kok / "gunluk" / "ag"
    if not ag.exists():
        return
    for d in ag.iterdir():
        if d.name.startswith("_gecici"):
            shutil.rmtree(d, ignore_errors=True)


def _kapi_sorunlari(anlik, son) -> list:
    """Veri kapıları evren üyesi hisse-günlerde (TASARIM 5.13). Geçmişteki kaynak günleri eksik gün olarak zaten
    işlenir; yalnız bugünün kaynak günü hatası kartı durdurur."""
    f = anlik.fiyat
    uye = f.loc[f["tarih"] >= pd.Timestamp(simulator.BASLANGIC), ["sembol", "tarih"]]
    bugun = f"kaynak günü hatası: {son.date()}"
    return [
        x
        for x in anlik.sorunlar_uye(uye)
        if not x.startswith("kaynak günü hatası") or x == bugun
    ]


def gunluk(
    tarih,
    kok="veri",
    simdi=None,
    kaynak=None,
    semboller=None,
    p=aileler.Parametre(),
    atr_n=motor.ATR_N,
    aktarim=None,
    kimlik=None,
    cikti_koku=None,
) -> int:
    """Günlük koşu; çıkış kodu: TAMAM ve BUGÜN ÇUBUK YOK 0, SORUNLU ve VERİ YOK 1. `kaynak`, `semboller`, `p` testte verilir."""
    tarih, kok = pd.Timestamp(tarih), Path(kok)
    simdi = simdi or dt.datetime.now(veri.ISTANBUL)
    # TASARIM 6 #126: çıktı yolları girdinin ve küresel sabitlerin yerine geçmez.
    cikti = Path(cikti_koku) if cikti_koku is not None else None
    rapor_dizini = cikti / "rapor" if cikti is not None else rapor.RAPOR_DIZINI
    veri_koku = cikti / "veri" if cikti is not None else kok
    kart_yolu = (
        cikti / "kayit" if cikti is not None else kayit.KAYIT_DIZINI
    ) / "kartlar.jsonl"
    if kimlik is not None and re.fullmatch(r"[A-Za-z0-9_-]+", kimlik):
        goruntu = (kok / "ag" / kimlik).resolve()
        if any(y.resolve().is_relative_to(goruntu) for y in (rapor_dizini, kart_yolu)):
            raise veri.VeriHatasi("çıktı yolu saklı görüntünün içine yazamaz")
    onizleme = aktarim is not None and aktarim.deneme_id is not None
    # TASARIM 5.15 S07: önizleme normal günlüğün tamamlanma ve kart durumunu yazmaz.
    dizin = rapor_dizini / "onizleme" / aktarim.kosu_id if onizleme else rapor_dizini
    yol = dizin / "durum.txt"
    kilitler = ExitStack()
    try:
        alanlar = {dizin.resolve()}
        if not onizleme:
            alanlar.add(kart_yolu.parent.resolve())
        for alan in sorted(alanlar):
            kilitler.enter_context(_cikti_kilidi(alan))
    except OSError as hata:
        kilitler.close()
        print(
            f"SORUNLU - Günlük çıktı kilidi alınamadı; başka koşu çalışıyor olabilir: {hata}"
        )
        return 1
    try:
        onceki = yol.read_text(encoding="utf-8").splitlines() if yol.exists() else []
        acik_gunlu_ekran = any(s.startswith("Eylem: İstenen gün: ") for s in onceki)
        saat = next(
            (
                x.split(": ", 1)[1]
                for x in onceki
                if x.startswith("Son başarılı koşu: ")
            ),
            "yok",
        )

        def bitir(durum, eylem, kimlik="yok", son="yok", sayi="yok") -> int:
            basarili = durum in BASARILI
            # TASARIM 6 #126: türetilen ekran da bilinen istenen günü taşır.
            if (istenen_kimlik is not None or acik_gunlu_ekran) and not onizleme:
                if istenen_kimlik is None and durum == "BUGÜN ÇUBUK YOK":
                    eylem = f"Girdi: indirme. {eylem}"
                eylem = f"İstenen gün: {tarih.date().isoformat()}. {eylem}"
            satirlar = [
                durum,
                f"Son başarılı koşu: {simdi:%Y-%m-%d %H:%M}"
                if basarili
                else f"Son başarılı koşu: {saat}",
                f"Anlık görüntü: {kimlik}",
                f"Son çubuk: {son}",
                f"Sembol sayısı: {sayi}",
                f"Eylem: {eylem}",
            ]
            _yaz(yol, lambda f: f.write("\n".join(satirlar) + "\n"))
            print(durum, "-", eylem)
            return 0 if basarili else 1

        istenen_kimlik = kimlik
        kimlik, son, sayi = kimlik or "yok", "yok", "yok"
        try:
            anlik = None
            if istenen_kimlik is not None:
                if not onizleme:
                    _eski_durum_bagi(onceki, kart_yolu, dizin)
                if not re.fullmatch(r"[A-Za-z0-9_-]+", istenen_kimlik):
                    raise veri.VeriHatasi(
                        f"geçersiz görüntü kimliği: {istenen_kimlik!r}"
                    )
                anlik = veri.oku(istenen_kimlik, kok)
                if aktarim is not None:
                    aktarim.veri_bagla(kimlik)
                    aktarim.ayar_dogrula(p)
                if not onizleme:
                    bag = _gun_bagi(tarih, kimlik, _gunluk_satirlari(kart_yolu))
                    if bag is not None:
                        _csv_dogrula(bag, dizin, kart_yolu)
                        durum = bag.get("durum", "TAMAM")
                        if (
                            onceki[:1] == [durum]
                            and f"Anlık görüntü: {kimlik}" in onceki
                            and _ekran_gunu(onceki) == tarih
                        ):
                            print("Bugünün başarılı koşusu var; bir şey yapılmadı.")
                            return 0
                        return bitir(
                            durum,
                            "Bugün işlem günü değil ya da çubuk yok; bir şey yapma."
                            if durum == "BUGÜN ÇUBUK YOK"
                            else f"Önceki başarılı kart tablosu korundu: {dizin / f'kartlar-{tarih:%Y%m%d}.csv'}",
                            kimlik,
                            anlik.gunler[-1].date().isoformat(),
                            anlik.fiyat["sembol"].nunique(),
                        )
            if (
                istenen_kimlik is None
                and onceki[:1]
                and onceki[0] in BASARILI
                and (
                    _ekran_gunu(onceki) == tarih
                    if acik_gunlu_ekran
                    else saat[:10] == tarih.date().isoformat()
                )
                and not onizleme
            ):
                if acik_gunlu_ekran and not _indirilen_cubuksuz(onceki):
                    # TASARIM 6 #126: seçeneksiz çağrı saklı ekranın kabulünü devralır.
                    _eski_durum_bagi(onceki, kart_yolu, dizin)
                    alanlar = dict(s.split(": ", 1) for s in onceki[1:] if ": " in s)
                    bag = _gun_bagi(
                        tarih, alanlar["Anlık görüntü"], _gunluk_satirlari(kart_yolu)
                    )
                    if bag is None:
                        raise veri.VeriHatasi(
                            "KART GÜNLÜĞÜ EKSİK: devralınacak başarı bulunamadı"
                        )
                    _csv_dogrula(bag, dizin, kart_yolu)
                print("Bugünün başarılı koşusu var; bir şey yapılmadı.")
                return 0
            if simdi.date() == tarih.date() and simdi.time() < ERKEN:
                return bitir(
                    "VERİ YOK",
                    "Koşu 18:15'ten önce başladı, kart üretilmedi (çubuk yarım olabilir). 18:15'ten sonra yeniden çalıştır.",
                )
            if anlik is None:
                _temizle(veri_koku)
                semboller = semboller or _semboller(kok, tarih)
                kimlik = veri.indir(
                    semboller,
                    veri_koku / "gunluk",
                    kaynak or kaynak_modulu.IsYatirim(),
                    simdi=simdi,
                )
                anlik = veri.oku(kimlik, veri_koku / "gunluk")
            if aktarim is not None:
                aktarim.veri_bagla(kimlik)
                aktarim.ayar_dogrula(p)
            son, sayi = anlik.gunler[-1], anlik.fiyat["sembol"].nunique()
            bilgi = dict(kimlik=kimlik, son=son.date().isoformat(), sayi=sayi)
            if son.date() != tarih.date():
                if istenen_kimlik is not None and not onizleme:
                    _kart_gunlugu(tarih, kimlik, [], kart_yolu, "BUGÜN ÇUBUK YOK")
                return bitir(
                    "BUGÜN ÇUBUK YOK",
                    "Bugün işlem günü değil ya da çubuk yok; bir şey yapma.",
                    **bilgi,
                )
            sorunlar = _kapi_sorunlari(anlik, son)
            if sorunlar:
                return bitir(
                    "SORUNLU",
                    "Kart üretilmedi: veri kapısı başarısız ("
                    + "; ".join(sorunlar)
                    + "). Kartlara güvenme.",
                    **bilgi,
                )
            kartlar = _kartlar(anlik, tarih, p, atr_n, aktarim)
            csv_yol = dizin / f"kartlar-{tarih:%Y%m%d}.csv"

            def yaz_csv(f):
                w = csv.writer(f, delimiter=";")
                w.writerow(SUTUNLAR)
                w.writerows(kartlar)

            if not onizleme:
                # TASARIM 6 #126: indirme de kabul edilen başka kimliğin CSV'sini yazamaz.
                bag = _gun_bagi(tarih, kimlik, _gunluk_satirlari(kart_yolu))
                if bag is not None:
                    kabul = _csv_dogrula(bag, dizin, kart_yolu)
                    if _kart_degerleri(kartlar) != kabul:
                        raise veri.VeriHatasi(
                            "yeni hesap kabul edilen kartlarla uyuşmuyor"
                        )
            try:
                _yaz(csv_yol, yaz_csv)
            except PermissionError:
                return bitir(
                    "SORUNLU",
                    f"Kart yazılamadı: {csv_yol.name} açık, kapatıp yeniden çalıştır.",
                    **bilgi,
                )
            if not onizleme:
                _kart_gunlugu(tarih, kimlik, kartlar, kart_yolu)
            return bitir(
                "TAMAM",
                f"Bugün {len(kartlar)} kart var: {csv_yol} dosyasını aç."
                if kartlar
                else f"Bugün kart yok; bir şey yapma. Tablo: {csv_yol}",
                **bilgi,
            )
        except veri.KaynakYok:
            return bitir(
                "VERİ YOK",
                "Kaynağa ulaşılamadı, kart üretilmedi. Saat başı yeniden denenir.",
            )
        except Exception as hata:  # noqa: BLE001 — her hata SORUNLU yazılır, çıkış kodu 1
            return bitir(
                "SORUNLU",
                f"Kart üretilmedi: {hata}. Hatayı oku ve yeniden çalıştır.",
                kimlik,
                str(son)[:10] if son != "yok" else son,
                sayi,
            )
    finally:
        kilitler.close()
