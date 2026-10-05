# Sorular 06: EMA sıkışması

06-001. B-momentum 1. bölüm "Ratio %" formülünün görselde olmadığını açıkça söylüyor; KURALLAR 3 "bant ≤ %1,2" yazarken hangi büyüklüğü %1,2 ile karşılaştırdığını Tansu'dan alıntılamadan nasıl "birinci el" diyebiliyor?

06-002. aileler.py bandı (max−min)/Close ile hesaplıyor; paydanın günlük kapanış, EMA ortalaması, EMA200 veya en düşük EMA olması aynı dönemi %1,2 altında veya üstünde bırakabilir, hangi payda KRDMD'nin %0,64'ünü üretiyor?

06-003. KRDMD ortalama oranı %0,64 tek bir sayıdır; "sadakat kontrolü" bu sayıyı yeniden üretmek için kaç aday formül deneyecek ve denenen formül sayısı arttıkça "eşleşti" iddiasının anlamı nasıl korunacak?

06-004. B-momentum 1. bölüm "Ratio sıkışma boyunca ~0.5-1" diyor; ortalama %0,64 ile bu aralık, max−min/Close formülüyle tutarlı mı, yoksa CV veya ATR-normal formülle de aynı ortalama çıkabilir mi?

06-005. Lejanttaki EMA değerleri (31.92, 30.74, 29.58, 28.43) Son Kapanış 36.68'e göre hesaplandığında bant yaklaşık %9,5 çıkıyor; bu sayılar sıkışma günü değil grafik sonu değeri olduğuna göre, bunlardan formül doğrulanabilir mi?

06-006. Görselde "20 gün" yazıyor, 17.12.2025–14.01.2026 arası 28 takvim günü; BIST tatilleri (yılbaşı 1 Ocak) düşüldüğünde bar sayısı gerçekten 20 mi, ve bu 20 sayısı sadakat testinin geçme ölçütü olarak kullanılacak mı?

06-007. "Min 3 gün" ardışık barlar mı demek, yoksa pencere içinde toplam 3 bar mı; aileler.py `rolling(10).sum() >= 3` ile ardışık olmayan günleri de sayıyor, KURALLAR 3 ise "en az 3 gün" diyor; hangisi esas?

06-008. aileler.py'deki rolling(10) penceresi Tansu'nun hiçbir görselinde yok; bu 10 sayısı nereden geldi ve KURALLAR 3'teki "sıkışma bittikten sonraki 10 gün" ile aynı 10 mu, farklı mı?

06-009. Sıkışma "bitti" ne zaman sayılır: ilk %1,2 üstü bar mı, ardışık iki bar mı, yoksa oran %1,2'nin üstüne çıkıp geri dönerse dönem bölünür mü; KRDMD dönemi bu kurala göre tek parça mı kalıyor?

06-010. Oran %1,2 çizgisi etrafında dalgalanırsa (1,19–1,21–1,18) dönem parçalanır ve "min 3 gün" yeniden başlar; histerezis yok, bu durum 520 sayımını nasıl şişirir veya azaltır?

06-011. "Son 130 mum" pencere Tansu'nun tarama penceresidir; sistem tüm tarihte sıkışma ararken bu pencereyi görmezden geliyor, 130 mumdan eski bir sıkışma Tansu'nun aracında hiç görünmeyeceğine göre sadakat bozulmuyor mu?

06-012. EMA200 için ilk 200 bar uyarlama gerektirir; aileler.py `min_periods=gun` ile ilk 199 barı NaN bırakıyor, bu durumda 2015 sonrası işlem gören her hissenin ilk ~10 ayı sinyalsiz kalır; TASARIM'da bu kayıp ölçülmüş mü?

06-013. adjust=False ve ilk değeri tohum alan özyinelemeli EMA, başlangıçta SMA tohumlayan EMA'dan (TradingView) farklı değerler verir; Tansu'nun aracı hangisini kullanıyor ve fark %1,2 eşiği için önemli mi?

06-014. EMA200 değeri, veri başlangıç tarihine göre (2015 mi, 2010 mu, hisse halka arz tarihi mi) bin onda birler seviyesinde değişir; sınama verisinin başlangıç tarihi sonuçlara ne kadar duyarlı ve bu duyarlılık raporlanacak mı?

