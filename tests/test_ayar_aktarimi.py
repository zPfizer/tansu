"""#88: üç eski aktarım sınırında hesap sonucu (TASARIM 5.14).

Sentetik seri: 40 gün 100, sonra 103, 104, 105, 106. ATR14 sinyalde
1 + 2,5/14 = 33/28. Giriş 104. ATR1,5 stopu 104 - 99/56 = 102,232142857;
ATR2 stopu 104 - 33/14 = 101,642857143. Ertesi düşük 102 yalnız ilkine değer.
Kutu altı 99,5; ona değmez. Sinyalden sonraki günler yeni sinyal üretmez.
"""

import json
import csv
import datetime as dt
from dataclasses import replace

import pandas as pd
import pytest

from tansu import __main__ as komut
from tansu import (
    aileler,
    deneme,
    gunluk,
    katalog,
    kayit,
    motor,
    rapor,
    simulator,
    tansusinama,
)
from tests.test_gunluk import kagit_aile
from tests.test_k1 import anlik_hazirla
from tests.test_kayit import pilot_deneme
from tests.test_simulator import P, mum


IZGARA = {"esik": [0.005], "min_gun": [3], "pencere": [3]}


def test_s11_cocuk_yalniz_dogrulanmis_ustten_tam_s10_yontemini_alir(
    tmp_path, monkeypatch
):
    from tansu.aktarim import AyarAktarimi
    from tests.test_tansusinama import s11_kayitli, s10_revizyon

    depo, ust, _ = s11_kayitli(tmp_path, monkeypatch)
    aktarim = AyarAktarimi(depo, ust.deneme_id)
    cocuk = aktarim.cocuk({"min_gun": 2})
    d = depo.deneme_oku(cocuk.deneme_id)
    assert d["yontem_ayarlari"] == {
        "yontem": "kayitli_donem_v1",
        "tekrar": 0,
        "yurutme_surumu": "bagimsiz_islem_v1",
        "fiyat_politikasi": "aof_v1",
        "muhasebe_politikasi": "tani_referans_v1",
    }
    assert d["ust_deneme_id"] == d["baglar"]["izgara_ust_deneme"] == ust.deneme_id
    assert d["ayar_parmak_izi"] == cocuk.kayit_makbuzu.ayar_ozeti
    assert (
        d["strateji"]["ayar_parmak_izi"] != aktarim.kayit["strateji"]["ayar_parmak_izi"]
    )
    for alan in ("donemler", "veri_ayarlari", "risk_ayarlari", "masraf_ayarlari"):
        assert d[alan] == aktarim.kayit[alan]
    once = depo.yol.read_bytes()
    with pytest.raises(deneme.PilotHatasi, match="dondurulmuş"):
        aktarim.cocuk({"min_gun": 9})
    assert depo.yol.read_bytes() == once
    yontem = aktarim.kayit["yontem_ayarlari"]
    yeni = s10_revizyon(
        depo,
        ust,
        yontem_ayarlari=yontem
        | dict(hucre_yontemi=yontem["hucre_yontemi"] | dict(keyfi=1)),
    )
    once = depo.yol.read_bytes()
    with pytest.raises(deneme.PilotHatasi, match="yürütme"):
        AyarAktarimi(depo, yeni.deneme_id).cocuk({"min_gun": 2})
    assert depo.yol.read_bytes() == once


def fiyatlar():
    kap = [100.0] * 40 + [103.0, 104.0, 105.0, 106.0]
    gunler = pd.bdate_range("2026-01-05", periods=len(kap))
    return [
        mum(g, k, k + 0.5, 102.0 if i == 42 else k - 0.5)
        for i, (g, k) in enumerate(zip(gunler, kap, strict=True))
    ]


@pytest.mark.parametrize(
    "stop,cikis,neden,risk",
    [("atr15", 102.232142857, "stop", 1.767857143), ("kutu", 106.0, "veri_sonu", 4.5)],
)
def test_izgara_hucre_ayari_ve_kurulumu_sonucu_degistirir(
    tmp_path, stop, cikis, neden, risk
):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    p = replace(P, stop=stop)
    m = motor.mumlar(anlik, "A", p)
    t = tansusinama.ema_tablolari(m, p, IZGARA, m.index[40])[0]
    assert len(t) == 1
    assert t.cikis_fiyat.tolist() == pytest.approx([cikis])
    assert t.neden.tolist() == [neden]
    assert t.planlanan_risk.tolist() == pytest.approx([risk])
    assert t.giris_fiyat.tolist() == [104.0]
    assert t.sinyal_tarih.tolist() == [m.index[40]]


