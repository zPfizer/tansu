# Sorular 14: Test stratejisi

14-001. TASARIM.md §4 her modülün "küçük bir yüzü" olduğunu söylüyor; testler hangi yüzlerden yazılacak ve bir modülün içi değişince hangi testlerin kırılmaması gerekiyor?

14-002. Adım fonksiyonu (pozisyon, bugünkü mum) → pozisyon imzasıyla hem sınamada hem canlıda kullanılıyor (A5). Bu fonksiyonun ayrı test edilmesi mi, yoksa yalnız Motor üzerinden dolaylı test edilmesi mi gerekir, ve "ikisi ayrışamaz" iddiasını hangi test kanıtlar?

14-003. Motor "belirleyici" (A2, A3) deniyor. Aynı girdiyle iki koşunun bire bir aynı işlem listesini verdiğini hangi test, hangi karşılaştırma yöntemiyle (hash, DataFrame eşitliği, tolerans) doğrular?

14-004. Mevcut `tests/test_kanit.py` `MASRAF == 0.002` ve alış 0,20 + satış 0,22 varsayıyor; TASARIM 5.4 ise her yönde %0,3 diyor. Eski testlerin hangileri yeni tasarımda tamamen silinecek, hangileri uyarlanacak?

14-005. §5.3 "Her kural için motor sınamaları (kod yazılmadan önce)" yedi durum sayıyor. Bu yedi durum yeterli mi; giriş günü stop kontrolü, giriş günü hem stop hem hedef, ve ertesi gün hiç verisi olmayan sinyal hangi testlere dahil?

14-006. Hedefte çıkış, stopta çıkış, boşluklu stop, aynı gün stop+hedef, tavan girişi, taban kilidi ve bozulma çıkışı için elle hesaplanan beklenen değerleri kim doğrulayacak? Hesabı yazan ile kodu yazan aynı ajan olursa elle hesap bağımsız sayılır mı?

14-007. Elle hesaplanmış örneklerdeki sayılar testin içinde mi, yoksa ayrı bir tablo dosyasında (CSV/JSON) mı durmalı? Levent bu sayıları okuyup "doğru mu" diye kontrol edebilecek mi?

14-008. Stop dolumu kuralı (5.3, S2-8) "gün düşüğü ≤ stop ise stop fiyatından; gün yükseği de stopun altındaysa AOF'tan". Gün düşüğü tam stopa eşitken ve gün yükseği tam stopa eşitken kenar durumlar hangi testlerle ayrı ayrı sabitlenecek?

14-009. Kilitli tavan ve kilitli taban tanımı "düşük = yüksek = tavan" (5.3). Float karşılaştırmasında tam eşitlik mi, tolerans mı kullanılacak ve bu seçimi hangi test zorlar?

14-010. Fiyat limiti 12.03.2020'de ±%20'den ±%10'a geçiyor (5.1). Limit değişim gününün iki yanındaki karantina eşiği testleri nasıl yazılacak, ve ECILC/RYSAS 12.03.2020 örneği sabit test verisine alınacak mı?

14-011. Test mumları sentetik mi (elle yazılmış 5-10 satır) yoksa gerçek İş Yatırım verisinden kesilmiş mi olacak? Her iki türün hangi seam'de kullanılacağı nasıl bölüştürülecek?

14-012. Gerçek veriden kesilmiş fixture'lar repoya girerse İş Yatırım kullanım koşulları (TASARIM §8 açık soru 1) bilinmeden dosyayı depoda saklamak sorun yaratır mı?

14-013. Gerçek veri fixture'ı "veri anlık görüntüsü" (B2) gibi tarihli ve değişmez mi olacak? Kaynak geçmişi sonradan değiştirirse fixture'ın yeniden indirilmesine kim ve hangi testle karar verecek?

14-014. Testler hiçbir koşulda ağa çıkmamalı mı? Bunu zorlayan bir mekanizma (soket engeli, pytest eklentisi) olacak mı, yoksa yalnız disiplin mi?