06-015. EMA hesabı düzeltilmiş (bedelsiz/temettü) fiyatla mı, ham fiyatla mı yapılıyor; BIST'te sık bedelsiz sermaye artırımı varken ham fiyatta EMA'lar bölünme gününde sahte bir sıçrama yapar ve oranı yapay bozar.

06-016. Yahoo `.IS` Adj Close temettüyü de düzeltir; EMA için düzeltilmiş, işlem fiyatı için ham fiyat kullanılırsa sıkışma oranı (EMA düzeltilmiş) ile kırılım seviyesi (ham) farklı ölçeklerde karşılaştırılır; bu tutarsızlık engellendi mi?

06-017. Yahoo bedelsiz bölünmeleri bazen geç veya hatalı düzeltir; hatalı düzeltilmiş bir hissede EMA200'ün sıçraması sahte "sıkışma" veya sahte kırılım üretirse bunu ayıklayan bir veri kontrolü var mı?

06-018. Tansu'nun KRDMD grafiği hangi fiyat serisinde çizildi (yfinance varsayılanı sürüme göre auto_adjust değiştiriyor, B-momentum 24. bölüm uyarısı); sadakat kontrolü hangi sürümle yapıldı ve sonuç sürüme bağlı mı?

06-019. KRDMD örneği 2025-12-17 → 2026-01-14 iken sistemin kullandığı veri bu dönemi içeriyor mu; veri araştırması (veri-kaynaklari.md) Yahoo'nun KRDMD için aynı kapanışları verdiğini doğruladı mı?

06-020. Sadakat testi yalnızca KRDMD tek örneğine dayanıyor; tek örnekte hem formül hem eşik ayarlanırsa parametre uydurma (overfitting) olur, formülü doğrulayacak ikinci bağımsız örnek var mı?

06-021. Tek örneği yeniden üretmek formülün doğru olduğunu kanıtlamaz, çünkü birçok formül tek bir dönemi aynı çıkarabilir; kontrol hangi yanlış formülü reddedebilecek kadar ayırt edici?

06-022. KURALLAR satır 30 "Tek örnek (sıkışmadan sonra yükseliş)" diyor; seçilmiş pozitif örnek olduğu için hayatta kalma yanlılığı var, Tansu'nun "başarısız sıkışma" örneği hiç gösterilmedi mi?

06-023. ICBCT "Pre Signal" görselinde "AKTİF 3g" ve "▲1 BULL ▼0 BEAR ⚡0 CONFLICT" var; BEAR ve CONFLICT sayaçları aşağı yönlü kırılım olduğunu gösterir, KURALLAR 3 neden yalnız yukarı kırılımı alıyor?

06-024. ICBCT'de Tansu "parametreleri açıklayamam" diyor; KRDMD aracıyla ICBCT aracı aynı araç mı, ve KRDMD parametrelerinin (%1,2, 3 gün) ICBCT'ye uygulandığı varsayımı nereden geliyor?

06-025. "Pre Signal" adı, kırılımdan önce erken sinyal anlamına gelir; KURALLAR 3 ise kırılım sonrası giriş yazıyor, bu Tansu'nun "Pre Signal" fikrini tersine çevirmiyor mu?

06-026. ICBCT'de "bir günde %5" sonucu bildirilmiş; sıkışma kırılımı genellikle günler sürer, tek günde %5 BIST tavan-taban bandı içinde kalan bir hareket mi ve bu iddia sistem hedefiyle nasıl uzlaşıyor?

06-027. KURALLAR 3 girişi "sıkışma bittikten sonraki 10 gün içinde, kapanış sıkışma dönemindeki en yüksek fiyatın üstüne çıkarsa" diyor; "en yüksek fiyat" günlük High mı yoksa Close mu, ve sıkışma dönemi 20 gün ise bu tepe 20 günlük High ile aynı mı?

06-028. aileler.py kırılımı "20 günlük tepe (High.shift(1).rolling(20).max())" üzerinden tanımlıyor, KURALLAR 3 ise "sıkışma dönemindeki en yüksek"; iki tanım farklı, hangisi sınanıyor ve prototipin sonuçları hâlâ geçerli mi?

