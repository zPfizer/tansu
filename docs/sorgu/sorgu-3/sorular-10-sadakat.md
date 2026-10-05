# Sorular 10: Sadakat, ürün, işletme

**10-001** TASARIM 2 "Aile = yer + teyit" diyor ve Tansu'nun sırasını "zone → kırılım → likidite → teyit" diye veriyor; seçilen üç ailenin (çift rotasyonu, AB=CD, EMA sıkışması) hiçbiri bölge tabanlı değilken bu satır nasıl doğru olur?

**10-002** KURALLAR §3 ölçüt 3 "Tansu sayısal bir sonuç göstermiş" şartını koyuyor, ama dizinde EMA sıkışmasının kanıtı "Tek örnek (sıkışmadan sonra yükseliş)" yazıyor. Üçüncü aile bu ölçütü hangi gerekçeyle geçti?

**10-003** docs/kurallar/D "koda en sadık geçirilebilecekler" sıralamasında sektör liderleri + anomali temizleme 1., günlük rebalancing 2., çift rotasyonu 3.; KURALLAR §3 ilk ikisini neden hiç anmıyor ve hangi ölçüt onları eledi?

**10-004** EMA sıkışmasında giriş tetiği (bitişten sonra 10 gün içinde sıkışma tepesinin üstünde kapanış) tamamen YORUM; Tansu'dan yalnız tolerans ve gün sayısı geliyor. Bu aile hâlâ "Tansu'dan esinlenen" sayılabilir mi, yoksa sistemin kendi stratejisi mi?

**10-005** KURALLAR §2 AB=CD'ye "H" (az YORUM) veriyor, ama aynı satırda pivot ayarı, oran toleransı ve stop eksik; §3 pivot ayarını sadakat kontrolüne bırakıyor. "H" etiketi bu eksiklerle nasıl bağdaşıyor?

**10-006** SMRTG +%305 sonucu tüm sermayenin bileşik kullanıldığı işlemlerden çıkıyor (E K15), TASARIM 5.6 ise %1 risk ve %10 pozisyon tavanı kullanıyor. Tansu'nun "sınanacak iddiası" bu boyutlamayla hangi anlamda aynı iddia olarak kalıyor?

**10-007** Tansu'nun AB=CD örneklerinde fiyat 18'den 6–8 TL'ye inen hisse var (E K7); C teyit edildiğinde fiyat SMA250 altındaysa TASARIM 5.5 gün sonu çıkışı girişin ertesi günü pozisyonu kapatmaz mı? Bu durumda Tansu'nun kazandıran işlemleri risk paketiyle nasıl yeniden üretilecek?

**10-008** E K3 SMA250'nin Tansu'nun "giriş bileşenlerinden biri" olabileceğini, girişin SMA250 üstü gerektirip gerektirmediğinin belirsiz olduğunu yazıyor. TASARIM 5.5 SMA250'yi yalnız çıkış yapıyor; giriş filtresiyse üç ailenin sinyal sayısı ne kadar değişir?

**10-009** KURALLAR §3 risk paketini "SMA250 altı kapanışta çıkış (bütün aileler)" diye tanımlayıp aynı paragrafta çift rotasyonunun kendi çıkışı olduğunu söylüyor; TASARIM 5.5 de paketi çifte uygulamıyor. "Bütün aileler" ifadesi çifti kapsıyor mu?

**10-010** Tansu'nun 5 kapısından "uygun risk/ödül (1:2 veya 1:3)" (E K23) tasarımda hiç yok; üstelik E K11 kendi BALAT çıktısının R/R'sinin 0,20–0,32 olduğunu gösteriyor. Bu eşik hangi gerekçeyle sistemden çıkarıldı ve bu çıkarma Tansu'nun giriş filtresini düşürmek anlamına gelmiyor mu?

**10-011** Tansu'nun (ikinci el) "tek seferlik test bozulan ilişkiyi kaçırır, rolling izle" ilkesine karşın TASARIM 5.6 çiftleri yılda bir kez, 252 günlük tek eşbütünleşme testiyle seçiyor ve yıl içinde izlemiyor (S2-25). Bu, Tansu'nun açık bir ilkesine ters düşen bir tasarım kararı değil mi?

**10-012** Tansu'nun kendi çifti AGROT–GARAN farklı sektörlerde (gıda perakende–banka) ve nakit çıkışlı iki bacaklı bir sürüm (D, gorsel-paket-52); TASARIM 5.6'nın "aynı sektör" kuralı onu seçmez. Sistemin "çift rotasyonu" hangi Tansu sürümünü temsil ediyor, hangisini dışarıda bırakıyor?

