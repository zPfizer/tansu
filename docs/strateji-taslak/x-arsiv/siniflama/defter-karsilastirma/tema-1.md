# TEMA 1 — Seçim-momentum, evren-likidite, rejim: defter öneri belgesi

Girdi: `tema-1.jsonl` (132 satır). İlişki dağılımı: genisletir 59, yeni 35, cesitlendirir 29, celisir 9. "DEFTER OKUMA HATASI" satırı yok.
Defter kayıt tarihleri: 2026-08-27 ile 2026-09-06 arası. Bu tarih kaydın deftere yazıldığı tarihtir. Sözün asıl tarihi belirsiz.
Görsel doğrulaması yapılan gönderiler "(görsel doğrulandı)" ile işaretli.

---

## 1. Yeni yöntem aileleri

Bu bölüm iki grubu kapsar: adı defterde olmayan yöntemler ve adı defterde olmayan türevler (cesitlendirir). Satırı "yeni" olup yontem_defterde=var olan aileler de buradadır; bunlar ayrıca işaretli.

### 1.1 AKD skoru (aracı kurum dağılımı davranışı)
- Ne yapar: Aracı kurumların net alım-satımını pencerelere göre puanlar. Toplayan kurum hâlâ taşıyor mu, satışa mı geçti, onu ölçer. Sonra takas ve teknikle süzer.
- Parametreler: pencereler 1 ay, 1 hafta, son 1-2 gün (1941822029767774507); son 3-2-1 gün (1951972240926429210). Son 1 ayda en çok toplayan ilk 5 kurum. Skor 4 = "Son 1 ayda toplayanlar son 1 günde satışta", 3 = "1 ay toplayan ama 1 haftada zayıf", 1 = "Hem toplayan hem de hâlâ taşımaya devam eden". Aylık/haftalık/günlük puan +2/+3/+4 = biriktirme, eksi = realize, sıfıra yakın = kararsızlık (1941442798663643585). Diğer alıcıların payı < %10, ilk 2 kurum yüksek toplama, takas toplu (1978894148645339180). Emeklilik fonları %50 üzeri toplamışsa olumlu (1951972240926429210). Eleme: A_t1 ∩ S_t2, yani t1'de ilk 5 alıcıda olup t2'de ilk 5 satıcıya geçen kurumun hisseleri elenir; sayım s_i^A = Σ 1{i∈A_t}, s_i^S = Σ 1{i∈S_t} (1964614079252938928, görsel doğrulandı: "22 sinde alınan 25 inde satılan hisseler (ilk 5 alıcı tarafından) elenecek / Elenmiş liste final liste olacak").
- Türevler: tek kurumun alım payı ve sırası (Bank of America: BAKAB %62.41, 1970563597626405045; TERA: DSTKF %76.75, 1970590008487878993); ilk 2 alıcı payı ve alıcıdan satıcıya geçiş (EFORC 6 Ekim %88.0, 7 Ekim %56.6, "GEÇİŞ YOK", 1975637160608079950); kurumun birden çok gün topladığı hisseler pay toplamıyla (TERA 131.84, PASEU 127.86, HEDEF 106.35, 1980359173222367308); döngüsel alım izleme, döngü tanımı yok (1980361475215794358). İş akışı: Matrix IQ'dan Excel, ~580–600 satır, günlük veri haftalık/aylık pencereye birleştirilir, kod ~980 satır, takas henüz dahil değil (1971236706264207844).
- Kaynak: 1941442798663643585 (2025-07-05), 1941822029767774507 (2025-07-06), 1951972240926429210 (2025-08-03), 1964614079252938928 (2025-09-07), 1970563597626405045 (2025-09-23), 1970590008487878993 (2025-09-23), 1971236706264207844 (2025-09-25), 1975637160608079950 (2025-10-07), 1978894148645339180 (2025-10-16), 1980359173222367308 (2025-10-20), 1980361475215794358 (2025-10-20).
- Vurgu ve olgunluk: "Yeni geliştirdiğim sistem" (1941822029767774507); "emeklilik fonları %50 üzeri toplamışsa tadından yenmez" (1951972240926429210); "Yarına tavanlar olacak çok eminim" (1978894148645339180). Olgunluk: çekirdek. Pencereler ve skor sınıfları tam; "yüksek toplama" eşiği ve skor formülü yok.

### 1.2 Takas dağılımı okuması (satır "yeni", yontem_defterde=var)
- Ne yapar: Takasta ilk 5'teki kurum tipine göre hisseyi sağlıklı, kurumsal ilgili ya da spekülatif diye ayırır.
- Parametreler: ilk 5'te kalıcı emeklilik fonu/portföy şirketi (Ak Portföy, Anadolu Hayat, İş Portföy) = sağlıklı; kalıcı yabancı kurum (Citibank, Deutsche Bank, HSBC, Merrill Lynch) = kurumsal ilgi; yabancı oranı düşükken ani artış ve kısa sürede satış = spekülatif yabancı; ilk 5'te sürekli yer değiştiren bireysel/küçük kurum, 2-3 gün içinde al-sat = spekülatif (1939414080336670931). Birleşik okuma: takasta yatırım fonları ve Citi dominant + AKD'de toplama + küçük yatırımcı çıkıyor + alış/satış oranı 27.6x + son gün negatif getiri (1983492569574056243).
- Kaynak: 1939414080336670931 (2025-06-29), 1983492569574056243 (2025-10-29).
- Vurgu: belirsiz.
- Olgunluk: çekirdek. Kurum listesi tam; "kalıcı" ve "ani artış" eşiği yok.

### 1.3 Fon portföy birikim skoru (Fund X-Ray)
- Ne yapar: Fonun KAP portföy raporlarını karşılaştırır. Fonun ağırlık ve TL pozisyon artırdığı hisseleri "erken birikim" diye işaretler. Radar olarak kullanılır, al-sat sinyali değildir.
- Parametreler: kural "ağırlık artışı + TL pozisyon artışı + en az 2 rapor boyunca devam eden artış + fiyatın henüz aşırı genişlememiş olması"; "yalnız ağırlık artışı varsa bunu tek başına alış olarak kabul etmiyoruz" (2097384587525812358, görsel doğrulandı). Göreceli Güç 20G = 20G getiri − XU100 20G getiri (2096679609559347293, görsel doğrulandı: TRHOL 86.86 − 1.69 → 85.16; ANELE 63.33 − 1.69 = 61.64). Sütunlar: ağırlık değişimi (puan), TL pozisyon değişimi, ağırlık/TL artış dönemi sayısı, 20G getiri, hacim anomalisi, 20G medyan TL hacim. Skor 0-100; sınıflar GÜÇLÜ ERKEN BİRİKİM / ERKEN BİRİKİM / İZLE / ZAYIF-YOK.
- Kaynak: 2096000569068454011 (2026-09-04), 2096679609559347293 (2026-09-06), 2097384587525812358 (2026-09-08).
- Vurgu: "Bu liste işlem sinyali değildir" (2097384587525812358 görseli).
- Olgunluk: çekirdek. Skor formülü, ağırlıklar ve sınıf eşikleri yazılı değil.

