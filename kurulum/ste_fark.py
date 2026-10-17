"""STE linter on the added lines of the instruction files: python ste_fark.py <base> [linter].

The exit code is the exit code of the linter.
"""

import subprocess
import sys
from pathlib import Path

YONERGE_YOLLARI = [
    "AGENTS.md",
    "CLAUDE.md",
    "CODING_STANDARDS.md",
    "DEFINITION_OF_DONE.md",
    ".github/pull_request_template.md",
    "docs/agents",
    ".claude/agents",
    ".claude/skills",
]


def ste_fark(taban, linter=None):
    """STE linter'ı yalnız yönerge dosyalarına eklenen satırlarla çalıştırır; çıkış kodu linter'ınkidir.

    Fark, taban ile HEAD'in ortak atasına göre alınır: taban dal noktasından sonra ilerlediyse onun satırları dalın eklemesi sayılmaz.
    """
    kok = subprocess.run(
        ["git", "merge-base", taban, "HEAD"],
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout.strip()
    fark = subprocess.run(
        ["git", "diff", "-U0", "--no-color", kok, "--", *YONERGE_YOLLARI],
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout
    eklenen = []
    parca_icinde = False
    for s in fark.splitlines():
        if s.startswith("diff --git "):
            parca_icinde = False
        elif s.startswith("@@ "):
            parca_icinde = True
        elif parca_icinde and s.startswith("+"):
            eklenen.append(s[1:])
    print(f"ste-fark: eklenen satir = {len(eklenen)}", flush=True)
    if not eklenen:
        return 0
    linter = Path(
        linter or Path.home() / ".claude/skills/asd-ste100/scripts/ste-lint.py"
    )
    if not linter.exists():
        print(f"ste-fark: linter yok: {linter}")
        return 1
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(linter)],
        input="\n".join(eklenen) + "\n",
        encoding="utf-8",
    ).returncode


if __name__ == "__main__":
    sys.exit(ste_fark(*sys.argv[1:]))