def test_stratejiler_art_arda_soguk_kosu_ile_ayni_islemleri_verir(tmp_path):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    m = motor.mumlar(anlik, "A", P)
    birlikte = tansusinama.ema_tablolari(
        m, P, {**IZGARA, "stop": ["atr15", "atr2", "kutu"]}, m.index[40]
    )
    assert [t.cikis_fiyat.iloc[0] for t in birlikte] == pytest.approx(
        [102.232142857, 106.0, 106.0]
    )
    for stop, t in zip(("atr15", "atr2", "kutu"), birlikte, strict=True):
        ayri = tansusinama.ema_tablolari(
            m.copy(deep=True), replace(P, stop=stop), IZGARA, m.index[40]
        )[0]
        pd.testing.assert_frame_equal(t, ayri)


def test_tansu_komutu_secilen_ayarla_hesaplanan_sonucu_yazar(tmp_path, monkeypatch):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    # Küçük sentetik gösterge dönemleri; sinyal ve işlem hesabı gerçektir.
    monkeypatch.setitem(aileler.VARYANTLAR, "stop_atr15", replace(P, stop="atr15"))
    monkeypatch.setattr(tansusinama, "IZGARA", {simulator.AILE: IZGARA})
    assert (
        komut.main(
            [
                "tansu-sinama",
                "--kok",
                str(tmp_path),
                "--kimlik",
                anlik.kimlik,
                "--aile",
                simulator.AILE,
                "--isci",
                "1",
                "--varyant",
                "stop_atr15",
            ]
        )
        == 0
    )
    (yol,) = rapor.RAPOR_DIZINI.glob("tansu-sinama-*.json")
    sonuc = json.loads(yol.read_text(encoding="utf-8"))
    assert len(sonuc["aileler"][simulator.AILE]["hisseler"]) == 1
    (hisse,) = sonuc["aileler"][simulator.AILE]["hisseler"]
    # (5725/56) * 0,999 / (104 * 1,001) - 1 = -110549/5829824 -> -0,018963.
    assert hisse["net"] == pytest.approx([-0.018963], abs=1e-7)
    assert hisse["olcu"]["islem"] == 1


def test_gunluk_komutu_secilen_ayarla_stop_durumunu_yazar(tmp_path, monkeypatch):
    anlik = anlik_hazirla(tmp_path / "gunluk", {"A": fiyatlar()[:-1]})
    kagit_aile()
    monkeypatch.setitem(aileler.VARYANTLAR, "stop_atr15", replace(P, stop="atr15"))
    monkeypatch.setattr(gunluk, "_semboller", lambda *a: ["A"])
    # Yalnız veri indirme sınırı: saklı sentetik görüntü okunur, hesap değiştirilmez.
    monkeypatch.setattr(gunluk.veri, "indir", lambda *a, **k: anlik.kimlik)
    tarih = str(anlik.gunler[-1].date())
    assert (
        komut.main(
            [
                "gunluk",
                tarih,
                "--kok",
                str(tmp_path),
                "--varyant",
                "stop_atr15",
            ]
        )
        == 0
    )
    (satir,) = (
        (kayit.KAYIT_DIZINI / "kartlar.jsonl").read_text(encoding="utf-8").splitlines()
    )
    assert len(json.loads(satir)["kartlar"]) == 1
    (kart,) = json.loads(satir)["kartlar"]
    assert kart["durum"] == "STOP"
    assert kart["stop"] == "102,23"
    assert kart["referans"] == "103,00"


def kayitli(tmp_path, monkeypatch, stop="atr15"):
    # Katalog verisi sentetiktir; kayıt ve hesap yüzleri değiştirilmez.
    monkeypatch.setattr(katalog, "_TANIMLAR", {"bugun": replace(P, stop=stop)})
    depo = deneme.PilotKayit(tmp_path / "pilot.jsonl")
    makbuz = pilot_deneme(depo, veri_ayarlari={"veri_referanslari": ["20261005-1930"]})
    return depo, makbuz


def komutu_kos(argv, capsys):
    try:
        kod = komut.main(argv)
    except SystemExit as hata:
        kod = hata.code
    return kod, capsys.readouterr().err


