# Sorular 04: Çift rotasyonu

04-001. KURALLAR §3 madde 1 sapmayı `log(Y) − β·log(X)` (α yok) yazıyor, D dosyası ise `ε = log Y − α − β·log X` diyor; hangisi geçerli ve α'nın olmaması Z'nin ortalamasını nasıl etkiler?

04-002. Sorgu-2 S2-23 "sadakatle bulunamazsa log(Y) − log(X), 60 gün" diyor; "bulunamadı" kararı hangi sayısal toleransla verilecek (Z = −3,108 için ± kaç)?

04-003. Sadakat yalnız iki sayıya (Son Z −3,108, Önceki Z −3,404) dayanıyor ve D dosyası rapor tarihini "dönem ucu yok" diye kaydediyor; Z hangi takvim günü için yeniden üretilecek?

04-004. 60/120 gün ve log oran/β'lı kalıntı olmak üzere dört aday iki sayıya uydurulursa, birden fazla adayın aynı sayıyı üretmesi ve yanlış adayın seçilmesi riski nasıl ölçülecek?

04-005. β her gün yeniden tahmin ediliyorsa geçmiş ε değerleri de her gün değişir; ΔZ = Z_t − Z_{t−1} içindeki Z_{t−1} o günkü β ile mi yoksa bugünkü β ile mi hesaplanır?

04-006. Yuvarlanan pencerede ortalama ve std, t günü gözlemini içeriyor mu; içeriyorsa |Z| için matematiksel üst sınır ±2 eşiğinin anlamını değiştirmez mi?

04-007. Std için ddof=0 mı ddof=1 mi kullanılacak, ve bu fark Tansu'nun −3,108 rakamını yeniden üretme toleransının içinde mi kalıyor?

04-008. TASARIM 5.6 çift seçimini 252 günlük pencerede yaparken KURALLAR Z'yi 60 veya 120 günlük pencerede standartlaştırıyor; eşbütünleşme ölçeği ile Z ölçeği neden farklı ve bu uyumsuzluk bilinçli mi?

04-009. Tansu'nun raporunda "Half-Life" alanı boş; tasarım half-life'ı seçimde, Z penceresinde ya da girişte hiç kullanmıyorsa, yarı ömrü Z penceresinden uzun olan bir çiftte ±2 eşiği neyi ölçer?

04-010. Tansu'da X = GARAN referans bacak; yeni seçilen çiftlerde X ve Y rolü neye göre atanıyor ve Engle–Granger p-değeri yöne bağlıyken yön seçimi p'yi küçülten tarafa mı yapılıyor?

04-011. β negatif ya da sıfıra yakın çıkarsa "Y ucuz / X ucuz" yön anlamı ve hangi hisseye geçileceği nasıl tanımlı?

04-012. Tansu raporunda Beta 1,675, Beta CV 0,277 ve ayrı bir rolling beta penceresi (~30 gün, düşük güven) var; tasarım β istikrarına hiç bakmıyorsa β penceresi Z penceresiyle aynı mı olacak?

04-013. Yahoo ve İş Yatırım düzeltilmiş fiyatları bugünkü düzeltme katsayısıyla geriye ölçeklenmiş; t gününde β ve Z hesaplanırken gelecekteki temettü ve sermaye artırımı katsayıları pencerenin içine sızmıyor mu?

04-014. D dosyasında VAKBN grafiğinde Z'nin Temmuz 2025'te tek günde ≈ −2,5'ten +4'e sıçraması veri hatası mı bölünme mi bilinmiyor; motor spread serisinde böyle bir sıçramayı sinyal mi yoksa hata mı sayacak?

04-015. ΔZ'nin işaretine ek eşik ya da süreklilik koşulu yok; Z_t ile Z_{t−1} arasında 0,001'lik gürültü farkı gerçek sinyal üretiyorsa sahte "dönüş" günlerinin sayısı hiç raporlanacak mı?

04-016. Sorgu-2 S28 "ΔZ > 0 tek gün yeterli, Tansu'nun raporu öyle (+0,30)" diyor; rapor yalnızca bir günün ΔZ'sini gösterirken ve tweet onayın detayını "ileride anlatacağım" derken bu hangi kanıtla "birinci el" sayılıyor?

