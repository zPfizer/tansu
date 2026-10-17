"""Hook script of Claude Code. Hook mode: no arguments, one JSON on stdin, action by hook_event_name.

An exception ends with exit 1. Claude Code shows the error and does not block. An unknown event ends with exit 0.
- PreToolUse Edit, Write, MultiEdit: an instruction file needs a call of asd-ste100 by the acting agent.
- PreToolUse Edit, Write, MultiEdit: a code file needs calls of mattpocock-skills:tdd and ponytail:ponytail.
- PreToolUse Bash, PowerShell: a shell read of an existing file is blocked (use the Read tool).
- PreToolUse Bash: a heredoc, a run of kapi.ps1 (powershell or pwsh with kapi.ps1, or kapi.ps1 as the command),
  and git <ref>:.<path> without MSYS_NO_PATHCONV=1 are blocked.
- SubagentStop: an answer longer than the word limit of the subagent prompt is sent back once.

The skill gate mirrors AGENTS.md "Every job" (STE before instruction text)
and `tansu-yeni-is` "Build" (tdd and ponytail before code).
"""

import json
import re
import shlex
import sys
from pathlib import Path

from ste_fark import YONERGE_YOLLARI

KOD_KLASORLERI = {"tansu", "tests", "kurulum", ".github"}
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
            metinler = (
                [icerik]
                if isinstance(icerik, str)
                else [
                    b.get("text", "") for b in icerik or [] if b.get("type") == "text"
                ]
            )
            for metin in metinler:
                adlar.update(
                    re.findall(r"<command-name>/([^<]+)</command-name>", metin)
                )
    return adlar


def _ardisik(parcalar, dizi):
    return any(parcalar[i : i + len(dizi)] == list(dizi) for i in range(len(parcalar)))


def _gerekli_beceriler(dosya):
    parcalar = dosya.replace("\\", "/").split("/")
    if any(_ardisik(parcalar, y.split("/")) for y in YONERGE_YOLLARI):
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
    if eksik:
        print(
            'Follow AGENTS.md "Every job" and tansu-yeni-is "Build", then retry.',
            file=sys.stderr,
        )
    return 2 if eksik else 0


def _dosya_mu(belirtec, cwd):
    adaylar = (belirtec, re.sub(r"^/([a-zA-Z])/", r"\1:/", belirtec))
    return any((Path(cwd) / a).is_file() for a in adaylar)


def _komutlar(komut):
    """Her komut parçası için (komut adı, belirteçler, öndeki NAME=değer atamaları)."""
    for parca in re.findall(
        r"""(?:\\.|"(?:\\.|[^"\\])*"|'[^']*'|[^|;&\n"'\\])+""", komut
    ):
        try:
            belirtecler = shlex.split(
                parca, posix=False
            )  # posix=False: Windows yolları bozulmaz
        except ValueError:
            belirtecler = parca.split()
        atamalar = []
        while belirtecler and re.match(r"\w+=", belirtecler[0]):
            anahtar, deger = belirtecler.pop(0).split("=", 1)
            atamalar.append(anahtar + "=" + deger.strip("\"'"))
        belirtecler = [b.strip("\"'") for b in belirtecler]
        if belirtecler:
            ad = Path(belirtecler[0].replace("\\", "/")).name.lower()
            yield ad.removesuffix(".exe"), belirtecler, atamalar


def _okuma_komutu(komut, cwd):
    """Dosya okuyan ilk komutun adını döner; yoksa None."""
    # ponytail: any later token that is an existing file counts as the operand.
    # Ceiling: "$x = Get-Content f" and nested calls pass; a file named like an option value (head -n 5, file "5") blocks.
    for ad, belirtecler, _ in _komutlar(komut):
        if ad == "cd" and len(belirtecler) == 2:
            cwd = Path(cwd) / belirtecler[1]
        if ad in OKUMA_KOMUTLARI and any(
            not b.startswith("-") and _dosya_mu(b, cwd) for b in belirtecler[1:]
        ):
            return ad
    return None