### 1.4 TEFAS fon para akışı (fon sınıfı rotasyonu ve fon sıralaması)
- Ne yapar: Fon ve fon sınıfı net para akışını 1G/5G/20G pencerede okur. PPF'den HSF'ye geçişi risk-on işareti sayar. Fon çıkışının portföy hisselerine baskısını tahmin eder.
- Parametreler: fon evreni 20G net akışa göre azalan sıralanır; sütunlar büyüklük, gözlem 63, akış günü, dönem net akış, 1G/5G/20G net akış, 20G getiri, Sharpe (2094913511986020386). Risk-on = PPF çıkışı + HSF/SER girişi, 5G ve 20G aynı yönde; PPF çıkışı durur ve HSF girişi zayıflarsa momentum kaybı; akış fon büyüklüğüne oranla okunur; 20G getiri × 20G net akış dört bölge (2099556801611977021). Serbest fon akışı borsaya giriş sayılmaz (2097018434563473539). Fon çıkışı → fonda ağırlığı yüksek hisselerde satış baskısı; fonda short varsa küçültme short kapama kaynaklı alım üretir (2099967840405086603). Tüm fonlarda ilk 15 giriş / ilk 15 çıkış, 20G (2099565529698545872); PPF 20G akış (2096644397110534476); PPF 5G akış (2099120376278127042).
- Kaynak: 2094913511986020386 (2026-09-01), 2096644397110534476 (2026-09-06), 2097018434563473539 (2026-09-07), 2099120376278127042 (2026-09-13), 2099556801611977021 (2026-09-14), 2099565529698545872 (2026-09-14), 2099967840405086603 (2026-09-15).
- Vurgu: "borsa için asıl önemli gösterge ... para piyasası fonlarındaki bu büyük likiditenin hisse senedi fonlarına doğru geçiş yapıp yapmayacağı olacak" (2097018434563473539).
- Olgunluk: çekirdek. Pencereler tam; risk-on eşiği yok.

### 1.5 Fon getiri sıralaması (adı defterde yok, R032 türevi)
- Ne yapar: Fonları TEFAS resmi 1 ay getirisine göre sıralar ve risk ölçüleriyle yan yana koyar.
- Parametreler: PPF, 1 Ay Getiri azalan, ilk 10; yanında Sharpe, Sortino, volatilite, max DD, Calmar (2096655622938693877, 2097381679560102246). HSF: Max Drawdown, Sharpe, Sortino, Calmar, Beta, Treynor, M², Jensen Alpha; likidite için günlük stres testi (2096661898385113202). Tüm fonlar, ilk 10, veri uyarısı sütunu "1A uç getiri - teyit, düşük AUM" (2099564220601835538). PPF sınıfı 154 fon, ilk 50 (2099569262847230211).
- Kaynak: 2096655622938693877 (2026-09-06), 2096661898385113202 (2026-09-06), 2097381679560102246 (2026-09-08), 2099564220601835538 (2026-09-14), 2099569262847230211 (2026-09-14).
- Vurgu: "Bu tablo bir performans sıralamasıdır; alınacak fonlar listesi değildir" (2099569262847230211 görseli); "stress testi önemli, onu da he gün yapıyorum likidite kontrolü için" (2096661898385113202).
- Olgunluk: tam (sıralama kuralı belli); seçim eşiği yok.

### 1.6 Fon yatırımcı sayısı filtresi (evren-likidite)
- Ne yapar: Az yatırımcılı fonda yüksek getiriyi manipülasyon, likidite ve çıkış riski sayar. Bu fonu evrenden çıkarır.
- Parametreler: örnek 11 yatırımcı; NMG kümülatif getiri 9944%, Sharpe 106.17. Eşik yok.
- Kaynak: 1979695659432427919 (2025-10-18), 1979721101304361294 (2025-10-19), 1979721927809012208 (2025-10-19).
- Vurgu: "11 kişilik fonda bu kadar yüksek getiri çok tehlikelidir" (1979695659432427919).
- Olgunluk: fikir-çekirdek arası. Eşik yok.

### 1.7 Manipülasyon işaretleriyle evren dışlama (satır "yeni", yontem_defterde=var)
- Ne yapar: Manipüle hisseyi evrenden çıkarmak için beş işaret verir.
- Parametreler: haber/bilanço olmadan ani hacim + sert fiyat artışı; dar aralıkta hızlı hareket, gün içi yukarı çekip son dakikada düşürme; alışta hep aynı kurum, satışta yok; sosyal medyada ani "uçacak" paylaşımları; zarar/borç ile fiyat uyumsuzluğu. Eşik yok.
- Kaynak: 1945020445117264368 (2025-07-15).
- Vurgu: "belli bir kurum alışta hep en önde yer alıyor, satışta ise hiç gözükmüyorsa bu durum şüphelidir".
- Olgunluk: çekirdek.

### 1.8 Thompson Sampling ile hisse önerisi
- Ne yapar: Her hisse için getiri dağılımı kurar. Her gün dağılımdan çekiş yapar. En yüksek çekişi alan hisseyi önerir. Dağılımı yeni veriyle günceller.
- Parametreler: normal dağılım, parametreler geçmiş ortalama getiri ve oynaklık; günlük çekiş; araçlar pandas/numpy/scipy, Yahoo Finance. Pencere yok.
- Kaynak: 1940670472590372957 (2025-07-03).
- Vurgu: belirsiz.
- Olgunluk: çekirdek.

### 1.9 Kısa vadeli momentum dönüşü
- Ne yapar: 1 hafta ya da 1 ay içinde çok yükselen hisselerin sonraki dönemde ortalama altı kalabileceğini söyler. Getirisi düşük ama temeli sağlam hisseleri izler.
- Parametreler: pencere 1 hafta / 1 ay; eşik yok.
- Kaynak: 1946948449275928807 (2025-07-20).
- Vurgu: belirsiz.
- Olgunluk: fikir-çekirdek arası.

### 1.10 Ichimoku bulut taraması
- Ne yapar: Bulut üstü ve dizilim koşullarıyla hisse seçer.
- Parametreler: Tenkan-sen > Kijun-sen; Senkou Span A > Senkou Span B; Close > Senkou Span A; Chikou Span > Close. Periyotlar yok.
- Kaynak: 1847998614548721928 (2024-10-20).
- Vurgu: belirsiz.
- Olgunluk: çekirdek.

### 1.11 Vegas tüneli (adı defterde yok, R214/R128 türevi)
- Ne yapar: Kısa EMA'nın EMA144/EMA169 tünelinin üstüne geçtiği hisseleri bulur.
- Parametreler: EMA13 > EMA144 > EMA169, hisse bazında periyot optimizasyonu önerisi (1845923939736080720). EMA12'nin EMA144 ve EMA169'u "yeni" yukarı kesmesi, "yeni" penceresi yok (1839308965039190302). 15 dakika zaman dilimi (1838670037353374138). Günlükte para girişi şartıyla (1846640825771377067, 1846638825864413237).
- Kaynak: 1838670037353374138 (2024-09-24), 1839308965039190302 (2024-09-26), 1845923939736080720 (2024-10-14), 1846638825864413237 (2024-10-16), 1846640825771377067 (2024-10-16).
- Vurgu: "Çok basit bir stratejisi var ... Bununla tavan hisseler bulduk" (1845923939736080720); "günlükte iyi çalışır. para girişini takip etmek şartı ile" (1846640825771377067).
- Olgunluk: tam (1845923939736080720 dizilimi); kısa EMA 12/13 farkı için bkz. 4. bölüm.

