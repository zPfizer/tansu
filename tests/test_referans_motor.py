"""Bağımsız referanslarla fark testi. Referanslar SPEC 5.1-5.4 ve SPEC 11 madde 1'den yazıldı, ürün kodunu çağırmaz;
aynı tohumlu rastgele girdide ürünle alan alan karşılaştırılır. SPEC'in sustuğu yerlerin kararları tests/test_islem.py
test adlarındadır; referans onları izler."""

import math
from collections import Counter

import numpy as np
import pandas as pd
import pytest

from tansu import islem, sinama, yapi
from tansu.strateji import bos_sinyal
from tansu.stratejiler import STRATEJILER, gartley
from tests.sentetik import SABIT, rastgele_tablo

MALIYET = 0.0015 * 1.05  # taraf başına komisyon ve BSMV (SPEC 5.3)
TABAN = 0.5  # risk tabanı, ATR katı (SPEC 5.2)
CIKISLAR = {
    "dokunus, iki yarım hedef": islem.Cikis(
        "dokunus", (("hedef1", 0.5), ("hedef2", 0.5))
    ),
    "kapanis, hedefsiz": islem.Cikis("kapanis"),
    "dokunus, üç hedef, artık pay": islem.Cikis(
        "dokunus", (("hedef1", 0.3), ("hedef2", 0.3), ("hedef3", 0.3))
    ),
}
DOLUM_TOHUMLARI = range(12)
GARTLEY_TOHUMLARI = range(100, 120)


# --- Dolum ve çıkış referansı (SPEC 5.1-5.4) ---


