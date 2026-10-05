# Sorular 13: Veri depolama

13-001. TASARIM.md §4 "Veri deposu" satırı "tarihli, değişmez anlık görüntü" diyor. "Anlık görüntü" tam olarak nedir: bütün evrenin her indirmedeki tam kopyası mı, yoksa yalnız o gün eklenen satırlar mı?

13-002. Anlık görüntü hisse başına bir dosya mı, gün başına bir klasör mü, yoksa tek bir büyük dosya mı olacak? Her seçenekte "bu koşu hangi anlık görüntüyü kullandı" sorusu nasıl tek bir kimlikle cevaplanır?

13-003. Mevcut `tansu/veri.py` her sembol için `veri/<SEMBOL>.parquet` yazıp aynı dosyanın üstüne yazıyor. Değişmezlik ilkesi (B2) ile bu davranış arasındaki geçiş nasıl olacak, eski dosyalar ne olacak?

13-004. Parquet, DuckDB, SQLite ve CSV arasında seçim hangi ölçüte göre yapılacak? Veri 12 MB iken (`veri/` klasörü) bu seçim neden önemli, önemli değilse neden dört seçenek tartışılıyor?

13-005. TASARIM.md §3 DuckDB'yi "gereksiz katman" diye kapsam dışı bırakıyor. Anlık görüntü sorgularının (örn. "bu tarihte, bu sembolün ham fiyatı") parquet dosyaları üzerinde pandas ile yapılması yeterli mi, yeterliliği neyle ölçülecek?

13-006. Değişmezlik nasıl zorlanacak: dosya salt okunur yapılacak mı, içerik hash'i mi kaydedilecek, yoksa yalnız bir kural olarak mı yazılacak? Yanlışlıkla üstüne yazılırsa kim fark eder?

13-007. Anlık görüntü kimliği tarih mi (`20261005`), içerik hash'i mi, yoksa ikisi mi? Aynı gün iki kez indirme yapılırsa (manuel yenileme) kimlik çakışması nasıl çözülür?

13-008. Kaynaklar "geçmişi sonradan değiştirebilir" (§4). Yeni indirmenin eski anlık görüntüyle farkı otomatik raporlanacak mı? Fark çıkarsa hangi eşik uyarı, hangisi hata sayılır?

13-009. İş Yatırım `HisseTekil` ham (`HG_*`) ve düzeltilmiş (`HGDG_*`) seriyi ayrı veriyor. İkisi aynı anlık görüntüde iki ayrı tablo olarak mı saklanacak? Düzeltilmiş seriyi saklamak §5.1'de yalnız karşılaştırma için gerekiyor; her gün saklamaya değer mi?

13-010. Borsapy (çapraz kontrol kaynağı) verisi de anlık görüntüye giriyor mu? Girmezse §5.1'deki "bütün hisse × gün karşılaştırması" sonradan yeniden üretilebilir mi?

13-011. Tek bir koşuda kaç kaynak kullanılıyor (İş Yatırım fiyat, şirket olayları, borsapy, EVDS faiz, KAP, Yahoo sadakat verisi)? Her birinin anlık görüntüsü ayrı mı, tek bir "veri sürümü" altında mı toplanacak?

13-012. Sadakat kontrolü Yahoo verisi kullanıyor (§7 madde 2), gerçek sınama İş Yatırım. İki kaynağın anlık görüntüleri aynı depoda aynı şemayla mı tutulacak, yoksa karışmaları şemayla nasıl engellenecek?

13-013. Sütun şeması sabitlenecek mi (kapanış, yüksek, düşük, AOF, hacim, piyasa değeri)? Kaynak ileride sütun eklerse ya da adını değiştirirse eski anlık görüntüler nasıl okunur?

13-014. `HACIM` biriminin (lot mu TL mi) çözümü §5.1'de "ilk veri işinde" bırakılmış. Birim kararı anlık görüntüde mi, okuma katmanında mı uygulanacak? Birim hatası bulunursa eski anlık görüntüler yeniden yazılacak mı?

13-015. Tarih sütunu saat dilimi içeren zaman damgası mı, saf tarih mi? Windows'ta yerel saat, UTC ve İstanbul saati karışması günlük çubuk tarihini bir gün kaydırabilir mi?

13-016. Fiyatlar float64 mu, ondalık mı saklanacak? BIST fiyat adımı (0,01) ve düzeltme katsayılarıyla çarpma birikimi, hash'lerin ve tekrarlanabilirliğin bozulmasına yol açar mı?

