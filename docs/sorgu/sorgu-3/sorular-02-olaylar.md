# Sorular 02: Şirket olayları

02-001. TASARIM 5.1 kendi uyguladığı `SHHE_FIYAT_AYAR_OR` düzeltmesini `HGDG` ile karşılaştırıyor, ama veri-kaynaklari 3.2'ye göre `HGDG` nakit temettüyü de içeriyor; kod 04 kayıtlarının çarpanı temettüyü taşıyor mu, taşımıyorsa karşılaştırma her temettü gününde "fark" üretmez mi?

02-002. Çarpanla düzeltilmiş seri ile `HGDG` aynı İş Yatırım olay tablosundan türüyorsa 5.1'deki karşılaştırma bağımsız doğrulama sayılabilir mi; tablodaki yanlış bir çarpanı hangi adım yakalar?

02-003. TASARIM 5.1 "kodda bir kez uygulanır" diyor; aynı güne düşen birden çok kayıt (ör. kod 03 ile kod 04) için çarpanların uygulama sırası ve olay gününün kendisinin düzeltilip düzeltilmediği nerede tanımlı?

02-004. veri-kaynaklari 1.2'de HEKTS 2021 için yüzdelerden çıkan 0,2646 ile İş Yatırım çarpanı 0,2801 farklı; "çarpanı doğrudan al" kararı, çarpanın resmî Borsa İstanbul baz fiyatıyla tutarlı olduğunu hangi kontrolle gösteriyor?

02-005. TASARIM 8.2 temettü `SHHE_TARIH` değerinin ex-date mi ödeme günü mü olduğunu açık bırakıyor, oysa 5.1 düzeltmeyi ve karantina istisnasını bu tarihe dayandırıyor; bu soru kapanana kadar temettü düzeltmesi hangi tarihle uygulanıyor?

02-006. Temettü tarihi ödeme günüyse ham kapanıştaki düşüş tablodaki günden haftalar önce olur; bu gün "olayla açıklanmayan sıçrama" sayılıp karantinaya girer mi?

02-007. `HGDG` temettüyü brüt mü net mü işliyor; TASARIM 8.6 vergiyi doğrulanmamış bıraktığına göre toplam getiri serisi kural ve K2 getirilerini ne kadar şişiriyor ve %0,5 masraf bunu kapatıyor mu?

02-008. TASARIM 5.1 borsapy ile "farkı %0,5'i aşan günler listelenir" diyor, ama borsapy temettüsüz; her temettü ex-gününde fark eşiği aşılacağına göre liste nasıl okunacak, gürültüden gerçek hata nasıl ayrılacak?

02-009. Fark listesi çıktıktan sonra ne olacağı yazılı değil: hangi kaynak kazanıyor, hata karantina mı oluyor, düzeltme mi yapılıyor; 5.1 "fiyat yamanmaz" derken "çarpanı doğrudan al" ile nasıl uzlaşıyor?

02-010. S2-13 göstergelerin `HGDG`'den hesaplanacağını söylüyor, 5.1 ise ham fiyata kendi çarpanımızı uygulayıp `HGDG` ile yalnız karşılaştırıyor; göstergeler hangi serinin üstünde çalışıyor?

02-011. `HGDG`'nin temettü içerdiği yalnızca CCOLA örneğine dayanıyor ve THYAO için `HGDG/HG` oranı 2015–2024 arasında tek sabit değer (0,9769); bu, düzeltmenin tek bir olaydan geldiğini mi gösterir, THYAO'nun diğer temettü kayıtlarıyla çapraz kontrol edildi mi?

02-012. `HGDG` değerleri iki üç ondalıkla yuvarlanıyorsa (CCOLA 76,62), CCOLA %1000 gibi büyük bedelsizlerden sonra düşük fiyatlı eski serilerde ATR ve günlük getiri yuvarlama gürültüsü taşımaz mı?

02-013. Borsa İstanbul baz fiyatı fiyat adımına yuvarlanır; İş Yatırım çarpanı yuvarlanmış baz fiyattan mı teorik fiyattan mı üretiliyor ve düşük fiyatlı hissede 1 tick'lik sistematik hata birikir mi?

