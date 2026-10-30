"""Referans paneli ve düzeltme koşusu: eski deneme betikleriyle; deneme defterine yazmaz, kilit açmaz.

Eski betikler bu dalda yoktur; çalıştırmadan önce `origin/gartley-pdf` (725a86f) dalından `kanit/gartley-yontem/` altına
alınır: `yontem.py` (SHA-256 f9d682a1…), `pdf.py` (3e8f2dc6…), `hisse-gruplari.csv`, `deneme-defteri.tsv`. Veri `kur.py`.

  panel.py <gunler.pkl> <etiket>          -> ayar grubu (371 hisse), 2015-2022; satır panel.tsv'ye
  panel.py sinav <gunler.pkl> <etiket>    -> düzeltme koşusu: eski sınavlar, ayrık grup, aynı adaylar ve geçme şartı
  panel.py kontrol                        -> düzeltmelerin öz denetimi (eski davranış kırmızı, düzeltilmiş yeşil)
Ortam: TANSU_DUZELTME="D1t,T3,E2,S1s,S2s" (`duzeltme.py`), TANSU_TG=1 (Tansu-tam aday, ön kayıttan sonra), TANSU_FAIZ
(faiz dosyası; yoksa `yontem.py`'nin kendi yolu). Çıktı %TEMP%/tansu-denetim-panel/ altında.
"""

import hashlib
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

BURA = Path(__file__).resolve().parent
sys.path[:0] = [
    str(BURA),
    str(BURA.parent / "gartley-yontem"),
]  # işçiler sys.path'i devralır

from tansu import islem  # noqa: E402

# pdf.py b9f6107 motoruna yazıldı; f4ca87d `UYE_DEGIL` adını kaldırdı (üyelik süzgeci çağırana geçti). Yalnız ad; davranış yok.
if not hasattr(islem, "UYE_DEGIL"):
    islem.UYE_DEGIL = "evren dışı"

import pdf  # noqa: E402  (yontem'i kendisi yükler)

yontem = pdf.yontem
import duzeltme  # noqa: E402
import tansu_tam  # noqa: E402

# İşçiler de bu üst düzeyi koşar: düzeltmeler ortam değişkeninden, her süreçte aynı.
DUZELTME = duzeltme.uygula(os.environ.get("TANSU_DUZELTME", ""), yontem, pdf)
P = Path(os.environ["TEMP"]) / "tansu-denetim-panel"
ADAYLAR_Y = ("gartley", "gt-k", "abcd-k")
ADAYLAR_P = ("S2-Z", "S3")


def satir(etiket, ad, s, p):
    u = p["uc_parca"]
    return [
        etiket,
        ad,
        s.get("sinyal", 0),
        s.get("n", 0),
        round(s.get("ort_R", float("nan")), 3),
        round(s.get("ortanca_R", float("nan")), 3),
        round(s.get("p_tek_yonlu", float("nan")), 4),
        round(u["faiz_geliri_tl"]),
        round(u["islem_kari_tl"]),
        round(u["en_iyi_uc_olmadan_islem_kari_tl"]),
        round(u["son_kasa_tl"]),
        round(u["yalniz_nakit_kasasi_tl"]),
        round(u["fark_tl"]),
        p["islem"],
    ]


def _tg_sembol(arg):
    sembol, gun, bas, para_da = arg
    piyasa = yontem.para.Piyasa({sembol: gun}, [sembol], gun.index)
    s = tansu_tam.sinyaller(gun)
    s.loc[(gun.index < bas) | ~gun["uye"].to_numpy(bool), ["giris", "tekrar"]] = [
        False,
        0,
    ]
    cikis, acik_gun = yontem.para._cikis_kur(tansu_tam.CIKIS)
    islem._acik_gun = acik_gun
    aday = SimpleNamespace(desen="gartley")
    return (
        yontem._sinyal_duzeyi(sembol, gun, s, cikis, piyasa, tansu_tam.AD, aday),
        yontem._motor(sembol, gun, s, cikis, tansu_tam.AD) if para_da else [],
    )


def tg(gunler: dict) -> tuple[dict, dict]:
    """Tansu-tam Gartley (ön kayıtlı yeni aday): sinyal düzeyi özet ve para katmanı, eski adaylarla aynı ölçülerle."""
    argl = [(s, gunler[s], yontem.DONEM.bas, True) for s in sorted(gunler)]
    with ProcessPoolExecutor(yontem.ISCI) as havuz:
        parca = list(havuz.map(_tg_sembol, argl, chunksize=4))
    sin = pd.DataFrame([r for p in parca for r in p[0]])
    isl = pd.DataFrame([r for p in parca for r in p[1]])
    if len(isl):
        isl = isl.sort_values(
            ["dolum_tarihi", "sinyal_tarihi", "sembol"], kind="stable"
        ).reset_index(drop=True)
    s = {"aday": tansu_tam.AD, "sembol": len(gunler), **yontem.sinyal_ozeti(sin)}
    p, *_ = yontem.para_katmani(isl, gunler)
    k = yontem.SONUC / f"tg-{len(gunler)}"
    k.mkdir(parents=True, exist_ok=True)
    sin.to_csv(k / "sinyaller.csv", index=False, encoding="utf-8")
    isl.to_csv(k / "islemler.csv", index=False, encoding="utf-8")
    yontem._yaz_json(k / "ozet.json", {**s, "para": p})
    return s, p


