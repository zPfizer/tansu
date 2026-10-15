"""Atıf denetimi araçları (bilet 08): bölüm atıfları ve karar etiketleri var olan yere gider.

`tests/test_atif.py` ve `tests/test_sahipler.py` bu araçları kullanır. Ağa çıkmaz.
"""

import re
import subprocess
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

# Bu iki test dosyası bilerek kırık atıf örneği taşır; taramaya girmez.
HARIC = {"tests/test_atif.py", "tests/test_sahipler.py"}

ATIF = re.compile(r"(TASARIM|KURALLAR) §?(\d+(?:\.\d+)*)")
BASLIK = re.compile(r"#{2,4} (\d+(?:\.\d+)*)\.?\s")
# B-n ve C-n: sonuc-3-4.md kararı; S2-n: sorgu-2.md sorusu. "B-n" gibi şablonlar rakamsızdır, eşleşmez.
ETIKET = re.compile(r"(?<![\w-])(?:([BC])-(\d+)|(S2)-(\d+))(?![\w-])")
# İ: NN-NNN: sorgu-3 ve sorgu-4 sorusu; liste virgülle sürer, satır sonunda bölünebilir.
SORU_LISTESI = re.compile(r"İ:\s*((?:\d{2}-\d{3}\s*,?\s*)+)")