@pytest.mark.parametrize("kayit_var", [False, True])
def test_git_hatasi_pilot_ve_sonuc_yazimindan_once_durur(
    tmp_path, monkeypatch, capsys, kayit_var
):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    monkeypatch.setitem(aileler.VARYANTLAR, "bugun", P)
    monkeypatch.setattr(tansusinama, "IZGARA", {simulator.AILE: IZGARA})
    argv = [
        "tansu-sinama",
        "--kok",
        str(tmp_path),
        "--kimlik",
        anlik.kimlik,
        "--aile",
        simulator.AILE,
        "--isci",
        "1",
    ]
    if kayit_var:
        depo, makbuz = kayitli(tmp_path, monkeypatch)
        yol = tmp_path / "girdi" / "pilot.jsonl"
        yol.parent.mkdir()
        yol.write_bytes(depo.yol.read_bytes())
        argv += ["--deneme-id", makbuz.deneme_id, "--deneme-dosyasi", str(yol)]

    def git_hatasi():
        raise kayit.KayitHatasi("Git bilgisi doğrulanamadı.")

    once = {
        y.relative_to(tmp_path): y.read_bytes()
        for y in tmp_path.rglob("*")
        if y.is_file()
    }
    monkeypatch.setattr(kayit, "_git", git_hatasi)
    kod = komut.main(argv)
    cikti = capsys.readouterr()
    assert kod == 1 and "Git" in cikti.err
    assert cikti.out == ""
    sonra = {
        y.relative_to(tmp_path): y.read_bytes()
        for y in tmp_path.rglob("*")
        if y.is_file()
    }
    assert sonra == once


def test_tam_cozulmus_kayit_tek_giristen_eklenir_ve_eskisi_degismez(tmp_path):
    depo = deneme.PilotKayit(tmp_path / "pilot.jsonl")
    ilk = pilot_deneme(depo)
    once = depo.yol.read_bytes()
    strateji = katalog.legacy_coz("stop_atr15")
    hata = None
    try:
        yeni = pilot_deneme(depo, strateji, ust_deneme=ilk.deneme_id)
    except ValueError as e:
        hata = str(e)
    assert hata is None, f"Tam çözülmüş kayıt reddedildi: {hata}"
    assert yeni.deneme_id != ilk.deneme_id
    assert yeni.ayar_ozeti != ilk.ayar_ozeti
    assert depo.yol.read_bytes().startswith(once)
    ayni = pilot_deneme(depo, strateji)
    assert ayni.ayar_ozeti == yeni.ayar_ozeti
    assert ayni.deneme_id != yeni.deneme_id  # Belge: açık kaydetme yeni revizyondur.


def test_kayitli_tansu_komutu_cocuk_ayarini_isleme_ve_sonuca_tasir(
    tmp_path, monkeypatch, capsys
):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    depo, m = kayitli(tmp_path, monkeypatch)
    monkeypatch.setattr(tansusinama, "IZGARA", {simulator.AILE: IZGARA})
    kod, hata = komutu_kos(
        [
            "tansu-sinama",
            "--kok",
            str(tmp_path),
            "--kimlik",
            anlik.kimlik,
            "--aile",
            simulator.AILE,
            "--isci",
            "1",
            "--deneme-id",
            m.deneme_id,
            "--deneme-dosyasi",
            str(depo.yol),
        ],
        capsys,
    )
    assert kod == 0, hata
    olaylar = depo.oku()
    cocuklar = [o for o in olaylar if o.get("ust_deneme_id") == m.deneme_id]
    assert len(cocuklar) == 1
    cocuk = cocuklar[0]
    assert cocuk["strateji"]["parametreler"][1]["koken"] == "legacy_izgara"
    baglar = [o for o in olaylar if o["kayit_turu"] == "ayar_bagi"]
    assert {o["asama"] for o in baglar} == {"sinyal", "islem", "sonuc"}
    assert {o["deneme_id"] for o in baglar} == {cocuk["deneme_id"]}
    assert all(
        {"tur", "konum", "tarih", "alinti", "karar_durumu"} <= set(k)
        for o in baglar
        for k in o["kaynaklar"]
    )
    assert {o["ayar_parmak_izi"] for o in baglar} == {cocuk["ayar_parmak_izi"]}
    (islem,) = [o for o in baglar if o["asama"] == "islem"]
    assert islem["icerik"]["cikis_fiyat"] == pytest.approx(102.232142857)
    (sonuc,) = [o for o in baglar if o["asama"] == "sonuc"]
    assert sonuc["icerik"]["net"] == pytest.approx(-0.018963, abs=1e-7)
    assert sonuc["referanslar"] == [islem["kayit_id"]]


