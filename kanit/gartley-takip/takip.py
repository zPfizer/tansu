"""Gartley para takibi: dondurulmuş ayar, 01.10.2026'dan beri, 100.000 TL, taze BIST verisi (kanit/gartley-takip.md).

Kullanım:
  takip.py [veri-klasörü] [--mevcut] [--cikti <klasör>]

Her koşu veriyi günceller (artımlı), ayarı değiştirmeden 01.10.2026'dan son tam işlem gününe kadar koşturur ve
`kayit/<son gün>/` altına yeni bir kayıt yazar. Var olan kayıt klasörünün üstüne asla yazmaz.
`--mevcut`: indirme yok, veri klasöründeki son anlık görüntü kullanılır. `--cikti`: kayıt kökü (varsayılan: bu betiğin
yanındaki `kayit/`).
"""

import argparse
import datetime as dt
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

BU = Path(__file__).resolve().parent
REPO = BU.parents[1]
PARA_KLASORU = REPO / "kanit" / "gartley-para"
sys.path[:0] = [
    str(REPO),
    str(PARA_KLASORU),
]  # tansu bu depodan gelir; işçi süreçler de para'yı bulur

from tansu import islem, kaynak, sinama, veri  # noqa: E402

para = importlib.import_module("para")

AYAR_SHA = "118ad754930a67cb70f4ace06de0981142e1a5539dcdfe15ca6e2eb0d43e32e6"
PARA_SHA = "95dfd8a9774e61a4be56087b3d106b7de56483c81ae67fb4a0e9dc51a130dd83"
BASLANGIC = pd.Timestamp("2026-10-01")
VERI_BASLANGIC = dt.date(2024, 1, 1)  # ısınma: pivot, ATR ve karantina geçmişi
SERMAYE = para.SERMAYE
KAPANIS_SAATI = 19  # İstanbul; bu saatten önceki bugün tam gün sayılmaz
EN_AZ_PAY = 0.9  # son günün satır sayısı bir önceki günün en az bu payı olmalı (kaynak günü yarım gelebilir)
VARSAYILAN_KOK = Path(r"C:\Users\levent\Desktop\TANSU\veri\takip-gartley")
KAYIT_KOKU = BU / "kayit"
ATLANAN_DOSYA = "atlanan-gunler.json"


