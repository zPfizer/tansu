"""Kanca betiği (kurulum/kanca.py): tek JSON girdi alır, çıkış kodu ve çıktıyla karar verir.

Testler betiği alt süreç olarak çalıştırır; girdi birebir JSON'dur, beklenen değerler sabittir.
"""

import json
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
    assert (
        'Follow AGENTS.md "Every job" and tansu-yeni-is "Build", then retry.'
        in s.stderr
    )


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
    assert 'AGENTS.md "Every job"' in s.stderr


def test_arac_sonucundaki_komut_satiri_sayilmaz(tmp_path):
    blok = {
        "type": "tool_result",
        "content": "<command-name>/asd-ste100</command-name>",
    }
    iz = tmp_path / "ana.jsonl"
    iz.write_text(
        json.dumps({"type": "user", "message": {"role": "user", "content": [blok]}})
        + "\n",
        encoding="utf-8",
    )
    assert _kos(_duzenle("AGENTS.md", iz)).returncode == 2


def test_metin_blogundaki_komut_satiri_sayilir(tmp_path):
    blok = {"type": "text", "text": "<command-name>/asd-ste100</command-name>"}
    iz = tmp_path / "ana.jsonl"
    iz.write_text(
        json.dumps({"type": "user", "message": {"role": "user", "content": [blok]}})
        + "\n",
        encoding="utf-8",
    )
    assert _kos(_duzenle("AGENTS.md", iz)).returncode == 0


