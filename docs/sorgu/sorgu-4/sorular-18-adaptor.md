# Sorular 18: Dış kaynak adaptörleri

18-001. TASARIM.md §4 üç ayrı dış kaynağı (İş Yatırım, borsapy/TradingView, KAP, EVDS) kullanıyor. "Adaptör" sözcüğü modül tablosunda geçmiyor; bu kaynakların hangi modülün içinde, hangi sınırın arkasında duracağı nerede yazılı?

18-002. HTTP istemcisi olarak requests, httpx ya da borsapy'nin kendi içindeki istemci seçilebilir. pyproject.toml'da bağımlılık listesi bile yok; bu seçim hangi ölçüte göre yapılacak ve kim yapacak?

18-003. İş Yatırım `HisseTekil` için borsapy'nin kullanmadığı kendi çağrımız mı yazılacak, yoksa isyatirimhisse paketi mi kullanılacak? veri-kaynaklari.md §1.3 bu paketi "kurmadık" diyor; neden kurulmadan elendi?

18-004. Owner "güvenilir kütüphane, kendi yazılmış kod değil" istiyor. İş Yatırım için tek güvenilir seçenek kendi yazdığımız ince bir sarmalayıcıysa, bu istek nasıl karşılanmış sayılacak?

18-005. borsapy bağımlılığı sürüm sabitlenecek mi? borsapy tek kişilik, belgelenmemiş uç noktalara dayanan bir paket; yeni sürüm sessizce davranış değiştirirse backtest sonuçları nasıl korunur?

18-006. borsapy'nin 78 sermaye azaltımı kodunu atması (veri-kaynaklari.md §1.1) bilinen bir kusur. Paketi hâlâ bağımlılık olarak tutmak, bu kusurlu paketin başka hangi sessiz kusurlarını içeri alır?

18-007. borsapy hem TradingView WebSocket, hem TCMB sayfası, hem evren CSV'si, hem sektör bilgisi için kullanılıyor (TASARIM.md §4, §5.6). Tek bir paketin dört ayrı işi yapması, paket kırıldığında dört işin birden durması demek değil mi?

18-008. borsapy yalnızca "kişisel ve eğitim amaçlı" lisans notu taşıyor (veri-kaynaklari.md §3.1). Sistem yalnız Levent için çalışıyor; ama yarın bir arkadaşına verilirse bu koşul ne olur?

18-009. TradingView WebSocket gecikmeli (~15 dk) ve resmî değil. Çapraz kontrol kaynağı olarak kullanılan bu veri koptuğunda, §5.1'deki "tam karşılaştırma" adımı durur mu yoksa atlanır mı?

18-010. TASARIM.md §4 "Kullanım koşulları ve hız sınırları bulunamadı; az sayıda istek, yerel önbellek" diyor. "Az sayıda" kaç istek demek: 100 hisse × 11 yıl tek bir ilk indirmede kaç çağrıya denk gelir?

18-011. İlk toplu indirme (~100 aktif hisse, ayrıca kapanmış semboller) tek seferde mi yapılacak, yoksa günlere yayılacak mı? İş Yatırım IP engeli uyarısı (isyatirimhisse notu) göz önüne alınırsa ilk indirme neden ban riski taşımıyor?

18-012. İstekler arasında bekleme süresi saniye cinsinden kaç olacak ve bu değer kodda mı, ayar dosyasında mı duracak? Owner bu değeri değiştirebilecek mi?

18-013. Hız sınırlayıcı için hazır bir kütüphane (ör. tenacity, pyrate-limiter, hishel) mi kullanılacak, yoksa `time.sleep` mi? Hangisi "minimum altyapı" ölçütüne uyar?

18-014. Yeniden deneme (retry) politikası nerede tanımlı? 429, 5xx, bağlantı kopması ve boş yanıt için ayrı ayrı kaç deneme, hangi bekleme (üstel mi, sabit mi) uygulanacak?

