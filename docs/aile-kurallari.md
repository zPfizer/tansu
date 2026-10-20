# Aile kuralları

Okuma kuralları (birinci el, ikinci el, NotebookLM ve YORUM tanımları: GLOSSARY):
- Kuralın dayanağı notun Ham metni ve görselleridir (NotebookLM görselleri dahil). Ham dışı metinle çelişkide görsel geçerlidir.
- Ham dışı bölümler (Sentez, Cevo çıkarımı, Kaynak kartı, Teknik Ek) ikinci eldir; tek başına kural dayanağı olmaz.
  "NotebookLM görseli" etiketi yalnız bilgi verir.
- Eski resmi sayımda bir YORUM'un sınamada denenen her değeri yeni deneme sayılır; istisna: önceden yazılmış sağlamlık ızgarasının
  hücreleri ve masraf senaryoları deneme sayısına girmez (TASARIM 5.10, 5.11; İ: 09-056). Sadakat kontrolünde denenen
  aday formüller deneme sayısına girmez, p üretmez; seçilen formül kural kaydına girer (TASARIM 5.11, İ: 10-033, 04-090).
- Yeni motorun revizyon kaydı, resmi sayımdan ayrıdır; sahibi TASARIM §5.15'tir. Aşağıdaki mevcut aile tanımları legacy olarak korunur; panelde izinli tam bileşim kanıtı aynı bölümün BİLEŞİM kapısındadır (Levent 18.10: "Tabii önce Tansu sonra internet."; [DVC kullanıcı kılavuzu](https://doc.dvc.org/user-guide), araştırmada erişim 18.10.2026; S01 YORUM kayıt sınırı).

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
4. 05.10 ön denemesindeki "4 ATR hedef" ve "EMA50 altı çıkış" Tansu kaynaklarında yok; kaldırılır.

## 3. Seçim

**Ölçütler (seçimden önce yazıldı):**
1. Giriş kuralının çekirdeği birinci elden belli.
2. Bedava günlük veriyle uygulanabilir.
3. Tansu sayısal bir sonuç göstermiş (sınanacak bir iddia var).
4. Aynı fikri iki kez sınamamak için farklı türde aileler seçilir.

**İlk sürümde sınanacak aileler:**
| Sıra | Aile | Neden | En önemli YORUM |
|---|---|---|---|
| 1 | Çift rotasyonu | 4 ölçütün hepsi; sayısal çıktısı var (VAKBN–GARAN raporu, §4) | sapma formülü ve pencere |
| 2 | EMA sıkışması | parametreler birinci el; oran formülü sadakatle seçildi (YORUM, aşağıda) | giriş tetiği |

