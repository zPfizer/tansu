# Ham sentez B: R131–R263 ile İ1–İ8 yeniden tartımı

Kapsam: R131–R263 (133 kayıt, hepsi okundu). R245–R263 (19 kayıt) yalnız tweet bağlantısı; metin yok, bu yüzden kanıt değeri sıfır. Açılan görseller (kayıt numarası): R188, R196, R200, R208, R209, R212, R213, R215, R216, R217 (G2, G4), R219. Açılmayan görseller: R161, R165, R167, R168, R173, R177, R191, R207 (metin yok, okuma yok).

İşaretler (sahiplik):
- **[T]** Tansu'nun kendi cümlesi gibi okunuyor (birinci tekil, sohbet, kendi çalışmasına atıf). Kesin değil.
- **[M]** Açıklayıcı ders metni. Tansu hesabında paylaşılmış. Kendi görüşü mü, LLM/kitap aktarımı mı belirsiz. Ağırlığı düşük.
- **[G]** Görsel okuması. "NotebookLM" imzalı infografikler dış üretimdir; Tansu paylaşmış ama yazarı o değil.
- **[B]** Beyin/otomasyon başlığı. Tansu'nun metni değil.

Önemli uyarı: R138 ("Sizin grafiğiniz ise 'yavaş ama kararlı'…"), R210 ("Grafik (Panel 2): Mavi çizgi…"), R192, R197, R199 gibi uzun metinler Tansu'nun grafiğini yorumlayan bir model çıktısına benziyor; Tansu bunları paylaşarak onaylamış olabilir ama her cümle onun görüşü olmayabilir.

---

## İ1. Önce rejim, sonra işlem

**DESTEK (9)**
- D1 [M/T] R131: "piyasa hareketli ortalamanın altındaysa, bu durum satış yönlü; hareketli ortalamanın üzerindeyse, alış yönlü işlem yapılması gerektiğini gösterir. … Trend is your friend."
- D2 [M] R190: "Denge günlerinde trend takibi yapmak genellikle kayıpla sonuçlanır." / "Piyasa dengedeyken 'ping-pong' oynamalı …, dengesizlik varken ise 'sörf' yapmalı".
- D3 [M] R199: "Düşüş trendi (Lower Highs & Lower Lows) yapan bir hissede bu strateji uygulanmaz."
- D4 [T] R210: "herşey kurallara dayalı. Duyguya yer yok. Sistem ne derse o." Checklist: "Çıkışlar VIX'e göre değil, Fiyat grafiğine (BIST 100) göre yapılır. 4 indikatörden 2'sinin bozulması gerekir." Görsel R209 [G]: "BIST 100 yükselirken VIX'in düşmesi veya sakin kalması gerekir."
- D5 [T] R132 ve R198: "ortalamaların sıkışma alanları genelde patlamaya işaret eder" (R132). "Volatilite (oynaklık) ölmüştür. … Yay gerilmektedir" (R198, [M]; "Ben 5-8-13 kullandım." [T]).
- D6 [M] R138: "strateji, piyasa kan ağlarken sizi nakitte tutarak sermayenizi bir kalkan gibi korumuş." / "İşlem yapmamak da bir işlemdir".
- D7 [M] R186: "Fiyat VWAP üstünde + POC üstündeyse: Sadece alış yönlü bak. … Fiyat ikisinin arasındaysa: Çayını iç, izle."
- D8 [M] R189: "Beyaz çizgi (EMA 200) şu an tam fiyatın tepesinde bir tavan görevi görüyor. Bu ortalamanın üzerine hacimli bir yerleşme gelmeden 'kalıcı dönüş başladı' demek zor."
- D9 [G] R212: "250 günlük hareketli ortalamanın altında bir kapanış yaparsa pozisyondan çık." Kayıt metni [T]: "işleme giriş bileşenlerinizden birisi 250SMA. (bu 200SMA 200EMA 250EMA' da olabilir, stratejinize kalmış.)"

**ÇELİŞKİ (5)**
- C1 [M] R220: "Cesaret, uçlarda gezer" / "Küçük yatırımcı genelde bu %5'lik şoklarda panikleyip elindekini satar. Büyük oyuncular (Smart Money) ise bu olayları 'indirim' veya 'fırsat' olarak görür." Şokta durma yerine şokta pozisyon alma öneriyor.
- C2 [M] R226: "Bizim yaptığımız tek şey, bu üç koşulun aynı anda (confluence) gerçekleştiği o 'kırmızı ok' anında tetiği çekmekti." (düşüşte, istatistiksel bant dışında alım). R227: "Sol Üst Köşe (Düşük Fiyat + Yüksek Hacim): … güçlü bir 'Al' fırsatı olabilir." [T] "Dip yakalanmıştır."
- C3 [M] R190: "Fiyat bu uç noktalara (2. veya 3. sapma) ulaştığında, 'ortalama değerine geri dönme' (mean reversion) eğilimi gösterir." Rejim yerine ortalamaya dönüş.
- C4 [T] R156: "Mean reversion, absolute pricing oscilator kullanılarak oluşturulan bir strateji. … Buna bir de yükselen kanal desteği çizdik mi mis"
- C5 [M] R237: "Her şey genelde piyasa için kötü algılanan bir haberle başlar. … işin iç yüzünü bilenler devreye girer." Kötü haber/şok sonrası birikim anlatısı.

**Mevcut (A) maddeleri**
- Doğrulanan: "düşüş yapısında strateji uygulanmaz" (p06,107) → D3. "denge = ping-pong, dengesizlik = trend" (p02) → D2. Düşük oynaklık = kırılım habercisi (p04,36 (G)) → D5 (yalnız EMA sıkışması üzerinden).
- Bulunamayan: "Şokta yeni alım sinyalleri tamamen durdurulur" (p02): hamda yok; C1 tersini söylüyor. "Pozisyon Büyüklüğü Çarpanı Tam/Defansif" (fiyat+oynaklık birlikte artınca): hamda yok (yalnız R211 volatiliteyle ters boyut ve R183 aylık kasa oranı, ikisi de rejim çarpanı değil). "Volatilite Rejimi Theta / rehavet": hamda yok. XU100 "WMA21 altı… GEÇİŞ / CHoCH": yalnız bağlantı başlığı (R258 [B]), metin yok.

---

## İ2. Yer önce, gösterge sonra

**DESTEK (12)**
- D1 [T] R206: "Fibo 0.618 bir 'duvar' değil, sadece bir 'bölge'dir. Çok abartılmaması lazım. İşe yaramadığı zamanlar da vardır." / "Matematiksel oran (Fibo) + Piyasa Yapısı (Order Block) = Sniper Giriş."
- D2 [G] R208: "Tek Sinyale Güvenme, Kesişim Ara!" / "Fiyat kilit bir destek/direnç seviyesine gelmesiyle birlikte, birden fazla bağımsız teknik sinyalin aynı anda oluşmasıdır." (NotebookLM imzalı).
- D3 [G] R217: "Tek bir çizgiden çok daha güçlü olan bu bölgeler" / "Amaç, tek bir doğru çizgi bulmak değil, piyasanın matematiksel gridini oluşturan bu enerji kümelerini tespit etmektir." Ayrıca "Sorun metodolojinin kendinde değil, onun statik ve tek boyutlu uygulanışındadır." (p06,120 aidiyeti belirsizdi: görsel Caterpillar örneği, başka bir kaynaktan; Tansu paylaşmış.)
- D4 [T] R149: "confluence alanının gücü..." (PETKM; görsel)
- D5 [M] R197: "Sadece Fibonacci yetmez. … Order Block (Emir Bloğu) veya FVG … aranır. Fiyatın hem Fibo 0.618-0.786 arasına gelmesi hem de bu yeşil kutuya değmesi en güçlü sinyaldir." / [T] "Buyurun size canavar gibi bir strateji".
- D6 [M] R204: "Elliott ve Fibonacci 'Fiyatın nereye düşeceğini' (Seviye) söyler; FVG ise fiyatın 'Neden oraya düşmek zorunda olduğunu' (Likidite/Denge) açıklar." [T] "Hafta başında verdiğimiz listede idi. %8 getiri"
- D7 [M] R226: "Fiyat istatistiksel olarak ucuzladı. (Standart Sapma) / Küçük yatırımcı malı sattı. (Hacim/Kapitülasyon) / Balinalar malı topladı. (OBI/Derinlik)".
- D8 [M] R222: "Giriş sinyali tek bir fiyat adımı değil, XA 0.786 ile BC uzantısının kesiştiği dar bir fiyat aralığıdır."
- D9 [M] R221: "Gartley formasyonunun dönüş noktası tam olarak bu FVG kutusunun içine denk geliyor."
- D10 [M] R192: "Fiyat şu an Demand Zone (Yeşil Kutu) içinde. Yani risk almak için en uygun, stop seviyesine en yakın yer burası."
- D11 [M] R187: "Onay (Confluence): IV seviyeleri; günlük pivot noktaları veya trend çizgileri ile kesiştiğinde sinyal gücü çok daha yüksektir."
- D12 [T] R166: "Teknik analiz size 'Nereden' alınacağını söyler, temel analiz ise 'Ne' alınacağını." (yer/ne ayrımı; değerleme + teknik)