def referans_motor(gun: pd.DataFrame, sinyal: pd.DataFrame, cikis: islem.Cikis):
    """Günleri bir kez yürür; her gün önce bekleyen emri ya da açık işlemi, sonra o günün sinyalini işler.

    Dönen: işlemler (ürün kaydının alan adlarıyla), red sayaçları ve hangi kural yolunun çalıştığını sayan kapsam."""
    tarih = gun.index
    aof, yuk, dus, kap, atr = (
        gun[c].to_numpy(float) for c in ("aof", "yuksek", "dusuk", "kapanis", "atr")
    )
    tavan, taban, karantina = (
        gun[c].to_numpy(bool) for c in ("kilit_tavan", "kilit_taban", "karantina")
    )
    cikis_sinyali = sinyal["cikis_sinyali"].to_numpy(bool)
    red = Counter({islem.AYNI_GUN: int(sinyal["tekrar"].sum())})
    kapsam: Counter = Counter()
    islemler: list[dict] = []
    emir = poz = None
    son_fiyatli = -1

    def emir_gunu(d):
        """None: emir bekler; float: dolum fiyatı; str: emir düştü, neden."""
        if emir["tur"] == "piyasa":
            if not (math.isfinite(kap[d]) and math.isfinite(aof[d])):
                return None
            return islem.TAVAN_KILIDI if tavan[d] else aof[d]
        seviye = emir["seviye"]
        if math.isfinite(kap[d]):
            if not tavan[d] and yuk[d] < seviye:
                kapsam["limit AOF dolumu"] += 1
                return aof[d]
            if not tavan[d] and dus[d] <= seviye:
                kapsam["limit seviyeye eşit dip"] += dus[d] == seviye
                return seviye
            if kap[d] < emir["stop"]:
                return islem.STOP_KAPANISI
        return islem.SURE_DOLDU if d == emir["son"] else None

    def kapat(d, fiyat, neden):
        poz["parcalar"].append((d, fiyat, poz["kalan"], neden))
        return True

    def islem_gunu(d):
        """SPEC 5.4 adım sırası; işlem kapanınca True."""
        stop, ilk = poz["stop"], d == poz["dolum"]
        if cikis.stop_mod == "kapanis" and kap[d] < stop:
            yarin = "stop (kapanış)"
        else:
            yarin = islem.CIKIS_SINYALI if cikis_sinyali[d] else None
        dokunus = cikis.stop_mod == "dokunus"
        if taban[d]:
            if ilk and poz["giris"] <= stop:
                poz["bekleyen"] = "stop (dolumda)"
            elif poz["bekleyen"] is None:
                poz["bekleyen"] = "stop" if dokunus and dus[d] <= stop else yarin
            kapsam["taban kilidinde bekleyen çıkış"] += poz["bekleyen"] is not None
            return False
        if ilk and poz["giris"] <= stop:
            return kapat(d, poz["giris"], "stop (dolumda)")
        if ilk:
            if dokunus and dus[d] <= stop:
                return kapat(d, stop, "stop")
            poz["bekleyen"] = yarin
            return False
        if poz["bekleyen"] is not None:
            return kapat(d, aof[d], poz["bekleyen"])
        if dokunus and yuk[d] < stop:
            return kapat(d, aof[d], "stop")
        if dokunus and dus[d] <= stop:
            kapsam["stopa eşit dip"] += dus[d] == stop
            return kapat(d, stop, "stop")
        for ad, pay in cikis.hedef:
            seviye = poz["hedefler"][ad]
            if ad in poz["dolan"] or math.isnan(seviye):
                continue
            if dus[d] > seviye:
                fiyat = aof[d]
            elif yuk[d] >= seviye:
                fiyat = seviye
            else:
                break
            pay = min(pay, poz["kalan"])
            poz["kalan"] -= pay
            poz["dolan"].add(ad)
            poz["parcalar"].append((d, fiyat, pay, ad))
            if poz["kalan"] <= 1e-12:
                return True
        poz["bekleyen"] = yarin
        return False

    def kayit():
        giris, stop, t, parcalar = poz["giris"], poz["stop"], poz["t"], poz["parcalar"]
        ham_risk = giris - stop
        risk = max(ham_risk, TABAN * atr[t]) if math.isfinite(stop) else math.nan
        kar = sum(
            pay * (f - giris - (giris + f) * MALIYET) for _, f, pay, _ in parcalar
        )
        son_gun, son_fiyat, _, neden = parcalar[-1]
        dolum = poz["dolum"]
        ileri = {}
        for n in (1, 3, 5, 10):  # SPEC 5.2: dolumdan sonraki n. günün kapanışına net %
            c = kap[dolum + n] if dolum + n < len(kap) else math.nan
            ileri[f"getiri_{n}"] = (c - giris - (giris + c) * MALIYET) / giris * 100
        tam = dolum + 10 < len(kap)  # MFE/MAE yalnız dolumdan sonraki tam 10 günde
        tepe = uc(yuk, dolum + 1, dolum + 11, max) if tam else None
        dip = uc(dus, dolum + 1, dolum + 11, min) if tam else None
        mfe = math.nan if tepe is None else tepe - giris
        mae = math.nan if dip is None else giris - dip
        return {
            **ileri,
            "mfe_yuzde": mfe / giris * 100,
            "mae_yuzde": mae / giris * 100,
            "mfe_R": mfe / risk,
            "mae_R": mae / risk,
            "tutma_gun": son_gun - dolum,
            "stop_gun": son_gun - dolum if neden.startswith("stop") else math.nan,
            **{
                f"{ad}_gun": next(
                    (g - dolum for g, _, _, n in parcalar if n == ad), math.nan
                )
                for ad, _ in cikis.hedef
            },
            "sinyal_tarihi": tarih[t],
            "dolum_tarihi": tarih[poz["dolum"]],
            "dolum_fiyati": giris,
            "cikis_tarihi": tarih[son_gun],
            "cikis_fiyati": son_fiyat,
            "cikis_nedeni": neden,
            "kismi": "; ".join(
                f"{tarih[g].date()} {n} {f:.4f} x{pay:g}"
                for g, f, pay, n in parcalar[:-1]
            ),
            "R": kar / risk,
            "net_yuzde": kar / giris * 100,
            "risk_tabanli": ham_risk <= TABAN * atr[t],
            "dolumda_stop": neden == "stop (dolumda)",
            "acik": neden == "açık",
        }

    for d in range(len(tarih)):
        if math.isfinite(kap[d]):
            son_fiyatli = d
        if emir is not None:
            sonuc = emir_gunu(d)
            if isinstance(sonuc, str):
                red[sonuc] += 1
                emir = None
            elif sonuc is not None:
                poz = {
                    "t": emir["t"],
                    "dolum": d,
                    "giris": float(sonuc),
                    "stop": emir["stop"],
                    "hedefler": emir["hedefler"],
                    "kalan": 1.0,
                    "dolan": set(),
                    "parcalar": [],
                    "bekleyen": None,
                }
                emir = None
        if poz is not None and math.isfinite(kap[d]) and islem_gunu(d):
            islemler.append(kayit())
            poz = None
        if not sinyal["giris"].iat[d]:
            continue
        satir = sinyal.iloc[d]
        tur, stop = satir["giris_tur"], float(satir["stop"])
        referans = float(satir["seviye"]) if tur == "limit" else kap[d]
        hedefler = {h: float(satir[h]) for h in islem.HEDEFLER}
        if karantina[d]:
            red[islem.KALITE] += 1
        elif emir is not None or poz is not None:
            red[islem.ACIK_VAR] += 1
        elif math.isfinite(stop) and not stop < referans:
            red[islem.STOP_USTTE] += 1
        elif math.isfinite(stop) and not atr[d] > 0:
            red[islem.ATR_YOK] += 1
        elif cikis.hedef and all(math.isnan(hedefler[h]) for h, _ in cikis.hedef):
            red[islem.HEDEF_YOK] += 1
        else:
            emir = {
                "t": d,
                "tur": tur,
                "seviye": float(satir["seviye"]),
                "son": d + int(satir["gecerlilik"]),
                "stop": stop,
                "hedefler": hedefler,
            }
    if emir is not None:
        red[islem.VERI_SONU] += 1
    if poz is not None:
        d = son_fiyatli
        poz["parcalar"].append((d, kap[d], poz["kalan"], "açık"))
        islemler.append(kayit())
    return islemler, red, kapsam