02-014. Kod 09 (temettüden bedelsiz) ve kod 03 kayıtlarında `SHHE_BDSZ_TM_ORAN` ile `SHHE_NAKIT_TM_ORAN` aynı satırda geliyorsa, K2'nin "aynı temettü düzeltmesi" ve rapordaki temettü payı bedelsiz ile nakit ayrılarak nasıl hesaplanır?

02-015. GetSermayeArttirimlari gövdesindeki `"endeksKodu":"09"` bir endeks filtresi mi; endeks dışı ve kapanmış hisselerin olayları tabloda dönüyor mu (veri-kaynaklari 1.1)?

02-016. Hisse başına tek çağrıda boş yanıt dönerse sistem "olay yok" mu "çağrı başarısız" mı sayıyor; çerez/oturum hatasında sessizce olaysız seri üretilmesini ne engelliyor?

02-017. `"yil":0, "zaman":"HEPSI"` ile bütün yılların tek yanıtta kesilmeden geldiği sınandı mı (KAP için 2000 kayıt sınırı gözlenmişti); ~500 hisse × 11 yıl toplu çekimde IP engeli (veri-kaynaklari 1.3) olay kaydı eksikliği olarak mı görünür?

02-018. Kapanmış hisselerin (ASYAB gibi) son günlerinde olay tablosu ve `HGDG` tam mı; iflas, zorunlu pay alımı veya işlem sırası kapanışındaki son fiyat sıçraması karantinaya mı girer yoksa "açıklanamayan" mı sayılır?

02-019. Kod 78 (sermaye azaltımı) çarpanı AYGAZ'da 1,0 çıktı; nakit iadeli sermaye azaltımlarında fiyat gerçekten sürekli kalıyor mu, çarpan 1,0 her 78 kaydı için doğru mu?

02-020. Anlamı bilinmeyen 07, 79, 90, 99 kodları (veri-kaynaklari 8.3) olay gününde bir kayıt olarak bulunduğunda, bu kayıt 5.1'deki "olayla açıklanmış" istisnasını alıp karantina kapısından geçer mi?

02-021. TASARIM 4'teki "bölünme" hisse bölünmesini mi şirket bölünmesini (spin-off) mi kapsıyor; birleşme, bölünme ve pay birleştirme (ters bölünme) olayları hangi kodla geliyor ve çarpanları 1'den büyük olduğunda hiç sınandı mı?

02-022. Sembol değişikliği veya birleşme sonrası seri iki sembole bölünüyorsa göstergeler, evren ve karantina bu kopukluğu nasıl ele alıyor?

02-023. Bedelli sürecinde yeni pay alma hakkı ayrı bir sembolle işlem görüyor; hak sembollerinin ham serisi İş Yatırım'dan geliyorsa evren ve sinyal taramasına ayrı bir hisse gibi sızmasını ne engelliyor?

02-024. veri-kaynaklari 1.2 bedelsiz için kayıt tarihinin gerçek işlem günü olduğunu 5 vakayla doğruluyor, temettü için doğrulama yok; 5.1'in karantina kuralı temettü tarihlerine de aynı güveni mi gösteriyor?

02-025. Temettü avansı, ara temettü ve taksitli temettü ayrı kayıt mı geliyor; aynı yıl birden çok kayıt çakışırsa çarpan zinciri ve karantina nasıl işler?

02-026. TASARIM 4 yalnız "ham fiyat anlık görüntüsü"nü tarihli ve değişmez tutacağını söylüyor; olay tablosu ve `HGDG` de anlık görüntüye giriyor mu, girmiyorsa 5.1'deki `HGDG` karşılaştırması tekrar üretilebilir mi?

02-027. İş Yatırım olay tablosuna sonradan eklenen veya düzeltilen kayıtlar geçmiş koşuların düzeltilmiş serisini sessizce değiştirir; tablo kayıt tarihi tutuyor mu, nokta-zamanlı (point-in-time) yeniden üretim mümkün mü?

02-028. 5.1 karantinada "o hisse o pencerede sınamadan çıkar" diyor ama pencerenin uzunluğunu vermiyor; pencere sıçramadan önceki göstergeler ısınma aralığını (ör. SMA250) kapsıyorsa bu, sıçramayı önceden bilerek eleme yapmak, yani bakış sızıntısı olmaz mı?

02-029. Karantina bir pozisyon açıkken devreye girerse pozisyon hangi fiyattan, hangi tarihte kapanıyor ve bu işlem sayıma giriyor mu?

