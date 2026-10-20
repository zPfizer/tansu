"""`veri` yüzü: sahte kaynaktan anlık görüntü üretme, okuma, olay denetimi.

Fiyatlar CCOLA'nın İş Yatırım'daki gerçek değerleridir (08–15.08.2024). Olay çarpanları
`GetSermayeArttirimlari`'ndan alındı. Beklenen değerler elle hesaplandı (yorumlarda).
"""

import datetime as dt
import json

import numpy as np
import pandas as pd
import pytest

from tansu import veri
from tansu.kaynak import KaynakHatasi


# Olay tarihi: SHHE_TARIH, ms epoch, İstanbul gece yarısı (UTC 21:00, önceki gün).
def epoch(gun):
    return int(
        dt.datetime(
            gun.year, gun.month, gun.day, tzinfo=dt.timezone(dt.timedelta(hours=3))
        ).timestamp()
        * 1000
    )


def satir(tarih, ham, duz):
    return {
        "tarih": pd.Timestamp(tarih),
        "ham_kapanis": ham,
        "kapanis": duz,
        "ham_aof": ham,
        "ham_yuksek": ham,
        "ham_dusuk": ham,
        "aof": duz,
        "yuksek": duz,
        "dusuk": duz,
        "hacim": 1.0,
        "pd": 1.0,
        "hao_pd": 1.0,
        "sermaye": 1.0,
        "xu100": 1.0,
    }


CCOLA_FIYAT = [
    satir("2024-08-08", 757.5, 66.3352),
    satir("2024-08-09", 757.5, 66.3352),
    satir("2024-08-12", 760.5, 66.5979),
    satir("2024-08-13", 69.35, 66.8037),
    satir("2024-08-14", 67.75, 65.2624),
    satir("2024-08-15", 67.6, 65.1179),
]
CCOLA_OLAY = [
    {
        "SHT_KODU": "02",
        "SHHE_TARIH": epoch(dt.date(2024, 8, 13)),
        "SHHE_FIYAT_AYAR_OR": 0.09090909138724523,
    },
    {
        "SHT_KODU": "04",
        "SHHE_TARIH": epoch(dt.date(2025, 5, 26)),
        "SHHE_FIYAT_AYAR_OR": 0.9792410463023796,
    },
    {
        "SHT_KODU": "04",
        "SHHE_TARIH": epoch(dt.date(2026, 5, 12)),
        "SHHE_FIYAT_AYAR_OR": 0.9837037037037037,
    },
]


class SahteKaynak:
    def __init__(self, fiyatlar, olaylar):
        self.fiyatlar, self.olaylar_ = fiyatlar, olaylar

    def fiyat(self, sembol, bas, son):
        return pd.DataFrame(self.fiyatlar[sembol])

    def olaylar(self, sembol):
        return self.olaylar_[sembol]


SIMDI = dt.datetime(2026, 10, 5, 19, 30)


def test_cift_kalite_politikalari_sonsuz_fiyati_esitlemez():
    # #85: eski iki yolun gözlenmiş farkı; son fiyat dolum günü değildir.
    gunler = pd.date_range("2024-01-01", periods=3)
    C = np.array([[10.0, 20.0], [np.inf, 21.0], [12.0, 22.0]])
    A = C.copy()
    F = {"I": np.ones((3, 2), dtype=bool)}
    F.update({k: np.zeros((3, 2), dtype=bool) for k in ("T", "B", "Kar")})
    p = veri.cift_girdileri(gunler, C, A, F, "legacy_portfoy_v1")
    t = veri.cift_girdileri(gunler, C, A, F, "legacy_tansu_v1")
    assert p["Kar"][:, 0].tolist() == [False, False, False]
    assert t["Kar"][:, 0].tolist() == [False, True, False]
    assert t["SA"][:, 0].tolist() == [10.0, 10.0, 12.0]
    assert t["E"][:, 0].tolist() == [False, True, True]
    assert t["G"][:, 0].tolist() == [True, False, True]
    assert np.isinf(p["SA"][1, 0])
    assert t["son_gecerli_fiyat_tarihi"][1, 0] == np.datetime64("2024-01-01")