**ÇELİŞKİ (7)**
- C1 [M/T] R131: "Çok kafa bulandırmaya gerek yok, … Konu bundan ibarettir." Tek göstergeli (hareketli ortalama) yön kuralı; bölge yok.
- C2 [T] R148: "if (half_trend[t] == 'buy' and momentum[t] > momentum_threshold) Nice" (yalnız iki gösterge kapısı).
- C3 [M] R139: "Enter long: AD() Ref(Mov(AD(),opt1,E), 1) … OPT1 Current value: 3" (yalnız A/D-EMA kuralı; bölge yok. Karşılaştırma işareti yapıştırmada düşmüş.)
- C4 [M] R170: Williams %R 14 + SMA 14 pullback; bölgesiz, tamamen gösterge.
- C5 [M] R233: "Giriş: RSI (14) değeri, 30 seviyesinin altından yukarı doğru keserek bu seviyenin üzerinde bir kapanış yaptığında."
- C6 [T] R145: "İndikatör cart curt hikaye. Topsis yapın." Göstergeyi küçümsüyor, ama yer kavramına da gitmiyor.
- C7 [M] R185: "Vaktinizi indikatörlere değil, olasılık yoğunluk fonksiyonlarına harcayın." R185 ile R148/R170/R233 aynı hesapta çelişiyor.

**Mevcut (A) maddeleri**
- Doğrulanan: "Tek Sinyale Güvenme, Kesişim Ara!" (p06,112) → D2 (görsel metni birebir). "Formasyonun gücü talep toplama bölgesinde" (p04,34/40) → D8, D9 (Gartley PRZ + FVG) kısmen. Statik tek Fibonacci eleştirisi (G p06,120) → D3.
- Bulunamayan: "Sıra: bölge → kırılımlar → likidite hareketleri → 4 saatlik teyit" (p03): hamda yok; en yakın R206 (H4 order block, günlük fibo) ve R189 (4 saatlik + günlük + fibo). "ABCD'ye gözü kapalı güvenilmez; kanalı okumadan iş yapılmaz" (p04,43): hamda yok.

---

## İ3. Yapı tamamlanınca bile tepki beklenir

**DESTEK (10)**
- D1 [T] R194: "İşte bu yüzden retest beklemek önemlidir. Bakın macd yanıltmış ama hacim asla desteklememiş."
- D2 [M] R195: "Teyit (Onay) Şart: Sadece fiyat hareketi yetmez; Hacim (Volume) veya Delta'nın bu kırılımı desteklemesi gerekir." / "En temiz giriş fırsatı genellikle 'Retest' (Yeniden Test) aşamasında olur."
- D3 [M] R198: "Güvenli Giriş (Önerilen): 'Breakout' (Kırılım) Beklemek. … Alım sinyali, bu mumun kapanışıdır veya bu mumun ardından gelen küçük geri çekilmedir (Retest)."
- D4 [M] R199: "FOMO Yok: Fiyat FVG bölgesine gelmeden dönerse işlem yapılmaz. Piyasa fırsatlarla doludur, arkasından koşma." Ayrıca "Kural 6 (Aktiflik): … doldurulmamış (Fresh/Unmitigated) olmalıdır."
- D5 [M] R236: "Bu noktada oluşan bir Çekiç, Yutan Boğa veya Cımbız Dip formasyonu, 'W' formasyonunun ikinci bacağının tamamlandığını ve desteğin çalıştığını teyit eder."
- D6 [T] R214: "son gün yükselen trend desteğinden tepki almış yeşil yakmış falan filan"
- D7 [T] R241: "TC noktasında oluşan inverted hammer ise pastanın üzerindeki çilektir."
- D8 [M] R170: "Giriş: Williams %R'ın -50'den yukarı döndüğü mumun (yeşil mum) en yüksek seviyesinin üzerine çıkıldığında işleme girilir."
- D9 [G] R196: "Fiyat ve OBV Senkronizasyonu = Yüksek Güven" (NotebookLM imzalı). R195 [M]: "OBV'nin fiyatla uyumlu olup olmadığına bakın (Fiyat yükselirken OBV de yükseliyor mu?)."
- D10 [T] R238: "Geniş gövdeli mum düşük hacim, anomali / Dar gövdeli mum yüksek hacim, anomali" (hacim teyidi uyumsuzluğu uyarısı).

**ÇELİŞKİ (6)**
- C1 [M] R197: "Fiyat düzeltme yaparak 0.618 seviyesine … indiğinde ve buradaki yeşil kutu (destek alanı) ile temas ettiğinde ALIM (LONG) yönlü işlem aranır." Tetik temas; tepki şartı yok.
- C2 [M] R199: "Emir Tipi: FVG kutusunun üst bandına veya %61.8 seviyesine 'Limit Alış' emri." Önceden konan limit emir, tepkiyi beklemiyor.
- C3 [M] R241: "Fiyat, … FVG/Talep Bölgesi'ne (sarı kutu) tam olarak temas etti." / "ideal bir alım kurulumuna ulaşmıştır." (tepki yok, temas yeterli).
- C4 [M] R192: "Giriş Mantığı: 'Fiyat şu an Demand Zone (Yeşil Kutu) içinde. … '" ; "Fiyat buraya değdiğinde tepki alımı gelmesi beklenir."
- C5 [M] R198: "Agresif Giriş (Riskli): EMA'lar hala sıkışıkken, fiyat talep bölgesinin alt sınırına değdiğinde alım yapmak. … kazanç oranı (R/R) muazzamdır." (güvenli girişin yanında geçerli alternatif sayılıyor).
- C6 [M] R243: "Boşluğu Soldurma (Fading the Gap)" ve "Boşluğun Dolmasını Bekleyip Başlangıç Yönünde İşlem Yapma" iki ayrı yöntem olarak veriliyor; hangisini seçtiği yok.

**Mevcut (A) maddeleri**
- Doğrulanan: "MACD toparlanma sinyali yanıltıcı oldu; hacim hiç desteklemedi" (p06,103) → D1 (görsel de aynı kayıt). "FVG'ye gelmeden dönen fiyat kovalanmaz" (p06,107) → D4. "Fiyat ve OBV Senkronizasyonu = Yüksek Güven" (G p06,104) → D9 (görsel başlığı birebir).
- Bulunamayan: "FVG'de 1H/4H CHoCH beklemek" (p05,69): hamda yok; yalnız R206'da H4 order block geçiyor. Durum etiketleri "[AKTİF]", "TEPKI_VERDI", "BOZULDU", "[TAMAMLANDI]" (p04) ve "D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ", "RETEST VAR (6 kez)": hamda yok. En yakın etiket: R241 görsel okuması "ALKA - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 2 (Düzeltme: -39.3%)" [G]. Bu bir temas etiketi; tepki etiketi değil.

---

## İ4. Geçersizlik ve hedef merdiveni baştan yazılı