04-017. D dosyası VAKBN grafiğinde Z ≈ −2,3'e inip döndüğü halde sinyal olmadığını yazıyor; tek günlük ΔZ > 0 kuralı o dönüşte sinyal üretecekse tasarımın Tansu'nun kendi grafiğiyle çeliştiği nasıl ele alınacak?

04-018. Z, −2,5'ten +2,5'e ΔZ koşulunu sağlayan bir gün olmadan (monoton yükselişle) geçerse pozisyon yanlış hissede mi kalır, ve bu durum için tasarımda hangi kural var?

04-019. İki hissenin birinde işlem durdurma, tek fiyat ya da hacimsiz gün varsa o günkü fiyat ileri taşınıyor mu ve ΔZ'si bu ileri taşınan değerle sıfırlanıp sahte onay üretebilir mi?

04-020. KURALLAR "ilk sinyale kadar nakit; sonra hep bir hissede" diyor, D dosyası "hep yatırımda" kuralını yüksek güven sayıyor; ilk sinyale kadar geçen sürenin Tansu'daki %28,5'i (piyasada kalma %72,27) tasarımda yeniden üretilecek mi?

04-021. Strateji ilk sinyale kadar nakitte, 50/50 tutma ise ilk günden yatırımda; bu karşılaştırma nakit dönemi yüzünden kurulumdan adil mi?

04-022. Yıllık seçimde yeni giren çift, ilk sinyale kadar nakitte mi bekleyecek yoksa bir hissede mi başlayacak; her yıl bu nakit penceresinin ortalama uzunluğu raporlanacak mı?

04-023. Boştaki nakit politika faizi kazanıyor (TASARIM 5.6) ama Tansu'nun hesabında nakit faizi yok; faiz kaynaklı fazla getiri çift bölmesinde K1 ve K2'ye karşı sonuçtan ayrıştırılacak mı?

04-024. Politika faizi 2015–2017, TLREF sonrası dönem kullanılıyor; TLREF'in başladığı tarihten önceki geçiş yılında hangi seri hangi güne kadar kullanılacak?

04-025. Her çiftin payı her an tek hissede olduğundan 5 çiftli bölme en fazla 5 hisseli bir portföydür; maksimum düşüş sınırı bu yoğunlaşmayla gerçekçi mi ölçülüyor?

04-026. TASARIM 5.6 "p < 0,05 olan çiftler, p'ye göre en iyi 5" der; aynı sektörde 10 hisse 45 çift eder ve %5 yanlış pozitif beklenir, tasarım çoklu test düzeltmesi (FDR) yapmıyor; seçilen 5'in "kazananın laneti" nasıl sınanacak?

04-027. Eşbütünleşme testi hangisi: statsmodels `coint` (Engle–Granger), trend parametresi, gecikme sayısı, otomatik gecikme seçimi; Tansu'nun p = 0,048 değerinin hangi test ve pencereyle hesaplandığı da bilinmiyor.

04-028. Seçilen çiftlerin ertesi yıl da p < 0,05 kalma oranı (örneklem dışı süreklilik) raporlanmayacaksa, seçim kuralının eşbütünleşmeyi öngördüğü nasıl gösterilecek?

04-029. TASARIM 5.6 "aynı sektör" şartı koyuyor; AGROT (perakende) ile GARAN (banka) aynı sektörde değil, yani Tansu'nun üç çiftinden biri kuralla seçilemez; "ayrıca gösterilir" derken motor bu çifti hangi kurallarla koşturacak?

04-030. GARAN hem VAKBN–GARAN hem AGROT–GARAN çiftinde; "bir hisse bir çiftte" kuralı Tansu'nun çiftlerini aynı bölmede birlikte koşturmayı engelliyor mu, ve ayrı koşuların sonuçları nasıl karşılaştırılıyor?