Sürüm kapsamı: TASARIM §3. AB=CD ilk sürümde yoktur (TASARIM §3, Sorgu 3); ikinci dalgada geometri sadakati yönsüz yapılır (bilet 04, 14.10).

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
2. **EMA sıkışması kırılımı**. Tansu genel sıkışma parametresi vermez; %1,2 ve 3 gün örnek ayarıdır (B §1).
   gorsel-paket-65 Ham'daki "Bir günde %5 Ema sıkışması" belirsizdir. Ailenin getiri iddiası bizim hipotezimizdir (İ: 10-002).
   - Oran: (en büyük EMA − en küçük EMA) / EMA200; EMA20/50/100/200, `ewm(adjust=False)`. Formül görselde yok (B §1); sadakat
     kontrolüyle KRDMD örneğinde eşleşti, KRDMD dışında doğrulanmadı (YORUM, §4; düşüş trendinde paydanın EMA200 mü
     en küçük EMA mı olduğu açıktır, TASARIM §8 madde 6; bilet 04, 14.10).
   - Sıkışma dönemi: oranın ≤ %1,2 olduğu art arda en az 3 gün; oranın eşiği aştığı ilk gün dönemi
     bitirir. Tansu'nun %1,2 ve 3 günü "örnekteki değer"dir.
   - Giriş (`bugun`, varsayılan; YORUM): dönem bitiminden sonraki 10 gün içinde kapanış, dönemin en yüksek gün yükseğini
     aşarsa ertesi gün girilir. Dönem başına tek giriş vardır. Stop ve çıkış risk paketidir (TASARIM §5.5); hedef yoktur.
   - Not: Tansu'nun ICBCT "Pre Signal"i sıkışma sürerken çıkar (B §2); bizim tetik bitişten sonradır (YORUM).
   - **Modül 1** (Levent 16.10: kendi giriş, çıkış, risk ve piyasa kuralı olan strateji; hiçbir parçası kodda eksik kalmaz).
     Tansu = Ham metninden alıntı; YORUM = bizim seçim. Aksi yazılmadıkça sayılar ve tanımlar YORUM'dur.
     Varsayılan `bugun`, yukarıdaki Giriş kuralıdır; diğer kurallar aşağıdaki varyantlardır.
     - **Kutu.** Tansu: "EMA sıkışmasının olduğu Talep Bölgesinin (Yeşil Kutu)"
       (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham). YORUM: kutu sıkışma dönemidir; alt sınır dönemin en düşük düşüğüdür.
       Üst sınırı `kutu_ust` seçer: `yuksek` (varsayılan girişe uygun, dönemin en yüksek gün yüksekliği) ya da `govde`.
       Tansu konsolidasyon kutusunda gövde ve fitil uçlarını kullanır (A §14). Tansu: "En yüksek mumun gövdesinin
       bittiği yer ile, en düşük mumun gölgesinin bittiği yer." (`gorsel-paket-18-konsolidasyon-body-wick`, Ham).
       `govde`'de üst sınır, dönemde gün yüksekliği en büyük olan günün gövde ucudur (YORUM: "en yüksek mum" =
       yüksekliği en büyük gün; eşitlikte ilk gün). Açılış olmadığı için gövde ucu = max(önceki kapanış, kapanış)
       (YORUM; bölgelerdeki vekil ölçü). Önceki kapanış serinin önceki günüdür; dönemden önce olabilir.
       Serinin ilk gününde gövde ucu kapanıştır (YORUM: önceki kapanış yoktur; bölgeler de aynı vekil ölçüyü kullanır).
       Üst sınır giriş tetiğini, `retest` seviyesini ve `kutu_ust` sütununu değiştirir; alt sınır değişmez.
     - **Sıkışma.** Tansu: "EMA'ların (örneğin EMA 20, 50, 100) birbirinin içine geçtiğini ve "düzleştiğini" gör."
       (`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127`, Ham). Oran şartı bu cümleyi karşılar; ayrı eğim
       süzgeci yoktur (YORUM: cümle sayı vermez; ölçülmedi).
     - **Giriş türü** (`giris`). Ortak pencere dönem bitişinden sonraki 10 gündür (YORUM; bugünkü kural).
       Gerekli ve yeterli adaylık şartları: tetik, bütün süzgeçler, kapanış ≥ SMA250 ve ısınma o gün sağlanır. Penceredeki ilk aday sinyaldir; dönem başına tektir.
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
         süzgecidir. Ortak giriş penceresi uygulanır.
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
         ("negatif büyüyor" okuması YORUM). TradingView'den yalnız formül alınır; veri kullanılmaz (TASARIM §4).
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
         / (+DI + −DI); +DI + −DI = 0 ise DX = 0 (YORUM: yönlü hareket yoksa trend yoktur; TA-Lib kuralı).
         Bu durum ATR = 0 olan düz ya da durdurulmuş hisseyi de kapsar. ADX, DX'in 14 günlük Wilder ortalamasıdır;
         hesaplanamayan gün aday değildir (Eksik değer).
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
         Tansu: "Eğer fiyat bu kutunun altına sarkar ve kapanış yaparsa, analiz
         iptal olur" (aynı not, Ham). `stop` = `kutu` iken, sıkışma dönemi bittikten sonra ve aday günden önce herhangi
         bir günün kapanışı kutu altının altındaysa (kapanış < kutu alt) o dönemden sinyal çıkmaz. `retest` için dönem
         bitişinden j gününe kadar bakılır; k ile j arası dahildir. Kapsam YORUM'dur: kural yalnız kutu stopunda
         uygulanır; `atr2`, `atr15` ve bugünkü kural değişmez. Dönem bitişi olmayan `agresif` girişte bu kural uygulanmaz (YORUM).
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
         ise stop = max(stop, giriş + (n − 2) × ATR_sinyal). n = 2'de stop giriştir, n = 3'te 1 ATR'dir.
         ATR_sinyal = 0 ise (fiyatı 14 gün kıpırdamayan hisse) n tanımsızdır; merdiven basamağı yoktur, öbür kurallar uygulanır (YORUM).
         ATR sinyal gününündür (YORUM: E K25'in giriş günü ATR'si giriş AOF'undan önce bilinmez).
         Eşik karşılaştırmaları (n, `atr3`, `dip` etkinliği, başabaş) 9 ondalığa yuvarlanır; kayan nokta hatası basamağı düşürmesin diye (YORUM).
       - Başabaş çıkışı (E K32). Tansu: "Eğer kârlı bölgeye geçtikten sonra fiyat geri dönerek tekrar tam olarak giriş
         fiyatınıza ulaşırsa, derhal pozisyondan çıkmanız gerekir."
         (`tweet-under30-over30-1-5r-basabas-cikis-1992547498343161903`, Ham). R tanımı: TASARIM §5.3 "İşlem günlüğü".
         Yüksek ≥ giriş + 1,5 × R ise stop = max(stop, giriş). Aktivasyon fiyat alanı olarak gün yüksekliği YORUM'dur (E K32).
       - İz süren stop başlangıcı (YORUM). Tansu: "pozisyonun risk/ödül oranı hedefine ulaştığında Trailing Stop (TS) ve kâr
         alma kuralları devreye girer" (`tweet-rsi30-giris-iki-asamali-cikis`, Ham; Ham'da yazar yok). Not sayı vermez.
         Başlangıçlar yukarıdaki ATR merdiveni ve başabaş maddelerindedir. Statik ya da dinamik iz süren stop seçimi (E K4) Levent'e kalır; değiştirilmez.
       - Yarı satış tek seferdir; pozisyonun yarısı satılır, kalanı öbür kurallarla çıkar. Kuralı `cikis` seçer.
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
           RSI70 yarı satışı için girişten sonraki bir u gününde (giriş günü hariç; YORUM) u ≤ t−1, kapanış_u > giriş fiyatı ve
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
       değerleridir ve karşılaştırma tabanıdır. Her varyant ayrı kural
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

İkinci dalga ve kapsam dışı kurallar: TASARIM §3. Diğerleri dizinde kalır; kaynak çıktıkça yükselir.

"Ertesi gün" sınamada nasıl modellendiği (Tansu'nun T+1 açılışı uygulanamaz): TASARIM 5.3.

**Risk paketi:** TASARIM §5.5–5.6; kaynaklar E K1–K3. Çift rotasyonu bu pakete tabi değildir; karşı uçta geçişle çıkar (aile 1).

## 4. Sadakat kontrolü (sınamadan önce)

Sadakat kontrolünde getiri sonuçlarına bakılmaz. YORUM'ları sonuca bakarak seçmek yasak.
Tansu'nun **kendi çıktılarındaki rakamları** yeniden üretmek serbesttir; bu performans değil, kural okumasının kanıtıdır.

| Aile | Tansu çıktısı | Hedef değerler (sahibi) | Bu neyi çözer |
|---|---|---|---|
| Çift rotasyonu | VAKBN–GARAN raporu | D, "Tansu'nun kanıtı" ve "Çift sistemi çekirdeği" | sapma formülü ve pencere |
| EMA sıkışması | KRDMD | B §1 | oran formülü |
| AB=CD (ikinci dalga) | KRPLS, MARKA #13, SMRTG tablosu | C §3, §5 | pivot ayarı, yön |
| Kanal (ikinci dalga) | AEFES 03.09.2026 | A §2 | kanal çizim yöntemi |

Ölçümler, aday sayıları ve toleranslar: `docs/sadakat.md`; Sorgu 3 ölçümü: `docs/sorgu/sonuc-3-4.md`. Burada kararlar durur.
- **EMA sıkışması çözüldü** yalnız KRDMD örneğinde; dışında doğrulanmadı. Oran formülü: §3 aile 2.
  İş Yatırım ham serisinde EMA200 sıkı toleransı geçmez (bilet 05); sonuç **gevşek bantla üretildi**.
  EMA200 uzun belleklidir ve Tansu'nun veri başlangıcı bilinmez. Seçilen "son 3 yıl" başlangıcı sınamada sabit tutulur ve rapora yazılır; formül değişmez (İ: 06-014).
- **Çift Z'si üretilemedi:** Sorgu 3, bilet 06 ve 10.10.2026 ek turu; aday listesi koşudan önce commit edildi (bf79a28).
  Karar: **YORUM kalıcıdır** (log oran, 60 gün); yeni tur açılmaz. Beta, korelasyon, piyasada kalma ve Mart–Mayıs 2025 kontrolleri formül olmadığı için yapılmadı. Fiyat serisi: TASARIM 5.1.

Veri: Kontrol İş Yatırım ham seriyle yapılır (TASARIM 5.1). Yahoo ölçümü: `docs/sorgu/sonuc-3-4.md` O9.

Kural:
- Tolerans, adaylar denenmeden önce yazılır. "Üretti" = Tansu'nun gösterdiği son hanenin yarısı içinde
  (Z için ±0,0005). Gevşek bant (±0,05) yalnız tek aday kalırsa kullanılır. (İ: 04-002, 14-058)
  Aynı dönemi ve gün sayısını veren, ölçülen her değeri (ortalama, EMA'lar) birbirinden en çok `docs/sadakat.md` başındaki
  toleransla (gösterilen son hanenin yarısı, ±0,005) ayrılan adaylar eşdeğerdir ve tek aday sayılır. EMA'da son 3 yıl ve son
  2 yıl böyledir; ölçülen değerler `docs/sadakat.md` EMA tablosundadır. (bilet 05, 14.10)
- Birden çok aday formülden, ölçülen değerlerin Tansu'nun rakamlarına mutlak farkları toplamı en küçük olan seçilir.
  Eşitlikte aday sırasındaki ilk aday alınır (bilet 07a, 14.10). Çift Z'si adaylarına standart sapmanın ddof'u {0; 1} de girer (İ: 19-028).
- Rapor tarihi bilinmiyorsa (Z_t, Z_{t−1}) çifti bütün işlem günlerinde aranır; eşleşen günler yazılır.
  (İ: 04-003)
- Hiçbiri üretemezse YORUM olarak kalır ve raporda yazılır.
- Sonuç `docs/sadakat.md`'ye yazılır; `python -m tansu sadakat` aynı rakamları yeniden üretir. (İ: 11-023)

## 5. Bilinen riskler
- Tansu'nun örnek çiftleri ve hisseleri sonuca bakılarak seçilmiş olabilir. Bu yüzden çift rotasyonu
  yalnız onun çiftlerinde değil, önceden yazılmış bir kuralla seçilen bütün çiftlerde sınanır
  (aynı sektör: YORUM, TASARIM 5.6; oluşum penceresinde eşbütünleşme). Onun çiftleri ayrıca gösterilir. AGROT–GARAN
  rotasyon değildir (iki bacak + nakit) ve borsapy'ye göre farklı sektördedir (bizim veri: borsapy; Tansu iddiası değil).
- NotebookLM görselleri birinci eldir (GLOSSARY); Tansu'nun kendi kuralı olmayabilir.
