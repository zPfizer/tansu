import json
import os
import subprocess
import sys
import time
import venv
from pathlib import Path

import pytest

BETIK = Path(__file__).resolve().parents[1] / "kurulum" / "kanca.py"
MESAJ = (
    "For behavior changes, run a red test under tests/ before code edits. "
    "For a pure refactor, use refactor-before and refactor-after with unchanged tests. "
    'See kurulum/kanca.py --help and CODING_STANDARDS.md "Test first". '
    "Observed session_id: null.\n"
)


@pytest.fixture(autouse=True)
def git_ortami(monkeypatch, tmp_path):
    for ad in os.environ:
        if ad.startswith("GIT_"):
            monkeypatch.delenv(ad)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_ATTR_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))
    (tmp_path / "iz.jsonl").write_text("", encoding="utf-8")


def _git(depo, *arg):
    return subprocess.run(
        [
            "git",
            "-c",
            "user.name=Tansu test",
            "-c",
            "user.email=test@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.autocrlf=false",
            "-c",
            f"core.attributesFile={os.devnull}",
            "-c",
            f"core.excludesFile={os.devnull}",
            *arg,
        ],
        cwd=depo,
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout.strip()


@pytest.fixture
def depo(tmp_path):
    dizin = tmp_path / "depo"
    dizin.mkdir()
    _git(dizin, "init", "-b", "main", "--template=")
    for dosya in ("tansu/a.py", "tests/test_a.py"):
        yol = dizin / dosya
        yol.parent.mkdir()
        yol.write_text("# İlk sürüm\n", encoding="utf-8")
    _git(dizin, "add", "tansu/a.py", "tests/test_a.py")
    _git(dizin, "commit", "-m", "taban")
    _git(dizin, "update-ref", "refs/remotes/origin/main", "HEAD")
    return dizin


def _kos(girdi, cwd, env=None, python=sys.executable):
    return subprocess.run(
        [python, "-X", "utf8", str(BETIK)],
        input=json.dumps(girdi),
        capture_output=True,
        encoding="utf-8",
        cwd=cwd,
        env=env,
    )


def _duzenle(
    depo,
    dosya="tansu/a.py",
    arac="Edit",
    env=None,
    session_id=None,
    python=sys.executable,
):
    return _kos(
        {
            "hook_event_name": "PreToolUse",
            "tool_name": arac,
            "tool_input": {"file_path": str(depo / dosya)},
            "transcript_path": str(depo.parent / "iz.jsonl"),
            "session_id": session_id,
        },
        depo,
        env,
        python,
    )


@pytest.mark.parametrize("arac", ["Edit", "Write", "MultiEdit"])
@pytest.mark.parametrize("dosya", ["tansu/a.py", "kurulum/yeni/a.py", ".github/a.py"])
def test_kod_duzenleme_test_degisikligi_ister(depo, arac, dosya):
    sonuc = _duzenle(depo, dosya, arac)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (2, "", MESAJ)


@pytest.mark.parametrize("durum", ["yeni", "degisen", "staged", "commit"])
def test_test_degisikligi_kodu_acar(depo, durum):
    dosya = "tests/yeni.py" if durum == "yeni" else "tests/test_a.py"
    (depo / dosya).write_text("# Yeni test\n", encoding="utf-8")
    if durum in {"staged", "commit"}:
        _git(depo, "add", dosya)
    if durum == "commit":
        _git(depo, "commit", "-m", "test")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_baska_klasordeki_test_sayilmaz(depo):
    (depo / "test_a.py").write_text("# Test\n", encoding="utf-8")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (2, "", MESAJ)


@pytest.mark.parametrize(
    "dosya",
    [
        "tests/test_a.py",
        "AGENTS.md",
        ".scratch/x.py",
        "betik.py",
        "tansu/a.md",
        "tansu/a.ps1",
    ],
)
@pytest.mark.parametrize("git_var", [True, False])
def test_kapsam_disindaki_dosyalar_gecer(depo, dosya, git_var):
    ortam = None if git_var else {**os.environ, "PATH": ""}
    sonuc = _duzenle(depo, dosya, env=ortam)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_depo_disindaki_klasor_gecer(tmp_path):
    disari = tmp_path / "disari"
    disari.mkdir()
    sonuc = _duzenle(disari)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_git_baslatilamazsa_gecer(depo):
    sonuc = _duzenle(depo, env={**os.environ, "PATH": ""})
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


@pytest.mark.parametrize("test_degisti", [False, True])
def test_origin_main_yoksa_yalniz_calisma_agaci_sayilir(depo, test_degisti):
    _git(depo, "update-ref", "-d", "refs/remotes/origin/main")
    if test_degisti:
        (depo / "tests/test_a.py").write_text("# Yeni\n", encoding="utf-8")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (
        (0, "", "") if test_degisti else (2, "", MESAJ)
    )


def test_origin_main_bozuksa_engellemez(depo):
    (depo / ".git/refs/remotes/origin/main").write_text("bozuk\n", encoding="utf-8")
    sonuc = _duzenle(depo)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


@pytest.mark.parametrize("arac", ["Bash", "PowerShell", "Read"])
def test_baska_araclar_sessizce_gecer(tmp_path, arac):
    sonuc = _kos({"hook_event_name": "PreToolUse", "tool_name": arac}, tmp_path)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


@pytest.mark.parametrize("olay", ["SubagentStop", "Notification", "Bilinmeyen"])
def test_baska_olaylar_sessizce_gecer(tmp_path, olay):
    sonuc = _kos({"hook_event_name": olay}, tmp_path)
    assert (sonuc.returncode, sonuc.stdout, sonuc.stderr) == (0, "", "")


def test_gecersiz_json_engellemez(tmp_path):
    sonuc = subprocess.run(
        [sys.executable, "-X", "utf8", str(BETIK)],
        input="json degil",
        capture_output=True,
        encoding="utf-8",
        cwd=tmp_path,
    )
    assert sonuc.returncode == 1
    assert "JSONDecodeError" in sonuc.stderr


@pytest.fixture
def refactor_depo(depo):
    (depo / "tansu/a.py").write_text("def deger():\n    return 6\n", encoding="utf-8")
    (depo / "tests/test_a.py").write_text(
        "import runpy\n"
        "def test_deger():\n"
        "    assert runpy.run_path('tansu/a.py')['deger']() == 6\n",
        encoding="utf-8",
    )
    (depo / ".gitignore").write_text("__pycache__/\n.pytest_cache/\n", encoding="utf-8")
    _git(depo, "add", "tansu/a.py", "tests/test_a.py", ".gitignore")
    _git(depo, "commit", "-m", "calisan test")
    _git(depo, "update-ref", "refs/remotes/origin/main", "HEAD")
    return depo


def _refactor(
    depo,
    komut="refactor-before",
    session_id="oturum",
    *secimler,
    env=None,
    python=sys.executable,
):
    if komut == "refactor-before" and not secimler:
        secimler = ("--file", "tansu/a.py", "--test", "tests/test_a.py")
    return subprocess.run(
        [
            python,
            "-X",
            "utf8",
            str(BETIK),
            komut,
            "--session-id",
            session_id,
            *secimler,
        ],
        input="{}",
        capture_output=True,
        encoding="utf-8",
        cwd=depo,
        env=env,
    )


@pytest.fixture
def farkli_python(tmp_path):
    taban = Path(sys._base_executable)
    if taban != Path(sys.executable):
        return str(taban)
    dizin = tmp_path / "kanca-python"
    venv.EnvBuilder(with_pip=False).create(dizin)
    return str(dizin / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))


