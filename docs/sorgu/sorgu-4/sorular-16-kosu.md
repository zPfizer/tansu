# Sorular 16: Koşu, zamanlama, günlük

## A. Komut satırı biçimi

16-001. TASARIM §6 "19:30: veri güncellenir" diyor ama komutun adı, alt komutları ve girdileri hiçbir yerde yok. Günlük koşu, sınama, rapor, sadakat kontrolü ve kural kaydı tek komutun alt komutları mı, ayrı giriş noktaları mı olacak?

16-002. Mevcut prototip `python -m tansu.rapor` ile çalışıyor (rapor.py). Yeni sistemde `-m` biçimi mi, kurulu bir `tansu` komutu mu, yoksa Task Scheduler'ın doğrudan çağıracağı bir `.bat` mı kullanılacak? Hangisinin Levent'in elinde en az şeyle çalışacağı nasıl gösterilecek?

16-003. Komut satırı kütüphanesi olarak argparse, typer ve click arasındaki seçim, "güvenilir kütüphane, asgari altyapı" ölçütüne göre neye dayanarak yapılacak? Bağımlılık eklemenin getirdiği Windows uyumluluk riski kim tarafından ölçülecek?

16-004. pyproject.toml'da şu an yalnız pytest ayarı var; bağımlılık, `[project.scripts]` ya da paket bilgisi yok. Giriş noktası nerede tanımlanacak ve `.venv` içindeki kurulum Levent'in makinesinde tek adımla nasıl yeniden kurulacak?

16-005. Günlük koşu ile sınama koşusu aynı çalıştırılabilir dosyayı mı paylaşacak? Paylaşırsa Levent yanlışlıkla akşam görevi yerine 1.000 tekrarlı K1 sınamasını başlatabilir; bunu önleyen şey nedir?

16-006. Komutlar Levent'in elle yazacağı şeyler mi, yoksa yalnız zamanlayıcının çağıracağı şeyler mi? "Teknik olmayan" bir kullanıcı için hangi komutlar belgelenecek ve kaç tane olması kabul edilebilir?

16-007. Günlük koşu tek adım (hepsini yap) mı, yoksa 6. bölümdeki beş adım ayrı alt komutlar mı olacak? Kısmen başarısız bir koşuda tek adımı yeniden çalıştırma yolu var mı?

16-008. Komut satırı bayrakları (tarih, kuru koşu, zorla, ayrıntılı) için hangi kümeye karar verildi? "Yapılandırılabilirlik istenmedikçe eklenmez" ilkesiyle `--tarih` gibi bir geçersiz kılma ne zaman gerekli sayılacak?

16-009. Yapılandırma (veri klasörü, rapor klasörü, saat, hisse listesi) kodda sabit mi, bir TOML dosyasında mı, ortam değişkeninde mi tutulacak? Mevcut veri.py ve rapor.py `KLASOR` yolunu dosya konumundan türetiyor; bu yaklaşım zamanlayıcı altında ve kurulum taşınınca nasıl davranır?

