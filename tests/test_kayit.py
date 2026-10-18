"""`kosu()` yüzü: kural kaydı, deneme günlüğü, başlangıç denetimi (TASARIM 5.8, 5.11).

Veri: 8 günlük sentetik seri (tests/test_motor.py'deki elle hesap): sinyal gün 5, giriş gün 6 AOF 104,
çıkış gün 7 kapanış 105 (veri sonu). Tek işlem.
"""

import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest

from tansu import aileler, kayit, motor, veri
from tansu import deneme as pilot
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
    for g, k, y in zip(gunler, kap, yuk, strict=True):
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


def test_temiz_agacta_resmi_kirli_agacta_resmi_degil(tmp_path, monkeypatch):
    monkeypatch.setattr(kayit, "TAM_TABAN", 7)
    monkeypatch.setattr(kayit, "TAM_CARPAN", 1)
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    kayit.denetim_yaz(
        {"gecti": True}, P, ATR_N
    )  # ilk resmi koşu için geçen boru hattı denetimi şart (TASARIM 5.12)
    calistir(
        tmp_path,
        kimlik,
        resmi=True,
        git=TEMIZ,
        tekrar=kayit.tekrar_sayisi(
            True, P, ATR_N
        ),  # resmi koşu tam tekrar ister (TASARIM 5.7)
    )
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


def coker(*a, **k):
    raise RuntimeError("koşu yarıda")


def test_gelistirme_kosusu_deneme_sayisina_girmez(tmp_path, monkeypatch):
    # TASARIM 5.11: geliştirme koşusu m'yi artırmaz; yarıda kalan geliştirme koşusu da saymaz.
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    calistir(tmp_path, kimlik)
    monkeypatch.setattr(motor, "sinama", coker)
    with pytest.raises(RuntimeError):
        calistir(tmp_path, kimlik)
    assert [s["olay"] for s in satirlar()][-1] == "basladi"
    assert kayit.deneme_sayisi() == 0


def test_yarida_kalan_resmi_kosu_m_ye_girer_ve_deneme_sayisi_B_ve_holm_ayni_m_yi_kullanir(
    tmp_path, monkeypatch
):
    # TASARIM 5.11: m = resmi koşuların sınadığı (kural, aile) çiftleri, yarıda kalan dahil; B = max(1.000, 200·m).
    # Üç kural, her biri iki aile ve yarıda kalmış resmi koşu: m = 6 -> B = max(1.000, 1.200) = 1.200.
    # Bu kuralın iki p'si 0,01 ve öteki dört çift p yok (yarım) -> en kötü durum p = 1: sıralı [0,01; 0,01; 1; 1; 1; 1],
    # Holm 0,01·6 = 0,06 ve max(0,06; 0,01·5) = 0,06; holm_m = 6.
    kimlik = anlik_hazirla(tmp_path)
    kayit.denetim_yaz({"gecti": True}, P, ATR_N)
    monkeypatch.setattr(motor, "sinama", coker)
    ps = [
        aileler.Parametre(
            periyotlar=(1, 2), esik=e, min_gun=3, pencere=3, isinma=4, sma_n=2
        )
        for e in (0.005, 0.006, 0.007)
    ]
    kural_idler = []
    for p in ps:
        kural_idler.append(kayit.kayitla(p, ATR_N)["kural_id"])
        with pytest.raises(RuntimeError):
            kayit.kosu(
                kimlik,
                tmp_path,
                p=p,
                atr_n=ATR_N,
                resmi=True,
                tekrar=kayit.tekrar_sayisi(True, p, ATR_N),
                git=TEMIZ,
            )
    assert kayit.deneme_sayisi() == 6
    assert kayit.tekrar_sayisi(True, ps[0], ATR_N) == 1200
    kural_id = kural_idler[0]
    h = kayit.holm_hesapla(kural_id, {a: 0.01 for a in kayit.AILELER}, True)
    assert [(h[a]["holm_m"], h[a]["holm_p"]) for a in kayit.AILELER] == [
        (6, pytest.approx(0.06)),
        (6, pytest.approx(0.06)),
    ]


