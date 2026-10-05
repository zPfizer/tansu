# İzleme 09: istatistik ve kabul

Kaynak: `docs/sorgu/sorgu-3/cevaplar-09-istatistik.md`. Karşılaştırılan: TASARIM taslak 6, KURALLAR, sonuc-3-4 (B-1..B-20, C-1..C-11). Yalnız EKSİK, KARAR ve YANLIŞ satırları izlendi.

09-001 — EKSİK — VAR — KURALLAR §3 (her ailenin "K1 ön şartı" satırı) + TASARIM 5.7 K1 Seçim; ön şart kod olduğu için C-6 hash'ine girer
09-002 — EKSİK — VAR — TASARIM 5.8 ("sonraki her değişiklik yeni denemedir") + sonuc C-6 (hash = kod + parametre)
09-003 — EKSİK — YENİ — TASARIM 5.7 K1 Eşleştirme: (a) türünde sayı gün başına korunur, hisseler o günün ön şartlı havuzundan çekilir
09-005 — EKSİK — VAR — TASARIM 5.7 p değeri ("aile p'si iki türün büyüğü"), sonuc B-15
09-006 — EKSİK — TEKRAR — 09-003
09-007 — EKSİK — RED — aşırı kurulum; 100 hisse × gün havuzu sinyalden çok büyük, güçsüzlüğü MDE ve "Ölçülemedi" (5.12, B-17) zaten yakalar
09-009 — EKSİK — YENİ — TASARIM 5.11: Holm yalnız B ≥ 1.000 tekrarlı p ile yapılır; geliştirmedeki 200 tekrarlı p Holm'a girmez
09-012 — EKSİK — VAR — TASARIM 5.7 K1 Çıkış ("tam çıkış paketi"), sonuc B-15
09-013 — EKSİK — RED — AB=CD ikinci dalgada
09-014 — EKSİK — VAR — TASARIM 5.7 K1 Çift bölmesinde ("aynı sayıda geçiş, rastgele günlerde; ilk giriş günü gerçeğe eşitlenir")
09-015 — EKSİK — YENİ — TASARIM 5.7 K1 Çift bölmesinde: "K1 çiftte yalnız z-skor zamanlamasını ölçer; seçim değeri K2 ile okunur" notu
09-016 — EKSİK — VAR — TASARIM 5.7 p değeri ("istatistik işlem başına ortalama fazla getiri"); medyan yalnız ek gösterim, 5.9
09-017 — EKSİK — VAR — TASARIM 5.7 ("tek yönlü") + 5.12.1 ("Holm düzeltmeli p < 0,05")
09-018 — EKSİK — VAR — TASARIM 5.7 fazla getiri tanımı ("aynı tutma süresinde") + K1 Çıkış
09-019 — EKSİK — YENİ — TASARIM 5.7 K2: sepet ay başı kurulur, aylık dengelenir (evren zaten aylık)
09-020 — EKSİK — YENİ — TASARIM 5.7 K2: sepet aynı %0,3 masrafı ay başı evren değişiminde ve dengelemede öder
09-021 — YANLIŞ — VAR — TASARIM 5.7 K2 "maruziyet eşleşmeli", sonuc B-13 (sepet ağırlığı = kuralın o günkü payı, kalan faizde)
09-022 — YANLIŞ — VAR — TASARIM 5.7 K2 ("kalanı aynı faizi kazanır"), sonuc B-13
09-025 — EKSİK — YENİ — TASARIM 5.8: "parametre sabit; yıllık yürüme yalnız çift seçimini yeniler; kâğıt dönemin yerine geçmez" (ad yanıltıcı)
09-027 — EKSİK — YENİ — TASARIM 5.12.4: tamamlanmamış yıl (2026) paydadan çıkar, ayrıca gösterilir
09-028 — EKSİK — VAR — TASARIM 5.1 (2010'dan indirme, ilk sinyal 30.11.2015) + 5.8 (2015–2017 ile başlar)
09-031 — EKSİK — RED — yalnız etiket; karar değişmez, kapsam dışı
09-032 — EKSİK — VAR — TASARIM 5.8 ("2015–2026 bütünüyle geliştirme/doğrulama verisi") + 5.10
09-034 — EKSİK — RED — yalnız etiket, ağırlık aynı; kapsam dışı
09-035 — YANLIŞ — VAR — TASARIM 5.9 "blok uzunluğu = max(20, ortalama tutma süresi)", sonuc B-16 (çiftte tutma ≈ 66 gün olunca blok uzar)
09-036 — EKSİK — RED — aşırı kurulum; B-16 blok kuralı yeter, durağan bootstrap ek yöntem
09-037 — EKSİK — YENİ — TASARIM 5.9: aralık yalnız rapordur; karar 5.12'den (p) verilir
09-038 — EKSİK — TEKRAR — 09-037
09-039 — EKSİK — RED — aşırı kurulum; B-13 nakit sıfırlarını kaldırır, B-18 null denetimi var
09-041 — EKSİK — YENİ — TASARIM 6.5 kart satırı: aralık birimi ve yöntemi yazılır ("%95 yüzdelik, blok bootstrap, günlük portföy serisi"); işlem düzeyi ile günlük seri tutarsızlığı giderilir
09-042 — EKSİK — VAR — TASARIM 5.7 (ortalama istatistiği) + 5.12.4 (en iyi %5 atılınca pozitif) + 5.9 medyan
09-044 — EKSİK — VAR — TASARIM 5.12 "Ölçülemedi", sonuc B-17
09-046 — EKSİK — YENİ — TASARIM 5.9: saptanabilir en küçük etki günlük portföy serisinden (bağımsız birim = gün) hesaplanır
09-047 — EKSİK — YENİ — TASARIM 5.9: çift bölmesinde örneklem şartı = en az 100 geçiş ve 60 farklı geçiş günü (işlem yerine)
09-050 — EKSİK — VAR — TASARIM 5.12 ("örneklem dolmazsa ... Ölçülemedi"), B-17
09-051 — EKSİK — YENİ — TASARIM 5.11: kabul kararı kabul anındaki m ile donar; sonradan artan m eski kararı geri almaz
09-052 — EKSİK — VAR — TASARIM 5.11 ("benzersiz kural kimlikleri") + sonuc C-6 (Holm birimi = kural kimliği; aynı kuralın tekrar koşusu sayılmaz)
09-053 — EKSİK — VAR — TASARIM 5.8 ("sonraki her değişiklik yeni denemedir"); hata düzeltmesi istisnası eklenmez (katı kural daha güvenli)
09-054 — EKSİK — VAR — TASARIM 5.11 ("her koşu yazılır"), C-6
09-055 — EKSİK — VAR — TASARIM 5.11 (her koşu günlükte, her benzersiz kural kimliği Holm'a girer); seçim ölçütleri KURALLAR §3'te getirisiz yazılı
09-056 — EKSİK — YENİ — TASARIM 5.10/5.11: ızgara hücreleri ve masraf senaryoları Holm m'ye girmez; Holm'a yalnız %0,3'teki p girer (şimdiki "benzersiz kural kimliği" ızgara hücrelerini m'ye sokar)
09-057 — EKSİK — TEKRAR — 09-056
09-058 — EKSİK — VAR — TASARIM 5.11 + sonuc C-6 (yalnız ekleme, git'te, resmi koşu temiz git ağacı ister); hash zinciri aşırı kurulum, eklenmez
09-059 — EKSİK — RED — aşırı kurulum; Holm ve B ≥ 20·m (B-14) zaten bedeli ödetir, varyant bütçesi ek kural
09-060 — EKSİK — VAR — TASARIM 5.12 (sentetik boş veriyle yanlış kabul ≤ %5), sonuc B-18
09-061 — EKSİK — YENİ — TASARIM 5.10: ızgara tanımı (parametre aralığı, hücre sayısı, tohum) kural kaydı hash'ine girer
09-062 — EKSİK — YENİ — TASARIM 5.10: sağlamlık şartı = pozitif hücre oranı ≥ %70 (Levent onaylar); 5.12.5 buna atıf yapıyor ama eşik yok
09-063 — EKSİK — TEKRAR — 09-056
09-064 — EKSİK — YENİ — TASARIM 5.10: hücre "pozitif" = K1'e göre ortalama fazla getiri > 0, %0,3 masrafla; p aranmaz
09-066 — EKSİK — VAR — TASARIM 5.12 (enjekte edilmiş etkiyle güç ölçümü), sonuc B-18
09-068 — EKSİK — RED — M7/M8 kararı; 5.8 kâğıt dönemin yalnız büyük bozulmayı yakaladığını zaten yazıyor, ek gerekçe belge işi
09-069 — EKSİK — RED — aşırı kurulum; 5.12.4 (en iyi %5 işlem atılınca pozitif) yeter
09-070 — EKSİK — RED — alt sınır şartı K1 kararını ikileştirir (09-038 ile aynı gerekçe); 5.12.2 K2 kontrolü olarak kalır
09-071 — EKSİK — VAR — TASARIM 5.6 ("VAKBN–GARAN ayrıca gösterilir; kabul kararına girmez"); dönem/masraf ayrıntısı eklenmez
09-072 — EKSİK — YENİ — TASARIM 6.4: kriter 1–5'i geçen aile "Kâğıt" etiketiyle kart üretir; "Canlı" kriter 6'dan sonra
09-074 — EKSİK — YENİ — TASARIM 5.8: kâğıt dönemde tek bakış, erken durdurma yok, 12 ayda dolmazsa "Ölçülemedi"
09-075 — EKSİK — VAR — TASARIM 6.6 (açık kartlar Adım ile yeniden hesaplanır) + 5.3 (AOF dolumu); gerçek dolum sütunu eklenmez
09-076 — EKSİK — VAR — TASARIM 5.8 (parmak izi kayda geçer) + 6.6/C-5 (kartlar.jsonl yalnız ekleme) + 4 (değişmez anlık görüntü)
09-077 — EKSİK — RED — kapsam dışı; piyasa durumu yalnız rapor (B-19)
09-078 — EKSİK — VAR — TASARIM 5.8 (her değişiklik yeni deneme; yeni ayrılmış dönem = kural kaydından sonrası)
09-079 — EKSİK — VAR — sonuc C-6 (hash = kod + parametre) + C-2 (sürümler sabit, lock dosyası) + TASARIM 5.11 (anlık görüntü, tohum günlükte)
09-080 — EKSİK — RED — aşırı kurulum; C-6 git commit yeter, yedek/dış kayıt yok kararı
09-081 — EKSİK — VAR — TASARIM başlık (C7: ön deneme kanıt değil) + 5.8 (2015–2026 bütünüyle geliştirme verisi, yeni dönem kayıttan sonra)
09-082 — EKSİK — RED — aşırı muhafazakâr; seçim getiriye bakmadı, 5.11 koşulan kuralları sayar, m'yi tüm katalogla başlatmak gücü öldürür
09-083 — EKSİK — VAR — TASARIM 5.12.6 (nokta oranı şartı, Holm yalnız 5.12.1'de) + 5.8 ("yalnız büyük bozulmaları yakalar")
09-084 — EKSİK — VAR — TASARIM 5.7 (işlem ve portföy seviyesi fazla getiri) + 5.8 (çift için günlük fazla getiri serisi)
09-085 — EKSİK — VAR — TASARIM 5.2 (evren kuralı kodda) + sonuc C-6 (kod hash'i) + C-5 (kartlar.jsonl)
09-086 — EKSİK — YENİ — TASARIM 5.7 K1: rastgele işlemler aynı giriş filtresini uygular (kilitli tavan, SMA250, likidite); kilitli tavandan kaçan sinyal sayısı raporlanır
09-088 — EKSİK — VAR — TASARIM 5.7 K2 maruziyet eşleşmeli, sonuc B-13
09-089 — EKSİK — TEKRAR — 09-015
09-090 — EKSİK — RED — kapsam dışı; kriter dışı bilgi, K2 maruziyet eşleşmesi beta farkını karşılar
09-091 — EKSİK — RED — 5.2 / B3 ile çelişir (mutlak getiri karar için kullanılmaz)
09-092 — EKSİK — YENİ — TASARIM 5.3: veri bitince açık pozisyon son kapanıştan zorunlu çıkar; K1 ve K2 aynı kuralı uygular
09-093 — EKSİK — RED — kapsam dışı; evren 100 kararı (5.2), BIST30 duyarlılığı gereksiz kurulum
09-094 — EKSİK — VAR — TASARIM 8 açık soru 3 (tedbirli hisseler bedava veriyle ayrılamıyor)
09-095 — EKSİK — RED — aşırı kurulum; 5.4 %0,5 masraf senaryosu kayma payını karşılıyor
09-096 — EKSİK — RED — aşırı kurulum; evren en büyük 100 + %20 hacim elemesi (5.2), fark sınırlı
09-097 — EKSİK — VAR — TASARIM 6.6 / C-5 (kartlar.jsonl yalnız ekleme = değişmez sinyal defteri); yeniden hesap fark raporu eklenmez
09-098 — EKSİK — TEKRAR — 09-056
09-100 — EKSİK — RED — aşırı kurulum; 5.12.6 zaten nokta oranı, p üretmez; aralık yalnız bilgi (09-037)

## Özet

Sayımlar (grep): 80 madde = VAR 35, TEKRAR 6, YENİ 20, RED 19. Dosyada KARAR hükmü yok; EKSİK 77, YANLIŞ 3.

YANLIŞ maddeler: üçü de VAR (021, 022 = TASARIM 5.7 K2 / B-13; 035 = TASARIM 5.9 / B-16). Hiçbiri YENİ ya da RED değil.

YENİ maddeler ve önerilen değişiklik:
1. 09-003 — 5.7 K1 Eşleştirme: (a) türünde gün başına sayı, (b) türünde hisse başına sayı.
2. 09-009 — 5.11: Holm yalnız B ≥ 1.000 p'si ile; 200 tekrarlı p girmez.
3. 09-015 — 5.7 K1 Çift: "yalnız z-skor zamanlamasını ölçer" notu.
4. 09-019 — 5.7 K2: sepet ay başı kurulur, aylık dengelenir.
5. 09-020 — 5.7 K2: sepet %0,3 masrafı öder.
6. 09-025 — 5.8: "yıllık bölme, parametre sabit; kâğıt dönemin yerine geçmez".
7. 09-027 — 5.12.4: tamamlanmamış yıl paydadan çıkar.
8. 09-037 — 5.9: aralık yalnız rapor, karar p'den.
9. 09-041 — 6.5 kart: aralık birimi ve yöntemi yazılır (işlem düzeyi / günlük seri tutarsızlığı).
10. 09-046 — 5.9: en küçük etki günlük portföy serisinden hesaplanır.
11. 09-047 — 5.9: çift bölmesi için en az 100 geçiş ve 60 farklı geçiş günü.
12. 09-051 — 5.11: karar kabul anındaki m ile donar.
13. 09-056 — 5.10/5.11: ızgara hücreleri ve masraf senaryoları m'ye girmez; Holm'a %0,3 p'si girer.
14. 09-061 — 5.10: ızgara tanımı (aralık, hücre sayısı, tohum) hash'e girer.
15. 09-062 — 5.10: sağlamlık eşiği pozitif hücre ≥ %70 (Levent onayı).
16. 09-064 — 5.10: "pozitif" = K1'e göre ortalama fazla getiri > 0, %0,3 masrafla.
17. 09-072 — 6.4: üçüncü statü "Kâğıt" (kriter 1–5 geçince kart; Canlı kriter 6'dan sonra).
18. 09-074 — 5.8: kâğıt dönemde tek bakış, erken durdurma yok, 12 ayda dolmazsa Ölçülemedi.
19. 09-086 — 5.7 K1: rastgele işlemler aynı giriş filtresini uygular; kaçırılan tavan girişi sayısı raporlanır.
20. 09-092 — 5.3: veri bitince son kapanıştan zorunlu çıkış; K1 ve K2 aynı.
