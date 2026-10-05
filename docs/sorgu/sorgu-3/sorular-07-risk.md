# Sorular 07: Risk, çıkış, dolum

Dal: risk paketi, çıkışlar, dolum modeli, Adım ve Motor. Kaynaklar: TASARIM taslak 5, KURALLAR, GLOSSARY, `kurallar/E-risk-cikis-surec.md`, `sorgu-2.md`.

## A. Pozisyon büyüklüğü (%1 risk)

07-001. TASARIM 5.6 tek pozisyonu sermayenin %10'u ile sınırlarken 5.5 lotu %1 / 2 ATR ile hesaplar; 2 ATR fiyatın %10'undan küçük olduğunda %10 tavanı bağlayıcı olur ve gerçek risk %1'in altında kalır. İşlemlerin hangi oranında %1 kuralı, hangi oranında tavan belirleyici olacak ve bu rapora yazılacak mı?

07-002. BIST100 hisselerinde tipik 2 ATR / fiyat oranı %10'un altındaysa "%1 risk" fiilen "%10 pozisyon" demektir; bu durumda Tansu'nun risk paketi (E-K1) sınanmış sayılır mı, yoksa sabit boyutlu bir portföy mü sınanmış olur?

07-003. TASARIM 5.5 "adet = risk / 2ATR" der ama "risk" yüzdesinin başlangıç sermayesine mi, o günkü özkaynağa mı, o günkü boş nakde mi uygulandığını yazmaz; E-K1 bu noktayı "belirsiz" bırakmıştı. Hangisi seçildi ve getiri bileşikleşmesine etkisi nerede gösterilecek?

07-004. TASARIM 5.6 sermayeyi 1.000.000 TL olarak sabit yazar; 2015–2026 arasında TL'nin değeri ve hisse işlem hacimleri kat kat değiştiği için aynı nominal tutar 2015'te büyük, 2026'da küçük bir pozisyon demektir. 5.4'teki %2 likidite sınırı bu yüzden yıllara göre farklı sıklıkta bağlamayacak mı?

07-005. E-K1'deki Tansu örneğinde 1000 / 14,30 = 69,93 iken "~70 hisse" yazılıdır ve 70 lot riski %1'in üstüne çıkarır; TASARIM lotun aşağı mı yukarı mı yuvarlanacağını hiçbir yerde yazmıyor. Motor sınamaları (5.3) bu yuvarlamayı kapsıyor mu?

07-006. Lot hesabı sinyal günü ATR'sine ve sinyal günü kapanışına göre yapılıyorsa, giriş ertesi günün AOF'unda gerçekleştiğinde (5.3) gerçekleşen risk %1'den sapar. Sapma hangi aşamada düzeltilir, düzeltilmezse ölçülen "R" ile planlanan "R" arasındaki fark raporlanacak mı?

07-007. %1 riskin hesabında giriş ve çıkış masrafı (5.4, her yönde %0,3) paydaya katılıyor mu? Katılmıyorsa, 2 ATR çok dar olan düşük oynaklıklı hissede masraf riskin büyük bölümünü oluşturmaz mı?

07-008. Ucuz hisselerde (örneğin 3 TL altı) fiyat adımı (tick) 2 ATR'nin kayda değer bir kısmı olabilir; stop seviyesi ve ATR fiyat adımına yuvarlanıyor mu, yoksa sürekli fiyat varsayımıyla mı hesaplanıyor?

07-009. Aynı gün birden çok sinyal gelip boş yer yetmediğinde "en likit önce" (5.6, M12) denir; en likit hisseyi seçmek büyük şirketlere sistematik eğilim yaratır ve 5.4'teki %2 likidite sınırını gevşetir. Likitlik hangi pencerenin medyanıyla ölçülüyor: 10 gün (5.4), 60 gün (5.2)?

07-010. Sermayenin %1'i risk, en çok 10 pozisyon: aynı sektörde (örneğin bankalar) aynı gün açılan 10 pozisyon birlikte stop olursa gerçek kayıp %10'a yaklaşır. Toplam açık risk veya korelasyon sınırı yokluğu (E-K1 "belirsiz kalanlar") kabul ölçütündeki %25 düşüş kuralını (5.12) nasıl etkiler?

07-011. Pozisyon büyüklüğü sinyal gününde hesaplanır, ama pozisyon ertesi gün açılır; sinyal ile giriş arasında ATR'de büyük bir sıçrama (örneğin giriş günü boşluk) olursa stop mesafesi 2 ATR'nin neresinde kalır? Bu fark bir motor sınamasında yer alıyor mu?

