"""Gartley ve S3 ileri izleme: dondurulmuş kurallar, düzeltilmiş motor, taze BIST verisi (kanit/gartley-takip.md
"İleri izleme").

Kullanım (depo kökünden, ana sanal ortamla):
  izle.py [--mevcut] [--zamanli]

Dondurulmuş kurallar `izleme/dondurma.json`'dadır: dosya özetleri, betik düzeltmeleri, izinli motor ağaçları ve
adayların başlangıç günü. Biri uyuşmazsa betik hiçbir şey indirmeden durur. Her koşu iki adayı başlangıç gününden son
tam işlem gününe kadar baştan hesaplar ve `izleme/<son gün>-<motor ağacı>/` klasörünü yeni yazar; klasör varsa hiçbir
şey yazmadan 0 ile çıkar. Her yeni kayıt `izleme/izleme.tsv`'ye aday başına bir satır ekler.
`--mevcut`: indirme yok, veri klasöründeki son anlık görüntü. `--zamanli`: zamanlanmış görev kipi; çıktı veri
klasöründeki `izleme-log/`a yazılır ve yeni kayıt `gartley-takip` dalına yerel olarak commit edilir (push yok).
`--cikti <klasör>`: kayıt kökü (deneme için; varsayılan `izleme/`).
"""

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import traceback
from pathlib import Path

import pandas as pd

BU = Path(__file__).resolve().parent
REPO = BU.parents[1]
sys.path[:0] = [
    str(REPO),
    str(REPO / "kanit" / "gartley-yontem"),
    str(REPO / "kanit" / "gartley-denetim"),
    str(BU),
]  # işçi süreçler sys.path'i devralır

from tansu import islem, sinama, veri  # noqa: E402

# pdf.py b9f6107 motoruna yazıldı; sonraki motor `UYE_DEGIL` adını kaldırdı. Yalnız ad (kanit/gartley-denetim/panel.py).
if not hasattr(islem, "UYE_DEGIL"):
    islem.UYE_DEGIL = "evren dışı"

import duzeltme  # noqa: E402
import pdf  # noqa: E402  (yontem ve para'yı yükler, kendi dondurulmuş özetlerini denetler)
import takip  # noqa: E402  (veri yardımcıları: indirme, son tam gün, faiz, kayıt yazımı)

yontem = pdf.yontem
para = yontem.para
IZLEME = BU / "izleme"
DONDURMA_YOLU = IZLEME / "dondurma.json"
DONDURMA = json.loads(DONDURMA_YOLU.read_text(encoding="utf-8"))
TSV = IZLEME / "izleme.tsv"
DAL = "gartley-takip"
# İşçi süreçler de bu üst düzeyi koşar: düzeltmeler her süreçte aynı (kanit/gartley-denetim/panel.py).
DUZELTME = duzeltme.uygula(DONDURMA["duzeltme"], yontem, pdf)
TSV_KOLON = [
    "kayit",
    "son_gun",
    "aday",
    "baslangic",
    "ozkaynak_tl",
    "getiri_yuzde",
    "faiz_geliri_tl",
    "islem_kari_tl",
    "en_iyi_uc_haric_islem_kari_tl",
    "yalniz_nakit_tl",
    "xu100_al_tut_tl",
    "sinyal",
    "dolan_emir",
    "alinan_islem",
    "acik_pozisyon",
    "en_kotu_dusus_yuzde",
    "motor_agaci",
    "tansu_commit",
    "veri_kimligi",
    "yazildi",
]