### 1.12 Supertrend / MOST / KAMA trend kapısı (adı defterde yok, R148 türevi)
- Ne yapar: Trend takip göstergesini yön kapısı yapar, ikinci göstergeyi tetik yapar.
- Parametreler: Supertrend yukarı/aşağı listesi (1838663920996831643); Supertrend + son gün RSI14 > 50 (1841917340419559794); bullish listesi (1843373717247922211); BIST100 günlük (1844830887294197939); Supertrend yukarı + son gün KAMA al (1853065056759550021); MOST al sinyali (1844832419821539723). Hiçbirinde ATR periyodu ve çarpan yok.
- Kaynak: 1838663920996831643 (2024-09-24), 1841917340419559794 (2024-10-03), 1843373717247922211 (2024-10-07), 1844830887294197939 (2024-10-11), 1844832419821539723 (2024-10-11), 1853065056759550021 (2024-11-03).
- Vurgu: belirsiz.
- Olgunluk: çekirdek (kapı yapısı belli, parametre yok).

### 1.13 Golden Cross EMA50/EMA200 (adı defterde yok, R128/R131 türevi)
- Ne yapar: EMA50'nin EMA200'ü yukarı kesmesini hisse taramasında ve endeks rejiminde kullanır.
- Parametreler: EMA50 EMA200'ü 1 gün önce yukarı keser (1844838137366806837); görselde 2 gün önce (1844070126406250885); BIST100 "EMA Crossover (50-200)" (1847537834397237420).
- Kaynak: 1844070126406250885 (2024-10-09), 1844838137366806837 (2024-10-11), 1847537834397237420 (2024-10-19).
- Vurgu: belirsiz.
- Olgunluk: tam.

### 1.14 Diğer seçim-momentum türevleri (tek gönderi)
- RoC(9) sıfır kesişi: son kapanış gününde RoC 9 0 eksenini yukarı keser; grafikte RoC 9/20/50 (1840816385540440325, 2024-09-30; 1840826561273979333, 2024-09-30). Olgunluk: tam. R105 türevi.
- MACD pozitif uyumsuzluk: fiyat alçak dip, MACD yüksek dip; evren BIST30; eşik yok (1837867391310540998, 2024-09-22). Olgunluk: çekirdek. R116 türevi (R116 gizli uyumsuzluk).
- Momentum breakout: düşen direnç kırılımından önce sinyal verir; günlük çalıştırılır (1862055089713602762, 2024-11-28). Kanıt: "momentum breakout çok daha önce yakaladığı için yazmadım". Olgunluk: fikir.
- ANP (Analitik Ağ Süreci): TOPSIS yerine kriterler arası bağımlılık ve geri besleme; 7 adım; örnek kriterler kârlılık, borçluluk, fiyat oynaklığı, sektör büyüme potansiyeli (1944868638307311952, 2025-07-14). Olgunluk: çekirdek. R179/R145 türevi.

### 1.15 ADX + BBW persentil yatay piyasa filtresi (satır "yeni", yontem_defterde=var)
- Ne yapar: Yatay piyasayı tanır ve işlem açmayı durdurur.
- Parametreler: ADX < 20 VE BBW son 100 barın en düşük %20'lik diliminde (rolling percentile) → işlem açma. BB periyodu/sapması ve ADX periyodu yok.
- Kaynak: 2004287128214356186 (2025-12-25).
- Vurgu: "Tam teşekküllü bir agent yazmak yerine bu iki metriği birleştiren matematiksel bir filtre kurmanız yeterlidir."
- Olgunluk: çekirdek (eşikler tam, periyotlar yok).

### 1.16 Takvim etkileri ve gap (rejim)
- Haftanın günü etkisi: ortalama günlük getiri haftanın gününe göre; kötü getirili günde işleme girilmez; "ralli döneminde salı, şimdi pazartesi" (1891539591531823394, 2025-02-17); çarşamba endeks için kötü (1891948299474616579, 2025-02-18). Ölçüm dönemi yazılı değil. Olgunluk: çekirdek. R183 türevi.
- Çok gaplı seans ertesi temkin: açılışı görmeden işlem yapma (1866237714728645031, 2024-12-09; satır "yeni", yontem_defterde=var). Kanıt: "Açılışı görelim. Acele işlemler yapmayın." Olgunluk: fikir.

### 1.17 Makro rejim aileleri (altın ve faiz)
- GSYİH büyüme yavaşlaması → altın: BEA reel GSYİH, çeyreklik yıllıklandırılmış, art arda ≥2 çeyrek yavaşlama; ölçü dönem içi NYMEX altın getirisi; 13 dönemin 9'u pozitif (+24.7, +21.7, +15.8, +0.1, +26.9, +3.4, +28.0, +16.4, +40.4), 4'ü negatif (−7.5, −10.4, −6.7, −2.4) (2083875779218198689, 2026-08-02). Tetik teknik resesyon değil, yavaşlama sinyali (2083875781457928398, 2026-08-02). Güncel uygulama 2026/Q1 2.1, Q2 1.5, Q3 önemli (2083875783332741531, 2026-08-02). Olgunluk: tam (koşul ve ölçü belli).
- Japonya likidite sıkışması → Altın/Gümüş rasyosu: BoJ faiz artışı / Japon tahvil satışı → yen carry çözülmesi → gümüş daha sert düşer → rasyo 80 → 90-100; eylem gümüşten altına ya da nakde (1992188666593112507, 2025-11-22). Olgunluk: çekirdek, eşik yok.
- Negatif reel faiz → altın: reel faiz = nominal faiz − enflasyon; faiz indirimi + yüksek enflasyon → negatif reel faiz → altın (2083953538661539956, 2026-08-02). Olgunluk: çekirdek. R071 türevi.
- Vasicek faiz patikası: r0 = 0.50, θ = 0.30, 1 yıl simülasyon, κ ve σ yok; DCF iskonto oranı; faiz düşüş eğilimi → bankacılık dışı/borçlu sanayi olumlu; faiz oynaklığı yüksek → defansif (1925776822249144708, 2025-05-23). Satır "genisletir R166/R229" diyor, yontem_defterde=yok. Olgunluk: çekirdek.
- Kelebek etkisi ilk ipuçları: düşük volatilite = sıçrama riski; anlamsız habere düşük hacimli hissede ani tepki; korelasyon kırılması; opsiyonda olağan dışı primlenme (1914692264384774310, 2025-04-22). Olgunluk: fikir-çekirdek. R077/R034 türevi.

---

## 2. Genişletmeler (R kaydı başına)

