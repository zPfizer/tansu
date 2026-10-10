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
| Sadakat kontrolü | Bir kuralın kaynak ekrandaki rakamları yeniden üretip üretmediğinin denetimi. Sonucu iki düzeydir: sıkı toleransla "üretti" ya da yalnız gevşek bantta yakınlık; gevşek bant üretim sayılmaz (KURALLAR §4). |
| Hazırlık (H / K / X) | Bir kuralın kaynaktan ne kadar kodlanabildiği: H birinci elden ve az YORUM'la, K kısmen ve önemli YORUM'la, X kodlanamaz. Ailenin durumundan ayrıdır (KURALLAR §2). |

## Veri

| Terim | Anlam |
|---|---|
| Fiyat | Bir hissenin günlük yüksek, düşük, kapanış, ağırlıklı ortalama ve hacim serisi. |
| Hacim | Bir günde işlem gören TL tutarıdır, hisse adedi değildir (TASARIM §5.4). |
| İşlem günü | Borsanın açık olduğu gün. Bir hissenin işlem günü, o hissenin hacimle işlem gördüğü gündür (TASARIM §4, §5.1). |
| İşlem durdurma | Bir hissenin işlem görmediği gün ya da dönem (TASARIM §5.2). |
| Hissenin kapanması | Bir hissenin borsada işleminin sona ermesi (TASARIM §5.2). |
| Takvim günü | Hafta sonu ve tatil dahil her gün (TASARIM §5.6, §5.12). |
| Ham fiyat | O gün borsada oluşan fiyat. |
| Düzeltilmiş fiyat | Şirket olaylarının etkisi geçmişe yayılarak tek ölçeğe getirilmiş fiyat (TASARIM §5.1). |
| Şirket olayı | Fiyatı mekanik olarak değiştiren olay: bedelsiz, bölünme, bedelli, temettü. |
| Olay çarpanı | Şirket olayının fiyat ölçeğini ne kadar değiştirdiğini gösteren katsayı (TASARIM §5.1). |
| Olay denetimi | Olay çarpanıyla ham fiyattan bulunan değerin düzeltilmiş fiyatla tutarlı olup olmadığının kontrolü (TASARIM §5.1). |
| Mum | Bir hissenin bir günlük fiyat kaydı (TASARIM §4). |
| Anlık görüntü | Bir indirmenin değişmez kopyası. Kimliği veri sürümüdür (TASARIM §4, §6). |
| Manifest | Anlık görüntünün dosyalarını ve her dosyanın parmak izini içeren kayıt (TASARIM §4, §5.11). |
| NaN | Eksik sayısal değer. Sıfırdan ayrıdır (TASARIM §5.13). |
| Eksik gün | Verisi olmayan gün (TASARIM §5.1). |
| Isınma | Göstergeler için gerekli geçmiş verinin biriktiği başlangıç dönemi (TASARIM §5.1). |
| Fiyat limiti | Bir hissenin bir günde çıkabileceği en yüksek (tavan) ve inebileceği en düşük (taban) fiyat (TASARIM §5.1). |
| Fiyat adımı | Fiyatın değişebileceği en küçük tutar (TASARIM §5.1). |
| Kilitli gün | Kapanışı tavanda ya da tabanda sayılan gün (TASARIM §5.3). |
| Satır ihlali | Tek bir fiyat satırının kendi içinde tutarsız ya da bozuk olması (TASARIM §5.13). |
| Yapısal ihlal | Düzenlenmiş veri serisinde günlerin yanlış sırada olması ya da aynı günün farklı fiyatlarla tekrarlanması (TASARIM §5.13). |
| Hisse-gün | Bir hissenin bir günlük gözlemi. Üye hisse-gün, hissenin o ayın evreninde olduğu gündür; veri kapısı oranları bu birimle sayılır (TASARIM §5.13). |
| Karantina | Veri ihlali nedeniyle bir hisseye belirli bir dönem için konan yeni giriş kısıtı (TASARIM §5.1, §5.13). |
| Kaynak günü hatası | Bir günün verisinin kaynakta toplu bozuk gelmesi (TASARIM §5.13). |
| Veri kapısı | Bir koşunun veriyi kullanmadan önce geçmesi gereken kontrol (TASARIM §5.13). |

