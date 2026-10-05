# Sorular 09: İstatistik ve kabul

**09-001.** TASARIM 5.7 K1 "kuralın kendi ön şartlarını sağlayan günler" diyor; AB=CD ve EMA sıkışması için bu ön şartlar nerede ve hangi tanımla önceden yazılmış, çünkü ön şart genişliği null dağılımın kendisini belirliyor?

**09-002.** Ön şart gevşek seçilirse K1 kolay geçilir, sıkı seçilirse zor geçilir; ön şart tanımı bir "araştırmacı serbestlik derecesi" olarak deneme günlüğüne (5.11) giriyor mu?

**09-003.** K1 türü (a) "aynı gün, başka hisse" piyasa genelinde kümelenen sinyal günlerinde (ör. endeks dibi) rastgele hisseyi aynı piyasa şokuna maruz bırakır; peki kuralın aynı gün birden çok hissede sinyal vermesi permütasyonda hisse sayısı olarak nasıl korunuyor?

**09-004.** K1 türü (b) "aynı hisse, ±20 gün içinde başka gün" seçilen rastgele günün getirisi sinyal gününün getirisiyle örtüşen pencereler paylaşır; bu bağımlılık p değerini şişirmiyor mu?

**09-005.** K1'in (a) ve (b) türleri ayrı p değeri üretirse 5.12.1 hangisini kullanıyor, biri geçip diğeri geçmezse karar ne oluyor?

**09-006.** "Sayılar hisse başına eşleştirilir" (5.7) türü (a)'da rastgele sinyal başka hisseye atandığında hisse başına sayı korunamaz; bu cümle yalnız türü (b) için mi geçerli?

**09-007.** EMA sıkışması gibi dar ön şartlı bir ailede ön şartı sağlayan gün havuzu gerçek sinyal sayısına yakınsa, permütasyon dağılımı dejenere olmaz mı ve bu durumda p değeri anlamlı kalır mı?

**09-008.** 1.000 permütasyonda ulaşılabilir en küçük p değeri 1/1001 ≈ 0,001; Holm düzeltmesinde deneme sayısı 50'yi aşınca eşik 0,001'in altına iner, bu durumda hiçbir aile matematiksel olarak geçemez mi?

**09-009.** Geliştirmede 200 tekrarla üretilen p değerleri (çözünürlük 1/201) deneme günlüğüne yazılıyor mu ve Holm sıralamasına, 1.000 tekrarlı son rapor p değerleriyle birlikte mi giriyor?

**09-010.** Rastgele kurala "pozisyon sınırı ve sıra kuralı" uygulanır (5.7); "en likit önce" sırası rastgele sinyal sayısı boş yeri aştığında seçimi likit hisselere kaydırır ve bu rastgele kuralın getirisini kuraldan farklı yönde etkilemez mi?

**09-011.** "Açık pozisyon varken gelen sinyal sayıma girmez" (5.3) kuralı rastgele kurala uygulanınca eşleştirilen sayı ham sinyal sayısı mı yoksa kabul edilmiş işlem sayısı mı; ikisi farklı null üretir.

**09-012.** Rastgele işlemlerde çıkış hangi kuralla yapılıyor: 2 ATR stop ve SMA250 çıkışı mı, kuralın gerçekleşen tutma süresi mi? Bu iki seçim farklı bir K1 null'ı ve farklı p değeri üretir.

**09-013.** AB=CD için stop A seviyesi ve hedef D = C + r(B−A) (5.5); rastgele bir günde A, B, C pivotları yoktur, bu durumda K1 rastgele işleminin stop ve hedefi nasıl üretiliyor?

**09-014.** Çift bölmesi K1'i "aynı çiftlerde aynı sayıda geçiş, rastgele günlerde" (5.7); geçiş sayısı sonuca koşullu bir nicelik olduğundan rastgele geçişler yön (Y'ye mi X'e mi) ve zamanlama bakımından hangi dağılımdan çekiliyor?

**09-015.** Çift bölmesinde yıllık çift seçimi (önceki 252 gün, p < 0,05) K1 null'ının parçası mı; değilse seçilmiş çiftlerin seçim sonrası ortalamaya dönüşü rastgele geçişte de görüleceği için K1 çift seçiminin değerini ölçebilir mi?