def rastgele_girdi(tohum):
    """Rastgele tablo ve sinyal çerçevesi: limit ve piyasa, bazen referansın üstünde stop, NaN hedef, rastgele geçerlilik
    ve çıkış sinyali. Seviyelerin bir kısmı gelecekteki gerçek bir dip ya da tepedir, böylece eşit dokunuş da sınanır."""
    r = np.random.default_rng(tohum)
    gun = rastgele_tablo(tohum, n=500)
    gun["karantina"] = r.random(len(gun)) < 0.05
    yuk, dus, kap = (gun[c].to_numpy(float) for c in ("yuksek", "dusuk", "kapanis"))
    s = bos_sinyal(gun.index)
    s["cikis_sinyali"] = r.random(len(gun)) < 0.03

    def gelecek(dizi, t, ufuk):
        x = dizi[t + 1 : t + 1 + ufuk]
        x = x[np.isfinite(x)]
        return float(r.choice(x)) if len(x) else math.nan

    fiyatli = np.flatnonzero(np.isfinite(kap))
    for t in fiyatli[r.random(len(fiyatli)) < 0.1]:
        gecerlilik = int(r.integers(1, 12))
        limit = r.random() < 0.6
        seviye = math.nan
        if limit:
            seviye = gelecek(dus, t, gecerlilik) if r.random() < 0.3 else math.nan
            if not seviye < kap[t]:
                seviye = kap[t] * r.uniform(0.9, 1.0)
        referans = seviye if limit else kap[t]
        zar = r.random()
        if zar < 0.05:
            stop = math.nan
        elif zar < 0.12:
            stop = referans * r.choice([1.0, r.uniform(1.0, 1.02)])
        else:
            stop = gelecek(dus, t, 20) if zar < 0.35 else math.nan
            if not stop < referans:
                stop = referans * r.uniform(0.85, 0.995)
        hedef = referans * np.cumprod(1 + r.uniform(0.01, 0.06, 4))
        ilk = gelecek(yuk, t, 20)
        if r.random() < 0.3 and ilk > referans:
            hedef[0] = ilk
        hedef[r.random(4) < 0.15] = math.nan
        if r.random() < 0.05:
            hedef[:] = math.nan
        s.iloc[
            t,
            s.columns.get_indexer(
                ["giris", "giris_tur", "seviye", "gecerlilik", "stop"]
            ),
        ] = [
            True,
            "limit" if limit else "piyasa",
            seviye,
            gecerlilik,
            stop,
        ]
        s.iloc[t, s.columns.get_indexer(list(islem.HEDEFLER))] = hedef
        if r.random() < 0.1:
            s.iloc[t, s.columns.get_loc("tekrar")] = int(r.integers(1, 3))
    return gun, s


