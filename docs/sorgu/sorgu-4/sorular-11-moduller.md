# Sorular 11: Depo yapısı ve modüller

11-001. TASARIM.md §4 tablosu 12 modül sayıyor. Hangileri ayrı bir dosya, hangileri ayrı bir paket, hangileri yalnızca bir fonksiyon olmayı hak ediyor?

11-002. Takvim modülü "tarih → işlem günü mü" diye tek bir soruya cevap veriyor. Bu, veri deposundaki fiyat tablosunun tarih sütunundan türetilemez mi, yoksa ayrı bir modül gerekçesi var mı?

11-003. Maliyet modülü "işlem → masraf" ve sabit %0,3. Sabit bir yüzde için ayrı modül mü, simülatörde bir sabit mi?

11-004. §4'te Maliyet için "Takılıp çıkarılabilir" yazıyor. Takılıp çıkarılacak ikinci bir maliyet modeli var mı, yoksa bu soyutlama tek uygulamalı bir arayüz mü?

11-005. Şirket olayları ile Veri deposu neden iki modül? Düzeltme katsayısının uygulanması (§5.1) hangisinin işi?

11-006. Evren modülü "tarih → taranabilecek hisseler". İki uygulaması var (ara çözüm PD ile en büyük 100, sonra KAP). Bu iki uygulama aynı arayüzün arkasında mı duracak, yoksa biri öbürünü silecek mi?

11-007. Piyasa durumu modülü kapı değil, yalnızca etiket (§4). Etiket yalnız rapor bölmek için kullanılacaksa ayrı modül yerine rapor modülünde bir fonksiyon olamaz mı?

11-008. Aile modülü "hisse fiyatı → sinyal günleri" diyor. Çift rotasyonu iki hissenin fiyatını alır ve pozisyon durumu taşır. Bu "Aile" arayüzüne sığıyor mu?

11-009. Çift rotasyonunda stop yok, karşı uçta geçiş var (§5.5). Bu davranış Adım fonksiyonunun imzasına (pozisyon, bugünkü mum → pozisyon) nasıl girer, bir mumla iki hisse nasıl temsil edilir?

11-010. Adım fonksiyonunun girdisi "bugünkü mum" tek. ATR, SMA250 ve EMA gibi geçmişe bakan göstergeler bu girdide yok. Bu değerler nereden gelir ve Adım hâlâ saf mı kalır?

11-011. Adım fonksiyonu sinyali de üretiyor mu, yoksa yalnız açık pozisyonu mu güncelliyor? Giriş kararı ile çıkış kararı aynı fonksiyonda mı yaşar?

11-012. "Sınama ve canlı günlük aynı fonksiyonu kullanır" (§4, A5). Canlıda Adım'a verilen mum AOF'lu kapanmış gün mü, yoksa 19:30'da yarım kalmış veri mi? Bu fark Adım'ın arayüzünü değiştirir mi?

11-013. Adım fonksiyonu pandas Series/DataFrame mi alacak, düz sayılar mı? Bu seçim, gün gün döngünün (§4 Motor) hızını ve sınama dayanıklılığını nasıl etkiler?

11-014. Motor "Adım'ı gün gün koşar". 100 hisse × 11 yıl × 1.000 rastgele tekrar (§5.7) için Python döngüsü yeterli mi? Yetmezse Adım'ın yeri nerede olur?

11-015. Rastgele kural karşılaştırması (K1) motoru 1.000 kez koşturuyor. Motor bu kullanım için mi tasarlanacak, yoksa K1 ayrı bir koşucu mu gerektirir?

11-016. Motor ile Simülatör arasındaki sınır net değil. Pozisyon boyutu ve %10 tavan, "10 pozisyon" sınırı motora mı simülatöre mi ait? Sinyal sırası ve likidite sınırı (M11, M12) kimin?

11-017. İşlem listesi (motor çıktısı) bir DataFrame mi, dataclass listesi mi? İki modül arasındaki en önemli sözleşme bu şekil; nerede tanımlanır?