def test_e1_kayitli_goruntu_referansi_eksik_deger_ve_degismezlik(tmp_path):
    import hashlib

    a = anlik(tmp_path)
    klasor = tmp_path / "ag" / a.kimlik
    once = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in klasor.iterdir()
    }
    istek = veri.VeriIstegi(
        ("CCOLA",),
        "2024-08-08",
        "2024-08-15",
        "yerel",
        "legacy_tansu_v1",
        "legacy_tansu_v1",
        "is_yatirim",
        "xu100",
    )
    yanit = veri.veri_hazirla(istek, a.kimlik, tmp_path)
    assert len(yanit["piyasa"]) == 6
    ilk = yanit["piyasa"][0]
    assert ilk.get("bos_nedenleri", {}).get("olay_ref") == "olay_yok"
    assert (
        yanit["referans"].get("bos_nedenleri", {}).get("isinma_donemi") == "istenmedi"
    )
    assert ilk["ham_acilis"] == {
        "deger": None,
        "birim": "TL/adet",
        "bos_nedeni": "kaynakta_yok",
    }
    assert ilk["ham_kapanis"]["deger"] == 757.5
    assert ilk["duzeltilmis_kapanis"]["deger"] == 66.3352
    assert yanit["referans"]["manifest_parmak_izi"] == once["manifest.json"]
    assert yanit["referans"]["kalite_surumu"] == "legacy_tansu_v1"
    assert yanit["referans"]["goruntu_id"] == a.kimlik
    assert {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in klasor.iterdir()
    } == once
    (klasor / "olaylar.json").write_text("{}", encoding="utf-8")
    with pytest.raises(veri.VeriHatasi, match="manifest uyuşmuyor"):
        veri.veri_hazirla(istek, a.kimlik, tmp_path)


def _eski_cift_hazirligi(gunler, C, A, F, tansu):
    """#85 öncesi ciftbolme.hazirla / tansusinama.cift_tablolari hesapları.

    Bu donmuş karşılaştırma sahibi ürünün yeni hazırlama fonksiyonunu çağırmaz.
    """
    Kar = F["Kar"] | np.isinf(C) | np.isinf(A) if tansu else F["Kar"]
    G = F["I"] & ~Kar
    if tansu:
        G = G & np.isfinite(C) & (C > 0) & np.isfinite(A) & (A > 0)
    return {
        "C": C,
        "A": A,
        "I": F["I"],
        "T": F["T"],
        "B": F["B"],
        "Kar": Kar,
        "G": G,
        "E": pd.DataFrame(Kar.astype(float))
        .rolling(250, min_periods=1)
        .max()
        .to_numpy()
        .astype(bool),
        "SA": pd.DataFrame(A).where(G).ffill().to_numpy(),
        "Cf": pd.DataFrame(C).where(G).ffill().to_numpy(),
    }


@pytest.mark.parametrize("politika", ["legacy_portfoy_v1", "legacy_tansu_v1"])
def test_kayitli_sentetik_goruntu_eski_hazirlamayla_ayni(
    tmp_path, monkeypatch, politika
):
    import hashlib

    fiyatlar = [dict(r) for i, r in enumerate(CCOLA_FIYAT) if i != 1]
    fiyatlar[3]["kapanis"] = -1.0  # 14.08 bozuk; 09.08 eksik.
    b = [satir(r["tarih"], 100.0, 100.0) for r in CCOLA_FIYAT]
    k = SahteKaynak({"CCOLA": fiyatlar, "BBBB": b}, {"CCOLA": CCOLA_OLAY, "BBBB": []})
    kimlik = veri.indir(["CCOLA", "BBBB"], tmp_path, k, simdi=SIMDI)
    klasor = tmp_path / "ag" / kimlik
    once = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in klasor.iterdir()
    }

    def yasak(*args, **kwargs):
        pytest.fail("yerel tekrar sağlayıcıya erişti")

    monkeypatch.setattr(SahteKaynak, "fiyat", yasak)
    monkeypatch.setattr(SahteKaynak, "olaylar", yasak)
    a = veri.oku(kimlik, tmp_path)
    beklenen = pd.concat(
        [
            pd.DataFrame(fiyatlar).assign(sembol="CCOLA"),
            pd.DataFrame(b).assign(sembol="BBBB"),
        ],
        ignore_index=True,
    )
    pd.testing.assert_frame_equal(a.fiyat, beklenen)
    assert a.olaylar["kod"].tolist() == ["02", "04", "04"]
    assert a.olaylar["carpan"].tolist() == [
        0.09090909138724523,
        0.9792410463023796,
        0.9837037037037037,
    ]
    g = a.gun_tablosu
    ccola = g[g["sembol"] == "CCOLA"]
    assert ccola["eksik"].tolist() == [False, True, False, False, False, False]
    assert ccola["karantina"].tolist() == [False, False, False, False, True, False]
    semboller = ["CCOLA", "BBBB"]  # Bilerek alfabetik değil.
    C, A = [
        a.fiyat.pivot(index="tarih", columns="sembol", values=ad)
        .reindex(index=a.gunler, columns=semboller)
        .to_numpy()
        for ad in ("kapanis", "aof")
    ]
    F = {
        ad: g.pivot(index="tarih", columns="sembol", values=sutun)
        .reindex(index=a.gunler, columns=semboller)
        .fillna(False)
        .astype(bool)
        .to_numpy()
        for ad, sutun in (
            ("I", "islem"),
            ("T", "kilit_tavan"),
            ("B", "kilit_taban"),
            ("Kar", "karantina"),
        )
    }
    eski = _eski_cift_hazirligi(a.gunler, C, A, F, politika == "legacy_tansu_v1")
    yeni = veri.cift_girdileri(
        a.gunler, C, A, veri.cift_bayraklari(g, a.gunler, semboller), politika
    )
    for ad, deger in eski.items():
        np.testing.assert_array_equal(yeni[ad], deger, err_msg=ad)
    istek = veri.VeriIstegi(
        tuple(semboller),
        "2024-08-08",
        "2024-08-15",
        "yerel",
        politika,
        "legacy",
        "is_yatirim",
        "xu100",
    )
    yanit = veri.veri_hazirla(istek, kimlik, tmp_path)
    json.dumps(yanit, allow_nan=False)
    assert [r["sembol"] for r in yanit["piyasa"]] == semboller * 6
    eksik = yanit["piyasa"][2]
    assert eksik["duzeltilmis_kapanis"]["deger"] is None
    assert eksik["son_gecerli_fiyat_tarihi"] == "2024-08-08"
    assert not eksik["islem"]
    assert yanit["piyasa"][8]["duzeltilmis_kapanis"] == {
        "deger": None,
        "birim": "TL/adet",
        "bos_nedeni": "pozitif_degil",
    }
    assert yanit["kalite"]["karantina_araliklari"] == [
        {"sembol": "CCOLA", "baslangic": "2024-08-14", "bitis": "2024-08-15"}
    ]
    assert {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in klasor.iterdir()
    } == once


