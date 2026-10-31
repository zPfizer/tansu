"""Komut girişi: `python -m tansu <komut>` (docs/SPEC.md bölüm 7)."""

import argparse
import contextlib
import datetime as dt
import msvcrt
import os
import shutil
import sys
import webbrowser
from pathlib import Path

import pandas as pd

from tansu import ayar, durum, kaynak, rapor, sinama, veri
from tansu.stratejiler import STRATEJILER

VERI_BASLANGIC = dt.date(2019, 1, 1)  # 2019-2020 yalnız ısınma (SPEC 3.4)
SAKLANAN_GORUNTU = 10
KILIT = "tansu-veri.kilit"
# Proje dosyaları (durum.csv, ayarlar, rapor) bu kökte: komut her klasörden aynı çalışır (31.10.2026).
PROJE = Path(__file__).resolve().parents[1]


def veri_koku() -> Path:
    return Path(os.environ.get("TANSU_VERI") or Path.home() / "Desktop" / "TANSU-veri")


def _kok_var(kok: Path) -> None:
    if not kok.is_dir():
        raise veri.VeriHatasi(
            f"veri kökü yok: {kok}; klasörü oluştur ya da TANSU_VERI ile var olan bir klasörü göster"
        )


@contextlib.contextmanager
def _tek_yazar(kok: Path):
    yol = kok / KILIT
    tutamak = os.open(yol, os.O_RDWR | os.O_CREAT)
    try:
        try:
            msvcrt.locking(tutamak, msvcrt.LK_NBLCK, 1)
        except OSError:
            raise veri.VeriHatasi(
                f"başka bir `tansu veri` koşusu sürüyor: {kok}"
            ) from None
        try:
            yield
        finally:
            msvcrt.locking(tutamak, msvcrt.LK_UNLCK, 1)
    finally:
        os.close(tutamak)
        # Başka tutamak açıkken Windows silmez, kilit tek kalır.
        with contextlib.suppress(OSError):
            yol.unlink()


def _goruntuler(kok: Path) -> list[Path]:
    """`ag/` altındaki görüntüler, eskiden yeniye; adı geçerli kimlik olmayan klasör (`2019-arsiv`) görüntü değildir."""
    return sorted(p for p in (kok / "ag").glob("2*") if veri.kimlik_gecerli(p.name))


def _son_kimlik(kok: Path) -> str:
    goruntuler = _goruntuler(kok)
    if not goruntuler:
        raise veri.VeriHatasi("anlık görüntü yok: önce `tansu veri` çalıştır")
    return goruntuler[-1].name


def son_anlik(kok: Path) -> veri.Anlik:
    _kok_var(kok)
    return veri.oku(_son_kimlik(kok), kok)


def goruntuleri_buda(
    kok: Path, korunan: frozenset[str] = frozenset(), saklanan: int = SAKLANAN_GORUNTU
) -> list[str]:
    """En yeni `saklanan` görüntüyü ve ayarların gösterdiklerini (`korunan`) tutar; yarım kalmış `_gecici-*` klasörlerini siler.

    `veri` kilidi altında çalışır. Silinen görüntülerin adlarını döndürür."""
    for yarim in (kok / "ag").glob("_gecici-*"):
        shutil.rmtree(yarim)
    eskiler = [p for p in _goruntuler(kok)[:-saklanan] if p.name not in korunan]
    for klasor in eskiler:
        shutil.rmtree(klasor)
    return [p.name for p in eskiler]


def _veri(a) -> int:
    try:
        _kok_var(a.kok)
        with _tek_yazar(a.kok):
            _indir_ve_yaz(a.kok)
    except (veri.VeriHatasi, kaynak.KaynakHatasi) as hata:
        print(f"tansu veri: {hata}", file=sys.stderr)
        return 1
    return 0


def _indir_ve_yaz(kok: Path) -> None:
    # Ayarların görüntüleri budanmaz; bozuk ayar dosyası indirmeden önce durdurur.
    korunan = ayar.veri_kimlikleri(PROJE / ayar.AYAR_KOKU)
    # Evren bütün BIST: bugünkü KAP listesi ve veri başlangıcından beri kapanan kodlar (SPEC 2, 3.4)
    kapanan = kaynak.kapanan_kodlar()
    kapanan = kapanan[~(kapanan["tarih"] < pd.Timestamp(VERI_BASLANGIC))]
    semboller = sorted(
        {*kaynak.sirket_kodlari().astype(str).str.strip(), *kapanan["kod"]}
    )
    k = kaynak.Artimli(
        kaynak.IsYatirim(), kok / "onbellek" / f"fiyat-{VERI_BASLANGIC:%Y%m%d}"
    )
    kimlik = veri.indir(semboller, kok, k, bas=VERI_BASLANGIC, kapanan=kapanan)
    silinen = goruntuleri_buda(kok, korunan)
    anlik = veri.oku(kimlik, kok)
    son_seans = anlik.gunler[-1]
    print(
        f"anlık görüntü {kimlik}; silinen eski görüntü: {len(silinen)}; "
        f"önbellek: {k.sayac['artimli']} artımlı, {k.sayac['tam']} tam"
    )
    print("sembol  ilk_tarih   son_tarih   satir  durum")
    tarihler = anlik.fiyat.groupby("sembol")["tarih"].agg(["min", "max", "size"])
    for s in semboller:
        if s in tarihler.index:
            ilk, son, n = tarihler.loc[s]
            durum = "tamam" if son >= son_seans else "son gün eksik"
            print(f"{s:<7} {ilk.date()}  {son.date()}  {n:>5}  {durum}")
        else:
            durum = "inmedi" if s in anlik.inmeyen else "kaynak boş"
            print(f"{s:<7} {'-':<10}  {'-':<10}  {0:>5}  {durum}")


