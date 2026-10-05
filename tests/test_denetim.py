"""Boru hattı denetimi (TASARIM 5.12, B-18): sentetik boş dünya, gömülü etki, yanlış kabul ve güç oranları."""

import json

import numpy as np
import pandas as pd
import pytest

from tansu import aileler, ciftbolme, denetim, evren, kayit, simulator


def test_dunya_ayni_tohum_ayni_veri_ve_farkli_tohum_farkli_veri():
    a, b, c = (denetim.dunya(t, hisse=8, gun=300) for t in (1, 1, 2))
    pd.testing.assert_frame_equal(a.fiyat, b.fiyat)
    assert not a.fiyat["kapanis"].equals(c.fiyat["kapanis"])


def test_dunya_veri_kapilarindan_temiz_gecer_ve_evren_en_alttaki_yuzde_yirmiyi_eler():
    # 40 hisse: likidite eleği ⌊40 · 0,2⌋ = 8 hisse eler, evren 32 hisse (TASARIM 5.2); karantina, kilit, olay uyarısı yok.
    a = denetim.dunya(3, hisse=40, gun=400)
    assert a.sorunlar == [] and not a.gun_tablosu["karantina"].any()
    assert not a.gun_tablosu["kilit_tavan"].any() and not a.gun_tablosu["kilit_taban"].any()
    assert len(evren.evren(a, pd.Timestamp("2013-03-01"))) == 32


def test_dunya_fiyat_iliskileri_ve_getiri_siniri():
    a = denetim.dunya(4, hisse=6, gun=500)
    f = a.fiyat
    assert ((f["dusuk"] <= f["aof"]) & (f["aof"] <= f["yuksek"]) & (f["dusuk"] <= f["kapanis"])
            & (f["kapanis"] <= f["yuksek"])).all()
    r = f.sort_values(["sembol", "tarih"]).groupby("sembol")["kapanis"].apply(lambda s: np.log(s).diff().dropna())
    assert r.abs().max() <= 0.07 + 1e-12
    assert len(a.gunler) == 500 and a.faiz_gunluk(a.gunler[0], a.gunler[-1]).notna().all()


def test_etki_kaydir_sinyalden_sonraki_2_ile_6_gunlere_yayilir_ve_ust_uste_biner():
    # Tek sinyal j=2, etki 0,05 (günde 0,01): kayma günler 4..8'de 0,01 artar, sonra sabit.
    np.testing.assert_allclose(denetim.etki_kaydir(10, [2], 0.05), [0, 0, 0, 0, .01, .02, .03, .04, .05, .05])
    # İki sinyal j=2 ve j=3: ek = [0,0,0,0,.01,.02,.02,.02,.02,.01]; kümülatif toplam.
    np.testing.assert_allclose(denetim.etki_kaydir(10, [2, 3], 0.05), [0, 0, 0, 0, .01, .03, .05, .07, .09, .10])
    assert not denetim.etki_kaydir(10, [], 0.05).any()


@pytest.mark.parametrize("aile", [simulator.AILE, ciftbolme.AILE])
def test_etki_ekle_giris_gunune_dokunmaz_fiyat_iliskilerini_korur_ve_fiyati_yukari_iter(aile):
    # EMA: 40 hisse boş dünyada sinyal var; çift: yıllık seçilen çiftin geçiş sinyali var. İlk değişen gün, sinyalden en erken
    # 2 gün sonradır; fiyat oranı (etkili / etkisiz) hiçbir yerde 1'in altına düşmez (yalnız pozitif etki).
    a = denetim.dunya(7, hisse=24, gun=1100)
    b = denetim.etki_ekle(a, aile, 0.05)
    f0, f1 = a.fiyat.set_index(["sembol", "tarih"]), b.fiyat.set_index(["sembol", "tarih"])
    oran = (f1["kapanis"] / f0["kapanis"]).unstack(0)
    assert (oran >= 1 - 1e-12).all().all() and (oran > 1 + 1e-12).any().any()
    ilk = oran.apply(lambda s: s.index[(s > 1 + 1e-12).to_numpy()][0] if (s > 1 + 1e-12).any() else pd.NaT)
    assert (ilk.dropna() >= a.gunler[2]).all()
    f = b.fiyat
    assert ((f["dusuk"] <= f["aof"]) & (f["aof"] <= f["yuksek"]) & (f["dusuk"] <= f["kapanis"]) & (f["kapanis"] <= f["yuksek"])).all()
    assert (f["ham_kapanis"] == f["kapanis"]).all()