def test_e1_alt_kume_kaynak_gunu_kararini_degistirmez(tmp_path):
    semboller = [f"S{i:02}" for i in range(20)]
    fiyatlar = {
        s: [
            satir("2024-01-02", 100.0, 100.0),
            satir("2024-01-03", 130.0 if i < 10 else 100.0, 130.0 if i < 10 else 100.0),
        ]
        for i, s in enumerate(semboller)
    }
    kimlik = veri.indir(
        semboller,
        tmp_path,
        SahteKaynak(fiyatlar, dict.fromkeys(semboller, [])),
        simdi=SIMDI,
    )
    istek = veri.VeriIstegi(
        ("S19",),
        "2024-01-03",
        "2024-01-03",
        "yerel",
        "legacy_tansu_v1",
        "legacy",
        "is_yatirim",
        "xu100",
    )
    sonuc = veri.veri_hazirla(istek, kimlik, tmp_path)
    assert sonuc["piyasa"][0]["kalite_bayraklari"] == ["eksik"]
    assert not sonuc["piyasa"][0]["islem"]
    assert sonuc["piyasa"][0]["son_gecerli_fiyat_tarihi"] == "2024-01-02"


@pytest.mark.parametrize(
    "alan, deger, mesaj",
    [
        ("kalite_surumu", "gelecek_v999", "bilinmeyen kalite"),
        ("semboller", ("CCOLA", "CCOLA"), "tekrarlı"),
        ("bitis", "2024-08-01", "dönem geçersiz"),
        ("uyelik_surumu", "", "referansı boş"),
    ],
)
def test_e1_cozulmemis_istegi_kabul_etmez(tmp_path, alan, deger, mesaj):
    from dataclasses import replace

    a = anlik(tmp_path)
    istek = veri.VeriIstegi(
        ("CCOLA",),
        "2024-08-08",
        "2024-08-15",
        "yerel",
        "legacy_tansu_v1",
        "legacy",
        "is_yatirim",
        "xu100",
    )
    with pytest.raises(veri.VeriHatasi, match=mesaj):
        veri.veri_hazirla(replace(istek, **{alan: deger}), a.kimlik, tmp_path)


def anlik(tmp_path, fiyat=CCOLA_FIYAT, olay=CCOLA_OLAY):
    k = SahteKaynak({"CCOLA": fiyat}, {"CCOLA": olay})
    kimlik = veri.indir(["CCOLA"], tmp_path, k, simdi=SIMDI)
    return veri.oku(kimlik, tmp_path)


def test_ccola_bolunmesi_olay_carpaniyla_tutar(tmp_path):
    # 12.08 beklenen oran = 0,090909 × 0,979241 × 0,983704 = 0,087572; gözlenen 66,5979/760,5 = 0,087571.
    # 13.08 beklenen = 0,979241 × 0,983704 = 0,963283; gözlenen 66,8037/69,35 = 0,963283.
    a = anlik(tmp_path)
    assert a.olay_uyarilari.empty
    assert list(a.fiyat["sembol"].unique()) == ["CCOLA"]
    assert len(a.fiyat) == 6


def test_bozuk_duzeltilmis_fiyat_uyari_verir(tmp_path):
    bozuk = [dict(s) for s in CCOLA_FIYAT]
    bozuk[1]["kapanis"] = (
        70.0  # 09.08: 70/757,5 = 0,09241; beklenen 0,08757 → fark %5,5
    )
    a = anlik(tmp_path, fiyat=bozuk)
    assert list(a.olay_uyarilari["tarih"]) == [pd.Timestamp("2024-08-09")]


