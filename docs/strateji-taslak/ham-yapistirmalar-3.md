# Tansu ham yapıştırmalar — 3. dosya: R245–R263 tweet metinleri ve görselleri (kaynaktan)

Bu dosyada R245–R263 kayıtlarının tweet metinleri ve görselleri vardır. `ham-yapistirmalar-2.md` bu kayıtlarda yalnız bağlantı taşıyordu. Metinler 06.10.2026 tarihinde `https://api.fxtwitter.com/The_Tansu_/status/<ID>` ham JSON çıktısındaki `tweet.text` alanından birebir alındı (yalnız R252 için bu uç nokta metni kesti; R252 `https://api.fxtwitter.com/2/thread/<ID>` uç noktasından alındı). Model özeti kullanılmadı. Görseller `tweet.media.all[].url` adresinden curl ile indirildi. Dosya yolları beyin klasörüne göredir: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`.

Tarihler API'deki `tweet.created_at` değeridir (UTC). Her kayıt başlığındaki tarih tweet tarihidir. Kayıt tarihi (R-numarasının yapıştırıldığı an) `ham-yapistirmalar-2.md` içinde kalır (06.09.2026 12:58–13:49 UTC).

Çekme sonucu: 20 tweet çekildi (19 kayıt; R260 iki tweet). Hata yok; silinmiş tweet yok. Beyin notu bulunan ve notu olmayan ayrımı: R254 ve R256 için de beyin notu bulundu (`kaynak-tansu-2095218573631279414.md`, `kaynak-tansu-2095201144544846208.md`). R246, R255, R256, R262 görselsizdir.

### R245 · 2026-09-06 12:51:59 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096582181170598078
- Beyin notu: `kaynak-aefes-yukselen-kanal-alt-bant-2096582181170598078.md`

> Hadi şunu vereyim
> Ne kadar çok rt o kadar çok formasyon:)
> #AEFES

Görseller:
- G1: https://pbs.twimg.com/media/HRiOTwUbQAA9WKw.png?name=orig · SHA-256 `c40435937c46a5a3d3b709c3c9586e85fd11d7827e6391ef9ad549dbe5a18c52` · `assets/kaynak-aefes-yukselen-kanal-alt-bant-2096582181170598078/01-aefes-yukselen-kanal.png`

### R246 · 2026-09-06 12:46:32 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096580811080261784
- Beyin notu: `kaynak-80-100-hafta-yatay-tarama-2096580811080261784.md`

> Aslında en temiz strateji bulacaksın 80-100 haftalık yatay giden bir hisse dibinde oturup bekleyeceksin. 
> Yazalım o zaman taramasını:)

Görseller: yok.

### R247 · 2026-09-06 12:33:23 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096577500612624410
- Beyin notu: `kaynak-dusen-yapi-retest-2096577500612624410.md`

> Şunu bir arakadaşa hediye edeyim
> Gider mi gitmez mi artık orası tahtacıya kalmış
> Güzer retest var

Görseller:
- G1: https://pbs.twimg.com/media/HRiKCaCXwAQEWho.jpg?name=orig · SHA-256 `27608f63d8dab1783698429d7596d5844f0fab6d48659beef083bc73989a0293` · `assets/kaynak-dusen-yapi-retest-2096577500612624410/01-dusen-ust-sinir-retest.jpg`

### R248 · 2026-09-06 12:27:32 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096576027791131079
- Beyin notu: `kaynak-dusen-yapi-kirilim-2096576027791131079.md`

> Canlanın:)

Görseller:
- G1: https://pbs.twimg.com/media/HRiIw1mawAAN4X-.jpg?name=orig · SHA-256 `a4a0b1e9c7333924520e9f82a5f2041529582b636a89fc120bd471a5ca0ca65e` · `assets/kaynak-dusen-yapi-kirilim-2096576027791131079/01-yesil-kirilim-mumu.jpg`

### R249 · 2026-09-06 08:06:26 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096510322190201208
- Beyin notu: `kaynak-three-drives-2096510322190201208.md`

> Strateji konuşalım
> 
> Three Drives Pattern, yani Üç İtiş Formasyonu, fiyatın trend yönünde art arda üç kez yeni bir ekstrem nokta üretmesiyle oluşan bir dönüş yapısıdır. Yükselen piyasada üç adet giderek yükselen tepe, düşen piyasada ise üç adet giderek düşen dip görülür. Ancak bu formasyonu sadece “üç tepe” ya da “üç dip” olarak görmek büyük hata olur. Three Drives’ın asıl değeri, fiyat hareketinin kendi içinde oluşturduğu Fibonacci, fiyat ve zaman simetrisidir.
> 
> Örneğin düşüş yönündeki bir Three Drives Buy yapısında önce Drive 1 adı verilen ilk dip oluşur. Ardından fiyat A noktasına doğru tepki verir. Daha sonra yeniden satış gelir ve Drive 2, Drive 1’in altında yeni bir dip oluşturur. Drive 2’den sonra C noktasına doğru ikinci tepki hareketi gelir. Son olarak fiyat tekrar aşağı hareket eder ve Drive 3, Drive 2’nin de altında üçüncü ve son dip olarak oluşur. Satış yönlü Three Drives yapısında ise bunun tam tersi görülür; her yeni tepe bir öncekinin üzerinde oluşur.
> 
> Burada önemli olan bu hareketlerin rastgele oluşmamasıdır. Drive 1 sonrasındaki A düzeltmesi ve Drive 2 sonrasındaki C düzeltmesi ideal olarak önceki hareketin yaklaşık yüzde 61,8 veya yüzde 78,6’sını geri almalıdır. Ardından Drive 2 ve Drive 3’ün, önceki düzeltme hareketlerinin yaklaşık 1,272 veya 1,618 Fibonacci extension seviyelerinde tamamlanması beklenir. Yani formasyonun hem geri çekilmelerinde hem de yeni ekstrem noktalarında Fibonacci ilişkisi vardır.
> 
> Three Drives’ın içinde aynı zamanda bir AB=CD mantığı da bulunur. A noktasından Drive 2’ye kadar gerçekleşen hareket ile C noktasından Drive 3’e kadar gerçekleşen hareket birbirine yakın büyüklükte olmalıdır. Bu bize fiyat simetrisini verir. Eğer ilk bacak ile ikinci bacak birbirinden tamamen farklıysa, grafikte üç tepe veya üç dip olsa bile yapı kaliteli bir Three Drives değildir.
> 
> Formasyondaki ikinci önemli unsur zaman simetrisidir. A’dan Drive 2’ye kadar geçen süre ile C’den Drive 3’e kadar geçen sürenin birbirine yakın olması beklenir. Biri 10 bar, diğeri 11-12 bar sürüyorsa yapı oldukça dengelidir. Fakat biri 8 bar, diğeri 30 bar sürüyorsa formasyonun görsel ve zamansal dengesi bozulur. Zaman sürelerinin mutlaka birebir aynı olması da gerekmez; Fibonacci zaman oranlarına yakınlık da kabul edilebilir.
> 
> Üçüncü önemli konu ise görsel simetridir. Three Drives grafiğe baktığınızda doğal görünmelidir. Hareketleri zorlayarak bir formasyon yaratmaya çalışıyorsanız büyük ihtimalle ortada gerçek bir Three Drives yoktur. Üç drive’ın büyüklüğü, aralarındaki düzeltmeler ve hareketlerin süreleri genel olarak birbirleriyle uyumlu olmalıdır. Bu formasyonun en önemli özelliklerinden biri de budur: matematiksel oranlarla görsel fiyat davranışı aynı noktada buluşur.
> 
> Three Drives’ın önemli olmasının nedeni, bize trendin giderek olgunlaştığını gösterebilmesidir. Fiyat üçüncü kez trend yönünde yeni bir ekstrem nokta üretirken, hareketin Fibonacci hedefleri, fiyat simetrisi ve zaman simetrisi de tamamlanıyorsa trendin son bölümüne yaklaşıyor olma ihtimali artar. Bu nedenle özellikle Drive 3 bölgesi önemli bir potential reversal zone, yani olası dönüş alanıdır.
> 
> Fakat burada çok önemli bir ayrım var. Drive 3 oluştu diye doğrudan ters yönde işlem açmak doğru değildir. Three Drives bize kesin dönüş değil, dönüş ihtimalinin yoğunlaştığı bir bölge verir. Özellikle trend çok güçlüyse fiyat 1,618 extension seviyesini aşabilir ve formasyon başarısız olabilir. Bu nedenle Drive 3 sonrasında fiyatın gerçekten reaksiyon verip vermediğini izlemek gerekir.
> 
> Benim açımdan Three Drives’ı değerli yapan şey tam olarak budur. Bu formasyon sadece bir şekil değildir. Market structure, Fibonacci, AB=CD, fiyat simetrisi ve zaman simetrisini tek bir yapının içinde birleştirir. Bu yüzden grafikte rastgele formasyon aramak yerine piyasanın kendi ritmini ölçmemizi sağlar.
> 
> Önce fiyatın gerçekten üç drive oluşturduğunu görürüz. Sonra Fibonacci ilişkilerini kontrol ederiz. Ardından fiyat ve zaman simetrisine bakarız. Bütün yapı aynı şeyi söylüyorsa Drive 3 bölgesini yakından takip ederiz. Formasyonu fiyatın üzerine zorla oturtmayız fiyatın bize gösterdiği yapıyı trade ederiz.

Görseller:
- G1: https://pbs.twimg.com/media/HRhMNlYbwAACrVs.png?name=orig · SHA-256 `e84c76cd682612bd82ac43c8c7c6e2932edd748c81e4af0d5711cecc0858e698` · `assets/kaynak-three-drives-2096510322190201208/01-three-drives.png`

### R250 · 2026-09-06 07:46:49 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096505383955079277
- Beyin notu: `kaynak-doas-kelebek-2096505383955079277.md`

> kelebeklerrrrr
> #doas

Görseller:
- G1: https://pbs.twimg.com/media/HRhIeAdbcAAL2_B.png?name=orig · SHA-256 `47302ccedee26cc7638ecced551ecfa4f9a36e82e9e7caef27c90c94f1f503b8` · `assets/kaynak-doas-kelebek-2096505383955079277/01-doas-kelebek.png`

### R251 · 2026-09-05 22:01:55 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096358189696520213
- Beyin notu: `kaynak-vakbn-garan-rotasyon-2096358189696520213.md`
- Tweetin metni boştur (yalnız iki görsel). Tweet, The_Tansu_ hesabının kendi tweetine yanıttır (`replying_to_status` 2096357339926311405).
- Üst tweet (2096357339926311405, 2026-09-05 21:58:32 UTC, The_Tansu_), birebir:

> Arbitraj hisselerini bu başlıkta paylaşıyorum.
> Toplanın :)

Görseller:
- G1: https://pbs.twimg.com/media/HRfClwkbMAA6Hb1.png?name=orig · SHA-256 `f027257388884b674bca7d66b595c7776eb1c68bed34d06d689145b67f8cbd90` · `assets/kaynak-vakbn-garan-rotasyon-2096358189696520213/01-vakbn-garan-rapor-1.png`
- G2: https://pbs.twimg.com/media/HRfCqHhXgAcah_D.jpg?name=orig · SHA-256 `53258f47d1594ac305aa1d8a51da7bd4ba5195478f511c1352b8f79bb2efe9ee` · `assets/kaynak-vakbn-garan-rotasyon-2096358189696520213/02-vakbn-garan-rapor-2.jpg`

### R252 · 2026-09-05 07:58:41 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2096145981062475910
- Beyin notu: `kaynak-xu100-corwin-schultz-2096145981062475910.md`

- Uyarı: `api.fxtwitter.com/The_Tansu_/status/<ID>` bu tweetin metnini yalnız ilk 272 karakter kadar döndürdü (`is_note_tweet` yanlışlıkla false). Tam metin (5266 karakter) `https://api.fxtwitter.com/2/thread/2096145981062475910` yanıtındaki `status.text` alanından alındı. Diğer 19 tweet için iki uç nokta aynı metni verdi (karşılaştırıldı).

