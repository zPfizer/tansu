"""İstatistik: p değeri, Holm, blok bootstrap, saptanabilir en küçük etki, K1 ve kabul tablosu (TASARIM 5.7, 5.9, 5.12)."""

from collections import Counter, defaultdict
from datetime import date
import math
from numbers import Real

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from tansu import aileler, cift, ciftbolme, gostergeler, motor, simulator

GUN = 252  # yıllıklandırma
Z_ALFA, Z_GUC = 1.645, 0.842  # tek yönlü %5, güç %80 (TASARIM 5.9)
K1_MASRAF = 0.005  # Holm'a giren p %0,5 masrafla (TASARIM 5.7)
K1_PENCERE = 20  # tür (b): ±20 gün (TASARIM 5.7)
SUPHELI_KAZANMA, AZ_ISLEM = 0.90, 5  # TASARIM 5.14: yalnız eski rapor etiketleri.


class K1Hatasi(Exception):
    """Ön şartlı gün kümesi gereken sayıdan küçük: sessizce kırpılmaz (TASARIM 5.7)."""


def ortalama_fazla(islemler) -> float:
    """K1 istatistiği: işlem başına ortalama fazla getiri (TASARIM 5.7); işlem yoksa NaN."""
    return float(islemler["fazla"].mean()) if len(islemler) else float("nan")


class EmaK1:
    """EMA sıkışması K1: ön şartlı gün havuzları ve rastgele sinyal çekimi (TASARIM 5.7 "K1 uygulama kuralları").

    Konumlar hissenin mum tablosundaki (`motor.mumlar`) satır konumlarıdır."""

    def __init__(self, anlik, p, atr_n, uye, kirilim=None):
        kirilim = kirilim or aileler.KIRILIM_GUN
        xu = anlik.fiyat.groupby("tarih")["xu100"].first()
        durum = gostergeler.piyasa_durumu(xu[xu > 0])
        uye_gun = uye.groupby("sembol")["tarih"].agg(list)
        self.zincir, self.gercek, self.sayi = {}, {}, Counter()
        self.kurulum = {}  # sembol -> gerçek sinyallerin kutu alt ve hedefi (yoksa None); rastgele giriş kutusuzdur
        self.havuz = {"a": defaultdict(list), "ek": defaultdict(list)}
        self.komsu, self.komsusuz = (
            {},
            [],
        )  # (sembol, konum) -> tür (b) adayları; komşusuz sinyaller
        for s in sorted(uye_gun.index):
            m = motor.mumlar(anlik, s, p, atr_n)
            f = m.dropna(subset=["kapanis"])
            z = self.zincir[s] = motor.Zincir(m, p)
            konum = m.index.get_indexer(f.index)
            uygun = (
                m.index.isin(uye_gun[s]) & ~z.engelli
            )  # evren üyesi ve karantina penceresi dışı
            a, ek = np.zeros(len(m), bool), np.zeros(len(m), bool)
            a[konum], ek[konum] = (
                aileler.on_sart(f, p),
                aileler.sikismasiz_kirilim(f, p, kirilim),
            )
            hisse = np.zeros(
                len(m), bool
            )  # tür (b): hisse düzeyi uygun gün (TASARIM 5.7)
            hisse[konum] = aileler.uygun_gunler(f, p)
            a, ek, hisse = a & uygun, ek & uygun, hisse & uygun
            for tur, maske in (("a", a), ("ek", ek)):
                for i in np.flatnonzero(maske):
                    self.havuz[tur][m.index[i]].append((s, int(i)))
            sig = aileler.sinyal(f, p)
            self.kurulum[s] = motor.kurulum_bilgisi(f, p)
            # örtüşen iki sıkışma döneminin penceresi aynı güne sinyal verebilir: bir hisse bir günde tek sinyaldir
            gercek = sorted(
                {
                    int(i)
                    for i in m.index.get_indexer(sig[sig.isin(uye_gun[s])])
                    if uygun[i]
                }
            )
            if gercek:
                self.gercek[s] = gercek
            d = durum.reindex(m.index).fillna(False).to_numpy(bool)
            for i in gercek:
                self.sayi[m.index[i]] += 1
                aday = [
                    j
                    for j in range(
                        max(0, i - K1_PENCERE), min(len(m), i + K1_PENCERE + 1)
                    )
                    if j != i and hisse[j] and d[j] == d[i]
                ]
                if aday:
                    self.komsu[(s, i)] = aday
                else:  # TASARIM 5.7: komşusuz sinyal (b)'den düşer ve sayılır
                    self.komsusuz.append((s, m.index[i].date()))
        if self.sayi and not self.komsu:
            raise K1Hatasi(
                f"tür (b): hiçbir sinyalin ±{K1_PENCERE} gün içinde aynı piyasa durumunda başka uygun günü yok "
                f"(örn. {self.komsusuz[0][0]} {self.komsusuz[0][1]})"
            )
        self.ek_eksik = 0  # ek kol raporluktur: havuzu yetmeyen sinyal çekimden düşer ve sayılır (TASARIM 5.7)
        for tur in ("a", "ek"):
            for gun, n in self.sayi.items():
                yok = n - len(self.havuz[tur].get(gun, ()))
                if yok > 0 and tur == "a":
                    raise K1Hatasi(
                        f"{gun.date()}: {n} sinyal için ön şartlı havuz {n - yok} hisse ({tur})"
                    )
                if yok > 0:
                    self.ek_eksik += yok

    def cek(self, tur, rng) -> dict:
        """Rastgele sinyaller: {sembol: konumlar}. `a` ve `ek`: gün başına gerçek sinyal sayısı kadar, havuzdan yerine koymadan;
        `b`: her gerçek sinyal için aynı hissede ±20 satırdan başka ön şartlı bir gün."""
        sec = defaultdict(list)
        if tur == "b":
            for (s, i), aday in sorted(self.komsu.items()):
                sec[s].append(int(rng.choice(aday)))
        else:
            for gun, n in sorted(self.sayi.items()):
                havuz = self.havuz[tur][gun]
                for k in rng.choice(len(havuz), min(n, len(havuz)), replace=False):
                    sec[havuz[k][0]].append(havuz[k][1])
        return {s: sorted(v) for s, v in sorted(sec.items())}

    def tablo(self, secim, gercek=False) -> tuple:
        """(işlem tablosu, düşen sinyal sayısı): `motor.sinama` ile aynı sütunlar. `gercek`: `secim` gerçek sinyallerdir,
        kutu stopu ve hedef kullanılır; rastgele girişte kutu yoktur (`atr2` yedeği, hedef yok)."""
        kapali, sembol, dusen = [], [], 0
        for s in sorted(secim):
            k, d = self.zincir[s].kapali(secim[s], self.kurulum[s] if gercek else None)
            kapali += k
            sembol += [s] * len(k)
            dusen += d
        return motor._tablo(kapali).assign(
            sembol=sembol
        ), dusen  # tek tablo: hisse başına DataFrame kurmak yavaştı


