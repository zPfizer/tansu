# İzleme 03: Evren (cevaplar-03-evren.md ↔ taslak 6)

Kapsam: hüküm EKSİK (76) ve YANLIŞ (3) olan 79 madde. OLGU, CEVAPLI ve ZAYIF SORU maddeleri alınmadı. Tasarım belgesi düzenlenmedi.

03-001 — EKSİK — RED — fiili dolaşım (HAO_PD) taraması ikinci dalgada (TASARIM 3); ilk sürüm piyasa değeriyle sıralar; HAO_PD gürültülü, ölçüm 03-001 kendisi söylüyor
03-004 — EKSİK — YENİ — TASARIM 5.2 evren kuralına ekle: şirket başına tek kod (en yüksek 60 günlük TL hacimli); aynı şirketin kodları K2'de iki kez ağırlıklanmaz
03-005 — EKSİK — VAR — TASARIM 5.2 "yalnız pay hisseleri" + 60 günlük medyan elemesi
03-006 — EKSİK — VAR — TASARIM 5.1 Hacim: "hacmi sıfır olan gün işlem günü değildir"; 5.2 "o tarihte işlem gören"
03-007 — EKSİK — VAR — TASARIM 5.2 "60 günlük medyan TL hacimde en alttaki %20 elenir"; sonuc B-9
03-008 — EKSİK — VAR — TASARIM 5.2 alt %20 yüzdelik eşiği (mutlak TL değil); sonuc B-9
03-010 — EKSİK — VAR — TASARIM 5.2 "önceki ayın son kapanışındaki piyasa değeri"; sonuc B-9
03-011 — EKSİK — VAR — TASARIM 5.1 "veri 2010'dan indirilir… ilk sinyal 30.11.2015"; sonuc B-6
03-012 — EKSİK — VAR — TASARIM 5.2 "ayın ilk işlem günü"; TASARIM 4 Takvim fiyat günlerinden
03-013 — EKSİK — RED — aile kuralları zaten olay tanımlı (KURALLAR 3: dönem başına tek giriş, Z ve ΔZ eşiği); ek kural gereksiz
03-014 — EKSİK — VAR — TASARIM 5.2 "evren yalnız yeni girişi sınırlar; açık pozisyon kendi kuralıyla kapanır"; sonuc B-9
03-015 — EKSİK — VAR — TASARIM 5.2 "bugünkü listeyi geçmişe uygulamak sonuçları iyimser yapar"; göreli yorum 5.2 Sonuç + 5.7 K2 (12 ay gecikmeli varyant uygulanmaz, aşırı kurulum)
03-016 — EKSİK — RED — aşırı kurulum: histerezis ek parametre ve deneme; en küçük sistem istiyor
03-017 — EKSİK — RED — aşırı kurulum: Jaccard örtüşme eşiği; gerçek BIST100 işi TASARIM 7.10 paralel iş
03-018 — EKSİK — VAR — TASARIM 5.2 son madde "gerçek BIST100 çıkarılınca kurallar onda da koşulur"; TASARIM 7.10
03-019 — EKSİK — TEKRAR — 03-095
03-022 — EKSİK — VAR — TASARIM 4 `evren` modülü tarih → hisseler; `motor` Adım sınama ve canlıda ortak (A5); TASARIM 6
03-023 — EKSİK — RED — aşırı kurulum: KAP kapanmış sembol keşfi; TASARIM 5.2 eksikliği kabul eder ("bulunamayan semboller raporda yazılır"), TASARIM 8.4 açık soru
03-024 — EKSİK — RED — aşırı kurulum: keyfi %80 eşiği; 5.2 zaten bulunamayanları raporlar
03-027 — EKSİK — VAR — TASARIM 5.2 "kapanan hissede açık pozisyon −%100; nedeni bilinirse son fiyat"; sonuc B-9
03-028 — EKSİK — VAR — TASARIM 5.2 "60 işlem gününden uzun durdurma kapanma sayılır"; TASARIM 5.6 boş nakit faiz
03-029 — EKSİK — RED — aşırı kurulum: karantina (TASARIM 5.1) pencereyi zaten dışlar; elle birleşme etiketi gereksiz
03-031 — EKSİK — VAR — TASARIM 5.1 Karantina "açık pozisyon son temiz AOF'ta kapanır ve sayılır"
03-033 — EKSİK — RED — aşırı kurulum: kod yeniden kullanımı BIST'te nadir, ölçülmemiş
03-034 — EKSİK — TEKRAR — 03-004
03-037 — EKSİK — RED — TASARIM 5.1 ikinci kaynak + 5.13 eşik yeterli; güncel/kapanmış ayrı oran raporu aşırı kurulum
03-039 — EKSİK — VAR — TASARIM 5.2 (B-9: çıkan hissenin açık pozisyonu açık kalır, kapanışı −%100 ile görünür)
03-040 — EKSİK — TEKRAR — 03-039
03-041 — EKSİK — TEKRAR — 03-023
03-043 — EKSİK — RED — kapsam dışı: gerçek BIST100 zinciri TASARIM 7.10 paralel iş; ayrıntı o iş açılınca yazılır
03-044 — EKSİK — RED — kapsam dışı: gerçek BIST100 yedek kuralı, TASARIM 7.10 paralel iş
03-045 — EKSİK — RED — kapsam dışı: KAP yürürlük tarihi, TASARIM 7.10 paralel iş
03-046 — EKSİK — RED — kapsam dışı: KAP PDF çift okuma, TASARIM 7.10 paralel iş
03-047 — EKSİK — VAR — TASARIM 5.8 "sonraki her değişiklik yeni denemedir" + sonuc C-6 (hash kod + parametre; Holm birimi kural kimliği); "Canlı için KAP bağlayıcı" kısmı uygulanmaz (bkz. 03-099)
03-048 — EKSİK — RED — aşırı kurulum: ek çeyrek başı ara evren varyantı
03-050 — EKSİK — YENİ — TASARIM 5.6 çift seçimine ekle: sektörü olmayan (kapanmış) hisse çifte girmez; rapor "çift bölmesi hayatta kalanlardan kurulur" yazar
03-051 — EKSİK — YENİ — TASARIM 5.6 çift seçimine ekle: yıl başı seçim o yılın Ocak ilk işlem günü evreniyle yapılır
03-052 — EKSİK — VAR — TASARIM 5.2 (B-9, evren yalnız yeni girişi sınırlar) + 5.6 "yıl geçişi" kuralı
03-054 — EKSİK — VAR — TASARIM 5.6 "aynı sektörden en fazla 2 çift"; sonuc B-10
03-056 — EKSİK — VAR — TASARIM 5.2 "Sektör: kaba ve tarih bilgisiz; bilinen yanlılık" ("küçük" demiyor); duyarlılık varyantı uygulanmaz, aşırı kurulum
03-057 — EKSİK — TEKRAR — 03-056
03-059 — EKSİK — VAR — TASARIM 5.6 "p'ye göre açgözlü, bir hisse en fazla bir çiftte; boş pay nakitte"; sonuc B-10
03-060 — EKSİK — YENİ — TASARIM 5.6 çift bölmesine ekle: çiftin hissesi kapanırsa pay 5.2 kuralıyla kapanır, yıl sonuna kadar nakitte faiz kazanır, çift yeniden seçilmez
03-061 — EKSİK — TEKRAR — 03-054
03-062 — EKSİK — VAR — TASARIM 5.4 "pozisyon son 10 günün medyan TL tutarının %2'sini geçemez" (tavan sıfırsa pozisyon sıfır)
03-063 — EKSİK — RED — aşırı kurulum: TÜFE endeksleme ve yıl bazlı likidite raporu; TÜFE verisi kaynaklarda yok
03-064 — EKSİK — YENİ — TASARIM 5.6 "en likit önce" satırına ekle: likidite = sinyal günü dahil son 10 günün medyan TL tutarı (5.4 ile aynı)
03-065 — EKSİK — YENİ — TASARIM 5.7 K2'ye ekle: sepet ay başı evrenle yeniden dengelenir ve %0,3 masraf uygulanır
03-066 — EKSİK — YENİ — TASARIM 5.7 K2'ye ekle: sepet üyeliği giriş günü evreni, günlük eşit ağırlık; sepette kapanan hisse 5.2 kuralıyla işlenir
03-067 — EKSİK — VAR — TASARIM 5.7 K1 "kuralın kendi ön şartlarını sağlayan günlerden seçilir", tür (b) ±20 gün
03-068 — EKSİK — YENİ — TASARIM 5.3 sinyal ve giriş maddesine ekle: SMA250 hesaplanamayan (250 günden az geçmişi olan) hisse sinyal üretmez
03-069 — EKSİK — TEKRAR — 03-068
03-070 — EKSİK — RED — aşırı kurulum: ikinci (PD ağırlıklı) sepet; K2 eşit ağırlık kararı sonuc B-13
03-071 — EKSİK — RED — aşırı kurulum: çeyrek dönüşü etiketi, etkisi ölçülmemiş
03-072 — EKSİK — RED — aşırı kurulum: K2'ye likidite şartı; K2 maruziyet eşleşmeli (sonuc B-13), ek şart yok
03-073 — EKSİK — RED — kapsam dışı: KAP listesi ile yanlılık ölçümü, TASARIM 7.10 paralel iş
03-074 — EKSİK — RED — kapsam dışı: aynı KAP ölçümü, TASARIM 7.10
03-075 — EKSİK — RED — kapsam dışı: aynı KAP ölçümü, TASARIM 7.10
03-076 — EKSİK — RED — kapsam dışı: aynı KAP ölçümü; örneklem şartı zaten 5.9 ve "Ölçülemedi" 5.12
03-077 — EKSİK — RED — kapsam dışı: KAP sabit liste ayrıştırması, TASARIM 7.10; aşırı kurulum
03-078 — EKSİK — RED — kapsam dışı: iki kesitli KAP ölçümü, TASARIM 7.10
03-079 — EKSİK — RED — aşırı kurulum: 5.12'ye KAP sabit liste işareti şartı; 5.12 göreli ölçütler (K1, K2) yeterli
03-080 — EKSİK — TEKRAR — 03-046
03-081 — EKSİK — TEKRAR — 03-004
03-082 — EKSİK — TEKRAR — 03-077
03-083 — YANLIŞ — RED — taslak 6 5.2 "üst sınır" demiyor; mutlak getiri zaten karar dışı (5.2 Sonuç); öncül taslak 6'da yok
03-084 — EKSİK — YENİ — TASARIM 5.2 Sonuç'a ekle: "göreli karşılaştırma da yanlılıktan tam arınmış değildir; yönü ölçülmedi"
03-086 — YANLIŞ — YENİ — TASARIM 5.2 Sonuç'a ekle: mutlak getiri karar dışı; tek istisna 5.12 portföy kuralı, yalnız ret yönünde (geçmesi kanıt değildir)
03-087 — EKSİK — VAR — TASARIM 4 `evren` canlıda da kullanılır (A5); TASARIM 5.12 madde 6 "doğrulamadaki etkinin en az yarısı"
03-089 — EKSİK — VAR — TASARIM 5.11 deneme günlüğü (veri anlık görüntüsü + git commit) ve Holm birimi benzersiz kural kimliği; sonuc C-6
03-090 — EKSİK — VAR — TASARIM 5.8 kural kaydı + sonuc C-6 (hash: kod dosyalarının ast.dump'ı + parametre JSON'u; sonraki değişiklik yeni deneme)
03-092 — EKSİK — RED — Tansu'nun 500+ momentum evreni ilk sürümde yok (TASARIM 3); 03-093 etiketi yeter
03-093 — EKSİK — YENİ — TASARIM 5.2 evren kuralına ekle: "(YORUM, bizim; Tansu'nun evren tanımı yok)"
03-094 — EKSİK — TEKRAR — 03-093
03-095 — EKSİK — RED — TASARIM 5.3 kilitli gün tanımı yeterli; brüt takas ayırt edilemez (TASARIM 8.3 açık soru); ek bayrak aşırı kurulum
03-097 — YANLIŞ — RED — fiili dolaşım ikinci dalgada (TASARIM 3); HAO_PD TASARIM 4'te zaten alan olarak listeli; S2-51 düzeltmesi tasarım belgesini değiştirmez
03-098 — EKSİK — TEKRAR — 03-047
03-099 — EKSİK — RED — 5.2 Sonuç ve 5.12 göreli ölçütle karar verir (sonuc B-3b); ara evrene karşı KAP şartı Canlı kararını süresiz bloklar, aşırı kurulum
03-100 — EKSİK — RED — taslak 6 "yanlılığı azaltan" sıfatını kullanmıyor ("BIST100 benzeri"); ad değişikliği gereksiz

