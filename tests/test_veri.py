"""`veri` yüzü: sahte kaynaktan anlık görüntü üretme, okuma, olay denetimi.

Fiyatlar CCOLA'nın İş Yatırım'daki gerçek değerleridir (08–15.08.2024). Olay çarpanları
`GetSermayeArttirimlari`'ndan alındı. Beklenen değerler elle hesaplandı (yorumlarda).
"""

import datetime as dt
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


def _sektor_anlik(tmp_path, semboller=("A", "B", "C", "D")):
    k = SahteKaynak(
        {s: CCOLA_FIYAT for s in semboller}, {s: CCOLA_OLAY for s in semboller}
    )
    return veri.indir(list(semboller), tmp_path, k, simdi=SIMDI, borsapy=_YalnizA())


def test_sektor_tamamla_yeni_anlik_goruntu_yazar_eskisi_degismez(tmp_path):
    # A zaten var (korunur, sorulmaz). B, C sektör alır; D KAP listesinde yok (None) → sektörsüz, kapsamda yazılır.
    eski = _sektor_anlik(tmp_path)
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
