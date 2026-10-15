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
    assert (
        not a.gun_tablosu["kilit_tavan"].any()
        and not a.gun_tablosu["kilit_taban"].any()
    )
    assert len(evren.evren(a, pd.Timestamp("2013-03-01"))) == 32


def test_dunya_fiyat_iliskileri_ve_getiri_siniri():
    a = denetim.dunya(4, hisse=6, gun=500)
    f = a.fiyat
    assert (
        (f["dusuk"] <= f["aof"])
        & (f["aof"] <= f["yuksek"])
        & (f["dusuk"] <= f["kapanis"])
        & (f["kapanis"] <= f["yuksek"])
    ).all()
    r = (
        f.sort_values(["sembol", "tarih"])
        .groupby("sembol")["kapanis"]
        .apply(lambda s: np.log(s).diff().dropna())
    )
    assert r.abs().max() <= 0.07 + 1e-12
    assert (
        len(a.gunler) == 500 and a.faiz_gunluk(a.gunler[0], a.gunler[-1]).notna().all()
    )


@pytest.mark.parametrize("aile", [simulator.AILE, ciftbolme.AILE])
def test_etki_ekle_yalniz_giris_gununun_aofunu_dusurur_fiyat_iliskilerini_korur(aile):
    # Değişen tek şey AOF (ve düşüğü); kapanış, yüksek, hacim aynı. AOF yalnız etki/(1+etki) oranında ve en az bir hissede düşer.
    a = denetim.dunya(7, hisse=24, gun=1100)
    b = denetim.etki_ekle(a, aile, 0.05)
    f0, f1 = (
        a.fiyat.set_index(["sembol", "tarih"]),
        b.fiyat.set_index(["sembol", "tarih"]),
    )
    for c in ("kapanis", "yuksek", "hacim", "ham_kapanis", "ham_yuksek", "pd"):
        pd.testing.assert_series_equal(f0[c], f1[c])
    oran = (f1["aof"] / f0["aof"]).to_numpy()
    assert set(np.round(oran, 12)) == {1.0, round(1 / 1.05, 12)}
    f = b.fiyat
    assert (
        (f["dusuk"] <= f["aof"])
        & (f["aof"] <= f["yuksek"])
        & (f["dusuk"] <= f["kapanis"])
        & (f["kapanis"] <= f["yuksek"])
    ).all()
    assert (
        (f["ham_dusuk"] <= f["ham_aof"]) & (f["ham_aof"] <= f["ham_yuksek"])
    ).all() and (f["ham_aof"] == f["aof"]).all()


def test_etki_ekle_ema_sinyali_izleyen_gunun_aofu_elle_hesapla():
    # Her sinyal gününü (kapanış günü j) izleyen günün (j+1) AOF'u 1,05'e bölünür; başka hiçbir günün AOF'u değişmez.
    a = denetim.dunya(7, hisse=24, gun=1100)
    konum = pd.Series(np.arange(len(a.gunler)), index=a.gunler)
    b = denetim.etki_ekle(a, simulator.AILE, 0.05)
    sinyalli = 0
    for s, f in a.fiyat.groupby("sembol"):
        sig = konum.reindex(
            aileler.sinyal(f.set_index("tarih")[["kapanis", "yuksek"]])
        ).to_numpy()
        beklenen = np.ones(len(f))
        beklenen[sig[sig + 1 < len(f)] + 1] = 1 / 1.05
        r = (
            b.fiyat[b.fiyat["sembol"] == s].set_index("tarih")["aof"]
            / f.set_index("tarih")["aof"]
        ).to_numpy()
        np.testing.assert_allclose(r, beklenen)
        sinyalli += len(sig) > 0
    assert sinyalli >= 1  # sınama boş değil


def kucuk(**kw):
    return dict(
        n=1, n_etki=1, tekrar=3, isci=1, hisse=8, gun=700, etkiler=(0.05,), **kw
    )


