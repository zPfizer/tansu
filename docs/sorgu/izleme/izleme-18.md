# İzleme 18: cevaplar-18-adaptor.md (TASARIM taslak 6 karşılaştırması)

Kapsam: yalnız EKSİK, KARAR, YANLIŞ hükümleri. Dosyada EKSİK yok. CEVAPLI, OLGU ve ZAYIF SORU maddeleri alınmadı.

18-001 — KARAR — VAR — TASARIM 4 (`kaynak` ağa çıkan tek yer, `veri` anlık görüntü), sonuc C-3
18-002 — KARAR — VAR — sonuc C-8 (requests), pyproject.toml
18-003 — KARAR — VAR — pyproject.toml ve sonuc C-2 (isyatirimhisse yok, yeni bağımlılık yok); TASARIM 4 kaynak
18-005 — KARAR — VAR — sonuc C-2, pyproject.toml (`==` sürümleri, borsapy==0.11.0)
18-007 — YANLIŞ — RED — kod yapısı ayrıntısı; kaynaklar TASARIM 4'te ayrı sayılı, dondurma anlık görüntüyle olur (C-4)
18-008 — KARAR — RED — aşırı kurulum; kişisel kullanım, dağıtım yok, kullanım koşulu zaten TASARIM 8.1'de açık soru
18-009 — KARAR — YENİ — TASARIM 5.1 "İkinci kaynak" maddesine ekle: borsapy alınamazsa kontrol "yapılmadı" yazılır, kart durmaz
18-011 — KARAR — VAR — sonuc C-8 (istekler arası 1 sn, 429 için yeniden deneme), TASARIM 4 (az sayıda istek)
18-012 — KARAR — VAR — sonuc C-8 (1 sn)
18-013 — KARAR — TEKRAR — 18-012
18-014 — KARAR — VAR — sonuc C-8 (ağ/429/5xx için 3 deneme)
18-015 — KARAR — VAR — sonuc C-7 ve TASARIM 5.13 (5'ten fazla hisse inmezse SORUNLU)
18-016 — KARAR — VAR — sonuc C-8 (zaman aşımı 5, 30); 20 dk koşu sınırı alınmaz, C-7 4 saatlik yeniden deneme yeter
18-017 — KARAR — RED — aşırı kurulum; requests varsayılan başlığı çalıştı
18-018 — KARAR — VAR — sonuc C-8 (şema `assert`), TASARIM 5.13 satır şartları
18-019 — KARAR — RED — kapsam dışı; kod ayrıntısı, tasarım kararı değil
18-020 — KARAR — VAR — sonuc C-7 (saat Europe/Istanbul), pyproject.toml (tzdata)
18-023 — KARAR — VAR — sonuc O1 ve TASARIM 5.1 (HACIM TL'dir; birim zaten çözüldü)
18-024 — KARAR — VAR — TASARIM 4 (takvim fiyat günlerinden çıkar)
18-025 — KARAR — VAR — sonuc C-8 (şema assert), TASARIM 5.13 (satır şartları)
18-026 — KARAR — TEKRAR — 18-025
18-027 — KARAR — VAR — TASARIM 5.1 (olay denetimi HGDG ile ham seri karşılaştırması, karantina)
18-028 — KARAR — VAR — TASARIM 5.13 ve 6 madde 2 (kapı geçmezse kart üretilmez), 6 madde 7 (SORUNLU / VERİ YOK)
18-029 — KARAR — VAR — TASARIM 5.1 (olay denetimi, karantina)
18-030 — KARAR — RED — aşırı kurulum; anlık görüntü değişmez (TASARIM 4), iki görüntü karşılaştırması gerekmez
18-031 — KARAR — VAR — sonuc C-4 (parquet + manifest), TASARIM 4 (olay tablosu bütün kodlarıyla)
18-032 — KARAR — VAR — pyproject.toml (pyarrow==25.0.1, requires-python sabit), sonuc C-4, C-10 (yedek yok)
18-033 — KARAR — VAR — sonuc C-4 (`veri/ag/<YYYYMMDD-HHMM>/`)
18-034 — KARAR — VAR — sonuc C-4 ve TASARIM 6 madde 2 (geçici klasör, `os.replace`)
18-035 — YANLIŞ — VAR — sonuc C-4 (her akşam tam indirme, yeni klasör); `veri.py` prototipi silindi (TASARIM 7 adım 1)
18-036 — KARAR — RED — 19:30 koşusu seans sonrası; TASARIM 5.1 "bugünkü veri" kuralı yeter, yayın saati 8.1'de açık soru
18-037 — KARAR — VAR — TASARIM 5.13 ve sonuc C-7 (100 hisseden 5'ten fazlası inmezse SORUNLU; azı koşuyu durdurmaz)
18-038 — KARAR — RED — kapsam dışı; bulunamayan semboller TASARIM 5.2'de raporlanır, eşleme dosyası gerekmez
18-039 — KARAR — VAR — TASARIM 5.2 (işlemi kapanan hisseler, bulunamayanlar raporda), 8 madde 4
18-040 — KARAR — VAR — TASARIM 4 (olaylar bütün kodlarıyla)
18-042 — KARAR — RED — C-4 ile çelişir (her akşam tam indirme)
18-043 — KARAR — VAR — TASARIM 5.1 (HGDG geçerli kalır, ikinci kaynak farkı yalnız listelenir)
18-044 — KARAR — YENİ — TASARIM 5.1 "İkinci kaynak" maddesine ekle: yalnız iki kaynakta ortak günler karşılaştırılır, tek kaynaklı gün sayısı raporlanır
18-045 — KARAR — VAR — pyproject.toml (KAP paketi yok), TASARIM 7 adım 10 (KAP paralel iş)
18-048 — KARAR — RED — kapsam dışı; gerçek BIST100 paralel iştir (TASARIM 7 adım 10), ilk sürüm evreni 5.2 kuralıyla
18-049 — KARAR — RED — kapsam dışı; KAP paralel iş (TASARIM 7 adım 10)
18-047 — YANLIŞ — RED — kapsam dışı; KAP evren doğrulaması paralel iş (TASARIM 7 adım 10), ilk sürüm 5.2 kuralını kullanır
18-050 — YANLIŞ — RED — kapsam dışı; KAP/gerçek BIST100 ilk sürümde yok (TASARIM 5.2 son madde, 7 adım 10)
18-051 — KARAR — VAR — TASARIM 5.2 (evren kuralı bütün dönemde piyasa değerine göre; bugünkü liste kullanılmaz)
18-052 — KARAR — RED — EVDS çıktı (sonuc B-8, C-2)
18-053 — KARAR — RED — EVDS anahtarı yok (sonuc B-8); gizli bilgi kalmadı
18-054 — KARAR — RED — EVDS anahtarı yok (sonuc B-8); gizli bilgi kalmadı
18-055 — KARAR — VAR — sonuc B-8 ve TASARIM 4 (faiz = borsapy politika faizi)
18-056 — YANLIŞ — VAR — sonuc B-8, TASARIM 4 ve 5.6 (yalnız politika faizi; EVDS/TLREF yok)
18-057 — KARAR — VAR — sonuc B-8, TASARIM 4 (borsapy politika faizi tek seri)
18-059 — KARAR — VAR — sonuc B-8 (ileri doldurma, bir gün gecikmeli), TASARIM 5.6 faiz satırı
18-060 — YANLIŞ — RED — Yahoo çıktı (sonuc B-2, C-2); sadakat ham İş Yatırım serisiyle yapılır (KURALLAR 4)
18-061 — KARAR — RED — Yahoo çıktı (sonuc B-2)
18-062 — KARAR — RED — Yahoo çıktı (sonuc B-2)
18-063 — KARAR — RED — Yahoo çıktı (sonuc B-2)
18-064 — YANLIŞ — VAR — sonuc C-3 (Yahoo kodu silinir), TASARIM 5.1 / Ek A B1 (eşikli düzeltme yok); Yahoo sadakat önerisi RED (B-2)
18-065 — KARAR — VAR — sonuc C-9 (elle hesap, ağ conftest ile kapalı)
18-067 — KARAR — TEKRAR — 18-025
18-068 — KARAR — RED — aşırı kurulum; sonuc C-9 ağı kapatır, günlük koşunun kapıları zaten ölçer (TASARIM 5.13, 6)
18-069 — KARAR — RED — aşırı kurulum; C-9 test yüzleri `kaynak`'ı saymaz, ağ testi yok
18-070 — KARAR — TEKRAR — 18-069
18-071 — KARAR — YENİ — TASARIM 6 madde 2'ye ekle: kaynak erişilemezse dondurulmuş anlık görüntülerle sınama sürer, yalnız canlı kart durur
18-072 — KARAR — TEKRAR — 18-071
18-073 — KARAR — VAR — TASARIM 5.11 ve sonuc C-6 (deneme günlüğü veri anlık görüntüsünü yazar)
18-074 — KARAR — VAR — TASARIM 4 (`kaynak`: sembol, tarih aralığı → ham tablo; sınıf yok, düz paket)
18-075 — KARAR — YENİ — TASARIM 4 `kaynak` satırına ekle: ham `HG_*` adları `kaynak` içinde tek sözlükle proje adlarına çevrilir; sütun adı dili GLOSSARY "Fiyat" ile tek seçilir
18-076 — KARAR — VAR — TASARIM 6 madde 4 (UTF-8 BOM CSV); hisse kodları ASCII
18-077 — KARAR — TEKRAR — 18-076
18-078 — KARAR — VAR — TASARIM 6 madde 1 ve sonuc C-7 (kaçırılan koşu çalışır)
18-079 — KARAR — RED — aşırı kurulum; truststore kurulu değil (pyproject.toml), yeni bağımlılık yok kararı
18-080 — KARAR — RED — aşırı kurulum; borsapy başarısızlığı 18-009 ile atlanır
18-081 — KARAR — VAR — TASARIM 6 madde 7 (`VERİ YOK` + Türkçe eylem cümlesi)
18-082 — KARAR — RED — aşırı kurulum; sonuc C-8 (3 deneme, şema assert) yeter
18-083 — KARAR — VAR — sonuc C-7 (stdlib logging, günlük dosyası `gunluk/YYYY-MM-DD.log`)
18-084 — KARAR — RED — aşırı kurulum; C-7 günlük dosyası yeter
18-085 — KARAR — VAR — sonuc C-4 (anlık görüntü deposu, ayrı HTTP önbelleği yok)
18-087 — KARAR — VAR — sonuc C-4 (her akşam tam indirme), C-8 (1 sn aralık, sıralı)
18-088 — KARAR — RED — C-4 ile çelişir (tam indirme, yarım klasör atılır); kısmi sürdürme aşırı
18-089 — KARAR — VAR — pyproject.toml (`requires-python`, `dependencies`), sonuc C-2 (uv yok)
18-090 — KARAR — VAR — sonuc C-2 (`requirements.lock.txt`), temizlik adımı yapıldı
18-091 — KARAR — RED — aşırı kurulum; 20 MB sınırı gerekmez
18-092 — KARAR — TEKRAR — 18-090
18-093 — KARAR — YENİ — TASARIM 7 adım 2'ye ekle: ilk indirmeden önce İş Yatırım ve borsapy kullanım koşulları okunur (8.1)
18-094 — KARAR — TEKRAR — 18-008
18-095 — KARAR — VAR — TASARIM 5.13 ve 5.1 "bugünkü veri" (şema ve tazelik kapıları)
18-096 — KARAR — VAR — TASARIM 5.1 (hacmi sıfır gün işlem günü değil), 5.13 (satır şartları, bozuk satır karantina)
18-097 — YANLIŞ — VAR — TASARIM 4 (`kaynak` ham tablo döner, `veri` anlık görüntü yazar), sonuc C-3
18-098 — KARAR — TEKRAR — 18-036
18-099 — KARAR — RED — kapsam dışı; süreç kararı, AGENTS.md zaten ajan çalışmasını tanımlar
18-100 — KARAR — TEKRAR — 18-071

## Özet

Sayımlar (grep, satır başı "18-"):
- VAR: 47
- TEKRAR: 10
- YENİ: 5
- RED: 28
- Toplam: 90 (82 KARAR + 8 YANLIŞ; EKSİK yok)

YENİ maddeler ve önerilen değişiklik:
- 18-009: TASARIM 5.1 "İkinci kaynak": borsapy alınamazsa kontrol "yapılmadı" yazılır, kart durmaz.
- 18-044: TASARIM 5.1 "İkinci kaynak": yalnız iki kaynakta ortak günler karşılaştırılır; tek kaynaklı gün sayısı raporlanır.
- 18-071 (18-072 ve 18-100 tekrarı): TASARIM 6 madde 2: kaynak erişilemezse dondurulmuş anlık görüntülerle sınama sürer, yalnız canlı kart durur.
- 18-075: TASARIM 4 `kaynak`: ham `HG_*` adları tek sözlükle proje adlarına çevrilir; sütun adı dili tek seçilir (GLOSSARY "Fiyat").
- 18-093: TASARIM 7 adım 2: ilk indirmeden önce iki sitenin kullanım koşulları okunur.

YANLIŞ maddeler, VAR olmayanlar:
- 18-007: RED, kod yapısı ayrıntısı; kaynaklar TASARIM 4'te ayrı, dondurma C-4 ile olur.
- 18-047: RED, KAP evren doğrulaması paralel iş (TASARIM 7 adım 10).
- 18-050: RED, KAP evren CSV'si ilk sürümde yok (TASARIM 5.2, 7 adım 10).
- 18-060: RED, Yahoo çıktı (sonuc B-2, C-2).

YANLIŞ maddeler, VAR: 18-035, 18-056, 18-064, 18-097.
