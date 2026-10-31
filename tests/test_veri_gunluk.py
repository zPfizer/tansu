import numpy as np
import pandas as pd
import pytest

from tansu import __main__ as komut
from tansu import kaynak, sinama, veri
from tansu.__main__ import main


def uyeler(tarih, surum="bist30_2026_v1"):
    istek = veri.UyelikIstegi((tarih,), "donemsel_bist30_v1", surum)
    return set(veri.uyelik_hazirla(istek)["gunler"][tarih]["semboller"])


def test_2026_uyeligi_donem_degisimleriyle_30_uye_doner():
    mart, nisan, ekim = uyeler("2026-03-31"), uyeler("2026-04-01"), uyeler("2026-10-01")
    assert len(mart) == len(nisan) == len(ekim) == 30
    assert "ULKER" in mart and "VAKBN" not in mart
    assert "VAKBN" in nisan and "ULKER" not in nisan
    assert "TRMET" in ekim and "DSTKF" not in ekim
    assert "DSTKF" in uyeler("2026-09-30")


def test_2021_2025_uyeligi_30_uye_doner():
    assert len(uyeler("2025-11-21", "bist30_2021_2025_v1")) == 30


@pytest.mark.parametrize(
    "tarih,surum",
    [("2027-01-04", "bist30_2026_v1"), ("2026-01-02", "bist30_2021_2025_v1")],
)
def test_surum_kendi_tarih_araligi_disinda_durur(tarih, surum):
    with pytest.raises(veri.UyelikKapsamHatasi):
        uyeler(tarih, surum)


def test_uyelik_araliklari_eski_kodlari_yeni_koda_cevirir():
    a = veri.uyelik_araliklari()

    def uye(sembol, tarih):
        t = pd.Timestamp(tarih)
        return bool(((a.sembol == sembol) & (a.bas <= t) & (t <= a.son)).any())

    assert not {"KOZAL", "KOZAA"} & set(a.sembol)
    assert uye("TRALT", "2023-01-02") and uye("TRALT", "2026-06-01")
    assert uye("TRMET", "2022-01-03") and not uye("TRMET", "2024-01-02")
    assert uye("TRMET", "2026-10-01")
    assert veri.uyelik_bitisi() == pd.Timestamp("2026-12-31")


def fiyat_satiri(sembol, tarih, kapanis, yuksek=None, dusuk=None):
    yuksek, dusuk = yuksek or kapanis * 1.01, dusuk or kapanis * 0.99
    return {
        "sembol": sembol,
        "tarih": pd.Timestamp(tarih),
        "ham_kapanis": kapanis,
        "ham_aof": kapanis,
        "ham_yuksek": yuksek,
        "ham_dusuk": dusuk,
        "kapanis": kapanis,
        "aof": kapanis,
        "yuksek": yuksek,
        "dusuk": dusuk,
        "hacim": 1000.0,
        "xu100": 9000.0,
    }


def sentetik_anlik():
    gunler = ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"]
    satirlar = [fiyat_satiri("AAA", t, 10.0) for t in gunler]
    satirlar += [
        fiyat_satiri("TRALT", "2024-01-02", 100.0),
        fiyat_satiri("TRALT", "2024-01-03", 110.0, 110.0, 110.0),
        fiyat_satiri("TRALT", "2024-01-05", 105.0),
        fiyat_satiri("TRALT", "2024-01-08", 50.0),
    ]
    olaylar = pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    return veri.Anlik("sentetik", pd.DataFrame(satirlar), olaylar)


def test_gunluk_sozlesmesi_eksik_gun_kilit_karantina_ve_uyelik():
    g = veri.gunluk(sentetik_anlik(), "TRALT")
    assert list(g.columns) == [
        "aof",
        "yuksek",
        "dusuk",
        "kapanis",
        "hacim",
        "ham_yuksek",
        "ham_dusuk",
        "ham_kapanis",
        "kilit_tavan",
        "kilit_taban",
        "tavan_kapanis",
        "karantina",
        "uye",
        "xu100",
    ]
    assert g.index.name == "tarih" and len(g) == 5
    assert np.isnan(g.loc["2024-01-04", "kapanis"])
    assert g["kilit_tavan"].tolist() == [False, True, False, False, False]
    assert g["tavan_kapanis"].tolist() == [False, True, False, False, False]
    assert g["karantina"].tolist() == [False, False, False, False, True]
    assert g["uye"].all()
    # BIST 30 dışı pay da evrende
    assert veri.gunluk(sentetik_anlik(), "AAA")["uye"].all()
    with pytest.raises(veri.VeriHatasi):
        veri.gunluk(sentetik_anlik(), "YOK")