> Yatırımcı gözüyle Corwin-Schultz modelini şöyle anlatayım, belki bir bakış açısı sağlar.
> 
> Corwin-Schultz, tahtanın gerçek emir defterini görmeden sadece günlük High ve Low fiyatlarını kullanarak hissenin yaklaşık alış-satış makasını, yani spread'ini tahmin etmeye çalışır. Kısacası şunu söyler
> 
> "Bu hissede alıcı ile satıcı birbirine ne kadar yakın, işlem yapmak ne kadar rahat veya pahalı?"
> 
> Spread düşükse genelde likidite daha iyidir. Alıcı ve satıcı birbirine daha yakındır, emirlerin daha sağlıklı gerçekleşme ihtimali yüksektir ve fiyat kayması riski daha düşüktür.
> 
> Spread yükseliyorsa tahta inceliyor olabilir. Alıcı ile satıcı arasındaki mesafe açılır, işlem maliyeti artar ve özellikle büyük emirlerde fiyat kayması riski yükselir.
> 
> Modelin Sigma kısmı ise başka bir şeyi anlatır. Fiyatın ne kadar sert hareket ettiğini, yani volatiliteyi tahmin eder.
> 
> Bu yüzden Spread ve Sigma'yı birlikte okumak daha anlamlıdır. 
> 
> Spread düşük, Sigma düşük: Likidite iyi, piyasa sakin. En rahat yapı.
> 
> Spread düşük, Sigma yüksek: Tahta likit ama fiyat savaşı sert. Güçlü hareket olabilir.
> 
> Spread yüksek, Sigma düşük: Fiyat sakin görünür ama tahta incelmiş olabilir. Gizli likidite riski vardır.
> 
> Spread yüksek, Sigma yüksek: Hem likidite bozuk hem hareket sert. En riskli yapı.
> 
> Bizim açımızdan en kritik nokta şudur. Corwin-Schultz hisse yükselecek mi düşecek mi demez. Sadece Hareketin kalitesini anlatır.
> 
> Örneğin fiyat yükselirken Spread düşüyorsa, yükseliş likidite bozulmadan gerçekleşiyor demektir ve bu daha sağlıklı bir yapıdır.
> 
> Ama fiyat yükselirken Spread de yükseliyorsa, fiyat yukarı gidiyor olsa bile hareket daha kırılgan olabilir.
> 
> Kısaca:
> 
> Fiyatin yönü söyler.
> Spread tahtanın sağlığını söyler.
> Sigma hareketin sertliğini söyler.
> 
> Ben bu modeli yatırımcı açısından daha çok bir işlem kalitesi ve likidite risk radarı olarak kullanmak daha faydalidir, tek başına al-sat göstergesi olarak değil.
> 
> XU100 Özelinde Güncel Durum
> 
> XU100'de güncel Spread yüzde 2,15 seviyesinde. Tarihsel ortalama ise yaklaşık yüzde 1,09. Yani alıcı ile satıcı arasındaki tahmini fiyat farkı şu anda normalden belirgin biçimde daha yüksek. Bu da piyasanın likidite açısından geçmişe göre daha zayıf bir bölgede bulunduğunu gösteriyor.
> 
> Sigma ise şu anda oldukça düşük seviyede. Bunun anlamı fiyat hareketlerinin son günlerde sakinleşmiş olmasıdır. Başka bir ifadeyle endeks çok sert hareket etmiyor fakat aynı anda Spread yüksek olduğu için işlem yapmak geçmişe göre daha rahat hale gelmiş değil.
> 
> Son iki günlük harekete baktığımızda Spread hızla yükselirken Sigma düşüyor. Yani fiyat sakinleşiyor fakat alıcı ile satıcı arasındaki makas açılıyor. Bu durum yatırımcı açısından önemlidir çünkü dışarıdan sakin görünen bir piyasanın altında likidite zayıflıyor olabilir.
> 
> Beş günlük daha yavaş ölçüm ise henüz farklı bir tablo gösteriyor. Bunun nedeni kısa dönem ortalamalarının yeni harekete daha geç tepki vermesidir. Bu yüzden son iki günlük hareket ile beş günlük görünümün farklı olması normaldir. Burada esas dikkat edilmesi gereken nokta, son günlerde yeni bir likidite bozulmasının başlayıp başlamadığıdır.
> 
> Fiyat tarafında XU100 son 20 işlem gününde yaklaşık yüzde 1,45 yükselmiş durumda. Ancak genel görünüm güçlü bir trendden çok yatay ve dalgalı bir yapıya işaret ediyor.
> 
> Spread ve Sigma Birlikte Ne Anlatıyor?
> 
> Şu anki yapı basitçe şöyle okunabilir. Fiyat hareketleri sakinleşiyor ama piyasanın likidite kalitesi zayıflıyor.
> Yani endeks çok sert hareket etmese bile alıcı ve satıcı arasındaki mesafe açılıyor. Bu nedenle düşük volatiliteyi tek başına olumlu kabul etmek doğru olmaz.
> 
> Piyasa Davranışı
> 
> Bu yapı yatırımcı için biraz yanıltıcı olabilir. Grafik sakin görünürken tahtadaki derinlik azalıyor olabilir. Böyle bir ortamda normalden büyük bir alış veya satış emri geldiğinde fiyat beklenenden daha hızlı hareket edebilir.
> 
> Dolayısıyla düşük Sigma, risk azaldı anlamına gelmez. Çünkü likidite tarafındaki bozulma devam ediyorsa piyasa dışarıdan sakin görünse bile kırılgan olabilir.
> 
> İşlem Açısından Anlamı
> 
> Şu anda asıl izlenmesi gereken gösterge Spread.
> 
> Spread yeniden tarihsel ortalamasına doğru gerilerse, piyasanın likidite tarafında rahatlama başladığını söylemek daha mümkün olur.
> 
> Spread yüksek kalmaya devam ederse, fiyat sakin görünse bile işlem sırasında fiyat kayması riski devam eder. Özellikle büyük pozisyonlarda istenen fiyattan işlem gerçekleştirmek zorlaşabilir.
> 
> Kısa Dönem Rejim Notu
> 
> Son iki günlük hareket ile beş günlük ortalamanın farklı şeyler söylemesi çelişki değildir. İki günlük ölçüm piyasadaki en yeni değişimi gösterirken beş günlük ölçüm daha yavaş hareket eder.
> 
> Bu nedenle son günlerde yeni bir likidite bozulması başlamış olabilir ve beş günlük ölçüm henüz bunu tam olarak yansıtmıyor olabilir.
> 
> XU100'de şu anda temel risk volatiliteden çok likidite tarafında görünüyor. Fiyat hareketleri sakinleşmiş olsa da Spread tarihsel olarak yüksek seviyede. Bu nedenle piyasanın daha sağlıklı hale geldiğini söylemek için yalnızca volatilitenin düşmesi yeterli değil. Daha olumlu bir tablo için Spread'in de yeniden daralmaya başlaması gerekir.
> 
> Fiyat sakin, ama piyasanın iç yapısı henüz tam rahat değil.
> 
> Bu yüzden yatırımcı açısından şu aşamada en önemli sinyal, Spread'in yeniden normal seviyelere dönüp dönmeyeceği. #XU100

