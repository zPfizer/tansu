"""Kanca betiği (kurulum/kanca.py): tek JSON girdi alır, çıkış kodu ve çıktıyla karar verir.

Testler betiği alt süreç olarak çalıştırır; girdi birebir JSON'dur, beklenen değerler sabittir.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BETIK = Path(__file__).resolve().parents[1] / "kurulum" / "kanca.py"


def _kos(girdi, *argv, cwd=None, env=None):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(BETIK), *argv],
        input=json.dumps(girdi),
        capture_output=True,
        encoding="utf-8",
        cwd=cwd,
        env=env,
    )


def _iz(yol, *beceriler, komut=None):
    """Küçük JSONL dökümü yazar: her beceri için bir Skill çağrısı, komut için bir kullanıcı satırı."""
    satirlar = [{"type": "user", "message": {"role": "user", "content": "merhaba"}}]
    for ad in beceriler:
        blok = {"type": "tool_use", "name": "Skill", "input": {"skill": ad}}
        satirlar.append(
            {"type": "assistant", "message": {"role": "assistant", "content": [blok]}}
        )
    if komut:
        icerik = f"<command-name>/{komut}</command-name>"
        satirlar.append(
            {"type": "user", "message": {"role": "user", "content": icerik}}
        )
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("".join(json.dumps(s) + "\n" for s in satirlar), encoding="utf-8")
    return yol


def _duzenle(dosya, iz, arac="Edit", **ek):
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": arac,
        "tool_input": {"file_path": dosya},
        "transcript_path": str(iz),
        **ek,
    }


# --- 02: beceri kapısı ---


def test_yonerge_dosyasi_beceri_cagrisiz_engellenir(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl")
    s = _kos(_duzenle("AGENTS.md", iz))
    assert s.returncode == 2
    assert "Call the Skill tool with asd-ste100, then retry." in s.stderr


def test_yonerge_dosyasi_beceri_cagrisiyla_gecer(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl", "asd-ste100")
    s = _kos(_duzenle("AGENTS.md", iz))
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def test_komut_satiri_da_cagri_sayilir(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl", komut="asd-ste100")
    assert _kos(_duzenle("AGENTS.md", iz)).returncode == 0


@pytest.mark.parametrize(
    "dosya",
    [
        "C:\\Users\\levent\\Desktop\\TANSU-retro\\CODING_STANDARDS.md",
        "/c/x/.github/pull_request_template.md",
        "docs/agents/kod-kurallari.md",
        "x/.claude/agents/codex.md",
        "x/.claude/skills/tansu-belge/SKILL.md",
        "DEFINITION_OF_DONE.md",
        "CLAUDE.md",
    ],
)
def test_her_yonerge_dosyasi_engellenir(tmp_path, dosya):
    iz = _iz(tmp_path / "ana.jsonl")
    s = _kos(_duzenle(dosya, iz, arac="Write"))
    assert s.returncode == 2
    assert "asd-ste100" in s.stderr


def test_kod_dosyasi_iki_beceriyi_de_ister(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl")
    s = _kos(_duzenle("C:\\a\\TANSU-retro\\tests\\test_x.py", iz, arac="MultiEdit"))
    assert s.returncode == 2
    assert "Call the Skill tool with mattpocock-skills:tdd, then retry." in s.stderr
    assert "Call the Skill tool with ponytail:ponytail, then retry." in s.stderr


def test_kod_dosyasi_yalniz_eksik_beceriyi_ister(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl", "tdd")
    s = _kos(_duzenle("kurulum/kanca.py", iz))
    assert s.returncode == 2
    assert "ponytail:ponytail" in s.stderr
    assert "tdd" not in s.stderr


def test_kod_dosyasi_iki_beceriyle_gecer(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl", "mattpocock-skills:tdd", "ponytail:ponytail")
    s = _kos(_duzenle("kurulum/kurulum.ps1", iz))
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


@pytest.mark.parametrize(
    "dosya",
    [
        "docs/TASARIM.md",
        ".scratch/x.md",
        "C:/Users/levent/Desktop/TANSU/.scratch/x.py",
        "tansu/veri.json",
        "betik.py",
    ],
)
def test_baska_dosyalar_gecer(tmp_path, dosya):
    iz = _iz(tmp_path / "ana.jsonl")
    s = _kos(_duzenle(dosya, iz))
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def test_alt_ajan_kendi_dokumunden_okunur(tmp_path):
    ana = _iz(tmp_path / "ana.jsonl", "asd-ste100")
    _iz(tmp_path / "ana" / "subagents" / "agent-a1.jsonl")
    s = _kos(_duzenle("AGENTS.md", ana, agent_id="a1"))
    assert s.returncode == 2
    assert "asd-ste100" in s.stderr


def test_alt_ajanin_kendi_cagrisi_sayilir(tmp_path):
    ana = _iz(tmp_path / "ana.jsonl")
    _iz(tmp_path / "ana" / "subagents" / "agent-a1.jsonl", "asd-ste100")
    s = _kos(_duzenle("AGENTS.md", ana, agent_id="a1"))
    assert (s.returncode, s.stderr) == (0, "")


def test_alt_ajan_dokumu_yoksa_ana_dokume_duser(tmp_path):
    ana = _iz(tmp_path / "ana.jsonl", "asd-ste100")
    s = _kos(_duzenle("AGENTS.md", ana, agent_id="yok"))
    assert (s.returncode, s.stderr) == (0, "")


def test_bilinmeyen_olay_sessizce_gecer():
    s = _kos({"hook_event_name": "Notification"})
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


# --- 03: kabuk kuralları ---


def _kabuk(komut, arac="Bash", cwd=None):
    return _kos(
        {
            "hook_event_name": "PreToolUse",
            "tool_name": arac,
            "tool_input": {"command": komut},
            "cwd": str(cwd or Path.cwd()),
        }
    )


@pytest.fixture
def dosya(tmp_path):
    (tmp_path / "f.txt").write_text("bir\niki\n", encoding="utf-8")
    return tmp_path / "f.txt"


def test_cat_var_olan_dosyayi_engeller(tmp_path, dosya):
    s = _kabuk("cat f.txt", cwd=tmp_path)
    assert s.returncode == 2
    assert "Read the file with the Read tool, not with cat." in s.stderr


def test_get_content_mutlak_yolu_engeller(tmp_path, dosya):
    s = _kabuk(f"Get-Content {dosya}", arac="PowerShell", cwd=tmp_path)
    assert s.returncode == 2
    assert "not with get-content." in s.stderr


def test_git_bash_yolu_eslenir(tmp_path, dosya):
    p = dosya.as_posix()
    gitbash = f"/{p[0].lower()}{p[2:]}" if p[1:2] == ":" else p
    s = _kabuk(f"tail -n 1 {gitbash}", cwd=tmp_path)
    assert s.returncode == 2
    assert "not with tail." in s.stderr


@pytest.mark.parametrize(
    "komut",
    [
        "sed -n '1,2p' f.txt",
        "FOO=1 head -n 1 f.txt",
        "echo a && awk '{print}' f.txt",
        "ls | cut -c1-3 f.txt",
        "type f.txt",
    ],
)
def test_kabuk_okumasi_her_bicimde_engellenir(tmp_path, dosya, komut):
    assert _kabuk(komut, cwd=tmp_path).returncode == 2


@pytest.mark.parametrize(
    "komut",
    [
        "git log | head -5",
        "head -n 5",
        "cat yok.txt",
        "cat",
        "echo f.txt",
        "$x = Get-Content f.txt",
    ],
)
def test_boru_okumasi_ve_dosyasiz_komutlar_gecer(tmp_path, dosya, komut):
    s = _kabuk(komut, cwd=tmp_path)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def test_heredoc_engellenir():
    komut = "git commit -m \"$(cat <<'EOF'\nmesaj\nEOF\n)\""
    s = _kabuk(komut)
    assert s.returncode == 2
    assert (
        "No heredoc. Give a commit message with several -m arguments or -F <file>. "
        "Put Python code in a file or in one-line -c." in s.stderr
    )


@pytest.mark.parametrize(
    ("komut", "arac"),
    [
        ("git commit -m bir -m iki", "Bash"),
        ("cat <<< merhaba", "Bash"),
        ('echo "<<EOF"', "PowerShell"),
    ],
)
def test_heredoc_olmayan_komutlar_gecer(komut, arac):
    s = _kabuk(komut, arac=arac)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def test_bash_ten_kapi_ps1_engellenir():
    s = _kabuk("powershell -File kurulum/kapi.ps1")
    assert s.returncode == 2
    assert "Run kurulum\\kapi.ps1 with the PowerShell tool, not from Bash." in s.stderr


def test_powershell_aracindan_kapi_ps1_gecer():
    s = _kabuk(".\\kurulum\\kapi.ps1", arac="PowerShell")
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def test_git_ref_yolu_msys_olmadan_engellenir():
    s = _kabuk("git show HEAD:.claude/settings.json")
    assert s.returncode == 2
    assert (
        "Put MSYS_NO_PATHCONV=1 before git, or Git Bash changes the <ref>:<path> argument."
        in s.stderr
    )


@pytest.mark.parametrize(
    ("komut", "arac"),
    [
        ("MSYS_NO_PATHCONV=1 git show HEAD:.claude/settings.json", "Bash"),
        ("git show HEAD:AGENTS.md", "Bash"),
        ("git show HEAD:.claude/settings.json", "PowerShell"),
    ],
)
def test_git_ref_yolu_kosullari_gecer(komut, arac):
    s = _kabuk(komut, arac=arac)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


# --- 04: cevap kontrolleri ---


def _cikti(s):
    """Betik başarıyla bitip JSON yazmalı; yazmadıysa assert düşer."""
    assert (s.returncode, s.stdout != "") == (0, True)
    return json.loads(s.stdout)


def _arac_sonrasi(komut, arac="Bash"):
    return _kos(
        {
            "hook_event_name": "PostToolUse",
            "tool_name": arac,
            "tool_input": {"command": komut},
        }
    )


@pytest.mark.parametrize("arac", ["Bash", "PowerShell"])
def test_gh_pr_create_sonrasi_hatirlatir(arac):
    s = _arac_sonrasi("gh pr create --title x --body y", arac)
    assert _cikti(s) == {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "A pull request was opened. If the ccd_pr tools exist, call get_status. "
            "If it does not report this pull request, call bind_pr.",
        }
    }


@pytest.mark.parametrize("komut", ["gh pr list", "gh pr view 42", "git push"])
def test_baska_komutlar_sonrasi_sessiz(komut):
    s = _arac_sonrasi(komut)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def _alt_durdur(tmp_path, istem, son, **ek):
    iz = tmp_path / "alt.jsonl"
    iz.write_text(
        json.dumps({"type": "user", "message": {"role": "user", "content": istem}})
        + "\n"
        + json.dumps(
            {"type": "user", "message": {"role": "user", "content": "at most 1 words"}}
        )
        + "\n",
        encoding="utf-8",
    )
    return _kos(
        {
            "hook_event_name": "SubagentStop",
            "agent_transcript_path": str(iz),
            "last_assistant_message": son,
            **ek,
        }
    )


def test_alt_ajan_sinirdan_uzunsa_geri_gonderilir(tmp_path):
    s = _alt_durdur(tmp_path, "Answer in at most 5 words.", "bir iki uc dort bes alti")
    assert _cikti(s) == {
        "decision": "block",
        "reason": "Your answer has 6 words. The limit of your prompt is 5 words. "
        "Write the answer again in at most 5 words.",
    }


@pytest.mark.parametrize(
    ("istem", "son"),
    [
        ("Answer in at most 5 words.", "bir iki uc dort bes"),
        ("Answer in at most 5 words.", "  bir\niki\tuc dort bes  "),
        ("Cevap en fazla 3 sözcük olsun.", "bir iki uc"),
        ("Cevap en fazla 3 kelime olsun.", "bir iki uc"),
        ("Answer in AT MOST 3 Words.", "bir iki uc"),
        ("Answer briefly.", "bir iki uc dort bes alti yedi"),
    ],
)
def test_alt_ajan_sinir_icindeyse_veya_sinir_yoksa_gecer(tmp_path, istem, son):
    s = _alt_durdur(tmp_path, istem, son)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


@pytest.mark.parametrize(
    ("istem", "ileti"),
    [
        (
            "Cevap en fazla 3 sözcük olsun.",
            "Your answer has 4 words. The limit of your prompt is 3 words.",
        ),
        (
            "Cevap en fazla 3 kelime olsun.",
            "Your answer has 4 words. The limit of your prompt is 3 words.",
        ),
    ],
)
def test_alt_ajan_turkce_sinir_okunur(tmp_path, istem, ileti):
    s = _alt_durdur(tmp_path, istem, "bir iki uc dort")
    assert _cikti(s)["reason"].startswith(ileti)


def test_alt_ajan_ilk_kullanici_mesaji_blok_listesi_olabilir(tmp_path):
    iz = tmp_path / "alt.jsonl"
    icerik = [{"type": "text", "text": "Reply in at most 2 words."}]
    iz.write_text(
        json.dumps({"type": "user", "message": {"role": "user", "content": icerik}})
        + "\n",
        encoding="utf-8",
    )
    s = _kos(
        {
            "hook_event_name": "SubagentStop",
            "agent_transcript_path": str(iz),
            "last_assistant_message": "bir iki uc",
        }
    )
    assert _cikti(s)["decision"] == "block"


def test_alt_ajan_ikinci_kez_geri_gonderilmez(tmp_path):
    s = _alt_durdur(
        tmp_path, "Answer in at most 2 words.", "bir iki uc dort", stop_hook_active=True
    )
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def _durdur(son, **ek):
    return _kos({"hook_event_name": "Stop", "last_assistant_message": son, **ek})


def _engel(vurus):
    return {
        "decision": "block",
        "reason": f"Your last message names an internal file or a section number: {vurus}. "
        "Levent gets no internal file or rule number. Write the message again without them. "
        "Put a command in a code block.",
    }


@pytest.mark.parametrize(
    ("son", "vurus"),
    [
        ("Open AGENTS.md first.", "AGENTS.md"),
        ("The rule is in § 5.1 now.", "§"),
        ("See docs/TASARIM.md and § 5.1 and kod.py.", "TASARIM.md, kod.py, §"),
        ("Check kayit.jsonl and ayar.json.", "kayit.jsonl, ayar.json"),
    ],
)
def test_son_mesajda_dosya_adi_veya_paragraf_isareti_geri_gonderilir(son, vurus):
    s = _durdur(son)
    assert _cikti(s) == _engel(vurus)


@pytest.mark.parametrize(
    "son",
    [
        "Done. Run this:\n```\npytest tests/test_kanca.py\n```\nThen look at PR 42, commit a1b2c3d.",
        "Run:\n~~~powershell\nGet-Content AGENTS.md  # § 5\n~~~",
        "Nothing to report. See https://github.com/zPfizer/TANSU/pull/42.",
        "Version 3.14 and e.g. this.",
    ],
)
def test_son_mesaj_temizse_veya_kod_blogundaysa_gecer(son):
    s = _durdur(son)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def test_son_mesaj_ikinci_kez_geri_gonderilmez():
    s = _durdur("Open AGENTS.md first.", stop_hook_active=True)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


# --- 05: ste-fark ---

SAHTE_LINTER = (
    "import sys\n"
    "metin = sys.stdin.read()\n"
    "print('linter girdisi:', metin.strip())\n"
    "sys.exit(1 if ';' in metin else 0)\n"
)


def _git(kok, *args):
    subprocess.run(
        ["git", "-c", "user.name=T", "-c", "user.email=t@example.com"]
        + ["-c", "commit.gpgsign=false", "-C", str(kok), *args],
        check=True,
        capture_output=True,
        encoding="utf-8",
    )


@pytest.fixture
def depo(tmp_path):
    """Eski AGENTS.md satırında noktalı virgül var; hepsi kayıtlı."""
    kok = tmp_path / "depo"
    kok.mkdir()
    _git(kok, "init", "-q", "-b", "master")
    (kok / "AGENTS.md").write_text("eski; satir\n", encoding="utf-8")
    (kok / "docs").mkdir()
    (kok / "docs" / "TASARIM.md").write_text("tasarim\n", encoding="utf-8")
    _git(kok, "add", "AGENTS.md", "docs/TASARIM.md")
    _git(kok, "commit", "-q", "-m", "ilk")
    return kok


@pytest.fixture
def linter(tmp_path):
    yol = tmp_path / "sahte_linter.py"
    yol.write_text(SAHTE_LINTER, encoding="utf-8")
    return yol


def _fark(depo, linter):
    return _kos({}, "ste-fark", "HEAD", str(linter), cwd=depo)


def test_ste_fark_eklenen_noktali_virgulde_kalir(depo, linter):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("yeni; satir\n")
    s = _fark(depo, linter)
    assert s.returncode == 1
    assert "ste-fark: eklenen satir = 1" in s.stdout
    assert "linter girdisi: yeni; satir" in s.stdout


def test_ste_fark_eski_noktali_virgul_ve_temiz_ekleme_gecer(depo, linter):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("yeni temiz satir\n")
    s = _fark(depo, linter)
    assert "ste-fark: eklenen satir = 1" in s.stdout
    assert "linter girdisi: yeni temiz satir" in s.stdout
    assert "eski" not in s.stdout
    assert s.returncode == 0


def test_ste_fark_yonerge_disi_dosya_sayilmaz(depo, linter):
    (depo / "docs" / "TASARIM.md").write_text("tasarim; degisti\n", encoding="utf-8")
    s = _fark(depo, linter)
    assert (s.returncode, s.stdout) == (0, "ste-fark: eklenen satir = 0\n")


def test_ste_fark_linter_dosyasi_yoksa_kalir(depo, tmp_path):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("yeni temiz satir\n")
    yok = tmp_path / "yok.py"
    s = _fark(depo, yok)
    assert s.returncode == 1
    assert f"ste-fark: linter yok: {yok}" in s.stdout


def test_ste_fark_varsayilan_linter_ev_klasorundedir(depo, tmp_path):
    with (depo / "AGENTS.md").open("a", encoding="utf-8") as f:
        f.write("yeni temiz satir\n")
    ev = tmp_path / "ev"
    ev.mkdir()
    env = {**os.environ, "USERPROFILE": str(ev), "HOME": str(ev)}
    s = _kos({}, "ste-fark", "HEAD", cwd=depo, env=env)
    beklenen = ev / ".claude" / "skills" / "asd-ste100" / "scripts" / "ste-lint.py"
    assert s.returncode == 1
    assert f"ste-fark: linter yok: {beklenen}" in s.stdout