02-030. Karantinaya girenler rastgele değil (sıkıntılı, oynak, tedbirli hisseler); karantinanın kural lehine mi aleyhine mi yanlılık yarattığı ve K1/K2'ye aynı karantinanın uygulanıp uygulanmadığı yazılı mı?

02-031. Limit-aşımı kuralı yalnız limiti %0,5 aşan günleri yakalar; limit altında kalan eksik bir %5 bedelsiz ya da %4 temettü kaydı hangi kontrolle bulunur?

02-032. TASARIM 5.1 eşiği "günün limiti +%0,5" iken veri-kaynaklari 7.2 "günlük >|%25|" diyor; ±%10 döneminde %10,5 ile %25 arasındaki eksik olaylar hangi belgeye göre uyarı üretir?

02-033. Prosedür sayfa 36'ya göre bedelli ve bedelsiz günlerinde fiyat tescili sırasında marj serbest veya ayrı; 5.1'in "o günkü limit" kuralı olay günü için nasıl yeniden tanımlanıyor ve olay kaydı var diye "açıklanmış" sayılan bir günde sıçrama çarpanla uyuşmuyorsa yakalanıyor mu?

02-034. 5.1 karantina örneği olarak ECILC ve RYSAS'ı 12.03.2020'de veriyor; bu tarih ±%20 rejiminin son günü, yani sıçrama limit rejimi yüzünden mi olay yüzünden mi, ve hangi koşul onları karantinaya sokuyor?

02-035. 30.11.2015 öncesi ABCD döneminin marjı doğrulanmamış (veri-kaynaklari 8.4) iken 2015'in ilk on bir ayında karantina limiti hangi rakamla çalışıyor?

02-036. 2020-10 sonrası pazar bazlı marj (Yıldız %20, Ana %15, Alt %10) ile ±%10 ölçümü çelişiyor ve doğrulanmadı; karantina limiti ve olay günü sıçrama yargısı hangi varsayıma dayanıyor?

02-037. İşlem durdurma, tedbir veya eksik satır nedeniyle birkaç gün aralıklı iki kapanış arasındaki yasal getiri tek günlük limiti aşabilir; 5.1 bu çok günlük boşlukları olaysız sıçrama sayıp karantinaya sokar mı?

02-038. 5.1 tavan/taban kontrolünü ham fiyatla yapıyor; ex-date günü tavan ve taban önceki ham kapanıştan değil düzeltilmiş baz fiyattan hesaplandığına göre kilitli tavan/taban testi bu günde hangi referansla yapılıyor?

02-039. Kilitli tavan testi "düşük = yüksek = tavan" eşitliğine bakıyor; tavan fiyatı fiyat adımına yuvarlanmış baz fiyattan geliyorsa kayan nokta ve yuvarlama farkı, özellikle olay günlerinde, yanlış negatif üretmez mi?

02-040. 5.1 "hacim olağandışıysa kart üretilmez" diyor; bedelsiz sonrası lot hacmi ölçek olarak sıçradığında bu eşik olay sonrası haftalarca kartı bastırır mı, hangi hacim serisiyle (ham/`HGDG_HACIM`) ölçülüyor?

02-041. 5.3 girişi ertesi günün AOF'undan alıyor; AOF `HG_AOF` mu `HGDG_AOF` mi ve ex-date gününde bu ikisi farklı ölçekte olduğunda giriş fiyatı hangisi?

02-042. 5.3 "stop ve hedef giriş fiyatından ve sinyal günü ATR'sinden" hesaplanır; sinyal günü t'dir, t+1 bedelsiz ex-date ise giriş yeni ölçekte, ATR eski ölçekte kalır; stop nasıl hesaplanır?

02-043. Adım fonksiyonunun girdisi "pozisyon" (TASARIM 4); açık pozisyonun giriş, stop, hedef, ATR alanları olay gününde kim tarafından yeniden ölçekleniyor ve bu dönüşüm sınama ile canlıda aynı kodla mı yapılıyor?

02-044. Backtest'te pozisyonun girişi "o gün geçerli" ölçekte mi yoksa "bugünkü düzeltilmiş" ölçekte mi saklanıyor; çıkış başka bir ölçekteki seriden geliyorsa işlem getirisi nasıl hesaplanıyor?

