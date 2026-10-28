"""Ağa çıkan tek modül: İş Yatırım (TASARIM 4; kullanım kararı `docs/arastirma/kullanim-kosullari-fiyat-adimi.md`)."""

import datetime as dt
import io
import json
import re
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import requests

KOK = "https://www.isyatirim.com.tr"
FIYAT_URL = KOK + "/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil"
OLAY_URL = (
    KOK
    + "/_layouts/15/IsYatirim.Website/StockInfo/CompanyInfoAjax.aspx/GetSermayeArttirimlari"
)
CEREZ_URL = KOK + "/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx"
KAPANAN_URL = "https://www.borsaistanbul.com/datum/IslemSirasiKapananSirketler.xls"
USER_AGENT = "tansu-kisisel/0.1"

# İş Yatırım alanı → proje adı. ham_* düzeltmesiz (HG), diğerleri düzeltilmiş (HGDG).
ALANLAR = {
    "HG_KAPANIS": "ham_kapanis",
    "HG_AOF": "ham_aof",
    "HG_MAX": "ham_yuksek",
    "HG_MIN": "ham_dusuk",
    "HG_HACIM": "hacim",
    "HGDG_KAPANIS": "kapanis",
    "HGDG_AOF": "aof",
    "HGDG_MAX": "yuksek",
    "HGDG_MIN": "dusuk",
    "PD": "pd",
    "HAO_PD": "hao_pd",
    "SERMAYE": "sermaye",
    "END_DEGER": "xu100",
}
OLAY_ALANLARI = {
    "SHT_KODU",
    "SHHE_TARIH",
    "SHHE_FIYAT_AYAR_OR",
}  # veri.oku bunları okur


class KaynakHatasi(Exception):
    pass


def _sema(sembol, kayitlar, alanlar):
    eksik = set().union(*(alanlar - set(k) for k in kayitlar))
    if eksik:
        raise KaynakHatasi(f"{sembol}: eksik alan {sorted(eksik)}")


