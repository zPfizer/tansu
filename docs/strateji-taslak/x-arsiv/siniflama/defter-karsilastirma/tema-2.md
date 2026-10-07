# TEMA 2 — Bölge ve formasyon: defter öneri belgesi

Kaynak: `tema-2.jsonl` (175 satır: 101 genişletir, 58 çeşitlendirir, 13 çelişir, 3 yeni). Defter: `defter-fikir.txt`, `defter-1..4.md`.

Okuma notları:
- Gönderi tarihleri 2023-08 ile 2026-09 arasındadır. Defter kayıtları 2026-08-27 ile 2026-09-06 arasındadır. Bu yüzden çelişkilerin çoğunda defter sonra gelir.
- "(görsel doğrulandı)" notu, bu belge yazılırken görselin Read ile açıldığını ve sayıların görselle uyuştuğunu belirtir.
- "(bu belgede hesaplandı)" notu, sayının satırda değil, doğrulanan görseldeki değerlerden hesaplandığını belirtir.
- Olgunluk: **tam** = parametre + giriş + çıkış/stop var. **çekirdek** = kural var, bazı parametreler yok. **fikir** = yalnız ad ya da örnek var.

---

## 1. Yeni yöntem aileleri

Bu bölümde iki tür yöntem var: defterde adı ve amacı olmayan yöntemler, adı defterde olmayan türevler.

### 1.1 RSI üzerine Fibonacci (RSI Fibo)
- **Ne yapar:** Fibonacci seviyelerini fiyata değil, RSI çizgisine uygular. Seviyeleri "momentum destek ve direnci" olarak okur.
- **Parametreler:** RSI(14). Pencere geriye doğru 144 gün (ya da 144 çubuk). Bu pencerede RSI'ın en yüksek ve en düşük değerleri arasına Fibonacci çekilir. Seviyeler 23.6 / 38.2 / 50 / 61.8.
- **Kural:** Boğa piyasasında RSI 38.2 ya da 50'ye düşüp yukarı dönerse momentum destek bulur. Ayı piyasasında RSI 50 ya da 61.8'e çıkıp aşağı dönerse momentum dirence takılır. Dönüş ölçütü, stop ve çıkış yazılı değil.

*Kaynak ve durum:*
- **Kaynak:** 1986826801885167861 (2025-11-07).
- **Tansu'nun vurgusu:** Yöntemi "standart bir al-sat sinyali üreten mekanik bir sistemden çok ... yoruma dayalı bir model" diye tanımlar.
- **Olgunluk:** çekirdek.
- **Not:** Satırda `yontem_defterde: "var"` yazar. Defterde RSI'a çekilen Fibonacci yok. R208 yalnız "Fibonacci Seviyesi + RSI Uyumsuzluğu" çakışmasını anlatır. İşaret büyük olasılıkla hatalıdır. İlgili gönderi: 1908510592639398132 (2025-04-05) fiyat Fibonaccisinde de "144 bar iyi" der.

### 1.2 Mum formasyonu kod kuralları (Tansu'nun kendi kodu, Mart–Mayıs 2025 serisi)
Defterde R023 (bullish engulfing kodu) ve R143 (gölge/gövde geometrisi) var. Aşağıdaki formasyonların adı defterde yok.

**a) Tasuki Gap**
- **Kod (Bullish):** `C[i] < O[i]`, `C[i] < O[i-1]`, `C[i] > C[i-2]`, `C[i-1] > O[i-1]`, `O[i-1] > C[i-2]` (gap), `C[i-2] > O[i-2]` (görsel doğrulandı).
- **Kural:** Birinci mum güçlü yeşildir. İkinci mum yukarı gap ile açılır ve yeşil kapanır. Üçüncü mum kırmızıdır ve gap'i tamamen kapatmaz. Bearish türü bunun tersidir. Bullish türü destekte, bearish türü dirençte güçlenir. Filtreler: hacim, EMA, RSI, MACD, trend yönü. Gap büyüklüğü ve "güçlü" mum için eşik yok.
- **Kullanım:** Önce RSI pozitif uyumsuzluğu oluşur, sonra Tasuki Gap gelir. Bu sıra alım teyidi sayılır. RSI periyodu yazılı değil.
- **Kaynak:** 1905592381618962842 (2025-03-28), 1910750629976297685 ve 1910750631876309396 (2025-04-11), 1914394674921722043 (2025-04-21), 1919047175444533558 (2025-05-04).

**b) Shrinking (daralan mumlar)**
- **Ayı türü kodu:** `C[i-4] > O[i-4]`, `C[i] < O[i]`, `C[i] < L[i-3]`. Gövde mutlak değerleri sırayla küçülür: i-3 < i-4, i-2 < i-3, i-1 < i-2. Ek koşul: `L[i-1] > L[i-2] > L[i-3]`. Sinyal aynı gün `sell = -1` (görsel doğrulandı).
- **Boğa türü (metin):** Birinci mum ayıdır. Mum 2–4'ün rengi serbesttir, her biri bir öncekinden küçüktür. Beşinci mum boğadır ve ikinci mumun tepesini aşar.
- **Kaynak:** 1906298040333308407, 1906298044510879769, 1906298048017264857, 1906299112422551926, 1906299132194476185 (hepsi 2025-03-30).

**c) Quintuplets (beşizler)**
- **Kod:** Son 5 mumun her birinde `C > O`, `C > önceki C` ve `C − O < body` koşulu var. Ayı türü bunun tersidir. Sinyal aynı gün verilir (görsel doğrulandı). `body` değişkeninin değeri görselde yok.
- **Kural:** Formasyon düşük volatilitede, küçük gövdeli boğa mumlarıyla oluşur.
- **Kaynak:** 1905940770281910507 (2025-03-29), 1919053643946303495 (2025-05-04; burada "bir sonraki gün alım" der).

**d) Bottle, H, Slingshot**
- **Bottle:** mum1 boğa. mum2 boğadır, alt fitili yoktur (açılış = en düşük), üst fitili vardır. `high2 > close2`, `open2 < close1` (aşağı gap). Kaynak: 1905945897105531327, 1905945899810910520 (2025-03-29).
- **H (3 mum, devam):** mum1 `C > O`. mum2 kararsızlık mumu, `O = C`. mum3 `C > O`, `C3 > C2`, `L3 > L2`. Kaynak: 1905960716571451830, 1905960719561986200 (2025-03-29).
- **Slingshot:** mum1 boğa. mum2 daha yukarıda kapanır. mum3–4'ün sonuncusu öncekinin tepesini geçmez. Son mumda `low ≤ mum1 high` ve `close > mum2 high`. mum2–3'ün rengi serbest. Kaynak: 1905953843331940372, 1905953875007357298 (2025-03-29).

**e) Dark Cloud Cover ve Piercing**
- **Dark Cloud Cover:** Yukarı trendde oluşur. 1. mum beyaz ve uzundur. 2. mum siyahtır, 1. mumun üstünde açılır ve 1. gövdenin ortasının altında kapanır. 2. gündeki hacim artışı güveni artırır. Stop 1. mumun en yükseğidir. Hedef yakın destektir. Başka göstergeyle teyit gerekir. Kaynak: 1982688365007794207 (2025-10-27).
- **Piercing:** Tarama çıktısında ölçüm var: Hit Ratio 50.0 %, Profit Factor 2.78, Realized RR 2.78, Number of Trades 4 (görselden). Kaynak: 1906062787979210957 (2025-03-29).

- **Olgunluk:** Giriş koşulları kodla tam. Çıkış yalnız Dark Cloud Cover'da var. Aile geneli: çekirdek.
- **Tansu'nun vurgusu:** Kodları kendisi yazar. Piercing için "Bunlar momentum hisselerim değil, basit taramalar" der.