**10-013** D, VAKBN grafiğinde Z ≈ −2,3'e inip dönmesine rağmen Mart–Mayıs 2025'te sinyal çıkmadığını ve nedeninin bilinmediğini (kapı mı, ısınma mı) yazıyor. Tansu'nun "Pair Health GÜÇLÜ / Cointegration p 0,048 CURRENT" kapısı gerçek bir giriş izniyse, kapısız kural onun işlemlerinden hangi yönde ayrışır?

**10-014** TASARIM 5.6 "bir hisse en fazla bir çiftte" kuralını koyuyor; Tansu'nun üç çiftinden ikisi GARAN'ı paylaşıyor (VAKBN–GARAN, AGROT–GARAN). "Ayrıca gösterilen" Tansu çiftleri bu kuralla birlikte nasıl koşulacak, yoksa kural onları baştan kırpıyor mu?

**10-015** KURALLAR başlığı ikinci el bilginin "kural olarak tek başına kullanılmayacağını" söylüyor, ama AB=CD stopu "C'den sonra fiyat A'yı geçerse kalıp ölür" cümlesine (ikinci el, E K15 T-abcd) dayanıyor. İlke ile bu istisna arasındaki sınır nerede çiziliyor?

**10-016** TASARIM 5.5 AB=CD'yi "Tansu'nun kendi sınamasındaki (SMRTG, ISKPL) C'den D'ye bacak" diye tanımlıyor; E K15 ISKPL için "not; görsel açılmadı" diyor. C'den D'ye bacak yorumu hiç açılmamış bir görsele ve nota dayanıyorsa bu "birinci el" sayılabilir mi?

**10-017** E Uyarı 1, çoğu notta tweet URL'si olmadığını ve yazar atfının doğrulanmadığını söylüyor (yalnız iki istisna). Üç ailenin birinci el sayılan parametrelerinden kaçı URL'si doğrulanmış Tansu paylaşımına, kaçı yalnız "havuz bağlamına" dayanıyor?

**10-018** KURALLAR "Her YORUM, sınamada deneme sayısına girer" diyor; çiftte sapma formülü, pencere, β yöntemi, AB=CD'de pivot ayarı, stop, EMA'da oran formülü, tetik, ATR uzunluğu YORUM. Holm düzeltmesindeki deneme sayısı bu YORUM'lardan nasıl sayılıyor ve bu sayı kabul eşiğini fiilen ulaşılamaz kılmıyor mu?

**10-019** D, 52 tablosunda giriş günü PnL=0 olduğu için "T+1 Open"ın PnL'e gerçekten uygulanıp uygulanmadığının belirsiz olduğunu yazıyor; KURALLAR §3 ise T+1 açılışı "birinci el" sayıyor. Tansu'nun eğrisi kapanıştan hesaplanmışsa sadakat kontrolünün "T+1 Open" kolu neyi kanıtlar?

**10-020** D, Z penceresini VAKBN/CIMSA için ≈60, AGROT/GARAN için ≈120–126 gün tahmin ediyor (çifte özgü olabilir). Beş çifte tek bir pencere (60 veya 120) uygulamak Tansu'nun yaptığını mı temsil ediyor, yoksa bizim tek pencere varsayımımızı mı?

**10-021** D'ye göre AGROT/GARAN'ın Nisan 2026 sürümü momentum onaysız, sonraki VAKBN/CIMSA sürümleri onaylı; Tansu kuralını zamanla değiştiriyor. Kural kaydından sonra 6 ay süren kâğıt üstü dönemde Tansu yeni bir sürüm paylaşırsa sistem hâlâ "Tansu'ya sadık" sayılır mı?

**10-022** TASARIM 4 "önceki Nabız kuralı bizimdi, Tansu'nun değil" diyor; TASARIM 2 tablosu ve D, "Piyasanın Nabzı" raporunu Tansu'nun paylaştığı kaynak olarak veriyor (NotebookLM imzalı). Eski kural Tansu'nunsa M9 kararının gerekçesi, bizimse §2 satırı doğru mu?

**10-023** E/D'deki VAKBN raporu "Toplam Maliyet 2.054,78 TL (6 geçiş)" diyor; bu, geçiş başına kabaca %0,1 bacak maliyetine denk gelir. TASARIM 5.4 %0,3 ile %0,5'i kabul eşiği yapıyorsa Tansu'nun +%52,9 sonucu hangi maliyet varsayımıyla "yeniden üretildi" sayılacak?

**10-024** Tansu BALAT, AKSGY, KAPLM ve bağı kopan çiftin başarısız sonuçlarını kendisi paylaşıyor. Sistemin AB=CD ve çift kuralları bu başarısız örnekleri sinyal olarak üretir mi, üretmezse sadakat kontrolü yalnız Tansu'nun olumlu örneklerini test etmiş olmuyor mu?