def ema_k1(
    anlik, b, p, atr_n, uye, tekrar, tohum=0, masraf=K1_MASRAF, kirilim=None
) -> dict:
    """EMA ailesi K1: gerçek kural ve `tekrar` rastgele kol (a, b, ek); p = (1 + k) / (1 + B). Aile p'si a ve b'nin büyüğü."""
    k = EmaK1(anlik, p, atr_n, uye, kirilim)
    istatistik = lambda secim, gercek_mi=False: ortalama_fazla(
        simulator.k1_islemler(k.tablo(secim, gercek_mi)[0], b, masraf)
    )  # noqa: E731
    gercek = istatistik(k.gercek, True)
    p_tur = {}
    for sira, tur in enumerate(("a", "b", "ek")):
        rng = np.random.default_rng([tohum, sira])
        p_tur[tur] = p_deger(
            gercek, [istatistik(k.cek(tur, rng)) for _ in range(tekrar)]
        )
    return {
        "gercek": gercek,
        "p_a": p_tur["a"],
        "p_b": p_tur["b"],
        "p_ek": p_tur["ek"],
        "p": max(p_tur["a"], p_tur["b"]),
        "tekrar": tekrar,
        "sinyal": sum(len(v) for v in k.gercek.values()),
        "komsusuz": len(k.komsusuz),
        "ek_eksik": k.ek_eksik,
    }


def cift_tablo(islemler, b) -> pd.DataFrame:
    """Çift tutuş dönemleri (`ciftbolme._rotasyon`) ve sepete göre `fazla` getiri."""
    t = pd.DataFrame(islemler, columns=CiftK1.SUTUN)
    fazla = (
        t["getiri"] - simulator.sepet_getirisi(b, t["giris_tarih"], t["cikis_tarih"])
        if len(t)
        else []
    )
    return t.assign(fazla=fazla)