04-031. Çakışmada "p'si en iyi çift kalır" açgözlü bir kural; elenen çiftin diğer hissesi için yeni bir çift aranıyor mu ve sonuçta 5'ten az çift kalırsa bölmenin payı ne olur?

04-032. Aynı sektörden 5 çift bulunmazsa (az hisseli sektörler, çakışmalar) bölmenin sermayesi bütün yıl nakitte mi kalır, yoksa kalan çiftler sermayeyi paylaşır mı?

04-033. Çift için sektör bugünkü borsapy sınıflamasından alınıyor (Sorgu-2 S21); 2015 tarihli bir çiftte hisse o yıl başka sektördeyse seçim ileriyi görüyor ve "küçük yanlılık" ölçülmeden nasıl küçük sayılıyor?

04-034. Çift evreni hangisi: TASARIM 5.2 "BIST100 sabit/nokta-zamanlı liste" mi yoksa Sorgu-2 S19'daki piyasa değeri + 60 günlük medyan hacimle en büyük 100 mü; yıl içinde evrenden düşen hisse çiftte tutulmaya devam ediyor mu?

04-035. Yıl başı seçimi takvim yılının ilk işlem günü mü, hangi kapanışa kadar veri kullanıyor, ve seçim ile ilk işlem arasındaki gün sayısı sızıntı bırakıyor mu?

04-036. İş Yatırım verisinin başlangıcı 2015 ise ilk 252 gün seçim penceresi + ilk 60 gün Z ısınması çift bölmesinin ilk işlem yılını 2016'ya iter; ileri yürümenin 2015–2017 başlangıç eğitimi ile bu nasıl hizalanıyor?

04-037. Holding ile iştiraki ya da aynı grup şirketleri (aynı sektör etiketli) yapısal bağ ve ortak kontrol nedeniyle eşbütünleşik görünebilir; tasarım bunların çift olarak seçilmesini engelliyor mu?

04-038. Nominal TL fiyatlarda yüksek enflasyon ve devalüasyon dönemlerinde (2018, 2021 sonu) ortak trend p-değerini yapay olarak iyileştiriyor olabilir; 252 günlük pencerelerde rejim kırılması sınanıyor mu?

04-039. Sorgu-2 S25 "Tansu'nun kuralında çıkış yok" diyor, oysa D dosyası Tansu'nun rolling cointegration kapısını (p > eşik → yeni giriş yok) ve raporda "Pair Health GÜÇLÜ / CURRENT" göstergesini kaydediyor; bu kapının tasarımdan çıkarılması Tansu'ya sadakatle nasıl uyuşuyor?

04-040. Tansu'nun başarısız örneğinde (paket 53) strateji ≈79 bin TL'de yatay kalıyor; "hep yatırımda" kuralı yatay çizgi üretemez, bu da Tansu'nun sisteminde bir nakde geçiş ya da askı olduğunu mu gösterir ve tasarım bunu neden yok sayıyor?

04-041. "Bağı kopan çift ≈ −%21" KURALLAR'da bir sadakat kanıtı olarak geçiyor; çift ve dönem verilmemişken bu örnek hangi testle yeniden üretilecek ya da tasarımda neye karşı sınanacak?

04-042. Yıl içinde çiftin bağı koparsa (rolling p > 0,05, β kayması) tasarım yıl sonuna kadar hiçbir şey yapmıyor; bu bekleme süresindeki maksimum zarar sınırı hangi ölçüde raporlanacak?

04-043. Çiftin bir bacağı yıl içinde birleşme, devralma, işlem durdurma ya da kapanma yaşarsa pozisyonun hangi fiyattan kapanacağı ve payın ne olacağı tanımlı mı?

04-044. Yıllık seçimde düşen çiftin pozisyonu kapanır ve yeni çifte geçer: yıl başında ilk işlem günü hem satış hem alış masrafı doğar; bu yıllık toplu işlem hacmi AOF ve likidite sınırı açısından hesaba katılıyor mu?

04-045. Yine seçilen çift "işlemsiz devam eder" ama payı yılın içinde kâr/zararla kaymışsa pay yıl başında eşitleniyor mu; eşitleniyorsa işlemsizlik ifadesi yanlış mı olur?