13-017. Şirket olayları tablosu (bedelsiz, bölünme, bedelli, temettü) hangi biçimde saklanacak: ayrı bir parquet, ayrı tablo, ya da fiyat dosyasının içinde sütun? Aynı depo mu, ayrı depo mu?

13-018. `GetSermayeArttirimlari` yanıtı ham haliyle (JSON/HTML) mi arşivlenecek, yoksa yalnız ayrıştırılmış tablo mu? Ayrıştırıcı hatası sonradan bulunursa ham yanıt olmadan düzeltme yapılabilir mi?

13-019. Şirket olayı tablosunun satırı değişebilir mi (kaynak eski bir oranı düzeltirse)? Bu tablo da tarihli ve değişmez mi, yoksa fiyat anlık görüntüsünden bağımsız olarak üstüne mi yazılacak?

13-020. Fiyat anlık görüntüsü ile şirket olayı tablosu farklı günlerde alınırsa, düzeltme katsayısı (`SHHE_FIYAT_AYAR_OR`) tutarsız bir çift üretir. İkisinin aynı sürüme bağlı olduğu nasıl garanti edilir?

13-021. Temettü kayıtlarındaki tarih hak kullanım günü mü ödeme günü mü (§8.2)? Cevap yanlış çıkarsa saklanan tablo yeniden mi indirilir, yoksa yorum katmanında mı düzeltilir? Bu belirsizlik şemaya nasıl yansıtılır?

13-022. Düzeltme katsayıları saklanacak mı, her koşuda ham fiyat ve olay tablosundan yeniden mi hesaplanacak? Hesaplanmış düzeltilmiş fiyat önbelleğe alınırsa önbelleğin ne zaman geçersiz olduğu nasıl bilinir?

13-023. Karantina listesi (§5.1) veri deposunun parçası mı, ayrı bir çıktı mı? Karantina kararı hangi anlık görüntüden türetildiğini nasıl taşır?

13-024. Kapanmış semboller (ASYAB gibi) için depoda satır tutuluyor mu? Bir sembol yeniden adlandırılır ya da birleşirse anahtar nedir: kod mu, sabit bir kimlik mi?

13-025. Evren (`PD` ile nokta-zamanlı en büyük 100, §5.2) her ay başı için ayrı tablo olarak saklanacak mı? Piyasa değeri sütunu anlık görüntüyle birlikte donuyorsa, evren eski anlık görüntüyle yeniden üretilebilir mi?

13-026. Günlük çalışma "veri güncellenir" diyor (§6.1). Güncelleme artımlı (yalnız yeni günler) mi, tam yeniden indirme mi? Kaynak geçmişi değiştirebiliyorsa artımlı indirme eski satırlardaki değişikliği nasıl yakalar?

13-027. Tam yeniden indirme 100 sembol için kaç istek, ne kadar süre? Kullanım koşulları ve hız sınırı bilinmiyorken (§8.1) her akşam tam indirme kabul edilebilir mi?

13-028. Artımlı güncellemede son N günün her seferinde yeniden indirilmesi (örtüşme penceresi) tasarlanacak mı? N kaç olacak ve bu seçim hangi veriye dayanıyor?

13-029. İndirme sırasında 100 sembolün 40'ı geldi, ağ koptu. Yarım indirme yeni anlık görüntü sayılır mı, atılır mı, devam mı edilir? Kısmi anlık görüntüyle koşan sınama nasıl engellenir?

13-030. Bir sembol için kaynak boş ya da hatalı veri döndürürse (örn. bir günlük hacim sıfır) bu satır depoya yazılır mı, atılır mı, işaretlenir mi? Mevcut `temizle()` satırları sessizce siliyor; yeni sistemde silme kabul edilir mi?

13-031. İş Yatırım günlük veriyi ne zaman yayınlıyor bilinmiyor (§8.7). 19:30'da indirilen bugünkü çubuk kısmi olabilir. Kısmi çubuk anlık görüntüye girerse ertesi gün düzelen satır "değişmez" ilkesini nasıl bozmaz?

13-032. "Bugünkü veri" kontrolü (§5.1, m6) çubuk tarihine bakıyor. Bu kontrol depolama katmanının işi mi, ayrı bir doğrulama modülünün mü? Doğrulama başarısızsa anlık görüntü yine de yazılır mı?

