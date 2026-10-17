import os
import re
import subprocess
import sys


# Beş kural (Levent 17.10: "Sadeleştir."). Testi, biçimi ve lint'i ci iş akışı kanıtlar.
KURAL_1 = "Kural 1: PR gövdesinde Closes #<issue> satırı olmalı."
KURAL_2 = "Kural 2: ## Kabul ölçütleri bölümünde en az bir kutu olmalı ve her kutu işaretli olmalı."
KURAL_3 = "Kural 3: ## Gerçek veri kanıtı bölümünde içi dolu bir kod bloğu olmalı."
KAPATMA = re.compile(
    r" *(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved) #[0-9]+\s*",
    re.IGNORECASE,
)


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
            return satirlar[sira + 1 : son]
    return None


def _yorumsuz(metin):
    return re.sub(r"<!--.*?-->", "", metin, flags=re.DOTALL)


def _kabul_hatasi(bolum):
    if bolum is None:
        return True
    kutular = [satir for satir in bolum if re.match(r"^\s*- \[[ xX]\]", satir)]
    return not kutular or any(re.match(r"^\s*- \[ \]", satir) for satir in kutular)


def _kod_kaniti(bolum):
    bloklar = re.finditer(
        r"^ {0,3}(`{3,}|~{3,})[^\n]*\n([\s\S]*?)^ {0,3}\1[ \t]*$",
        "\n".join(bolum),
        re.MULTILINE,
    )
    return any(blok.group(2).strip() for blok in bloklar)


def _inceleme_hatasi(bolum):
    if bolum is None:
        return "bölüm yok"
    sorunlar = []
    if not any(re.fullmatch(r"Denetçi:[ \t]*\S.*", satir) for satir in bolum):
        sorunlar.append("Denetçi: alanı boş veya eksik")
    sonuclar = [satir for satir in bolum if re.match(r"\s*Sonuç:", satir)]
    if len(sonuclar) > 1:
        sorunlar.append(f"Sonuç: satırı tek olmalı ({len(sonuclar)} satır var)")
    elif not any(
        re.fullmatch(r"Sonuç:[ \t]*(geçti|GEÇTİ|NOTLU GEÇTİ)[ \t]*", satir)
        for satir in sonuclar
    ):
        sorunlar.append("Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik")
    return "; ".join(sorunlar)


def _temiz_birlesme(denetlenen, bas_sha, taban, dizin):
    def git(*arg):
        return subprocess.run(
            ["git", "--no-replace-objects", *arg],
            cwd=dizin,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="surrogateescape",
            check=True,
        ).stdout

    def dosyalar(x, y):
        cikti = git("diff-tree", "-r", "-z", "--name-only", "--no-renames", x, y)
        return set(cikti.split("\0")) - {""}

    # Denetim ağaçları karşılaştırır, birleştirmez; iki tarafın da değiştirdiği dosya yeni geçiş ister.
    try:
        git("merge-base", "--is-ancestor", denetlenen, bas_sha)
        for satir in git(
            "rev-list", "--first-parent", "--parents", f"{denetlenen}..{bas_sha}"
        ).splitlines():
            sha, *ebeveynler = satir.split()
            if len(ebeveynler) != 2:
                return False
            birinci, ikinci = ebeveynler
            git("merge-base", "--is-ancestor", ikinci, taban)
            taban_ortak = git("merge-base", "--all", birinci, ikinci).split()
            if len(taban_ortak) != 1:
                return False
            getirilen = dosyalar(taban_ortak[0], ikinci)
            dal = dosyalar(taban_ortak[0], birinci)
            if (
                getirilen & dal
                or not dosyalar(birinci, sha) <= getirilen
                or not dosyalar(ikinci, sha) <= dal
            ):
                return False
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False
    return True


def _denetlenen_hatasi(govde, bas_sha, taban, dizin):
    satirlar = re.findall(r"^Denetlenen commit:(.*)$", govde, re.MULTILINE)
    if len(satirlar) != 1:
        return (
            "Kural 5: PR gövdesinde Denetlenen commit: <40 küçük harfli onaltılı hane> "
            f"satırı tek olmalı ({len(satirlar)} satır var)."
        )
    sha = satirlar[0].strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        return (
            "Kural 5: Denetlenen commit: değeri 40 küçük harfli onaltılı hane olmalı."
        )
    if bas_sha is None or sha == bas_sha:
        return ""
    if taban is None:
        return "Kural 5: Denetlenen commit PR başı değil ve taban dal bilinmiyor."
    if _temiz_birlesme(sha, bas_sha, taban, dizin):
        return ""
    return (
        f"Kural 5: Denetlenen commit ({sha}) PR başı ({bas_sha}) değil; "
        "sonraki commit'ler temiz bir taban birleştirmesi değil."
    )


def hatalar(
    govde: str | None,
    bas_sha: str | None = None,
    taban: str | None = None,
    dizin=None,
) -> list[str]:
    govde = _yorumsuz(govde or "")
    satirlar = govde.splitlines()
    sonuc = []
    if not any(KAPATMA.fullmatch(satir) for satir in satirlar):
        sonuc.append(KURAL_1)
    if _kabul_hatasi(_bolum(satirlar, "## Kabul ölçütleri")):
        sonuc.append(KURAL_2)
    kanit = _bolum(satirlar, "## Gerçek veri kanıtı")
    if kanit is None or not _kod_kaniti(kanit):
        sonuc.append(KURAL_3)
    if ayrinti := _inceleme_hatasi(_bolum(satirlar, "## Bağımsız inceleme")):
        sonuc.append("Kural 4: ## Bağımsız inceleme: " + ayrinti + ".")
    if ayrinti := _denetlenen_hatasi(govde, bas_sha, taban, dizin):
        sonuc.append(ayrinti)
    return sonuc


if __name__ == "__main__":
    sorunlar = hatalar(
        os.environ.get("PR_GOVDE", ""),
        os.environ.get("PR_BAS_SHA") or None,
        "origin/" + os.environ["GITHUB_BASE_REF"]
        if os.environ.get("GITHUB_BASE_REF")
        else None,
    )
    for sorun in sorunlar:
        print(sorun)
    if sorunlar:
        sys.exit(1)
    print("Definition of Done listesi tam.")
    sys.exit(0)