**DESTEK (11)**
- D1 [M] R199: "Stop … Yükselişin başladığı ana dibin (Point 0) hemen altı. … analiz geçersiz olur (Invalidation)." / "Hedef 1 (Güvenli): Eski Tepe Noktası (Point 1)." / "Hedef 2 … (1. Dalga Boyu x 1.618) + Düzeltmenin Bittiği Yer."
- D2 [M] R197: "Stop Loss (SL): Fibonacci 1.0 seviyesinin … hemen altına koyulur. Eğer fiyat buranın altına inerse trend bozulmuş demektir." / "Take Profit (TP): İlk hedef … Fibonacci 0.0 seviyesi … Fibonacci uzatmaları (-0.27 vb.)".
- D3 [M] R198: "Stop noktası, EMA sıkışmasının olduğu Talep Bölgesinin (Yeşil Kutu) hemen altı olmalıdır. … analiz iptal olur".
- D4 [M] R203: "TP1 (İlk Kar Al - 0.382) … pozisyonun bir kısmı (örn. yarısı) kapatılır ve Stop Loss seviyesi giriş fiyatına (Entry) çekilir." / "X Noktası Altı: En yaygın stop noktasıdır." / "1.13 veya 1.27 XA".
- D5 [M] R222: "Risk: |Giriş Fiyatı (D) - Stop Loss (X)|" / "Eğer Ödül / Risk < 1.5 ise (veya stratejinize göre 2), formasyon teknik olarak doğru olsa bile işleme girilmez".
- D6 [M] R192: "Eğer fiyat bu Yeşil Kutunun (3.50 altı gibi) altına sarkar ve orada kapanış yaparsa, bu strateji çöp olur (Stop Loss)."
- D7 [M] R184: "Giriş fiyatının 2ATR altına da acil stop konulur." Gün sonu: "Kapanış bazlıdır".
- D8 [T] R224: "Stratejide de fiyat Giriş + 1.5 ATR seviyesine ulaştığında Trailing Stop (TS) aktif hale gelir" / "önceki günün en düşüğünün altında kapanış ve %50 satış, ve emergency stop 2atr ile kalan tüm maldan çıkış."
- D9 [T] R233: "Pozisyonun %50'si satılır." (RSI 70 reddi) / "Bir önceki günün (mumun) en düşük fiyat seviyesinin (LOW) altında bir kapanış … Kalan %50'lik pozisyonun tamamı satılır".
- D10 [T] R239: "Statik iz süren stop: Hedef = Giriş + (1.5 × Giriş ATR) → Sabit kalır / Dinamik İz Süren Stop Hedef = Giriş + (1.5 × O Günün ATR) → Her gün değişir … Bu daha zekice bir trailing stop yöntemidir." / "İlk kar alma yeriniz, bu nokta geçildikten sonraki barlardan hangisi bir gün öncekinin en düşüğünün altında kapattı ise orasıdır. %50'sin satın."
- D11 [M] R170: "Stop Loss: En yakın dip (swing low) seviyesine konulur." / "Hedef: En az 1:2 Risk/Ödül oranı hedeflenir."

