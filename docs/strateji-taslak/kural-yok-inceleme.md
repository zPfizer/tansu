# "Kural yok" satırlarının incelemesi (izlenebilirlik.md, kilit: Tansu kural/formül vermedi)

Kapsam: izlenebilirlik.md içinde bu kilidi taşıyan 74 satır. Dosyada 76 geçiş var; 2'si açıklama satırıdır (sütun başlığı ve özet tablosu). Sayılan satır: 74.

## Yöntem ve sınırlar

- Sıra: H1 (gizli), H2 (görselde), H3 (başka kayıtta), H4 (standart tanım), H5 (eksik). Her satıra tek ana sonuç yazıldı. Kısmi bulgu "not" alanındadır.
- Görseller beyin notlarındaki assets yolundan Read ile açıldı. Açılan görsel: R008 G7/G8, R049, R076, R077, R094, R108, R114, R116 G1/G2, R117, R119, R124, R125 G1/G2, R126, R128, R129, R133, R136, R138, R156, R168, R187, R192, R193, R203, R216, R219, R221, R234 (görsel hamda var, beyinde yok; DOAS görseli beyin notu eşleşmesiyle açıldı), R235. Küçük yazı "okunamadı" diye işaretlendi.
- R233, R235, R236, R237, R243 için ham metin tam okundu. R233'ün kendi görseli yok.
- H3 taraması: defter-1..4.md ve ham-yapistirmalar*.md içinde anahtar kelime ve eş anlamlı Grep.
- H4 kaynakları: bu oturumda web araması ile doğrulananlar "web" diye işaretli (APO/Donadio, Hikkake, Weinstein 30 hafta, gizli uyumsuzluk, bayrak/flama/takoz/OBO ölçü kuralı). Diğer standartlar (Bollinger 20/2, VaR, mark-to-market, HBK, IV beklenen hareket) bilinen tanımdır; bu oturumda açılmadı. Kaynak adı verildi.
- Hesaplar bu dosyada yapıldı ve etiketlendi ("hesap").
- Not: "H4" Tansu'nun bir tarayıcı eşiğini vermez. H4 yalnız göstergenin tanımını çözer.

---

## Satır satır inceleme

### 1. R004 · formasyon · "Takoz TOBO OBO" ve "Bir de bayrak flama olur"
- Sonuç: H4.
- Kanıt: ham R004: "Uygulamanın ilk algoritmaları; ... Takoz TOBO OBO İlk bunlar olacak Bir de bayrak flama olur". Yalnız isim listesi var. Sapma gösteren cümle yok.
- Standart (web): bayrak/flama 5-15 bar sıkışma, ölçü hedefi direk boyu; takoz iki yakınsayan eğimli çizgi; OBO hedefi baş-boyun mesafesi (tradingsim.com ve kotakneo.com sayfaları). OBO kuralı ayrıca R219'da yazılı (H2).
- Not: tarayıcı eşikleri (pivot, bar sayısı, tolerans) yine Tansu'dan gelmez. Standart pivot kuralı seçilir.

### 2. R006 · formasyon · "Takoz olur"
- Sonuç: H4.
- Kanıt: ham R006 "Takoz olur, Opsiyon fiyatları ile ABD borsasında ...". Başka cümle yok.
- Standart: yükselen takoz (aşağı kırılım eğilimi), düşen takoz (yukarı kırılım eğilimi) (web, tradingsim.com).

### 3. R007 · formasyon · "Bir de bayrak flama olur"
- Sonuç: H4.
- Kanıt: ham R007 tek cümle: "Bir de bayrak flama olur".
- Standart: bayrak paralel çizgi, flama hafif yakınsayan çizgi; ikisi de devam formasyonu (web, kotakneo.com).

### 4. R008 · formasyon · yatay sıkışma, üçgen/flama daralma, "Kırılım" etiketi
- Sonuç: H5.
- Kanıt (görselden, G8): yükselen kırmızı alt çizgi kırılmış; sağda iki kırmızı etiket var; metinleri "Sinyal (Sonrası)" ve "Kırılım (Sonrası)" gibi görünür, okunamadı. G7: turuncu yükselen çizgi ve yatay mavi bölge; etiketler okunamadı.
- Eksik: sıkışmanın tanımı (daralma oranı, bar sayısı) ve kırılımın tanımı (kapanış mı, tolerans mı).
- Yorum seçenekleri: (a) üçgen için standart: iki üst, iki alt temas, yakınsayan çizgiler. (b) araçtaki bölge kırılımı mantığı (R008 G4: "Kırılım ... (Temas:4)"). Tansu'nun örneklerine en yakın: (b), çünkü etiket aynı araçtan geliyor. Kesin değil.

### 5. R021 · felsefe · "ML ile trade hiç sevmem ama ara ara bakarım"
- Sonuç: H5 (kural değil, tutum).
- Kanıt: ham R021 aynı cümle. Aynı kayıtta "13 trade gününde 9 isabetli": görselden konsol "Hit Rate: 69.23%", model türü ve hit tanımı yok.
- Eksik: yok; cümle bir kural taşımaz. Tasarıma girmez.

### 6. R049 · temel-değerleme · "Ekranda mavi çizgi xxxx kırmızı ise fiyat bir altta iken diğeri kesin üste"
- Sonuç: H1.
- Kanıt: ham R049: "Ekranda mavi çizgi  xxxx kırmızı ise fiyat bir altta iken diğeri kesin üste diğeri üste iken öteki kesin altta:)". Tansu metriği "xxxx" ile gizliyor.
- Görselden: başlık, legend ve ticker yok. Sol eksen "Oran (%)" 0-80, sağ eksen 0-800+. Mavi seri 2020/03 yaklaşık %78, 2023/09 yaklaşık %10, 2024/06 yaklaşık %6. Kırmızı seri 2023/09 yaklaşık 690, 2024/03-06 yaklaşık 770-780. Ters faz çoğu çeyrekte görünür. Mavi serinin adı okunamadı.

### 7. R053 · giriş · "Bollinger Bantlarında alt ve üst bantlar genelde +-2 standart sapmayı temsil eder ..."
- Sonuç: H4.
- Kanıt: ham R053 aynı cümle ("%95'inin bu sınırlar içinde kalması beklenir").
- Standart: Bollinger Bantları = orta bant (varsayılan 20 periyot SMA) ± 2 standart sapma (John Bollinger; bu oturumda açılmadı). Tansu "+-2 standart sapma" yazıyor; uyuyor.
- Not: görsel kitap şekli ve "SE" (standart hata) kullanıyor; tweet metni "SD". Karışıklık var. Pencere ve ortalama türü yazılmamış; varsayılan alınır.

### 8. R053 · giriş · "-2SE veya -3SE seviyesine inmesi ... tepki alımı fırsatı"
- Sonuç: H5.
- Kanıt: ham R053: "Fiyatın -2SE veya -3SE seviyesine inmesi istatistiksel olarak nadir bir durumdur. Bu seviyeler, ... tepki alımı fırsatı olarak değerlendirilebilir."
- Eksik: tetik (bantın altında kapanış mı, bandın içine dönüş mü), -2 mi -3 mü, çıkış (orta bant mı), stop.
- Yorum seçenekleri: (a) kapanış alt bandın altında, ertesi gün bandın içine dönüşte al. (b) dokunuşta al. (c) -3 yalnız ikinci kademe. Tansu'nun tek yakın örneği R187 (IV-SD bantları): "-1SD ... alım fırsatı, stop -2SD altı". En yakın (a)+R187 stop mantığı. Kesin değil.

