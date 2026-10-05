# İzleme 16: cevaplar-16-kosu.md izlemesi

Kapsam: dosyada EKSİK hükmü yok. KARAR 74 satır, YANLIŞ 4 satır izlendi. CEVAPLI, OLGU ve ZAYIF SORU satırları kapsam dışıdır.
Karşılaştırılan belgeler: TASARIM (taslak 6), KURALLAR, GLOSSARY, sonuc-3-4 (B-n, C-n), AGENTS.md, pyproject.toml.

16-001 — KARAR — YENİ — TASARIM 4 `__main__` satırı: `gunluk | sinama | sadakat | kayit` (şu an yalnız gunluk/sinama yazılı); rapor ayrı komut olmaz.
16-002 — KARAR — VAR — TASARIM 4 `__main__` ve 6.1 (`python -m tansu gunluk`), sonuc C-7; venv python yolu AGENTS "Çalışma kuralları".
16-003 — KARAR — VAR — sonuc C-2 (bağımlılık listesinde typer yok) ve AGENTS "Bağımlılık" (önce stdlib); argparse adı yazılı değil, ama başka kütüphane eklenemez.
16-004 — YANLIŞ — VAR — pyproject.toml'da `[project]`, `==` sabitli bağımlılıklar ve tzdata var; sonuc C-2 (pandas-ta-classic ve quantstats çıktı, cevaptaki liste eskidir).
16-005 — KARAR — VAR — TASARIM 6.1 (görev yalnız `gunluk` çalıştırır).
16-006 — KARAR — VAR — TASARIM 6.7 ("Levent yalnız buna bakar").
16-007 — KARAR — VAR — TASARIM 6 (günlük işleyiş tek komutta, 6.1 yeniden deneme).
16-008 — KARAR — YENİ — TASARIM 4 `__main__` satırı: `gunluk` bayraksız; `sinama --son` (1.000 tekrar, bayraksız 200, 5.7).
16-010 — KARAR — VAR — sonuc C-7 (`gunluk/YYYY-MM-DD.log`, stdlib logging).
16-011 — KARAR — VAR — TASARIM 8.1 (yayın saati açık soru) ve 6.1 (saatte bir yeniden deneme), sonuc C-7 (19:30 + 4 saat tekrar).
16-012 — KARAR — YENİ — TASARIM 6.1: görev ayarları tek satır: yalnız oturum açıkken (parolasız), WakeToRun kapalı, StartWhenAvailable, IgnoreNew, ExecutionTimeLimit PT1H, WorkingDirectory depo kökü, RunOnlyIfNetworkAvailable.
16-013 — KARAR — TEKRAR — 16-012 (WakeToRun kapalı aynı görev ayarı satırında).
16-014 — KARAR — VAR — TASARIM 6.1 ("Tanım dosyası depoda (`kurulum/`)"), sonuc C-7.
16-015 — KARAR — VAR — AGENTS "Çalışma kuralları" (Python `.venv\Scripts\python.exe`) ve TASARIM 6.7 (son başarılı koşu saati eski kalırsa Levent görür).
16-016 — KARAR — TEKRAR — 16-012 (WorkingDirectory depo kökü).
16-017 — KARAR — VAR — sonuc C-7 ("çakışmayı yok say").
16-018 — KARAR — TEKRAR — 16-012 (ExecutionTimeLimit PT1H).
16-019 — KARAR — VAR — TASARIM 6.7 (kanıt `durum.txt` ve günlük; zamanlayıcı geçmişi kullanılmaz).
16-020 — KARAR — TEKRAR — 16-012 (oturum açıkken çalıştır aynı hesabı zorlar).
16-022 — KARAR — RED — değişiklik gerektirmez; öncelik ayarı yok kararı (aşırı kurulum).
16-023 — KARAR — VAR — TASARIM 6.1 ("Kaçırılan koşu, bilgisayar açılınca çalışır"), sonuc C-7.
16-025 — KARAR — VAR — TASARIM 6.6 (açık kartlar her gün sinyal gününden itibaren Adım ile yeniden hesaplanır), sonuc C-5.
16-026 — KARAR — VAR — TASARIM 6.6 ve 5.3 (Adım gün gün işler; kapanış mum tarihiyle).
16-027 — KARAR — RED — aşırı kurulum: `kosular.csv` yeni dosya; 16-035 için `durum.txt` son başarılı koşu tarihi yeter.
16-028 — KARAR — RED — aşırı kurulum: TASARIM 6.7 son başarılı koşu saati eski kalınca bayatlığı zaten gösterir; ESKİ etiketi ve gün sayacı gereksiz.
16-029 — KARAR — RED — aşırı kurulum: TASARIM 5.8 dönemi zaten "6 ay ve 30 işlem" ile uzatır; %10 uyarısı gereksiz.
16-030 — KARAR — RED — kapsam dışı: geriye dönük sinyal listesi "veri deliği" raporu; asgari sistem değil.
16-032 — KARAR — RED — yeni kayıt türü gerekmez (aşırı kurulum); değişiklik yok.
16-033 — KARAR — VAR — TASARIM 6.1 (başarısızsa 4 saat saatte bir yeniden dener), sonuc C-7; "TAMAM varsa çık" kısmı 16-035'te.
16-034 — KARAR — VAR — TASARIM 6.1 (kaçırılanı zamanlayıcı çalıştırır), sonuc C-7; kodda ek mantık yok.
16-035 — KARAR — YENİ — TASARIM 6.1: bugün için `durum.txt` son başarılı koşu tarihi bugünse `gunluk` hiçbir şey yapmadan çıkar (tekrarlı tetikleyici başarıdan sonra da çalışır); bir test.
16-036 — KARAR — YENİ — TASARIM 6.7: `durum.txt` ve kart CSV geçici dosyaya yazılır, `os.replace` ile adlandırılır (anlık görüntü için C-4 zaten böyle).
16-037 — KARAR — TEKRAR — 16-035 (aynı gün ikinci anlık görüntü yok).
16-038 — YANLIŞ — VAR — TASARIM 5.1 "Bugünkü veri" (son çubuk tarihi), sonuc C-4; `st_mtime` kodu yok (grep: .py dosyalarında sonuç yok, temizlik yapıldı).
16-039 — KARAR — TEKRAR — 16-035 (ikinci koşu çıkar; sınama aynı test).
16-040 — KARAR — RED — kapsam dışı: rapor HTML (TASARIM 3); TASARIM 5.11 alanları (tarih, kural kimliği, anlık görüntü, commit, tohum) izlenebilirlik için yeter.
16-041 — KARAR — VAR — TASARIM 5.11 (Holm benzersiz kural kimliğiyle; tekrar koşu yeni deneme değil), sonuc C-6, AGENTS (yalnız ekleme); CSV adı C-6 ile çelişir, `kayit/deneme.jsonl` geçerli.
16-043 — KARAR — VAR — TASARIM 6.2 (geçici klasör, kapılar geçerse yeni anlık görüntü), sonuc C-4.
16-044 — KARAR — TEKRAR — 16-001 (`kayit` alt komutu); yalnız ekleme zaten sonuc C-6.
16-045 — YANLIŞ — VAR — sonuc C-7 ("çakışmayı yok say") ve C-4 (`os.replace`); kilit hiçbir belgede yok, cevabın düzeltmesi "kilit yok" ile uyumlu.
16-053 — KARAR — VAR — sonuc C-7 (stdlib logging), C-2 (loguru yok).
16-054 — KARAR — VAR — sonuc C-7 (`gunluk/`) ve TASARIM 6.7.
16-055 — KARAR — VAR — sonuc C-7 (`gunluk/YYYY-MM-DD.log`).
16-056 — KARAR — TEKRAR — 16-055 (döndürme ve silme yok, günlük dosya).
16-058 — KARAR — RED — kod ayrıntısı (günlük satır biçimi); belgeye gerek yok.
16-059 — KARAR — RED — kod ayrıntısı; sinama kaydı için commit ve anlık görüntü zaten TASARIM 5.11'de.
16-060 — KARAR — VAR — sonuc C-7 (`gunluk/` işletim) ve C-6 (`kayit/deneme.jsonl` bilimsel).
16-061 — KARAR — RED — kod ayrıntısı (captureWarnings); aşırı kurulum.
16-062 — KARAR — YENİ — TASARIM 6.1: `__main__` en üst düzeyde yakalanmayan istisnayı günlüğe yazar ve çıkış kodu 1 verir.
16-063 — KARAR — RED — kod ayrıntısı (günlük düzeyleri); SORUNLU koşulları zaten TASARIM 5.13'te.
16-064 — KARAR — RED — kod ayrıntısı (utf-8); CSV kodlaması TASARIM 6.4'te var.
16-065 — KARAR — RED — gereksiz: sistem emir vermez ve hesap bilgisi tutmaz (TASARIM 1); yeni kural gerekmez.
16-066 — KARAR — RED — kod ayrıntısı (sinama günlük sıklığı); aşırı kurulum.
16-067 — KARAR — VAR — TASARIM 6.7 (tek kanal `durum.txt`) ve TASARIM 3 (Telegram yok).
16-068 — KARAR — TEKRAR — 16-062 (çıkış kodu 1 = beklenmeyen istisna; başka kod yok).
16-069 — KARAR — VAR — TASARIM 5.1 "Bugünkü veri" (kart yok) ve 6.7 (`SORUNLU`).
16-070 — KARAR — YENİ — TASARIM 6.7: ilk satır değerlerine `BUGÜN ÇUBUK YOK` (tatil, çıkış 0) eklenir; `VERİ YOK` ile karışmaz.
16-071 — KARAR — VAR — TASARIM 6.7 (son başarılı koşu saati); Streamlit kısmı sonuc C-1 ile çıktı.
16-073 — KARAR — VAR — TASARIM 3 (Telegram yok) ve 6.7; sonuc C-1.
16-075 — KARAR — VAR — TASARIM 6.7 (Türkçe eylem cümlesi).
16-076 — KARAR — VAR — TASARIM 5.13 "Günlük koşu" (100 hisseden 5'ten fazlası inmezse SORUNLU), sonuc C-7.
16-077 — KARAR — VAR — sonuc C-7 (Europe/Istanbul) ve pyproject.toml (`tzdata==2026.5`).
16-078 — KARAR — TEKRAR — 16-079 ("bugün" İstanbul saatinden).
16-079 — KARAR — VAR — sonuc C-7 ve TASARIM 6.1 (saat Europe/Istanbul).
16-080 — KARAR — RED — kod ayrıntısı (tarih tipi ve ISO ofset); aşırı kurulum.
16-081 — KARAR — RED — kod ayrıntısı (saat dilimi atma); `kaynak`/`veri` sınamasında yakalanır.
16-084 — KARAR — VAR — TASARIM 5.1 "Bugünkü veri" (saate değil son çubuk tarihine bakar).
16-085 — YANLIŞ — VAR — TASARIM 4 ("Takvim, fiyat günlerinden çıkar (XU100 günleri, borsapy)"), sonuc C-3; tatil listesi hiçbir belgede yok.
16-088 — KARAR — RED — değişiklik gerektirmez (yarım gün özel kural yok); cevaptaki "hacim olağandışı kontrolü" TASARIM 5.1'de yok.
16-091 — KARAR — VAR — TASARIM 4 (takvim XU100 günleri) ve 5.13 (indirilemeyen hisse sayısı eşiği).
16-092 — KARAR — VAR — TASARIM 6.1 ("hafta içi 19:30").
16-093 — KARAR — RED — C-8 ile çelişir (C-8: 1 sn aralık, zaman aşımı (5, 30), 3 deneme; cevap: 2 deneme, 5 sn).
16-094 — KARAR — VAR — sonuc C-8 (requests, elle deneme) ve C-2 (tenacity yok).
16-095 — KARAR — VAR — TASARIM 5.13 (5'ten çoğu inmezse SORUNLU) ve 5.2 (bulunamayan semboller raporda).
16-097 — KARAR — VAR — TASARIM 6.1 (saatte bir yeniden dener), sonuc C-7; RunOnlyIfNetworkAvailable 16-012'dedir.
16-098 — KARAR — VAR — sonuc C-8 ("şema `assert`") ve TASARIM 5.13 (satır şartları).
16-099 — KARAR — YENİ — TASARIM 5.1 "İkinci kaynak": borsapy alınamazsa çapraz kontrol atlanır, günlüğe UYARI ve `durum.txt` ikinci satırı "çapraz kontrol yok".
16-100 — KARAR — VAR — AGENTS "Deneme günlüğü" (her sınama koşusu) ve TASARIM 5.11, sonuc C-6; günlük koşu sınama değildir.

## Özet

Sayımlar (grep ile, yazımdan sonra):

- Toplam 78 madde: VAR 42, TEKRAR 10, YENİ 8, RED 18.
- Hüküm türü: KARAR 74, YANLIŞ 4, EKSİK 0.

YENİ maddeler (önerilen değişiklik):
- 16-001: TASARIM 4 `__main__` satırı `gunluk | sinama | sadakat | kayit` olur; rapor ayrı komut olmaz.
- 16-008: TASARIM 4 `__main__`: `gunluk` bayraksız; `sinama --son` (1.000 tekrar, bayraksız 200).
- 16-012: TASARIM 6.1'e görev ayarları satırı (oturum açıkken/parolasız, WakeToRun kapalı, StartWhenAvailable, IgnoreNew, PT1H, WorkingDirectory, RunOnlyIfNetworkAvailable). 16-013, 16-016, 16-018, 16-020 bunu tekrarlar.
- 16-035: TASARIM 6.1: `durum.txt` son başarılı koşu tarihi bugünse `gunluk` çıkar; bir test. 16-037, 16-039 bunu tekrarlar.
- 16-036: TASARIM 6.7: `durum.txt` ve kart CSV geçici dosya + `os.replace` ile yazılır.
- 16-062: TASARIM 6.1: `__main__` yakalanmayan istisnayı günlüğe yazar, çıkış kodu 1. 16-068 bunu tekrarlar.
- 16-070: TASARIM 6.7: ilk satıra `BUGÜN ÇUBUK YOK` (tatil) değeri eklenir.
- 16-099: TASARIM 5.1: borsapy yoksa çapraz kontrol atlanır; UYARI + `durum.txt` ikinci satır.

YANLIŞ olup VAR olmayan madde: yok. Dört YANLIŞ maddenin hepsi VAR: 16-004 (pyproject, C-2), 16-038 (TASARIM 5.1 ve kodda `st_mtime` yok), 16-045 (C-7, C-4; kilit yok), 16-085 (TASARIM 4 Takvim, C-3).

Not: 16-027 RED olduğu için `kosular.csv` açılmaz; 16-035 kaydı `durum.txt` tarihinden okur.