TAM_ALANLAR = [
    "sinyal_tarihi",
    "dolum_tarihi",
    "dolum_fiyati",
    "cikis_tarihi",
    "cikis_fiyati",
    "cikis_nedeni",
    "kismi",
    "risk_tabanli",
    "dolumda_stop",
    "acik",
    "tutma_gun",
]
YAKIN_ALANLAR = [
    "R",
    "net_yuzde",
    *(f"getiri_{n}" for n in (1, 3, 5, 10)),
    "mfe_yuzde",
    "mae_yuzde",
    "mfe_R",
    "mae_R",
    "stop_gun",
]


def test_motor_bagimsiz_dolum_referansiyla_ayni_islemleri_ve_red_sayilarini_verir():
    nedenler, redler, kapsam = Counter(), Counter(), Counter()
    for ad, cikis in CIKISLAR.items():
        for tohum in DOLUM_TOHUMLARI:
            gun, s = rastgele_girdi(tohum)
            motor, motor_red = islem.simule(
                gun, s, cikis, sembol="R", strateji="t", sinif="a"
            )
            ref, ref_red, ref_kapsam = referans_motor(gun, s, cikis)
            durum = f"{ad}, tohum {tohum}"
            assert +motor_red == +ref_red, durum
            assert len(motor) == len(ref), durum
            for m, r in zip(motor, ref, strict=True):
                assert {a: m[a] for a in TAM_ALANLAR} == {
                    a: r[a] for a in TAM_ALANLAR
                }, durum
                for a in YAKIN_ALANLAR + [f"{ad}_gun" for ad, _ in cikis.hedef]:
                    assert m[a] == pytest.approx(
                        r[a], rel=1e-12, abs=1e-12, nan_ok=True
                    ), durum
            nedenler.update(r["cikis_nedeni"] for r in ref)
            nedenler.update(
                parca.split(" ")[1]
                for r in ref
                for parca in filter(None, r["kismi"].split("; "))
            )
            kapsam.update(ref_kapsam)
            kapsam["kısmi çıkış"] += sum(bool(r["kismi"]) for r in ref)
            kapsam["risk tabanı"] += sum(r["risk_tabanli"] for r in ref)
            redler += ref_red
    beklenen_neden = {
        "stop",
        "stop (dolumda)",
        "stop (kapanış)",
        islem.CIKIS_SINYALI,
        "açık",
    }
    assert beklenen_neden | {"hedef1", "hedef2", "hedef3"} <= set(nedenler), nedenler
    # STOP_KAPANISI burada oluşamaz: stop seviyenin altında, kilitsiz günde stopun altındaki kapanış önce emri doldurur.
    red_nedenleri = {
        islem.KALITE,
        islem.ACIK_VAR,
        islem.STOP_USTTE,
        islem.HEDEF_YOK,
        islem.SURE_DOLDU,
        islem.VERI_SONU,
        islem.AYNI_GUN,
        islem.TAVAN_KILIDI,
        islem.ATR_YOK,
    }
    assert red_nedenleri <= set(+redler), redler
    yollar = {
        "limit AOF dolumu",
        "limit seviyeye eşit dip",
        "stopa eşit dip",
        "taban kilidinde bekleyen çıkış",
        "kısmi çıkış",
        "risk tabanı",
    }
    assert yollar <= set(+kapsam), kapsam


# --- Gartley referansı (SPEC 11 madde 1, yerel kural kartı) ---


def referans_pivotlar(yuk, dus, k) -> list[tuple]:
    """(tür, pivot günü, onay günü, fiyat). Yalnız fiyatlı günler bar sayılır; pivot, ortası olduğu 2k+1 barlık pencerenin
    ilk en büyüğü (tepe) ya da ilk en küçüğüdür (dip); onay k. fiyatlı bardır. Sıra: onay, pivot, tür."""
    fiyatli = [
        i for i in range(len(yuk)) if math.isfinite(yuk[i]) and math.isfinite(dus[i])
    ]
    sonuc = []
    for j in range(k, len(fiyatli) - k):
        pencere = fiyatli[j - k : j + k + 1]
        tepeler = [yuk[i] for i in pencere]
        dipler = [dus[i] for i in pencere]
        gun, onay = fiyatli[j], fiyatli[j + k]
        if tepeler.index(max(tepeler)) == k:
            sonuc.append(("T", gun, onay, float(yuk[gun])))
        if dipler.index(min(dipler)) == k:
            sonuc.append(("D", gun, onay, float(dus[gun])))
    return sorted(sonuc, key=lambda p: (p[2], p[1], p[0]))


