# TEMA 5a — Ölçüm yöntemi, ilke, araç-öğrenme: defter öneri belgesi

Girdi: `tema-5a.jsonl` (248 satır: genisletir 81, yeni 64, cesitlendirir 89, celisir 14). Defter: `defter-fikir.txt` ve `../../../defter-1..4.md`.

Okuma notları:

- `tema-5a.jsonl` içinde "DEFTER OKUMA HATASI" satırı yok (0 eşleşme).
- `defter-1..4.md` bu klasörde değil. Dosyalar `docs/strateji-taslak/` kökünde.
- Defter başlıklarındaki tarih kayıt anıdır (2026-08-27/28). Kaydın özgün paylaşım tarihi defterde yok. Bu belgede "defter tarihi" bu kayıt anını gösterir.
- "Görsel doğrulandı" ifadesi, görseli bu belge için Read ile açtığımı gösterir.
- Kaynak sütunundaki tarih, gönderinin tarihidir.

---

## 1. Yeni yöntem aileleri

Bu bölüm, defterde adı ya da amacı olmayan yöntemleri ve adı defterde olmayan türevleri toplar. Defterde adı olup yalnız "fikir" düzeyinde kalan GARCH (R097) ve Merton/DtD (R061) Bölüm 2'dedir.

Olgunluk: **tam** = formül ve parametre birlikte var; **çekirdek** = mantık var, eşik ya da pencere eksik; **fikir** = yalnız ad ya da öneri.

### 1.1 Fon riski ailesi (hisse senedi fonu likidite, akış, maruziyet)

Tansu'nun kendi aracı. Gönderiler 2026-09-04 ile 2026-09-20 arasında. Ailede en çok tekrar eden konu budur (23 satır).

Tansu'nun vurgusu: "En önemli erken uyarı, fon fiyatında ilk kırmızı gün değil güçlü para girişlerinin belirgin şekilde yavaşlaması ve ardından kalıcı para çıkışına dönüşmesidir." (2095931263593095368). Ayrıca 2100513708170428797 (2026-09-17): "5 Eylülde Yusuf Beye verdiğim cevabı ciddiye dahi almadı." Bu cümle, 2096243590133407910'daki stres testinin sonradan doğrulandığını savunur.

#### 1.1a Likidasyon süresi ve marketability stresi — olgunluk: tam

| Türev | Ne yapar | Parametreler (birebir) | Kaynak (id, tarih) |
|---|---|---|---|
| Days-to-liquidate stres testi | Fon çıkışında pozisyonun kaç günde satılacağını hesaplar | gün = (çıkış TL × ağırlık) / (0,20 × 20G medyan TL hacim); senaryo %10 çıkış; katılım %20; TRHOL 546,87 Mn / (0,20 × 378,78 Mn) = 7,22 gün KRİTİK; BIGEN 4,1, ANELE 3,9, KARCL 3,3 gün; TERA ağırlık %8,63 ama 1,6 gün | 2095983340142882886 (2026-09-04) |
| Teorik tasfiye süresi | Pozisyonu 20G medyan TL hacme böler | pozisyon / 20G medyan TL hacim; katılım oranları yazılı değil; sonraki katman spread, order-book depth, ±%2 aralıktaki toplam alış/satış (üst gönderide saat 11); stres ve taban günlerinde geçmiş hacim yanıltıcı | 2096187367778370014 (2026-09-05) |
| Marketability stres testi | Stres altında satılabilirliği ölçer | stresli gün = normal gün (%20 katılım) / kullanılabilir hacim katsayısı; BIGEN 11,12 / 0,05 = 222,40; TKNKA 5,94 / 0,55 = 10,80; girdiler: taban benzeri 10G sayısı, ardışık taban, 5G/20G hacim oranı (BIGEN 0,14); skor 100 KRİTİK; katsayı ve skor formülü yazılı değil | 2097031747347030189 (2026-09-07) |
| Fon stres testi (itfa senaryosu) | Fonun %5/%10 itfayı nakit ve likit varlıkla karşılayıp karşılamadığını sınar | girdiler: 5 ve 20 günlük para akışı, AUM zirveden düşüş, likit tampon, portföy konsantrasyonu, büyük pozisyon / medyan işlem hacmi; itfa %5 veya %10; "PSR %99 üstü alfa kanıtı değildir"; eşik yok | 2096243590133407910 (2026-09-05); 2096278310611218490 (2026-09-05); 2100513708170428797 (2026-09-17) |
| Tam tasfiye tablosu (TLY) | %20 katılımla tam tasfiye günü | OZATD 320, TRHOL 158, TEHOL 89, ANELE 72 gün | 2099919520844382444 (2026-09-15) |

Görsel doğrulaması (2095983340142882886-1.png, -2.png): TRHOL satırı 6,54 ağırlık, 20G medyan ₺378,78 Mn, %10 çıkış ₺546,87 Mn, %10 çıkış gün %20 = 7,22. Formül görseldeki değerle tutar. Tablo ayrıca %10/%20/%30 katılımla tam likidasyon gününü verir (TRHOL 129,15 / 64,58 / 43,05). Likidite sınıfı "Pozisyon / Medyan Hacim" oranıyla sıralanır: 2,67 ve üstü KRİTİK, 1,23–1,51 YÜKSEK, 0,41–0,97 ORTA, 0,37 ve altı DÜŞÜK. Bu sınırlar görseldeki satırlardan çıkarımdır; eşik yazılı değildir.

#### 1.1b Akış erken uyarı ve skorlar — olgunluk: çekirdek

| Türev | Ne yapar | Parametreler (birebir) | Kaynak (id, tarih) |
|---|---|---|---|
| Erken uyarı zinciri | Fon kaynaklı satış baskısını sırayla izler | "5 günlük para akışı negatife döner → 20 günlük akış zayıflar → AUM zirveden geriler → yüksek ağırlıklı ve düşük likiditeli hisselerde risk artar"; erken birikim adayları PEKGY, DSTKF; DOH: en büyük %21,1, ilk 5 %45,6 | 2099132513708851639 (2026-09-13); 2099138697182507037 (2026-09-13) |
| Erken Uyarı Skoru | Yapısal Risk ve Aktivasyonu birleştirir | Yapısal: fon ağırlığı, likidite, kriz satılabilirliği; Aktivasyon: 5 ve 20G akış, AUM zirveden gerileme, KAP pozisyon değişimi, fiyat-hacim; THF 5G ₺44,63 Mr (%31,5 AUM), 20G ₺120,83 Mr (%85,3 AUM); birleştirme formülü ve renk eşikleri yok | 2099594176606187548 (2026-09-14); 2099919520844382444 (2026-09-15) |
| Fon Stres Skoru | Fonu rejime yerleştirir | bileşenler: para çıkışı + yüksek hisse oranı, repo/borçlanma, likit tampon erimesi, fon içi fon, valör uyumsuzluğu, Days to Liquidate, VİOP, look-through; rejimler NORMAL, GERİLİYOR, FİNANSMAN STRESİ, ZORUNLU SATIŞ RİSKİ, KRİTİK; rejim eşikleri yok | 2097983494991339894 (2026-09-10) |
| Flow velocity / acceleration | Akışın hızını ve ivmesini ölçer | velocity = günlük akış / AUM (%) ortalaması, 5G ve 20G; TLY 5G %1,15 < 20G %1,37, ivme pozitif; acceleration formülü yok | 2099959209467211874 (2026-09-15) |
| Risk okuma listesi ve çerçeve | Beş göstergeyi birlikte okur | para akışı, AUM değişimi, yoğunlaşma, likidasyon süresi, marketability stress; ilk 5/10 hisse ağırlığı; KAP aylık portföy + TEFAS; Sharpe, Sortino, volatilite, MaxDD, Calmar; eşik yok | 2097548996193526092 (2026-09-09); 2097393379243962378 (2026-09-08); 2095931263593095368 (2026-09-04) |

Görsel çıkarımı (2099594176606187548-1.png): Erken Uyarı Skoru çizgisi, Yapısal Risk ile Aktivasyonun ağırlıklı toplamına uyar. Yaklaşık değerler: ANELE 88,6 / 12,5 → 43; SELEC 79,7 / 9 → 37,3; DSTKF 27 / 0 → 10,8. Bu üç nokta skor ≈ 0,4 × Yapısal + 0,6 × Aktivasyon ilişkisine uyar. Çarpım ilişkisine uymaz. Satırdaki yöntem adı "Yapısal Risk × Aktivasyon" der. Gönderide formül yok. Ağırlıklar belirsizdir; Tansu'ya sorulmalıdır.