class CiftK1:
    """Çift bölmesi K1: aynı çiftlerde, gerçek tutuş sayısı kadar sinyal, rastgele günlerde (TASARIM 5.7 "K1 uygulama kuralları")."""

    SUTUN = [
        "cift",
        "sembol",
        "giris_tarih",
        "giris_fiyat",
        "cikis_tarih",
        "cikis_fiyat",
        "neden",
        "adet",
        "getiri",
    ]

    def __init__(self, h, b, masraf=K1_MASRAF):
        self.h, self.b, self.masraf = h, b, masraf
        gunler, p, setler = h["gunler"], h["p"], h["setler"]
        self.gercek = self._tablo(
            ciftbolme._rotasyon(h["M"], setler, p.en_fazla, masraf)[0]
        )
        ayri = (
            self.gercek["cift"].str.split("-", expand=True)
            if len(self.gercek)
            else pd.DataFrame({0: [], 1: []})
        )
        self.gercek = self.gercek.assign(y=ayri[0], x=ayri[1])
        self.cift = {}  # (y, x) -> (tutuş sayısı, ilk sinyal konumu, ilk hedef, uygun konumlar)
        for (y, x), g in self.gercek.groupby(["y", "x"]):
            z = cift.z_skor(h["Kc"][y], h["Kc"][x], p.z_pencere).to_numpy()
            etkin = np.zeros(len(gunler), bool)
            for k, st in enumerate(setler):
                if (y, x) in st["ciftler"]:
                    son = (
                        setler[k + 1]["bas"] if k + 1 < len(setler) else len(gunler) + 1
                    )
                    etkin[st["bas"] - 1 : son - 1] = True
            ilk = g.sort_values("giris_tarih").iloc[0]
            s0 = gunler.get_loc(ilk["giris_tarih"]) - 1  # sinyal, girişten bir gün önce
            uygun = np.flatnonzero(
                (np.abs(z) >= p.z_esik) & etkin & (np.arange(len(gunler)) > s0)
            )
            if len(uygun) < len(g) - 1:
                raise K1Hatasi(
                    f"{y}-{x}: {len(g)} tutuş için |Z| ≥ {p.z_esik} olan {len(uygun) + 1} uygun gün var"
                )
            self.cift[(y, x)] = (len(g), s0, 1 if ilk["sembol"] == y else -1, uygun)

    def _tablo(self, islemler) -> pd.DataFrame:
        return cift_tablo(islemler, self.b)

    def cek(self, rng) -> dict:
        """(y, x) -> hedef dizisi (+1 Y, −1 X, 0 sinyal yok); ilk sinyal gerçeğin aynısı, sonrakiler sırayla öteki bacak."""
        sonuc = {}
        for yx, (n, s0, yon, uygun) in self.cift.items():
            konum = sorted([s0, *rng.choice(uygun, n - 1, replace=False)])
            hedef = np.zeros(len(self.h["gunler"]), dtype=int)
            hedef[konum] = [yon * (-1) ** i for i in range(n)]
            sonuc[yx] = hedef
        return sonuc

    def istatistik(self, hedefler) -> float:
        bos = np.zeros(len(self.h["gunler"]), dtype=int)
        M = {**self.h["M"], "hedef": lambda y, x: hedefler.get((y, x), bos)}
        t = self._tablo(
            ciftbolme._rotasyon(M, self.h["setler"], self.h["p"].en_fazla, self.masraf)[
                0
            ]
        )
        return ortalama_fazla(t)


def cift_k1(h, b, tekrar, tohum=0, masraf=K1_MASRAF) -> dict:
    """Çift bölmesi K1 (`ciftbolme.hazirla` çıktısı `h`); p = (1 + k) / (1 + B)."""
    k = CiftK1(h, b, masraf)
    gercek = ortalama_fazla(k.gercek)
    rng = np.random.default_rng([tohum, 3])
    p = p_deger(gercek, [k.istatistik(k.cek(rng)) for _ in range(tekrar)])
    return {
        "gercek": gercek,
        "p": p,
        "tekrar": tekrar,
        "gecis": len(k.gercek),
        "gecis_gun": int(k.gercek["giris_tarih"].nunique()),
    }


MIN_ISLEM, MIN_GUN = 100, 60  # TASARIM 5.9 örneklem şartı
SAGLAMLIK_ESIK, YIL_ESIK = 0.60, 0.60  # TASARIM 5.10, 5.12 ölçüt 4
DUSUS_ESIK, DUSUS_GUN = 0.25, 365  # TASARIM 5.12 portföy kuralı
GIDIS_DONUS = 2 * K1_MASRAF  # TASARIM 5.12 "Ölçülemedi"
GECTI, GECMEDI, OLCULEMEDI = "Geçti", "Geçmedi", "Ölçülemedi"


def dusus(ozkaynak) -> tuple:
    """İlk kapanış politikasıyla (en büyük düşüş oranı, takvim günü süresi).

    TASARIM 5.12: eski süre, düşüş olmasa da ardışık zirveler arasını kapsar.
    """
    sonuc = egri_dususu(
        dict(
            tur="legacy_ozkaynak",
            satirlar=[dict(an=t, deger=v) for t, v in ozkaynak.iloc[1:].items()],
            baslangic_degeri=ozkaynak.iloc[0],
            baslangic_ani=ozkaynak.index[0],
            baslangic_politikasi="ilk_kapanis",
            tarih_temeli="takvim_gunu",
            normalizasyon="ilk_kapanis",
            birim="oran",
            muhasebe_politikasi="legacy_portfoy_v1",
            referanslar=[],
        )
    )
    return float(sonuc["derinlik"]["deger"]), int(sonuc["sure"]["deger"])


def _sonlu_sayi(deger):
    return (
        isinstance(deger, Real) and not isinstance(deger, bool) and math.isfinite(deger)
    )


def _olcu(deger, birim, neden="veri_eksik"):
    if not _sonlu_sayi(deger):
        return dict(deger=None, birim=birim, bos_nedeni=neden)
    return dict(deger=deger, birim=birim, bos_nedeni=None)