def izlenen_dosyalar(kok):
    """tansu/, tests/, docs/, AGENTS.md ve GLOSSARY.md altındaki git'e girmiş .py ve .md dosyaları."""
    cikti = subprocess.run(
        ["git", "-C", str(kok), "ls-files", "-z", "--"]
        + ["tansu", "tests", "docs", "AGENTS.md", "GLOSSARY.md"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout
    adlar = cikti.split("\0")
    return [kok / ad for ad in adlar if ad.endswith((".py", ".md")) and ad not in HARIC]


def bolum_numaralari(yol):
    """Belgenin numaralı başlıkları: '## 5. ...' -> '5', '### 5.1 ...' -> '5.1'.

    Numaralı alt başlığı olmayan bölümde (TASARIM 6, 7, 8) '6.2' o bölümün 2. maddesidir.
    """
    numaralar = set()
    maddeler = set()
    bolum = None
    for satir in yol.read_text(encoding="utf-8").splitlines():
        if eslesme := BASLIK.match(satir):
            numaralar.add(eslesme.group(1))
            if satir.startswith("## "):
                bolum = eslesme.group(1)
        elif bolum and (madde := re.match(r"(\d+)\. ", satir)):
            maddeler.add(f"{bolum}.{madde.group(1)}")
    alt_var = {numara.split(".")[0] for numara in numaralar if "." in numara}
    return numaralar | {m for m in maddeler if m.split(".")[0] not in alt_var}


def atif_kirikleri(kok, dosyalar):
    """`TASARIM <n>`, `TASARIM §<n>`, `KURALLAR §<n>` atıflarından başlığı olmayanlar: 'dosya:satır: atıf'."""
    var = {
        ad: bolum_numaralari(kok / "docs" / f"{ad}.md")
        for ad in ("TASARIM", "KURALLAR")
    }
    kirik = []
    for yol in dosyalar:
        metin = yol.read_text(encoding="utf-8")
        for eslesme in ATIF.finditer(metin):
            if eslesme.group(2) not in var[eslesme.group(1)]:
                satir = metin.count("\n", 0, eslesme.start()) + 1
                kirik.append(
                    f"{yol.relative_to(kok).as_posix()}:{satir}: {eslesme.group(0)}"
                )
    return kirik


def karar_tanimlari(sorgu):
    """docs/sorgu altında tanımlı etiketler: 'B-3', 'C-1', 'S2-7', 'İ:08-027'."""
    tanim = set()
    bolum = None
    for satir in (sorgu / "sonuc-3-4.md").read_text(encoding="utf-8").splitlines():
        baslik = re.match(r"## ([BC])\. ", satir)
        if baslik:
            bolum = baslik.group(1)
        elif satir.startswith("## "):
            bolum = None
        elif bolum and (madde := re.match(r"(\d+)\. ", satir)):
            tanim.add(f"{bolum}-{madde.group(1)}")
    for satir in (sorgu / "sorgu-2.md").read_text(encoding="utf-8").splitlines():
        if madde := re.match(r"(\d+)\. ", satir):
            tanim.add(f"S2-{madde.group(1)}")
    for yol in sorgu.glob("sorgu-[34]/sorular-*.md"):
        for satir in yol.read_text(encoding="utf-8").splitlines():
            if soru := re.match(r"\**(\d{2}-\d{3})(?!\d)", satir):
                tanim.add(f"İ:{soru.group(1)}")
    return tanim


def etiket_kirikleri(kok, dosyalar, sorgu):
    """İ:, B-, C-, S2- etiketlerinden tanımı olmayanlar: 'dosya:satır: etiket'."""
    tanim = karar_tanimlari(sorgu)
    kirik = []
    for yol in dosyalar:
        metin = yol.read_text(encoding="utf-8")
        bulunan = []
        for eslesme in ETIKET.finditer(metin):
            if eslesme.group(1):
                etiket = f"{eslesme.group(1)}-{eslesme.group(2)}"
            else:
                etiket = f"S2-{eslesme.group(4)}"
            bulunan.append((eslesme.start(), etiket))
        for eslesme in SORU_LISTESI.finditer(metin):
            for soru in re.finditer(r"\d{2}-\d{3}", eslesme.group(1)):
                bulunan.append((eslesme.start(1) + soru.start(), f"İ:{soru.group(0)}"))
        for yer, etiket in bulunan:
            if etiket not in tanim:
                satir = metin.count("\n", 0, yer) + 1
                kirik.append(f"{yol.relative_to(kok).as_posix()}:{satir}: {etiket}")
    return kirik


BEYIN = Path.home() / "Desktop" / "YONETIM" / "beyin"
HAVUZ = BEYIN / "kisisel" / "300-Projects" / "Tansu X Veri Havuzu"

# Taslak dosyalar AGENTS.md tablosunda "hiçbir olguya sahip değil, kayma denetimi dışında" der;
# havuz notlarına çalışma adlarıyla atıf verirler. Beyin kaynak yolu denetimine girmezler.
BEYIN_HARIC = ("docs/strateji-taslak", "docs/strateji-modulleri-taslak.md")

_NOT_ADI = re.compile(
    r"(gorsel-paket-\d[\w-]*|kaynak-[a-z0-9][\w-]*|tweet-[a-z0-9][\w-]*?)(\.md)?"
)
_ASSETS = re.compile(r"assets[/\\]([^/\\]+)(?:[/\\]([^/\\]+))?")


def sahip_tablosu(agents):
    """AGENTS.md 'Belgeler ve sahipleri' tablosunun ilk sütunu: (depo yolları, beyin yolları).

    'a.md … e.md' aralığı iki uç ve o klasördür.
    """
    depo, beyin = [], []
    icinde = False
    for satir in agents.read_text(encoding="utf-8").splitlines():
        if satir.startswith("## "):
            icinde = "Belgeler ve sahipleri" in satir
        if not (icinde and satir.startswith("| ")) or satir.startswith("| File"):
            continue
        hucre = satir.split("|")[1]
        yollar = re.findall(r"`([^`]+)`", hucre)
        if "…" in hucre:
            ilk, son = yollar
            klasor = ilk.rsplit("/", 1)[0]
            depo += [ilk, f"{klasor}/{son}", klasor]
            continue
        for yol in yollar:
            (beyin if "300-Projects" in yol else depo).append(yol)
    return depo, beyin


def yerel_mi(kok, yol):
    """Yol .gitignore'da mı (yerel dosya; CI'da bulunmaz)?"""
    return (
        subprocess.run(
            ["git", "-C", str(kok), "check-ignore", "-q", yol], capture_output=True
        ).returncode
        == 0
    )


def sahip_dosyalari(kok, yollar):
    """Tablodaki yollardan var olan .md dosyaları (klasörse içindekiler, 'a … e' aralığı dahil)."""
    dosyalar = []
    for yol in yollar:
        hedef = kok / yol
        if hedef.is_dir():
            dosyalar += sorted(hedef.rglob("*.md"))
        elif hedef.is_file():
            dosyalar.append(hedef)
    return list(dict.fromkeys(dosyalar))


def beyin_kirikleri(kok, dosyalar, havuz):
    """Havuz notu ve görsel yollarından havuzda olmayanlar: 'dosya:satır: belirteç'.

    Kısa ad (`gorsel-paket-45`) not adının başıdır. `...`, `<ad>`, `*`, `NN` içeren belirteç şablondur.
    """
    notlar = {yol.stem for yol in havuz.glob("*.md")}
    kirik = []
    for yol in dosyalar:
        goreli = yol.relative_to(kok).as_posix()
        if goreli.startswith(BEYIN_HARIC):
            continue
        metin = yol.read_text(encoding="utf-8")
        for eslesme in re.finditer(r"`([^`\n]+)`", metin):
            belirtec = eslesme.group(1).strip()
            if any(isaret in belirtec for isaret in ("...", "…", "<", "*", "NN")):
                continue
            var = None
            if ad := _NOT_ADI.fullmatch(belirtec):
                var = any(
                    n == ad.group(1) or n.startswith(ad.group(1) + "-") for n in notlar
                )
            elif varlik := _ASSETS.fullmatch(belirtec):
                klasor = havuz / "assets" / varlik.group(1)
                var = klasor.is_dir() and (
                    not varlik.group(2) or (klasor / varlik.group(2)).exists()
                )
            if var is False:
                satir = metin.count("\n", 0, eslesme.start()) + 1
                kirik.append(f"{goreli}:{satir}: {belirtec}")
    return kirik


def _havuz_metni(kok):
    """KURALLAR.md ve docs/kurallar/*.md; 'Kısa atıfların tam adları' bölümü hariç (o bölüm yalnız ad listesidir)."""
    parcalar = []
    for yol in [
        kok / "docs" / "KURALLAR.md",
        *sorted((kok / "docs" / "kurallar").glob("*.md")),
    ]:
        satirlar, atla = [], False
        for satir in yol.read_text(encoding="utf-8").splitlines():
            if satir.startswith("## "):
                atla = satir.startswith("## Kısa atıfların tam adları")
            if not atla:
                satirlar.append(satir)
        parcalar.append("\n".join(satirlar))
    return "\n".join(parcalar)


def kapsanmayan_notlar(kok, havuz):
    """Havuz notlarından belgede atıfı olmayanlar.

    Atıf: tam ad; ad başı (`kaynak-x`, `gorsel-paket-17-ad`); `T-x` (tweet-x'in başı); gorsel-paket
    numarası (`gorsel-paket-NN`, `gp-NN`, `G-NN`, `GNN`, listede `-NN`). 'Kural içermeyen notlar'
    listesi de tam addır. `-NN` biçimi gevşektir: `-60)` gibi eksi bir sayı da o numaralı notu sayar.
    """
    metin = _havuz_metni(kok)
    adlar = {
        m.group(1).rstrip("-")
        for m in re.finditer(r"(?<![\w-])((?:gorsel-paket|kaynak|tweet)-[\w-]*)", metin)
    }
    adlar |= {
        "tweet-" + m.group(1).rstrip("-")
        for m in re.finditer(r"(?<![\w-])T-([a-z0-9][\w-]*)", metin)
    }
    numaralar = {
        int(m.group(1))
        for m in re.finditer(r"(?<![\w-])(?:gp-|G-?|gorsel-paket-)(\d+)(?!\d)", metin)
    }
    numaralar |= {
        int(m.group(1))
        for m in re.finditer(r"(?<![\w.,/-])-(\d{2,3})(?![\d.,%/])", metin)
    }
    kapsanmayan = []
    for ad in sorted(yol.stem for yol in havuz.glob("*.md")):
        if re.search(rf"(?<![\w-]){re.escape(ad)}(?![\w-])", metin):
            continue
        if any(ad == on or ad.startswith(on + "-") for on in adlar):
            continue
        numara = re.match(r"gorsel-paket-(\d+)", ad)
        if numara and int(numara.group(1)) in numaralar:
            continue
        kapsanmayan.append(ad)
    return kapsanmayan