def test_calistir_yapi_oranlar_ve_gecti_bayragi():
    s = denetim.calistir(**kucuk())
    assert (s["n"], s["n_etki"], s["tekrar"], s["esik"], s["etkiler"]) == (
        1,
        1,
        3,
        0.05,
        [0.05],
    )
    for aile in (simulator.AILE, ciftbolme.AILE):
        for d in (*s["yanlis_kabul"][aile].values(), *s["guc"][aile][0.05].values()):
            assert d["n"] == 1 and d["adet"] in (0, 1) and d["oran"] == d["adet"]
        assert (
            s["yanlis_kabul"][aile]["kagit"]["adet"]
            <= s["yanlis_kabul"][aile]["olcut_1_4"]["adet"]
        )  # Kâğıt alt küme
    assert s["gecti"] == all(
        s["yanlis_kabul"][a]["olcut_1_4"]["oran"] <= 0.05 for a in s["yanlis_kabul"]
    )


def test_tekil_ayni_tohum_ayni_sonuc():
    ayni = lambda: denetim.tekil(5, simulator.AILE, 0.05, 3, 8, 700)  # noqa: E731
    assert ayni() == ayni()


def sonuc_ornek(gecti):
    d = lambda adet, n: {"n": n, "adet": adet, "oran": adet / n}  # noqa: E731
    yk = {
        a: {"olcut_1_4": d(1 if not gecti else 0, 20), "kagit": d(0, 20)}
        for a in (simulator.AILE, ciftbolme.AILE)
    }
    guc = {
        0.05: {"olcut_1_4": d(3, 4), "kagit": d(1, 4)},
        0.1: {"olcut_1_4": d(4, 4), "kagit": d(2, 4)},
    }
    return {
        "n": 20,
        "n_etki": 4,
        "tekrar": 200,
        "etkiler": [0.05, 0.1],
        "hisse": 125,
        "gun": 2000,
        "yanlis_kabul": yk,
        "guc": {a: guc for a in yk},
        "esik": 0.05,
        "gecti": gecti,
    }


def test_yaz_docs_ve_rapor_dosyalarini_yazar_yuzdeler_elle():
    # 1/20 = %5,00; 0/20 = %0,00; güç %5 etkide 3/4 = %75,00 ve 1/4 = %25,00; %10 etkide 4/4 = %100,00 ve 2/4 = %50,00.
    md, html = denetim.yaz(sonuc_ornek(False))
    metin = md.read_text(encoding="utf-8")
    assert "KALDI: ilk resmi koşu yapılmaz" in metin and "%5,00 (1/20)" in metin
    assert (
        "Güç %5,00 (ölçüt 1–4 / Kâğıt) |" in metin
        and "%75,00 (3/4) / %25,00 (1/4)" in metin
    )
    assert (
        "%100,00 (4/4) / %50,00 (2/4)" in metin
        and "EMA sıkışması" in metin
        and "Çift rotasyonu" in metin
    )
    assert (
        "(ölçüt 1–4 Geçti ve portföy kuralı reddetmedi)" in metin
        and "TASARIM 5.12" in metin
        and "alt kümesidir" not in metin
    )
    assert "GEÇTİ" in denetim.yaz(sonuc_ornek(True))[0].read_text(encoding="utf-8")
    assert "Boru hattı denetimi" in html.read_text(encoding="utf-8")


def test_denetim_komutu_sonucu_gunluge_destek_olarak_yazar_ve_ilk_resmi_kosu_kapisini_acar(
    monkeypatch, capsys
):
    from tansu.__main__ import main

    monkeypatch.setattr(denetim, "calistir", lambda **kw: sonuc_ornek(True))
    kayit.kayitla()
    assert main(["denetim"]) == 0
    satir = [
        json.loads(s)
        for s in (kayit.KAYIT_DIZINI / "deneme.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ][-1]
    assert (satir["tur"], satir["olay"], satir["gecti"]) == ("destek", "denetim", True)
    assert (
        kayit.denetim_gecti(satir["kod_hash"]) and kayit.deneme_sayisi() == 0
    )  # Holm m'ye girmez
    monkeypatch.setattr(denetim, "calistir", lambda **kw: sonuc_ornek(False))
    assert main(["denetim"]) == 1
    assert not kayit.denetim_gecti(satir["kod_hash"])  # son denetim kaldı
    assert "ilk resmi koşu yapılmaz" in capsys.readouterr().err