def _egri_sozlesmesi(egri):
    gerekli = {
        "tur",
        "satirlar",
        "baslangic_degeri",
        "baslangic_ani",
        "baslangic_politikasi",
        "tarih_temeli",
        "normalizasyon",
        "birim",
        "muhasebe_politikasi",
        "referanslar",
    }
    if not isinstance(egri, dict) or not gerekli <= egri.keys():
        raise ValueError("Eğrinin başlangıç, birim ve tarih sözleşmesi eksik.")
    if (egri["tur"], egri["birim"]) not in {
        ("legacy_ozkaynak", "oran"),
        ("tani_net_r", "R"),
        ("tani_referans", "oran"),
    } or egri["tarih_temeli"] not in ("takvim_gunu", "gozlem_adimi"):
        raise ValueError("Desteklenmeyen eğri birimi veya tarih temeli.")
    if egri["baslangic_politikasi"] not in ("acik", "ilk_kapanis"):
        raise ValueError("Desteklenmeyen başlangıç politikası.")


def _egri_noktalari(egri):
    satirlar = [
        dict(an=egri["baslangic_ani"], deger=egri["baslangic_degeri"]),
        *egri["satirlar"],
    ]
    degerler = [s["deger"] for s in satirlar]
    if egri["tarih_temeli"] == "takvim_gunu":
        anlar = [pd.Timestamp(s["an"]) for s in satirlar]
    else:
        anlar = [s["an"] for s in satirlar]
    if any(pd.isna(t) for t in anlar) or any(
        a > b for a, b in zip(anlar, anlar[1:], strict=False)
    ):
        raise ValueError("Eğri gözlem anları sıralı ve tanımlı olmalıdır.")
    return anlar, degerler


def _egri_bos_nedeni(egri, degerler):
    if not all(_sonlu_sayi(v) for v in degerler):
        return "egri_degeri_eksik"
    if egri["tur"] == "legacy_ozkaynak" and degerler[0] <= 0:
        return "egri_paydasi_gecersiz"
    if egri["tur"] != "legacy_ozkaynak" and degerler[0] != 0:
        raise ValueError("Tanısal eğri sıfırdan başlamalıdır.")
    return None


def _derinlik_farki(egri, zirve, deger):
    if egri["tur"] != "legacy_ozkaynak":
        return zirve - deger
    if egri["baslangic_politikasi"] == "ilk_kapanis":
        return (zirve - deger) / zirve
    return -(deger / zirve - 1)


def _zirve_taramasi(egri, anlar, degerler):
    zirve, zirve_ani, derinlik, sure = degerler[0], anlar[0], 0.0, 0
    dususte = False
    for an, deger in zip(anlar[1:], degerler[1:], strict=True):
        aralik = an - zirve_ani
        if egri["tarih_temeli"] == "takvim_gunu":
            aralik = aralik.days
        if deger >= zirve:
            # TASARIM 5.12: eski süre hesabı ardışık zirvelerin aralığını da korur.
            if dususte or egri["baslangic_politikasi"] == "ilk_kapanis":
                sure = max(sure, aralik)
            zirve, zirve_ani, dususte = deger, an, False
        else:
            dususte = True
            derinlik = max(derinlik, _derinlik_farki(egri, zirve, deger))
            sure = max(sure, aralik)
    return float(derinlik), int(sure)


def egri_dususu(egri):
    """TASARIM 5.15 S11: açık başlangıç ve tarih politikasıyla tek zirve taraması."""
    _egri_sozlesmesi(egri)
    anlar, degerler = _egri_noktalari(egri)
    neden = _egri_bos_nedeni(egri, degerler)
    if neden:
        return dict(
            derinlik=_olcu(None, egri["birim"], neden),
            sure=_olcu(None, egri["tarih_temeli"], neden),
        )
    derinlik, sure = _zirve_taramasi(egri, anlar, degerler)
    return dict(
        derinlik=_olcu(derinlik, egri["birim"]), sure=_olcu(sure, egri["tarih_temeli"])
    )


def _legacy_kar_olculeri(kazanc, kayip):
    return {
        "kazanan": len(kazanc),
        "kaybeden": len(kayip),
        "kar_carpani": float(kazanc.sum() / abs(kayip.sum()))
        if kayip.sum() != 0
        else None,
        "kazanc_kayip": float(kazanc.mean() / abs(kayip.mean()))
        if len(kazanc) and len(kayip) and kayip.mean() != 0
        else None,
    }


def _legacy_islem_olculeri(r, tutma):
    n = len(r)
    kazanc, kayip = r[r > 0], r[r <= 0]
    return {
        "islem": n,
        "kazanma": len(kazanc) / n if n else None,
        "ort_islem": float(r.mean()) if n else None,
        "medyan_islem": float(np.median(r)) if n else None,
        "net": float(np.prod(1 + r) - 1),
        "ort_tutma": float(np.mean(tutma)) if n else None,
        **_legacy_kar_olculeri(kazanc, kayip),
    }


