# Denetim: strateji-modulleri-taslak.md

Denetçi: bağımsız oturum. Her bulgu ham kayıtla (R001–R263) ya da görselle karşılaştırıldı.

## Tur 0 (ilk okuma)

Dosya ilk okuma anı: 06.10.2026 13:04 (yerel saat). Sürüm: 400 satır. Bölüm başlıkları: Neden · Yapı · Kaynak · Keşif parçaları · Tansu'nun bakış açısı (Kaynak ağırlığı, İ1–İ12, Kör noktalar) · Sisteme etkisi · Modül kataloğu (1 Rejim R1–R13, 2 Tarama T1–T13, 3 Kurulum D1–D18, 4 Teyit C1–C6, 5 Yönetim Y1–Y6) · Kapsam dışı · İlk dalga önerisi · Ortak yapı taşları · Açık sorular.

Yöntem: (1) sentez bölümündeki her tırnaklı parça, 263 kaydın tamamında alt dize olarak arandı ve atıf yapılan R numarasıyla karşılaştırıldı (yaklaşık 110 parça, 70'e yakın benzersiz alıntı). (2) Atıf yapılan her kayıt elle okundu. (3) Görseller açıldı: gorsel-paket-115, KAPLM (tweet-harmonik-xb…), ISKPL, SMRTG (paket 03), XU100 günlük (kaynak-xu100-1-eylul), paket 125.

Sonuç: 110 parçanın büyük çoğunluğu atıf yapılan kayıtta birebir var. Metinde bulunamayan parçalar: "retest yarar sağlıyor mu?" (hamda yok, B1); R212'nin iki görsel cümlesi (görselde var, biri birebir değil, B12); "20 bar içinde TEPKİ GELMEDİ" (görselde birebir). Geri kalan "bulunamayan" çıktılar tırnaklı etiketlerdir (AL sinyali, Tam/Defansif, bölgeli, yapı stopu esas). Asıl sorunlar işaretleme, ağırlık ve eksik karşı kanıtta; alıntı uydurması yalnız B1.

### Bulgular

**YÜKSEK**

**B1. "retest yarar sağlıyor mu?" Tansu'nun sorusu değil, hamda yok.**
- Yer: İ3 Hüküm ("Bu, Tansu'nun cevapsız sorusunu ('retest yarar sağlıyor mu?') ölçer") ve katalog C2 ("Açık soru … Tansu'da yanıtsız").
- Kanıt: 263 kaydın hiçbirinde bu cümle yok. Kaynak: `beyin/…/not-backtest-giris-sadeligi-risk-islem-gunlugu.md` satır 44, "Sentez (yapay zekâ)" bölümü: "Retest beklemek yarar sağlıyor mu, yoksa girişi fazla mı geciktiriyor? Bunlar test edilecek sorular; cevapları henüz yok." Ham kayıt R255 yalnız bağlantıdır (taslağın kendi kuralı: R245–R263 kanıt sayılmaz). Not, bu soruları paylaşılan metnin öğrettiği "test edilecek sorular" olarak anlatır. Tansu'nun kendi cevapsız sorusu olarak değil.
- Düzeltme: "Tansu'nun cevapsız sorusu" ifadesini sil. "Retest'in katkısı ölçülmemiş (R194 yalnız tek olumsuz örnek)" yaz. Ölçüm tasarımı (D'de limit ile tepki teyidi karşılaştırması) kendi gerekçesiyle kalabilir.

**B2. Y4 ve ilk dalga 5: NotebookLM infografiği "birebir (H)" ve Tansu kuralı sayılmış.**
- Yer: Katalog Y4 ("G (infografik) … H [p06]"); İlk dalga 5 ("kural görselde birebir (H)").
- Kanıt: `assets/gorsel-paket-115-…/01-position-sizing-yuzde1-2atr-sma250-stop.jpg`: sağ altta "NotebookLM" imzası. Taslağın kendi tanımı bu görseli (G-dış) yapar. Tansu'nun R212 metni yalnız şunu der: "Diyelim ki sermayenizin ancak %1'ini kaybetmek riskini göze alabilirsiniz ve diyelim ki işleme giriş bileşenlerinizden birisi 250SMA. (bu 200SMA 200EMA 250EMA' da olabilir, stratejinize kalmış.)". Yani %1 bir örnek ("diyelim ki"). 2 ATR ile bölme, acil stop ve gün sonu SMA250 çıkışı yalnız NotebookLM görselinde ve (M/belirsiz) R184'te var.
- Düzeltme: Y4 düzeyini G-dış yap, sadakat hedefini "yorum" olarak etiketle. İlk dalgada "birebir (H)" ifadesini kaldır. %1'in "diyelim ki" örneği olduğunu yaz.

**ORTA**

**B3. İ1 hükmü (rejim kapısı, "uzun ortalama altında alım yok"): karşı (T) kanıt atlanmış; ağırlık "Orta" bile iyimser.**
- Yer: İ1 Çelişki ve Hüküm; Sisteme etkisi 3; İlk dalga 1.
- Kanıt, aleyhte: R001 "Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın"; R026 (aynı kayıt, taslakta şok freni için kullanılıyor) "Sabit hareketli ortalamalar ani piyasa paniklerinde yavaş kalır ve size hatalı alım satım yaptırabilir"; R105 "ortalama kullanıyor iseniz eğimlere dikkat edeceksiniz". Bu üçü İ7'de kısmen geçiyor ama İ1 çelişki listesi yalnız ortalamaya dönüşü sayıyor.
- Kanıt, lehte: R131 "hareketli ortalamanın altındaysa, bu durum satış yönlü" (periyot yok). "250 günlük" yalnız G-dış (R212). "WMA21" yalnız XU100 aracı lejantı. R089 ("kırmızı bölgedeki yükselişler patır patır geri gelir") bir ortalama değil, tanımsız mavi seri/sıfır kesişimi (R049/R089/R093). Gerçek rejim dayanağı R026 (şok) ve R092 (fiyat+vol birlikte artış).
- Düzeltme: İ1'e R001, R026 ilk cümlesi ve R105'i karşı kanıt olarak yaz. Hükmü ikiye böl: şok freni (T, R026, R092; güçlü) ile ortalama kapısı (T R131 tek; periyot yorum). "uzun ortalama altında alım yok"u yorum etiketle. R089'u rejim dayanağı olmaktan çıkar. R118/R119'daki (sigma ve spread kuralı) rejim kanıtlarını ekle (bkz. B15).

**B4. R101 ve R099 (T) sayılmış; ikisi de uzun, başlıklı açıklama metni.**
- Yer: İ1 Çelişki ("(T) R101 'piyasa … ister yüzde 10 düşsün …'"), İ10 ("(T) … R101 'hiçbir strateji kusursuz değildir'"), Kör nokta 4 ("R101 'Peki Ya İp Koparsa?'"), İ5 Çelişki (R099 "92.354 TL'lik tüm bakiyesiyle").
- Kanıt: R101 yalnız ilk iki cümle Tansu'nun ("Anlatalım Nedir bu istatistiksel arbitraj meselesi … Son grafik ise arbitraj sistemimin çıktıları"). Devamı, "Peki Ya İp Koparsa?", "İşlem Stratejisi Nasıl Çalışıyor?" gibi başlıklı, "Özetle:" ile biten metin. Taslağın (M) tanımına uyuyor. R099'da "muhtemelen fiyatlar beklediğimiz ideal yakınsamayı yapmadan dalgalanmış … ve biz bu ilk trade'den zarar etmişiz" yorumu grafiği anlatan bir yazarın tahminidir. Rakamlar görsellerden doğrulanabilir; yorum metni değil.
- Etki: İ10 "Güçlü" hükmü R101'siz de 4 (T) ile ayakta kalıyor. Kör nokta 4 ve İ1 çelişkisi ise (M) etiketi alır.
- Düzeltme: R101 ve R099 gövde alıntılarını (M) işaretle. R099 sayılarını (G) görsel kaynağından ver.

**B5. İ6 Hükmü: "Rapor kazanma oranını tek ölçüt yapmaz; bu bizim kararımızdır, Tansu'nun değil" hamla çelişiyor.**
- Kanıt: R140 (Tansu "Dursun bir kenarda lazım olur" diyerek paylaşmış, (M)): "Yüzdelik doğruluk … acemi yatırımcıların bir takıntısıdır ancak bir işlem sistemini değerlendirmek için çok önemli bir kriter değildir"; temel ölçüt ödül/risk ve maksimum sermaye erimesi, "Kümülatif Sermaye grafiği". R234 (T): "%55 başarı oranıyla para kazanmak için, her işlemde Risk/Ödül oranını en az 1:1.5 … ayarlamak gerekir". R115: "ham getiriden bir miktar feragat ederek karşılığında çok daha huzurlu bir eğri". Taslak R140'ı yalnız "Kapsam dışı"da bir cümleyle geçiyor, İ6'da yok.
- Düzeltme: İ6 çelişkisine R140 (M, paylaşılmış) ve R234 ekle. Hükmü "kazanma oranı tek ölçüt değil: Tansu'nun paylaştığı kaynak (M R140) ve kendi sözü (R234 R/R) aynı yönde" olarak yaz. Kararın "bizim" olduğu iddiası kalkar.

**B6. İ5 "Güçlü" fazla iyimser; %1 ve 2 ATR Tansu kuralı değil.**
- Yer: İ5 başlığı ve Hüküm ("tek hisse modüllerinde %1 risk / 2 ATR lot").
- Kanıt: bkz. B2. İ5'te (T) sayımı: R212 (örnek), R211 (volatilite arttıkça pozisyon küçülür; gerçek T), R201 (likidite; kayıp bütçesi değil), R113 ("Portföy optimizasyonu ve volatilite trading arasındaki ilişki huzurlu gecelerin anahtarıdır": kayıp bütçesi değil, portföy), R026 ("sadece elinizdeki riski yönetin": genel). Kayıp bütçesi ile adet ilişkisini kuran T cümle yalnız R212 ("kaç lot almanız gerektiğini biliyor musunuz?" ve %1 örneği) ile R211. Taslağın Güçlü eşiği: en az 3 (T)/(G).
- Düzeltme: Başlığı "Orta" yap (ya da "Güçlü: boyut volatiliteyle ters (R211, R212). Orta: %1 ve 2 ATR G-dış/M"). R113 ve R201'i bu ilkenin dayanağı olmaktan çıkar (R201 likidite için ayrı satır).

**B7. İ4 / Sisteme etkisi 2: çıkış zinciri hamdan tam çıkmıyor.**
- Kanıt: R224 (T): "kar alma %10 (sizin belirleyeceğiniz), ikinci kar alma, trialling stop noktası … önceki günün en düşüğünün altında kapanış ve %50 satış, ve emergency stop 2atr". R239 (T): ilk kar alma = iz süren moda girdikten sonra "bir gün öncekinin en düşüğünün altında kapattı ise orasıdır. %50'sin satın". R233 (M gövde + T kapanış cümlesi): ilk %50 RSI 70 reddinde, ikinci %50 önceki gün dibi altı kapanışta. Yani "R233 ve R239 aynı %50 + önceki gün dibi kuralı" yanlış: R233'te önceki gün dibi ikinci %50. Sisteme etkisi 2'deki "TP1'de %50" (T) değildir: bu (M) R203 ("pozisyonun bir kısmı (örn. yarısı) kapatılır ve Stop Loss … giriş fiyatına çekilir") ve pk123 (G-dış/M tablo). R239'da 1.5 ATR iz süren stopun mesafesi değil, aktivasyon eşiğidir ("Giriş + 1.5ATR noktasına geldiğinizde artık hedef izleyeceksiniz").
- Ayrıca T kaynaklar genel stratejilerdir (R224, R239, R233 RSI). Harmonik/formasyon modülleri için T kaynak yalnız geçersizlik (R019, R043) ve R090 "FIBO seviylerine göre iz süren takibe göre TP kovalanır".
- Düzeltme: Zinciri kaynak etiketiyle ver: [T R224/R239] 1.5 ATR aktivasyon, önceki gün dibi altı kapanışta %50, 2 ATR acil; [M R233] RSI 70 reddi; [M R203] TP1'de %50 + stop girişe. Hükmü "formasyon modülleri için Tansu çıkışı = geçersizlik + Fib takip (R090); ATR zinciri genel (T) ve ölçümde denenir" yap.

**B8. İlk dalga ve Sisteme etkisi 7: M kaynaklı kurallar "sadakat" adayı sayılmış (kendi kuralıyla çelişki).**
- Kanıt: Sisteme etkisi 7: "Gösterge stratejileri (RSI 30 R233, Williams %R R170, A/D-EMA R139) parametreleri açık olduğu için sadakat testine kolay aday". R233 giriş kuralı ve R170 kuralları (M). Sisteme etkisi 6 ise (M) kaynaklı kurala "yorum" der. R139'da operatör (`>`/`<`) kayıt metninde yok.
- Düzeltme: Bu üç strateji "açık parametreli ama (M)/(G)" olarak yaz; sadakat sınıfı "yorum"; yalnız R233'ün T kapanış cümlesi (grafik anlatımı) Tansu kullanımına dayanak.

**B9. İ8 ve ilk dalga arasında tutarsızlık: momentum ön eleme.**
- Kanıt: R189 (T): "tüm hisseler önce momentum sistemimden geçiyor sonra ayrıntılı yazıyorum"; R137 beş aşama. İ8 "Güçlü" der. İlk dalga (rejim → D1/D2 → C1 → Y) momentum kapısı içermiyor; İ12 momentumu "seçim katmanı, ilk dalga dışı" sayıyor. Bu bir ölçüm basitleştirmesi, ama yazılı değil.
- Düzeltme: İlk dalgada "Tansu'nun akışında bu kurulumlar momentum ön elemesinden geçen hisselerde aranır; ilk dalga ön eleme olmadan koşar, sonuç yorumlanırken bu not edilir" cümlesini ekle.

**B10. Katalog kaynak işaretleri hamla eskimiş (Tur 0 sürümünde).**
- R3 "Düzey A": R026 (T). D1 "– kapı (A)": R019 (T) "BC, AB'yi aşamaz … C'den sonra fiyat A'yı geçerse patern bozuldu sayılır". D3 ayrı tarayıcı "(p01 K2 notu, A)": R011 (T). D4 Trident D = (B×C)/A "(A)": R090 (T, kayıt sahibinin kendi metni). D11 EMA sıkışması: R127, R132, R082, R125 (T). D18 "HalfTrend ve Williams'ın Tansu'ya atfı doğrulanamadı": R148 (T, Tansu kodu paylaşıyor "Nice") ve R170 (T "Şöyle bir strateji yazalım", kural gövdesi M). D12 "Z formülü yok": kopma kapısı için R034/R228/R262 (T) kointegrasyon. D13/D14 "(A) zincir/kural": R197/R199 (M) ve R205 (T). T3 "Eşik oran mı pay adedi mi belirsiz": R083 (T) "Dolaşımdaki pay adedinin <%30 olduğu senetler ile ilgili … stratejik taramalar" (oran, %30), "KAP ile verileri alabiliyoruz". R10 "A (+G)": R186 (T, "benim kullandığım mantık şöyle: fiyat VWAP üstünde + POC üstündeyse sadece alış yönlü bak").
- Düzeltme: Bu satırlara "Ham:" notu ve T/M/G-dış işareti ekle (Tur 1'de bir kısmı yapıldı, bkz. Tur 1).

**B11. İ3: "D oluşumunu teyit için B kırılımı" bağlamdan kopuk; R197 "limit emir" içermiyor.**
- Kanıt: R090'da "D oluşumunu teyit etmek için ise B noktası kırılımı gerekir" cümlesi satış yönlü formasyon paragrafında ("Satış yönlü formasyon … D noktasından sonra teorik olarak düşüş olacaktır"). Alış yönlü paragrafta teyit yok: "teorik D noktasından yani dipten pozisyon alınır". Yani "tepki teyidi" Tansu'nun alış yönlü kullanımı için dayanak değil. R197 (M) "temas ettiğinde ALIM (LONG) yönlü işlem aranır"; "limit emir" ifadesi yok. "Limit Alış emri" R199'da var.
- Düzeltme: R090 alıntısına "(satış yönlü formasyon için)" ekle; BIST'te kısa bacak yok notu ile bağla. "(M) R197, R199 limit emirle temas girişi" cümlesinde R197'yi "temas girişi", R199'u "limit alış" diye ayır. İ3 hükmü (iki giriş koşulur) yine geçerli.

**DÜŞÜK**

**B12. R212 alıntısı birebir değil.** İ1: "(G-dış) R212: 'Fiyat, 250 günlük hareketli ortalamanın altında bir kapanış yaparsa pozisyondan çıkın'". Görselde: "Fiyat, 250 günlük hareketli ortalamanın altında bir kapanış yaparsa pozisyonundan çık." Düzelt. Ayrıca görselde bu kural çıkış (gün sonu stop); T metinde 250SMA "giriş bileşeni". İ1 bunu alım kapısı yapıyor: yön farkını not et.

**B13. R109 yanlış bağlam.** "kitaptaki modeli aynen uygulama (T R111, R109)": R111 tam tersini söyler ("sadece kitaplarda gördüğünüz hazır modelleri olduğu gibi uygulamaya çalışmak sizi başarıya götürmez"). R109 "önce kağıt üzerinde çöz, sonra koda dök"tür. Düzelt: "kitaptaki modeli aynen uygulamama (R111); önce kağıt-kalem (R109)".

**B14. R227 yanlış anlatılmış.** İ11: "(T/M) R227 gerçek emir defteri verisinin olmadığını söylüyor". R227: COT "Yönetilen Para" long/short oyuncu sayısı, açık pozisyon ve "trader count" verisi "elimizde yok … yfinance ve standart borsa verilerinde" yok. Emir defteri R225 ve R126 paketinde. Düzelt: "açık pozisyon/oyuncu sayısı (COT) verisi yok; vekil (proxy) kullanıldı".

**B15. Eksik (T) kanıtlar (kural/strateji).**
- R105 (T): "Bana sistem ile ilgili gelen sorulara verdiğim cevaplar hep aynı. Arkadaşlar ortalama kullanıyor iseniz eğimlere dikkat edeceksiniz. Momentum trader iseniz sinyal eğiminize dikkat edeceksiniz." Tansu'nun kendi sözüyle tekrar eden ilke: eğim. İ listesinde yok (T9 yalnız katalogda). R137 aşama 2 de aynı yönde.
- R171 (T giriş + açıklama) ve R157 (T kapanış cümlesi): doğrulama ve yanlışlama görüşü ("Eğer testler stratejinin başarısız olduğunu söylüyorsa … o 'popüler' kurala yatırım yapmaktan vazgeçmenizi sağlar"; "iki satır kod yazayım ya da yazdırayım sevdası … orta ve uzun vadede yıkıma sebep olabilir"). Taslak ekseni "5. Doğrulama: … yanlışlama hakkındaki görüşü" diyor; İ6 bunları kullanmıyor.
- R172: "Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR" (başlıklı metin, (M) olabilir) "D'de limit" (dipten alım) ve R227 "Dip yakalanmıştır" ile çelişir; İ3'te çelişki olarak geçmiyor.
- R114 (T kapanış): "doğru formasyonu doğru seviyede, sıfır duyguyla ve tam zamanında yakalamak. Sonrası zaten trendin peşine takılmaktan ibaret." İ2/İ4 için özet T cümle.
- R077 (T): "Rehavet ortamı vardır ve fiyat bir yöne kırılacaktır." İ9'a eklenir.
- R118 ve R119 (T-ağırlıklı rapor yorumu, birinci çoğul): "Spread yüksek, Sigma yüksekse; o tahtadan uzak durun ya da stop-loss seviyelerini çok geniş tut", "Sigma ani bir sıçrama görmediğimiz sürece". İ1 rejim/şok için ek kanıt (katalog R7/R8'de var, İ1'de yok).
- R090 (T): "Strtejiyi açıklamak isterdim ama artık strateji vs yazmıyorum." Kör nokta 3'e eklenir. R090'ın son paragrafı ("Lindsay'in Trident'i … Kuantum İpi") başka bir hesabın yanıtıdır; alıntı yapılmamış, doğru.
- Düzeltme: Bu maddeleri ilgili İ bölümlerine ekle.

**B16. R078 / Y5 "olumsuz sonucu da paylaşıyor".** Katalog Y5 ve Açık sorular (parça 04): "Tansu'nun kendi çıktısında pasifin gerisinde". R078 tweet metni: "sadece gün sonu eklemeler eksiltmeler ile sistem getirisi 1.5 yada %27". Metin pasifin (%27,81) önde olduğunu söylemiyor; görselde var (%26,76 karşı %27,81). "Olumsuz sonucu paylaşıyor" yerine "tabloda görünüyor, anlatımda yok" (Kör nokta 1'in destekleyici örneği).

**B17. Küçük atıf ve etiket sorunları.**
- İ1: R089 etiketsiz; indikatör kimliği belirsiz (B3). İ2: "R233 RSI 30, R170 Williams %R" gövdeleri (M).
- İ5: R113, R201 dayanak olarak gevşek (B6). İ8: R028 iki volatilite kodunun kesişimi, akış aşamaları değil (yalnız "kesişim" kavramı).
- İlk dalga 1: "14.443,45" yalnız tweet metninden (R258 bağlantı; not yapay zekâ okumasına dayanıyor), "(not)" olarak etiketli ama "birinci el (G)" cümlesinin yanında okunuyor. Ayır.
- R232 (likidite eşiği "(M)"): kayıtta "Geçen gün bir dostum", "Detaylı bir çalışmam var onu sadeleştirip … paylaşırım" gibi kişisel ses var; (T/M) yazılabilir.
- R170 "Bi bakın bakalım backtesti nasıl": ölçüm yok kanıtı olarak değil, "backtest'e bakın" daveti olarak da okunabilir (kayıtta görsel yok; ölçüm var mı bilinmiyor).

### Doğrulananlar

1. İ bölümlerindeki tırnaklı alıntıların neredeyse tamamı atıf yapılan R kaydında birebir (R014, R019, R024, R026, R036, R037, R043, R080, R081, R082, R085, R087, R090, R092, R098, R100, R102, R111, R125, R127, R131, R132, R137, R138, R145, R166, R189, R194, R201, R206, R210, R211, R222, R224, R234, R238, R240 ve diğerleri).
2. R245–R263 (19 kayıt) yalnız bağlantıdır; taslağın bu iddiası doğru.
3. gorsel-paket-115 görseli NotebookLM imzalı; (G-dış) etiketi İ1 ve İ5'te doğru.
4. gorsel-paket-111 görselinin "TAKVİM GÜNLERİNİ SAYIN" düzeltmesi ve NotebookLM imzası (beyin notu) tutarlı.
5. KAPLM görseli: "D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ) | [Ek bilgi] C sonrası son 10 günde BEKLENEN yönde: DÜŞÜYOR" birebir. R014'ün "10 gün" ifadesi D sonrasıdır; görselin 10 günü C sonrası. Katalog C1 bunu doğru ayırıyor.
6. ISKPL görseli: 5 patern, 5 hedef, 0 stop; tarihler 2024-04-03, 2024-08-13, 2025-03-21, 2025-06-19, 2026-01-21; %610,01; 710.006,23. SMRTG: 12 patern, 7 hedef, 3 stop, 2 açık; %305,33; 405.327,42. Katalog sayıları doğru.
7. XU100 1 Eylül görseli: "WMA Close 21", "GÜNLÜK 14229.01", "SETUP: 45/100", "YAPI: GEÇİŞ / BULLISH CHoCH". Katalog R4 doğru.
8. Paket 125 görseli: "STOP: 104.34 / ATR: 4.62", çözünürlük düşük; katalog Y3 notu doğru.
9. Katalog satır sayısı 56 = 13 + 13 + 18 + 6 + 6 (Tur 0 sürümü).
10. T işaretleri doğru: R026, R092, R131, R001, R244, R014, R019, R080, R081, R085, R087, R100, R102, R201, R211, R224, R239. (M) işaretleri doğru: R220, R226, R187, R203, R222, R230.
11. R137 beş aşama ve "Bu sistem satılık değil" alıntıları doğru; Kör nokta 7 (ML'yi sevmiyor ama ANN) R021, R234, R137 ile uyumlu.
12. Taslağın sayı ve tarih örnekleri beyin notlarında bulundu: 710.006,23 (iskpl), 152.862 (vakbn-garan), 405.327 (paket 03), 126.764 (paket 37), 92.354 (paket 52), 389,30 (paket 58), 0,2389 (paket 06).

### Özet (Tur 0)
Alıntı: ~110 parça. Bulgu: 2 YÜKSEK, 9 ORTA, 6 DÜŞÜK (B1–B17; B3–B11 ORTA, B12–B17 DÜŞÜK; B15 birleşik).

## Tur 1 (katalog ve ilk dalga güncellemesi)

Okuma anı: 06.10.2026 ~13:12. Dosya 413 satır. Denetlenen: koordinatörün listesindeki 16 değişiklik (R1, R3, D1 kapı, D2, D3, D11, D12, D17, D18, D19, C1, Y1, Y3, Y4, İlk dalga, Medyan satırı, katalog başlığı).

Durum: Tur 0'dan B1 (retest sorusu) ve İ bölümlerindeki B3–B8 bu turda değişmedi (İ1–İ12 metni aynı); hâlâ açık. B2 kısmen giderildi (aşağıda T1-4). B10 büyük ölçüde giderildi (R3, D1 kapı, D3, D11, D18, D12 işlendi; D4 Trident (R090), T3 (R083), R10 (R186) hâlâ açık).

### Bulgular

**ORTA**

**T1-1. D1 kapı satırı: "Oranlar (T) R080" yanlış işaret.**
- Yer: D1 "– kapı (T)" satırı: "Oranlar (T) R080: BC 0.382/0.50/0.618, CD 1.00/1.27/1.618".
- Kanıt: R080'de Tansu'nun cümlesi yalnız son satır: "D noktasına bakın, talep toplama bölgesine bakın, hissenin tepkilerine bakın. Doğru kod böyle yazılır." Oranlar, kayıttaki uzun başlıklı gövdede: "4 Kritik Noktanın (A, B, C, D) Bulunması: … BC Düzeltmesinin Ölçülmesi (Fibo Oranı): … (0.382, 0.50, 0.618 vb.) … CD Hedefinin Ölçülmesi (Uzantı): … (1.00, 1.27, 1.618 vb.)". Bu (M) metindir ("vb." ile açık uçlu). R019 (T) yalnız "BC, AB'yi aşamaz BC tam 1.00 olabilir" der. Kapı (T) R019'dan doğru.
- Düzeltme: "Oranlar (M) R080 (Tansu 'Doğru kod böyle yazılır' diye onaylamış)" yaz. İlk dalga seçim gerekçesindeki "oranları (T) R080'de" cümlesini aynı şekilde düzelt.

**T1-2. D19 (RSI 30) ilk dalgada: sadakat hedefi yok; sınıf (M).**
- Yer: D19 "Sadakat hedefi: yok (yalnız işaretli grafik)"; İlk dalga seçim gerekçesi ("D19'un giriş ve iki aşamalı çıkışı R233'te tam").
- Kanıt: R233 kaydında görsel yok (kayıtta `[img]`/G1 satırı yok). Beyin notu `tweet-rsi30-giris-iki-asamali-cikis.md` satır 59: "grafik görseli bu kayıtta yapıştırılmamış". "Yalnız işaretli grafik" yanıltıcı: elde grafik de yok. Giriş ve çıkış kuralı (M) gövdesinde; T olan tek cümle: "Üst paneldeki mumlar sırası ile giriş noktası, trailling noktası, ilk %50 kar aldiğımız RSI70 reddi ve ikinci %50 kar aldığımız önceki mumun en düşüğünün altında kapanış".
- Etki: Kaynak ağırlığı kuralı (M kural = "yorum") ve "Sadakat önce" ilkesi (Tansu'nun kendi örneğini yeniden üretmek) ile çelişir. "Kural açık olanlar önce" ölçütü sadakat ölçütünün yerine geçmiş.
- Düzeltme: D19 sadakat hedefini "yok (grafik yapıştırılmamış)" yaz. Sınıfı "yorum (M kural) + T kullanım doğrulaması". İlk dalgaya girmesi kalırsa gerekçeyi "sadakat testi değil, açık kural ölçümü" olarak değiştir.

**T1-3. İlk dalga zinciri: C1 yalnız formasyon (D noktası) modüllerine uyar.**
- Yer: "kurulum (D1, D19, D11) → teyit (C1: D'de limit / tepki teyidi iki kol)".
- Kanıt: C1, "D gerçekleşti ama … TEPKİ" penceresidir; D19'da D noktası yok (RSI kesişimi), D11'de D noktası yok (R198 (M): sıkışma → breakout mumu veya retest; stop demand altı). Y2 hedef merdiveni de harmonik/Fib hedefidir; D19'un hedefi RSI 70 reddidir.
- Düzeltme: Zinciri modül başına yaz: D1 → C1; D11 → C2 (breakout/retest; R198 M); D19 → kendi çıkışı (R233) ve Y3. Y2'yi "yalnız D1" olarak sınırla. "ortak yönetim" ifadesine "D19 kendi iki aşamalı çıkışını kullanır" notu ekle.

**T1-4. Y4: Düzey düzeltildi, "H" ve gerekçe satırı kaldı (B2 kısmen giderildi).**
- Yer: Y4 satırı: H/K/X "H [p06]"; son sütun "p06 görseli kuralı birebir veriyor (H)".
- Kanıt: Düzey artık "G-dış + T" (doğru, gorsel-paket-115 görselinde "NotebookLM"). "H = kural birinci elden belli" tanımı G-dış için geçmez. T alıntı "sermayenizin ancak %1'ini kaybetmek riskini göze alabilirsiniz", R212'de "Diyelim ki" ile başlar (örnek). "250SMA" R212'de "işleme giriş bileşenlerinizden birisi" (giriş), görselde ise çıkış (gün sonu stop).
- Düzeltme: H/K/X'i "K (yorum)" yap; son sütunu "kural (G-dış) NotebookLM; T R212 yalnız %1 örneği ve 250SMA giriş bileşeni" olarak yaz. Sadakat hedefi "yok (G-dış)". İlk dalgadaki eski liste madde 5 ("birebir (H)") zaten "Eski öneri" altında, ama silinmesi daha temiz.

**T1-5. İlk dalga: D11 için "EMA 5-8-13" varyantı sadakat çapası olarak zayıf.**
- Yer: "D11 EMA 5-8-13", gerekçe "D11'in ayarı (T) R198'de, eşiği yorumdur".
- Kanıt: D11 satırında sayısal örnek (G) KRDMD (EMA20/50/100/200; tolerans %1,2; min 3 gün; 17.12.2025 → 14.01.2026; ort. oran %0,64). EMA5/8/13 için satırın kendisi "eşik yok" diyor. R198'deki T cümle ("Ben 5-8-13 kullandım.") tek cümle ve (M) gövdede örnek olarak EMA 20/50/100 geçiyor. R125 (T) açıkça "parametrelerin detaylarını verip stratejimi anlatamam" der; R127 (T) rasyoyu okura bırakır. Yani her iki varyantın eşiği yorum; ama KRDMD sayıları sınanabilir hedef verir.
- Düzeltme: D11 ilk dalgada KRDMD (20/50/100/200) çapasıyla yaz; 5-8-13'ü varyant olarak ekle. R125'i "Ham:" notuna ekle.

**DÜŞÜK**

**T1-6. D19 alıntısı birebir değil.** Ham: "ilk %50 kar aldığımız RSI70 reddi"; R233'te "ilk %50 kar aldiğımız RSI70 reddi" (yazım hatası "aldiğımız"). Yazım hatalarını koru (kayıt başlığı kuralı: birebir).

**T1-7. C1: "20 bar (görsel) ve 10 gün (ham) aynı pencerenin iki değeri" kanıtsız.** KAPLM görselinde iki ayrı ifade: "D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ)" ve "[Ek bilgi] C sonrası son 10 günde BEKLENEN yönde: DÜŞÜYOR". "Son 10 günde belirsizleşti" durum değişiminin yakınlığı da olabilir. Tur 0 sürümü "iki ayrı parametre olabilir" demişti; bu daha doğru. "İkisi de koşulur" kararı yerinde.

**T1-8. D18 satırında eski cümle kaldı.** "HalfTrend ve Williams'ın Tansu'ya atfı doğrulanamadı" Ham notu ile çelişiyor (R148 Tansu'nun kod satırı "Nice"; R170 "Şöyle bir strateji yazalım"). Eski cümleyi "atıf: Tansu paylaşmış; Williams kural gövdesi (M)" ile değiştir.

**T1-9. D12 Ham notu: R228 genel kural, Nisan 2025 sessizliğini açıklamıyor.** Satır zaten "kointegrasyon p 0,048 CURRENT" gösteriyor (rapor kapısı geçiyor). "ilk sınanacak kapı kointegrasyon" varsayım; "olabilir" olarak yaz. Daha doğrudan T kayıt R034 ("Herkes cointegration bakmak istiyor ama çok azı rolling cointegration ile zamanla bozulmayı önlüyor") atıf almamış; ekle.

**T1-10. Y3 / İ4 kalıntıları (B7 açık).** Y3 satır başlığı "TP1'de %50, stop girişe …" parça/M kaynaklı (R203, pk123); Düzey "T (ham)" hepsini kapsıyor görünüyor. R233'te ilk %50 RSI 70 reddi (D19 bunu doğru yazıyor), R224'te ilk kâr %10 (kullanıcı belirler). İ4 ("R233 ve R239 aynı %50 + önceki gün dibi") ve Sisteme etkisi 2 ("TP1'de %50") değişmedi.

**T1-11. Küçük bayat satırlar.** D1 başlığı "r 1,0 ve 1,27" (Ham R080 1.618'i de sayıyor). D17 "Tansu 'geri dönmek zorunda' diyor": bu cümle (M) R226'dır, etiket yok. Okuma anahtarındaki "Düzey eski işarettir; ham esastır" kuralı iyi, ama okuyucu D17'de bunu görmez.

### Doğrulananlar (Tur 1)

1. Yeni "Ham:" alıntıları kayıtta birebir (11 kayıt, 20'ye yakın parça): R092 (iki parça), R026 ("Yeni al sinyallerini tamamen durdur"; "son X günlük dalgalanmasını son 1 aylık dalgalanmasıyla"), R019 (iki boşluk dahil), R011, R222 ("Ödül / Risk < 1.5 ise … işleme girilmez"), R014, R198, R132, R127, R101 ("Z-Skoru +2.0 seviyesini yukarı kırarsa", "normale (0.5 seviyelerine)"), R228, R156, R053, R170 ("Williams %R: 14", "Bi bakın bakalım backtesti nasıl"), R148 (kod satırı), R224 (iki parça, "%10 (sizin belirleyeceğiniz)"), R234, R212, R001. Tek sapma: T1-6.
2. İşaretler doğru: R3 ve R1 (T) R026 ve R092; D3 (T) R011; D1 kapı (T) R019; D11 R198, R132, R127 (T); D12 R101 "biçimi (M)'ye yakın" (Tur 0 B4 ile uyumlu); D18 R170 (M) ve R148 (T); Y4 G-dış (NotebookLM imzası görselde); D2 R222 (M).
3. Y1: dört stop ailesinin dayanakları hamla uyumlu: yapı (R019, R043), ATR (R224, R212), yüzde ve R/R (R234 örnek, R230 M), SD bandı (R187 M). "Yapı esas" hükmünün kaldırılması hamla tutarlı.
4. D2'nin ikinci dalgaya alınması gerekçesi (pk123 boğa D formülü ters; R222 gövdesi M; "Tansu" sınıfı birebir üretilemez) hamla ve beyin notuyla tutarlı.
5. Katalog sayımı: 13 + 13 + 19 + 6 + 6 = 57; başlık doğru.
6. Medyan satırı: R001 birebir; (T) etiketi doğru; "anomali kuralı G (|30g| > %50)" paket 07 ile uyumlu.
7. D19'un kural özeti R233 gövdesiyle uyumlu: RSI(14) 30 altından yukarı kesme + üstünde kapanış; RSI 70 üstünden altına kapanışta %50; önceki mumun LOW'u altında kapanışta kalan %50; "risk/ödül hedefi" sayısı ve stop yok.

### Özet (Tur 1)
Bulgu: 0 YÜKSEK, 5 ORTA (T1-1 ... T1-5), 6 DÜŞÜK (T1-6 ... T1-11). Tur 0'dan açık kalanlar: B1 (YÜKSEK, İ3/C2 "retest" sorusu), B3–B9, B11 (İ metni değişmedi).

## Tur 2 (yazarın Tur 0 + Tur 1 düzeltmeleri)

Okuma anı: 06.10.2026 13:19. Dosya 469 satır. Yöntem: sentez (satır 70–268) ve katalogdaki tüm tırnaklı ve «» parçalar 263 kayda karşı yeniden tarandı; yeni alıntılar elle okundu; ilk dalga tablosu ve değişen katalog satırları okundu.

### Tur 0 / Tur 1 bulgularının durumu

- Giderildi: B1 (kısmen; bkz. T2-1), B2/T1-4, B3, B4, B5, B6 (kısmen; T2-2), B7 (T1-10 dahil), B8, B9, B10 (D4, T3, R10 eklendi; T2-5), B11, B13, B14, B15, B16, T1-1, T1-2, T1-3, T1-5, T1-6, T1-7, T1-8, T1-9, T1-11.
- Açık / kısmen: B17 kalanları (T2-6).

### B12 kesinleştirme (R212 görsel cümlesi)

`gorsel-paket-115-…/01-position-sizing-yuzde1-2atr-sma250-stop.jpg` yeniden açıldı. "Gün Sonu Stop'u" kutusu: "Fiyat, 250 günlük hareketli ortalamanın altında bir kapanış yaparsa pozisyon… çıkın." Sondaki sözcük "çıkın" (Tur 0'daki "çık." yanlıştı). Ortadaki sözcüğü ("pozisyonundan" mı, "pozisyondan" mı) 680 px genişlikte kesin ayırt edemiyorum; okumam "pozisyonundan" yönünde ama emin değilim. Taslak cümleyi artık tırnakla vermiyor; konu kapalı. Tırnakla verilecekse orijinal dosyayı büyüterek kontrol et.

### B1 için düzeltme (denetçi)

Tur 0 B1'de fazla kesin yazdım. `not-backtest-…md` satır 35: Levent'in paylaştığı ana metin tarayıcıda Tansu'nun 2 Eylül 2026 21:13 gönderisiyle eşleşmiş; "Retest beklemek yarar sağlıyor mu…" cümleleri bu metnin özetindeki "test edilecek sorular" arasında. Yani soru Tansu'nun gönderisine ait olabilir. Ham kayıtta yalnız bağlantı var (R255) ve eşleşme yapay zekâ doğrulaması. "Tansu'nun cevapsız sorusu" ifadesini kaldırmak doğru (kanıt sayılmaz); ama "Tansu'nun değil" demek de kanıtsız. Bkz. T2-1.

### Bulgular

**ORTA**

**T2-1. C2 ve İ3: "Tansu'nun değil" iddiası kanıtsız (B1 düzeltmesi aşırı gitti).**
- Yer: C2 son sütun ("sorusu Tansu'nun değil, beyin notunun yapay zekâ sentezinden (denetim B1)"); İ3 Hüküm parantezi.
- Kanıt: not satır 35 ve 44; ham R255 yalnız bağlantı.
- Düzeltme: "ham metin yok (R255 yalnız bağlantı); beyin notu soruları Tansu'nun 2 Eylül gönderisine bağlıyor ama doğrulanamıyor; kanıt sayılmadı" yaz. "(denetim B1)" gibi iç referansları hüküm metninden çıkar; düzeltme geçmişi okumayı zorlaştırıyor.

**T2-2. İ5 "Boyut volatiliteyle ters: Güçlü" kendi eşiğine uymuyor.**
- Kanıt: Güçlü = en az 3 (T)/(G). Sağlam dayanak R211 (T). R212 (T) yalnız "kaç lot almanız gerektiğini biliyor musunuz?" ve %1 örneğini verir; volatiliteyle ters ilişki R212 metninde yok, yalnız (G-dış) görselde ("2 ATR değerine bölün"). R184 (M). R097 yalnız proje niyeti.
- Düzeltme: başlık "Orta (R211 T; R212 T dolaylı; ATR bölen G-dış/M)". Sisteme etkisi 2'de "Boyut volatiliteyle ters (T)" → "(T R211)".

**T2-3. İlk dalga D1 satırı: sadakat hedefi ile teyit kolları farklı işlemleri ölçüyor.**
- Yer: İlk dalga tablosu D1: teyit "C1: D'de limit / tepki teyidi"; sadakat "ISKPL 5/5, SMRTG 7/3/2".
- Kanıt: R018 (T): "AB=CD 1000 günlük C noktasından alım yapılsa idi D satış karları". ISKPL görseli: "Tarih (C)", "hedef": işlem C'den D'ye. C1 penceresi D sonrasıdır (R014); D'de limit girişi D'den başlar. Tansu'nun sonuç tablosunu üretecek kol (C girişi, D çıkışı) tabloda yok.
- Düzeltme: D1'e üçüncü kol ekle: "C girişi → D çıkışı (sadakat kolu: ISKPL/SMRTG)". Yön notu (SMRTG C→D aşağı yönlü; BIST'te kısa) yeni tabloda düşmüş; geri koy.

**DÜŞÜK**

**T2-4. İ1 "Şok freni Güçlü" sınırda.**
- Kanıt: sağlam (T) R026, R092. R118/R119 "(T/M)" (uzun rapor yorumu). Eşik 3. R119'daki karşı cümle atlanmış: "Eğer Spread düşük ama Sigma yüksekse; orada gerçek bir "boğa-ayı savaşı" vardır; trendin yönüne güvenebilirsin". R119 tek hisse likiditesi, piyasa şoku değil.
- Düzeltme: "Güçlü (2 T + 2 T/M)" ya da "Orta-Güçlü"; karşı cümleyi çelişki olarak ekle.

**T2-5. Kalan eski etiketler (B10 devamı).**
- T3 "Eşik %30 (A)" → "(T R083)". D4 Düzey "G + A (kural)", Trident formülü artık (T R090): Düzey'i güncelle.
- R10 "yön kuralı R186'da (T: 'benim kullandığım mantık')": kural gövdesi uzun, numaralı (M biçimi); T olan yalnız giriş cümlesi. "(T beyan + M gövde)" yaz; gövde "short fırsatı" içeriyor (BIST'te kısa yok).
- R137 İ8, İ13, Kör nokta 3 ve 7'de (T): gövde numaralı aşamalı başlıklı ama birinci tekilde. "(T/M)" yaz.
- İ4: R224 ilk kâr almayı iz süren moddan önce sayar (giriş → %10 kâr → ikinci kâr → TS noktası → önceki gün dibi %50 → acil stop); R239 ilk kârı aktivasyondan sonraki önceki-gün-dibi kapanışı sayar. Zincir ikisini tek sıraya indiriyor; "%10"un anlamı (fiyat mı pozisyon payı mı) belli değil. Not düş.

**T2-6. B17 kalanları.**
- Eski ilk dalga listesi duruyor; madde 1'de "14.443,45" (tweet metninden; R258 yalnız bağlantı) "birinci elden (G)" ifadesinin yanında, madde 5 "tek sayısal örnek" yeni tabloyla yan yana kafa karıştırır. Eski listeyi sil ya da "(eski, geçersiz)" yaz.
- İ8 R028 notu: R028 iki volatilite kodunun kesişimi, akış kanıtı değil; önemsiz. R170 ikinci okuması önemsiz.

### Doğrulananlar (Tur 2)

1. Yeni alıntıların tamamı atıf yapılan kayıtta birebir (yazım hatalarıyla): R026 ilk cümle, R118, R119, R105 ("dikkt"), R137 ("eğimi ni"), R212 ("musunzu"), R140, R234, R171 («"popüler"»), R157 ("kıs avadede"), R077, R114, R090 (Fib iz süren; "Strtejiyi"), R239, R034, R083, R197, R199, R172, R227, R226, R129, R078. Alıntı hatası yok.
2. R239 aktivasyon okuması doğru.
3. R090 bağlamı doğru işaretlendi (B noktası kırılımı satış yönlü paragrafta).
4. İ6'daki R140 ve R234 eklenmesi hamla tutarlı; "bizim kararımız" kaldırılması doğru.
5. R099 "tüm bakiye": paket 52 görsel tablosunda 92.354,65 TL giriş sermayesi var (G); "sayı görselde G" notu doğru.
6. D19 "yorum", sadakat "yok (grafik yapıştırılmamış)"; "açık kural ölçümü" çerçevesi doğru.
7. D1 kapı (T R019), oranlar (M R080); D12 R034/R228 ve "varsayım" etiketi doğru.
8. Y4 "K (yorum)", "yok (G-dış)": NotebookLM imzasıyla uyumlu. Y5 notu (%26,76 / %27,81; metin anlatmıyor) görsel ve R078 ile uyumlu.
9. İ1 bölünmesi (ortalama kapısı Zayıf): R131 periyotsuz tek (T), karşı R026/R001/R105: tutarlı.
10. C5 R199 alıntısı ve (M) etiketi doğru.

### Özet (Tur 2)
0 YÜKSEK, 3 ORTA (T2-1 ... T2-3), 3 DÜŞÜK grup (T2-4 ... T2-6). Alıntı hatası yok.

## Tur 3 (son kontrol)

Okuma anı: 06.10.2026 ~13:30. Dosya 466 satır. Yöntem: taslaktaki tüm tırnaklı ve «» parçalar R atıfıyla otomatik yeniden tarandı (Tur 2 + Tur 3 değişiklikleri dahil); T2-1 ... T2-6 değişiklikleri elle okundu.

### Tur 2 bulgularının durumu

- T2-1 giderildi: İ3 hükmü ve C2 "ham metni yok (R255 yalnız bağlantı); beyin notu Tansu'nun 2 Eylül gönderisine bağlıyor ama doğrulanamıyor: kanıt sayılmadı". "(denetim B..)" iç referansları metinden kalktı (arama: sıfır sonuç).
- T2-2 giderildi: İ5 başlığı "Orta (R211 T; R212 T dolaylı; ATR bölen G-dış/M)".
- T2-3 giderildi: D1 üçüncü kol "C girişi → D çıkışı" ve (T) R018 alıntısı kayıtta birebir; SMRTG yön notu geri kondu.
- T2-4 giderildi: İ1 "Orta-Güçlü", R119 karşı cümlesi eklendi. Hamdaki yazım "yüksekse, orada" (virgül); benim Tur 2 alıntımdaki noktalı virgül hatalıydı, taslağın hâli doğru.
- T2-5 giderildi: T3 (T R083), D4 düzeyi, R10 "(T beyan + M gövde)", R137 (T/M), İ4'te R224/R239 sıra farkı ve "%10" belirsizliği.
- T2-6 giderildi: eski ilk dalga listesi silindi (arama: "Eski öneri" ve "14.443" ilk dalga bölümünde yok; "14.443" yalnız R4 kataloğunda, "(not)" etiketli).

### Yeni bulgular

Alıntı ve R numarası hatası yok. Otomatik tarama yalnız etiket, görsel metni ve tırnaklı kısaltmalar döndürdü (kayıtta aranamayan görsel/etiket metinleri; yanlış R yok).

**DÜŞÜK**
- T3-1. Sisteme etkisi ve ilk dalga başlıklarında "Güçlü/Orta-Güçlü" ağırlık ifadeleri tutarlı ama İ8 hâlâ "Güçlü" ve R137'yi (T/M) sayıyor; R189, R011, R166 yeterli olduğu için sonuç değişmez. Gerek yok, bilgi notu.
- T3-2. Kalan B17 maddesi (İ8 R028 "akış" kanıtı değil, kavram örneği) açık; etkisi yok.

### Doğrulananlar (Tur 3)

1. T2-1 ... T2-6 değişikliklerinin hepsi dosyada mevcut ve ham/görselle tutarlı.
2. R018 alıntısı ve D1 üç kollu tasarım: ISKPL/SMRTG tabloları C→D işlemidir; sadakat kolu artık Tansu'nun örneğini üretecek biçimde.
3. Tüm sentez ve katalog alıntıları atıf yapılan kayıtta birebir.
4. Açık YÜKSEK bulgu yok. Açık ORTA bulgu yok.

### Hüküm
Taslak, yazara geri dönmeden kabul edilebilir: açık YÜKSEK ya da ORTA bulgu kalmadı, alıntılar birebir, kalan iki madde DÜŞÜK ve sonucu değiştirmiyor.