14-015. İş Yatırım `HisseTekil` ve borsapy istemcileri testte nasıl yerine konacak: kayıtlı yanıt (cassette, vcr/responses), elle sahte sınıf, ya da istemciyi saran ince bir arayüz? Hangisi "minimum altyapı" ilkesine uyar?

14-016. Canlı kaynağa karşı çalışan "duman testi" hiç olacak mı? Olacaksa kim, ne sıklıkla çalıştıracak ve başarısız olursa sistemin "kart üretilmez" davranışıyla nasıl ilişkilenecek?

14-017. İş Yatırım API'sinin şeması sessizce değişirse (sütun adı, `HACIM` birimi) hangi test bunu yakalar? Sözleşme testi yalnız canlı veriyle mümkünse hermetik ilkeyle çelişmez mi?

14-018. `HACIM` biriminin (lot mu TL mi) ilk veri işinde çözülmesi planlanıyor (5.1). Bu çözümün sonucu bir testle mi kaydedilecek, ve birim yanlış çıkarsa hangi testler sessizce yanlış geçer (likidite %2 kuralı gibi)?

14-019. Şirket olayı düzeltmesi kodda bir kez uygulanıp İş Yatırım `HGDG` ile karşılaştırılıyor (5.1). Bu karşılaştırma bir test mi, yoksa her koşuda çalışan bir çalışma zamanı denetimi mi? İkisi arasındaki sınır nerede?

14-020. Düzeltme katsayısı `SHHE_FIYAT_AYAR_OR` için hangi elle hesaplanmış örnekler kullanılacak (bedelsiz, bölünme, bedelli, temettü ayrı ayrı) ve bedelli ile temettü katsayısının formülü kimden doğrulanacak?

14-021. Temettü kaydındaki tarih hak kullanım günü mü ödeme günü mü (§8 açık soru 2) bilinmiyor. Bu belirsizlik varken düzeltme testinin beklenen değeri nasıl yazılır; yanlış varsayım testi tautolojik yapmaz mı?

14-022. Karantina kuralı "limiti +%0,5 aşan ve olayla açıklanmayan" günü dışlıyor. Olayla açıklanan sıçrama ile açıklanmayan sıçramanın aynı gün çakıştığı durumlar için test var mı?

14-023. Takvim modülü BIST tatillerini ve yarım günleri içeriyor (A1). Bayram tatili uzatması gibi tarihler koda sabit yazılırsa hangi test bu listenin eksikliğini yakalar?

14-024. Evren modülü "nokta-zamanlı en büyük 100" üretiyor (5.2). Gelecek bilgisi sızıntısını (look-ahead) yakalayan test nasıl yazılır: bir tarihe kadar kesilmiş veriyle üretilen evren, tam veriyle üretilenle aynı mı diye mi?

14-025. Look-ahead sızıntısı yalnız Evren'de değil, göstergelerde, ATR'de, çift seçiminde (yıllık eşbütünleşme) de var. Bu sızıntıyı bütün seam'lerde birden yakalayan genel bir test (veriyi t gününde kesip sonucun değişmediğini doğrulama) olacak mı?

14-026. Kapanmış hisselerin (ASYAB gibi) hayatta kalan yanlılığı testi nasıl yapılır? Evrenin kapanmış sembolü içerdiğini doğrulamak için hangi fixture gerekir?

14-027. Maliyet modülü "takılıp çıkarılabilir" (A1). Maliyet sıfırken sonucun brüt getiriyle bire bir eşit olduğunu doğrulayan bir test var mı, ve %0,1/%0,3/%0,5 senaryoları için ayrı elle hesaplar yazılacak mı?

14-028. Likidite sınırı "son 10 günün medyan TL işlem tutarının %2'si" (5.4). Sınırda tam eşit, bir lot fazla ve yetersiz veri (10 günden az) durumlarının her biri ayrı test mi olacak?