07-012. Tansu'nun infografiği 100.000 $ ve "~70 hisse" örneğini veriyor; örnekte giriş fiyatı yok ve 70 hissenin sermayeyi aşıp aşmadığı bilinmiyor (E-K1). Bu durumda "kaldıraç yok" ve %10 tavan kuralları Tansu'ya mı, bize mi ait ve ekranda hangisi olarak sunulacak?

07-013. Hisse sayısı tam sayı (1 lot) iken sermayenin %10'u küçük hisse fiyatlarına bölünür; pozisyon 0 lota yuvarlanırsa sinyal sayılıyor mu, sayılmıyor mu? Sayılmıyorsa K1 rastgele karşılaştırmada aynı eleme uygulanıyor mu?

07-014. Boştaki nakit politika faizi kazanırken pozisyon açıkken nakit tutarı "özkaynak" tanımında yer alıyor mu? Risk tutarı nakit artırımıyla (faiz geliri) dolaylı büyüyorsa sınama ölçekten bağımsız oranlarla okunur (S2-2) iddiası hâlâ geçerli mi?

07-015. Kart ekranı (6.4) "1.000.000 TL için adet" gösterir; Levent'in gerçek sermayesi bundan farklıysa %10 tavanı ve %2 likidite sınırı farklı bağlayacaktır. Kartın adedi hangi sermayeyle üretildiğinde backtest ile aynı davranışı verir?

## B. 2 ATR stop ve ATR(14)

07-016. ATR uzunluğu ve yumuşatma türü kaynakta yok; TASARIM 5.5 "14" der ama Wilder, SMA ya da EMA olduğunu belirtmez. Üç yumuşatmanın stop mesafesini ve işlem sayısını nasıl değiştirdiği 5.10'daki parametre sağlamlığı ızgarasına dahil mi?

07-017. ATR düzeltilmiş fiyattan (HGDG, 5.1) hesaplanırsa, geçmişte uygulanan bedelsiz ya da temettü düzeltmesi TL cinsinden ATR'yi yeniden ölçekler. Stop seviyesi (giriş − 2 ATR) hangi seride (ham ya da düzeltilmiş) tutuluyor ve düşük/yüksek ile hangi seride karşılaştırılıyor?

07-018. 5.1 "fiyat seviyesi gerektiren her şey düzeltmesiz fiyatla" der; stop seviyesi bir fiyat seviyesidir. Stop düzeltmesiz seride, ATR düzeltilmiş seride hesaplanırsa iki seri arasındaki ölçek farkı stop mesafesini bozmaz mı?

07-019. Pozisyon açıkken bedelsiz, bölünme, bedelli ya da temettü olursa stop seviyesi nasıl güncellenir? Backtestte düzeltilmiş seri bunu örtük çözer, ama canlıda ham fiyat düşer; Adım fonksiyonu bu olayı bilmeden stopu tetikler mi?

07-020. TASARIM 5.3 stop ve hedefi "giriş fiyatından ve sinyal günü ATR'sinden" hesaplar; E-K2 tanımında ATR "giriş kararında bilinen son tamamlanmış değer" idi. Sinyal günü ATR'si kapanışı içeriyor mu, ve sinyal günü boşluğu ATR'yi şişiriyorsa stop gereğinden geniş olmuyor mu?

07-021. Kilitli tavan/taban günlerinde Yüksek = Düşük olduğu için günlük aralık sıfıra yakındır; ATR bu günlerde düşer ve ardından gelen pozisyon boyutu büyür. Kilitli günler ATR hesabında özel işleniyor mu?

07-022. Tansu'nun etiketi "STOP: 184.54, ATR: 4.62" (G-125) yalnız iki sayı gösterir ve E-K2 giriş fiyatının doğrulanamadığını söyler. 2 ATR'nin "giriş − 2×ATR" olduğu hangi birinci el kanıta dayanıyor; yoksa bu bir YORUM olarak mı kalıyor?

07-023. Tansu'nun kuralı "fiyat gün içinde stop seviyesine düşerse anında çık" der; backtest bunu "Düşük ≤ stop" ile modeller. Düşük, açılış ve kapanış müzayedelerinde oluşan fiyatları da içeriyorsa, aracı kurumların koşullu emri sürekli seansta tetikleniyorken müzayede fiyatı stopu "tetikledi" sayılmaz mı?

07-024. Stop dolumu "stop fiyatından" varsayılıyor (5.3). Gün açılışı stopun altında ama gün yüksek stopun üstündeyse (açılışta boşluk, sonra toparlanma) kural stop fiyatından dolum der; bu satış fiilen açılışa yakın bir fiyattan, stopun altında gerçekleşmez miydi?