## Evren ve piyasa

| Terim | Anlam |
|---|---|
| Evren | Belli bir ayda yeni giriş için taranabilen hisseler (TASARIM §5.2). |
| Hayatta kalan yanlılığı | Bugün var olan hisselere bakarak geçmişi iyimser görme hatası (TASARIM §5.2). |
| Piyasa durumu | Endeksin o günkü durum etiketi (TASARIM §5.7, §6). |

## Kurallar ve sinyaller

| Terim | Anlam |
|---|---|
| Aile | Bir kurulum türünü tanımlayan kural (KURALLAR §2–3, TASARIM §3). |
| Sinyal | Ailenin kuralının sağlandığı gün. |
| Düşen sinyal | Giriş günü olmadığı ya da tavanda kilitli olduğu için girilemeyen sinyal (TASARIM §5.3). |
| Reddedilen sinyal | Pozisyon yeri, nakit ya da boyut sınırı yüzünden girilemeyen sinyal (TASARIM §5.3, §5.6). |
| ATR | Ortalama gerçek aralık: bir hissenin günlük fiyat oynaklığı (TASARIM §5.5). |
| EMA | Üssel hareketli ortalama: bir veri serisinin yakın günlere daha çok ağırlık veren ortalaması. |
| SMA | Basit hareketli ortalama: bir veri serisinin son n gününün eşit ağırlıklı ortalaması. |
| Gerçek aralık | Bir günün fiyat aralığı, önceki kapanışa göre oluşan boşluk dahil (TASARIM §5.5). |
| Wilder ortalaması | EMA'ya benzer ama ağırlığı daha yavaş azalan ortalama. EMA ve SMA'dan ayrıdır (TASARIM §5.5). |
| EMA sıkışması kırılımı | Seçili EMA'lar birbirine yaklaştıktan sonra kapanışın sıkışma dönemindeki en yükseği aşması (KURALLAR §3). |
| Sıkışma oranı | Seçili EMA'ların birbirine ne kadar yakın olduğunu ölçen oran (KURALLAR §3). |
| Sıkışma dönemi | Sıkışma oranının eşiği aşmadığı art arda günler (KURALLAR §3). |
| Giriş penceresi | Sıkışma dönemi bittikten sonra giriş sinyalinin oluşabileceği dönem (KURALLAR §3). |
| Çift rotasyonu | Bir çiftin iki hissesi arasında Z'ye göre geçiş yapmaya dayanan aile (KURALLAR §3). |
| Bacak | Bir çiftin iki hissesinden biri. |
| Geçiş | Çiftte tutulan bacağı satıp öteki bacağı almak (TASARIM §5.6). |
| Z, ΔZ | Z, çiftteki fark serisinin ortalamasından kaç standart sapma uzakta olduğudur. ΔZ, Z'nin bir günlük değişimidir (KURALLAR §2–3). |
| Z penceresi | Z'nin ortalama ve sapmasının hesaplandığı gün sayısı. Seçim penceresinden bağımsızdır (KURALLAR §3). |
| ddof | Standart sapma hesabında bölenden düşülen sayı (TASARIM §5.6). |
| Eşbütünleşme | Tek başına durağan olmayan iki fiyat serisinin doğrusal bir birleşiminin durağan olması. Korelasyondan ayrıdır (TASARIM §5.6). |
| Engle–Granger | İki seri arasındaki farkın kalıcı olarak ortalamaya dönüp dönmediğini sınayan eşbütünleşme testi (TASARIM §5.6). |
| AIC | İstatistiksel model seçimine yönelik ölçüt (TASARIM §5.6). |
| OLS | En küçük kareler: iki seri arasındaki eğimi, hataların karesini en aza indirerek bulan yöntem (TASARIM §5.6). |
| Açgözlü seçim | Adayları sıraya koyup her adımda sınırlara uyan ilk adayı alan, önceki seçimi değiştirmeyen yöntem (TASARIM §5.6). |
| Seçim penceresi | Çift seçiminde eşbütünleşmenin ölçüldüğü geçmiş dönem (TASARIM §5.6). |
| β | Çift seçiminde bir hissenin logaritmik fiyatının ötekininkine göre ne kadar hareket ettiğini gösteren eğim (TASARIM §5.6). |

