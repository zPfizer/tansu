import os
import re
import sys


BASLIKLAR = (
    "## Kabul ölçütleri",
    "## Definition of Done",
    "## Bağımsız inceleme",
    "## Gerçek veri kanıtı",
)
AKISLAR = ("tansu-yeni-is", "tansu-hata", "tansu-belge", "tansu-karar", "tansu-eval")
BECERI_ORTAK = [
    "verification-before-completion",
    "mattpocock-skills:pr",
    "mattpocock-skills:code-review",
]
BECERI_BELGE = [
    "mattpocock-skills:writing-for-agents",
    "mattpocock-skills:domain-modeling",
    "asd-ste100",
]
KAPI_SATIRLARI = (
    (
        r"kapi: pytest(?: \(belge\))? -> 0",
        "kapi: pytest -> 0 ya da kapi: pytest (belge) -> 0",
    ),
    (r"kapi: ruff check -> 0", "kapi: ruff check -> 0"),
    (r"kapi: ruff format -> 0", "kapi: ruff format -> 0"),
    (r"kapi: git diff --check -> 0", "kapi: git diff --check -> 0"),
    (
        r"kapi: HEAD [0-9a-f]{40} temiz",
        "kapi: HEAD <40 küçük harfli onaltılı hane> temiz",
    ),
)
KAPI_ONEKLERI = (
    "kapi: pytest",
    "kapi: ruff check",
    "kapi: ruff format",
    "kapi: git diff --check",
    "kapi: HEAD",
)
KALDI = re.compile(r"(?<!\w)kald[ıiIİ](?!\w)", re.IGNORECASE)
SUPHE = re.compile(r"(?<!\w)(olabilir|belki|şüphe|emin\s+değ[iİ]l)", re.IGNORECASE)


def _bolum(satirlar, baslik):
    for sira, satir in enumerate(satirlar):
        if satir.startswith(baslik):
            son = next(
                (
                    yer
                    for yer in range(sira + 1, len(satirlar))
                    if satirlar[yer].startswith("## ")
                ),
                len(satirlar),
            )
            return list(enumerate(satirlar[sira + 1 : son], start=sira + 2))
    return None


def _dod_hatasi(bolum):
    isaretli = [
        (sira, satir) for sira, satir in bolum if re.match(r"^\s*- \[[xX]\]", satir)
    ]
    eksik = [
        str(sira) for sira, satir in isaretli if not re.search(r"kanıt:\s*\S", satir)
    ]
    sorunlar = []
    if len(isaretli) < 10:
        sorunlar.append("en az 10 işaretli satır olmalı")
    if eksik:
        sorunlar.append("kanıt eksik; satır: " + ", ".join(eksik))
    if not any(
        re.match(r"^\s*- \[[xX]\] Tansu:", satir) and re.search(r"kanıt:\s*\S", satir)
        for _, satir in isaretli
    ):
        sorunlar.append("Tansu: satırı işaretli ve kanıtlı olmalı")
    return "; ".join(sorunlar)


def _inceleme_hatasi(bolum):
    sorunlar = []
    if not any(re.fullmatch(r"Denetçi:[ \t]*\S.*", satir) for _, satir in bolum):
        sorunlar.append("Denetçi: alanı boş veya eksik")
    sonuclar = [satir for _, satir in bolum if re.match(r"\s*Sonuç:", satir)]
    if len(sonuclar) > 1:
        sorunlar.append(f"Sonuç: satırı tek olmalı ({len(sonuclar)} satır var)")
    elif not any(
        re.fullmatch(r"Sonuç:[ \t]*(geçti|GEÇTİ|NOTLU GEÇTİ)[ \t]*", satir)
        for satir in sonuclar
    ):
        sorunlar.append("Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik")
    return "; ".join(sorunlar)


def _kod_kaniti(bolum):
    metin = "\n".join(satir for _, satir in bolum)
    bloklar = re.finditer(
        r"^ {0,3}(`{3,}|~{3,})[^\n]*\n([\s\S]*?)^ {0,3}\1[ \t]*$",
        metin,
        re.MULTILINE,
    )
    return any(blok.group(2).strip() for blok in bloklar)


def _beceri_hatasi(govde, akis_ad):
    satirlar = re.findall(r"^Çağrılan beceriler:(.*)$", govde, re.MULTILINE)
    if len(satirlar) != 1:
        return f"PR gövdesinde Çağrılan beceriler: satırı tek olmalı ({len(satirlar)} satır var)."
    isimler = [ad.strip(" \t\r`") for ad in satirlar[0].split(",")]
    isimler = [ad for ad in isimler if ad]
    if not isimler:
        return "Çağrılan beceriler: listesi boş."
    gerekli = [akis_ad] if akis_ad else []
    if akis_ad in ("tansu-yeni-is", "tansu-hata", "tansu-belge"):
        gerekli += BECERI_ORTAK
    if akis_ad == "tansu-belge" and "toplu havuz okuma" not in isimler:
        gerekli += BECERI_BELGE
    eksik = [ad for ad in gerekli if ad not in isimler]
    if eksik:
        return "Çağrılan beceriler: listesinde eksik: " + ", ".join(eksik) + "."
    return ""