class IsYatirim:
    def __init__(
        self, oturum=None, bekleme=1.0, zaman_asimi=(5, 120), deneme_bekleme=(5, 15, 45)
    ):
        self.oturum = oturum or requests.Session()
        self.oturum.headers["User-Agent"] = USER_AGENT
        self.bekleme, self.zaman_asimi, self.deneme_bekleme = (
            bekleme,
            zaman_asimi,
            deneme_bekleme,
        )
        self._cerez = oturum is not None  # sahte oturumda çerez adımı yok

    def fiyat(self, sembol, bas, son) -> pd.DataFrame:
        """Tek istek; başarısızsa yıl yıl. Kaynak bazı sembollerde uzun aralığa boş yanıt verir (ALARK, 26.10.2026)."""
        try:
            return self._fiyat(sembol, bas, son)
        except KaynakHatasi:
            if bas.year == son.year:
                raise
        parcalar = [
            self._fiyat(
                sembol, max(bas, dt.date(y, 1, 1)), min(son, dt.date(y, 12, 31))
            )
            for y in range(bas.year, son.year + 1)
        ]
        return (
            pd.concat([p for p in parcalar if not p.empty] or parcalar[:1])
            .drop_duplicates("tarih")
            .sort_values("tarih", kind="stable")
            .reset_index(drop=True)
        )

    def _fiyat(self, sembol, bas, son) -> pd.DataFrame:
        govde = self._iste(
            "get",
            FIYAT_URL,
            params={
                "hisse": sembol,
                "startdate": bas.strftime("%d-%m-%Y"),
                "enddate": son.strftime("%d-%m-%Y"),
            },
        )
        kayitlar = govde.get("value") if isinstance(govde, dict) else None
        if kayitlar is None:
            raise KaynakHatasi(f"{sembol}: 'value' yok")
        if not kayitlar:
            return pd.DataFrame(columns=["tarih", *ALANLAR.values()])
        _sema(sembol, kayitlar, {"HGDG_TARIH", *ALANLAR})
        f = pd.DataFrame(kayitlar)
        f = f[["HGDG_TARIH", *ALANLAR]].rename(
            columns={"HGDG_TARIH": "tarih", **ALANLAR}
        )
        f["tarih"] = pd.to_datetime(f["tarih"], format="%d-%m-%Y")
        return f.sort_values("tarih", kind="stable").reset_index(
            drop=True
        )  # GARAN yanıtı sırasız (TASARIM 5.13)

    def olaylar(self, sembol) -> list:
        """Ham `GetSermayeArttirimlari` kayıtları, bütün kodlarıyla (süzme yok)."""
        if not self._cerez:  # uç nokta önce şirket sayfasından oturum çerezi ister
            self._iste("get", CEREZ_URL, params={"hisse": sembol}, json_bekle=False)
            self._cerez = True
        govde = self._iste(
            "post",
            OLAY_URL,
            json={
                "hisseKodu": sembol,
                "hisseTanimKodu": "",
                "yil": 0,
                "zaman": "HEPSI",
                "endeksKodu": "09",
                "sektorKodu": "",
            },
        )
        d = govde.get("d") if isinstance(govde, dict) else None
        if d is None:
            raise KaynakHatasi(f"{sembol}: olay yanıtında 'd' yok")
        kayitlar = json.loads(d) if isinstance(d, str) else d
        _sema(sembol, kayitlar, OLAY_ALANLARI)
        return kayitlar

    def _iste(self, yontem, url, json_bekle=True, **kw):
        bekle = (0, *self.deneme_bekleme)
        for n, sure in enumerate(bekle):
            time.sleep(sure)
            try:
                yanit = getattr(self.oturum, yontem)(
                    url, timeout=self.zaman_asimi, **kw
                )
                if yanit.status_code == 429 or yanit.status_code >= 500:
                    raise requests.HTTPError(str(yanit.status_code))
                if yanit.status_code >= 400:  # kalıcı hata: yeniden deneme yok
                    raise KaynakHatasi(f"{url}: HTTP {yanit.status_code}")
                time.sleep(self.bekleme)
                return yanit.json() if json_bekle else None
            except (
                requests.ConnectionError,
                requests.Timeout,
                requests.HTTPError,
                ValueError,
            ) as hata:  # ValueError: JSON değil
                son_hata = hata
        raise KaynakHatasi(f"{url}: {len(bekle)} denemede alınamadı ({son_hata})")


def kapanan_tablo(ham) -> pd.DataFrame:
    """Borsa İstanbul "İşlem Sırası Kapanan Şirketler" tablosundan pay kodları: kod, ad, tarih, aciklama.

    Fon ve diğer türler (`.F1` vb.) ve 2010 öncesi kapananlar atılır; tarihsiz satır kalır."""
    t = ham.iloc[4:, :4].set_axis(["kod", "ad", "tarih", "aciklama"], axis=1)
    t = t[t["kod"].astype(str).str.fullmatch(r"[A-Z0-9]+(\.E)?")].copy()
    t["kod"] = t["kod"].str.removesuffix(".E")
    t["tarih"] = pd.to_datetime(t["tarih"])
    return t[~(t["tarih"] < "2010-01-01")].reset_index(drop=True)


def kapanan_kodlar(oturum=None) -> pd.DataFrame:
    """İşlemi kapanmış pay kodları (Borsa İstanbul, birincil kaynak; `Data/DataFilePaths` listesinde)."""
    oturum = oturum or requests.Session()
    yanit = oturum.get(
        KAPANAN_URL, timeout=(5, 120), headers={"User-Agent": USER_AGENT}
    )
    if yanit.status_code != 200:
        raise KaynakHatasi(f"{KAPANAN_URL}: HTTP {yanit.status_code}")
    return kapanan_tablo(
        pd.read_excel(io.BytesIO(yanit.content), header=None)
    )  # .xls için xlrd