18-015. Boş gövdeli 200 yanıtı İş Yatırım'da "hisse yok", "tarih aralığı boş" ve "engellendim" anlamlarından hangisi olabilir? Retry mantığı bu üçünü nasıl ayırt edecek?

18-016. Zaman aşımı değerleri (bağlantı, okuma) belirtilmemiş. 19:30 günlük koşuda bir uç nokta takılırsa bütün koşu kaç dakikada bırakılacak (TASARIM.md §6.1)?

18-017. İş Yatırım istekleri için User-Agent, Referer ve Accept başlıkları hangileri olacak? Tarayıcı taklidi başlık göndermek kullanım koşulları açısından kabul edilebilir mi?

18-018. `GetSermayeArttirimlari` önce hisse sayfasından oturum çerezi alıyor (veri-kaynaklari.md §1.1). Çerez süresi dolarsa ya da sayfa yapısı değişirse adaptör bunu nasıl fark edecek?

18-019. Çerez ve oturum yönetimi her koşuda baştan mı kurulacak, yoksa diske mi yazılacak? Diske yazılan oturum çerezi gizli veri sayılır mı?

18-020. HisseTekil tarih parametresi dd-mm-yyyy. Yaz saati, yerel saat dilimi ve "bugün" tanımı (İstanbul saati) adaptörde nerede sabitlenecek? Windows saati yanlış ayarlıysa ne olur?

18-021. HisseTekil yanıtında Türkçe ondalık virgül ve binlik nokta kullanımı var mı, yoksa sayılar JSON sayısı olarak mı geliyor? Ayrıştırma kuralı belgede doğrulanmış mı?

18-022. `SHHE_TARIH` milisaniye epoch olarak geliyor. Bu epoch UTC mi, yerel gece yarısı mı? Bir günlük kayma, bedelsiz düzeltmesini yanlış güne uygular; bunu hangi test yakalar?

18-023. HACIM biriminin lot mu TL mi olduğu bilinmiyor (TASARIM.md §5.1, S2-14). Birim adaptörde mi, alan adı eşlemesinde mi, yoksa veri deposunda mı sabitlenecek?

18-024. İş Yatırım `HGDG` alanlarının yarım gün (arife) seanslarındaki davranışı bilinmiyor. Takvim modülü (§4) ile adaptör arasındaki "bu gün veri bekleniyor mu" sorumluluğu kimde?

18-025. Adaptör sözleşmesi (schema) nerede tanımlı? Beklenen sütunlar, tipler ve boş olabilirlik pandera, pydantic ya da düz `assert` ile mi doğrulanacak?

18-026. İş Yatırım bir alan adını değiştirirse (ör. `HG_AOF` → başka ad) ne olur? Eksik sütun hata mı verir, yoksa pandas sessizce NaN mı üretir?

18-027. Alan eklenirse, çıkarılırsa ya da bir alanın anlamı değişirse (aynı ad, farklı birim) bu değişikliği yakalayacak kontrol var mı? Yalnız ad kontrolü anlam değişimini yakalamaz.

18-028. Şema değişikliği tespitinde koşu durdurulacak mı? Durdurulursa Levent akşam hiç rapor görmez; durdurulmazsa bozuk veriyle kart üretilir. Hangisi seçilir ve neden?

18-029. HGDG/HG oranı sabit olmalı (veri-kaynaklari.md §3.2: THYAO 0,9769). Bu oran adaptörde bir bütünlük kontrolü olarak mı kullanılacak? Temettü günü dışında oran sıçrarsa ne yapılacak?

18-030. İş Yatırım geçmiş veriyi sonradan düzeltirse (TASARIM.md §4, B2) anlık görüntü yeni indirmeyle eskisi arasındaki farkı nasıl gösterecek? Fark raporu adaptörün işi mi?

18-031. Ham yanıtın kendisi (JSON metni) diske yazılacak mı, yoksa yalnız ayrıştırılmış tablo mu? Kaynak değişirse eski yanıtı yeniden ayrıştırmak gerekebilir; ham yanıtı saklamamak bunu engeller.

