"""Bilet Status denetimi (S5): her `.scratch/**/issues/*.md` bileti tek `**Status:**` satırı taşır ve
değer `docs/agents/issue-tracker.md` "Status field" ile `docs/agents/triage-labels.md` sözleşmesinden çıkar."""

import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

STATUS = re.compile(r"^\*\*Status:\*\*\s*(.*?)\s*$")


def _izinli_degerler(kok):
    """({tam eşleşen değer: yol öneki ya da None}, parantezli değerlerin başları): sözleşme dosyalarından çıkar.

    Madde satırında değerden sonra `/` ile biten ikinci bir kod parçası varsa, değer yalnız o yol önekli biletlerde geçerlidir.
    """
    tam, bas = {}, set()
    izleyici = (kok / "docs" / "agents" / "issue-tracker.md").read_text(
        encoding="utf-8"
    )
    icinde = False
    for satir in izleyici.splitlines():
        if satir.startswith("## "):
            icinde = satir == "## Status field"
        if icinde and satir.startswith("- `"):
            deger, *oteki = satir.split("`")[1::2]
            if " (" in deger:
                bas.add(deger.split(" (")[0])
            else:
                tam[deger] = next((p for p in oteki if p.endswith("/")), None)
    etiketler = (kok / "docs" / "agents" / "triage-labels.md").read_text(
        encoding="utf-8"
    )
    for satir in etiketler.splitlines():
        if satir.startswith("| `"):
            tam.update(dict.fromkeys(re.findall(r"`([^`]+)`", satir.split("|")[2])))
    return tam, bas


def _izinli_mi(deger, goreli, tam, bas):
    if deger in tam:
        return tam[deger] is None or goreli.startswith(tam[deger])
    return any(re.fullmatch(rf"{re.escape(b)} \(\s*\S.*\)", deger) for b in bas)


def bilet_ihlalleri(kok):
    """Her bilet için 'yol:satır: neden' (yol köke göreli, `/` ayraçlı)."""
    tam, bas = _izinli_degerler(kok)
    ihlal = []
    for yol in sorted(kok.glob(".scratch/**/issues/*.md")):
        goreli = yol.relative_to(kok).as_posix()
        satirlar = yol.read_text(encoding="utf-8").splitlines()
        durumlar = [
            (no, eslesme.group(1))
            for no, satir in enumerate(satirlar, 1)
            if (eslesme := STATUS.match(satir))
        ]
        if not durumlar:
            ihlal.append(f"{goreli}:1: Status satırı yok")
        elif len(durumlar) > 1:
            ihlal.append(f"{goreli}:{durumlar[1][0]}: birden çok Status satırı")
        elif not _izinli_mi(durumlar[0][1], goreli, tam, bas):
            ihlal.append(
                f"{goreli}:{durumlar[0][0]}: izin verilmeyen değer: {durumlar[0][1]}"
            )
    return ihlal


def _sozlesme_kopyala(hedef):
    (hedef / "docs" / "agents").mkdir(parents=True, exist_ok=True)
    for ad in ("issue-tracker.md", "triage-labels.md"):
        (hedef / "docs" / "agents" / ad).write_text(
            (KOK / "docs" / "agents" / ad).read_text(encoding="utf-8"),
            encoding="utf-8",
        )