### 1.3 TA-Lib CDL taraması ve adı defterde olmayan tek mumlar
- **Ne yapar:** TA-Lib `CDL*` işlevleriyle son gün (ya da son saat) mumlarını etiketler. Evren BIST30, BIST50, XU100 ya da tek hissedir. Saatlik türde veri periyodu 5 gündür.
- **Parametreler:** Yön ve işlem kuralı yok. Tansu çıktıyı "analizlerinde kullanmak isteyenler için" ham girdi olarak verir.
- **Kaynak (TA-Lib):** 1847992441699246587, 1847995732692725934 (2024-10-20), 1848384600541729106 (2024-10-21), 1848805345545851079 (2024-10-22), 1851722895086752198 (2024-10-30).
- **Kaynak (TA-Lib, devam):** 1866680568965922864 (2024-12-11), 1889377222160486600 ve 1889453445549097041 (2025-02-11), 1898114891531071762 (2025-03-07), 1899922146769485826 (2025-03-12).
- **Kaynak (TA-Lib, son):** 1907095706285826234 (2025-04-01), 1908276450450432440 (2025-04-04; 22 bar).

*Tek mumlar ve durum:*
- **Tek mumlar:** Belt Hold + Closing Marubozu dip teyidi (2009318796025360724, 2026-01-08). Marubozu teyit mumu (1909682434720809077, 2025-04-08). Endekste closing marubozu, ertesi gün yükseliş beklentisi (1943070866323181796, 2025-07-09).
- **Tek mumlar (devam):** Fibo 78.6'da asılı adam, kırılımda hedef 61.8 = 10.22 (1908505150668370269, 2025-04-05). Shooting Star taraması (1851736967240618260, 2024-10-30; 1855002192115024146, 2024-11-08). Tanım ve eşik yok.
- **Olgunluk:** fikir (kural yok, yalnız etiket).

### 1.4 Harmonik tür genişlemesi (adı defterde olmayan türler)
- **Ne yapar:** Defterde Gartley, Kelebek, AB=CD, Crab ve Kuğu var. Tarayıcı kartlarında başka türler de çıkıyor.
- **Bat:** VKING (1876368569438765488, 2025-01-06; XA 7.06, AB −3.08, BC 1.00, CD −1.68, Fibo 31.56 / 31.28). ANHYT (1877449919641833760, 2025-01-09; XA 25.00, AB −7.35, BC 5.05, CD −7.75, Fibo 92.46 / 91.16). LIDER (1893684348391391620, 2025-02-23; XA 19.00, AB −7.80, BC 3.10, CD −4.90, Fibo 141.37 / 140.55).
- **Alt Bat ve Cypher:** Alt Bat MRGYO (1872027142181232735, 2024-12-25; XA 0.42, AB −0.17, BC 0.07, CD −0.13; Fibo 0.618: 1.63, 0.786: 1.61). Cypher INDEX-USD (1878174325863313704, 2025-01-11; XA 0.48, AB −0.33, BC 0.40, CD −0.59; Fibo 2.66 / 2.56).
- **Tarayıcı menüsü:** 10 tür ayrı seçenektir: Butterfly, Gartley, Cypher, Bat, Alt Bat, Crab, Deep Crab, Shark, White Swan, Black Swan. Ayrıca [11] TÜM FORMASYONLAR ve [0] çoklu seçim var. Evren 521 hisse (1977815566183497963, 2025-10-13).

*Ek tür ve durum:*
- **Derin Yengeç:** CCOLA görselinin başlığı "Derin Yengeç Formasyonu + Demand/Supply Analizi"dir (2089770598620713304, 2026-08-18; görsel doğrulandı). Satırda yalnız "Crab" yazıyor.
- **Olgunluk:** çekirdek (kart var; tür için oran kuralı yazılı değil).

### 1.5 Tepe/dip algoritması (Level 1 / Level 2) ve dip taraması
- **Ne yapar:** İki kademede tepe ve dip noktalarını işaretler. Kırmızı = tepe, yeşil = dip. Dip oluşmadıkça yeni tepeleri işaretler.
- **Parametreler:** Tarama penceresi son 10 gün. Level 1 = day trade. Level 2 = trend takibi, daha az sinyal. Repaint yok. Dip parametreleri grid search ile optimize edilir. Kademe tanımı ve eşik yok.
- **Kullanım:** Dip ve diğer göstergeler olumluysa giriş yapılır. Price action mum teyidinden sonra "kısa sürede" giriş yapılır.
- **Dip taraması derecesi:** 3 kriter + OB yapısı = 1. derece dip sinyali. Dipte EMA13 > EMA8 > EMA5 sıralaması. Mumlar: 3INSIDE / BELTHOLD / CLOSINGMARUBOZU (2002099118366486932, 2025-12-19).

*Kaynak ve durum:*
- **Kaynak:** 1908897010742067310 ve 1909002131635331358 (2025-04-06), 1910423863822811223 (2025-04-10), 1924944817441710378 (2025-05-20), 1950987288378519760 (2025-07-31).
- **Tansu'nun vurgusu:** "Dibi herkes kendine göre yakalıyor benim de kendi algoritmam var." "bunları sinyal olarak görmemek lazım." "Overfitting diye saçma sapan yorumlar yapmayın ... sadece istatistik var."
- **Olgunluk:** çekirdek.
- **İlgi:** R039 ATR zigzag ile ilişkisi belirsiz. Satırların üçü `genisletir` ve `yontem_defterde: yok` işaretlidir.

### 1.6 Bant, kanal ve ortalama türevleri (adı defterde yok)
- **ATR bantları:** bant = EMA26 ± k × ATR14 (k = 1, 2, 3). Close–EMA26 sapması % olarak verilir. Konum etiketleri "+2ATR üstü" ve "pivot bandı S1–R1". MACD AL/SAT türleri: hook, 0 geçiş, kesişim. Kaynak: 1957877677777375736 (2025-08-19). Olgunluk: çekirdek.
- **Keltner kanalı:** Orta bant EMA20, ±1/±2/±3 bant. Yanında EMA5, SMA200, SMA250, RSI14 70/30. Giriş koşulu ve ATR çarpanı yazılı değil (1979691577632231774, 2025-10-18). BTC kartında etiket DC_UP/DC_DOWN (1852451504705155208, 2024-11-01). Olgunluk: fikir.
- **Vegas tüneli:** Üç ortalama 30-109-150, günlük, "parametreler optimize edilmiştir". Ortalama türü yazılı değil. Kaynak: 1835559479842070775 (2024-09-16). Olgunluk: fikir.
- **T3 kesişimi + Belt Hold:** T3 parametreleri yazılı değil. EMA 5/8/13/21. Kaynak: 1995924034911961480 (2025-12-02). Olgunluk: fikir.
- **Kanal orta noktası, dikdörtgen, range breakout:** Kanal orta noktası "mıknatıs" olarak kullanılır, tanımı yok (1914188571033940188, 1914387519392579977; 2025-04-21). Dikdörtgen bantta destekte al, dirençte sat (1987071191442497586, 2025-11-08). Range breakout + CDLBELTHOLD (1950285317841301734, 2025-07-29). Olgunluk: fikir.