def test_olay_tablosu_bir_gun_kaymis_olsa_da_eslesir(tmp_path):
    kayik = [dict(o) for o in CCOLA_OLAY]
    kayik[0]["SHHE_TARIH"] = epoch(dt.date(2024, 8, 12))  # gerçek adım 13.08'de
    a = anlik(tmp_path, olay=kayik)
    assert a.olay_uyarilari.empty


def test_olay_tablosu_bir_gun_sonraya_kaymis_olsa_da_eslesir(tmp_path):
    kayik = [dict(o) for o in CCOLA_OLAY]
    kayik[0]["SHHE_TARIH"] = epoch(dt.date(2024, 8, 14))  # gerçek adım 13.08'de
    a = anlik(tmp_path, olay=kayik)
    assert a.olay_uyarilari.empty


def test_iki_gun_kayma_pencere_disidir_uyari_verir(tmp_path):
    # Olay 15.08'e yazılırsa aday günler 14.08 ve 15.08; 13.08'deki gerçek adım bulunamaz.
    kayik = [dict(o) for o in CCOLA_OLAY]
    kayik[0]["SHHE_TARIH"] = epoch(dt.date(2024, 8, 15))
    a = anlik(tmp_path, olay=kayik)
    assert not a.olay_uyarilari.empty


def test_ayni_gune_iki_kayit_carpilir(tmp_path):
    # Bölünme çarpanı 0,090909 iki kayda bölünür: 0,30303 × 0,30000 = 0,090909.
    iki = [dict(o) for o in CCOLA_OLAY]
    iki[0] = {**iki[0], "SHHE_FIYAT_AYAR_OR": 0.30303030462415077}
    iki.insert(1, {**iki[0], "SHT_KODU": "01", "SHHE_FIYAT_AYAR_OR": 0.3})
    a = anlik(tmp_path, olay=iki)
    assert a.olay_uyarilari.empty


def test_pencereden_onceki_olay_hicbir_satiri_etkilemez(tmp_path):
    # Gerçek koşuda bulundu: pencere başından önceki olay ilk güne kaydırılıp ilk satıra uygulanıyordu.
    once = [
        {
            "SHT_KODU": "04",
            "SHHE_TARIH": epoch(dt.date(2024, 8, 7)),
            "SHHE_FIYAT_AYAR_OR": 0.5,
        },
        *CCOLA_OLAY,
    ]
    a = anlik(tmp_path, olay=once)
    assert a.olay_uyarilari.empty


def test_bozuk_manifest_hata_verir(tmp_path):
    k = SahteKaynak({"CCOLA": CCOLA_FIYAT}, {"CCOLA": CCOLA_OLAY})
    kimlik = veri.indir(["CCOLA"], tmp_path, k, simdi=SIMDI)
    dosya = next(
        p for p in (tmp_path / "ag" / kimlik).iterdir() if p.suffix == ".parquet"
    )
    dosya.write_bytes(dosya.read_bytes() + b"x")
    with pytest.raises(veri.VeriHatasi):
        veri.oku(kimlik, tmp_path)


def test_anlik_goruntu_kimligi_tarihli_ve_olay_ham_json_saklanir(tmp_path):
    k = SahteKaynak({"CCOLA": CCOLA_FIYAT}, {"CCOLA": CCOLA_OLAY})
    kimlik = veri.indir(["CCOLA"], tmp_path, k, simdi=SIMDI)
    assert kimlik == "20261005-1930"
    ham = json.loads(
        (tmp_path / "ag" / kimlik / "olaylar.json").read_text(encoding="utf-8")
    )
    assert ham["CCOLA"] == CCOLA_OLAY
    klasor = tmp_path / "ag" / kimlik
    manifest = json.loads((klasor / "manifest.json").read_text(encoding="utf-8"))
    assert "kapanan.csv" not in manifest["dosyalar"]
    assert not (klasor / "kapanan.csv").exists()
    assert len(veri.oku(kimlik, tmp_path).fiyat) == 6
    (klasor / "kapanan.csv").write_bytes(b"eski kanit")
    assert len(veri.oku(kimlik, tmp_path).fiyat) == 6
    assert (klasor / "kapanan.csv").read_bytes() == b"eski kanit"
    assert not any(p.name.startswith("_") for p in (tmp_path / "ag").iterdir())


class SahteBorsapy:
    def __init__(self, faiz, sektor):
        self._faiz, self._sektor = faiz, sektor

    def faiz(self):
        return pd.DataFrame(
            {
                "tarih": pd.to_datetime([t for t, _ in self._faiz]),
                "faiz": [f for _, f in self._faiz],
            }
        )

    def sektor(self, sembol):
        return self._sektor[sembol]


FAIZ = [("2024-03-22", 50.0), ("2024-12-27", 47.5), ("2025-01-24", 45.0)]


