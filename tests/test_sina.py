import dataclasses
import datetime as dt
import json
import os
from html import escape as html_kacis
from pathlib import Path

import pandas as pd
import pytest

from tansu import __main__ as komut
from tansu import ayar, islem, montecarlo, rapor, sinama
from tansu.__main__ import main
from tansu.strateji import bos_sinyal
from tansu.stratejiler import STRATEJILER
from tests.sentetik import (
    SABIT,
    anlik,
    gartley_yolu,
    gun_tablosu,
    ortalama_yolu,
    piyasa,
)


TEMIZ = sinama.VeriKapisi(0.0, 0.0, 0, (), ())


def sentetik_anlik(yol=None):
    yol = gartley_yolu() if yol is None else yol
    return anlik({"AKBNK": gun_tablosu(yol, bas="2022-01-03")})


@pytest.fixture
def ortam(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "stratejiler").mkdir()

    def kur(ad, durum="taslak", yol=None, strateji=None):
        """Kurulan strateji `SABIT`i varsayılan ve tek noktalı aralık olarak taşır."""
        s, v = STRATEJILER[ad], SABIT[ad]
        tek = dataclasses.replace(
            s, varsayilan=v, aralik={k: (v[k],) for k in s.aralik}
        )
        monkeypatch.setitem(komut.STRATEJILER, ad, strateji or tek)
        monkeypatch.setattr(komut, "son_anlik", lambda kok: sentetik_anlik(yol))
        (tmp_path / "stratejiler" / "durum.csv").write_text(
            f"ad,durum,tarih,not\n{ad},{durum},2026-10-26,\n", encoding="utf-8"
        )

    return kur


def durum(tmp_path):
    return (tmp_path / "stratejiler" / "durum.csv").read_text(encoding="utf-8")


def test_sina_raporu_yazar_ve_durumu_sinandi_yapar(ortam, tmp_path, capsys):
    ortam("gartley")
    assert main(["sina", "gartley"]) == 0
    assert "1 sinyal, 1 dolum" in capsys.readouterr().out
    html = (tmp_path / "rapor" / "gartley" / "sinama.html").read_text(encoding="utf-8")
    for baslik in ("Dönem tablosu", "2021", "2025", "Bütün yıllar", "Kümülatif R"):
        assert baslik in html
    for baslik in ("İleri yürüme", "Saklı dönem", "Izgara sonucu", rapor.ACIKLAMA):
        assert baslik in html
    assert all(w.ad in html for w in ayar.PENCERELER)
    assert "Parametreler (varsayılan)" in html and "n/a (N = 1)" in html
    islemler = pd.read_csv(tmp_path / "rapor" / "gartley" / "islemler.csv")
    assert islemler.loc[0, "cikis_nedeni"] == "hedef2" and islemler.loc[0, "R"] > 0
    assert "Saklı dönem" in (tmp_path / "rapor" / "gartley" / "ozet.md").read_text(
        encoding="utf-8"
    )
    assert "gartley,sinandi," in durum(tmp_path)
    assert not (tmp_path / "stratejiler" / "ayarlar").exists()
    tohum = str(montecarlo.TOHUM)
    for baslik in ("Monte Carlo", tohum, "Batma riski", "Bayraklar", rapor.ONAY_YOK):
        assert baslik in html
    ozet = (tmp_path / "rapor" / "gartley" / "ozet.md").read_text(encoding="utf-8")
    assert tohum in ozet and "örnek az (N = 0)" in ozet


