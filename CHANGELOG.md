# Değişiklik günlüğü

TANSU'nun önemli değişiklikleri bu dosyada, en yenisi üstte olacak biçimde yer alır.
Düzen [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
sürüm numaraları [Semantic Versioning](https://semver.org/spec/v2.0.0.html) biçimini izler.

## [Yayımlanmamış]

- İşlem kontrolü, düzeltilmiş AOF ve kapanışta veri kapısının mevcut yuvarlama payını kullanır; fiyatlar ve ham limit denetimi korunur. (#169)
- Kayıtlı ileri yürümede seçim alanı, sonuç içeriği ve nihai giriş kohortu sayımları aynı kaynak doğrulamasına bağlandı. Tam kontrollerin bitmesi için CI iş süresi 15 dakikadan 30 dakikaya çıkarıldı; testler ve başarı ölçütleri korundu. (#93)

- #136: Kural kataloğu, aile kuralları ve kaynak dökümü tek sahipli belgelere ayrıldı; kaynak kimlikleri ve gerekli kısıtlar korundu.

### Değişti

- Saklı ileri yürüme kaynakları, çağıranın özetinden bağımsız yayımlanmış sürüm özetleriyle doğrulanır; tutarlı özetli sahte üyelik ve pay bağları eklemede ve geçmiş okumada reddedilir. (#167)
- Tam denetimlerin tamamlanması için CI iş süresi 30 dakikadan 60 dakikaya çıkarıldı; testler ve başarı ölçütleri korundu. (#167)

- Pay kimliği seçilmiş ileri yürümenin üyelik ve eşleme kaynakları başlangıç kaydında özetleriyle saklanır; geçmiş okuma canlı tablolara bağlı kalmaz. Eksik eski gelişim kanıtı açıkça reddedilir. (#167)

- Ortak dönem kurulumu sinyal tarihlerini iki sınır günü dahil seçer; dönem sırası, aynı gün tekrarları, değerler ve sinyal kimlikleri korunur. Sınır günleri kurulumda bulunmasa da geçerli seçim hata vermez. (#168)

- Site işlerinin esas şablonu Levent'in tarihli kararı ve içerik özetiyle sabitlendi; modül başına kaynak, canlı kanıt ve ayrı yayım onayı korundu. (#69)

- Ana dal adı `main` oldu; CI, edit kancası, kapanış komutu ve güncel iş yönergeleri yeni ada uyarlandı. (#142)

- Çalışma kuralları kullanılan ajan araçlarına uyarlandı; belge sahipliği ve bekleyen sözleşmelerin durumu netleşti. Tekrarlanan inceleme kuralları atfa dönüştü, iş klasörü kapanışına silme onayı ve kanıt kontrolü eklendi. (#130)
- Altı çalışma belgesi mevcut sahiplerinde birleştirildi; kontrol ve gerçek veri kanıtı inceleme öncesine alındı, küçük işte yazıcı devri ve kapsam kuralları sadeleştirildi. Eski bilet sözleşmesi geçmiş bölümüyle korundu.

### Eklendi

- Mevcut 24 varyantın kayıtlı altı dönem sınaması için açık eşleme alan komut ve destek raporu eklendi; eksik sonuçlar ve gerçek kayıt başvuruları korunur. (#57)

- Kayıtlı sağlayıcı ve görüntüye bağlı, açık seçimli pay kimliği eklendi. Tarihli KOZAA/TRMET ve KOZAL/TRALT kodları fiyat ve olay değerleri değiştirilmeden aynı pay geçmişine bağlanır. Eski etiket davranışı korunur; kaynak, özet ve çakışma hataları reddedilir. Eksik ısınma ve düzeltme kökeninin kanıt sınırı korunur. (#167)

- Pay kimliği başvuruları LF biçiminde sabitlendi; taşınabilir tablo özeti ve gerçek depo eşlemeleri otomatik denetleniyor. (#167)

- Pay kimliği ileri yürümenin eğitim seçimi, sinyal kaydı ve taşınan işlemine bağlandı; aynı görüntü özetine sahip başka kimlik seçimi reddedilir. (#167)

- Kayıtlı ileri yürüme, her çeyrekten önce eğitim seçimini kaydeder; tek kronolojik akışta açık ve bekleyen işlemlerin özgün ayarını korur. Eğitim dışlamaları, giriş kohortları ve açık ufuk ayrı kayıtlarla izlenir. (#93)
- Küçük grup hazırlığı ayrı komut ve kayıt olayıyla eklendi. En fazla üç strateji revizyonu ve 60 kesin seans dondurulur; eksik kaynak tanımı, veri, takvim ve üyelik adlandırılmış engel olur. Hazırlık hesap başlatmaz; değişen tanım yeni revizyon ister, eski kayıt tarihçede kalır. İlk kaynak ailesi engelli kalır. (#116)

- Kayıtlı taramanın ölçü hissesi gerçek dönem ve işlem kayıtlarına bağlandı. Seçilen ayarın uygun merkez ve bileşen açıklamasıyla çelişmesi reddedilir; işlemsiz hisse kayıtları korunur. (#92)

- Kayıtlı taramada bilinmeyen sonuç kayıp mesafesi sayılmaz. Başarısız dönem/hisse seçimi ve çelişkili seçildi etiketi kayıt sınırında reddedilir; bölge açıklamaları korunur. Eski düşüş süresinin açıklaması korunan ilk kapanış davranışına uyarlandı. (#92)

- Kayıtlı ayar taraması, birimleri açık ölçüler ve Levent onaylı geniş kârlı bölge seçimi eklendi. Bütün izinli ayarlar ilk hesap öncesinde kaydedilip doğrulanır; eksik ve başarısız sonuçlar gerekçeleriyle görünür kalır. Kimliği doğrulanmış veri, kapsam denetimi her ayarda korunarak paylaşılır. Eski yöntemler ortak hesap sahiplerini kullanır; farklı başlangıç ve süre anlamları açıkça ayrılır. Günlük izin ve açık korumalar korunur. (#92)

- Kayıtlı denemeyle beş ayrı yıl ve birleşik dönem yürütülür; ortak EMA ve tek hisse işlem hesabı mevcut kayıt pilotuna bağlandı. Isınma, açık işlem, kısmi satış ve hata kayıtları korunur. Kayıplı para aktarımı ve başlangıçla uyuşmayan ayar hesap başlatmaz. Eksik fiyat, kurulum veya limit kanıtı tam başarı sayılmaz; eski sınama yolu ve çift risk kapısı korunur. (#91)

- Tek hisse için bağımsız riskli işlem geçişi eklendi; günlük adım ve toplu yürütme aynı dolum, yarı satış, erteleme ve durum kaydını kullanır. Yarı satışta adet aşağı yuvarlanır; kurulum girdileri ve kararın kendi gösterge gereksinimi doğrulanır. Giriş, fiyat ve kapanış adımları okunabilir işlevlere ayrıldı; eski hesaplar ve çift risk kapısı korunur. (#90)

- İlk kaynak ailesinin giriş alternatifleri, açık alanları ve kanıt aktarım sözleşmesi hazırlandı; hesaplama ve seçim izni verilmedi, eski 24 tanımın korumaları korundu. (#117)

- Bağımsız %2 masraflı risk bütçesi, aşağı tam adet yuvarlama, kullanılmayan bütçe ve gerçekleşen net R ortak E3 hesabına alındı; komisyon varsayımı Levent'in 20.10.2026 onayıyla kesinleşti. Eski sonuçlar korundu, çiftin sayısal risk dayanağı #128'e taşındı. (#89)

- Ayar değişikliği, önceki değere dönüş ve tekrar koşuları ayrı bağlarla saklayan geçici kayıt pilotu eklendi; kayıt modülü işlem hesabının dışında sınıflandı, saklanmış eski kimlikler ve resmi deneme sayısı korundu. (#84)
- Tek hisse ve çift ailelerinde göstergeler ile işlem hazırlığı ortak hesapta üretiliyor; sinyal hazırlığıyla birlikte taşınıyor, eski çağrılar korunuyor. (#87)
- Mevcut 24 strateji tanımını ayarları ve kaynak kökenleriyle koruyan sürümlü katalog eklendi; bütün birleşim kanıtı eksik seçeneklerin panel ve komut seçimi kapalı tutuldu. (#83)
- Yedi hesap sınırı sentetik sınır testleriyle korunuyor; kural kaydı durum testi kapsamı korunarak hızlandırıldı. (#109)
- Sürümlü BIST 30 başvuru tablosu, tarihli üyelik kanıtı ve giriş günü denetimi eklendi; eksik kapsam koşuyu durdurur, eski evren politikaları korunur. (#86)
- Kayıtlı görüntü, piyasa kayıtları ve çift girdileri ortak veri motorunda hazırlandı; eski iki kalite politikası ve manifest doğrulaması korundu. (#85)
- Havuzdaki kalan 1.259 not okundu; ek kaynaklar, yeni okumalar ve gerekçeli kapsam dışı kayıtları belgelere işlendi. (#59)
- Yeni motorun davranış sözleşmesi; bağımsız işlem, dönem, kayıt ve motor sınırları ile açık yöntem ve sahip kapıları belgelendi. Eski politikalar korundu. (#82)
- Modül 1'in dokuz parçasını sade Türkçeyle, tarihli Tansu alıntıları ve henüz olmayan işlerin işaretleriyle açıklayan bağımsız sayfa eklendi. (#72)
- Güncel taramadaki 47 notun 48 görseli yeniden okundu; kurtarılan metinler ve okunamayan parçaların gerekçeleri kaydedildi. (#62)
- Üçgen girişinin 30 hissedeki sıfır işlemi, yükselmeyen salınım dipleriyle açıklandı; kod değişmedi. (#56)
- Yeni modül varyantının siteye girmeden önce resmi olmayan gölge koşuda sinyal üretmesi ve çıktıları Levent'in onaylaması kuralı yazıldı. (#71)
- Ajan araç çağrıları ve yanıtları kancayla denetleniyor; talimatlara eklenen satırlar STE denetiminden geçiyor. (#42, issue #52)
- Sonsuz düzeltilmiş fiyattan sonraki 250 satırlık giriş engeli, tek hisse ve çift yollarında ayrı testlerle korunuyor. (#58)
- GitHub ana sayfasından işlere, hedeflere, değişikliklere, yayımlanan sürüme ve kontrol sonuçlarına ulaşılabiliyor.

### Değişti

- Beceri akışlarında küçük iş kapsamı ve issue/PR kuralları uyumlandı; karar yöntemleri ile hakem doğrulaması koşula bağlandı, bulunamayan çağrılar mevcut araçlarla uygulanacak adımlara dönüştürüldü.
- Okuyucu ve vekil ajanları isteğe bağlı yardımcı oldu; dosya ve satır sayısına bağlı okuyucu zorunluluğu kalktı, ana oturum teknik soruları kaynaklardan çözüyor ve Levent'e ait kararları ona soruyor.
- İş kuralları ve Tansu akışlarında mattpocock-skills zorunluluğu kaldırıldı; gerekli adımlar doğrudan yazıldı, diğer beceri kuralları korundu.
- Tansu EMA ızgarası hücrenin ayarını ve kurulumunu motora, Tansu sınaması ve günlük komutları seçilen varyantı hesaba iletiyor; hücreler ayrı işlem önbelleği kullanıyor. (#88)
- Kök belgeler ve iş kuralları sadeleşti: denetçi sayısı riske göre, günlüğü kodu değiştiren yazar, küçük belge düzeltmeleri PR ile giriyor; README özet bölümü kalktı. (#122)
- Yerel test kapısı kaldırıldı; kanca yalnız önce testin yazıldığını denetliyor; PR denetimi gerçek veri kanıtını yalnız tansu/ kodu değişince, denetçiyi yalnız kod değişince istiyor ve yalnız master birleştirmesi gelen PR’a yeni inceleme turu istemiyor. (#122)
- Katalog kaynak turunda genel ATR çıkışı ile girişe özel başabaş ve RSI çıkışları ayrıldı; 24 tanımın eksik bileşim dayanakları açık tutuldu. (#83)
- TASARIM'da standart long/short çıkışı çift rotasyonundan ayrıldı; aynı gün stop ve hedef durumu güncel öncelik kuralına bağlandı. (#60)
- Açık havuz sayacı okunmadı listelerini kapsamdan ayırıyor; yalnız bu listelerde kalan üç nota okuma veya gerekçeli kural içermez kaydı eklendi. (#59)
- Paralel dalların değişiklik günlüğünde aynı yere eklediği satırlar, yerel Git birleştirmesinde birlikte korunuyor; Kural 5 yalnız birinci ebeveynle aynı kip ve türdeki normal dosyanın birebir union sonucunu temiz sayıyor. (#102)
- İş gövdeleri triage biçiminde yazılıyor; sade açıklama, ajan brifi ve bağlı işler şablonda yer alıyor. (#103)
- Yerel kapıya driftlint eklendi; inceleme girdileri, başarısız çalıştırma ve bir defalık tur sıfırlama kuralları güncel akışa uyarlandı. (#47, issue #53)
- Sadakat raporunda hesap tarihi kaynak tarihinden ayrıldı; X arşivi atıfları ve çift Z adaylarının yorum sınırları açıklandı. (#61)
- Issue ve PR yolları belirlendi; gerekçeli, yalnız izinli belge dosyalarını değiştiren PR'lar issue olmadan kabul ediliyor. (#79)
- Ruff B905 ve B023 kontrolleri açıldı; `zip` uzunluk tercihleri ve döngü içi fonksiyonların kullandığı değerler açıkça bağlandı. (#74)
- GitHub deposunun adı tansu oldu; eski adres yeni adrese yönleniyor.
- Değişiklik başlıkları kapattıkları işin numarasıyla başlıyor; otomatik kabul denetimi bu eşleşmeyi kontrol ediyor.
- Açık işler, çalışma sırasına göre numaralanmış ve sağlayacakları sonuçla adlandırılmış sürüm hedeflerine bağlandı.
- Değişiklik açıklamaları kısaldı ve Türkçe yönergeler içeriyor. Otomatik kabul denetimi 15 kuraldan 6 kurala indi.
- Bilgisayarda yalnız değişen işle ilgili testler çalışıyor. Tüm testler GitHub'da çalışıyor.
- GitHub'daki otomatik kontroller yalnız Windows'ta çalışıyor.

### Düzeltildi

- Evren indirmesinde kapanan şirket kanıtı yayın öncesinde manifeste katılıyor; listelenmiş eksik dosyalar veri hatası veriyor. Eski görüntüler kendi manifestleriyle korunuyor. (#133)
- Kod sürümü proje kökünden, kalıtılan Git yönlendirmelerinden bağımsız doğrulanıyor; Git hatasında koşu hesabı ve Tansu sınamasının ayar aktarımı başlamıyor, doğrudan sonuç yazımı duruyor. (#132)

- Tamamlanma denetimi, Windows üzerinde Türkçe kural uyarılarını eksiksiz yazıyor; eksik kabul kutusu yine reddediliyor. (#118)
- Strateji kataloğundaki kural ayarları ve sabitler kod parmak izinin kapsamına alındı. (#83)
- Veri katmanının motor katmanına ters bağımlılığı kaldırıldı; karantina süresinin tek sahibi veri katmanı oldu, değer ve davranış korundu. (#85)

### Kaldırıldı

- Eski çalışma notları ve arşivler GitHub'dan çıkarıldı. Bilgisayarda ve git geçmişinde kalıyor.

## [0.1.0] — 2026-10-17

GitHub'daki sürüm etiketi: `v0.1`.

### Eklendi

- İşler GitHub'da açılıyor ve değişikliklerle bağlanıyor. Birleştirme ilgili işi kapatıyor. (#75, issue #49)
- Sıkışma yöntemine arz bölgesi ve üçgen girişleri, düşüş süzgeci, gösterge teyitleri, yarı satış kuralları ve 24 varyant eklendi. (#35)
- Tansu'nun yöntemiyle geçmiş sınama ve Sınama sekmesi eklendi. Geçerli fiyat günü ile dönemin son günü ayrı ele alınıyor. (#36)
- X arşivinden dört partide toplam 400 not kural belgelerine işlendi. (#30, #31, #32, #33)
- Değişmemesi gereken kurallar testlerle korunuyor. Belge atıfları, kayıtlar, belge sahipleri ve kaynak kapsamı otomatik denetleniyor. (#4, #6, #23, #24)

### Değişti

- Sözlük, tasarım ve kural belgeleri birbiriyle ve kaynaklarla hizalandı. Tekrarlanan bilgiler kendi sahibi olan belgeye bağlandı. (#3, #5, #7, #8, #9, #10, #29)
- Kod standartları ortak kaynağa bağlandı. Otomatik kod ve biçim kontrolleri ile Windows testleri eklendi. (#2, #11, #12, #37)
- Ajan görevleri, belge yerleri ve iş akışları düzenlendi. Eski fabrika işleri donduruldu. (#19, #20, #21, #22, #25, #27, #38, #39)
- İnceleme kararı incelenen değişiklik kaydına bağlandı. İnceleme turları, başarısızlık ölçütleri ve test kapısı kuralları netleşti. (#34, #40, #41)
- Beceri seçimi ölçüldü ve sonuçları kaydedildi. Ölçüm oturumlarının araç kullanım sınırları netleşti. (#28)

### Düzeltildi

- Rapor metinleri, çıktı biçimleri, yıllık fazla getiri ve deneme sayımı tasarıma uyarlandı. Kural kimliğinin kapsadığı bilgiler belgelendi. (#13, #17, #18)
- Yeni rapor eski raporun üstüne yazmıyor. Bir hissenin yalnız bir gün geçerli olduğu durum üç hesaplama bölümünde de ele alınıyor. (#14)
- Önceki günün her kartındaki hisse indiriliyor. Bozulma nedenleri ayrı etiketleniyor ve veri kopyaları silinmiyor. (#15)
- Şirket olaylarının tarih eşleştirmesi düzeltildi. Bozuk satır, karantina ve piyasa durumu davranışları tasarıma uyarlandı. (#16)

### Kaldırıldı

- Kurulu zamanlanmış görevler kaldırıldı. Görev tanımları yeniden kurulum için depoda tutuluyor. (#26)

[Yayımlanmamış]: https://github.com/zPfizer/tansu/compare/v0.1...HEAD
[0.1.0]: https://github.com/zPfizer/tansu/releases/tag/v0.1