**10-025** Tansu'nun çıktıları yfinance/.IS ile üretildiyse Yahoo'nun bedelsiz/bedelli günlerindeki sahte sıçramaları (veri-kaynaklari §2) onun rakamlarına gömülüdür. Tasarım Yahoo'yu "yanlış" ilan edip kuralı temiz veriyle sınıyorsa, sınanan şey Tansu'nun gördüğü kural-veri bileşiminden farklı olmuyor mu?

**10-026** Sadakat kontrolünde Yahoo'nun hangi serisi kullanılacak: `Close`, `Adj Close` (yalnız temettü düzeltmeli), `auto_adjust=True` bedelsiz düzeltmesi yapmıyor (veri-kaynaklari 2.2)? Tansu'nun hangisini kullandığı bilinmiyorsa "Tansu'nun rakamını en iyi üreten formül" seri seçimine de bağımlı olmaz mı?

**10-027** VAKBN–GARAN raporunda "dönem ucu yok" (D); "son Z −3,108, önceki Z −3,404" hangi güne ait olduğu bilinmeden yeniden üretiliyor. Rapor tarihi, pencere ve β yöntemiyle birlikte serbest bir parametre olduğunda sahte bir eşleşme nasıl dışlanacak?

**10-028** KURALLAR §4 "birden çok aday formül denenir, en iyi üreten seçilir" diyor ve hedef olarak yalnız iki Z değeri ile 6 geçiş veriyor. "Üretti" için sayısal tolerans ve birden çok formülün eşleştiği durumda seçim kuralı sorgudan önce yazılı mı?

**10-029** Sadakat kontrolü "getiriye bakmaz" diyor, ama hedef olarak 6 geçişi (stratejinin işlem sayısı) ve VAKBN raporunun geri kalan satırlarını kullanıyor. Geçiş sayısını tutturmak performans eğrisini tutturmaya ne kadar yakındır ve sınır hangi kuralla çiziliyor?

**10-030** KRDMD için tek hedef var: 17.12.2025–14.01.2026 arası sıkışma ve "ortalama oran %0,64". Paydası kapanış, EMA200, EMA ortalaması gibi birkaç aday tek bir ortalamayı tesadüfen tutturabiliyorsa bu tek sayı oran formülünü gerçekten belirler mi?

**10-031** Sadakat tablosunda KRPLS ve MARKA #13 için D değerleri (11,29 / 10,05 / 70,25) kontrol ediliyor; gorsel-paket-01 dosya adları "krpls-...-abcd-dusus" ve "marka-pattern13-backtest-dusus" diyor. Kontrol edilen kalıplar düşüş yönlüyse yalnız-alış AB=CD kuralının doğru okunduğu bunlarla nasıl gösterilir?

**10-032** TASARIM 8.5 ve KURALLAR §4 "üretilemezse YORUM olarak kalır" diyor. Sapma formülü ve pencere YORUM kalırsa "Tansu'nun en güçlü rakamları, H hazırlık" diye 1 numaraya konan çift rotasyonu raporda hangi etiketle sunulacak?

**10-033** Sadakat kontrolü sırasında denenen aday formüller, pencereler ve pivot ayarları 5.11 deneme günlüğüne yazılıp Holm sayısına katılıyor mu, yoksa sadakat adımı "getiriye bakmıyor" gerekçesiyle sayım dışı mı?

**10-034** Formül Yahoo'da seçiliyor, gerçek sınama İş Yatırım `HGDG` verisiyle yapılıyor (TASARIM 7.2). Seçilen formülün aynı hisse ve günlerde İş Yatırım serisinde Tansu'nun rakamına yakın çıktığının doğrulanması planlanmış mı, yakın çıkmazsa hangi veri esas alınacak?

**10-035** Yahoo ~2994 satır, İş Yatırım ve borsapy ~2945 satır veriyor (tatil günleri, veri-kaynaklari 3.1). 60 "gün" pencereli Z-skoru satır sayısına bağlıysa Yahoo'daki hayalet satırlar Tansu'nun rakamını yeniden üretirken pencereyi kaydırmaz mı?

**10-036** Sadakat hedeflerinin çoğu düşük çözünürlüklü görsellerden elle okunmuş rakamlar (D: "çözünürlük düşük", "belirsiz"). Okuma hatası payı sadakat toleransına hesaba katılıyor mu, "üretildi" kararı bu hata payının içinde mi veriliyor?

**10-037** TASARIM 5.3 "T+1 açılış"ı sadakat kontrolünde Yahoo açılışıyla ayrıca üretiyor, asıl sınama AOF ile yapılıyor. Aynı kural iki dolumla farklı fazla getiri verirse kabul ölçütü hangisine bakar ve hangisi "Tansu'nun kuralı" olarak raporlanır?