def _yorumsuz(metin):
    return re.sub(r"<!--.*?-->", "", metin, flags=re.DOTALL)


def _karar_hatasi(bolum):
    satirlar = _yorumsuz("\n".join(satir for _, satir in bolum)).splitlines()

    def alanlar(onek):
        return [
            satir.split(":", 1)[1].strip()
            for satir in satirlar
            if re.match(rf"\s*{onek}:", satir)
        ]

    sorunlar = []
    sonuclar = alanlar("Sonuç")
    sonuc = None
    if len(sonuclar) == 1 and re.fullmatch(r"geçti|GEÇTİ|NOTLU GEÇTİ", sonuclar[0]):
        sonuc = sonuclar[0].replace("geçti", "GEÇTİ")

    karar_onek = r"Denetçi kararı \(aynen\)"
    karar = alanlar(karar_onek)
    diger = "\n".join(
        satir for satir in satirlar if not re.match(rf"\s*(Sonuç|{karar_onek}):", satir)
    )
    if len(karar) != 1:
        sorunlar.append(
            f"Denetçi kararı (aynen): satırı tek olmalı ({len(karar)} satır var)"
        )
    elif not karar[0]:
        sorunlar.append("Denetçi kararı (aynen): metni boş")
    else:
        if KALDI.search(karar[0]):
            sorunlar.append("Denetçi kararı KALDI içeriyor")
        elif SUPHE.search(karar[0]):
            sorunlar.append(
                "Denetçi kararı şüphe sözcüğü içeriyor "
                "(olabilir, belki, şüphe, emin değil)"
            )
        sozcukler = list(
            dict.fromkeys(
                s.replace("geçti", "GEÇTİ")
                for s in re.findall(r"NOTLU GEÇTİ|GEÇTİ|geçti", karar[0])
            )
        )
        if not sozcukler:
            sorunlar.append("Denetçi kararında GEÇTİ ya da NOTLU GEÇTİ sözcüğü yok")
        elif sonuc and sozcukler != [sonuc]:
            sorunlar.append(
                f"Denetçi kararındaki sözcük ({', '.join(sozcukler)}) "
                f"Sonuç: değerinden ({sonuc}) farklı"
            )

    if KALDI.search(diger):
        sorunlar.append("Bağımsız inceleme bölümünde KALDI sözcüğü var")

    sayilar = alanlar("Yanlış iddia sayısı")
    if len(sayilar) != 1:
        sorunlar.append(
            f"Yanlış iddia sayısı: satırı tek olmalı ({len(sayilar)} satır var)"
        )
    elif not re.fullmatch(r"\d+", sayilar[0]):
        sorunlar.append("Yanlış iddia sayısı: değeri tam sayı olmalı")
    elif int(sayilar[0]) > 0:
        sorunlar.append("Yanlış iddia sayısı: yanlış iddia varken karar geçemez")

    ikinci = alanlar("İkinci geçiş")
    if len(ikinci) != 1:
        sorunlar.append(f"İkinci geçiş: satırı tek olmalı ({len(ikinci)} satır var)")
    elif ikinci[0] not in ("yok", "geçti"):
        sorunlar.append("İkinci geçiş: yok ya da geçti olmalı")
    return "; ".join(sorunlar)


def _kapi_hatasi(bolum, bas_sha, kod_var):
    satirlar = [satir.rstrip() for _, satir in bolum]
    eksik = [
        etiket
        for desen, etiket in KAPI_SATIRLARI
        if not any(re.fullmatch(desen, satir) for satir in satirlar)
    ]
    sorunlar = ["eksik satır: " + "; ".join(eksik)] if eksik else []
    if kod_var and "kapi: pytest (belge) -> 0" in satirlar:
        sorunlar.append("kod değişti; tam pytest gerekir")
    cok = [
        onek
        for onek in KAPI_ONEKLERI
        if sum(satir.startswith(onek) for satir in satirlar) > 1
    ]
    if cok:
        sorunlar.append("birden çok satır: " + "; ".join(cok))
    bulunan = [
        m.group(1)
        for satir in satirlar
        if (m := re.fullmatch(r"kapi: HEAD ([0-9a-f]{40}) temiz", satir))
    ]
    if bulunan and bas_sha and bas_sha not in bulunan:
        sorunlar.append(
            "kapi: HEAD değeri PR başından farklı; "
            f"beklenen: {bas_sha}, bulunan: {', '.join(bulunan)}"
        )
    return "; ".join(sorunlar)