def test_etki_ekle_ema_tek_sinyalli_hissede_oran_elle_hesapla(tmp_path):
    # Hissenin ilk (ve yalnız bu sinyalden etkilenen) günlerinde oran: j sinyal günü → j+2…j+6'da exp(0,01·k), sonra exp(0,05).
    a = denetim.dunya(7, hisse=24, gun=1100)
    konum = pd.Series(np.arange(len(a.gunler)), index=a.gunler)
    b = denetim.etki_ekle(a, simulator.AILE, 0.05)
    bulundu = 0
    for s, f in a.fiyat.groupby("sembol"):
        sig = aileler.sinyal(f.set_index("tarih")[["kapanis", "yuksek"]])
        if len(sig) != 1:
            continue
        j = konum[sig[0]]
        if j + 7 >= len(a.gunler):
            continue
        r = (b.fiyat[b.fiyat["sembol"] == s].set_index("tarih")["kapanis"] / f.set_index("tarih")["kapanis"]).to_numpy()
        beklenen = np.exp(np.minimum(np.maximum(np.arange(len(r)) - (j + 1), 0), 5) * 0.01)
        np.testing.assert_allclose(r, beklenen)
        bulundu += 1
    assert bulundu >= 1


def kucuk(**kw):
    return dict(n=1, n_etki=1, tekrar=3, isci=1, hisse=8, gun=700, **kw)


def test_calistir_yapi_oranlar_ve_gecti_bayragi():
    s = denetim.calistir(**kucuk())
    assert (s["n"], s["n_etki"], s["tekrar"], s["esik"]) == (1, 1, 3, 0.05)
    for aile in (simulator.AILE, ciftbolme.AILE):
        for bolum in ("yanlis_kabul", "guc"):
            for a in ("olcut_1_4", "kagit"):
                d = s[bolum][aile][a]
                assert d["n"] == 1 and d["adet"] in (0, 1) and d["oran"] == d["adet"]
        assert s["yanlis_kabul"][aile]["kagit"]["adet"] <= s["yanlis_kabul"][aile]["olcut_1_4"]["adet"]  # Kâğıt alt küme
    assert s["gecti"] == all(s["yanlis_kabul"][a]["olcut_1_4"]["oran"] <= 0.05 for a in s["yanlis_kabul"])


def test_tekil_ayni_tohum_ayni_sonuc():
    ayni = lambda: denetim.tekil(5, simulator.AILE, 0.05, 3, 8, 700)  # noqa: E731
    assert ayni() == ayni()


def sonuc_ornek(gecti):
    d = lambda adet, n: {"n": n, "adet": adet, "oran": adet / n}  # noqa: E731
    yk = {a: {"olcut_1_4": d(1 if not gecti else 0, 20), "kagit": d(0, 20)} for a in (simulator.AILE, ciftbolme.AILE)}
    return {"n": 20, "n_etki": 4, "tekrar": 200, "etki": 0.05, "hisse": 40, "gun": 2000, "yanlis_kabul": yk,
            "guc": {a: {"olcut_1_4": d(3, 4), "kagit": d(1, 4)} for a in yk}, "esik": 0.05, "gecti": gecti}


def test_yaz_docs_ve_rapor_dosyalarini_yazar_yuzdeler_elle():
    # 1/20 = %5,00; 0/20 = %0,00; güç 3/4 = %75,00 ve 1/4 = %25,00.
    md, html = denetim.yaz(sonuc_ornek(False))
    metin = md.read_text(encoding="utf-8")
    assert "KALDI: ilk resmi koşu yapılmaz" in metin and "%5,00 (1/20)" in metin and "%75,00 (3/4)" in metin
    assert "%25,00 (1/4)" in metin and "EMA sıkışması" in metin and "Çift rotasyonu" in metin
    assert "GEÇTİ" in denetim.yaz(sonuc_ornek(True))[0].read_text(encoding="utf-8")
    assert "Boru hattı denetimi" in html.read_text(encoding="utf-8")


def test_denetim_komutu_sonucu_gunluge_destek_olarak_yazar_ve_ilk_resmi_kosu_kapisini_acar(monkeypatch, capsys):
    from tansu.__main__ import main
    monkeypatch.setattr(denetim, "calistir", lambda **kw: sonuc_ornek(True))
    kayit.kayitla()
    assert main(["denetim"]) == 0
    satir = [json.loads(s) for s in (kayit.KAYIT_DIZINI / "deneme.jsonl").read_text(encoding="utf-8").splitlines()][-1]
    assert (satir["tur"], satir["olay"], satir["gecti"]) == ("destek", "denetim", True)
    assert kayit.denetim_gecti(satir["kod_hash"]) and kayit.deneme_sayisi() == 0  # Holm m'ye girmez
    monkeypatch.setattr(denetim, "calistir", lambda **kw: sonuc_ornek(False))
    assert main(["denetim"]) == 1
    assert not kayit.denetim_gecti(satir["kod_hash"])  # son denetim kaldı
    assert "ilk resmi koşu yapılmaz" in capsys.readouterr().err