13-033. Anlık görüntü boyutu tahmini: yaklaşık 100 sembol, 11 yıl, yaklaşık 2.800 işlem günü, 7 sütun için ham boyut ne kadar? Her gün tam kopya tutulursa 1 yılda, 5 yılda kaç GB olur?

13-034. Eski anlık görüntüler ne kadar süre saklanacak? Deneme günlüğü (§5.11) bir anlık görüntüye atıf yaptığı sürece o anlık görüntü silinemez mi? Bu bağımlılık nasıl izlenir?

13-035. Silme politikası otomatik mi manuel mi? Non-teknik bir sahip için "hangi anlık görüntüler silinebilir" kararı nasıl sade bir hale getirilir?

13-036. Anlık görüntüler farklılaşma (delta) olarak mı saklanacak, yoksa her biri tam mı? Delta depolama bir bozuk halkanın sonraki bütün anlık görüntüleri okunmaz yapması riskini taşır; bu risk kabul edilir mi?

13-037. Parquet sıkıştırma kodeği (snappy, zstd) ve satır grubu boyutu bir karar mı, varsayılan mı? Farklı pyarrow sürümleri aynı veriden farklı bayt üretirse dosya hash'i anlık görüntü kimliği olarak kullanılabilir mi?

13-038. Hangi dosyalar git'e girecek? Mevcut `.gitignore` `veri/`yi dışarıda bırakıyor; `rapor/islemler-20261005.parquet` ise repoda. Hangisi doğru kural, bir kural yazılı mı?

13-039. Anlık görüntüler git'te yoksa kaybolurlarsa "kural kaydı" (§5.8) ve deneme günlüğündeki hash'ler artık yeniden üretilemez. Bu kabul edilen bir risk mi, yoksa ikinci bir yedek şart mı?

13-040. Küçük ama kritik tablolar (şirket olayları, kural kaydı, deneme günlüğü, karantina listesi) git'te tutulmalı mı? Binlerce satırlık bir CSV ya da parquet diff'i okunabilir mi?

13-041. Büyük dosyalar için Git LFS, DVC ya da hiçbiri mi? "Güvenilir kütüphane, asgari altyapı" ilkesi (görev tanımı) veri sürümleme aracını gerektirir mi, gerektirmezse alternatif nedir?

13-042. AGENTS.md'ye göre uzak repo yok (`.scratch/` yerel). Yedek olarak yalnız yerel disk mi kullanılacak? Disk arızası ya da yanlış silme durumunda 11 yıllık veri ve deneme günlüğü nasıl geri gelir?

13-043. Yedek ne sıklıkla, nereye, kim tarafından alınacak? Teknik olmayan sahip bunu nasıl fark edip kontrol edecek?

13-044. Proje klasörü Masaüstü'nde. OneDrive masaüstünü senkronize ediyorsa parquet dosyalarının yazılırken senkronize edilmesi bozuk ya da kilitli dosya yaratabilir mi? Bu risk değerlendirildi mi?

13-045. Windows'ta virüs koruması ya da arama dizinleyicisi bir dosyayı açıkken yazma/yeniden adlandırma hatası verebilir. Atomik yazma (geçici dosyaya yaz, sonra yeniden adlandır) Windows'ta güvenilir mi?

13-046. Yol uzunluğu sınırı ve Türkçe karakterli klasör adları (örn. "Masaüstü" varsa) hash dosya adları ve derin klasör yapısı ile sorun çıkarır mı? Dosya düzeni bu kısıtlara göre doğrulandı mı?

13-047. Run günlüğünde (deneme günlüğü, §5.11) veri sürümü hangi alanlarla yazılacak: anlık görüntü kimliği, dosya hash'i, indirme zamanı, sembol sayısı, satır sayısı? Asgari alan seti nedir?

13-048. Deneme günlüğü kendisi nerede, hangi biçimde (CSV, JSONL, SQLite) tutulacak? Birden çok koşu aynı anda yazarsa satır bozulması nasıl önlenir?

13-049. Deneme günlüğü yalnız eklemeli (append-only) mi? Hatalı bir satır sonradan düzeltilebilir mi, düzeltilemiyorsa düzeltme nasıl işaretlenir?

13-050. Kod hash'i ile veri hash'i aynı kayıtta nasıl birleşir? Yalnız veri değişir (kaynak geçmişi düzeltir) ve kod aynı kalırsa yeni koşu "yeni deneme" sayılır mı (§5.11 Holm düzeltmesi etkilenir)?