**09-016.** K1 p değeri hangi istatistik üzerinden hesaplanıyor: ortalama fazla getiri, medyan, Sharpe? 5.9 medyanı ayrıca gösteriyor ve 5.12.1 yalnız "fazla getiri pozitif" diyor.

**09-017.** K1 p değeri tek yönlü mü çift yönlü mü; tasarım "pozitif ve p < 0,05" diyor, bu tek yönlü α = 0,05 mi, yoksa Holm sonrası çift yönlü mü?

**09-018.** İşlem seviyesi fazla getiri "aynı tutma süresinde sepet getirisi" ile tanımlı (5.7); rastgele kuralın tutma süresi kendi çıkış kuralından mı geliyor, yoksa kuralın tutma süresi dağılımından mı örnekleniyor?

**09-019.** K2 "eşit ağırlıklı sepet" için yeniden dengeleme sıklığı yazılı değil; günlük dengeleme düşük likiditeli hisselerde sıçrama (bid-ask bounce) primi üretir, bu K2'yi yapay yükseltmez mi?

**09-020.** K2 sepeti masraf öder mi; kural %0,3 öderken sepet sıfır masrafla yarışırsa ya da sepet de ay başı evren değişimi için öderse fazla getirinin işareti değişir mi?

**09-021.** Kuralın ortalama maruziyeti %30 gibi düşükse (kalan nakit faiz kazanıyor) K2'ye göre günlük fazla getiri piyasa yükselirken sistematik negatif, düşerken pozitif olur; 5.12.2 beta/maruziyet düzeltmesi yapıyor mu?

**09-022.** Faizin yıllık %40–50 olduğu dönemlerde nakit faizi fazla getiriyi tek başına pozitif yapabilir; 5.12.2 "nakit faiz dahil" fazla getiriyi bu mekanik katkıdan nasıl ayıracak?

**09-023.** K2 sepeti her ay başı piyasa değerine göre kurulan top-100 evrenin eşit ağırlıklı getirisi; büyük PD seçimi ve eşit ağırlık küçük/orta hisse primi taşır, bu "evrenin kendi yanlılığı" K2'ye göre fazla getiriyi ölçmeye ne yapar?

**09-024.** Çift bölmesi için K2 "aynı çiftlerin 50/50 tutulması"; çiftler yıl başında p < 0,05 ile seçildiğinden 50/50 tutma in-sample seçilmiş bağı taşır, K2 hangi bakımdan "aynı evrenin basit sepeti" sayılıyor?

**09-025.** Parametreler sabit olduğundan "genişleyen pencereli ileri yürüme" (5.8) hiçbir şey eğitmez; bunun yıl yıl bölmeden farkı nedir ve neden "ileri yürüme" adı kullanılıyor?

**09-026.** 5.8 "2015–2017 ile başlar, her yıl bir sonraki yıl sınanır"; böylece 2018–2026 yaklaşık 9 test yılı kalıyor ve 2015–2017 hiç test edilmiyor, bu 5.12.4'teki "yılların en az %60'ı" için 9 yılın 6'sı demek değil mi, ve bu ölçüt ne kadar ayırt edici?

**09-027.** 2026 yılı tamamlanmamış bir yıl; yıl pozitifliği ölçütünde (5.12.4) kısmi yıl sayılıyor mu, sayılıyorsa hangi gün sayısından itibaren?

**09-028.** SMA250 ve 252 günlük eşbütünleşme penceresi için ısınma süresi gerekir; 2015 başlangıçlı veriyle ilk geçerli sinyal ve ilk çift seçimi hangi tarihte olur ve "2015–2017 ile başlar" ifadesi bununla çelişmez mi?