06-029. Kırılım "sıkışma bittikten sonra" arıyorsa sıkışma sürerken olan kırılım (oran %1,2 altındayken fiyat tepeyi aşıyor) sayılmıyor; EMA'lar yavaş olduğundan fiyat sıkışma devam ederken kırmak zorunda değil mi?

06-030. EMA200 ve EMA100 gecikmeli olduğundan, fiyat sıkışma tepesini aştığı gün oran bozulmuş olmayabilir; "bitti" tanımı fiyat kırılımına bağlıysa döngüsel olmuyor mu?

06-031. 10 günlük giriş penceresi hangi veriden seçildi; Tansu bu pencereyi hiç söylemedi (B-momentum 1: giriş yok), 5, 10, 20 gün seçeneklerinden biri sonuç görüldükten sonra seçildiyse bu bir veri avcılığı değil mi?

06-032. Pencere içinde birden fazla kapanış tepeyi aşarsa yalnız ilk kırılım mı alınır, ve sinyal sonrası stop ile çıkılan işlemin aynı dönemde ikinci kez giriş üretmesi engelleniyor mu?

06-033. "Sıkışma döneminin en yüksek fiyatı" dönem bittiği gün belli olur; dönem sonu ile giriş kararının günü arasındaki ilişki, dönemin bitişini ancak ertesi gün bilen bir algoritmada ileri bakış (look-ahead) yaratır mı?

06-034. Dönem ortalama oranı (%0,64) ve dönem süresi (20 gün) dönemin tamamı bilindikten sonra hesaplanır; bu özetler giriş filtresi olarak kullanılırsa, dönem içindeki bir gün için gelecek bilgisini kullanmış olmaz mı?

06-035. Dönemin başlangıç günü yalnızca "3 gün doldu" anında kesinleşir; sinyal günü dönem kesinleştikten sonra mı yoksa dönem bitiminden mi sayılıyor, ve sınama motorunda bu iki gün ayrımı nasıl uygulanıyor?

06-036. aileler.py'de `sikisma` terimi rolling(10) içinde yer alıyor ve kırılım aynı gün değerlendiriliyor; bu iki koşulun aynı barda birlikte doğru olması, sıkışma sürerken kırılım gerektirir, KURALLAR 3 ise sıkışma bittikten sonra kırılım diyor, hangi anlam hedeflendi?

06-037. KURALLAR 3'te hacim koşulu yok, aileler.py'de `Volume > 1.5 × 20 günlük medyan` var; hacim teyidi neden katalogdan düştü ve bu karar Tansu'nun görsellerinde hangi kanıta dayanıyor?

06-038. Tansu'nun gp-64 (hacimle EMA kırılımı) ve gp-68 (hacimli KDE kırılımı) örnekleri hacmi şart gösteriyor; hacimsiz bir kırılım kuralını "Tansu'nun EMA sıkışması" diye sunmak sadakat ihlali mi?

06-039. Hacim teyidi eklenirse 1,5× çarpanı ve 20 günlük medyan Tansu'dan gelmiyor; bu iki sayı YORUM olarak etiketlendi mi, ve sorgu-2'deki cevap bunu açıkladı mı?

06-040. Hacim koşulu kataloğa eklenmezse sahte kırılım (false breakout) oranı yükselir; sınama sonuçlarında sahte kırılım oranı ayrı raporlanacak mı?

06-041. BIST'te açılış ve kapanış seansı hacimleri tek günlük Volume'a gömülüdür; tek bir blok işlem veya kapanış seansı emri günlük hacmi 1,5× aşırtırsa teyit geçersiz olur mu?

06-042. Yahoo `.IS` günlük Volume'ının lot mu TL mi olduğu hissede değişmez, ama bedelsiz sonrası lot hacmi düzeltilmezse hacim medyanı bölünme sonrası sahte artar; hacim serisi düzeltiliyor mu?

06-043. Sıkışma dönemi sakin geçtiğinden hacim medyanı düşüktür; düşük baz hacim yüzünden sıradan bir günde 1,5× kolayca aşılır, bu eşik sıkışma sonrası hacimden gerçekten ayırt eder mi?

06-044. Kırılım günü hacmi gün sonunda bilinir; kapanışta kırılım ve hacmi doğruladıktan sonra "ertesi açılış" girişi (KURALLAR 3) yerine sistem "ertesi AOF" kullanıyor (KURALLAR satır 103), AOF ile açılış arasındaki fark bu aileyi nasıl etkiler?