def test_bilet_ihlalleri_sahte_kokte_tam_liste(tmp_path):
    _sozlesme_kopyala(tmp_path)
    bilet = tmp_path / ".scratch" / "x" / "issues"
    bilet.mkdir(parents=True)
    ornekler = {
        "01-gecerli.md": "# T\n**Status:** ready-for-agent\n",
        "02-kapali.md": "# T\n**Status:** kapali\n",
        "03-yok.md": "# T\n\nStatus: done\n",
        "04-iki.md": "# T\n**Status:** claimed\n**Status:** resolved\n",
        "05-eski-done.md": "# T\n**Status:** done\n",
        "06-done-pr.md": "# T\n**Status:** done (PR #9, abc1234)\n",
        "07-done-bos.md": "# T\n**Status:** done ()\n",
    }
    for ad, metin in ornekler.items():
        (bilet / ad).write_text(metin, encoding="utf-8")
    arsiv = tmp_path / ".scratch" / "arsiv" / "tansu-mvp" / "issues"
    arsiv.mkdir(parents=True)
    (arsiv / "01-eski.md").write_text("# T\n**Status:** done\n", encoding="utf-8")
    # Karar: yalın `done` yalnız arşiv yolunda geçerlidir (issue-tracker.md); 05 artık reddedilir.
    assert bilet_ihlalleri(tmp_path) == [
        ".scratch/x/issues/02-kapali.md:2: izin verilmeyen değer: kapali",
        ".scratch/x/issues/03-yok.md:1: Status satırı yok",
        ".scratch/x/issues/04-iki.md:3: birden çok Status satırı",
        ".scratch/x/issues/05-eski-done.md:2: izin verilmeyen değer: done",
        ".scratch/x/issues/07-done-bos.md:2: izin verilmeyen değer: done ()",
    ]


def test_yakin_ramak_degerler_reddedilir_bolum_disi_madde_sayilmaz(tmp_path):
    _sozlesme_kopyala(tmp_path)
    izleyici = tmp_path / "docs" / "agents" / "issue-tracker.md"
    izleyici.write_text(
        izleyici.read_text(encoding="utf-8") + "\n## Other\n\n- `zzz`: x\n",
        encoding="utf-8",
    )
    bilet = tmp_path / ".scratch" / "x" / "issues"
    bilet.mkdir(parents=True)
    ornekler = {
        "01-bitisik.md": "# T\n**Status:** done(PR #9)\n",
        "02-acik.md": "# T\n**Status:** done (PR #9\n",
        "03-buyuk.md": "# T\n**Status:** Done (a)\n",
        "04-donex.md": "# T\n**Status:** donex (a)\n",
        "05-artik.md": "# T\n**Status:** done (a) tail\n",
        "06-rol-artik.md": "# T\n**Status:** ready-for-agent extra\n",
        "07-bolum-disi.md": "# T\n**Status:** zzz\n",
        "08-gecerli.md": "# T\n**Status:** done (a)\n",
    }
    for ad, metin in ornekler.items():
        (bilet / ad).write_text(metin, encoding="utf-8")
    assert bilet_ihlalleri(tmp_path) == [
        ".scratch/x/issues/01-bitisik.md:2: izin verilmeyen değer: done(PR #9)",
        ".scratch/x/issues/02-acik.md:2: izin verilmeyen değer: done (PR #9",
        ".scratch/x/issues/03-buyuk.md:2: izin verilmeyen değer: Done (a)",
        ".scratch/x/issues/04-donex.md:2: izin verilmeyen değer: donex (a)",
        ".scratch/x/issues/05-artik.md:2: izin verilmeyen değer: done (a) tail",
        ".scratch/x/issues/06-rol-artik.md:2: izin verilmeyen değer: ready-for-agent extra",
        ".scratch/x/issues/07-bolum-disi.md:2: izin verilmeyen değer: zzz",
    ]


def test_bos_status_degeri_sayilir(tmp_path):
    _sozlesme_kopyala(tmp_path)
    bilet = tmp_path / ".scratch" / "x" / "issues"
    bilet.mkdir(parents=True)
    ornekler = {
        "01-iki-biri-bos.md": "# T\n**Status:** claimed\n**Status:**\n",
        "02-tek-bos.md": "# T\n**Status:**\n",
    }
    for ad, metin in ornekler.items():
        (bilet / ad).write_text(metin, encoding="utf-8")
    assert bilet_ihlalleri(tmp_path) == [
        ".scratch/x/issues/01-iki-biri-bos.md:3: birden çok Status satırı",
        ".scratch/x/issues/02-tek-bos.md:2: izin verilmeyen değer: ",
    ]


def test_gercek_biletler_sozlesmeye_uyar():
    assert bilet_ihlalleri(KOK) == []