def git(*arg: str) -> str:
    cikti = subprocess.run(
        ["git", "-C", str(REPO), *arg],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return cikti.stdout.strip()


def dondurma_denetimi() -> str:
    """Dondurulmuş dosyalar ve motor ağacı; uyuşmazsa durur. `tansu/` ağacının özetini döndürür."""
    for yol, beklenen in DONDURMA["dosyalar"].items():
        gercek = hashlib.sha256((REPO / yol).read_bytes()).hexdigest()
        if gercek != beklenen:
            raise SystemExit(
                f"dondurulmuş dosya değişmiş: {yol} {gercek} != {beklenen}"
            )
    if git("status", "--porcelain", "--", "tansu"):
        raise SystemExit("tansu/ commit edilmemiş değişiklik taşıyor")
    agac = git("rev-parse", "HEAD:tansu")
    if agac not in DONDURMA["motor_agaclari"]:
        raise SystemExit(f"motor ağacı dondurmada yok: {agac}")
    return agac


def veri_koku() -> Path:
    """Ana deponun `veri/takip-gartley` klasörü (Git dışı); worktree'den de aynı klasör."""
    ortak = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir"))
    return ortak.parent / "veri" / "takip-gartley"


def aday_kos(ad: str, gunler: dict, bas: pd.Timestamp, son: pd.Timestamp) -> tuple:
    """Denetimin düzeltme koşusuyla aynı yol: Gartley `yontem.kos`, PDF adayı `pdf.kos`, para `yontem.para_katmani`."""
    if ad == "gartley":
        sin, isl = yontem.kos(
            gunler, [("gartley", yontem.DONMUS_ORAN)], para_da=True, bas=bas
        )[0]
    else:
        sin, isl = pdf.kos(gunler, [ad], para_da=True, bas=bas)[0]
    o, gun, durum, akis, adet = yontem.para_katmani(isl, gunler, sinama.Donem(bas, son))
    isl = isl.assign(
        kasa_durumu=[durum.get(i, "") for i in isl.index],
        adet=[adet.get(i, 0) for i in isl.index],
        kar_tl=[round(akis[i], 2) if i in adet else None for i in isl.index],
    )
    return sin, isl, gun, o


def kiyas(gunler: dict, faiz: pd.DataFrame, bas: pd.Timestamp, son: pd.Timestamp):
    xu = para.xu100(gunler)
    takvim = xu.index[(xu.index >= bas) & (xu.index <= son)]
    onceki = xu.index[xu.index < takvim[0]][-1]
    return para.kiyaslar(xu, para.gunluk_faiz(faiz, takvim, onceki), takvim)


def calis(mevcut: bool, cikti: Path = IZLEME) -> tuple[Path, str] | None:
    """Yeni kayıt yazılırsa (klasör, veri kimliği); kayıt zaten varsa None. `cikti`: kayıt kökü ve izleme.tsv'nin yeri."""
    agac = dondurma_denetimi()
    kok = veri_koku()
    kok.mkdir(parents=True, exist_ok=True)
    tsv = cikti / TSV.name
    print(f"tansu: {Path(sys.modules['tansu'].__file__).parent}; motor ağacı {agac}")
    if not mevcut:  # var olan kayıt indirme maliyeti taşımasın
        beklenen = cikti / f"{takip.beklenen_son_gun():%Y%m%d}-{agac[:7]}"
        if beklenen.exists():
            print(f"kayıt zaten var: {beklenen.name}; yeni işlem günü yok")
            return None
    kimlik = takip.son_kimlik(kok) if mevcut else takip.indir(kok)
    anlik = veri.oku(kimlik, kok)
    son = takip.son_gun(anlik)
    hedef = cikti / f"{son:%Y%m%d}-{agac[:7]}"
    if hedef.exists():
        print(f"kayıt zaten var: {hedef.name}")
        return None
    yontem.FAIZ = kok / "faiz" / f"{kimlik}.parquet"
    # Reddedilen takip.py koşusu anlık görüntüyü faizsiz bırakabilir; o zaman faiz şimdi alınır.
    faiz = takip.faiz_al(kok, kimlik, mevcut and yontem.FAIZ.exists())
    gunler = {
        s: t.loc[:son] for s, t in sinama.gunler(anlik).items() if not t.loc[:son].empty
    }
    tablolar, adaylar, satirlar = {}, {}, []
    yazildi = dt.datetime.now(veri.ISTANBUL).strftime("%Y-%m-%d %H:%M")
    tansu_commit = git("rev-parse", "HEAD")
    for ad, a in DONDURMA["adaylar"].items():
        bas = pd.Timestamp(a["baslangic"])
        if (
            bas > son
        ):  # başlangıç günü verinin son tam gününden sonra: kasa henüz açılmadı
            adaylar[ad] = {"baslangic": str(bas.date()), "durum": "başlamadı"}
            continue
        sin, isl, gun, o = aday_kos(ad, gunler, bas, son)
        u = o["uc_parca"]
        alinan = isl[isl["kasa_durumu"] == "alındı"] if len(isl) else isl
        ozet = {
            "baslangic": str(bas.date()),
            "ozkaynak_tl": round(u["son_kasa_tl"]),
            "getiri_yuzde": round((u["son_kasa_tl"] / para.SERMAYE - 1) * 100, 2),
            "faiz_geliri_tl": round(u["faiz_geliri_tl"]),
            "islem_kari_tl": round(u["islem_kari_tl"]),
            "en_iyi_uc_haric_islem_kari_tl": round(
                u["en_iyi_uc_olmadan_islem_kari_tl"]
            ),
            "yalniz_nakit_tl": round(u["yalniz_nakit_kasasi_tl"]),
            "xu100_al_tut_tl": kiyas(gunler, faiz, bas, son)["xu100_son"],
            "sinyal": len(sin),
            "dolan_emir": len(isl),
            "alinan_islem": o["islem"],
            "acik_pozisyon": int(alinan["acik"].astype(bool).sum())
            if len(alinan)
            else 0,
            "en_kotu_dusus_yuzde": o["en_kotu_dusus_yuzde"],
            "kasanin_atladigi": o["atlanan"],
            "sinyal_sonuclari": dict(sin["sonuc"].value_counts()) if len(sin) else {},
        }
        adaylar[ad] = ozet
        satirlar.append(
            {
                "kayit": hedef.name,
                "son_gun": str(son.date()),
                "aday": ad,
                **{k: ozet[k] for k in TSV_KOLON if k in ozet},
                "motor_agaci": agac[:7],
                "tansu_commit": tansu_commit[:7],
                "veri_kimligi": kimlik,
                "yazildi": yazildi,
            }
        )
        for t, dosya in ((sin, "sinyaller"), (isl, "islemler")):
            sayi = t.select_dtypes("number").columns
            tablolar[f"{ad}-{dosya}.csv"] = t.round(dict.fromkeys(sayi, 4))
        tablolar[f"{ad}-gunluk-kasa.csv"] = gun.round(2).reset_index()
    manifest = json.loads(
        (kok / "ag" / kimlik / "manifest.json").read_text(encoding="utf-8")
    )
    atlanan = kok / takip.ATLANAN_DOSYA
    takip.yaz(
        hedef,
        tablolar,
        {
            "son_gun": str(son.date()),
            "sermaye_tl": para.SERMAYE,
            "adaylar": adaylar,
            "dondurma_sha256": hashlib.sha256(DONDURMA_YOLU.read_bytes()).hexdigest(),
            "duzeltme": DUZELTME,
            "motor_agaci": agac,
            "tansu_commit": tansu_commit,
            "veri_kimligi": kimlik,
            "veri_fiyat_sha256": manifest["dosyalar"]["fiyat.parquet"],
            "veri_baslangici": str(takip.VERI_BASLANGIC),
            "sembol": len(gunler),
            "inmeyen_sembol": len(anlik.inmeyen),
            "bos_sembol": len(anlik.bos),
            "kaynak_gunu_hatasi": [str(t.date()) for t in anlik.kaynak_gunleri],
            "atlanan_kaynak_gunleri": json.loads(atlanan.read_text(encoding="utf-8"))
            if atlanan.exists()
            else {},
            "faiz_son_degisim": {
                "tarih": str(faiz["tarih"].max().date()),
                "yuzde": float(faiz.loc[faiz["tarih"].idxmax(), "faiz"]),
            },
        },
    )
    yeni = not tsv.exists()
    pd.DataFrame(satirlar, columns=TSV_KOLON).to_csv(
        tsv,
        sep="\t",
        index=False,
        header=yeni,
        mode="a",
        encoding="utf-8",
        lineterminator="\n",
    )
    for s in satirlar:
        print("\t".join(str(s[k]) for k in TSV_KOLON))
    print(f"yazıldı: {hedef}")
    return hedef, kimlik


def commit_et(mesaj: str) -> None:
    """Yalnız kayıt klasörleri ve izleme.tsv; daha önce commit edilmemiş kayıt da girer. Push yok."""
    yollar = [
        str(p.relative_to(REPO))
        for p in [*sorted(IZLEME.glob("2*-*")), TSV]
        if p.exists()
    ]
    if not yollar or not git("status", "--porcelain", "--", *yollar):
        print("commit edilecek kayıt yok")
        return
    git("add", "--", *yollar)
    git("commit", "-m", mesaj, "--", *yollar)
    print(f"commit: {git('rev-parse', '--short', 'HEAD')}")


def zamanli() -> int:
    """Zamanlanmış görev: çıktı veri klasörüne; dal yanlışsa hiçbir şey yapmaz (çıkış 2)."""
    log = veri_koku() / "izleme-log" / f"{dt.datetime.now():%Y%m%d-%H%M}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8", buffering=1) as f:
        sys.stdout = sys.stderr = f
        try:
            dal = git("rev-parse", "--abbrev-ref", "HEAD")
            if dal != DAL:
                print(f"dal {dal}; izleme yalnız {DAL} dalında commit eder")
                return 2
            sonuc = calis(mevcut=False)
            hedef, kimlik = sonuc or (None, None)
            commit_et(
                f"İzleme: {hedef.name} kaydı (veri {kimlik})"
                if hedef
                else "İzleme: önceki koşudan commit edilmemiş kayıt"
            )
            return 0
        except BaseException:  # noqa: BLE001  görevin sonucu log dosyasında kalsın
            traceback.print_exc()
            return 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--mevcut", action="store_true", help="indirme yok; son anlık görüntü"
    )
    ap.add_argument("--zamanli", action="store_true", help="zamanlanmış görev kipi")
    ap.add_argument(
        "--cikti", type=Path, default=IZLEME, help="kayıt kökü (deneme için)"
    )
    a = ap.parse_args()
    if a.zamanli:
        sys.exit(zamanli())
    calis(a.mevcut, a.cikti)