def hatalar(govde: str, bas_sha: str | None = None, kod_var: bool = False) -> list[str]:
    if not govde or not govde.strip():
        return [
            "Kural 1: gövde boş; gerekli dört başlık yok.",
            "Kural 2: gövde boş; işaretsiz kutu kontrolü yapılamadı.",
            "Kural 3: ## Kabul ölçütleri bölümünde işaretli kutu yok.",
            "Kural 4: ## Definition of Done bölümünde 10 kanıtlı işaretli satır yok.",
            "Kural 5: ## Bağımsız inceleme bölümünde Denetçi: ve Sonuç: geçti ya da NOTLU GEÇTİ yok.",
            "Kural 6: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu yok.",
            "Kural 8: gövde boş; Çağrılan beceriler: satırı yok.",
            "Kural 9: gövde boş; ## Bağımsız inceleme bölümünde Denetçi kararı (aynen):, "
            "Yanlış iddia sayısı: ve İkinci geçiş: satırı yok.",
            "Kural 10: gövde boş; ## Gerçek veri kanıtı bölümünde kapi: satırları yok.",
        ]

    satirlar = govde.splitlines()
    bolumler = [_bolum(satirlar, baslik) for baslik in BASLIKLAR]
    sonuc = []
    eksik = [baslik for baslik, bolum in zip(BASLIKLAR, bolumler) if bolum is None]
    if eksik:
        sonuc.append("Kural 1: eksik başlıklar: " + ", ".join(eksik) + ".")
    isaretsiz = [
        str(sira)
        for sira, satir in enumerate(satirlar, start=1)
        if re.match(r"^\s*- \[ \]", satir)
    ]
    if isaretsiz:
        sonuc.append(
            "Kural 2: işaretsiz kutu var; satır: " + ", ".join(isaretsiz) + "."
        )

    kabul, dod, inceleme, kanit = bolumler
    if kabul is not None and not any(
        re.match(r"^\s*- \[[xX]\]", satir) for _, satir in kabul
    ):
        sonuc.append(
            "Kural 3: ## Kabul ölçütleri bölümünde en az bir işaretli kutu olmalı."
        )
    if dod is not None and (ayrinti := _dod_hatasi(dod)):
        sonuc.append("Kural 4: ## Definition of Done bölümünde " + ayrinti + ".")
    if inceleme is not None and (ayrinti := _inceleme_hatasi(inceleme)):
        sonuc.append("Kural 5: ## Bağımsız inceleme bölümünde " + ayrinti + ".")
    if kanit is not None and not _kod_kaniti(kanit):
        sonuc.append(
            "Kural 6: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu olmalı."
        )
    ad = "|".join(AKISLAR)
    akis = re.findall(r"^Akış:.*$", govde, re.MULTILINE)
    akis_ad = None
    if len(akis) == 1 and re.fullmatch(
        rf"Akış:[ \t]*(`({ad})`|({ad}))[ \t\r]*", akis[0]
    ):
        akis_ad = akis[0].split(":", 1)[1].strip(" \t\r`")
    if not akis_ad:
        sonuc.append(
            "Kural 7: PR gövdesinde Akış: <ad> satırı olmalı; <ad> "
            + ", ".join(AKISLAR[:-1])
            + " ya da "
            + AKISLAR[-1]
            + " olmalı."
        )
    if ayrinti := _beceri_hatasi(govde, akis_ad):
        sonuc.append("Kural 8: " + ayrinti)
    if inceleme is not None and (ayrinti := _karar_hatasi(inceleme)):
        sonuc.append("Kural 9: ## Bağımsız inceleme bölümünde " + ayrinti + ".")
    if kanit is not None and (ayrinti := _kapi_hatasi(kanit, bas_sha, kod_var)):
        sonuc.append("Kural 10: ## Gerçek veri kanıtı bölümünde " + ayrinti + ".")
    if "İNCELEME" in _yorumsuz(govde):
        sonuc.append("Kural 11: PR gövdesinde İNCELEME yer tutucusu kalmış.")
    return sonuc


if __name__ == "__main__":
    sorunlar = hatalar(
        os.environ.get("PR_GOVDE", ""),
        os.environ.get("PR_BAS_SHA") or None,
        os.environ.get("PR_KOD_VAR") == "1",
    )
    for sorun in sorunlar:
        print(sorun)
    if sorunlar:
        sys.exit(1)
    print("Definition of Done listesi tam.")
    sys.exit(0)