### R192 — EMA kümesi üstü kapanış
- Defterde: SMC tarama kodu; "fiyatın, o tepesindeki Mor ve Turuncu çizgilerin de üzerine çıkıp kalıcı olması gerekir" (EMA kümesi, periyot yok).
- X ekler (kümenin periyotları): son gün kapanış > EMA5, EMA14, EMA34, EMA55 (1842563290372940025, 1847729477876666512); + son gün RSI14 > 50 (1842574480692150662, 1847730820838281340, 1848807342705676791, 1851721104156774497).
- X ekler (varyant): kapanış > EMA14, EMA34, EMA55 ve RSI(14) son gün 50'yi yukarı geçer (1844069225851469851, 1844825767483482566, 1845913799976800345). Çalışılmış örnek: TUREX EMA14 93.36, EMA34 91.43, EMA55 87.24, kapanış 94.60 (1844069225851469851 görsel özeti).
- X ekler (para girişi ile): + CMF son 3 gün > 0, önceki 3 gün < 0 (1848806602553385447, 1851720332580966708, 1852063288533881329); liste para giriş-çıkışıyla süzülür (1852065846069465325).
- Uyarılar: "Bu çok sinyal üretiyor ama yine de çeşitlilik iyidir" (1848807342705676791); "Zaten tavan olmuş dikkat" (1852063288533881329); sinyal gelen ETILR için "UZAK DURUN" (1848806602553385447); "teknik ve temel analizinizi yapınız" (1844825767483482566).

### R137 — Çok aşamalı karar destek (CMF, ML, Sharpe)
- Defterde: 3. aşama "ADX ve Para Akışı (CMF)" teyit; YSA momentum; eşik yok.
- X ekler (CMF tanımı): para girişi = CMF son 3 gün > 0, önceki 3 gün < 0; EMA5 > EMA13; RSI21 > 50; CMF periyodu yok (1846310706263871703). "Son 3 gün para girişi artan" (1848427208005521904); CMF Buy/Sell son 3 güne göre (1851723604758507677).
- X ekler (sıra değişikliği): "Aslolan para girişidir. Para yoksa gerisine bakmaya gerek yok." Defterde CMF teyit aşaması; X'te ilk kapı (1851719680052072481).
- X ekler (ML ve pencere): regresyon kırılımı penceresi 60 gün, momentum hareketli penceresi 16 gün, ML momentum olasılığı (1890128183972008095); X günlük penceredeki momentum liderlerinin lokal zirveleri ML girdisi, fiyat tepkisi 1–2 gün gecikebilir, X yazılı değil (1920446141105103040); eleme olasılık > 0.50, kontrol sütunları "HACİM 1.5x | CMF ARTAN | ADX>20" işaret olarak, GSDDE 0.728 (1965629890100941012).
- X ekler (Sharpe eşiği): Sharpe > +0.20 = momentum alanı. Eşik @upotaker'ın; Tansu onaylıyor: "Bu da o hisseleri benim sistemimde momentum alanına sokar" (1905021778126102810).

### R196 / R230 — OBV ve sinyal uyumu
- Defterde: R196 fiyat-OBV senkronu, eşik yok; R230 "İki veya daha fazla teknik göstergenin aynı anda aynı yönde sinyal üretmesi".
- X ekler: son gün EMA5 > EMA20, EMA10 > EMA20, ikisi EMA20'yi yukarı kesmiş; MACD > sinyal; RSI14 > 50 ve önceki gün ≤ 50; son 5 gün OBV değişimi > 0; MACD parametreleri yok (1847008515014922537). Varyant: kapanış > EMA5 + "EMA5-10-20 MACD RSI14-50 VE OBV50" (1851719680052072481 görsel özeti; OBV50 tanımı belirsiz).

### R212 / R131 — EMA200
- Defterde: R212 "250SMA. (bu 200SMA 200EMA 250EMA' da olabilir)" giriş bileşeni; R131 MA üstü alış, altı satış, süre yok.
- X ekler: tetik "Son gün EMA 200'ü yukarı kesen hisseler" (1844068170853949930); endeks için süre 200 günlük EMA, altı olumsuz (1827078541797945391).

### R255 — WaveTrend
- Defterde: WaveTrend yardımcı teyit, parametre yok.
- X ekler: WT(10,21), WT_1/WT_2, aşırı satım bandı −50/−60, BIST30, son gün al (1845369437441933344); "bunu birşeyler le kombinlemek lazım" (1848426907441692797).

### R200 / R202 — Beta, alpha, kayan ölçüler
- Defterde: R200 beta formülü ve rejime göre beta; R202 "Rolling alpha Rolling skewness", pencere yok.
- X ekler: Faz 1'de fiyat sinyale zayıf tepki verirse kazanç zor; tepki varsa yükselen endekste yüksek beta + yüksek alpha (1878050003647697038); kural Faz 2 ve 3 için de geçerli (1878050007133106656); aylık ve günlük ayrı CAPM, GARAN Alpha(M) 0.0262466, Beta(M) 0.989105 (1878132805504254308).
- X ekler: kayan pencere 20 ya da 60 gün, her gün yenilenir; üçlü yüksek kayan alpha + yüksek kayan Sharpe + düşük beta; politik yoğunluk yüksekse düşük beta (1953112693407203768).

### R214 / R167 / R116 — Tarama birleşimi
- Defterde: R214 EMA5>EMA8>EMA13 + destek tepkisi; R167 EMA5/8/13/34 çizili, kural yok.
- X ekler: RSI pozitif uyumsuzluk + kapanış marubozu + alternatif momentum + son gün breakout + EMA 5>8>13>34 dizilimi; görselde CDLMATCHINGLOW / CDLCLOSINGMARUBOZU (1915163157531910187).

### R166 / R069 — Temel + teknik birleşimi
- Defterde: temel fırsat + teknik kapı; takas ayağı yok.
- X ekler: teknik ayak 60 günlük direnç kırılımı + hacim artışı; temel örnek net kâr %80 artış; üçüncü ayak takas: alıcılar kurumsal, satıcılar küçük yatırımcı (1935015198277951650).

### R110 — Sharpe
- Defterde: Max Sharpe teğet portföy; formül yok.
- X ekler: Sharpe = (Getiri − Risksiz Faiz) / Volatilite; getiri yıllık ya da son 6 ay; risksiz faiz örnek %30 yıllık; evren BIST100/BES fonları; azalan sıralama (1940482825427235036).

### R097 — GARCH
- Defterde: "garch ve standart sapma ... örnek ile göstereceğim" (yalnız fikir).
- X ekler: her hisseye ayrı GARCH; ölçü = ortalama getiri / ortalama GARCH tahmini volatilite; yüksek korele hisselerde düşük riskli seçilir (1940666220354654588). GARCH volatilitesi yükselen dönemde Sharpe yüksek VE beta düşük hisse; araçlar arch/statsmodels (1952471946383265824). GARCH derecesi ve pencere yok.

### R120 — 12 aylık momentum
- Defterde: 12 aylık getiri, 10 decile, aylık yenileme.
- X ekler: momentum = Π(1 + aylık getiri) − 1, temettü dahil; Apple 2014 örneği %40,62; alternatif pencereler 1/3/6 ay, 3/5 yıl (1946925694652674087).

