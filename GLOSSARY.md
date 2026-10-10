# Sözlük

Sistemin dili. Kurallar Tansu'dan esinlenen yorumlardır; Tansu'nun kendi sistemi değildir. Bu dosya terimin ne
olduğunu söyler; sayı, formül ve işleyiş, atıf verilen bölümdedir (TASARIM = `docs/TASARIM.md`, KURALLAR =
`docs/KURALLAR.md`).

## Kaynak

| Terim | Anlam |
|---|---|
| Birinci el | Tansu'nun kendi aracının görsel çıktısı: başlık, etiket, tablo, kod. Nasıl kullanıldığı KURALLAR'dadır. |
| İkinci el | Tansu'dan aktarılan ama onun aracından çıkmayan metin: notlardaki özet ya da aktarılan tweet. |
| NotebookLM | Tansu'nun paylaştığı ama kendi aracından çıkmayan infografik. |
| YORUM | Tansu'nun fikir ya da değer vermediği bir noktada bizim belirlediğimiz değer ya da kural (ör. Tansu'nun açıklamadığı parametre). Tansu'nun fikri olan noktada YORUM geçerli değildir; Tansu'ya uyulamıyorsa bu "uygulanamaz" diye nedeniyle yazılır. Deneme sayımına etkisi KURALLAR'dadır. |
| Sadakat kontrolü | Bir kuralın Tansu'nun kendi ekranındaki rakamları yeniden üretip üretmediğinin denetimi. Getiriye bakmaz. Sonucu sıkı toleransla eşleşme ya da gevşek bantla yakınlık olarak iki düzeyde verir; değerleri KURALLAR §4'tedir. |
| Hazırlık (H / K / X) | Bir kuralın kaynaktan ne kadar kodlanabildiği: H az YORUM'la, K önemli YORUM'la, X kodlanamaz. Kaynağın birinci ya da ikinci el olmasından ayrıdır. Ailenin durumundan ayrıdır (KURALLAR §2). |

## Veri

