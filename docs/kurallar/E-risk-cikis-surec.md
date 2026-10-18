# E. Risk, çıkış ve süreç kuralları (Tansu kaynaklı)

Hazırlanma: 2026-10-05. Yalnız okuma araştırması. Hiçbir parametre uydurulmadı. Boşluklar YORUM etiketiyle işaretli.

## 0. Nasıl okunur

Kaynak kökü: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`. Görseller `assets\<klasör>\` altında. Kısaltma: G = gorsel-paket, T = tweet-, K = kaynak-.

Kaynak türü ve YORUM tanımları GLOSSARY'dedir. Bu dosyada etiketler Ham (birinci el), BİRİNCİ EL (görsel), NOTEBOOKLM (NotebookLM görseli; birinci el, etiket yalnız bilgi verir), İKİNCİ EL (notun Ham dışındaki bölümleri) ve YORUM olarak yazılır; notların Ham dışı bölümlerindeki "Levent ... belirtti" cümleleri aktarılan metnin özetidir.

Uyarı 1: Notlarda "Levent" sözcüğü aktarılan tweet metnini anlatan kişiyi gösterir. Çoğu notta tweet URL'si yok ve Ham'da yazar yok. Yazarın Tansu olduğu havuz bağlamından gelir. Havuz ana notu "Levent'in X paylaşımlarından derlediği" der. Yani yazar atfı çoğu not için doğrulanmış değil. Tek istisna: `not-backtest-giris-sadeligi-risk-islem-gunlugu.md` (URL: x.com/The_Tansu_/status/2095213493133713664, 2 Eylül 2026) ve K-akfis (3 Eylül 2026).

Uyarı 2: `T-atr-risk-butcesi-position-sizing-stop-loss` için `assets` klasörü yok. Yalnız metin ve bir Python satırı var. İkisi de Ham (birinci el); Ham'da yazar yok.

Uyarı 3: Notlardaki "Cevo katkısı", "Cevo düzeltmesi", test fixture, state machine ve "kanonik" bölümleri Tansu'ya ait değil. Bunları Tansu ifadesi olarak kullanma.

Uyarı 4: 05.10 ön denemesi "4 ATR hedef" ve "kapanış EMA50 altı bozulma" kullandı; bu kaynaklarda ikisi de yok. Tansu'nun 2 ATR stopu var. Güncel karar: varsayılan kuralda hedef yok (EMA ailesinin hedefi varyantlardadır, KURALLAR §3), gün sonu stopu SMA250 (YORUM); sahip TASARIM §5.5, KURALLAR §1 madde 4. Aşağıdaki "4 ATR hedef" ve "EMA50" anmaları bu eski ön denemeyi gösterir. (bilet 04, 14.10)

---

# BÖLÜM 1. Pozisyon büyüklüğü ve stoplar

## K1. Risk bütçesi ve lot hesabı (%1 / 2 ATR)

- Kaynak: G-115 (`assets/gorsel-paket-115-position-sizing-1pct-2atr-sma250/01-position-sizing-yuzde1-2atr-sma250-stop.jpg`), T-atr-risk-butcesi (Ham), T-volatilite-ters-orantili (Ham).
- Tansu'nun ifadesi:
  - Görsel, verbatim (NOTEBOOKLM görseli, birinci el): "Risk Tutarınızı Belirleyin: Toplam sermayenizin en fazla %1'ini kaybetmeyi göze alın." "Hisse Adedini Hesaplayın: Belirlediğiniz risk tutarını, hissenin 2 ATR (Ortalama Gerçek Aralık) değerine bölün." "Örnek Hesaplama: 100.000$ sermaye ve 14.30$ 2 ATR için: 1.000$ / 14.30$ = ~70 hisse."
  - G-115 Ham (paraphrase): Sermayenin %1'ini kaybetmek göze alınır; giriş bileşenlerinden biri 250SMA olabilir, SMA200, EMA200 veya EMA250 de seçilebilir. İşlemde kaç lot alınacağını bilmek yatırımcılığın en önemli konularından biridir.
  - T-atr-risk-butcesi Ham (paraphrase): "Hayat kalitesini bozmayacak sermaye", işlem başına TL risk bütçesi. Formül: "Göze Alınan Kayıp / Hisse Volatilitesi = Lot Sayısı". Örnek: "500 TL / 2 TL = 250 Lot" (Ham: volatilite "2 ATR değeri" 2 TL). Python satırı: `Close[-1] - 2*ATR[-1]`.
  - T-volatilite-ters-orantili Ham: Volatilitesi yüksek hissede pozisyon büyüklüğü küçülür. Ana amaç sermayeyi korumak. "Oyuna dahil olmamız gerektiğinde zaten oluruz."
- Tanım (günlük OHLCV ile hesaplanabilir):
  1. `risk_tutarı = sermaye × 0,01`.
  2. `stop_mesafesi = 2 × ATR` (hisse başına, fiyat birimi).
  3. `lot_ham = risk_tutarı / stop_mesafesi`.
   4. Lot = tam sayı. Aşağı yuvarlama YORUM'dur; yaklaşık 70 hisse paylaşılan NotebookLM örneğidir, yuvarlama talimatı yoktur (NotebookLM, G115/g1, örnek hesap). 1000/14,30 = 69,93; 70 × 14,30 = 1001 > %1.
  5. Görsel metni "2 ATR değeri" der. 14,30 = 2 ATR mesafesi okunur (NOTEBOOKLM). T-atr-risk-butcesi örneğinde "2 TL" için aynı okuma doğru olursa 250 lot. ATR = 2 TL olsaydı 125 lot olurdu. Metin 250 diyor. Yani payda = 2×ATR mesafesi (görselde açık; T-atr-risk-butcesi Ham'ında "volatilitesi/2 ATR değeri").
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| risk / işlem | %1 sermaye (örnek) | Ham G-115; NotebookLM, G115/g1; genel oran seçimi YORUM |
| stop mesafesi çarpanı | 2 ATR | görsel G-115 |
| örnek sermaye | 100.000 USD | görsel G-115 |
| örnek 2 ATR | 14,30 USD | görsel G-115 |
| örnek sonuç | ~70 hisse | görsel G-115 |
| ATR periyodu | verilmedi | YORUM (14, Wilder) |
| ATR hangi zaman diliminde | verilmedi | YORUM (günlük) |
| aşağı yuvarlama (69) | verilmedi | YORUM |
| komisyon/kayma payı | verilmedi | YORUM (sıfır başla, duyarlılık koş) |
| sermaye = nakit mi, toplam özkaynak mı | verilmedi | YORUM |

- Belirsiz kalanlar: ATR uzunluğu ve yumuşatma türü. Sermayenin tanımı (anlık özkaynak mı, başlangıç mı). Birden fazla açık pozisyonda toplam açık risk sınırı var mı (Tansu söylemedi). Lot üst sınırı (nakit aşımı). Aynı anda açık pozisyon sayısı. Örnekte giriş fiyatı yok, yani 70 × fiyat sermayeyi aşar mı bilinmiyor.
- Tansu'nun kanıtı: Tek örnek hesap. Performans, backtest, sembol yok. Sonuç: aritmetik tutarlı, edge kanıtı yok.
- Bedava günlük veriyle uygulanabilir mi: Evet. ATR günlük High/Low/Close ile hesaplanır. Lot bölünebilirliği (BIST 1 lot) için ek veri gerekmez.
- Kaynak güveni: Lot formülü T-atr-risk-butcesi Ham'ında, %1 ve 250SMA G-115 Ham'ında, 2 ATR'ye bölme örneği NotebookLM görselindedir (hepsi birinci el). Örnek kullanım "gerçek Tansu işlemi" değil. ATR detayı yok. Orta.

## K2. Acil stop (giriş − 2 ATR, gün içi anında çıkış)

- Kaynak: G-115 (NotebookLM görseli), G-125 (`assets/gorsel-paket-125-kismi-kar-trailing-stop/01-kismi-kar-trailing-prev-low-emergency-stop.jpg`), T-atr-risk-butcesi (Ham). Acil Stop ve Gün Sonu Stop adları Ham metinde vardır (Ham, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Tansu'nun ifadesi:
  - Görsel G-115, verbatim (NOTEBOOKLM görseli, birinci el): "Acil Durum Stop'u: Giriş fiyatının 2 ATR değeri kadar altına bir stop noktası koyun." "Anında Çıkış Kuralı: Fiyat gün içinde acil durum stop seviyesine düşerse, anında pozisyonu kapatın."
  - G-125 Ham: "emergency stop 2atr ile kalan tüm maldan çıkış".
  - G-125 görsel (BİRİNCİ EL): Sol uçta kırmızı kutu etiketi "STOP" ve "ATR" satırları. Bilet 04 (14.10) görseli açıp büyüterek inceledi (dosya: `assets/gorsel-paket-125-kismi-kar-trailing-stop/01-kismi-kar-trailing-prev-low-emergency-stop.jpg`, 680×147 piksel; etiket yazısı yaklaşık 3 piksel yüksekliğinde). Rakamlar **okunamaz**: önceki iki okuma çelişir ("184.54 / 4.62" bu dosyada ve havuz notunda; "104.34 / 4.62" taslak M ve taslak parçalarında), ikisi de doğrulanamaz. Hiçbir kural bu sayıya dayanmaz. Bu çelişkinin tek kaydı burasıdır; başka dosyalar sayı yazmaz, buraya atıf verir. (bilet 04, 14.10; yazıcı kararı)
  - T-atr-risk-butcesi Ham: "Giriş fiyatının 2ATR altına da acil stop konulur." "Acil Stop: Fiyat bu seviyeye değdiği an, gün sonunu beklemeden derhal çıkılır."
- Tanım:
  1. Giriş günü: `stop = giriş_fiyatı − 2 × ATR` (ATR giriş kararında bilinen son tamamlanmış değer, YORUM).
  2. Her gün: `Low ≤ stop` ise çık (gün içi temas).
  3. Gün düşüğü stopun altındaysa dolum fiyatı TASARIM 5.3'tedir; kaynak boşlukta dolumu açıklamaz (YORUM).
  4. Aynı gün hem stop hem hedef değerse stop önce (YORUM, muhafazakâr).
   5. YORUM: bizim seçimimiz giriş ATR'si değişse bile stopu sabit tutmaktır. Ham giriş−2ATR ile güncel Close−2ATR'yi birlikte verir; başlangıç stopu ile güncelleme politikası ayrımı açık değildir (Ham, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| çarpan | 2 ATR | görsel G-115, Ham G-125, Ham T-atr-risk-butcesi |
| tetik | gün içi temas, anında çıkış | görsel G-115 |
| etiket örneği | "STOP" ve "ATR" etiketi var; rakamlar okunamaz (yukarıdaki G-125 görsel maddesi) | görsel G-125 |
| ATR periyodu | yok | YORUM (14) |
| ATR sabit mi, hareketli mi | başlangıç stopu için kaynak güncelleme politikası vermiyor; iz süren stop eşiği için statik ve dinamik iki biçim vardır (K4) | YORUM: girişte sabit bizim seçimimiz; başlangıç/güncelleme ayrımı belirsiz (Ham, tweet-atr-risk-butcesi-position-sizing-stop-loss:22) |
| tetik fiyatı: Low mu, son işlem mi | yok | YORUM (günlük Low) |
| boşlukta dolum | yok | YORUM (TASARIM 5.3) |
| stop fiyatına limit emir mi, piyasa emri mi | yok | YORUM (piyasa) |

- Belirsiz kalanlar: G-125 etiketindeki stop sayısı giriş − 2×ATR midir? Rakamlar okunamadığı ve giriş fiyatı grafikte okunmadığı için sınanamaz. G-125 etiketi soldadır, yani giriş anında yazılmış stop gibi görünür; bunu doğrulayan metin yok. Stop long için yazılmış; short için Tansu bir şey demedi.
- Tansu'nun kanıtı: Yok (kural anlatımı). G-125 grafiği seçilmiş tek örnek.
- Bedava günlük veriyle uygulanabilir mi: Evet, günlük High/Low ile. Gün içi sıra bilinmediği için aynı gün stop+hedef çatışması çözülemez (stop önce varsayımı). Projede Open yoktur (TASARIM 5.1); açılış boşluğu TASARIM 5.3'te AOF ile modellenir.
- Kaynak güveni: Kural T-atr-risk-butcesi Ham'ında, G-125 Ham'ında ve G-115 NotebookLM görselindedir (hepsi birinci el). Orta-yüksek. Uygulama ayrıntıları yok.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-2atr-stop-bant-al-sinyali-1987526117389922781` — 2 ATR stopunu (YORUM: "2ATR" stop çarpanı diye okundu) volatil piyasada trendde kalma gerekçesi olarak tekrar eder: "Volatil piyasalarda 2ATR'nin gücü sizi trendde tutar" (Ham). Görsel etiketi "STOP: 0.86 / ATR: 0.39 / AL" (görsel metni). Giriş fiyatı görselde yok, bu yüzden stop = giriş − 2 ATR doğrulanamaz.
  - `tweet-atr-acil-stop-iki-kosul-cikis-1992564976113143927` — Okunabilir acil stop etiketi: "EMERGENCY STOP: 117.12 / ATR: 3.08", grafikte GİRİŞ okunun altında; ayrıca "TS: 128.18" etiketi (anlamı yazılı değil) ve "S1+S2 %100" tam çıkış (görsel, açıldı). "Sistemin 2 koşulu sağlamayınca %100 satış yaptırdığı yerden düşüşe bakınız." (Ham). S1 ve S2 koşulları yazılı değil; giriş fiyatı görselde yok.
  - `tweet-atr-stop-kar-alma-1958800350435029372` — ATR ile stop koyma tavsiyesi, AVHOL için %6-7 kâr örneğiyle: "Satmadı iseniz ve zararda iseniz Atr ile stop koymadığınız için yine sözüm yok." (Ham). Çarpan yazılı değil; tekrar, sayısal parametre yok.
  - `tweet-atr-14-tr-formulu-2atr-esigi-1987507728718205244` — Okuma (YORUM): Bu ATR açıklaması 14 günlük basit ortalamayı verir. Ham: "ATR periyodu 14 gün olarak varsayılır." ve "Elde edilen bu 14 günlük Gerçek Aralık (TR) değerlerinin basit hareketli ortalaması (SMA) alınarak 1 ATR değeri bulunur." İki katı: "2 ATR = 1 ATR Değeri (x) 2".
  - `tweet-atr-stop-marubozu-hacim-delta-2044863959027925319` — Okuma (YORUM): ATR stop ile kâr alma veya hacim-delta incelemesi önerilir. Ham: "ATR bazlı stop ile sürekli kar alacaksınız" ve "marubozu düşük hacim fake'dir,yüksek hacim ise dönüş sinyalidir."
  - `tweet-gunluk-kirilim-bosluk-atr-stop-2002784596455244247` — Okuma (YORUM): Kırılım ve boşluk anlatımında farklı ATR stop örneği. Ham: "günün ATR'si neyse, giriş yerinizden o kadar uzağa stop koyarak". Retest ve hacim teyidi: "Kırılımlarda hacim onayı ve retest bekleyin". Mevcut 2 ATR kuralını değiştirmez.

## K3. Gün sonu (kapanış) stopu: SMA250

