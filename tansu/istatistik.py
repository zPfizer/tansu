"""İstatistik: p değeri, Holm, blok bootstrap, saptanabilir en küçük etki, K1 ve kabul tablosu (TASARIM 5.7, 5.9, 5.12)."""

from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from tansu import aileler, cift, ciftbolme, gostergeler, motor, simulator

GUN = 252  # yıllıklandırma
Z_ALFA, Z_GUC = 1.645, 0.842  # tek yönlü %5, güç %80 (TASARIM 5.9)
K1_MASRAF = 0.005  # Holm'a giren p %0,5 masrafla (TASARIM 5.7)
K1_PENCERE = 20  # tür (b): ±20 gün (TASARIM 5.7)


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
        uye_gun = uye.groupby("sembol")["tarih"].agg(pd.DatetimeIndex)
        self.zincir, self.gercek, self.sayi = {}, {}, Counter()
        self.havuz = {"a": defaultdict(list), "ek": defaultdict(list)}
        self.komsu, self.komsusuz = (
            {},
            [],
        )  # (sembol, konum) -> tür (b) adayları; komşusuz sinyaller
        for s in sorted(uye_gun.index):
            m = motor.mumlar(anlik, s, p, atr_n)
            f = m.dropna(subset=["kapanis"])
            z = self.zincir[s] = motor.Zincir(m)
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

    def tablo(self, secim) -> tuple:
        """(işlem tablosu, düşen sinyal sayısı): `motor.sinama` ile aynı sütunlar."""
        kapali, sembol, dusen = [], [], 0
        for s in sorted(secim):
            k, d = self.zincir[s].kapali(secim[s])
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
    istatistik = lambda secim: ortalama_fazla(
        simulator.k1_islemler(k.tablo(secim)[0], b, masraf)
    )  # noqa: E731
    gercek = istatistik(k.gercek)
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
SAGLAMLIK_ESIK, YIL_ESIK = 0.60, 0.60  # TASARIM 5.10, 5.12.4
DUSUS_ESIK, DUSUS_GUN = 0.25, 365  # TASARIM 5.12 portföy kuralı
GIDIS_DONUS = 2 * K1_MASRAF  # TASARIM 5.12 "Ölçülemedi"
GECTI, GECMEDI, OLCULEMEDI = "Geçti", "Geçmedi", "Ölçülemedi"


def dusus(ozkaynak) -> tuple:
    """(en büyük düşüş oranı, düşüşte kalma süresi takvim günü): önceki zirvenin altında kalınan en uzun süre, kapanış bazlı."""
    zirve, zirve_gun, en_buyuk, sure = -np.inf, None, 0.0, 0
    for gun, v in ozkaynak.items():
        if v >= zirve:
            sure = max(sure, (gun - zirve_gun).days if zirve_gun is not None else 0)
            zirve, zirve_gun = v, gun
        else:
            en_buyuk = max(en_buyuk, (zirve - v) / zirve)
    if ozkaynak.iloc[-1] < zirve:
        sure = max(sure, (ozkaynak.index[-1] - zirve_gun).days)
    return float(en_buyuk), int(sure)


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
    return float((1 + np.sum(r >= gercek)) / (1 + len(r)))


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