07-025. TASARIM 5.3 boşluk dolumunu AOF'a yalnız "gün yükseği de stopun altındaysa" bağlıyor. Neden AOF < stop koşulu değil de bu koşul seçildi ve iki koşulun işlem sayısındaki farkı ölçüldü mü?

07-026. Stop dolumunda masraf sabit %0,3 (5.4) iken boşlukla stop yiyen işlemin gerçek kayması çok daha büyük olur. Stop dolumlarında kayma neden giriş dolumlarıyla aynı sabit masrafa bağlı?

07-027. BIST'te aracı kurum "zarar durdur" emirleri çoğunlukla koşullu emirdir ve fiyat adımı, fiyat marjı ve tek fiyat/müzayede dönemleriyle sınırlıdır. Stop dolumu "tam stop fiyatı" olarak mı, "tetiklenen ilk limit/piyasa emri fiyatı" olarak mı modelleniyor ve fark nerede ölçülüyor?

07-028. İşlem durdurma (KAP açıklaması, volatilite durdurması) sırasında stop dokunulmuş olsa da emir çalışmaz ve açılışta daha düşük fiyatta dolar. Durdurma günleri veride nasıl görünüyor ve stop dolumu bunları yakalıyor mu?

07-029. Stop her işlemde sabittir (E-K2 YORUM): ATR giriş anında dondurulur. Giriş sonrası oynaklık iki katına çıkarsa stop gereğinden dar kalır; bu seçimin alternatifine kıyasla duyarlılığı 5.10'a konmuş mu?

07-030. G-118 "zarar durdur emri kullanmamak bir numaralı hata" der; çift rotasyonunda hiç stop yoktur (5.5). Üç ailenin birinde stop olmaması Tansu'nun "risk paketi bütün ailelerde" tanımını zayıflatmıyor mu ve neden bu ailede %25 düşüş portföy kuralı (5.12) yeterli sayılıyor?

## C. AOF dolum modeli

07-031. İş Yatırım'ın AOF alanı gün sonunda hesaplanan tek bir sayıdır; giriş AOF'tan yapıldığında Düşük/Yüksek'e dayanan stop ve hedef kontrolü AOF'un oluştuğu zamandan önceki fiyat hareketlerini de "giriş sonrası" sayar. Bu giriş günü kontrolü (5.3) ileriye bakma yanlılığı oluşturmaz mı?

07-032. Giriş günü Düşük ≤ giriş − 2 ATR ise işlem aynı gün stop olur; ancak Düşük, AOF'un hesaplandığı alımlardan önce ya da sonra oluşmuş olabilir. Giriş günü stop ve hedef için kaçıncı sıralama varsayımı kullanılıyor ve kaç işlem aynı gün çıkıyor?

07-033. AOF günün tüm işlemlerini içerir; bir birey tek bir AOF fiyatından 100.000 TL'lik alım yapamaz. "Bireysel yatırımcı gün içinde işlem yapar" (5.3) gerekçesi AOF'un ulaşılabilir olduğunu kanıtlamıyor; ulaşılabilirlik hangi veriyle sınandı?

07-034. Kırılım, sıkışma çıkışı gibi sinyaller sinyal sonrası günde sıklıkla yüksek hacimle açılış boşluğu üretir; AOF bu boşluğu gün boyu ortalar ve yukarı boşlukta alımı gerçekçi olmayan biçimde ucuz gösterebilir. AOF modelinin giriş maliyetine yönlü yanlılığı ölçülüyor mu?

07-035. Yahoo açılışıyla "T+1 açılış" kuralı sadakat kontrolünde ayrıca üretilir (5.3) ama Yahoo "kullanılmaz" (4). Bu ek koşunun sonucu AOF sonucundan çok farklıysa kabul ölçütü (5.12) hangi dolum modeline bakar?

07-036. AOF'un Borsa İstanbul'da hangi işlemleri (müzayedeler, toptan satış, özel emirler, çapraz işlemler) içerdiği doğrulandı mı? Toptan satış pazarı işlemleri AOF ve Yüksek/Düşük değerlerini bozuyorsa dolum varsayımı da bozulur.

07-037. AOF alanının her zaman Düşük ile Yüksek arasında kaldığı ve işlem olmayan günlerde (HACIM = 0) boş ya da önceki değeri taşımadığı, 2015–2026 için tüm hisselerde doğrulandı mı?

07-038. TASARIM 5.5 çıkışı "ertesi açılışta" der, 5.3 ve KURALLAR §3 notu bunu AOF yapar. Aynı belgede iki dolum fiyatı tanımı bulunması motor kodunda hangisinin uygulanacağını belirsiz bırakmıyor mu?