02-045. Adet = risk / 2ATR düzeltilmiş ATR'den çıkıyor ve bedelsiz sonrası lot sayısı da değişiyor; "tek pozisyon en fazla sermayenin %10'u" ve lot yuvarlaması hangi ölçekte kontrol ediliyor?

02-046. 5.4 likidite sınırı "son 10 günün medyan TL tutarı" ham fiyat × HACIM ile hesaplanıyor; HACIM lot ise ve pencere bir bedelsiz olayını kesiyorsa lot ölçeği karışmaz mı, hangi hacim serisi (ham/düzeltilmiş) kullanılıyor?

02-047. Evrenin 60 günlük medyan TL tutarı (5.2) için aynı ölçek sorusu: HACIM zaten TL ise ham fiyatla çarpmak çifte sayım olur, lot ise `HG_HACIM` ile `HGDG_HACIM` karışırsa olay ayında yanlış elemeler olur; S2-14 çözülene kadar evren nasıl kurulur?

02-048. Evren her ay başı `PD`'ye göre sıralanıyor; bedelli sermaye artırımı `SERMAYE`'yi artırır ve `PD` fiyata göre gecikmeli güncellenebilir; bedelli dönemlerinde sıralama şişiyor mu ve bu alanların güncelleme günü doğrulandı mı?

02-049. ATR hesabındaki önceki kapanış terimi olay gününde düzeltilmemiş ham kapanışsa gerçek aralık sahte sıçrar; 5.1 "göstergeler düzeltilmiş" diyor ama ATR'nin üç bileşeninin (yüksek, düşük, önceki kapanış) aynı seriden geldiği nerede garanti ediliyor?

02-050. Nakit temettü ex-gününde ham fiyat temettü kadar düşer ve aracı kurumdaki stop emri ham fiyatta tetiklenir; stop kontrolü `HGDG` serisinde yapılırsa bu tetiklenme backtest'te görünmez; stop kontrolü hangi seriyle yapılıyor?

02-051. Yüksek temettü verimli bir hissede (%8 gibi) ham fiyat düşüşü "giriş − 2 ATR" stop mesafesinin önemli bölümünü tek günde yer; düzeltilmiş seri bunu gizlerse canlı kart ile backtest aynı kuralı mı uyguluyor?

02-052. AB=CD'de D hedefi ve A seviyesi stopu açık pozisyon sırasında bedelsiz, bedelli veya temettü olayıyla ölçek değiştirir; bu seviyeler yeniden ölçekleniyor mu ve hangi gün geçerli oluyor?

02-053. AB=CD pivotları (A, B, C) ve geometri koşulları (BC ≤ AB, C > A) bugünün `HGDG` serisinde hesaplanıyor; temettü düzeltmesi aralarındaki oranları değiştirdiği için bir kalıp bazı koşularda var, yeni bir temettüden sonra yok sayılabilir mi?

02-054. 5.5'teki "kapanış SMA250 altına inerse ertesi açılışta çık" kuralında kapanış ham, SMA düzeltilmiş seriden gelirse ex-date günü sahte çıkış doğar; karşılaştırmanın iki tarafı için hangi seri yazılı?

02-055. 5.3 boşluklu stop kuralı "gün yüksek de stopun altındaysa AOF'tan dolum" diyor; stop eski ölçekte kalırsa bedelsiz ex-gününde `HG_MAX` her zaman stopun altı olur ve sahte stop-AOF dolumu üretir; bu nasıl önleniyor?

02-056. BIST fiyat adımı fiyat aralığına göre değişir; bedelsiz sonrası düşük fiyatlı hissede 2 ATR stop, hedef ve AOF dolumu tick'e yuvarlanmıyor ve tick ATR'nin büyük kesri olabiliyor; modelde fiyat adımı var mı?

02-057. Bedelsiz payların hesaba geçmesi ex-date'ten sonra gecikmeli olur; ex-date günü veya hemen sonrasında çıkış yapan pozisyonun yeni paylarını satabildiği varsayımı simülatörde nasıl modelleniyor?

02-058. T+2 takasta ex-date'ten önceki son haklı günde alınan hisse hak sahibi olur; sinyal t, giriş t+1 AOF kuralı bu hak sahipliğini (ve temettü/bedelsiz payını) doğru günlerde mi atfediyor?