14-029. Simülatörde "aynı gün sinyal sayısı boş yeri aşarsa en likit önce" (M12) kuralı var. Eşit likiditede sıralamanın deterministik olması hangi testle sabitlenecek?

14-030. Tek pozisyon en fazla sermayenin %10'u, en fazla 10 pozisyon, %1 risk, kaldıraç yok (5.6). Bu üç sınırın aynı anda bağlayıcı olduğu bir elle hesaplanmış senaryo yazılacak mı, ve adet yuvarlamasının (lot, aşağı/yukarı) test edilmesi nasıl olacak?

14-031. Çift bölmesinde "her çift payı her an çiftin bir hissesindedir" (5.6). Bu değişmezi (invariant) her gün kontrol eden bir test veya çalışma zamanı kontrolü olacak mı?

14-032. Yıllık çift seçiminde düşen çiftin pozisyonunun kapanması ve payın yeni çifte geçmesi (S2-25..27) karmaşık bir durum geçişi. Bu geçiş hangi küçük elle hesaplanmış takvimle test edilecek?

14-033. Boştaki nakdin politika faizi kazanması (B4) için hangi elle hesap yazılacak? Politika faizinin toplantı günlerinde basamak değiştirdiği ve hafta sonu/tatil günlerinin faiz birikimine girip girmediği bir testle sabitlenecek mi?

14-034. Sermaye eğrisinin son değeri ile işlem listesinin toplamı arasında muhasebe tutarlılığı (nakit + pozisyon değeri = toplam) her koşuda doğrulanacak mı, ve bu denetim test mi çalışma zamanı kontrolü mü?

14-035. İki bölme türü için ortak bir simülatör arayüzü mü olacak, yoksa iki ayrı modül mü? Testler arayüze mi yazılacak yoksa her uygulamaya ayrı mı?

14-036. Fazla getiri tanımı iki seviyede (işlem ve portföy, 5.7). İşlem seviyesi sepet getirisinin "aynı tutma süresi" için hesaplanması elle hesaplanmış küçük bir 3 hisseli evrenle test edilecek mi?

14-037. K1 eşleştirilmiş rastgele kuralın iki türü ((a) aynı gün başka hisse, (b) aynı hisse ±20 gün) için "hisse başına eşleştirilmiş sayı" özelliği hangi testle doğrulanır? Rastgele örnekleme küçük bir evrende tam sayılabiliyorsa, tam sayım ile örnekleme karşılaştırılacak mı?

14-038. "Pozisyon sınırı ve sıra kuralı rastgele kurala da uygulanır" (S2-44). Rastgele kuralın gerçek kuralla aynı simülatörden geçtiğini hangi test garanti eder?

14-039. Rastgele kural yalnız ailenin ön şartlarını sağlayan günlerden seçiliyor. Ön şart kümesi boşsa veya gereken sayıdan küçükse hangi davranış beklenir ve bu hangi testle sabitlenir?

14-040. Permütasyon ve bootstrap testleri sabit tohumla (seed) deterministik mi yapılacak? Tohum değiştiğinde testin hâlâ geçmesi gerekip gerekmediği nasıl karar verilir?

14-041. Sabit tohumlu bir istatistik testi sayısal Python/numpy sürümü değişince farklı rakam verirse bu test kırılması bir hata sayılır mı? Rastgele sayı üreteci olarak `numpy.random.default_rng` (PCG64) sürüm kararlılığına güvenilecek mi?

14-042. Güven aralığı 20 günlük bloklarla yeniden örnekleme (5.9) kullanıyor. Bu yöntemin doğruluğu, bilinen bir otokorelasyonlu seride (ör. AR(1)) kapsama oranı simülasyonuyla mı sınanacak, ve bu sınama test paketine mi girer yoksa yavaş ayrı bir doğrulamaya mı?