**ÇELİŞKİ (5)** (yapı-stopu esas hükmünü zayıflatır)
- C1 [M] R230: "Unutmayın: İşleme girerken Zarar Durdurma (Stop Loss) seviyenizi her zaman bu orana göre belirleyin." (R/R 1:2 veya 1:3'e göre stop). Mevcut (A) "Stop'u 1:2/1:3 R/R'ye göre belirle" hamda doğrulandı ve görsellerle (yapı stopu) birlikte yaşıyor.
- C2 [T] R234: "Risk/Ödül oranını en az 1:1.5 (örneğin %2 Stop, %3 Kar Al) olarak ayarlamak gerekir." Yüzde stop.
- C3 [M] R187: "Risk Yönetimi: -1SD seviyesinden işleme girildiğinde, stop seviyesi genellikle -2SD (fiyatın orada kalma olasılığı %95) altına konulur." Bant stopu.
- C4 [M] R184: "dolayısı ile hissenin mevcut fiyatından 2 adet ATR … değerini çıkararak … stop_level = data['Close'].iloc[-1] - (2 * atr.iloc[-1])" Volatilite stopu, yapıdan bağımsız.
- C5 [M] R195: "Stop-loss … ATR indikatörünü kullanın. … günün ATR'si neyse, giriş yerinizden o kadar uzağa stop koyarak".
Sonuç: hamda en az dört stop ailesi var (yapı: D1–D6, ATR: D7/C4/C5, yüzde/R:R: C1/C2, SD bantı: C3). "Yapı esas" sentezi hamla tam desteklenmiyor; ATR ve yapı yan yana.

**Mevcut (A) maddeleri**
- Doğrulanan: "TP1'de kısmi kâr + stop girişe" (p06,109/125) → D4, D8–D10. "+1,5 ATR'de iz süren stop" → D8, D10. "SL = X_Fiyat − ATR*2" (G p06,123) → D7 (ATR*2, ancak X_Fiyat= giriş: "Giriş fiyatının 2 ATR altına"). "Hedef 0.618 / 1.000 / 1.618" (G p04) → D1 (1.618), D4 (0.618 TP2).
- Bulunamayan: "Fincan-kulp hedef = kırılım + derinlik, R/R 1:2,27" (p05,58) ve "SAYAS TP2 (.618 CD)" (G): hamda ayrı görsel yok. TP2 0.618 CD mantığı R203'te var (metin). "AKFIS ENTRY, STOP, TP1–TP3": yalnız bağlantı başlığı (R253 [B]).

---

## İ5. Önce kayıp bütçesi, sonra adet

**DESTEK (10)**
- D1 [G] R212: "Toplam sermayenizin en fazla %1'ini kaybetmeyi göze alın." / "Belirlediğiniz risk tutarını, hissenin 2 ATR değerine bölün." / "100.000$ sermaye ve 14.30$ 2 ATR için: 1.000$ / 14.30$ = ~70 hisse." Kayıt [T]: "Diyelim ki sermayenizin ancak %1'ini kaybetmek riskini göze alabilirsiniz".
- D2 [M] R184: "Ne kadar hisse alacağınıza fiyatına bakarak değil, risk limitinize bakarak karar vermelisiniz." / "Formül: Göze Alınan Kayıp / Hisse Volatilitesi = Lot Sayısı / Örnek: 500 TL / 2 TL = 250 Lot."
- D3 [T] R211: "Volatilitesi yüksek olan hisselerde position sizing matematiksel olarak küçülür ve bu çok doğrudur. … Asıl amacımız sermayemizi korumak.. Oyuna dahil olmamız gerektiğinde zaten oluruz."
- D4 [M] R138: "piyasada Haklı çıkmak bir ego tatminidir, ancak sermayeyi korumak bir hayatta kalma becerisidir." / "Uzun vadede zengin eden şey büyük kârlar değil, bu tür küçük ve kontrollü kayıplardır." / "Sharpe 0.67 … 'yavaş ama kararlı' olanın yarışı kazandığını kanıtlıyor."
- D5 [M] R140: "Maksimum sermaye erimesi, bir stratejinin pratik olarak uygulanabilirliğini belirler." / "Eğer bu erimeler diğer indikatörlerin erimeleriyle karşılaştırıldığında şiddetliyse, o işlem sistemini bir kenara bırakmalı".
- D6 [T] R201: "kıyıda köşede kalmış, derinliği olmayan sitelerle veya sığ hisselerle vakit kaybetmeyin. … doğrudan ETF'lere ve likit hisselere odaklanın. … Paranızı içeride kilitlemeyin".
- D7 [M] R225: "küçük yatırımcı olarak likit olmayan hisselerde kaybedensin." / "emir defterinde sadece ilk 2-3 kademede yeterli lot var mı kontrol edin, Alış yaparken limit emir kullanın".
- D8 [M] R183: "Her ay aynı agresiflikte işlem yapılmaz." / "Nisan Ayı (Genelde Pozitif): … kasanızın %80'i ile oyuna girebilirsiniz. Ağustos Ayı …: kasanızın sadece %30'u ile işlem yapıp". (Tansu mu yazdı, belirsiz.)
- D9 [M] R184: "kaybettiğinizde hayat kalitenizi bozmayacak, uykularınızı kaçırmayacak bir sermaye ile yola çıkmaktır."
- D10 [M] R229: "Her rotasyon hamlesine sıkı bir Zarar Kes (Stop-Loss) kriteri koymak. Bu, stratejinin batmasını önler".

**ÇELİŞKİ (4)**
- C1 [M] R220: "En büyük karlar Fat Tails alanında yapılır." / "Cesaret, uçlarda gezer".
- C2 [M] R185: "Piyasanın rastlantısal olmayan (non-random) bileşenlerini ayıklayabilir, … bu uç senaryoları nasıl kâra dönüştüreceğinizi öğretir." (uçları kâra çevirme).
- C3 [M/T] R137 ve R138: R137 "hedef, 'en çok kazandıran' hisseyi değil, … Maximum Sharpe Ratio kombinasyonunu bulmak" [T/M]; R138 "geceleri huzurlu uyumanızı sağlayan şey Sharpe değil, kümülatif getiri grafiğindeki o sakinliktir". Sharpe hem hedef hem küçümseniyor.
- C4 [T] R181: "161.700 kombinasyon yaptıktan sonra sevgili algo matematiksel olarak optimal 3 hisselik portföyü verecek" (büyük arama; aşırı uyum riski, huzurlu eğri ilkesi ile doğrudan çelişmez ama sınırlı sınama).
Not: R184 formül belirsiz. "Volatilite/2 ATR" ve "500/2=250" ifadesi stop mesafesinin 1 ATR mi 2 ATR mı olduğunu açıkça vermiyor; R212 görseli "risk / 2 ATR" diyor, R184 örneği "volatilitesi/2 ATR değeri 2 TL" diyor. Kodlamada R212 esas alınabilir.

**Mevcut (A) maddeleri**
- Doğrulanan: "Piyasada haklı çıkmak ego tatmini…" (p05,75) → D4 (birebir). "Daha düşük getiri karşılığında daha düşük oynaklık ve düşüş tablosu" (p05,59) → D4 (R138: %19.1 vs %10.8, drawdown -%10/-%15). "Nakitte beklemek disiplindir" (p05,52) → R138. "Oynaklığı yüksek hissede büyüklük küçülür" (p02) → D3. "Likit olmayan hisseden uzak durulur" (p02) → D6, D7. (G) "%1 kayıp bütçesi, lot = risk / 2 ATR; gün içi acil stop" (p06,115) → D1, R184.
- Bulunamayan: yok.

---

## İ6. Kural koda dökülür, sistem ellenmez, sonuç ölçülür, başarısızlık da gösterilir

**DESTEK (10)**
- D1 [M] R171: "Eğer testler stratejinin başarısız olduğunu söylüyorsa, o 'popüler' kurala yatırım yapmaktan vazgeçmenizi sağlar." / "'Acaba çalışır mı?' diye kumar oynamak yerine, 'Veriler ne diyor?' sorusuna yanıt".
- D2 [T] R210: "herşey kurallara dayalı. Duyguya yer yok. Sistem ne derse o."
- D3 [M] R218: "komisyon oranlarını ve kayma maliyetlerini (slippage) hesaba katarak milimetrik olarak" / "bot sizin disiplininizle çalışır, duygusuzca alım-satım yapar ve stop-loss seviyelerinize sadık kalır. Psikoloji, küçük yatırımcının en büyük düşmanıdır".
- D4 [M/T] R157: "İşlem maliyetleri, piyasa likiditesi ve kayma (slippage) gibi gerçek dünya unsurlarını yüksek sadakatle simüle etmelidir." Son cümle [T]: "iki satır kod yazayım ya da yazdırayım sevdası kısa vadede karlı gibi görünsede orta ve uzun vadede yıkıma sebep olabilir."
- D5 [M] R140: "Yüzdelik doğruluk … acemi yatırımcıların bir takıntısıdır ancak bir işlem sistemini değerlendirmek için çok önemli bir kriter değildir." / "toplam net kârın maksimum sermaye erimesine oranı" / "Kümülatif Sermaye grafiği" / "Basit tut". (Kaynak belirsiz: "Dursun bir kenarda lazim olur", büyük olasılıkla aktarma.)
- D6 [T] R138: "EMA değeri walk forward le optimzie edilerek model oluşturulmuştur." (walk-forward) / "Strateji %19.1 getiri sağlarken, piyasada kalan kişi sadece %10.8 kazanabilmiş."
- D7 [T] R152: "2023 yıl sonunda sanırım froto gerçek maliyet ve kapanış değeri tam olarak 747 TL idi. Bu basit değerleme de 796tl hedef fiyat vermiş 2023 senesi başında." R150: "Tutarlılığını kontrol etmek için xxcelde eski yaptığım değerlemeleri koda döküyorum." R153: "doğruluğunu kontrol etmek için daha önceki excel çalışmalarından alınarak yapıldığı için eski tarihlidir."
- D8 [T] R234: "Doğruluk (Accuracy) : %55.00 Kesinlik (Precision) : %55.31 Duyarlılık (Recall) : %45.44 / Finansal piyasalarda %70 gibi bir değer yakalarsanız bu harika bir sonuçtur. %90'lar ise mümkün değildir." Zayıf sonucu açık gösteriyor.
- D9 [M] R228: "Cointegration olmadan açılan işlemlerde büyük zararlar yazıp ta ne yapacağız diyen çok insan gördüm." (test edilmemiş istatistiksel arbitraj uyarısı). Metin [T] ("Derslerde öğrencilerin yaptığı…").
- D10 [G] R215: "Plana Sadık Kalmamak" / "'Zarar Durdur' Emri Kullanmamak" (NotebookLM imzasız; dış üretim olabilir).

**ÇELİŞKİ (6)**
- C1 [T] R170: "Bi bakın bakalım backtesti nasıl" (testi okura bırakıyor; sonuç yok).
- C2 [T] R156: "Şunu can sıkıntısından yazdım, grafiği düzenlemedim bile, ama çalışıyor:)" (kanıt yok).
- C3 [T] R197: "Buyurun size canavar gibi bir strateji / Artık taramasını yaparsınız" ve R186 "Python kodu ile taraması da yazılır." Kural yayımlanıyor, ölçüm yok.
- C4 [T/M] R174: "Modern Yaklaşım ise … tüm olası parametre kombinasyonlarını test etmek ve en düşük hata oranını bulmak. Ben doğrusu bunu kullanıyorum..." ve R185: "Çoğu geliştirici, ömrünü klasik indikatörlerin … parametrelerini optimize ederek harcar. Ancak bu, doğru yapılmaz ise, … geçmiş verinin gürültüsünü … mükemmelleştirmeye çalışmaktan başka bir şey değildir." Optimizasyon hem yapılıyor hem uyarılıyor ("sistem ellenmez" ile gerilim).
- C5 [T] R234: "Bu model üzerinde hiç çalışmadığım henüz yazdığım bir algoritma." (ve "Makine öğrenmesi modellerini aslında hisse senedi işlemlerinde kullanmayı pek sevmem").
- C6 [T] R152 ve R150: doğrulama tek örnekle ("FROTO … sanırım 747 TL"; "2023 yılında ARCLK hissesinin bu değerlere ulaştığını"). Seçilmiş olumlu örnek.

**Mevcut (A) maddeleri**
- Doğrulanan: "Win rate tek başına ölçüt değil; net kâr + en büyük düşüş + sermaye eğrisi" (p02) → D5. "Katkısı gösterilmeyen filtreleri koruma" (p03): ters yönde kanıt; hamda katkı ölçümü yok (C1–C3, C6).
- Bulunamayan: "sadece sistem çalışıyor, hiç ellemiyorsun" (p05,55): hamda birebir yok (D2 yakın). "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım" (p05,53): hamda yok; yakın R228 (kointegrasyon şart). Açık soru "Retest beklemek yarar sağlıyor mu?" için hamda cevap bir örnekle (R194, n=1); ölçüm yok. (G) "BACKTEST SONUÇLARI (SMRTG)", "T+1 Open İşlemler", "Max Drawdown −27.44%": hamda yok. (G) "Fiyat-ortalaması yöntemi (ESKİ / script'teki)": hamda yok.

---

## İ7. Medyan, uç değer temizliği

**DESTEK (4)**
- D1 [T] R244: "Medyanı şöyle bir kanal gibi kullanın arkadaşlar. Biraz üzerinde düşünelim." Görsel okuması [G]: "sarı noktalı üst bant çizgisi, yeşil kesik orta/alt bant çizgileri ve aralarında koyu yeşil dolgulu kanal".
- D2 [M] R185: "Piyasalar nadiren 'Normal Dağılım' gösterir. … Kurtosis (Basıklık) ve Skewness (Çarpıklık) gibi kavramlarla tanışırsınız."
- D3 [M] R232: "BIST100'ün işlem hacmi ortalamasını baz alırsanız THY, ASELSAN, ISCTR gibi devasa hacimli hisseler ortalamayı o kadar yukarı çeker ki, aslında çok sağlıklı olan ama … 'hacimsiz' sanıp elersiniz." / "Yöntem B (Dinamik): … hacimde en altta kalan %25'i (çöp olanları) at." / "bir sığ hissenin %10 yapıp endeksi bozması".
- D4 [T] R202: "Rolling alpha Rolling skewness. Bunları anlamaya çalışın. Momentum listelerimize uyguluyoruz."

**ÇELİŞKİ (5)**
- C1 [M] R187: "Olasılıklar: Fiyatın %68.2'si 1SD, %95.4'ü 2SD ve %99'u 3SD bantları içinde gerçekleşir." (normal dağılım varsayımı) ve R185/R220 (fat tail) ile aynı hesapta çelişir.
- C2 [M] R190: "Fiyat hareketlerinin yaklaşık %68'i 1. Standart Sapma içinde gerçekleşir; burası 'Değer Bölgesi'dir."
- C3 [M] R232: "Adım 2 (Rolling Mean / Hareketli Ortalama): … Son 20 günün (1 ay) veya 60 günün (3 ay) hacim ortalamasını alın." Aynı kayıtta ortalama öneriliyor, medyan yok.
- C4 [M] R144: "Tarihsel Ortalamalar: Şirket son 36 çeyrekte … hangi PD/DD bandında fiyatlanmış?" / "Sektör Ortalaması: Sektörün 2.5 olduğu yerde 1.0 olan bir hisse 'görece' ucuzdur." Çıpa ortalama; medyan yok.
- C5 [M] R226: "Fiyat, standart sapmasından o kadar uzaklaştı ki, matematiksel olarak 'geri dönmek zorunda' olduğu bir noktaya gerildi."

**Mevcut (A) maddeleri**
- Doğrulanan: yalnız (X) "Medyan temelli çalışın" aralığında yok (R001'de; bu kapsamda yok). R244 medyan kanalını gösteriyor (yeni destek, ek kanıt).
- Bulunamayan: "|30g getiri| > %50 → ANOMALİ, ortalamadan çıkarıldı" (G p04,07): hamda yok. "Değerlemede IQR k=1,5" (G p04,27): hamda yok. R238'deki "anomali" mum gövdesi/hacim uyumsuzluğudur, getiri aykırı değeri değil.

---

## İ8. Akış: tarama, harita, kesişim, tepki, yönetim; her formasyona ayrı tarayıcı

**DESTEK (9)**
- D1 [T] R189: "Hisselerin analizini böyle yapıyorum grupta. Ama tüm hisseler önce momentum sistemimden geçiyor sonra ayrıntılı yazıyorum." (p06,99 birebir doğrulandı).
- D2 [T] R137: "Bu sistem satılık değil arkadaşlar" / "1. Aşama: Momentum ve Sinyal Yakalama → 2. Aşama: Pozitif Eğim … → 3. Aşama: Teknik Onay → 4. Aşama: Markowitz → 5. Aşama: Maksimum Sharpe Seçimi" / "kimler koşmaya hazır, hangileri doğru yöne bakıyor, diye eliyoruz ve son aşamada bu atletlerden en dengeli takımı nasıl kurarım".
- D3 [T] R158: "Radara giren, sinyal üreten hisselerin tüm değerlemeleri yapılacak ve temel analiz sonuçlar detaylı üretilecek."
- D4 [T] R166: "Değerleme %50 potansiyel diyorsa, Teknik 'Şimdi al' dediğinde sistem alarm verecek."
- D5 [T] R192: "#python ile yeni tarama kodumuz … Price Action … ve Smart Money Concepts … bölgelerini bize getiriyor."
- D6 [T] R221 ve R222: "algoritmik taramalarımızda teknik yapısıyla dikkat çeken ve dönüş sinyalleri üreten MAKIM" (R221); "bu çalışma, manuel çizimden ziyade, bir Trading Sistemi veya Algoritmik Tarama mantığıyla hazırlanmıştır" (R222).
- D7 [M] R232: "Sektörleri kendiniz belirleyin. … 80'e yakın sektör … Yoksa … hacim tuzağına düşersiniz." (sektör → hacim eşiği sıralaması).
- D8 [M] R218: "Python, binlerce hisseyi saniyeler içinde tarayıp, sadece sizin belirlediğiniz çok katmanlı kriterlere (örneğin: hem RSI değeri düşük, hem F/K oranı ucuz, hem de hacmi artan) uyanları önünüze getirerek".
- D9 [T] R151 ve R158: "İNA'sonucunun %40'ı, basit çarpan değerlemesi ve detaylı çarpan değerlemesinin ortalamasının %60'ı alınarak sapmalar minimize edilir." (R151); "İndirgenmiş nakit akışı yöntemlerinin üçünün ortalaması toplam ağırlığın yüzde kırkını oluşturacak. … çarpanlar analizinin ortalaması ise yüzde altmışı." (R158).

**ÇELİŞKİ (3)**
- C1 [T] R143: "Aşağıdaki kodu kullan geliştir formasyonları tanımla vs vs" (OHLC mum geometrisi tek motor; ayrı tarayıcı ilkesine ters).
- C2 [T] R240: "gerçi bistte artık bir önemi yok. sırtlanların kol gezdiği bir cambazhaneden farksız." (temel analiz değerlendirme listesi için); oysa R158/R166/R151 akışa temel analiz ve değerleme koyuyor.
- C3 [T] R234: "Makine öğrenmesi modellerini aslında hisse senedi işlemlerinde kullanmayı pek sevmem ama temel modelim de bir makine öğrenmesi algoritmasına dayanıyor:)" (R137'de "yapay sinir ağları ile oluşturduğum bir momentum stratejim var").

**Mevcut (A) maddeleri**
- Doğrulanan: "önce kendi momentum sisteminden geçiriyor, sonra seçilenleri ayrıntılı yazıyor" (p06,99) → D1 (birebir).
- Bulunamayan: "Gartley ve Butterfly'ı tek motorda birleştirmek yerine ayrı tarayıcı" (p01): hamda yok; formasyona özgü stop var (R203 "Crab, Shark gibi") ama ayrı tarayıcı iddiası yok. (G) "sektör liderleri 30/60/90 gün": hamda yok; R232 20/60 gün hacim ortalaması var (başka şey). (G) "Araç çıktıları hep aynı biçimde": R241 [G] başlık biçimi ("ALKA - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 2 …") tek örnek.

---

## YENİ İLKE adayları (İ1–İ8'de olmayan, en az 2 kayıtta)

**Y1. Değerleme ayrı bir ayak: çok yöntem, çapraz kontrol, güvenlik marjı, otomatik hesap ve manuel geçersiz kılma**
Kayıtlar: R144, R147, R150, R151, R152, R153, R154, R155, R158, R159, R163, R166.
- R158: "Üç yöntemin birbirine bu kadar yakın çıkması tesadüf değil, aslında güven veren bir işaret." [T]
- R155: "DCF bir hedef fiyat üretme makinesi değil, varsayımlarınızı ve piyasanın beklentilerini test ettiğiniz matematiksel bir stres çarkıdır." / "mutlaka ciddi bir güvenlik marjı (örneğin %20 ile %30 arası) talep edin." [T/M]
- R163: "Eğer FCFE değeri, DDM değerinden çok yüksekse: Şirket nakit üretiyor ama bunu hissedarıyla paylaşmıyor". [M]
- R150: "Yıllık net kar ve tahmini favök kod tarafından hesaplanabileceği gibi şirketin verileri ile de hareket edebilmek tutarlılık açısıdnan önemli olabilir. O nedenle koda manuel giriş seçeneği de koydum." [T] R151: "Burada kodumuz bunu kendisi de hesaplıyor, fakat manuel giriş seçeneği de yazdım." [T]
- R147: "Net kar, havadan gelen bir rakam değildir; cironun bir türevidir." / "Modeller, sığ ve yanıltıcı olabilen salt enflasyonist ciro büyümelerini baz almak yerine, doğrudan şirketin faaliyet hacmine (adet/ton) inen 'aşağıdan yukarıya' (bottom-up)". [T/M]
- R144: "Sadece 'PD/DD oranı 1'in altında, o halde bu hisse bedava' diyerek alım yapmak büyük bir hatadır." [M]
Not: bu ilke teknik kurulum ilkelerinin dışında kalıyor. Kör nokta: R240'ta [T] temel analiz için "bistte artık bir önemi yok", yani değerleme akışına katkısı Tansu'nun kendi sözüyle tartışmalı.

**Y2. Göreli konum: mutlak değere değil, kendi geçmişine ve sektörüne göre "neredeyiz"**
Kayıtlar: R144, R183, R202, R227, R229, R232.
- R227: "Dinamik Aralık (Dynamic Range): Hissenin şu anki fiyatının ve hacminin son 1 yıla (252 işlem günü) göre nerede olduğunu yüzdesel olarak hesaplar." / "Bizim Kodumuz: Son 1 yıla (252 gün) göre 'neredeyiz' diye bakar." [T]
- R144: "36 çeyreklik (uzun dönem) ortalamayı bir 'çıpa' noktası olarak alıp" [M]
- R229: "Göreceli Güç Filtresi: Sektörün genel piyasaya göre … yeni yeni ayrışmaya başladığı anı yakalamak." [T/M]
- R232: "Elmayla armudu kıyaslamayın." / "Anlık hacme bakılmaz, 'karakteristik' hacme bakılır." [T/M]
- R183: "Hangi aylarda %70 ve üzeri ihtimalle yükseldiğine bakın" [M]
- R202: "Rolling alpha Rolling skewness." [T]

**Y3. Akıllı para izi: fiyat ile hacim/derinlik uyumsuzluğu, birikim ve dağıtım evreleri**
Kayıtlar: R198, R226, R227, R235, R237, R238, R186, R221.
- R226: "Fiyat hareket etmese bile, tahtanın derinliğinde 'Alıcılar' (Bid side), 'Satıcıları' (Ask side) agresif bir şekilde domine etmiş." [M]
- R237: "Eğer herkes korkup kaçarsa kime satacaklar? O yüzden korkuyu, sadece senin elindeki hisseyi sattırmaya yetecek seviyede, dozunda tutarlar." [T/M]
- R238: "Sizin paranızı istiyorlar Dikkatli olun / Geniş gövdeli mum düşük hacim, anomali" [T]
- R227: "Durum A (Yükseliş Yorgunluğu): Fiyat tepede … Hacim çizgisi dipte" [T/M]
- R235 [G]: kitap şeması "Birikim Süreci", "Dağıtım Süreci", "Alım Tepesi", "Satış Tepesi".
- R198: "Bu bölge genellikle 'Akümülasyon' (Toplama) evresidir." [M]
Not: R227'de yazar kendisi veri sınırını belirtiyor: "yfinance ve standart borsa verilerinde kimin ne kadar mal taşıdığı veya kaç kişinin pozisyon açtığı (trader count) bilgisi bulunmaz. Bu nedenle, bu stratejiyi yfinance ile kodlarken kavramsal bir yaklaşım (Proxy) kullanacağız." Yani "akıllı para" kanıtı proxy.

**Y4. Çok kriterli sıralama ve portföy optimizasyonu (seçimi sezgiyle değil, matematiksel motorla yap)**
Kayıtlar: R137, R145, R175, R178, R179, R181, R182.
- R145: "Topsis analizinin deneysel sonuçları inanılmaz." [T]
- R179: "birçok farklı ve bazen birbiriyle çelişen veriyi … tek bir rasyonel puana indirgeyebilmesidir." / "Yakında projeye başlıyorum." [T/M]
- R182: "Neden Monte Carlo Yerine 'Spicy' Model? … Bu yaklaşım ise piyasadaki gürültüyü (noise) filtreler" [T/M] (Monte Carlo reddi; deterministik Markowitz)
- R175/R178: "Sektör rotasyonu Convex Hull ile VZA analizini birlikte çalışırsanız muazzam sonuçlar elde edersiniz." [T]
- R181: "161.700 kombinasyon yaptıktan sonra sevgili algo matematiksel olarak optimal 3 hisselik portföyü verecek" [T]
Not: R185'te Monte Carlo risk of ruin için öneriliyor; R182 Monte Carlo'yu seçim için reddediyor (rol ayrımı).

**Y5. Asimetri ve konvekslik: kayıp sınırlı, kazanç açık**
Kayıtlar: R185, R220, R229, R260 (başlık yalnız).
- R229: "Asimetrik Getiri: Seçilen sektörün, piyasa beklentileri doğru çıktığında sağlayacağı getirinin, yanlış çıktığında yaşanacak kayıptan kat kat fazla olması." [T/M]
- R220: "Piyasada zamanın %95'inde işler normal gider … servet transferi, o geriye kalan %5'lik uç olaylarda gerçekleşir." [M]
- R185: "tekil işlemlerin sonucuna değil, bir işlem dizisinin Beklenen Değerine (E) odaklanırsınız" [M]
Çelişki notu: İ1 ve İ5 (şokta küçül/dur) ile gerilimli (bkz. İ1-C1).

**Y6. Tahmin etme, tepe/dip kahramanlığı yapma; ama dip arama da var (çelişkili aday)**
Kayıtlar (destek): R172, R185, R199, R226. Kayıtlar (ters): R227, R229, R237.
- R172: "Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR." [M/T]
- R185: "Finansal piyasalarda algoritma geliştirenlerin düştüğü en büyük tuzak, fiyatın gelecekteki yönünü 'tahmin etmeye' çalışmaktır." [M]
- R226: "Sistem burada bir 'tahmin' yapmadı." [M]
- Ters: R227 [T] "Ok ile ilaretlenen sağdaki benim grafiğim soldaki ise hissenin grafiği. Dip yakalanmıştır." R229: "Dip Yakınlığı: Hareketin başlangıcını yakalamak için geç kalınmamış olması." R237 birikim anlatısı.
Karar için: ilke olarak yazılırsa "dip yakalamayı hedefleme" ve "dip adayı taramaları" birlikte açıklanmalı.

Tek kayıtta kalan, aday sayılmayan fikirler: aylık mevsimsellik ve kasa oranı (R183), kointegrasyon şartı (R228, R262 yalnız başlık), VIX-BIST kontrol listesi (R209–R210), ML ile %55 doğruluk (R234), Pine Script yerine Python (R218), makro yayınları izleme (R231; R229'da yan söz).

---

## Somut kurallar ve parametreler

| parametre | değer | alıntı | R### |
| --- | --- | --- | --- |
| Trend yönü filtresi | fiyat hareketli ortalamanın üstü = alış, altı = satış | "piyasa hareketli ortalamanın altındaysa, bu durum satış yönlü" | R131 |
| EMA sıkışma kümesi | EMA 5-8-13 | "Ben 5-8-13 kullandım." | R198 |
| Boğa dizilimi | ema5>ema8>ema13 | "ema5>ema8>ema13 de oluşmuş" | R214 |
| A/D-EMA modeli | EMA periyodu opt1 = 3, walk-forward ile optimize | "OPT1 Current value: 3 Çatır çutur girip çıkmak için, 1-2 gün" / "EMA değeri walk forward le optimzie edilerek" | R139, R138 |
| A/D-EMA sonuç | strateji %19.1, B&H %10.8, Sharpe 0.67, düşüş -%10 ile -%15 bandı | "Strateji %19.1 getiri sağlarken, piyasada kalan kişi sadece %10.8" | R138 |
| Williams %R swing | 30 dk, %R 14, SMA 14, aşırı alım -20..0, aşırı satım -80..-100, geri dönüş -50 | "Zaman Dilimi: 30 Dakika / Williams %R: 14 periyotluk." | R170 |
| Williams %R hedef | en az 1:2 R/R, stop swing low | "Hedef: En az 1:2 Risk/Ödül oranı hedeflenir." | R170 |
| RSI girişi | RSI(14) 30 üstüne kapanış | "RSI (14) değeri, 30 seviyesinin altından yukarı doğru keserek" | R233 |
| RSI çıkış 1 | RSI 70 üstünden altına kapanış: %50 sat | "Pozisyonun %50'si satılır." | R233 |
| RSI çıkış 2 | önceki gün düşüğü altına kapanış: kalan %50 | "Bir önceki günün (mumun) en düşük fiyat seviyesinin (LOW) altında bir kapanış" | R233 |
| İz süren stop aktivasyon | Giriş + 1.5 ATR | "fiyat Giriş + 1.5 ATR seviyesine ulaştığında Trailing Stop (TS) aktif hale gelir" | R224 |
| İz süren stop türleri | statik (giriş ATR) / dinamik (o günün ATR) | "Dinamik İz Süren Stop Hedef = Giriş + (1.5 × O Günün ATR) → Her gün değişir" | R239 |
| İlk kâr alma | %10 (kullanıcı belirler) ve %50 | "kar alma %10 (sizin belirleyeceğiniz)" | R224 |
| Acil stop | giriş - 2 ATR; gün içi anında çık | "Giriş fiyatının 2ATR altına da acil stop konulur." | R184 |
| Gün sonu stop | kapanış bazlı; SMA250 örneği | "Gün Sonu Stop: Kapanış bazlıdır" / "250 günlük hareketli ortalamanın altında bir kapanış yaparsa pozisyondan çık." | R184, R212 (G) |
| Risk bütçesi | sermayenin %1'i | "sermayenizin ancak %1'ini kaybetmek riskini göze alabilirsiniz" | R212 |
| Lot formülü | risk / 2 ATR | "Belirlediğiniz risk tutarını, hissenin 2 ATR değerine bölün." | R212 (G) |
| Lot örneği (TL) | 500 TL / 2 TL = 250 lot | "Örnek: 500 TL / 2 TL = 250 Lot." | R184 |
| Aylık kasa oranı | %80 iyi ay, %30 zayıf ay | "kasanızın %80'i ile oyuna girebilirsiniz" / "kasanızın sadece %30'u ile" | R183 |
| Mevsimsellik eşiği | %70 üstü yükselen aylar, 10-20 yıl | "Hangi aylarda %70 ve üzeri ihtimalle yükseldiğine bakın" | R183 |
| Elliott W2 geri çekilme | min 0.50, ideal 0.618-0.65, max 0.786 | "İdeal (Golden Pocket): %61.8 - %65 Arası / Maksimum: %78.6" | R199 |
| W1 itki koşulu | en az %10 | "en az %10'luk bir marj içermeli" | R199 |
| W3 hedefi | (W1 boyu x 1.618) + düzeltme sonu | "(1. Dalga Boyu x 1.618) + Düzeltmenin Bittiği Yer." | R199 |
| W4 geri çekilme | W3'ün 0.24, 0.38 veya 0.50'si | "4. Dalga Düşüşü = 3. Dalga Yükselişi X (0.24 veya 0.38 veya 0.50)" | R205 |
| Fibonacci golden zone | 0.618-0.786 (OTE), 0.5 altı = discount; SL 1.0 altı; TP 0.0, -0.27 | "Stratejinin asıl odaklandığı yer 0.618 (Altın Oran) ile 0.786 arasındaki bölgedir." | R197 |
| Harmonik TP | TP1 0.382, TP2 0.618, TP3 C noktası, TP4 1.272/1.618 | "TP1 (İlk Kar Al - 0.382): Formül: D + ((C - D) * 0.382)" | R203 |
| Harmonik stop | X altı; derin formasyonda 1.13/1.27 XA | "1.13 veya 1.27 XA" | R203 |
| Gartley | AB=0.618 XA; BC 0.382-0.886 AB; CD=0.786 XA ve BC 1.272/1.618 | "XA bacağının %78.6 (0.786) geri çekilme seviyesinde sonlanmalıdır" | R222 |
| Gartley tolerans | %3-%5 | "mutlaka bir %3-%5 tolerans (sapma payı) tanımlamanızı öneririm." | R222 |
| Giriş R/R eşiği | 1.5 (veya 2) altı: girme | "Eğer Ödül / Risk < 1.5 ise (veya stratejinize göre 2)" | R222 |
| R/R başka kaynaklar | 1:2-1:3; 1:1.5 (%2 stop, %3 kâr) | "1 kaybetme riskine karşılık 2 veya 3 kazanma hedefi" / "en az 1:1.5 (örneğin %2 Stop, %3 Kar Al)" | R230, R234 |
| SD bantları | 1SD %68.2, 2SD %95.4, 3SD %99; alım -1SD, stop -2SD altı | "stop seviyesi genellikle -2SD … altına konulur" | R187 |
| Değer bölgesi | işlemlerin %68'i; açılış değer bölgesi dışında = dengesizlik | "işlemlerin %68'inin gerçekleştiği alan" | R190 |
| Hacim eşiği | 20 veya 60 gün ortalama; 10 Milyon TL; alttan %25 at | "20 günlük ortalama hacmi 10 Milyon TL altındaki hisseleri listeme sokma." | R232 |
| Emir defteri kontrolü | ilk 2-3 kademede yeterli lot; limit emir | "emir defterinde … sadece ilk 2-3 kademede yeterli lot var mı kontrol edin" | R225 |
| VIX-BIST çıkış | 4 göstergeden 2'si bozulunca çık (SMA20 altı, Heikin Ashi kırmızı) | "4 indikatörden 2'sinin bozulması gerekir." | R210 |
| VIX-BIST giriş | fiyat > SMA20 ve SMA50, AO yeşil, RSI > MAV; VIX < hızlı bant, VIX RSI < SMA10 | "Checklist: Fiyat > Ortalamalar + AO = Yeşil + RSI > MAV" / "VIX < Hızlı Bantlar & VIX RSI < MAV" | R210 |
| Korelasyon | negatif aranır | "Negatif korelasyon arıyoruz. Eğer negatif değilse aşırı dikkat." | R210 |
| Yedi gösterge raporu | skor 4/5, ADX 22.9, RSI 68.1, korelasyon -0.60, VIX 13.47 | "Genel Yükseliş Skoru: 4/5" / "Nihai Karar: DİKKATLİ İYİMSERLİK" | R188 (G) |
| Konum penceresi | 252 işlem günü | "son 1 yıla (252 işlem günü)" | R227 |
| Momentum skoru | ln(fiyat) regresyon eğimi, yıllıklandırma 252, x R² | "return annualized * (rvalue ** 2)" | R176 |
| Değerleme ağırlığı | DCF üçlüsü %40, çarpanlar %60 | "İNA'sonucunun %40'ı, … ortalamasının %60'ı alınarak" | R151, R158 |
| Basit F/K örneği | büyüme %100, net marj %10, F/K 4.33x | "satışlarının %100 büyüyeceği, net kar marjının %10 olacağı" / "(4.33x) FK çarpanını" | R151 |
| Adet bazlı örnek | F/K 10.00x; FAVÖK marjı %6.0; FD/FAVÖK 16.00x | "F/K çarpanı (10.00x) ile" / "%6.0 FAVÖK Marjı" / "16.00x" | R147 |
| DCF süresi / WACC | EREGL 10 yıl; WACC 19.1; FCFF/FCFE/DDM 5 yıl | "DCF de WACC 19.1 kullanılmıştır." / "Beş yıl boyunca büyüyen nakit akışlarını" | R153, R158 |
| DCF güvenlik marjı | %20-%30 | "(örneğin %20 ile %30 arası)" | R155 |
| Uç değer payı | %60-%80, g'de %0.5 oynama | "bugünkü değerinin %60 ile %80'i, … 'Uç Değer'den gelir" | R155 |
| PD/DD çıpa | 36 çeyrek ortalama; sektör 2.5 vs 1.0 | "son 36 çeyrekte" | R144 |
| ML kabul eşiği | doğruluk %55 (R/R 1:1.5 şartıyla); %70 harika; %90 mümkün değil | "Doğruluk (Accuracy) : %55.00" | R234 |
| Portföy araması | 161.700 üçlü kombinasyon | "161.700 kombinasyon" | R181 |
| Skewness penceresi | 63 gün | (yalnız başlık) "CWENE — 63 Günlük Skewness" | R260 [B] |

---

## Tansu'nun reddettikleri ve uyardıkları

Reddedilen:
- Tepe/dip avı: "ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR." (R172).
- Kazanma oranı takıntısı: "acemi yatırımcıların bir takıntısıdır" (R140).
- Tek bir sinyal: "Tek Sinyale Güvenme, Kesişim Ara!" (R208 [G]).
- Fibonacci'yi duvar saymak: "Fibo 0.618 bir 'duvar' değil, sadece bir 'bölge'dir." (R206).
- Göstergeye odaklı geliştirme: "Vaktinizi indikatörlere değil, olasılık yoğunluk fonksiyonlarına harcayın." (R185); "İndikatör cart curt hikaye." (R145).
- Monte Carlo ile portföy seçimi: "Neden Monte Carlo Yerine 'Spicy' Model?" (R182).
- Korelasyon = arbitraj: "Korelasyonun yüksek olması, istatistiksel arbitraj yapabileceğiniz anlamına gelmez." / "Cointegration (Eşbütünleşme) şarttır, şarttır. şarttır." (R228).
- Değer tuzağı: "PD/DD oranı 1'in altında, o halde bu hisse bedava" demek "büyük bir hatadır" (R144).
- Geçmişi çarpanla çarpmak ve sabit büyüme: "geçmiş net karı çarpanla çarpma hatası" (R147); "geçmiş yılın tam kapanış verilerinin üzerine sabit bir büyüme oranı eklemek veya geçen yılın kar marjlarını doğrudan kopyalamak gibi pratik ama tehlikeli yollar" (R150).
- DCF tek sonuca inanmak: "tek bir 'gerçek değere' körü körüne inanmak yerine" (R155).
- BIST100 hacim ortalaması: "Hayır. Eğer BIST100 ortalamasını referans alırsanız, analizinizi daha başlamadan çöpe atarsınız." (R232).
- Sığ hisse: "sığ hisselerle vakit kaybetmeyin" (R201); "Emir defteri çok dengesiz görünen hisselerde işlem yapmayın" (R225).
- Piyasa emri: "piyasa emriyle girdiğinizde sığ derinlik nedeniyle çok yüksek fiyattan alabilirsiniz" (R225).
- Hızlı kod: "iki satır kod yazayım ya da yazdırayım sevdası … yıkıma sebep olabilir." (R157).
- Platform bağımlılığı: "Pine Script ile 'ev sahibi' TradingView'dir; siz ise kuralları başkası tarafından belirlenmiş bir odada oyun oynayan misafirsinizdir." (R218).
- Tek boyutlu RSI: "RSI: Sadece Fiyata bakar. Hacmi bilmez." (R227).
- Makine öğrenmesi: "kullanmayı pek sevmem" (R234); yüksek doğruluk iddiası: "%90'lar ise mümkün değildir." (R234).
- Denge günü trend takibi ve dengesizlikte ters işlem: "Denge günlerinde trend takibi yapmak genellikle kayıpla sonuçlanır." / "aralığın tersine işlem açmak (fading) son derece risklidir." (R190).
- FOMO: "arkasından koşma." (R199).
- Tek aralıklı statik Fibonacci: "Sorun metodolojinin kendinde değil, onun statik ve tek boyutlu uygulanışındadır." (R217 [G]).
- Hacimsiz geniş mum: "Geniş gövdeli mum düşük hacim, anomali" (R238).
- Excel hata riski: "Excel'de bir hücreyi yanlış kaydırmak tüm analizi çökertebilir." (R159 [M]).

Uyarılar:
- "Haber Akışı: Bilanço veya kritik haber öncesi oluşan teknik yapılar risk barındırır, temkinli olunmalıdır." (R199 [M])
- "Tamamen eğitim amaçlıdır, hisse döner dönemz bilemem önemli olan kavramlara yatkınlığınızı arttırmak." (R221 [T])
- "Pine kullanıcıları lütfen linç yapmayın. Fikirlerimi beyan ettim." (R218 [T]).

---

## Kör noktalar: hamın desteklediği / çürüttüğü

1. **"Kanıtların çoğu seçilmiş olumlu örnek; tek hisse, kısa dönem, masrafsız."**
   - Hamın desteği: R152 ("sanırım froto … 747 TL idi … 796tl hedef fiyat"), R150 ("2023 yılında ARCLK hissesinin bu değerlere ulaştığını ve sonra fiyatın geri geldiğini göreceksiniz."), R193 ("Gerçekleşmiş bir hikayeye bakalım"), R204 ("%8 getiri"), R227 ("Dip yakalanmıştır."). Hepsi tek örnek, anlatı biçimi. R138 getiri karşılaştırmasında maliyet geçmiyor.
   - Hamın kısmi çürütmesi: R234 zayıf ML sonucunu kendisi veriyor (%55); R138 "0.67 Sharpe oranı çok iddialı görünmeyebilir"; R194 başarısız teyit örneği (retest/MACD); R157 ve R218 maliyet ve slippage simülasyonu gerektiğini yazıyor (ilke var, ölçüm yok).
2. **"Açık sorusunu kendisi soruyor (retest yarar sağlıyor mu?) ama cevabı yok."**
   - Hamda tek cevap anekdot: R194 "İşte bu yüzden retest beklemek önemlidir." (n=1). R170 testi okura bırakıyor ("Bi bakın bakalım backtesti nasıl"). Tutulan ölçüm yok. Destekleniyor.
3. **"'Bağımsız kanıt' dediği göstergelerin çoğu aynı fiyat serisinden türüyor."**
   - Destek: R208 [G] örnek listesi "RSI Uyumsuzluğu, Fibonacci Geri Çekilme Seviyeleri, Trend Çizgileri, Mum Formasyonları" hepsi fiyat türevi, ama metin "birden fazla bağımsız teknik sinyal" diyor. R158 "Birbirinden tamamen bağımsız mantıksal yollar" dediği FCFF/FCFE/DDM aynı büyüme varsayımlarından beslenir (R158'in kendi cümlesi; ortak girdi tespiti bizim yorumumuz, hamda yazılı değil).
   - Kısmi çürütme: R226 hacim ve emir defteri dengesizliği (OBI) fiyat dışı veri; R227 ise bu verinin gerçek halinin ellerinde olmadığını itiraf ediyor ("bu ver'ler şu anda elimizde yok") ve proxy kullanıyor.
4. **"Bazı parametreleri bilerek saklıyor; eşikleri tecrübeyle seçiyor."**
   - Destek: R137 "Sistem nasıl işliyor stratejiyi anlatmadan biraz işleyişi anlatayım"; R147 "xxxx adetlik satış tahmini"; R202 "Ne olduğunu anlatacağım." (ertelenmiş); R198 "(örneğin EMA 20, 50, 100) … Ben 5-8-13 kullandım."; R212 "stratejinize kalmış".
   - Çürütme: R197, R199, R203, R222 açık parametre veriyor (fibo oranları, tolerans, R/R). Yani teknik kurulum parametreleri açık, sinyal sistemi (momentum/yapay sinir ağı) kapalı.
5. **"Ortalamaya dönüşü 'zorunlu' gibi anlatıyor; şişman kuyruk ile çelişiyor."**
   - Destek: R226 "matematiksel olarak 'geri dönmek zorunda' olduğu bir noktaya gerildi"; R187 normal dağılım bantları; R190 "mean reversion". Aynı hesapta R185 ve R220 şişman kuyruk. Destekleniyor (iç çelişki).
6. **Yeni kör nokta: metnin yazarı belirsiz.** Hamda uzun metinler (R138, R190, R192, R195, R197, R199, R210) açıklayıcı model çıktısı gibi okunuyor ("Sizin grafiğiniz", "Grafik (Panel 2)"). Bu metinlerden çıkan "Tansu ilkesi", Tansu'nun sözü olmayabilir. Çıkarılırken [T] işaretli satırlar öncelikli olmalı.
7. **Yeni kör nokta: kısa pozisyon kuralları.** R131 ("satış yönlü"), R170 ("Satış (Short) Koşulları"), R186 ("Buraları 'short' (satış) fırsatı olarak gör"), R243 (short FVG fading) BIST'te açığa satış olmayan bir hesapta anlatılıyor; taslaktaki "BIST'te açığa satış yok" notu (Sisteme etkisi 5) hamla çelişmiyor ama kısa yönlü kurallar yalnız çıkış/uyarı olarak kullanılmalı.
8. **Yeni kör nokta: Tansu'nun kendi tutarsızlıkları.** R234 "Makine öğrenmesi … pek sevmem" ve R137/R166 yapay sinir ağı; R240 "bistte artık bir önemi yok" ve R158/R166 yoğun değerleme; R185 indikatör optimizasyonu eleştirisi ve R174/R138 optimizasyon kullanımı.
9. **Yeni kör nokta: veri.** R245–R263 (19 kayıt) yalnız bağlantı; "kaynak notu" başlıkları Levent'in/otomasyonun, Tansu'nun değil. Bu kayıtlar kanıt sayılmamalı. Metinlerine ulaşılırsa İ3, İ4, İ6 için en yararlı olanlar: R255 (backtest/giriş sadeliği), R253 (AKFIS FVG retest), R257/R258 (XU100 rejim).