@pytest.mark.parametrize("python_turu", ["ayni", "farkli"])
def test_saf_refaktor_gercek_once_sonra_kanitiyla_acilir_ve_kapanir(
    refactor_depo, farkli_python, python_turu
):
    depo = refactor_depo
    python = sys.executable if python_turu == "ayni" else farkli_python
    once = _refactor(depo)
    assert once.returncode == 0, once.stdout + once.stderr
    izin = _duzenle(depo, session_id="oturum", python=python)
    assert izin.returncode == 0, izin.stderr
    (depo / "tansu/a.py").write_text(
        "def deger():\n    return 2 * 3\n", encoding="utf-8"
    )
    assert _duzenle(depo, session_id="oturum", python=python).returncode == 0
    sonra = _refactor(depo, "refactor-after")
    assert sonra.returncode == 0, sonra.stdout + sonra.stderr
    assert _duzenle(depo, session_id="oturum", python=python).returncode == 2


def _kanit(sonuc):
    assert sonuc.returncode == 0, sonuc.stdout + sonuc.stderr
    yol = Path(json.loads(sonuc.stdout.splitlines()[-1])["receipt"])
    return yol, json.loads(yol.read_text(encoding="utf-8"))


def test_refaktor_sonrasi_farkli_python_testi_baslatmadan_reddedilir(
    refactor_depo, farkli_python
):
    depo = refactor_depo
    yol, once = _kanit(_refactor(depo))
    sonra = _refactor(depo, "refactor-after", python=farkli_python)
    assert sonra.returncode == 1
    assert "Use the same Python interpreter as the before run." in sonra.stderr
    assert sonra.stdout == ""
    assert json.loads(yol.read_text(encoding="utf-8")) == once