## İşlem ve risk

| Terim | Anlam |
|---|---|
| İşlem fiyatı (AOF) | Bir günün ağırlıklı ortalama fiyatı (TASARIM §5.3). |
| Adım | Bir pozisyonun bir günlük güncellemesi (TASARIM §4). |
| Motor | Sinyalleri Adım'dan geçirip işlemlere çeviren parça (TASARIM §4). |
| Simülatör | İşlemleri bölmenin kurallarıyla sermayeye uygulayıp günlük özkaynak eğrisini üreten parça (TASARIM §4, §5.6). |
| İşlem | Tek hisse bölmesinde bir pozisyonun girişten çıkışa kadarki tamamı. Çift bölmesinde işlem tutuş dönemidir (TASARIM §5.3, §5.6). |
| Adet, lot | Adet, alınan hisse sayısıdır. Lot, alınabilen en küçük birimdir (TASARIM §5.6). |
| Dolum | Bir alım ya da satımın belirli bir gün ve fiyattan gerçekleşmesi (TASARIM §5.3, §5.13). |
| Özkaynak | Portföyün nakit ve açık pozisyonlardan oluşan toplam güncel değeri (TASARIM §5.6). |
| Maruziyet | Özkaynağın hisselerde duran payı (TASARIM §5.7). |
| Masraf | Alış ve satışın komisyon, BSMV (banka ve sigorta muameleleri vergisi) ve kayma maliyeti. Kayma, emrin beklenen fiyattan kötü dolmasıdır (TASARIM §5.4). |
| Medyan | Sıralanmış değerlerin ortasındaki değer. Uç değerlerden ortalama kadar etkilenmez. |
| Likidite | Bir hissede istenen fiyattan rahat girip çıkabilme (TASARIM §5.4, §5.6). |
| Likidite sınırı | Bir pozisyonun, hissenin yakın günlerdeki işlem tutarına göre alabileceği en büyük pay (TASARIM §5.4). |
| Pozisyon tavanı | Tek pozisyonun özkaynakta alabileceği en büyük pay (TASARIM §5.6). |
| Bağlayıcı sınır | Boyutlama sınırlarından adedi fiilen belirleyen en küçüğü (TASARIM §5.6). |
| Bölme | Bir ailenin kendi sermayesi ve boyutlama kuralı (TASARIM §5.6). |
| Risk paketi | Tek hisse bölmesinin boyutlama ve çıkış kuralları: işlem başı risk, pozisyon tavanı, likidite sınırı, stop ve bozulma çıkışı (TASARIM §5.5–5.6). |
| Stop | Zararı kesme seviyesi (TASARIM §5.5). |
| Bozulma | İki anlamı vardır. Projede: kapanışın uzun dönem ortalamasının altına inmesi, yani gün sonu stopu (TASARIM §5.5). Harmonik kaynaklarda: formasyonun geçersizleşmesi (KURALLAR §2). |
| Hedef | Kâr hedefi, kâr alma seviyesidir; formasyon hedefi (D), harmonik kurulumun tamamlanma seviyesidir. Çift rotasyonunda hedef, geçilecek bacaktır (TASARIM §5.5–5.6, KURALLAR §2). |
| R | Hisse başına planlanan risk tutarı (TASARIM §5.3). |
| Planlanan risk | Stop değerse pozisyonun tamamında kaybedilecek tutar (TASARIM §5.3). |
| Fiili risk | Planlanan riskin özkaynağa oranı. |
| Gerçekleşen kayıp | İşlemde gerçekten kaybedilen tutar (TASARIM §5.3). |
| Çift | Aralarında eşbütünleşme olan iki hisse (TASARIM §5.6). |
| Çift payı | Çift bölmesinde bir çifte ayrılan sermaye (TASARIM §5.6). |
| Tutuş dönemi | Çift bölmesinde bir bacağın alımından satımına geçen süre. Bu bölmede işlemin karşılığıdır (TASARIM §5.6). |
| 50/50 tanısal | Seçilen çiftlerin iki bacağına eşit dağılımla tutulan sepetin karşılaştırması (TASARIM §5.6). |