def anlik_borsapy(tmp_path, faiz=FAIZ, fiyat=CCOLA_FIYAT):
    k = SahteKaynak({"CCOLA": fiyat}, {"CCOLA": CCOLA_OLAY})
    b = SahteBorsapy(faiz, {"CCOLA": "GIDA"})
    kimlik = veri.indir(["CCOLA"], tmp_path, k, simdi=SIMDI, borsapy=b)
    return kimlik, veri.oku(kimlik, tmp_path)


def test_faiz_ve_sektor_anlik_goruntuye_yazilir_ve_manifestte_hashlenir(tmp_path):
    kimlik, a = anlik_borsapy(tmp_path)
    manifest = json.loads(
        (tmp_path / "ag" / kimlik / "manifest.json").read_text(encoding="utf-8")
    )
    assert {"faiz.parquet", "sektor.json"} <= set(manifest["dosyalar"])
    assert list(a.faiz["faiz"]) == [50.0, 47.5, 45.0]
    assert a.sektor == {"CCOLA": "GIDA"}


def test_okuma_canli_borsapyye_baglanmaz_bozuk_faiz_dosyasi_hata_verir(tmp_path):
    kimlik, _ = anlik_borsapy(tmp_path)
    dosya = tmp_path / "ag" / kimlik / "faiz.parquet"
    dosya.write_bytes(dosya.read_bytes() + b"x")
    with pytest.raises(veri.VeriHatasi):
        veri.oku(kimlik, tmp_path)


def test_faiz_gunluge_ileri_doldurulur_ve_bir_gun_gecikir(tmp_path):
    # Değişim 22.03.2024'te %50 olur; ertesi gün (23.03) kullanılır, 22.03'te seri henüz yoktur.
    # 27.12.2024'te %47,5 olur: 27.12 hâlâ eski %50'yi, 28.12 yeni %47,5'i kullanır.
    _, a = anlik_borsapy(tmp_path)
    s = a.faiz_gunluk(dt.date(2024, 3, 23), dt.date(2024, 12, 29))
    assert s[pd.Timestamp("2024-03-23")] == 50.0
    assert s[pd.Timestamp("2024-07-01")] == 50.0
    assert s[pd.Timestamp("2024-12-27")] == 50.0
    assert s[pd.Timestamp("2024-12-28")] == 47.5
    assert (
        len(s) == 282
    )  # 23.03 – 29.12.2024 takvim günü: 9 + 30+31+30+31+31+30+31+30+29 → 282


def test_faiz_serisi_baslangici_kapsamiyorsa_hata(tmp_path):
    _, a = anlik_borsapy(tmp_path)
    with pytest.raises(veri.VeriHatasi):  # 22.03'te önceki gün değeri yok
        a.faiz_gunluk(dt.date(2024, 3, 22), dt.date(2024, 3, 25))


def test_son_faiz_degisim_tarihi_kaydedilir(tmp_path):
    _, a = anlik_borsapy(tmp_path)
    assert a.faiz_son_degisim == pd.Timestamp("2025-01-24")


def test_bos_faiz_serisi_sorunludur(tmp_path):
    k = SahteKaynak({"CCOLA": CCOLA_FIYAT}, {"CCOLA": CCOLA_OLAY})
    with pytest.raises(veri.VeriHatasi):
        veri.indir(
            ["CCOLA"],
            tmp_path,
            k,
            simdi=SIMDI,
            borsapy=SahteBorsapy([], {"CCOLA": "GIDA"}),
        )
    assert not (tmp_path / "ag").exists() or not list((tmp_path / "ag").iterdir())


def test_takvim_xu100_kapanisi_olan_gunlerdir(tmp_path):
    # 09.08'de xu100 NaN (kapanış yok), 12.08'de 0 → ikisi de takvimde yok. Kalan 4 gün.
    f = [dict(s) for s in CCOLA_FIYAT]
    f[1]["xu100"], f[2]["xu100"] = float("nan"), 0.0
    _, a = anlik_borsapy(tmp_path, fiyat=f)
    assert list(a.gunler) == [
        pd.Timestamp(t)
        for t in ("2024-08-08", "2024-08-13", "2024-08-14", "2024-08-15")
    ]


def test_sektoru_alinamayan_ya_da_bos_sembol_indirmeyi_durdurmaz(tmp_path):
    # Evren ölçeğinde bazı kodlar için KAP sektörü yoktur; sektör yalnız inen hisseler için sorulur.
    class Borsapy(SahteBorsapy):
        def sektor(self, sembol):
            if sembol == "CCOLA2":
                raise KaynakHatasi(sembol)
            assert sembol != "BOS", "boş sembol için sektör sorulmaz"
            return "GIDA"

    k = SahteKaynak(
        {"CCOLA": CCOLA_FIYAT, "CCOLA2": CCOLA_FIYAT, "BOS": []},
        {"CCOLA": CCOLA_OLAY, "CCOLA2": CCOLA_OLAY, "BOS": []},
    )
    kimlik = veri.indir(
        ["CCOLA", "CCOLA2", "BOS"], tmp_path, k, simdi=SIMDI, borsapy=Borsapy(FAIZ, {})
    )
    a = veri.oku(kimlik, tmp_path)
    assert (a.sektor, a.bos) == ({"CCOLA": "GIDA"}, ("BOS",))


