"""Hook script of Claude Code. Hook mode: no arguments, one JSON on stdin, action by hook_event_name.

An exception ends with exit 1. Claude Code shows the error and does not block. An unknown event ends with exit 0.
- PreToolUse Edit, Write, MultiEdit: an instruction file needs a call of asd-ste100 by the acting agent.
- PreToolUse Edit, Write, MultiEdit: a code file needs calls of mattpocock-skills:tdd and ponytail:ponytail.
- PreToolUse Bash, PowerShell: a shell read of an existing file is blocked (use the Read tool).
- PreToolUse Bash: a heredoc, the text kapi.ps1, and git <ref>:.<path> without MSYS_NO_PATHCONV=1 are blocked.
- PostToolUse Bash, PowerShell: after gh pr create, a reminder to call the ccd_pr tools.
- SubagentStop: an answer longer than the word limit of the subagent prompt is sent back once.
- Stop: a final message with a file name or the sign § outside code blocks is sent back once.
- ste-fark <base> [linter]: the STE linter reads only the lines added to the instruction files since <base>.

The skill gate mirrors AGENTS.md "Every job" (STE before instruction text)
and `tansu-yeni-is` "Build" (tdd and ponytail before code).
"""

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

YONERGE_ADLARI = {
    "AGENTS.md",
    "CLAUDE.md",
    "CODING_STANDARDS.md",
    "DEFINITION_OF_DONE.md",
}
YONERGE_YOLLARI = [
    (".github", "pull_request_template.md"),
    ("docs", "agents"),
    (".claude", "agents"),
    (".claude", "skills"),
]
KOD_KLASORLERI = {"tansu", "tests", "kurulum", ".github"}
STE_YOLLARI = [
    "AGENTS.md",
    "CLAUDE.md",
    "CODING_STANDARDS.md",
    "DEFINITION_OF_DONE.md",
    ".github/pull_request_template.md",
    "docs/agents",
    ".claude/agents",
    ".claude/skills",
]
OKUMA_KOMUTLARI = {
    "cat",
    "head",
    "tail",
    "sed",
    "awk",
    "cut",
    "less",
    "more",
    "get-content",
    "gc",
    "type",
}


def _iz_yolu(girdi):
    """Dökümü: alt ajan girdisinde kendi dökümü varsa o, yoksa ana döküm."""
    yol = Path(girdi["transcript_path"])
    if ajan := girdi.get("agent_id"):
        alt = yol.with_suffix("") / "subagents" / f"agent-{ajan}.jsonl"
        if alt.exists():
            return alt
    return yol


def _cagrilar(yol):
    """Dökümde çağrılan beceri adları: Skill araç çağrıları ve /komut satırları."""
    adlar = set()
    for satir in Path(yol).read_text(encoding="utf-8").splitlines():
        if not satir.strip():
            continue
        kayit = json.loads(satir)
        icerik = (kayit.get("message") or {}).get("content")
        for blok in icerik if isinstance(icerik, list) else []:
            if blok.get("type") == "tool_use" and blok.get("name") == "Skill":
                adlar.add(blok["input"]["skill"])
        if kayit.get("type") == "user":
            adlar.update(re.findall(r"<command-name>/([^<]+)</command-name>", satir))
    return adlar


def _ardisik(parcalar, dizi):
    return any(parcalar[i : i + len(dizi)] == list(dizi) for i in range(len(parcalar)))


def _gerekli_beceriler(dosya):
    parcalar = dosya.replace("\\", "/").split("/")
    if parcalar[-1] in YONERGE_ADLARI or any(
        _ardisik(parcalar, y) for y in YONERGE_YOLLARI
    ):
        return ["asd-ste100"]
    if parcalar[-1].endswith((".py", ".ps1")) and KOD_KLASORLERI & set(parcalar[:-1]):
        return ["mattpocock-skills:tdd", "ponytail:ponytail"]
    return []


def _beceri_kapisi(girdi):
    gerekli = _gerekli_beceriler(girdi["tool_input"]["file_path"])
    if not gerekli:
        return 0
    cagrilan = _cagrilar(_iz_yolu(girdi))
    eksik = [b for b in gerekli if not {b, b.rpartition(":")[2]} & cagrilan]
    for ad in eksik:
        print(f"Call the Skill tool with {ad}, then retry.", file=sys.stderr)
    return 2 if eksik else 0


def _dosya_mu(belirtec, cwd):
    # ponytail: any later token that is an existing file counts as the operand.
    # Ceiling: "$x = Get-Content f" and nested calls pass; a file named like an option value (head -n 5, file "5") blocks.
    adaylar = (belirtec, re.sub(r"^/([a-zA-Z])/", r"\1:/", belirtec))
    return any((Path(cwd) / a).is_file() for a in adaylar)