@pytest.mark.parametrize(
    ("bozuk", "beklenen"),
    [
        (0, "Veri kapısı: temiz. Karantina oranı 0.00% (eşik 1%)"),
        (2, "Veri kapısı: SORUNLU (karantina oranı > %1). Karantina oranı 1.65%"),
    ],
)
def test_sina_veri_kapisi_kalsa_da_raporu_yazar_ve_sorunlu_der(
    ortam, tmp_path, monkeypatch, capsys, bozuk, beklenen
):
    """TASARIM 5.13: karantina hisse-gün oranı %1'i aşarsa koşu yine yazılır, rapor SORUNLU der ve oranları yazar.
    Retro 30.10 bulgu 2: kapı `veri.py`'de vardı ama hiçbir komut onu çağırmıyordu."""
    ortam("gartley")
    g = gun_tablosu(gartley_yolu(), bas="2022-01-03")
    kotu = g.index[100 : 100 + bozuk]
    g.loc[kotu, "kapanis"] = g.loc[kotu, "yuksek"] + 1  # kapanış > yüksek: satır ihlali
    monkeypatch.setattr(komut, "son_anlik", lambda kok: anlik({"AKBNK": g}))
    assert main(["sina", "gartley"]) == 0
    assert beklenen in capsys.readouterr().out
    klasor = tmp_path / "rapor" / "gartley"
    assert beklenen in (klasor / "ozet.md").read_text(encoding="utf-8")
    html = (klasor / "sinama.html").read_text(encoding="utf-8")
    assert html_kacis(beklenen) in html


def test_sina_sinif_b_ileri_getiri_tablosu_ve_yuzde_birimi_yazar(
    ortam, tmp_path, capsys
):
    ortam("ortalama-kesisim", yol=ortalama_yolu())
    assert main(["sina", "ortalama-kesisim"]) == 0
    cikti = capsys.readouterr().out
    assert "1 sinyal, 1 dolum, toplam " in cikti and " %\n" in cikti
    klasor = tmp_path / "rapor" / "ortalama-kesisim"
    html = (klasor / "sinama.html").read_text(encoding="utf-8")
    for baslik in ("İleri getiri", "Ufuk (gün)", "Kümülatif %", "Toplam %"):
        assert baslik in html
    assert "Seviyelerin isabeti" not in html and "n/a (N = 1)" in html
    assert "Monte Carlo" in html and "Batma riski" not in html
    islemler = pd.read_csv(klasor / "islemler.csv")
    assert islemler.loc[0, "cikis_nedeni"] == "çıkış sinyali"
    assert pd.isna(islemler.loc[0, "R"])
    assert "Toplam %" in (klasor / "ozet.md").read_text(encoding="utf-8")


def test_sina_islem_yoksa_islemler_csv_sutun_basligini_yazar(ortam, tmp_path):
    g = STRATEJILER["gartley"]
    bos = dataclasses.replace(
        g,
        hesapla=lambda gun, p: bos_sinyal(gun.index),
        aralik={k: (g.varsayilan[k],) for k in g.aralik},
    )
    ortam("gartley", strateji=bos)
    assert main(["sina", "gartley"]) == 0
    tablo = pd.read_csv(tmp_path / "rapor" / "gartley" / "islemler.csv")
    assert tablo.empty
    assert list(tablo.columns) == list(islem.kayit_sutunlari(g.cikis))


def baska_programda_acik(monkeypatch, hedef):
    gercek_replace, gercek_csv = os.replace, pd.DataFrame.to_csv

    def replace(src, dst, *a, **k):
        if Path(dst).name == hedef:
            raise PermissionError(13, "Erişim engellendi", str(src), None, str(dst))
        return gercek_replace(src, dst, *a, **k)

    def to_csv(self, yol=None, *a, **k):
        if yol is not None and Path(yol).name == hedef:
            raise PermissionError(13, "Erişim engellendi", str(yol))
        return gercek_csv(self, yol, *a, **k)

    monkeypatch.setattr(os, "replace", replace)
    monkeypatch.setattr(pd.DataFrame, "to_csv", to_csv)


RAPOR_KLASORU = Path("rapor", "gartley")
AYAR_JSON = Path("stratejiler", "ayarlar", "gartley.json")


