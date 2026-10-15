"""`kosu()` yüzü: kural kaydı, deneme günlüğü, başlangıç denetimi (TASARIM 5.8, 5.11).

Veri: 8 günlük sentetik seri (tests/test_motor.py'deki elle hesap): sinyal gün 5, giriş gün 6 AOF 104,
çıkış gün 7 kapanış 105 (veri sonu). Tek işlem.
"""

import datetime as dt
import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd
import pytest

from tansu import aileler, kayit, motor, veri
from tests.test_veri import SahteBorsapy, SahteKaynak, satir

P = aileler.Parametre(
    periyotlar=(1, 2), esik=0.005, min_gun=3, pencere=3, isinma=4, sma_n=2
)
ATR_N = 2
TEMIZ = lambda: ("abc123", False)  # noqa: E731
KIRLI = lambda: ("abc123", True)  # noqa: E731


def anlik_hazirla(tmp_path, son_kapanis=105.0, dakika=30):
    # İlk gün Şubat'ın son günü: Mart evreni ona dayanır, sinyal günü (gün 5) evrendedir (TASARIM 5.6 evren süzgeci, bilet 11).
    gunler = pd.bdate_range("2026-02-27", periods=8)
    kap = [100.0] * 5 + [103.0, 104.0, son_kapanis]
    yuk = [100.5, 100.5, 101, 100.5, 100.5, 103.5, 104.5, 105.5]
    fiyat = []
    for g, k, y in zip(gunler, kap, yuk):
        s = satir(g, k, k)
        s.update(yuksek=y, ham_yuksek=y, dusuk=k - 0.5, ham_dusuk=k - 0.5)
        fiyat.append(s)
    return veri.indir(
        ["XXXX"],
        tmp_path,
        SahteKaynak({"XXXX": fiyat}, {"XXXX": []}),
        simdi=dt.datetime(2026, 10, 5, 19, dakika),
        borsapy=SahteBorsapy([("2025-01-01", 40.0)], {"XXXX": "X"}),
    )  # simülatör faiz ister (bilet 10)


def satirlar():
    yol = kayit.KAYIT_DIZINI / "deneme.jsonl"
    return [
        s
        for s in map(json.loads, yol.read_text(encoding="utf-8").splitlines())
        if s["tur"] != "destek"
    ]  # destek: bilet 13


def calistir(tmp_path, kimlik, **kw):
    kw.setdefault("git", TEMIZ)
    return kayit.kosu(kimlik, tmp_path, p=P, atr_n=ATR_N, **kw)


def test_kural_kaydi_yoksa_tek_satirla_durur_ve_gunluk_yazilmaz(tmp_path):
    kimlik = anlik_hazirla(tmp_path)
    with pytest.raises(kayit.KayitHatasi, match="Kural kaydı yok"):
        calistir(tmp_path, kimlik)
    assert not (kayit.KAYIT_DIZINI / "deneme.jsonl").exists()


def test_parametre_degisince_hash_uyusmaz_ve_durur(tmp_path):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    baska = aileler.Parametre(
        periyotlar=(1, 2), esik=0.006, min_gun=3, pencere=3, isinma=4, sma_n=2
    )
    with pytest.raises(kayit.KayitHatasi, match="uyuşmuyor"):
        kayit.kosu(kimlik, tmp_path, p=baska, atr_n=ATR_N, git=TEMIZ)
    assert [s["olay"] for s in satirlar()] == ["kayit"]


def test_kod_listesi_degisince_hash_uyusmaz_ve_durur(tmp_path, monkeypatch):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    monkeypatch.setattr(kayit, "KOD_DOSYALARI", kayit.KOD_DOSYALARI[:-1])
    with pytest.raises(kayit.KayitHatasi, match="uyuşmuyor"):
        calistir(tmp_path, kimlik)


def test_kosu_basladi_ve_bitti_satiri_yazar_ve_islemi_dondurur(tmp_path):
    kimlik = anlik_hazirla(tmp_path)
    kural = kayit.kayitla(P, ATR_N)
    sonuc = calistir(tmp_path, kimlik)
    assert len(sonuc["islemler"]) == 1 and sonuc["dusen"] == 0
    t = sonuc["islemler"].iloc[0]
    assert (t.giris_fiyat, t.cikis_fiyat, t.neden) == (104.0, 105.0, "veri_sonu")
    kayit_s, basladi, bitti = satirlar()
    assert [kayit_s["olay"], basladi["olay"], bitti["olay"]] == [
        "kayit",
        "basladi",
        "bitti",
    ]
    assert kayit_s["tur"] == "kayit"
    assert basladi["tur"] == bitti["tur"] == "deneme"
    assert basladi["kosu_id"] == bitti["kosu_id"] == sonuc["kosu_id"]
    assert basladi["kural_id"] == kural["kural_id"] == bitti["kural_id"]
    assert basladi["anlik"] == kimlik
    ozet = hashlib.sha256(
        (Path(tmp_path) / "ag" / kimlik / "manifest.json").read_bytes()
    ).hexdigest()
    assert basladi["manifest_sha256"] == ozet
    assert basladi["param"]["aile"]["esik"] == 0.005 and basladi["param"]["atr_n"] == 2
    assert basladi["git_commit"] == "abc123"
    assert {"python", "lock_sha256", "pandas"} <= set(basladi["ortam"])
    assert (bitti["islem_sayisi"], bitti["dusen_sinyal"]) == (1, 0)
    assert bitti["ozet"] == sonuc["ozet"]