06-045. Kırılım günü kapanışa yakın tavan veya sert yükseliş yaşandıysa ertesi gün boşluklu açılır; ertesi AOF ile gerçek erişilebilir fiyat arasındaki fark BIST'te hangi sıklıkla %2'yi aşıyor ve bu fark sınamada modelleniyor mu?

06-046. BIST günlük +%10 tavan ve −%10 taban var; kırılım günü tavan kilitlenirse (alım yapılamaz) ertesi gün de tavan açılırsa giriş mümkün değil, sınama bu işlemleri doldurulmuş sayıyor mu?

06-047. Sıkışma, düşük likiditeli ve dar bantlı hisselerde (ince hisse) sık görülür; EMA'lar birbirine yakın çünkü fiyat hareket etmiyor, bu "sıkışma" mı yoksa işlem görmeyen hisse mi, minimum işlem hacmi filtresi var mı?

06-048. Fiyat adım (tick) büyüklüğü düşük fiyatlı hissede (örneğin 3,62 TL) oranı yüzde olarak büyük adımlarla yapay kuantize eder; %1,2 eşiği tek tick'le aşılabiliyorsa düşük fiyatlı hisselerde sıkışma tanımı güvenilir mi?

06-049. Uzun süre durağan fiyat (fiyat çıpası, "ince tahta") ile EMA'lar kendiliğinden birleşir; bu tür hisselerde 520 dönemin ne kadarı gerçek sıkışma ve ne kadarı hareketsiz hisse?

06-050. Dört EMA'nın %1,2 bant içinde olması fiyatın EMA'lardan uzak olmasına da izin verir; fiyatın kendisinin bandın içinde olması gerekmiyor mu, ve KRDMD'de fiyat sıkışma sırasında bantta mıydı?

06-051. Bant paydası Close ise, Close EMA'lardan yukarıda veya aşağıda uzaksa payda sabit kalırken EMA'lar birleşir; paydanın günlük oynaması oranı gereksiz oynatır, EMA ortalaması paydası daha kararlı olmaz mıydı?

06-052. Sıkışma yönü (EMA dizilimi) gözetilmiyor: EMA20 > EMA200 mü yoksa tersi mi; düşüş eğiliminden gelen bir sıkışmanın yukarı kırılımı ile yükseliş eğiliminden gelenin aynı kural olması Tansu'nun metnine uyar mı?

06-053. gp-68'de Tansu, sıkışmadan sonra "50>100>200 dizilimine geçiş" şartı koyuyor (ikinci el); bu dizilim koşulu kataloğa girmedi, neden?

06-054. KURALLAR 3 "Hedef yok (Tansu vermedi)" diyor; hedefsiz ve stop'u risk paketine bırakan bir kuralın R-çoklusu ve beklenen değeri nasıl yorumlanacak ve hangi çıkış kuralı sonucu belirliyor?

06-055. Stop "risk paketi"ne bırakılmış; risk paketi (TASARIM 5.5) AB=CD için tasarlandı, sıkışma kırılımında stop uzaklığı kırılım tepesi ile EMA bandı arasındaysa ATR tabanlı stop ile uyuşuyor mu?

06-056. TASARIM 5.6 işlem başına %1 risk ve pozisyon başına %10 sermaye üst sınırı koyuyor; sıkışma kırılımında stop sıkı (örneğin %3) ise %1 risk %33 pozisyon demektir, %10 sınırı hep mi bağlayıcı ve gerçek risk %0,3'e mi düşüyor?

06-057. 10 pozisyon üst sınırında "aynı gün sinyal sayısı boş yeri aşarsa en likit önce" (M12) kuralı sıkışma ailesinde BIST'in toplu dönemlerinde (genel piyasa kırılımı) çok sinyalin aynı gün gelmesine yol açar; sıralama sonucu ağırlıklı olarak likit büyük hisseleri mi seçiyor?

06-058. Sıkışma kırılımı piyasa genelinde korele olur (XU100 sıkışması gp-68 örneği); aynı güne yığılan sinyaller bağımsız işlem sayılırsa istatistiksel anlamlılık şişmez mi?