11-018. Simülatör "iki bölme türü" için tek modül. Tek hisse bölmesi ve çift bölmesi ayrı iki program gibi görünüyor. Ortak kod var mı, yoksa tek modülde iki bağımsız dal mı?

11-019. İstatistik modülü "sermaye eğrisi → güven aralığı, p değeri". Blok yeniden örnekleme için arch/statsmodels hazır fonksiyon veriyor mu? Modül yalnız ince bir sarmalayıcıysa var olması gerekir mi?

11-020. Holm düzeltmesi ve deneme günlüğü (§5.11) hangi modülde? Tabloda hiçbir modül bunu sahiplenmiyor.

11-021. Kural kaydı ve kod hash'i (§5.8) için hangi modül sorumlu? §4 tablosunda yok, ama §7 madde 3'te zorunlu.

11-022. Deneme günlüğü ve kural kaydı tek bir depolama mı, iki mi? Bunlar "modül" mü, yoksa tek bir tablo/dosya mı?

11-023. Sadakat kontrolü (§7 madde 2) bir modül mü, bir betik mi, bir test mi? Çıktısı bir kez üretilip kaydedilecekse kalıcı kod olması gerekir mi?

11-024. Karantina mantığı (§5.1) hangi modülde? Veri deposu mu, şirket olayları mı, ayrı bir "kalite" modülü mü?

11-025. İkinci kaynakla (borsapy) tam karşılaştırma bir modül mü, bir kez koşulan denetim mi? Her koşuda mı yoksa yalnız veri indirildiğinde mi çalışır?

11-026. Kart üretimi (§6) ve CSV kart listesi hangi modülde? "Rapor" yalnız markdown ve CSV diyor, ama "kart" kavramı GLOSSARY.md'de ayrı bir terim.

11-027. Kart durum güncellemesi (AKTİF/STOP/HEDEF/BOZULDU, §6 madde 5) kalıcı bir durum tutmayı gerektirir. Bu durum nerede saklanır ve hangi modül sahibi?

11-028. Streamlit "Kanıt" ekranı (§3) hangi pakette durur? Raporu okuyan bir ekran, motor ve istatistik paketlerine bağımlı olmamalı; bu bağımlılık yönü nasıl korunur?

11-029. Streamlit kapsamda ama "ilk aile kabul edilene kadar bekler" listesinde Streamlit kart paneli var. Ekran bir sayfa; markdown raporu zaten varken bu sayfa neden ilk sürümde gerekli?

