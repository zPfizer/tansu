## Ne okudum

İlk dosyanın ilk satırı:

```text
# Tansu'dan ayrılan noktalar ve YORUM'lar (10.10, Codex 6.1-Sol okuyucu)
```

**İstenen 81 satırı denetledim. 10 satırın sınıfı değişmeli:** 1, 11, 18, 22, 28, 29, 46, 48, 56, 95.

TASARIM, KURALLAR ve A–E’deki atıfları; 49 havuz notunun ilgili metinlerini ve 61 görseli açtım. Ham metin ile yapay zekâ sentezini ayırdım. Hiçbir dosyayı değiştirmedim.

Kısaltmalar: **T, K, A–E** ilk tablodaki dosyalardır. **G65:21**, `gorsel-paket-65-…md` dosyasının 21. satırıdır; **G65/g1**, o notun ilk görselidir. **Rota**, `kaynak-vakbn-garan-rotasyon-2096358189696520213.md`; **XU**, `kaynak-xu100-bekle-teyit-2095196517577461974.md`. `tweet-…` adları havuzdaki `.md` dosyalarıdır.

Kaynak türleri:

- **Aktarım:** Tansu’nun sözü olarak Ham bölümüne aktarılmış metin; ikinci el.
- **Metin:** X’ten birebir alındığı kaynak kaydında belirtilen metin.
- **Araç:** Havuzda Tansu’ya atfedilen grafik veya araç çıktısı.
- **Eğitim:** Paylaşılan şema/tablo; Tansu’nun kendi üretimi olduğu doğrulanmamış.
- **NotebookLM:** Görselde filigranı görülen infografik.

## Doğrulama

**TANSU’YA ÇEVİR**, yalnız gerekçede belirtilen somut kısım içindir. Aynı satırdaki açıklanmamış ayrıntılar kendiliğinden kaynak kuralı olmaz.

