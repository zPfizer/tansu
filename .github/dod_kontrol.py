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


def _cit(satir):
    m = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", satir)
    if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
        return m.group(1)
    return None


def _gorunur(satirlar):
    # GitHub'da görünen satırlar (CommonMark): kod çiti, HTML yorum bloğu ve
    # paragraf içi çok satırlı yorum gizlidir; kapanmayan çit ve blok sona kadar sürer.
    gorunur, cit, yorum_blogu, bekleyen = [], None, False, None
    for satir in satirlar:
        if cit:
            m = re.match(r" {0,3}(`+|~+)[ \t]*$", satir)
            if m and m.group(1)[0] == cit[0] and len(m.group(1)) >= len(cit):
                cit = None
            continue
        if yorum_blogu:
            yorum_blogu = "-->" not in satir
            continue
        kesen = not satir.strip() or _cit(satir) or re.match(r" {0,3}(#|<!--)", satir)
        if bekleyen is not None:
            if not kesen and "-->" not in satir:
                bekleyen.append(satir)
                continue
            if not kesen:
                bekleyen = None
                continue
            gorunur += bekleyen
            bekleyen = None
        if _cit(satir):
            cit = _cit(satir)
            continue
        if re.match(r" {0,3}<!--", satir):
            yorum_blogu = "-->" not in satir.split("<!--", 1)[1]
            continue
        gorunur.append(satir)
        kod_disi = re.sub(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", "", satir)
        if "<!--" in kod_disi and "-->" not in kod_disi.rsplit("<!--", 1)[1]:
            bekleyen = []
    return gorunur + (bekleyen or [])


def hatalar(govde: str) -> list[str]:
    if not govde or not govde.strip():
        return [
            "Kural 1: gövde boş; gerekli dört başlık yok.",
            "Kural 2: gövde boş; işaretsiz kutu kontrolü yapılamadı.",
            "Kural 3: ## Kabul ölçütleri bölümünde işaretli kutu yok.",
            "Kural 4: ## Definition of Done bölümünde 10 kanıtlı işaretli satır yok.",
            "Kural 5: ## Bağımsız inceleme bölümünde Denetçi: ve Sonuç: geçti ya da NOTLU GEÇTİ yok.",
            "Kural 6: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu yok.",
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
    akis = [satir for satir in _gorunur(satirlar) if satir.startswith("Akış:")]
    if len(akis) != 1 or not re.fullmatch(
        rf"Akış:[ \t]*(`({ad})`|({ad}))[ \t\r]*", akis[0]
    ):
        sonuc.append(
            "Kural 7: PR gövdesinde Akış: <ad> satırı olmalı; <ad> "
            + ", ".join(AKISLAR[:-1])
            + " ya da "
            + AKISLAR[-1]
            + " olmalı."
        )
    return sonuc


if __name__ == "__main__":
    sorunlar = hatalar(os.environ.get("PR_GOVDE", ""))
    for sorun in sorunlar:
        print(sorun)
    if sorunlar:
        sys.exit(1)
    print("Definition of Done listesi tam.")
    sys.exit(0)