Görseller:
- G1: https://pbs.twimg.com/media/HRb_x7YWYAA750T.png?name=orig · SHA-256 `8dc8df5761135f6cd207b48fc598d260684a2253153b8a728ec1c0f2ac3740f6` · `assets/kaynak-xu100-corwin-schultz-2096145981062475910/01-xu100-corwin-schultz.png`

### R253 · 2026-09-03 14:45:56 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2095523694881697974
- Beyin notu: `kaynak-akfis-breakout-fvg-retest-2095523694881697974.md`

> Dikkat edelim bu yapıya

Alıntılanan tweet (`tweet.quote`; metin R254 ile aynıdır):

> Breakout-->FVG-->Retest-->Confirmation
> Bu yapıları arayın

Görseller:
- G1: https://pbs.twimg.com/media/HRTLqJHaUAAn143.png?name=orig · SHA-256 `08486b0ed6ff9b1e0c0c1f86370d44b0a00472cd73687fb133841068a84bb390` · `assets/kaynak-akfis-breakout-fvg-retest-2095523694881697974/01-akfis-retest-teyit.png`
- Alıntılanan tweetin görseli: https://pbs.twimg.com/media/HRO2COUWcAExbdW.png?name=orig · SHA-256 `f4d224050d77a73c62c66a8bee0d3b5257f25c9319334e4d62697c278163d985` · `assets/kaynak-akfis-breakout-fvg-retest-2095523694881697974/02-alinti-breakout-fvg-retest-confirmation.png` (R254 G1 ile aynı dosya)