### 9. R053 · boyut-risk · "Bantların genişliği hissenin ne kadar riskli ve oynak olduğunu ortaya koyar."
- Sonuç: H4.
- Standart: Bollinger BandWidth = (üst − alt) / orta bant (John Bollinger). Cümle bir ölçü tanımıdır; eşik yok.

### 10. R053 · boyut-risk · "maksimum kaybı hesaplamaya yarar ... (VaR)"
- Sonuç: H4.
- Kanıt: ham R053: "Portföyün belirli bir güven düzeyinde (örneğin %95) uğrayabileceği maksimum kaybı hesaplamaya yarar."
- Standart: Value at Risk = belirli güven düzeyi ve ufuk için kayıp eşiği (tarihsel, parametrik, Monte Carlo). Tansu güven düzeyi %95 verdi. Ufuk ve yöntem yok.

### 11. R058 · felsefe · "Ml modelleri sıkıntılıdır"
- Sonuç: H5 (kural değil, tutum).
- Kanıt: ham R058. Aynı kayıtta "olması gereken piyasa değeri tahmin edilir; sapma optimize edilir" cümlesi ayrı satırdır.

### 12. R076 · teyit-tetik · "eh bunu yolculamayalım mı şimdi..." (yön çatışması)
- Sonuç: H5.
- Kanıt (görselden): "D (CD=1.0AB)" etiketi düşen kırmızı direnç çizgisinde; D'den sonra yukarı mumlar. Metin: "Düşeni kırmış, sell yönlü abcd'yi tamamlamışi beyaz kuğu da oluşmuş".
- Eksik: çakışma çözümü. Sell yönlü AB=CD ile yukarı kırılım aynı anda olursa ne yapılır.
- Yorum seçenekleri: (a) çakışmada işlem yok. (b) kırılım önceliği. (c) long-only sistemde sell yönlü yapı yalnız çıkış uyarısı. Tansu cümlesi espri; hiçbiri doğrulanmaz.

### 13. R077 · rejim · yeşil üçgenler (nisan 2025 oynaklık sıçraması sonrası alım)
- Sonuç: H5.
- Kanıt (görselden): başlık "Volatilite Rejimi: Mevcut (v_t) vs Ortalama (Theta)"; mor v_t, turuncu kesikli Theta, gri bant. Mart-Nisan 2025'te v_t yaklaşık 4,3'e sıçrıyor; yeşil üçgenler bu sıçrama dönemine denk geliyor. Kırmızı üçgenler 2024 başı ve 2025 başı gibi düşük v_t dönemlerinde. Bant genişliği ve v_t formülü okunamadı.
- Eksik: v_t tanımı, theta penceresi, bant genişliği (k·σ), üçgenin tetik koşulu.
- Yorum seçenekleri: (a) yeşil = v_t gri bandın üstüne çıkıp geri döndüğünde. (b) yeşil = bandın üstünde olduğu sürece. Görsele en yakın: (a)/(b) belirsiz; "okunamadı".

### 14. R090 · hedef-çıkış · "hedefi dinamik olarak kalibre ediyor ... otonom kâr alabiliyor"
- Sonuç: H5 (Tansu'nun cümlesi değil).
- Kanıt: defter denetimi: metin başka bir hesabın Tansu'ya cevabı (M/A). Cümle "dünkü referans ile bugünkü açılış arasındaki korelasyonu (Varyans/K-Means) saniyede bir tarayıp".
- Eksik: yöntem. Saniyelik tarama gün içi veri ister (veri kilidi).
- Not: Tansu'nun kendi sözü "artık strateji vs yazmıyorum" (R090). Tasarıma girmez.

### 15. R094 · rejim · BIST100 / BIST_VOL "gülümseme"
- Sonuç: H5 (kural değil, gözlem).
- Kanıt (görselden): saçılım grafiği "BIST 100 ve BIST Volatilite Log Getirileri"; x −0,20..0,18; y −0,4..0,7; V biçimli bulut. Metin: "Piyasa yapıcının bize bir mesajı var:) KY sizi seviyorum diyor".
- Eksik: BIST_VOL tanımı (hangi seri) ve bir karar kuralı. Eşik yok.

### 16. R099 · ölçüm-ilkesi · "Mark-to-Market"
- Sonuç: H4.
- Kanıt: ham R099 "Mark-to-Market" açık pozisyonu güncel değerle raporlama. Görselde net kâr 13.436,14 TL, işlem günlük dökümü.
- Standart: açık pozisyon her gün kapanış fiyatıyla değerlenir. Kapanış değeriyle rapor zaten tasarımda var (izlenebilirlik notu). Sapma yok.

### 17. R105 · giriş · "Kesişim gerçekleştiğinde fiyat genellikle %5-%10 primlenmiş olur."
- Sonuç: H5 (kural değil, ampirik iddia).
- Kanıt: ham R105 (yazar M). Kanıt, örnek, pencere yok.
- Eksik: hangi ortalama çifti. Ölçülmeden kural olmaz. Seçenek: test edilecek hipotez olarak ölçüm koluna koy; kural olarak alma.

### 18. R108 · rejim · Weinstein 4 evre ("X haftalık eğri")
- Sonuç: H4.
- Kanıt: ham R108 "Fiyatın X haftalık eğriyi ve hacmi arkasına alarak ...". Görselde (A1CAP) sarı uzun ortalama var; periyot yazılı değil ("okunamadı").
- Standart (web): Weinstein evre analizi 30 haftalık hareketli ortalama etrafındadır. Evre 1 yatay taban, evre 2 fiyat artan ortalamanın üstünde, evre 3 tepe, evre 4 fiyat düşen ortalamanın altında. Kaynak: Stan Weinstein, "Secrets for Profiting in Bull and Bear Markets" (1988); sayfalar: trendsandbreakouts.com, deepvue.com.
- Not: Tansu'nun "X" değeri belli değil. 30 hafta standarttır.

### 19. R110 · boyut-risk · "4. Sistemin üzerine inşaa edilecek hissenin oranı %50 den fazla olmalıdır."
- Sonuç: H5.
- Kanıt: ham R110 aynı cümle, "Hisse Sayısı" maddesinin altında. Başka kayıtta aynı cümle yok. R112 örneğinde XU100 %50 / TEKTU %30 / EREGL %20.
- Eksik: "oran" neyin oranı.
- Yorum seçenekleri: (a) tek hissenin ağırlığı en fazla %50 olmalı (3-10 hisse ile uyumlu). (b) çekirdek (Markowitz) hisselerinin toplamı portföyün %50'sinden fazla. (c) hissenin oranı = hisse payı/endeks payı (R112'deki XU100 %50 örneği). Tansu'nun elindeki tek sayısal örnek R112; ona en yakın: (b). Kesin değil.