def test_kayitli_gunluk_komutu_kayit_ayarindan_stop_durumu_uretir(
    tmp_path, monkeypatch, capsys
):
    anlik = anlik_hazirla(tmp_path / "gunluk", {"A": fiyatlar()[:-1]})
    depo, m = kayitli(tmp_path, monkeypatch)
    kagit_aile()
    monkeypatch.setattr(gunluk, "_semboller", lambda *a: ["A"])
    monkeypatch.setattr(gunluk.veri, "indir", lambda *a, **k: anlik.kimlik)
    kod, hata = komutu_kos(
        [
            "gunluk",
            str(anlik.gunler[-1].date()),
            "--kok",
            str(tmp_path),
            "--deneme-id",
            m.deneme_id,
            "--deneme-dosyasi",
            str(depo.yol),
        ],
        capsys,
    )
    assert kod == 0, hata
    # TASARIM S07: önizleme normal kart günlüğüne yazılmaz; aynı kart CSV'de kalır.
    (csv_yol,) = (rapor.RAPOR_DIZINI / "onizleme").glob("*/kartlar-*.csv")
    with csv_yol.open(encoding="utf-8-sig", newline="") as f:
        (kart,) = list(csv.DictReader(f, delimiter=";"))
    assert not (kayit.KAYIT_DIZINI / "kartlar.jsonl").exists()
    assert kart["durum"] == "STOP"
    assert kart["stop"] == "102,23"
    assert "önizleme" in kart["kanit"]
    assert "148 işlem" not in kart["kanit"]
    baglar = [o for o in depo.oku() if o["kayit_turu"] == "ayar_bagi"]
    assert {o["deneme_id"] for o in baglar} == {m.deneme_id}
    assert {o["ayar_parmak_izi"] for o in baglar} == {m.ayar_ozeti}
    assert {o["asama"] for o in baglar} == {"sinyal", "islem", "sonuc"}


def test_sayisal_ayar_degisiminden_sonra_onceki_deneme_ve_sonuclar_degismez(
    tmp_path, monkeypatch, capsys
):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    depo, m = kayitli(tmp_path, monkeypatch)
    argv = [
        "tansu-sinama",
        "--kok",
        str(tmp_path),
        "--kimlik",
        anlik.kimlik,
        "--aile",
        simulator.AILE,
        "--isci",
        "1",
        "--deneme-id",
        m.deneme_id,
        "--deneme-dosyasi",
        str(depo.yol),
    ]
    monkeypatch.setattr(tansusinama, "IZGARA", {simulator.AILE: IZGARA})
    assert komutu_kos(argv, capsys)[0] == 0
    once = depo.yol.read_bytes()
    onceki_sonuclar = [o for o in depo.oku() if o.get("asama") == "sonuc"]
    assert len(onceki_sonuclar) == 1
    monkeypatch.setattr(
        tansusinama, "IZGARA", {simulator.AILE: {**IZGARA, "min_gun": [5]}}
    )
    assert komutu_kos(argv, capsys)[0] == 0
    assert depo.yol.read_bytes().startswith(once)
    cocuklar = [o for o in depo.oku() if o.get("ust_deneme_id") == m.deneme_id]
    assert len(cocuklar) == 2
    assert cocuklar[0]["deneme_id"] != cocuklar[1]["deneme_id"]
    assert cocuklar[0]["ayar_parmak_izi"] != cocuklar[1]["ayar_parmak_izi"]
    assert [o for o in depo.oku() if o.get("asama") == "sonuc"][:1] == onceki_sonuclar


def test_kayitli_gunluk_eski_gunluk_basarisini_ayar_kaniti_saymaz(
    tmp_path, monkeypatch, capsys
):
    anlik = anlik_hazirla(tmp_path / "gunluk", {"A": fiyatlar()[:-1]})
    depo, m = kayitli(tmp_path, monkeypatch)
    kagit_aile()
    monkeypatch.setitem(aileler.VARYANTLAR, "bugun", P)
    monkeypatch.setattr(gunluk, "_semboller", lambda *a: ["A"])
    monkeypatch.setattr(gunluk.veri, "indir", lambda *a, **k: anlik.kimlik)
    argv = ["gunluk", str(anlik.gunler[-1].date()), "--kok", str(tmp_path)]
    assert komutu_kos(argv, capsys)[0] == 0
    gunluk_yol = kayit.KAYIT_DIZINI / "kartlar.jsonl"
    once = gunluk_yol.read_bytes()
    assert json.loads(once)["kartlar"][0]["durum"] == "AKTİF"
    durum_yolu = rapor.RAPOR_DIZINI / "durum.txt"
    satirlar = durum_yolu.read_text(encoding="utf-8").splitlines()
    satirlar[1] = f"Son başarılı koşu: {anlik.gunler[-1].date()} 19:30"
    durum_yolu.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    assert (
        komutu_kos(
            argv + ["--deneme-id", m.deneme_id, "--deneme-dosyasi", str(depo.yol)],
            capsys,
        )[0]
        == 0
    )
    sonuclar = [o for o in depo.oku() if o.get("asama") == "sonuc"]
    assert len(sonuclar) == 1, (
        "Eski günlük başarı kayıtlı ayar hesabının yerine kullanıldı"
    )
    assert sonuclar[0]["icerik"]["kartlar"][0][3] == "STOP"
    assert gunluk_yol.read_bytes() == once