07-039. SMA250 çıkışında "gün sonu" (E-K3) Tansu'da kapanışta mı yoksa ertesi gün mü çıkıldığı belirsizdi; TASARIM ertesi gün AOF'unu seçti. Kapanışta çıkış (aynı gün müzayede fiyatı) varsayımının sonuçları ne kadar değiştirdiği raporlanacak mı?

07-040. Giriş dolumu ve çıkış dolumu aynı AOF fiyatından, aynı sabit masrafla yapılıyor (5.4); alım ve satış yönündeki AOF'a göre kayma yönleri farklıdır (kırılım alımı ortalamanın üstünde, panik satışı altında doldurur). Masraf neden simetrik?

07-041. Kapanış fiyatı (KAPANIS) ve AOF'un farkı sinyal günü kapanışını bilen bir kullanıcı için ertesi AOF'un tahmin edilebilir kısmını içerir mi; bunun sistematik kâr olarak ölçüldüğü bir kontrol (örneğin sinyalsiz rastgele günlerde aynı AOF dolum farkı) var mı?

07-042. Hedef dolumunun "Yüksek ≥ hedef" ile gerçekleştiği varsayımı limit emrinin sıra önceliğini yok sayar: hedef seviyesine yalnızca bir tik dokunulmuşsa gerçek emir dolmayabilir. Hedefte dolum için dokunma yeterli mi, ve açılış hedefin üstündeyse (boşluk) dolum hedef fiyatında mı, daha iyi fiyatta mı?

07-043. Giriş AOF'u AB=CD hedefi D'nin üstündeyse (hedef zaten geçilmiş) işlem açılıyor mu, hemen hedefte mi kapanıyor, yoksa reddediliyor mu? Bu kenar durum 5.3'ün motor sınamaları listesinde yok.

07-044. Hedef dolumu ve giriş dolumu aynı gün, aynı AOF ve Yüksek/Düşük verisine dayandığı için giriş günü hedef kontrolü (5.3) ile stop-önce kuralı çelişebilir; AOF hedefin üstündeyse stop-önce kuralı hâlâ stopu mu seçer?

07-045. Aynı gün hem stop hem hedef değerse stop önce (5.3); bu işlemlerin oranı raporlanır. Oran yüksek çıkarsa (geniş aralıklı hisselerde) "iyimser fark ayrıca gösterilir" ifadesi hangi eşikte sonucu geçersiz kılar?

07-046. Dolumların neredeyse tamamı Düşük/Yüksek/AOF günlük özetlerine dayanıyor; gün içi sıra bilgisi hiç yok. AOF'un Düşük ile Yüksek'e göre konumu, sıralama için bir ipucu olarak kullanılabilir iken neden yalnız mutlak iyimser/kötümser iki uç gösteriliyor?

07-047. %0,3 sabit masraf "komisyon, BSMV, kayma, açılışta kovalama birlikte" (5.4); AOF modeli açılış kovalamasını zaten ortadan kaldırdığını iddia ediyor. Açılışta kovalama payı hem AOF seçimiyle hem masrafla iki kez mi sayılıyor, yoksa hiç sayılmıyor mu?

07-048. Yarım gün seansları (arife) ve yeni müzayede/seans saatleri değiştiğinde AOF, Düşük ve Yüksek günlük anlamını koruyor mu? Seans yapısı 2015–2026 arasında değiştiği için stop ve dolum varsayımları dönemler arasında tutarlı mı?

07-049. İşlem kısıtlı hisselerde (tedbirli, brüt takas, tek fiyat) günlük AOF yalnız müzayede fiyatıdır ve gün içi stop çalışmaz; TASARIM 8.4 bunu "bilinen yanlılık" yapmayı öngörüyor. Dolum modeli bu hisseleri tek tek ayırmıyorsa stop ve giriş sonuçları hangi yönde sapar?

07-050. Giriş yalnız AOF'tan yapılır; işlem hacminin AOF'ta %2'yi aşması (5.4 "son 10 günün medyanı") o günün gerçek hacmine göre değil medyana göre sınırlanır. Sinyal günü sonrası hacim çöküşünde (örneğin tavan kuyruğu) pozisyonun o gün dolabilmesi kontrol ediliyor mu?

## D. Kilitli tavan/taban

07-051. Kilitli tavan tespiti "Düşük = Yüksek = tavan" ister; tavan fiyatı hangi fiyattan hesaplanıyor? Borsa İstanbul pay piyasasında baz fiyatın önceki günün kapanışı mı yoksa ağırlıklı ortalama fiyatı mı olduğu doğrulandı mı? Doğrulanmadıysa tüm tavan/taban tespiti ve karantina eşiği (5.1) yanlış bir referansa dayanır.

