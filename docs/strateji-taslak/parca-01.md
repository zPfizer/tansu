# Parça 01: tweet-* (alfabetik ilk dilim, … tweet-harmonik-xb-…) keşfi

Durum: bitti (06.10.2026). Okuma: ham not + `assets/` görselleri. Not ile görsel çelişirse görsel esas.

Kapsam notu:
- Görev "ilk 44" dedi. `ls` ve Glob sırasıyla `tweet-9aydan-…` ile `tweet-harmonik-xb-…` arası **43 dosya** var; 44. dosya yok (bir sonraki `tweet-iskpl-…` parça 02'nin ilk dosyası). 43 dosya okundu.
- 32 dosya baştan sona okundu. 11 değerleme/bilanço/proje dosyasının yalnız kaynak bölümü okundu (asuzu, beklenen-fk, bist-hft, convex-hull, dea-vza, dusuk-korelasyon, fat-tail, froto, gordon, fcfe-ddm, cari-oran). Bunlar strateji değil ya da proje tanımı; kurallar ilk bölümde zaten tamdı.
- 6 görsel açıldı (ACSEL, engulfing kodu, A1CAP, SAYAS, KAPLM, Bollinger kitap sayfası). ASUZU'nun 4 görseli (değerleme) açılmadı.

Atıf notu (önemli): bu 43 notun yalnız 3'ünde X bağlantısı var (asuzu, beklenen-fk, bollinger; yazar @The_Tansu_). Diğerlerinde "Levent tarafından iletilen metin" yazıyor. Notlar tweet yazarını "Levent" diye anlatıyor (örnek: "Levent, … önerdi"). Bu yüzden aşağıdaki bütün kural metinleri **ikinci el**, yalnız görseldeki başlık/etiket/kod **birinci el**. Notlardaki "Cevo çıkarımı", "state machine", "backtest matrisi", Wilson/Bayes hesapları, "Not Doing" listeleri Tansu'nun sözü DEĞİLDİR; kartlara alınmadı.

## 1. Dosya tablosu (43)

Tür: strateji / çıkış / filtre / tarama / yapı taşı / strateji değil.

| # | Dosya (tweet-…md) | Tür | Tek satır |
|---|---|---|---|
| 1 | 9aydan-yilsonu-satis-net-kar-tahmini | strateji değil | Değerleme: önceki yıl satış × büyüme, kalan satış × marj + 9A kâr. Girdi eksik. |
| 2 | abcd-cd-bacagi-siddet-belirleyicileri | strateji değil | AB=CD'de CD bacağı şiddetini ne belirler? Araştırma sorusu, hipotez listesi; veri/sonuç yok. |
| 3 | abcd-geometrik-gecerlilik-kurallari | yapı taşı | AB=CD kapısı: BC ≤ AB, D, B'yi aşmalı, C sonrası A aşılırsa bozulur. |
| 4 | acsel-direnc-kirilimi-volume-profile-val | strateji | Direnç aşılırsa VAL'e hareket (koşullu senaryo). Görsel var, seviye okunamadı. |
| 5 | alark-125-42 | strateji | Trend kırılımı, bearish butterfly'a doğru, 125,42'ye kadar long. Oran yok. |
| 6 | algoritma-tasarimi-temelleri-trading-sistemleri | strateji değil | Mühendislik ilkeleri (amaç, veri, backtest, risk). Strateji yok. |
| 7 | arima-hiperparametre-acf-pacf-grid-search | strateji değil | ARIMA derece seçimi: itertools ızgarası + rolling doğrulama. |
| 8 | aritmetik-ortalama-outlier-rejim-tehlikesi | strateji değil | Ortalama uç gözleme kırılgan (19×100 + 50 → SMA20 97,5; medyan 100). Görüş; yapı taşı: medyan/MAD. |
| 9 | asuzu-coklu-degerleme-tutarliligi | strateji değil | ASUZU F/K, PD/DD, FD/FAVÖK tutarlılığı (X bağlantılı, 4 görsel). |
| 10 | atr-risk-butcesi-position-sizing-stop-loss | çıkış | Lot = risk TL / stop mesafesi; 2 ATR ilk stop; acil, gün sonu, iz süren stop. |
| 11 | aylik-getiri-mevsimsellik-piyasa-hafizasi | filtre | Aylık pozitif kapanış oranı %70+ olan aylarda maruziyeti ayarla (10–20 yıl). |
| 12 | beklenen-fk-coklu-regresyon-modeli | strateji değil | Büyüme, ROE, payout, beta, faizle beklenen F/K regresyonu (X bağlantılı). |
| 13 | bist-hft-colocation-quant-rekabet-kod-ogrenin | strateji değil | BIST'te HFT/colocation görüşü; "kod öğrenin". |
| 14 | bollinger-kuyruklari-ortalama-donus-var | strateji | ±2/−3 kuyruk = ortalamaya dönüş fırsatı + VaR limiti. Kural yok (X bağlantılı, 1 görsel). |
| 15 | bullish-engulfing-mum-kodu | yapı taşı | Tansu kodu: 4 katı open/close koşulu, `buy=1`. Tetik; giriş/stop yok. |
| 16 | cari-oran-likidite-acigi-bedelli-sermaye-artirimi | strateji değil | Cari oran < 1 → bedelli riski. Temel analiz kuralı; negatif filtre adayı, eşiği sayı değil oran < 1. |
| 17 | clenow-exponential-regression-momentum-bist-projesi | tarama | Log-fiyat OLS eğimi × R² momentum skoru; kod tam, lookback yok. |
| 18 | confluence-bagimsiz-kanit-yogunlugu | yapı taşı | "Confluence alanları daha güvenli" ilkesi. Tanım/faktör listesi yok. |
| 19 | convex-hull-dea-sektor-rotasyonu-projesi | tarama | Convex Hull + DEA ile sektör rotasyonu; proje niyeti, formül yok. |
| 20 | dea-vza-sektor-rotasyonu-malmquist-projesi | tarama | Sektör = DMU; girdi risk/volatilite/çarpan; çıktı getiri/alpha/temettü/momentum. Proje. |
| 21 | dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading | strateji | Üç aşamalı portföy: aday 10–20 → Max Sharpe 3–10 hisse (çekirdek %50+) → volatilite trading. |
| 22 | elliott-wave4-wave3-retracement-024-038-050 | yapı taşı | 4. dalga düşüşü = 3. dalga yükselişi × 0,24 / 0,38 / 0,50. Hedef merdiveni. |
| 23 | endeks-5of5-nhnl-corwin-schultz-likidite | filtre | Endeks raporu: skor 5/5, ADX 28,9, RSI 77,6, VIX 20,6, NH-NL; "Full Long". Eşik yok. |
| 24 | fat-tail-firsat-survival-konvekslik | strateji değil | "Herkesin olduğu yerde para yoktur"; fat-tail şokları fırsat. Genel görüş; kural yok. |
| 25 | fcfe-ddm-capraz-kontrol-degerleme-motoru | strateji değil | Python FCFE/DDM motoru anlatımı. Değerleme. |
| 26 | fibo-0618-bolge-h4-order-block-multitimeframe | strateji | Günlük Fib 0,618 bölgesi + H4 Order Block = "sniper giriş". Sayısal kural yok; video yok. |
| 27 | fibonacci-extension-abcd-kullanimi | yapı taşı | AB=CD hedefi için Fib extension (A1CAP görseli). |
| 28 | fiili-dolasim-yuzde-30-alti-stratejik-taramalar | tarama | Fiili dolaşım oranı < %30 evreninde taramalar; veri KAP. Tarama içeriği yok. |
| 29 | finans-muhendisligi-destek-direnc-seviye-motoru | yapı taşı | "Finans mühendisliği modelleriyle destek/direnç bulunur mu" proje fikri; model yok. |
| 30 | fiyat-hacim-fiili-dolasim-ucgeni | yapı taşı | "Fiyat ve hacim resmin 2/3'ü, fiili dolaşım resmi tamamlar." Formül notun (Cevo). |
| 31 | fiyatlar-trend-halinde-hareket-eder | strateji değil | Trend sürer, tepe/dip avcılığı yok. İlke; kural yok. |
| 32 | formasyon-arz-talep-confluence-kapisi | filtre | Yalnız kaliteli formasyon arz/talep bölgesiyle çakışırsa paylaş. Tanım yok. |
| 33 | froto-nakit-piyasa-degeri-18-89 | strateji değil | FROTO nakit/piyasa değeri %18,89 (ort. %17,17). Bilanço verisi. |
| 34 | garch-standart-sapma-volatilite-risk-minimizasyonu | strateji değil | "Bu akşam örnek göstereceğim" vaadi. İçerik yok. |
| 35 | gartley-butterfly-ayri-tarayicilar | strateji değil | Mimari ders: Gartley ve Butterfly ayrı taransın, ortak yalnız sonuç arayüzü. |
| 36 | gartley-d-tepki-penceresi-10-gun | çıkış | D'den 10 gün içinde tepki yoksa "belirsiz". SAYAS görseli (giriş D, stop X, TP1, TP2). |
| 37 | gordon-buyume-modeli-temettu-degerleme | strateji değil | Gordon: P0 = D1/(r−g). Eğitim. |
| 38 | gunluk-trade-breakout-gap-retest-volume-delta-atr-obv | strateji | Gün içi: kapanışla breakout + hacim/delta + retest; gap-and-go / gap-fill; ATR stop; OBV. |
| 39 | haftalik-bullish-gartley-talep-alani-tarama | tarama | Haftalık bullish Gartley, XABC tamam, C talep alanında, D hedefi var. |
| 40 | halftrend-buy-momentum-threshold-kapisi | strateji | `half_trend == "buy" and momentum > eşik`. İki gösterge de tanımsız. |
| 41 | hareketli-ortalama-ust-alt-trend-yon-filtresi | filtre | Fiyat MA üstünde → alış yönlü, altında → satış yönlü. MA tanımsız. |
| 42 | harmonik-momentum-squeeze-projesi | strateji değil | Harmonik + squeeze zamanlaması araştırma önerisi; kural/veri yok. |
| 43 | harmonik-xb-trend-kirilimi-stratejisi | strateji | X–B çizgisi kırılımı = D'ye kadar taktik pozisyon. KAPLM görseli. |

## 2. Aday modül kartları

Uygulanabilirlik: H = kural birinci elden belli, K = çekirdek belli yorum gerekir, X = formül yok.

### Kart 1: X–B trend çizgisi kırılımı (harmonik, D'ye kadar taktik)

- **Tür:** strateji (giriş tetiği; çıkış = D).
- **Kaynak:** `tweet-harmonik-xb-trend-kirilimi-stratejisi.md` + `assets/tweet-harmonik-xb-trend-kirilimi-stratejisi/01-kaplm-xb-trend-kirilimi.jpg`; `tweet-alark-125-42.md` (bearish karşılığı). X bağlantısı yok. Görsel birinci el (araç çıktısı); metin ikinci el.
- **Tansu'nun ifadesi:** görsel birebir: `KAPLM.IS - Eşleşen Patern (Bullish) [TAMAMLANDI]`; lejant `Trend Çizgisi (X->B uzatılmış)`. Not özeti: "X–B trend çizgisinin yapıya göre aşağı/yukarı kırılması short veya long pozisyon için kullanılabilir". ALARK notu özeti: "125,42'ye kadar long fırsatı", "bearish butterfly".
- **Kurallar:** X ve B'den çizgi çiz, uzat. Bullish yapıda çizgi aşağı kırılırsa D'ye kadar kısa; D'de tepki gelirse long adayı. Bearish yapıda çizgi yukarı kırılırsa D'ye kadar long (ALARK: hedef 125,42). Notun kendisi bu yön eşlemesini "Cevo çıkarımı" diye yazıyor; "AŞAĞI yönde kırılım" ve "SAT (taktik KISA, D'ye kadar)" etiketleri DGATE/SOKE görsellerinde birinci el (parça 04). Giriş fiyatı, stop, kırılım bazı (kapanış/fitil), tampon: yok. Zaman dilimi: günlük gibi (KAPLM Mart–Ağustos 2026 günlük mum; yazılmamış).
- **Sonuç (görsel):** KAPLM bullish Gartley XABC, okunan yaklaşık X≈330, A≈745, B≈500–505, C≈680, D≈420 (D etiketi `D: 424.23 …` kısmen okunuyor). Çizgi Haziran'da aşağı kırılıyor (kırmızı okla işaretli), fiyat Temmuz sonunda D'ye iniyor; D'den sonra tepki yok. İşlem getirisi gösterilmemiş.
- **Veri:** günlük OHLCV yeter.
- **Belirsizlik:** pivot (X, B) ayarı; kırılım bazı ve tolerans; stop; kısa pozisyonun kapanışı; BIST'te açığa satış (bizim kısıt).
- **Uygulanabilirlik: K.** Çizgi ve yön belli; giriş fiyatı, stop, kapanış kuralı yok. Tek örnek, sonuçsuz.

### Kart 2: Gartley D girişi, TP merdiveni ve D sonrası tepki penceresi

- **Tür:** strateji (giriş D, stop X) + çıkış (TP1, TP2) + tarama (haftalık aday sorgusu).
- **Kaynak:** `tweet-gartley-d-tepki-penceresi-10-gun.md` + `assets/tweet-gartley-d-tepki-penceresi/01-sayas-gartley-d-tepki-penceresi.jpg`; `tweet-haftalik-bullish-gartley-talep-alani-tarama.md`; `tweet-gartley-butterfly-ayri-tarayicilar.md`; `tweet-harmonik-momentum-squeeze-projesi.md` (yalnız araştırma önerisi). X bağlantısı yok. SAYAS görseli ve KAPLM üst notu birinci el; metinler ikinci el.
- **Tansu'nun ifadesi:** SAYAS görsel birebir: `SAYAS - Patern #2 Detaylı (Fibonacci + Trade Management) | Bullish (LONG) | Sistem: Carney`; lejant `Giriş (D)`, `Bk Stop (X)`, `TP1 (1:1 R/R)`, `TP2 (.618 CD)`. KAPLM üst notu birebir: `D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ)`; ikinci satır: `[Ek bilgi] C sonrası fiyat son 10 günde BEKLENEN yönde: DÜŞÜYOR (Bullish/AL paternde CD bacağı aşağı olmalı…` (satır sağda kesik). Not özeti: "D noktasından sonra 10 gün içinde beklenen yönde tepki oluşmazsa yapı belirsiz sayılabilir". Haftalık sorgu (not özeti): "haftalıkta talep alanıyla ilişkili, C'si oluşmuş, XABC'si tamam, D hedefi belirlenmiş bullish Gartley".
- **Kurallar:**
  - Giriş = D (limit), stop = X, TP1 = 1:1 R/R, TP2 = ".618 CD".
  - SAYAS okunan (etiketler küçük; seviyeler hesapla tutarlı): X≈20,65 (1,000 çizgisi), A≈144,25 (0,000), B≈68 (XA'nın ≈0,618'i), C≈122, D≈47,15 (0,786 çizgisi, XA'nın 0,786'sı). XA=123,6; 144,25 − 0,786×123,6 = 47,1.
  - TP1 ≈ 73–74 (D + (D−X) = 73,65). TP2 çizgisi görselde ≈106–107; bu D + 0,618×(A−D) = 107,2 ile tutarlı, D + 0,618×(C−D) ≈ 93 ile değil. Yani ".618 CD" etiketi A–D bacağı üzerinden okunuyor (çizgi yüksekliği pikselden ±3 yaklaşık).
  - Tepki penceresi: not 10 gün, KAPLM görseli 20 bar. Birim ve min. hareket yok.
  - Haftalık tarama: zaman dilimi haftalık; C'nin talep alanında olması (not "C noktasının uzun vadeli talep toplama alanında" der; D'nin talep alanıyla çakışması ayrı filtre).
  - Gartley oranları bu notlarda yok (tablo `gorsel-paket-123`, parça 06 kapsamı).