### 20. R114 · formasyon · "Fincan Oluşumu (Mavi Çizgi) ... Fibo 100% ... 317.00 (Fibo 0%)"
- Sonuç: H5 (kısmi H2).
- Kanıt (görselden): lejant "FİNCAN", "KULP", "Fibo Bitiş: 317.00", "Fibo Başlangıç: 212.20". Fib çizgileri: 0% 317.00; 23.6% 292.27; 38.2% 276.97; 50% 264.60; 61.8% 252.23; 78.6% 234.63; 100% 212.20. Hesap: 317 − r × 104,80 bu değerleri verir (292,27; 276,97; 264,60; 252,23; 234,63 doğru).
- Bulunan kural: Fib ölçeği dipten (100%) sağ ağza (0%) çizilir; seviyeler tepeden aşağı ölçülür.
- Eksik: fincanın bulunması (dip ve ağız pivotu seçimi, minimum süre, yuvarlaklık).
- Yorum seçenekleri: (a) sol ağız = dipten önceki en yüksek pivot (300,75; görseldeki mavi çizginin başlangıcı), sağ ağız = dipten sonraki ilk pivot tepe. (b) sağ ağız = en yüksek kapanış. Tansu'nun örneğine uyan: (a).

### 21. R114 · formasyon · "Kulp ... Fibonacci 61.8% (252.23) ve 50% (264.60) bölgesi"
- Sonuç: H5.
- Kanıt: metin kulpun 50%-61,8% bölgesine kadar indiğini söyler. Görselde turuncu kulp tabanı yaklaşık 242-245 görünür (yaklaşık okuma). Bu 61,8% çizgisinin (252,23) altında, 78,6% çizgisinin (234,63) üstünde. Metinle uyuşmaz görünür.
- Eksik: kulbun kabul aralığı (en fazla geri çekilme), kulp süresi.
- Yorum seçenekleri: (a) en fazla %61,8. (b) en fazla %78,6 (görselin gösterdiği). Görsele yakın: (b). Okuma kesin değil.

### 22. R114 · teyit-tetik · "300.75 seviyesindeki yeşil kesik çizgiyi (KIRILMA) yukarı kesiyor"
- Sonuç: H2.
- Kanıt (görselden): yeşil kesikli çizgi "KIRILMA 300.75"; "SİNYAL! 2025-10-24" oku. Mavi fincan çizgisinin başlangıcı aynı seviyede görünür (yaklaşık 300). Hedef hesabı bunu doğrular (satır 23).
- Bulunan kural: kırılma seviyesi = fincanın sol ağız yüksekliği (300,75). Sinyal: fiyat bu çizgiyi yukarı keser.
- Okunamadı: kesişim kapanışla mı, gün içi mi.

### 23. R114 · hedef-çıkış · "Fincan derinliği kadar yukarı gitme" (389.30)
- Sonuç: H2.
- Kanıt (görselden): mor çizgi "HEDEF: 389.30". Hesap: derinlik = sol ağız − dip = 300,75 − 212,20 = 88,55. Hedef = kırılma + derinlik = 300,75 + 88,55 = 389,30 (tam eşleşir).
- Bulunan kural: hedef = KIRILMA + (KIRILMA − dip). İzlenebilirlik notundaki çelişki (389,30 − 104,80 = 284,50) yanlış derinlik tabanından geliyor: 104,80 = 317 − 212,20, sağ ağız farkıdır.

### 24. R114 · boyut-risk · "1:2.27 Risk/Reward"
- Sonuç: H5.
- Kanıt (görselden): başlıkta "Risk/Reward: 1:2.27". Giriş ve stop çizgisi okunamadı.
- Hesap: giriş = 300,75 ise ödül 88,55; risk 39,01; stop 261,74. Bu seviye hiçbir Fib çizgisi ile eşleşmez (50% = 264,60; 61,8% = 252,23). Giriş 50% stop ile 2,45; 61,8% stop ile 1,83 verir.
- Eksik: giriş fiyatı (kırılma çizgisi mi, sinyal günü kapanışı mı) ve stop (hangi çizgi).
- Yorum seçenekleri: (a) giriş sinyal günü kapanışı, stop kulp dibi. (b) giriş kırılma çizgisi, stop Fib 50%. Hiçbiri 2,27'yi vermez. Sonuç: doğrulanamadı.

### 25. R116 · teyit-tetik · gizli pozitif uyumsuzluk ("diplerin yükseldiğini ... aşağı kaydığını")
- Sonuç: H2.
- Kanıt (görselden, G1 üst etiket): "Swing=15 sol-only | MinGap=15" (başı kesik). Fiyat panelinde mavi çizgi iki dibi bağlar (yüksek dip); alt panelde kırmızı kesikli çizgi iki dibi bağlar (alçak dip), sağ değer yaklaşık 0,21.
- Bulunan kural: fiyat pivot dipleri (Swing=15, yalnız sol pencere) arasında MinGap=15 bar; ikinci fiyat dibi yüksek, ikinci gösterge dibi alçak.
- Okunamadı: gösterge kimliği ve "sol-only" tam anlamı.

### 26. R116 · rejim · "Teknik olarak biz buna trend devam sinyali diyoruz."
- Sonuç: H4.
- Standart (web): fiyat daha yüksek dip, osilatör daha alçak dip yaparsa gizli (hidden) pozitif uyumsuzluk; trend devamı sinyalidir (luxalgo.com, schwab.com, coingecko.com sayfaları). Tansu'nun kullanımı bununla aynı.

### 27. R117 · teyit-tetik · "Gizli uyumsuzlukları takip ediniz, arkadaşça hatırlatma."
- Sonuç: H3.
- Kanıt: aynı kavramın parametresi R116 görselinde: "Swing=15 sol-only | MinGap=15" (satır 25). R117 görselinde (görselden): yeşil üçgenler fiyat yüksek dibinde, alt panelde kırmızı çizgi alçalan dipleri bağlar, sarı noktalar. R117 görselinde parametre yazısı yok.
- Bulunan kural: satır 25'teki kural.

### 28. R118 · rejim · "Düşük Hacim uyarısı"
- Sonuç: H5.
- Kanıt: ham R118 "genel hacim analizindeki Düşük Hacim uyarısı hala masada" (yazar M). Eşik yok.
- Eksik: "düşük" neye göre.
- Yorum seçenekleri: (a) son 20 günlük ortalama hacmin altı. (b) hacim dağılımının alt %25'i. Tansu'nun elindeki en yakın kural R232 (20/60 gün ortalama, alt %25 at; 10 milyon TL sabit eşik). En yakın: (a)/(b), ama R232 evren filtresi içindir.

### 29. R118 · giriş · "Liderleri Takip Edin: XU100 spread'i düşük ve stabil olduğu için ..."
- Sonuç: H5.
- Kanıt: ham R118 aynı cümle. Aynı kavram R119'da: Corwin-Schultz spread, görselden "21g rolling"; FROTO ortalama %1,7990, medyan %0,7841, maks %9,8494; metin: "spread'in tekrar ortalamaya (%1.79) dönmesini beklemek gerekir". XU100 ortalama spread %1,06 (R118).
- Eksik: "düşük ve stabil" eşiği; "ağırlığı yüksek hisse" tanımı.
- Yorum seçenekleri: (a) spread ortalamanın altında. (b) spread medyanın altında. Tansu'nun cümlesine yakın: (a).

### 30. R118 · rejim · "Mikro-Makro Çelişkisi ..."
- Sonuç: H5 (kural değil, yorum).
- Kanıt: ham R118. Dar spread + düşük hacim = "para seçici". Eşik ve eylem yok.