07-052. Kapanıştan kapanışa limit aşımı karantina nedeni sayılır (5.1, +%0,5); baz fiyat kapanış değilse, tamamen normal ±%10 hareket kapanıştan kapanışa %10'u aşabilir ve veri hatası gibi karantinaya girer. Bu eşik hangi tarihli, hangi baz fiyat tanımıyla doğrulandı?

07-053. Düşük = Yüksek günlerinin tamamı kilit değildir: tek fiyat yöntemine alınan, işlem durdurulan, çok az işlem gören hisseler de Düşük = Yüksek üretir. Bu günler "kilitli tavan/taban" sayılırsa giriş ve çıkış kuralları yanlış tetiklenmez mi?

07-054. Tavanda açılıp birkaç tik aşağı işlem gören, ardından yeniden tavana kilitlenen gün Düşük < Yüksek üretir ve kilitli sayılmaz; AOF'tan alım serbest kalır. Gerçekte bu günlerde milyonlarca lotluk alış kuyruğu vardır; "yaklaşık kilitli" günleri tanımlayan bir eşik var mı?

07-055. Kilitli tavanda giriş yoktur ama kilitli tavanda çıkış (hedef satışı) serbest mi? Aynı gün kilitli tavanda hedefin dolumu simetrik biçimde reddediliyorsa çıkış kuralı iyimser, serbest bırakılıyorsa giriş kuralıyla asimetrik olur; hangisi uygulanıyor?

07-056. Kilitli tabanda çıkış "ertesi güne kayar" (5.3); ertesi gün de kilitliyse ne olur ve ertesi gün hangi fiyattan satılır: AOF, stop, yoksa taban fiyatı? Birden çok gün kilitli kalan hisselerin gerçekleşen kaybı −2R'nin çok altına inebilir; bu raporlanacak mı?

07-057. Taban kilidi Düşük = Yüksek = taban olduğunda tanımlıdır; ancak gün başında kilitli açılıp gün sonunda hafif açılan taban günlerinde (Yüksek > Düşük) çıkış "stop fiyatından" varsayılır. Gerçekte taban kuyruğundaki satıcı aynı fiyattan dolmaz; bu iyimser dolum nasıl sınırlanıyor?

07-058. Stop seviyesi günlük taban fiyatının altında kalıyorsa (stop = giriş − 2 ATR, hisse üst üste limit-aşağı gidiyorsa) stop dolumu fiilen taban fiyatına çıkar. Dolum fiyatı günlük limitle kırpılıyor mu?

07-059. TASARIM 5.1 limit rejimini tarihe bağlar (2015–2020 ±%20, sonrası ±%10); limit tarihleri, farklı pazarlar (Yıldız/Ana/Alt) ve halka arz ilk günlerindeki farklı limitler kodda nasıl temsil ediliyor? Yanlış limit kilit tespitini bozar.

07-060. Tavan/taban kontrolü "düzeltmesiz fiyatla" yapılır (5.1); bedelsiz ya da bölünme sonrası baz fiyat ayarlanır ve ilk günde tavan seviyesi önceki kapanıştan hesaplanamaz. Olay günü bu kontrol nasıl çalışıyor?

07-061. Pozisyon açıkken taban kilidi 3 gün sürüp açıldığında oluşan kayıp gerçekleşirken, aynı gün giriş yapılan başka hisseler için nakit serbest değildir. Simülatör kilitlenmiş pozisyonun nakdini ve pozisyon sayısı sınırını (en fazla 10) nasıl yönetiyor?

07-062. Çift rotasyonunda bir bacak kilitliyse (örneğin satılacak hisse tabanda) geçiş yapılamaz, öbür bacakta alım yapılabilir mi? "Her çift payı her an çiftin bir hissesindedir" (5.6) değişmezi bu durumda bozulur; hangi kural geçerli?

## E. SMA250 çıkışı ve ailelere özgü çıkışlar

07-063. Bütün ailelere SMA250 altı kapanışta çıkış uygulanıyor (5.5) ama aile giriş kuralları SMA250 üstü şartı içermiyor olabilir. EMA sıkışması veya AB=CD girişi fiyat SMA250'nin altındayken oluşursa pozisyon açıldığı gün çıkış sinyali taşır; bu durum nasıl işleniyor?

07-064. Giriş günü SMA250 çıkış koşulu sinyal günü kapanışında zaten sağlanıyorsa (Kapanış < SMA250) Adım pozisyonu açtığı gün mü kapatır? Bu "açıl-kapat" işlemleri sayıma, masrafa ve 100 işlem şartına (5.9) giriyor mu?