04-046. "Eşit pay" 1.000.000 / 5 = 200.000 TL YORUM olarak yazılmış; çift sayısı 5'ten azsa pay 1.000.000/n mi 200.000 mi ve pay getiriyle bileşik mi büyüyor yoksa sabit mi?

04-047. M11 likidite sınırı (son 10 günün medyan TL işlem tutarının %2'si) çift bölmesine uygulanıyor mu; uygulanırsa tam rotasyon zorunluyken sınır aşıldığında pozisyon yarım mı geçilecek?

04-048. TASARIM 5.5 risk paketini çift bölmesine uygulamıyor ama KURALLAR "Risk paketi: ... SMA250 altı kapanışta çıkış (bütün aileler)" diyor; çift bölmesi için hangi metin geçerli?

04-049. Portföy kuralı en büyük düşüş %25'i aşamaz (m5); Tansu'nun VAKBN–GARAN sonucunda Max DD −%27,44 var, yani tasarım Tansu'nun kendi sonucunu reddeder; bu ölçüt bölme düzeyinde mi birleşik portföy düzeyinde mi uygulanıyor?

04-050. Stopsuz uzun-yönlü rotasyonun piyasa betası yaklaşık 1'dir; endeks düşerken iki hisse birlikte düşerse "göreli değer" kazancı yoktur, bu durumda fazla getiri ölçümü piyasa betasından nasıl ayrıştırılıyor?

04-051. K2 (aynı evrenin eşit ağırlıklı sepeti) çift bölmesi için tüm BIST100 evreni mi yoksa yalnız seçilen 10 hisse mi; ikisi arasında seçim sonucu değiştirebilirse hangisi önceden yazılmış?

04-052. K1 çift için "aynı çiftlerde, aynı sayıda geçiş, rastgele günlerde" diyor; rastgele günde hangi hisseye geçilecek (sırayla mı yoksa rastgele mi), ve ilk giriş günü rastgele mi?

04-053. B5 "rastgele sinyaller kuralın kendi ön şartlarını sağlayan günlerden seçilir" diyor; çift için ön şart |Z| ≥ 2 mi, aynı çift ve aynı yıl mı, yoksa hiç ön şart yok mu?

04-054. Gerçek kuralın geçiş sayısı yıldan yıla ve çiftten çifte değişiyor; K1 eşleştirmesi çift başına mı, yıl başına mı, bölme toplamına göre mi yapılıyor?

04-055. Rastgele kuralın nakit dönemi (ilk sinyale kadar) gerçek kuralla eşleştiriliyor mu; eşleştirilmezse K1 farkı nakit/yatırımlı süre farkından da gelebilir mi?

04-056. 1.000 rastgele tekrarla en küçük ulaşılabilir p ≈ 0,001 iken Holm düzeltmesi deneme sayısı arttıkça eşiği küçültür; çift ailesi için kabul eşiği fiilen ulaşılabilir kalıyor mu?

04-057. 50/50 tutma günlük dengelenen bir portföy mü yoksa başlangıçta bir kez alınan sabit adet mi; Tansu'nun "50/50 Buy&Hold" tanımı bilinmiyorken karşılaştırma kuralı hangi tanıma dayanıyor?

04-058. %100 tek hissede olan strateji ile %50/50 tutma farklı risk taşıyor; fazla getiri tanımı (günlük fark) riski normalize etmiyorsa K2 ve 50/50 karşısındaki "başarı" yüksek oynaklığın ödülü olabilir mi?

04-059. TASARIM 5.7 "Çift bölmesi için ayrıca aynı çiftlerin 50/50 tutulması" diyor, ama 5.12 kabul ölçütlerinde yalnız K1 ve K2 geçiyor; 50/50 tutma kabul kararında hangi role sahip?

04-060. "Yılların en az %60'ı pozitif" ölçütü ileri yürümede yaklaşık 9–10 yıla bakıyor; çift bölmesinde 5 yıl pozitif bir eşiği kısa örneklemle şanstan ayırt edebilir mi?

04-061. 5.9 "en az 100 işlem ve 60 farklı sinyal günü" istiyor; Tansu'da 20 ayda 6 geçiş görülüyor, 5 çift × 10 yıl ile bile işlem sayısı çiftler arası bağımlılıkla şişiyorsa örneklem şartı çift için nasıl okunacak?

04-062. 20 günlük blok bootstrap, ortalama tutma süresi 60+ gün olan çift pozisyonlarında otokorelasyonu yakalar mı; blok uzunluğu tutma süresiyle ilişkilendirildi mi?

04-063. Kâğıt üstü canlı dönem çift bölmesinde "günlük fazla getiri serisi, en az 6 ay"; 6 ayda 5 çiftle ~15 geçiş görülecekse doğrulamadaki etkinin yarısını saptama gücü hiç hesaplandı mı?

04-064. TASARIM 5.3 işlemi ertesi AOF'ta yapıyor, Tansu'nun etiketi "T+1 Open"; BIST açılışı tek fiyatlı seansla belirlenir ve AOF bütün günü yansıtır, bu iki fiyatın farkı çift geçişinde sistematik bir yönde sapma yaratmaz mı?

04-065. Çift geçişi aynı gün bir satış ve bir alış demektir; İş Yatırım AOF'u gerçek dolum fiyatı olarak ulaşılabilir mi, ve 200.000 TL'lik emir AOF'a yakın dolar mı?

04-066. Satış bedeli T+2'de takas olurken aynı gün başka hisseyi almak için kullanılabiliyor mu; tasarım bu geçişi aracı kurum teminat/gün içi kurallarından bağımsız varsayıyor mu?

04-067. Sabit %0,3 her yönde, bir geçiş = iki işlem = %0,6; Tansu'nun VAKBN raporu 6 geçiş için 2.054,78 TL maliyet gösteriyor (geçiş başına ≈ 342 TL), bu rakam %0,3/yön ile uyumlu mu ve maliyet formülü sadakat kapsamında mı?

04-068. Sinyal sonrası gün satılacak hisse kilitli tabanda ise geçiş yapılamaz; alınacak hisse kilitli tavanda ise giriş yok: yarım rotasyonda sermaye eski hissede mi, nakitte mi, ve ertesi gün Z koşulu hâlâ geçerli sayılacak mı?

04-069. Fiyat adımı (kademe) ve açılış seansı farkı, düşük fiyatlı hisselerde AOF ile kapanış arasında Z'de ölçülebilir fark yaratır; sinyal hesabı kapanışla, dolum AOF'la yapıldığında bu uyuşmazlık test ediliyor mu?

04-070. Çift bacaklarından biri brüt takas, tek fiyat ya da kredili işlem yasağı gibi tedbirliyse sinyal geçersiz mi sayılacak; TASARIM 8 madde 4 bunu bilinmeyen bırakırken çift kuralı bu bilgisizlikten nasıl etkilenecek?

04-071. Temettü ayrıldığı günde satış-alış zamanlaması, nakit temettünün vergilendirilmesi ve stopaj çift rotasyonunda hesaba katılıyor mu; "aynı temettü düzeltmesi" yalnız fiyat düzeltmesi mi yoksa elde edilen nakit mi?

04-072. Bedelli sermaye artırımı ve haklar çiftin bir bacağında Z'de sıçrama yaratır; düzeltmenin hangi veri kaynağında nasıl yapıldığı Yahoo ile İş Yatırım arasında farklıysa Z'ler eşleşir mi?

04-073. Sabit %0,3 masraf bankalar ile OYAKC gibi daha az likit hisseler için aynı; Corwin–Schultz spread'i (D dosyası, FROTO'da ort. %1,8) çift hisselerinde farklı çıkıyorsa kayma varsayımı çift rotasyonunu ne kadar iyimser kılar?

