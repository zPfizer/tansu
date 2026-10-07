# Strateji modülleri: taslak (keşif)

Durum: keşif sürüyor. Başlangıç: 06.10.2026. Bu dosya çalışma belleğidir; karar TASARIM'a ancak keşif bitince girer.

## Neden

İlk resmi koşu (bilet 15) iki aileyi sınadı: EMA sıkışması ve çift rotasyonu. İkisi de büyük ölçüde bizim yorumumuzdu
(EMA giriş tetiği YORUM, çift Z'si üretilemedi). Levent'in yönü (06.10): Tansu'nun her alım satım stratejisi bir modül
olsun; modüller tek bir backtest motorunda koşsun; motor sinyal üretsin. Modüller Tansu'nun ham notlarından ve
görsellerinden çıkarılır.

## Yapı (öneri, 06.10)

- **Strateji modülü**: "bugün bu hissede kurulum var mı" sorusuna sinyal döndürür. Sinyal: hisse, tarih, yön, giriş
  şekli, stop, hedefler, geçersizlik, kaynak notu.
- **Modül türleri**: giriş, çıkış/risk, piyasa filtresi, tarama (sıralama), yapı taşı (pivot, Fib, kanal, FVG, OB).
- **Tek backtest motoru**: dolum kuralları ortak (T+1 AOF, limit kilidi, maliyet); stop ve hedef modülden gelir.
- **Rapor**: strateji başına işlem listesi, sermaye eğrisi, kazanma oranı, ortalama R, kâr faktörü, en büyük düşüş,
  yıllık tablo, XU100 al-tut karşılaştırması. İstatistik sınavı (K1, Holm) en sonda; kart yalnız sınavı geçene.
- **Sadakat önce**: her modül önce Tansu'nun kendi örneğini yeniden üretmeye çalışır; tutarsa "Tansu", tutmazsa "yorum".

## Kaynak

Kök: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`
(89 tweet, 21 kaynak, 1 not, 127 görsel paketi notu, 201 görsel). Önceki özet: `docs/KURALLAR.md`,
`docs/kurallar/A-..D-*.md` (ikinci okuma; ham kaynak önceliklidir).

## Keşif parçaları

Her parça bir ajanın ham okumasıdır: `docs/strateji-taslak/parca-NN.md`.

| Parça | Kapsam | Durum |
|---|---|---|
| 01 | tweet-*, alfabetik ilk 43 (… tweet-harmonik-xb-…) | bitti: 43 not, 6 görsel, 19 kart (2 H, 11 K, 6 X); ASUZU'nun 4 değerleme görseli açılmadı |
| 02 | tweet-*, alfabetik son 46 (tweet-iskpl-… …) | bitti: 46 not, 4 görsel; dosyada 33 başlık (ajan 25 aday kart bildirdi; 8 K, 17 X) |
| 03 | kaynak-* (21), not-* (1) | bitti: 13 kart, 19 görsel; 4 kitap/repo notu yalnız başı okundu, ekonometri PDF açılmadı |
| 04 | gorsel-paket-01 – 43 (not + görsel) | bitti: 43 paket, 60 görsel (26'nın notu yok), 15 kart (2 H, 5 K, 8 X) |
| 05 | gorsel-paket-44 – 85 (not + görsel) | bitti: 42 paket, 56 görsel; dosyada 30 başlık (ajan: 2 H, 13 K, 8 X); önceki okumayla ciddi çelişki yok |
| 06 | gorsel-paket-86 – 128 (not + görsel) | bitti: 43 paket, 53 görsel, 22 kart (3 H, 15 K, 4 X); hiçbir pakette backtest tablosu yok |

## Tansu'nun bakış açısı (sentez, parçalar gelince)

Levent (06.10): "Tansu gibi düşünmemiz lazım; tweetlerden ve görsellerden onun bakış açısını sentezlemeliyiz."
Modüller tek tek değil, bu bakış açısının parçaları olarak kurulur. Sentez her parçanın "bakış açısı (ipuçları)"
bölümündeki birebir alıntılardan yapılır; her ilke en az bir alıntıya bağlanır, alıntısız ilke yazılmaz.

Toplanacak eksenler:
1. Piyasaya bakış: trend mi, ortalamaya dönüş mü, rejim, şişman kuyruk.
2. Kurulum seçimi: confluence, bağımsız kanıt, arz-talep, formasyon.
3. Giriş ve teyit: kırılım, geri test, hacim, mum.
4. Risk, pozisyon, stop ve hedef mantığı.
5. Doğrulama: backtest, forward test, yanlışlama hakkındaki görüşü.
6. Akış: tarama → filtre → tetik → yönetim; araçları nasıl birleştirdiği.
7. Reddettikleri ve tekrar eden ilkeler.

**Kaynak ağırlığı (06.10, ham okuma sonrası):** sentez artık Levent'in birebir yapıştırdığı 263 ham kayda dayanır
(`ham-yapistirmalar.md`, `ham-yapistirmalar-2.md`). Ham okuması: `strateji-taslak/ham-sentez-a.md` (R001–R130),
`ham-sentez-b.md` (R131–R263). Ajanların 15 alıntısını kaynakta birebir doğruladım. Ham içinde de ses farkı var:

- **(T)** Tansu'nun kısa, birinci tekil, sohbet dili cümlesi: en güçlü kanıt.
- **(G)** Tansu'nun kendi aracının görseli (kod, lejant, tablo). NotebookLM imzalı infografik dış üretimdir: **(G-dış)**.
- **(M)** Uzun, başlıklı, maddeli ders metni. Tansu paylaşmış ama yazarı belirsiz (LLM ya da kitap). Tek başına ilke
  kurmaz; yalnız (T)/(G) ile aynı yöndeyse destek sayılır. Modülde (M)'den gelen kural "yorum" etiketi alır.
- **(A)** Eski notlardaki aktarım. Hamla doğrulanmayan (A) maddeleri bu sürümden çıkarıldı.
- R245–R263 (19 kayıt) yalnız bağlantıdır, metin yok; kanıt sayılmaz.

Ağırlık: **Güçlü** = en az 3 (T)/(G), ciddi (T) çelişkisi yok · **Orta** = (T) desteği var ama (T) çelişkisi de var ·
**Zayıf** = destek az ya da Tansu'nun kendi araçları tersini yapıyor.

### Sentez: Tansu bir işlemi nasıl kurar (06.10, hama göre yeniden tartıldı)

Tansu'nun işlemi tek bir "AL sinyali" değildir. Aynı sıra ile kurulan bir **kurulum hikâyesidir**:
rejim uygun mu → yer doğru mu → yapı tamamlandı mı → fiyat tepki verdi mi → risk ve hedef baştan yazılı mı.

**İ1. Önce rejim, sonra işlem. — Şok freni Orta-Güçlü, ortalama kapısı Zayıf**
- (T) R026: "Kısa vadeli dalgalanma aniden fırlarsa algoritmayı Piyasa Şoku moduna geçirir. Yeni al sinyallerini tamamen
  durdur"; şok ölçüsü: "son X günlük dalgalanmasını son 1 aylık dalgalanmasıyla kıyaslayin" (X verilmemiş).
- (T) R092: "Fiyat ve volatilite aynı anda artması pek istenilen bir durum değildir sonu genelde kötü biter";
  "sistemim pozisyonu kapatıp defansif pozisyoon aldı".
- (T/M) R118, R119 (rapor yorumu): "Sigma ani bir sıçrama görmediğimiz sürece"; "Spread yüksek, Sigma yüksekse; o
  tahtadan uzak durun ya da "stop-loss" seviyelerini çok geniş tut".
- (T) R131: "hareketli ortalamanın altındaysa, bu durum satış yönlü; … üzerindeyse, alış yönlü … Trend is your friend."
  Periyot yok.
- (G-dış) R212 görseli: 250 günlük ortalamanın altında kapanış → **çık** (gün sonu stop). (T) R212 metni ise 250SMA'yı
  "işleme giriş bileşenlerinizden birisi" sayar: "(bu 200SMA 200EMA 250EMA' da olabilir, stratejinize kalmış.)".
- Çelişki, ortalama kapısına karşı (T): R026'nın ilk cümlesi "Sabit hareketli ortalamalar ani piyasa paniklerinde yavaş
  kalır ve size hatalı alım  satım yaptırabilir"; R001 "Ortalamaları temel alan indikatörler hava civadır"; R105
  "ortalama kullanıyor iseniz eğimlere dikkt edeceksiniz".
- Çelişki, rejim şartı taşımayan stratejiler: ortalamaya dönüş ve çift. (M) R101 "piyasa … ister yüzde 10 düşsün, ister
  yüzde 10 çıksın, bizi hiç ilgilendirmiyor"; R053 −2/−3 SE "tepki alımı fırsatı". (M) R220 şoku fırsat sayıyor.
- Hüküm, ikiye bölündü:
  - **Şok freni — Orta-Güçlü (2 T + 2 T/M):** (T) R026, R092; (T/M) R118/R119 aynı yönde. Şokta yeni giriş yok;
    eldeki risk yönetilir. Pencere X verilmemiş: yorum. Karşı: R119 tek hisse likiditesi için "Eğer Spread düşük ama
    Sigma yüksekse, orada gerçek bir "boğa-ayı savaşı" vardır; trendin yönüne güvenebilirsin" (yüksek sigma tek başına
    çıkış sebebi değil).
  - **Ortalama kapısı — Zayıf, yorum:** tek (T) dayanak R131 (periyotsuz); Tansu'nun kendi sözleri ortalamaya karşı.
    "Uzun ortalama altında alım yok" bizim yorumumuzdur; ölçümde kapılı/kapısız iki kol koşulur.
  - Kapılar trend ve formasyon modüllerine uygulanır; ortalamaya dönüş ve çift modülleri muaftır. "Tam/Defansif"
    çarpanın oranları hamda yok: yorum. R089 (kırmızı bölge, "patır patır geri gelir") tanımsız bir seriye dayanır;
    rejim dayanağı sayılmadı.

**İ2. Yer önce, gösterge sonra. — Güçlü (formasyonlar için)**
- (T) R080: "D noktasına bakın, talep toplama bölgesine bakın, hissenin tepkilerine bakın. Doğru kod böyle yazılır."
- (T) R081: "tam talep toplama bölgesinden haftalıkta tepkisini almış kütür kütür gitmiş. İşte bu yapıların peşindeyiz."
- (T) R085: "gözü kapalı ABCD'ye nasıl güveneceksin kanalı okumadan iş yapılır mı?"; R075, R009, R127 aynı yönde.
- (T) R037: "Distal line ve proximal line'ı kavrarsak bu işişn %50'si biter"; R055: confluence alanları "Her seferinde
  zenginlik yaratmışlar"; R206: "Fibo 0.618 bir 'duvar' değil, sadece bir 'bölge'dir."
- Çelişki: Tansu bölgesiz gösterge stratejileri de paylaşıyor: R131 tek ortalama, R148 half-trend + momentum,
  R233 RSI 30, R170 Williams %R. (T) R145: "İndikatör cart curt hikaye."
- Hüküm: formasyon modüllerinde bölge zorunlu. Gösterge stratejileri ayrı bir aile; onlarda bölge yok, ama ölçümde
  "bölgeli" varyantları da koşulur.

**İ3. Yapı tamamlanınca bile tepki beklenir. — Orta**
- (T) R014: "10 gün içinde D noktasından bir tepki yapmıyor ise belirsiz bir yapı olarak bakılabilir."
- (T) R087: "Abcd analizine güvenip çaat diye alırsan küüt diye böyle olursun. Her zaman çalışmaz."
- (T) R194: "İşte bu yüzden retest beklemek önemlidir. Bakın macd yanıltmış ama hacim asla desteklememiş."
- (T) R090 (yalnız **satış yönlü** formasyon paragrafında): "D oluşumunu teyit etmek için ise B noktası kırılımı gerekir";
  R098: momentum dönüş teyidi "karlarda çarpan etkisine".
- (G) Durum etiketleri [AKTİF] / TEPKI_VERDI / BOZULDU / [TAMAMLANDI] ve "20 bar içinde TEPKİ GELMEDİ" yalnız görsellerde var.
- Çelişki: (T) R090 alış yönlü paragrafta teyit yok: "teorik D noktasından yani dipten pozisyon alınır". (M) R197 temas
  girişi ("temas ettiğinde ALIM (LONG) yönlü işlem aranır"); (M) R199 limit alış. (M?) R172 "ASLA TEPE VEYA DİP NOKTALARI
  YAKALAMAYA ÇALIŞMAK DEĞİLDİR" D'de dipten alımla çelişir; (T) R227 ise "Dip yakalanmıştır" diyor.
- Hüküm: tek doğru giriş yok. Her formasyon modülü iki girişle koşulur: **D'de limit** ve **tepki teyidi**. Retest'in katkısı
  hamda ölçülmemiş (R194 tek olumsuz örnek); iki kol bunu ölçer. "Retest beklemek yarar sağlıyor mu?" sorusunun ham
  metni yok (R255 yalnız bağlantı); beyin notu onu Tansu'nun 2 Eylül gönderisine bağlıyor ama doğrulanamıyor: kanıt
  sayılmadı. Tepki penceresi parametredir:
  10 gün (R014, D sonrası) ve 20 bar (görsel); görseldeki "son 10 gün" ayrı bir ifade olabilir.

**İ4. Geçersizlik ve hedef baştan yazılıdır. — Güçlü; "yapı stopu esas" hükmü kaldırıldı**
- Yapı geçersizliği: (T) R019 "C'den sonra fiyat A'yı geçerse patern bozuldu sayılır"; R043 "(Close < zone_low)".
- Çıkış zinciri, parça parça kaynağıyla. Not: R224 ilk kâr almayı ("%10 (sizin belirleyeceğiniz)") iz süren moddan önce
  sayar; R239 ilk kârı aktivasyondan sonraki önceki gün dibi kapanışı sayar. "%10"un fiyat mı pay mı olduğu belli değil.
  Aşağıdaki sıra iki kaynağı tek sıraya indirir: yorumdur.
  - [T R224, R239] Giriş + 1.5 ATR iz süren modun **aktivasyon** noktasıdır (mesafe değil): "İz süren moda girdiğinizde
    yani Giriş + 1.5ATR noktasına geldiğinizde artık hedef izleyeceksiniz". Bundan sonra önceki günün dibinin altında
    kapanışta %50 satılır (R239 "%50'sin satın"; R224 "önceki günün en düşüğünün altında kapanış ve %50 satış").
  - [T R224] Acil stop: "emergency stop 2atr ile kalan tüm maldan çıkış"; ilk kâr "%10 (sizin belirleyeceğiniz)".
  - [M R233] RSI stratejisinde ilk %50 RSI 70 reddinde, ikinci %50 önceki gün dibi altı kapanışta.
  - [M R203] TP1'de pozisyonun "bir kısmı (örn. yarısı)" kapatılır, stop girişe çekilir; harmonik TP merdiveni.
- Hedef: (T) R090 "D = (B * C) / A"; formasyon için (T) R090 "D dibinden sonra FIBO seviylerine göre iz süren takibe göre
  TP kovalanır"; Fib merdiveni (M) R203 TP1 0.382 / TP2 0.618 / TP3 C; giriş eşiği (M) R222 "Ödül / Risk < 1.5 ise …
  işleme girilmez".
- Çelişki: hamda en az dört stop ailesi var: yapı, ATR (R184, R212), yüzde ve R/R (T R234 "%2 Stop, %3 Kar Al";
  M R230), SD bandı (M R187). Zaman stopu da var (R014).
- Hüküm: modül **geçersizliği** (analiz iptali) verir. Formasyon modülleri için Tansu'nun çıkışı geçersizlik + Fib iz
  süren takip (R090). ATR zinciri (1.5 ATR aktivasyon, önceki gün dibi altı kapanışta %50, 2 ATR acil) genel bir (T)
  kuralıdır; formasyonlarda ölçümde ayrı kol olarak denenir. "TP1'de %50 + stop girişe" (M R203) ayrı koldur. Stop
  aileleri ölçümde karşılaştırılır.

**İ5. Önce kayıp bütçesi, sonra adet. — Orta (R211 T; R212 T dolaylı; ATR bölen G-dış/M); %1 ve 2 ATR yorum**
- (T) R212: "kaç lot almanız gerektiğini biliyor musunzu?"; %1 bir **örnektir**: "Diyelim ki sermayenizin ancak %1'ini
  kaybetmek riskini göze alabilirsiniz". (G-dış, NotebookLM; Tansu paylaşmış) "Belirlediğiniz risk tutarını, hissenin 2 ATR
  (Ortalama Gerçek Aralık) değerine bölün."
- (T) R211: "Volatilitesi yüksek olan hisselerde position sizing matematiksel olarak küçülür ve bu çok doğrudur. … Asıl
  amacımız sermayemizi korumak."
- Ayrı başlık, likidite (kayıp bütçesi değil): (T) R201 "sığ hisselerle vakit kaybetmeyin … likit hisselere odaklanın".
- Çelişki: (M) R099 çift sistemi "92.354 TL'lik tüm bakiyesiyle yeni bir işleme giriyor" (sayı görselde G); (M) R220
  "Cesaret, uçlarda gezer".
- Hüküm: boyutun volatiliteyle ters olması Tansu'nun ilkesi (R211, R212). %1 risk ve 2 ATR bölen yorum etiketiyle
  kullanılır (örnek + G-dış); ölçümde parametredir. Çift modülünde tam bakiye (Tansu'nun kendi örneği); motor iki
  boyutlamayı ayrı tutar. Likidite eşiği ((T/M) R232: 20 günlük ortalama hacim < 10 mn TL eleme) parametredir, yorumdur.

**İ6. Kural koda dökülür, sistem ellenmez, sonuç ölçülür. — Orta (söylüyor, az yapıyor)**
- (T) R100: "Her arbitraj fırsatı çalışmaz Mutlaka backtest etmek lazım"; R102: "Sadece sistem çalışıyor hiç ellemiyorsun:)";
  R210: "herşey kurallara dayalı. Duyguya yer yok. Sistem ne derse o."; R111: "backtest ve forward test süreçlerini".
- (T) R234 zayıf sonucunu açık veriyor ("Doğruluk (Accuracy) : %55.00"); R138 "walk forward le optimzie".
- Yanlışlama: (M) R171 «Eğer testler stratejinin başarısız olduğunu söylüyorsa, o "popüler" kurala yatırım yapmaktan
  vazgeçmenizi sağlar»; (T) R157 "iki satır kod yazayım ya da yazdırayım sevdası kıs avadede karlı gibi görünsede orta ve
  uzun vadede yıkıma sebep olabilir".
- Çelişki: yayımlanan stratejilerin çoğunda ölçüm yok: (T) R170 "Bi bakın bakalım backtesti nasıl"; R156 "can
  sıkıntısından yazdım … ama çalışıyor"; tek örnek anlatıları (R116 "5 günde %29", R152 FROTO). Optimizasyonu hem
  kullanıyor (R174) hem uyarıyor (M R185). Kazanma oranını öne çıkarıyor: (T) R021 "%70 çok yüksek bir başarı oranıdır".
- Kazanma oranı: (T) R021 %70'i öne çıkarıyor; ama (M, Tansu "Dursun bir kenarda lazim olur" diye paylaşmış) R140
  "Yüzdelik doğruluk … acemi yatırımcıların bir takıntısıdır" ve (T) R234 "%55 başarı oranıyla … Risk/Ödül oranını en az
  1:1.5" aynı yönde: kazanma oranı R/R ile birlikte okunur.
- Hüküm: ölçüm Tansu'nun söylediği ama yapmadığı iştir. Motorumuzun asıl katkısı budur. Rapor kazanma oranını tek ölçüt
  yapmaz; R140 ve R234 bu yönde.

**İ7. Medyan ve uç değer temizliği. — Zayıf (genel ilke değil)**
- (T) R001: "Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın"; R244 "Medyanı şöyle bir kanal
  gibi kullanın"; R033 "anomalileri çıkarmaz iseniz sizi yanıltır".
- Çelişki: Tansu'nun kendi araçları ortalama kullanıyor: R068 "bu ortalamaların da ortalamasını alırım", R131 hareketli
  ortalama, R101 Z-skoru, R053 ±2 SE bandı. %50 anomali eşiği ve IQR k=1,5 yalnız görsellerde var.
- Hüküm: modül hesapları Tansu'nun yazdığı gibi kalır (ortalama varsa ortalama). Medyan ve anomali temizliği sıralama ve
  ölçüm katmanında kullanılır (sektör rotasyonu, değerleme çarpanları, rapor istatistiği).

**İ8. Akış: tarama → harita → kesişim → tepki → yönetim; her formasyona ayrı tarayıcı. — Güçlü**
- (T) R189: "tüm hisseler önce momentum sistemimden geçiyor sonra ayrıntılı yazıyorum."
- (T/M) R137: beş aşama: "Momentum ve Sinyal Yakalama", "Pozitif Eğim ve Görsel Doğrulama", "Teknik Onay",
  "Markowitz Portföy Optimizasyonu", "Maksimum Sharpe Seçimi"; "kimler koşmaya hazır, hangileri doğru yöne bakıyor, diye eliyoruz".
- (T) R011: "Gartley taramasını ayrı yapın butterfly taramasını ayrı yapın. Konsolide etmek bünyeye büyük zulüm."
- (T) R028: "Kesişim kümesi yatırım noktasıdır."; R166: "değerleme %50 potansiyel diyorsa, Teknik "Şimdi al" dediğinde
  sistem alarm verecek."
- Çelişki: R065/R067 "tek tuş" ve R143 tek mum motoru. Çözüm: kodda ayrı dedektör, kullanıcıya tek ekran.

**Yeni ilkeler (ham okumadan, en az iki (T) kaydında)**

**İ9. Sıkışma kırılımın habercisidir. — Güçlü**
- (T) R082: "konoslidasyon ne kadar uzarsa kırılım o denli şiddetli oluyor"; R132: "ortalamaların sıkışma alanları
  genelde patlamaya işaret eder"; R198: "Ben 5-8-13 kullandım."
- (T) R127: "Rasyoyu siz belirleyeceksiniz … sıkışma rasyosu sizin tecrübenize kalmış." Eşik verilmemiş: yorum gerekir.
- (T) R077: "Rehavet ortamı vardır ve fiyat bir yöne kırılacaktır." (yönsüz)
- Etki: EMA sıkışma ailesi Tansu'nun gerçekten savunduğu bir fikir; ilk koşudaki giriş tetiği ise hâlâ bizim yorumumuz.

**İ10. Hiçbir kurulum %100 çalışmaz. — Güçlü (en çok tekrar eden fikir)**
- (T) R014 "Her gartley çalışmaz"; R024 "Her harmonik %100 çalışır diye de bir kaide olamaz"; R087 "Her zaman çalışmaz.";
  R100 "Her arbitraj fırsatı çalışmaz"; (M) R101 "hiçbir strateji kusursuz değildir".
- Etki: her modül raporu başarısız kurulumları da listeler. BOZULDU durumu sonuçtur, hata değildir.

**İ11. Hacim teyidi ve "ayak izi". — Orta**
- (T) R024 "Hacim ayak izine bakıyoruz"; R036 "Fiyat ve hacim, resmin yalnızca üçte ikisidir, fiilen işlem gören hisse
  sayısı ise resmi tamamlar"; R238 "Geniş gövdeli mum düşük hacim, anomali"; R194 "hacim asla desteklememiş".
- Sınır: (T/M) R227 açık pozisyon ve oyuncu sayısı (COT, "trader count") verisinin "yfinance ve standart borsa
  verilerinde" olmadığını söylüyor; "akıllı para" ölçüsü vekil (proxy) değişkendir. Emir defteri ayrı konu (R225).

**İ12. Teknik "nereden", temel "ne". — Orta; ayrı katman**
- (T) R166 "teknik analiz size "Nereden" alınacağını söyler, temel analiz ise "Ne" alınacağını"; R069 "Buna bir de tekniği
  ekleyin olsun bitsin"; R158 değerleme ağırlıkları (DCF üçlüsü %40, çarpanlar %60).
- Çelişki: (T) R240 temel analiz için "bistte artık bir önemi yok".
- Etki: değerleme, momentum sıralaması, TOPSIS ve Markowitz (R137, R145, R181) strateji modülü değil, **seçim katmanıdır**.
  İlk dalganın dışında kalır.

**İ13. Eğim kesişimden önce döner. — Orta**
- (T) R105: "Bana sistem ile ilgili gelen sorulara verdiğim cevaplar hep aynı  Arkadaşlar ortalama kullanıyor iseniz
  eğimlere dikkt edeceksiniz. Momentum trader iseniz sinyal eğiminize dikkat edeceksiniz"; gövdesi (M): "Momentum (Hız),
  değerden (Fiyat veya Gösterge) önce döner."
- (T/M) R137 ikinci aşama: "Pozitif Eğim ve Görsel Doğrulama"; "hem fiyatın hem de oluşan sinyalin eğimi ni kontrol ediyorum".
- Etki: ortalama kullanan modüllerde (D11, rejim kapısı) kesişim yerine eğim kolu da ölçülür.

İkincil, tek başına ilke kurmayan fikirler: volatilite getiri kaynağıdır (R030, R102), kitaptaki hazır modeli olduğu gibi
uygulamama (T R111) ve önce kağıt-kalemle çözme (T R109), kara kutu istememe (T R039, R058), göreli konum (R227 252 gün),
asimetri (M R229). Özet (T) R114: "doğru formasyonu doğru seviyede, sıfır duyguyla ve tam zamanında yakalamak. Sonrası
zaten trendin peşine takılmaktan ibaret."

**Kör noktalar (Tansu'nun kendi yönteminde, hamla sınandı)**
1. Seçilmiş olumlu örnek: destekleniyor. R116, R152, R227 ("Dip yakalanmıştır"), R021 (13 günde 9 isabet). Kısmi karşı
   kanıt: kendi başarısızlıklarını da gösteriyor (R087, R194, R234, R099 ilk işlemde zarar).
2. "Bağımsız kanıt" aynı fiyat serisinden türüyor: destekleniyor (R040, R208 örnek listesi). İstisna: hacim, fiili dolaşım
   (R036, R083) ve bilanço verisi gerçekten farklı kaynak.
3. Parametre saklama: kısmen. Kurulum geometrisi açık (R019, R080, R222 "%3-%5 tolerans"). Sinyal sistemi kapalı:
   R125 "parametrelerin detaylarını verip stratejimi anlatamam"; R137 "Bu sistem satılık değil"; R090 "Strtejiyi
   açıklamak isterdim ama artık strateji vs yazmıyorum".
4. Ortalamaya dönüşü "zorunlu" anlatıyor: destekleniyor (M R226 "geri dönmek zorunda"; R053 normal dağılım). Ama (T) R100
   "Görünmez bağ kopmuş olabilir" ve (M) R101 "Peki Ya İp Koparsa?" riski sözle kabul ediyor.
5. Yazar belirsiz: uzun metinlerin çoğu (M). Bu metinlerden çıkan kural Tansu'nun sözü olmayabilir.
6. Açığa satış: sık anlatıyor (R099 "AGROT SAT, GARAN AL", R101, R131, R170). BIST'te kısa bacak yok.
7. Kendi tutarsızlıkları: ML'yi sevmiyor (R021, R234) ama momentum sistemi yapay sinir ağı (R137); temel analize "önemi
   yok" diyor (R240) ama yoğun değerleme yazıyor (R158).

### Sisteme etkisi (öneri)

1. **Modül = kurulum yaşam döngüsü**, sinyal değil. Durumlar Tansu'nun kendi etiketleri: ADAY (yapı/bölge bulundu) →
   AKTİF (fiyat bölgede) → TEPKİ_VERDİ (teyit; giriş burada) → TAMAMLANDI (hedef) / BOZULDU (geçersizlik).
2. **Katmanlar**: rejim (piyasa + hisse) → bölge/yapı haritası (ortak yapı taşları) → kurulum dedektörü (formasyon)
   → teyit (tepki, retest, hacim) → yönetim. Yönetim (İ4): modülün geçersizliği her zaman; çıkış kolları kaynağıyla
   ayrı: [T] 1.5 ATR aktivasyon + önceki gün dibi altı kapanışta %50 + 2 ATR acil; [M] TP1'de %50 + stop girişe;
   formasyonlarda [T R090] Fib iz süren takip. Boyut volatiliteyle ters (T R211); %1 / 2 ATR yorum parametresi (İ5).
3. **Rejim kapısı** (İ1): şok freni (T, Güçlü): şokta yeni giriş yok. Ortalama kapısı (yorum): uzun ortalama altında alım
   yok; kapılı/kapısız iki kol. Yalnız trend ve formasyon modüllerine uygulanır; ortalamaya dönüş ve çift modülleri
   muaftır. "Tam/Defansif" çarpanın oranı hamda yok: yorum.
4. **Ölçüm katmanı hamda ölçülmemiş soruları cevaplar** (İ6): aynı modül D'de limit / tepki teyidi, bölgeli / bölgesiz,
   yapı stopu / ATR stopu / R:R stopu ile koşulur; katkısı olmayan katman atılır. Rapor başarısız kurulumları da
   listeler (İ10). Rapor biçimi: hedefe ulaşan / stop / açık; sermaye eğrisi, en büyük düşüş, al-tut, maliyet.
5. **BIST'te açığa satış yok**: kısa yönlü kurulumlar (SMRTG AB=CD, R131 "satış yönlü") "D'de alım" varyantına çevrilir
   ya da yalnız çıkış sinyali olarak kullanılır.
6. **Sadakat etiketi kaynağa göre**: (T) ve (G) kaynaklı kural "Tansu"; (M) kaynaklı ya da eşiği verilmemiş kural
   (EMA sıkışma oranı R127, şok penceresi X R026) "yorum" etiketi alır.
7. **Seçim katmanı ayrıdır** (İ12): momentum sıralaması, değerleme, TOPSIS, Markowitz strateji modülü değildir; ilk
   dalgaya girmez. Ama Tansu'nun akışında kurulumlar momentum ön elemesinden geçen hisselerde aranır (T R189); ilk dalga
   ön elemesiz koşar ve sonuç bu notla okunur. Gösterge stratejileri (RSI 30 R233, Williams %R R170, A/D-EMA R139)
   parametreleri açık ama kural gövdeleri (M) ya da operatörü eksik (R139): sadakat sınıfı "yorum"; açık kural ölçümüne
   adaydırlar, sadakat testine değil.

## Modül kataloğu (birleştirme, parçalar gelince)

Birleştirme: 06.10.2026, yalnız parça dosyalarındaki kartlardan. 56 modül satırı (katman başına: rejim 13, tarama 13,
kurulum 18, teyit 6, yönetim 6). Yeni sayı eklenmedi; sayılar parçalardan aynen alındı. Ham güncellemesiyle (06.10)
D19 (RSI 30, ham R233) eklendi: 57 satır, kurulum 19.

Okuma anahtarı:
- Kaynak: pNN = parça no. K/M/K-05-xx/M06-xx = o parçanın kart no'su; pkNN = görsel paket no'su.
- Düzey: **G** Tansu'nun görseli (birinci el) · **X** X bağlantılı birebir metin · **A** aktarım (ikinci el). Parantezde ek düzey yazıldı.
- H/K/X: H kural birinci elden belli · K çekirdek belli, yorum gerekir · X formül yok. Sınıflar çelişirse ikisi de yazıldı,
  ilk yazılan sayıma girdi.
- Sadakat: "[piksel]" = parça yazarının grafikten ölçtüğü yaklaşık değer. "(not)" = notun sayısı, görselde doğrulanmadı.
- Veri sütunu: "OHLCV" = günlük OHLCV yeter.
- **Ham güncellemesi (06.10):** "Düzey" sütunu parça okumalarının eski G/X/A işaretidir. Hamda birebir karşılığı bulunan
  satırlara "Ham:" notu eklendi ve sentezdeki işaretler kullanıldı: (T) Tansu'nun kendi cümlesi, (G-dış) NotebookLM
  infografiği, (M) yazarı belirsiz ders metni. Ham ile eski düzey çelişirse ham esastır.

### 1. Rejim / piyasa filtresi

| # | Ad | Kaynak | Düzey | H/K/X | Sadakat hedefi | Veri | En önemli yorum noktası |
|---|---|---|---|---|---|---|---|
| R1 | Pozisyon büyüklüğü çarpanı Tam/Defansif; sağlıklı–sağlıksız yükseliş | p05 K-05-05 (pk48, 49), K-05-03 (pk46) | G | X | yok (tek grafik; "Mom Eşiği 0.15", "Kırılma Eşiği 0.0" lejanttan) | OHLCV olası; formül bilinmiyor | Yön G: fiyat ve volatilite birlikte artarsa Defansif. Mavi/turuncu serinin formülü ve Tam/Defansif değerleri yok. Ham: (T) R092 "Fiyat ve volatilite aynı anda artması pek istenilen bir durum değildir"; "sistemim pozisyonu kapatıp defansif pozisyoon aldı". |
| R2 | Volatilite rejimi okları (v_t / Theta); konsolidasyon uzunluğu–kırılım şiddeti | p04 Kart K (pk36, 41) | G | X | yok | OHLC; model bilinmiyor | "Rehavet" = düşük oynaklık, yönsüz kırılım habercisi (A). Eşik ve formül yok. |
| R3 | Volatilite şok freni (yeni alım yok); vol ile ters orantılı boyut | p02 M13, M14; p01 K15 ("sigma sıçramasını izle") | A | K (düşük) [p02 M13]; X [p02 M14; önceki okuma şok freni için X] | yok ("bir ay ≈ 21 işlem günü" bizim yorum) | OHLCV | Eylem kuralı net (şokta yeni alım ve yeni hisse yok), kısa/uzun pencere ve eşik yok; bu yüzden K düşük. Ham: düzey (T) R026 "Yeni al sinyallerini tamamen durdur"; ölçü "son X günlük dalgalanmasını son 1 aylık dalgalanmasıyla" (X verilmemiş: yorum). |
| R4 | Trend/rejim filtresi: kapanış WMA21 üstü/altı (XU100); MA yön filtresi; EMA50/100/200 + KDE | p03 M11 (xu100-1-eylul, bekle-teyit); p01 K10; p05 K-05-18 (pk68); p06 pk107 (A: "düşüş yapısında uygulanmaz") | G (+A) | K (WMA21); X (CHoCH, SETUP puanı) | XU100 1 Eylül günlük 14229,01; WMA21 geri alma eşiği 14.443,45 ve son kısa tepe 14.722,02 (not); SETUP 45/100 (günlük), 35/100 (4s); 2 Eylül SETUP 7/100 ve 13/100. pk68: kapanış 14587,90, EMA50 13310,99, EMA100 12840,90, EMA200 12256,37 | XU100 OHLCV; 4s CHoCH gün içi ister | "WMA Close 21" G. MA türü ve periyodu p01 K10'da yok. SETUP formülü ve "kalıcılık" yok. |
| R5 | "Piyasanın Nabzı" 7 göstergeli skor | p06 M06-04 (pk98) | G | K | Anlık: VIX 13,47 (güvenli üst limit 16,99); ADX 22,9; RSI 68,1; SMA18 11335,87 / SMA35 11026,53; fiyat 11336,18; korelasyon −0,60; skor 4/5, "Dikkatli iyimserlik" | BIST100 OHLCV + VIX (dış) | 7 kutudan 5 üzerinden skor toplama kuralı yok. Hacim kutusu 0 (veri hatası olabilir). |
| R6 | BIST100 + VIX "Kusursuz Long" 5 adım | p06 M06-13 (pk113, 114) | G | K (fiyat > SMA20 > SMA50 kısmı H) | İşlem sonucu yok. pk114: 2025-01-01..2025-12-14, korelasyon 30 gün, VIX RSI(200) < SMA(10) | XU100 OHLCV + ^VIX (dış) | Çıkış "SMA20 altı VEYA HA kırmızı VEYA VIX RSI ortalamayı yukarı keser": veya/ve belirsiz. "4 göstergeden 2'si" hangi 4 belli değil. |
| R7 | Endeks "bugün ne anlatıyor" skoru | p01 K15 | A | X | Tek anlık: skor 5/5, ADX 28,9, RSI 77,6, VIX 20,6, 20g NH-NL 83, XU100 CS ort. %1,06, "Full Long" | NH-NL için bileşen OHLC (sağkalım yanlılığı) | 5 bileşenin kimliği ve eşikler yok. |
| R8 | Corwin–Schultz spread + sigma (likidite/risk, yön değil) | p03 M12; p05 K-05-12 (pk62); p01 K15 | G | K | XU100 21g: ort. %1,088, medyan %0,454, P75 %1,899, P90 %3,028. FROTO: ort. %1,7990 (notta 1,7909; görsel esas), medyan %0,7841, max %9,8494 (2025-04-14), ort. sigma %2,1133 | OHLCV (H/L) | Sigma formülü ve "yüksek/düşük" eşiği yok. Yorum kuralı (A): spread+sigma yüksek → uzak dur / geniş stop. |
| R9 | Gerçekleşen yıllık volatilite sınıfı | p06 M06-21 (pk124); p02 M14 | G (kod) | H | DOAS günlük %2,25, yıllık %35,66; eşik %40 (std × √252, 1 yıl) | OHLCV | Yalnız sınıflama; boyuta bağlanması yok. |
| R10 | Hacim profili / auction: denge–dengesizlik, VWAP+POC yön izni, VAL/VAH | p02 M3, M4; p01 K6 (ACSEL), K7; p05 K-05-16 (pk66) | A (+G grafik) | X (p02 M4, p01 K6, p05 K-05-16); K (p02 M3) | Value Area %68 (A, tek sayı). ALKIM (not): fiyat 31,00, VWAP 28,00, POC 29,71, VAH 30,24 | OHLCV yetmez: gün içi/tick; günlük proxy yaklaşık ve etiketli | M3'ün yön kuralı (VWAP ve POC üstü al, arası bekle) belli, bu yüzden K; diğerlerinde tetik ve eşik yok, X. Pencere, VA %, VWAP reset yok. Ham: yön kuralı R186'da (T beyan "benim kullandığım mantık" + M gövde; gövdedeki "short" BIST'te yok). |
| R11 | Aylık mevsimsellik (pozitif kapanış oranı ≥ %70) | p01 K14 | A | K | yok (Ocak 10 yılın 8'i sözlü; %80/%30 örnek, kural değil) | OHLCV → aylık; 10–20 yıl | Oranı maruziyete çevirme kuralı yok. |
| R12 | Weinstein 4 evre | p05 K-05-09 (pk56) | G (etiket) + A | X | yok | haftalık OHLCV | Evre sınırı ve ortalama periyodu yok. |
| R13 | Trend rejimi: rolling korelasyon (HMM gereksiz) | p02 M17 | A (kaynak kimliği doğrulanmamış) | X | yok | OHLCV | Seri çifti, pencere, eşik yok. |

### 2. Tarama / evren

| # | Ad | Kaynak | Düzey | H/K/X | Sadakat hedefi | Veri | En önemli yorum noktası |
|---|---|---|---|---|---|---|---|
| T1 | Sektör liderleri 30/60/90 gün + anomali dışlama (\|30g getiri\| > %50) | p04 Kart C (pk06, 07); p02 M23 | G | K (anomali kuralı H) | 2026-08-14. 30g: Petrol 0,2389, Mimarlık-Müh. 0,1431, Mesleki-Bilimsel 0,1030. 60g: Yatırım Şirk. 0,1289, Petrol 0,1283, Demir Çelik 0,1030. 90g: Bayındırlık 0,2875, Demir Çelik 0,2859, Bilişim 0,2344. Dayanıklı Tüketim (18 hisse): basit ort. −%1,32; eski fiyat-ortalaması +%90,99; temiz (17/18) −%11,11; fark 9,79 puan; OZATD +%165,06 | Sektör üyelik tablosu ayrı kaynak + OHLCV | Pencere takvim mi işlem günü mü yok. Sektör sinyalinin hisse girişine bağı yok. HKTM görselde +12,62 (pk07 notu −12,62 yazmış, hata). |
| T2 | Sektör rotasyonu: huni (lider sektör → DuPont → ucuz hisse → mevsimsellik); DEA/VZA; Convex Hull | p02 M23 (X metni); p01 K19 | X (M23, plan) + A | X | yok | Sektör getirisi + bilanço | Birebir Tansu cümlesi var ama ölçüt yok ("yapılacak, bitince paylaşılacak"). |
| T3 | Evren filtreleri: fiili dolaşım oranı < %30; likit hisse/ETF kapısı | p01 K16; p04 Kart D (pk08); p02 M15 | G (tablo) + A | H (p01, evren filtresi olarak); X (p04: tarihsel seri yok; canlı K); likidite kapısı X | KENT 0,54 (1.781.294,53 pay, 2026-05-17), KLNMA 0,92, CMENT 2,71, SNPAM 4,13, GARAN 13,98 (2026-06-02). Eşik %30 (T R083) | KAP fiili dolaşım (OHLCV yetmez); ADV OHLCV'den | Ham (T) R083: "Dolaşımdaki pay adedinin <%30 olduğu senetler" (oran; KAP verisi). Anlık değer geriye taşınamaz. Notun OZATD %13,22 satırı görselde yok. |
| T4 | 80–100 hafta yatay kalan hisse, alt bölgede bekle | p03 M9 | X (tweet özeti) | X | yok | haftalık/günlük OHLCV | Eğim, bant genişliği, "alt bölge" eşiği, çıkış: hiçbiri yok. |
| T5 | Clenow tipi üstel regresyon momentum (log-fiyat eğimi × R²) | p01 K11 | A (kod notta) | K | yok | OHLCV | Skor = (1+eğim)^252 × R² (kod, A). Lookback ve seçim kuralı yok. Yön kapısı gerekir (bizim yorum). |
| T6 | 12 aylık momentum decile (10 grup, üst grup 1 ay) | p05 K-05-13 (pk63) | A | K | Görsel yalnız DEY tablosu: NIBAS 3,62→11,60 (%220,44), DOGUB %202,31, TMPOL %142,20, POLTK %2,53; bitiş kapanışı NaN, gerçekleşmiş getiri değil | OHLCV, 500+ hisse, ölü hisse dahil | Atlama ayı, ağırlık, maliyet yok. Tansu'nun kendi sayısal sonucu yok. |
| T7 | Momentum × faaliyet nakit akışı 5×5 (Mom5 ∩ CFO5, çeyreklik) | p02 M10 | A | K | yok | fiyat + bilanço (CFO); OHLCV yetmez | Momentum formülü bu iletide yok. CFO verisi bedava zor. |
| T8 | 63 günlük rolling skewness (liste etiketi) | p03 M13 | G | H | Sınıflar: < −0,50; −0,50..0; 0..+0,50; > +0,50; > +1 ise büyük günleri kontrol. CWENE son ≈ +0,2/+0,3 | OHLCV (kapanış) | AL/SAT değil, tarama sütunu. Skewness tahmincisi tanımı yok. |
| T9 | Diğer momentum: eğim dönüşü (erken uyarı), rolling alpha, ANN → çift pozitif eğim → ADX/CMF/mum | p02 M9, M19, M20 | A | X | yok ("%5–10 prim" iddia) | OHLCV | Tek net kural: fiyat eğimi > 0 VE sinyal eğimi > 0 (M20). ANN ve eşikler gizli. |
| T10 | Fiyat konumu × hacim konumu haritası (252 gün) | p06 M06-20 (pk128) | G | K | konum = 100×(değer−min)/(max−min), pencere 252 gün (not). Bölgeler: dip x ≤ 20 ve y ≥ 80; aşırı ısınma x ≥ 80 ve y ≥ 80 | OHLCV | Getiri iddiası sınanmamış. Proxy olduğunu Tansu kendisi söylüyor. |
| T11 | Bilanço tabanlı sıralamalar: PD/DD + ROE + sektör + 36 çeyrek; TOPSIS; relatif değerleme | p02 M11, M21, M22 | A | K (PD/DD+ROE); X (TOPSIS, relatif) | 36 çeyrek; örnek sektör 2,5 / şirket 1,0 → ucuz adayı | çeyreklik bilanço; OHLCV yetmez | Eşikler ve kriter listesi yok. |
| T12 | VRP (VOL AL / VOL SAT) ve model-free varyans kesişimi | p04 Kart B (pk05); p02 M25 | G | X | Görünen hisselerin hepsi negatif: HEKTS ≈ −0,195, YKBNK ≈ −0,114, ASELS ≈ −0,082, VESTL ≈ −0,065, AKBNK ≈ −0,058 | RV 21g OHLCV'den; IV proxy tanımsız, gerçek IV opsiyon ister | RV tarafı yapı taşı olarak kullanılabilir. Eşikler okunamadı. |
| T13 | Portföy kurma: 3 aşama (10–20 aday → Max Sharpe 3–10 hisse, çekirdek ≥ %50 → vol trading); min-vol / max-Sharpe | p01 K18; p04 Kart M (pk33) | A (K18); G (pk33) | K (zayıf) [p01]; X [p04] | pk33, 20–31 Mayıs 2026 (±1): MV ≈ 115, MS ≈ 108,7, BIST100 ≈ 97,8 | OHLCV | Aşama 1 ve 3 eşiği yok; bileşen ve ağırlık yok. |

### 3. Kurulum dedektörleri

| # | Ad | Kaynak | Düzey | H/K/X | Sadakat hedefi | Veri | En önemli yorum noktası |
|---|---|---|---|---|---|---|---|
| D1 | AB=CD (C'den al / D'de al; D = C ∓ r·(B−A), r 1,0 / 1,27 / 1,618 (M R080)) | p01 K3; p02 M1; p04 Kart A, A-EK (pk01, 03, 32–43); p05 K-05-02 (pk45) | G (tablolar, etiketler) + A (kapı) | K | ISKPL: 5/5 hedef, 0 stop; 100.000 → 710.006,23 (%610,01); getiriler %46,98 / 56,67 / 49,90 / 45,37 / 41,50; C tarihleri 2024-04-03, 2024-08-13, 2025-03-21 (notta 2025-02-21; görsel esas), 2025-06-19, 2026-01-21. SMRTG: 12 kalıp, 7 hedef, 3 stop, 2 açık; 100.000 → 405.327,42 (%305,33) | OHLCV (haftalık da); küm. delta tick/proxy | Yön: p04 SMRTG getirilerini C'den D'ye aşağı (kısa) yeniden üretti; p02 ISKPL pozitif getiri. BIST'te "D'de alım" varyantının Tansu sayısı yok. Stop kuralı, pivot ayarı, oran toleransı yok. |
| | – kapı (T) | p01 K3; ham R019 | T | | BC/AB ≤ 1,00; D, B'yi aşar; C sonrası A aşılırsa bozulur. Ham R019: "BC, AB'yi aşamaz  BC tam 1.00 olabilir D, B'yi aşmalı C'den sonra fiyat A'yı geçerse patern bozuldu sayılır" | | Bozulma fitil mi kapanış mı yok. Oranlar (M) R080 gövdesi: BC "(0.382, 0.50, 0.618 vb.)", CD "(1.00, 1.27, 1.618 vb.)"; Tansu'nun cümlesi yalnız onay: "Doğru kod böyle yazılır." |
| | – katılım vetosu | p05 K-05-02 | G | X | BALAT: D(CD=1.27AB), küm. delta uzun süre negatif; "her zaman çalışmaz" | tick/proxy | Veto kuralı sayısız. Olumsuz örnek fikstürü olarak kullanılır. |
| D2 | Gartley: D girişi (limit), stop X, TP merdiveni; haftalık talep alanı taraması | p01 K2; p04 Kart A (pk02: SOKE, LUKSK); p06 M06-16 (pk122, 123) | G | K | SAYAS: X≈20,65, A≈144,25, B≈68, C≈122, D≈47,15 (XA'nın 0,786'sı) [piksel]; TP1 ≈ 73,65 = D+(D−X); TP2 ≈ 107 = D+0,618·(A−D) = 107,2. LUKSK: giriş = D = 86,95, stop (X) 73,00. SOKE D 12,53 | OHLCV (günlük/haftalık) | pk123 tablosu: B = XA 0,618, C = AB 0,382–0,886, D = XA 0,786, SL = X veya X − 2·ATR, TP1 %50. Tablodaki boğa D formülü standart tanıma ters; standart tanım kullanılır, "Tansu" olarak birebir üretilemez. Ham: tolerans %3–5 ve "Ödül / Risk < 1.5 ise … işleme girilmez" (M) R222; tepki penceresi 10 gün (T) R014. |
| D3 | Butterfly (bullish; ayrı tarayıcı) | p03 M5; p01 K1 (ALARK bearish) | G | K | DOAS: A 209,10; X 170,10; B ≈ 178,45 (XA 0,786); D 159,40 [TAMAMLANDI]; 1,272 = 159,49; 1,618 "max risk" = 146,00. ALARK: 125,42'ye kadar long (A) | OHLCV | Giriş, stop, yukarı hedef yok. "D hedefi" aşağı projeksiyon, kâr hedefi değil. Gartley ve Butterfly ayrı tarayıcı: ham (T) R011 "Gartley taramasını ayrı yapın butterfly taramasını ayrı yapın". |
| D4 | Diğer harmonik: Three Drives, Lindsay Trident, Siyah/Beyaz Kuğu | p03 M6; p05 K-05-04 (pk47); p04 Kart J (pk34, 35) | G (görsel) + A (Three Drives kuralı) + T (Trident formülü R090) | K (Three Drives, Trident); X (Kuğu) | Three Drives (A): ara düzeltme 0,618/0,786, uzatma 1,272/1,618, süre 10 bara karşı 11–12 bar dengeli. Trident: D = (B×C)/A (T R090: "D = (B \* C) / A"). LIDER 127,40 | OHLCV | Three Drives görselinde fiyat ekseni yok. Trident formülü ile görseldeki "CD=1.27AB" aynı değer mi doğrulanamadı. Kuğu oranı yok. |
| D5 | X–B trend çizgisi kırılımı (D'ye kadar taktik) | p01 K1; p04 Kart A (DGATE, SOKE) | G (etiket) + A | K | KAPLM: X≈330, A≈745, B≈500–505, C≈680, D 424,23 (okunan); çizgi Haziran'da aşağı kırıldı, D'de tepki yok | OHLCV | Giriş fiyatı, stop, kırılım bazı yok. "SAT (taktik KISA, D'ye kadar)" BIST'te açığa satış. |
| D6 | Kanal alt bant teması / yükselen destek tepkisi | p03 M3 (AEFES); p04 pk43 (RYSAS); p06 M06-02 (pk93), M06-22 (pk117), M06-11 (pk103) | G | K (AEFES, GEDZA); X (pk117, AKSGY) | AEFES: Lookback 120; alt bant 17,76; Low 17,92 (+%0,92); kapanış–bant +%2,56; temas 3/3; genişlik +%15,3 | OHLCV | Kanal çizimi, temas toleransı (≥ %0,92), "tepki" tanımı, stop, hedef yok. |
| D7 | Düşen direnç kırılımı (+ retest, + talep) | p03 M4; p05 K-05-14 (pk64); p04 pk34 | G | K [p05]; p03: yalnız yapı K, giriş X | LIDER: 127,40, kırılım 2026-05-18, Temas 3, Lookback 20. BALAT: 75,95, kırılım 2026-05-15 (notta 05-19; görsel esas), Temas 3, Lookback 30 | OHLCV | Tolerans, kapanışla mı, retest penceresi, stop, hedef yok. Girişi biz tanımlarsak yorum olur. |
| D8 | Konsolidasyon → kırılım → FVG → range-high retest → teyit (AKFIS "A+") | p03 M2 | G | K | AKFIS [piksel]: ENTRY ≈ 3,75; STOP ≈ 3,62; TP ≈ 3,87 / 3,94 / 4,00 (R ≈ 0,9 / 1,4 / 1,9). Alıntı örnek: ENTRY ≈ 114; STOP ≈ 106,6; TP ≈ 120,0 / 121,9 / 129,9 (R ≈ 0,7 / 1,0 / 2,0). Skor 100/100 | OHLCV (VolMA20) | İki örnekte R katları tutarsız: sabit 1/1,5/2R kuralı çıkmıyor. Konsolidasyon, FVG toleransı, teyit tanımı, TP kaynağı yok. |
| D9 | Fincan-kulp | p05 K-05-10 (pk58) | G | K | GUBRF: Fib 317,00 → 212,20; kırılma 300,75; hedef 389,30 = 300,75 + (300,75 − 212,20); R/R 1:2,27 (ima edilen stop ≈ 261,7, benim aritmetiğim); sinyal 2025-10-24, tamamlanma 2025-10-28 | OHLCV | Fincan/kulp dedektörü ve stop yok. Kulp dibi %61,8'in altında (görsel). |
| D10 | Gizli pozitif uyumsuzluk (higher low / osilatör lower low) | p05 K-05-11, K-05-22 (pk60, 61, 74) | G | K (pk74 formül gizli: X) | Swing=15 sol-only, MinGap=15; ≈ 540 → 690 (≈ +%28; notta %29) | OHLCV | Osilatör kimliği, giriş tetiği, stop yok. Sol-only = yeniden çizim riski. |
| D11 | EMA sıkışması (EMA20/50/100/200; demand içi EMA5/8/13) | p05 K-05-15 (ICBCT), K-05-17 (KRDMD), K-05-21 (pk71); p06 M06-09 (pk106), M06-01 (pk92) | G | K (KRDMD'de setup ölçüsü H) | KRDMD: tolerans %1,2, min 3 gün, 17.12.2025 → 14.01.2026 (20 gün), ort. oran %0,64. ICBCT: EMA20 14,44 / EMA50 14,29 / EMA100 14,31 / EMA200 14,42 (aralık ≈ %1,04, benim hesabım) | OHLCV ("1 periyot" günlük mü kesin değil) | Oran formülü görselde yok. "Pre Signal" tetiği gizli. EMA5/8/13 için eşik yok. Dragonfly işareti görselde yok (X). Ham: (T) R198 "Ben 5-8-13 kullandım"; (T) R132 "ortalamaların sıkışma alanları genelde patlamaya işaret eder"; eşik (T) R127 "sıkışma rasyosu sizin tecrübenize kalmış" → eşik yorumdur. |
| D12 | Çift rotasyonu / stat-arb (Z ±2, momentum dönüş onayı, T+1 açılış) | p03 M1 (+ kointegrasyon notu); p05 K-05-06, 07, 08 (pk51–55); p02 M6, M7, M8 | G (raporlar) | K [p03, p05]; X [p02 M6–M8] | VAKBN–GARAN: 100.000 → 152.862,86 (%52,86); B&H %20,88; MDD −%27,44; Sharpe 0,929; Sortino 1,338; CAGR %28,93; 6 geçiş; maliyet 2.054,78 TL; piyasada kalma %72,27; Son Z −3,108, önceki −3,404. CIMSA–OYAKC: +49.245 TL (+%49,2). AGROT–GARAN: 3 işlem; 2025-12-12 Z 2,05 → 2026-02-16 çıkış Z 0,37 (92.354,65) → 2026-03-09 Z −2,01; 20.04.2026 +%13,44 (B&H +%0,91), 23.04.2026 +%8,76 (B&H −%3,55). Olumsuz örnek (pk53): ≈ 100.000 → 79.000 | OHLCV (kapanış + açılış) | Z formülü ve penceresi yok. Nisan 2025'te Z ≈ −2,3 ve −2,0 iken işlem yok: ek kapı olabilir (p03; kointegrasyon p 0,048, Pair Quality 55,600/100). AGROT çıkışı Z 0,37 (G); "0,5 çevresi" A. Bacak yapısı (long-short mu) kanıtsız. Ham: giriş "Z-Skoru +2.0 seviyesini yukarı kırarsa", çıkış "normale (0.5 seviyelerine)" R101 (biçimi (M)'ye yakın); ek kapı adayı (T) R228 "Arbitraj için Cointegration (Eşbütünleşme) şarttır" ve (T) R034 "çok azı rolling cointegration ile zamanla bozulmayı önlüyor". Raporda p 0,048 (anlık) geçiyor; Nisan 2025 sessizliğini **rolling** kointegrasyon açıklıyor olabilir (varsayım, sınanacak). |
| D13 | BOS → HH → Fib 0,618–0,786 → FVG/Order Block teması | p06 M06-07 (pk105); p01 K5 | G (Fib etiketleri) + A (zincir) | K [p06]; X [p01 K5] | Fib 0,0 = 216,77; 0,382 = 191,32; 0,5 = 183,46; 0,618 = 175,60; 1,0 = 150,15. Stop Fib 1,0 altı; TP1 Fib 0,0 | OHLCV; p01'de ek H4 OHLC | Çelişki gerekçesi: p06'da sayılı kural zinciri var, p01 K5'te 0,618 dışında sayı yok. Pivot, BOS bazı, FVG/OB tanımı, giriş fiyatı yok. |
| D14 | Elliott: dalga 2 + Fib + fresh FVG; dalga 4 geri alım; CWENE dalga 2 + demand | p06 M06-08 (pk107, 110, 102); p01 K4; p03 M10 | G (etiket) + A (kural) | K [p06, p01 K4 formül]; X [p03 M10, dalga sayımı] | BRYAT "Elliott Wave 2 (Fibo %64,3)"; ENJSA "Wave 4 (Fibo %54,0)", Wave 5 hedefi ≈ 94. Kural (A): impulse ≥ %10, geri alım %50–78,6 (ideal 0,618–0,65), stop Point0, TP1 Point1, TP2 C + 1,618·W1. Dalga 4: P4 = P3 − r·(P3−P2), r = 0,24 / 0,38 / 0,50. CWENE: 33,10 → 48,30; iptal 33,10 altı (not) | OHLCV | Dalga sayımı öznel, otomasyonu zor. Sabit kural "swing low → swing high ≥ %10 → geri alım" olarak yazılırsa yorum bizimdir. |
| D15 | Confluence kapısı: formasyon × arz-talep; swing + talep + HSAR; çoklu aralık Fib kümeleri | p01 K17; p04 Kart I (pk21); p05 K-05-24 (pk78); p06 M06-17 (pk120), pk112; p03 M8 | G (etiket) | X [p01, p04, p05]; K [p06 M06-17, yapı taşı olarak] | yok. Etiketler: GC=F 4448,90; PETKM 19,88; kümeler x1 ≈ 44,0–44,8, x2 ≈ 45,6–46,2 [piksel] | OHLC | HSAR tanımı, çakışma ve küme toleransı yok. "Bağımsız" kanıtlar aynı fiyat serisinden (p06 pk112 notu). Sınav fikri: aynı formasyon bölgeli / bölgesiz. |
| D16 | A/D–EMA3 (long/short durum stratejisi) | p05 K-05-23 (pk75) | G (+A kod) | K | Strateji %19,1; B&H %10,8; Sharpe 0,67; MDD ≈ −%17; OPT1 = 3 | OHLCV | Kural `AD() [op] Ref(Mov(AD(),opt1,E),1)`; [op] okunamadı. BIST'te short. Dönem ve maliyet yok. |
| D17 | Ortalamaya dönüş / bant aşırılığı: Bollinger kuyruğu, −1SD al / −2SD stop, AZTEK "ayı tuzağı" | p01 K12; p06 M06-03 (pk97), M06-19 (pk127) | A (K12'de X bağlantısı, kural yok) | X | yok. Kitap görseli: ±1/2/3 SE, %68 / %95 / %99,7 (G) | OHLCV (IV yerine realize vol); OBI emir defteri ister | k, pencere, IV kaynağı yok. "geri dönmek zorunda" (M R226) şişman kuyruk ile çelişir. Ham: (T) R156 "Mean reversion, absolute pricing oscilator kullanılarak oluşturulan bir strateji" (parametre yok); R053 −2/−3 SE "tepki alımı fırsatı". |
| D18 | Kuralı eksik / atfı zayıf: HalfTrend + momentum; Williams %R + SMA14 (30 dk); beş kapı çerçevesi; APO EMA10–40; gizli filtreli breakout; BOM; AHENK | p01 K9; p02 M2, M5; p05 K-05-25 (pk85), K-05-01 (pk44); p03 M7, M8 | A / G | X (HalfTrend ve Williams K, zayıf) | Williams: hedef ≥ 2R (A); notun backtest rakamları Cevo'nun, hedef sayılmaz | Williams 30 dk gün içi; diğerleri OHLCV | Atıf: ikisini de Tansu paylaşmış (R148 kod satırı, R170); Williams kural gövdesi (M). Beş kapıda "stop R/R'ye göre" (A) yapı stopuyla çatışır (bkz. Y1). Ham: Williams %R kuralı R170'te tam (M; "Williams %R: 14", 30 dk), Tansu'nun cümlesi yalnız "Bi bakın bakalım backtesti nasıl"; HalfTrend R148 (T) "if (half_trend[t] == 'buy' and momentum[t] > momentum_threshold)" eşik yok. |
| D19 | RSI 30 girişi, iki aşamalı çıkış | ham R233 (beyin: tweet-rsi30-giris-iki-asamali-cikis) | M (kural metni) + T (kullanım: "ilk %50 kar aldiğımız RSI70 reddi") | K; sadakat sınıfı "yorum" | yok (grafik yapıştırılmamış; kayıtta görsel yok) | OHLCV | Kural tam: giriş RSI(14) 30'un altından yukarı keser ve üstünde kapanır; RSI 70 üstünden altına kapanışta %50 sat; önceki gün dibi altında kapanışta kalan %50. Açık: iz süren stopun "risk/ödül oranı hedefi" sayısı ve stop yok. |

### 4. Teyit / tetik

| # | Ad | Kaynak | Düzey | H/K/X | Sadakat hedefi | Veri | En önemli yorum noktası |
|---|---|---|---|---|---|---|---|
| C1 | Tepki penceresi (D sonrası) ve durum etiketleri | p01 K2; p04 pk01–03 | G | K | KAPLM: "D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ)". Etiketler: AKTİF, TEPKI_VERDI, BOZULDU, TAMAMLANDI | OHLCV | Ham: (T) R014 "10 gün içinde D noktasından bir tepki yapmıyor ise belirsiz bir yapı olarak bakılabilir": 10 gün de D sonrasıdır. Görselde iki ayrı ifade var ("20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ)" ve "C sonrası son 10 günde"); 20 bar ve 10 gün ayrı parametreler olabilir, ikisi de koşulur. Asgari hareket yok. Durum etiketleri yalnız görselde (hamda metin yok). |
| C2 | Retest teyidi | p06 M06-11 (pk103); p03 M2, M4, not-backtest; p01 K7 | G | X | AKSGY: "RETEST VAR (6 kez)", ilk temas 2025-10-14, son temas 2025-12-08, temas sonrası 9 gün; ADX 34,13, RSI 41,13, MACD −0,013 | OHLCV | Kural yok. Retest'in katkısı hamda ölçülmemiş: (T) R194 "İşte bu yüzden retest beklemek önemlidir" tek örnek; (M) R198 retest girişi. "Retest beklemek yarar sağlıyor mu?" sorusunun ham metni yok (R255 yalnız bağlantı); beyin notu onu Tansu'nun 2 Eylül gönderisine bağlıyor, doğrulanamıyor. Ölçüm katmanı cevaplar. |
| C3 | Hacim / OBV / küm. delta teyidi | p06 pk104, pk121; p05 pk45; p01 K7 | G | H (OBV: close_t > close_t−1 ise OBV += hacim, düşerse −=); X (delta) | yok ("Fiyat ve OBV Senkronizasyonu = Yüksek Güven", G) | OHLCV (OBV); delta tick/proxy | Eşik yok. Delta tanımı bilinmiyor. |
| C4 | Mum dedektörleri: bullish engulfing (kod), engulfing + EMA34, Tweezer Bottom, Advance Block | p01 K8; p06 M06-01 (pk92), pk76; p02 M18; p04 Kart G (pk12) | G (kod) | H (engulfing); K (engulfing + EMA34); X (Tweezer, Advance Block) | yok. Engulfing: close[i] > open[i]; close[i−1] < open[i−1]; open[i] < close[i−1]; close[i] > open[i−1] | OHLC | Giriş zamanı, çıkış, bağlam yok. KLMSN'de Buy Signal (24 Şubat) engulfing mumundan önce. |
| C5 | CHoCH / BOS + alt zaman dilimi onayı (1H/4H) | p05 K-05-19 (pk69); p04 Kart F (pk11); p03 M11 | G (etiket) + A (tanım) | K | yok | OHLCV ile FVG/BOS; 1H/4H CHoCH gün içi ister | Pivot ayarı, kapanış/fitil, tampon yok. Ham (M) R199: "Fiyat FVG bölgesine gelmeden dönerse işlem yapılmaz"; 1H/4H CHoCH (M) R129. |
| C6 | Gün içi breakout / gap / retest | p01 K7 | A | K | yok | OHLCV alt kümesi; delta tick | "Kararlı kapanış", hacim eşiği, ATR çarpanı yok. |

### 5. Yönetim

| # | Ad | Kaynak | Düzey | H/K/X | Sadakat hedefi | Veri | En önemli yorum noktası |
|---|---|---|---|---|---|---|---|
| Y1 | Yapı stopu (X, Point0, Fib 1,0 altı, demand/distal altı) | p01 K2; p04 Kart A, E-EK; p05 K-05-10; p06 M06-07, 08, 10 | G | K | LUKSK stop 73,00; BALAT STOP 64,00; DOAS 1,618 "max risk" 146,00; RBR: proximal = giriş, distal = stop; CWENE iptal 33,10 | OHLCV | Ham güncellemesi (06.10): "yapı esas" hükmü kaldırıldı (sentez İ4). Hamda dört stop ailesi var: yapı (T R019, R043), ATR (R224, R212), yüzde ve R:R ((T) R234 "%2 Stop, %3 Kar Al"; (M) R230), SD bandı ((M) R187). Yapı stopu modülün geçersizliğidir; çıkışı Y3 zinciri yönetir; aileler ölçümde karşılaştırılır. |
| Y2 | Hedef merdiveni | p01 K2; p04 Kart A-EK (pk43); p05 K-05-10; p06 M06-08, 10, 16, 18 | G | K | RYSAS: 22,60 / 24,20 / 26,80 = D + {0,618; 1; 1,618}·(A−D). SAYAS: TP1 ≈ 73,65, TP2 ≈ 107. BALAT: 84,88 / 87,02 / 90,50 / 92,98 (r 0,382 / 0,618 / 1,0 / 1,272 · (C−D), D ≈ 81,4 nottan). GUBRF 389,30. Gartley: TP1 = D + 0,382·(A−D). Elliott TP2 = C + 1,618·W1 | OHLCV | Çapa çelişkisi: BALAT C−D üzerinden, Gartley tablosu ve SAYAS A−D üzerinden. İki çapa ayrı parametre olmalı. |
| Y3 | Kısmi kâr + iz süren stop: [T R224/R239] +1,5 ATR'de iz süren mod aktif, sonra önceki gün dibi altı kapanışta %50, 2 ATR acil; [M R203, pk123] TP1'de %50 + stop girişe | p06 M06-15 (pk125), M06-16 (pk123), pk109; ham R224, R233, R239 | T (ham) + G (pk123: "Pozisyonun %50'sini Kapat") | K | pk125: "STOP: 104.34 / ATR: 4.62" (düşük çözünürlük) | OHLCV | Ham (T) R224: "fiyat Giriş + 1.5 ATR seviyesine ulaştığında Trailing Stop (TS) aktif hale gelir" / "önceki günün en düşüğünün altında kapanış ve %50 satış, ve emergency stop 2atr ile kalan tüm maldan çıkış"; ilk kâr "%10 (sizin belirleyeceğiniz)". R239: statik (giriş ATR) ve dinamik (o günün ATR) iz süren stop. Açık: ATR periyodu. |
| Y4 | Önce kayıp bütçesi: %1 risk, adet = risk / 2 ATR, acil stop = giriş − 2 ATR, gün sonu stop = kapanış < 250 günlük ortalama | p06 M06-14 (pk115); p01 K13; ham R212 | G-dış (NotebookLM infografik) + T (R212 "sermayenizin ancak %1'ini kaybetmek riskini göze alabilirsiniz", "250SMA") | K (yorum) | yok (G-dış); infografik örneği: 100.000$ sermaye, 2 ATR = 14,30$ → 1.000$ / 14,30 ≈ 70 hisse (69,93) | OHLCV (acil stop için günlük H/L yaklaşık) | Kural (G-dış) NotebookLM; T R212 yalnız %1 örneği ("Diyelim ki") ve 250SMA'yı giriş bileşeni sayar (görselde çıkış). Boyutun volatiliteyle ters olması (T) R211. p01 notu "500 TL / 2 TL = 250 lot" (M R184). ATR periyodu ve SMA/EMA ayrımı yok. |
| Y5 | Gün sonu sabit ağırlık yeniden dengeleme | p04 Kart L (pk37); p02 M12 | G | H [p04]; K [p02] | GARAN %50 / KGYO %40 / CCOLA %10; 01.04–15.05.2026; 100.000 → 126.764,84 (%26,76); pasif 127.805,42 (%27,81); fark −1.040,58 (−%1,04); 30 işlem | OHLCV (kapanış) | Gerekçe: p04 görselde tam rapor var; p02 notunda parametre yok. Tabloda pasifin gerisinde (%26,76 / %27,81); tweet metni (R078 "sistem getirisi 1.5 yada %27") bunu anlatmıyor: Kör nokta 1 örneği. Maliyet ve işlem fiyatı yok. |
| Y6 | Zayıflık / çıkış uyarıları: haftalık Gravestone Doji, OBO boyun kırılımı, Advance Block | p05 K-05-20 (pk70); p06 M06-18 (pk121); p04 Kart G | G (+A) | K (Gravestone, OBO); X (Advance Block) | OBO hedefi = baş–boyun mesafesi (G). Gravestone: tepe ≈ 150, gövde ≈ 112 [piksel] | haftalık/günlük OHLCV | Gövde/gölge eşiği yok. OBO long-only evrende yalnız çıkış uyarısı olur. |

### Kapsam dışı (strateji değil)

Değerleme (ASUZU, ARCLK, FROTO F/K ve FD/FAVÖK, EREGL DCF, CoE/WACC, Merton, Gordon, FCFE/DDM, ROC, bilanço kontrol listeleri), ML ve
ANN çıktıları (ML 13 günde 9 isabet %69,23), eğitim ve yöntem notları (ARIMA, GARCH, algoritma tasarımı, Python öğrenme), HFT ve
emir defteri araştırması, makro ve veri notları (USD/TRY forward, TSLA implied move, FED, CME araç haritası), kitap/repo önerileri.
Backtest ilkeleri (p03 not-backtest, p02 teknik-indikator değerlendirme) modül değil; ölçüm katmanının girdisidir.

### İlk dalga önerisi (ham güncellemesi, 06.10)

Ortak kapı: rejim (R3 şok freni, Güçlü; ortalama kapısı R4 yorum, kapılı/kapısız iki kol). Boyut: volatiliteyle ters
(T R211); %1 / 2 ATR yorum parametresi (Y4). Zincir modül başına:

| Modül | Teyit | Çıkış | Sadakat |
|---|---|---|---|
| D1 AB=CD | Üç kol: **C girişi → D çıkışı** (sadakat kolu; (T) R018 "AB=CD 1000 günlük C noktasından alım yapılsa idi D satış karları"); D'de limit; tepki teyidi (C1: 10 gün, 20 bar) | geçersizlik (T R019) + Y2 hedef / Fib iz süren (T R090); ATR zinciri ayrı kol | Tansu: ISKPL 5/5, SMRTG 7/3/2 (G tablolar, C→D işlemleri); kapı (T) R019, oranlar (M) R080. Yön: SMRTG getirileri C→D aşağı (kısa); BIST'te kısa yok, bu tablo "D'de alım" kolunda karşılaştırma için kullanılmaz |
| D11 EMA sıkışması | C2: breakout mumu / retest ((M) R198) | stop demand altı (M R198) + Y3 | çapa KRDMD (EMA20/50/100/200, tolerans %1,2, min 3 gün; G); varyant EMA 5-8-13 (T R198 tek cümle); eşik yorum (T R125, R127) |
| D19 RSI 30 | yok (kesişim kuralı) | kendi iki aşamalı çıkışı (M R233) + 2 ATR acil (T R224) | yorum: grafik yapıştırılmamış; **açık kural ölçümü**, sadakat testi değil |

Ayrı koşu: D12, kointegrasyon kapısıyla (T R228; rolling, T R034: varsayım).

Seçim gerekçesi: D1 hem sadakat çapası (Tansu'nun en somut sonuç tabloları) hem (T) geçersizlik kuralı taşıyor. D11
Tansu'nun savunduğu fikir (İ9) ve KRDMD sınanabilir sayı veriyor. D19 sadakat için değil, kuralı tam açık bir gösterge
stratejisinin motoru uçtan uca sınaması için. Tansu'nun akışında kurulumlar momentum ön elemesinden geçen hisselerde
aranır (T R189); ilk dalga ön elemesiz koşar, sonuç bu notla okunur. D2 Gartley ikinci dalgaya kaldı:
Tansu'nun tablosundaki D formülü ters (pk123), "Tansu" sınıfı birebir üretilemez. Sadakat sayıları (Y2 RYSAS/SAYAS,
D12 VAKBN–GARAN ve AGROT–GARAN) katalog satırlarındadır. Ham öncesi eski öneri (R4 → D1, D2 → C1 → Y4, Y2; ayrı D12)
geçersizdir.

## Ortak yapı taşları (birleştirme)

Modül no'ları katalogdaki R/T/D/C/Y numaralarıdır. "Birinci el" = Tansu'nun görseli/kodu (G) tanımı veriyor mu.

| Yapı taşı | Kullanıldığı modüller | Tanım nereden / birinci el mi |
|---|---|---|
| Tepe-dip (swing/pivot/ZigZag) | D1–D5, D9, D13, D14, C5, Y1 | Ayar hiçbir yerde yok. Birinci el yalnız etiketler (HH/HL/LH/LL, Swing Points) ve parametre izleri: "Swing=15 sol-only, MinGap=15" (p05 pk60), "Lookback 20/30/120", "Temas 3" (başlıklar). İki pivot + delmeme kuralı A (p02 M16). Pivotun "bilindiği an" tanımı yok (p06). ZigZag adı okunan bölümlerde geçmiyor. |
| Fib seviyeleri / kümeleri | D1–D4, D9, D13, D14, D15, Y2 | Birinci el: SAYAS, DOAS, GUBRF, BOS-Fib ölçekleri (0,236 … 1,618); extension 1,0 / 1,27 / 1,618 (RYSAS, A1CAP etiketleri). Kümeler/çoklu aralık (p06 pk120): slayt, Tansu'ya aidiyeti belirsiz; "statik tek çizgi" eleştirisi G ama aidiyet belirsiz. Küme toleransı yok. |
| Arz-talep bölgesi (distal/proximal) | D6, D13, D15, C5, Y1, R10 | Birinci el: p04 pk09 şeması birebir ("distal = base'in en yükseği, proximal = base'in en düşük gövde fiyatı"); RBR: proximal giriş, distal stop (pk15); kırılım: close < zone_low (pk13, not). Talep aynası çıkarım. Base seçimi ve bölge üretimi hiçbir yerde yok. |
| FVG | D8, D13, D14, D15, C5 | Şekil G: "FVG %50" lejantı (AKFIS), imbalance güç şeması (pk17). Formül (bullish: low3 − high1 > 0) notta, birinci el değil. Güç sınıfı ve "fresh" eşiği yok. |
| Order block / sponsor candle | D13 | Sponsor candle şeması G (pk20: sert hareket öncesi son zıt renkli mum); OB tanımı yok (p06 pk105'te yalnız adı). |
| Kanal / trend çizgisi | D5, D6, D7, D4, C2 | Çizim yöntemi yok; G yalnız lejant ve çıktı alanları (Lookback, Temas, Alt bant, Low–Bant %). X–B çizgisi lejant G ("Trend Çizgisi (X->B uzatılmış)"). |
| Hacim profili yaklaşımı | R10, C6 | Birinci el yalnız grafik/lejant ("Gaussian VP (POC/VAH/VAL)", ACSEL; "VWAP + Volume Profile + Delta", ALKIM). Hesap yok. Günlük OHLCV ile yalnız yaklaşık profil (etiketli). |
| ATR | Y3, Y4, D2, C6, R9 (yerine std) | Birinci el: "SL = X_Fiyat − ATR*2" (p06 pk123), 2 ATR (pk115), "ATR: 4.62" (pk125). Periyot hiçbir yerde yok. |
| EMA / SMA / WMA | R4, R5, R6, D11, D16, Y4 | Birinci el: "WMA Close 21" (XU100); EMA20/50/100/200 (KRDMD, ICBCT); EMA5/8/13 (araç lejantı); SMA18/35 (pk98); SMA20/50 (pk113); OPT1 = 3 (pk75). "250 günlük hareketli ortalama" türü belirsiz (pk115). |
| CHoCH / BOS | R4, C5, D13 | Tanım A (p04 not-kaynak): BOS = trend yönünde önceki swing kırılması; CHoCH = korunan karşı swing'in ilk kaybı. Etiketler G. Pivot ayarı ve kapanış/fitil yok. |
| Z-skor / spread | D12 | Etiket ve ±2 çizgileri G; spread formülü ve pencere yok. ΔZ = Z_t − Z_{t−1} tutarlı (p03: 0,296 hesabı). |
| Mum geometrisi, engulfing | C4 | Birinci el kod: üst/alt gölge (p05 pk76); engulfing 4 koşul (p01 K8). |
| OBV, klasik günlük pivot, realize vol | C3 (OBV), R9 (realize vol); klasik pivot hiçbir modülde kullanılmıyor | Birinci el formül: OBV (pk104), P/R1–R3/S1–S3 (pk100), std × √252 (pk124). |
| Medyan (ortalama yerine) | T1 (anomali dışlama), R8 (CS medyan) | (T) birebir: "Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın" (ham R001); anomali kuralı G (|30g| > %50). Sentez İ7: Tansu'nun kendi araçları ortalama kullanıyor; medyan yalnız sıralama/ölçüm katmanında. |

## Açık sorular

- **(06.10, beyin notları düzeltildi; her biri görsel açılarak):** ISKPL 3. işlem tarihi 2025-03-21; TTRAK tablosu TOASO
  2025/9 = 2,30 (sektör ortalamaları artık uzlaşıyor, ortalama prim %53,6); paket 07 HKTM +12,62 (ekran özeti satırlarla
  birebir; "iç tutarsızlık" bulgusu geri alındı); paket 08'de OZATD satırı yok (07↔08 "düşük float" bağı geri alındı);
  paket 93 EMA 5 ve EMA 13; paket 111 görseli "takvim günlerini sayın" diyor; paket 71'de Dragonfly etiketi yok (Tansu
  metinde anıyor). Paket 123: not doğru, hata Tansu'nun tablosunda (boğa D = X + (A−X)·0,786 ters).

- **(orkestratör, 06.10, iki görsel bizzat okundu: `assets/kaynak-vakbn-garan-rotasyon-…/rapor.webp`, `grafik.webp`)**
  Çift rotasyonu iki yönlü: Z ≥ +2'de dönüşte "GARAN AL" (X), Z ≤ −2'de yukarı dönüşte "VAKBN AL" (Y); işlem etiketi
  dönüşten sonraki günde (T+1 Open), ör. Eyl 2025 ve Tem 2026'da Z ≈ −1,8'de. Rapor "Z donusu +0.30" = −3,108 − (−3,404):
  ΔZ = Z_t − Z_{t−1} yeniden doğrulandı. Arka plan gölgesi elde tutulan hisseyi gösteriyor (mavi GARAN, yeşil VAKBN),
  bir "sağlık dönemi" değil — parça 03'ün gölge yorumu zayıf. Ara 2025'te Z ≈ −3,5 iken işlem yok: zaten VAKBN'de.
  Nisan 2025'te Z ≈ −2,2 iken işlem yok ve portföy Haziran sonuna kadar düz: açıklama hâlâ açık; Z serisi Mart ortasında
  başlıyor, yani uzun pencereli bir ısınma (kointegrasyon/sağlık) ya da test başlangıcı olabilir. Raporda kapı adayı
  metrikler birinci elden var: "Cointegration p 0.048 CURRENT", "Pair Quality 55.600 /100", "Pair Health GUCLU",
  "Beta CV 0.277", Half-Life boş. Z formülü ve pencereler görselde yok — X'te de yayımlanmamış olabilir.
- (parça 03) Çift rotasyonu: VAKBN–GARAN grafiğinde Nisan 2025'te Z ≈ −2,3 ve −2,0 iken işlem yok, portföy Haziran
  sonuna kadar düz. "Z ≤ −2 ve ΔZ > 0" tek başına yetmiyor; ek bir kapı (kointegrasyon / çift sağlığı) olabilir.
  Bilet 06'nın Z'yi üretememesinin bir sebebi bu olabilir.
- (parça 03) AKFIS kırılım+FVG: hedef katları iki örnekte tutarsız (≈0,9/1,4/1,9R ve ≈0,7/1,0/2,0R).
- (parça 03) 80–100 hafta yatay tarama notu önceki dizinde yoktu.
- (parça 02) Hacim profili (POC/VAH/VAL + VWAP) ve denge/dengesizlik (auction) notları önceki katalogda yok.
  Günlük veriyle hacim profili ancak yaklaşık kurulur (gün içi hacim dağılımı yok).
- (parça 02) Not–görsel farkları: ISKPL 3. işlem görselde 2025-03-21, notta 2025-02-21; TTRAK tablosunda TOASO
  2025/9 görselde 2,30, notta 2,00. Sadakat hedefi görselden alınır.
- (parça 06) Not–görsel farkları: paket 111 görseli Fibonacci gün sayımında "takvim günlerini sayın" diyor, not tersini;
  paket 93 notu EMA3/8/13, görselde EMA5 ve EMA13; Gartley tablosunda (123) boğa D formülü standart tanıma ters.
- (parça 06) 86–128 arasında Tansu'nun backtest tablosu yok; yalnız seçilmiş örnekler (ör. BALAT TP 84,88 / 87,02 /
  90,50 / 92,98, stop 64,00). Bu paketlerden gelen modüllerde sadakat hedefi tek örnek düzeyinde kalır.
- (parça 05) Çift ailesinin daha çok örneği var: CIMSA–OYAKC (51), AGROT–GARAN (52/54/55) ve bir olumsuz örnek (53).
  Parça 03'teki "ek kapı" sorusu bu örneklerle birlikte sınanmalı.
- (parça 05) Paket 71: notun "Dragonfly işaretli" dediği etiket görselde yok.
- (parça 01) Harmonik hedef merdiveni: SAYAS'ta ".618 AD" etiketli (07.10 okuma düzeltmesi) TP2 ≈ 107, D + 0,618·(A−D) = 107,2 ile uyuyor
  (C–D üzerinden ≈ 93 olurdu). Önceki "kaynaklar çelişiyor" yargısı zayıflar.
- (parça 04) AB=CD yönü: SMRTG getirileri C'den D'ye AŞAĞI yönlü fiyat farkı olarak yeniden üretildi (kısa yön);
  paket 03 notu "yükseliş" diyor. KURALLAR'daki tespit doğrulandı. BIST'te açığa satış yok: modül "D'de alım"
  varyantıyla (hedef 0,618 / 1,0 / 1,618) kurulmalı ya da kısa yön ayrı tutulmalı.
- (parça 04) Not hataları: paket 07'de HKTM notta −12,62, görselde +12,62; paket 08'deki OZATD %13,22 satırı görselde yok.
- (parça 04) Gün sonu rebalancing: Tansu'nun kendi raporunda pasifin 1,04 puan gerisinde (olumsuz sonucu da paylaşıyor).
- (parça 01) Gartley tepki penceresi: KAPLM'de "20 bar" ve "son 10 gün" aynı araçta iki ayrı test olabilir; önceki
  okumanın saydığı çelişki tek çelişki olmayabilir.