def _yazilanlar(yol, json_yolu) -> str:
    yazilan = [str(p) for p in (yol and yol.parent, json_yolu) if p]
    return f" Bu koşunun yeni yazdıkları: {', '.join(yazilan)}." if yazilan else ""


def _kos(a, *, ayarla: bool) -> int:
    """`sina` ve `ayarla` için tek akış; farkları json yazımı ve durum geçişi (SPEC 4, 5.7)."""
    komut: durum.Komut = "ayarla" if ayarla else "sina"
    strateji = STRATEJILER.get(a.ad)
    if strateji is None:
        print(f"tansu {komut}: bilinmeyen strateji {a.ad}", file=sys.stderr)
        return 2
    yol = json_yolu = None
    durum_csv, ayarlar = PROJE / durum.DOSYA, PROJE / ayar.AYAR_KOKU
    try:
        satirlar = durum.oku(durum_csv)
        onceki = durum.durumu(satirlar, a.ad)
        if durum.reddeder(komut, onceki):
            print(
                f"tansu {komut}: {a.ad} {onceki}; önce taslak olmalı", file=sys.stderr
            )
            return 1
        okunan = (
            None
            if ayarla
            else ayar.oku(strateji, ayarlar, gerekli=onceki in durum.AYARLI)
        )
        anlik = son_anlik(a.kok)
        s = rapor.hazirla(
            strateji,
            sinama.gunler(anlik),
            kimlik=anlik.kimlik,
            kapi=sinama.veri_kapisi(anlik),
            sinanan=durum.sinanan(satirlar, a.ad),
            ayarla=ayarla,
            okunan=okunan,
        )
        yol = rapor.yaz(s, PROJE / rapor.RAPOR_KOKU)
        if ayarla:  # json rapordan sonra: yarıda kalan koşu onaysız parametre bırakmaz
            json_yolu = ayar.yaz(
                strateji, s.yuruyus.son, veri_kimligi=s.kimlik, kok=ayarlar
            )
        yeni_durum = durum.gec(a.ad, komut, puanli=s.yuruyus.son.puanli, yol=durum_csv)
    except veri.VeriHatasi as hata:
        print(f"tansu {komut}: {hata}{_yazilanlar(yol, json_yolu)}", file=sys.stderr)
        return 1
    except PermissionError as hata:
        hedef = hata.filename2 or hata.filename or hata
        print(
            f"tansu {komut}: {hedef} için erişim engellendi; dosya başka bir programda açıksa kapatıp yeniden çalıştır. durum.csv değişmedi.{_yazilanlar(yol, json_yolu)}",
            file=sys.stderr,
        )
        return 1
    for satir in rapor.konsol(s):
        print(satir)
    if json_yolu:
        print(f"ayar: {json_yolu}")
    print(f"rapor: {yol}; durum: {yeni_durum}")
    if durum.yeniden_onay(komut, onceki):
        print(f"Levent yeniden onaylamalı: tansu onayla {a.ad}")
    if a.ac:
        webbrowser.open(yol.resolve().as_uri())
    return 0


def _sina(a) -> int:
    return _kos(a, ayarla=False)


def _ayarla(a) -> int:
    return _kos(a, ayarla=True)


def _yedekle(a) -> int:
    """Ayarların gösterdiği ve en yeni görüntüyü `hedef`e kopyalar; geri yükleme rollerin yer değiştirmesidir."""
    try:
        _kok_var(a.kok)
        # Klasör açılmaz: takılmamış sürücü ya da yazım hatası başka yerde yedek bırakmasın.
        if not a.hedef.is_dir():
            raise veri.VeriHatasi(
                f"hedef klasör yok: {a.hedef}; sürücüyü tak ya da var olan bir klasör ver"
            )
        kimlikler = ayar.veri_kimlikleri(PROJE / ayar.AYAR_KOKU) | {_son_kimlik(a.kok)}
    except veri.VeriHatasi as hata:
        print(f"tansu yedekle: {hata}", file=sys.stderr)
        return 1
    rc = 0
    for kimlik in sorted(kimlikler):
        try:
            sonuc = veri.yedekle(kimlik, a.kok, a.hedef)
        except (veri.VeriHatasi, OSError) as hata:
            print(f"tansu yedekle: {kimlik}: {hata}", file=sys.stderr)
            rc = 1
        else:
            print(f"{kimlik}: {sonuc} ({a.hedef / 'ag' / kimlik})")
    return rc