### 1.7 Göreli konum ve dipten uzaklık
- **Ne yapar:** Fiyatın kayan bir penceredeki en düşük ve en yüksek arasındaki yerini ölçer.
- **Parametreler:** Göreli konum 0–1, pencere 16 gün (R227'de 252 gün). Örnek ≈0.95 = 16 günlük zirveye yakın, aşağı sarkma riski (1775315669824700852, 1775315672647528494; 2024-04-03). Formül yazılı değil.
- **Dipten uzaklık:** % = (son − dip) / (zirve − dip). Pencereler haftalık, aylık, 3, 6, 12 aylık. Sektör bazlı "Dibine Yakın Hisseler" listesi. Örnek DOAS: son 279.70, haftalık dip/zirve 271.10 / 325.81, değer 15.72. Eşik yok (1696021655947018369, 2023-08-28).
- **Olgunluk:** çekirdek.

### 1.8 Gann fanı
- **Ne yapar:** Fan çizgilerini trend teyidi ve destek olarak kullanır.
- **Parametreler:** Fan açıları 1/8 … 8/1. SAYAS: fiyat 1/2 fanı içinde. 0.236 Fibo (86,275) kırılırsa 3/1 fanına geçiş = düşüş trendi teyidi (1767689603035640165, 2024-03-12). Sonraki destek EMA200 = 3/1 fanı üst çizgisi (1767689605325684841, 2024-03-12). 2023-05-03 dibinden çizilen fanda 8/1 çizgisi destek, hedefler 4,92 ve 5,55; hesap yazılı değil (1771838096432099715, 2024-03-24).
- **Olgunluk:** fikir.

---

## 2. Genişletmeler (R kaydı başına)

### 2.1 Harmonik (a)
- **R008:** Defterde harmonik araç etiketleri var (D [TAMAMLANDI]/[AKTİF], X→B kırılımı). → X gönderileri eski tarayıcı kartının alanlarını ekliyor. Kart sayıları XA / AB / BC / CD bacak fiyat farkıdır, oran değildir. Kartta iki çizgi var: Fibo 0.618 ve 0.786 = D − r × |CD|. Örnek MACKO: 110.5 − 0.618 × 9.50 = 104.63; 110.5 − 0.786 × 9.50 = 103.03 (görsel doğrulandı). Adı verilmeyen bir kartta AB > XA (XA 0.25, AB −0.56); "onayını almış" der, onay tanımı yok (1898707683152220197). Kaynak: 1899198147823366265, 1870627477254721649, 1898707683152220197.
- **R011:** Defterde "Gartley taramasını ayrı yapın butterfly taramasını ayrı yapın" var. → Tarayıcı 10 türü ayrı seçenek olarak sunar, ayrıca [11] TÜM FORMASYONLAR ve [0] çoklu seçim var. Evren 521 hisse (1977815566183497963). Not: [11] seçeneği R011'deki "konsolide etmek" uyarısıyla gerilim taşır; bağlam belirsiz.
- **R013:** Defterde X–B trend çizgisi kırılımı var; yön eşlemesi açık değil. → Bullish Gartley'de kırılım yönü AŞAĞI. Kırılım "son 10 günde" aranır. Örnek: D 15.90, 0.786 = 15.68, kırılım 2026-08-13 (2091451219659104540).
- **R014:** Defterde 10 günlük tepki penceresi ve SAYAS işlem yönetimi var. → Çalışılmış örnek: Giriş D = 144.20 − 0.786 × (144.20 − 20.60) = 47.05. İlk Stop X = 20.60. TP1 (1:1) = 47.05 + (47.05 − 20.60) = 73.50. TP2 = 47.05 + 0.618 × (144.20 − 47.05) = 107.09 (2091220738510332198). Ek: D'den sonra fiyat A'yı (0.000 = 5.63) yukarı kırınca araç "GÜÇLÜ TEYİT (A kırıldı)" ve "trend hızlanması" der; D 0.786 = 4.14 (2092318619321446897). Bu A kırılımı D sonrasıdır; R019'daki A ihlali C–D arasıdır ve bozulma sayılır.
- **R016:** Defterde "CD bacağının şiddetini ne belirler?" sorusu var. → Tansu bir takipçinin cevabına (AB bacağının oluşum süresi) "kesinlikle doğru" der. "time management açısından daha önemli" ikinci bir ölçüt de var; adı yok, sayı yok (2091066263594295378).

### 2.2 Harmonik (b)
- **R075 / R076:** Defterde Siyah Kuğu + talep bölgesi, Beyaz Kuğu + sell AB=CD var. → Kuğu kartlarında BC > AB ya da AB > XA. Fibo çizgileri D − r × |CD|. CEMTS (XA 0.77, AB −0.35, BC 1.01, CD −0.42; Fibo 8.65 / 8.58). BVSAN (XA 14.70, AB −5.40, BC 10.45, CD −9.65; Fibo 82.54 / 80.92). Haftalık NUHCM (XA 28.50, AB −20.25, BC 63.25, CD −25.50; Fibo 281.74 / 277.46). Haftalık AVTUR (XA 3.39, AB −2.31, BC 5.91, CD −5.52; Fibo 8.08 / 7.15).
- **R075 / R076 (devam):** R076 kartı: XA 1.72, AB −2.24, BC 1.30, CD −1.34; Fibo 13.29 / 13.07 (1876682058896224584). White Swan kartı: XA 0.28, BC 0.19, CD −0.34; Fibo 2.43 / 2.37; 05.03'te tamamlandı, kısa vadeli kâr alındı, oran yok (1898001029884485900). MACKO çizgilerinin ikisi de X'in (105.0) altında (1899198147823366265; görsel doğrulandı). Kaynak: 1870627477254721649, 1871624647734923639, 1871631845055685007, 1891203604557463891.
- **R090:** Defterde D = B × C / A (Lindsay Trident) var. → Araç kanal desteğine ±%2.0 bant çizer. "Gerçek D − Teorik D" farkını ayrıca gösterir: 1496.00 − 1453.00 = 43.00 (%2.96). A 1985.00, C ≈1950, B ≈1480 ile B × C / A ≈ 1454; B ve C grafikten yaklaşık okundu (2096219752695816530).

*Devam:*
- **R203:** Defterde TP1–TP4 = D + (C − D) × 0.382 / 0.618 / C / 1.272 ve "X noktası altı geçersiz" var. → Üç çalışılmış örnek formülü doğrular (görsel doğrulandı):
  - Gartley KUYAS: C 70.00, D = 70.00 − 8.00 = 62.00; TP1 65.06; TP2 66.94; TP3 70.00; TP4 72.18. X = 70.00 − 4.90 + 8.10 − 12.70 = 60.50 = STOP (2090515278199136740).
  - Derin Yengeç CCOLA: D = 90.05 − 9.70 = 80.35; TP1 84.06; TP2 86.34; TP3 90.05; TP4 92.69. STOP 78.89, X'te değil, demand kutusunun üst kenarında. Teyit: talepten başlayan hareket için düşen trend kırılımı (2089770598620713304).
  - Kelebek DERIM: D = 39.50 − 4.62 = 34.88; TP1 36.64; TP2 37.74; TP3 39.50; TP4 40.76. STOP 34.19, D'nin 0.69 altında, demand kutusu içinde (2090514210228740261).
- **R221:** Defterde Gartley D + FVG ve teyit göstergeleri (yorum düzeyinde) var. → Gartley D teyit listesi: yutan boğa mumu, RSI(14) > 50, artan hacim, güçlenen trend (ADX(14) panelinde 25 çizgisi), MACD (1998449727399145947).
- **R222:** Defterde AB = 0.618 XA, D = 0.786 XA, %3–%5 tolerans var. → PETKM kartı kurala uyuyor: AB/XA = 1.48 / 2.34 = 0.632; D geri çekilmesi 1.81 / 2.34 = 0.774. D altındaki Fibo 0.618 = 16.76 ve 0.786 = 16.51, ikisi de X'in (≈17.14) altında (1879266462432706615). Kurala uymayan kartlar için Bölüm 3.1'e bakın.

### 2.3 Harmonik (c) ve Fibonacci
- **R250:** Defterde DOAS kelebeği var, D = XA'nın 1.272 uzantısı, 1.618 "max risk". → Swing pivot penceresi 15 gün. Endekse (XU100) uygulanır. D hedefi = 12966.30 + 1.272 × (15204.90 − 12966.30) = 15813.80. Max risk 1.618 = 16588.36 (2091947979921891468). Eski kartlarda D uzantısı: EGGUB 1.67 (1871626708304150884), 1.06 (1879995899432301062), IHEVA 1.14 (1883641498564264218). IHEVA Fibo 0.618: 2.28 = 2.48 − 0.618 × 0.32; 0.786: 2.23.
- **R020:** Defterde 1.272 / 1.618 / 2.0 uzantıları var. → 138.2% uzantı seviyesi; görselde 161.8% de çizili; son mum 138.2%'ye ulaşıyor (1950637105606173073).
- **R040:** Defterde "bağımsız faktör" confluence ilkesi var, sayı yok. → Elliott iç/dış sayım hedefi etrafında %5'lik Fibo sapma alanı = confluence alanı (2086920060254212344).

*Devam:*
- **R149:** Defterde confluence (talep/arz + Fibo + EMA + hacim) var, metin yok. → Fibo son 6 ay verisiyle çizilir (bkz. Bölüm 4). Fibo seviyesi ile EMA200 aynı noktadaysa güçlü tepki beklenir. Yakınlık eşiği yok (1842203367826706883).
- **R217:** Defterde Fibonacci'nin statik kullanımı eleştirisi ve konfluans var; kod yok. → Kod: `period='1y'`, kapanış max/min. Seviye = max − oran × (max − min). Oranlar 0.236 / 0.382 / 0.618 / 0.786. EMA 10/20/50/100/200 (`ewm`, `adjust=False`). EMA ve Fibo değerleri direnç merdiveni olarak sıralanır. DOAS örneği: max 399.75, min 208.80; 0.618 = 281.74; merdiven 215.57, 219.02, 230.22, 245.53, 249.66, 258.28, 281.74 (görsel doğrulandı).
- **R217 (devam):** Pencere 1 yıldır, başlıktaki 6 ay yanlıştır (1844837554795008098). Önce 1 ya da 2 yıllık grafiğe bakılır. Fibo başlangıç tarihi vadeye göre seçilir. "144 bar iyi" (1908510592639398132). Kaynak: 1842212999169253445, 1844836756501471622, 1847621973553144140.

### 2.4 Elliott
- **R193:** Defterde Elliott "Hedef (Wave 5)" çizgisi var, hesap yok; Hikkake yalnız ad. → 5. Dalga Hedef (W3 × 0.618) = 212.92 TL; Impulse (1-3) +59.0%; 4. dalga düzeltmesi −14.7%; formülün tabanı görselde yok (1984338420769177613). 5. dalga hedef bölgesi = 1.618 X (P1'den) ile 0.618 Y (P3'ten) kesişimi; ENJSA 93.73–103.03 TL; Fibo %49.2; X ve Y bacak tanımı yok (2000274228516413714).
- **R193 (Hikkake):** İç bar = mum önceki mumun gövde ve fitili içindedir. Ardından aşağı sahte kırılım, birkaç gün içinde yukarı dönüş = alım. Stop iç barın altı. Teyit: kırılım mumunun hacmi ve büyüklüğü, RSI/MACD, hacim artışı, EMA 8 ya da EMA 21 desteği. Düşük volatilitede daha anlamlı. Gün sayısı ve hacim eşiği yok (1913982654933848532).
- **R205:** Defterde 4. dalga = 3. dalga × 0.24 / 0.38 / 0.50 var. → Araç oranları: Wave 2 Retracement %86.4, Wave 4 Retracement %52.8 (0.50 sınıfı), Wave3/Wave1 2.69, Wave5/Wave1 1.44, C/0-5 %110.4. C teyidi = yeni dip gelmemesi + BOM sinyali (2094008240824635656).
- **R261:** Defterde Elliott 2. dalga + demand çakışması, iki giriş türü var. → 3. dalga başlangıcı = fiyatın 1. tepe (B) seviyesini yukarı geçtiği gün (ASGYO, B ~13.1, başlangıç 2024-07-17; 1947614735068770788). Tarama penceresi: son 3 gün içinde 3. dalga başlangıcı (1950944201924845870).

### 2.5 Bölge: arz/talep, FVG
- **R037:** Defterde distal ve proximal çizgi şeması var. → Proximal çizgi = base bölgesi içindeki en düşük gövde fiyatı, yani min(open, close). Mum rengi önemsizdir. Gap'li açılışta çizgi daha aşağıdaki gövdeden çekilir (2088907925704110444, 2088908047590502894).
- **R129:** Defterde FVG mıknatıs ve OTE var. → En yakın FVG'ye yüzde uzaklık ölçülür; %0.00 = "TEMAS" etiketi (1989089558164873727).
- **R168:** Defterde trend desteği + demand + FVG + BOS var (görselden). → Stop: trend çizgisi altı (≈45–46 TL) kalıcı kapanış. Teyit: MACD yukarı kesişim + RSI aşırı alımda değil + fiyat EMA üstü. Hedef eski zirve 50 TL ve üzeri (2016244555516150121).
- **R204:** Defterde 0.618 (ya da 0.50) + FVG çakışması var. → Fibo çekildikten sonra yükselen trend desteğine yakın FVG fiyat hedefidir. Bu FVG 0.618 alanındaysa (örnek 185.51) güçlü hedeftir ve trend desteği kırılır (2002147457422307730).
- **R258 / R255:** Defterde WMA21, MACD, RSI 45.0, WaveTrend yorumu var. → Görsel parametreler: WMA Close 21; MACD 12 26 9; RSI 14 70/30; WT 10 21 | 60 53 −53 −60. Bölge durumları DEMAND/TOPLAMA ve DEMAND/TEST EDİLDİ (191.40–192.75). YÜKSELEN TREND 265.50 TEMAS 4 (2094842420387029311).

### 2.6 Kanallar
- **R246:** Defterde "80-100 haftalık yatay giden bir hisse dibinde oturup bekleyeceksin" var; yataylık ölçüsü yok. → Tarama çıktısı: "<n> hafta yatay (alt − üst)", "% değişim" = üst / alt − 1, başlangıç idx (görsel doğrulandı: OFSYM 52 hafta 33.94–43.92, %29.40). Örnek süreler 27, 34, 37, 50, 52, 65, 104 hafta. Kırılım teyidi: "önceki hafta breakout, son hafta teyit" (AYCES 34 hafta 386.25–500.50, %29.58; görsel doğrulandı).
- **R246 (devam):** Giriş kanal desteğinde (1949055258195378520: 52 hafta 6.34–8.06, %27.13). Haftalık kanalda dipten tepeye işlem örneği (1956028500407619964: 27 hafta 24.76–33.10, %33.68). 65 haftada üst temas U1–U4, alt temas L1–L4 (2096651255514821058). 53 haftalık kanal dibinden yukarı hareket tetiği (2045431237335036123). Kaynak: 1942198658486686133, 1943009441273487705, 1949048313266721141, 1962962557699871050, 1963314020007776602.
- **R082 / R051 / R124 / R225:** Defterde konsolidasyon süresi ↔ kırılım şiddeti var. → Günlük yatay kanal kuralı: son 2 ay içinde 7–30 gün süren, (max − min) / min < %10 bant (AKMGY 30 gün 183.30–200.00, %9.11; görsel doğrulandı). Yukarı hacimli kırılım = alım, aşağı = satım. Bant içinde büyük pozisyon yok. Stop bandın hemen dışı. AKD: üst bantta satış yığılması direnç, alt bantta alış yığılması destek, kırılım öncesi kademe çekilmesi. Takas: kurumsal/yabancı/fon alımı kırılımı destekler, yalnız bireysel yoğunlaşma = fake kırılım (1939569795696922684). Ek örnek: 25 hafta 101.00–112.60 (%11.5), kırılım barı 2025-07-21, SMA 20W, VWAP, Vol MA 20W (2049157737360065010).

*Devam:*
- **R245:** Defterde 120 barlık yükselen kanal etiketi var. → 60 barlık kanal ve "DESTEK YAKININDA" etiketi (destek 10072.40, fiyat 10110.00; 1984032255535443993). 90 bar; "İçeride kapanış %100.0"; Üst/Alt 3/3; Low-Bant +0.09%; Genişlik değişimi −27.8% (2097010207821877561).
- **R214:** Defterde EMA5 > EMA8 > EMA13 + yükselen trend desteğine temas var; temas ölçüsü yok. → Temas = son gün fiyatı ≈ trend çizgisinin son gün değeri (13.87 / 13.85, fark ≈ %0.14; 1951645372041806086). Lookback 30 / 35 / 40 gün, durum "TAKİP ET" (1952069518538481977). ADX(14) 20 çizgisi ve RSI(14) 50 çizgisi referans (1986488325180432605).
- **R244 / R001:** Defterde "Medyanı şöyle bir kanal gibi kullanın" var. → Bant = medyan ± 1 standart sapma (2093084917080924363).

### 2.7 Çizgiler, pivotlar, ATR
- **R039:** Defterde Swing Pivot ve Regresyon/Zarf yöntemleri var; periyot yok. → Trend çizgisi 72 günlük lookback (1875902526824030471). Trend çizgisi benzer büyüklükteki pivotları bağlar; kanal karşı taraftaki pivottan paralel çizgiyle kurulur (2096653615624810555). Zarf: destek = min eğimli, direnç = max eğimli çizgi; pencere son 45 mum (1952070959529336857) ya da 27 mum (1952071338971091397). Regresyon kanalında BUY alt bantta, SELL üst bantta; pencere yok (1873520948949008581).
- **R039 (ATR zigzag ve pivot):** Dip: son tepeden ATR kadar düşüş, ardından yukarı dönüş. Örnek tepe 100, ATR 2.5, eşik 97.5, dip 97.0. ATR periyodu yok (1911038743839900154). Pivot ölçütleri: gövde kalınlığı, iğne uzunluğu, önceki mumla mesafe, sol/sağ bar sayısı; sayı yok (1764349976069501071).
- **R221 (ATR + AKD):** → Dip: −3 ATR sert düşüş, −2 ATR civarında toparlanma, birkaç gün karışık kırmızı-yeşil. AKD 1 hafta: ilk 5 kurum satışa geçmiyor, ilk 5 payı %40–60, ilk 2 payı %60–70. Takasta toplulaşma. Emeklilik fonu ağırlığı güçlendirir (1964644641208222079).
- **R191:** Defterde günlük pivot P, R1–R3, S1–S3 kodu var. → R4 = R3 + (R2 − R1); S4 = S3 − (S1 − S2). `under_X = Close < X` bayrakları. BIST30, 2023-07-17'den (1848461886192271748). Pivot haftalık uygulanır; 2 ATR üstüne atan endekste ilk hedef R2 = 11219 (1957867341552971801).
- **R055:** Defterde Talep + HSAR kesişimi var. → Kaynak kitap: Tsinaslanidis & Zapranis, *Technical Analysis for Algorithmic Pattern Recognition*. Seviyeler regional high/low noktalarından. n = seviyeye düşen regional high/low sayısı (FROTO n=2; GC=F 3,427.27 n=3). Tolerans ve pencere yok (2086822816695918859, 2086827188788035838).

### 2.8 Klasik formasyonlar
- **R114:** Defterde fincan Fibo %100 = dip, %0 = sağ ağız; hedef 389.30; "hangi tabana eklendiği yazılmamış" var. → Hedef = kırılım + (kırılım − fincan dibi): 300.75 + (300.75 − 212.20) = 389.30 (GUBRF, görsel doğrulandı; 2047238753366761631). NTHOL: KIRILMA 47.50, HEDEF 60.82 = 47.50 + (47.50 − 34.18) (görsel doğrulandı; 1986961469393473699). Stop kulp altında 10.41; giriş = fincan kenarları çizgisinin geçilmesi (1986946515508543529).
- **R114 (devam):** Araç alanları: durum RETESTTE / TETİKLENDİ, Kalite /100, R/R, Hacim x, Fib %38.2 ve %50. ALARK: Kalite 65.0/100, R/R 1:2.54, Hacim 0.77x, Kırılım 99.15, Hedef 122.02, Stop 91.13, Fib %38.2 90.41, Fib %50 87.71 (görsel doğrulandı; 2095610529330905560). "İşte setup budur" = kırılım sonrası retestte giriş. "Retest kaliteyi arttırır" (2095921661098836095: Kalite 63.5, R/R 1:1.70, Hacim 1.29x, Kırılım 48.60, Hedef 56.03, Stop 45.18).
- **R127 / R128:** Defterde EMA sıkışması (Tolerans %1.2, Min 3 gün) var. → Yükselen üçgen: EMA yakınlığı (10 ve 20 günlük EMA; eşik yok) + en az 2 yakın tepe (yatay direnç) + 3 ya da daha fazla yükselen dip; direncin yukarı kırılımı = alım (1952086678639669635). Tarama penceresi son 3 gün; ek filtre yükselen trend desteğinden tepki (1952092703740866703, 1952093418366112014). Kırılım = üst çizginin üstünde kapanan bar; kırılım barında hacim ortalama çizgisi üstünde; geri dönüş düşük hacimle; hedef = üçgen taban yüksekliği yukarı projekte (1954300245707497649).

*Devam:*
- **R128 (KDE):** Defterde KDE penceresi 150 mum var. → 50 mum = kısa vade, 100 mum = orta vade (1952908597480075631, 1952908601275699243).
- **R219:** Defterde OBO kuralları var. → TOBO (aynası): onay = haftalık kapanış boyun çizgisi üstünde. Hacim sol omuzdan başa azalır, sağ omuzdan boyuna artar, kırılımda yüksektir. Boyuna pullback = ikinci alım fırsatı. Hedef = kırılım + (boyun − baş); örnek Baş 20, Boyun 30 → Hedef 40. Sağ omuz oluşmadan alım erkendir (1913995238978277848). Haftalık TOBO geriye dönük kontrol: "Hiç getirmeyen haftalıkta %30-40 arası getirmiş"; örneklem sayısı ve tutma süresi yok (1900332136906784924).
- **R006:** Defterde "Takoz olur" (yalnız ad) var. → Takoz metrikleri: Skor 99.0/100, çizgi üstü %2.19, daralma %77.0, içeride %93.3, temas 5+3, hacim 2.16x (Hacim MA20'ye göre), Teyit EVET. Eşikler yazılı değil (2095927899249406462).

### 2.9 Bayrak, Bollinger, mum, momentum
- **R007 / R004:** Defterde "bayrak flama olur" (yalnız ad) var. → Haftalık boğa bayrak; araç direği ve kanal çizgisini çizer, kırılım tarihi 2025-03-10 (1900554823331635298). Tarayıcı alanları: tip Yükseliş Bayrak, kırılım fiyatı 87,70, kırılımdan uzaklık 0,0%, RSI(14) 45,1, hacim değişimi +98,6% (2096025629770571980).
- **R190:** Defterde 2. ya da 3. sapmada ortalamaya dönüş var. → BB 3 SS, ortalama 20EMA; üst banttan ortalamaya dönüş hedefi 317–318 (1778707323147448589). 60 dk, BOL(20,3), hedef 20 periyot ortalama (1786749759627133185).
- **R023 / R171:** Defterde bullish engulfing kodu ve "fikirlerinizi test edin" ilkesi var. → Bearish engulfing kodu: `Open > önceki Close`, `Close < önceki Open`, önceki mum yeşil. Rejection: karşı fitil > gövde × 5, aynı yön fitil < gövde / 10. Ölçüm: sinyalden sonraki mumun yönü. BTC-USD günlük 2022-04-1 – 2024-02-27; 38 sinyal, %68.42 yükseliş, %31.58 düşüş (görsel doğrulandı; 1762402307503780152, 1762402303221346600). Dizilim EMA5 > EMA8 > EMA13 > EMA34 + bullish engulfing; teyit hacim, RSI 30'dan çıkış ya da MACD, EMA34 kırılımı, ikinci gün devam (1923069231043838440).

*Devam:*
- **R208:** Defterde confluence ilkesi var. → RSI'ın iki tepe arasındaki düşen trend çizgisi son gün yukarı kırılır + aynı gün TA-Lib BELTHOLD. Stop: mumun altı. Hedef: 2–3 gün momentum takibi ya da önceki dirençler. Sonuç birkaç günde %5 (1911135810839105880, 1911146678016504174).
- **R241:** Defterde "inverted hammer pastanın üzerindeki çilektir" var. → CDLINVERTEDHAMMER: düşüş trendi sonrası, kısa gövde, uzun fitil; RSI pozitif uyumsuzluk ile birlikte dönüş sinyali; oran eşiği yok (1910746404265279494).
- **R105:** Defterde ortalama eğimi var. → EMA20 (15.64) destek; RSI 50 altına inme = momentum kaybı; gönderi kesik (1778359964634915038).

---

## 3. Çelişkiler

### 3.1 Gartley tarama kartları R222 / R203 oranlarına uymuyor
**Defter tarafı (R222, 2026-08-28 11:27):** "AB Bacağı (Düzeltme): XA bacağının tam olarak %61.8 ($0.618$) seviyesine kadar geri çekilmelidir. Bu, Gartley'i diğer harmoniklerden ayıran en kritik kuraldır" ve "CD Bacağı: XA bacağının %78.6 geri çekilme seviyesinde sonlanmalıdır", tolerans "%3-%5". R203 (2026-08-28 08:41): "X Noktası Altı: ...formasyon geçersiz sayılır (Invalidation)."

**Gönderi tarafı (kartlar "Bullish Gartley Found for …", 2024-12 – 2025-02; KUYAS 2026-08):**
- ALCAR 1871623972544274600 (2024-12-24): XA 93.50, AB −63.00, BC 47.00, CD −68.50 → AB/XA 0.674; (A − D)/XA = 84.5 / 93.5 = 0.90.
- DIA-USD 1873451580521099741 (2024-12-29, haftalık): XA 0.75, AB −0.42 → AB/XA 0.56; D 0.64.
- POLS-USD 1877652247015764086 (2025-01-10, saatlik): AB/XA 0.71; D 0.87 (noktalar görselden yaklaşık).
- BINHO 1879264702431387933 (2025-01-14): AB/XA 0.624 (uyar); D 0.70.
- BIZIM 1884657021883949099 (2025-01-29): AB/XA 0.69; D 0.75.

**Gönderi tarafı (devam):**
- ARENA 1888626133933121609 (2025-02-09): XA 6.18, AB −4.34, BC 3.30, CD −5.20 → AB/XA 0.70; (A − D)/XA = 6.24 / 6.18 = 1.01. Bacaklardan D − X = 6.18 − 4.34 + 3.30 − 5.20 = −0.06, yani D X'in altındadır (görsel doğrulandı). R203'e göre bu yapı geçersizdir.
- TTKOM 1892643772430766103 (2025-02-20): XA 4.22, AB −2.50, BC 1.80, CD −2.12 → AB/XA 0.59 (uyar); D 2.82 / 4.22 = 0.67 (görsel doğrulandı).
- KUYAS 2090515278199136740 (2026-08-20, satır `genisletir`): X→A 12.70, A→B 8.10, B→C 4.90, C→D −8.00 → AB/XA 0.638 (uyar); (A − D)/XA = 11.20 / 12.70 = 0.88 (bu belgede hesaplandı; görsel doğrulandı). 0.786'nın dışında.
- Uyan kart: PETKM 1879266462432706615 (2025-01-14): 0.632 / 0.774.

**Kart sayılarının anlamı:** Kartlardaki XA / AB / BC / CD değerleri oran değil, bacak fiyat farkıdır. Kartın iki çizgisi "Fibo 0.618" ve "Fibo 0.786" = D − r × |CD| formülüyle D'nin altına çizilir. Doğrulanan örnekler: TTKOM 48.38 − 0.618 × 2.12 = 47.07; ARENA 32.75 − 0.618 × 5.20 = 29.55; MACKO 110.5 − 0.618 × 9.50 = 104.63. Bu çizgiler ne R222 girişi (D = X + (A − X) × 0.786) ne de R203/R222 hedefleridir (D'nin üstünde). Çizgilerin işlevi yazılı değil (1870627477254721649 notu): belirsiz.

**Olasılıklar:**
- **Tarihçe:** Kartlar eski tarayıcının çıktısıdır (2024-12 – 2025-02, "Found for" başlıklı grafik). R222 ve R203 2026-08'de yazıldı. 2026-08 aracı (SAYAS, 2091220738510332198) girişi tam 0.786'ya koyar. Kanıt: tarih sırası ve iki farklı araç görünümü. Ama KUYAS (2026-08-20) yeni araçta da 0.88 verir; bu, tarihçe açıklamasını zayıflatır.
- **Hata:** Tarayıcı toleransı çok geniş olabilir ya da D'yi X'e göre denetlemiyor olabilir (ARENA). Kanıt: ARENA'da D < X iken "Gartley Found" yazar.
- **Bağlam:** Tansu "Her gartley çalışmaz ama çalışmasa bile oluşumunda bazı stratejiler kurgulanabilir" (R014) ve "Her harmonik %100 çalışır diye de bir kaide olamaz" (R024) der. Kartlar aday listesi olabilir. Kanıt yok: belirsiz.

**İlgili harmonik kart notu:** EGGUB Butterfly kartında D, XA'nın 1.67 uzantısındadır (1871626708304150884, 2024-12-24). R250 (2026-09-06) 1.618'i "max risk" diye etiketler. Bu bir çelişki adayıdır; satır `genisletir` işaretlidir.

**Hedef formülü notu (defter içi):** R203 hedefleri (C − D) üzerinden, R222 hedefleri (A − D) üzerinden hesaplar. R014 TP2'si de ".618 AD"dir. KUYAS örneği (2090515278199136740) R203 formülünü kullanır. Hangi aracın hangi formülü kullandığı belirsiz; SAYAS başlığında "Sistem: Carney" yazar.

### 3.2 FVG "subjektif" — R199
- **Gönderi (1893637273029050563, 2025-02-23):** "ben çok sevmiyorum bu işleri aslında. biraz subjektif geliyor bana"; hassasiyet ayarı subjektif; AKBNK'ta 16 FVG bölgesi.
- **Defter (R199, 2026-08-28 08:02):** "buradaki kurumsal ayak izlerini (FVG) giriş sinyali olarak kullanır"; "1. mumun en yükseği ile 3. mumun en düşüğü arasında boşluk kalmalı".
- **Sonra gelen:** defter.
- **Olasılık:** Tarihçe. Kanıt: 2025-11 ve 2025-12 gönderileri FVG'yi araçta kullanır ("TEMAS FVG (0.00% Uzaklık)", 1989089558164873727; FVG 0.618 hedefi, 2002147457422307730).

### 3.3 ATR dip/tepe alım-satım bölgesi — R172, R111
- **Gönderi (1927454690960101506, 2025-05-27):** "Dip ➡️ Alım bölgesi / Tepe ➡️ Satış bölgesi" ve "Biz burada train/test bölmedik".
- **Defter (R172, 2026-08-28 05:21):** "Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR." **R111 (2026-08-27 23:42):** "sabırla backtest ve forward test süreçlerini yönetmeniz gerekir".
- **Sonra gelen:** defter.
- **Olasılık:** Bağlam olabilir. Dip ancak dönüşten sonra onaylanır; bu, gerçek zamanlı dip tahmini değildir. Satır çelişkiyi "kısmi" sayar. Level 1/2 gönderileri de noktaların "sinyal olarak" görülmemesini ister (1909002131635331358). Tarihçe olasılığı da var: belirsiz.

### 3.4 Çarpan + İNA ağırlığı — R151, R068
- **Gönderi (1769794170590245323, 2024-03-18; 1787051924061118650, 2024-05-05):** TTRAK 2023/4Ç tablosu: "ÇARPANLARA VE İNA'YA GÖRE ORTALAMA FİYAT 1,539.90" (çarpan 1,620.53; İNA 1,486.14). Hesap: 0.4 × 1,620.53 + 0.6 × 1,486.14 = 1,539.89, yani İNA %60. Ters ağırlıkla sonuç 1,566.77 olur.
- **Defter (R151, 2026-08-28 02:59):** "İNA'sonucunun %40'ı, basit çarpan değerlemesi ve detaylı çarpan değerlemesinin ortalamasının %60'ı". **R068 (2026-08-27 20:58):** "En sonunda bu ortalamanın %60'ını, DCF'in de %40'ını alırım."
- **Sonra gelen:** defter.
- **Olasılık:** Tarihçe (kod sonra değişmiş olabilir) ya da hata (eski kodda ağırlıklar ters bağlanmış olabilir). Kanıt: R068'in örneği de "2024 mart ayında gelen 2023 sonu bilançosu" dönemidir, yani gönderiyle aynı dönem. Bu, tarihçe açıklamasını zayıflatır. Örneğin aynı hisse olup olmadığı belirsiz.

### 3.5 Harmonik paylaşımda destek-direnç — R009, R024
- **Gönderi (1892640823361098050, 2025-02-20):** "Ben destek direnç vs vs bakmam. Gartley butterfly çıkarsa veririm."
- **Defter (R009, 2026-08-27 17:01):** "bu akşam iyi bir formasyon bulursam, böyle tam arz talep bölgesinde vereceğim". **R024 (2026-08-27 17:59):** "Destek ve dirençlere bakıyoruz Hacim ayak izine bakıyoruz".
- **Sonra gelen:** defter.
- **Olasılık:** Tarihçe. Kanıt: 2026-08 araç görselleri harmonik ile demand/supply'ı aynı grafikte verir ("Derin Yengeç Formasyonu + Demand/Supply Analizi", 2089770598620713304; "Gartley Formasyonu + Demand/Supply Analizi", 2090515278199136740).

### 3.6 Elliott C yerine 3. dalga — R199
- **Gönderi (1950934573468025012, 2025-07-31):** "Elliot C taraması değil, 3.itki dalgası taraması yapın. Getirileri daha iyi." Sayı yok.
- **Defter (R199, 2026-08-28 08:02):** "FVG kutusunun üst bandına veya %61.8 seviyesine 'Limit Alış' emri" (giriş C bölgesinde).
- **Sonra gelen:** defter.
- **Olasılık:** Bağlam. R261 (2026-09-06) iki girişi de kabul eder: agresif = bölgede, muhafazakâr = direnç kırılımı. Getiri iddiasının kanıtı yok: belirsiz.

---

## 4. Tansu'nun gönderi içi hataları ve defter okuma hataları

### 4.1 Formül ve kod hataları
- **Fibo kodu (1847621973553144140, 2024-10-19):** `fourth_level = max_value * difference * 0.618` yazar; eksi yerine çarpı vardır. İkinci blokta doğru formül var. Düzeltme: `max_value - difference * 0.618`.
- **Tasuki kodu yorumu (1905592381618962842, 2025-03-28):** Yorum "# 3. mum, 2. mumdan daha aşağıda açılmış" der. Kod ise `data[i, close_column] < data[i - 1, open_column]` ile kapanışı denetler (görsel doğrulandı). Üçüncü mumun açılışı denetlenmez. Nedeni belirsiz.
- **Shrinking ayı kodu (1906298048017264857, 2025-03-30):** Kodda `L[i-1] > L[i-2] > L[i-3]` koşulu var (görsel doğrulandı). Metin (1906298044510879769) bu yükselen dip koşulunu söylemez.
- **Quintuplets (1905940770281910507 ↔ 1919053643946303495):** Kod "Aynı gün" sinyal verir (görsel doğrulandı). Sonraki metin "bir sonraki gün alım" der. `body` değeri iki gönderide de yok.

### 4.2 Metin–görsel uyuşmazlıkları
- **Fibo penceresi (1844836756501471622 ↔ 1844837554795008098, 2024-10-11):** Başlık 6 ay der, kod 1 yıl kullanır. Tansu düzeltir: "Pardon 1 yıllık. başlığı değiştirmemişim". 1842203367826706883 (2024-10-04) de "Son 6 aylık veriler" der. Aynı gün DOAS görseli 2023-10 – 2024-09 aralığını gösterir (görsel doğrulandı). Bu gönderinin 6 ay mı 1 yıl mı kullandığı belirsiz.
- **Zarf kanalı (1952070959529336857, 2025-08-03):** Metin 30 gün der, görsel "Son 45 mum" der.
- **3. dalga taraması (1950944201924845870, 2025-07-31):** Başlık "SON 3 GÜNDE 3. DALGA BAŞLANGICI" der; çıktıdaki tüm tarihler 2024-07-30'dur.
- **Keltner (1852451504705155208, 2024-11-01):** Kanal Keltner diye anılır; görsel etiketleri DC_UP/DC_DOWN'dur (Donchian adlandırması). Hangi kanal olduğu belirsiz.
- **ALARK R/R (2095610529330905560, 2026-09-03):** Kart R/R 1:2.54 yazar. Kırılım 99.15 giriş sayılırsa (122.02 − 99.15) / (99.15 − 91.13) = 2.85 çıkar (bu belgede hesaplandı). Giriş fiyatı yazılı değil: belirsiz. Fib %38.2 = 90.41 ve %50 = 87.71 değerlerinden fincan aralığı 76.27–99.15 çıkar; hedef 99.15 + 22.88 = 122.03 ile uyuşur.

### 4.3 Kart adlandırma tutarsızlıkları
- "Gartley" adlı kartların çoğu R222 oranlarına uymaz; ARENA'da D < X (Bölüm 3.1).
- Adı olmayan kart (1898707683152220197): AB > XA; "onayını almış" der, onay tanımı yok.

### 4.4 Defter okuma hataları
- **R014 TP2 (2091220738510332198):** Görsel "TP2 (.618 AD)" yazar. Defter ".618 CD" diye kaydetmişti. `defter-1.md` R014 bugün (07.10) düzeltildi: "TP2 (.618 AD)", "İlk Stop (X)", 0.786: 47.05. `defter-fikir.txt` R014 satırı hâlâ eski metni taşır: "Bk Stop (X)", "TP2 (.618 CD)", "0.786: 47.10". Düzeltme: `defter-fikir.txt` R014 satırını `defter-1.md` ile eşitle.
- **R114 hedef tabanı:** Defter "hedefin hangi tabana eklendiği yazılmamış (389.30 − 104.80 = 284.50)" der. Okuma hatası değil, eksik çözüm. Taban = kırılım 300.75, derinlik = kırılım − dip = 88.55 (2047238753366761631; görsel doğrulandı).
- **Karşılaştırma girdisi notları (defter değil):** IHEVA için "yeniden üretilemedi" notu yanlış; formül D − r × |CD| (1883641498564264218). MACKO için "aralık çıkarılamadı" notu yanlış (1899198147823366265). RSI Fibo satırında `yontem_defterde: "var"` işareti defterle uyuşmaz (1986826801885167861).

---

## 5. Defter için öneri listesi

Sıra ölçütü: tam parametre, Tansu'nun kendi yöntemi, birden çok gönderide tekrar. İlk 10 maddede görsel parametreler Read ile doğrulandı. Uyuşmazlık: CCOLA formasyonu satırda "Crab", görselde "Derin Yengeç". Diğer değerler uyuştu.

### Öncelik 1–5
1. **genişlet R246 (+R082):** Yatay kanal tarama tanımı. Haftalık süre (örnekler 25–104 hafta), "% değişim" = üst / alt − 1, kırılım teyidi "önceki hafta breakout, son hafta teyit". Günlük tür: son 2 ay, 7–30 gün, (max − min) / min < %10, stop bandın hemen dışı, AKD/takas filtresi. Kaynak: 1939569795696922684, 1942198658486686133, 1962962557699871050, 1943009441273487705, 1949055258195378520, 1956028500407619964, 2049157737360065010, 2096651255514821058, 1949048313266721141, 1963314020007776602, 2045431237335036123.
2. **genişlet R203 (+R222, R014):** Çalışılmış TP örneklerini ve stop yerini ekle. Gartley'de stop X; Derin Yengeç ve Kelebekte stop demand kutusunda (D altı). Hedef tabanı farkını (C − D ile A − D) not et. Kaynak: 2090515278199136740, 2089770598620713304, 2090514210228740261, 2091220738510332198.
3. **genişlet R114:** Hedef = kırılım + (kırılım − fincan dibi). Retestte giriş, Kalite /100, R/R, Hacim x, Fib %38.2/%50 alanları. Kaynak: 2047238753366761631, 1986961469393473699, 1986946515508543529, 2095610529330905560, 2095921661098836095.
4. **ekle — Mum formasyonu kod kuralları:** Tasuki Gap, Shrinking, Quintuplets, Bottle, H, Slingshot koşullarını birebir yaz; eksik `body` eşiğini "belirsiz" diye işaretle. Kaynak: 1905592381618962842, 1906298048017264857, 1905940770281910507, 1905945897105531327, 1905960716571451830, 1905953875007357298, 1914394674921722043.
5. **genişlet R008 / R075:** Harmonik kart okuma kuralı. Kart sayıları bacak fiyat farkıdır; çizgiler D − r × |CD|; "Pattern completed on" tarihi. Kartların R222 oranlarına uymadığını uyarı olarak ekle (Bölüm 3.1). Kaynak: 1899198147823366265, 1888626133933121609, 1892643772430766103, 1870627477254721649, 1883641498564264218.

### Öncelik 6–10
6. **genişlet R217:** Fibo kodu: `period='1y'` kapanış max/min, seviye = max − oran × (max − min), oranlar 0.236/0.382/0.618/0.786, EMA 10/20/50/100/200 direnç merdiveni; 144 bar; önce 1–2 yıllık bakış. Kaynak: 1842212999169253445, 1844836756501471622, 1844837554795008098, 1847621973553144140, 1908510592639398132.
7. **genişlet R037:** Proximal = base içindeki min(open, close); renk önemsiz; gap'te alttaki gövde. Kaynak: 2088907925704110444, 2088908047590502894.
8. **genişlet R023 / R171:** Bearish engulfing + rejection kodu (fitil > gövde × 5, < gövde / 10) ve ölçüm (38 sinyal, %68.42 / %31.58). EMA5 > 8 > 13 > 34 + engulfing teyit listesi. Kaynak: 1762402307503780152, 1762402303221346600, 1923069231043838440.
9. **genişlet R219:** TOBO kuralları: haftalık kapanış onayı, hacim sırası, pullback = ikinci alım, hedef = kırılım + (boyun − baş). Kaynak: 1913995238978277848, 1900332136906784924.
10. **ekle — RSI üzerine Fibonacci:** RSI(14), 144 bar, 23.6/38.2/50/61.8; boğada 38.2/50 desteği, ayıda 50/61.8 direnci. Kaynak: 1986826801885167861.

### Öncelik 11–15
11. **ekle — Tepe/dip algoritması (Level 1 / Level 2):** Son 10 gün, Level 1 day trade, Level 2 trend takibi, repaint yok, grid search; dip taraması dereceleri. Kademe tanımı belirsiz. Kaynak: 1924944817441710378, 1909002131635331358, 1910423863822811223, 1950987288378519760, 2002099118366486932.
12. **genişlet R221 / R039:** ATR dip tanımı (−3 ATR düşüş, −2 ATR toparlanma; tepe − ATR eşiği) + AKD eşikleri (ilk 5 %40–60, ilk 2 %60–70). Kaynak: 1964644641208222079, 1911038743839900154.
13. **genişlet R208:** RSI düşen trend çizgisi kırılımı + aynı gün BELTHOLD; stop mumun altı; hedef 2–3 gün ya da önceki direnç. Kaynak: 1911135810839105880, 1911146678016504174.
14. **genişlet R127:** Yükselen üçgen: 2 yakın tepe, 3+ yükselen dip, kırılım barında hacim ortalama üstü, hedef = taban yüksekliği. Kaynak: 1952086678639669635, 1954300245707497649, 1952092703740866703, 1952093418366112014.
15. **genişlet R013 / R014:** Bullish yapıda X→B kırılımı AŞAĞI, son 10 gün; D sonrası A kırılımı = "GÜÇLÜ TEYİT". Kaynak: 2091451219659104540, 2092318619321446897.

### Öncelik 16–20
16. **genişlet R214 / R245:** Temas ölçüsü (fiyat ≈ çizgi), lookback 30/35/40, kanal 60/90 bar, "İçeride kapanış %". Kaynak: 1951645372041806086, 1952069518538481977, 1986488325180432605, 1984032255535443993, 2097010207821877561.
17. **genişlet R191:** R4 = R3 + (R2 − R1), S4 = S3 − (S1 − S2); haftalık pivot. Kaynak: 1848461886192271748, 1957867341552971801.
18. **genişlet R128:** KDE penceresi 50 mum (kısa vade) ve 100 mum (orta vade). Kaynak: 1952908597480075631, 1952908601275699243.
19. **çeşitlendir R008 / R011 — harmonik türleri:** Bat, Alt Bat, Cypher, Deep Crab, Shark ve 10 türlü tarayıcı menüsü. Kaynak: 1876368569438765488, 1877449919641833760, 1893684348391391620, 1872027142181232735, 1878174325863313704, 1977815566183497963, 2089770598620713304.
20. **genişlet R193 / R205 / R261 — Elliott:** 3. dalga başlangıcı = 1. tepe (B) geçişi; son 3 gün taraması; 5. dalga hedefleri (W3 × 0.618; 1.618 X ile 0.618 Y kesişimi); araç oranları. Kaynak: 1947614735068770788, 1950944201924845870, 1984338420769177613, 2000274228516413714, 2094008240824635656.

### Öncelik 21–25
21. **ekle — Göreli konum ve dipten uzaklık:** 16 günlük kayan max/min; dipten uzaklık % = (son − dip) / (zirve − dip), haftalık–12 aylık. Kaynak: 1775315669824700852, 1775315672647528494, 1696021655947018369.
22. **ekle — ATR bantları:** EMA26 ± k × ATR14 (k = 1, 2, 3), konum etiketleri. Kaynak: 1957877677777375736.
23. **çeşitlendir R143 — TA-Lib CDL taraması ve tek mumlar:** Belt Hold, Closing Marubozu, Asılı adam, Shooting Star, Dark Cloud Cover, Piercing. Kaynak: 1847992441699246587, 1907095706285826234, 2009318796025360724, 1982688365007794207, 1908505150668370269.
24. **çeşitlendir R039 / R053 — kanal ve ortalama türevleri:** Keltner, Vegas 30-109-150, T3, kanal orta noktası, dikdörtgen, range breakout, regresyon kanalı, zarf pencereleri (45/27 mum), trend çizgisi lookback 72. Kaynak: 1979691577632231774, 1835559479842070775, 1995924034911961480, 1914188571033940188, 1952070959529336857.
25. **genişlet — tek kaynaklı kalan R kayıtları:** Bölüm 2'deki R006, R007, R016, R020, R040, R055, R090, R105, R129, R149, R168, R190, R204, R241, R244, R250, R258 eklerini ilgili kayda yaz. Kaynak: Bölüm 2'deki id'ler.

### Öncelik 26–27
26. **ekle — Gann fanı (fikir):** 1/8–8/1 fan açıları; 3/1 fanına geçiş = düşüş teyidi; fan + EMA200 çakışması. Kaynak: 1767689603035640165, 1767689605325684841, 1771838096432099715.
27. **genişlet — çelişki kayıtları:** Bölüm 3'teki altı çelişkiyi ilgili R kaydına "tarihçe" notu olarak ekle (R222, R199, R172, R151/R068, R009/R024). Kaynak: 1871623972544274600, 1893637273029050563, 1927454690960101506, 1769794170590245323, 1892640823361098050, 1950934573468025012.