def test_tarihsiz_ya_da_carpansiz_olay_kaydi_okumada_atilir(tmp_path):
    # Gerçek ACSEL kayıtları: planlanmış temettü yer tutucusu, tarih 0001-01-01 (ms -62135596800000) ve
    # çarpan 0,0; bir başkasında tarih geçerli ama çarpan 0,0. İkisi de düzeltme taşımaz.
    bos = [
        {"SHT_KODU": "04", "SHHE_TARIH": -62135596800000, "SHHE_FIYAT_AYAR_OR": 0.0},
        {
            "SHT_KODU": "04",
            "SHHE_TARIH": epoch(dt.date(2024, 8, 14)),
            "SHHE_FIYAT_AYAR_OR": 0.0,
        },
    ]
    a = anlik(tmp_path, olay=CCOLA_OLAY + bos)
    assert len(a.olaylar) == 3 and (a.olaylar["carpan"] > 0).all()


class SahteKapSektor:
    """`kaynak.KapSektor` yüzü: ad | None (listede yok) | KaynakHatasi."""

    def __init__(self, sonuc):
        self.sonuc, self.sorulan = sonuc, []

    def sektor(self, sembol):
        self.sorulan.append(sembol)
        s = self.sonuc[sembol]
        if s == "HATA":
            raise KaynakHatasi(sembol)
        return s


class _YalnizA(SahteBorsapy):
    def __init__(self):
        super().__init__(FAIZ, {})

    def sektor(self, sembol):
        if sembol != "A":
            raise KaynakHatasi(sembol)  # KAP ilk sembolden sonra boş döndü (bilet 07)
        return "ESKI"


def _sektor_anlik(tmp_path, semboller=("A", "B", "C", "D"), kapanan=None):
    k = SahteKaynak(
        {s: CCOLA_FIYAT for s in semboller}, {s: CCOLA_OLAY for s in semboller}
    )
    return veri.indir(
        list(semboller), tmp_path, k, simdi=SIMDI, borsapy=_YalnizA(), kapanan=kapanan
    )


@pytest.mark.parametrize("kanit", [False, True])
def test_sektor_tamamla_yeni_anlik_goruntu_yazar_eskisi_degismez(tmp_path, kanit):
    # A zaten var (korunur, sorulmaz). B, C sektör alır; D KAP listesinde yok (None) → sektörsüz, kapsamda yazılır.
    kapanan = (
        pd.DataFrame(
            [["D", "Şirket", "2024-08-13", "birleşmiştir"]],
            columns=["kod", "ad", "tarih", "aciklama"],
        )
        if kanit
        else None
    )
    eski = _sektor_anlik(tmp_path, kapanan=kapanan)
    manifest_eski = (tmp_path / "ag" / eski / "manifest.json").read_bytes()
    kap = SahteKapSektor({"B": "BANKA", "C": "GIDA", "D": None})
    yeni, rapor = veri.sektor_tamamla(
        eski, tmp_path, kap, ["D", "C", "B", "A"], simdi=dt.datetime(2026, 10, 5, 20, 0)
    )
    assert yeni == "20261005-2000" and kap.sorulan == ["D", "C", "B"]
    assert (tmp_path / "ag" / eski / "manifest.json").read_bytes() == manifest_eski
    a = veri.oku(yeni, tmp_path)  # manifest doğrulanır
    assert a.sektor == {"A": "ESKI", "B": "BANKA", "C": "GIDA"}
    assert len(a.fiyat) == 4 * len(CCOLA_FIYAT) and len(a.olaylar) == 4 * 3
    m = json.loads(
        (tmp_path / "ag" / yeni / "manifest.json").read_text(encoding="utf-8")
    )
    assert m["kaynak"] == eski
    assert m["sektor_kapsam"] == {
        "hedef": 4,
        "var": 3,
        "listede_yok": ["D"],
        "alinamayan": [],
    }
    assert rapor == m["sektor_kapsam"]
    if kanit:
        eski_kanit = tmp_path / "ag" / eski / "kapanan.csv"
        yeni_kanit = tmp_path / "ag" / yeni / "kapanan.csv"
        assert yeni_kanit.read_bytes() == eski_kanit.read_bytes()
        assert (
            m["dosyalar"]["kapanan.csv"]
            == json.loads(manifest_eski)["dosyalar"]["kapanan.csv"]
        )