def _legacy_egri_olculeri(egri, pozisyonda):
    deger = np.concatenate(([1.0], np.asarray(egri, dtype=float)))
    gunluk = deger[1:] / deger[:-1] - 1
    sapma = gunluk.std(ddof=1) if len(gunluk) > 1 else 0.0
    dusus = egri_dususu(
        dict(
            tur="legacy_ozkaynak",
            satirlar=[dict(an=i, deger=v) for i, v in enumerate(deger[1:], 1)],
            baslangic_degeri=1.0,
            baslangic_ani=0,
            baslangic_politikasi="acik",
            tarih_temeli="gozlem_adimi",
            normalizasyon="baslangic_bir",
            birim="oran",
            muhasebe_politikasi="legacy_tansu_v1",
            referanslar=[],
        )
    )
    max_dd = -dusus["derinlik"]["deger"] if dusus["derinlik"]["deger"] else 0.0
    return {
        "max_dd": max_dd,
        "sharpe": float(gunluk.mean() / sapma * np.sqrt(252)) if sapma > 0 else None,
        "calmar": float((deger[-1] ** (252 / len(gunluk)) - 1) / abs(max_dd))
        if max_dd < 0
        else None,
        "maruziyet": pozisyonda / len(gunluk),
    }


def _legacy_bayraklar(kazanma, n):
    bayraklar = []
    if kazanma is not None and kazanma >= SUPHELI_KAZANMA:
        bayraklar.append("şüpheli: aşırı uyum")
    if n < AZ_ISLEM:
        bayraklar.append("az işlem")
    return bayraklar


def _legacy_olculer(girdi):
    """TASARIM 5.14: eski formüller ve uyarılar tek ölçü sahibinde kalır."""
    r = np.asarray(girdi["getiriler"], dtype=float)
    sonuc = _legacy_islem_olculeri(r, girdi["tutma"])
    sonuc.update(_legacy_egri_olculeri(girdi["egri"], girdi["pozisyonda"]))
    sonuc["bayraklar"] = _legacy_bayraklar(sonuc["kazanma"], len(r))
    return sonuc


def _gunluk_anlar(satirlar):
    if any(not isinstance(s.get("an"), (str, date)) for s in satirlar):
        return None
    try:
        anlar = [pd.Timestamp(s["an"]) for s in satirlar]
    except ValueError, TypeError:
        return None
    if any(pd.isna(an) or an != an.normalize() for an in anlar):
        return None
    return anlar


def _gunluk_seri_nedeni(g, r):
    gunler, risksiz_gunler = _gunluk_anlar(g), _gunluk_anlar(r)
    if gunler is None or risksiz_gunler is None:
        return "gunluk_tarih_gecersiz"
    try:
        sirali = sorted(set(gunler))
    except TypeError:
        return "gunler_hizasiz"
    if gunler != risksiz_gunler or gunler != sirali:
        return "gunler_hizasiz"
    if len(g) < 2:
        return "iki_gozlem_gerekli"
    if not all(_sonlu_sayi(x.get("deger")) for x in g + r):
        return "gunluk_deger_eksik"
    return None


def _gunluk_sharpe(karsilastirma):
    if karsilastirma is None:
        return _olcu(None, "oran", "gunluk_karsilastirma_yok")
    k = karsilastirma
    if k.get("politika") != "gunluk_fark_252_v1":
        raise ValueError("Desteklenmeyen Sharpe politikası.")
    if not k.get("payda") or not k.get("kaynak_ref") or not k.get("referanslar"):
        return _olcu(None, "oran", "payda_veya_kaynak_eksik")
    g, r = k.get("getiriler", []), k.get("risksiz", [])
    neden = _gunluk_seri_nedeni(g, r)
    if neden:
        return _olcu(None, "oran", neden)
    fark = np.array([a["deger"] - b["deger"] for a, b in zip(g, r, strict=True)])
    sapma = fark.std(ddof=1)
    if sapma == 0:
        return _olcu(None, "oran", "sapma_sifir")
    return _olcu(
        float(fark.mean() / sapma * np.sqrt(252)), "oran", "gunluk_deger_gecersiz"
    )


def _tek_islemler(islemler):
    gorulen = {}
    for i in islemler:
        kimlik = i.get("islem_id") or i.get("pozisyon", {}).get("risk_girdisi", {}).get(
            "islem_id"
        )
        if not isinstance(kimlik, str) or not kimlik:
            raise ValueError("Ölçü için gerçek işlem kimliği gerekli.")
        if kimlik in gorulen:
            if gorulen[kimlik] != i:
                raise ValueError(f"Çelişkili işlem sonucu: {kimlik}")
            continue
        gorulen[kimlik] = i
        yield kimlik, i


