# İzleme 08: Portföy, masraf

Kaynak: `docs/sorgu/sorgu-3/cevaplar-08-portfoy.md`. Karşılaştırılan: TASARIM (taslak 6), KURALLAR, GLOSSARY, sonuc-3-4 (B-1..B-20, C-1..C-11), AGENTS. Atlanan hükümler: CEVAPLI, OLGU, ZAYIF SORU. Hiçbir tasarım belgesi düzenlenmedi.

08-001 — EKSİK — VAR — TASARIM 5.6 (tavanın bağladığı işlem oranı ve gerçekleşen risk raporda), sonuc B-12
08-003 — EKSİK — VAR — TASARIM 5.6 (sermaye 1.000.000 TL, özkaynak = nakit + pozisyonların kapanış değeri), sonuc B-12
08-004 — EKSİK — VAR — TASARIM 5.6 ("bileşik büyür")
08-005 — EKSİK — TEKRAR — 08-021 (likidite tavanının bağladığı işlem oranı; yıl kırılımı 5.12.4'te zaten var)
08-006 — EKSİK — RED — AB=CD ikinci dalgada; ATR ailelerinde adet = %1 risk / 2 ATR zaten 5.5 ve 5.6'da
08-007 — EKSİK — VAR — TASARIM 5.6 ("adet aşağı yuvarlanır"), sonuc B-12; kartta fiili risk var (6.5)
08-008 — EKSİK — VAR — TASARIM 6.5 (referans fiyat = sinyal kapanışı) ve 6.6 (Adım ile yeniden hesap), sonuc B-20
08-009 — EKSİK — YENİ — TASARIM 6.5: kartta stop "tahmini (referans fiyat − 2 ATR); gerçek stop ertesi AOF'tan" diye etiketlenir
08-010 — EKSİK — YENİ — TASARIM 5.1/5.3: pozisyonun giriş, stop, adet durumu tek ölçekte (HGDG) tutulur; ham seri yalnız limit, kilit, likidite içindir
08-011 — EKSİK — VAR — TASARIM 5.1 (getiriler HGDG'den; HGDG brüt temettü ve bedelli düzeltir), TASARIM 5.4 (vergi sınamaya girmez), sonuc O2
08-012 — EKSİK — TEKRAR — 08-010 (pozisyon durumu HGDG ölçeğinde)
08-013 — EKSİK — YENİ — TASARIM 5.6: adet = min(risk adedi, %10 tavan, %2 likidite, nakit/(fiyat·(1+masraf))); nakit yetmezse küçült
08-014 — EKSİK — YENİ — TASARIM 5.4: "valör modellenmez; satış nakdi aynı gün kullanılır" varsayımı bir cümleyle yazılır
08-015 — EKSİK — YENİ — TASARIM 5.3: aynı AOF gününde önce çıkışlar, sonra girişler işlenir
08-016 — EKSİK — YENİ — TASARIM 5.3: slot ya da nakit yüzünden reddedilen sinyal işlem sayısına girmez; sayısı raporda ayrı yazılır
08-017 — EKSİK — YENİ — TASARIM 5.6: "en likit" = 5.4'teki 10 günlük medyan TL tutarı
08-018 — EKSİK — VAR — TASARIM 5.9 (örneklem şartı), 5.12 ve sonuc B-17 ("Ölçülemedi"); tutma süresi 5.9 blok uzunluğunda kullanılır
08-019 — EKSİK — YENİ — TASARIM 5.4: 10 günlük pencere sinyal günü dahil, giriş günü hariç
08-021 — EKSİK — YENİ — TASARIM 5.4: rapor, %2 likidite tavanının bağladığı işlem oranını yazar (5.6'daki %10 tavan satırı gibi); kalan miktar ertesi gün alınmaz
08-022 — EKSİK — YENİ — TASARIM 5.7 K1: rastgele işlemler aynı simülatörden geçer (aynı boyutlandırma, faiz, masraf, pozisyon sınırı, sıra); gerçekleşen risk günlüğe yazılır
08-023 — EKSİK — RED — aşırı kurulum (giriş tavanı 5.4'te var; çıkış günü hacim oranı tanı satırı)
08-024 — EKSİK — RED — aşırı kurulum (adet/gerçek gün hacmi dağılımı tanı satırı; karar kuralı değil)
08-025 — EKSİK — RED — aşırı kurulum (katılım dağılımı raporu; %2 tavanı ve %0,3 masraf 5.4'te, %0,5 senaryosu var)
08-027 — EKSİK — YENİ — TASARIM 8: açık soru "HACIM toptan/çapraz işlemleri içeriyor mu (şişkin medyan olası)"
08-028 — EKSİK — RED — aşırı kurulum (kilit tanımı 5.3'te ve sonuc B-5'te; "tavana yakın AOF" yeni parametre)
08-029 — EKSİK — VAR — TASARIM 5.3 ("kilitli tabanda çıkış ertesi güne kayar"), sonuc B-5
08-030 — EKSİK — YENİ — TASARIM 5.3/6.5: işlem günlüğüne "planlanan risk" ve "gerçekleşen kayıp" kolonları (boşluklu stop, ardışık kilit)
08-031 — EKSİK — VAR — TASARIM 5.3 ("dolum min(stop, AOF)"), sonuc B-4
08-032 — EKSİK — VAR — TASARIM 5.3 ("Giriş günü: yalnız stop kontrol edilir", min(stop, AOF)), sonuc B-4
08-033 — EKSİK — TEKRAR — 08-030 (gerçekleşen kayıp / planlanan risk kolonu; yıl bazı 5.12.4'te var)
08-035 — EKSİK — VAR — TASARIM 5.6 (özkaynak = pozisyonların kapanış değeri); duyarlılık satırı gereksiz
08-036 — EKSİK — VAR — TASARIM 5.2 (kapanan hissede açık pozisyon −%100, nedeni bilinirse son fiyat; bulunamayan semboller raporda), sonuc B-9
08-037 — EKSİK — VAR — TASARIM 5.2 ("Evren yalnız yeni girişi sınırlar. Evrenden çıkan hissenin açık pozisyonu kendi kuralıyla kapanır"), sonuc B-9
08-038 — EKSİK — VAR — TASARIM 5.4 ("komisyon, BSMV, kayma birlikte"; "açılışta kovalama" ifadesi yok)
08-039 — EKSİK — RED — aşırı kurulum (5.4 sabit %0,3 ve %0,1/%0,5 gösterimi yeter; tarife belgesi gerekmez)
08-040 — YANLIŞ — RED — taslak 6'da "ölçekten bağımsız" iddiası yok (5.6 sabit 1.000.000 TL; likidite TL tavanı açık, kart sınırı için 08-098); sermaye ızgarası aşırı kurulum
08-041 — EKSİK — RED — aşırı kurulum (evren BIST100 benzeri; fiyat adımı kırılımı gereksiz)
08-042 — EKSİK — VAR — TASARIM 5.4 (%0,5 masraf senaryosu, kabul için şart) ve 5.3 (min(stop, AOF)), sonuc B-4
08-043 — EKSİK — RED — aşırı kurulum (5.4 %0,1/%0,3/%0,5 aralığı yeter; masraf tarihçesi araştırması gereksiz)
08-044 — EKSİK — VAR — TASARIM 5.4 ("Vergi: sınamaya girmez; raporda not edilir"), TASARIM 8.7
08-045 — EKSİK — RED — aşırı kurulum (başa baş masrafı; %0,1/%0,3/%0,5 gösterimi yeter)
08-048 — EKSİK — YENİ — TASARIM 5.7 K2: sepet ay başı dengelenir, AOF'tan AOF'a, aynı %0,3 masrafı öder; K1 portföyle aynı masrafı öder
08-051 — YANLIŞ — VAR — TASARIM 5.6 çift bölmesi ("Her çift payı, ilk sinyale kadar nakittedir; sonra hep çiftin bir hissesindedir")
08-052 — EKSİK — VAR — TASARIM 5.6 ("Boş pay nakitte kalır"), sonuc B-10, K2 maruziyet eşleşmeli (5.7, B-13)
08-053 — EKSİK — YENİ — TASARIM 5.6: hiç çift seçilmeyen yıl "işlem yok" işaretlenir ve 5.12.4 paydasından çıkar
08-054 — EKSİK — YENİ — TASARIM 5.6: yıllık çift seçimi yılın ilk işlem günü kapanışında; çıkış ve girişler ertesi AOF'ta (5.3)
08-055 — EKSİK — RED — aşırı kurulum (5.4 %2 tavanı pozisyona zaten uygulanır; evren en alt %20 hacmi eler)
08-056 — EKSİK — YENİ — TASARIM 5.6: çift payları yıl başı eşit, yıl içinde dengeleme yok; K2 çift için yıl başı 50/50 sabit adet
08-058 — EKSİK — YENİ — TASARIM 5.9: çift bölmesinde "işlem" = geçişten geçişe tutuş dönemi
08-059 — EKSİK — RED — aşırı kurulum (alfa regresyonu; K2 maruziyet eşleşmeli, B-13, varyansı zaten hizalar)
08-060 — EKSİK — RED — aşırı kurulum (TASARIM 5.6: Tansu'nun çifti "ayrıca gösterilir"; iki masraflı satır gereksiz)
08-061 — EKSİK — VAR — TASARIM 5.8 (6 ayda saptanabilir en küçük etki ≈ %56, "yalnız büyük bozulmaları yakalar") ve 5.12 "Ölçülemedi", sonuc B-17
08-062 — EKSİK — RED — kapsam dışı (KURALLAR 4 sadakat yalnız Z, beta, geçiş, sıkışma süresi üretir; getiri ve faiz hesaplanmaz)
08-063 — YANLIŞ — VAR — TASARIM 4 ("Faiz: borsapy TCMB politika faizi; 2015'ten tek seri"), sonuc B-8 ve O8
08-067 — EKSİK — TEKRAR — 08-068 (faiz duyarlılığı)
08-068 — EKSİK — RED — B-13 ile örtüşür (K2 kalanı aynı faizle kazanır; faiz iki tarafta ortak); faizli/faizsiz çift koşu aşırı kurulum
08-069 — EKSİK — VAR — TASARIM 5.6 ("bir gün gecikmeli politika faizi, takvim günü, /365"), sonuc B-8
08-070 — EKSİK — VAR — TASARIM 4 simulator ve 5.6 ("boştaki nakit faiz kazanır")
08-071 — EKSİK — YENİ — TASARIM 8 ve 5.13: açık soru "faiz serisi 1 hafta repo mu"; faiz serisi boşsa koşu SORUNLU; rapor başlığına faiz kaynağı ve son tarih
08-072 — EKSİK — VAR — TASARIM 5.7 K3 (ölçüt değil; faiz simülatörde), 5.12'de K3 ölçütü yok
08-073 — EKSİK — RED — aşırı kurulum (K2 maruziyet eşleşmeli ve K3 yeter; "hiç işlem yapma" bilgi satırı)
08-074 — EKSİK — TEKRAR — 08-071 (faiz serisi yoksa durur; başlıkta kaynak ve tarih)
08-075 — EKSİK — VAR — TASARIM 5.7 K2 maruziyet eşleşmeli, sonuc B-13
08-076 — EKSİK — TEKRAR — 08-048 (K2 yeniden dengeleme sıklığı)
08-077 — EKSİK — TEKRAR — 08-048 (K2 ve K1 AOF'tan AOF'a, aynı masraf)
08-078 — EKSİK — RED — B-15 ile çelişir (K1 p değeri işlem başına ortalama fazla getiri; 5.12.1 ve 5.12.2 iki düzeyi bilerek ayırır)
08-079 — EKSİK — TEKRAR — 08-022 (K1 aynı simülatörde)
08-081 — EKSİK — TEKRAR — 08-022 (K1 aynı boyutlandırma)
08-083 — EKSİK — YENİ — TASARIM 5.8: tek sürekli koşu; sermaye yıldan yıla taşınır; yıl = eğrinin kesiti; yıllık fazla getiri = o yıldaki günlük portföy fazla getirisi toplamı (5.7)
08-084 — EKSİK — TEKRAR — 08-083 (yıl kesiti tanımı)
08-086 — EKSİK — RED — aşırı kurulum (5.8 yıl bazlı sonuç zaten ayrı yazılır; TÜFE kaynağı yok)
08-087 — EKSİK — YENİ — TASARIM 5.12 portföy kuralı: "en büyük düşüş nominal TL özkaynak eğrisinde ölçülür"
08-088 — EKSİK — VAR — TASARIM 5.6 ("İlk sürümde her aile kendi sermayesiyle ayrı") ve 5.12 portföy kuralı
08-089 — EKSİK — VAR — TASARIM 5.12 ("aile reddedilir"); yeni YORUM/deneme sayısı 5.8 ve KURALLAR 0
08-090 — EKSİK — YENİ — TASARIM 5.12 portföy kuralı: %25 ve 12 ay kuralı %0,5 masraflı, faizli eğriye uygulanır
08-092 — EKSİK — TEKRAR — 08-083 (etki birimi = günlük portföy fazla getirisi, yıllık)
08-093 — EKSİK — RED — aşırı kurulum (KURALLAR 3 YORUM satırları ve P5 farkı zaten ayırır; isteğe bağlı Tansu koşusu gereksiz)
08-094 — EKSİK — VAR — TASARIM 5.10 ("YORUM satırları" ızgarada oynar; %10 tavan YORUM, sonuc B-12), KURALLAR 0 (her YORUM deneme sayısına girer)
08-095 — EKSİK — VAR — TASARIM 5.5 ("kaynak Tansu'nun paylaştığı infografik"), KURALLAR 0 NotebookLM ayrımı
08-096 — YANLIŞ — VAR — TASARIM 5.5 ("ertesi günün AOF'unda"), 5.3 ve KURALLAR 3 sonu
08-098 — EKSİK — YENİ — TASARIM 6.5: kartta "likidite üst sınırı: X TL" satırı (mutlak TL; farklı sermayede Levent kendi yüzdesini çarpar)
08-099 — EKSİK — RED — kapsam dışı (sistem emir vermez, P1; "gerçek dolum" kolonu aşırı kurulum)
08-100 — EKSİK — VAR — TASARIM 5.1 (olay denetimi: çarpan ham seriye uygulanır, HGDG ile karşılaştırılır, fark %0,5'i aşarsa uyarı), sonuc B-2

## Özet

Sayımlar grep ile yapıldı (aşağıda).

- Toplam: 83 madde (EKSİK 79, YANLIŞ 4)
- VAR: 30
- TEKRAR: 11
- YENİ: 22
- RED: 20

### YENİ maddeler ve önerilen değişiklik
- 08-009: 6.5 kartta stop "tahmini" etiketi.
- 08-010: 5.1/5.3 pozisyon durumu HGDG ölçeğinde (08-012 aynı).
- 08-013: 5.6 adet formülüne nakit sınırı.
- 08-014: 5.4 valör modellenmez cümlesi.
- 08-015: 5.3 aynı gün önce çıkış, sonra giriş.
- 08-016: 5.3 reddedilen sinyal sayacı.
- 08-017: 5.6 "en likit" = 5.4 medyan tutarı.
- 08-019: 5.4 pencere sinyal günü dahil, giriş günü hariç.
- 08-021: 5.4 likidite tavanı bağlama oranı raporda (08-005 aynı).
- 08-022: 5.7 K1 aynı simülatörden geçer (08-079, 08-081 aynı).
- 08-027: 8 açık soru: HACIM toptan/çapraz işlem içeriyor mu.
- 08-030: 5.3/6.5 planlanan risk ve gerçekleşen kayıp kolonları (08-033 aynı).
- 08-048: 5.7 K2 ay başı dengeleme, aynı masraf (08-076, 08-077 aynı).
- 08-053: 5.6 çift seçilmeyen yıl "işlem yok", 5.12.4 paydası dışı.
- 08-054: 5.6 çift seçim zamanı: yılın ilk işlem günü kapanışı, ertesi AOF.
- 08-056: 5.6 çift payı yıl başı eşit, yıl içinde dengeleme yok.
- 08-058: 5.9 çift bölmesinde işlem = geçişten geçişe tutuş dönemi.
- 08-071: 8 ve 5.13 faiz serisi açık sorusu, boşsa SORUNLU, başlıkta kaynak ve tarih (08-074 aynı).
- 08-083: 5.8 tek sürekli koşu, yıl = eğri kesiti, yıllık fazla getiri tanımı (08-084, 08-092 aynı).
- 08-087: 5.12 en büyük düşüş nominal TL özkaynak eğrisinde.
- 08-090: 5.12 portföy kuralı %0,5 masraflı, faizli eğriye uygulanır.
- 08-098: 6.5 kartta mutlak TL likidite üst sınırı.

### YANLIŞ maddeler (VAR olmayanlar)
- 08-040 — RED: taslak 6'da "ölçekten bağımsız" iddiası yok; kart sınırı 08-098 ile çözülür.
Diğer üç YANLIŞ (08-051, 08-063, 08-096) VAR.
