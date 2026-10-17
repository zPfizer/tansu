"""Close script: close the work folder of a merged PR.

Usage: `python kurulum/kapanis.py <work folder>`. Run it after `gh pr merge <N> --merge`,
from the main checkout (not inside the work folder: Windows cannot remove it).
1. Remove the work folder (no `--force`).
2. Fast-forward `master` of the main checkout from `origin`.
3. Delete the local branch (`git branch -d`).
4. Print three proof lines. Exit 1 if one proof fails.
Every failed git call prints its stderr and stops with exit 1.
"""

import subprocess
import sys
from pathlib import Path


def dur(mesaj):
    print(mesaj, file=sys.stderr)
    sys.exit(1)


def git(klasor, *args):
    sonuc = subprocess.run(
        ["git", "-C", str(klasor), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if sonuc.returncode != 0:
        dur(f"kapanis: git {' '.join(args)} basarisiz:\n{sonuc.stderr.strip()}")
    return sonuc.stdout.strip()


def main(is_klasoru):
    is_ = Path(is_klasoru).resolve()
    # Windows cannot remove a folder that is the working directory of a process.
    if Path.cwd().resolve().is_relative_to(is_):
        dur("kapanis: betigi ana klasorden calistir; is klasorunun icinden olmaz")
    dal = git(is_, "branch", "--show-current")
    if not dal:
        dur("kapanis: is klasoru bir dal uzerinde degil")
    ana = Path(
        git(is_, "rev-parse", "--path-format=absolute", "--git-common-dir")
    ).parent
    # Check before any change: pull --ff-only would move the wrong branch.
    if git(ana, "branch", "--show-current") != "master":
        dur("kapanis: ana klasor master uzerinde degil")

    git(ana, "worktree", "remove", str(is_))
    git(ana, "pull", "--ff-only", "origin", "master")
    git(ana, "branch", "-d", dal)

    bas = git(ana, "rev-parse", "HEAD")
    if bas != git(ana, "rev-parse", "origin/master"):
        dur(f"kapanis: ana HEAD {bas} origin/master degil")
    print(f"kapanis: ana HEAD {bas} = origin/master")
    agaclar = git(ana, "worktree", "list", "--porcelain").splitlines()
    if is_.exists() or any(
        Path(satir.removeprefix("worktree ")).resolve() == is_
        for satir in agaclar
        if satir.startswith("worktree ")
    ):
        dur(f"kapanis: is klasoru duruyor: {is_}")
    print("kapanis: is klasoru yok")
    if git(ana, "ls-remote", "--heads", "origin", dal):
        dur(f"kapanis: uzak dal var: {dal}")
    print("kapanis: uzak dal yok")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        dur("kullanim: kapanis.py <is klasoru>")
    main(sys.argv[1])
