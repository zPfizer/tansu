# İzleme 20: Sürüm, belge, bakım (cevaplar-20-bakim.md)

Karşılaştırılan: TASARIM.md (taslak 6), KURALLAR.md, GLOSSARY.md, sonuc-3-4.md (B-1..B-20, C-1..C-11), AGENTS.md, pyproject.toml, .gitignore, .gitattributes, requirements.lock.txt.
Atlanan hükümler: OLGU, CEVAPLI, ZAYIF SORU. Dosyada EKSİK hükmü yok.

20-001 — KARAR — RED — yedek yok kararı
20-002 — KARAR — RED — yedek yok kararı
20-003 — YANLIŞ — YENİ — TASARIM §5.11: deneme günlüğü satırı anlık görüntü `manifest.json` sha256'sını da yazar; koşu başında manifest yeniden hash'lenir, uyuşmazsa koşu durur. Ayrı `kayit/anlik.csv` açılmaz (C-4 manifest zaten var); "ham dosyalar yedekle korunur" kısmı RED (yedek yok kararı)
20-004 — KARAR — TEKRAR — 20-003 (salt-okunur bayrağı ayrıca RED: aşırı kurulum)
20-005 — YANLIŞ — VAR — `.gitignore` (`*.parquet`, `rapor/`), sonuc-3-4 C-10. "rapor/*.md git'e girer" kısmı uygulanmaz: C-10 `rapor/` tümünü git dışı bıraktı
20-006 — KARAR — YENİ — TASARIM §5.8: kural kaydı parmak izi = `git rev-parse HEAD`; resmi koşu kirli çalışma ağacında (`git status --porcelain` boş değil) reddedilir; deneme koşusu günlüğe "kirli" yazar. C-6'daki `ast.dump` karması gerekmez (temiz ağaç + commit yeter)
20-007 — KARAR — VAR — AGENTS.md satır 26 (`rebase`, `--amend`, `--force` yok)
20-008 — KARAR — VAR — AGENTS.md satır 15 (ana dal `master`; uzak depo yok)
20-010 — KARAR — TEKRAR — 20-033
20-011 — KARAR — RED — aşırı kurulum (commit öneki; deneme günlüğü commit hash'i zaten taşır, §5.11)
20-012 — KARAR — RED — aşırı kurulum (çıktı-hash ölçütü); "yeni deneme" tanımı §5.8 ve §5.11'de var
20-013 — KARAR — RED — aşırı kurulum; commit hash'i yeter (§5.8 üstteki 20-006, §5.11)
20-014 — YANLIŞ — VAR — `.gitattributes` (`* text=auto eol=lf`), C-10
20-015 — YANLIŞ — VAR — `.gitignore` (`*.parquet`), AGENTS.md satır 26 (`git add .` yok)
20-016 — KARAR — TEKRAR — 20-007 (geçmiş yeniden yazma yasağı)
20-017 — KARAR — VAR — TASARIM satır 20-21 (ön deneme "kanıt değildir"); `rapor/` git dışı (`.gitignore`)
20-019 — KARAR — YENİ — AGENTS.md "Domain docs" (satır 43): "kararlar `docs/adr/`" yerine "ADR yok; karar `docs/TASARIM.md`, gerekçe `docs/sorgu/`"
20-021 — KARAR — RED — kapsam dışı (arşiv dosyası; kural eklemek gereksiz)
20-022 — KARAR — RED — gereksiz; Levent'in okuduğu yer `durum.txt` (§6.7), TASARIM onun belgesi değil
20-023 — YANLIŞ — VAR — AGENTS.md satır 17 ve 22 (testler yalnız TASARIM yüzlerinden; testte sabitler literal) ve §4 ("maliyet tek sabit")
20-024 — KARAR — VAR — AGENTS.md satır 3-4 ve 12 (belge tek kaynak, kod belgeye uyar); regex testi "şimdi değil" diye ertelenmiş
20-025 — KARAR — RED — C-6 kural kaydı donmuş dataclass; ek `.toml` aşırı kurulum
20-028 — KARAR — VAR — TASARIM §4 (Türkçe modül adları), GLOSSARY.md
20-029 — KARAR — RED — 20-031 ile `.scratch/` bırakılır
20-030 — KARAR — RED — kapsam dışı (commit sıklığı kuralı gereksiz)
20-031 — YANLIŞ — YENİ — AGENTS.md "Issue tracker" (satır 35) ve "Triage labels" (satır 39): `.scratch/` + beş etiket yerine tek `TODO.md` (kökte, ≤20 satır, iki başlık: "Şimdi" ve "Bekleyen")
20-033 — KARAR — YENİ — AGENTS.md "Çalışma kuralları": ekle "`git push`, `reset --hard`, `veri/` silme, kural parametresi değiştirme yok"; satır 28'i "yeni paket yalnız Levent onayıyla" yap
20-035 — KARAR — TEKRAR — 20-031 ("Şimdi" başlığı)
20-037 — YANLIŞ — TEKRAR — 20-033 ("Yapma" listesi)
20-038 — YANLIŞ — YENİ — AGENTS.md satır 12: "belgeyi önce düzelt" yerine "dur, Levent'e sor; TASARIM/KURALLAR/AGENTS onaysız değiştirilmez". Şu an satır 12 ajana belgeyi düzeltme izni veriyor
20-039 — YANLIŞ — VAR — AGENTS.md satır 16 (`.venv\Scripts\python.exe -m pytest -q`)
20-040 — KARAR — VAR — AGENTS.md satır 15 (Windows, PowerShell, `.venv\Scripts\python.exe`)
20-041 — KARAR — RED — aşırı kurulum (dosya sayısı sınırı)
20-042 — KARAR — VAR — AGENTS.md satır 16 (pytest yeşil olmadan commit yok)
20-043 — YANLIŞ — VAR — AGENTS.md satır 17-22 (test TASARIM yüzlerinden, elle hesaplı beklenen değer) ve C-9 (beklenen değerler ayrı ajanın elle hesabı). Docstring §numarası ve denetim ritüeli RED (20-079)
20-044 — KARAR — VAR — AGENTS.md satır 17 ("önce kırmızı test")
20-046 — KARAR — VAR — `requirements.lock.txt`, C-2
20-047 — KARAR — VAR — C-2 ("uv yok", pip + lock)
20-048 — KARAR — VAR — C-2 (bağımlılık listesi; quantstats, duckdb vb. çıktı), `pyproject.toml`
20-049 — KARAR — RED — aşırı kurulum (ölçüt); paket onayı 20-033'te
20-050 — KARAR — RED — aşırı kurulum; sürümler `==` sabit (`pyproject.toml`), yükseltme yok
20-051 — KARAR — VAR — C-2 (dev yalnız pytest), `pyproject.toml`
20-052 — KARAR — TEKRAR — 20-051
20-053 — KARAR — VAR — AGENTS.md satır 16 (hook yok, pytest kapısı)
20-054 — YANLIŞ — VAR — C-2 ve `pyproject.toml` (`dev = ["pytest==9.1.1"]`; mypy/pyright yok)
20-056 — KARAR — VAR — `pyproject.toml` dev bağımlılığı yalnız pytest
20-057 — KARAR — VAR — TASARIM §5.3 (motor sınamaları listesi), C-9 (coverage yok)
20-058 — KARAR — VAR — AGENTS.md satır 16
20-059 — KARAR — VAR — C-9 (CI yok), AGENTS.md satır 16
20-060 — KARAR — VAR — AGENTS.md satır 15 ("uzak depo ve yedek yok")
20-061 — KARAR — VAR — TASARIM §4 (fiyat kaynağı anahtarsız); `.env` kuralı YAGNI
20-062 — KARAR — TEKRAR — 20-033 (paket yalnız onayla)
20-064 — KARAR — TEKRAR — 20-038 (belge ve AGENTS.md onaysız değişmez)
20-065 — KARAR — RED — kapsam dışı (müdahale gerekmiyor)
20-067 — KARAR — TEKRAR — 20-019
20-068 — KARAR — VAR — sonuc-3-4.md (birleştirme belgesi), TASARIM satır 8
20-069 — KARAR — VAR — sonuc-3-4.md başlığı ("Soru ve cevaplar: sorgu-3/, sorgu-4/"), TASARIM satır 3-8
20-070 — YANLIŞ — VAR — AGENTS.md "Okuma sırası" (satır 6-10)
20-071 — KARAR — RED — kapsam dışı (havuz beyin tarafında)
20-072 — KARAR — RED — gereksiz; TASARIM başlığı tarih taşıyor
20-074 — KARAR — VAR — TASARIM §6.1 (19:30) ve §6.7 (`rapor/durum.txt`: TAMAM/SORUNLU/VERİ YOK + son başarılı koşu saati)
20-075 — KARAR — VAR — TASARIM §6.1, C-7 (`kurulum/`)
20-076 — KARAR — VAR — TASARIM §6.2 ve C-4 (her akşam tam indirme)
20-077 — KARAR — RED — aşırı kurulum; AGENTS.md ve `durum.txt` (§6.7) yeter
20-078 — KARAR — TEKRAR — 20-070
20-079 — KARAR — RED — aşırı kurulum (denetim ritüeli); §5.12 boru hattı denetimi ve C-9 testleri var
20-080 — KARAR — TEKRAR — 20-079
20-081 — KARAR — VAR — TASARIM §7 adım 1 (temizlik)
20-082 — KARAR — VAR — `pyproject.toml` (`pythonpath = ["."]`)
20-083 — KARAR — VAR — TASARIM §4 ("Paket düzdür"), C-3
20-084 — KARAR — RED — aşırı kurulum
20-085 — KARAR — RED — sürüm/etiket gereksiz (20-013)
20-086 — KARAR — RED — `git log` yeter; ayrı "Yapıldı" bölümü gereksiz
20-087 — KARAR — RED — gün başına dosya aşırı; geçmişi `kayit/kartlar.jsonl` (§6.6) ve `kayit/deneme.jsonl` (§5.11) tutar
20-088 — KARAR — VAR — TASARIM §5.11 (`kayit/deneme.jsonl`), C-6 (yalnız ekleme, git'te), AGENTS.md satır 24-25; haftalık yedek kısmı RED (yedek yok kararı)
20-090 — KARAR — RED — aşırı kurulum (`attrib +R`, etiket); kural kaydı §5.8
20-091 — KARAR — VAR — AGENTS.md satır 18-21 (testi gevşetme yasak, gerekçe önce belgeye)
20-092 — KARAR — RED — gereksiz; karar TASARIM'a işlenir
20-093 — YANLIŞ — TEKRAR — 20-038
20-094 — KARAR — TEKRAR — 20-024
20-097 — KARAR — TEKRAR — 20-056
20-098 — KARAR — TEKRAR — 20-033
20-099 — KARAR — RED — kapsam dışı; yedek yok kararı (zip yedek)
20-100 — KARAR — RED — aşırı kurulum (15 dk sınırı); araç ölçütü 20-056

## Özet

Etiket sayıları (grep): VAR 37, TEKRAR 15, YENİ 6, RED 26. Toplam 84 satır (YANLIŞ 13 dahil).

YENİ maddeler:
- 20-003: TASARIM §5.11 deneme günlüğüne manifest sha256 ekle; koşu başında doğrula, uyuşmazsa dur.
- 20-006: TASARIM §5.8 kural kaydı parmak izi = `git rev-parse HEAD`; kirli ağaçta resmi koşu reddedilir.
- 20-019: AGENTS.md satır 43: ADR yok; karar TASARIM.md, gerekçe docs/sorgu/.
- 20-031: AGENTS.md satır 35 ve 39: `.scratch/` ve beş etiket yerine tek `TODO.md` (≤20 satır).
- 20-033: AGENTS.md Çalışma kuralları: git gönderme (push), `reset --hard`, `veri/` silme, kural parametresi değiştirme yok; yeni paket yalnız Levent onayıyla (satır 28).
- 20-038: AGENTS.md satır 12: belge çelişirse dur ve Levent'e sor; TASARIM/KURALLAR/AGENTS onaysız değişmez.

YANLIŞ olup VAR olmayanlar:
- 20-003 YENİ: yukarıdaki değişiklik.
- 20-031 YENİ: yukarıdaki değişiklik.
- 20-037 TEKRAR: 20-033.
- 20-038 YENİ: yukarıdaki değişiklik.
- 20-093 TEKRAR: 20-038.
