"""Gartley deneme betiklerinin denetim düzeltmeleri (`kanit/gartley-denetim.md`).

Eski betikler (`yontem.py` f9d682a1…, `pdf.py` 3e8f2dc6…) değişmez. Her düzeltme burada denetim kimliğiyle adlı bir
işlevdir; `uygula("D1t,E2", yontem, pdf)` onları içe aktarılmış modüllere yükler. Motor düzeltmeleri (`tansu/`) ayrı
PR'larla `yeniden-kurulus`'a girer; bu dosya yalnız deneme betiklerinin kendi kodundaki hataları düzeltir.
"""

from types import SimpleNamespace

import numpy as np
import pandas as pd

from tansu import gostergeler, islem, yapi


def D1t(yontem, pdf):
    """Desen D1-D3, deneme betikleri: PDF XABC ve AB=CD ABC noktaları bacak ucu olmalı; ilk nokta t'ye dek eşit ya da öte
    bir değer görünce desen bozulur (motorda `yapi.bacak_uclari`, PR 253). Pivot sırası, bacak ucu olmayan sıra atlanarak
    verilir; betiklerin kendi oran ve sıra kontrolleri değişmez."""
    for modul, ad, n in ((pdf, "sinyaller", 4), (yontem, "_abcd_kurulumlari", 3)):
        eski = getattr(modul, ad)

        def yeni(gun, *a, _eski=eski, _modul=modul, _n=n, **k):
            y, d = gun["yuksek"].to_numpy(float), gun["dusuk"].to_numpy(float)

            def ardisik(pivotlar):
                for sira in yapi.ardisik(pivotlar):
                    if len(sira) < _n or yapi.bacak_uclari(
                        y, d, sira[-_n:], sira[-1].onay_gun
                    ):
                        yield sira

            # ponytail: modülün `yapi` adını çağrı boyunca değiştirir; betikler tek iş parçacığında koşar
            _modul.yapi = SimpleNamespace(**{**vars(yapi), "ardisik": ardisik})
            try:
                return _eski(gun, *a, **k)
            finally:
                _modul.yapi = yapi

        setattr(modul, ad, yeni)


def T3(yontem, pdf):
    """İşlem T3: teyit günündeki RSI(14) > 50, Tansu'nun basit ortalamalı RSI'ıdır (SPEC 3.12), Wilder değil."""
    yontem.gostergeler = SimpleNamespace(
        **{**vars(gostergeler), "rsi": gostergeler.rsi_basit}
    )


def E2(yontem, pdf):
    """Emir E2: açılış stopu yalnız günün yükseği stopun altındaysa (açılış kesin stopun altında) AOF'den çıkar. AOF günün
    ortalamasıdır; AOF < stop iken yüksek >= stop olan günde açılış stopun üstünde olabilir, motor stoptan çıkar."""
    para = yontem.para
    eski = para._cikis_kur

    def yeni(c):
        cikis, acik = eski({**c, "acilis_stopu": False})
        if not c.get("acilis_stopu", True):
            return cikis, acik

        def acik_gun(e, i, g, ck):
            if (
                i > e.dolum_i
                and not g.taban_kilit[i]
                and not e.bekleyen
                and g.yuk[i] < e.stop
            ):
                return islem._kapat(e, i, g.aof[i], "stop (açılış)")
            return acik(e, i, g, ck)

        return cikis, acik_gun

    para._cikis_kur = yeni


def S1s(yontem, pdf):
    """İstatistik S1: p değerinin yeniden örnekleme kümesi dolumun takvim çeyreği. Haftalık küme ortak piyasa hareketini
    (işlem R'si ile tutma dönemindeki BIST 100 getirisi arasında 0,29-0,52 ilişki) bağımsız sayıyordu."""
    yontem.hafta = lambda tarih: (
        tarih.dt.year.astype(str) + "-Q" + tarih.dt.quarter.astype(str)
    )


def S2s(yontem, pdf):
    """İstatistik S2: geçme şartı 1 en az 30 dolum ister (SPEC 5.6 `EN_AZ`); 2 dolumla p = 0 çıkabiliyordu."""
    eski = yontem.gecme

    def gecme(s, p, k=yontem.K_SINAV):
        g = eski(s, p, k)
        if s.get("n", 0) < yontem.EN_AZ_DOLUM:
            g["1_ortR_pozitif_ve_p"] = g["EVET"] = False
        return g

    yontem.gecme = gecme


