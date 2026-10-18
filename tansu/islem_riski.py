"""E3: sürümlü risk bütçesi ve gerçekleşen dolum maliyeti (TASARIM 5.15 S08)."""

import math
from decimal import Decimal, DecimalException
from numbers import Real

RISK_SURUMU = "bagimsiz_risk_v1"
MASRAF_SURUMU = "komisyon_bsmv_v1"
RISK_ORANI = 0.02
KOMISYON_BSMV = 0.001575  # TASARIM 5.15: dağıtıcı girdisi; patron onayı bekliyor.


def _pozitif(x):
    return (
        isinstance(x, Real) and not isinstance(x, bool) and math.isfinite(x) and x > 0
    )


def _risk_nedeni(giris, ilk_stop, nominal_tutar, aile):
    if not _pozitif(giris) or not _pozitif(nominal_tutar):
        return "gecersiz_risk_girdisi"
    if aile == "cift_rotasyonu":
        return "risk_dayanagi_eksik"
    if not _pozitif(ilk_stop) or ilk_stop >= giris:
        return "gecersiz_risk_girdisi"
    return None


def _plan(giris, ilk_stop, nominal_tutar):
    giris, stop, nominal = (Decimal(str(x)) for x in (giris, ilk_stop, nominal_tutar))
    butce = nominal * Decimal(str(RISK_ORANI))
    c = Decimal(str(KOMISYON_BSMV))
    birim = giris - stop + c * (giris + stop)
    adet = int(butce // birim)
    planlanan = adet * birim
    sonuc = {
        "risk_butcesi": float(butce),
        "birim_risk": float(birim),
        "adet": adet,
        "planlanan_risk": float(planlanan),
        "ilk_risk": float(planlanan) if adet else None,
        "kullanilmayan_butce": float(butce - planlanan),
        "planlanan_giris_maliyeti": float(adet * giris * c),
        "planlanan_stop_maliyeti": float(adet * stop * c),
        "risk_nedeni": None if adet else "butce_yetersiz",
    }
    if not _pozitif(sonuc["birim_risk"]) or not _pozitif(sonuc["risk_butcesi"]):
        raise ValueError("risk hesabı sonlu ve pozitif değil")
    return sonuc


def boyutla(giris, ilk_stop, nominal_tutar, *, aile, risk_surumu):
    """Masraflı bütçeyi tam adede aşağı yuvarlar (TASARIM 5.15 S08)."""
    if risk_surumu != RISK_SURUMU:
        raise ValueError(f"bilinmeyen risk sürümü: {risk_surumu}")
    if aile not in ("ema_sikismasi", "cift_rotasyonu"):
        raise ValueError(f"bilinmeyen aile: {aile}")
    butce = nominal_tutar * RISK_ORANI if _pozitif(nominal_tutar) else None
    neden = _risk_nedeni(giris, ilk_stop, nominal_tutar, aile)
    sonuc = {
        "risk_surumu": risk_surumu,
        "nominal_tutar": nominal_tutar if _pozitif(nominal_tutar) else None,
        "risk_orani": RISK_ORANI,
        "risk_butcesi": butce,
        "adet": None,
        "planlanan_risk": None,
        "ilk_risk": None,
        "birim_risk": None,
        "kullanilmayan_butce": None,
        "planlanan_giris_maliyeti": None,
        "planlanan_stop_maliyeti": None,
        "net_r": None,
        "risk_nedeni": neden,
    }
    if neden is None:
        try:
            sonuc.update(_plan(giris, ilk_stop, nominal_tutar))
        except DecimalException, OverflowError, ValueError:
            sonuc["risk_nedeni"] = "gecersiz_risk_girdisi"
    return sonuc


def fiyat_getirisi(giris, cikis, masraf):
    """Eski masraflı fiyat getirisi; skaler ve dizi aritmetiğini korur (TASARIM 5.14)."""
    return cikis * (1 - masraf) / (giris * (1 + masraf)) - 1


def _tek_dolumlar(dolumlar):
    if not isinstance(dolumlar, list):
        raise ValueError("dolumlar liste olmalı")
    gorulen = {}
    for d in dolumlar:
        if (
            not isinstance(d, dict)
            or not {"dolum_id", "adet", "fiyat", "yon"} <= d.keys()
        ):
            raise ValueError("dolum alanları eksik")
        kimlik = d["dolum_id"]
        if not isinstance(kimlik, str) or not kimlik:
            raise ValueError("dolum kimliği eksik")
        if kimlik in gorulen:
            if gorulen[kimlik] != d:
                raise ValueError(f"çelişkili dolum: {kimlik}")
            continue
        gorulen[kimlik] = dict(d)
        yield d


def _dolum_gecerli(d):
    adet, fiyat = d["adet"], d["fiyat"]
    return _pozitif(adet) and _pozitif(fiyat) and math.isfinite(adet * fiyat)


def _net_sonuc(alis, satis):
    return satis - alis - alis * KOMISYON_BSMV - satis * KOMISYON_BSMV


def _dolum_toplamlari(dolumlar):
    alinan = satilan = alis = satis = 0.0
    kismi = []
    for d in _tek_dolumlar(dolumlar):
        kimlik = d["dolum_id"]
        adet, fiyat, yon = d["adet"], d["fiyat"], d["yon"]
        if not _dolum_gecerli(d):
            raise ValueError(f"geçersiz dolum: {kimlik}")
        if yon == "alis" and satilan == 0:
            alinan += adet
            alis += adet * fiyat
        elif yon == "satis" and satilan + adet <= alinan:
            satilan += adet
            satis += adet * fiyat
            if satilan < alinan:
                kismi.append(
                    dict(
                        dolum_id=kimlik,
                        adet=adet,
                        net_sonuc=_net_sonuc(alis * (adet / alinan), adet * fiyat),
                    )
                )
        else:
            raise ValueError(f"dolum sırası, yönü veya miktarı geçersiz: {kimlik}")
    if not math.isfinite(alis + satis + alinan + satilan):
        raise ValueError("dolum toplamı sonlu değil")
    return alinan, satilan, alis, satis, kismi


def maliyet_hesapla(dolumlar, *, masraf_surumu):
    """TASARIM 5.15 S08: tek işlemin kimlikli, gerçekleşmiş dolumlarını hesaplar."""
    if masraf_surumu != MASRAF_SURUMU:
        raise ValueError(f"bilinmeyen masraf sürümü: {masraf_surumu}")
    alinan, satilan, alis, satis, kismi = _dolum_toplamlari(dolumlar)
    alis_maliyeti, satis_maliyeti = alis * KOMISYON_BSMV, satis * KOMISYON_BSMV
    pay = satilan / alinan if alinan else 0.0
    maliyet_temeli = alis * pay
    net = _net_sonuc(maliyet_temeli, satis)
    return {
        "masraf_surumu": masraf_surumu,
        "alinan_adet": alinan,
        "satilan_adet": satilan,
        "kalan_adet": alinan - satilan,
        "alis_maliyeti": alis_maliyeti,
        "satis_maliyeti": satis_maliyeti,
        "kalan_alis_maliyeti": alis_maliyeti * (1 - pay),
        "gerceklesen_maliyet": alis_maliyeti + satis_maliyeti,
        "gerceklesen_kayip": max(0.0, maliyet_temeli - satis),
        "net_sonuc": net,
        "gerceklesen_kismi_sonuclar": kismi,
        "net_fiyat_getirisi": (satis - satis_maliyeti) / (alis + alis_maliyeti) - 1
        if alinan and alinan == satilan
        else None,
    }


def _sonuc_olculeri(net, risk, neden=None):
    """TASARIM 5.15/#82: sonuç paydaları ve gerekçeli boş nihai/kısmi ölçüler."""
    sonuc = {}
    bos_nedenleri = {}
    for alan, payda in (
        ("referans_getirisi", risk["nominal_tutar"]),
        ("net_r", risk["ilk_risk"]),
    ):
        sonuc[alan] = net / payda if neden is None and payda else None
        if sonuc[alan] is None:
            bos_nedenleri[alan] = neden or risk["risk_nedeni"]
    return {**sonuc, "bos_nedenleri": bos_nedenleri}


def hesapla(girdi):
    """TASARIM 5.15 S08: aday bütçesi ile varsa gerçekleşmiş dolum sonucu ayrı kalır."""
    sonuc = boyutla(
        girdi.get("giris_fiyat"),
        girdi.get("ilk_stop"),
        girdi.get("nominal_tutar"),
        aile=girdi["aile"],
        risk_surumu=girdi["risk_surumu"],
    )
    dolumlar = girdi.get("dolumlar")
    # TASARIM 5.15: tabloya eklenen NaN, eksik alan gibi dolum bilgisi taşımaz.
    if dolumlar is not None and not (
        isinstance(dolumlar, Real) and math.isnan(dolumlar)
    ):
        sonuc.update(maliyet_hesapla(dolumlar, masraf_surumu=girdi["masraf_surumu"]))
        neden = (
            "giris_dolumu_yok"
            if not sonuc["alinan_adet"]
            else "islem_acik"
            if sonuc["kalan_adet"]
            else None
        )
        sonuc.update(_sonuc_olculeri(sonuc["net_sonuc"], sonuc, neden))
        if neden:
            sonuc["bos_nedenleri"]["net_fiyat_getirisi"] = neden
        for kismi in sonuc["gerceklesen_kismi_sonuclar"]:
            kismi.update(_sonuc_olculeri(kismi["net_sonuc"], sonuc))
        ilk_risk = sonuc["ilk_risk"]
        sonuc["gerceklesen_kayip_r"] = (
            sonuc["gerceklesen_kayip"] / ilk_risk if ilk_risk else None
        )
    return sonuc