16-010. Komutun çıktısı insan için ekrana mı yazılacak, yalnız günlük dosyasına mı? Levent konsolu hiç görmeyecekse `print` çağrıları (rapor.py'deki `print(yol)` gibi) ne olacak?

## B. Windows Görev Zamanlayıcı

16-011. TASARIM §6 "19:30" der; §8.7 "İş Yatırım günlük veriyi saat kaçta yayınlıyor?" sorusu açıktır. 19:30 değeri ölçülmeden seçildiyse görevin saati hangi kanıtla sabitlenecek ve sonradan nasıl değiştirilecek?

16-012. Görev kullanıcı oturumu açıkken mi, oturum kapalıyken mi çalışacak? "Kullanıcı oturum açmış olsun ya da olmasın çalıştır" seçeneği parola saklama gerektirir; Levent bunu kurabilir mi?

16-013. Bilgisayar 19:30'da uyku ya da hazırda bekletme modundaysa görev ne yapacak? "Görevi çalıştırmak için bilgisayarı uyandır" seçeneği açılacak mı ve dizüstü pil modunda bu izin verilir mi?

16-014. Görev tanımı nerede tutulacak: Görev Zamanlayıcı arayüzünde elle mi, repoda bir XML dosyasında mı? Levent makineyi yeniden kurarsa ya da görevi yanlışlıkla silerse görev nasıl geri gelecek?

16-015. Görev hangi Python'u çağıracak: `.venv\Scripts\python.exe` mutlak yolu mu, `py` başlatıcısı mı? `.venv` silinir ya da taşınırsa görevin sessizce ölmediğini kim fark edecek?

16-016. Görevin çalışma dizini (Başlangıç yeri) ne olacak? veri.py ve rapor.py yolları dosya konumundan türetildiği için çalışıyor, ama yapılandırma ve günlük yolları göreli olursa zamanlayıcı altında System32'de çalışma riski nasıl kapanacak?

16-017. Görev "önceki örnek hâlâ çalışıyorsa" ne yapacak: yeni örneği başlatma, mevcut olanı durdurma, paralel çalıştırma? Bu ayar uygulama içi kilitle nasıl çakışmayacak?

16-018. Görev için zaman aşımı ("görev şu süreden uzun çalışırsa durdur", varsayılan 72 saat) belirlenecek mi? Takılı kalan bir indirme sonraki akşamın koşusunu engelleyebilir; azami süre kaç dakika olmalı ve neye göre?

16-019. Görev son sonucunu Görev Zamanlayıcı geçmişine yazar, ama "geçmiş" varsayılan olarak kapalı gelir. Kapalıysa görevin hiç çalışıp çalışmadığı nasıl kanıtlanacak?

16-020. Görevin çalıştığı kullanıcı hesabı ile Levent'in etkileşimli hesabı aynı mı? Farklıysa veri/rapor klasörlerinin erişim izinleri ve Python önbellek yolları (borsapy, pandas-ta önbelleği) farklı çıkabilir; bu nasıl kontrol edilecek?

16-021. Windows güncellemesi gece yeniden başlatma yapıyorsa 19:30 görevi etkilenir mi? Etkinse bu durum günlükte nasıl ayırt edilecek?

16-022. Sınama koşusu (K1, en az 1.000 tekrar) aynı makinede saatlerce sürebilir. Bu koşu çalışırken 19:30 görevi başlarsa CPU, bellek ve disk için ne öncelik verilecek?

## C. Kaçırılan koşular ve telafi

16-023. Bilgisayar 19:30'da kapalıysa ertesi gün açılışta ne olacak? "Görev kaçırılırsa en kısa sürede çalıştır" ayarı açılacak mı, ve açılırsa koşu saat 09:00'da çalıştığında "bugünkü veri" sayılan şey ne olacak?

16-024. TASARIM §5.1 "son çubuğun tarihi bugün değilse o gün kart üretilmez" der. Kaçırılan bir günün koşusu sonradan yapılırsa o gün için kart üretilecek mi, yoksa kaçırılan gün kalıcı olarak "kart yok" mu sayılacak?

16-025. Telafi koşusu hangi günleri geriye dönük dolduracak: yalnız son kaçırılan günü mü, son N işlem gününü mü? Veri deposu anlık görüntüsü ve açık kartların güncellenmesi (§6.5) kaçırılan günler için sırayla mı işlenecek?

16-026. Açık kartların Adım fonksiyonuyla güncellenmesi her gün bir mum ilerletir. İki gün kaçırılırsa Adım fonksiyonu iki mumu sırayla mı işleyecek? Aradaki günlerde stop ya da hedef değmişse kart hangi tarihle kapanacak?

16-027. "Kaçırılan koşu" nasıl tanımlanacak: günlük koşu kaydı olmayan işlem günü mü, son başarılı koşudan bu yana geçen süre mi? Bu tanım için kayıt nerede tutulacak?

16-028. Levent tatile çıkıp bilgisayarı bir hafta kapalı bırakırsa, dönüşte hangi çıktıyı görmeyi bekler? Eski kartların güncel olmadığı ekranda nasıl belirtilecek?

16-029. Kâğıt üstü canlı dönem en az 6 ay ve 30 işlem ister (§5.8). Bu dönemde kaçırılan günler döneme sayılacak mı, ve kaçırılan gün sayısı için bir üst sınır var mı ki dönem geçerliliğini yitirmesin?

16-030. Kaçırılan gün sayısı kâğıt üstü izlemede sinyal kaybı demektir. Sinyal kaçırma, ayrılmış dönem kanıtını bozan bir "veri deliği" olarak raporlanacak mı?

16-031. Telafi koşusu çalışırken veri kaynağı tarih aralığı ister mi (yalnız son çubuk mu, eksik günler mi)? Veri deposunun "tarihli, değişmez anlık görüntü" kuralı (§4) eksik günleri doldurmayı nasıl etkiler?

16-032. 19:30'dan sonra Levent manuel olarak koşuyu başlatırsa bu "telafi" mi "yeniden koşu" mu sayılacak? Raporlar iki durumu ayırt edecek mi?

16-033. Aynı akşam ikinci kez (örn. 22:00'de) çalışan bir koşu, ilk koşunun verisi eksik olduğu için gerekli olabilir: İş Yatırım verisi 19:30'da henüz yayınlanmamışsa (§8.7) otomatik ikinci deneme var mı, varsa kaçta?

16-034. Telafi mantığı (kaçırılan günleri bulma) kendi kodu mu olacak, yoksa Görev Zamanlayıcı ayarlarına mı bırakılacak? "Kendi zamanlayıcı yazma" yasağı ile "kaçırılanı yakalama" ihtiyacı nasıl bağdaşacak?

## D. Tekrar koşulabilirlik (idempotans)

16-035. Aynı gün için günlük koşu iki kez çalıştırılırsa kart CSV'si üzerine mi yazılacak, yenisi mi eklenecek, yoksa ikinci koşu hiçbir şey yapmadan mı çıkacak? Bu davranış nerede yazılı olacak?

16-036. Günlük koşu kart listesini CSV'ye yazarken yazma ortasında elektrik kesilirse dosya yarım kalabilir. Yazma "geçici dosyaya yaz, sonra yeniden adlandır" biçiminde mi olacak, yoksa bu ne zaman gerekli sayılır?

16-037. §4'te veri deposu "değişmez anlık görüntü" tutar. Aynı gün iki kez çalışmak iki anlık görüntü yaratır mı? Hangisi o günün resmî kaydıdır ve deneme günlüğünde (§5.11) hangisi anılır?

16-038. Mevcut veri.py "aynı gün ikinci kez indirilmez" kuralını dosya değişiklik tarihine göre uyguluyor. Yeni sistemde "bugün indirildi" bilgisi neye dayanacak: dosya zamanı mı, kayıt tablosu mu, son çubuk tarihi mi? Dosya zamanı yanıltıcı olduğunda (kopyalama, saat farkı) ne olur?

16-039. Günlük koşu açık kartları günceller (§6.5). Aynı gün koşu iki kez çalışırsa Adım fonksiyonu aynı mumu iki kez uygulayabilir mi? Bunun olmadığını gösteren sınama ne olacak?

16-040. Raporun adı tarih içeriyor (`kanit-20261005.md`, rapor.py). Aynı gün ikinci sınama koşusu ilk raporun üzerine yazarsa deneme günlüğündeki (§5.11) önceki kayıt kanıtsız mı kalacak?

16-041. Deneme günlüğüne yazılan her koşu kaydı kalıcı ve eklemeli (append-only) mi? Aynı koşu yarıda kesilip yeniden başlarsa günlükte iki kayıt mı, bir kayıt mı olacak ve Holm düzeltmesi hangisini sayacak?

16-042. "Kuru koşu" (hiçbir şey yazmadan ne olacağını göster) gerekli mi, yoksa yeniden koşunun zararsız olması yeterli mi? Zararsızlığı hangi test kanıtlayacak?

16-043. Günlük koşuda başarısız olan bir adım (örn. kalite kontrolü) kendinden önceki adımların çıktılarını geri alacak mı? Tazelik kontrolü başarısızsa indirilen veri deposunda kalacak mı?

16-044. Kural kaydı ve hash (§5.8) "ilk getiri koşusundan önce" yazılır. Bu kayıt bir koşunun yan etkisi mi, ayrı bir komut mu? Yanlışlıkla ikinci kez çalıştırılırsa kayıt değişir mi?

## E. Koşu kilidi

16-045. Aynı anda iki koşu (örn. 19:30 görevi ve Levent'in elle başlattığı koşu) aynı parquet dosyalarına yazarsa ne olur? Kilit gerekli mi, ve gerekliyse "bu kilit olmasa neyin bozulacağı" somut olarak gösterildi mi?

16-046. Kilit için hangi mekanizma kullanılacak: kilit dosyası, `msvcrt.locking`, portalocker gibi bir kütüphane, işletim sistemi mutex'i? Hangisi Windows'ta güvenilir ve "kendi kütüphanemizi yazmama" ilkesine uyar?

16-047. Süreç çökerse ya da güç kesilirse kilit dosyası arkada kalır ("bayat kilit"). Bayat kilit nasıl anlaşılacak ve bir sonraki koşu bu yüzden hiç çalışmadan sessizce çıkarsa Levent bunu nasıl fark edecek?

16-048. Kilit kapsamı nedir: yalnız günlük koşuyu mu korur, yoksa sınama koşusu, rapor üretimi ve veri indirmeyi de kapsar mı? Uzun sınama koşusu kilidi tutarsa günlük koşu beklemeden mi çıkacak yoksa bekleyecek mi?

16-049. Kilit alınamayınca koşu hangi çıkış koduyla ve hangi günlük satırıyla bitecek? Bu durum "başarısızlık" mı, "atlandı" mı sayılacak?

16-050. Veri deposunun `veri\` altındaki parquet dosyalarını aynı anda okuyan Streamlit "Kanıt" ekranı (§3) bir koşu yazarken açılırsa yarım dosya okuyabilir. Okuyucu için koruma gerekli mi, ve neyle sağlanacak?

16-051. Kilit, birden fazla Python süreci başlatan bir iş (çok işlemli K1 sınaması) içinde ne yapar? Alt süreçler kilidi miras alacak mı?

16-052. Tek kişi, tek makine varsayımı kilit gerekliliğini ortadan kaldırıyor mu? Bu varsayım bozulursa (veri klasörü OneDrive ya da ağ sürücüsünde senkronize olursa) ne olacak?

## F. Günlük kaydı (log)

16-053. Günlük kaydı için standart `logging` modülü mü, loguru gibi bir kütüphane mi kullanılacak? "Güvenilir kütüphane" ölçütü ile "asgari altyapı" ölçütü bu seçimde çatışırsa hangisi öncelikli?

16-054. Günlük dosyaları nerede duracak: `veri\`, `rapor\` ya da yeni bir `gunluk\` klasörü mü? Levent'in hatayı bulmak için hangi klasöre bakacağı nerede yazılacak?

16-055. Günlük dosyası günlük döndürmeli mi (`TimedRotatingFileHandler`), boyuta göre mi, yoksa koşu başına ayrı dosya mı? Koşu başına dosya, "bir akşamın kaydı tek dosya" sorusunu kolaylaştırır; bu tercih neye göre yapılacak?

16-056. Günlükler kaç gün ya da kaç MB saklanacak? Kural, kâğıt üstü canlı dönemde (en az 6 ay, §5.8) bir sorunun nedenini sonradan araştırmaya yetecek şekilde mi belirlenecek?

16-057. Windows'ta `TimedRotatingFileHandler` döndürme sırasında dosya başka bir süreç tarafından açıksa PermissionError verir. Günlük dosyasını aynı anda zamanlayıcı koşusu ve elle koşu yazarsa bu nasıl yönetilecek?

16-058. Günlük satır biçimi düz metin mi (insan okur), JSON mu (makine okur)? Levent'in günlüğü Not Defteri ile okuyacağı varsayılırsa JSON biçimi buna uyar mı?

16-059. Her koşu başında hangi bilgiler günlüğe yazılacak: kod hash'i, kütüphane sürümleri, veri anlık görüntüsü kimliği, Python sürümü, makine saati ve saat dilimi? §5.11 deneme günlüğü ile bu koşu günlüğü arasındaki sınır nerede?

16-060. Operasyon günlüğü (koşu geçti mi, hata ne) ile deneme günlüğü (§5.11, bilimsel kayıt) aynı yerde mi, ayrı yerlerde mi tutulacak? İkisini birleştirmek günlük döndürme sırasında deneme kaydını silme riski doğurur mu?

16-061. Kütüphanelerin (borsapy, requests, statsmodels) uyarı ve hata çıktıları günlüğe yönlendirilecek mi? Konsola `print` yapan kütüphaneler zamanlayıcı altında sessizce kaybolursa nasıl yakalanacak?

16-062. Yakalanmayan istisnalar (traceback) günlüğe nasıl yazılacak? `sys.excepthook` ve zamanlayıcı altında `pythonw.exe` kullanımı (konsol penceresi yok) stderr çıktısını yutar; bu nasıl önlenecek?

16-063. Günlüğe hangi düzeyler kullanılacak ve "uyarı" ile "hata" arasındaki sınır nerede çizilecek? Örneğin bir hisse karantinaya girmesi (§5.1) uyarı mı, hata mı, bilgi mi?

16-064. Günlük dosyasında Türkçe karakterler (ı, İ, ş, ğ) Windows varsayılan kod sayfasında bozulabilir. Günlük dosya kodlaması ve konsol kodlaması (`encoding="utf-8"`) nasıl sabitlenecek?

16-065. Günlükte sembol listesi, fiyat ya da pozisyon bilgisi gibi kişisel/mali veri yer alacak mı? Yedekleme ya da paylaşım sırasında günlük dosyaları bu açıdan gözden geçirilecek mi?

16-066. Çok uzun koşularda (sınama) ilerleme bilgisi günlüğe ne sıklıkla yazılacak? 100 hisse × 3 aile × 1.000 tekrar için günlük dosyası kontrolsüz büyürse bu nasıl sınırlanacak?

## G. Çıkış kodları ve başarısızlığın görünürlüğü

16-067. Levent bir koşunun başarısız olduğunu nereden görecek: e-posta, masaüstü bildirimi, Telegram (§3'te "yok"), rapor klasöründeki bir dosya mı? "Telegram yok" kararı ile "sessiz başarısızlığın fark edilmesi" ihtiyacı nasıl bağdaşacak?

16-068. Çıkış kodu sözleşmesi ne olacak: 0 başarı, 1 genel hata, ayrı kodlar (kilit alınamadı, veri bayat, kalite kontrolü başarısız, tatil günü)? Görev Zamanlayıcı bu kodları Levent'e nasıl gösterir, yoksa yalnız "son çalıştırma sonucu" sütunu mu?

16-069. Veri bayatsa ya da kalite kontrolü başarısızsa "kart üretilmez" (§5.1, §6.1). Bu durum işletim sistemi açısından başarı (çıkış kodu 0, doğru davranış) mı, başarısızlık mı? Levent ikisini nasıl ayırt edecek?

16-070. Levent akşam kart listesini açtığında dosya yoksa bunun nedeni "bugün sinyal yok", "tatil", "veri bayat" ya da "koşu hiç çalışmadı" olabilir. Dört durumu ayırt eden tek bir görünür işaret (örn. durum dosyası) olacak mı?

16-071. "Bugün koşu çalıştı ve sinyal yok" ile "bugün koşu çalışmadı" durumlarının kullanıcıya aynı görünmesi ciddi bir güven riski doğurur. Koşunun yaşadığını kanıtlayan bir "son başarılı koşu" göstergesi nerede olacak?

16-072. Koşu çökmeden yarıda donarsa (ağ bekliyor) çıkış kodu hiç oluşmaz. Donma, zaman aşımı olmadan nasıl tespit edilecek?

16-073. Bildirim gerekecekse kanal olarak hangisi "asgari altyapı"dır: Windows toast bildirimi, e-posta (SMTP parolası saklama gerekir), bir dosya ya da Görev Zamanlayıcı'nın kendi uyarısı? Parola ya da anahtar saklama ihtiyacı doğan seçenekler baştan elenecek mi?

16-074. Bildirim yalnız başarısızlıkta mı, her akşam mı gelecek? Her akşam gelen "tamam" bildirimi okunmaz hâle gelirse başarısızlık bildirimi kaybolabilir; bu denge nasıl kurulacak?

16-075. Bir hata bildirimi hata türünü ve Levent'in yapacağı eylemi içerecek mi (örn. "veri bayat, 21:00'de yeniden dene")? Teknik olmayan bir kullanıcı için hata iletisi Türkçe ve eylem odaklı olacak mı?

16-076. Kısmi başarı (örn. 100 sembolden 3'ünün indirilememesi) nasıl raporlanacak? Kalite eşiği (kaç sembol eksikse koşu "başarısız" sayılır) §5.1'de tanımlı değil.

## H. Saat dilimi ve yaz saati

16-077. Türkiye 2016'dan beri kalıcı UTC+3 kullanıyor, yaz saati uygulaması yok. Sistem yine de "Europe/Istanbul" saat dilimini mi kullanacak yoksa sabit UTC+3 mü? Windows saat dilimi ayarı Levent'in makinesinde yanlışsa (örn. yurt dışında) görev saati ne olur?

16-078. Levent'in bilgisayarının saat dilimi Europe/Istanbul dışına ayarlanırsa (seyahat) 19:30 görevi yerel saate göre mi çalışacak? Bu durumda "bugünün işlem günü" kararı hangi saate göre verilecek?

16-079. `dt.date.today()` (veri.py, rapor.py) makine yerel saatini kullanır. Yeni kodda "bugün" kavramı saat dilimi farkındalıklı bir saatten mi türetilecek? Makine saati yanlışsa tazelik kontrolü (§5.1 "son çubuğun tarihi bugün değilse") yanlış karar verir; bu nasıl korunacak?

16-080. Tarihler ve zaman damgaları (anlık görüntü, deneme günlüğü, kural kaydı) UTC mi, İstanbul saati mi saklanacak? Saat dilimsiz (naive) zaman damgalarının parquet ve pandas arasında sessizce kayması nasıl önlenecek?

16-081. İş Yatırım ve borsapy (TradingView) farklı saat dilimleriyle zaman damgası döndürürse günlük çubuk tarihleri bir gün kayabilir. Gün sınırı (00:00 UTC ile 03:00 İstanbul) hangi katmanda normalleştirilecek?

16-082. Geçmiş veri 2015'e uzanıyor. 2015–2016 döneminde Türkiye yaz saati uyguluyordu (ve 2016 Eylül'de kalıcı +3'e geçti). Bu dönemin zaman damgalı verisi (günlük çubukta anlamlı mı?) işlenirken saat dilimi veritabanı (`zoneinfo` ve Windows'ta `tzdata` paketi) gerekli mi?

16-083. Windows'ta Python `zoneinfo` kendi saat dilimi veritabanını içermez; `tzdata` paketi gerekir. Bu bağımlılık pyproject'e eklenecek mi, yoksa saat dilimi hiç kullanılmadan sabit sapma mı kullanılacak?

16-084. Görev Zamanlayıcı'nın 19:30'u yerel saat olarak yorumlaması ile kodun "bugünkü seans kapanışı 18:00 (ya da 18:10)" varsayımı birbirine nasıl bağlanacak? Seans saatleri değişirse (BIST kapanış saatleri geçmişte değişti) bu bilgi nerede tutulacak?

## I. Tatiller ve yarım günler

16-085. §4 "Takvim: tarih → işlem günü mü; BIST tatilleri, yarım günler" der. Tatil listesi hangi kaynaktan gelecek: Borsa İstanbul duyurusu, bir Python paketi (exchange_calendars, pandas-market-calendars, holidays), elle yazılmış liste? Hangisinde BIST kapsamı ve dinî bayram tarihleri doğru?

16-086. Dinî bayramlar ay takvimine bağlı ve yıllar önceden Resmî Gazete ile kesinleşir. Takvim önümüzdeki yıl için yeterince güncel değilse koşu hangi davranışı gösterecek: tatili bilmediği için bir tatil gününde kart üretmeye mi çalışacak?

16-087. Köprü günleri için hükümet bazen idari izin ilan eder; borsa kapalı ya da yarım gün olabilir. Bu duyurular takvime otomatik mi girecek, elle mi? Kim, ne sıklıkla güncelleyecek?

16-088. Yarım gün (arife) seansları ne zaman biter ve hacim ile AOF bu günlerde farklı davranır mı? Günlük koşu yarım günde saat 19:30'dan önce mi sonra mı anlamlı veri bulur, ve sınama yarım günleri normal gün sayar mı?

16-089. Tatil günü 19:30 görevi çalışırsa ne yapacak: hiç çalışmadan çıkacak mı, "tatil, atlandı" günlüğü yazacak mı? Bu davranış "koşu çalıştı ve sinyal yok" ile nasıl karıştırılmayacak?

16-090. Takvim modülü hem sınamada (geçmiş 2015–2026) hem günlük koşuda kullanılacak. Aynı kaynak geçmiş tatilleri (örn. 15 Temmuz sonrası olağanüstü kapanışlar, 2020 Mart'taki duruş) de doğru verir mi, yoksa fiyat verisindeki eksik günler mi "işlem günü değil" kanıtı sayılacak?

16-091. Veri kaynağında bir gün için çubuk yoksa bu tatil midir, veri eksikliği midir? §5.1 karantina ve §6.1 tazelik kuralı bu iki durumu takvim olmadan ayırt edemez; hangi kaynak yetkilidir?

16-092. Hafta sonu Cumartesi ya da Pazar günü koşu görevi çalışacak mı? Görev yalnız Pazartesi–Cuma tanımlanırsa, hafta sonu açık kart güncellemesi ve kaçırılan koşu telafisi bu tanımla nasıl çelişmez?

## J. Ağ hataları ve yeniden deneme

16-093. İş Yatırım `HisseTekil` ve borsapy için zaman aşımı, yeniden deneme sayısı ve bekleme süresi ne olacak? "Kullanım koşulları ve hız sınırları bulunamadı" (§4) denildiğinde yeniden deneme kendisi hız sınırına çarpmayı artırır mı?

16-094. Yeniden deneme için tenacity, urllib3 `Retry` ya da requests adaptörü gibi hazır bir mekanizma mı kullanılacak, yoksa elle bir döngü mü? Borsapy kendi içinde yeniden deneme yapıyorsa iki katmanlı deneme çarpanı sorun olur mu?

16-095. Tek bir sembol indirilemezse koşu o sembolü atlayıp devam mı edecek, yoksa tüm koşu mu başarısız olacak? Atlanan sembol sinyal kaybıdır; eksik sembol listesi kartların yanında nasıl görünecek?

16-096. Kısmi veriyle (örneğin bugünün çubuğu henüz yayınlanmamış) alınan yanıt ile boş yanıt ayırt edilecek mi? İş Yatırım veriyi gün içinde geçici değerlerle yayınlarsa bu veri "bugünün çubuğu" olarak depoya girip değişmez anlık görüntüye dönüşebilir mi?

16-097. Ağ geçici olarak yoksa (Wi-Fi bağlanmamış, uyku sonrası ağ henüz gelmemiş) koşu ilk denemede başarısız olur. 19:30'da uyandırılan bir makinenin ağı hazır olana kadar beklenecek mi, ve ne kadar?

16-098. Kaynak yanıtı sessizce değişirse (sütun adı, birim, HACIM lot/TL belirsizliği §5.1) bu bir ağ hatası değil ama koşuyu bozar. Şema doğrulaması hangi katmanda yapılacak ve başarısız olunca ne olacak?

16-099. Çapraz kontrol kaynağı borsapy yanıt vermezse (yalnız İş Yatırım verisi alınırsa) günlük koşu çapraz kontrolsüz mü devam edecek? Bu durumun kartlara "doğrulanmamış veri" olarak yansıması gerekli mi?

## K. Sınama koşusu ile günlük koşu ayrımı

16-100. Sınama (backtest) koşusu ile günlük koşu aynı veri deposunu, aynı Adım fonksiyonunu ve aynı deneme günlüğünü paylaşıyor (§4, §5.11). Günlük koşu deneme günlüğüne yazar mı, ve yazarsa her akşamki rutin koşu Holm düzeltmesindeki deneme sayısını şişirir mi?
