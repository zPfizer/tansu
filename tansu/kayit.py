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

from tansu import aileler, motor, rapor, simulator, veri

KAYIT_DIZINI = Path("kayit")  # testte conftest yönlendirir
PAKET = Path(__file__).parent
# Elle yazılmış, kural kaydına giren dosyalar. K1 kodu gelince eklenir (yeni deneme olur).
KOD_DOSYALARI = ["aileler.py", "cift.py", "evren.py", "gostergeler.py", "motor.py", "simulator.py"]
HASH_DISI = ["__init__.py", "__main__.py", "kaynak.py", "kayit.py", "rapor.py", "sadakat.py", "veri.py"]
# KURALLAR §3 madde 2 (YORUM): eşik, en az gün, giriş penceresi.
IZGARA = {"esik": [0.010, 0.012, 0.015], "min_gun": [2, 3, 5], "pencere": [5, 10, 20]}


class KayitHatasi(Exception):
    pass


def _ozet(metin) -> str:
    return hashlib.sha256(metin if isinstance(metin, bytes) else metin.encode("utf-8")).hexdigest()


def _json(nesne) -> str:
    return json.dumps(nesne, sort_keys=True, ensure_ascii=False)


def _kural(p, atr_n) -> dict:
    kod = _ozet("".join(f"{ad}:{ast.dump(ast.parse((PAKET / ad).read_text(encoding='utf-8')))}\n"
                        for ad in sorted(KOD_DOSYALARI)))
    param = {"aile": asdict(p), "atr_n": atr_n}
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


def deneme_sayisi() -> int:
    """Holm'un m'si: başlamış her `deneme` koşusu; `bitti` satırı aranmaz."""
    return sum(s["olay"] == "basladi" and s["tur"] == "deneme" for s in _oku())


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


def kosu(kimlik, kok, p=aileler.Parametre(), atr_n=motor.ATR_N, tur="deneme", resmi=False, tohum=0,
         tekrar=0, git=_git, bas=simulator.BASLANGIC) -> dict:
    """Kural kaydını denetler, manifesti yeniden hash'ler, `basladi` ve `bitti` satırlarını yazar."""
    kural = _kural(p, atr_n)
    kayitlar = [s for s in _oku() if s["olay"] == "kayit"]
    if not kayitlar:
        raise KayitHatasi("Kural kaydı yok: önce `python -m tansu kayit` çalıştır.")
    if kayitlar[-1]["kural_id"] != kural["kural_id"]:
        raise KayitHatasi("Kural hash'i kayıtla uyuşmuyor: kod ya da parametre değişti; yeni kayıt ve yeni deneme gerekir.")
    anlik = veri.oku(kimlik, kok)  # manifesti yeniden hash'ler; uyuşmazsa VeriHatasi
    manifest = _ozet((Path(kok) / "ag" / kimlik / "manifest.json").read_bytes())
    commit, kirli = git()
    kosu_id = f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}"
    taban = {"tur": tur, "kosu_id": kosu_id, "kural_id": kural["kural_id"]}
    _yaz({**taban, "olay": "basladi", "tarih": _simdi(), "kod_hash": kural["kod_hash"],
          "param_hash": kural["param_hash"], "param": kural["param"], "anlik": kimlik,
          "manifest_sha256": manifest, "git_commit": commit, "tohum": tohum, "tekrar": tekrar,
          "ortam": _ortam(), "resmi": bool(resmi) and not kirli, "kirli": kirli})
    islemler, dusen = motor.sinama(anlik, p, atr_n)
    sim = simulator.calistir(anlik, islemler, dusen, bas)
    html, csv = rapor.yaz(sim, {"kosu_id": kosu_id, "anlik": kimlik, "kod_hash": kural["kod_hash"]})
    ozet = _ozet(islemler.to_csv(index=False) + f"|{dusen}|"
                 + "|".join(s["islemler"].to_csv(index=False) for s in sim["masraf"].values()))
    _yaz({**taban, "olay": "bitti", "tarih": _simdi(), "islem_sayisi": len(islemler), "dusen_sinyal": dusen,
          "ozet": ozet, "veri_sorunlari": sim["bilgi"]["sorunlar"],
          "masraf_sonuc": {str(m): {"son_ozkaynak": float(s["ozkaynak"].iloc[-1]), "son_k2": float(s["k2"].iloc[-1]),
                                    "islem": len(s["islemler"]), "reddedilen": s["reddedilen"]}
                           for m, s in sim["masraf"].items()}})
    return {"kosu_id": kosu_id, "ozet": ozet, "islemler": islemler, "dusen": dusen, "sim": sim, "rapor": html,
            "csv": csv}