#### 1.1c Net maruziyet, katkı ve diğer fon ölçüleri — olgunluk: çekirdek

| Türev | Ne yapar | Parametreler (birebir) | Kaynak (id, tarih) |
|---|---|---|---|
| Net hisse maruziyeti | Brüt hisse oranından VİOP short'u düşer, beta ile ayarlar | THF brüt ~%88 → net ~%65 → beta ayarlı ~%38; başka bir tarih: net %64,47 = %77,82 − %13,35, beta ayarlı %40,15; beta ayar formülü yok; LONG VİOP net maruziyeti düşürmez (DOH net = brüt %69,13) | 2096700133731643859 (2026-09-06); 2097395059641679900 (2026-09-08); 2097031747347030189 (2026-09-07); 2099594176606187548 |
| Getiri katkı motoru | Günlük fon getirisini hisse ve VİOP katkısına ayırır | katkı = tahmini ağırlık × günlük getiri (ANELE %4,70 × 5,29% = 0,249%); +1,05% + (−0,33%) = +0,73%; reconciliation katsayısı 0,8648 (tanımı yok); açıklanan +0,80; KARCL %6,62 × +7,37% = +0,488% | 2097064583185715412 (2026-09-07); 2099944754511278524 (2026-09-15) |
| KAP ağırlık değişimi okuması | İki rapor arası ağırlık farkı + akış | TMV: BIGEN +9,97, SELEC +6,42, ANELE +5,65, TEHOL −8,41 puan; "doğrudan 'şu kadar hisse aldı/sattı' diye okumamak gerekir" | 2097427778232529261 (2026-09-08) |
| Fon sınıfı akış ve AUM/fiyat farkı | Yeni parayı fiyat etkisinden ayırır | PPF −401,5 Mr, HSF +98,1 Mr, serbest +194,8 Mr; "fon fiyatı yüzde 10 yükselirken fon büyüklüğü yüzde 30-40 artıyorsa" fark yeni paradır | 2099908239471116731 (2026-09-15) |
| Tek gün çıkış ve ters repo | Tek gün çıkışı AUM'a oranlar, karşı tarafı izler | TP2 16,27 Mr / ~259 Mr ≈ %6,3; portföy %67 ters repo; valör kuralı: "13.30 öncesi ise t+1" | 2099913462034088091 (2026-09-15); 2100938761227923617 (2026-09-18) |

### 1.2 Durağanlık testleri — olgunluk: çekirdek (karar kuralı tam, lag ve pencere yok)

Tek dizi, 2025-03-26. Defterde durağanlık testi adı yok.

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Görsel kontrol | hareketli ortalama ve hareketli std zamanla sabitse durağan; pencere yok | 1904748983735455775; 1904748990458900518 |
| Birinci fark | `data['Döviz_Kuru'].diff().dropna()`; fark sonrası test şart | 1904748986738651154; 1904749005990510772 |
| ADF | p < 0.05 → durağan; istatistik kritik değerden küçük (daha negatif) → durağan | 1904748993797632344; 1904748996893053368 |
| ADF başarısız | p > 0.05 → ikinci fark gibi ek dönüşüm | 1904748999908692189 |
| KPSS | ADF yanında çapraz kontrol | 1904749002748281042 |

Tekrar: ADF, 2099952521221661048'de (2026-09-15) Granger öncesi kullanılır (Bölüm 1.3).

### 1.3 Granger nedensellik ve gecikmeli korelasyon — olgunluk: tam

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Granger kullanım çerçevesi | önce ADF, gerekirse fark; lag AIC/BIC ile; gözlem aylık 5 yıl, günlük birkaç ay; örnek makro→BIST100, TUPRS→PETKM; "sonuç nedensellik değil tahmin gücü"; anlamlılık eşiği yok | 1922963356362703307 (2025-05-15) |
| Sıra | "Korelasyon → Gecikmeli Korelasyon → Granger Nedensellik" | 2099751961159454867 (2026-09-15) |
| THF akış–getiri sonucu | günlük getiri ve normalize akış (% AUM); eş anlı Pearson 0,12, Spearman 0,07; getiri→akış lag2 Pearson 0,245 / Spearman 0,353; Granger getiri→akış lag 2–5 FDR p ≈ 0,0012; akış→getiri FDR sonrası anlamsız; sonraki pencereler 20, 60, 120 gün ve tüm tarih | 2099952521221661048 (2026-09-15) |
| Alıntı | aynı sonuç, ilke: "getirinin kaynağına ve sürdürülebilirliğine bakmak gerekir" | 2101627771524927545 (2026-09-20) |

Görsel doğrulandı (2099952521221661048-1.png). Lag 1–5 tablosu, ADF tablosu (getiri −7,674, p 0,0050; akış −3,085, p 0,0300; kritik %5 −2,86) ve Granger tablosu satırla tutar. Görselde iki uyarı var:

- ADF notu: "NumPy ADF fallback | p yaklaşık; karar %5 kritik değere göre."
- Granger yöntemi: "NUMPY OLS FALLBACK". p değerleri yaklaşıktır.
- Akış→Getiri lag 1'de ham p 0,0188, FDR p 0,0547 (anlamsız). FDR düzeltmesi sonucu değiştirir.
- Gözlem 305–309.

### 1.4 Faktör modelleri — olgunluk: çekirdek (pencere ve regresyon tanımı yok)

Defterde yalnız piyasa betası (R200: β = Kov/Var) var. Gönderiler betayı makro faktörlere taşır. 2025-01 ile 2025-07 arasında 15 satırda tekrar eder.

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| USD/TRY faktör betası | BIST30: ISCTR ≈ −1.21, HALKB ≈ −1.09, AKBNK ≈ −1.06 … FROTO ≈ 0.50; getiri değişimi = beta × USD/TRY değişimi (THYAO 1.5 → %1.5, varsayımsal) | 1878182162945495259; 1878182165176795195; 1878182172818804853 (2025-01-11) |
| Altı faktörlü beta | USDTRY, EURUSD, BRENT, SPX, DAX, US_10Y; hisse başına ayrı beta | 1878209442790998442 (2025-01-11); 1919250826435965149 (2025-05-05); 1943070389388873813, 1943070394308792479 (2025-07-09) |
| Faktör betası tanımı | "bir varlığın … belirli bir risk faktörüne karşı duyarlılığını ölçen bir katsayı"; THYAO'yu en çok USD kuru etkiler | 1893286879052648887 (2025-02-22); 1888872602493448198, 1888872604653482082 (2025-02-10) |
| Fama-French | piyasa faktörü + SMB (küçük − büyük) + HML (yüksek − düşük defter değeri); ek MOM, likidite, faiz, makro; denklem yok | 1893286881917366600; 1893286885021085822; 1893286887827116496 (2025-02-22) |
| CDS ve hacim regresyonları | XBANK günlük getiri ~ CDS değişimi (baz puan), kontrol Dolar/TL ve tahvil faizi, GARCH, PCA faktör; hacim ~ beta, fiyat, piyasa getirisi, volatilite, haber | 1939757379349872937 (2025-06-30); 1941169284698587472 (2025-07-04) |

### 1.5 Yön sınıflandırma ve makine öğrenmesi — olgunluk: çekirdek/fikir

Lojistik regresyon defterde var (R234); Bölüm 2'dedir. HMM ve random forest Bölüm 3'tedir.

| Türev | Parametreler (birebir) | Kaynak | Olgunluk |
|---|---|---|---|
| KNN yön sınıflaması | hedef ertesi gün +1/−1; doğruluk %75; değişkenler open, high, low, adj close; Öklid uzaklığı; k yok; veri son 10 yıl | 1859240563205107928 (2024-11-20); 1861901396506743020 (2024-11-27); 1862021493363786215 (2024-11-28); 1864342754844660140 (2024-12-04); 1864017629444186615 (2024-12-03) | çekirdek |
| PRED tabanlı backtest | `return2 = return * return_sign`, kümülatif toplam; pozisyon kuralı görünmüyor | 1874198139688935767 (2024-12-31) | çekirdek |
| Confusion matrix ve LSMA | TP, FP (Tip 1), FN (Tip 2), TN; LSMA %69 win rate, TUPRS ertesi gün 156.45, periyot yok | 1851753105047552410 (2024-10-30); 1844097728105836649 (2024-10-09) | fikir |
| PPO (pekiştirmeli öğrenme) | PPO al/bekle/sat politikası öğrenir; tahmin modülü ayrı tutulur | 1912527539655811203 (2025-04-16) | fikir |
| PSO ve NN volatilite | PSO önerisi, parametre yok; realized vol 2010–2021 eğitim, NN tahmini, ağ yapısı yok | 1825298362775826730 (2024-08-18); 2023873325991424381 (2026-02-17) | fikir |

