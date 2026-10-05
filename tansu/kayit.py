"""Kural kaydı ve deneme günlüğü; `kosu()` getiri gösteren tek yoldur (TASARIM 4, 5.8, 5.11)."""

import ast
import datetime as dt
import hashlib
import importlib.metadata as meta
import json
import subprocess
import sys
import uuid
from dataclasses import asdict
from pathlib import Path

import numpy as np

from tansu import aileler, ciftbolme, istatistik, motor, rapor, saglamlik, simulator, veri

KAYIT_DIZINI = Path("kayit")  # testte conftest yönlendirir
PAKET = Path(__file__).parent
# Elle yazılmış, kural kaydına giren dosyalar (K1 kodu `istatistik.py`, sağlamlık ızgarası `saglamlik.py`'dir).
KOD_DOSYALARI = ["aileler.py", "cift.py", "ciftbolme.py", "evren.py", "gostergeler.py", "istatistik.py", "motor.py",
                 "saglamlik.py", "simulator.py"]
GELISTIRME, TAM_TABAN, TAM_CARPAN = 200, 1000, 200  # TASARIM 5.7: B = 200 geliştirmede, tamda max(1.000, 200·m)
AILELER = (simulator.AILE, ciftbolme.AILE)
HASH_DISI = ["__init__.py", "__main__.py", "denetim.py", "gunluk.py", "kaynak.py", "kayit.py", "rapor.py", "sadakat.py",
             "veri.py"]
IZGARA = saglamlik.IZGARA  # KURALLAR §3 (YORUM): her ailenin önceden yazılmış ızgarası


class KayitHatasi(Exception):
    pass


def _ozet(metin) -> str:
    return hashlib.sha256(metin if isinstance(metin, bytes) else metin.encode("utf-8")).hexdigest()


def _json(nesne) -> str:
    return json.dumps(nesne, sort_keys=True, ensure_ascii=False)


def _kural(p, atr_n) -> dict:
    kod = _ozet("".join(f"{ad}:{ast.dump(ast.parse((PAKET / ad).read_text(encoding='utf-8')))}\n"
                        for ad in sorted(KOD_DOSYALARI)))
    param = {"aile": asdict(p), "atr_n": atr_n, "cift": asdict(ciftbolme.Parametre())}
    param_hash, izgara_hash = _ozet(_json(param)), _ozet(_json(IZGARA))
    return {"kural_id": _ozet(kod + param_hash + izgara_hash)[:16], "kod_hash": kod, "param_hash": param_hash,
            "izgara_hash": izgara_hash, "param": param, "izgara": IZGARA}


def _yaz(satir: dict) -> None:
    yol = KAYIT_DIZINI / "deneme.jsonl"
    yol.parent.mkdir(parents=True, exist_ok=True)
    with yol.open("a", encoding="utf-8") as f:  # yalnız ekleme
        f.write(_json(satir) + "\n")


def _oku() -> list:
    yol = KAYIT_DIZINI / "deneme.jsonl"
    if not yol.exists():
        return []
    return [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s]


def _simdi() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def kayitla(p=aileler.Parametre(), atr_n=motor.ATR_N) -> dict:
    """Kural kaydını deneme günlüğüne yazar (`tur=kayit`)."""
    kural = _kural(p, atr_n)
    _yaz({"tur": "kayit", "olay": "kayit", "tarih": _simdi(), **kural})
    return kural


def denetim_yaz(sonuc, p=aileler.Parametre(), atr_n=motor.ATR_N) -> None:
    """Boru hattı denetimi sonucunu (`gecti` bayrağı ve oranlar) bu kodun hash'iyle günlüğe yazar (`tur=destek`, Holm m'ye girmez)."""
    kural = _kural(p, atr_n)
    _yaz({"tur": "destek", "olay": "denetim", "tarih": _simdi(), "kod_hash": kural["kod_hash"],
          "kural_id": kural["kural_id"], **_temiz(sonuc)})