def sinav(pkl: Path, etiket: str):
    """Düzeltme koşusu, yeni sınav değil: eski sınavlar aynı dondurulmuş adaylar, aynı ayrık grup ve aynı geçme şartıyla
    (yontem k = 3, pdf k = 5). Seçim yok, kilit ve defter yok."""
    yontem.PKL = pkl
    yontem.PKL_SHA = hashlib.sha256(pkl.read_bytes()).hexdigest()
    yontem.SONUC = pdf.SONUC = P / "sinav" / etiket
    yontem.FAIZ = Path(os.environ.get("TANSU_FAIZ", yontem.FAIZ))
    yontem._SINAV_ACIK = True
    satirlar = []
    for ad in ("gt-k", "abcd-k", "gartley"):
        s = yontem.calistir_sinyal(ad, "ayrik", defter=False)
        p = yontem.calistir_para(ad, "ayrik", defter=False)
        satirlar.append((satir(etiket, ad, s, p), yontem.gecme(s, p)))
    for ad in ADAYLAR_P:
        ((o, _),), _ = pdf.kos_yaz([ad], "ayrik", on="")
        satirlar.append(
            (satir(etiket, ad, o, o["para"]), yontem.gecme(o, o["para"], pdf.K_SINAV))
        )
    tsv = P / "sinav.tsv"
    yeni = not tsv.exists()
    with open(tsv, "a", encoding="utf-8", newline="\n") as f:
        if yeni:
            f.write(
                "etiket\taday\tsinyal\tdolum\tort_R\tortanca_R\tp\tfaiz\tislem_kari\ten_iyi_uc_haric\tson_kasa\tnakit\tfark"
                "\tpara_islem\tk\tsart1\tsart2\tsart3\tEVET\n"
            )
        for r, g in satirlar:
            sart = [
                g[a]
                for a in (
                    "1_ortR_pozitif_ve_p",
                    "2_en_iyi_uc_olmadan_islem_kari_pozitif",
                    "3_son_kasa_nakit_ustu",
                )
            ]
            f.write("\t".join(map(str, [*r, g["k"], *sart, g["EVET"]])) + "\n")
    print(
        json.dumps(
            {"etiket": etiket, "duzeltme": DUZELTME, "satir": [r for r, _ in satirlar]},
            ensure_ascii=False,
        )
    )


def main():
    if sys.argv[1] == "kontrol":
        assert not DUZELTME, "kontrol düzeltmesiz süreçte koşar"
        print(
            json.dumps(
                {**duzeltme.kontrol(yontem, pdf), "tg": tansu_tam.kontrol()},
                ensure_ascii=False,
            )
        )
        return
    if sys.argv[1] == "sinav":
        return sinav(Path(sys.argv[2]).resolve(), sys.argv[3])
    pkl, etiket = Path(sys.argv[1]).resolve(), sys.argv[2]
    yontem.PKL = pkl
    yontem.PKL_SHA = hashlib.sha256(pkl.read_bytes()).hexdigest()
    yontem.SONUC = pdf.SONUC = P / "sonuc" / etiket
    yontem.FAIZ = Path(os.environ.get("TANSU_FAIZ", yontem.FAIZ))
    satirlar = []
    for ad in ADAYLAR_Y:
        s = yontem.calistir_sinyal(ad, "ayar", defter=False)
        p = yontem.calistir_para(ad, "ayar", defter=False)
        satirlar.append(satir(etiket, ad, s, p))
    cikti, _ = pdf.kos_yaz(list(ADAYLAR_P), "ayar", on="", para_da=True)
    for ad, (o, _) in zip(ADAYLAR_P, cikti, strict=True):
        satirlar.append(satir(etiket, ad, o, o["para"]))
    if os.environ.get("TANSU_TG"):  # ön kayıttan sonra
        satirlar.append(satir(etiket, tansu_tam.AD, *tg(yontem.veri_yukle("ayar"))))
    tsv = P / "panel.tsv"
    yeni = not tsv.exists()
    with open(tsv, "a", encoding="utf-8", newline="\n") as f:
        if yeni:
            f.write(
                "etiket\taday\tsinyal\tdolum\tort_R\tortanca_R\tp\tfaiz\tislem_kari\ten_iyi_uc_haric\tson_kasa\tnakit\tfark\tpara_islem\n"
            )
        for r in satirlar:
            f.write("\t".join(map(str, r)) + "\n")
    print(
        json.dumps(
            {
                "etiket": etiket,
                "duzeltme": DUZELTME,
                "pkl_sha256": yontem.PKL_SHA,
                "satir": satirlar,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