### 1.6 Regresyon tanılama ve istatistik sınama — olgunluk: çekirdek/fikir

| Türev | Parametreler (birebir) | Kaynak | Olgunluk |
|---|---|---|---|
| Ridge, Lasso, polinom | Lasso alpha 10^-4–10^4, optimal ≈10^-2 (RMSE en düşük, keskin artıştan önce); Ridge ve polinom parametresiz; "polinomial regresyon trendi. çok severim" | 1825277249374867614 (2024-08-18); 1825488501254578373 (2024-08-19); 1843972937059295526 (2024-10-09) | çekirdek |
| Durbin-Watson | kesitsel çoklu regresyonda otokorelasyon model hatası; sınır değeri yok | 1950584440805081552 (2025-07-30) | fikir |
| Fisher z | yıllık korelasyonlar z'ye çevrilir, ortalamanın sıfırdan farkı test edilir; "Uzun vadeli ilişki arıyor iseniz direk cointegration bakın" | 1956102757468770306 (2025-08-14) | çekirdek |
| Koşullu rastlantı testi | bir seriyi aynı volatilite dağılımını koruyarak karıştır, çok kez tekrarla; gerçek korelasyon dağılımın ucundaysa anlamlı; tekrar sayısı ve eşik yok | 1955986393622306882 (2025-08-14) | çekirdek |
| AB testi ve √n kuralı | iki benzer hisseye eşit küçük tutar, süre yok; 10 kat veri → belirsizlik 1/√10 ≈ 0,32 | 1958791121686904877 (2025-08-22); 2089154878794764480 (2026-08-17) | fikir |

### 1.7 Zaman serisi ve döngü — olgunluk: çekirdek/fikir

| Türev | Parametreler (birebir) | Kaynak | Olgunluk |
|---|---|---|---|
| Holt-Winters | ARIMA yerine mevsimsel üstel düzeltme; parametre yok | 1779094045844750602 (2024-04-13) | fikir |
| SARIMAX / auto ARIMA stepwise | AIC en küçük; m=12, D=1; en düşük ARIMA(2,0,1)(2,1,0)[12] AIC=4346.705 (liste kesik) | 2019525738207060400 (2026-02-05) | çekirdek |
| Fourier + Wavelet | "İlk keşif için Fourier …, sonra Wavelet ile o periyotların zamanla nasıl değiştiğine bakılır" | 1978893346727956651 (2025-10-16) | fikir |
| Markov geçiş matrisi | RSI'nın 0.786 Fibo seviyesini yukarı kırması sonrası devam olasılığı; sayı yok; vurgu: "Siz beni dinleyin, düşeni kıran bu işin temelidir." | 1950612726146842846 (2025-07-30) | fikir |
| EWMA Z-Score ve rolling max | getirinin EWMA ortalaması ±2σ (AGYO, katsayı yok); rolling maximum, pencere yok | 1937605928653640084 (2025-06-24); 1784817550561284226 (2024-04-29) | fikir |

### 1.8 Performans oranları — olgunluk: çekirdek

Defterde Sharpe ve max Sharpe var. Treynor, Jensen, M2, IR ve profit factor yok.

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Formül seti | Treynor = (getiri − rf)/beta; Jensen alfa = getiri − CAPM beklenen; M2 = rf + Sharpe × piyasa vol.; IR = (getiri − benchmark)/tracking error; Sortino = (getiri − rf)/downside deviation; tek fonda Sharpe/M2/Sortino, çeşitlendirilmişte Treynor/alfa | 1980319432141308317 (2025-10-20) |
| Oran seçimi | dört orandan risk algısına göre 2'si; orta vade 3 ay–1 yıl; rolling her 30 günde | 1951196059939569688 (2025-08-01); 1953401516565340457 (2025-08-07) |
| Information ratio | "yüksek alpha düşük information ratio güzeldir" (formül yok); IR yönetici becerisidir | 1773320333249896719; 1773329683167211531 (2024-03-28) |
| Profit factor | 1,68; win rate %80 | 1875902835780677930 (2025-01-05) |
| Rolling Sharpe (21 gün) | −0.4 seviyesi (sarı), etiketsiz kırmızı çizgi; kural yok | 1910417850684367263 (2025-04-10) |

Not: 1773320333249896719 "düşük information ratio" tercih eder. 1980319432141308317 IR'yi aktif getiri/tracking error olarak tanımlar; bu tanımda yüksek IR iyidir. İki ifade tutarsızdır; Bölüm 4'e bakın.

### 1.9 Teknik gösterge türevleri (adı defterde olmayan) — olgunluk karışık

#### 1.9a Tam parametreli türevler

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Ichimoku | Tenkan = (maxH9+minL9)/2; Kijun = (maxH26+minL26)/2; Span A = ((Tenkan+Kijun)/2).shift(26); Span B = ((maxH52+minL52)/2).shift(26); Chikou = Close.shift(−26); parametre optimizasyonu sorusu | 1760937885190996368 (2024-02-23); 1840046005787504758 (2024-09-28) |
| EMA5 / EMA10(EMA5) + CCI | al: ema1 > ema2 ve önceki bar ema1 <= ema2; CCI = (TP − SMA20(TP)) / (0.015 × ortalama sapma 20), CCI EMA20, ±100 | 1760742464309350866; 1760725146959270113 (2024-02-22) |
| Vegas tüneli | EMA 12/144/169 + RSI(14) ve 50 çizgisi | 1827737743683707129 (2024-08-25); 1783160562156716179 (2024-04-24) |
| MOST ve HO / CCI üstüne MOST | THYAO 500 bar OPT1 15, OPT2 3, OPT3 11, OPT4 1, OPT5 5, OPT6 0,5, getiri %468,01; DOAS 60 dk OPT1 52, OPT2 3, %34,67 | 1779521360609354088 (2024-04-14); 1782789450767962601 (2024-04-23) |
| Üç ardışık düşüş mumu | son 3 mumda open − close > body ve 3 kapanış art arda düşüş → i+1'de sell = −1 (body değeri görünmüyor) | 1905475655686353161 (2025-03-28) |

#### 1.9b Çekirdek ve fikir türevler

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| RoC | RoC 9/20/50; ROC20 ve 0 ekseni geçişi; EMA5/13 | 1841215497481666930 (2024-10-01); 1842233841034883242 (2024-10-04) |
| Repaint-free tepe/dip | tepe, fiyat yeterince ters hareket edince onaylanır; `update()` yalnız geçmişe ilerler; eşik yok | 1908628358008889494 (2025-04-05); 1908945733903892945 (2025-04-06) |
| ADX + ADXR, 3 PSAR, Double Top | ADXR parametresiz; üç SAR serisi parametresiz; Double Top H = 2.99 (3.93%), W = 29 bars | 1761664509876265367 (2024-02-25); 1951730032168317197 (2025-08-02); 1953795273248973235 (2025-08-08) |
| Alexander filtresi, golden cross optimizasyonu | Alexander filtresi KFEIN al-tutu geçemedi, filtre yüzdesi yok; 50/200 yerine optimize MA çifti | 1775296855494078885; 1775296857473737047 (2024-04-02); 2071142623520215512 (2026-06-28) |
| Kontrarian ve grafik ölçeği | aracı kurum önerisi ters indikatör; kısa vade lineer, uzun vade logaritmik: "Arkadaşlar lineer bakın grafiklere logaritmik bakmayın." | 1918326021629108312 (2025-05-02); 1984620734136602784; 1984653261765558427 (2025-11-01) |