06-059. KURALLAR 98 "99 hissede 11 yılda 520 sıkışma dönemi" diyor; bu sayı ardışık ≥3 gün kuralıyla mı, rolling(10) ile mi, hangi payda ile ve düzeltilmiş mi ham fiyatla sayıldı?

06-060. 520 dönem 99 hisse × 11 yıl demek yaklaşık hisse başına 5,3 dönem; bu rakam "kaba sayım" olarak etiketli, ama sınama için yeterli örnek mi, yoksa EMA200 uyarlama kaybı ve %10 pozisyon sınırı sonrası kaç işlem kalıyor?

06-061. 520 dönemin hepsi bağımsız mı: aynı hisse için komşu iki dönem (kısa ayrılık) tek sıkışmanın bölünmüş hali olabilir, birleştirme kuralı olmadan sayı kaç gerçek olaya karşılık gelir?

06-062. "Sıklık kontrolü" ne için? Sıklık yüksekse kural gevşek, düşükse seyrek diye hangi aralık kabul edilir, ve 520 sayısı geçme veya kalma kararını hangi eşikle belirliyor?

06-063. 99 hisse seçimi 2026'da hayatta olan hisselerdir; 11 yıl içinde işlem dışı kalan veya iflas eden hisseler yoksa hayatta kalma yanlılığı sıklığı ve getiriyi nasıl bozar?

06-064. Yahoo `.IS` verisinde sembol değişimleri (ticker devri, birleşme) 11 yıllık seriyi keser; kesik seride EMA200 yeniden başlar mı yoksa NaN mı kalır, ve hisse sayısı 99 sabit mi?

06-065. Sıkışma kırılımı sınamasında endeks (XU100) rejimi izlenmiyor; 11 yıllık BIST yüksek enflasyon ve nominal yükseliş döneminde her yukarı kırılım kazanç gibi görünür, getiri nominal mi, XU100'e göre mi ölçülüyor?

06-066. TL cinsinden nominal fiyatlarda enflasyon nedeniyle sürekli yükseliş varsa, "yükseliş kırılımı" rastgele giriş kuralına karşı bile pozitif getiri verir; sıkışma kuralının katkısını ayıran bir rastgele-giriş kıyaslaması planlı mı?

06-067. Sınamada karşılaştırma tabanı (benchmark) nedir: al-ve-tut mu, rastgele sinyal mi, sıkışma olmayan kırılım (yalnızca 20 günlük tepe + hacim) mu; sıkışma koşulunun sinyale değer kattığı hangi testle gösterilecek?

06-068. aileler.py'deki ailenin sıkışma kısmı çıkarılıp yalnız "hacimli 20 günlük tepe kırılımı" bırakıldığında sonuç aynı çıkarsa, EMA sıkışması aileyi hiç açıklamıyor demektir; bu çıkarma testi yapıldı mı?

06-069. Sıkışma süre eşiği (3 gün) çok kısa: oran %1,2'nin altındaki 3 günlük geçici bir tesadüf EMA yavaşlığı yüzünden sıkışma sayılır; Tansu'nun KRDMD dönemi 20 gün iken 3 günlük dönemler aynı dünya mı?

06-070. Bir sıkışmada ortalama oran %0,64, eşik %1,2; bant tam eşik civarında kalan dönemlerle (ortalama %1,1) çok sıkı dönemleri aynı kabul etmek Tansu'nun "sıkışma" fikrine uyuyor mu?

06-071. Dört EMA'nın birbirine yakınlığı fiyat volatilitesiyle ölçeklenir; yüksek oynaklıklı hissede (günlük %4) %1,2 asla gerçekleşmeyebilir, düşük oynaklıklı hissede (günlük %0,8) hep gerçekleşebilir, tek sabit eşik hisse evrenini adil tarıyor mu?

06-072. Eşik ve süre için duyarlılık analizi (%1,0 / %1,2 / %1,5 ve 2 / 3 / 5 gün) planlandı mı, yoksa sonuçlar yalnız Tansu'nun tek değerinde mi raporlanacak?

06-073. Tansu B-momentum 1'de ratio ve süre eşiğinin "tasarımcının tecrübesine kalmış" olduğunu söylüyor; yani eşikler ayarlanabilir demek, bu durumda %1,2 ve 3 gün katalogda neden sabit kural gibi "birinci el" etiketi taşıyor?