- **Sonuç (görsel):** SAYAS: D 0,786 çizgisine (~47) varıyor (eksen Oca 2025 civarı), sonra 2025–2026 boyunca yaklaşık 30–60 bandında yatay, Haziran–Temmuz 2026'da ~70'e tırmanıyor. TP1 çizgisine (~73) ulaşıp ulaşmadığı okunamadı. İşlem getirisi yok. KAPLM'de D'den tepki yok.
- **Veri:** günlük/haftalık OHLCV yeter.
- **Belirsizlik:** pivot ayarı, oran toleransı, "10 gün" birimi ve başlangıcı, tepkinin asgari büyüklüğü, talep alanı üretimi, TP2 çapası (A–D mi C–D mi).
- **Uygulanabilirlik: K.** Giriş/stop/TP birinci elden belli (SAYAS); Gartley oranları, tolerans, pivot ve tepki eşiği yok.

### Kart 3: AB=CD geometri kapısı ve Fibonacci extension hedefi

- **Tür:** yapı taşı + giriş adayı (C'den D'ye).
- **Kaynak:** `tweet-abcd-geometrik-gecerlilik-kurallari.md`, `tweet-fibonacci-extension-abcd-kullanimi.md` + `assets/tweet-fibonacci-extension-abcd-kullanimi/01-a1cap-fibonacci-extension-abcd.png`, `tweet-abcd-cd-bacagi-siddet-belirleyicileri.md` (yalnız soru). X bağlantısı yok. A1CAP görseli birinci el; kural metni ikinci el.
- **Tansu'nun ifadesi:** not özeti: "BC bacağı AB bacağının uzunluğunu aşamaz"; BC/AB tam 1,00 geçerli; "D, CD yönünde B noktasını aşmalıdır"; C sonrası fiyat A'yı BC yönünde aşarsa pattern bozulur. Extension notu: "Fibonacci extensionlar öğrenilmeli, AB=CD ile kullanılmalı". Görsel birebir: `A1CAP - Swing Yapısı, Fibonacci ve Range/Breakout Analizi (Yükseliş) | Harmonik sayı: 6.31 TL`; lejant `Swing (X -> A)`, `AB+CD Paterni`.
- **Kurallar:**
  - `BC/AB ≤ 1,00`; D, AB yönünde B'nin ötesinde; C sonrası A aşılırsa geçersiz.
  - Hedef: D(r) = C + r·(B−A), `r` = 1,00 / 1,27 / 1,618 (r aday listesi "sonraki açıklama"dan, `gorsel-paket-39`, parça 04); notta bu formül "Cevo çıkarımı". BC aday oranları 0,382 / 0,50 / 0,618 aynı yerden.
  - Bozulmanın fitil mi kapanış mı olduğu yok. Zaman dilimi yok.