### 1.10 Opsiyon ve türev fiyatlama (strateji tarafı) — olgunluk: çekirdek

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Black-Scholes + Monte Carlo GBM | d1 = (ln(S/K) + (r − q + σ²/2)T)/(σ√T); call = S·e^(−qT)·N(d1) − K·e^(−rT)·N(d2); MC N=100000; BS 3.7452 / MC 3.7986; S, K, T, r, q, σ görünmüyor; kod hatası Bölüm 4'te | 1979645829377057243 (2025-10-18) |
| Greek'ler | alım theta −5,033; satım theta −5,64; vega 4,54; alım rho 1,39; satım rho −0,082; girdi yok; vega üs hatası Bölüm 4'te | 1942718595714396552 (2025-07-08) |
| P ve Q ölçümü | Q altında beklenen getiri = risksiz faiz; f_Q(x) = ξ(x)·f_P(x); ξ formülü yok | 1911126822588154108; 1911126825217982630 (2025-04-12) |
| Max OI strike + IV | en yüksek OI strike 205$ fiyatın gideceği seviye; IV 25.68%; ATM IV %28,0 vs 30 gün HV | 1936838035485983031 (2025-06-22) |
| Stoikov / difüzyon modelleri | "Etliye sütlüye karışmadan alım satımdan para kazanma yolları var"; parametre yok | 1867862826204942394 (2024-12-14) |

### 1.11 Piyasa mikro yapısı ve pozisyon verisi — olgunluk: çekirdek/fikir

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Emir defteri şekil fit | histogram fit mu ≈ 0.15–0.20, v₀ = 6.51; Dirac modeli q = 0.68 | 1911700859420889185 (2025-04-14) |
| Envanter azaltma MC | 10.000 hisse; 5 profil (lineer, hızlı/yavaş lineer, hızlı/yavaş kuadratik); 100.000 senaryo; piyasa etkisi β; yukarı trendde yavaş satış, aşağı trendde erken satış | 1924523925683274094 (2025-05-19) |
| Pozisyonlanma | yatırımcı tipine göre alım-satım kırılımı; eşik yok | 1917373384280924312 (2025-04-30) |
| AKD toplu çekim ve okuma | her gün toplu çek, kümülatif yap; kümülatif + parçalı + son gün birlikte | 1967190744399327388 (2025-09-14); 1964624298250731611 (2025-09-07) |
| Gün bazında mevsimsellik | ayın her günü için yıllar arası ortalama getiri (2010–2025) | 1911360294384816565 (2025-04-13) |

### 1.12 Portföy kurma türevleri — olgunluk: fikir

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Black-Litterman + moving window | "markowitz ya da daha iyisi black litterman modeli"; en eski veri çıkar, en yeni girer; pencere yok | 1797263552606061016 (2024-06-02) |
| Risk parity | Markowitz ile karşılaştırma; parametre yok | 1852647216193626153 (2024-11-02) |

### 1.13 Kur ve parite modelleri (R052 kurumsal kur çalışmasının çeşitlenmesi) — olgunluk: çekirdek

Hisse stratejisi değildir. R052'deki Monte Carlo kur tahminine alternatif sunar.

| Türev | Parametreler (birebir) | Kaynak |
|---|---|---|
| Pariteler (PPP, Fisher, UIP, forward) | PPP Δs = π − π*; Fisher i − i* = E(π − π*); forward p = i − i*; örnek enf. %8/%3, faiz %10/%4 → fark %5, %6; denklik |i − i* − p| < 1e-6 | 1906617978633789949; 1906617981221700057; 1906617984665137406; 1906617992508584357; 1906617994656039300 (2025-03-31) |
| Parite kodu ve özet | `ExchangeRateParity` sınıfı; Enflasyon Farkı 5.00%, Faiz Farkı 6.00%, Forward Prim 6.00% | 1906617998963535982; 1906618004739072494 (2025-03-31) |
| CIP regresyonu ve nispi PPP | (f − s) = α + β(i − i*) + ε; nispi PPP 2021–2030 serisi; TR %13 / ABD %2 → 0.11 | 1906621697274323162 (2025-03-31); 1907020119080935479; 1907020122851569733; 1907020125770772606; 1907020130984264014 (2025-04-01) |
| Psi ağırlıklı beklenti modeli (a) | s_t^n = (1 − psi)·Σ psi^i·E_t(x_{t+i}); beklentiler [39, 40.5, 42, 43, 44], psi 0.60 → 37.36416 | 1904911424641450458; 1904909627801624887 (2025-03-26) |
| Psi ağırlıklı beklenti modeli (b) | psi 0.60–0.80 yüksek frekanslı veride; Calvo fiyatlamada kullanılır; psi seçimi amaca bağlı | 1904911436888916240; 1904911426780622906; 1904909630540489156; 1904911430878363767; 1904911428877762622 (2025-03-26) |

### 1.14 Ders ve eğitim içeriği (strateji değil)

| Konu | Parametreler (birebir) | Kaynak |
|---|---|---|
| Black-Scholes dersi | S=100, X=80, T=1, r=0,05, q=0, σ=0,2 → put 0,6872; X=100, S 50–149 call/put eğrisi | 1897926526496035063; 1897926542044389854; 1897926545328501123; 1897926549338214614 (2025-03-07) |
| Binom ağacı (CRR) dersi (a) | u = exp(σ√dt), d = 1/u, q = (exp(r·dt) − d)/(u − d), dt = T/M; S0=100, strike=100, T=1, r=0,05, σ=0,2, M=3 → 11,0439 | 1905916780465307673; 1905916768196890659; 1905916770944266411 (2025-03-29) |
| Binom ağacı dersi (b) | düğümler 100; 112,24/89,09; 125,98/100/79,38; 141,40/112,24/89,09/70,72; içsel değer S − 100 | 1905916785615884772; 1905916773540528131; 1905916775931208060 (2025-03-29) |
| Ekonomi alıştırmaları | Qd = 100 − 2P, Qs = 50 + 3P → P* = 10, Q* = 80; MR = MC, Q = 10 | 1906972824842965372; 1906995019594056009 (2025-04-01) |
| Öğrenme sırası ve rutini | SMA → 2 SMA kesişimi → EMA → 2 EMA, 3 EMA → MACD → MACD+RSI; her 10 günde mini proje, 3–6 ay; kümülatif % = 100 × (fiyat − ilk)/ilk | 1861803141479457118 (2024-11-27); 1922994519655538765 (2025-05-15); 1826114680508867029 (2024-08-21) |

---

## 2. Genişletmeler (R kaydı başına)

Biçim: **R0xx**: defterde ne var → X gönderileri ne ekliyor.

### 2.1 Risk ve istatistik ölçüleri

- **R097** (GARCH): defterde "garch ve standart sapma kullanarak … örnek ile göstereceğim" — yalnız fikir. → 1899583516670611844 (2025-03-11): sabit ortalama GARCH(1,1), Student t, log getiri, 545 gözlem; omega 0.2951, alpha 0.1494, beta 0.7625, mu 0.1473, nu 15.38. 1952739571466211673 (2025-08-05): model seçimi "Daha düşük AIC/BIC → Daha iyi model", yüksek log-likelihood, standartlaştırılmış artıklarda Ljung-Box, EGARCH asimetri, "GARCH(1,1) çoğu zaman yeterli". Görsel doğrulandı: AIC 2172.34, BIC 2193.84. Uyarı: görselde omega p 0.414, alpha p 0.301; yalnız beta anlamlı (p 1.004e-03). Satırdaki "alpha+beta ≈ 0.912: kalıcı volatilite" yorumu anlamsız alpha'ya dayanır.
- **R061** (Merton): defterde girdi seti (A0 100, σA %25, D 80, r %5, T 1) ve çıktı DD 0.97, EDF %17; formül ve eşik yok. → 1852070155779739853 (2024-10-31): dtd = (ln(V/D) + (r + 0,5σ²)T)/(σ√T); V = piyasa değeri + borç; σ = günlük getiri std × √252; dtd > 1 düşük, < 1 yüksek risk; DOAS D = 300 milyon, r = 0,25, T = 1 → 1.7867. 1907840099489874309 (2025-04-03): DD > 2 çok güvenli, ≈1–1.5 orta, < 1 risk artıyor (1.5–2 tanımsız). 1907840096851624360: EDF = P(A_T ≤ DPT) = N(−DD), DD 1.3056σ → EDF %9.58. 1888561706638405699, 1888561708865589736 (2025-02-09): PD 0.00–0.20 düşük, 0.21–0.50 orta, 0.51–1.00 yüksek. Görseller doğrulandı. Kod hatası Bölüm 4'te.
- **R053** (Bollinger, VaR): defterde ±2 SD, %95, pencere yok. → 1850460386371281374, 1850468058747326871 (2024-10-27): orta = SMA(kapanış, 20), üst/alt = SMA ± 2 × örnek std(20). 1916228528850272645 (2025-04-26): VaR ufku 1 gün, %95; hesap yöntemi yok. 1822922559236555075 (2024-08-12): günlük getiri KDE, örnek vol BIMAS 0,0191, EKGYO 0,0255, GUBRF 0,0299.
- **R033** (IQR): defterde IQR k=1,5 ve |30g getiri| > %50. → 1822549636013240372 (2024-08-11): IQR = P75 − P25 günlük getiriye, 2014-07-30–2024-07-30, boxplot. 1823485106893300074: tek yılın uç getirisi aylık ortalamayı bozar.
- **R185** (Risk of Ruin, tahmin karşıtlığı): defterde "Monte Carlo … Risk of Ruin" yalnız fikir. → 1874240306461512014 (2024-12-31): p=0,49 → x2 olasılığı %1,80; p=0,51 → %98; formül P = 1/(1+(q/p)^N), N≈100 (satır bu formülü sonuçtan türetmiş; gönderide yazılı değil). 1874238154355728692: %1.83. 1977458197158932959 (2025-10-12): UsualDrunk/ColdDrunk/EWDrunk, 10–100000 adım, 100 deneme, uzaklık ∝ √adım.