def sirket_kodlari() -> pd.Series:
    """Bugünkü bütün pay kodları (borsapy `companies`, KAP şirket listesi). Ağa çıkan tek yer burasıdır (TASARIM 4)."""
    import borsapy

    return borsapy.companies()["ticker"]


class Onbellekli:
    """Sembol başına yanıtı klasöre yazar. Saatler süren evren indirmesi yarıda kesilirse yeniden başlayınca
    tamamlanan semboller tekrar istenmez. Hata yazılmaz; yalnız başarılı yanıt saklanır."""

    def __init__(self, kaynak, klasor):
        self._kaynak, self._klasor = kaynak, Path(klasor)
        self._klasor.mkdir(parents=True, exist_ok=True)

    def fiyat(self, sembol, bas, son) -> pd.DataFrame:
        yol = self._klasor / f"{sembol}.fiyat.parquet"
        if yol.exists():
            return pd.read_parquet(yol)
        f = self._kaynak.fiyat(sembol, bas, son)
        f.to_parquet(yol, index=False)
        return f

    def olaylar(self, sembol) -> list:
        yol = self._klasor / f"{sembol}.olaylar.json"
        if yol.exists():
            return json.loads(yol.read_text(encoding="utf-8"))
        o = self._kaynak.olaylar(sembol)
        yol.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
        return o


class Artimli:
    """Günlük güncelleme (SPEC 3.8): sembol başına son yanıtı saklar, kaynaktan yalnız son `ORTUSME` günü ister.

    Örtüşen günler önbellekle aynı değilse (yeni bölünme ya da temettü düzeltilmiş geçmişi değiştirir) sembolün
    bütün geçmişi ve olayları yeniden istenir. Önbelleğin son günü seans içi olabilir; karşılaştırılmaz, yenisi alınır.
    `sayac`: bu koşuda kaç sembol artımlı, kaç sembol tam indi. Klasör başlangıç tarihine göre ayrı tutulur."""

    ORTUSME = 10  # işlem günü

    def __init__(self, kaynak, klasor):
        self._kaynak, self._klasor = kaynak, Path(klasor)
        self._klasor.mkdir(parents=True, exist_ok=True)
        self._tam = set()
        self.sayac = Counter()

    def fiyat(self, sembol, bas, son) -> pd.DataFrame:
        yol = self._klasor / f"{sembol}.fiyat.parquet"
        eski = pd.read_parquet(yol) if yol.exists() else None
        if eski is not None and len(eski) > self.ORTUSME:
            kes = eski["tarih"].iloc[-self.ORTUSME]
            yeni = self._kaynak.fiyat(sembol, kes.date(), son)
            ortak = eski[eski["tarih"] >= kes].iloc[:-1].set_index("tarih")
            gelen = yeni.drop_duplicates("tarih").set_index("tarih")
            gelen = gelen.reindex(ortak.index)[ortak.columns]
            if np.allclose(ortak, gelen, rtol=1e-6, atol=0, equal_nan=True):
                f = pd.concat([eski[eski["tarih"] < kes], yeni], ignore_index=True)
                f.to_parquet(yol, index=False)
                self.sayac["artimli"] += 1
                return f
        f = self._kaynak.fiyat(sembol, bas, son)
        f.to_parquet(yol, index=False)
        self._tam.add(sembol)
        self.sayac["tam"] += 1
        return f

    def olaylar(self, sembol) -> list:
        # ponytail: olaylar yalnız tam inişte yenilenir. Kaynak düzeltmeyi geç yansıtırsa o günün görüntüsü eski
        # olayla kurulur, ertesi koşu düzeltir. Sorun olursa olayları her koşuda iste (koşu ≈ iki katı sürer).
        yol = self._klasor / f"{sembol}.olaylar.json"
        if sembol not in self._tam and yol.exists():
            return json.loads(yol.read_text(encoding="utf-8"))
        o = self._kaynak.olaylar(sembol)
        yol.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
        return o