- **Sonuç (görsel):** A1CAP: A≈15,3 → B≈9,1 → C≈12,3 (okunan, yaklaşık), noktalı D projeksiyonu ≈6,1–6,3'e iniyor; üç "ext" etiketli seviye yaklaşık 8,8 / 7,9 / 6,8 (küçük etiket, kesin okunamadı). Gerçek fiyat Ağustos'ta ≈8 civarı. `Harmonik sayı: 6.31 TL` D hedefine ya da AB mesafesine (≈6,2–6,3) yakın; notun "tanımsız" demesi doğru, tanım okunamadı. Getiri yok.
- **Veri:** günlük OHLCV yeter.
- **Belirsizlik:** pivot ayarı, oran toleransı, giriş (C'den mi D'den mi), stop, hedef çıkış kuralı.
- **Uygulanabilirlik: K** (geometri kapısı H; giriş/stop yok). SMRTG/ISKPL sonuçları bu parçada değil (parça 02/04).

### Kart 4: Elliott 4. dalga geri alım merdiveni

- **Tür:** yapı taşı (hedef/bölge); giriş yok.
- **Kaynak:** `tweet-elliott-wave4-wave3-retracement-024-038-050.md`. X bağlantısı yok; görsel yok; ikinci el.
- **Tansu'nun ifadesi (not özeti):** "3. dalgada yükselen miktarın %24, %38, %50'si 4. dalgada geri alınabilir"; örnek: 3. dalga 100 birim → düşüş 24/38/50 birim.
- **Kurallar:** P4 = P3 − r·(P3−P2), r ∈ {0,24; 0,38; 0,50} (Fibonacci karşılığı 0,236/0,382/0,500 notun açıklaması). Bearish için aynı formül işaretli. Standart itkide 4. dalga 1. dalga alanına girmemeli (notun Elliott kuralı, Tansu'nun değil). Pivot, giriş, stop, zaman dilimi: yok.
- **Sonuç:** yok. (`ENJSA %54,0` başlığı başka paket, parça 06.)
- **Veri:** günlük OHLCV yeter; dalga sayımı otomasyonu zor.
- **Belirsizlik:** P2/P3 pivot seçimi, hangi r'nin kullanılacağı, tetik.
- **Uygulanabilirlik: K.** Formül H; dalga sayımı ve giriş X.

### Kart 5: Günlük Fib 0,618 bölgesi + H4 Order Block

- **Tür:** strateji.
- **Kaynak:** `tweet-fibo-0618-bolge-h4-order-block-multitimeframe.md`. X bağlantısı yok; video atıf var ama notta yok ("REFERENCED_NOT_PROVIDED"); ikinci el.
- **Tansu'nun ifadesi (not özeti):** "Fibonacci 0,618 bir duvar değil bölge"; "Matematiksel oran (Fibo) + Piyasa Yapısı (Order Block) = Sniper Giriş".
- **Kurallar:** günlük 0,618'den dönüş beklenirken wick, daha derindeki H4 Order Block'u test edebilir; Fib + OB çakışması giriş adayı. Sayı yok (0,618 dışında). Fib çapası, bölge genişliği, OB tanımı, tetik, stop: yok.
- **Sonuç:** yok.
- **Veri:** günlük + 4 saatlik OHLC. 4 saatlik veri bedava günlükte yok.
- **Belirsizlik:** hemen her şey.
- **Uygulanabilirlik: X.**

### Kart 6: Direnç kırılımı + Volume Profile VAL hedefi (ACSEL)

- **Tür:** strateji (koşullu senaryo).
- **Kaynak:** `tweet-acsel-direnc-kirilimi-volume-profile-val.md` + `assets/tweet-acsel-direnc-kirilimi-volume-profile-val/01-acsel-direnc-volume-profile-val.png`. X bağlantısı yok. Görsel birinci el.
- **Tansu'nun ifadesi (not özeti):** direnç aşılırsa, mevcut hacim düşük olsa da VAL'e doğru hareket potansiyeli; harmonik yapı tek başına garanti değil.
- **Kurallar:** direnç kırılımı = tetik; hedef = VAL. Görselde: üstte sarı arz, altta mavi talep bölgesi, düşen kırmızı kesikli direnç çizgileri, kırmızı oklar, sağda yatay hacim profili (üstü seyrek, kırmızı kutulu), lejantta Gaussian VP (POC/VAH/VAL) ve talep/arz bölgeleri. Fiyat eksen Mayıs–Ağustos 2026. Seviyeler, VAL fiyatı, profil aralığı okunamadı. Stop yok.
- **Sonuç:** yok (kırılım olmamış, senaryo).
- **Veri:** gerçek hacim profili gün içi işlem ister; günlük OHLCV ile yaklaşık profil kurulur (araç "Gaussian VP", formülü bilinmiyor).
- **Belirsizlik:** kırılım tanımı, profil penceresi ve value-area yüzdesi, stop, zaman dilimi.
- **Uygulanabilirlik: X.**

### Kart 7: Günlük trade breakout / gap / retest

- **Tür:** strateji (gün içi) + yapı taşı (breakout, gap, OBV, ATR).
- **Kaynak:** `tweet-gunluk-trade-breakout-gap-retest-volume-delta-atr-obv.md`. X bağlantısı yok; görsel yok; ikinci el.
- **Tansu'nun ifadesi (not özeti):** breakout = VAH, direnç veya trend çizgisi üstüne kararlı kapanış; teyit hacim veya delta; temiz giriş retest; gap'ler destek/direnç gibi; runaway/gap-and-go ile gap-fill ayrı; rising window alt sınırı destek, falling window üst sınırı direnç; ATR stop; OBV teyit.
- **Kurallar:** sıra: seviye kırılır → kapanış kabulü → hacim/delta teyidi → retest girişi. Gap: kapanıştan açılışa fark, doldurma ya da devam. Stop ATR'ye göre. Hiç sayı yok (ATR çarpanı, pencere, "kararlı" tanımı, hacim eşiği yok). Zaman dilimi "günlük trade" (gün içi).
- **Sonuç:** yok.
- **Veri:** breakout, gap, OBV, ATR günlük OHLCV'den çıkar. Delta tick/aggressor verisi ister (bedava yok). VAH gün içi profil ister.
- **Belirsizlik:** kırılımın "kararlı" tanımı, retest şartı, gap kimliği (açılış mı boşluk mu), hedef, stop çarpanı.
- **Uygulanabilirlik: K** (yalnız günlük OHLCV alt kümesi). Delta kolu X.

### Kart 8: Bullish engulfing dedektörü

- **Tür:** yapı taşı (giriş tetiği).
- **Kaynak:** `tweet-bullish-engulfing-mum-kodu.md` + `assets/tweet-bullish-engulfing-mum-kodu/01-bullish-engulfing-kodu.png`. X bağlantısı yok. **Birinci el** (Tansu'nun kod görseli).
- **Tansu'nun ifadesi (görsel, birebir okundu):** `def signal(data, open_column, close_column, buy_column, sell_column):` döngü `i` = 1'den; koşul: `close[i] > open[i]` ve `close[i-1] < open[i-1]` ve `open[i] < close[i-1]` ve `close[i] > open[i-1]`; eşleşirse `buy_column = 1`; `try … except: pass`; `sell_column` kullanılmıyor.
- **Kurallar:** 4 katı eşitsizlik, yalnız gövde, fitil yok. Giriş zamanı, stop, hedef, trend/bölge bağlamı: yok.
- **Sonuç:** yok.
- **Veri:** günlük OHLC yeter.
- **Belirsizlik:** işlemin ne zaman yapılacağı (sonraki açılış? AOF?), çıkış, bağlam.
- **Uygulanabilirlik: H** (tetik). Strateji olarak X (stop/çıkış yok).

### Kart 9: HalfTrend "buy" + momentum eşiği

- **Tür:** strateji (giriş filtresi çifti).
- **Kaynak:** `tweet-halftrend-buy-momentum-threshold-kapisi.md`. X bağlantısı yok; görsel yok. Notta kod Tansu'ya atfedilmiyor: "Levent'in beğendiği minimal confluence". Atıf belirsiz.
- **Tansu'nun ifadesi (not içi kod):** `if half_trend[t] == "buy" and momentum[t] > momentum_threshold:  # Nice`.
- **Kurallar:** iki koşul AND → long adayı. HalfTrend parametresi (amplitude), durum mu olay mı, momentum formülü, pencere, eşik: yok. Çıkış, stop: yok.
- **Sonuç:** yok.
- **Veri:** HalfTrend ve momentum günlük OHLCV'den hesaplanır.
- **Belirsizlik:** hepsi; Tansu'nun kuralı olduğu bile doğrulanamadı.
- **Uygulanabilirlik: K (zayıf).** Mantık belli, iki gösterge tanımsız. Tansu'ya atıf yoksa çıkarılmalı.

### Kart 10: Hareketli ortalama yön filtresi

- **Tür:** filtre.
- **Kaynak:** `tweet-hareketli-ortalama-ust-alt-trend-yon-filtresi.md`. X bağlantısı yok; ikinci el.
- **Tansu'nun ifadesi (not özeti):** "Piyasa hareketli ortalamanın altındaysa satış yönlü, üzerindeyse alış yönlü işlem"; "Trend is your friend".
- **Kurallar:** kapanış > MA → long yönü; kapanış < MA → sat/kaçın. MA türü, periyot, zaman dilimi, eşitlik, giriş/çıkış: yok.
- **Sonuç:** yok.
- **Veri:** günlük OHLCV yeter.
- **Belirsizlik:** MA türü ve periyodu (bizim yorum), "satış yönlü" = açığa satış mı pozisyon azaltma mı.
- **Uygulanabilirlik: K.**
- Aynı ailede, strateji değil sayılan: `tweet-fiyatlar-trend-halinde-hareket-eder.md` (ilke: ters sinyale kadar trendde kal; kural yok).

### Kart 11: Clenow tipi üstel regresyon momentum sıralaması

- **Tür:** tarama (sıralama).
- **Kaynak:** `tweet-clenow-exponential-regression-momentum-bist-projesi.md`. X bağlantısı yok; görsel yok; kod notta metin. İkinci el. Atıf: "Levent … paylaştı"; kitap atfı (Clenow, *Stocks on the Move*) doğrulanmadı.
- **Tansu'nun ifadesi (not içi kod):**
  `r = np.log(price_array); slope, _, rvalue, _, _ = linregress(np.arange(len(r)), r); annualized = (1 + slope) ** 252; return annualized * (rvalue ** 2)`
- **Kurallar:** log-fiyata zamanla OLS; skor = (1+eğim)^252 × R². Lookback, evren, kaç hisse, ağırlık, yeniden dengeleme, maliyet: yok. Not: planlanan BIST denemesi.
- **Sonuç:** yok (plan). Notun sentetik fixture'ı Cevo'nun: pürüzlü yükseliş (0,777) ile kusursuz düşüş (0,777) aynı skoru alıyor; yön kapısı gerekir (bizim yorum).
- **Veri:** günlük OHLCV yeter.
- **Belirsizlik:** lookback, negatif eğim politikası, portföy kuralı.
- **Uygulanabilirlik: K.** Skor fonksiyonu H; seçim ve rebalans X.

### Kart 12: Bollinger alt kuyruk / ortalamaya dönüş + VaR

- **Tür:** strateji (zayıf) + yapı taşı.
- **Kaynak:** `tweet-bollinger-kuyruklari-ortalama-donus-var.md` + `assets/tweet-2087267070752760121/01-normal-dagilim-se-68-95-997.png`. X: https://x.com/The_Tansu_/status/2087267070752760121 (11.08.2026 22:57). X metni notta tırnaklı yok, özet var; görsel birinci el (kitap sayfası).
- **Tansu'nun ifadesi:** not özeti: normal dağılım kuyrukları Bollinger bantları, ortalamaya dönüş fırsatları ve portföy VaR limitiyle ilişkilendiriliyor; "−2SE/−3SE" ifadesi. Görsel birebir: `Örneklem Ortalamalarının Frekans Dağılımı`, `Popülasyon ortalaması, μ`, ±1/2/3 SE, `%68`, `%95`, `%99,7`.
- **Kurallar:** yok. Periyot, k, giriş, çıkış, VaR güven düzeyi, ufuk: yok. (SE ≠ SD ve z ≤ −2 aday olayı: notun düzeltmesi, Cevo.)
- **Sonuç:** yok.
- **Veri:** günlük OHLCV yeter.
- **Belirsizlik:** her şey.
- **Uygulanabilirlik: X.**

### Kart 13: ATR risk bütçesi, lot ve stoplar (çıkış/risk)

- **Tür:** çıkış / risk.
- **Kaynak:** `tweet-atr-risk-butcesi-position-sizing-stop-loss.md`. X bağlantısı yok; görsel yok; kod parçası notta. İkinci el.
- **Tansu'nun ifadesi (not özeti ve kod):** kabul edilebilir kayıptan lot hesapla; örnek "500 TL / 2 TL = 250 lot"; ilk stop fiyatın "2 ATR" altı; acil stop intraday dokunuşla; kapanış (gün sonu) stopu; trailing stop yükselen fiyatla. Kod: `stop_level = data['Close'].iloc[-1] - (2 * atr.iloc[-1])`.
- **Kurallar:** lot = risk bütçesi (TL) / hisse başına stop mesafesi (TL); ilk stop = giriş − 2 × ATR; acil stop: gün içi dokunuşta çık; gün sonu stop: tamamlanmış kapanış seviyenin altındaysa; iz süren stop: yalnız yukarı. ATR penceresi, trailing çarpanı, gün sonu stop seviyesi: yok. Zaman dilimi: not "intraday" etiketli, örnek günlük gibi.
- **Sonuç:** yok.
- **Veri:** günlük OHLCV yeter (acil stop gün içi dokunuş sınamada günlük yüksek/düşük ile yaklaşır).
- **Belirsizlik:** "2 TL" 2×ATR mesafesi mi ATR mi (notta iki okuma: 250 mi 125 lot mu); ATR periyodu; gün sonu stop seviyesi.
- **Uygulanabilirlik: K.** Lot formülü ve 2 ATR H; ATR penceresi, trailing ve gün sonu seviyesi YORUM.

### Kart 14: Aylık mevsimsellik filtresi

- **Tür:** filtre (takvim).
- **Kaynak:** `tweet-aylik-getiri-mevsimsellik-piyasa-hafizasi.md`. X bağlantısı yok; görsel yok; ikinci el. Notun Wilson/Bayes/çoklu test hesapları Cevo'nun.
- **Tansu'nun ifadesi (not özeti):** 10 yılın 8'inde pozitif Ocak, kötü Eylül, "Sell in May", Nisan %80 ve Ağustos %30 maruziyet örnekleri; son 10–20 yılda aylık getirileri çıkarıp %70+ pozitif oranlı ayları izle.
- **Kurallar:** her takvim ayı için son 10–20 yıl pozitif kapanış oranı; ≥ %70 olan ay "yüksek olasılıklı", kasa oranını ona göre ayarla (örnek: iyi Nisan %80, zayıf Ağustos %30 yatırımda). Varlık/endeks, oran eşiğinin altı için kural, giriş/çıkış günü: yok. "%80/%30" örnektir, kural değil.
- **Sonuç:** yok (8/10 Ocak sözlü).
- **Veri:** günlük OHLCV'den aylık kapanış getirisi; 10–20 yıllık tarih şart (BIST için düzeltilmiş seri).
- **Belirsizlik:** hangi varlık, eşiğin kasa oranına çevrilmesi, yıl sayısı 10 mu 20 mi.
- **Uygulanabilirlik: K.**

### Kart 15: Endeks "bugün ne anlatıyor" skoru (piyasa filtresi)

- **Tür:** filtre.
- **Kaynak:** `tweet-endeks-5of5-nhnl-corwin-schultz-likidite.md`. X bağlantısı yok; görsel yok; ikinci el.
- **Tansu'nun ifadesi (not özeti):** başlık "Bugün endeks bana ne anlatıyor?"; genel skor 5/5, ADX 28,9, RSI 77,6, VIX 20,6, 20 günlük NH-NL 83, 65 günlük NH-NL "Katılım Yok", XU100 Corwin–Schultz ort. spread %1,06; sonuç "Full Long; likit endeks liderlerinde kal; düşük hacim ve zayıf 65 günlük katılım nedeniyle yan hisselerde agresifleşme; sigma sıçramasını izle".
- **Kurallar:** yok. 5 bileşenin kimliği, eşikler, "83" fark mı oran mı, sigma tanımı yok. "Bugün" tarihi yok.
- **Sonuç:** tek anlık görüntü.
- **Veri:** NH-NL için XU100 bileşenlerinin günlük OHLC'si (sağkalım yanlılığı sorunu); VIX = ABD VIX; Corwin–Schultz günlük yüksek/düşükten hesaplanır.
- **Belirsizlik:** tamamı.
- **Uygulanabilirlik: X.**

### Kart 16: Düşük fiili dolaşım evreni (<%30) ve float turnover

- **Tür:** filtre (evren) + yapı taşı (float turnover); "stratejik taramalar" X.
- **Kaynak:** `tweet-fiili-dolasim-yuzde-30-alti-stratejik-taramalar.md`, `tweet-fiyat-hacim-fiili-dolasim-ucgeni.md`. X bağlantısı yok; görsel yok; ikinci el. Tablo görseli: `gorsel-paket-08` (parça 04).
- **Tansu'nun ifadesi (not özeti):** fiili dolaşım yalnız anlatılmamalı, taranmalı; eşik %30 altı hisselerde çeşitli taramalar yapılabilir; veriler KAP'tan alınabiliyor; "fiyat ve hacim resmin üçte ikisi, fiilen işlem görebilen hisse sayısı resmi tamamlar".
- **Kurallar:** evren = fiili dolaşım **oranı** < 0,30 (notun normalizasyonu; Tansu "pay adedi" diyor gibi okunuyor). Hangi taramaların yapılacağı yok; `float_turnover = hacim / fiili dolaşım payı` formülü Cevo'nun. Beş "stratejik tarama" Cevo'nun önerisi, Tansu'nun değil.
- **Sonuç:** yok (önceki tablodaki KENT %0,54, GARAN %13,98 bu notta anılıyor).
- **Veri:** günlük OHLCV yetmez; KAP fiili dolaşım oranı ve tarihçesi (anlık değer geriye taşınamaz).
- **Belirsizlik:** eşiğin %30'u "oran" mı "adet" mi; tarama içerikleri.
- **Uygulanabilirlik: H** yalnız evren filtresi olarak (veri ayrı); taramalar **X**.

### Kart 17: Formasyon + arz/talep çakışma kapısı ve confluence

- **Tür:** filtre (ilke); yapı taşı (confluence).
- **Kaynak:** `tweet-formasyon-arz-talep-confluence-kapisi.md`, `tweet-confluence-bagimsiz-kanit-yogunlugu.md`. X bağlantısı yok; ikinci el.
- **Tansu'nun ifadesi (not özeti):** "önceki gün uygun kurulum bulamadı; yeni paylaşımı ancak kaliteli bir formasyon arz veya talep bölgesiyle çakışırsa yapacak"; "confluence alanları daha güvenlidir; birden fazla bağımsız teknik faktör aynı fiyat seviyesinde buluşur".
- **Kurallar:** yok. "Kaliteli formasyon", "çakışma", faktör listesi, eşik: yok. Faktör aileleri, olasılık çarpımı, ceza formülleri Cevo'nun.
- **Sonuç:** yok.
- **Veri:** günlük OHLCV (bölge ve formasyon), hacim.
- **Uygulanabilirlik: X.** Sınama tasarımı için ilke olarak kullanılır (formasyonu bölge şartıyla ve şartsız karşılaştır).

### Kart 18: Üç aşamalı portföy (düşük korelasyon, yüksek volatilite → Max Sharpe → volatilite trading)

- **Tür:** strateji (portföy).
- **Kaynak:** `tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading.md`. X bağlantısı yok; görsel yok; ikinci el ("kitapların yazmadığı tecrübe").
- **Tansu'nun ifadesi (not özeti):** Aşama 1: düşük korelasyon ve yüksek volatiliteyle 10–20 aday. Aşama 2: Markowitz/etkin sınır/Max Sharpe ile 3–10 nihai hisse, bir çekirdek hissenin %50+ ağırlığı. Aşama 3: stratejik ağırlığı koruyarak RSI/Bollinger/ortalamaya dönüşle volatilite trading.
- **Kurallar:** sayılar: 10–20 aday, 3–10 hisse, çekirdek ≥ %50. Korelasyon ve volatilite eşiği, lookback, getiri tahmini, risksiz faiz, RSI/Bollinger eşikleri, yeniden dengeleme: yok.
- **Sonuç:** yok (notun el örneği sentetik, Cevo).
- **Veri:** günlük OHLCV yeter.
- **Belirsizlik:** aşama 1 ve 3'ün tamamı.
- **Uygulanabilirlik: K (zayıf).** Aşama 2 `scipy.optimize` ile kodlanır; aşama 1 ve 3 X.

### Kart 19: Sektör rotasyonu: DEA/VZA (+ Convex Hull)

- **Tür:** tarama (sektör sıralaması).
- **Kaynak:** `tweet-dea-vza-sektor-rotasyonu-malmquist-projesi.md`, `tweet-convex-hull-dea-sektor-rotasyonu-projesi.md`. X bağlantısı yok; ikinci el.
- **Tansu'nun ifadesi (not özeti):** Sektörler karar verme birimi; girdi: risk, volatilite, çarpanlar; çıktı: getiri, alpha, temettü, momentum; etkin sektörler portföye, skor düşünce rotasyon; Malmquist ile dinamik verimlilik; PyDEA/SciPy; Convex Hull ile DEA birlikte "çok güçlü sonuçlar".
- **Kurallar:** yok (model türü, yönelim, ufuk, evren, kaç sektör). 
- **Sonuç:** yok ("muazzam sonuçlar" beklenti).
- **Veri:** çarpanlar (F/K, PD/DD) bilanço verisi ister; OHLCV yetmez. Sektör üyeliği ayrı kaynak.
- **Uygulanabilirlik: X.**

## 3. Strateji olmayan notlar (tek satır)

- 9aydan, asuzu, beklenen-fk, fcfe-ddm, gordon, froto, cari-oran: değerleme/bilanço (cari oran < 1 → bedelli riski: ileride bilanço filtresi adayı, sayı yok).
- algoritma-tasarimi, arima, garch, bist-hft, fat-tail, aritmetik-ortalama: eğitim/görüş/yöntem vaadi.
- abcd-cd-bacagi, harmonik-momentum-squeeze: araştırma sorusu; veri/kural yok.
- gartley-butterfly-ayri-tarayicilar: yazılım mimarisi kararı (iki ayrı tarayıcı).
- finans-muhendisligi S/R motoru: proje fikri; model verilmemiş.

## 4. Ortak yapı taşları (bu parçada geçenler)

1. Pivot/swing (tepe-dip) bulma: kart 1, 2, 3, 4. Ayar hiçbir yerde yok.
2. Fibonacci geri alım ve extension: 0,618 (kart 5), 0,236/0,382/0,50 (kart 4), extension 1,0/1,27/1,618 (kart 3).
3. Trend çizgisi (X–B): kart 1.
4. XABCD geometri (Gartley, Butterfly, AB=CD) ve durum etiketleri: kart 1, 2, 3.
5. Arz/talep bölgesi (distal/proximal), Order Block, FVG: kart 2, 5, 17.
6. Hacim profili (POC, VAH, VAL): kart 6, 7.
7. Breakout, retest, gap tanımı; OBV; ATR: kart 7, 13.
8. Mum dedektörü (engulfing): kart 8.
9. Log-regresyon eğimi ve R²: kart 11.
10. Band/z-skor (Bollinger), medyan/MAD (aritmetik-ortalama notu): kart 12.
11. Fiili dolaşım oranı, float turnover: kart 16.
12. NH-NL, Corwin–Schultz, ADX, RSI: kart 15.
13. Takvim ayı pozitif oran: kart 14.

Aynı fikrin başka notlarda geçtiği yerler:
- **ATR / 2 ATR stop:** kart 13 ve kart 7. Önceki okuma 2 ATR'yi `gorsel-paket-115` (NotebookLM) bağlıyor.
- **Bölge + formasyon çakışması:** kart 17, kart 2 (talep alanı), kart 5, kart 6.
- **Trend/MA:** kart 9, 10, 15 (ADX/RSI), 31 numaralı `fiyatlar-trend` ilkesi.
- **Ortalamaya dönüş:** kart 12 ve kart 18 (aşama 3).
- **Volatilite şoku freni:** `tweet-volatilite-piyasa-soku-yeni-alim-freni` (parça 02); kart 15 "sigma sıçramasını izle".
- **D sonrası tepki penceresi:** kart 1 ve 2 (KAPLM görseli ve SAYAS notu).

## 5. Önceki okumayla (docs/KURALLAR.md, docs/kurallar/) karşılaştırma

Ham kaynak önceliklidir. Aşağıdakiler bu parçada çıkan fark ya da eksiklerdir.

1. **10 gün / 20 bar "çelişkisi" tek çelişki olmayabilir.** KURALLAR §2 ve C-10 bunu not (10 gün) ile görsel (20 bar) arasında çelişki sayıyor. KAPLM görselinin üst notunda ikisi aynı araç çıktısında: `20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ)` ve ikinci satır `C sonrası fiyat son 10 günde BEKLENEN yönde: DÜŞÜYOR …`. Yani 10 gün, D'den sonraki pencere değil, "C sonrası son 10 gün yön" testi olabilir; 20 bar D sonrası tepki penceresi. İkisi araçta birlikte var. Çözüm: ikisini ayrı parametre say.
2. **SAYAS TP2.** Önceki okuma TP kaynaklarını çelişkili buluyor (CD / AD). SAYAS görselinde ".618 CD" etiketli çizginin yüksekliği ≈106–107 okunuyor; bu D + 0,618·(A−D) = 107,2 ile uyuyor, D + 0,618·(C−D) ≈ 93 ile uymuyor. Yani Tansu'nun aracı etiketi "CD" yazsa da çizgiyi A–D üzerinden çiziyor görünür (piksel okuması, ±3). TP1 ≈ 73–74 = D + (D−X), 1:1 R/R ile tutarlı. Bu, C-§7'deki "AD'nin %61,8'i" satırını destekliyor.
3. **2 ATR yalnız NotebookLM değil.** KURALLAR "Risk ve çıkış" tablosu %1 risk, lot = risk/(2 ATR) ve 2 ATR acil stopu NotebookLM infografiğine bağlıyor. `tweet-atr-risk-butcesi…` notu 2×ATR ilk stopu, acil stopu, gün sonu stopu ve trailing'i ikinci elden de veriyor. Bu notta %1 risk ve SMA250 yok; ikisi yalnız NotebookLM'den geliyor.
4. **Önceki okumada hiç olmayan notlar (bu parçada keşfedildi):** fiili dolaşım <%30 evreni ve float turnover (kart 16), aylık mevsimsellik (kart 14), düşük korelasyon + Max Sharpe portföyü (D-dosyasında var, burada kart 18), DEA/VZA ve Convex Hull sektör rotasyonu (kart 19), formasyon/confluence ilkesi (kart 17, sadece A-§16'da anılıyor). `tweet-acsel…` A-§303'te "okunmadı" idi; burada okundu (kart 6).
5. **Aynı konuda tutarlı bulgular:** engulfing kodu görselden birebir aynı (kart 8); Elliott 0,24/0,38/0,50 aynı (kart 4); KAPLM D≈420 ve "TEPKİ GELMEDİ" aynı (kart 1); Bollinger'da kural yok (kart 12); Clenow kodu aynı (kart 11).
6. **HalfTrend:** önceki okuma "K, atfı belirsiz" diyor. Bu parçada da K (zayıf); notta kodun "Levent'in beğendiği" diye geçmesi Tansu'ya atfı daha da zayıflatıyor.
7. **A1CAP "Harmonik sayı: 6.31 TL":** not "yorumlanmadı" diyor. Görselde noktalı D projeksiyonu ≈6,1–6,3'e iniyor; sayı D hedefi ya da AB mesafesi olabilir. Kesin değil.

## Tansu'nun bakış açısı (ipuçları)

Uyarı: alıntılar notlardaki "Kaynak" cümleleridir (aktarım; öznesi çoğunlukla "Levent"). Yalnız görsel etiketleri ve `Herkesin olduğu yerde para yoktur` gibi tırnaklı ifadeler Tansu'ya daha yakın. "Yorum:" satırları benimdir.

**Piyasaya bakış: trend, ortalama, kuyruk**
- "Bir hareket başladıktan sonra ters sinyal oluşana kadar trend yönünde kalma yaklaşımını vurguladı." (fiyatlar-trend-halinde-hareket-eder)
- "Görevin tepe veya dip tahmin etmek değil; dönüşü gözlemek, harekete katılmak ve bozulmada ayrılmak olduğunu belirtti." (aynı)
- "Piyasa hareketli ortalamanın altındaysa satış yönlü, üzerindeyse alış yönlü işlem yapılmalıdır." / "Ana ilke: `Trend is your friend`." (hareketli-ortalama-ust-alt-trend-yon-filtresi)
- "Levent gereksiz karmaşıklığa karşı en sade trend kuralını verdi." (aynı)
- "aritmetik ortalamanın finansal veride uç gözlemlere kırılgan olduğunu ve bunun en çıplak tehlikesini anlattı." (aritmetik-ortalama-outlier-rejim-tehlikesi)
- "Herkesin olduğu yerde para yoktur"; "En büyük kârlar Fat Tails alanında yapılır" (Soros'a atfedilmiş); zamanın %95'i normal, %5'i şok. (fat-tail-firsat-survival-konvekslik)
- "normal dağılım kuyruklarını Bollinger bantları, ortalamaya dönüş fırsatları ve portföy VaR limitiyle ilişkilendiriyor" (bollinger-kuyruklari-ortalama-donus-var)
- "büyük fon/algoritma döneminde küçük yatırımcının piyasa hafızasını aylık getiri istatistikleriyle okuyabileceğini anlattı." (aylik-getiri-mevsimsellik-piyasa-hafizasi)
- Yorum: trendde kal, tepe/dip avlama; ortalamaya dönüşü ve uç olayı ise ayrı ve kuyruğu ciddiye alan bir lens olarak tutuyor. Trend ile fat-tail fırsatı arasındaki ilişki (şokta alım mı, yeni alım freni mi) notlarda çözülmemiş.

**Kurulum seçimi: confluence, bağımsızlık, bölge**
- "confluence alanları daha güvenlidir; çünkü birden fazla bağımsız teknik faktör aynı fiyat seviyesinde buluşur." (confluence-bagimsiz-kanit-yogunlugu)
- "yeni bir paylaşımı ancak kaliteli bir formasyon arz veya talep bölgesiyle çakışırsa yapacağını bildiriyor." (formasyon-arz-talep-confluence-kapisi)
- "harmonik yapının tek başına garanti olmadığını; destek/direnç ve hacim bağlamının da değerlendirilmesi gerektiğini söylüyor." (acsel-direnc-kirilimi-volume-profile-val)
- "Her Gartley formasyonu beklenen D sonrası dönüşü üretmez." (gartley-d-tepki-penceresi-10-gun, notun ana fikir cümlesi)
- "fiyat ve hacim resmin üçte ikisidir; fiilen işlem görebilen hisse sayısı resmi tamamlar." (fiyat-hacim-fiili-dolasim-ucgeni)
- "Haftalıkta … C noktasının uzun vadeli talep toplama alanında" aranır (haftalik-bullish-gartley-talep-alani-tarama, notun yorumu).
- Yorum: tek formasyon yetmiyor; bölge + hacim/dolaşım bağlamı arıyor. "Bağımsız" kelimesi Tansu'nun tezinde geçiyor, ama hangi faktörlerin bağımsız sayıldığı yok. Seçici olmak (aday yoksa paylaşmama) bir ilke.

**Girişi teyit etme**
- "Breakout'u VAH, direnç veya trend çizgisi üstüne kararlı kapanış; teyidi volume veya delta; temiz girişi retest olarak tanımladı." (gunluk-trade-breakout-gap-retest-volume-delta-atr-obv)
- "Fibonacci 0,618'in bir duvar değil bölge olduğunu ve her zaman çalışmayacağını belirtti." / `Matematiksel oran (Fibo) + Piyasa Yapısı (Order Block) = Sniper Giriş` (fibo-0618-bolge-h4-order-block-multitimeframe)
- Görsel: `D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ` (KAPLM, harmonik-xb-trend-kirilimi-stratejisi). SAYAS lejantı: `Giriş (D)`.
- "Kaynak stratejisi 125,42 seviyesine kadar long fırsatı bildirmiş; ancak olası pullback nedeniyle hareketin izlenmesi gerektiğini belirtiyor." (alark-125-42, not özeti)
- Yorum: giriş "seviye + tepki/teyit"; çizgiye dokunmak yetmiyor. Teyidin sayısal tanımı hiçbir yerde yok.

**Risk ve pozisyon**
- "sürdürülebilir başarının kazançtan önce kabul edilebilir kaybı yönetmekle başladığını belirtti." (atr-risk-butcesi-position-sizing-stop-loss)
- "500 TL / 2 TL = 250 lot"; ilk stop "2 ATR" altı; acil stop intraday temasla, gün sonu stop kapanışla, iz süren stop yükselen fiyatla (aynı not).
- "kitapların yazmadığı" tecrübe tabanlı üç aşamalı portföy sistemi: 10–20 aday, 3–10 hisse, çekirdek %50+ (dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading).
- Yorum: önce kayıp bütçesi, sonra lot; stoplar katmanlı (acil + kapanış + iz süren). Portföyde bilinçli yoğunlaşma (çekirdek %50+) var.

**Stop ve hedef mantığı**
- SAYAS lejantı (görsel): `Bk Stop (X)`, `TP1 (1:1 R/R)`, `TP2 (.618 CD)`; başlıkta `Fibonacci + Trade Management`.
- "X ve B noktalarından geçen çizgi ileri uzatılır" ve D'ye kadar taktik pozisyon (harmonik-xb-trend-kirilimi-stratejisi, not özeti).
- Yorum: stop yapı noktasında (X), hedef R/R ve Fib oranından. Hedef ladder'ı ("D'ye kadar", "125,42'ye kadar") hedefi önceden tanımlı seviyeye bağlıyor.

**Backtest, doğrulama, yöntem**
- "Backtest gerçek maliyet ve likiditeyi içermeli." / "Birkaç satırlık yüzeysel kod orta-uzun vadede risk yaratabilir." (algoritma-tasarimi-temelleri-trading-sistemleri)
- "Tweezer Bottom mum yapısını kodlayın, tarayın, getirisini ölçün" (tweet-tweezer, parça 02'den KURALLAR/B-§11 aktarımı; bu parçada okunmadı).
- "Basit indikatör ve çizgi yorumları kurumsal rekabette tek başına yetersiz kalıyor." / "Bireysel yatırımcı kod öğrenmeli." (bist-hft-colocation-quant-rekabet-kod-ogrenin)
- Tercih: "Python itertools ile parametre kombinasyonlarını tarayıp en düşük hatalı modeli seçmek"; ACF/PACF yorumu için "deneyim ve öznel yorum gerektirdiğini vurguladı." (arima-hiperparametre-acf-pacf-grid-search)
- Yorum: göz yorumundan koda, öznelden sistematik taramaya geçişi savunuyor. Kendi paylaştığı kanıtlar seçilmiş örnekler (KAPLM tek örnek, başarısız D'yi de gösteriyor). Notlardaki OOS/Holm/çoklu test dili Cevo'nun, Tansu'nun değil.

**Araçları birleştirme (tarama → filtre → tetik → yönetim)**
- "fiili dolaşım verisinin yalnız anlatılmaması, stratejik biçimde taranması gerektiğini savunan" (fiili-dolasim-yuzde-30-alti-stratejik-taramalar)
- "Gartley ve Butterfly kodlarını tek ortak tarama sisteminde konsolide etmeyi tamamladığını; ancak uygulama ve bakım maliyetinin çok yüksek olduğunu bildiriyor. Önerisi, iki formasyonu ayrı taramak" (gartley-butterfly-ayri-tarayicilar)
- "Sektör rotasyonunda Convex Hull ve VZA/DEA birlikte" (convex-hull-dea-sektor-rotasyonu-projesi); "Modelleri yaratıcı biçimde yeniden kullanarak yakında denemelere başlanacağını belirtti." (finans-muhendisligi-destek-direnc-seviye-motoru)
- Yorum: akış: evren/tarama (fiili dolaşım, formasyon, sektör) → bölge/yapı filtresi → tetik (kırılım, D tepkisi) → yönetim (stop, TP, trailing). Her formasyona ayrı tarayıcı.

**Reddettiği veya eleştirdiği**
- Tepe/dip tahmini ("Görevin tepe veya dip tahmin etmek değil").
- Ortalamanın uç değer kırılganlığı (aritmetik-ortalama notu); medyan tercihi başka notta (`tweet-medyan-temelli…`, bu parçada değil).
- Gereksiz karmaşıklık ("Levent gereksiz karmaşıklığa karşı en sade trend kuralını verdi.").
- Tek göstergeye/çizgiye güven ("harmonik yapının tek başına garanti olmadığını").
- Tek ortak harmonik motor (bakım maliyeti).
- Yorum: "basit ama bağlamlı" çizgi: sade trend filtresi + çoklu bağlam; karmaşık tek motor ve tek gösterge reddi.

**Tekrar eden ilkeler (Yorum)**
1. Trendde kal, dönüşü tahmin etme, bozulmada çık.
2. Seviye bir çizgi değil bölge; tek faktör yetmez, teyit gerekir.
3. Önce kayıp bütçesi ve stop, sonra büyüklük.
4. Her şeyi koda dök, tara, ölç; göz yorumuna güvenme.
5. Seçici ol: uygun aday yoksa paylaşma/işlem yapma.
6. Veri tabanını (fiili dolaşım, hacim) fiyatın yanına koy.

Güvenilirlik: bunların hepsi ikinci el aktarım; Tansu'nun kendi metni için X bağlantılı yalnız bollinger, asuzu, beklenen-fk var.