### R178 — Convex hull
- Defterde: "Sektör rotasyonu Convex Hull ile VZA analizini birlikte çalışırsanız" (yalnız fikir).
- X ekler: sektör beklenen getiri ve riski → convex hull → çizgi üzerindeki sektörler → Sharpe → ağırlık (1947024537079468538). Sıra: son 30-90 gün getirisi yüksek sektörler → convex hull → sektör içi cross-sectional momentum → Markowitz ya da Black-Litterman (1949014576458023063).

### R032 / R033 — Sektör rotasyonu
- Defterde: R032 pencereler 30/60/90 gün; R033 anomali |30g getiri| > %50 çıkarılır.
- X ekler: her 90 günde son 90 gün getirisine göre ilk 3 sektör, eşit ağırlık, 90 gün değişiklik yok; test 1/2/3 sektör × 30/60/90 gün; en iyi "3 Sectors / 90 Days 5.282638" (1947774961801736417, görsel doğrulandı; değerin birimi belirsiz). Sektör getirisi = sektördeki hisselerin ortalama getirisi (1947783188945731622).

### R002 — Sektör zinciri
- Defterde: sektör rotasyonu → yüksek korele sektörler → lider sektör; sayı yok.
- X ekler: son 30 gün getirisine göre ilk 10 sektörün 30 günlük getiri korelasyon matrisi (1951627374774087770); 5 yıl veri, en hızlı 10 sektör, sektör içinde son 10 günde yükselen trende temas / pullback / tepki veren hisseler (1951634776156258423); momentumu en yüksek 10 sektörün faz alanındaki en güçlü 10 hissesi + bayrak taraması (1955360082641948922).

### R225 / R226 — Derinlik
- Defterde: alış tarafı kalın, satış ince = iyi sinyal; eşik yok.
- X ekler: derinlik alış/satış oranı (örnek 59.2x) + günlük değişim negatif = alım baskısı adayı (1983491105631993940).

### R022 — Momentum penceresi
- Defterde: Mom1–Mom5 dilimleri; momentum penceresi yok.
- X ekler: lookback örnekleri 5 / 10 / 20 gün; Tansu'nun kendi değeri gizli (1993444658085826808).

### R183 — Mevsimsellik
- Defterde: ≥%70 yükselen ay; Ocak örneği; anlamlılık testi yok.
- X ekler: hisse bazında t testi, p < 0.05 anlamlı (KRDMB t 2.549, p 0.027); ek sütunlar Sharpe, Win/Loss, Skewness, Kurtosis, Shapiro; az veride W/L INF'e güvenme; p 0.0536 "wild card" (2009899784748794098). XU100 Şubat 2015–2026: 5 pozitif / 7 negatif, başarı %41.7, ort. −0.54%, maks +8.20%, min −11.03%, std 5.02% (2018404523635515480).

### R176 — Eğim × R² momentum
- Defterde: kod tam; pencere uzunluğu yok.
- X ekler: çalışılmış örnek ALARK yıllıklandırılmış eğim 1.5565 × R² 0.8749 = 1.3617; grafik başlığı "Son 250 Gün" (pencere olabilir, kesin değil); 0-1 "Sinyal" serisi ve 0.5 çizgisi tanımsız (2018765685091139701).

### R031 — VRP
- Defterde: VRP = IV − RV; VOL AL eşiği −0.005 (defter: "okunuş belirsiz").
- X ekler: zincir sektör rotasyonu → kârlı sektörler → VRP < 0 hisselere eşit tutar (~20.000 TL/hisse); 2026-08-01 alım, ana para 100,000 TL, 5 hisse (BMSTL −0.0561, CEMAS −0.1054, BRSAN −0.1095, DOKTA −0.1337, CELHA −0.6717); 2026-08-19 maliyet 99,513.08 → 108,420.92 TL, %8.95 (2089838087606087814, görsel doğrulandı). Eşik farkı (−0.005 / < 0) için bkz. 4. bölüm.

### R028 / R029 — VRP kesişim kümesi
- Defterde: iki kodun kesişim kümesi; implied move örneği %10.4.
- X ekler: kesişim çıktısı Skew, IM%, RV%, IV%, VRP, Vade; INTC 0.189, 12.6%, 79.9%, 60.7%, −19.2%; MU 0.192, 12.7%, 103.5%, 62.2%, −41.3%; vade 2026-09-11; ABD hisseleri (2090161750444327119, görsel doğrulandı; VRP = IV − RV hesabı tutuyor).

### R118 / R257 — NH−NL piyasa genişliği
- Defterde: R118 NH−NL 20 ve 65 gün, eşik yok; R257 katılım zayıf, sayı yok.
- X ekler (formül): NH/NL Close'a göre 52 hafta; 5g toplam = son 5 işlem günü NH−NL toplamı, haftalık değer W-FRI; eşikler N'e göre sabit: boğa teyidi +0.80 × N, spike/panik −1.30 × N, günlük ±51 (= 0.10 × N); N = 510 → +408 / −663 (1956454944967700857, görsel doğrulandı).
- X ekler (okuma): birkaç gün üst üste NH−NL ≥ +51 ve NH−NL_5D ≥ +408 → boğa teyit; NH−NL < 0 kalırsa rüzgâr ters; −663 altına inip üstüne dönüş = alış adayı (1956359671154884947). Çalışılmış örnek 2025-08-15: NH−NL = 35, güçlü gün eşiğine kalan +16 / −86; 5g = 177, boğa teyidine kalan +231, spike eşiğine mesafe 840 (1956454944967700857 görseli; hesaplar tutuyor).
- X ekler (karar örneği): 20 gün NL−NH farkı 102, 5 günlük birikimli −365 → güçlü ayı; 65 gün −19, boğa eşiği için en az 70 hisse daha; karar alım yok, spike dönüşü beklenir (2027084975686689177).

### R210 / R209 — VIX bantları ve korelasyon rejimi
- Defterde: R210 negatif korelasyon arar; "VIX < Hızlı Bantlar & VIX RSI < MAV"; bant parametreleri yok. R209 SMA 20/50.
- X ekler (bantlar): yavaş bant BB(20,2) ofset 10; hızlı bant BB(10,1) ofset 5 (1996656703665066072, görsel doğrulandı: "Yavaş Üst Bant (20,2 | Off:10)", "Hızlı Üst Bant (10,1 | Off:5)").
- X ekler (korelasyon): pencere 30 gün, ±0.5 kesik çizgiler; VIX RSI(200), MAV = SMA(10) (1999759348868796729, görsel doğrulandı). Rejimler: negatif normal, pozitif anomali, sıfıra yakın belirsizlik; stratejiler Korkuyu Satın Al / Rehaveti Sat / Ayrışmayı Oyna; "VIX >25 hızla yükseliyor → nakda geç/short"; pozitif korelasyonda Dolar/TL kontrolü; Renko kutu 100 (1999567041905492120).
- X ekler (çalışılmış örnek): 2025-03-18 korelasyon 0.62 "POZİTİF (RİSKLİ)" → nakitte bekle; long skoru 4/5 iken sonra sert düşüş; RSI ortalaması SMA 14; VIX hızlı bant üst limiti SMA 10 + Std (25.98) (1999774979194540153).

