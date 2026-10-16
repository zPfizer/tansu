# D. Çift (pairs) / Portföy / Piyasanın Nabzı — Kural Çıkarımı

Kapsam: Tansu X Veri Havuzu notları + görseller. Görsel yolu kökü: `beyin/kisisel/300-Projects/Tansu X Veri Havuzu/assets/`.
Etiketler (kaynak türü tanımları GLOSSARY'dedir): **GÖRSEL** = görselde okundu (birinci el; NotebookLM görseli de birinci eldir, "NotebookLM görseli" etiketi yalnız bilgi verir), **Ham** = notun `## Ham` bölümü (birinci el), **NOT** = notun Ham dışındaki bölümleri (ikinci el), **YORUM** = benim çıkarımım / boşluk. Hiçbir parametre sessizce uydurulmadı.

Genel uyarı: Tansu kod, formül, pencere, maliyet, OOS vermiyor. Görseller düşük çözünürlüklü.

---

# BÖLÜM 1 — Çift / göreli değer rotasyonu

## Çift sistemi çekirdeği (Z-skor spread, ±2 giriş, momentum dönüş onayı, T+1 Open)
- **Kaynak:** kaynak-vakbn-garan-rotasyon-2096358189696520213 (rapor.webp, grafik.webp); gorsel-paket-51 (01-cimsa-oyakc-rotatif-portfoy-zskor.jpg); -52 (01,02,03 png); -53 (01 jpg); -54 (03-stat-arb-sistem-ciktilari.png; GÖRSEL: 01/02 görseller etiketsiz mum grafikleri); -55 (01 png); tweet-stat-arb-momentum-donus-teyidi-kar-carpani; kaynak-kointegrasyon-sinirlari; tweet-rolling-cointegration-iliski-bozulma-kapisi; tweet-istatistiksel-arbitraj-150bin-esbutunlesme-taramasi.
- **Tansu'nun ifadesi (GÖRSEL, birebir etiketler):**
  - "RELATIVE VALUE ROTATION | VAKBN <-> GARAN"; "SON GUN: YENI AL SINYALI | VAKBN AL | Y goreli ucuz, Z donusu +0.30".
  - Grafik: "GARAN (X)", "VAKBN (Y)", "Strateji", "50/50 Buy&Hold", "Z-Score", "GARAN AL", "VAKBN AL", "Rolling Corr", "Rolling Beta"; paneller "Normalize Fiyatlar", "Portfoy Performansi", "Z-Score ve T+1 Open Islemler", "Pair Health: Rolling Correlation ve Beta".
  - 51: "CIMSA (X)", "OYAKC (Y)", "Relatif Momentum Portoyu", "Buy & Hold (50/50)", "3- Z-Skoru ve Momentum Donus Onayli Islemler | SON GUN: YENI AL SINYALI", "Asiri Ucuz CIMSA Siniri (+2.0)", "Asiri Ucuz OYAKC Siniri (-2.0)", "OYAKC Tutulan Donemler", "CIMSA Tutulan Donemler" (görselde Türkçe karakter yok).
  - 52: "STAT-ARB ÖZETİ | AGROT ↔ GARAN", "Durum: AKTİF LONG (AGROT Ucuz)"; log: "AGROT SAT, GARAN AL", "POZİSYON KAPAT (Nakit)", "AGROT AL, GARAN SAT".
  - 54: "GARAN (Endeks/X)", "AGROT (Hisse/Y)", "Stat-Arb Stratejisi", "Z-Skoru ve Dinamik Sinyaller", "AGROT SAT GARAN AL" (Z≈+2), "AGROT AL GARAN SAT" (Z≈-2); "İŞLEM GEÇMİŞİ (Excel'e Kaydedildi: StatArb_Islem_Logu_AGROT_GARAN.xlsx)".
  - 55: "İstatistiksel Arbitraj Backtest | AGROT.IS & GARAN.IS", "Spread Z-Skoru". Grafikte ±2 çizgilerinin yanında soluk ±0,5 çizgileri var (GÖRSEL).
  - Tweet paraphrase (Ham, tweet-stat-arb-momentum-donus-teyidi-kar-carpani): "stat-arb sisteminde momentum dönüş teyidi kârlarda çarpan etkisi yaratıyor; deneyleri ileride anlatacağım; momentum trader sisteme farklı bakar." Sayı yok.
  - Tweet (Ham): 150.000 kombinasyona kadar eşbütünleşme taraması. Tweet (Ham): tek seferlik test bozulan ilişkiyi kaçırır, rolling izle. Tweet (Ham, kaynak-kointegrasyon-sinirlari): Engle–Granger/Johansen; yüksek korelasyon ≠ durağan spread.
  - 54 notunun "kaynak açıklaması" (Ham, gorsel-paket-54-stat-arb-pairs-trading-kanonik-aciklama): ucuz bacak long, pahalı bacak short; Z ±2 giriş; Z ~0,5 çevresine dönüşte çıkış.
- **Tanım (hesaplanabilir):**
  1. X = referans bacak (GARAN; 51'de CIMSA), Y = diğer bacak (VAKBN / AGROT / OYAKC). Seri sırası = grafik etiketi (GÖRSEL).
  2. Spread: `ε_t = log(Y_t) − α − β·log(X_t)` ve `Z_t = (ε_t − ort)/std` (rolling). Bu **YORUM**: Tansu formül vermedi. Rapor "Beta" ve "Rolling Beta" gösterdiği için hedge oranlı kalıntı en olası aday. Alternatif: log oran. Hangisi olduğu bilinmiyor.
  3. Yön anlamı (GÖRSEL, 3 pair'de tutarlı): Z > +2 → Y pahalı, X ucuz → X'i tut (GARAN AL / CIMSA AL / AGROT SAT-GARAN AL). Z < −2 → Y ucuz → Y'yi tut (VAKBN AL / OYAKC AL / AGROT AL).
  2b. Z-dönüşü (GÖRSEL, hesaplandı): rapor "Son Z −3,108", "Önceki Z −3,404", başlıkta "Z dönüşü +0.30". −3,108 − (−3,404) = +0,296 ≈ +0,30. Yani **Z dönüşü = ΔZ_t = Z_t − Z_{t−1}**. Bu, görselden doğrulanan tek net "momentum dönüş" tanımıdır.
  4. "Momentum dönüş onayı" (YORUM, ΔZ tanımı üzerine): Alt uçta `Z ≤ −2 ve ΔZ > 0` → Y AL. Üst uçta `Z ≥ +2 ve ΔZ < 0` → X AL. Grafikte işaretler Z'nin yerel tepe/dibinde (dönüşte) duruyor; bu kurala uyar (GÖRSEL, 51 ve VAKBN grafik; 55'te AL/SAT işareti yok). K/M gün sürekliliği veya tampon (buffer) görünmüyor.
  5. Emir: "T+1 Open" etiketi (GÖRSEL) → sinyal t kapanışında, işlem t+1 açılışında.
   6. YORUM: bu katalogdaki rotasyon seçimi ilk sinyale kadar nakit, sonra tek hissede kalmadır. VAKBN grafiğinin başlangıçtaki yatay eğrisi nakitle uyumludur; ısınma veya başlama koşulu da olabilir, genel nakit politikasını açıklamaz (GÖRSEL, kaynak-vakbn-garan-rotasyon-2096358189696520213/02-vakbn-garan-rapor-2.jpg). Grafikte 6 AL etiketi vardır.
  7. İki bacaklı sürüm (AGROT/GARAN): giriş Z≥+2 / ≤−2; çıkış nakit "POZİSYON KAPAT" Z=0,37 (GÖRSEL log). Çıkış eşiği ±0,5 olabilir (55 grafiğinde ±0,5 soluk çizgiler GÖRSEL; 54 notu "~0,5" Ham). Çıkış zaman aşımı/stop görünmüyor.
  8. Eski sürüm (AGROT/GARAN, Nisan 2026) **momentum onaysız**: Z=+2,05'te girdi, Z sonra ≈3'e çıktı (GÖRSEL 54 grafik). İkinci giriş Z=−2,01 iken Z −2,54'e kadar kötüleşti (GÖRSEL 52 tablo). Yani eşik geçişinde ilk gün giriş. "Momentum dönüş onaylı" 51/VAKBN sürümleri daha yeni (YORUM).
- **Parametreler:**

| parametre | değer | kaynak |
|---|---|---|
| Giriş eşiği | \|Z\| ≥ 2 | GÖRSEL (51,52,54,55,VAKBN grafik) |
| Çıkış eşiği (iki bacaklı) | Z=+0,37'de kapandı; ±0,5 çizgisi | GÖRSEL (log, 55) / Ham (54: "~0,5") |
| Z dönüşü | ΔZ=Z_t−Z_{t−1} | GÖRSEL (hesapla uyuştu) |
| Dönüş onay ek koşulu (K/M, tampon) | yok / bilinmiyor | Ham tweet: ayrıntı "birileriki safhada anlatacağım" |
| Emir zamanı | T+1 Open | GÖRSEL (VAKBN grafik başlığı) |
| Z penceresi | VAKBN, CIMSA ≈ 60 işlem günü (Z serisi veri başlangıcından ~3 ay sonra başlıyor); AGROT/GARAN ≈ 120–126 gün (Z, 2025-04-01 veri başlangıcından ~6 ay sonra başlıyor) | YORUM (grafik başlangıç gecikmelerinden tahmin; pair'e özel olabilir) |
| Rolling corr penceresi | ≈ Z ile aynı başlangıç (~60 gün) | YORUM |
| Rolling beta penceresi | ≈ 30 gün (beta çizgisi daha erken başlıyor) | YORUM, düşük güven |
| Spread tanımı / hedge | bilinmiyor | YORUM |
| Hedge oranı (AGROT/GARAN) | long AGROT ≈ 0,97×NAV (±0,04), short GARAN ≈ 0,38×NAV (±0,06) | YORUM, regresyon: 52'nin 29 günlük PnL tablosundan (R²=0,96; NAV farkı PnL ile tam uyuşuyor). Yani 1:1 TL değil, yaklaşık 1 : 0,4. Oran beta temelli olabilir. |
| Başlangıç sermayesi | 100.000 TL | GÖRSEL |
| Maliyet | VAKBN raporunda "Toplam Maliyet 2.054,78 TL" (6 geçiş); formül yok | GÖRSEL |

- **Giriş / çıkış / sağlık kapıları:**
  - Giriş: yukarıdaki Z + dönüş. Çıkış: iki bacaklı → |Z|≤~0,5 nakit; rotasyon → ters uçta diğer hisseye geçiş.
  - Sağlık (GÖRSEL, rapor.webp): "Rolling Corr 0,731", "Beta 1,675", "Beta CV 0,277", "Half-Life" (boş, birim "Gun"), "Cointegration p 0,048 — CURRENT", "Pair Quality 55,600 /100", "Pair Health GUCLU". Pair Health panelinde corr (sol eksen 0,4–0,8) ve beta (sağ eksen 0,257–2,107); altta etiketsiz kırmızı noktalı yatay çizgi (corr ≈0,35–0,4 civarı: olası alt kapı, YORUM, düşük güven).
   - Eşikler ve işlem engelleme mantığı yoktur (GÖRSEL, kaynak-vakbn-garan-rotasyon-2096358189696520213/01-vakbn-garan-rapor-1.png). YORUM: 55,6 ile GÜÇLÜ eşleşmesi bu katalogda açıklama adayıdır; tek örnekten yeterlilik eşiği çıkmaz. Pair Quality formülü ve bantları açık değildir.
  - Kapıların işlediğine dair ipucu: VAKBN grafiğinde Z ≈ −2,3'e indi ve döndü (Mar–May 2025), fakat sinyal yok. Neden bilinmiyor (kapı/ısınma/başka kural) — YORUM.
  - 54 notu (NOT, ikinci el, Claude): DEGRADING/SUSPENDED yaşam döngüsü, FDR, rolling gate. Bunlar Tansu'nun değil, Claude önerisi.
- **Belirsiz kalanlar:** spread tanımı (log oran mı, β'lı kalıntı mı), β nasıl bulunuyor (rolling OLS? sabit?), Z penceresi, ortalama/std kaynağı, half-life boş, p-değeri hangi test ve hangi pencere, Pair Quality formülü, Pair Health bantları, onay kuralının tam biçimi, çıkış eşiği kesin değeri, nakde dönme koşulu rotasyonda var mı, T+1 Open'ın PnL'e gerçekten uygulanıp uygulanmadığı (52 tablosunda giriş günü state=1 ve PnL=0: giriş kapanışta mı açılışta mı belirsiz), VAKBN grafiğinde Z'nin Ağustos 2025 ortasında (eksene göre) tek günde ≈−2,5'ten +4'e sıçraması (veri/temettü/bölünme hatası mı?), 2026-04-20 PnL kayması, çift sayısı.
- **Tansu'nun kanıtı (tüm sayılar, GÖRSEL):**
  - VAKBN↔GARAN (tarih: grafik ~Oca 2025–Eyl 2026, dönem ucu yok): 100.000 → 152.862,86 TL; net K/Z 52.862,86; toplam getiri +%52,86; 50/50 B&H +%20,88; "Benchmark Farkı +31,99" (yuvarlak sayı 31,98); Max DD −%27,44; Sharpe 0,929; Sortino 1,338; CAGR +%28,93; geçiş 6; maliyet 2.054,78 TL; piyasada kalma %72,27; son Z −3,108, önceki −3,404.
  - CIMSA/OYAKC (grafik ~Oca 2025–May 2026): "Net: +49,245 TL (+49.2%)" (başlık, etiket; B&H sayısı yok, grafikte B&H çok altında).
  - AGROT/GARAN iki sürüm: (a) 2026-04-20: 100.000 → 113.436,14; +%13,44; B&H +%0,91; 3 olay; işlem 1 (kapalı, −7.645,35 TL / −%7,65, 66 gün) + nakit 21 gün + açık (+21.081,49 MTM, 42 gün). (b) 2025-04-01..2026-04-23: strateji +%8,76; B&H −%3,55; 3 işlem; güncel Z −0,91. (c) Negatif örnek (53): pair/dönem verilmemiş; strateji ≈79 bin TL'ye düşüp yatay (≈−%21, görsel tahmin); B&H ≈105–107 bin; Tansu sözü (Ham, gorsel-paket-53): "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım; görünmez bağ kopmuş olabilir."
  - Maliyet, komisyon, borç, OOS kanıtı yok. Tüm sonuçlar tek pair, tek dönem, seçilmiş.
- **Bedava günlük veriyle uygulanabilir mi:** Hesaplama düzeyinde evet: yfinance `.IS` günlük adjusted close + statsmodels (`coint`, OLS) yeter (YORUM; kaynak araç veya kütüphane adı vermiyor). Projenin güncel veri durumu ayrıdır: İş Yatırım, Yahoo yok, açılış yok; T+1 açılış dolumu uygulanamaz (TASARIM 5.1, 5.3). Eksik: formül, eşikler. Short bacağı BIST perakende için zor (açığa satış listesi/kısıt) (dış kaynak: BIST açığa satış kuralları, beyinde kaynak yok; YORUM); long-only rotasyon uygulanabilir ve Tansu'nun VAKBN/CIMSA sürümü zaten long-only (YORUM: rotasyon = ucuz olanı tut). İki bacaklı sürümün borç/finansman maliyeti verisi ücretsiz değil.
- **Kaynak güveni:** Giriş ±2, Z-dönüşü=ΔZ ve yön etiketleri GÖRSEL'dedir. YORUM: long-only rotasyon ve ilk sinyale kadar nakit bu katalogdaki model seçimleridir; grafik genel nakit politikasını açıklamaz (GÖRSEL, kaynak-vakbn-garan-rotasyon-2096358189696520213/02-vakbn-garan-rapor-2.jpg). Spread/hedge/pencere/sağlık eşikleri açık değildir. Performans: tek örnek, doğrulanmamış.

## Çıkış / başarısız pair ve sağlık kapısı (Rolling cointegration)
- **Kaynak:** tweet-rolling-cointegration-iliski-bozulma-kapisi (Ham); VAKBN rapor.webp; gorsel-paket-53.
- **Tansu'nun fikri:** kayan eşbütünleşmeyle ilişki bozulmasını izlemektir (Ham, tweet-rolling-cointegration-iliski-bozulma-kapisi:21); uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- **Tanım:** YORUM: bu katalogdaki kapı seçimi pencere W ve `coint` p-değeriyle p > eşik iken yeni girişi kapatmaktır; kaynak pencere, sıklık, eşik, süreklilik ve bozulunca yapılacak işlemi açıklamaz (Ham, tweet-rolling-cointegration-iliski-bozulma-kapisi:21; GÖRSEL, kaynak-vakbn-garan-rotasyon-2096358189696520213/01-vakbn-garan-rapor-1.png).
- **Parametreler:** p=0,048 kaynakta görünür (GÖRSEL, kaynak-vakbn-garan-rotasyon-2096358189696520213/01-vakbn-garan-rapor-1.png). YORUM: 0,05 bu katalogdaki eşik seçimidir; gösterilen değerden zorunlu kapı eşiği çıkmaz.
- **Giriş/çıkış/kapı:** YORUM: p<0,05 bu katalogdaki giriş izni seçimidir; hangi ölçünün hangi işlemi engellediği ve bozulunca yapılacak işlem kaynakta açık değildir (GÖRSEL, kaynak-vakbn-garan-rotasyon-2096358189696520213/01-vakbn-garan-rapor-1.png; Ham, tweet-rolling-cointegration-iliski-bozulma-kapisi:21).
- **Belirsiz:** pencere, test (Engle–Granger?), p'nin her gün mü hesaplandığı, kapıyı hangi sinyaller kullanıyor, 53'teki kopmuş pair'in neden kapanmadığı (yatay ≈79 bin: nakit/askıya mı, bug mı?).
- **Tansu'nun kanıtı:** p=0,048 tek sayı. 53 negatif sonuç (yukarıda).
- **Bedava veri:** hesap yapılabilir; kaynak fikri pencere, sıklık, eşik ve eylem vermediğinden tam kapı olarak uygulanamaz (Ham, tweet-rolling-cointegration-iliski-bozulma-kapisi:21).
- **Kaynak güveni:** fikir Ham'da tek cümledir; hesaplanabilir kapı tanımı yoktur.
- **Ek kanıt (KANIT, bilet 04, 14.10):** `tweet-korelasyon-yuksek-istatistiksel-arbitraj-garanti-degil` (Ham; X arşivi bu gönderiyi Tansu'nun kendi gönderisi olarak gösterir, id 1994264146452340762; bu not o gönderidir): yüksek korelasyon istatistiksel arbitraj için yetmez; "Arbitraj için Cointegration (Eşbütünleşme) şarttır"; eşbütünleşme olmadan açılan işlemlerde "büyük zararlar". Yani çift seçiminde eşbütünleşme ön koşuldur. Test yöntemi, pencere, eşik, sayısal zarar örneği yok.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-dinamik-hedge-call-duvari-asimi-2083449552279937370` — Zayıf eşbütünleşmede çift kapatılmaz, risk dinamik hedge oranıyla yönetilir: "Cointegration zayıf olduğundan bu iki duvar arasında dinamik hedge oranlarıyla risk yakından yönetilmeli." (Ham). 4251 aşılırsa momentum squeeze beklenir; varlık ve üst gönderi notta yok (01.08.2026, emtia, bağlam eksik).

## 150 bin kombinasyon tarama
- **Kaynak:** tweet-istatistiksel-arbitraj-150bin-esbutunlesme-taramasi (Ham). Görsel yok.
- **Ifade (Ham, paraphrase):** "Eşbütünleşme testi iyi ihtimalle 150.000 kombinasyon taramasına kadar çıkabilir; bilmeniz önemli." C(549,2)≈150 bin (Claude hesabı).
- **Tanım:** Tüm ikili çiftleri eşbütünleşme testinden geçir. Evren, pencere, test, çoklu-test düzeltmesi Tansu'da yok. FDR vb. Claude önerisi (YORUM).
- **Kanıt:** yok. **Bedava veri:** testler evet (uzun sürer). **Güven:** sadece ölçek uyarısı.

---

# BÖLÜM 2 — Portföy

## Günlük (gün sonu) sabit ağırlık rebalancing
- **Kaynak:** gorsel-paket-37 (01-portfoy-kz-raporu.png, 02-gunluk-rebalancing-islem-logu.png); tweet-volatilite-harvesti-sabit-agirlik-rebalancing.
- **Tansu'nun ifadesi:** Ham (gorsel-paket-37): "gün sonu eklemeler eksiltmeler ile sistem getirisi 1.5 yada %27"; "ay" Ham'da yazmaz, 1,5 ay okuması görsel dönemden gelir (YORUM). Tweet (Ham, tweet-volatilite-harvesti-sabit-agirlik-rebalancing, paraphrase): ters korelasyonlu iki varlığı belirli oranlarda aktif yeniden dengeleyerek çalkantıyı getiri motoruna çevirmeyi matematiksel kanıtlama önerisi; kanıt sonra paylaşılacak.
- **Tanım:** Hedef ağırlıklar GARAN.IS %50 / KGYO.IS %40 / CCOLA.IS %10 (GÖRSEL başlık). Her gün sonu: `hedef_değer_i = w_i × portföy_değeri`; fark kadar AL/SAT (log sütunları: "Adet", "İşlem (TL)", "Toplam İşlem TL", "Portföy Değeri"). Formül YORUM (standart constant-mix).
- **Parametreler:** ağırlıklar 50/40/10 (GÖRSEL); sıklık günlük (GÖRSEL: 30 işlem günü batch); dönem 01.04.2026–15.05.2026; bant/eşik yok; maliyet yok; "Toplam Hacim 76.623,82 TL" ve "Ort. İşlem 2.554,13 TL", "En Büyük İşlem 7.825,91 TL" (log başlığı, düşük çözünürlük, tahmini okuma).
- **Giriş/çıkış/kapı:** Yok. Sürekli tam yatırımlı. Aynı gün 3 varlıkta da AL veya SAT görülen satırlar var (nakit/dış akış?), neden belirsiz.
- **Belirsiz:** emir zamanı (kapanış mı T+1 mi), nakit akışı, komisyon, lot yuvarlama, neden bazı günler üç AL.
- **Kanıt (GÖRSEL, 15.05.2026):** başlangıç 100.000; son kapanış 126.764,84 (+%26,76); önceki kapanış 129.433,76; günlük K/Z −2.668,92 (−%2,06); pasif (aynı ağırlıklarla sabit) 127.805,42 (+%27,81); aktif–pasif −1.040,58 (−%1,04). Bileşen getirisi: GARAN +%4,85 (129,80), KGYO +%58,21 (12,53), CCOLA +%20,98 (82,95). Yani **rebalancing bu pencerede pasifin 1,04 puan altında**; getiri varlık seçiminden (KGYO) geliyor. Bu bir hesap: 0,5×4,85+0,4×58,21+0,1×20,98 = 27,81 (GÖRSEL ile uyuşuyor).
- **Bedava veri:** Evet (yfinance günlük kapanış). **Güven:** Kural basit ve net; ama kanıt kısa (1,5 ay) ve pasifi geçemiyor. Yüksek (kural), düşük (kanıt).

## Ağırlık duyarlılığı (TEKTU / EREGL)
- **Kaynak:** gorsel-paket-57 (01–04).
- **İfade:** Ham: "geriye doğru simülasyonlar önemlidir"; TEKTU ağırlığı arttıkça getiri artıyor, EREGL arttıkça düşüyor.
- **Tanım:** Tek varlık ağırlığını 0..1 (0,1 adım) tara, kalan ağırlığı dağıt, dönem net getirisini yazdır. Kalan ağırlığın dağıtımı verilmedi. YORUM (hesapla): TEKTU=0 → 11,6; kalan XU100:EREGL 5:2 oranında dağıtılırsa 11,5. EREGL=0 → 18,0; kalan XU100:TEKTU 5:3 dağıtılırsa 17,9. Yani "kalanı orantılı dağıt" varsayımı veriye yakın (±0,1–0,2 puan; aktif rebalancing farkı olabilir).
- **Parametreler:** dönem 01.04.2026–22.04.2026; ızgara 0,0–1,0 adım 0,1; mevcut 50/30/20 (XU100/TEKTU/EREGL), revize 50/40/10 (GÖRSEL).
- **Kanıt (GÖRSEL):** TEKTU: 0→11,6; 0,1→13,5; 0,2→15,4; 0,3→17,2; 0,4→19,1; 0,5→20,9; 0,6→22,7; 0,7→24,5; 0,8→26,3; 0,9→28,1; 1,0→29,8 (%). EREGL: 0→18,0; 0,1→17,6; 0,2→17,2; 0,3→16,8; 0,4→16,4; 0,5→15,9; 0,6→15,4; 0,7→14,9; 0,8→14,4; 0,9→13,8; 1,0→13,3. Mevcut: son kapanış 117.229,03 (+%17,23); pasif 117.002,06 (+%17,00); aktif–pasif +226,97 (+%0,23); XU100 +%10,80, TEKTU +%29,82 (12,32), EREGL +%13,27 (32,60). Revize: 118.844,17 (+%18,84); pasif 118.656,84 (+%18,66); fark +187,33 (+%0,19). Günlük K/Z −510,18 (−%0,43) / +26,24 (+%0,02).
- **Karar kuralı:** Yok. Bu ex-post duyarlılık; optimal ağırlık seçme kuralı değil.
- **Bedava veri:** Evet. **Güven:** Görsel yüksek, kural yok.

## Min-Vol / Max-Sharpe vs BIST100 (DEY marjı)
- **Kaynak:** gorsel-paket-33 (01 jpg).
- **İfade (GÖRSEL):** "Portföy Kapanış Performansı, DEY Marjı ve BIST100 Karşılaştırması (Excel Base 100)"; "MV - Kapanış Getirisi", "MV - DEY (Kümülatif En Yüksek)", "MS - Kapanış Getirisi", "MS - DEY (Kümülatif En Yüksek)", "BIST100 Benchmark"; "Min Volatility Portföyü (Kapanış vs DEY)", "Max Sharpe Portföyü (Kapanış vs DEY)". Ham: Tansu "portföy üzerine düşeni yaptıve yapıyor" (Ham'daki yazım).
- **Tanım:** MV = minimum varyans, MS = maksimum Sharpe (YORUM; standart Markowitz). DEY = dönem içi kümülatif en yüksek değer (kapanış değil). Hesap biçimi (gün içi high toplamı mı?) bilinmiyor.
- **Parametreler:** Hiçbiri verilmedi: evren, ağırlık, optimizasyon penceresi, risksiz oran, kısıtlar, maliyet.
- **Kanıt (GÖRSEL, yaklaşık okuma, ~20 Mayıs–1 Haz 2026, birkaç işlem günü):** MV kapanış ≈115, MV DEY ≈123–124; MS kapanış ≈108–109, MS DEY ≈118–119; BIST100 ≈97,8. İlk günden sonra ikisi de düştü (MV ≈97,6; MS ≈95,4; BIST100 ≈94).
- **Bedava veri:** Optimizer evet (scipy); sonuç yeniden üretilemez (girdi yok). **Güven:** çok düşük; ~8 gün.

## 161.700 kombinasyon taraması
- **Kaynak:** gorsel-paket-96 (01 png).
- **İfade (GÖRSEL):** "İlerleme: 35150/161700 kombinasyon test edildi" … "37300/161700". Ham: 161.700 kombinasyon bitince algoritma "matematiksel olarak optimal" 3 hisselik portföyü verecek; evren = 6 Ocak'ta momentum alanındaki hisseler; amaç o tarihten bugüne getiriyi görmek.
- **Tanım:** C(100,3)=161.700 (hesap doğru; 100 aday sayısı YORUM çıkarımı). Her üçlü için bir amaç ölçüsü hesaplanıyor; hangisi, ağırlık yöntemi (eşit mi Markowitz mı) bilinmiyor.
- **Parametreler:** yok. **Kanıt:** sadece ilerleme sayacı (en az %23,07 tamam). Sonuç yok.
- **Uyarı:** "6 Ocak'tan bugüne en iyi üçlü" ex-post oracle'dır, ileriye dönük kural değil (YORUM).
- **Bedava veri:** Hesap evet; momentum formülü ve liste bilinmiyor. **Güven:** çok düşük.

## B&H vs sinyal bazlı strateji scorecard
- **Kaynak:** gorsel-paket-59 (01 png).
- **İfade (GÖRSEL):** "Toplam Getiri: B&H +%21.54, Sinyal Bazlı +%14.74 ('B&H ham getiride önde')", "Yıllık Volatilite %33.16 / %23.21 ('Strateji, oynaklığı ~%30 azaltmış')", "Max Drawdown −%2.46 / −%1.72", "Sharpe Oranı 9.477 / 9.477 ('Risk başına düşen getiri başabaş')".
- **Tanım:** Sinyal kuralı verilmedi. Hesap (YORUM): 23,21/33,16=%70,0; 1,72/2,46=%69,9; 14,74/21,54=%68,4 → strateji B&H riskinin ~%70'ini taşıyor gibi (ör. ~%70 maruziyet); Sharpe aynı çıkması buna uyar.
- **Parametreler:** dönem, sinyal, frekans, risksiz oran yok. YORUM: Sharpe 9,5 için kısa dönem açıklaması bu katalogda adaydır; kaynak dönemi veya örnek seçimi amacını açıklamaz (Ham, gorsel-paket-59-buyhold-sinyal-risk-scorecard:20; GÖRSEL, gorsel-paket-59-risk-scorecard/01-buyhold-sinyal-stratejisi-risk-scorecard.png).
- **Bedava veri:** kural yok, uygulanamaz. **Güven:** düşük.

## Üç aşamalı portföy (düşük korelasyon + yüksek vol → Max Sharpe → vol trading); ANN/Markowitz pipeline; "Spicy"/SciPy; risk bütçesi
- **Kaynak:** tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading; tweet-satilik-degil-momentum-teknik-markowitz-max-sharpe-pipeline; tweet-spicy-scipy-deterministik-markowitz-optimizasyonu; tweet-portfoy-optimizasyonu-volatilite-trading-risk-butcesi. Görsel yok. Hepsi Ham.
- **İfade (Ham, paraphrase):** Aşama 1: düşük korelasyon + yüksek volatiliteyle 10–20 aday. Aşama 2: Markowitz/etkin sınır/Max Sharpe ile 3–10 nihai hisse, bir çekirdek hisse >%50 (Ham, tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading:21). Aşama 3: stratejik ağırlığı koruyarak RSI/Bollinger/ortalamaya dönüş ile volatilite trading. Pipeline: ANN momentum → eğim → ADX/CMF/mum → Markowitz → Max Sharpe; "Bu sistem satılık değil", parametre ve model paylaşılmıyor. "Spicy" (muhtemelen SciPy): Monte Carlo yerine deterministik optimizasyon. Portföy optimizasyonu ve volatilite trading ilişkisi "huzurlu gecelerin anahtarıdır".
- **Parametreler (Ham):** aday 10–20; nihai 3–10; çekirdek >%50 (Ham, tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading:21). Diğerleri yok (lookback, tahmin yöntemi, beklenen getiri, risksiz oran, RSI/Bollinger eşikleri).
- **Giriş/çıkış:** yok. **Kanıt:** yok.
- **Bedava veri:** scipy.optimize ile Max Sharpe/Min Vol evet; aday süzme ve ANN/teknik adımlar tanımsız. YORUM: `scipy.optimize.minimize` SLSQP, ağırlık ≥0 ve toplam=1 bizim çözüm seçimlerimizdir. Çekirdek >0,5 kaynaklıdır (Ham, tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading:21).
- **Güven:** düşük (sadece taslak).

---

# BÖLÜM 3 — Piyasa rejimi / "Piyasanın Nabzı"

## Hangi "VIX"?
- GÖRSEL 114: VIX paneli 10–50 aralığında, tepe ≈52. YORUM: bu katalogda CBOE VIX (ABD, S&P 500) olarak okunur; kaynak yalnız VIX etiketi verir, ticker/kaynak/formül açık değildir (GÖRSEL, gorsel-paket-114-bist-vix-python-master/01-bist-vix-master-paneller-1-3.png ve gorsel-paket-50-bist-volatilite-gulumsemesi/01-bist100-bist-vol-log-getiri-scatter.png).
- GÖRSEL 50: ayrı bir "BIST_VOL" serisi var (BIST100 ile log getiri scatter). Tanımı/kaynağı verilmemiş. Bedava günlük kaynağı doğrulanamadı: web aramasında BIST için resmî VIX benzeri bulunamadı (TRVIX yalnızca akademik öneri; VİOP verisi ücretli olabilir) (dış kaynak: web araması, beyinde kaynak yok; YORUM). YORUM: ayrı araştırma gerekir.
- Bedava: CBOE VIX = yfinance `^VIX` veya FRED `VIXCLS`. Zaman farkı: BIST kapanışı ABD VIX kapanışından önce; önceki ABD günü kullanılmalı (YORUM; Tansu belirtmiyor).

## Piyasanın Nabzı (7 kutu, skor 4/5)
- **Kaynak:** gorsel-paket-98 (01 jpg; NotebookLM görseli, birinci el).
- **İfade (GÖRSEL):** başlık "Piyasanın Nabzı: Teknik Analiz Raporu"; "Yedi temel gösterge…". Kutular:
  1. Korelasyon (Borsa & VIX) — "Mevcut Korelasyon Değeri: −0.60" — "Yorum: SAĞLIKLI".
  2. Fiyat & Trend (SMA 18/35) — "MEVCUT FİYAT 11336.18; SMA Kısa (18) 11335.87; SMA Uzun (35) 11026.53" — "POZİTİF"; "Yükseliş Trendi (Boğa)".
  3. Momentum (Awesome Oscillator) — "Mevcut Durum: Kırmızı Çubuk (Düşüyor)" — "NEGATİF".
  4. Güç Göstergesi (RSI) — "Mevcut RSI: 68.0" ve "Ortalama RSI: 68.1" (büyütülmüş görselden okundu; düşük çözünürlük, son haneler az belirsiz) — "GÜÇLÜ".
  5. Korku Endeksi (VIX) — "Mevcut VIX: 13.47"; "Güvenli Bölge Üst Limiti: 16.99" — "GÜVENLİ (SAKİN)".
  6. Trend Gücü (ADX & DI) — "Mevcut ADX Değeri: 22.9"; "25 Üzeri: Güçlü Trend" — "TREND OLUŞUM AŞAMASINDA".
  7. Hacim — "Ortalama Hacim 4,805,210,000", "Mevcut Hacim: 0" — "DÜŞÜK HACİM".
  Alt: "Genel Yükseliş Skoru: 4 / 5"; "Nihai Karar: DİKKATLİ İYİMSERLİK"; "Analiz edilen ilk beş kritik kuraldan dördü pozitif sinyal veriyor"; "Aksiyon Önerisi: Stoplu iyimserlik… mutlaka zarar durdurma (stop-loss)".
- **Tanım (hesaplanabilir kısım):**
  1. Skor = ilk 5 kutudan pozitif sayısı (GÖRSEL: "ilk beş kritik kuraldan dördü"). ADX ve Hacim skora girmiyor, destekleyici.
   2. Kutu kuralları: Korelasyon < 0 → SAĞLIKLI; Fiyat > SMA18 > SMA35 → POZİTİF (11336,18 > 11335,87 > 11026,53); AO kırmızı → NEGATİF; RSI 68 → GÜÇLÜ; VIX 13,47 < 16,99 → GÜVENLİ; ADX 22,9 < 25 → "oluşum". RSI kaynakta kendi ortalamasıyla anlatılır; YORUM: 50/60 sabit eşik adayları bizim seçimimizdir, kaynak karşılaştırmayı hesaplanabilir biçimde vermez (NotebookLM görseli, gorsel-paket-98-piyasanin-nabzi-teknik-rapor/01-piyasanin-nabzi-yedi-gosterge-raporu.jpg).
  3. Nihai karar eşlemesi: 4/5 → "Dikkatli İyimserlik" (tek örnek; diğer skorların etiketi bilinmiyor).
- **Parametreler:**

| parametre | değer | kaynak |
|---|---|---|
| SMA kısa/uzun | 18 / 35 | GÖRSEL |
| AO | standart 5/34 (medyan fiyat) | YORUM (görselde parametre yok) |
| RSI | 14 varsayımı | YORUM; eşik bilinmiyor |
| ADX eşiği | 25 | GÖRSEL |
| VIX "güvenli üst limit" | 16,99 | GÖRSEL; kaynağı/yöntemi bilinmiyor (114'teki "VIX Ofsetli Bantlar" üst bandı olabilir, YORUM) |
| Korelasyon penceresi | 30 gün (114 grafik başlığı: "Korelasyon (VIX vs BIST 100 - 30 Günlük)") | GÖRSEL (114) |
| Skor | 4/5 | GÖRSEL |

- **Giriş/çıkış/kapı:** Rapor işlem sinyali değil, yeni pozisyon için ortam notu. Görsel metni: "Stoplu iyimserlik … zarar durdurma (stop-loss) seviyeleri belirlenmelidir" (GÖRSEL). YORUM: hacim=0 için veri hatası bu katalogda açıklama adayıdır; kaynak nedenini ve eylemi açıklamaz (NotebookLM görseli, gorsel-paket-98-piyasanin-nabzi-teknik-rapor/01-piyasanin-nabzi-yedi-gosterge-raporu.jpg).
- **Belirsiz:** korelasyonun serisi (seviye mi getiri mi; 114'te değerler −0,75…+0,65 arası: getiri korelasyonu gibi, YORUM), hangi hisse/endeks (BIST100 varsayımı; fiyat 11.336 ≈ XU100 değeri, çözünürlük/tarih yok), RSI/AO eşikleri, 4/5'in tüm bantları, hacim 0'ın nedeni, "ortalama hacim" penceresi.
- **Kanıt:** yok (tek anlık görüntü; sonuç yok). **Bedava veri:** Hesaplama düzeyinde evet (XU100.IS OHLCV ve ^VIX bizim veri seçimimizdir, görselde veri kaynağı yok; yfinance endeks hacmi güvenilir olmayabilir, YORUM); projede XU100 yalnız kapanış verir (TASARIM 5.1).
- **Güven:** Skor mantığı orta (görselden hesaplanır); eşikler düşük.

## BIST VIX long: 5 adım kontrol listesi + Python master analiz
- **Kaynak:** gorsel-paket-113 (01 jpg), gorsel-paket-114 (01, 02 png).
- **İfade (GÖRSEL 113):** başlık "BIST 100 & VIX: Kusursuz Yükseliş (Long) Pozisyonu İçin 5 Adımlı Kontrol Listesi".
  - ADIM 1 Korelasyon Kontrolü: "BIST 100 yükselirken VIX'in düşmesi veya sakin kalması gerekir"; durum "GEÇERLİ".
  - ADIM 2 Disiplin ve Trend: "Heikin Ashi Mumlarını Kullan"; "GEÇERLİ".
  - ADIM 3 Long Giriş Şartları: "Fiyat > Hareketli Ortalamalar"; hem SMA 20 (sarı) hem SMA 50 (eflatun) üstünde; kısa ortalama uzunun üstünde; "GEÇERLİ (ÇOK GÜÇLÜ)".
  - ADIM 4 VIX Teyidi: "VIX endeksi düşük seviyelerde olmalı ve VIX RSI göstergesi kendi hareketli ortalamasının (SMA 10) altında seyretmelidir"; "GEÇERLİ".
  - ADIM 5 Çıkış Stratejisi: "çıkış kararı VIX'e değil, doğrudan BIST 100 fiyat grafiğine göre" (örnek: Fiyat < SMA 20 veya Heikin Ashi kırmızıya dönmesi); durum "ÇIKIŞ SİNYALİ YOK".
  - Alt: "SONUÇ: Kusursuz Long"; "Alarm Sinyali: Fiyat, SMA 20'nin altına inerse ve/veya aynı zamanda VIX RSI kendi ortalamasını yukarı keserse, bu durum potansiyel bir risk artışına işaret eder ve çıkış stratejisi değerlendirilmelidir."
  - GÖRSEL 114: başlık "BIST 100 (XU100) & VIX MASTER ANALİZİ (2025-01-01 - 2025-12-14)"; paneller: 1 "BIST 100 (Heikin Ashi) + SMA 20/50"; 2 "Korelasyon (VIX vs BIST 100 - 30 Günlük)" (±0,5 kesikli çizgiler); 3 "VIX Ofsetli Bantlar (Çizgi Grafik)" (Hızlı Üst, Yavaş Üst); 4 "VIX Awesome Osilatörü"; 5 "VIX RSI (200) + SMA (10)" (60 kırmızı, 40 yeşil kesikli çizgi).
  - Ham (gorsel-paket-114): sistemin kurallara dayalı olduğu, duyguya yer olmadığı; **çıkış için dört indikatörden ikisinin bozulması** gerektiği (ayrıntı yok).
- **Tanım (hesaplanabilir):**
   - İzin ("Kusursuz Long") = hepsi doğru; UYGULANAMAZ: projenin endeks kaynağı yalnız kapanış verir, HA için açılış/yüksek/düşük ve diğer seriler eksiktir (Ham, gorsel-paket-114-bist-vix-python-master-analiz:23–68; GÖRSEL, gorsel-paket-114-bist-vix-python-master/01-bist-vix-master-paneller-1-3.png):
    1. 30 günlük korelasyon(VIX, BIST100) < 0 (GÖRSEL: "sıfırın altında"; serinin getiri mi seviye mi olduğu YORUM).
    2. BIST100 Heikin Ashi mumu yeşil.
    3. Kapanış > SMA20 > SMA50 (YORUM: SMA20>SMA50 "kısa uzunun üstünde" ile uyumlu).
    4. VIX sakin (bant içi / düşük seviye) VE VIX RSI(200) < SMA10(VIX RSI).
    5. Çıkış koşulu yok.
   - Fiyat < SMA20 veya HA kırmızı çıkışı, fiyat+VIX alarmı ve 2/4 anlatımı ayrı kaynak ifadeleridir (Ham, gorsel-paket-114-bist-vix-python-master-analiz:54,68; GÖRSEL, gorsel-paket-113-bist-vix-long-checklist/01-bist-vix-long-bes-adim-kontrol.jpg). YORUM: bu katalogdaki çıkış adayı fiyat < SMA20 veya HA kırmızı; ve/veya VIX RSI SMA10'u yukarı kesmesidir. Kesin çıkış birleşimi ve sayılan dört gösterge açık değildir.
- **Parametreler:**

| parametre | değer | kaynak |
|---|---|---|
| SMA | 20 ve 50 (BIST100) | GÖRSEL |
| Heikin Ashi | günlük | GÖRSEL (114; frekans gün) |
| Korelasyon penceresi | 30 gün | GÖRSEL |
| VIX RSI | RSI(200) | GÖRSEL |
| VIX RSI sinyal | SMA(10) | GÖRSEL |
| VIX RSI bantları | 60 / 40 | GÖRSEL (114 panel 5) |
| VIX Ofsetli Bantlar | formül/offset/pencere yok | belirsiz |
| VIX AO | görünüyor, parametre yok | belirsiz; 114'te AO VIX'e ait, 114 Ham'ı 3. kuralda "AO = Yeşil" diyor (Ham) → çelişki |
| Çıkış 2/4 | Ham (gorsel-paket-114) | birinci el, ayrıntı yok |

- **Giriş/çıkış/kapı:** yukarıda. Korelasyon "sağlıklı" kapısı: < 0 (GÖRSEL); sıfırın altı eşik, ±0,5 çizgileri grafikte (kapı olarak kullanılıp kullanılmadığı belirsiz).
- **Belirsiz:** VIX "düşük seviye" eşiği (98'deki 16,99?), ofset bant formülü, VIX AO'nun rolü, 2/4 listesi, VIX hizalama (aynı gün/önceki gün), yeşil HA tek mum mu ardışık mı, RSI(200) ısınması (≥200 gün veri gerekir; 114'te ocak 2025'ten başlıyor, öncesi gösterilmemiş).
- **Kanıt:** yok (geriye dönük işlem sonucu yok). 114 notu bunu tarihsel snapshot sayıyor (NOT, ikinci el: Kaynak kartı). Snapshot 2025-12-14 (pazar) bitişli.
- **Bedava veri:** Hesaplama düzeyinde evet: XU100.IS OHLC ve ^VIX/FRED bizim veri seçimimizdir (YORUM; kaynakta sağlayıcı adı yok); HA, SMA, RSI(200), AO, rolling corr pandas ile hesaplanır. Projenin XU100 kaynağı yalnız kapanış verir (TASARIM 5.1); HA ve AO için açılış, yüksek, düşük yoktur, bu yüzden güncel durumda uygulanamaz (yukarıdaki Tanım).
- **Kaynak güveni:** Giriş/çıkış mantığı orta-yüksek (görselde açık yazılı); VIX eşik/bant ve 2/4 düşük.

## Endeks 5/5 skor (NH-NL, Corwin–Schultz, likidite)
- **Kaynak:** tweet-endeks-5of5-nhnl-corwin-schultz-likidite (Ham; görsel yok).
- **İfade (Ham):** "Bugün endeks bana ne anlatıyor?" Değerler: genel skor 5/5, ADX 28,9, RSI 77,6, VIX 20,6, 20 günlük NH-NL 83, 65 günlük NH-NL "Katılım Yok", XU100 Corwin–Schultz ort. spread %1,06. Sonuç: ana trend "Full Long"; likit endeks liderlerinde kal; düşük hacim ve zayıf 65 gün katılımı nedeniyle yan hisselerde agresifleşme; sigma sıçramasını izle.
- **Tanım:** NH-NL = N günlük yeni yüksek sayısı − yeni düşük sayısı (YORUM, standart; "83" fark mı oran mı belirsiz). 5/5'in beş bileşeni bilinmiyor.
- **Parametreler:** pencereler 20 ve 65 gün (Ham); eşikler yok.
- **Kanıt:** yok. **Bedava veri:** NH-NL için XU100 bileşenlerinin günlük OHLC'si (yfinance, bileşen listesi ve sağkalım yanlılığı sorunu); CS spread için günlük high/low (evet). **Güven:** düşük.

## Corwin–Schultz spread / sigma
- **Kaynak:** kaynak-xu100-corwin-schultz (spread-sigma.webp); gorsel-paket-62 (FROTO, 01 png).
- **İfade:** Ham (kaynak-xu100-corwin-schultz): spread ve sigma birlikte işlem kalitesi ve risk göstergesi, yön sinyali değil; düşük sigma + yüksek spread = sakin görünen ama kırılgan olabilir. XU100 spread ≈%2,15, tarihsel ort. ≈%1,09, son 20 işlem günü getirisi ≈%1,45; son iki günde spread ↑ sigma ↓. GÖRSEL: "Corwin-Schultz Bid-Ask Spread 21 Gunluk", "Volatilite Tahmini Sigma", "Referans Seviyeleri: Ortalama 1.088%, Medyan 0.454%, P75 1.899%, P90 3.028%" (kesikli çizgiler: 3,03 kırmızı, 1,9 gri, 1,09 turuncu). FROTO: "Ortalama Spread 1.7990%, Medyan Spread 0.7841%, Max Spread 9.8494% (2025-04-14), Min Spread 0.0000% (2024-01-31), Ortalama Sigma 2.1133%", "Corwin-Schultz Bid-Ask Spread (%, 21g rolling)", "Volatilite Tahmini (Sigma %)".
- **Tanım:** Corwin–Schultz 2012 günlük high/low spread tahmincisi (dış kaynak: Corwin–Schultz 2012 makalesi, formül beyinde yok; YORUM) (iki günlük range, β ve γ'dan α, spread = 2(e^α−1)/(1+e^α), negatifler sıfıra çekilir — grafikte çok sayıda tam sıfır görünür, bu "sıfıra kırpma" ile uyumlu, YORUM). "21 gün" bir rolling pencere olarak etiketli (ortalama mı, pencerede tahmin mi belirsiz). Sigma: tahminci ile gelen volatilite tahmini (formül belirsiz).
- **Parametreler:** pencere 21 gün (GÖRSEL); referanslar ort/medyan/P75/P90 (GÖRSEL); eşik kuralı yok (P90 çizgisi vardır).
- **Giriş/çıkış:** yok (bilgi göstergesi). **Kanıt:** yok. **Bedava veri:** Evet; tek gerekli yfinance günlük high/low. YORUM: endeks high/low gerçek bileşen spreadini yansıtmaz (Cevo çıkarımı, ikinci el; Ham'da yok).
- **Güven:** Gösterge tanımı orta, kural yok.

## SETUP x/100, YAPI (XU100 1 ve 2 Eylül)
- **Sahibi:** A §5 (XU100 başlıkları, puanlar, gösterge parametreleri, tweet metni, puan formülünün yokluğu). Burada tekrar edilmez. (bilet 04, 14.10)
- **Piyasa durumu yönünden okuma:** SETUP puanı formülsüzdür ve yeniden üretilemez; piyasa durumu etiketi olarak kullanılamaz (TASARIM §3: etiket YORUM'dur).

## FROTO / Volatilite şoku (yeni alım freni) / Trend rejimi
- **Tansu'nun fikri:** oynaklık şokunda yeni alımı durdurup mevcut riski yönetmektir (Ham, tweet-volatilite-piyasa-soku-yeni-alim-freni:21); uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- **Trend rejimi (korelasyon vs HMM):** tweet-trend-rejim-degisimi-korelasyon-hmm-gereksiz. Not kendisi kaynağın URL'sinin bulunmadığını ve Levent'in görüşü olarak kullanılamayacağını yazıyor. Tezi: güçlü korelasyon varsa HMM gereksiz; hangi seri/pencere/eşik yok. Güven: çok düşük. BIST100–BIST_VOL scatter (gorsel-paket-50): X "BIST100", Y "BIST_VOL", log getiriler; V/U şekilli (iki yönde büyük hareketlerde BIST_VOL yukarı). Tansu şakası (Ham, gorsel-paket-50): "Piyasa yapıcının bize bir mesajı var". Kanıt: tek scatter; aralık BIST100 ≈ −0,20…+0,18, BIST_VOL ≈ −0,4…+0,7; tarih/n yok. YORUM: doğrusal korelasyon bu ilişkiyi kaçırır (kuadratik/mutlak getiri kullan).

## Sektör rotasyonu: liderler 30/60/90 ve anomali temizleme
- **Kaynak:** gorsel-paket-06 (01 png), gorsel-paket-07 (01 png), tweet-sektor-rotasyonundan-hisse-secimine.
- **İfade:** Ham (Tansu tweet 27 Ağustos 2026, alıntı): "Sektör rotasyonu… lider sektörde Dupont analizi, ucuz kalmış hisseler… mevsimsel satışları." (planlanan zincir; teslim yok).
- **Tanım (GÖRSEL 06+07):**
  1. Sektör skoru = sektörün son N gün getirisi, N ∈ {30, 60, 90} (çıktı: "Son 30/60/90 Günlük Getiride En İyi 3 Sektör", "Name: 2026-08-14", GÖRSEL 06). Görsel 07 yalnız Dayanıklı Tüketim için 30 günlük "Hisse bazlı basit ortalama (TÜM HİSSELER)" gösterir. 06'daki sıralamanın ve 60/90 günlük skorların aynı basit ortalamayla hesaplandığı görselde yazmaz (YORUM). "N gün" işlem günü mü takvim günü mü belirsiz.
  2. Görsel 07 iki yöntemi yan yana yazar: "Hisse bazlı basit ortalama" %-1,32 ve "Fiyat-ortalaması yöntemi (ESKİ / script'teki)" %+90,99. Görsel bu yönteme "yanlış" demez; anomali temizlemesi sonrası temiz ortalama −%11,11 (GÖRSEL 07).
  3. Anomali kuralı: `|30g getiri| > %50` → ANOMALİ, ortalamadan çıkar ("OZATD.IS: %+165.06 ← ANOMALİ, ortalamadan çıkarıldı"). Temiz ortalama 17/18 hisseyle.
  4. Sıralama: sektör skoruna göre en iyi 3.
- **Parametreler:** pencereler 30/60/90 (GÖRSEL); anomali eşiği %50 (GÖRSEL) (60/90 gün için aynı eşik mi belirsiz); toplama: aritmetik ortalama (GÖRSEL). **Medyan:** görselde medyan yok; notlardaki medyan Claude önerisi. Hesabımla: tüm hisseler medyan −12,12; temiz medyan −12,69 (YORUM bilgi; ortalama −1,32 / −11,11).
- **Kanıt (GÖRSEL, 2026-08-14):** 30g: Petrol 0,2389; Mimarlık ve Mühendislik Faal. 0,1431; Mesleki Bilimsel Tekn. Faal. 0,1030. 60g: Yatırım Şirketleri 0,1289; Petrol 0,1283; Demir Çelik 0,1030. 90g: Bayındırlık ve İmar 0,2875; Demir Çelik 0,2859; Bilişim ve Yazılım 0,2344. Dayanıklı Tüketim: 18 hisse; ham ort. −%1,32; temiz −%11,11; fark 9,79 puan; 18 hisse listesi görselde (ALCAR −11,55; ARCLK −4,46; ARZUM −12,82; BVSAN −4,93; FORMT −25,33; HATSN −7,92; HKTM +12,62; IHEVA −2,43; IMASM −16,23; KLMSN −11,33; MAKIM −12,82; MEKAG −17,93; OZATD +165,06; SAFKR −7,07; SILVR −12,69; SNICA −27,25; VESBE −13,89; VESTL −12,85). Hesapla doğrulandı.
- **Giriş/çıkış/kapı:** Yok. Sektör sıralaması sonrası şirket aşaması DuPont + ucuzluk + mevsimsellik (planlanan; tanım yok).
- **Belirsiz:** sektör evreni/sınıflandırması (ad "Petrol", "Demir Çelik" vb. — KAP/BIST sektör listesi gibi), N gün tanımı, anomali eşiği diğer pencerelerde, sektör başına minimum hisse sayısı, getirinin düzeltmeli fiyatla mı hesaplandığı, hangi pencere "lider" sayılacak (üç pencerenin ortak lideri yok: Petrol 30/60, Demir Çelik 60/90).
- **Bedava veri:** Evet (yfinance `.IS` günlük kapanış; sektör üyeliği için ücretsiz tam liste: KAP/Borsa İstanbul sayfaları, elle derleme gerekir — YORUM).
- **Güven:** Hesap kuralı 30 günlük için yüksek (basit ortalama, |30g|>%50); 60/90 günlük yöntem görselde yok. Evren düşük.
- **Hacim filtresi (bilet 04, 14.10):** `tweet-sektor-rotasyonu-hacim-tuzagi-sabit-tl-esigi` (Ham; X arşivi bu metni Tansu'nun kendi gönderisi olarak gösterir, id 1992891892736930163; gönderi notu: `tweet-sektor-rotasyonu-tl-hacim-filtresi-1992891892736930163`). Sektör rotasyonunda hacim filtresi BIST100 ortalamasına göre kurulmaz (büyük hacimli hisseler ortalamayı yükseltir, orta ölçekli şirketleri haksız eler). Tanım: günlük TL hacmi = kapanış fiyatı × işlem adedi; 20 günlük (1 ay) veya 60 günlük (3 ay) hareketli ortalama; sonra eşik. Yöntem A (sabit): 20 günlük ortalama hacmi 10 milyon TL altındaki hisseler listeye girmez. Yöntem B (dinamik): sektör içinde hacimde en alttaki %25 atılır. Sektör ayrımı sektörün kendi içinde yapılır ("80'e yakın sektör", Tansu'nun tahmini). Parametre: 20/60 gün (Tansu); 10 milyon TL ve %25 örnek değerdir, gerekçe ve test yok. Likidite kapısı eşiğiyle ilişki: E K10. Günlük bedava veriyle: evet. Güven: Ham; X arşivi gönderiyi Tansu'nun kendi gönderisi olarak gösterir.
- **Konveks rotasyon (bilet 04, 14.10):** `tweet-konveks-rotasyon-stratejisi-makro-dongu` (Ham; X arşivi bu metni Tansu'nun kendi gönderisi olarak gösterir, id 1993786615110750282; gönderi notu: `tweet-konveks-sektor-rotasyonu-bes-adim-1993786615110750282`; "çok fazla detayı olan" daha büyük bir projenin adımlarından biri). Beş adım: (1) makro ve döngü analizi (ekonomik döngünün aşaması rotasyon yönünü belirler; örnek: faiz indirimi beklentisi, bankacılık); (2) konveksite filtresi (F/K tarihsel ortalamanın altında, makro beklentisi güçlü sektör); (3) erken aşama: dipten uzaklık düşük, sektör BIST100'e veya sektör endeksine göre yeni ayrışıyor; (4) negatif konveksiteli sektörden pozitif konveksiteliye sermaye kaydırma; (5) her rotasyon hamlesine zarar kes kriteri. Eşik, zarar kes düzeyi, test yok; "konveksite" burada ölçülmeyen yarı-sezgisel bir terimdir (YORUM). F/K ve makro adımı değerleme ve makro verisi ister (TASARIM 3: değerleme kapsam dışı). Uygulanabilir mi: HAYIR (eşiksiz çerçeve).
- **DEA/VZA sektör seçimi (bilet 04, denetim tur 1; Ham; X arşivi bu gönderiyi Tansu'nun kendi gönderisi olarak gösterir, id 2019059725963317611; bu not o gönderidir; YORUM):** `tweet-dea-vza-sektor-rotasyonu-malmquist-projesi` (Ham metin Levent'in yapıştırdığı içeriktir; yalnız ilk cümle kısa ve birinci tekil, ders gövdesi uzun ve başlıklıdır). Kural, tek satır: her sektör bir karar birimidir; girdi (volatilite, beta, F/K, PD/DD) ve çıktı (getiri, alfa, temettü, momentum) üzerinden DEA etkinlik skoru (0–1) hesaplanır; skoru 1 olan ya da 1'e en yakın 3–4 sektör portföye girer, analiz aylık ya da çeyreklik tekrarlanır, skoru belirgin düşen sektörden çıkılır; Malmquist endeksi 1'in üstündeyse "güçlü al" sayılır. Parametre: yalnız 3–4 sektör, skor 1, Malmquist > 1; "belirgin düşüş", evren, dönem, yönelim ve ölçek varsayımı yok. Kanıt yok (proje aşamasında). Uygulanabilir mi: HAYIR (F/K ve PD/DD girdileri değerleme verisi ister, TASARIM 3; girdi kimlikleri ve çalıştırılmış sonuç yok). İlişkili proje fikri: `tweet-convex-hull-dea-sektor-rotasyonu-projesi` (kural içermez listesinde).
- **Aylık mevsimsellik (bilet 04, denetim tur 1; Ham; X arşivi bu gönderiyi Tansu'nun kendi gönderisi olarak gösterir, id 2009731947375854034; gönderi notu: `tweet-aylik-mevsimsellik-olasilik-kasa-ayari-2009731947375854034`; YORUM):** `tweet-aylik-getiri-mevsimsellik-piyasa-hafizasi` (Ham metin Levent'in yapıştırdığı uzun, başlıklı ders metnidir). Kural, tek satır: enstrümanın son 10–20 yıllık aylık getirisinden, pozitif kapanış olasılığı %70 ve üzeri olan aylar "yüksek olasılık", düşüşün derinleştiği aylar "risk" sayılır; işlem ağırlığı bu takvime göre ayarlanır. Parametre: yalnız 10–20 yıl ve %70; "Ocak 10 yılın 8'i pozitif" örnek, kasa oranları (Nisan %80, Ağustos %30) örnektir, kural değildir. Maruziyete çevirme kuralı, test ve sonuç yok. Uygulanabilir mi: KISMEN (aylık kapanış yeter).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-aylik-getiri-mevsimsellik-nisan-sat-agustos-al-1782838495599378879` — Aylık mevsimsellik kuralına DOAŞ örneği: son 20 yılın takvim ayı ortalama getirilerinden Şubat'tan Nisan'a yükseliş, Nisan zirve, Ağustos'a düşüş; "Nisan sat Ağustos al, Kasım sat." (Ham, alıntılanan Tansu gönderisi). Sonuç iddiası (Nisan 2024 zirve) veri göstermez; tek hisse. Parametre: pencere = son 20 yıl; takvim = Nisan sat, Ağustos al, Kasım sat (Ham).
  - `tweet-aylik-mevsimsellik-getiri-istatistigi-2018404523635515480` — Aylık mevsimsellik kuralının ölçülmüş örneği: XU100 Şubat getirisi 12 yılda 5 pozitif, 7 negatif; başarı oranı %41,7 (%70 eşiğinin altında, "risk" ayı). "BIST Şubat ayını sevmiyor." (Ham). Grafikte 2015-2026 çubukları var; gönderi 2026-02-02 tarihli, yani 2026 Şubat çubuğu yarım aydır (YORUM). Parametre: XU100 Şubat: pozitif 5, negatif 7, toplam 12, başarı oranı %41,7, ortalama −%0,54, maksimum +%8,20, minimum −%11,03, standart sapma %5,02 (görsel, açıldı).
  - `tweet-aylik-mevsimsellik-olasilik-kasa-ayari-2009731947375854034` — Tekrar: aynı aylık mevsimsellik kuralı; bu gönderi Tansu'nun X gönderisidir (2026-01-09, id 2009731947375854034), yazar belirsizliği kalkar. "Hangi aylarda %70 ve üzeri ihtimalle yükseldiğine bakın (Yüksek Olasılık)." (Ham). Kasa oranları Nisan %80, Ağustos %30 örnektir (Ham: "Uygulama").
  - `tweet-aylik-ortalama-getiri-mevsimsellik-1911360286876925997` — Aylık mevsimsellik hesap yöntemi: Yahoo Finance aylık kapanıştan aylık % getiri, takvim ayı ortalaması, tek ay (Nisan) filtresi, ayın günlerine göre günlük ortalama. "Bir hisse senedinin belli bir ayda, örneğin Nisan ayında, tarihsel olarak kazandırma eğilimi olup olmadığını görmek için kullanır." (Ham). Çıktı yalnız grafik, eşik ve sonuç kuralı yok. Günlük grafikte x ekseni "Day of February", başlık "April" (görsel, açıldı; Tansu'nun kod etiketi hatası). Parametre: aylık getiri = (bu ay kapanış − önceki ay kapanış) / önceki ay kapanış, veri Yahoo Finance (Ham).

---

# Sıralama: koda en sadık geçirilebilecekler
1. **Sektör getiri liderleri + anomali temizleme (30/60/90, basit ort., |30g|>%50):** 30 günlük basit ortalama ve anomali eşiği görselde var (07); 60/90 günlük yöntem, evren ve N-gün tanımı eksik.
2. **Günlük sabit ağırlık rebalancing (50/40/10 tipi):** kural tam; emir zamanı ve maliyet eksik (YORUM ile doldurulur).
3. **Çift rotasyonu (VAKBN/CIMSA tarzı, long-only):** giriş ±2 + ΔZ dönüşü + T+1 Open tanımlı; ilk sinyale kadar nakit ("Piyasada Kalma +72.27%", GÖRSEL). Spread/pencere/β/sağlık eşikleri YORUM ile doldurulmalı; kod "Tansu'nun kuralı" değil "yaklaşık yeniden yapım" olur.
4. **BIST-VIX 5 adım listesi:** adım kuralları (SMA20/50, HA, VIX RSI(200)<SMA10, korelasyon<0, çıkış fiyat<SMA20 veya HA kırmızı) tanımlı; VIX "sakin" eşiği ve 2/4 kuralı eksik.
5. **Piyasanın Nabzı 4/5 skoru:** ilk beş kutu sayımı üretilebilir; RSI/AO eşikleri eksik.
6. **Corwin–Schultz spread (21g) ve referans yüzdelikleri:** hesaplanabilir; kural yok, gösterge.

# Boşluklar (kodlanamaz / çok belirsiz)
- Spread tanımı, hedge β, Z penceresi, Pair Quality/Health formülü, half-life, p-değeri penceresi, Z çıkış eşiği kesin değer, rotasyonda nakit çıkışı.
- Momentum dönüş onayının tam biçimi (tweet "ileride anlatacağım" diyor; yalnız ΔZ görsel kanıtı var).
- İki bacaklı AGROT/GARAN hedef oranı yalnız regresyon tahmini (≈1 : 0,38).
- Min-Vol/Max-Sharpe portföy, 161.700 tarama, 3 aşamalı portföy, ANN pipeline: parametresiz.
- SETUP x/100 puanı, NH-NL 5/5 skoru, VIX ofset bantları, "VIX AO" rolü, 16,99 limiti.
- BIST_VOL serisi: kaynağı tanımsız, bedava günlük veri doğrulanmadı.
- Hiçbir sistemde maliyet sonrası, OOS veya canlı kanıt yok.

## Aylık mevsimsellik: istatistiksel eleme tablosu (p-değeri, Sharpe, çarpıklık; Ocak, 13 hisse)
- **Kaynak:** `tweet-aylik-getiri-p-value-sharpe-skewness-eleme-2009899784748794098` (Ham ve görsel birinci el, görsel açıldı; Tansu'nun X gönderisi, 2026-01-10).
- **Tansu'nun ifadesi (verbatim):** "İstatistik ile bu noktaları belirlemek ve sizlerin bulacağı kesişimler ile teyitleşmelerini sağlamak ayrı bir güven verir." "Ocak ayı için KRDMB teknik ve istatistiksel olarak en sağlam dayanak." Eşik (Ham): "P-Value: 0.027 (<0.05)". Görsel sütunları (görsel, açıldı): T-Statistic, P-Value, İstatistiksel Anlamlı, Sharpe Ratio, Ortalama Kazanç (%), Ortalama Kayıp (%), Win/Loss Ratio, Skewness, Kurtosis, Normal Dağılım, Shapiro P-Value.
- **Tanım:** Bu bölüm, yukarıdaki "Aylık mevsimsellik" maddesine (pozitif kapanış olasılığı %70 ve üzeri) bir istatistik süzgeç katmanı ekler. Tablo Ocak ayı için 13 hisse satırı verir (AGHOL, ASTOR, AYES, BEYAZ, DURDO, EGEPO, GMTAS, GOLTS, KRDMA, KRDMB, KRONT, SDTTR, SEGMN).
  1. P-Value < 0.05 ise "İstatistiksel Anlamlı: Evet". Yalnız KRDMB geçer (t 2.549, p 0.027). Test türü yazılı değil; YORUM: geçmiş Ocak getirilerinin ortalaması sıfırdan farklı mı testi.
  2. Sharpe düşük ya da negatif ise zayıf halka (Ham: EGEPO −0.118; AYES 0.156 ve SEGMN 0.263; "Getiri riski karşılamıyor").
  3. Win/Loss Ratio = ortalama kazanç / ortalama kayıp (KRDMB 12.14 / 3.28 ≈ 3.70; görsel 3.71, yuvarlama farkı).
  4. Skewness işareti: pozitif = yukarı sürpriz potansiyeli, negatif = ani sert düşüş riski (Ham: ASTOR, DURDO, GMTAS pozitif; AGHOL, AYES negatif).
  5. Ortalama kayıp 0 ve Win/Loss INF olan hisseler (ASTOR, GMTAS) veri azlığı nedeniyle güvenilmez sayılır (Ham: "muhtemelen" 1-2 Ocak verisi). YORUM: ASTOR için t 1.995 ve p 0.1841 değerleri t-dağılımında df = 2 (3 Ocak) ile uyuşur (elle hesap: p = 1 − t / √(t² + 2) = 0.184); Ham'ın 1-2 Ocak tahmini bununla uyuşmaz.
  6. P-değeri sınırda olan BEYAZ (0.0536) "wild card" diye anılır: daha riskli, getiri potansiyeli yüksek (Ham). KRDMA'nın p-değeri de sınırdadır (0.0519, görsel); Ham onu anmaz.
- **Parametreler:**

| parametre | değer | kaynak |
|---|---|---|
| p-değeri eşiği | < 0.05 | Ham, görsel ("İstatistiksel Anlamlı") |
| Sharpe eşiği | yok | belirsiz |
| Win/Loss eşiği | yok | belirsiz |
| Skewness eşiği | yok (yalnız işaret) | Ham |
| minimum Ocak sayısı | yok | belirsiz |
| normallik testi | Shapiro, p sütunu (DURDO 0.0203; SEGMN boş) | görsel, açıldı |

- **Belirsiz kalanlar:** Her hissenin Ocak sayısı (n) ve yıl aralığı. Ocak 2026'nın dahil olup olmadığı (gönderi 10 Ocak 2026; YORUM: dahilse ay yarımdır). Aylık getirinin tanımı (kapanıştan kapanışa mı). Sharpe'ın yıllıklandırması. 13 hisse için çoklu test düzeltmesi yok (YORUM: tek bir p < 0.05 tesadüf olabilir). Giriş ve çıkış kuralı yok; tablo "dayanak" diye anılır. "Kesişimler ile teyit" için hangi göstergelerin kullanıldığı yazılı değil. 13 hissenin hangi evrenden seçildiği yazılı değil.
- **Tansu'nun kanıtı:** Tablo yalnız geçmiş Ocak getirisini özetler. İleriye dönük sınama yok. 13 hisseden yalnız biri anlamlıdır. Edge kanıtı yok.
- **Bedava veri:** Evet. Aylık getiri günlük kapanıştan çıkar. t-testi ve Shapiro için kütüphane gerekir; TASARIM §4 ile denetlenmedi (YORUM). Hazırlık K.
- **Güven:** Orta. Ham ve görsel birinci eldir ve sayılar uyumludur. Test türü ve örneklem büyüklüğü yazılı değildir.