13-051. Aynı kural, aynı kod, aynı veriyle ikinci kez koşulursa (tekrar üretme testi) deneme günlüğüne yeni satır mı eklenir? Holm düzeltmesinde bu tekrarlar deneme sayısını şişirir mi?

13-052. Kural kaydı (§5.8) "sadakat kontrolü bitince, ilk getiri koşusundan önce" yazılıyor. Kayıt, veri anlık görüntüsüne de bağlı mı? Kayıttan sonra kaynak geçmişi değişirse "ayrılmış dönem" tanımı bozulur mu?

13-053. Kâğıt üstü canlı dönem (§5.8) gün gün veri ekler. Canlı dönemde alınan bir günlük çubuk sonradan kaynakta değişirse, canlı kayıt (o gün görülen) ile sonraki sürüm arasındaki fark hangisine göre değerlendirilir?

13-054. Canlı kart listesi (CSV, §6.4) o gün hangi anlık görüntüyle üretildiğini yazacak mı? Kartların sonradan yeniden üretilebilmesi için hangi minimum bilgi gerekir?

13-055. Önbellek ve anlık görüntü aynı şey mi? `veri.py` "aynı gün ikinci kez indirilmez" diye önbellek kullanıyor. Yeni tasarımda önbellek (atılabilir) ile anlık görüntü (değişmez) ayrı kavramlar olarak mı tutulacak?

13-056. Önbelleğin geçerlilik kuralı bugün `mtime == bugün`. Dosya zamanı güvenilir bir ölçüt mü (dosya kopyalama, geri yükleme, saat değişikliği)? Yerine ne kullanılacak?

13-057. Parquet dosyası yarım yazılmış (bozuk) ise okuma hatası nasıl yakalanır: yazılırken sağlama toplamı mı, okurken `try/except` mi? Bozuk dosya sessizce boş sonuç döndürebilir mi?

13-058. Bozuk önbellek tespit edildiğinde sistem otomatik mi yeniden indirir, durup mu sorar? Teknik olmayan sahip hangi mesajı görecek ve ne yapacak?

13-059. Bozuk dosya bir anlık görüntünün parçasıysa (değişmez veri) yeniden indirmek aynı veriyi vermez. O anlık görüntüye bağlı sınama sonuçları geçersiz mi sayılır, yedekten mi geri yüklenir?

13-060. Elektrik kesintisi koşu sırasında olursa hangi dosyalar kısmi kalabilir (anlık görüntü, deneme günlüğü, rapor)? Başlangıçta tutarlılık kontrolü yapılacak mı?

13-061. Anlık görüntü dizini ile deneme günlüğü arasında tutarlılık nasıl doğrulanır: günlük bir hash'e atıf yapıyor ama dosya yoksa, ya da dosya var günlükte yoksa ne olur?

13-062. Günlük koşu (19:30) ile elle çalıştırılan geri test aynı anda çalışırsa ne olur? Biri anlık görüntü yazarken diğeri okuyabilir mi?

13-063. Geri test başlarken anlık görüntü kimliğini "sabitler" mi (başlangıçta çözüp sonuna kadar kullanır)? Koşu ortasında günlük güncelleme yeni anlık görüntü eklerse geri test hangisini görür?

13-064. "En son anlık görüntü" göstergesi (işaretçi dosya, sembolik bağ, en yüksek tarihli klasör) hangi mekanizmayla tutulacak? Windows'ta sembolik bağlantı yönetici hakkı gerektirebilir; alternatif nedir?

13-065. Dosya kilidi kullanılacak mı (örn. `filelock`) yoksa değişmezlik + atomik yeniden adlandırma ile kilitsiz mi çalışılacak? Güvenilir kütüphane ilkesi hangisini destekler?

13-066. Aynı gün planlı görev iki kez tetiklenirse (Windows Görev Zamanlayıcı çakışması, bilgisayar uykudan uyandı) ikinci örnek ne yapar? Tek örnek garantisi nasıl sağlanır?

13-067. PC 19:30'da kapalı ya da uykuda ise günlük koşu kaçırılır. Kaçırılan günler sonradan nasıl doldurulur (artımlı indirme boşlukları kendiliğinden kapatır mı)? Boşluk raporda görünür mü?

13-068. Planlı görev kaç gün üst üste çalışmazsa sahip bunu nasıl öğrenir? Eski veriyle kart üretmeyi engelleyen tazelik kontrolü (§6.1) depolama katmanının hangi bilgisine bakar?