## Özet

Etiket sayıları (grep ile sayıldı):

| Etiket | Sayı |
|---|---|
| VAR | 25 |
| TEKRAR | 12 |
| YENİ | 11 |
| RED | 31 |
| Toplam | 79 |

YENİ maddeler ve önerilen değişiklik:
1. 03-004 — 5.2: şirket başına tek kod (en yüksek 60 günlük TL hacimli).
2. 03-050 — 5.6: sektörü olmayan hisse çifte girmez; rapora not.
3. 03-051 — 5.6: yıl başı seçim Ocak ilk işlem günü evreniyle.
4. 03-060 — 5.6: çiftin hissesi kapanırsa pay 5.2 kuralıyla kapanır, yıl sonuna kadar nakitte faiz kazanır.
5. 03-064 — 5.6: "en likit" = son 10 günün medyan TL tutarı (5.4 ile aynı).
6. 03-065 — 5.7 K2: sepet ay başı yeniden dengelenir, %0,3 masraf.
7. 03-066 — 5.7 K2: sepet üyeliği giriş günü evreni; sepette kapanan hisse 5.2 kuralıyla.
8. 03-068 — 5.3: SMA250 hesaplanamayan hisse sinyal üretmez.
9. 03-084 — 5.2 Sonuç: göreli karşılaştırma da yanlılıktan tam arınmış değil.
10. 03-086 — 5.2 Sonuç: mutlak getiri karar dışı; tek istisna 5.12 portföy kuralı, yalnız ret yönünde.
11. 03-093 — 5.2: evren kuralına "(YORUM, bizim)" etiketi.

YANLIŞ maddeler ve VAR olmayanlar:
1. 03-083 — RED: taslak 6 "üst sınır" demiyor; öncül yok.
2. 03-086 — YENİ: yukarıdaki 10. madde.
3. 03-097 — RED: fiili dolaşım ikinci dalgada; HAO_PD zaten alan olarak listeli.