06-074. Sınama dönemi 11 yıl ise eşik ve pencere kararları hangi dönemde seçildi; seçim dönemi ile test dönemi ayrıldı mı, ya da 2025-12 KRDMD örneği (en yeni dönem) eğitim mi test mi sayılıyor?

06-075. KRDMD örneği Aralık 2025 – Ocak 2026 arasında, kural bu örnekten çıkarıldı ve aynı örnekle doğrulandı; bu döngüsel doğrulama dışında kural tasarımı hangi dışarıdan örnekle sınanacak?

06-076. KURALLAR "sıkışmadan sonra yükseliş" diyor; B-momentum 1 yükselişin sıkışmadan sonra 36.68'e kadar gittiğini (28.43 EMA200'e göre %29) gösteriyor, bu getirinin ne kadarı kırılım girişiyle yakalanabilir ve girişin bu örnekte hangi gün olacağı hesaplandı mı?

06-077. KRDMD örneğinde sistemin kuralı (10 gün içinde, dönem tepesi üstünde kapanış) Tansu'nun gösterdiği hareketi gerçekten yakalıyor mu; yakalamıyorsa kural Tansu'nun örneğiyle bile örtüşmüyor demektir, bu kontrol yapıldı mı?

06-078. KRDMD'nin ardından görülen "%10+ ratio" sıçraması kırılımın EMA'ları fiyatla birlikte açtığını gösterir; ratio kırılımdan önce mi yoksa sonra mı %1,2'yi geçti, ve bu sıra "bitiş" tanımıyla uyuşuyor mu?

06-079. EMA20 hızlı, EMA200 yavaş; fiyat sıkışma tepesini kırınca EMA20 hızla yükselir ve oran %1,2'yi kırılım gününden önce de geçebilir; bu durumda "sıkışma bittikten sonraki 10 gün" penceresi kırılımdan önce kapanır mı?

06-080. Sıkışma bitişi ile fiyatın dönem tepesini kırması arasında kırılım olmadan fiyat aşağı kırarsa (aşağı sahte hareket) ve sonra yukarı dönerse, sinyal verilir mi ve 10 gün sayacı hangi olayda başlar?

06-081. Dönem tepesi kapanışla mı yoksa gün içi High ile mi tanımlı; High ile tanımlıysa tek bir iğne (fitil) yüzünden tepe yapay yükselir, kırılım zorlaşır; BIST'te açılış/kapanış seansı fiyat oynaklığı bu seçimi hassaslaştırıyor mu?

06-082. Kırılım kapanışla onaylanıyor ama gün içi fitil tepeyi çoktan geçmiş olabilir; sınama "ertesi AOF" ile giriyorsa sahte kırılımın (fitil geri dönüşü) etkisi gerçekçi mi ölçülür?

06-083. "Sahte kırılım" kavramı hiçbir yerde sayısal olarak tanımlı değil; kırılım sonrası kaç gün içinde tepenin altına dönülürse sahte sayılır ve bu oran kural kabul kriterlerinden biri mi?

06-084. Sıkışma kırılımı için kabul kriteri (sorgu-2 veya TASARIM) hangi metriklerle yazılı (isabet, beklenen değer, tarih bazında tutarlılık); yazılı değilse "kural çalıştı" kararını kim, hangi eşikle verecek?

06-085. sorgu-2 yazarının bu aile hakkındaki cevapları (sıkışma oranı, 10 gün, hacim) doğrulanabilir bir kanıta mı dayanıyor yoksa "kaba sayım" mı; aileler.py ve KURALLAR 3 arasındaki hacim farkı sorgu-2'de neden ele alınmadı?

06-086. aileler.py eski prototip olarak duruyor; yeni sistem bu dosyayı mı çağırıyor, yoksa KURALLAR 3'ü yeniden yazıyor, ve iki sürüm farklı sonuç verirse "TASARIM'daki kural" hangisini temsil ediyor?

06-087. aileler.py `fillna(False)` ile NaN barları (EMA200 isınması, hacim medyanı) sinyalsiz sayar; bu sessiz davranış sınama raporunda "sinyal yok" ile "veri yok" ayrımını siliyor mu?

