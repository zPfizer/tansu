"""Atıf denetimi araçları (bilet 08): bölüm atıfları ve karar etiketleri var olan yere gider.

`tests/test_atif.py`, `test_sahipler.py`, `test_havuz.py` ve `test_sinirlar.py` bu araçları kullanır. Ağa çıkmaz.
"""

import re
import subprocess
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

# Bu dosyalar bilerek kırık atıf ve yol örneği taşır; taramaya girmez.
HARIC = {
    "tests/test_atif.py",
    "tests/test_sahipler.py",
    "tests/test_sinirlar.py",
    "tests/atif_araclari.py",
}

_NO = r"\d+(?:\.\d+)*"
# `TASARIM 5.1`, `TASARIM §5.1`, `docs/TASARIM.md` §5.1
ATIF = re.compile(rf"(TASARIM|KURALLAR)(?:\.md`?)? §?({_NO})")
# Atıf listesi ya da aralığı: `, §99`, ` ve §4`, `–5.6`, `/5.3`
MADDE = re.compile(
    r"\s+madde\s+(\d+)"
)  # `KURALLAR §3 madde 2` = 3.2 (bölümün 2. maddesi)
ATIF_DEVAMI = re.compile(rf"(\s*[–-]\s*|,\s*|\s+ve\s+|\s*/\s*)(§)?({_NO})")
# Düz sayıdan sonra boşluk ve sözcük gelirse sayı atıf değil nesnedir: `TASARIM 5.1 ve 6 gün`
SOZCUK_ARDINDAN = re.compile(r"\s+(?!ve\s+§?\d)[^\W\d_]")
# Atıfın hemen ardından gelen alıntı başlık ya da kalın terim: TASARIM 5.8 "Kural kaydı"
ALINTI = re.compile(
    r"""(?:,| ve|:)? ?\(?(?:"([^"\n]+)"|“([^”\n]+)”|‘([^’\n]+)’|\*\*([^*\n]+)\*\*)"""
)
BASLIK = re.compile(r"#{2,4} (\d+(?:\.\d+)*)\.?\s")
# B-n ve C-n: sonuc-3-4.md kararı; S2-n: sorgu-2.md sorusu. "B-n" gibi şablonlar rakamsızdır, eşleşmez.
ETIKET = re.compile(r"(?<![\w-])(?:([BC])-(\d+)|(S2)-(\d+))(?![\w-])")
# İ: NN-NNN: sorgu-3 ve sorgu-4 sorusu; liste virgülle sürer, satır sonunda bölünebilir.
SORU_LISTESI = re.compile(r"İ:\s*((?:\d{2}-\d{3}\s*,?\s*)+)")


DOSYA_KOKLERI = (
    "tansu",
    "tests",
    "docs",
    ".claude",
    ".github",
    "AGENTS.md",
    "CLAUDE.md",
    "GLOSSARY.md",
    "AKIS.md",
    "CODING_STANDARDS.md",
    "DEFINITION_OF_DONE.md",
)


