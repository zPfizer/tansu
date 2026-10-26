import pandas as pd

from tansu import __main__ as komut
from tansu import veri
from tansu.__main__ import main
from tests.sentetik import gartley_yolu, gun_tablosu


def sentetik_anlik():
    g = gun_tablosu(gartley_yolu(), bas="2022-01-03")
    fiyat = g[["aof", "yuksek", "dusuk", "kapanis", "hacim", "xu100"]].copy()
    fiyat["ham_aof"], fiyat["ham_yuksek"] = g["aof"], g["yuksek"]
    fiyat["ham_dusuk"], fiyat["ham_kapanis"] = g["dusuk"], g["kapanis"]
    fiyat = fiyat.reset_index().assign(sembol="AKBNK")
    olaylar = pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    return veri.Anlik("20260101-0000", fiyat, olaylar)


def test_sina_raporu_yazar_ve_durumu_sinandi_yapar(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(komut, "son_anlik", lambda kok: sentetik_anlik())
    (tmp_path / "stratejiler").mkdir()
    (tmp_path / "stratejiler" / "durum.csv").write_text(
        "ad,durum,tarih,not\ngartley,taslak,2026-10-26,\n", encoding="utf-8"
    )
    assert main(["sina", "gartley"]) == 0
    assert "1 sinyal, 1 dolum" in capsys.readouterr().out
    html = (tmp_path / "rapor" / "gartley" / "sinama.html").read_text(encoding="utf-8")
    for baslik in ("Dönem tablosu", "2021", "2025", "Bütün yıllar", "Kümülatif R"):
        assert baslik in html
    assert "n/a (N = 1)" in html
    islemler = pd.read_csv(tmp_path / "rapor" / "gartley" / "islemler.csv")
    assert islemler.loc[0, "cikis_nedeni"] == "hedef2" and islemler.loc[0, "R"] > 0
    assert (tmp_path / "rapor" / "gartley" / "ozet.md").exists()
    durum = (tmp_path / "stratejiler" / "durum.csv").read_text(encoding="utf-8")
    assert "gartley,sinandi," in durum
