import dataclasses
import json

import pandas as pd
import pytest

from tansu import __main__ as komut
from tansu import ayar, rapor, sinama, veri
from tansu.__main__ import main
from tansu.stratejiler import STRATEJILER
from tests.sentetik import gartley_yolu, gun_tablosu, ortalama_yolu, piyasa


def sentetik_anlik(yol=None):
    g = gun_tablosu(gartley_yolu() if yol is None else yol, bas="2022-01-03")
    fiyat = g[["aof", "yuksek", "dusuk", "kapanis", "hacim", "xu100"]].copy()
    fiyat["ham_aof"], fiyat["ham_yuksek"] = g["aof"], g["yuksek"]
    fiyat["ham_dusuk"], fiyat["ham_kapanis"] = g["dusuk"], g["kapanis"]
    fiyat = fiyat.reset_index().assign(sembol="AKBNK")
    olaylar = pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    return veri.Anlik("20260101-0000", fiyat, olaylar)


@pytest.fixture
def ortam(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "stratejiler").mkdir()

    def kur(ad, durum="taslak", yol=None, strateji=None):
        s = STRATEJILER[ad]
        tek = dataclasses.replace(s, aralik={k: (s.varsayilan[k],) for k in s.aralik})
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
    islemler = pd.read_csv(klasor / "islemler.csv")
    assert islemler.loc[0, "cikis_nedeni"] == "çıkış sinyali"
    assert pd.isna(islemler.loc[0, "R"])
    assert "Toplam %" in (klasor / "ozet.md").read_text(encoding="utf-8")


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
    assert icerik["parametreler"] == dict(STRATEJILER["gartley"].varsayilan)
    assert icerik["puanli"] is False and icerik["suzgecler"] == ["nabiz"]
    assert "gartley,yetersiz-ornek," in durum(tmp_path)
    html = (tmp_path / "rapor" / "gartley" / "sinama.html").read_text(encoding="utf-8")
    assert rapor.ORNEK_AZ in html and "Parametreler (ayarlı" in html
    assert "ayar: " in capsys.readouterr().out


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