def deneme_sayisi() -> int:
    """Holm'un m'si: başlamış her `deneme` koşusu; `bitti` satırı aranmaz."""
    return sum(s["olay"] == "basladi" and s["tur"] == "deneme" for s in _oku())


def _ilk_p() -> dict:
    """(kural_id, aile) → ilk resmi p: günlükteki `deneme` koşularından, ilk görülen (TASARIM 5.11)."""
    resmi, p = {}, {}
    for s in _oku():
        if s["olay"] == "basladi" and s["tur"] == "deneme":
            resmi[s["kosu_id"]] = bool(s.get("resmi"))
        elif s["olay"] == "bitti" and s["tur"] == "deneme" and resmi.get(s["kosu_id"]) and s.get("k1"):
            for aile, k in s["k1"].items():
                p.setdefault((s["kural_id"], aile), k["p"])
    return p


def holm_hesapla(kural_id, ps, resmi) -> dict:
    """Aile → {holm_p, holm_m, varsayimsal, donmus}. `ps`: bu koşunun K1 p'leri (aile → p).

    Holm'a her (kural, aile) çiftinin ilk resmi p'si girer; bu koşunun yeni çiftleri de eklenir (geliştirmede
    `varsayimsal`). Kâğıt'a geçmiş çiftin Holm p'si ve m'si donar (TASARIM 5.11)."""
    mevcut = _ilk_p()
    donmus = {(s["kural_id"], s["aile"]): s for s in _oku()
              if s["olay"] == "durum" and s["resmi"] and s["durum"] == "Kâğıt"}
    tum = dict(mevcut)
    for aile, p in ps.items():
        tum.setdefault((kural_id, aile), p)
    duzeltilmis = dict(zip(tum, istatistik.holm(list(tum.values()))))
    sonuc = {}
    for aile in ps:
        a = (kural_id, aile)
        if a in donmus:
            sonuc[aile] = {"holm_p": donmus[a]["holm_p"], "holm_m": donmus[a]["holm_m"], "varsayimsal": False,
                           "donmus": True}
        else:
            sonuc[aile] = {"holm_p": duzeltilmis[a], "holm_m": len(tum), "varsayimsal": a not in mevcut and not resmi,
                           "donmus": False}
    return sonuc


def denetim_gecti(kod_hash) -> bool:
    """Bu kod hash'iyle yapılmış son boru hattı denetimi geçti mi (`tur=destek`, `olay=denetim`)? Yoksa yanlış (TASARIM 5.12)."""
    satirlar = [s["gecti"] for s in _oku() if s["olay"] == "denetim" and s["kod_hash"] == kod_hash]
    return bool(satirlar) and satirlar[-1]


def tekrar_sayisi(son, p=aileler.Parametre(), atr_n=motor.ATR_N) -> int:
    """K1 tekrar sayısı B: geliştirmede 200; `--son`da max(1.000, 200·m), m = günlükteki ilk resmi p'ler + bu kuralın yeni p'leri."""
    if not son:
        return GELISTIRME
    mevcut = _ilk_p()
    kural_id = _kural(p, atr_n)["kural_id"]
    m = len(mevcut) + sum((kural_id, a) not in mevcut for a in AILELER)
    return max(TAM_TABAN, TAM_CARPAN * m)


def durum_oku(aile) -> str:
    """Ailenin durumu: en son resmi `durum` satırı; yoksa Deneme (TASARIM 5.12)."""
    resmi = [s["durum"] for s in _oku() if s["olay"] == "durum" and s["aile"] == aile and s["resmi"]]
    return resmi[-1] if resmi else "Deneme"


