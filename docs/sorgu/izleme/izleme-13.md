# İzleme 13: Veri depolama (cevaplar-13-depolama.md)

Karşılaştırılan tasarım: TASARIM taslak 6, KURALLAR, GLOSSARY, sonuc-3-4, AGENTS, pyproject. Dosyada EKSİK hükmü yok; KARAR 76, YANLIŞ 6.
Not: sonuc C-4 kimliği `YYYYMMDD-HHMM` olarak yazar; cevap dosyası `YYYYMMDD-8 hex` önerir (bkz. 13-007).

13-001 — KARAR — VAR — sonuc C-4 (her akşam tam indirme), TASARIM 6.2
13-002 — KARAR — VAR — sonuc C-4 (indirme başına klasör, parquet + manifest sha256)
13-004 — YANLIŞ — VAR — sonuc C-4 (parquet, veritabanı yok), sonuc C-2 (duckdb çıkar)
13-006 — KARAR — YENİ — TASARIM 4 `veri` satırına: "okuyucu AG'yi açarken manifest sha256'sını doğrular; uyuşmazlık = hata" (salt okunur bayrağı eklenmez)
13-007 — KARAR — RED — sonuc C-4 ile çelişir (kimlik YYYYMMDD-HHMM); hash eki aşırı kurulum
13-008 — KARAR — RED — aşırı kurulum; veri kapıları (TASARIM 5.13) ve borsapy karşılaştırması (5.1) yeter, HGDG zaten her olayda değişir
13-009 — KARAR — VAR — TASARIM 4 ve 5.1 (ham HG ve düzeltilmiş HGDG seriler)
13-010 — KARAR — TEKRAR — 13-011
13-011 — KARAR — YENİ — TASARIM 4 `veri` notuna: "AG = tek klasör; içinde fiyat.parquet (uzun biçim, tüm semboller), olaylar, faiz, borsapy getirileri; veri sürümü = AG kimliği"
13-012 — KARAR — RED — Yahoo kararı (sonuc B-2): Yahoo hiç kullanılmaz, ayrı klasör gerekmez
13-013 — KARAR — VAR — sonuc C-8 (şema `assert`); `sema_surumu` alanı gereksiz
13-014 — KARAR — VAR — sonuc O1 ve TASARIM 5.1 (HACIM TL)
13-015 — KARAR — YENİ — TASARIM 4 `veri` notuna: "tarih sütunu saat dilimsiz saf tarih (datetime64)"
13-016 — KARAR — RED — karar gerektirmez; pandas varsayılanı (float64)
13-017 — KARAR — TEKRAR — 13-011
13-018 — KARAR — RED — aşırı kurulum; ayrıştırıcı hatasında yeniden indirme yeter (tam indirme, sonuc C-4)
13-019 — KARAR — TEKRAR — 13-011
13-021 — KARAR — VAR — TASARIM 4 (olay tarihi hak kullanım günüdür), sonuc O3
13-022 — KARAR — TEKRAR — 13-025
13-023 — KARAR — TEKRAR — 13-082
13-024 — KARAR — VAR — TASARIM 5.2 (işlemi kapanan hisseler)
13-025 — KARAR — RED — gereksiz karar; tasarımda türetilmiş depo zaten yok (evren her koşuda hesaplanır, TASARIM 4)
13-026 — KARAR — VAR — sonuc C-4 (her akşam tam indirme)
13-028 — YANLIŞ — VAR — sonuc C-4 (tam indirme; örtüşme penceresi yok)
13-029 — KARAR — VAR — sonuc C-4, TASARIM 6.2 (geçici klasör, kapılar geçerse os.replace)
13-030 — KARAR — VAR — TASARIM 5.13 (bozuk satır karantina sayılır, silinmez)
13-032 — KARAR — VAR — TASARIM 5.13 ve 6.2 (kapılar AG olmadan önce)
13-034 — KARAR — YENİ — TASARIM 5.11 sonuna: "deneme günlüğünde adı geçen AG silinmez" (20 GB eşiği alınmaz)
13-035 — KARAR — TEKRAR — 13-034
13-036 — YANLIŞ — VAR — sonuc C-4 (her akşam tam indirme, delta yok)
13-037 — KARAR — RED — karar gerektirmez; pyarrow varsayılanı
13-038 — KARAR — VAR — sonuc C-10 (`rapor/`, `*.parquet` ignore, `git rm --cached`), AGENTS (veri ve rapor git'e girmez)
13-039 — KARAR — RED — yedek yok kararı (sonuc D-2)
13-040 — KARAR — VAR — sonuc C-6 (deneme.jsonl git'te), TASARIM 5.11
13-041 — YANLIŞ — VAR — sonuc C-10 ve AGENTS (veri git dışı; LFS/DVC bağımlılık listesinde yok, C-2)
13-042 — KARAR — RED — yedek yok kararı
13-043 — KARAR — RED — yedek yok kararı
13-045 — KARAR — RED — aşırı kurulum; os.replace C-4'te var, yeniden deneme gerekmez (hata = koşu SORUNLU, TASARIM 5.13)
13-047 — KARAR — RED — aşırı kurulum; C-4 yalnız sha256 ister, ek alanlar veriden okunur
13-048 — KARAR — VAR — sonuc C-6, AGENTS (günlük yalnız eklenir)
13-049 — KARAR — VAR — AGENTS (günlük düzenlenmez ve silinmez), sonuc C-6
13-050 — KARAR — VAR — sonuc C-6 (Holm birimi benzersiz kural kimliği), TASARIM 5.11
13-051 — KARAR — VAR — TASARIM 5.11 (aynı kuralın tekrar koşusu yeni deneme değildir)
13-052 — KARAR — RED — sonuc C-6 ile çelişir (kural kimliği yalnız kod + parametre; AG deneme günlüğündedir, 5.11)
13-053 — KARAR — TEKRAR — 13-034
13-054 — KARAR — TEKRAR — 13-082
13-055 — KARAR — RED — aşırı kurulum; günde bir koşu, çakışma Zamanlayıcı'da yok sayılır (sonuc C-7)
13-056 — YANLIŞ — VAR — TASARIM 7.1 ve sonuc C-3 (Yahoo kodu, `veri.py` önbelleği silindi)
13-057 — KARAR — TEKRAR — 13-006
13-058 — KARAR — RED — yedek yok kararı (hata verme kısmı 13-006'da)
13-059 — KARAR — RED — yedek yok kararı
13-060 — KARAR — RED — kod ayrıntısı; jsonl düzenleme AGENTS ile çelişir
13-061 — KARAR — RED — aşırı kurulum
13-063 — KARAR — VAR — TASARIM 5.11 (günlüğe veri anlık görüntüsü yazılır)
13-064 — KARAR — RED — aşırı kurulum; klasör adı sıralanır, en yeni klasör yeter (sonuc C-4)
13-065 — KARAR — VAR — sonuc C-7 (kilitsiz; çakışma yok sayılır), C-2 (filelock yok)
13-066 — KARAR — VAR — sonuc C-7 (çakışmayı yok say); `.kilit` dosyası aşırı kurulum
13-067 — KARAR — RED — tam indirme boşluğu kapatır (sonuc C-4); ek fark raporu aşırı kurulum
13-068 — KARAR — VAR — TASARIM 5.1 (bugünkü veri) ve 6.7 (durum.txt VERİ YOK)
13-072 — KARAR — TEKRAR — 13-011
13-073 — KARAR — TEKRAR — 13-025
13-074 — KARAR — TEKRAR — 13-025
13-075 — KARAR — TEKRAR — 13-082
13-076 — KARAR — TEKRAR — 13-011
13-077 — KARAR — RED — kapsam dışı; gerçek BIST100 elle listeleri paralel iş (TASARIM 7.10)
13-079 — KARAR — TEKRAR — 13-024
13-081 — KARAR — TEKRAR — 13-007
13-082 — KARAR — YENİ — TASARIM 6.7 / rapor: rapor ve kart CSV ilk satırına "Veri: <AG kimliği>, son çubuk <tarih>, <n> sembol"
13-083 — KARAR — VAR — sonuc C-6, TASARIM 5.11 (günlük: kural kimliği, anlık görüntü, commit); AG karşılaştırma kısmı 13-008 gibi RED
13-085 — KARAR — VAR — sonuc C-2 (`==` sabitleme), pyproject.toml
13-086 — KARAR — VAR — TASARIM 6.4 (CSV `;`, ondalık virgül, UTF-8 BOM)
13-087 — KARAR — RED — Yahoo kararı (sonuc B-2); eski veri/yahoo klasörü gerekmez
13-088 — KARAR — VAR — sonuc C-9 (ağ kapalı, sentetik veri, testte literal)
13-089 — KARAR — RED — kod ayrıntısı; testler C-9'a göre yazılır, belge kararı gerekmez
13-090 — KARAR — TEKRAR — 13-089
13-091 — KARAR — VAR — sonuc C-4 ve TASARIM 6.2 (yazma geçici klasörde, tam ve geçerliyse os.replace)
13-093 — KARAR — RED — kapsam dışı; ilk sürümde ek komut yok (TASARIM 4 `__main__` yalnız gunluk/sinama)
13-096 — KARAR — RED — kod ayrıntısı; imza testlerden çıkar (AGENTS: önce test)
13-097 — KARAR — TEKRAR — 13-082
13-099 — KARAR — TEKRAR — 13-082
13-100 — KARAR — VAR — TASARIM 4 (`veri` tek modül, AG değişmez), sonuc C-3
13-084 — YANLIŞ — VAR — sonuc C-2 ve pyproject.toml (pandas==3.0.6, pyarrow==25.0.1 yazılı)

## Özet

Sayımlar (grep, 82 satır): VAR 33, TEKRAR 19, YENİ 5, RED 25.

YENİ maddeler:
- 13-006: TASARIM 4 `veri` satırına "okuyucu AG'yi açarken manifest sha256'sını doğrular; uyuşmazlık = hata".
- 13-011: TASARIM 4 `veri` notuna "AG = tek klasör; fiyat.parquet (uzun biçim), olaylar, faiz, borsapy; veri sürümü = AG kimliği".
- 13-015: TASARIM 4 `veri` notuna "tarih sütunu saat dilimsiz saf tarih".
- 13-034: TASARIM 5.11 sonuna "deneme günlüğünde adı geçen AG silinmez".
- 13-082: TASARIM 6.7: rapor ve kart CSV ilk satırına AG kimliği, son çubuk tarihi, sembol sayısı.

YANLIŞ maddeler (6): hepsi VAR (13-004, 13-028, 13-036, 13-041, 13-056, 13-084). YENİ ya da RED olan YANLIŞ yok.