def test_resmi_kosu_tekrar_0_ile_reddedilir_gunluge_satir_yazmaz(tmp_path):
    # TASARIM 5.7: resmi koşuda B ≥ max(1.000, 200·m); tekrar 0 (K1 yok) bu şartı sağlamaz.
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    kayit.denetim_yaz({"gecti": True}, P, ATR_N)
    once = (kayit.KAYIT_DIZINI / "deneme.jsonl").read_text(encoding="utf-8")
    with pytest.raises(kayit.KayitHatasi, match="tekrar"):
        calistir(tmp_path, kimlik, resmi=True, tekrar=0)
    assert (kayit.KAYIT_DIZINI / "deneme.jsonl").read_text(encoding="utf-8") == once


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
        "katalog.py",
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


@pytest.mark.parametrize(
    "arg, beklenen",
    [
        (["--varyant", "tansu"], aileler.VARYANTLAR["tansu"]),
        ([], aileler.Parametre()),
    ],
    ids=["tansu", "varsayilan_bugun"],
)
def test_varyant_secimi_kayit_ve_sinama_komutlarina_gecer(monkeypatch, arg, beklenen):
    # TASARIM 5.11: `kayit|sinama --varyant <ad>` seçer, varsayılan `bugun`.
    from tansu.__main__ import main

    gelen = []
    monkeypatch.setattr(
        kayit, "kayitla", lambda p: gelen.append(("kayit", p)) or {"kural_id": "x"}
    )

    def sahte_tekrar(son, p):
        gelen.append(("tekrar", p))
        return 7

    def sahte_kosu(*a, p, **k):
        gelen.append(("kosu", p))
        raise kayit.KayitHatasi("durdu")

    monkeypatch.setattr(kayit, "tekrar_sayisi", sahte_tekrar)
    monkeypatch.setattr(kayit, "kosu", sahte_kosu)
    assert main(["kayit", *arg]) == 0
    assert main(["sinama", "--kimlik", "k", *arg]) == 1
    assert gelen == [("kayit", beklenen), ("tekrar", beklenen), ("kosu", beklenen)]


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


@pytest.mark.parametrize(
    "dosya, eski, yeni",
    [
        (
            "simulator.py",
            "MASRAFLAR = (0.001, 0.003, 0.005)",
            "MASRAFLAR = (0.001, 0.003, 0.006)",
        ),
        ("istatistik.py", "K1_MASRAF = 0.005", "K1_MASRAF = 0.006"),
        # B sabitleri (GELISTIRME, TAM_TABAN, TAM_CARPAN): kayit.py'de tek demet, sırayla.
        (
            "kayit.py",
            "    200,\n    1000,\n    200,\n",
            "    201,\n    1000,\n    200,\n",
        ),
        (
            "kayit.py",
            "    200,\n    1000,\n    200,\n",
            "    200,\n    1001,\n    200,\n",
        ),
        (
            "kayit.py",
            "    200,\n    1000,\n    200,\n",
            "    200,\n    1000,\n    201,\n",
        ),
    ],
    ids=[
        "MASRAFLAR",
        "K1_MASRAF",
        "GELISTIRME",
        "TAM_TABAN",
        "TAM_CARPAN",
    ],
)
def test_masraf_sabiti_degisince_kod_hashi_degisir(
    tmp_path, monkeypatch, dosya, eski, yeni
):
    # TASARIM 5.8 "Kural kaydı", "Hash dışı": masraf senaryoları ve K1 masrafı kural sabitidir, hash içindedir (bilet 07f).
    paket = tmp_path / "paket"
    paket.mkdir()
    for ad in kayit.KOD_DOSYALARI:
        shutil.copyfile(kayit.PAKET / ad, paket / ad)
    monkeypatch.setattr(kayit, "PAKET", paket)
    once = kayit.kayitla(P, ATR_N)
    yol = paket / dosya
    metin = yol.read_text(encoding="utf-8")
    assert metin.count(eski) == 1
    yol.write_text(metin.replace(eski, yeni), encoding="utf-8")
    sonra = kayit.kayitla(P, ATR_N)
    assert sonra["kod_hash"] != once["kod_hash"]
    assert sonra["kural_id"] != once["kural_id"]


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


