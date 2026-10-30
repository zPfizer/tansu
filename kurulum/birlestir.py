"""`yeniden-kurulus` dalına tek birleştirme yolu: AGENTS.md birleştirme kuralını denetler, yöntemi kendisi seçer.

Kural (AGENTS.md, kalıcı onay Levent 30.10.2026): PR başındaki her denetim geçer, yorumlardan biri baş SHA'yı ve
GEÇTİ ya da NOTLU GEÇTİ kararını taşır. `main`'i getiren PR `--merge` ile, öbürleri `--squash` ile birleşir;
squash atalığı düşürür, merge commit dalın bütün commit'lerini açık geçmişe taşır. `main`'e birleştirme Levent'indir.
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
KARAR = re.compile(r"(?<!\w)(?:NOTLU )?GEÇTİ(?!\w)")


def yontem(main_basta: bool, main_tabanda: bool) -> str:
    """`main`'in ucu PR başında var, tabanda yoksa PR `main`'i getirir."""
    return "--merge" if main_basta and not main_tabanda else "--squash"


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
    if not any(sha in y["body"] and KARAR.search(y["body"]) for y in pr["comments"]):
        sonuc.append(f"baş SHA {sha} ve GEÇTİ kararı taşıyan inceleme yorumu yok")
    return sonuc


def _gh(*arglar):
    return subprocess.run(
        ["gh", *arglar], capture_output=True, check=True, encoding="utf-8"
    ).stdout


def _main_icinde(depo, ref):
    """`main`'in ucu `ref`'in atası mı (GitHub karşılaştırması: `main` geride ya da aynı)."""
    durum = _gh("api", f"repos/{depo}/compare/{ref}...main", "--jq", ".status")
    return durum.strip() in {"behind", "identical"}


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
        secilen = yontem(
            _main_icinde(arg.repo, pr["headRefOid"]),
            _main_icinde(arg.repo, pr["baseRefName"]),
        )
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