| # | Nokta | Verilen sınıf | Doğru sınıf | Neden (kaynak yeriyle) |
|---|---|---|---|---|
| 1 | Aynı sektör zorunluluğu | TANSU’YA ÇEVİR | **BELİRSİZ** | **Aktarım, G54:21:** farklı sektör mümkün; aynı sektör yasak değil. Anlatılan yöntem long/short. Buradan T:384,403’teki rotasyon filtresini zorunlu kaldırma sonucu çıkmaz. |
| 2 | Sıkışma sonrası giriş | SESSİZ | SESSİZ | **Aktarım + araç, G65:21, g1:** ön sinyal sıkışma içinde; ayrıntıları okura bırakıyor. K:103’teki tetik kendi seçimimiz olarak kalabilir. |
| 3 | Sıkışma sayıları | SESSİZ | SESSİZ | **Aktarım + araç, G67:21, g1; G65:21:** rasyo seçimi okura bırakılmış. %1,2 ve üç gün örnekte var; zorunlu genel değer değiller. |
| 4 | Açılış yerine AOF | UYGULANAMAZ | UYGULANAMAZ | **Araç, Rota/g2, işlem paneli:** açıkça T+1 Open. T:163’te tanımlanan kaynakta açılış yok. AOF aynı dolum değildir. Bu kanıt çift örneğine aittir. |
| 5 | Gün sonu stopunun dolumu | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22; NotebookLM, G115/g1:** kapanış koşulu var; gerçekleşme fiyatı ve seansı yok. T:342’nin ertesi AOF’u kaynak kuralı sayılamaz. |
| 6 | Kartı pozisyona bağlama | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Araç, G02/g1:** Durum, Reaksiyon, Giriş ve Stop ayrı alanlar. Alan ayrımı somut. T:816’daki pozisyon etiketleri harmonik durum diye sunulmamalı; EMA’ya D tamamlanması eklenmemeli. |
| 7 | Likidite ölçüsü | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-sektor-rotasyonu-hacim-tuzagi-sabit-tl-esigi:32–49; tweet-medyan-temelli-finansal-indikatorler:23:** sektör taraması ile genel gösterge önerisi farklı. T:261,331 için tek zorunlu ölçü çıkmıyor. |
| 8 | Likidite kapasitesi | SESSİZ | SESSİZ | **Aktarım, tweet-likit-hisseler-etf-islem-derinligi-slippage-kapasite:21:** likit hisse öneriyor; %2, on gün veya kalan miktarı almama kuralı vermiyor. |
| 9 | Likidite eleği yüzdesi | SESSİZ | SESSİZ | **Aktarım, tweet-sektor-rotasyonu-hacim-tuzagi-sabit-tl-esigi:45–51:** eşik seçimi açıkça okura ait. Ancak sektör içindeki sıralama ile T:261’deki genel evren sıralaması aynı uygulama değil. |
| 10 | Sabit parametre / walk-forward | SESSİZ | SESSİZ | **Aktarım, G75:43,49:** walk-forward A/D örneğine ait. İki ilk aileye zorunlu aktarım yok; T:561 için bu kaynakla değişiklik istenemez. |
| 11 | Şok filtresinin yokluğu | TANSU’YA ÇEVİR | **BELİRSİZ** | **Aktarım, tweet-volatilite-piyasa-soku-yeni-alim-freni:21:** şokta yeni alımı durdurmak açık. Ancak şokun hesaplanabilir tanımı yok: **fikir var, kural yok**. T:85 için eksiksiz kapı çıkmıyor. |
| 12 | Şok hesabının ayrıntıları | SESSİZ | SESSİZ | **Aynı aktarım:21:** karşılaştırma fikri var; standart sapma, 21 işlem günü, X, eşik ve bekleme süresi yok. SESSİZ yalnız bu ayrıntılar için geçerli. |
| 13 | ATR14 ve Wilder | SESSİZ | SESSİZ | **Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22; NotebookLM, G115/g1:** ATR var; 14, Wilder ve başlangıç hesabı yok. T:343’ün YORUM etiketi doğru. |
| 14 | Lotu aşağı yuvarlama | SESSİZ | SESSİZ | **NotebookLM, G115/g1, örnek hesap:** yaklaşık 70 hisse yazıyor. Aşağı/yukarı yuvarlama talimatı yok. |
| 15 | Beta için log fiyat OLS | SESSİZ | SESSİZ | **Araç, Rota/g1–g2:** Beta ve Rolling Beta var; hesap yok. T:407’deki yöntem kaynak formülü olarak doğrulanamaz. |
| 16 | Stop adları | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22:** “Acil Stop” ve “Gün Sonu Stop” açıkça kullanılmış. Adlar somut; mevcut terimler korunur, atıf düzeltilir. |
| 17 | Harmonik D’nin rolü | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-iskpl-abcd-cden-dye-backtest:23; araç, G02/g1:** C→D’de D satış hedefi; dönüş işleminde D giriş/tamamlanma bölgesi. Faz ayrımı somut. |
| 18 | İlk sinyale kadar nakit | TANSU’YA ÇEVİR | **BELİRSİZ** | **Araç, Rota/g2:** başlangıçtaki yatay eğri nakitle uyumlu; nakit politikasını açıklamıyor. Isınma/işleme başlama koşulu da olabilir. T:372 genel kaynak kuralı diye doğrulanamaz. |
| 19 | SMA çıkışına “bozulma” denmesi | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-abcd-geometrik-gecerlilik-kurallari:21; G13:21:** bozulma belirli yapının geçersizliğidir. T:817’de SMA çıkışı, karantina ve iptali aynı kaynak anlamında birleştirmek yanlış. |
| 20 | Z formülü ve pencere | SESSİZ | SESSİZ | **Araç, Rota/g1–g2:** Z değerleri var; formül, pencere ve ddof yok. K:88–89’un kaynakla aynı Z’yi ürettiği söylenemez. |
| 21 | Bir günlük ΔZ yeterliliği | SESSİZ | SESSİZ | **Araç, Rota/g1; aktarım, tweet-stat-arb-momentum-donus-teyidi-kar-carpani:21:** dönüş fikri ve tek günlük değişim görülüyor; tek günün yeterli olacağı açıklanmıyor. |
| 22 | Yalnız yıllık çift kontrolü | TANSU’YA ÇEVİR | **BELİRSİZ** | **Aktarım, tweet-rolling-cointegration-iliski-bozulma-kapisi:21:** kayan izleme öneriliyor. Pencere, sıklık, eşik ve bozulunca yapılacak işlem yok: **fikir var, kural yok**. |
| 23 | Eşbütünleşme seçim ayrıntıları | SESSİZ | SESSİZ | **Metin, kaynak-kointegrasyon-sinirlari-2093658795700338821:48; araç, Rota:** test ailesi öneriliyor; T:385–409’daki 252 gün, AIC, sıralama ve roller verilmemiş. |
| 24 | Pair Health/Quality kapıları | BELİRSİZ | BELİRSİZ | **Araç, Rota/g1:** p=0,048, Quality=55,6 ve GÜÇLÜ görünüyor. Bunlardan eşik veya işlem engelleme mantığı çıkarılamaz; D:59–78’deki tahminler kanıt değil. |
| 25 | Çift sayısı ve paylar | SESSİZ | SESSİZ | **Araç, Rota/g1–g2:** tek çift var. Beş pay, sektör başına iki çift ve yeniden dengeleme politikası yok. |
| 26 | Pozisyon ve toplam risk sınırları | SESSİZ | SESSİZ | **Aktarım, G115:20; tweet-algoritma-tasarimi-temelleri-trading-sistemleri:21:** risk/limit fikri var. %10 tavan ve on pozisyon verilmemiş; %1 de örnek olarak anlatılıyor. |
| 27 | Ham/düzeltilmiş fiyat | BELİRSİZ | BELİRSİZ | **Araç, Rota/g2:** ipucu kutusunda fiyat var; genel düzeltme politikası yok. T:206’nın bütün Tansu sistemlerine genellenmesi bu görselle kanıtlanmaz. |
| 28 | SMA250 seçimi ve giriş filtresi | SESSİZ | **BELİRSİZ** | **Aktarım, G115:20; NotebookLM, g1:** ortalama seçimi okura bırakılmıştır. Ancak T:285’teki kesin giriş karşılaştırması verilmemiştir. Satır iki ayrı iddiayı birleştiriyor; seçim kısmı SESSİZ kalır. |
| 29 | Piyasa durumunun yalnız bilgi olması | TANSU’YA ÇEVİR | **BELİRSİZ** | **Metin, XU:35–47:** belirli tarihe ve seviyelere ait teyit önerisi. Her güne uygulanacak seviye/kalıcılık hesabı yok: **fikir var, kural yok**. SMA50 yerine doğrudan yeni kapı çıkarılamaz. |
| 30 | BIST/VIX listesini aynen uygulama | UYGULANAMAZ | UYGULANAMAZ | **Aktarım + araç, G114:23–68, g1:** HA ve başka seriler gerekiyor. T:169’daki yalnız endeks kapanışıyla birebir uygulanamaz. Ayrıca çıkış mantığı da belirsiz. |
| 31 | Üç mum FVG tanımı | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, G107:47–48:** `high[t−2] < low[t]` karşılığı açık. Bu alt kural kodlanabilir; A:25 ve C:543’te yalnız Claude önerisi sayılması yanlış. |
| 33 | AKFIS stop/TP piksel okuması | BELİRSİZ | BELİRSİZ | **Araç, AKFIS `01-akfis-retest-teyit.png`:** çizgiler var; formül ve temas/kapanış koşulu yok. A:35’teki stop altı kapanış kaynak kuralı değildir. |
| 34 | Trend çizgisi yöntemi | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21–27:** pivotları ikili bağlama ve arada delinmeme açık. Yöntem tercihi somut; pivot tespiti ve kanal üretiminin bütün ayrıntıları hâlâ açık. |
| 36 | Lookback anlamı | BELİRSİZ | BELİRSİZ | **Araç, G34/g1 ve G45/g1:** 20/30 etiketleri var, açıklama yok. A:79’daki iki olasılıktan biri kesinleştirilemez. |
| 37 | Trend kırılımının fiyat alanı | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21:** kapanışla aşma açık ve kodlanabilir. Bu, bütün başka kırılım türlerinin aynı koşulu kullandığını kanıtlamaz. |
| 40 | Touch anlamı | BELİRSİZ | BELİRSİZ | **Araç, G10/g1 ve G12/g1, alt tablolar:** Touch sütunları var; mum, ayrı ziyaret veya temas sayımının tanımı yok. |
| 41 | Teyit anlamı | BELİRSİZ | BELİRSİZ | **Araç, G13/g1, alt tablo:** tarih sütunu var; oluşum tarihi olduğu açıklanmıyor. A:144’ün eşitlemesi doğrulanamıyor. |
| 42 | Talepte distal/proximal | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Eğitim, G15/g1:** giriş/proximal ve distal/stop ilişkisi çizilmiş. Yalnız simetri icadı değil. Ancak base veya leg-out seçiminin tek evrensel formülü verilmemiş. |
| 44 | Demand bozulmasında kapanış/fitil | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, G13:21:** ilk `Close < zone_low` açık; Low daha katı seçenek diye ayrılmış. Ana tarif kodlanabilir; aracın fiilen hangi seçeneği kullandığı ayrıca doğrulanmış değil. |
| 46 | Golden Zone giriş ve ileri hedef | TANSU’YA ÇEVİR | **BELİRSİZ** | **Aktarım, G105:48–55:** temas bölgesinde işlem arama var; kesin tetik/emir yok: **fikir var, kural yok**. −0,27 ise açık bir hedef örneği; A:199’daki “oran yok” yanlış. |
| 47 | GEDZA EMA adları | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Araç, G93/g1, sol üst lejant:** EMA3 ve EMA13 yazıyor. A:211,213’te EMA5’i EMA3 yapma düzeltmesi kesin. |
| 48 | AKSGY destek altı çıkış | TANSU’YA ÇEVİR | **BELİRSİZ** | **Aktarım, G103:21 ve trend çizgisi notu:21:** retest/hacim ve kapanışla çizgi kırılması var; AKSGY pozisyonunu kapatma talimatı yok. Çıkış için **fikir var, kural yok**. |
| 55 | Mavi seri ve çarpan | BELİRSİZ | BELİRSİZ | **Araç, G48/g1:** birlikte hareket gözleniyor; tek neden veya tam koşul kanıtlanmıyor. E:191’deki gözlem üretim kuralına dönüştürülemez. |
| 56 | Tam/Defansif sayıları | TANSU’YA ÇEVİR | **BELİRSİZ** | **Aktarım, G48:21:** bu olayda pozisyonu kapattığını söylüyor. Bütün Defansif durumların 0, bütün Tam durumların 1 olduğu açıklanmıyor. Olay somut, genel çarpan kuralı yok. |
| 57 | Swing=15 / MinGap=15 | BELİRSİZ | BELİRSİZ | **Araç, G60/g1, üst etiket:** sayılar ve sol-only var. Eşitlik, pivot yenileme ve seçim algoritması yok; B:173 tam kaynak algoritması değildir. |
| 60 | A/D işlem operatörleri | BELİRSİZ | BELİRSİZ | **Aktarım, G75:41,49:** `AD > EMA` yönü var; dört işlem satırında operatörler eksik. Gecikme/kesişim koşulları tamamlanamıyor. |
| 70 | Bollinger sapma fikri | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-bollinger-kuyruklari-ortalama-donus-var:25–29:** ±2 standart sapma somut. B:406’daki “k yok” yanlış. −2SE/−3SE ifadesi aynı formüle sessizce çevrilemez; tam giriş kuralı yok. |
| 73 | Formasyon durumları | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Araç, G02/g1 ve G03/g1:** durum ve tepki ayrımı somut. `TEPKİ_VERDİ`, G02’de Reaksiyon sütununda; tek durum zinciri gibi sunulmamalı. Eşikler verilmemiş. |
| 75 | A ihlalinin fiyat alanı | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-abcd-geometrik-gecerlilik-kurallari:21:** A’yı geçme var; Close/High/Low seçimi yok. |
| 76 | AB=CD işlem stopu | BELİRSİZ | BELİRSİZ | **Araç, G03/g2; aynı aktarım:21:** stop/bozulma sonuçları ve geometrik ihlal var. Stop fiyatının A olduğu açıklanmıyor. |
| 78 | C→D işleminin alış yönü | UYGULANAMAZ | UYGULANAMAZ | **Araç, G03/g1; aktarım, tweet-iskpl-abcd-cden-dye-backtest:23:** sınıf yalnız aşağı yönlü SMRTG C→D işlemi için doğru. ISKPL metni açıkça C’den alımı anlatıyor; bütün AB=CD ailesi uygulanamaz değildir. |
| 79 | Gartley D yönü | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Eğitim, G123/g1; araç, SAYAS görseli:** %78,6 geri çekilme SAYAS’ta A’dan aşağı ölçülmüş. `D=A−0,786(A−X)` somut; C:256 zaten bunu yapıyor. |
| 81 | Gartley toleransı | BELİRSİZ | BELİRSİZ | **Aktarım, G123:49; araç, G122/g1:** %3–5 var, birimi yok. MAKIM bacaklarından genel tarayıcı toleransı çıkarılamaz; C:282’deki yaklaşık %10 kanıt değildir. |
| 82 | Gartley stop seçenekleri | BELİRSİZ | BELİRSİZ | **Eğitim, G123/g1; araç, G02/g1:** tablo X/XA1,13/X−2ATR içeriyor; LUKSK Stop(X) gösteriyor. Genel seçim kuralı yok. |
| 83 | Gartley TP1 | BELİRSİZ | BELİRSİZ | **Eğitim, G123/g1; araç, SAYAS görseli:** tabloda AD×0,382; SAYAS lejantında 1:1 R/R. İki ayrı uygulama; tek genel TP1 doğrulanmıyor. |
| 84 | Gartley X altı geçersizlik | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, G109:54–56:** X altı geçersizlik fikri açık; Gartley için somut. Bütün bullish harmoniklere genellenemez; aynı metin derin formasyonlarda X altı alternatiflerini ayırıyor. |
| 85 | Kelebek B oranı ve stop | BELİRSİZ | BELİRSİZ | **Araç, DOAS `01-doas-kelebek.png`; G01/g6:** B konumları farklı; DOAS’ta 1,618 “max risk” etiketi var. Tolerans ve emir stopu açıklanmıyor. |
| 88 | 10 gün / 20 bar | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-gartley-d-tepki-penceresi-10-gun:21; araç, KAPLM üst notu:** tweet D’den itibaren on gün diyor. Görselde ayrıca 20 bar ve “son 10 gün” var. Birim ve ortak politika belirsiz. |
| 90 | BALAT TP2’de AD/CD | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, G109:35; araç, g1:** `D+0,618(C−D)` açık; çizili seviyelerle uyumlu. C:393’te AD yerine CD yazılması kesin. |
| 92 | Trident D formülü | BELİRSİZ | BELİRSİZ | **Aktarım, G47:20; araç, g1:** metin `B×C/A`, görsel `CD=1,27AB`. Ayrıca Ham satırının sonunda başka kişinin teşekkür/yanıt metni karışmış; tamamı Tansu sözü sayılamaz. |
| 95 | Kümülatif delta yerine proxy | UYGULANAMAZ | **BELİRSİZ** | **Araç, G45/g1, alt panel:** Kümülatif Delta yazıyor; hesabı yok. Gerçek işlem deltası günlük veriden çıkmaz, fakat Tansu’nun panelinin zaten proxy olmadığı kanıtlanmış değil. |
| 96 | “Taze” FVG | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, G107:48–50:** üç mum boşluğu ve daha önce doldurulmamış olma şartı kaynakta açık. C:543,559’un kaynak yok iddiası yanlış; kısmi/tam dolum sınırı hâlâ belirsiz. |
| 98 | Dalga 4 oranları | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-elliott-wave4-wave3-retracement-024-038-050:27:** 0,24/0,38/0,50 açık ve kodlanabilir. C:577’deki 0,236/0,382 başka seçimdir. |
| 100 | Fibonacci gün sayımı | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **NotebookLM, G111/g1, sağ alt:** hafta sonu/tatil dahil takvim günü açık. C:604,612 zaten doğru; yeni davranış değişikliği değil. Tolerans verilmemiş. |
| 105 | Çekirdek ağırlık sınırı | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading:21:** açıkça %50’den fazla. D:138,140’ta `≥` yerine `>` somut düzeltmedir; SLSQP kaynaktan gelmiyor. |
| 107 | Scorecard’dan %70 maruziyet | BELİRSİZ | BELİRSİZ | **Araç, G59/g1:** maruziyet sütunu yok. Volatilite oranından pozisyon oranı belirlenemez; D:131 bir açıklama adayıdır. |
| 108 | VIX kimliği | BELİRSİZ | BELİRSİZ | **Araç, G114/g1 ve G50/g1:** VIX ve BIST_VOL adları var; ticker/kaynak/formül yok. D:148’in CBOE eşlemesi bu görsellerle kesinleşmez. |
| 111 | Nabız RSI ve sıfır hacim | BELİRSİZ | BELİRSİZ | **NotebookLM, G98/g1:** RSI kendi ortalamasıyla anlatılmış; 50/60 eşiği yok. Hacim 0 gösteriliyor ama nedeninin veri hatası olduğu açıklanmıyor. |
| 112 | VIX çıkış mantığı | BELİRSİZ | BELİRSİZ | **Aktarım, G114:54,68; NotebookLM, G113/g1:** 2/4, fiyat/HA çıkışı ve fiyat+VIX alarmı ayrışıyor. Alarmı kesin çıkışla birleştirmek doğru değil. |
| 114 | NH–NL 83 puanı | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-endeks-5of5-nhnl-corwin-schultz-likidite:30–36:** 83 puan var; ölçek ve evren yok. D:226’daki ham fark formülü kaynak hesabı diye doğrulanamaz. |
| 115 | Sektör ortalaması | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Araç, G07/g1:** “hisse bazlı basit ortalama” açık. Yeniden üretimde aritmetik ortalama somut; D:260 zaten bunu söylüyor. Medyan ayrı öneridir. |
| 118 | ATR’nin sabit kalması | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22:** giriş−2ATR ile güncel Close−2ATR birlikte var. Başlangıç stopu/güncelleme ayrılmadan E:77 doğrulanamaz. |
| 120 | Chandelier tipi trailing | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20:** giriş+1,5ATR ve sonraki dip-altı kapanış açık. E:126–128’deki High−kATR/max zinciri bu kaynakta yok; kaynak anlatımı somut biçimde değişmeli. |
| 122 | Önceki dip satışının zamanı | TANSU’YA ÇEVİR | TANSU’YA ÇEVİR | **Aynı aktarım:20:** aktivasyon geçildikten sonraki barlardan ilk uygun kapanış diyor. Bu sıra kodlanabilir; her gün koşulsuz satış değildir. |
| 124 | %50’nin paydası ve TP2 | BELİRSİZ | BELİRSİZ | **Aktarım, G125:20:** önceki kısmi satışlar ve ardından %50 var. İlk miktarın mı kalan miktarın mı yarısı olduğu açık değil; ikinci satış ayrıntısı da yok. |
| 126 | Trailing/kısmi kârı erteleme | BELİRSİZ | BELİRSİZ | **Aktarım, G125:20 ve ATR notu:22:** çıkış fikirleri var. Her iki ilk ailede zorunlu ortak paket oldukları açıklanmıyor; T:93’ün kaldırılması zorunlu sonuç değil. |
| 129 | Şok freni / uçlarda fırsat | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-fat-tail-firsat-survival-konvekslik:21 ve şok notu:21:** açık bir mantıksal çelişki kanıtlanmış değil. Fırsat anlatısı işlem tetiği vermez; şok frenine istisna oluşturmaz. |
| 130 | Önce teknik stop / R:R | BELİRSİZ | BELİRSİZ | **Aktarım, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:48–49; G123:42–49:** farklı bağlamlar. Gartley’de X stopu ve R:R ret kuralı açık; bunu bütün sistemlere genelleme kaynakta yok. |
| 135 | Her sistemde stop | BELİRSİZ | BELİRSİZ | **Aktarım, G125:20; araç, Rota/g2; eğitim, G118/g1:** risk ilkesi ile rotasyonun çıkışı ayrılmalı. Grafikte stop görünmemesi, stop bulunmadığını kanıtlamaz; T:346 kesin kaynak hükmü değildir. |
| 148 | Araç ve formül kimliği | BELİRSİZ | BELİRSİZ | **Araç, G01–G02; aktarım, G02:27; eğitim, G120/g1–g4:** isimler ve ekranlar var. Üretici, sıra numarasının anlamı ve bütün iç yöntemler doğrulanmış değil. |
| 149 | Örnek seçiminin amacı | BELİRSİZ | BELİRSİZ | **Aktarım, ISKPL notu:23, G107:41–43, G59:20; ilgili araç görselleri:** örnekler var, seçim gerekçeleri yok. Yüksek getiriden seçme/kısa dönem/varyant açıklamaları kanıtlanmamış. |