07-065. SMA250 için 250 gün veri gerekir; 2015 başı veri sınırı ve walk-forward'ın 2015–2017 ile başlaması (5.8) ilk yıllarda çıkış kuralını çalışmaz kılar. İlk 250 günde pozisyonlar nasıl çıkıyor ve yeni halka arzlar sistematik olarak dışlandığında hayatta kalan yanlılığı artmıyor mu?

07-066. SMA250 düzeltilmiş seriden hesaplanır (E-K3 YORUM); bedelsiz çarpanları orantılı, temettü düzeltmeleri ise çarpansal ya da toplamsal olabilir. Düzeltmenin yeni bir olayla geriye dönük değişmesi SMA250 kesişimini değiştirebilir; çıkış günleri anlık görüntüye göre sabit mi?

07-067. Tampon veya histerezis yok (E-K3 YORUM 0); fiyat SMA250 çevresinde gidip gelirse ardışık çıkış ve yeniden giriş (testere) oluşur. Yeniden giriş yeni sinyal beklemeden olmaz (5.3) denir ama EMA sıkışması gibi bir ailede sinyal ile SMA250 çıkışının aynı seviyede iç içe olması beklenmiyor mu?

07-068. EMA sıkışması ailesinde (EMA20/50/100/200 birbirine yakın) fiyat çoğunlukla SMA250 yakınındadır; "hedef yok, stop 2 ATR, SMA250 çıkışı" paketi bu ailenin çıkışını fiilen SMA250'ye bağlar. Çıkışı belirleyen kural 2 ATR mi SMA250 mi ve neden bu aile için paket "Tansu'nun" sayılıyor?

07-069. Aileye özgü hedef yoksa pozisyon süresiz açık kalabilir (zaman stopu ertelendi, 3). 10 pozisyon sınırı dolu kaldığında yeni sinyaller reddedilir; tutma süresi dağılımı ve reddedilen sinyal oranı raporlanacak mı, yoksa bu K1 karşılaştırmasında kuralın aleyhine sistematik bir sapma olarak mı kalır?

07-070. TASARIM 5.5 AB=CD stopunu A seviyesi yapar ve genel 2 ATR'yi bu aileden çıkarır (S2-34), dayanağı ikinci el "C'den sonra fiyat A'yı geçerse kalıp ölür" cümlesi ve SMRTG zararlarıdır. Aynı Tansu çıktısı G-02'de "Stop (X)" sütunu içerir; AB=CD için kullanılan sütunun A mı X mı olduğu nereden biliniyor?

07-071. SMRTG zararları −%12 ile −%25 (G-03); bu sonuçlar sermayenin tamamı her işlemde bileşik kullanılarak (E-K15) elde edilmiş görünür. Tansu'nun AB=CD sonuçları %1 risk sınırı olmadan üretilmişse, sadakat kontrolü (7.2) bu sonuçları risk paketi altında nasıl karşılaştırır?

07-072. AB=CD'de stop A seviyesindeyse stop mesafesi çoğu zaman 2 ATR'den çok büyüktür; %1 riskli lot küçülür ve %10 tavanı bağlamaz, bu da pozisyonları çok küçük yapar. "Hedef D" ile stop A arasındaki ödül/risk oranı hesaplandı mı ve Tansu'nun kendi 1:2 eşiğinin (E-K23) altındaysa işlem hâlâ sayılıyor mu?

07-073. A seviyesinin aşılması "kalıp ölür" tetiğidir; bu gün içi mi (Düşük < A) yoksa kapanışa mı (Kapanış < A) bağlı? E-K15 bunu açıkça belirtmez, TASARIM 5.5 ise "stop A seviyesi" der. Gün içi temasla stop alındığında dolum fiyatı A mı, AOF mı?

07-074. AB=CD'de giriş C'nin teyit edildiği günü izleyen AOF'tur (S2-31); D hedefi o güne kadar bilinen A, B, C'den hesaplanır. Teyit penceresi nedeniyle C ile giriş arasında fiyat D'ye yaklaşmış ya da A'nın altına düşmüş olabilir; bu durumda sinyal geçerli sayılıyor mu?

07-075. "Bozulma" GLOSSARY'de kapanışın SMA250 altına inmesi, 5.3'te "bozulma çıkışı" test ismi, 6.5'te kart durumu BOZULDU ve Tansu'da AB=CD'de pattern geçersizliğidir. Bu üç anlamın hangisi Adım fonksiyonunda "STOP", hangisi "BOZULDU" durumunu üretir?