**10-038** Çift rotasyonu "Tansu'nun en güçlü rakamları" gerekçesiyle 1. aile seçildi (KURALLAR §3); +%52,9 ve +%49,2 2025–2026 dönemine ait ve tasarımcılar bu rakamları görmüş durumda. Aile seçiminin Tansu'nun getiri rakamlarına bakılarak yapılması "getiriye bakılmaz" ilkesinin ve 5.8'deki yanmış dönem mantığının dışında mı kalıyor?

**10-039** "Tansu'nun kodunda yfinance ve .IS görünüyor" varsayımı hangi görsellere dayanıyor; yalnız boğa yutan mum kodu ve AGROT.IS & GARAN.IS başlığı mı? EMA sıkışması (KRDMD) ve AB=CD araçlarının da Yahoo kullandığı nereden biliniyor?

**10-040** TASARIM 2 "Önce piyasanın havası"nı Tansu'nun ilk ilkesi olarak listeliyor, ama TASARIM 3 ve 4 etiketi kapı yapmıyor, yeni girişi durdurmuyor. Etiketin hiçbir karara girmediği bir sistemde bu ilke somut olarak nerede uygulanıyor?

**10-041** TASARIM 4/6 "piyasa durumu etiketi" diyor ama etiketin hangi göstergelerle, hangi eşiklerle ve hangi sınıflarla üretildiğini hiçbir yerde tanımlamıyor; D'de Nabız için SMA 18/35 ile 20/50 çelişkisi var. Etiketin tanımı olmadan "sonuçlar etikete göre ayrı raporlanır" nasıl sınanabilir?

**10-042** KURALLAR Piyasa durumu satırı VIX'in ABD VIX olduğunu ve Yahoo'da bedava olduğunu yazıyor; TASARIM 4 "Yahoo kullanılmaz" diyor ve İş Yatırım VIX vermiyor. Etiketin VIX bileşeni hangi kaynaktan, hangi lisansla gelecek?

**10-043** ABD VIX kapanışı BIST kapanışından sonra oluşur (D: "önceki ABD günü kullanılmalı"). Geçmiş günleri etikete göre gruplarken t günü VIX'i mi, t−1'i mi kullanılıyor; ilki sinyal anında bilinmeyen bilgiyi sınıflamaya sokmaz mı?

**10-044** BIST-VIX 5 adım kuralı VIX RSI(200) istiyor (D); en az 200 gün ısınma gerekir. 2015 başındaki ve etiketi hesaplanamayan günler gruplamada nereye düşüyor?

**10-045** TASARIM 4 sonuçları etikete göre ayrı raporlamayı öngörüyor; aile × varyant × etiket dilimleri sayısız ek karşılaştırma üretir. Bu dilim p değerleri 5.11 Holm sayımına giriyor mu, girmiyorsa Levent dilimden dilime bakarak kendi "kuralını" nasıl ayıklamaktan korunacak?

**10-046** K1(b) "aynı hisse, aynı piyasa durumunda ±20 gün" eşleştirmesi etiketi fiilen bir kontrol değişkeni yapıyor (TASARIM 5.7). Etiket "kapı değil" denirken etiket tanımının değişmesi p değerini değiştiriyorsa etiket tanımı kural kaydı ve hash'e dahil mi?

**10-047** TASARIM 4 Nabız'ın kapı olmaktan çıkma gerekçesini "bizimdi, Tansu'nun değil, ve 2023 sonrası tutmadı" diye veriyor. Tutmayan şey bizim YORUM formülümüzse Tansu'nun "önce piyasa" ilkesini düşürmek bu sonuçtan mantıksal olarak çıkar mı?

**10-048** TASARIM 6.4 kartta piyasa durumu alanı saymıyor; §1'deki akşam sorusunun ilk yarısı "Piyasa nasıl?". Levent bu cevabı akşam hangi ekranda ve hangi biçimde görüyor?

**10-049** Etiket VIX veya endeks verisi eksik olduğunda ya da 19:30 kontrolü başarısız olduğunda üretilemiyor; "yalnız bilgi" denmesi kartın yine üretileceği anlamına mı geliyor, Streamlit "Kanıt" ekranı etiket yokken ne gösteriyor?

**10-050** Tansu'nun piyasa araçları farklı cevaplar veriyor: Nabız 4/5 "dikkatli iyimserlik" (AO NEGATİF), BIST-VIX 5 adım "Kusursuz Long", endeks 5/5 "Full Long" (NH-NL, Corwin–Schultz). Etiket bunlardan hangisine karşılık geliyor ve aynı günde çelişirlerse hangisi gösterilir?