## İlk sürümü değiştirecek kesin noktalar

**Kesin düzeltmeler kaynak atfı, kart anlamı ve dolum ayrımıdır. Yeni şok, piyasa teyidi veya çift sağlığı kapısının tam kuralı bu kaynaklardan çıkmıyor.**

1. **Kartta formasyon ile pozisyonu ayır — #6, #19.**  
   T:73’teki sistem karşılığı şu olmalı:

   > İlk sürüm kartı pozisyon durumunu gösterir. Tansu’nun harmonik formasyon durumunu ve reaksiyonunu yeniden üretmez.

   T:812’de `Durum` → `Pozisyon durumu`. T:816–818’de SMA250 çıkışı `GÜN SONU STOPU`, karantina `KARANTİNA ÇIKIŞI`, iptal `GİRİŞ İPTAL` olarak ayrı anlatılmalı; hepsi `BOZULDU` altında toplanmamalı. Bunlar önerilen uygulama adlarıdır, Tansu’dan alınmış etiketler değildir.

2. **AOF farkını açık yaz — #4, #5.**  
   K:112 ve T:284,413 için kesin ayrım:

   > VAKBN–GARAN kaynak paneli T+1 açılış işlemi gösterir. Mevcut veri açılış içermediğinden sınama ertesi gün AOF kullanır; bu, kaynak dolumunun yaklaşık modelidir.

   T:342’ye:

   > SMA250 altı kapanış çıkış koşuludur. Ertesi gün AOF’unda dolum, projenin varsayımıdır; kaynak dolum zamanını açıklamaz.

