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


def karar(govde: str, sha: str) -> str | None:
    """Yorum `sha` için inceleme kararı mı: satır başında `İncelenen commit: <sha>` ve `Sonuç: <karar>`.
    Yorumun başka yerindeki karar sözcüğü sayılmaz ("pytest GEÇTİ" maddesi olumsuz yorumu onaya çevirmesin)."""
    if not re.search(rf"^İncelenen commit: {sha}(?!\w)", govde, re.M):
        return None
    m = SONUC.search(govde)
    return m and m.group(1)


def engeller(pr: dict) -> list[str]:
    """Birleştirmeyi durduran nedenler; boş liste = kural sağlandı. `pr`: gh pr view JSON'u."""
    if pr["baseRefName"] != TABAN:
        return [f"taban {pr['baseRefName']}: kalıcı onay yalnız {TABAN} içindir"]
    sonuc = [] if pr["state"] == "OPEN" else [f"PR durumu {pr['state']}"]
    denetimler = pr["statusCheckRollup"]
    if not denetimler:
        sonuc.append("PR başında denetim yok")
    for d in denetimler:
        ad = d.get("name") or d.get("context")
        durum = d.get("conclusion") or d.get("state")
        if durum not in GECEN:
            sonuc.append(f"denetim {ad}: {durum or d.get('status')}")
    sha = pr["headRefOid"]
    kararlar = [k for y in pr["comments"] if (k := karar(y["body"], sha))]
    if not kararlar:
        sonuc.append(f"baş SHA {sha} için Sonuç satırlı inceleme yorumu yok")
    elif kararlar[-1] == "GEÇMEDİ":
        sonuc.append(f"baş SHA {sha} için son inceleme kararı GEÇMEDİ")
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