13-069. DuckDB ya da SQLite seçilirse tek yazıcı kilitleri geri test ile günlük koşu arasında çakışır. Yalnız parquet kullanmak bu sorunu gerçekten ortadan kaldırır mı, yoksa deneme günlüğü yine tek yazıcı noktası mı?

13-070. İş Yatırım ve borsapy çağrıları sırasında önbellek yazılırken ikinci süreç aynı sembolü indirmeye başlarsa çift indirme ve çakışan yazma olur mu? Sembol bazında kilit gerekli mi?

13-071. Geri test (§5.7) en az 1.000 rastgele tekrar koşuyor. Tekrarlar fiyatı her seferinde diskten mi okur, bellekte mi tutar? Belleğe sığmama durumu (100 sembol × 11 yıl pek küçük) bir sorun mu, değilse bu soru depolama seçimini etkiler mi?

13-072. Hisse başına dosya düzeni ile "bütün evrenin bir günü" sorgusu (evren seçimi, likidite taraması) çelişir. Hangi erişim kalıbı baskın olacak ve düzen buna göre mi seçilecek?

13-073. Piyasa değeri (`PD`) fiyatla aynı satırda geliyor. Evren seçimi için her ay başı tüm sembollerin PD'sine bakılıyor; bu için ayrı bir türetilmiş tablo mu üretilecek, yoksa her seferinde ham veriden mi hesaplanacak?

13-074. Türetilmiş veriler (göstergeler, düzeltilmiş fiyat, evren, karantina) saklanacak mı, her seferinde mi hesaplanacak? Saklanırsa hangi anlık görüntüden türediğini nasıl bilir ve geçersizlenmesi nasıl yönetilir?

13-075. Geri test sonuçları (`rapor/islemler-*.parquet`) veri deposundan ayrı bir "çıktı" katmanı mı? Çıktıların veri sürümüyle birlikte arşivlenmesi ve karşılaştırılması düşünüldü mü?

13-076. EVDS/TCMB faiz serisi, TLREF ve politika faizi geçmişi (§5.6) nasıl saklanacak? Basamak seri olduğu için ayrı küçük tablo mu, fiyatla aynı yapıda mı? Faiz kaynağı geçmişi düzeltirse bu da bir anlık görüntü mü?

13-077. KAP "Dönemsel Endeks Değişiklikleri" duyuruları (§7 madde 8) elle çıkarılacak listeler üretiyor. Elle girilen veri (2015 BIST30 listesi) hangi biçimde, kim tarafından, hangi kaynak notuyla depoya girer? Elle veri ile indirilen veri aynı güvenceyi taşır mı?

13-078. Kaynak notu ve lisans: İş Yatırım ve TradingView verisinin yerel kopyasını saklamak kullanım koşullarına uyar mı (§8.1)? Koşullar saklamayı yasaklıyorsa tasarımın hangi parçası çöker?

13-079. Sembol adı değişikliği, birleşme ve kodun yeniden kullanımı: aynı kod farklı şirketi göstermişse geçmiş fiyat zinciri karışır. Depoda şirket kimliği ile sembol ayrımı var mı?

13-080. Bölünme ya da bedelsiz sonrası eski anlık görüntülerdeki ham fiyatlar değişmiyor. Ancak düzeltilmiş hesaplar yeni olay tablosuyla farklı sonuç verir. Eski deneme günlüğü satırlarının hangi olay tablosu sürümüyle üretildiği nasıl kaydedilir?

13-081. Sürüm numarası şeması (tarih, artan sayı, hash) ile "veri sürümü" nasıl adlandırılacak ki teknik olmayan sahip raporda okuyup anlayabilsin?

13-082. Raporda (markdown) veri sürümü hangi biçimde görünecek? Sahibin "bu sonuç hangi veriyle üretildi" sorusunu tek satırla cevaplayan bir ifade var mı?

13-083. İki koşunun sonuçları farklı çıkarsa, farkın nedeninin (kod, parametre, veri) ayrıştırılması için hangi bilgi saklanıyor? Veri farkı anlık görüntüler arasındaki satır farkı olarak üretilebilir mi?

13-084. Bağımlılık sürümleri (pandas, pyarrow, pandas-ta-classic, numpy, statsmodels) sonucu etkiler. `pyproject.toml` şu an yalnız pytest ayarı içeriyor ve bağımlılık bildirmiyor. Kilit dosyası (lockfile) veri sürümleme ile birlikte kaydedilecek mi?