04-074. Kart sinyali 19:30'da (kapanış verisiyle) çıkıyor ama işlem ertesi günün AOF'unda; AOF ancak gün sonunda belli olduğundan kullanıcıya kartta "giriş bölgesi" ve geçiş emri hangi fiyat türüyle verilecek?

04-075. Sadakat kontrolü Yahoo verisiyle, gerçek sınama İş Yatırım verisiyle yapılıyor; iki kaynak arasındaki Z farkı ölçülürse çift seçiminin (p-değerleri) iki veride aynı çıkacağı gösterildi mi?

04-076. Sadakat başarısız olursa "ilgili parça YORUM kalır" (TASARIM 8 madde 5); çift ailesinin tüm kuralı zaten YORUM ağırlıklıyken sonuçların "Tansu'nun kuralı" diye mi yoksa "yaklaşık yeniden yapım" diye mi etiketleneceği tanımlı mı?

04-077. Pencere ve β türü Tansu'nun 2025–2026 VAKBN–GARAN çıktısına uydurularak seçilecek, sonra 2015–2026 tümü test sayılıyor; parametreyi seçtiğiniz dönemin test içinde kalması sızıntı değil mi?

04-078. Tansu'nun çiftleri sonuca bakılarak seçilmiş olabilir (KURALLAR §ekler); onun çiftleri kabul kararına girmiyor ama pencere/β kararı tam o çiftlerden çıkarsa seçim yanlılığı kurala geri sızmıyor mu?