**10-051** TASARIM 6.4'teki kanıt satırı örneği "112 işlem, ... fazla getiri −%0,2 ± %1,1: ayırt edilemiyor", oysa 6.3 deneme ailelerini gizliyor ve 5.12 Canlı olmak için p < 0,05 pozitif fazla getiri istiyor. Kartı gösterilen bir ailenin kanıt satırı "ayırt edilemiyor" diyebilir mi?

**10-052** 5.8 ve 5.12.6 uyarınca hiçbir aile en az 6 ay ve 30 işlem dolmadan Canlı olamaz; bu süre boyunca kart listesi boş. Levent bu aylarda her akşam ne görüyor ve §1'deki "hangi hissede hangi kural sağlandı" vaadi o dönemde ne anlama geliyor?

**10-053** §1 "nerede yanıldığımı anlarım" diyor; Tansu'nun süreç ilkesi (E K18) aday tarihi, giriş gerekçesi, invalidation, MFE/MAE içeren işlem günlüğü ve 1/3/5 günlük izleme istiyor. Tasarımda kart sonrası "neden stop oldu / neden hedefe gitti" sorusunu cevaplayan hangi ekran veya kayıt var?

**10-054** TASARIM 2 Tansu durumlarını AKTİF / TAMAMLANDI / BOZULDU diye veriyor, 6.5 AKTİF / STOP / HEDEF / BOZULDU kullanıyor, E K15 ayrıca TEPKİ_VERDİ ve BELİRSİZLEŞTİ gösteriyor; GLOSSARY "Bozulma"yı SMA250 altı kapanış sayarken Tansu'da BOZULDU kalıp geçersizliği (A aşıldı). Hangi etiket kümesi nihai ve BOZULDU hangi olayı ifade ediyor?

**10-055** Kart 19:30'da üretiliyor; giriş fiyatı ertesi günün AOF'u (5.3), stop da bu giriş fiyatından hesaplanıyor. Henüz bilinmeyen AOF yokken kartın "giriş bölgesi" ve "stop" alanlarında hangi rakamlar yazılıyor?

**10-056** Çift rotasyonu kartında stop ve hedef yok (5.5); kart "Y'ye geç" derken Levent'in elinde X mi, nakit mi var, sistem bunu nereden bilecek? Simülasyondaki çift bölmesinin durumu Levent'in gerçek portföyüyle nasıl eşleşiyor?

**10-057** Simülasyon girişi ertesi günün AOF'una koyuyor; AOF gün sonunda belli olan bir fiyat ve bir insan alıcı onu önceden hedefleyemiyor. Levent'in fiilen yapabileceği işlem (açılışta, gün içinde) ile simüle edilen dolum arasındaki fark kartta ve kanıt satırında nasıl yansıtılıyor?

**10-058** Pozisyon tavanı sermayenin %10'u (5.6), risk %1 ve stop 2 ATR; ATR'si %2'den küçük hisselerde tavan bağlayıcı olur ve fiili risk %1'in altında kalır. Kart hangi büyüklüğü gösteriyor ve kanıt satırındaki fazla getiri aynı büyüklükle mi hesaplanmış?

**10-059** Kart "sermayenin yüzdesi ve 1.000.000 TL için adet" veriyor, Levent'in sermayesi ise bilinmiyor (S2-2). Teknik olmayan sahibin yüzdeyi kendi sermayesine elle çevirirken yanlış ölçeklemesine karşı ne var; çift bölmesinde 200.000 TL'lik pay hangi biçimde yazılıyor?

