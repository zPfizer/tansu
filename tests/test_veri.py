"""`veri` yüzü: sahte kaynaktan anlık görüntü üretme, okuma, olay denetimi.

Fiyatlar CCOLA'nın İş Yatırım'daki gerçek değerleridir (08–15.08.2024). Olay çarpanları
`GetSermayeArttirimlari`'ndan alındı. Beklenen değerler elle hesaplandı (yorumlarda).
"""

import datetime as dt
import hashlib
import json

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


def test_kayitli_sentetik_goruntu_yerelden_okunur(tmp_path, monkeypatch):
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
    assert {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in klasor.iterdir()
    } == once


def test_yarisi_karantinada_olan_kaynak_gunu_eksik_sayilir(tmp_path):
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
    g = veri.oku(kimlik, tmp_path).gun_tablosu.set_index(["sembol", "tarih"])
    s19 = g.loc[("S19", pd.Timestamp("2024-01-03"))]
    assert s19["eksik"] and not s19["islem"] and not s19["karantina"]


@pytest.mark.parametrize("bozuk, kaynak", [(2, True), (1, False)])
def test_kaynak_gunu_esigi_satirlarin_yuzde_onu(tmp_path, bozuk, kaynak):
    # 30.04.2018: 411 hissenin 73'ünde (%17,8) düzeltilmiş düşük 0; %50 eşiği kaçırıyordu. Eşik %10
    # (SPEC 3.9 istisnası, Levent 30.10.2026). 20 satırın 2'si işaretliyse o satırlar kaynak hatasıdır (eksik,
    # karantinasız); 1'i ise satır karantinaya girer.
    semboller = [f"S{i:02}" for i in range(20)]
    fiyatlar = {
        s: [
            satir("2024-01-02", 100.0, 100.0),
            satir("2024-01-03", *([130.0] * 2 if i < bozuk else [100.0] * 2)),
        ]
        for i, s in enumerate(semboller)
    }
    kimlik = veri.indir(
        semboller,
        tmp_path,
        SahteKaynak(fiyatlar, dict.fromkeys(semboller, [])),
        simdi=SIMDI,
    )
    g = veri.oku(kimlik, tmp_path).gun_tablosu.set_index(["sembol", "tarih"])
    s00 = g.loc[("S00", pd.Timestamp("2024-01-03"))]
    assert s00["eksik"] == kaynak and s00["karantina"] != kaynak


@pytest.mark.parametrize("bozuk", [2, 9])
def test_yarisindan_azi_bozuk_kaynak_gununde_tutarli_satir_fiyatini_korur(
    tmp_path, bozuk
):
    # 16.09.2026: 623 satırın 126'sında (%20) ham AOF [düşük, yüksek] dışında; kalan 497 hisse gerçek düşüş günüdür
    # (ortanca −%5). Yalnız bozuk satırlar eksik gün olur ve karantina açmaz; tutarlı satırlar fiyatını korur
    # (SPEC 3.9 istisnası, Levent 30.10.2026). 20 satırın 2'si ya da 9'u (%45, yarının altı) bozuk: S00 eksik, S19
    # 90'da kapanır, fiyatı kalır.
    semboller = [f"S{i:02}" for i in range(20)]
    fiyatlar = {
        s: [
            satir("2024-01-02", 100.0, 100.0),
            {**satir("2024-01-03", 90.0, 90.0), "ham_yuksek": 91.0, "yuksek": 91.0}
            | ({"ham_aof": 95.0, "aof": 95.0} if i < bozuk else {}),
        ]
        for i, s in enumerate(semboller)
    }
    kimlik = veri.indir(
        semboller,
        tmp_path,
        SahteKaynak(fiyatlar, dict.fromkeys(semboller, [])),
        simdi=SIMDI,
    )
    a = veri.oku(kimlik, tmp_path)
    g = a.gun_tablosu.set_index(["sembol", "tarih"])
    gun = pd.Timestamp("2024-01-03")
    assert g.loc[("S00", gun), "eksik"] and not g.loc[("S00", gun), "karantina"]
    s19 = g.loc[("S19", gun)]
    assert not s19["eksik"] and s19["islem"] and not s19["karantina"]
    f = a.hesap_fiyati.set_index(["sembol", "tarih"])
    assert f.loc[("S19", gun), "kapanis"] == 90.0
    assert pd.isna(f.loc[("S00", gun), "kapanis"])


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