04-079. D dosyası paket-98 görselinin NotebookLM ile yeniden çizilmiş olabileceğini not ediyor; VAKBN rapor.webp'in de yapay zekâyla yeniden çizilip çizilmediği doğrulandı mı ve sayılar sadakat kanıtı olarak ne kadar güvenilir?

04-080. D dosyasına göre VAKBN/CIMSA için pencere ≈ 60, AGROT/GARAN için ≈ 120–126 gün (çifte özel olabilir); tasarım tek pencere mi seçecek, çifte özel pencere seçiliyorsa bu parametre sayısını (5.10, 5.11) nasıl artırıyor?

04-081. Tansu'nun raporunda "Pair Quality 55,6 / GÜÇLÜ" ve "Rolling Corr 0,731" var; tasarımın seçimi yalnız p < 0,05'e dayanırken Tansu'nun "GÜÇLÜ" sınıfıyla ilişkisi hiç sınanmayacak mı?

04-082. Yalnızca p < 0,05 şartı düşük korelasyonlu (örneğin < 0,4) çiftleri de geçirebilir; D dosyasında rapor grafiğinde corr için olası alt kapı (~0,35–0,4) not edilmişken tasarım bu kapıyı neden kullanmıyor?

04-083. Tansu'nun AGROT/GARAN iki bacaklı sürümü long-short ve nakde kapatıyor, VAKBN/CIMSA sürümü long-only rotasyon; tasarım yalnızca ikincisini alıyor ama "Tansu'nun çiftleri" listesine AGROT–GARAN'ı koyuyor, hangi sürüme hangi çift ait?

04-084. Tweet "stat-arb'da momentum dönüş teyidi kâr çarpanı" diyor ve ayrıntıyı vermiyor; ΔZ tek gün dışında fiyat momentumu ya da başka bir teyit olabilirken tasarım ΔZ'yi neden "birinci el" saydı?

04-085. VAKBN grafiğinde 6 AL etiketi ve "6 geçiş" aynı sayı olarak kullanılıyor; ilk giriş de bir AL ise gerçek geçiş sayısı 5 değil mi ve maliyetin (2.054,78 TL) hesaplanması bu tanıma göre değişmez mi?

04-086. KURALLAR §tablo "Çift rotasyonu: güvenilirlik H" derken sapma formülü, pencere ve çift seçimi eksik olarak kaydedilmiş; kuralın merkezindeki üç belirsizliğe rağmen "H" etiketi neye dayanıyor?

04-087. D dosyası Tansu'nun örneklerini yalnızca "tek pair, tek dönem, seçilmiş" diye niteliyor ve OOS kanıtı yok diyor; tasarımın 2015–2026 kabul ölçütleri bu seçilmiş örneklerden çıkan parametreleri sınadığı için dolaylı olarak seçim yanlılığı taşımıyor mu?