def _islem_olcu_kaydi(kimlik, i):
    s = i["sonuc"]
    nedenler = s.get("bos_nedenleri", {})
    o = {
        ad: _olcu(
            s.get(alan),
            birim,
            nedenler.get(alan) or s.get("risk_nedeni") or "sonuc_eksik",
        )
        for ad, alan, birim in (
            ("net_sonuc", "net_sonuc", "TL"),
            ("masraf", "gerceklesen_maliyet", "TL"),
            ("net_fiyat_getirisi", "net_fiyat_getirisi", "oran"),
            ("referans_getirisi", "referans_getirisi", "oran"),
            ("net_r", "net_r", "R"),
            ("adet", "alinan_adet", "adet"),
            ("kalan_adet", "kalan_adet", "adet"),
        )
    }
    return dict(
        islem_id=kimlik,
        islem_ref=i.get("islem_ref"),
        cikis_tarih=i.get("pozisyon", {}).get("cikis_tarih"),
        olculer=o,
        paydalar={a: s.get(a) for a in ("ilk_risk", "nominal_tutar")},
        muhasebe_politikasi="bagimsiz_olcu_v1",
        masraf_surumu=s.get("masraf_surumu"),
        kismi_sonuclar=s.get("gerceklesen_kismi_sonuclar", []),
    )


def _kapali_sonuc(s):
    adet = s.get("alinan_adet")
    return _sonlu_sayi(adet) and adet > 0 and s.get("kalan_adet") == 0


def _islem_olculeri(islemler):
    kapali, acik = [], []
    for kimlik, i in _tek_islemler(islemler):
        kayit = _islem_olcu_kaydi(kimlik, i)
        if _kapali_sonuc(i["sonuc"]):
            kapali.append(kayit)
        else:
            acik.append(kayit)
    return kapali, acik


def _toplam_olcu(kapali, ad, birim):
    degerler = [i["olculer"][ad]["deger"] for i in kapali]
    neden = "kapali_islem_yok" if not kapali else f"{ad}_eksik"
    deger = sum(degerler) if degerler and None not in degerler else None
    return _olcu(deger, birim, neden)


def _getiri_ozeti(kapali):
    r = [i["olculer"]["net_fiyat_getirisi"]["deger"] for i in kapali]
    if not r or None in r:
        return {
            ad: _olcu(None, "oran", "kapali_getiri_eksik")
            for ad in ("kazanma", "ort_islem", "medyan_islem")
        }
    return dict(
        kazanma=_olcu(sum(v > 0 for v in r) / len(r), "oran"),
        ort_islem=_olcu(float(np.mean(r)), "oran"),
        medyan_islem=_olcu(float(np.median(r)), "oran"),
    )


def _bagimsiz_olcu(islemler, egri, karsilastirma):
    kapali, acik = _islem_olculeri(islemler)
    o = dict(islem=_olcu(len(kapali), "adet"))
    for ad, birim in (
        ("net_sonuc", "TL"),
        ("masraf", "TL"),
        ("net_r", "R"),
        ("referans_getirisi", "oran"),
    ):
        o[ad] = _toplam_olcu(kapali, ad, birim)
    o.update(_getiri_ozeti(kapali))
    o["sharpe"] = _gunluk_sharpe(karsilastirma)
    o["calmar"] = _olcu(None, "oran", "tanisal_toplam_ozkaynak_degil")
    egri_olculeri = {
        "derinlik": _olcu(None, "R", "egri_yok"),
        "sure": _olcu(None, "takvim_gunu", "egri_yok"),
    }
    if egri is not None:
        egri_olculeri = egri_dususu(egri)
    return dict(
        politika="bagimsiz_olcu_v1",
        olculer=o,
        islemler=kapali,
        acik_kismi=acik,
        egri_tanimi=egri,
        egri_olculeri=egri_olculeri,
        karsilastirma=karsilastirma,
    )


def _legacy_birim(ad):
    if ad in ("islem", "kazanan", "kaybeden"):
        return "adet"
    return "gun" if ad == "ort_tutma" else "oran"


def olc(islemler, *, politika, egri=None, karsilastirma=None):
    """TASARIM 5.15 S11: sürümlü, birimli işlem ve eğri ölçüleri."""
    if politika == "pozitif_fazla_legacy_v1":
        fazla = ortalama_fazla(islemler)
        return dict(
            politika=politika,
            olculer=dict(
                islem=_olcu(len(islemler), "adet"),
                fazla=_olcu(fazla, "oran", "islem_yok"),
            ),
        )
    if politika == "eksen_maksimin_legacy_v1":
        eski = _legacy_olculer(islemler)
        return dict(
            politika=politika,
            legacy=eski,
            olculer={
                k: _olcu(v, _legacy_birim(k), "eski_payda_tanimsiz")
                for k, v in eski.items()
                if k != "bayraklar"
            },
        )
    if politika != "bagimsiz_olcu_v1":
        raise ValueError(f"Bilinmeyen ölçü politikası: {politika}")
    return _bagimsiz_olcu(islemler, egri, karsilastirma)


def _tamamlanan_yillar(yillik, bas, bitis, islem_yok) -> list:
    """Ilk ve son yarım yıl ile çift bölmesinin "işlem yok" yılları paydadan çıkar (TASARIM 5.12)."""
    return [
        y
        for y in yillik.index
        if bas <= pd.Timestamp(y, 1, 15)
        and bitis >= pd.Timestamp(y, 12, 15)
        and y not in islem_yok
    ]