@pytest.mark.parametrize(
    ("komut_adi", "baslangic", "yol", "yazilan"),
    [
        ("sina", "taslak", Path("stratejiler", "durum.csv"), (RAPOR_KLASORU,)),
        ("sina", "taslak", RAPOR_KLASORU / "islemler.csv", ()),
        ("ayarla", "sinandi", AYAR_JSON, (RAPOR_KLASORU,)),
        (
            "ayarla",
            "sinyalde",
            Path("stratejiler", "durum.csv"),
            (RAPOR_KLASORU, AYAR_JSON),
        ),
    ],
)
def test_yazilacak_dosya_baska_programda_aciksa_acik_mesaj_ve_cikis_1(
    ortam, tmp_path, monkeypatch, capsys, komut_adi, baslangic, yol, yazilan
):
    ortam("gartley", durum=baslangic)
    once = (tmp_path / "stratejiler" / "durum.csv").read_bytes()
    baska_programda_acik(monkeypatch, yol.name)
    assert main([komut_adi, "gartley"]) == 1
    hata = capsys.readouterr().err
    assert f"tansu {komut_adi}: {yol} " in hata and "durum.csv değişmedi" in hata
    assert all(str(p) in hata for p in yazilan)
    assert yazilan or "yazdıkları" not in hata
    assert all((tmp_path / p).exists() for p in yazilan)
    assert (tmp_path / "stratejiler" / "durum.csv").read_bytes() == once
    assert not list(tmp_path.rglob("*.tmp"))


def test_ayar_json_bozuksa_ayarla_yazilan_rapor_klasorunu_soyler(
    ortam, tmp_path, capsys
):
    ortam("gartley", durum="sinandi")
    json_yolu = tmp_path / AYAR_JSON
    json_yolu.parent.mkdir(parents=True)
    json_yolu.write_text("{bozuk", encoding="utf-8")
    once = (tmp_path / "stratejiler" / "durum.csv").read_bytes()
    assert main(["ayarla", "gartley"]) == 1
    hata = capsys.readouterr().err
    assert f"tansu ayarla: {AYAR_JSON}: geçersiz JSON" in hata
    assert str(RAPOR_KLASORU) in hata
    assert (tmp_path / RAPOR_KLASORU / "sinama.html").exists()
    assert json_yolu.read_text(encoding="utf-8") == "{bozuk"
    assert (tmp_path / "stratejiler" / "durum.csv").read_bytes() == once


def test_okunacak_durum_dosyasi_kilitliyse_yazilamadi_demez(
    ortam, tmp_path, monkeypatch, capsys
):
    ortam("gartley")
    yol = Path("stratejiler", "durum.csv")
    once = (tmp_path / yol).read_bytes()
    gercek_open = Path.open

    def open_(self, mode="r", *a, **k):
        if mode == "r" and self.name == yol.name:
            raise PermissionError(13, "Erişim engellendi", str(self))
        return gercek_open(self, mode, *a, **k)

    monkeypatch.setattr(Path, "open", open_)
    assert main(["sina", "gartley"]) == 1
    hata = capsys.readouterr().err
    assert f"tansu sina: {yol} " in hata and "durum.csv değişmedi" in hata
    assert "yazılamadı" not in hata
    assert (tmp_path / yol).read_bytes() == once
    assert not (tmp_path / "rapor").exists()


def test_ayarla_puanli_nokta_yoksa_varsayilanlari_yazar_suzgeci_korur(
    ortam, tmp_path, capsys
):
    ortam("gartley", durum="sinandi")
    ayarlar = tmp_path / "stratejiler" / "ayarlar"
    ayarlar.mkdir()
    (ayarlar / "gartley.json").write_text(
        '{"parametreler": {}, "suzgecler": ["nabiz"]}', encoding="utf-8"
    )
    assert main(["ayarla", "gartley"]) == 0
    icerik = json.loads((ayarlar / "gartley.json").read_text(encoding="utf-8"))
    assert icerik["parametreler"] == dict(komut.STRATEJILER["gartley"].varsayilan)
    assert icerik["puanli"] is False and icerik["suzgecler"] == ["nabiz"]
    assert "gartley,yetersiz-ornek," in durum(tmp_path)
    html = (tmp_path / "rapor" / "gartley" / "sinama.html").read_text(encoding="utf-8")
    assert rapor.ORNEK_AZ in html and "Parametreler (ayarlı" in html
    assert "ayar: " in capsys.readouterr().out