**10-060** Kartlardaki fiyat, ATR ve SMA250 düzeltilmiş (HGDG, temettü dahil; THYAO'da HGDG/HG = 0,9769) seriden mi geliyor, ham seriden mi? Levent aracı kurum ekranında ham fiyat görürken stop ve giriş düzeltilmiş seriden yazılırsa rakamlar uyuşur mu?

**10-061** BIST'te fiyat adımı (kademe) vardır; stop = giriş − 2 ATR keyfi bir sayıdır. Kart stop ve hedefi emir olarak girilebilir bir fiyata yuvarlıyor mu, yuvarlama stop mesafesini ve %1 riski değiştirirse bu nasıl hesaba katılıyor?

**10-062** TASARIM 8.4 tedbirli hisselerin (brüt takas, tek fiyat) ayırt edilip edilemediğini açık bırakıyor; sinyal günü kilitli tavan kapanışı olan hisse için kart ertesi gün alınamayacak bir "giriş bölgesi" gösterebilir. Kart bu durumları kullanıcıya uyarı olarak taşıyor mu?

**10-063** Kanıt satırındaki "± %1,1" nedir: standart hata mı, %95 güven aralığı mı; işlem başına mı, gün başına mı? Teknik olmayan bir sahibin "ayırt edilemiyor" ifadesini doğru okuduğunu gösteren bir anlaşılırlık sınaması tanımlı mı?

**10-064** Kanıt satırı kayıt anında bir kez mi hesaplanıyor, yoksa kâğıt üstü dönem biriktikçe güncelleniyor mu? Satırdaki rakam yanmış 2023 sonrasını içeren ileri yürüme sonucu mu, yoksa yalnız kâğıt üstü dönem mi?

**10-065** "Hiçbir aile geçmedi" ekranı "birinci sınıf sonuç" sayılıyor (§1), oysa Levent "modern, A'dan Z'ye çalışan" bir sistem istedi (S2-3). Bu ekran ile "veri sorunlu" ve "sistem çalışmıyor" durumlarını teknik olmayan sahibin birbirinden ayırabildiğini gösteren hangi sınama tanımlı?

**10-066** Streamlit "Kanıt" ekranı "raporu ve piyasa durumunu okuyor" (3); Windows'ta Streamlit'i kim, nasıl başlatıyor, ekran 19:30 koşusundan sonra kendiliğinden yenileniyor mu, rapor markdown'ı veri arayüzü olarak ayrıştırılırsa biçim değişiminde ekran ne yapıyor?

**10-067** Kart CSV'si Türkçe yerelli Windows'ta Excel'de çift tıklamayla açılacak; ondalık virgül, ";" liste ayırıcısı ve UTF-8 BOM'suz Türkçe karakterler (ı, ş, ğ) sütunları bozabilir. CSV'nin Levent'in makinesinde okunur açıldığını gösteren bir kabul adımı var mı?

**10-068** Kanıt yalnız simüle edilen kural sonuçlarını ölçüyor; Levent bazı kartlarda gerçek işlem yapıp bazılarını atlayacak. Gerçekleşen işlemlerin ve atlanan kartların kaydı tutulmazsa "nerede yanıldığımı anlarım" cevabı sistemin mi, Levent'in mi hatasını ayırt edecek?

**10-069** Aynı gün sinyal sayısı boş yeri aşarsa "en likit önce" sırası simülasyonda belirleyici (5.6, M12). Kart listesi hangi sırayla gösteriliyor ve sermayesi hepsini almaya yetmeyen Levent'e hangi kartların simülasyonda "alındığı" nasıl söyleniyor?

**10-070** Kartta veri tarihi, üretim saati ve anlık görüntü kimliği gösterilmiyorsa Levent Streamlit'i gece 22:00'de ya da ertesi sabah açtığında kartın taze mi bayat mı olduğunu, 19:30 kontrolünün geçip geçmediğini nereden anlıyor?

**10-071** Açık pozisyonu olan hissede gelen yeni sinyal "sayıma girmez" (5.3); Tansu'nun yöntemi ise girişi oluşmayan adayları da izlemek (E K18). Bu sinyal kartı kullanıcıya gösteriliyor mu ve hiç gösterilmiyorsa Levent "sinyal var ama kart yok" durumunu nasıl yorumlayacak?

**10-072** Levent Tansu'nun paylaşımlarını takip ediyor; Tansu bir gün KRDMD'de sıkışma paylaşır, sistem ise o aileyi "deneme" olarak gizler (6.3). Sistem "Tansu bugün X dedi, sizde neden yok" sorusuna hangi çıktıyla cevap veriyor?

**10-073** İş Yatırım günlük veriyi ne zaman yayınlıyor bilinmiyor (TASARIM 8.7); 19:30 sabit seçilmiş. Veri 19:30'dan sonra gelirse her gün tazelik kontrolü başarısız olur ve kart üretilmez; yeniden deneme veya geç koşu politikası var mı?

**10-074** Bilgisayar kapalıyken kaçırılan görev ertesi sabah (ör. 11:00'de) koşarsa İş Yatırım "bugünkü" satırı gün içi kısmi veri taşıyabilir; 5.1 yalnız "son çubuk tarihi bugün değilse" diyor, tarih eşleşir. Kısmi çubuk Adım durumuna ve karta nasıl sızmaz?

**10-075** TASARIM 5.1 "hacim olağandışıysa kart üretilmez" diyor; eşik, pencere ve karşılaştırma ölçüsü tanımlı değil. Arife yarım günleri ve bayram öncesi düşük hacimli günler yanlış alarmla kartı bastırır mı, yüksek hacimli gerçek günleri kaçırır mı?

**10-076** TASARIM 4 Takvim modülü BIST tatillerini ve yarım günleri bilmekle yükümlü; S2-15 ise "İş Yatırım'ın verdiği günler işlem günüdür" diyor. Veride eksik kalan bir gün sessizce tatil sayılırsa Takvim modülü neyi doğruluyor ve bayram tarihlerini yıllık kim güncelliyor?

**10-077** Windows Görev Zamanlayıcı'da "kullanıcı oturum açmamışken çalıştır", pil/uyku/hazırda bekletme koşulları, uyandırma zamanlayıcısı ve masaüstündeki klasörün OneDrive eşzamanlaması hiç tanımlı değil. Hafta sonu ve tatil dahil gözetimsiz 30 günlük bir koşu denemesi planlanmış mı?

**10-078** Koşu hiç çalışmazsa, Python/ortam bozulursa ya da rapor yazılmadan çökerse ortada ne "veri sorunlu" satırı ne yeni rapor olur (S2-48 raporun ilk satırına dayanıyor). Boş bir akşam ile "sinyal yok" akşamını Levent nasıl ayırt eder?

**10-079** İş Yatırım uç noktası belgelenmemiş bir dahili AJAX çağrısı ve oturum çerezi istiyor; borsapy TradingView WebSocket'ine bağlı (veri-kaynaklari 1.1, 3.1). Biçim değişimini kim, nasıl fark ediyor ve 100 hissenin 3'ü eksik geldiğinde kalan 97 için kart üretiliyor mu?

**10-080** Kural kaydı "kodun parmak izi" tutuyor (5.8) ama pandas-ta-classic, statsmodels, borsapy sürümlerini kapsamıyor. Bir kütüphane güncellemesi gösterge değerlerini değiştirirse bu yeni deneme sayılır mı ve 6 ay sonraki koşu bugünküyle yeniden üretilebilir mi?

**10-081** Kâğıt üstü dönemin ilk aylarında hata düzeltmek kaçınılmaz; her kod değişikliği hash'i değiştirip "yeni deneme" sayılırsa 6 aylık saat sıfırlanır. Hata düzeltmesi, günlük biçimi değişikliği ve yeniden düzenleme (refactor) için kural değişikliğinden ayrı bir politika yazılı mı?

**10-082** Ham fiyat anlık görüntüsü "tarihli, değişmez" (4) ve her koşu hangisini kullandığını yazıyor; ama 11 yıllık geçmiş tek istekle geliyor (S2-17). Her akşam tüm geçmiş yeniden indirilip kaydedilirse ~500 sembol × günlük kopya disk ve istek açısından ne kadar tutar, tutulmuyorsa "değişmez anlık görüntü" ne zaman alınıyor?

**10-083** S2-17 "günlük 1 istek" diyor, TASARIM 5.1 bütün hisse × gün getirilerini borsapy ile tam karşılaştırıyor ve Evren aylık olarak bütün sembollerin PD ve 60 günlük hacmini gerektiriyor; TASARIM 4 aynı yerde "kullanım koşulları bulunamadı; az sayıda istek" diyor. Günlük ve ilk yükleme istek sayısı gerçekte kaç ve 1 sn bekleme ile süre kaç dakika?

**10-084** Açık kartların durumu hangi kalıcı depoda tutuluyor (DuckDB ertelendi, 3)? Koşu yarıda kesilirse ya da aynı gün iki kez çalışırsa Adım güncellemesi (AKTİF / STOP / HEDEF) çift işlenmeden, yarım yazılmadan nasıl korunuyor?

**10-085** Deneme günlüğü (Holm sayısı) ve kural kaydı tek bir bilgisayarda düz dosyalar olarak duruyorsa, silinmesi veya düzenlenmesi çoklu deneme sayısını sessizce sıfırlar ve ön kayıt iddiasını boşaltır. Dışarıdan zaman damgalı bir kanıt veya yedek var mı?

**10-086** TASARIM 4 "Kullanım koşulları ve hız sınırları bulunamadı" diyor, S2-52 ise "kişisel kullanım" diyor; bu ifade isyatirimhisse ve borsapy README'lerinden geliyor, İş Yatırım veya TradingView şartlarından değil (veri-kaynaklari 1.3, 3.1). Belgelenmemiş uç noktaları günlük otomatik çekmenin hukuki dayanağı ne ve 7. adımda kod yazmaya başlanmadan 8.1 neden kapanmıyor?

**10-087** TradingView WebSocket verisini borsapy üzerinden tüm hisse × gün karşılaştırması için kullanmak (5.1) TradingView şartlarına uyuyor mu? Engellenirse ikinci kaynak kayboluyor; veri doğrulaması o durumda neye dayanacak?

**10-088** isyatirimhisse IP engeli uyarısı yapıyor (veri-kaynaklari 1.3); ilk toplu çekim (~500 sembol × 11 yıl) ev IP'sini engelletirse Evren, sadakat ve motor aynı anda duruyor. Böyle bir durumda planlanmış bir geri dönüş yolu var mı?

**10-089** Kart hisse, stop, hedef ve pozisyon büyüklüğü gösteriyor; "Sistem emir vermez, 'AL' demez" (§1) cümlesine rağmen bu içerik fiilen talimat gibi okunur. Levent kartı yakınlarına gösterirse SPK yatırım danışmanlığı sınırı ve "Tansu" adının/görsellerinin kullanımı (onay, itibar) ne durumda; S2-52 "paylaşılmaz" bunu kapsıyor mu?

**10-090** Hisse kazancı ve temettü vergisi doğrulanmadı (8.6); %0,5 masraf senaryosu "bir kısmını karşılar" deniyor. Kanıt satırı ve kabul ölçütü vergi öncesi sonuca dayanıyorsa, kâğıt üstü kârlı çıkan bir aile gerçek net getiride kaybettirebilir; bu kartta nasıl gösteriliyor?

**10-091** Evren KAP "Dönemsel Endeks Değişiklikleri" PDF'lerine ve KAP'ın belgelenmemiş API'sine bağımlı olacak; kullanım koşulları okunmadı (veri-kaynaklari 1.4). Şartlar otomatik çekmeyi yasaklarsa 8. adımda kurulan geçmiş BIST100 listesinin hukuki durumu ne olur?

**10-092** Adım fonksiyonu ortak (4) ama sinyalleri Aile üretiyor ve canlıda kaydırmalı pencereyle, sınamada belki toplu hesaplanıyor. Canlı boru hattını geçmiş üzerinde tekrar oynatıp sınama işlemleriyle birebir aynı işlem listesini ürettiğini kanıtlayan bir test tanımlı mı?

**10-093** "Sınama ve canlı aynı fonksiyonu kullanır, ayrışamaz" (A5) işlev için doğru olabilir, ama veri için değil: yeni bir bedelsizde `HGDG` geçmişi yeniden ölçeklenir ve canlı günde hesaplanan ATR/SMA250 sonradan değişir. Canlı ile sonradan sınanan sonuç arasındaki veri revizyonu farkı nasıl ölçülüyor?

**10-094** 5.12.6 kâğıt üstü fazla getiriyi doğrulama etkisinin "en az yarısı" ile karşılaştırıyor; doğrulama nihai düzeltilmiş veriyle, kâğıt üstü gün gün alınan veriyle hesaplanıyor. İki farklı veri rejimini aynı eşikle kıyaslamak adil mi, veri-kalite farkı eşiğe giriyor mu?

**10-095** Kural kaydı "kural, parametreler ve kodun parmak izi" diyor; Evren (PD tabanlı), Takvim, Maliyet ve Piyasa durumu modülleri de bu kapsamda mı? Evren'in KAP gerçek BIST100 ile değiştirilmesi (7.8) geçmiş sonuçları değiştirir; bu yeni deneme mi sayılacak?

**10-096** TASARIM 5.3 motor için yedi sınamayı "kod yazılmadan önce" tanımlıyor; hepsi stop/hedef/dolum odaklı. Çift rotasyonu geçişi (ΔZ dönüşü), simülatörün nakit faizi, bölme muhasebesi, 20 günlük blok yeniden örnekleme ve Holm hesabı için hangi bilinen-cevaplı testler tanımlı?

**10-097** Motor "belirleyici" (4) ama K1 1.000 rastgele tekrar ve blok yeniden örnekleme kullanıyor. Tohum politikası ve platform/kütüphane sürümü aynı kodda aynı p değerini garanti ediyor mu, farklı iki koşunun p değeri ne kadar ayrışırsa kabul kararı değişir?

**10-098** Veri deposu, Şirket olayları ve Evren aynı iki kaynaktan (İş Yatırım, borsapy) besleniyor ve Evren Veri deposunun PD/hacim alanına bağlı; "her modülün küçük bir dış yüzü var" ifadesine rağmen bir kaynak değişirse hangi modül testi kırılır, modüller kaynak olmadan (sahte veriyle) bağımsız sınanabilir mi?

**10-099** Rapor ile Streamlit arasındaki sözleşme markdown ve CSV dosyaları; şema sürümü, zorunlu alanlar ve sürüm uyumsuzluğunda davranış tanımlı değil. Rapor biçimi değiştiğinde Streamlit'in sessizce yanlış sayı göstermediğini hangi test garanti ediyor?

**10-100** "Önce sadakat, sonra kâr: tutmazsa değiştirilmiş hali yeni deneme" (§1) diyor, ama Tansu sistematik sonuç vermiyor, yalnız seçilmiş örnekler paylaşıyor (KURALLAR §1.1). Bir ailenin "Tansu'nun gösterdiği haliyle tutmadığı" hangi ölçütle, hangi sayısal eşikle ve hangi aşamada karara bağlanıyor?
