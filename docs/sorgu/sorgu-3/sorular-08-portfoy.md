# Sorular 08: Portföy, masraf

Kapsam: tek hisse bölmesi, çift bölmesi, nakit faizi, masraf, likidite, enflasyon, düşüş kuralı, fazla getiri tanımları.

## A. Boyutlandırma ve bölme mekaniği

08-001. TASARIM 5.6'da adet %1 risk / 2 ATR ile, üst sınır sermayenin %10'u ile belirleniyor; ATR/fiyat oranı yaklaşık %5'in altındaki hisselerde %10 sınırı bağlayıcı olduğunda "%1 risk" işlemlerin yüzde kaçında gerçekten uygulanıyor ve rapor bu oranı yazıyor mu?

08-002. 10 pozisyon × %1 risk aynı anda açıkken toplam açık risk %10'a ulaşır; KURALLAR/E K1 "toplam açık risk sınırı Tansu'da yok" diyor, TASARIM 5.6 bu boşluğu hangi kuralla dolduruyor?

08-003. "%1 risk" ve "%10 tavan" için "sermaye" 1.000.000 TL'lik başlangıç değeri mi, günlük özkaynak (açık pozisyonlar dahil) mı? TASARIM 5.6 bunu yazmıyor, E K1 bunu "belirsiz" olarak bırakıyor.

08-004. Sermaye bileşik büyüyorsa %10 tavanı, %2 likidite tavanı ve adet her gün yeni özkaynağa göre mi hesaplanır; bileşik büyümüyorsa 11 yıllık eğri sabit 1.000.000 TL'ye göre mi okunur?

08-005. Başlangıç sermayesi 2015'ten 2026'ya nominal 1.000.000 TL'de sabit kalırken TL ciddi biçimde değer kaybediyor; 5.4'teki %2 likidite tavanı 2015'te sık sık, 2026'da neredeyse hiç bağlamazsa yıllar arası sonuçlar nasıl karşılaştırılabilir?

08-006. AB=CD stopu A seviyesi (SMRTG zararları −%12…−%25) iken adet formülündeki paydada 2 ATR mi yoksa giriş−A mesafesi mi kullanılıyor? TASARIM 5.5 ile 5.6 bunu açıkça bağlamıyor.

08-007. Adet tam lota yuvarlanırken aşağı mı yukarı mı yuvarlanıyor, ve yuvarlama sonrası gerçek risk raporda gösteriliyor mu? E K1 bu noktayı YORUM olarak bırakmıştı, TASARIM'de karşılığı yok.

08-008. %10 tavanı için adet = 0,10 × sermaye / giriş fiyatı gerekir ve giriş fiyatı ertesi günün AOF'u; AOF gün bitmeden bilinmediğine göre sinyal akşamı kartta yazan adet ile motorun üreteceği adet nasıl aynı kalır (TASARIM 6.4)?

08-009. Stop ve hedef "giriş fiyatından" (gerçekleşen AOF) hesaplandığına göre, sinyal akşamı karta yazılan stop seviyesi ertesi gün AOF'a göre değişiyor mu; değişiyorsa canlı kart ile backtest aynı kuralı mı uyguluyor?

08-010. Adet için ATR düzeltilmiş seriden (HGDG), tavan ve işlem fiyatı ham seriden alınıyor (5.1); iki farklı ölçekte hesaplanan değerler adet formülünde nasıl birleştiriliyor?

08-011. Pozisyon açıkken bedelsiz (adet artar), bedelli (nakit gerekir) ve temettü (nakit girer, stopaj) olayları simülatörde nasıl işleniyor? HGDG temettüyü fiyata gömüyorsa nakit akışı ve temettü vergisi hangi kalemde görünüyor?

08-012. Pozisyon açıkken oluşan düzeltme olaylarından sonra, giriş−2 ATR olarak sabitlenmiş stop seviyesi yeniden ölçekleniyor mu, ölçekleniyorsa hangi seriden?

08-013. Kaldıraç yok kuralı altında nakit bir pozisyonun gereken tutarından azsa (zarar sonrası ya da dolu slotlar) giriş küçülür mü, atlanır mı? TASARIM 5.6 bu durumu anlatmıyor.