@pytest.mark.slow
def test_ayarla_puanli_secimle_ayarlandi_yapar_sinyaldeyse_onay_ister(
    ortam, tmp_path, monkeypatch, capsys
):
    kesisim = dataclasses.replace(
        STRATEJILER["ortalama-kesisim"],
        varsayilan={"ortalama": "SMA", "cift": "9/21", "teyit_gun": 0},
        aralik={"teyit_gun": (0, 2)},
    )
    ortam("ortalama-kesisim", durum="sinyalde", strateji=kesisim)
    monkeypatch.setattr(sinama, "gunler", lambda anlik: piyasa(sembol=2))
    assert main(["ayarla", "ortalama-kesisim"]) == 0
    cikti = capsys.readouterr().out
    assert (
        "tansu onayla ortalama-kesisim" in cikti and "ızgara 2 nokta, puanlı 2" in cikti
    )
    assert "ortalama-kesisim,ayarlandi," in durum(tmp_path)
    assert json.loads(
        (tmp_path / "stratejiler" / "ayarlar" / "ortalama-kesisim.json").read_text(
            encoding="utf-8"
        )
    )["puanli"]
    assert main(["sina", "ortalama-kesisim"]) == 0
    assert "ortalama-kesisim,ayarlandi," in durum(tmp_path)
    html = (tmp_path / "rapor" / "ortalama-kesisim" / "sinama.html").read_text(
        encoding="utf-8"
    )
    assert "Parametreler (ayarlı" in html and "saklı döneme ulaşmıyor" not in html
    assert "Rastgele giriş kıyası" in html and "yüzdelik" in html
    assert "rastgele giriş yüzdeliği n/a" not in capsys.readouterr().out