### R188 — Piyasanın Nabzı raporu
- Defterde: yedi gösterge ve değerleri; tanım eşikleri kısmi.
- X ekler (2001696307468022197, görsel doğrulandı): korelasyon −1'e yakın sağlıklı, +1'e yakın anomali; fiyat > SMA 18/35 boğa (satır bunu atlamış); AO yeşil bar; RSI > SMA 14(RSI); VIX < "Hızlı Bant" (SMA 10 + Std); ADX > 25 güçlü trend, +DI/−DI yön; hacim > SMA 20 teyit; skor "İLK 5 KURALA GÖRE" 4/5.

---

## 3. Çelişkiler

Karar verilmedi. Her konuda iki taraf, tarihler ve olasılık var. Defter tarihi kayıt tarihidir; sözün asıl tarihi belirsiz.

### 3.1 HMM ile rejim tespiti — R091
- Gönderi tarafı: "Yeşil: Belirli bir rejime (state 0) denk gelen fiyat noktalarını temsil eder." (1898475888250916913, 2025-03-08); siyah "yüksek volatilite (paniğe yakın hareketler) veya trend dönüşleri" (1898475890918514837, 2025-03-08); "HIDDEN MARKOV MODEL" (1898475893422690610, 2025-03-08); "Yeşilde kal, kırmızıda tetikte ol, siyahta bekle, turuncuda analiz yap! ... siyahta yatırım yapılmaz." (1912487017788698997, 2025-04-16); "Derin öğrenme temelli rejim detektörleri bu anlamda klasik modellerin çok daha ilerisindedir" (1913224177407926759, 2025-04-18).
- Defter tarafı: R091 (kayıt 2026-08-27): "Trend rejim değişikliği için HMM yapmanıza gerek yok Koç gibi korelasyon varken hiç gerek yok hemde".
- Sıra: gönderiler önce (2025-03/04), defter kaydı sonra.
- Olasılık: tarihçe. Kanıt: R091 sonra geliyor ve kesin dil kullanıyor; VIX sistemi (R210, 1999567041905492120) korelasyonla rejim okuyor. Bağlam olasılığı da var: R091 "trend rejim değişikliği" diyor; HMM gönderisi volatilite davranışını sınıflıyor ("HMM yönü değil davranışı ölçer", 1912487017788698997). Hata kanıtı yok.

### 3.2 Ertesi gün yön tahmini — R185
- Gönderi tarafı: "Yarın %69.85 ihtimal ile yukarı yönlü kapanış yapacağız. Yüksek betalı hisselerde pozisyon alalım." (1892656632976318511, 2025-02-20); "Tahmin algoritmam da yarın için %68 ihtimal ile eksi kapanış verdi." (1907899832108274069, 2025-04-03).
- Defter tarafı: R185 (kayıt 2026-08-28): "Finansal piyasalarda algoritma geliştirenlerin düştüğü en büyük tuzak, fiyatın gelecekteki yönünü 'tahmin etmeye' çalışmaktır."
- Sıra: gönderiler önce, defter sonra.
- Olasılık: tarihçe ya da bağlam. Tarihçe kanıtı: 1913224177407926759 (2025-04-18) zaten "fiyat seviyesini tahmin etme, rejimi tespit et" diyor; görüş Nisan 2025'te dönmüş olabilir. Bağlam kanıtı: R234 "temel modelim de bir makine öğrenmesi algoritmasına dayanıyor" ve "%70 gibi bir değer yakalarsanız bu harika bir sonuçtur"; yani olasılık modeli defterde de var. R058 "Ml modelleri sıkıntılıdır" ile de gerilim var. Hangisi olduğu belirsiz.

### 3.3 Win rate süzgeci — R140, R234
- Gönderi tarafı: "Winrate %80'den büyük olanları tarattım"; görsel süzgeç "Win Rate >= %80.0 | İşlem >= 5 | Profit Factor >= 0.00 | Komisyon: %0.10"; tabloda 5-7 işlemle %85.7-%100 seçiliyor (2092745592661246196, 2026-08-26).
- Defter tarafı: R140 (kayıt 2026-08-28): "Yüzdelik doğruluk ..., acemi yatırımcıların bir takıntısıdır ancak bir işlem sistemini değerlendirmek için çok önemli bir kriter değildir." R234 (kayıt 2026-08-28): "%90'lar ise mümkün değildir."
- Sıra: gönderi 2 gün önce, defter sonra.
- Olasılık: bağlam. Kanıt: gönderide süzgeç talep bölgesiyle birlikte aday daraltma için kullanılıyor; R140 sistem değerlendirmesinden söz ediyor. Hata olasılığı: Profit Factor >= 0.00 hiçbir hisseyi elemez (bkz. 4. bölüm); 5 işlemle %80+ oranı küçük örnek. Karar belirsiz.

### 3.4 200 günlük ortalamanın altında alım — R131, R212, R199
- Gönderi tarafı: dört kriter PD < DD, RSI 30 altından yukarı dönüş, F/K 5–15, fiyat 200 günlük ortalamanın altında; "200 günlük ortalamanın altında işlem görmesi ise hâlâ genel piyasa trendinin altında kaldığını, ancak bir dönüş potansiyeli taşıdığını ima eder" (1938905375119434125, 2025-06-28).
- Defter tarafı: R131 (kayıt 2026-08-28): "eğer piyasa hareketli ortalamanın altındaysa, bu durum satış yönlü"; R212 (kayıt 2026-08-28): "Fiyat, 250 günlük hareketli ortalamanın altında bir kapanış yaparsa pozisyondan çıkın."; R199 (kayıt 2026-08-28): "Düşüş trendi (Lower Highs & Lower Lows) yapan bir hissede bu strateji uygulanmaz."
- Sıra: gönderi önce, defter sonra.
- Olasılık: bağlam. Kanıt: gönderi değer + dönüş stratejisi; defter kayıtları trend stratejileri. R233 de RSI(14) 30 yukarı kesişiyle giriş veriyor. R144 "Sadece 'PD/DD oranı 1'in altında, o halde bu hisse bedava' diyerek alım yapmak büyük bir hatadır" diyor; gönderi PD/DD'yi tek başına kullanmıyor. Tarihçe kanıtı yok.

---

## 4. Gönderi içi hatalar ve tutarsızlıklar

### 4.1 Metin–görsel uyuşmazlıkları (görsel doğrulandı)
- 2097018434563473539 (2026-09-07): metin "Hisse senedi fonlarında ... Son bir günde 4,24 milyar TL ... net giriş" ve PPF için "son beş günde 33,1 milyar TL giriş" diyor. Tabloda HSF 1G "-₺4.24 Mr", PPF 5G "-₺33.08 Mr". İkisi çıkış. Metin işareti kaçırmış.
- 2090161750444327119 (2026-08-19): metin "10/09/2026 tarihine kadar" diyor; görselde vade "2026-09-11". Bir gün fark. Metin "%12 oranında yukarı yönlü hareket" diyor; R028 ise IV'ye göre "+- yönde" hareket diyor. IM% sütununda yön bilgisi yok. Yön iddiası belirsiz.
- 1956454944967700857 (2025-08-15): ikinci görselin başlığı "BIST 50 | Günlük NH−NL"; aynı görselde "N (evren): 510". Başlık ve evren uyuşmuyor.
- 2001696307468022197 (2025-12-18): "MEVCUT HACİM: 0 | ORTALAMA HACİM: 5,036,280,000". Hacim verisi gelmemiş. R188'de de "mevcut 0" var. Hata tekrar ediyor.