04-088. Z eşiği ±2 ile birlikte iki bacaklı sürümde çıkış ±0,5 görünüyor; rotasyonda ±0,5'in rolü yoksa Z bu bandın içindeyken ΔZ ne kadar önemli ve soluk ±0,5 çizgileri ne için çizilmiş?

04-089. 5.10 küçük rastgele ızgara çift için hangi parametreleri oynatıyor (pencere, β türü, eşik, p eşiği, top-N); "pozitif hücre oranı" için geçme eşiği önceden yazıldı mı?

04-090. Sadakat aşamasında denenen sapma adayları ve pencereler (4 aday) deneme günlüğüne ve Holm düzeltmesine "deneme" olarak giriyor mu, "getiriye bakılmaz" ilkesi ise sonra getiriye göre en iyi aday seçilmeyeceğini nasıl garanti ediyor?

04-091. Aynı bölmede 5 çiftin geçiş günleri çakışırsa (ör. bankaların hepsi aynı günde sinyal verirse) çiftler arası korelasyon yüzünden bölme etkin olarak daha az bağımsız bahis içeriyor; bu bağımlılık p-değeri ve blok bootstrap içinde hesaba katılıyor mu?

04-092. Sinyal günü t'de hisse A'nın kapanışı ile B'nin kapanışı farklı seansta/likiditede oluşuyorsa (kapanış seansı, tek fiyat) Z'nin eşzamanlı olmayan fiyatlardan etkilenmesi ölçülüyor mu?

04-093. Piyasa genelinde çöküş günlerinde (ör. tavan/taban serileri) iki hissenin de kilitli olduğu durumda Z hesabı ve geçiş emri nasıl çalışıyor; bu günlerin simülasyonda oranı biliniyor mu?

04-094. Yıl başındaki yeni çiftin Z penceresi için 60–120 gün geçmiş veri gerekiyor; veri o hisse için yoksa (yeni halka arz, uzun süreli işlem durması) çift seçimden dışlanıyor mu ve bu dışlama sağkalım yanlılığı yaratıyor mu?

04-095. Seçim p-değeri 252 günlük log fiyatlarla hesaplanıyor; hisse bölünmesi ya da düzeltmesi olan çiftlerde düzeltilmiş mi ham mı fiyat kullanılacak ve bu seçim p'yi 0,05 sınırının iki yanına itebilir mi?

04-096. Sorgu-2 S46 "yılların %60'ı günlük fazla getirinin yıllık toplamıyla uygulanır" diyor; çift bölmesinde bir yılda tek bir büyük geçiş ya da seçilen çiftin rastlantısal bir sıçraması o yılın işaretini belirliyorsa ölçüt gürültüye açık değil mi?

04-097. Sadakat kontrolünde "6 geçiş" ve "Piyasada kalma %72,27" gibi ek sayılar da var; bunlar Z'den bağımsız doğrulama olarak kullanılıp kullanılmayacağı ve tutmazsa hangi parçanın YORUM kalacağı yazılı mı?

04-098. Tansu raporunda "Son Z −3,108" ve "VAKBN AL" birlikte; Z = −3,1'de bile ΔZ > 0 olunca AL deniyorsa, Z'nin −2'den −3,4'e kadar düşmesi sırasında tutulan X hissesindeki kayıp (Max DD −%27,44) kuralın doğal bir maliyeti mi diye tasarım hiç ayrıca ölçüyor mu?

04-099. Tansu'nun VAKBN–GARAN çıktısının dönem sonu ve veri kaynağı (yfinance `.IS` düzeltilmiş mi ham mı) bilinmiyorken +%52,86 ve Sharpe 0,929 gibi sayıların "elde edilebilir referans" olarak kullanılması tasarımda ne kadar yer tutuyor?

04-100. Çift rotasyonunun bütün parametreleri (spread, pencere, β, seçim penceresi, p eşiği, top-5, eşit pay) YORUM iken, bu aileyi "Canlı" yapan kabul ölçütü başarısızlığı ve ailenin Tansu'nun gerçek kuralını sınadığı iddiası arasında nasıl ayrım yapılacak?
