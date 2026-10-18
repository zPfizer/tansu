"""Check for a test change before a Python code edit in Claude Code.

Only PreToolUse Edit, Write, and MultiEdit events can block an edit.
Exit 2 blocks an edit. Exit 0 permits it without output.
An exception, including invalid JSON, ends with exit 1 and does not block.
If Git cannot judge the edit, permit it.
This check sees only Git changes. It cannot prove that a test ran red.
A test change on the branch counts for every code file.
"""

import json
import subprocess
import sys
from pathlib import Path

KOD_KLASORLERI = {"tansu", "kurulum", ".github"}


def _git(dizin, *arg):
    return subprocess.run(
        ["git", "-C", str(dizin), *arg],
        capture_output=True,
        encoding="utf-8",
        errors="surrogateescape",
        check=True,
    ).stdout.strip()


def _kod_deposu(dosya):
    if dosya.suffix != ".py" or not KOD_KLASORLERI.intersection(dosya.parts[:-1]):
        return None
    ust = dosya.parent
    while not ust.is_dir():
        ust = ust.parent
    kok = Path(_git(ust, "rev-parse", "--show-toplevel"))
    goreli = dosya.relative_to(kok)
    return kok if goreli.parts[0] in KOD_KLASORLERI else None


def _test_degisti(kok):
    if _git(kok, "status", "--porcelain", "--untracked-files=all", "--", "tests"):
        return True
    try:
        _git(kok, "rev-parse", "--verify", "origin/master")
    except subprocess.CalledProcessError:
        return False
    ortak = _git(kok, "merge-base", "HEAD", "origin/master")
    return bool(_git(kok, "diff", "--name-only", f"{ortak}..HEAD", "--", "tests"))


def main():
    girdi = json.load(sys.stdin)
    if girdi.get("hook_event_name") != "PreToolUse":
        return 0
    if girdi.get("tool_name") not in {"Edit", "Write", "MultiEdit"}:
        return 0
    dosya = Path(girdi["tool_input"]["file_path"])
    if not dosya.is_absolute():
        dosya = Path(girdi.get("cwd") or Path.cwd()) / dosya
    try:
        kok = _kod_deposu(dosya.resolve())
        if kok is None or _test_degisti(kok):
            return 0
    except OSError, subprocess.CalledProcessError:
        return 0
    print(
        'Write a red test under tests/ first, then edit the code (docs/agents/kod-kurallari.md "Test first").',
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