02-059. Düzeltilmiş seri bedelli dilüsyonu maliyetsiz yok sayar; gerçek yatırımcı hakkı kullanmak için nakit koymak veya hakkı satmak zorundadır, simülatör bedelli sırasındaki açık pozisyonda hangisini varsayıyor ve nakit gereksinimi modelde var mı?

02-060. Bedelli çarpanı teorik baz fiyat formülünden geliyor; gerçekleşen hak fiyatı (piyasada işlem gören) teorik değerden saparsa gerçek yatırımcı sonucu çarpanın varsaydığından ayrılır, bu fark ölçülüyor mu?

02-061. Yeni pay alma hakkı işlem döneminde (marj ±%50, prosedür sayfa 36) hisse sinyali veya açık kart hisse fiyatındaki hak etkisiyle karışabilir; bu dönemde sinyal üretimi veya Adım güncellemesi ayrı mı ele alınıyor?

02-062. TASARIM 6'daki kart 19:30'da üretilir, ertesi sabah hisse bedelsizle 1/10 fiyatta açılabilir; Levent'in elindeki giriş bölgesi, stop ve hedef eski ölçekte kalıyor, kart bu durumda hangi etiketi alır?

02-063. Olay gününde ham kapanış %-90 görünür; 6.5'te açık kartlar Adım ile güncellenirken seri henüz düzeltilmemişse kart "STOP" olarak yanlış kapanır; olay tablosu ve `HGDG` olay gününün akşamı güncellenmiş oluyor mu?

02-064. 6.1'deki 19:30 tazelik kontrolü yalnız son çubuk tarihine bakıyor; olay tablosunun veya `HGDG` düzeltmesinin o gün işlenmiş olduğu nasıl doğrulanıyor?

02-065. Kartta gösterilen giriş, stop ve hedef seviyeleri hangi ölçekte; `HGDG` geriye dönük yeniden ölçeklendiği için bugünkü ile aracı kurum fiyatı uyuşsa bile sonraki bir temettüden sonra aynı kartın seviyeleri değişir mi?

02-066. Sinyal geçmişi yeniden üretilirse (örneğin yeni bir temettü sonrası) bugün çalışan sinyal kuralı geçmiş günlerde farklı sinyal verebilir; sinyal günlüğü o gün yazılıp dondurulan bir kayıt mı yoksa her seferinde yeniden hesaplanan bir şey mi (repainting)?

02-067. TASARIM 6.4'teki kanıt satırı ("112 işlem, ... ± %1,1") yeni bir olay sonrası geçmiş yeniden ölçeklendiğinde değişir; kartın kanıt satırı hangi anlık görüntüye bağlı ve raporlarda tekrar üretilebilirlik nasıl sağlanıyor?

02-068. 5.8 kâğıt üstü canlı dönemde açılan işlemler olay anında ham fiyatla mı kaydediliyor, sonradan `HGDG` ile mi kapatılıyor; kayıtlı canlı sonuç sonraki temettü/bedelsiz ile geriye dönük değişebilir mi?

02-069. 5.12.6 canlı dönem etkisini "doğrulamadaki etkinin en az yarısı" ile kıyaslıyor; canlı işlem getirileri olay kayıtlarıyla yeniden ölçekleneceği için iki dönemin getiri tanımı aynı mı?

02-070. 5.8 kural kaydı kodun hash'ini alıyor; olay çarpan tablosu ve düzeltme sürümü hash'e giriyor mu, İş Yatırım tablosu veya `HGDG` değişince sonuç değişirse bu yeni deneme (5.11) sayılıyor mu?

02-071. Bedelsiz ve temettü ex-date'leri KAP/İş Yatırım'da önceden duyurulur; tablo ileri tarihli kayıtları içeriyorsa canlı sistem ve backtest bu bilgiyi simetrik biçimde mi kullanıyor, yoksa canlıda ex-date öncesi kart bastırılıyor mu?

02-072. Backtest 2018 sinyal gününde bugünkü eksiksiz olay tablosuyla düzeltilmiş seri kullanır; o gün bilinmeyen sonraki temettü ve bedelli düzeltmeleri, seviye bağımlı kurallarda (ATR TL, fiyat adımı, lot) bilgi sızdırır mı?

