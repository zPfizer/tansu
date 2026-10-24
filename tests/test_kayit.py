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
from copy import deepcopy
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest

from tansu import aileler, kayit, motor, saglamlik, veri
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
    once = (kayit.KAYIT_DIZINI / "deneme.jsonl").read_bytes()
    with pytest.raises(kayit.KayitHatasi, match="kirli ağaç"):
        calistir(
            tmp_path,
            kimlik,
            resmi=True,
            git=KIRLI,
            tekrar=kayit.tekrar_sayisi(True, P, ATR_N),
        )
    assert (kayit.KAYIT_DIZINI / "deneme.jsonl").read_bytes() == once
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
        "islem_riski.py",
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


@pytest.mark.parametrize(
    "degisiklik",
    [
        dict(bilinmeyen=True),
        dict(kontrol_noktalari=[1000.0]),
        dict(hassasiyet_r=Decimal("0.01")),
        dict(tohum=True),
        dict(yontem="kayitli_monte_carlo_v999"),
    ],
)
def test_s13_mc_yontemi_bilinmeyen_alani_ve_yanlis_turu_kaydetmez(tmp_path, degisiklik):
    from tansu.deneme import PilotKayit, PilotHatasi
    from tests.test_tansusinama import s13_yontem

    depo = PilotKayit(tmp_path / "mc.jsonl")
    yontem = s13_yontem(
        dict(
            deneme_id="wf",
            kosu_id="wf-kosu",
            sonuc_ref="wf-ozet",
            bitis_ref="wf-bitis",
            icerik_ozeti="00" * 32,
        )
    )
    pilot_deneme(depo, yontem_ayarlari=yontem)
    once = depo.yol.read_bytes()
    hata = None
    try:
        pilot_deneme(depo, yontem_ayarlari=yontem | degisiklik)
    except PilotHatasi as yakalanan:
        hata = yakalanan
    assert hata is not None, "MC yöntemi eksik veya bilinmeyen alanla kalıcı olamaz."
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize(
    "alan",
    [
        "bilinmeyen",
        "kontrol_turu",
        "ayar_ozeti",
        "yontem_surumu",
        "dis_alan",
        "kimlik_surumu",
        "kaynak",
        "strateji",
    ],
)
def test_s13_kanonik_mc_deneme_degisimini_yeni_okuyucu_reddeder(tmp_path, alan):
    from tests.test_tansusinama import s13_yontem

    depo = pilot.PilotKayit(tmp_path / "mc.jsonl")
    yontem = s13_yontem(
        dict(
            deneme_id="wf",
            kosu_id="wf-kosu",
            sonuc_ref="wf-ozet",
            bitis_ref="wf-bitis",
            icerik_ozeti="00" * 32,
        )
    )
    pilot_deneme(depo, yontem_ayarlari=yontem)
    olaylar = depo.oku()
    assert len(olaylar) == 1
    if alan == "bilinmeyen":
        olaylar[0]["yontem_ayarlari"]["bilinmeyen"] = True
    elif alan == "kontrol_turu":
        olaylar[0]["yontem_ayarlari"]["kontrol_noktalari"] = [1000.0]
    elif alan == "ayar_ozeti":
        olaylar[0]["risk_ayarlari"]["oran"] = Decimal("0.03")
    elif alan == "yontem_surumu":
        olaylar[0]["yontem_ayarlari"]["yontem"] = "kayitli_monte_carlo_v999"
    elif alan == "dis_alan":
        olaylar[0]["bilinmeyen"] = True
    elif alan == "kimlik_surumu":
        olaylar[0]["kimlik_bicimi_surumu"] = "pilot_s03_v999"
    elif alan == "strateji":
        olaylar[0]["strateji"]["aile"] = "gecersiz"
        olaylar[0]["ayar_parmak_izi"] = pilot._ayar_ozeti(pilot._ayarlar(olaylar[0]))
    else:
        olaylar[0]["kaynaklar"] = []
    depo.yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
    once = depo.yol.read_bytes()
    with pytest.raises(pilot.PilotHatasi):
        pilot_deneme(pilot.PilotKayit(depo.yol))
    assert depo.yol.read_bytes() == once
    with pytest.raises(pilot.PilotHatasi):
        pilot.PilotKayit(depo.yol).oku()


def _s13_mc_baglam_deposu(tmp_path):
    from tests.test_tansusinama import s13_yontem

    depo = pilot.PilotKayit(tmp_path / "mc-baglam.jsonl")
    yontem = s13_yontem(
        dict(
            deneme_id="wf",
            kosu_id="wf-kosu",
            sonuc_ref="wf-ozet",
            bitis_ref="wf-bitis",
            icerik_ozeti="00" * 32,
        )
    )
    m = pilot_deneme(
        depo,
        yontem_ayarlari=yontem,
        veri_ayarlari=dict(
            kaynak="yerel",
            veri_referanslari=["ag-1"],
            manifest_ozeti="manifest-1",
            uyelik_surumu="uyelik-1",
        ),
    )
    return depo, m, yontem


def _s13_mc_kosu_alanlari(yontem):
    return dict(
        kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
        tohum=yontem["tohum"],
        ureteci_surumu=yontem["uretec"],
        is_listesi=["00" * 32],
    )


def test_s13_mc_yazim_dogrulanmis_ayrik_kayit_ve_tek_sahip(tmp_path):
    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    with depo.mc_yazim(m.deneme_id):
        ilk = depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
        ilk["yontem_ayarlari"]["tekrar"] = -1
        ikinci = depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
        assert ikinci["yontem_ayarlari"]["tekrar"] == yontem["tekrar"]
        with pytest.raises(pilot.PilotHatasi, match="zaten etkin"):
            with depo.mc_yazim(m.deneme_id):
                pass
    assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id") == ikinci
    assert pilot.PilotKayit(depo.yol).deneme_oku(m.deneme_id) == ikinci


def test_s13_mc_bosta_kayit_surece_yoluyla_aktarilir(tmp_path):
    import pickle

    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    tasinan = pickle.loads(pickle.dumps(depo))
    assert tasinan.yol == depo.yol
    assert tasinan.deneme_oku(m.deneme_id) == depo.deneme_oku(m.deneme_id)
    with tasinan.mc_yazim(m.deneme_id):
        assert tasinan.mc_kayit(m.deneme_id, "deneme", "deneme_id")


def test_s13_mc_etkin_kayit_surece_beklemeden_aktarilmaz(tmp_path):
    import pickle
    from threading import Event, Thread

    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    bitti = Event()
    hatalar = []

    def aktar():
        try:
            pickle.dumps(depo)
        except (pilot.PilotHatasi, TypeError) as hata:
            hatalar.append(hata)
        finally:
            bitti.set()

    with depo.mc_yazim(m.deneme_id):
        isci = Thread(target=aktar, daemon=True)
        isci.start()
        assert bitti.wait(1), "Etkin MC bağlamının aktarımı beklememelidir."
        assert len(hatalar) == 1
        assert isinstance(hatalar[0], pilot.PilotHatasi)
        assert "Etkin MC" in str(hatalar[0])
        isci.join(timeout=1)
    assert pickle.loads(pickle.dumps(depo)).deneme_oku(m.deneme_id)


def test_s13_mc_yayindan_sonra_cagiran_nesnesi_kaydi_degistirmez(tmp_path):
    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    ortam = {"python": "3.14", "sinama": {"etiket": "ilk"}}
    with depo.mc_yazim(m.deneme_id):
        with pilot_kosu(
            depo, m.deneme_id, ortam=ortam, **_s13_mc_kosu_alanlari(yontem)
        ) as kosu:
            kayit = depo.mc_makbuzlar(kosu, [kosu.makbuz], "baslangic")[0]
            ortam["sinama"]["etiket"] = "degisti"
            kosu._baslangic["ortam"]["sinama"]["etiket"] = "ikinci"
            tekrar = depo.mc_kayit(kosu.makbuz.kosu_id, "baslangic", "kosu_id")
            assert tekrar["ortam"]["sinama"]["etiket"] == "ilk"
            assert tekrar == kayit
    dogal = pilot.PilotKayit(depo.yol).oku()
    assert dogal[-1]["ortam"]["sinama"]["etiket"] == "ilk"


def test_s13_mc_korunan_ve_dogal_baslangic_ayni_alanlari_kabul_eder(
    tmp_path, monkeypatch
):
    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    dogal_yol = tmp_path / "mc-dogal.jsonl"
    dogal_yol.write_bytes(depo.yol.read_bytes())
    dogal = pilot.PilotKayit(dogal_yol)
    alanlar = _s13_mc_kosu_alanlari(yontem)
    with depo.mc_yazim(m.deneme_id):
        with pilot_kosu(depo, m.deneme_id, **alanlar) as kosu:
            korunan = depo.mc_makbuzlar(kosu, [kosu.makbuz], "baslangic")[0]
            assert depo.mc_kayit(kosu.makbuz.kosu_id, "baslangic", "kosu_id") == korunan
            assert depo.mc_kayit("legacy", "baslangic", "mod") == korunan
            assert pilot.PilotKayit(depo.yol).oku()[-1] == korunan
    with monkeypatch.context() as degisiklik:
        degisiklik.setattr(pilot, "_mc_birim", lambda *args, **kwargs: None)
        with dogal.mc_yazim(m.deneme_id):
            assert dogal._mc_baglam.tutacaklar is None
            with pilot_kosu(dogal, m.deneme_id, **alanlar) as kosu:
                kayit = dogal.mc_makbuzlar(kosu, [kosu.makbuz], "baslangic")[0]
                assert (
                    dogal.mc_kayit(kosu.makbuz.kosu_id, "baslangic", "kosu_id") == kayit
                )
                assert dogal.mc_kayit("legacy", "baslangic", "mod") == kayit
                assert pilot.PilotKayit(dogal.yol).oku()[-1] == kayit
    for alan in ("kayit_id", "kosu_id", "olusturma_zamani"):
        korunan.pop(alan)
        kayit.pop(alan)
    assert korunan == kayit


def test_s13_mc_baglam_dis_okuma_yazma_adlandirma_ve_bagi(tmp_path):
    import json
    import os
    import subprocess
    import sys

    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    bag = tmp_path / "mc-hardlink.jsonl"
    tasinan = tmp_path / "mc-tasinan.jsonl"
    os.link(depo.yol, bag)
    once = depo.yol.read_bytes()
    kod = (
        "import json,os,sys\n"
        "islem,yol,bag,tasinan=sys.argv[1:]\n"
        "try:\n"
        " if islem=='oku':\n"
        "  with open(yol,'rb') as f: sonuc=len(f.read())\n"
        " elif islem in ('ekle','ekle_ac'):\n"
        "  fd=os.open(yol,os.O_WRONLY|os.O_APPEND)\n"
        "  try:\n"
        "   if islem=='ekle': os.write(fd,b'BAD')\n"
        "  finally: os.close(fd)\n"
        "  sonuc='acildi'\n"
        " elif islem in ('bag','bag_ac'):\n"
        "  fd=os.open(bag,os.O_RDWR)\n"
        "  try:\n"
        "   if islem=='bag': os.write(fd,b'BAD')\n"
        "  finally: os.close(fd)\n"
        "  sonuc='acildi'\n"
        " elif islem=='tasi':\n"
        "  os.rename(yol,tasinan);os.rename(tasinan,yol);sonuc='tasindi'\n"
        " print(json.dumps({'izin':True,'sonuc':sonuc}))\n"
        "except OSError as e:\n"
        " print(json.dumps({'izin':False,'errno':e.errno,'winerror':getattr(e,'winerror',None)}))\n"
    )
    with depo.mc_yazim(m.deneme_id):
        korunan = depo._mc_baglam.tutacaklar is not None
        islemler = [
            "oku",
            "ekle" if korunan else "ekle_ac",
            "bag" if korunan else "bag_ac",
            "tasi",
        ]
        gozlemler = {}
        for islem in islemler:
            sonuc = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    "-X",
                    "utf8",
                    "-c",
                    kod,
                    islem,
                    str(depo.yol),
                    str(bag),
                    str(tasinan),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
                check=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            gozlemler[islem] = json.loads(sonuc.stdout)
        assert gozlemler["oku"] == {"izin": True, "sonuc": len(once)}
        if korunan:
            for islem in ("ekle", "bag", "tasi"):
                assert gozlemler[islem]["izin"] is False
                assert gozlemler[islem]["errno"] == 13
        else:
            for islem in ("ekle_ac", "bag_ac", "tasi"):
                assert gozlemler[islem]["izin"] is True
        assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
        assert depo.yol.read_bytes() == once
    assert pilot.PilotKayit(depo.yol).deneme_oku(m.deneme_id)