## Kart ve günlük koşu

| Terim | Anlam |
|---|---|
| Koşu | Sistemin bir kez çalıştırılması. Günlük koşu günlük verinin, sınama koşusu geçmiş veride bir kuralın değerlendirilmesidir. Sınama koşusu resmi ya da geliştirme koşusudur; yalnız resmi koşu kabul kararına girer (TASARIM §6, §5.11). |
| Temiz / kirli ağaç | Denetimin kapsadığı dosyalarda commit edilmemiş değişiklik yoksa ağaç temizdir, varsa kirlidir; kapsam TASARIM §5.11'dedir. |
| Günlük koşu durumu | Günlük koşunun sonuç etiketi: TAMAM, SORUNLU, VERİ YOK, BUGÜN ÇUBUK YOK (TASARIM §6). |
| Kart | Bir sinyalin günlük listedeki hâli: hisse, aile, referans fiyat, stop, büyüklük, fiili risk, durum, kanıt satırı (TASARIM §6). |
| Referans fiyat | Sinyal günü kapanışı. |
| Kart durumu | Kartın pozisyonla ilgili etiketi: AKTİF (giriş bekliyor ya da pozisyon açık), STOP (stop değdi), BOZULDU (bozulma, karantina çıkışı ya da giriş iptali) (TASARIM §6). |
| Kanıt satırı | Kartta ailenin sınama sonucunu özetleyen satır (TASARIM §6). |

## Sınama ve kabul

