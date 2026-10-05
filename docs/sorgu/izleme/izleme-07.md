# İzleme 07: cevaplar-07-risk.md, taslak 6'ya karşı

Kapsam: hüküm EKSİK (70) ve YANLIŞ (3) olan maddeler. KARAR hükmü bu dosyada yok. Tasarım belgeleri değiştirilmedi.

07-002 — EKSİK — VAR — TASARIM 5.6 ve sonuc B-12 (rapor tavanın bağladığı işlem oranını ve fiili riski yazar)
07-003 — EKSİK — VAR — TASARIM 5.6 (özkaynak = nakit + pozisyonların kapanış değeri), sonuc B-12
07-004 — EKSİK — RED — aşırı kurulum: sermaye ölçekleme gereksiz, 5.4 %2 likidite sınırı zaten var
07-005 — EKSİK — VAR — TASARIM 5.6 (adet aşağı yuvarlanır), sonuc B-12; test listesi kısmı 07-085'te
07-007 — EKSİK — RED — kapsam dışı: masraf R paydasına girmez, 5.4 %0,1/0,3/0,5 senaryoları yeter
07-008 — EKSİK — RED — aşırı kurulum: tick yuvarlama BIST100 evreninde 2 ATR yanında ihmal edilir
07-009 — EKSİK — YENİ — TASARIM 5.6 "en likit önce" satırına "(5.4'teki 10 günlük medyan TL)" yazılır
07-010 — EKSİK — RED — aşırı kurulum: toplam risk sınırı Tansu'da yok; 5.6 en çok 10 pozisyon zaten sınırlar
07-012 — EKSİK — VAR — TASARIM 5.6 ("YORUM, bizim", tavan uyarısı), sonuc B-12; tavansız varyant ayrıca RED (aşırı)
07-014 — EKSİK — VAR — TASARIM 5.6 (özkaynak = nakit + pozisyonların kapanış değeri)
07-015 — EKSİK — RED — aşırı kurulum: kart zaten sermaye yüzdesi verir (6.5); tek kullanıcı, sabit 1.000.000 TL
07-016 — EKSİK — VAR — TASARIM 5.5 ("uzunluk 14, Wilder ortalaması (YORUM)"); ızgaraya ATR uzunluğu eklemek RED (deneme sayısını şişirir)
07-017 — EKSİK — YENİ — TASARIM 5.1 "Seriler"e: giriş, ATR, stop ve düşük karşılaştırması aynı seriden (HGDG anlık görüntü) alınır
07-018 — EKSİK — TEKRAR — 07-017
07-019 — EKSİK — VAR — TASARIM 6.2 ve 6.6 (her gün anlık görüntüden Adım ile yeniden hesap), 5.1 (Yahoo yok, tek anlık görüntü)
07-024 — YANLIŞ — VAR — TASARIM 5.3 "Stop dolumu min(stop, AOF)", sonuc B-4
07-025 — EKSİK — VAR — TASARIM 5.3 / sonuc B-4 (min(stop, AOF)); sayı raporu RED (ayrıntı)
07-026 — EKSİK — VAR — TASARIM 5.4 (kayma dahil %0,3; kabul %0,5'te de geçmeli) ve 5.3 min(stop, AOF)
07-027 — EKSİK — VAR — TASARIM 5.3 (stop dolumu min(stop, AOF) = stop fiyatı veya daha kötüsü), sonuc B-4
07-028 — EKSİK — VAR — TASARIM 5.1 "Hacim" (hacmi sıfır olan gün işlem günü değildir), sonuc B-7
07-029 — EKSİK — VAR — TASARIM 5.3 "Stop: giriş fiyatından ve sinyal günü ATR'sinden hesaplanır" (sabit)
07-030 — YANLIŞ — VAR — KURALLAR §3 risk paketi satırı ("çift rotasyonu hariç") ve TASARIM 5.5
07-031 — EKSİK — VAR — TASARIM 5.3 "Giriş günü: yalnız stop kontrol edilir", sonuc B-4
07-032 — EKSİK — TEKRAR — 07-031
07-034 — EKSİK — RED — kapsam dışı: K1 aynı AOF girişini kullanır, fark nötrleşir (5.7); ayrı ölçüm gereksiz
07-035 — EKSİK — RED — Yahoo tamamen çıktı (sonuc B-2); tek dolum modeli AOF
07-038 — YANLIŞ — VAR — TASARIM 5.5 "ertesi günün AOF'unda"
07-041 — EKSİK — YENİ — TASARIM 5.7 K1 "Çıkış" satırına: rastgele işlemler aynı AOF girişi ve aynı masrafla işlenir
07-042 — EKSİK — RED — hedef yok (TASARIM 5.5 "Hedef yok")
07-043 — EKSİK — RED — AB=CD ikinci dalgada
07-044 — EKSİK — RED — AB=CD ikinci dalgada (D kenarı)
07-045 — EKSİK — RED — aşırı kurulum: tek dolum modeli AOF, iki uçlu kabul eşiği gereksiz
07-047 — EKSİK — VAR — TASARIM 5.4 ("komisyon, BSMV, kayma birlikte"; "açılışta kovalama" ifadesi yok)
07-049 — EKSİK — RED — B-4 ile kapanır: tek fiyat gününde min(stop, AOF) gerçek fiyatı verir; ayrı kural gereksiz
07-050 — EKSİK — RED — aşırı kurulum: 5.4 %2 medyan hacim sınırı zaten var
07-053 — EKSİK — VAR — TASARIM 5.3 "Kilitli gün" (düşük = yüksek, hacim > 0 ve limit fiyatında), sonuc B-5
07-054 — EKSİK — RED — aşırı kurulum: yaklaşık kilit tanımı ek parametre; 5.3 giriş günü kilidi yeter
07-055 — EKSİK — RED — kapsam dışı: 5.3 yalnız tavanda girişi, tabanda çıkışı kısıtlar; tavanda çıkış zaten serbest
07-056 — EKSİK — VAR — TASARIM 5.3 ("ertesi güne kayar") ve B-4 (dolum min(stop, AOF)); rapor sayısı RED
07-057 — EKSİK — VAR — TASARIM 5.3 / sonuc B-4 (07-024 kuralı)
07-059 — EKSİK — VAR — TASARIM 5.1 "Fiyat limiti" (L tarih dönemleri) ve 5.2 (60 günlük medyan hacim filtresi)
07-060 — EKSİK — YENİ — TASARIM 5.1 "Fiyat limiti"ne: olay gününde baz = ham önceki kapanış × olay çarpanı (kilit ve limit için)
07-061 — EKSİK — VAR — TASARIM 5.3 (kilitli tabanda çıkış kayar, pozisyon açık kalır), 5.6 özkaynak kapanış değeriyle
07-062 — EKSİK — RED — kapsam dışı: çiftte kilitli geçiş nadir; ek kural yok
07-063 — EKSİK — VAR — TASARIM 5.3 "Sinyal günü kapanış SMA250 altındaysa giriş yok", sonuc B-12
07-064 — EKSİK — TEKRAR — 07-063
07-065 — EKSİK — YENİ — TASARIM 5.3 "Sinyal ve giriş"e: SMA250 hesaplanamıyorsa (250 gün yok) giriş yok; K1'de de aynı
07-068 — EKSİK — RED — aşırı kurulum: çıkış nedeni dağılımı rapor süsü; kabul ölçütünü etkilemez
07-069 — EKSİK — RED — aşırı kurulum: tutma süresi 5.9'da blok uzunluğu için zaten hesaplanır; ayrı rapor çıktısı gereksiz
07-070 — EKSİK — RED — AB=CD ikinci dalgada
07-072 — EKSİK — RED — AB=CD ikinci dalgada
07-073 — EKSİK — RED — AB=CD ikinci dalgada
07-074 — EKSİK — RED — AB=CD ikinci dalgada
07-075 — EKSİK — VAR — GLOSSARY "Stop" ve "Bozulma" (Bozulma = SMA250 çıkışı); 3. anlam AB=CD ile gider
07-076 — EKSİK — VAR — TASARIM 5.12 portföy kuralı (düşüş %25 / 12 ay: aile reddedilir)
07-078 — EKSİK — VAR — TASARIM 4 (`motor` Adım tek hisse; `cift` kendi döngüsü)
07-079 — EKSİK — YENİ — TASARIM 5.3 "Yeni sinyal"e: SMA250 çıkışı bildirilmiş ama dolmamış pozisyon "açık" sayılır
07-080 — EKSİK — VAR — TASARIM 5.7 K1 ("sayılar hisse başına eşleştirilir"; aynı kural rastgelede de geçerli, 5.3)
07-081 — EKSİK — RED — aşırı kurulum: K1 aynı atlamayı uygular (nötr); ek rapor satırı gereksiz
07-082 — EKSİK — RED — aşırı kurulum: pozisyon sınırsız duyarlılık koşusu ek deneme yükü
07-083 — EKSİK — TEKRAR — 07-031
07-084 — EKSİK — VAR — TASARIM 5.3 "Kilitli tavanda giriş yok" (iptal; yeni sinyal gerekir)
07-085 — EKSİK — YENİ — TASARIM 5.3 "Motor sınamaları"na ekle: lot yuvarlama, %10 tavan, olay gününde açık pozisyon, ardışık kilit, karantinada açık pozisyon
07-086 — EKSİK — RED — aşırı kurulum: 5.9 medyan ve en iyi %5 atılmış sonuç yeter; R dağılımı süs
07-087 — EKSİK — RED — aşırı kurulum: MFE/MAE ilk sürümde karar girdisi değil
07-089 — EKSİK — TEKRAR — 07-090
07-090 — EKSİK — YENİ — TASARIM 6.5 kart satırı: stop "referans fiyat − 2 ATR, tahmini" etiketli; gerçek stop giriş dolunca Adım'da hesaplanır
07-092 — EKSİK — RED — uygulama ayrıntısı: Adım girdisi kod aşamasında; TASARIM 4 yüzü yeter
07-093 — EKSİK — VAR — TASARIM 5.11 (deneme günlüğünde tohum)
07-095 — EKSİK — VAR — TASARIM 5.12 son bölüm (boru hattı denetimi: sentetik boş veri, yanlış kabul ≤ %5), sonuc B-18
07-097 — EKSİK — VAR — TASARIM 4 modül tablosu (motor Adım + Motor, simulator, kayit)
07-098 — EKSİK — VAR — TASARIM 5.1 "Karantina" (açık pozisyon son temiz AOF'ta kapanır ve sayılır)
07-099 — EKSİK — VAR — TASARIM 5.2 (kapanan hissede −%100 / son fiyat, 60 gün durdurma = kapanma) ve 5.1 Hacim

## Özet

### Sayılar (grep ile sayıldı)
- EKSİK satırı: 70
- YANLIŞ satırı: 3
- VAR: 33
- TEKRAR: 5
- YENİ: 8
- RED: 27

### YENİ maddeler ve önerilen değişiklik
- 07-009: TASARIM 5.6 "en likit önce" satırına "(5.4'teki 10 günlük medyan TL)" yaz.
- 07-017: TASARIM 5.1 "Seriler"e yaz: giriş, ATR, stop ve düşük karşılaştırması aynı seriden (HGDG anlık görüntü).
- 07-041: TASARIM 5.7 K1 "Çıkış"a yaz: rastgele işlemler aynı AOF girişi ve aynı masrafla işlenir.
- 07-060: TASARIM 5.1 "Fiyat limiti"ne yaz: olay gününde baz = ham önceki kapanış × olay çarpanı.
- 07-065: TASARIM 5.3'e yaz: SMA250 hesaplanamıyorsa (250 gün yok) giriş yok; K1'de de aynı.
- 07-079: TASARIM 5.3 "Yeni sinyal"e yaz: SMA250 çıkışı bildirilmiş ama dolmamış pozisyon "açık" sayılır.
- 07-085: TASARIM 5.3 motor sınamalarına ekle: lot yuvarlama, %10 tavan, olay gününde açık pozisyon, ardışık kilit, karantinada açık pozisyon.
- 07-090: TASARIM 6.5 kartta stop "referans fiyat − 2 ATR, tahmini" etiketli olsun; gerçek stop giriş dolunca hesaplanır.

### YANLIŞ olup VAR olmayan madde
- Yok. Üç YANLIŞ maddenin üçü de taslak 6'da kapalı: 07-024 (5.3, B-4), 07-030 (KURALLAR §3 "çift rotasyonu hariç"), 07-038 (5.5 "ertesi günün AOF'unda").