02-073. BIST'te bedelsiz duyurusu öncesi/sonrası fiyat yükselişi (bedelsiz rallisi) bilinen bir davranıştır; sinyaller ex-date çevresinde kümelenirse K1(b) "aynı hisse ±20 gün" bu etkiyi dışlıyor mu, yoksa kural şans yerine olay takvimini mi yakalıyor?

02-074. K1 rastgele günleri ex-date, olay öncesi ve olay sonrası günleri içeriyor mu; rastgele giriş gününün ex-date olması durumunda dolum mantığı (5.3) aynı mı?

02-075. Temettü sezonu (Mart–Haziran) mevsimselliği sinyalleri aynı aylarda toplarsa 5.9'daki "en az 60 farklı sinyal günü" ve 5.12.4'teki "yılların %60'ı" ölçütleri bağımsız örnek sayısını abartmaz mı?

02-076. Piyasa durumu etiketi XU100'e (temettüsüz fiyat endeksi) dayanıyor; K2 sepeti temettülü `HGDG`'den hesaplanıyor; K1(b)'deki "aynı piyasa durumu" ve etikete göre raporlama iki farklı getiri tanımını karıştırmıyor mu?

02-077. K2 "aynı temettü düzeltmesiyle" temettüyü ex-date'te yeniden yatırılmış sayar; gerçek bireysel yatırımcı temettüyü haftalar sonra nakit alır ve vergisi kesilir, bu fark K2 ile kural arasındaki fazla getiriyi hangi yönde etkiler?

02-078. K2 eşit ağırlıklı sepetin yeniden dengeleme sıklığı yazılı değil; bedelsiz/bedelli olaylarında sepetteki lot, ağırlık ve temettü yeniden yatırımı hangi kuralla işleniyor?

02-079. S4'teki yıllık çift seçimi (252 gün, p < 0,05) `HGDG` (temettülü) ile mi borsapy (temettüsüz) ile mi yapılıyor; iki bacağın temettü verimleri farklıysa (VAKBN–GARAN) eşbütünleşme p değeri seri seçimine duyarlı mı ve bu duyarlılık raporlanıyor mu?

02-080. Çift rotasyonunda geçiş günü bir bacakta ex-date varsa AOF ham ve düzeltilmiş seriler arasında karışırsa sahte getiri doğar; geçiş fiyatı hangi seriden alınıyor?

02-081. Çift payı "her an çiftin bir hissesindedir"; tutulan hisse nakit temettü öderse nakit hangi tarihte hesaba geçiyor, faiz kazanıyor mu, yoksa `HGDG` ile otomatik yeniden yatırılmış mı sayılıyor?

02-082. Çift bacaklarından birinde eksik kalan bir olay kaydı log farkı serisinde kalıcı bir basamak yaratır ve sahte eşbütünleşme veya sahte ΔZ sinyali üretir; çift bölmesinde karantina iki bacağı birlikte mi çıkarıyor?

02-083. 5.7 işlem seviyesi fazla getiri sepet getirisini kapanıştan kapanışa, kural işlemini AOF'tan AOF'ya ölçüyorsa; ex-date gününde ve çevresinde bu iki ölçüm farkı sistematik fazla getiri üretir mi?

02-084. Raporda kural getirisinin ne kadarı temettüden (toplam getiri) ne kadarı fiyattandır ayrı gösteriliyor mu; temettü katkısı yalnız yüksek temettülü hisselerde yoğunsa "Tansu'nun kuralı çalışıyor" yargısı yanıltıcı olmaz mı?

02-085. Tansu'nun yfinance çıktıları temettü düzeltmeli (`Adj Close`) mi ham mı; B-momentum notu `auto_adjust` varsayılanının yfinance sürümüne göre değiştiğini söylerken TASARIM 5.1 "düzeltilmiş" seçimini sadakat açısından nasıl gerekçelendiriyor?

02-086. veri-kaynaklari 2.2 Yahoo bedelsiz serisinin yanlış olduğunu gösteriyor; TASARIM 7.2 sadakat adımında Yahoo verisini kullanmak Tansu'nun hatalı sayılarını da yeniden üretmek demektir, eşleşme neyi kanıtlar, eşleşmeme neyi kanıtlar?