def test_sektor_tamamla_art_arda_bes_hatada_durur_tamamlananlar_tekrar_istenmez(
    tmp_path,
):
    eski = _sektor_anlik(tmp_path, tuple("ABCDEFGH"))
    hedef = list("BCDEFGH")
    kap = SahteKapSektor(
        {"B": "BANKA", "C": "HATA", "D": "HATA", "E": "HATA", "F": "HATA", "G": "HATA"}
    )
    yeni, _ = veri.sektor_tamamla(
        eski, tmp_path, kap, hedef, simdi=dt.datetime(2026, 10, 5, 20, 0)
    )
    assert yeni is None and kap.sorulan == list(
        "BCDEFG"
    )  # beşinci art arda hatada durur
    assert [a.name for a in (tmp_path / "ag").iterdir()] == [
        eski
    ]  # yarım anlık görüntü yazılmaz
    kap2 = SahteKapSektor(
        {"C": "GIDA", "D": "GIDA", "E": "GIDA", "F": "GIDA", "G": "HATA", "H": "HAVA"}
    )
    yeni, rapor = veri.sektor_tamamla(
        eski, tmp_path, kap2, hedef, simdi=dt.datetime(2026, 10, 5, 20, 1)
    )
    assert kap2.sorulan == list("CDEFGH")  # B önbellekten
    assert veri.oku(yeni, tmp_path).sektor == {
        "A": "ESKI",
        "B": "BANKA",
        "C": "GIDA",
        "D": "GIDA",
        "E": "GIDA",
        "F": "GIDA",
        "H": "HAVA",
    }
    assert rapor["alinamayan"] == ["G"] and rapor["var"] == 6 and rapor["hedef"] == 7


def test_olay_denetimi_yuzde_ikiyi_asarsa_uye_kosusu_sorunludur(tmp_path):
    # TASARIM 5.13: yalnız üye hisse-günlerde olay farkı > %2 kapıyı tetikler.
    gunler = pd.bdate_range("2024-01-02", periods=50)
    fiyat = [satir(g, 100.0, 100.0) for g in gunler]
    fiyat[0] = satir(gunler[0], 100.0, 99.0)  # 1/50 = %2, eşik dahil değil.
    a = anlik(tmp_path / "sinir", fiyat=fiyat, olay=[])
    uye = a.fiyat[["sembol", "tarih"]]
    assert a.oranlar(uye) == (0.0, 0.02, 50)
    assert a.sorunlar_uye(uye) == []
    fiyat[1] = satir(gunler[1], 100.0, 99.0)  # 2/50 = %4, kapı başarısız.
    b = anlik(tmp_path / "asan", fiyat=fiyat, olay=[])
    assert b.oranlar(uye) == (0.0, 0.04, 50)
    assert b.sorunlar_uye(uye) == ["olay denetimi farkı olan gün oranı > %2"]
    # İkinci fark evren dışı bırakılırsa pay ve payda birlikte küçülür: 1/49 > %2.
    assert b.sorunlar_uye(uye.iloc[1:]) == ["olay denetimi farkı olan gün oranı > %2"]
    assert b.sorunlar_uye(uye.iloc[2:]) == []


def test_karantinaya_giren_fiyat_yamanmaz(tmp_path):
    # TASARIM 5.1: karantina fiyatı değiştirmez; ham ve düzeltilmiş değerler saklanır.
    a = anlik(
        tmp_path,
        fiyat=[satir("2024-01-02", 100.0, 50.0), satir("2024-01-03", 150.0, 75.0)],
        olay=[],
    )
    g = a.gun_tablosu.set_index("tarih")
    assert g.loc["2024-01-03", "karantina"]
    assert a.fiyat.loc[1, ["ham_kapanis", "ham_aof", "kapanis", "aof"]].tolist() == [
        150.0,
        150.0,
        75.0,
        75.0,
    ]
    yeniden = veri.oku(a.kimlik, tmp_path)
    assert yeniden.fiyat.loc[
        1, ["ham_kapanis", "ham_aof", "kapanis", "aof"]
    ].tolist() == [150.0, 150.0, 75.0, 75.0]


def _karantina(a):
    return a.gun_tablosu.set_index("tarih")["karantina"].tolist()


def test_limit_bazi_onceki_gunun_ham_kapanisidir_karantinali_gun_de_baz_olur(tmp_path):
    # TASARIM 5.1: baz fiyat = önceki ham kapanış. d2 150 (100'ün +%50'si) karantinaya girer; d3 tavanı 150 × 1,10 = 165,
    # d3 kapanışı 160 limit içinde, karantina yok. (Önceki temiz kapanış 100 olsaydı tavan 110 olur, d3 karantinaya girerdi.)
    a = anlik(
        tmp_path,
        fiyat=[
            satir("2024-01-02", 100.0, 100.0),
            satir("2024-01-03", 150.0, 150.0),
            satir("2024-01-04", 160.0, 160.0),
        ],
        olay=[],
    )
    assert _karantina(a) == [False, True, False]
    assert a.gun_tablosu["tavan"].iloc[2] == pytest.approx(165.0)


# Ham 100, 101, 102, 51, 52; düzeltilmiş 50, 50,5, 51, 51, 52 (çarpan 0,5 gerçekte 05.01.2024'te işler).
BOLUNME = [
    satir("2024-01-02", 100.0, 50.0),
    satir("2024-01-03", 101.0, 50.5),
    satir("2024-01-04", 102.0, 51.0),
    satir("2024-01-05", 51.0, 51.0),
    satir("2024-01-08", 52.0, 52.0),
]