def _ilk_sozcuk(belirtec):
    """Belirteç tırnaklı bir komut satırıysa ilk sözcüğü (öndeki & veya . atılır)."""
    try:
        sozcukler = shlex.split(belirtec, posix=True)
    except ValueError:
        sozcukler = belirtec.split()
    if sozcukler and sozcukler[0] in ("&", "."):
        sozcukler = sozcukler[1:]
    return sozcukler[0] if sozcukler else ""


def _kapi_calistirir(komut):
    """Bash komut adını veya PowerShell'in dosya/komut girişini denetler."""
    for ad, belirtecler, _ in _komutlar(komut):
        if ad.endswith("kapi.ps1"):
            return True
        if ad not in ("powershell", "pwsh"):
            continue
        for i, b in enumerate(belirtecler[1:], 1):
            if b.lower() in ("-file", "-f", "-command", "-c"):
                if i + 1 == len(belirtecler):
                    break
                deger = belirtecler[i + 1]
                if b.lower() in ("-command", "-c"):
                    deger = _ilk_sozcuk(" ".join(belirtecler[i + 1 :]))
                if deger.lower().endswith("kapi.ps1"):
                    return True
                break
            if not b.startswith("-"):
                if b.lower().endswith("kapi.ps1"):
                    return True
                break
    return False


def _msys_eksik(komut):
    """git <ref>:.<yol> parçası, MSYS_NO_PATHCONV=1 öneki ya da önceki 'export MSYS_NO_PATHCONV=1' olmadan var mı."""
    verildi = False
    for ad, belirtecler, atamalar in _komutlar(komut):
        if ad == "export" and any(
            b.replace('"', "").replace("'", "") == "MSYS_NO_PATHCONV=1"
            for b in belirtecler[1:]
        ):
            verildi = True
        elif (
            ad == "git"
            and not verildi
            and "MSYS_NO_PATHCONV=1" not in atamalar
            and any(re.match(r"[^-\s][^\s:]*:\.[\w./-]", b) for b in belirtecler)
        ):
            return True
    return False


def _tirnaksiz(komut):
    """Tırnaklı veriyi örter, çift tırnak içindeki komutların verisini de örter."""
    return re.sub(
        r'"(?:\\.|[^"\\])*"|\'[^\']*\'|\(\(.*?\)\)',
        lambda m: (
            " ".join(
                _tirnaksiz(a or b)
                for a, b in re.findall(r"\$\((.*?)\)|`(.*?)`", m[0], re.S)
            )
            if m[0][0] == '"' and re.search(r"\$\(|`", m[0])
            else "Q"
        ),
        komut,
        flags=re.S,
    )


def _kabuk(girdi):
    komut = girdi["tool_input"]["command"]
    mesaj = None
    if girdi["tool_name"] == "Bash":
        if re.search(r"(?<!<)<<(?!<)-?[ \t]*['\"\\\w]", _tirnaksiz(komut)):
            mesaj = (
                "No heredoc. Give a commit message with several -m arguments or -F <file>. "
                "Put Python code in a file or in one-line -c."
            )
        elif _kapi_calistirir(komut):
            mesaj = "Run kurulum\\kapi.ps1 with the PowerShell tool, not from Bash."
        elif _msys_eksik(komut):
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
        r"(at most|under|en fazla)\s+(\d+)\s+(?:words?|sözcük|kelime)",
        _ilk_kullanici_mesaji(girdi["agent_transcript_path"]),
        re.IGNORECASE,
    )
    sayi = len(girdi["last_assistant_message"].split())
    # "under N" means fewer than N words, so its limit is N-1.
    sinir = eslesme and int(eslesme[2]) - (eslesme[1].lower() == "under")
    if eslesme and sayi > sinir:
        reason = (
            f"Your answer has {sayi} words. The limit of your prompt is {sinir} words. "
            f"Write the answer again in at most {sinir} words."
        )
        print(json.dumps({"decision": "block", "reason": reason}))
    return 0


KANCALAR = {
    "PreToolUse": _on_arac,
    "SubagentStop": _alt_ajan_durdu,
}


def main():
    girdi = json.load(sys.stdin)
    return KANCALAR.get(girdi["hook_event_name"], lambda g: 0)(girdi)


if __name__ == "__main__":
    sys.exit(main())