18-032. Anlık görüntü dosya biçimi parquet mi (pyarrow bağımlılığı, mevcut veri.py bunu kullanıyor)? Windows'ta pyarrow tekerlek (wheel) kurulumu Python sürümü yükselince kırılırsa Levent bunu nasıl onaracak?

18-033. Her koşunun "hangi anlık görüntüyü kullandığını yazması" (§4) için görüntü kimliği ne olacak: tarih mi, içerik özeti (hash) mi? Aynı gün iki indirme olursa hangisi geçerli?

18-034. Kısmi indirme (ör. 100 hissenin 63'ü indi, sonra ağ koptu) tutarlı bir anlık görüntü sayılır mı? Yarım kalan indirme diskte nasıl işaretlenecek ve yeniden başlatma atomik mi?

18-035. Aynı gün ikinci çalıştırmada yeniden indirme yapılmaması kuralı (mevcut veri.py, dosya tarihine bakıyor) gün içinde veri güncellenirse eski veriyi dondurur. Yeni tasarımda önbellek geçerlilik kuralı ne olacak?

18-036. Tazelik kontrolü "son çubuğun tarihi bugün değilse" diyor (§5.1). İş Yatırım günlük veriyi saat kaçta yayınlıyor sorusu açık (§8.7); adaptör 19:30'dan önce çekilirse yarım günlük çubuk (gün içi değer) dönebilir mi?

18-037. Hisse bazında hata yalıtımı: 100 hisseden biri hata verirse diğer 99 devam eder mi? Hatalı hisse listesi raporun neresinde görünecek?

18-038. Bir hisse sembolü yeniden adlandırılırsa, birleşirse ya da koddan çıkarsa (İş Yatırım `.E` ekli kodu boş döndürüyor) sembol eşleme tablosu nerede tutulacak?

18-039. Kapanmış hisseler için İş Yatırım `HisseTekil`'in veri döndürüp döndürmediği "ASYAB" dışında sınanmadı (§5.2). Adaptör bu hisselerde boş yanıtı "veri yok" mu, "hata" mı sayacak?

18-040. `GetSermayeArttirimlari` bütün kodlarıyla saklanacak (§4). Bilinmeyen yeni bir `SHT_KODU` gelirse adaptör bunu sessizce geçirecek mi, yoksa koşuyu uyarıyla mı durduracak?

18-041. Çarpan `SHHE_FIYAT_AYAR_OR` nakit temettü kayıtlarında da var mı? Temettü tarihi ex-date mi ödeme günü mü sorusu açık (§8.2); adaptör bu belirsizliği taşıyan alanı "doğrulanmadı" diye mi işaretleyecek?

18-042. Şirket olayları tablosunu İş Yatırım'dan hisse hisse çekmek yüzlerce ek istek demek. Olay tablosu ne sıklıkla yenilenecek: her gün mü, haftalık mı, yalnız yeni olay beklenirken mi?

18-043. İş Yatırım ve borsapy getirileri %0,5'ten fazla ayrışırsa (§5.1) hangi kaynak "doğru" sayılacak? Bu karar adaptör katmanında mı, doğrulama modülünde mi verilecek?

18-044. İki kaynağın takvimleri farklı (Yahoo 2994, borsapy 2946 satır; veri-kaynaklari.md §3.1). Çapraz kontrolde eksik gün farkı "fark" mı sayılır, yoksa önce kesişim mi alınır?

18-045. KAP adaptörü hangi uç noktaya dayanacak? `members/byCriteria` belgelenmemiş ve kullanım koşulları okunmamış (veri-kaynaklari.md §1.4); bu adaptör neden "kütüphane" yerine kendi kodumuzla yazılıyor?

18-046. KAP "Dönemsel Endeks Değişiklikleri" bilgisi PDF ekinde (§4). PDF ayrıştırma için hangi kütüphane kullanılacak ve tablo biçimi çeyrekler arasında değişirse ayrıştırıcı bunu nasıl fark edecek?

18-047. PDF'den çıkan tablo yanlış okunursa hata birikir (§4: "bir çeyrek kaçarsa sonrası bozulur"). Her çeyrek için sonucu bugünkü CSV'ye karşı doğrulayan bir adım adaptörün parçası mı?

18-048. KAP tek sorguda en çok 2000 kayıt döndürüyor. Sayfalama ya da tarih aralığını bölme mantığı kimde? Sınır dolduğunda adaptör "kayıt kaybı olabilir" uyarısı verecek mi?

18-049. KAP sitesi bot trafiğini engelleyebilir. Engellenirse evren inşası (§7 adım 8) bütünüyle durur; bunun yerine elle indirilmiş PDF'leri bir klasörden okumak yedek yol olarak düşünülmüş mü?

18-050. KAP adaptörü bir kez çalışıp sonucu dondurulan bir iş mi, yoksa her koşuda yenilenen bir kaynak mı? Tek seferlik ise "adaptör" katmanı gerekli mi, yoksa elle bir veri dosyası yeterli mi?

18-051. 2015–2016 için KAP kapsaması doğrulanmadı (§8.3). Bu kapsama yoksa adaptör boş döner; evren modülü buna "bilinmiyor" diye mi tepki verecek, yoksa bugünkü listeyle mi dolduracak?

18-052. EVDS API anahtarı nerede saklanacak: ortam değişkeni, `.env` dosyası, Windows Kimlik Yöneticisi (keyring) ya da kod içi? Owner teknik değil; anahtarı ilk kez kim, nasıl girecek?

18-053. `.env` dosyası kullanılacaksa `.gitignore` zaten var mı? Depo bir gün paylaşılır ya da yedeklenirse (bulut senkronizasyonu dahil) anahtar sızabilir; bunu hangi mekanizma önler?

18-054. EVDS anahtarı bir hata mesajına, günlük dosyasına ya da rapora yazılırsa ne olur? Başlıkta (`key`) gittiği için istek günlüğü açılınca sızar; günlükleme bunu maskeleyecek mi?

18-055. EVDS anahtarı iptal edilir ya da süresi dolarsa sistem ne yapacak? Anahtar yokken bile çalışması mı, yoksa durması mı gerekir (borsapy `tcmb` anahtarsız yedek yol sunuyor)?

18-056. TASARIM.md §4 faiz için "TCMB politika faizi (borsapy)" diyor; §5.6 ise "EVDS" ve "2017 sonrası TLREF" diyor. Bu iki bölüm çelişmiyor mu: EVDS anahtarı gerçekten zorunlu mu, yoksa hiç gerekmeyecek mi?

18-057. EVDS politika faizi seri kodu doğrulanamadı (veri-kaynaklari.md §6). Kod bulunamazsa adaptör hangi seriyi kullanacak ve "gecelik" ile "1 hafta repo" farkı simülatör sonuçlarını ne kadar kaydırır?

18-058. TLREF 2018-12-28'de başlıyor; 2015–2018 için gecelik repo serisi başka bir seri. İki seriyi tek bir günlük faiz serisinde birleştiren adaptör ne yapacak: sıçrama, birim farkı (yıllık/günlük) nasıl ele alınacak?

18-059. Faiz serisi toplantı günlerinde basamak olarak geliyor ve ileri doldurma gerekiyor. İleri doldurma adaptörde mi, simülatörde mi yapılacak? Veri eksikse sessizce son değer mi taşınacak?

18-060. Yahoo adaptörü "yalnız sadakat kontrolü için" tutuluyor (§7 adım 2). Bu amaç için bütün bir adaptör katmanı ve `yfinance` bağımlılığı gerekli mi, yoksa Tansu'nun rakamları tek seferlik indirilip dondurulabilir mi?

18-061. yfinance de belgelenmemiş bir Yahoo uç noktasına dayanıyor ve sık kırılıyor. Yahoo çalışmayı bırakırsa sadakat kontrolü (kabul kapısı) ne olacak: kontrol atlanır mı, yoksa sonsuza dek beklenir mi?

18-062. Sadakat kontrolü "Yahoo açılışı" gerektiriyor (§5.3). Yahoo açılışı hangi tarihte, hangi yfinance sürümüyle indirildiyse o sonuç sonradan yeniden üretilebilir olmalı; indirilen veri depoda dondurulacak mı?

18-063. Yahoo verisi ve İş Yatırım verisi aynı depoda mı duracak? Yahoo anlık görüntüsünün yanlışlıkla gerçek sınamaya karışmasını engelleyen bir ayrım (adlandırma, klasör, tür) var mı?

18-064. Mevcut `tansu/veri.py` `temizle` içinde eşikle bedelsiz düzeltiyor; tasarım bunu yasaklıyor (B1). Yeni sistemde Yahoo adaptörü hiçbir düzeltme yapmayacak mı, yoksa sadakat için Yahoo'nun ham halini aynen mi koruyacak?

18-065. Sahte (fake) adaptörler testlerde nasıl üretilecek? Elle yazılmış küçük DataFrame mi, gerçek yanıtlardan kaydedilmiş sabit dosyalar (cassette) mı, yoksa vcrpy/responses gibi bir kütüphane mi?

18-066. Gerçek yanıtlardan kaydedilmiş örnekler tutulacaksa, bunlar İş Yatırım verisinin bir kopyası olarak depoya girer. Bu, kullanım koşullarına ve "kişisel kullanım" sınırına aykırı olur mu?

18-067. Sahte adaptör gerçekle aynı sözleşmeyi (aynı sütunlar, aynı hata türleri) sağladığı nasıl kanıtlanacak? Sahte, gerçekten ayrışırsa testler yeşil, canlı sistem kırmızı olur.

18-068. Gerçek ağa çıkan bir "canlı duman testi" olacak mı? Olacaksa ne sıklıkla, kim çalıştıracak ve başarısızlığı CI olmayan tek kişilik Windows makinede nasıl görünür olacak?

18-069. Mevcut testler (tests/test_nabiz_veri.py) yalnız `temizle` ve `nabiz`'i sınıyor; ağ hata durumlarını (zaman aşımı, 429, bozuk JSON, kesik yanıt) sınayan test hiç yok. Bunlar hangi düzeyde sınanacak: adaptör birim testi mi, uçtan uca mı?

18-070. Ağ hatası enjekte etmek için sahte HTTP taşıyıcısı (httpx.MockTransport, responses, pytest-httpserver) mi kullanılacak? requests seçilirse bu araç zinciri hangisi olur ve bağımlılık sayısı kaç artar?

18-071. Bir kaynak tamamen kaybolursa (İş Yatırım uç noktasını kapatırsa) yedek ne? Tasarımda tek birincil fiyat kaynağı var; borsapy (temettüsüz, TradingView) tek başına birincil kaynak olarak yeterli mi, yoksa sınama yöntemi çöker mi?

18-072. Kaynak kaybolursa geçmiş anlık görüntüler yeterli mi? Yeni gün verisi gelmediğinde sistem "sınama sürer, canlı kart durur" modunda mı kalacak? Bu davranış tasarımda yazılı değil.

18-073. Kaynak değişirse (ör. İş Yatırım fiyatları artık farklı biçimde düzeltirse) eski anlık görüntülerle yeni veri aynı seride birleştirilemez. Bu "seri kırılması" sınama tarihçesini ve deneme günlüğünü (§5.11) nasıl etkiler?

18-074. Adaptör arayüzü (sözleşme) neye benzeyecek: tek fonksiyon mu (`fiyat(sembol, baslangic, bitis)`), Protocol/ABC sınıfı mı? Tek uygulamalı bir arayüz "gereksiz soyutlama" olmaz mı; ikinci kaynak (borsapy) zaten var diye mi gerekli?

18-075. Adaptörün döndürdüğü tablo biçimi ham kaynak adlarını (`HG_KAPANIS`) mı, projenin kendi adlarını mı taşıyacak? Ad çevirisi nerede yapılacak ve GLOSSARY.md bu adları kapsıyor mu?

18-076. Türkçe karakterler: İş Yatırım ve KAP yanıtlarında İ/ı, ş, ğ içeren hisse adları ve sektör adları gelir. Kodlama (UTF-8, Windows cp1254) ve büyük/küçük harf eşleştirmesi (`"i".upper()` Türkçe'de sorun çıkarır) adaptörde nasıl ele alınacak?

18-077. Konsol ve dosya kodlaması Windows 11'de varsayılan olarak cp1252/cp1254 olabilir. Rapor ve günlük dosyaları UTF-8 olarak yazılacak mı, `PYTHONUTF8` ayarlanacak mı? Bunu owner bilmek zorunda mı?

18-078. Windows Görev Zamanlayıcı ile 19:30 koşusu (§6.1) bilgisayar kapalıysa, uykudaysa ya da ağsızsa ne yapacak? Kaçırılan günün verisi sonradan nasıl tamamlanacak (geri doldurma)?

18-079. Proxy, kurumsal güvenlik duvarı ya da antivirüs TLS denetimi ev PC'sinde sertifika hatası üretirse (özellikle WebSocket) adaptör `verify=False` önerecek mi? Hata mesajı owner'a anlaşılır olacak mı?

18-080. Windows'ta Python ile çalışan WebSocket (borsapy → TradingView) arka plan iş parçacığı ya da asyncio ile kurulur. Zamanlanmış görevde başsız (headless) çalıştırmada bu takılırsa süreç sonsuza dek asılı kalabilir; bir üst zaman sınırı var mı?

18-081. Adaptör hataları owner'a nasıl iletilecek? "ConnectionError" yığın izi mi, yoksa "İş Yatırım'a ulaşılamadı, bugün kart üretilmedi" gibi Türkçe tek cümle mi? Bu çeviri katmanı kimde?

18-082. Hata türleri sınıflandırması var mı: geçici (yeniden denenir), kalıcı (kaynak değişti), politika (engellendik)? Üç tür için sistem davranışı ayrı yazılmalı; şu an tek bir "sorun varsa kart üretilmez" cümlesi var (§6.1).

18-083. Günlük (log) için hangi kütüphane kullanılacak: stdlib `logging`, loguru ya da düz `print`? Günlük dosyası ne kadar süre saklanacak ve disk dolarsa ne olacak?

18-084. Her ağ çağrısının günlüğe yazılması (URL, durum kodu, süre, bayt) zorunlu mu? Kaynak davranışının zaman içinde değiştiğini (yavaşlama, boyut düşüşü) fark etmenin tek yolu bu veri olabilir.

18-085. Önbellek: ham yanıt için ayrı bir HTTP önbelleği (requests-cache, hishel) mi kullanılacak, yoksa anlık görüntü deposu zaten önbellek görevi görüyor mu? İki katman aynı veriyi iki kez saklamaz mı?

18-086. HTTP önbelleği kullanılırsa eski yanıt "taze" sanılıp Levent'in 19:30 kartı eski veriyle üretilebilir. Önbellek geçerlilik süresi ile tazelik kontrolü (§5.1, m6) arasındaki çakışma nasıl çözülecek?

18-087. Eşzamanlılık: tek kişilik Windows PC'de hisseleri paralel mi (thread, asyncio) yoksa sırayla mı çekeceğiz? Paralellik hız sınırı riskini artırır; sıralı çekim ilk indirmeyi saatlere uzatır. Hedef süre nedir?

18-088. İlk indirme saatler sürerse yarıda kesilebilir (uyku modu, güncelleme yeniden başlatması). Devam edebilir (resumable) indirme tasarımda var mı, yoksa her kesintide baştan mı başlanacak?

18-089. Adaptörlerin bağımlılıkları (pandas-ta-classic, statsmodels, quantstats, borsapy, pyarrow, ağ kütüphaneleri) toplamda ağır bir kurulum. Owner teknik değil; tek komutla kurulum ve Python sürümü sabitleme (uv, pip, requirements kilidi) nasıl sağlanacak?

18-090. Bağımlılık sürümleri kilitlenmezse borsapy ya da pandas bir güncellemede ayrıştırmayı bozar. Kilit dosyası (uv.lock, requirements.txt hash) kullanılacak mı ve güncelleme kararını kim, ne zaman verecek?

18-091. Güvenlik: kaynaktan gelen JSON/HTML güvenilmeyen girdidir. Beklenmedik büyük yanıt, sıkıştırma bombası ya da `eval` benzeri kullanım (borsapy iç kodu) riski için yanıt boyut sınırı ve ayrıştırıcı kısıtı düşünülmüş mü?

18-092. Tedarik zinciri riski: borsapy, isyatirimhisse gibi küçük paketler tek bakımcılı. Bir paket ele geçirilir ya da yayından kalkarsa (PyPI'den silinirse) nasıl önlem alınacak: sürüm kilidi, yerel tekerlek kopyası, kaynak kodu içeri alma (vendoring)?

18-093. Yasal ve etik çerçeve: İş Yatırım, TradingView, KAP ve TCMB sayfalarından otomatik veri çekmenin kullanım koşullarına uygunluğu açık soru (§8.1). Bu koşullar okunmadan sistem "çalışır" ilan edilecek mi, ve okunduğunda sonuç "yasak" çıkarsa kaynak planı ne olur?

18-094. Veri lisansı: İş Yatırım verisi türetilmiş rapor ve CSV olarak dosya paylaşılırsa (arkadaş, forum, Telegram) redistribution sorunu doğar. Tasarım "kişisel kullanım" diyor; bu sınırı raporların kendisi hatırlatacak mı?

18-095. Uç noktalar belgesiz ve her an değişebilir. Değişikliği ilk kim fark edecek: otomatik bir bütünlük testi mi, yoksa Levent'in akşam raporunda tuhaf bir sayı görmesi mi? Tespit gecikmesinin kabul edilebilir üst sınırı kaç gündür?

18-096. Kaynak sessizce bozuk veri döndürürse (ör. bir gün için AOF sıfır, hacim sıfır) bu hata mı, "işlem yok" mu? Adaptör katmanındaki "geçersiz satır" tanımı ile veri deposundaki karantina tanımı (§5.1) nerede ayrışıyor?

18-097. Ağ adaptörleri saf (yan etkisiz) mi olacak, yoksa kendi önbelleğini ve diske yazmayı da yapacak mı? Veri deposu modülü ile adaptör arasındaki sınır net değilse (mevcut `veri.py` ikisini birden yapıyor) sahte adaptörle test etmek zorlaşır.

18-098. Zaman damgası ve tarih: İş Yatırım "bugün" verisini gün içinde canlı döndürürse, adaptör bunu kapanmış çubuktan nasıl ayıracak? Seans saatleri ve tatil takvimi (§4 Takvim modülü) bu karara girdi sağlıyor mu?

18-099. Sürüm uyumu ve ileriye dönük bakım: Owner tek kişilik, teknik değil. Kaynak bozulduğunda onarımı kim yapacak (Claude oturumu mu, owner mu)? Adaptör kodu, bir yapay zekâ oturumunun 20 satırda onarabileceği kadar küçük ve yalıtılmış tutulacak mı?

18-100. Hangi kaynaklar "birincil", hangileri "çapraz kontrol", hangileri "yalnız sadakat" ve hangileri "tek seferlik" olarak sınıflandırılacak? Bu sınıflamaya göre her kaynak için ayrı bir "kaybolursa ne olur" cümlesi kodlamadan önce docs/ içinde yazılacak mı?
