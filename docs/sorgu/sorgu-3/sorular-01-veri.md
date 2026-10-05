# Sorular 01: Veri

01-001. TASARIM 4 "Veri deposu" satırı "tarihli, değişmez" anlık görüntü diyor, ama formatı, konumu, saklama süresi ve bütünlük kanıtı (hash) hiçbir yerde yazılı değil; "değişmez" neyle sınanır?

01-002. Her gün bütün hisseler için tam geçmiş (HGDG yeniden ölçeklendiği için) yeniden indirilirse anlık görüntü sayısı ve boyutu ne olur; yalnız yeni gün eklenirse HGDG'nin geçmişe dönük değişimi nasıl yakalanır?

01-003. Anlık görüntü indirilirken 500 hissenin bir kısmı hız sınırı veya hata yüzünden inerse yarım anlık görüntü ile tam anlık görüntü arasındaki fark nasıl işaretlenir; deneme günlüğü (5.11) hangisini kaydeder?

01-004. Kâğıt üstü canlı dönemde (5.8) günlük kart o günün 19:30 verisiyle üretiliyor; sonradan HGDG geçmişi değişince canlı kayıt eski veriyle mi yeniden hesaplanır, hangisi "kayıt" sayılır?

01-005. 19:30'da çekilen "bugünkü çubuk" İş Yatırım tarafından sonradan düzeltilebiliyor mu (kapanış fiyatı, AOF, hacim); doğrulanmadıysa (Açık soru 7) 5.1'deki tazelik kontrolü bunu nasıl ayırt eder?

01-006. sorgu-2 S16 "yayın saati AÇIK" diyor ama TASARIM 6 koşuyu 19:30'a sabitliyor; bu saat hangi ölçüme dayanıyor ve yarım günlerde (arife) veri daha erken mi yayınlanıyor?

01-007. TASARIM 5.1 "son çubuğun tarihi bugün değilse kart üretilmez" diyor; resmî tatil, hissenin işlem durdurması ve hafta sonu koşusu bu kuralla nasıl ayrışır?

01-008. "Hacim olağandışıysa kart üretilmez" (5.1) cümlesinde "olağandışı" için sayısal eşik, pencere ve test yok; bu iddia nasıl sınanır?

01-009. TASARIM 4 "Takvim" modülü BIST tatillerini ve yarım günleri girdi olarak istiyor, sorgu-2 S15 ise "İş Yatırım'ın verdiği günler işlem günüdür" diyor; takvimin gerçek kaynağı hangisi ve ikisi çelişirse hangisi kazanır?

01-010. İş Yatırım serisinde bir günün eksik olması (kaynak boşluğu) ile gerçek bir tatil nasıl ayırt edilir; hem İş Yatırım hem borsapy aynı günü kaçırırsa hangi kontrol bunu yakalar?

01-011. veri-kaynaklari 3.1 satır sayısını borsapy için ~2946, İş Yatırım için 2945, sorgu-2 ise 2.947 veriyor; bu üç sayı arasındaki fark tarih aralığıyla mı yoksa eksik günlerle mi açıklanıyor ve kim doğruladı?

01-012. 2023 Şubat depremi sonrası Borsa İstanbul'un art arda birkaç gün kapalı kaldığı dönem, ATR, SMA250 ve "10 günlük medyan hacim" pencerelerinde nasıl ele alınıyor; takvim tablosu bunu bilecek mi?

01-013. Bayram köprü günleri (idari izin) ve ara tatiller için borsanın kapalı olduğu günler resmî tatil listesinde yoksa takvim modülü yanlış gün üretir; bu liste hangi belgeden derlenecek?

01-014. Yarım günlerde (arife) hacim ve gün aralığı yaklaşık yarıya iner; ATR, hacim eşiği, "olağandışı hacim" ve 2 ATR stopu bu günleri nasıl farklı işler?

01-015. Hissenin tek başına işlem durdurması (KAP açıklaması, SPK yasağı) satırı eksik bırakıyorsa, "XU100 ile kesişim" (sorgu-2 S15) göstergelerin pencerelerini kaydırır mı; boşluk günleri ileri mi doldurulur, atlanır mı?