14-043. Kapsama oranı sınaması binlerce yeniden örnekleme gerektirir. Test hızı hedefi (ör. tüm paket kaç saniye) ile istatistiksel gücü nasıl dengelemeyi düşünüyorsunuz?

14-044. Boş (sıfır varyanslı) fazla getiri serisi, tek işlem, ve 60'tan az sinyal günü gibi uç girdilerde istatistik modülü hata mı verir, NaN mı döner, yoksa "yetersiz örneklem" mi der? Bu hangi testlerle sabitlenir?

14-045. p değeri 1.000 tekrardan çıkıyor ve Holm düzeltmesi uygulanıyor (5.11). Holm düzeltmesi küçük elle hesaplı bir p değerleri listesiyle mi, yoksa statsmodels sonucuyla mı doğrulanacak? Kütüphane çıktısını beklenen değer yapmak tautolojik olmaz mı?

14-046. statsmodels, quantstats ve pandas-ta-classic güvenilen kütüphaneler olarak seçilmiş. Kütüphanenin kendi işlevini yeniden test etmek gerekir mi, yoksa yalnız bizim ona verdiğimiz girdileri ve çıktıyı yorumlama kodunu mu test ederiz?

14-047. "Bu örneklemle saptanabilecek en küçük etki" (5.9) hesabı için bilinen bir etki gömülü sentetik veride gücü doğrulayan bir test olacak mı?

14-048. Sentetik veride bilinen etki gömme (ör. gerçek kenarı olan bir kural enjekte etme) ve sistemin onu bulup bulmadığını sınama, hem motor hem istatistik için uçtan uca bir "pozitif kontrol" olarak planlanıyor mu?

14-049. Tersi: hiçbir kenarı olmayan saf rastgele yürüyüş verisinde sistemin "hiçbir aile geçmedi" demesi (yanlış pozitif oranı) bir test mi olacak? Yanlış pozitif oranı 5%'in altında mı kalmalı ve bu kaç koşuyla ölçülür?

14-050. Kabul ölçütü §5.12 altı koşuldan oluşuyor. Her koşulun tek başına sınır değerinde (tam %60 yıl, tam p=0,05) doğru karar verdiği hangi testle gösterilecek?

14-051. "Hiçbir aile geçmedi" ekranı birinci sınıf sonuç (§1). Bu durumun rapor ve Streamlit ekranında hata vermeden doğru görüntülendiğini hangi test kontrol eder?

14-052. Deneme günlüğü (5.11) yazma işlemi yan etkili ve kalıcı. Testlerin gerçek günlüğü kirletmediğini ve geçici dizinde çalıştığını nasıl garanti edeceksiniz?

14-053. Kural kaydı ve kod parmak izi (hash) (5.8) için hangi test yazılır: kodda tek satır değişince hash'in değiştiğini mi, yoksa boşluk/yorum değişince değişmediğini mi doğrulamak gerekir? Hash neyin üzerinden alınır?

14-054. Kural kaydı "ilk getiri koşusundan önce" yapılmalı. Bu sıralamayı kodda zorlayan bir kapı (gate) ve onu sınayan test olacak mı?

14-055. Sadakat kontrolü (KURALLAR §4) Tansu'nun rakamlarını yeniden üretiyor (VAKBN–GARAN z −3,108, KRDMD %0,64, D = 11,29/10,05/70,25). Bu kontrol bir pytest testi mi, bir rapor betiği mi, yoksa ikisi birden mi?

14-056. Sadakat kontrolünün beklenen değerleri Tansu'nun görsellerinden elle okunmuş sayılar. Bu sayıların yanlış okunması ihtimalini (not ile görsel çelişkisi, KURALLAR §1.3) test altyapısı nasıl yönetir?

14-057. Sadakat kontrolü Yahoo verisini kullanıyor (§7.2), oysa Yahoo başka her yerde yasak. Yahoo verisi testlerde hermetik olarak nasıl donduruluyor ve bu fixture'ın yeniden üretilebilirliği nasıl kaydedilir?