def kontrol(yontem, pdf):
    """Her düzeltme için elle hesaplanmış küçük durum: eski davranış beklenen değeri vermez (kırmızı), düzeltilmiş verir.
    Düzeltmesiz yeni bir süreçte çağrılır; düzeltmeleri kendisi sırayla yükler."""
    sonuc = {}

    # D1t: B (gün 8, 14) bacağın dibi değil, gün 5'te 13 var; sıra atlanmalı.
    yuk = np.array(
        [10.5, 13, 16, 20, 18, 14, 15, 16, 14.5, 15, 16, 16.5, 17, 16.5, 16.0]
    )
    dus = np.array(
        [10.0, 12, 15, 19, 17, 13, 14, 15, 14.0, 14.5, 15, 16, 16.5, 16, 15.5]
    )
    pivotlar = [
        yapi.Pivot("D", 0, 2, 10.0),
        yapi.Pivot("T", 3, 5, 20.0),
        yapi.Pivot("D", 8, 10, 14.0),
        yapi.Pivot("T", 12, 14, 17.0),
    ]
    gun = pd.DataFrame({"yuksek": yuk, "dusuk": dus})
    sahte_p, sahte_y = SimpleNamespace(yapi=yapi), SimpleNamespace(yapi=yapi)
    sahte_p.sinyaller = lambda g, *a: [
        s[-4:] for s in sahte_p.yapi.ardisik(pivotlar) if len(s) == 4
    ]
    sahte_y._abcd_kurulumlari = lambda g: [
        s[-3:] for s in sahte_y.yapi.ardisik(pivotlar[1:]) if len(s) == 3
    ]
    eski = (len(sahte_p.sinyaller(gun)), len(sahte_y._abcd_kurulumlari(gun)))
    D1t(sahte_y, sahte_p)
    yeni = (len(sahte_p.sinyaller(gun)), len(sahte_y._abcd_kurulumlari(gun)))
    assert eski == (1, 1) and yeni == (0, 0), (eski, yeni)
    sonuc["D1t"] = {"eski": eski, "yeni": yeni}

    # E2: dolum 1. gün 10'dan, stop 9. 2. gün AOF 8,9 < stop ama yüksek 9,5 >= stop, düşük 8,5: motor stoptan (9) çıkar.
    g = pd.DataFrame(
        {
            "aof": [10.0, 10.0, 8.9],
            "yuksek": [10.2, 10.2, 9.5],
            "dusuk": [9.8, 9.8, 8.5],
            "kapanis": [10.0, 10.0, 9.0],
            "atr": 0.5,
            "kilit_tavan": False,
            "kilit_taban": False,
            "tavan_kapanis": False,
            "uye": True,
            "karantina": False,
        },
        index=pd.bdate_range("2022-01-03", periods=3),
    )
    motor = islem.Gun(g, pd.DataFrame({"cikis_sinyali": False}, index=g.index))

    def cikis_fiyati():
        _, acik = yontem.para._cikis_kur({"tur": "tp1", "acilis_stopu": True})
        e = islem._Islem(0, {"hedef1": 12.0}, 9.0, 0.25)
        islem._doldur(e, 1, 10.0)
        for i in (1, 2):
            if acik(e, i, motor, islem.Cikis("dokunus", (("hedef1", 1.0),))):
                return e.parcalar[-1][1]
        return None

    eski = cikis_fiyati()
    E2(yontem, pdf)
    yeni = cikis_fiyati()
    assert eski == 8.9 and yeni == 9.0, (eski, yeni)
    sonuc["E2"] = {"eski": eski, "yeni": yeni}

    # T3: kapanış 1, 2, 1, 2, ... RSI(2) basit ortalamayla her gün 50; Wilder ilk değerden sonra 50'den sapar.
    k = pd.Series([1.0, 2, 1, 2, 1, 2, 1, 2])
    eski = round(float(yontem.gostergeler.rsi(k, 2).iloc[-1]), 3)
    T3(yontem, pdf)
    yeni = round(float(yontem.gostergeler.rsi(k, 2).iloc[-1]), 3)
    assert eski != 50 and yeni == 50, (eski, yeni)
    sonuc["T3"] = {"eski": eski, "yeni": yeni}

    # S1s: 2022-03-31 ve 2022-04-01 farklı çeyrek, aynı hafta değil; 2022-03-28 ile 2022-03-31 aynı hafta.
    t = pd.Series(pd.to_datetime(["2022-03-28", "2022-03-31", "2022-04-01"]))
    eski = yontem.hafta(t).tolist()
    S1s(yontem, pdf)
    yeni = yontem.hafta(t).tolist()
    assert eski == ["2022-13", "2022-13", "2022-13"] and yeni == [
        "2022-Q1",
        "2022-Q1",
        "2022-Q2",
    ], (eski, yeni)
    sonuc["S1s"] = {"eski": eski, "yeni": yeni}

    # S2s: 2 dolum, ikisi de kazançlı: p = 0, eski geçme şartı 1 tutar; en az 30 dolum gerekir.
    s = {"n": 2, "ort_R": 1.0, "p_tek_yonlu": 0.0}
    p = {
        "uc_parca": {
            "en_iyi_uc_olmadan_islem_kari_tl": 1.0,
            "son_kasa_tl": 2.0,
            "yalniz_nakit_kasasi_tl": 1.0,
        }
    }
    eski = yontem.gecme(s, p)["EVET"]
    S2s(yontem, pdf)
    yeni = yontem.gecme(s, p)["EVET"]
    assert eski is True and yeni is False, (eski, yeni)
    sonuc["S2s"] = {"eski": eski, "yeni": yeni}
    return sonuc


def uygula(adlar: str, yontem, pdf) -> list[str]:
    secilen = [a for a in adlar.split(",") if a]
    for a in secilen:
        globals()[a](yontem, pdf)
    return secilen
