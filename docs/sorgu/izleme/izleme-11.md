# İzleme 11: cevaplar-11-moduller.md, taslak 6'ya karşı

Kapsam: EKSİK, KARAR, YANLIŞ hükümlü 96 madde. CEVAPLI (11-012, 11-070), OLGU (11-049) ve ZAYIF SORU (11-064) alınmadı.

11-001 — KARAR — VAR — TASARIM 4 (düz paket, takvim ve maliyet modül değil), sonuc C-3
11-002 — YANLIŞ — VAR — TASARIM 4 ("Takvim, fiyat günlerinden çıkar"), TASARIM 5.1 Bugünkü veri
11-003 — YANLIŞ — VAR — TASARIM 4 ("Maliyet tek bir sabittir"), TASARIM 5.4
11-004 — YANLIŞ — VAR — TASARIM 4: taslak 6'da "takılıp çıkarılabilir" notu yok; maliyet tek sabit
11-005 — KARAR — RED — `duzelt(ham, olaylar)` B-2 ve TASARIM 5.1 ile çelişir (HGDG kaynaktan gelir, olay çarpanı yalnız denetim); olay tablosunun veri'de durması zaten TASARIM 4
11-006 — KARAR — VAR — TASARIM 4 (evren), TASARIM 5.2 (KAP'lı gerçek BIST100 sonra)
11-007 — YANLIŞ — VAR — TASARIM 4 gostergeler satırı (piyasa durumu burada), sonuc C-3
11-008 — YANLIŞ — VAR — TASARIM 4 (aileler = tek hisse aileleri; cift = kendi döngüsü)
11-009 — KARAR — VAR — TASARIM 4 (motor Adım, cift kendi döngüsü), TASARIM 5.6
11-010 — KARAR — YENİ — TASARIM 4 motor satırı: "mum = ön hesaplı atr/sma250 sütunlu bir gün satırı; göstergeler vektörel hesaplanır, sınamada ve canlıda aynı kod"
11-011 — KARAR — VAR — TASARIM 4 (Adım pozisyon günceller, Motor sinyalden işlem üretir), TASARIM 5.3, TASARIM 6.6
11-013 — KARAR — TEKRAR — 11-010 (mum düz satır)
11-014 — KARAR — RED — erken optimizasyon, hız ölçülmedi; numba C-11 ile çelişir (numba yok, önce algoritma, sonra joblib)
11-015 — KARAR — VAR — TASARIM 5.7 K1 (rastgele işlem tam çıkış paketini uygular), TASARIM 7 adım 8
11-016 — KARAR — VAR — TASARIM 4 simulator, TASARIM 5.4 (likidite M11), TASARIM 5.6 (tavan, 10 pozisyon, M12)
11-017 — KARAR — RED — kapsam dışı: işlem tablosu sütunları kod docstring'inde tanımlanır, tasarıma girmez
11-018 — KARAR — VAR — TASARIM 4 simulator, TASARIM 5.6 (iki bölme), faiz
11-019 — KARAR — VAR — TASARIM 4 istatistik (statsmodels yalnız coint ve Holm), TASARIM 5.9 (blok bootstrap kendi kodumuz)
11-020 — KARAR — VAR — TASARIM 4 kayit, TASARIM 5.11, sonuc C-6
11-021 — KARAR — VAR — TASARIM 4 kayit, sonuc C-6
11-022 — KARAR — RED — tek modül TASARIM 4'te zaten var; iki CSV C-5/C-6 ile çelişir (deneme.jsonl, kartlar.jsonl)
11-023 — YANLIŞ — YENİ — KURALLAR §4 Kural: "sadakat sonucu `docs/sadakat.md`'ye yazılır; ayrı kalıcı sadakat dosyası yok, aile kodu aileler.py'de" (sonuç kaydı yeri belgede yok)
11-024 — KARAR — VAR — TASARIM 5.1 Karantina, TASARIM 4 veri (veri kapıları)
11-025 — KARAR — VAR — TASARIM 5.1 İkinci kaynak ve Bugünkü veri, TASARIM 6.2, sonuc C-4 (her akşam yeni anlık görüntü)
11-026 — KARAR — RED — markdown çıktı TASARIM 4 ve C-1 ile çelişir (tek HTML + CSV + durum.txt)
11-027 — KARAR — RED — kartlar.csv C-5 ile çelişir (`kayit/kartlar.jsonl`, yalnız ekleme; açık kart her gün yeniden hesaplanır)
11-028 — YANLIŞ — VAR — TASARIM 3 ("Yok": Streamlit), sonuc C-1, C-2
11-029 — YANLIŞ — TEKRAR — 11-028
11-030 — KARAR — VAR — TASARIM 4 ("Paket düzdür"), sonuc C-3
11-031 — KARAR — VAR — TASARIM 7 adım 1, sonuc C-3 (kanit.py, nabiz.py silinir; temizlik yapıldı)
11-032 — KARAR — VAR — TASARIM 7 adım 1, KURALLAR §1 madde 4, sonuc B-2, C-3
11-033 — KARAR — VAR — TASARIM 4 gostergeler satırı
11-034 — KARAR — RED — pandas-ta-classic C-2 ile çelişir; TASARIM 4 "Kütüphane yok", ATR Wilder kendi kodumuz
11-035 — KARAR — TEKRAR — 11-010
11-036 — KARAR — TEKRAR — 11-035
11-037 — KARAR — VAR — sonuc C-9 ("veriyi kes, geçmiş değişmesin" testi)
11-038 — KARAR — VAR — TASARIM 4 (aileler → sinyal günleri, motor sinyalleri alır)
11-039 — KARAR — YENİ — TASARIM 4 altına tek satır: "Bağımlılık yönü kaynak → veri → evren, gostergeler → aileler, cift → motor → simulator → istatistik → kayit → rapor → __main__; geri import yok"
11-040 — KARAR — VAR — TASARIM 4 kaynak ("Ağa çıkan tek yer"); not: "disk yazma yalnız kayit ve rapor" kısmı geçersiz, veri anlık görüntü yazar (C-4)
11-041 — KARAR — VAR — TASARIM 4 kaynak, sonuc C-3, C-8
11-042 — YANLIŞ — TEKRAR — 11-041 (kaynaklar fonksiyon, ortak sınıf yok)
11-043 — KARAR — VAR — sonuc C-8 (şema `assert`), TASARIM 5.13
11-044 — KARAR — YENİ — TASARIM 4 veri satırı: "borsapy tabloları (faiz, sektör, endeks günleri) anlık görüntüye yazılır; koşu canlı borsapy'a bağlı kalmaz"
11-045 — KARAR — VAR — TASARIM 4 (kaynak tek ağ noktası; statsmodels yalnız coint ve Holm), sonuc C-2 (pandas-ta-classic, yfinance çıktı)
11-046 — KARAR — VAR — TASARIM 4 ("Ölçütler kısa kendi kodumuz"), sonuc C-2 (quantstats çıktı); ATR "kütüphane çağrısı" kısmı geçersiz
11-047 — YANLIŞ — VAR — pyproject.toml `[project] dependencies` (== sabit, dev = pytest), sonuc C-2
11-048 — KARAR — VAR — pyproject.toml (`pythonpath`, ad, `requires-python`, bağımlılıklar), TASARIM 4 `__main__`
11-050 — KARAR — VAR — sonuc C-2 (`==` sabit, `requirements.lock.txt`, uv yok), pyproject.toml
11-051 — KARAR — YENİ — AGENTS.md çalışma kuralları: "Kod, dosya, sütun ve CSV başlığı adları Türkçe ASCII (aile, adim, evren, bolme, kart); rapor ve kart metni Türkçe karakterli"
11-052 — KARAR — TEKRAR — 11-051
11-053 — KARAR — RED — aşırı kurulum: GLOSSARY ad eşlemesi, kontrol aracı yok; 11-051 yeter
11-054 — KARAR — RED — kapsam dışı: kod adı ayrıntısı, kodda karar verilir
11-055 — KARAR — RED — kapsam dışı: kod adı ayrıntısı, kodda karar verilir
11-056 — KARAR — RED — TASARIM 6.4/6.5 kart içeriğiyle çelişir (referans fiyat, fiili risk, hedef yok; kart günlüğü C-5 jsonl)
11-057 — KARAR — VAR — TASARIM 4 ve sonuc C-3 (modül listesinde tipler yok)
11-058 — KARAR — RED — kapsam dışı: sütun adı eşlemesi kodda tanımlanır (11-051 kuralı yeter)
11-059 — KARAR — VAR — TASARIM 5.1 Seriler (gösterge ve getiri HGDG'den, limit/kilit/likidite ham HG'den)
11-060 — KARAR — VAR — sonuc C-4 (parquet, veritabanı yok); yol C-4'teki `veri/ag/<YYYYMMDD-HHMM>/` olur
11-061 — KARAR — YENİ — sonuc C-4'e: "günlük anlık görüntüler 30 gün sonra silinir; deneme günlüğünde adı geçen anlık görüntü hiç silinmez" (boyut ölçülmedi)
11-062 — KARAR — TEKRAR — 11-022
11-063 — KARAR — VAR — sonuc C-6 (kod parmak izi, `ast.dump` sha256 + parametre sha256), TASARIM 5.8
11-065 — KARAR — RED — yedek yok kararı (AGENTS.md); `rapor/` git'e girmez (C-10)
11-066 — KARAR — VAR — sonuc C-6 (parametre = kodda donmuş dataclass), TASARIM 4 (maliyet sabit)
11-067 — KARAR — VAR — sonuc C-6 (parametre aile kodunda, hash kodu kapsar)
11-068 — KARAR — VAR — sonuc C-6 (donmuş dataclass), TASARIM 5.10 (ızgara)
11-069 — KARAR — VAR — sonuc C-6, TASARIM 4 (aileler tek hisse; cift ayrı)
11-071 — KARAR — RED — kapsam dışı: yeni aile maliyet tahmini, tasarım değişikliği yok
11-072 — KARAR — VAR — TASARIM 4 (aileler + cift ayrı); AB=CD ilk sürümde yok (B-1, TASARIM 3), uygulanmaz
11-073 — KARAR — VAR — TASARIM 4 cift, TASARIM 5.6 Çift seçimi
11-074 — KARAR — RED — kapsam dışı: zigzag/pivot yalnız AB=CD için, o ikinci dalga (B-1)
11-075 — KARAR — RED — B-2 ve C-2: Yahoo hiç kullanılmaz, yfinance çıktı
11-076 — KARAR — RED — B-2 ve C-2: Yahoo hiç kullanılmaz, yfinance çıktı
11-077 — KARAR — RED — B-19 ve TASARIM 6.3 ile çelişir (XU100 kapanış > SMA50; SMA200 yok)
11-078 — YANLIŞ — YENİ — TASARIM 3: "(yalnız raporlama)" → "(motoru ve girişi etkilemez; K1(b) örneklemesinde ve rapor bölmesinde kullanılır)"
11-079 — KARAR — RED — aşırı kurulum: evren anlık görüntüden belirleyici türetilir (TASARIM 5.2), ayrı tablo gerekmez
11-080 — KARAR — RED — TASARIM 5.2 ve B-9 ile çelişir (kapanan hissede −%100, nedeni bilinirse son fiyat)
11-081 — KARAR — RED — kapsam dışı: kod/süreç ayrımı ayrıntısı; TASARIM 5.12 ölçütleri zaten yazılı
11-082 — KARAR — YENİ — TASARIM 5.12 sonuna: "Canlı etiketini Levent kayit'a yalnız-ekleme satırı olarak yazar; kod yalnız ölçütü hesaplar" (canlı bayrağı yeri belgede yok)
11-083 — KARAR — VAR — TASARIM 4 rapor ("Şablon motoru yok"), sonuc C-1 (f-string)
11-084 — YANLIŞ — VAR — sonuc C-2 (quantstats çıktı), TASARIM 4 ("Ölçütler kısa kendi kodumuz"); taslak 6'da quantstats geçmiyor; "yalnız markdown" kısmı geçersiz (HTML, C-1)
11-085 — KARAR — VAR — TASARIM 4 `__main__` (`gunluk` / `sinama`)
11-086 — KARAR — YENİ — TASARIM 6.1: "`gunluk` hata ya da kapı başarısızlığında çıkış kodu ≠ 0 verir (Görev Zamanlayıcı yeniden denemesi bunu ister) ve durum.txt ilk satırı SORUNLU olur"
11-087 — KARAR — VAR — TASARIM 4 motor ("sınama ve canlı günlük aynı Adım"), TASARIM 6.6
11-088 — KARAR — TEKRAR — 11-027
11-089 — KARAR — TEKRAR — 11-086
11-090 — KARAR — RED — C-7 ile çelişir (`gunluk/YYYY-MM-DD.log`, stdlib logging)
11-091 — KARAR — VAR — TASARIM 7 adım 1 (kanit/nabiz testleri silinir; temizlik yapıldı), TASARIM 5.3
11-092 — KARAR — VAR — TASARIM 5.3 Motor sınamaları (9 senaryo)
11-093 — KARAR — VAR — sonuc C-9 (ağ conftest ile kapalı)
11-094 — KARAR — VAR — pyproject.toml (dev yalnız pytest), AGENTS.md test kapısı, sonuc C-9
11-095 — KARAR — YENİ — AGENTS.md "Domain docs" satırı: "kararlar `docs/adr/`" → "kararlar `docs/TASARIM.md`'de"
11-096 — KARAR — VAR — AGENTS.md ("belgeyi önce düzelt, sonra kodu yaz"), TASARIM başı
11-097 — KARAR — RED — TASARIM 7 sırası geçerli (evren 4. adımda); ayrı ilk-dilim planı ek kurulum
11-098 — KARAR — TEKRAR — 11-097
11-099 — KARAR — RED — aşırı kurulum: `__all__` ve ad sınırı denetimsiz niyet beyanı
11-100 — KARAR — RED — aşırı kurulum: TASARIM 4 zaten modül haritası; AGENTS.md okuma sırası yeter, `test_harita.py` gereksiz

## Özet

Sayımlar (grep ile, 96 madde): VAR 51, TEKRAR 10, YENİ 10, RED 25.

YENİ maddeler:
1. 11-010 — TASARIM 4 motor satırı: mum = ön hesaplı atr/sma250 sütunlu gün satırı; göstergeler sınamada ve canlıda aynı vektörel kod.
2. 11-023 — KURALLAR §4: sadakat sonucu `docs/sadakat.md`'ye yazılır; ayrı kalıcı sadakat dosyası yok.
3. 11-039 — TASARIM 4: tek yönlü import sırası, geri import yok.
4. 11-044 — TASARIM 4 veri: borsapy tabloları (faiz, sektör, endeks günleri) anlık görüntüye yazılır.
5. 11-051 — AGENTS.md: kod, dosya, sütun, CSV başlığı adları Türkçe ASCII; metin Türkçe karakterli.
6. 11-061 — C-4: günlük anlık görüntüler 30 gün sonra silinir; deneme günlüğünde geçenler silinmez.
7. 11-078 — TASARIM 3: "(yalnız raporlama)" ifadesi K1(b) kullanımını kapsayacak biçimde düzeltilir.
8. 11-082 — TASARIM 5.12: Canlı etiketini Levent kayit'a ekleme satırı olarak yazar.
9. 11-086 — TASARIM 6.1: `gunluk` hatada çıkış kodu ≠ 0, durum.txt SORUNLU.
10. 11-095 — AGENTS.md "Domain docs": "kararlar docs/adr/" → "kararlar docs/TASARIM.md'de".

YANLIŞ maddelerden VAR olmayanlar (12 YANLIŞ içinde):
- 11-023 — YENİ: sadakat sonucu `docs/sadakat.md`'ye yazılır (yukarıda, madde 2).
- 11-078 — YENİ: TASARIM 3 "yalnız raporlama" düzeltmesi (yukarıda, madde 7).
- 11-029 — TEKRAR 11-028 (11-028 VAR: TASARIM 3, C-1, C-2).
- 11-042 — TEKRAR 11-041 (11-041 VAR: TASARIM 4 kaynak, C-8).
- Diğer 8 YANLIŞ (002, 003, 004, 007, 008, 028, 047, 084) VAR.