01-016. Sorgu-2 S15 kesişim için XU100 kullanıyor; XU100 günlük serisinin kaynağı (veri-kaynaklari'nda yok), tatil takvimi ve geçmişi hangi dosyadan gelir ve piyasa durumu etiketi buna nasıl bağlanır?

01-017. İş Yatırım `HisseTekil` için "2015-01-02'den başlar" ölçümü, uç noktanın sınırı mı yoksa araştırmacının başlangıç tarihi seçimi mi; 2015 öncesi için sorgu denendi mi ve denenmediyse 250 günlük SMA ısınması 2015 verisinin hangi kısmını işlem dışı bırakır?

01-018. Tasarım 2015'i geliştirme verisi sayıyor (5.8) ama SMA250 ısınması 2015 işlem günlerinin neredeyse tamamını tüketir; ilk sinyal gerçekte hangi tarihte mümkün ve "2015–2017 ile başlayan ileri yürüme" bu yüzden fiilen kaç yıllık veridir?

01-019. 5.1 "30.11.2015 – 12.03.2020 arası ±%20" yazıyor; 02.01.2015 – 27.11.2015 arasındaki ABCD dönemi marjı bilinmiyor (veri-kaynaklari 5.1); bu 11 aylık dönemde karantina eşiği ne olacak?

01-020. 30.11.2015'teki BISTECH geçişinde HG_KAPANIS ve HG_HACIM tanımları (resmî kapanış fiyatı, tek taraflı/çift taraflı hacim, kapanış seansı yöntemi) değişti mi; geçiş öncesi ve sonrası aynı seri sayılabilir mi?

01-021. veri-kaynaklari 5.5 Ekim 2020 sonrası pazar bazlı marjın (Yıldız %20, Ana %15, Alt %10) yürürlükte olup olmadığını "doğrulanmadı" diyor; TASARIM 5.1 buna rağmen tüm hisseler için tek ±%10 yazıyor, bu fark neye dayanıyor?

01-022. Karantina eşiği "o günkü limit +%0,5" ise limiti hangi hisse için hangi pazara göre okuyacak; Yıldız Pazar'daki bir hisse ±%20 ise ve yanlış ±%10 uygulanırsa gerçek bir +%15 gün yanlış karantinaya girmez mi?

01-023. Kilitli tavan/taban tespiti (5.3) için tavan fiyatının hesaplanması gerekir; baz fiyat, fiyat adımına yuvarlama ve adım tablosunun dönemsel değişimi hangi veriden alınacak ve sınama kapsıyor mu?

01-024. Bedelsiz, bedelli veya temettü gününde borsa baz fiyatı düzeltir; ham dünkü kapanışla ham bugünkü kapanış arasındaki oran bu günlerde tavan/taban kontrolünde yanıltır, 5.1 "düzeltmesiz fiyatla" kuralı bu günleri nasıl ele alıyor?

01-025. Rüçhan hakkı işlem döneminde marj ±%50 veya serbest (veri-kaynaklari 5.9); hisse bu günlerde karantinaya mı girer, motor bu günde stop ve hedef için hangi kuralı uygular?

01-026. Kilitli tavan tespiti "düşük = yüksek = tavan" şartı arıyor; açılışta birkaç lot işlem görüp sonra tavana kilitlenen gün (düşük < yüksek) için giriş "mümkün" sayılır, bu gerçekçi mi ve nasıl sınanacak?

01-027. Aynı kural taban için de kullanılıyor; düşük = yüksek = taban olmayan ama kuyruğun fiilen kapanmadığı günlerde (az lot işlem) çıkış AOF'tan yapılabilir kabul ediliyor, bu AOF'un gerçekleşebilir olduğuna dair kanıt var mı?

01-028. Art arda birçok gün kilitli tavan veya taban yapan hisselerde (halka arz serileri, kötü haber) giriş yok/çıkış kayıyor kuralı pozisyonu kaç gün tutar; kayan çıkışta fiyat ertesi gün %20 daha aşağı gelirse bu kayıp hangi varsayımla hesaplanır?

01-029. Tek fiyat yöntemiyle işlem gören hisselerde (gözaltı, yakın izleme pazarı, tedbirli) gün içi tek fiyat oluşur, bu yüzden düşük = yüksek = AOF olur; kod bunu "kilitli tavan/taban" sanmaz mı?

01-030. Açık soru 4 tedbirli hisselerin (brüt takas, tek fiyat) bedava veriyle ayırt edilemeyebileceğini söylüyor; ayırt edilemezse AOF doluma ve likidite varsayımı bu hisselerde ne kadar bozulur ve "bilinen yanlılık" nasıl ölçülür?

01-031. AOF'un tanımı (açılış ve kapanış seansı işlemleri dahil mi, özel/ikili işlemler dahil mi, hacim ağırlıklı mı) belgelenmedi; gün aralığı dışında kalan AOF veya AOF = 0 satırları için doğrulama kuralı var mı?

01-032. Giriş fiyatı olarak günün AOF'unun, hissenin tüm günün işlemlerinin ortalaması olduğu için, bu fiyatın sinyal sonrası bütün gün boyunca pozisyon büyüklüğünün %2'sine kadar eşit dağıtılarak gerçekleşebileceği varsayımı hangi veriyle sınanıyor?

01-033. Giriş günü stop kontrolü gün düşüğü ile yapılıyor (5.3), ama düşük, AOF alımından önce oluşmuş olabilir; gün içi sıra bilinmeden "giriş günü stop vuruldu" kararı veri kaynağından nasıl çıkarılır?

01-034. Stop dolum kuralında gün yükseği stopun altındaysa AOF'ta dolum yazılı; düşüğün stopun altında ama yüksek stopun üstünde olduğu "açılışta boşluk, sonra toparlama" günlerinde stop fiyatından dolum gerçekçi mi ve açılış verisi olmadan bu iki durum nasıl ayrılır?

01-035. E-risk-cikis-surec.md satır 75 boşlukta dolumu "açılış fiyatı veya daha kötüsü" olarak yazıyor, TASARIM 5.3 ise AOF diyor; bu çelişkide hangi belge geçerli ve diğeri ne zaman güncellenecek?

01-036. KURALLAR.md EMA sıkışması için "99 hissede 11 yılda 520 sıkışma (Yahoo verisi)" sayısını veriyor; Yahoo bu tasarımda yasak, bu sıklık sayımı İş Yatırım verisiyle yeniden yapıldı mı ve ilk sayı hangi kararda kullanıldı?

01-037. TASARIM 7.2 sadakat kontrolünde Yahoo verisini kullanıyor, oysa veri-kaynaklari 2.2 Yahoo'nun bedelsiz günlerinde sahte sıçrama verdiğini kanıtlıyor; Tansu'nun rakamlarını bozuk veriyle yeniden üretmeye çalışmak, bozuk verinin Tansu'da da olduğunu varsayıyor mu?

01-038. Sadakat kontrolü Yahoo'da başarılı olup İş Yatırım'da başarısızsa (veya tersi), ailenin "Tansu gibi çalıştığı" sonucu hangi veri seti için geçerli sayılır?

01-039. Yahoo'da Tansu'nun kullandığı seri `auto_adjust` açık mı kapalı mı bilinmiyor; kontrol bu iki ayarı da deneyecek mi, ve hangisi İş Yatırım'daki HGDG (temettülü) ya da borsapy (temettüsüz) ile eşleşecek?

01-040. HGDG nakit temettüyü içeriyor (toplam getiri tipi, veri-kaynaklari 3.2), borsapy içermiyor; 5.1 çapraz kontrolün %0,5 eşiği, temettü verimi %0,5'ten yüksek olan her ex-günde alarm vermez mi?

01-041. HGDG/HG oranı THYAO için 2015-01'den 2024-12'ye kadar sabit 0,9769; bu, on yıl boyunca hiç temettü düzeltmesi uygulanmadığı anlamına da gelebilir, "HGDG tüm nakit temettüleri uygular" iddiası hangi ikinci hisse/olayla doğrulandı?

01-042. Temettü kaydındaki tarihin ex-date mi ödeme tarihi mi olduğu bilinmiyor (Açık soru 2); HGDG düzeltmesi ödeme tarihinde uygulanıyorsa, ex-date ile ödeme arasındaki haftalarda düzeltilmiş seri yanlış seviyede olur ve bu aralıkta üretilen sinyaller nasıl etkilenir?

01-043. 5.1 kendi düzeltme katsayısını (`SHHE_FIYAT_AYAR_OR`) HGDG ile karşılaştırıyor; katsayı nakit temettüyü içermiyorsa (kod 04), iki seri yapısal olarak farklı olur, hangi fark "hata", hangisi "temettü" sayılacak?

01-044. `SHHE_FIYAT_AYAR_OR` bedelli ve bedelsizi tek katsayıda birleştiriyor (HEKTS 2021: 0,2801; formülle 0,2646); katsayının hangi ex-fiyata göre hesaplandığı bilinmeden "doğrudan al" kararı sınanabilir mi?

01-045. Aynı gün birden çok olay (örnek: bedelli + temettü, ya da iki ayrı kayıt) olduğunda katsayıların çarpım sırası ve çift sayım riski için sınama vakası var mı?

01-046. Sermaye azaltımı (kod 78, çarpan 1,0) fiyatı düzeltmiyor; ama bu olay bir hissenin hisse sayısını ve PD'sini değiştiriyor, Evren seçimindeki PD bu olay günü nasıl davranır?

01-047. Kod 07, 79, 90, 99 ve birleşme/bölünme (spin-off) olaylarının anlamı bilinmiyor (veri-kaynaklari 8.3); olay tablosunda bilinmeyen kod, açıklanamayan sıçrama gibi karantinaya mı gidiyor yoksa yok sayılıyor mu?

01-048. Karantina tanımı "o hisse o pencerede sınamadan çıkar" diyor ama pencere uzunluğu yok; sıçramadan önceki sinyaller de siliniyorsa, sonradan bilinen bir olay nedeniyle geçmiş sinyal çıkarılmış olmaz mı (ileriye bakış)?

01-049. Karantinaya girmek için "bir gün ±limit dışı hareket" gerekli; ama gerçek veri hatası çoğu zaman limit içinde kalır (örneğin %8'lik atlanmış bedelsiz); olay tablosunda eksik kayıt olduğunda bu hata nasıl yakalanır?

01-050. veri-kaynaklari 7.2 "ham kapanış günlük >|%25| sıçrıyorsa ve kayıt yoksa uyar" diyor, TASARIM 5.1 ise limit +%0,5 diyor; iki eşik neden farklı ve hangisi nihai?

01-051. Karantina oranı (hisse-gün veya hisse-pencere sayısı) için raporlama veya üst sınır yok; evrenin %5'i karantinaya girerse sonuçların hangi yönde yanlı olacağı raporda nasıl yazılacak?

01-052. Karantinaya sokulan günler çoğunlukla uç getirili günler; bu günleri atmak ve onları içeren sinyalleri dışlamak, kuralların uç getirilerini seçici olarak kırpmaz mı ve K1 rastgele kuralı aynı kırpmadan geçiyor mu?

01-053. 5.1 örneği "ECILC ve RYSAS, 12.03.2020" karantinaya girmiş sayılıyor; o tarihte limit hâlâ ±%20 idi (değişiklik 13.03.2020), hangi değişim bu iki hissede %20,5'i aştı ve hangi veride görüldü?

01-054. Fiyat limiti değişim tarihi 13.03.2020 gün içi başlıyorsa 12.03.2020 akşamı mı yoksa 13.03.2020 seansından mı geçerli; 12 Mart ile 13 Mart arasındaki karantina kararı hangi güne yazılacak?

01-055. İş Yatırım ve borsapy fiyatlarını getiri bazında karşılaştırma %0,5 farkla "listelenir" diyor; listeye giren bir günün ne yapılacağı (hangi kaynak kazanır, karantina mı, düzelt mi) yazılı değil, bu denetim sonuçsuz bir rapor mu?

01-056. borsapy çapraz kontrolü TradingView son işlem fiyatını kapanış olarak alıyorsa, kapanış seansı fiyatı (resmî kapanış) ile günlük farkların %0,5'i aştığı ince işlem gören hisselerde kaynaklar neden ayrılacak ve hangi kaynak doğru kabul edilecek?

01-057. Toplu çekimde (~500 hisse × 11 yıl) iki kaynak için hız sınırı ve IP engeli riski sınanmadı (veri-kaynaklari 8.1); engellenirse tasarımın hangi kısmı çalışmaz ve yedek kaynak var mı?

01-058. İş Yatırım uç noktası belgelenmemiş dahili AJAX; alan adı veya biçim değiştiğinde sessizce boş/eksik veri dönerse (örneğin `.E` eki gibi) hangi şema sınaması bunu yakalar?

01-059. "Kişisel kullanım" koşulu ve borsapy'nin "ticari kullanım yok" şartı dururken, sistem raporlarını başkasıyla (ör. Levent'in paylaştığı kişiler) paylaşmak lisansı ihlal eder mi; bu sınır nerede yazılı?

01-060. `SHHE_TARIH` alanı milisaniye epoch olarak geliyor; UTC'den İstanbul gününe çevirirken (gece yarısı = önceki gün 21:00 UTC) bir gün kayma riski için sınama var mı?

01-061. HG_* alanları iki ondalıkla yuvarlanıyorsa düşük fiyatlı hisselerde (1 TL civarı) bir fiyat adımı %1 olur; HGDG'nin çarpan uygulamasından sonraki yuvarlama hatası çapraz kontrolün %0,5 eşiğini kendi başına aşar mı?

01-062. `HGDG_HACIM` düzeltilmiş hacimdir; bedelsizde hacim lot olarak ölçekleniyor mu, TL olarak mı; ham ve düzeltilmiş hacmin ne zaman hangisinin kullanılacağı (likidite için ham fiyat × ham lot) belgelenmedi.

01-063. `HACIM`ın lot mu TL mi olduğu hâlâ açık (5.1); 5.4'teki %2 likidite limiti ve 5.2'deki 60 günlük medyan TL tutarı bu cevaba bağlı, cevap gelene kadar hangi sayılarla koşu yapılıyor?

01-064. Hacim, özel/ikili (toptan) işlemleri, açılış/kapanış seansı eşleşmelerini ve gün içi çapraz emirleri dahil ediyorsa, "likit hisse" ve %2 pozisyon sınırı için kullanılan medyan TL tutarı gerçekte alınıp satılabilen miktarı abartmaz mı?

01-065. Evrende `PD` (piyasa değeri) kullanılıyor, ama `HAO_PD` (halka açık piyasa değeri) mevcut; gerçek BIST100 seçimi halka açık değere dayanır, bu tercih evreni BIST100'den sistematik olarak nasıl uzaklaştırır?

01-066. PD'nin hangi fiyat ve hangi sermaye (SERMAYE) ile hesaplandığı belgelenmedi; sermaye kaydı bedelsiz tescilinde gecikmeli güncellenirse PD olay gününde 2-10 kat sıçrayabilir, evren her ay başı seçimi bu günlere denk gelirse ne olur?

01-067. Aynı şirketin birden çok pay grubu (A/B grubu, kurucu payı) ayrı semboller olarak işlem görüyorsa PD, şirket ya da sembol bazlı mı sayılır; aynı şirket evrende iki kez yer alabilir mi?

01-068. "Her ay başında" evren hesabında ay başı günün verisi kullanılıyorsa seçim anı ile ilk işlem günü aynı mı; seçim hangi günün kapanışından yapılır ve bu seçimden sonra çıkan hisse (kapanış) için kural var mı?

01-069. Evren, 60 günlük medyan TL hacmi şartı arıyor; halka arzdan sonraki ilk 60 günde hisse hiç evrene giremez, ama halka arz sonrası tavan serileri sinyal üretir; sinyal evreni ile ısınma şartı nasıl uyumlu?

01-070. Kapanmış hissenin son günleri (işlem durdurma, taban serisi, birleşme ile tasfiye) veride nasıl görünür ve pozisyon açıkken seri bittiğinde çıkış fiyatı nedir; veri bitişi sıfır getiri mi, son fiyat mı, kayıp mı sayılır?

01-071. Birleşmeyle (devralınan şirket) ya da hisse değişimiyle kaybolan semboller için sahibin gerçek getirisi (devralan hisse veya nakit) fiyat serisinde yoktur; bu hisseler "kapanmış" olarak mı yoksa kayıp mı sayılacak?

01-072. İş Yatırım `HisseTekil` kapanmış sembolleri döndürüyor (ASYAB) ama kaç tanesi için döndürdüğü ölçülmedi; döndürmeyen semboller rastgele mi yoksa kötü sonuçlanmış şirketler mi, ve bu bilgi yanlılık büyüklüğünü nasıl sınırlar?

01-073. Hisse kodu değişiklikleri (isim değişimi, kod yeniden kullanımı) için sembol-şirket eşleme tablosu yok; aynı kod iki farklı şirketi temsil edebilirse tarihsel seri ve olay tablosu yanlış eşleşir, bu nasıl önlenecek?

01-074. 5.2 ara evren için "kapanmış sembollerin listesi borsapy + KAP'tan" yazıyor; borsapy yalnız güncel hisseleri veriyor (veri-kaynaklari 4), listeyi tamamlayacak KAP sorgusunun 2000 kayıt sınırı ve kapsamı doğrulanmadı, bu kaynak gerçekte ne verecek?

01-075. Bedelli sermaye artırımında hissenin düzeltilmiş getirisi tüm haklarını kullanan hissedarı varsayar; fiilen gereken nakit (rüçhan kullanımı) simülatörde yok, bedelli günlerinde sermaye eğrisi bu yüzden iyimser olmaz mı?

01-076. HGDG temettüyü brüt olarak yeniden yatırıyor görünürken (ex-gün, anında, vergisiz), gerçekte temettü ödeme tarihinde ve stopajla gelir; bu fark K2 sepeti ve kural arasında eşit mi etkiler, yoksa uzun tutulan işlemlere mi yarar?

01-077. TASARIM 5.1 göstergeleri HGDG gibi temettülü seriden hesaplıyor, oysa Tansu'nun grafiği (TradingView/Yahoo) temettüsüz fiyat serisi; SMA250 ve EMA sıkışması oranlarındaki fark sinyal tarihlerini kaydırmaz mı ve sadakat kontrolü bunu nasıl ayırır?

01-078. Düzeltmenin sistemde iki yolu var: kendi katsayımızla düzeltme (5.1) ve İş Yatırım HGDG'si; göstergeler "düzeltilmiş fiyattan" derken hangisi kastediliyor ve iki seri farklıysa hangisi kaynak sayılıyor?

01-079. Açık bir pozisyon bedelsiz/bölünmeyle karşılaşırsa kartta stop ve hedef seviyeleri (ham TL) ile Adım fonksiyonu içindeki seviyeler (düzeltilmiş) arasındaki dönüşüm nasıl yapılır; canlı kartın ham seviyesi ne zaman yeniden yazılır?

01-080. HGDG her yeni olayda geçmişi yeniden ölçekler; bir gösterge pencere içinde mutlak seviye gerektiriyorsa (ör. A seviyesi stopu, pivot noktalar) hangi tarihli HGDG'ye göre hesaplanır ve sinyal günündeki gerçek ham seviyeyle tutarlılık nasıl sağlanır?

01-081. AB=CD stopu A seviyesi; A birkaç yıl önceki düzeltilmiş fiyattır, bu aralıkta bedelli/temettü olduysa A'nın ham TL karşılığı sinyal günü ile işlem günü arasında değişebilir mi ve kartta hangi değer yazılır?

01-082. İş Yatırım'ın HGDG serisinin geçmişe dönük değişimi nedeniyle iki gün farklı indirmede aynı tarihli sinyalin değişip değişmediğini ölçen bir sınama yok; "belirleyici motor" (4, Motor) iddiası bu durumda anlık görüntü sabitlenmeden nasıl savunulur?

01-083. Likidite sınırı (%2 pozisyon, 10 günlük medyan TL) pozisyon büyüklüğünü kısıtlıyor; AOF'un gün hacmiyle ağırlıklı olması bu kısıtın dolum fiyatını (kayma) etkilemesini kapsıyor mu, yoksa sabit %0,3 masrafın içine mi gömülüyor ve düşük likit hissede bu oran yeterli mi?

01-084. Sabit %0,3 masraf içinde "açılışta kovalama" da sayılıyor (5.4), ama TASARIM 5.3 açılış yerine AOF kullandığı için açılışta kovalama yoktur; masraf bileşenleri yeni dolum modeline göre yeniden gerekçelendirildi mi?

01-085. Fiyat adımı (tick) tablosu dönemler arasında değişti; AOF ile yapılan girişte ve stop/hedef fiyatlarında adım yuvarlaması yok; düşük fiyatlı hissede 2 ATR stopu birkaç tick'e iniyorsa dolum varsayımı nasıl bozulur?

01-086. Evrendeki hisseler için sektör sınıflaması bugünkü borsapy'den; sınıflamanın kaynağı (BIST sektör indeksi mi, borsapy kendi etiketi mi) ve zamana göre değişimi için doğrulama yok; kapanmış hisselerin sektörü olmayacağı için çift seçiminden dışlanması yanlılık yaratmaz mı?

01-087. Faiz için TASARIM 4 "TCMB politika faizi (borsapy)" ve "TLREF yalnız 2018 sonrası" diyor, 5.6 ise "EVDS; 2015–2017 politika faizi, sonrası TLREF" diyor; EVDS anahtarı gerekliyken borsapy yolu anahtarsız, hangisi gerçekten kullanılacak ve çelişki kapatıldı mı?

01-088. TLREF 28.12.2018'de hesaplanmaya, 17.06.2019'da yayına başladı; 5.6'daki "2015–2017 politika faizi, sonrası TLREF" ifadesi 2018'in tamamını ve 2019 başını açıkta bırakıyor, bu aralıkta hangi faiz kullanılacak?

01-089. borsapy politika faizi serisi 2026-01-23'te bitiyor (veri-kaynaklari 6), bugün 05.10.2026; ileri doldurma sonuncu değeri (37,0) kullanıyorsa, arada olan faiz kararları sessizce yok sayılır; tazelik kontrolü bu seriyi de kapsıyor mu?

01-090. borsapy `lending` sütununun 1 hafta repo olduğu doğrulanmadı; marjinal fonlama veya gecelik borç verme faizi olabilir, ve TCMB'nin 2016–2018'de fiilen kullandığı efektif fonlama oranı politika faizinden farklıydı; boştaki nakit getirisi bu yüzden hangi yönde yanlı?

01-091. Faiz serisi toplantı günlerinde basamak; kararın yürürlük günü, ilan günü ve veriye giriş günü farklıysa günlük nakit getirisi yeniden kurulurken geleceği bilen bir kayma olabilir mi ve ileri doldurma hangi günden başlıyor?

01-092. Açık soru 6 hisse kazancı ve temettü vergisini "doğrulanmadı" bırakıyor; HGDG vergisiz temettü yeniden yatırımı varsayarken %0,5 masraf senaryosu bunu "bir kısmını karşılar" diyor; bu "bir kısım" hangi hesapla gösterilecek?

01-093. TASARIM 5.8'de 2015–2026 geliştirme/doğrulama verisi sayılıyor; veri kaynağı değişir ya da İş Yatırım geçmişi düzeltirse (yeni olay eklenmesi) daha önce kayıtlı kuralın parmak izi aynı kalsa bile sonuçların değişmesi "yeni deneme" sayılır mı?

01-094. Deneme günlüğü (5.11) veri anlık görüntü kimliğini yazıyor, ama anlık görüntü yalnız fiyatları mı kapsıyor yoksa olay tablosu, evren, faiz ve takvimi de kapsıyor mu; bunlardan biri değişirse aynı koşu yeniden üretilebilir mi?

01-095. Anlık görüntü bir kez alınıp "değişmez" ise, İş Yatırım yanlış bir geçmiş veriyi sonradan düzelttiğinde sistem eski hatalı anlık görüntüyle çalışmaya devam eder; hatalı veriyi tespit edip anlık görüntüyü kullanımdan düşürme süreci tarif edildi mi?

01-096. Windows görev zamanlayıcıda "kaçırılan görevi çalıştır" (sorgu-2 S47) seçilirse bilgisayar iki gün kapalıyken bir sonraki koşu iki günü birden alır; atlanan günün anlık görüntüsü yok ve o günün kartları hiç üretilmedi, bu boşluk kayıt dışı mı kalır?

01-097. 5.1 çapraz kontrol "bütün hisse × gün getirileri" için borsapy'nin 15 dakika gecikmeli TradingView verisini kullanıyor; günün son çubuğu henüz kesinleşmemiş olabilir, 19:30'da bugünün çapraz kontrolü nasıl güvenilir olur?

01-098. Sorgu-2 S12 "HGDG geçmişe dönük değişir mi? Değişiklik yok" diyor; ama değişmesi anlık görüntü sorununu çözmekle bitmez, ham fiyat + olay tablosu + HGDG üçlüsü aynı anlık görüntüde tutulmazsa kendi düzeltmemizle HGDG karşılaştırması farklı tarihli verilerle mi yapılır?

01-099. Sorgu-2 S17 "11 yıl tek seferde geliyor; 1 sn bekleme" diyor; satır sayısı, yanıt boyutu ve zaman aşımı sınırı (2945 satır THYAO için çalıştı) 500 sembol ve yeni kısmi güncellemeler için ölçüldü mü, yoksa tek bir hisse örneğinden genelleme mi?

01-100. Veri kalitesi için kabul/ret kapısı (örneğin karantina oranı, çapraz kontrol farkı sayısı, eksik gün sayısı üst sınırı) önceden yazılı değil; "veri yeterince temiz" kararı sonuç gelmeden hangi sayısal ölçütle verilecek ve ölçüt sonuca bakarak gevşetilirse bunu kim fark edecek?