def test_kayitli_izgara_iki_iscide_tam_baglari_yazar(tmp_path, capsys):
    gunler = pd.bdate_range("2021-01-04", periods=514)
    kap = [100.0] * 510 + [110.0, 112.0, 114.0, 115.0]
    seri = [mum(g, k, k + 0.5, k - 0.5) for g, k in zip(gunler, kap, strict=True)]
    anlik = anlik_hazirla(tmp_path, {"A": seri, "B": seri})
    depo = deneme.PilotKayit(tmp_path / "pilot.jsonl")
    m = pilot_deneme(depo, veri_ayarlari={"veri_referanslari": [anlik.kimlik]})
    # Tek hücreyi E4'ün gerçek süreç havuzunda çalıştır; çocuk süreçler gerçek kataloğu okur.
    from tansu.aktarim import AyarAktarimi

    sonuc = tansusinama.calistir(
        anlik,
        {},
        (simulator.AILE,),
        isci=2,
        ilerleme=lambda *a: None,
        izgara={simulator.AILE: {"esik": [0.012], "min_gun": [3], "pencere": [10]}},
        aktarim=AyarAktarimi(depo, m.deneme_id),
    )
    assert sonuc["aileler"][simulator.AILE]["ozet"]["toplam"] == 2
    baglar = [o for o in depo.oku() if o["kayit_turu"] == "ayar_bagi"]
    assert len([o for o in baglar if o["asama"] == "islem"]) == 2
    sonuclar = [o for o in baglar if o["asama"] == "sonuc"]
    assert len(sonuclar) == 2
    assert {o["icerik"]["hisse"] for o in sonuclar} == {"A", "B"}
    assert {o["kosu_id"] for o in baglar} == {sonuc["kosu_id"]}


@pytest.mark.parametrize("bozuk", ["eksik", "ozet", "yok"])
def test_gecersiz_deneme_hesabi_baslatmadan_kimligiyle_durur(
    tmp_path, monkeypatch, capsys, bozuk
):
    depo, m = kayitli(tmp_path, monkeypatch)
    kimlik = m.deneme_id
    olay = depo.oku()[0]
    if bozuk == "eksik":
        olay["strateji"]["parametreler"] = olay["strateji"]["parametreler"][:-1]
    elif bozuk == "ozet":
        olay["ayar_parmak_izi"] = "yanlis"
    else:
        kimlik = "olmayan-deneme"
    depo.yol.write_bytes(deneme.kanonik(olay) + b"\n")
    # Görüntü yok: kayıt denetimi daha önce yapılmazsa yanlış aşamada durur.
    kod, hata = komutu_kos(
        [
            "tansu-sinama",
            "--kok",
            str(tmp_path),
            "--deneme-id",
            kimlik,
            "--deneme-dosyasi",
            str(depo.yol),
        ],
        capsys,
    )
    assert kod == 1
    assert kimlik in hata
    assert not list(rapor.RAPOR_DIZINI.glob("tansu-sinama-*.json"))


def test_kayitsiz_komut_eski_sonucu_korur_ve_bagini_isaretler(tmp_path, monkeypatch):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    monkeypatch.setitem(aileler.VARYANTLAR, "bugun", P)
    monkeypatch.setattr(tansusinama, "IZGARA", {simulator.AILE: IZGARA})
    assert (
        komut.main(
            [
                "tansu-sinama",
                "--kok",
                str(tmp_path),
                "--kimlik",
                anlik.kimlik,
                "--aile",
                simulator.AILE,
                "--isci",
                "1",
            ]
        )
        == 0
    )
    yol = rapor.RAPOR_DIZINI / "ayar-baglari.jsonl"
    assert yol.exists(), "Kayıtsız koşunun ayrı bağlantı kaydı yok"
    baglar = deneme.PilotKayit(yol).oku()
    assert all(
        o["deneme_id"] is None and o["kayit_durumu"] == "kayitsiz" for o in baglar
    )
    assert not any(o["kayit_turu"] == "deneme" for o in baglar)