**09-029.** Kriter 1 (birleşik ileri yürüme fazla getirisi) ile kriter 4 (yılların %60'ı pozitif) aynı yıllık serilerden türer; bu iki kriter ne kadar bağımsız ve birlikte geçme olasılığı bağımsızlık varsayımıyla mı hesaplandı?

**09-030.** AB=CD ve EMA sıkışması yıllık birkaç işlem üretiyorsa yıl bazlı fazla getirinin işareti neredeyse yazı-tura olur; yıl pozitifliği %60 ölçütünün gürültüdeki geçme olasılığı hesaplandı mı?

**09-031.** Fiyat limiti 13.03.2020'de ±%20'den ±%10'a, pay bazında devre kesici 17.07.2017'de değişti (veri-kaynakları 5); yıl bölmeleri bu rejim kırılmalarını bir yılın içine sokuyor, 2020 yılı için sonuç iki rejimin karışımı olmuyor mu?

**09-032.** Sağlamlık ızgarası (5.10) hücreleri 2015–2026'nın tamamında mı yoksa yıl yıl mı koşuluyor; tamamında koşuluyorsa 2023 sonrası yanmış dönem ızgarayı da kirletmiyor mu?

**09-033.** Sadakat kontrolü "getiriye bakılmaz" (KURALLAR §4) ama kontrol Tansu'nun 2025–2026 görsellerindeki rakamlarla yapılıyor; tasarımcı aynı dönemin sonuçlarını (VAKBN–GARAN +%52,9 gibi) görmüş durumda, 5.8'deki "yandı" bildirimi bu dönemi kapsıyor mu?

**09-034.** İleri yürüme yıllarının 2025–2026'sı Tansu'nun örnek dönemleriyle çakışıyor; bu yıllar doğrulamada ayrı mı işaretleniyor yoksa kriter 1 ve 4'te diğer yıllarla eşit ağırlıkla mı sayılıyor?

**09-035.** 5.9 "20 günlük bloklar" seçimini hangi veri gerekçelendiriyor; çift bölmesinde ortalama tutma süresi 66 gün gibi (D dosyası, AGROT–GARAN) olduğundan 20 günlük blok bağımlılık süresinden kısa kalmıyor mu?

**09-036.** Blok bootstrap sabit uzunluklu mu (moving block) yoksa durağan (stationary) mı; blok sınırında açık pozisyonun bağımlılığı koptuğu için fazla getiri serisinin otokorelasyonu nasıl korunuyor?

**09-037.** Güven aralığı bootstrap'tan, p değeri K1 permütasyonundan geliyor; 5.12'nin altı kriterinden hangisi bootstrap aralığına bağlı, iki yöntem çelişirse hangisi geçerli?

**09-038.** Güven düzeyi (%90, %95) ve aralık türü (yüzdelik, BCa) 5.9'da yazılı değil; kriterlerde alt sınırın sıfırın üstünde olması mı aranıyor yoksa yalnız nokta tahmininin işareti mi?

**09-039.** Günlük portföy fazla getirisi serisinin çoğu gününde pozisyon yok ve fark yalnız nakit faizi ile sepet getirisinden oluşuyor; bu çok sıfırlı/kuyruklu seride 20 günlük blok bootstrap güvenilir bir aralık verir mi?

**09-040.** BIST'te tavan/taban serileri ve 2018, 2021 TL krizleri günlük fazla getiride değişken varyans ve ağır kuyruk yaratır; blok bootstrap durağanlık varsayar, bu varsayım hangi testle denetleniyor?

**09-041.** TASARIM 6.4'teki örnek kart "−%0,2 ± %1,1" yazıyor; "±" standart hata mı, %95 aralık yarı genişliği mi, birim işlem başına mı yoksa yıllık portföy mü, ve bu rakamı hangi yöntem üretiyor?

**09-042.** Fazla getirinin kuyruğu ağırsa ortalama yerine medyan gösterilir (5.9); kabul ölçütü ortalamaya mı medyana mı bakıyor, ikisi ters işaretliyse ne olur?

**09-043.** "En az 100 işlem ve 60 farklı sinyal günü" eşikleri hangi güç hesabından çıktı; 100 işlemde işlem başına fazla getiri SD'si %8 ise saptanabilir en küçük etki yaklaşık %1,6 çıkar, bu masraf varsayımının (%0,6 gidiş-dönüş) üstünde mi altında mı?

**09-044.** "Ölçülen dağılımla saptanabilecek en küçük etki hesaplanır ve raporda yazılır" (5.9) ama 5.12.5 yalnızca sayı eşiğini arıyor; MDE, Tansu'nun iddia ettiği etkiden büyük çıkarsa aile "reddedildi" mi yoksa "karar verilemez" mi sayılıyor?

**09-045.** MDE gözlenen varyanstan hesaplanıyor; aynı veriden tahmin edilen varyansla yapılan "post-hoc güç" analizi bilinen biçimde bilgilendirici değildir, bu hesap önceden varsayılan bir varyansla mı yapılıyor?

**09-046.** 100 işlemin 60 sinyal gününden gelmesi aynı gün birden çok işlem olduğu anlamına gelir; etkin bağımsız örneklem 100 değil 60'a yakın olduğundan MDE hangi sayıya göre hesaplanıyor?

**09-047.** Çift bölmesinde "işlem sayısı yerine günlük fazla getiri serisi" (5.8) kullanılıyor ama 5.9'daki "100 işlem ve 60 sinyal günü" şartı çift bölmesi için ne anlama geliyor; eşdeğer bir sayı yazılı değil.

**09-048.** Bir hissede çiftin geçiş sayısı yılda birkaç tane olduğundan Tansu'nun VAKBN–GARAN'ında 1,5 yılda 6 geçiş görülüyor; 5 çift × 9 yılda yaklaşık kaç bağımsız geçiş beklenir ve sınamanın birimi "bütün çift bölmesi" ise etkin N = 1 bölme değil mi?

**09-049.** Aynı sektörden seçilen 5 çift (ör. bankalar) ortak faktör taşır; "5 aktif çift" gözlemi 5 bağımsız örnek sayılırsa güç şişmez mi?

**09-050.** KURALLAR §3'teki "99 hissede 11 yılda 520 sıkışma dönemi" Yahoo ve bugünkü evrenle kaba sayım; kırılım koşulu, pozisyon sınırı ve ay başı evren filtresinden sonra EMA ailesi 100 işleme ulaşabiliyor mu, ulaşamazsa sonuç "kabul edilmedi" mi "ölçülemedi" mi?

**09-051.** Holm "o ana kadarki bütün denemelerle" yapılıyor (5.11); deneme sayısı zamanla büyüdüğünden erken kabul edilen bir aile sonradan eklenen denemelerle geriye dönük reddedilir mi, ve "Canlı" statüsü geri alınır mı?

**09-052.** Deneme birimi 5.11'de "tarih, aile, çıkış, parametre, veri anlık görüntüsü, kod hash", sorgu-2 S2-45'te "aile, varyant, parametre"; veri anlık görüntüsü farklı bir yeniden koşu yeni deneme sayılıyor mu, ve iki belgeden hangisi bağlayıcı?

**09-053.** Hata düzeltmesi sonrası yeniden koşu kod hash'ini değiştirir; bu yeni bir deneme mi (Holm m artar) yoksa aynı denemenin düzeltilmiş hali mi, ve bu ayrımı kim hangi kuralla yapıyor?

**09-054.** Geliştirme sırasındaki 200 tekrarlı koşular, motor sınamaları ve sadakat kontrolü adayları deneme günlüğüne yazılıyor mu; yazılmayan her koşu Holm düzeltmesini sessizce gevşetir.

**09-055.** KURALLAR başında "her YORUM sınamada deneme sayısına girer" deniyor, KURALLAR §4'te sapma formülü için birden çok aday formül deneniyor; seçilmeyen adaylar da m'ye sayılıyor mu?

**09-056.** 5.10'daki rastgele ızgaranın her hücresi ayrı deneme sayılır mı; 50 hücre Holm m'yi 50 artırırsa kabul eşiği yarı yarıya düşer ve ızgara sağlamlık kontrolünden cezaya dönüşür.

**09-057.** %0,1 / %0,3 / %0,5 masraf senaryoları (5.4) üç ayrı p değeri üretir; bunlar Holm ailesine ayrı denemeler olarak mı giriyor yoksa tek denemenin varyasyonu mu?

**09-058.** Deneme günlüğü kullanıcının kendi tuttuğu bir dosya ise değiştirilemezlik ve zaman damgası garantisi yok; Levent günlüğe yazmadan elle koşu yapabilir, bu durumda Holm düzeltmesi neye dayanıyor?

**09-059.** Giriş bölümü "tutmazsa değiştirilmiş hali yeni deneme sayılır"; bir aileye getirilebilecek varyant sayısında üst sınır yok, sınırsız deneme sonunda Holm eşiği ulaşılamaz hale gelmez mi?

**09-060.** Holm yalnız ailenin I. tür hatasını (FWER) kontrol eder; 6 kriterin AND'i ve %0,5 masrafta tekrar koşusu ile birleşince toplam yanlış-pozitif oranı ölçülüyor mu, örneğin sistem rastgele üretilmiş kurallarla uçtan uca koşulup yanlış kabul oranı kalibre ediliyor mu?

**09-061.** 5.10 "ek: parametre kaydı" diyor ama TASARIM'de böyle bir ek yok (Ek A yalnız bulgu tablosu); ızgara aralığı, hücre sayısı ve örnekleme dağılımı nerede önceden yazılı?

**09-062.** "Pozitif hücre oranı raporlanır" ama 5.12.5 sağlamlık şartının eşiğini vermiyor; null altında pozitif hücre oranı yaklaşık %50 olacağından hangi oran "sağlam" sayılır?

**09-063.** Izgara hücreleri aynı veriyi ve çoğunlukla örtüşen işlemleri paylaşır; pozitif hücre oranı bağımsız hücreler gibi yorumlanırsa ne anlama gelir?

**09-064.** Izgara hücresinde "pozitif" hangi ölçüye göre: K1'e göre mi, K2'ye göre mi, hangi masrafla?

**09-065.** Altı kriterin hepsi sağlanmalı (5.12); her kriter gerçek bir etki varken %80 olasılıkla geçse bile ortak geçme olasılığı bağımsızlıkta 0,8^6 ≈ %26'dır, tasarım bu ortak yanlış-negatif oranını hesapladı mı ve kabul edilebilir buldu mu?

**09-066.** %0,5 masraf eşiği (kriter 3) etkiyi yarıya indirebilir ve gücü düşürür; gerçek ve Tansu'nun iddia ettiği büyüklükte bir etkiyi ölçüt geçirebilir mi, bunu bilinen pozitif kontrolle (enjekte edilmiş sentetik etki) sınayan bir adım var mı?

**09-067.** 5.12.6 "kâğıt üstü fazla getiri doğrulamadaki etkinin en az yarısı" nokta tahmini oranıdır; kâğıt dönemde 30 işlemle gürültü bu oranı kontrol altında tutamaz, bu ölçütün gerçek bir etki varken geçme olasılığı nedir?

**09-068.** Doğrulama etkisi, birçok varyant arasından geçen bir kuralın etkisi olduğundan yukarı yanlıdır (kazananın laneti); "yarısı" bu şişmeyi karşılamak için mi seçildi, yoksa keyfi mi?

**09-069.** Kriter 4 "en iyi %5 işlem atılınca sonuç hâlâ pozitif" hangi ölçüyle (ortalama mı) ve 100 işlemde 5 işlemi atmak yeterince ayırt edici mi; kalan 95 işlem hâlâ aynı birkaç tavan serisinin etkisini taşıyabilir.

**09-070.** Kriter 2 yalnızca "K2'ye göre portföy fazla getirisi pozitif" diyor; nokta tahmin işareti gürültüde yaklaşık %50 geçer, bu kriter fiilen bilgi taşıyor mu yoksa yalnız bir form şartı mı?

**09-071.** "Portföy kuralı: en büyük düşüş %25'i, düşüşte kalma 12 ayı geçmez" (5.12 sonu) altı kriterin parçası mı, hangi dönem ve hangi masrafla ölçülür; Tansu'nun kendi VAKBN–GARAN sonucunda MaxDD −%27,4 olduğuna göre sadakat sınaması bu kuralı baştan ihlal etmiyor mu?

**09-072.** Altı kriterden kriter 6 ancak kâğıt dönemden sonra ölçülebiliyor; kriter 1–5 geçince aile "Canlı" mı yoksa "Kâğıt" mı, ve 6 ay boyunca kartlar üretiliyor mu üretilmiyor mu (6. bölüm "yalnız Canlı aileler" diyor)?

**09-073.** Kâğıt dönem en az 6 ay ve 30 kapanmış işlem (5.8); 30 işlemle işlem başına fazla getirinin SE'si ne kadar, ve bu dönem kriter 6'yı gerçekten sınayabilecek güçte mi?

**09-074.** "İşlem sayısı dolana kadar uzar" isteğe bağlı durdurma (optional stopping) üretir; kâğıt dönemde ne zaman, kaç kez bakılacağı ve durdurma kuralı önceden yazılı değilse sonuç favori anda kesilir.

**09-075.** Kâğıt işlemler simülasyondaki AOF dolum varsayımıyla mı kapatılıyor yoksa Levent'in gerçek dolumuyla mı; birincisi gerçek yürütmeyi ölçmez, ikincisi kuralın değil Levent'in performansını ölçer.

**09-076.** Kâğıt dönem boyunca İş Yatırım verisi düzeltmeler ve yeni bedelsizler nedeniyle geçmişe dönük değişir (veri-kaynakları, 4); kâğıt dönem sonuçları hangi anlık görüntüyle kilitleniyor?

**09-077.** 6 aylık kâğıt dönem tek bir piyasa rejiminde geçerse sepeti geçmek rejime bağlıdır; kriter 6 tek rejimle "doğrulamadaki etkinin yarısı" şartını nasıl anlamlı yorumlar?

**09-078.** "Kural, parametreler ve kod hash'i ilk getiri koşusundan önce kayda geçer" (5.8) ama doğrulama 2015–2026'nın tamamını bu hash ile koşar; hash sonrası yapılan her hata düzeltmesi "yeni deneme" olduğunda ayrılmış dönem yeniden başlıyor mu?

**09-079.** Hash kapsamına bağımlılık sürümleri (pandas-ta-classic, statsmodels), rastgele tohum ve veri anlık görüntüsü dahil mi; dahil değilse aynı hash farklı sonuç üretebilir.

**09-080.** Kural kaydı yerel bir git commit'i ise tarihi geri çevrilebilir; "kayıttan sonrası ayrılmış dönem" iddiasını dışarıdan doğrulanabilir kılan bir zaman damgası mekanizması var mı?

**09-081.** 5.8 "iki aile ve bu tasarım o döneme bakılarak yazıldı"; hangi iki aile ve hangi bilgi sızdı, ayrıca bu sızıntıyı ölçecek ya da sınırlayacak bir kontrol tanımlandı mı?

**09-082.** Aile seçim ölçütü 3 "Tansu sayısal bir sonuç göstermiş" (KURALLAR §3); seçim, Tansu'nun başarılı gösterdiği örneklere dayanıyor, bu seçim yanlılığı Holm m'ye kaç deneme olarak giriyor?

**09-083.** Aynı yeni ayrılmış dönemde üç aile paralel kâğıt işlemde; her aile için kriter 6 ayrı bir test olduğundan çoklu karşılaştırma düzeltmesi kâğıt dönemde de uygulanıyor mu?

**09-084.** Kriter 6'da "etki" işlem başına fazla getiri mi, yıllıklandırılmış portföy fazla getirisi mi; 9 yıllık doğrulama ile 6 aylık kâğıt dönemi aynı birimde karşılaştırmak için yıllıklandırma kuralı yazılı değil.

**09-085.** Canlı dönemde evren her ay PD ile yeniden kuruluyor; İş Yatırım PD alanının geriye dönük düzeltilip düzeltilmediği bilinmiyorsa kural-hash'i evren verisini kapsıyor mu?

**09-086.** Tavan kilidi (düşük = yüksek = tavan) kâğıt dönemde de giriş yapılamaz sayılıyor; BIST'te kırılım sinyali sonrası tavan serileri sık olduğundan işlem sayısı 30'a ulaşmayabilir, bu kayıp kural lehine mi aleyhine mi okunuyor?

**09-087.** Çift bölmesinde günlük fazla getiri serisi (5.8) için örneklem şartı tanımsız; kâğıt dönemde 6 ay ≈ 126 işlem günü ve günlük SD %1 ise saptanabilir yıllık etki yaklaşık ne kadardır ve bu etki masrafı aşıyor mu?

**09-088.** Çiftler "aynı sektör" içinden seçildiğinden (5.6) çift sayısı küçük sektörlerde 5'ten az olabilir; çift sayısı değişkense sınamanın birimi "bütün çift bölmesi" yıllar arasında karşılaştırılabilir mi?

**09-089.** Yıl başı seçimi (p < 0,05, 252 gün) ile yıl içi sinyalleri aynı çiftlere uyguladığından eşbütünleşme bağı seçim penceresinde zaten "kanıtlanmış"; K1'in rastgele geçişleri bu bağdan yararlanmaz mı ve bu yüzden K1'in gücü düşük olmaz mı?

**09-090.** Çift rotasyonunda pozisyon her an çiftin bir hissesindedir; ortalama maruziyet %100 ama beta çiftin hisselerine göre farklıdır (Tansu'nun regresyonla bulunan ≈1:0,4 oranı); fazla getiri beta farkı için düzeltiliyor mu?

**09-091.** 5.2 "mutlak getiriler üst sınırdır, karar için kullanılmaz" diyor; ama kabul ölçütü yalnız göreli (K1, K2) iken sepete göre pozitif ama mutlak olarak negatif ya da faizin altında bir aile "Canlı" olabilir mi?

**09-092.** Kapanmış/işlemden kalkmış hisselerin son günleri (askıya alma, çıkış fiyatı) veride yok; kural bu hisselerde pozisyondayken veri biterse işlem nasıl kapanıyor, ve bu kayıp K1/K2'ye simetrik yansıyor mu?

**09-093.** 5.2'de 2015 BIST30 sabit listesiyle "yanlılığın büyüklüğü ölçülür"; ölçülen fark kabul/ret kararını etkiliyor mu, hangi farkın üstünde sonuç geçersiz sayılıyor?

**09-094.** Tedbirli hisseler (VBTS, brüt takas, tek fiyat; Açık soru 4) bedava veriyle ayrılamıyor; kırılım sinyalleri tedbir öncesi sert yükselişlerde yoğunlaştığından kural tedbirli günlerde sinyal alırken K1 rastgele günleri tedbirsiz olabilir, bu fark nasıl ele alınıyor?

**09-095.** İşlem ertesi günün AOF'undan modelleniyor (5.3); kırılım sinyali sonrası gün hacim ve boşluk bakımından rastgele günden farklıdır, sabit %0,3 masraf bu sinyale özgü AOF kaymasını karşılar ve K1 bu etkiyi dengeler mi?

**09-096.** Sabit %0,3 masraf tüm hisselere uygulanıyor; K1 türü (a) başka hisse seçerken likidite ve kayma bakımından eşleştirme yapmıyor, daha az likit hisselere düşen rastgele işlemler kuralla aynı masrafı ödeyerek karşılaştırmayı bozmaz mı?

**09-097.** "Kural-hash holdout" yalnız ileriye dönük veriyi korur; BIST'te canlı dönemde bedelsiz/temettü sonrası geçmiş fiyatlar yeniden ölçeklendiğinde göstergeler ve sinyal tarihleri değişebilir, kayıtlı kural aynı sinyalleri üretmeye devam eder mi?

**09-098.** Birden çok seviyede (aile × masraf × K1 türü × ızgara hücresi × yıl) çoklu karşılaştırma var; toplam m kaç ve "hiçbir aile geçmedi" sonucu bu m ile neredeyse garanti değil mi, böyle bir sonucun bilgi değeri nedir?

**09-099.** Gerçek bir etki yokken (null) üç ailenin birinin bile 6 kriteri geçme olasılığı bu tasarımda hesaplandı mı ve hesaplanmadıysa "ölçüt önceden yazıldı" iddiası neyi garanti ediyor?

**09-100.** TASARIM 4 "İstatistik modülü canlı kâğıt üstü işlemde de aynısı kullanılır" diyor; 30 işlemlik örnekte 20 günlük blok bootstrap yalnız birkaç blok verirken ve 1.000 permütasyon aynı p çözünürlüğünü verirken aynı modül iki rejimde nasıl geçerli kalır?