14-058. Sadakat kontrolünde "birden çok aday formül denenir, en iyi üreten seçilir". Hangi tolerans (yuvarlama, ±0,001, ±%1) "üretildi" sayılır ve bu tolerans sonuca bakılarak mı seçilecek?

14-059. Sadakat sonucu "üretilemedi" ise ilgili parça YORUM kalıyor (§8.5). Bu durumda sadakat testi başarısız mı sayılır, atlanır mı (xfail/skip), ve test paketi yeşilken sessizce kırmızı bir gerçeği gizler mi?

14-060. Sadakat kontrolü Yahoo açılışını kullanan "T+1 açılış" varyantını da üretiyor (S2-7). İki varyantın (AOF ile Yahoo açılışı) aynı Adım fonksiyonunu kullandığı nasıl test edilir?

14-061. Pivot (tepe/dip) bulma ayarı kaynakta yok ve sadakatle seçilecek. Pivotun yalnız teyit edildiği gün görünür olması (gelecek barlara bakmama) hangi testle zorlanır?

14-062. Çift rotasyonunda sapma formülü ve pencere (60/120) belirsiz. Aday formüllerin her biri için aynı test paketi mi koşacak, yoksa seçilen formül kilitlendikten sonra mı test yazılacak?

14-063. Çift rotasyonunun "Z ≤ −2 ve ΔZ > 0" kuralı tam sınırda (Z = −2 tam, ΔZ = 0 tam) nasıl davranır? Bu kenar durumları hangi elle hesaplı seri test eder?

14-064. EMA sıkışması için "bant ≤ %1,2, en az 3 gün" ve giriş tetiği "sıkışma bittikten sonra 10 gün içinde kapanış en yüksek fiyatın üstüne çıkarsa". Tam 3. gün, tam %1,2 ve tam 10. gün kenarları için ayrı sentetik seriler yazılacak mı?

14-065. EMA200 gibi uzun göstergelerin ısınma (warm-up) döneminde ürettiği NaN'ların sinyal üretmediği hangi testle sabitlenecek? pandas-ta-classic'in ısınma davranışı sürümler arası değişirse ne olur?

14-066. Göstergeler için kütüphane (pandas-ta-classic) kullanılıyor. Kütüphane sürümünün yükseltilmesi sinyal günlerini değiştirirse, bunu yakalayan bir altın dosya (golden file) tutulacak mı?

14-067. Altın dosya: hangi çıktıların (sinyal listesi, işlem listesi, sermaye eğrisi, rapor metni) altın olarak saklanacak? Her dosyanın boyutu ve kaç tane olacağı nasıl sınırlanır?

14-068. Altın dosya değiştiğinde güncelleme kararını kim, hangi inceleme ile verecek? Levent diff'i okuyamıyorsa "testi geçir diye altını yeniden üret" refleksi nasıl engellenir?

14-069. Markdown raporun tamamı altın dosya olursa tarih/saat ve sürüm gibi değişken alanlar testi kırar. Raporun hangi bölümleri deterministik kabul edilir ve değişken alanlar nasıl maskelenir?

14-070. Rapor ve CSV kart listesinde Türkçe karakterler ve ondalık ayırıcı (virgül/nokta) Windows 11 yerel ayarına göre değişebilir. Bu kodlama ve yerel ayar farkını hangi test yakalar?

14-071. Windows'ta satır sonu (CRLF/LF) ve dosya yolu ayırıcıları altın dosya karşılaştırmasını bozabilir. Karşılaştırma bu farklara karşı nasıl sağlamlaştırılacak?

14-072. Hypothesis (özellik tabanlı test) kullanılacak mı? Kullanılacaksa hangi değişmezler adaydır: sermaye hiç negatif olmaz, stop dolumu hiçbir zaman gün aralığının dışında olmaz, masraf getiriyi hiç artırmaz?