@pytest.mark.parametrize("bozuk", ["kurulum_yok", "kutu_eksik", "ayar_degisti"])
def test_yeni_yol_eksik_kurulumu_ve_degisen_ayari_dolumdan_once_durdurur(
    tmp_path, monkeypatch, capsys, bozuk
):
    from tansu import aktarim

    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    depo, m = kayitli(tmp_path, monkeypatch, stop="kutu")
    monkeypatch.setattr(tansusinama, "IZGARA", {simulator.AILE: IZGARA})
    kurulum = aileler.kurulum
    ema = aktarim.AyarAktarimi.ema
    if bozuk == "kurulum_yok":
        monkeypatch.setattr(aileler, "kurulum", lambda *a: None)
    elif bozuk == "kutu_eksik":
        monkeypatch.setattr(
            aileler, "kurulum", lambda *a: kurulum(*a).assign(kutu_alt=float("nan"))
        )
    else:

        def degisen(self, *args):
            self.p = replace(self.p, stop="atr2")
            return ema(self, *args)

        monkeypatch.setattr(aktarim.AyarAktarimi, "ema", degisen)
    beklenmeyen = None
    try:
        kod, hata = komutu_kos(
            [
                "tansu-sinama",
                "--kok",
                str(tmp_path),
                "--kimlik",
                anlik.kimlik,
                "--aile",
                simulator.AILE,
                "--isci",
                "1",
                "--deneme-id",
                m.deneme_id,
                "--deneme-dosyasi",
                str(depo.yol),
            ],
            capsys,
        )
    except AttributeError as e:
        beklenmeyen = e
    assert beklenmeyen is None, f"Kayıt kimliği olmayan hata: {beklenmeyen}"
    assert kod == 1
    cocuk = next(o for o in depo.oku() if o.get("ust_deneme_id") == m.deneme_id)
    assert cocuk["deneme_id"] in hata
    assert not any(o.get("asama") in ("islem", "sonuc") for o in depo.oku())
    assert not list(rapor.RAPOR_DIZINI.glob("tansu-sinama-*.json"))


@pytest.mark.parametrize("asama", ["sinyal", "islem"])
def test_gercek_aktarim_sinirinda_ozet_farki_sonucu_durdurur(
    tmp_path, monkeypatch, capsys, asama
):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    depo, m = kayitli(tmp_path, monkeypatch)
    monkeypatch.setattr(tansusinama, "IZGARA", {simulator.AILE: IZGARA})
    yaz = deneme.PilotKayit.bag_kaydet
    bozulan = []

    def degisen(self, **kw):
        makbuz = yaz(self, **kw)
        if kw["asama"] == asama:
            olaylar = self.oku()
            olaylar[-1]["ayar_parmak_izi"] = "baska-ayar"
            self.yol.write_bytes(b"".join(deneme.kanonik(o) + b"\n" for o in olaylar))
            bozulan.append(makbuz.olay_id)
        return makbuz

    monkeypatch.setattr(deneme.PilotKayit, "bag_kaydet", degisen)
    kod, hata = komutu_kos(
        [
            "tansu-sinama",
            "--kok",
            str(tmp_path),
            "--kimlik",
            anlik.kimlik,
            "--aile",
            simulator.AILE,
            "--isci",
            "1",
            "--deneme-id",
            m.deneme_id,
            "--deneme-dosyasi",
            str(depo.yol),
        ],
        capsys,
    )
    assert kod == 1
    assert bozulan and bozulan[0] in hata
    assert not any(o.get("asama") == "sonuc" for o in depo.oku())
    if asama == "sinyal":
        assert not any(o.get("asama") == "islem" for o in depo.oku())
    assert not list(rapor.RAPOR_DIZINI.glob("tansu-sinama-*.json"))


