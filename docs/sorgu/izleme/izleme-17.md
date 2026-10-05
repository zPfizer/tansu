# İzleme 17: cevaplar-17-cikti.md maddelerinin taslak 6 ile karşılaştırması

Kapsam: hüküm EKSİK, KARAR ya da YANLIŞ olan maddeler. CEVAPLI (17-016, 17-072) ve ZAYIF SORU maddeleri alınmadı. Dosyada EKSİK hükmü yok.
Genel not: cevap dosyası "3 aile", "SQLite durum deposu", "yedek", "matplotlib/grafik" varsayıyor. Bunlar sonuc C-1, C-4, C-5, C-6, C-10 ve "yedek yok" kararıyla uyuşmaz. İlk sürümde 2 aile var.

17-001 — YANLIŞ — VAR — TASARIM 3 (Streamlit "Yok" listesinde, "Tek dosya HTML rapor" Var listesinde), sonuc C-1
17-002 — KARAR — VAR — TASARIM 3 "Tek dosya HTML rapor", sonuc C-1 "tarayıcıda açılır"
17-003 — YANLIŞ — VAR — sonuc C-1 (HTML, f-string, şablon motoru yok); markdown-it-py pyproject'ta yok, eklenmez
17-004 — KARAR — VAR — sonuc C-1 (f-string, Jinja2 yok); tabulate pyproject'ta yok, yeni bağımlılık eklenmez
17-005 — KARAR — VAR — TASARIM 4 (istatistik hesaplar, rapor yalnız çıktı üretir)
17-006 — KARAR — YENİ — TASARIM 4 `rapor`: dosya adı `rapor/rapor-YYYYMMDD-HHMM.html`, üstüne yazılmaz
17-007 — KARAR — YENİ — TASARIM 4 `rapor`: HTML başlık bloğuna koşu kimliği, veri anlık görüntü tarihi, kod hash'i yazılır
17-008 — KARAR — YENİ — TASARIM 1: rapor ilk satırı sabit cümle "Hiçbir aile kabul ölçütünü geçmedi (0/2)"; aile sayısı 3 değil 2
17-009 — KARAR — TEKRAR — 17-008 (ilk ekran "Geçen aile: n/2"; veri tarihi 17-007'de)
17-010 — KARAR — YENİ — TASARIM 6.5: %95 aralık sıfırı içeriyorsa "ayırt edilemiyor"; p, Holm p, toplam deneme sayısı raporda "Ayrıntı" bölümünde
17-011 — KARAR — VAR — TASARIM 6.5 (örnek zaten "−%0,2 (%95 aralık −%2,4 ile +%2,0)"; "±" yok)
17-012 — KARAR — VAR — TASARIM 5.8, 5.9, 5.11 (yıllık ileri yürüme, yeniden örnekleme, çoklu deneme düzeltmesi Türkçe geçiyor)
17-013 — KARAR — RED — yeni bağımlılık (matplotlib pyproject'ta yok), aşırı kurulum
17-014 — KARAR — VAR — sonuc C-2 (quantstats çıkanlar listesinde)
17-018 — KARAR — RED — matplotlib pyproject'ta yok; ilk sürümde grafik yok (TASARIM 5.12 grafik istemiyor)
17-020 — KARAR — RED — aşırı kurulum: grafik ilk sürümde zorunlu değil, tablo yeter
17-029 — KARAR — VAR — TASARIM 4 (`rapor`: sonuçlar → HTML + CSV + durum.txt, tek yönlü)
17-032 — KARAR — TEKRAR — 17-079 (aile × ölçüt tablosu; "3 aile" yanlış, 2 aile)
17-033 — KARAR — TEKRAR — 17-079 (tablonun kaynağı kabul fonksiyonu çıktısı; uygulama ayrıntısı)
17-034 — KARAR — VAR — TASARIM 6.4 ve GLOSSARY "Canlı / Deneme" (deneme aileleri kartta gösterilmez)
17-035 — KARAR — TEKRAR — 17-093 (yasaklı kelime testi)
17-036 — YANLIŞ — VAR — sonuc C-1, C-2 (Streamlit çıkar); pyproject'ta streamlit yok
17-037 — KARAR — VAR — TASARIM 3, sonuc C-1
17-038 — YANLIŞ — VAR — pyproject.toml (`[project]`, `==` sabit, requires-python) ve sonuc C-2; temizlik adımı yapıldı
17-040 — KARAR — YENİ — AGENTS.md Çalışma kuralları: yollar `pathlib`, dosyalar açıkça `encoding="utf-8"` (CSV'de `utf-8-sig`) ile açılır/yazılır
17-041 — KARAR — YENİ — TASARIM 6.5: CSV sabit sütunlar: Tarih; Hisse; Aile; Durum; Referans; Stop; Pozisyon %; Adet; Fiili risk; Kanıt; Kaynak (Giriş alt/üst ve Hedef çıkar: B-20, hedef yok)
17-042 — KARAR — RED — kapsam dışı: CSV sistemin girdisi değil, her gün ayrı dosya
17-043 — KARAR — VAR — TASARIM 6.4 (`;` ayraç)
17-044 — KARAR — VAR — TASARIM 6.4 (ondalık virgül)
17-045 — KARAR — VAR — TASARIM 6.4 (UTF-8 BOM)
17-046 — KARAR — TEKRAR — 17-084 (biçim kuralları: ISO tarih)
17-047 — KARAR — VAR — sonuc C-5 (açık kartlar CSV'den okunmaz, Adım ile yeniden hesaplanır), TASARIM 6.6
17-048 — KARAR — YENİ — TASARIM 6.7: CSV geçici dosyaya yazılıp `os.replace` ile taşınır; `PermissionError` (Excel'de açık) olursa durum.txt SORUNLU, "CSV açık, kapatıp yeniden çalıştır". SQLite kısmı atılır
17-049 — KARAR — YENİ — TASARIM 6.4: kart CSV'si `rapor/kartlar-YYYYMMDD.csv`, her gün yeni dosya (`rapor/` zaten git dışı); SQLite kısmı atılır
17-050 — KARAR — YENİ — TASARIM 6.4: sinyal yoksa yalnız başlık satırlı CSV yazılır; CSV hiç yok = koşu çalışmadı
17-051 — KARAR — RED — TASARIM 6.7 durum.txt ilk satırı TAMAM/SORUNLU/VERİ YOK; yeni değerler gereksiz, 17-050 ayrımı yapar
17-052 — KARAR — VAR — TASARIM 6.5 (sermayenin yüzdesi ve 1.000.000 TL için adet), sonuc B-20
17-053 — KARAR — VAR — TASARIM 5.6 (adet aşağı yuvarlanır)
17-054 — YANLIŞ — VAR — sonuc B-20, TASARIM 6.5 ve GLOSSARY "Referans fiyat" (giriş yerine sinyal günü kapanışı; gerçek giriş ertesi işlem fiyatı)
17-055 — KARAR — TEKRAR — 17-093 (sabit etiket/sütun listeleri testi)
17-056 — KARAR — YENİ — TASARIM 6.5: kart durumu AKTİF / STOP / BOZULDU (ilk sürümde hedef yok, HEDEF ve TAMAMLANDI yok); TASARIM 2 tablosuna "Tansu'nun etiketleri" notu
17-057 — KARAR — VAR — TASARIM 5.3 "Yeni sinyal" (açık pozisyonda yeni sinyal işlem açmaz)
17-058 — KARAR — VAR — TASARIM 6.6, sonuc C-5 (günlük kart çıktısı `kayit/kartlar.jsonl`'e yalnız eklenir)
17-059 — KARAR — VAR — sonuc C-5 (CSV girdi değil; açık kartlar Adım ile yeniden hesaplanır); SQLite kısmı geçersiz
17-060 — KARAR — RED — C-4 ("veritabanı yok") ve C-5 ile çelişir
17-061 — KARAR — RED — C-4/C-5 ile çelişir (SQLite işlemi gereksiz; durum yok)
17-062 — KARAR — VAR — sonuc C-5 (her gün sinyal gününden yeniden hesap; belirleyici, tekrar koşu aynı sonuç)
17-063 — KARAR — VAR — sonuc C-5 (atlanan gün kaybolmaz, sinyal gününden itibaren hesap), TASARIM 6.1 (kaçırılan koşu)
17-064 — KARAR — RED — yedek yok kararı (sonuc D-2) ve C-5 (SQLite yok)
17-065 — KARAR — RED — yedek yok kararı ve C-5 (SQLite yok)
17-066 — KARAR — RED — C-6 ile çelişir (`kayit/deneme.jsonl`, CSV değil)
17-067 — KARAR — RED — yedek yok kararı (sonuc D-2, AGENTS.md "yedek yok")
17-068 — KARAR — RED — `kartlar/`, `durum.sqlite`, `veri/yedek` çelişir; düzen zaten C-4, C-6, C-7'de (`veri/ag/`, `kayit/`, `gunluk/`, `rapor/`)
17-069 — KARAR — VAR — sonuc C-10 (`rapor/` .gitignore'a), AGENTS.md Git kuralı; `kartlar/` ayrı klasör olmadığı için gerekmez (17-049)
17-070 — KARAR — RED — değişiklik gerektirmez; `son.html` önerisi 17-071'de reddedildi
17-071 — KARAR — RED — aşırı kurulum: tarihli dosya adı ve durum.txt yeter
17-073 — YANLIŞ — VAR — sonuc C-4 (parquet `veri/ag/`), C-10 (`*.parquet` ignore, `git rm --cached`), TASARIM 7.1; `veri/ara/` gerekmez
17-074 — KARAR — YENİ — TASARIM 4 `rapor`: `rapor/islemler-<koşu>.csv` (`;`, utf-8-sig): hisse, aile, giriş/çıkış tarihi, giriş/çıkış fiyatı, çıkış nedeni, getiri
17-075 — KARAR — TEKRAR — 17-074
17-076 — KARAR — TEKRAR — 17-077 (karantina sayısı "Uyarılar" bölümünde)
17-077 — KARAR — YENİ — TASARIM 4 `rapor`: tek "Uyarılar" bölümü, kabul tablosundan sonra (karantina sayısı, bulunamayan semboller, tavan bağlama oranı, olay denetimi farkları); boşsa "Uyarı yok"
17-078 — KARAR — VAR — TASARIM 5.2 "Sonuç" (mutlak getiri karar için kullanılmaz)
17-079 — KARAR — YENİ — TASARIM 5.12: raporda aile başına 6 ölçüt için geçti/kaldı + değer tablosu; genel "Geçti" yalnız hepsi sağlanınca
17-080 — KARAR — VAR — TASARIM 5.4 (sonuçlar %0,1 / %0,3 / %0,5 ile gösterilir)
17-081 — KARAR — VAR — TASARIM 5.8 (ileri yürüme yıllık sonuçlar ayrı yazılır), 5.4
17-082 — KARAR — RED — aşırı kurulum: TASARIM 5.10 pozitif hücre oranı yeter
17-083 — YANLIŞ — VAR — TASARIM 7.1 ve sonuc C-3 (`nabiz.py` silinir), B-19 (piyasa durumu = XU100 > SMA50), TASARIM 1 P1 (emir dili yok)
17-084 — KARAR — YENİ — TASARIM 4 `rapor`: tek biçim yardımcısı: yüzde elle virgüllü (`locale` yok), TL raporda nokta binlik, CSV'de binliksiz, tarih ISO YYYY-MM-DD
17-085 — KARAR — TEKRAR — 17-084
17-086 — KARAR — TEKRAR — 17-084
17-087 — KARAR — YENİ — TASARIM 6.4: raporda başlık altında sabit uyarı "Tansu'dan esinlenen yorum"; CSV'de `Kaynak` sütunu (17-041)
17-088 — KARAR — VAR — TASARIM 6.7 (durum.txt Türkçe eylem cümlesi), sonuc C-7 (`gunluk/*.log`), TASARIM 5.13 (kapı geçmezse kart yok)
17-089 — KARAR — VAR — TASARIM 6.7, TASARIM 3 (Telegram yok)
17-090 — KARAR — VAR — TASARIM 6.1, sonuc C-7
17-091 — KARAR — VAR — TASARIM 4 `__main__` (`gunluk` / `sinama`)
17-092 — KARAR — RED — kapsam dışı: iç uygulama ayrıntısı, AGENTS.md "testler yalnız TASARIM yüzlerinden"
17-093 — KARAR — YENİ — sonuc C-9 test listesine `rapor` eklenir: sahte sonuçtan rapor ve CSV üret; sütun listesi, ilk satır cümlesi, sabit durum listesi, yasaklı kelime (AL, SAT, ÖNERİ, "Tansu'nun sistemi") denetle
17-094 — YANLIŞ — VAR — TASARIM 7.1 (ön deneme kodu silinir), sonuc C-10 (`git rm --cached`), TASARIM giriş notu (ön deneme kanıt değil); temizlik adımı yapıldı
17-095 — KARAR — VAR — TASARIM 5.11 (deneme günlüğü her koşuyu yazar; karşılaştırma iki satırdır)
17-096 — KARAR — TEKRAR — 17-010 ("Ayrıntı" bölümü: deneme sayısı ve Holm p listesi)
17-097 — KARAR — RED — kapsam dışı: tasarım değişikliği değil, tek seferlik elle sınama
17-098 — KARAR — RED — GLOSSARY.md ve 17-012 yeter; ikinci sözlük sabiti gereksiz
17-099 — KARAR — RED — gereksiz: TASARIM 6.7 durum.txt zaten tek bakılacak yer
17-100 — KARAR — RED — SQLite durum deposu C-4/C-5 ile çelişir; HTML + CSV kısmı zaten C-1 ve TASARIM 3'te

## Özet

Sayımlar (grep ile, madde satırları):
- VAR: 37
- TEKRAR: 11
- YENİ: 16
- RED: 20
- Toplam madde satırı: 84

YENİ maddeler ve önerilen değişiklik:
- 17-006: TASARIM 4 `rapor`: dosya adı `rapor/rapor-YYYYMMDD-HHMM.html`, üstüne yazılmaz.
- 17-007: TASARIM 4 `rapor`: başlık bloğunda koşu kimliği, veri anlık görüntü tarihi, kod hash'i.
- 17-008: TASARIM 1: rapor ilk satırı sabit cümle "Hiçbir aile kabul ölçütünü geçmedi (0/2)".
- 17-010: TASARIM 6.5: %95 aralık sıfırı içeriyorsa "ayırt edilemiyor"; p, Holm p, deneme sayısı "Ayrıntı" bölümünde.
- 17-040: AGENTS.md: yollar `pathlib`, dosyalar açıkça `encoding="utf-8"` (CSV `utf-8-sig`).
- 17-041: TASARIM 6.5: sabit CSV sütunları (Tarih; Hisse; Aile; Durum; Referans; Stop; Pozisyon %; Adet; Fiili risk; Kanıt; Kaynak).
- 17-048: TASARIM 6.7: CSV `os.replace` ile yazılır; `PermissionError` olursa durum.txt SORUNLU "CSV açık".
- 17-049: TASARIM 6.4: kart CSV'si `rapor/kartlar-YYYYMMDD.csv`, her gün yeni dosya.
- 17-050: TASARIM 6.4: sinyal yoksa yalnız başlık satırlı CSV.
- 17-056: TASARIM 6.5: durum listesi AKTİF / STOP / BOZULDU; TASARIM 2'ye not.
- 17-074: TASARIM 4 `rapor`: `rapor/islemler-<koşu>.csv` işlem listesi.
- 17-077: TASARIM 4 `rapor`: tek "Uyarılar" bölümü, boşsa "Uyarı yok".
- 17-079: TASARIM 5.12: raporda aile başına 6 ölçüt geçti/kaldı tablosu.
- 17-084: TASARIM 4 `rapor`: tek biçim yardımcısı (virgüllü yüzde, TL binlik, ISO tarih).
- 17-087: TASARIM 6.4: raporda sabit "Tansu'dan esinlenen yorum" uyarısı; CSV `Kaynak` sütunu.
- 17-093: sonuc C-9: `rapor` için tek test (sütunlar, ilk satır, yasaklı kelime).

YANLIŞ maddeler VAR olmayanlar: yok. Sekiz YANLIŞ maddenin hepsi VAR (17-001, 17-003, 17-036, 17-038, 17-054, 17-073, 17-083, 17-094). Dayanakları yukarıdaki satırlarda.
