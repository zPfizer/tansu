# Değişiklik günlüğü

TANSU'nun önemli değişiklikleri bu dosyada, en yenisi üstte olacak biçimde yer alır.
Düzen [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
sürüm numaraları [Semantic Versioning](https://semver.org/spec/v2.0.0.html) biçimini izler.

## [Yayımlanmamış]

### Eklendi

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
- Kod incelemesi artık OpenAI Codex eklentisiyle yapılıyor.

### Düzeltildi

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
