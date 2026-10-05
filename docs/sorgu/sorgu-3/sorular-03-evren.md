# Sorular 03: Evren

03-001. TASARIM 5.2 evreni "piyasa değeri en büyük 100" diye kurar, oysa gerçek BIST100 fiili dolaşımdaki değere dayanır ve veride `HAO_PD` hazır durur (veri-kaynaklari 3.2); neden toplam `PD` seçildi ve kontrol payı büyük hisseler evrene nasıl yansır?
03-002. S2-19 "veride PD var" der ama yalnız alanın varlığı doğrulandı; İş Yatırım `PD` değerinin geçmiş günler için nokta-zamanlı olduğu (sonradan yeniden hesaplanmadığı) hangi gözlemle gösterildi?
03-003. `PD` = fiyat × `SERMAYE` ise, bedelsiz/bedelli günü `SERMAYE` güncellemesi fiyat düşüşüyle aynı gün gelmezse PD günlerce yanlış olur; ay başı sıralaması bu güne denk gelirse evren üyeliği ne olur?
03-004. Aynı şirketin birden fazla pay grubu (ayrı kodlar) PD sıralamasında iki kez sayılırsa 100 sınırı kimi dışarıda bırakır, ve bu durum K2 sepetinde aynı şirketi iki kez ağırlıklandırmaz mı?
03-005. İş Yatırım işlem sırası listesinde rüçhan hakları, BYF, varant ve imtiyazlı paylar (ISKUR.E gibi, veri-kaynaklari 5.9) pay gibi dönüyorsa, evrene girmemeleri hangi filtreyle sağlanır?
03-006. TASARIM 5.2 "o gün işlem gören" der; hacmi sıfır olan, tek fiyatla işlem gören veya işlem durdurulmuş gün bu tanımda "işlem gören" sayılır mı?
03-007. "60 günlük medyan TL işlem tutarı şartı" (5.2) için sayısal eşik hiçbir yerde yazılmıyor; eşiği kim, hangi veriye bakarak koyacak ve bu değer 5.10'daki parametre kaydına girecek mi?
03-008. Eşik nominal TL ise 2015 ile 2026 arasındaki enflasyon nedeniyle aynı sayı çok farklı bir likidite anlamına gelir; eşik sabit mi tutulacak, endekslenecek mi, ve hangisi evrenin boyutunu bozmaz?
03-009. HACIM'ın birimi (lot mu TL mi) hâlâ çözülmedi (5.1, 8) ve ham `HG_HACIM` bedelsiz sonrası lot sayısı olarak ölçeklenmiyorsa, medyan TL tutarı hesabı bu çözülmeden evren kurulabilir mi?
03-010. "Her ay başında" sıralama hangi günün kapanış verisiyle yapılır; ay başı günün kapanışı kullanılıp aynı günün sinyalleri yeni listeyle taranırsa look-ahead olmaz mı?
03-011. Veri 02.01.2015'te başladığı için 60 günlük medyan en erken Mart 2015'te hesaplanır; Ocak–Mart 2015 için evren nedir ve 5.8'in 2015–2017 doğrulama başlangıcı bunu nasıl karşılar?
03-012. "Ay başı" ilk işlem günü müdür; Bayram tatilleri ve yarım günler (Takvim modülü, TASARIM 4) ay başı tanımını kaydırırsa evren hangi tarihten geçerli olur?
03-013. Ay içinde evrene yeni giren bir hissede o gün zaten sağlanmış bir kural (örneğin süregelen EMA sıkışması) sinyal sayılır mı, yoksa evrene girişten sonra ilk taze sinyal mi beklenir?
03-014. Aylık yeniden kurmada evrenden çıkan bir hissede açık pozisyon zorla kapanır mı, açık kalır mı, ve çıkış fiyatı nedir; aynı kural K1 rastgele kuralda ve K2 sepetinde nasıl uygulanır?
03-015. PD sıralaması geçmiş fiyat getirisinin bir fonksiyonudur; son aylarda yükselen hisseler listeye girer, düşenler çıkar, bu seçim trend ve sıkışma ailelerini sistematik olarak lehine çevirmez mi?
03-016. 100. sıra civarında histerezis yok; sıra 99–101 arasında gidip gelen hisseler her ay girip çıkarsa sinyal sayısı, açık pozisyon çıkışları ve maliyet bundan nasıl etkilenir?
03-017. Ara evren gerçek BIST100'ün kurallarını (pazar şartı, tedbir dışlaması, halka açıklık) uygulamıyorsa, iki liste arasındaki örtüşme oranı hiçbir yerde ölçülmüyor; hangi örtüşme "yeterince yakın" sayılır?
03-018. "Ara evren hayatta kalan yanlılığını azaltır" iddiası (S2-19) hangi gözlemle çürütülebilir; gerçek üyelik yokken azalmanın doğrulanacağı bir kontrol (örneğin KAP verisinin bulunduğu bir dönemde karşılaştırma) planda var mı?
03-019. Tedbirli (brüt takas, tek fiyat, açığa satış yasağı) veya Yakın İzleme Pazarı'ndaki hisseler PD ile evrene girebilir; 8.4 "bilinen yanlılık olarak yazılır" der ama yönü ve büyüklüğü ölçmek için gerekli veri kaynağı gösterilmiyor.
03-020. Holding ve iştiraklerinin PD'si aynı değeri iki kez taşıdığı halde S2-22 bankaları, holdingleri ve GYO'ları evrene dahil eder; bu, eşit ağırlıklı K2 sepetini ve sektör içi çift seçimini nasıl etkiler?
03-021. Evren büyüklüğü sabit 100'dür ama listelenen hisse sayısı 2015'ten 2026'ya belirgin değişir; "en büyük 100" piyasanın zamanla farklı bir dilimini temsil ederse yıllar arası karşılaştırma (5.8 yıllık ileri yürüme) neyi ölçer?
03-022. Canlı günlük işleyişte (TASARIM 6) bugünün evreni hangi kaynaktan gelir, ara evren mi gerçek BIST100 mü; sınama ile canlı farklı evren kullanırsa A5'teki "ikisi ayrışamaz" ilkesi nasıl korunur?
03-023. Kapanmış sembollerin listesi "borsapy + KAP"tan gelecek (5.2) ama borsapy yalnız bugünkü listeyi verir (veri-kaynaklari 4) ve KAP sorgusu 2000 kayıt sınırına takılır; kapanmış sembol listesi hangi sorguyla ve hangi tamlıkla üretilecek?
03-024. "Bulunamayanlar raporda yazılır" (5.2) bir sayı verir ama yanlılığın büyüklüğünü vermez; bulunamayan kapanmış sembol oranı hangi eşiği aşarsa "mutlak getiriler üst sınırdır" ifadesi bile geçersiz olur?
03-025. İş Yatırım `HisseTekil` kapanmış sembol için yalnız ASYAB ile sınandı (S2 giriş); başka kaç kapanmış kodda ham, `HGDG` ve `PD` alanlarının eksiksiz döndüğü doğrulandı?
03-026. ASYAB'ın 25.07.2016'daki son işlem günü iflas, birleşme veya pay alım teklifi gibi hangi nedenle oldu ve son fiyat yatırımcının gerçek çıkış değerini temsil ediyor mu?
03-027. Kapanışın nedenine göre (tasfiye, birleşme, gönüllü çıkış, pay alım teklifi) hissedarın eline geçen değer farklıdır; tasarımda bir pozisyonun delist anındaki terminal getirisini belirleyen tek bir kural var mı?
03-028. İşlem durdurulmuş hissede açık pozisyon varsa, taban kilidi kuralı "ertesi güne kayar" der (5.3); durdurma aylarca sürerse pozisyon, sermaye eğrisi ve boşta nakit nasıl muhasebeleştirilir?
03-029. Birleşme olayları İş Yatırım'da hangi `SHT_KODU` ile geliyor bilinmiyor (veri-kaynaklari 8.3); düzeltme çarpanı yoksa birleşme günü sahte sıçrama olarak karantinaya girmez mi?
03-030. Karantina (5.1) açıklanamayan en uç hareketleri o hissenin penceresinden çıkarır; delist öncesi çöküşler çoğunlukla bu sınıfa girerse karantina, kayıpları atıp kazançları bırakarak hayatta kalan yanlılığını yeniden üretmez mi?
03-031. Karantinaya giren bir hissede açık pozisyon varsa ne olur, pozisyon "sınamadan çıkar" mı, hangi fiyattan kapanır, ve bu karar kural lehine mi aleyhine mi sapar?
03-032. Sembol değişikliğinde İş Yatırım eski kodun geçmişini yeni kodun altında mı verir, yoksa seri ikiye bölünür mü; bölünürse aynı şirket 60 günlük medyan şartında sıfırlanıp evrenden düşer mi?
03-033. Bir kod sonradan başka bir şirkete verilirse iki şirketin serisi tek seri gibi görünür; fark limit içinde kalırsa karantina bunu yakalamaz, bu durum nasıl saptanacak?
03-034. Kod değiştiren şirket hem "kapanmış sembol" listesine (eski kod) hem bugünkü listeye (yeni kod) girerse aynı şirket evrende iki kez ya da hiç bulunmaz mı?
03-035. Şirket bölünmesi (spin-off) olayında `SHHE_FIYAT_AYAR_OR` çarpanı bölünme değerini yansıtıyor mu (veri-kaynaklari 8.3 bilinmiyor); yansıtmıyorsa bölünme günü ham fiyat düşüşü hayatta kalan yanlılığından ayrılabilir mi?
03-036. `GetSermayeArttirimlari` kapanmış kodlar için de kayıt dönüyor mu; dönmüyorsa bu hisselerin düzeltme katsayısı (B1) nereden gelecek ve `HGDG` ile çapraz kontrol nasıl yapılacak?
03-037. 5.1'deki "bütün hisse × gün" ikinci kaynak karşılaştırması borsapy ile yapılır ve borsapy güncel hisseleri döndürür; kapanmış hisseler ikinci kaynak olmadan sınanırsa veri kalitesi hayatta kalanlar lehine eşitsiz olmaz mı?
03-038. İş Yatırım uzun süre önce kapanmış kodların geçmişini sildiyse veya hiç tutmuyorsa, ilk anlık görüntüden önce kaybolan delistlerin yıl dağılımı (özellikle 2015–2018) ölçülebilir mi?
03-039. Delist öncesinde likidite çöker; 60 günlük medyan TL şartı (5.2) bu hisseyi delistten aylar önce evrenden çıkarırsa, evren düşüş sürecini zaten dışarıda bırakıp yanlılığı kısmen geri getirmez mi?
03-040. Aynı şekilde PD'nin düşmesiyle 100. sıranın altına inen bir hisse evrenden çıkar; evren iflasa giden yolu görmeden ayrıldığı için ara evren hangi delist kayıplarını gerçekten içeriyor?
03-041. İş Yatırım `HisseTekil` hisse kodu ister; "bütün semboller" listesi bugünkü ve KAP kaynaklarından bir araya getirilemezse, kod keşfi (brute-force deneme dahil) tasarımın hangi adımında yer alıyor ve hız sınırı bilinmezken (8.1) nasıl yapılacak?
03-042. 8.3 KAP endeks duyurularının 2015–2016'yı kapsayıp kapsamadığını bilmiyor (veri-kaynaklari 4: bulunamadı); kapsamazsa 5.8 doğrulaması 2015–2017'de başladığı için ilk yılların evreni hangi yöntemle kurulur?
03-043. KAP bildirimi yalnız değişenleri listeler; zincir hangi başlangıç listesinden kurulacak, bir çeyrek kaçarsa sonraki bütün çeyrekler bozulur (veri-kaynaklari 4), hatayı yakalayacak bağımsız bir kontrol noktası var mı?
03-044. Dönemsel duyurular çeyrek başı değişikliklerdir; çeyrek içinde delist, birleşme veya SPK kararıyla boşalan yerin kime geçtiği bu duyurulardan çıkmıyorsa liste ara dönemlerde 100 hissede kalır mı?
03-045. Duyuru yürürlükten en az 10 gün önce yapılır (veri-kaynaklari 4); yeniden kurulan üyelik duyuru tarihinden başlatılırsa endekse girecek hissenin fiyat hareketi look-ahead olur, yürürlük tarihinden başlatılırsa hangi tarih kullanılacak?
03-046. PDF eklerinin makinece okunabilirliği bilinmiyor (veri-kaynaklari 8.5); ~40 duyurunun elle ayrıştırılması gerekirse bu işin hata oranı ve ikinci okuma kontrolü nasıl tasarlandı?
03-047. Adım 8'de gerçek BIST100 hazır olunca sonuçlar değişirse hangi evren bağlayıcıdır; kural kaydından sonra evrenin değişmesi 5.8'e göre "yeni deneme" sayılıyorsa 2015–2026 yanmış veri üzerinde ikinci bir gözlem yapılmış olmaz mı?
03-048. KAP listesi çeyreklik, ara evren aylıktır; iki evren zamanda hizalı olmadığı için fark yalnız yanlılıktan değil kurma sıklığından da gelir, bu iki etki nasıl ayrılacak?
03-049. Sektör "bugünkü sınıflamadan (borsapy)" alınır (5.2, S2-21); borsapy'nin sektör alanı hangi kaynağa dayanıyor (BIST sektör endeksi, KAP, İş Yatırım) ve sınıflama ne kadar ayrıntılı?
03-050. Kapanmış hissenin bugünkü sektörü yoktur; çift evreninde bu hisseler nasıl sınıflanır, sınıfsız kalırsa çift bölmesi yine yalnız hayatta kalanlardan mı kurulur?
03-051. TASARIM 5.6 çiftleri "aynı sektördeki BIST100 hisseleri" arasından yıl başında seçer; bu BIST100 ara evren midir, ve ara evren aylık değişirken yıl başındaki üyelik hangi ayın listesidir?
03-052. Çift seçildikten sonra hisselerden biri aylık evrenden veya likidite şartından düşerse çift yıl sonuna kadar sürer mi, yoksa aylık evren kuralı çifti de bozar mı?
03-053. Eşbütünleşme sınaması "önceki 252 gün" ister; veri 02.01.2015'te başladığı için 2015 yıl başı seçimi yapılamaz, ilk çift yılı 2016 ise 5.8'in "2015–2017 ile başlar" ifadesiyle çelişmez mi?
03-054. Bir sektörde 2–3 hisse, bir sektörde 15+ hisse varsa aday çift sayısı çok eşitsizdir ve "p'ye göre en iyi 5" büyük sektörlerde daha çok çiftten minimum p seçmek anlamına gelir; bu seçim yanlılığı hangi kontrolle ölçülür?
03-055. Tansu'nun AGROT–GARAN çifti (5.6) tasarımın kendi "aynı sektör" şartını sağlıyor mu; sağlamıyorsa "Tansu'nun çifti" ile bizim seçim kuralımız aynı yöntemin iki örneği sayılabilir mi?
03-056. Sektör sınıflamasında 2015'ten bu yana değişen hisse sayısı ölçülmeden "bilinen küçük yanlılık" denmesi (5.2) neye dayanıyor?
03-057. Bugünkü sektör bilgisi, sonradan iştirak ilişkisi kuran veya faaliyet alanı değişen şirketleri geçmişte de aynı sektörde göstererek çift evrenini geleceğe bakarak şekillendirmez mi?
03-058. KURALLAR D'deki Tansu sektör rotasyonu "sektör evreni/sınıflandırması belirsiz" der; borsapy sınıflaması Tansu'nun sektör adlarıyla (Petrol, Demir Çelik) eşleşiyor mu, eşleşmiyorsa hangisi esas?
03-059. Bir hissenin en iyi p'li çiftte tutulup diğer çiftlerden elenmesi (S2-27) sonrasında elenen çiftin ortağına yedek çift aranır mı; 5'ten az çift çıkarsa boş pay nakitte mi kalır ve bu nakit kural getirisine katkı sayılır mı?
03-060. Her çift payı "her an çiftin bir hissesindedir" (5.6); o hisse delist olur veya işlem durdurulursa payın akıbeti ne olur ve çift yıl sonuna kadar nasıl devam eder?
03-061. Beş çiftin tamamı aynı sektörden (örneğin bankalar) çıkarsa "bütün çift bölmesi" tek bir sektör bahsine dönüşür; sektör yoğunlaşması için bir sınır var mı?
03-062. 5.2 evren filtresi 60 günlük medyan, 5.4 pozisyon filtresi 10 günlük medyan kullanır; iki farklı pencere neden ve 10 günlük medyan evren üyesi bir hissede sık sık %2 tavanını sıfıra yaklaştırırsa sinyal sayısı nasıl etkilenir?
03-063. 1.000.000 TL sermaye ve %2 likidite tavanı sabit nominal TL'dir; 2015'te büyük, 2026'da küçük bir pozisyon anlamına gelir, zamana yayılan sonuçlar bu ölçek kaymasıyla nasıl karşılaştırılır?
03-064. "Aynı gün sinyal sayısı boş yeri aşarsa en likit önce" (5.6, M12) en likidin hangi pencereyle ölçüldüğünü ve sinyal günü hacminin dahil olup olmadığını söylemiyor; dahilse look-ahead değil mi?
03-065. K2 sepeti aylık mı, günlük mü yeniden dengelenir; eşit ağırlıkta her yeniden dengeleme maliyetsiz mi varsayılır ve bu maliyetsizlik kural–sepet farkını kuralın aleyhine nasıl çarpıtır?
03-066. İşlem seviyesi fazla getirisi "aynı tutma süresinde aynı evrenin sepeti" (5.7) olduğundan, sepet üyeliği giriş gününe mi çıkış gününe mi göre alınır ve tutma süresi içinde delist olan sepet üyesinin getirisi nasıl hesaplanır?
03-067. K1(b) "aynı hisse, ±20 gün" için seçilecek gün hissenin evrende olmadığı bir aya düşerse veya hisse o sırada delist olmuşsa o rastgele gün nasıl ele alınır?
03-068. Evren 60 gün geçmiş ister ama SMA250 çıkışı ve EMA200 oranı 250+ gün ister; yeni halka arz olmuş, evrene girmiş ve 250 gün geçmişi olmayan hissede sinyal ve çıkış nasıl işler?
03-069. Halka arzlar tavan serileriyle PD'yi hızla şişirip 60 gün sonra top-100'e girebilir; bu hisseler kilitli tavan girişi yasağı (5.3) nedeniyle işlem dışı kalır, evrende yer alıp sinyal üretmeden sayıya katılmaları sepeti nasıl değiştirir?
03-070. Eşit ağırlıklı K2 sepeti, kural sinyallerinin seçtiği büyük/likit hisselere göre küçük ve düşük fiyatlı hisselere daha fazla ağırlık verir; boyut tilt'i fazla getiriyi evren etkisinden ayıramaz mı?
03-071. Çeyrek sonu endeks yeniden dengeleme günlerinde kapanış hacmi ve AOF bozulur; ertesi gün AOF'tan giriş (5.3) bu günlere denk gelirse dolum fiyatı ve 10 günlük medyan TL tutarı nasıl etkilenir?
03-072. Evrende olup likidite %2 şartı yüzünden hiç işlem yapılamayan hisseler K2 sepetinde duruyorsa sepet, kuralın fiilen işlem yapabildiği evrenden daha geniş ve farklı olmaz mı?
03-073. 5.2 "Borsa İstanbul'un 2015 endeks değişikliği duyurularından o günkü BIST30 elle çıkarılır" der; veri-kaynaklari 4 ise 2015-09 ve 2015-12 için KAP'ta bu başlıklı bildirimi bulamadı, bu ölçüm hangi kaynakla yapılacak ve yapılamazsa ne olacak?
03-074. 2015'te dört çeyreklik liste vardır; "o günkü BIST30" hangisidir ve bu sabit liste yalnız 2015 boyunca mı yoksa 2015–2026 boyunca mı kullanılacak?
03-075. 2015 BIST30'unun büyük çoğunluğu bugün hâlâ listelidir; ölçüm yanlılığı küçük gösterip asıl yanlılığın yaşandığı 50.–100. sıradaki orta/küçük hisseler hakkında bilgi vermeyebilir, bu açık nasıl kapatılacak?
03-076. 30 hisseyle 5.9'un "en az 100 işlem ve 60 sinyal günü" şartı ve sektör içi çift bölmesi sağlanabilir mi; sağlanamazsa BIST30 sonucu istatistiksel olarak yanlılığı ölçmeye yeter mi?
03-077. BIST30-2015 ile ara evren arasındaki fark evren büyüklüğünden (30'a karşı 100) mi, kurma yönteminden mi, yanlılıktan mı kaynaklanıyor; bu üçünü ayıran bir kontrol var mı?
03-078. Yanlılık tek bir kesitte (2015) ölçülür; liste yaşlandıkça yanlılık büyür, bu tek ölçüm 2026'ya uzanan 100'lük bir evrenin yanlılığına nasıl genellenir?
03-079. Ölçüm "büyük" çıkarsa ne değişir: 5.12 kabul ölçütlerinde bu ölçüme bağlı bir eşik veya karar yok, ölçüm yalnız bilgi olarak mı kalıyor?
03-080. BIST30 listesi elle çıkarılır; elle yapılan tek kişilik bir çıkarımı doğrulayan ikinci bir kaynak veya kontrol var mı?
03-081. 2015 BIST30 sabit listesindeki şirketlerin bir kısmı sonradan kod değiştirdi veya birleşti; bu hisselerin 2026'ya kadar izlenmesi, ölçümün ölçmeye çalıştığı sembol/delist sorununu önce çözmeyi gerektirmez mi?
03-082. Sabit BIST30 listesinde aylık yeniden kurma yoktur, ara evrende vardır; fark yalnız hayatta kalan yanlılığı değil kompozisyon ve devir farkını da içerir, bunlar nasıl ayrışır?
03-083. "Mutlak getiriler üst sınırdır" (5.2) hükmü yalnız yanlılığın yönünün hep pozitif olduğunu varsayar; delist kayıplarının, çıkarılan hisselerin ve ters yönlü etkilerin işaretinin pozitif olduğu nasıl kanıtlandı?
03-084. Stop ve çıkış kuralı olan strateji düşen hissede erken çıkar, K2 sepeti tutar; delist ve çöküş kayıpları ikisini farklı etkilediği için yanlılık göreli farkta da kalmaz mı, "yalnız göreli yorum" neyi gerçekten korur?
03-085. Hayatta kalan hisseler tanım gereği yükselen eğilim gösterdiğinden kırılım ve trend kuralları bu seçimden rastgele kuraldan daha fazla yararlanır; yanlılığın kural ve K1 için eşit olduğu varsayımı sinyale koşullu olduğu için bozulmaz mı?
03-086. 5.12 son satırdaki portföy kuralı (en büyük düşüş %25, düşüşte kalma 12 ay) mutlak sermaye eğrisine uygulanır; mutlak getiri "karar için kullanılmaz" denirken bu kural hayatta kalan yanlılıklı eğrinin üzerinde nasıl karar verir?
03-087. 5.12.6 kâğıt üstü canlı fazla getirisinin doğrulama etkisinin en az yarısı olmasını ister; doğrulama evreni yanlılıklı, canlı evreni ise farklı olduğundan iki etki aynı ölçekte karşılaştırılabilir mi?
03-088. Raporda ve kartın kanıt satırında (6.4) mutlak getiri gösterilmeye devam edecek mi; edilecekse "üst sınır" uyarısı kartta nerede ve nasıl yer alır?
03-089. 5.11 deneme günlüğü alanları (tarih, aile, çıkış, parametre, anlık görüntü, kod hash) evren tanımını içermiyor; PD eşiği, 60 gün, 100 veya BIST30/KAP evreni farklı denemeler Holm düzeltmesine sayılıyor mu?
03-090. 5.8 kural kaydındaki hash evren kodunu ve eşiklerini de kapsıyor mu; evren parametresi değişirse bu "yeni deneme" ve yeni ayrılmış dönem demek midir?
03-091. Sadakat kontrolündeki Tansu örnekleri (SMRTG, ISKPL, KRPLS, MARKA, KRDMD, CIMSA, OYAKC) ilgili tarihlerde PD ile ara evrenin ilk 100'ünde mi; değilse sadakat ölçümü ile gerçek sınama farklı evrenlerde yapılmış olmaz mı?
03-092. KURALLAR B satır 279 Tansu'nun momentum evrenini "500+ BIST hissesi (2015'ten)" gösterir, BRYAT stratejisi "yüksek hacimli BIST30/100" der; tasarım 100'e daraltırken Tansu'nun hangi sınamasını temsil ettiğini iddia ediyor?
03-093. KURALLAR E "likit hisse" tanımını açık bırakır (YORUM); tasarım bunu "PD büyüklüğü + işlem tutarı" olarak somutlaştırdı, ama PD büyüklüğü işlem derinliğiyle aynı şey değildir; ekranda evrenin Tansu'dan değil bizden geldiği nerede belirtilecek?
03-094. P5 her ailenin "Tansu'dan esinlenen bizim yorumumuz" olduğunu söyler; evren seçimi de bizim yorumumuzsa rapor başlığında hangi evrenle koşulduğu ve bu seçimin YORUM etiketi ne olacak?
03-095. Brüt takas ve tek fiyat günlerinde AOF tek fiyat veya anlamsızdır (5.3 AOF dolumu); bu günler veri kaynaklarında ayırt edilemiyorsa (8.4) dolum modeli ve evren filtresi bu hisseleri nasıl ele alır?
03-096. İşlem durdurulan veya hacmi sıfır olan günlerde İş Yatırım satır döndürüyor mu; döndürüyorsa önceki kapanışı taşıyan bu satırlar medyan hacim, ATR ve eşbütünleşme penceresine sahte gün olarak girmez mi?
03-097. S2-51 Levent'in fiili dolaşım < %30 taramasını "ikinci dalga"ya erteler; fiili dolaşım evren kurmada yoksa BIST100'ün temel ölçütü ilk sürümde hiç temsil edilmiyor, bu ertelemenin evren yanlılığına etkisi tartıldı mı?
03-098. Adım 3'te kural kaydı yapılır ve adım 7'de üç aile koşulur, ama adım 8'de gerçek BIST100 evreni paralel iş olarak sonra gelir; kayıtlı kuralın evreni sonradan değişecekse 5.8 "sonraki her değişiklik yeni denemedir" ilkesiyle nasıl uyuşur?
03-099. Borsa İstanbul DataStore resmi üyelik arşivi olabilir ama kapsam ve ücret doğrulanmadı (veri-kaynaklari 4); KAP yolu ve bedava yol çökerse "ara evren geçicidir" ifadesinin bitiş koşulu nedir ve ara evrenle ne kadar süre karar verilir?
03-100. S2-19 ara evrenin kapanmış hisseleri "içerebileceğini" söyler, S2-20 ise liste bulunamazsa kalan yanlılığın yalnız raporda yazılacağını söyler; hiç kapanmış sembol bulunamazsa bile evren hâlâ "yanlılığı azaltan" evren diye mi adlandırılır?
