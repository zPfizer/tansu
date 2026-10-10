# E. Risk, çıkış ve süreç kuralları (Tansu kaynaklı)

Hazırlanma: 2026-10-05. Yalnız okuma araştırması. Hiçbir parametre uydurulmadı. Boşluklar YORUM etiketiyle işaretli.

## 0. Nasıl okunur

Kaynak kökü: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`. Görseller `assets\<klasör>\` altında. Kısaltma: G = gorsel-paket, T = tweet-, K = kaynak-.

Kaynak türleri:

| Etiket | Anlam |
|---|---|
| BİRİNCİ EL | Görseli ben açıp okudum: Tansu aracının çıktısı, grafik etiketi, tablo, kod. |
| BİRİNCİ EL (infografik) | NotebookLM infografiği. Tansu paylaştı. Tansu'nun kendi aracı değil. Metni yapay zekâ özeti. |
| İKİNCİ EL | Yalnız not (*.md) içinde var. Notlar çoğunlukla Claude yazımı. "Levent ... belirtti" cümleleri aktarılan tweet metninin özetidir. |
| YORUM | Tansu söylemedi. Ben veya notlardaki Claude önerdi. |

Uyarı 1: Notlarda "Levent" sözcüğü aktarılan tweet metnini anlatan kişiyi gösterir. Çoğu notta tweet URL'si yok. Yazarın Tansu olduğu havuz bağlamından gelir. Havuz ana notu "Levent'in X paylaşımlarından derlediği" der. Yani yazar atfı çoğu not için doğrulanmış değil. Tek istisna: `not-backtest-giris-sadeligi-risk-islem-gunlugu.md` (URL: x.com/The_Tansu_/status/2095213493133713664, 2 Eylül 2026) ve K-akfis (3 Eylül 2026).

Uyarı 2: `T-atr-risk-butcesi-position-sizing-stop-loss` için `assets` klasörü yok. Yalnız metin ve bir Python satırı var. Hepsi İKİNCİ EL.

Uyarı 3: Notlardaki "Cevo katkısı", "Cevo düzeltmesi", test fixture, state machine ve "kanonik" bölümleri Tansu'ya ait değil. Bunları Tansu ifadesi olarak kullanma.

Uyarı 4: `TANSU\GLOSSARY.md` stop = giriş − 2 ATR, hedef = giriş + 4 ATR, bozulma = kapanış EMA50 altı der. Bu kaynaklarda "4 ATR hedef" ve "EMA50" yok. Tansu'nun 2 ATR stopu var. 4 ATR hedef ve EMA50 bizim kararımız (YORUM). Aşağıda tekrar belirtilir.

---

# BÖLÜM 1. Pozisyon büyüklüğü ve stoplar

## K1. Risk bütçesi ve lot hesabı (%1 / 2 ATR)

- Kaynak: G-115 (`assets/gorsel-paket-115-position-sizing-1pct-2atr-sma250/01-position-sizing-yuzde1-2atr-sma250-stop.jpg`), T-atr-risk-butcesi (not), T-volatilite-ters-orantili (not).
- Tansu'nun ifadesi:
  - Görsel, verbatim (BİRİNCİ EL infografik): "Risk Tutarınızı Belirleyin: Toplam sermayenizin en fazla %1'ini kaybetmeyi göze alın." "Hisse Adedini Hesaplayın: Belirlediğiniz risk tutarını, hissenin 2 ATR (Ortalama Gerçek Aralık) değerine bölün." "Örnek Hesaplama: 100.000$ sermaye ve 14.30$ 2 ATR için: 1.000$ / 14.30$ = ~70 hisse."
  - G-115 notu (İKİNCİ EL, paraphrase): SMA250 yerine SMA200, EMA200 veya EMA250 seçilebilir. İşlemde kaç lot alınacağını bilmek yatırımcılığın en önemli konularından biridir.
  - T-atr notu (İKİNCİ EL, paraphrase): "Hayat kalitesini bozmayacak sermaye", işlem başına TL risk bütçesi. Örnek: "Göze alınan kayıp 500 TL / 2 ATR değeri 2 TL = 250 lot". Python satırı: `Close[-1] - 2*ATR[-1]`.
  - T-volatilite-ters-orantili (İKİNCİ EL): Volatilitesi yüksek hissede pozisyon büyüklüğü küçülür. Ana amaç sermayeyi korumak. "Uygun zamanda oyuna zaten girilir."
- Tanım (günlük OHLCV ile hesaplanabilir):
  1. `risk_tutarı = sermaye × 0,01`.
  2. `stop_mesafesi = 2 × ATR` (hisse başına, fiyat birimi).
  3. `lot_ham = risk_tutarı / stop_mesafesi`.
   4. Lot = tam sayı. Aşağı yuvarlama YORUM'dur; yaklaşık 70 hisse paylaşılan NotebookLM örneğidir, yuvarlama talimatı yoktur (NotebookLM, G115/g1, örnek hesap). 1000/14,30 = 69,93; 70 × 14,30 = 1001 > %1.
  5. Görsel metni "2 ATR değeri" der. 14,30 = 2 ATR mesafesi okunur (BİRİNCİ EL). T-atr örneğinde "2 TL" için aynı okuma doğru olursa 250 lot. ATR = 2 TL olsaydı 125 lot olurdu. Metin 250 diyor. Yani payda = 2×ATR mesafesi (görselde açık, T-atr'de çıkarım).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| risk / işlem | %1 sermaye (örnek) | NotebookLM, G115/g1; genel oran seçimi YORUM |
| stop mesafesi çarpanı | 2 ATR | görsel G-115 |
| örnek sermaye | 100.000 USD | görsel G-115 |
| örnek 2 ATR | 14,30 USD | görsel G-115 |
| örnek sonuç | ~70 hisse | görsel G-115 |
| ATR periyodu | verilmedi | YORUM (14, Wilder) |
| ATR hangi zaman diliminde | verilmedi | YORUM (günlük) |
| aşağı yuvarlama (69) | verilmedi | YORUM |
| komisyon/kayma payı | verilmedi | YORUM (sıfır başla, duyarlılık koş) |
| sermaye = nakit mi, toplam özkaynak mı | verilmedi | YORUM |

- Belirsiz kalanlar: ATR uzunluğu ve yumuşatma türü. Sermayenin tanımı (anlık özkaynak mı, başlangıç mı). Birden fazla açık pozisyonda toplam açık risk sınırı var mı (Tansu söylemedi). Lot üst sınırı (nakit aşımı). Aynı anda açık pozisyon sayısı. Örnekte giriş fiyatı yok, yani 70 × fiyat sermayeyi aşar mı bilinmiyor.
- Tansu'nun kanıtı: Tek örnek hesap. Performans, backtest, sembol yok. Sonuç: aritmetik tutarlı, edge kanıtı yok.
- Bedava günlük veriyle uygulanabilir mi: Evet. ATR günlük High/Low/Close ile hesaplanır. Lot bölünebilirliği (BIST 1 lot) için ek veri gerekmez.
- Kaynak güveni: Formül BİRİNCİ EL (infografik). Örnek kullanım "gerçek Tansu işlemi" değil. ATR detayı yok. Orta.

## K2. Acil stop (giriş − 2 ATR, gün içi anında çıkış)

- Kaynak: G-115 (NotebookLM görseli), G-125 (`assets/gorsel-paket-125-kismi-kar-trailing-stop/01-kismi-kar-trailing-prev-low-emergency-stop.jpg`), T-atr (not). Acil Stop ve Gün Sonu Stop adları aktarılan metinde vardır (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Tansu'nun ifadesi:
  - Görsel G-115, verbatim (BİRİNCİ EL infografik): "Acil Durum Stop'u: Giriş fiyatının 2 ATR değeri kadar altına bir stop noktası koyun." "Anında Çıkış Kuralı: Fiyat gün içinde acil durum stop seviyesine düşerse, anında pozisyonu kapatın."
  - G-125 notu (İKİNCİ EL, paraphrase): "2ATR emergency stop ile kalan tüm pozisyonun kapatılması".
  - G-125 görsel (BİRİNCİ EL): Sol uçta kırmızı kutu etiketi "STOP: 184.54" ve "ATR: 4.62" (düşük çözünürlük; ilk okumada net, büyütmede bulanık). Etiket yalnız bu iki sayıyı gösterir.
  - T-atr notu (İKİNCİ EL): "İlk stop fiyatın 2 ATR altı, acil stop intraday temasla".
- Tanım:
  1. Giriş günü: `stop = giriş_fiyatı − 2 × ATR` (ATR giriş kararında bilinen son tamamlanmış değer, YORUM).
  2. Her gün: `Low ≤ stop` ise çık (gün içi temas).
  3. Açılış stopun altındaysa (boşluk) dolum = açılış fiyatı veya daha kötüsü (YORUM; Tansu kaynaklarında yok).
  4. Aynı gün hem stop hem hedef değerse stop önce (YORUM, muhafazakâr).
   5. YORUM: bizim seçimimiz giriş ATR'si değişse bile stopu sabit tutmaktır. Aktarım giriş−2ATR ile güncel Close−2ATR'yi birlikte verir; başlangıç stopu ile güncelleme politikası ayrımı açık değildir (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| çarpan | 2 ATR | görsel G-115, not G-125 |
| tetik | gün içi temas, anında çıkış | görsel G-115 |
| etiket örneği | STOP 184,54 / ATR 4,62 | görsel G-125 |
| ATR periyodu | yok | YORUM (14) |
| ATR sabit mi, hareketli mi | kaynak genel güncelleme politikası vermiyor | YORUM: girişte sabit bizim seçimimiz; başlangıç/güncelleme ayrımı belirsiz (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22) |
| tetik fiyatı: Low mu, son işlem mi | yok | YORUM (günlük Low) |
| boşlukta dolum | yok | YORUM (açılış) |
| stop fiyatına limit emir mi, piyasa emri mi | yok | YORUM (piyasa) |

- Belirsiz kalanlar: G-125 etiketindeki 184,54 giriş − 2×ATR midir? Giriş fiyatı grafikte okunmuyor. Eğer öyleyse giriş ≈ 184,54 + 2×4,62 = 193,78 (YORUM, doğrulanmamış). G-125 etiketi soldadır, yani giriş anında yazılmış stop gibi görünür; bunu doğrulayan metin yok. Stop long için yazılmış; short için Tansu bir şey demedi.
- Tansu'nun kanıtı: Yok (kural anlatımı). G-125 grafiği seçilmiş tek örnek.
- Bedava günlük veriyle uygulanabilir mi: Evet, günlük High/Low ile. Gün içi sıra bilinmediği için aynı gün stop+hedef çatışması çözülemez (stop önce varsayımı). Açılış boşluğu günlük Open ile modellenir.
- Kaynak güveni: Kural BİRİNCİ EL (infografik). Orta-yüksek. Uygulama ayrıntıları yok.

## K3. Gün sonu (kapanış) stopu: SMA250

- Kaynak: G-115 (NotebookLM görseli), T-atr (not). Gün Sonu Stop adı aktarılan Tansu metnindedir (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Tansu'nun ifadesi: NotebookLM örneği SMA250 altında kapanışta çıkışı gösterir (NotebookLM, G115/g1). Aktarımda ortalama seçimi okura bırakılır (Aktarım, G115:20); SMA200, EMA200, EMA250 alternatifleri vardır. YORUM: SMA250'yi kesin giriş filtresi olarak seçmek bizim kararıdır; giriş karşılaştırması kaynakta yoktur.
- Tanım:
  1. Her gün kapanışında `Close < SMA250` ise çıkış sinyali.
  2. Çıkış ertesi seans açılışında (YORUM; Tansu "gün sonu" der, yani kapanışta emir mi, ertesi gün mü belirtmedi).
  3. K2 acil stop bundan bağımsız ve önceliklidir (YORUM; infografik iki kuralı yan yana verir, öncelik sırasını yazmaz).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| ortalama | SMA 250 gün | görsel G-115 |
| alternatifler | SMA200, EMA200, EMA250 | not G-115 |
| tetik | kapanış < ortalama | görsel G-115 |
| tampon/histerezis | yok | YORUM (0) |
| çıkış zamanı | yok | YORUM (ertesi açılış) |
| fiyat bazı: düzeltilmiş mi, ham mı | yok | YORUM (düzeltilmiş) |

- Belirsiz kalanlar: Seçim kuralı (hangi ortalama?). Giriş de SMA250 üstü mü gerektirir (not: giriş bileşenlerinden biri; geri kalan bileşenler verilmedi). 250 gün veri yoksa ne olacak (YORUM: sinyal yok).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet. 250 gün geçmiş gerekir (yeni halka arzlar elenir).
- Kaynak güveni: Kural BİRİNCİ EL (infografik). Orta-yüksek.

## K4. İz süren stop (trailing)

- Kaynak: G-125 (görsel + not); Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20.
- Tansu'nun ifadesi (İKİNCİ EL): giriş + 1,5 ATR aktivasyonu ve bundan sonraki barlarda ilk önceki dip altı kapanışta %50 satış anlatılır (Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20). G-125 grafiğinde çizgi/bantlar vardır; formül okunmaz.
- Tanım (aktarılan kaynak sırası; Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20):
   1. YORUM: bizim aktivasyon seçimi `High ≥ giriş + 1,5×ATR_giriş`; High teması mı kapanış mı kullanıldığı kaynakta açık değildir.
   2. Giriş + 1,5 ATR aktivasyonu geçilir; satış koşulu bundan sonraki barlarda aranır.
   3. Bu barlardan ilk `Close[t] < Low[t−1]` kapanışında %50 satış sinyali oluşur.
   4. %50'nin ilk mi kalan miktara mı uygulandığı açık değildir (Aktarım, G125:20).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| aktivasyon | giriş + 1,5 ATR | Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20 |
| satış sırası | aktivasyondan sonraki barlarda ilk dip-altı kapanış | Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20 |
| aktivasyon temeli (High/Close) | yok | YORUM |
| trailing ATR sabit mi | yok | YORUM |
| Chandelier / yalnız yukarı / max stop | kaynakta yok | YORUM alternatifleri; aktarılan dip-altı satış kuralının parçası değil |

- Belirsiz kalanlar: aktivasyonun High/Close bazı, ATR zamanı, aynı bar sırası, %50 paydası ve dolum zamanı. Chandelier ve max stop zinciri kaynak kuralı değildir (Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20).
- Tansu'nun kanıtı: G-125 grafiği; seçilmiş, olumlu yönetim örneği. Fiyat çıkış oklarından sonra düşer. Fiyat/dolum etiketi yok.
- Bedava günlük veri: kapanış ve önceki Low hesabı yapılabilir; aktivasyonun fiyat alanı, ATR zamanı ve dolum ayrıntıları açık değildir.
- Kaynak güveni: Düşük-orta. Formül yok.

## K5. Kısmi kâr ve "önceki gün dibi altı kapanış → %50 sat" (G-125)

- Kaynak: G-125 (görsel + not).
- Tansu'nun ifadesi (İKİNCİ EL, paraphrase): Görsel oklarını soldan sağa şöyle anlattı: giriş, ilk kâr alma, ikinci kâr alma, trailing/büyük kâr satış dönemi, "önceki günün en düşüğünün altında kapanışla %50 satış", "2ATR emergency stop ile kalan tüm pozisyonun kapatılması". "İlk kâr alma için %10 örneği verdi; oran kullanıcı/strateji tarafından seçilebilir." Görselden sonra fiyatın düşmeye devam ettiğini belirtti. Kısmi kâr almanın "karmaşık/çoklu çıkış koşullu stratejilerde belirli amaçlara hizmet ettiğini" söyledi.
- Görsel (BİRİNCİ EL): Kırmızı oklar ve sarı yıldız işaretleri. Fiyat/tarih/TP seviyesi yazısı yok. Yalnız STOP 184,54 / ATR 4,62 etiketi okunur.
- Tanım (kaynakta olan iskelet):
  1. Giriş.
  2. TP1: "%10" (anlamı belirsiz, aşağıda).
  3. TP2 (ikinci satış): ayrıntıları belirtilmemiş.
  4. Fiyat ≥ giriş + 1,5 ATR: trailing aktif (K4).
   5. Aktivasyon geçildikten sonraki barlardan ilk `Close[t] < Low[t−1]` kapanışında %50 satış sinyali oluşur (Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20); ertesi açılış dolumu YORUM'dur.
  6. 2 ATR emergency stop: kalan tamamını kapat (girişten itibaren aktif, YORUM).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| TP1 | "%10" | not G-125 (ikinci el) |
| TP1 anlamı | fiyat %10 mu, pozisyonun %10'u mu | belirsiz |
| TP2 (ikinci satış) | ayrıntıları belirtilmemiş | Aktarım, G125:20 |
| trailing aktivasyon | giriş + 1,5 ATR | not G-125 |
| önceki gün dibi tetik | aktivasyon geçildikten sonraki barlarda ilk kapanış < Low[t−1] | Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20 |
| azaltma oranı | %50 | not G-125 |
| %50 paydası | ilk lot mu, kalan lot mu | belirsiz |
| emergency | 2 ATR | not G-125 |
| tampon | yok | YORUM |

- Belirsiz kalanlar: (i) %10 fiyat getirisi mi (`giriş × 1,10`) lot oranı mı (`ilk lot × 0,10`). (ii) İkinci satışın ayrıntıları belirtilmemiş. (iii) %50 ilk miktarın mı kalan miktarın mı yarısı (Aktarım, G125:20). (iv) Kısmi satış sonrası stop taşınması. (v) Aynı gün olay sırası ve dolum. Dip-altı kapanış aktivasyondan sonraki barlarda aranır (Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20).
- Tansu'nun kanıtı: Tek seçilmiş grafik. Backtest yok, dolum yok, tam-çıkış kıyaslaması yok.
- Bedava günlük veri: Evet (Low[t−1], Close, ATR). Önceki gün dibi günlük mumdan hesaplanır.
- Kaynak güveni: Düşük. Yalnız özet metin ve okunmayan grafik. TP1/TP2 ve %50 kimlikleri çözülmeden uygulanamaz.

## K6. Volatiliteyle ters orantılı pozisyon (kavram) ve GARCH sözü

- Kaynak: T-volatilite-ters-orantili (not), T-garch (not).
- Tansu'nun ifadesi (İKİNCİ EL): "Volatilitesi yüksek hisselerde position sizing'in matematiksel olarak küçülmesi doğru bir risk yönetimi kuralıdır." "Yüksek volatilite yüksek kâr fırsatı kadar yüksek risk taşır." "Ana amaç sermayeyi korumak; uygun zamanda oyuna zaten girilir." T-garch: GARCH ve standart sapma ile volatilite riskini azaltma örneğini "bu akşam" göstereceğini söyledi (söz; örnek yok).
- Tanım: K1 ile aynı. Sabit parasal risk / geniş ATR stopu = küçük lot. Volatilite ölçüsü, pencere verilmedi. GARCH içeriği yok (yalnız vaat).
- Parametreler: Hepsi yok. Pencere, ölçü (std/ATR/GARCH), risk % (K1'den %1 alınabilir, YORUM).
- Belirsiz kalanlar: Ters orantılı ağırlık (inverse-vol portföy) mı, sabit risk lotu mu. Notlar ikisini ayırır; Tansu ayırmadı.
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: İlke düzeyi, İKİNCİ EL. K1 ile tutarlı.

## K7. Pozisyon büyüklüğü çarpanı: Tam / Defansif (SMRTG)

- Kaynak: G-48 (`assets/gorsel-paket-48-smrtg-fiyat-vol/01-smrtg-fiyat-vol-birlikte-artis-defansif.jpg`), not.
- Tansu'nun ifadesi (İKİNCİ EL, paraphrase): "SMRTG'de yeni çılgınlık başladı. Sistem pozisyonu kapatıp defansif duruma geçti. Fiyatla volatilitenin aynı anda artması genellikle kötü sonuçlanır."
- Görsel (BİRİNCİ EL, büyütülerek okundu): Üç panel. Üst: fiyat (TL) ~18'den ~6-8'e iner, sağ uçta keskin yükseliş. Orta: mavi düz çizgi ve turuncu noktalı çizgi; kırmızı kesikli "Kırılma Eşiği (0.0)"; mor noktalı yatay çizgi ≈0,2. Alt: "Pozisyon Büyüklüğü Çarpanı" ikili adım grafiği, üst seviye "(Tam)", alt seviye "(…ansif)" (Defansif).
- Tanım (YORUM-gözlem): Dört geçişte mavi serinin sıfır geçişi ile Tam/Defansif değişimi birlikte görülür; bu katalogda ilişki adayı olarak okunur. Tek neden veya tam üretim koşulu doğrulanmaz; mor 0,2 çizgisinin rolü açık değildir (Araç, G48/g1).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| eşik | 0,0 ("Kırılma Eşiği") | görsel G-48 |
| 0,2 çizgisi | rolü belirsiz | görsel |
| Tam çarpan değeri | kaynakta yok | YORUM: 1,0 bizim seçimimiz; genel eşleme açık değil (Aktarım, G48:21) |
| Defansif çarpan değeri | kaynakta yok | YORUM: 0 = kapalı bizim seçimimiz; aktarım yalnız bu olayda pozisyonu kapattığını söyler, genel eşleme vermez (Aktarım, G48:21) |
| mavi serinin tanımı | yok | YORUM (hisse getirisi ile Δvolatilite'nin yuvarlanan korelasyonu; not da doğrulanmadı diyor) |
| turuncu seri | yok | belirsiz |
| pencere | yok | belirsiz |

- Belirsiz kalanlar: Mavi/turuncu serilerin tanımı ve pencere. Seri adları görselde kapatılmış (beyaz bantlar). Tam ve Defansif sayısal çarpanlar. Çıkışı yapan mı çarpan mı (metin "kapatıp", grafik çarpan).
- Tansu'nun kanıtı: Tek hisse (SMRTG), seçilmiş. Defansif dönemlerde fiyat ağırlıkla sert düşmüş gibi görünür; sistemin P&L sonucu yok.
- Bedava günlük veri: Kısmen. Fiyat verisi var. Hangi "volatilite" olduğu (gerçekleşen, ATR, implied) bilinmediği için seri yeniden üretilemez. Aday: 20 günlük getiri std değişimi (YORUM).
- Kaynak güveni: Görsel BİRİNCİ EL. Seri kimliği yok. Düşük-orta.

## K8. Volatilite şok freni (yeni alım yok)

- Kaynak: T-volatilite-piyasa-soku-yeni-alim-freni (not; URL yok).
- Tansu'nun fikri, oynaklık şokunda yeni alımı durdurup mevcut riski yönetmektir (Aktarım, tweet-volatilite-piyasa-soku-yeni-alim-freni:21); uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- Tanım: `oran = std(getiri, son X gün) / std(getiri, son ~21 gün)`. `oran ≥ eşik` ise şok. Şokta yeni giriş yok. (X, pencere, eşik hepsi YORUM; notta formül Claude'a ait.)
- Parametreler: X yok. "Bir ay" = ~21 işlem günü (YORUM). Eşik yok. Çıkış/bekleme süresi yok.
- Belirsiz kalanlar: Piyasa şoku endeks düzeyinde mi, hisse bazında mı (not ayırır, Tansu demedi). Kısa pencere aylık pencerenin içinde (örtüşme).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: İlke İKİNCİ EL. Parametre yok.
- Not: Bizim GLOSSARY'deki "Piyasa Nabzı BEKLE günü yeni giriş yok" bu ilkeye benzer ama eşiği Tansu vermedi.

## K9. Fat tail, hayatta kalma

- Kaynak: T-fat-tail-firsat-survival-konvekslik (not), T-probabilistik-edge (not).
- Tansu'nun ifadesi (İKİNCİ EL): "Herkesin olduğu yerde para yoktur." "En büyük kârlar Fat Tails alanında yapılır" (George Soros'a atfedilmiş, doğrulanmadı). Zamanın %95'i normal, %5'i kriz/şok/aşırı ralli. Küçük yatırımcı şokta panikle satar, "Smart Money" fırsat görür. T-probabilistik: Algoritmik geliştiricinin en büyük tuzağı kesin yön tahmini ve klasik indikatör parametrelerini geçmişe uydurmak. Normal dağılım yerine fat tail, skewness, kurtosis. Monte Carlo ile risk of ruin ve güven aralığı.
- Tanım: Kural yok. Yalnız ilke. Parametre: "%95 / %5" anlatı sayısı, eşik değil (YORUM: sabit sayma).
- Belirsiz kalanlar: fırsat anlatısı işlem tetiği vermez; şok frenine istisna oluşturmaz. İki fikir arasında açık mantıksal çelişki kanıtlanmış değildir; strateji, zaman ve eylem açık değildir (Aktarım, tweet-fat-tail-firsat-survival-konvekslik:21 ve şok notu:21).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Kuyruk istatistikleri evet. Risk of ruin için işlem dizisi gerekir.
- Kaynak güveni: Düşük (anlatı). İşlem kuralı ve atıf doğrulanmış değildir.

## K10. Likidite ve kapasite kapısı

- Kaynak: T-likit-hisseler-etf-islem-derinligi-slippage-kapasite (not).
- Tansu'nun ifadesi (İKİNCİ EL): Trade'i ciddiye alan yeni yatırımcılar derinliği olmayan alanlar ve sığ hisseler yerine ETF'lere ve likit hisselere odaklanmalı. Gerekçe: istenen zamanda ve makul fiyatta girip çıkabilmek, sermayeyi düşük likiditede kilitlememek.
- Tanım: Eşik yok. Notun `quantity_liquidity` kuralı Claude'a ait (YORUM).
- Parametreler: Yok (ADV, spread, katılım oranı verilmedi).
- Belirsiz kalanlar: "Likit" tanımı, hangi ETF'ler (BIST'te sınırlı).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Kısmen. Günlük hacim ve TL hacmi var. Spread ve derinlik yok (G-126 order book ayrı kaynak, kapsam dışı).
- Kaynak güveni: İlke, İKİNCİ EL.

---

# BÖLÜM 2. Kâr alma, çıkış, geçersizlik

## K11. Harmonik hedef merdiveni (BALAT, CD geri alımı)

- Kaynak: G-109 (`assets/gorsel-paket-109-balat-harmonik-tp/01-balat-siyah-kugu-harmonik-tp.png`), not.
- Tansu'nun ifadesi (İKİNCİ EL, paraphrase): Harmonik formasyonlarda D noktasındaki dönüşten sonra TP seviyeleri CD bacağının geri alım oranlarıyla kurulur. Bullish örnek: TP1 = 0,382, TP2 = 0,618, TP3 = C noktası, TP4 = 1,272/1,618 uzantı. "TP1'de kısmi kâr ve stop'u entry'ye çekme. TP2 güçlü/hacimli aşılırsa trend hedeflerine geç." Stop: bullish yapılarda X altı; bazı derin patternlerde XA 1,13/1,27 uzantısı. Not: TP2 "en güvenilir hedef" kaynak görüşü.
- Görsel (BİRİNCİ EL, okundu): Başlık "BALAT.IS - Siyah Kuğu & HEDEFLER". Sağ üst çizgi etiketleri: "TP4 (1.272): 92.98", "TP3 (C Tepe): 90.50", "TP2: 87.02", "TP1: 84.88", "STOP: 64.00". Panel: RSI, ADX, MACD. Tarih ekseni Eylül–Aralık 2025. D fiyatı yazılı değil.
- Tanım: `TP(r) = D + r × (C − D)`. r = 0,382; 0,618; 1,000; 1,272.
  - Doğrulama (benim hesabım): C − D = 9,10 ve D ≈ 81,40 ile TP1 = 84,88, TP2 = 87,02, TP3 = 90,50, TP4 = 92,98. Görsel seviyeleriyle uyuşur (yuvarlama içinde).
  - Görseldeki risk/ödül (ölçüm): D ≈ 81,40, stop 64,00, risk ≈ 17,40; TP1 ödülü ≈ 3,48 (0,20 R), TP2 ≈ 5,62 (0,32 R). YORUM: bu katalogda K23'ün 1:2/1:3 eşiğiyle karşılaştırılır; kaynakların farklı bağlamlarını bütün sistemlerde ortak R/R kuralı olarak birleştirmek doğrulanmış değildir (Aktarım, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:48–49; G123:42–49).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| TP1 | D + 0,382 (C − D) | görsel G-109 (84,88) |
| TP2 | D + 0,618 (C − D) | görsel G-109 (87,02) |
| TP3 | C (%100) | görsel G-109 (90,50) |
| TP4 | 1,272 (1,618 alternatif, not) | görsel 92,98 / not |
| stop (BALAT) | 64,00 | görsel G-109 |
| stop kuralı | X altı / XA 1,13-1,27 | not (ikinci el) |
| TP1'de kısmi miktar | yok | belirsiz (G-123'te %50) |
| stop → entry | TP1 sonrası | not (ikinci el) |
| stop tamponu | yok | YORUM |

- Belirsiz kalanlar: Kısmi miktar G-109'da yok. Entry fiyatı (D mi, onaylı dönüş mü) yok. TP2 "güçlü/hacimli" eşiği yok. TP4: 1,272 mi 1,618 mi (görsel 1,272 yazıyor).
- Tansu'nun kanıtı: Tek grafik. Gerçekleşen sonuç yok (grafik sağ uçta TP3'e yakın/üstü gibi görünür; okunmadı, YORUM yapılmadı).
- Bedava günlük veri: TP aritmetiği evet. Pivot (X, A, B, C, D) tespiti kuralı yok; pivot parametreleri verilmedi.
- Kaynak güveni: Seviyeler BİRİNCİ EL. Yönetim kuralları İKİNCİ EL.

## K12. Gartley takip tablosu: stop ve TP1/TP2 (G-123) ve SAYAS aracı

- Kaynak: G-123 (`assets/gorsel-paket-123-gartley-algoritmik-tablo/01-gartley-excel-algoritmik-takip-tablosu.png`), T-gartley-d-tepki-penceresi (`assets/tweet-gartley-d-tepki-penceresi/01-sayas-gartley-d-tepki-penceresi.jpg`), not G-123.
- Tansu'nun ifadesi:
  - G-123 tablosu, verbatim (BİRİNCİ EL; Excel/yazılım mantığı örneği): "Stop Loss (SL) | X Noktası (veya XA 1.13) | Pozisyon Kapat (Invalidation) | SL = X_Fiyat − ATR*2". "Take Profit 1 (TP1) | AD'nin %38.2'si | Pozisyonun %50'sini Kapat | TP1 = D + (A-D) * 0.382". "Take Profit 2 (TP2) | AD'nin %61.8'i | Kalan Pozisyonu Kapat | TP2 = D + (A-D) * 0.618". "D Noktası (GİRİŞ) | XA'nın %78.6'sı | Buy Limit / Sell Limit | Giriş Fiyatı = X + (A-X)*0.786 (Boğa için)". "B Noktası Teyidi | XA'nın %61.8'i". "C Noktası Teyidi | AB'nin %38.2 - %88.6 arası".
  - Not G-123 (İKİNCİ EL): Girişte R:R hesapla. Reward/risk < 1,5 (veya stratejiye göre < 2) ise pattern doğru olsa da işlemi reddet. BIST için Python/Excel'de %3-5 tolerans.
  - SAYAS görsel (BİRİNCİ EL; Tansu aracı "Sistem: Carney", başlık "Patern #2 Detaylı (Fibonacci + Trade Management) — Bullish (LONG)"): Legend: "Giriş (D)", "Bk Stop (X)", "TP1 (1:1 R/R)", "TP2 (.618 AD)". Fib etiketleri (XA bacağı, büyütülerek okundu, son rakamlar bulanık): 0.000 = 144.25; 0.236 = 115.03; 0.382 = 96.98; 0.5 = 82.41; 0.618 = 67.82; 0.786 = 47.05; 1.000 = 20.65.
- Tanım (iki farklı TP1 tanımı var):
  - A) Excel tablosu: `TP1 = D + 0,382 × (A − D)`, %50 kapat. `TP2 = D + 0,618 × (A − D)`, kalanı kapat. Stop = X veya `X − 2×ATR`.
  - B) SAYAS aracı: `TP1 = D + (D − X)` (1:1 R/R). `TP2 = D + 0,618 × (A − D)`. Stop = X.
  - SAYAS doğrulaması (benim hesabım; piksel konumları ile kontrol edildi): D = 47,05, X = 20,65, A = 144,25. TP1 = 47,05 + 26,40 = 73,45. TP2 = 47,05 + 0,618 × 97,20 = 107,12. Çizili iki yeşil noktalı çizgi ≈73 ve ≈107'de. TP 0,382 AD (≈84,2) çizilmemiş. Yani B tanımı doğrulandı.
  - Not (kendi hesabım): Excel örneğindeki bullish D = X + (A−X)×0,786 ifadesi, XA'nın %78,6 geri çekilmesi değil (o X + 0,214 (A−X) olur). SAYAS çıktısında D = 47,05 = fib 0,786 çizgisi (A'dan aşağı 0,786 ölçülmüş), yani Excel formülü örnek yazımda ters (G-123 notu aynı bulguyu verir).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| stop | X veya XA 1,13 veya X − 2 ATR | görsel G-123 |
| stop (SAYAS) | X | görsel SAYAS |
| TP1 (Excel) | AD %38,2, %50 kapat | görsel G-123 |
| TP1 (SAYAS) | 1:1 R/R | görsel SAYAS |
| TP2 | AD %61,8, kalan kapat | görsel (iki kaynak) |
| min R:R girişte | 1,5 (veya 2) | not G-123 (ikinci el) |
| tolerans | %3-5 | not G-123 (ikinci el) |
| ATR periyodu | yok | YORUM |
| giriş | D'de limit | görsel G-123, SAYAS "Giriş (D)" |

- Belirsiz kalanlar: eğitim tablosu TP1 AD×0,382, SAYAS TP1 1:1 R/R gösterir; tek genel TP1 yoktur (Eğitim, G123/g1; Araç, SAYAS görseli). Stop X / XA 1,13 / X−2 ATR için genel seçim kuralı yoktur (Eğitim, G123/g1; Araç, G02/g1). "Bk Stop" kısaltması, pivot ve tolerans birimi açık değildir.
- Tansu'nun kanıtı: SAYAS tek grafik; fiyat D'den sonra uzun süre yatay, TP'lere gitmemiş görünür (2023-2026 aralığı; grafikte fiyat ~47 üstünde dolaşır, 73'e yakın bir tepe var). Sonuç etiketi yok. Bu örnek Tansu'nun "Gartley her zaman çalışmaz" mesajıyla uyumlu (T-gartley-d notu).
- Bedava günlük veri: Formül evet. Pivotlar için dedektör kuralı gerekir.
- Kaynak güveni: Tablo ve SAYAS legend BİRİNCİ EL (yüksek). İkisi çelişir. Orta.

## K13. Kırılım, FVG, retest, teyit kartı (AKFIS): ENTRY, STOP, TP1-3

- Kaynak: K-akfis (`assets/kaynak-akfis-breakout-fvg-retest-2095523694881697974/akfis.webp`, `alinti-ornek.webp`), not.
- Tansu'nun ifadesi: 2 Eylül 2026 alıntı gönderisinin önerdiği sıra "Breakout → FVG → Retest → Confirmation" (not özeti, İKİNCİ EL). Görsel başlığı verbatim (BİRİNCİ EL): "AKFIS | Breakout + Range Retest + RSI Divergence | A+ SETUP | AL TETİKLENDİ | Sınıf: A+ | Skor: 100/100". Legend: AKFIS, Hacim, VolMA20, RSI 14, Range High / Retest, Range Low, "FVG %50", AL, ENTRY, STOP, TP1, TP2, TP3.
- Tanım (Tansu'dan çıkan): Konsolidasyon kutusu → yukarı kırılım → bullish FVG + confluence → range high retest → confirmation → AL. Çıkış çizgileri: ENTRY (yeşil düz), STOP (kırmızı kesikli), TP1/TP2/TP3 (kesikli). "FVG %50" noktalı çizgi = FVG orta noktası.
- Benim piksel okumam (YORUM, yaklaşık, fiyat etiketi yok):
  - Alıntı örneği (sembolsüz, eksen 100-150): ENTRY ≈ 114,3; STOP ≈ 106,4 (FVG bandının hemen altı); range high ≈ 111,3; FVG ≈ 107,5-108,8; hedef çizgileri ≈ 120, ≈122, ≈130. Stop mesafesi ≈ 7,9. Hedefler ≈ 0,7R, 1,0R, 2,0R.
  - AKFIS ana görsel: ENTRY ≈ 3,75; STOP ≈ 3,62; üç hedef çizgisi ≈ 3,87-4,00. Çizgi renkleri legend ile eşleşmiyor (TP2/TP3 sırası tutarsız görünüyor).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| FVG referansı | %50 (orta nokta) | görsel legend |
| stop konumu | FVG/retest bölgesi altı (≈) | YORUM (piksel) |
| TP sayısı | 3 | görsel legend |
| TP fiyat/oran | yok | belirsiz |
| puan | 100/100, A+ | görsel (formül yok) |
| RSI | 14 | görsel legend |
| hacim ortalaması | VolMA20 | görsel legend |

- Belirsiz kalanlar: Stop ve TP kuralları tamamen. Puan formülü. FVG tespit/dolum kuralı. Retest toleransı. "Confirmation" koşulu.
- Tansu'nun kanıtı: Seçilmiş olumlu örnek; sonraki yükseliş görselde var. Sonuç/dolum yok.
- Bedava günlük veri: Fikir evet. Stop/TP kuralı olmadığı için çıkış uygulanamaz.
- Kaynak güveni: Etiket BİRİNCİ EL. Çıkış parametresi yok. Düşük.

## K14. Fincan-kulp hedef ve R/R (GUBRF)

- Kaynak: G-58 (`assets/gorsel-paket-58-gubrf-fincan-kulp/01-gubrf-fincan-kulp-fibo-kirilim-hedef.png`), not.
- Tansu'nun ifadesi: Görsel başlığı verbatim (BİRİNCİ EL): "GUBRF — Formasyon Tamamlanma: 2025-10-28 | Risk/Reward: 1:2.27". Etiketler: "SİNYAL! 2025-10-24", "HEDEF: 389.30", "KIRILIM: 300.75", "Fibo Bitiş: 317.00", "Fibo Başlangıç: 212.20", Fib 0% 317.00, 23,6% 292.27, 38,2% 276.97, 50% 264.60, 61,8% 252.23, 78,6% 234.63, 100% 212.20. Not (İKİNCİ EL): "fincan derinliği kadar neckline üstü hedef".
- Tanım: Hedef = kırılım + (kırılım − fincan dibi) = 300,75 + (300,75 − 212,20) = 389,30 (benim hesabım; görselle uyuşur).
- R/R 1:2,27 doğrulaması: Stop yazılı değil. Giriş = 300,75 varsayımıyla ödül 88,55; risk = 88,55 / 2,27 = 39,01; ima edilen stop ≈ 261,74 (not da aynı; Fib %50 264,60'a yakın). Giriş = 317,00 (Fib 0%) varsayımıyla ödül 72,30; risk 31,85; stop ≈ 285,15. İki giriş varsayımı da doğrulanmış değil (YORUM).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| hedef | kırılım + fincan derinliği | not + hesap |
| hedef fiyatı | 389,30 | görsel |
| R/R | 1:2,27 | görsel |
| stop | yok | belirsiz |
| giriş | yok (sinyal tarihi 24.10.2025) | belirsiz |
| sinyal ile tamamlanma tarihi farkı | 24.10 vs 28.10 | görsel |

- Belirsiz kalanlar: Stop, giriş fiyatı, kulp derinliği çelişkisi (kaynak metin %50-61,8 sığ düzeltme der; görselde turuncu kulp dibi ≈240, Fib %61,8'in 252 altında; not bunu çelişki olarak işaretler).
- Tansu'nun kanıtı: Tek örnek, fiyat hedefi aşıp ≈450 üstüne çıkmış (BİRİNCİ EL grafik). Seçilmiş olumlu örnek.
- Bedava günlük veri: Hedef formülü evet. Dedektör kodu yok.
- Kaynak güveni: Etiketler BİRİNCİ EL (yüksek). Stop yok. Orta.

## K15. Durum etiketleri ve geçersizlik (AKTİF, TAMAMLANDI, TEPKİ_VERDİ, BOZULDU, TAMAM, belirsiz)

- Kaynak: G-02 (`assets/gorsel-paket-02/01-soke-luks-coklu-sistem-sonuclari.png`), G-03 (`assets/gorsel-paket-03/01-smrtg-swing-fibonacci-abcd-analizi.jpg`, `02-smrtg-backtest-sonuclari.png`), G-01, T-gartley-d-tepki-penceresi, T-harmonik-xb-trend-kirilimi (`assets/tweet-harmonik-xb-trend-kirilimi-stratejisi/01-kaplm-xb-trend-kirilimi.jpg`), T-abcd-geometrik-gecerlilik-kurallari (not), T-iskpl-abcd (not).
- Tansu'nun ifadesi (BİRİNCİ EL araç çıktıları):
  - G-02 tablosu: sütunlar "Hisse | Tip | Sistem | Durum | Reaksiyon | D Hedefi | Giriş | Stop (X)". SOKE.IS: "SAT (taktik KISA, D'ye kadar) — D'de AL'a döner", Pesavento ve Carney, Durum "AKTIF", Reaksiyon "-", D hedefi 12.53, Giriş "-", Stop "-". LUKSK.IS: "AL (Buy)", Durum "TAMAMLANDI", Reaksiyon "TEPKI_VERDI", D hedefi 86.95, Giriş 86.95, Stop 73.00.
  - G-03 grafiği: D hedef etiketleri "[TAMAM]" ve "[BOZULDU]" (örn. "D (hedef): 12.43 [TAMAM]", "D (hedef): 27.34 [BOZULDU]", ileri hedef "D (hedef): 16.75").
  - G-03 backtest ekranı: "Toplam patern sayısı: 12, Hedefe ULAŞAN: 7, Stop'a takılan / bozulan: 3, Henüz sonuçlanmamış (açık): 2". İşlemler: stop −23,29%, −12,10%, −24,85%; hedef +36,59, +28,93, +50,72, +47,30, +30,61, +26,14, +24,20. Başlangıç 100.000 TL, bitiş 405.327,42 TL, "Toplam getiri: %305.33". Her işlemde tüm sermaye bileşik kullanılmış görünür (sermaye sütunu).
  - KAPLM görseli başlığı verbatim: "KAPLM.IS - Eşleşen Patern (Bullish) [TAMAMLANDI] | D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ) | [Ek bilgi] C sonrası fiyat son 10 günde BEKLENEN yönde: DÜŞÜYOR (Bullish/AL paternde CD bacağı aşağı olmalı...".
  - G-01'de "D: 226,80 [TAMAMLANDI]" ve "DGATE.IS — Kelebek Formasyonu (AL) [AKTİF]" (not tablosundan, görsel açılmadı, İKİNCİ EL).
  - T-gartley-d (İKİNCİ EL): "Her Gartley beklenen D sonrası dönüşü üretmez. D'den sonra 10 gün içinde beklenen yönde tepki oluşmazsa yapı belirsiz kabul edilebilir."
  - T-abcd (İKİNCİ EL): AB=CD kuralları: BC ≤ AB (eşitlik geçerli). D, B'yi CD yönünde aşmalı. C'den sonra fiyat A'yı BC yönünde aşarsa pattern bozulur.
- Tanım (etiket anlamları, çıkarım):

| etiket | çıkarılan anlam | güven |
|---|---|---|
| AKTİF | Formasyon durumu: D henüz oluşmadı veya oluşuyor; giriş ve stop ayrı alanlardır | Araç, G02/g1 |
| TAMAMLANDI | Formasyon durumu: D bölgesine ulaşıldı/pattern tamamlandı; pozisyon sonucu değil | Araç, G02/g1 ve G03/g1 |
| TEPKİ_VERDİ / TEPKİ GELMEDİ | Reaksiyon alanı: D sonrası beklenen yönde tepki; formasyon durumundan ayrı | Araç, G02/g1 ve G03/g1; KAPLM üst notu |
| BELİRSİZLEŞTİ | KAPLM: pencere içinde reaksiyon yok | görsel KAPLM |
| TAMAM [G-03] | AB=CD D hedefine ulaşıldı | görsel G-03 + backtest ("hedef") |
| BOZULDU [G-03] | Formasyon geçersizliği; işlem stop fiyatı bu etiketten çıkmaz | Araç, G03/g2; Aktarım, tweet-abcd-geometrik-gecerlilik-kurallari:21 |
| BOZULDU kriteri | C sonrası A aşılır (kural notta) | not T-abcd (ikinci el) |

- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| tepki penceresi | 20 bar ("TEPKİ GELMEDİ") | görsel KAPLM |
| "belirsizleşti" penceresi | son 10 gün | görsel KAPLM |
| tweet'teki pencere | 10 gün | not (ikinci el) |
| 10 gün = takvim mi, işlem günü mü | yok | belirsiz |
| minimum tepki büyüklüğü | yok | belirsiz |
| AB=CD stop | fiyatı bilinmiyor; A ihlali geometrik geçersizliktir | Araç, G03/g2; Aktarım, tweet-abcd-geometrik-gecerlilik-kurallari:21 |
| AB=CD işlem getirisi | stop −12…−25%, hedef +24…+51% | görsel G-03 |

- Belirsiz kalanlar: on günlük tepki penceresi D'den başlar; takvim/seans birimi yoktur (Aktarım, tweet-gartley-d-tepki-penceresi-10-gun:21). KAPLM'deki 20 bar ve "son 10 gün" ayrı ifadelerdir, ortak politika yoktur (Araç, KAPLM üst notu). Minimum tepki büyüklüğü yoktur. A ihlalinin Close/High/Low bazı ve işlem stopunun A olup olmadığı açık değildir (Aktarım, tweet-abcd-geometrik-gecerlilik-kurallari:21; Araç, G03/g2).
- Tansu'nun kanıtı: G-03: 12 pattern, 7 hedef, 3 stop, 2 açık; kapanmış işlemlerde %70 isabet (7/10). Tek hisse (SMRTG), 2024-2026. T-iskpl: ISKPL için 5/5 hedef, 1000 günlük tarama (not; görsel açılmadı). Seçilmiş hisseler. KAPLM örneği ise başarısız örnek (D'de tepki yok); Tansu bunu kendisi paylaştı.
- Bedava günlük veri: Evet, ancak pivot ve dedektör kuralları gerekir.
- Kaynak güveni: Etiketler BİRİNCİ EL (yüksek). Eşikler yok veya çelişkili. Orta.

## K16. Demand bölgesi geçersizliği (TTKOM)

- Kaynak: G-13 (`assets/gorsel-paket-13-ttkom-demand-invalidation/01-ttkom-demand-zone-break-clipping.png`), not.
- Tansu'nun ifadesi (İKİNCİ EL): oluşum sonrası ilk `Close < zone_low` kapanışında demand kutusu biter; `Low < zone_low` daha katı ayrı seçenektir (Aktarım, G13:21). Aracın hangi seçeneği kullandığı ayrıca doğrulanmış değildir.
- Görsel (BİRİNCİ EL): Başlık "TTKOM - Demand & Supply Bölgesi Analizi". Kırmızı ok, fiyatın eski gri demand kutusunun altına inmesini gösterir. Gri kutu kırılım tarihinde biter. Alt tablo: Son Fiyat 54.50, Max 75.85, Min 47.48, Aktif Demand 49.05-51.30, D.Touch 0, Aktif Supply 63.29-65.48, S.Touch 1.
- Tanım: oluşum sonrası ilk t için `Close[t] < zone_low` olduğunda bölge t'de geçersizdir (Aktarım, G13:21); sonraki kırılım tarihi değiştirmez. `Low[t] < zone_low` daha katı ayrı seçenektir.
- Parametreler: tampon yok (YORUM 0). Ana tarif Close'tur; Low ayrı seçenektir (Aktarım, G13:21). Zaman dilimi açık değildir.
- Tansu'nun kanıtı: Tek grafik, yalnız görsel doğrulama.
- Bedava günlük veri: Evet (bölge tanımı verilirse).
- Kaynak güveni: Görsel BİRİNCİ EL, kural İKİNCİ EL. Orta-düşük.

## K17. Retest bekle (AKSGY)

- Kaynak: G-103 (`assets/gorsel-paket-103-aksgy-retest-macd-volume-failure/01-aksgy-retest-macd-volume-failure.png`), not.
- Tansu'nun ifadesi (İKİNCİ EL): Retest beklemenin önemini AKSGY grafiğiyle anlattı. "MACD toparlanma sinyali yanıltıcı oldu. Hacim bu hareketi hiç desteklemedi."
- Görsel (BİRİNCİ EL): Başlık "AKSGY | EMA8 > EMA13 > EMA5 | ADX: 34.13 | RSI: 41.13 | MACD: -0.013 | RETEST VAR (6 kez)", "İlk Temas: 2025-10-14 | Son Temas: 2025-12-08 | Temas Sonrası: 9 gün". Fiyat yükselen cyan destek çizgisine 6 kez dokunur. Son büyük kırmızı mum destek altına sarkar. Hacim panelinde alım denemelerinde genişleme yok. Kırmızı çerçeve son retest kümesini gösterir.
- Tansu'nun fikri, AKSGY'de retest ve hacim teyidi aramaktır (Aktarım, G103:21 ve trend çizgisi notu:21); çıkış için uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- Parametreler: Temas toleransı yok. Çizginin çıkarımı (anchor) yok. EMA 5/8/13 sırası ters (8>13>5) görsel başlıkta yazılı (ilginç, "EMA8 > EMA13 > EMA5").
- Tansu'nun kanıtı: Tek başarısız teyit örneği.
- Bedava günlük veri: Evet; çizgi kuralı gerekir.
- Kaynak güveni: Düşük (kural yok).

---

# BÖLÜM 3. Süreç ve değerlendirme kuralları

## K18. Backtest ile giriş sadeleştirme ve işlem günlüğü

- Kaynak: `not-backtest-giris-sadeligi-risk-islem-gunlugu.md` (URL var: x.com/The_Tansu_/status/2095213493133713664, 2 Eylül 2026; not, kaynağı doğrulandığını söyler). Görsel yok.
- Tansu'nun ifadesi (İKİNCİ EL; paraphrase, tweet metni notta özetlenmiş):
  1. "Adayları geriye dönük izle": örnek: 26 Ağustos'ta seçilen hisselerin sonraki 1, 3 ve 5 gündeki sonuçlarını incele.
  2. Aday tiplerini karşılaştır: "Daily iyi + 4H bullish CHoCH + RS güçlü + Demand/FVG desteği" gerçekten kazandırıyor mu? Retest beklemek yarar sağlıyor mu, girişi fazla mı geciktiriyor?
  3. Girişi sadeleştir: Market Structure ve fiyat davranışı ana motor. RSI, MACD, WaveTrend ve RS yardımcı teyit. Tüm göstergelerin aynı anda yeşil olması gerekliliğini veriyle sorgula.
  4. Riski merkeze koy: "Güzel setup tek işlemde büyük sermaye riski için gerekçe değil." Pozisyon büyüklüğü stop mesafesine göre. Belirli risk yüzdesi önerilmiyor.
  5. İşlem günlüğü: "aday tarihi → giriş → giriş gerekçesi → invalidation → TP → sonuç → MFE/MAE". Birkaç aylık kayıtla gerçek istatistik.
  6. Yalnız katkı sağlayanı tut: göstergeleri ve filtreleri sonuçlara katkısına göre ölç; katkısı olmayanı sadeleştirme adayı yap.
  - Ek paylaşım (2 Eylül 2026, 20:24, not özeti): "Analize indikatörün AL sinyaliyle başlanmıyor." İnceleme sırası: bölge → kırılımlar → likidite hareketleri → 4 saatlik teyit.
- Tanım (bizim backtest için çıkan):
  1. Her aday için sinyal tarihi t0 kaydet. Sonuç: getiri(t0+1), (t0+3), (t0+5) işlem günü (gün tanımı belirsiz, aşağıda).
  2. Aday sonrası fiyat değişimi ile uygulanabilir giriş/çıkış sonucunu ayrı ölç (not, Cevo sentezi, YORUM).
  3. Her filtreyi tek tek çıkarıp (ablation) katkıyı ölç.
  4. Günlük alanları: aday_tarihi, giriş, gerekçe, invalidation, TP, sonuç, MFE, MAE.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| takip ufukları | 1, 3, 5 gün | not (ikinci el) |
| gün = takvim mi, işlem günü mü | yok | YORUM (işlem günü) |
| günlük alanları | 8 alan | not |
| risk % | verilmedi | belirsiz |
| minimum örneklem | "birkaç ay" | not |
| maliyet varsayımı | yok | YORUM |

- Belirsiz kalanlar: Karar eşikleri ("katkı sağlıyor" ne demek). Retest beklenen süre. Giriş oluşmayan adayların sonucu (not: korunmalı, YORUM).
- Tansu'nun kanıtı: Yöntem önerisi. Sonuç yok.
- Bedava günlük veri: Evet (1/3/5 gün için). MFE/MAE günlük High/Low ile yaklaşık hesaplanır.
- Kaynak güveni: URL'li tweet (en güvenilir süreç kaynağı), ama metin özet. Orta-yüksek.

## K19. Teknik indikatör ve sistem değerlendirme kriterleri

- Kaynak: `tweet-teknik-indikator-islem-sistemi-degerlendirme-kriterleri.md` (not; URL yok).
- Tansu'nun ifadesi (İKİNCİ EL; notun "Kaynak ilkeleri" listesi; "Levent'in saklanmasını istediği çerçeve" der, yazar atfı kesin değil):
  1. Kazanma oranı acemilerin sık takıldığı, tek başına sistem kalitesini göstermeyen metrik.
  2. Sık yanılan sistem yüksek kazanç/zarar asimetrisiyle başarılı olabilir; sık haklı çıkan sistem küçük kazanç/büyük kayıp ile zayıf olabilir.
  3. Toplam net kâr ile maksimum sermaye erimesi birlikte okunmalı.
  4. Maksimum drawdown yalnız arka arkaya zararların toplamı değil, tüm equity curve'ün peak-to-trough kaybı.
  5. Kümülatif sermaye eğrisi büyük erimeleri ve pratik uygulanabilirliği görünür kılar.
  6. Sistemler aynı koşullarda karşılaştırılmalı; derin ve uzun erimeli model elenmeli.
  7. Karmaşık metrikler basit equity-curve incelemesinin yerini almamalı.
  - Notun "net kâr / maksimum drawdown" oranına "ödül/risk" dendiğini söyler (Recovery Factor'a denk, not).
- Tanım: Madde 2 ve 4 formülleri standart (not). `beklenti = kazanma_oranı × ort_kazanç − kayıp_oranı × ort_kayıp − maliyet`. `MDD = min(equity / running_peak − 1)`. `getiri/|MDD|`.
- Parametreler: Eşik yok (kaç MDD fazla? Tansu söylemedi).
- Belirsiz kalanlar: "Derin ve uzun erimeli" eşiği. Karşılaştırma ölçütü (Sharpe mı, equity mi).
- Tansu'nun kanıtı: Yok (ilke).
- Bedava günlük veri: Evet.
- Kaynak güveni: İKİNCİ EL, yazar atfı belirsiz. Orta.

## K20. Probabilistik edge, fat tail, risk of ruin

- Kaynak: `tweet-probabilistik-edge-fat-tail-risk-of-ruin.md` (not).
- Tansu'nun ifadesi (İKİNCİ EL): Algoritma geliştiricilerin en büyük tuzağı fiyat yönünü kesin tahmin etmeye ve klasik indikatör parametrelerini geçmişe uydurmaya çalışmak. Gerçek edge: matematiksel modelleme, olasılık teorisi, beklenen değer ve işlem dizisi sonuçları. Normal dağılım yerine fat tail, skewness, kurtosis, black swan dayanıklılığı. Monte Carlo ile risk of ruin. İstatistiksel güven aralığı. Matematik non-random bileşenleri ayıklar.
- Tanım (kaynaktan): Parametre uydurma yasağı. Monte Carlo ile ruin olasılığı: işlem sonuç dağılımı (R katsayıları) yeniden örneklenir, belirlenen sermaye kaybı seviyesine ulaşma oranı hesaplanır (YORUM; Tansu yöntem vermedi).
- Parametreler: Ruin eşiği yok. Güven düzeyi yok (YORUM %95).
- Belirsiz kalanlar: Her şey sayısal.
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: İlke düzeyi. Notun plateau, nested walk-forward, deflated metrics önerileri Claude'a ait (YORUM).

## K21. Python ile doğrulama ve yanlışlama; Williams %R sonucu

- Kaynak: `tweet-python-finans-fikir-dogrulama-ve-yanlislama.md`, `tweet-williams-r-sma-swing-strateji-backtest.md` (not).
- Tansu'nun ifadesi (İKİNCİ EL): "Finans piyasalarında Python kullanmasının ana nedeni fikirleri ve piyasa iddialarını test edebilmek." İndikatör tavsiyelerini doğrudan parayla denemek yerine matematiksel modele ve backteste çevirmek. pandas/NumPy, backtesting ve objektif karar mekanizması.
- Williams notu: Kurallar "Kullanıcı kuralları" olarak yazılı (30 dk, Williams %R 14, SMA 14, hedef ≥2R). Kaynak türü `user-provided-strategy-spec`. Sonuçlar bizim projemizin backtesti (Yahoo, ~60 gün): maliyetli long-only PF 0,988; iki yönlü PF 0,587; short kolu sıfır maliyette bile PF 0,830. Bu bölüm Tansu'nun sonucu DEĞİL. Tansu kanıtı olarak kullanma.
- Tanım: Metot: fikir → denklem → nedensel sinyal → tarihsel simülasyon → maliyet/risk raporu → reddet veya sürdür.
- Parametreler: Yok.
- Tansu'nun kanıtı: Yok (ilke).
- Kaynak güveni: İKİNCİ EL. Williams sonuçları Tansu dışı.

## K22. Süreç ilkeleri: kitap sentezi, algoritma tasarımı, kendini yenileyen sistem, kağıt-kalem, 116

- Kaynak: T-kitap-model-sentezi, T-algoritma-tasarimi-temelleri, T-kendini-yenileyen-algoritma-ana-frekans, T-kagit-kalem-matematik-once-kod-sonra (hepsi not), G-116 (`assets/gorsel-paket-116-veriden-sinyale-algo-sureci/01-veriden-sinyale-algoritmik-trader-gelistirme.jpg`).
- Tansu'nun ifadesi:
  - G-116 (BİRİNCİ EL infografik, verbatim başlık): "Veriden Sinyale: Algoritmik Trader'ın Geliştirme Süreci". Dört adım: "1. Teknoloji ve Analitik Araçlar: Sürecin temeli Python ve veri analitiği araçları ile atılır." "2. Otomasyon ve Modelleme: Teknik analiz göstergeleri ve istatistiksel modeller Borsa İstanbul için otomatikleştirilir." "3. Geriye Dönük Test (Backtest): Geliştirilen sistemlerin başarısı geçmiş veriler üzerinde titizlikle test edilir." "4. Optimizasyon ve Sinyal Tasarımı: Risk/getiri oranı optimize edilmiş, kod tabanlı sinyal mekanizmaları tasarlanır."
  - T-kitap (İKİNCİ EL): Kitaplar vizyon geliştirir, fakat hazır modelleri aynen uygulamak başarı getirmez. Başarı farklı kaynaklardan öğrenilen modelleri sentezlemek, sonra sabırla backtest ve forward test yürütmek. Bilgiyi işleme, modele dönüştürme ve kod mimarisi asıl ayırıcı.
  - T-algoritma (İKİNCİ EL): Amaç açık olmalı. Zaman ve bellek verimli. İstatistik/ML doğru problemde. "Backtest gerçek maliyet ve likiditeyi içermeli." Risk kontrolleri ve beklenmedik durum planları. Tasarım-test-iyileştirme sürekli döngü. Birkaç satırlık yüzeysel kod orta-uzun vadede risk.
  - T-kendini-yenileyen (İKİNCİ EL): Sistem her döngüde güçlenen, verinin ince katmanlarını işleyen olmalı; "ana frekans" araması; hata payını azaltan, kendini yenileyen matematiksel yapı.
  - T-kagit-kalem (İKİNCİ EL; notun kendisi "kaynak kimliği doğrulanmamış" ve "kullanıcı kuralı değil" der): Detaylı model varsa önce kâğıt üzerinde matematiksel çöz, sonra koda dök.
- Tanım: Süreç sırası: veri → model (denklem) → backtest (maliyet+likidite dahil) → forward test → optimizasyon/sinyal tasarımı.
- Parametreler: Yok. Forward test süresi yok.
- Belirsiz kalanlar: Forward test uzunluğu. "Ana frekans" bir yöntem mi, metafor mu belirsiz.
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: G-116 BİRİNCİ EL (genel). Notlar İKİNCİ EL. Kâğıt-kalem notu düşük.

## K23. Kesinlik dili, 5 kapı ve R/R eşiği

- Kaynak: T-piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi, T-yuksek-ihtimalli-gunluk-islem-bes-kapi (not).
- Tansu'nun ifadesi (İKİNCİ EL):
  - Kesinlik: "kesin gidecek/uçacak/tavan" söylemi kaçma sinyali; olasılık, risk-ödül, koşul ve invalidation dili profesyonel yaklaşım.
  - 5 kapı: aktif volatilite, sinyal uyumu/confluence, pozitif momentum, ana trend yönü, uygun risk/ödül. "Yükselen trendde yalnız alım, düşen trendde yalnız satış." "Kabul eşiği örnek: 1:2 veya 1:3 risk/ödül." "Stop Loss seviyesi her zaman bu orana göre belirlenmeli."
- Tanım: `R/R = (hedef − giriş) / (giriş − stop) ≥ 2` (veya 3).
- Parametreler: R/R 1:2 veya 1:3 (not, ikinci el). Volatilite, momentum formülleri yok.
- YORUM: bizim sıra seçimimiz önce teknik geçersizlik stopu, sonra R/R hesabı ve yetersiz işlemi reddetmektir. Günlük işlem metni ile Gartley farklı bağlamlardır; bu sıra bütün sistemler için Tansu kuralı değildir, genel uygulanma kapsamı açık değildir (Aktarım, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:48–49; G123:42–49).
- Tansu'nun kanıtı: G-109'un R/R'si (0,20-0,32) bu eşiğin altında kalır (K11). Tansu bunu kendi paylaştığı çıktıda açıklamıyor.
- Bedava günlük veri: Evet.
- Kaynak güveni: İKİNCİ EL. Orta.

## K24. Başarı ölçütleri ve başarısızlık örnekleri: ML isabet, scorecard, stat-arb, 118

- Kaynak: T-ml-trade-13-gun-9-isabet (`assets/tweet-ml-trade-13-gun-9-isabet/01-ml-trade-hit-rate.png`), G-59 (`assets/gorsel-paket-59-risk-scorecard/01-buyhold-sinyal-stratejisi-risk-scorecard.png`), G-53 (`assets/gorsel-paket-53-stat-arb-bag-kopusu/01-statarb-negatif-backtest-bag-kopusu.jpg`), G-118 (`assets/gorsel-paket-118-yatirimci-basarisizlik-kontrol/01-yatirimcilar-neden-basarisiz-olur.jpg`).
- Tansu'nun ifadesi:
  - ML (not, İKİNCİ EL): ML ile trade yaklaşımını sevmediğini, modeli ara sıra incelediğini, finans için %70 doğruluğu yüksek gördüğünü belirtti. Görsel (BİRİNCİ EL, verbatim): "Toplam sinyal üretilen gün : 14; AL sinyali : 1; SAT sinyali : 13; Sonucu bilinen gün sayısı : 13; Tutarlı (Hit) : 9; Tutarsız (Miss) : 4; Tutarlılık Oranı (Hit Rate): 69.23%". 9/13 = 69,23% (doğrulandı). Wilson %95 aralığı ≈ 42-87% (benim hesabım, 13 örnek). 13/14 sinyal SAT: baz oran etkisi (piyasa düşüyorsa isabet modelden gelmez, YORUM).
  - G-59 (BİRİNCİ EL; metin: "Buy & Hold (B&H) vs Sinyal Bazlı Strateji"): Toplam getiri +%21.54 / +%14.74. Yıllık volatilite %33.16 / %23.21 ("Strateji, oynaklığı ~%30 azaltmış"). Max Drawdown −%2.46 / −%1.72 ("Kayıp yönetimi çok daha başarılı"). Sharpe 9.477 / 9.477 ("Risk başına düşen getiri başabaş"). Yorum sütunu: "B&H ham getiride önde." Not (İKİNCİ EL): bu tablonun "ham getiriden feragat karşılığında daha huzurlu eğri" gösterdiğini belirtti. Benim kontrolüm: 23,21/33,16 = 0,700 ve 1,72/2,46 = 0,699: risk ölçeği ≈ %70. Getiri korunumu 14,74/21,54 = %68,4. Sharpe aynı: dönem ve risksiz faiz verilmediği için doğrulanamaz (getiri/vol oranları 0,635 vs 0,650).
  - G-53 (BİRİNCİ EL grafik): "2) Portföy Performansı (TL)", "Buy & Hold (Başlangıç 100,000 ₺)" ve "Stat-Arb Stratejisi". Stat-arb ~100k'dan ~79k'ya düşer, uzun yatay; B&H ~105k'de biter. Tansu açıklaması (not, İKİNCİ EL, tırnaklı): "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım; görünmez bağ kopmuş olabilir."
  - G-118 (BİRİNCİ EL infografik, verbatim): "Yatırımcılar Neden Başarısız Olur?" Üç aile, dokuz madde: Bilgi ve Hazırlık Eksikliği (Ticaret Planının Olmaması: "Sağlam bir metodoloji olmadan, anlık kararlarla işlem yaparlar."; Yetersiz Bilgi; Uzman Desteği Aramamak). Disiplin ve Psikoloji (Duygusal Kararlar; Hatalardan Ders Almamak; Plana Sadık Kalmamak). Sermaye ve Risk Yönetimi Zafiyeti (Yetersiz Sermaye: "Küçük sermaye genellikle para kaybeder ve kaldıraç riskini anlamazlar."; Zayıf Para Yönetimi; "'Zarar Durdur' Emri Kullanmamak: Bu, küçük bir kaybı büyük bir kayba dönüştüren bir numaralı yoldur.").
- Tanım: Sonuç raporunda isabet, sinyal dağılımı, örneklem büyüklüğü ve baz oran birlikte raporlanır. Strateji, B&H ile risk ve çekilme bazında kıyaslanır. Negatif sonuç saklanmaz.
- Parametreler: ML için eşik %70 "yüksek" (Tansu'nun yargısı, not). Başka eşik yok.
- Belirsiz kalanlar: G-59'da dönem, rf, işlem maliyeti, strateji kuralı, zaman-piyasada oranı yok. ML'de label tanımı ve dönem yok.
- Tansu'nun kanıtı: Küçük örneklem (13), seçilmiş pencere (G-53, G-59).
- Bedava günlük veri: Evet.
- Kaynak güveni: Görseller BİRİNCİ EL (yüksek). Yorumlar İKİNCİ EL.

---

# EK A. Kapsam dışı ama ilgili (yalnız not başlıklarından; görsel açılmadı, İKİNCİ EL)

| not | Tansu'nun çıkış/stop sözü (not özeti) |
|---|---|
| G-105 BOS Fibonacci golden zone | Stop Fib 1,0 / impuls swing low altı. TP1 = Fib 0,0 (eski tepe). İleri hedef negatif Fib uzantısı. |
| G-107 BRYAT Elliott dalga 2 | Giriş FVG üst bandı veya Fib 0,618 limit. Stop Point0 altı. TP1 = Point1. TP2 = C + 1,618 × Wave1. Bilanço öncesi risk uyarısı. |
| G-106 demand EMA squeeze | Stop demand altı kapanış. TP1 üst supply bölgesi. |
| G-113 BIST-VIX 5 adım (görsel okundu, BİRİNCİ EL infografik) | Adım 5: "Pozisyondan çıkış kararı VIX'e göre değil, doğrudan BIST 100 fiyat grafiğinden belirlenir (örneğin Fiyat < SMA 20 veya Heikin Ashi kırmızıya dönmesi)." Alarm: "Fiyat, SMA 20'nin altına inerse VE YA AYNI ZAMANDA VIX RSI kendi ortalamasını yukarı keserse ... çıkış stratejisi değerlendirilmelidir." G-114 notu "4 göstergeden 2'si" der (not; infografikte yok). |

---

# (a) Tansu risk ve çıkış paketi: onun anlattığı biçim

Bu paket yalnız Tansu'nun söylediklerini birleştirir. Her boşluk etiketli.

| # | adım | Tansu'nun söylediği | etiket |
|---|---|---|---|
| 1 | Evren/likidite | ETF ve likit hisse. Sığ hisse yok. | İKİNCİ EL; eşik YORUM |
| 2 | Piyasa izni | Tansu'nun fikri şokta yeni alımı durdurmaktır (Aktarım, tweet-volatilite-piyasa-soku-yeni-alim-freni:21); uygulanamaz: kaynak hesaplanabilir tanım vermiyor. | İKİNCİ EL |
| 3 | Hisse rejimi | G48 olayında pozisyon kapanır; Tam/Defansif genel üretim koşulu açık değil | İKİNCİ EL (Aktarım, G48:21); 0,0 çizgisi GÖRSEL, 1/0 çarpan seçimi YORUM |
| 4 | Giriş | Setup bazlı (Bölüm 2). Kırılım+FVG+retest+teyit veya D'de limit. | kural eşiği YORUM |
| 5 | İlk stop | Giriş − 2 ATR (harmonikte X veya XA 1,13 veya X − 2 ATR) | BİRİNCİ EL (infografik, tablo) |
| 6 | Lot | %1 sermaye / (2 ATR mesafesi), paylaşılan örnek | BİRİNCİ EL (NotebookLM, G115/g1); genel risk oranı ve yuvarlama YORUM |
| 7 | Acil çıkış | Gün içinde stopa temas = anında kapat | BİRİNCİ EL (infografik) |
| 8 | Gün sonu çıkış | Kapanış SMA250 altı = çık (SMA200/EMA200/EMA250 alternatif) | BİRİNCİ EL + not |
| 9 | Kısmi kâr | Excel (G-123): TP1'de %50 sat. TP2'de kalanı sat. G125: ilk satışta "%10". İkinci satışın ayrıntıları belirtilmemiş. | Excel BİRİNCİ EL; G125 İKİNCİ EL (Aktarım, G125:20); "%10" anlamı ve %50 paydası belirsiz |
| 10 | Hedef | CD/AD geri alımı 0,382/0,618/C/1,272; SAYAS: TP1 = 1:1, TP2 = 0,618 AD; kırılım formasyonu: derinlik kadar | BİRİNCİ EL seviyeler |
| 11 | Stop taşıma | TP1 sonrası stop entry'ye (G-109 notu); trailing +1,5 ATR sonrası aktif | İKİNCİ EL; formül YORUM |
| 12 | Önceki gün dibi | Aktivasyon geçildikten sonraki barlarda ilk kapanış < önceki gün Low: %50 satış sinyali | İKİNCİ EL (Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20); payda açık değil |
| 13 | Geçersizlik | A ihlali ve ilk Close < zone_low yapı geçersizliğidir; reaksiyon pencereleri ayrı alanlardır | İKİNCİ EL (Aktarım, tweet-abcd-geometrik-gecerlilik-kurallari:21; G13:21); A fiyat alanı ve 10 gün/20 bar ortak politikası açık değil |
| 14 | Min R/R | 1:2 veya 1:3 (günlük setup); Gartley bağlamından ayrı | İKİNCİ EL; genel stop/R:R sırası YORUM (Aktarım, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:48–49; G123:42–49) |
| 15 | Günlük | aday → giriş → gerekçe → invalidation → TP → sonuç → MFE/MAE | İKİNCİ EL (URL'li tweet) |

Eksik (Tansu söylemedi), hepsi YORUM ile doldurulmalı ve YORUM etiketli kalmalı:

1. ATR periyodu ve yumuşatma türü (Wilder, SMA, EMA) ve zaman dilimi.
2. Stop kontrolü gün içi Low ile mi, kapanışla mı (acil: gün içi; SMA250: kapanış; harmonik: belirtilmedi).
3. Boşlukta dolum modeli (açılış/stop fiyatı).
4. Aynı gün stop ve hedef çatışması.
5. Birden fazla açık pozisyonda toplam risk sınırı ve korelasyon.
6. TP1 "%10" kimliği; TP2 miktarı; %50 paydası.
7. Trailing aktivasyonunun High/Close bazı, ATR zamanı ve dolum ayrıntıları (Chandelier k çarpanı kaynak kuralı değildir).
8. Hedef için sabit ATR çarpanı yok. GLOSSARY'deki "4 ATR hedef" bizim kararımız.
9. EMA50 çıkışı kaynak kuralı değildir. NotebookLM örneği SMA250 altında kapanışta çıkışı gösterir; ortalama seçimi okura aittir (Aktarım, G115:20; NotebookLM, g1). Projenin gün sonu stopu ile harmonik bozulma ayrıdır.
10. Zaman stopu: Tansu'da yalnız "tepki penceresi" (10 gün/20 bar) var; pozisyon zaman stopu yok.
11. Komisyon ve kayma varsayımı.
12. Short taraf için hiçbir ATR kuralı verilmedi (yalnız not "short için tersi").
13. Açık noktalar: (i) TP1 AD×0,382 (eğitim) ve 1:1 R/R (SAYAS) için genel seçim. (ii) Stop/R:R sırasının strateji kapsamı. (iii) Fırsat anlatısı işlem tetiği veya şok frenine istisna vermez. (iv) 10 gün ile 20 barın ortak politikası.

Bizim kanıt kapımız: Bu paketin hiçbir parçası için Tansu'nun gerçek işlem sonucu veya tam örneklemli backtest'i yok. Yalnız tek hisse, seçilmiş örnekler (SMRTG 7/10, ISKPL 5/5, GUBRF, BALAT, AKFIS) ve ML 9/13 var.

# (b) Tansu'nun değerlendirme ilkeleri: bizim backtest için kontrol listesi

Kaynak numaraları ilgili K bölümleridir. Hepsi İKİNCİ EL, aksi belirtilmedikçe.

Grup 1. Ölçüm (K19)
- [ ] Kazanma oranını tek ölçüt yapma. Beklenti (R cinsinden), payoff ve profit factor raporla.
- [ ] Net kâr ve maksimum drawdown'u birlikte oku. MDD tüm equity eğrisinin zirveden dibe kaybıdır.
- [ ] Kümülatif sermaye eğrisini çiz ve incele (derinlik, süre, düz dönemler).
- [ ] Sistemleri aynı koşulda kıyasla (evren, dönem, maliyet, risk düzeyi). Derin ve uzun erimeli modeli ele.
- [ ] Karmaşık metrik (Sharpe vb.) eğri incelemesinin yerine geçmez.

Grup 2. Adaylar ve filtreler (K18)
- [ ] Her adayı 1, 3 ve 5 işlem günü sonrası ölç (gün tanımı: işlem günü, YORUM).
- [ ] Filtre ablation: her filtreyi tek tek çıkar, katkıyı ölç. Katkısız filtreyi at.
- [ ] Retest beklemenin etkisini ölç (getiri ve girişin gecikmesi).
- [ ] Giriş oluşmayan adayları da tut (YORUM, notun Cevo sentezi).
- [ ] İşlem günlüğü alanlarını doldur: aday tarihi, giriş, gerekçe, invalidation, TP, sonuç, MFE, MAE.

Grup 3. Risk (K1-K5, K23, G-118)
- [ ] Lot stop mesafesinden hesaplanır; %1 / 2 ATR paylaşılan NotebookLM örneğidir, genel risk oranı seçimi YORUM'dur (NotebookLM, G115/g1).
- [ ] Aileye özgü çıkış ve risk yöntemini raporla. YORUM: bu kontrol listesinde ayrı stop kullanımı aranır; rotasyon grafiği genel stop politikasını açıklamaz (Aktarım, G125:20; Araç, Rota/g2; Eğitim, G118/g1).
- [ ] Planlanan kayıp ve gerçekleşen kaybı kıyasla (boşluk etkisi).
- [ ] YORUM: bizim sıra seçimimiz teknik geçersizlik stopu, sonra R/R 1:2 veya 1:3 kapısıdır; bütün sistemlerde ortak Tansu sırası açık değildir (Aktarım, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:48–49; G123:42–49).
- [ ] Plana sadakat: kural dışı çıkış/giriş yok.

Grup 4. Doğruluk ve baz oran (K24, K20)
- [ ] Küçük örneklemde güven aralığı ver (13 örnek = %42-87 gibi).
- [ ] Baz oran ve sinyal dağılımı raporla (13/14 SAT örneği).
- [ ] Strateji sonucunu B&H ile aynı risk düzeyinde kıyasla (G-59).
- [ ] Negatif sonucu yayımla (G-53: bağ kopabilir; "her fırsat çalışmaz").
- [ ] Parametreyi geçmişe uydurma. Fat tail ve ruin için Monte Carlo (yöntem YORUM).

Grup 5. Süreç (K21, K22)
- [ ] Önce denklem, sonra kod (kâğıt-kalem notu düşük güven).
- [ ] Backtest maliyet ve likiditeyi içerir (K22, K10).
- [ ] Backtestten sonra forward test (süre belirtilmedi).
- [ ] Fikri parayla değil kodla yanlışla (K21). Kural reddedilirse nedenini yaz (örnek: Williams short kolu, bizim sonucumuz).

Grup 6. Dil (K23)
- [ ] Çıktıda kesinlik dili yok: koşul, olasılık, invalidation, risk/ödül.

Bir sonraki küçük adım: K1-K3'ü (ATR periyodu 14 Wilder YORUM) günlük BIST verisinde tek bir kural olarak kodla ve planlanan ile gerçekleşen kayıp farkını ölç.
