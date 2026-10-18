"""`evren` yüzü: ay başı sıralama, geleceği görmeme, likidite eleği, tek kod, kapanma (TASARIM 5.2).

Sentetik anlık görüntü; `kosu` (bilet 09) henüz yok, bu yüzden en yüksek yüz `evren(anlik, tarih)`.
Takvim 2026-01-01 .. 2026-04-30 iş günleridir (86 gün, tatil yok). Elle hesaplanan dizinler:
Ocak 0-21 (09.01 = 6), Şubat 22-41, Mart 42-63 (31.03 = 63), Nisan 64-85 (01.04 = 64, 06.04 = 67).
"""

import pandas as pd
import pytest

from tansu import evren as ev
from tansu.veri import Anlik
from tansu import veri

TAKVIM = pd.bdate_range("2026-01-01", "2026-04-30")
NISAN = pd.Timestamp("2026-04-01")


def test_resmi_bist30_degisim_gununde_yeni_liste_ve_kaynak():
    # Kaynak CSV: MGROS bitis=2021-04-01, SASA baslangic=2021-04-01.
    yanit = veri.uyelik_hazirla(
        veri.UyelikIstegi(
            ("2021-03-31", "2021-04-01"), "donemsel_bist30_v1", "bist30_2021_2025_v1"
        )
    )
    assert set(yanit["gunler"]) == {"2021-03-31", "2021-04-01"}
    once, sonra = (yanit["gunler"][t] for t in ("2021-03-31", "2021-04-01"))
    assert len(once["semboller"]) == len(sonra["semboller"]) == 30
    assert set(sonra["semboller"]) - set(once["semboller"]) == {"SASA"}
    assert set(once["semboller"]) - set(sonra["semboller"]) == {"MGROS"}
    kanit = next(k for k in sonra["kanitlar"] if k["sembol"] == "SASA")
    assert kanit["kaynak_id"] == "2021Q2"
    assert kanit["yururluk_baslangici"] == "2021-04-01"
    assert kanit["yururluk_bitisi"] == "2025-12-31"


def test_bist30_eksik_gunlerin_tamami_ve_surum_hatada():
    with pytest.raises(veri.VeriHatasi) as hata:
        veri.uyelik_hazirla(
            veri.UyelikIstegi(
                ("2020-12-31", "2021-01-01", "2025-12-31", "2026-01-01"),
                "donemsel_bist30_v1",
                "bist30_2021_2025_v1",
            )
        )
    assert hata.value.eksik_tarihler == ["2020-12-31", "2026-01-01"]
    assert "bist30_2021_2025_v1" in str(hata.value)


@pytest.mark.parametrize("bozuk", ["eksik_uye", "cakisma", "kaynak", "aralik"])
def test_bist30_bozuk_kayitla_kosu_baslamaz(monkeypatch, bozuk):
    oku = pd.read_csv

    def bozuk_oku(*args, **kwargs):
        t = oku(*args, **kwargs)
        if bozuk == "eksik_uye":
            return t[t["sembol"] != "AKBNK"]
        if bozuk == "cakisma":
            return pd.concat([t, t[t["sembol"] == "AKBNK"]], ignore_index=True)
        t.loc[t["sembol"] == "AKBNK", "kaynak_id" if bozuk == "kaynak" else "bitis"] = (
            "" if bozuk == "kaynak" else "2020-01-01"
        )
        return t

    monkeypatch.setattr(pd, "read_csv", bozuk_oku)
    with pytest.raises(veri.VeriHatasi):
        veri.uyelik_hazirla(
            veri.UyelikIstegi(
                ("2021-02-05",), "donemsel_bist30_v1", "bist30_2021_2025_v1"
            )
        )


def anlik(semboller):
    """semboller: ad -> dict(pd, hacim, bas=0, son=85, ozel={tarih: pd}, bos=[dizinler])."""
    satirlar = []
    for ad, s in semboller.items():
        for i, gun in enumerate(TAKVIM):
            if i < s.get("bas", 0) or i > s.get("son", 85) or i in s.get("bos", ()):
                continue
            pdeger = s.get("ozel", {}).get(str(gun.date()), s["pd"])
            satirlar.append(
                {
                    "sembol": ad,
                    "tarih": gun,
                    "ham_kapanis": 10.0,
                    "pd": pdeger,
                    "hacim": s["hacim"],
                    "xu100": 1.0,
                }
            )
    olaylar = pd.DataFrame(columns=["sembol", "tarih", "kod", "carpan"])
    return Anlik("sentetik", pd.DataFrame(satirlar), olaylar)


def test_ay_basi_siralama_onceki_ay_sonu_piyasa_degeri():
    a = anlik(
        {
            "A": dict(pd=100, hacim=1e6),
            "B": dict(pd=300, hacim=1e6),
            "C": dict(pd=200, hacim=1e6),
            "D": dict(pd=50, hacim=1e6),
        }
    )
    # en büyük 3, büyükten küçüğe; D en küçük olduğu için dışarıda
    assert ev.evren(a, NISAN, en_buyuk=3, elenen=0) == ["B", "C", "A"]
    # ay içindeki başka bir gün aynı ay başı listesini verir
    assert ev.evren(a, pd.Timestamp("2026-04-15"), en_buyuk=3, elenen=0) == [
        "B",
        "C",
        "A",
    ]