13-085. Parquet dosyaları pyarrow sürümleri arasında okunabilir kalır mı? 5 yıl sonra bugünün anlık görüntüleri yeni sürümlerle açılabilmesi için bir biçim geçiş planı gerekli mi?

13-086. CSV, sahibin Excel'de açıp okuması için cazip. Ondalık ayracı Türkçe yerelde virgül, liste ayracı noktalı virgül. Kart CSV'si (§6) ve olası veri dışa aktarımı hangi kodlama ve ayraçla yazılacak?

13-087. Mevcut `rapor/islemler-20261005.parquet` ve `veri/*.parquet` Yahoo ön denemesinden. §1 bu rakamları kanıt saymıyor. Bu dosyalar silinecek mi, arşivlenecek mi, yoksa yanlışlıkla yeni sistemde okunmaması için nasıl ayrılacak?

13-088. Tests klasöründeki testler ağ erişimi olmadan çalışabilecek mi? Test için gerçek anlık görüntülerin küçük bir örneği (fixture) git'e girecek mi, girerse hangi hisse ve tarih aralığı?

13-089. Geliştirme sırasında deney verisi (sentetik fiyat) ile gerçek anlık görüntüler aynı klasörde karışabilir. Test ve gerçek veri depoları ayrı kök dizinlerde mi olacak ve bir yanlışlıkla karışmayı kim engeller?

13-090. Depo kök yolu (`veri/`) koda gömülü (`Path(__file__).parent.parent / "veri"`). Verinin proje dışında (örn. başka bir disk) durması isteniyorsa yapılandırma nereden gelecek ve varsayılan ne?

13-091. Disk dolarsa indirme ve yazma ne yapar? Yarım yazılmış anlık görüntü varken disk dolu hatası sessiz kalırsa sonraki koşu bozuk veriyle devam eder mi?

13-092. Okuma performansı: 100 sembolün tek tek parquet dosyası ile tek bir birleşik dosya arasında, günlük kullanımda ve 1.000 tekrarlı rastgele sınamada hangi fark ölçüldü? Karar ölçüme mi, tahmine mi dayanıyor?

13-093. Sahip, veriye bakmak isterse (örn. "AKBNK'nın geçen salı kapanışı neydi") bunu nasıl yapacak? Teknik olmayan biri için parquet açan bir araç, kısa bir komut ya da kart ekranı var mı?

13-094. Streamlit "Kanıt" ekranı (§3) raporu ve piyasa durumunu okuyor. Ekran, koşu devam ederken yazılan dosyayı okuyabilir mi? Yarım yazılmış rapor ekranda hatalı sonuç gösterebilir mi?

13-095. Veri deposuna erişen kod tek bir modülde mi toplanacak (§4 "küçük yüz"), yoksa diğer modüller doğrudan dosya yoluna erişecek mi? Depolama biçimi değişirse kaç modül etkilenir?

13-096. Veri deposu modülünün dışarıya açtığı yüz ne olacak: `fiyat(sembol, anlik_goruntu)`, `olaylar(sembol)`, `evren(tarih)`? Her çağrının hangi anlık görüntüyü kullandığı çağıran tarafından zorunlu olarak mı verilir, yoksa varsayılan "en yeni" mi?

13-097. Varsayılan "en yeni" anlık görüntü, geçmiş bir sonucu yeniden üretmeye çalışan kişiyi sessizce yeni veriyle çalıştırır. Anlık görüntü kimliği açıkça verilmediğinde sistem hata mı verir, uyarır mı?

13-098. Kullanıcının hiç bakmadığı bir anlık görüntü gitmeden önce hangi koşullarda "bu sürüm kayıt altında kullanıldı" diye korunacak? Kullanılan her anlık görüntünün (rapora girmiş olanlar) kalıcı olarak ayrılması gerekir mi?

13-099. Veri kalitesi sonuçları (karantina, borsapy farkı, eksik gün) depolama katmanında mı kaydedilir? Kalite raporunun kendisi de değişmez bir artefakt olarak anlık görüntüye eşlenecek mi?

13-100. Bu depolama kararlarının hepsi ilk hafta sonunda yanlış çıkarsa (örn. parquet yetmedi, hisse başına dosya yavaş) geri dönüş maliyeti nedir? Depolama biçimini değiştirirken eski deneme günlüğü hash'lerinin geçerliliği nasıl korunur?