07-076. 5.5 çift rotasyonunda stop yoktur ve "Risk paketi bu bölmeye uygulanmaz"; ama 5.12'nin portföy kuralı (%25 düşüş) çift bölmesine de uygulanır. Düşüş %25'i aşınca ne olur: sınama başarısız mı sayılır, pozisyon mu kapanır, yoksa yalnızca rapor satırı mıdır?

07-077. Çift geçişinde satış ve alış ayrı AOF'ta ve ayrı %0,3 masrafla yapılır; bir geçiş çift yönlü %0,6 maliyet demektir. Tansu'nun tablolarında masraf yokken (E-K15 "masrafsız") ΔZ sinyallerinin sıklığı bu maliyeti taşır mı, ve sıklık bilindiğinde net kâr işareti değişmez mi?

07-078. Çift rotasyonunda Adım fonksiyonu "(pozisyon, bugünkü mum)" imzasıyla tek bir mum alır; çift geçişi iki hissenin mumunu, iki hissenin kilit durumunu ve z-skorunu gerektirir. Adım gerçekten iki bölme türü için de aynı fonksiyon mu?

## F. Giriş günü, yeniden sinyal, portföy

07-079. Pozisyon açıkken gelen sinyal yeni işlem açmaz ve sayıma girmez (5.3, C9, B5d); ancak aynı sinyal pozisyon çıkış gününde ya da çıkış sinyaliyle aynı gün gelirse ne olur: yeniden giriş mi, yok sayma mı? Çıkışın AOF'ta, yeni girişin ertesi AOF'ta olduğu günlerde sıra nasıl işleniyor?

07-080. Rastgele kural K1'de pozisyon açıkken gelen rastgele gün atlanıyorsa, rastgele işlem sayısı kuralın işlem sayısından az olur; "sayılar hisse başına eşleştirilir" (5.7) iddiası bu atlama sonrası da korunuyor mu?

07-081. Pozisyon açıkken yeni sinyalin sayılmaması kuralın sonucuna bilgi taşıyan bir seçici filtre ekler: kazançlı pozisyonlar uzun açık kalıp daha çok sinyali atlar. Atlanan sinyallerin dağılımı ve sonuçları raporda gösteriliyor mu?

07-082. En fazla 10 pozisyon dolu iken gelen sinyaller reddedilir; reddedilen sinyallerin sonradan nasıl performans gösterdiği (fırsat maliyeti) ölçülmeden "kural işe yaramadı" sonucu portföy kısıtından mı yoksa kuraldan mı geliyor ayırt edilebilir mi?

07-083. 5.3 "giriş günü de stop ve hedef kontrol edilir" der; giriş günü yüksek ve düşük zaten giriş dolumundan önce oluşmuş fiyatları içerir. Giriş günü kontrolü yalnız AOF'tan sonraki bölüme mi uygulanır, ve bunun veriden nasıl ayrıldığı belli mi?

07-084. Sinyal günü kapanışında tavanda kilitlenen hisseler ertesi gün de tavan açabilir; giriş "yok" ise sinyal ertesi güne mi ertelenir, tamamen iptal mi edilir? İptal edilirse kuralın en güçlü momentum günleri sistematik olarak sayım dışı kalır; bu K1 rastgele kuralıyla aynı mı?

07-085. Motor sınamalarının listesi (5.3: hedef, stop, boşluklu stop, aynı gün stop+hedef, tavan girişi, taban kilidi, bozulma çıkışı) lot yuvarlama, %10 tavan, giriş günü stop, tekrar sinyal, SMA250 çıkışı, bedelsiz sırasında açık pozisyon ve ardışık kilit günlerini içermiyor. Bu eksikler bilinçli mi?

07-086. Planlanan kayıp ile gerçekleşen kayıp farkı (boşluk etkisi) E-Grup 3 kontrol listesinde "Tansu'nun ilkesi" olarak yer alır; TASARIM raporu bu farkı bir çıktı olarak tanımlamıyor. Raporda R katsayısı dağılımı (kazanç ve kayıp, R cinsinden) ve −1R'den büyük kayıp oranı olacak mı?

07-087. MFE/MAE ve işlem günlüğü (E-K18) Tansu'nun birkaç ayda gerçek istatistik üretme önerisidir; TASARIM 5.11 deneme günlüğünü tutar ama işlem düzeyinde MFE/MAE tutmaz. Bu alanlar olmadan stop ve hedef parametrelerinin duyarlılığı nasıl incelenir?

07-088. Kısmi kâr, iz süren stop ve "önceki günün dibi altı kapanışta %50 sat" kuralları kapsam dışına alındı (3, 5.5) ama Tansu paylaşımlarının çıkış tarafındaki en detaylı tek örneği (G-125) bunlardır. "Önce sadakat" ilkesi (1) varken Tansu'nun gösterdiği çıkış biçimi sınanmadan atılması bu ilkeyle çelişmiyor mu?