- Kaynak: G-115 (NotebookLM görseli), T-atr-risk-butcesi (Ham). Gün Sonu Stop adı Ham metindedir: "Kapanış bazlıdır ve sizin risk algınıza göre değişir" (Ham, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Tansu'nun ifadesi: NotebookLM görseli SMA250 altında kapanışta çıkışı gösterir (NotebookLM, G115/g1; birinci el). Ham'da ortalama seçimi okura bırakılır: "stratejinize kalmış" (Ham, G115:20); SMA200, EMA200, EMA250 alternatifleri vardır. YORUM: SMA250'yi kesin giriş filtresi olarak seçmek bizim kararıdır; giriş karşılaştırması kaynakta yoktur.
- Tanım:
  1. Her gün kapanışında `Close < SMA250` ise çıkış sinyali.
  2. Çıkış zamanı ve fiyatı TASARIM 5.5'tedir (YORUM). Tansu "gün sonu" der; kapanışta emir mi, ertesi gün mü belirtmedi.
  3. K2 acil stop bundan bağımsız ve önceliklidir (YORUM; infografik iki kuralı yan yana verir, öncelik sırasını yazmaz).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| ortalama | SMA 250 gün | görsel G-115 |
| alternatifler | SMA200, EMA200, EMA250 | Ham G-115 |
| tetik | kapanış < ortalama | görsel G-115 |
| tampon/histerezis | yok | YORUM (0) |
| çıkış zamanı | yok | YORUM (TASARIM 5.5) |
| fiyat bazı: düzeltilmiş mi, ham mı | yok | YORUM (düzeltilmiş) |

- Belirsiz kalanlar: Seçim kuralı (hangi ortalama?). Giriş de SMA250 üstü mü gerektirir (Ham: giriş bileşenlerinden biri; geri kalan bileşenler verilmedi). 250 gün veri yoksa ne olacak (YORUM: sinyal yok).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet. 250 gün geçmiş gerekir (yeni halka arzlar elenir).
- Kaynak güveni: SMA250 altı kapanış çıkışı NotebookLM görselindedir (birinci el); SMA250 giriş bileşeni ve alternatifler G-115 Ham'ındadır. Orta-yüksek.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ema200-alti-kapanis-boyun-cikis-1771661476517810644` — ASTOR gerçek örneği (23.03.2024): "Cuma kapanışı 200EMA altında gerçekleşti." (Ham); beklenen geri çekilme 90, kötü senaryo 83,77, en kötü 66. 83,77 görselde Fib 0 seviyesi, EMA200 çizgisi fiyatın üstündedir (görsel, açıldı). Çıkış sinyali EMA200'den değil "Ok ile işaretlenen boyunun kesilmesi" ile verilmişti; "boyun" anlamı belirsiz (Ham). Parametre: ortalama = EMA200, kapanış bazlı (Ham; K3'te alternatif olarak var; bu örnekte çıkış tetiği olduğu söylenmiyor, yalnız olumsuz okuma).

## K4. İz süren stop (trailing)

- Kaynak: G-125 (görsel + Ham); Ham, tweet-statik-dinamik-iz-suren-stop-atr:20.
- Tansu'nun ifadesi (Ham, tweet-statik-dinamik-iz-suren-stop-atr:20): İki biçim de bu Ham metnindedir (Ham'da yazar yok). Statik: "Hedef = Giriş + (1.5 × Giriş ATR) → Sabit kalır". Dinamik: "Hedef = Giriş + (1.5 × O Günün ATR) → Her gün değişir". Ham metni dinamiği tercih eder: "Bu daha zekice bir trailing stop yöntemidir." Giriş + 1,5 ATR aktivasyonu ve bundan sonraki barlarda ilk önceki dip altı kapanışta %50 satış anlatılır. G-125 grafiğinde çizgi/bantlar vardır; formül okunmaz.
- Tanım (kaynak sırası; Ham, tweet-statik-dinamik-iz-suren-stop-atr:20):
   1. Aktivasyon eşiği iki biçimdedir: statik `giriş + 1,5×ATR_giriş` (sabit), dinamik `giriş + 1,5×ATR_t` (ATR_t o günün ATR'si, her gün değişir). YORUM: bizim seçim `High ≥ giriş + 1,5×ATR_giriş` (statik); Ham metni dinamiği önerir. High teması mı kapanış mı kullanıldığı kaynakta açık değildir.
   2. Giriş + 1,5 ATR aktivasyonu geçilir; satış koşulu bundan sonraki barlarda aranır.
   3. Bu barlardan ilk `Close[t] < Low[t−1]` kapanışında %50 satış sinyali oluşur.
   4. %50'nin ilk mi kalan miktara mı uygulandığı açık değildir (Ham, G125:20).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| aktivasyon | giriş + 1,5 ATR (statik: giriş ATR'si, sabit; dinamik: o günün ATR'si, her gün değişir) | Ham, tweet-statik-dinamik-iz-suren-stop-atr:20 |
| satış sırası | aktivasyondan sonraki barlarda ilk dip-altı kapanış | Ham, tweet-statik-dinamik-iz-suren-stop-atr:20 |
| aktivasyon temeli (High/Close) | yok | YORUM |
| trailing ATR sabit mi | statik (sabit) ve dinamik (her gün) iki biçim var; Ham metni dinamiği önerir | Ham, tweet-statik-dinamik-iz-suren-stop-atr:20; YORUM: bizim seçim statik; Ham metni dinamiği önerir |
| Chandelier / yalnız yukarı / max stop | kaynakta yok | YORUM alternatifleri; aktarılan dip-altı satış kuralının parçası değil |

- Belirsiz kalanlar: aktivasyonun High/Close bazı, dinamik biçimde ATR'nin hangi bardan okunduğu, aynı bar sırası, %50 paydası ve dolum zamanı. Chandelier ve max stop zinciri kaynak kuralı değildir (Ham, tweet-statik-dinamik-iz-suren-stop-atr:20).
- Tansu'nun kanıtı: G-125 grafiği; seçilmiş, olumlu yönetim örneği. Fiyat çıkış oklarından sonra düşer. Fiyat/dolum etiketi yok.
- Bedava günlük veri: kapanış ve önceki Low hesabı yapılabilir; aktivasyonun fiyat alanı, ATR zamanı ve dolum ayrıntıları açık değildir.
- Kaynak güveni: Düşük-orta. Aktivasyon formülü Ham'da var (iki biçim); fiyat alanı ve dolum yok.
- Modül 1 çıkış paketi: KURALLAR §3.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-atr-iz-suren-stop-1933510083163406784` — ATR ile iz süren stop kullanma tavsiyesi, sonuç yorumu olarak: "Atr ile iz süren stop koymazsan bugünkü gibi mal gibi malda kalırsın." (Ham). Çarpan, periyot ve güncelleme kuralı yok; tekrar.
  - `tweet-atr-iz-suren-stop-1960955617868210398` — ATR tabanlı iz süren stopun gerekçesi ve sınırları: sabit yüzde yerine volatiliteye göre stop; dezavantajlar: geç stop, düşük hacimli hissede yanlış sinyal, ATR periyodunu anlama gereği. "Burada ATR tabanlı iz süren stop yöntemi devreye girer." (Ham). Sayı, çarpan ve periyot yok.
  - `tweet-atr-iz-suren-stop-momentum-cikis-1948688680555790671` — Tutma/izleme ayrımı: momentum alanındaysa ve fiyat trend devam olasılığının üzerindeyse tutar, değilse ATR ile iz süren stopla izler. "Hisse momentum alanda iken fiyatı , trend devam olasılığının üzerinde ise hisseyi tutarım değilse Atr ile iz süren stopla takip yaparım" (Ham). "Momentum alanı" ve "trend devam olasılığı" ölçüsü yazılı değil (YORUM).
  - `tweet-dinamik-atr-kar-alma-sistemi-2020653845316309354` — THYAO grafiği "DİNAMİK ATR BAZLI KAR ALMA SİSTEMİ" (görsel, açıldı): giriş oku, her barda değişen kesikli ATR bantları, sarı yıldız, düz kırmızı kesikli stop çizgisi ve kırmızı X çıkış; sayı ve etiket yok. Ham: "Stop avcıları her yerde." (Ham). YORUM: bantlar günlük ATR'ye bağlı dinamik hedef biçimini gösterir (09.02.2026).
  - `tweet-izleyen-stop-trend-takibi-2052841801157841279` — Mum grafiğinde fiyatın altında mavi noktalı iz süren stop çizgisi ve siyah X çıkış işaretleri var; formül yok: "Bilimsel yolla trend böyl takip edilir:)" (Ham). Mart-Kasım 2025 penceresi; yükselişte çizgi yukarı basamaklanır, X'ten sonra çizgi fiyatın altından yeniden başlar (görsel, açıldı).
  - `tweet-statik-dinamik-atr-iz-suren-stop-1989985215452758434` — Tekrar ve yazar teyidi: K4'ün dayandığı statik ve dinamik iz süren stop metni Tansu'nun kendi X gönderisi olarak geldi (16.11.2025): "Dinamik İz Süren Stop Hedef = Giriş + (1.5 × O Günün ATR) → Her gün değişir" (Ham). "Bu daha zekice bir trailing stop yöntemidir." (Ham). Yeni değer yok; K4'teki "Ham'da yazar yok" notu bu gönderi için geçerli değil.

## K5. Kısmi kâr ve "önceki gün dibi altı kapanış → %50 sat" (G-125)

- Kaynak: G-125 (görsel + Ham).
- Tansu'nun ifadesi (Ham, G-125, paraphrase): Görsel oklarını soldan sağa şöyle anlattı: giriş, ilk kâr alma, ikinci kâr alma, trailing/büyük kâr satış dönemi, "önceki günün en düşüğünün altında kapanış ve %50 satış", "emergency stop 2atr ile kalan tüm maldan çıkış". İlk kâr alma için "%10 (sizin belirleyeceğiniz)" der; oran kullanıcı/strateji tarafından seçilir. Görselden sonra fiyatın düşmeye devam ettiğini belirtti. Kısmi kâr almanın karmaşık ve çoklu çıkış koşullu stratejilerde belirli amaçlara hizmet ettiğini söyledi.
- Görsel (BİRİNCİ EL): Kırmızı oklar ve sarı yıldız işaretleri. Fiyat/tarih/TP seviyesi yazısı yok. Yalnız bir STOP / ATR etiketi vardır; rakamları okunamaz (K2, G-125 görsel maddesi).
- Tanım (kaynakta olan iskelet):
  1. Giriş.
  2. TP1: "%10" (anlamı belirsiz, aşağıda).
  3. TP2 (ikinci satış): ayrıntıları belirtilmemiş.
  4. Fiyat ≥ giriş + 1,5 ATR: trailing aktif (K4).
   5. Aktivasyon geçildikten sonraki barlardan ilk `Close[t] < Low[t−1]` kapanışında %50 satış sinyali oluşur (Ham, tweet-statik-dinamik-iz-suren-stop-atr:20); kısmi satışın dolumu YORUM'dur (TASARIM 5.3); EMA ailesinin varyantları bu satışı dener (KURALLAR §3, dip varyantı; TASARIM 5.5, iz süren stop ve kısmi kâr maddesi).
  6. 2 ATR emergency stop: kalan tamamını kapat (girişten itibaren aktif, YORUM).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| TP1 | "%10" | Ham G-125 |
| TP1 anlamı | fiyat %10 mu, pozisyonun %10'u mu | belirsiz |
| TP2 (ikinci satış) | ayrıntıları belirtilmemiş | Ham, G125:20 |
| trailing aktivasyon | giriş + 1,5 ATR | Ham G-125 |
| önceki gün dibi tetik | aktivasyon geçildikten sonraki barlarda ilk kapanış < Low[t−1] | Ham, tweet-statik-dinamik-iz-suren-stop-atr:20 |
| azaltma oranı | %50 | Ham G-125 |
| %50 paydası | ilk lot mu, kalan lot mu | belirsiz |
| emergency | 2 ATR | Ham G-125 |
| tampon | yok | YORUM |

- Belirsiz kalanlar: (i) %10 fiyat getirisi mi (`giriş × 1,10`) lot oranı mı (`ilk lot × 0,10`). (ii) İkinci satışın ayrıntıları belirtilmemiş. (iii) %50 ilk miktarın mı kalan miktarın mı yarısı (Ham, G125:20). (iv) Kısmi satış sonrası stop taşınması. (v) Aynı gün olay sırası ve dolum. (vi) Adım sırası iki kaynakta farklıdır: statik tweet (Ham, tweet-statik-dinamik-iz-suren-stop-atr:20) ilk kâr almayı aktivasyondan sonraki ilk dip-altı kapanış (%50) yapar; G-125 Ham'ı %10 kâr alma ve ikinci kâr almayı trailing ve dip-altı %50'den önce sayar. Tek geçerli sıra seçilmedi. Dip-altı kapanış aktivasyondan sonraki barlarda aranır (Ham, tweet-statik-dinamik-iz-suren-stop-atr:20).
- Tansu'nun kanıtı: Tek seçilmiş grafik. Backtest yok, dolum yok, tam-çıkış kıyaslaması yok.
- Bedava günlük veri: Evet (Low[t−1], Close, ATR). Önceki gün dibi günlük mumdan hesaplanır.
- Kaynak güveni: Düşük. Yalnız Ham metni (TP rakamı ve formül yok) ve okunmayan grafik. TP1/TP2 ve %50 kimlikleri çözülmeden uygulanamaz.
- Modül 1 çıkış paketi: KURALLAR §3.
- RSI 30 girişi ve iki aşamalı çıkış (`tweet-rsi30-giris-iki-asamali-cikis`; Ham; Ham'da yazar yok; grafik notta yok; bilet 04, 14.10): giriş: RSI(14) 30'un altından yukarı kesip üzerinde kapanış yapar. Kâr alma: RSI(14) 70'in üzerindeyken 70'in altında kapanırsa (RSI 70 reddi) pozisyonun %50'si satılır; kalan %50, bir önceki günün low'unun altında kapanışta satılır ve işlem biter. Tansu'nun cümlesi: "Üst paneldeki mumlar sırası ile giriş noktası, trailling noktası, ilk %50 kar aldığımız RSI70 reddi ve ikinci %50 kar aldığımız önceki mumun en düşüğünün altında kapanış." Parametre: RSI(14), 30, 70, %50 + %50 (Ham). Belirsiz: başlangıç ("sıkı") stop yok; "risk/ödül hedefi" ile "SMA 50 / RSI 50 dirençleri" ilişkisi belli değil; trailing noktası tanımsız; backtest yok. K5 ile fark: K5'te önceki gün dibi altı kapanış ilk %50'yi satar ve kalanı 2 ATR acil stop kapatır; bu notta aynı kapanış kalan %50'yi (tam çıkışı) satar, ilk %50'yi RSI 70 reddi satar. İkisi ayrı Tansu notudur; çözülmedi, K5 değişmedi.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-atr-stop-hedef-iki-kademeli-yari-satis-1989777185264066973` — İki koşullu yarım satış (K1, K2) çıktısı: K1 ile pozisyonun %50'si satıldı (2025-07-07, 182.50, +%10.61), K2 ile kalanın %50'si satıldı (2025-08-20, 196.10, +%18.85), kalan %25 (görsel, açıldı). Grafikte "HEDEF: 173.49 (1.5 ATR)", "STOP: 153.69", "ATR: 5.66" etiketleri okunur. K1 ve K2 koşulları yazılı değil. "Sırf grafiklere bakmamak için, tembelliğimden, şöyle bir sistem yazıyorum." (Ham) Parametre: hedef etiketi = giriş + 1.5 ATR ("HEDEF: 173.49 (1.5 ATR)") (görsel, açıldı); stop = giriş − 2 ATR (hesap, YORUM: 173.49 − 1.5 × 5.66 = 165.00; 153.69 + 2 × 5.66 = 165.01; 182.50 / 165.00 = %10.61 ile tutarlı); kısmi satış = %50 + kalanın %50'si, kalan %25 (görsel, açıldı).
  - `tweet-gun-ici-yuzde-3-5-kar-al-1925591759523840425` — Gün içi işlemde sabit kâr alma hedefi: yüzde 3–5 görünce çık. "%3-5 gör, at cebe çekil hocam." (Ham). Gün içi veri TASARIM §3 kapsam dışıdır. Görselde (ATR Directional Change Extreme Points) hedefle ilgili sayı yok (görsel metni). Parametre: gün içi kâr alma hedefi = %3-5 (Ham); pozisyonun ne kadarının satılacağı belirsiz.
  - `tweet-rsi30-donus-yari-ve-tam-cikis-kurallari-1991721699922870638` — RSI 30'dan dönüşte direnç ve çıkış: 50 RSI ve 50 SMA tavan görevi görür. %50 satış koşulları: fiyat RSI 50'yi veya SMA 50'yi reddeder; ya da 1.5 ATR kârdayken önceki günün düşüğünün altında kapanış gelir. "Bu 3 senaryodan herhangi ikisi gerçekleşirse işlemin tamamını kapatın." (Ham). K5'teki RSI 70 reddi çıkışından farklı ikinci kurgu. Parametre: yarı çıkış koşulları = RSI 50 reddi, SMA 50 reddi, 1.5 ATR kârda önceki gün düşüğü altı kapanış; tam çıkış = üç koşuldan herhangi ikisi (Ham); "reddetme" tanımı, RSI periyodu ve SMA'nın kapanış temeli yok

## K6. Volatiliteyle ters orantılı pozisyon (kavram) ve GARCH sözü

- Kaynak: T-volatilite-ters-orantili (Ham), T-garch-standart-sapma (Ham).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok): "Volatilitesi yüksek olan hisselerde position sizing matematiksel olarak küçülür ve bu çok doğrudur." "Yüksek volalite yüksek kar olduğu kadar yüksek risk ihtiva eder." "Asıl amacımız sermayemizi korumak." "Oyuna dahil olmamız gerektiğinde zaten oluruz." T-garch-standart-sapma: GARCH ve standart sapma ile volatilite riskini azaltma örneğini "bu akşam" göstereceğini söyledi (söz; örnek yok).
- Tanım: K1 ile aynı. Sabit parasal risk / geniş ATR stopu = küçük lot. Volatilite ölçüsü, pencere verilmedi. GARCH içeriği yok (yalnız vaat).
- Parametreler: Hepsi yok. Pencere, ölçü (std/ATR/GARCH), risk % (K1'den %1 alınabilir, YORUM).
- Belirsiz kalanlar: Ters orantılı ağırlık (inverse-vol portföy) mı, sabit risk lotu mu. Notlar ikisini ayırır; Tansu ayırmadı.
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: İlke düzeyi (Ham). K1 ile tutarlı.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-volatiliteye-gore-pozisyon-buyuklugu-1987500065401733478` — K6'nın belirsizliğini kapatır: ters orantılı portföy ağırlığı değil, sabit TL risk için değişken lot: yüksek volatilite, stop mesafesi genişler, adet azalır; düşük volatilite, stop daralır, adet artabilir: "Her işlemde, piyasa koşulları ne olursa olsun, hesabınızın yalnızca önceden belirlenmiş bir yüzdesini riske atın." ve "Amacımız, her işlemde aynı TL riskini korumaktır." (Ham). Volatilite ölçüsü ve pencere yok (ATR anılmaz); K1 formülüyle tutarlı. Parametre: risk / işlem = sermayenin %1'i (örnek) (Ham)
  - `tweet-garch-model-secim-aic-bic-ljung-box-1952739571466211673` — `tweet-garch-model-secim-aic-bic-ljung-box-1952739571466211673` (2025-08-05): GARCH model seçimi: "Daha düşük AIC/BIC → Daha iyi model" ve "Yüksek log-likelihood iyidir." (Ham). Kontrol önerisi: "Ljung-Box testi uygulanabilir." Sınır: "Bazen basit GARCH(1,1) yeterli ve stabildir."
  - `tweet-garch-risk-basina-getiri-secimi-1940666220354654588` — `tweet-garch-risk-basina-getiri-secimi-1940666220354654588` (2025-07-03): Risk başına getiri seçimi: "Ardından her hissenin ortalama getirisi ile ortalama tahmini volatilitesini karşılaştırırsınız." ve "Aynı getiriyi daha az oynaklıkla sunan hisse, finansal olarak daha verimli bir seçimdir." (Ham).
  - `tweet-garch-volatilite-kaliciligi-1899583516670611844` — `tweet-garch-volatilite-kaliciligi-1899583516670611844` (2025-03-11): Volatilite kalıcılığı örneği: "Şimdi yüksek beta ile BİST'de volatilitenin kalıcı olduğunu bir kere kabul edelim." (Ham). Okuma (YORUM): model katsayısı genel işlem eşiği olarak alınmaz.
  - `tweet-garch-volatilite-tahmini-1940416146601111638` — `tweet-garch-volatilite-tahmini-1940416146601111638` (2025-07-02): Volatiliteye göre boyut ayarı: "Örneğin, volatilite artıyorsa pozisyonlar azaltılır, düşüyorsa artırılır." (Ham).

## K7. Pozisyon büyüklüğü çarpanı: Tam / Defansif (SMRTG)

- Sahibi: B §8 (gp-48 görsel okuması, çarpan değerleri, serilerin kimliği, gözlem). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk yönünden okuma: Tansu'nun çarpan fikri vardır, hesaplanabilir tanımı yoktur; kural olarak uygulanamaz.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-fiyat-volatilite-birlikte-artis-defans-2053089712877797538` — `tweet-fiyat-volatilite-birlikte-artis-defans-2053089712877797538` (2026-05-09): SMRTG risk örneği: "sistemim pozisyonu kapatıp defansif pozisyoon aldı." ve "Fiyat ve volatilite aynı anda artması pek istenilen bir durum değildir sonu genelde kötü biter." (Ham).

## K8. Volatilite şok freni (yeni alım yok)

- Kaynak: T-volatilite-piyasa-soku-yeni-alim-freni (Ham; URL yok; Ham'da yazar yok).
- Tansu'nun fikri, oynaklık şokunda yeni alımı durdurup mevcut riski yönetmektir (Ham, tweet-volatilite-piyasa-soku-yeni-alim-freni:21); uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- Tanım: `oran = std(getiri, son X gün) / std(getiri, son ~21 gün)`. `oran ≥ eşik` ise şok. Şokta yeni giriş yok. (X, pencere, eşik hepsi YORUM; notta formül Claude'a ait.)
- Parametreler: X yok. "Bir ay" = ~21 işlem günü (YORUM). Eşik yok. Çıkış/bekleme süresi yok.
- Belirsiz kalanlar: Piyasa şoku endeks düzeyinde mi, hisse bazında mı (not ayırır, Tansu demedi). Kısa pencere aylık pencerenin içinde (örtüşme).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: İlke Ham'da. Parametre yok.
- Not: 05.10 ön denemesindeki "Piyasa Nabzı BEKLE günü yeni giriş yok" bu ilkeye benzerdi ama eşiği Tansu vermedi. Güncel karar: piyasa durumu girişi durdurmaz, yalnız etiket olarak gösterilir (TASARIM §3, §6; bilet 04, 14.10).

## K9. Fat tail, hayatta kalma

- Kaynak: T-fat-tail-firsat-survival-konvekslik (Ham), T-probabilistik-edge (Ham).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok): "Herkesin olduğu yerde para yoktur." "En büyük kârlar Fat Tails alanında yapılır" (George Soros'a atfedilmiş, doğrulanmadı). Zamanın %95'i normal, %5'i kriz/şok/aşırı ralli. Küçük yatırımcı şokta panikle satar, "Smart Money" fırsat görür. T-probabilistik: Algoritmik geliştiricinin en büyük tuzağı kesin yön tahmini ve klasik indikatör parametrelerini geçmişe uydurmak. Normal dağılım yerine fat tail, skewness, kurtosis. Monte Carlo ile risk of ruin ve güven aralığı.
- Tanım: Kural yok. Yalnız ilke. Parametre: "%95 / %5" anlatı sayısı, eşik değil (YORUM: sabit sayma).
- Belirsiz kalanlar: fırsat anlatısı işlem tetiği vermez; şok frenine istisna oluşturmaz. İki fikir arasında açık mantıksal çelişki kanıtlanmış değildir; strateji, zaman ve eylem açık değildir (Ham, tweet-fat-tail-firsat-survival-konvekslik:21 ve şok notu:21).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Kuyruk istatistikleri evet. Risk of ruin için işlem dizisi gerekir.
- Kaynak güveni: Düşük (anlatı). İşlem kuralı ve atıf doğrulanmış değildir.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-kayip-telafi-asimetrisi-1874416190443114907` — Kayıp-telafi asimetrisi: %10 kayıptan dönmek için %11 civarı kazanç gerekir, sermayeyi korumak önceliktir: "90 liranızı tekrar 100 lira yapmak için %11.12 kazanmanız lazım." (Ham). Parametre: örnek kayıp = %10, telafi getirisi = %11.12 (Ham; tam değer 1/0,9-1 = %11,11).
  - `tweet-butterfly-effect-early-signals-1914692264384774310` — Küçük olayların zincirleme fiyat etkisi tartışılır (22.04.2025, Ham): "Volatilite düşükse, ani sıçrama riskine karşı tetikte olun." Erken işaret: "Normalde birlikte hareket eden iki varlık ayrışmaya başlıyorsa, bir şeyler oluyor olabilir." Okuma (YORUM): İhtimal dili korunur; bu uyarılar otomatik giriş veya çıkış koşulu değildir.
  - `tweet-getiri-normal-dagilim-uyumu-1878081476161327393` — Okuma (YORUM): Dağılımın uç değerleri için risk uyarısı. Ham: "Marjinal değerler para kazandırır ama terste de bırakır."

## K10. Likidite ve kapasite kapısı

- Kaynak: T-likit-hisseler-etf-islem-derinligi-slippage-kapasite (Ham).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok): Trade'i ciddiye alan yeni yatırımcılar derinliği olmayan alanlar ve sığ hisseler yerine ETF'lere ve likit hisselere odaklanmalı. Gerekçe: istenen zamanda ve makul fiyatta girip çıkabilmek, sermayeyi düşük likiditede kilitlememek.
- Tanım: Eşik yok. Notun `quantity_liquidity` kuralı Claude'a ait (YORUM). Sektör rotasyonu bağlamında Tansu'nun hacim filtresi örnekleri: sahibi D, "Hacim filtresi". (bilet 04, 14.10)
- Parametreler: Yok (ADV, spread, katılım oranı verilmedi).
- Belirsiz kalanlar: "Likit" tanımı, hangi ETF'ler (BIST'te sınırlı).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Kısmen. Günlük hacim ve TL hacmi var. Spread ve derinlik yok (G-126 order book ayrı kaynak, kapsam dışı).
- Kaynak güveni: İlke (Ham).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-fon-konsantrasyon-para-cikisi-likidite-riski-2095997339391414488` — Geçmiş işlem hacmi likiditeyi tek başına ölçmez: hisse tabana kilitlenince satıcı var, alıcı yok. Taban/kilitlenme riski yüksek hisselerde pozisyon boyutu önceden azaltılmalı (fon yönetimi bağlamı, PUK örneği). "Likidite, iyi günde ne kadar hacim olduğu değil kötü günde ne kadar satış yapabildiğinizdir." (Ham)
  - `tweet-fon-likidasyon-stres-testi-2096208341374542257` — Fon alırken bakılacak ayrı süreç: hisse bazında marketability (taban-kilitlenme) risk skoru ve normal ile stresli likidasyon süresi. Tansu: "Ha açıkça ben bunlara çokdetaylı bakıyor muyum hayır." (Ham); görsel başlıkları "Marketability / Taban-Kilitlenme Risk Skoru" ve "Normal vs Stresli Likidasyon Süresi" (görsel metni). Eşik ve formül yok.
  - `tweet-fon-marketability-likidasyon-net-maruziyet-2097031747347030189` — Hisse bazında marketability tablosu: Taban Benzeri 10G, Ardışık Taban Benzeri, 5G/20G medyan hacim oranı, %20 katılımla normal ve stresli likidasyon günü, 0–100 skor ve risk sınıfı. "Normal koşullarda yüzde 20 piyasa katılımıyla pozisyonun boşaltılması yaklaşık 11 gün sürerken stres senaryosunda hesaplanan süre 222 güne kadar çıkıyor." (Ham) Parametre: piyasa katılım oranı = %20 (Ham); marketability skoru 100 = KRİTİK, 56–60 = YÜKSEK, 28–36 = ORTA (görsel, açıldı; sınır değerleri tablodan çıkarım, YORUM); 5G/20G hacim oranı BIGEN 0.14 (görsel, açıldı).
  - `tweet-hisse-fonu-risk-okuma-listesi-2097548996193526092` — Hisse senedi fonu risk okumasında pozisyonun piyasa likiditesi ölçülmeli; ölçü ileride eklenecek: "fon bu hisseyi ortalama piyasa hacmine göre kaç günde satabilir?" (Ham). Eşik yok. Notun geri kalanı fon analizi (akış, AUM, KAP/TEFAS, türev) ve hisse sinyali dışıdır.

---

# BÖLÜM 2. Kâr alma, çıkış, geçersizlik

## K11. Harmonik hedef merdiveni (BALAT, CD geri alımı)

- Sahibi: C §11 (kaynak G-109, TP merdiveni, doğrulama, parametreler, belirsizlikler). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: kısmi kâr, stop taşıma ve stop seçimi G-109 Ham'ında "genellikle" ve "örn." diliyle anlatılır; genel kural değildir (C §11). R/R eşiği K23'tedir.

## K12. Gartley takip tablosu: stop ve TP1/TP2 (G-123) ve SAYAS aracı

- Sahibi: C §7 (G-123 tablosu, SAYAS, iki ayrı TP1 tanımı, stop seçenekleri, SAYAS doğrulaması). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: tek genel TP1 ve tek genel stop seçimi yoktur (C §7); Gartley girişinin R/R eşiği C §7'dedir (K23 günlük işlem 5 kapısıdır).

## K13. Kırılım, FVG, retest, teyit kartı (AKFIS): ENTRY, STOP, TP1-3

- Sahibi: A §1 (görsel etiketleri, piksel okumaları, parametreler). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: stop ve TP kuralları tamamen belirsizdir (A §1).

## K14. Fincan-kulp hedef ve R/R (GUBRF)

- Sahibi: B §21 (görsel etiketleri, hedef formülü, R/R doğrulaması). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: hedef formülü vardır; giriş seviyesi (KIRILMA 300.75, gorsel-paket-58 Ham) vardır; stop yoktur (B §21).
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-fincan-kulp-kirilma-hedef-stop-1986946515508543529` — `tweet-fincan-kulp-kirilma-hedef-stop-1986946515508543529` (2025-11-07): Örnek hedef: "fincan derinliği kadar bir yükseliş beklentisiyle hesaplanmış" (Ham). Stop: "kulp seviyesinin altına, 10.41 fiyatına bir" (Ham). Okuma (YORUM): Ham örneği giriş 12.53 ve hedef 16.10 verir; bunlar genel eşik değildir.
  - `tweet-parabol-boyun-cizgisi-kirilim-hedef-stop-1953874288156594652` — `tweet-parabol-boyun-cizgisi-kirilim-hedef-stop-1953874288156594652` (2025-08-08): Ham: "fincan kulp vs vs". Açılan ADGYO görseli: "Neckline 35.78", "Entry ~ 35.78", "Target 44.84", "Stop 26.45", "ADGYO | R:R ≈ 0.97". Okuma (YORUM): parabol/boyun kırılımı örneğinin seviyeleridir; genel R/R kabul eşiği değiştirilmez.

## K15. Durum etiketleri ve geçersizlik (AKTİF, TAMAMLANDI, TEPKİ_VERDİ, BOZULDU, TAMAM, belirsiz)

- Sahipleri: C §2 (durum etiketleri ve anlamları), C §3 (AB=CD geçerlilik kuralları, BOZULDU kriteri), C §5 (SMRTG ve ISKPL sonuçları), C §10 (D sonrası tepki penceresi: 10 gün ve 20 bar). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: etiketler formasyon durumudur, işlem sonucu değildir; BOZULDU etiketinden işlem stop fiyatı çıkmaz.

## K16. Demand bölgesi geçersizliği (TTKOM)

- Sahibi: A §9 (zone_low kuralı, Close ve Low seçenekleri, parametreler); TTKOM alt tablosu A §6'dadır. Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: bozulma kuralı stop mantığına bağlanabilir; Tansu bir stop fiyatı vermez.

## K17. Retest bekle (AKSGY)

- Sahibi: A §12 (AKSGY başlığı, temas sayısı, Tansu'nun yorumu, parametreler). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: Tansu'nun fikri retest ve hacim teyidi aramaktır; çıkış için uygulanamaz, kaynak hesaplanabilir tanım vermiyor (Ham, G103:21).

---

# BÖLÜM 3. Süreç ve değerlendirme kuralları
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-dusen-trend-kirilim-pullback-onay-1949696229383770448` — Pullback taraması (28.07.2025): “İşte pullback taraması böyle yapılır” (Ham); “Düşen Trend Kırılımı + Pullback + Onay” (görsel metni). Okuma (YORUM): kırılımı pullback ve onay aşamaları izler.
  - `tweet-dusen-trend-kirilimi-pullback-1950609712287797598` — Düşen trend sonrası pullback tercihi (30.07.2025): “inanın bana en iyisi düşeni kıran.” ve “bir de pull back yaptıktan sonra yakalarsanız tamamdır” (Ham).

## K18. Backtest ile giriş sadeleştirme ve işlem günlüğü

- Kaynak: `not-backtest-giris-sadeligi-risk-islem-gunlugu.md` (URL var: x.com/The_Tansu_/status/2095213493133713664, 2 Eylül 2026; not, kaynağı doğrulandığını söyler). Görsel yok.
- Tansu'nun ifadesi (Ham, tweet metni birebir; aşağıda paraphrase):
  1. "Adayları geriye dönük izle": örnek: 26 Ağustos'ta seçilen hisselerin sonraki 1, 3 ve 5 gündeki sonuçlarını incele.
  2. Aday tiplerini karşılaştır: "Daily iyi + 4H bullish CHoCH + RS güçlü + Demand/FVG desteği" gerçekten kazandırıyor mu? Retest beklemek yarar sağlıyor mu, girişi fazla mı geciktiriyor?
  3. Girişi sadeleştir: Market Structure ve fiyat davranışı ana motor. RSI, MACD, WaveTrend ve RS yardımcı teyit. Tüm göstergelerin aynı anda yeşil olması gerekliliğini veriyle sorgula.
  4. Riski merkeze koy: setup ne kadar güzel olursa olsun tek işlemde büyük sermaye riske edilmez. Pozisyon büyüklüğü stop mesafesine göre. Belirli risk yüzdesi önerilmiyor.
  5. İşlem günlüğü: "Aday tarihi → giriş → neden girdik → invalidation → TP → sonuç → maksimum olumlu/olumsuz hareket" (MFE/MAE'ye denk; YORUM). Birkaç aylık kayıtla gerçek istatistik.
  6. Yalnız katkı sağlayanı tut: göstergeleri ve filtreleri sonuçlara katkısına göre ölç; katkısı olmayanı sadeleştirme adayı yap.
  - Ek paylaşım (`kaynak-tansu-2095201144544846208`, 2 Eylül 2026, 17:24 UTC, Ham): "Analize indikatörün AL sinyaliyle başlanmıyor." İnceleme sırası: bölge → kırılımlar → likidite hareketleri → 4 saatlik teyit.
- Tanım (bizim backtest için çıkan):
  1. Her aday için sinyal tarihi t0 kaydet. Sonuç: getiri(t0+1), (t0+3), (t0+5) işlem günü (gün tanımı belirsiz, aşağıda).
  2. Aday sonrası fiyat değişimi ile uygulanabilir giriş/çıkış sonucunu ayrı ölç (not, Cevo sentezi, YORUM).
  3. Her filtreyi tek tek çıkarıp (ablation) katkıyı ölç.
  4. Günlük alanları: aday_tarihi, giriş, gerekçe, invalidation, TP, sonuç, MFE, MAE.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| takip ufukları | 1, 3, 5 gün | Ham |
| gün = takvim mi, işlem günü mü | yok | YORUM (işlem günü) |
| günlük alanları | 8 alan (MFE ve MAE ayrı sayıldı; YORUM) | Ham |
| risk % | verilmedi | belirsiz |
| minimum örneklem | "birkaç ay" | Ham |
| maliyet varsayımı | yok | YORUM |

- Belirsiz kalanlar: Karar eşikleri ("katkı sağlıyor" ne demek). Retest beklenen süre. Giriş oluşmayan adayların sonucu (not: korunmalı, YORUM).
- Tansu'nun kanıtı: Yöntem önerisi. Sonuç yok.
- Bedava günlük veri: Evet (1/3/5 gün için). MFE/MAE günlük High/Low ile yaklaşık hesaplanır.
- Kaynak güveni: URL'li tweet (en güvenilir süreç kaynağı); metin Ham'da birebir. Orta-yüksek.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-ab-testi-iki-hisse-karsilastirma-1958791121686904877` — Okuma (YORUM): İki benzer hisseyi küçük eşit yatırımlarla karşılaştırma önerisidir. Ham: "Burada yatırımcı küçük bir portföy bölümüyle iki tarafa da eşit miktarda yatırım yapabilir." Ölçütler: "Getiri oranı, oynaklık, işlem hacmi, sektör karşılaştırması, bilanço açıklamalarına tepki gibi ölçütler seçilebilir."
  - `tweet-momentum-filtre-getiri-karsilastirma-1866225571761455225` — `tweet-momentum-filtre-getiri-karsilastirma-1866225571761455225` (2024-12-09, Ham): Ham: “Getiri grafiği hoşumuza giderse İlk grafikte optimizasyon da yaparak momentumu takip edebiliriz.” Okuma (YORUM): momentum trend takibi ve getiri karşılaştırması birlikte ele alınır.
  - `tweet-z-skor-cift-islem-backtest-2049220756781904348` — `tweet-z-skor-cift-islem-backtest-2049220756781904348` (2026-04-28). Çift işlem çıktısına eşlik eden uyarı: "Backteste bakınız, hayat kurtarır:)" (Ham). Okuma (YORUM): seçilmiş geçmiş sınama örneğidir.

## K19. Teknik indikatör ve sistem değerlendirme kriterleri

- Kaynak: `tweet-teknik-indikator-islem-sistemi-degerlendirme-kriterleri.md` (Ham; URL yok; Ham'da yazar yok).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok; "Dursun bir kenarda lazım olur" diye başlar):
  1. Kazanma oranı acemi yatırımcıların takıntısıdır, tek başına sistem kalitesini göstermez.
  2. Etkili bazı modeller haklı olduklarından daha sık yanılabilir; bazı marjinal modeller yanıldıklarından daha sık haklı çıkabilir. Kazanç/zarar asimetrisi açıklaması Ham'da yok.
  3. Temel performans ölçütü toplam net kârın maksimum sermaye erimesine oranıdır; kâr yüksek olsa da büyük erimeli model pratik değildir.
  4. Maksimum drawdown yalnız arka arkaya zararların toplamı değil, tüm equity curve'ün peak-to-trough kaybı.
  5. Kümülatif sermaye eğrisi büyük erimeleri ve pratik uygulanabilirliği görünür kılar.
  6. Erimeler diğer indikatörlerin erimeleriyle karşılaştırıldığında şiddetliyse sistem bir kenara bırakılmalı. "Aynı koşullarda" ve "uzun" Ham'da yok.
  7. Karmaşık metrikler basit equity-curve incelemesinin yerini almamalı.
  - Ham "net kâr / maksimum sermaye erimesi" oranına "ödül/risk oranı" der (Recovery Factor'a denk; YORUM).
- Tanım: Madde 2 ve 4 formülleri standart tanımdır (Ham'da formül yok; YORUM). `beklenti = kazanma_oranı × ort_kazanç − kayıp_oranı × ort_kayıp − maliyet`. `MDD = min(equity / running_peak − 1)`. `getiri/|MDD|`.
- Parametreler: Eşik yok (kaç MDD fazla? Tansu söylemedi).
- Belirsiz kalanlar: "Derin ve uzun erimeli" eşiği. Karşılaştırma ölçütü (Sharpe mı, equity mi).
- Tansu'nun kanıtı: Yok (ilke).
- Bedava günlük veri: Evet.
- Kaynak güveni: Ham; Ham'da yazar yok. Orta.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-backtest-asiri-uyum-kontrolu-1992410986989441388` — Aşırı uyum (overfitting) kontrolü: kazanan ve kaybeden işlem sayısı yaklaşık eşit olmalı; kazanma oranı %90 ve üstü şüpheli, %58 dengeli sayılır; kayıp işlemlerin büyüklüğüne ve R/R'ye bakılır. "Kar eden ve zarar eden işlem sayıları hemen hemen aynı olmalı ki overfitting tehlikesi ortadan kalkmış olsun" (Ham). Örnek GARAN: 31 işlem, 18 kâr, 13 zarar, %58,06, kümülatif %1153,73 (görsel, açıldı). Parametre: şüpheli kazanma oranı eşiği = %90 ve üzeri (Ham: "Eğer Kazanma Oranı 90% veya üzeri olsaydı"); örnek kazanma oranı = %58,06 = 18/31 (görsel, açıldı).
  - `tweet-gridsearch-profit-factor-3-bist-1908615000765190336` — Seçim eşiği olarak profit factor: gridsearch ile BIST'te profit factor 3'ün üstündeki hisseleri listeleyip onlarda işlem yapmak amaçlanmış. "gridsearch ile bist'te profit factor >3 olan hisseleri listeleyerek onlarda trade etmek" (Ham). YORUM: örneklem içi grid aramasıyla seçilen PF aşırı uyum riski taşır (bkz. K20). Parametre: profit factor eşiği = >3 (Ham).
  - `tweet-sharpe-orani-verimlilik-olcumu-1764308357639262709` — Sharpe oranı verimlilik ölçüsü olarak sunulur: (hisse getirisi − risksiz getiri) / hisse standart sapması; "yüksek sharpe ratio yakalamak için standart sapmanın düşük olduğu hisselerde trade yapmak önemlidir" (Ham). Eşik yok. K19 madde 7 (karmaşık metrik equity eğrisinin yerine geçmez) ile gerilim: Tansu Sharpe'ı önemli ölçüt sayar, yerine geçirmeyi söylemez (YORUM).
  - `tweet-alfa-beta-sharpe-birlikte-okuma-1943613913314017615` — Okuma (YORUM): Alfa, beta ve Sharpe birlikte değerlendirilir. Ham: "Dolayısıyla ideal senaryo, yüksek alfa – düşük beta dengesidir." Ek ölçüt: "O yüzden sadece alfa değil, alfa ile birlikte yüksek Sharpe oranı da önemlidir."
  - `tweet-alpha-sharpe-performans-olcumu-1914033217968996791` — Okuma (YORUM): Alfa endekse göre, Sharpe birim riske göre performansı okumak için kullanılır. Ham: "İdeal bir yatırım, pozitif alpha yaratmalı ve yüksek Sharpe Oranı ile bunu istikrarlı şekilde başarmalıdır." Sharpe formülü: "(Portföy Getirisi – Risksiz Getiri) / Volatilite".
  - `tweet-faz-hisse-sharpe-sortino-filtresi-1878409818358043106` — `tweet-faz-hisse-sharpe-sortino-filtresi-1878409818358043106` (2025-01-12; Ham): Faz hisselerinde risk başına getiri teyidi: "Her faz hissede, Sharpe ve sortino oranlarını alacaksınız artık." ve "Yani tüm şartları iyi görünen bir hissede yüksek Sharpe ve sortino yakalarsanız, mis:)" (Ham).
  - `tweet-getiri-dagilimi-iqr-aykiri-deger-1822549636013240372` — Okuma (YORUM): Yatırımcıya getiri dağılımı incelemesi önerilir. Ham: "Eğer day trader değilseniz, yatırımcı iseniz, senetlerin getiri dağılımına bakınız. Sıra dışı değerleri spot ediniz." Bu bir inceleme adımıdır.
  - `tweet-getiri-yogunluk-grafigi-volatilite-1822922559236555075` — Okuma (YORUM): Uzun vadeli yatırımda volatilite incelemesi. Ham: "Uzun vadeli değer yatırımcısının hisse volatilitesini mutlaka göz önünde tutması taraftarıyım".
  - `tweet-gunluk-getiri-dagilimi-grafik-kodu-1845204252421128436` — Okuma (YORUM): İşlem öncesi getiri dağılımı incelemesi. Ham: "En azından alacağınız hissenin günlük getirilerine şöyle bir bakın. Dağılımı görün."
  - `tweet-level1-dip-tepe-profit-factor-tarama-1908666927045886118` — Level 1 dip-tepe için çalışma notu: "Level 1 dip-tepe algoritmasında profit factor > 3 hisseleri bul" (Ham, 05.04.2025). Okuma (YORUM): devamında BIST dip sinyallerini listeleme, grafik ve PNL kontrolü istenir; PF > 3 bu algoritmaya ait seçimdir.
  - `tweet-normalize-getiri-ayni-sermaye-karsilastirma-1878078841471611279` — `tweet-normalize-getiri-ayni-sermaye-karsilastirma-1878078841471611279` (2025-01-11): Ham: "aynı başlangıç sermayesiyle yapılan yatırımlarda, yüzdesel olarak karşılaştıracağız." Okuma (YORUM): faz 1/2/3 hisseleri aynı başlangıç tarihi ve sermayesiyle normalize edilir.
  - `tweet-normalize-performans-karsilastirma-1878114420573749502` — `tweet-normalize-performans-karsilastirma-1878114420573749502` (2025-01-11): Ham: "başlangıç değerini 100 birim kabul ederek". Okuma (YORUM): banka hisseleri ve XU100 örneği, mutlak fiyat yerine ortak başlangıçlı yüzde performans karşılaştırmasını gösterir.
  - `tweet-portfoy-yonetimi-getiri-risk-temelleri-2099534451353006287` — `tweet-portfoy-yonetimi-getiri-risk-temelleri-2099534451353006287` (2026-09-14): Ham: "Portföyün yalnızca kazanç üretmesi yetmez, risksiz alternatife kıyasla aldığı ilave risk karşılığında yeterli ek getiri üretmesi gerekir." Okuma (YORUM): bileşik/yıllıklandırılmış ve reel getiri; volatilite, drawdown, benchmark ve varlıklar arası ilişkiler birlikte değerlendirilir. Ham: "Günlük getirilerin standart sapmasını hesapladıktan sonra bunu 252'nin karekökü ile çarparız."; "daha sonra Ticker.history() ile özellikle son tarihler için ikinci bir kontrol yapacağız." Okuma (YORUM): kaynak, download serisini history ile tarih bazında birleştirmeyi veri kalitesi adımı olarak anlatır; mevcut veri politikasına kendiliğinden aktarılmaz.
  - `tweet-risk-ayarli-performans-metrikleri-2096615408161759499` — - `tweet-risk-ayarli-performans-metrikleri-2096615408161759499` (2026-09-06; Ham): Riskle değerlendirme (Ham): "Bir yatırım çok kazandırmış olabilir ama önemli olan o kazancı ne kadar risk alarak yaptığıdır." "Sharpe ve Sortino buna bakar, Alpha piyasadan daha iyi olup olmadığını, Beta da piyasadan ne kadar etkilendiğini gösterir."
  - `tweet-risksiz-getiri-tahvil-yillik-volatilite-1878173923646349656` — - `tweet-risksiz-getiri-tahvil-yillik-volatilite-1878173923646349656` (2025-01-11; Ham): Ham: "risk primim 10 yıllık devlet tahvili faizi." Örnek veri dönemi: "işlem gören tüm günlük veriler üzerinden yapılıyor (2022-01-01'den 2025-01-10'a kadar)." Okuma (YORUM): günlük getirilerden yıllık volatilite hesaplama bağlamıdır; dönem kalıcı varsayılan değildir.
  - `tweet-risksiz-oran-10-yillik-tahvil-1913880746973946124` — - `tweet-risksiz-oran-10-yillik-tahvil-1913880746973946124` (2025-04-20; Ham): Risksiz oran (Ham): "Risk free rate olduğu işin 10 yıllık DT faizi kullanacaksınız." "Abd için ise bu oran 0.05 olur." Okuma (YORUM): ikinci sayı gönderi tarihindeki örnektir, kalıcı oran değildir.
  - `tweet-temettu-taramasi-sabit-buyume-riski-2089833787161039283` — Okuma (YORUM): Temettü taramasında sabit büyüme varsayımına uyarı. Ham: “sürdürülemez sabit büyüme varsayımını unutmayın.” ve “Döngüsel sektörlerde tek bir yılın yüksek temettüsü taranırsa, hisse 3 kat ucuz gibi görünür ama ertesi yıl temettü sıfıra inebilir.”

## K20. Probabilistik edge, fat tail, risk of ruin

- Kaynak: `tweet-probabilistik-edge-fat-tail-risk-of-ruin.md` (Ham).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok): Algoritma geliştiricilerin en büyük tuzağı fiyat yönünü kesin tahmin etmeye ve klasik indikatör parametrelerini geçmişe uydurmaya çalışmak. Gerçek edge: matematiksel modelleme, olasılık teorisi, beklenen değer ve işlem dizisi sonuçları. Normal dağılım yerine fat tail, skewness, kurtosis, black swan dayanıklılığı. Monte Carlo ile risk of ruin. İstatistiksel güven aralığı. Matematik non-random bileşenleri ayıklar.
- Tanım (kaynaktan): Ham klasik indikatör parametrelerinin optimizasyonunu "doğru yapılmaz ise" geçmiş verinin gürültüsünü mükemmelleştirmek sayar; koşullu uyarıdır, yasak değildir. Monte Carlo ile ruin olasılığı: işlem sonuç dağılımı (R katsayıları) yeniden örneklenir, belirlenen sermaye kaybı seviyesine ulaşma oranı hesaplanır (YORUM; Tansu yöntem vermedi).
- Parametreler: Ruin eşiği yok. Güven düzeyi yok (YORUM %95).
- Belirsiz kalanlar: Her şey sayısal.
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: İlke düzeyi. Notun plateau, nested walk-forward, deflated metrics önerileri Claude'a ait (YORUM).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-dip-taramasi-backtest-overfitting-1908882937325531171` — Tansu'nun kendi kabul ölçüsü: optimizasyondan sonra yaklaşık %50 win rate parametrelerini kullanır; "Ben matrixdeki robotlarımda da optimizasyon sonrası %50 winrate olan parametreler ile yol alırım." (Ham). ASELS dip taraması: 21 işlem, 9 kazanan, win rate %42,86, PF 1,64, max drawdown −13,74, Sharpe 0,22 (görsel, açıldı). Ham, 9/21'i overfitting olmadığının göstergesi sayar; bu sonuç tek hisse, tek dönemdir. Parametre: optimizasyon sonrası kabul edilen win rate ≈ %50 (Ham; Tansu'nun kendi robotları için ifade, eşik değil).
  - `tweet-kumarbaz-iflasi-olasilik-avantaji-1874240306461512014` — Kumarbaz iflası: kazanma ihtimali %49 ise parayı ikiye katlama ihtimali %1.80, %51 ise %98: "kazanma ihtimali %51 kaybetme ihtimali %49 ise paranızı x2 yapma ihtimaliniz %98" (Ham). Parametre: kazanma olasılığı 0,49 → x2 olasılığı %1.80; 0,51 → %98 (Ham); bahis birimi sayısı yazılmamış, hesap 100 birimde tutuyor: 1/(1+(0,51/0,49)^100) = %1,80 (YORUM, bizim hesabımız).
  - `tweet-rastgele-yuruyus-karekok-belirsizlik-1977458197158932959` — - `tweet-rastgele-yuruyus-karekok-belirsizlik-1977458197158932959` (2025-10-12; Ham): Risk ilkesi (Ham): "Stop loss kullanmak, portföyü çeşitlendirmek, pozisyon büyüklüğünü ayarlamak hep bu rastgelelikten korunmak içindir." Okuma (YORUM): rastgele yürüyüş eğitiminden risk yönetimi gerekçesi çıkarır; belirli bir stop değeri olarak kullanılmaz.

## K21. Python ile doğrulama ve yanlışlama; Williams %R sonucu

- Kaynak: `tweet-python-finans-fikir-dogrulama-ve-yanlislama.md`, `tweet-williams-r-sma-swing-strateji-backtest.md` (Ham).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok): "Finans piyasalarında Python kullanmasının ana nedeni fikirleri ve piyasa iddialarını test edebilmek." İndikatör tavsiyelerini doğrudan parayla denemek yerine matematiksel modele ve backteste çevirmek. pandas/NumPy, backtesting ve objektif karar mekanizması.
- Williams notu: Kurallar "Kullanıcı kuralları" olarak yazılı (30 dk, Williams %R 14, SMA 14, hedef ≥2R). Kaynak türü `user-provided-strategy-spec`. Sonuçlar bizim projemizin backtesti (Yahoo, ~60 gün): maliyetli long-only PF 0,988; iki yönlü (long + short) muhafazakâr maliyette PF 0,587, sıfır maliyette PF 0,830; short kolu için notta yalnız "PF<1" yazar. Bu bölüm Tansu'nun sonucu DEĞİL. Tansu kanıtı olarak kullanma.
- Tanım (Ham): varsayım → matematiksel model → geçmiş veriyle backtest → test başarısızsa kuraldan vazgeç. YORUM: bizim metot sırası fikir → denklem → nedensel sinyal → tarihsel simülasyon → maliyet/risk raporu → reddet veya sürdür; "nedensel sinyal" ve "maliyet raporu" Ham'da yok.
- Parametreler: Yok.
- Tansu'nun kanıtı: Yok (ilke).
- Kaynak güveni: Ham (Python notu). Williams sonuçları Tansu dışı.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-williams-r-macd-backtest-1845098408727461989` — Tansu'nun kendi Williams %R sonucu (K21'de şimdiye dek yalnız bizim backtestimiz var): BTC, W%R(14) ile MACD birlikte 100.000 $ için 3.546 $ (%3,5) kazandırdı, al-tut %42,64; yalnız %R: strateji %81, al-tut %85. "%R ile MACD, BTC'de felaket bir senaryo yarattı. Maalesef iyi çalışmadı." (Ham). Grafikler (görsel, açıldı): 2024-01–2024-10 üç sinyal (al ≈12.01, sat ≈26.01, al ≈28.08), strateji eğrisi ≈103.000, al-tut ≈142.000; yalnız %R grafiği 2023-11'den, başlangıç 1.000, strateji ≈1.800, al-tut ≈1.850. %R çizgileri −20 (SELL, aşırı alım) ve −80 (BUY, aşırı satım). MACD periyotları, MACD'nin rolü (YORUM: filtre), maliyet, kayma ve stop yok. Tansu kötü sonucu kendisi paylaşır (seçilmemiş olumsuz vaka). BTC kripto, BIST evreni dışı: kripto kapsamı, karar Levent'te bekliyor. Parametre: Williams %R periyodu = 14; aşırı alım çizgisi = −20; aşırı satım çizgisi = −80 (görsel, açıldı)
  - `tweet-williams-r-strateji-backtest-1844502539414511699` — Tansu'nun ikinci Williams %R sonucu: strateji eğrisi al-tuttan çok yüksek bitti. "Hayırlı uğurlu olsun:D" (Ham). Görsel (görsel, açıldı): başlık "No Strategy Gain vs WR Strategy Gain"; 2023-11–2024-10, başlangıç 1.000, WR stratejisi ≈2.750, strateji yok ≈1.330 (yaklaşık okuma); W%R çizgileri −20 ve −80; fiyat ≈1.800–4.000. Sembol yazılı değil (YORUM: fiyat yolundan ETH). Kripto, BIST dışı: kripto kapsamı, karar Levent'te bekliyor. Önceki BTC sonucuyla (MACD ile %3,5; yalnız %R %81 ve al-tut %85) birlikte karışık kanıttır; tek varlık, maliyet ve kayma yok, giriş-çıkış kuralı yazılı değil.
  - `tweet-derinlik-fiyat-korelasyon-analizi-1983480217894060348` — Derinlik varsayımını sınayan 28.10.2025 verili çalışma (29.10.2025): “EN ÖNEMLİ BULGU: İLİŞKİ ÇOK ZAYIF!” ve “Busebep ile kademe analizi büyük önem taşımaktadır.” (Ham). Okuma (YORUM): tek günün korelasyon sonucu genel bir fiyat tahmin kuralı olarak alınmaz.
  - `tweet-derinlik-fiyat-korelasyon-analizi-1983528060700778778` — Derinlik çalışmasının grafik açıklaması (29.10.2025): “Derinlik verisi tek başına güvenilir değil.” ve “Bir hissede çok alış lotu olması, o hissenin yükseleceği anlamına gelmiyor.” (Ham). Okuma (YORUM): 28 Ekim verisine ait bulgu, derinlikten kesin yön sonucu çıkarma varsayımını sınırlar.
  - `tweet-granger-nedensellik-test-kosullari-1922963356362703307` — Okuma (YORUM): Granger uygulaması için durağanlık ve gecikme seçimi önerilir. Ham: "Bu yüzden önce ADF testi ile serilerin durağan olup olmadığı kontrol edilmelidir." ve "AIC/BIC kriterleri ile belirlenebilir."
  - `tweet-marubozu-volatilite-bandi-taramasi-1843736658199622086` — Marubozu ve K Volatility kodu için uyarı: "Mutlaka göz ile kontrol edin mum boyları kişiselleştirilebilir. Ben kendime göre yazdım." (Ham, 08.10.2024). Okuma (YORUM): paylaşımın mum boyu ayarları evrensel formasyon standardı sayılmaz.

## K22. Süreç ilkeleri: kitap sentezi, algoritma tasarımı, kendini yenileyen sistem, kağıt-kalem, 116

- Kaynak: T-kitap-model-sentezi, T-algoritma-tasarimi-temelleri, T-kendini-yenileyen-algoritma-ana-frekans, T-kagit-kalem-matematik-once-kod-sonra (hepsi Ham), G-116 (`assets/gorsel-paket-116-veriden-sinyale-algo-sureci/01-veriden-sinyale-algoritmik-trader-gelistirme.jpg`).
- Tansu'nun ifadesi:
  - G-116 (NOTEBOOKLM görseli, birinci el, verbatim başlık): "Veriden Sinyale: Algoritmik Trader'ın Geliştirme Süreci". Dört adım: "1. Teknoloji ve Analitik Araçlar: Sürecin temeli Python ve veri analitiği araçları ile atılır." "2. Otomasyon ve Modelleme: Teknik analiz göstergeleri ve istatistiksel modeller Borsa İstanbul için otomatikleştirilir." "3. Geriye Dönük Test (Backtest): Geliştirilen sistemlerin başarısı geçmiş veriler üzerinde titizlikle test edilir." "4. Optimizasyon ve Sinyal Tasarımı: Risk/getiri oranı optimize edilmiş, kod tabanlı sinyal mekanizmaları tasarlanır."
  - T-kitap (Ham; Ham'da yazar yok): Kitaplar vizyon geliştirir, fakat hazır modelleri aynen uygulamak başarı getirmez. Başarı farklı kaynaklardan öğrenilen modelleri sentezlemek, sonra sabırla backtest ve forward test yürütmek. Bilgiyi işleme, modele dönüştürme ve kod mimarisi asıl ayırıcı.
  - T-algoritma (Ham; Ham'da yazar yok): Amaç açık olmalı. Zaman ve bellek verimli. İstatistik/ML doğru problemde. Backtest işlem maliyeti, piyasa likiditesi ve kaymayı simüle etmeli. Risk kontrolleri ve beklenmedik durum planları. Tasarım-test-iyileştirme sürekli döngü. İki satır kod "orta ve uzun vadede yıkıma sebep olabilir".
  - T-kendini-yenileyen (Ham; Ham'da yazar yok): Sistem her döngüde güçlenen, verinin ince katmanlarını işleyen olmalı; "ana frekans" araması; hata payını azaltan, kendini yenileyen matematiksel yapı.
  - T-kagit-kalem (Ham; Ham'da yazar yok; "Asla kalem kağıt kullanmadan sistem yazmam" der): Detaylı model varsa önce kâğıt üzerinde matematiksel çöz, sonra koda dök.
- Tanım: Kaynak sıraları: G-116 Python/analitik → otomasyon/modelleme → backtest → optimizasyon/sinyal tasarımı; T-kitap Ham'ı modelleri sentezle, sonra backtest ve forward test. YORUM: bizim süreç sırası veri → model (denklem) → backtest (maliyet+likidite dahil) → forward test → optimizasyon/sinyal tasarımı; forward testin optimizasyondan önce gelmesi hiçbir kaynakta yok.
- Parametreler: Yok. Forward test süresi yok.
- Belirsiz kalanlar: Forward test uzunluğu. "Ana frekans" bir yöntem mi, metafor mu belirsiz.
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: G-116 NOTEBOOKLM görseli (birinci el; genel). Notlar Ham. Kâğıt-kalem notu düşük.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-talep-bolgesinden-donus-2085813886062649480` — Okuma (YORUM): Arz-talep temelli sade analiz vurgusu. Ham: “Dediğim gibi herşey arz talep dostlar”, “Kafanızı yüzlerce indikatör ile yormayın” ve “Basit düşünün”.
  - `tweet-trend-takibi-tepe-dip-avlamama-2020521053739467058` — Okuma (YORUM): Trend takibinde uç noktayı yakalama iddiasından kaçınma. Ham: “Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR.” ve “akıntının (momentumun) yönünü tayin edip o dalgayı sürmeye odaklanmalısınız.”