def test_gelecegi_gormez_onceki_ay_sonu_degeri_kullanilir():
    a = anlik(
        {
            "A": dict(pd=100, hacim=1e6),
            # 31.03'te (dizin 63) 90, 01.04'ten sonra 1000: 31.03 değeri geçerli, A'dan küçük
            "F": dict(pd=90, hacim=1e6, ozel={"2026-04-01": 1000, "2026-04-02": 1000}),
            # 30.03'te 500 ama 31.03'te 80: ay sonu değeri geçerli
            "G": dict(pd=80, hacim=1e6, ozel={"2026-03-30": 500}),
        }
    )
    assert ev.evren(a, NISAN, en_buyuk=2, elenen=0) == ["A", "F"]


def test_likidite_elegi_en_alttaki_yuzde_yirmi():
    # 10 hisse; piyasa değeri hacimle ters: en büyük MV en az likit. Medyan hacim 1e6..10e6.
    semboller = {f"S{i}": dict(pd=100 - i, hacim=(i + 1) * 1e6) for i in range(10)}
    sonuc = ev.evren(anlik(semboller), NISAN)
    # alttaki %20 = 2 hisse (hacim 1e6, 2e6 = S0, S1) elenir; kalan 8, MV sırası S2..S9
    assert sonuc == [f"S{i}" for i in range(2, 10)]


def test_likidite_medyani_son_60_gunle_sinirli():
    # Son 60 gün = dizin 4..63. S0'ın hacmi dizin 0-3'te 1e9 (pencere dışı), sonra 1e6: medyan 1e6.
    semboller = {f"T{i}": dict(pd=10 + i, hacim=(i + 2) * 1e7) for i in range(8)}
    b = anlik(
        {**semboller, "S0": dict(pd=100, hacim=1e6), "S1": dict(pd=90, hacim=5e6)}
    )
    b.fiyat.loc[
        (b.fiyat["sembol"] == "S0") & (b.fiyat["tarih"] <= TAKVIM[3]), "hacim"
    ] = 1e9
    # 10 hisse: elenen 2 = en düşük medyan: S0 (1e6) ve S1 (5e6); 1e9 ilk günler medyanı etkilemez
    assert "S0" not in ev.evren(b, NISAN) and "S1" not in ev.evren(b, NISAN)
    assert len(ev.evren(b, NISAN)) == 8


def test_sirket_basina_tek_kod_hacmi_yuksek_kalir():
    a = anlik(
        {
            "X1": dict(pd=500, hacim=2e6),
            "X2": dict(pd=400, hacim=9e6),
            "Y": dict(pd=100, hacim=1e6),
        }
    )
    assert ev.evren(a, NISAN, elenen=0, coklu=[("X1", "X2")]) == ["X2", "Y"]


def test_islem_gormeyen_ve_kapanan_evrende_yok():
    a = anlik({"A": dict(pd=100, hacim=1e6), "Z": dict(pd=900, hacim=1e6, son=6)})
    assert ev.evren(a, NISAN, elenen=0) == ["A"]


def test_kapanma_60_gunden_uzun_durdurma():
    a = anlik(
        {
            "A": dict(pd=1, hacim=1e6),
            "Z": dict(pd=1, hacim=1e6, son=6),  # 09.01'den sonra hiç yok
            "Y60": dict(
                pd=1, hacim=1e6, bos=range(7, 67)
            ),  # 60 gün durdu, 06.04'te döndü
            "Y61": dict(pd=1, hacim=1e6, bos=range(7, 68)),  # 61 gün durdu
        }
    )
    k = ev.kapananlar(a).set_index("sembol")
    assert sorted(k.index) == ["Y61", "Z"]
    # son işlem dizin 6, 61. işlemsiz gün dizin 67 = 06.04.2026
    assert k.loc["Z", "kapanma_gunu"] == pd.Timestamp("2026-04-06")
    assert k.loc["Y61", "kapanma_gunu"] == pd.Timestamp("2026-04-06")
    assert k.loc["Z", "son_islem"] == pd.Timestamp("2026-01-09")
    assert k.loc["Z", "getiri"] == -1.0


def test_kapanma_nedeni_biliniyorsa_son_fiyat():
    a = anlik({"A": dict(pd=1, hacim=1e6), "Z": dict(pd=1, hacim=1e6, son=6)})
    k = ev.kapananlar(a, nedeni_bilinen={"Z"}).set_index("sembol")
    assert pd.isna(k.loc["Z", "getiri"])  # NaN = son fiyat kullanılır


def test_sembol_listesi_bugunku_paylar_ve_kapananlarin_birlesimi_tekrarsiz():
    kapanan = pd.DataFrame(
        {"kod": ["OLMK", "THYAO", "ROYAL"]}
    )  # THYAO yeniden kotlanmış gibi iki listede
    assert ev.tum_semboller(["THYAO", "AKBNK"], kapanan) == [
        "AKBNK",
        "OLMK",
        "ROYAL",
        "THYAO",
    ]