def test_s13_mc_onceden_acik_yazici_ve_esleme_korumayi_reddeder(tmp_path):
    import subprocess
    import sys
    from threading import Timer

    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    with depo.mc_yazim(m.deneme_id):
        korunan = depo._mc_baglam.tutacaklar is not None
    with depo.yol.open("r+b"):
        if korunan:
            with pytest.raises(OSError):
                with depo.mc_yazim(m.deneme_id):
                    pass
        else:
            with depo.mc_yazim(m.deneme_id):
                assert depo._mc_baglam.tutacaklar is None
                assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")

    kod = (
        "import mmap,sys\n"
        "f=open(sys.argv[1],'r+b')\n"
        "v=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_WRITE)\n"
        "f.close()\n"
        "print('READY',flush=True)\n"
        "assert sys.stdin.readline().strip()=='RELEASE'\n"
        "v.close()\n"
    )
    isci = subprocess.Popen(
        [sys.executable, "-B", "-X", "utf8", "-c", kod, str(depo.yol)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    zamanlayici = Timer(20, isci.kill)
    zamanlayici.start()
    try:
        assert isci.stdout.readline().strip() == "READY"
        if korunan:
            with pytest.raises(OSError):
                with depo.mc_yazim(m.deneme_id):
                    pass
        else:
            with depo.mc_yazim(m.deneme_id):
                assert depo._mc_baglam.tutacaklar is None
                assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
        isci.stdin.write("RELEASE\n")
        isci.stdin.flush()
        assert isci.wait(timeout=10) == 0, isci.stderr.read()
    finally:
        zamanlayici.cancel()
        if isci.poll() is None:
            isci.kill()
            isci.wait(timeout=10)
    with depo.mc_yazim(m.deneme_id):
        assert (depo._mc_baglam.tutacaklar is not None) is korunan
        assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")


def test_s13_mc_isci_aniden_cikinca_koruma_serbest_kalir(tmp_path):
    import os
    import subprocess
    import sys

    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    kod = (
        "import os,sys\n"
        "from tansu.deneme import PilotKayit\n"
        "with PilotKayit(sys.argv[1]).mc_yazim(sys.argv[2]) as d:\n"
        " print(int(d._mc_baglam.tutacaklar is not None),flush=True)\n"
        " os._exit(77)\n"
    )
    sonuc = subprocess.run(
        [sys.executable, "-B", "-X", "utf8", "-c", kod, str(depo.yol), m.deneme_id],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=20,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert sonuc.returncode == 77, sonuc.stderr
    korunan = sonuc.stdout.strip() == "1"
    with depo.mc_yazim(m.deneme_id):
        assert (depo._mc_baglam.tutacaklar is not None) is korunan
        assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
    fd = os.open(depo.yol, os.O_WRONLY | os.O_APPEND)
    os.close(fd)
    assert pilot.PilotKayit(depo.yol).deneme_oku(m.deneme_id)


def test_s13_mc_veri_tutacagi_onegi_kesemez_yalniz_sona_ekler(tmp_path):
    import ctypes
    import os
    from ctypes import wintypes

    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    once = depo.yol.read_bytes()
    with depo.mc_yazim(m.deneme_id):
        oturum = depo._mc_baglam
        if oturum.tutacaklar is None:
            assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
            assert depo.yol.read_bytes() == once
        else:
            import msvcrt

            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel.SetEndOfFile.argtypes = [wintypes.HANDLE]
            kernel.SetEndOfFile.restype = wintypes.BOOL
            fd = oturum.veri_fd
            os.lseek(fd, 0, os.SEEK_SET)
            assert not kernel.SetEndOfFile(wintypes.HANDLE(msvcrt.get_osfhandle(fd)))
            assert ctypes.get_last_error() == 5
            assert depo.yol.read_bytes() == once
            assert os.write(fd, pilot._KESIK) == len(pilot._KESIK)
            os.fsync(oturum.kontrol_fd)
            assert depo.yol.read_bytes() == once + pilot._KESIK
            with pytest.raises(pilot.PilotHatasi, match="sonu değişti"):
                depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
            assert oturum.gecersiz
    assert pilot.PilotKayit(depo.yol).deneme_oku(m.deneme_id)


def test_s13_mc_yazim_ayni_dosyanin_baska_yolunu_reddeder(tmp_path):
    import os

    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    diger = tmp_path / "mc-diger-ad.jsonl"
    os.link(depo.yol, diger)
    with depo.mc_yazim(m.deneme_id):
        asil = depo.yol
        depo.yol = diger
        try:
            if depo._mc_baglam.tutacaklar is None:
                assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
            else:
                with pytest.raises(pilot.PilotHatasi, match="yolu değişti"):
                    depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
        finally:
            depo.yol = asil
        if depo._mc_baglam.tutacaklar is None:
            assert not depo._mc_baglam.gecersiz
        else:
            assert depo._mc_baglam.gecersiz
            with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
                depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
    assert pilot.PilotKayit(asil).deneme_oku(m.deneme_id)


def test_s13_mc_yazim_yabanci_kaydi_ve_sorgu_hatasini_durdurur(tmp_path):
    depo, m, _ = _s13_mc_baglam_deposu(tmp_path)
    once = depo.yol.read_bytes()
    with depo.mc_yazim(m.deneme_id):
        if depo._mc_baglam.tutacaklar is None:
            assert depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
            assert not depo._mc_baglam.gecersiz
        else:
            cagirdi = []
            with pytest.raises(pilot.PilotHatasi, match="başka kayıt türünü"):
                depo._ekle(
                    dict(kayit_turu="ayar_bagi", deneme_id=m.deneme_id),
                    lambda olaylar: cagirdi.append(olaylar),
                )
            assert not cagirdi
            assert depo._mc_baglam.gecersiz
    assert depo.yol.read_bytes() == once
    with depo.mc_yazim(m.deneme_id):
        with pytest.raises(pilot.PilotHatasi, match="Kayıt bağı bulunamadı"):
            depo.mc_kayit("yok", "mc_plan")
        assert depo._mc_baglam.gecersiz
        with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
            depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")


def test_s13_mc_yazim_baska_kosuyu_ve_yanlis_makbuzu_durdurur(tmp_path):
    from types import SimpleNamespace

    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    with depo.mc_yazim(m.deneme_id):
        with pilot_kosu(
            depo,
            m.deneme_id,
            kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
            tohum=yontem["tohum"],
            ureteci_surumu=yontem["uretec"],
            is_listesi=["00" * 32],
        ) as kosu:
            sahte = SimpleNamespace(
                makbuz=pilot.Makbuz(
                    "sahte", m.deneme_id, "başka-koşu", kosu.makbuz.ayar_ozeti
                )
            )
            with pytest.raises(pilot.PilotHatasi, match="koşu veya ayar bağı"):
                depo.mc_makbuzlar(sahte, [kosu.makbuz], "baslangic")
            assert depo._mc_baglam.gecersiz
    assert pilot.PilotKayit(depo.yol).oku()


def test_s13_mc_fiziksel_makbuz_geri_okuma_hatasi_baglami_durdurur(
    tmp_path, monkeypatch
):
    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    with depo.mc_yazim(m.deneme_id):
        with pilot_kosu(depo, m.deneme_id, **_s13_mc_kosu_alanlari(yontem)) as kosu:
            oturum = depo._mc_baglam
            if oturum.tutacaklar is None:
                assert depo.mc_makbuzlar(kosu, [kosu.makbuz], "baslangic")
                assert not oturum.gecersiz
            else:
                once = depo.yol.read_bytes()
                asil_oku = pilot._aralik_oku
                konum, uzunluk, _ = oturum.araliklar[kosu.makbuz.olay_id]

                def bozuk_oku(fd, bas, sayi):
                    if (bas, sayi) == (konum, uzunluk):
                        return b"X" * sayi
                    return asil_oku(fd, bas, sayi)

                with monkeypatch.context() as degisiklik:
                    degisiklik.setattr(pilot, "_aralik_oku", bozuk_oku)
                    with pytest.raises(pilot.PilotHatasi, match="fiziksel makbuz"):
                        depo.mc_makbuzlar(kosu, [kosu.makbuz], "baslangic")
                assert oturum.gecersiz
                with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
                    depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
                assert depo.yol.read_bytes() == once
    assert pilot.PilotKayit(depo.yol).oku()[-1]["kayit_turu"] == "baslangic"


def test_s13_mc_yazim_ikinci_koku_reddeder(tmp_path):
    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    alanlar = dict(
        kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
        tohum=yontem["tohum"],
        ureteci_surumu=yontem["uretec"],
        is_listesi=["00" * 32],
    )
    with depo.mc_yazim(m.deneme_id):
        with pilot_kosu(depo, m.deneme_id, **alanlar):
            once = depo.yol.read_bytes()
            if depo._mc_baglam.tutacaklar is None:
                with pilot_kosu(depo, m.deneme_id, **alanlar):
                    pass
                assert len(depo.oku()) == 3
                assert not depo._mc_baglam.gecersiz
            else:
                with pytest.raises(pilot.PilotHatasi, match="ikinci koşu"):
                    with pilot_kosu(depo, m.deneme_id, **alanlar):
                        pass
                assert depo._mc_baglam.gecersiz
                assert depo.yol.read_bytes() == once


def test_s13_mc_yayin_kesintisi_ikinci_yazimi_engeller(tmp_path, monkeypatch):
    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    alanlar = dict(
        kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
        tohum=yontem["tohum"],
        ureteci_surumu=yontem["uretec"],
        is_listesi=["00" * 32],
    )
    with depo.mc_yazim(m.deneme_id):
        if depo._mc_baglam.tutacaklar is None:
            with pilot_kosu(depo, m.deneme_id, **alanlar):
                pass
            assert len(depo.oku()) == 2
            assert not depo._mc_baglam.gecersiz
        else:
            once = depo.yol.read_bytes()
            veri_fd = depo._mc_baglam.veri_fd
            asil_yaz = pilot.os.write

            def kes(fd, baytlar):
                if fd == veri_fd:
                    raise KeyboardInterrupt("Yayın kesildi.")
                return asil_yaz(fd, baytlar)

            with monkeypatch.context() as degisiklik:
                degisiklik.setattr(pilot.os, "write", kes)
                with pytest.raises(KeyboardInterrupt, match="Yayın kesildi"):
                    with pilot_kosu(depo, m.deneme_id, **alanlar):
                        pass
            assert depo._mc_baglam.gecersiz
            with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
                with pilot_kosu(depo, m.deneme_id, **alanlar):
                    pass
            assert depo.yol.read_bytes() == once
    assert pilot.PilotKayit(depo.yol).deneme_oku(m.deneme_id)


@pytest.mark.parametrize(
    "asama", ["icerik_kisa", "lf_kisa", "ilk_fsync", "ikinci_fsync", "geri_okuma"]
)
def test_s13_mc_yayin_asamalari_makbuz_vermez_ve_taze_okuyucu_kurtarir(
    tmp_path, monkeypatch, asama
):
    depo, m, yontem = _s13_mc_baglam_deposu(tmp_path)
    once = depo.yol.read_bytes()
    korunan = False
    with depo.mc_yazim(m.deneme_id):
        oturum = depo._mc_baglam
        korunan = oturum.tutacaklar is not None
        if oturum.tutacaklar is None:
            with pilot_kosu(depo, m.deneme_id, **_s13_mc_kosu_alanlari(yontem)):
                pass
            assert not oturum.gecersiz
        else:
            asil_yaz = pilot.os.write
            asil_fsync = pilot.os.fsync
            asil_oku = pilot._aralik_oku
            fsync_sayisi = []

            def yaz(fd, baytlar):
                if fd == oturum.veri_fd and (
                    (asama == "icerik_kisa" and baytlar != b"\n")
                    or (asama == "lf_kisa" and baytlar == b"\n")
                ):
                    return 0
                return asil_yaz(fd, baytlar)

            def fsync(fd):
                if fd == oturum.kontrol_fd:
                    fsync_sayisi.append(True)
                    if (asama == "ilk_fsync" and len(fsync_sayisi) == 1) or (
                        asama == "ikinci_fsync" and len(fsync_sayisi) == 2
                    ):
                        raise OSError("Kalıcılık onayı kesildi.")
                return asil_fsync(fd)

            def oku(fd, konum, uzunluk):
                if asama == "geri_okuma" and konum >= len(once) and uzunluk > 1:
                    return b"X" * uzunluk
                return asil_oku(fd, konum, uzunluk)

            with monkeypatch.context() as degisiklik:
                degisiklik.setattr(pilot.os, "write", yaz)
                degisiklik.setattr(pilot.os, "fsync", fsync)
                degisiklik.setattr(pilot, "_aralik_oku", oku)
                hata_turu = (
                    pilot.PilotHatasi
                    if asama == "geri_okuma"
                    else pilot.PilotBelirsizHatasi
                )
                with pytest.raises(hata_turu):
                    with pilot_kosu(depo, m.deneme_id, **_s13_mc_kosu_alanlari(yontem)):
                        pass
            assert oturum.gecersiz
            with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
                depo.mc_kayit(m.deneme_id, "deneme", "deneme_id")
    dogal = pilot.PilotKayit(depo.yol)
    beklenen = 2 if not korunan or asama in ("ikinci_fsync", "geri_okuma") else 1
    assert len(dogal.oku()) == beklenen
    if beklenen == 1:
        pilot_deneme(dogal)
        assert len(pilot.PilotKayit(depo.yol).oku()) == 2


def test_s13_mc_koruma_kapatma_hatasi_asli_gizlemez(tmp_path, monkeypatch):
    import os

    depo, _, _ = _s13_mc_baglam_deposu(tmp_path)
    asil_kapat = pilot.os.close
    kapananlar = []
    asil_hata = ValueError("İşlem hatası")

    def kapat(fd):
        kapananlar.append(fd)
        asil_kapat(fd)
        if len(kapananlar) == 1:
            raise OSError("İlk kapatma raporu")

    if os.name == "nt":
        yakalanan = None
        with monkeypatch.context() as degisiklik:
            degisiklik.setattr(pilot.os, "close", kapat)
            try:
                with pilot._mc_koruma(depo.yol) as tutacaklar:
                    if tutacaklar is None:
                        assert depo.deneme_oku(depo.oku()[0]["deneme_id"])
                    else:
                        raise asil_hata
            except ValueError as hata:
                yakalanan = hata
        if kapananlar:
            assert yakalanan is asil_hata
            assert len(kapananlar) == 2
        else:
            assert yakalanan is None
            assert depo.oku()
    else:
        with depo.mc_yazim(depo.oku()[0]["deneme_id"]):
            assert depo._mc_baglam.tutacaklar is None
            assert depo.mc_kayit(depo.oku()[0]["deneme_id"], "deneme", "deneme_id")


def test_s13_baslamadan_hata_bitisinin_kimligi_ve_isleri_degistirilemez(tmp_path):
    from tests.test_tansusinama import s13_yontem

    depo = pilot.PilotKayit(tmp_path / "mc-bitis.jsonl")
    y = s13_yontem(
        dict(
            deneme_id="wf",
            kosu_id="wf-kosu",
            sonuc_ref="wf-ozet",
            bitis_ref="wf-bitis",
            icerik_ozeti="00" * 32,
        )
    )
    veri = dict(
        kaynak="yerel",
        veri_referanslari=["ag-1"],
        manifest_ozeti="manifest-1",
        uyelik_surumu="uyelik-1",
    )
    m = pilot_deneme(depo, yontem_ayarlari=y, veri_ayarlari=veri)
    baska = pilot_deneme(depo, yontem_ayarlari=y, veri_ayarlari=veri)
    eski = pilot_deneme(depo)
    with pilot_kosu(
        depo,
        m.deneme_id,
        kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
        tohum=y["tohum"],
        ureteci_surumu=y["uretec"],
        is_listesi=["00" * 32],
    ) as kosu:
        once = depo.yol.read_bytes()
        hata = None
        try:
            kosu.bitir(
                durum="hata",
                tamamlanan=[],
                basarisiz=["00" * 32],
                yontemler=[y["yontem"], "nihai"],
                olculer={},
                cikti_referanslari=[],
                ozetler=dict(calisma_turu="nihai", yontem_tamamlandi=True),
            )
        except pilot.PilotHatasi as yakalanan:
            hata = yakalanan
        assert hata is not None, (
            "Sıfır senaryolu ön gösterim nihai tamamlanma iddia edemez."
        )
        assert depo.yol.read_bytes() == once
        kosu.bitir(
            durum="hata",
            tamamlanan=[],
            basarisiz=["00" * 32],
            yontemler=[y["yontem"]],
            olculer={},
            cikti_referanslari=[],
            ozetler={},
        )
    for ustveri in (
        {"hata": ""},
        dict(calisma_turu="on_gosterim", yontem_tamamlandi=False),
    ):
        with pilot_kosu(
            depo,
            m.deneme_id,
            kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
            tohum=y["tohum"],
            ureteci_surumu=y["uretec"],
            is_listesi=["00" * 32],
        ) as kosu:
            kosu.bitir(
                durum="hata",
                tamamlanan=[],
                basarisiz=["00" * 32],
                yontemler=[y["yontem"], "on_gosterim"],
                olculer={},
                cikti_referanslari=[],
                ozetler=ustveri,
            )
        assert pilot.PilotKayit(depo.yol).oku()[-1]["ozetler"] == ustveri
    with pytest.raises(ValueError, match="Erken hata"):
        with pilot_kosu(
            depo,
            m.deneme_id,
            kod_kimligi="kayitli_monte_carlo_v1:sha256:" + "00" * 32,
            tohum=y["tohum"],
            ureteci_surumu=y["uretec"],
            is_listesi=["00" * 32],
        ):
            raise ValueError("Erken hata")
    fiziksel = depo.oku()
    assert fiziksel[-1]["durum"] == "hata" and depo.kurtar()["cozumsuz_kosular"] == []
    kabul_edilen = []
    for boz in (
        "isler",
        "ayar",
        "kaynak",
        "alan",
        "yinelenen",
        "durum",
        "ust",
        "legacy_ust",
        "calisma_turu",
        "tamamlanma",
        "tamamlanma_turu",
        "yontemler",
        "olculer",
        "ustveri",
    ):
        olaylar = deepcopy(fiziksel)
        bitis = olaylar[-1]
        if boz == "isler":
            bitis["basarisiz"] = []
        elif boz == "ayar":
            bitis["ayar_parmak_izi"] = "baska-ayar"
        elif boz == "kaynak":
            bitis["kaynaklar"] = []
        elif boz == "alan":
            bitis["bilinmeyen"] = True
        elif boz == "yinelenen":
            olaylar.append(dict(bitis, kayit_id="ikinci-bitis"))
        elif boz == "durum":
            bitis["durum"] = "bilinmeyen"
        elif boz == "ust":
            bitis["deneme_id"] = baska.deneme_id
        elif boz == "legacy_ust":
            bitis["deneme_id"] = eski.deneme_id
        elif boz == "calisma_turu":
            bitis["ozetler"] = dict(calisma_turu="nihai", yontem_tamamlandi=False)
        elif boz == "tamamlanma":
            bitis["ozetler"] = dict(calisma_turu="on_gosterim", yontem_tamamlandi=True)
        elif boz == "tamamlanma_turu":
            bitis["ozetler"] = dict(calisma_turu="on_gosterim", yontem_tamamlandi=0)
        elif boz == "yontemler":
            bitis["yontemler"] = [y["yontem"], "nihai"]
        elif boz == "olculer":
            bitis["olculer"] = dict(toplam_r=1.0)
        else:
            bitis["ozetler"] = dict(bilinmeyen=True)
        yol = tmp_path / ("bitis-" + boz + ".jsonl")
        yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            continue
        kabul_edilen.append(boz)
    baslangic_no = next(
        i for i, o in enumerate(fiziksel) if o["kayit_turu"] == "baslangic"
    )
    eski_kayit = depo.deneme_oku(eski.deneme_id)
    for boz in ("ust", "ust_ayar", "ust_ayar_kod", "tohum", "uretec", "alan"):
        # No finish or typed MC event can hide a missing start READ guard.
        olaylar = deepcopy(fiziksel[: baslangic_no + 1])
        baslangic = olaylar[-1]
        if boz.startswith("ust"):
            baslangic["deneme_id"] = eski.deneme_id
            if boz != "ust":
                baslangic["ayar_parmak_izi"] = eski_kayit["ayar_parmak_izi"]
            if boz == "ust_ayar_kod":
                baslangic["kod_kimligi"] = "kod-1"
        elif boz == "tohum":
            baslangic["tohum"] += 1
        elif boz == "uretec":
            baslangic["ureteci_surumu"] = "random-v1"
        else:
            baslangic["bilinmeyen"] = True
        yol = tmp_path / ("baslangic-" + boz + ".jsonl")
        yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            continue
        kabul_edilen.append("baslangic_" + boz)
    assert kabul_edilen == [], (
        "MC başlangıç öneki ve hata bitişi değişmez kimlik ve tam iş muhasebesi gerektirir."
    )


def test_s13_kalici_kontrol_ilk_noktayi_atlayamaz():
    """Kurulmuş kesin önek; bu örnek yerel 20.000 senaryo yürütmesi değildir."""
    from tansu import istatistik

    d = dict(
        deneme_id="d",
        ayar_parmak_izi="a",
        yontem_ayarlari=dict(kontrol_noktalari=[10000, 20000, 40000, 80000, 100000]),
    )
    b = dict(kosu_id="k", deneme_id="d", ayar_parmak_izi="a")
    girdi = dict(
        kayit_turu="mc_girdi", kayit_id="g", **b, kayit=dict(isler=[dict(anahtar="j")])
    )
    olcu = istatistik.mc_olc([1.0, -2.0, 3.0])
    planlar = [
        dict(
            kayit_turu="mc_plan",
            kayit_id=f"p{i}",
            kosu_id="k",
            kayit=dict(anahtar="j", indeks=i),
        )
        for i in range(20000)
    ]
    sonuclar = [
        dict(
            kayit_turu="mc_senaryo",
            kayit_id=f"s{i}",
            kosu_id="k",
            kayit=dict(plan_ref=f"p{i}", durum="tamamlandi", olculer=olcu),
        )
        for i in range(20000)
    ]
    tani = istatistik.mc_kontrol([olcu] * 20000)
    k = dict(
        girdi_ref="g",
        anahtar="j",
        onceki_ref=None,
        sonuc_referanslari=[o["kayit_id"] for o in sonuclar],
        tani=tani,
    )
    olaylar = [girdi] + planlar + sonuclar
    hata = None
    try:
        pilot._mc_kontrol_dogrula(olaylar, d, b, k, onek=pilot._mc_onek(olaylar))
    except pilot.PilotHatasi as yakalanan:
        hata = yakalanan
    assert hata is not None, "İlk kalıcı kontrol 20.000 ile 10.000'i atlayamaz."
    ilk = dict(
        k,
        sonuc_referanslari=k["sonuc_referanslari"][:10000],
        tani=istatistik.mc_kontrol([olcu] * 10000),
    )
    onek = [girdi] + planlar[:10000] + sonuclar[:10000]
    pilot._mc_kontrol_dogrula(onek, d, b, ilk, onek=pilot._mc_onek(onek))
    kontrol = dict(kayit_turu="mc_kontrol", kayit_id="c", **b, kayit=ilk)
    onek += [kontrol] + planlar[10000:] + sonuclar[10000:]
    ikinci = dict(
        k,
        onceki_ref="c",
        tani=istatistik.mc_kontrol([olcu] * 20000, onceki=ilk["tani"]),
    )
    pilot._mc_kontrol_dogrula(onek, d, b, ikinci, onek=pilot._mc_onek(onek))
    atlanan = dict(ikinci, tani=istatistik.mc_kontrol([olcu] * 40000))
    for i in range(20000, 40000):
        onek.extend(
            [
                dict(
                    kayit_turu="mc_plan",
                    kayit_id=f"p{i}",
                    kosu_id="k",
                    kayit=dict(anahtar="j", indeks=i),
                ),
                dict(
                    kayit_turu="mc_senaryo",
                    kayit_id=f"s{i}",
                    kosu_id="k",
                    kayit=dict(plan_ref=f"p{i}", durum="tamamlandi", olculer=olcu),
                ),
            ]
        )
    atlanan["sonuc_referanslari"] = [f"s{i}" for i in range(40000)]
    with pytest.raises(pilot.PilotHatasi, match="sonraki kayıtlı nokta"):
        pilot._mc_kontrol_dogrula(onek, d, b, atlanan, onek=pilot._mc_onek(onek))
    on_gosterim = dict(
        ilk,
        sonuc_referanslari=k["sonuc_referanslari"][:1000],
        tani=istatistik.mc_kontrol([olcu] * 1000),
    )
    pilot._mc_kontrol_dogrula(
        [girdi] + planlar[:1000] + sonuclar[:1000],
        dict(d, yontem_ayarlari=dict(kontrol_noktalari=[1000])),
        b,
        on_gosterim,
    )


def test_s13_bitis_gec_isi_ve_tahmin_kanitini_yeniden_denetler(tmp_path, monkeypatch):
    from tansu import istatistik, tansusinama as ts
    from tests.test_tansusinama import s13_kayitli, s13_kosu

    depo, m, _, kaynak = s13_kayitli(tmp_path, monkeypatch)
    kabul = []
    for sonuc_var in (True, False):
        ctx, d, g = s13_kosu(depo, m, kaynak)
        with ctx as kosu:
            gm = kosu.mc_girdi_kaydet(kayit=g)
            om = kosu.mc_ozet_kaydet(
                kayit=dict(
                    girdi_ref=gm.olay_id,
                    isler=[ts._mc_is_ozeti(i, 1000, [], []) for i in g["isler"]],
                    uyarilar=[],
                )
            )
            is_ = next(
                i
                for i in g["isler"]
                if i["dilim"] == "2022"
                and i["deney"] == "sira_v1"
                and i["durum"] == "hazir"
            )
            p, pm = ts._mc_planlar(depo, kosu, d, g, gm.olay_id, is_, 0, 1, [], {})[0]
            if sonuc_var:
                kosu.mc_senaryo_sonucu_kaydet(
                    kayit=dict(
                        plan_ref=pm.olay_id,
                        durum="tamamlandi",
                        **istatistik.mc_senaryo_olculeri(g, is_, p["cekilis"]),
                        yeniden_sinama={},
                        sonuc_referanslari=[],
                        asama=None,
                        neden=None,
                    )
                )
            alanlar = dict(
                durum="hata",
                tamamlanan=[],
                basarisiz=[i["anahtar"] for i in g["isler"]],
                yontemler=["kayitli_monte_carlo_v1"],
                olculer={},
                cikti_referanslari=[om.olay_id],
                ozetler={},
            )
            once = depo.yol.read_bytes()
            try:
                kosu.bitir(**alanlar)
            except pilot.PilotHatasi:
                assert depo.yol.read_bytes() == once
                if not sonuc_var:
                    kurtarma = next(
                        o
                        for o in depo.kurtar()["mc_belirsiz_kosular"]
                        if o["kosu_id"] == kosu.makbuz.kosu_id
                    )
                    is_kurtarma = next(
                        i for i in kurtarma["isler"] if i["anahtar"] == is_["anahtar"]
                    )
                    assert is_kurtarma["denenen"] is None
                    assert is_kurtarma["deneme_yayin_belirsiz"] == [0, 0]
            else:
                kabul.append(("gec_is_yaz", sonuc_var))
            bitis = dict(
                kayit_id=f"bozuk-bitis-{sonuc_var}",
                sema_surumu=pilot.SURUM,
                olusturma_zamani=dt.datetime.now(dt.timezone.utc),
                kayit_turu="bitis",
                deneme_id=d["deneme_id"],
                kosu_id=kosu.makbuz.kosu_id,
                ayar_parmak_izi=d["ayar_parmak_izi"],
                kaynaklar=d["kaynaklar"],
                bitis_zamani=dt.datetime.now(dt.timezone.utc),
                **alanlar,
            )
            yol = tmp_path / f"gec-is-{sonuc_var}.jsonl"
            yol.write_bytes(once + pilot.kanonik(bitis) + b"\n")
            try:
                pilot.PilotKayit(yol).oku()
            except pilot.PilotHatasi:
                pass
            else:
                kabul.append(("gec_is_oku", sonuc_var))

    fiziksel = [
        pilot._coz(json.loads(s)) for s in depo.yol.read_bytes().split(b"\n") if s
    ]
    girdi_no = next(i for i, o in enumerate(fiziksel) if o["kayit_turu"] == "mc_girdi")
    girdi = fiziksel[girdi_no]
    blok = next(
        i
        for i in girdi["kayit"]["isler"]
        if i["deney"] == "ortak_tarih_blok_v1" and i["dilim"] == "birlesik"
    )
    if blok.get("blok_tahmini", {}).get("ham") is None:
        kabul.append("ham_tahmin_saklanmadi")
    for boz in (
        "eksik",
        "ham",
        "girdi_ozeti",
        "yontem",
        "uzunluklar",
        "neden",
        "fazla",
    ):
        yanlis = deepcopy(girdi["kayit"])
        if boz == "eksik":
            for i in yanlis["isler"]:
                i.pop("blok_tahmini", None)
        else:
            b = next(i for i in yanlis["isler"] if i["anahtar"] == blok["anahtar"])
            tahmin = b.setdefault(
                "blok_tahmini",
                dict(
                    yontem="ppw2009_arch72_v1",
                    ham=0.0,
                    uzunluklar=[1],
                    neden=None,
                    girdi_ozeti="00" * 32,
                ),
            )
            tahmin[boz] = {
                "ham": 999.0,
                "girdi_ozeti": "00" * 32,
                "yontem": "yanlis",
                "uzunluklar": [],
                "neden": "yanlis",
                "fazla": True,
            }[boz]
        ctx, _, _ = s13_kosu(depo, m, kaynak)
        with ctx as kosu:
            once = depo.yol.read_bytes()
            try:
                kosu.mc_girdi_kaydet(kayit=yanlis)
            except pilot.PilotHatasi:
                assert depo.yol.read_bytes() == once
            else:
                kabul.append(("tahmin_yaz", boz))
        olaylar = deepcopy(fiziksel[: girdi_no + 1])
        olaylar[-1]["kayit"] = yanlis
        olaylar[-1]["icerik_ozeti"] = pilot._mc_ozet(yanlis)
        yol = tmp_path / f"tahmin-{boz}.jsonl"
        yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            pass
        else:
            kabul.append(("tahmin_oku", boz))
    assert kabul == [], (
        "Bitiş güncel işi, girdi ise saklı tahmin kanıtını doğrulamalıdır."
    )


def test_s13_wf_parti_kesintisi_ve_kayitli_hata_sayimlari_ayridir(
    tmp_path, monkeypatch
):
    from tansu import istatistik, tansusinama as ts
    from tests.test_tansusinama import s13_kayitli, s13_kosu, s13_plan

    depo, m, _, kaynak = s13_kayitli(tmp_path, monkeypatch)
    ctx, d, g = s13_kosu(depo, m, kaynak)
    with ctx as kosu:
        is_, planlar = s13_plan(depo, kosu, d, g, deney="sira_v1", sayi=5)
        kurtarma = depo.kurtar()["mc_belirsiz_kosular"][0]["isler"]
        belirsiz = next(i for i in kurtarma if i["anahtar"] == is_["anahtar"])
        assert belirsiz["denenen"] is None and belirsiz["kesin_tamamlanan"] == 0
        assert belirsiz["deneme_yayin_belirsiz"] == [0, 4]
        assert belirsiz["baslamayan_kanitli"] == 995
        once = depo.yol.read_bytes()
        with pytest.raises(pilot.PilotHatasi, match="belirsiz"):
            kosu.bitir(
                durum="hata",
                tamamlanan=[],
                basarisiz=[i["anahtar"] for i in g["isler"]],
                yontemler=["kayitli_monte_carlo_v1"],
                olculer={},
                cikti_referanslari=[],
                ozetler={},
            )
        assert depo.yol.read_bytes() == once
        ikinci_ctx, ikinci_d, ikinci_g = s13_kosu(depo, m, kaynak)
        with pytest.raises(ValueError, match="Yayın öncesi kesinti"):
            with ikinci_ctx as ikinci_kosu:
                s13_plan(depo, ikinci_kosu, ikinci_d, ikinci_g, deney="sira_v1", sayi=1)
                raise ValueError("Yayın öncesi kesinti")
        ikinci = next(
            k
            for k in depo.kurtar()["mc_belirsiz_kosular"]
            if k["kosu_id"] == ikinci_kosu.makbuz.kosu_id
        )
        assert next(i for i in ikinci["isler"] if i["anahtar"] == is_["anahtar"])[
            "deneme_yayin_belirsiz"
        ] == [0, 0]
        kayitlar = []
        for p, pm in planlar[:2]:
            olcu = istatistik.mc_senaryo_olculeri(g, is_, p["cekilis"])
            kayitlar.append(
                dict(
                    plan_ref=pm.olay_id,
                    durum="tamamlandi",
                    **olcu,
                    yeniden_sinama={},
                    sonuc_referanslari=[],
                    asama=None,
                    neden=None,
                )
            )
        kayitlar.append(
            dict(
                plan_ref=planlar[2][1].olay_id,
                durum="hata",
                olculer={},
                sembol_olculeri={},
                yeniden_sinama={},
                sonuc_referanslari=[],
                asama="olcum",
                neden="Kontrollü hesap arızası.",
            )
        )
        once = depo.yol.read_bytes()
        with pytest.raises(pilot.PilotHatasi, match="Kayıt bağı bulunamadı"):
            kosu.mc_sonuclari_kaydet(
                kayitlar=[kayitlar[0], dict(kayitlar[1], plan_ref="gelecek-plan")]
            )
        assert depo.yol.read_bytes() == once
        assert (
            next(
                i
                for i in depo.kurtar()["mc_belirsiz_kosular"][0]["isler"]
                if i["anahtar"] == is_["anahtar"]
            )["kesin_tamamlanan"]
            == 0
        )

        iid = next(
            i
            for i in g["isler"]
            if i["dilim"] == "2022" and i["deney"] == "yerine_koyma_v1"
        )
        iid_planlari = ts._mc_planlar(
            depo, kosu, d, g, planlar[0][0]["girdi_ref"], iid, 0, 2, [], {}
        )
        iid_sonuclari = [
            dict(
                plan_ref=pm.olay_id,
                durum="tamamlandi",
                **istatistik.mc_senaryo_olculeri(g, iid, p["cekilis"]),
                yeniden_sinama={},
                sonuc_referanslari=[],
                asama=None,
                neden=None,
            )
            for p, pm in iid_planlari
        ]
        hata = None
        try:
            kosu.mc_sonuclari_kaydet(
                kayitlar=[
                    kayitlar[0],
                    iid_sonuclari[0],
                    kayitlar[1],
                    iid_sonuclari[1],
                    kayitlar[2],
                ]
            )
        except pilot.PilotHatasi as yakalanan:
            hata = yakalanan
        assert hata is None, (
            f"Ayrı deneylerin sıralı sonuçları iç içe gelebilir: {hata}"
        )
        assert [
            o["kayit"]["plan_ref"]
            for o in pilot._mc_is_sonuclari(
                depo.oku(), kosu.makbuz.kosu_id, iid["anahtar"]
            )
        ] == [pm.olay_id for _, pm in iid_planlari]
        kurtarma = depo.kurtar()["mc_belirsiz_kosular"][0]["isler"]
        kayitli = next(i for i in kurtarma if i["anahtar"] == is_["anahtar"])
        assert kayitli["denenen"] == 3 and kayitli["kesin_tamamlanan"] == 2
        assert kayitli["deneme_yayin_belirsiz"] is None
        assert kayitli["baslamayan_kanitli"] == 997
        once = depo.yol.read_bytes()
        with pytest.raises(pilot.PilotHatasi):
            kosu.mc_planlari_kaydet(kayitlar=[planlar[0][0]])
        with pytest.raises(pilot.PilotHatasi):
            kosu.mc_sonuclari_kaydet(kayitlar=[kayitlar[0]])
        with pytest.raises(pilot.PilotHatasi):
            kosu.bitir(
                durum="tamamlandi",
                tamamlanan=[is_["anahtar"]],
                basarisiz=[],
                yontemler=["kayitli_monte_carlo_v1"],
                olculer={},
                cikti_referanslari=[],
                ozetler={},
            )
        assert depo.yol.read_bytes() == once
        olaylar = depo.oku()
        ozetler = []
        for i in g["isler"]:
            sonuclar = pilot._mc_is_sonuclari(
                olaylar, kosu.makbuz.kosu_id, i["anahtar"]
            )
            ozetler.append(
                ts._mc_is_ozeti(
                    i,
                    1000,
                    sonuclar,
                    [],
                    hata=ValueError("Kontrollü hesap arızası.")
                    if i["anahtar"] == is_["anahtar"]
                    else None,
                )
            )
        yanlis = deepcopy(ozetler)
        yanlis[0]["tamamlanan"] = 1000
        with pytest.raises(pilot.PilotHatasi):
            kosu.mc_ozet_kaydet(
                kayit=dict(
                    girdi_ref=planlar[0][0]["girdi_ref"], isler=yanlis, uyarilar=[]
                )
            )
        om = kosu.mc_ozet_kaydet(
            kayit=dict(girdi_ref=planlar[0][0]["girdi_ref"], isler=ozetler, uyarilar=[])
        )
        kosu.bitir(
            durum="hata",
            tamamlanan=[],
            basarisiz=[i["anahtar"] for i in g["isler"]],
            yontemler=["kayitli_monte_carlo_v1"],
            olculer={},
            cikti_referanslari=[om.olay_id],
            ozetler={},
        )

    fiziksel = [
        pilot._coz(json.loads(s)) for s in depo.yol.read_bytes().split(b"\n") if s
    ]
    kabul_edilen = []
    for boz in (
        "alan",
        "surum",
        "yontem",
        "kosu",
        "plan",
        "olcu",
        "ic_sema",
        "kimlik",
        "parti",
        "bitis",
        "dis_kimlik",
        "tur_degistir",
        "plan_kimligi_liste",
    ):
        olaylar = deepcopy(fiziksel)
        parti = next(
            o
            for o in olaylar
            if o["kayit_turu"] == "mc_parti"
            and o["kayit"]["kayitlar"][0]["kayit_turu"] == "mc_senaryo"
        )
        ic = parti["kayit"]["kayitlar"][0]
        if boz == "alan":
            ic["kayit"]["bilinmeyen"] = True
        elif boz == "surum":
            ic["surum"] = "mc_senaryo_v999"
        elif boz == "yontem":
            ic["yontem_surumu"] = "kayitli_ileri_v1"
        elif boz == "kosu":
            ic["kosu_id"] = "baska-kosu"
        elif boz == "plan":
            ic["kayit"]["plan_ref"] = planlar[1][1].olay_id
        elif boz == "olcu":
            ic["kayit"]["olculer"]["toplam_r"]["deger"] += 1.0
        elif boz == "ic_sema":
            ic["sema_surumu"] = "pilot_s03_v999"
        elif boz == "kimlik":
            ic["kayit_id"] = planlar[0][1].olay_id
        elif boz == "parti":
            ic["parti_ref"] = "kesinlesmemis-parti"
        elif boz == "dis_kimlik":
            ozet = next(o for o in olaylar if o["kayit_turu"] == "mc_ozet")
            ozet["kayit_id"] = olaylar[0]["kayit_id"]
            olaylar = olaylar[: olaylar.index(ozet) + 1]
        elif boz == "tur_degistir":
            girdi = next(o for o in olaylar if o["kayit_turu"] == "mc_girdi")
            girdi["kayit_turu"] = "sonuc"
            olaylar = olaylar[: olaylar.index(girdi) + 1]
        elif boz == "plan_kimligi_liste":
            plan_partisi = next(
                o
                for o in olaylar
                if o["kayit_turu"] == "mc_parti"
                and o["kosu_id"] == kosu.makbuz.kosu_id
                and o["kayit"]["kayitlar"][0]["kayit_turu"] == "mc_plan"
            )
            plan_partisi["kayit"]["kayitlar"][0]["kayit_id"] = ["unhashable-plan-id"]
            plan_partisi["icerik_ozeti"] = pilot._mc_ozet(plan_partisi["kayit"])
            olaylar = olaylar[: olaylar.index(plan_partisi) + 1]
        else:
            next(
                o
                for o in olaylar
                if o["kayit_turu"] == "bitis" and o["kosu_id"] == kosu.makbuz.kosu_id
            )["durum"] = "tamamlandi"
        ic["icerik_ozeti"] = pilot._mc_ozet(ic["kayit"])
        parti["icerik_ozeti"] = pilot._mc_ozet(parti["kayit"])
        yol = tmp_path / ("mc-" + boz + ".jsonl")
        yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
        if boz == "plan_kimligi_liste":
            once = yol.read_bytes()
            for eylem in (
                lambda yol=yol: pilot.PilotKayit(yol).oku(),
                lambda yol=yol: pilot_deneme(pilot.PilotKayit(yol)),
            ):
                try:
                    eylem()
                except pilot.PilotHatasi:
                    continue
                kabul_edilen.append(boz)
            assert yol.read_bytes() == once, (
                "Bozuk plan kimliğini reddeden ekleme dosyayı değiştirmemelidir."
            )
            continue
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            continue
        kabul_edilen.append(boz)
    assert kabul_edilen == [], (
        "Yeni okuyucu kanonik fakat geçersiz MC kaydını reddetmelidir."
    )

    plan_no = next(
        i
        for i, o in enumerate(fiziksel)
        if o["kayit_turu"] == "mc_parti"
        and o["kosu_id"] == kosu.makbuz.kosu_id
        and o["kayit"]["kayitlar"][0]["kayit_turu"] == "mc_plan"
    )
    sonuc_no = next(
        i
        for i, o in enumerate(fiziksel)
        if o["kayit_turu"] == "mc_parti"
        and o["kosu_id"] == kosu.makbuz.kosu_id
        and o["kayit"]["kayitlar"][0]["kayit_turu"] == "mc_senaryo"
    )
    for boz in ("gelecek_plan", "bozuk_ikinci_ic", "kapanmis_kosu"):
        olaylar = deepcopy(fiziksel)
        parti = olaylar[sonuc_no]
        if boz == "gelecek_plan":
            olaylar.insert(plan_no, olaylar.pop(sonuc_no))
            beklenen = "Kayıt bağı bulunamadı: " + planlar[0][1].olay_id
        elif boz == "bozuk_ikinci_ic":
            parti["kayit"]["kayitlar"][1]["kayit"]["plan_ref"] = "gelecek-plan"
            ic = parti["kayit"]["kayitlar"][1]
            ic["icerik_ozeti"] = pilot._mc_ozet(ic["kayit"])
            parti["icerik_ozeti"] = pilot._mc_ozet(parti["kayit"])
            beklenen = "Kayıt bağı bulunamadı: gelecek-plan"
        else:
            parti = deepcopy(parti)
            parti["kayit_id"] += ":sonra"
            for ic in parti["kayit"]["kayitlar"]:
                ic["kayit_id"] += ":sonra"
                ic["parti_ref"] = parti["kayit_id"]
            parti["icerik_ozeti"] = pilot._mc_ozet(parti["kayit"])
            olaylar.append(parti)
            beklenen = "MC kaynak veya açık koşu bağı uyuşmuyor."
        yol = tmp_path / (boz + ".jsonl")
        yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
        okuyucu = pilot.PilotKayit(yol)
        for oku in (okuyucu.oku, okuyucu.kurtar):
            with pytest.raises(pilot.PilotHatasi) as hata:
                oku()
            assert str(hata.value.__cause__) == beklenen
        yol.write_bytes(depo.yol.read_bytes())
        assert okuyucu.oku() == depo.oku()
        assert okuyucu.kurtar() == depo.kurtar()

    with depo.mc_yazim(m.deneme_id):
        korunan = depo._mc_baglam.tutacaklar is not None
        yeni_ctx, yeni_d, yeni_g = s13_kosu(depo, m, kaynak)
        with yeni_ctx as yeni_kosu:
            yeni_is, yeni_planlar = s13_plan(
                depo, yeni_kosu, yeni_d, yeni_g, deney="sira_v1", sayi=1
            )
            ilk_plan = yeni_planlar[0][0]
            nufus = len(ilk_plan["cekilis"]["indeksler"])
            ikinci = dict(
                ilk_plan,
                indeks=1,
                cekilis=istatistik.mc_plan(
                    "sira_v1",
                    yeni_is["anahtar"],
                    1,
                    n=nufus,
                    tohum=yeni_d["yontem_ayarlari"]["tohum"],
                ),
            )
            bozuk_ucuncu = dict(ikinci)
            once = depo.yol.read_bytes()
            with pytest.raises(pilot.PilotHatasi, match="MC plan indeksi yinelenmiş"):
                yeni_kosu.mc_planlari_kaydet(kayitlar=[ikinci, bozuk_ucuncu])
            assert depo.yol.read_bytes() == once
            if depo._mc_baglam.tutacaklar is None:
                assert not depo._mc_baglam.gecersiz
                yeni_kosu.mc_planlari_kaydet(kayitlar=[ikinci])
            else:
                assert depo._mc_baglam.gecersiz
                with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
                    yeni_kosu.mc_planlari_kaydet(kayitlar=[ikinci])
                assert depo.yol.read_bytes() == once
    taze = pilot.PilotKayit(depo.yol)
    plan_indeksleri = [
        o["kayit"]["indeks"]
        for o in taze.oku()
        if o["kayit_turu"] == "mc_plan" and o["kosu_id"] == yeni_kosu.makbuz.kosu_id
    ]
    assert plan_indeksleri == ([0] if korunan else [0, 1])
    with depo.mc_yazim(m.deneme_id):
        taze_ctx, taze_d, taze_g = s13_kosu(depo, m, kaynak)
        with taze_ctx as taze_kosu:
            _, taze_planlar = s13_plan(
                depo, taze_kosu, taze_d, taze_g, deney="sira_v1", sayi=1
            )
            assert len(taze_planlar) == 1
    assert pilot.PilotKayit(depo.yol).oku()


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


def pilot_kilit_arizasi(ariza, asama):
    if os.name == "nt":
        import msvcrt as kilit

        ad, al, birak = "locking", kilit.LK_LOCK, kilit.LK_UNLCK
    else:
        import fcntl as kilit

        ad, al, birak = "flock", kilit.LOCK_EX, kilit.LOCK_UN
    asil = getattr(kilit, ad)
    hedef = al if asama.startswith("kilit_al") else birak

    def kilitle(fd, mod, *args):
        if mod != hedef:
            return asil(fd, mod, *args)
        if asama.endswith("sonra"):
            asil(fd, mod, *args)
        raise OSError(asama)

    ariza.setattr(kilit, ad, kilitle)


def pilot_kilit_dosyasi_arizasi(ariza, asama):
    asil_ac = Path.open

    class KilitDosyasi:
        def __init__(self, dosya):
            self.dosya = dosya
            self.arama = 0

        def __enter__(self):
            self.dosya.__enter__()
            return self

        def __exit__(self, *args):
            self.dosya.__exit__(*args)
            if asama == "kilit_kapat":
                raise OSError(asama)

        def seek(self, *args):
            self.arama += 1
            if (asama, self.arama) in (("kilit_ilk_seek", 1), ("kilit_son_seek", 2)):
                raise OSError(asama)
            return self.dosya.seek(*args)

        def fileno(self):
            return self.dosya.fileno()

    def ac(yol, *args, **kwargs):
        if yol.suffix != ".lock":
            return asil_ac(yol, *args, **kwargs)
        if asama == "kilit_ac":
            raise OSError(asama)
        return KilitDosyasi(asil_ac(yol, *args, **kwargs))

    ariza.setattr(Path, "open", ac)


def pilot_adim_arizasi(ariza, depo, asama):
    def hata(*args, **kwargs):
        if asama.endswith("denetim"):
            raise OSError("LF sonucu doğrulanamıyor")
        raise OSError(asama)

    hedefler = {
        "kimlik": (pilot, "uuid4"),
        "kodla": (pilot, "kanonik"),
        "makbuz": (pilot, "Makbuz"),
        "dizin": (Path, "mkdir"),
        "ac": (os, "open"),
        "icerik": (os, "write"),
        "fsync": (os, "fsync"),
    }
    if asama in hedefler:
        ariza.setattr(*hedefler[asama], hata)
        return
    if asama.startswith(("kilit_al", "kilit_birak")):
        pilot_kilit_arizasi(ariza, asama)
        return
    if asama.startswith("kilit_"):
        pilot_kilit_dosyasi_arizasi(ariza, asama)
        return
    if asama.startswith("oku_"):
        asil_oku = Path.read_bytes
        okumalar = 0

        def oku(yol):
            nonlocal okumalar
            if yol == depo.yol:
                okumalar += 1
                if okumalar == int(asama[-1]):
                    raise OSError(asama)
            return asil_oku(yol)

        ariza.setattr(Path, "read_bytes", oku)
        return
    if asama.startswith("kapat"):
        asil_kapat = os.close

        def kapat(fd):
            asil_kapat(fd)
            if asama == "kapat_diger":
                raise RuntimeError(asama)
            raise OSError(asama)

        ariza.setattr(os, "close", kapat)
        return
    asil_yaz = os.write

    def yaz(fd, veri):
        if veri != b"\n":
            if asama == "icerik_kisa":
                return asil_yaz(fd, veri[:11])
            return asil_yaz(fd, veri)
        if asama.endswith("denetim"):
            for nesne, ad in (
                (os, "fstat"),
                (os, "lseek"),
                (os, "read"),
                (os, "open"),
                (Path, "read_bytes"),
                (Path, "stat"),
                (Path, "open"),
            ):
                ariza.setattr(nesne, ad, hata)
        if asama.startswith("lf_sonra"):
            asil_yaz(fd, veri)
        if asama == "lf_kisa":
            return 0
        hata()

    ariza.setattr(os, "write", yaz)


@pytest.mark.parametrize("giris", ["kosu", "duzelt"])
@pytest.mark.parametrize("asama", ["kilit_al", "oku_1"])
def test_pilot_yazma_hazirligi_io_hatasi_kesin_basarisizdir(
    tmp_path, monkeypatch, giris, asama
):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    with pilot_kosu(depo, deneme.deneme_id) as kosu:
        sonuc = pilot_sonuc(kosu)
        pilot_bitir(kosu)
    once = depo.yol.read_bytes()
    olaylar = depo.oku()
    hesap, api_hatasi = [], None

    with monkeypatch.context() as ariza:
        pilot_adim_arizasi(ariza, depo, asama)
        try:
            if giris == "kosu":
                with pilot_kosu(depo, deneme.deneme_id):
                    hesap.append("basladi")
            else:
                depo.duzelt(
                    sonuc.olay_id,
                    gerekce="hazirlik siniri",
                    yeni_degerler={"uyarilar": ["aciklama"]},
                )
        except OSError as hata:
            api_hatasi = hata

    assert type(api_hatasi) is pilot.PilotYazmaHatasi
    assert not isinstance(api_hatasi, pilot.PilotBelirsizHatasi)
    assert type(api_hatasi.__cause__) is OSError
    assert str(api_hatasi.__cause__) == asama
    assert hesap == []
    yeni = pilot.PilotKayit(depo.yol)
    assert yeni.yol.read_bytes() == once
    assert yeni.oku() == olaylar
    assert yeni.kurtar()["cozumsuz_kosular"] == []
    assert yeni.kurtar()["uyarilar"] == []
    iz = yeni.izle(sonuc.olay_id)
    assert iz["durum"] == "tamamlandi"
    assert iz["baslangic"]["kosu_id"] == kosu.makbuz.kosu_id
    assert iz["deneme"]["deneme_id"] == deneme.deneme_id
    assert iz["duzeltmeler"] == []

    with monkeypatch.context() as ariza:
        pilot_adim_arizasi(ariza, yeni, asama)
        with pytest.raises(OSError) as hata:
            yeni.oku()
    assert type(hata.value) is OSError


@pytest.mark.parametrize(
    "asama,gorunur",
    [
        ("kimlik", False),
        ("kodla", False),
        ("makbuz", False),
        ("dizin", False),
        ("kilit_ac", False),
        ("kilit_ilk_seek", False),
        ("kilit_al", False),
        ("kilit_al_sonra", False),
        ("oku_1", False),
        ("oku_2", False),
        ("ac", False),
        ("icerik", False),
        ("icerik_kisa", False),
        ("fsync", False),
        ("lf", False),
        ("lf_kisa", False),
        ("lf_sonra", True),
        ("lf_once_denetim", False),
        ("lf_sonra_denetim", True),
        ("kapat", True),
        ("kapat_diger", True),
        ("kilit_son_seek", True),
        ("kilit_birak", True),
        ("kilit_birak_sonra", True),
        ("kilit_kapat", True),
    ],
)
def test_pilot_yazma_adimlari_makbuz_ve_kurtarma_uyusur(
    tmp_path, monkeypatch, asama, gorunur
):
    depo = pilot.PilotKayit(tmp_path / "olaylar.jsonl")
    deneme = pilot_deneme(depo)
    makbuz, api_hatasi = None, None

    try:
        with pilot_kosu(depo, deneme.deneme_id) as kosu:
            sonuc = pilot_sonuc(kosu)
            once = depo.yol.read_bytes()
            with monkeypatch.context() as ariza:
                pilot_adim_arizasi(ariza, depo, asama)
                makbuz = pilot_bitir(kosu)
    except pilot.PilotYazmaHatasi as hata:
        api_hatasi = hata
    yeni = pilot.PilotKayit(depo.yol)
    tamamlandi = yeni.izle(sonuc.olay_id)["durum"] == "tamamlandi"
    belirsiz = asama.endswith("denetim")
    if belirsiz:
        assert type(api_hatasi).__name__ == "PilotBelirsizHatasi"
        assert isinstance(api_hatasi, pilot.PilotBelirsizHatasi)
        assert isinstance(api_hatasi, pilot.PilotYazmaHatasi)
        assert makbuz is None
        assert api_hatasi.kosu_id == kosu.makbuz.kosu_id
        assert api_hatasi.deneme_id == deneme.deneme_id
        assert api_hatasi.kayit_id.startswith("pilot_s03_v1:")
        assert api_hatasi.kayit_id.encode("utf-8") in yeni.yol.read_bytes()[len(once) :]
    else:
        assert (makbuz is not None) == tamamlandi
    assert tamamlandi == gorunur
    if gorunur:
        if belirsiz:
            assert yeni.oku()[-1]["kayit_id"] == api_hatasi.kayit_id
        else:
            assert api_hatasi is None
            assert makbuz.uyarilar
            assert yeni.oku()[-1]["kayit_id"] == makbuz.olay_id
        assert yeni.kurtar()["cozumsuz_kosular"] == []
    else:
        assert isinstance(api_hatasi, pilot.PilotYazmaHatasi)
        if not belirsiz:
            assert type(api_hatasi) is pilot.PilotYazmaHatasi
        assert yeni.kurtar()["cozumsuz_kosular"] == [kosu.makbuz.kosu_id]
        assert yeni.izle(sonuc.olay_id)["durum"] == "cozumsuz"
        assert [o["kayit_turu"] for o in yeni.oku()] == ["deneme", "baslangic", "sonuc"]
    assert yeni.yol.read_bytes().startswith(once)


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


@pytest.mark.parametrize(
    "hata", ["kok", "kok_bos", "rev-parse", "status", "bos", "calistirilamaz"]
)
def test_git_hatasi_kosu_kaydi_yazmaz(tmp_path, monkeypatch, hata):
    kimlik = anlik_hazirla(tmp_path)
    kayit.kayitla(P, ATR_N)
    yol = kayit.KAYIT_DIZINI / "deneme.jsonl"
    once = yol.read_bytes()

    def git_calistir(komut, **secenek):
        if hata == "calistirilamaz":
            raise OSError("git yok")
        if komut[1:] == ["rev-parse", "--show-toplevel"]:
            kod = 1 if hata == "kok" else 0
            cikti = "" if hata == "kok_bos" else str(kayit.PAKET.parent.resolve())
        else:
            kod = 1 if komut[1] == hata else 0
            cikti = "" if hata == "bos" or komut[1] == "status" else "abc123"
        sonuc = subprocess.CompletedProcess(komut, kod, cikti, "git hatası")
        if secenek.get("check"):
            sonuc.check_returncode()
        return sonuc

    monkeypatch.setattr(subprocess, "run", git_calistir)
    with pytest.raises(kayit.KayitHatasi, match="Git"):
        kayit.kosu(kimlik, tmp_path, p=P, atr_n=ATR_N)
    assert yol.read_bytes() == once
    assert not (tmp_path / "rapor").exists()


@pytest.mark.parametrize(
    "ortam",
    ["yok", "depo", "harf", "agac", "indeks", "nesneler", "ortak", "yapilandirma"],
)
def test_git_proje_koku_ve_kayit_istisnasi(tmp_path, monkeypatch, ortam):
    depolar = [tmp_path / "proje", tmp_path / "baska"]
    surumler = []
    for depo in depolar:
        depo.mkdir()
        (depo / "tansu").mkdir()
        (depo / "tansu" / "kod.py").write_text(depo.name, encoding="utf-8")
        for komut in (
            ["init"],
            ["add", "tansu/kod.py"],
            [
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.com",
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-m",
                depo.name,
            ],
        ):
            subprocess.run(["git", *komut], cwd=depo, check=True, capture_output=True)
        surumler.append(
            subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=depo,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
    assert surumler[0] != surumler[1]
    proje, baska = depolar
    ayarlar = {
        "yok": {},
        "depo": {"GIT_DIR": str(baska / ".git"), "GIT_WORK_TREE": str(baska)},
        "harf": {"gIt_DiR": str(baska / ".git"), "gIt_WoRk_TrEe": str(baska)},
        "agac": {"GIT_WORK_TREE": str(baska)},
        "indeks": {"GIT_INDEX_FILE": str(baska / ".git" / "index")},
        "nesneler": {"GIT_OBJECT_DIRECTORY": str(baska / ".git" / "objects")},
        "ortak": {"GIT_COMMON_DIR": str(baska / ".git")},
        "yapilandirma": {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.worktree",
            "GIT_CONFIG_VALUE_0": str(baska),
        },
    }
    for ad, deger in ayarlar[ortam].items():
        monkeypatch.setenv(ad, deger)
    once = dict(os.environ)
    monkeypatch.setattr(kayit, "PAKET", proje / "tansu")
    for klasor in (proje, proje / "tansu", tmp_path, baska):
        monkeypatch.chdir(klasor)
        assert kayit._git() == (surumler[0], False)
    (proje / "kayit").mkdir()
    (proje / "kayit" / "deneme.jsonl").write_text("{}\n", encoding="utf-8")
    assert kayit._git() == (surumler[0], False)
    (proje / "tansu" / "kod.py").write_text("degisti", encoding="utf-8")
    assert kayit._git() == (surumler[0], True)
    assert dict(os.environ) == once
    alt = proje / "alt"
    (alt / "tansu").mkdir(parents=True)
    monkeypatch.setattr(kayit, "PAKET", alt / "tansu")
    with pytest.raises(kayit.KayitHatasi, match="Git"):
        kayit._git()


def test_s10_bozuk_deneme_baslangic_makbuzu_uretemez(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "pilot.jsonl")
    makbuz = pilot_deneme(depo)
    kayitlar = depo.oku()
    kayitlar[0]["risk_ayarlari"]["oran"] = Decimal("0.9")
    depo.yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in kayitlar))
    hesap = []
    try:
        with pilot_kosu(depo, makbuz.deneme_id):
            hesap.append("basladi")
    except pilot.PilotHatasi:
        pass
    assert hesap == [], "Tam ayarı bozulmuş deneme hesap başlatamaz"
    assert [o["kayit_turu"] for o in depo.oku()] == ["deneme"]


def pilot_donem_sonucu(kosu, donem, **degisiklik):
    alanlar = dict(
        is_id="XXXX",
        donem=donem,
        durum="tamamlandi",
        islem_referanslari=[],
        birimler={"net_sonuc": "TL"},
        muhasebe_politikasi="tani_referans_v1",
        uyarilar=[],
        cikti_referanslari=[],
        icerik={"adaylar": [], "durumlar": {}},
    )
    return kosu.donem_sonucu_kaydet(**(alanlar | degisiklik))


@pytest.mark.parametrize("durumlar", [{}, {"TEST": {"durum": "bekliyor"}}])
def test_s10_donem_makbuzu_kayitli_is_donem_ve_tek_yayin_ister(tmp_path, durumlar):
    depo = pilot.PilotKayit(tmp_path / "pilot.jsonl")
    deneme = pilot_deneme(depo)
    donem = depo.deneme_oku(deneme.deneme_id)["donemler"][0]
    with pilot_kosu(depo, deneme.deneme_id, is_listesi=["XXXX", "YYYY"]) as kosu:
        with pytest.raises(pilot.PilotHatasi, match="başlangıç listesinde"):
            pilot_donem_sonucu(kosu, donem, is_id="yok")
        with pytest.raises(pilot.PilotHatasi, match="kayıtlı denemede"):
            pilot_donem_sonucu(kosu, donem | dict(baslangic=dt.date(2024, 1, 1)))
        sonuc = pilot_donem_sonucu(
            kosu, donem, icerik={"adaylar": [], "durumlar": durumlar}
        )
        for is_id in ("XXXX", "YYYY"):
            with pytest.raises(pilot.PilotHatasi, match="zaten kayıtlı"):
                pilot_donem_sonucu(kosu, donem, is_id=is_id)
        kosu.bitir(
            durum="hata",
            tamamlanan=["XXXX"],
            basarisiz=["YYYY"],
            yontemler=[],
            olculer={},
            cikti_referanslari=[sonuc.olay_id],
            ozetler={},
        )
    once = depo.yol.read_bytes()
    iz = pilot.PilotKayit(depo.yol).izle(sonuc.olay_id)
    assert iz["sonuc"]["icerik"]["durumlar"] == durumlar
    assert depo.yol.read_bytes() == once
    assert iz["sonuc"]["sonuc_turu"] == "donem_v1"
    assert "sinyal_id" not in iz["sonuc"] and iz["sonuc"]["islem_referanslari"] == []
    assert iz["durum"] == "hata"


def test_s10_donem_islem_ve_cocuk_referansi_ayni_kosuya_aittir(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "pilot.jsonl")
    ilk = pilot_deneme(depo)
    d = depo.deneme_oku(ilk.deneme_id)["donemler"][0]
    d2 = d | dict(baslangic=dt.date(2024, 1, 1), bitis=dt.date(2024, 12, 31))
    deneme = pilot_deneme(depo, donemler=[d, d2])

    def islem(kosu, donem):
        return kosu.islem_kaydet(
            sinyal_id="gercek-sinyal",
            donem=donem,
            birimler={"adet": "adet"},
            muhasebe_politikasi="tani_referans_v1",
            uyarilar=[],
            cikti_referanslari=[],
            olaylar=[dict(dolum_id="gercek-dolum", yon="alis", adet=1, fiyat=100)],
        )

    with pilot_kosu(depo, deneme.deneme_id) as kosu:
        eski_islem = islem(kosu, d)
        eski_sonuc = pilot_donem_sonucu(
            kosu, d, islem_referanslari=[eski_islem.olay_id]
        )
        pilot_bitir(kosu)
    with pilot_kosu(depo, deneme.deneme_id, is_listesi=["XXXX", "YYYY"]) as kosu:
        baska_donem = islem(kosu, d2)
        for ref in (eski_islem.olay_id, baska_donem.olay_id):
            with pytest.raises(pilot.PilotHatasi, match="başka koşuya veya döneme"):
                pilot_donem_sonucu(kosu, d, islem_referanslari=[ref])
        with pytest.raises(pilot.PilotHatasi, match="başka koşuya"):
            pilot_donem_sonucu(kosu, d, cikti_referanslari=[eski_sonuc.olay_id])
        yeni_islem = islem(kosu, d)
        with pytest.raises(pilot.PilotHatasi, match="yinelenmiş"):
            pilot_donem_sonucu(kosu, d, islem_referanslari=[yeni_islem.olay_id] * 2)
        yeni = pilot_donem_sonucu(kosu, d, islem_referanslari=[yeni_islem.olay_id])
        ikinci = pilot_donem_sonucu(
            kosu,
            d2,
            is_id="YYYY",
            islem_referanslari=[baska_donem.olay_id],
            cikti_referanslari=[yeni.olay_id],
        )
        kosu.bitir(
            durum="tamamlandi",
            tamamlanan=["XXXX", "YYYY"],
            basarisiz=[],
            yontemler=[],
            olculer={},
            cikti_referanslari=[yeni.olay_id, ikinci.olay_id],
            ozetler={},
        )
    assert depo.izle(ikinci.olay_id)["sonuc"]["cikti_referanslari"] == [yeni.olay_id]


def pilot_arama_ust(depo, degerler=(0.010, 0.015)):
    donemler = [
        dict(
            ad=str(y),
            baslangic=dt.date(y, 1, 1),
            bitis=dt.date(y, 12, 31),
            isinma_baslangici=dt.date(2018, 1, 1),
            sinir_surumu="bagimsiz_donem_v1",
        )
        for y in range(2025, 2020, -1)
    ]
    donemler.append(donemler[-1] | dict(ad="birlesik", bitis=dt.date(2025, 12, 31)))
    return pilot_deneme(
        depo,
        donemler=donemler,
        yontem_ayarlari=dict(
            yontem="kayitli_izgara_v1",
            tekrar=0,
            secim_politikasi="genis_bolge_net_r_v1",
            olcu_politikasi="bagimsiz_olcu_v1",
            eksenler=[dict(ad="esik", birim="oran", degerler=list(degerler))],
            hucre_yontemi=dict(
                yontem="kayitli_donem_v1",
                tekrar=0,
                yurutme_surumu="bagimsiz_islem_v1",
                fiyat_politikasi="aof_v1",
                muhasebe_politikasi="tani_referans_v1",
            ),
        ),
    )


def pilot_arama_hisse_olcusu(kosu, cocuk, donem, sembol, islemsiz):
    olcu = dict(
        politika="bagimsiz_olcu_v1",
        islemler=[],
        acik_kismi=[],
        egri_tanimi=dict(referanslar=[]),
    )
    if islemsiz:
        return dict(sembol=sembol, durum="islemsiz", olcu=olcu)
    islem_id = f"islem:{donem['ad']}"
    if sembol != "TEST":
        islem_id += f":{sembol}"
    islem = kosu.islem_kaydet(
        sinyal_id=f"{cocuk['deneme_id']}:{donem['ad']}:{sembol}",
        donem=donem,
        birimler={"adet": "adet"},
        muhasebe_politikasi="tani_referans_v1",
        uyarilar=[],
        cikti_referanslari=[],
        olaylar=[
            dict(pozisyon=dict(risk_girdisi=dict(islem_id=islem_id, sembol=sembol)))
        ],
    )
    olcu["islemler"] = [dict(islem_id=islem_id, islem_ref=islem.olay_id)]
    olcu["egri_tanimi"]["referanslar"] = [islem.olay_id]
    return dict(sembol=sembol, durum="tamamlandi", olcu=olcu)


def pilot_arama_donemi(kosu, cocuk, donem, hata, *, hisseler=("TEST",), islemsiz=()):
    semboller = [
        pilot_arama_hisse_olcusu(kosu, cocuk, donem, s, s in islemsiz) for s in hisseler
    ]
    refs = [i["islem_ref"] for s in semboller for i in s["olcu"]["islemler"]]
    neden = "hesap başarısız" if hata else None
    sonuc = pilot_donem_sonucu(
        kosu,
        donem,
        is_id=f"donem:{donem['ad']}",
        durum="hata" if hata else "tamamlandi",
        islem_referanslari=refs,
        icerik=dict(
            deneme_id=cocuk["deneme_id"],
            kosu_id=kosu.makbuz.kosu_id,
            ayar_parmak_izi=cocuk["ayar_parmak_izi"],
            strateji_ayar_parmak_izi=cocuk["strateji"]["ayar_parmak_izi"],
            neden=neden,
            asama="islem" if hata else None,
            durumlar={s: dict(durum="bekliyor") for s in hisseler},
        ),
    )
    return dict(
        donem=donem,
        is_id=f"donem:{donem['ad']}",
        durum="hesap_hatasi" if hata else "tamamlandi",
        neden=neden,
        asama="islem" if hata else None,
        sonuc_ref=sonuc.olay_id,
        islem_referanslari=refs,
        beklenen_semboller=list(hisseler),
        semboller=semboller,
    )


def pilot_arama_hucresi(
    depo,
    ust,
    indeks,
    hata=False,
    *,
    basarisiz_donemler=(),
    hisseler=("TEST",),
    islemsiz=(),
):
    esik = ust["yontem_ayarlari"]["eksenler"][0]["degerler"][indeks]
    strateji = pilot.katalog.legacy_coz("bugun", sayisal_ayarlar={"esik": esik})
    kayit = pilot_deneme(
        depo,
        strateji,
        ust_deneme=ust["deneme_id"],
        baglar={"izgara_ust_deneme": ust["deneme_id"]},
        donemler=ust["donemler"],
        yontem_ayarlari=ust["yontem_ayarlari"]["hucre_yontemi"],
    )
    cocuk = depo.deneme_oku(kayit.deneme_id)
    isler = [f"donem:{d['ad']}" for d in cocuk["donemler"]]
    with pilot_kosu(depo, kayit.deneme_id, is_listesi=isler) as kosu:
        donemler, bitis, hata = pilot_arama_cocuk_donemleri(
            kosu, cocuk, isler, hata, basarisiz_donemler, hisseler, islemsiz
        )
    return dict(
        indeks=[indeks],
        is_id=f"hucre:{indeks}",
        ayarlar={"esik": esik},
        ust_deneme_id=ust["deneme_id"],
        deneme_id=kayit.deneme_id,
        kosu_id=kosu.makbuz.kosu_id,
        ayar_parmak_izi=kayit.ayar_ozeti,
        strateji_ayar_parmak_izi=strateji.ayar_parmak_izi,
        tam_ayarlar=pilot._ayarlar(cocuk),
        kayit_makbuzu=asdict(kayit),
        baslangic_makbuzu=asdict(kosu.makbuz),
        bitis_makbuzu=asdict(bitis),
        durum="hesap_hatasi" if hata else "tamamlandi",
        neden="hesap başarısız" if hata else None,
        donemler=donemler,
    )


def pilot_arama_cocuk_donemleri(
    kosu, cocuk, isler, hata, basarisiz_donemler, hisseler, islemsiz
):
    donemler = [
        pilot_arama_donemi(
            kosu,
            cocuk,
            d,
            hata or d["ad"] in basarisiz_donemler,
            hisseler=hisseler,
            islemsiz=islemsiz,
        )
        for d in cocuk["donemler"]
    ]
    basarisiz = [d["is_id"] for d in donemler if d["durum"] == "hesap_hatasi"]
    hata = bool(basarisiz)
    bitis = kosu.bitir(
        durum="hata" if hata else "tamamlandi",
        tamamlanan=[i for i in isler if i not in basarisiz],
        basarisiz=basarisiz,
        yontemler=[],
        olculer={},
        cikti_referanslari=[d["sonuc_ref"] for d in donemler],
        ozetler={},
    )
    return donemler, bitis, hata


@pytest.fixture
def pilot_arama(tmp_path, request):
    depo = pilot.PilotKayit(tmp_path / "arama.jsonl")
    kayit = pilot_arama_ust(depo)
    ust = depo.deneme_oku(kayit.deneme_id)
    with pilot_kosu(
        depo, kayit.deneme_id, is_listesi=["arama", "hucre:0", "hucre:1"]
    ) as kosu:
        hucreler = [
            pilot_arama_hucresi(depo, ust, 0),
            pilot_arama_hucresi(depo, ust, 1, getattr(request, "param", False)),
        ]
        yield (
            depo,
            kosu,
            dict(
                is_id="arama",
                hucreler=hucreler,
                bolgeler=[],
                politika_surumu="genis_bolge_net_r_v1",
                birimler={"net_r": "R"},
                uyarilar=[],
                cikti_referanslari=[
                    d["sonuc_ref"] for h in hucreler for d in h["donemler"]
                ],
            ),
        )


def pilot_arama_bitir(kosu, refs, **degisiklik):
    return kosu.bitir(
        **(
            dict(
                durum="tamamlandi",
                tamamlanan=["arama", "hucre:0", "hucre:1"],
                basarisiz=[],
                yontemler=[],
                olculer={},
                cikti_referanslari=refs,
                ozetler={},
            )
            | degisiklik
        )
    )


def test_s11_arama_gercek_cocuk_sonuclarini_yayinlar_eski_kosu_kisitini_korur(
    pilot_arama,
):
    depo, kosu, girdi = pilot_arama
    once = depo.yol.read_bytes()
    makbuz = kosu.arama_sonucu_kaydet(**girdi)
    assert isinstance(makbuz, pilot.Makbuz), "Arama gerçek kalıcı kayıt makbuzu vermeli"
    sonuc = pilot.PilotKayit(depo.yol).izle(makbuz.olay_id)["sonuc"]
    assert sonuc["sonuc_turu"] == "arama_v1"
    assert sonuc["deneme_id"] == kosu.makbuz.deneme_id
    assert sonuc["hucreler"] == girdi["hucreler"]
    assert sonuc["cikti_referanslari"] == girdi["cikti_referanslari"]
    cocuk = girdi["hucreler"][0]
    donem_izi = pilot.PilotKayit(depo.yol).izle(cocuk["donemler"][0]["sonuc_ref"])
    assert donem_izi["deneme"]["ust_deneme_id"] == kosu.makbuz.deneme_id
    assert donem_izi["baslangic"]["kosu_id"] == cocuk["kosu_id"]
    assert (
        donem_izi["sonuc"]["islem_referanslari"]
        == cocuk["donemler"][0]["islem_referanslari"]
    )
    assert "sinyal_id" not in sonuc
    assert depo.yol.read_bytes().startswith(once)
    with pytest.raises(pilot.PilotHatasi, match="zaten kayıtlı"):
        kosu.arama_sonucu_kaydet(**girdi)
    d = girdi["hucreler"][0]["donemler"][0]
    with pytest.raises(pilot.PilotHatasi, match="başka koşuya"):
        pilot_donem_sonucu(
            kosu, d["donem"], is_id="arama", cikti_referanslari=[d["sonuc_ref"]]
        )
    with pytest.raises(pilot.PilotHatasi, match="Her iş bir kez"):
        pilot_arama_bitir(kosu, [makbuz.olay_id], tamamlanan=["arama", "hucre:0"])
    with pytest.raises(pilot.PilotHatasi, match="Her iş bir kez"):
        pilot_arama_bitir(
            kosu, [makbuz.olay_id], tamamlanan=["arama", "hucre:0", "hucre:1", "arama"]
        )
    pilot_arama_bitir(kosu, [makbuz.olay_id])
    assert depo.izle(makbuz.olay_id)["durum"] == "tamamlandi"


@pytest.mark.parametrize(
    "boz",
    [
        pytest.param(
            lambda g: g["hucreler"][0].update(ust_deneme_id="baska-ust"), id="parent"
        ),
        pytest.param(
            lambda g: g["hucreler"][0].update(deneme_id=g["hucreler"][1]["deneme_id"]),
            id="child",
        ),
        pytest.param(
            lambda g: g["hucreler"][0].update(kosu_id=g["hucreler"][1]["kosu_id"]),
            id="run",
        ),
        pytest.param(
            lambda g: g["hucreler"][0].update(ayar_parmak_izi="sahte"), id="full-hash"
        ),
        pytest.param(
            lambda g: g["hucreler"][0].update(strateji_ayar_parmak_izi="sahte"),
            id="strategy-hash",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["tam_ayarlar"]["risk_ayarlari"].update(
                oran=Decimal("0.9")
            ),
            id="full-settings",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["ayarlar"].update(esik=0.015), id="axis-value"
        ),
        pytest.param(
            lambda g: g["hucreler"][0].update(indeks=[1]), id="duplicate-coordinate"
        ),
        pytest.param(lambda g: g["hucreler"].pop(), id="missing-cell"),
        pytest.param(lambda g: g["hucreler"][0]["donemler"].pop(), id="missing-period"),
        pytest.param(
            lambda g: g["hucreler"][0]["donemler"][0].update(sonuc_ref="yok"),
            id="missing-result",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["donemler"][0].update(
                sonuc_ref=g["hucreler"][1]["donemler"][0]["sonuc_ref"]
            ),
            id="cross-child-result",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["donemler"][0].update(
                sonuc_ref=g["hucreler"][0]["donemler"][1]["sonuc_ref"]
            ),
            id="cross-period-result",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["donemler"][0].update(
                islem_referanslari=g["hucreler"][1]["donemler"][0]["islem_referanslari"]
            ),
            id="cross-child-trade",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["donemler"][0]["semboller"][0]["olcu"][
                "islemler"
            ][0].update(
                islem_ref=g["hucreler"][1]["donemler"][0]["islem_referanslari"][0]
            ),
            id="measured-trade",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["baslangic_makbuzu"].update(ayar_ozeti="sahte"),
            id="start-receipt",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["kayit_makbuzu"].update(olay_id="sahte"),
            id="registration-receipt",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["donemler"][0].update(sonuc_ref=None),
            id="unpublished-success",
        ),
        pytest.param(lambda g: g["cikti_referanslari"].pop(), id="missing-output"),
        pytest.param(
            lambda g: g["cikti_referanslari"].append(g["cikti_referanslari"][0]),
            id="duplicate-output",
        ),
        pytest.param(
            lambda g: g["hucreler"][0].update(durum="tanimlanmamis", neden="sahte"),
            id="unknown-status",
        ),
        pytest.param(
            lambda g: g["hucreler"][0]["donemler"][0]["semboller"][0]["olcu"].update(
                politika="eksen_maksimin_legacy_v1"
            ),
            id="measurement-policy",
        ),
    ],
)
def test_s11_arama_sahte_hucre_bagini_yazmaz(pilot_arama, boz):
    depo, kosu, girdi = pilot_arama
    girdi = deepcopy(girdi)
    boz(girdi)
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Sahte çocuk veya sonuç bağı kalıcı arama sonucu olamaz"
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize("pilot_arama", [True], indirect=True)
def test_s11_basarisiz_cocuk_tam_basari_olarak_bitirilemez(pilot_arama):
    depo, kosu, girdi = pilot_arama
    makbuz = kosu.arama_sonucu_kaydet(**girdi)
    refs = [makbuz.olay_id] if makbuz is not None else []
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        pilot_arama_bitir(kosu, refs)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Başarısız çocuk tamamlanan listesiyle tam başarıya çevrilemez"
    assert depo.yol.read_bytes() == once
    pilot_arama_bitir(
        kosu,
        refs,
        durum="hata",
        tamamlanan=["arama", "hucre:0"],
        basarisiz=["hucre:1"],
    )
    assert depo.izle(makbuz.olay_id)["durum"] == "hata"


@pytest.mark.parametrize(
    "tur,yol,deger",
    [
        ("deneme", ("ust_deneme_id",), "baska-ust"),
        ("deneme", ("baglar", "izgara_ust_deneme"), "baska-ust"),
        ("deneme", ("risk_ayarlari", "oran"), Decimal("0.7")),
        ("deneme", ("yontem_ayarlari", "muhasebe_politikasi"), "baska-yontem"),
        ("baslangic", ("ayar_parmak_izi",), "sahte-ozet"),
        ("baslangic", ("deneme_id",), "baska-cocuk"),
        ("sonuc", ("kosu_id",), "baska-kosu"),
        ("sonuc", ("ayar_parmak_izi",), "sahte-ozet"),
        ("sonuc", ("icerik", "strateji_ayar_parmak_izi"), "sahte-strateji"),
        ("sonuc", ("donem", "baslangic"), dt.date(2000, 1, 1)),
        ("islem", ("kosu_id",), "baska-kosu"),
        ("islem", ("donem", "baslangic"), dt.date(2000, 1, 1)),
        ("islem", ("ayar_parmak_izi",), "sahte-ozet"),
        ("islem", ("olaylar", 0, "pozisyon", "risk_girdisi", "sembol"), "BASKA"),
        ("islem", ("olaylar", 0, "pozisyon", "risk_girdisi", "sembol"), None),
        ("sonuc", ("icerik", "durumlar"), {}),
        ("bitis", ("tamamlanan",), []),
        ("ust", ("ayar_parmak_izi",), "sahte-ust-ozet"),
    ],
)
def test_s11_arama_gercek_kaydin_bagini_tekrar_dogrular(pilot_arama, tur, yol, deger):
    depo, kosu, girdi = pilot_arama
    h = girdi["hucreler"][0]
    olaylar = depo.oku()
    kimlik = kosu.makbuz.deneme_id if tur == "ust" else h["deneme_id"]
    kayit_turu = "deneme" if tur == "ust" else tur
    olay = next(
        o
        for o in olaylar
        if o["kayit_turu"] == kayit_turu and o.get("deneme_id") == kimlik
    )
    alan = olay
    for ad in yol[:-1]:
        alan = alan[ad]
    alan[yol[-1]] = deger
    depo.yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Yuva doğru görünse de gerçek kayıt bağı tekrar doğrulanmalı"
    assert depo.yol.read_bytes() == once


def test_s11_yayin_olmadan_ust_arama_tamamlanamaz(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "arama.jsonl")
    kayit = pilot_arama_ust(depo)
    with pilot_kosu(
        depo, kayit.deneme_id, is_listesi=["arama", "hucre:0", "hucre:1"]
    ) as kosu:
        reddedildi = False
        try:
            pilot_arama_bitir(kosu, [])
        except pilot.PilotHatasi:
            reddedildi = True
        assert reddedildi, "Yayımlanmamış arama tam başarı olamaz"


def test_s11_kayitsiz_cocuk_alti_gerekceli_yuvayla_kalir(pilot_arama):
    depo, kosu, girdi = pilot_arama
    girdi = deepcopy(girdi)
    h = girdi["hucreler"][1]
    h.update(
        deneme_id=None,
        kosu_id=None,
        ayar_parmak_izi=None,
        kayit_makbuzu=None,
        baslangic_makbuzu=None,
        bitis_makbuzu=None,
        durum="kayit_hatasi",
        neden="kayıt reddedildi",
    )
    for d in h["donemler"]:
        d.update(
            durum="baslamadi",
            neden="kayıt reddedildi",
            asama=None,
            sonuc_ref=None,
            islem_referanslari=[],
            semboller=[],
            beklenen_semboller=[],
        )
    girdi["cikti_referanslari"] = [
        d["sonuc_ref"] for d in girdi["hucreler"][0]["donemler"]
    ]
    makbuz = kosu.arama_sonucu_kaydet(**girdi)
    assert isinstance(makbuz, pilot.Makbuz), (
        "Gerekçeli çalışmamış hücre görünür kalmalı"
    )
    kayit = depo.izle(makbuz.olay_id)["sonuc"]["hucreler"][1]
    assert kayit["deneme_id"] is None
    assert [d["durum"] for d in kayit["donemler"]] == ["baslamadi"] * 6
    assert all(d["neden"] == "kayıt reddedildi" for d in kayit["donemler"])


def test_s11_secilen_bolge_kayitsiz_cocuga_baglanamaz(pilot_arama):
    depo, kosu, girdi = pilot_arama
    girdi = deepcopy(girdi)
    h = girdi["hucreler"][1]
    h.update(
        deneme_id=None,
        kosu_id=None,
        ayar_parmak_izi=None,
        kayit_makbuzu=None,
        baslangic_makbuzu=None,
        bitis_makbuzu=None,
        durum="kayit_hatasi",
        neden="kayıt reddedildi",
    )
    for d in h["donemler"]:
        d.update(
            durum="baslamadi",
            neden="kayıt reddedildi",
            sonuc_ref=None,
            islem_referanslari=[],
            semboller=[],
        )
    girdi["cikti_referanslari"] = [
        d["sonuc_ref"] for d in girdi["hucreler"][0]["donemler"]
    ]
    ust = depo.deneme_oku(kosu.makbuz.deneme_id)
    bolge = pilot_arama_bolgesi(ust, girdi["hucreler"])
    bolge.update(secilen=[1], secilen_deneme_id=None, neden=None)
    girdi["bolgeler"] = [bolge]
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Kaydı olmayan çocuk seçilmiş sonuç olarak yayımlanamaz"


def test_s11_yayin_sonrasi_hata_asli_hatayi_kapatmaz(pilot_arama):
    depo, kosu, girdi = pilot_arama
    kosu.arama_sonucu_kaydet(**girdi)
    bitis = None
    try:
        bitis = pilot_arama_bitir(
            kosu,
            [],
            durum="hata",
            tamamlanan=[],
            basarisiz=["arama", "hucre:0", "hucre:1"],
        )
    except pilot.PilotHatasi:
        pass
    assert isinstance(bitis, pilot.Makbuz), (
        "Koşu bağlamının hata kapanışı asıl hatayı örtemez"
    )
    assert depo.oku()[-1]["durum"] == "hata"


def test_s11_kosu_baglami_yayindan_sonraki_asli_hatayi_korur(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "arama.jsonl")
    kayit = pilot_arama_ust(depo)
    ust = depo.deneme_oku(kayit.deneme_id)
    asil = RuntimeError("yayından sonraki asıl hata")
    yakalanan = None
    try:
        with pilot_kosu(
            depo, kayit.deneme_id, is_listesi=["arama", "hucre:0", "hucre:1"]
        ) as kosu:
            hucreler = [pilot_arama_hucresi(depo, ust, i) for i in range(2)]
            makbuz = kosu.arama_sonucu_kaydet(
                is_id="arama",
                hucreler=hucreler,
                bolgeler=[],
                politika_surumu="genis_bolge_net_r_v1",
                birimler={"net_r": "R"},
                uyarilar=[],
                cikti_referanslari=[
                    d["sonuc_ref"] for h in hucreler for d in h["donemler"]
                ],
            )
            once = depo.yol.read_bytes()
            raise asil
    except (RuntimeError, pilot.PilotHatasi) as hata:
        yakalanan = hata
    assert yakalanan is asil, "Hata kapanışı bağlamdan çıkan asıl hatayı değiştiremez"
    assert depo.yol.read_bytes().startswith(once)
    assert depo.izle(makbuz.olay_id)["durum"] == "hata"
    assert depo.oku()[-1]["basarisiz"] == ["arama", "hucre:0", "hucre:1"]


def test_s11_reddedilen_baslangic_makbuzu_basarili_sonuc_olamaz(pilot_arama):
    depo, kosu, girdi = pilot_arama
    girdi = deepcopy(girdi)
    h = girdi["hucreler"][1]
    h.update(
        durum="hesap_hatasi",
        neden="başlangıç makbuzu uyuşmuyor",
        baslangic_makbuzu=None,
        bitis_makbuzu=None,
    )
    for d in h["donemler"]:
        d.update(
            durum="baslamadi",
            neden=h["neden"],
            sonuc_ref=None,
            islem_referanslari=[],
            semboller=[],
        )
    girdi["cikti_referanslari"] = [
        d["sonuc_ref"] for d in girdi["hucreler"][0]["donemler"]
    ]
    makbuz = kosu.arama_sonucu_kaydet(**girdi)
    assert depo.izle(makbuz.olay_id)["sonuc"]["hucreler"][1]["durum"] == "hesap_hatasi"
    assert depo.izle(makbuz.olay_id)["sonuc"]["hucreler"][1]["kosu_id"] == h["kosu_id"]


@pytest.mark.parametrize("belirsiz", [False, True])
def test_s11_arama_yazma_hatasi_sahte_makbuz_ve_bitis_uretmez(
    tmp_path, monkeypatch, belirsiz
):
    depo = pilot.PilotKayit(tmp_path / "arama.jsonl")
    kayit = pilot_arama_ust(depo)
    ust = depo.deneme_oku(kayit.deneme_id)
    tur = pilot.PilotBelirsizHatasi if belirsiz else pilot.PilotYazmaHatasi

    def yazma_hatasi(*args):
        raise OSError("arama yazma hatası")

    with pytest.raises(tur):
        with pilot_kosu(
            depo, kayit.deneme_id, is_listesi=["arama", "hucre:0", "hucre:1"]
        ) as kosu:
            hucreler = [pilot_arama_hucresi(depo, ust, i) for i in range(2)]
            once = depo.oku()
            if belirsiz:
                monkeypatch.setattr(
                    pilot, "_lf_yaz", lambda *a: (None, OSError("belirsiz yayın"))
                )
            else:
                monkeypatch.setattr(pilot, "_icerik_yaz", yazma_hatasi)
            kosu.arama_sonucu_kaydet(
                is_id="arama",
                hucreler=hucreler,
                bolgeler=[],
                politika_surumu="genis_bolge_net_r_v1",
                birimler={"net_r": "R"},
                uyarilar=[],
                cikti_referanslari=[
                    d["sonuc_ref"] for h in hucreler for d in h["donemler"]
                ],
            )
    assert depo.oku() == once
    assert depo.kurtar()["cozumsuz_kosular"] == [kosu.makbuz.kosu_id]


def pilot_arama_bolge_ozeti(h, no, sembol):
    d = h["donemler"][no]
    s = next((s for s in d["semboller"] if s["sembol"] == sembol), None)
    durum = s["durum"] if d["durum"] == "tamamlandi" and s else d["durum"]
    return dict(
        indeks=h["indeks"],
        deneme_id=h["deneme_id"],
        durum=durum,
        kapali_islem_sayisi=(
            1 if durum == "tamamlandi" else 0 if durum == "islemsiz" else None
        ),
        toplam_net_r=1.0 if durum == "tamamlandi" else None,
    )


def pilot_arama_bolgesi(ust, hucreler, no=0, sembol="TEST"):
    ozetler = [pilot_arama_bolge_ozeti(h, no, sembol) for h in hucreler]
    bolge = saglamlik.sec(
        dict(eksenler=ust["yontem_ayarlari"]["eksenler"]),
        ozetler,
        politika="genis_bolge_net_r_v1",
    )
    h = next((h for h in hucreler if h["indeks"] == bolge["secilen"]), None)
    return bolge | dict(
        strateji_id=ust["strateji"]["kayit_id"],
        donem=ust["donemler"][no],
        sembol=sembol,
        secilen_deneme_id=h["deneme_id"] if h else None,
    )


@pytest.mark.parametrize("pilot_arama", [True], indirect=True)
def test_s11_bolge_basarisiz_donemi_secilmis_yayinlamaz(pilot_arama):
    depo, kosu, girdi = pilot_arama
    ust = depo.deneme_oku(kosu.makbuz.deneme_id)
    bolge = pilot_arama_bolgesi(ust, girdi["hucreler"])
    assert bolge["secilen"] is None
    assert bolge["hucreler"][1]["durum"] == "hesap_hatasi"
    bolge.update(
        secilen=[1], secilen_deneme_id=girdi["hucreler"][1]["deneme_id"], neden=None
    )
    girdi["bolgeler"] = [bolge]
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Başarısız dönem tam bölge açıklamasıyla da seçilemez"
    assert depo.yol.read_bytes() == once


@pytest.fixture
def pilot_arama_secilen(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "arama.jsonl")
    kayit = pilot_arama_ust(depo, (0.010, 0.012, 0.015))
    ust = depo.deneme_oku(kayit.deneme_id)
    with pilot_kosu(
        depo, kayit.deneme_id, is_listesi=["arama", "hucre:0", "hucre:1", "hucre:2"]
    ) as kosu:
        hucreler = [
            pilot_arama_hucresi(
                depo, ust, i, basarisiz_donemler=("2024",) if i == 1 else ()
            )
            for i in range(3)
        ]
        yield (
            depo,
            kosu,
            dict(
                is_id="arama",
                hucreler=hucreler,
                bolgeler=[pilot_arama_bolgesi(ust, hucreler)],
                politika_surumu="genis_bolge_net_r_v1",
                birimler={"net_r": "R"},
                uyarilar=[],
                cikti_referanslari=[
                    d["sonuc_ref"] for h in hucreler for d in h["donemler"]
                ],
            ),
        )


@pytest.mark.parametrize(
    "yol",
    [
        ("hucreler",),
        ("bolgeler",),
        ("en_iyi",),
        ("sembol",),
        ("hucreler", 0, "komsular"),
        ("hucreler", 0, "alan_disi_komsular"),
        ("hucreler", 0, "eksik_komsular"),
        ("hucreler", 0, "karli"),
        ("hucreler", 0, "sinir"),
        ("hucreler", 0, "uygun_merkez"),
        ("hucreler", 0, "uzaklik"),
        ("hucreler", 0, "en_kotu_komsu"),
        ("hucreler", 0, "kapali_islem_sayisi"),
        ("hucreler", 0, "toplam_net_r"),
        ("bolgeler", 0, "indeksler"),
        ("bolgeler", 0, "buyukluk"),
        ("bolgeler", 0, "medyan_net_r"),
        ("bolgeler", 0, "uygun_merkezler"),
        ("bolgeler", 0, "kanonik_indeks"),
        ("en_iyi", "indeks"),
        ("en_iyi", "secildi"),
    ],
)
def test_s11_bolge_eksik_aciklamayla_yayinlanmaz(pilot_arama, yol):
    depo, kosu, girdi = pilot_arama
    ust = depo.deneme_oku(kosu.makbuz.deneme_id)
    bolge = pilot_arama_bolgesi(ust, girdi["hucreler"])
    alan = bolge
    for ad in yol[:-1]:
        alan = alan[ad]
    alan.pop(yol[-1])
    girdi["bolgeler"] = [bolge]
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, (
        "Verilen her bölge hücre, komşu, sınır ve eşitlik açıklamasını taşımalı"
    )
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize(
    "boz",
    [
        pytest.param(lambda b: b.update(hucreler=[]), id="absent-cell-identities"),
        pytest.param(
            lambda b: b.update(hucreler=b["hucreler"][:1] * 2), id="duplicate-cell"
        ),
        pytest.param(
            lambda b: b["hucreler"][0].update(deneme_id="baska-cocuk"),
            id="summary-child",
        ),
        pytest.param(
            lambda b: b["hucreler"][0].update(durum="hesap_hatasi"), id="summary-status"
        ),
        pytest.param(lambda b: b.update(politika="eski"), id="policy"),
        pytest.param(lambda b: b.update(strateji_id="baska-strateji"), id="strategy"),
        pytest.param(lambda b: b["donem"].update(ad="baska-donem"), id="period"),
        pytest.param(lambda b: b.update(bolgeler=None), id="component-list"),
        pytest.param(
            lambda b: b["hucreler"][0].update(komsular=None), id="neighbor-list"
        ),
        pytest.param(
            lambda b: b["hucreler"][0].update(komsular=[[99]]), id="neighbor-coordinate"
        ),
        pytest.param(
            lambda b: b["bolgeler"][0].update(indeksler=[[99]]),
            id="component-coordinate",
        ),
        pytest.param(
            lambda b: b.update(
                secilen=[0], secilen_deneme_id="baska-cocuk", neden=None
            ),
            id="selected-child",
        ),
    ],
)
def test_s11_bolge_sahte_aciklama_bagini_yazmaz(pilot_arama, boz):
    depo, kosu, girdi = pilot_arama
    ust = depo.deneme_oku(kosu.makbuz.deneme_id)
    bolge = pilot_arama_bolgesi(ust, girdi["hucreler"])
    boz(bolge)
    girdi["bolgeler"] = [bolge]
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Bölgenin açıklaması aynı hücre, dönem ve hisseye bağlı olmalı"
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize(
    "durum",
    ["islemsiz", "eksik", "hesap_hatasi", "kayit_hatasi", "baslamadi", "tanimlanmamis"],
)
def test_s11_bolge_basarili_donemde_basarisiz_hisseyi_secmez(
    pilot_arama_secilen, durum
):
    depo, kosu, girdi = pilot_arama_secilen
    h = girdi["hucreler"][1]
    bolge = girdi["bolgeler"][0]
    assert bolge["secilen"] == [1]
    assert h["donemler"][0]["durum"] == "tamamlandi"
    h["donemler"][0]["semboller"][0]["durum"] = durum
    bolge["hucreler"][1]["durum"] = durum
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Tamamlanmış dönemdeki başarısız veya işlemsiz hisse seçilemez"
    assert depo.yol.read_bytes() == once


def test_s11_bolge_ayni_donemde_baska_hisseyi_secmez(pilot_arama_secilen):
    depo, kosu, girdi = pilot_arama_secilen
    bolge = girdi["bolgeler"][0]
    assert bolge["secilen"] == [1]
    bolge["sembol"] = "BASKA"
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Seçilen sonuç aynı hissede tamamlanmış ölçü gerektirir"
    assert depo.yol.read_bytes() == once


def test_s11_bolge_baska_donem_basarisizken_tamamlanan_donemi_secer(
    pilot_arama_secilen,
):
    depo, kosu, girdi = pilot_arama_secilen
    h = girdi["hucreler"][1]
    bolge = girdi["bolgeler"][0]
    assert h["durum"] == "hesap_hatasi"
    assert h["donemler"][0]["durum"] == "tamamlandi"
    assert h["donemler"][1]["durum"] == "hesap_hatasi"
    assert bolge["secilen"] == [1]
    makbuz = kosu.arama_sonucu_kaydet(**girdi)
    sonuc = pilot.PilotKayit(depo.yol).izle(makbuz.olay_id)["sonuc"]
    assert sonuc["bolgeler"] == girdi["bolgeler"]
    assert sonuc["bolgeler"][0]["secilen_deneme_id"] == h["deneme_id"]
    kosu.bitir(
        durum="hata",
        tamamlanan=["arama", "hucre:0", "hucre:2"],
        basarisiz=["hucre:1"],
        yontemler=[],
        olculer={},
        cikti_referanslari=[makbuz.olay_id],
        ozetler={},
    )
    assert depo.izle(makbuz.olay_id)["durum"] == "hata"


def test_s11_bolge_nedenli_secimsiz_aciklamayi_korur(pilot_arama):
    depo, kosu, girdi = pilot_arama
    ust = depo.deneme_oku(kosu.makbuz.deneme_id)
    girdi["bolgeler"] = [pilot_arama_bolgesi(ust, girdi["hucreler"])]
    assert girdi["bolgeler"][0]["secilen"] is None
    assert girdi["bolgeler"][0]["neden"] == "uygun_merkez_yok"
    makbuz = kosu.arama_sonucu_kaydet(**girdi)
    assert (
        pilot.PilotKayit(depo.yol).izle(makbuz.olay_id)["sonuc"]["bolgeler"]
        == girdi["bolgeler"]
    )


def test_s11_baslamamis_bolge_hissesiz_ve_secimsiz_kalir(pilot_arama):
    depo, kosu, girdi = pilot_arama
    for h in girdi["hucreler"]:
        h.update(
            deneme_id=None,
            kosu_id=None,
            ayar_parmak_izi=None,
            kayit_makbuzu=None,
            baslangic_makbuzu=None,
            bitis_makbuzu=None,
            durum="kayit_hatasi",
            neden="kayıt reddedildi",
        )
        for d in h["donemler"]:
            d.update(
                durum="baslamadi",
                neden=h["neden"],
                sonuc_ref=None,
                islem_referanslari=[],
                semboller=[],
                beklenen_semboller=[],
            )
    ust = depo.deneme_oku(kosu.makbuz.deneme_id)
    girdi["bolgeler"] = [pilot_arama_bolgesi(ust, girdi["hucreler"], sembol=None)]
    girdi["cikti_referanslari"] = []
    makbuz = kosu.arama_sonucu_kaydet(**girdi)
    bolge = pilot.PilotKayit(depo.yol).izle(makbuz.olay_id)["sonuc"]["bolgeler"][0]
    assert bolge["sembol"] is None
    assert bolge["secilen"] is None
    assert bolge["secilen_deneme_id"] is None
    assert bolge["neden"] == "uygun_merkez_yok"
    assert [h["durum"] for h in bolge["hucreler"]] == ["baslamadi", "baslamadi"]


@pytest.mark.parametrize("secim_var", [False, True])
def test_s11_en_iyi_hucre_yanlis_secim_etiketi_tasiyamaz(
    pilot_arama_secilen, secim_var
):
    depo, kosu, girdi = pilot_arama_secilen
    bolge = girdi["bolgeler"][0]
    assert bolge["en_iyi"]["indeks"] == [0]
    assert bolge["secilen"] == [1]
    if not secim_var:
        bolge.update(secilen=None, secilen_deneme_id=None, neden="uygun_merkez_yok")
    bolge["en_iyi"]["secildi"] = True
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "En iyi hücre seçilmediği halde seçildi diye etiketlenemez"
    assert depo.yol.read_bytes() == once


def test_s11_iki_aciklamadaki_hisse_gercek_kaydin_yerini_alamaz(pilot_arama_secilen):
    depo, kosu, girdi = pilot_arama_secilen
    for h in girdi["hucreler"]:
        h["donemler"][0]["semboller"][0]["sembol"] = "BASKA"
    girdi["bolgeler"][0]["sembol"] = "BASKA"
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "İki açıklama uyuşsa da hisse gerçek dönem kaydında bulunmalı"
    assert depo.yol.read_bytes() == once


@pytest.fixture
def pilot_arama_hisseli(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "hisseli-arama.jsonl")
    kayit = pilot_arama_ust(depo)
    ust = depo.deneme_oku(kayit.deneme_id)
    with pilot_kosu(
        depo, kayit.deneme_id, is_listesi=["arama", "hucre:0", "hucre:1"]
    ) as kosu:
        hucreler = [
            pilot_arama_hucresi(
                depo, ust, i, hisseler=("TEST", "IKINCI", "BOS"), islemsiz=("BOS",)
            )
            for i in range(2)
        ]
        yield (
            depo,
            kosu,
            dict(
                is_id="arama",
                hucreler=hucreler,
                bolgeler=[],
                politika_surumu="genis_bolge_net_r_v1",
                birimler={"net_r": "R"},
                uyarilar=[],
                cikti_referanslari=[
                    d["sonuc_ref"] for h in hucreler for d in h["donemler"]
                ],
            ),
        )


@pytest.mark.parametrize("boz", ["eksik", "yinelenen", "eklenen"])
def test_s11_hisse_kumesi_gercek_islemsiz_hisseyi_korur(pilot_arama_hisseli, boz):
    depo, kosu, girdi = pilot_arama_hisseli
    semboller = girdi["hucreler"][0]["donemler"][0]["semboller"]
    if boz == "eksik":
        semboller.pop()
    else:
        ek = deepcopy(semboller[-1])
        if boz == "eklenen":
            ek["sembol"] = "YOK"
        semboller.append(ek)
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, (
        "İşlemsiz hisse de gerçek dönem hissesinde tekil ve eksiksiz kalmalı"
    )
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize("alan", ["islemler", "acik_kismi"])
@pytest.mark.parametrize("degistir", [False, True])
def test_s11_gercek_islem_basvurusu_kendi_hissesinde_kalir(
    pilot_arama_hisseli, alan, degistir
):
    depo, kosu, girdi = pilot_arama_hisseli
    d = girdi["hucreler"][0]["donemler"][0]
    ilk, ikinci, bos = d["semboller"]
    if alan == "acik_kismi":
        for s in (ilk, ikinci):
            s["olcu"]["acik_kismi"] = s["olcu"]["islemler"]
            s["olcu"]["islemler"] = []
    if degistir:
        for ad in (alan, "egri_tanimi"):
            ilk["olcu"][ad], ikinci["olcu"][ad] = (
                ikinci["olcu"][ad],
                ilk["olcu"][ad],
            )
    once = depo.yol.read_bytes()
    reddedildi = False
    makbuz = None
    try:
        makbuz = kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi == degistir, "Aynı dönem ve referans kümesi farklı hisseye yetmez"
    if degistir:
        assert depo.yol.read_bytes() == once
    else:
        sonuc = pilot.PilotKayit(depo.yol).izle(makbuz.olay_id)["sonuc"]
        kayitli = sonuc["hucreler"][0]["donemler"][0]["semboller"]
        assert [s["sembol"] for s in kayitli] == ["TEST", "IKINCI", "BOS"]
        assert kayitli[-1] == bos
        assert bos["durum"] == "islemsiz"
        assert bos["olcu"]["islemler"] == []
        gercek = depo.izle(d["sonuc_ref"])["sonuc"]["icerik"]
        assert gercek["durumlar"]["TEST"]["durum"] == "bekliyor"
        assert ilk["durum"] == "tamamlandi"


@pytest.mark.parametrize(
    "boz",
    [
        pytest.param(
            lambda b: b["hucreler"][1].update(karli=False), id="not-profitable"
        ),
        pytest.param(lambda b: b["hucreler"][1].update(karli=1), id="truthy-profit"),
        pytest.param(
            lambda b: b["hucreler"][1].update(uygun_merkez=False), id="ineligible"
        ),
        pytest.param(
            lambda b: b["hucreler"][1].update(uygun_merkez=1), id="truthy-eligible"
        ),
        pytest.param(lambda b: b["hucreler"][1].update(sinir=True), id="boundary"),
        pytest.param(lambda b: b["hucreler"][1].update(sinir=0), id="falsey-boundary"),
        pytest.param(
            lambda b: b["hucreler"][1].update(eksik_komsular=[[0]]),
            id="missing-neighbor",
        ),
        pytest.param(lambda b: b.update(bolgeler=[]), id="missing-component"),
        pytest.param(
            lambda b: b["bolgeler"][0].update(indeksler=[[0], [2]]), id="missing-member"
        ),
        pytest.param(
            lambda b: b["bolgeler"][0].update(uygun_merkezler=[]),
            id="missing-eligible-center",
        ),
        pytest.param(
            lambda b: b["bolgeler"].append(deepcopy(b["bolgeler"][0])),
            id="duplicate-member-component",
        ),
        pytest.param(
            lambda b: b["bolgeler"].append(
                dict(b["bolgeler"][0], indeksler=[[2]], kanonik_indeks=[2])
            ),
            id="other-eligible-component",
        ),
    ],
)
def test_s11_secilen_merkez_hucre_ve_bilesen_aciklamasiyla_tutarlidir(
    pilot_arama_secilen, boz
):
    depo, kosu, girdi = pilot_arama_secilen
    bolge = girdi["bolgeler"][0]
    assert bolge["secilen"] == [1]
    boz(bolge)
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, (
        "Seçilen merkez kendi hücresine ve tek uygun bileşenine bağlı olmalı"
    )
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize("secim_var", [False, True])
def test_s11_bilesen_uygun_merkezi_kendi_uyesinde_bildirir(
    pilot_arama_secilen, secim_var
):
    depo, kosu, girdi = pilot_arama_secilen
    bolge = girdi["bolgeler"][0]
    if not secim_var:
        bolge.update(secilen=None, secilen_deneme_id=None, neden="uygun_merkez_yok")
    bolge["bolgeler"].append(
        dict(
            bolge["bolgeler"][0],
            indeksler=[[0]],
            uygun_merkezler=[[2]],
            kanonik_indeks=[0],
        )
    )
    once = depo.yol.read_bytes()
    reddedildi = False
    try:
        kosu.arama_sonucu_kaydet(**girdi)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, "Her bileşen yalnız kendi üyesini uygun merkez diye gösterebilir"
    assert depo.yol.read_bytes() == once


def test_s12_kayit_bagi_nihai_sonucu_ve_acik_ufku_korur(tmp_path, monkeypatch):
    from copy import deepcopy
    from tests.test_tansusinama import s12_sinyalli, s12_calistir

    depo, m, _ = s12_sinyalli(tmp_path, monkeypatch, son_sinyal="2025-10-04")
    asil_islem = pilot._Kosu.ileri_islem_kaydet
    asil_sonuc = pilot._Kosu.ileri_sonucu_kaydet
    asil_secim = pilot._Kosu.ileri_secim_kaydet
    denetlenen = []

    def bozmalar(kayit):
        if kayit["tur"] == "bolum":
            if kayit["bolum_id"] != "2022Q1":
                return []
            alanlar = [
                (("secimler", 0, "test_deneme_id"), "kayitsiz-cocuk"),
                (("sayimlar", "TEST", "kapali_islem"), "yanlis-tur"),
                (("kontrol_refleri",), []),
                (("kontrol_refleri",), kayit["kontrol_refleri"] * 2),
                (("uyarilar",), []),
            ]
        else:
            alanlar = [
                (("olculer", "TEST", "olculer", "net_r", "deger"), 999999.0),
                (("olculer", "TEST", "olculer", "net_r", "birim"), "TL"),
                (("olculer", "TEST", "olculer", "sharpe", "bos_nedeni"), "uydurma"),
                (("olculer", "TEST", "egri_tanimi", "referanslar"), []),
                (("olculer", "TEST", "islemler", 0, "islem_ref"), "kayitsiz-islem"),
                (("olculer",), {}),
                (("kontrol_refleri",), []),
                (("giris_kohort_sayimlari", "2022Q2", "TEST", "kapali_islem"), 2),
                (("giris_kohort_sayimlari", "2025Q4", "TEST", "acik_islem"), 1.0),
            ]
        sonuc = []
        for yol, deger in alanlar:
            yanlis = deepcopy(kayit)
            hedef = yanlis
            for a in yol[:-1]:
                hedef = hedef[a]
            hedef[yol[-1]] = deger
            sonuc.append(yanlis)
        return sonuc

    def secim(kosu, *, kayit):
        if kayit["durum"] == "secildi":
            yanlis = deepcopy(kayit)
            yanlis["bolge"]["hucreler"][1]["uzaklik"] = 999
            once = depo.yol.read_bytes()
            with pytest.raises(pilot.PilotHatasi, match="seçim bölgesi"):
                asil_secim(kosu, kayit=yanlis)
            assert depo.yol.read_bytes() == once
        return asil_secim(kosu, kayit=kayit)

    def islem(kosu, *, islem, ufuk):
        yanlis = deepcopy(islem)
        yanlis["pozisyon"]["ayar"]["min_gun"] = 5
        with pytest.raises(pilot.PilotHatasi, match="özgün sinyal"):
            asil_islem(kosu, islem=yanlis, ufuk=ufuk)
        yanlis = deepcopy(islem)
        yanlis["sonuc"]["net_sonuc"] += 1.0
        with pytest.raises(pilot.PilotHatasi, match="gerçek E3"):
            asil_islem(kosu, islem=yanlis, ufuk=ufuk)
        r = asil_islem(kosu, islem=islem, ufuk=ufuk)
        with pytest.raises(pilot.PilotHatasi, match="zaten yayımlandı"):
            asil_islem(kosu, islem=islem, ufuk=ufuk)
        denetlenen.append(r.olay_id)
        return r

    def sonuc(kosu, *, kayit):
        for yanlis in bozmalar(kayit):
            once = depo.yol.read_bytes()
            with pytest.raises(pilot.PilotHatasi):
                asil_sonuc(kosu, kayit=yanlis)
            assert depo.yol.read_bytes() == once
        if kayit["tur"] == "bolum" and kayit["bolum_id"] == "2022Q1":
            yanlis = deepcopy(kayit)
            yanlis["islem_refleri"] = [
                dict(
                    yanlis["kontrol_refleri"][0],
                    rol="tamamlanmis_islem",
                    islem_id="yanlis",
                )
            ]
            with pytest.raises(pilot.PilotHatasi, match="Kayıt bağı"):
                asil_sonuc(kosu, kayit=yanlis)
        if kayit["tur"] == "birlesik":
            yanlis = deepcopy(kayit)
            yanlis["giris_kohortlari"] = {"2022Q1": yanlis["islem_refleri"]}
            with pytest.raises(pilot.PilotHatasi, match="kohort"):
                asil_sonuc(kosu, kayit=yanlis)
        return asil_sonuc(kosu, kayit=kayit)

    monkeypatch.setattr(pilot._Kosu, "ileri_islem_kaydet", islem)
    monkeypatch.setattr(pilot._Kosu, "ileri_sonucu_kaydet", sonuc)
    monkeypatch.setattr(pilot._Kosu, "ileri_secim_kaydet", secim)
    r = s12_calistir(depo, m, tmp_path)
    assert r["durum"] == "tamamlandi", [
        (b["bolum_id"], b["neden"]) for b in r["bolumler"]
    ]
    assert len(denetlenen) == 2
    islemler = [o for o in depo.oku() if o.get("islem_turu") == "ileri_islem_v1"]
    assert [o["rol"] for o in islemler] == ["tamamlanmis_islem", "acik_ufuk"]
    acik = islemler[-1]["olaylar"][0]
    assert acik["pozisyon"]["cikis_tarih"] is None
    assert acik["sonuc"]["net_r"] is None
    assert acik["sonuc"]["kalan_adet"] > 0
    assert acik["degerleme"]["tarih"] == "2025-10-05"

    asil_olaylar = depo.oku()
    birlesik = next(
        o["kayit"]
        for o in asil_olaylar
        if o.get("sonuc_turu") == "ileri_v1" and o["kayit"]["tur"] == "birlesik"
    )
    assert birlesik["giris_kohort_sayimlari"]["2025Q4"]["TEST"] == dict(
        kapali_islem=0, ayri_giris_gunu=1, acik_islem=1
    )
    for hedef in asil_olaylar:
        if hedef.get("sonuc_turu") != "ileri_v1":
            continue
        for no, yanlis in enumerate(bozmalar(hedef["kayit"])):
            onceki = asil_olaylar[: asil_olaylar.index(hedef)]
            yol = tmp_path / f"{hedef['bolum_id']}-{no}-icerik.jsonl"
            yol.write_bytes(
                b"".join(pilot.kanonik(o) + b"\n" for o in onceki)
                + pilot.kanonik(hedef | dict(kayit=yanlis))
                + b"\n"
            )
            with pytest.raises(pilot.PilotHatasi):
                pilot.PilotKayit(yol).oku()
    kabul_edilen = []
    for tur in (
        "ileri_secim",
        "ileri_sinyal",
        "ileri_kontrol",
        "islem",
        "bolum",
        "birlesik",
        "bitis",
        "surum",
        "yetim",
        "ileri_ref",
        "sahip",
        "rol",
        "baslangic",
        "yinelenen_olay",
        "bilinmeyen_tur",
        "kontrol_float",
        "sinyal_legacy",
        "sinyal_pay_kimligi",
        "kontrol_legacy",
        "islem_legacy",
        "bolum_legacy",
    ):
        olaylar = deepcopy(asil_olaylar)
        aranan = (
            "ileri_sinyal"
            if tur
            in (
                "surum",
                "yetim",
                "ileri_ref",
                "sahip",
                "yinelenen_olay",
                "bilinmeyen_tur",
            )
            else "islem"
            if tur == "rol"
            else "ileri_kontrol"
            if tur == "kontrol_float"
            else tur
        )
        aranan = {
            "sinyal_legacy": "ileri_sinyal",
            "sinyal_pay_kimligi": "ileri_sinyal",
            "kontrol_legacy": "ileri_kontrol",
            "islem_legacy": "islem",
            "bolum_legacy": "bolum",
        }.get(tur, aranan)
        hedef = next(
            o
            for o in olaylar
            if (
                o["kayit_turu"] == aranan
                and (aranan != "ileri_secim" or o["kayit"]["durum"] == "secildi")
                and (aranan != "islem" or o.get("islem_turu") == "ileri_islem_v1")
            )
            or (
                aranan in ("bolum", "birlesik")
                and o.get("sonuc_turu") == "ileri_v1"
                and o["kayit"]["tur"] == aranan
            )
        )
        if tur.endswith("_legacy"):
            legacy = next(
                x
                for x in olaylar
                if x["kayit_turu"] == "deneme"
                and x["yontem_ayarlari"]["yontem"] == "kayitli_donem_v1"
            )
            hedef["deneme_id"] = legacy["deneme_id"]
            hedef["ayar_parmak_izi"] = legacy["ayar_parmak_izi"]
        elif tur == "ileri_secim":
            hedef["kayit"]["deneme_ayar_parmak_izi"] = "uydurma"
        elif tur == "ileri_sinyal":
            hedef["deneme_ayar_parmak_izi"] = "uydurma"
        elif tur == "sinyal_pay_kimligi":
            hedef["sinyal"]["veri_ref"]["pay_kimligi"] = dict(
                surum="pay_kimligi_v1",
                tablo_ozeti="a" * 64,
                kaynak="is_yatirim",
                goruntu_id="s10",
                manifest_ozeti=hedef["sinyal"]["veri_ref"]["manifest_parmak_izi"],
            )
        elif tur == "ileri_kontrol":
            hedef["onceki_ref"] = "baska-kontrol"
        elif tur == "islem":
            hedef["olaylar"][0]["sonuc"]["net_r"] += 1.0
        elif tur == "bolum":
            hedef["kayit"]["bolum_id"] = "2022Q4"
        elif tur == "birlesik":
            hedef["kayit"]["giris_kohortlari"] = {
                "2022Q1": hedef["kayit"]["islem_refleri"]
            }
        elif tur == "bitis":
            hedef = next(
                o
                for o in olaylar
                if o["kayit_turu"] == "bitis" and o["kosu_id"] == r["kosu_id"]
            )
            hedef["cikti_referanslari"] = [
                next(
                    o["kayit_id"]
                    for o in olaylar
                    if o.get("sonuc_turu") == "ileri_v1"
                    and o["kayit"]["tur"] == "bolum"
                )
            ]
        elif tur == "surum":
            hedef["surum"] = "ileri_sinyal_v999"
        elif tur == "yetim":
            hedef["secim_ref"] = "kayitsiz-secim"
        elif tur == "ileri_ref":
            olaylar.remove(hedef)
            secim = next(
                i for i, o in enumerate(olaylar) if o["kayit_id"] == hedef["secim_ref"]
            )
            olaylar.insert(secim, hedef)
        elif tur == "sahip":
            hedef["kosu_id"] = "baska-kosu"
        elif tur == "baslangic":
            hedef = next(
                o
                for o in olaylar
                if o["kayit_turu"] == "baslangic" and o["kosu_id"] == r["kosu_id"]
            )
            hedef["ayar_parmak_izi"] = "baska-ust"
        elif tur == "yinelenen_olay":
            olaylar.insert(olaylar.index(hedef) + 1, deepcopy(hedef))
        elif tur == "bilinmeyen_tur":
            hedef["kayit_turu"] = "bilinmeyen"
            hedef.pop("surum")
        elif tur == "kontrol_float":
            hedef["bolum_id"] = 2022.0
        else:
            hedef["rol"] = "bilinmeyen-rol"
        yol = tmp_path / (tur + "-bozuk.jsonl")
        yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            continue
        kabul_edilen.append(tur)
    assert kabul_edilen == [], (
        "Yeni okuyucu kanonik fakat geçersiz WF kaydını reddetmelidir"
    )


def test_s12_birlesik_olay_kaynagi_uydurulamaz(tmp_path, monkeypatch):
    from copy import deepcopy
    from tests.test_tansusinama import s12_kayitli, s12_calistir

    depo, m, piyasa = s12_kayitli(tmp_path, monkeypatch)
    piyasa[:] = [r for r in piyasa if r["tarih"] != "2022-01-04"]
    asil = pilot._Kosu.ileri_sonucu_kaydet
    denetlenen = []

    def sonuc(kosu, *, kayit):
        if kayit["tur"] == "birlesik":
            yanlis = deepcopy(kayit)
            yanlis["olaylar"] = [
                dict(
                    olay_id="uydurma",
                    tarih="2022-01-04",
                    sembol="TEST",
                    tur="dolum",
                    icerik={},
                )
            ]
            with pytest.raises(pilot.PilotHatasi, match="gerçek E3"):
                asil(kosu, kayit=yanlis)
            denetlenen.append(True)
        return asil(kosu, kayit=kayit)

    monkeypatch.setattr(pilot._Kosu, "ileri_sonucu_kaydet", sonuc)
    r = s12_calistir(depo, m, tmp_path)
    assert r["durum"] == "hata"
    assert denetlenen == [True]
    bolumler = [
        o["kayit"]
        for o in depo.oku()
        if o.get("sonuc_turu") == "ileri_v1" and o["kayit"]["tur"] == "bolum"
    ]
    assert len(bolumler) == 1, "Başlayan bölümün ret gerekçesi kalıcı olmalıdır"
    assert bolumler[0]["durum"] == "hata"
    assert bolumler[0]["neden"] == r["bolumler"][0]["neden"]
    assert "seans kapsamı" in bolumler[0]["hatalar"][0]["neden"]


def grup_kayit_tanimi():
    # Yalnız E5 şema örneği; gerçek veya hesaplanabilir kaynak strateji değildir.
    ref = dict(yol="statik-kaynak", sha256="a" * 64)
    return dict(
        grup_id="grup",
        revizyon="1",
        soru="Açık alanlar tamam mı?",
        strateji_revizyonlari=[
            dict(
                revizyon_ref="kaynak-1",
                kaynak=ref,
                yayim_tarihi="2025-12-19",
                deneme_id="dogrulanmis-basvuru",
                eksik_alanlar=[],
            )
        ],
        seanslar=["2025-01-02"],
        isinma_baslangici="2024-12-31",
        hisse_kurali=dict(
            semboller=["AKBNK"],
            evren_politikasi="donemsel_bist30_v1",
            uyelik_surumu="bist30_2021_2025_v1",
        ),
        referanslar=dict(
            anlik_goruntu="ag",
            manifest_ozeti="m",
            uyelik_ozeti="u",
            kod_ozeti="k",
            takvim=ref,
            yontem=ref,
            risk=ref,
            masraf=ref,
        ),
        gozlem_durumu="kesif",
        durdurma_kurali="Teknik hata durdurur.",
    )


def test_grup_hazirligi_ayri_olaydir_hazir_da_olsa_yurutmez(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "hazirlik.jsonl")
    tanim = grup_kayit_tanimi()
    engel = dict(alan="seanslar", neden="Kesin seçim eksik.")
    kayitlar = []
    with pytest.raises(pilot.PilotHatasi, match="zorunlu alan"):
        depo.grup_hazirligi_kaydet(
            tanim=dict(grup_id="grup", revizyon="taslak"), engeller=[], dislamalar=[]
        )
    for engeller, durum in (([engel], "engelli"), ([], "hazir")):
        m = depo.grup_hazirligi_kaydet(tanim=tanim, engeller=engeller, dislamalar=[])
        kayitlar.append(m.olay_id)
        olay = pilot.PilotKayit(depo.yol).grup_hazirligi_oku(m.olay_id, tanim=tanim)
        assert olay["hazirlik_durumu"] == durum
        assert olay["yurutme_izni"] is False
        assert olay["tanim"] == tanim
        assert m.deneme_id is None and m.kosu_id is None
        assert set(olay) == {
            "kayit_id",
            "sema_surumu",
            "olusturma_zamani",
            "kayit_turu",
            "hazirlik_turu",
            "tanim",
            "tanim_ozeti",
            "engeller",
            "dislamalar",
            "hazirlik_durumu",
            "yurutme_izni",
        }
    assert [o["kayit_turu"] for o in depo.oku()] == ["grup_hazirligi"] * 2
    with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
        depo.grup_hazirligi_oku(kayitlar[0], tanim=tanim)
    assert depo.grup_hazirligi_oku(kayitlar[0])["hazirlik_durumu"] == "engelli"


@pytest.mark.parametrize(
    "alan", ["strateji", "anlik_goruntu", "uyelik_ozeti", "kod_ozeti", "yontem"]
)
def test_grup_degisen_basvuru_yeni_revizyon_ister_tarihce_korunur(tmp_path, alan):
    depo = pilot.PilotKayit(tmp_path / "hazirlik.jsonl")
    tanim = grup_kayit_tanimi()
    m = depo.grup_hazirligi_kaydet(
        tanim=tanim, engeller=[dict(alan="kaynak", neden="Test engeli.")], dislamalar=[]
    )
    eski = depo.yol.read_bytes()
    yeni = deepcopy(tanim)
    if alan == "strateji":
        yeni["strateji_revizyonlari"] = [dict(revizyon_ref="yeni-kaynak")]
    else:
        yeni["referanslar"] = {
            alan: {"yol": "yeni", "sha256": "a" * 64} if alan == "yontem" else "yeni"
        }
    with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
        depo.grup_hazirligi_oku(m.olay_id, tanim=yeni)
    with pytest.raises(pilot.PilotHatasi, match="yeni revizyon"):
        depo.grup_hazirligi_kaydet(
            tanim=yeni,
            engeller=[dict(alan="kaynak", neden="Test engeli.")],
            dislamalar=[],
        )
    assert depo.yol.read_bytes() == eski
    yeni["revizyon"] = "2"
    n = depo.grup_hazirligi_kaydet(
        tanim=yeni, engeller=[dict(alan="kaynak", neden="Test engeli.")], dislamalar=[]
    )
    assert depo.yol.read_bytes().startswith(eski)
    assert depo.grup_hazirligi_oku(m.olay_id)["tanim"] == tanim
    with pytest.raises(pilot.PilotHatasi, match="geçersiz"):
        depo.grup_hazirligi_oku(m.olay_id, tanim=tanim)
    assert depo.grup_hazirligi_oku(n.olay_id, tanim=yeni)["tanim"] == yeni


@pytest.mark.parametrize("alan,adet", [("strateji_revizyonlari", 4), ("seanslar", 61)])
def test_grup_revizyon_ve_seans_sinirini_asamaz(tmp_path, alan, adet):
    depo = pilot.PilotKayit(tmp_path / "hazirlik.jsonl")
    tanim = dict(
        grup_id="grup",
        revizyon="1",
        strateji_revizyonlari=[dict(revizyon_ref=str(i)) for i in range(3)],
        seanslar=pd.bdate_range("2025-01-02", periods=60).strftime("%Y-%m-%d").tolist(),
    )
    m = depo.grup_hazirligi_kaydet(
        tanim=tanim, engeller=[dict(alan="kaynak", neden="Test engeli.")], dislamalar=[]
    )
    assert len(depo.grup_hazirligi_oku(m.olay_id)["tanim"][alan]) == adet - 1
    tanim["revizyon"] = "2"
    if alan == "seanslar":
        tanim[alan].append("2025-12-31")
    else:
        tanim[alan].append(dict(revizyon_ref="fazla"))
    with pytest.raises(pilot.PilotHatasi, match="en fazla"):
        depo.grup_hazirligi_kaydet(
            tanim=tanim,
            engeller=[dict(alan="kaynak", neden="Test engeli.")],
            dislamalar=[],
        )
    assert len(depo.oku()) == 1


def test_grup_hazirligi_hesap_sonucu_ve_gecersiz_tarih_almaz(tmp_path):
    depo = pilot.PilotKayit(tmp_path / "hazirlik.jsonl")
    for degisiklik in (dict(performans=1), dict(seanslar=["2025-02-30"])):
        with pytest.raises(pilot.PilotHatasi):
            depo.grup_hazirligi_kaydet(
                tanim=dict(grup_id="grup", revizyon="1") | degisiklik,
                engeller=[dict(alan="kaynak", neden="Test engeli.")],
                dislamalar=[],
            )
    assert not depo.yol.exists()


@pytest.mark.parametrize(
    "degisiklik",
    [
        {"yurutme_izni": True},
        {"yurutme_izni": 0},
        {"hazirlik_durumu": "hazir"},
        {"performans": {"net_getiri": 1}},
        {"hazirlik_turu": "bilinmeyen_v1"},
        {"engeller": [{"alan": "seanslar", "neden": 0}]},
        {"engeller": [{"alan": "seanslar", "neden": "Eksik.", "fazla": 1}]},
        {
            "dislamalar": [
                {"sembol": "AKBNK", "tarih": "gecersiz", "neden": "uye_degil"}
            ]
        },
        {"engeller": [], "hazirlik_durumu": "hazir"},
        {"olusturma_zamani": 0},
    ],
    ids=[
        "yurutme-izni",
        "sifir-false-degildir",
        "engelli-hazir-olamaz",
        "hesap-sonucu",
        "hazirlik-turu",
        "engel-nedeni",
        "engel-fazla-alani",
        "dislama-tarihi",
        "eksik-hazir-tanimi",
        "olay-zamani",
    ],
)
def test_grup_okuyucusu_kanonik_ama_gecersiz_olayi_reddeder(tmp_path, degisiklik):
    depo = pilot.PilotKayit(tmp_path / "hazirlik.jsonl")
    m = depo.grup_hazirligi_kaydet(
        tanim=dict(grup_id="grup", revizyon="1"),
        engeller=[dict(alan="seanslar", neden="Kesin seçim eksik.")],
        dislamalar=[],
    )
    olay = depo.grup_hazirligi_oku(m.olay_id)
    olay.update(degisiklik)
    depo.yol.write_bytes(pilot.kanonik(olay) + b"\n")
    reddedildi = False
    try:
        pilot.PilotKayit(depo.yol).grup_hazirligi_oku(m.olay_id)
    except pilot.PilotHatasi:
        reddedildi = True
    assert reddedildi, (
        "Kanonik kodlama geçersiz hazırlık olayını kabul edilebilir yapmaz."
    )


@pytest.mark.parametrize(
    "boz", ["surum", "bos", "eksik", "fazla", "ozet", "goruntu", "manifest", "null"]
)
def test_grup_pay_kimligi_yanlis_ve_bagsiz_secimi_reddeder(tmp_path, boz):
    tanim = grup_kayit_tanimi()
    ref = tanim["referanslar"]
    ref["manifest_ozeti"] = "a" * 64
    secim = dict(
        surum="pay_kimligi_v1",
        tablo_ozeti="b" * 64,
        kaynak="is_yatirim",
        goruntu_id="ag",
        manifest_ozeti="a" * 64,
    )
    if boz == "surum":
        secim["surum"] = "bilinmeyen"
    elif boz == "bos":
        secim["kaynak"] = ""
    elif boz == "eksik":
        del secim["tablo_ozeti"]
    elif boz == "fazla":
        secim["otomatik"] = True
    elif boz == "ozet":
        secim["tablo_ozeti"] = "b" * 63
    elif boz == "goruntu":
        secim["goruntu_id"] = "diger"
    elif boz == "manifest":
        secim["manifest_ozeti"] = "c" * 64
    else:
        secim = None
    ref["pay_kimligi"] = secim
    depo = pilot.PilotKayit(tmp_path / "hazirlik.jsonl")
    with pytest.raises(pilot.PilotHatasi, match="[Pp]ay kimliği"):
        depo.grup_hazirligi_kaydet(tanim=tanim, engeller=[], dislamalar=[])
    assert not depo.yol.exists()


def test_grup_pay_kimligi_gecmisi_guncel_tabloyu_okumaz(tmp_path, monkeypatch):
    from hashlib import sha256
    from tansu import veri

    tanim = grup_kayit_tanimi()
    tanim["referanslar"]["manifest_ozeti"] = "a" * 64
    tanim["referanslar"]["pay_kimligi"] = dict(
        surum="pay_kimligi_v1",
        tablo_ozeti="b" * 64,
        kaynak="is_yatirim",
        goruntu_id="ag",
        manifest_ozeti="a" * 64,
    )
    depo = pilot.PilotKayit(tmp_path / "hazirlik.jsonl")
    m = depo.grup_hazirligi_kaydet(tanim=tanim, engeller=[], dislamalar=[])

    def yasak(*a, **k):
        pytest.fail("E5 geçmiş okuması piyasa veya güncel eşleme yükleyemez")

    monkeypatch.setattr(veri, "pay_kimligi_hazirla", yasak)
    monkeypatch.setattr(veri, "oku", yasak)
    assert pilot.PilotKayit(depo.yol).grup_hazirligi_oku(m.olay_id)["tanim"] == tanim
    olay = depo.oku()[0]
    olay["tanim"]["referanslar"]["pay_kimligi"]["surum"] = "bilinmeyen"
    olay["tanim_ozeti"] = sha256(pilot.kanonik(olay["tanim"])).hexdigest()
    depo.yol.write_bytes(pilot.kanonik(olay) + b"\n")
    with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır"):
        pilot.PilotKayit(depo.yol).oku()


def _s12_acik_kosu(tmp_path, monkeypatch):
    from tansu import tansusinama as ts
    from tests.test_tansusinama import s12_kayitli

    depo, deneme, _ = s12_kayitli(tmp_path, monkeypatch)

    def kes(_):
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        ts.kayitli_ileri_calistir(
            depo,
            deneme.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            ilerleme=kes,
        )
    baslangiclar = [
        o
        for o in depo.oku()
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] == deneme.deneme_id
    ]
    assert len(baslangiclar) == 1
    return depo, deneme, baslangiclar[0]


def _s12_devam_kimligi(b):
    return dict(
        mod=b["mod"],
        kod_kimligi=b["kod_kimligi"],
        ortam=b["ortam"],
        bagimlilik_ozeti=b["bagimlilik_ozeti"],
    )


@pytest.mark.parametrize("kuyruk", [b"kesik-icerik", b"bozuk-tam-satir\n"])
def test_s12_devam_yalniz_son_lfsiz_kuyrugu_ayirir(tmp_path, monkeypatch, kuyruk):
    depo, _, bas = _s12_acik_kosu(tmp_path, monkeypatch)
    once = depo.yol.read_bytes()
    with depo.yol.open("ab") as dosya:
        dosya.write(kuyruk)
    if kuyruk.endswith(b"\n"):
        with pytest.raises(pilot.PilotHatasi):
            with depo.ileri_devam(bas["kosu_id"], **_s12_devam_kimligi(bas)):
                pass
        assert depo.yol.read_bytes() == once + kuyruk
    else:
        with depo.ileri_devam(bas["kosu_id"], **_s12_devam_kimligi(bas)) as kosu:
            assert any("Eksik satır" in u for u in kosu.makbuz.uyarilar)
        assert depo.yol.read_bytes() == once + kuyruk + pilot._KESIK
        assert depo.oku()[-1] == bas


def test_s12_kesik_kuyruk_uyarisi_hesaptan_once_gorunur(tmp_path, monkeypatch):
    from tansu import tansusinama as ts

    depo, deneme, bas = _s12_acik_kosu(tmp_path, monkeypatch)
    with depo.yol.open("ab") as dosya:
        dosya.write(b"yarim-satir")
    once = depo.yol.read_bytes()
    mesajlar = []

    def ilerleme(mesaj):
        mesajlar.append(mesaj)
        if "Eksik satır" in mesaj:
            raise KeyboardInterrupt

    def hesaplama_yasak(*_args, **_kwargs):
        pytest.fail("WF uyarıdan önce hesaplamaya geçti")

    monkeypatch.setattr(veri, "oku", lambda *_: None)
    monkeypatch.setattr(ts, "_ileri_secimler", hesaplama_yasak)
    with pytest.raises(KeyboardInterrupt):
        ts.kayitli_ileri_calistir(
            depo,
            deneme.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            devam_kosu_id=bas["kosu_id"],
            ilerleme=ilerleme,
        )
    assert any("Eksik satır" in mesaj for mesaj in mesajlar)
    assert depo.yol.read_bytes() == once + pilot._KESIK


def test_s12_devam_bilinmeyen_isaret_ve_aktarim_hatasi(tmp_path, monkeypatch):
    depo, deneme, bas = _s12_acik_kosu(tmp_path, monkeypatch)
    once = depo.yol.read_bytes()
    with pytest.raises(pilot.PilotHatasi, match="Bilinmeyen WF devam sürümü"):
        with depo.kosu(
            deneme.deneme_id,
            mod=bas["mod"],
            anlik_goruntu=bas["anlik_goruntu"],
            manifest_ozeti=bas["manifest_ozeti"],
            uyelik_surumu=bas["uyelik_surumu"],
            kod_kimligi=bas["kod_kimligi"],
            ortam=bas["ortam"] | {"ileri_devam_surumu": None},
            bagimlilik_ozeti=bas["bagimlilik_ozeti"],
            tohum=None,
            is_listesi=bas["is_listesi"],
        ):
            pass
    assert depo.yol.read_bytes() == once
    olaylar = deepcopy(depo.oku())
    olaylar[-1]["ortam"]["ileri_devam_surumu"] = None
    bozuk = tmp_path / "isaret-yok.jsonl"
    bozuk.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
    with pytest.raises(pilot.PilotHatasi):
        pilot.PilotKayit(bozuk).oku()

    def aktarim_hatasi(_):
        raise OSError("disk aktarımı")

    with depo.ileri_devam(bas["kosu_id"], **_s12_devam_kimligi(bas)) as kosu:
        monkeypatch.setattr(pilot.os, "fsync", aktarim_hatasi)
        with pytest.raises(pilot.PilotDayaniklilikHatasi) as hata:
            kosu.ileri_dayaniklastir(kosu.makbuz)
    assert hata.value.kayit_id == bas["kayit_id"]
    assert depo.yol.read_bytes() == once
    assert not any(o["kayit_turu"] == "bitis" for o in depo.oku())


def test_s12_devam_ikinci_surec_kilidi_ve_os_salimi(tmp_path, monkeypatch):
    depo, _, bas = _s12_acik_kosu(tmp_path, monkeypatch)
    kod = (
        "import sys,time; from tansu.deneme import PilotKayit; "
        "d=PilotKayit(sys.argv[1]); k=sys.argv[2]; "
        "b=next(o for o in d.oku() if o.get('kosu_id')==k and o['kayit_turu']=='baslangic'); "
        "with d.ileri_devam(k, mod=b['mod'], kod_kimligi=b['kod_kimligi'], "
        "ortam=b['ortam'], bagimlilik_ozeti=b['bagimlilik_ozeti']): "
        "print('KILITLI',flush=True); time.sleep(30)"
    )
    # Bileşik with ifadesi ayrı satır ister; süreç kodu tek argüman olarak kalır.
    kod = kod.replace("; with d.ileri_devam", "\nwith d.ileri_devam")
    surec = subprocess.Popen(
        [sys.executable, "-B", "-X", "utf8", "-c", kod, str(depo.yol), bas["kosu_id"]],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=Path(__file__).resolve().parents[1],
    )
    try:
        assert surec.stdout.readline().strip() == "KILITLI", surec.stderr.read()
        with pytest.raises(pilot.PilotHatasi, match="başka işçide"):
            with depo.ileri_devam(bas["kosu_id"], **_s12_devam_kimligi(bas)):
                pass
    finally:
        surec.terminate()
        surec.wait(timeout=10)
    with depo.ileri_devam(bas["kosu_id"], **_s12_devam_kimligi(bas)):
        pass


def test_s12_devam_farkli_temp_ile_ayni_gunlugu_iki_isci_acamaz(tmp_path, monkeypatch):
    depo, _, bas = _s12_acik_kosu(tmp_path, monkeypatch)
    kod = """
import sys, tempfile, time
from tansu.deneme import PilotHatasi, PilotKayit
d = PilotKayit(sys.argv[1])
k = sys.argv[2]
b = next(o for o in d.oku() if o.get('kosu_id') == k and o['kayit_turu'] == 'baslangic')
print('TEMP:' + tempfile.gettempdir(), flush=True)
try:
    with d.ileri_devam(k, mod=b['mod'], kod_kimligi=b['kod_kimligi'],
                       ortam=b['ortam'], bagimlilik_ozeti=b['bagimlilik_ozeti']):
        print('KILITLI' if sys.argv[3] == 'tut' else 'ACILDI', flush=True)
        if sys.argv[3] == 'tut':
            time.sleep(30)
except PilotHatasi as hata:
    print('RED:' + str(hata), flush=True)
    sys.exit(2)
"""
    birinci_temp = tmp_path / "ilk-temp"
    ikinci_temp = tmp_path / "ikinci-temp"
    birinci_temp.mkdir()
    ikinci_temp.mkdir()
    birinci_env = os.environ.copy() | dict(
        TEMP=str(birinci_temp), TMP=str(birinci_temp)
    )
    ikinci_env = os.environ.copy() | dict(TEMP=str(ikinci_temp), TMP=str(ikinci_temp))
    komut = [
        sys.executable,
        "-B",
        "-X",
        "utf8",
        "-c",
        kod,
        str(depo.yol),
        bas["kosu_id"],
    ]
    tutan = subprocess.Popen(
        [*komut, "tut"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=birinci_env,
        cwd=Path(__file__).resolve().parents[1],
    )
    try:
        assert Path(
            tutan.stdout.readline().strip().removeprefix("TEMP:")
        ).resolve() == (birinci_temp.resolve())
        assert tutan.stdout.readline().strip() == "KILITLI", tutan.stderr.read()
        ikinci = subprocess.run(
            [*komut, "dene"],
            capture_output=True,
            text=True,
            timeout=15,
            env=ikinci_env,
            cwd=Path(__file__).resolve().parents[1],
        )
        assert Path(ikinci.stdout.splitlines()[0].removeprefix("TEMP:")).resolve() == (
            ikinci_temp.resolve()
        )
        assert ikinci.returncode == 2, (ikinci.stdout, ikinci.stderr)
        assert "RED:WF denemesi başka işçide yürütülüyor." in ikinci.stdout
    finally:
        tutan.terminate()
        tutan.wait(timeout=10)
    serbest = subprocess.run(
        [*komut, "dene"],
        capture_output=True,
        text=True,
        timeout=15,
        env=ikinci_env,
        cwd=Path(__file__).resolve().parents[1],
    )
    assert serbest.returncode == 0, (serbest.stdout, serbest.stderr)
    assert serbest.stdout.splitlines()[-1] == "ACILDI"


def test_s12_egitim_sonucu_tam_e1_kimligini_yazar_ve_yeniden_okur(
    tmp_path, monkeypatch
):
    from tansu import tansusinama as ts
    from tests.test_tansusinama import s12_kayitli

    depo, eski, _ = s12_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(eski.deneme_id)
    secim = dict(
        surum="pay_kimligi_v1",
        tablo_ozeti=veri._YAYIMLANMIS_KAYNAK_OZETLERI["pay_kimligi_v1"],
        kaynak=d["veri_ayarlari"]["kaynak"],
        goruntu_id="s10",
        manifest_ozeti=d["veri_ayarlari"]["manifest_ozeti"],
    )
    v = deepcopy(d["veri_ayarlari"]) | dict(pay_kimligi=secim)
    m = pilot_deneme(
        depo,
        d["strateji"],
        donemler=d["donemler"],
        veri_ayarlari=v,
        yontem_ayarlari=d["yontem_ayarlari"],
        risk_ayarlari=d["risk_ayarlari"],
        masraf_ayarlari=d["masraf_ayarlari"],
    )
    e1, ekle, uyelik = veri.veri_hazirla, depo._ekle, veri.uyelik_hazirla
    ek = hashlib.sha256(
        json.dumps(secim, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    def pay_uyeligi(uyelik, _politika):
        return uyelik | dict(pay_kimligi=secim)

    def paket(*args):
        p = e1(*args)
        p["referans"].update(
            pay_kimligi=secim, kayit_id=p["referans"]["kayit_id"] + "/" + ek
        )
        p["uyelik"]["pay_kimligi"] = secim
        return p

    def ilk_sonucta_dur(olay, *args):
        makbuz = ekle(olay, *args)
        if olay["kayit_turu"] == "sonuc" and olay.get("sonuc_turu") == "donem_v1":
            raise KeyboardInterrupt
        return makbuz

    monkeypatch.setattr(veri, "uyelik_hazirla", lambda istek, **_kw: uyelik(istek))
    monkeypatch.setattr(veri, "pay_kimligi_hazirla", lambda *_a, **_k: {})
    monkeypatch.setattr(veri, "pay_uyeligi", pay_uyeligi)
    monkeypatch.setattr(veri, "veri_hazirla", paket)
    monkeypatch.setattr(depo, "_ekle", ilk_sonucta_dur)
    with pytest.raises(KeyboardInterrupt):
        ts.kayitli_ileri_calistir(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=None
        )
    olaylar = pilot.PilotKayit(depo.yol).oku()
    sonuc = next(o for o in olaylar if o.get("sonuc_turu") == "donem_v1")
    durum = sonuc["icerik"]["durumlar"]["TEST"]
    assert (
        durum["iz"]
        and durum["yurutme"]["veri_ref_id"]
        == (sonuc["icerik"]["veri_referansi"]["kayit_id"])
    )
    assert durum["yurutme"]["veri_ref_id"].endswith("/" + ek)

    yanlis = deepcopy(olaylar)
    sonuc = next(o for o in yanlis if o.get("sonuc_turu") == "donem_v1")
    ref = sonuc["icerik"]["veri_referansi"]
    ref["kayit_id"] += "/yanlis"
    durum = sonuc["icerik"]["durumlar"]["TEST"]
    durum["yurutme"]["veri_ref_id"] = ref["kayit_id"]
    durum.pop("butunluk")
    durum["butunluk"] = motor._iz_kodu(durum)
    icerik = sonuc["icerik"]
    icerik.pop("cikti_parmak_izi")
    icerik["cikti_parmak_izi"] = hashlib.sha256(pilot.kanonik(icerik)).hexdigest()
    onek = b"".join(pilot.kanonik(o) + b"\n" for o in yanlis[: yanlis.index(sonuc)])
    ekle_yolu = tmp_path / "yanlis-e1-ekle.jsonl"
    ekle_yolu.write_bytes(onek)
    eklenen = {
        k: v
        for k, v in sonuc.items()
        if k not in ("kayit_id", "sema_surumu", "olusturma_zamani")
    }
    with pytest.raises(pilot.PilotHatasi, match="WF çocuk E1 kimliği"):
        pilot.PilotKayit(ekle_yolu)._ekle(eklenen)
    assert ekle_yolu.read_bytes() == onek
    yol = tmp_path / "yanlis-e1.jsonl"
    yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in yanlis))
    with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır") as hata:
        pilot.PilotKayit(yol).oku()
    assert "WF çocuk E1 kimliği" in str(hata.value.__cause__)


def test_s12_egitim_sonucsuz_hatasi_ozgun_kalir(tmp_path, monkeypatch):
    from tansu import tansusinama as ts
    from tests.test_tansusinama import s12_kayitli

    depo, m, _ = s12_kayitli(tmp_path, monkeypatch)
    asil = ValueError("özgün eğitim hatası")

    def boz(*_args):
        raise asil

    monkeypatch.setattr(ts, "_donem_yaz", boz)
    with pytest.raises(ValueError, match="özgün eğitim hatası") as hata:
        ts.kayitli_ileri_calistir(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=None
        )
    assert hata.value is asil
    olaylar = depo.oku()
    cocuklar = {
        o["kosu_id"]
        for o in olaylar
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] != m.deneme_id
    }
    assert len(cocuklar) == 1
    assert not any(
        o["kayit_turu"] in ("sonuc", "bitis") and o.get("kosu_id") in cocuklar
        for o in olaylar
    )


@pytest.mark.parametrize("alan", ["mod", "kod_kimligi", "ortam", "bagimlilik_ozeti"])
def test_s12_devam_degisen_yurutme_kimligini_yazmaz(tmp_path, monkeypatch, alan):
    depo, _, bas = _s12_acik_kosu(tmp_path, monkeypatch)
    once = depo.yol.read_bytes()
    kimlik = _s12_devam_kimligi(bas)
    kimlik[alan] = dict(kimlik[alan], bagimliliklar={}) if alan == "ortam" else "farkli"
    with pytest.raises(pilot.PilotHatasi):
        with depo.ileri_devam(bas["kosu_id"], **kimlik):
            pass
    assert depo.yol.read_bytes() == once


def test_s12_devam_manifest_sabitken_goruntu_bayti_degismesin(tmp_path, monkeypatch):
    from tansu import tansusinama as ts
    from tests.test_tansusinama import s12_kayitli

    depo, ilk, _ = s12_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(ilk.deneme_id)
    goruntu = tmp_path / "ag" / "wf-goruntu"
    goruntu.mkdir()
    fiyat = goruntu / "fiyat.parquet"
    pd.DataFrame(columns=["sembol", "tarih"]).to_parquet(fiyat)
    (goruntu / "olaylar.json").write_text("{}", encoding="utf-8")
    manifest = goruntu / "manifest.json"
    manifest.write_text(
        json.dumps(
            dict(
                kimlik="wf-goruntu",
                dosyalar={
                    p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (fiyat, goruntu / "olaylar.json")
                },
            )
        ),
        encoding="utf-8",
    )
    v = d["veri_ayarlari"] | dict(
        veri_referanslari=["wf-goruntu"],
        manifest_ozeti=hashlib.sha256(manifest.read_bytes()).hexdigest(),
    )
    m = pilot_deneme(
        depo,
        d["strateji"],
        donemler=d["donemler"],
        veri_ayarlari=v,
        yontem_ayarlari=d["yontem_ayarlari"],
        risk_ayarlari=d["risk_ayarlari"],
        masraf_ayarlari=d["masraf_ayarlari"],
        eski_referans=d["eski_referans"],
    )

    def kes(_):
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        ts.kayitli_ileri_calistir(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=kes
        )
    bas = next(
        o
        for o in depo.oku()
        if o["kayit_turu"] == "baslangic" and o["deneme_id"] == m.deneme_id
    )
    with fiyat.open("ab") as dosya:
        dosya.write(b"degisti")
    once = depo.yol.read_bytes()
    with pytest.raises(veri.VeriHatasi, match="manifest uyuşmuyor"):
        ts.kayitli_ileri_calistir(
            depo,
            m.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            devam_kosu_id=bas["kosu_id"],
            ilerleme=None,
        )
    assert depo.yol.read_bytes() == once


def test_s12_devam_uyelik_kaynagi_degismisse_yazmaz(tmp_path, monkeypatch):
    from tansu import tansusinama as ts

    depo, deneme, bas = _s12_acik_kosu(tmp_path, monkeypatch)
    once = depo.yol.read_bytes()
    asil = veri.uyelik_hazirla

    def degisen(istek):
        return asil(istek) | dict(tablo_parmak_izi="farkli-uyelik")

    monkeypatch.setattr(veri, "oku", lambda *_: None)
    monkeypatch.setattr(veri, "uyelik_hazirla", degisen)
    with pytest.raises(ValueError, match="Üyelik parmak izi"):
        ts.kayitli_ileri_calistir(
            depo,
            deneme.deneme_id,
            veri_koku=tmp_path,
            mod="gelistirme",
            devam_kosu_id=bas["kosu_id"],
            ilerleme=None,
        )
    assert depo.yol.read_bytes() == once


def test_s12_okuyucu_ust_revizyonu_tek_basina_dogrular(tmp_path, monkeypatch):
    from tests.test_tansusinama import s12_kayitli

    depo, makbuz, _ = s12_kayitli(tmp_path, monkeypatch)
    asil = depo.deneme_oku(makbuz.deneme_id)
    kabul_edilen = []
    for tur in (
        "bilinmeyen_alan",
        "eski_ozet",
        "bilinmeyen_yontem",
        "yinelenen",
        "kimlik_surumu",
        "ust_yetim",
        "fazla_alan",
        "float_kimlik",
    ):
        o = deepcopy(asil)
        if tur == "bilinmeyen_alan":
            o["yontem_ayarlari"]["bilinmeyen"] = True
        elif tur == "eski_ozet":
            o["ayar_parmak_izi"] = "eski-ozet"
        elif tur == "bilinmeyen_yontem":
            o["yontem_ayarlari"]["yontem"] = "kayitli_ileri_v999"
        elif tur == "kimlik_surumu":
            o["kimlik_bicimi_surumu"] = "bilinmeyen"
        elif tur == "ust_yetim":
            o["ust_deneme_id"] = "kayitsiz-ust"
        elif tur == "fazla_alan":
            o["surum"] = "bilinmeyen"
        elif tur == "float_kimlik":
            o["deneme_id"] = 1.0
        yol = tmp_path / (tur + "-ust.jsonl")
        yol.write_bytes((pilot.kanonik(o) + b"\n") * (2 if tur == "yinelenen" else 1))
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            continue
        kabul_edilen.append(tur)
    assert kabul_edilen == [], (
        "WF üst revizyonu sonraki olay olmadan da doğrulanmalıdır"
    )


def test_s12_okuyucu_kosu_sahibini_legacy_ustle_gizleyemez(tmp_path, monkeypatch):
    from tests.test_tansusinama import s12_kayitli, s12_calistir

    depo, makbuz, piyasa = s12_kayitli(tmp_path, monkeypatch)
    piyasa[:] = [x for x in piyasa if x["tarih"] != "2022-01-04"]
    sonuc = s12_calistir(depo, makbuz, tmp_path)
    asil = depo.oku()
    legacy = next(
        x
        for x in asil
        if x["kayit_turu"] == "deneme"
        and x["yontem_ayarlari"]["yontem"] == "kayitli_donem_v1"
    )
    kabul_edilen = []
    for tur in (
        "bitis",
        "bitis_baska_kosu",
        "baslangic",
        "baslangic_ozeti",
        "baslangic_legacy_kod",
        "ileri_secim",
        "birlesik",
    ):
        olaylar = deepcopy(asil)
        aranan = (
            "bitis"
            if tur == "bitis_baska_kosu"
            else "baslangic"
            if tur.startswith("baslangic")
            else tur
        )
        hedef = next(
            x
            for x in olaylar
            if x.get("kosu_id") == sonuc["kosu_id"]
            and (
                x["kayit_turu"] == aranan
                or (
                    aranan == "birlesik"
                    and x.get("sonuc_turu") == "ileri_v1"
                    and x["kayit"]["tur"] == "birlesik"
                )
            )
        )
        hedef["deneme_id"] = legacy["deneme_id"]
        if tur != "baslangic":
            hedef["ayar_parmak_izi"] = legacy["ayar_parmak_izi"]
        if tur == "bitis_baska_kosu":
            hedef["kosu_id"] = next(
                x["kosu_id"]
                for x in olaylar
                if x["kayit_turu"] == "baslangic" and x["kosu_id"] != sonuc["kosu_id"]
            )
        if tur == "baslangic_legacy_kod":
            hedef["kod_kimligi"] = hedef["kod_kimligi"].replace(
                "kayitli_ileri_v1", "kayitli_donem_v1", 1
            )
        if tur.startswith("baslangic"):
            olaylar = olaylar[: olaylar.index(hedef) + 1]
        yol = tmp_path / (tur + "-legacy-sahip.jsonl")
        yol.write_bytes(b"".join(pilot.kanonik(x) + b"\n" for x in olaylar))
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            continue
        kabul_edilen.append(tur)
    assert kabul_edilen == [], (
        "WF koşusu legacy üst kimliğiyle anlamsal denetimden kaçamamalıdır"
    )


def test_s12_turetilmis_secim_ve_ozet_yayinda_ve_okumada_dogrulanir(
    tmp_path, monkeypatch
):
    from tests.test_tansusinama import s12_kayitli, s12_calistir
    from tansu import saglamlik

    depo, makbuz, piyasa = s12_kayitli(tmp_path, monkeypatch)
    piyasa[:] = [x for x in piyasa if x["tarih"] not in ("2021-01-04", "2022-01-04")]
    sonuc = s12_calistir(depo, makbuz, tmp_path)
    asil = depo.oku()
    ust = depo.deneme_oku(makbuz.deneme_id)
    baslangic = next(
        x for x in asil if x["kayit_id"] == sonuc["baslangic_makbuzu"].olay_id
    )
    kabul_edilen = []
    for tur in (
        "izinli_alan",
        "secici_aciklamasi",
        "olculer",
        "sayimlar",
        "secimler_eksik",
        "secimler_tekrar",
        "secim_icerigi",
        "basari",
        "bolumler_eksik",
        "ufuk",
        "bitis_olculeri",
        "bitis_sayimlari",
    ):
        hedef = next(
            x
            for x in asil
            if (
                tur in ("izinli_alan", "secici_aciklamasi")
                and x["kayit_turu"] == "ileri_secim"
            )
            or (
                tur
                in (
                    "sayimlar",
                    "secimler_eksik",
                    "secimler_tekrar",
                    "secim_icerigi",
                    "basari",
                )
                and x.get("sonuc_turu") == "ileri_v1"
                and x["kayit"]["tur"] == "bolum"
            )
            or (
                tur in ("olculer", "bolumler_eksik", "ufuk")
                and x.get("sonuc_turu") == "ileri_v1"
                and x["kayit"]["tur"] == "birlesik"
            )
            or (
                tur.startswith("bitis_")
                and x["kayit_turu"] == "bitis"
                and x["kosu_id"] == sonuc["kosu_id"]
            )
        )
        onceki = asil[: asil.index(hedef)]
        yanlis = deepcopy(hedef)
        k = yanlis.get("kayit", {})
        if tur == "izinli_alan":
            hucreler = [
                dict(
                    indeks=h["indeks"],
                    deneme_id=None,
                    durum="alan_disi",
                    kapali_islem_sayisi=None,
                    toplam_net_r=None,
                )
                for h in k["bolge"]["hucreler"]
            ]
            k.update(
                egitim_cocuklari=[],
                durum="secim_yok",
                neden="uygun_merkez_yok",
                bolge=saglamlik.sec(
                    dict(eksenler=ust["yontem_ayarlari"]["eksenler"]),
                    hucreler,
                    politika="genis_bolge_net_r_v1",
                ),
            )
        elif tur == "secici_aciklamasi":
            k["bolge"]["neden"] = "uydurma"
        elif tur == "olculer":
            k["olculer"] = {"UYDURMA": dict(net_r=999999.0)}
        elif tur == "sayimlar":
            k["sayimlar"] = {"TEST": dict(kapali_islem="yanlis_tur")}
        elif tur == "secimler_eksik":
            k["secimler"] = []
        elif tur == "secimler_tekrar":
            k["secimler"].append(deepcopy(k["secimler"][0]))
        elif tur == "secim_icerigi":
            k["secimler"][0]["test_deneme_id"] = "kayitsiz-cocuk"
        elif tur == "basari":
            k.update(durum="tamamlandi", neden=None, hatalar=[])
        elif tur == "bolumler_eksik":
            k["bolum_refleri"] = []
        elif tur == "ufuk":
            k["donem"] = dict(uydurma=True)
        elif tur == "bitis_olculeri":
            yanlis["olculer"] = dict(net_r=999999.0)
        else:
            yanlis["ozetler"] = dict(
                tamamlanan=999, denenen=999, basarisiz=0, baslamayan=0
            )
        yol = tmp_path / (tur + "-yayin.jsonl")
        onceki_bayt = b"".join(pilot.kanonik(o) + b"\n" for o in onceki)
        yol.write_bytes(onceki_bayt)
        kosu = pilot._Kosu(
            pilot.PilotKayit(yol), sonuc["baslangic_makbuzu"], ust, baslangic
        )
        try:
            if hedef["kayit_turu"] == "ileri_secim":
                kosu.ileri_secim_kaydet(kayit=k)
            elif hedef["kayit_turu"] == "sonuc":
                kosu.ileri_sonucu_kaydet(kayit=k)
            else:
                kosu.bitir(
                    **{
                        a: yanlis[a]
                        for a in (
                            "durum",
                            "tamamlanan",
                            "basarisiz",
                            "yontemler",
                            "olculer",
                            "cikti_referanslari",
                            "ozetler",
                        )
                    }
                )
        except pilot.PilotHatasi:
            assert yol.read_bytes() == onceki_bayt
        else:
            kabul_edilen.append((tur, "yayin"))
        yol = tmp_path / (tur + "-okuma.jsonl")
        yol.write_bytes(onceki_bayt + pilot.kanonik(yanlis) + b"\n")
        try:
            pilot.PilotKayit(yol).oku()
        except pilot.PilotHatasi:
            pass
        else:
            kabul_edilen.append((tur, "okuma"))
    assert kabul_edilen == [], (
        "Türetilmiş WF içeriği gerçek kayıtlarına bağlı olmalıdır"
    )


def test_s12_erken_hata_bitisinde_gercek_sayim_ve_neden_korunur(tmp_path, monkeypatch):
    from tests.test_tansusinama import s12_kayitli, s12_calistir
    from tansu import veri

    depo, m, _ = s12_kayitli(tmp_path, monkeypatch)

    def dur(*args, **kwargs):
        raise ValueError("uyelik-denetimi")

    monkeypatch.setattr(veri, "uyelik_hazirla", dur)
    with pytest.raises(ValueError, match="uyelik-denetimi"):
        s12_calistir(depo, m, tmp_path)
    bitis = next(
        x
        for x in depo.oku()
        if x["kayit_turu"] == "bitis" and x["deneme_id"] == m.deneme_id
    )
    assert "hata" in bitis["ozetler"], (
        "Erken hata bitişi gerçek hata gözlemini korumalıdır"
    )
    assert bitis["ozetler"] == dict(
        tamamlanan=0, denenen=0, basarisiz=0, baslamayan=16, hata="uyelik-denetimi"
    )
    assert bitis["durum"] == "hata"
    assert bitis["tamamlanan"] == bitis["cikti_referanslari"] == []
    assert len(bitis["basarisiz"]) == 17
    assert depo.kurtar()["uyarilar"] == []


def test_s12_pay_kimligi_sakli_uyelik_kaniti_canli_tablolardan_bagimsizdir(
    tmp_path, monkeypatch
):
    import builtins
    from tansu import tansusinama as ts
    from tests.test_tansusinama import s12_kayitli, s12_calistir
    from tests.test_veri import pay_kimlikli_goruntu

    asil_uyelik = veri.uyelik_hazirla
    depo, eski, _ = s12_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(eski.deneme_id)
    a, secim = pay_kimlikli_goruntu(tmp_path, monkeypatch)
    v = d["veri_ayarlari"]
    uyelik = asil_uyelik(
        veri.UyelikIstegi(
            tuple(v["takvim"]["seanslar"]), v["evren_politikasi"], v["uyelik_surumu"]
        )
    )
    v.update(
        veri_referanslari=[a.kimlik],
        manifest_ozeti=secim["manifest_ozeti"],
        uyelik_ozeti=uyelik["tablo_parmak_izi"],
        pay_kimligi=secim,
    )
    m = pilot_deneme(
        depo,
        d["strateji"],
        **{
            k: d[k]
            for k in (
                "donemler",
                "yontem_ayarlari",
                "veri_ayarlari",
                "risk_ayarlari",
                "masraf_ayarlari",
            )
        },
    )
    monkeypatch.setattr(veri, "uyelik_hazirla", asil_uyelik)

    def hesap_yok(*args, **kwargs):
        raise ValueError("sentetik hesap öncesi sınır")

    monkeypatch.setattr(ts, "_ileri_secimler", hesap_yok)
    sonuc = s12_calistir(depo, m, tmp_path)
    asil = depo.oku()
    baslangic = next(
        o for o in asil if o["kayit_id"] == sonuc["baslangic_makbuzu"].olay_id
    )
    ilk = next(
        o
        for o in asil
        if o.get("sonuc_turu") == "ileri_v1" and o["kayit"]["tur"] == "bolum"
    )
    assert (
        ilk["kayit"]["durum"] == "hata"
        and "sentetik hesap öncesi sınır" in ilk["kayit"]["neden"]
    )
    ayar_ozeti = depo.deneme_oku(m.deneme_id)["ayar_parmak_izi"]
    assert ayar_ozeti == m.ayar_ozeti

    asil_open, asil_path_open = builtins.open, Path.open

    def kapali(yol):
        return isinstance(yol, (str, Path)) and Path(yol).name in (
            "uyelik.csv",
            "eslemeler.csv",
        )

    def dosya_ac(yol, *args, **kwargs):
        if kapali(yol):
            raise OSError("canlı üyelik ve eşleme tabloları kapalı")
        return asil_open(yol, *args, **kwargs)

    def yol_ac(yol, *args, **kwargs):
        if kapali(yol):
            raise OSError("canlı üyelik ve eşleme tabloları kapalı")
        return asil_path_open(yol, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", dosya_ac)
    monkeypatch.setattr(Path, "open", yol_ac)
    hata = None
    try:
        okunan = pilot.PilotKayit(depo.yol).oku()
    except (OSError, pilot.PilotHatasi) as yakalanan:
        hata = yakalanan
    assert hata is None, f"Geçmiş WF okuması saklı kaynakları kullanmalıdır: {hata}"
    assert okunan == asil
    kanit = baslangic["uyelik_kaniti"]
    assert kanit["surum"] == "ileri_uyelik_kaniti_v1"
    assert (
        hashlib.sha256(kanit["uyelik_tablo_metni"].encode("utf-8")).hexdigest()
        == v["uyelik_ozeti"]
    )
    assert (
        hashlib.sha256(kanit["pay_kimligi_tablo_metni"].encode("utf-8")).hexdigest()
        == secim["tablo_ozeti"]
    )

    onceki = asil[: asil.index(baslangic)]
    onceki_bayt = b"".join(pilot.kanonik(o) + b"\n" for o in onceki)
    for boz in ("eksik", "surum", "alan", "uyelik_ozeti", "pay_ozeti", "metin_turu"):
        yanlis = deepcopy(baslangic)
        if boz == "eksik":
            del yanlis["uyelik_kaniti"]
        elif boz == "surum":
            yanlis["uyelik_kaniti"]["surum"] = "bilinmeyen"
        elif boz == "alan":
            yanlis["uyelik_kaniti"]["fazla"] = True
        elif boz == "uyelik_ozeti":
            yanlis["uyelik_kaniti"]["uyelik_tablo_metni"] += "\n"
        elif boz == "pay_ozeti":
            yanlis["uyelik_kaniti"]["pay_kimligi_tablo_metni"] += "\n"
        else:
            yanlis["uyelik_kaniti"]["pay_kimligi_tablo_metni"] = 0
        yol = tmp_path / (boz + "-sakli-kaynak.jsonl")
        yol.write_bytes(onceki_bayt + pilot.kanonik(yanlis) + b"\n")
        with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır"):
            pilot.PilotKayit(yol).oku()
        yol.write_bytes(onceki_bayt)
        kwargs = {
            a: yanlis[a]
            for a in (
                "mod",
                "anlik_goruntu",
                "manifest_ozeti",
                "uyelik_surumu",
                "kod_kimligi",
                "ortam",
                "bagimlilik_ozeti",
                "tohum",
                "is_listesi",
                "ureteci_surumu",
            )
        }
        if "uyelik_kaniti" in yanlis:
            kwargs["uyelik_kaniti"] = yanlis["uyelik_kaniti"]
        with pytest.raises(pilot.PilotHatasi, match="[Üü]yelik kanıtı"):
            with pilot.PilotKayit(yol).kosu(m.deneme_id, **kwargs):
                pytest.fail("Bozuk kaynak kanıtı başlangıç makbuzu alamaz")
        assert yol.read_bytes() == onceki_bayt


@pytest.mark.parametrize(
    "boz",
    ["yanlis_pay", "uyelik", "saglayici", "tarih", "goruntu", "manifest", "kaynak"],
)
def test_s12_pay_kimligi_sakli_kaynak_ozeti_tek_basina_yetki_vermez(
    tmp_path, monkeypatch, boz
):
    from io import StringIO
    from tests.test_tansusinama import s12_kayitli

    asil_uyelik = veri.uyelik_hazirla
    depo, eski, _ = s12_kayitli(tmp_path, monkeypatch)
    monkeypatch.setattr(veri, "uyelik_hazirla", asil_uyelik)
    d = depo.deneme_oku(eski.deneme_id)
    kok = Path(veri.__file__).parent / "referans"
    uyelik = (kok / "bist30_2021_2025_v1" / "uyelik.csv").read_bytes().decode("utf-8")
    esleme = (kok / "pay_kimligi_v1" / "eslemeler.csv").read_bytes().decode("utf-8")
    satir = pd.read_csv(StringIO(esleme), dtype=str, keep_default_na=False).iloc[0]
    v = d["veri_ayarlari"]
    v.update(
        kaynak=satir["kaynak"],
        veri_referanslari=[satir["goruntu_id"]],
        manifest_ozeti=satir["manifest_ozeti"],
        uyelik_ozeti=hashlib.sha256(uyelik.encode("utf-8")).hexdigest(),
        pay_kimligi=dict(
            surum="pay_kimligi_v1",
            tablo_ozeti=hashlib.sha256(esleme.encode("utf-8")).hexdigest(),
            **{a: satir[a] for a in ("kaynak", "goruntu_id", "manifest_ozeti")},
        ),
    )

    def kaydet():
        return pilot_deneme(
            depo,
            d["strateji"],
            **{
                a: d[a]
                for a in (
                    "donemler",
                    "yontem_ayarlari",
                    "veri_ayarlari",
                    "risk_ayarlari",
                    "masraf_ayarlari",
                )
            },
        )

    kanit = dict(
        surum="ileri_uyelik_kaniti_v1",
        uyelik_tablo_metni=uyelik,
        pay_kimligi_tablo_metni=esleme,
    )
    kwargs = dict(
        mod="gelistirme",
        anlik_goruntu=v["veri_referanslari"][0],
        manifest_ozeti=v["manifest_ozeti"],
        uyelik_surumu=v["uyelik_surumu"],
        is_listesi=[b["ad"] for b in d["donemler"]] + ["birlesik"],
        uyelik_kaniti=kanit,
    )
    gecerli = kaydet()
    with pytest.raises(RuntimeError, match="hesap yok"):
        with pilot_kosu(depo, gecerli.deneme_id, **kwargs):
            raise RuntimeError("hesap yok")
    asil = next(o for o in depo.oku() if o["kayit_turu"] == "baslangic")
    assert pilot.PilotKayit(depo.yol).oku() == depo.oku()

    if boz == "uyelik":
        uyelik = uyelik.replace("AKBNK", "AUDITFAKE")
    elif boz == "yanlis_pay":
        esleme = esleme.replace("TRMET", "TRHOL")
    elif boz == "tarih":
        esleme = esleme.replace("2025-11-24", "2025-11-25")
    else:
        alan = {
            "saglayici": "kaynak",
            "goruntu": "goruntu_id",
            "manifest": "manifest_ozeti",
            "kaynak": "kaynak_id",
        }[boz]
        yeni = "f" * 64 if alan == "manifest_ozeti" else "audit_kanitsiz"
        esleme = esleme.replace(satir[alan], yeni)
        if alan in ("kaynak", "goruntu_id", "manifest_ozeti"):
            v["pay_kimligi"][alan] = yeni
            if alan == "goruntu_id":
                v["veri_referanslari"] = [yeni]
                kwargs["anlik_goruntu"] = yeni
            else:
                v[alan] = yeni
                if alan == "manifest_ozeti":
                    kwargs[alan] = yeni
    kanit.update(uyelik_tablo_metni=uyelik, pay_kimligi_tablo_metni=esleme)
    v["uyelik_ozeti"] = hashlib.sha256(uyelik.encode("utf-8")).hexdigest()
    v["pay_kimligi"]["tablo_ozeti"] = hashlib.sha256(esleme.encode("utf-8")).hexdigest()
    sahte = kaydet()
    once = depo.yol.read_bytes()
    kabul_edilen = []
    try:
        with pilot_kosu(depo, sahte.deneme_id, **kwargs):
            kabul_edilen.append("ekleme")
            raise RuntimeError("hesap yok")
    except pilot.PilotHatasi as hata:
        assert "onaylı kaynak özeti" in str(hata)
        assert depo.yol.read_bytes() == once
    except RuntimeError as hata:
        assert str(hata) == "hesap yok"

    # Yerel olay biçimi korunur; kayıtlı seçim ve iki metnin özeti birlikte değiştirilir.
    yanlis = deepcopy(asil)
    yanlis.update(
        kayit_id=asil["kayit_id"] + ":sahte",
        kosu_id=asil["kosu_id"] + ":sahte",
        deneme_id=sahte.deneme_id,
        ayar_parmak_izi=sahte.ayar_ozeti,
        anlik_goruntu=kwargs["anlik_goruntu"],
        manifest_ozeti=kwargs["manifest_ozeti"],
        uyelik_kaniti=kanit,
    )
    yol = tmp_path / "sahte-sakli-kaynak.jsonl"
    yol.write_bytes(once + pilot.kanonik(yanlis) + b"\n")
    try:
        pilot.PilotKayit(yol).oku()
        kabul_edilen.append("yeni okuyucu")
    except pilot.PilotHatasi as hata:
        assert "Bozuk tam satır" in str(hata)
        assert "onaylı kaynak özeti" in str(hata.__cause__)
    assert kabul_edilen == [], "Çağıranın tutarlı özeti kaynağa yetki veremez"


def test_s12_ham_aralik_politikasi_kontrol_ekleme_ve_taze_okumaya_baglidir(
    tmp_path, monkeypatch
):
    from copy import deepcopy
    from tansu import motor
    from tests.test_tansusinama import s12_sinyalli, s12_calistir

    depo, m, _ = s12_sinyalli(
        tmp_path, monkeypatch, kilit_politikasi="ham_aralik_v1", limit=False
    )
    asil = pilot._Kosu.ileri_kontrol_kaydet
    reddedilen = []

    def politikasiz(durum):
        d = deepcopy(durum)
        d["yurutme"].pop("kilit_politikasi")
        d.pop("butunluk")
        return d | dict(butunluk=motor._iz_kodu(d))

    def kontrol(kosu, *, bolum_id, sembol, durum, onceki_ref):
        once = depo.yol.read_bytes()
        with pytest.raises(ValueError, match="uyuşmuyor"):
            asil(
                kosu,
                bolum_id=bolum_id,
                sembol=sembol,
                durum=politikasiz(durum),
                onceki_ref=onceki_ref,
            )
        assert depo.yol.read_bytes() == once
        reddedilen.append(bolum_id)
        return asil(
            kosu,
            bolum_id=bolum_id,
            sembol=sembol,
            durum=durum,
            onceki_ref=onceki_ref,
        )

    monkeypatch.setattr(pilot._Kosu, "ileri_kontrol_kaydet", kontrol)
    r = s12_calistir(depo, m, tmp_path)
    assert r["durum"] == "tamamlandi"
    assert len(reddedilen) == 16
    olaylar = pilot.PilotKayit(depo.yol).oku()
    ust = depo.deneme_oku(m.deneme_id)
    for o in olaylar:
        if o["kayit_turu"] == "deneme" and o["ust_deneme_id"] == m.deneme_id:
            assert (
                o["yontem_ayarlari"]["hucre_yontemi"]
                == ust["yontem_ayarlari"]["hucre_yontemi"]
            )
    for o in olaylar:
        if o["kayit_turu"] == "ileri_kontrol":
            o["durum"] = politikasiz(o["durum"])
            break
    yol = tmp_path / "politikasiz-kontrol.jsonl"
    yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
    with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır") as hata:
        pilot.PilotKayit(yol).oku()
    assert "önceki durum veya yürütme bağı uyuşmuyor" in str(hata.value.__cause__)


def test_kilit_politikasi_yeni_ayar_ozeti_eski_kaydi_degistirmez(tmp_path, monkeypatch):
    from copy import deepcopy
    from tests.test_tansusinama import s10_kayitli, s10_revizyon

    depo, m, _ = s10_kayitli(tmp_path, monkeypatch)
    eski = deepcopy(depo.deneme_oku(m.deneme_id))
    assert "kilit_politikasi" not in eski["yontem_ayarlari"]
    once = depo.yol.read_bytes()
    yeni = s10_revizyon(
        depo,
        m,
        yontem_ayarlari=eski["yontem_ayarlari"]
        | dict(kilit_politikasi="ham_aralik_v1"),
    )
    assert yeni.ayar_ozeti != m.ayar_ozeti
    assert depo.yol.read_bytes().startswith(once)
    taze = pilot.PilotKayit(depo.yol)
    assert taze.deneme_oku(m.deneme_id) == eski
    assert (
        taze.deneme_oku(yeni.deneme_id)["yontem_ayarlari"]["kilit_politikasi"]
        == "ham_aralik_v1"
    )


@pytest.mark.parametrize("tekrar", [False, 0.0])
@pytest.mark.parametrize("politika", [None, "ham_aralik_v1"])
def test_s11_yerel_yontem_kapisi_esdeger_ama_kanonik_olmayan_turu_reddeder(
    tmp_path, tekrar, politika
):
    # TASARIM 5.15: yerel S11 yayınının ortak yöntem kapısı türleri korur.
    depo = pilot.PilotKayit(tmp_path / "kanonik-arama.jsonl")
    kayit = pilot_arama_ust(depo)
    ust = deepcopy(depo.deneme_oku(kayit.deneme_id))
    hucre = ust["yontem_ayarlari"]["hucre_yontemi"]
    hucre["tekrar"] = tekrar
    if politika is not None:
        hucre["kilit_politikasi"] = politika
    once = depo.yol.read_bytes()
    hata = None
    try:
        pilot._arama_yontemi(ust, "genis_bolge_net_r_v1")
    except pilot.PilotHatasi as exc:
        hata = str(exc)
    assert hata is not None and "yürütme ayarı" in hata
    assert depo.yol.read_bytes() == once


def test_dogal_isinma_ekleme_ve_yeni_okuma_ayni_sakli_kaniti_denetler(
    tmp_path, monkeypatch
):
    import builtins
    from tansu import tansusinama as ts
    from tests.test_tansusinama import dogal_isinma_kayitli

    depo, m, _ = dogal_isinma_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(m.deneme_id)
    kod, ortam = ts._kayitli_kimlik(*kayit._git(), 1)
    donem = d["donemler"][2]
    is_id = "donem:2023"
    with ts._ileri_kosu(depo, d, "gelistirme", kod, ortam, [is_id]) as kosu:
        r = ts._kayitli_sonuc(d, kosu.makbuz.kosu_id, is_id, donem)
        paket = ts._donem_verisi(d, r, tmp_path)
        assert paket is not None
        r = ts._kayitli_donem((d, r, paket))
        assert r["durum"] == "tamamlandi", r["hatalar"]
        assert r["isinma"]["ASTOR"]["dogal_bekleyis"]["isinma_tamamlanma_gunu"] is None
        prefix = depo.yol.read_bytes()
        for boz in (
            "sayi",
            "gerekli",
            "bool",
            "gelecek_500",
            "kaynak_ref",
            "eksik_neden",
            "eksik_uye",
            "e1_onek",
            "e1_isinma_kesimi",
        ):
            yanlis = deepcopy(r)
            x = yanlis["isinma"]["ASTOR"]
            if boz == "sayi":
                x["gozlem"] += 1
            elif boz == "gerekli":
                x["gerekli"] = 499
            elif boz == "bool":
                x["tamam"] = 0
            elif boz == "gelecek_500":
                x["dogal_bekleyis"]["isinma_tamamlanma_gunu"] = "2024-12-17"
            elif boz == "kaynak_ref":
                x["dogal_bekleyis"]["e1_ref"] = "yanlis"
            elif boz == "eksik_neden":
                del x["dogal_bekleyis"]
            elif boz == "eksik_uye":
                del yanlis["isinma"]["ASTOR"]
                del yanlis["durumlar"]["ASTOR"]
            elif boz == "e1_isinma_kesimi":
                yanlis["veri_referansi"]["isinma_donemi"]["baslangic"] = "2023-07-03"
            else:
                yanlis["veri_referansi"]["gecmis_kaniti"]["ASTOR"]["gozlem_ozeti"] = (
                    "0" * 64
                )
            with pytest.raises(pilot.PilotHatasi, match="[ıIİi]sınma|[ıIİi]şlem"):
                kosu.donem_sonucu_kaydet(
                    is_id=is_id,
                    donem=donem,
                    durum="tamamlandi",
                    islem_referanslari=[],
                    birimler=ts.DONEM_BIRIMLERI,
                    muhasebe_politikasi="tani_referans_v1",
                    uyarilar=[],
                    cikti_referanslari=[],
                    icerik=yanlis,
                )
            assert depo.yol.read_bytes() == prefix
            o = dict(
                kayit_id="fixture:" + boz,
                sema_surumu=pilot.SURUM,
                olusturma_zamani=__import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc
                ),
                kayit_turu="sonuc",
                sonuc_turu="donem_v1",
                deneme_id=m.deneme_id,
                kosu_id=kosu.makbuz.kosu_id,
                ayar_parmak_izi=m.ayar_ozeti,
                is_id=is_id,
                donem=donem,
                durum="tamamlandi",
                icerik=yanlis,
            )
            yol = tmp_path / (boz + "-okuma.jsonl")
            yol.write_bytes(prefix + pilot.kanonik(o) + b"\n")
            with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır"):
                pilot.PilotKayit(yol).oku()
        r = ts._donem_yaz(kosu, r, [])
        kosu.bitir(
            durum="tamamlandi",
            tamamlanan=[is_id],
            basarisiz=[],
            yontemler=[],
            olculer={},
            cikti_referanslari=[r["makbuz"].olay_id],
            ozetler={},
        )
    asil = depo.oku()
    bas = next(o for o in asil if o["kayit_turu"] == "baslangic")
    onceki = asil[: asil.index(bas)]
    for boz in ("eksik", "surum", "kaynak"):
        yanlis = deepcopy(bas)
        if boz == "eksik":
            del yanlis["uyelik_kaniti"]
        elif boz == "surum":
            yanlis["uyelik_kaniti"]["surum"] = "bilinmeyen"
        else:
            yanlis["uyelik_kaniti"]["ilk_islem_tablo_metni"] += "\n"
        yol = tmp_path / (boz + "-baslangic.jsonl")
        yol.write_bytes(
            b"".join(pilot.kanonik(o) + b"\n" for o in onceki)
            + pilot.kanonik(yanlis)
            + b"\n"
        )
        with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır"):
            pilot.PilotKayit(yol).oku()
        yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in onceki))
        kwargs = {
            a: bas[a]
            for a in (
                "mod",
                "anlik_goruntu",
                "manifest_ozeti",
                "uyelik_surumu",
                "kod_kimligi",
                "ortam",
                "bagimlilik_ozeti",
                "tohum",
                "is_listesi",
                "ureteci_surumu",
            )
        }
        if "uyelik_kaniti" in yanlis:
            kwargs["uyelik_kaniti"] = yanlis["uyelik_kaniti"]
        with pytest.raises(pilot.PilotHatasi, match="[Kk]anıt|[ıIİi]şlem"):
            with pilot.PilotKayit(yol).kosu(m.deneme_id, **kwargs):
                pytest.fail("Geçersiz START hesap sınırına ulaşamaz")
    asil_open, asil_path_open = builtins.open, Path.open

    def dosya_ac(yol, *args, **kwargs):
        if isinstance(yol, (str, Path)) and Path(yol).name in (
            "uyelik.csv",
            "eslemeler.csv",
            "ilk_islem.csv",
        ):
            raise OSError("canlı kaynaklar kapalı")
        return asil_open(yol, *args, **kwargs)

    def yol_ac(yol, *args, **kwargs):
        if yol.name in ("uyelik.csv", "eslemeler.csv", "ilk_islem.csv"):
            raise OSError("canlı kaynaklar kapalı")
        return asil_path_open(yol, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", dosya_ac)
    monkeypatch.setattr(Path, "open", yol_ac)
    assert pilot.PilotKayit(depo.yol).oku() == asil


@pytest.mark.parametrize(
    "alan", ["pay_kimligi_tablo_metni", "uyelik_tablo_metni", "ilk_islem_tablo_metni"]
)
def test_dogal_isinma_start_bos_kaynak_canli_tabloya_donmez(
    tmp_path, monkeypatch, alan
):
    from tansu import tansusinama as ts
    from tests.test_tansusinama import s10_kayitli

    asil_uyelik = veri.uyelik_hazirla
    depo, eski, _ = s10_kayitli(tmp_path, monkeypatch)
    monkeypatch.setattr(veri, "uyelik_hazirla", asil_uyelik)
    d = depo.deneme_oku(eski.deneme_id)
    kok = Path(veri.__file__).parent / "referans"
    ilk_bayt = (kok / "ilk_islem_v1" / "ilk_islem.csv").read_bytes()
    pay_bayt = (kok / "pay_kimligi_v1" / "eslemeler.csv").read_bytes()
    uyelik_bayt = (kok / "bist30_2021_2025_v1" / "uyelik.csv").read_bytes()
    from io import BytesIO

    satir = pd.read_csv(BytesIO(ilk_bayt), dtype=str).iloc[0]
    bag = {a: satir[a] for a in ("kaynak", "goruntu_id", "manifest_ozeti")}
    v = d["veri_ayarlari"] | dict(
        kaynak=bag["kaynak"],
        veri_referanslari=[bag["goruntu_id"]],
        manifest_ozeti=bag["manifest_ozeti"],
        uyelik_ozeti=hashlib.sha256(uyelik_bayt).hexdigest(),
        ilk_islem=dict(
            surum="ilk_islem_v1",
            tablo_ozeti=hashlib.sha256(ilk_bayt).hexdigest(),
            **bag,
        ),
        pay_kimligi=dict(
            surum="pay_kimligi_v1",
            tablo_ozeti=hashlib.sha256(pay_bayt).hexdigest(),
            **bag,
        ),
    )
    m = pilot_deneme(
        depo,
        d["strateji"],
        **{a: d[a] for a in ("donemler", "risk_ayarlari", "masraf_ayarlari")},
        veri_ayarlari=v,
        yontem_ayarlari=d["yontem_ayarlari"]
        | dict(isinma_politikasi="kaynakli_isinma_v1"),
    )
    kanit = ts._ileri_uyelik_kaniti(v)
    kwargs = dict(
        mod="gelistirme",
        anlik_goruntu=bag["goruntu_id"],
        manifest_ozeti=bag["manifest_ozeti"],
        uyelik_surumu=v["uyelik_surumu"],
        is_listesi=["donem:2023"],
        uyelik_kaniti=kanit,
    )
    with pytest.raises(RuntimeError, match="hesap yok"):
        with pilot_kosu(depo, m.deneme_id, **kwargs):
            raise RuntimeError("hesap yok")
    olaylar = depo.oku()
    bas = next(o for o in olaylar if o["kayit_turu"] == "baslangic")
    prefix = b"".join(pilot.kanonik(o) + b"\n" for o in olaylar[: olaylar.index(bas)])
    yanlis = deepcopy(bas)
    yanlis["uyelik_kaniti"][alan] = None
    yol = tmp_path / (alan + "-taze.jsonl")
    yol.write_bytes(prefix + pilot.kanonik(yanlis) + b"\n")
    asil_open = Path.open
    canli_okuma = []

    def ac(p, *args, **kwargs):
        if p.name in ("uyelik.csv", "eslemeler.csv", "ilk_islem.csv"):
            canli_okuma.append(p.name)
            raise OSError("canlı tablo okuma yasak")
        return asil_open(p, *args, **kwargs)

    monkeypatch.setattr(Path, "open", ac)
    assert pilot.PilotKayit(depo.yol).oku() == olaylar
    hatalar = []
    once = depo.yol.read_bytes()
    for oku in (False, True):
        try:
            if oku:
                pilot.PilotKayit(yol).oku()
            else:
                with pilot_kosu(
                    depo,
                    m.deneme_id,
                    **(kwargs | dict(uyelik_kaniti=yanlis["uyelik_kaniti"])),
                ):
                    raise RuntimeError("geçersiz START kabul edildi")
        except (pilot.PilotHatasi, OSError) as hata:
            hatalar.append(hata)
    assert len(hatalar) == 2 and all(isinstance(h, pilot.PilotHatasi) for h in hatalar)
    assert canli_okuma == [], "Eksik saklı metin canlı parser yoluna ulaşamaz"
    assert depo.yol.read_bytes() == once


def test_s13_dogal_isinma_kaydi_wf_hucresine_onekte_baglanir(tmp_path, monkeypatch):
    from tansu import tansusinama as ts
    from tests.test_tansusinama import (
        dogal_isinma_ileri_kayitli,
        s10_revizyon,
        s13_yontem,
    )

    depo, wf = dogal_isinma_ileri_kayitli(tmp_path, monkeypatch)
    kaynak = dict(
        deneme_id=wf.deneme_id,
        kosu_id="henuz-baslamamis-wf",
        sonuc_ref="henuz-yayimlanmamis-sonuc",
        bitis_ref="henuz-yayimlanmamis-bitis",
        icerik_ozeti="00" * 32,
    )
    # Kayıt eşleşmesi tamamlanmış WF uygunluğu değildir. Hesap burada başlamaz.
    donemler = [
        dict(
            ad=str(y),
            baslangic=dt.date(y, 1, 1),
            bitis=dt.date(y, 12, 31),
            isinma_baslangici=dt.date(2018, 1, 1),
            sinir_surumu="surekli_ileri_v1",
        )
        for y in range(2022, 2026)
    ]
    donemler.append(dict(donemler[0], ad="birlesik", bitis=dt.date(2025, 12, 31)))
    m, hata = None, None
    try:
        m = s10_revizyon(
            depo, wf, donemler=donemler, yontem_ayarlari=s13_yontem(kaynak)
        )
    except pilot.PilotHatasi as yakalanan:
        hata = yakalanan
    assert m is not None, f"MC kaydı eşleşmiş donmuş WF hücresini kullanmalıdır: {hata}"
    d = depo.deneme_oku(m.deneme_id)
    assert d["yontem_ayarlari"] == s13_yontem(kaynak)
    assert "hucre_yontemi" not in d["yontem_ayarlari"]
    assert d["veri_ayarlari"] == depo.deneme_oku(wf.deneme_id)["veri_ayarlari"]
    once = depo.yol.read_bytes()
    olaylar = depo.oku()
    onceki = b"".join(pilot.kanonik(o) + b"\n" for o in olaylar[:-1])
    for boz in ("ilk_islem_yok", "veri_farki", "kaynak_yok", "wf_degil"):
        yanlis = deepcopy(d)
        if boz == "ilk_islem_yok":
            del yanlis["veri_ayarlari"]["ilk_islem"]
        elif boz == "veri_farki":
            yanlis["veri_ayarlari"]["takvim"]["kaynak_ref"] = "baska-kayitli-takvim"
        elif boz == "kaynak_yok":
            yanlis["yontem_ayarlari"]["kaynak"]["deneme_id"] = "kayitsiz-wf"
        else:
            yanlis["yontem_ayarlari"]["kaynak"]["deneme_id"] = olaylar[0]["deneme_id"]
        with pytest.raises(pilot.PilotHatasi, match="MC.*(kayna|veri)|WF"):
            s10_revizyon(
                depo,
                m,
                veri_ayarlari=yanlis["veri_ayarlari"],
                yontem_ayarlari=yanlis["yontem_ayarlari"],
            )
        assert depo.yol.read_bytes() == once
        yanlis["ayar_parmak_izi"] = pilot._ayar_ozeti(
            dict(
                strateji={
                    a: x
                    for a, x in yanlis["strateji"].items()
                    if a != "olusturma_zamani"
                }
            )
            | {
                a: yanlis[a]
                for a in (
                    "donemler",
                    "veri_ayarlari",
                    "yontem_ayarlari",
                    "risk_ayarlari",
                    "masraf_ayarlari",
                )
            }
        )
        yol = tmp_path / ("mc-kayit-" + boz + ".jsonl")
        ham = onceki + pilot.kanonik(yanlis) + b"\n"
        yol.write_bytes(ham)
        with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır") as ret:
            pilot.PilotKayit(yol).oku()
        assert "MC ısınma kaynağı" in str(ret.value.__cause__) or (
            "MC ısınma kaynağının" in str(ret.value.__cause__)
        )
        assert yol.read_bytes() == ham
    monkeypatch.setattr(veri, "ILK_ISLEM_KOKU", tmp_path / "olmayan-tablo")
    assert pilot.PilotKayit(depo.yol).deneme_oku(m.deneme_id) == d
    assert not any(o["kayit_turu"] == "baslangic" for o in depo.oku())
    with pytest.raises(pilot.PilotHatasi, match="kaynak_wf_yok"):
        ts.kayitli_monte_carlo_calistir(
            depo, m.deneme_id, veri_koku=tmp_path, mod="gelistirme", ilerleme=None
        )
    assert depo.yol.read_bytes() == once


def test_s13_kurulmus_isinma_sahibi_ara_durumu_ve_is_kumesini_korur(
    tmp_path, monkeypatch
):
    from tansu import istatistik
    from tansu import tansusinama as ts
    from tests.test_tansusinama import dogal_isinma_kayitli

    # İki gerçek E1/E2/E3 kesimi. Bu kurulmuş sahip girdisi uygun WF kaynağı değildir.
    depo, m, _ = dogal_isinma_kayitli(tmp_path, monkeypatch)
    d = depo.deneme_oku(m.deneme_id)
    hucre = d["yontem_ayarlari"]
    yurutme_d = d | dict(yontem_ayarlari=dict(hucre_yontemi=hucre))
    donemler = [
        dict(
            ad=f"2023Q{q}",
            baslangic=dt.date(2023, ay, 1),
            bitis=dt.date(2023, son_ay, son_gun),
            isinma_baslangici=dt.date(2018, 1, 1),
            sinir_surumu="surekli_ileri_v1",
        )
        for q, ay, son_ay, son_gun in ((3, 7, 9, 30), (4, 10, 12, 31))
    ]
    kod, ortam = ts._kayitli_kimlik(*kayit._git(), 1)
    durumlar, bolumler = {}, []
    isler = [q["ad"] for q in donemler]
    with ts._ileri_kosu(depo, d, "gelistirme", kod, ortam, isler) as kosu:
        for q in donemler:
            r = ts._kayitli_sonuc(d, kosu.makbuz.kosu_id, q["ad"], q)
            paket = ts._ileri_test_paketi(d, r, tmp_path, durumlar)
            for sembol in paket["semboller"]:
                durumlar[sembol] = ts._ileri_test_sembolu(
                    depo,
                    yurutme_d,
                    kosu,
                    r,
                    paket,
                    sembol,
                    None,
                    durumlar.get(sembol),
                    paket["uyelik"],
                )
            assert r["hatalar"] == []
            bolumler.append(
                dict(
                    bolum=q["ad"],
                    durum="tamamlandi",
                    hatalar=[],
                    donem=q,
                    veri_referansi=r["veri_referansi"],
                    isinma=r["isinma"],
                    durumlar={s: deepcopy(durumlar[s]) for s in paket["semboller"]},
                )
            )
        kosu.bitir(
            durum="iptal",
            tamamlanan=[],
            basarisiz=isler,
            yontemler=[],
            olculer={},
            cikti_referanslari=[],
            ozetler=dict(
                hata="Yalnız kurulmuş MC sahip kontrolü. WF/MC tam koşusu değildir."
            ),
        )
    b = next(o for o in depo.oku() if o["kayit_id"] == kosu.makbuz.olay_id)
    kanit = b["uyelik_kaniti"]
    assert all(len(q["durumlar"]) == 30 for q in bolumler)
    assert bolumler[0]["isinma"]["ASTOR"]["tamam"] is False
    assert bolumler[0]["isinma"]["ASTOR"]["dogal_bekleyis"]["neden"] == "dogal_isinma"
    assert (
        bolumler[0]["isinma"]["ASTOR"]["dogal_bekleyis"]["isinma_tamamlanma_gunu"]
        is None
    )
    tekrar = dict(durumlar=deepcopy(durumlar), bolumler=bolumler)
    # Eski sahip bu yeni politikada kanıtsız on altı bölüm iddiasını kabul ediyordu.
    # Önek yalnız bu saf sahibi sınar; yerel günlükte sahte MC/WF sonucu yayımlanmaz.
    is_ = dict(
        anahtar="kurulmus-sahip",
        deney="ayar_komsulugu_v1",
        tanim=dict(
            dilim=dict(baslangic=dt.date(2023, 7, 1), bitis=dt.date(2023, 12, 31))
        ),
    )
    g = dict(
        kaynak=dict(deneme_id=d["deneme_id"]),
        isler=[is_],
        seanslar=d["veri_ayarlari"]["takvim"]["seanslar"],
        nufus=[],
        semboller=sorted(durumlar),
        kontrol_referanslari=["kurulmus:" + s for s in sorted(durumlar)],
    )
    onek = [d | dict(yontem_ayarlari=dict(hucre_yontemi=hucre))]
    onek.append(
        dict(
            kayit_turu="mc_girdi",
            kayit_id="kurulmus:girdi",
            kayit=g,
            deneme_id=d["deneme_id"],
            kosu_id=b["kosu_id"],
            ayar_parmak_izi=d["ayar_parmak_izi"],
        )
    )
    onek.extend(
        dict(kayit_turu="ileri_kontrol", kayit_id="kurulmus:" + s, sembol=s)
        for s in sorted(durumlar)
    )
    p = dict(girdi_ref="kurulmus:girdi", anahtar=is_["anahtar"], cekilis={})
    eski = dict(
        durumlar=durumlar,
        bolumler=[
            dict(bolum=f"{y}Q{q}", durum="tamamlandi", hatalar=[])
            for y in range(2022, 2026)
            for q in range(1, 5)
        ],
    )
    k = dict(
        plan_ref="kurulmus:plan",
        yeniden_sinama=eski,
        sonuc_referanslari=[],
        **istatistik.mc_senaryo_olculeri(g, is_, {}, durumlar=durumlar),
    )
    with pytest.raises(pilot.PilotHatasi, match="MC.*ısınma|MC.*bölüm"):
        pilot._mc_sonuc_kaniti(onek, d, b, p, k)

    def sakla(tam):
        sonuc = deepcopy(tam)
        for q in sonuc["bolumler"]:
            q["durumlar"] = {
                pay: ts._mc_bolum_durumunu_sakla(ara, tam["durumlar"][pay])
                for pay, ara in q["durumlar"].items()
            }
        return sonuc

    nihai_once = pilot.kanonik(tekrar["durumlar"])
    sikisik = deepcopy(tekrar)
    for q in sikisik["bolumler"]:
        for sembol, durum in q["durumlar"].items():
            q["durumlar"][sembol] = dict(
                durum={
                    a: x
                    for a, x in durum.items()
                    if a not in ("iz", "islemler", "retler")
                },
                gecmis_onekleri={
                    a: len(durum[a]) for a in ("iz", "islemler", "retler")
                },
            )
    hata = None
    try:
        pilot._mc_isinma_bolumleri_dogrula(
            [],
            d,
            b,
            k | dict(yeniden_sinama=sikisik),
            donemler=donemler,
            kanit=kanit,
            yurutme_d=yurutme_d,
        )
    except pilot.PilotHatasi as exc:
        hata = str(exc)
    assert hata is None, f"Kayıpsız E3 geçmiş önekleri geri kurulmalıdır: {hata}"
    uretilen = sakla(tekrar)
    assert pilot.kanonik(uretilen) == pilot.kanonik(sikisik)
    for tam_q, kisa_q in zip(tekrar["bolumler"], uretilen["bolumler"], strict=True):
        for pay, ara in tam_q["durumlar"].items():
            acik = pilot._mc_bolum_durumunu_ac(
                kisa_q["durumlar"][pay], tekrar["durumlar"][pay]
            )
            assert pilot.kanonik(acik) == pilot.kanonik(ara)
    assert pilot.kanonik(tekrar["durumlar"]) == nihai_once
    for uzunluk in (True, -1, 1.5, "1", 1000000):
        yanlis = deepcopy(sikisik)
        yanlis["bolumler"][0]["durumlar"]["ASTOR"]["gecmis_onekleri"]["iz"] = uzunluk
        with pytest.raises(pilot.PilotHatasi, match="geçmiş öneğinin uzunluğu"):
            pilot._mc_isinma_bolumleri_dogrula(
                [],
                d,
                b,
                k | dict(yeniden_sinama=yanlis),
                donemler=donemler,
                kanit=kanit,
                yurutme_d=yurutme_d,
            )
    yanlis = deepcopy(sikisik)
    ara = yanlis["bolumler"][0]["durumlar"]["ASTOR"]
    ara["durum"]["karantina_kalan"] = 1
    with pytest.raises(pilot.PilotHatasi, match="önceki durum veya yürütme bağı"):
        pilot._mc_isinma_bolumleri_dogrula(
            [],
            d,
            b,
            k | dict(yeniden_sinama=yanlis),
            donemler=donemler,
            kanit=kanit,
            yurutme_d=yurutme_d,
        )
    yanlis = deepcopy(sikisik)
    ara = yanlis["bolumler"][0]["durumlar"]["ASTOR"]
    ara["gecmis_onekleri"]["iz"] += 1
    acik = pilot._mc_bolum_durumunu_ac(ara, tekrar["durumlar"]["ASTOR"])
    acik.pop("butunluk")
    ara["durum"]["butunluk"] = motor._iz_kodu(acik)
    with pytest.raises(pilot.PilotHatasi, match="tam seans önekini"):
        pilot._mc_isinma_bolumleri_dogrula(
            [],
            d,
            b,
            k | dict(yeniden_sinama=yanlis),
            donemler=donemler,
            kanit=kanit,
            yurutme_d=yurutme_d,
        )
    assert yanlis["durumlar"] == tekrar["durumlar"]
    # Yalnız E5 sinyal bağı için kurulmuş önek. Bu bir E2 sinyal üretim kanıtı değildir.
    sd = d | dict(
        yontem_ayarlari=d["yontem_ayarlari"] | dict(kaynak=dict(kosu_id=b["kosu_id"]))
    )
    cocuk = d | dict(donemler=[donemler[0]])
    plan = dict(
        stres_cocuklari=[
            dict(
                secim_ref="kurulmus:secim",
                deneme_id=d["deneme_id"],
                bolum="2023Q3",
                sembol="ASTOR",
            )
        ]
    )
    po = dict(
        kayit_turu="mc_plan",
        kayit_id="kurulmus:plan",
        kayit=plan,
        deneme_id=d["deneme_id"],
        kosu_id=b["kosu_id"],
        ayar_parmak_izi=d["ayar_parmak_izi"],
    )
    sinyal = dict(
        plan_ref=po["kayit_id"],
        secim_ref="kurulmus:secim",
        deneme_id=d["deneme_id"],
        bolum="2023Q3",
        sembol="ASTOR",
        tarih="2023-07-03",
        sinyal=dict(
            sembol="ASTOR",
            tarih="2023-07-03",
            parametreler=motor._duz(
                {a["ad"]: a["deger"] for a in d["strateji"]["parametreler"]}
            ),
            veri_ref=deepcopy(bolumler[0]["veri_referansi"]),
            kaynak_sinyal=dict(
                semboller=["ASTOR"],
                tarih="2023-07-03",
                baglar=dict(
                    ayar_parmak_izi=d["strateji"]["ayar_parmak_izi"],
                    veri_ref_id=bolumler[0]["veri_referansi"]["kayit_id"],
                ),
            ),
        ),
    )
    for boz in ("ilk_islem", "gecmis", "erken_sinyal"):
        yanlis = deepcopy(sinyal)
        if boz == "ilk_islem":
            yanlis["sinyal"]["veri_ref"]["ilk_islem"]["tablo_ozeti"] = "00" * 32
        elif boz == "gecmis":
            yanlis["sinyal"]["veri_ref"]["gecmis_kaniti"]["ASTOR"]["gozlem_ozeti"] = (
                "00" * 32
            )
        with pytest.raises(pilot.PilotHatasi, match="MC.*ısınma|MC.*ilk işlem"):
            pilot._mc_sinyal_dogrula([cocuk, b, po], sd, b, yanlis)
    for boz in ("ara_durum", "eksik_is", "gelecek_kesim"):
        yanlis = deepcopy(tekrar)
        q = yanlis["bolumler"][0]
        if boz == "ara_durum":
            durum = q["durumlar"]["ASTOR"]
            durum["iz"][-1]["net_sonuc"] = 1.0
            durum.pop("butunluk")
            durum["butunluk"] = motor._iz_kodu(durum)
        elif boz == "eksik_is":
            del q["isinma"]["ASTOR"]
            del q["durumlar"]["ASTOR"]
        else:
            q["isinma"]["ASTOR"]["dogal_bekleyis"]["isinma_tamamlanma_gunu"] = (
                "2024-12-17"
            )
        assert yanlis["durumlar"] == tekrar["durumlar"]
        with pytest.raises(pilot.PilotHatasi, match="MC.*ısınma|MC.*bölüm"):
            pilot._mc_isinma_bolumleri_dogrula(
                [],
                d,
                b,
                k | dict(yeniden_sinama=sakla(yanlis)),
                donemler=donemler,
                kanit=kanit,
                yurutme_d=yurutme_d,
            )
    # Ayrı E3 girdisi: dönem sonunda bekleyen sinyal sonraki seansta düşer.
    # Bu kontrol E2'nin bu sinyali ürettiğini iddia etmez.
    strateji = ts.katalog.legacy_coz(
        d["strateji"]["varyant"],
        d["strateji"]["katalog_surumu"],
        sayisal_ayarlar={
            a["ad"]: a["deger"]
            for a in d["strateji"]["parametreler"]
            if a["koken"] == "legacy_izgara"
        },
    )
    parametre = aileler.Parametre(**{a.ad: a.deger for a in strateji.parametreler})
    hesap = aileler.ortak_donem_kurulumu(paket | dict(semboller=["EREGL"]), strateji)[
        "EREGL"
    ]
    mumlar = ts._s10_mumlar(paket, "EREGL", hesap, kilit_politikasi="ham_aralik_v1")
    mumlar.loc[pd.Timestamp("2023-10-02"), "islem"] = False
    sinyal_id = "kurulmus:bekleyen"
    bekleyen = motor.tara(
        mumlar.loc["2023-07-01":"2023-09-30"],
        {pd.Timestamp("2023-09-29"): sinyal_id},
        parametre,
        kurulum=hesap["kurulum"],
        yurutme=ts._ileri_yurutme(yurutme_d, b["kosu_id"], "EREGL"),
    )
    dusen = motor.tara(
        mumlar.loc["2023-10-01":"2023-12-31"],
        {},
        parametre,
        kurulum=hesap["kurulum"],
        yurutme=ts._ileri_yurutme(yurutme_d, b["kosu_id"], "EREGL"),
        onceki_durum=bekleyen,
    )
    assert bekleyen["pozisyon"]["durum"] == "bekliyor"
    assert dusen["pozisyon"] is None and dusen["islemler"] == []
    assert any(
        x["tur"] == "dusen_sinyal" and x["sinyal_id"] == sinyal_id
        for x in dusen["retler"]
    )
    tasima = deepcopy(tekrar)
    tasima["bolumler"][0]["durumlar"]["EREGL"] = bekleyen
    tasima["bolumler"][1]["durumlar"]["EREGL"] = dusen
    tasima["durumlar"]["EREGL"] = dusen
    so = dict(
        kayit_turu="mc_sinyal",
        kayit_id=sinyal_id,
        deneme_id=d["deneme_id"],
        kosu_id=b["kosu_id"],
        ayar_parmak_izi=d["ayar_parmak_izi"],
        kayit=dict(
            plan_ref=k["plan_ref"],
            bolum="2023Q3",
            sembol="EREGL",
            tarih="2023-09-29",
            sinyal=dict(
                parametreler=motor._duz(asdict(parametre)),
                kaynak_sinyal=dict(
                    semboller=["EREGL"],
                    tarih="2023-09-29",
                    baglar=dict(
                        ayar_parmak_izi=d["strateji"]["ayar_parmak_izi"],
                        veri_ref_id=bolumler[0]["veri_referansi"]["kayit_id"],
                    ),
                ),
            ),
        ),
    )
    hata = None
    try:
        pilot._mc_isinma_bolumleri_dogrula(
            [so],
            d,
            b,
            k | dict(yeniden_sinama=sakla(tasima)),
            donemler=donemler,
            kanit=kanit,
            yurutme_d=yurutme_d,
        )
    except pilot.PilotHatasi as exc:
        hata = str(exc)
    assert hata is None, f"Sonraki çeyrekte düşen bekleyen sinyal reddedildi: {hata}"
    eksik_tasima = deepcopy(tasima)
    ara = eksik_tasima["bolumler"][0]["durumlar"]["EREGL"]
    ara["pozisyon"], ara["sonuc"], ara["durum"] = None, None, "bos"
    ara.pop("butunluk")
    ara["butunluk"] = motor._iz_kodu(ara)
    assert eksik_tasima["durumlar"] == tasima["durumlar"]
    with pytest.raises(pilot.PilotHatasi, match="taşıma durumunu kaybetmiş"):
        pilot._mc_isinma_bolumleri_dogrula(
            [so],
            d,
            b,
            k | dict(yeniden_sinama=sakla(eksik_tasima)),
            donemler=donemler,
            kanit=kanit,
            yurutme_d=yurutme_d,
        )
    mumlar.loc[pd.Timestamp("2023-10-02"), "islem"] = True
    giren = motor.tara(
        mumlar.loc["2023-10-01":"2023-12-31"],
        {},
        parametre,
        kurulum=hesap["kurulum"],
        yurutme=ts._ileri_yurutme(yurutme_d, b["kosu_id"], "EREGL"),
        onceki_durum=bekleyen,
    )
    poz = giren["pozisyon"] or giren["islemler"][0]["pozisyon"]
    assert poz["giris_tarih"] == "2023-10-02"
    assert poz["risk_girdisi"]["sinyal_id"] == sinyal_id
    tasima["bolumler"][1]["durumlar"]["EREGL"] = giren
    tasima["durumlar"]["EREGL"] = giren
    hata = None
    try:
        pilot._mc_isinma_bolumleri_dogrula(
            [so],
            d,
            b,
            k | dict(yeniden_sinama=sakla(tasima)),
            donemler=donemler,
            kanit=kanit,
            yurutme_d=yurutme_d,
        )
    except pilot.PilotHatasi as exc:
        hata = str(exc)
    assert hata is None, f"Sonraki çeyrekte giren bekleyen sinyal reddedildi: {hata}"
    # Kapalı işlem listesi ve sıfırlanan güncel dolum listesi de kayıpsız geri kurulur.
    mumlar.loc[pd.Timestamp("2023-10-03"), ["dusuk", "ham_dusuk"]] = 90.0
    kapali = motor.tara(
        mumlar.loc["2023-10-01":"2023-12-31"],
        {},
        parametre,
        kurulum=hesap["kurulum"],
        yurutme=ts._ileri_yurutme(yurutme_d, b["kosu_id"], "EREGL"),
        onceki_durum=bekleyen,
    )
    assert len(kapali["islemler"]) == 1
    assert kapali["dolumlar"] == []
    for ara in (bekleyen, kapali, dusen):
        son = dusen if ara is dusen else kapali
        kisa = ts._mc_bolum_durumunu_sakla(ara, son)
        assert pilot.kanonik(pilot._mc_bolum_durumunu_ac(kisa, son)) == pilot.kanonik(
            ara
        )
    bozuk = deepcopy(kapali)
    bozuk["islemler"][0]["sonuc"]["net_sonuc"] += 1.0
    with pytest.raises(pilot.PilotHatasi, match="kanonik öneği"):
        ts._mc_bolum_durumunu_sakla(bozuk, kapali)
    bozuk = deepcopy(dusen)
    bozuk["retler"][0]["neden"] = "baska"
    with pytest.raises(pilot.PilotHatasi, match="kanonik öneği"):
        ts._mc_bolum_durumunu_sakla(bozuk, dusen)
    assert pilot.kanonik(tekrar["durumlar"]) == nihai_once
    (tmp_path / "mc-isinma-sahip-kaniti.json").write_text(
        json.dumps(
            dict(
                tur="kurulmus_sahip",
                uygun_tamamlanmis_wf_mc=False,
                bolum_sayisi=2,
                uye_sayilari=[30, 30],
                nihai_sembol_sayisi=len(tekrar["durumlar"]),
                kanit_bayt=len(pilot.kanonik(tekrar)),
                sikisik_kanit_bayt=len(pilot.kanonik(uretilen)),
                sikisik_bolum_kayitlari_bayt=len(pilot.kanonik(uretilen["bolumler"])),
                sikisik_bolum_durumlari_bayt=len(
                    pilot.kanonik([q["durumlar"] for q in uretilen["bolumler"]])
                ),
                yalniz_nihai_durum_bayt=len(pilot.kanonik(tekrar["durumlar"])),
                bolum_kayitlari_bayt=len(pilot.kanonik(bolumler)),
                bolum_durumlari_bayt=len(
                    pilot.kanonik([q["durumlar"] for q in bolumler])
                ),
                nihai_iz_satiri=sum(len(x["iz"]) for x in tekrar["durumlar"].values()),
                bolum_iz_satiri=sum(
                    len(x["iz"]) for q in bolumler for x in q["durumlar"].values()
                ),
                bolum_seanslari=[
                    len(
                        {
                            x["tarih"]
                            for x in q["durumlar"]["ASTOR"]["iz"]
                            if q["donem"]["baslangic"].isoformat()
                            <= x["tarih"]
                            <= q["donem"]["bitis"].isoformat()
                        }
                    )
                    for q in bolumler
                ],
            )
        ),
        encoding="utf-8",
    )


@pytest.mark.parametrize("deger", [None, 0, [], "metadata"])
def test_pilot_legacy_hucre_metaverisi_kayitta_korunur(tmp_path, deger):
    depo = pilot.PilotKayit(tmp_path / "yeni-legacy.jsonl")
    yontem = dict(yontem="legacy", tekrar=2, hucre_yontemi=deger)
    makbuz, hata = None, None
    try:
        makbuz = pilot_deneme(depo, yontem_ayarlari=yontem)
    except pilot.PilotHatasi as exc:
        hata = str(exc)
    assert makbuz is not None, f"Yeni seçim olmayan eski kayıt reddedildi: {hata}"
    once = depo.yol.read_bytes()
    kayitlar = pilot.PilotKayit(depo.yol).oku()
    assert len(kayitlar) == 1 and kayitlar[0]["yontem_ayarlari"] == yontem
    assert kayitlar[0]["ayar_parmak_izi"] == makbuz.ayar_ozeti
    assert depo.yol.read_bytes() == once


@pytest.mark.parametrize("deger", [None, 0, [], "metadata"])
def test_pilot_legacy_hucre_metaverisi_tarihsel_okumada_korunur(tmp_path, deger):
    tohum = pilot.PilotKayit(tmp_path / "tohum.jsonl")
    pilot_deneme(tohum)
    eski = tohum.oku()[0]
    eski["yontem_ayarlari"]["hucre_yontemi"] = deger
    # S07 eski kayıt biçimi: yalnız izinli metaveri ve onun tam ayar özeti değişir.
    ayarlar = {
        a: eski[a]
        for a in (
            "donemler",
            "veri_ayarlari",
            "yontem_ayarlari",
            "risk_ayarlari",
            "masraf_ayarlari",
        )
    }
    ayarlar["strateji"] = {
        k: v for k, v in eski["strateji"].items() if k != "olusturma_zamani"
    }
    eski["ayar_parmak_izi"] = pilot._ayar_ozeti(ayarlar)
    yol = tmp_path / "tarihsel-legacy.jsonl"
    once = pilot.kanonik(eski) + b"\n"
    yol.write_bytes(once)
    kayitlar, hata = None, None
    try:
        kayitlar = pilot.PilotKayit(yol).oku()
    except pilot.PilotHatasi as exc:
        hata = str(exc)
    assert kayitlar is not None, f"Geçerli eski günlük yeni okumada reddedildi: {hata}"
    assert kayitlar == [eski]
    assert yol.read_bytes() == once


@pytest.mark.parametrize(
    "yer,deger",
    [
        (yer, deger)
        for yer in ("dogrudan", "ic_ice")
        for deger in (None, 0, [], "bilinmeyen")
    ]
    + [("bozuk_hucre", deger) for deger in (None, 0, [], "metadata")]
    + [("golgelenen", "bilinmeyen")],
)
def test_pilot_secili_isinma_bozuk_politikayi_eski_metaveri_saymaz(
    tmp_path, yer, deger
):
    depo = pilot.PilotKayit(tmp_path / "secili.jsonl")
    pilot_deneme(depo)
    once = depo.yol.read_bytes()
    secim = dict(
        surum="ilk_islem_v1",
        tablo_ozeti=veri._YAYIMLANMIS_KAYNAK_OZETLERI["ilk_islem_v1"],
        kaynak="yerel",
        goruntu_id="ag-1",
        manifest_ozeti="a" * 64,
    )
    v = dict(
        kaynak="yerel",
        veri_referanslari=["ag-1"],
        manifest_ozeti="a" * 64,
        ilk_islem=secim,
    )
    y = dict(yontem="legacy", tekrar=2)
    if yer == "dogrudan":
        y["isinma_politikasi"] = deger
    elif yer == "ic_ice":
        y["hucre_yontemi"] = dict(isinma_politikasi=deger)
    elif yer == "bozuk_hucre":
        y["hucre_yontemi"] = deger
    else:
        y["hucre_yontemi"] = dict(isinma_politikasi="kaynakli_isinma_v1")
        y["isinma_politikasi"] = deger
    with pytest.raises(pilot.PilotHatasi, match="birlikte"):
        pilot_deneme(depo, veri_ayarlari=v, yontem_ayarlari=y)
    assert depo.yol.read_bytes() == once
    assert not any(o["kayit_turu"] == "baslangic" for o in depo.oku())


@pytest.mark.parametrize(
    "boz",
    [
        None,
        "kaynak",
        "kanit",
        "sil",
        "sil_yeniden_muhurle",
        "ayar_yeniden_muhurle",
        "sil_yapi",
    ],
)
def test_s10_hedef_yoklugu_native_kaynak_bagi_ve_eski_okuma(tmp_path, monkeypatch, boz):
    from tests.test_tansusinama import s10_hedef_yoklugu, s10_calistir

    depo, m = s10_hedef_yoklugu(tmp_path, monkeypatch)
    sonuc = s10_calistir(depo, m, tmp_path)
    olaylar = depo.oku()
    olay = next(
        o
        for o in olaylar
        if o.get("sonuc_turu") == "donem_v1" and o["donem"]["ad"] == "2021"
    )
    durum = olay["icerik"]["durumlar"]["TEST"]
    assert "hedef_yok_kaniti" in durum["pozisyon"]["risk_girdisi"]
    if boz is None:
        once = depo.yol.read_bytes()
        assert (
            pilot.PilotKayit(depo.yol).izle(sonuc["donemler"][4]["makbuz"].olay_id)[
                "sonuc"
            ]["icerik"]["durumlar"]["TEST"]
            == durum
        )
        assert depo.yol.read_bytes() == once
        return
    if boz == "kaynak":
        olay["icerik"]["adaylar"][0]["kayit_id"] = "baska-kaynak"
    elif boz == "kanit":
        durum["pozisyon"]["risk_girdisi"]["hedef_yok_kaniti"]["kaynak_sinyal_id"] = (
            "baska-kaynak"
        )
    elif boz == "sil_yapi":
        del durum["pozisyon"], durum["islemler"]
    else:
        pozisyon = durum["pozisyon"]
        risk = pozisyon["risk_girdisi"]
        if boz == "ayar_yeniden_muhurle":
            pozisyon["ayar"]["pencere"] += 1
            risk["hedef_yok_kaniti"]["parametreler"]["pencere"] += 1
            risk["ayar_parmak_izi"] = motor._iz_kodu(pozisyon["ayar"])
        else:
            del risk["hedef_yok_kaniti"]
        if boz != "sil":
            # Saldırı yalnız dış mührü değil, yeni kimlik ve girdi özetini de değiştirir.
            y = {
                a: v
                for a, v in risk.items()
                if a
                not in (
                    "sinyal_id",
                    "ayar_parmak_izi",
                    "islem_id",
                    "hedef_yok_kaniti",
                    "giris_fiyat",
                    "ilk_stop",
                )
            }
            kimlik = [
                y,
                risk["sinyal_id"],
                pozisyon["sinyal_tarih"],
                pozisyon["ayar"],
                pozisyon["kutu_alt"],
                pozisyon["hedef"],
            ]
            if "hedef_yok_kaniti" in risk:
                kimlik.append(risk["hedef_yok_kaniti"])
            risk["islem_id"] = motor._iz_kodu(kimlik)
            durum["son_girdi"] = motor._iz_kodu(["saldirganin_yeni_girdisi", kimlik])
    durum["butunluk"] = motor._iz_kodu(
        {a: v for a, v in durum.items() if a != "butunluk"}
    )
    depo.yol.write_bytes(b"".join(pilot.kanonik(o) + b"\n" for o in olaylar))
    with pytest.raises(pilot.PilotHatasi, match="Bozuk tam satır"):
        pilot.PilotKayit(depo.yol).oku()