### R254 · 2026-09-02 18:33:29 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2095218573631279414
- Beyin notu: `kaynak-tansu-2095218573631279414.md` (görev metni R254/R256 için not yok demişti; not dosyası mevcut)

> Breakout-->FVG-->Retest-->Confirmation
> Bu yapıları arayın

Görseller:
- G1: https://pbs.twimg.com/media/HRO2COUWcAExbdW.png?name=orig · SHA-256 `f4d224050d77a73c62c66a8bee0d3b5257f25c9319334e4d62697c278163d985` · `assets/kaynak-tansu-2095218573631279414/01-breakout-fvg-retest-confirmation.png`

### R255 · 2026-09-02 18:13:18 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2095213493133713664
- Beyin notu: `not-backtest-giris-sadeligi-risk-islem-gunlugu.md`

> Not alın lazım olur.
> 
> Backtest yapın. Örneğin 26 Ağustos'ta hangi hisseleri aday seçtiniz sonraki 1, 3 ve 5 günde ne olmuş bakın. Böylece kurallarınızı gözünüzle doğrulayın.
> 
> Hangi aday tipi para kazandırıyor? Örneğin Daily iyi + 4H bullish CHoCH + RS güçlü + Demand/FVG desteği olanlar mı? Yoksa retest beklemek bizi fazla mı geciktiriyor? Bunu veriden çıkarın.
> 
> Giriş sistemini sadeleştirin. Her göstergenin aynı anda yeşil olması gerekmeyebilir. Market Structure ve fiyat davranışı ana motor olsun RSI, MACD, WaveTrend, RS gibi unsurlar yardımcı teyit olsun.
> 
> Risk yönetimini sistemin merkezine koyun. Bir setup ne kadar güzel olursa olsun tek işlemde büyük sermaye riske etmeyin. Pozisyon büyüklüğünü stop mesafesine göre hesaplayın.
> 
> İşlem günlüğü oluşturun. Aday tarihi → giriş → neden girdik → invalidation → TP → sonuç → maksimum olumlu/olumsuz hareket. Birkaç ay sonra kendi gerçek istatistiğiniz olsun.
> Sadece gerçekten çalışan yapıları tutun sistemde. Bir gösterge veya filtre sonuçlara katkı sağlamıyorsa sırf teknik görünmek için sistemde tutmayın.

Görseller: yok.

### R256 · 2026-09-02 17:24:14 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2095201144544846208
- Beyin notu: `kaynak-tansu-2095201144544846208.md` (görev metni R254/R256 için not yok demişti; not dosyası mevcut)

> Bir hisseyi incelerken benim ilk sorduğum soru “hangi indikatör AL diyor?” değildir. Asla ama asla bu hatayı yapmam
> 
> İlk sorum şudur:
> 
> Fiyat şu anda hangi yapının içinde ve alıcı mı satıcı mı kontrolü ele geçirmeye çalışıyor?
> 
> Bundan sonra fiyatın bulunduğu bölgeyi, kırılımları, likidite hareketlerini ve 4 saatlik teyidi incelerim.
> 
> Kendime bir analiz şablonu hazırladım, tıpkı bir iş prosedürü gibi, manuel analizlerde o şablonu izliyorum. Şablonu aynı zamanda koşullar ve sonuçlar ile koda da döktüm ve hangi koşulda hagi sonucun çıkabileceğinin açıklamalarını da yazdım,  kod da aynı sonuçları veriyor ama makine dilinde. İnanılmaz kolaylık.

Görseller: yok.

### R257 · 2026-09-02 17:05:51 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2095196517577461974
- Beyin notu: `kaynak-xu100-bekle-teyit-2095196517577461974.md`