| Terim | Anlam |
|---|---|
| Tohum | Rastgele seçimin başlangıç değeri (TASARIM §5.11). |
| Parmak izi (hash) | Bir dosyanın ya da verinin içeriğinden hesaplanan kısa kimlik. Kod parmak izi kod yapısının, parametre parmak izi kural ayarlarının kimliğidir (TASARIM §5.8). |
| Kural kaydı | Kuralın, parametrelerinin ve kodunun parmak izi (TASARIM §5.8). |
| Deneme günlüğü | Koşuların, kural kayıtlarının ve aile durumlarının kaydı (TASARIM §5.11). |
| Deneme sayısı (m) | Holm düzeltmesinde sayılan resmi deneme sayısı. Aile durumu olan "Deneme"den ve tekrar sayısından (B) ayrıdır (TASARIM §5.11). |
| Tekrar sayısı (B) | K1'de rastgele kuralın kaç kez çekildiği (TASARIM §5.7). |
| Kanıt | Bir ailenin geçmiş veride, masraflar dahil, karşılaştırmalı sınama sonucu. |
| Fazla getiri | Kuralın getirisinin karşılaştırma sepetinin getirisinden farkı (TASARIM §5.7). |
| Ön şartlı gün havuzu | Bir karşılaştırmada rastgele girişin seçilebileceği günler (TASARIM §5.7). |
| Rastgele kural | Karşılaştırma türünün uygunluk şartlarını sağlayan günlerden rastgele seçilen girişler (TASARIM §5.7). |
| K1 | Rastgele girişlere dayanan kuralla karşılaştırma (TASARIM §5.7). |
| Ek kol | EMA sıkışması için sıkışmasız aynı kırılımla yapılan ek karşılaştırma (TASARIM §5.7). |
| K2 | Aynı evrenin eşit ağırlıklı sepetiyle karşılaştırma (TASARIM §5.7). |
| K3 | Faizle karşılaştırma (TASARIM §5.7). |
| p değeri | K1 p değeri, rastgele tekrarların gerçek kural kadar iyi ortalama sonuç vermesine dayanan istatistiksel ölçüdür. Eşbütünleşme p değeri, iki seri arasındaki farkın durağanlığına ilişkin test ölçüsüdür (TASARIM §5.6–5.7, §5.12). |
| Holm | Birden çok denemenin birlikte doğurduğu yanlış kabul riskine yönelik istatistiksel düzeltme (TASARIM §5.11). |
| Güven aralığı | Ortalama fazla getiri tahmininin şans payından gelen belirsizlik aralığı (TASARIM §5.9). |
| Blok bootstrap | Günlük seriyi ardışık bloklar hâlinde yeniden örnekleyerek güven aralığı çıkarma yöntemi (TASARIM §5.9). |
| Örneklem şartı | Karar verilebilmesi için gereken en az gözlem sayısı (TASARIM §5.9). |
| Saptanabilir en küçük etki (MDE) | Verinin şanstan ayırt edebileceği en küçük fazla getiri (TASARIM §5.9, §5.12). |
| İleri yürüme yılları | Tek sürekli koşunun yıllara kesilmiş parçaları (TASARIM §5.8). |
| Ayrılmış dönem | Kurallar yazılırken bakılmamış dönem: kural kaydından sonrası. |
| Sağlamlık ızgarası | Ailenin önceden belirlenmiş parametre hücreleri (TASARIM §5.10). |
| Pozitif hücre | Sağlamlık ızgarasında olumlu sayılan hücre (TASARIM §5.10). |
| Portföy kuralı | Özkaynak düşüşünün büyüklüğü ve süresine ilişkin, aileden bağımsız ret ölçütü (TASARIM §5.12). |
| En büyük düşüş | Özkaynak eğrisinin bir zirveden sonraki en derin düşüşü (TASARIM §5.12). |
| Düşüşte kalma süresi | Özkaynak eğrisinin önceki zirvesinin altında kaldığı en uzun süre (TASARIM §5.12). |
| Boru hattı denetimi | Sınama düzeneğinin kendi denetimi: kuralın getiri öngörmediği sentetik veride yanlış kabul oranı ve gömülü etkide güç (TASARIM §5.12). |
| Yanlış kabul | Getiri öngörmeyen sentetik veride ailenin kabul ölçütlerinin bir kısmından geçmesi. Kâğıt durumuyla aynı değildir (TASARIM §5.12). |
| Güç | Boru hattı denetiminde, gerçek etkisi olan sentetik veride ailenin ölçütlerden geçme oranıdır. MDE hesabında, gerçek bir etkinin istatistiksel olarak yakalanma olasılığıdır (TASARIM §5.12, §5.9). |
| Geçti / Geçmedi | Bir kabul ölçütünün ya da ailenin genel sonucu. Aile durumundan ayrıdır (TASARIM §5.12). |
| Ölçülemedi | Karar vermeye veri ya da süre yetmediğini belirten sonuç. "Geçmedi"den ayrıdır (TASARIM §5.12). |
| Deneme / Kâğıt / Canlı | Deneme, resmi kabul almamış; Kâğıt, geçmiş sınamayı geçmiş; Canlı, kâğıt üstü dönemi de geçmiş aile durumudur (TASARIM §5.12, §6). |
| Kâğıt üstü dönem | Kâğıt ailenin para konmadan izlendiği dönem. Canlı durumundan ayrıdır (TASARIM §5.8). |
