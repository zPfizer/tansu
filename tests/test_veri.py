"""`veri` yüzü: sahte kaynaktan anlık görüntü üretme, okuma, olay denetimi.

Fiyatlar CCOLA'nın İş Yatırım'daki gerçek değerleridir (08–15.08.2024). Olay çarpanları
`GetSermayeArttirimlari`'ndan alındı. Beklenen değerler elle hesaplandı (yorumlarda).
"""

import datetime as dt
import json

import pandas as pd
import pytest

from tansu import veri

# Olay tarihi: SHHE_TARIH, ms epoch, İstanbul gece yarısı (UTC 21:00, önceki gün).
def epoch(gun):
    return int(dt.datetime(gun.year, gun.month, gun.day, tzinfo=dt.timezone(dt.timedelta(hours=3))).timestamp() * 1000)


def satir(tarih, ham, duz):
    return {"tarih": pd.Timestamp(tarih), "ham_kapanis": ham, "kapanis": duz,
            "ham_aof": ham, "ham_yuksek": ham, "ham_dusuk": ham, "aof": duz, "yuksek": duz, "dusuk": duz,
            "hacim": 1.0, "pd": 1.0, "hao_pd": 1.0, "sermaye": 1.0, "xu100": 1.0}


CCOLA_FIYAT = [
    satir("2024-08-08", 757.5, 66.3352),
    satir("2024-08-09", 757.5, 66.3352),
    satir("2024-08-12", 760.5, 66.5979),
    satir("2024-08-13", 69.35, 66.8037),
    satir("2024-08-14", 67.75, 65.2624),
    satir("2024-08-15", 67.6, 65.1179),
]
CCOLA_OLAY = [
    {"SHT_KODU": "02", "SHHE_TARIH": epoch(dt.date(2024, 8, 13)), "SHHE_FIYAT_AYAR_OR": 0.09090909138724523},
    {"SHT_KODU": "04", "SHHE_TARIH": epoch(dt.date(2025, 5, 26)), "SHHE_FIYAT_AYAR_OR": 0.9792410463023796},
    {"SHT_KODU": "04", "SHHE_TARIH": epoch(dt.date(2026, 5, 12)), "SHHE_FIYAT_AYAR_OR": 0.9837037037037037},
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
    bozuk[1]["kapanis"] = 70.0  # 09.08: 70/757,5 = 0,09241; beklenen 0,08757 → fark %5,5
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
    once = [{"SHT_KODU": "04", "SHHE_TARIH": epoch(dt.date(2024, 8, 7)), "SHHE_FIYAT_AYAR_OR": 0.5}, *CCOLA_OLAY]
    a = anlik(tmp_path, olay=once)
    assert a.olay_uyarilari.empty


def test_bozuk_manifest_hata_verir(tmp_path):
    k = SahteKaynak({"CCOLA": CCOLA_FIYAT}, {"CCOLA": CCOLA_OLAY})
    kimlik = veri.indir(["CCOLA"], tmp_path, k, simdi=SIMDI)
    dosya = next(p for p in (tmp_path / "ag" / kimlik).iterdir() if p.suffix == ".parquet")
    dosya.write_bytes(dosya.read_bytes() + b"x")
    with pytest.raises(veri.VeriHatasi):
        veri.oku(kimlik, tmp_path)


def test_anlik_goruntu_kimligi_tarihli_ve_olay_ham_json_saklanir(tmp_path):
    k = SahteKaynak({"CCOLA": CCOLA_FIYAT}, {"CCOLA": CCOLA_OLAY})
    kimlik = veri.indir(["CCOLA"], tmp_path, k, simdi=SIMDI)
    assert kimlik == "20261005-1930"
    ham = json.loads((tmp_path / "ag" / kimlik / "olaylar.json").read_text(encoding="utf-8"))
    assert ham["CCOLA"] == CCOLA_OLAY
    assert not any(p.name.startswith("_") for p in (tmp_path / "ag").iterdir())