02-087. SMRTG'nin −%23,29 ve −%24,85 stop kayıpları ile +%50,72 hedefi gibi büyük hareketler Yahoo bedelsiz artefaktı olabilir; SMRTG ve ISKPL işlem tarihleri arasındaki şirket olayları sadakat kontrolünde taranıyor mu?

02-088. 5.3 Tansu'nun "T+1 açılış" kuralını Yahoo açılışıyla ayrıca üretiyor; Yahoo `Open` olay günlerinde yanlış ölçeklenmiş (CCOLA 01.08–12.08.2024), bu açılış verisi hangi günlerde güvenilir ve olay günleri çıkarılıyor mu?

02-089. Tansu'nun ekran çıktıları kendi tarihinde Yahoo'nun o günkü serisinden üretildi; bugünkü Yahoo çekimi sonraki bedelsiz ve düzeltmelerle geçmişi değiştirmiş olabilir, VAKBN–GARAN z-skoru ve KRDMD sıkışmasının yeniden üretiminde bu zaman kayması nasıl ele alınıyor?

02-090. KRDMD sıkışması (%0,64) EMA200 ve fiyat penceresine dayanıyor; o pencerede bedelsiz veya temettü olduysa Tansu'nun oranı ile bizim `HGDG` tabanlı oranımız farklı çıkar, sadakat kontrolünün toleransı bunu hesaba katıyor mu?

02-091. E-risk notu fiyat bazını (düzeltilmiş/ham) Tansu'nun söylemediği bir YORUM olarak işaretliyor; TASARIM 5.1 ise bunu kesin bir kural gibi yazıyor, Tansu'nun 70 hisselik lot örneği ham fiyatlıysa "2 ATR" boyutlandırması düzeltilmiş seriyle sadakatten sapmaz mı?

02-092. 5.3'te motor sınamaları listesinde (hedef, stop, boşluk, aynı gün, tavan, taban, bozulma) bedelsiz, bedelli ve temettü gününde açık pozisyon testi yok; bu eksik hangi sınamayla kapanıyor?

02-093. Düzeltme katmanının birim testleri veri-kaynaklari'ndaki 7 vakaya (AYGAZ, CCOLA, FENER, HEKTS ×2, TUKAS, EUREN) dayanıyor; ters bölünme, aynı güne çakışan kayıt, 1,0 çarpanlı kayıt ve eksik satır vakaları için beklenen çıktı nerede yazılı?

02-094. Karantinaya alınan hisse × gün sayısı, çıkarılan pencerelerin oranı ve karantinasız/karantinalı sonuç farkı raporda yazılıyor mu; karantina sonucu ne kadar değiştiriyor ölçülmeden "veri hatası ayrıştırıldı" iddiası nasıl savunulur?

02-095. Olay tablosundaki hataya sonuçların duyarlılığı hiç sınanmıyor; bilinen olaylardan birkaçı çarpanı bozulmuş ya da silinmiş olarak enjekte edilse kabul ölçütünün (5.12) sonucu değişir mi, bunu ölçen bir adım var mı?

02-096. 5.1 "fark varsa o gün listelenir" der ama kabul eşiği yok; kaç gün farkına kadar aile sınamaya girer, ve 5.12 kabul ölçütleri veri kalitesi kapısı içermiyor.

02-097. S2-14 HACIM birimini "fiyat × lot" karşılaştırmasıyla çözmeyi planlıyor; bu karşılaştırma bedelsiz olay günlerinde ve düzeltilmiş ile ham seriler arasında bozulur, test hangi günlerde ve hangi seriyle yapılacak?

02-098. Bedelli veya bedelsiz süreci sırasında hisse işlem durdurulur veya kilitli tabana girerse 5.3 "taban kilidinde çıkış ertesi güne kayar" kuralı olay günlerinde stopun yürümemesi sonucunu nasıl yansıtıyor?

02-099. Ham seride olay gününe denk gelen satır eksikse (işlem görmedi, tedbir, veri boşluğu) çarpan hangi güne uygulanıyor ve ilk mevcut satırdaki sıçrama karantinaya mı girer?

02-100. Bedelsiz sonrası düşük fiyat ve küçük tick bireysel işlem hacmini artırır, `PD` ve TL tutar sıralaması olay çevresinde yapay biçimde kayabilir; "aynı gün sinyal fazlasında en likit önce" (5.6) ve evren seçimi bu mikroyapı etkisine karşı korunuyor mu?
