"""Check test changes or explicit refactor evidence before a Claude code edit.

Only PreToolUse Edit, Write, and MultiEdit events can block an edit.
Hook exit 2 blocks an edit. Hook exit 0 permits it without output.
An uncaught exception, including invalid JSON, exits 1 and does not block.
Git errors on the ordinary route permit edits. Invalid refactor evidence does not.
The ordinary route sees Git changes. It cannot prove that a test ran red.
A test change on the branch counts for every code file.
The refactor commands run selected tests before and after scoped edits.
Passing tests do not establish semantic equivalence or adequate coverage.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

KOD_KLASORLERI = {"tansu", "kurulum", ".github"}
KANIT_SURESI = 8 * 60 * 60


def _ortam():
    korunan = {
        "GIT_CONFIG_NOSYSTEM",
        "GIT_CONFIG_GLOBAL",
        "GIT_CONFIG_SYSTEM",
        "GIT_ATTR_NOSYSTEM",
    }
    return {
        ad: deger
        for ad, deger in os.environ.items()
        if not ad.upper().startswith("GIT_") or ad.upper() in korunan
    }


def _git(dizin, *arg):
    return subprocess.run(
        ["git", "-C", str(dizin), *arg],
        capture_output=True,
        encoding="utf-8",
        errors="surrogateescape",
        check=True,
        env=_ortam(),
    ).stdout


def _kod_deposu(dosya):
    if dosya.suffix != ".py" or not KOD_KLASORLERI.intersection(dosya.parts[:-1]):
        return None
    ust = dosya.parent
    while not ust.is_dir():
        ust = ust.parent
    kok = Path(_git(ust, "rev-parse", "--show-toplevel").strip()).resolve()
    goreli = dosya.relative_to(kok)
    return kok if goreli.parts[0] in KOD_KLASORLERI else None


def _test_degisti(kok):
    if _git(kok, "status", "--porcelain", "--untracked-files=all", "--", "tests"):
        return True
    try:
        _git(kok, "rev-parse", "--verify", "--quiet", "refs/remotes/origin/main")
    except subprocess.CalledProcessError as hata:
        if hata.returncode == 1 and not hata.stdout and not hata.stderr:
            return False
        raise
    ortak = _git(kok, "merge-base", "HEAD", "origin/main").strip()
    return bool(_git(kok, "diff", "--name-only", f"{ortak}..HEAD", "--", "tests"))


def _kimlik(kok):
    return {
        "root": str(kok),
        "git_dir": str(
            Path(_git(kok, "rev-parse", "--absolute-git-dir").strip()).resolve()
        ),
        "head": _git(kok, "rev-parse", "HEAD").strip(),
    }


def _kanit_yolu(kimlik, oturum):
    anahtar = json.dumps([kimlik["root"], kimlik["git_dir"], oturum]).encode("utf-8")
    return (
        Path(tempfile.gettempdir())
        / "tansu-refactor-v1"
        / (hashlib.sha256(anahtar).hexdigest() + ".json")
    )


def _kaydet(yol, kanit):
    yol.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=yol.parent, delete=False
    ) as dosya:
        json.dump(kanit, dosya, ensure_ascii=True, sort_keys=True)
        gecici = dosya.name
    os.replace(gecici, yol)


def _secimler(kok, dosyalar, testler):
    if not dosyalar or not testler:
        raise ValueError("Declare at least one code file and one test file.")
    kod = []
    secilen = []
    for girdi, hedef in [(ad, kod) for ad in dosyalar] + [
        (ad, secilen) for ad in testler
    ]:
        if not isinstance(girdi, str) or not girdi or girdi.startswith("-"):
            raise ValueError("Invalid file selection.")
        dosya, *dugum = girdi.split("::", 1) if hedef is secilen else [girdi]
        if any(isaret in dosya for isaret in "*?[]"):
            raise ValueError("Select exact files, not patterns.")
        yol = (kok / dosya).resolve()
        goreli = yol.relative_to(kok)
        if yol.suffix != ".py" or yol.is_dir():
            raise ValueError("Select a Python file.")
        if hedef is kod:
            if goreli.parts[0] not in KOD_KLASORLERI:
                raise ValueError("The code file is outside the guarded folders.")
        elif goreli.parts[0] != "tests" or not yol.is_file():
            raise ValueError("Select an existing test file under tests/.")
        hedef.append(goreli.as_posix() + ("::" + dugum[0] if dugum else ""))
    return sorted(set(kod)), sorted(set(secilen))


def _anlik(kok, dosyalar):
    tumu = hashlib.sha256()
    disarisi = hashlib.sha256()
    adlar = set(
        _git(kok, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split(
            "\0"
        )
    ) - {""}
    for ad in sorted(adlar):
        yol = kok / ad
        yol.resolve().relative_to(kok)
        if yol.is_symlink():
            icerik = b"link\0" + os.fsencode(os.readlink(yol))
        elif not yol.exists():
            icerik = b"missing"
        else:
            icerik = b"file\0" + hashlib.sha256(yol.read_bytes()).digest()
        kayit = os.fsencode(ad) + b"\0" + icerik + b"\0"
        tumu.update(kayit)
        if ad not in dosyalar:
            disarisi.update(kayit)
    return tumu.hexdigest(), disarisi.hexdigest()


def _sonuclar(rapor):
    kok = ET.fromstring(rapor)
    durumlar = []
    for test in kok.iter("testcase"):
        if test.find("failure") is not None or test.find("error") is not None:
            raise ValueError("The test report contains a failure or an error.")
        durumlar.append(
            [
                test.get("classname", ""),
                test.get("name", ""),
                "skipped" if test.find("skipped") is not None else "passed",
            ]
        )
    if not any(durum[2] == "passed" for durum in durumlar):
        raise ValueError("The test run has no passing cases.")
    return sorted(durumlar)


def _testleri_kos(kok, testler):
    dizin = Path(tempfile.mkdtemp(prefix="tansu-refactor-run-"))
    rapor = dizin / "junit.xml"
    cikti = dizin / "output.txt"
    komut = [
        sys.executable,
        "-X",
        "utf8",
        "-B",
        "-m",
        "pytest",
        "-q",
        "-o",
        "addopts=",
        "-p",
        "no:cacheprovider",
        "--basetemp",
        str(dizin / "pytest"),
        "--junitxml",
        str(rapor),
        *testler,
    ]
    ortam = _ortam()
    ortam.pop("PYTEST_ADDOPTS", None)
    sonuc = subprocess.run(
        komut,
        cwd=kok,
        env=ortam,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        encoding="utf-8",
        timeout=3600,
    )
    cikti.write_text(sonuc.stdout + sonuc.stderr, encoding="utf-8")
    print(sonuc.stdout, end="")
    print(sonuc.stderr, end="", file=sys.stderr)
    if sonuc.returncode != 0:
        raise ValueError(f"Tests failed with exit {sonuc.returncode}. Output: {cikti}")
    veri = rapor.read_bytes()
    return {
        "argv": komut,
        "exit_code": 0,
        "report": str(rapor),
        "sha256": hashlib.sha256(veri).hexdigest(),
        "cases": _sonuclar(veri),
        "output": str(cikti),
    }


def _kaniti_oku(kok, oturum):
    kimlik = _kimlik(kok)
    yol = _kanit_yolu(kimlik, oturum)
    try:
        kanit = json.loads(yol.read_text(encoding="utf-8"))
    except RecursionError as hata:
        raise ValueError("The refactor evidence JSON is nested too deeply.") from hata
    if (
        not isinstance(kanit, dict)
        or set(kanit)
        != {
            "version",
            "state",
            "session_id",
            "repo",
            "files",
            "tests",
            "created_at",
            "expires_at",
            "baseline_full_hash",
            "outside_scope_hash",
            "before",
        }
        or type(kanit.get("version")) is not int
        or kanit.get("version") != 1
        or kanit.get("state") != "open"
    ):
        raise ValueError("Refactor evidence is not open.")
    if not all(
        isinstance(kanit[ad], str)
        and len(kanit[ad]) == 64
        and all(harf in "0123456789abcdef" for harf in kanit[ad])
        for ad in ("baseline_full_hash", "outside_scope_hash")
    ):
        raise ValueError("Invalid evidence fingerprint.")
    if kanit["session_id"] != oturum or kanit["repo"] != kimlik:
        raise ValueError("Refactor session, worktree, or HEAD changed.")
    simdi = time.time()
    baslangic, bitis = kanit["created_at"], kanit["expires_at"]
    if not all(
        type(sayi) in {int, float} and -sys.float_info.max <= sayi <= sys.float_info.max
        for sayi in (baslangic, bitis)
    ):
        raise ValueError("Invalid evidence time.")
    if not baslangic <= simdi < bitis or bitis != baslangic + KANIT_SURESI:
        raise ValueError("Refactor evidence expired or has an invalid time.")
    if not isinstance(kanit["files"], list) or not isinstance(kanit["tests"], list):
        raise ValueError("Invalid evidence selections.")
    dosyalar, testler = _secimler(kok, kanit["files"], kanit["tests"])
    if dosyalar != kanit["files"] or testler != kanit["tests"]:
        raise ValueError("Evidence selections are not canonical.")
    once = kanit["before"]
    if (
        not isinstance(once, dict)
        or set(once) != {"argv", "exit_code", "report", "sha256", "cases", "output"}
        or not isinstance(once["argv"], list)
        or not once["argv"]
        or not all(isinstance(arg, str) for arg in once["argv"])
        or not isinstance(once["output"], str)
        or type(once["exit_code"]) is not int
    ):
        raise ValueError("Invalid before-run evidence.")
    rapor_yolu = Path(once["report"]).resolve()
    if (
        rapor_yolu.parent.parent != Path(tempfile.gettempdir()).resolve()
        or not rapor_yolu.parent.name.startswith("tansu-refactor-run-")
        or rapor_yolu.name != "junit.xml"
    ):
        raise ValueError("The report is outside its private temporary directory.")
    rapor = rapor_yolu.read_bytes()
    if (
        once["exit_code"] != 0
        or hashlib.sha256(rapor).hexdigest() != once["sha256"]
        or _sonuclar(rapor) != once["cases"]
    ):
        raise ValueError("The before report does not match its evidence.")
    if _anlik(kok, dosyalar)[1] != kanit["outside_scope_hash"]:
        raise ValueError("Inputs outside the declared code scope changed.")
    return yol, kanit


def _refactor_once(kok, oturum, dosyalar, testler):
    kimlik = _kimlik(kok)
    yol = _kanit_yolu(kimlik, oturum)
    kanit = {"version": 1, "state": "pending", "session_id": oturum, "repo": kimlik}
    _kaydet(yol, kanit)
    dosyalar, testler = _secimler(kok, dosyalar, testler)
    tumu, disarisi = _anlik(kok, dosyalar)
    baslangic = time.time()
    once = _testleri_kos(kok, testler)
    if _kimlik(kok) != kimlik or _anlik(kok, dosyalar) != (tumu, disarisi):
        raise ValueError("The tested inputs changed during the before run.")
    kanit.update(
        state="open",
        files=dosyalar,
        tests=testler,
        created_at=baslangic,
        expires_at=baslangic + KANIT_SURESI,
        baseline_full_hash=tumu,
        outside_scope_hash=disarisi,
        before=once,
    )
    _kaydet(yol, kanit)
    print(json.dumps({"state": "open", "receipt": str(yol)}))
    return 0


def _refactor_sonra(kok, oturum):
    yol, kanit = _kaniti_oku(kok, oturum)
    if Path(sys.executable) != Path(kanit["before"]["argv"][0]):
        raise ValueError("Use the same Python interpreter as the before run.")
    taban = _anlik(kok, kanit["files"])
    sonra = _testleri_kos(kok, kanit["tests"])
    if _anlik(kok, kanit["files"]) != taban or _kaniti_oku(kok, oturum)[1] != kanit:
        raise ValueError("The tested inputs or evidence changed during the after run.")
    if sonra["cases"] != kanit["before"]["cases"]:
        raise ValueError("Test case identities or skip states changed.")
    kanit.update(
        state="closed", after=sonra, final_full_hash=taban[0], closed_at=time.time()
    )
    _kaydet(yol, kanit)
    print(json.dumps({"state": "closed", "receipt": str(yol)}))
    return 0


def _refactor_izni(kok, oturum, dosya):
    if not isinstance(oturum, str) or not oturum.strip():
        return False
    try:
        _, kanit = _kaniti_oku(kok, oturum)
        return dosya.relative_to(kok).as_posix() in kanit["files"]
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        ET.ParseError,
        subprocess.CalledProcessError,
    ):
        return False


def _komut():
    parser = argparse.ArgumentParser(
        description='Run unchanged tests before and after a pure refactor. Apply CODING_STANDARDS.md "Test first". Passing tests do not prove semantic equivalence. Git-ignored and external inputs are outside the fingerprint.'
    )
    alt = parser.add_subparsers(dest="command", required=True)
    once = alt.add_parser(
        "refactor-before",
        help="Run a passing baseline and open an eight-hour scoped grant.",
    )
    sonra = alt.add_parser(
        "refactor-after", help="Repeat the saved tests and close the grant on success."
    )
    for komut in (once, sonra):
        komut.add_argument(
            "--session-id",
            required=True,
            help="Use the actual session_id printed by the blocked Claude edit.",
        )
    once.add_argument(
        "--file",
        action="append",
        default=[],
        help="Exact guarded Python file, repeated for each file. Future files are allowed.",
    )
    once.add_argument(
        "--test",
        action="append",
        default=[],
        help="Existing Python file or node ID under tests/, repeated as needed.",
    )
    arg = parser.parse_args()
    try:
        if not arg.session_id.strip():
            raise ValueError("A nonempty session ID is required.")
        kok = Path(_git(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()
        if arg.command == "refactor-before":
            return _refactor_once(kok, arg.session_id, arg.file, arg.test)
        return _refactor_sonra(kok, arg.session_id)
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        ET.ParseError,
        subprocess.SubprocessError,
    ) as hata:
        print(f"Refactor evidence rejected: {hata}", file=sys.stderr)
        return 1


def main():
    if len(sys.argv) > 1:
        return _komut()
    girdi = json.load(sys.stdin)
    if girdi.get("hook_event_name") != "PreToolUse":
        return 0
    if girdi.get("tool_name") not in {"Edit", "Write", "MultiEdit"}:
        return 0
    dosya = Path(girdi["tool_input"]["file_path"])
    if not dosya.is_absolute():
        dosya = Path(girdi.get("cwd") or Path.cwd()) / dosya
    try:
        dosya = dosya.resolve()
        kok = _kod_deposu(dosya)
        if kok is None or _test_degisti(kok):
            return 0
    except OSError, subprocess.CalledProcessError:
        return 0
    oturum = girdi.get("session_id")
    if _refactor_izni(kok, oturum, dosya):
        return 0
    print(
        "For behavior changes, run a red test under tests/ before code edits. "
        "For a pure refactor, use refactor-before and refactor-after with unchanged tests. "
        'See kurulum/kanca.py --help and CODING_STANDARDS.md "Test first". '
        f"Observed session_id: {json.dumps(oturum, ensure_ascii=True)}.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