def sha256(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()


def git(*arg: str) -> str:
    cikti = subprocess.run(
        ["git", "-C", str(REPO), *arg],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return cikti.stdout.strip()


def dondurulmus_ayar() -> Path:
    """Ayar ve para katmanı dondurulmuş dosyalarsa ayar yolunu döndürür; değilse durur."""
    for yol, beklenen in (
        (PARA_KLASORU / "ayar.json", AYAR_SHA),
        (PARA_KLASORU / "para.py", PARA_SHA),
    ):
        gercek = sha256(yol)
        if gercek != beklenen:
            raise SystemExit(
                f"dondurulmuş dosya değişmiş: {yol.name} {gercek} != {beklenen}"
            )
    return PARA_KLASORU / "ayar.json"


# --- Veri ---


class KaynakKaydi:
    """Kaynağın atladığı günleri toplar: `f.attrs["atlanan_gunler"]` indirmeden sonra kalmaz."""

    def __init__(self, ic):
        self._ic, self.atlanan = ic, {}

    def fiyat(self, sembol, bas, son):
        f = self._ic.fiyat(sembol, bas, son)
        if f.attrs.get("atlanan_gunler"):
            self.atlanan[sembol] = list(f.attrs["atlanan_gunler"])
        return f

    def olaylar(self, sembol):
        return self._ic.olaylar(sembol)


def indir(kok: Path) -> str:
    """Bütün BIST (bugünkü kodlar + kapananlar) 2024'ten bugüne; önbellek artımlıdır. Anlık görüntü kimliğini döndürür."""
    kapanan = kaynak.kapanan_kodlar()
    kapanan = kapanan[~(kapanan["tarih"] < pd.Timestamp(VERI_BASLANGIC))]
    semboller = sorted(
        {*kaynak.sirket_kodlari().astype(str).str.strip(), *kapanan["kod"]}
    )
    kayitci = KaynakKaydi(kaynak.IsYatirim())
    onbellek = kaynak.Artimli(
        kayitci, kok / "onbellek" / f"fiyat-{VERI_BASLANGIC:%Y%m%d}"
    )
    kimlik = veri.indir(semboller, kok, onbellek, bas=VERI_BASLANGIC, kapanan=kapanan)
    yol = (
        kok / ATLANAN_DOSYA
    )  # birikimli: önceki koşularda atlanan gün sonraki artımlı koşuda yeniden istenmez
    eski = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}
    for sembol, gunler in kayitci.atlanan.items():
        eski[sembol] = sorted({*eski.get(sembol, []), *gunler})
    yol.write_text(
        json.dumps(eski, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8"
    )
    print(
        f"önbellek: {onbellek.sayac['artimli']} artımlı, {onbellek.sayac['tam']} tam; kaynağın atladığı: {len(kayitci.atlanan)} sembol"
    )
    return kimlik


def son_kimlik(kok: Path) -> str:
    klasorler = sorted(p.name for p in (kok / "ag").glob("2*"))
    if not klasorler:
        raise SystemExit(f"anlık görüntü yok: {kok / 'ag'}")
    return klasorler[-1]


def faiz_al(kok: Path, kimlik: str, mevcut: bool) -> pd.DataFrame:
    """Politika faizi projenin kaynağından (TCMB); anlık görüntüyle eşlenik saklanır, `--mevcut` aynısını okur."""
    yol = kok / "faiz" / f"{kimlik}.parquet"
    if not mevcut:
        faiz = kaynak.Borsapy().faiz()
        if faiz.empty:
            raise SystemExit("faiz serisi boş")
        yol.parent.mkdir(parents=True, exist_ok=True)
        faiz.to_parquet(yol, index=False)
    return pd.read_parquet(yol)


def yeni_kayit_yolu(kayit_koku: Path, son: pd.Timestamp) -> Path:
    """O güne ait kayıt klasörü varsa durur (üstüne yazılmaz); yoksa yolunu döndürür."""
    hedef = kayit_koku / son.strftime("%Y%m%d")
    if hedef.exists():
        raise SystemExit(
            f"kayıt zaten var: {hedef}; üstüne yazılmaz. Sonraki işlem gününden sonra yeniden koş."
        )
    return hedef


def beklenen_son_gun() -> pd.Timestamp:
    """İndirmeden önce kaynağa tek istek (THYAO, son 10 gün): son tam işlem günü, `son_gun` ile aynı seans kuralı."""
    simdi = dt.datetime.now(veri.ISTANBUL)
    f = kaynak.IsYatirim().fiyat(
        "THYAO", simdi.date() - dt.timedelta(days=10), simdi.date()
    )
    gunler = f.loc[f["xu100"] > 0, "tarih"]
    if simdi.hour < KAPANIS_SAATI:
        gunler = gunler[gunler.dt.date < simdi.date()]
    return gunler.max()


def son_gun(anlik: veri.Anlik) -> pd.Timestamp:
    """Son tam işlem günü: seans sonrası alınmış ve satır sayısı bir önceki günden belirgin az olmayan son gün."""
    cekim = dt.datetime.strptime(anlik.kimlik, "%Y%m%d-%H%M")
    gunler = anlik.gunler
    sayi = anlik.fiyat.groupby("tarih").size()
    for i in range(len(gunler) - 1, 0, -1):
        gun = gunler[i]
        erken = gun.date() == cekim.date() and cekim.hour < KAPANIS_SAATI
        yarim = sayi[gun] < EN_AZ_PAY * sayi[gunler[i - 1]]
        if erken or yarim:
            print(
                f"son gün sayılmadı: {gun.date()} ({'seans içi' if erken else 'satır sayısı az'})"
            )
            continue
        return gun
    raise SystemExit("tam işlem günü yok")


# --- Motor ---


def sinyal_kaydi(pkl: Path, ayar: dict, son: pd.Timestamp) -> pd.DataFrame:
    """Motorun her sinyali ve sonu. Para katmanının kullandığı `para._sembol` ana süreçte koşar; motorun
    `_red_nedeni` ve `oyna` çağrıları sarılıp sinyal başına sonuç okunur (motor dosyasına dokunulmaz)."""
    d, c = ayar["desen"], ayar["cikis"]
    (pivot,) = d["pivotlar"]  # dondurulmuş ayarda tek pivot var
    p = {
        "pivot": pivot,
        "tolerans": d["tolerans"],
        "gecerlilik": d["gecerlilik"],
        "stop": d["stop"],
        "rr_min": d["rr_min"],
    }
    kayit, simdiki = {}, [None]
    red, oyna = islem._red_nedeni, islem.oyna

    def red_kaydi(satir, gun_satiri, acik_var, cikis):
        neden = red(satir, gun_satiri, acik_var, cikis)
        kayit[(simdiki[0], satir.name)] = {
            "D": satir["seviye"],
            "stop": satir["stop"],
            "motor_durumu": f"düştü: {neden}" if neden else None,
        }
        return neden

    def oyna_kaydi(g, i, satir, cikis, taban, sayac):
        once = Counter(sayac)
        e, j = oyna(g, i, satir, cikis, taban, sayac)
        if e is not None:
            durum = "doldu"
        else:
            (neden,) = sayac - once  # emir düşünce tek bir sayaç artar
            durum = "bekliyor" if neden == islem.VERI_SONU else f"düştü: {neden}"
        kayit[(simdiki[0], satir.name)]["motor_durumu"] = durum
        return e, j

    islem._red_nedeni, islem.oyna = red_kaydi, oyna_kaydi
    try:
        para._yukle(str(pkl), str(son.date()))
        for sembol in sorted(para._GUNLER):
            simdiki[0] = sembol
            para._sembol((sembol, p, d.get("okuma", "oran"), c, BASLANGIC, son))
    finally:
        islem._red_nedeni, islem.oyna = red, oyna
    satirlar = [{"sembol": s, "sinyal_gunu": t, **v} for (s, t), v in kayit.items()]
    kolon = ["sembol", "sinyal_gunu", "D", "stop", "motor_durumu"]
    return (
        pd.DataFrame(satirlar, columns=kolon)
        .sort_values(["sinyal_gunu", "sembol"], kind="stable")
        .reset_index(drop=True)
    )


ISLEM_KOLONLARI = {
    "sembol": "sembol",
    "sinyal_gunu": "sinyal_tarihi",
    "D": "seviye",
    "stop_sinyal": "stop",
    "son_stop": "son_stop",
    "dolum_gunu": "dolum_tarihi",
    "dolum_fiyati": "dolum_fiyati",
    "kismi_cikis": "kismi",
    "cikis_gunu": "cikis_tarihi",
    "cikis_fiyati": "cikis_fiyati",
    "cikis_nedeni": "cikis_nedeni",
    "R": "R",
    "acik": "acik",
}


def islem_tablosu(
    isl: pd.DataFrame, durum: dict, akis: dict, adet: dict
) -> pd.DataFrame:
    """Motorun dolan her emri: kasa kararı (alındı ya da atlandı), adet ve kâr. Açık pozisyon son kapanışla değerlenir."""
    isl = isl.reindex(columns=list(ISLEM_KOLONLARI.values()))
    t = pd.DataFrame({ad: isl[kolon] for ad, kolon in ISLEM_KOLONLARI.items()})
    t["adet"] = [adet.get(k, 0) for k in isl.index]
    t["kasa_durumu"] = [durum.get(k, "") for k in isl.index]
    t["kar_tl"] = [round(akis[k], 2) if k in adet else np.nan for k in isl.index]
    return t.round(
        {
            "D": 4,
            "stop_sinyal": 4,
            "son_stop": 4,
            "dolum_fiyati": 4,
            "cikis_fiyati": 4,
            "R": 3,
        }
    )


def acik_tablosu(t: pd.DataFrame) -> pd.DataFrame:
    """Son günde açık pozisyonlar; `kar_tl` satış maliyeti ve kayması düşülmüş değerleme kârıdır."""
    a = t[t["acik"].astype(bool) & (t["kasa_durumu"] == "alındı")]
    a = a.assign(piyasa_degeri_tl=(a["adet"] * a["cikis_fiyati"]).round(2))
    a = a.rename(
        columns={"cikis_gunu": "son_fiyat_gunu", "cikis_fiyati": "son_kapanis"}
    )
    return a[
        [
            "sembol",
            "dolum_gunu",
            "dolum_fiyati",
            "adet",
            "son_fiyat_gunu",
            "son_kapanis",
            "son_stop",
            "piyasa_degeri_tl",
            "kar_tl",
        ]
    ]


def yaz(hedef: Path, tablolar: dict[str, pd.DataFrame], ozet: dict) -> None:
    """Geçici klasöre yazar, sonra adlandırır: yarım kayıt klasörü kalmaz, var olan klasörün üstüne yazılmaz."""
    hedef.parent.mkdir(parents=True, exist_ok=True)
    gecici = Path(tempfile.mkdtemp(prefix=".gecici-", dir=hedef.parent))
    try:
        for ad, tablo in tablolar.items():
            tablo.to_csv(
                gecici / ad,
                index=False,
                encoding="utf-8",
                date_format="%Y-%m-%d",
                lineterminator="\n",
            )
        (gecici / "ozet.json").write_text(
            json.dumps(
                ozet,
                ensure_ascii=False,
                indent=1,
                default=lambda o: o.item() if hasattr(o, "item") else str(o),
            )
            + "\n",
            encoding="utf-8",
        )
        os.rename(gecici, hedef)  # hedef varsa hata verir
    except BaseException:
        shutil.rmtree(gecici, ignore_errors=True)
        raise


def calis(kok: Path, kayit_koku: Path, mevcut: bool) -> dict:
    ayar_yolu = dondurulmus_ayar()
    ayar = para.ayar_oku(str(ayar_yolu))
    print(f"tansu: {Path(sys.modules['tansu'].__file__).parent}")
    kok.mkdir(parents=True, exist_ok=True)
    if not mevcut:  # reddedilecek koşu indirme maliyeti taşımasın
        yeni_kayit_yolu(kayit_koku, beklenen_son_gun())
    kimlik = son_kimlik(kok) if mevcut else indir(kok)
    anlik = veri.oku(kimlik, kok)
    son = son_gun(anlik)
    hedef = yeni_kayit_yolu(kayit_koku, son)
    faiz = faiz_al(kok, kimlik, mevcut)
    g = {
        s: t.loc[:son] for s, t in sinama.gunler(anlik).items() if not t.loc[:son].empty
    }  # 2025'te kesik değil
    pkl = kok / f"gunler-{kimlik}.pkl"
    pd.to_pickle((kimlik, g), pkl)
    faiz_yolu = kok / "faiz" / f"{kimlik}.parquet"
    sonuc, gun, isl, durum, akis, adet = para.kos(
        str(pkl),
        str(faiz_yolu),
        ayar,
        sinama.Donem(BASLANGIC, son),
        kok / "onbellek-islem",
    )
    sin = sinyal_kaydi(pkl, ayar, son)
    doldu = set(
        zip(
            sin.loc[sin["motor_durumu"] == "doldu", "sembol"],
            sin.loc[sin["motor_durumu"] == "doldu", "sinyal_gunu"],
            strict=True,
        )
    )
    assert doldu == set(
        zip(isl.get("sembol", []), isl.get("sinyal_tarihi", []), strict=True)
    ), "sinyal kaydı para katmanının işlemleriyle uyuşmuyor"
    kasa = {
        (isl.at[k, "sembol"], isl.at[k, "sinyal_tarihi"]): d for k, d in durum.items()
    }
    sin["kasa_durumu"] = [
        kasa.get((s, t), "")
        for s, t in zip(sin["sembol"], sin["sinyal_gunu"], strict=True)
    ]
    sin = sin.round({"D": 4, "stop": 4})
    tablo = islem_tablosu(isl, durum, akis, adet)
    acik = acik_tablosu(tablo)

    ozkaynak = float(gun["ozkaynak"].iloc[-1])
    pnl = pd.Series(
        {k: akis[k] for k, d in durum.items() if d == "alındı"}, dtype=float
    )
    assert (
        np.isfinite(ozkaynak)
        and abs(ozkaynak - (SERMAYE + sonuc["faiz_geliri_tl"] + sonuc["islem_kari_tl"]))
        <= 2
    ), "özkaynak = sermaye + faiz + işlem kârı tutmuyor"
    xu = para.xu100(g)
    rf = para.gunluk_faiz(faiz, gun.index, xu.index[xu.index < gun.index[0]][-1])
    nakit_son = SERMAYE * float((1 + rf * (1 - ayar["nakit"]["kesinti"])).prod())
    manifest = json.loads(
        (kok / "ag" / kimlik / "manifest.json").read_text(encoding="utf-8")
    )
    atlanan = kok / ATLANAN_DOSYA
    ozet = {
        "son_gun": str(son.date()),
        "baslangic": str(BASLANGIC.date()),
        "sermaye_tl": SERMAYE,
        "ozkaynak_tl": round(ozkaynak),
        "getiri_yuzde": round((ozkaynak / SERMAYE - 1) * 100, 2),
        "faiz_geliri_tl": sonuc["faiz_geliri_tl"],
        "islem_kari_tl": sonuc["islem_kari_tl"],
        "en_iyi_uc_haric_islem_kari_tl": round(
            float(pnl.sum() - pnl.nlargest(3).sum())
        ),
        "yalniz_nakit_ozkaynak_tl": round(nakit_son),
        "en_kotu_dusus_yuzde": sonuc["en_kotu_dusus_yuzde"],
        "sinyal": len(sin),
        "dolan_emir": len(isl),
        "alinan_islem": sonuc["islem"],
        "bekleyen_emir": int((sin["motor_durumu"] == "bekliyor").sum()),
        "acik_pozisyon": len(acik),
        "kasanin_atladigi": sonuc["atlanan"],
        "kiyas": sonuc["kiyas"],
        "faiz_son_degisim": {
            "tarih": str(faiz["tarih"].max().date()),
            "yuzde": float(faiz.loc[faiz["tarih"].idxmax(), "faiz"]),
        },
        "ayar_sha256": AYAR_SHA,
        "para_py_sha256": PARA_SHA,
        "tansu_commit": git("rev-parse", "HEAD"),
        "tansu_ve_para_dosyalari_temiz": git(
            "status", "--porcelain", "--", "tansu", "kanit/gartley-para"
        )
        == "",
        "veri_kimligi": kimlik,
        "veri_fiyat_sha256": manifest["dosyalar"]["fiyat.parquet"],
        "veri_baslangici": str(VERI_BASLANGIC),
        "inmeyen_sembol": len(anlik.inmeyen),
        "bos_sembol": len(anlik.bos),
        "kaynak_gunu_hatasi": [str(t.date()) for t in anlik.kaynak_gunleri],
        "atlanan_kaynak_gunleri": json.loads(atlanan.read_text(encoding="utf-8"))
        if atlanan.exists()
        else {},
    }
    yaz(
        hedef,
        {
            "sinyaller.csv": sin,
            "islemler.csv": tablo,
            "acik.csv": acik,
            "gunluk-kasa.csv": gun.round(2).reset_index(),
        },
        ozet,
    )
    print(json.dumps(ozet, ensure_ascii=False, indent=1))
    print(f"yazıldı: {hedef}")
    return ozet


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "kok",
        nargs="?",
        type=Path,
        default=VARSAYILAN_KOK,
        help="veri klasörü (Git dışı)",
    )
    ap.add_argument(
        "--mevcut", action="store_true", help="indirme yok; son anlık görüntüyü kullan"
    )
    ap.add_argument("--cikti", type=Path, default=KAYIT_KOKU, help="kayıt kökü")
    a = ap.parse_args()
    calis(a.kok, a.cikti, a.mevcut)
