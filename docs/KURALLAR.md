# Kural kataloğu (05.10.2026)

Kaynak: beyindeki Tansu havuzu (16.10 sayımı: 1.926 not, 1.848 görsel ve 1 PDF; 1.668 not X arşivinden eklendi, eleme kaydı
havuzda `x-arsiv/eleme.jsonl`). Ayrıntılar `docs/kurallar/A–E` dosyalarındadır;
bu belge onların dizini ve seçimidir. Her kuralın kaynağı, parametresi ve "YORUM" etiketi orada. X arşivi notları var olan
bölümlerde "Ek kaynaklar (X arşivi, 16.10)" bloğunda, yeni kurallar yeni bölümlerde, tek öğeli olanlar dosyanın
"X arşivi kısa kayıtları (16.10)" bölümündedir.

Okuma kuralları (birinci el, ikinci el, NotebookLM ve YORUM tanımları GLOSSARY'dedir):
- Kuralın dayanağı birinci el kaynaktır: notun Ham metni ve notun görselleri (NotebookLM görselleri dahil). Notun Ham dışı
  bölümü görselle çelişirse görsel geçerlidir (§1 madde 3).
- Notun öbür bölümleri (Sentez, Cevo çıkarımı, Kaynak kartı, Teknik Ek) ikinci eldir ve kural olarak tek başına kullanılmaz;
  "NotebookLM görseli" etiketi yalnız bilgi verir.
- Bir YORUM'un sınamada denenen her değeri yeni deneme sayılır; istisna: önceden yazılmış sağlamlık ızgarasının
  hücreleri ve masraf senaryoları deneme sayısına girmez (TASARIM 5.10, 5.11; İ: 09-056). Sadakat kontrolünde denenen
  aday formüller deneme sayısına girmez, p üretmez; seçilen formül kural kaydına girer (TASARIM 5.11, İ: 10-033, 04-090).

## 1. Ana bulgular

1. Tansu bazı kurallar için tam giriş + stop + hedef üçlüsü verir: gorsel-paket-105, -106 ve -107 Ham metinleri ve AKFIS
   görseli (ENTRY, STOP, TP1–3). gorsel-paket-58 Ham giriş (300.75), hedef (389.30) ve risk/ödül (1:2.27) verir; stop vermez.
   Sistematik çok sembollü sınama yoktur; yalnız tek sembollü tablolar vardır (SMRTG 12 patern, ISKPL 5 patern). Kanıtı
   seçilmiş örneklerdir; bazı başarısız örnekleri de paylaşır (BALAT, AKSGY, bağı kopan çift).
2. Talep/arz bölgesi üretim kuralı, temas toleransı ve SETUP puan formülü hiçbir yerde yok. Tepe/dip (pivot) ayarı
   yalnız gorsel-paket-60 görselinde görünür ("Swing=15 sol-only | MinGap=15"); konsolidasyon bölgesinin sınırı
   gorsel-paket-18 Ham'da tanımlıdır (en yüksek mumun gövde ucu, en düşük mumun gölge ucu).
3. Gartley takip tablosunda (gorsel-paket-123) D girişi `X + (A-X) * 0.786 (Boğa için)` yazılıdır; tablonun kendi TP
   formülleri D'nin A'nın altında olduğunu varsayar. Hata Tansu'nun tablosunun içindedir (YORUM: bizim hesabımız, C §7).
   Notun Ham dışı bölümü görselle çelişirse görsel geçerlidir.
4. 05.10 ön denemesindeki "4 ATR hedef" ve "EMA50 altı çıkış" Tansu kaynaklarında yok; kaldırılır.

## 2. Dizin

Hazırlık sütunu: H, K ve X anlamı için GLOSSARY "Hazırlık" maddesine bakın.

Her satırın kaynak okuması (parametre, sayı, Tansu'nun kanıtı, eksik YORUM'lar) "Bölüm" sütunundaki A–E bölümündedir; bu
dizin kaynak değerini yinelemez.

### Giriş aileleri
| Kural | Bölüm | Hazırlık |
|---|---|---|
| Çift rotasyonu | D, "Çift sistemi çekirdeği" | **K** |
| AB=CD + hedef merdiveni | C §3–5 | **K** |
| EMA sıkışması (KRDMD) | B §1 | **H** |
| Yükselen kanal alt bant teması (AEFES) | A §2 | **K** |
| Kırılım + range retest + FVG (AKFIS A+) | A §1 | **K** |
| Gartley | C §7 | **K** |
| BOS + Fib altın bölge + FVG/OB | A §10 | **K** |
| Elliott 2. dalga (BRYAT) | C §16 | **K** |
| Düşen direnç kırılımı + talep (LIDER/BALAT) | A §3; C §13 | **K** |
| Fincan-kulp (GUBRF) | B §21 | **K** |
| Gizli pozitif uyumsuzluk | B §9 | **K** |
| A/D–EMA(3) (ISCTR) | B §12 | **K** |
| Bullish engulfing | B §10 | H (tetik) |
| Kelebek, Trident, Three Drives, X–B kırılımı | C §8, §12, §15, §9 | K |
| SETUP puanı | A §5 | **X** |
| D.Touch / D.Teyit | A §6 | **X** |
| Siyah/Beyaz Kuğu | C §13 | **X** |
| BOM, AHENK, gizli filtre | A §16, §14 | **X** |
| Mavi çizgi, Pre Signal | B §8, §2 | **X** |
| Bottle pattern (iki mum) | B §33 | K |
| SMA kesişimi (TUPRS, EURUSD) | B §35 | K |
| Üç kırmızı mum SELL sinyali | B §36 | K |
| Fibonacci düzeyi + bant sistemi | C §23 | K |
| EMA200 yukarı kesen tarama, golden cross adayı (CMENT) | C §24 | K |
| Kapanış aralığı Fibonacci + EMA seviye haritası (DOAS) | C §25 | X |
| Siyah Kuğu (bullish) oran aralıkları | C §26 | K |
| Elliott 0-1-a-b-c: c dibi ve 1. tepe direnci (LIDFA, AKBNK) | C §27 | K |
| Elliott 0-5 sonrası ABC: Fibonacci merdiveni, C teyidi, P-BOM (IDGYO, CRDFA) | C §28 | K |
| Elliott taramaları (C taraması, 3. itki dalgası taraması) | C §29 | X |
| Aralık kırılımı + bullish mum teyidi (DITAS) | A §18 | K |
| Fibonacci %78,6 tepki taraması: birleşim koşulları ve onay (EMA20, düşen trend kırılımı) | C §31 | K |
| Tüm Fibonacci düzeylerinde destek dönüşü ve direnç kırılımı taraması | C §32 | K |
| Fibonacci %161,8 uzantısı: haftalık dip taraması (fiyat ve RSI) | C §33 | X |
| RSI üzerinde Fibonacci (0,786 ve 0,618 dönüşü, 0,382 reddi) | C §34 | K |
| ADX ve ±DI kesişimi, ADX tepesi | B §37 | K |
| Bollinger 3 SS banda temas + zıt renkli mum | B §38 | K |
| Bollinger orta bandı üstünde kapanış + RSI 50 kesişimi (aynı bar) | B §39 | K |
| Bollinger sıkışması + RSI 50 kesişimi | B §40 | K |
| BELTHOLD + RSI düşen trend kırılımı | B §41 | K |
| RSI(14) 30/70 son gün taraması | B §42 | H |
| Mum sinyalinde trend filtresi | B §43 | X |
| Bollinger Keltner dışında + alt banttan sekme (fikir) | B §44 | X |
| Bollinger Keltner sıkışması ve kırılım | B §45 | K |
| BULL/BEAR etiketi: sinyal toplamı (FROTO) | B §46 | K |
| Bullish Hikkake: iç bar, sahte kırılım, iç bar altı stop | B §47 | K |
| Bullish Tasuki (üç mum kodu, GARAN) | B §48 | H |
| Dark Cloud Cover: düşüş uyarısı, stop ilk mum tepesi | B §49 | K |
| Doji + RSI(14) 30/70 taraması | B §50 | H |
| Doji + boğa teyit mumu: stop ve hedef | B §51 | K |
| RSI pozitif uyumsuzluk taraması + teyit katmanları | B §52 | K |
| WaveTrend (10, 21) aşırı satım taraması | B §53 | K |
| CMF para girişi filtresi (3 gün pozitif, önceki 3 gün negatif) | B §54 | K |
| EMA dizilimi son gün taraması | B §55 | H |
| Kapanış EMA'ların üstünde + RSI14 > 50 (+ CMF dönüşü) | B §56 | K |
| EMA5 x EMA13/14 kesişimi + RSI 50 | B §57 | K |
| EMA dizilimi + RSI trend kırılımı + MACD sıfır üstü | B §58 | K |
| EMA5 ve EMA10 x EMA20 kesişimi + MACD + OBV + RSI 50 | B §59 | K |
| EMA5 x EMA(EMA5) kesişimi + CCI(20) | B §60 | K |
| Momentum teyit listesi (AGROT, BYDNR) | B §61 | X |
| EMA sıkışması sonrası hacimli kapanış | B §62 | K |
| EMA12 x EMA144/169 tüneli kesişimi | B §63 | K |
| X arşivi kısa kayıtları | A §17, B §34 | X |
| X arşivi kısa kayıtları (Elliott) | C §30 | X |
| Haftalık aralık kırılımı ve günlük teknik teyit | A §19 | K |
| Kanal altı kapanışta AL, kanal üstü kapanışta SAT çıktısı | A §20 | K |
| SMC + Elliott trend takibi: indirimli bölgede aktif FVG, limit giriş ve iki hedef | A §21 | K |
| ATR bantlarıyla dip adayı | B §64 | K |
| EWMA Z-skor getiri bantları: ±2 uç hareket ve ortalamaya dönüş | B §65 | K |
| H formasyonu: üç mumlu boğa trend devamı | B §66 | K |
| Harami Cross: trend sonunda doji ve üçüncü gün onayı | B §67 | K |
| Ichimoku hesaplaması ve dört koşullu bulut taraması | B §68 | K |
| Keltner kanalında trend ve yatay piyasa ayrımı | B §69 | K |
| MA20/MA50 yükselen trend ve geri çekilme sınırı | B §70 | K |
| MA5 sapmasıyla kısa pozisyon ve ortalamaya dönüş deneyi | B §71 | K |
| MACD uyumsuzluğu: karşılaştırmalı tarama, tolerans ve örnekler | B §72 | K |
| MACD son bar kesişimi ve yerel yukarı dönüş taraması | B §73 | K |
| MACDAS karşılıklı kesişimleri ve optimizasyon aralıkları | B §74 | K |
| Çok ölçekli momentum modelinde eğitim/test ayrımı ve olasılık kararı | B §75 | K |
| Çoklu PSAR ve regresyon kanalıyla tarama | B §76 | K |
| SMA20/SMA40 teyidinden sonra ilk PSAR barında giriş | B §77 | K |
| Quintuplets: beş küçük gövdeli mum ve farklı sinyal günleri | B §78 | K |
| Regresyon kanalı orta/üst bant kırılımı ve pencere tercihi | B §79 | K |
| ROC9 sıfır çizgisi yukarı kesişimi ve ROC seri örnekleri | B §80 | K |
| ROC50, ADX/ADXR ve OBV ile giriş, teyit ve çıkış | B §81 | K |
| RSI14'ün beş dönem VAR ortalaması ile 50 kesişimi | B §82 | K |
| Temel kalite, teknik zamanlama ve takas: haftalık dip filtre önerisi | B §83 | K |
| Uyarlanır orta hat: uç değer, Bollinger zarfı ve rejim okuması | B §84 | X |
| Dönüş sinyallerini VEYA, teyidi VE ile birleştirme | B §85 | K |
| WMA vade seçimi ve 4/9/18 kesişimiyle long giriş/çıkış | B §86 | K |
| WMA5/14/34/55 ile RSI50 teyit taraması | B §87 | K |
| Shrinking (daralan) mum formasyonu: beş mum, gövde daralması ve ikinci mum sınırı | B §88 | K |
| Slingshot mum kırılımı: ikinci tepe üstü kapanış ve mum sırası belirsizliği | B §89 | K |
| TOBO: haftalık kapanış, hacim, hedef ve momentum takibi | C §35 | K |
| İkili dipte mum teyidi ve Adam & Eve | C §36 | K |
| X arşivi kısa kayıtları (piyasa ve portföy) | D, X arşivi kısa kayıtları (18.10) | X |
| Birinci fark sonrası durağanlık kontrolü: ADF ve KPSS | D, Birinci fark sonrası durağanlık kontrolü: ADF ve KPSS | K |
| Durağan Convex Hull: köşe sıklığı ve GARCH filtresi | D, Durağan Convex Hull: köşe sıklığı ve GARCH filtresi | K |
| Fon birikimi: ağırlık ve TL pozisyon artışını birlikte izleme (hisse dışı kaynak kaydı) | D, Fon birikimi: ağırlık ve TL pozisyon artışını birlikte izleme (hisse dışı kaynak kaydı) | K |
| HMM davranış rejimleri ve lojistik yön modeli | D, HMM davranış rejimleri ve lojistik yön modeli | K |
| Kayan alfa ve Sharpe: düzey, istikrar ve beta birlikte | D, Kayan alfa ve Sharpe: düzey, istikrar ve beta birlikte | K |
| Risk parity: eşit sermaye yerine risk katkısı | D, Risk parity: eşit sermaye yerine risk katkısı | K |
| Thompson Sampling: dağılımdan örnekle günlük hisse önerisi | D, Thompson Sampling: dağılımdan örnekle günlük hisse önerisi | K |

### Risk ve çıkış (E)
| Kural | Bölüm | Hazırlık |
|---|---|---|
| Risk bütçesi ve lot | E K1 | H |
| Acil stop | E K2 | H |
| Gün sonu stopu | E K3 | H |
| İz süren stop, kısmi kâr | E K4, K5 | K |
| Harmonik hedef merdivenleri | C §4, §11 (E K11) | K |
| Durum etiketleri | C §2 (E K15) | H (ad) |
| Tepki penceresi | C §10 (E K15) | K |
| ATR basamak merdiveni | E K25 | K |
| Momentum marjında kâr al | E K28 | K |
| Fon satış baskısı, fon risk radarı (hisse dışı; kapsam kararı Levent'te bekliyor) | E K26, K27 | K, X |
| X arşivi kısa kayıtları (kripto dahil) | E K29 | X |
| Veriyi periyot kapanışında çek (tamamlanmış çubuk) | E K30 | H |
| Optimizasyonda sağlam bölge ve aşırı uyum | E K31 | K |
| Başabaş çıkışı (R aktivasyonlu, Under 30 Over 30) | E K32 | K |
| Value-at-Risk (VaR) ve hedge | E K33 | X |
| Grid alım-satım: yüzde ızgarası ve ATR stop kodu | E K34 | K |

E K1–K3: kaynakları birinci eldir, bu yüzden H'dir. K1 ve K2 Ham'dadır (tweet-atr-risk-butcesi-position-sizing-stop-loss, Ham'da yazar yok; gorsel-paket-115). K3'ün SMA250 altı kapanış çıkışı gorsel-paket-115 NotebookLM görselindedir. ATR uzunluğu, dolum ve SMA250'nin giriş filtresi olarak seçimi YORUM'dur (E K1–K3).

### Piyasa durumu (D)
| Kural | Bölüm | Hazırlık |
|---|---|---|
| Piyasanın Nabzı 4/5 (NotebookLM) | D, "Piyasanın Nabzı" | K |
| BIST + VIX 5 adım (NotebookLM) | D, "Hangi VIX?"; "BIST VIX long: 5 adım kontrol listesi" | K |
| Sektör liderleri 30/60/90 gün + anomali temizleme | D, "Sektör rotasyonu" | H |
| Volatilite şoku freni | E K8 | X |
| Aylık mevsimsellik eleme tablosu | D, "Aylık mevsimsellik: istatistiksel eleme tablosu" | K |
| Portföy VIF kontrolü | D, "Portföy VIF kontrolü" | K |
| Haftanın günü mevsimselliği (giriş günü filtresi) | D, "Haftanın günü mevsimselliği" | K |
| Aracı kurum dağılımı (AKD): ilk 5 kurum toplama takibi | D, "Aracı kurum dağılımı (AKD)" | X |

## 3. Seçim

**Ölçütler (seçimden önce yazıldı):**
1. Giriş kuralının çekirdeği birinci elden belli.
2. Bedava günlük veriyle uygulanabilir.
3. Tansu sayısal bir sonuç göstermiş (sınanacak bir iddia var).
4. Seçilenler birbirinden farklı türde olsun (aynı fikri iki kez sınamamak için).

**İlk sürümde sınanacak aileler:**
| Sıra | Aile | Neden | En önemli YORUM |
|---|---|---|---|
| 1 | Çift rotasyonu | 4 ölçütün hepsi; sayısal çıktısı var (VAKBN–GARAN raporu, §4) | sapma formülü ve pencere |
| 2 | EMA sıkışması | parametreler birinci el; oran formülü sadakatle seçildi (YORUM, aşağıda) | giriş tetiği |

Sürüm kapsamının sahibi TASARIM §3'tür. AB=CD ilk sürümde yoktur (gerekçe TASARIM §3, Sorgu 3). İkinci dalgada
geometri sadakati yönsüz yapılır. (bilet 04, 14.10)

**Ailelerin işlem kuralları (ilk sürüm):**

1. **Çift rotasyonu** (kaynak okuması: D, "Çift sistemi çekirdeği"). Sinyal hesabı düzeltilmiş seriden yapılır; ham seri yalnız sadakat kontrolündedir (TASARIM 5.1).
   - Sapma: log(Y) − log(X), ortalama ve standart sapma son 60 günden, standart sapma ddof 1 (YORUM; Tansu'nun Z'si
     üç sadakat turunda üretilemedi, §4 ve `docs/sadakat.md`: YORUM kalıcıdır). Sabit terim (α) yok; ortalama çıkarıldığı için Z aynıdır. (ddof: TASARIM 5.6; bilet 04, 14.10)
   - Z ≤ −2 ve ΔZ > 0 → ertesi gün Y'ye geç. Z ≥ +2 ve ΔZ < 0 → ertesi gün X'e geç. Tek günlük ΔZ
     yeterlidir (YORUM; kaynak ΔZ'yi tanımlar, kaç günlük onay gerektiğini söylemez: D).
   - İlk sinyale kadar nakit; sonra hep bir hissede (YORUM; genel nakit politikası kaynakta açık değil,
     TASARIM 5.6). Ayrı stop yok (YORUM; kaynak stop politikasını açıklamaz, TASARIM 5.5).
   - Çiftler önceden yazılmış kuralla seçilir (TASARIM 5.6).
   - K1 ön şartı: çift seçilmiş ve |Z| ≥ 2 olan günler.
   - Sağlamlık ızgarası (TASARIM 5.10, YORUM): Z penceresi {60; 120}, eşik {1,5; 2; 2,5}, seçim p'si
     {0,01; 0,05; 0,10}. (İ: 04-089)
2. **EMA sıkışması kırılımı** (Tansu sıkışma için genel parametre vermez: %1,2 ve 3 gün örnek ayarıdır (B §1);
   gorsel-paket-65 Ham'daki "Bir günde %5 Ema sıkışması"nın anlamı açık değil. Giriş, stop ve hedef sözlerine
   aşağıdaki "Modül 1" maddesi bakar. Bu ailenin getiri iddiası bizim hipotezimizdir, İ: 10-002)
   - Oran: (en büyük EMA − en küçük EMA) / EMA200; EMA20/50/100/200, `ewm(adjust=False)`. Formül görselde yok (B §1); sadakat
     kontrolüyle KRDMD örneğinde eşleşti, KRDMD dışında doğrulanmadı (YORUM, §4; düşüş trendinde paydanın EMA200 mü
     en küçük EMA mı olduğu açıktır, TASARIM §8 madde 6; bilet 04, 14.10).
   - Sıkışma dönemi: oranın ≤ %1,2 olduğu art arda en az 3 gün; oranın eşiği aştığı ilk gün dönemi
     bitirir. Tansu'nun %1,2 ve 3 günü "örnekteki değer"dir.
   - Giriş (YORUM; varsayılan kural, varyant `bugun`): dönem bittikten sonraki 10 gün içinde kapanış, dönemdeki en
     yüksek gün yükseğinin üstüne çıkarsa ertesi gün. Dönem başına tek giriş. Varsayılan kuralda stop ve çıkış risk
     paketidir (TASARIM §5.5) ve hedef yoktur. Tansu'nun öbür giriş, stop, hedef ve çıkış sözleri aşağıdaki "Modül 1"
     maddesinde varyant olarak durur.
   - Not: Tansu'nun ICBCT "Pre Signal"i sıkışma sürerken çıkar (B §2); bizim tetik bitişten sonradır (YORUM).
   - **Modül 1** (Levent 16.10: modül, kendi giriş, çıkış, risk ve piyasa kuralı olan bir stratejidir; modül 1'in
     hiçbir parçası kodda eksik kalmaz). Tansu = notun Ham metninden alıntı; YORUM = bizim seçim. Sayılar ve tanımlar
     aksi yazılmadıkça YORUM'dur. Varsayılan kural yukarıdaki Giriş maddesidir. Öbür her kural bir varyanttır
     (aşağıdaki tablo).
     - **Kutu.** Tansu: "EMA sıkışmasının olduğu Talep Bölgesinin (Yeşil Kutu)"
       (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham). YORUM: kutu, sıkışma dönemidir. Üst sınır
       dönemdeki en yüksek gün yüksekliği, alt sınır dönemdeki en düşük gün düşüğüdür. Tansu konsolidasyon kutusunda üst
       sınır için gövde ucunu, alt sınır için fitil ucunu söyler (A §14, `gorsel-paket-18-konsolidasyon-body-wick`).
       Biz üst sınırda varsayılan olarak gün yüksekliğini alırız; çünkü varsayılan giriş kuralı böyledir (YORUM).
       `kutu_ust` alanı üst sınırı seçer: `yuksek` (varsayılan) ya da `govde`. Tansu: "En yüksek mumun gövdesinin
       bittiği yer ile, en düşük mumun gölgesinin bittiği yer." (`gorsel-paket-18-konsolidasyon-body-wick`, Ham).
       `govde`'de üst sınır, dönemde gün yüksekliği en büyük olan günün gövde ucudur (YORUM: "en yüksek mum" =
       yüksekliği en büyük gün; eşitlikte ilk gün). Veride açılış yok; gövde ucu = max(önceki kapanış, kapanış)
       (YORUM; bölgelerdeki vekil ölçüyle aynı). Önceki kapanış, serinin önceki günüdür; dönemden önceki gün olabilir.
       Yalnız serinin ilk gününde önceki kapanış yoktur, o gün gövde ucu kapanıştır (YORUM: veri o kapanışı taşır ve
       bölgeler aynı vekil ölçüyü kullanır). Üst sınır giriş tetiğini, `retest` seviyesini ve `kutu_ust` sütununu değiştirir; alt sınır
       değişmez.
     - **Sıkışma.** Tansu: "EMA'ların (örneğin EMA 20, 50, 100) birbirinin içine geçtiğini ve "düzleştiğini" gör."
       (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham). Oran şartı bu cümleyi karşılar; ayrı eğim
       süzgeci yoktur (YORUM: cümle sayı vermez; ölçülmedi).
     - **Giriş türü** (`giris`). Giriş penceresi, dönem bitişinden sonraki 10 gündür (YORUM; bugünkü kural). Bir gün
       aday olur ancak ve yalnız tetik, bütün süzgeçler, kapanış ≥ SMA250 ve ısınma o gün sağlanırsa. Pencerede ilk aday
       gün sinyaldir. Dönem başına tek sinyal vardır.
       - `kutu` (YORUM; bugünkü kural): kapanış kutu üstünün üstündedir.
       - `ema`. Tansu: "fiyat hacim ile ema'ların üzerinde kapansın, sonra otur izle"
         (`tweet-ema-sikismasi-hacimli-kapanis-al-1953221966678376915`, Ham). Kapanış, setteki en büyük EMA'nın
         üstündedir. Hacim kısmı hacim süzgecidir (aşağıda).
       - `mum` (güvenli giriş). Tansu: "ilk güçlü ve gövdesi uzun yeşil mumu" ve "Alım sinyali, bu mumun kapanışıdır"
         (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham). Veride açılış yok; bu yüzden ölçüler
         YORUM'dur. Yeşil: kapanış > önceki kapanış. Uzun: yüksek − düşük ≥ 1,0 × ATR14. Güçlü: (kapanış − düşük) /
         (yüksek − düşük) ≥ 2/3. Kutudan yukarı: kapanış > kutu üstü.
       - `retest`. Tansu: "bu mumun ardından gelen küçük geri çekilmedir (Retest)" (aynı not, Ham). YORUM: pencerede
         ilk `mum` günü k olsun; hacim şartı k'de aranır. k+1 … k+5 içinde düşüğü ≤ kutu üstü olan ilk gün j'dir. j'nin
         kapanışı kutu üstünün üstündeyse sinyal j'dir. Değilse bu dönemde sinyal yoktur. Öbür süzgeçler j'de aranır.
         k'de hacim şartı sağlanmazsa da bu dönemde sinyal yoktur; j giriş penceresinin dışına düşebilir (YORUM).
       - `agresif`. Tansu: "EMA'lar hala sıkışıkken, fiyat talep bölgesinin alt sınırına değdiğinde alım yapmak." ve
         "Stop olma ihtimali yüksektir" (aynı not, Ham). Pencere yoktur; sıkışma sürerken aranır. t günü için t−1'de
         biten koşu (oran ≤ eşik) en az 3 gün sürmüştür (sıkışma dönemiyle aynı süre; YORUM). Düşük_t ≤ koşunun t−1'e
         kadarki en düşük düşüğü ve kapanış_t ≥ o düşüktür (YORUM: değdi, altında kapanmadı; Tansu: kutunun altında
         kapanışta "analiz iptal olur"). Kutu = koşu + t günü. Koşu başına tek sinyal vardır. Hacim şartı uygulanmaz;
         bu bir kırılım değildir (YORUM).
       - `arz`. Tansu: "Fiyat iki kutu arasına sıkışmış." ve "Yatırımcı: Fiyatın üstteki kırmızı kutuyu hacimli bir şekilde
         kırıp üzerinde kapanış yapmasını beklemelidir."
         (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham). YORUM: üst kutu, dönem bitişinde sabitlenir.
         Üst kutu, dönem bitişinde aktif (bilinen gün ≤ dönem sonu, bölge o gün bitmemiş) arz bölgelerinden proximal'ı kutu
         üstünden büyük olanların en küçük proximal'lısıdır (Hedef maddesindeki bölge tanımı). Böyle bölge yoksa bu dönemde
         sinyal yoktur. Pencerede kapanış, üst kutunun distal'ının üstündeyse gün tetiktir. "hacimli" kısmı hacim
         süzgecidir. Pencere 10 gündür (YORUM; bugünkü kural).
       - `ucgen`. Tansu: "Kırılma tarihi olarak görülen bar, üst çizginin üzerine taşan ve üzerinde kapanan bar"
         (`tweet-ema-sikismasi-ucgen-kirilim-hacim-1954300245707497649`, Ham) ve "fiyatın direnci yukarı kırması genellikle
         güçlü bir yükseliş sinyali olarak yorumlanır" (`tweet-ema-sikisma-yukselen-ucgen-tarama-1952086678639669635`,
         Ham). Dönemde üçgen aranır (tanım: Üçgen hedefi maddesi). Üçgen yoksa bu dönemde sinyal yoktur. Üst çizgi, o
         üçgenin ilk ve son salınım tepesinden geçer (YORUM: Tansu çizginin hangi tepelerden geçtiğini yazmaz). Pencerede
         t günü, kapanış_t > çizginin t'deki değeriyse tetiktir. Salınım noktaları dönemin içindedir; dönem bitişinde
         hepsi bilinir. Hacim kısmı hacim süzgecidir.
     - **Süzgeçler** (hepsi aday şartıdır). Eksik değer (YORUM): hacim ya da gösterge teyidi hesaplanamayan gün aday
       değildir; momentum squeeze hesaplanamayan gün süzgeçten geçer (kural yalnız "negatif ve düşen" günü eler).
       - Hacim (`hacim_kat`: 0, 2, 3). Tansu: "Breakout anında hacmin ortalamanın en az 2-3 katı olması lazım."
         (`tweet-qullamaggie-tarzi-hacimli-breakout-tarama-1979546907505545421`, Ham; genel kırılım kuralıdır, EMA'ya özel
         değildir). Aynı notta: "Gün içi kırılma yetmez, kapanış o seviyenin üstünde olmalı." Ayrıca Tansu: "Hacimli
         kırılım, gerçek kırılımdır kuralı" (`gorsel-paket-64-dusen-trend-talep-hacim-ema-breakout`, Ham; Ham'da yazar yok). `hacim_kat`
         > 0 ise hacim_t ≥ `hacim_kat` × önceki 20 günün hacim ortalaması (t hariç; 20 YORUM). Hacim TL tutarıdır,
         adet değildir (TASARIM §5.4).
       - Momentum squeeze (`momentum`). Tansu: "EMA sıkışması bull sinyal aldınız ama momentum squeeze neg ve negatif
         büyüyor" ve "bull yönde aksiyon alınmaz" (`tweet-ema-sikisma-momentum-conflict-2045457969215631398`, Ham).
         Tansu formül ya da ayar vermez (B §2). YORUM: gösterge, LazyBear'ın Squeeze Momentum Indicator göstergesidir (TradingView
         açık betiği, 2014; John Carter'ın TTM Squeeze göstergesi, Mastering the Trade, 2005): val = linreg(kapanış −
         ort(ort(en_yüksek(yüksek, 20), en_düşük(düşük, 20)), SMA(kapanış, 20)), 20). linreg, 20 günlük en küçük kareler
         doğrusunun son gündeki değeridir. `momentum` açıkken val_t < 0 ve val_t < val_{t−1} ise gün aday değildir
         ("negatif büyüyor" okuması YORUM). Formülün kaynağı TradingView betiğidir; veri değildir (TASARIM §4: TradingView
         verisi kullanılmaz).
       - Gösterge teyidi (`teyit` = `gosterge`). Tansu'nun ek teyit listesi zorunlu kural değildir ve kaçının şart
         olduğunu yazmaz (B §62). Hepsi birlikte tek varyanttır (YORUM). MACD(12, 26, 9) histogramı artıyor, yani
         h_t > h_{t−1}; Tansu: "histo eğimi artmaya başlamış"
         (`tweet-ema-sikisma-macd-histogram-egim-1957958199425818842`, Ham; periyotlar YORUM). PSAR(0,02; 0,02; 0,2;
         Wilder 1978) kapanışın altındadır; Tansu: "PSAR'lar fiyat altına insin"
         (`tweet-ema-sikisma-psar-trend-temas-hacim-1956041277096546504`, Ham; ayar yok; başlangıç YORUM: ilk gün
         yükselen trend, ilk SAR ilk düşük, ilk uç nokta ilk yüksek). Stokastik %K(14) > %D(3);
         Tansu: "stoc güzel kesmiş" (`tweet-ema-squeeze-downtrend-break-checklist-1953173142861414759`, Ham; ayar yok;
         periyotlar YORUM). Momentum artıyor, yani squeeze momentum val_t > val_{t−1}; trend güçleniyor, yani ADX_t >
         ADX_{t−1}; Tansu: "trend güşlenmiş momentum artmış"
         (`tweet-ema-squeeze-downtrend-break-checklist-1953173142861414759`, Ham; ölçüler YORUM). ADX(14, Wilder 1978;
         YORUM, standart tanım): +DM, −DM ve gerçek aralık Wilder ortalamasıyla 14 gün yumuşatılır; DX = 100 × |+DI − −DI|
         / (+DI + −DI); +DI + −DI = 0 ise (yönlü hareket yok; ATR = 0 olan düz ya da durdurulmuş hisse dahil) DX = 0 (YORUM: yönlü
         hareket yoksa trend yoktur; TA-Lib kuralı); ADX, DX'in 14 günlük Wilder ortalamasıdır. ADX hesaplanamayan gün aday
         değildir (Eksik değer).
         Listedeki hacim maddesi hacim süzgecindedir.
       - Trend teyidi (`teyit` = `trend`; vekil kararı 16.10: trend çizgileri de kodlanır). Tansu: "şahane düşeni kırmış"
         (`tweet-ema-squeeze-downtrend-break-checklist-1953173142861414759`, Ham) ve "Yükselen trende temas edip tepki
         alsın" (`tweet-ema-sikisma-psar-trend-temas-hacim-1956041277096546504`, Ham). Doğru tanımı YORUM'dur (Tansu pivot
         ayarı vermez; trend çizgisinin sahibi A §12). Salınım noktaları aşağıdaki üçgen maddesindeki tanımla bulunur
         (pencere 2); t günü için yalnız bilinenler kullanılır (nokta i, i+2 ≤ t). Düşen trend kırılımı: t'den önceki
         son iki salınım tepesinde ikincisi birincisinden alçaktır ve iki tepeden geçen doğrunun t'deki değeri
         kapanış_t'den küçüktür. Yükselen trende temas ve tepki: son iki salınım dibinde ikincisi yüksektir; doğru d(x)
         olsun; t−5 … t içinde bir u günü için düşük_u ≤ d(u) × 1,01 ve kapanış_u ≥ d(u) olur, ve kapanış_t >
         kapanış_u. İkisinden biri sağlanırsa teyit geçer.
       - R/R kapısı (`rr_min` = 2; Levent 16.10: en az 1:2 ödül/risk, altındakiler sinyal değildir). Hedef
         bulunduysa (hedef − kapanış_t) / (kapanış_t − stop_tahmini) ≥ `rr_min` olmalıdır. kapanış_t ≤ stop_tahmini ise
         gün aday değildir. stop_tahmini: `kutu` için kutu alt; `atr15` için kapanış_t − 1,5 × ATR_t; `atr2` için
         kapanış_t − 2 × ATR_t. Hedef bulunmazsa kapı uygulanmaz; ödül sınırsız sayılır (YORUM). Giriş tahmini
         kapanış_t'dir; gerçek giriş ertesi günün AOF'udur (TASARIM §5.3).
       - Düşüş (`dusus`: açık ya da kapalı; varsayılan kapalı). Tansu: "Fiyatın güçlü bir düşüşten sonra durulduğu ve
         yataya bağladığı Demand (Talep) bölgesini çiz." (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`,
         Ham). Tansu "güçlü düşüş" için sayı vermez. YORUM: açıkken dönem başından önceki 20 günün en yüksek yükseği,
         kutu alt + 3 × ATR14 (dönem başı günü) değerinden küçükse dönem sayılmaz. 20 ve 3 YORUM'dur. Yalnız dönem
         başından önceki günlere bakılır. Dönem başından önce 20 gün yoksa ya da ATR14 hesaplanamıyorsa süzgeç
         hesaplanamaz ve dönem sayılmaz (YORUM). `agresif` girişte dönem başı, t−1'de biten koşunun ilk günüdür; kutu
         alt, o girişin kutusunun (koşu + t) altıdır (YORUM: agresif girişin kendi kutusu; koşu t'de bilinir).
       - Bilgi olarak okunan cümleler (kural değildir; YORUM). `tweet-qullamaggie-tarzi-hacimli-breakout-tarama-1979546907505545421`
         notundaki tarama maddeleri (RSI > 60, MACD pozitif, fiyat MA 20-50-200 üstünde) başka bir tarama stratejisidir;
         yalnız hacim ve "kapanış o seviyenin üstünde" cümleleri yukarıda kuraldır. `tweet-ema-sikisma-macd-histogram-egim-1957958199425818842`
         notundaki "0 altında" o grafiğin durumunu anlatır; kural "histogram artıyor" kalır. `gorsel-paket-15-rbr-demand-zone`
         ortak bir şemadır; Tansu'nun kendi sözü değildir.
     - **Stop** (`stop`; Levent 16.10: başlangıç stopu 1,5 ATR ve 2 ATR, ikisi de sınanır).
       - `atr2` (varsayılan): giriş − 2 × ATR_sinyal (E K2; TASARIM §5.5).
       - `atr15`: giriş − 1,5 × ATR_sinyal (E K25 başlangıç stopu; YORUM).
       - `kutu`. Tansu: "Stop noktası, EMA sıkışmasının olduğu Talep Bölgesinin (Yeşil Kutu) hemen altı olmalıdır."
         (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham). Başka örnekte: "bu strateji çöp olur
         (Stop Loss)" (`gorsel-paket-101-avod-demand-bearish-fvg-supply-ema`, Ham; Ham'da yazar yok). Yatay bantta: "stop-loss seviyelerini
         bu bandın hemen dışına koymak rasyonel bir risk yönetimidir."
         (`tweet-yatay-konsolidasyon-7-30-gun-yuzde10-1939569795696922684`, Ham). YORUM: "hemen altı" kutu altıdır; bir
         fiyat adımı farkı modellenmez. Kutu yoksa (K1 rastgele girişi) `atr2` uygulanır. Giriş günü AOF ≤ stop ise giriş
         iptal olur (Tansu: kutunun altında kapanışta "analiz iptal olur"; iptal kuralı YORUM) ve düşen sinyal sayılır
         (TASARIM §5.3).
         Kutu altı kapanış kurulumu iptal eder. Tansu: "Eğer fiyat bu kutunun altına sarkar ve kapanış yaparsa, analiz
         iptal olur" (aynı not, Ham). `stop` = `kutu` iken, sıkışma dönemi bittikten sonra ve aday günden önce herhangi
         bir günün kapanışı kutu altının altındaysa (kapanış < kutu alt) o dönemden sinyal çıkmaz. `retest` için dönem
         bitişinden j gününe kadar bakılır; k ile j arası dahildir. Kapsam YORUM'dur: kural yalnız kutu stopunda
         uygulanır; `atr2` ve `atr15` ve bugünkü kural değişmez. `agresif` girişte dönem bitişi yoktur; bu kural
         uygulanmaz (YORUM; o girişin kendi şartı yukarıdadır).
     - **Hedef** (`hedef` = `tansu`; Levent 16.10: "Tansu bazı kurallarına satış hedef veriyorsa biz de o kuralı
       kullanmalıyız."). Varsayılan `yok`.
       - Arz bölgesi hedefi. Tansu: "İlk hedef, grafiğin sağ üstünde gördüğün Kırmızı Bölge (Supply/Arz) alanıdır."
         (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham) ve "üsteki supply alanına kadar yolu açık."
         (`tweet-arz-talep-bolgesi-hedef-2085799233915912673`, Ham). t günü aktif (bilinen gün ≤ t, bölge bitmemiş) ve
         proximal > kapanış_t olan arz bölgelerinin en küçük proximal'ı hedeftir (YORUM: en yakın).
       - Bölge (YORUM). Tansu bölge üretim kuralını sayılarla vermez (§1 madde 2). Bizim okumamız: açılış yok;
         yeşil mum = kapanış > önceki kapanış; gövde = önceki kapanış ile kapanışın küçüğü ve büyüğü. Arz: Tansu: "Sert
         bir düşüş hareketi başlamadan hemen önceki son yükseliş mumudur." (`gorsel-paket-20-sponsor-candle`, Ham; Ham'da yazar yok).
         b yeşil, b+1 yeşil değil; b+1 … b+3 içinde kapanış ≤ gövde_alt_b − 1,0 × ATR_b olan ilk gün bilinen gündür
         (bölge o gün bilinir; ATR eşiği YORUM). distal = yüksek_b, proximal = gövde_alt_b (A §7). Bozulma (A §9'un
         aynası): bilinen günden sonra ilk kapanış > distal; o gün bölge biter. Talep (ayna; Tansu: "Sert bir yükseliş
         hareketi başlamadan hemen önceki son düşüş mumudur." aynı not, Ham): b kırmızı (kapanış < önceki kapanış), b+1
         kırmızı değil; b+1 … b+3 içinde kapanış ≥ gövde_üst_b + 1,0 × ATR_b; distal = düşük_b, proximal = gövde_üst_b;
         bozulma (A §9, Ham'ın ana seçeneği): ilk kapanış < distal (daha katı `low < zone_low` kodlanmaz). Çıktı
         sütunları (A §6): `bas`, `bilinen`, `proximal`, `distal`, `bitis`, `temas`, `teyit`. temas, bilinen günden
         sonra bölge aktifken fiyatın bölgeye girdiği gün sayısıdır (arz: yüksek ≥ proximal; talep: düşük ≤ proximal;
         bozulma günü sayılmaz).
         teyit, bilinen gündür (YORUM, A §6).
       - Üçgen hedefi. Tansu: "hedefi de üçgenin taban yüksekliğini yukarı projekte ederek düşünmek mantıklıdır."
         (`tweet-ema-sikismasi-ucgen-kirilim-hacim-1954300245707497649`, Ham). Tarama adımları: "En az iki tane birbirine
         yakın tepeler (yatay direnç seviyesi) ve üç veya daha fazla yükselen dip aranır."
         (`tweet-ema-sikisma-yukselen-ucgen-tarama-1952086678639669635`, Ham). Salınım noktaları sıkışma dönemi içinde
         bulunur (agresifte koşu, t−1'e kadar; YORUM): gün yüksekliği iki yanındaki ikişer günün en büyüğüne eşit ya da
         üstüyse salınım tepesidir; düşükte ayna; yanlar dönemin içindedir (pencere 2). Üçgen şartı: en az 2 tepe ve her
         sonraki tepe ≤ ilk tepe × 1,01; en az 3 dip ve her dip bir öncekinden yüksek. Tansu'nun üst çizgi tarifi: "üst
         çizgi ise yataya yakın ama hafif aşağı sarkıyor"
         (`tweet-ema-sikismasi-ucgen-kirilim-hacim-1954300245707497649`, Ham; simetrik üçgen). Bu yüzden yatay ya da
         düşen üst çizgi kabul edilir ("yakın" = %1; YORUM). Hedef = en yüksek tepe + (ilk tepe − ilk dip) ("taban
         yüksekliği" ölçüsü YORUM).
       - `tansu` hedefi: arz ve üçgen hedeflerinden kapanış_t'nin üstünde kalanların küçüğüdür (ilk engel; YORUM: Tansu
         "İlk hedef" der). İkisi de yoksa hedef yoktur.
     - **Çıkış paketi** (`cikis`: `yok`, `atr3`, `dip`, `rsi70`, `rsi50`; Levent 16.10: 4 yarı satış kuralı sınanır).
       Tansu bu stratejiye özel kısmi satış ya da iz süren stop yazmamıştır (B §62: çıkış yok); yalnız "Yeşilde al,
       EMA'lar açılınca sür, Kırmızıda sat." der (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham).
       "Sür" kısmı ortak paketle doldurulur (YORUM; E K4, K5, K25, K32). `cikis` = `yok` iken yalnız stop, hedef ve SMA250
       gün sonu stopu vardır (TASARIM §5.5).
       - ATR merdiveni (E K25). Tansu: "Stop her zaman YUKARI hareket eder, aşağı inmez"
         (`tweet-atr-iz-suren-stop-tablosu-2045421697814126693`, görsel metni). n = ⌊(yüksek − giriş) / ATR_sinyal⌋. n ≥ 2
         ise stop = max(stop, giriş + (n − 2) × ATR_sinyal). Yani n = 2'de stop giriştir, n = 3'te 1 ATR'dir. Stop yalnız
         yukarı gider. ATR_sinyal = 0 ise (fiyatı 14 gün kıpırdamayan hisse) n tanımsızdır ve merdiven basamağı yoktur;
         öbür kurallar sayıyla aynen uygulanır (YORUM; sıfıra bölme tanımsızdır). ATR sinyal günü değeridir (YORUM; E K25'te giriş günü ATR'sidir, o değer giriş AOF'undan önce
         bilinmez). Bu bölümdeki eşik karşılaştırmaları (n, `atr3`, `dip` etkinliği, başabaş) 9 ondalığa yuvarlanarak
         yapılır; kayan nokta hatası tam bir basamağı düşürmesin diye (YORUM).
       - Başabaş çıkışı (E K32). Tansu: "Eğer kârlı bölgeye geçtikten sonra fiyat geri dönerek tekrar tam olarak giriş
         fiyatınıza ulaşırsa, derhal pozisyondan çıkmanız gerekir."
         (`tweet-under30-over30-1-5r-basabas-cikis-1992547498343161903`, Ham). R tanımı: TASARIM §5.3 "İşlem günlüğü".
         Yüksek ≥ giriş + 1,5 × R ise stop = max(stop, giriş). Aktivasyon fiyat alanı olarak gün yüksekliği YORUM'dur (E K32).
       - İz süren stop başlangıcı (YORUM). Tansu: "pozisyonun risk/ödül oranı hedefine ulaştığında Trailing Stop (TS) ve kâr
         alma kuralları devreye girer" (`tweet-rsi30-giris-iki-asamali-cikis`, Ham; Ham'da yazar yok). Not sayı vermez.
         ATR merdiveni n ≥ 2'de, başabaş 1,5 R'de başlar. İz süren stopun statik ya da dinamik oluşu (E K4) Levent'e kalır;
         buna dokunulmaz.
       - Yarı satış: tek sefer, pozisyonun yarısı. Kalan yarı öbür kurallarla çıkar. `cikis` değeri hangi kuralın
         çalıştığını seçer.
         - `atr3` (E K25). Tansu: "3 ATR'ye ulaşınca %50 satış yapın"
           (`tweet-atr-iz-suren-stop-tablosu-2045421697814126693`, görsel metni). Yüksek ≥ giriş + 3 × ATR_sinyal olunca
           gün içinde yarı satılır.
         - `dip` (E K4, K5). Tansu: "İlk kar alma yeriniz, bu nokta geçildikten sonraki barlardan hangisi bir gün
           öncekinin en düşüğünün altında kapattı ise orasıdır. %50'sin satın."
           (`tweet-statik-dinamik-atr-iz-suren-stop-1989985215452758434`, Ham). Yüksek ≥ giriş + 1,5 × ATR_sinyal olunca
           kural etkin olur (statik biçim; Ham dinamik biçimi "daha zekice" bulur; statik seçim YORUM, E K4). Etkin
           olduktan sonraki günlerden ilk kapanış < önceki gün düşüğü ise ertesi günün AOF'unda yarı satılır. Kalan yarı
           stopla ve merdivenle çıkar.
         - `rsi70` (E K5). Tansu: "ilk %50 kar aldiğımız RSI70 reddi ve ikinci %50 kar aldığımız önceki mumun en
           düşüğünün altında kapanış" (`tweet-rsi30-giris-iki-asamali-cikis`, Ham; Ham'da yazar yok). RSI14_{t−1} ≥ 70 > RSI14_t ise ertesi
           günün AOF'unda yarı satılır (RSI, Wilder ortalamasıyla; Ham: "70 seviyesinin üzerindeyken, daha sonra 70
           seviyesinin altına düşerek kapanış yaptığında"; "daha sonra" = ertesi gün, YORUM). Sonra ilk kapanış <
           önceki gün düşüğü ise ertesi günün AOF'unda kalanın tamamı satılır (neden `cikis_kurali`).
           Etkinleşme önşartı. Tansu: "Pozisyon kâr bölgesine geçtikten ve SMA 50/RSI 50 dirençleri aşıldıktan sonra, ana
           kâr alma sinyali RSI 70 Reddi ile başlar." (`tweet-rsi30-giris-iki-asamali-cikis`, Ham; Ham'da yazar yok).
           RSI70 yarı satışı yalnız girişten sonra bir u günü varsa sayılır (giriş günü sayılmaz; merdiven, başabaş ve
           `dip` gibi ertesi günden başlar; YORUM): u ≤ t−1, kapanış_u > giriş fiyatı ve
           kapanış_u > SMA50_u (SMA50, kapanışın 50 günlük basit ortalamasıdır). RSI ≥ 50 şartı RSI ≥ 70 ile örtülüdür.
           Ölçüler YORUM'dur (Ham sayı vermez).
         - `rsi50` (E K5). Tansu yarı satış koşulları: "Fiyat 50 RSI seviyesini reddederse." "Fiyat 50 SMA ortalamasını
           reddederse." "1.5 ATR kârdayken, önceki günün düşüğünün altında kapanış gelirse." Tam çıkış: "Bu 3
           senaryodan herhangi ikisi gerçekleşirse işlemin tamamını kapatın."
           (`tweet-rsi30-donus-yari-ve-tam-cikis-kurallari-1991721699922870638`, Ham). Üç senaryo: RSI50 reddi
           (RSI14_{t−1} ≥ 50 > RSI14_t); SMA50 reddi (yüksek_t ≥ SMA50_t > kapanış_t); 1,5 ATR kârda dip (`dip`
           tetiği). İlk senaryo ertesi AOF'ta yarı satış verir. İkinci farklı senaryo (aynı gün iki senaryo dahil)
           ertesi AOF'ta tam çıkış verir (neden `cikis_kurali`). "Reddetme" tanımı YORUM'dur; Ham tanım vermez.
       - Gün sırası (YORUM; açık pozisyon, giriş günü hariç; dolum fiyatları TASARIM §5.3): karantina ya da işlem yok
         (bugünkü kural), stop, bekleyen tam çıkış, bekleyen yarı satış, hedef, `atr3` yarı satışı, kapanış kuralları
         (SMA250 bugünkü kural; yarı ve tam çıkış tetikleri ertesi AOF'a bırakılır), stop güncellemesi (ertesi gün için).
         Giriş günü yalnız stop kontrol edilir (TASARIM §5.3); merdiven, başabaş ve `dip` etkinliği ertesi günden
         başlar. SMA250 çıkışı bildirilen gün kapanış tetiklerine (`dip`, `rsi70`, `rsi50`) bakılmaz; o günün bekleyen
         yarı satış dolumu ve `atr3` yarı satışı sıradaki yerinde olur. `rsi70`'te kalanın çıkışı için kapanış, yarı
         satışın dolduğu günden itibaren aranır. "Önceki gün" son dolu gündür.
         Aynı güne iki dönemin sinyali düşerse ilk dönemin kutusu ve hedefi kullanılır. K1 rastgele girişinde kutu ve
         hedef yoktur (`atr2` yedeği, hedef çıkışı yok; YORUM).
     - **Piyasa durumu** (Levent 16.10): yalnız bilgidir, kartı durdurmaz (TASARIM §3).
     - **Varyantlar** (`aileler.VARYANTLAR`). Temel `tansu`: periyotlar (20, 50, 100, 200), giriş `mum`, hacim 2 kat,
       momentum açık, teyit `yok`, düşüş `dusus` kapalı, kutu üstü `yuksek`, stop `kutu`, hedef `tansu`, R/R 2, çıkış `atr3` (YORUM: Tansu'nun söylediği
       kuralların birleşimi). Her varyant temelden tek boyut değiştirir. `bugun` istisnadır: varsayılan `Parametre()`
       değerleridir, yani yukarıdaki Giriş maddesinin bugünkü kuralıdır; karşılaştırma tabanıdır. Her varyant ayrı kural
       kimliği ve ayrı denemedir (TASARIM §5.11). Tabloda 24 varyant vardır. Günlük kart `bugun` ile kalır (TASARIM §6).

       | Varyant | Değişen boyut ve değer | Kaynak |
       |---|---|---|
       | `bugun` | giriş `kutu`, hacim 0, momentum kapalı, teyit `yok`, stop `atr2`, hedef `yok`, çıkış `yok` | bugünkü kural (yukarıdaki Giriş maddesi) |
       | `tansu` | temel | yukarıdaki maddeler |
       | `ema_5_8_13` | periyotlar (5, 8, 13) | Tansu: "Ben 5-8-13 kullandım." (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham) |
       | `ema_20_50_100` | periyotlar (20, 50, 100) | Tansu: "EMA'ların (örneğin EMA 20, 50, 100) birbirinin içine geçtiğini" (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham) |
       | `ema_10_20_50` | periyotlar (10, 20, 50) | Tansu: "EMA 10   EMA 20   EMA 50" (`tweet-ema-sikisma-tarama-1996662869107134897`, G1 görsel metni; PAPIL örneği) |
       | `ema_50_100_200` | periyotlar (50, 100, 200) | Tansu örnekleri: B §25, B §62 |
       | `giris_kutu` | giriş `kutu` | bugünkü giriş kuralı |
       | `giris_ema` | giriş `ema` | Giriş türü, `ema` |
       | `giris_retest` | giriş `retest` | Giriş türü, `retest` |
       | `giris_agresif` | giriş `agresif` | Giriş türü, `agresif` |
       | `giris_arz` | giriş `arz` | Giriş türü, `arz` |
       | `giris_ucgen` | giriş `ucgen` | Giriş türü, `ucgen` |
       | `kutu_govde` | `kutu_ust` `govde` | Tansu: "En yüksek mumun gövdesinin bittiği yer" (`gorsel-paket-18-konsolidasyon-body-wick`, Ham); Kutu maddesi |
       | `hacim_yok` | hacim 0 | hacim süzgecinin karşılaştırması (YORUM) |
       | `hacim_3` | hacim 3 kat | Tansu: 2-3 kat (üst uç) |
       | `momentum_kapali` | momentum kapalı | momentum squeeze süzgecinin karşılaştırması (YORUM) |
       | `dusus_sonrasi` | `dusus` açık | Tansu: "Fiyatın güçlü bir düşüşten sonra durulduğu" (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham); Düşüş süzgeci |
       | `teyit_acik` | teyit `gosterge` | Gösterge teyidi |
       | `teyit_trend` | teyit `trend` | Trend teyidi |
       | `stop_atr15` | stop `atr15` | Levent 16.10; E K25 |
       | `stop_atr2` | stop `atr2` | Levent 16.10; E K2 |
       | `cikis_dip` | çıkış `dip` | E K4, K5 |
       | `cikis_rsi70` | çıkış `rsi70` | E K5 |
       | `cikis_rsi50` | çıkış `rsi50` | E K5 |
   - K1 ön şartı: (a) türünde sıkışma dönemi bitmiş ve 10 günlük pencere açık günler (Modül 1 varyantlarında
     `arz` ve `ucgen` aynı 10 günlük pencere havuzunu kullanır (YORUM); `retest` için pencere 5 gün uzar; `agresif` için t−1'de biten koşusu en az 3 gün olan günlerdir; YORUM: gerçek
     sinyal günleri havuzun içinde kalır); (b) türünde sıkışma penceresi şartı aranmaz, yalnız hisse düzeyi şartlar (kapanış ≥ SMA250, ısınma, evren, karantina) aranır (TASARIM 5.7; bilet 03). Ek kol: sıkışmasız aynı kırılım (kapanış önceki 20 günün en yüksek yükseğinin üstünde, sıkışma penceresinde değil; 20 YORUM, TASARIM 5.7).
   - Sağlamlık ızgarası (TASARIM 5.10, YORUM): eşik {%1,0; %1,2; %1,5}, en az gün {2; 3; 5}, giriş
     penceresi {5; 10; 20}. (İ: 06-072)

İkinci dalga ve kapsam dışı olanlar TASARIM §3'tedir. Diğer kurallar dizinde kalır; kaynak çıktıkça yükselir.

"Ertesi gün" sınamada nasıl modellendiği (Tansu'nun T+1 açılışı uygulanamaz): TASARIM 5.3.

**Risk paketi:** sahibi TASARIM §5.5–5.6'dır; kaynak notları E K1–K3'tedir. Çift rotasyonu bölmesi bu pakete tabi
değildir, çıkışı karşı uçta geçiştir (yukarıda aile 1).

## 4. Sadakat kontrolü (sınamadan önce)

YORUM'ları sonuca bakarak seçmek yasak. Ama Tansu'nun **kendi çıktılarındaki rakamları** yeniden üretmek
serbesttir; bu performans değil, kuralın doğru okunduğunun kanıtıdır.

| Aile | Tansu çıktısı | Hedef değerler (sahibi) | Bu neyi çözer |
|---|---|---|---|
| Çift rotasyonu | VAKBN–GARAN raporu | D, "Tansu'nun kanıtı" ve "Çift sistemi çekirdeği" | sapma formülü ve pencere |
| EMA sıkışması | KRDMD | B §1 | oran formülü |
| AB=CD (ikinci dalga) | KRPLS, MARKA #13, SMRTG tablosu | C §3, §5 | pivot ayarı, yön |
| Kanal (ikinci dalga) | AEFES 03.09.2026 | A §2 | kanal çizim yöntemi |

Sonuçlar. Ölçülen değerler, aday sayıları ve toleranslar `docs/sadakat.md`'dedir (Sorgu 3 ölçümü: `docs/sorgu/sonuc-3-4.md`); burada yalnız karar durur.
- **EMA sıkışması çözüldü** (KRDMD örneğinde; KRDMD dışında doğrulanmadı): oran formülü §3 aile 2'dedir. İş Yatırım ham serisinde (bilet 05) EMA200 sıkı toleransı geçmez; karar: sonuç **gevşek
  bantla üretildi**; veri başlangıcı olarak "son 3 yıl" seçildi (ölçümler ve aday sonuçları `docs/sadakat.md`). Neden: EMA200
  uzun belleklidir; Tansu'nun veri başlangıcı bilinmiyor. Oran formülü değişmez. Sınamada veri başlangıcı sabit tutulur ve
  rapora yazılır (İ: 06-014).
- **Çift Z'si üretilemedi:** Sorgu 3, bilet 06 ve 10.10.2026 ek turu (aday listesi koşudan önce commit edildi, bf79a28)
  Tansu'nun Z'sini üretemedi (ayrıntı `docs/sadakat.md`). Karar: **YORUM kalıcıdır** (log oran, 60 gün); yeni tur açılmaz.
  Beta, korelasyon, piyasada kalma ve Mart–Mayıs 2025 kontrolleri formül olmadığı için yapılmadı. Fiyat serisi politikası:
  TASARIM 5.1.

Veri: Kontrol İş Yatırım ham seriyle yapılır (TASARIM 5.1). Yahoo ölçümü: `docs/sorgu/sonuc-3-4.md` O9.

Kural:
- Tolerans, adaylar denenmeden önce yazılır. "Üretti" = Tansu'nun gösterdiği son hanenin yarısı içinde
  (Z için ±0,0005). Gevşek bant (±0,05) yalnız tek aday kalırsa kullanılır. (İ: 04-002, 14-058)
  Aynı dönemi ve gün sayısını veren, ölçülen her değeri (ortalama, EMA'lar) birbirinden en çok `docs/sadakat.md` başındaki
  toleransla (gösterilen son hanenin yarısı, ±0,005) ayrılan adaylar eşdeğerdir ve tek aday sayılır. EMA'da son 3 yıl ve son
  2 yıl böyledir; ölçülen değerler `docs/sadakat.md` EMA tablosundadır. (bilet 05, 14.10)
- Birden çok aday formül denenir; Tansu'nun rakamını en iyi üreten seçilir.
  En iyi: ölçülen değerlerin Tansu'nun rakamlarından mutlak farklarının toplamı en küçük olan aday; eşitlikte aday
  sırasındaki ilk aday (bilet 07a, 14.10). Çift Z'si için aday
  kümesine standart sapmanın ddof'u {0; 1} de girer. (İ: 19-028)
- Rapor tarihi bilinmiyorsa (Z_t, Z_{t−1}) çifti bütün işlem günlerinde aranır; eşleşen günler yazılır.
  (İ: 04-003)
- Hiçbiri üretemezse YORUM olarak kalır ve raporda yazılır.
- Sonuç `docs/sadakat.md`'ye yazılır; `python -m tansu sadakat` aynı rakamları yeniden üretir. (İ: 11-023)
- Bu adım getiri sonuçlarına bakmaz.

## 5. Bilinen riskler
- Tansu'nun örnek çiftleri ve hisseleri sonuca bakılarak seçilmiş olabilir. Bu yüzden çift rotasyonu
  yalnız onun çiftlerinde değil, önceden yazılmış bir kuralla seçilen bütün çiftlerde sınanır
  (aynı sektör: YORUM, TASARIM 5.6; oluşum penceresinde eşbütünleşme). Onun çiftleri ayrıca gösterilir. AGROT–GARAN
  rotasyon değildir (iki bacak + nakit) ve borsapy'ye göre farklı sektördedir (bizim veri: borsapy; Tansu iddiası değil).
- NotebookLM görselleri birinci eldir (GLOSSARY); Tansu'nun kendi kuralı olmayabilir.

## Kural içermeyen notlar (bilet 04, 14.10)

Havuzdaki her not A–E dosyalarında ya da bu belgede geçer. Aşağıdaki notlar işlem kuralı (giriş, çıkış, filtre, eşik) içermiyor. Yazarı belirsiz bir metindeki kural "kural içermez" sayılmaz; A–E'de "Ham; Ham'da yazar yok" etiketiyle yazılır (ör. DEA/VZA ve aylık mevsimsellik notları: D, "Sektör rotasyonu"). Bir değerleme notu filtre ya da eşik taşıyorsa girdisinde yazılır; kapsamı TASARIM §3 dışarıda bırakır. Okuma derinliği: kısa notlar baştan sona; uzun değerleme notlarında Ham, Sentez ve teknik başlıklar. Biçim: dosya adı · gerekçe. "Kapsam dışı: TASARIM §3": TASARIM 3 (değerleme, opsiyon).

gorsel-paket-04-tsla-implied-move · kapsam dışı: TASARIM §3 (opsiyon); ABD örneği, kural yok
gorsel-paket-108-beta-risk-pusulasi · değerleme: beta tanımı; görsel rejime göre beta eşiği verir (boğada Beta > 1, ayıda Beta < 1); kapsam dışı: TASARIM §3
gorsel-paket-130-piyasa-evreleri-birikim-dagitim-semasi · kavram şeması, sayı yok
gorsel-paket-133-medyan-kanal-kullanimi · gösterge fikri, parametre yok (medyan: B §28)
gorsel-paket-14-isletme-analizi-kriterleri · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-16-temel-momentum-ters-faz · proje fikri, metrik ve eşik yok
gorsel-paket-19-eurtry-forward-monte-carlo · kur forward çalışması, kapsam dışı
gorsel-paket-22-hisse-karar-destek-pipeline · süreç şeması, eşik yok
gorsel-paket-23-froto-ppe-fiyat · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-24-merton-modeli · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-25-degerleme-agirliklandirma · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-27-asuzu-fk-ex-ante-zaman-cizgisi · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-28-proje-bugunku-deger-ve-teknik-kapi · değerleme, kapsam dışı: TASARIM §3; teknik kapı parametresiz
gorsel-paket-29-uc-yontem-rs-wacc-dcf-girdileri · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-30-fed-beklenti-altin-fiyatlama · haber: makro tablo
gorsel-paket-72-hbk-fiyat-bilanco-katalizoru · haber: bilanço; teknik teyit parametresiz
gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-77-asuzu-bottom-up-adet-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-79-arclk-aradonem-manuel-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-80-froto-basit-fk-fdfavok-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-81-froto-basit-fk-ileri-hedef-outcome · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-82-eregli-dcf-10y-ic-deger · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-83-eregli-tek-tus-dcf-konsol · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-84-dcf-varsayim-riski-sensitivity-reverse-mos · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-86-fcff-fcfe-ddm-coklu-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-87-cost-of-equity-total-beta · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-88-basit-capm-coe-python · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-89-fcff-fcfe-ddm-yontem-secim-matrisi · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-90-ebit-vergi-forecast-bilesik-buyume · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-91-dcf-fcff-adim-adim-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-94-ham-fiyat-getiri-risk-portfoy · eğitim
gorsel-paket-95-capm-portfoy-agirlik-risk-mutabakat · değerleme, kapsam dışı: TASARIM §3
kaynak-cme-group-volatilite-opsiyon-veri-araclari · kapsam dışı: TASARIM §3 (opsiyon veri aracı tanıtımı)
kaynak-ekonometri-hangi-soru-hangi-yontem-haritasi · eğitim: yöntem haritası
kaynak-stefan-jansen-ml-algo-trading · eğitim: kitap önerisi
tansu-calisma-kurallari · süreç notu, işlem kuralı değil
tweet-10-yil-ceyreklik-fk-sektor-karsilastirma-1956736838187565389 · Değerleme, kapsam dışı: TASARIM §3. Ham son 10 yılın çeyreklik bilançolarından kısa, orta ve uzun dönem F/K hesaplayıp sektör ortalamasıyla karşılaştırma yöntemini verir.
tweet-120-bar-kanal-salinim-yapisi-1989048623116464625 · Grafik örneği: MANAS 120 barlık kanal ve swing etiketleri. Ham, aynı hareketlerin tekrarlandığına ilişkin gözlem verir.
tweet-200sma-250sma-rsi30-kilit-noktalar-1979927243942944965 · görüş ve vaat: 200SMA, 250SMA ve RSI 30 "kilit nokta" denir, koşul ve örnek yok (konu: E K3 SMA250 çıkışı, E K5 RSI 30 girişi)
tweet-9aydan-yilsonu-satis-net-kar-tahmini · değerleme, kapsam dışı: TASARIM §3
tweet-ab-cd-fibonacci-hedef-seviyeleri-2090921643178594458 · SMRTG için AB=CD ve Fibonacci hedef grafiği; Ham mağduriyet yorumu, görsel metni belirli tarihteki hedef ve swing etiketleri taşır. Konu: C §3–4.
tweet-ab-cd-hedef-gerceklesme-fibonacci-2090804106457702877 · SAYAS için gerçekleşen hedefe ilişkin tek grafik örneği. Ham: Hedefin dediği ve fiyatın geldiği yere bak. Görsel metni D hedef ve swing etiketlerini içerir. Konu: C §3–4.
tweet-abcd-127-talep-bolgesi-2057150214583038444 · Tarama grafiği: ABCD BUY, CD=1.27AB ve 13.10–14.06 talep bölgesi etiketleri; Ham yalnız gider mi sorusu. Konu: C §3 ve §13.
tweet-abcd-formasyon-python-tespiti-2053210859061535153 · örnek grafik, koşul yok (THYAO AB=CD çıktısı; Ham: "python ne güne duruyor"; konu: C §3)
tweet-abcd-harmonik-fib-ema-seti-2055612928091398421 · Tarama grafiği: ABCD SELL, Beyaz Kuğu, EMA5/8/13 ve CD=1.0AB etiketleri; Ham yalnız gider mi sorusu. Konu: C §3 ve §13.
tweet-abcd-kanal-alt-bant-girisi-2096217971274191340 · Altı hisse için ABCD tarama çıktısı: gerçek ve teorik D fiyatları ile AL / GİRİŞ işaretleri. Ham hisse adları ve grafiğe bakma çağrısıdır. Konu: C §3, kanal bağlamı §14.
tweet-abcd-kanal-alt-bant-girisi-2096218117739311325 · ABCD geçmiş örneği: gerçek D 5.03 ve teorik D 4.98 etiketli grafik; Ham sonuç beğenisidir. Konu: C §3.
tweet-abcd-kanal-alt-bant-girisi-2096280302985322829 · SASA ABCD grafik örneği: gerçek D 2.22 ve teorik D 2.15; Ham ilgi ifadesidir. Konu: C §3.
tweet-abcd-patern-d-hedefi-backtest-2092343114971095065 · MARKA patern #13 geçmiş grafik örneği: D hedefi 70.25 ve kırılım işaretleri. Ham yalnız MARKA adıdır. Aynı örneğin okuması: C §3 ve §5.
tweet-abcd-yengec-harmonik-fibonacci-talep-2061893882619523361 · Grafik örneği: ABCD BUY, Yengeç, CD=1.0AB, EMA5/8/13 ve Fibonacci etiketleri. Konu: C §3 ve §13.
tweet-acf-pacf-statsmodels-aylik-getiri-1878753192923803957 · Eğitim: statsmodels ile S&P500 beş yıllık aylık getirisinin ACF/PACF çizimi; gecikme 20 çizim ayarıdır.
tweet-adet-bazli-ciro-fk-fdfavok-hedef-fiyat-2040789837628751919 · Değerleme, kapsam dışı: TASARIM §3. Adet bazlı satış, kur ve marj tahmininden F/K 10 ve FD/FAVÖK 16 çarpanıyla ASUZU hedef fiyatı üretilir.
tweet-akd-alici-konsantrasyon-taramasi-1964443262544232634 · AKD tarama çıktısı ve paylaşım vaadi: ilk 5/2/10 kurum yoğunlaşma tablosu ile RODRG örneği. Konu: D AKD bölümü.
tweet-akd-matrix-iq-gunluk-veritabani-1964445184328159257 · araç tercihi, veri kaynağı (AKD Matrix IQ'dan alınıyor, günlük veri tabanı planı); kural öğesi yok
tweet-akd-veri-kaynagi-api-1941449822050848997 · araç tercihi, veri kaynağı (AKD için Matrix IQ ve Algolab); kural öğesi yok; tekrar: tweet-akd-matrix-iq-gunluk-veritabani-1964445184328159257
tweet-aktif-devir-hizi-dupont-1918458073099710657 · Temel analiz ve değerleme, kapsam dışı: TASARIM §3. FROTO aktif devir hızı, net kâr marjı ve finansal kaldıraçla DuPont çerçevesinde değerlendirilir.
tweet-aktif-karlilik-dupont-ayristirma-1918417139813187678 · Temel analiz ve değerleme, kapsam dışı: TASARIM §3. Aktif kârlılık formülü ve DuPont bileşenleri açıklanır; şirketlerin varlık verimliliği karşılaştırılır.
tweet-aktif-karlilik-sektor-karsilastirma-1918476060125196735 · Temel analiz ve değerleme, kapsam dışı: TASARIM §3. FROTO aktif devir hızı ve aktif kârlılığının sektör karşılaştırmasıdır.
tweet-alfa-beta-aylik-gunluk-karsilastirma-1878132805504254308 · Banka hisselerinin aylık ve günlük alfa/beta sonuç tablosu. Ham GARAN portföy tercihini beyan eder; belirli dönemin performans karşılaştırmasıdır.
tweet-alim-satim-listesi-index-esitleme-1852430160085020742 · araç tercihi, kod yardımcısı (alım ve satım fiyat listesini endeks uzunluğuna eşitler), kural öğesi yok
tweet-alpha-beta-risk-ranking-1823687517155016847 · Kitap tanıtımı ve üç hisse için alfa/beta yorum örneği. Görsel metni BIMAS, EKGYO ve GUBRF piyasa duyarlılığını karşılaştırır.
tweet-altin-call-duvari-supply-demand-fvg-2085798184811483582 · Kapsam dışı: TASARIM §3 (emtia/opsiyon). Altında 4613 dolar call duvarı, dağıtım bölgesi ve güçlü talep tepkisi için tarihli senaryo.
tweet-altman-z-skoru-bathory-iflas-esik-1890148860330406128 · Temel bilanço riski ve değerleme, kapsam dışı: TASARIM §3. Kitap görselinde Altman Z ve Bathory modelleri ile iflas risk eşikleri aktarılır; Ham kodlama niyetidir.
tweet-amt-hacim-profili-delta-2002453171923267893 · KRONT hacim profili ve kümülatif delta grafik çıktısı; VAH/POC/VAL etiketleri. Ham yorumu okuyucuya bırakır.
tweet-analitik-ag-sureci-hisse-secimi-1944868638307311952 · eğitim (Analitik Ağ Süreci yöntem anlatımı); eşik, parametre ve ölçülen sonuç yok
tweet-aosm-uc-yontem-ortalamasi-1851001656747704382 · Değerleme, kapsam dışı: TASARIM §3. İNA için AOSM hesabında üç farklı yolun ortalamasını alma tercihi.
tweet-araci-kurum-alici-pozisyon-taramasi-1970563597626405045 · Tarama sonucu: BANK OF AMERICA alıcı pozisyonları, oran ve TOP2/TOP5 sütunları. Ham günlük alınan hisseler listesini tanıtır.
tweet-araci-kurum-alici-pozisyon-taramasi-1970590008487878993 · Tarama sonucu: TERA alıcı pozisyonları. Görsel metninde beşinci satır okunamıyor; bu satırdan çıkarım yapılmadı.
tweet-araci-kurum-korelasyon-ag-analizi-1970601017650622775 · Araştırma ve proje denemesi: üç günlük kurum korelasyonu ve kurum-hisse ağı. Ham bu grafiklerin şimdilik güvenilir olmadığını açıkça bildirir.
tweet-araci-kurum-satis-orani-siralama-1967162325028548887 · Deneme çıktısı ve proje fikri: BANK OF AMERICA satış oranı sıralaması, takip sistemi ve ajan entegrasyonu niyeti.
tweet-araci-kurum-yogunlasma-olcumu-1990455214315643360 · Hisse adı açıklanmayan AKD yoğunlaşma tablosu ve pasta grafikleri. İlk iki/ilk beş kurum ve diğer alıcı-satıcı paylarının tek tarihli çıktısıdır.
tweet-arima-hiperparametre-acf-pacf-grid-search · eğitim: model seçimi
tweet-arz-bolgesinden-donus-2093470896073646190 · Altında arz bölgesinden gerçekleşmiş dönüşün tek grafik örneği; Ham sonuç gözlemidir. Konu: A §6.
tweet-arz-talep-bolgesinde-formasyon-bekleyisi · sohbet; tekrar: tweet-formasyon-arz-talep-confluence-kapisi ham kaydı
tweet-arz-talep-denge-fiyati-kodu-1906972824842965372 · eğitim (iktisat alıştırması: Qd=100-2P, Qs=50+3P Python kodu); arz-talep bölgesi (demand/supply) değil, kural öğesi yok
tweet-asit-test-orani-formulu-1949421615135240509 · Temel analiz ve değerleme, kapsam dışı: TASARIM §3. Asit test oranı: dönen varlıklardan stokları çıkarıp kısa vadeli yükümlülüklere bölme formülü.
tweet-asuzu-coklu-degerleme-tutarliligi · değerleme, kapsam dışı: TASARIM §3
tweet-atr-tabanli-stop-seviyesi-1987562052194644270 · tarama çıktısı, kural öğesi yok (konu: E K2): TAVHL için "STOP: 247.20, ATR: 8.90, AL" etiketi, giriş fiyatı ve koşul yok
tweet-avellaneda-stoikov-rezerv-fiyat-spread-1911734132360552515 · Kapsam dışı: TASARIM §3 (gün içi emir defteri ve piyasa yapıcılık). Avellaneda-Stoikov rezerv fiyatı, envanter ve optimal bid/ask spread açıklaması.
tweet-ayi-bayrak-formasyon-taramasi-1904259315042795787 · Kripto POLS-USD için ayı bayrağı tarama çıktısı; 23.03.2025 kırılım tarihi etiketidir. Ham kripto okuyucularına hitaptır.
tweet-aylik-getiri-alfa-beta-veri-hazirlik-1823474810975932753 · Eğitim ve veri hazırlığı: BIMAS, EKGYO, GUBRF ve XU100 aylık verisini indirme ve Adj Close seçme kodu.
tweet-aylik-mevsimsellik-ortalama-getiri-1736483254402797925 · TUPRS takvim aylarına göre ortalama getiri grafiği; Ham grafiğin gösterdiği istatistiği tanıtır. Konu: D aylık mevsimsellik.
tweet-aylik-ortalama-getiri-mevsimsellik-1723970919104721129 · PEGASUS ve XU100 aylık getiri/mevsimsellik grafikleri ile PGSUS-XU100 saçılım grafiği. Ham aylara göre tarihsel hareketi yorumlar; tamamlanmamış gönderi zinciri parçasıdır.
tweet-aylik-ortalama-maliyet-birikim-1783840694043623592 · kişisel yatırım alışkanlığı (aylık düzenli alım, ortalama maliyet, hedef 2028-2030); kural öğesi yok
tweet-ayni-ceyrek-yillik-karsilastirma-1956819684713509048 · Temel analiz ve değerleme, kapsam dışı: TASARIM §3. Mevsimselliği ayırmak için aynı çeyrekleri yıllar arasında karşılaştırma yöntemi.
tweet-az-yatirimcili-fon-risk-kontrolu-1979721927809012208 · eğitim, fon riski uyarısı (11 yatırımcılı fon örneği); eşik yok (fon kapsamı: E K26)
tweet-bayrak-flama-formasyon-taramasi-1900500470029795548 · XU100 günlük grafiğinde boğa/ayı bayrak ve ayı flama işaretleri; Ham tarama yazma planıdır.
tweet-bayrak-flama-formasyon-taramasi-1900536123773850053 · ASELS günlük bayrak/flama tarama grafiği ve kodu daha önce yazma temennisi.
tweet-bayrak-flama-kirilim-tarama-1990456862681018711 · AKGRT bayrak/flama tarama sonucu: 17.11.2025 kırılım etiketi; Ham hisse adını açıklar.
tweet-bayrak-flama-kirilim-tarama-1993022005516619970 · CRDFA bayrak/flama tarama sonucu: 19.11.2025 kırılım etiketi ve önceki paylaşıma gönderme.
tweet-bayrak-flama-kirilim-taramasi-1924518333967159587 · AVPGY bayrak/flama tarama sonucu: 16.05.2025 kırılım etiketi; Ham kodlama emeği ve sonuç beğenisidir.
tweet-bayrak-flama-kirilim-taramasi-1925627889174659386 · LIDFA bayrak/flama tarama sonucu: 21.05.2025 kırılım etiketi; Ham formasyonu beğenir.
tweet-bayrak-flama-kirilim-taramasi-2018379701509620135 · BURVA bayrak/flama ve çoklu gösterge grafik çıktısı: 27.01.2026 kırılımı, EMA5/13, destek, talep ve FVG etiketleri.
tweet-bayrak-flama-kirilim-taramasi-2031773880533053751 · AYCES bayrak/flama tarama sonucu: 05.03.2026 kırılım etiketi; alıntılanan Ham yüzde 3,5 gerçekleşme yorumudur.
tweet-bayrak-flama-kirilim-tespiti-1940851291376570571 · BIGCH bayrak/flama tarama sonucu: 01.07.2025 kırılım etiketi; Ham çalışan kodun yararına ilişkin görüştür.
tweet-bayrak-flama-kirilim-tespiti-1941917288505987367 · BVSAN bayrak/flama tarama sonucu: 04.07.2025 kırılım etiketi; Ham elinde tutanlara dikkat çağrısıdır.
tweet-bayrak-flama-kirilim-tespiti-1941917577342488859 · EGGUB bayrak/flama tarama sonucu: 01.07.2025 kırılım etiketi ve önceki harmonik kazanç beyanı.
tweet-bayrak-flama-kirilimi-1949523572512481441 · ENSRI bayrak/flama tarama sonucu: 22.07.2025 kırılım etiketi; Ham gerçekleşmiş harekete ilişkin yorumdur.
tweet-bayrak-flama-kirilimi-1984304925052989897 · Hisse adı açıklanmayan kırılım grafiği; Ham IMASM benzeri olasılık sorusudur, görsel metni tarih ve RSI paneli etiketidir.
tweet-bayrak-flama-tarayici-2096025629770571980 · ARDYZ yükseliş bayrağı tarama kartı: kırılım tarihi, son fiyat, RSI, hacim değişimi ve kırılımdan uzaklık tek örneğin çıktı alanlarıdır.
tweet-bayrak-kirilim-pivot-ema-atr-seviye-1957895443104301198 · KRVGD bayrak/flama ve haftalık pivot/EMA26±ATR seviye çıktısı. Ham çalışma çağrısıdır; fiyatlar örneğin konum raporudur.
tweet-bedelsiz-potansiyeli-odenmis-sermaye-yedek-2086040274434715957 · Temel analiz ve değerleme, kapsam dışı: TASARIM §3. Ödenmiş sermayenin düşük, geçmiş kâr ve yedeklerin yüksek kalmasıyla bedelsiz potansiyeli değerlendirilir.
tweet-beklenen-fk-ceyrek-kar-tahmini-1913886647306846652 · değerleme: cari F/K yerine ilk çeyrek kâr beklentisinden tahmini HBK ve beklenen F/K hesaplama görüşü; kapsam dışı: TASARIM §3
tweet-beklenen-fk-coklu-regresyon-modeli · değerleme, kapsam dışı: TASARIM §3
tweet-beklenti-al-gerceklesen-sat-2085043282694779123 · görüş: slogan, ölçülür giriş veya çıkış koşulu yok
tweet-beta-formul-rejime-gore-secim-2001638298473894378 · değerleme: beta tanımı (kovaryans / varyans); görsel rejime göre beta yönü verir (boğada Beta > 1, ayıda Beta < 1, yatayda Beta ≈ 1.0); rejim tanımı ve hesap penceresi yok; aynı içerik gorsel-paket-108-beta-risk-pusulasi; kapsam dışı: TASARIM §3
tweet-bilanco-analizi-uc-katmanli-kod-mimarisi-1956642533762597363 · bilanço analizi yazılım mimarisi: veri temizleme, analiz ve sunum olmak üzere üç katman önerisi; değerleme altyapısı, kapsam dışı: TASARIM §3
tweet-bilanco-kalemi-bolme-hbk-hesabi-1888364638825243071 · değerleme veri hazırlığı: Financials sınıfıyla AKBNK bilançosunu çağırma ve iki bilanço satırını bölerek HBK hesaplama kodu; kapsam dışı: TASARIM §3
tweet-bilanco-kalemleri-basit-rasyo-1954546640431235183 · temel analiz eğitimi: net kâr, sermaye, borç ve özsermayeden rasyo hesaplayıp dönemleri karşılaştırma; kapsam dışı: TASARIM §3
tweet-bilanco-sonrasi-fiyat-tepkisi-1941562469320884677 · bilanço ve fiyat ilişkisi ödevi: ADESE, IHLGM, RGYAS, SONME için faaliyet kârı ve bilanço sonrası 40–55 günlük fiyat karşılaştırması; temel analiz, kapsam dışı: TASARIM §3
tweet-bilanco-yillik-kar-fk-fd-favok-1695361936651653499 · değerleme: SAYAS bilançosundan yıllık kâr, HBK, F/K, firma değeri ve yıllık FAVÖK hesabı örneği; kapsam dışı: TASARIM §3
tweet-binomial-tree-option-pricing-1905916768196890659 · opsiyon fiyatlama eğitimi: üç adımlı binomial fiyat ağacı, içsel değer ve geriye doğru iskonto kodu; örnekte spot 100, kullanım 100, vade 1 yıl; kapsam dışı: TASARIM §3
tweet-birikim-sureci-kotu-haber-akilli-para · sohbet: Wyckoff anlatısı, kural yok
tweet-bist-hft-colocation-quant-rekabet-kod-ogrenin · görüş
tweet-black-scholes-call-put-kodu-1911177641643983112 · opsiyon değerleme: Black-Scholes call/put kodu ve teorik fiyatla piyasa fiyatını karşılaştırma; örnekte 1,63 TL altı ucuz olabilir, 2 TL pahalı olabilir; kapsam dışı: TASARIM §3
tweet-black-scholes-delta-hedge-put-sayisi-1942962939696156904 · opsiyon risk yönetimi: Black-Scholes ve delta hedge eğitimi; Ham 1000 hisse ve 0,5 delta için 500 put örneği verir; bu hesap doğrulanmış uygulama kuralı sayılmaz; kapsam dışı: TASARIM §3
tweet-black-scholes-merton-tahvil-fiyatlama-1875619396414251058 · tahvil değerleme: Black-Scholes-Merton ile varlık değerinden call değerini çıkarma kodu ve 81,76 örnek sonucu; kapsam dışı: TASARIM §3
tweet-black-scholes-monte-carlo-opsiyon-kodu-1979645829377057243 · opsiyon fiyatlama: Black-Scholes teorik değeri ile Monte Carlo benzetimini karşılaştıran kod; piyasa fiyatı teorik fiyattan çok pahalıysa almama görüşü; kapsam dışı: TASARIM §3
tweet-black-scholes-option-pricing-1897926528647749945 · opsiyon fiyatlama: Avrupa tipi call/put Black-Scholes hesabı, AAPL opsiyon zinciri ve 180 kullanım fiyatlı call örneği; kapsam dışı: TASARIM §3
tweet-black-scholes-theta-vega-rho-formulleri-1942718595714396552 · opsiyon duyarlılık eğitimi: theta, vega ve rho üzerinden zaman, volatilite ve faiz etkilerini tartışan model çalışması; kapsam dışı: TASARIM §3
tweet-black-scholes-yanlis-fiyatli-opsiyon-1852043715721994405 · opsiyon proje fikri: Black-Scholes ve Monte Carlo ile yanlış fiyatlı opsiyon bulup alıp satma planı; kapsam dışı: TASARIM §3
tweet-bollinger-macd-adx-adxr-panel-1761494383709290807 · grafik, koşul yok (iki görsel: Bollinger, MACD, ADX ve ADXR paneli, "20-day SMA" etiketi; Ham yalnız "#MIATK soran olmuştu"; görsel metni)
tweet-bollinger-orta-bant-rsi50-kesisim-1840463074622685613 · sohbet (kod paylaşımı: wetransfer sorunu, numpy sürümü) ve tarama çıktısı, kural öğesi yok (konu: B §39); PENGD görselinin kırpılmış kopyası, RSI satırı yok
tweet-borc-kaynak-orani-sektor-kiyasi-1918057202553929898 · temel analiz: borç/kaynak oranını sektör ortalamalarıyla karşılaştırma ve finansal sürdürülebilirliği değerlendirme; kapsam dışı: TASARIM §3
tweet-borc-ozkaynak-orani-sektor-2086514064688124094 · temel analiz: FROTO borç/özkaynak oranının yaklaşık %175 ile sektör altında kaldığı yönünde tarihli değerlendirme; kapsam dışı: TASARIM §3
tweet-borc-vadesi-ozkaynak-likidite-riski-1944869714729345492 · temel analiz: güçlü özkaynağa rağmen kısa vadeli borç, faiz ve borç yapısı kaynaklı likidite riski uyarısı; kapsam dışı: TASARIM §3
tweet-borc-varlik-orani-sektor-karsilastirma-1950539635001557460 · temel analiz: DOAS borç/varlık oranının seyri ve iki hisselik sektör kıyası; borçlanma artışı ve finansal dayanıklılık yorumu; kapsam dışı: TASARIM §3
tweet-borc-varlik-orani-sektor-karsilastirma-2086122842655973634 · temel analiz: FROTO kaldıraç oranındaki düşüşü sektörel borçlanma baskısıyla karşılaştıran eğitim örneği; kapsam dışı: TASARIM §3
tweet-brut-kar-marji-pandas-hesabi-1908260105658724698 · bilanço eğitimi: pandas ile çeyreklik brüt kârı satış gelirlerine bölme kodu; kapsam dışı: TASARIM §3
tweet-capm-borc-maliyeti-wacc-esigi-1911635217472709037 · değerleme: CAPM özsermaye maliyeti ve WACC; yeni yatırımın en az WACC kadar getiri sağlaması gerektiği belirtilir; kapsam dışı: TASARIM §3
tweet-capm-ozkaynak-maliyeti-python-2037822186157707619 · değerleme: CAPM özkaynak maliyetini risksiz faiz, beta ve risk primiyle hesaplayan Python örneği; kapsam dışı: TASARIM §3
tweet-capm-portfoy-getiri-std-sapma-2018392636910916018 · CAPM ve portföy matematiği eğitim alıştırması: beklenen getiri, standart sapma ve minimum varyans ağırlıkları; iki görsel farklı ağırlık senaryoları içerir; değerleme, kapsam dışı: TASARIM §3
tweet-capm-wacc-damodaran-carpan-ina-birlesik-fiyat-1778895335592472990 · değerleme: TAOSO için CAPM, WACC ve Damodaran yaklaşımı; risksiz faiz %27, CDS %5,1, ülke risk primi %5,7, risk primi %5 örnek varsayımları; kapsam dışı: TASARIM §3
tweet-cari-oran-likidite-acigi-bedelli-sermaye-artirimi · değerleme, kapsam dışı: TASARIM §3
tweet-carpan-40-ina-60-agirliklandirma-1708030356564160854 · değerleme: TTRAK için çarpan %40 ve İNA %60 ağırlıklandırması, yıl sonu 1584 TL fiyat ve satış adedinden kâr tahmini; kapsam dışı: TASARIM §3
tweet-carpan-ceo-hedefli-kar-modeli-1700754232658231421 · değerleme: SMRTG için çarpan ve CEO'nun ciro/FAVÖK hedeflerinden kâr tahmini; Ham ile tabloda farklı yazılan hedefler genel işlem eşiği değildir; kapsam dışı: TASARIM §3
tweet-carpan-degerleme-akademik-bulgular-1939273526134939965 · değerleme: ileri F/K, sektöre özel çarpan, benzer büyüme ve kârlılığa göre şirket seçimi üzerine literatür değerlendirmesi; kapsam dışı: TASARIM §3
tweet-carpan-ina-birlesik-degerleme-tablosu-1774367633820750263 · değerleme: ASUZU için yıl sonu adil fiyat beklentisi; çarpan, İNA ve kâr tahmin tablosu; kapsam dışı: TASARIM §3
tweet-carpan-ina-birlesik-degerleme-tablosu-1781013117201154255 · değerleme: MIGROS için muhafazakâr varsayımla hazırlanmış çarpan, İNA ve kâr tahmin tablosu; kapsam dışı: TASARIM §3
tweet-carpan-ina-kar-tahmin-birlesik-1769338023169143095 · değerleme: DOAS operasyonel net işletme sermayesi yorumu ve çarpan/İNA/kâr tahmini tablosu; kapsam dışı: TASARIM §3
tweet-carpan-ina-kar-tahmin-birlesik-deger-1848034791116931310 · değerleme: çarpan ortalamaları ile İNA ve kâr tahminini birleştirme planı; Ham ilk grup için %6, ikinci grup için %40 yazar; sayılar düzeltilmedi; kapsam dışı: TASARIM §3
tweet-carpan-ina-ortalama-degerleme-1850969302347989014 · değerleme: SAYAS için geçmiş adil fiyat çalışmasının gerçekleşmeye ilişkin hatırlanması; Ham dönüş fiyatını sanırım ifadesiyle anlatır; kapsam dışı: TASARIM §3
tweet-carpan-ina-ortalama-hedef-fiyat-1695389783147581542 · değerleme: SAYAS için çarpan ve İNA ile 144 TL hedef ve 205 milyon yıllık kâr beklentisi; kapsam dışı: TASARIM §3
tweet-carpan-ina-ortalama-hedef-fiyat-1708049006742417472 · değerleme: SAYAS çarpan ve İNA çalışmasının yeniden paylaşımı; fiyat beklentisi tablosu; kapsam dışı: TASARIM §3
tweet-carpan-kar-dcf-agirlikli-hedef-1913527179364765803 · değerleme: çarpan ve kâr modeli ortalamasına %60, DCF değerine %40 ağırlık vererek nihai hedef oluşturma; kapsam dışı: TASARIM §3
tweet-carpan-kar-tahmin-degerleme-1768555476961165694 · değerleme: PEGASUS için çarpanla 1470 TL, kâr modeliyle 917 TL adil fiyat ve %12 büyüme varsayımı; kapsam dışı: TASARIM §3
tweet-carpan-kar-tahmin-ortalama-degerleme-1698276357233352931 · değerleme: CWENE için 637 milyon USD satış tahmininden hareketle çarpan ve kâr modellerini ortalama; kapsam dışı: TASARIM §3
tweet-carpan-kar-tahmin-ortalama-degerleme-1698364484601929916 · değerleme: TÜPRAŞ çarpan ve kâr tahmini tablosu ile 200 TL hedef beklentisi; kapsam dışı: TASARIM §3
tweet-carpan-kar-tahmin-ortalama-degerleme-1705920509647482939 · değerleme: KIMMR için çarpan ve kâr modeli; yetersiz veri nedeniyle İNA yapılamadığı belirtilen örnek; kapsam dışı: TASARIM §3
tweet-carpan-kar-tahmin-ortalama-degerleme-1708882556945420567 · değerleme: CWENE 30 milyon USD KAP haberi ve 637 milyon USD satış tahminine dayalı önceki değerlemenin alıntısı; kapsam dışı: TASARIM §3
tweet-carpan-tarihsel-ortalama-karsilastirma-1979562013647905210 · değerleme: günlük çarpan yerine uzun, orta ve kısa vade ortalamalarıyla güncel konumu karşılaştırma; kapsam dışı: TASARIM §3
tweet-cci-posc-macd-gosterge-seti-1761507718693548409 · grafik, koşul yok (THYAO; Ham yalnız etiket; iki gönderide sekiz gösterge grafiği: EMA5 üzerinden EMA5, CCI ve 20 günlük EMA, Price Oscillator (POSC), MACD ve sinyal, Ichimoku, 13 ve 60 günlük WMA, Stokastik %K/%D, Momentum ve 8 günlük MA; görsel metni). Çizim ayarlarıdır, giriş veya eşik yok (ilgili: B §34 kısa kayıtlarındaki çoklu gösterge seti, YORUM)
tweet-coklu-model-degerleme-birlestirme-1774181659425796563 · değerleme: ASUZU için F/K, FD/FAVÖK, üç çarpan ve İNA modelini birleştirme; tek modele bağlı kalmama görüşü; kapsam dışı: TASARIM §3
tweet-coklu-osilator-negatif-uyumsuzluk-2049565175494181237 · grafik, koşul yok (ISDMR; Ham: "Enteresan değil mi"). Görselde (açıldı) fiyat tepesinden yatay çizgi ve üç osilatör panelinde alçalan tepe çizgisi (çoklu negatif uyumsuzluk çizimi); osilatör adları, eşik ve sinyal tanımı yok
tweet-convex-hull-dea-sektor-rotasyonu-projesi · proje fikri
tweet-covered-interest-parity-regression-1906621697274323162 · ekonometri eğitimi: güvenceli faiz paritesini faiz farkıyla ölçen regresyon denklemi; hisse işlem kararı değil, döviz ve faiz ilişkisi alıştırması
tweet-cufflinks-quantfig-macd-rsi-grafik-kodu-1860765789856379348 · eğitim ve araç tercihi: grafik kodu (cufflinks QuantFig ile XU100, 2022-2024; MACD 12/26/9 ve RSI(20) 70/30 çizim ayarı); giriş koşulu yok
tweet-dcf-5-adim-wacc-terminal-deger-2036496365371417087 · Değerleme: DCF adımları ve WACC için üç akademik yaklaşımın ortalaması; kapsam dışı: TASARIM §3.
tweet-delta-hedge-implied-volatility-open-interest-1978358660934795342 · Opsiyon delta hedge, implied volatility ve open interest anlatımı; yüksek/düşük volatilitede opsiyon satma/alma görüşü taşır; kapsam dışı: TASARIM §3.
tweet-dibe-uzaklik-taramasi-1696021655947018369 · 28.08.2023 otomotiv hisselerinin dip-zirve ve dönemsel uzaklık tablosu; Ham yalnız DOAS dip-zirve analizini tanıtır, tablo ölçüm çıktısıdır.
tweet-distance-to-default-python-kodu-1852070155779739853 · Temel risk modeli: distance-to-default >1 düşük, <1 yüksek iflas riski örneği; Tansu rakamların sallamasyon olduğunu belirtir; kapsam dışı: TASARIM §3 (değerleme).
tweet-divergence-macd-cross-1911093378961256668 · vaat ("Asla yanılmaz:))") ve tarama çıktısı, kural öğesi yok (konu: B §52); örnek kripto (MKR-USD), kripto kapsamı: karar Levent'te bekliyor
tweet-doji-mum-rsi-30-70-sinyal-1848385134174589367 · tarama çıktısı, kural öğesi yok (konu: B §50); üç sembol: BFREN Sat, CCOLA ve KAREL Al
tweet-doji-mum-rsi-30-70-tarama-1851724305836499212 · tarama çıktısı, kural öğesi yok (konu: B §50); tek sembol: SOKM Al
tweet-dort-buyume-orani-yuzde-10-oncelik-1945811547680297466 · Temel analiz: dört büyüme oranının her birinde en az %10 beklentisi; öncelik özkaynak, hisse başına kâr, satış/brüt kâr, nakit akışı; kapsam dışı: TASARIM §3.
tweet-dupont-aktif-karlilik-analizi-1780322516126306636 · BRISA temel değerlemesi: sektör DuPont kıyası, %40 çarpan ve %60 İNA ağırlığı, kâr tahmin modelleri; kapsam dışı: TASARIM §3.
tweet-dupont-oran-sektor-karsilastirma-1954935103194534196 · DuPont oran ve sektör karşılaştırma çıktısı; finansal marj, devir, borç ve ROE tablosu; kapsam dışı: TASARIM §3 (temel değerleme).
tweet-dupont-roe-ayristirma-borc-esikleri-1979208183236157837 · DuPont temel analizi: Ham borç oranında %70 üstünü riskli, %30–50 arasını dengeli, %30 altını muhafazakâr sayar; ROE bileşenleri ve yıllıklandırma anlatılır; kapsam dışı: TASARIM §3.
tweet-dupont-roe-sector-ranking-1886887500183974168 · Dayanıklı tüketim sektörünün özsermaye kârlılığına göre sıralı DuPont tablosu; kapsam dışı: TASARIM §3 (temel değerleme).
tweet-dupont-sektor-karsilastirma-1771970054793433148 · KCAER DuPont, yatırım, nakit dönüşü ve çarpan değerlemesinin sektörle kıyası; kapsam dışı: TASARIM §3.
tweet-dupont-sektor-karsilastirma-1777571511395557531 · Enerji sektörü DuPont finansal oran tablosu; kapsam dışı: TASARIM §3 (temel değerleme).
tweet-dupont-sektor-lideri-momentum-faz-1886875307187356067 · DuPont ve temel filtre ile momentum fazı projesi: sektöründe en yüksek ROE veya en yüksek net Sharpe kâr marjı ve en düşük F/K seçimi; temel seçim kapsam dışı: TASARIM §3.
tweet-duran-varlik-artisi-dusuk-fk-tarama-1950901940524617991 · Yıllık duran varlık artışı yüksek, F/K düşük şirket taraması ve sektör kıyası; ROE ekleme fikri taşır; kapsam dışı: TASARIM §3 (temel değerleme).
tweet-duran-varlik-artisi-fk-strateji-1954964170585030772 · Duran varlık yatırımı ile makul F/K birlikte değerlendirilir; %50 artış ve %34–35 pay örneği genel büyüme ile kapasite yatırımını ayırır; kapsam dışı: TASARIM §3.
tweet-duran-varlik-fiyat-xu100-karsilastirma-1955010441526022428 · TOASO yatırımı, finansman yapısı, kârlılık ve nakit akışı ile fiyat/endeks ayrışmasının temel analizi; kapsam dışı: TASARIM §3.
tweet-dusuk-carpan-ucuzluk-sektor-tarihsel-filtre-1925078204198355066 · Değerleme: düşük çarpanı tek başına ucuzluk saymama; sektör, tarihsel çarpan, büyüme ve risk bağlamı filtresi; kapsam dışı: TASARIM §3.
tweet-dusuk-fk-dusuk-pd-yuksek-ozkaynak-tarama-1944866780041838894 · Temel tarama: düşük F/K ve piyasa değeri, yüksek özkaynak; kârın sürdürülebilirliği ve sektör incelemesi şartı taşır; kapsam dışı: TASARIM §3.
tweet-earnings-forecast-before-multiples-1913888429349228909 · Değerlemede faaliyet raporlarından kâr beklentisi hesaplandıktan sonra F/K ve çarpan kullanımı; kapsam dışı: TASARIM §3.
tweet-efk-ns-orani-q2-marj-donum-noktasi-1957079412760813739 · YAYLA EFK/net satışlar marj iyileşmesi; ikinci çeyrek yıllar arası artış ve 12 aylık marj, nakit dönüşü, borç teyidi; kapsam dışı: TASARIM §3 (temel analiz).
tweet-elliott-abc-fvg-algoritma-1989365905504256144 · örnek grafik, koşul yok (görsel: 1-2-3-A-B-C etiketi, sarı FVG kutusu, Matriks ekranı; Ham: "İşte böyle çalışıyor algoritma"; konu: C §17)
tweet-ema-5-13-21-kesisim-sinyal-1849524500439744798 · grafik, koşul yazılı değil: ARCLK için EMA5/13/21 kesişimi al (siyah ok) ve sat (turuncu) işareti; kod WeTransfer bağlantısında, notta yok; eğitim amaçlı davet
tweet-ema-dizilim-rsi-cmf-tarama-1847735111942336850 · sohbet ("otomasyona geçeceğiz"); görsel mum formasyonu işaretleme kodu parçası, koşul yok
tweet-ema-hizalama-rsi-50-tarama-1851721104156774497 · tarama çıktısı, kural öğesi yok (konu: B §56)
tweet-ema200-ema50-cmf-rsi-tarama-1847558481227702504 · Dış dosya paylaşım duyurusu; EMA200, EMA50, CMF ve RSI araç adlarını sıralar. Bağlantı içeriği bu işte açılmadı.
tweet-emir-defteri-histogram-fit-modelleme-1911700859420889185 · Anlık emir defteri için histogram modelleme ve likidite dağılımı örneği; Ham μ, v₀ ve q sonuçlarını yorumlar. İşlem emri veya tarama filtresi yerine mikro yapı modellemesini tanıtır.
tweet-enflasyon-farki-pi-pi-yildiz-1907020125770772606 · makro gösterge tanımı (π − π* = yerli eksi yabancı enflasyon, örnek %13 ve %2 için ≈ 0,11); eşik ve kural yok, üst gönderi notta yok
tweet-envanter-azaltma-monte-carlo-pnl-1924523925683274094 · proje anlatısı: kavramsal Monte Carlo simülasyonu (5 envanter stratejisi, 100.000 senaryo, 3 piyasa koşulu); sayısal sonuç ve eşik yok, yalnız kavramsal ilke (yükselen trendde yavaş, düşen trendde hızlı sat)
tweet-esas-faaliyet-kari-fk-5-15-tarama-1698267718074438032 · Değerleme taraması; kapsam dışı: TASARIM §3. Ham artan esas faaliyet kârı, fiyat sıçramaması, yüksek özsermaye kârlılığı, F/K 5-15 ve «Net kar marjı (sharpe) 2’nin üzerinde» koşullarını verir. Son ifadenin metrik adı belirsizdir.
tweet-esas-faaliyet-marj-kalitesi-1774017615482032258 · SAYAS esas faaliyet ve kâr marjı kalitesi yorumu; değerleme, kapsam dışı: TASARIM §3. Ham marj takibi önerir ve 2023/4Ç bilançosunu bekler.
tweet-esik-kantil-fiyat-anomali-tespiti-1964205713430876532 · Fiyat anomalileri bulma ve tarama geliştirme fikri; görsel metni TUPRS eşik/kantil anomali gösterimidir. Ham yedi yöntemle anomali bulunabileceğini söyler; belirli alış veya satış önerisi yerine kod çalışmasını tanıtır.
tweet-evds-api-mevduat-faizi-cekme-1766868425815535946 · veri çekme kodu (EVDS API, seri TP.TRY.MT02: TL 3 aya kadar mevduat faizi) ve makro görüş (faiz, enflasyon); kural öğesi yok
tweet-excel-degerleme-calismasi-koda-donusumu · değerleme, kapsam dışı: TASARIM §3
tweet-faiz-artisi-sektor-etkisi-1918962559870283779 · Faiz artışı, ÜFE/TÜFE, kredi ve sektör etkilerine ilişkin makroekonomik açıklama; sanayi, inşaat, otomotiv ve dayanıklı tüketim kanallarını anlatır.
tweet-faiz-indirimi-sektor-rotasyonu-1933105044791906410 · Faiz indirimi, WACC, enflasyon ve sektörlerin beklenen tepkisine ilişkin değerleme açıklaması; kapsam dışı: TASARIM §3.
tweet-faiz-karar-botu-zaman-serisi-nlp-1913122317263057042 · Faiz kararı tahmin botu proje fikri; NLP ve zaman serisini birleştiren karar simülasyonu önerir. Hisse alım-satım kuralı yerine gelecekte geliştirilecek makro tahmin aracını anlatır.
tweet-faiz-paritesi-uip-forward-prim-1906617987676696651 · Faiz paritesi ve forward prim eşitliklerini tanımlar; döviz değerlemesi, kapsam dışı: TASARIM §3.
tweet-faktor-beta-usdtry-duyarlilik-1862799793593934301 · USDTRY gibi makro faktörlere hisse duyarlılığını beta ile ölçen analiz aracının tanıtımı; alım-satım talimatı yerine modelin amacını anlatır.
tweet-fama-french-factor-beta-1893286879052648887 · Fama-French faktör betası, SMB ve HML kavramlarını açıklayan eğitim notu; değer yatırımına ilişkin model tanımı.
tweet-favok-yillik-buyume-fiyat-2087251201691685145 · FROTO FAVÖK büyümesi ve geçmiş fiyat performansı yorumu; değerleme, kapsam dışı: TASARIM §3. Ham %300 üzeri büyüme ve -%34 küçülme örneklerini tartışır.
tweet-fcfe-ddm-capraz-kontrol-degerleme-motoru · değerleme, kapsam dışı: TASARIM §3
tweet-fcfe-fcff-ddm-model-secimi-2037806406577828200 · FCFE, FCFF/DCF ve DDM değerleme modellerinin kullanım yeri, nakit akışı ve iskonto oranı karşılaştırması; kapsam dışı: TASARIM §3.
tweet-fed-dxy-yuan-gumus-zinciri-1994257611793875220 · Fed, DXY, yuan ve gümüş için makro senaryo açıklaması; resesyon ve yumuşak iniş ayrımı yapar. Emtia-makro bağlamı, hisse işlem kuralı değildir.
tweet-fibo-144-bar-786-bandi-1842305345110302780 · tarama çıktısı, kural öğesi yok (konu: C §23); tek hisse (AKSA) grafiği; @fiboborsa'ya yanıt: "Python taramasından çıkan hisselerden biri"
tweet-fibo-786-bandi-tepki-teyit-gostergeleri-1847021977669628220 · tarama çıktısı, kural öğesi yok (konu: C §23); MACKO ve ULUUN için gösterge ekranı §23'teki ekranla aynı, eşik yok
tweet-fibonacci-78-6-tepki-taramasi-1843361242519617709 · tarama çıktısı, kural öğesi yok (konu: C §23); IHAAS için EMA 89/144/233 ekranı §23/§24'te var
tweet-fibonacci-786-bandi-tepki-tarama-1851718708936282217 · tarama çıktısı, kural öğesi yok (konu: C §23); 30.10.2024 tarama listesi, EUREN grafiği
tweet-fibonacci-786-ema-rsi-tarama-1847613665018630286 · tarama çıktısı, kural öğesi yok (konu: C §23); VKGYO grafiği, Telegram bot ('Tbot admin') ekran görüntüsü; tarama botla gönderiliyor
tweet-finansal-borc-buyume-orani-python-2044481287348490525 · Finansal borcun yıllık büyüme yüzdesini hesaplayan Python örneği; temel bilanço analizi, kapsam dışı: TASARIM §3.
tweet-finansal-veri-api-kaynaklari-1762361028178796875 · araç tercihi: veri API listesi (Nasdaq Data-on-Demand, Alpha Vantage, Intrinio, IEX Cloud); BIST için kural öğesi yok
tweet-fiyat-esas-faaliyet-kari-uyumu-1917362530000986239 · Fiyat artışı ile esas faaliyet kârı düşüşünü değerleme riski olarak açıklayan temel analiz; kapsam dışı: TASARIM §3.
tweet-fiyat-grafigi-otesi-makro-bakis · haber: makro eğitim
tweet-fiyat-hbk-uyumsuzlugu-fake-ralli-1999967178410557740 · ADESE fiyat-HBK uyumsuzluğu vaka analizi; değerleme, kapsam dışı: TASARIM §3. Ham RSI 70/30 gözlemlerini ve %90 sahte yükseliş iddiasını içerir; bunlar bu yorumun unsurlarıdır.
tweet-fk-5-15-roe-ema200-alti-tarama-1913366510841536776 · Değerleme filtresi; kapsam dışı: TASARIM §3. Ham F/K 5-15, yüksek özsermaye kârlılığı ve fiyatın EMA200 altında olması şartlarını verir.
tweet-fk-bandi-alim-satim-froto-1916743082336285121 · FROTO F/K değerleme stratejisi; kapsam dışı: TASARIM §3. Ham 6.7 altında hazırlık, 6.3 altında kademeli alım, 5.0-3.5 agresif alım, 6.7-8.0 tutma ve 10 civarında satış eşiklerini verir.
tweet-fk-fd-favok-kar-tahmin-ortalama-deger-1756414209389150383 · SAYAS için kâr tahmini ve piyasa çarpanı modellerini ortalayan değerleme yöntemi; kapsam dışı: TASARIM §3. Ham kısa dönemi 8 çeyrek olarak verir.
tweet-fk-regresyon-tahmin-modeli-1781073109694447899 · Regresyon ile F/K tahmini önerisi; değerleme, kapsam dışı: TASARIM §3. Ham son yanıtta yinelenen temettü büyüme oranını temettü ödeme oranı olarak düzeltir.
tweet-fk-sektor-kisa-uzun-donem-hedef-fiyat-2040920818687832236 · 2023/12 verileri ile sektör ve tarihsel F/K değerleme tablosu; kapsam dışı: TASARIM §3. Görsel metni kısa/uzun dönem çeyrekleri ve ASUZU hedef değerlerini listeler.
tweet-fk-sektorel-sirket-ortalama-python-1852711643660083507 · Excel rasyo tablosundan şirket ve sektör F/K ortalamalarını hesaplayan kod örneği; değerleme, kapsam dışı: TASARIM §3.
tweet-fk-tahmini-regresyon-vif-10-1824814340668617001 · İleri dönem F/K regresyon tahmini ve deneysel model tanıtımı; değerleme, kapsam dışı: TASARIM §3. Ham birden fazla regresyon modeli deneyip hata payı en düşük olanı kullanmayı önerir.
tweet-fk-tarihsel-dip-tepe-al-sat-1948761534139617474 · Tarihsel F/K değerleme stratejisi; kapsam dışı: TASARIM §3. Ham 15 yıllık örnek, 3-5 alım ve 15 üzeri satış bölgelerini geçmiş tepkiye bağlı anlatır.
tweet-fk-zscore-52-hafta-esik-1-5-1948771787728454054 · F/K Z-skor değerleme taraması; kapsam dışı: TASARIM §3. Ham 52 haftalık ortalama ve sapma, -1.5 veya altında alım düşüncesi ve +1.5 veya üstünde satış değerlendirmesi verir.
tweet-fon-cikisi-satis-baskisi-tahmini-2099970636386812395 · proje fikri ve soru: fon çıkışının satış baskısını tahmin etme, geçmiş KAP raporlarıyla güven skoru; model, formül ve sonuç yok (konu: yeni fon çıkışı bölümü, E)
tweet-fon-gunluk-getiri-tahmini-katki-2097060991586447371 · THF günlük katkı tahmininin gerçekleşmediğini bildiren sonuç paylaşımı; işlem kuralı yerine tahmin performansı örneğidir.
tweet-fon-gunluk-getiri-tahmini-katki-2097065200687915032 · DOH günlük fon getirisi tahmininin isabetine ilişkin sonuç paylaşımı; işlem kuralı yerine tahmin performansı örneğidir.
tweet-fon-net-akis-getiri-tarama-2094913511986020386 · tarama çıktısı, kural öğesi yok (fon sıralama tablosu: 1G/5G/20G net akış, 20G getiri, Sharpe sütunları; konu: fon-risk-radari)
tweet-fon-ortak-agirlik-degisimi-birikim-2096343856476496081 · vaat / proje fikri: fon ağırlık değişimi ve ortak hareket analizi duyurusu, ölçü ve eşik yok (konu: fon-risk-radari)
tweet-fon-para-akisi-analizi-2097019577112600707 · fon yorumu (KHP para piyasası fonu), eşik yok; kural öğesi yok (konu: fon-risk-radari)
tweet-fon-secimi-treynor-m2-jensen-1979637504694464888 · Treynor, M2 ve Jensen analizlerini fon taramasına ekleme planı; tamamlanmış seçim kuralı yerine geliştirme niyetini anlatır.
tweet-forward-kur-monte-carlo-risk-primi-1966512882306179577 · Şirketlerin forward kur pazarlığı, Monte Carlo, risk primi ve kur volatilitesi yönetimi; döviz risk modeli, kapsam dışı: TASARIM §3.
tweet-froto-nakit-piyasa-degeri-18-89 · değerleme, kapsam dışı: TASARIM §3
tweet-fx-parity-regression-variables-1906617981221700057 · Döviz paritesi regresyonunun değişkenleri: kur değişimi, enflasyon farkı, faiz farkı ve forward prim; kur modeli, kapsam dışı: TASARIM §3.
tweet-fx-position-factor-beta-1913865330448879926 · Döviz pozisyonunu faktör modelleri ve beta ile ilişkilendiren bilanço analizi; temel analiz, kapsam dışı: TASARIM §3.
tweet-gartley-harmonik-fibo-oran-1962604746000277528 · tarama çıktısı, kural öğesi yok (konu: C §7); görselde yalnız etiketler: XA 2.66, AB -1.72, BC 0.82, CD -1.04, Fibo 0.618 28.06, Fibo 0.786 27.88; Ham şaka, koşul yok. Hesap (bizim): AB/XA ≈ 0,65, BC/AB ≈ 0,48, CD/BC ≈ 1,27, yani §7 aralıklarıyla uyumlu bir örnek; fiyat çizgilerinin hangi bacaktan çekildiği belli değil
tweet-gartley-harmonik-tarama-1950604013919150218 · Harmonik tarama duyurusu ve tek fiyat grafiği; Ham yalnız ertesi günün sonucunu beklediğini bildirir. Görsel metni örnek bacak uzunluklarını listeler.
tweet-gartley-harmonik-tarama-1950604352554672612 · Gartley örneğine övgü; Ham yalnız gartley'in güzelliği ifadesidir. Görsel metnindeki bacak uzunlukları seçilmiş örneğin ölçüleridir.
tweet-gbm-monte-carlo-fiyat-simulasyonu-1858993037722173743 · DOAS için GBM ve Monte Carlo fiyat simülasyonu tanıtımı; görsel metni simülasyon grafiğinin eksenlerini ve 10000 denemeyi bildirir. İşlem kararı yerine model çıktısı paylaşılır.
tweet-getiri-dagilimi-istatistik-analizi-1723657129066692666 · DOAS geçmiş getiri istatistikleri ve yatırım değerlendirmesi; ortalama, sapma ve uç getiriler örneklem sonuçlarıdır.
tweet-getiri-korelasyon-matrisi-heatmap-1895180161261412820 · Altı hisse için korelasyon matrisi çizdirme kodu ve ısı haritası; araç tanıtımıdır.
tweet-getiri-pct-change-portfoy-temeli-2020503416938860634 · Veri indirme ve günlük getiri hesabı ders özeti; portföy optimizasyonuna giriş eğitimidir.
tweet-gizli-pozitif-uyumsuzluk-tespiti-2046685232066097536 · Python ile çizilen uyumsuzluk grafiğinin tanıtımı. Ham çizgilerin yazılım tarafından üretildiğini anlatır.
tweet-gordon-buyume-modeli-temettu-degerleme · değerleme, kapsam dışı: TASARIM §3
tweet-gorunmeyen-varlik-carpan-degerleme-1946857813327876099 · Marka, yazılım, patent ve müşteri sadakatinin şirket değerlemesine katılması açıklanır. Konu bilanço ve çarpan değerlemesidir.
tweet-grid-bot-stop-hedef-seviyeleri-1840389925788635186 · Güncellenmiş gridbot indirme paylaşımı ve EKGYO örnek işlem seviyeleri çıktısı. Formül yerine çıktının paylaşımıdır.
tweet-gun-saat-satis-heatmap-pivot-1764250055114899657 · dış kapsam: pazarlama satış analitiği (gün-saat ısı haritası, perakende verisi), BIST işlem kuralı yok
tweet-gunluk-yatay-kanal-tarama-1962980857469170156 · DERIM yatay kanal tespitinin seçilmiş çıktı örneği; Ham kodun iyi çalıştığını bildirir, görsel metni örnek kanal aralığını listeler.
tweet-haber-akisi-makine-ogrenmesi-1853895705217147159 · Geçmiş haberlerle BIST tepkisini öğrenen model geliştirme planı; tamamlanmış bir işlem sistemi paylaşılmaz.
tweet-haftalik-black-swan-sonuc-ornegi-1873395749804966002 · Haftalık NUHCM Black Swan çıktısı için seçilmiş sonuç paylaşımı. Ham geçen hafta paylaşılan örneğin harekete başladığını bildirir.
tweet-haftalik-boga-bayragi-kirilim-1907535347296174534 · Haftalık boğa bayrağı örneği ve tekrar beklentisi sorusu. Görsel metni yalnız kırılım tarihini verir.
tweet-haftalik-boga-bayrak-kirilimi-1900554823331635298 · Seçilmiş boğa bayrağı kırılım duyurusu. Ham görselde günlük yazmasına rağmen periyodun haftalık olduğunu düzeltir.
tweet-haftalik-harmonik-formasyon-taramasi-1870898053881934052 · Aralık içinde tamamlanan dört haftalık harmonik örnek paylaşımı. Grafik metinleri seçilmiş formasyonların bacak uzunluklarını ve Fibonacci seviyelerini verir.
tweet-haftalik-harmonik-formasyon-taramasi-1871631845055685007 · Orta vadeli yatırımcıya haftalık NUHCM harmonik örneği paylaşımı. Bacak ve Fibonacci seviyeleri örnek çıktıdır.
tweet-haftalik-kanal-kirilimi-vwap-tarama-2049157737360065010 · COSMO haftalık kanal ve VWAP grafiğinin sonuç paylaşımı. Ham oluşan marja dikkat çeker; çıktı örnek kanalı ve çizili göstergeleri tanımlar.
tweet-haftalik-pivot-destek-direnc-1866670388639568347 · 9737 seviyesine olası düzeltme yorumu ve pivot grafiği. Tek tarihli piyasa beklentisidir.
tweet-haftalik-pivot-pp-r1-1908528429424582781 · BTCUSD için haftalık PP/R1 seviyelerinin iyi çalıştığı yorumu. Kripto örneği ve geçmiş sonuç paylaşımıdır.
tweet-haftalik-range-breakout-1936801552372519179 · ULUUN haftalık range breakout seçilmiş sonuç grafiği. Ham kazanım övgüsü içerir.
tweet-haftalik-swing-vwap-seviyeleri-1987305332721524852 · OZSUB haftalık dinamik VWAP, swing destekleri ve dirençleri raporu. Tek tarihli seviye çıktısıdır.
tweet-haftalik-tobo-boyun-kirilimi-1923093092237709652 · Haftalık TOBO örneği paylaşımı. Ham yalnız formasyonu adlandırır; görsel metni fiyat grafiğinin eksenlerini verir.
tweet-haftalik-tobo-taramasi-1902066033009291375 · Haftalık TOBO taramasından tek grafik paylaşımı. Ham yalnız formasyonu adlandırır.
tweet-haftalik-yatay-kanal-tarama-1956028500407619964 · ARDYZ haftalık yatay kanal örneği ve geçmiş işlem övgüsü. Kanal ölçüleri örnek çıktıdır.
tweet-hammer-buy-signal-scan-1898324842044133705 · 6 Mart Hammer tarama listesi ve 7 Mart sonuç övgüsü. YESIL seçilmiş örnektir.
tweet-harami-green-scan-1898311765017956811 · MAGEN Harami taraması ve ertesi gün tavan iddiası. Tek seçilmiş sonuç örneğidir.
tweet-hareketli-ortalama-backtest-araci-1979931015771517315 · araç tercihi: harici hareketli ortalama backtest sitesi bağlantısı ("Kaydedin lazım olur"), kural öğesi yok
tweet-harmonik-butterfly-tarama-fibo-seviyeleri-1883641498564264218 · IHEVA Butterfly taramasından tek örnek. Ham yalnız formasyon adını söyler; görsel metni örnek bacak ölçülerini listeler.
tweet-harmonik-d-noktasi-bolge-1999919258638176557 · SELEC hibrit harmonik/RSI grafiği paylaşımı. Ham paylaşma niyetini belirtir; çıktı tek örnektir.
tweet-harmonik-d-tp-stop-seviyeleri-2094135381419606299 · Günlük harmonik yapının TP ve stop seviyeli tek örneği. Ham sonucu belirsiz bir beklenti olarak sunar.
tweet-harmonik-formasyon-dedektoru-1870247700957946232 · Harmonik dedektörünün tamamlandığı ve taramanın hazırlanacağı duyurusu. KCHOL seçilmiş sonuç örneğidir.
tweet-harmonik-formasyon-fibo-seviyeleri-1870627477254721649 · CEMTS Black Swan örneği paylaşımı ve analizi okuyucuya bırakma mesajı. Bacak ve Fibonacci seviyeleri örnek çıktıdır.
tweet-harmonik-formasyon-fibo-seviyeleri-1870891005924585533 · BIZIM, BRSAN, KRONT ve SUWEN harmonik örnekleri. Ham formasyon adlarını listeler ve beğeni ister.
tweet-harmonik-formasyon-fibo-seviyeleri-1871623972544274600 · ALCAR günlük Gartley örneği paylaşımı. Ham tamamlanan formasyonu hediye olarak sunar; ölçüler tek örneğe aittir.
tweet-harmonik-formasyon-fibo-seviyeleri-1871624647734923639 · BVSAN günlük Black Swan örneği paylaşımı. Görsel metni örnek bacak ve Fibonacci seviyelerini verir.
tweet-harmonik-formasyon-fibo-seviyeleri-1871626708304150884 · EGGUB günlük Butterfly örneği paylaşımı. Ham formasyonu ve periyodu adlandırır.
tweet-harmonik-formasyon-fibo-seviyeleri-1872027142181232735 · MRGYO Alt Bat örneği ve beğeni çağrısı. Görsel metni örnek ölçülerini verir.
tweet-harmonik-formasyon-fibo-seviyeleri-1873389418914234688 · Seçilmiş EGGUB sonuç paylaşımı. Ham Gartley derken açılan görsel Butterfly adını taşır; örnek adlandırması çelişkilidir.
tweet-harmonik-formasyon-fibo-seviyeleri-1874132152021115346 · ALCAR örneğinin önceki paylaşıma bağlı yıl sonu sonuç yorumu. İşlem sistemi yerine seçilmiş grafik paylaşılır.
tweet-harmonik-formasyon-taramasi-1870623312260513908 · AGHOL Beyaz Kuğu geçmiş örneği ve kodu daha önce yazmış olma isteği. Geçmişe dönük seçilmiş sonuç yorumudur.
tweet-harmonik-formasyon-taramasi-1871632842897461539 · BIST Black Swan örneğinde formasyonun çalıştığı iddiası. Bacak ölçüleri tek örneğe aittir.
tweet-harmonik-kelebek-tespit-1998859904845766784 · PRZMA Kelebek örneği için temkinli paylaşım. Ham formasyonu beğenmediğini ve sonucu kısmete bıraktığını söyler.
tweet-harmonik-kopekbaligi-tespit-1999178373705400710 · MHRGY köpekbalığı tespitinin paylaşımı ve yeniden gönderme çağrısı; görsel dökümü bu tek örneğin formasyon bacaklarını ve gösterge panellerini sunar.
tweet-harmonik-xabcd-fibo-tespiti-1899198147823366265 · Kodun yakaladığı örneğe övgü; görsel dökümü MIATK Engulf Green çıktısı ve EMA5/8/13 çizgileridir. Not başlığından harmonik kural türetilmez.
tweet-harmonik-xabcd-fibo-tespiti-1907086886956372475 · Bullish crab için sonuç bekleyen tek örnek; görsel dökümü bu örneğin bacaklarını sunar.
tweet-harmonik-xabcd-oranlari-1839739709989237220 · XABCD görselini kodlama niyeti; görsel dökümündeki 0,667, 1,529, 0,662 ve 0,896 tek çizim etiketleridir.
tweet-hbk-net-faaliyet-kari-yorumu-1917574325323895006 · Değerleme ve temel analiz; HBK ile net faaliyet kârının birlikte yükselişi olumlu, ikisinin düşüşü riskli okunur. Kapsam dışı: TASARIM §3.
tweet-hbk-net-kar-odenmis-sermaye-24-ceyrek-1911030882531418617 · Değerleme: 24 çeyrek HBK hesabı, son 12 dönem gösterimi ve son 4 dönem yıllık HBK toplamı. NEFK artışı ile HBK artışı olumlu, NEFK düşerken HBK artışı geçici gelir uyarısıdır. Kapsam dışı: TASARIM §3.
tweet-hbk-period-momentum-1911030864818937888 · Temel analiz veri hazırlığı: 3/6/9/12 aylık mali tablolar, XI_29→UFRS→UFRS_K sırası ve HBK sistemi tanıtımı. Kapsam dışı: TASARIM §3.
tweet-hbk-yilliklandirilmis-fk-hesabi-1916736171838767120 · Değerleme: güncel fiyat / yıllıklandırılmış HBK ile F/K hesabı; son dört çeyrek ve sektör karşılaştırması. Kapsam dışı: TASARIM §3.
tweet-heikin-ashi-olcekli-rsi-1842913670592163990 · TUPRS Heikin Ashi ve -40/+40 ölçekli RSI gösterimi hakkında kullanım sorusu ve backtest beğenisi.
tweet-heikin-ashi-taramasi-1845163805984059682 · Heikin Ashi taraması için dosya bağlantısı ve paylaşım çağrısı.
tweet-hilo-kesisim-al-sat-1877605823737729513 · DOAS HiLo al/sat sinyalinin tek örnek çıktısı; Ham gelen sinyali duyurur.
tweet-hisse-getiri-hesaplama-kodu-1886081532466475239 · Öğrencilere getiri hesaplama kodu bağlantısı; CSV yerine yf ile veri indirme önerisi.
tweet-hisse-korelasyon-matrisi-1949096413641543721 · Bilişim ve yazılım hisselerinin korelasyon matrisi; hücreler gözlem değeridir, bu paylaşım doğrudan bir çift seçimi kararı vermez.
tweet-hsar-yatay-destek-direnc-2086822816695918859 · Algoritmik örüntü tanıma kitabı ve FROTO HSAR çıktısı; destek/direnç fiyatları tek örneğin çizim etiketleridir.
tweet-iki-ceyrek-buyume-yavaslamasi-altin-2083875779218198689 · ABD büyümesinde art arda en az iki çeyrek yavaşlama ile altın talebi ilişkisi; BIST hisse işlem kapsamı dışındaki makro/altın incelemesi.
tweet-iki-cizgi-trend-degisimi-1987956410379104378 · THYAO trend değişimi çıktısına ilişkin çalışma duyurusu; görsel dökümünde SR1 (SARI-10), YSL (YEŞİL-6) ve tarihli sinyaller yer alır.
tweet-ilk-200-gun-max-min-kirilim-2038167666242748877 · GC=F altın vadeli işlem grafiğinde ilk 200 gün maksimum/minimum çizgileri; BIST hisse işlem kapsamı dışındaki araç örneği.
tweet-implied-volatility-okuma-1932156513432256960 · Opsiyon IV kavramı: beklenen hareket büyüklüğü yön belirtmez; bilanço, haber ve kırılım beklentisi bağlamı. Kapsam dışı: TASARIM §3 (opsiyon).
tweet-ina-favok-marji-sonsuz-buyume-1695183583676113357 · SAYAS indirgenmiş nakit akışı değerlemesi; Ham 2024 satış büyümesini %100, sonraki yılları %40 varsayar. Kapsam dışı: TASARIM §3.
tweet-ina-kar-tahmin-carpan-degerleme-1850987001161322723 · İNA, kâr tahmini ve çarpan analizini Excel’den Python’a taşıma niyeti. Kapsam dışı: TASARIM §3 (değerleme).
tweet-ina-on-yillik-veri-kosulu-1781414242047984084 · Değerleme: İNA için 10 yıllık mali veri; istikrarlı şirket için F/K 6–16 ve net kâr marjı Sharpe >2; CANTE özelinde F/K 5–8 alım görüşü. Kapsam dışı: TASARIM §3.
tweet-iq-csharp-python-veri-hatti-1964627639425270263 · araç tercihi: veri hattı (IQ verisi C# kodu ile çekilir, Python'da işlenir; API yok), kural öğesi yok
tweet-iq-excel-python-akd-verisi-1970561329590354082 · araç tercihi: veri alımı (IQ Excel eklentisi + Python; AKD verisi, yf yetmez), kural öğesi yok
tweet-is-yatirim-bilanco-veri-toplama-1942613749073879070 · eğitim: bilanço verisini İş Yatırım'dan otomatik toplayıp klasörde havuzlama önerisi; veri yöntemi, değerleme tarafı (kapsam dışı: TASARIM §3), kural öğesi yok
tweet-isyatirim-financial-data-source-1889446483449037295 · araç tercihi: İş Yatırım finansal verisi (class tipi kodla erişim), değerleme verisi (kapsam dışı: TASARIM §3), kural öğesi yok
tweet-iv-ani-artisi-bilanco-haber-beklentisi-1909184195953295533 · Opsiyon IV ani artışının yaklaşan bilanço/haber beklentisi olarak yorumlanması. Kapsam dışı: TASARIM §3 (opsiyon).
tweet-iv-delta-takas-karar-matrisi-1936705102133301277 · Opsiyon IV, delta ve takas karar matrisi; yüksek IV/yüksek delta/alım yoğunluğu olumlu, satım yoğunluğu uyarı olarak okunur. Kapsam dışı: TASARIM §3 (opsiyon).
tweet-iv-hv-orani-persentil-max-oi-1939330303618662583 · AAPL opsiyon incelemesi: 30 günlük HV, bir yıllık dağılım persentili, IV/HV 1,37 ve 215 USD direnç örneği. Kapsam dışı: TASARIM §3 (opsiyon).
tweet-iv-sd-bantlari-destek-direnc-stop-2004570898192302503 · Opsiyondan türetilen IV/SD stratejisi: yükselen trendde -1SD alım, genellikle -2SD altı stop ve pivot/trend kesişimi teyidi. Kapsam dışı: TASARIM §3 (opsiyon).
tweet-iv-takas-fiyat-uclu-sinyal-1932151673390285171 · Opsiyon IV ile takas modeli önerisi: örnek senaryoda üç gün artan IV, yabancı net alımı, artan hacim ve açık pozisyon. Kapsam dışı: TASARIM §3 (opsiyon).
tweet-iv-yukselisi-yatay-fiyat-kirilim-1925561082392834472 · Opsiyon IV yükselişi ile yatay fiyatın yönü bilinmeyen kırılım beklentisi olarak okunması. Kapsam dışı: TASARIM §3 (opsiyon).
tweet-kama-10-2-30-supertrend-al-sat-1853053450319286714 · KAMA ile Supertrend birleşiminin GARANTI üzerinde deneme çıktısı; KAMA daha sık işlem açıp kapatıyor gözlemi ve dalgalı hisseler için olasılıklı değerlendirme.
tweet-kanal-asagi-kirilim-tespiti-1871248456964329949 · CMBTN aşağı kanal kırılımının tek grafik çıktısına Python övgüsü.
tweet-kanal-gecisi-olculu-hareket-1770920833109639207 · KCHOL için üst kanala geçiş sonrası bir haftada yaklaşık %22 potansiyel görüşü; tarihli hisse tahmini.
tweet-kanal-kirilimi-hacim-onayi-1904044260556509658 · Offset yöntemiyle kanal kırılımı grafiği ve trend özdeyişi; başlık tek örnekte kullanılan yöntemi tanıtır.
tweet-kanal-kirilimi-regresyon-r2-1904029830036775278 · Grupta yapılan harmonik, bayrak/flama, OBO/TOBO ve kanal taramalarının duyurusu; odağın momentum faz alanları olduğu açıklanır. R² değerleri tek grafik çıktısıdır.
tweet-kanal-kirilimi-retest-taramasi-2015849090161025288 · ERBOS retest çıktısı paylaşımı ve okuyucuya araştırma çağrısı; sekiz gün önceki kırılım bu örneğin zaman etiketidir.
tweet-kap-agirlik-gunluk-hisse-katkisi-2099944754511278524 · THF fonunun KAP ağırlıkları ve günlük hisse katkı raporu; fon portföyü raporlama örneği, hisse işlem kuralı olarak kullanılmaz.
tweet-karlilik-oranlari-sektor-karsilastirma-1695424938251796654 · SAYAS kârlılık oranlarının geçmiş dönem ve sektör karşılaştırma tablosu. Kapsam dışı: TASARIM §3 (değerleme).
tweet-kelebek-abcd-fib-uzanti-d-hedef-2092340608480297126 · tarama çıktısı, kural öğesi yok (konu: C §3): KRPLS D hedefleri 11.29 [TAMAM], 10.05 [TAMAM], 7.83 [BOZULDU] ve uzantı ızgarası (0.000 8.42 … 2.000 11.30) §3'ün KRPLS örnekleriyle aynı; G3'te X-B çizgili harmonik, D 11.20 [TAMAMLANDI] (konu: C §9 şablonu), G2'de kırılım etiketleri (Temas, RSI Kırılım); Ham: "Bu da serbest dusus" yorum
tweet-kisa-periyot-momentum-indikatorleri-1840173948811530658 · Tansu’nun kendisinin işlem yapmadığını belirttiği 15 dakikalık zaman dilimi için RSI/MACD/momentum/Supertrend araç önerisi; günlük sistem dışında teorik kısa vade yanıtı.
tweet-kisa-vadeli-finansal-yukumluluk-payi-2086152222870536647 · Bilanço incelemesi: kısa vadeli finansal yükümlülüklerin kısa vadeli yükümlülüklerde yaklaşık %10 payı olumlu değerlendirilir. Kapsam dışı: TASARIM §3 (temel analiz).
tweet-kmeans-silhouette-pca-kume-gorsellestirme-1762356653779763260 · eğitim: müşteri kümeleme (K-means, silhouette, PCA) kod örneği; ürün/kargo verisi, trade kuralı yok (havuz etiketi: dış kapsam)
tweet-kmv-distance-to-default-1851754725680488551 · KMV temerrüde uzaklık modelinin çalışma amacı ve kavram şeması. Kapsam dışı: TASARIM §3 (temel analiz).
tweet-kredi-analizi-yatirim-kontrol-listesi-1913877696590876973 · Şirket kredi analizi kontrol listesi: kullanım amacı, geri ödeme, ortaklık, SWOT ve kredi geçmişi incelemesi. Kapsam dışı: TASARIM §3 (temel analiz).
tweet-kripto-harmonik-formasyon-taramasi-1873445492048412848 · HEGIC-USD kripto deep crab tarama çıktısı ve tamamlanma duyurusu; tarihli örnek, BIST hisse kapsamı dışında.
tweet-kripto-harmonik-formasyon-taramasi-1873447078531391896 · HEGIC-USD Deep_crab grafiği ve bacak uzunlukları; tek kripto formasyonu çıktısı.
tweet-kripto-harmonik-formasyon-taramasi-1873447542824042560 · FTM-USD Shark grafiği ve bacak uzunlukları; tek kripto formasyonu çıktısı.
tweet-kripto-harmonik-formasyon-taramasi-1873451580521099741 · DIA-USD Gartley grafiği ve bacak uzunlukları; tek kripto formasyonu çıktısı.
tweet-kripto-harmonik-formasyon-taramasi-1874171816165638347 · Saatlik ONT-USD Butterfly grafiği ve bacak uzunlukları; tek kripto formasyonu çıktısı.
tweet-kripto-korelasyon-cift-taramasi-1859336518604816885 · Kripto çiftleri için tarihli al-sat ve korelasyon sonuç tablosu; tarama çıktısı.
tweet-kripto-korelasyon-cift-taramasi-1874123378564751802 · Kripto çiftleri için korelasyona göre sıralanmış yfinance sonuç tablosu; tarama çıktısı.
tweet-kripto-korelasyon-cift-taramasi-1874128145231843628 · Binance kripto çiftleri için tarihli al-sat ve korelasyon sonuç tablosu; tarama çıktısı.
tweet-kripto-rsi-uyumsuzluk-macd-filtre-tablosu-1910818851954077948 · BCH-USD RSI uyumsuzluk grafiği ve kripto tarama sonuç tablosu; RSI 30 ve MACD sıfır konumları sonuç sütunlarıdır.
tweet-kumulatif-getiri-fiyat-olcegi-karsilastirma-1826052707150361031 · Farklı fiyat ölçeklerini kümülatif getiri ile karşılaştırma açıklaması; performans sunumu.
tweet-kumulatif-getiri-fonksiyonu-1822596707558760524 · Kitap için mutlak ve yüzde kümülatif getiri fonksiyonu açıklaması; performans hesabı eğitimi.
tweet-kur-farki-esas-faaliyet-kari-1692269598073094408 · Temel analiz: kur farkı gideri olasılığına karşı esas faaliyet kârına bakma yanıtı; kapsam dışı değerleme.
tweet-kur-riski-forward-monte-carlo-risk-primi-1984661206162964976 · Şirket kur riskinde forward pazarlığı, Monte Carlo, risk primi ve Euro volatilitesi çerçevesi; hisse işlem sistemi dışı kur yönetimi.
tweet-lasso-alpha-rmse-selection-1825488501254578373 · Lasso düzenlileştirmesinde alpha, RMSE ve katsayı davranışı eğitimi; işlem sinyali yerine model ayarı açıklaması.
tweet-likidite-orani-esik-1-sektor-ortalamasi-1949414090499112967 · Temel analiz, kapsam dışı değerleme: son dört çeyrek likidite oranı, örnek risk eşiği 1 altı ve sektör ortalaması filtresi; sektör üstünde istikrar veya iyileşme takibi.
tweet-likidite-oranlari-analiz-sablonu-1781773593480720390 · FROTO finansal analiz şablonu; kapsam dışı değerleme. Görsel metninde cari oran için 1,0 üstü tercih edilir.
tweet-likidite-sikisma-altin-gumus-rasyo-1992188666593112507 · Japonya likidite sıkışması ve altın/gümüş rasyosu üzerine makro senaryo; emtia ve kur bağlamı. Yüzde 5/2 düşüş ile 80/90/100 rasyo değerleri açıklama örnekleridir.
tweet-lineer-grafik-kisa-vade-log-uzun-vade-1984620734136602784 · Kısa vadede lineer, uzun vadede logaritmik grafik okuma açıklaması; fiyat gösterim yöntemi.
tweet-log-vs-linear-chart-scale-1953201892202307992 · Uzun vadede logaritmik, kısa ve dar aralıkta lineer grafik açıklaması; gösterim tercihi.
tweet-lojistik-regresyon-temerrut-risk-skoru-1888561699722031190 · Temerrüt risk modeli; kapsam dışı bilanço/değerleme çalışması. Örnek kategoriler 0,00–0,20 düşük, 0,21–0,50 orta, 0,51–1,00 yüksek; modele ve sektöre göre değişebilir.
tweet-low-pe-trap-check-1913884830405693941 · Değerleme, kapsam dışı: F/K 5 altının tek başına değer göstermediği; sektör, büyüme ve kârlılık trendi kontrolü.
tweet-lsma-ols-tahmin-1844843534156701805 · LSMA/OLS koduna dış bağlantı ve gelecekte sinir ağı çalışması duyurusu; notta açıklanan içerik araç paylaşımıdır.
tweet-ma1-otokorelasyon-formulu-1945117767059038312 · MA(1) zaman serisinin varyans ve otokorelasyon türetimi; istatistik eğitimi.
tweet-macd-12-26-9-cufflinks-kodu-1837799586166972425 · Cufflinks ile MACD gösterge hesaplama ve çizim eğitimi; 12/26/9 grafik ayarlarıdır.
tweet-macd-12-26-9-wma-13-60-kod-1762082053330440337 · MAVI için MACD 12/26/9 ve WMA 13/60 hesaplama ve grafik kodu paylaşımı; gösterge çizim örneği.
tweet-macd-5-gun-uyumsuzluk-karsilastirma-1839083016456442293 · AEFES tek hisse MACD pozitif uyumsuzluk tarama grafiği; beş gün karşılaştırması başlıkta yer alır.
tweet-macd-5-gun-uyumsuzluk-karsilastirma-1839083246379774447 · AGHOL tek hisse MACD pozitif uyumsuzluk tarama grafiği; beş gün karşılaştırması başlıkta yer alır.
tweet-macd-5-gun-uyumsuzluk-karsilastirma-1839083538265645555 · AKFGY tek hisse MACD pozitif uyumsuzluk tarama grafiği; beş gün karşılaştırması başlıkta yer alır.
tweet-macd-haftalik-pozitif-uyumsuzluk-1843754494062145990 · AKCNS, EREGL, TUPRS ve VKGYO haftalık MACD uyumsuzluk tarama sonuçları; dört hafta karşılaştırmalı eğitim grafikleri.
tweet-macd-pozitif-uyumsuzluk-taramasi-1837867391310540998 · ISCTR için BIST30 MACD pozitif uyumsuzluk tarama sonucu ve fiyat/MACD çizim kodu; tek örnek çıktı.
tweet-macd-pozitif-uyumsuzluk-taramasi-1837875098834882936 · BIMAS fiyat ve MACD pozitif uyumsuzluk grafiği; günlük çalıştırma niyetiyle paylaşılan seçilmiş sonuç.
tweet-macd-pozitif-uyumsuzluk-taramasi-1837886506586755338 · BRSAN için 12 Temmuz uyumsuzluğunun geçmişe dönük seçilmiş grafik sonucu.
tweet-macd-pozitif-uyumsuzluk-taramasi-1840349130532544681 · AKGRT Supertrend bearish sinyali ile haftalık ve günlük MACD uyumsuzluk grafiklerinin karşılaştırılması; seçilmiş çelişkili gösterge çıktısı.
tweet-macd-pozitif-uyumsuzluk-taramasi-1843752733347852648 · HEKTS için 3/5/10 gün pozitif uyumsuzluk sonuçları ve beş günlük karşılaştırma grafiği; tarama çıktısı.
tweet-macd-son-gun-al-backtest-1861839074463474170 · MACD son gün AL taraması için harici BacktesterClass kodu bağlantısı ve ileri seviye kullanım duyurusu.
tweet-macd-uyumsuzluk-grafikleme-1837850713247842570 · MACD negatif uyumsuzluk grafiği paylaşımı; grafikleme eğitimi ve ayrı tarama çalışması duyurusu.
tweet-macro-factor-beta-sensitivity-1888872602493448198 · Temel analiz ve makro faktör betası; kapsam dışı değerleme. Döviz yükselişi beklentisinde yüksek faktör betası ve olumlu yabancı para net pozisyonu filtresi önerilir.
tweet-maddi-duran-varlik-artisi-fiyat-2086038590417522979 · FROTO maddi duran varlık artışı ile fiyat ilişkisi; bilanço temelli değerleme, kapsam dışı.
tweet-makro-faktor-beta-analizi-1943070389388873813 · Hisse/makro faktör beta sonuç grafikleri ve öğrencilere yorumlama sorusu; faktör analizi eğitimi.
tweet-makro-faktor-korelasyon-matrisi-1948872188653699417 · Makro faktör korelasyon matrisi ve takip çağrısı; tarihli istatistiksel çıktı.
tweet-markowitz-iki-hisse-portfoy-1759294658004291906 · DOAS/GESAN için %70/%30 portföy ve bir yıllık getiri/risk örneği; tarihli ağırlıklandırma sonucu, genel sabit dağılım kuralı değildir.
tweet-mavilim-kesisim-sinyali-1943066690709070008 · MAVİLİMW fiyat kesişimleriyle AL/SAT işaretli örnek grafik; Python uygulaması paylaşımı.
tweet-mavilimw-kesisim-al-sat-1877599322851741828 · MAVİLİMW fiyat kesişimleriyle AL/SAT işaretli örnek grafik ve tarama paylaşma duyurusu.
tweet-max-oi-strike-iv-karsilastirma-1936838035485983031 · AAPL maksimum OI strike 205 dolar ile ima edilen/tarihsel volatilite karşılaştırması; opsiyon analizi, kapsam dışı.
tweet-max-sharpe-portfoy-secimi-2011146964000449005 · HEDEF/ECILC/ALKA üçlü Max-Sharpe portföyünün tarihli ağırlık sonucu ve etkin sınır grafiği; günlük paylaşım sonucu.
tweet-merton-iflas-riski-makro-faktor-var-1971347390725861395 · Merton iflas riskine makro faktörler, VAR etki-tepki, CIR faiz ve rejim geçişi ekleme önerisi; bilanço risk modellemesi, kapsam dışı.
tweet-merton-kredi-fiyatlama-parametreleri-1852095049011433982 · Merton kredi fiyatlama örneği; A0=100, varlık volatilitesi=0,25, borç=80, faiz=0,05 ve vade=1 başlangıç ayarları; kapsam dışı kredi/değerleme.
tweet-merton-model-temerrut-tablosu-1851750265239609482 · Merton temerrüt olasılığı, beklenen kayıp ve borç değerleme örneği; kapsam dışı kredi risk projesi.
tweet-merton-modeli-iflas-riski-1907840086084874577 · Merton/KMV iflas risk modeli; kapsam dışı bilanço/değerleme. Ham sınıfları DD > 2 çok güvenli, DD yaklaşık 1–1,5 orta risk, DD < 1 artan risk.
tweet-min-vol-max-sharpe-karsilastirma-2015507534979748036 · Momentum listesinden seçilen üçlü Min-Vol ve Max-Sharpe portföylerin tarihli ağırlık/getiri karşılaştırma sonucu.
tweet-minimum-risk-portfoy-sepet-1763067841606000707 · EREGL/GARAN/BIMAS/AKBNK/TUPRS için Min-Vol ve Max-Sharpe ağırlıkları ile getiri/risk sonuçlarının karşılaştırması; örnek çıktı.
tweet-minimum-varyans-portfoy-etkin-sinir-1760181402333577279 · ABD hisseleri için minimum varyans portföyünün performans ve ağırlık listesi ile etkin sınır grafiği; tarihli sonuç.
tweet-momentum-dilim-getiri-sharpe-1771618495223996854 · Momentum dilimlerinin yıllık getiri/Sharpe grafikleri ve Max-Sharpe/Min-Vol etkin sınır çıktıları; tarihli sonuç sunumu.
tweet-momentum-filtre-sinyal-takibi-1866600397357424772 · BIST momentum grafiğinin o güne ait aşağı kırılım gerçekleşmedi durum bildirimi.
tweet-momentum-scan-fvg-fill-1893708657478492479 · BIGCH için momentum listesinde görünme ve boşluğu doldurma gözlemi; tek hisseye ait geçmiş hareket yorumu.
tweet-monte-carlo-avrupa-call-fiyatlama-1897644272918081670 · Avrupa tipi call opsiyonunu Monte Carlo ile fiyatlayan kod; kapsam dışı: TASARIM §3 (opsiyon).
tweet-monte-carlo-gbm-fiyat-simulasyonu-1858372675342598641 · GBM fiyat yollarının ortalamasından hisse veya opsiyon değeri belirleme çalışması; kapsam dışı: TASARIM §3 (değerleme).
tweet-muhafazakar-carpan-secimi-1695379852642189814 · En yüksek tarihsel F/K yerine muhafazakâr tahmin öneren değerleme yaklaşımı; kapsam dışı: TASARIM §3 (değerleme).
tweet-nefk-artar-hbk-artmaz-uyumsuzluk-1893717988043342127 · NEFK artışı ile HBK artışı arasındaki ayrışmadan gelecekte fiyat artışı bekleyen temel analiz; kapsam dışı: TASARIM §3 (değerleme).
tweet-nefk-hbk-ayrisma-potansiyel-marj-1889068388334370953 · NEFK yükselirken HBK yükselmemesini potansiyel marj olarak okuyan temel analiz; momentum bağlamı var; kapsam dışı: TASARIM §3 (değerleme).
tweet-nefk-hbk-karsilastirma-gizli-firsat-1892680047779074122 · NEFK artarken fiyatın artmamasını olası fırsat sayan temel analiz; kapsam dışı: TASARIM §3 (değerleme).
tweet-negatif-reel-faiz-altin-2083953538661539956 · Stagflasyon, nominal/reel faiz ve altın ilişkisi; altın ve makro senaryo kapsamı, BIST hisse işlem kuralı değildir.
tweet-net-isletme-sermayesi-devir-oranlari-1951223829453259190 · NİS ihtiyacı, mevcut sermaye ve alacak/stok/borç devir süreleriyle finansal sağlık değerlendirmesi; kapsam dışı: TASARIM §3 (temel analiz).
tweet-net-kar-marji-esas-faaliyet-sicrama-tarama-1709805069644820609 · Ham filtresi net kâr marjı (sharpe) >2 ve NEFK sıçramasına karşı fiyatın henüz hareket etmemesidir; takas, INA, DuPont ve özsermaye/FK analizleriyle değerleme kapsamı; TASARIM §3 dışı.
tweet-net-kar-marji-sektor-karsilastirma-1979215761173348439 · TMSN net kâr marjının sektör ortalaması ve fiyat grafiğiyle karşılaştırılması; kapsam dışı: TASARIM §3 (temel analiz).
tweet-net-yabanci-para-pozisyonu-satis-orani-1950865602647646516 · FROTO net yabancı para pozisyonu/satış oranından kur ve bilanço riskine, faktör ve GARCH fiyat tahminine uzanan temel analiz; kapsam dışı: TASARIM §3.
tweet-net-ypp-yillik-satis-orani-kur-etkisi-1915860915729166759 · Birikimli satışları çeyrekleştirme, yıllıklandırma ve Net YPP/satış × kur değişimi ile bilanço etkisi değerlemesi; kapsam dışı: TASARIM §3. Ham örnekte %0,486 ile 100 milyon cirodan 48,6 milyon sonucu birlikte yazılıdır; aritmetik düzeltilmedi.
tweet-nihai-hedef-tek-tus-temel-teknik-degerleme-llm-nlp · vaat: hedef beyanı
tweet-nispi-ppp-kur-enflasyon-testi-1907020119080935479 · makro, kur ve enflasyon farkı testi (nispi PPP), kural öğesi yok, kapsam dışı
tweet-normalize-makro-faktor-takibi-1948878388761919613 · Euro/TRY, BIST100 ve ons altının normalize eğrileri üzerinden makro döngü ve kur şoku izleme önerisi; makro tahmin kapsamı.
tweet-numpy-returns-volatility-montecarlo-1912781858145808482 · NumPy vektörleştirme, broadcasting, korelasyon, regresyon, volatilite ve simülasyon eğitimi; son beş fiyat ortalaması örneği araç kullanımını gösterir.
tweet-obo-boyun-cizgisi-tespit-1998101671155741183 · CRFSA OBO ve boyun çizgisi grafiği üzerinden okuyucuya yöneltilen durum sorusu; belirli örnek hakkında yorum talebi.
tweet-oncu-gostergeler-listesi-1846663491203318269 · Ichimoku, PSAR, OBV, Stokastik ve uyumsuzlukları öncü gösterge olarak adlandıran araç listesi.
tweet-opsiyon-call-put-duvari-1994748031900492128 · GC=F altın opsiyon call/put duvarları ve call duvarının mıknatıs etkisi; kapsam dışı: TASARIM §3 (opsiyon, altın).
tweet-opsiyon-oi-strike-direnc-delta-1980136440672465307 · AAPL call delta/strike/OI örneği; 255 kırılımı, 250 altı alım ve 250–255 bant işlemi koşulları vardır; kapsam dışı: TASARIM §3 (opsiyon, ABD hissesi).
tweet-optimal-momentum-plus-simulasyon-tamamlandi · vaat
tweet-otokorelasyon-durbin-watson-kontrolu-1950584440805081552 · Zaman serisi ve kesitsel regresyonda otokorelasyon, bağımsızlık varsayımı ve Durbin-Watson hakkında ekonometri eğitimi.
tweet-ozellik-secimi-korelasyon-pca-1941790321668432140 · Regresyon özellik seçiminde yorumlanabilirlik için korelasyon, büyük boyutlu tahmin için PCA karşılaştırması; modelleme eğitimi.
tweet-ozkaynak-artisi-varlik-finansman-yatirim-verimliligi · değerleme, kapsam dışı: TASARIM §3
tweet-pandas-rolling-volatility-filters-1912735331918516711 · Pandas rolling, filtreleme, normalizasyon, eksik veri ve görselleştirme eğitimi; 20 günlük std ve MA200 karşılaştırması araç örnekleridir.
tweet-pandas-zaman-serisi-kod-kaliplari-2023876641689075990 · eğitim (pandas zaman serisi kod kalıpları tablosu)
tweet-panik-sonrasi-birikim-sureci-1991190753322701181 · Anna Coulling alıntısıyla panik sonrası yavaş birikimi anlatan davranışsal piyasa açıklaması.
tweet-parite-kodu-enflasyon-faiz-farki-1906617992508584357 · Enflasyon/faiz farkı ve forward priminden kur değişimi tahmin eden parite kodu; kapsam dışı: döviz/uluslararası parite.
tweet-pca-faktor-regresyon-endeks-hedef-1771536925809135885 · PCA ile makro faktörleri seçip BIST100 getirisine regresyonla hedef endeks değeri tahmini önerisi; proje fikri.
tweet-pd-dd-beklenen-ozsermaye-degerleme-2041968928205766731 · ASUZU beklenen özsermaye ve sektör/kısa/uzun dönem PD/DD çarpanlarıyla hedef fiyat değerlemesi; açılan ikinci görsel fiyat/trend çizimidir; kapsam dışı: TASARIM §3.
tweet-pd-net-satis-carpan-daralmasi-2043007802344370231 · ASUZU PD/net satış çarpan daralması ve kârlılık ayrımı üzerinden değerleme; kapsam dışı: TASARIM §3.
tweet-pddd-roe-sektor-tarihsel-value-trap-filtresi · değerleme: Ham bir filtre verir (düşük PD/DD + yüksek ROE + sektör altı çarpan; 36 çeyrek çıpa); kapsam dışı: TASARIM §3
tweet-pddd-sektor-tarihsel-roe-filtresi-2042694526268047744 · Düşük PD/DD + yüksek ROE + sektör altı çarpan filtresi; 36 çeyreklik tarihsel ortalamayı çıpa yapan değerleme ve değer tuzağı uyarısı; kapsam dışı: TASARIM §3.
tweet-period-net-profit-capital-extract-1913605982594138565 · bilanço kalemi (net kâr, sermaye) çekme kodu, değerleme ve temel veri, kapsam dışı: TASARIM §3
tweet-pine-script-python-gorev-ayrimi-veri-backtest-icra · araç tercihi
tweet-piyasa-carpanlari-kar-tahmin-ortalama-fiyat-1700795951890256309 · FROTO piyasa çarpanları, kâr tahmin modeli ve INA hedef fiyatlarının ortalamasıyla değerleme; kapsam dışı: TASARIM §3.
tweet-ppo-rl-trading-agent-1912522737773383734 · PPO öğrenen ajan projesi ve Open/Hold/Close aksiyon mimarisi duyurusu; öğrenilmiş işlem politikası yerine proje yaklaşımını anlatır.
tweet-ppo-with-separate-forecast-1912527539655811203 · PPO aksiyon politikası ile ayrı fiyat tahmin modülünün mimari karşılaştırması; yazılım tasarımı önerisi.
tweet-psar-lrc-mum-formasyonu-kombinasyonu-2043779884867076189 · TRGYO PSAR/LRC ve mum kombinasyonunun grafik sonuç paylaşımı; Ham, yazılan kodun kalabalıklığına ilişkin kişisel tercih bildirir.
tweet-psi-agirlikli-beklenti-formulu-1904627496487649715 · Döviz kuru tahmini için geometrik ağırlıklı beklenti denklemi ve gelecek kod duyurusu; fiyat modelleme eğitimi.
tweet-psi-normalize-agirlikli-ortalama-1904909627801624887 · Psi ağırlık normalizasyonu ve model amacına göre parametre seçimi açıklaması; tahmin modeli eğitimi.
tweet-put-call-duvari-rejim-kurali-2085630100037406985 · Kapsam dışı: TASARIM §3 (opsiyon, ons altın). Ham, put duvarı 3846 üstünde yükseliş ve call duvarı 4251 üstünde momentum koşullarını verir.
tweet-python-ai-stratejik-yonetim-vizyon-misyon-kodlama · kurumsal proje, kapsam dışı
tweet-python-direnc-cizgisi-onceki-tepe-1826718993950146703 · ARÇELİK grafiğine tarih seçerek destek ve EMA ekleme kodu paylaşımı; çizim yardımcısı.
tweet-python-finans-verisi-ogrenme-yol-haritasi · eğitim
tweet-q2-faaliyet-kari-artis-sepet-stratejisi-1957003613827420651 · Kapsam dışı: TASARIM §3 (temel değerleme). BIST50 içinde son dört Q2 faaliyet kârı artışı filtresi, ENKAI örneği ve bilanço öncesi alım/sonrası satış önerisi.
tweet-q2-satis-4-yil-surekli-artis-taramasi-1956830336467243263 · Kapsam dışı: TASARIM §3 (temel değerleme). Otomotivde son dört yılın Q2 net satışları sürekli artan şirket filtresi; yüksek momentumlu sektör/endeks seçimi önerisi.
tweet-q2-satis-buyume-cagr-tarama-1956848925543206980 · Kapsam dışı: TASARIM §3 (temel değerleme). Son dört yıl Q2 satış büyümesi BIST50 tablosu ve CAGR karşılaştırması.
tweet-range-momentum-sinir-agi-1940140382408626504 · Range ve momentum özelliklerini yapay sinir ağına girdi yapma önerisi; öğrenme veri seti ve model mimarisi anlatımı.
tweet-rasyo-kumeleme-mlp-hisse-secimi-2086819758138134758 · değerleme, kapsam dışı: TASARIM §3 (10 finansal rasyo ile kümeleme ve MLP süzme şeması; rasyo listesi ve eşik yok)
tweet-regression-forward-pe-forecast-1826661985305702552 · Kapsam dışı: TASARIM §3 (değerleme). Regresyonla F/K 24 tahmini tarihsel 24–25 ortalamasıyla karşılaştırılır.
tweet-regression-models-error-comparison-1825625155139145879 · Model seçimi sorusu; OLS, Ridge, Lasso ve diğer tahmin modellerinin hata ölçü tablosu.
tweet-regresyon-kanali-bant-sinyali-1873520948949008581 · Altın fiyatında regresyon kanalı örnek grafiği ve davet paylaşımı; emtia örneği.
tweet-regresyon-ml-rasyolardan-piyasa-degeri-sapmasi · değerleme, kapsam dışı: TASARIM §3
tweet-relatif-degerleme-piyasa-norm-bantlari · değerleme, kapsam dışı: TASARIM §3
tweet-resesyon-altin-primi-2085258283170889857 · ABD büyüme yavaşlaması ve altın primi üzerine makro/emtia yorumu; iki çeyrek yavaşlama ve üçüncü çeyrek resesyon ihtimali örnekleri.
tweet-ridge-optimal-alpha-fk-tahmini-1825279192390594981 · Kapsam dışı: TASARIM §3 (değerleme). BIMAS F/K için Ridge alpha 0,26 ile 20,89 tahmini ve deneysel hata ölçüleri.
tweet-risk-neutral-measure-pricing-1911126822588154108 · Kapsam dışı: TASARIM §3 (opsiyon fiyatlama/değerleme). P ve Q ölçüleri ile risk nötr yoğunluk dönüşümü eğitimi ve AKBNK örnek kodu.
tweet-risksiz-faiz-iskonto-etkisi-1925214172616556966 · Kapsam dışı: TASARIM §3 (değerleme). ABD on yıllık faizinin %5 olmasının WACC, iskonto ve hisse değerlemesine etkisi.
tweet-roc-nopat-yatirilan-sermaye-hesabi · değerleme, kapsam dışı: TASARIM §3
tweet-roc50-adx-obv-fibo-ema-paneli-1842218572157759579 · DOAS için ROC, ADX/ADXR, OBV, EMA ve Fibonacci panellerinin örnek çizimi; Ham grafiğe nasıl bakılacağını sorar.
tweet-roe-artan-ozsermaye-trendi-1918372698268549332 · Kapsam dışı: TASARIM §3 (temel değerleme). Özsermaye büyürken ROE'nin de artması ve yıllara yayılan kârlılık trendi incelemesi.
tweet-roe-ema200-fk-5-15-tarama-1913371749841858666 · Kapsam dışı: TASARIM §3 (temel değerleme). Yüksek ROE, EMA200 altında fiyat ve 5–15 F/K birleşimi; sektör kıyası.
tweet-roe-fk-5-15-ema200-tarama-1917737673801732180 · Kapsam dışı: TASARIM §3 (temel değerleme). Sektörüne göre yüksek ROE ve 5–15 F/K seçimi; otomotiv bilanço tablosu.
tweet-roe-net-kar-ozsermaye-formulu-1915483594597806535 · Kapsam dışı: TASARIM §3 (temel değerleme). Son dört çeyrek net kâr, cari/geçen yıl ortalama özsermaye, pozitif ROE sektör ortalaması ve EMA200 altı filtreleme anlatımı.
tweet-roe-sector-ema200-screen-1913363640226283736 · Kapsam dışı: TASARIM §3 (temel değerleme). Sektör ROE karşılaştırması ve EMA200 altı durumunu gösteren tablo biçimi güncellemesi.
tweet-roe-yuksek-fk-dusuk-200-gun-alti-1914714348368359654 · Kapsam dışı: TASARIM §3 (temel değerleme). Beklenen kâr üzerinden DuPont, yüksek ROE, düşük F/K ve 200 günlük ortalama altı seçimi.
tweet-rolling-korelasyon-ile-varlik-secimi-2084960697675325591 · Altın/gümüş için varlık seçimi; son 10 yıl ve bir yıllık rolling korelasyon/R² ile altın yükseliş beklentisine karşılık gümüş alma önerisi. Emtia kapsamı.
tweet-rolling-maximum-pencere-1784817550561284226 · Rolling maximum teriminin hareketli pencere içi en yüksek değeri kaydetme tanımı; istatistik/kodlama kavramı.
tweet-rsi-fibo-786-donus-1925626094935236883 · tarama çıktısı, kural öğesi yok (konu: C §34); ASTOR 22.05.2025, başlık "RSI Fibo 78.6 Dönüş & Mum Grafik", mum etiketleri CDLRICKSHAWMAN, CDLHARAMICROSS, CDLHARAMI; Ham: "Ne arasan var:)" ve "Bilgi amaçlıdır"
tweet-rsi-gizli-uyumsuzluk-1843387861770612872 · RSI Hidden Divergences V1 aracının bağlantısı ve Python taraması yazma duyurusu; alıntılanan aracın sahibi @TTesviyeci.
tweet-rsi-trendline-break-peak-detector-1908815347332899241 · RSI üzerinde dip-tepe algoritması çalışmasına başlama planı; tamamlanmış tarama değil.
tweet-sarimax-aic-adimsal-model-secimi-2019525738207060400 · SARIMAX modelinin AIC arama günlüğü ve bekleme yorumu; model geliştirme durumu.
tweet-satis-faaliyet-netkar-ayrisma-1917696323387810195 · Kapsam dışı: temel analiz; FROTO ilk çeyrek satış, faaliyet kârı ve net kâr ayrışması yorumu.
tweet-sektor-ici-en-yuksek-roe-tarama-1913883842542215527 · Kapsam dışı: değerleme filtresi; aynı sektörde yüksek ROE, fiyat EMA200 altında ve F/K 5-15 aralığında aday seçimi.
tweet-sektor-ortalama-carpan-karsilastirma-1941238181569183878 · Kapsam dışı: değerleme; F/K ve PD/DD karşılaştırmasını şirketin kendi sektör ortalamasıyla yapma ilkesi.
tweet-sektor-ortalama-roe-fk-ema200-1941488860137185289 · Kapsam dışı: değerleme; savunma şirketlerinde ROE, F/K ve EMA200 altında olma karşılaştırma tablosu.
tweet-sektor-ortalamasi-faaliyet-kari-buyumesi-2044511362269769989 · Kapsam dışı: temel analiz; ASUZU esas faaliyet kârının yıllık büyümesini otomotiv sektör ortalamasıyla karşılaştırır.
tweet-sektor-pd-dd-tarihsel-karsilastirma-2041613755423855037 · Kapsam dışı: değerleme; otomotiv PD/DD tarihsel ve anlık sektör karşılaştırması.
tweet-shooting-star-taramasi-1851744148518559891 · Shooting Star tarama dosyasının indirme bağlantısı ve yeniden yükleyememe duyurusu.
tweet-sirket-degerlendirme-sektor-isletme-finansal-degerleme-kontrol-listesi · değerleme, kapsam dışı: TASARIM §3
tweet-sma20-rolling-std-volatilite-1897620709624442886 · Pandas rolling() ile SMA20 ve kapanış fiyatının standart sapmasını hesaplama öğreticisi; grafik ve son değer tablosu gösterir.
tweet-sma200-intraday-rejection-1989347751818387468 · XAUUSD saatlik grafiğinde tek gün içi tepkinin övgüsü; Ham yalnız “İşte bu mükemmel bir intraday rejection!” der. SMA200/SMA250 ve RSI14 ekran değerleri bu gözlemin bağlamıdır.
tweet-sma21-ema9-grafik-kodu-1837543668888052053 · GE için 2018–2019 grafiğine SMA21 ve EMA9 ekleyen görselleştirme kodu; Ham “SMA21 ve EMA9, sizce nasıl olur?” diye görüş ister.
tweet-spekulatif-balon-psi-agirlikli-ortalama-1904911424641450458 · USD beklentilerinin psi ile ağırlıklandırılması ve MSE ile psi kalibrasyonu üzerine ekonometri örneği; BIST işlem kuralı yerine kur modeli açıklamasıdır.
tweet-spread-zskor-arbitraj-alani-1942316588176146874 · IHGZT–IHLGM spread ekranına ilişkin yön bulma sorusu; Ham “Kim yorumlayacak?” ve “hangisi long hangisi short?” der. Görsel metni belirli günün Z-skor ve arbitraj alanı etiketini verir; eğitim sorusu bağlamıdır.
tweet-stochrsi-ema-kodu-1878071323894702111 · StochRSI ve EMA kodu için dış dosya paylaşımı ve kod öğrenme uyarısı; paylaşım duyurusudur.
tweet-tahvil-efektif-sure-faiz-agaci-1851746402830807298 · Tahvil fiyatlama, faiz ağacı ve efektif süre eğitim görseli; hisse sinyali yerine tahvil değerleme bağlamıdır.
tweet-takas-virman-gercek-satis-ayrimi-1936386099225448628 · görüş: takas yorumu ilkesi (aracı kurumlar arası virman satış sayılmaz; birkaç gün veya hafta boyunca desen, hacim ve fiyat teyidi); eşik ve tarama koşulu yok; takas ve AKD verisi bedava günlük veride yok
tweet-talep-bolgesi-direnc-kirilim-taramasi-2055040107351072798 · SARKY için gerçekleşmiş tavan hareketi ve açılış fırsatı yorumu; tek hisse sonucunun ardından paylaşılmış kırılım ekranıdır.
tweet-talib-candle-pattern-labeling-1889453445549097041 · SELGD mumlarına TA-Lib adları eklenmiş grafik ve “Şiirini de yazmıştık” yorumu; gösterim örneğidir.
tweet-talib-candle-pattern-scan-1898114891531071762 · XU100 üzerinde oluşmuş mumların TA-Lib etiketleri ve kod paylaşmama duyurusu; tek tarihli tespit çıktısıdır.
tweet-talib-mum-formasyonu-etiketleme-1866680568965922864 · XU100 mum etiketleri eşliğinde o gün dikkatli olma çağrısı; belirli günün piyasa yorumudur.
tweet-talib-mum-formasyonu-taramasi-1907095706285826234 · XU100 üzerinde TA-Lib mum adlarıyla hazırlanmış günlük grafik ve “Arz ederim” sunuşu; tespit çıktısıdır.
tweet-tarihsel-carpan-stdsap-bantlari-1696022604472111319 · DOAS tarihsel F/K ve PD/DD grafiğine dayalı tek şirket değerleme yorumu; 400 üzeri hedef fiyat bu tarihli beklentidir.
tweet-telegram-bot-python-mesaj-1847042700467745116 · araç tercihi: Telegram bot ile algoritma çıktısı gönderme kodu; kural öğesi yok (TASARIM Telegram'ı "Yok" listesine koyar)
tweet-temel-filtre-sonra-teknik-tarama-1850990584338792873 · proje fikri: planlanan yeni nesil tarama, önce temel analiz ve fiyat değerlendirmesi süzgeci, sonra teknik tarama; eşik yok; değerleme, kapsam dışı: TASARIM §3
tweet-ters-omuz-bas-omuz-tespiti-1986119683108467034 · EREGL hakkında kişisel ve mizahi piyasa yorumu; geçmiş TOBO tespit grafiği eşlik eder.
tweet-to-float-excel-finansal-tutar-donusum-1956812751902474403 · araç: Excel'den gelen tutar metnini sayıya çeviren Python işlevi; kural öğesi yok
tweet-toplu-akd-cekme-kumulatif-veri-1967190744399327388 · araç tercihi, veri kaynağı (AKD her gün toplu çekilir ve kümülatif toplanır; Matrix bireysele API vermiyor); kural öğesi yok
tweet-topsis-cok-kriterli-hisse-secimi-2015048294649545183 · görüş: çok kriterli sıralama yöntemi (TOPSIS), eşik yok; proje fikri ve kod satış planı; girdiler F/K, PD/DD gibi değerleme verisi: kapsam dışı: TASARIM §3
tweet-topsis-cok-kriterli-hisse-siralama-motoru · görüş: sıralama yöntemi, eşik yok
tweet-topsis-hisse-secimi-yaklasan-proje · proje fikri
tweet-trend-destegi-temas-taramasi-2004244938373189697 · ADEL destek teması ekranı eşliğinde yeniden paylaşım isteği ve gidişat sorusu; tek günün izleme görüntüsüdür.
tweet-trendline-ilk-temas-kirilim-taramasi-1876021137383313484 · AFYON kırılım grafiğiyle paylaşılan mizahi yorum; ilk temas ve giriş tarihi içeren tek tarama örneğidir.
tweet-ttrak-pddd-primi-carpan-sikismasi · değerleme, kapsam dışı: TASARIM §3
tweet-two-stock-cumulative-spread-chart-1826114676817535204 · İki hisseyi kümülatif yüzde gelişim ve spread grafiğinde karşılaştırma kodu; görselleştirme eğitimi bağlamıdır.
tweet-uc-yontemli-carpan-degerleme-1769338002923298874 · DOAS için çarpan, kâr modeli ve indirgenmiş nakit akımı fiyatlamasını birleştiren değerleme anlatımı; hisseye özgü tahmini kâr ve WACC girdileri taşır.
tweet-ucgen-formasyon-taramasi-1904108571874259313 · DOGE-USD üçgen taramasının tamamlanma duyurusu ve örnek grafiği.
tweet-ucgen-formasyon-taramasi-1904256033763008735 · DOT-USD üçgen taraması için sonuç paylaşımı ve çalışma yorumu.
tweet-ucgen-formasyon-taramasi-1904256792198361335 · LTC-USD üçgen tespitinin örnek grafik çıktısı.
tweet-ucuz-hisse-200gun-alti-fk-pddd-1911119110798246227 · Değerleme kapsamı: 200 günlük ortalama altı fiyatı, güçlü finansallar ve sektöre göre uygun F/K ile PD/DD birlikte değerlendirilir (TASARIM §3).
tweet-usdcny-dusus-gumus-teyit-1994259185186353443 · Kapsam dışı gümüş ve döviz yorumu: FED faiz indirimi sırasında USD/CNY düşüşü gümüş için teyit olarak anlatılır.
tweet-ustel-ho-5-21-izleme-1816821058864886230 · Kişisel ekran izleme yanıtı: üssel HO 5–21 gün kullanımı anlatılır ve stratejisinin buna bağlı olmadığı açıkça belirtilir.
tweet-uzun-yatay-kanal-kirilimi-1947321881876382024 · Kimliği gizlenen hissenin 38 haftalık yatay hareket grafiği ve okuyucunun grafiği tamamlamasına yönelik paylaşım.
tweet-varyans-replikasyon-vrp-kesisim-2090161750444327119 · Kapsam dışı ABD opsiyon varyans primi: gerçek IV kullanan risk primi modeli ile modelden bağımsız varyans replikasyonunun kesişimi; %12 olası hareket örneği.
tweet-vegas-tuneli-taramasi-1844075976613154828 · DNISI Vegas taramasının örnek grafik çıktısı ve okuyucuya bırakılan değerlendirme.
tweet-vegas-tuneli-taramasi-1844829993517326540 · FRIGO Vegas tarama sonucu ve DNISI geçmiş kârına ilişkin örnek yorum; 521 hisse taranan örnek evrendir.
tweet-volatilite-arbitraji-iv-hv-delta-hedge-1925556979520487602 · Kapsam dışı opsiyon arbitrajı: IV ile gerçekleşen volatilite farkı, delta hedge, long/short vega ve gamma pozisyonları; TASARIM §3.
tweet-wacc-capm-temettu-tahvil-ortalama-2036552143470002482 · Değerleme kapsamı: CAPM, temettü indirgeme ve tahvil artı risk primiyle özsermaye maliyeti ortalaması, ardından WACC; TASARIM §3.
tweet-wacc-uc-yontem-ortalama-rs-2036528581526917387 · Değerleme kapsamı: üç yöntemle Rs ortalaması ve WACC hesabının Python çıktı tablosu; TASARIM §3.
tweet-wacc-uc-yontem-ozsermaye-ortalama-1911632045777789394 · Değerleme kapsamı: üç özsermaye maliyeti yönteminin ortalaması ve WACC; yeni projelerin getirisi WACC oranını geçmiyorsa yatırım yapılmaması anlatılır; TASARIM §3.
tweet-wbdata-dunya-bankasi-makro-veri-cekme-1860262968446824713 · araç ve veri: wbdata ile ABD toplam rezerv serisini çekip çizen Python kodu (makro veri); kural öğesi yok
tweet-williams-r-doji-macd-tarama-1844739877859930532 · Gelecek geliştirme planı: Williams %R taramasına doji, MACD, EMA ve T3 sürümleri ekleme ve verimliliklerini test etme duyurusu.
tweet-williams-r-macd-kesisim-1849541640152588314 · Williams R ve MACD kesişimleri için gelecek strateji duyurusu.
tweet-xu100-dusen-trend-cizgisi-kirilimi-2088425168657952901 · XU100 için tarihli karar bölgesi ve uzun vadeli düşen trende yaklaşırken zayıflama yorumu; iki tarihli trend çizgisinin örnek durum paylaşımı.
tweet-yatay-kanal-akd-takas-inceleme-1962983036904968431 · DMSAS yatay grafik, günlük aracı kurum dağılımı ve takas tablolarının okuyucu analizine bırakıldığı örnek.
tweet-yatay-kanal-tespiti-1942196593928650791 · AFYON yatay kanalının örnek grafik çıktısı ve kanal içi hareket yorumu.
tweet-yatirim-artisi-90-rsi-50-tarama-1950916832409403513 · Temel analiz kapsamı: otomotiv hisselerinde yatırım artışı %90 üstü ve günlük RSI>50 birleşik filtresi; TASARIM §3 dışındaki temel veri gerektirir.
tweet-yf-gecikme-gunluk-periyot-1849792794132435435 · araç tercihi, veri kaynağı: yfinance 15 dk gecikmeli, günlük veri tercihi, gecikme için en az 4 saatlik periyot önerisi (veri zamanlaması: E K30); işlem eşiği yok (Yahoo kullanılmaz: TASARIM §5.1)
tweet-yfinance-bist-is-uzantisi-1761496087221707093 · araç tercihi, veri çekme kodu: yfinance BIST .IS eki; kural öğesi yok
tweet-yfinance-close-auto-adjust-true-1892947326915739997 · araç tercihi, kütüphane sürüm uyarısı (yfinance auto_adjust=True, Adj Close yerine Close); kural öğesi yok
tweet-yfinance-haftalik-veri-cekme-1849540753816453297 · araç tercihi, veri çekme kodu (yfinance interval 1wk); kural öğesi yok
tweet-yfinance-hareketli-ortalama-20-50-150-kodu-1979643710326653361 · AAPL verisi üzerinde hareketli ortalama ve standart sapma hesaplayıp grafik çizme eğitimi; 20/50/150 ve 100 pencereleri çizim örneğine aittir.
tweet-yfinance-multi-stock-merge-1897595128165929334 · araç tercihi, veri çekme kodu (iki hissenin Close serisini birleştirme); kural öğesi yok
tweet-yfinance-multiindex-droplevel-1893614943657755035 · araç tercihi, kütüphane düzeltmesi (MultiIndex droplevel); kural öğesi yok; tekrar: tweet-yfinance-close-auto-adjust-true-1892947326915739997
tweet-yfinance-multiindex-duzeltme-1893610096833200443 · araç tercihi, kütüphane düzeltmesi (MultiIndex); kural öğesi yok; kod hacmi 0 olan satırları atar (veri temizliği, eşik yok)
tweet-yfinance-opsiyon-zinciri-iv-open-interest-1909203207387037837 · kapsam dışı: TASARIM §3 (opsiyon); ABD örneği (AAPL zinciri), kural yok
tweet-yfinance-plotly-mum-grafigi-kodu-1983214789644976325 · araç tercihi, grafik kodu (Plotly mum grafiği, DOAS); kural öğesi yok
tweet-yfinance-veri-eksikligi-1846284880206086632 · araç tercihi, veri kaynağı uyarısı (yfinance son günler eksik olabilir); kural öğesi yok
tweet-yillik-hbk-fiyat-ayrisma-1954539134158041128 · Değerleme kapsamı: yıllıklandırılmış HBK yönü ile fiyat ayrışmasını değerlendirme; kâr artarken fiyatın geride kalması fırsat, kâr düşerken yüksek fiyat risk örneği; TASARIM §3.
tweet-yilliklandirilmis-veri-carpan-1917565014988218574 · Temel değerleme kapsamı: dört çeyrek yıllıklandırılmış finansal verilerle mevsimsellik, sürdürülebilir kâr ve F/K karşılaştırması; TASARIM §3.
tweet-yon-olasilik-esik-sinyali-1958130783354323290 · DITAS için 2025-08-19 tarihli 0,99 yön olasılığı LONG bias model çıktısı ve ertesi gün performans yorumu.
tweet-yonetim-hedefli-kar-tahmin-modeli-1706542464125776037 · Değerleme kapsamı: SMRTG için CEO ciro ve FAVÖK hedeflerinden kâr tahmin modeli, piyasa çarpanı hedefleri ve tarihli fiyat beklentileri; TASARIM §3.
tweet-ytd-ceyreklik-ttm-yillandirma-bilanco-1956754276270641304 · Temel değerleme kapsamı: YTD farklarından çeyreklik veri, son dört çeyrek toplamıyla TTM üretimi; duran varlıklar, faaliyet/net kâr ve sektör F/K karşılaştırması; TASARIM §3.
tweet-yuksek-beta-martingale-1876964680947696067 · görüş: yüksek betalı hisse ile martingale iddiası; deneysel çalışma atfı kaynaksız; koşul, parametre ve sonuç yok
tweet-yukselen-trend-destek-temas-taramasi-2016245363062005978 · MAGEN destekli trend taramasının geçmişte çalıştığına ilişkin seçilmiş grafik örneği ve basitlik yorumu.
tweet-yukselen-ucgen-kirilim-tespiti-1954244081036546156 · RALYH yükselen üçgen kırılımının tarihli grafik çıktısı ve okuyucuya yöneltilen değerlendirme sorusu.
tweet-yutan-formasyon-taramasi-1843017197884760484 · Boğa/ayı yutan formasyon tarama kodu bağlantısı ve KCHOL örnek çıktı paylaşımı.
tweet-zigzag-tobo-tespiti-onay-1908975769994596535 · Haftalık TOBO için örnek grafik ve iyi dilek paylaşımı.
tweet-finans-muhendisligi-destek-direnc-seviye-motoru · Araştırma niyeti; Ham: Yakında denemeye başlayacağız. Finans mühendisliğiyle destek/direnç bulma sorusudur; işlem koşulu, model veya formül vermez (Ham; Ham'da yazar yok).

## Kısa atıfların tam adları (bilet 04, 14.10)

A–E dosyaları bazı notlara kısa adla atıf verir: `gorsel-paket-NN` notuna gp-NN, G-NN, GNN veya -NN; `tweet-X` notuna T-X; `kaynak-X-<tweet no>` notuna kaynak-X. Tam dosya adları (ad denetimi için):

gorsel-paket-01-harmonik-formasyon-tarama
gorsel-paket-02-coklu-sistem-provenance
gorsel-paket-03-smrtg-abcd-backtest
gorsel-paket-06-sektor-getiri-liderleri
gorsel-paket-07-sektor-anomali-temizleme
gorsel-paket-12-doas-advance-block
gorsel-paket-21-confluence-alan-taramasi
gorsel-paket-32-gartley-abcd-talep-dusen-kirilimi
gorsel-paket-33-min-vol-max-sharpe-dey-bist100
gorsel-paket-35-beyaz-kugu-sell-abcd-dusen-kirilimi
gorsel-paket-37-gunluk-rebalancing-aktif-pasif
gorsel-paket-38-akcns-haftalik-abcd-talep-ema
gorsel-paket-39-abcd-detector-fibo-talep-tepki
gorsel-paket-40-haftalik-abcd-talep-tepki
gorsel-paket-42-buy-abcd-yukselen-destek-hedefler
gorsel-paket-43-rysas-buy-abcd-kanal-baglamı (dosya adında ASCII dışı "ı" var)
gorsel-paket-47-lindsay-trident-abc-b-kirilimi-d
gorsel-paket-50-bist100-bist-volatilite-gulumsemesi
gorsel-paket-51-cimsa-oyakc-rotatif-zskor-portfoy
gorsel-paket-52-agrot-garan-duygusuz-disiplin-mtm
gorsel-paket-53-stat-arb-bag-kopusu-negatif-backtest
gorsel-paket-54-stat-arb-pairs-trading-kanonik-aciklama
gorsel-paket-55-volatilite-arbitraj-otonom-sistem-tercihi
gorsel-paket-57-tektu-eregl-agirlik-duyarliligi
gorsel-paket-59-buyhold-sinyal-risk-scorecard
gorsel-paket-62-froto-corwin-schultz-spread-sigma
gorsel-paket-69-przma-bullish-fvg-revisit-ote
gorsel-paket-96-momentum-161700-uclu-portfoy-aramasi
gorsel-paket-98-piyasanin-nabzi-teknik-rapor
gorsel-paket-99-klmsn-momentum-multitimeframe-bos-demand-fibo
gorsel-paket-101-avod-demand-bearish-fvg-supply-ema
gorsel-paket-102-enjsa-elliott-wave5-hikkake-fvg-outcome
gorsel-paket-107-bryat-smc-elliott-wave2-fvg-wave3
gorsel-paket-109-balat-harmonik-tp-cd-retracement
gorsel-paket-110-elliott-wave2-fib-fvg-yuzde8
gorsel-paket-111-elliott-5plus3-fibonacci-islem-gunleri
gorsel-paket-113-bist-vix-long-bes-adim-kontrol
gorsel-paket-114-bist-vix-python-master-analiz
gorsel-paket-115-position-sizing-yuzde1-2atr-sma250
gorsel-paket-116-veriden-sinyale-algoritmik-trader-gelistirme
gorsel-paket-118-yatirimci-basarisizlik-surec-risk-kontrol
gorsel-paket-120-fibonacci-coklu-aralik-konfluans
gorsel-paket-122-makim-gartley-fvg-momentum
gorsel-paket-123-gartley-algoritmik-takip-formul-mutabakati
gorsel-paket-125-kismi-kar-trailing-prev-low-emergency-stop
gorsel-paket-126-bist-order-book-derinlik-bmp-fit
gorsel-paket-127-aztek-istatistiksel-uc-kapitulasyon-obi-ayi-tuzagi
kaynak-kointegrasyon-sinirlari-2093658795700338821
kaynak-xu100-corwin-schultz-2096145981062475910
tweet-algoritma-tasarimi-temelleri-trading-sistemleri
tweet-garch-standart-sapma-volatilite-risk-minimizasyonu
tweet-kagit-kalem-matematik-once-kod-sonra
tweet-kendini-yenileyen-algoritma-ana-frekans
tweet-kitap-model-sentezi-backtest-forward-test-kod-mimarisi
tweet-likit-hisseler-etf-islem-derinligi-slippage-kapasite
tweet-piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi
tweet-volatilite-ters-orantili-position-sizing-sermaye-koruma