### 2.2 Performans ve getiri ölçüleri

- **R137 / R115 / R251** (Sharpe, Sortino): defterde Max Sharpe ve "Sharpe aynı" kıyası; formül yok. → 2099366035111493673 (2026-09-14): `annual_return = returns.mean() * 252`; `annual_vol = returns.std() * (252 ** 0.5)`; `sharpe = (annual_return - rf) / annual_vol`. 1878164936150360461 (2025-01-11): Sortino = (yıllık getiri − rf) / aşağı yön std; GARAN 0.858181 / 0.49284 / 0.317296 → Sharpe 0.932111, Sortino 1.4478 (görsel doğrulandı; rf ≈ 0,3988 hesaptan tutar). 1940482821056835778: A (20−10)/10 = 1.00, B (30−10)/25 = 0.80; rf TR için 1 yıllık tahvil. 1913512010253205811: −0.40 ve −0.60'tan dönüş. 1908884987643846859: yıllık Sharpe < 1 kötü.
- **R137 / R115** (devam): 1949243802948149440 (2025-07-26): risksiz faizsiz Sharpe. 2099453056337203495 (2026-09-14): "getiri mevduatı aşamıyorsa … Sharpe negatif". 1764308361485459914 (2024-03-03): öncelik paranın korunması. 1914033217968996791 (2025-04-20): alfa aynı beta düzeyinde, Sharpe farklı risk düzeyinde kıyas. 1878173923646349656: std 2022-01-01 → 2025-01-10.
- **R137** (CMF): defterde "ADX ve Para Akışı (CMF)", eşik yok. → 1849791369482486118 (2024-10-25): MFV = Hacim × (2×Kapanış − Yüksek − Düşük)/(Yüksek − Düşük); CMF = 20 günlük MFV toplamı / 20 günlük hacim toplamı; 0 nötr.
- **R070** (risksiz faiz): defterde CAPM'de Rf = 10Y − 5Y CDS. → 1913880746973946124 (2025-04-20): "10 yıllık DT faizi kullanacaksınız. Abd için ise bu oran 0.05". 1913876527881539592: TR için 0.40 makul, 10Y ≈ 0.38.
- **R202** (rolling alpha): defterde "Rolling alpha Rolling skewness", pencere yok. → 1953358552308892053 (2025-08-07): "20-30-30-50 ona siz karar vereceksiniz". 1953390566898532487: 30 ya da 40 gün; seviye ve istikrar birlikte. 1953400490747662376: periyot volatiliteye göre (30 yerine 40).
- **R173** (getiri tanımı): → 1822596707558760524 (2024-08-11): yüzde getiri = 100 × (son − ilk)/ilk. 2001021294612242538 (2025-12-16): brüt = P_t/P_{t−1}, net = brüt − 1.

### 2.3 Beta, regresyon ve korelasyon

- **R200** (beta): defterde β = Kov/Var ve beta sınıfları. → 1878077873543663650 (2025-01-11): R_a = β·R_m + α; formül ve regresyon betası aynı 0.98910; alpha 0.02625. 1884663638360736096 (2025-01-29): aylık ve günlük beta farklı (BRYAT 1.21695 / 0.87178). 1823687517155016847 (2024-08-14): alfa anlamlılığı (EKGYO α 0,0147 anlamsız).
- **R066** (çoklu regresyon): defterde "Çoklu doğrusal bağlantı problemleri … bazı değişkenleri modelden çıkarmak gerekir". → 1825285752105619922 (2024-08-18): VIF, eşik yok. 1941790321668432140 (2025-07-06): "Anlamak ön plandaysa korelasyon, sadece tahminse PCA daha uygundur." 1866098693931421725: eğitim penceresi son 4 yıl.
- **R091** (korelasyon): defterde "Koç gibi korelasyon", pencere yok. → 1895180161261412820 (2025-02-27): Pearson, günlük % getiri, 2024-01-01–2025-01-01, EREGL–KRDMD 0,74. 2084854243131846782 (2026-08-05): uzun dönem ve 12 aylık rolling korelasyon + R². 1861112812967285159: "Pearson".
- **R234** (lojistik regresyon, doğruluk): defterde hacim+RSI lojistik model, doğruluk %55,00. → 1893042422088642888 (2025-02-21): olasılıklar PRED sütununa, karar sınırı 0.5. 1893042417617522992: eğitim %90, test %10. 1958130783354323290 (2025-08-20): UP eşik ≈0,6, DOWN eşik ≈0,4; DITAS olasılık 0.99 → LONG bias (görsel doğrulandı: noktalı çizgiler ≈0,6 ve ≈0,4). 1860463695790305656: bağımsız değişkenler 0/1 gösterge durumları. 1908882939976307137: ~%50 win rate veren parametre seçilir.
- **R174** (ARIMA): defterde itertools grid search, "en düşük hata oranı". → 1795910557695877254 (2024-05-29): MAE, MSE, RMSE minimum. 1878753192923803957: plot_acf/plot_pacf lags=20. 1945117767059038312: MA(1) var(y) = (1+β²)var(ε), corr = β/(1+β²).

### 2.4 Gösterge parametreleri ve optimizasyon

- **R138** (optimizasyon): defterde "EMA değeri walk forward le optimzie edilerek". → 1986899794032304554 (2025-11-07): SMA grid 10–250; XU100 2020-11-07–2025-11-07 en iyi 35/240, çarpan 4.6948, al-tut %+786.25; sağlam bölge: komşu parametreler de kârlıysa sağlam ((40,140),(45,145),(40,150)); "en iyi ayar bile zarardaysa strateji çöp". 1829983002304086142: TUPRS 50/200 → 48/247, strateji ~16,5, al-tut ~30. 1828161056960827738: DOAS Vegas 12-144-169 → 8-150-150, ~4,35 → ~5,05. 1778715914843684969: "Eğer gerçekten değişkenleri optimize etmeyi bilmiyorsanız trade yapmayın." Görseller doğrulandı.
- **R138** (devam): 1840170065464803535 (2024-09-28): "5-12 sadece bir kural ama optimize edilmeli". 1962960506509000705 (2025-09-02): "her hissenin ema'sı optimizasyon ile belli olur".
- **R140** (overfitting, metrikler): → 1992410986989441388 (2025-11-23): win rate ≥ %90 aşırı uyum şüphesi; GARAN 31 işlem, %58.06, kümülatif %1153.73. 1908882937325531171 (2025-04-06): K/Z 17.83, 21 işlem, win rate %42.86, PF 1.64, max DD −13.74, Sharpe 0.22.
- **R233** (RSI): defterde RSI(14), 30 girişi, 70 reddi. → 1860318349797814519 (2024-11-23): RSI = MA_Up/(MA_Up + MA_Down) × 100, period 20 rolling mean, 70/30. 1845465765421453791: Tansu SMA tabanlı, pandas_ta EMA tabanlı.
- **R258** (WMA, WaveTrend): defterde yalnız WMA21. → 1762082053330440337 (2024-02-26): WMA ağırlıkları 1..n, WMA13 ve WMA60; MACD = EMA12 − EMA26, sinyal EMA9 (adjust=False). 1760919805035467002: WMA 13/60. 1845362765898097116, 1845362768632799316 (2024-10-13): WT (10, 21); eşik >−60 ve <50 → <−50 ve <50.
- **R184 / R212** (ATR): → 1987507728718205244 (2025-11-09): TR = max(H − L, |H − önceki C|, |önceki C − L|); ATR = SMA(TR, 14); 2 ATR risk eşiği.