class KapSektor:
    """Toplu sektör okuma (TASARIM 4, bilet 11): KAP şirket listesi bir kez, sembol başına bir şirket sayfası.
    İstekler arası `bekleme` sn, User-Agent `tansu-kisisel/0.1`. Düzenler borsapy 0.11.0 `_providers/kap.py`'den."""

    LISTE_URL = "https://www.kap.org.tr/tr/bist-sirketler"
    SAYFA_URL = "https://kap.org.tr/tr/sirket-bilgileri/ozet"
    LISTE_DUZENI = (
        r'\\"mkkMemberOid\\":\\"([^\\"]+)\\",\\"kapMemberTitle\\":\\"[^\\"]+\\",'
        r'\\"relatedMemberTitle\\":\\"[^\\"]*\\",\\"stockCode\\":\\"([^\\"]+)\\"'
    )
    SEKTOR_DUZENI = r'href="/tr/Sektorler\?sector=[^"]*">([^<]+)</a>'

    def __init__(self, oturum=None, bekleme=1.0, zaman_asimi=(5, 30)):
        self.oturum = oturum or requests.Session()
        self.oturum.headers["User-Agent"] = USER_AGENT
        self.bekleme, self.zaman_asimi, self._oid = bekleme, zaman_asimi, None

    def _al(self, url) -> str:
        try:
            yanit = self.oturum.get(url, timeout=self.zaman_asimi)
        except requests.RequestException as hata:
            raise KaynakHatasi(f"{url}: {hata}") from hata
        time.sleep(self.bekleme)
        if yanit.status_code != 200:
            raise KaynakHatasi(f"{url}: HTTP {yanit.status_code}")
        return yanit.text

    def sektor(self, sembol):
        """Sektör adı; KAP listesinde olmayan kod için None; engel, ağ hatası ya da sektörsüz sayfa için KaynakHatasi
        (sayfa 200 ama sektör yoksa engel sayfası olabilir: sektörsüz diye yazılmaz)."""
        if self._oid is None:
            self._oid = {
                kod.strip(): oid
                for oid, kodlar in re.findall(
                    self.LISTE_DUZENI, self._al(self.LISTE_URL)
                )
                for kod in kodlar.split(",")
            }
        if sembol not in self._oid:
            return None
        bulunan = re.search(
            self.SEKTOR_DUZENI, self._al(f"{self.SAYFA_URL}/{self._oid[sembol]}")
        )
        if not bulunan:
            raise KaynakHatasi(f"{sembol}: şirket sayfasında sektör yok")
        return bulunan.group(1).strip()


class Borsapy:
    """Yalnız faiz (TCMB '1 Hafta Repo' sayfası) ve sektör (KAP şirket sayfası). TradingView'e dokunmaz:
    borsapy kaynak kodundan doğrulandı (`_providers/tcmb_rates.py`, `_providers/kap.py`)."""

    def __init__(self, tcmb=None, kap=None):
        if tcmb is None or kap is None:  # sahte nesne verilmezse borsapy'yi geç yükle
            import borsapy
            from borsapy._providers.kap import get_kap_provider

            tcmb, kap = tcmb or borsapy.TCMB(), kap or get_kap_provider()
        self._tcmb, self._kap = tcmb, kap

    def faiz(self) -> pd.DataFrame:
        """Politika faizi, yalnız değişim günleri: tarih, faiz (yüzde)."""
        h = self._tcmb.history("policy")
        return pd.DataFrame(
            {
                "tarih": pd.DatetimeIndex(h.index).normalize(),
                "faiz": h["lending"].astype(float).to_numpy(),
            }
        )

    def sektor(self, sembol) -> str:
        ad = self._kap.get_company_details(sembol).get("sector")
        if not ad:  # borsapy ağ hatasında sessizce {} döndürür
            raise KaynakHatasi(f"{sembol}: KAP sektörü alınamadı")
        return ad
