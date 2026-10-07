# Notlar arası ilişkiler ve eksik parça eşleştirme

Levent (06.10): "Notları birbirleriyle ilişkili mi diye bakınca eksik parçaları bulabilirsin."
Yöntem: bir modülün eksik parçası (tetik, stop, kapı, parametre) başka bir notta aranır. Eşleşme bir hipotezdir;
sadakat testiyle (Tansu'nun kendi örneğini yeniden üretme) doğrulanmadan kural sayılmaz.

İşaretler: (G) görsel, birinci el · (X) birebir · (A) aktarım. Kaynaklar parça dosyalarındaki bölümlerdir.

## İlk üç örnek (orkestratör, 06.10)

### 1. Çift rotasyonu: eksik kapı
- Eksik: VAKBN–GARAN grafiğinde Nisan 2025'te Z ≈ −2,3 ve −2,0 iken işlem yok; portföy Haziran sonuna kadar düz
  (p03, ajan okuması). "Z ≤ −2 ve ΔZ > 0" tek başına yetmiyor; bilet 06 Z'yi 1.564 adayla üretemedi.
- İlişkili notlar:
  - (A) "stat-arb sisteminde momentum dönüş teyidi uygulanmasının kârlarda çarpan etkisi" (p02).
  - (A) "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım; görünmez bağ kopmuş olabilir" (p05, 53;
    AGROT–GARAN olumsuz örnek).
  - (A) Kointegrasyon: "yüksek korelasyonun durağan spread anlamına gelmediği"; Engle-Granger / Johansen (p03).
  - Aynı aileden başka örnekler: CIMSA–OYAKC (p05, 51), AGROT–GARAN (p05, 52/54/55).
- Hipotez: giriş = Z eşiği + momentum dönüş teyidi; üstünde bir "çift sağlığı" kapısı (kointegrasyon). Gölgeli dönem
  bu kapının açık olduğu dönem olabilir.
- Sınama: VAKBN–GARAN ve CIMSA–OYAKC'de Nisan 2025 sinyalsizliğini ve işlem tarihlerini yeniden üretiyor mu?

### 2. EMA sıkışması: eksik giriş tetiği
- Eksik: KRDMD'de sıkışma ölçüsü çözüldü (bilet 05), giriş tetiği yok; bilet 15'te tetiği biz uydurduk.
- İlişkili notlar:
  - (A) "sıkışma zamanları iyi tespit edilirse ve aynı alanda formasyon bulunursa güçlü kâr fırsatı" (p05, 67).
  - (A) Demand içinde EMA sıkışması; "agresif giriş demand alt sınırı/fitil; güvenli giriş ilk uzun bullish breakout
    mumu veya retest" (p06, 106).
  - (G) ICBCT Pre Signal: EMA seti görselde, tetik gizli (p05, 65). (A) "parametreleri açıklayamam, ana fikri verdim" (p05, 65).
  - (A) Sıkışma = "kısa/orta/uzun vadeli denge ve düşük oynaklık" (p05, 68); (G) rehavet = kırılım habercisi (p04, 36).
- Hipotez: sıkışma tek başına sinyal değil, bir **bağlam**. Giriş = sıkışma bir talep bölgesindeyken ilk uzun yükseliş
  mumu kırılımı ya da kırılım sonrası geri test.

### 3. AB=CD: parçalar beş notta dağınık, birleşince tam kurulum
- Yapı: D = C + r(B−A) (rakamla doğrulandı, KURALLAR).
- Bağlam: (A) "ABCD'ye gözü kapalı güvenilmez; kanalı okumadan iş yapılmaz" (p04, 43); talep toplama bölgesi (p04, 40).
- Tepki penceresi: (G) "D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ" (p01, KAPLM).
- Teyit: (G) BALAT "Küm. Delta" negatif, kör ABCD başarısız (p05, 45). Günlük veride delta yok → hacim yaklaşımı.
- Stop ve hedef: (G) "İlk Stop (X)", "TP1 (1:1 R/R)", "TP2 (.618 AD)" (p01, SAYAS; okuma 07.10'da düzeltildi, defter-1 görsel düzeltmesi 41); (G) "Hedef 0.618 / 1.000 / 1.618" (p04, 42/43).
- Yön: SMRTG tablosu kısa yönlü (p04); BIST'te "D'de alım" varyantı (p04, RYSAS "Taze D Noktası (Alış)").
- Hipotez: tam kurulum = kanal/talep bağlamında D → 20 bar içinde tepki + hacim teyidi → giriş → stop X, TP1 1:1, TP2 0,618.

## Tam eşleştirme

Kaynak: parca-01 … parca-06 (p01–p06) ve gerektiğinde ham görseller (06.10, ajan). Kısaltma: p04/02 = parça 04, paket 02; p01/K2 = parça 01, kart 2.
Bağ türleri: (a) aynı hisse ve yakın tarih · (b) aynı araç ya da çıktı biçimi · (c) aynı kavram, farklı ad · (d) bir notun sorusuna başka notun cevabı.
Güven: yüksek = birinci el (G/X) ile destekli · orta = birden çok aktarım ya da G+A uyuşuyor · düşük = tek aktarım ya da yalnız benzerlik.
Bu görevde ham görselden doğrulananlar "(görsel doğrulandı)" ile işaretli: p05/46, 48, 49 (mavi çizgi aracı), p04/36, p05/65, 67, p05/44, p04/41, p05/74.

### Kümeler (aynı "sistem"e ait görünen not grupları)

1. **Harmonik tarayıcı ailesi.** Üyeler: p01 (KAPLM, SAYAS, A1CAP, ALARK, abcd-geometrik, fibonacci-extension, gartley-d-tepki, haftalık Gartley, gartley-butterfly-ayrı), p02/M1 (ISKPL), p03 (DOAS kelebek, Three Drives), p04/01–03, 32, 34, 35, 38–43 (KRPLS, DGATE, MARKA, SOKE, LUKSK, SMRTG, LIDER, AKCNS, RYSAS), p05/45 (BALAT), 47 (Trident), p06/109 (BALAT Siyah Kuğu), 122 (MAKIM), 123 (Gartley tablosu).
   Ortak iz: "D (CD=1.0AB)" ve "D (CD=1.27AB)" etiketi; "Sistem: Pesavento/Carney"; durum etiketleri TAMAMLANDI/AKTİF/TEPKI_VERDI/BOZULDU; "Harmonik sayı: N TL" başlık alanı (A1CAP 6.31, SMRTG 3.02); "Hedef 0.618/1.000/1.618"; "X->B trend çizgisi"; EMA 5/8/13 + "Direnç TL" + "Küm. Delta" paneli.
2. **Arz-talep / SMC bölge ailesi.** Üyeler: p04/09–13, 15, 17, 18, 20, 21, p06/93, 99, 101, 105–107, 110, p05/64, 69, 78, p03 (AHENK, BOM, CWENE dalga2, AKFIS, XU100), p01 (acsel, fibo-0618-OB, formasyon-arz-talep, confluence), p02 (talep-bölgesi-volume-profile, tweezer).
   Ortak iz: lejant "Demand Zone / Supply Zone / Bullish FVG / Bullish BOS", EMA 9/21/50/100/200, Swing Points; tablo sütunları D.Touch, D.Teyit, S.Touch, S.Teyit; "Price Action & Smart Money Analysis" başlığı (AVOD, KLMSN, GEDZA, PRZMA).
3. **Rejim / volatilite / likidite ailesi.** Üyeler: p04/36, 41, 05 (VRP), 04; p05/46, 48, 49, 50, 62, 68; p03 (xu100 ×3, skewness); p02 (şok freni, ters orantılı sizing, trend-rejim-HMM, denge/dengesizlik); p01 (endeks-5of5, fat-tail, bollinger); p06/97, 98, 113, 114, 124.
   Ortak iz: Corwin–Schultz 21 günlük (p03/M12, p05/62, p01 endeks notu), RV 21 gün (p04/05), v_t/Theta (p04/36), VIX (p06/98, 113, 114; p01 endeks), "sigma".
4. **Stat-arb / çift ve yeniden dengeleme ailesi.** Üyeler: p03/M1 (VAKBN–GARAN, kointegrasyon-sınırları), p05/51–55 (CIMSA–OYAKC, AGROT–GARAN ×4), p02/M6–M8, p04/37 + p02/M12 (GARAN/KGYO/CCOLA, volatilite harvesti), p01/K18 aşama 3.
   Ortak iz: üç panelli dashboard ("1) Fiyat Yakınlaşması", "2) Portföy Performansı", "3) Z-Skoru ve …"), Z ±2 kesikli çizgi, Buy & Hold kıyası, X = GARAN (Endeks/X), ".xlsx işlem logu", "T+1 Open".
5. **EMA sıkışma ve konsolidasyon-kırılım ailesi.** Üyeler: p05/65, 67, 68, 71, p06/106, 92, p05/44, p04/41, 18, p03 (AKFIS, düşen yapı ×2, 80-100 hafta), p05/56.
   Ortak iz: EMA 20/50/100/200 + "Son 130 Mum | 1 periyot | Tolerans %1.2 | Min 3 gün" başlığı (p05/65 ile 67 aynı araç, görsel doğrulandı); dinamik üst/alt kesikli bant + yeşil üçgen + sarı ortalama (p05/44 ile p04/41 aynı araç, görsel doğrulandı).
6. **Trend çizgisi / kanal motoru ailesi.** Üyeler: p02/M16, p03 (AEFES, düşen yapı ×2, BOM), p05/45, 64, p06/93, 103, 117, p04/32, 34, 35, 38, 40, 42, 43.
   Ortak iz: "Lookback N", "Temas: N", "Son Temas", "RETEST VAR (n kez)", "Direnç TL", "Destek Trendi". Değerler: Lookback 20 (LIDER), 30 (BALAT), 120 (AEFES); Temas 3 (LIDER, BALAT, AEFES 3/3), 5 ve 7 (BOM), 6 (AKSGY).
7. **Momentum liste / portföy optimizasyon ailesi.** Üyeler: p01/K11 (Clenow), K18, p02/M9, M10, M19, M20, M21, p05/63, p03 (CWENE skewness), p06/99, p04/33, p06/95, 96.
   Ortak iz: "momentum listesi" üzerine katman (skewness, alpha, ADX/CMF) → Markowitz → Max Sharpe; "DEY" (dönem en yüksek marjı) ölçüsü p04/33 ve p05/63'te aynı ad.
8. **Risk ve çıkış (ATR) ailesi.** Üyeler: p01/K13, p06/115, 125, 123, p02/M14, p05/48.
   Ortak iz: lot = risk / 2 ATR; acil stop giriş − 2 ATR; gün sonu stop; kısmi kâr %50.
9. **Temel / değerleme ailesi (strateji dışı, çapraz bağlı).** Üyeler: p01 (asuzu, beklenen-fk, 9aydan, fcfe-ddm), p04/25, 27, 28, 29, p05/77, 79–84, p02 (relatif değerleme, pddd-roe, ttrak, sektör rotasyonundan).
   Ortak iz: "kısa dönem 8 çeyrek / uzun dönem 36 çeyrek, IQR k=1.5" (p04/27, G) ile "36 çeyreklik PD/DD bandı" (p02/M11, A).
10. **Puan ve karar kartı ailesi.** Üyeler: p03 (AKFIS Skor 100/100, XU100 SETUP /100, Pair Quality /100), p06/98 (4/5), p01 endeks (5/5), p04/26 (1–5 puan, ağırlıklı).
   Ortak iz: "Sınıf / Skor / Karar" üçlüsü; formül hiçbirinde yok.

### Ek kanıt (ilk üç örneğe)

**Örnek 1, çift rotasyonu, eksik kapı: rejim ya da şok kapısı olabilir.**
- (G) FROTO Corwin–Schultz görselinde "Max Spread: 9.8494% (2025-04-14)" (p05/62). (G) v_t/Theta görselinde v_t Nisan 2025'te ≈4,3'e sıçrıyor, Theta ≈2,3 (p04/36, görsel doğrulandı). İki ayrı araç aynı ayda uç değer veriyor.
- (G) CIMSA–OYAKC portföyü ≈2025-01…05 nakitte (p05/51); VAKBN–GARAN portföyü ≈Haziran sonuna kadar 100k'da düz (p03/M1). İki çift aynı pencerede sinyalsiz. Çifte özgü bir kopuş yerine ortak bir kapı daha olası.
- (A) "Piyasa Şoku modu: yeni alım sinyalleri tamamen durur" (p02/M13).
- Hipotez: kapı = volatilite şoku freni ya da kointegrasyon sağlığı (ikisi birlikte olabilir). Güven: orta (3 G zaman uyumu + 1 A kural; kapı kimliği kanıtlanmadı).
- (G) VAKBN–GARAN raporunda "Cointegration p 0,048 — CURRENT", "Pair Quality 55,600/100", "Health GÜÇLÜ" (p03/M1): p değeri 0,05 sınırında. "CURRENT" durum etiketi birinci el; p02/M7'deki CANDIDATE…RETIRED listesinin kalanı Cevo'nun, doğrulanamadı.
- (G) AGROT–GARAN: test dönemi 2025-04-01 → 2026-04-23, 3 işlem; ilk işlem 2025-12-12 (p05/54 ile 52). Yani ≈8 ay işlemsiz. Aynı sessizlik üçüncü çiftte. p05/52 başlangıç tarihi yazmıyor (okunamadı).
- Sınama: v_t/Theta bandını ve CS spread'i BIST100 için üret; Nisan–Haziran 2025'te "şok açık" günlerde VAKBN–GARAN ve CIMSA–OYAKC girişlerini kapat; rapor tarihlerini (ilk işlem, nakit süresi) yeniden üretiyor mu bak. Dış bilgi (notlarda yok, doğrulanmadı): Mart 2025 sonunda BIST'te bir şok yaşandı.

**Örnek 2, EMA sıkışması, eksik tetik: ek parçalar.**
- (b, G) ICBCT kutusu "▲ AKTİF 3g" (p05/65) ile KRDMD başlığı "Tolerans %1.2 | Min 3 gün" (p05/67) aynı araç; üst çubuk her ikisinde "Son 130 Mum … 1 periyot". ICBCT aralığı (14,44 − 14,29) / 14,42 ≈ %1,04 ≤ %1,2: eşiği tutuyor. Yani "AKTİF 3g" = sıkışma ≥ 3 gün (görsel doğrulandı).
- (G) ICBCT çubuğunda "▲1 BULL ▼0 BEAR ⚡0 CONFLICT" sayaçları: araç sıkışmaya yön etiketi de koyuyor. Etiketin tanımı okunamadı.
- (a, G+G) KLMSN: p06/92 "Engulfing + EMA34 Tepki/Kırılım" (EMA5/8/13/34 sıkışık ≈30,7–31,2; Buy Signal üçgeni 24 Şubat; geniş yeşil mum 26 Şubat ≈30,5 → 33,7) ve p06/99 (aynı hisse, fiyat 34,54). Zincir: sıkışma → Buy Signal (24 Şub) → engulfing teyidi (26 Şub). Bu, p01/K8'deki "engulfing giriş zamanı yok" eksiğini dolduruyor: engulfing = sıkışma çıkışındaki teyit mumu (orta).
- (G) KRDMD sıkışmadan sonra Ratio ≈0,6 → ≈12 (p05/67): çıkış "EMA'lar açılırken" olur; ratio formülü (maks EMA − min EMA)/EMA200 p05'te önceki okumaya atıflı.
- Sınama: KRDMD 17.12.2025–14.01.2026 pencerelerini 4 EMA + %1,2 + 3 gün ile yeniden üret (20 gün, ort. %0,64); sonra "ilk uzun yeşil mum" ve "engulfing" tetiklerini ayrı ayrı karşılaştır; KLMSN 24–26 Şubat'ı fixture yap.

**Örnek 3, AB=CD: ek parçalar.**
- Stop/bozulma (b+A, orta): tablo satırı "Stop'a takılan / bozulan" (G, p04/03 ve p02/M1) iki kavramı tek sütunda topluyor. p01/abcd-geometrik: "C sonrası A aşılırsa pattern bozulur" (A). Hipotez: AB=CD'de stop = bozulma = C sonrası A'nın aşılması. Sınama: SMRTG'nin üç stop kaydı (2024-03-27 −%23,29; 2025-09-15 −%12,10; 2026-01-29 −%24,85) için A düzeyinden (A−C)/C hesapla; eşleşiyor mu bak.
- Getiri tanımı (d, orta): p04/A-EK, SMRTG getirilerini C'den D'ye fiyat düşüşü olarak yeniden üretti (kısa yön). p02/M1'de ISKPL aynı biçimli tabloyu veriyor (aynı araç). Hipotez: "getiri" sütunu |C→D|/C olabilir, yön bağımsız. ISKPL için C ve D yönünü fiyat verisiyle kontrol et; ISKPL'nin +%610'u BIST'te yapılamayacak kısa işlem içeriyor olabilir. (p02/M1 yönü yalnız çıkarım olarak yazmıştı.)
- Zaman çizgisi (a, G): SMRTG fiyatı 18 → 6–8 TL düşüyor, sağ uçta sert yükseliş (p05/48); p04/03 işlemlerinin 7'si "hedef" ve sonuncusu 2026-01-29 stop. Düşen hissede kısa C→D kazanır; son stop yükselişe denk gelir. Bu, +%305'in kısmen düşüş trendinin ürünü olduğunu düşündürür (orta; p05/48 eksen tarihi okunamadı).
- "Harmonik sayı" (b, orta): A1CAP "6.31 TL" (p01/K3, AB mesafesi ≈6,2–6,3) ve SMRTG "3.02 TL" (p04/01) aynı başlık alanı. Hipotez: alan = son AB bacağı uzunluğu (TL). Sınama: SMRTG'nin son AB bacağı 3,02 TL mi?
- Stop için ek ipucu: LUKSK "stop (X) 73,00" ve SAYAS "Bk Stop (X)" (G, p04/02, p01/K2): Gartley'de stop = X. AB=CD'de X yok; stop A olabilir (yukarıdaki hipotez).

### Eksik parça tablosu

| # | Modül | Eksik | Dolduran notlar | Hipotez | Güven | Sınama |
|---|---|---|---|---|---|---|
| 1 | X–B trend çizgisi kırılımı (p01/K1, K) | giriş fiyatı, stop, kapanış kuralı | p04/02 (SOKE "SAT (taktik KISA, D'ye kadar) — D'de AL'a döner"; LUKSK giriş = D = 86,95, stop (X) 73,00), p04/01 (DGATE "Kırılım: AŞAĞI yönde, 2026-08-18", D 49,66 AKTİF), p01/K2 (SAYAS giriş D, stop X) | Çizgi kırılımı giriş değil, bir durum: kırılım → "taktik KISA, D'ye kadar" → D'de TEPKI_VERDI ise AL, stop X. BIST long-only için kırılım = bekle. | yüksek (3 G tablo/etiket) | KAPLM (Haz kırılım → D 424 Temmuz sonu → tepki yok), DGATE (18.08.2026 → D 49,66), SOKE: durum geçişlerini tarihleriyle yeniden üret |
| 2 | D sonrası tepki penceresi (p01/K2, K) | 10 gün mü 20 bar mı; "belirsiz" ve "BOZULDU" eşiği | p01 §5 (KAPLM aynı çıktıda 20 bar + 10 gün), p04/01 ("[BOZULDU]", "TEPKI_VERDI"), p01/abcd-geometrik (A aşılırsa bozulur) | İki ayrı parametre: 20 bar = D sonrası tepki penceresi; 10 gün = C sonrası yön testi. BOZULDU = geometri bozulması (A aşıldı), TEPKI GELMEDİ = süre dolumu. | orta (G etiket + A kural) | SMRTG/KRPLS durum etiketli D'leri (TAMAM, BOZULDU) tarihleriyle üret; KAPLM'de 20 bar ve 10 gün ayrı say |
| 3 | AB=CD stop ve getiri yönü (p04/A-EK, p02/M1, K) | stop kuralı, yön | Bkz. "Ek kanıt, Örnek 3" | Stop = A aşılması; getiri = mutlak (C→D)/C | orta | SMRTG 3 stop, ISKPL 5 işlem fiyat kontrolü |
| 4 | Gartley oranları ve D formülü (p01/K2, p06/123) | oran tablosu yok (p01); 123'te D formülü ters | p06/123 (G tablo: B XA 0,618; C AB 0,382–0,886; D XA 0,786), p04/02 (SOKE "0.786: 12.53"; X≈10,23, A≈21,20: 21,20 − 0,786×10,97 = 12,58), p03/DOAS (B 0,786 XA, D 1,272 XA = Butterfly) | Standart: D = A − 0,786(A−X); 123'teki "X + (A−X)×0,786" yanlış yön. | yüksek (SOKE görseli ile hesap tutuyor) | SOKE, MAKIM (p06/122) D'lerini bu formülle yeniden üret |
| 5 | Hedef merdiveni (p01/K2 "TP2 çapası", p04/A) | TP2 A–D mi C–D mi; TP1 tanımı | p01/K2 (SAYAS TP2 ≈107 = D + 0,618(A−D)), p06/123 (TP2 = D + 0,618(A−D), TP1 %50 kapat), p04/43 (RYSAS 22,60/24,20/26,80 = A−D oranları), p06/109 (BALAT TP = D + r(C−D), r 0,382/0,618/1,0/1,272) | Hedef çapası araca ("Sistem") bağlı: Carney/Gartley ve AB=CD: A−D; Siyah Kuğu: C−D. Etiket "CD" tek başına güvenilmez. TP1 de değişir (SAYAS 1:1 R/R; 123: 0,382 AD). | orta (3 G ladder, her biri kendi aracında tutarlı) | SAYAS, RYSAS, BALAT/109 hedef rakamlarını her formülle üret; hangi formül hangi aracı tutturuyor |
| 6 | Butterfly stop (p03/DOAS, p06/123) | stop kuralı | p03/DOAS (D 159,40 < X 170,10; "1.618 (max risk): 146.00"), p06/123 ("X veya XA 1,13"), p06/109 (derin pattern: XA 1,13/1,27) | Butterfly'da D, X'in altında; stop X olamaz. Stop = XA uzantısı (1,618 "max risk" = 146,00). | orta (G etiket + 2 A) | DOAS: D 159,40 sonrası fiyat 146'ya vardı mı; 1,13 / 1,27 / 1,618 hangisi tarihli sonuca uyar |
| 7 | Three Drives (p03/M6, K) | işlem kuralı, oran toleransı, zaman toleransı | p01/abcd-geometrik (AB=CD mantığı), p04/40 (talep bölgesinde tepki), p06/111 (Fibonacci gün sayımı 5/8/13/21 takvim günü) | Drive 3 = D; tolerans AB=CD ile aynı; zaman simetrisi Fibonacci gün sayımı ile ölçülür. | düşük (iki farklı aktarım, ilişki dolaylı) | p03/M6 örneğinde A→D2 ve C→D3 bar sayısını (≈4 / ≈4) takvim gününe çevir; 5/8/13'e düşüyor mu |
| 8 | EMA sıkışması giriş tetiği (örnek 2) | tetik | Bkz. "Ek kanıt, Örnek 2" | Bağlam = sıkışma AKTİF; teyit = ilk uzun yeşil / engulfing; çıkış = ratio açılması | orta | KRDMD, KLMSN, ICBCT |
| 9 | Gizli filtreli breakout (p05/44, X) | iki filtre | p04/41 (aynı araç: dinamik bant + yeşil üçgen + sarı ortalama; hipotez: konsolidasyon uzunluğu kırılım şiddetini belirler), p03/80-100 hafta (uzun taban), p05/56 (Weinstein: taban, hacim kurur, hacimli kırılım), p03/AKFIS (range high) | Filtre 1 = kutu süresi (A→B uzunluğu). Filtre 2 bilinmiyor; hacim (taban sessiz, B'de hacim) adaydır. | düşük (araç eşleşmesi görsel doğrulandı, filtre kimliği tahmin) | 44'ün A→B süresini ölç; 41'in 6 üçgeninde kutu süresi ile sonraki yükseliş büyüklüğü ilişkili mi |
| 10 | Mavi çizgi, Tam/Defansif çarpan (p05/46, 48, 49, X) | formül, eşik | Bkz. "Gizli parametre ipuçları, 1" | Mavi seri fiyat–volatilite birlikte hareketini ölçer; gölgeli pencere mavi > 0 ile örtüşür | orta (araç ve gölge eşlemesi G), düşük (formül) | SMRTG: rolling korelasyon (getiri, Δ21g RV) üret; 48'deki Defansif pencereleri tutturuyor mu |
| 11 | Volatilite rejimi okları ve şok freni (p04/36, p02/M13, K/X) | pencere, eşik | p04/36 (görsel: v_t, Theta, gri bant; kırmızı üçgen v_t bandın altında, yeşil üçgen v_t bandın üstünde), p04/05 (RV 21d), p03/M12 ve p05/62 (CS 21g), p02/M13 ("son X gün / son bir ay") | "Bir ay" = 21 işlem günü (3 aracın ortak penceresi); şok = v_t gri bandın üstü; rehavet = bandın altı. "Son X gün" bilinmiyor. | orta (21 gün: 3 G; band kuralı: görsel okuma) | 36'daki üçgen tarihlerini (Nisan 2025 yeşil, 2024 başı ve Oca–Mar 2025 kırmızı) bant kuralıyla yeniden üret |
| 12 | VRP, IV proxy (p04/05, X) | proxy formülü, eşik | p02/M25 (iki motor: VRP + model-free varyans; "gerçek IV"), p04/05 başlık ("Log Contract • Constant Dollar Gamma Çerçevesi"), p04/04 (TSLA implied move %10,4: açık opsiyon sürümü) | "Log Contract" = model-free varyans (log kontrat) tabanlı proxy; RV = 21g. Eşik çizgileri okunamadı. | orta (G başlık + A) | BIST'te opsiyon zinciri yok; proxy'yi tanımlamadan "VOL SAT/AL" sıralaması sınanamaz. İlk adım: RV21 sıralamasını p04/05 görselindeki sırayla karşılaştır (HEKTS en düşük, YKBNK, ASELS) |
| 13 | Stat-arb momentum dönüş teyidi (p02/M6, X) | formül, "çarpan" | p05/51 (başlık "Momentum Dönüş Onaylı"), p05/54 (başlık "Dinamik Sinyaller", girişler Z 2,05 ve −2,01: eşik hemen aşılınca), p03/M1 (giriş Z −3,108, ΔZ +0,296: aşırıya gidip dönünce) | İki sürüm: ham ±2 girişi (AGROT–GARAN) ve ΔZ onaylı (CIMSA–OYAKC, VAKBN–GARAN). "Çarpan" = iki sürümün farkı olabilir. | orta (G başlık + G rakam) | Aynı çiftte (AGROT–GARAN) onaysız ve onaylı girişleri karşılaştır; Z 2,05 / −2,01 girişleri onaylı kuralla elenir mi |
| 14 | Sektör rotasyonundan hisse seçimi (p02/M23, X) | ölçütler | p04/06 (30/60/90 gün ilk 3 sektör, çalışan sürüm), p04/07 (anomali: mutlak 30g getiri > %50 dışla), p04/27 (8 / 36 çeyrek, IQR k=1.5), p02/M11 (36 çeyrek PD/DD + ROE), p01/K14 (aylık %70+) | Huni: sektör = 30/60/90 getiri sırası; "ucuz" = çarpan kısa/uzun dönem bandının altı; DuPont = ROE ayrıştırması; son adım = mevsimsellik. | orta | 30/60/90 çıktısındaki 2026-08-14 sektörlerinden başlayıp her sektörde ucuz hisse listesini üret |
| 15 | Relatif değerleme norm bandı (p02/M22, X) | band yöntemi | p04/27 ("KISA DÖNEM 8 çeyrek, UZUN DÖNEM 36 çeyrek, IQR k=1.5", ASUZU F/K 14,78x / 10,03x), p02/M11 (36 çeyreklik tarihsel PD/DD bandı) | Norm bandı = şirketin geçmiş çeyreklik çarpanlarının IQR (k=1,5) sınırları; kısa 8, uzun 36 çeyrek. | yüksek (G ile A aynı 36 çeyrek) | ASUZU 2023/12: sektör 7,60x, 14,78x, 10,03x ve hedef 91,33 / 177,61 / 120,53 yeniden üretilsin |
| 16 | 9 aydan yıl sonu kâr tahmini (p01/9aydan, girdi eksik) | kalan satış payı | p02/M23 ("satış mevsimselliği", X birebir) | Kalan çeyrek satışı = geçmiş yıllardaki çeyrek payı (mevsimsellik). Dikkat: bu satış mevsimselliğidir; p01/K14 fiyat mevsimselliğidir, ayrı kavram. | orta | ASUZU/FROTO 9A + mevsim payı ile yıl sonu tahmini; p05/79–80 hedefleriyle kıyasla |
| 17 | Rolling alpha ve skewness katmanı (p02/M19, X) | tanım | p03/M13 (63 gün, ±0,5 sınıf, >+1 kontrol), p02/M19 ("momentum listelerine uygulandı") | Skewness = 63 gün, sınıflar p03'teki gibi (G+X tweet). Rolling alpha tanımı yok. | yüksek (skewness), düşük (alpha) | CWENE 63 günlük skewness serisini p03 görselindeki ≈+1 (2024) / ≈−1 (2025 Mar–Haz) ile karşılaştır |
| 18 | "Satılık değil" boru hattı (p02/M20, X) | ANN, ADX/CMF eşikleri, mum tanımları | p02/M8 (ML 9/13, %69,23: araç konsolu), p04/22 (MLP Sinir Ağı), p05/K-05-26 ve p01/K8 (mum kodları: gölge hesabı, engulfing), p06/117 ("ADX 20" çizgisi), p06/98 (ADX ≥ 25) | "ANN momentum" = p02/M8'deki ML modeli (ad farkı); çekiç/sabah yıldızı p05/76'daki gölge hesabına dayanır; ADX eşiği 20–25 arası, iki görsel çelişiyor. | düşük (3 dolaylı eşleşme) | ML konsol çıktısındaki 14 gün sinyalini pipeline ilk aşama çıktısıyla karşılaştır; ADX 20 ve 25 ayrı dene |
| 19 | HalfTrend "buy" + momentum eşiği (p01/K9, K zayıf) | iki gösterge, eşik | p05/46 (görsel "Mom Eşiği (0.15)"), p05/48 (mor noktalı eşik ≈+0,2) | Kodda "momentum_threshold" ile görselde "Mom Eşiği" aynı kavram olabilir (eşik 0,15–0,2). Ama 46/48'deki seri fiyat–vol aracı (satır 10); HalfTrend bağı kanıtsız. | düşük (yalnız ad benzerliği) | HalfTrend kartı Tansu'ya atfı doğrulanana kadar çıkar; eşik 0,15 yalnız "Mom Eşiği" notu olarak kalsın |
| 20 | MA yön filtresi (p01/K10) | MA türü ve periyodu | p03/M11 (G: "WMA Close 21", XU100 1 Eylül "WMA21 altında"), p06/113–114 (SMA 20/50), p06/98 (SMA 18/35), p06/115 (250 gün) | Endeks yön filtresi = WMA21 (birinci el). Hisse için tek periyot yok; aynı piyasaya üç farklı çift (18/35, 20/50, WMA21) var. | orta (endeks), düşük (hisse) | XU100 için WMA21 üstü/altı filtresini 2025–2026'da çalıştır; SETUP puanı 45/100 gününü ve 1 Eylül notunu üret |
| 21 | Endeks 5/5 skor (p01/K15, X) | beş bileşen, eşikler | p06/98 (7 kutu, 4/5, "DİKKATLİ İYİMSERLİK", VIX < 16,99 güvenli, ADX 25), p03/M11–M12 (SETUP /100, CS), p06/113–114 | Aynı sistem türü ("Full Long" ↔ "Dikkatli iyimserlik"). Bileşen adayları: ADX, RSI, VIX, NH-NL, CS. Eşik uyumsuzluğu var (Çelişki 7). | düşük | Aynı gün için 98'in 7 kutusunu üret; 4/5 nasıl toplanıyor (hangi 2 kutu düşürüldü) |
| 22 | Bollinger / SD bantları (p01/K12, X) | k, periyot, giriş/çıkış | p06/97 (−1SD al, −2SD stop, IV), p06/127 (alt istatistiksel bant + hacim + OBI), p02/M4 (%68, 2SD/3SD'de dönüş artar), p01/K12 (±1/2/3 SE görsel) | Çekirdek ortak: normal dağılım bantları, "aday olay". −2SD bir notta stop, ötekilerde dip: kural çıkarılamaz. | düşük (çelişen aktarımlar) | Hiçbir kural yazma; z ≤ −2 olaylarını "aday olay" olarak say, getiri dağılımına bak |
| 23 | ATR lot ve stoplar (p01/K13, K) | "2 TL" okuması, gün sonu seviyesi, ATR pencere | p06/115 (G: 100.000$, %1, "14.30$ 2 ATR için", 1.000/14,30 ≈ 70 hisse; gün sonu = 250 günlük ortalama altı kapanış), p06/125 (STOP 104,34 / ATR 4,62), p02/M14 | 2 TL = 2 ATR mesafesi (250 lot). Gün sonu stop = 250 günlük ortalama. ATR periyodu hâlâ yok. | yüksek (G; 115 NotebookLM infografiği, aracın kendisi değil) | 125'teki STOP 104,34 = giriş − 2×4,62 → giriş ≈113,6 mı; ATR(14) ile 4,62'yi üret |
| 24 | Kısmi kâr ve iz süren stop (p06/125) | oranlar | p06/123 (TP1'de %50), p06/109 (TP1'de kısmi kâr, stop girişe), p06/125 (+1,5 ATR trailing; önceki gün dibi altı kapanışta %50) | TP1'de %50 kapat, stop girişe; +1,5 ATR'de trailing; ikinci %50 önceki gün dibi altı kapanışta. | orta (3 aktarım uyuşuyor, 123 G) | BALAT 109 TP1 84,88 sonrası zinciri uygula |
| 25 | Fib 0,618 bölgesi + H4 Order Block (p01/K5, X) | çapa, OB, tetik | p06/105 (BOS → HH → Fib çapası swing low→high; 0,618–0,786; FVG/OB teması; stop Fib 1,0; TP1 Fib 0), p04/20 (sponsor candle = sert hareket öncesi son zıt mum = OB), p05/69 (1H/4H CHoCH teyidi), p06/99 (4H BOS haritası) | p01/K5 = p06/105 zinciri; OB = sponsor candle; teyit = alt zaman dilimi CHoCH. | orta | 105'teki Fib değerleri (216,77 / 175,60 / 150,15) yeniden üretilsin |
| 26 | ACSEL VAL hedefi (p01/K6, X) | VAL, profil | p02/M3–M4 (VAL altı sarkma + value'ya dönüş → POC; VA %68), p01/ACSEL lejant "Gaussian VP", p06/66 (POC 29,71 / VAH 30,24 / VWAP 28,00) | Fiyat value'nun altında; direnç aşılırsa value'ya giriş = VAL hedefi, sonra POC. "Gaussian VP" yumuşatılmış profil; VA %68 = ±1σ. | orta | ALKIM 66'daki POC/VAH'ı günlük OHLCV ile yaklaşık profil kurup karşılaştır (yaklaşık, etiketle) |
| 27 | "Kaliteli formasyon + bölge" kapısı (p01/K17, X) | çakışma ve kalite tanımı | p03/AKFIS ("BULLISH FVG + CONFLUENCE", "Sınıf: A+, Skor 100/100"), p04/21 ("Talep+HSAR Kesişimi"), p06/120 (çoklu aralık Fib kümeleri), p04/09 (distal/proximal) | Çakışma = iki bölge kutusunun fiyat aralığı kesişimi boş değil; kalite = araç "Sınıf" etiketi (A+). | orta (G etiket; formül yok) | AKFIS: FVG ≈3,64–3,69 ile range high 3,64 kesişimi; sınıf A+ eşiğini 2. örnekle (alıntı, ≈114) karşılaştır |
| 28 | Elliott dalga geri alımı (p01/K4) | hangi oran, tetik | p06/102 (G: "ELLIOTT WAVE 4 (Fibo: %54.0)"), p06/107 (Wave 2 %50–78,6), p03/M10 (CWENE: dalga 1 33,10 → 48,30, dip ≈35) | 0,24/0,38/0,50 merdiveni araçta sabit değil; araç gerçek oranı yazıyor (%54). CWENE dalga-2 geri alımı (48,30 − 35)/15,20 ≈ %87,5, 107'nin %78,6 sınırının dışında. | orta | 107 kuralını BRYAT (%64,3) ile dene; CWENE'yi 107'nin fixture'ı yapma |
| 29 | Mum dedektörleri: Tweezer, Doji, Advance Block (p02/M18, p05/70–71, p04/12) | tolerans, eşik | p05/76 (G kod: upper_shadow, lower_shadow), p01/K8 (G kod: engulfing), p04/12 (not: 3 mum, küçülen gövde, uzayan üst fitil) | Hepsi p05/76'daki gölge hesabı + p01/K8'deki kod biçimiyle yazılır. Eşik (gölge/gövde) hâlâ yok. | orta (iki G kod, aynı stil) | Gravestone (p05/70) ve DOAS advance block için üst gölge / gövde oranını ölç; eşik önerme, dağılımı raporla |
| 30 | Siyah ve Beyaz Kuğu (p04/J, X) | oran tanımı | p04/35 ("Beyaz Kuğu", "D (CD=1.0AB)"), p04/34 (LIDER "Harmonik: Siyah Kuğu"), p06/109 (BALAT Siyah Kuğu: TP = D + r(C−D)), p05/45 (BALAT "D(CD=1.27AB)") | Beyaz = eşit bacak (CD = 1,0 AB); Siyah = uzatılmış (≈1,27). | düşük (dolaylı) | BALAT 109 (D ≈81,4) ve 45 (D 74,00) için CD/AB oranını ölç |
| 31 | Gizli pozitif uyumsuzluk osilatörü (p05/74, X) | osilatör kimliği | p05/60 ("Swing=15 sol-only, MinGap=15"), p05/61, p03/AHENK (WaveTrend benzeri panel), p03/M11 (WT 10 21 parametreleri), p05/74 görseli (alt panel: iki çizgi + histogram) | Osilatör WaveTrend ailesi olabilir; geometri ve pivot parametresi 60'tan. 60'taki "≈0,21 seviyeli çizgi" WT ölçeğine (±60) uymuyor. | düşük | Swing=15 sol-only ile 74'teki DIV işaretlerinin tarihlerini üretmeyi dene; WT(10,21) ve RSI iki aday |
| 32 | Fiili dolaşım taramaları (p01/K16, X) | tarama içeriği | p04/08 (40 satır tablo; KENT %0,54 … GARAN %13,98), p01/fiyat-hacim-üçgeni, p03/M7 ("iki tavan") | "Strateji" = float turnover = hacim / fiili dolaşım. BOM ile bağ yok sayılır (kanıt yok). | düşük | KAP fiili dolaşım serisi yoksa geriye dönük test yapılamaz; yalnız canlı filtre |
| 33 | Skor ve sınıf formülü (p03: AKFIS, XU100, Pair Quality; p01/K15) | formül | p03/not-backtest (aday tipleri: "Daily iyi + 4H bullish CHoCH + RS güçlü + Demand/FVG desteği"), p06/98 (4/5 + etiket), p04/26 (1–5, ağırlıklı) | /100 skoru = bileşen puanlarının ağırlıklı toplamı; bileşenler not-backtest'teki aday tipi listesi. Hepsi yeşil olmak zorunda değil (p06/98: AO negatif, hacim düşük, yine 4/5). | düşük | AKFIS ve XU100 için bileşenleri ayrı puanla; 100/100 ve 45/100 tutuyor mu |

### Gizli parametre ipuçları

1. **Mavi çizgi (p05/46, 48, 49).** Görsel doğrulandı: üç görsel aynı aracın çıktısı. Ortak: mavi düz çizgi (sol eksen), turuncu noktalı çizgi (sağ eksen), mor noktalı eşik ("Mom Eşiği (0.15)" 46'da; 48'de ≈+0,2), kırmızı kesikli "Kırılma Eşiği (0.0)", altta "Pozisyon Büyüklüğü Çarpanı (Tam/Defansif)" basamak çizgisi.
   - Gölgeli pencere mavi serinin sıfır üstündeki dönemlerine denk geliyor: 49'da gölge ≈x255–430 aralığında mavi sıfırın üstünde, mavi sıfırı aşağı kestiğinde gölge bitiyor ve fiyat sağlıklı yükseliyor; 48'de gölgeler mavinin sıfır üstündeki iki döneminde; 46'da mavi sıfırı yukarı kestiği anda gölge başlıyor ve alt basamak çizgisi aynı aralıkta alçak. Gölge rengi üç görselde farklı (kırmızı, pembe, yeşil): renk anlamı okunamadı.
   - 48'de basamak çizgisi mavi < 0 iken de alçak kalıyor (x≈260–385): "mavi > 0 ⇒ Defansif" tam kural değil; çıkış koşulu (turuncu ya da gecikme) okunamadı.
   - Hipotez: mavi = fiyat getirisi ile volatilite değişiminin birlikte hareketi (rolling korelasyon benzeri; değer aralığı −0,2…+0,3 buna uyar, ama doğrulanmadı); p05/48 notundaki "fiyatla volatilite birlikte artarsa kötü" ile uyumlu. Güven: orta (araç ve gölge eşlemesi) / düşük (formül).
   - Sınama: SMRTG günlük verisinde rolling korelasyon(getiri, Δ21 günlük RV) hesapla; 48'deki iki Defansif pencereyi (fiyat ≈11→14 TL ve ≈8,5→11,5 TL yükselişleri) tutturuyor mu.
2. **ICBCT "Pre Signal" (p05/65).** Açık sürüm KRDMD (p05/67): EMA20/50/100/200, tolerans %1,2, min 3 gün, 130 mum, ratio = (maks EMA − min EMA)/EMA200 (önceki okuma). ICBCT'de eşik tutuyor (≈%1,04). Gizli kalan: "Pre Signal" oku ve BULL/BEAR/CONFLICT tanımı (okunamadı). "Parametreleri açıklayamam" cümlesi (A, p05/65) çoğunlukla bu iki öğe için geçerli; sayısal parametreler zaten KRDMD görselinde açık. Güven: yüksek (sıkışma parametreleri), düşük (Pre Signal).
3. **Gizli filtre 44 (p05/44).** p04/41 aynı aracın daha çok örnekli sürümü: sarı ve cyan kesikli dinamik bantlar, yeşil üçgen, kahverengi ortalama; 44'te üst/alt bant ve sarı ortalama aynı. p05/71 "Donchian benzeri turuncu kesikli kanal" da aynı aile. Bant uzunluğu ve filtreler okunamadı. 41'de üçgenler konsolidasyon tabanında; üçgenin kırılım anı mı, kutu başı mı olduğu okunamadı. Güven: orta (aynı araç), düşük (filtre kimliği).
4. **Gizli pozitif uyumsuzluk (p05/74 ↔ 60, 61).** Açık parametre yalnız p05/60'ta: "Swing=15 sol-only | MinGap=15". 74'te osilatör adı beyazla kapatılmış; alt panel: iki çizgi + histogram. 74'teki "Getiri: +63,4%, β = 0,132" etiketi ile p06/108 beta infografiği arasında bağ var mı bilinmiyor.
5. **"Swing=15" ve pivot ayarı.** Hiçbir harmonik notunda pivot ayarı yok. Açık değerler başka araçlarda: Swing=15 (p05/60), Lookback 20/30/120 (kanal motoru). Hipotez: harmonik pivot ayarını SMRTG'nin 12 C tarihi ve ISKPL'nin 5 C tarihi üzerinden geriye çöz (hangi L/R pencere bu tarihleri üretiyor). Güven: düşük (hipotez), sınama değeri yüksek.
6. **Düşen direnç / kanal motoru (p03/AEFES, p04/34, p05/45).** Temas ≥ 3 aday asgari değer: LIDER 3, BALAT 3, AEFES 3/3; hiçbir görselde 3'ün altı yok (BOM 5/7, XU100 7/8). Lookback araca göre 20, 30, 120. Güven: orta.
7. **Kümülatif delta (p04/32, 45).** Lejant "Kum. Delta" günlük grafikte duruyor; günlük OHLCV ile tick delta olmaz, araç bir yaklaşım kullanıyor. Hesabı okunamadı.
8. **SETUP / Skor puanı (p03).** Formül hiçbir görselde yok; p06/98'de bileşenler açık (7 kutu) ama toplama kuralı yok.
9. **İşaret sözleşmesi (açık).** Z > +2 ⇒ X AL: VAKBN–GARAN (X = GARAN), AGROT–GARAN (X = GARAN), CIMSA–OYAKC ("Aşırı Ucuz CIMSA Sınırı (+2.0)"). Üç görselde tutarlı (p05/52'de belirtilmişti).

### Çelişkiler (hangisi esas)

1. **SMRTG yönü.** p04/03 notu "Yükseliş" diyor; p04/A-EK getirileri C'den D'ye düşüş olarak yeniden üretti. Esas: görsel + hesap (aşağı yön). ISKPL için yön henüz doğrulanmadı (p02/M1 çıkarım).
2. **TP2 çapası.** SAYAS etiketi ".618 AD" (07.10 okuma düzeltmesi; ilk okuma "CD" idi) ve hesap A–D üzerinden tutuyor (p01); BALAT 109 gerçekten C–D üzerinden (p06). Esas: araç başına ölçüm.
3. **TP1.** SAYAS "1:1 R/R" (p01) ile p06/123 "AD'nin %38,2'si". İki ayrı sistem (Carney / Excel tablo). Esas: kendi görselinden okunan sistem.
4. **Gartley D formülü.** p06/123 tablosu ile SOKE (p04/02). Esas: SOKE görseli; tablo yön hatalı (satır 4).
5. **10 gün / 20 bar.** p01/K2 ayrı parametre (satır 2). Esas: KAPLM görselinin kendisi.
6. **Stop: R/R mi, yapı mı.** p02/M5 "stop R/R'ye göre" ve Cevo düzeltmesi. G örnekleri: SAYAS stop X, GUBRF R/R 1:2,27 stop çizilmeden sonradan hesaplanıyor (p05/58); p06/123 "R:R < 1,5 ise reddet". Esas: stop yapıdan, R/R kapı (red koşulu). Güven: orta.
7. **VIX eşiği.** p06/98: VIX < 16,99 "GÜVENLİ"; p01 endeks notunda VIX 20,6 iken skor 5/5 ve "Full Long". İki sistem aynı eşiği kullanamaz. Esas: yok; p06/98 birinci el ama NotebookLM çıktısı; p01 notu aktarım. İkisi de eşik olarak alınmasın.
8. **SMA çiftleri.** p06/98 SMA 18/35; p06/113–114 SMA 20/50; p03 WMA21; aynı XU100 (≈11.300–11.500, Aralık 2025: 98'de fiyat 11.336, p05/68'de KDE 11.292, 114'te dönem sonu ≈11.500). Esas: kendi aracının görseli (WMA21, p03); NotebookLM şablonlarındaki 18/35 ve 20/50 parametre sayılmaz.
9. **Bollinger / −2SD.** p06/97 "−2SD stop"; p06/127 "alt banda inen geri dönmek zorunda"; p02/M4 "2SD/3SD'de dönüş olasılığı artar"; p01/fat-tail "Herkesin olduğu yerde para yoktur". Esas: X bağlantılı birebir metin (Bollinger notu) kural içermiyor; hiçbiri kural olamaz.
10. **Temel analiz önemsiz mi.** p02/sirket-degerlendirme ("BIST'te temel değerlendirmenin önemi kalmadı", atıf belirsiz) ile p01/asuzu ve beklenen-fk (X bağlantılı birebir değerleme). Esas: X bağlantılı notlar.
11. **Likit mi, düşük fiili dolaşım mı.** p02/M15 sığ hisselerden uzak dur; p01/K16 fiili dolaşım < %30 taraması. İkisi ikinci el. Katman farkı: evren üretimi ile işlem kapasitesi. Esas: yok; ikisini ayrı filtre say.
12. **AGROT–GARAN iki özet (+%13,44, 20.04; +%8,76, 23.04).** Çelişki değil, ardışık görüntüler (üç günde −4,7 puan). Esas: p05/54 (dönem aralığı yazılı). p05/52'nin başlangıç tarihi okunamadı.
13. **Birinci el / not hatası (hep görsel esas).** ISKPL 3. işlem 2025-03-21 (p02), TOASO PD/DD 2,30 (p02), HKTM +12,62 (p04/07), FROTO ort. spread %1,7990 (p05/62), BALAT kırılım 2026-05-15 (p05/45), takvim günü sayımı (p06/111), OZATD satırı yok (p04/08).
14. **Elliott 4. dalga ≤ %50 mi.** p01/K4 merdiveni (0,24/0,38/0,50) ile ENJSA %54,0 (p06/102 G). Esas: görsel; merdiven üst sınır değil.
15. **Siyah Kuğu D oranı.** p04/34 etiketi ile BALAT 45 (1,27) ve 109 aynı hissede farklı tarihler. Esas: yok; oran doğrulanamadı.