| Terim | Anlam |
|---|---|
| Fiyat | Bir hissenin günlük yüksek, düşük, kapanış, ağırlıklı ortalama ve hacim serisi. |
| Hacim | Bir günde işlem gören tutar. Projede TL işlem hacmidir, adet değil. Likidite hesabı TASARIM §5.4'tedir. |
| İşlem günü | Borsanın açık olduğu gün; ortak takvim endeks günlerinden çıkar (TASARIM §4). Bir hissenin işlem günü, o hissenin hacimle işlem gördüğü gündür (TASARIM §5.1). Hangi hesabın hangisini saydığı TASARIM'dadır. |
| İşlem durdurma | Bir hissenin işlem görmediği gün ya da dönem. Uzun durdurma hissenin kapanması sayılır (TASARIM §5.2). |
| Hissenin kapanması | Bir hissenin borsada işleminin sona ermesi. Açık pozisyonun nasıl kapandığı TASARIM §5.2'dedir. |
| Takvim günü | Hafta sonu ve tatil dahil her gün. Faiz ve düşüşte kalma süresi takvim günüyle sayılır (TASARIM §5.6, §5.12). |
| Ham fiyat | O gün borsada oluşan fiyat. |
| Düzeltilmiş fiyat | Şirket olaylarının etkisi geçmişe yayılarak tek ölçeğe getirilmiş fiyat. Hangi hesabın hangi seriyi kullandığı TASARIM §5.1'dedir. |
| Şirket olayı | Fiyatı mekanik olarak değiştiren olay: bedelsiz, bölünme, bedelli, temettü. |
| Olay çarpanı | Şirket olayının fiyat ölçeğini ne kadar değiştirdiğini gösteren katsayı (TASARIM §5.1). |
| Olay denetimi | Olay çarpanıyla ham fiyattan bulunan değerin düzeltilmiş fiyatla tutarlı olup olmadığının kontrolü (TASARIM §5.1). |
| Mum | Bir hissenin bir günlük fiyat kaydı. Tansu'da açılış, yüksek, düşük ve kapanıştan oluşur. Projede açılış yoktur (uygulanamaz: veride yok); satır önceden hesaplanmış göstergeleri de taşır. Sütunları TASARIM §4'tedir. |
| Anlık görüntü | Bir indirmenin değişmez kopyası; kimliği veri sürümüdür. Tam anlık görüntü sınamada, günlük anlık görüntü günlük koşuda kullanılır; içerikleri TASARIM §4 ve §6'dadır. |
| Manifest | Anlık görüntünün dosyalarını ve her dosyanın parmak izini tutan kayıt. Uyuşmazlık koşuyu durdurur (TASARIM §4, §5.11). |
| NaN | Eksik sayısal değer. Sıfırdan ayrıdır; hangi alanda bulunduğuna göre karantina ya da eksik gün kararı TASARIM §5.13'tedir. |
| Eksik gün | Verisi olmayan gün. İleri doldurulmaz, yani önceki günün değeri o güne kopyalanmaz; o gün sinyal ve giriş yoktur. Açık pozisyonun son kapanışla değerlenmesi veri doldurmak değildir (TASARIM §5.1). |
| Isınma | Hissenin verisi göstergeleri dolduracak kadar uzamadan sinyal verilmeyen ilk dönem. Süreleri TASARIM §5.1'dedir. |
| Fiyat limiti | Bir hissenin bir günde çıkabileceği en yüksek (tavan) ve inebileceği en düşük (taban) fiyat. Oranı TASARIM §5.1'dedir. |
| Fiyat adımı | Fiyatın değişebileceği en küçük tutar. Tablosu TASARIM §5.1'dedir. |
| Kilitli gün | Limit kontrolüne göre kapanışı tavanda ya da tabanda sayılan gün: tavanda giriş yok, tabanda çıkış ertesi güne kalır. Tolerans ve daha dar duyarlılık tanımı TASARIM §5.3'tedir. |
| Satır ihlali | Tek bir fiyat satırının kendi içinde tutarsız ya da bozuk olması. Hisse-günü karantinaya sokar (TASARIM §5.13). |
| Yapısal ihlal | Kaynak yanıtı düzenlendikten sonra serinin hâlâ bozuk sırada ya da farklı fiyatlı tekrar eden günle kalması. Koşuyu durdurur (TASARIM §5.13). |
| Karantina | Veri ihlali yüzünden yeni girişe kapatılan hisse-dönem; açık pozisyon kapanır, fiyat yamanmaz. Tetikleyiciler TASARIM §5.1 ve §5.13'tedir. |
| Kaynak günü hatası | Bir günün verisinin kaynakta toplu bozuk gelmesi. O gün hisseler karantinaya girmez; gün eksik gün sayılır (TASARIM §5.13). |
| Veri kapısı | Bir koşunun veriyi kullanmadan önce geçmesi gereken kontrol. Geçmezse kart üretilmez (TASARIM §5.13). |

## Evren ve piyasa