@pytest.mark.slow
def test_hazirla_parametreyi_kaynagina_gore_secer_ve_dosya_yazmaz(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    kesisim = dataclasses.replace(
        STRATEJILER["ortalama-kesisim"],
        varsayilan={"ortalama": "SMA", "cift": "9/21", "teyit_gun": 0},
        aralik={"teyit_gun": (0, 2)},
    )
    gunler = piyasa(sembol=2)
    ortak = {"kimlik": "t", "kapi": TEMIZ, "sinanan": 1}

    ayarli = rapor.hazirla(kesisim, gunler, ayarla=True, okunan=None, **ortak)
    assert ayarli.parametre == ayarli.yuruyus.son.parametre
    assert ayarli.ayar_tarihi == dt.date.today().isoformat()
    assert (ayarli.kimlik, ayarli.sinanan) == ("t", 1)

    okunan = ayar.Okunan(
        {"ortalama": "SMA", "cift": "9/21", "teyit_gun": 2}, "2026-01-02"
    )
    kayitli = rapor.hazirla(kesisim, gunler, ayarla=False, okunan=okunan, **ortak)
    assert (kayitli.parametre, kayitli.ayar_tarihi) == (
        okunan.parametreler,
        "2026-01-02",
    )

    varsayilan = rapor.hazirla(kesisim, gunler, ayarla=False, okunan=None, **ortak)
    assert varsayilan.parametre == kesisim.varsayilan
    assert varsayilan.ayar_tarihi is None
    assert not list(tmp_path.iterdir())


def kesisim_sinamasi(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    kesisim = dataclasses.replace(
        STRATEJILER["ortalama-kesisim"],
        varsayilan={"ortalama": "SMA", "cift": "9/21", "teyit_gun": 0},
        aralik={"teyit_gun": (0, 2)},
    )
    return rapor.hazirla(
        kesisim,
        piyasa(sembol=2),
        kimlik="t",
        kapi=TEMIZ,
        sinanan=1,
        ayarla=True,
        okunan=None,
    )


@pytest.mark.slow
@pytest.mark.parametrize(
    ("n", "beklenen"),
    [
        (sinama.EN_AZ, "n/a (uygun rastgele gün ya da şablon yok)"),
        (5, "n/a (N = 5)"),
    ],
)
def test_konsol_rastgele_giris_yoksa_raporla_ayni_nedeni_yazar(
    tmp_path, monkeypatch, n, beklenen
):
    s = kesisim_sinamasi(tmp_path, monkeypatch)
    s = dataclasses.replace(s, mc=dataclasses.replace(s.mc, n=n, rastgele=None))
    assert rapor.konsol(s)[4].endswith(f"rastgele giriş yüzdeliği {beklenen}")


@pytest.mark.slow
def test_konsol_olcu_satirlarini_sinamadan_uretir(tmp_path, monkeypatch):
    s = kesisim_sinamasi(tmp_path, monkeypatch)
    satirlar = rapor.konsol(s)
    assert len(satirlar) == 6
    assert "ızgara 2 nokta, puanlı 2" in satirlar[1]
    assert s.sakli_var and satirlar[3].startswith("saklı dönem ")
    assert satirlar[4].startswith("Monte Carlo: tohum ")
    erken = dataclasses.replace(s, sakli_son=sinama.SAKLI_BAS - pd.Timedelta(days=1))
    assert not erken.sakli_var
    assert rapor.konsol(erken)[3] == "saklı dönem: veri saklı döneme ulaşmıyor"


@pytest.mark.slow
def test_yaz_metin_islevlerinin_metnini_oldugu_gibi_yazar(tmp_path, monkeypatch):
    s = kesisim_sinamasi(tmp_path, monkeypatch)
    html, md = rapor.html_metni(s), rapor.md_metni(s)
    assert not list(tmp_path.iterdir())
    assert "Dönem tablosu" in html and md.startswith("# ortalama-kesisim: sınama özeti")
    klasor = rapor.yaz(s, tmp_path / "r").parent
    assert (klasor / "sinama.html").read_bytes() == html.encode("utf-8")
    assert (klasor / "ozet.md").read_bytes() == md.encode("utf-8")
    assert (klasor / "islemler.csv").exists()


def test_sina_bozuk_jsonu_izgaradan_once_reddeder(ortam, tmp_path, monkeypatch):
    ortam("gartley")
    (tmp_path / "stratejiler" / "ayarlar").mkdir()
    (tmp_path / "stratejiler" / "ayarlar" / "gartley.json").write_text("[]", "utf-8")
    monkeypatch.setattr(ayar, "yuru", lambda *a, **k: pytest.fail("ızgara koştu"))
    assert main(["sina", "gartley"]) == 1
    assert not (tmp_path / "rapor").exists()


def test_sinanan_strateji_sayisi_beklemedekini_saymaz(ortam, tmp_path):
    ortam("gartley")
    with (tmp_path / "stratejiler" / "durum.csv").open("a", encoding="utf-8") as f:
        f.write("eski,beklemede,2026-10-26,\nbaska,sinandi,2026-10-26,\n")
    assert main(["sina", "gartley"]) == 0
    html = (tmp_path / "rapor" / "gartley" / "sinama.html").read_text(encoding="utf-8")
    assert "Şimdiye kadar sınanan strateji: 2." in html


def test_ayarla_beklemedeki_stratejiyi_reddeder(ortam, tmp_path):
    ortam("gartley", durum="beklemede")
    assert main(["ayarla", "gartley"]) == 1
    assert not (tmp_path / "stratejiler" / "ayarlar").exists()
    assert "gartley,beklemede," in durum(tmp_path)