11-030. Önerilen paket yapısı düz mü (tansu/*.py), alt paketli mi (tansu/veri/, tansu/sinama/)? 12 modül için hangisi okunabilir, hangisi gereksiz derinlik?

11-031. Mevcut prototipte tansu/ altında 5 düz dosya var (aileler, kanit, nabiz, rapor, veri). Yeni yapıda hangi dosya adları korunur, hangileri silinir?

11-032. Prototipten silinecekler listesi var mı? veri.py (yfinance), kanit.py (vectorbt, 4 ATR hedef), nabiz.py (kapı mantığı), rapor.py (5 rastgele tekrar, 2023 ayrılmış dönem) dört dosyanın dördü de eski tasarıma ait görünüyor. Hangisinden ne kurtarılır?

11-033. aileler.py içindeki `ema()` yardımcı fonksiyonu kanit.py tarafından içe aktarılıyor (aileler → kanit bağımlılığı tersine döner). Yeni yapıda göstergeler nerede yaşar?

11-034. Göstergeler (EMA, ATR, SMA) pandas-ta-classic'ten mi alınacak, pandas ewm/rolling ile mi? İki kaynak karışırsa aynı EMA'nın iki hesaplaması oluşmaz mı?

11-035. Adım fonksiyonu gün gün çalıştığı için göstergeleri önceden vektörel hesaplanmış sütun olarak mı bekler? Göstergeyi sınamada vektörel, canlıda tek gün hesaplamak aynı sonucu garanti eder mi?

11-036. Aile sinyali vektörel (tüm seri bir anda) ise, canlı günde "bugünkü sinyal" son satırı mı olur? Bu, sinyal fonksiyonunun geleceğe sızmadığını nasıl kanıtlar?

11-037. Gelecek sızıntısı (look-ahead) sınaması için bir test düzeneği tasarıma yazılmış mı? Hangi modülün test düzeni bunu üstlenir?

11-038. Bağımlılık yönü hangisi: aile → motor, motor → aile mı? Motor aileyi bir fonksiyon olarak mı alır, yoksa aile motoru mu çağırır?

11-039. Hangi modüller bir diğerini içe aktarabilir? Döngüsel bağımlılığı (ör. motor ↔ maliyet, simülatör ↔ istatistik) önleyen yazılı bir kural var mı?

11-040. Bir "çekirdek" (saf mantık: aile, adım, motor, simülatör) ve "kenar" (veri indirme, dosya, rapor, ekran) ayrımı yapılacak mı? Yapılmazsa saf mantık dosyaya ve ağa bağlanır mı?

11-041. Ağa çıkan tek yer veri deposu mu? İş Yatırım, borsapy, KAP, EVDS dört kaynak; her biri ayrı bir bağdaştırıcı (adapter) mı, tek dosya mı?

11-042. Dört veri kaynağı için ortak bir "kaynak" arayüzü gerekiyor mu? Kaynakların hepsi farklı şeyler döndürüyor (fiyat, olay, üyelik, faiz); ortak arayüz anlamlı mı, yoksa zorlama bir soyutlama mı?

11-043. İş Yatırım `HisseTekil` için resmî olmayan bir uç nokta kullanılıyor (veri-kaynaklari.md). Uç nokta değişirse hangi modül etkilenir ve etki nasıl sınırlanır?

11-044. borsapy üçüncü taraf bir kütüphane ve §4'te 78 kodu attığı yazıyor. Evren, faiz, sektör ve çapraz kontrol için dört yerde borsapy'a dayanmak, tek bir kütüphaneye aşırı bağımlılık mı?

11-045. Modül başına bir kütüphane haritası var mı? Hangi modül hangi kütüphaneyi içe aktarabilir (ör. yalnız veri paketi pandas dışında ağ kütüphanesi kullanabilir)?

11-046. Sahibi "güvenilir kütüphane" istiyor. Hangi modüller tamamen kütüphane çağrısı olabilir (istatistik → statsmodels/arch, ölçütler → quantstats) ve hangileri bizim yazdığımız kod olmak zorunda?

11-047. Tasarım vectorbt'yi reddediyor, ama pyproject.toml bağımlılık listesi içermiyor; prototip vectorbt ve yfinance'i kullanıyor. Bağımlılıkların tek doğru yeri neresi ve eski bağımlılıklar nasıl temizlenir?

11-048. pyproject.toml yalnız pytest ayarı içeriyor; proje meta verisi, bağımlılıklar, Python sürümü, paket adı yok. Paket kurulabilir olacak mı (pip install -e), yoksa `pythonpath = ["."]` yeterli mi?

11-049. Python sürümü (.venv 3.14 görünüyor) pandas-ta-classic, quantstats, statsmodels ile uyumlu mu? Sürüm sabitleme kuralı nerede yazılı?

11-050. Bağımlılıkları kilitlemek için uv/pip-tools/lock dosyası kullanılacak mı? Tek kişilik, Windows 11 PC kurulumunda ne kadarı gerekli?

11-051. Kodda Türkçe alan adları (Aile, Adım, Evren, Bölme, Kart) mı, İngilizce mi? Prototip Türkçe (`islemler`, `sinyal`, `nabiz`); kütüphane API'leri İngilizce. İkisi aynı satırda karışırsa okunabilirlik ne olur?

11-052. Türkçe karakterler (ı, ş, ğ) kod adlarında kullanılacak mı? Prototip ASCII'ye çevirmiş (`kanit`, `bolme`); bu kural yazılı mı ve dosya adları, sütun adları, CSV başlıkları için de geçerli mi?

11-053. GLOSSARY.md'deki terimler ile kod adları bire bir eşleşecek mi (Fazla getiri → `fazla_getiri`, Bozulma → `bozulma`)? Eşleşme kontrol edilecek mi, yoksa sözlük ile kod zamanla ayrışır mı?

11-054. "Adım" kelimesi İngilizce "step" için seçilmiş. Kodda `adim` mi, `step` mi? Gün sayacı olarak "adım" ile pozisyon güncellemesi olarak "adım" karışır mı?

11-055. "Bölme" (tek hisse/çift) GLOSSARY'de var; kodda `bolme` ile hisse "bölünmesi" (split) aynı kökten. Şirket olayındaki bölünme ile portföy bölmesi kod adlarında nasıl ayrılır?

11-056. Raporlar ve kart başlıkları Türkçe; sütun adları kodda hangi dilde? CSV kart listesinin sütun adları sözleşme mi, yoksa serbest mi?

11-057. Ortak veri tipleri (Fiyat tablosu, İşlem, Pozisyon, Sinyal) nerede tanımlanır? Bu tipler hangi modüle ait olmadığı için hepsi tarafından içe aktarılan bir `tipler` dosyası gerekir mi?

11-058. Fiyat tablosunun sütun sözleşmesi ne: İngilizce `Close/High/Low` (prototip), Türkçe `kapanis/yuksek/dusuk`, ya da İş Yatırım ham adları `HG_KAPANIS`? Dönüşüm hangi sınırda yapılır?

11-059. Fiyat tablosunda ham ve düzeltilmiş fiyat birlikte duruyor (§5.1). Aile ve göstergeler yanlışlıkla ham sütunu okursa bedelsiz günü sahte kırılım olur. Bu hata türünü tür düzeyinde önlemek mümkün mü, yoksa yalnızca disiplin mi?

11-060. Veri deposu "tarihli, değişmez anlık görüntü" tutuyor. Anlık görüntü formatı parquet dosyası mı, klasör mü, SQLite mi? DuckDB ertelendi; parquet yeterli mi?

11-061. Anlık görüntü klasörü her koşuda bir kopya mı? 100 hisse × 11 yıl günlük veri küçüktür, ama kaç anlık görüntü saklanır ve ne zaman silinir?

11-062. Deneme günlüğü (§5.11) ekleme yapılan bir CSV mi, SQLite mi, JSON satırları mı? Windows'ta çift tıklayıp açılan sahip için en az altyapı hangisi?

11-063. Kural kaydı (§5.8) kod hash'i hangi koda bakıyor? Tüm paketin hash'i mi, yalnız ilgili aile dosyasının mı? Ortak bir Adım değişince bütün kayıtlar mı geçersiz olur?

11-064. Git depoda yok gibi görünüyor (depoda .git araması yapılmadı, ama AGENTS.md'de uzak repo yok yazıyor). Kod hash'i için git commit kimliği mi kullanılacak, dosya içeriği hash'i mi?

11-065. Çıktı klasörleri (veri/, rapor/, anlık görüntü/, deneme günlüğü) kod ağacının neresinde? Hangisi git'e girer, hangisi .gitignore'da, hangisi yedeklenir?

11-066. Yapılandırma (parametreler, evren büyüklüğü, masraf %0,3, 1.000.000 TL sermaye) nerede durur? Parametre kaydı (§5.10 "ek: parametre kaydı") bir Python sabiti mi, TOML/YAML mi?

11-067. Ailenin parametreleri (%1,2 bant, 3 gün, r = 1,0) aile kodunun içinde mi, ayrı bir kayıt dosyasında mı? Kural kaydı hash'i hangisine bakar?

11-068. 5.10'daki "rastgele ızgara" parametre sağlamlığı, her ailenin parametrelerini dışarıdan değiştirebilmeyi gerektirir. Aile arayüzü parametreleri bir nesne olarak mı alır?

11-069. Aile arayüzü fonksiyon mu (prototipte `Callable`), sınıf mı, protokol mü? Parametre, durum ve çift ailesinin iki hissesi için en küçük çalışan şekil hangisi?

11-070. AILELER sözlüğü kayıt defteri (registry) deseni. Üç aile için bu sözlük gerekli mi, yoksa açık bir liste ya da doğrudan içe aktarma yeter mi?

11-071. "Yeni aile eklemek: fonksiyon yaz, AILELER'e kaydet" (aileler.py). Üçüncü bir aile eklemenin gerçek maliyeti ne olacak ve bu maliyet mevcut arayüzle tahmin edilebiliyor mu?

11-072. Ailelerin ayrı dosya mı yoksa tek `aileler.py` dosyasında mı yaşayacağı belli değil. Çift rotasyonu eşbütünleşme ve z-skor gerektirir, AB=CD pivotlar; üçü tek dosyada kalır mı?

11-073. Çift seçimi (§5.6, eşbütünleşme) bir aile mi, evren mi, ayrı bir modül mü? Yıllık seçim ve çakışma çözümü hangi modülün sorumluluğu?

11-074. AB=CD pivot tespiti için bir kütüphane (scipy.signal.find_peaks, zigzag) mi kullanılacak, kendi yazılacak mı? Pivot ayarı "sadakat kontrolüyle belirlenir"; bu ayar hangi dosyada tutulur?

11-075. Sadakat kontrolü Yahoo verisiyle yapılacak (§7). "Yahoo kullanılmaz" kuralı ile çelişmemesi için Yahoo'ya dokunan kod nerede izole edilir ve ana veri deposundan nasıl ayrılır?

11-076. Sadakat kontrolü tamamlandıktan sonra Yahoo kodu silinecek mi? Silinirse ilerideki sadakat yeniden denemeleri nasıl yapılır?

11-077. Piyasa durumu etiketi için prototipteki `nabiz.py` yeniden yazılıyor ama BEKLE/TAM_ALIM/DIKKATLI kapı mantığı korunamaz. Hangi satırlar kullanılabilir ve etiket kümesi ne olur?

11-078. Piyasa durumu etiketi rastgele karşılaştırmada (K1 b türü, "aynı piyasa durumu ±20 gün") kullanılıyor. Bu, Piyasa durumunu motorun bir girdisi yapar; "yalnız raporlama" iddiasıyla tutarlı mı?

11-079. Evren modülü her ay başında üretiyor, fakat motor her gün evrene bakıyor. Evren çıktısı tarih bazlı bir tablo mu, çağrıldıkça hesaplanan bir fonksiyon mu?

11-080. Kapanmış hisselerin fiyat verisi (ASYAB gibi) veri deposuna nasıl girer? Kapanışta pozisyonun nasıl sonlandığı (delisting) Adım ve Motor'da hangi kuralla ele alınır?

11-081. Sınama yöntemi 12 maddelik (§5.1–§5.12). Bu maddelerin kaçı kod modülü, kaçı yalnız belge ve süreç? Örneğin 5.12 kabul ölçütü bir kod fonksiyonu mu, elle okunan bir liste mi?

11-082. Kabul ölçütü otomatik hesaplanacaksa "Canlı/Deneme" etiketini kim atar? Bu etiket kodun içinde mi, bir dosyada mı, yoksa insan kararıyla mı yazılır?

11-083. Rapor modülü yalnız markdown ve CSV üretiyor. Markdown'ı üretmek için bir şablon kütüphanesi (Jinja) mı, f-string mi? Sahip kolayca değiştirebilsin diye hangisi daha az altyapı?

11-084. quantstats raporu HTML üretir. Tasarım "Ölçütler quantstats'tan" diyor ama çıktı markdown. Bu iki biçim nasıl bir arada durur?

11-085. Komut satırı giriş noktası var mı? Prototipte `python -m tansu.rapor` var. Sahip teknik değil; günlük 19:30 işi ve sınama koşusu için hangi komutlar ve hangi tek giriş dosyası olacak?

11-086. Günlük işi (§6) Windows Görev Zamanlayıcı ile mi çalışacak? Zamanlayıcıyı tetikleyecek giriş noktası hangi paket ve komut, ve başarısızlığı sahibe nasıl bildirir?

11-087. Günlük işleyiş (canlı) ile sınama (geçmiş) iki ayrı üst düzey akış. Bunların ortak kısmı yalnız Adım mı, yoksa veri okuma ve aile çağrısı da ortak mı? Ortak olmayan her satır "ayrışma" riskidir.

11-088. Canlı akışta durum (açık pozisyonlar/kartlar) bir dosyada saklanıyor olmalı. Bu dosyanın biçimi ve sahibi belirsiz. Hangi modül yazar, hangisi okur?

11-089. Hata ve eksik veri yönetimi (§6 madde 1: sorun varsa kart üretilmez) hangi katmanda? Her modül kendi hatasını mı atar, yoksa üst düzey akış mı yakalar?

11-090. Günlük kayıt (log) gerekli mi? Standart `logging` yeter mi, ya da hiç log tutmayıp rapor ve deneme günlüğü yeterli mi?

11-091. Test yapısı: tests/ klasörü düz. Test_aileler, test_kanit, test_nabiz_veri eski modüllere bağlı. Hangileri taşınır, hangileri silinir?

11-092. §5.3 "Motor sınamaları, kod yazılmadan önce" yedi senaryo sayıyor. Bu yedi sınama motor mu, Adım mı düzeyinde yazılır? Adım doğrudan test edilirse Motor için ayrı test ne ekler?

11-093. Ağa bağlı testler (İş Yatırım, borsapy) CI'sız tek kişilik ortamda nasıl ele alınır? Kaydedilmiş örnek yanıtlar (fixture) mı, canlı test mi, hiç test yok mu?

11-094. Tür denetimi (mypy/pyright), biçimleyici (ruff/black) kullanılacak mı? "Minimum altyapı" ile "sağlam temel" arasında hangisi bu kategoriye girer?

11-095. docs/adr/ klasörü AGENTS.md'de tarif edilmiş ama yok. Modül sınırları ve kütüphane seçimleri gibi kararlar ADR olarak mı yazılacak, yoksa TASARIM.md yeterli mi?

11-096. TASARIM.md "kod bu belgeye uyar" diyor, 12 modül tablosu kodun yapısını dayatıyor. Kod ile tasarım ayrışırsa hangisi güncellenir ve bunu kim kontrol eder?

11-097. Hangi modül ilk sürümde gerçekten gerekli, hangisi "ilk aile kabul edilene kadar bekleyebilir"? Örneğin Takvim, Maliyet, Piyasa durumu, Şirket olayları ilk uçtan uca koşu için şart mı?

11-098. İlk uçtan uca "dikey dilim" ne olacak: tek hisse, tek aile, sabit evren, Adım + Motor + minimal rapor mu? Hangi modüller bu dilimde yok ve sonradan eklenince arayüzlerini değiştirir mi?

11-099. Modüllerin "dışa küçük yüz" ilkesi (§4) için ölçülebilir bir kural var mı (ör. her modülün genel fonksiyon sayısı, dışa açık adların `__all__` listesi)? Yoksa bu ilke yalnız niyet beyanı mı?

11-100. Sahip teknik değil ve tek kişi çalıştırıyor. Bir yıl sonra yeni bir kişi (ya da yeni bir model oturumu) depoyu açtığında hangi tek dosya hangi modülün nerede olduğunu, hangi komutun ne yaptığını söylüyor ve bu dosya kodla nasıl senkron tutuluyor?