def test_temiz_agacta_resmi_kirli_agacta_resmi_degil(tmp_path):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    kayit.denetim_yaz(
        {"gecti": True}, P, ATR_N
    )  # ilk resmi koşu için geçen boru hattı denetimi şart (TASARIM 5.12)
    calistir(tmp_path, kimlik, resmi=True, git=TEMIZ)
    calistir(
        tmp_path, kimlik, resmi=False, git=KIRLI
    )  # kirli ağaçta resmi istenirse koşu durur (TASARIM 5.11)
    calistir(tmp_path, kimlik, resmi=False, git=TEMIZ)
    b = [s for s in satirlar() if s["olay"] == "basladi"]
    assert [(s["resmi"], s["kirli"]) for s in b] == [
        (True, False),
        (False, True),
        (False, False),
    ]


def test_bitti_satiri_olmayan_basladi_deneme_sayilir(tmp_path, monkeypatch):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    calistir(tmp_path, kimlik)

    def coker(*a, **k):
        raise RuntimeError("koşu yarıda")

    monkeypatch.setattr(motor, "sinama", coker)
    with pytest.raises(RuntimeError):
        calistir(tmp_path, kimlik)
    assert [s["olay"] for s in satirlar()][-1] == "basladi"
    assert kayit.deneme_sayisi() == 2  # kayıt satırı ve destek koşuları sayılmaz


def test_ayni_tohum_ve_ayni_anlik_goruntu_ayni_ozeti_verir(tmp_path):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    a = calistir(tmp_path, kimlik, tohum=7)
    b = calistir(tmp_path, kimlik, tohum=7)
    assert a["ozet"] == b["ozet"] and a["kosu_id"] != b["kosu_id"]
    assert satirlar()[1]["tohum"] == 7


def test_baska_veri_baska_ozet_verir(tmp_path):
    kayit.kayitla(P, ATR_N)
    a = calistir(tmp_path, anlik_hazirla(tmp_path, 105.0))
    b = calistir(tmp_path, anlik_hazirla(tmp_path, 106.0, dakika=31))
    assert a["ozet"] != b["ozet"]


def test_bozuk_manifest_kosuyu_baslamadan_durdurur(tmp_path):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    (tmp_path / "ag" / kimlik / "fiyat.parquet").write_bytes(b"bozuk")
    with pytest.raises(veri.VeriHatasi, match="manifest"):
        calistir(tmp_path, kimlik)
    assert [s["olay"] for s in satirlar()] == ["kayit"]


def test_gunluk_yalniz_eklenir_onceki_satirlar_degismez(tmp_path):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    calistir(tmp_path, kimlik)
    once = (kayit.KAYIT_DIZINI / "deneme.jsonl").read_text(encoding="utf-8")
    calistir(tmp_path, kimlik)
    sonra = (kayit.KAYIT_DIZINI / "deneme.jsonl").read_text(encoding="utf-8")
    assert sonra.startswith(once) and len(sonra) > len(once)


def test_resmi_durumlar_yalniz_ailenin_resmi_durum_satirlarini_sirayla_verir(tmp_path):
    for aile, durum, resmi in [
        ("a", "Deneme", True),
        ("b", "Kâğıt", True),
        ("a", "Kâğıt", False),
        ("a", "Kâğıt", True),
    ]:
        kayit._yaz(
            {
                "tur": "durum",
                "olay": "durum",
                "aile": aile,
                "durum": durum,
                "resmi": resmi,
            }
        )
    kayit._yaz({"tur": "kayit", "olay": "kayit"})
    assert [s["durum"] for s in kayit.resmi_durumlar("a")] == ["Deneme", "Kâğıt"]
    assert kayit.resmi_durumlar("yok") == []


