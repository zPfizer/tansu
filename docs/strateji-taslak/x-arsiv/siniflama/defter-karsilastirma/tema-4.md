# TEMA 4 — Değerleme-temel, portföy, çift: defter öneri belgesi

Kaynak: `tema-4.jsonl` (201 satır: genisletir 99, cesitlendirir 55, yeni 27, celisir 19, ayni 1). Defter: `defter-fikir.txt`, `defter-1..4.md`. Defter kayıtları 2026-08-27 ile 2026-09-06 arasında tarihlidir. Bu temadaki X gönderileri 2023-08 ile 2026-09 arasındadır.

Görsel doğrulama: bu belge için 17 görsel açıldı (liste 4.3'te). Tarih biçimi: YYYY-AA-GG.

Kapsam notu: görevde örnek verilen "fon akışı/fon riski", "AKD/takas" ve "iflas skorları" aileleri bu temada yöntem olarak yok. "Takas" yalnız 1709805069644820609 kontrol listesinde bir ad olarak geçer. Altman ya da benzeri iflas skoru bu temada yok. Bu aileler başka temalardadır.

---

## 1. Yeni yöntem aileleri

Olgunluk: **tam** = formül ve eşik yazılı; **çekirdek** = adımlar belli, eşik ya da pencere eksik; **fikir** = yalnız ad ya da yön.

### 1.1 Esas faaliyet kârı (NEFK) – fiyat ayrışması (temel teyitli arbitraj)

Ne yapar: Net esas faaliyet kârı artan ama fiyatı artmayan hisseyi bulur. Çift sürümünde bu hisse, fiyatı artmış koreli bir eşle eşleşir.

- Parametreler (birebir):
  - 1941455577097306576: "1) İş Yatırım bilanço verisi Python ile; 2) satışı ve net esas faaliyet kârı artan ama fiyatı artmayan hisse; 3) eşi: EFK'si artan ve fiyatı yükselmiş, benzer korelasyonlu hisse; 4) korelasyon + eşbütünleşme; 5) sapmada farkın kapanması yönünde pozisyon". Eşik yok.
  - 1956737745528705173: "yüksek korelasyon + eşbütünleşme p < 0,05; iki şirkette de satış, net esas faaliyet kârı ve net dönem kârı artıyor; biri fiyatlamış, öbürü geride". Korelasyon eşiği ve sapma ölçüsü yok.
  - 1781333788556935603: "betalar eşit, yüksek pozitif korelasyon, iki hissede net esas faaliyet kârı artışı, birinde fiyata yansımamış".
  - 1889068388334370953 ve 1911030895248539760: NEFK↑ ve HBK↑ = olumlu; "NEFK düşerken HBK yükseliyorsa, dikkat: Bu kâr başka yerden geliyor olabilir".
  - 1917362530000986239: "fiyat ↑ + esas faaliyet kârı ↓ = değerleme riski; fiyat ↑ + esas faaliyet kârı ↑ = sağlıklı trend"; XU100 ile göreli kıyas; fiyat endeksi başlangıç = 1.
- Kaynak gönderiler:
  - Çift sürümü: 1781333788556935603 (2024-04-19), 1862514359622111242 (2024-11-29), 1862514363178811538 (2024-11-29), 1891144792211353762 (2025-02-16), 1941455577097306576 (2025-07-05), 1956737745528705173 (2025-08-16); sektör türevi 1949018697315524785 (2025-07-26).
  - Tek hisse sürümü: 1888814948886724906 (2025-02-10), 1889068388334370953 (2025-02-10), 1892680047779074122 (2025-02-20), 1893717988043342127 (2025-02-23), 1917362530000986239 (2025-04-29).
  - Kâr kalitesi: 1692269598073094408 (2023-08-17), 1774017615482032258 (2024-03-30), 1911030895248539760 (2025-04-12), 1911034541701050726 (2025-04-12).
  - Kontrol listeleri: 1698267718074438032 (2023-09-03), 1709805069644820609 (2023-10-05).
- Olay çalışması türevi 1941562469320884677 (2025-07-05): EFK artış = (son − önceki) / |önceki| (IHLGM −127.864.460 → −36.056.694 = %71,80); fiyat değişimi = bilanço sonrası 40–55 gün fiyat / bilanço öncesi fiyat − 1. Sonuç yazılmamış ("ödev").
- Tansu'nun vurgusu: "orada temel analiz açısından istatistiksel bir arbitraj vardır" (1862514363178811538); "NEFK artarken hisse fiyatı artmıyor ise orada sizin için gizlenmiş bir fırsat olabilir" (1892680047779074122).
- Olgunluk: çekirdek. Adımlar tam. "Fiyata yansımamış" ölçüsü, korelasyon eşiği ve pencere hiçbir gönderide yok. Defterde "esas faaliyet kârı" ve temel-çift birleşimi yok (1941455577097306576 satırı).

### 1.2 "Sharpe net kâr marjı" ve F/K bandı ile istikrar / dışlama kuralı

- Ne yapar: Şirketi "istikrarlı" sayar ya da yatırım dışı bırakır.
- Parametreler (birebir):
  - 1781414254576300469: "İstikrarlı şirket olarak lanse edilebilecek FK'sı 6-16 arası ve sharpe net kar marjı 2 üstü olan şirketlerden".
  - 1794036593734418591: "1- sharpe net kar marjı 2 den küçük şirketlere, 2-patron şirketlerine, 3-büyüme şirketlerine YATIRIM YAPMA".
  - 1698267718074438032: "Özsermaye karlılığı yüksek F/K'sı 5-15 arasında"; "net kar marjı (sharpe)" > 2.
  - 1780322525055996240: "3,7 sharpe net kar marjı ile oldukça istikrarlı"; F/K 9,6 son 10 yılın dibi.
  - 1709805069644820609: kontrol listesinde "net kâr marjı (sharpe) > 2".
- Kaynak gönderiler: 1698267718074438032 (2023-09-03), 1709805069644820609 (2023-10-05), 1780322525055996240 (2024-04-16), 1781414254576300469 (2024-04-19), 1794036593734418591 (2024-05-24).
- Tansu'nun vurgusu: büyük harfle "YATIRIM YAPMA" (1794036593734418591).
- Olgunluk: çekirdek. Eşik tam (> 2; F/K 5–15 ya da 6–16). "Sharpe net kâr marjı" formülü hiçbir gönderide yok. Ölçünün marj mı Sharpe mi olduğu belirsiz. Not: F/K aralığı iki gönderide farklıdır (5–15 ve 6–16). 1917737673801732180 (2025-05-01) yine 5–15 der.

### 1.3 Tarihsel F/K ve PD/DD standart sapma bandı ile al-sat

- Ne yapar: Hissenin kendi çarpan geçmişinden ortalama ±1/±2 SD bandı çıkarır. Alt bantta alır, üst bantta satar.
- Parametreler (birebir, görselden doğrulandı):
  - 1694839230298468742 DOAS F/K: Ort 4,90; +1SD 6,39; +2SD 7,88; −1SD 3,40; −2SD 1,91. İşlem: "FK 2-3 arası alınıp, 7-5 arası satılabilir."
  - 1696022604472111319 (2014–2023): F/K Ort 8,41, +1SD 12,77, +2SD 17,13, −1SD 4,06; PD/DD Ort 2,04, +1SD 2,82, +2SD 3,61, −1SD 1,25, −2SD 0,46. "Uygun yer" eşiği yok.
  - 1700793391423058126 FROTO: "Trade seveler 7-8 bandından alıp 16-19 bandında satabilir." Dönemsellik notu: sene sonu net kâr artar.
  - 1916743082336285121 FROTO: F/K < 6,7 hazırlık; < 6,3 kademeli alım; 5,0–3,5 agresif alım; < 3,5 ikinci pozisyon; 6,7–8,0 tut; ~10 kademeli satış; > 10 hızlı satış.
  - 1913691337184154030: F/K ve PD/DD tarihsel ortalama altında + HBK artıyor + RSI 30 altından dönüş; örnek "ROE %20, F/K < 5, RSI 25'ten yukarı".
- Kaynak gönderiler: 1694839230298468742 (2023-08-24), 1696022604472111319 (2023-08-28), 1700793391423058126 (2023-09-10), 1913691337184154030 (2025-04-19), 1916743082336285121 (2025-04-28).
- Görsel notu: 1916743082336285121 görseli FROTO F/K zaman serisidir (2014/12–2024/12, dip ≈3,4 2023/12). Eşikler görselde yok; yalnız metinde. Sektör ortalaması çizgisi lejantta var, grafikte çizili değil.
- Olgunluk: tam (hisse başına eşik). Genel kural (her hisse için kaç SD) belirsiz; eşikler hisseye özel. Defterde R144 36 çeyrek PD/DD çıpası verir; SD bandı ve işlem eşiği vermez.

### 1.4 Black-Scholes opsiyon fiyatlama ve delta hedge

- Ne yapar: Avrupa tipi call/put adil değerini hesaplar. Model fiyatını piyasa fiyatıyla kıyaslar. Delta ile korunma adedini bulur.
- Parametreler (birebir, kod görseli 1897926533991268696 doğrulandı):
  - b = r − q; d1 = (ln(S/X) + (b + σ²/2)T)/(σ√T); d2 = d1 − σ√T.
  - call = S·e^(−qT)·N(d1) − X·e^(−rT)·N(d2); put = X·e^(−rT)·N(−d2) − S·e^(−qT)·N(−d1).
  - Örnek 1 (1897926537623609581, 1911177646052131219): S=100, X=130, T=1, r=0,05, q=0, σ=0,2 → 1,6396. Piyasada 2 TL ise pahalı.
  - Örnek 2 (1897926559081660560, görsel doğrulandı): AAPL S=170,73, X=180, T=7/366, r=0,055, q=0, σ=0,260261 → 0,21169777.
  - Varsayımlar (1911177641643983112): işlem maliyeti/arbitraj yok, sabit faiz, lognormal fiyat, sabit volatilite, Avrupa tipi.
- Yeniden hesap: iki örneği python ile yeniden hesapladım: 0,211698 ve 1,639593. Gönderilerle uyuşuyor.
- Kaynak gönderiler: 1885700221285368014 (2025-02-01); 1897926528647749945, 1897926530874880464, 1897926533991268696, 1897926537623609581, 1897926559081660560 (hepsi 2025-03-07); 1911177641643983112, 1911177646052131219 (2025-04-12); 1942962939696156904, 1942962944314098004 (2025-07-09).
- Olgunluk: tam (kod + iki çalışılmış örnek). Delta hedge adedinde hata var (bölüm 4). Defterde opsiyon tarafı yalnız implied move (R029) ve VRP (R031).

### 1.5 Kredi riski ve tahvil fiyatlama

- Ne yapar: Geri çağrılabilir tahvili faiz ağacıyla fiyatlar; temerrüde uzaklığı KMV ile ölçer.
- Parametreler (birebir):
  - 1851746402830807298: faiz ağacı 4,500% → 4,976/4,074% → 6,757/5,532/4,530%; nominal 100$, kupon %5,25, 1 yıl sonra 100$'dan callable; dy = 100 bps; duration = (P− − P+)/(2·P0·dy); callable 1,66, option free 2,75.
  - 1851754725680488551 (KMV): eşik borç yerine DPT; sürüklenme r yerine μA; DD bileşenleri ln(A0/DPT) + (μA − ½σA²)T; EDF = P(A_T ≤ DPT).
  - 1913877696590876973: kredi raporu kontrol listesi (kullanım amacı, geri ödeme, teminat, ortaklık yapısı, SWOT). Ölçü yok.
- Kaynak gönderiler: 1851746402830807298 (2024-10-30), 1851754725680488551 (2024-10-30), 1913877696590876973 (2025-04-20). Merton borç fiyatı (R061 genişletmesi) bölüm 2'de.
- Olgunluk: callable tahvil tam; KMV çekirdek; kontrol listesi fikir.

### 1.6 Net yabancı para pozisyonu (NetYPP) ile kur duyarlılığı

- Ne yapar: Döviz açığının ciroya göre baskısını ölçer.
- Parametreler (birebir):
  - 1915860915729166759: çeyrek satış = kümülatif farkı (09−06, 06−03, 03 doğrudan); yıllık satış = son 4 çeyrek; "Yabancı para pozisyonu / Net satışlar oranı × Kur değişimi = Şirkete kar veya zarar etkisi."
  - 1950865602647646516: NetYPP negatifleşir ve oran büyürse kur riski uyarısı; GARCH ve faktör analiziyle birlikte. Görsel: FROTO NetYPP 2024/12 ≈ −75B, oran −0,05 ile −0,175 arası.
  - 1913865330448879926: NetYPP = döviz varlıkları − döviz borçları; makro faktör olarak Fama-French 3 / Carhart 4 regresyonuna girer; statsmodels, linearmodels.
- Kaynak gönderiler: 1913865330448879926 (2025-04-20), 1915860915729166759 (2025-04-25), 1950865602647646516 (2025-07-31). İlgili: 1692269598073094408 (2023-08-17, kur farkı gideri varsa esas faaliyet kârına bak).
- Olgunluk: oran tam; uyarı eşiği yok (çekirdek).
- Defterde: yalnız R010 "nakdin döviz/faiz dağılımı".

### 1.7 TTM (son 4 çeyrek) yıllıklandırma ilkesi

- Ne yapar: Kümülatif bilançodan çeyrek değer türetir, son 4 çeyreği toplar. F/K, ROE, FD/FAVÖK bu değerle hesaplanır.
- Parametreler (birebir):
  - 1917565014988218574: altı gerekçe (mevsimsellik arındırma, tek çeyrek oynaklığı, trend, F/K ve FD/FAVÖK'ü yıllık kârla hesaplama, analist raporlarıyla kıyas, tek iyi çeyrekle pozisyona girmeme).
  - 1695361936651653499: yıllık kâr = 2023/6 + 2022/12 − 2022/6 (166.304.000 + 153.185.000 − 63.332.000 = 256.157.000); F/K = 73,15 / 3,316 = 22,06; FD/FAVÖK 33,15.
  - 1956754276270641304: Q1 = YTD, diğerleri YTD farkı; TTM = 4 çeyrek kayan toplam; kalemler satış 3C, esas faaliyet kârı 3H, ana ortaklık net kârı 3Z, duran varlık = 1BG + 1BGA + 1BH.
- Kaynak gönderiler: 1695361936651653499 (2023-08-26), 1917565014988218574 (2025-04-30), 1956754276270641304 (2025-08-16). R133/R146 genişletmeleri bölüm 2'de.
- Olgunluk: tam.
- Defterde: kâr tahmininde ileriye dönük yıl sonu kârı var (R062, R146); TTM ilkesi yazılı değil.

### 1.8 Adı defterde olmayan bilanço oranı türevleri

Grup A (borç ve likidite):
- Asit-test (1949421615135240509, 2025-07-27): "(Toplam Dönen Varlıklar -Stoklar) / Toplam Kısa Vadeli Yükümlülükler". R060 stokları dahil eder. Tam.
- Borç/kaynak (1918057202553929898, 2025-05-01): Toplam Borç / Toplam Kaynaklar; sektör ortalaması 0,595 (8 hisse). Tam, eşik yok.
- Borç/varlık (2086122842655973634, 2026-08-08): (KVY+UVY)/toplam varlık; FROTO 2026-Q2 %63,37, sektör %70,21. Tam.
- KV finansal yükümlülük payı (2086152222870536647, 2026-08-08): "%10 dolayında olması güzel bir durumdur". Tam.
- Nakit döngüsü (1951223829453259190, 2025-08-01): alacak/stok/borç devir hızı ve süresi; "net işletme sermayesi ihtiyacı < mevcut net işletme sermayesi → rahat". Formül ve eşik yok. Çekirdek.

Grup B (çarpan ve büyüme):
- PD/Net Satış TTM (2043007802344370231, 2026-04-11): PD = güncel ödenmiş sermaye × split-adjusted fiyat; ASUZU 0,91 → 0,65. Tam.
- FAVÖK YoY (2087251201691685145, 2026-08-11): "[3H + 4B](t) / [3H + 4B](t-1yıl) - 1"; FROTO 2023 ≈ %335 tepe, fiyat tepesi 2024/03. Tam, eşik yok.
- EFK/NS Q2 trendi (1957079412760813739, 2025-08-17): YoY = yüzde puan farkı (YAYLA −202,51 − (−261,48) = 58,97). Çekirdek.
- Görünmeyen varlıklar (1946857813327876099, 2025-07-20): marka, yazılım, patent; benzetme yöntemiyle dolaylı. Fikir.
- Parabolic SAR + hacim teyidi (1956635616818381305, 2025-08-16): SAR noktası fiyatın altına geçer + hacim artar. Eşik yok. Çekirdek.

### 1.9 Bedelsiz sermaye artırımı potansiyeli

- Ne yapar: Ödenmiş sermayeyi birikmiş kâr ve yedeklerle kıyaslar.
- Parametre (birebir, 2086040274434715957, 2026-08-08): "ödenmiş sermayesi düşük kalmış ancak yıllar içinde elde ettiği kârlar ve diğer yedekleri büyümüşse, bedelsiz potansiyeli yüksek çıkar". Oran eşiği yok.
- Ek kanıt (görselden): SAYAS (1850969302347989014) ve TTRAK (1708030356564160854) değerleme tablolarında "BEDELSİZ POTANSİYELİ" alanı var, ama boş. Alan 2023'ten beri tabloda durur.
- Olgunluk: çekirdek.

### 1.10 TOPSIS ve Gri TOPSIS

- Ne yapar: Şirketleri finansal oranlarla çok ölçütlü sıralar. Sonra DuPont gelir.
- Parametreler (birebir, kod görseli 1942540360460259582 doğrulandı):
  - Kriterler Net Kar Marjı, ROE, ROA, Borç/Özsermaye; `weights = np.array([0.3, 0.3, 0.2, 0.2])`.
  - Fayda: x/√Σx²; maliyet (Borç/Özsermaye): min/x; Ci = D_neg/(D_pos+D_neg).
  - Çıktı: SISE 0,576603; TUPRS 0,576055; EREGL 0,346221.
  - Gri TOPSIS (1947985822071894179): 7 adım; gri sayılı (aralık) matris; eşit ağırlık; gri sayının kesin sayıya dönüşümü; evren çimento sektörü.
- Kaynak gönderiler: 1942540360460259582 (2025-07-08), 1947985822071894179 (2025-07-23).
- Olgunluk: klasik TOPSIS tam; Gri TOPSIS çekirdek (kriter adları yok).
- Defterde: R179 kriterleri F/K, PD/DD, ROE, borçluluk, RSI; ağırlık ve kod yok.

### 1.11 VIF (çoklu doğrusallık) süzgeci: F/K regresyonu ve portföy

- Ne yapar: Regresyonda ve portföyde birbirine bağlı değişkenleri ya da hisseleri ayıklar.
- Parametreler (birebir):
  - 1824814340668617001 (kod görseli doğrulandı): `predict_pe_ratio_vif_filtered`, "model with VIF < 10"; 10 değişken (Operating_Profit_Growth, EBITDA_Growth, Net_Profit_Growth, Net_Sales_Growth, Closing_Price, ROCE, Divident_Yield, Debt_to_Equity_Ratio, Sector_ROE, Growth_in_Short_Term_Liabilities); çıktı 17,49075.
  - 1825279192390594981: Ridge alpha 0,26; MSE 3,0899, RMSE 1,7578, R² 0,9613 (metinden); BIMAS 2024/6 tahmini 20,897302 (görsel doğrulandı; 8 test satırı).
  - 1825283202191167740: HBK F/K modeline değişken olarak girmez (VIF).
  - 1823403053212475711 (portföy): "10 üzeri olmasın, 5 üstü olmazsa daha harika olur".
  - 1822565459905888316 (portföy): portföy kurmadan önce VIF ya da kovaryans matrisi kontrolü.
- Kaynak gönderiler: 1822565459905888316 (2024-08-11), 1823403053212475711 (2024-08-13), 1824814340668617001 (2024-08-17), 1825279192390594981 (2024-08-18), 1825283202191167740 (2024-08-18).
- Tansu'nun vurgusu: "Hoca VIF kavramını bilmiyor olabilir mi?" (1825283202191167740).
- Olgunluk: tam. Defterde R066 regresyonu verir; VIF yok.

### 1.12 Kişisel portföy tahsis kuralları

Defterde bu kuralların hiçbiri yok.

- Kripto üst sınırı (tam, üç farklı değer): "maks. %1 ile %5" (1783205936427119005, 2024-04-24); "Max %4" (1840693444294975693, 2024-09-30); "max %5-10" (1860757961032835441, 2024-11-24).
- Temettüyü aynı hisseye yeniden yatırma (1769351216369213499, 2024-03-17): "540 lotuma karşı 20.000 tl dolayında temettü alacağım, bununla yine #doas alacağım". Çekirdek.
- Düzenli aylık alım / DCA (1783840694043623592, 2024-04-26): hedef 2028–2030; tutar yok. Çekirdek.
- Çekirdek-uydu (1761787714523865301, 2024-02-25): "portföyümün %80 i uzun vadeli %20 si de trade". Tam.
- Varlık sınıfı sepeti: 1878086554394009983 (2025-01-11; altın, faiz, bono, tahvil; ağırlık yok); 2100012254636683371 (2026-09-16; "Altın, döviz veya para piyasası fonlarıyla sepet yapmak lüks değil, zorunluluktur."); pasif endeks 1945059707393105960 (2025-07-15), 1987747948675952790 (2025-11-10; %70 hisse / %30 tahvil).

### 1.13 Risk parity

- Ne yapar: Her varlığın toplam riske eşit katkısını hedefler; ağırlık volatiliteyle ters orantılı.
- Parametreler: 1822360182682165714 görselden RPP / MinVar ağırlık BIMAS ≈0,43/≈0,64, EKGYO ≈0,30/≈0,20, GUBRF ≈0,27/≈0,16. 1827476527899894046 seçim kuralı: "Use Risk Parity if: You are seeking a more balanced and diversified approach"; belirli hedef → Markowitz (min varyans ya da max Sharpe). Formül ve pencere yok.
- Kaynak gönderiler: 1822360182682165714 (2024-08-10), 1827476527899894046 (2024-08-24), 1944760309123575813 (2025-07-14).
- Olgunluk: çekirdek.

### 1.14 Black-Litterman ve kayan pencere

- Parametreler: "21 günlük rolling black litterman benim tercihim" (2096146762188611697). Seçim kuralı (1940657356347474399): görüş yoksa Markowitz, görüş varsa BL; "Başlangıçta Markowitz ile başlanmalı"; Markowitz uç ağırlık örneği %120 / −%40; PyPortfolioOpt. Görüş matrisi ve diğer girdiler yazılı değil.
- Kaynak gönderiler: 1797263549892276362 (2024-06-02), 1797263555382702421 (2024-06-02), 1940657356347474399 (2025-07-03), 2096143361002385717 (2026-09-05), 2096146762188611697 (2026-09-05).
- İlgili fikir: gradient descent ile ağırlık (1885700224598880340, 2025-02-01); parametre yok.
- Tansu'nun vurgusu: "benim tercihim".
- Olgunluk: çekirdek (pencere 21 gün; görüşler yok).

### 1.15 Durağan Convex Hull ve GARCH filtresi

- Parametreler: her periyotta Convex Hull; hissenin köşe olduğu periyot sayısı; periyot haftalık/aylık/çeyreklik (1949942724888506647). GARCH sürümü 5 adım: "Yüksek köşe süresi ve düşük GARCH volatilitesi olan hisseleri seç." (1949942729116373465). Yüzdelik, eşik ve GARCH derecesi yok.
- Kaynak gönderiler: 1949942724888506647, 1949942729116373465 (2025-07-28).
- Olgunluk: çekirdek.

### 1.16 VİOP endeks short ile beta ayarlı hedge

- Parametreler (2097068834284863827, 2026-09-07): THF örneği brüt hisse ~%84,6, VİOP short/NAV ~%20,4, net hisse ~%64,2, beta ayarlı net piyasa riski ~%38 (formül yazılı değil).
- Olgunluk: çekirdek.

### 1.17 Çift (pairs) türevleri

- Tavan tetikli çift (1857953385569190399, 2024-11-17): tavan olan hisseye yüksek koreli eş. Eşik yok. Çekirdek.
- Eşbütünleşik çift ağı ve t-SNE (1898476669851316502, 1898479427132256391; 2025-03-08): çift istatistikle bulunur; t-SNE yalnız görselleştirme. Fikir.
- Granger + HMM + pairs (1922967215969542347, 2025-05-15): yalnız adlar. Fikir. Defterde HMM yalnız R091'de "gerek yok".
- Spek–spek eşleşme (1941240803654877456, 2025-07-04): aynı sektör ya da temadaki spekülatif eş. Çekirdek.
- GVX rejim filtresi (1999361321435811868, 2025-12-12): altın–DXY; "GVX'i bir al-sat sinyali olarak değil ... 'Rejim Filtresi' olarak"; sayısal eşik yok. Çekirdek.

---

## 2. Genişletmeler (R kaydı başına)

Biçim: "R: defterde ne var → X ne ekliyor".

### 2.1 Değerleme ağırlığı ve çarpanlar

- R064/R151: ağırlıkları DCF ile verir → DCF yokken nihai = (çarpan ort. + kâr modeli ort.)/2; 446,42 = (393,48 + 499,35)/2; kâr modeli = ort(F/K fiyatı 512,75, FD/FAVÖK fiyatı 485,96); satış girdisi 637 milyon USD (1698276357233352931, 2023-09-03; 1756414213394686142, 2024-02-10: "standart sapmayı minimuma indirmeyi hedefledim").
- R146: kâr modeli → girdi CEO'nun sene sonu ciro ve FAVÖK hedefi; çarpan modeli 75,39 (%4,0), kâr modeli 116,64 (%61); "Daha sağlıklıdır" (1700754232658231421).
- R064/R068: çarpan ortalaması → kod: 2011/12–2023/12 yıl sonu F/K aritmetik ortalaması, `fillna(0)`; ASUZU sektörel 11,25, şirket 50,25 (1852711643660083507).
- R062/R064: sektör kıyası → literatür: "%15 hata payı içinde kalma oranı yaklaşık %40" (Kaplan & Ruback); ileriye dönük F/K en doğru; peer grubu büyüme, kârlılık, risk benzerliğiyle (1939273526134939965).
- R062/R144: kısa/uzun pencere → "KISA DÖNEM : 2025/12 dahil geriye 8 çeyrek + anlık"; uzun = 36Ç + anlık; sektör = 8 hisse; ASUZU PD/DD 0,99 (sektör 2,18), kısa 1,38 (2,60), uzun 0,98 (2,56) (2041941067025494204).

### 2.2 DCF, WACC, risk primi

- R153/R165: İNA adı → SAYAS çalışılmış örnek: 10 yıl; büyüme 50%, 150%, 50%, 40%, 40%, 20%, 20%, 18%, 15%, 15%, uç %5; FAVÖK marjı %23,1 sonra %20,8; AOSM %13,5; sonsuz büyüme %3; 11.379.300 ÷ 77.250 = 147,30 TL; fiyat 74,00 → %99 (1695183583676113357).
- R070: Damodaran ÜRP formülü → çalışılmış örnek: TR 10Y %27, TR 5Y CDS %5,1, ABD 5Y CDS %0,58 → ÜRP %5,07, toplam ERP %10,07 (1769338011815211270). Hesabım: (5,1 − 0,58) × 1,12 = 5,06.
- R070/R153: üç rs yöntemi → rs = rd + RP, "RP: Ek risk primi (genelde %3–5 arası alınır)"; WACC = wd·rd·(1−T) + wc·rs; üç rs eşit ortalama; proje getirisi WACC altındaysa yatırım yok (1911632045777789394).
- R159: Total Beta CoE → karar kuralı: beklenen getiri < CoE (%16,21) ise işe girme (2037876835120296077).
- R061: Merton girdileri → borç = A − call; d1 = (ln(A/D) + (r − γ + ½σ²)T)/(σ√T); A=100, D=90, r=0,05, γ=0,02, T=1, σ=0,3 → 81,76 (1875619396414251058). Python ile yeniden hesap: 81,762.

### 2.3 HBK, TTM, ROE (R133, R146, R152, R144)

- R133: HBK adı → HBK = 3L / 2OA; veri sırası XI_29 → UFRS → UFRS_K (1911030879519994288); 24 çeyrek seri (1911030882531418617); pivot son 12 dönem, 2 ondalık (1911030886180528368); 3-6-9-12 aylık dönemsel ivme (1911030864818937888).
- R133: yıllık HBK → son 4 dönem toplamı (1911033991064416640); TCELL 7,00 = 0,36+1,21+2,30+3,13; 21,23 = 1,30+2,85+7,74+9,34 (1889451595584115079, görsel doğrulandı); yıllık HBK ile fiyat: "kâr trendinin yukarı, fiyatın ise geride olduğu dönemler fırsat" (1954539134158041128).
- R133/R062/R152: F/K → çeyreklik HBK = dönemsel(t) − dönemsel(t−1); "FK = Güncel Hisse Fiyatı / Yıllıklandırılmış HBK" (1916736171838767120); yıllık net kâr = son 4 çeyrek (1915483602713997579).
- R146: kâr serisi → çeyrek net kâr = kümülatif(t) − kümülatif(t−1); İş Yatırım API 2014–2025 (1915483600121737649); 3C/3H/3Z okuma kuralları: "ciro artarken 3H düşüyorsa marj baskısı" (1956754276270641304).
- R144/R179: ROE adı → ROE = son 4 çeyrek net kâr / ((cari özsermaye + geçen yıl aynı çeyrek)/2) (1915483606887055800); ROE = net kâr / özsermaye (1915483594597806535).

### 2.4 DuPont (R002, R158)

- R002/R158: DuPont yalnız ad → KCAER şirket/sektör: net kâr marjı %7,86/%4,30 (1771970054793433148); aktif devir %125,28/%88,75 (1771970056819253739); borç/kaynak %41,97/%43,92, aktif kârlılık %9,85/%3,82 (1771970060413726871).
- R002/R064: sektör = 100 endeksi: NKM ~182, aktif devir ~141, aktif kârlılık ~258, borç ~95, ÖK kârlılığı ~276; stok devir sektörün ~yarısı, alacak tahsilat ~10 gün uzun (1771970071931338855).
- R002/R158: formüller → aktif kârlılık = yıllık net kâr / toplam varlık × 100 = NKM × ADH; sektör ort. 5,619 = yalnız pozitif 6 değerin ortalaması (1918417139813187678, görsel doğrulandı); ADH = yıllık net satış / ortalama toplam varlık (1918458073099710657); CANTE ADH %34 × NKM %7,66 → ~%2 (1781414247290765330).
- R002/R158: tablo → 30 enerji hissesi; ALFAS 23,62 × 1,9635 = 46,38 (1777571511395557531); dayanıklı tüketim ROE sıralı, Dupont_Analizi_Tuketim.xlsx (1886887500183974168).
- R002/R158: tam şema → ROE = NKM × ADH × finansal kaldıraç; borç eşikleri "%70'in üzerindeki borç oranları riskli ... %30-50 arası dengeli ... %30'un altı muhafazakar"; DOAS ROE %230 → %8 kırmızı bayrak (1979208183236157837).

### 2.5 Tarama filtreleri (R059, R060, R134, R144, R218, R240, R002)

- R059/R144: bilanço kalemi → duran varlık artış % = (DV / 1 yıl önceki DV − 1) × 100 + F/K + sektör F/K (1950901940524617991; TOASO 98,14, DOAS 62,78); "%90'dan büyük ... RSI>50" otomotiv (1950916832409403513); DV × F/K karar matrisi (1954964170585030772); FROTO DV %54,22, F/K 8,44 < sektör 23,55 (1956635609449091123); fiyata gecikmeli yansıma (1955010441526022428).
- R060/R134: cari oran < 1 → NİS > 0, cari oran > 1,5, borç/varlık < %50, net nakit akışı > 0 (1946652254116684019); likidite oranı < 1 riskli, sektör altı ek uyarı (1949414090499112967); borç/varlık seyri okuma kuralları (1950539635001557460); borç/özkaynak FROTO ≈ %173, sektör ≈ %452 (2086514064688124094).
- R144/R218: "Düşük PD/DD + Yüksek ROE + Sektör altı çarpan" sayısız → F/K 5–15 ve ROE > sektör ort. (14,60); FROTO 34,34/8,43, TTRAK 30,43/14,68 (1917737673801732180).
- R218/R144/R166: temel + haftalık dip: net kâr büyümesi son 4 çeyrek pozitif (%10+), borç/özkaynak < 1, PD/DD < 1,5, brüt kârlılık > %20; haftalık RSI < 30, fiyat / 52 hafta dip < 1,10, son 2 hafta hacim önceki 4 haftadan %20+ (1954864370409783700).
- R240/R057: soru → "her biri için en az yüzde onluk bir büyüme"; öncelik özkaynak > HBK > satış/brüt kâr > nakit akışı (1945811547680297466).

### 2.6 Mevsimsel satış ve faaliyet kârı (R002, R118)

- R002/R046: aynı çeyrek kıyası; "3 yıl üst üste Q2 dönemlerinde artış" güçlenme, iki yıl düşüş yapısal sorun (1956819684713509048).
- R002/R118: Q2 net satış 2022Q2 < 2023Q2 < 2024Q2 < 2025Q2; CAGR3y = (2025Q2/2022Q2)^(1/3) − 1; FROTO %83,94, OTKAR %71,45, ASUZU %61,72 (1956830336467243263); BIST50: KONTR %135,74, FROTO %83,94, MGROS %82,11 (1956848925543206980).
- R002/R133: esas faaliyet kârı (3DF) sürümü: CAGR = (7.985.885.000 / 2.752.546.000)^(1/3) − 1 = %42,63; "Q2 bilançoları öncesinde pozisyon alıp açıklama sonrasında satmayı" (1957003613827420651).

### 2.7 Regresyon ve diğer değerleme (R066, R045, R145/R179, R164)

- R066: regresyon → aday modeller çoklu doğrusal, polinomial, lasso, ridge (1781073113205117347); regresyon F/K 24 ile tarihsel ort. 24–25 kıyası (1826661989126733986); VIF ailesi 1.11'de.
- R045: Gordon → "Döngüsel sektörlerde tek bir yılın yüksek temettüsü taranırsa, hisse 3 kat ucuz gibi görünür" (2089833787161039283).
- R145/R179: TOPSIS ağırlık ve kod 1.10'da (1942540360460259582).
- R164: "ayni" satırı; okuma hatası bölüm 4.2'de (2036840358210945219).

### 2.8 Portföy (R074, R110, R137, R173, R177, R178, R181, R182, R030)

- R110/R112: Markowitz → DOAS %70 / GESAN %30, ρ = 0,26, 1 yıl, risk %46, getiri %350 (1759294658004291906).
- R177/R074: min varyans → 5 hisse ağırlık ARCLK 0,265, EREGL 0,240, GARAN 0,178, THYAO 0,050, TUPRS 0,268 (1760032311100465169); 10 hisse getiri %1081,99, risk %167,80 (1771618491960811992); kapalı form `weights = inv_cov_matrix.dot(ones) / ones.dot(inv_cov_matrix).dot(ones)` ve `weights = sharpe_ratios / sharpe_ratios.sum()` (1878777386839503131).
- R173/R182: Monte Carlo kod → N_PORTFOLIOS = 10**5; N_DAYS = 252; `np.random.lognormal`, satır toplamı 1 (1822304577560985704).
- R178: Convex Hull → sektör ön elemesi + Sharpe (1947006461487517762); köşe sektörler Bankacılık (Std 152,68, Getiri 440,74, Sharpe 2,89) vb., kesitsel momentum 1/3/6 ay (1948891823121801615); 2–3 köşe sektör, her birinden 3–4 hisse, Markowitz (1949378649817280840).
- R137/R181/R074: tarama → max Sharpe Top 3 HEDEF %65,81, ECILC %26,47, ALKA %7,72 (2011146964000449005); p value < 0.05 filtresi, Min Vol +%2,55, Max Sharpe +%4,95 (2011888520944550254); tarama 20 → elle 10–15 → optimizasyon (2044720738934915283); DEY_Marj_% formülü, Min Vol / Max Sharpe ağırlıkları (2009963157498802601); momentum 6 grup × 5 hisse, 10 yıl (1822009542328426674).

### 2.9 Portföy (devam)

- R030/R078: volatilite harvesti → 2015-01-02→2025-12-30, vol oranı %0–%100 taraması; %30: aktif %3426,22 / pasif %833,65 (2053179966284530147); rebalance "Günlüktür" (2053377141421584469). Vol bileşeninin hangi varlık olduğu belirsiz.
- R110/R137: Sharpe → risksiz oran "ABD piysaları için bu 0.05 alınır"; TR iki basamaklı, değer yok (1951989068390187136).
- R173/R223: getiri tanımları → log getiri = ln(Pt/Pt−1); yıl = 252; yıllık vol = günlük std × √252; reel getiri = (1+nominal)/(1+enflasyon) − 1; yf.download + Ticker.history ile son gün kontrolü (2099534451353006287).

### 2.10 Çift: eşbütünleşme (R228, R262)

- R262: test adı var, p eşiği yok → "Eğer Pv<0.05, ve Tv<Cv ise conitegration var derim." (1874473152455246129); "p-değeri %5'ten küçük çıkarsa" (1941623461744415106).
- R228/R262: ilke → p tablosu (görsel doğrulandı, 1941585010051498309): SAHOL-YKBNK korelasyon 0,953 / p 0,0094 Evet; SAHOL-THYAO 0,89 / 0,033 Evet; THYAO-YKBNK 0,0226 Evet; TUPRS-YKBNK 0,0229 Evet; AKBNK-SAHOL 0,968 / 0,1615 Hayır.
- R096/R101/R228: tarama hattı → "1) bütün BIST; 2) korelasyon > 0,7; 3) eşbütünleşme testi; 4) z-score ±2" (1941900327655027097).
- R262/R096: ML hattı → StandardScaler; K-Means, küme sayısı KneeLocator; küme içinde Engle-Granger p < 0.05 ve test ist. < kritik değer; hedge ratio OLS; `spread = A - hedge_ratio * B` (1912875732646117781).
- R002/R228 ve R100/R034: sektör getirisinde eşbütünleşme şartı (1949013716512411954); geride kalan sektör + p < 0,05 (1949018697315524785); 5 yıl penceresi: ilk 4 yıl p < 0,05, son yıl ayrışma, temel analizle kaynak araması (1956228467021824388).

### 2.11 Çift: spread ve tarama (R101, R096, R251, R100)

- R101: Z ±2 ve çıkış 0,5 var → spread = log getiri farkı, bantlar HO ± std (1857400047589048780); "Sabit standart sapma ... ±2 standart sapma" (1860462510752575670); 30HO ile trend, log fark (1891546429388189846); "Asıl hareket 1-2 gün sonra başlıyor" (1861423505184563297).
- R101: bantlar → gri işlem bantları +2..+4 ve −2..−4 (1858560343200436379, görsel doğrulandı: 2022-11 – 2024-11, son değer ≈ +2,7); EREGL–KRDMD aynı bantlar (1941550364911862113).
- R101/R228: korelasyon eşiği → "Normal şartlarda pairs trading için 0.80 ve üstü alınır ama ben BIST ortamında 0.71'in anlamlı" (1862207562378035671); kripto kodu > 0.80 filtresi (1875859168810447196); korelasyon tuzağı örneği: TUPRS–MGROS %98 korelasyon, kümülatif getiri ≈ −%80 ile −%88 (1776001445969502607, R228/R100).
- R096: evren → BIST, 2014–2025, günlük getiri, korelasyon > %80, Excel (1891546418520654268); kümülatif getiriye göre çift seçimi (1859335541617197519).
- R251/R034/R091: Pair Health → rolling correlation 30/60/90 gün, beta stabilitesi, half-life; bozulma örneği ~%70 → ~%30 (2096167419941130368); tarayıcı sınıfları YENİ AL SİNYALİ / DEVAM EDEN FIRSAT (|Z| > 2) / BOLGEYE YAKLASIYOR (|Z| ≈ 1,48–1,94) (2093048380297547956).
---

## 3. Çelişkiler

Bu temada 19 "celisir" satırı var. Ek olarak tema-5'teki 1850969302347989014 ağırlık başlığına kanıt olarak girer. Karar vermiyorum; olasılık ve kanıtı yazıyorum.

### 3.1 Değerleme ağırlığı: çarpan %40 / İNA %60 ↔ defter çarpan %60 / DCF %40

**Defter tarafı (birebir):**
- R068 (2026-08-27): "En sonunda bu ortalamanın %60'ını, DCF'in de %40'ını alırım."
- R151 (2026-08-28): "En so aşamada ise İNA'sonucunun %40'ı, basit çarpan değerlemesi ve detaylı çarpan değerlemesinin ortalamasının %60'ı alınarak sapmalar minimize edilir."
- R158 (2026-08-28): "İndirgenmiş nakit akışı yöntemlerinin üçünün ortalaması toplam ağırlığın yüzde kırkını oluşturacak. Üç farklı vade için hesaplanan çarpanlar analizinin ortalaması ise yüzde altmışı."
- R158 gerekçesi: "piyasa ne der sorusu, biz ne hesapladık sorusundan genellikle daha bağlayıcı oluyor."
- R064 (2026-08-27): "(A\*0.6) + (DCF \* 0.4) = Hisse fiyatın ya da ((A+B)\*0.6) + (DCF \* 0.4) = Hisse fiyatın".

**Gönderi tarafı, metinle (birebir):**
- 1708030356564160854 (2023-09-30, TTRAK): "Çarpanlar %40, İNA %60 ağırlıklandırılarak 2023 sene sonu için ortalama fiyat 1584tl bulundu".
- 1780322528658886674 (2024-04-16, BRISA): "Ortalama çarpanlar fiyatının %40'ı ve İNA analizinin %60'ı alınarak".

**Gönderi tarafı, tablo hesabıyla (ilk 5):**

| id | tarih | hisse | çarpan ort. | İNA | tablo sonucu | 0,4×çarpan + 0,6×İNA |
|---|---|---|---|---|---|---|
| 1695389783147581542 | 2023-08-26 | SAYAS | 159,39 | 133,71 | 143,98 | 143,98 |
| 1708030356564160854 | 2023-09-30 | TTRAK | 785,30 | 2116,93 | 1584,28 | 1584,28 |
| 1708049006742417472 | 2023-09-30 | SAYAS | 120,49 | 133,71 | 128,42 | 128,42 |
| 1769338023169143095 | 2024-03-17 | DOAS | 626,98 | 636,04 | 632,42 | 632,42 |
| 1774367633820750263 | 2024-03-31 | ASUZU | 147,96 | 139,53 | 142,90 | 142,90 |

**Gönderi tarafı, tablo hesabıyla (devam):**

| id | tarih | hisse | çarpan ort. | İNA | tablo sonucu | 0,4×çarpan + 0,6×İNA |
|---|---|---|---|---|---|---|
| 1778895335592472990 | 2024-04-12 | TOASO | 456,73 | 320,00 | 374,69 | 374,69 |
| 1780322534144999705 | 2024-04-16 | BRISA | 207,22 | 170,00 | 184,89 | 184,89 |
| 1850969302347989014 (tema-5) | 2024-10-28 | SAYAS (eski tablo) | 159,39 | 133,71 | 143,98 | 143,98 |

Not: 1708049006742417472 satırı görsel tarihini 2023-08-27 olarak verir; gönderi tarihi 2023-09-30'dur.

**Yeniden hesap, örnek 1 — SAYAS (görsel 1850969302347989014-1.jpg açıldı):**
- Görsel: F/K'ya göre 47,12; PD/DD'ye göre 269,47; FD/FAVÖK'e göre 161,59; İNA'ya göre 133,71; ORTALAMA FİYAT 143,98; ORTALAMA GETİRİ 96,8%; fiyat 73,15.
- Çarpan ortalaması = (47,12 + 269,47 + 161,59) / 3 = 159,393.
- 0,4 × 159,393 + 0,6 × 133,71 = 63,757 + 80,226 = **143,98**. Tabloyla aynı.
- Ters ağırlık: 0,6 × 159,393 + 0,4 × 133,71 = **149,12**. Tabloyla uyuşmaz.
- Getiri: 143,98 / 73,15 − 1 = %96,8. Tabloyla aynı.
- Aynı tablo 1695389783147581542'de (2023-08-26) de var. 1850969302347989014 (2024-10-28) bu tabloyu "Hey gidi günler ... 73 lirada iken yaptığım nokta atışı" diye yeniden paylaşır.

**Yeniden hesap, örnek 2 — TTRAK 2023/2Ç (görsel 1708030356564160854-1.jpg açıldı):**
- Görsel: F/K'ya göre 824,37; PD/DD'ye göre 240,21; FD/FAVÖK'e göre 1.291,33; ORTALAMA FİYAT 785,30; İNA 2116,93; çarpan+İNA 1584,28; getiri 79,83%; hisse 881,00; kâr modeli 939,48 / 1.227,89 → 1.083,69 (23,01%).
- (824,37 + 240,21 + 1.291,33) / 3 = 785,30. Tabloyla aynı.
- 0,4 × 785,30 + 0,6 × 2116,93 = 314,12 + 1270,16 = **1584,28**. Tabloyla ve metinle aynı.
- Ters ağırlık: 0,6 × 785,30 + 0,4 × 2116,93 = **1317,95**. Uyuşmaz.
- 1584,28 / 881 − 1 = %79,83. Tabloyla aynı. Kâr modeli (1.083,69) nihai fiyata girmez.

**Zaman sırası:** Gönderiler 2023-08-26 ile 2024-04-16 arasında hep %40 çarpan / %60 İNA kullanır. 1848034791116931310 (2024-10-20) planı ise "İlk grubun %6'ı / İkinci grubun %40ı" der; grup 1 çarpanlardır. Satır bunu %60 çarpan / %40 (İNA + kâr modeli) olarak okur. Defter kayıtları (2026-08-27/28) sonra gelir ve %60 çarpan / %40 DCF der.

**Olasılık:**
- Tarihçe (en güçlü kanıt): eski tablolar 40/60; 2024-10-20 planı ve 2026 defteri 60/40. Ağırlık 2024-04 ile 2024-10 arasında değişmiş olabilir. Değişim gerekçesi olarak yalnız R158 cümlesi var.
- Hata: zayıf. Yedi tablonun hepsi 40/60 ile tutarlıdır; iki gönderi metni de 40/60 der. Tek tabloda yazım hatası değil, tutarlı bir yöntemdir.
- Bağlam: 1850969302347989014 (2024-10-28) eski tabloyu yeniden paylaşır; yeni bir 40/60 kararı değildir.
- Belirsiz: 2024-10 sonrası 40/60 kullanan yeni bir tablo bu temada yok. 2025 tarihli ağırlık tablosu bu temada yok.

**İlgili alt çelişki — kâr modelinin grubu (1848034791116931310, 2024-10-20):**
- Gönderi: "İNA'ya göre fiyat / Kar tahmin modeline göre fiyat / Bunların ortalaması / İlk grubun %6'ı / İkinci grubun %40ı" (kâr modeli İNA ile %40 grubunda).
- Defter R064 (2026-08-27): "((A+B)\*0.6) + (DCF \* 0.4)" (B = basit kâr modeli, %60 grubunda). R151 de "basit çarpan değerlemesi"ni %60'a koyar.
- Defter sonra gelir. Olasılık: tarihçe ya da bağlam (plan taslağı). "%6" yazım hatasıdır (bölüm 4).

### 3.2 Çarpanların eşit ya da sektöre göre ağırlığı

- Gönderi 1939273530073354480 (2025-06-29): "her çarpanı da eşit ağırlıkla değerlendirmek yerine, sektörüne ve duruma göre uygun ağırlıklar vermeye çalışmalı". Kaynak Cheng & McNamara (2000).
- Defter R064 (2026-08-27): "her bir ortalamanın (3 ) ortalamasını alacaksın"; R068: "Sonra bu ortalamaların da ortalamasını alırım" (eşit ağırlık).
- Defter sonra gelir.
- Olasılık: bağlam. Gönderi bir literatür özetidir; satır "iyileşme sınırlı" diye not eder. Tansu'nun kendi kuralı eşit ağırlıktır.

### 3.3 PD/DD aracında kalan dönem kârı (2041968928205766731 ↔ R062)

- Gönderi (2026-04-08) görseli: "Donem Net Kari (3Z) 2,330,587,214 TL; Yilin Kalaninda Bekl. Kar 3,028,332,000 TL; Beklenen Ozsermaye 14,945,537,852 TL". Hesap: 11.917.205.852 + 3.028.332.000 = 14.945.537.852; 3Z düşülmemiş.
- Defter R062 (2026-08-27): "Kalan Dönem Beklenen Kâr 2,507,864,254 TL (= Tahmini Yıl Sonu - 3Z)".
- Defter sonra gelir.
- Olasılık: hata, sonra düzeltilmiş (tarihçe). Erken araçta tam yıl kârı kalan döneme eklenmiş. Ayrıca 2025/12 çarpanları 2023/12 özsermayesine uygulanmış.

### 3.4 Monte Carlo ↔ R182 "Spicy"

- Gönderi 1771531828676919771 (2024-03-23): "doğrusu bende monte carlo simülasyonunu tercih ediyorum".
- Gönderi 1890128570749710462 (2025-02-13): "markowitz kodunu monte carlo lie yazıp optimize ediyorum". Arada 1822304577560985704 (2024-08-10) MC kodunu verir (10**5 portföy, lognormal ağırlık).
- Defter R182 (2026-08-28): "Neden Monte Carlo Yerine 'Spicy' Model? ... Bizim tercih ettiğimiz 'Spicy' yaklaşımı ise bu rastlantısallığı reddeder." Defter sonra gelir (gönderilerden 18–29 ay sonra).
- Olasılık:
  - Tarihçe: 2009963157498802601 (2026-01-10) "Spicy Markowitz" kullanır. Geçiş 2025-02 ile 2026-01 arasında olabilir.
  - Bağlam: defter R182 yazarını "M (LLM biçimli)" diye işaretler. R185 Monte Carlo'yu risk of ruin için önerir; rol farklıdır.
  - Hata: kanıt yok.

### 3.5 Eşbütünleşme ↔ R228 "şarttır"

- Gönderi 1862575026785898738 (2024-11-29): "Kısa vadelilere baktığım için cointegration analizi yapmadım".
- Gönderi 1874473150085468373 (2025-01-01): "İstatistiksel arbitraj sistemimde henüz cointegration bakmıyorum çünkü zaten çok kısa vadeli trade amaçlı kullanıyorum."
- Gönderi 2086417789812646087 (2026-08-09): "Gold and Copper showed a p-value of 0.13 in the cointegration test. Accepting this risk, our relative arbitrage model triggered a BUY Copper signal."; görsel: "Eşbütünleşik değil ya da sınırda (p=0.13578047524292614)"; Corr_Tam 0,385, Corr_60G 0,5675.
- Defter R228 (2026-08-28): "Arbitraj için Cointegration (Eşbütünleşme) şarttır, şarttır. şarttır."; R262 (2026-09-06): "sadece faydalı bir gösterge değil, stratejinin üzerine inşa edildiği zorunlu bir temel". Defter sonra gelir. 2086417789812646087, R228'den 19 gün öncedir.
- Olasılık:
  - Tarihçe (2024-11 ve 2025-01 gönderileri): "henüz" sözcüğü geçişi gösterir. Aynı gün 1874473152455246129 karar kuralını yazar ("bot yazılıyor"). 2025-07-05'ten sonra test hatta girer (1941585010051498309, 1941900327655027097).
  - Bağlam (2026-08-09): varlık emtia; risk açıkça kabul edilmiş. Kural dışı bilinçli bir istisna olabilir. Belirsiz.

### 3.6 "Risksiz kazanç" ↔ R100

- Gönderi 1857456246426611922 (2024-11-15): "önemli olan korelasyonın bozulduğu yerlerde fiyat farkından arbitraj yakalamak Risksiz kazanç :)".
- Gönderi 1858202441918869545 (2024-11-17): "bu beraberliğin bozulduğu aralığı yakalayarak oradan risksiz kazanç elde etmek".
- Defter R100 (2026-08-27): "Her arbitraj fırsatı çalışmaz Mutlaka backtest etmek lazım Görünmez bağ kopmuş olabilir."
- Defter sonra gelir.
- Olasılık:
  - Bağlam (söylem): ilk gönderide ":)" var. Tansu 1776001445969502607'de (2024-04-04, gönderilerden önce) %98 koreli TUPRS–MGROS çiftinde −%80..−%88 kümülatif getiri gösterir. Yani riski önceden biliyor.
  - Tarihçe: R100 daha temkinli bir dil kullanır.

### 3.7 Tek varlık ↔ R099

- Gönderi 1938917789491667197 (2025-06-28): "bir yatırımcının tüm sermayesini tek bir varlık ya da projeye tahsis etmesi, finansal evrimsel süreç açısından yüksek ölüm riski taşıyan bir davranıştır".
- Defter R099 (2026-08-27): "92.354 TL'lik tüm bakiyesiyle yeni bir işleme giriyor" (defter: "tüm sermaye tek pozisyon — kural tam").
- Defter sonra gelir.
- Olasılık: bağlam. R099 iki bacaklı (AL/SAT) çift işlemidir; tek varlık değildir. Çelişki zayıf.

---

## 4. Hatalar ve tutarsızlıklar

### 4.1 Tansu'nun gönderi içi hata ve tutarsızlıkları

Grup A (formül ve hesap):
- 1942962939696156904: "1000 * 0.5 = 500 adet put opsiyon almanız gerekir". Tam delta hedge için adet = hisse / |delta| = 1000 / 0,5 = 2000. Metindeki formül hatalı.
- 1915860915729166759: 100 milyon TL ciro × %0,486 = 0,486 milyon TL. Metin 48,6 milyon TL der.
- 1915483606887055800: "ROE = Yıllık Net Kâr / (Cari + Geçen Yıl Özsermaye) / 2". İşlem önceliğiyle sonuç yarıya iner. Kastedilen: Net Kâr / ((cari + geçen)/2).
- 2036840358210945219 (R164 kaynağı): kodda `ebit = e` güncellemesi üssü biriktirir. EBIT_i = EBIT_(i−1) × 1,017^i; yıl 5 = 5000 × 1,017^15 = 6.438,49. Düz bileşik büyüme 5.439,7 verir.
- 1852711643660083507: `fillna(0)` eksik F/K'yı 0 sayar; ortalama aşağı iner.

Grup B (adlandırma ve tablo):
- 1942540360460259582: "Gri TOPSIS" adı. Kodda gri sayı ya da aralık yok; uygulama klasik TOPSIS (görsel doğrulandı).
- 1957079412760813739: tablodaki "CAGR" sütunu bileşik değil; iki farkın ortalaması: (−118,34 + 261,48)/2 = 71,57.
- 1918057202553929898: grafik başlığı "Borç/Özkaynak Oranı"; metindeki formül Toplam Borç / Toplam Kaynaklar. Değerler (0,60–0,83) kaynak oranıyla uyumlu.
- 1848034791116931310: "İlk grubun %6'ı". Bağlam %60'ı gösterir.
- 2086514064688124094: metin %175; görsel ≈ %173.

Grup C (gönderiler arası ve eşik):
- SAYAS İNA iki farklı sonuç: 1695183583676113357 (2023-08-25) "hisse değeri 147TL bulunmuştur" (147,30); bir gün sonra 1695389783147581542 (2023-08-26) İNA 133,71. Neden belirsiz (parametre değişikliği olabilir; kanıt yok).
- 1695183583676113357: metin 2024 büyümesini %100 der; tablo 150%.
- Ülke risk primi iki gönderide farklı: 1769338011815211270 (2024-03-17) %5,07 = (5,1 − 0,58) × 1,12; 1778895335592472990 (2024-04-12) "Türkiye 5 yıllık CDS %5,1 alınmıştır. Ülke risk primi %5,7" = 5,1 × 1,12 = 5,71. İkinci hesapta ABD CDS düşülmemiş. R070 görseli "(TR CDS − US CDS) × 1.12" der. Karşılaştırma satırındaki "R070 çarpanıyla tutarlı" notu yalnız 1,12 için doğrudur; formül tutarlı değildir.
- Kripto üst sınırı üç değer: %1–5 (1783205936427119005), %4 (1840693444294975693), %5–10 (1860757961032835441).
- 2086152222870536647: eşik "%10 dolayında"; aynı görselde FROTO son pay ≈ %31. Metin yorumlamaz.

Grup D (görselden yeni bulgu ve diğer):
- 1889451595584115079 (görsel açıldı): tabloda 2021/12 satırı yok. 2022/9 yıllık HBK 5,53 = 1,66 (2021/9) + 0,36 + 1,21 + 2,30. Yani "son 4 dönem" bu satırda 4 ardışık çeyrek değil, 5 çeyreklik aralığı kapsar. 2022/12 ve sonrası doğru.
- 1777571511395557531 ve 1886887500183974168: ÖK kârlılığı borç kaynak oranından yeniden üretilemiyor (AKENR 14,45 / 0,4313 = 33,50, tabloda 42,49). Neden belirsiz.
- 1918417139813187678: sektör ortalaması 5,619 yalnız pozitif değerlerin ortalamasıdır (görsel doğrulandı). Negatif TMSN ve OTKAR dışarıda. Bu bir yöntem seçimi; yazılı değil.
- 1698267718074438032: "net kar marjı (sharpe)" adı belirsiz (marj mı Sharpe mi).
- 2093048380297547956: Z sütunu bu çıktıda "son -> önceki" sırasında; tek çift görselinde ters sıra ("Z: -2.010 -> -1.877").

### 4.2 Defter okuma hataları

- R164 (DEFTER OKUMA HATASI, satır 2036840358210945219): eski okuma "EBIT ve vergi bileşik büyüme: e = ebit × (1+g/100)^i". Kod üssü biriktirir (4.1 Grup A).
  - Durum: `defter-3.md` R164 07.10'da düzeltildi ("07.10 düzeltme: eski okuma 'bileşik büyüme'; kaynak X 2036840358210945219").
  - Açık kalan: `defter-fikir.txt` R164 satırı hâlâ eski okumayı taşır: "EBIT ve vergi bileşik büyüme: e = ebit × (1+g/100)^i; vergi = e × t/100 — kural tam (görselden)."
- Olası defter içi tutarsızlık (doğrulanmadı): R068 örneği "tahmini yıl sonu kâr 3.028.232.000 TL" der; R062 ve 2041968928205766731 "3,028,332,000" der. R068 görselini açmadım; hangisinin doğru olduğu belirsiz.

### 4.3 Bu belge için açılan görseller

- Ağırlık: 1850969302347989014-1, 1708030356564160854-1.
- Çift: 1941585010051498309-1, 1858560343200436379-1.
- Çarpan bandı: 1694839230298468742-1, 1696022604472111319-1, 1916743082336285121-1.
- HBK/DuPont/TOPSIS: 1889451595584115079-1, 1918417139813187678-1, 1942540360460259582-1.
- Black-Scholes/VIF: 1897926533991268696-1, 1897926559081660560-1, 1824814340668617001-1, 1825279192390594981-1.
- Uyuşmazlık: 1916743082336285121 görselinde F/K eşikleri yok; eşikler yalnız metinde. 1825279192390594981 görselinde alpha, MSE, R² yok; bu değerler metinden. 1941585010051498309'da satırın verdiği "SAHOL-YKBNK 0,0094 Evet" doğru; korelasyonu 0,953'tür.

---

## 5. Defter için öneri listesi

Sıralama ölçütü: tam parametre + Tansu'nun kendi yöntemi + birden çok gönderide tekrar önce. "Görsel" = parametre görselden Read ile doğrulandı.

### Öncelik 1–5

1. **genişlet R068/R151/R158/R064** — ağırlık tarihçesi: 2023-08 – 2024-04 tabloları çarpan %40 / İNA %60; 2024-10 planı ve defter %60 / %40. Kâr modeli nihai fiyata girmez (TTRAK). Kaynak: 1695389783147581542, 1708030356564160854, 1708049006742417472, 1769338023169143095, 1774367633820750263, 1778895335592472990, 1780322528658886674, 1780322534144999705, 1848034791116931310, 1850969302347989014. Görsel: SAYAS ve TTRAK yeniden hesaplandı, uyuşuyor.
2. **ekle — NEFK–fiyat ayrışması ailesi** (tek hisse + çift sürümü + kâr kalitesi). Kaynak: 1941455577097306576, 1956737745528705173, 1862514363178811538, 1781333788556935603, 1892680047779074122, 1889068388334370953, 1911030895248539760, 1917362530000986239. Parametre metinden; eşik yok, "belirsiz" diye işaretle.
3. **genişlet R262/R228** — karar kuralı "Pv<0.05, ve Tv<Cv"; hat: korelasyon > 0,7 → eşbütünleşme → Z ±2; ML hattı (K-Means + Engle-Granger + OLS hedge ratio). Kaynak: 1874473152455246129, 1941623461744415106, 1941585010051498309, 1941900327655027097, 1912875732646117781. Görsel: p tablosu doğrulandı (SAHOL-YKBNK korelasyonu 0,953, satırda yazılmamış).
4. **genişlet R101** — spread = log fark; 30 HO; sabit std; bantlar ±2 iç, ±4 dış; korelasyon eşiği 0,80 (BIST 0,71). Kaynak: 1857400047589048780, 1858560343200436379, 1860462510752575670, 1862207562378035671, 1891546429388189846, 1941550364911862113. Görsel: ±2..±4 bantları doğrulandı.
5. **ekle — tarihsel F/K-PD/DD SD bandı al-sat**. Kaynak: 1694839230298468742, 1696022604472111319, 1700793391423058126, 1916743082336285121, 1913691337184154030. Görsel: DOAS ve 2014–2023 bant değerleri doğrulandı. Düzeltme: FROTO eşikleri (6,7 / 6,3 / 3,5 / 10) görselde yok, yalnız metinde.

### Öncelik 6–10

6. **genişlet R133/R146/R152 + ekle TTM ilkesi** — kümülatif farkla çeyrek, 4 çeyrek kayan toplam, F/K = fiyat / yıllık HBK, ROE paydası ortalama özsermaye. Kaynak: 1917565014988218574, 1956754276270641304, 1916736171838767120, 1915483602713997579, 1889451595584115079, 1695361936651653499. Görsel: TCELL toplamları doğrulandı. Düzeltme: 2021/12 eksik, 2022/9 yıllık değeri 5 çeyreği kapsar (4.1 Grup D).
7. **genişlet R002/R158 DuPont** — ROE = NKM × ADH × kaldıraç; ADH paydası ortalama aktif; borç eşikleri > %70 riskli, %30–50 dengeli, < %30 muhafazakar. Kaynak: 1979208183236157837, 1918417139813187678, 1918458073099710657, 1771970054793433148, 1777571511395557531. Görsel: aktif kârlılık sektör ort. 5,619 (yalnız pozitifler) doğrulandı.
8. **ekle — Black-Scholes opsiyon fiyatlama** (kod + iki örnek + varsayımlar + delta hedge). Kaynak: 1897926533991268696, 1897926559081660560, 1911177646052131219, 1911177641643983112, 1942962939696156904. Görsel: kod ve AAPL çıktısı 0,21169777 doğrulandı; python ile yeniden hesap uyuşuyor. Düzeltme: delta hedge adedi 1000/0,5 = 2000.
9. **ekle — "sharpe net kâr marjı" istikrar/dışlama kuralı** (> 2; F/K 5–15 ya da 6–16; patron ve büyüme şirketi dışlama). Kaynak: 1781414254576300469, 1794036593734418591, 1698267718074438032, 1780322525055996240, 1709805069644820609. Görsel gerekmedi (metin). Formül belirsiz; defterde "tanımsız" diye işaretle.
10. **genişlet R066 — VIF < 10 süzgeçli F/K regresyonu ve Ridge**. Kaynak: 1824814340668617001, 1825279192390594981, 1825283202191167740, 1826661989126733986, 1781073113205117347. Görsel: VIF < 10 kodu, 10 değişken, 17,49 çıktısı ve Ridge tahmini 20,897 doğrulandı. Düzeltme: alpha 0,26, MSE, R² görselde yok; metinden.

### Öncelik 11–15

11. **genişlet R178 + çeşitlendir Durağan Convex Hull/GARCH**. Kaynak: 1947006461487517762, 1948891823121801615, 1949378649817280840, 1949942724888506647, 1949942729116373465.
12. **ekle — NetYPP / yıllık satış kur duyarlılığı**. Kaynak: 1915860915729166759, 1950865602647646516, 1913865330448879926. Not: 48,6 milyon hatasını düzelt.
13. **genişlet R145/R179 TOPSIS (0,3/0,3/0,2/0,2) + çeşitlendir Gri TOPSIS**. Kaynak: 1942540360460259582, 1947985822071894179.
14. **genişlet R059/R144 — duran varlık artışı taraması** (> %90 + RSI > 50; DV × F/K matrisi). Kaynak: 1950901940524617991, 1950916832409403513, 1954964170585030772, 1955010441526022428, 1956635609449091123.
15. **genişlet R002/R118 — Q2 ardışık artış + CAGR3y**. Kaynak: 1956830336467243263, 1956848925543206980, 1957003613827420651, 1956819684713509048.

### Öncelik 16–20

16. **genişlet R060/R134 + çeşitlendir borç/likidite oranları** (cari oran > 1,5; borç/varlık < %50; asit-test; KV finansal pay %10). Kaynak: 1946652254116684019, 1949414090499112967, 1949421615135240509, 2086152222870536647, 2086514064688124094.
17. **çeşitlendir R110 — Black-Litterman 21 gün kayan pencere ve seçim kuralı**. Kaynak: 2096146762188611697, 1940657356347474399, 1797263549892276362, 1797263555382702421, 2096143361002385717.
18. **genişlet R251/R034 — Pair Health ve tarayıcı sınıfları**. Kaynak: 2096167419941130368, 2093048380297547956.
19. **genişlet R177/R173 — min varyans kapalı form, Sharpe orantılı ağırlık, MC lognormal kodu**. Kaynak: 1878777386839503131, 1822304577560985704, 1760032311100465169.
20. **çeşitlendir R074/R177 — risk parity ve seçim kuralı**. Kaynak: 1822360182682165714, 1827476527899894046, 1944760309123575813.

### Öncelik 21–25

21. **ekle — kripto üst sınırı** (üç değer: %1–5, %4, %5–10; tarih sırasıyla yaz, tek değer seçme). Kaynak: 1783205936427119005, 1840693444294975693, 1860757961032835441.
22. **genişlet R070 — Damodaran ÜRP çalışılmış örneği**; 5,07 ile 5,7 farkını not et. Kaynak: 1769338011815211270, 1778895335592472990, 1911632045777789394.
23. **genişlet R062 — PD/DD pencere tanımı (8Ç + anlık, 36Ç + anlık) ve erken sürümdeki 3Z hatası**. Kaynak: 2041941067025494204, 2041968928205766731.
24. **genişlet R164 — `defter-fikir.txt` satırını defter-3.md'deki 07.10 düzeltmesiyle eşitle**. Kaynak: 2036840358210945219.
25. **ekle — bedelsiz potansiyeli** (tablo alanı 2023'ten beri var, ölçü yok). Kaynak: 2086040274434715957, 1708030356564160854, 1850969302347989014.

### Öncelik 26–30

26. **genişlet R153/R165 — SAYAS İNA çalışılmış örneği** (147,30; 133,71 farkını belirsiz diye not et). Kaynak: 1695183583676113357, 1695389783147581542.
27. **genişlet R030 — sabit oranlı günlük dengeleme oran taraması**. Kaynak: 2053179966284530147, 2053377141421584469.
28. **ekle — kişisel tahsis kuralları** (%80/%20 çekirdek-uydu, temettü yeniden yatırım, DCA, altın/döviz/PPF sepeti). Kaynak: 1761787714523865301, 1769351216369213499, 1783840694043623592, 2100012254636683371, 1987747948675952790.
29. **ekle — callable tahvil (faiz ağacı) ve KMV**. Kaynak: 1851746402830807298, 1851754725680488551; genişlet R061: 1875619396414251058.
30. **çeşitlendir R101 — çift türevleri** (GVX rejim filtresi, spek–spek, tavan tetik, ağ/t-SNE, Granger+HMM). Kaynak: 1999361321435811868, 1941240803654877456, 1857953385569190399, 1898476669851316502, 1922967215969542347.

### Öncelik 31–33

31. **çeşitlendir — VİOP endeks short ile beta ayarlı hedge**. Kaynak: 2097068834284863827.
32. **çeşitlendir R066/R110 — portföyde VIF < 10 (tercih < 5)**. Kaynak: 1823403053212475711, 1822565459905888316.
33. **ekle — EFK değişimi ve bilanço sonrası 40–55 gün fiyat tepkisi (olay çalışması)**. Kaynak: 1941562469320884677.
