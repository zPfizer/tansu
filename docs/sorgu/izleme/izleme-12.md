# İzleme 12: Ortam ve bağımlılıklar (cevaplar-12-ortam.md)

Karşılaştırılan: TASARIM taslak 6, KURALLAR, GLOSSARY, sonuc-3-4, AGENTS.md, pyproject.toml.
Dosyada EKSİK hüküm yok; 54 KARAR ve 13 YANLIŞ işlendi (67 madde).

12-003 — KARAR — VAR — sonuc C-2 ve pyproject (`requires-python = "==3.14.*"`, aynı anlam)
12-005 — KARAR — VAR — sonuc C-2 (`requires-python`, uv yok); venv kurulumu için bkz. 12-088
12-006 — YANLIŞ — VAR — TASARIM 4 (vectorbt kullanılmaz), sonuc C-2, pyproject'te yok
12-010 — YANLIŞ — VAR — sonuc C-2 (duckdb çıkanlar listesinde), TASARIM 3 (veritabanı yok), pyproject'te yok
12-012 — KARAR — VAR — sonuc C-4 (parquet, pyarrow) ve pyproject
12-013 — KARAR — TEKRAR — 12-039 (içerik hash'i)
12-014 — KARAR — VAR — TASARIM 4 `istatistik` (statsmodels `coint` ve Holm için), sonuc C-2, pyproject
12-016 — YANLIŞ — VAR — TASARIM 4 `gostergeler` ("Kütüphane yok"), sonuc C-2 (pandas-ta-classic çıkar); ATR testi için bkz. 12-018
12-018 — YANLIŞ — YENİ — sonuc C-9 test yüzleri listesine `gostergeler` ekle: Wilder ATR(14) ve EMA için elle hesaplı 5 satırlık örnek testi (listede `gostergeler` yok)
12-019 — KARAR — RED — Yahoo tamamen çıktı; yfinance sonuc C-2 çıkanlar listesinde (C-2 ile çelişir)
12-020 — KARAR — RED — Yahoo kararı (sonuc B-2): sadakat İş Yatırım ham seriyle yapılır, yfinance yolu yok
12-021 — KARAR — VAR — KURALLAR 4 ("sonuç kaydedilir"); yfinance kısmı geçersiz (sonuc B-2, C-2)
12-023 — KARAR — RED — TASARIM 4 ve sonuc C-2 borsapy'yi faiz, sektör ve endeks günleri kaynağı yapar; elle CSV C-2 ile çelişir
12-026 — YANLIŞ — VAR — sonuc C-2 (`==` sabit, requirements.lock.txt), pyproject; borsapy ekte olsun kısmı C-2 ile çelişir, uygulanmaz
12-027 — KARAR — VAR — sonuc C-2 (yalnız `==`, hash zorunluluğu yok)
12-028 — YANLIŞ — VAR — sonuc C-2 (`pip freeze` ile requirements.lock.txt); temizlik adımında yapıldı
12-030 — KARAR — YENİ — TASARIM 5.11 deneme günlüğü satırına Python, pandas, numpy, scipy, statsmodels sürümleri ve requirements.lock.txt sha256 alanı ekle (şu an yok)
12-031 — KARAR — VAR — sonuc C-2 (uv yok), AGENTS çalışma kuralları (`.venv\Scripts\python.exe`), TASARIM 4 `__main__`
12-037 — KARAR — RED — kapsam dışı: etkilenen satırlar silinen ön deneme kodundadır (TASARIM 7.1)
12-038 — KARAR — TEKRAR — 12-039 (içerik hash'i, datetime64[ns] çevirisi)
12-039 — KARAR — RED — aşırı kurulum: anlık görüntü bir kez yazılır ve değişmez, sonuc C-4 manifest sha256 yeter; sürümler kilitli
12-040 — YANLIŞ — VAR — sonuc C-2 (kilit dosyası); "olgun kütüphane" ölçütü belgelerde yok, silinecek bir şey yok; altın dosya kısmı 12-042'de RED
12-041 — KARAR — VAR — sonuc C-2 (`==` sabit, kilit dosyası; yükseltme elle yapılır); altın dosya şartı 12-042'de RED
12-042 — KARAR — RED — aşırı kurulum: TASARIM 5.3 motor sınamaları ve sonuc C-9 elle hesaplı testler kayma ve hatayı yakalar; kilitli sürümler
12-044 — KARAR — TEKRAR — 12-030 (aynı günlük satırı; tohum zaten TASARIM 5.11'de, numpy sürümü 12-030 ile gelir)
12-045 — YANLIŞ — VAR — TASARIM 4 ("Ölçütler kısa kendi kodumuzdur"), sonuc C-2 (quantstats çıkar)
12-047 — YANLIŞ — VAR — TASARIM 4 (ölçütler kendi kodumuzdur; "quantstats'tan" cümlesi draft 6'da yok), sonuc C-9 (Simülatör, İstatistik testleri)
12-048 — YANLIŞ — VAR — TASARIM 3 (Streamlit yok), sonuc C-1; Kanıt ekranı HTML rapordur (TASARIM 3, 6)
12-050 — KARAR — VAR — sonuc C-1 (Streamlit yok), TASARIM 3
12-051 — KARAR — VAR — TASARIM 4 `__main__` (`python -m tansu gunluk`), AGENTS çalışma kuralları
12-052 — KARAR — VAR — TASARIM 6.1, sonuc C-7 (Görev Zamanlayıcı tanımı `kurulum/`)
12-053 — YANLIŞ — VAR — TASARIM 6.1 ve sonuc C-7 (kaçırılan koşu çalışır), TASARIM 6.2 (her koşu tam indirme, eksik gün kendiliğinden dolar); schedule pyproject'te yok
12-054 — KARAR — VAR — sonuc C-7 (stdlib logging, `gunluk/` günlüğü), TASARIM 6.2 ve 6.7 (kart yok, `durum.txt` SORUNLU)
12-055 — KARAR — VAR — sonuc C-2 (kilit dosyası yeter) ve sonuc C-10 (yedek tutulmaz)
12-056 — KARAR — RED — yedek yok kararı (sonuc C-10, D-2)
12-060 — KARAR — VAR — TASARIM 6.4 (CSV `;` ayraç, ondalık virgül, UTF-8 BOM)
12-061 — YANLIŞ — VAR — sonuc C-10 (`rapor/` ignore, izlenen ön deneme dosyaları `git rm --cached`), AGENTS Git kuralı, TASARIM 7.1
12-062 — KARAR — VAR — TASARIM 4 (paket düz, `tansu/`), sonuc C-3, pyproject `pythonpath`
12-063 — KARAR — VAR — pyproject (`[build-system]` yok), TASARIM 4 (kurulabilir paket gerekmez)
12-064 — KARAR — VAR — TASARIM 4 ve sonuc C-3 (tek paket `tansu`)
12-065 — KARAR — VAR — pyproject (`dev = ["pytest==9.1.1"]`), sonuc C-2
12-066 — KARAR — VAR — sonuc C-2 (geliştirme: pytest) ve C-9 (hypothesis/coverage/CI yok); mypy, ruff, pre-commit pyproject'te yok
12-067 — KARAR — VAR — sonuc C-9 (hypothesis/coverage/CI yok)
12-068 — KARAR — VAR — AGENTS çalışma kuralları (test kapısı: commit öncesi `.venv\Scripts\python.exe -m pytest -q`)
12-070 — KARAR — VAR — TASARIM 4 `gostergeler` (kütüphane yok), sonuc C-6 (hash kod dosyalarını kapsar)
12-071 — KARAR — RED — kilit hash'i kural kimliğine girmezse Holm sayımı şişmez (sonuc C-6); sürüm izi 12-030 ile günlükte tutulur
12-073 — KARAR — VAR — AGENTS Bağımlılık kuralı (yeni paket öncesi TASARIM 4 ve stdlib'e bak, `==` ile yaz)
12-074 — KARAR — VAR — sonuc C-8 (HTTP requests), C-2 (httpx yok), pyproject
12-075 — KARAR — RED — C-3 ile çelişir (HTTP istemcisi `kaynak` modülündedir, `veri.py`'de değil); ağ testleri sonuc C-9 ile kapalı
12-076 — KARAR — VAR — sonuc C-8 (şema doğrulaması `assert`), pydantic yok (C-2)
12-077 — KARAR — VAR — sonuc C-8 (requests, zaman aşımı, 3 deneme), TASARIM 4 (yerel önbellek)
12-078 — KARAR — RED — spekülatif: sorun çıkmadan truststore eklenmez; kapsam dışı
12-079 — KARAR — RED — TASARIM 4 ("Takvim, fiyat günlerinden çıkar") ve sonuc C-3 ile çelişir; elle takvim dosyası yok
12-080 — KARAR — VAR — pyproject (`tzdata==2026.5`), sonuc C-2
12-082 — KARAR — RED — aşırı kurulum: pip-audit kurulmaz; tek kullanıcı, yerel PC
12-087 — KARAR — VAR — AGENTS çalışma kuralları (Python `.venv\Scripts\python.exe`)
12-088 — KARAR — YENİ — AGENTS çalışma kuralları'na 2 satır kurulum: `py -3.14 -m venv .venv` ve `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt`; veri yedeği adımı yok
12-089 — KARAR — RED — yedek yok kararı (sonuc C-10, D-2); veri yeniden indirilir (sonuc C-4)
12-090 — KARAR — RED — yedek yok kararı (sonuc C-10, D-2)
12-092 — YANLIŞ — VAR — sonuc C-11 ("numba yok"), C-2 (numba çıkar), TASARIM 4 (vectorbt yok), pyproject'te yok
12-094 — KARAR — VAR — pyproject (`pandas==3.0.6`), sonuc C-2
12-095 — KARAR — VAR — pyproject (scipy var, scikit-learn yok), sonuc C-2 (scipy kalır) ve C-11 (joblib yalnız yetmezse)
12-096 — KARAR — VAR — TASARIM 3 ve sonuc C-1 (HTML rapor, panel yok), pyproject'te matplotlib yok
12-097 — KARAR — RED — C-3 ile çelişir (modül listesinde `ayar` yok; sabitler ilgili modülde, maliyet tek sabit TASARIM 4); TOML/YAML zaten yok
12-098 — KARAR — VAR — sonuc C-6 (donmuş dataclass), pydantic yok (C-2)
12-099 — KARAR — TEKRAR — 12-030 (rapor başlığına aynı sürümler; deneme günlüğü satırı yeter)
12-100 — KARAR — VAR — AGENTS çalışma kuralları (test kapısı: pytest -q); altın dosya kısmı 12-042'de RED

## Özet

Sayım (grep ile): VAR 45 · TEKRAR 4 · YENİ 3 · RED 15 · toplam 67 (54 KARAR + 13 YANLIŞ).

YENİ maddeler:
- 12-018: sonuc C-9 test yüzlerine `gostergeler` ekle; Wilder ATR(14) ve EMA için elle hesaplı küçük test.
- 12-030: TASARIM 5.11 deneme günlüğü satırına Python, pandas, numpy, scipy, statsmodels sürümleri ve requirements.lock.txt sha256 ekle.
- 12-088: AGENTS çalışma kuralları'na 2 satır kurulum (`py -3.14 -m venv .venv`, `pip install -r requirements.lock.txt`).

YANLIŞ maddeler, VAR olmayanlar:
- 12-018 (YENİ): yukarıdaki değişiklik.
- Başka yok. Diğer 12 YANLIŞ madde VAR (12-006, 12-010, 12-016, 12-026, 12-028, 12-040, 12-045, 12-047, 12-048, 12-053, 12-061, 12-092).