def _bolunme_olayi(gun):
    return [{"SHT_KODU": "02", "SHHE_TARIH": epoch(gun), "SHHE_FIYAT_AYAR_OR": 0.5}]


@pytest.mark.parametrize("olay_gunu", [dt.date(2024, 1, 4), dt.date(2024, 1, 5)])
def test_adimi_t_eksi_1_ya_da_t_tarihli_olay_aciklar_karantina_yok(tmp_path, olay_gunu):
    # TASARIM 5.1 karantina: t = 05.01 (51 / 102 = 0,5); olay 04.01 (t-1) ya da 05.01 (t) yazılsa da
    # baz fiyat 05.01'de 102 × 0,5 = 51, tavan 51 × 1,10 = 56,1.
    a = anlik(tmp_path, fiyat=BOLUNME, olay=_bolunme_olayi(olay_gunu))
    assert _karantina(a) == [False] * 5
    assert a.gun_tablosu["tavan"].iloc[3] == pytest.approx(56.1)
    # 04.01 (olay günü ya da t-1) fiyat adımı değil (102 / 101): baz 101, tavan 101 × 1,10 = 111,1, karantina yok.
    assert a.gun_tablosu["tavan"].iloc[2] == pytest.approx(111.1)


def test_t_arti_1_tarihli_olay_adimi_aciklamaz_adim_gunu_karantinaya_girer(tmp_path):
    # TASARIM 5.1 (vekil kararı 15.10, 07e-4): olay 08.01 (t+1), adım 05.01. Baz 102, taban 102 × 0,9 = 91,8;
    # kapanış 51 taban altında: karantina. 08.01: 52 / 51 adım değil, çarpan almaz, baz 51, kapanış 52: temiz.
    a = anlik(tmp_path, fiyat=BOLUNME, olay=_bolunme_olayi(dt.date(2024, 1, 8)))
    assert _karantina(a) == [False, False, False, True, False]
    assert a.gun_tablosu["taban"].iloc[3] == pytest.approx(91.8)


def test_bozuk_satir_baz_fiyat_olmaz_baz_onceki_tutarli_gunun_ham_kapanisidir(tmp_path):
    # TASARIM 5.1 (vekil kararı 15.10): d2'de ham düşük 200 > ham kapanış 150, satır ihlali, karantina.
    # d3 tavanı bozuk d2'den değil d1'den çıkar: 100 × 1,10 = 110; d3 kapanışı 160 > 110 × 1,005, karantina.
    bozuk = {**satir("2024-01-03", 150.0, 150.0), "ham_dusuk": 200.0}
    a = anlik(
        tmp_path,
        fiyat=[
            satir("2024-01-02", 100.0, 100.0),
            bozuk,
            satir("2024-01-04", 160.0, 160.0),
        ],
        olay=[],
    )
    assert _karantina(a) == [False, True, True]
    assert a.gun_tablosu["tavan"].iloc[2] == pytest.approx(110.0)


def test_adim_orani_onceki_tutarli_kapanisa_bakar_bozuk_satir_atlanir(tmp_path):
    # TASARIM 5.1 adım (bilet 07e-b, 5.13): kapanışlar 100, 50, 50; 2. gün bozuk (ham düşük 200 > kapanış), 3. gün olay
    # (çarpan 0,5). Oran 50 / 100 (önceki tutarlı kapanış) = 0,5: adım. Baz 100 × 0,5 = 50, taban 50 × 0,9 = 45,
    # kapanış 50 içinde: karantina yok. 2. gün bozuk satır: karantina.
    bozuk = {**satir("2024-01-03", 50.0, 50.0), "ham_dusuk": 200.0}
    a = anlik(
        tmp_path,
        fiyat=[
            satir("2024-01-02", 100.0, 100.0),
            bozuk,
            satir("2024-01-04", 50.0, 50.0),
        ],
        olay=_bolunme_olayi(dt.date(2024, 1, 4)),
    )
    assert _karantina(a) == [False, True, False]
    assert a.gun_tablosu["taban"].iloc[2] == pytest.approx(45.0)


@pytest.mark.parametrize("ad", ["kapanan.csv", "fiyat.parquet"])
def test_manifestteki_eksik_dosya_veri_hatasidir(tmp_path, ad):
    klasor = tmp_path / "ag" / "eksik"
    klasor.mkdir(parents=True)
    (klasor / "manifest.json").write_text(
        json.dumps({"dosyalar": {ad: "0" * 64}}), encoding="utf-8"
    )
    with pytest.raises(Exception) as hata:
        veri.oku("eksik", tmp_path)
    assert isinstance(hata.value, veri.VeriHatasi)
    assert f"eksik/{ad}" in str(hata.value)
    assert isinstance(hata.value.__cause__, FileNotFoundError)