def test_her_tansu_dosyasi_kod_listesinde_ya_da_hash_disinda():
    dosyalar = {p.name for p in Path(kayit.__file__).parent.glob("*.py")}
    assert dosyalar == set(kayit.KOD_DOSYALARI) | set(kayit.HASH_DISI)
    assert not set(kayit.KOD_DOSYALARI) & set(kayit.HASH_DISI)
    # TASARIM 5.11 kuralı: işlem, dolum, kapı, evren, p ya da kabul kararını değiştirebilen her modül listede.
    assert set(kayit.KOD_DOSYALARI) == {
        "aileler.py",
        "cift.py",
        "ciftbolme.py",
        "evren.py",
        "gostergeler.py",
        "istatistik.py",
        "kayit.py",
        "motor.py",
        "saglamlik.py",
        "simulator.py",
        "veri.py",
    }


def test_komutlar_kayit_ve_sinama(tmp_path, capsys):
    from tansu.__main__ import main

    kok = str(tmp_path)
    kimlik = anlik_hazirla(tmp_path)
    assert main(["sinama", "--kok", kok]) == 1
    assert "Kural kaydı yok" in capsys.readouterr().err
    assert main(["kayit"]) == 0
    # Varsayılan parametreyle 8 günlük seride işlem yok; komut yine de başlar ve biter.
    assert main(["sinama", "--kok", kok, "--kimlik", kimlik]) == 0
    # Bilet 12: koşu sonunda her aile için bir `durum` satırı da yazılır (K1, Holm, kabul).
    assert [s["olay"] for s in satirlar()] == [
        "kayit",
        "basladi",
        "bitti",
        "durum",
        "durum",
    ]
    assert (
        satirlar()[1]["tekrar"] == 200
        and satirlar()[2]["tekrar"] == 200
        and not satirlar()[2]["son"]
    )


def test_sinama_son_tam_tekrari_calistirir_ve_gunluge_yazar(
    tmp_path, monkeypatch, capsys
):
    # Tam B = max(taban, çarpan · m); m = 2 (iki yeni aile). Taban 7, çarpan 1 -> 7; geliştirmede 200.
    from tansu.__main__ import main

    monkeypatch.setattr(kayit, "TAM_TABAN", 7)
    monkeypatch.setattr(kayit, "TAM_CARPAN", 1)
    kimlik = anlik_hazirla(tmp_path)
    assert main(["kayit"]) == 0
    assert main(["sinama", "--kok", str(tmp_path), "--kimlik", kimlik, "--son"]) == 0
    _, basladi, bitti, _, _ = satirlar()
    assert (basladi["tekrar"], basladi["son"], bitti["tekrar"], bitti["son"]) == (
        7,
        True,
        7,
        True,
    )
    assert "K1 ema_sikismasi: p" in capsys.readouterr().out


def test_kod_hashi_yorum_ve_bosluktan_etkilenmez(tmp_path, monkeypatch):
    # TASARIM 5.8: kod hash'i yorum ve boşluk değişince aynı kalır.
    paket = tmp_path / "paket"
    paket.mkdir()
    for ad in kayit.KOD_DOSYALARI:
        shutil.copyfile(kayit.PAKET / ad, paket / ad)
    monkeypatch.setattr(kayit, "PAKET", paket)
    once = kayit.kayitla(P, ATR_N)
    yol = paket / "motor.py"
    metin = yol.read_text(encoding="utf-8")
    yol.write_text(
        "# Yalnız açıklama değişti.\n\n"
        + metin.replace("import pandas as pd", "import  pandas  as  pd"),
        encoding="utf-8",
    )
    sonra = kayit.kayitla(P, ATR_N)
    assert sonra["kod_hash"] == once["kod_hash"]
    assert sonra["kural_id"] == once["kural_id"]
    # Anlamlı değişiklik kontrolü: fonksiyon adı değişirse aynı hash kabul edilmez.
    yol.write_text(
        metin.replace("def bekleyen(", "def yeni_bekleyen("), encoding="utf-8"
    )
    assert kayit.kayitla(P, ATR_N)["kod_hash"] != once["kod_hash"]


def test_her_yeni_gunluk_satiri_sema_1_tasir_ve_okuyucu_sema_siz_satiri_okur(tmp_path):
    kayit.kayitla(P, ATR_N)
    kayit.denetim_yaz({"gecti": True}, P, ATR_N)
    yol = kayit.KAYIT_DIZINI / "deneme.jsonl"
    ham = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines()]
    assert [(s["tur"], s["sema"]) for s in ham] == [("kayit", 1), ("destek", 1)]
    yol.write_text(
        json.dumps({"tur": "destek", "olay": "denetim", "kod_hash": "k", "gecti": True})
        + "\n",
        encoding="utf-8",
    )
    assert kayit.denetim_gecti("k") is True