def _henuz_yok(a) -> int:
    print(f"tansu {a.komut}: henüz yapılmadı (docs/SPEC.md bölüm 12).", file=sys.stderr)
    return 2


def ayristirici() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="tansu",
        description="Tansu stratejilerinin giriş, stop ve hedef seviyeleri. Alım-satım talimatı vermez.",
    )
    alt = ap.add_subparsers(dest="komut", required=True, metavar="komut")
    kok = veri_koku()

    p = alt.add_parser("veri", help="veriyi indir veya güncelle")
    p.add_argument("--kok", type=Path, default=kok, help=argparse.SUPPRESS)
    p.set_defaults(calistir=_veri)

    p = alt.add_parser("sina", help="stratejiyi geçmiş veride sına, rapor yaz")
    p.add_argument("ad")
    p.add_argument("--ac", action="store_true", help="raporu tarayıcıda aç")
    p.add_argument("--kok", type=Path, default=kok, help=argparse.SUPPRESS)
    p.set_defaults(calistir=_sina)

    p = alt.add_parser("ayarla", help="2021-2025 üzerinde parametre ayarla")
    p.add_argument("ad")
    p.add_argument("--kok", type=Path, default=kok, help=argparse.SUPPRESS)
    p.set_defaults(calistir=_ayarla, ac=False)

    p = alt.add_parser("onayla", help="stratejiyi akşam sinyaline al (yalnız Levent)")
    p.add_argument("ad")
    p.add_argument("--suzgec", action="append", default=[])
    p.add_argument("--liste-cikisi", action="store_true")
    p.set_defaults(calistir=_henuz_yok)

    p = alt.add_parser("tara", help="akşam taraması ve seviye listesi")
    p.add_argument("--oturum", help="YYYY-AA-GG")
    p.add_argument("--gonderme", action="store_true", help="Telegram'a gönderme")
    p.add_argument("--bekleme-yok", action="store_true", help="veri için bekleme")
    p.set_defaults(calistir=_henuz_yok)

    p = alt.add_parser("durum", help="stratejilerin sınıfı ve durumu")
    p.set_defaults(calistir=_henuz_yok)

    p = alt.add_parser(
        "yedekle",
        help="ayarların ve en yeni veri görüntüsünü hedef klasöre kopyala",
    )
    p.add_argument("hedef", type=Path, help="var olan klasör, örneğin yedek sürücü")
    p.add_argument("--kok", type=Path, default=kok, help=argparse.SUPPRESS)
    p.set_defaults(calistir=_yedekle)
    return ap


class _Yansi:
    """stderr'e yazılanı geçirir; kayıt için metni tutar."""

    def __init__(self, hedef):
        self.hedef, self.metin = hedef, ""

    def write(self, metin: str) -> int:
        self.metin += metin
        return self.hedef.write(metin)

    def __getattr__(self, ad):
        return getattr(self.hedef, ad)


def _kaydet(argv: list[str], a, rc: int | str, hata: str) -> None:
    """`kayit/tansu.log`a bir satır: zaman, argümanlar, rc, veri kökündeki en yeni görüntü, ilk hata satırı."""
    try:
        goruntu = _son_kimlik(getattr(a, "kok", None) or veri_koku())
    except veri.VeriHatasi, OSError:
        goruntu = "-"
    zaman = dt.datetime.now().isoformat(timespec="seconds")
    satir = f"{zaman} {' '.join(argv)} rc={rc} goruntu={goruntu} {hata}"
    try:
        (PROJE / "kayit").mkdir(exist_ok=True)
        with (PROJE / "kayit" / "tansu.log").open(
            "a", encoding="utf-8", newline="\n"
        ) as f:
            f.write(satir.replace("\n", " ").rstrip() + "\n")
    except OSError as hata:
        print(f"tansu: koşu kaydı yazılamadı: {hata}", file=sys.stderr)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    a = ayristirici().parse_args(argv)
    yansi = _Yansi(sys.stderr)
    try:
        with contextlib.redirect_stderr(yansi):
            rc = a.calistir(a)
    except BaseException as hata:
        _kaydet(argv, a, "istisna", f"{type(hata).__name__}: {hata}")
        raise
    # Hata satırı `tansu <komut>: ` ile başlar; önündeki uyarı satırları (ör. FutureWarning) kayda girmez.
    onek = f"tansu {a.komut}: "
    satirlar = yansi.metin.splitlines()
    hata = next(
        (s for s in satirlar if s.startswith(onek)), satirlar[0] if satirlar else ""
    )
    _kaydet(argv, a, rc, hata if rc else "")
    return rc


if __name__ == "__main__":
    sys.exit(main())