08-014. BIST'te hisse satışının valörü varken aynı gün çıkış yapıp başka hisseye giriş yapmak (çift geçişi dahil) simülatörde nakdi ne zaman kullanılabilir sayıyor; valör süresince bu nakit faiz kazanıyor mu?

08-015. Aynı AOF gününde hem çıkış hem giriş olunca simülatör önce çıkışları mı işliyor; serbest kalan slot ve nakit aynı gün kullanılabiliyor mu, ve bu sıra rastgele kural K1'de de aynı mı?

08-016. Slot dolu olduğu için reddedilen sinyaller "işlem sayısı" ve K1'in "hisse başına eşleştirilen sayı" hesabına giriyor mu? Girmiyorsa eşleştirme üretilen sinyallere mi, açılan işlemlere mi yapılıyor (5.3, 5.7)?

08-017. "En likit önce" (M12) ifadesindeki likidite 10 günlük medyan TL tutarı mı, 60 günlük medyan mı, piyasa değeri mi? Aynı gün çok sinyal geldiğinde bu sıra sistematik olarak büyük hisselere ve bankalara yönelirse bu, kuralın başarısına karıştırılmıyor mu?

08-018. EMA sıkışmasında hedef yok ve çıkış yalnız SMA250/2 ATR ise pozisyonlar aylarca açık kalır; 10 slotlu tavanla 11 yılda kaç kapanmış işlem bekleniyor ve 5.9'daki "en az 100 işlem" şartı bu tavanla ulaşılabilir mi?

## B. Likidite, dolum ve piyasa mikro yapısı

08-019. 5.4 likidite için "son 10 günün medyanı", 5.2 evren için "60 günlük medyan" diyor; iki pencerenin gerekçesi nedir, ve 10 günlük pencere sinyal gününü ya da giriş gününü içeriyor mu?

08-020. %2 tavanı HACIM alanından hesaplanırken HACIM'in birimi (lot mu TL mi) hâlâ AÇIK (S2-14); "kod yazılmadan önce" sınanacak bir kural, birimi bilinmeyen bir alana nasıl bağlanıyor? Ayrıca HG_HACIM mi HGDG_HACIM mi kullanılıyor?

08-021. Pozisyon %2 tavanını aşınca ne oluyor: pozisyon küçülüyor mu, işlem atlanıyor mu, kalan miktar ertesi gün mü alınıyor? "Kısmi dolum" TASARIM'de hiç geçmiyor.

08-022. Likidite tavanı pozisyonu küçülttüğünde %1 risk kuralı korunuyor mu yoksa risk fiilen düşüyor mu, ve K1 rastgele kuralında aynı küçültme aynı biçimde uygulanıyor mu?

08-023. %2 tavanı yalnız girişte mi denetleniyor? Stop veya SMA250 çıkışı hacmin kuruduğu günlerde tüm pozisyonun gün AOF'unda satılabildiği nasıl varsayılıyor?

08-024. AOF dolumu için ertesi günün gerçek hacmi mi kullanılıyor, yoksa yalnız önceki günlerin medyanı mı? Gerçek hacim kullanılıyorsa bu ileriye bakmak, kullanılmıyorsa düşük hacimli günün dolum riski nasıl yansıyor?

08-025. Emrimiz ertesi günün AOF'una pay veriyor olsa da AOF'u kendi hacmimizle oynatmıyor mu; sabit %0,3 hangi katılım oranını (gün hacmi içindeki pay) varsayıyor?

08-026. İş Yatırım'ın AOF alanının hesaplanma biçimi (kapanış seansı ve açılış seansı dahil mi, toptan/çapraz işlem dahil mi) belgelenmedi; dolum fiyatının tamamı bu alana dayanırken tanım doğrulanmadan hangi kanıtla güvenilir sayılıyor?

08-027. HACIM'e toptan veya çapraz işlemler dahilse medyan TL tutarı ve %2 tavanı şişer; bu işlemler ayıklanabiliyor mu, ayıklanamıyorsa likidite kuralı hangi yanlılıkla çalışıyor?

08-028. Kilitli tavan yalnız düşük = yüksek = tavan olan günlerde "giriş yok" sayılıyor (5.3); tavanda açılıp kısa süre işlem görmüş ama kuyruğun doldurmadığı günlerde AOF'tan dolum varsayılması iyimser değil mi, bu günler kaç tane ve nasıl ölçülüyor?