@pytest.mark.parametrize(
    "ilk_gun, iki_seans", [("2015-11-23", True), ("2015-11-30", False)]
)
def test_tek_seans_oncesi_seans_basina_yuzde_on(tmp_path, ilk_gun, iki_seans):
    # 30.11.2015 öncesi iki seans, seans başına ±%10 (BİST duyurusu 11699; SPEC 3.9 istisnası, Levent 30.10.2026).
    # 11 → 13,31 (+%21: ilk seans 12,10 tavanında, ikinci seans onun +%10'unda) aşım değildir; ±%10'da H = L kapanış
    # kilittir; +%25 yine aşımdır. Tek seansta (±%20) aynı yol: +%21 aşım, ±%10 kilit değil.
    tarihler = pd.bdate_range(ilk_gun, periods=5)
    fiyat = [
        satir(t, p, p)
        for t, p in zip(tarihler, [10.0, 11.0, 13.31, 11.98, 14.975], strict=True)
    ]
    fiyat[2] |= {"ham_dusuk": 12.10, "dusuk": 12.10}
    g = anlik(tmp_path, fiyat=fiyat, olay=[]).gun_tablosu
    assert g["karantina"].tolist() == [False, False, not iki_seans, False, True]
    assert g["kilit_tavan_duyarli"].tolist() == [False, iki_seans, False, False, False]
    assert g["kilit_taban_duyarli"].tolist() == [False, False, False, iki_seans, False]


def test_tek_seans_oncesi_baz_onceki_aof_kilitli_taban_gunu_asim_degil(tmp_path):
    # Eski rejimde baz önceki seansın AOF'siydi (BISTECH 2.1.1); seans verisi olmadığından sınır, önceki kapanış ve
    # AOF'nin dışından ölçülür ve pay %1'dir. Gerçek veri: ASLAN 04.10.2010 560 → 450, H = L (−%19,6); DENIZ 25.05.2012
    # kapanış 17,75, AOF 16,39 → 14,20 (−%20). İkisi de kilitli taban günüdür, aşım değil. H = L +%21 gün de kilittir.
    def ek(**alan):  # ham ve düzeltilmiş alan aynı (çarpan 1)
        return {on + a: v for a, v in alan.items() for on in ("ham_", "")}

    def yol(ad, onceki, gun, onceki_ek=None, gun_ek=None):
        o = satir("2012-05-24", onceki, onceki) | (onceki_ek or {})
        s = satir("2012-05-25", gun, gun) | (gun_ek or {})
        return anlik(tmp_path / ad, fiyat=[o, s], olay=[]).gun_tablosu

    g = yol("aslan", 560.0, 450.0)
    assert g["karantina"].tolist() == [False, False]
    assert g["kilit_taban_duyarli"].tolist() == [False, True]
    deniz = ek(aof=16.39, dusuk=16.39), ek(aof=14.38, yuksek=15.95)
    g = yol("deniz", 17.75, 14.20, *deniz)
    assert g["karantina"].tolist() == [False, False]
    g = yol("tavan", 10.0, 12.10)
    assert g["karantina"].tolist() == [False, False]
    assert g["kilit_tavan_duyarli"].tolist() == [False, True]
    # Kilit de iki bazdan ölçülür: önceki AOF'nin ±%10'unda H = L kapanış kilittir (kapanışın ±%10'una varmasa da).
    g = yol("aof_tavan", 10.0, 10.45, ek(aof=9.50, dusuk=9.50))
    assert g["kilit_tavan_duyarli"].tolist() == [False, True]
    g = yol("aof_taban", 10.0, 9.45, ek(aof=10.50, yuksek=10.50))
    assert g["kilit_taban_duyarli"].tolist() == [False, True]


def test_dort_ondaliga_yuvarli_dusuk_fiyatli_kapanis_bozuk_sayilmaz(tmp_path):
    # TASARIM 5.13: HGDG_KAPANIS 4 ondalığa yuvarlı, HGDG_MIN ve HGDG_MAX değil. Gerçek veri AKFGY 17.01.2014: ham
    # kapanış = ham düşük = 1,19; düzeltilmiş kapanış 0,4082 < düzeltilmiş düşük 0,408246 (fark 0,000046). Bağıl
    # 1e-4 pay 0,5 TL altında yarım birimi (0,00005) karşılamaz. Gerçek ihlal (0,4076, düşükten %0,16 aşağı) bozuk kalır.
    def gun(tarih, kapanis):
        return {
            **satir(tarih, 1.19, 0.408246),
            "ham_yuksek": 1.23,
            "yuksek": 0.421968,
            "kapanis": kapanis,
        }

    a = anlik(
        tmp_path,
        fiyat=[
            gun("2024-01-02", 0.408246),
            gun("2024-01-03", 0.4082),
            gun("2024-01-04", 0.4076),
            # Üst sınır: ham kapanış = ham yüksek; düzeltilmiş kapanış 0,4083 > düzeltilmiş yüksek 0,408254 (fark 0,000046).
            {**gun("2024-01-05", 0.4083), "ham_yuksek": 1.19, "yuksek": 0.408254},
        ],
        olay=[],
    )
    assert a.gun_tablosu["bozuk"].tolist() == [False, False, True, False]
    assert _karantina(a) == [False, False, True, False]