def test_pilot_kanonik_tur_anahtar_ondalik_ve_tarih_sozlesmesi():
    assert (
        pilot.kanonik({"b": None, "a": 1})
        == b'["sozluk",[["a",["tam","1"]],["b",["bos"]]]]'
    )
    assert pilot.kanonik({"b": None, "a": 1}) == pilot.kanonik({"a": 1, "b": None})
    assert len({pilot.kanonik(v) for v in (True, 1, 1.0, "1", Decimal("1"), None)}) == 6
    assert pilot.kanonik(Decimal("1.00")) == b'["ondalik","1.00"]'
    assert pilot.kanonik(dt.date(2026, 10, 18)) == b'["tarih","2026-10-18"]'
    assert (
        pilot.kanonik(
            dt.datetime(2026, 10, 18, 3, tzinfo=dt.timezone(dt.timedelta(hours=3)))
        )
        == b'["zaman","2026-10-18T00:00:00+00:00"]'
    )
    for deger in (
        float("nan"),
        float("inf"),
        Decimal("NaN"),
        {1: "a"},
        dt.datetime(2026, 1, 1),
        {"$x": 1},
        object(),
    ):
        with pytest.raises(ValueError):
            pilot.kanonik(deger)


def pilot_deneme(depo, varyant="bugun", **degisiklik):
    alanlar = dict(
        aktor="yazar",
        gerekce="kanıt",
        donemler=[
            {
                "baslangic": dt.date(2025, 1, 1),
                "bitis": dt.date(2025, 12, 31),
                "isinma_baslangici": None,
                "sinir_surumu": "v1",
                "bos_nedenleri": {"isinma_baslangici": "gerekmiyor"},
            }
        ],
        veri_ayarlari={"kaynak": "yerel", "veri_referanslari": ["ag-1"]},
        yontem_ayarlari={"yontem": "legacy", "tekrar": 2},
        risk_ayarlari={"oran": Decimal("0.02")},
        masraf_ayarlari={"oran": Decimal("0.003")},
        eski_referans={"kural_id": "eski-k", "kosu_id": "eski-r", "sinif": "destek"},
    )
    alanlar.update(degisiklik)
    return depo.deneme_kaydet(varyant, **alanlar)


def test_pilot_revizyonlar_eklenir_katalog_ve_eski_sayim_korunur(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "pilot" / "olaylar.jsonl")
    once_kural = kayit.kayitla(P, ATR_N)["kural_id"]
    once_sayim = kayit.deneme_sayisi()
    ilk = pilot_deneme(depo)
    assert ilk is not None
    once = depo.yol.read_bytes()
    ikinci = pilot_deneme(depo, "tansu", ust_deneme=ilk.deneme_id)
    geri = pilot_deneme(depo, ust_deneme=ikinci.deneme_id)
    ayni = pilot_deneme(depo, ust_deneme=geri.deneme_id)
    assert len({m.deneme_id for m in (ilk, ikinci, geri, ayni)}) == 4
    assert ilk.ayar_ozeti == geri.ayar_ozeti == ayni.ayar_ozeti
    assert ikinci.ayar_ozeti != ilk.ayar_ozeti
    assert depo.yol.read_bytes().startswith(once)
    assert depo.oku()[0]["strateji"]["parametreler"][0]["deger"] == (20, 50, 100, 200)
    assert depo.oku()[0]["eski_referans"] == {
        "kural_id": "eski-k",
        "kosu_id": "eski-r",
        "sinif": "destek",
    }
    assert kayit.kayitla(P, ATR_N)["kural_id"] == once_kural
    assert kayit.deneme_sayisi() == once_sayim


def pilot_kosu(depo, deneme_id, **degisiklik):
    alanlar = dict(
        mod="legacy",
        anlik_goruntu="ag-1",
        manifest_ozeti="manifest-1",
        uyelik_surumu="uyelik-1",
        kod_kimligi="kod-1",
        ortam={"python": "3.14"},
        bagimlilik_ozeti="lock-1",
        tohum=42,
        is_listesi=["XXXX"],
        ureteci_surumu="random-v1",
    )
    alanlar.update(degisiklik)
    return depo.kosu(deneme_id, **alanlar)


