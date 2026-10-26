# Faz 1: göç, yeni CI, belgeler, komut iskeleti

Tarih: 26.10.2026. Dal: `yeniden-kurulus` (kaynak `v0.1-arsiv`).

## Yapılanlar

- Koruma listesi dışındaki 102 izlenen dosya dalda silindi (SPEC 8.2, 8.5). Eski kod, belgeler ve kayıtlar `v0.1-arsiv` etiketinde duruyor.
- Kalan dosyalar: `tansu/{__init__,__main__,veri,kaynak,gostergeler,cift}.py`, `tansu/referans/`, `tests/{conftest,test_veri,test_kaynak,test_gostergeler,test_cift,test_komut}.py`, `pyproject.toml`, `requirements.lock.txt`, `.gitignore`, `.gitattributes`, `.claude/settings.json`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `.github/workflows/ci.yml`.
- `kayit/deneme.jsonl` ve `kayit/kartlar.jsonl` silindi: korunan modüller `kayit/` okumuyor.
- `tests/conftest.py` yalnız ağ engelini tutuyor. `ci.yml` yeniden yazıldı (Windows: ruff check, ruff format --check, pytest); `dod.yml` aynı PR'da silindi.
- `AGENTS.md` tek sayfa, `CLAUDE.md` yalnız `@AGENTS.md`, `README.md` Türkçe.
- Komut iskeleti: `tansu/__main__.py` altı alt komut; `[project.scripts] tansu`. Yapılmamış komutlar çıkış kodu 2 ile "henüz yapılmadı" yazar.
- `.gitignore`: SPEC bölüm 4 rapor satırları, `kayit/sinyaller.csv`, `kayit/tara.log`; Ek B #12 açık olduğu için `docs/SPEC.md`, `docs/PLAN.md`, `docs/eksik-denetim.md`, `stratejiler/*.md` (`sahip-kararlari.md` hariç) ve `tests/altin/` yerelde.
- `docs/SPEC.md`, `docs/PLAN.md`, `docs/eksik-denetim.md` yerel kopya olarak yazıldı (Git dışı).
- `stratejiler/sahip-kararlari.md` Ek B varsayılanlarıyla; `stratejiler/durum.csv` başlıkla.
- `psutil` doğrudan bağımlılıklardan çıktı. Kilit dosyası `pyproject` kapanışından yeniden üretildi; `psutil` dolaylı olarak kalıyor (`borsapy` → `pymupdf4llm` → `psutil`), paket kümesi aynı (65).

## Spec'ten sapmalar (gerekçeli)

- `.gitattributes` korundu, iki satıra indi (`* text=auto eol=lf`, `*.parquet binary`): satır sonu kuralı olmadan Windows'ta biçim farkı çıkar.
- `.claude/settings.json` korundu: Levent'in beyin kancaları ve yasak git komutları (ör. `git add -A`) burada. Yalnız silinen `kurulum/kanca.py` kancası çıkarıldı.
- SPEC 8.3 (`aileler.py`, `ciftbolme.py`, `motor.py` okuması): kod `v0.1-arsiv` etiketinde okunabilir; port, yapı kuralına göre ilk kullanan fazda yapılır (pivotlar faz 3, çift kodu faz 8).

## Silinen korunan testler (yalnız silinen davranışı sınayanlar)

- `tests/test_cift.py`: `ciftbolme` kullanan 5 test (6 düğüm): `test_cift_ortak_kurulum_hedef_bacak_ve_gerekceli_bos_alanlar`, `test_cift_ortak_kurulum_isinma_ve_eksik_veri` (2), `test_cift_ortak_deger_tarih_eski_uyarlayiciyla_ayni`, `test_cift_strateji_uyusmazligi_ve_donem_disi_hata`, `test_cift_cozulmus_ayarlar_birim_ve_kaynak_tasir`.
- `tests/test_kaynak.py`: eski `evren-indir` komutunu sınayan 2 test (4 düğüm): `test_evren_indir_ag_icin_yalniz_kaynagi_kullanir_borsapyye_dogrudan_cikmaz`, `test_evren_indir_kaniti_yayin_oncesi_manifestle_tamamlar` (3).

## Komutlar ve çıktı

```
$ .venv\Scripts\python.exe -m ruff check tansu tests
All checks passed!
$ .venv\Scripts\python.exe -m ruff format --check tansu tests
15 files already formatted
$ .venv\Scripts\python.exe -X utf8 -m pytest -q
119 passed in 3.73s
$ .venv\Scripts\python.exe -X utf8 -m tansu --help
usage: tansu [-h] komut ...
positional arguments:
  komut
    veri      veriyi indir veya güncelle
    sina      stratejiyi geçmiş veride sına, rapor yaz
    ayarla    2021-2025 üzerinde parametre ayarla
    onayla    stratejiyi akşam sinyaline al (yalnız Levent)
    tara      akşam taraması ve seviye listesi
    durum     stratejilerin sınıfı ve durumu

$ git check-ignore -v --no-index rapor/gartley/sinama.html rapor/gartley/ozet.md rapor/sinyal/2026-10-26.md kayit/sinyaller.csv docs/SPEC.md stratejiler/gartley.md stratejiler/sahip-kararlari.md tests/altin/gartley.csv
.gitignore:16:/rapor/*/*	rapor/gartley/sinama.html
.gitignore:17:!/rapor/*/ozet.md	rapor/gartley/ozet.md
.gitignore:18:/rapor/sinyal/	rapor/sinyal/2026-10-26.md
.gitignore:19:/kayit/sinyaller.csv	kayit/sinyaller.csv
.gitignore:23:/docs/SPEC.md	docs/SPEC.md
.gitignore:26:/stratejiler/*.md	stratejiler/gartley.md
.gitignore:27:!/stratejiler/sahip-kararlari.md	stratejiler/sahip-kararlari.md
.gitignore:28:/tests/altin/	tests/altin/gartley.csv
```

CI sonucu: PR'da (aşağıya eklenir).