def izlenen_dosyalar(kok):
    """tansu/, tests/, docs/, .claude/, .github/, AGENTS.md, CLAUDE.md, GLOSSARY.md, AKIS.md, CODING_STANDARDS.md, DEFINITION_OF_DONE.md altındaki git'e girmiş .py ve .md dosyaları.

    `.scratch/` bilerek dışarıdadır: biletler ve arşiv tarihsel metindir, atıfları o günün TASARIM'ına göredir.
    """
    cikti = subprocess.run(
        ["git", "-C", str(kok), "ls-files", "-z", "--"] + [*DOSYA_KOKLERI],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout
    adlar = cikti.split("\0")
    return [kok / ad for ad in adlar if ad.endswith((".py", ".md")) and ad not in HARIC]


def bolum_metinleri(yol):
    """Belgenin numaralı bölümleri ve metinleri: {'5': ..., '5.1': ...}.

    Bölüm metni başlık satırından aynı ya da üst düzeydeki sonraki başlığa kadardır; numarasız başlık
    (`## Ek A`) da bölümü bitirir. Kod bloklarındaki `#` satırları başlık sayılmaz.
    Numaralı alt başlığı olmayan bölümde (TASARIM 6, 7, 8) '6.2' o bölümün 2. maddesidir;
    madde metni sonraki maddeye ya da bölüm sonuna kadardır.
    """
    satirlar = yol.read_text(encoding="utf-8").splitlines()
    basliklar = []  # (satır sırası, düzey, numara ya da None)
    maddeler = []  # (satır sırası, bölüm numarası, madde no)
    bolum = None
    kodda = False
    for sira, satir in enumerate(satirlar):
        if satir.lstrip().startswith(("```", "~~~")):
            kodda = not kodda
        if kodda:
            continue
        if baslik := re.match(r"(#{1,6}) ", satir):
            numara = BASLIK.match(satir)
            basliklar.append((sira, len(baslik.group(1)), numara and numara.group(1)))
            if len(baslik.group(1)) == 2:
                bolum = numara and numara.group(1)
        elif bolum and (madde := re.match(r"(\d+)\. ", satir)):
            maddeler.append((sira, bolum, madde.group(1)))
    metinler = {}
    for yer, (sira, duzey, numara) in enumerate(basliklar):
        if numara:
            son = next(
                (s for s, d, _ in basliklar[yer + 1 :] if d <= duzey), len(satirlar)
            )
            metinler[numara] = "\n".join(satirlar[sira:son])
    alt_var = {numara.split(".")[0] for numara in metinler if "." in numara}
    for yer, (sira, bolum, madde) in enumerate(maddeler):
        if bolum in alt_var:
            continue
        sonraki = maddeler[yer + 1][0] if yer + 1 < len(maddeler) else len(satirlar)
        ust_son = next(
            (s for s, d, _ in basliklar if s > sira and d <= 2), len(satirlar)
        )
        metinler[f"{bolum}.{madde}"] = "\n".join(satirlar[sira : min(sonraki, ust_son)])
    return metinler


def bolum_numaralari(yol):
    """Belgenin numaralı başlıkları ve alt başlıksız bölümlerin maddeleri."""
    return set(bolum_metinleri(yol))


def _duz(metin):
    # Türkçe büyük/küçük harf: İ, I, ı hepsi i olur; satır sonları ve girintiler tek boşluk olur.
    for harf in "İIı":
        metin = metin.replace(harf, "i")
    return " ".join(metin.split()).casefold()


def atif_numaralari(metin):
    """Metindeki bölüm atıfları: (belge, numara, başlangıç, ilk numaranın bitişi, liste var mı).

    `TASARIM §5.1, §99`, `TASARIM 5.5, 5.6`, `KURALLAR §3 ve §4` ve `TASARIM §5.5–5.6` her numarayı verir.
    Aralıkta iki uç da denetlenir. Listede virgülle gelen numara `§` taşımalı ya da noktalı olmalıdır
    (`TASARIM 5.1, 6 gün` bir atıf listesi değildir). ` ve ` ve `/` ardından düz sayı da okunur
    (`TASARIM 5 ve 99`, `TASARIM 5/99`), ama sayıdan sonra boşluk ve sözcük gelirse okunmaz
    (`TASARIM 5.1 ve 6 gün`). `TASARIM.md §5` dosya biçimi de bir atıftır.
    """
    for eslesme in ATIF.finditer(metin):
        belge = eslesme.group(1)
        sonuc = [(belge, eslesme.group(2), eslesme.start(), eslesme.end(), False)]
        konum = eslesme.end()
        if madde := MADDE.match(metin, konum):
            numara = f"{eslesme.group(2)}.{madde.group(1)}"
            sonuc.append((belge, numara, eslesme.start(), madde.end(), True))
        while devam := ATIF_DEVAMI.match(metin, konum):
            ayrac, isaret, numara = devam.groups()
            aralik = (
                ayrac.strip() == "–"
            )  # `§2–3`; tireyle (`5.2 - 3 gün`) yalnız noktalı numara sayılır
            duz_ve_ya_bolu = ayrac.strip() in ("ve", "/") and not SOZCUK_ARDINDAN.match(
                metin, devam.end()
            )
            if not (isaret or "." in numara or aralik or duz_ve_ya_bolu):
                break
            sonuc.append((belge, numara, eslesme.start(), devam.end(), True))
            konum = devam.end()
        yield from sonuc


def atif_kirikleri(kok, dosyalar):
    """Bölüm atıflarından sorunlu olanlar: 'dosya:satır: atıf'.

    Sorun: başlık yok (`TASARIM 9`, listedeki ya da aralıktaki her numara dahil) ya da atıfın ardındaki
    alıntı terim (`TASARIM 5.8 "Kural kaydı"`) atıf yapılan bölümün metninde geçmiyor.
    """
    var = {
        ad: bolum_metinleri(kok / "docs" / f"{ad}.md") for ad in ("TASARIM", "KURALLAR")
    }
    kirik = []
    for yol in dosyalar:
        if yol.relative_to(kok).as_posix().startswith(TASLAKLAR):
            continue  # taslaklar kayma denetimi dışında (AGENTS.md "Belgeler ve sahipleri")
        metin = yol.read_text(encoding="utf-8")
        for belge, numara, basla, bitis, listede in atif_numaralari(metin):
            bolumler = var[belge]
            satir = metin.count("\n", 0, basla) + 1
            yer = f"{yol.relative_to(kok).as_posix()}:{satir}: "
            if listede:
                if numara not in bolumler:
                    kirik.append(f"{yer}{belge} §{numara}")
                continue
            yer += metin[basla:bitis]
            if numara not in bolumler:
                kirik.append(yer)
            elif alinti := ALINTI.match(metin, bitis):
                terim = next(parca for parca in alinti.groups() if parca)
                if _duz(terim.rstrip(".…")) not in _duz(bolumler[numara]):
                    kirik.append(f'{yer} "{terim}" bölümde yok')
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

# AGENTS.md "Belgeler ve sahipleri": taslaklar hiçbir olguya sahip değildir ve kayma denetimi dışındadır
# (04c, 14.10). Bu yüzden atıf, yol, bağlantı ve beyin yolu denetimlerine girmezler.
TASLAKLAR = ("docs/strateji-taslak", "docs/strateji-modulleri-taslak.md")

_NOT_ADI = re.compile(
    r"(gorsel-paket-\d[\w-]*|kaynak-[a-z0-9][\w-]*|tweet-[a-z0-9][\w-]*?)(\.md)?"
)
_ASSETS = re.compile(r"assets[/\\]([^/\\]+)(?:[/\\]([^/\\]+))?")


def sahip_tablosu(agents):
    """AGENTS.md 'Belgeler ve sahipleri' tablosunun ilk sütunu: (depo yolları, beyin yolları).

    'A-x.md … E-y.md' aralığı iki uç, aradaki her harfin dosyası (`<H>-*.md`, depo kökü AGENTS.md'nin klasörü;
    eşleşen hepsi, yoksa `<H>-*.md` yolu: yok diye raporlanır) ve o klasördür.
    """
    kok = agents.parent
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
            ara = []
            for kod in range(ord(ilk.rsplit("/", 1)[1][0]) + 1, ord(son[0])):
                desen = f"{chr(kod)}-*.md"
                bulunan = sorted((kok / klasor).glob(desen))
                ara += [f"{klasor}/{d.name}" for d in bulunan] or [f"{klasor}/{desen}"]
            depo += [ilk, f"{klasor}/{son}", *ara, klasor]
            continue
        for yol in yollar:
            (beyin if "300-Projects" in yol else depo).append(yol)
    return depo, beyin


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

    Kısa ad (`gorsel-paket-45`) not adının başıdır (tire sınırında). `...`, `…`, `<`, `*`, `NN` içeren belirteç şablondur.
    """
    notlar = {yol.stem for yol in havuz.glob("*.md")}
    kirik = []
    for yol in dosyalar:
        goreli = yol.relative_to(kok).as_posix()
        if goreli.startswith(TASLAKLAR):
            continue
        metin = yol.read_text(encoding="utf-8")
        for eslesme in re.finditer(r"`([^`\n]+)`", metin):
            belirtec = re.split(r"[:\s#]", eslesme.group(1).strip())[
                0
            ]  # açıklama, :satır yol değil
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
    """Havuz atıflarının sayıldığı metin: docs/kurallar/A-…E-*.md'nin tamamı ve docs/KURALLAR.md'nin yalnız
    'Kural içermeyen notlar' bölümü (başlıktan sonraki aynı düzey `## ` başlığa kadar).

    KURALLAR.md'nin öbür bölümleri (Dizin, Seçim, 'Kısa atıfların tam adları', ...) ve başka dosyalar sayılmaz.
    """
    parcalar = [
        yol.read_text(encoding="utf-8")
        for yol in sorted((kok / "docs" / "kurallar").glob("*.md"))
        if re.fullmatch(
            r"[A-E]-.*\.md", yol.name
        )  # glob Windows'ta büyük/küçük harfi ayırmaz
    ]
    liste, icinde = [], False
    for satir in (
        (kok / "docs" / "KURALLAR.md").read_text(encoding="utf-8").splitlines()
    ):
        if satir.startswith("## "):
            icinde = satir.startswith("## Kural içermeyen notlar")
        if icinde:
            liste.append(satir)
    parcalar.append("\n".join(liste))
    return "\n".join(parcalar)


def havuz_sorunlari(kok, havuz):
    """Havuz notlarından belgede atıfı olmayanlar ve belirsiz kısa atıflar.

    Her kısa atıf tek bir nota çözülmelidir: tam ad; ad başı (`kaynak-x`, `gorsel-paket-17-ad`); `T-x`
    (tweet-x'in başı); gorsel-paket numarası (`gorsel-paket-NN`, `gp-NN`, `G-NN`, `GNN`, listede `-NN`).
    Birden çok nota çözülen atıf 'belirsiz atıf ...' hatasıdır (tam adı dururken kısa ad aynı kalır);
    hiçbirine çözülmeyen kısa atıf yok sayılır (beyin yolu denetimi onu ayrıca yakalar).
    'Kural içermeyen notlar' listesi tam addır. `-NN` biçimi gevşektir: `-60)` gibi eksi bir sayı da
    o numaralı notu sayar.
    """
    metin = _havuz_metni(kok)
    notlar = sorted(yol.stem for yol in havuz.glob("*.md"))
    kapsanan, sorunlar = set(), []

    def coz(belirtec, adaylar):
        if len(adaylar) == 1:
            kapsanan.add(adaylar[0])
        elif adaylar:
            sorunlar.append(f"belirsiz atıf {belirtec}: {', '.join(adaylar)}")

    kapsanan |= {
        ad for ad in notlar if re.search(rf"(?<![\w-]){re.escape(ad)}(?![\w-])", metin)
    }
    # Tam adlar kısa atıf olarak yeniden okunmaz (`gorsel-paket-01-ad` içindeki `01` bir numara atfı değildir).
    for ad in kapsanan:
        metin = re.sub(rf"(?<![\w-]){re.escape(ad)}(?![\w-])", " ", metin)
    onekler = {
        m.group(1).rstrip("-")
        for m in re.finditer(
            r"(?<![\w-])((?:gorsel-paket|kaynak|tweet)-\w[\w-]*)", metin
        )
    }
    onekler |= {
        "tweet-" + m.group(1).rstrip("-")
        for m in re.finditer(r"(?<![\w-])T-([a-z0-9][\w-]*)", metin)
    }
    for onek in sorted(onekler):
        coz(
            onek,
            [n for n in notlar if n == onek]
            or [n for n in notlar if n.startswith(onek + "-")],
        )
    numaralar = {
        int(m.group(1))
        for m in re.finditer(r"(?<![\w-])(?:gp-|G-?|gorsel-paket-)(\d+)(?!\d)", metin)
    }
    numaralar |= {
        int(m.group(1))
        for m in re.finditer(r"(?<![\w.,/-])-(\d{2,3})(?![\d.,%/])", metin)
    }
    for numara in sorted(numaralar):
        coz(
            f"gorsel-paket-{numara}",
            [n for n in notlar if re.match(rf"gorsel-paket-0*{numara}(-|$)", n)],
        )
    return sorunlar + [n for n in notlar if n not in kapsanan]


# Depo yolu sayılan klasör kökleri. veri/, rapor/, gunluk/ (.gitignore'da) her koşuda oluşan çalışma
# çıktısı klasörleridir; belgeler henüz olmayan çıktı dosyalarını anar, bu yüzden taranmaz.
KOKLER = (
    "tansu",
    "tests",
    "docs",
    ".github",
    "kurulum",
    "kayit",
    ".claude",
    ".scratch",
    "arsiv",
)
# Şablon ya da aralık işareti taşıyan yol yol değildir: `rapor-<koşu>.html`, `tansu/*.py`, `A–E`.
# Yalnız ayrıştırılmış yola bakılır; sondaki açıklama (`yol (NN numaralı bölüm)`) şablon sayılmaz.
SABLON = ("<", "*", "…", "YYYY", "–", "NN")
# Kök dizin dosyaları ve docs/ belgeleri bare adla anılır (`GLOSSARY.md`, `TASARIM.md`, `pyproject.toml`).
KOK_DOSYASI = re.compile(r"[A-Z][A-Z_-]*\.md|pyproject\.toml|requirements\.lock\.txt")
# Yol gibi görünen ama depo dosyası olmayan adlar. Her istisna tek bir dosyaya ve o dosyadaki tek bir
# anışa bağlıdır: ad ancak o dosyada, belirtilen metnin hemen ardından gelirse atlanır (ad: (dosya, öncesi)).
ISTISNA_ADLARI = {
    # reddedilen fikir (docs/sorgu/izleme/karar.md 20-031)
    "TODO.md": ("docs/sorgu/izleme/karar.md", "yerine "),
    # domain.md bu dosyanın olmadığını söyler
    "GLOSSARY-MAP.md": ("docs/agents/domain.md", "no "),
}
# Markdown bağlantı hedefi: [metin](hedef "başlık") ve [kimlik]: hedef
BAGLANTI = re.compile(r"\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
BAGLANTI_TANIMI = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*<?(\S+?)>?\s*$", re.MULTILINE)
DIS_BAGLANTI = re.compile(r"(?:[a-z][a-z0-9+.-]*:|#|//)", re.IGNORECASE)


def yerel_koklar(kok):
    """.gitignore'daki sabitlenmiş (başı '/') yol girişleri; yerelde var olan, CI'da olmayan dosyalar."""
    koklar = []
    for satir in (kok / ".gitignore").read_text(encoding="utf-8").splitlines():
        if satir.startswith("/") and "*" not in satir:
            koklar.append(satir.strip("/"))
    return sorted(koklar, key=len)


def yerel_kok_adi(kok, yol):
    """Yol .gitignore'daki yerel bir kökün altındaysa o kökün yolu, değilse None."""
    yol = yol.strip("/")
    for giris in yerel_koklar(kok):
        if yol == giris or yol.startswith(giris + "/"):
            return giris
    return None


def yerel_kok_yok(kok, yol):
    """Yol .gitignore'daki yerel bir kökün altındaysa ve o kök bu makinede yoksa True (CI'da atlanır).

    Kök varsa False döner: dosya eksikse yazım hatasıdır, atlanmaz.
    """
    giris = yerel_kok_adi(kok, yol)
    return giris is not None and not (kok / giris).exists()


def _istisna_mi(goreli, metin, baslangic, ad):
    """Ad, ISTISNA_ADLARI'nda bu dosya ve bu anış için tanımlı mı? (anış: backtick'in hemen öncesindeki metin)."""
    if ad not in ISTISNA_ADLARI:
        return False
    dosya, oncesi = ISTISNA_ADLARI[ad]
    return goreli == dosya and metin[:baslangic].endswith(oncesi)


def yol_kirikleri(kok, dosyalar):
    """Dosyalardaki depo yolları, kök dosya adları ve Markdown bağlantı hedefleri.

    Backtick içinde `tansu/...`, `tests/...`, `docs/...`, `.github/...` gibi yollar ve kök dosya adları
    denetlenir; `\\` ayracı `/` sayılır (`docs\\X.md`). `:satır`, `::test`, `#bölüm` eki ile ardındaki
    açıklama yol sayılmaz. Markdown bağlantı hedefi, bağlantıyı taşıyan dosyaya göre çözülür
    (`http(s):`, `mailto:`, `#bağlantı` atlanır, `#parça` ve `?sorgu` atılır).
    Var olmayan hedef 'dosya:satır: yol' olarak döner. Yerel kökün (docs/sorgu, docs/strateji-taslak)
    kendisi yoksa yol atlanır; kök varsa eksik dosya hatadır.
    """
    kirik = []

    def kontrol(goreli, metin, konum, var, ad):
        if var or yerel_kok_yok(kok, ad):
            return
        satir = metin.count("\n", 0, konum) + 1
        kirik.append(f"{goreli}:{satir}: {ad}")

    for yol in dosyalar:
        goreli = yol.relative_to(kok).as_posix()
        if goreli.startswith(TASLAKLAR):
            continue  # taslaklar kayma denetimi dışında (AGENTS.md "Belgeler ve sahipleri")
        metin = yol.read_text(encoding="utf-8")
        for eslesme in re.finditer(r"`([^`\n]+)`", metin):
            belirtec = eslesme.group(1).strip().replace("\\", "/")
            ad = re.split(r"[:\s#]", belirtec)[0]
            if any(isaret in ad for isaret in SABLON):
                continue
            if "/" in ad:
                if ad.split("/")[0] not in KOKLER:
                    continue
                adaylar = [ad]
            elif KOK_DOSYASI.fullmatch(ad) and not _istisna_mi(
                goreli, metin, eslesme.start(), ad
            ):
                adaylar = [ad, f"docs/{ad}"]
            else:
                continue
            var = any((kok / aday).exists() for aday in adaylar)
            kontrol(goreli, metin, eslesme.start(), var, ad)
        for eslesme in [*BAGLANTI.finditer(metin), *BAGLANTI_TANIMI.finditer(metin)]:
            hedef = eslesme.group(1).replace("\\", "/")
            if DIS_BAGLANTI.match(hedef):
                continue
            hedef = re.split(r"[#?]", hedef)[0]
            if not hedef:
                continue
            cozulmus = (yol.parent / hedef).resolve()
            try:
                goreli_hedef = cozulmus.relative_to(kok.resolve()).as_posix()
            except ValueError:
                goreli_hedef = hedef  # depo dışına çıkan hedef de var olmalı
            kontrol(goreli, metin, eslesme.start(), cozulmus.exists(), goreli_hedef)
    return kirik