> #xu100
> 
> Piyasanın mevcut görünümü, yeni bir yükseliş hareketinin başladığını söylemek için sağlıklı değil. Ana eğilim belirgin biçimde yukarı dönmüş değil piyasa daha çok yön arayışı ve geçiş süreci içerisinde bulunuyor. Son yükseliş denemesinin ardından üst bölgelerde satışla karşılaşılması ve fiyatın yeniden geri çekilmesi, alıcıların henüz kontrolü kalıcı biçimde ele geçiremediğini gösteriyor.
> 
> Kısa vadede aşağı yönlü baskı devam ediyor. Son geri çekilmede aşağıdaki likiditenin alınmasının ardından tepki görülmüş olması olumlu bir detay olsa da bu hareketi şimdilik yeni bir yükseliş trendinin başlangıcı olarak değerlendirmek doğru olmaz. Daha çok mevcut düşüşün ardından oluşabilecek geçici bir toparlanma ihtimali söz konusu. Bu nedenle piyasanın gerçekten yön değiştirdiğini kabul etmek için fiyatın yaklaşık 14.722 seviyesinin üzerine çıkması ve burada kalıcılık göstermesi gerekiyor.
> 
> Yukarı yönlü hareketin güç kazanması halinde ilk önemli sınav 14.740–14.876 bölgesi olacaktır. Bu alan aşılabilirse sırasıyla 14.868–14.992 ve ardından 15.133–15.205 bölgeleri gündeme gelebilir. Dolayısıyla 14.722 üzerindeki hareket tek başına nihai bir yükseliş teyidi değil; daha güçlü direnç bölgelerine doğru ilerleyebilmek için ilk önemli eşik olarak görülmelidir.
> 
> Aşağı tarafta ise piyasanın kırılganlığı devam ediyor. Özellikle 13.739 civarının altına doğru bir geri çekilme, mevcut toparlanma ihtimalini ciddi biçimde zayıflatacaktır. Daha aşağıda 13.000 civarı piyasanın önemli savunma alanlarından biri olmaya devam ediyor. Bu nedenle mevcut seviyelerde agresif biçimde yükseliş yönünde pozisyon almak yerine, fiyatın yukarı yönlü gücünü kanıtlamasını beklemek daha sağlıklı görünüyor.
> 
> Piyasanın genel havasında şu anda olağanüstü bir panik veya kriz fiyatlaması bulunmuyor. Ancak sakin bir ortam olması, piyasanın güçlü olduğu anlamına gelmiyor. Asıl problem, yükselişe katılımın zayıf olması. Kısa vadede geniş hisse grubuna bakıldığında düşüşe katılan şirket sayısının yükselişe katılanlardan belirgin biçimde fazla olduğu görülüyor. Bu durum, endekste zaman zaman tepki yükselişleri görülse bile piyasanın genelinde satış baskısının devam ettiğine işaret ediyor.
> 
> Daha geniş zaman perspektifinde görünüm kısa vadeye kıyasla biraz daha dengeli; ancak burada da güçlü ve yaygın bir yükseliş katılımı henüz oluşmuş değil. Yani piyasanın tamamının birlikte yukarı hareket ettiği sağlıklı bir yükseliş ortamından söz etmek için erken.
> 
> Sonuç olarak mevcut piyasa yapısı “AL” konumundan çok “BEKLE ve TEYİT ARA” konumundadır. Şu aşamada dip tahmini yapmaya çalışmak yerine, piyasanın yukarı yönlü iradesini göstermesi beklenmelidir. Yaklaşık 14.722 üzerindeki kalıcı hareket ilk olumlu sinyal olacaktır; 14.876–15.000 bölgesinin aşılması ise yükseliş senaryosunu çok daha güvenilir hale getirecektir. Bunlar gerçekleşmediği sürece görülecek yükselişlerin ana trend değişiminden ziyade tepki hareketi olma ihtimali daha yüksektir.
> 
> Ana mesaj ise piyasada büyük panik yok ancak güven de henüz oluşmuş değil. Risk almak için acele edilmemeli, nakit esnekliği korunmalı ve yeni pozisyonlar ancak fiyatın yukarı yönlü gücünü açık biçimde göstermesinden sonra artırılmalıdır.

Görseller:
- G1: https://pbs.twimg.com/media/HROgBUPbIAACA5b.png?name=orig · SHA-256 `d564cb12d242a90121c2bb463d5d9b53508f64142ae0ea914ebb13ccdce67f70` · `assets/kaynak-xu100-bekle-teyit-2095196517577461974/01-xu100-gorsel-1.png`
- G2: https://pbs.twimg.com/media/HROhW2qWUAQKebf.jpg?name=orig · SHA-256 `9e315915eece8b1d0df4666759d72d8fb896af1e10762aef726502b2c9d03175` · `assets/kaynak-xu100-bekle-teyit-2095196517577461974/02-xu100-gorsel-2.jpg`

### R258 · 2026-09-01 18:09:34 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2094850165920403866
- Beyin notu: `kaynak-xu100-1-eylul-2094850165920403866.md`

> #XU100
> 
> fiyat 14226.96, WMA21 14443.45 seviyesinin altında ve WMA aşağı eğimli. Bu nedenle kısa vadeli trend dönüşü henüz teyit edilmiş sayılmaz.
> 
> Satış momentumu hâlâ güçlü MACD histogramı negatif tarafta zayıflama göstermiyor.
> RSI 45.0 nötr bölgede.
> WaveTrend kısa vadede zayıf / negatif eğilim gösteriyor.
> Güçlü yükselen yapısal trend (7 temas) 2026-08-31 tarihinde yakın zamanda kapanışla kırılmış. 
> 
> Market structure geçiş/nötr aşamada yön teyidi bekleniyor. Fiyatın altında en yakın demand bölgesi 13633.00-13659.74. Düşüş trendinin döndüğüne dair henüz yeterli fiyat teyidi yok. İlk anlamlı olumlu gelişme WMA21'in (14443.45) geri alınması, ardından 14722.02 seviyesindeki son kısa vadeli tepenin kırılması olur. Yukarı hareket gelişirse 14230.73-14301.92 aktif Bearish FVG ilk direnç / likidite alanı olarak izlenmelidir. 14140.43 altına kalıcı geçiş, en yakın Bullish FVG desteğinin kaybedildiğini gösterir. Teknik uyum skoru 35/100 ve durum ZAYIF.

Görseller:
- G1: https://pbs.twimg.com/media/HRJmAlNWUAARq50.png?name=orig · SHA-256 `bbf80c54376ddf0cbb5e2d4e50b66ae1ba927c51ed663466decc8b8d007c2a2a` · `assets/kaynak-xu100-1-eylul-2094850165920403866/01-xu100-teknik-gorsel-1.png`
- G2: https://pbs.twimg.com/media/HRJmC7_XUAA_S5D.jpg?name=orig · SHA-256 `171d4bdeb0eb4af502c9cfa0d3ba7dcf1458457e4ea680eca0d90f17c33498c5` · `assets/kaynak-xu100-1-eylul-2094850165920403866/02-xu100-teknik-gorsel-2.jpg`

### R259 · 2026-08-31 18:06:11 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2094486927328059452
- Beyin notu: `kaynak-ahenk-demand-2094486927328059452.md`

> Ahengin uyumu
> Şunu biraz geliştirmenin önemine inandım şu an.

Görseller:
- G1: https://pbs.twimg.com/media/HREcsSbXcAIrWP_.jpg?name=orig · SHA-256 `5bd6db09e39883e65aca1c9fb1a443c84957f65c87cf7f051ae493cffd750a9d` · `assets/kaynak-ahenk-demand-2094486927328059452/01-ahengin-uyumu.jpg`

### R260 · 2026-08-30 19:42:12 UTC ve 19:42:13 UTC (iki tweet, ikincisi birincisine yanıt) · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet 1: https://x.com/The_Tansu_/status/2094148699769241961
- Tweet 2: https://x.com/The_Tansu_/status/2094148704089587805 (`replying_to_status` 2094148699769241961)
- Beyin notu: `kaynak-cwene-skewness-2094148699769241961.md`