08-029. Kilitli taban benzer biçimde yalnız düşük = yüksek = taban ise çıkış engelli; tabana kilitlenip az miktar işlem gören günlerde çıkış AOF fiyatından tam dolmuş sayılıyorsa kuyruktaki satıcının kısmi dolumu nasıl modelleniyor?

08-030. Taban kilidi ardışık günler sürerse çıkış fiyatı ilk işlem görülen günün AOF'u mu; bu kayıp %1 risk sınırını çok aşabilir, ve pozisyon bu süre boyunca slot ve sermaye eğrisinde nasıl sayılıyor?

08-031. Stop dolumu: gün düşüğü ≤ stop ve gün yükseği stopun üstündeyse stop fiyatından dolum varsayılıyor (5.3); gün stopun altında açılıp sonra toparlanırsa gerçek dolum açılışa yakın kötü fiyat olur ve açılış verisi yokken bu durum nasıl ayırt ediliyor?

08-032. Giriş günü stop kontrolünde stop giriş AOF'undan hesaplanıyor, ama günün düşüğü AOF zamanından önce oluşmuş olabilir; gün içi sıra bilinmezken giriş günü stopunun tetiklenip tetiklenmediği nasıl karara bağlanıyor?

08-033. 30.11.2015–12.03.2020 arası ±%20 limit varken stop dolumu stop fiyatından varsayılıyor; bu dönemde boşluklu stop sıklığı ve gerçekleşen kayıp %1 riskin kaç katı olabilir, ve dönem ayrımlı raporlanıyor mu?