3. **Risk paketinin kaynağını ve seçimlerini ayır — #13, #14, #16, #26, #28.**  
   T:340 ve K:114 çevresindeki atıf şu ayrımı taşımalı:

   > Acil stop ve gün sonu stopu adları aktarılan Tansu metninde vardır. %1 risk ve SMA250 çıkışı paylaşılan NotebookLM örneğinde gösterilir. Ortalama seçimi okura bırakılmıştır. ATR14/Wilder, lot yuvarlama ve %10 pozisyon tavanı kaynakta verilmez.

   SMA250’nin **kesin giriş filtresi** olarak Tansu’ya atfı kaldırılmalı; giriş koşulu #28’deki açık noktadır.

4. **Çiftte gözlem ile genel kuralı ayır — #1, #18, #135.**  
   T:384,403’te aynı sektörün Tansu zorunluluğu olduğu söylenmemeli. K:92 ve T:372,346 için kaynak sınırı açık olmalı:

   > İlk sinyale kadar nakit ve ayrı stop kullanmama, mevcut rotasyon modelinin kurallarıdır. Kaynak grafik bunların genel politika olduğunu açıklamaz.

   Bu inceleme, sektör filtresinin kaldırılmasını veya yeni bir stop eklenmesini kesinleştirmiyor.

## Boşluklar

1. **Fikirden tam kurala geçilemeyenler:** #11 şok tanımı, #22 kayan çift sağlığı ve #29 piyasa teyidi. Eşik, zamanlama ve eylem tamamlanmadan kod değişikliği çıkarılamaz.
2. **İlk ailelerde açık kalanlar:** Z/β hesabı, Pair Health kapıları, SMA giriş koşulu, stop güncellemesi ve dolum zamanı. Görselde sonuç bulunması algoritmayı açıklamıyor.
3. **Karışık satırlar bölünmeli:** Özellikle #28, #46, #56 ve #96; bilinen fikir/değer ile bilinmeyen uygulama ayrıntısı aynı sınıfa sıkıştırılmış.
4. **Kaynak atfı güçlendirilmeli:** Ham’a aktarılmış söz, Tansu’nun araç çıktısı, eğitim şeması ve NotebookLM aynı kanıt türü değil. G47’de başka kişinin yanıtı da ham metne karışmış.
5. **Örnekten genelleme sınırı:** İlk sinyale kadar nakit, Defansif=0, gerçek delta kullanımı, tolerans ve stopsuz rotasyon; mevcut görseller bunları genel kural olarak kanıtlamıyor.