def test_davranis_degisen_sonra_kosusu_kapanmaz_ve_sureyi_uzatmaz(refactor_depo):
    depo = refactor_depo
    yol, once = _kanit(_refactor(depo))
    (depo / "tansu/a.py").write_text("def deger():\n    return 7\n", encoding="utf-8")
    sonra = _refactor(depo, "refactor-after")
    assert sonra.returncode == 1
    assert "assert 7 == 6" in sonra.stdout
    assert json.loads(yol.read_text(encoding="utf-8")) == once
    assert _duzenle(depo, session_id="oturum").returncode == 0
    (depo / "tansu/a.py").write_text(
        "def deger():\n    return 3 + 3\n", encoding="utf-8"
    )
    assert _refactor(depo, "refactor-after").returncode == 0


@pytest.mark.parametrize("durum", ["basarisiz", "bos", "skip", "hata"])
def test_basarisiz_once_kaniti_izin_vermez(refactor_depo, durum):
    depo = refactor_depo
    test = {
        "basarisiz": "def test_a():\n    assert False\n",
        "bos": "# Toplanacak test yok.\n",
        "skip": "import pytest\ndef test_a():\n    pytest.skip('fixture')\n",
        "hata": "raise RuntimeError('collection error')\n",
    }[durum]
    (depo / "tests/test_a.py").write_text(test, encoding="utf-8")
    _git(depo, "add", "tests/test_a.py")
    _git(depo, "commit", "-m", "olumsuz test tabani")
    _git(depo, "update-ref", "refs/remotes/origin/main", "HEAD")
    sonuc = _refactor(depo)
    assert sonuc.returncode == 1
    assert _duzenle(depo, session_id="oturum").returncode == 2


def test_yeni_basarisiz_once_eski_izni_gecersiz_kilar(refactor_depo):
    depo = refactor_depo
    _kanit(_refactor(depo))
    (depo / "tansu/a.py").write_text("def deger():\n    return 7\n", encoding="utf-8")
    sonuc = _refactor(depo)
    assert sonuc.returncode == 1
    assert "assert 7 == 6" in sonuc.stdout
    assert _duzenle(depo, session_id="oturum").returncode == 2


@pytest.mark.parametrize(
    "durum", ["oturum", "hedef", "head", "worktree", "eksik_oturum"]
)
def test_kanit_yalniz_ayni_oturum_ve_kapsamda_gecer(refactor_depo, durum):
    depo = refactor_depo
    _kanit(_refactor(depo))
    assert _duzenle(depo, session_id="oturum").returncode == 0
    oturum, dosya = "oturum", "tansu/a.py"
    if durum == "oturum":
        oturum = "diger"
    elif durum == "eksik_oturum":
        oturum = None
    elif durum == "hedef":
        dosya = "tansu/b.py"
    elif durum == "head":
        _git(depo, "commit", "--allow-empty", "-m", "yeni head")
    else:
        diger = depo.parent / "diger-worktree"
        _git(depo, "worktree", "add", "--detach", str(diger), "HEAD")
        depo = diger
    assert _duzenle(depo, dosya, session_id=oturum).returncode == 2


@pytest.mark.parametrize(
    "dosya", ["tests/test_a.py", "pyproject.toml", "tansu/b.py", " veri ü.txt"]
)
def test_kapsam_disi_degisen_girdi_sonra_kanitini_reddeder(refactor_depo, dosya):
    depo = refactor_depo
    yol, once = _kanit(_refactor(depo))
    with (depo / dosya).open("a", encoding="utf-8") as cikti:
        cikti.write("\n# Degisen girdi\n")
    sonra = _refactor(depo, "refactor-after")
    assert sonra.returncode == 1
    assert "outside the declared code scope changed" in sonra.stderr
    assert json.loads(yol.read_text(encoding="utf-8")) == once
    if not dosya.startswith("tests/"):
        assert _duzenle(depo, session_id="oturum").returncode == 2