def kabul(g) -> dict:
    """Bir ailenin 6 ölçütlük kabul tablosu ve durumu (TASARIM 5.12 ve "Ölçütlerin uygulanışı").

    Girdi `g`: fazla {masraf: K1 işlem başına fazla getiri}, p (Holm, ya da None), portfoy {masraf: günlük portföy fazla
    getirisi ortalaması}, yillik (yıl → fazla getiri, %0,3), bas/bitis, islem_yok, islem_fazla (%0,3, işlem başına),
    islem, gun (örneklem), mde (yıllık), islem_yil, ozkaynak (%0,5, faizli), saglamlik (oran ya da None).
    Satır: no, ad, durum, ham [(etiket, değer, birim)]; birim: yuzde, sayi, p."""
    p, f, pf = g["p"], g["fazla"], g["portfoy"]
    p_gecti = None if p is None else p < 0.05
    sonuc = lambda ok: OLCULEMEDI if ok is None else (GECTI if ok else GECMEDI)  # noqa: E731
    yil = _tamamlanan_yillar(g["yillik"], g["bas"], g["bitis"], g["islem_yok"])
    pozitif = float((g["yillik"].loc[yil] > 0).mean()) if yil else float("nan")
    fazla = np.sort(np.asarray(g["islem_fazla"], dtype=float))[::-1]
    atilmis = (
        float(fazla[int(np.ceil(0.05 * len(fazla))) :].mean())
        if len(fazla)
        else float("nan")
    )
    ornek = g["islem"] >= MIN_ISLEM and g["gun"] >= MIN_GUN
    mde_islem = g["mde"] / g["islem_yil"] if g["islem_yil"] else float("inf")
    olculemedi = (not ornek) or mde_islem > GIDIS_DONUS
    maks, sure = dusus(g["ozkaynak"])
    ret = maks > DUSUS_ESIK or sure > DUSUS_GUN
    sag = g["saglamlik"]
    bir = None if p_gecti is None else (f[0.003] > 0 and p_gecti)
    uc = None if p_gecti is None else (f[0.005] > 0 and pf[0.005] > 0 and p_gecti)
    bes = OLCULEMEDI if not ornek or sag is None else sonuc(sag >= SAGLAMLIK_ESIK)
    satirlar = [
        {
            "no": 1,
            "ad": "K1'e göre fazla getiri pozitif ve Holm p < 0,05",
            "durum": sonuc(bir),
            "ham": [("Fazla getiri %0,3", f[0.003], "yuzde"), ("Holm p", p, "p")],
        },
        {
            "no": 2,
            "ad": "K2'ye göre portföy fazla getirisi pozitif",
            "durum": sonuc(pf[0.003] > 0),
            "ham": [("Günlük fazla getiri ortalaması %0,3", pf[0.003], "yuzde")],
        },
        {
            "no": 3,
            "ad": "Masraf %0,5'te de 1 ve 2",
            "durum": sonuc(uc),
            "ham": [
                ("K1 fazla getiri %0,5", f[0.005], "yuzde"),
                ("Portföy fazla getiri %0,5", pf[0.005], "yuzde"),
            ],
        },
        {
            "no": 4,
            "ad": "Yılların %60'ında pozitif; en iyi %5 işlem atılınca pozitif",
            "durum": sonuc(None if not yil else (pozitif >= YIL_ESIK and atilmis > 0)),
            "ham": [
                ("Pozitif yıl oranı", pozitif, "yuzde"),
                ("En iyi %5 atılmış ortalama", atilmis, "yuzde"),
            ],
        },
        {
            "no": 5,
            "ad": "Örneklem (100 işlem, 60 gün) ve sağlamlık ≥ %60",
            "durum": bes,
            "ham": [
                ("İşlem", g["islem"], "sayi"),
                ("Farklı gün", g["gun"], "sayi"),
                ("Sağlamlık", np.nan if sag is None else sag, "yuzde"),
            ],
        },
        {
            "no": 6,
            "ad": "Kâğıt üstü dönemde etki doğrulamanın yarısı",
            "durum": OLCULEMEDI,
            "ham": [],
        },
    ]
    d = [s["durum"] for s in satirlar]
    genel = (
        GECMEDI
        if ret
        else OLCULEMEDI
        if olculemedi
        else GECMEDI
        if GECMEDI in d
        else OLCULEMEDI
        if OLCULEMEDI in d
        else GECTI
    )
    return {
        "satirlar": satirlar,
        "genel": genel,
        "ret": ret,
        "olculemedi": olculemedi,
        "dusus": (maks, sure),
        "mde_islem": mde_islem,
        "durum": "Kâğıt" if not ret and all(x == GECTI for x in d[:5]) else "Deneme",
    }


def holm(p) -> list:
    """Holm düzeltmeli p'ler, girdi sırasında (statsmodels)."""
    return [float(x) for x in multipletests(list(p), method="holm")[1]]