def test_islemsiz_gun_fiyatsiz_gundur_karantina_acmaz(tmp_path):
    # Kaynak işlemsiz günü hacim 0, ham AOF = yüksek = düşük = 0 ve önceki kapanışla verir (CLKHO 13.10.2015). TASARIM
    # 5.13 "sıfır hacim sıradan işlemsiz gündür"; SPEC 3.9 istisnası (Levent 30.10.2026). Aynı satır hacimliyse bozuktur.
    def tablo(hacim, sifir=("aof", "yuksek", "dusuk")):
        sifirlar = {on + s: 0.0 for s in sifir for on in ("ham_", "")}
        gun = {**satir("2024-01-03", 10.0, 10.0), **sifirlar, "hacim": hacim}
        g = anlik(
            tmp_path / f"{hacim}-{'-'.join(sifir)}",
            fiyat=[
                satir("2024-01-02", 10.0, 10.0),
                gun,
                satir("2024-01-04", 10.5, 10.5),
            ],
            olay=[],
        )
        return g.gun_tablosu, g.hesap_fiyati

    g, f = tablo(0.0)
    assert g["eksik"].tolist() == [False, True, False]
    assert not g["bozuk"].any() and not g["karantina"].any()
    assert f["kapanis"].isna().tolist() == [False, True, False]
    g, _ = tablo(500.0)
    assert g["bozuk"].tolist() == [False, True, False]
    assert g["karantina"].tolist() == [False, True, False]
    # Fiyatlı işlemsiz gün (H = L = kapanış > 0) fiyatını korur; yalnız AOF'si 0 olan satır kısmi satırdır, bozuktur.
    g, f = tablo(0.0, sifir=())
    assert not g["eksik"].any() and not g["bozuk"].any()
    assert f["kapanis"].notna().all()
    g, _ = tablo(0.0, sifir=("aof",))
    assert g["bozuk"].tolist() == [False, True, False]


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


def test_yalniz_aofsi_bozuk_satirin_kapanisi_ertesi_gunun_limit_bazidir(tmp_path):
    # 16.09.2026'da 126 satırın ham AOF'si [düşük, yüksek] dışında, kapanışı tutarlı; 17.09'da bunların 55'i iki günlük
    # hareketle (54 düşüş, 1 yükseliş) sahte aşım oldu. d2 bozuk (AOF 95 > yüksek 93) ama ham kapanış 92 düşük-yüksek aralığında: d3 tabanı
    # 92 × 0,90 = 82,8; d3 kapanışı 84 limit içinde, karantina yok (d1'den ölçülse taban 90 olur, 84 aşım sayılırdı).
    bozuk = {**satir("2024-01-03", 92.0, 92.0), "ham_aof": 95.0, "aof": 95.0}
    bozuk |= {"ham_yuksek": 93.0, "yuksek": 93.0, "ham_dusuk": 91.0, "dusuk": 91.0}
    a = anlik(
        tmp_path,
        fiyat=[
            satir("2024-01-02", 100.0, 100.0),
            bozuk,
            satir("2024-01-04", 84.0, 84.0),
        ],
        olay=[],
    )
    assert a.gun_tablosu["bozuk"].tolist() == [False, True, False]
    assert _karantina(a) == [False, True, False]
    assert a.gun_tablosu["taban"].iloc[2] == pytest.approx(82.8)


@pytest.mark.parametrize(
    "ihlal", [{"ham_yuksek": 140.0}, {"ham_dusuk": 0.0, "dusuk": 0.0}]
)
def test_ham_kapanisi_tutarsiz_bozuk_satir_limit_bazi_olmaz(tmp_path, ihlal):
    # Ham kapanış yüksekten büyük (150 > 140) ya da ham düşük 0: kapanış güvenilmez, baz d1'in 100'üdür. d3 tavanı
    # 100 × 1,10 = 110; d3 kapanışı 160 > 110 × 1,005, karantina (d2 baz olsaydı tavan 165 olur, 160 temiz kalırdı).
    a = anlik(
        tmp_path,
        fiyat=[
            satir("2024-01-02", 100.0, 100.0),
            {**satir("2024-01-03", 150.0, 150.0), **ihlal},
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