### 2.5 Diğer yöntem kayıtları

- **R131** (MA kesişimi): → 1831402232769847775 (2024-09-04): position = 1 eğer SMA_S > SMA_L, değilse −1; strateji = position.shift(1) × log getiri. 1923090364673450197: kapanış > SMA20 → al; günlük getiri > 0,03 → al.
- **R116** (uyumsuzluk): → 1838307130526310602 (2024-09-23): `lookback_hours_list = [24, 72, 168, 336, 720]`.
- **R190** (mean reversion): → 1774872096142754162 (2024-04-01): bant kırmızı 1.10 (85. kantil), yeşil ~0.97 (15. kantil); KCHOL B&H 5.58x, MR 1.31x. 1827401211731189852: "düşen piyasalarda zarar yazar".
- **R183** (mevsimsellik): → 1782896581408116765: zirve ayı kümülatif seriden okunur. 1823485106893300074: outlier ve yoğunluk kontrolü.
- **R209 / R210** (Heikin Ashi): → 1844839462896832814 (2024-10-11): son gün yeşil HA kapanışı taraması; AEFES 100.000 → strateji 207.546, B&H 144.057.

### 2.6 Bağlam ve veri kayıtları

- **R052** (kur forward): → 1906617987676696651: UIP i − i* = E(Δs), forward i − i* = p. 1984661206162964976 (2025-11-01): "Konservatif fiyat → Monte Carlo dağılımı → Risk primi ayarı → Volatilite testi".
- **R122** (frekans): → 1955281569599402000 (2025-08-12): bileşen frekans, genlik, faz. 1978783564511481981 (2025-10-16): dominant döngü 20, 50, 200 gün; Kelly; iddia Sharpe 2,5-3,5 (kanıt yok).
- **R028 / R031** (IV): → 1925561082392834472 (2025-05-22): fiyat yatay + IV yükselişi → kırılım beklentisi, yön yok.
- **R186 / R024** (VP/AVWAP): → 2005293321233576379 (2025-12-28): "günlük grafikte son 60 bar (3 ay)".
- **R199 / R004** (zaman dilimi, SMC, kanal): → 1849792794132435435: yfinance 15 dk gecikmeli → en az 4 saatlik. 2001758848781107549: itki %10, geri çekilme %50–79, FVG. 1956109174083084636: haftalık kanal alt bandı + yeşil kapanış.

---

## 3. Çelişkiler

Defter tarihi kayıt anıdır. Özgün paylaşım tarihi bilinmez. Bu yüzden "sonra gelen" sırası kayıt anına göredir; özgün sıra belirsizdir.

### Ç1. HMM ↔ R091

- Gönderi 1923641490783322182 (2025-05-17): "HMM (Gizli Markov Modeli) güçlü bir araçtır"; "İlk aşamada HMM, bir zaman serisindeki gizli rejimleri tespit eder."
- Defter R091 (kayıt 2026-08-27 22:21, Yazar: T): "Trend rejim değişikliği için HMM yapmanıza gerek yok Koç gibi korelasyon varken hiç gerek yok hemde"
- Sonra gelen: defter kaydı (kayıt anına göre).
- Olasılık: **bağlam**. Gönderi HMM'i lojistik regresyona girdi (rejim olasılığı) olarak kullanır. R091 trend rejim değişikliğini tek başına tespit etmeyi konu alır. **Tarihçe** de olasıdır; R091'in özgün tarihi belirsiz.

### Ç2. Yön tahmini ↔ R185 ve R058

- Gönderi 1864545215593304274 (2024-12-05): "ne ka sorusunun cevabı sağlıklı olmaz. Yukarıdaki algo sınıflandırma algoritması yani kategorik veriler için bir tahmin yapıyor."
- Gönderi 1778899999671066629 (2024-04-12): "#randomforest benimde çok önem verdiğim bir algoritma. Yanlış anlamayın R2 0,98 falan yani :)"
- Defter R185 (kayıt 2026-08-28 06:35, Yazar: M, LLM biçimli): "algoritma geliştirenlerin düştüğü en büyük tuzak, fiyatın gelecekteki yönünü 'tahmin etmeye' çalışmaktır."
- Defter R058 (kayıt 2026-08-27 20:02): "Regresyon veya makine öğrenmesi modelleri ile hisse fiyatı modellenmez"
- Olasılık: **tarihçe**. 1977458197158932959 (2025-10-12) "Neden hisse senedi fiyatlarını tahmin etmemeliyiz ya da edemeyiz." der; bu, R185 yönündedir. **Bağlam** da var: 1864545215593304274 büyüklüğü reddeder, yalnız yönü sınıflar; 1778899999671066629 emtiadır, öğretim örneğidir. Ek kanıt: defterin kendi R234'ü lojistik regresyonla yön modeli kurar. R185 Tansu'nun kendi cümlesi olmayabilir (Yazar: M).

### Ç3. Yıllıklaştırma çarpanı ↔ R223

- Gönderi 1915540627405554032 (2025-04-24): ".std() * np.sqrt(255) → Günlük volatiliteyi yıllıklaştırır"; yıllık getiri = ort. günlük getiri × 255.
- Gönderi 1942696711287169192 (2025-07-08): "bu volatilite 252 işlem günüyle çarpılarak yıllık volatilite elde edilir"
- Defter R223 (kayıt 2026-08-28 11:36, Yazar: T): "yillik_volatilite = gunluk_volatilite * np.sqrt(252)"
- Sonra gelen: defter kaydı. Ayrıca 2099366035111493673 (2026-09-14) `returns.std() * (252 ** 0.5)` kullanır; bu, R223 ile uyumludur.
- Olasılık (255): **hata** ya da **bağlam**. Diğer Tansu kodları √252 kullanır (1852070155779739853 görseli, 2099366035111493673). Gönderide 255 için gerekçe yok. BIST işlem günü varsayımı olabilir; belirsiz.
- Olasılık (×252): **hata** (sözel anlatım). Varyans 252 ile çarpılır; std √252 ile çarpılır. Kodsuz cümledir.

### Ç4. Fiyatın std'si ile oynaklık ↔ R223

- Gönderi 1897620709624442886 (2025-03-06): `df["Volatilite_20"] = df["Close"].rolling(window=20).std()  # 20 günlük volatilite`; TUPRS Volatilite_20 5,80 (TL).
- Gönderi 1912735331918516711 (2025-04-17): "df['Close'].rolling(window=20).std() → 20 günlük volatilite."
- Defter R223 (kayıt 2026-08-28): "gunluk_volatilite = data['Getiri'].std()" (Getiri = `Close.pct_change()`).
- Olasılık: **hata** (adlandırma). Fiyat std'si TL birimlidir ve fiyat düzeyine bağlıdır. Hisseler arası kıyas yapılamaz. **Bağlam** da olası: fiyat std'si Bollinger bandı (R053) için doğrudur; eğitim gönderileridir.

### Ç5. Düşük std'li hisse ↔ R110 ve R230

- Gönderi 1764308359635710087 (2024-03-03): "yüksek sharpe ratio yakalamak için standart sapmanın düşük olduğu hisselerde trade yapmak önemlidir"
- Defter R110 (kayıt 2026-08-27 23:38): "Yüksek Volatilite: Portföye girecek hisselerin "hareketli" olması gerekir."
- Defter R230 (kayıt 2026-08-28 12:23): "1. Aktif Volatilite (Oynaklık) Aranmalı"
- Olasılık: **bağlam**. R110 volatilite hasadı (iç dalgalanmadan kâr) içindir. Gönderi Sharpe paydasını küçültmeyi konu alır. **Tarihçe** de olası; gönderi 2024'tür.

### Ç6. Williams %R −20 ↔ R170