def uc(dizi, bas, son, secim):
    """[bas, son) içindeki fiyatlı değerlerin `secim`i (min ya da max); boş pencerede None."""
    degerler = [dizi[i] for i in range(bas, son) if math.isfinite(dizi[i])]
    return secim(degerler) if degerler else None


def referans_gartley(gun: pd.DataFrame, p, kapsam: Counter) -> dict[int, dict]:
    """Onay günü -> seviyeler. Boğa XABC: aynı türden daha uç pivot öncekinin yerine geçer; C onaylanınca son dört pivot
    Carney oranlarında ve her biri kendi bacağının ucuysa kurulum olur."""
    yuk, dus, atr = (gun[c].to_numpy(float) for c in ("yuksek", "dusuk", "atr"))
    k, tol = int(str(p["pivot"]).removeprefix("sag_bar_")), float(p["tolerans"])
    sira, sonuc = [], {}
    for piv in referans_pivotlar(yuk, dus, k):
        if sira and sira[-1][0] == piv[0]:
            daha_uc = piv[3] > sira[-1][3] if piv[0] == "T" else piv[3] < sira[-1][3]
            if not daha_uc:
                continue
            sira[-1] = piv
        else:
            sira.append(piv)
        if len(sira) < 4 or sira[-1][0] != "T":
            continue
        X, A, B, C = sira[-4:]
        x, a, b, c = X[3], A[3], B[3], C[3]
        if not x < b < c < a:
            continue
        d = a - 0.786 * (a - x)
        ab, bc, cd = (a - b) / (a - x), (c - b) / (a - b), (c - d) / (c - b)
        if not (
            abs(ab - 0.618) <= tol * 0.618
            and 0.382 * (1 - tol) <= bc <= 0.886 * (1 + tol)
            and 1.272 * (1 - tol) <= cd <= 1.618 * (1 + tol)
        ):
            continue
        t = C[2]
        en_dusuk_x = uc(dus, X[1] + 1, t + 1, min)
        en_yuksek_a = uc(yuk, X[1] + 1, B[1], max)
        en_dusuk_b = uc(dus, A[1] + 1, C[1], min)
        en_yuksek_c = uc(yuk, B[1] + 1, t + 1, max)
        if not (
            (en_dusuk_x is None or en_dusuk_x >= x)
            and (en_yuksek_a is None or en_yuksek_a <= a)
            and (en_dusuk_b is None or en_dusuk_b >= b)
            and (en_yuksek_c is None or en_yuksek_c <= c)
        ):
            kapsam["bacak ucu değil"] += 1
            continue
        stop = x if p["stop"] == "X" else x - 2 * atr[t]
        h1, h2 = d + 0.382 * (a - d), d + 0.618 * (a - d)
        if p["rr_min"] != "kapali" and (h1 - d) / (d - stop) < float(p["rr_min"]):
            kapsam["R/R kapısı"] += 1
            continue
        once = sonuc.get(t)
        tekrar = 0 if once is None else once["tekrar"] + 1
        if once is not None and d <= once["seviye"]:
            once["tekrar"] = tekrar
            continue
        dip = uc(dus, C[1] + 1, t + 1, min)
        sonuc[t] = {
            "seviye": d,
            "stop": stop,
            "hedef1": h1,
            "hedef2": h2,
            "hedef3": c,
            "tekrar": tekrar,
            "durum": "TAMAMLANDI" if dip is not None and dip <= d else "AKTIF",
        }
    return sonuc


@pytest.mark.parametrize("k", [3, 5, 15])
def test_sag_bar_pivotlari_kaba_kuvvet_pencere_taramasiyla_ayni(k):
    for tohum in GARTLEY_TOHUMLARI:
        g = rastgele_tablo(tohum, n=1500)
        motor = [
            (p.tur, p.pivot_gun, p.onay_gun, p.fiyat)
            for p in yapi.sag_bar_pivotlari(g["yuksek"], g["dusuk"], k)
        ]
        ref = referans_pivotlar(
            g["yuksek"].to_numpy(float), g["dusuk"].to_numpy(float), k
        )
        assert motor == ref, f"tohum {tohum}"


