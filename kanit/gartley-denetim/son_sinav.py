"""Son sınav düzeneği: ön kayıtlı altı aday, bir dönem ve bir evrende, eski betikler değişmeden; deftere yazmaz.

Eski betikler `panel.py`'deki gibi `kanit/gartley-yontem/` altına alınır; veri `kur.py` ile kurulur.
python kanit/gartley-denetim/son_sinav.py <gunler.pkl> <faiz.parquet> <bas> <son> <evren: hepsi|ayar> <etiket>
Ortam: TANSU_DUZELTME (ön kayıttaki düzeltmeler). Satırlar %TEMP%/tansu-denetim-panel/son-sinav.tsv dosyasına eklenir.
`ayar` evreni yalnız düzenek doğrulaması içindir: 2015-2022 ayar grubunda panel satırını birebir vermelidir.
"""

import hashlib
import inspect
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import panel  # noqa: E402  (pdf, yontem, düzeltmeler ve TG)

yontem, pdf, para = panel.yontem, panel.pdf, panel.yontem.para
K = 6  # ön kayıt: gt-k, abcd-k, gartley, S2-Z, S3, tg


def donemi_kur(bas: pd.Timestamp, son: pd.Timestamp):
    """Betiklerin 2015-2022 dönemini değiştirir; eski dönemi taşıyan varsayılan değer kalırsa durur."""
    eski, yeni = yontem.DONEM, para.sinama.Donem(bas, son)
    yontem.DONEM = pdf.DONEM = yeni
    yontem.kos.__defaults__ = (True, bas)
    yontem.para_katmani.__defaults__ = (yeni,)
    pdf.kos.__defaults__ = (True, bas)
    for m in (yontem, pdf, para):
        for ad, f in inspect.getmembers(m, inspect.isfunction):
            for v in f.__defaults__ or ():
                if v is eski or (
                    isinstance(v, pd.Timestamp)
                    and v in {eski.bas, eski.son} - {bas, son}
                ):
                    raise SystemExit(f"eski dönem varsayılanı kaldı: {m.__name__}.{ad}")


def main():
    pkl, faiz, bas, son, evren, etiket = sys.argv[1:7]
    bas, son, pkl = pd.Timestamp(bas), pd.Timestamp(son), Path(pkl).resolve()
    yontem.PKL, yontem.PKL_SHA = pkl, hashlib.sha256(pkl.read_bytes()).hexdigest()
    yontem.FAIZ = Path(faiz).resolve()
    yontem.SONUC = pdf.SONUC = panel.P / "son-sinav" / etiket
    _, hepsi = pd.read_pickle(pkl)
    semboller = (
        set(hepsi)
        if evren == "hepsi"
        else set(yontem.gruplar().query("grup == @evren")["sembol"])
    )

    def veri_yukle(grup, son=son):
        return {
            s: t.loc[:son]
            for s, t in hepsi.items()
            if s in semboller and not t.loc[:son].empty
        }

    yontem.veri_yukle = veri_yukle
    donemi_kur(bas, son)
    satirlar = []
    for ad in ("gt-k", "abcd-k", "gartley"):
        s = yontem.calistir_sinyal(ad, evren, defter=False)
        p = yontem.calistir_para(ad, evren, defter=False)
        satirlar.append((panel.satir(etiket, ad, s, p), yontem.gecme(s, p, K)))
    cikti, _ = pdf.kos_yaz(list(panel.ADAYLAR_P), evren, on="", para_da=True)
    for ad, (o, _) in zip(panel.ADAYLAR_P, cikti, strict=True):
        satirlar.append(
            (panel.satir(etiket, ad, o, o["para"]), yontem.gecme(o, o["para"], K))
        )
    s, p = panel.tg(veri_yukle(evren))
    satirlar.append(
        (panel.satir(etiket, panel.tansu_tam.AD, s, p), yontem.gecme(s, p, K))
    )
    tsv = panel.P / "son-sinav.tsv"
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
            {
                "etiket": etiket,
                "duzeltme": panel.DUZELTME,
                "pkl_sha256": yontem.PKL_SHA,
                "faiz_sha256": hashlib.sha256(yontem.FAIZ.read_bytes()).hexdigest(),
                "donem": [str(bas.date()), str(son.date())],
                "sembol": len(semboller),
                "satir": [r for r, _ in satirlar],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