### 31. R119 · giriş · "Hacim (Volume) ile korele edip ... 'mal boşaltma' mı yoksa 'toplama' mı"
- Sonuç: H5.
- Kanıt: ham R119 "kodunu da yazabiliriz kolayca". Yapılmış kod ya da çıktı yok. Başka kayıtta tanım yok (Grep: "mal boşaltma").
- Eksik: korelasyon yöntemi, pencere, eşik, işaret.
- Yorum seçenekleri: spread ile hacim korelasyonu 21 günlük (görseldeki pencere); pozitif ve yüksek = boşaltma, negatif = toplama. Tansu'nun örneği yok; yalnız fikir.

### 32. R121 · momentum-seçim · "kodum optimal momentum+ portföyü için simülasyon yapıyor"
- Sonuç: H5.
- Kanıt: ham R121 tek cümle. R181: "161.700 kombinasyon ... optimal 3 hisselik portföy"; hesap: 100 × 99 × 98 / 6 = 161.700, yani 100 hisseden 3'lü kombinasyon. Amaç fonksiyonu yazılı değil (R137'de "Maksimum Sharpe").
- Eksik: "+" ne demek, amaç fonksiyonu.
- Yorum seçenekleri: (a) 100 momentum hissesinden en yüksek Sharpe'lı 3'lü. (b) R120'deki 12 aylık decile en üst grup. En yakın: (a).

### 33. R124 · teyit-tetik · "En sağdaki uzun yeşil mum ... o günü en yüksek seviyeye yakın kapattığını"
- Sonuç: H5.
- Kanıt: ham R124 aynı cümle. Görselde (görselden) son mum uzun yeşil, üst fitil çok kısa. Sayı yok. Aynı kavram R(ham satır 3221): "gövdesi uzun yeşil mum" nitel.
- Eksik: "uzun" ve "yakın" eşiği.
- Yorum seçenekleri: (a) gövde ≥ 1 × ATR(14) ve (Yüksek − Kapanış) / (Yüksek − Düşük) ≤ 0,2. (b) gövde ≥ son 20 mum gövde ortalamasının 1,5 katı. Tansu'dan örnek sayı yok. Standart bir "yüksek yakın kapanış" göstergesi var (Chaikin Close Location Value), ama Tansu bunu anmıyor.

### 34. R125 · teyit-tetik · "Pre signal ok ile işaretlenen mum matrix ekranında"
- Sonuç: H1.
- Kanıt: ham R125: "Bir günde %5 Ema sıkışması parametrelerin detaylarını verip stratejimi anlatamam ama öz fikri zaten verdim."
- Görselden: ICBCT, "Son Kapanış: 14.55", EMA30/50/100/200 lejantı, mavi kutu "AKTİF 2g", ok "Pre signal". Pre-signal koşulu yazılı değil. Başka araç çıktısı (R127, KRDMD) "EMA Sıkışması | Tolerans %1.2 | Min 3 gün" gösteriyor ama EMA seti farklı (20/50/100/200); aynı eşik olduğu varsayılmaz.

### 35. R126 · bölge · "düşüşün 0.786 düzeltme seviyesine (yaklaşık ₺31.00)"
- Sonuç: H4.
- Standart: Fibonacci geri çekilme oranı 0,786 (= √0,618). Seviye = dip + 0,786 × (tepe − dip). Aracın ölçeği R114 ile uyumlu (satır 20).
- Okunamadı: HH ve HL fiyatları; 31,00 doğrulanamadı. Direnç olarak kullanım kuralı yok.

