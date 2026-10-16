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
       Biz üst sınırda gün yüksekliğini alırız; çünkü varsayılan giriş kuralı böyledir (YORUM).
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
         periyotlar YORUM). Listedeki hacim maddesi hacim süzgecindedir.
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
         yukarı gider. ATR sinyal günü değeridir (YORUM; E K25'te giriş günü ATR'sidir, o değer giriş AOF'undan önce
         bilinmez).
       - Başabaş çıkışı (E K32). Tansu: "Eğer kârlı bölgeye geçtikten sonra fiyat geri dönerek tekrar tam olarak giriş
         fiyatınıza ulaşırsa, derhal pozisyondan çıkmanız gerekir."
         (`tweet-under30-over30-1-5r-basabas-cikis-1992547498343161903`, Ham). Yüksek ≥ giriş + 1,5 × R ise stop =
         max(stop, giriş). Aktivasyon fiyat alanı olarak gün yüksekliği YORUM'dur (E K32).
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
         başlar. SMA250 çıkışı bildirilen gün yarı satış ve kural tetiklerine bakılmaz. "Önceki gün" son dolu gündür.
         Aynı güne iki dönemin sinyali düşerse ilk dönemin kutusu ve hedefi kullanılır. K1 rastgele girişinde kutu ve
         hedef yoktur (`atr2` yedeği, hedef çıkışı yok; YORUM).
     - **Piyasa durumu** (Levent 16.10): yalnız bilgidir, kartı durdurmaz (TASARIM §3).
     - **Varyantlar** (`aileler.VARYANTLAR`). Temel `tansu`: periyotlar (20, 50, 100, 200), giriş `mum`, hacim 2 kat,
       momentum açık, teyit `yok`, stop `kutu`, hedef `tansu`, R/R 2, çıkış `atr3` (YORUM: Tansu'nun söylediği
       kuralların birleşimi). Her varyant temelden tek boyut değiştirir. `bugun` istisnadır: varsayılan `Parametre()`
       değerleridir, yani yukarıdaki Giriş maddesinin bugünkü kuralıdır; karşılaştırma tabanıdır. Her varyant ayrı kural
       kimliği ve ayrı denemedir (TASARIM §5.11). Günlük kart `bugun` ile kalır (TASARIM §6).

       | Varyant | Değişen boyut ve değer | Kaynak |
       |---|---|---|
       | `bugun` | giriş `kutu`, hacim 0, momentum kapalı, teyit `yok`, stop `atr2`, hedef `yok`, çıkış `yok` | bugünkü kural (yukarıdaki Giriş maddesi) |
       | `tansu` | temel | yukarıdaki maddeler |
       | `ema_5_8_13` | periyotlar (5, 8, 13) | Tansu: "Ben 5-8-13 kullandım." (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham) |
       | `ema_50_100_200` | periyotlar (50, 100, 200) | Tansu örnekleri: B §25, B §62 |
       | `giris_kutu` | giriş `kutu` | bugünkü giriş kuralı |
       | `giris_ema` | giriş `ema` | Giriş türü, `ema` |
       | `giris_retest` | giriş `retest` | Giriş türü, `retest` |
       | `giris_agresif` | giriş `agresif` | Giriş türü, `agresif` |
       | `hacim_yok` | hacim 0 | hacim süzgecinin karşılaştırması (YORUM) |
       | `hacim_3` | hacim 3 kat | Tansu: 2-3 kat (üst uç) |
       | `momentum_kapali` | momentum kapalı | momentum squeeze süzgecinin karşılaştırması (YORUM) |
       | `teyit_acik` | teyit `gosterge` | Gösterge teyidi |
       | `teyit_trend` | teyit `trend` | Trend teyidi |
       | `stop_atr15` | stop `atr15` | Levent 16.10; E K25 |
       | `stop_atr2` | stop `atr2` | Levent 16.10; E K2 |
       | `cikis_dip` | çıkış `dip` | E K4, K5 |
       | `cikis_rsi70` | çıkış `rsi70` | E K5 |
       | `cikis_rsi50` | çıkış `rsi50` | E K5 |
   - K1 ön şartı: (a) türünde sıkışma dönemi bitmiş ve 10 günlük pencere açık günler; (b) türünde sıkışma penceresi şartı aranmaz, yalnız hisse düzeyi şartlar (kapanış ≥ SMA250, ısınma, evren, karantina) aranır (TASARIM 5.7; bilet 03). Ek kol: sıkışmasız aynı kırılım (kapanış önceki 20 günün en yüksek yükseğinin üstünde, sıkışma penceresinde değil; 20 YORUM, TASARIM 5.7).
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
tweet-200sma-250sma-rsi30-kilit-noktalar-1979927243942944965 · görüş ve vaat: 200SMA, 250SMA ve RSI 30 "kilit nokta" denir, koşul ve örnek yok (konu: E K3 SMA250 çıkışı, E K5 RSI 30 girişi)
tweet-9aydan-yilsonu-satis-net-kar-tahmini · değerleme, kapsam dışı: TASARIM §3
tweet-abcd-formasyon-python-tespiti-2053210859061535153 · örnek grafik, koşul yok (THYAO AB=CD çıktısı; Ham: "python ne güne duruyor"; konu: C §3)
tweet-akd-matrix-iq-gunluk-veritabani-1964445184328159257 · araç tercihi, veri kaynağı (AKD Matrix IQ'dan alınıyor, günlük veri tabanı planı); kural öğesi yok
tweet-akd-veri-kaynagi-api-1941449822050848997 · araç tercihi, veri kaynağı (AKD için Matrix IQ ve Algolab); kural öğesi yok; tekrar: tweet-akd-matrix-iq-gunluk-veritabani-1964445184328159257
tweet-alim-satim-listesi-index-esitleme-1852430160085020742 · araç tercihi, kod yardımcısı (alım ve satım fiyat listesini endeks uzunluğuna eşitler), kural öğesi yok
tweet-analitik-ag-sureci-hisse-secimi-1944868638307311952 · eğitim (Analitik Ağ Süreci yöntem anlatımı); eşik, parametre ve ölçülen sonuç yok
tweet-arima-hiperparametre-acf-pacf-grid-search · eğitim: model seçimi
tweet-arz-talep-bolgesinde-formasyon-bekleyisi · sohbet; tekrar: tweet-formasyon-arz-talep-confluence-kapisi ham kaydı
tweet-arz-talep-denge-fiyati-kodu-1906972824842965372 · eğitim (iktisat alıştırması: Qd=100-2P, Qs=50+3P Python kodu); arz-talep bölgesi (demand/supply) değil, kural öğesi yok
tweet-asuzu-coklu-degerleme-tutarliligi · değerleme, kapsam dışı: TASARIM §3
tweet-atr-tabanli-stop-seviyesi-1987562052194644270 · tarama çıktısı, kural öğesi yok (konu: E K2): TAVHL için "STOP: 247.20, ATR: 8.90, AL" etiketi, giriş fiyatı ve koşul yok
tweet-aylik-ortalama-maliyet-birikim-1783840694043623592 · kişisel yatırım alışkanlığı (aylık düzenli alım, ortalama maliyet, hedef 2028-2030); kural öğesi yok
tweet-az-yatirimcili-fon-risk-kontrolu-1979721927809012208 · eğitim, fon riski uyarısı (11 yatırımcılı fon örneği); eşik yok (fon kapsamı: E K26)
tweet-beklenen-fk-coklu-regresyon-modeli · değerleme, kapsam dışı: TASARIM §3
tweet-beklenti-al-gerceklesen-sat-2085043282694779123 · görüş: slogan, ölçülür giriş veya çıkış koşulu yok
tweet-beta-formul-rejime-gore-secim-2001638298473894378 · değerleme: beta tanımı (kovaryans / varyans); görsel rejime göre beta yönü verir (boğada Beta > 1, ayıda Beta < 1, yatayda Beta ≈ 1.0); rejim tanımı ve hesap penceresi yok; aynı içerik gorsel-paket-108-beta-risk-pusulasi; kapsam dışı: TASARIM §3
tweet-birikim-sureci-kotu-haber-akilli-para · sohbet: Wyckoff anlatısı, kural yok
tweet-bist-hft-colocation-quant-rekabet-kod-ogrenin · görüş
tweet-bollinger-macd-adx-adxr-panel-1761494383709290807 · grafik, koşul yok (iki görsel: Bollinger, MACD, ADX ve ADXR paneli, "20-day SMA" etiketi; Ham yalnız "#MIATK soran olmuştu"; görsel metni)
tweet-bollinger-orta-bant-rsi50-kesisim-1840463074622685613 · sohbet (kod paylaşımı: wetransfer sorunu, numpy sürümü) ve tarama çıktısı, kural öğesi yok (konu: B §39); PENGD görselinin kırpılmış kopyası, RSI satırı yok
tweet-cari-oran-likidite-acigi-bedelli-sermaye-artirimi · değerleme, kapsam dışı: TASARIM §3
tweet-cci-posc-macd-gosterge-seti-1761507718693548409 · grafik, koşul yok (THYAO; Ham yalnız etiket; iki gönderide sekiz gösterge grafiği: EMA5 üzerinden EMA5, CCI ve 20 günlük EMA, Price Oscillator (POSC), MACD ve sinyal, Ichimoku, 13 ve 60 günlük WMA, Stokastik %K/%D, Momentum ve 8 günlük MA; görsel metni). Çizim ayarlarıdır, giriş veya eşik yok (ilgili: B §34 kısa kayıtlarındaki çoklu gösterge seti, YORUM)
tweet-coklu-osilator-negatif-uyumsuzluk-2049565175494181237 · grafik, koşul yok (ISDMR; Ham: "Enteresan değil mi"). Görselde (açıldı) fiyat tepesinden yatay çizgi ve üç osilatör panelinde alçalan tepe çizgisi (çoklu negatif uyumsuzluk çizimi); osilatör adları, eşik ve sinyal tanımı yok
tweet-convex-hull-dea-sektor-rotasyonu-projesi · proje fikri
tweet-cufflinks-quantfig-macd-rsi-grafik-kodu-1860765789856379348 · eğitim ve araç tercihi: grafik kodu (cufflinks QuantFig ile XU100, 2022-2024; MACD 12/26/9 ve RSI(20) 70/30 çizim ayarı); giriş koşulu yok
tweet-divergence-macd-cross-1911093378961256668 · vaat ("Asla yanılmaz:))") ve tarama çıktısı, kural öğesi yok (konu: B §52); örnek kripto (MKR-USD), kripto kapsamı: karar Levent'te bekliyor
tweet-doji-mum-rsi-30-70-sinyal-1848385134174589367 · tarama çıktısı, kural öğesi yok (konu: B §50); üç sembol: BFREN Sat, CCOLA ve KAREL Al
tweet-doji-mum-rsi-30-70-tarama-1851724305836499212 · tarama çıktısı, kural öğesi yok (konu: B §50); tek sembol: SOKM Al
tweet-elliott-abc-fvg-algoritma-1989365905504256144 · örnek grafik, koşul yok (görsel: 1-2-3-A-B-C etiketi, sarı FVG kutusu, Matriks ekranı; Ham: "İşte böyle çalışıyor algoritma"; konu: C §17)
tweet-ema-5-13-21-kesisim-sinyal-1849524500439744798 · grafik, koşul yazılı değil: ARCLK için EMA5/13/21 kesişimi al (siyah ok) ve sat (turuncu) işareti; kod WeTransfer bağlantısında, notta yok; eğitim amaçlı davet
tweet-ema-dizilim-rsi-cmf-tarama-1847735111942336850 · sohbet ("otomasyona geçeceğiz"); görsel mum formasyonu işaretleme kodu parçası, koşul yok
tweet-ema-hizalama-rsi-50-tarama-1851721104156774497 · tarama çıktısı, kural öğesi yok (konu: B §56)
tweet-enflasyon-farki-pi-pi-yildiz-1907020125770772606 · makro gösterge tanımı (π − π* = yerli eksi yabancı enflasyon, örnek %13 ve %2 için ≈ 0,11); eşik ve kural yok, üst gönderi notta yok
tweet-envanter-azaltma-monte-carlo-pnl-1924523925683274094 · proje anlatısı: kavramsal Monte Carlo simülasyonu (5 envanter stratejisi, 100.000 senaryo, 3 piyasa koşulu); sayısal sonuç ve eşik yok, yalnız kavramsal ilke (yükselen trendde yavaş, düşen trendde hızlı sat)
tweet-evds-api-mevduat-faizi-cekme-1766868425815535946 · veri çekme kodu (EVDS API, seri TP.TRY.MT02: TL 3 aya kadar mevduat faizi) ve makro görüş (faiz, enflasyon); kural öğesi yok
tweet-excel-degerleme-calismasi-koda-donusumu · değerleme, kapsam dışı: TASARIM §3
tweet-fcfe-ddm-capraz-kontrol-degerleme-motoru · değerleme, kapsam dışı: TASARIM §3
tweet-fibo-144-bar-786-bandi-1842305345110302780 · tarama çıktısı, kural öğesi yok (konu: C §23); tek hisse (AKSA) grafiği; @fiboborsa'ya yanıt: "Python taramasından çıkan hisselerden biri"
tweet-fibo-786-bandi-tepki-teyit-gostergeleri-1847021977669628220 · tarama çıktısı, kural öğesi yok (konu: C §23); MACKO ve ULUUN için gösterge ekranı §23'teki ekranla aynı, eşik yok
tweet-fibonacci-78-6-tepki-taramasi-1843361242519617709 · tarama çıktısı, kural öğesi yok (konu: C §23); IHAAS için EMA 89/144/233 ekranı §23/§24'te var
tweet-fibonacci-786-bandi-tepki-tarama-1851718708936282217 · tarama çıktısı, kural öğesi yok (konu: C §23); 30.10.2024 tarama listesi, EUREN grafiği
tweet-fibonacci-786-ema-rsi-tarama-1847613665018630286 · tarama çıktısı, kural öğesi yok (konu: C §23); VKGYO grafiği, Telegram bot ('Tbot admin') ekran görüntüsü; tarama botla gönderiliyor
tweet-finansal-veri-api-kaynaklari-1762361028178796875 · araç tercihi: veri API listesi (Nasdaq Data-on-Demand, Alpha Vantage, Intrinio, IEX Cloud); BIST için kural öğesi yok
tweet-fiyat-grafigi-otesi-makro-bakis · haber: makro eğitim
tweet-fon-cikisi-satis-baskisi-tahmini-2099970636386812395 · proje fikri ve soru: fon çıkışının satış baskısını tahmin etme, geçmiş KAP raporlarıyla güven skoru; model, formül ve sonuç yok (konu: yeni fon çıkışı bölümü, E)
tweet-fon-net-akis-getiri-tarama-2094913511986020386 · tarama çıktısı, kural öğesi yok (fon sıralama tablosu: 1G/5G/20G net akış, 20G getiri, Sharpe sütunları; konu: fon-risk-radari)
tweet-fon-ortak-agirlik-degisimi-birikim-2096343856476496081 · vaat / proje fikri: fon ağırlık değişimi ve ortak hareket analizi duyurusu, ölçü ve eşik yok (konu: fon-risk-radari)
tweet-fon-para-akisi-analizi-2097019577112600707 · fon yorumu (KHP para piyasası fonu), eşik yok; kural öğesi yok (konu: fon-risk-radari)
tweet-froto-nakit-piyasa-degeri-18-89 · değerleme, kapsam dışı: TASARIM §3
tweet-gartley-harmonik-fibo-oran-1962604746000277528 · tarama çıktısı, kural öğesi yok (konu: C §7); görselde yalnız etiketler: XA 2.66, AB -1.72, BC 0.82, CD -1.04, Fibo 0.618 28.06, Fibo 0.786 27.88; Ham şaka, koşul yok. Hesap (bizim): AB/XA ≈ 0,65, BC/AB ≈ 0,48, CD/BC ≈ 1,27, yani §7 aralıklarıyla uyumlu bir örnek; fiyat çizgilerinin hangi bacaktan çekildiği belli değil
tweet-gordon-buyume-modeli-temettu-degerleme · değerleme, kapsam dışı: TASARIM §3
tweet-gun-saat-satis-heatmap-pivot-1764250055114899657 · dış kapsam: pazarlama satış analitiği (gün-saat ısı haritası, perakende verisi), BIST işlem kuralı yok
tweet-hareketli-ortalama-backtest-araci-1979931015771517315 · araç tercihi: harici hareketli ortalama backtest sitesi bağlantısı ("Kaydedin lazım olur"), kural öğesi yok
tweet-iq-csharp-python-veri-hatti-1964627639425270263 · araç tercihi: veri hattı (IQ verisi C# kodu ile çekilir, Python'da işlenir; API yok), kural öğesi yok
tweet-iq-excel-python-akd-verisi-1970561329590354082 · araç tercihi: veri alımı (IQ Excel eklentisi + Python; AKD verisi, yf yetmez), kural öğesi yok
tweet-is-yatirim-bilanco-veri-toplama-1942613749073879070 · eğitim: bilanço verisini İş Yatırım'dan otomatik toplayıp klasörde havuzlama önerisi; veri yöntemi, değerleme tarafı (kapsam dışı: TASARIM §3), kural öğesi yok
tweet-isyatirim-financial-data-source-1889446483449037295 · araç tercihi: İş Yatırım finansal verisi (class tipi kodla erişim), değerleme verisi (kapsam dışı: TASARIM §3), kural öğesi yok
tweet-kelebek-abcd-fib-uzanti-d-hedef-2092340608480297126 · tarama çıktısı, kural öğesi yok (konu: C §3): KRPLS D hedefleri 11.29 [TAMAM], 10.05 [TAMAM], 7.83 [BOZULDU] ve uzantı ızgarası (0.000 8.42 … 2.000 11.30) §3'ün KRPLS örnekleriyle aynı; G3'te X-B çizgili harmonik, D 11.20 [TAMAMLANDI] (konu: C §9 şablonu), G2'de kırılım etiketleri (Temas, RSI Kırılım); Ham: "Bu da serbest dusus" yorum
tweet-kmeans-silhouette-pca-kume-gorsellestirme-1762356653779763260 · eğitim: müşteri kümeleme (K-means, silhouette, PCA) kod örneği; ürün/kargo verisi, trade kuralı yok (havuz etiketi: dış kapsam)
tweet-nihai-hedef-tek-tus-temel-teknik-degerleme-llm-nlp · vaat: hedef beyanı
tweet-nispi-ppp-kur-enflasyon-testi-1907020119080935479 · makro, kur ve enflasyon farkı testi (nispi PPP), kural öğesi yok, kapsam dışı
tweet-optimal-momentum-plus-simulasyon-tamamlandi · vaat
tweet-ozkaynak-artisi-varlik-finansman-yatirim-verimliligi · değerleme, kapsam dışı: TASARIM §3
tweet-pandas-zaman-serisi-kod-kaliplari-2023876641689075990 · eğitim (pandas zaman serisi kod kalıpları tablosu)
tweet-pddd-roe-sektor-tarihsel-value-trap-filtresi · değerleme: Ham bir filtre verir (düşük PD/DD + yüksek ROE + sektör altı çarpan; 36 çeyrek çıpa); kapsam dışı: TASARIM §3
tweet-period-net-profit-capital-extract-1913605982594138565 · bilanço kalemi (net kâr, sermaye) çekme kodu, değerleme ve temel veri, kapsam dışı: TASARIM §3
tweet-pine-script-python-gorev-ayrimi-veri-backtest-icra · araç tercihi
tweet-python-ai-stratejik-yonetim-vizyon-misyon-kodlama · kurumsal proje, kapsam dışı
tweet-python-finans-verisi-ogrenme-yol-haritasi · eğitim
tweet-rasyo-kumeleme-mlp-hisse-secimi-2086819758138134758 · değerleme, kapsam dışı: TASARIM §3 (10 finansal rasyo ile kümeleme ve MLP süzme şeması; rasyo listesi ve eşik yok)
tweet-regresyon-ml-rasyolardan-piyasa-degeri-sapmasi · değerleme, kapsam dışı: TASARIM §3
tweet-relatif-degerleme-piyasa-norm-bantlari · değerleme, kapsam dışı: TASARIM §3
tweet-roc-nopat-yatirilan-sermaye-hesabi · değerleme, kapsam dışı: TASARIM §3
tweet-rsi-fibo-786-donus-1925626094935236883 · tarama çıktısı, kural öğesi yok (konu: C §34); ASTOR 22.05.2025, başlık "RSI Fibo 78.6 Dönüş & Mum Grafik", mum etiketleri CDLRICKSHAWMAN, CDLHARAMICROSS, CDLHARAMI; Ham: "Ne arasan var:)" ve "Bilgi amaçlıdır"
tweet-sirket-degerlendirme-sektor-isletme-finansal-degerleme-kontrol-listesi · değerleme, kapsam dışı: TASARIM §3
tweet-takas-virman-gercek-satis-ayrimi-1936386099225448628 · görüş: takas yorumu ilkesi (aracı kurumlar arası virman satış sayılmaz; birkaç gün veya hafta boyunca desen, hacim ve fiyat teyidi); eşik ve tarama koşulu yok; takas ve AKD verisi bedava günlük veride yok
tweet-telegram-bot-python-mesaj-1847042700467745116 · araç tercihi: Telegram bot ile algoritma çıktısı gönderme kodu; kural öğesi yok (TASARIM Telegram'ı "Yok" listesine koyar)
tweet-temel-filtre-sonra-teknik-tarama-1850990584338792873 · proje fikri: planlanan yeni nesil tarama, önce temel analiz ve fiyat değerlendirmesi süzgeci, sonra teknik tarama; eşik yok; değerleme, kapsam dışı: TASARIM §3
tweet-to-float-excel-finansal-tutar-donusum-1956812751902474403 · araç: Excel'den gelen tutar metnini sayıya çeviren Python işlevi; kural öğesi yok
tweet-toplu-akd-cekme-kumulatif-veri-1967190744399327388 · araç tercihi, veri kaynağı (AKD her gün toplu çekilir ve kümülatif toplanır; Matrix bireysele API vermiyor); kural öğesi yok
tweet-topsis-cok-kriterli-hisse-secimi-2015048294649545183 · görüş: çok kriterli sıralama yöntemi (TOPSIS), eşik yok; proje fikri ve kod satış planı; girdiler F/K, PD/DD gibi değerleme verisi: kapsam dışı: TASARIM §3
tweet-topsis-cok-kriterli-hisse-siralama-motoru · görüş: sıralama yöntemi, eşik yok
tweet-topsis-hisse-secimi-yaklasan-proje · proje fikri
tweet-ttrak-pddd-primi-carpan-sikismasi · değerleme, kapsam dışı: TASARIM §3
tweet-wbdata-dunya-bankasi-makro-veri-cekme-1860262968446824713 · araç ve veri: wbdata ile ABD toplam rezerv serisini çekip çizen Python kodu (makro veri); kural öğesi yok
tweet-yf-gecikme-gunluk-periyot-1849792794132435435 · araç tercihi, veri kaynağı: yfinance 15 dk gecikmeli, günlük veri tercihi, gecikme için en az 4 saatlik periyot önerisi (veri zamanlaması: E K30); işlem eşiği yok (Yahoo kullanılmaz: TASARIM §5.1)
tweet-yfinance-bist-is-uzantisi-1761496087221707093 · araç tercihi, veri çekme kodu: yfinance BIST .IS eki; kural öğesi yok
tweet-yfinance-close-auto-adjust-true-1892947326915739997 · araç tercihi, kütüphane sürüm uyarısı (yfinance auto_adjust=True, Adj Close yerine Close); kural öğesi yok
tweet-yfinance-haftalik-veri-cekme-1849540753816453297 · araç tercihi, veri çekme kodu (yfinance interval 1wk); kural öğesi yok
tweet-yfinance-multi-stock-merge-1897595128165929334 · araç tercihi, veri çekme kodu (iki hissenin Close serisini birleştirme); kural öğesi yok
tweet-yfinance-multiindex-droplevel-1893614943657755035 · araç tercihi, kütüphane düzeltmesi (MultiIndex droplevel); kural öğesi yok; tekrar: tweet-yfinance-close-auto-adjust-true-1892947326915739997
tweet-yfinance-multiindex-duzeltme-1893610096833200443 · araç tercihi, kütüphane düzeltmesi (MultiIndex); kural öğesi yok; kod hacmi 0 olan satırları atar (veri temizliği, eşik yok)
tweet-yfinance-opsiyon-zinciri-iv-open-interest-1909203207387037837 · kapsam dışı: TASARIM §3 (opsiyon); ABD örneği (AAPL zinciri), kural yok
tweet-yfinance-plotly-mum-grafigi-kodu-1983214789644976325 · araç tercihi, grafik kodu (Plotly mum grafiği, DOAS); kural öğesi yok
tweet-yfinance-veri-eksikligi-1846284880206086632 · araç tercihi, veri kaynağı uyarısı (yfinance son günler eksik olabilir); kural öğesi yok
tweet-yuksek-beta-martingale-1876964680947696067 · görüş: yüksek betalı hisse ile martingale iddiası; deneysel çalışma atfı kaynaksız; koşul, parametre ve sonuç yok

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