## K23. Kesinlik dili, 5 kapı ve R/R eşiği

- Kaynak: T-piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi, T-yuksek-ihtimalli-gunluk-islem-bes-kapi (Ham).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok):
  - Kesinlik: "kesin gidecek/uçacak/tavan" söylemi kaçma sinyali; olasılık, risk-ödül, koşul ve invalidation dili profesyonel yaklaşım.
  - 5 kapı ve kabul eşiği örneği: sahibi B §20. (bilet 04, 14.10)
- Tanım: `R/R = (hedef − giriş) / (giriş − stop)`; eşik B §20'dedir.
- Parametreler: R/R eşiği ve beş kapının ölçüleri B §20'dedir.
- Sıra (Ham, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:49): Tansu stopu R/R oranına göre belirler: "Zarar Durdurma (Stop Loss) seviyenizi her zaman bu orana göre belirleyin." Uygun R/R sunmayan kurulum tercih edilmez (Ham, :48). Günlük işlem metni ile Gartley farklı bağlamlardır (Gartley'de R/R girişte stop X ile hesaplanır, eşik C §7; G123:42–49); bu sıranın bütün sistemler için Tansu kuralı olduğu söylenmemiştir, genel uygulanma kapsamı açık değildir.
- Tansu'nun kanıtı: YORUM (bizim hesabımız; STOP/TP etiketleri G-109 görselinde, D noktası piksel tahmini): G-109'un R/R'si ≈ 0,20-0,32 bu eşiğin altında kalır (C §11). Tansu bunu kendi paylaştığı çıktıda açıklamıyor.
- Bedava günlük veri: Evet.
- Kaynak güveni: Ham. Orta.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-cok-konusulan-hisseden-cikis-1790005102301823000` — Kesinlik dili kaçma sinyali ilkesine benzer bir ilke: enerji hisseleri örneğinde (13.05.2024) "Bir konu borsada çok dillendirilirse arkanıza bakmadan oradan kaçın." (Ham). Gerekçe: "Malı satacak adam arıyorlardır. Arz talep!" Ölçülür koşul, eşik ve çıkış zamanı yok.
  - `tweet-talep-bolgesi-risk-getiri-bakisi-2003179205014802645` — Okuma (YORUM): Talep bölgesindeki fırsat risk ve potansiyel getiriyle değerlendirilir. Ham: “Önemli olan talep bölgesinde yakalamak” ve “Alacağım riske bakarım bir de potansiyel getirisine.”

## K24. Başarı ölçütleri ve başarısızlık örnekleri: ML isabet, scorecard, stat-arb, 118

- Kaynak: T-ml-trade-13-gun-9-isabet (`assets/tweet-ml-trade-13-gun-9-isabet/01-ml-trade-hit-rate.png`), G-59 (`assets/gorsel-paket-59-risk-scorecard/01-buyhold-sinyal-stratejisi-risk-scorecard.png`), G-53 (`assets/gorsel-paket-53-stat-arb-bag-kopusu/01-statarb-negatif-backtest-bag-kopusu.jpg`), G-118 (`assets/gorsel-paket-118-yatirimci-basarisizlik-kontrol/01-yatirimcilar-neden-basarisiz-olur.jpg`).
- Tansu'nun ifadesi:
  - ML (Ham): ML ile trade yaklaşımını sevmediğini, modeli ara sıra incelediğini, finans için %70 doğruluğu yüksek gördüğünü belirtti. Görsel (BİRİNCİ EL, verbatim): "Toplam sinyal üretilen gün : 14; AL sinyali : 1; SAT sinyali : 13; Sonucu bilinen gün sayısı : 13; Tutarlı (Hit) : 9; Tutarsız (Miss) : 4; Tutarlılık Oranı (Hit Rate): 69.23%". 9/13 = 69,23% (doğrulandı). Wilson %95 aralığı ≈ 42-87% (benim hesabım, 13 örnek). 13/14 sinyal SAT: baz oran etkisi (piyasa düşüyorsa isabet modelden gelmez, YORUM).
  - G-59 (B&H ile sinyal bazlı strateji scorecard): sahibi D, "B&H vs sinyal bazlı strateji scorecard" bölümü. Burada tekrar edilmez. (bilet 04, 14.10)
  - G-53 (bağı kopan stat-arb çifti, negatif örnek): sahibi D, "Tansu'nun kanıtı" (AGROT/GARAN, madde c). Tansu'nun açıklaması (Ham, tırnaklı): "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım; görünmez bağ kopmuş olabilir."
  - G-118 (NOTEBOOKLM görseli, birinci el, verbatim): "Yatırımcılar Neden Başarısız Olur?" Üç aile, dokuz madde: Bilgi ve Hazırlık Eksikliği (Ticaret Planının Olmaması: "Sağlam bir metodoloji olmadan, anlık kararlarla işlem yaparlar."; Yetersiz Bilgi; Uzman Desteği Aramamak). Disiplin ve Psikoloji (Duygusal Kararlar; Hatalardan Ders Almamak; Plana Sadık Kalmamak). Sermaye ve Risk Yönetimi Zafiyeti (Yetersiz Sermaye: "Küçük sermaye genellikle para kaybeder ve kaldıraç riskini anlamazlar."; Zayıf Para Yönetimi; "'Zarar Durdur' Emri Kullanmamak: Bu, küçük bir kaybı büyük bir kayba dönüştürmenin bir numaralı yoludur.").
- Tanım: Sonuç raporunda isabet, sinyal dağılımı, örneklem büyüklüğü ve baz oran birlikte raporlanır. Strateji, B&H ile risk ve çekilme bazında kıyaslanır. Negatif sonuç saklanmaz.
- Parametreler: ML için eşik %70 "yüksek" (Tansu'nun yargısı, Ham). Başka eşik yok.
- Belirsiz kalanlar: G-59'da dönem, rf, işlem maliyeti, strateji kuralı, zaman-piyasada oranı yok. ML'de label tanımı ve dönem yok.
- Tansu'nun kanıtı: Küçük örneklem (13), seçilmiş pencere (G-53, G-59).
- Lojistik regresyon filtresi ve R/R koşulu (`gorsel-paket-129-doas-lojistik-regresyon-hacim-rsi-filtreli-strateji`; Ham Tansu'nun metni, görsel birinci el; bilet 04, 14.10): hacim ve RSI verisiyle lojistik regresyon modeli; doğruluk %55,00, kesinlik %55,31, duyarlılık %45,44; Tansu: finansal piyasada %70 harika, %90 mümkün değil; modeli "yeni yazılmış, üzerinde hiç çalışılmamış" diye anlatır. Kural cümlesi (birebir): "%55 başarı oranıyla para kazanmak için, her işlemde Risk/Ödül oranını en az 1:1.5 (örneğin %2 Stop, %3 Kar Al) olarak ayarlamak gerekir." Görsel: `DOAS.IS - ML + Hacim + RSI Filtreli Strateji`; EMA 21, RSI paneli (30, 70 çizgileri, "Trend Ayrımı (50)"), "SAT" ve "Güçlü AL (Vol+RSI)" işaretleri; doğruluk sayıları görselde yok, özellik ve hedef değişken tanımı yok, örneklem dışı doğrulama yok. R/R ≥ 1:1,5 eşiği K23'teki 1:2 veya 1:3 eşiğinden farklıdır; bağlamlar ayrı (K23 günlük işlem 5 kapısı, bu not ML isabet oranı); çözülmedi, K23 değişmedi.
- Bedava günlük veri: Evet.
- Kaynak güveni: G-118 NOTEBOOKLM görseli (birinci el); diğer görseller ve Ham BİRİNCİ EL (yüksek). Wilson aralığı ve baz oran yorumları bizim hesabımızdır (YORUM).
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-hata-metrigi-model-secimi-1795910557695877254` — Okuma (YORUM): Paylaşılan araştırmanın model seçim ölçütü işlem sistemi kârlılığıyla aynı ölçüt değildir. Ham: "Bildiğiniz üzere en iyi model, hata metriklerinin (MAE, MSE, RMSE) minimum olduğu modele göre belirlenir." (29.05.2024). SSE Composite ve CSI 300 araştırması bağlamı korunur.
  - `tweet-indikator-durumu-ikili-ozellik-1860463695790305656` — Okuma (YORUM): Model girdilerinin anlamına açıklık getiren kaynak. Ham: "Bağımsız değişkenler, fiyatın teknik göstergelere göre durumlarıdır. 0 ve 1 değerleri, strateji koşullarına göre belirlenmiştir." (23.11.2024).
  - `tweet-knn-yukselis-dusus-siniflama-1864342754844660140` — Okuma (YORUM): Sınıflandırma hedefi ve mesafe ölçüsü açıklanır. Ham: "Bağımlı değişkenim yükselecek ya da düşecek" ve "Öklid uzaklığı ile mesafeleri ölçüp sınıflandırıyorum." (04.12.2024). Bunlar doğruluk veya kârlılık kanıtı değildir.
  - `tweet-winrate-80-tarama-backtest-tablosu-2092745592661246196` — `tweet-winrate-80-tarama-backtest-tablosu-2092745592661246196` (2026-08-26). Deneysel tarama filtresi: "Winrate %80'den büyük olanları tarattım" (Ham). Sinyal yaşı ve yapı teyidi: "Diğer hisselerin al sinyalleri çoktan gelmiş, risk almayalım." ve "Bu sistemi talep toplama bölgesi gibi analizlerle beraber kullanırız" (Ham).

## K25. ATR basamak merdiveni: kademeli kâr alma ve yalnız yukarı giden stop (1–5 ATR)

- Kaynak: `tweet-atr-iz-suren-stop-tablosu-2045421697814126693` (Ham + görsel, açıldı), `tweet-atr-kademeli-iz-suren-stop-kar-al-2020671177329352789` (Ham + görsel, açıldı), `tweet-atr-ile-kar-alma-seviyeleri-2049076484371804271` (Ham), `tweet-13-ema-3atr-spike-kar-al-1963273280581751113` (Ham). Dördü Tansu'nun X gönderisidir (birinci el). K4 ve K5 ayrı yöntemlerdir (giriş + 1,5 ATR aktivasyonu, önceki gün dibi altı kapanış); bu bölüm onları değiştirmez.
- Tansu'nun ifadesi (verbatim):
  - Görsel, YAPRK tablosu (görsel, açıldı): "Stop her zaman YUKARI hareket eder, aşağı inmez"; "3 ATR'ye ulaşınca %50 satış yapın"; "Yarın fiyat 3 ATR seviyesine ulaşırsa → Stop'u 1 ATR seviyesine çekin + %50 satış". Gönderi metni (Ham, 2026-04-18): "herkese tüm hisseleri nerede satması gerektiğini de veriyorum. sat tuşuna da benim basmamı kimse beklemesin."
  - Ham (2026-04-28): "O yüzden art ile her hissede kar alacağın seviyeleri veriyorum. Satarsın satmazsın sana kalmış." ("art" yazım hatası; YORUM: ATR demek istiyor.)
  - Ham (2026-02-09): "Stop yamulana kadar kar alıyoruz:)" ve "Gruba verilecek iz süren kar al ve stop sistemi."
  - Ham (2025-09-03): "Bu seviyeler kâr almayı düşünmek için uygun bölgeler olabilir. Kademeli satış, riski azaltır." ve "3 ATR’den sonra hemen alım yapmak genellikle dezavantajlıdır."
- Tanım (görsel tablosundan; örnek YAPRK, giriş 2026-03-16, giriş fiyatı 15.05 TL, ATR(14) 1.27 TL):
  1. Giriş günü başlangıç stop 13.15 TL, başlangıç risk %12.62. Hesap: 15.05 − 13.15 = 1.90, bu da yaklaşık 1.5 × 1.27. YORUM: başlangıç stop = giriş − 1.5 ATR; görsel formül yazmaz. K2'deki 2 ATR acil stop ile farklıdır; çelişki çözülmedi.
  2. Seviye n (n = 1…5): hedef fiyat = giriş + n × ATR (16.32; 17.58; 18.85; 20.12; 21.38). ATR giriş gününün tek değeridir, tabloda sabit.
  3. Fiyat n ATR seviyesine ulaşınca stop yukarı çekilir. n=1: stop değişmez (13.15, "Başlangıç"). n=2: stop = GİRİŞ (15.05). n≥3: stop = (n−2) ATR seviyesi (3 ATR → 16.32; 4 ATR → 17.58; 5 ATR → 18.85).
  4. Stop yalnız yukarı gider, aşağı inmez.
  5. 3 ATR seviyesinde pozisyonun %50'si satılır (tabloda "%50 SATIŞ"). Satılan oranın neye göre %50 olduğu yazılı değil.
  6. "Risk %" sütunu (hedef fiyat − stop) / hedef fiyat gibi okunur (hesap: 1 ATR için (16.32 − 13.15) / 16.32 = %19.4, görsel %19.41) (YORUM).
  7. Günlük kayıt (`tweet-atr-kademeli-iz-suren-stop-kar-al-2020671177329352789`, görsel, açıldı; hisse adı yok): satırlar "n ATR - tarih", "Hedef", "Fiyat", "Stop". Giriş fiyatı yazılı değil; YORUM: giriş 143.00 TL ve ATR adımı yaklaşık 4.39 TL (hesap: 154.70 / 1.0818 = 143.00; 147.39 − 143.00 = 4.39). 1 ATR (2025-06-30) stop 143.00; 2 ATR (2025-07-01) stop 147.39; 3 ATR (2025-07-02) stop 147.39 ve "%50 SATIŞ YAPILDI"; 4 ATR stop 151.79; 5 ATR stop 156.18; … 10 ATR (2025-08-22) stop 178.14; "STOP ÇARPILDI - 2025-09-02", "Sonuç: %24.58" (hesap: 178.14 / 143.00 − 1 = %24.6; YORUM: bu, kalan pozisyonun getirisidir; %50 satışla birleşik değildir).
  8. Kayıt ile tablo iki yerde ayrışır: (a) n=2 adımında kayıtta stop 147.39 (1 ATR seviyesi; etiket "0 ATR"), tabloda GİRİŞ (0 ATR); (b) n=1 adımında kayıtta stop 143.00 (YORUM: giriş fiyatı; etiket "-1 ATR"), tabloda başlangıç stop (giriş − 1.5 ATR, YORUM). n≥3 için ikisi aynıdır: stop (n−2) ATR seviyesi.
  9. 13 EMA yazısı (`tweet-13-ema-3atr-spike-kar-al-1963273280581751113`, Ham): fiyat 13 EMA üzerinde kalıp 1 ATR, sonra 2 ATR'ye kademeli ilerlerse sağlıklıdır. Bir anda 3 ATR'ye fırlama ya da 3 ATR üzerine iğne bırakma (spike) risktir. Pozisyonu olan için 3 ATR kâr alma bölgesidir ve satış kademelidir. Yeni pozisyon için 3 ATR'den sonra hemen alınmaz; geri çekilme ya da yeni denge beklenir. Spike sonrası 13 EMA civarında tutunma trend devamına, EMA altına sert dönüş tepe sinyaline işaret eder. 3 ATR'nin neye göre ölçüldüğü (giriş mi, EMA13 mü) yazılı değil.
  10. `tweet-atr-ile-kar-alma-seviyeleri-2049076484371804271`: Tansu her hisse için ATR ile kâr alma seviyelerini verir; satış kararı okura aittir. Çarpan ve koşul yazılı değil; YORUM: seviyeler bu tablodaki gibi n × ATR basamaklarıdır.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| ATR periyodu | 14 | görsel, açıldı ("ATR (14)") |
| seviye adımı | 1 ATR (hedef = giriş + n × ATR) | görsel, açıldı |
| başlangıç stop | giriş − 1.5 ATR (hesap) | YORUM |
| stop yükseltme | n=1 değişmez; n=2 giriş; n≥3 (n−2) ATR seviyesi | görsel, açıldı |
| kısmi satış | 3 ATR'de %50 | görsel, açıldı |
| stop yönü | yalnız yukarı | görsel, açıldı |
| 3 ATR ölçü referansı (13 EMA yazısı) | yok | YORUM (EMA13 ya da giriş) |

- Belirsiz kalanlar: Stopun tetik tabanı (gün içi Low mu, kapanış mı). "Seviyeye ulaştı" ölçüsü (High mı, kapanış mı). Giriş fiyatının kapanış olup olmadığı. %50 satıştan sonra kalan miktar için ek satış (6 ATR ve üstü) yok. ATR giriş değerinde sabit mi kalır (tabloda tek ATR var; günlük güncelleme yok). Başlangıç stopun gerçekten 1.5 ATR olup olmadığı. n=1 ve n=2 adımlarında kayıt ile tablo farkı. 13 EMA yazısı ile tablonun ilişkisi.
- Tansu'nun kanıtı: Günlük kayıt tek hisse, geriye dönük, seçilmiş örnektir (çıkış %24.58; %50 satışın toplam getiriye etkisi yazılmaz). YAPRK tablosu yalnız giriş günü planıdır; sonuç yok. Backtest yok.
- Bedava günlük veri: Evet. Günlük OHLC ve ATR(14) yeter. Seviye için High, stop için Low kullanmak YORUM'dur.
- Kaynak güveni: Orta-yüksek. Tablo kuralları görselde net ve birinci eldir. Başlangıç stop formülü ve n=1, n=2 farkı YORUM'dur. 13 EMA yazısı kavramsaldır, sayı vermez. Hazırlık K.
- Modül 1 çıkış paketi: KURALLAR §3.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-sabit-atr-kar-alma-iz-suren-stop-2022431570012106899` — ASTOR tablosu K25 merdivenini 1–20 ATR'ye uzatır (giriş 2026-02-03, 155.00 TL, ATR(14) 7.56 TL, başlangıç stop 143.66 = giriş − 1,5×ATR, hesap: 11.34); stop n ATR'de (n−2) ATR seviyesine çıkar; 3 ATR'de (2026-02-12, 183.40) stop 162.56 ve %50 satış, 4 ATR'de stop 170.11, durum AÇIK (%50) (görsel, açıldı). "Listelerde uygulanacak stop ve kar alma sistemi." (Ham). Başlangıç stop 1,5 ATR (hesap) ile K2'nin 2 ATR acil stopu: karar Levent'te bekliyor. Parametre: seviye sayısı = 1–20 ATR (görsel, açıldı); stop (n−2) ATR seviyesi, n=20 için 18 ATR (görsel, açıldı)
  - `tweet-sabit-atr-kar-alma-iz-suren-stop-2022434791292080331` — Tekrar: GZNMI için aynı 1–20 ATR tablosu (giriş 2026-02-12, 56.15 TL, ATR(14) 2.85 TL, başlangıç stop 51.88 = giriş − 1,5×ATR, hesap: 4.27 ≈ 4.275); 1 ATR 2026-02-13'te ulaşıldı (61.75), stop aynı, durum AÇIK (%100) (görsel, açıldı). Ham metin yok; alıntılanan gönderi: "Tavan İkna olduk mu" (Ham). Başlangıç stop 1,5 ATR ile K2 2 ATR: karar Levent'te bekliyor.
  - `tweet-ema13-tepki-2atr-macd-histo-egimi-1957860013008990268` — 13 EMA ve ATR birlikte (XU100, 19.08.2025): "13 günlük ortalamadan tepki alıyoruz, 2ATR üzerinde kapatıyoruz, macd histo eğimi de artıyor neg. bölgede." (Ham). İlk hedef söylenmez ("hedef kouşmam"). 2 ATR'nin neye göre ölçüldüğü yok (K25 madde 9 ile aynı belirsizlik); K25 başlangıç stop ~1,5 ATR ile K2 2 ATR sorusu karar Levent'te bekliyor, bu not bir stop değildir. MACD histogram eğimi için B §17. Parametre: Tepki ortalaması = EMA13; kapanış eşiği = 2 ATR üzerinde (ölçü tabanı yok) (Ham); grafikte EMA26 kanalı ±%6,8 (XU100; ATR ile ilişkisi yazılı değil, YORUM: 2 ATR bandı olabilir) (görsel, açıldı)

## K26. Fon çıkışı kaynaklı satış baskısı: likidasyon günü stres testi ve net maruziyet (hisse dışı fon analizi; kapsam kararı Levent'te bekliyor)

- Kaynak: Yedisi Ham (Tansu'nun X gönderileri, 04–15.09.2026): `tweet-fon-cikis-stres-testi-satis-gunu-2095983340142882886` (görsel G1 ve G2 açıldı), `tweet-brut-net-hisse-viop-hedge-beta-ayarli-2097068834284863827`, `tweet-brut-hisse-viop-hedge-net-maruziyet-2097395059641679900`, `tweet-fon-akis-yogunlasma-agirlik-rotasyonu-2097427778232529261`, `tweet-fon-erken-uyari-yapisal-risk-aktivasyon-2099594176606187548`, `tweet-fon-cikisi-ters-repo-karsi-taraf-2099913462034088091`, `tweet-fon-cikis-hizi-short-kapama-kurali-2099967840405086603`.
- Kapsam (YORUM, 16.10; karar Levent'te bekliyor): Yatırım fonu BIST hissesi değildir; TASARIM §3 evreni BIST100 benzeri hisselerdir ve fonu anmaz. Bu bölüm kaynak kaydıdır. Hisse tarafındaki 20 günlük medyan TL hacim fikri E K10'a bağlanır.
- Tansu'nun ifadesi (verbatim):
  - Stres testi (04.09.2026, THF): "THF’den %10 büyüklüğünde bir para çıkışı olduğunu ve fonun her hissede günlük işlem hacminin en fazla %20’sine katılarak satış yaptığını varsaydığımızda en yüksek satış yükü TRHOL’de oluşuyor, yaklaşık 7,2 işlem günü." "Asıl denklem: Pozisyon büyüklüğü / piyasa likiditesi." "Bu çalışma hisse yönü tahmini değil büyük fon çıkışlarında hangi tahtaların satış baskısına daha hassas olabileceğini ölçen bir stres testidir." Aynı gönderide: güçlü para girişi sürdüğü için bunları "yakın vadeli satış sinyali olarak görmüyorum"; akış negatife dönerse TRHOL, BIGEN, ANELE ve KARCL "ilk takip edeceğim likidite riskleri".
  - Çıkış hızı ve short (15.09.2026): "Fon çıkışı var → hangi hisseler ağır basıyorsa teorik satış baskısı oralarda daha yüksek." "Çıkış hızı azalıyor → bu baskının şiddeti de zamanla azalabilir." "Short pozisyon varsa → fon pozisyon küçültürken burada satış değil, teorik olarak short kapama kaynaklı alım tarafı oluşabilir." Örnek: DSTKF, TLY.
  - Net maruziyet (07–08.09.2026): "brüt hisse oranı ile net piyasa riski aynı şey değil". THF örnekleri: brüt hisse ≈%84,6, VİOP short/NAV ≈%20,4, net hisse ≈%64,2, beta ayarlı net piyasa riski ≈%38; diğer gönderide brüt ≈%97,8, net ≈%63. "Üstelik TEFAS ve KAP verilerinin tarihleri farklı olabildiği için bunlar yaklaşık ölçümlerdir." "Brüt pozisyona değil VİOP hedge’ine, net exposure’a, beta ayarlı riske, likiditeye ve portföy yoğunlaşmasına birlikte bakmak gerekiyor."
  - Erken uyarı (14.09.2026, THF): "Mavi sütun Yapısal Risk", "Turuncu sütun Aktivasyon", "Yeşil çizgi ise Erken Uyarı Skoru; yapısal risk ile aktivasyonun birleşik sonucudur." "Yeşil = aktif satış baskısı yok, Sarı = stres sinyalleri oluşmaya başladı, yakın takip, Kırmızı = para çıkışı, AUM düşüşü, pozisyon azaltımı ve fiyat-hacim bozulması gibi birden fazla teyit aynı anda devreye girmiş olabilir." Sınıflama: "Aktif zorunlu satış riski: DÜŞÜK", "Yapısal likidite riski: YÜKSEK", "Konsantrasyon riski: ORTA", "Piyasa yön riski: hedge nedeniyle ORTA", "Genel durum: ŞİMDİLİK SAĞLIKLI, AMA PARA AKIŞINA ÇOK DUYARLI".
  - Para akışı ve ters repo (15.09.2026, TP2): "Benim açımdan bu bir kriz sinyali değil, güçlü bir erken uyarı sinyali." Tek günlük 16,27 milyar TL çıkış; fon büyüklüğü ≈259 → 243 milyar TL (≈%6,3); 3.803 yatırımcı. Takip: karşı taraf yoğunlaşması, teminat kalitesi ve çıkışların birkaç gün devam edip etmediği. "Tek başına ters repo yüksekliği sorun değil önemli olan ters reponun kimle ve hangi teminatla yapıldığı."
  - Para girişi ve yoğunlaşma (08.09.2026, TMV): son 5 günde yaklaşık 2,28 milyar TL, son 20 günde 5,02 milyar TL tahmini net giriş; ilk 5 hisse ≈%56,5 (OZATD %12,89, ANELE %12,17, TRHOL %11,28, SELEC %10,16, BIGEN %9,97). Bu yapı "belirgin bir zorunlu satış baskısı olmadığını düşündürüyor".
- Tanım (Ham; formüller YORUM, görsel sütunlarından geri çıkarıldı):
  1. Stres testi: her hisse için pozisyon TL (fon ağırlığı × fon değeri), 20 günlük medyan TL hacim, çıkış oranı c (%5, %10), piyasa katılımı k (%10, %20, %30). Likidasyon günü (tam tasfiye) = pozisyon / (k × medyan hacim). Çıkış stresi günü = çıkış satış TL / (k × medyan hacim). Doğrulama (görsel, açıldı): TRHOL pozisyon ₺4,89 Mr, medyan ₺378,78 Mn, oran 12,92, %10 / %20 / %30 katılımda 129,15 / 64,58 / 43,05 gün; %10 çıkışta satış ₺546,87 Mn, %20 katılımda 7,22 gün (546,87 / (0,20 × 378,78) = 7,22). Satış TL pozisyonun tam %10'u değildir (TRHOL ≈%11,2; tüm satırlarda ≈%11,2); katsayının kaynağı görselde yok (YORUM: 0,10 / ≈0,894).
  2. Likidite Skoru (YORUM, görselden geri çıkarıldı): min(100, 50 × Pozisyon / Medyan Hacim). Kontrol (görsel, açıldı): GIPTA oran 1,51 → 75,72; KORDS 0,97 → 48,28; AKSEN 0,37 → 18,51; EFOR 0,32 → 16,04.
  3. Likidite Riski sınıfı: KRİTİK, YÜKSEK, ORTA, DÜŞÜK. Görünen sınırlar (YORUM): DÜŞÜK en çok skor 18,51; ORTA 20,45–48,28; YÜKSEK 61,70–75,72; KRİTİK skor 100 (en düşük KRİTİK oran 2,67). Kesin eşik görselde yok.
  4. Net maruziyet: net hisse = brüt hisse oranı − VİOP short notional / NAV (Ham: "basit hesap"; THF 14.09: %77,82 − %13,35 = %64,47). Beta ayarlı net piyasa riski formülü verilmedi (THF 14.09: ≈%40,15; YORUM: Σ beta × ağırlık − short notional).
  5. Erken Uyarı Skoru = Yapısal Risk (ağırlık, likidite, kriz anında satılabilirlik) ile Aktivasyon (5 ve 20 günlük para akışı, AUM'daki gerileme, KAP'taki pozisyon değişimi, fiyat-hacim davranışı) birleşimi. Birleşim formülü ve ağırlıklar verilmedi. Okuma (Ham): mavi yüksek ve turuncu düşük = yapısal kırılgan ama aktif baskı yok; turuncu yükseliyor = stres; ikisi birden yüksek = teorik risk fiili baskıya dönmeye başlamış olabilir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| çıkış stresi oranı c | %10 (görselde %5 ve %10) | Ham; görsel (açıldı) |
| piyasa katılımı k | ana senaryo %20; tabloda %10, %20, %30 | Ham; görsel (açıldı) |
| hacim penceresi | 20 gün medyan TL hacim | görsel (açıldı) |
| likidite skoru | min(100, 50 × oran) | YORUM |
| risk sınıfı eşikleri | kesin değer yok (sınır aralıkları yukarıda) | YORUM |
| akış penceresi | 5 ve 20 gün | Ham |
| erken uyarı skoru formülü ve renk eşikleri | yok | belirsiz |
| ters repo / karşı taraf eşiği | yok | belirsiz |

- Belirsiz kalanlar: Satış TL katsayısı (≈%11,2). Skor sınıf eşikleri. Aktivasyon ve Erken Uyarı Skoru formülü, ağırlıkları ve renk eşikleri. Beta ayarlı net risk formülü ve beta penceresi. Sinyal olarak kullanım: Tansu bunu "hisse yönü tahmini değil" stres testi olarak tanımlar ve yakın vadeli satış sinyali saymaz. Planlanan model (geçmiş KAP raporlarıyla test, "güven skoru") henüz yapılmamıştır (Ham, 15.09.2026).
- Tansu'nun kanıtı: Yalnız THF (04.09 ve 14.09), TMV, TP2 anlık tabloları. Geriye dönük test, isabet oranı ve sonuç yok. Rakamlar farklı tarihli TEFAS ve KAP verisine dayanır (Ham: yaklaşık).
- Bedava günlük veri: Hayır, kısmen. Hisse tarafı (20 günlük medyan TL hacim) günlük veriyle hesaplanır. Fon ağırlıkları, para akışı, AUM, VİOP short notional TEFAS ve KAP verisi ister; TASARIM'da bu veri yok ve KAP portföyü gecikmelidir (Ham: KAP hedge verisi 08/2026, TEFAS 14.09.2026).
- Kaynak güveni: Ham (birinci el). Orta: stres testi tablosu görselle doğrulandı; erken uyarı ve net risk ölçüleri yöntem belirtmeden anlatılmış. Hazırlık K (stres testi tablosu hesaplanabilir; kapsam kararı bekliyor).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ortak-hisse-zorunlu-satis-riski-2096698351781884285` — Ortak hisse yolu: TLY ve TMV satış yaparsa THF ile ortak, likiditesi zayıf hisselerde baskı oluşur: "Asıl kritik nokta ortak hisselerin büyüklüğü ve günlük hacme göre satışın ne kadar ağır kalacağı." (Ham). Eşik yok; fon analizi kapsamı: karar Levent'te bekliyor.
  - `tweet-pozisyon-medyan-hacim-tasfiye-suresi-2096187367778370014` — Likidasyon ölçüsü: "pozisyon büyüklüğünü hissenin 20 günlük medyan TL işlem hacmine oranlayıp, farklı piyasa katılım oranlarında teorik tasfiye süresini hesaplıyoruz" (Ham). Geçmiş hacim taban ve stres günlerinde yanıltır; spread, derinlik ve fiyat aralığındaki alış/satış miktarı eklenmeli (Ham). Fon analizi kapsamı: karar Levent'te bekliyor.
  - `tweet-ppf-secim-likidite-karsi-taraf-cesitlendirme-2099814980212134159` — Para piyasası fonu seçimi: tek ters repoya, tek pay senedi teminatına veya tek karşı tarafa yüklenmeyen, likit, kamu kâğıdı tamponlu fon; hızlı para çıkışı zorunlu satış yaratır: "Aynı getiriyi hangisi daha temiz ve daha düşük yapısal riskle üretiyor sorusunu soralım." (Ham). Eşik yok; Tansu metni "ChatGPT dilinde" diye anar; fon analizi kapsamı: karar Levent'te bekliyor.
  - `tweet-viop-hedge-net-beta-maruziyeti-2096700133731643859` — THF net maruziyet örneği, 06.09.2026 (K26 net maruziyet maddesiyle aynı yöntem): "Kağıt üzerinde %88 hisse taşımasına rağmen VİOP short pozisyonları sonrası net hisse maruziyeti yaklaşık %65." (Ham). Portföyün yaklaşık %47'si 9 hissede; beta etkisiyle net piyasa yön riski yaklaşık %38 (Ham). Görsel (görsel, açıldı): brüt hisse %88,23; VİOP short/NAV %22,79; basit hedge oranı %25,84; net hisse %65,44; portföy beta 0,70; beta ayarlı hedge %38,19; net beta maruziyeti %38,07; veri güveni ORTA. KAP türev tablosu (görsel metni): 36 satır, 35 SHORT ve 1 LONG (F_SASA0926, ₺242 Mn); en büyüğü F_XU0301026 short ₺7,26 Mr. Kontrol: 88,23 − 22,79 = 65,44 (K26 net formülüyle uyumlu). YORUM: 0,70 × 88,23 − 22,79 = 38,97, görseldeki 38,07 değildir; beta ayarlı formül belirsiz. Fon analizi kapsamı: karar Levent'te bekliyor. Parametre: THF 06.09.2026: brüt hisse %88,23; VİOP short/NAV %22,79; net hisse %65,44; portföy beta 0,70; net beta maruziyeti %38,07 (görsel, açıldı)
  - `tweet-fon-akis-hizi-ivme-velocity-2099959209467211874` — `tweet-fon-akis-hizi-ivme-velocity-2099959209467211874` (2026-09-15): Akış ivmesi: "Hatta yönünden çok, o hareketin ne kadar hızlandığına önem vermek gerekir." ve "Bu tek başına al-sat sinyali değil elbette." (Ham). Okuma (YORUM): TLY için 5 ve 20 günlük çıkış karşılaştırması örnektir.

## K27. Fon risk radarı: para akışı, AUM, yoğunlaşma ve likidite erken uyarı zinciri (hisse dışı fon analizi; kapsam kararı Levent'te bekliyor)

- Kaynak: On dördü Ham (Tansu'nun X gönderileri, 04–18.09.2026; biri 18.10.2025): `tweet-fon-erken-uyari-zinciri-para-akisi-2099132513708851639`, `tweet-fon-negatif-akis-risk-kurali-2099138697182507037`, `tweet-fon-para-akisi-likidite-erken-uyari-2095931263593095368`, `tweet-fon-likidite-konsantrasyon-erken-uyari-2099919520844382444`, `tweet-fon-icerik-taban-riski-2095801101626814908`, `tweet-fon-riski-akis-likidasyon-marketability-2097393379243962378`, `tweet-fon-risk-radar-skor-haritasi-2097551651838034055`, `tweet-fon-stres-skoru-rejimleri-2097983494991339894`, `tweet-fon-stres-testi-akis-aum-likit-tampon-2096243590133407910`, `tweet-fon-stres-testi-likidite-itfa-2100513708170428797` (öncekinin tekrarı), `tweet-fon-likidite-stres-sorulari-2100003921867501927`, `tweet-fon-risk-kontrol-listesi-2099926035282235807`, `tweet-fon-stres-risk-basliklari-2100922358806565025`, `tweet-fon-yatirimci-sayisi-risk-kontrol-1979695659432427919` (18.10.2025; ayrı bir fon seçim filtresi). `tweet-fon-stres-testi-likidite-itfa-2100513708170428797` Tansu'nun kendi gönderisini alıntılar; yeni kural içermez.
- Kapsam (YORUM, 16.10; karar Levent'te bekliyor): Yatırım fonu BIST hissesi değildir; bu bölüm kaynak kaydıdır. Tansu'nun kendi çerçevesi: bu bir hisse sinyali değil, fon izleme kuralıdır. Stres testi hesabı K26'dadır.
- Tansu'nun ifadesi (verbatim):
  - Zincir (13.09.2026, DOH örneği): "5 günlük para akışı negatife döner → 20 günlük akış zayıflar → AUM zirveden geriler → yüksek ağırlıklı ve düşük likiditeli hisselerde risk artar." Aynı gönderide örnek okuma: "Genel risk seviyesi orta-yüksek"; en büyük pozisyon fonun %21,1'i, ilk 5 pozisyon %45,6'sı, portföyün yaklaşık %39,6'sı yüksek/kritik likidite grubunda, en zor pozisyonda (DSTKF) teorik çıkış yaklaşık 12 işlem günü.
  - Negatif akış kuralı (LTL): 5G yaklaşık −37,92 milyon TL, 20G −649,89 milyon TL. "Hem kısa hem orta vadeli akışın negatif olması, fondaki çıkış baskısının devam ettiğini gösteriyor." Sonraki adım: AUM gerilemesi ve yüksek ağırlıklı pozisyonlarda gerçek adet azaltımının başlayıp başlamadığı izlenir.
  - İlk erken uyarı (THF): "En önemli erken uyarı, fon fiyatında ilk kırmızı gün değil güçlü para girişlerinin belirgin şekilde yavaşlaması ve ardından kalıcı para çıkışına dönüşmesidir." Fon büyüdükçe büyük pozisyonların likiditesi önem kazanır.
  - İçerik riski: "Fonun görünen günlük getirisine değil, fonun içindeki hisselerde ne olduğuna bakın. Likit hisseler bile taban oluyorsa asıl risk henüz fon fiyatına tam yansımamış olabilir."
  - TLY örneği: 5G yaklaşık 14 milyar TL, 20G yaklaşık 72,6 milyar TL net çıkış; fon büyüklüğü zirveden yaklaşık %12 geri. "Bir hissenin zor satılması tek başına alarm üretmez." Sistem, fonun para kaybını, AUM'un zirveden gerilemesini, pozisyon değişimlerini ve fiyat-hacim davranışını birlikte değerlendirir.
  - Beş ölçünün birleşimi: "Özellikle sürekli para çıkışı + yoğun portföy + düşük likidite + yüksek marketability stresi aynı anda oluşuyorsa risk ciddi biçimde yükselir." (para akışı, fon büyüklüğü değişimi, portföy yoğunlaşması, likidasyon süresi, marketability stresi.)
  - Planlanan çıktı (Fund Risk Radar): fon için 0–100 risk skoru ve ısı haritası: "Para Akışı, AUM, Yoğunlaşma, Likidite ve Türev Riski ayrı ayrı düşük, orta veya yüksek olarak gösterilecek." Ayrı "Fon Stres Skoru" ve rejimler: "NORMAL, GERİLİYOR, FİNANSMAN STRESİ, ZORUNLU SATIŞ RİSKİ ve KRİTİK".
  - Stres testi girdileri: 5G ve 20G akış, AUM'un zirveden gerilemesi, likit tampon, konsantrasyon, büyük pozisyonların işlem kapasitesine oranı. Soru: "Fon yüzde 5 veya yüzde 10 büyüklüğünde bir itfayla karşılaştığında, bunu nakit ve likit varlıklardan mı karşılayabiliyor". "likidite stresini yönetemeyen bir portföyün düşük volatilitesi çoğu zaman yalnızca stres gelene kadar düşük kalır."
  - Liste notları: soru listesi ("Fon ne kadar sürede nakit yaratabilir Yatırımcı çıkışları hızlanıyor mu?"), kontrol listesi ("Fonda görünmeyen risk bazen fiyat grafiğinde hemen ortaya çıkmaz."), beş risk başlığı ("likidite riski, konsantrasyon riski, marketability riski, taban riski, karşı taraf riski"). Üçünde de eşik yok.
  - Fon seçim filtresi (NMG örneği): "11 kişilik fonda bu kadar yüksek getiri çok tehlikelidir". Gerekçe: çok az yatırımcılı fonda çok yüksek getiri tuzak sayılır (fiyat oynatma, düşük hacim, çıkış sıkışması).
- Tanım: Bu bir BIST hissesi sinyali değil, fon izleme kuralıdır. Zincirin halkaları: (1) son 5 günlük tahmini net para akışı negatife döner; (2) son 20 günlük akış zayıflar; (3) fon büyüklüğü (AUM) zirveden geriler; (4) yüksek ağırlıklı ve düşük likiditeli hisselerde risk artar. 5G ve 20G akış birlikte negatifse çıkış baskısı sürüyor sayılır. YORUM: "zayıflar" ve "zirveden geriler" için sayısal ölçü yoktur; sayı eşikleri bizim seçimimiz olurdu ve bu kayıtta seçilmemiştir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| 5G net akış | negatife dönüş; eşik yok | Ham |
| 20G net akış | zayıflama; eşik yok | Ham |
| AUM | zirveden gerileme; eşik yok (örnek: TLY'de yaklaşık %12) | Ham |
| yoğunlaşma | en büyük pozisyon ve ilk 5 pozisyon ağırlığı; eşik yok (örnek %21,1 ve %45,6) | Ham |
| itfa testi | %5 veya %10 | Ham |
| risk skoru aralığı | 0–100; formül ve ağırlık yok | Ham |
| rejimler | NORMAL, GERİLİYOR, FİNANSMAN STRESİ, ZORUNLU SATIŞ RİSKİ, KRİTİK; sınırlar yok | Ham |
| yatırımcı sayısı | 11 (NMG örneği; eşik değil) | Ham |

- Belirsiz kalanlar: Bütün eşikler ve pencereler. "Zayıflar" ve "zirveden geriler" için ölçü. Skor formülü ve bileşen ağırlıkları. Kırmızı, sarı, yeşil pozisyon sınırları. "Tahmini net akış" hesabı (TEFAS verisinden türetilmiş, yöntem yazılı değil). KAP portföyü aylıktır, TEFAS daha günceldir; Tansu tarih farkını kendisi uyarı olarak yazar. "Az yatırımcı" için sayı eşiği.
- Tansu'nun kanıtı: Yok. Örnek fonlar (DOH, THF, TLY, LTL, TP2 ve diğerleri) tek tek okunur; sınama ve sonuç yok.
- Bedava günlük veri: Hayır. TEFAS fon akışı ve KAP portföy verisi TASARIM'ın günlük hisse OHLCV verisinde yok.
- Kaynak güveni: Ham, birinci el. İlke ve uyarı düzeyi; eşik yok. Hazırlık X.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-aum-fiyat-farki-para-girisi-rotasyon-2099908239471116731` — Okuma (YORUM): Fon fiyatı, AUM ve para akışı birlikte okunur; sınıflar arası çıkış-giriş birebir transfer sayılmaz. Ham: "Fon büyüklüğünün artması sadece fonun değer kazanmasından kaynaklanmıyor." ve "Veriler böyle birebir bir transferi göstermiyor."
  - `tweet-fon-inceleme-iki-asamali-cerceve-2096196385636815320` — `tweet-fon-inceleme-iki-asamali-cerceve-2096196385636815320` (2026-09-05; Ham): Fon içi inceleme: "fon ne taşıyor, konsantrasyonu ne, portföyü nasıl değişiyor, likiditesi ve forced-selling riski nedir." (Ham). Okuma (YORUM): önce piyasa akışı ve fon risk/getiri profili, sonra fon içeriği incelenir.
  - `tweet-fon-para-giris-hizi-yavaslama-uyarisi-2096257686266343893` — `tweet-fon-para-giris-hizi-yavaslama-uyarisi-2096257686266343893` (2026-09-05; Ham): Akış hızına dikkat: "Para hızlı giriyorsa iştah vardır; yavaşlıyorsa tereddüt başlamıştır." ve "Hele bir de çıkış hızı artıyorsa, fiyat hâlâ güçlü görünse bile ben temkinli olurum." (Ham).
  - `tweet-granger-para-akisi-getiri-nedensellik-2101627771524927545` — Okuma (YORUM): THF incelemesi getiri kaynağına ve sürdürülebilirliğe bakmayı önerir. Ham: "Fon analizinde sadece getiriye değil, getirinin kaynağına ve sürdürülebilirliğine bakmak gerekir."
  - `tweet-para-girisi-getiri-ayri-olcum-2099588429470187691` — `tweet-para-girisi-getiri-ayri-olcum-2099588429470187691` (2026-09-14): Ham: "para girişini fon talebinin gücü olarak, getiriyi ise ayrı bir performans göstergesi olarak değerlendiriyorum." Okuma (YORUM): THF örneğinde hedge ve net maruziyet, para girişi-getiri ilişkisinde ayrı izlenir.

## K28. Momentum listesinde marjı görünce kâr al (günlük hedef %3)

- Kaynak: `tweet-momentum-daily-profit-taking-1899490904479535439` (Ham), `tweet-momentum-hisse-onceden-cikis-hedefi-1969789658574868800` (Ham + görsel, açıldı), `tweet-momentum-intraday-margin-exit-1911100402596024733` (Ham). Üçü Tansu'nun X gönderisidir (11.03.2025, 21.09.2025, 12.04.2025). K5 ve K25 başka çıkış yöntemleridir; bu bölüm onları değiştirmez.
- Tansu'nun ifadesi (verbatim): "10-15 arası hisse veriyorum." "Momentum trader olarak günlük kazancımızı almamız lazım. Sert hareket sert tepki getirir." "Eliniz satış tuşuna gitmeyi bilmeli." (Ham, 11.03.2025). "Momentum hisseleri faz alanlarına çıktığında artık oyuncular! kar almaya başlar, dolayısı ile satış daha hızlı ve sert olur." "Nerede satacağınızı bilmezseniz Tukas örneğinde olduğu gibi -7 yersiniz." "Günde %3 kazansanız ayda bileşik getiri ile %143 kazanırsınız." (Ham, 21.09.2025). "Toplam% altında 19 Eylül itibari ile getirisi var, DEY% altında ise hissenin yarattığı marj." (Ham, 21.09.2025). "bunlar en yüksek değerleri zaten momentum traderlar olarak marjı görünce satmak lazım" ve "listede homojenlik yoktu kötü getiriler de oldu" (Ham, 12.04.2025: "gün içi oluyor sonra düzeliyor").
- Tanım: (YORUM) Günlük momentum listesindeki hisse, liste gününden sonra bir marj (kâr) oluşunca satılır; beklenen tepe beklenmez. Marj ölçüsü Tansu'nun tablosundaki "DEY_Potansiyel_%" sütunudur: Dönem_Max / Başlangıç − 1 (görsel, açıldı; 12 satırın hepsinde bizim hesabımızla tutar, örnek IPEKE 69.00 / 64.05 − 1 = %7,73; B §14'teki DEY formülüyle aynı). Görsel tablo (görsel, açıldı): "HİSSE FİYAT ANALİZİ - 17 Eylül 2025 / 19 Eylül 2025", 12 hisse, 3 gün; Toplam_% +6.17 (IPEKE) ile −15.46 (TUKAS) arası; 6 hisse pozitif, 6 negatif; 12 hissenin hepsinde DEY_Potansiyel_% pozitif (1.31 ile 10.66 arası), kapanışı negatif 6 hissede de (1.31 ile 7.50 arası; TUKAS 3.86). Bizim hesap: ortalama Toplam_% = −0,10; ortalama DEY_Potansiyel_% = 5,49.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| liste büyüklüğü | 10-15 hisse | Ham |
| günlük hedef | %3 | Ham |
| aylık bileşik | %143 | Ham; 1,03^30 − 1 = %142,7 (30 gün varsayımı, YORUM); 21 işlem günüyle %86,0 |
| satış tetiği | "marjı görünce" (eşik yok) | Ham |
| stop | yok | Ham'da yok |
| ölçüm penceresi | 17-19 Eylül 2025, 3 gün | görsel, açıldı |

- Belirsiz kalanlar: Marj eşiği ve satış fiyatı. Liste seçim kuralı (Tansu "listede homojenlik yoktu" der). Tablodaki Günlük_% tanımı (Toplam_% / 3 değil: IPEKE 6.17 ve 4.86). Ham "-7" der; tabloda TUKAS Günlük_% −6.17 ve Toplam_% −15.46; "-7" hangi ölçüdür belli değil. Satış gün içi mi kapanışta mı.
- Tansu'nun kanıtı: 12 hisselik tek tablo, 3 gün; seçilmiş dönem. DEY gerçekleşmiş tepedir (sonradan bilinir); tepede satış mümkün değildir, tablo "marjı görünce sat" kuralının sonucu değildir (YORUM).
- Bedava günlük veri: Kısmen. Günlük High ve Close ile 3 günlük sonuç ve DEY hesaplanır. "Marjı görünce" satışı gün içi izleme ister. TASARIM §3 süre çıkışını ilk sürümün dışında tutar; iz süren stop ve kısmi kâr yalnız EMA ailesinin varyantlarındadır (KURALLAR §3).
- Kaynak güveni: Ham ve görsel birinci el; eşik yok: düşük-orta. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-tobo-tarama-al-sinyali-1928156672142254465` — Okuma (YORUM): PKART grafikleriyle günlük kazanç sonrası yeni taramayı bekleme ifadesi. Ham: “Al günlük banka faizini geç kenara yeni taramaları bekle:)”. Okuma (YORUM): Bu ifade mevcut yüzde hedefini yeniden tanımlamaz.

## K29. X arşivi kısa kayıtları (16.10)

- Derinlik skoru, Weighted OBI ve Master Score (emir defteri likidite riski; `tweet-depth-score-weighted-obi-master-score-1985834408268431394`, `tweet-derinlik-skoru-likidite-siralama-1983531759049326636`; Ham; Tansu'nun X gönderileri, 04.11.2025 ve 29.10.2025): "Benim kod "VBTS" nedir bilmez, o sadece semptomları okur." "Master_Score diyor ki: "Bu kağıt tavan gidiyor (Yüksek Score_Momentum) ama tahtası hem çok sığ (Düşük Depth_Score) hem de birileri satışta (Negatif Weighted_OBI). O hedefe gidiş yolu şu an 'sağlıksız' ve 'çok riskli'."" "Hata da yapmış olabilirim" (Ham). Örnek: CRDFA'da Weighted_OBI −0,58. Sıralama gönderisi: "Şu da şurada dursun belki lazım olur" / "28 Ekim analizidir"; görsel metni: Depth_Score'a göre "En Likit 10" (GSRAY 70.000000 … PGSUS 15.433848) ve "En Az Likit 10" (ISBTR 0.000000 … LUKSK 0.228698); sütunlar SON, Depth_Score, Spread_Pct, Total_Depth. Spread_Pct yüzde olamayacak büyüklükte (örnek GSRAY −1,1e10, ISBTR −111): başlık veya birim tutarsız (Tansu'nun çıktısında, havuz hatası değil). Master_Score formülü, bileşen ağırlıkları, eşik, emir defteri seviye sayısı yok. Günlük veriyle: hayır (emir defteri verisi ister; K10: spread ve derinlik yok). Hazırlık X. Güven: Ham; düşük.
- Günlük minor trendde %5 kâr al, haftalıkta bekle (`tweet-harmonik-gunluk-5-kar-al-haftalik-bekle-1871469112029024683`; Ham; Tansu'nun yanıt gönderisi, 24.12.2024; üst gönderi notta yok): "Bunlar günlük minor trend al %5 i geç kenara" ve "Haftalıkları bekleyeceksiniz getirisi daha yüksek". Gönderi üç hisse kodu sayar (Brsan, Suwen, Uluse); "bunlar" bu üçünü gösterir (YORUM). Parametre: günlük kâr eşiği %5 (Ham). %5 fiyat getirisi mi pozisyon oranı mı belli değil (YORUM: fiyat getirisi); "minor trend" tanımı, kurulumun adı (dosya adı "harmonik" der; Ham'da bu sözcük yok), giriş koşulu, tam ya da kısmi çıkış, haftalıkta çıkış ve stop yok. Tansu: "Kazançları ben yazmıyorum grupta arkadaşlar yazsın": sonuç paylaşmaz. Günlük veriyle: %5 eşiği evet, kurulum tanımı olmadığı için kural olarak hayır. Hazırlık X. Güven: düşük.
- Hisse bazlı giriş-çıkış parametre optimizasyonu (`tweet-hisse-bazli-ema-optimizasyonu-1845478584154026462`, `tweet-hisse-bazli-parametre-optimizasyonu-1840170065464803535`, `tweet-macdas-varsayilan-parametre-testi-1778715914843684969`; Ham; Tansu'nun X gönderileri, 13.10.2024, 28.09.2024, 12.04.2024): "Her hisse için optimizasyon yaparak bulunur", "Ben onu hisse özelinde yapıyorum", "Taramadsn çıkam hisselerin giriş çıkış optimım ema değerini bulursunuz" (13.10.2024). "parametreler optimize edilmedi. her hisse için farklı parametrelerde giriş çıkış yapmak lazım. 5-12 sadece bir kural ama optimize edilmeli." ve "Bu liste günlük." (28.09.2024). "Eğer gerçekten değişkenleri optimize etmeyi bilmiyorsanız trade yapmayın." (12.04.2024; DOAS, standart MACDAS parametreleri, son 500 bar). Görsel (macdas, görsel açıldı): iki çizgi, "Data" mavi çizgi yaklaşık %300–360'a, "Overall" kırmızı çizgi yaklaşık %60–75'e çıkar, 13.04.2022–02.04.2024 (yaklaşık okuma); Ham hangi çizginin al-tut olduğunu yazmaz (YORUM: Data = al-tut, Overall = strateji). Parametre: zaman dilimi günlük, örnek kural "5-12" (YORUM: EMA 5 ve EMA 12; Ham EMA demez), macdas penceresi son 500 bar. Optimizasyon aralığı, ölçütü, yöntemi ve örneklem dışı doğrulama yok. YORUM: K20'de Tansu klasik indikatör parametre optimizasyonunu "doğru yapılmaz ise" gürültüye uydurma sayar; bu notlar hisse bazında optimizasyon önerir; ikisi de koşulludur ("bilmiyorsanız yapmayın" ortak noktadır); çelişki çözülmedi. TASARIM kural parametresini yalnız belge değişikliği ve yeni deneme ile değiştirir; uygulama kararı belgeye aittir. Günlük veriyle: teknik olarak evet. Hazırlık X. Güven: Ham ve görsel birinci el; yöntem ve sayı yok: düşük. İlgili: B §34 (EMA 12-144-169).
- Kelly kriteri ile pozisyon büyüklüğü (`tweet-kelly-kriteri-pozisyon-boyutu-1874425159224000594`, `tweet-kelly-kriteri-pozisyon-boyutu-1874426039340007571`; Ham; Tansu'nun X gönderileri, 01.01.2025): "100.000 liram var , trade yapmak için ne kadar yatırayım ki optimal bir seviye olsun?" "Cevabı Kelly Criteria." "Bazıları fractional kelly criteria da kullanır." "Hisse kripto aynı mantık." "bunun hesaplama tablosu var ispatı ile birlikte. ben genelde kullanırım robotlarımda limitim genelde KC'dır benim." YORUM: Kelly oranı f* = p − (1 − p) / b (p kazanma olasılığı, b ortalama kazanç / ortalama kayıp); kesirli Kelly = k × f*; Tansu formülü, p ve b girdilerini ve kesri yazmaz. "Limit" sözü Kelly'nin sermaye payı için üst sınır olduğunu gösterir (YORUM). K1'deki %1 risk ve 2 ATR lot kuralıyla ilişki yazılı değil (Kelly üst sınır mı, K1'in yerine mi). Sayı yok (sermaye örneği 100.000 TL). Hesaplama tablosu havuzda yok. Günlük veriyle: formül evet; p ve b için işlem dizisi gerekir (YORUM: backtest işlem listesi verir; küçük örneklemde tahmin hatası büyük). Hazırlık X. Güven: düşük.
- Satış hızı: Monte Carlo, doğrusal ve kuadratik (`tweet-monte-carlo-satis-hizi-stratejisi-1911720907514540232`; Ham ve görsel birinci el, iki görsel açıldı; Tansu'nun X gönderisi, 14.04.2025): "Hisselerimi nasıl bir hızla satarsam daha az zarar ederim?" Sonuç cümleleri: tarafsız piyasada "En iyi performans: Fast Quadratic"; yükselen piyasada "En iyi: Linear"; düşen piyasada "En az zarar: Fast Quadratic"; "Slow linear çok kötü". Beş hız profili (linear, fast linear, slow linear, fast quadratic, slow quadratic), AKBNK etiketi; ortalama PnL TRY üç senaryoda (mu = 0.00 / 0.04 / −0.04): linear −156.22 / 716.37 / −159.66; fast quadratic 185.62 / 1.20 / −67.12; slow quadratic −250.64 / 396.68 / −230.72; fast linear −536.72 / −541.45 / −403.72; slow linear −24964.50 / −24994.70 / −25093.12 (görsel, açıldı). Fiyat süreci, spread ve etki katsayıları, satış ufku, yol sayısı, mu birimi, kod yok. YORUM: slow linear'ın büyük kaybı süre sonunda satılmamış hisse kalmasından gelebilir (Ham: "sonunda kalan bile var"); simülasyon sentetiktir, AKBNK yalnız etikettir. Günlük veriyle: hayır (gün içi emir bölme, spread ve piyasa etkisi ister; TASARIM §3 gün içi veriyi dışarıda bırakır). Yalnız ilke: düşen veya yatay piyasada çıkışı geciktirme. Hazırlık X. Güven: düşük (model parametresi yok).
- Hedge: testere bölgesinde negatif korelasyonlu hisse ve eski put önerisi (`tweet-negatif-korelasyon-hedge-1858890348736532774`, `tweet-put-opsiyon-portfoy-koruma-1734957210545844544`; Ham; Tansu'nun X gönderileri, 19.11.2024 ve 13.12.2023; görsel yok): 19.11.2024: "Testere bölgelerinde negatif korelasyonlu hisseleri kullanarak riski hedge edebilirsiniz. Giriş seviyesi hedging stratejisi." ve "Viop çok da gerekli değil." 13.12.2023: "#bist100 olan incitici dalgalanmalar bir kez daha hedging kavramının önemini ortaya çıkardı. portföylerinizi düşüşlere karşı korumak için put opsiyonları satın alabilirsiniz. Eğer hisse senetleri değer kaybederse, put opsiyonları değer kazanır ve zararı telafi eder." YORUM: "testere bölgesi" yatay ve sık yön değiştiren fiyat aralığı demektir; hedge, eldeki pozisyonla ters yönde hareket eden hisse tutmaktır; korelasyon günlük getirilerden hesaplanır. Sonraki görüş (2024) hisse tabanlı hedge'dir, 2023 gönderisi put önerir; çelişki çözülmedi. Parametre yok: korelasyon eşiği, pencere, hedge oranı, testere bölgesi tanımı, hangi pozisyona hangi hedge, "giriş seviyesi" anlamı (YORUM: başlangıç düzeyi), hedge pozisyonunun boyutu ve çıkışı, put için vade ve kullanım fiyatı. Günlük veriyle: korelasyon hesabı evet (günlük kapanış getirileri); testere bölgesi tanımı olmadığı için kural olarak hayır. Put opsiyonu hayır: opsiyon TASARIM §3 kapsam dışıdır. D'deki çift ailesi ve sabit ağırlık dengelemesi ters korelasyonlu varlıkları başka amaçla kullanır; bu hedge ayrıdır (YORUM). İlgili: K33 (VaR ve hedge). Hazırlık X. Kaynak güveni: Ham birinci el; sayı ve koşul yok: düşük.
- Portföy payı: %80 uzun vade, %20 trade (`tweet-portfoy-80-uzun-20-trade-1761787714523865301`; Ham; Tansu'nun X yanıt gönderisi, 25.02.2024; üst gönderi id 1761784730012307695 notta yok; görsel yok): "O kadar doğru ki, trade yapacaksan bile temeli sağlam hissede trade yapacaksın. Volatilitesi yüksek bir ortamda her an terste kalabiliriz. Ben doğrusu portföyümün %80 i uzun vadeli %20 si de trade olarak tutuyorum. Temel analize çok önem veriyorum". Parametre: uzun vadeli kasa %80, trade kasası %20 (Ham); "temeli sağlam" ölçüsü yok. YORUM: Tansu sisteminin sinyalleri yalnız trade kasasına aittir; uzun vadeli kasa temel analize dayanır (değerleme, TASARIM §3 kapsam dışı). "temeli sağlam hissede trade yapacaksın" bir hisse filtresi sayılabilir, ama ölçüt yazılı değil. Bu dağılımın kural mı yoksa Tansu'nun kişisel durumu mu olduğu, yeniden dengeleme, trade kasası içinde pozisyon sayısı ve boyutu (K1 ile ilişki yazılı değil) belirsiz. Günlük veriyle: pay bölmesi veri gerektirmez; temel filtre hayır. Hazırlık X. Kaynak güveni: Ham birinci el; kişisel beyan, kural değil: düşük.

**Kripto (BIST evreni dışı)**

- Kripto için portföy payı üst sınırı (`tweet-kripto-portfoy-payi-yuzde-1-5-1783205936427119005`, `tweet-kripto-portfoy-yuzde-4-sinir-1840693444294975693`, `tweet-kripto-portfoy-yuzde-5-10-sinir-1860757961032835441`; Ham; Tansu'nun yanıt gönderileri, 24.04.2024, 30.09.2024, 24.11.2024): "Kriptoya hiç girmem, bence sizde portföyün maks. %1 ile %5 ini ayırın" (24.04.2024). "bilemem", "Bana göre değil", "Kimine göre öyle", "Portföyün Max %4’ini geçmemeli kripto yatırımı" (30.09.2024). "kripto tavsiye etmem ya ya da tüm portföyünüzün max %5-10'unu aşmamalı" (24.11.2024). Üç değer birbiriyle çelişir (tarih sırasıyla portföyün %1–%5'i, %4'ü, %5–%10'u); hangisi geçerli belli değil. Üçü de başkasına verilmiş kişisel öneridir; Tansu "girmem" ve "tavsiye etmem" der, yani kendi sistem kuralı değildir. YORUM: 30.09.2024 gönderisinde "Bana göre değil / Kimine göre öyle" ifadesi %4'ün Tansu'nun mu başkalarının mı görüşü olduğunu belirsiz bırakır (not 30.09.2024'te yanıt başlığında @JR_GPT, Ham gövdesinde @J0sephRock görünür; kullanıcı adı uyuşmuyor, not değiştirilmez). "Portföy" neyin toplamı, cevaplanan kişilerin portföy büyüklüğü belli değil. Kripto BIST kapsamında değildir; TASARIM §3 yalnız BIST hissesi, alış yönü. Hazırlık X. Güven: Ham; kişisel görüş, üç değer çelişir: düşük.

- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-rsi-esik-periyot-optimizasyonu-1860405835354054736` — RSI eşiği ve periyodu hisse volatilitesine göre optimize edilir: "RSI 30/70 Allah kelamı değil." (Ham). Biri 2,5 kat, öteki 1,2 kat civarı kümülatif çarpan veren iki ayar gösterilir (görsel, açıldı; yaklaşık okuma). Levent kararı 16.10: hisse bazında optimize edilir; uygulama TASARIM 5.14 (`tansu-sinama`). Parametre: RSI ayarı (periyot, üst eşik, alt eşik; sıra YORUM) = (6, 65, 20) ve (26, 75, 24), EURUSD=X, TC = 7e-05, 2004–2020 (görsel, açıldı)
  - `tweet-strateji-hisse-uygunluk-testi-1845362765898097116` — WaveTrend (10, 21) stratejisi DOAS'ta al-tutun gerisinde: "Çoğu strateji çalışmıyor bu hissede. Al tut stratejisi hep daha çok kazandırmış." (Ham). Eşik revizyonu ">-60 ve <50" yerine "<-50 ve <50" getiriyi artırdı; "her hissede ayrı ayrı bakmak lazım" (Ham). Levent kararı 16.10: hisse bazında optimize edilir; uygulama TASARIM 5.14 (`tansu-sinama`). Parametre: WaveTrend = (10, 21) (görsel, açıldı: "WT (10 , 21)"); eşik revizyonu = ">-60 ve <50" yerine "<-50 ve <50" (Ham; hangi çizgiye ve hangi koşula uygulandığı yazılı değil, YORUM: alım koşulu); A §5 tablosundaki WaveTrend eşikleriyle (60, 53, −53, −60) aynı değil
  - `tweet-tarama-sonrasi-grafik-teyidi-1841012769706905780` — Tarama listesi aday listesidir; grafik açılıp karar verilir: "Tarama sonucu çıkan her hisse alınmaz.taramada kullandığın parametreler her hisse için uygun değildir." ve "Tarama yelpaze daraltır." (Ham). Hisse bazlı parametre ihtiyacını destekleyen bir cümledir; sayı, eşik ve yöntem yok. Levent kararı 16.10: hisse bazında optimize edilir; uygulama TASARIM 5.14 (`tansu-sinama`).
  - `tweet-tarama-sonucu-gozle-dogrulama-1839014128201118148` — Yanıt (@lvntsahn; üst gönderi notta yok): taramadan çıkan sonuç göz ile incelenir ve backtest ile optimizasyon yolu açık bırakılır: "Ne olursa olsun taramadan çıkan sonuçların göz ile incelenmesi gerekir. En etkili backtest yoludur." (Ham). Sayı, eşik, optimizasyon aralığı ve ölçüt yok; göz incelemesi ölçülebilir kural değildir (YORUM). Levent kararı 16.10: hisse bazında optimize edilir; uygulama TASARIM 5.14 (`tansu-sinama`).
  - `tweet-yuzde-bes-kar-alma-kurali-2023354556990591279` — Tekrar: %5 kâr alma eşiği (Tansu'nun yanıt gönderisi, 16.02.2026). "Wall %5 i görünce kar almak lazım. BİST'te kar almadan ilerlemek büyük risk" (Ham). Yeni olan gerekçe cümlesidir (kâr almadan ilerlemek BIST'te risk). "Wall" hisse kodu mu belli değil (YORUM); %5 fiyat getirisi mi belli değil; kurulum, giriş, tam veya kısmi çıkış ve stop yok; üst gönderi notta yok.

- Hacim profili ile AB=CD hedef birleşiminde satış örneği (`tweet-rolatif-momentum-z-skoru-donus-onayi-2092655008948834306`; 26.08.2026, Ham): "POC'u geçerse 144-146'ya gitmek ister. VAL aynı zamanda 147"; "Küçük resimde ABCD hedefi de 148"; "Bir nevi confluence alanı o bölge. Gelirse satmakta fayda var". Okuma (YORUM): Rölatif momentum örnekleri dizisindeki tarihli satış bölgesi yorumudur. Sayılar örneğe aittir; genel hedef formülü, bant genişliği veya satış oranı olarak kullanılmaz. Bu koşullu hedef yorumu, çift rotasyonunun mevcut çıkışını değiştirmez. Hazırlık X.
- Kişisel yatırım dışlama ve satış notu (`tweet-yatirim-yapma-filtreleri-kendime-not-1794036593734418591`; 24.05.2024, Ham): "Kendime not"; "sharpe net kar marjı 2 den küçük şirketlere,"; "2-patron şirketlerine,"; "3-büyüme şirketlerine YATIRIM YAPMA"; "4-koç grubundan şaşma"; "5-şirkete aşık olma"; "6-vakti zamanı gelince yapıştır satışı, ACIMA"; "7-bu ülkede uzun vadeli yatırımcı olunmaz". Okuma (YORUM): Bunlar kişisel tercihlerdir. İlk satırın metrik tanımı belirsizdir; 2 sayısı Sharpe veya net kâr marjı eşiği diye ayrıştırılmaz. Kişisel kapsam ve satış zamanı ifadeleri otomatik evren veya çıkış kuralına çevrilmez. Hazırlık X.


## K30. Veriyi periyot kapanışında çek (tamamlanmış çubuk)

- Kaynak: `tweet-periyot-kapanisinda-veri-cekme-1923051430580977847` (Ham; Tansu'nun X yanıt gönderisi, 15.05.2025; üst gönderi id 1923042372901810520 notta yok; görsel yok).
- Tansu'nun ifadesi (verbatim): "Eğer 1H (saatlik), 4H (4 saatlik), D (günlük), W (haftalık) gibi zaman dilimlerinde veri çekiyorsanız verinin doğru ve eksiksiz olması için o periyodun kapanışında veri çekmek gerekir"
- Tanım: Mum verisi periyot kapanmadan çekilirse son çubuk eksiktir. Veriyi periyodun kapanışından sonra çek ve sinyali tamamlanmış çubuk üzerinde hesapla. YORUM: günlük sistemde bu, günlük çubuğu seans kapandıktan sonra çekmek ve haftalık çubuğu haftanın son işlem günü kapandıktan sonra çekmek demektir; devam eden çubuk sinyale girmez. TASARIM 5.1 (veri) ve 5.13 (veri kapıları) ile aynı yönde okunur (YORUM; TASARIM sahibidir).
- Parametreler: periyotlar 1H, 4H, D, W (Ham). Kapanıştan sonra bekleme süresi yok.
- Belirsiz kalanlar: Kapanıştan sonra ne kadar beklenir, kaynak gecikmesi ve ayarlı fiyat (düzeltme) güncellemesi, hangi veri sağlayıcı. 1H ve 4H TASARIM §3'te kapsam dışıdır.
- Tansu'nun kanıtı: Yok (veri ilkesi).
- Bedava günlük veri: Evet (D ve W için); 1H ve 4H kapsam dışı.
- Kaynak güveni: Orta. Ham birinci el; kısa, koşulsuz ilke. Hazırlık H.

## K31. Optimizasyonda sağlam (robust) bölge ve aşırı uyum (SMA 50/200 örneği)

- Kaynak: `tweet-sma-optimizasyon-saglam-bolge-asiri-uyum-1986899794032304554` (Ham ve görsel birinci el; görsel açıldı; Tansu'nun X gönderisi, 07.11.2025).
- Tansu'nun ifadesi (verbatim): "İyi bir optimizasyonun sırrı, en yüksek tek bir tepeyi (o %5000'lik tek sonucu) bulmak değildir. İyi optimizasyon, "sağlam" (robust) bir bölge bulmaktır." "(40, 140), (45, 145), (40, 150) gibi geniş bir alanın tamamı kârlıysa, "Tamam," dersin, "bu stratejinin kendisi sağlam, ayarları biraz değiştirsem bile çalışıyor."" "Ama sadece tek bir nokta (13, 47) kârlı, hemen yanındaki (14, 48) felaket zarardaysa, bil ki o bir tuzaktır." "Eğer en iyi ayarları bile para kazandırmıyorsa, o stratejiyle vakit kaybetmeyi bırakırsın." "Optimizasyon bir kurtarıcı değil, çok keskin bir bıçaktır." Gerekçe: 50/200 varsayılandır, "Bilmiyoruz. Sadece varsayıyoruz"; piyasa hızı değişir, ayar hissenin "kimliğine" uymalıdır.
- Tanım (kaynak sırası):
  1. Parametre ızgarasını tara (örnek: 10 ile 250 arası on binlerce kombinasyon).
  2. En yüksek tek noktayı seçme; komşu ayarların da kârlı olduğu geniş bölgeyi ara (sağlam bölge).
  3. Tek nokta kârlı, hemen yanındaki ayar zararlıysa o nokta aşırı uyumdur (overfitting); reddet.
  4. En iyi ayar bile zarardaysa stratejiyi bırak.
  5. Örnek (görsel, açıldı): XU100.IS, 2020-11-07–2025-11-07, en iyi ayar SMA 35/240, toplam getiri çarpanı 4,6948 (+%369,48); aynı dönemde al-tut +%786,25. En iyi bulunan ayar al-tutun altındadır.
  YORUM: komşuluk genişliği ve "kârlı" ölçüsü yazılı değil; uygulama için ızgara üzerinde hedef ölçütün komşuluk içindeki en kötü veya medyan değeri aranabilir (Tansu söylemedi).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| arama aralığı (örnek) | 10–250 | Ham |
| varsayılan SMA çifti | 50/200 | Ham |
| XU100 en iyi çift (5 yıl) | 35/240 | görsel, açıldı |
| komşuluk genişliği, kârlılık ölçüsü | yok | belirsiz |
| örneklem dışı doğrulama | yok | belirsiz |

40/145, 22/118, 13/47, (14, 48), (40, 140), (45, 145), (40, 150) çiftleri örnektir; kural parametresi değildir (Ham).
- Belirsiz kalanlar: Komşuluğun ölçüsü, hedef fonksiyon (getiri mi risk ayarlı mı), örneklem dışı ya da walk-forward doğrulama, yeniden optimizasyon sıklığı. Levent kararı 16.10: hisse bazında optimize edilir; uygulama TASARIM 5.14 (`tansu-sinama`). K20 sağlam bölge (plateau) önerisini Claude'a ait YORUM saymıştı; bu gönderi aynı fikri Tansu'nun kendi ifadesi olarak verir. TASARIM kural parametresini yalnız belge değişikliği ve yeni deneme ile değiştirir. İlgili: B §35 (SMA kesişimi), B §34 (EMA optimizasyonu).
- Tansu'nun kanıtı: Tek örnek, XU100 SMA 35/240, al-tutun altında. Sağlam ve tuzak bölge örnekleri varsayımsaldır (Ham "örneğin"); ısı haritası veya sayı yok.
- Bedava günlük veri: Evet (XU100.IS günlük kapanış, ızgara taraması).
- Kaynak güveni: Orta. Ham ve görsel birinci el; ilke düzeyi, ölçü yok. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-hareketli-ortalama-kesisim-optimizasyonu-2071142623520215512` — Okuma (YORUM): Sabit golden cross yerine kesişimlerin hangi rejimi gösterdiğini araştırma önerisi. Ham: "optimization should actually be used to analyze which moving average crossovers indicate the formation of bearish or bullish markets".

## K32. Under 30 Over 30: 1,5 R sonrası giriş fiyatına dönüşte başabaş çıkışı

- Kaynak: `tweet-under30-over30-1-5r-basabas-cikis-1992547498343161903` (Ham; Tansu'nun X gönderisi, 23.11.2025; görsel yok).
- Tansu'nun ifadesi (verbatim): "Eğer kârlı bölgeye geçtikten sonra fiyat geri dönerek tekrar tam olarak giriş fiyatınıza ulaşırsa, derhal pozisyondan çıkmanız gerekir." "Gün sonunu beklemeye gerek yoktur; fiyat giriş seviyesine geri döner dönmez çıkış yapılır." R tanımı (Ham): "Risk biriminiz, genellikle başlangıçtaki zararı durdurma mesafesi". Amaç (Ham): "iyi bir kazançlı işlem olabilecek bir işlemin, kaybeden bir işleme dönüşmesine izin vermemektir."
- Tanım (Ham): (1) "Under 30 Over 30" kurulumuyla girilir (kurulumun tanımı bu notta yok). (2) Fiyat girişten 1,5 R lehine ilerlerse kural devreye girer. (3) Fiyat sonra tam giriş fiyatına dönerse pozisyondan hemen çıkılır; sonuç başabaş olur. (4) Çıkış gün içinde, anında yapılır. YORUM: bu, 1,5 R aktivasyonlu başabaş stoptur (stop = giriş, aktivasyondan sonra).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| aktivasyon eşiği | 1,5 R | Ham |
| çıkış fiyatı | giriş fiyatı (başabaş) | Ham |
| çıkış zamanı | gün içi, anında (gün sonu beklenmez) | Ham |
| R tanımı | başlangıç stop mesafesi | Ham |
| R'nin sayısal değeri | yok (K2'deki 2 ATR ise 1,5 R = 3 ATR; K25'teki YORUM başlangıç stopu 1,5 ATR ise 1,5 R = 2,25 ATR) | YORUM |
| aktivasyon fiyat alanı (High mı, kapanış mı) | yok | belirsiz |

- Belirsiz kalanlar: "Under 30 Over 30" kurulumunun tanımı (YORUM: RSI 30 altından yukarı geçiş olabilir; K5'te "RSI 30 girişi" maddesi vardır, ama Ham ilişkiyi söylemez). Başlık "RSI30 Kırılımı" der, gövde RSI'dan değil giriş fiyatından söz eder; başlık ile gövde uyuşmaz. 1,5 R'ye ulaşmanın ölçüsü (gün içi High mı, kapanış mı). Dolum: giriş fiyatı limit mi stop mu, açılış boşluğunda nasıl. Maliyet sonrası giriş fiyatı küçük zarardır. Kısa yön (Ham "veya yükselebileceği" der) BIST'te yok. Bu kural K25'in "n=2 ATR'de stop = giriş" adımına yakındır; ölçü farklıdır (R ve ATR basamağı), çelişki sayılmadı (YORUM). R'nin başlangıç stop ölçüsü (K25'in 1,5 ATR değeri ile K2'nin 2 ATR değeri): karar Levent'te bekliyor.
- Tansu'nun kanıtı: Yok (ilke; sayı, örnek ve sonuç yok).
- Bedava günlük veri: Kısmen. Giriş ve 1,5 R aktivasyonu günlük High ile, anında çıkış günlük Low ile yaklaşılır; aynı gün içinde aktivasyon ve geri dönüş olursa sıra günlük veride bilinmez (YORUM).
- Kaynak güveni: Ham; ders anlatımı biçiminde, tek parametre (1,5 R). Kurulum tanımsız: düşük-orta. Hazırlık K.
- Modül 1 çıkış paketi: KURALLAR §3.

## K33. Value-at-Risk (VaR): vadeye göre azami kayıp ve kayıp toleransına göre hedge

- Kaynak: `tweet-var-farkli-vade-maks-kayip-1878086550665175243` (Ham + görsel, açıldı; üç gönderilik zincir, 11.01.2025), `tweet-var-kayip-toleransi-hedge-1878089934268965110` (Ham; yanıt, @metinka20441963; üst gönderi notta yok; 11.01.2025), `tweet-value-at-risk-olcumu-1916228528850272645` (Ham; 26.04.2025). Üçü de Tansu'nun X gönderisidir. Kavramsal not B §27'de (Bollinger ve VaR) tek cümledir.
- Tansu'nun ifadesi (verbatim): "Aşağıda örneğin bir hisse senedine yapılan 100.000 tl yatırımın %99 güven düzeyinde 1 gün 1 hafta 1 ay 3 ay da maks kayıp oranları gösterilmektedir." "Son 10 yıllık veirler içe çalıştım. Burada max riskiniz bun miktarlar." "Vadenize göre maks. riskinizi belirlersiniz. Sonra bunu hedge etmek istersiniz." Hedge araçları: "put opsiyonu satın alabilirsiniz", "tamamen ters korelasyonlu bir hisse senedini portföyde tutmak", yüksek volatiliteli varlıkları "daha sabit getirili varlıklarla" dengelemek (altın, faiz, bono, tahvil). Tolerans: "O aslında kaybetmeyi göze alabileceğiniz tutar ile ilgili. tamamen kişisel." "%99 güven düzeyinde 100 bin için günde 5.000tl kaybetmeyi göze alabilirim derseniz ona göre bir hedging yolu izlemeniz lazım." 26.04.2025: "VaR, belirli bir güven düzeyinde (örneğin %95) ve belirli bir zaman diliminde (örneğin 1 gün) beklenen maksimum kaybı sayısal olarak tahmin eder." Gerekçe: "Sermaye yönetimi ve stop-loss seviyeleri için bilimsel zemin oluşturur."
- Tanım: (1) Pozisyon tutarı (TL) için güven düzeyi ve vadeye göre VaR hesaplanır (Ham: son 10 yıl). (2) Kişisel kayıp toleransı (TL) VaR ile karşılaştırılır. (3) YORUM: tolerans VaR'dan küçükse fark hedge edilir (put, ters korelasyonlu hisse, sabit getirili varlık). Görsel değerleri (görsel, açıldı; bar okuması, ölçüm): 1 gün ≈5.900 TL, 1 hafta ≈13.400 TL, 1 ay ≈28.500 TL, 3 ay ≈52.000 TL. YORUM: 1 günlük VaR (≈5.900) Tansu'nun örnek toleransından (5.000) büyüktür; örnekte hedge gerekir, ama Tansu bu karşılaştırmayı açıkça yazmaz. YORUM: karekök-zaman ölçeği 1 günden 13.200 / 27.000 / 46.800 TL verir (bizim hesap); görsel daha büyüktür, yöntem belli değil.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| güven düzeyi | %99 (örnek; 26.04.2025 gönderisinde %95 örnek) | Ham |
| vadeler | 1 gün, 1 hafta, 1 ay, 3 ay | Ham, görsel (açıldı) |
| veri penceresi | son 10 yıl | Ham |
| örnek yatırım | 100.000 TL | Ham |
| örnek kayıp toleransı | günde 5.000 TL (kişisel) | Ham |
| VaR yöntemi | yok (tarihsel, parametrik, Monte Carlo belli değil) | belirsiz |
| hedge oranı, put vadesi ve kullanım fiyatı | yok | belirsiz |

- Belirsiz kalanlar: Yöntem ve vade ölçekleme. Hedge büyüklüğü formülü. "Ters korelasyonlu hisse" seçimi (BIST'te nadir; YORUM). VaR'ın stop-loss ile bağlantısı ("bilimsel zemin" der, formül yok). K1'deki %1 risk ve 2 ATR lotuyla ilişki yazılı değil: K1 işlem başına kayıp bütçesidir, VaR ise pozisyon veya portföy için dağılım ölçüsüdür (YORUM). Grafikte hisse adı yok.
- Tansu'nun kanıtı: Yok (tek grafik, hisse adı ve doğrulama yok).
- Bedava günlük veri: VaR hesabı evet (günlük kapanış getirileri, 10 yıl). Hedge araçları (put, VİOP) kapsam dışıdır: TASARIM yalnız BIST hissesi ve alış yönüdür; opsiyon verisi yok. Hisse tabanlı hedge için bkz. K29 (negatif korelasyon).
- Kaynak güveni: Ham ve görsel birinci el; kavramsal, tek örnek: düşük. Hazırlık X.

---

# EK A. Kapsam dışı ama ilgili: çıkış ve stop sözü olan notlar

Çıkış ve stop sözleri sahibi dosyadadır; burada yalnız nereye bakılacağı yazılır. (bilet 04, 14.10)

| not | Sahibi |
|---|---|
| G-105 BOS Fibonacci golden zone | A §10 |
| G-107 BRYAT Elliott dalga 2 | C §16 |
| G-106 demand EMA squeeze | B §3 |
| G-113 BIST-VIX 5 adım (çıkış adımı ve alarm) | D, "BIST VIX long: 5 adım kontrol listesi" |

---

# (a) Tansu risk ve çıkış paketi: onun anlattığı biçim

Bu paket yalnız Tansu'nun söylediklerini birleştirir. Her boşluk etiketli.

| # | adım | Sahibi | etiket |
|---|---|---|---|
| 1 | Evren/likidite | K10 | Ham; eşik YORUM |
| 2 | Piyasa izni | K8 | Ham; uygulanamaz |
| 3 | Hisse rejimi | B §8 | etiket B §8'dedir; çarpan eşlemesi YORUM |
| 4 | Giriş | A §1; C §7 | kural eşiği YORUM |
| 5 | İlk stop | K2; C §7 | K2: Ham ve NotebookLM görseli (birinci el) |
| 6 | Lot | K1 | Ham ve NotebookLM görseli (birinci el); genel risk oranı ve yuvarlama YORUM |
| 7 | Acil çıkış | K2 | Ham ve NotebookLM görseli (birinci el) |
| 8 | Gün sonu çıkış | K3 | NotebookLM görseli (birinci el) ve Ham |
| 9 | Kısmi kâr | K5; C §7 | Ham; "%10" anlamı ve %50 paydası belirsiz |
| 10 | Hedef | C §4, §7, §11; B §21 | seviyeler formasyona göre |
| 11 | Stop taşıma | K4; C §11 | Ham (K4); formül YORUM |
| 12 | Önceki gün dibi | K4, K5 | Ham; payda açık değil |
| 13 | Geçersizlik | C §3, §10; A §9 | etiket sahip bölümlerdedir; ortak politika açık değil |
| 14 | Min R/R | K23; B §20 | Ham; stop R/R oranına göre belirlenir (K23); genel uygulama kapsamı açık değil |
| 15 | Günlük | K18 | Ham (URL'li tweet) |

Eksik (Tansu söylemedi), hepsi YORUM ile doldurulmalı ve YORUM etiketli kalmalı:

1. ATR periyodu ve yumuşatma türü (Wilder, SMA, EMA) ve zaman dilimi.
2. Stop kontrolü gün içi Low ile mi, kapanışla mı (acil: gün içi; SMA250: kapanış; harmonik: belirtilmedi).
3. Boşlukta dolum modeli (açılış/stop fiyatı).
4. Aynı gün stop ve hedef çatışması.
5. Birden fazla açık pozisyonda toplam risk sınırı ve korelasyon.
6. TP1 "%10" kimliği; TP2 miktarı; %50 paydası.
7. Trailing aktivasyonunun High/Close bazı, ATR zamanı ve dolum ayrıntıları (Chandelier k çarpanı kaynak kuralı değildir).
8. Kâr hedefi için sabit ATR çarpanı yok; Ham'da "Hedef" diye yazılan giriş + 1,5 ATR eşiği iz süren moda geçiş eşiğidir (K4; statik ve dinamik biçim, Ham metni dinamiği önerir). "4 ATR hedef" 05.10 ön denemesinin kararıydı; kaldırıldı, güncel karar: varsayılan kuralda hedef yok; EMA ailesinin hedefi varyantlardadır (TASARIM §5.5, KURALLAR §3; bilet 04, 14.10).
9. EMA50 çıkışı kaynak kuralı değildir (05.10 ön denemesinin kararıydı; kaldırıldı). NotebookLM örneği SMA250 altında kapanışta çıkışı gösterir; ortalama seçimi okura aittir (Ham, G115:20; NotebookLM, g1). Projenin gün sonu stopu ile harmonik bozulma ayrıdır.
10. Zaman stopu: Tansu'da yalnız "tepki penceresi" (10 gün/20 bar) var; pozisyon zaman stopu yok.
11. Komisyon ve kayma varsayımı.
12. Short taraf için hiçbir ATR kuralı verilmedi (yalnız not "short için tersi").
13. Açık noktalar: (i) TP1 AD×0,382 (eğitim) ve 1:1 R/R (SAYAS) için genel seçim. (ii) Stop/R:R sırasının strateji kapsamı. (iii) Fırsat anlatısı işlem tetiği veya şok frenine istisna vermez. (iv) 10 gün ile 20 barın ortak politikası.

Bizim kanıt kapımız: Bu paketin hiçbir parçası için Tansu'nun gerçek işlem sonucu veya tam örneklemli backtest'i yok. Yalnız tek hisse ve seçilmiş örnekler var (sonuç sayıları sahibinde: SMRTG/ISKPL sayımı C §5; makine öğrenmesi sayımı E K24).

# (b) Tansu'nun değerlendirme ilkeleri: bizim backtest için kontrol listesi

Kaynak numaraları ilgili K bölümleridir. Kaynak türü (Ham, ikinci el, YORUM) ilgili K bölümünde yazılıdır.

Grup 1. Ölçüm (K19)
- [ ] Kazanma oranını tek ölçüt yapma. Beklenti (R cinsinden), payoff ve profit factor raporla.
- [ ] Net kâr ve maksimum drawdown'u birlikte oku. MDD tüm equity eğrisinin zirveden dibe kaybıdır.
- [ ] Kümülatif sermaye eğrisini çiz ve incele (derinlik, süre, düz dönemler).
- [ ] Sistemleri diğer göstergelerin erimeleriyle kıyasla; şiddetli erimeli modeli ele (Ham). YORUM: aynı koşul (evren, dönem, maliyet, risk düzeyi) bizim ekimizdir.
- [ ] Karmaşık metrik (Sharpe vb.) eğri incelemesinin yerine geçmez.

Grup 2. Adaylar ve filtreler (K18)
- [ ] Her adayı 1, 3 ve 5 işlem günü sonrası ölç (gün tanımı: işlem günü, YORUM).
- [ ] Filtre ablation: her filtreyi tek tek çıkar, katkıyı ölç. Katkısız filtreyi at.
- [ ] Retest beklemenin etkisini ölç (getiri ve girişin gecikmesi).
- [ ] Giriş oluşmayan adayları da tut (YORUM, notun Cevo sentezi).
- [ ] İşlem günlüğü alanlarını doldur: aday tarihi, giriş, gerekçe, invalidation, TP, sonuç, MFE, MAE.

Grup 3. Risk (K1-K5, K23, G-118)
- [ ] Lot stop mesafesinden hesaplanır; %1 (G-115 Ham) ve 2 ATR (NotebookLM görseli) paylaşılan örnektir, genel risk oranı seçimi YORUM'dur (NotebookLM, G115/g1).
- [ ] Aileye özgü çıkış ve risk yöntemini raporla. YORUM: bu kontrol listesinde ayrı stop kullanımı aranır; rotasyon grafiği genel stop politikasını açıklamaz (Ham, G125:20; Araç, kaynak-vakbn-garan-rotasyon-2096358189696520213 görsel 2; Eğitim, G118/g1). İstisna: seçilmiş çift rotasyonu bölmesi stopsuzdur, çıkışı karşı uçta geçiştir (TASARIM §5.5–5.6; KURALLAR §3); bu madde o bölmeye uygulanmaz. (bilet 04, 14.10)
- [ ] Planlanan kayıp ve gerçekleşen kaybı kıyasla (boşluk etkisi).
- [ ] Stop seviyesini R/R oranına göre belirle: "her zaman bu orana göre belirleyin" (Ham, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:49; eşik B §20); bütün sistemlerde ortak Tansu sırası olduğu söylenmemiştir (G123:42–49).
- [ ] Plana sadakat: kural dışı çıkış/giriş yok.

Grup 4. Doğruluk ve baz oran (K24, K20)
- [ ] Küçük örneklemde güven aralığı ver (13 örnek = %42-87 gibi).
- [ ] Baz oran ve sinyal dağılımı raporla (13/14 SAT örneği).
- [ ] Strateji sonucunu B&H ile aynı risk düzeyinde kıyasla (G-59).
- [ ] Negatif sonucu yayımla (G-53: bağ kopabilir; "her fırsat çalışmaz").
- [ ] Parametreyi geçmişe uydurma. Fat tail ve ruin için Monte Carlo (yöntem YORUM).

Grup 5. Süreç (K21, K22)
- [ ] Önce denklem, sonra kod (kâğıt-kalem notu düşük güven).
- [ ] Backtest maliyet ve likiditeyi içerir (K22, K10).
- [ ] Backtestten sonra forward test (süre belirtilmedi).
- [ ] Fikri parayla değil kodla yanlışla (K21). Kural reddedilirse nedenini yaz (örnek: Williams short kolu, bizim sonucumuz).

Grup 6. Dil (K23)
- [ ] Çıktıda kesinlik dili yok: koşul, olasılık, invalidation, risk/ödül.

Uygulama sırası ve durumu: TASARIM §7 (K1–K3 tamamlandı).

---

## K34. Grid alım-satım: yüzde ızgarası ve ATR stop kodu

- Kaynak: `tweet-grid-alim-satim-atr-stop-loss-kodu-1839747420302831898` (27.09.2024; Ham; Tansu'nun X gönderisi; G1, G2 ve G3 açıldı).
- Tansu'nun ifadesi (verbatim): "Bu stratejiyi hiç kullanmadığım ve bir talep üzerine yazdığımdan çok detaya inmedim." Ham ayrıca geliştirmeyi okuyucuya bırakır: "Kurgu kimine basit gelebilir, geliştirmek sizin elinizde."
- Tanım (açılan kaynak kodunun okuması, YORUM):
  1. G1, her çubuk için yüksek-düşük aralığı ile önceki kapanıştan uzaklıkların en büyüğünü alır. ATR bu serinin basit hareketli ortalamasıdır: `atr = tr.rolling(self.atr_period).mean()`.
  2. Izgara başlangıç fiyatının altına eşit yüzde adımları koyar: `lower_price = self.initial_price * (1 - (self.grid_size / 100) * level)`. Döngü `range(price_levels)` ile sıfırdan başlar.
  3. G2, `if current_price <= price:` koşulunda alış mesajı yazar. Satış fiyatı: `sell_price = price * (1 + (self.grid_size / 100))`.
  4. Stop, güncel fiyat ile ATR üzerinden belirlenir: `self.stop_loss = current_price - (atr_value * self.atr_multiplier)`.
  5. Stop kontrolü: `if self.stop_loss and current_price < self.stop_loss:`. Bu koşulda kapanış mesajı yazılır. Eşitlik stop koşuluna dahil değildir.
  6. G3 bir aylık günlük verinin son kapanışını hem başlangıç hem güncel fiyat yapar. Izgara, alış ve stop kontrolünü bu tek fiyatla çağırır. Okuma (YORUM): Bu gösterim, canlı emir iletimi veya ardışık geçmiş işlem simülasyonu değildir.
- Parametreler (G3'teki örnek çağrı; genel kural seçimi değildir):

| parametre | örnek değer | kaynak |
|---|---|---|
| ızgara aralığı | %0,4 | `grid_size=0.4`, G3 açıldı |
| alış büyüklüğü | 50 lot | `position_size=50`, G3; G2 mesajında lot |
| ATR periyodu | 14 | `atr_period=14`, G3 açıldı |
| ATR yumuşatması | basit ortalama | `rolling(self.atr_period).mean()`, G1 açıldı |
| stop çarpanı | 2 | `atr_multiplier=2`, G3 açıldı |
| ızgara seviye sayısı | 10 | `bot.create_grid(10)`, G3 açıldı |
| veri | bir ay, günlük | G3, `period="1mo", interval="1d"` |

- Belirsiz kalanlar (YORUM): Kaynak örneği pozisyon kaydını, gerçekleşen satış dolumunu, aynı seviyenin tekrar alınmasını, sermaye sınırını ve işlem maliyetini tanımlayan bir işlem yaşam döngüsü sunmaz. Stop tek nesne alanıdır; birden çok alımın stop sahipliği açıklığa kavuşturulmadan uygulanamaz. Bunlar kaynak okumasının sınırlarıdır.
- Tansu'nun kanıtı: Ham, bu stratejiyi hiç kullanmadığını söyler. Görseller kod örneğidir; kaynakta bir işlem sonuç tablosu gösterilmez. Bu kodu çalıştırıp başarı sonucu ürettiğimiz iddia edilmez.
- Günlük bedava veriyle uygulanabilir mi: YORUM: ATR ve ızgara fiyatları günlük yüksek, düşük ve kapanışla hesaplanabilir. Gün içindeki seviye geçiş sırası ile gerçekleşen dolum, günlük veriden aynı kesinlikte çıkarılamaz. Tam işlem modeli için yukarıdaki açık noktalar gerekir.
- Kaynak güveni: Ham ve açılan üç kod görseli birinci eldir. Hesap ifadeleri açık, uygulama gösterim düzeyindedir. Hazırlık K.