Tweet 1 (2026-08-30 19:42:12 UTC):

> Skewness’i konuşalım ama bunu istatistiksel bir süs gibi değil, getiri dağılımının hangi tarafta kuyruk riski taşıdığını ölçen bir finans mühendisliği aracı olarak konuşalım.
> 
> Gaussian yani normal dağılımda skewness = 0’dır. Çünkü dağılım tamamen simetriktir. Ortalama, medyan ve mod aynı merkezdedir. Sağ ve sol kuyruk birbirinin aynasıdır. Finansal getirilerde ise çoğu zaman durum böyle değildir.
> 
> Skewness < 0 ise dağılımın sol kuyruğu daha uzundur. Yani küçük ve normal kazançların yanında zaman zaman çok büyük negatif hareketler oluşuyor olabilir. Bu, özellikle çoğu gün kazanıyor ama bir günde bütün kârı geri veriyor tipi stratejilerde önemlidir.
> 
> Skewness > 0 ise sağ kuyruk uzundur. Çoğu getiri küçük olabilir fakat zaman zaman büyük pozitif hareketler gelir. Trend-following ve momentum sistemlerinde görmek istediğimiz yapı çoğu zaman buna daha yakındır.
> 
> Örneğin iki hisse düşünün. İkisinin de ortalama günlük getirisi yüzde 0.10 ve volatilitesi yüzde 2 olsun. Sadece mean ve standard deviation kullanırsanız ikisini aynı risk yapısında görürsünüz. Fakat birinin skewness değeri -1.5, diğerinin +1.5 ise gerçekte iki dağılım tamamen farklıdır. Birincisinin riskinin büyük kısmı sol kuyrukta, diğerinin potansiyeli sağ kuyruktadır.
> 
> Finans mühendisliği burada başlıyor. Ben skewness'i tek başına AL/SAT sinyali olarak kullanmam. Volatilite, momentum, kurtosis ve tail-risk ile birlikte dağılım filtresi olarak kullanırım.
> 
> Mesela;
> 
> Momentum pozitif + Rolling Skewness pozitif ise hareket yalnızca yükselmiyor, dağılımın sağ kuyruğu da büyüyor olabilir. Bu trend stratejileri açısından olumlu bir kombinasyondur.
> 
> Momentum pozitif ama Skewness çok negatif ise fiyat yükselmesine rağmen dağılımın içinde sert aşağı hareket riski bulunuyor olabilir.
> 
> Daha da önemlisi klasik Gaussian VaR ile skewness düzeltilmiş VaR'ı karşılaştırabiliriz. Çünkü klasik normal dağılım yaklaşımı skewness'i sıfır varsayar. Gerçek dağılım negatif skew taşıyorsa klasik Gaussian model riski olduğundan küçük gösterebilir.
> 
> Kodumuz bunu doğrudan yapıyor. Hissenin log getirilerini hesaplıyor, Gaussian dağılımla karşılaştırıyor, skewness ve kurtosis ölçüyor, 63 günlük Rolling Skewness çıkarıyor ve klasik Gaussian VaR ile Cornish-Fisher Skewness/Kurtosis düzeltilmiş VaR hesaplıyor.

Görseller (tweet 1):
- G1: https://pbs.twimg.com/media/HQ_n4q5XIAEQC8j.png?name=orig · SHA-256 `20f956f8c78ffee8494a98ca4a83a747c61119fe0fdbe8ca1bf79267fcebe6d0` · `assets/kaynak-cwene-skewness-2094148699769241961/01-cwene-skewness-panel.png`

Tweet 2 (2026-08-30 19:42:13 UTC; görsel yok):