def test_kod_dosyasi_iki_beceriyi_de_ister(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl")
    s = _kos(_duzenle("C:\\a\\TANSU-retro\\tests\\test_x.py", iz, arac="MultiEdit"))
    assert s.returncode == 2
    assert 'tansu-yeni-is "Build"' in s.stderr
    assert "Call the Skill tool" not in s.stderr


def test_kod_dosyasi_yalniz_eksik_beceriyi_ister(tmp_path):
    iz = _iz(tmp_path / "ana.jsonl", "tdd")
    s = _kos(_duzenle("kurulum/kanca.py", iz))
    assert s.returncode == 2
    assert 'tansu-yeni-is "Build"' in s.stderr
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
    assert 'AGENTS.md "Every job"' in s.stderr


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


def test_json_olmayan_girdi_cokmeyle_biter_engellemez():
    s = subprocess.run(
        [sys.executable, "-X", "utf8", str(BETIK)],
        input="json degil",
        capture_output=True,
        encoding="utf-8",
    )
    assert s.returncode == 1
    assert "JSONDecodeError" in s.stderr


KOK = Path(__file__).resolve().parents[1]


def test_kapinin_beceri_adlari_yonerge_dosyalarinda_durur():
    agents = (KOK / "AGENTS.md").read_text(encoding="utf-8")
    her_is = agents.split("\n## Every job", 1)[1].split("\n## ", 1)[0]
    yeni_is = (KOK / ".claude/skills/tansu-yeni-is/SKILL.md").read_text(
        encoding="utf-8"
    )
    yapim = next(s for s in yeni_is.splitlines() if s.startswith("6. **Build:**"))
    assert "`asd-ste100`" in her_is
    assert "`mattpocock-skills:tdd`" in yapim
    assert "`ponytail:ponytail`" in yapim


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


@pytest.mark.parametrize("ayirici", [";", "|", "&&", "||"])
def test_tirnak_icindeki_ayirici_komut_baslatmaz(ayirici):
    s = _kabuk(f'echo "note{ayirici} head AGENTS.md"')
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


def test_cd_sonrasi_dosya_okumasi_engellenir():
    s = _kabuk("cd docs && head agents/kod-kurallari.md")
    assert s.returncode == 2
    assert "not with head." in s.stderr


@pytest.mark.parametrize(
    ("dizin", "ayirici", "dosya"),
    [
        ("__pr42_missing_dir__", "||", "AGENTS.md"),
        ("docs", "&", "AGENTS.md"),
        ("docs", "||", "agents/kod-kurallari.md"),
        ("docs", "&", "agents/kod-kurallari.md"),
    ],
)
def test_cd_belirsiz_sonucta_iki_dizini_de_denetler(dizin, ayirici, dosya):
    s = _kabuk(f"cd {dizin} {ayirici} head {dosya}")
    assert s.returncode == 2
    assert "not with head." in s.stderr


def test_heredoc_tirnakli_kapanis_parantezi_ardinda_engellenir():
    s = _kabuk("echo \"$(printf '%s' 'x)'; python - <<EOF\nprint(1)\nEOF\n)\"")
    assert s.returncode == 2
    assert "No heredoc." in s.stderr


def test_heredoc_engellenir():
    komut = "git commit -m \"$(cat <<'EOF'\nmesaj\nEOF\n)\""
    s = _kabuk(komut)
    assert s.returncode == 2
    assert (
        "No heredoc. Give a commit message with several -m arguments or -F <file>. "
        "Put Python code in a file or in one-line -c." in s.stderr
    )


@pytest.mark.parametrize(
    "komut",
    [
        "cat <<EOF\nx\nEOF",
        "cat <<'EOF'\nx\nEOF",
        'cat << "END"\nx\nEND',
        "git commit -F - <<-EOF\nx\nEOF",
        "cat <<_son\nx\n_son",
        "cat <<123\nx\n123",
        "python - <<\\EOF\nprint(1)\nEOF",
        "python - <<E\\OF\nprint(1)\nEOF",
        "python - <<$EOF\nprint(1)\n$EOF",
        "python - <<E'OF'\nprint(1)\nEOF",
        'python - <<"EOF"\nprint(1)\nEOF',
    ],
)
def test_heredoc_bicimleri_engellenir(komut):
    s = _kabuk(komut)
    assert s.returncode == 2
    assert "No heredoc." in s.stderr


@pytest.mark.parametrize(
    ("komut", "arac"),
    [
        ("git commit -m bir -m iki", "Bash"),
        ("cat <<< merhaba", "Bash"),
        ('echo "<<EOF"', "PowerShell"),
        ('python -c "print(1 << 3)"', "Bash"),
        ("echo $((1<<2))", "Bash"),
        ('x <<< "text"', "Bash"),
        ('python -c "x=2; print(1<<x)"', "Bash"),
        ('echo "<<EOF"', "Bash"),
        ('git commit -m "see <<EOF"', "Bash"),
        ("echo '<<EOF'", "Bash"),
        ("echo \"$(printf '%s' '<<EOF')\"", "Bash"),
    ],
)
def test_heredoc_olmayan_komutlar_gecer(komut, arac):
    s = _kabuk(komut, arac=arac)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


@pytest.mark.parametrize(
    "komut",
    [
        "powershell -File kurulum/kapi.ps1",
        "pwsh.exe -NoProfile -File C:/x/kurulum/kapi.ps1 -Belge",
        "./kurulum/kapi.ps1",
        "cd x && powershell -File kapi.ps1",
        "PowerShell.exe kurulum/kapi.ps1",
        'powershell -Command "& .\\kurulum\\kapi.ps1"',
        'powershell -Command ".\\kurulum\\kapi.ps1 -Belge"',
        'powershell -File "C:/a b/kurulum/kapi.ps1"',
        "powershell -Command \"& 'C:/a b/kurulum/kapi.ps1' -Belge\"",
    ],
)
def test_bash_ten_kapi_ps1_engellenir(komut):
    s = _kabuk(komut)
    assert s.returncode == 2
    assert "Run kurulum\\kapi.ps1 with the PowerShell tool, not from Bash." in s.stderr


@pytest.mark.parametrize(
    "komut",
    [
        "git add kurulum/kapi.ps1",
        "git log -- kurulum/kapi.ps1",
        "git diff origin/master -- kurulum/kapi.ps1",
        "powershell -File kurulum/baska.ps1",
        "echo kapi.ps1 | powershell -Command -",
        'powershell -Command "Write-Output kapi.ps1"',
        "powershell -Command Write-Output kapi.ps1",
    ],
)
def test_kapi_ps1_adini_anan_komutlar_gecer(komut):
    s = _kabuk(komut)
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


@pytest.mark.parametrize(
    "komut",
    [
        "powershell -ExecutionPolicy Bypass -File kurulum/kapi.ps1",
        "powershell -ExecutionPolicy Bypass kurulum/kapi.ps1",
        'pwsh -WindowStyle Hidden -Command "& kurulum/kapi.ps1"',
    ],
)
def test_kapi_secenek_degerinden_sonra_engellenir(komut):
    s = _kabuk(komut)
    assert s.returncode == 2
    assert "with the PowerShell tool, not from Bash." in s.stderr


def test_powershell_aracindan_kapi_ps1_gecer():
    s = _kabuk(".\\kurulum\\kapi.ps1", arac="PowerShell")
    assert (s.returncode, s.stdout, s.stderr) == (0, "", "")


@pytest.mark.parametrize(
    "komut",
    [
        "git show HEAD:.claude/settings.json",
        "echo MSYS_NO_PATHCONV=1; git show HEAD:.claude/settings.json",
        "MSYS_NO_PATHCONV=1; git show HEAD:.claude/settings.json",
    ],
)
def test_git_ref_yolu_msys_olmadan_engellenir(komut):
    s = _kabuk(komut)
    assert s.returncode == 2
    assert (
        "Put MSYS_NO_PATHCONV=1 before git, or Git Bash changes the <ref>:<path> argument."
        in s.stderr
    )


@pytest.mark.parametrize(
    ("komut", "arac"),
    [
        ("MSYS_NO_PATHCONV=1 git show HEAD:.claude/settings.json", "Bash"),
        ("export MSYS_NO_PATHCONV=1; git show HEAD:.claude/x", "Bash"),
        ("export MSYS_NO_PATHCONV=1 && git show HEAD:.claude/x", "Bash"),
        ("git show HEAD:AGENTS.md", "Bash"),
        ("git show HEAD:.claude/settings.json", "PowerShell"),
        ("git log --grep=HEAD:.claude/settings.json", "Bash"),
        ('MSYS_NO_PATHCONV="1" git show HEAD:.claude/settings.json', "Bash"),
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
        ("Answer in under 3 words.", "bir iki"),
        ("Answer in at most 3 words.", "bir iki uc"),
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
        (
            "Answer in UNDER 3 words.",
            "Your answer has 4 words. The limit of your prompt is 2 words. "
            "Write the answer again in at most 2 words.",
        ),
    ],
)
def test_alt_ajan_turkce_sinir_okunur(tmp_path, istem, ileti):
    s = _alt_durdur(tmp_path, istem, "bir iki uc dort")
    assert _cikti(s)["reason"].startswith(ileti)


def test_alt_ajan_under_sinir_dahil_degildir(tmp_path):
    s = _alt_durdur(tmp_path, "Answer in under 3 words.", "bir iki uc")
    assert _cikti(s) == {
        "decision": "block",
        "reason": "Your answer has 3 words. The limit of your prompt is 2 words. "
        "Write the answer again in at most 2 words.",
    }


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