14-073. Hypothesis eklemek yeni bir bağımlılık. "Minimum altyapı" ilkesine göre elle yazılmış 10-20 kenar durumu yetmez mi? Hypothesis'in somut bir hatayı yakalayıp yakalamayacağı önceden nasıl tahmin edilir?

14-074. Hypothesis'in ürettiği rastgele OHLC mumlar fiziksel olarak geçerli olmalı (düşük ≤ açılış/kapanış ≤ yüksek). Bu kısıtların stratejisini yazmak testin kendisinden daha karmaşık olursa kabul edilir mi?

14-075. Hypothesis başarısız örnekleri veritabanına (.hypothesis klasörü) yazar. Bu klasör depoya girer mi, ve Levent'in PC'sinde başka bir yerde çalışırken tekrar üretilebilirlik nasıl sağlanır?

14-076. Mevcut testlerin neredeyse tamamı "düz seri + tek sıçrama" gibi sentetik mumlara dayanıyor. Bu mumların gerçek piyasanın bozuk özelliklerini (boşluk, tek fiyat seansı, hacimsiz gün) taşımadığı riski hangi testle kapatılır?

14-077. Testte kullanılan sentetik "ATR 2,5" gibi kurulumlar, kodun ATR hesabını doğrudan yeniden yazarak beklenen değeri üretirse tautoloji olur. Beklenen değerlerin koddan bağımsız (elle) üretildiğini nasıl denetlersiniz?

14-078. Bir test, uygulamadaki sabiti (ör. `MASRAF`, 2 ATR, 250 gün) içe aktarıp onunla karşılaştırıyorsa hiçbir şeyi sınamaz. Sabitlerin testlerde bağımsız yeniden yazılması mı, yoksa parametre kaydından okunması mı kuraldır?

14-079. Mutasyon testi (mutmut, cosmic-ray) ile testlerin gerçekten bir şey yakaladığı ölçülecek mi? Bu araç Windows'ta çalışıyor mu ve tek kişilik proje için fazla mı?

14-080. Kapsam (coverage) hedefi olacak mı: satır, dal (branch), ya da hiç? Hedef sayı varsa neden o sayı, ve yalnız motor/simülatör/istatistik için mi, bütün paket için mi?

14-081. Yüksek kapsam tautolojik testlerle de elde edilebilir. Kapsam yerine "yedi motor durumu + sadakat + pozitif kontrol" gibi davranış listesinin tamlığı mı ölçü olacak?

14-082. Streamlit "Kanıt" ekranı (§3) test edilecek mi? Streamlit `AppTest` ile mi, hiç test edilmeden mi (ekran yalnız raporu okuyor), yoksa ekranın ince tutulup test edilecek mantığın raporlama modülüne taşınması mı?

14-083. Günlük işleyiş 19:30'da çalışıyor (§6) ve "veri taze değilse kart üretilmez" (m6). Bu zamanlanmış görevin (Windows Görev Zamanlayıcı) ayrı bir uçtan uca testi olacak mı, yoksa yalnız fonksiyon testleri mi?

14-084. Tazelik kontrolü "son çubuğun tarihi bugün değilse" (5.1) saat ve saat dilimine bağlı. Testlerde sistem saati nasıl sabitlenecek (freezegun, parametre olarak geçirilen tarih)? Hangisi minimum altyapıdır?

14-085. Tatil günü ve hafta sonu çalıştırmada (Takvim) sistemin davranışı (kart yok, hata yok) nasıl testle sabitlenir?

14-086. Test hızı hedefi nedir: tüm paket kaç saniyede bitmeli? 100 hisse × 11 yıl günlük veriyle motor testleri yavaşsa, hangi testler "hızlı" hangileri "yavaş" işaretlenip ayrılır?

14-087. Tam tarihsel koşu (2015–2026, 1.000 rastgele tekrar, ızgara) saatler sürebilir. Bu koşunun kendisi bir test sayılır mı, yoksa test paketinin dışında bir üretim koşusu mu? Aradaki ayrım Levent'e nasıl anlatılır?