@pytest.mark.parametrize(
    "durum",
    [
        "json",
        "derin_json",
        "eksik_alan",
        "eksik_ozet",
        "surum",
        "kapali",
        "sure",
        "gelecek",
        "buyuk_tamsayi",
        "rapor",
    ],
)
def test_gecersiz_kanit_git_hatasi_gibi_izin_vermez(refactor_depo, durum):
    depo = refactor_depo
    yol, kanit = _kanit(_refactor(depo))
    if durum == "json":
        yol.write_text("{", encoding="utf-8")
    elif durum == "derin_json":
        yol.write_text("[" * 100000 + "0" + "]" * 100000, encoding="utf-8")
    elif durum == "rapor":
        Path(kanit["before"]["report"]).write_text("<broken>", encoding="utf-8")
    else:
        if durum == "eksik_alan":
            kanit.pop("before")
        elif durum == "eksik_ozet":
            kanit.pop("baseline_full_hash")
        elif durum == "surum":
            kanit["version"] = 999
        elif durum == "kapali":
            kanit["state"] = "closed"
        elif durum == "buyuk_tamsayi":
            kanit["created_at"] = 10**1000
            kanit["expires_at"] = kanit["created_at"] + 28800
        else:
            kanit["created_at"] = time.time() + (
                3600 if durum == "gelecek" else -9 * 3600
            )
            kanit["expires_at"] = kanit["created_at"] + 8 * 3600
        yol.write_text(json.dumps(kanit), encoding="utf-8")
    sonuc = _duzenle(depo, session_id="oturum")
    assert sonuc.returncode == 2, sonuc.stderr
    assert _refactor(depo, "refactor-after").returncode == 1


@pytest.mark.parametrize(
    "dosya,test",
    [
        ("../tansu/outside.py", "tests/test_a.py"),
        ("tansu/*.py", "tests/test_a.py"),
        ("tansu", "tests/test_a.py"),
        ("tests/test_a.py", "tests/test_a.py"),
        ("tansu/a.py", "../tests/test_a.py"),
        ("tansu/a.py", "--collect-only"),
    ],
)
def test_kapsam_ve_test_secimi_dosya_disina_cikamaz(refactor_depo, dosya, test):
    depo = refactor_depo
    _kanit(_refactor(depo))
    sonuc = _refactor(
        depo, "refactor-before", "oturum", "--file", dosya, "--test=" + test
    )
    assert sonuc.returncode == 1, sonuc.stdout + sonuc.stderr
    assert _duzenle(depo, session_id="oturum").returncode == 2


def test_toplama_secenekleri_gercek_test_kosusunu_degistiremez(refactor_depo):
    depo = refactor_depo
    (depo / "pyproject.toml").write_text(
        '[tool.pytest.ini_options]\naddopts = "--collect-only"\n', encoding="utf-8"
    )
    _, kanit = _kanit(
        _refactor(depo, env={**os.environ, "PYTEST_ADDOPTS": "--collect-only"})
    )
    assert kanit["before"]["cases"] == [["tests.test_a", "test_deger", "passed"]]
    assert _duzenle(depo, session_id="oturum").returncode == 0
    (depo / "tansu/a.py").write_text("def deger():\n    return 7\n", encoding="utf-8")
    sonuc = _refactor(
        depo, "refactor-after", env={**os.environ, "PYTEST_ADDOPTS": "--collect-only"}
    )
    assert sonuc.returncode == 1
    assert "assert 7 == 6" in sonuc.stdout


def test_oturumlar_birbirinin_kanitini_kapatmaz_ve_yeni_dosya_kapsama_girer(
    refactor_depo,
):
    depo = refactor_depo
    ilk, _ = _kanit(_refactor(depo))
    ikinci, _ = _kanit(
        _refactor(
            depo,
            "refactor-before",
            "ikinci",
            "--file",
            "tansu/a.py",
            "--file",
            "kurulum/yeni/b.py",
            "--test",
            "tests/test_a.py::test_deger",
        )
    )
    assert ilk != ikinci
    assert _refactor(depo, "refactor-after").returncode == 0
    assert _duzenle(depo, session_id="oturum").returncode == 2
    assert _duzenle(depo, "kurulum/yeni/b.py", session_id="ikinci").returncode == 0
    (depo / "kurulum/yeni").mkdir(parents=True)
    (depo / "kurulum/yeni/b.py").write_text("VALUE = 6\n", encoding="utf-8")
    assert _refactor(depo, "refactor-after", "ikinci").returncode == 0