- Gönderi 1844502539414511699 (2024-10-10), görsel: "-20 SELL (OVERBOUGHT)", "-80 BUY (OVERSOLD)".
- Gönderi 1845098408727461989 (2024-10-12): WR(14) −80 al / −20 sat; "%R ve MACD stratejisi 100.000$ için 3.546$ kazandırdı. (%3,5) Alıp tutan ise 42.64% kazandı"
- Defter R170 (kayıt 2026-08-28 04:55): "Ön Koşul: Williams %R önce aşırı alım bölgesine (-20 ile 0 arası) girmelidir."
- Olasılık: **bağlam**. Gönderi ortalamaya dönüş okumasıdır; R170 momentum geri çekilme kurgusudur (SMA14 filtresi, −50 dönüşü). Gönderinin kendi sonucu klasik okumanın BTC'de al-tutu geçemediğini gösterir.

### Ç7. RSI sabit eşik ↔ R233

- Gönderi 1860405835354054736 (2024-11-23): "RSI 30/70 Allah kelamı değil. Hissenin volatilitesine göre değerleri optimize etmeniz lazım"; EURUSD RSI (6, 65, 20) ~2,6 vs (26, 75, 24) ~1,24.
- Defter R233 (kayıt 2026-08-28 12:30): "RSI (14) değeri, 30 seviyesinin altından yukarı doğru keserek bu seviyenin üzerinde bir kapanış yaptığında."
- Olasılık: **bağlam**. R233 belli bir kurulumun varsayılan eşiğidir. Gönderi optimizasyon ilkesini (R138) söyler. Aynı gün 1860318349797814519 da 70/30 kullanır.

### Ç8. Emir defteri derinliği ↔ R225

- Gönderi 1983480217894060348 (2025-10-29): "alış baskısı olan hisseler (Alış lot > Satış lot) ortalama %0.06 değişim gösterdi Satış baskısı olan hisseler (Satış lot > Alış lot) ortalama %0.53 değişim gösterdi"
- Gönderi 1983528060700778778 (2025-10-29): "Yani bir hissede çok alış emri var diye yükselir sanma, çok satış emri var diye düşer sanmayin."; alış lot r = −0.031 p = 0.4542; satış lot r = −0.136 p = 0.0009.
- Defter R225 (kayıt 2026-08-28 11:53, Yazar: M): "Emir defterin alış tarafı kalınsa... satış tarafı inceyse... alım için iyi sinyal olabilir."
- Olasılık: **tarihçe** ya da **kaynak farkı**. Gönderi tek günlük (28/10/2025) ölçüme dayanır. R225 LLM biçimli metindir. Satır "R225 (2025-11-29) bu gönderiden sonra yazılmış" der; defterde bu tarih yok, doğrulanamadı (belirsiz).

### Ç9. Long-only ↔ R101 ve R013

- Gönderi 1840098451750826475 (2024-09-28): "Long, prensip olarak short işlem yapmıyorum :)"
- Defter R101 (kayıt 2026-08-27 22:59): "Aşırı Ucuzlayanı AL (Long) Aynı anda Aşırı Pahalananı SAT (Short)"
- Defter R013 (kayıt 2026-08-27 17:11): "Duruma göre short ya da long pozisyon alınır."
- Olasılık: **bağlam**. Gönderi Tansu'nun kişisel uygulamasıdır; R101 ve R013 yöntem anlatımıdır. Satıra göre R251 uygulaması short yerine öbür hisseye geçer; bu, gönderiyle uyumludur.

---

## 4. Gönderi içi hatalar ve tutarsızlıklar

### 4.1 Formül ve kod hataları

| Kaynak | Hata | Doğrusu |
|---|---|---|
| 1979645829377057243 (2025-10-18) | kodda `/ sigma*np.sqrt(T)` (öncelik hatası): σ'ya böler, √T ile çarpar | `/ (sigma*np.sqrt(T))`; T=1 dışında d1 yanlış |
| 1897926545328501123, 1897926549338214614 (2025-03-07) | `BlackScholes("c", s, X, Time, r, r - q, sigma)`: q argümanına r − q gider | q argümanına q (temettü verimi) |
| 1942718595714396552 (2025-07-08) | vega formülünde üs (−d1²) | standart üs −d1²/2 |
| 1852070155779739853 (2024-10-31) | görselde `market_cap = stock_price * 1000000`: hisse sayısı sabit 1 milyon. σ olarak hisse getirisi oynaklığı kullanılır; Merton varlık oynaklığı ister (bu belgenin görsel okuması) | piyasa değeri = fiyat × gerçek hisse adedi; σ_A ayrıca çözülür |
| 1907020122851569733 (2025-04-01) | kur değişimi = (S_t − S_{t−1}) / S_t; %10 artış 0.0909 çıkar, metin 0.10 der | payda S_{t−1} |

### 4.2 Ölçü ve adlandırma hataları

