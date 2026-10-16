"""SessionStart kancası (kurulum/oturum_baslangic.py): temiz ana depoyu kaynak/master'a ilerletir.

Testler gerçek git depoları kurar: uzak (bare), ana depo (uzak adı `kaynak`) ve yeni kayıt iten ikinci bir klon.
"""

import shutil
import subprocess

import pytest

from kurulum.oturum_baslangic import guncelle

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git yok")

GERI = "TANSU master kaynak/master'ın {} kayıt gerisinde; kurallar eski olabilir"


@pytest.fixture(autouse=True)
def _git_kimlik(monkeypatch):
    for ad in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{ad}_NAME", "Test")
        monkeypatch.setenv(f"GIT_{ad}_EMAIL", "test@example.com")
    monkeypatch.setenv("GIT_CONFIG_COUNT", "2")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "commit.gpgsign")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "false")
    monkeypatch.setenv("GIT_CONFIG_KEY_1", "core.autocrlf")
    monkeypatch.setenv("GIT_CONFIG_VALUE_1", "false")


def _git(kok, *args):
    return subprocess.run(
        ["git", "-C", str(kok), *args],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.strip()


def _kayit(kok, ad):
    (kok / "a.txt").write_text(ad, encoding="utf-8")
    _git(kok, "add", "a.txt")
    _git(kok, "commit", "-q", "-m", ad)


def _ileri(yan, n):
    """Uzağa n yeni kayıt iter."""
    for i in range(n):
        _kayit(yan, f"yeni-{i}")
    _git(yan, "push", "-q", "origin", "master")


@pytest.fixture
def depo(tmp_path):
    """(ana, yan): ana depo kaynak/master ile eşit; yan, uzağa kayıt itmek için ikinci klon."""
    uzak = tmp_path / "uzak.git"
    subprocess.run(
        ["git", "init", "-q", "--bare", "-b", "master", str(uzak)], check=True
    )
    ana = tmp_path / "ana"
    subprocess.run(["git", "init", "-q", "-b", "master", str(ana)], check=True)
    _git(ana, "remote", "add", "kaynak", str(uzak))
    _kayit(ana, "ilk")
    _git(ana, "push", "-q", "kaynak", "master")
    yan = tmp_path / "yan"
    subprocess.run(["git", "clone", "-q", str(uzak), str(yan)], check=True)
    return ana, yan


def test_temiz_master_bir_kayit_geride_ilerletilir(depo):
    ana, yan = depo
    _ileri(yan, 1)
    assert guncelle(ana) == ""
    assert _git(ana, "rev-parse", "master") == _git(ana, "rev-parse", "kaynak/master")
    assert _git(ana, "rev-list", "--count", "master") == "2"


def test_temiz_master_uc_kayit_geride_ilerletilir(depo):
    ana, yan = depo
    _ileri(yan, 3)
    assert guncelle(ana) == ""
    assert _git(ana, "rev-parse", "master") == _git(ana, "rev-parse", "kaynak/master")
    assert _git(ana, "rev-list", "--count", "master") == "4"


def test_kirli_agac_degismez_ve_uyarir(depo):
    ana, yan = depo
    _ileri(yan, 1)
    onceki = _git(ana, "rev-parse", "master")
    (ana / "a.txt").write_text("elle degisti", encoding="utf-8")
    assert guncelle(ana) == GERI.format(1)
    assert _git(ana, "rev-parse", "master") == onceki
    assert (ana / "a.txt").read_text(encoding="utf-8") == "elle degisti"


def test_izlenmeyen_dosya_ilerletmeyi_engellemez(depo):
    # Ana depoda `.scratch/` gibi izlenmeyen klasörler hep vardır.
    ana, yan = depo
    _ileri(yan, 1)
    (ana / "taslak.txt").write_text("izlenmiyor", encoding="utf-8")
    assert guncelle(ana) == ""
    assert _git(ana, "rev-parse", "master") == _git(ana, "rev-parse", "kaynak/master")
    assert (ana / "taslak.txt").read_text(encoding="utf-8") == "izlenmiyor"


def test_baska_dal_degismez_ve_uyarir(depo):
    ana, yan = depo
    _git(ana, "switch", "-q", "-c", "pr/x")
    _ileri(yan, 1)
    onceki = _git(ana, "rev-parse", "master")
    assert guncelle(ana) == GERI.format(1)
    assert _git(ana, "rev-parse", "master") == onceki
    assert _git(ana, "branch", "--show-current") == "pr/x"


def test_bagli_calisma_agaci_degismez(depo, tmp_path):
    ana, yan = depo
    wt = tmp_path / "wt"
    _git(ana, "worktree", "add", "-q", "-b", "pr/w", str(wt))
    _ileri(yan, 1)
    master = _git(ana, "rev-parse", "master")
    kafa = _git(wt, "rev-parse", "HEAD")
    assert guncelle(wt) == ""
    assert _git(ana, "rev-parse", "master") == master
    assert _git(wt, "rev-parse", "HEAD") == kafa
    assert _git(wt, "status", "--short") == ""


def test_kaynak_uzagi_yoksa_bos_doner(depo):
    ana, yan = depo
    _git(ana, "remote", "remove", "kaynak")
    assert guncelle(ana) == ""


def test_fetch_basarisizsa_ulasilamadi_der_ve_degismez(depo, tmp_path):
    # Karar (tur 1): başarısız fetch "güncel" gibi görünmez; sabit uyarı satırı yazılır.
    ana, yan = depo
    _git(ana, "remote", "set-url", "kaynak", str(tmp_path / "yok.git"))
    onceki = _git(ana, "rev-parse", "master")
    assert (
        guncelle(ana) == "TANSU kaynak/master'a ulaşılamadı; kurallar eski olabilir"
    )
    assert _git(ana, "rev-parse", "master") == onceki


def test_master_kaynakla_esitse_bos_doner(depo):
    ana, yan = depo
    assert guncelle(ana) == ""
    assert _git(ana, "rev-parse", "master") == _git(ana, "rev-parse", "kaynak/master")


def _kayit_dosyasi(ana, yan):
    """İzlenen kayit/kartlar.jsonl ekler; ana ve yan aynı kayıtta kalır."""
    (ana / "kayit").mkdir()
    (ana / "kayit" / "kartlar.jsonl").write_text("bir\n", encoding="utf-8")
    _git(ana, "add", "kayit/kartlar.jsonl")
    _git(ana, "commit", "-q", "-m", "kayit")
    _git(ana, "push", "-q", "kaynak", "master")
    _git(yan, "pull", "-q", "origin", "master")


def test_kayit_klasorundeki_yerel_degisiklik_ilerletmeyi_engellemez(depo):
    ana, yan = depo
    _kayit_dosyasi(ana, yan)
    _ileri(yan, 1)
    (ana / "kayit" / "kartlar.jsonl").write_text("bir\nyerel\n", encoding="utf-8")
    assert guncelle(ana) == ""
    assert _git(ana, "rev-parse", "master") == _git(ana, "rev-parse", "kaynak/master")
    assert (ana / "kayit" / "kartlar.jsonl").read_text(encoding="utf-8") == (
        "bir\nyerel\n"
    )


def test_kayit_disindaki_izlenen_degisiklik_engeller(depo):
    ana, yan = depo
    _kayit_dosyasi(ana, yan)
    _ileri(yan, 1)
    onceki = _git(ana, "rev-parse", "master")
    (ana / "kayit" / "kartlar.jsonl").write_text("bir\nyerel\n", encoding="utf-8")
    (ana / "a.txt").write_text("elle degisti", encoding="utf-8")
    assert guncelle(ana) == GERI.format(1)
    assert _git(ana, "rev-parse", "master") == onceki


def test_uzak_ayni_kayit_dosyasini_degistirirse_ff_reddeder(depo):
    ana, yan = depo
    _kayit_dosyasi(ana, yan)
    (yan / "kayit" / "kartlar.jsonl").write_text("bir\nuzak\n", encoding="utf-8")
    _git(yan, "commit", "-q", "-a", "-m", "uzak kayit")
    _git(yan, "push", "-q", "origin", "master")
    onceki = _git(ana, "rev-parse", "master")
    (ana / "kayit" / "kartlar.jsonl").write_text("bir\nyerel\n", encoding="utf-8")
    assert guncelle(ana) == GERI.format(1)
    assert _git(ana, "rev-parse", "master") == onceki
    assert (ana / "kayit" / "kartlar.jsonl").read_text(encoding="utf-8") == (
        "bir\nyerel\n"
    )


def test_yalniz_hazirlanmis_degisiklik_engeller(depo):
    ana, yan = depo
    _ileri(yan, 1)
    onceki = _git(ana, "rev-parse", "master")
    (ana / "a.txt").write_text("hazir", encoding="utf-8")
    _git(ana, "add", "a.txt")
    assert guncelle(ana) == GERI.format(1)
    assert _git(ana, "rev-parse", "master") == onceki


def test_ayrik_head_degismez_ve_uyarir(depo):
    ana, yan = depo
    _git(ana, "switch", "-q", "--detach")
    _ileri(yan, 1)
    onceki = _git(ana, "rev-parse", "master")
    assert guncelle(ana) == GERI.format(1)
    assert _git(ana, "rev-parse", "master") == onceki
    assert _git(ana, "branch", "--show-current") == ""


def test_ayrisan_master_degismez_ve_uyarir(depo):
    ana, yan = depo
    _kayit(ana, "yerel-ek")
    _ileri(yan, 1)
    yerel = _git(ana, "rev-parse", "master")
    assert guncelle(ana) == GERI.format(1)
    assert _git(ana, "rev-parse", "master") == yerel