def _okuma_komutu(komut, cwd):
    """Dosya okuyan ilk komutun adını döner; yoksa None."""
    for parca in re.split(r"\|\||&&|[|;\n]", komut):
        try:
            belirtecler = shlex.split(
                parca, posix=False
            )  # posix=False: Windows yolları bozulmaz
        except ValueError:
            belirtecler = parca.split()
        belirtecler = [b.strip("\"'") for b in belirtecler]
        while belirtecler and re.match(r"\w+=", belirtecler[0]):
            belirtecler.pop(0)
        if not belirtecler:
            continue
        ad = Path(belirtecler[0].replace("\\", "/")).name.lower().removesuffix(".exe")
        if ad in OKUMA_KOMUTLARI and any(
            not b.startswith("-") and _dosya_mu(b, cwd) for b in belirtecler[1:]
        ):
            return ad
    return None


def _kabuk(girdi):
    komut = girdi["tool_input"]["command"]
    mesaj = None
    if girdi["tool_name"] == "Bash":
        if re.search(r"(?<!<)<<(?!<)-?[ \t]*['\"]?\w", komut):
            mesaj = (
                "No heredoc. Give a commit message with several -m arguments or -F <file>. "
                "Put Python code in a file or in one-line -c."
            )
        elif "kapi.ps1" in komut:
            mesaj = "Run kurulum\\kapi.ps1 with the PowerShell tool, not from Bash."
        elif (
            re.search(r"\bgit\b", komut)
            and re.search(r"\S+:\.[\w./-]", komut)
            and "MSYS_NO_PATHCONV=1" not in komut
        ):
            mesaj = "Put MSYS_NO_PATHCONV=1 before git, or Git Bash changes the <ref>:<path> argument."
    if not mesaj and (ad := _okuma_komutu(komut, girdi.get("cwd") or ".")):
        mesaj = f"Read the file with the Read tool, not with {ad}."
    if mesaj:
        print(mesaj, file=sys.stderr)
    return 2 if mesaj else 0


def _on_arac(girdi):
    if girdi["tool_name"] in ("Edit", "Write", "MultiEdit"):
        return _beceri_kapisi(girdi)
    if girdi["tool_name"] in ("Bash", "PowerShell"):
        return _kabuk(girdi)
    return 0


def _arac_sonrasi(girdi):
    if girdi["tool_name"] in ("Bash", "PowerShell") and re.search(
        r"\bgh\s+pr\s+create\b", girdi["tool_input"]["command"]
    ):
        _yaz_json(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": "A pull request was opened. If the ccd_pr tools exist, call get_status. "
                    "If it does not report this pull request, call bind_pr.",
                }
            }
        )
    return 0


def _ilk_kullanici_mesaji(yol):
    for satir in Path(yol).read_text(encoding="utf-8").splitlines():
        kayit = json.loads(satir)
        ileti = kayit.get("message") or kayit
        if ileti.get("role") == "user":
            icerik = ileti["content"]
            if isinstance(icerik, list):
                return "\n".join(b.get("text", "") for b in icerik)
            return icerik
    return ""


def _alt_ajan_durdu(girdi):
    if girdi.get("stop_hook_active"):
        return 0
    eslesme = re.search(
        r"(?:at most|en fazla)\s+(\d+)\s+(?:words?|sözcük|kelime)",
        _ilk_kullanici_mesaji(girdi["agent_transcript_path"]),
        re.IGNORECASE,
    )
    sayi = len(girdi["last_assistant_message"].split())
    if eslesme and sayi > int(eslesme[1]):
        sinir = eslesme[1]
        _yaz_json(
            {
                "decision": "block",
                "reason": f"Your answer has {sayi} words. The limit of your prompt is {sinir} words. "
                f"Write the answer again in at most {sinir} words.",
            }
        )
    return 0


def _durdu(girdi):
    if girdi.get("stop_hook_active"):
        return 0
    metin = re.sub(r"(```|~~~).*?\1", "", girdi["last_assistant_message"], flags=re.S)
    vurus = re.findall(
        r"\b[\w.-]+\.(?:md|py|ps1|json|jsonl|yml|yaml|xml|toml|txt)\b", metin
    )
    vurus += ["§"] if "§" in metin else []
    if vurus:
        _yaz_json(
            {
                "decision": "block",
                "reason": "Your last message names an internal file or a section number: "
                f"{', '.join(dict.fromkeys(vurus))}. Levent gets no internal file or rule number. "
                "Write the message again without them. Put a command in a code block.",
            }
        )
    return 0


def _yaz_json(nesne):
    print(json.dumps(nesne))


KANCALAR = {
    "PreToolUse": _on_arac,
    "PostToolUse": _arac_sonrasi,
    "SubagentStop": _alt_ajan_durdu,
    "Stop": _durdu,
}


def ste_fark(taban, linter=None):
    """STE linter'ı yalnız yönerge dosyalarına eklenen satırlarla çalıştırır; çıkış kodu linter'ınkidir."""
    fark = subprocess.run(
        ["git", "diff", "-U0", "--no-color", taban, "--", *STE_YOLLARI],
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout
    eklenen = [
        s[1:]
        for s in fark.splitlines()
        if s.startswith("+") and not s.startswith("+++")
    ]
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


def main(argv):
    if argv[:1] == ["ste-fark"]:
        return ste_fark(*argv[1:])
    girdi = json.load(sys.stdin)
    return KANCALAR.get(girdi["hook_event_name"], lambda g: 0)(girdi)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