@pytest.mark.parametrize(
    ("pivot", "rr_min", "stop", "en_az", "yollar"),
    [
        ("sag_bar_3", "kapali", "X", 20, ("bacak ucu değil",)),
        ("sag_bar_3", 1.4, "X", 20, ("bacak ucu değil",)),
        ("sag_bar_5", "kapali", "X", 10, ("bacak ucu değil",)),
        ("sag_bar_5", 1.4, "X", 10, ("bacak ucu değil",)),
        ("sag_bar_5", "kapali", "X-2ATR", 10, ()),
        ("sag_bar_5", 1.4, "X-2ATR", 0, ("R/R kapısı",)),
        ("sag_bar_15", "kapali", "X", 5, ()),
        ("sag_bar_15", 1.4, "X", 5, ()),
    ],
)
def test_gartley_bagimsiz_bulucuyla_ayni_gun_ve_seviyeleri_verir(
    pivot, rr_min, stop, en_az, yollar
):
    p = {**SABIT["gartley"], "pivot": pivot, "rr_min": rr_min, "stop": stop}
    sayi, kapsam = 0, Counter()
    for tohum in GARTLEY_TOHUMLARI:
        g = rastgele_tablo(tohum, n=1500)
        s = gartley.STRATEJI.sinyal(g, p)
        motor = {
            int(t): {
                **{
                    a: float(s[a].iat[t])
                    for a in ("seviye", "stop", "hedef1", "hedef2", "hedef3")
                },
                "tekrar": int(s["tekrar"].iat[t]),
                "durum": s["durum"].iat[t],
            }
            for t in np.flatnonzero(s["giris"])
        }
        ref = referans_gartley(g, p, kapsam)
        assert set(np.flatnonzero(s["tekrar"])) <= set(motor), f"tohum {tohum}"
        assert motor.keys() == ref.keys(), f"tohum {tohum}"
        for t, m in motor.items():
            assert m == pytest.approx(ref[t], rel=1e-12), f"tohum {tohum}, gün {t}"
        sayi += len(ref)
    assert sayi >= en_az, f"{sayi} kurulum: test boş geçemez"
    assert set(yollar) <= set(kapsam), kapsam


OLCEK_PARAM = {"gartley": {"pivot": "sag_bar_5"}}


@pytest.mark.parametrize("ad", sorted(STRATEJILER))
@pytest.mark.parametrize("us", [-3, 4])
def test_fiyatlar_2_uzeri_k_ile_carpilinca_gunler_ve_r_ayni_seviyeler_olcekli(ad, us):
    strateji, p = STRATEJILER[ad], {**SABIT[ad], **OLCEK_PARAM.get(ad, {})}
    taban = {f"R{j}": rastgele_tablo(200 + j, n=1200) for j in range(4)}
    carpan = 2.0**us
    olcekli = {}
    for sembol, g in taban.items():
        g = g.copy()
        for c in (
            "aof",
            "yuksek",
            "dusuk",
            "kapanis",
            "ham_yuksek",
            "ham_dusuk",
            "ham_kapanis",
            "atr",
        ):
            g[c] = g[c] * carpan
        olcekli[sembol] = g
    donem = sinama.Donem(taban["R0"].index[0], taban["R0"].index[-1])
    k0 = sinama.calistir(strateji, taban, p, donem)
    k1 = sinama.calistir(strateji, olcekli, p, donem)
    assert len(k0.islemler) > 0
    pd.testing.assert_frame_equal(k0.sinyaller, k1.sinyaller)
    i0, i1 = k0.islemler, k1.islemler
    for a in (
        "sembol",
        "sinyal_tarihi",
        "dolum_tarihi",
        "cikis_tarihi",
        "cikis_nedeni",
    ):
        assert i0[a].tolist() == i1[a].tolist(), a
    for a in ("R", "net_yuzde"):
        np.testing.assert_allclose(i1[a], i0[a], rtol=1e-12, atol=1e-12)
    for a in (
        "dolum_fiyati",
        "cikis_fiyati",
        "seviye",
        "stop",
        "hedef1",
        "hedef2",
        "hedef3",
    ):
        np.testing.assert_allclose(i1[a], i0[a] * carpan, rtol=1e-12)