06-088. aileler.py `Volume.shift(1)` kullanarak hacim medyanını geçmiş 20 günle sınırlıyor (iyi), ama `High.shift(1).rolling(20)` ile tepeyi de önceki günlerle sınırlıyor; KURALLAR 3'teki "sıkışma dönemi en yüksek" tanımı için aynı ileri-bakış koruması yazılı mı?

06-089. Sıkışma barını tanımlayan oran gün t kapanışıyla hesaplanıyor; sinyal günün kapanışında üretilip aynı kapanış fiyatıyla işlem varsayılırsa (kapanıştan işlem) bu BIST'te uygulanabilir değildir, kapanış tahtasının son emir saati modellendi mi?

06-090. Sıkışma kırılımı sinyali akşam üretilir ve ertesi sabah emir verilir; veri-kaynaklari.md Yahoo gecikmesini ve gün sonu düzeltmelerini (volume güncellemesi) belirtiyorsa, sinyal üretildiği anda veri son hali mi, yoksa sonradan düzeltilen mi kullanılıyor?

06-091. Yahoo günlük Volume'ı gün sonu birkaç saat içinde revize edilebilir; sinyal gecesi alınan Volume ile sınamada kullanılan nihai Volume arasındaki fark hacim eşiğine yakın sinyalleri sessizce değiştirir mi?

06-092. Yahoo `.IS` günlük veride tatil günü ve yarım gün (arife) barları bulunur; arife yarım gününde hacim düşük, dolayısıyla hacim medyanı ve sıkışma sayacı bu barlardan nasıl etkileniyor?

06-093. Aynı sıkışmada hem EMA20/EMA50 hem EMA100/EMA200 çiftleri ayrı ayrı yakınsa, sadece dördü birden değil üçü yakın dönemlerde de Tansu kırılım denemiş olabilir; "dört EMA" şartı Tansu'nun lejantında sabit midir yoksa araç dört EMA'yı yalnızca gösteriyor mu?

06-094. gp-65 ICBCT için "EMA 4 çizgisi 14.44/14.29/14.31/14.42" okunuyor: sıralama EMA20, 50, 100, 200 ile bile bu değerlerde bant yaklaşık %1,0; yani ICBCT'de EMA'lar bu sıraya sahip değil (14.29 en düşük), bu sıra "adlar okunaksız" varsayımını zayıflatmıyor mu?

06-095. gp-71 Dragonfly Doji + EMA sıkışması çıkışı: Tansu sıkışmayı çıkış (exit) bağlamında mı kullanıyor; "sıkışma = giriş" varsayımı ile "sıkışma çıkışı" arasındaki yön çelişkisi katalogda çözüldü mü?

06-096. gp-106 EMA5/8/13 sıkışması demand bölgesinde, gp-65 ve gp-67 EMA20/50/100/200; sistem iki farklı sıkışma ailesini ayırıyor mu yoksa KURALLAR "EMA sıkışması" etiketi hepsini tek aile gibi gösterip sonuçları karıştırıyor mu?

06-097. Sıkışma sonrası yön belirsiz ("yön tetikleyicisi verilmedi"); yalnız yukarı kırılımı almak, aşağı kırılım sinyallerini yok sayarak ailenin gerçek simetrik yapısını (Tansu "yön bağımsız" diyor, gp-36) yarıya indirmiyor mu?

06-098. Tansu gp-36'da "rehavet ortamında fiyat bir yöne kırılacak, yön kırılım sonrası belli olur" diyor; "yalnız alış" TASARIM kuralı bu yön bağımsızlık ilkesini bilerek mi bozuyor ve bunun gerekçesi yazıldı mı?

06-099. TASARIM 5.6 tek hisse bölmesinde "tek pozisyon en fazla %10" ile sıkışma kırılımı sinyalleri BIST küçük hisselerinde yığılırsa (likidite düşük) 1.000.000 TL'lik %10 = 100.000 TL pozisyonun günlük hacmin kaçı olacağı ve piyasa etkisi (slippage) hesaplandı mı?

06-100. KRDMD örneğinin güncel gerçek sonucu ile sistemin üreteceği işlem (giriş günü, çıkış günü, R) hiç yan yana yazıldı mı; yazılmadıysa "Tansu sadakati" iddiası hangi çıktıya karşı ölçülüyor?