### 4.2 Gönderi içi ve gönderiler arası tutarsızlıklar
- Fund X-Ray kuralı "fiyatın henüz aşırı genişlememiş olması" (2097384587525812358). Aynı sistem TRHOL için "fiyat çok genişledi" yazıp "GÜÇLÜ ERKEN BİRİKİM" veriyor (2096000569068454011, 2096679609559347293; görsel doğrulandı).
- Aynı dönem (2026-07-01 → 2026-08-01), aynı ağırlıklar, farklı skor: TRHOL 77 (2096000569068454011) / 77 (2096679609559347293) / 72 (2097384587525812358); ALKLC 72 / 66; AKBNK 78 "GÜÇLÜ" / 74 "ERKEN". XU100 20G girdisi 0.97'den 1.69'a değişmiş. Olası neden veri güncellemesi; formül değişikliği de olabilir. Belirsiz.
- AKBNK "YENİ GİRDİ", önceki ağırlık 0.00, ama "Ağırlık Artış Dönemi 2" (2096000569068454011, 2096679609559347293). Tek raporla yeni giren hisse için 2 dönem artış belirsiz.
- Vegas tüneli kısa EMA'sı: EMA12 (1839308965039190302, 2024-09-26) ve EMA13 (1845923939736080720, 2024-10-14). Hata mı varyant mı, belirsiz.
- Trend ortalaması: VIX master görselinde "SMA 20/50" (1999759348868796729; R209 de SMA 20/50); rapor görselinde "SMA 18/35" (2001696307468022197; R188 de 18/35). Aynı sistem ailesinde iki parametre. Belirsiz.

### 4.3 Hesap ve formül notları
- 2092745592661246196: süzgeç "Profit Factor >= 0.00". Profit factor tanım gereği 0'dan küçük olamaz. Bu süzgeç hiçbir hisseyi elemez.
- 2018765685091139701: 1.5565 × 0.8749 = 1.36178, yuvarlanınca 1.3618. Görsel 1.3617 yazıyor. Girdiler yuvarlanmış olabilir; fark küçük.
- 2096679609559347293: TRHOL 86.86 − 1.69 = 85.17; görsel 85.16. Yuvarlama farkı.
- 2089838087606087814: VRP < 0 eşiği kullanılıyor; R031 görselinde AL eşiği −0.005 (defter: "okunuş belirsiz"). Eşik farkı mı, okuma farkı mı, belirsiz.
- Doğru çıkan hesaplar: NH−NL eşikleri (0.80 × 510 = 408; 1.30 × 510 = 663; kalan 231 ve 840); VRP = IV − RV (INTC, MU); VRP portföyü %8.95.
- Yazım: 1999567041905492120 tablosunda "Hakda Geç" (Nakda Geç).

### 4.4 Defter okuma hataları ve sınıflama notları
- tema-1.jsonl'de "DEFTER OKUMA HATASI" satırı yok.
- Satırı "yeni" olup yontem_defterde=var olanlar: 1939414080336670931, 1983492569574056243 (Takas analizi), 1945020445117264368 (Manipülasyon işaretleri), 1866237714728645031 (Gap), 2004287128214356186 (BBW persentil). Ad defterde geçiyor, bu amaçla geçmiyor.
- 1925776822249144708 "genisletir" diyor ama yontem_defterde=yok (Vasicek). Bu belgede yeni aile sayıldı.
- 1941442798663643585 "yeni" diyor ama R082'yi gösteriyor; R082 konsolidasyon–kırılım kaydıdır, AKD ile ilgisi zayıf.
- 2001696307468022197 satırı SMA 18/35 kuralını atlamış; görselde var.

---

## 5. Defter için öneri listesi (öncelik sırasıyla)

Öncelik ölçütü: tam parametre + Tansu'nun kendi yöntemi + birden çok gönderide tekrar. İlk 10 maddenin görsel parametreleri Read ile açıldı ve doğrulandı; uyuşmazlık yok, yalnız 4. bölümdeki notlar var.

### Öncelik 1–5
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 1 | genişlet | R192: EMA kümesi = EMA5/14/34/55 üstü kapanış + son gün RSI14 > 50; varyant EMA14/34/55 + RSI(14) son gün 50 yukarı geçiş | 1842563290372940025, 1842574480692150662, 1844069225851469851, 1844825767483482566, 1845913799976800345, 1847729477876666512, 1847730820838281340, 1848807342705676791, 1851721104156774497, 1852065846069465325 |
| 2 | genişlet | R137: para girişi tanımı CMF son 3 gün > 0 ve önceki 3 gün < 0; CMF'yi teyitten ilk kapıya al | 1846310706263871703, 1848806602553385447, 1851720332580966708, 1852063288533881329, 1851719680052072481, 1848427208005521904, 1851723604758507677 |
| 3 | genişlet | R118: NH−NL eşik formülü (N=510; günlük ±0.10N=±51; 5g boğa +0.80N=+408; spike −1.30N=−663; −663 altından dönüş = alım adayı) | 1956359671154884947, 1956454944967700857, 2027084975686689177 |
| 4 | ekle | AKD skoru ailesi: pencereler 1 ay/1 hafta/1-2 gün, ilk 5 kurum, skor 4/3/1, diğer alıcılar < %10, A_t1 ∩ S_t2 eleme | 1941822029767774507, 1941442798663643585, 1951972240926429210, 1964614079252938928, 1978894148645339180, 1971236706264207844, 1975637160608079950 |
| 5 | genişlet | R210/R188: VIX bantları BB(20,2) ofset 10 ve BB(10,1) ofset 5; korelasyon 30 gün ±0.5; VIX RSI(200), MAV SMA(10); rapor kuralları (RSI > SMA14, ADX > 25, hacim > SMA20) | 1996656703665066072, 1999759348868796729, 1999567041905492120, 1999774979194540153, 2001696307468022197 |

### Öncelik 6–10
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 6 | ekle | Fon portföy birikim skoru (Fund X-Ray): ağırlık artışı + TL artışı + ≥2 rapor + fiyat aşırı genişlememiş; Göreceli Güç 20G = 20G getiri − XU100 20G; skor formülü eksik diye işaretle | 2097384587525812358, 2096679609559347293, 2096000569068454011 |
| 7 | genişlet | R031: sektör rotasyonu → VRP < 0 hisselere eşit tutar; çalışılmış örnek 99,513.08 → 108,420.92 TL, %8.95 | 2089838087606087814 |
| 8 | genişlet | R032: her 90 günde son 90 gün getirisine göre ilk 3 sektör, eşit ağırlık; test tablosu (3 sektör-90 gün 5.282638); sektör getirisi = hisse ortalaması | 1947774961801736417, 1947783188945731622 |
| 9 | ekle | TEFAS fon sınıfı akış rejimi: PPF çıkışı + HSF/SER girişi, 5G ve 20G aynı yön = risk-on; serbest fon borsaya giriş sayılmaz | 2099556801611977021, 2097018434563473539, 2094913511986020386, 2099967840405086603, 2099565529698545872, 2096644397110534476 |
| 10 | çeşitlendir | R214: Vegas tüneli EMA13 > EMA144 > EMA169; günlükte para girişi şartı | 1845923939736080720, 1839308965039190302, 1846640825771377067, 1846638825864413237, 1838670037353374138 |