def pilot_sonuc(kosu, **degisiklik):
    alanlar = dict(
        sinyal_id="sinyal-1",
        islem_referanslari=[],
        donem={
            "baslangic": dt.date(2025, 1, 1),
            "bitis": dt.date(2025, 12, 31),
            "isinma_baslangici": None,
            "sinir_surumu": "v1",
            "bos_nedenleri": {"isinma_baslangici": "gerekmiyor"},
        },
        birimler={"kazanc": "TL"},
        muhasebe_politikasi="legacy-v1",
        uyarilar=[],
        cikti_referanslari=["sonuc.csv"],
        olculer={"kazanc": Decimal("12.30")},
    )
    alanlar.update(degisiklik)
    return kosu.sonuc_kaydet(**alanlar)


def pilot_bitir(kosu):
    return kosu.bitir(
        durum="tamamlandi",
        tamamlanan=["XXXX"],
        basarisiz=[],
        yontemler=["legacy"],
        olculer={},
        cikti_referanslari=[],
        ozetler={"islem": 1},
    )


def test_pilot_kosu_makbuz_izleme_ve_ekleme_duzeltmesi(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    with pilot_kosu(depo, deneme.deneme_id) as kosu:
        assert kosu is not None
        assert depo.oku()[-1]["kayit_id"] == kosu.makbuz.olay_id
        sonuc = pilot_sonuc(kosu)
        pilot_bitir(kosu)
    with pilot_kosu(depo, deneme.deneme_id) as tekrar:
        assert tekrar.makbuz.kosu_id != kosu.makbuz.kosu_id
        assert tekrar.makbuz.deneme_id == kosu.makbuz.deneme_id
    iz = depo.izle(sonuc.olay_id)
    assert iz["deneme"]["strateji"]["varyant"] == "bugun"
    assert iz["baslangic"]["anlik_goruntu"] == "ag-1"
    assert iz["baslangic"]["kod_kimligi"] == "kod-1"
    assert iz["durum"] == "tamamlandi"
    assert depo.kurtar()["cozumsuz_kosular"] == [tekrar.makbuz.kosu_id]
    once = depo.yol.read_bytes()
    depo.duzelt(
        sonuc.olay_id,
        gerekce="birim açıklaması",
        yeni_degerler={"uyarilar": ["açıklama"]},
    )
    assert depo.yol.read_bytes().startswith(once)
    assert depo.izle(sonuc.olay_id)["sonuc"]["uyarilar"] == []
    assert len(depo.izle(sonuc.olay_id)["duzeltmeler"]) == 1
    with pytest.raises(pilot.PilotHatasi):
        pilot_sonuc(kosu)


def test_pilot_fsync_hatasi_bitis_kurtarmada_tamamlandi_sayilmaz(tmp_path, monkeypatch):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    with pytest.raises(pilot.PilotYazmaHatasi, match="disk aktarımı başarısız"):
        with pilot_kosu(depo, deneme.deneme_id) as kosu:
            sonuc = pilot_sonuc(kosu)
            once = depo.yol.read_bytes()

            def hata(fd):
                raise OSError("disk aktarımı başarısız")

            with monkeypatch.context() as ariza:
                ariza.setattr(os, "fsync", hata)
                pilot_bitir(kosu)
    yeni = pilot.PilotKayit(depo.yol)
    assert yeni.kurtar()["cozumsuz_kosular"] == [kosu.makbuz.kosu_id]
    assert yeni.izle(sonuc.olay_id)["durum"] != "tamamlandi"
    assert yeni.yol.read_bytes().startswith(once)
    assert [o["kayit_turu"] for o in yeni.oku()] == ["deneme", "baslangic", "sonuc"]
    assert yeni.kurtar()["uyarilar"]
    pilot_deneme(yeni)
    assert yeni.kurtar()["cozumsuz_kosular"] == [kosu.makbuz.kosu_id]
    assert yeni.izle(sonuc.olay_id)["durum"] == "cozumsuz"
    assert yeni.yol.read_bytes().startswith(once)


@pytest.mark.parametrize("asama", ["baslangic", "sonuc", "bitis"])
@pytest.mark.parametrize("ariza", ["izin", "kisa", "fsync", "lf_izin", "lf_kisa"])
def test_pilot_yazma_hatasi_hesabi_ve_sahte_basariyi_engeller(
    tmp_path, monkeypatch, asama, ariza
):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    asil_yaz = os.write
    hesap = []

    def boz():
        def hata(*args):
            raise PermissionError("disk reddetti")

        if ariza == "fsync":
            monkeypatch.setattr(os, "fsync", hata)
        elif ariza.startswith("lf_"):

            def son_yaz(fd, veri):
                if veri == b"\n":
                    if ariza == "lf_izin":
                        raise PermissionError("satır sonu reddedildi")
                    return 0
                return asil_yaz(fd, veri)

            monkeypatch.setattr(os, "write", son_yaz)
        elif ariza == "kisa":
            monkeypatch.setattr(os, "write", lambda fd, veri: asil_yaz(fd, veri[:11]))
        else:
            monkeypatch.setattr(os, "write", hata)

    if asama == "baslangic":
        boz()
    with pytest.raises(pilot.PilotYazmaHatasi):
        with pilot_kosu(depo, deneme.deneme_id) as kosu:
            hesap.append("başladı")
            if asama == "sonuc":
                boz()
                try:
                    pilot_sonuc(kosu)
                except pilot.PilotYazmaHatasi:
                    pass  # Çağıran yutsa da bağlam başarıyla çıkamaz.
                with pytest.raises(pilot.PilotHatasi):
                    pilot_bitir(kosu)
            elif asama == "bitis":
                boz()
                pilot_bitir(kosu)
    assert hesap == ([] if asama == "baslangic" else ["başladı"])
    yeni = pilot.PilotKayit(depo.yol)
    assert all(o["kayit_turu"] != asama for o in yeni.oku())
    if asama != "baslangic":
        assert yeni.kurtar()["cozumsuz_kosular"] == [kosu.makbuz.kosu_id]


@pytest.mark.parametrize("kuyruk", [b'{"eksik":', b'["sozluk",[]]'])
def test_pilot_kesik_kuyruk_eski_satiri_degistirmeden_kurtarilir(tmp_path, kuyruk):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    with pilot_kosu(depo, deneme.deneme_id) as kosu:
        pass
    with depo.yol.open("ab") as dosya:
        dosya.write(kuyruk)
    once = depo.yol.read_bytes()
    kurtarma = depo.kurtar()
    assert kurtarma["cozumsuz_kosular"] == [kosu.makbuz.kosu_id]
    assert len(kurtarma["uyarilar"]) == 1
    yeni = pilot_deneme(depo)
    assert depo.yol.read_bytes().startswith(once)
    assert [o["kayit_turu"] for o in depo.oku()] == ["deneme", "baslangic", "deneme"]
    assert depo.oku()[-1]["deneme_id"] == yeni.deneme_id
    assert len(depo.kurtar()["uyarilar"]) == 1


def test_pilot_surecler_arasi_satirlar_karismaz(tmp_path):
    yol = tmp_path / "olaylar.jsonl"
    kod = "from pathlib import Path; from tests.test_kayit import pilot_deneme; from tansu.deneme import PilotKayit; import sys; d=PilotKayit(Path(sys.argv[1])); [pilot_deneme(d) for _ in range(4)]"
    surecler = [
        subprocess.Popen(
            [sys.executable, "-X", "utf8", "-c", kod, str(yol)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        for _ in range(3)
    ]
    for surec in surecler:
        _, hata = surec.communicate(timeout=40)
        assert surec.returncode == 0, hata.decode("utf-8")
    depo = pilot.PilotKayit(yol)
    assert len(depo.oku()) == 12
    assert len({o["deneme_id"] for o in depo.oku()}) == 12
    assert depo.kurtar()["uyarilar"] == []


@pytest.mark.parametrize(
    "degisiklik",
    [
        {"aktor": ""},
        {"donemler": []},
        {"risk_ayarlari": {"oran": 0.02}},
        {"masraf_ayarlari": {"oran": 2}},
        {"ust_deneme": "yok"},
        {"yontem_ayarlari": {"tekrar": -1}},
        {"eski_referans": {"kural_id": None}},
        {"baglar": {"egitim_denemeleri": []}},
    ],
)
def test_pilot_gecersiz_revizyon_yazilmaz(tmp_path, degisiklik):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    with pytest.raises(ValueError):
        pilot_deneme(depo, **degisiklik)
    assert depo.oku() == []


def test_pilot_izgara_wf_mc_ve_islem_baglari(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    ust = pilot_deneme(depo)
    egitim = pilot_deneme(
        depo,
        "tansu",
        ust_deneme=ust.deneme_id,
        baglar={"izgara_ust_deneme": ust.deneme_id},
    )
    test = pilot_deneme(depo, ust_deneme=ust.deneme_id)
    secim = pilot_deneme(
        depo,
        baglar={"egitim_denemeleri": [egitim.deneme_id], "test_deneme": test.deneme_id},
    )
    assert depo.oku()[-1]["baglar"]["test_deneme"] == test.deneme_id
    with pilot_kosu(depo, secim.deneme_id) as kosu:
        sonuc = pilot_sonuc(kosu)
        senaryo = kosu.senaryo_kaydet(sira=1, sonuc_referansi=sonuc.olay_id)
        assert depo.izle(senaryo.olay_id)["baslangic"]["kosu_id"] == kosu.makbuz.kosu_id
        with pytest.raises(pilot.PilotHatasi):
            kosu.senaryo_kaydet(sira=2, sonuc_referansi=sonuc.olay_id)
        with pytest.raises(pilot.PilotHatasi):
            kosu.senaryo_kaydet(sira=1, sonuc_referansi=sonuc.olay_id)
        with pytest.raises(pilot.PilotHatasi):
            pilot_sonuc(kosu, islem_referanslari=["yok"])
        islem = kosu.islem_kaydet(
            sinyal_id="sinyal-1",
            donem=depo.oku()[0]["donemler"][0],
            birimler={"adet": "adet"},
            muhasebe_politikasi="legacy-v1",
            uyarilar=[],
            cikti_referanslari=[],
            olaylar=[{"tur": "giris", "adet": Decimal("1")}],
        )
        bagli = pilot_sonuc(kosu, islem_referanslari=[islem.olay_id])
        assert depo.izle(bagli.olay_id)["sonuc"]["islem_referanslari"] == [
            islem.olay_id
        ]
        with pytest.raises(pilot.PilotHatasi):
            kosu.bitir(
                durum="tamamlandi",
                tamamlanan=[],
                basarisiz=[],
                yontemler=["legacy"],
                olculer={},
                cikti_referanslari=[],
                ozetler={},
            )
    with pilot_kosu(depo, secim.deneme_id) as baska:
        with pytest.raises(pilot.PilotHatasi):
            pilot_sonuc(baska, islem_referanslari=[islem.olay_id])
    yeni = pilot_deneme(depo, yontem_ayarlari={"yontem": "legacy", "tekrar": 3})
    assert yeni.deneme_id != ust.deneme_id and yeni.ayar_ozeti != ust.ayar_ozeti
    with pytest.raises(pilot.PilotHatasi):
        depo.duzelt(
            sonuc.olay_id,
            gerekce="yanlış bağ",
            yeni_degerler={"deneme_id": ust.deneme_id},
        )


def test_pilot_hesap_hatasi_gorunur_ve_bilinmeyen_sema_durur(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    with pytest.raises(RuntimeError, match="hesap durdu"):
        with pilot_kosu(depo, deneme.deneme_id):
            raise RuntimeError("hesap durdu")
    assert depo.oku()[-1]["durum"] == "hata"
    assert depo.kurtar()["cozumsuz_kosular"] == []
    with depo.yol.open("ab") as dosya:
        dosya.write(pilot.kanonik({"sema_surumu": "bilinmiyor"}) + b"\n")
    with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır"):
        depo.oku()


def test_pilot_baslangic_is_listesi_cagiran_degistirse_de_donuktur(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    isler = ["XXXX"]
    with pilot_kosu(depo, deneme.deneme_id, is_listesi=isler) as kosu:
        isler.append("YYYY")
        try:
            pilot_bitir(kosu)
            bitti = True
        except pilot.PilotHatasi:
            bitti = False
        assert bitti, "Başlangıç makbuzundaki tek iş tamamlanabilmelidir."