def test_git_ortami_baska_deponun_testini_veya_kanitini_kullanamaz(refactor_depo):
    depo = refactor_depo
    diger = depo.parent / "diger"
    _git(depo, "clone", "--no-hardlinks", str(depo), str(diger))
    (diger / "tests/test_a.py").write_text("# Baska test\n", encoding="utf-8")
    ortam = {
        **os.environ,
        "GIT_DIR": str(diger / ".git"),
        "GIT_WORK_TREE": str(diger),
        "GIT_INDEX_FILE": str(diger / ".git/index"),
    }
    _, kanit = _kanit(_refactor(depo, env=ortam))
    assert Path(kanit["repo"]["root"]) == depo
    assert _duzenle(depo, env=ortam, session_id="oturum").returncode == 0
    assert _duzenle(depo, env=ortam, session_id="baska").returncode == 2


@pytest.mark.parametrize("degisim", ["cases", "skips"])
def test_ayni_test_dosyalarinda_farkli_vaka_ve_skip_sonucu_kapanmaz(
    refactor_depo, degisim
):
    depo = refactor_depo
    (depo / "tansu/a.py").write_text("CASES = [1, 2]\nSKIP = False\n", encoding="utf-8")
    (depo / "tests/test_a.py").write_text(
        "import runpy\nimport pytest\n"
        "source = runpy.run_path('tansu/a.py')\n"
        "@pytest.mark.parametrize('case', source['CASES'])\n"
        "def test_case(case):\n"
        "    if source['SKIP'] and case == 2:\n"
        "        pytest.skip('source-controlled case')\n"
        "    assert case > 0\n",
        encoding="utf-8",
    )
    _git(depo, "add", "tansu/a.py", "tests/test_a.py")
    _git(depo, "commit", "-m", "dinamik vakalar")
    _git(depo, "update-ref", "refs/remotes/origin/main", "HEAD")
    _kanit(_refactor(depo))
    (depo / "tansu/a.py").write_text(
        "CASES = [1, 2, 3]\nSKIP = False\n"
        if degisim == "cases"
        else "CASES = [1, 2]\nSKIP = True\n",
        encoding="utf-8",
    )
    sonuc = _refactor(depo, "refactor-after")
    assert sonuc.returncode == 1
    assert "Test case identities or skip states changed" in sonuc.stderr


@pytest.mark.parametrize("asama", ["before", "after"])
def test_test_kosarken_degisen_kod_kanit_olmaz(refactor_depo, asama):
    depo = refactor_depo
    (depo / "tansu/a.py").write_text(
        f"MUTATE = {asama == 'before'}\n", encoding="utf-8"
    )
    (depo / "tests/test_a.py").write_text(
        "import runpy\nfrom pathlib import Path\n"
        "def test_mutation():\n"
        "    if runpy.run_path('tansu/a.py')['MUTATE']:\n"
        "        Path('tansu/a.py').write_text('MUTATE = True\\n# changed\\n', encoding='utf-8')\n"
        "    assert True\n",
        encoding="utf-8",
    )
    _git(depo, "add", "tansu/a.py", "tests/test_a.py")
    _git(depo, "commit", "-m", "kosu sirasinda degisim")
    _git(depo, "update-ref", "refs/remotes/origin/main", "HEAD")
    if asama == "after":
        _kanit(_refactor(depo))
        (depo / "tansu/a.py").write_text("MUTATE = True\n", encoding="utf-8")
    sonuc = _refactor(depo, "refactor-" + asama)
    assert sonuc.returncode == 1
    assert "changed during the" in sonuc.stderr


def test_engel_oturum_kimligini_kod_olarak_yazmaz(refactor_depo):
    oturum = "'; $(Write-Output injected)\nnext"
    sonuc = _duzenle(refactor_depo, session_id=oturum)
    assert sonuc.returncode == 2
    assert json.dumps(oturum) in sonuc.stderr
    assert len(sonuc.stderr.splitlines()) == 1