> Üstteki “Gerçek Getiri Dağılımı vs Gaussian” bölümünde mor sütunlar CWENE’nin gerçekleşmiş günlük getirileri, kırmızı eğri ise aynı ortalama ve volatiliteye sahip olsaydı getirilerin teorik Gaussian yani normal dağılımda nasıl görünmesi gerektiğini gösteriyor.
> 
> Burada önemli olan şu. CWENE’nin gerçek dağılımı kırmızı Gaussian eğriye tam oturmuyor. Gerçek getiriler sıfır çevresinde Gaussian’dan daha fazla yoğunlaşıyor ve uçlarda da olağan dışı hareketler mevcut. Yani piyasa normal dağılım kadar temiz ve simetrik davranmıyor. Finans mühendisliği açısından bunun anlamı şudur. Sadece standart sapmaya bakarak CWENE’nin riskini tarif etmek eksik kalabilir. Kuyruk hareketlerini de hesaba katmak gerekir.
> 
> Ortadaki grafik benim için asıl önemli bölüm: 63 günlük Rolling Skewness. Buradaki sıfır çizgisi Gaussian referansıdır. Skewness sıfıra yakınsa son 63 günlük getiriler yaklaşık simetriktir. Skewness +0.50'nin üzerine çıkıyorsa sağ kuyruk belirginleşmeye başlar. Yani normal günlük hareketlerin yanında zaman zaman olağan dışı güçlü pozitif getiriler geliyor demektir. Skewness -0.50'nin altına iniyorsa sol kuyruk belirginleşir. Yani zaman zaman olağan dışı büyük negatif getiriler görülmektedir.
> 
> CWENE açısından çok güzel bir örnek var.
> 
> 2024'ün ikinci yarısı ile 2025'in başlarında skewness yaklaşık +1 civarında. Bu dönemde dağılım güçlü şekilde pozitif skew taşıyor. Yani yukarı yönlü sıra dışı hareketlerin etkisi baskın.
> 
> Sonra 2025 baharında skewness bir anda yaklaşık -1 seviyesine düşüyor. Bu çok önemli bir rejim değişimidir. Dağılımın kuyruğu sağdan sola dönmüş. Yani o dönemde aşağı yönlü olağandışı getirilerin ağırlığı artmış.
> 
> Ardından 2025 yazında skewness tekrar sıfırın üzerine çıkıyor ve fiyat grafiğine bakarsan esas yükseliş hareketi de bundan sonra gelişmeye başlıyor.
> 
> Bu nedenle skewness'i fiyatla beraber kullanmak ilginç hale geliyor.
> 
> Alt grafik CWENE'nin fiyatı.
> 
> 2025 ortalarında fiyat yaklaşık 13–15 civarında dip yaptıktan sonra 20, 25, 30 ve sonunda 40'ın üzerine kadar yükseliyor. Aynı süreçte Rolling Skewness'in büyük negatif bölgeden çıkıp pozitife geçtiğini görüyoruz.
> 
> Ama burada çok önemli bir ayrım yapalım.Pozitif skewness = fiyat kesin yükselecek demek değildir.
> Skewness trend ölçmez. Skewness bize getiri dağılımındaki asimetrinin hangi yönde olduğunu söyler. 
> Dolayısıyla ben bunu yatırımcı olarak şöyle kullanırdım:
> Fiyat yükseliyor + momentum pozitif + skewness sıfırın üzerinde yükseliyor ise yükselişin içinde pozitif kuyruk davranışı oluşuyor olabilir. Bu benim için olumlu bir konfluens.
> 
> Fiyat yükseliyor fakat skewness hızla negatife dönüyorsa, fiyat grafiği hâlâ güzel görünmesine rağmen getirilerin altında negatif tail-risk oluşmaya başladığını düşünürüm.
> 
> Şimdi CWENE'nin bugünkü son kısmına bakarsak Rolling Skewness yaklaşık +0.2 / +0.3 civarında görünüyor.
> 
> Bu benim için NEGATİF DEĞİL,  olumlu. Ama +0.50'nin üzerinde değil → güçlü pozitif skew rejimi de değil.
> Yani şu anda dağılım hafif sağa çarpık. Olağanüstü güçlü bir “sağ kuyruk rejimi” henüz yok. Ben takip sisteminde bunu kabaca şöyle yorumlardım:
> 
> Skew < -0.50: Tail-risk negatif, dikkat.
> -0.50 < Skew < 0: Hafif negatif dağılım.
> 0 < Skew < +0.50: Hafif pozitif, yapıcı.
> Skew > +0.50: Belirgin pozitif sağ kuyruk.
> Skew > +1.00: Çok güçlü pozitif asimetri; fakat aynı zamanda birkaç büyük pozitif günün istatistiği bozup bozmadığını ayrıca kontrol etmek gerekir.
> 
> CWENE için şu anda benim okuyuşum şu olur:
> 
> Fiyat ana yükselişinden sonra düzeltme yaşamış. Rolling Skewness negatif bölgeden tekrar pozitif bölgeye geçmiş fakat henüz +0.50 eşiğini aşmamış. Bu nedenle dağılım tarafında bir iyileşme var, ancak henüz güçlü pozitif skew rejimi teyidi yok. Skewness +0.50 üzerine çıkarken fiyat da teknik dirençlerini kırmaya başlarsa iki farklı dünyadan aynı sinyali almış oluruz. fiyat yapısı yukarı, getiri dağılımı sağ kuyruğa dönüyor. İşte quant olarak benim ilgilendiğim konfluens bu olur.
> 
> Fiyat grafiği bize nereye gittiğimizi, skewness ise oraya giderken getirilerin hangi tarafta anormalleştiğini gösteriyor. Gaussian dağılımda skewness sıfırdır sağ ve sol risk simetriktir. Pozitif skewness sağ kuyruğun, negatif skewness ise sol kuyruğun ağırlaştığını söyler. Ben skewness'i tek başına AL/SAT göstergesi olarak değil, momentum ve fiyat trendinin dağılımsal kalitesini ölçmek için kullanıyorum. CWENE'de Rolling Skewness negatif bölgeden yeniden pozitife geçmiş durumda; bu iyileşme demek, fakat +0.50 üzerine çıkmadan güçlü pozitif skew rejiminden söz etmek için henüz erken.”
> 
> Bir de çok kritik bir nokta: Skewness'in yönü kadar değişimi de değerlidir. Mesela -1.0 → -0.5 → 0 → +0.3 → +0.6 şeklindeki bir dönüş, sadece “skewness bugün +0.6” bilgisinden çoğu zaman daha anlamlıdır. Çünkü burada aslında dağılım rejiminin dönüşünü yakalamaya çalışıyoruz.
> 
> Alın kullanın bunu.

### R261 · 2026-08-30 18:21:11 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2094128312729624792
- Beyin notu: `kaynak-cwene-dalga2-demand-2094128312729624792.md`

> #CWENE
> Elliott tarafında 33.10 → 48.30 Dalga 1, ardından 35 civarında 2? var. Demand & Supply grafiği de tam bu 35 civarının 32.5–36 bandındaki güçlü demand bölgesine denk geldiğini gösteriyor. Yani Elliott'un “2. dalga dibi olabilir” dediği yer, bağımsız olarak arz-talep açısından da mantıklı bir destek bölgesi. Son güçlü yeşil mum da bu bölgeden alıcı geldiğini gösteriyor.
> 
> Ben yatırımcı olarak seviyeleri şöyle okurum
> 
> 35–36: kritik destek üzerinde kaldıkça Dalga 2'nin bitmiş olma senaryosu canlı.
> 
> 37–38: hacim/denge bölgesi; bunun tekrar üstüne yerleşmesi olumlu.
> 
> 40–41.5: ilk ciddi kısa vadeli direnç. Burayı aşması hareketin güçlendiğini gösterir.
> 
> 44–48.5: güçlü supply bölgesi. Asıl mücadele burada.
> 48.30 üzeri kapanış: Elliott açısından Dalga 1 tepesi geri alınmış olur ve Dalga 3 senaryosu çok ciddi şekilde güçlenir.
> 
> 33.10 altı: mevcut bullish Elliott sayımı iptal.
> 
> Dolayısıyla benim gözümde şu anda “erken toplama bölgesinden tepki vermiş, fakat henüz ana kırılımı yapmamış hisse” görüntüsü var.
> 
> Agresif yatırımcı 35–36 demand bölgesinin korunmasını fırsat olarak görebilir ve 33.10'u yapısal risk seviyesi kabul eder. Daha muhafazakâr yatırımcı ise önce 40–41.5'in kırılmasını bekler.
> 
> En önemli nokta şu Elliott'taki 2? noktası ile Demand bölgesinin aynı yere denk gelmesi bence önemli bir konfluens. Bu nedenle 35 civarındaki dip artık tek başına bir Elliott pivotundan daha anlamlı. Ancak 48.30 kırılmadan “Dalga 3 başladı” demek için hâlâ erken.