def _temiz(x):
    """JSON için: NaN → None, numpy → Python."""
    if isinstance(x, dict):
        return {str(k): _temiz(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_temiz(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if np.isnan(x) else float(x)
    return int(x) if isinstance(x, np.integer) else x


def _fazla(b, t):
    """İşlem başına sepete göre fazla getiri (TASARIM 5.7)."""
    return t["getiri"].to_numpy() - simulator.sepet_getirisi(b, t["giris_tarih"], t["cikis_tarih"])


def _kabul(b, sonuclar, bilgi, holm, k1, islem_yok, gun_sutun, tohum, sag) -> dict:
    """Bir ailenin kabul tablosu ve güven aralığı; `sonuclar`: masraf → {islemler, ozkaynak, k2, yillik}; `sag`: ızgara hücreleri."""
    t = sonuclar[0.003]["islemler"]
    gunluk = {m: s["ozkaynak"].pct_change().iloc[1:] - s["k2"].pct_change().iloc[1:] for m, s in sonuclar.items()}
    g = gunluk[0.003].to_numpy()
    yil = max((bilgi["bitis"] - bilgi["basla"]).days / 365.25, 1e-9)
    tutma = float(np.mean(b["gunler"].get_indexer(t["cikis_tarih"]) - b["gunler"].get_indexer(t["giris_tarih"]))) if len(t) else 20.0
    mde = istatistik.saptanabilir_etki(g) if len(g) > 1 else float("nan")
    girdi = {"fazla": {m: float(np.nanmean(_fazla(b, s["islemler"]))) if len(s["islemler"]) else float("nan")
                       for m, s in sonuclar.items()},
             "p": holm["holm_p"], "portfoy": {m: float(x.mean()) for m, x in gunluk.items()},
             "yillik": sonuclar[0.003]["yillik"]["fazla"], "bas": bilgi["basla"], "bitis": bilgi["bitis"],
             "islem_yok": islem_yok, "islem_fazla": _fazla(b, t), "islem": len(t), "gun": int(t[gun_sutun].nunique()),
             "mde": mde, "islem_yil": len(t) / yil, "ozkaynak": sonuclar[0.005]["ozkaynak"], "saglamlik": saglamlik.oran(sag)}
    sonuc = istatistik.kabul(girdi)
    sonuc.update(ci=istatistik.blok_aralik(g, istatistik.blok_uzunlugu(tutma), tohum=tohum) if len(g) else (float("nan"),) * 2,
                 mde=mde, gercek=girdi["fazla"], holm=holm, k1=k1, izgara=sag)
    return sonuc


def _git() -> tuple:
    """(commit, kirli). `kayit/` hariç: koşunun kendi yazdığı günlük ağacı kirletmez."""
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    durum = subprocess.run(["git", "status", "--porcelain", "--", ".", ":!kayit"],
                           capture_output=True, text=True).stdout.strip()
    return commit, bool(durum)


def _ortam() -> dict:
    kok = PAKET.parent
    lock = kok / "requirements.lock.txt"
    return {"python": sys.version.split()[0], "pandas": meta.version("pandas"), "numpy": meta.version("numpy"),
            "lock_sha256": _ozet(lock.read_bytes()) if lock.exists() else None}


def hesapla(anlik, p, atr_n, bas, tekrar, tohum, holm_fn) -> dict:
    """Günlüksüz çekirdek: motor, simülatör, çift bölmesi, K1, sağlamlık ızgarası ve kabul tablosu (`kosu` ve boru hattı denetimi).

    `holm_fn`: {aile: p} → {aile: holm_hesapla çıktısı}. `tekrar` 0 ise K1, ızgara ve kabul yoktur (None)."""
    ilk = simulator.ilk_gun(anlik, bas)
    evr = simulator.evrenler(anlik, ilk, anlik.gunler[-1])
    uye = simulator.uyeler(anlik, evr, ilk)
    islemler, dusen = motor.sinama(anlik, p, atr_n, uye)
    sim = simulator.calistir(anlik, islemler, dusen, bas, evr=evr)
    h = ciftbolme.hazirla(anlik, evr, bas, aday_esik=max(IZGARA[ciftbolme.AILE]["p_esik"]))
    cift = ciftbolme.calistir(anlik, evr, bas, h=h)
    k1 = kabul = None
    if tekrar:  # K1 p'si, sağlamlık, Holm ve kabul tablosu (TASARIM 5.7, 5.10, 5.11, 5.12)
        b = simulator.k1_baglam(anlik, evr, bas)
        k1 = {simulator.AILE: istatistik.ema_k1(anlik, b, p, atr_n, uye, tekrar, tohum),
              ciftbolme.AILE: istatistik.cift_k1(h, b, tekrar, tohum)}
        sag = {simulator.AILE: saglamlik.ema(anlik, b, p, atr_n, uye),
               ciftbolme.AILE: saglamlik.cift(anlik, evr, b, bas, h["p"], h=h)}
        holm = holm_fn({a: k["p"] for a, k in k1.items()})
        kabul = {simulator.AILE: _kabul(b, sim["masraf"], sim["bilgi"], holm[simulator.AILE], k1[simulator.AILE], [],
                                        "sinyal_tarih", tohum, sag[simulator.AILE]),
                 ciftbolme.AILE: _kabul(b, cift["masraf"], sim["bilgi"], holm[ciftbolme.AILE], k1[ciftbolme.AILE],
                                        cift["islem_yok"], "giris_tarih", tohum, sag[ciftbolme.AILE])}
    return {"islemler": islemler, "dusen": dusen, "sim": sim, "cift": cift, "k1": k1, "kabul": kabul}


def kosu(kimlik, kok, p=aileler.Parametre(), atr_n=motor.ATR_N, tur="deneme", resmi=False, tohum=0,
         tekrar=0, git=_git, bas=simulator.BASLANGIC, son=False) -> dict:
    """Kural kaydını denetler, manifesti yeniden hash'ler, `basladi` ve `bitti` satırlarını yazar.

    `tekrar`: K1 tekrar sayısı B (0: K1 yok). `son`: tam tekrarlı koşu (`sinama --son`), yalnız günlüğe yazılır."""
    kural = _kural(p, atr_n)
    kayitlar = [s for s in _oku() if s["olay"] == "kayit"]
    if not kayitlar:
        raise KayitHatasi("Kural kaydı yok: önce `python -m tansu kayit` çalıştır.")
    if kayitlar[-1]["kural_id"] != kural["kural_id"]:
        raise KayitHatasi("Kural hash'i kayıtla uyuşmuyor: kod ya da parametre değişti; yeni kayıt ve yeni deneme gerekir.")
    if resmi and 0 < tekrar < tekrar_sayisi(True, p, atr_n):
        raise KayitHatasi(f"Resmi koşu tam tekrar ister: tekrar {tekrar} < {tekrar_sayisi(True, p, atr_n)}; "
                          "`sinama --son --resmi` kullan.")
    if resmi and not denetim_gecti(kural["kod_hash"]) and not any(
            s["olay"] == "basladi" and s["tur"] == "deneme" and s.get("resmi") for s in _oku()):
        raise KayitHatasi("İlk resmi koşu yapılmaz: bu kodla geçen boru hattı denetimi yok (yanlış kabul ≤ %5 şartı); "
                          "`python -m tansu denetim` çalıştır (TASARIM 5.12).")
    anlik = veri.oku(kimlik, kok)  # manifesti yeniden hash'ler; uyuşmazsa VeriHatasi
    manifest = _ozet((Path(kok) / "ag" / kimlik / "manifest.json").read_bytes())
    commit, kirli = git()
    kosu_id = f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}"
    taban = {"tur": tur, "kosu_id": kosu_id, "kural_id": kural["kural_id"]}
    _yaz({**taban, "olay": "basladi", "tarih": _simdi(), "kod_hash": kural["kod_hash"],
          "param_hash": kural["param_hash"], "param": kural["param"], "anlik": kimlik,
          "manifest_sha256": manifest, "git_commit": commit, "tohum": tohum, "tekrar": tekrar, "son": bool(son),
          "ortam": _ortam(), "resmi": bool(resmi) and not kirli, "kirli": kirli})
    h = hesapla(anlik, p, atr_n, bas, tekrar, tohum,
                lambda ps: holm_hesapla(kural["kural_id"], ps, bool(resmi) and not kirli))
    islemler, dusen, sim, cift, k1, kabul = (h[k] for k in ("islemler", "dusen", "sim", "cift", "k1", "kabul"))
    html, csv = rapor.yaz(sim, {"kosu_id": kosu_id, "anlik": kimlik, "kod_hash": kural["kod_hash"],
                                "holm_tarih": _simdi()[:10]}, cift, kabul=kabul)
    ozet = _ozet(islemler.to_csv(index=False) + f"|{dusen}|"
                 + "|".join(s["islemler"].to_csv(index=False) for s in sim["masraf"].values())
                 + "|" + "|".join(s["islemler"].to_csv(index=False) for k in ("masraf", "sabit")
                                  for s in cift[k].values()) + (f"|{_json(_temiz(k1))}" if k1 else ""))
    _yaz({**taban, "olay": "bitti", "tarih": _simdi(), "islem_sayisi": len(islemler), "dusen_sinyal": dusen,
          "tekrar": tekrar, "son": bool(son), "tohum": tohum, "k1": _temiz({a: {**k1[a], "gercek_masraf": kabul[a]["gercek"]} for a in k1}) if k1 else None,
          "ozet": ozet, "veri_sorunlari": sim["bilgi"]["sorunlar"],
          "masraf_sonuc": {str(m): {"son_ozkaynak": float(s["ozkaynak"].iloc[-1]), "son_k2": float(s["k2"].iloc[-1]),
                                    "islem": len(s["islemler"]), "reddedilen": s["reddedilen"]}
                           for m, s in sim["masraf"].items()},
          "cift_islem_yok": cift["islem_yok"],
          "cift_sonuc": {k: {str(m): {"son_ozkaynak": float(s["ozkaynak"].iloc[-1]), "son_k2": float(s["k2"].iloc[-1]),
                                      "son_elli_elli": float(s["elli_elli"].iloc[-1]), "islem": len(s["islemler"])}
                             for m, s in cift[k].items()} for k in ("masraf", "sabit")}})
    if kabul and tur == "deneme":  # aile durumu: yalnız ekleme satırı (TASARIM 5.11)
        for aile, k in kabul.items():
            _yaz({"tur": "durum", "olay": "durum", "tarih": _simdi(), "kosu_id": kosu_id, "kural_id": kural["kural_id"],
                  "aile": aile, "durum": k["durum"], "genel": k["genel"], "holm_p": k["holm"]["holm_p"],
                  "holm_m": k["holm"]["holm_m"], "varsayimsal": k["holm"]["varsayimsal"],
                  "resmi": bool(resmi) and not kirli, "olcutler": [[r["no"], r["durum"]] for r in k["satirlar"]],
                  "kanit": _temiz({"islem": len((sim if aile == simulator.AILE else cift)["masraf"][0.003]["islemler"]),
                                   "fazla": k["gercek"][0.003], "ci": k["ci"]})})  # kart kanıt satırı (TASARIM 6.5)
    for aile, k in (kabul or {}).items():  # sağlamlık ızgarası hücreleri: destek, Holm m'ye girmez (TASARIM 5.10, 5.11)
        for c in k["izgara"]:
            _yaz({"tur": "destek", "olay": "hucre", "tarih": _simdi(), "kosu_id": kosu_id, "kural_id": kural["kural_id"],
                  "aile": aile, **_temiz(c)})
    return {"kosu_id": kosu_id, "ozet": ozet, "islemler": islemler, "dusen": dusen, "sim": sim, "cift": cift,
            "rapor": html, "csv": csv, "k1": k1, "kabul": kabul}