## G. Adım, Motor, vectorbt

07-089. TASARIM 4 "Adım, sınama ile canlı günlük aynı fonksiyonu kullanır, böylece ikisi ayrışamaz" der; canlıda stop gün içinde çalışır ve Adım yalnızca 19:30'da bir günlük mumla çalışır. Canlıda "STOP" durumu olay sonrası mı yazılıyor, ve Levent bu durumu gerçek zamanda nasıl kullanır?

07-090. Canlıda kart giriş bölgesi, stop ve adedi sinyal günü akşamı üretilirken backtest stopu ertesi günün AOF'una göre hesaplar; AOF o akşam bilinmez. Kartta gösterilen stop backtestteki stoptan farklı olacaksa Adım ortak fonksiyon sayılabilir mi?

07-091. İş Yatırım günlük barı akşam yayınlandıktan sonra düzeltiliyor mu ve HGDG geçmişi her bedelsizde yeniden yazılıyor mu? Canlıda Adım bugünün geçici barına göre durum verirse (STOP/HEDEF), sonra veri değiştiğinde durum geri alınır mı?

07-092. Adım fonksiyonu (pozisyon, mum) alır ama ATR, SMA250, önceki gün düşüğü ve tavan/taban seviyesi geçmişe ihtiyaç duyar. Fonksiyonun gerçek girdisi (durumlu mu, durumsuz mu) tanımlı değil; "belirleyici" (4) iddiası bu durumun saklanma biçimine bağlı değil mi?

07-093. Motor "belirleyici" denir (4) ama K1 rastgele kuralı, 1.000 tekrar ve rastgele sinyal seçimi içerir. Rastgele tohum (seed) ve rastgele kural kodunun Adım döngüsünü paylaşıp paylaşmadığı kayıt altında mı?

07-094. vectorbt'in kullanılmayacağı gerekçesi "koşullu stop dolumu yapılamaz" (4, S2-41) olarak yazıldı; vectorbt özel sipariş fonksiyonu ve OHLC tabanlı `sl_stop`/`tp_stop` desteği sunar. Hangi vectorbt özelliği hangi sürümde denendi ve nasıl başarısız oldu, yoksa bu iddia denenmeden mi yazıldı?

07-095. Kendi Adım döngüsüne geçmek vectorbt'in hazır, geniş kullanıcı tabanında sınanmış dolum mantığını bırakmak demektir. Kendi motorun doğruluğunu (örneğin bağımsız bir referans uygulamayla çapraz kontrol) kanıtlayan, "elle hesaplanmış örnekler" dışında, ne var?

07-096. 1.000 rastgele tekrar × ~100 hisse × ~2.900 gün × üç aile × parametre ızgarası (5.10) saf Python Adım döngüsünde ne kadar sürer? Süre kabul edilemezse 200 tekrara (geliştirme) inmek p değerinin kararlılığını nasıl etkiler ve bu hız sınırı vectorbt kararını yeniden açmaz mı?

07-097. Adım ve Motor aynı zamanda tavan/taban kontrolü, karantina, olay günleri, nakit faiz ve likidite sınırını bilmek zorundaysa Adım "küçük ve açık" bir fonksiyon (4) olarak kalabilir mi? Hangi mantık Adım'da, hangisi Motor'da, hangisi Simülatör'de?

07-098. Karantinaya alınan hisse pencere boyunca "sınamadan çıkar" (5.1); pozisyon o sırada açıksa Adım bu pozisyonu nasıl kapatır: son fiyattan mı, sıfırdan mı, hiç mi? Karantina gerçek bir çöküşü (limit aşımı) kapsarsa en kötü işlemler sistematik olarak sayım dışı kalmaz mı?

07-099. İşlem durdurma (SPK/KAP kaynaklı uzun durdurmalar), delist ve takas yasakları pozisyon açıkken oluşursa fiyat veride görünmez; Adım bunu "veri yok" olarak mı, stop dokunuşu olarak mı, yoksa son fiyatla zarar yazma olarak mı işler?

07-100. Sorgu-2 S2-7, S2-8, S2-9, S2-10 dolum kararlarının (AOF, boşlukta AOF, tavan girişi, taban kilidi) tamamı "⚠️ karar" olarak yazıldı ama hiçbirinin gerçek günlük BIST işlemleriyle (örneğin gün içi veya emir defteri örneği) doğrulandığı belirtilmedi. Bu dolum kuralları hangi gözleme dayanıyor ve yanlış çıktıklarında hangi sonuç geçersiz olur?