### Öncelik 11–15
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 11 | genişlet | R196/R230: EMA5/10 > EMA20 kesişi + MACD > sinyal + RSI14 50 geçişi + 5 gün OBV > 0 | 1847008515014922537, 1851719680052072481 |
| 12 | ekle | Yatay piyasa filtresi: ADX < 20 VE BBW son 100 barın en düşük %20'si → işlem açma | 2004287128214356186 |
| 13 | genişlet | R120: momentum = Π(1 + aylık getiri) − 1, temettü dahil; Apple 2014 %40,62 | 1946925694652674087 |
| 14 | genişlet | R183: hisse bazlı ay etkisi t testi p < 0.05; XU100 Şubat çalışılmış örneği | 2009899784748794098, 2018404523635515480 |
| 15 | genişlet | R028/R029: VRP kesişim çıktı sütunları ve INTC/MU örneği; yön iddiasını belirsiz diye işaretle | 2090161750444327119 |

### Öncelik 16–20
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 16 | genişlet | R202/R200: kayan pencere 20/60 gün; yüksek kayan alpha + yüksek kayan Sharpe + düşük beta; faz + sinyal tepkisi + beta/alpha kapısı | 1953112693407203768, 1878050003647697038, 1878050007133106656, 1878132805504254308 |
| 17 | genişlet | R137: ML ayağı — regresyon kırılımı 60 gün, momentum penceresi 16 gün, olasılık > 0.50 | 1890128183972008095, 1965629890100941012, 1920446141105103040 |
| 18 | çeşitlendir | R128/R131: Golden Cross EMA50/EMA200, hisse ve endeks rejimi | 1844838137366806837, 1844070126406250885, 1847537834397237420 |
| 19 | genişlet | R097: GARCH risk başına getiri = ortalama getiri / ortalama GARCH volatilitesi; yüksek volatilitede yüksek Sharpe + düşük beta | 1940666220354654588, 1952471946383265824 |
| 20 | genişlet | R110: Sharpe formülü, risksiz faiz %30 örneği, 6 ay/yıllık getiri | 1940482825427235036 |

### Öncelik 21–25
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 21 | ekle | GSYİH art arda ≥2 çeyrek yavaşlama → altın (13 dönemin 9'u pozitif) | 2083875779218198689, 2083875781457928398, 2083875783332741531 |
| 22 | genişlet | R176: eğim × R² çalışılmış örneği (ALARK 1.3617), pencere 250 gün olası | 2018765685091139701 |
| 23 | genişlet | R178/R002: convex hull → cross-sectional momentum → Markowitz/BL sırası; ilk 10 sektör korelasyon, faz alanı ilk 10 hisse | 1949014576458023063, 1947024537079468538, 1951627374774087770, 1951634776156258423, 1955360082641948922 |
| 24 | çeşitlendir | R148: Supertrend/MOST/KAMA trend kapısı + RSI14 > 50 (parametre eksik) | 1841917340419559794, 1853065056759550021, 1838663920996831643, 1843373717247922211, 1844830887294197939, 1844832419821539723 |
| 25 | ekle | Takas dağılımı okuması (kalıcı fon/yabancı kurum = sağlıklı; ani yabancı artış ve kısa satış = spekülatif) | 1939414080336670931, 1983492569574056243 |

### Öncelik 26–30
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 26 | genişlet | R166: üçlü sinyal = 60 günlük direnç kırılımı + hacim + temel + takas | 1935015198277951650 |
| 27 | ekle | Fon yatırımcı sayısı filtresi (evren-likidite) | 1979695659432427919, 1979721101304361294, 1979721927809012208 |
| 28 | ekle | Manipülasyon işaretleriyle evren dışlama | 1945020445117264368 |
| 29 | çeşitlendir | R032: fon getiri sıralaması + risk ölçüleri + veri uyarısı | 2096655622938693877, 2097381679560102246, 2096661898385113202, 2099564220601835538, 2099569262847230211 |
| 30 | genişlet | R255: WaveTrend WT(10,21), −50/−60 bandı, tek başına yetmez | 1845369437441933344, 1848426907441692797 |

### Öncelik 31–35
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 31 | çeşitlendir | R105: RoC(9) sıfır ekseni yukarı kesişi | 1840816385540440325, 1840826561273979333 |
| 32 | genişlet | R212/R131: EMA200 yukarı kesiş tetiği; endeks EMA200 altı olumsuz | 1844068170853949930, 1827078541797945391 |
| 33 | ekle | Thompson Sampling ile günlük hisse önerisi | 1940670472590372957 |
| 34 | ekle | Ichimoku bulut taraması (periyot eksik) | 1847998614548721928 |
| 35 | çeşitlendir | R183: haftanın günü etkisi | 1891539591531823394, 1891948299474616579 |

### Öncelik 36–40
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 36 | genişlet | R225: derinlik alış/satış oranı yüksek + fiyat henüz tepkisiz | 1983491105631993940 |
| 37 | genişlet | R214/R167/R116: uyumsuzluk + marubozu + breakout + EMA 5>8>13>34 birleşik tarama | 1915163157531910187 |
| 38 | ekle | Kısa vadeli momentum dönüşü (1 hafta/1 ay) | 1946948449275928807 |
| 39 | ekle | Vasicek faiz patikası (r0 0.50, θ 0.30) ile iskonto ve sektör konumu | 1925776822249144708 |
| 40 | ekle | Japonya likidite sıkışması → Altın/Gümüş rasyosu | 1992188666593112507 |

### Öncelik 41–45
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 41 | çeşitlendir | R071: negatif reel faiz → altın | 2083953538661539956 |
| 42 | çeşitlendir | R179/R145: ANP | 1944868638307311952 |
| 43 | çeşitlendir | R116: MACD pozitif uyumsuzluk, BIST30 | 1837867391310540998 |
| 44 | çeşitlendir | R077/R034: kelebek etkisi ilk ipuçları; R105/R124: momentum breakout | 1914692264384774310, 1862055089713602762 |
| 45 | ekle | Çok gaplı seans ertesi açılışı bekle | 1866237714728645031 |

### Öncelik 46
| # | Etiket | Öneri | Kaynak id |
|---|---|---|---|
| 46 | genişlet | R022: momentum lookback örnekleri 5/10/20 gün | 1993444658085826808 |

Çelişki satırları (1898475888250916913, 1898475890918514837, 1898475893422690610, 1912487017788698997, 1913224177407926759, 1892656632976318511, 1907899832108274069, 2092745592661246196, 1938905375119434125) öneri listesine alınmadı. Bunlar için önce 3. bölümdeki karar gerekir.