### 36. R128 · rejim · "EMAs'lar artık birer direnç değil, güçlü birer dinamik destek haline gelmiştir."
- Sonuç: H5.
- Kanıt: ham R128 (yazar M). Görselden: EMA 50 (13310.99), EMA 100 (12840.90), EMA 200 (12256.37); kırmızı kutu sıkışma bölgesinde.
- Eksik: "dinamik destek"in tetiği (hangi EMA'ya geri çekilme, tolerans, teyit). Boğa dizilimi (50>100>200) ayrı satırda.
- Yorum seçenekleri: (a) dizilim sonrası EMA50'ye değince al. (b) yalnız rejim etiketi (kural yok). Tansu örneği yok.

### 37. R128 · hedef-çıkış · "fiyat ortalamalardan çok uzaklaştığında bir soğuma, yatay seyir veya ... re-test"
- Sonuç: H5.
- Kanıt: ham R128: "14.587 seviyesine ... EMA 50'den (13.310) oldukça uzaklaştığını". Hesap (görselden son kapanış 14587,90): EMA50'ye +%9,59; EMA100'e +%13,61; EMA200'e +%19,02.
- Eksik: "çok uzak" eşiği.
- Yorum seçenekleri: (a) EMA50'den ≥ %9,6 (Tansu örneği). (b) ATR katı. (c) yalnız bilgi. Tansu'nun tek örneği (a).

### 38. R129 · bölge · "FVG'ler bazen ... likiditeyi temizlemek istediği yerler"
- Sonuç: H5.
- Kanıt: ham R129 (gövde M); Tansu: "bana pek bakmayın". FVG tanımı başka kayıtta var (R199: 1. mumun en yükseği ile 3. mumun en düşüğü arası boşluk, doldurulmamış). Süpürme (sarkma) tanımı yok.
- Eksik: sarkma derinliği, süre, kapanış mı fitil mi.
- Yorum seçenekleri: (a) FVG alt sınırını fitille delip kapanışla içeri dönme. (b) kapanışla altında kalma = geçersiz. R199: "Yeşil kutunun altına sarkar ve kapanış yaparsa iptal" (R192 benzeri). En yakın: (b).

### 39. R129 · bölge · "Fiyat önce yukarıdaki dirençleri test edip likidite topladıktan sonra bu açık hesabı kapatmak isteyecektir."
- Sonuç: H5 (kural değil, senaryo).
- Kanıt: ham R129 aynı cümle. Sıra, eşik ve işlem yok.

### 40. R133 · temel-değerleme · "O yüzden HBK evrensel bir cevap sunar."
- Sonuç: H4.
- Kanıt: ham R133 (T giriş + M gövde). Görselden: "Fiyat & Yıllıklandırılmış HBK"; HBK yaklaşık 6,3 (2023), 9,4 (2024 ortası), 1 (2025 ortası), 3,6 (Ocak 2026).
- Standart: HBK = hisse başına kâr (EPS) = net dönem kârı / hisse sayısı. "Yıllıklandırılmış" = son 4 çeyrek toplamı. Mutlak EPS şirketler arası kıyas için yetmez (hisse sayısına bağlı); "evrensel" iddiası tanım değil, yorum. Karar kuralı yok.

### 41. R136 · teyit-tetik · özel subplot ile gizli pozitif uyumsuzluk
- Sonuç: H1.
- Kanıt: ham R136: "benim grafiğimdeki subplot pek bilinen birşey değil ama uyumsuzluk sinyalleri gayet iyi". Görselden: alt panelin başlık ve gösterge adı beyaz boyayla silinmiş; üst panelde MA20, MA50, "Bullish Divergence" (pembe kare), "DIV" etiketleri, sarı elmaslar.
- Not: uyumsuzluk kavramı H4 (satır 26). Gösterge kimliği Tansu'ya özel ve gizli.

### 42. R137 · momentum-seçim · "yapay sinir ağları ile oluşturduğum bir momentum stratejim var"
- Sonuç: H1.
- Kanıt: ham R137: "Bu sistem satılık değil arkadaşlar önce onu belirteyim. Sistem nasıl işliyor stratejiyi anlatmadan biraz işleyişi anlatayım". Çıktısı "pozitif eğimli ... bir excel". Model yapısı, girdi, eşik yok.

### 43. R138 · boyut-risk · "piyasa kan ağlarken sizi nakitte tutarak ... kalkan"
- Sonuç: H3.
- Kanıt: ham R138: "sadece belirgin trendleri (AD > EMA) toplamanın hikayesidir". R139: "Enter long: AD() Ref(Mov(AD(),opt1,E), 1) ... OPT1 Current value: 3". Görselden: kümülatif getiri yeşil çizgi düşüş döneminde yatay (nakit).
- Bulunan kural: A/D EMA'nın üstündeyse pozisyonda, altındaysa nakitte (satır 45). Nakit davranışı bu kuralın sonucudur.

### 44. R138 · ölçüm-ilkesi · "EMA değeri walk forward le optimzie edilerek model oluşturulmuştur."
- Sonuç: H5.
- Kanıt: ham R138 aynı cümle. R139: "OPT1 Current value: 3" (bir tarihteki optimum).
- Eksik: eğitim/test pencere uzunlukları, aday EMA aralığı, amaç fonksiyonu (Sharpe mı getiri mi), yeniden eğitim sıklığı.
- Yorum seçenekleri: (a) amaç Sharpe (görselde Sharpe 0,67 gösteriliyor). (b) amaç toplam getiri. En yakın: (a). Pencere için Tansu'dan sayı yok.

### 45. R139 · giriş · "Enter long: AD() Ref(Mov(AD(),opt1,E), 1) ... OPT1 Current value: 3"
- Sonuç: H3.
- Kanıt: operatörler metinde silinmiş. R138 operatörü verir: "(AD > EMA)". Görselden panel adı "Accumulation/Distribution | EMA Crossover".
- Bulunan kural: AD > Ref(EMA(AD, opt1), 1), opt1 = 3. Çıkış, tersinin olduğu varsayımıdır; yazılı değil. Short satırları grafikte yok (nakitte kalıyor); short kuralı okunamadı.

### 46. R139 · diğer · "Çatır çutur girip çıkmak için, 1-2 gün"
- Sonuç: H5.
- Kanıt: cümle "OPT1 Current value: 3" satırından hemen sonra geliyor.
- Eksik: "1-2 gün" ne.
- Yorum seçenekleri: (a) hızlı giriş çıkış için opt1 = 1-2. (b) elde tutma süresi 1-2 gün. En yakın: (a), çünkü cümle opt1 değerinin hemen ardından.

### 47. R156 · giriş · "Mean reversion, absolute pricing oscilator kullanılarak oluşturulan bir strateji."
- Sonuç: H2.
- Kanıt (görselden): lejant "ClosePrice", "Fast10DayEMA", "Slow40DayEMA", "buy" (kırmızı yukarı üçgen), "sell" (yeşil aşağı üçgen); fiyat 500-1100, 2014-2018.
- Standart (web): Donadio-Ghosh, "Learn Algorithmic Trading", APO ortalama dönüş: hızlı EMA 10, yavaş EMA 40; APO < −10 al, APO > +10 sat; yeni işlem son işlem fiyatından farklı; APO işaret değiştirince pozisyon kapanır (oreilly.com kitap sayfası). Görsel bu kitabın örnek grafiğiyle aynı etiketleri taşıyor.
- Bulunan kural: APO = EMA10 − EMA40; ±10 eşik kitaptandır, Tansu'nun görselinde yazılı değil. Tansu: "grafiği düzenlemedim bile". BIST için ±10 birim uygun değil; eşik fiyat ölçeğine bağlıdır.

### 48. R168 · teyit-tetik · Hacim, MACD, ADX, RSI panelleri; "Temas" işareti
- Sonuç: H5.
- Kanıt (görselden): lejant EMA 5, EMA 13, Trend Destek, Temas (turuncu üçgen), En Yakın Demand, En Yakın FVG, BOS. Paneller: Hacim, MACD+Signal, ADX, RSI (renkli üst ve alt bantlar). Periyotlar yazılı değil. "Temas" sayısı başka araç çıktısında var (R073-R087: "Temas: 3 | Lookback: 20"); tolerans yok.
- Eksik: panellerin karar bağlantısı; temas toleransı.
- Not: metin yok; görsel gösterim.

### 49. R183 · diğer · "Sektörel Döngüleri Yakalamak" (elektrik yaz/kış)
- Sonuç: H3.
- Kanıt: ham R183 aynı kayıtta eylem planı: "son 10-20 yıllık aylık getirilerini çıkarın. Hangi aylarda %70 ve üzeri ihtimalle yükseldiğine bakın". Sektör cümlesi: "enerji hisselerini talebin en düşük olduğu ... 'ölü sezonda' toplayıp, istatistiki olarak zirve yaptığı aylarda satmayı planlar".
- Bulunan kural: sektör endeksinin aylık getiri istatistiği (10-20 yıl, ≥%70 yükselen aylar) sat/al takvimi verir. "Ölü sezon" için ayrı eşik yok (en düşük aylık ortalama kabul edilir).
- Not: yazar M; kural Tansu'nun değil. Ölçüm koluna uygun.

### 50. R187 · bölge · "Alt Bantlar (Destek): -1SD veya -2SD ... Üst Bantlar (Direnç)"
- Sonuç: H4.
- Kanıt: ham R187: "Fiyatın %68.2'si 1SD, %95.4'ü 2SD ve %99'u 3SD bantları içinde gerçekleşir." Görselden: GC=F, güncel 4460,60; sağda normal dağılım ve ±SD çizgileri; IV değeri okunamadı.
- Standart: bant = fiyat × (1 ± k × IV × √(T/365)); k = 1, 2, 3. Normal dağılım kapsamı %68,27 / %95,45 / %99,73. Tansu "%99" yazıyor; yaklaşık.
- Eksik: vade T ve hangi IV (ATM, vade). Opsiyon verisi gerektirir (veri kilidi).

### 51. R187 · giriş · "-1SD seviyesine (ilk destek) geri çekilmesi güçlü bir alım fırsatıdır."
- Sonuç: H5.
- Kanıt: ham R187: "Yükselen bir trendde, fiyatın -1SD seviyesine ... geri çekilmesi".
- Eksik: yükselen trend tanımı, geri çekilme tetiği (dokunuş, kapanış).
- Yorum seçenekleri: (a) trend = fiyat > SMA50. (b) trend = EMA5>8>13 (Tansu'nun aracı). (c) dokunuşta limit alım. Tansu'nun örneği yok.

### 52. R187 · stop-geçersizlik · "stop seviyesi genellikle -2SD ... altına konulur."
- Sonuç: H5.
- Kanıt: ham R187 aynı cümle. "altına" ne kadar yazılı değil.
- Yorum seçenekleri: (a) kapanış -2SD altında. (b) -2SD − 1 ATR. En yakın: (a) (R192: "altına sarkar ve kapanış yaparsa").

### 53. R192 · teyit-tetik · "tam bir boğa trendi için fiyatın, o tepesindeki Mor ve Turuncu çizgilerin de üzerine çıkıp kalıcı olması gerekir."
- Sonuç: H5 (kısmi H2).
- Kanıt (görselden): lejant EMA 9, EMA 21, EMA 50 (mor), EMA 100 (turuncu), EMA 200 (beyaz). Renk eşlemesi lejanttan okundu; küçük yazı.
- Bulunan: mor = EMA50, turuncu = EMA100 (okuma).
- Eksik: "kalıcı" (kaç bar, kapanış mı).
- Yorum seçenekleri: (a) 2 ardışık kapanış. (b) 3 gün. Tansu'dan örnek yok.

### 54. R193 · formasyon · "HIKKAKE ... 'ayı tuzağı'"
- Sonuç: H4.
- Standart (web): Daniel Chesler, Active Trader Nisan 2004. İç mum (inside bar) + bir yönde sahte kırılım + 3-4 bar içinde karşı yönde kapanış. "Ayı tuzağı" = aşağı sahte kırılım sonrası yukarı dönüş (boğa hikkake); Tansu'nun cümlesi buna uyuyor. Kaynak: luxalgo.com, tradingsetupsreview.com.
- Okunamadı: aracın hikkake parametreleri (görselde sarı kutu etiketi).

### 55. R203 · teyit-tetik · "TP2'yi (0.618) güçlü ve hacimli bir mumla geçerse ... yeni bir yükseliş trendi olabilir"
- Sonuç: H5.
- Kanıt (görselden): TP1 84.88, TP2 87.02, TP3 90.50, TP4 92.98, STOP 64.00. Hesap: D = 81,40 alınırsa D + (C − D) × r formülü (C = 90,50) bu TP'leri verir. Yani TP formülleri H2'dir, ayrı satırdadır. "Güçlü ve hacimli mum" yazılı değil.
- Eksik: "güçlü" ve "hacimli" eşikleri; TP2 sonrası eylem.
- Yorum seçenekleri: (a) kalan %50 için trailing stop (R224: giriş + 1,5 ATR). (b) hedefi TP3/TP4'e uzat. En yakın: (a).

### 56. R216 · rejim · "Eğim Ne Kadar Dikse, Yükseliş O Kadar Güçlüdür" (DMA kanalı)
- Sonuç: H5.
- Kanıt (görselden): infografik, yazar G-dış. Sayı yok. "DMA" kısaltması hiçbir kayıtta açılmıyor.
- Eksik: DMA tanımı, eğim ölçüsü, "dik" eşiği.
- Yorum seçenekleri: (a) DMA = kaydırılmış hareketli ortalama. (b) dinamik ortalama kanalı. Doğrulanamadı.

### 57. R216 · rejim · "Evrelerin Birbirine Etkisi: Mevcut Evre Bir Sonrakini Belirler"
- Sonuç: H5.
- Kanıt (görselden): "Vasat bir yükseliş evresi, genellikle daha sert bir düşüş evresinin habercisidir. Hafif bir düşüş evresi ise bir sonraki yükselişin daha güçlü olacağına işaret eder."
- Eksik: evre sınırı, ölçü (süre, eğim). Sayı yok.

### 58. R219 · formasyon · OBO: "Üç Tepeyi Tespit Et"; "Boyun Çizgisini Çiz"
- Sonuç: H2.
- Kanıt (görselden, birebir): "1. Üç Tepeyi Tespit Et (Sol Omuz zirve, Baş daha yüksek zirve, Sağ Omuz daha alçak zirve)"; "2. Boyun Çizgisini (Neckline) Çiz: Omuzların ve başın taban dip noktalarını birleştiren bir destek çizgisi çekilir."
- Bulunan kural: baş en yüksek, sağ omuz baştan alçak, boyun çizgisi iki dibi bağlar. Sayısal tolerans yok. Yazar G-dış (Tansu paylaştı; kendi kuralı değil).

### 59. R219 · teyit-tetik · "3. Kırılımı Onayla ... Hacmi Kontrol Et"
- Sonuç: H2.
- Kanıt (görselden, birebir): "Fiyat, boyun çizgisini hacimli bir mumla aşağı kırdığında formasyon onaylanır."; "Sağ omuz oluşurken işlem hacminin azalması, formasyonun güvenilirliğini artırır."
- Eksik: "hacimli" ve "azalması" için sayı (nitel kural).

### 60. R219 · hedef-çıkış · "4. Hedef Fiyatı Belirle"
- Sonuç: H2.
- Kanıt (görselden, birebir): "Baş tepesi ile boyun çizgisi arasındaki mesafe kadar düşmesi beklenir." Standart ölçü kuralı ile aynı (web, tradingsim.com).
- Not: long-only tasarımda yalnız çıkış uyarısı (izlenebilirlik notu).

### 61. R220 · felsefe · "George Soros der ki: 'En büyük karlar Fat Tails alanında yapılır.'" (%95 / %5)
- Sonuç: H5 (kural değil).
- Kanıt: ham R220 (yazar M). %95 / %5 oranları yalnız anlatı; eşik, ölçü, işlem yok. Aynı tema R226 (aracın "güven aralığı bantları") bant genişliğini vermiyor.

### 62. R220 · rejim · "Küçük yatırımcı genelde bu %5'lik şoklarda panikleyip elindekini satar."
- Sonuç: H5 (kural değil, yorum).
- Kanıt: ham R220 aynı cümle.

### 63. R221 · teyit-tetik · "Swing Yapı ve Mum Formasyonları ... MACD ... RSI ... Hacim ve Takas Mantığı"
- Sonuç: H5.
- Kanıt (görselden): başlık "Yükseliş Gartley Formasyonu - MAKIM / Tamamlanma: 2025-11-28 | FVG: TEMAS (0.00%) | SWING: LH"; lejant Harami, Hacim MA(20), RSI, ADX, MACD, AL/SAT sinyali; RSI (14) üstte 70, altta 30 çizgisi; ADX (14) çizgisi 25; MACD periyotları okunamadı.
- Eksik: bu panellerin karar kuralı (teyit mi filtre mi).
- Not: parametreler (RSI 14, ADX 14, hacim MA 20) bulundu; kural bulunamadı.

### 64. R233 · hedef-çıkış · "pozisyonun risk/ödül oranı hedefine ulaştığında Trailing Stop (TS) ... devreye girer"
- Sonuç: H3.
- Kanıt: R224 (Tansu): "Stratejide de fiyat Giriş + 1.5 ATR seviyesine ulaştığında Trailing Stop (TS) aktif hale gelir". R239: "Statik iz süren stop: Hedef = Giriş + (1.5 × Giriş ATR) → Sabit kalır; Dinamik ... Giriş + (1.5 × O Günün ATR)". R233'teki "risk/ödül oranı hedefi" bu 1,5 ATR noktasıdır.
- Bulunan kural: TS aktivasyonu = Giriş + 1,5 ATR (statik) veya O günün ATR'si ile (dinamik).

### 65. R234 · ölçüm-ilkesi · "temel modelim de bir makine öğrenmesi algoritmasına dayanıyor:)"
- Sonuç: H1.
- Kanıt: R137: "Bu sistem satılık değil ... stratejiyi anlatmadan". R234: "Bu model üzerinde hiç çalışmadığım henüz yazdığım bir algoritma" (bu özel model için). Temel modelin yapısı verilmemiş.

### 66. R234 · teyit-tetik · "hacim RSI verileri ile lojistik regresyonla bir model"
- Sonuç: H5.
- Kanıt (görselden): "DOAS.IS - ML + Hacim + RSI Filtreli Strateji"; lejant "Güçlü AL (Vol+RSI)", "SAT", EMA 21; RSI paneli 30 / 70 çizgileri ve "Trend Ayrımı (50)". Metin: Doğruluk %55,00; Kesinlik %55,31; Duyarlılık %45,44.
- Eksik: hedef değişken (yön, kaç gün sonra), özellik listesi, olasılık eşiği, eğitim/test ayrımı.
- Yorum seçenekleri: (a) hedef: ertesi gün yükseliş; özellik: hacim oranı ve RSI(14); eşik 0,5. (b) hedef 5 günlük getiri > 0. Tansu'dan sayı yok.

### 67. R234 · ölçüm-ilkesi · "Finansal piyasalarda %70 gibi bir değer yakalarsanız bu harika bir sonuçtur."
- Sonuç: H5 (kural değil, ölçüt yorumu).
- Kanıt: ham R234 aynı cümle. R021: "Finansta %70 çok yüksek bir başarı oranıdır". Metin: "%90'lar ise mümkün değildir".
- Seçenek: kabul eşiği olarak kullanma (isabet ≥ %70); kural olarak alma.

### 68. R234 · rejim · "Trendli piyasalada çok iyi ve düşüşleri iyi yakalıyor."
- Sonuç: H5 (kural değil, iddia).
- Kanıt: ham R234. Sayı yok.

### 69. R234 · teyit-tetik · "Sistem daha seçici ve muhafazakar hale geldi. Her harekete atlamıyor"
- Sonuç: H5.
- Kanıt: aynı metin: "sadece güçlü (hacimli ve trend yönlü) fırsatlara giriyor". Görselden RSI "Trend Ayrımı (50)" çizgisi var: trend yönü = RSI > 50 olabilir. Hacim eşiği okunamadı.
- Eksik: "hacimli" eşiği; trend yönü tanımı.
- Yorum seçenekleri: (a) RSI > 50 ve hacim > 20 günlük ortalama. (b) EMA21 üstü. Görsele yakın: (a)'nın RSI kısmı; hacim kısmı tahmindir.

### 70. R234 · ölçüm-ilkesi · "Hacim ve RSI filtrelerinin eklenmesiyle modelin Doğruluk oranı %55.00 oldu."
- Sonuç: H5 (kural değil, sonuç).
- Kanıt: ham R234. Doğruluk tanımı, test dönemi ve veri bölmesi yok. Tasarım bunu ölçüt olarak almaz.

### 71. R235 · rejim · "Yükselen Trend → Birikim Süreci → Alım Tepesi / Test → Dağıtım Süreci → Satış Tepesi → Düşen Trend"
- Sonuç: H5.
- Kanıt (görselden): kitap sayfası fotoğrafı, şema; birikim ve dağıtım yatay aralık (iki kırmızı çizgi); mor kutular "Alım Tepesi", "Satış Tepesi"; yeşil ok "Test". Sayı yok. Kitap adı okunamadı.
- Eksik: evrelerin ölçülebilir tanımı.
- Yorum seçenekleri: (a) Wyckoff birikim/dağıtım şeması olarak etiketle. (b) Weinstein evreleri ile eşle (satır 18). Standart kaynak kitap bilinmiyor; doğrulanamadı.

### 72. R236 · formasyon · İkili Dip + Çekiç / Yutan Boğa / Cımbız Dip; Adam ve Havva
- Sonuç: H5 (kısmi H3).
- Kanıt: ham R236 (yazar M): "fiyatın ikinci kez dip seviyesine geldiği andır. Bu noktada oluşan bir Çekiç, Yutan Boğa veya Cımbız Dip formasyonu ... teyit eder." Yutan boğa kodu R023'te birebir var (mevcut yeşil, önceki kırmızı, mevcut açılış < önceki kapanış, mevcut kapanış > önceki açılış).
- Eksik: "aynı dip seviyesi" toleransı, iki dip arası bar aralığı, çekiç ve cımbız kodu.
- Yorum seçenekleri: (a) iki dip arası ≤ %3 fark, aralık 10-60 bar. (b) %5. Tansu'dan sayı yok; ikisi de tahmin.

### 73. R237 · rejim · "Her şey genelde piyasa için kötü algılanan bir haberle başlar ... alımları gizli ve yavaş yaparlar"
- Sonuç: H5 (kural değil, anlatı).
- Kanıt: ham R237. Ölçü yok. "Olayın özü budur." Anlatı fikri R235 ile aynı.

### 74. R243 · bölge · "FVG'yi avlamanın en kolay yolu ise büyük mumları incelemektir."
- Sonuç: H5.
- Kanıt: ham R243. FVG tanımı R199'da (1. mumun en yükseği ile 3. mumun en düşüğü arası). R050 görselinden: güç = bu boşluğun büyüklüğü, "Strongest" büyük boşluk, "Weak" küçük 2. mum. Nicel eşik yok.
- Eksik: "büyük mum" eşiği.
- Yorum seçenekleri: (a) 2. mum gövdesi ≥ 1,5 × son 20 mum ortalama gövde. (b) boşluk ≥ 1 × ATR. R050'ye en yakın: (b) (güç boşluk büyüklüğü).

---

## Sayılar

| Sonuç | Satır |
|---|---|
| H1 Gizli | 5 |
| H2 Görselde var | 7 |
| H3 Başka kayıtta var | 5 |
| H4 Standart tanım yeter | 13 |
| H5 Gerçekten eksik | 44 |
| Toplam | 74 |

H5 içinde kural olmayan satırlar (tutum, yorum, sonuç, anlatı): 13 satır (satır 5, 11, 14, 15, 17, 30, 61, 62, 67, 68, 70, 71, 73). Bu satırların eksiği "tamamlanacak parça" değildir; kural yoktur.

## H2 ve H3 ile "kural bulundu" diye açılanlar (tasarıma girmeye aday)

H2 (görselde):
1. R114 kırılma çizgisi (satır 22): kırılma = fincan sol ağız yüksekliği; yukarı kesişim = sinyal.
2. R114 fincan hedefi (satır 23): hedef = KIRILMA + (KIRILMA − dip); GUBRF için 300,75 + 88,55 = 389,30.
3. R116 gizli pozitif uyumsuzluk (satır 25): Swing=15 sol-only, MinGap=15. Gösterge kimliği okunamadı.
4. R156 APO ortalama dönüşü (satır 47): APO = EMA10 − EMA40. Eşik ±10 kitaptan; Tansu'nun görselinde yazılı değil.
5. R219 OBO yapısı (satır 58), kırılım onayı (satır 59), hedef (satır 60): nitel; yazar G-dış.

H3 (başka kayıtta):
1. R117 gizli uyumsuzluk takibi (satır 27): R116 parametreleri.
2. R138 nakit koruma (satır 43) ve R139 giriş (satır 45): AD > Ref(EMA(AD, 3), 1); aksi halde nakit. Çıkış operatörü yazılı değil.
3. R183 sektörel döngü (satır 49): aylık getiri istatistiği, 10-20 yıl, ≥%70 yükselen ay. Yazar M.
4. R233 trailing aktivasyonu (satır 64): Giriş + 1,5 ATR (R224, R239).

H4 (standart tanım): R004, R006, R007 (isim eşlemesi; tarayıcı eşiği ayrı), R053 Bollinger ±2 SD, bant genişliği, VaR, R099 mark-to-market, R108 Weinstein 30 hafta, R116 gizli uyumsuzluk = trend devamı, R126 Fib 0,786, R133 HBK (EPS), R187 IV-SD bantları, R193 Hikkake.

## H1 listesi: Tansu'ya sorulacak sorular

1. R049: Mavi çizgi hangi oran? (Ekranda "xxxx".)
2. R049: Kırmızı çizgi (sağ eksen 0-800) hangi seri?
3. R125: Pre-signal oku hangi koşulda çıkıyor?
4. R125: EMA sıkışma toleransı kaç yüzde, en az kaç gün? (R127'de KRDMD için %1,2 ve 3 gün; ICBCT için aynı mı?)
5. R136: Alt paneldeki özel gösterge nedir ve nasıl hesaplanır?
6. R137: YSA momentum çıktısında "pozitif eğim" eşiği nedir? (Not: "satılık değil, strateji anlatılmaz" dedi; cevap beklenmez.)
7. R234: "Temel model" hangi girdiyle ve hangi hedef değişkenle öğreniyor? (Aynı not: cevap beklenmez.)

8. R263 (06.10 tweet metninden): BOM sinyali nedir ve "şartlar da müsait" derken hangi şartlardır?
9. R246 (06.10 tweet metninden): "80-100 haftalık yatay" nasıl ölçülür (bant genişliği, eğim) ve çıkış nerede?
10. R249 (06.10): Three Drives'ta hedef ve stop nerede? (Tasarım: hedef C, geçersizlik 1,618 uzantısı; hedef YORUM.)

Toplam: 10 soru (H1 satırı 5; 8–10 R245–R263 tweet metinlerinden, 74 satırlık incelemenin dışında).

07.10 not taraması (beyin Ham bölümleri, görseller, defter ve ham dosyaları; Sentez kanıt sayılmadı): 10 sorunun hiçbirinin
cevabı notlarda yok. Nedenler: R049 ve R136 görsellerinde seri ve gösterge adları silinmiş ("xxxx", beyaz boya); R116
görselinin başlığı kırpılmış ("Swing=15 sol-only | MinGap=15" okunuyor, osilatör adı yok); R125'te Tansu "parametrelerin
detaylarını verip stratejimi anlatamam" der, görselde tolerans yok (EMA 30/50/100/200, R127'de 20/50/100/200); R137
eşiği "istediğim filtreyi yapabileceğim bir excel" ile kullanıcıya bırakır; R234'te girdi hacim ve RSI, hedef değişken
yok; BOM yalnız R263'te geçer, tanımsız; R246 ve R249'da çıkış/hedef/stop yazılı değil. Sorular açık kalır.

07.10 X taraması (`api.fxtwitter.com` arama, `from:The_Tansu_`; metinler `ham-yapistirmalar-3.md` Ek X1–X7):
- 5 (R136 osilatör): adı yine yok. Kısmi cevap: "günlük bakıyorum genelde 2 seneye kadar geriye bakıyorum" (X5);
  "Genellikle 10 ile 30 bar arası mesafeler en sağlıklı sinyali verir. 70+ bar sonra gelen bir dönüş, artık bir
  "uyumsuzluk" trade'inden ziyade ... yeni bir trendin başlangıcı" (X4). TMPOL görseli R116 ile aynı, başlık kırpık.
- 6 (R137 eğim eşiği): kısmi. "Eğer eğim negatiften pozitife dönüyorsa, momentum yukarı yönlü ivme kazanmaya başlamış
  demektir." (X6): eşik işaret değişimidir (0); YSA çıktısının eşiği yine yok.
- 8 (BOM): kısmi. "noktanin gerçekten swing lowpivot olduğundan emin olmak için X bar kadar öteleyerek kodladım" (X1):
  BOM bir swing dip pivotudur, sağında X bar ister. Görselde BOM, talep bölgesi başındaki "D-HL" ve bir swing dipte;
  IDGYO'da Elliott C dibinden sonra "BOM sinyalim de teyit vermişti" (X3). Tam kural ve "şartlar" yine yok.
- 9 (R246): kısmi. 2025 yatay kanal taraması: "kanalın alt bandına yaklaşıldığında hisse almak, üst banda
  yaklaşıldığında ise satmaktır"; hacimli kırılımda kırılım yönü; "mutlaka stop seviyeleri belirlemek ve hacimle teyit
  almaktır" (X7). Çıkış = üst bant. Yataylık ölçüsü yine yok.
- 1, 2, 3, 4, 7, 10: X'te yeni bilgi bulunamadı (arama: xxxx, pre signal, sıkışma, lojistik, temel model, three drives,
  conversation_id). Not: arama dizini konuşma yanıtlarının yalnız bir kısmını döndürür; bulunamadı "yok" demek değildir.

## H5 için en önemli 10 yorum kararı

1. Fincan-kulp tespiti (R114): dip, sol ağız ve sağ ağız nasıl seçilir; kulp en fazla kaç % geri çekilir. Tansu'nun GUBRF örneğine uyan: sol ağız = dipten önceki en yüksek pivot (300,75); kulp tabanı görselde %61,8 ile %78,6 arasında.
2. Fincan risk/ödül (R114): giriş ve stop çizgisi. 1:2,27 hiçbir basit seçenekle çıkmıyor; ya GUBRF'nin gerçek giriş fiyatı alınır ya da Tansu'ya sorulur.
3. Bant kuyruğu girişi (R053, R187): dokunuşta mı, kapanışla geri dönüşte mi alınır; çıkış orta bantta mı; stop -2SD altında kapanış mı.
4. Yön çatışması (R076): long-only sistemde sell yönlü AB=CD ile yukarı kırılım çakışırsa işlem yok mu, yalnız çıkış uyarısı mı.
5. Volatilite rejimi (R077, R092): v_t tanımı, bant genişliği, yeşil üçgenin tetiği.
6. Güçlü yeşil mum, yüksek yakın kapanış (R124): gövde eşiği (ATR katı) ve kapanış konumu eşiği.
7. Ortalamadan uzaklık (R128): eşik. Tansu'nun örneği EMA50'den +%9,59.
8. Düşük hacim ve spread eşiği (R118, R119): ortalamanın altı mı, alt %25 mi (R232), spread medyan mı ortalama mı.
9. Walk-forward ayarı (R138): eğitim/test pencere uzunluğu, aday EMA aralığı, amaç fonksiyonu.
10. R110 "%50" ve R121 "Optimal Momentum+": birinde oranın neyin oranı olduğu, diğerinde "+"ın anlamı ve amaç fonksiyonu (Sharpe). İkisi de tasarım dışı bırakılırsa karar gerekmez.