@pytest.mark.parametrize(
    "once_normal,bozuk", [(False, False), (True, False), (True, True)]
)
def test_kayitli_onizleme_normal_gunlugun_durumunu_ve_hesabini_degistirmez(
    tmp_path, monkeypatch, once_normal, bozuk
):
    from tansu.aktarim import AyarAktarimi

    anlik = anlik_hazirla(tmp_path / "gunluk", {"A": fiyatlar()[:-1]})
    depo, m = kayitli(tmp_path, monkeypatch)
    kagit_aile()
    monkeypatch.setattr(gunluk, "_semboller", lambda *a: ["A"])
    monkeypatch.setattr(gunluk.veri, "indir", lambda *a, **k: anlik.kimlik)
    tarih = anlik.gunler[-1].date()
    simdi = dt.datetime.combine(tarih, dt.time(19, 30))
    csv_yol = rapor.RAPOR_DIZINI / f"kartlar-{tarih:%Y%m%d}.csv"
    yollar = [
        csv_yol,
        rapor.RAPOR_DIZINI / "durum.txt",
        kayit.KAYIT_DIZINI / "kartlar.jsonl",
    ]
    if once_normal:
        assert gunluk.gunluk(tarih, tmp_path, simdi=simdi, p=P) == 0
    once = {y: y.read_bytes() if y.exists() else None for y in yollar}
    aktarim = AyarAktarimi(depo, m.deneme_id)
    p = replace(aktarim.p, stop="kutu") if bozuk else aktarim.p
    assert gunluk.gunluk(tarih, tmp_path, simdi=simdi, p=p, aktarim=aktarim) == int(
        bozuk
    )
    sonra = {y: y.read_bytes() if y.exists() else None for y in yollar}
    assert sonra == once, (
        "Önizleme normal günlük durumunu/CSV'sini/kart günlüğünü değiştirdi"
    )
    assert gunluk.gunluk(tarih, tmp_path, simdi=simdi, p=P) == 0
    with csv_yol.open(encoding="utf-8-sig", newline="") as f:
        (kart,) = list(csv.DictReader(f, delimiter=";"))
    assert (kart["durum"], kart["stop"]) == ("AKTİF", "101,64")
    gunluk_kaydi = yollar[-1].read_text(encoding="utf-8")
    assert m.deneme_id not in gunluk_kaydi
    assert json.loads(gunluk_kaydi)["kartlar"][0]["durum"] == "AKTİF"


@pytest.mark.parametrize("komut_adi", ["tansu-sinama", "gunluk"])
@pytest.mark.parametrize(
    "strateji",
    [
        None,
        [],
        "bugun",
        {"parametreler": [None]},
        {"parametreler": ["bozuk"]},
        {"parametreler": "bozuk"},
        {"parametreler": [{"ad": [], "deger": 3, "koken": "legacy_izgara"}]},
    ],
)
def test_bozuk_ayar_yapisi_komutta_kayit_kimligiyle_gorunur_hata_verir(
    tmp_path, capsys, komut_adi, strateji
):
    kimlik = "bozuk-ayar-kaydi"
    depo = deneme.PilotKayit(tmp_path / "bozuk.jsonl")
    depo.yol.write_bytes(
        deneme.kanonik(
            {
                "sema_surumu": deneme.SURUM,
                "kayit_turu": "deneme",
                "deneme_id": kimlik,
                "strateji": strateji,
            }
        )
        + b"\n"
    )
    argv = [komut_adi] + (["2026-10-05"] if komut_adi == "gunluk" else [])
    argv += ["--deneme-id", kimlik, "--deneme-dosyasi", str(depo.yol)]
    beklenmeyen = None
    try:
        kod, hata = komutu_kos(argv, capsys)
    except (AttributeError, KeyError, TypeError, ValueError) as e:
        beklenmeyen = f"{type(e).__name__}: {e}"
    assert beklenmeyen is None, f"Kayıt kimliği olmayan hata kaçtı: {beklenmeyen}"
    assert kod == 1
    assert kimlik in hata
    assert not list(rapor.RAPOR_DIZINI.glob("tansu-sinama-*.json"))
    assert not (rapor.RAPOR_DIZINI / "durum.txt").exists()


@pytest.mark.parametrize(
    "alan,deger",
    [
        ("veri_ayarlari", None),
        ("veri_ayarlari", {"veri_referanslari": None}),
        ("veri_ayarlari", {"veri_referanslari": "20261005-1930"}),
        ("yontem_ayarlari", []),
        ("yontem_ayarlari", {"tekrar": "bozuk"}),
        ("risk_ayarlari", None),
        ("risk_ayarlari", {"risk": 0.1}),
        ("masraf_ayarlari", []),
        ("masraf_ayarlari", {"masraf": 0.1}),
        ("donemler", []),
        ("eski_referans", {"kural_id": None, "bos_nedenleri": None}),
    ],
)
def test_ozeti_tutan_bozuk_ayar_yapisi_kimligiyle_reddedilir(tmp_path, alan, deger):
    from hashlib import sha256

    depo = deneme.PilotKayit(tmp_path / "pilot.jsonl")
    m = pilot_deneme(depo)
    olay = depo.oku()[0]
    olay[alan] = deger
    ayarlar = {
        a: olay[a]
        for a in (
            "donemler",
            "veri_ayarlari",
            "yontem_ayarlari",
            "risk_ayarlari",
            "masraf_ayarlari",
        )
    }
    ayarlar["strateji"] = {
        k: v for k, v in olay["strateji"].items() if k != "olusturma_zamani"
    }
    olay["ayar_parmak_izi"] = (
        f"{deneme.SURUM}:sha256:{sha256(deneme.kanonik(ayarlar)).hexdigest()}"
    )
    depo.yol.write_bytes(deneme.kanonik(olay) + b"\n")
    hata = None
    try:
        depo.deneme_oku(m.deneme_id)
    except deneme.PilotHatasi as e:
        hata = str(e)
    assert hata is not None, f"Bozuk {alan} özeti tuttuğu için kabul edildi"
    assert m.deneme_id in hata


