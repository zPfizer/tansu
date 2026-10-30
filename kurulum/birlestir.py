"""`yeniden-kurulus` dalına tek birleştirme yolu: AGENTS.md birleştirme kuralını denetler, yöntemi kendisi seçer.

Kural (AGENTS.md, kalıcı onay Levent 30.10.2026): PR başındaki her denetim geçer ve o baş için son inceleme yorumu
olumludur: satır başında `İncelenen commit: <baş SHA>` ve `Sonuç: GEÇTİ` ya da `Sonuç: NOTLU GEÇTİ`. `main`'i getiren
PR `--merge` ile, öbürleri `--squash` ile birleşir; squash atalığı düşürür, merge commit dalın bütün commit'lerini açık
geçmişe taşır. `main`'e birleştirme Levent'indir.
`.claude/settings.json` çıplak `gh pr merge`'ü yasaklar; yöntemi bu dosya seçer.

Kullanım: python -X utf8 kurulum/birlestir.py <PR> [--repo sahip/ad]
Çıkış kodu: 0 birleşti, 1 engel var ya da gh hata verdi.
"""

import argparse
import json
import re
import subprocess
import sys

TABAN = "yeniden-kurulus"
GECEN = {"SUCCESS", "SKIPPED", "NEUTRAL"}
SONUC = re.compile(r"^Sonuç: (NOTLU GEÇTİ|GEÇTİ|GEÇMEDİ)(?!\w)", re.M)
BLOK = re.compile(r"^(?=İncelenen commit: )", re.M)


def kararlar(govde: str, sha: str) -> list[str]:
    """Yorumdaki `sha` kararları, sırayla. Blok `İncelenen commit: <sha>` satırıyla başlar, sonraki `İncelenen commit:`
    satırında biter; karar bloğun `Sonuç:` satırıdır. Başka yerdeki karar sözcüğü ve başka SHA'nın bloğu sayılmaz
    (PR 279 inceleme turları 1 ve 2). `Sonuç:` satırı okunamayan blok "okunamadı" verir: olumsuz karar yazım
    hatasıyla onaya dönmesin."""
    sonuc = []
    for blok in BLOK.split(govde):
        if re.match(rf"İncelenen commit: {sha}(?!\w)", blok):
            m = SONUC.search(blok)
            sonuc.append(m.group(1) if m else "okunamadı")
    return sonuc


def denetim_engelleri(denetimler: list[dict]) -> list[str]:
    """Bitmemiş koşu her zaman durdurur; bitmiş koşulardan her denetimin sonuncusu geçmelidir. Aynı başta yeniden
    koşan iş eskisinin yerini alır: PR gövdesi düzelince `pr-iddia` yeniden koşar (PR 279 inceleme turu 2)."""
    if not denetimler:
        return ["PR başında denetim yok"]
    bitmis = sorted(
        (d for d in denetimler if d.get("status", "COMPLETED") == "COMPLETED"),
        key=lambda d: d.get("startedAt") or "",
    )
    son = {
        (d.get("workflowName"), d.get("name") or d.get("context")): d for d in bitmis
    }
    sayilan = [d for d in denetimler if d not in bitmis] + list(son.values())
    return [
        f"denetim {d.get('name') or d.get('context')}: {durum or d.get('status')}"
        for d in sayilan
        if (durum := d.get("conclusion") or d.get("state")) not in GECEN
    ]


def engeller(pr: dict) -> list[str]:
    """Birleştirmeyi durduran nedenler; boş liste = kural sağlandı. `pr`: gh pr view JSON'u."""
    if pr["baseRefName"] != TABAN:
        return [f"taban {pr['baseRefName']}: kalıcı onay yalnız {TABAN} içindir"]
    sonuc = [] if pr["state"] == "OPEN" else [f"PR durumu {pr['state']}"]
    sonuc += denetim_engelleri(pr["statusCheckRollup"])
    sha = pr["headRefOid"]
    hepsi = [k for y in pr["comments"] for k in kararlar(y["body"], sha)]
    if not hepsi:
        sonuc.append(f"baş SHA {sha} için Sonuç satırlı inceleme yorumu yok")
    elif hepsi[-1] not in {"GEÇTİ", "NOTLU GEÇTİ"}:
        sonuc.append(f"baş SHA {sha} için son inceleme kararı {hepsi[-1]}")
    return sonuc


def _gh(*arglar):
    return subprocess.run(
        ["gh", *arglar], capture_output=True, check=True, encoding="utf-8"
    ).stdout


def main_getiriyor(depo: str, bas: str, taban: str) -> bool:
    """Baş, tabanda olmayan bir `main` commit'i taşıyor mu: başın `main` ile ortak atası tabanın atası değilse taşır.
    Uçları karşılaştırmak yetmez: eşitleme dalı açıldıktan sonra `main` ilerlerse baş da geride kalır (PR 277)."""
    ortak = _gh(
        "api", f"repos/{depo}/compare/{bas}...main", "--jq", ".merge_base_commit.sha"
    )
    durum = _gh(
        "api", f"repos/{depo}/compare/{taban}...{ortak.strip()}", "--jq", ".status"
    )
    return durum.strip() in {"ahead", "diverged"}


def main():
    ayrac = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ayrac.add_argument("pr")
    ayrac.add_argument("--repo", default="zPfizer/tansu")
    arg = ayrac.parse_args()
    alanlar = "state,baseRefName,headRefName,headRefOid,statusCheckRollup,comments"
    try:
        pr = json.loads(
            _gh("pr", "view", arg.pr, "--repo", arg.repo, "--json", alanlar)
        )
        sorunlar = engeller(pr)
        for satir in sorunlar:
            print(f"ENGEL: {satir}")
        if sorunlar:
            return 1
        getiriyor = main_getiriyor(arg.repo, pr["headRefOid"], pr["baseRefName"])
        secilen = "--merge" if getiriyor else "--squash"
        print(f"PR {arg.pr}: {pr['headRefName']} → {TABAN}, {secilen}")
        _gh(
            "pr",
            "merge",
            arg.pr,
            "--repo",
            arg.repo,
            secilen,
            "--match-head-commit",
            pr["headRefOid"],
        )
    except subprocess.CalledProcessError as hata:
        print(f"gh hata verdi: {hata.stderr.strip()}", file=sys.stderr)
        return 1
    print(f"PR {arg.pr} birleşti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