08-034. Endekse Bağlı Devre Kesici günlerinde (2020-08'den beri) ve Şubat 2023 gibi birkaç gün borsanın kapalı kaldığı durumlarda Takvim ve simülatör stop, AOF ve faiz hesabını nasıl işliyor? TASARIM 4 yalnız tatil ve yarım günü anıyor.

08-035. Sermaye eğrisi kapanışla değerleniyorsa kilitli tabandaki, satılamayan pozisyon kapanış fiyatından mı yoksa gerçekçi bir değerle mi hesaplanıyor? Bu seçim %25 düşüş kuralını (5.12 sonu) doğrudan etkiler.

08-036. Pozisyon açıkken işlem sırası kapanan, işlem yasağı gelen veya brüt takas/tek fiyat tedbirine giren hissede çıkış değeri neye göre hesaplanıyor? Açık soru 8.4 bunu yalnız "yanlılık" diye yazıyor.

08-037. Evren her ay başı yeniden seçiliyorsa açık pozisyondaki hisse evrenden düştüğünde pozisyon kapanıyor mu, korunuyor mu? Korunuyorsa o hisse için Adım fonksiyonu hangi veriyle çalışmaya devam ediyor?

## C. Masraf varsayımları

08-038. Sabit %0,3 "komisyon, BSMV, kayma, açılışta kovalama birlikte" diyor; AOF modeli zaten açılışta kovalamayı dışarıda bırakıyorsa bu bileşen çift sayım olmuyor mu, ve bileşenlerin ayrı payı nerede yazılı?

08-039. Aracı kurumların emir başı asgari komisyon ve işlem tutarına göre kademeli oranları, 1.000.000 TL ölçeğinde ve Levent'in gerçek ölçeğinde yüzdesel bir masrafa nasıl çevriliyor?

08-040. S2-2 "sınama ölçekten bağımsız oranlarla okunur" diyor; %2 likidite tavanı, fiyat adımı, lot yuvarlaması ve asgari komisyon ölçeğe bağlı olduğuna göre bu iddia hangi koşulda doğrudur?

08-041. Düşük fiyatlı hissede (birkaç TL) tek fiyat adımı yüzde olarak büyüktür; sabit %0,3 kayma bu hisseler için hangi spread dağılımını varsayıyor ve bu bir veriyle sınanabilir mi?

08-042. Stop çıkışları (gap günleri, panik) ortalama işlemden belirgin biçimde kötü dolum alır; aynı sabit %0,3 stop çıkışlarına ve normal girişlere birlikte uygulanıyorsa bu adverse seçilimi nasıl yansıtıyor?

08-043. BSMV ve komisyon oranları 2015–2026 arasında değiştiyse tek sabit oran tüm dönem için nasıl gerekçelendiriliyor? Değişmediyse bu hangi kaynakla doğrulandı?

08-044. Hisse kazancı stopajı ve temettü stopajı doğrulanmadı (S2-6, 8.6); "%0,5 senaryosu bir kısmını karşılar" cümlesi hangi hesaba dayanıyor ve "kısmını" ne kadarı?

08-045. %0,1 / %0,3 / %0,5 üçlüsü hangi gerçek veriye veya komisyon tarifesine dayanıyor; dayanak yoksa üst sınırın %0,5 olması kabul kararını neden yeterince sert yapıyor?

08-046. %0,3 kayma varsayımı hiçbir gerçek dolumla kalibre edilmiyor; kâğıt üstü canlı dönemde (5.8) Levent'in gerçek dolum fiyatları AOF'a karşı kaydedilip kayma ölçülecek mi?

08-047. Çift bölmesi çok sık geçiş yapar, tek hisse bölmesi seyrek; masraf duyarlılığı ve %0,5 şartı bu devir hızı farkını ve K1 rastgele kuralının farklı devir hızını nasıl hesaba katıyor?

08-048. Portföy %0,3'ü ödüyor; K2 eşit ağırlıklı sepet ve K1 rastgele kural aynı masrafı ödüyor mu, sepet ay başı yeniden dengelemede masraf ödüyor mu? Brüt sepete karşı net portföy karşılaştırması adil olur mu?

08-049. Tansu'nun VAKBN–GARAN raporundaki toplam maliyet 2.054,78 TL (6 geçiş, 100.000 TL) bizim %0,3/yön varsayımıyla uyumlu mu? Sadakat kontrolü (KURALLAR 4) maliyet formülünü yeniden üretmeyi kapsıyor mu?

08-050. Çift bölmesinde bir geçiş bir satış ve bir alıştır; %0,3 "her yönde" olduğuna göre geçiş maliyeti %0,6 mı, yoksa tek %0,3 mü? Simülatör bunu nasıl uyguluyor?

## D. Çift bölmesi

08-051. TASARIM 5.6 "her çift payı her an çiftin bir hissesindedir" derken hemen ardından "ilk sinyale kadar nakit" ve yıllık seçimde düşen çiftin payı yeni çifte geçiyor; pay ne zaman nakit, ne zaman hissede, bu tutarlı tanımlı mı?

08-052. p < 0,05 süzgeci 5'ten az çift verirse boş paylar nakitte mi kalıyor yoksa kalan çiftlere mi dağılıyor? Nakitte kalıyorsa bölmenin K2'ye göre fazla getirisi o yıl nasıl yorumlanır?

08-053. Bir yılda hiçbir çift süzgeci geçmezse bölme bütün yıl nakit olur; K2 (aynı çiftlerin 50/50 tutulması) boş küme olduğunda fazla getiri serisi o yıl için nasıl tanımlı?

08-054. Yıllık seçimde düşen çiftin pozisyonu kapanırken zorunlu çıkışın maliyeti, günü (AOF) ve çıkış gününün taban kilidi olma durumu nasıl ele alınıyor; yılın ilk günü çıkışlar ve girişler birikmiyor mu?

08-055. Çift payı 200.000 TL tek hissede; %2 tavanı için ≥10.000.000 TL medyan günlük işlem tutarı gerekir. Küçük bir bacakta tavan bağlayıcıysa geçiş kısmen mi yapılır, kalan nakit mi, ve "her an bir hissede" kuralı bozulur mu?

08-056. 5 çift eşit paylıysa çiftler arası yeniden dengeleme var mı; kazanan çiftin payı büyür mü, bileşik mi sabit mi? K2'nin 50/50 tutması hangi ağırlık kuralını izliyor?

08-057. Çift rotasyonunda stop yok; Tansu'nun kendi bağı kopmuş çift örneği ≈−%21, VAKBN–GARAN MaxDD −%27,44 (D bölümü) ve %25 düşüş kuralı varken Tansu'nun en iyi örneği bile kuralı geçmiyor; çift bölmesi bu kural altında nasıl sınanıyor?

08-058. Rotasyonda "kapanan işlem" yok, geçiş var; çift bölmesinde "işlem" bir geçiş mi, bir tutuş dönemi mi? İşlem seviyesi fazla getiri (5.7) ve işlem sayısı bu birimi nasıl kullanıyor?

08-059. Çift bölmesi her an tek hissede (%100 yoğun), K2 ise 50/50; günlük fazla getiri serisi iki farklı risk profilinin farkıdır, bu varyans farkı fazla getirinin yorumunda nasıl ayrıştırılıyor? K2'nin başlangıç tarihi bölmenin ilk sinyaliyle hizalı mı?

08-060. Tansu'nun çiftleri "ayrıca gösterilir" (5.6); hangi sermayeyle gösteriliyor: Tansu'nun tek çiftte 100.000 TL'sinin ölçeğiyle mi, yoksa 5 çiftli bölmedeki 200.000 TL'lik payla mı?

08-061. Çift bölmesinde kabul, 6 aylık canlı dönemde günlük fazla getiri serisine bağlı (5.8); yaklaşık 125 günlük seri 20 günlük bloklarla yeniden örneklendiğinde yalnız 6 civarı blok oluşur, bu güven aralığı anlamlı sayılabilir mi?

08-062. Tansu'nun VAKBN grafiğinde "piyasada kalma %72,27", yani yaklaşık %28 nakit; Tansu'nun sonucunda nakit faizi yok, bizim simülatörde var; sadakat karşılaştırmasında bu fark nasıl izole ediliyor?

## E. Nakit faizi

08-063. TASARIM 4 "faiz: TCMB politika faizi, TLREF yalnız 2018 sonrası" diyor, 5.6 "2015–2017 politika faizi, sonrası TLREF" diyor; ikisi çelişiyor ve TLREF hesaplamasının 2018-12-28'de başladığı düşünülürse 2018'in büyük kısmı için hangi seri kullanılıyor?

08-064. veri-kaynaklari.md'ye göre TLREF 2018-12-28'den hesaplanıyor, 2019-06-17'de yayınlanmaya başladı; 2019'un ilk yarısında yayımlanmamış serinin geriye dönük hesaplanmış değerleri mi kullanılıyor, ve bu veri nereden alınıyor?

08-065. borsapy politika faizi serisi 2026-01-23'te bitiyor, bugün 05.10.2026; Ocak–Ekim 2026'daki toplantı kararları nasıl doldurulacak, ileri doldurma son basamağı sabit tutuyorsa faiz ve tüm sonuçlar hatalı olabilir mi?

08-066. borsapy'nin `lending` sütununun gerçekten 1 hafta repo faizi olduğu doğrulanmadı (veri-kaynaklari 6); bu sütun koridor üst bandı olabilirse boştaki nakit getirisi neden Bölüm 8 açık sorularında yer almıyor?

08-067. Politika faizi ile fiili gecelik fonlama maliyeti 2015–2018'de ve 2021–2023'te ayrışıyordu; nakit getirisi politika faizine göre alındığında hangi dönemde nakit getirisi gerçeğin altında ya da üstünde kalıyor ve bunun sınaması yapıldı mı?

08-068. Bireysel yatırımcı boştaki nakde politika faizini ya da TLREF'i kazanamaz (mevduat, repo, para piyasası fonu, stopaj, spread); simülatör hangi aracı ve hangi vergiyi/spreadi varsayıyor?

08-069. Faiz günlük nasıl tahakkuk ediyor: takvim günü (hafta sonu ve tatil dahil) mü iş günü mü, /365 mi /360 mı, bileşik mi basit mi? Bu tercih yüksek faizli yıllarda getiriyi anlamlı biçimde değiştirir.

08-070. Sinyal gününün kapanışı ile ertesi günün AOF girişi arasındaki nakit, ve satıştan gelen valördeki nakit faiz kazanıyor mu? Kazanmıyorsa ya da kazanıyorsa hangi gün sayımıyla?

08-071. Açık sorular (Bölüm 8) vergi, yayın saati, hacim birimi gibi konuları sayarken faiz serisi kodunun doğrulanamaması (veri-kaynaklari 8.6) neden listede yok?

08-072. K3 "portföy sonucu zaten faize karşı okunur" diyor ama faize karşı açık bir fazla getiri tanımı yok; hangi büyüklük "faize karşı" okunuyor ve bu okuma 5.12 ölçütlerinden hangisinde kullanılıyor?

08-073. Yüksek faiz rejiminde (nakit getirisi nominal olarak hisseyle yarışır) "hiç işlem yapma" portföyü raporlanıyor mu ve kuralın ondan istatistiksel olarak ayrıldığı ölçüte giriyor mu?

08-074. EVDS anahtarı henüz alınmadı (veri-kaynaklari 6); politika faizi kodu doğrulanamadığı için faiz bileşeni olmadan simülatör çalıştırılırsa sonuçlar rapora "nakit faizsiz" diye işaretlenerek mi çıkıyor?

## F. Fazla getiri tanımları

08-075. K2 eşit ağırlıklı sepet tam yatırımlı, portföy ise ortalama kısmen nakitte; 5.12.2 "K2'ye göre fazla getiri" ortalama yatırımlı oran farkını nasıl hesaba katıyor? Yüksek faizde nakit tutmak ve yükselen piyasada nakit tutmak aynı ölçütle nasıl yorumlanır?

08-076. K2 sepetinin yeniden dengeleme sıklığı (günlük, aylık, hiç) 5.7'de yazılı değil; günlük eşit ağırlıklı yeniden dengeleme düşük likiditeli hisselerde getiri primi üretebilir, hangi sıklık kullanılıyor?

08-077. İşlem seviyesi fazla getiri "işlemin getirisi − aynı tutma süresinde sepet getirisi" ise sepet getirisi kapanıştan kapanışa mı AOF'tan AOF'a mı hesaplanıyor, ve işlem getirisi masraflı mı masrafsız mı?

08-078. İşlem seviyesi ve portföy seviyesi fazla getiri farklı işaret verirse (slot sınırı, boyutlandırma, nakit) 5.12.1'deki "fazla getiri" hangisi; karar için hangisi birincil?

08-079. K1 rastgele kural portföyü de boştaki nakitte faiz kazanıyor mu? Kazanmıyorsa kural ile rastgele kural arasındaki fark yatırımlı kalma süresine, faize mi yoksa girişlerin kalitesine mi atfediliyor?

08-080. K1 rastgele girişlerde çıkış kuralı aynı (SMA250/2 ATR) ise tutma süresi dağılımı ve slot doluluğu kuraldan farklı olabilir; pozisyon sınırı etkisi (S2-42) bu farkı fazla getiriden nasıl ayırıyor?

08-081. K1 (a) "aynı gün, başka hisse" seçiminde başka hissenin likiditesi %2 tavanını farklı biçimde bağlar ve boyut, dolayısıyla maruziyet farklılaşır; eşleştirme boyut ya da maruziyet düzeyinde de yapılıyor mu?

08-082. İlk yıl(lar)da SMA250/252 günlük ısınma yüzünden işlem yokken portföy nakit faizi kazanıyor ve K2 sepeti piyasada; bu günler günlük fazla getiri serisine, bootstrap'e ve 5.12 ölçütlerine dahil mi?

08-083. İleri yürümede her yılın sınaması 1.000.000 TL'den mi başlıyor yoksa sermaye ve açık pozisyonlar yıldan yıla taşınıyor mu? Taşınmıyorsa yıl sınırında pozisyonlar zorla mı kapanıyor ve düşüş kuralı hangi eğriye bakıyor?

08-084. 5.12.4 "yılların en az %60'ında fazla getiri pozitif" 2015–2026 yaklaşık 10 ilerleme yılında 6 yıla denk gelir; fazla getirinin yıllık değeri hangi tanımla (günlük farkların toplamı, bileşik mi) hesaplanıyor?

## G. Enflasyon ve düşüş kuralı

08-085. TASARIM 5, sınamanın amacını sonucu "enflasyondan ayırmak" diye koyuyor; hiçbir ölçütte reel (TÜFE'ye göre) getiri yok, bu iddia hangi hesapla gerçekleşiyor?

08-086. 2021–2023'te politika faizi enflasyonun çok altındaydı (negatif reel faiz) ve hisse nominal getirileri yüksekti; yılların %60'ı ölçütü ve kâğıt üstü dönem bu rejimden hangi biçimde bağımsızlaştırılıyor?

08-087. %25 düşüş ve 12 ay "düşüşte kalma" nominal TL tepe noktasına göre mi hesaplanıyor; yüksek enflasyonda nominal tepe çabuk aşılsa da reel kayıp sürebilir, kural neden nominal?

08-088. Portföy kuralı "aileden bağımsız" (5.12 sonu) ama 5.6 aileleri ayrı sermayelerle ölçüyor; kural hangi sermaye eğrisine uygulanır, birleşik portföy kabulden sonra kurulacaksa kural kabul ölçütü olarak nasıl çalışıyor?

08-089. Düşüş kuralı ihlal edilirse sonuç ailenin reddi mi, boyutun küçültülmesi mi, uyarı mı? 5.12'deki "hepsi sağlanırsa Canlı" ile portföy kuralı arasındaki ilişki yazılı değil.

08-090. Düşüş kuralı %0,1, %0,3, %0,5 masraf senaryolarından hangisinde sağlanmalı; ve düşüş nakit faizi dahil eğrinin mi, faizsiz eğrinin mi düşüşü?

08-091. Dolar bazı karşılaştırma ilk sürümde yok (Kesilecek); 6 aylık canlı dönemde TL değer kaybı ya da faiz indirimi rejimi değişirse "etki doğrulamanın en az yarısı" kıyası nominal TL farkında mı yapılıyor?

08-092. 5.12.6'daki "doğrulamadaki etki" birimi nedir: işlem başına yüzde fark mı, günlük portföy fazla getirisi mi, yıllık mı? İşlem sayısı ve nakit oranı farklı olan iki dönem aynı birimle nasıl kıyaslanıyor?

## H. Tansu'ya sadakat, parametre kaydı ve uygulama

08-093. Tansu'nun SMRTG ve ISKPL sonuçları tüm sermayeyle bileşik, masrafsız, tek hissede; bizim %1 risk, %10 tavan ve masrafla bu sonuçlar hiç yeniden üretilemez. "Önce sadakat" ilkesi AB=CD için sermaye paketini hangi noktada Tansu'dan ayırıyor ve ayrım ekranda yazılı mı?

08-094. 10 pozisyon, %10 tavan ve %2 likidite tavanı Tansu kaynaklarında yok (E K1 "belirsiz"); bu üç parametre YORUM olarak Holm deneme sayısına giriyor mu, ve 5.10 sağlamlık ızgarasında oynatılıyor mu?

08-095. "Tansu'nun risk paketi" (%1, 2 ATR, SMA250) NotebookLM infografiğinden alınıyor ve KURALLAR §1'e göre Tansu'nun kendi aracından çıkmıyor; TASARIM 5.5 bunu "Tansu'nun" paketi diye sunmuyor mu, P5'teki "ekranda Tansu'nun sistemi diye sunulmaz" ilkesiyle tutarlı mı?

08-096. TASARIM 5.5 SMA250 çıkışını "ertesi açılışta" diyor, 5.3 ise açılış verisi olmadığı için "ertesi AOF" diyor; çıkış dolum fiyatı hangisi, ve iki cümle aynı kodda nasıl tek davranışa iniyor?

08-097. Aileler ayrı sermayede ölçülürken Levent gerçek hayatta tek hesapla aynı hissede iki ailenin sinyalini alabilir; birleşik portföyde aynı hissede çifte pozisyon, toplam risk ve %25 düşüş kuralı hangi aşamada sınanıyor?

08-098. Kartta "sermayenin yüzdesi ve 1.000.000 TL için adet" yazıyor (6.4); %2 likidite tavanı ve %10 tavan kartta gösterilen adedi kısıtlıyor mu, ve Levent'in sermayesi 1.000.000 TL'den farklıysa tavanlar kartta nasıl yeniden hesaplanıyor?

08-099. Canlıda AOF'a emir vermek mümkün değil (AOF gün sonunda bilinir); canlı kâğıt dönemi dolumu hangi fiyattan kaydediyor, ve backtest AOF dolumu ile canlı gerçekleşen dolum arasındaki sistematik fark nerede ölçülüyor?

08-100. İşlem getirisi hem ham fiyattan nakit hesabıyla (adet, masraf) hem de düzeltilmiş HGDG serisinden istatistik için hesaplanıyorsa iki hesabın aynı işlemde aynı getiriyi verdiğini kontrol eden bir sınama var mı?
