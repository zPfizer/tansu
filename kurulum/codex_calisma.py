"""Codex helper for the Tansu agent. Two commands.

`yol <bin folder>`: print the path of the newest usable `codex.exe`.
A folder is usable when it has `codex.exe` and `codex-code-mode-host.exe`.

`denetle <exit code> <output file> <log file> [--denetim]`: check a Codex run.
A failed run is not an audit round. The command prints the reasons and exits 1.
"""

import argparse
import json
import re
import sys
from pathlib import Path

LOG_IZLERI = ("failed to spawn", "os error")


def yol(bin_klasoru):
    adaylar = [
        klasor / "codex.exe"
        for klasor in Path(bin_klasoru).glob("*")
        if (klasor / "codex.exe").is_file()
        and (klasor / "codex-code-mode-host.exe").is_file()
    ]
    if not adaylar:
        print("codex: codex.exe yok")
        return 1
    print(max(adaylar, key=lambda p: p.stat().st_mtime).resolve().as_posix())
    return 0


def _nedenler(cikis_kodu, cikti, gunluk, denetim):
    nedenler = []
    if cikis_kodu != 0:
        nedenler.append(f"cikis kodu {cikis_kodu}")
    metin = cikti.read_text(encoding="utf-8-sig") if cikti.is_file() else ""
    if not metin.strip():
        nedenler.append("cikti dosyasi yok ya da bos")
    elif denetim:
        try:
            veri = json.loads(metin)
        except ValueError:
            veri = None
        if not (isinstance(veri, dict) and "verdict" in veri):
            nedenler.append("cikti JSON degil ya da verdict yok")
    kayit = gunluk.read_text(encoding="utf-8", errors="replace")
    nedenler += [f"log: {iz}" for iz in LOG_IZLERI if iz in kayit]
    if "CreateProcessWithLogonW" in kayit:
        kilit = re.search(r"CreateProcessWithLogonW[^\n]*\b1909\b", kayit)
        nedenler.append(
            "log: Codex sandbox account locked"
            if kilit
            else "log: CreateProcessWithLogonW"
        )
    return nedenler


def denetle(cikis_kodu, cikti, gunluk, denetim):
    nedenler = _nedenler(cikis_kodu, Path(cikti), Path(gunluk), denetim)
    if nedenler:
        print("codex: denetim calismadi: " + "; ".join(nedenler))
        return 1
    print("codex: calisma tamam")
    return 0


def main(argv):
    ayristirici = argparse.ArgumentParser(prog="codex_calisma.py")
    komutlar = ayristirici.add_subparsers(dest="komut", required=True)
    komutlar.add_parser("yol").add_argument("bin_klasoru")
    d = komutlar.add_parser("denetle")
    d.add_argument("cikis_kodu", type=int)
    d.add_argument("cikti_dosyasi")
    d.add_argument("gunluk_dosyasi")
    d.add_argument("--denetim", action="store_true")
    a = ayristirici.parse_args(argv)
    if a.komut == "yol":
        return yol(a.bin_klasoru)
    return denetle(a.cikis_kodu, a.cikti_dosyasi, a.gunluk_dosyasi, a.denetim)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
