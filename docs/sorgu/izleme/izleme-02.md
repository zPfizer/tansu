# İzleme 02: cevaplar-02-olaylar.md (EKSİK, KARAR, YANLIŞ maddeleri)

Karşılaştırılan: TASARIM taslak 6, KURALLAR, GLOSSARY, sonuc-3-4 (B-1..B-20, C-1..C-11, O1..O17), AGENTS.
Not: dosyada KARAR hükmü yok. ÇÖZÜM-A (iki katmanlı kendi seri) B-2 ile çelişir (göstergeler HGDG'den, kendi çarpan yalnız denetim) ve aşırı kurulumdur; ona bağlı maddeler RED.

02-002 — EKSİK — TEKRAR — 02-033 (olay günü ham getiri, ayar ile karşılaştırılır; yanlış çarpan 033 kuralında yakalanır)
02-003 — EKSİK — VAR — sonuc O3 ("çarpan o günden önceki satırlara uygulanır") ve TASARIM 4 ("Tarih hak kullanım günüdür")
02-008 — EKSİK — YENİ — TASARIM 5.1 İkinci kaynak: olay tablosunda kaydı olan günler borsapy karşılaştırmasından çıkarılır (borsapy düzeltme biçimi doğrulanmadı, sahte uyarıyı önler)
02-009 — EKSİK — VAR — TASARIM 5.1 (Olay denetimi: "HGDG geçerli kalır"; Karantina: "Fiyat yamanmaz")
02-010 — YANLIŞ — RED — taslak 6 zaten göstergeleri HGDG'den alır, kendi çarpan yalnız denetimdir (5.1, sonuc B-2); S2-13 ile çelişki yok; HGDG 4 ondalık gürültüsü BIST100 büyük hisselerinde ihmal edilebilir; ÇÖZÜM-A aşırı kurulum
02-014 — EKSİK — RED — ÇÖZÜM-A (temettüyü ayrı nakit akışı yapmak); HGDG bedelsiz, bedelli ve temettüyü zaten işler (B-2)
02-016 — EKSİK — VAR — TASARIM 5.1 Olay denetimi (boş tablo = çarpan 1, HGDG ile fark %0,5'i aşarsa uyarı) ve sonuc C-8 (şema assert, 3 deneme)
02-020 — EKSİK — TEKRAR — 02-033 (istisna yalnız ayarlı getiri tutarlıysa; bilinmeyen kod istisna almaz)
02-022 — EKSİK — YENİ — TASARIM 3 Kapsam dışı: "sembol değişikliği ve birleşme sürekliliği" ekle (veri biten sembol kapanma gibi okunmasın; nedeni bilinmeyen raporda listelenir, 5.2)
02-023 — EKSİK — VAR — TASARIM 5.2 ("yalnız pay hisseleri")
02-024 — EKSİK — YENİ — TASARIM 5.1 Karantina: olay istisnası SHHE_TARIH ±1 işlem günü penceresinde geçerlidir (HEKTS 2015-11-26 vakası)
02-026 — EKSİK — YENİ — TASARIM 4 veri / sonuc C-4: anlık görüntü olay tablosu ham JSON'unu da içerir (manifest sha256 ile)
02-028 — EKSİK — VAR — TASARIM 5.1 Karantina (250 gün yeni sinyal yok; önceki sinyaller silinmez)
02-029 — EKSİK — VAR — TASARIM 5.1 Karantina ("Açık pozisyon son temiz AOF'ta kapanır ve sayılır")
02-030 — EKSİK — VAR — TASARIM 5.1 Karantina ("Aynı maske kural, K1 ve K2'ye uygulanır"); karantinalı/karantinasız fark satırı için bkz 02-094
02-031 — EKSİK — VAR — TASARIM 5.1 Olay denetimi (olay tabloda yoksa ham x çarpan, HGDG'den %0,5'ten fazla sapar, uyarı); küçük temettü HGDG getirisini bozmaz
02-032 — EKSİK — TEKRAR — 02-031 (eksik olay denetimi oran/fark kontrolüne dayanır); veri-kaynaklari 7.2 işaretlemesi araştırma belgesidir, tasarım değişikliği değil
02-033 — EKSİK — YENİ — TASARIM 5.1 Fiyat limiti: olay gününde referans = önceki ham kapanış x ayar; karantina ve kilit bu ayarlı getiriyle yargılanır; bilinmeyen kod ya da ayar=1 istisna sayılmaz
02-034 — YANLIŞ — VAR — sonuc O7 (ECILC/RYSAS örneği yanlıştı); taslak 6 5.1'de örnek yok
02-035 — EKSİK — VAR — TASARIM 5.1 İndirme (ilk sinyal 30.11.2015, ±%20 rejiminin başı) ve sonuc B-6
02-037 — EKSİK — RED — sonuc O6: durdurma "eksik satır" değil sıfır hacimli satırdır; çok günlük boşluk oluşmaz; aşırı kurulum
02-038 — EKSİK — TEKRAR — 02-033 (ex-date referansı = önceki kapanış x ayar)
02-039 — EKSİK — VAR — TASARIM 5.3 Kilitli gün ("bir fiyat adımı toleransla") ve sonuc B-5; adım tablosu için bkz 02-056
02-041 — EKSİK — RED — ÇÖZÜM-A; taslak 6 giriş ve stop için tek seri (HGDG) kullanır (B-2)
02-042 — EKSİK — VAR — TASARIM 5.1 Seriler (göstergeler ve getiriler tek seriden, HGDG)
02-043 — EKSİK — VAR — TASARIM 6.6 / sonuc C-5 (açık kart her gün Adım ile yeniden hesaplanır; HGDG geriye ölçeklenir)
02-044 — EKSİK — VAR — TASARIM 5.1 Seriler (getiriler HGDG; giriş ve çıkış aynı seri, temettü dahil)
02-045 — EKSİK — RED — ÇÖZÜM-A; HGDG ölçeğinde adet x fiyat TL değeri değişmez, lot yuvarlama etkisi küçük; aşırı kurulum
02-049 — EKSİK — VAR — TASARIM 5.1 Seriler + 4 gostergeler (ATR, SMA tek seriden)
02-050 — EKSİK — RED — B-2 ile çelişir (stop HGDG'de; temettü düşüşünü stopa sokmak ÇÖZÜM-A gerektirir; aşırı kurulum)
02-051 — EKSİK — VAR — TASARIM 4 motor (sınama ve canlı aynı Adım, A5); temettü düşüşünü stopa sokma kısmı RED (bkz 02-050)
02-052 — EKSİK — RED — AB=CD ikinci dalgada (A ve D seviyeleri); ÇÖZÜM-A
02-053 — EKSİK — RED — kalıp geometrisi (harmonik, AB=CD) ikinci dalgada; ilk sürümde HGDG kullanılır
02-054 — EKSİK — VAR — TASARIM 5.1 Seriler (kapanış ve SMA250 aynı HGDG serisinden)
02-055 — EKSİK — VAR — TASARIM 5.1 Seriler (stop, yüksek, düşük aynı seri); ek motor testi için bkz 02-092
02-056 — EKSİK — YENİ — TASARIM 5.3 Kilitli gün: fiyat adımı = BISTECH adım tablosu (<20 TL 0,01; 20-50 0,02; 50-100 0,05; 100-250 0,10; 250-500 0,25; 500-1000 0,50; >=1000 1), YORUM/doğrulanmadı; kart yuvarlama ve ATR<3 adım kuralı RED (aşırı)
02-057 — EKSİK — RED — HGDG getirisi bedelsizi ölçek olarak zaten nötr tutar (B-2); ÇÖZÜM-A
02-058 — EKSİK — RED — HGDG getirisi hak mantığını kendiliğinden verir (ex-date öncesi girişte düzeltilmiş getiri); ayrı kod gereksiz (B-2)
02-059 — EKSİK — RED — bedelli teorik çarpanı HGDG'de; K1 ve K2 aynı etkiyi taşır; ±10 gün duyarlılık aşırı kurulum
02-062 — EKSİK — RED — kart her gün Adım ile yeniden hesaplanır (6.6); tablo ileri tarihli mi doğrulanmadı; aşırı kurulum
02-063 — EKSİK — RED — etki tek gündür, ertesi gün tablo gelince 6.6 yeniden hesabı düzeltir; açık soru 8.1; aşırı kurulum
02-064 — EKSİK — RED — 5.13 kapıları ve 5.1 Olay denetimi yeterli; üç ek tazelik kontrolü aşırı kurulum
02-065 — EKSİK — VAR — TASARIM 6.6 / sonuc C-5 (günün kart çıktısı kartlar.jsonl'e yalnız eklenir, geriye dönük değişmez)
02-066 — EKSİK — VAR — TASARIM 6.6 / sonuc C-5 (kartlar.jsonl yalnız ekleme)
02-067 — EKSİK — VAR — TASARIM 5.11 (deneme günlüğü: veri anlık görüntüsü, git commit); olay tablosunun anlık görüntüye girmesi 02-026'da
02-068 — EKSİK — RED — kapsam dışı: sistem emir vermez, Levent'in canlı işlemini kaydetmez (P1)
02-069 — EKSİK — RED — ÇÖZÜM-A (P_bölünme + net temettü akışı); getiri tanımı HGDG (B-2)
02-070 — EKSİK — VAR — TASARIM 5.11 ("Aynı kuralın tekrar koşusu yeni deneme değildir") ve sonuc C-6 (Holm birimi benzersiz kural kimliği)
02-071 — EKSİK — RED — olay tablosu yalnız denetim ve karantina istisnasında; ileri tarih sorunu doğurmaz; aşırı kurulum
02-072 — EKSİK — RED — ÇÖZÜM-A; 5.1 zaten limit, kilit, likiditeyi ham seriden alır
02-073 — EKSİK — RED — K1(b) aynı hisse ±20 gün olay etkisini aynı taşır; olay penceresi dışlama sonucu aşırı kurulum
02-074 — EKSİK — VAR — TASARIM 5.7 K1 Seçim (ön şartı sağlayan günler; ex-date dışlanmaz) ve 5.1 Karantina maskesi
02-077 — EKSİK — RED — ÇÖZÜM-A; brüt temettü şişmesi kural ve K2'de aynı etkiyi taşır; B-2
02-078 — EKSİK — VAR — TASARIM 5.7 Fazla getiri tanımı ve K2 (günlük karşılaştırma getirisi, eşit ağırlıklı sepet)
02-079 — EKSİK — RED — ÇÖZÜM-A; coint HGDG toplam getiri serisinde zaten, ikinci p değeri aşırı kurulum
02-080 — EKSİK — VAR — TASARIM 5.1 Seriler (iki bacak aynı HGDG serisi)
02-081 — EKSİK — RED — ÇÖZÜM-A (net temettü ayrı nakit akışı); HGDG ex-date'te yeniden yatırım varsayar
02-082 — EKSİK — YENİ — TASARIM 5.6 Çift bölmesi: bir bacak karantinadaysa çift o pencerede girişsiz kalır, açık bacak son temiz AOF'ta kapanır
02-083 — EKSİK — YENİ — TASARIM 5.7 Fazla getiri tanımı (işlem seviyesi): sepet getirisi işlemin giriş ve çıkış AOF'larından hesaplanır
02-084 — EKSİK — RED — ÇÖZÜM-A (fiyat/temettü ayrı satır); aşırı kurulum
02-085 — EKSİK — RED — Yahoo kullanılmaz (B-2)
02-086 — EKSİK — RED — Yahoo çıktı; sadakat İş Yatırım ham seriyle (B-2, O9, O10)
02-087 — EKSİK — RED — AB=CD ikinci dalgada (SMRTG, ISKPL) ve Yahoo çıktı
02-088 — EKSİK — RED — açılış yok, giriş AOF (5.3); Yahoo çıktı
02-089 — EKSİK — RED — Yahoo çıktı; anlık görüntü zaten tarihli (C-4)
02-090 — EKSİK — RED — Yahoo çıktı; EMA sadakati ham seriyle çözüldü (O9)
02-091 — EKSİK — RED — B-2 karardır (HGDG kesin); ham-yalnız-bölünme varyantı aşırı kurulum
02-092 — EKSİK — RED — HGDG ile olay motora girmez (olay veri katmanında); 5.3 motor sınamaları yeterli; vakalar ÇÖZÜM-A'ya bağlı
02-093 — EKSİK — YENİ — sonuc C-9 / TASARIM 5.1 Olay denetimi: veri birim testleri ekle: ayar>1 (sentetik), aynı güne iki kayıt (çarpım), +-1 gün kayması (HEKTS 2015-11-26); CCOLA temettü formülü RED
02-094 — EKSİK — YENİ — TASARIM 5.1 Karantina: rapor karantinalı hisse x gün sayısını ve oranını yazar (karantinalı/karantinasız fark satırı RED)
02-095 — EKSİK — RED — bozulma enjeksiyonu aşırı kurulum; olay tablosu getiriye girmez (yalnız denetim, B-18 boru hattı denetimi var)
02-096 — EKSİK — VAR — TASARIM 5.13 Eşikler (karantina oranı >%1, ikinci kaynak uyuşmazlığı >%2 ise koşu "veri sorunlu")
02-098 — EKSİK — TEKRAR — 02-038 (=02-033)
02-099 — EKSİK — VAR — sonuc O3 (çarpan SHHE_TARIH'ten önceki bütün satırlara); bileşik limit (1+L)^k kısmı RED (bkz 02-037)

## Özet

Etiket sayıları (grep ile):
- VAR: 27
- TEKRAR: 5
- YENİ: 10
- RED: 32
- Toplam satır: 74 (72 EKSİK + 2 YANLIŞ; KARAR yok)

YENİ maddeler ve önerilen değişiklik:
1. 02-008 — TASARIM 5.1 İkinci kaynak: olay tablosunda kaydı olan günler borsapy karşılaştırmasından çıkar.
2. 02-022 — TASARIM 3 Kapsam dışı: sembol değişikliği ve birleşme sürekliliği.
3. 02-024 — TASARIM 5.1 Karantina: olay istisnası SHHE_TARIH ±1 işlem günü.
4. 02-026 — TASARIM 4 veri / C-4: anlık görüntü olay tablosu JSON'unu da içerir.
5. 02-033 — TASARIM 5.1 Fiyat limiti: olay günü referansı = önceki ham kapanış x ayar; bilinmeyen kod ya da ayar=1 istisna değil.
6. 02-056 — TASARIM 5.3 Kilit: fiyat adımı tablosu (YORUM, doğrulanmadı).
7. 02-082 — TASARIM 5.6 Çift: bacak karantinadaysa çift girişsiz, açık bacak son temiz AOF'ta kapanır.
8. 02-083 — TASARIM 5.7 işlem seviyesi: sepet getirisi işlemin giriş ve çıkış AOF'larından.
9. 02-093 — C-9 / 5.1: olay denetimi birim testleri (ayar>1, aynı gün iki kayıt, ±1 gün kayması).
10. 02-094 — TASARIM 5.1 Karantina: rapor karantinalı hisse x gün sayısı ve oranı.

YANLIŞ maddeler (VAR değil olanlar):
- 02-010 — RED: taslak 6 göstergeleri zaten HGDG'den alır (5.1, B-2); S2-13 ile çelişki yok. Değişiklik yok.
(02-034 VAR: sonuc O7.)