14-088. Testleri çalıştırmak için Levent'in ne yazması gerekecek? Tek bir komut (`pytest`) mu, bir `.bat` dosyası mı? Başarılı ve başarısız çıktıyı teknik bilgisi olmayan biri nasıl okuyacak?

14-089. Testler Levent'in Windows 11 PC'sinde mi, ajanların çalıştığı ortamda mı çalışıyor? İki ortam arasında Python ve kütüphane sürümü farkı sonucu değiştirirse bunu hangi mekanizma yakalar (kilit dosyası, uv, pip freeze)?

14-090. CI (GitHub Actions vb.) tek kişilik, uzak repo olmayan bir proje için gerekli mi (AGENTS.md: işler yerel `.scratch/`)? CI yoksa "her değişiklikte testlerin koştuğunu" ne garanti eder: pre-commit kancası, ajan talimatı, hiçbiri?

14-091. Ajanlar kodu yazıyor ve testleri de kendisi yazıyor. Bir ajanın testi geçsin diye testi gevşetmesini (assertion silme, tolerans büyütme, skip ekleme) hangi mekanizma önler?

14-092. TDD "kod yazılmadan önce motor sınamaları" (5.3) deniyor. Önce testin yazılıp başarısız (kırmızı) olduğunun kanıtı nerede tutulur? Sıra kaydı olmadan TDD iddiası denetlenebilir mi?

14-093. Test dosyası düzeni nasıl olacak: seam başına bir dosya mı, modül başına mı? Mevcut `test_nabiz_veri.py` gibi birden çok modülü karıştıran dosyalar yeni düzende nasıl bölünecek?

14-094. Piyasa durumu (nabız) kapı olmaktan çıkmış, yalnız etiket (§4). Mevcut `nabiz` testleri hâlâ anlamlı mı, ve bu modülün hangi davranışı (SMA 18/35 ile 20/50 çelişkisi) test edilecek bir tanım olarak kabul edilebilir?

14-095. Birden fazla hisse aynı gün sinyal verdiğinde, sırayı ve pozisyon açma kararını etkileyebilecek hisse listesi sırası (sözlük/DataFrame sütun sırası) farkı sonucu değiştirirse bu bağımlılığı hangi test yakalar? Girdi karıştırılıp aynı çıktı beklenecek mi?

14-096. Aynı hissede pozisyon açıkken gelen yeni sinyalin sayıma girmemesi (C9, B5d) hem gerçek kuralda hem rastgele kuralda geçerli. İki yerde aynı kodun mu çalıştığı, yoksa iki ayrı uygulamanın mı olduğu bir testle nasıl ayrıştırılır?

14-097. Parametre sağlamlığı rastgele ızgara (5.10) ve "pozitif hücre oranı" raporluyor. Izgara örneklemesinin tohumlu ve yeniden üretilebilir olduğu ve oranın küçük elle hesaplı bir ızgarada doğru çıktığı test edilecek mi?

14-098. Test fixture'larındaki gerçek veriyi (örneğin CCOLA bölünmesi 13.08.2024, ECILC/RYSAS 12.03.2020) test içinde hangi biçimde (parquet, CSV, gömülü liste) saklamak, tek kişilik Windows kurulumunda ek bağımlılık gerektirmeden mümkündür?

14-099. Testler başarısız olduğunda hata mesajı Levent veya bir ajan için okunabilir mi? "assert a == b" yerine hangi gün, hangi hisse, hangi beklenen/gerçek değerle ve hangi kural maddesine (ör. §5.3 stop önce) atıf yapan mesaj yazılacak?

14-100. Test paketinin kendisinin ne zaman "yeterli" sayıldığı ve ne zaman değişeceği (kural kaydı gibi) nerede yazılı olacak? Kabul ölçütü önceden yazıldığı gibi, "testler tamam" ölçütü de önceden yazılıp tarihlenecek mi?
