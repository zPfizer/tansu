"""Ağa çıkan tek modül: İş Yatırım (TASARIM 4; kullanım kararı `docs/arastirma/kullanim-kosullari-fiyat-adimi.md`)."""

import json
import time

import pandas as pd
import requests

KOK = "https://www.isyatirim.com.tr"
FIYAT_URL = KOK + "/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil"
OLAY_URL = KOK + "/_layouts/15/IsYatirim.Website/StockInfo/CompanyInfoAjax.aspx/GetSermayeArttirimlari"
CEREZ_URL = KOK + "/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx"
USER_AGENT = "tansu-kisisel/0.1"

# İş Yatırım alanı → proje adı. ham_* düzeltmesiz (HG), diğerleri düzeltilmiş (HGDG).
ALANLAR = {
    "HG_KAPANIS": "ham_kapanis", "HG_AOF": "ham_aof", "HG_MAX": "ham_yuksek", "HG_MIN": "ham_dusuk",
    "HG_HACIM": "hacim", "HGDG_KAPANIS": "kapanis", "HGDG_AOF": "aof", "HGDG_MAX": "yuksek",
    "HGDG_MIN": "dusuk", "PD": "pd", "HAO_PD": "hao_pd", "SERMAYE": "sermaye", "END_DEGER": "xu100",
}
OLAY_ALANLARI = {"SHT_KODU", "SHHE_TARIH", "SHHE_FIYAT_AYAR_OR"}  # veri.oku bunları okur


class KaynakHatasi(Exception):
    pass


def _sema(sembol, kayitlar, alanlar):
    eksik = set().union(*(alanlar - set(k) for k in kayitlar))
    if eksik:
        raise KaynakHatasi(f"{sembol}: eksik alan {sorted(eksik)}")


class IsYatirim:
    def __init__(self, oturum=None, bekleme=1.0, zaman_asimi=(5, 120), deneme_bekleme=(5, 15, 45)):
        self.oturum = oturum or requests.Session()
        self.oturum.headers["User-Agent"] = USER_AGENT
        self.bekleme, self.zaman_asimi, self.deneme_bekleme = bekleme, zaman_asimi, deneme_bekleme
        self._cerez = oturum is not None  # sahte oturumda çerez adımı yok

    def fiyat(self, sembol, bas, son) -> pd.DataFrame:
        govde = self._iste("get", FIYAT_URL, params={
            "hisse": sembol, "startdate": bas.strftime("%d-%m-%Y"), "enddate": son.strftime("%d-%m-%Y")})
        kayitlar = govde.get("value") if isinstance(govde, dict) else None
        if kayitlar is None:
            raise KaynakHatasi(f"{sembol}: 'value' yok")
        if not kayitlar:
            return pd.DataFrame(columns=["tarih", *ALANLAR.values()])
        _sema(sembol, kayitlar, {"HGDG_TARIH", *ALANLAR})
        f = pd.DataFrame(kayitlar)
        f = f[["HGDG_TARIH", *ALANLAR]].rename(columns={"HGDG_TARIH": "tarih", **ALANLAR})
        f["tarih"] = pd.to_datetime(f["tarih"], format="%d-%m-%Y")
        return f

    def olaylar(self, sembol) -> list:
        """Ham `GetSermayeArttirimlari` kayıtları, bütün kodlarıyla (süzme yok)."""
        if not self._cerez:  # uç nokta önce şirket sayfasından oturum çerezi ister
            self._iste("get", CEREZ_URL, params={"hisse": sembol}, json_bekle=False)
            self._cerez = True
        govde = self._iste("post", OLAY_URL, json={
            "hisseKodu": sembol, "hisseTanimKodu": "", "yil": 0, "zaman": "HEPSI",
            "endeksKodu": "09", "sektorKodu": ""})
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
                yanit = getattr(self.oturum, yontem)(url, timeout=self.zaman_asimi, **kw)
                if yanit.status_code == 429 or yanit.status_code >= 500:
                    raise requests.HTTPError(str(yanit.status_code))
                if yanit.status_code >= 400:  # kalıcı hata: yeniden deneme yok
                    raise KaynakHatasi(f"{url}: HTTP {yanit.status_code}")
                time.sleep(self.bekleme)
                return yanit.json() if json_bekle else None
            except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as hata:
                son_hata = hata
        raise KaynakHatasi(f"{url}: {len(bekle)} denemede alınamadı ({son_hata})")


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
        return pd.DataFrame({"tarih": pd.DatetimeIndex(h.index).normalize(), "faiz": h["lending"].astype(float).to_numpy()})

    def sektor(self, sembol) -> str:
        ad = self._kap.get_company_details(sembol).get("sector")
        if not ad:  # borsapy ağ hatasında sessizce {} döndürür
            raise KaynakHatasi(f"{sembol}: KAP sektörü alınamadı")
        return ad