def p_deger(gercek, rastgele) -> float:
    """p = (1 + k) / (1 + B); k = gerçek kuraldan iyi ya da eşit rastgele tekrar sayısı, tek yönlü (TASARIM 5.7)."""
    if not np.isfinite(gercek):
        return 1.0
    r = np.asarray(rastgele, dtype=float)
    return float(
        (1 + np.sum(np.isnan(r) | (r >= gercek))) / (1 + len(r))
    )  # NaN tekrar iyi sayılır (TASARIM 5.7)


def saptanabilir_etki(g) -> float:
    """Günlük fazla getiri serisinden saptanabilir en küçük etki, yıllık (TASARIM 5.9)."""
    g = np.asarray(g, dtype=float)
    return float((Z_ALFA + Z_GUC) * g.std(ddof=1) / np.sqrt(len(g)) * GUN)


def blok_uzunlugu(ort_tutma) -> int:
    """Blok = max(20, ortalama tutma süresi) (TASARIM 5.9)."""
    return int(max(20, np.ceil(ort_tutma)))


def blok_aralik(g, blok, tekrar=1000, tohum=0) -> tuple:
    """Hareketli blok bootstrap: günlük serinin yıllıklandırılmış ortalamasının 2,5 ve 97,5 yüzdelikleri."""
    g = np.asarray(g, dtype=float)
    n, blok = len(g), min(blok, len(g))
    k = int(np.ceil(n / blok))
    baslar = np.random.default_rng(tohum).integers(0, n - blok + 1, size=(tekrar, k))
    ornek = g[(baslar[:, :, None] + np.arange(blok)).reshape(tekrar, -1)[:, :n]]
    alt, ust = np.percentile(ornek.mean(axis=1) * GUN, [2.5, 97.5])
    return float(alt), float(ust)


def kapali_r_egrisi(islemler, donem):
    gunler = {}
    refs = []
    for i in islemler:
        if i["sonuc"].get("kalan_adet") == 0:
            gun = i["pozisyon"]["cikis_tarih"][:10]
            gunler.setdefault(gun, []).append(i["sonuc"].get("net_r"))
            refs.append(i["islem_ref"])
    satirlar, toplam = [], 0.0
    for t, r in sorted(gunler.items()):
        toplam = toplam + sum(r) if toplam is not None and None not in r else None
        satirlar.append(dict(an=t, deger=toplam))
    return dict(
        tur="tani_net_r",
        satirlar=satirlar,
        baslangic_degeri=0.0,
        baslangic_ani=donem["baslangic"].isoformat(),
        baslangic_politikasi="acik",
        tarih_temeli="takvim_gunu",
        normalizasyon=dict(deger=1.0, birim="R", bos_nedeni=None),
        birim="R",
        muhasebe_politikasi="tani_net_r_v1",
        referanslar=refs,
    )


def ileri_kontrol_sayimi(durum, bolum):
    bas, son = bolum["baslangic"].isoformat(), bolum["bitis"].isoformat()
    giren = [i for i in durum["islemler"] if bas <= i["pozisyon"]["giris_tarih"] <= son]
    p = durum["pozisyon"]
    tarihler = {i["pozisyon"]["giris_tarih"] for i in giren}
    if p and p["giris_tarih"] and bas <= p["giris_tarih"] <= son:
        tarihler.add(p["giris_tarih"])
    return dict(
        kapali_islem=len(giren),
        ayri_giris_gunu=len(tarihler),
        acik_islem=int(bool(p and p["durum"] == "acik")),
        bekleyen_giris=int(bool(p and p["durum"] == "bekliyor")),
    )


def ileri_ozeti(islemler, *, semboller, donem, bolumler):
    """TASARIM 5.15 S12: değişmez nihai işlemlerin ölçü ve giriş kohortu sayımı."""
    semboller = sorted(semboller)
    kaynaklar = {s: [] for s in semboller}
    for i in islemler:
        kaynaklar[i["pozisyon"]["risk_girdisi"]["sembol"]].append(i)
    olculer = {
        s: olc(k, politika="bagimsiz_olcu_v1", egri=kapali_r_egrisi(k, donem))
        for s, k in kaynaklar.items()
    }
    sayimlar = {}
    for b in bolumler:
        bas, son = b["baslangic"].isoformat(), b["bitis"].isoformat()
        sayimlar[b["ad"]] = {}
        for s, kayitlar in kaynaklar.items():
            giren = [i for i in kayitlar if bas <= i["pozisyon"]["giris_tarih"] <= son]
            sayimlar[b["ad"]][s] = dict(
                kapali_islem=sum(_kapali_sonuc(i["sonuc"]) for i in giren),
                ayri_giris_gunu=len({i["pozisyon"]["giris_tarih"] for i in giren}),
                acik_islem=sum(not _kapali_sonuc(i["sonuc"]) for i in giren),
            )
    return dict(olculer=olculer, giris_kohort_sayimlari=sayimlar)