def test_gecersiz_kayitli_hucre_komutta_ust_deneme_kimligiyle_durur(
    tmp_path, monkeypatch, capsys
):
    anlik = anlik_hazirla(tmp_path, {"A": fiyatlar()})
    depo, m = kayitli(tmp_path, monkeypatch)
    once = depo.yol.read_bytes()
    monkeypatch.setattr(
        tansusinama, "IZGARA", {simulator.AILE: {**IZGARA, "min_gun": ["bozuk"]}}
    )
    beklenmeyen = None
    try:
        kod, hata = komutu_kos(
            [
                "tansu-sinama",
                "--kok",
                str(tmp_path),
                "--kimlik",
                anlik.kimlik,
                "--aile",
                simulator.AILE,
                "--isci",
                "1",
                "--deneme-id",
                m.deneme_id,
                "--deneme-dosyasi",
                str(depo.yol),
            ],
            capsys,
        )
    except ValueError as e:
        beklenmeyen = f"{type(e).__name__}: {e}"
    assert beklenmeyen is None, (
        f"Kayıt kimliği olmayan hücre hatası kaçtı: {beklenmeyen}"
    )
    assert kod == 1
    assert m.deneme_id in hata
    assert depo.yol.read_bytes() == once
    assert not list(rapor.RAPOR_DIZINI.glob("tansu-sinama-*.json"))


@pytest.mark.parametrize("aileler", [("cift_rotasyonu",), tansusinama.AILELER])
def test_kayitli_ema_deneme_cift_hesabini_baslatmadan_reddedilir(tmp_path, aileler):
    from tansu.aktarim import AyarAktarimi
    from tests.test_tansusinama import cift_anlik, IZGARA as TUM_IZGARA

    anlik = cift_anlik(tmp_path / "cift")
    depo = deneme.PilotKayit(tmp_path / "pilot.jsonl")
    makbuz = pilot_deneme(
        depo, "stop_atr15", veri_ayarlari={"veri_referanslari": [anlik.kimlik]}
    )
    once = depo.yol.read_bytes()
    hata = None
    try:
        tansusinama.calistir(
            anlik,
            {"A": "X", "B": "X", "C": "X"},
            aileler=aileler,
            isci=1,
            bas="2015-12-01",
            ilerleme=lambda *a: None,
            izgara=TUM_IZGARA,
            aktarim=AyarAktarimi(depo, makbuz.deneme_id),
        )
    except deneme.PilotHatasi as e:
        hata = str(e)
    assert hata is not None, "EMA denemesiyle bağsız çift hesabı kabul edildi"
    assert makbuz.deneme_id in hata
    assert "cift_rotasyonu" in hata
    assert depo.yol.read_bytes() == once


def test_s11_cocuk_ozeti_uyusmazsa_kayit_makbuzu_korunur(tmp_path, monkeypatch):
    from copy import deepcopy
    from tansu import deneme
    from tansu.aktarim import AyarAktarimi
    from tests.test_tansusinama import s11_kayitli

    depo, ust, _ = s11_kayitli(tmp_path, monkeypatch)
    aktarim = AyarAktarimi(depo, ust.deneme_id)
    oku = depo.deneme_oku

    def degisen_okuma(deneme_id):
        kayit = oku(deneme_id)
        if kayit["ust_deneme_id"] == ust.deneme_id:
            kayit = deepcopy(kayit)
            kayit["ayar_parmak_izi"] = "farkli-tam-ozet"
        return kayit

    monkeypatch.setattr(depo, "deneme_oku", degisen_okuma)
    with pytest.raises(deneme.PilotHatasi, match="makbuzu tam ayarla") as hata:
        aktarim.cocuk({"min_gun": 3})
    makbuz = getattr(hata.value, "kayit_makbuzu", None)
    assert makbuz is not None, (
        "Doğrulama hatası daha önce alınan kayıt makbuzunu kaybetmemeli"
    )
    kayit = deneme.PilotKayit(depo.yol).deneme_oku(makbuz.deneme_id)
    assert kayit["ayar_parmak_izi"] == makbuz.ayar_ozeti
    assert kayit["ust_deneme_id"] == ust.deneme_id