| Terim | Anlam |
|---|---|
| Evren | Belli bir ayda yeni giriş için taranabilen hisseler. İndirilen bütün hisselerden dardır. Seçim kuralı TASARIM §5.2'dedir. |
| Hayatta kalan yanlılığı | Bugün var olan hisselere bakarak geçmişi iyimser görme hatası. Bu projedeki kaynakları ve etkisi TASARIM §5.2'dedir. |
| Piyasa durumu | Endeksin o günkü durum etiketi. Yeni girişi durdurmaz (YORUM: Tansu'nun şok filtresi yeni alımı durdurur, o ayrı bir kuraldır ve ilk sürümde yoktur); K1 (b) karşılaştırmasında günleri eşlemek için kullanılır (TASARIM §5.7, §6). |

## Kurallar ve sinyaller

| Terim | Anlam |
|---|---|
| Aile | Bir kurulum türünün kuralı. Fiyattan sinyal günlerini çıkarır (KURALLAR §3). İlk sürümün aileleri TASARIM §3'tedir; katalogdaki öteki kurulumların (AB=CD, BOS, FVG, kanal vb.) adları ve kaynakları KURALLAR §2'dedir, terimleri bir aile sınanmaya alınınca buraya girer. |
| Sinyal | Ailenin kuralının sağlandığı gün; günün kapanışındadır. |
| Düşen sinyal | Giriş günü olmadığı ya da tavanda kilitli olduğu için girilemeyen sinyal; raporda "iptal" diye sayılır. Hangi durumda düştüğü TASARIM §5.3'tedir. |
| Reddedilen sinyal | Pozisyon yeri, nakit ya da boyut sınırı yüzünden girilemeyen sinyal. İşlem sayısına girmez; raporda ayrı sayılır (TASARIM §5.3, §5.6). |
| ATR | Ortalama gerçek aralık: bir hissenin günlük fiyat oynaklığı. Stop mesafesinin birimidir (TASARIM §5.5). |
| EMA | Üssel hareketli ortalama: bir veri serisinin yakın günlere daha çok ağırlık veren ortalaması. Bizde fiyata uygulanır; Tansu başka serilere de uygular. |
| SMA | Basit hareketli ortalama: bir veri serisinin son n gününün eşit ağırlıklı ortalaması. |
| Gerçek aralık | Bir günün fiyat aralığı, önceki kapanışa göre oluşan boşluk dahil. ATR'nin girdisidir; ATR'nin ayarları TASARIM §5.5'tedir. |
| Wilder ortalaması | Bizim ATR hesabında seçtiğimiz yumuşatma (YORUM; Tansu yumuşatma türünü vermez): EMA'ya benzer ama ağırlığı daha yavaş azalan ortalama. EMA ve SMA'dan ayrıdır; başlangıcı TASARIM §5.5'tedir. |
| EMA sıkışması kırılımı | İlk sürümün tek hisse ailesi: seçili EMA'lar birbirine yaklaştıktan sonra kapanışın sıkışma dönemindeki en yükseği aşması (KURALLAR §3). Sıkışma Tansu'nundur; kırılımla giriş YORUM'dur: Tansu'nun ön sinyali sıkışma sürerken çıkar. |
| Sıkışma oranı | Seçili EMA'ların birbirine ne kadar yakın olduğunu ölçen oran. EMA listesi ve formülü KURALLAR §3'tedir. |
| Sıkışma dönemi | Sıkışma oranının eşiği aşmadığı art arda günler (KURALLAR §3). |
| Giriş penceresi | Sıkışma dönemi bittikten sonra giriş sinyalinin oluşabileceği dönem (YORUM). Alımın zamanı KURALLAR §3'tedir. |
| Çift rotasyonu | İlk sürümün çift ailesi: bir çiftin iki hissesi arasında Z'ye göre ilk girişten sonra geçiş yapmak; ilk girişe kadar nakitte durulur (KURALLAR §3). |
| Bacak | Bir çiftin iki hissesinden biri. |
| Geçiş | Çiftte tutulan bacağı satıp öteki bacağı almak (TASARIM §5.6). |
| Z, ΔZ | Çiftte iki hissenin fark serisinin ortalamasından kaç standart sapma uzakta olduğu (Z) ve bunun bir günlük değişimi (ΔZ). Eşik ve ΔZ Tansu'nundur; fark serisi olarak logaritmik fiyat oranı YORUM'dur, Tansu'nun formülü üretilemedi. Z'nin hesabı KURALLAR §3'te, ΔZ'nin tanımı KURALLAR §2'dedir. |
| Z penceresi | Z'nin ortalama ve sapmasının hesaplandığı gün sayısı (KURALLAR §3). Seçim penceresinden bağımsızdır. |
| ddof | Standart sapma hesabında bölenden düşülen sayı. Z'nin değerini, dolayısıyla eşiğin aşılıp aşılmadığını etkiler; seçilen değer TASARIM §5.6'dadır. |
| Eşbütünleşme | Tek başına durağan olmayan iki fiyat serisinin doğrusal bir birleşiminin durağan olması: aradaki fark kalıcı olarak ortalamaya döner. Korelasyondan ayrıdır. Çift seçiminin ölçütüdür (TASARIM §5.6). |
| Engle–Granger | Eşbütünleşmeyi sınayan yöntem: iki seri arasındaki farkın kalıcı olarak ortalamaya dönüp dönmediğine bakar. Ayarları TASARIM §5.6'dadır. |
| AIC | Engle–Granger testinde kaç günlük gecikmenin kullanılacağını seçen ölçüt (TASARIM §5.6). |
| OLS | En küçük kareler: iki seri arasındaki eğimi, hataların karesini en aza indirerek bulan yöntem. β bununla hesaplanır (TASARIM §5.6). Logaritmik fiyata OLS uygulamak YORUM'dur: Tansu Beta'yı gösterir, hesabını vermez. |
| Açgözlü seçim | Adayları sıraya koyup her adımda sınırlara uyan ilk adayı alan, önceki seçimi değiştirmeyen yöntem. Çift seçiminde kullanılır; sıra ve sınırlar TASARIM §5.6'dadır. |
| Seçim penceresi | Çift seçiminde eşbütünleşmenin ölçüldüğü geçmiş dönem (TASARIM §5.6). |
| β | Çift seçiminde bir hissenin logaritmik fiyatının ötekininkine göre ne kadar hareket ettiğini gösteren eğim. Hesabı ve eleme kuralı TASARIM §5.6'dadır. |

## İşlem ve risk

| Terim | Anlam |
|---|---|
| İşlem fiyatı (AOF) | Bir günün ağırlıklı ortalama fiyatı. Olağan giriş ve çıkış, sinyalden sonraki günün AOF'undan sayılır (YORUM: Tansu ertesi gün açılışını kullanır, kaynağımızda açılış yok); stop ve veri sonu istisnaları TASARIM §5.3'tedir. |
| Adım | Bir pozisyonun bir günlük güncellemesi: (pozisyon, bugünkü mum) → pozisyon. Sınama ve günlük koşu aynı Adım'ı kullanır (TASARIM §4). |
| Motor | Sinyalleri Adım'dan geçirip işlemlere çeviren parça (TASARIM §4). |
| Simülatör | İşlemleri bölmenin kurallarıyla sermayeye uygulayıp günlük özkaynak eğrisini üreten parça (TASARIM §4, §5.6). |
| İşlem | Tek hisse bölmesinde bir pozisyonun girişten çıkışa kadarki tamamı. Çift bölmesinde işlem tutuş dönemidir (TASARIM §5.3, §5.6). Örneklemin neyle sayıldığı "Örneklem şartı" maddesindedir. |
| Adet, lot | Alınan hisse sayısı. Lot alınabilen en küçük birimdir; adetin tam lota aşağı yuvarlanması YORUM'dur (TASARIM §5.6). |
| Dolum | Bir alım ya da satımın gerçekleşmesi: hangi gün, hangi fiyattan. Kuralları TASARIM §5.3 ve §5.13'tedir. |
| Özkaynak | Portföyün toplam güncel değeri: nakit ve açık pozisyonlar. Hesabı TASARIM §5.6'dadır. |
| Maruziyet | Özkaynağın hisselerde duran payı. Ölçümü TASARIM §5.7'dedir. |
| Masraf | Alış ve satışta ödenen komisyon, BSMV (aracı kurum komisyonu üstündeki banka ve sigorta muameleleri vergisi) ve kayma (emrin beklenen fiyattan kötü dolması). Gelir vergisi masrafa girmez. Oranları TASARIM §5.4'tedir. |
| Medyan | Sıralanmış değerlerin ortasındaki değer. Uç değerlerden ortalama kadar etkilenmez. |
| Likidite | Bir hissede istenen fiyattan rahat girip çıkabilme. Ölçüsü olarak yakın günlerdeki medyan TL işlem tutarı YORUM'dur. Aynı gün yer yetmezse önce en likit hisse alınır (TASARIM §5.4, §5.6). |
| Likidite sınırı | Bir pozisyonun, hissenin yakın günlerdeki işlem tutarının belli bir payını geçemeyeceği sınır (YORUM; TASARIM §5.4). |
| Pozisyon tavanı | Tek pozisyonun özkaynakta alabileceği en büyük pay (TASARIM §5.6). |
| Bağlayıcı sınır | Boyutlama sınırlarından adedi fiilen belirleyen en küçüğü. Sınırlar ve eşitlikteki sıra TASARIM §5.6'dadır; rapor her sınırın bağlama oranını yazar. |
| Bölme | Bir ailenin kendi sermayesi ve boyutlama kuralı. Tek hisse bölmesi risk paketiyle, çift bölmesi çift paylarıyla boyutlanır (TASARIM §5.6). |
| Risk paketi | Tek hisse bölmesinin boyutlama ve çıkış kuralları: işlem başı risk, pozisyon tavanı, likidite sınırı, stop ve bozulma çıkışı (TASARIM §5.5–5.6). |
| Stop | Zararı kesen seviye; gün içinde değerse çıkılır. Kaynaktaki adı "acil durum stopu"dur (NotebookLM infografiği). Mesafesi TASARIM §5.5'tedir. |
| Bozulma | Kapanışın uzun dönem ortalamasının altına inmesi; kaynaktaki adı "gün sonu stopu"dur (NotebookLM infografiği, Tansu paylaştı). Ertesi gün çıkılması YORUM'dur. Ortalama TASARIM §5.5'tedir. |
| Hedef | Üç anlamı vardır. Kâr hedefi: kârı alan seviye; yalnız Tansu verdiyse kullanılır, ilk sürümün ailelerinde yoktur (TASARIM §5.5). Formasyon hedefi (D): Tansu'nun harmonik kurulumlarında formasyonun tamamlandığı ve girişin yapılabildiği seviye (KURALLAR §2). Çift rotasyonunda geçilecek bacak (TASARIM §5.6). |
| R | Hisse başına planlanan risk tutarı. Hesabı TASARIM §5.3'tedir. |
| Planlanan risk | Stop değerse pozisyonun tamamında kaybedilecek tutar. Hesabı TASARIM §5.3'tedir. |
| Fiili risk | Planlanan riskin özkaynağa oranı. |
| Gerçekleşen kayıp | İşlemde gerçekten kaybedilen tutar. Boşluklu stopta planlanan riskten büyük olabilir (TASARIM §5.3). |
| Çift | Aralarında eşbütünleşme olan iki hisse. Aynı sektör şartı bizim seçim kuralımızdır (YORUM); Tansu farklı sektörden çift de kullanır (TASARIM §5.6). |
| Çift payı | Çift bölmesinde bir çifte ayrılan sermaye. Nakitte ya da iki bacaktan birinde durur; ne zaman hangisinde olduğu TASARIM §5.6'dadır. |
| Tutuş dönemi | Çift bölmesinde bir bacağın alımından satımına geçen süre. Bölmede "işlem" budur; bitiş nedenleri TASARIM §5.6'dadır. |
| 50/50 tanısal | Seçilen çiftlerin iki bacağına eşit dağıtılıp tutulduğu karşılaştırma. Yalnız bilgi; kabul kararına girmez. Takvimi TASARIM §5.6'dadır. |

## Kart ve günlük koşu

| Terim | Anlam |
|---|---|
| Koşu | Bir çalıştırma. Günlük koşu kartları üretir (TASARIM §6). Sınama koşusu geçmiş veride kuralı sınar: resmi koşu temiz koda bağlanır ve kabul kararına girer, geliştirme koşusu girmez (TASARIM §5.11). |
| Temiz / kirli ağaç | Depoda commit edilmemiş değişiklik yoksa ağaç temizdir, varsa kirlidir. Resmi koşu kirli ağaçta yapılmaz; denetimin kapsamı TASARIM §5.11'dedir. |
| Günlük koşu durumu | Günlük koşunun sonucu: TAMAM, SORUNLU, VERİ YOK, BUGÜN ÇUBUK YOK. Levent yalnız buna bakar. Ne zaman hangisinin yazıldığı TASARIM §6'dadır. |
| Kart | Bir sinyalin günlük listedeki hâli: hisse, aile, referans fiyat, stop, büyüklük, fiili risk, durum, kanıt satırı (TASARIM §6). |
| Referans fiyat | Sinyal günü kapanışı. Kartta giriş yerine gösterilir; gerçek giriş ertesi günün işlem fiyatıdır. |
| Kart durumu | AKTİF (giriş bekliyor ya da pozisyon açık), STOP (stop değdi), BOZULDU (bozulma, karantina çıkışı ya da giriş iptali) (TASARIM §6). Adlar Tansu'nun formasyon etiketlerinden alındı; pozisyona bağlanan bu anlamları YORUM'dur. |
| Kanıt satırı | Kartta ailenin sınama sonucunu özetleyen satır (TASARIM §6). |

## Sınama ve kabul

| Terim | Anlam |
|---|---|
| Tohum | Rastgele seçimin başlangıç değeri. Aynı tohum ve aynı anlık görüntü aynı sonucu verir (TASARIM §5.11). |
| Parmak izi (hash) | Bir dosyanın ya da verinin içeriğinden hesaplanan kısa kimlik; içerik değişirse değişir. Kod hash'i kodun yapısından hesaplanır, yorum ve boşluk onu değiştirmez. Kod hash'i ve parametre hash'i kural kaydının parmak izleridir; kapsamı TASARIM §5.8'dedir. |
| Kural kaydı | Kuralın, parametrelerinin ve kodunun parmak izi. Sonraki her değişiklik yeni denemedir (TASARIM §5.8). |
| Deneme günlüğü | Koşuların, kural kayıtlarının ve aile durumlarının yazıldığı, yalnız eklenen günlük. Deneme sayısı buradan sayılır (TASARIM §5.11). |
| Deneme sayısı (m) | Holm düzeltmesinde sayılan resmi deneme sayısı. Neyin sayıldığı TASARIM §5.11'dedir. Aile durumu olan "Deneme"den ve tekrar sayısından (B) ayrıdır. |
| Tekrar sayısı (B) | K1'de rastgele kuralın kaç kez çekildiği. Deneme sayısı m büyüdükçe artar; formülü TASARIM §5.7'dedir. |
| Kanıt | Bir ailenin geçmiş veride, masraflar dahil, karşılaştırmalı sınama sonucu. |
| Fazla getiri | Kuralın, karşılaştırma sepetine göre ne kadar iyi ya da kötü olduğu. İşlem ve portföy düzeyinde iki hesabı TASARIM §5.7'dedir. |
| Ön şartlı gün havuzu | Bir karşılaştırmada rastgele girişin seçilebileceği günler. K1'in her türünün ve ek kolun havuzu ayrıdır; şartları TASARIM §5.7'dedir. |
| Rastgele kural | Karşılaştırma türünün uygunluk şartlarını sağlayan günlerden rastgele seçilen girişler. Şartlar TASARIM §5.7'dedir. |
| K1 | Rastgele kuralla karşılaştırma: aynı simülatörden geçen rastgele girişler. İki türü ve p değeri TASARIM §5.7'dedir. |
| Ek kol | EMA sıkışması için sıkışmasız aynı kırılımla yapılan ek karşılaştırma. Yalnız rapordur; aile p'sine girmez (TASARIM §5.7). |
| K2 | Aynı evrenin eşit ağırlıklı sepetiyle karşılaştırma; sepet kuralın maruziyeti kadar yatırımdadır, kalanı faiz kazanır (TASARIM §5.7). |
| K3 | Faizle karşılaştırma: boştaki nakit faiz kazandığı için portföy sonucu zaten faize karşı okunur (TASARIM §5.7). |
| p değeri | Bir sonucun şansla çıkma olasılığının ölçüsü. K1 p değeri: rastgele sınama tekrarlarının gerçek kural kadar iyi ortalama sonuç verip vermediğine dayanan ölçü; formülü TASARIM §5.7'dedir. Eşbütünleşme p'si: eşbütünleşme testinin p değeri; küçükse iki hisse arasındaki fark kalıcı olarak ortalamaya dönüyor sayılır. Çift seçiminde kullanılır (TASARIM §5.6). Kabul kararı p'ye tek başına bağlı değildir (TASARIM §5.12). |
| Holm | Çoklu deneme düzeltmesi: birden çok kural denendikçe p eşiğini sıkılaştırır. Hangi p'nin girdiği TASARIM §5.11'dedir. |
| Güven aralığı | Ortalama fazla getiri tahmininin şans payından gelen belirsizlik aralığı. Yalnız rapordur (TASARIM §5.9). |
| Blok bootstrap | Günlük seriyi ardışık bloklar hâlinde yeniden örnekleyerek güven aralığı çıkarma yöntemi (TASARIM §5.9). |
| Örneklem şartı | Karar verilebilmesi için gereken en az sayı: tek hisse bölmesinde işlem ve sinyal günü, çift bölmesinde geçiş ve geçiş günü (TASARIM §5.9). |
| Saptanabilir en küçük etki (MDE) | Verinin şanstan ayırt edebileceği en küçük fazla getiri. İşlem başına çevrilip masrafla karşılaştırılır; bunun sonuca etkisi ve karar sırası TASARIM §5.9 ve §5.12'dedir. |
| İleri yürüme yılları | Tek sürekli koşunun yıllara kesilmiş parçaları. Parametreler sabittir; yalnız çift seçimi yıllık yenilenir (TASARIM §5.8). Tansu'nun parametre optimize eden walk-forward'undan ayrıdır. |
| Ayrılmış dönem | Kurallar yazılırken bakılmamış dönem: kural kaydından sonrası. |
| Sağlamlık ızgarası | Ailenin önceden yazılmış parametre hücreleri. Hepsi birlikte koşar; en iyisi seçilmez. Şartı TASARIM §5.10'dadır. |
| Pozitif hücre | Sağlamlık ızgarasında olumlu sayılan hücre. Ölçütü TASARIM §5.10'dadır. |
| Portföy kuralı | Aileden bağımsız ret kuralı: özkaynak eğrisi çok düşerse ya da düşüşte çok kalırsa aile reddedilir. Geçmesi kanıt değildir (TASARIM §5.12). |
| En büyük düşüş | Özkaynak eğrisinin bir zirveden sonraki en derin düşüşü (TASARIM §5.12). |
| Düşüşte kalma süresi | Özkaynak eğrisinin önceki zirvesinin altında kaldığı en uzun süre (TASARIM §5.12). |
| Boru hattı denetimi | Sınama düzeneğinin kendi denetimi: kuralın getiri öngörmediği sentetik veride yanlış kabul oranı ve gömülü etkide güç (TASARIM §5.12). |
| Yanlış kabul | Getiri öngörmeyen sentetik veride ailenin kabul ölçütlerinin bir kısmından geçmesi. Kâğıt'a geçmekle aynı değildir; hangi ölçütlerin arandığı TASARIM §5.12'dedir. |
| Güç | İki anlamı vardır. Boru hattı denetiminde: gerçek etkisi olan sentetik veride ailenin aynı ölçütlerden geçme oranı (TASARIM §5.12). MDE hesabında: gerçek bir etkinin istatistiksel olarak yakalanma olasılığı (TASARIM §5.9). |
| Geçti / Geçmedi | Bir kabul ölçütünün ya da ailenin genel sonucu. Aile durumundan ayrıdır: genel sonuç Geçti olsa da durum Kâğıt olmayabilir. Karar sırası TASARIM §5.12'dedir. |
| Ölçülemedi | Kararı vermeye veri ya da süre yetmediği sonuç: örneklem dolmadı, etki ayırt edilemiyor ya da kâğıt üstü dönem başlamadı. "Geçmedi"den ayrıdır (TASARIM §5.12). |
| Deneme / Kâğıt / Canlı | Bir ailenin durumu. Deneme: henüz resmi kabul almadı, günlük kartlarda gösterilmez. Kâğıt: geçmiş sınamayı geçti, para konmadan izlenir. Canlı: kâğıt üstü dönemi de geçti (TASARIM §5.12). Kâğıt ailesinin kart üretmesi TASARIM §6'dadır. |
| Kâğıt üstü dönem | Kâğıt ailenin para konmadan izlendiği dönem; TASARIM'da "kâğıt üstü canlı dönem". Canlı durumuyla aynı şey değildir. Süresi ve değerlendirmesi TASARIM §5.8'dedir. |