Görseller:
- G1: https://pbs.twimg.com/media/HQ_VnLoWkAA89q_.png?name=orig · SHA-256 `2ee5a089d76781c5646717dcf6153ed4a1c428e933fcfa303287564abd832f09` · `assets/kaynak-cwene-dalga2-demand-2094128312729624792/01-cwene-elliott.png`
- G2: https://pbs.twimg.com/media/HQ_Vyy1WQAATHUP.jpg?name=orig · SHA-256 `f9d360a744e285253e6c3fccd9a24034da7bc31239f4d75e234fc11027097524` · `assets/kaynak-cwene-dalga2-demand-2094128312729624792/02-cwene-demand-supply.jpg`

### R262 · 2026-08-29 11:15:29 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2093658795700338821
- Beyin notu: `kaynak-kointegrasyon-sinirlari-2093658795700338821.md`

> Arbitraj Stratejilerinde Kointegrasyonun (Eşbütünleşme) Hayati Rolün Nedir?
> 
> Finansal piyasalarda arbitraj, geleneksel anlamıyla risksiz kâr elde etme amacı taşısa da, modern algoritmik trade'de daha çok "istatistiksel arbitraj" formunda karşımıza çıkar. İstatistiksel arbitrajın en popüler türlerinden biri olan ikili işlem (pairs trading) stratejilerinde başarının temel taşı, seçilen varlıklar arasındaki matematiksel ilişkidir. Bu noktada "kointegrasyon" (eşbütünleşme), sadece faydalı bir gösterge değil, stratejinin üzerine inşa edildiği zorunlu bir temel olarak öne çıkar.
> 
> Kointegrasyon Nedir ve Neden Korelasyondan Farklıdır?
> 
> Kointegrasyon, iki veya daha fazla rastgele yürüyüş (random walk) sergileyen zaman serisinin, doğrusal bir kombinasyonunun durağan (stationary) bir seri oluşturması durumudur. Finansal varlıkların fiyatları doğaları gereği durağan değildir zaman içinde trendler oluşturarak yukarı veya aşağı yönlü hareket ederler. Ancak kointegre olmuş iki varlığın fiyatları arasındaki "fark" veya "spread", sabit bir ortalama etrafında dalgalanma eğilimi gösterir.
> 
> Yatırımcıların sıklıkla düştüğü en büyük hata, korelasyon ile kointegrasyonu birbirine karıştırmaktır. Korelasyon, iki varlığın aynı yönde hareket etme eğilimini ölçer. Ancak korelasyon kısa vadeli bir ilişkidir ve zamanla bozulabilir. İki hisse senedi yüksek korelasyona sahip olsa bile, aralarındaki fiyat farkı zamanla sonsuza dek açılabilir.
> 
> Kointegrasyon ise görünmez bir ip gibidir. Klasik bir ekonometri analojisiyle korelasyon, aynı yöne doğru giden iki yabancıya benzerken, kointegrasyon tasmasıyla sahibine bağlı bir köpeğe benzer. Köpek sağa veya sola sapabilir, sahibi yavaşlayabilir (kısa vadede ayrışma), ancak uzun vadede aralarındaki mesafe (spread) tasmanın boyunu aşamaz ve eninde sonunda birbirlerine yaklaşırlar.
> 
> Kointegrasyonun Arbitrajdaki İşlevleri
> 
> Ortalamaya Dönüş (Mean Reversion) Mantığının İspatı: Kointegrasyon, iki varlığın fiyatları arasındaki farkın (spread) durağan olduğunu matematiksel olarak kanıtlar. Durağan bir serinin en temel özelliği, eninde sonunda kendi tarihsel ortalamasına dönmesidir. İkili arbitraj stratejisi tam olarak bu varsayımla çalışır: Spread tarihsel ortalamasından standart sapmalarla uzaklaştığında, pahalı olan varlık açığa satılır (short), ucuz olan varlık alınır (long). Kointegrasyon olmasaydı, spread'in ortalamaya döneceğine dair hiçbir istatistiksel güvence olmazdı.
> 
> Piyasa Riskinin İzole Edilmesi (Market Neutrality): Kointegre varlıklardan oluşan bir portföy, piyasanın genel yönünden bağımsız hale gelir. Örneğin, aynı sektörde faaliyet gösteren ve kointegre olan iki banka hissesi (Banka A ve Banka B) üzerinden yapılan bir işlemde, ekonomideki genel bir çöküş veya ani bir ralli her iki hisseyi de etkileyecektir. Yatırımcı birinde uzun, diğerinde kısa pozisyonda olduğu için bu makro şoklardan etkilenmez; sadece aralarındaki fiyat anomalisinin düzelmesinden kâr eder.
> 
> Sahte Sinyallerin Filtrelenmesi: Sadece fiyat hareketlerine veya korelasyona bakarak oluşturulan işlem çiftleri, yapısal kırılmalar karşısında yatırımcıyı terste bırakabilir. Johansen veya Engle-Granger gibi kointegrasyon testleri kullanılarak varlıklar arasındaki ilişkinin yapısal ve uzun vadeli olup olmadığı doğrulanır. Bu, rastgele veya geçici fiyat hareketlerinin "arbitraj fırsatı" olarak algılanmasının önüne geçer.
> 
> Sonuç olarak kointegrasyon, kaotik ve öngörülemez piyasa hareketleri içinde istatistiksel bir düzen bulma sanatıdır. Arbitraj modellerinde sadece fiyatların geçmişte nasıl hareket ettiğine bakmak yerine, varlıkların ekonomik temelleri ve piyasa dinamikleri arasındaki uzun vadeli bağın kointegrasyon testleriyle matematiksel olarak ispatlanması gerekir. Bu ispat olmadan uygulanan herhangi bir ikili işlem stratejisi, istatistiksel bir arbitraj olmaktan çıkıp, sıradan ve yüksek riskli bir yön tahminine dönüşür.

Görseller: yok.

### R263 · 2026-08-29 10:31:57 UTC · kaynak: api.fxtwitter.com (06.10.2026 çekildi)

- Tweet: https://x.com/The_Tansu_/status/2093647837162553475
- Beyin notu: `kaynak-bom-iki-tavan-2093647837162553475.md`

> BOM sinyalinin geldiği yerde şartlar da müsait ise çok etkili olabileceğine dair ilk kanıtlar gelmeye başladı
> 2 tavan üst üste vermiş tabi hala geliştirilmeye açık bir sistem. Çalışıyoruz bakalım

Görseller:
- G1: https://pbs.twimg.com/media/HQ4hgE1WoAEcNtb.jpg?name=orig · SHA-256 `544f3a0f11aecff0d8fc848808571baa75c823a855a40bfbc2191c2b48b48460` · `assets/kaynak-bom-iki-tavan-2093647837162553475/01-bom-sinyal.jpg`