| Kaynak | Hata | Doğrusu |
|---|---|---|
| 1897620709624442886, 1912735331918516711 | fiyatın 20 günlük std'si "volatilite" diye adlandırılır | getirinin std'si (R223) |
| 1915540627405554032 | yıllıklaştırma √255 / ×255 | √252 / ×252 (Tansu'nun diğer kodları) |
| 1942696711287169192 | "volatilite 252 işlem günüyle çarpılarak" | std × √252 |
| 1904911428877762622 | "Gelecek dönemlere daha fazla ağırlık vermek isterseniz düşük psi değeri verirsiniz." Ağırlık psi^i olduğundan düşük psi uzak dönemlere daha az ağırlık verir | metin koda terstir |
| 1773320333249896719 | "yüksek alpha düşük information ratio güzeldir" | IR = aktif getiri / tracking error tanımında (1980319432141308317) yüksek IR iyidir |

### 4.3 Metin–görsel ve sayı uyuşmazlıkları

- 1844839462896832814 (2024-10-11): metinde 440.57; görselde B&H 144.057 (satır: "aslında 44.057").
- 1906617998963535982 (2025-03-31): metin örneği yerel enflasyon %8; kod çağrısı `inflation_domestic=0.45`, çıktı enflasyon farkı 0.42.
- 1911360294384816565 (2025-04-13): metin Nisan der; grafik ekseni "Day of February", 29 gün.
- 1905916775931208060 (2025-03-29): örnek değer 10,29 TL ("mesela"); kod çıktısı 11,0439 (1905916780465307673).
- 2099594176606187548 (2026-09-14): yöntem adı çarpım (×) der; görseldeki skor ağırlıklı toplama uyar (Bölüm 1.1b).

### 4.4 Kanıtı zayıf iddialar

- 1908882937325531171 (2025-04-06): "21 işlemden 9 tanesi başarılı bu overfitting sorunu olmadığının göstergesi". Düşük isabet oranı tek başına aşırı uyum testi değildir. Out-of-sample sonucu yok.
- 1978783564511481981 (2025-10-16): "Sharpe 2,5-3,5, maks. düşüş %15-20" iddiası; backtest kanıtı yok.
- 1899583516670611844: alpha+beta ≈ 0.912 yorumu; omega ve alpha anlamsız (görsel: p 0.414, 0.301).
- 2099952521221661048: p değerleri NumPy fallback ile yaklaşık (görsel notu).

### 4.5 Defter okuma hataları

- `tema-5a.jsonl` içinde "DEFTER OKUMA HATASI" etiketli satır yok.
- 1983480217894060348 satırı R225 için "2025-11-29" tarihini verir. Defter-4 başlığı yalnız "2026-08-28 11:53" kayıt anını gösterir. Bu tarih doğrulanamadı; olası satır hatasıdır (belirsiz).

### 4.6 Tasarımda kopyalanmayacak formüller

1. Black-Scholes d1 kodu: `... / sigma*np.sqrt(T)` (1979645829377057243).
2. `BlackScholes(..., r, r - q, sigma)` çağrısı (1897926545328501123, 1897926549338214614).
3. Vega üssü −d1² (1942718595714396552).
4. DtD kodundaki `market_cap = stock_price * 1000000` ve σ_E = σ_A varsayımı (1852070155779739853).
5. Fiyat std'si = volatilite (1897620709624442886, 1912735331918516711).

Ek liste:

1. √255 ve ×255 yıllıklaştırma (1915540627405554032).
2. "volatilite × 252" (1942696711287169192).
3. Kur değişimi paydası S_t (1907020122851569733).
4. Psi yön ifadesi (1904911428877762622); kod formülü doğrudur, metin yanlıştır.

---

## 5. Defter için öneri listesi

Öncelik ölçütü: tam parametre, Tansu'nun kendi yöntemi, birden çok gönderide tekrar. İlk 10 maddede görseldeki parametreleri Read ile açtım. Hepsi satırla uyuştu. Ek bulgular "Görsel" sütunundadır.

### 5.1 Öncelik 1–5

| # | Etiket | Öneri | Kaynak id | Görsel |
|---|---|---|---|---|
| 1 | ekle | Fon likidite stres testi: gün = (çıkış TL × ağırlık)/(0,20 × 20G medyan TL hacim); senaryo %5/%10; katılım %10/%20/%30; stresli gün = normal gün / kullanılabilir hacim katsayısı | 2095983340142882886, 2096187367778370014, 2096243590133407910, 2097031747347030189, 2099919520844382444 | doğrulandı (TRHOL 7,22); sınıf sınırları görselden çıkarım |
| 2 | ekle | Fon akış erken uyarı zinciri ve Erken Uyarı Skoru: 5G → 20G → AUM → pozisyon riski; Yapısal Risk + Aktivasyon | 2099132513708851639, 2099594176606187548, 2097548996193526092, 2095931263593095368, 2099959209467211874 | doğrulandı; skor ≈ 0,4 Y + 0,6 A çıkarımı, formül Tansu'ya sorulmalı |
| 3 | ekle | Granger hattı: ADF → eş anlı → gecikmeli Pearson/Spearman (lag 1–5) → Granger lag 1–5 + FDR | 2099952521221661048, 2099751961159454867, 1922963356362703307, 2101627771524927545 | doğrulandı; p yaklaşık (NumPy fallback) |
| 4 | ekle | Durağanlık ön testi: ADF p < 0.05; değilse fark al; KPSS ile çapraz kontrol | 1904748993797632344, 1904748996893053368, 1904748999908692189, 1904749002748281042, 1904749005990510772 | metin (görsel yok) |
| 5 | genişlet | R097 GARCH(1,1): Student t, log getiri; omega 0.2951, alpha 0.1494, beta 0.7625; seçim AIC/BIC + Ljung-Box, EGARCH | 1899583516670611844, 1952739571466211673 | doğrulandı; omega ve alpha anlamsız |

### 5.2 Öncelik 6–10

| # | Etiket | Öneri | Kaynak id | Görsel |
|---|---|---|---|---|
| 6 | genişlet | R061 DtD formülü ve eşikleri: DD > 2 / ≈1–1.5 / < 1; EDF = N(−DD); PD 0.20/0.50 sınıfları. Kodu kopyalama (Bölüm 4.6) | 1852070155779739853, 1907840099489874309, 1907840096851624360, 1888561706638405699 | doğrulandı; ek hata market_cap × 1e6 |
| 7 | genişlet | R137/R115 Sharpe ve Sortino formülü: mean × 252, std × √252; rf = 10Y tahvil (TR ≈ 0,38–0,40, ABD 0,05) | 2099366035111493673, 1878164936150360461, 1913880746973946124, 1913876527881539592, 2099453056337203495 | doğrulandı (rf ≈ 0,3988 tutar) |
| 8 | genişlet | R202 rolling Sharpe/alpha: pencere 20/30/40/50, volatiliteye göre seçim; −0.40/−0.60 dönüş seviyesi | 1953358552308892053, 1953390566898532487, 1953400490747662376, 1910417850684367263, 1913512010253205811 | doğrulandı (21 gün, −0.4) |
| 9 | genişlet | R234 lojistik yön olasılığı: PRED, karar sınırı 0.5; UP ≈0,6 / DOWN ≈0,4; eğitim %90 / test %10 | 1893042422088642888, 1893042417617522992, 1958130783354323290, 1860463695790305656 | doğrulandı (≈0,6 / ≈0,4) |
| 10 | genişlet | R138 grid optimizasyonu + sağlam bölge kuralı + al-tut kıyası | 1986899794032304554, 1829983002304086142, 1828161056960827738, 1840170065464803535, 1962960506509000705 | doğrulandı (35/240; 48/247; 8-150-150) |

### 5.3 Öncelik 11–15

| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 11 | çeşitlendir | R200 altı faktörlü beta (USDTRY, EURUSD, BRENT, SPX, DAX, US_10Y) ve Fama-French SMB/HML; pencere tanımı eklenmeli | 1878209442790998442, 1919250826435965149, 1943070389388873813, 1893286881917366600, 1893286885021085822 |
| 12 | genişlet | R053 Bollinger n=20, ±2 örnek std; VaR 1 gün %95 | 1850460386371281374, 1850468058747326871, 1916228528850272645 |
| 13 | genişlet | R233 RSI: SMA tabanlı period 20 ve EMA tabanlı ayrımı; eşik hisseye göre optimize | 1860318349797814519, 1845465765421453791, 1860405835354054736 |
| 14 | genişlet | R140 aşırı uyum kontrolü: win rate ≥ %90 şüphe; PF, max DD, Sharpe çıktı seti | 1992410986989441388, 1908882937325531171, 1908882939976307137, 1875902835780677930 |
| 15 | genişlet | R258 WMA 13/60 + MACD 12/26/9; WaveTrend (10, 21), eşik <−50 ve <50 | 1762082053330440337, 1760919805035467002, 1845362765898097116, 1845362768632799316 |

### 5.4 Öncelik 16–20

| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 16 | genişlet | R137 CMF(20) formülü; R184/R212 ATR = SMA(TR, 14), 2 ATR | 1849791369482486118, 1987507728718205244 |
| 17 | ekle | Ichimoku 9/26/52, shift 26 | 1760937885190996368, 1840046005787504758 |
| 18 | çeşitlendir | R124/R105 EMA5 / EMA10(EMA5) kesişimi + CCI(20), ±100 | 1760742464309350866, 1760725146959270113 |
| 19 | çeşitlendir | R128/R138 Vegas EMA 12/144/169 + RSI(14) 50 | 1827737743683707129, 1783160562156716179 |
| 20 | genişlet | R116 lookback [24, 72, 168, 336, 720] saat; R186 VP/AVWAP son 60 bar | 1838307130526310602, 2005293321233576379 |

### 5.5 Öncelik 21–25

| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 21 | genişlet | R185 Risk of Ruin örnekleri (p=0,49 → %1,80; p=0,51 → %98) ve rastgele yürüyüş √adım | 1874240306461512014, 1874238154355728692, 1977458197158932959 |
| 22 | çeşitlendir | R021 KNN yön sınıflaması (OHLC, Öklid, %75); k eksik | 1859240563205107928, 1861901396506743020, 1864342754844660140 |
| 23 | çeşitlendir | R225 envanter azaltma Monte Carlo (100.000 senaryo, 5 profil) | 1924523925683274094 |
| 24 | çeşitlendir | R174 auto ARIMA stepwise AIC, m=12; MAE/MSE/RMSE | 2019525738207060400, 1795910557695877254 |
| 25 | ekle | Koşullu rastlantı testi (volatiliteyi koruyan karıştırma) | 1955986393622306882 |

### 5.6 Öncelik 26–30

| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 26 | çeşitlendir | R138/R251 Treynor, Jensen, M2, IR, Sortino formül seti | 1980319432141308317, 1951196059939569688, 1953401516565340457 |
| 27 | genişlet | R033 IQR'ı günlük getiriye uygula; R190 kantil bandı 85/15 | 1822549636013240372, 1774872096142754162, 1827401211731189852 |
| 28 | genişlet | R066 VIF, Durbin-Watson, PCA; Ridge/Lasso alpha taraması | 1825285752105619922, 1950584440805081552, 1941790321668432140, 1825488501254578373 |
| 29 | çeşitlendir | R052 parite ilişkileri ve psi modeli (kurumsal kur; hisse değil) | 1906617984665137406, 1904911424641450458, 1984661206162964976 |
| 30 | ekle | Ders modülü: Black-Scholes, binom (M=3 → 11,0439), BS+MC; yalnız eğitim, kod hataları düzeltilerek | 1905916780465307673, 1897926542044389854, 1979645829377057243 |

### 5.7 Öncelik 31–33

| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 31 | genişlet | R091 Pearson, 12 aylık rolling korelasyon + R² | 1895180161261412820, 2084854243131846782 |
| 32 | genişlet | R122 Fourier → Wavelet sırası | 1978893346727956651, 1955281569599402000 |
| 33 | ekle | Çelişki notu: Ç1–Ç9 defterde "açık soru" olarak işaretlensin; özgün tarihler eklensin | 1923641490783322182, 1864545215593304274, 1915540627405554032, 1983528060700778778, 1840098451750826475 |