def test_bozuk_gunun_fiyati_hesaba_girmez_karantina_kalir():
    # Bütün BIST'te 287 sembolde 8.311 bozuk gün (fiyat 0 ya da tutarsız OHLC): motor AOF 0'dan dolum yapıyordu.
    a = sentetik_anlik()
    a.fiyat.loc[
        (a.fiyat["sembol"] == "AAA") & (a.fiyat["tarih"] == "2024-01-04"), "aof"
    ] = 0.0
    g = veri.gunluk(a, "AAA")
    assert g.loc["2024-01-04", ["aof", "yuksek", "dusuk", "kapanis"]].isna().all()
    assert g.loc["2024-01-04", "karantina"]
    assert g.loc["2024-01-05", "kapanis"] == 10.0


def test_sinama_evreni_goruntudeki_butun_paylardir():
    assert set(sinama.gunler(sentetik_anlik())) == {"AAA", "TRALT"}


class SahteKaynak:
    def fiyat(self, sembol, bas, son):
        if sembol == "SOKE":
            raise kaynak.KaynakHatasi("SOKE: alınamadı")
        if sembol not in ("AKBNK", "TRALT", "ESKI"):
            return pd.DataFrame(columns=["tarih", *kaynak.ALANLAR.values()])
        satirlar = [fiyat_satiri(sembol, t, 10.0) for t in ("2019-01-02", "2019-01-03")]
        if sembol == "AKBNK":
            satirlar.append(fiyat_satiri(sembol, "2019-01-04", 10.0))
        f = pd.DataFrame(satirlar).drop(columns="sembol")
        return f.assign(pd=1.0, hao_pd=1.0, sermaye=1.0)

    def olaylar(self, sembol):
        return []


def sahte_evren(monkeypatch):
    monkeypatch.setattr(kaynak, "IsYatirim", SahteKaynak)
    monkeypatch.setattr(kaynak, "sirket_kodlari", lambda: pd.Series(["AKBNK"]))
    monkeypatch.setattr(
        kaynak,
        "kapanan_kodlar",
        lambda: pd.DataFrame(columns=["kod", "ad", "tarih", "aciklama"]).astype(
            {"tarih": "datetime64[ns]"}
        ),
    )


def test_veri_budamasi_ayarin_goruntusunu_korur_yarim_gecicileri_siler(
    monkeypatch, tmp_path, capsys
):
    for i in range(11):
        (tmp_path / "ag" / f"2020010{i // 10}-00{i:02d}").mkdir(parents=True)
    (tmp_path / "ag" / "_gecici-20200102-0000").mkdir()
    ayarlar = tmp_path / "stratejiler" / "ayarlar"
    ayarlar.mkdir(parents=True)
    (ayarlar / "gartley.json").write_text(
        '{"veri_kimligi": "20200100-0000"}', encoding="utf-8"
    )
    sahte_evren(monkeypatch)
    assert main(["veri", "--kok", str(tmp_path)]) == 0
    assert "silinen eski görüntü: 1" in capsys.readouterr().out
    assert (tmp_path / "ag" / "20200100-0000").is_dir()
    assert len(list((tmp_path / "ag").glob("2*"))) == 11
    assert not list((tmp_path / "ag").glob("_gecici-*"))


def test_veri_komutu_sembol_tablosu_yazar_ve_on_goruntu_tutar(
    monkeypatch, tmp_path, capsys
):
    for i in range(11):
        (tmp_path / "ag" / f"2020010{i // 10}-00{i:02d}").mkdir(parents=True)
    monkeypatch.setattr(kaynak, "IsYatirim", SahteKaynak)
    monkeypatch.setattr(
        kaynak, "sirket_kodlari", lambda: pd.Series(["AKBNK", "GARAN", "SOKE", "TRALT"])
    )
    kapanan = pd.DataFrame(
        {
            "kod": ["ESKI", "COKESKI"],
            "ad": ["", ""],
            "tarih": pd.to_datetime(["2020-05-04", "2015-01-05"]),
            "aciklama": ["", ""],
        }
    )
    monkeypatch.setattr(kaynak, "kapanan_kodlar", lambda: kapanan)
    assert main(["veri", "--kok", str(tmp_path)]) == 0
    cikti = capsys.readouterr().out
    assert "silinen eski görüntü: 2" in cikti
    goruntuler = sorted((tmp_path / "ag").glob("2*"))
    assert len(goruntuler) == komut.SAKLANAN_GORUNTU
    satirlar = {s.split()[0]: s for s in cikti.splitlines()[2:]}
    assert satirlar["AKBNK"].split()[1:] == ["2019-01-02", "2019-01-04", "3", "tamam"]
    assert satirlar["TRALT"].endswith("son gün eksik")
    assert satirlar["SOKE"].endswith("inmedi")
    assert satirlar["GARAN"].endswith("kaynak boş")
    assert (
        "ESKI" in satirlar
    )  # 2019'dan sonra kapanan pay evrende (hayatta kalan yanlılığı yok)
    assert (
        "COKESKI" not in satirlar
    )  # veri başlangıcından önce kapanan pay evrende değil
    assert (goruntuler[-1] / "kapanan.csv").exists()
    assert "önbellek: 0 artımlı, 4 tam" in cikti  # boş kaynak da tam iniş sayılır
    assert (tmp_path / "onbellek" / "fiyat-20190101" / "AKBNK.fiyat.parquet").exists()
