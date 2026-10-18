"""E4/E6 ayar aktarımı; hesap E2/E3'te, ekleme E5'tedir (TASARIM 5.15 S07)."""

from dataclasses import asdict, replace
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from uuid import uuid4

import pandas as pd

from tansu import aileler, deneme, katalog, motor, simulator


class AyarAktarimi:
    def __init__(self, depo, deneme_id=None, *, p=None, kosu_id=None, veri_ref=None):
        self.depo, self.deneme_id = depo, deneme_id
        self.kosu_id = (
            kosu_id or f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid4().hex[:6]}"
        )
        self.veri_ref = veri_ref
        self.kayit = depo.deneme_oku(deneme_id) if deneme_id is not None else None
        if self.kayit is not None:
            p = aileler.Parametre(
                **{a["ad"]: a["deger"] for a in self.kayit["strateji"]["parametreler"]}
            )
        if p is None:
            raise deneme.PilotHatasi(f"{deneme_id or self.kosu_id}: ayar eksik")
        self.p = p
        self.ozet = (
            self.kayit["ayar_parmak_izi"]
            if self.kayit is not None
            else f"kayitsiz:sha256:{sha256(deneme.kanonik(asdict(p))).hexdigest()}"
        )
        if veri_ref is not None:
            self.veri_bagla(veri_ref)

    def veri_bagla(self, kimlik):
        if (
            self.kayit is not None
            and kimlik not in self.kayit["veri_ayarlari"]["veri_referanslari"]
        ):
            raise deneme.PilotHatasi(
                f"{self.deneme_id}: veri referansı uyuşmuyor: {kimlik}"
            )
        self.veri_ref = kimlik

    def aile_dogrula(self, aileler):
        """TASARIM 5.15: EMA katalog kaydıyla çift hesabı yapılmaz."""
        if self.kayit is not None and tuple(aileler) != (simulator.AILE,):
            raise deneme.PilotHatasi(
                f"{self.deneme_id}: kayıtlı EMA ayarı bu ailelerle kullanılamaz: {', '.join(aileler)}; --aile ema_sikismasi gerekli"
            )

    def ayar_dogrula(self, p):
        if p != self.p:
            raise deneme.PilotHatasi(
                f"{self.deneme_id or self.kosu_id}: yürütme ayarı uyuşmuyor"
            )
        if self.kayit is not None:
            kayit = self.depo.deneme_oku(self.deneme_id)
            parametreler = {
                a["ad"]: a["deger"] for a in kayit["strateji"]["parametreler"]
            }
            if kayit["ayar_parmak_izi"] != self.ozet or parametreler != asdict(p):
                raise deneme.PilotHatasi(f"{self.deneme_id}: ayar özeti değişti")

    def cocuk(self, hucre):
        if self.kayit is None:
            return AyarAktarimi(
                self.depo,
                p=replace(self.p, **hucre),
                kosu_id=self.kosu_id,
                veri_ref=self.veri_ref,
            )
        s = self.kayit["strateji"]
        sayisal = {
            a["ad"]: a["deger"]
            for a in s["parametreler"]
            if a["koken"] == "legacy_izgara"
        }
        try:
            strateji = katalog.legacy_coz(
                s["varyant"], s["katalog_surumu"], sayisal_ayarlar={**sayisal, **hucre}
            )
        except (katalog.KatalogHatasi, OverflowError) as hata:
            raise deneme.PilotHatasi(
                f"{self.deneme_id}: geçersiz hücre ayarı: {hata}"
            ) from hata
        makbuz = self.depo.deneme_kaydet(
            strateji,
            aktor="S07",
            gerekce="Eski ızgara hücresi",
            ust_deneme=self.deneme_id,
            baglar={"izgara_ust_deneme": self.deneme_id},
            **{
                a: self.kayit[a]
                for a in (
                    "donemler",
                    "veri_ayarlari",
                    "yontem_ayarlari",
                    "risk_ayarlari",
                    "masraf_ayarlari",
                    "eski_referans",
                )
            },
        )
        return AyarAktarimi(
            self.depo, makbuz.deneme_id, kosu_id=self.kosu_id, veri_ref=self.veri_ref
        )

    def _yaz(self, asama, icerik, referanslar):
        self.ayar_dogrula(self.p)
        return self.depo.bag_kaydet(
            kosu_id=self.kosu_id,
            asama=asama,
            deneme_id=self.deneme_id,
            ayar_ozeti=self.ozet,
            veri_ref=self.veri_ref,
            referanslar=referanslar,
            icerik=icerik,
        ).olay_id

    def _oku(self, kimlik):
        olay = next((o for o in self.depo.oku() if o["kayit_id"] == kimlik), None)
        if olay is None or any(
            olay.get(a) != v
            for a, v in (
                ("kosu_id", self.kosu_id),
                ("deneme_id", self.deneme_id),
                ("ayar_parmak_izi", self.ozet),
                ("veri_ref_id", self.veri_ref),
            )
        ):
            raise deneme.PilotHatasi(f"{kimlik}: ayar bağı uyuşmuyor")
        return olay

    def sinyaller(self, m, kurulum, sembol):
        self.ayar_dogrula(self.p)
        if kurulum is None or not {"kutu_alt", "hedef"} <= set(kurulum.columns):
            raise deneme.PilotHatasi(f"{self.deneme_id or self.kosu_id}: kurulum eksik")
        kayitlar = {}
        for tarih, r in kurulum.iterrows():
            kimlik = f"{self.deneme_id or self.kosu_id}:{sembol}:{tarih.isoformat()}"
            if self.kayit is not None:
                gerekli = [m.at[tarih, "atr"]]
                if self.p.stop == "kutu":
                    gerekli.append(r.kutu_alt)
                if self.p.hedef != "yok":
                    gerekli.append(r.hedef)
                if any(pd.isna(v) or not math.isfinite(v) for v in gerekli):
                    raise deneme.PilotHatasi(f"{kimlik}: gerekli kurulum değeri eksik")
            kayitlar[tarih] = self._yaz(
                "sinyal",
                {
                    "sembol": sembol,
                    "tarih": tarih.isoformat(),
                    "kutu_alt": None if pd.isna(r.kutu_alt) else float(r.kutu_alt),
                    "hedef": None if pd.isna(r.hedef) else float(r.hedef),
                },
                [],
            )
        return kayitlar

    def ema(self, m, kurulum, sembol):
        kurulum = kurulum[~kurulum.index.duplicated()]
        sinyaller = self.sinyaller(m, kurulum, sembol)
        for kimlik in sinyaller.values():
            self._oku(kimlik)  # E2 → E3, hesap başlamadan.
        zincir = motor.Zincir(m, self.p, kurulum)
        tablo, dusen = zincir.calistir(m.index.get_indexer(kurulum.index))
        self.ayar_dogrula(zincir.ayar)
        return tablo, dusen, self.islemler(tablo, sinyaller)

    def islemler(self, tablo, sinyaller):
        satirlar = json.loads(tablo.to_json(orient="records", date_format="iso"))
        return [
            self._yaz("islem", r, [sinyaller[t]])
            for t, r in zip(tablo["sinyal_tarih"], satirlar, strict=True)
        ]

    def sonuc(self, icerik, islemler):
        return self._yaz("sonuc", icerik, islemler)

    def pozisyonlar(self, pozisyonlar, sinyaller):
        referanslar = []
        for p in pozisyonlar:
            self.ayar_dogrula(p.ayar)
            referanslar.append(
                self._yaz(
                    "islem",
                    {
                        "durum": p.durum,
                        "stop": p.stop,
                        "neden": p.neden,
                        "giris_fiyat": p.giris_fiyat,
                        "cikis_fiyat": p.cikis_fiyat,
                    },
                    [sinyaller[p.sinyal_tarih]],
                )
            )
        return referanslar
