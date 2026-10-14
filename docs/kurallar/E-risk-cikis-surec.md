# E. Risk, çıkış ve süreç kuralları (Tansu kaynaklı)

Hazırlanma: 2026-10-05. Yalnız okuma araştırması. Hiçbir parametre uydurulmadı. Boşluklar YORUM etiketiyle işaretli.

## 0. Nasıl okunur

Kaynak kökü: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`. Görseller `assets\<klasör>\` altında. Kısaltma: G = gorsel-paket, T = tweet-, K = kaynak-.

Kaynak türü ve YORUM tanımları GLOSSARY'dedir. Bu dosyada etiketler BİRİNCİ EL, NOTEBOOKLM (ikinci el sayılır), İKİNCİ EL ve YORUM olarak yazılır; notlardaki "Levent ... belirtti" cümleleri aktarılan metnin özetidir.

Uyarı 1: Notlarda "Levent" sözcüğü aktarılan tweet metnini anlatan kişiyi gösterir. Çoğu notta tweet URL'si yok. Yazarın Tansu olduğu havuz bağlamından gelir. Havuz ana notu "Levent'in X paylaşımlarından derlediği" der. Yani yazar atfı çoğu not için doğrulanmış değil. Tek istisna: `not-backtest-giris-sadeligi-risk-islem-gunlugu.md` (URL: x.com/The_Tansu_/status/2095213493133713664, 2 Eylül 2026) ve K-akfis (3 Eylül 2026).

Uyarı 2: `T-atr-risk-butcesi-position-sizing-stop-loss` için `assets` klasörü yok. Yalnız metin ve bir Python satırı var. Hepsi İKİNCİ EL.

Uyarı 3: Notlardaki "Cevo katkısı", "Cevo düzeltmesi", test fixture, state machine ve "kanonik" bölümleri Tansu'ya ait değil. Bunları Tansu ifadesi olarak kullanma.

Uyarı 4: 05.10 ön denemesi "4 ATR hedef" ve "kapanış EMA50 altı bozulma" kullandı; bu kaynaklarda ikisi de yok. Tansu'nun 2 ATR stopu var. Güncel karar: hedef yok, gün sonu stopu SMA250 (YORUM); sahip TASARIM §5.5, KURALLAR §1 madde 4. Aşağıdaki "4 ATR hedef" ve "EMA50" anmaları bu eski ön denemeyi gösterir. (bilet 04, 14.10)

---

# BÖLÜM 1. Pozisyon büyüklüğü ve stoplar

## K1. Risk bütçesi ve lot hesabı (%1 / 2 ATR)

- Kaynak: G-115 (`assets/gorsel-paket-115-position-sizing-1pct-2atr-sma250/01-position-sizing-yuzde1-2atr-sma250-stop.jpg`), T-atr-risk-butcesi (not), T-volatilite-ters-orantili (not).
- Tansu'nun ifadesi:
  - Görsel, verbatim (NOTEBOOKLM, ikinci el): "Risk Tutarınızı Belirleyin: Toplam sermayenizin en fazla %1'ini kaybetmeyi göze alın." "Hisse Adedini Hesaplayın: Belirlediğiniz risk tutarını, hissenin 2 ATR (Ortalama Gerçek Aralık) değerine bölün." "Örnek Hesaplama: 100.000$ sermaye ve 14.30$ 2 ATR için: 1.000$ / 14.30$ = ~70 hisse."
  - G-115 notu (İKİNCİ EL, paraphrase): SMA250 yerine SMA200, EMA200 veya EMA250 seçilebilir. İşlemde kaç lot alınacağını bilmek yatırımcılığın en önemli konularından biridir.
  - T-atr notu (İKİNCİ EL, paraphrase): "Hayat kalitesini bozmayacak sermaye", işlem başına TL risk bütçesi. Örnek: "Göze alınan kayıp 500 TL / 2 ATR değeri 2 TL = 250 lot". Python satırı: `Close[-1] - 2*ATR[-1]`.
  - T-volatilite-ters-orantili (İKİNCİ EL): Volatilitesi yüksek hissede pozisyon büyüklüğü küçülür. Ana amaç sermayeyi korumak. "Uygun zamanda oyuna zaten girilir."
- Tanım (günlük OHLCV ile hesaplanabilir):
  1. `risk_tutarı = sermaye × 0,01`.
  2. `stop_mesafesi = 2 × ATR` (hisse başına, fiyat birimi).
  3. `lot_ham = risk_tutarı / stop_mesafesi`.
   4. Lot = tam sayı. Aşağı yuvarlama YORUM'dur; yaklaşık 70 hisse paylaşılan NotebookLM örneğidir, yuvarlama talimatı yoktur (NotebookLM, G115/g1, örnek hesap). 1000/14,30 = 69,93; 70 × 14,30 = 1001 > %1.
  5. Görsel metni "2 ATR değeri" der. 14,30 = 2 ATR mesafesi okunur (NOTEBOOKLM). T-atr örneğinde "2 TL" için aynı okuma doğru olursa 250 lot. ATR = 2 TL olsaydı 125 lot olurdu. Metin 250 diyor. Yani payda = 2×ATR mesafesi (görselde açık, T-atr'de çıkarım).
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
- Kaynak güveni: Formül NOTEBOOKLM (ikinci el). Örnek kullanım "gerçek Tansu işlemi" değil. ATR detayı yok. Orta.

## K2. Acil stop (giriş − 2 ATR, gün içi anında çıkış)

- Kaynak: G-115 (NotebookLM görseli), G-125 (`assets/gorsel-paket-125-kismi-kar-trailing-stop/01-kismi-kar-trailing-prev-low-emergency-stop.jpg`), T-atr (not). Acil Stop ve Gün Sonu Stop adları aktarılan metinde vardır (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Tansu'nun ifadesi:
  - Görsel G-115, verbatim (NOTEBOOKLM, ikinci el): "Acil Durum Stop'u: Giriş fiyatının 2 ATR değeri kadar altına bir stop noktası koyun." "Anında Çıkış Kuralı: Fiyat gün içinde acil durum stop seviyesine düşerse, anında pozisyonu kapatın."
  - G-125 notu (İKİNCİ EL, paraphrase): "2ATR emergency stop ile kalan tüm pozisyonun kapatılması".
  - G-125 görsel (BİRİNCİ EL): Sol uçta kırmızı kutu etiketi "STOP" ve "ATR" satırları. Bilet 04 (14.10) görseli açıp büyüterek inceledi (dosya: `assets/gorsel-paket-125-kismi-kar-trailing-stop/01-kismi-kar-trailing-prev-low-emergency-stop.jpg`, 680×147 piksel; etiket yazısı yaklaşık 3 piksel yüksekliğinde). Rakamlar **okunamaz**: önceki iki okuma çelişir ("184.54 / 4.62" bu dosyada ve havuz notunda; "104.34 / 4.62" taslak M ve taslak parçalarında), ikisi de doğrulanamaz. Hiçbir kural bu sayıya dayanmaz. Bu çelişkinin tek kaydı burasıdır; başka dosyalar sayı yazmaz, buraya atıf verir. (bilet 04, 14.10; yazıcı kararı)
  - T-atr notu (İKİNCİ EL): "İlk stop fiyatın 2 ATR altı, acil stop intraday temasla".
- Tanım:
  1. Giriş günü: `stop = giriş_fiyatı − 2 × ATR` (ATR giriş kararında bilinen son tamamlanmış değer, YORUM).
  2. Her gün: `Low ≤ stop` ise çık (gün içi temas).
  3. Gün düşüğü stopun altındaysa dolum fiyatı TASARIM 5.3'tedir; kaynak boşlukta dolumu açıklamaz (YORUM).
  4. Aynı gün hem stop hem hedef değerse stop önce (YORUM, muhafazakâr).
   5. YORUM: bizim seçimimiz giriş ATR'si değişse bile stopu sabit tutmaktır. Aktarım giriş−2ATR ile güncel Close−2ATR'yi birlikte verir; başlangıç stopu ile güncelleme politikası ayrımı açık değildir (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| çarpan | 2 ATR | görsel G-115, not G-125 |
| tetik | gün içi temas, anında çıkış | görsel G-115 |
| etiket örneği | "STOP" ve "ATR" etiketi var; rakamlar okunamaz (yukarıdaki G-125 görsel maddesi) | görsel G-125 |
| ATR periyodu | yok | YORUM (14) |
| ATR sabit mi, hareketli mi | kaynak genel güncelleme politikası vermiyor | YORUM: girişte sabit bizim seçimimiz; başlangıç/güncelleme ayrımı belirsiz (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22) |
| tetik fiyatı: Low mu, son işlem mi | yok | YORUM (günlük Low) |
| boşlukta dolum | yok | YORUM (TASARIM 5.3) |
| stop fiyatına limit emir mi, piyasa emri mi | yok | YORUM (piyasa) |

- Belirsiz kalanlar: G-125 etiketindeki stop sayısı giriş − 2×ATR midir? Rakamlar okunamadığı ve giriş fiyatı grafikte okunmadığı için sınanamaz. G-125 etiketi soldadır, yani giriş anında yazılmış stop gibi görünür; bunu doğrulayan metin yok. Stop long için yazılmış; short için Tansu bir şey demedi.
- Tansu'nun kanıtı: Yok (kural anlatımı). G-125 grafiği seçilmiş tek örnek.
- Bedava günlük veriyle uygulanabilir mi: Evet, günlük High/Low ile. Gün içi sıra bilinmediği için aynı gün stop+hedef çatışması çözülemez (stop önce varsayımı). Projede Open yoktur (TASARIM 5.1); açılış boşluğu TASARIM 5.3'te AOF ile modellenir.
- Kaynak güveni: Kural NOTEBOOKLM (ikinci el). Orta-yüksek. Uygulama ayrıntıları yok.

## K3. Gün sonu (kapanış) stopu: SMA250

- Kaynak: G-115 (NotebookLM görseli), T-atr (not). Gün Sonu Stop adı aktarılan Tansu metnindedir (Aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22).
- Tansu'nun ifadesi: NotebookLM örneği SMA250 altında kapanışta çıkışı gösterir (NotebookLM, G115/g1). Aktarımda ortalama seçimi okura bırakılır (Aktarım, G115:20); SMA200, EMA200, EMA250 alternatifleri vardır. YORUM: SMA250'yi kesin giriş filtresi olarak seçmek bizim kararıdır; giriş karşılaştırması kaynakta yoktur.
- Tanım:
  1. Her gün kapanışında `Close < SMA250` ise çıkış sinyali.
  2. Çıkış zamanı ve fiyatı TASARIM 5.5'tedir (YORUM). Tansu "gün sonu" der; kapanışta emir mi, ertesi gün mü belirtmedi.
  3. K2 acil stop bundan bağımsız ve önceliklidir (YORUM; infografik iki kuralı yan yana verir, öncelik sırasını yazmaz).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| ortalama | SMA 250 gün | görsel G-115 |
| alternatifler | SMA200, EMA200, EMA250 | not G-115 |
| tetik | kapanış < ortalama | görsel G-115 |
| tampon/histerezis | yok | YORUM (0) |
| çıkış zamanı | yok | YORUM (TASARIM 5.5) |
| fiyat bazı: düzeltilmiş mi, ham mı | yok | YORUM (düzeltilmiş) |

- Belirsiz kalanlar: Seçim kuralı (hangi ortalama?). Giriş de SMA250 üstü mü gerektirir (not: giriş bileşenlerinden biri; geri kalan bileşenler verilmedi). 250 gün veri yoksa ne olacak (YORUM: sinyal yok).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet. 250 gün geçmiş gerekir (yeni halka arzlar elenir).
- Kaynak güveni: Kural NOTEBOOKLM (ikinci el). Orta-yüksek.

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
- Görsel (BİRİNCİ EL): Kırmızı oklar ve sarı yıldız işaretleri. Fiyat/tarih/TP seviyesi yazısı yok. Yalnız bir STOP / ATR etiketi vardır; rakamları okunamaz (K2, G-125 görsel maddesi).
- Tanım (kaynakta olan iskelet):
  1. Giriş.
  2. TP1: "%10" (anlamı belirsiz, aşağıda).
  3. TP2 (ikinci satış): ayrıntıları belirtilmemiş.
  4. Fiyat ≥ giriş + 1,5 ATR: trailing aktif (K4).
   5. Aktivasyon geçildikten sonraki barlardan ilk `Close[t] < Low[t−1]` kapanışında %50 satış sinyali oluşur (Aktarım, tweet-statik-dinamik-iz-suren-stop-atr:20); kısmi satışın dolumu YORUM'dur; TASARIM kısmi kârı ve iz süren stopu erteledi (TASARIM 5.5, "İz süren stop ve kısmi kâr" maddesi, :373).
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
- RSI 30 girişi ve iki aşamalı çıkış (`tweet-rsi30-giris-iki-asamali-cikis`; Ham Tansu'nun metni, ikinci el özet; grafik notta yok; bilet 04, 14.10): giriş: RSI(14) 30'un altından yukarı kesip üzerinde kapanış yapar. Kâr alma: RSI(14) 70'in üzerindeyken 70'in altında kapanırsa (RSI 70 reddi) pozisyonun %50'si satılır; kalan %50, bir önceki günün low'unun altında kapanışta satılır ve işlem biter. Tansu'nun cümlesi: "Üst paneldeki mumlar sırası ile giriş noktası, trailling noktası, ilk %50 kar aldığımız RSI70 reddi ve ikinci %50 kar aldığımız önceki mumun en düşüğünün altında kapanış." Parametre: RSI(14), 30, 70, %50 + %50 (not). Belirsiz: başlangıç ("sıkı") stop yok; "risk/ödül hedefi" ile "SMA 50 / RSI 50 dirençleri" ilişkisi belli değil; trailing noktası tanımsız; backtest yok. K5 ile fark: K5'te önceki gün dibi altı kapanış ilk %50'yi satar ve kalanı 2 ATR acil stop kapatır; bu notta aynı kapanış kalan %50'yi (tam çıkışı) satar, ilk %50'yi RSI 70 reddi satar. İkisi ayrı Tansu notudur; çözülmedi, K5 değişmedi.

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

- Sahibi: B §8 (gp-48 görsel okuması, çarpan değerleri, serilerin kimliği, gözlem). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk yönünden okuma: Tansu'nun çarpan fikri vardır, hesaplanabilir tanımı yoktur; kural olarak uygulanamaz.

## K8. Volatilite şok freni (yeni alım yok)

- Kaynak: T-volatilite-piyasa-soku-yeni-alim-freni (not; URL yok).
- Tansu'nun fikri, oynaklık şokunda yeni alımı durdurup mevcut riski yönetmektir (Aktarım, tweet-volatilite-piyasa-soku-yeni-alim-freni:21); uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- Tanım: `oran = std(getiri, son X gün) / std(getiri, son ~21 gün)`. `oran ≥ eşik` ise şok. Şokta yeni giriş yok. (X, pencere, eşik hepsi YORUM; notta formül Claude'a ait.)
- Parametreler: X yok. "Bir ay" = ~21 işlem günü (YORUM). Eşik yok. Çıkış/bekleme süresi yok.
- Belirsiz kalanlar: Piyasa şoku endeks düzeyinde mi, hisse bazında mı (not ayırır, Tansu demedi). Kısa pencere aylık pencerenin içinde (örtüşme).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: İlke İKİNCİ EL. Parametre yok.
- Not: 05.10 ön denemesindeki "Piyasa Nabzı BEKLE günü yeni giriş yok" bu ilkeye benzerdi ama eşiği Tansu vermedi. Güncel karar: piyasa durumu girişi durdurmaz, yalnız etiket olarak gösterilir (TASARIM §3, §6; bilet 04, 14.10).

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
- Tanım: Eşik yok. Notun `quantity_liquidity` kuralı Claude'a ait (YORUM). Sektör rotasyonu bağlamında Tansu'nun hacim filtresi örnekleri: sahibi D, "Hacim filtresi". (bilet 04, 14.10)
- Parametreler: Yok (ADV, spread, katılım oranı verilmedi).
- Belirsiz kalanlar: "Likit" tanımı, hangi ETF'ler (BIST'te sınırlı).
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Kısmen. Günlük hacim ve TL hacmi var. Spread ve derinlik yok (G-126 order book ayrı kaynak, kapsam dışı).
- Kaynak güveni: İlke, İKİNCİ EL.

---

# BÖLÜM 2. Kâr alma, çıkış, geçersizlik

## K11. Harmonik hedef merdiveni (BALAT, CD geri alımı)

- Sahibi: C §11 (kaynak G-109, TP merdiveni, doğrulama, parametreler, belirsizlikler). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: kısmi kâr, stop taşıma ve stop seçimi ikinci el ve genel kural değildir (C §11). R/R eşiği K23'tedir.

## K12. Gartley takip tablosu: stop ve TP1/TP2 (G-123) ve SAYAS aracı

- Sahibi: C §7 (G-123 tablosu, SAYAS, iki ayrı TP1 tanımı, stop seçenekleri, SAYAS doğrulaması). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: tek genel TP1 ve tek genel stop seçimi yoktur (C §7); Gartley girişinin R/R eşiği C §7'dedir (K23 günlük işlem 5 kapısıdır).

## K13. Kırılım, FVG, retest, teyit kartı (AKFIS): ENTRY, STOP, TP1-3

- Sahibi: A §1 (görsel etiketleri, piksel okumaları, parametreler). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: stop ve TP kuralları tamamen belirsizdir (A §1).

## K14. Fincan-kulp hedef ve R/R (GUBRF)

- Sahibi: B §21 (görsel etiketleri, hedef formülü, R/R doğrulaması). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: hedef formülü vardır; stop ve giriş fiyatı yoktur (B §21).

## K15. Durum etiketleri ve geçersizlik (AKTİF, TAMAMLANDI, TEPKİ_VERDİ, BOZULDU, TAMAM, belirsiz)

- Sahipleri: C §2 (durum etiketleri ve anlamları), C §3 (AB=CD geçerlilik kuralları, BOZULDU kriteri), C §5 (SMRTG ve ISKPL sonuçları), C §10 (D sonrası tepki penceresi: 10 gün ve 20 bar). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: etiketler formasyon durumudur, işlem sonucu değildir; BOZULDU etiketinden işlem stop fiyatı çıkmaz.

## K16. Demand bölgesi geçersizliği (TTKOM)

- Sahibi: A §9 (zone_low kuralı, Close ve Low seçenekleri, parametreler); TTKOM alt tablosu A §6'dadır. Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: bozulma kuralı stop mantığına bağlanabilir; Tansu bir stop fiyatı vermez.

## K17. Retest bekle (AKSGY)

- Sahibi: A §12 (AKSGY başlığı, temas sayısı, Tansu'nun yorumu, parametreler). Burada tekrar edilmez. (bilet 04, 14.10)
- Risk/çıkış yönünden okuma: Tansu'nun fikri retest ve hacim teyidi aramaktır; çıkış için uygulanamaz, kaynak hesaplanabilir tanım vermiyor (Aktarım, G103:21).

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
  - Ek paylaşım (`kaynak-tansu-2095201144544846208`, 2 Eylül 2026, 20:24, not özeti): "Analize indikatörün AL sinyaliyle başlanmıyor." İnceleme sırası: bölge → kırılımlar → likidite hareketleri → 4 saatlik teyit.
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
  - G-116 (NOTEBOOKLM, ikinci el, verbatim başlık): "Veriden Sinyale: Algoritmik Trader'ın Geliştirme Süreci". Dört adım: "1. Teknoloji ve Analitik Araçlar: Sürecin temeli Python ve veri analitiği araçları ile atılır." "2. Otomasyon ve Modelleme: Teknik analiz göstergeleri ve istatistiksel modeller Borsa İstanbul için otomatikleştirilir." "3. Geriye Dönük Test (Backtest): Geliştirilen sistemlerin başarısı geçmiş veriler üzerinde titizlikle test edilir." "4. Optimizasyon ve Sinyal Tasarımı: Risk/getiri oranı optimize edilmiş, kod tabanlı sinyal mekanizmaları tasarlanır."
  - T-kitap (İKİNCİ EL): Kitaplar vizyon geliştirir, fakat hazır modelleri aynen uygulamak başarı getirmez. Başarı farklı kaynaklardan öğrenilen modelleri sentezlemek, sonra sabırla backtest ve forward test yürütmek. Bilgiyi işleme, modele dönüştürme ve kod mimarisi asıl ayırıcı.
  - T-algoritma (İKİNCİ EL): Amaç açık olmalı. Zaman ve bellek verimli. İstatistik/ML doğru problemde. "Backtest gerçek maliyet ve likiditeyi içermeli." Risk kontrolleri ve beklenmedik durum planları. Tasarım-test-iyileştirme sürekli döngü. Birkaç satırlık yüzeysel kod orta-uzun vadede risk.
  - T-kendini-yenileyen (İKİNCİ EL): Sistem her döngüde güçlenen, verinin ince katmanlarını işleyen olmalı; "ana frekans" araması; hata payını azaltan, kendini yenileyen matematiksel yapı.
  - T-kagit-kalem (İKİNCİ EL; notun kendisi "kaynak kimliği doğrulanmamış" ve "kullanıcı kuralı değil" der): Detaylı model varsa önce kâğıt üzerinde matematiksel çöz, sonra koda dök.
- Tanım: Süreç sırası: veri → model (denklem) → backtest (maliyet+likidite dahil) → forward test → optimizasyon/sinyal tasarımı.
- Parametreler: Yok. Forward test süresi yok.
- Belirsiz kalanlar: Forward test uzunluğu. "Ana frekans" bir yöntem mi, metafor mu belirsiz.
- Tansu'nun kanıtı: Yok.
- Bedava günlük veri: Evet.
- Kaynak güveni: G-116 NOTEBOOKLM (ikinci el; genel). Notlar İKİNCİ EL. Kâğıt-kalem notu düşük.

## K23. Kesinlik dili, 5 kapı ve R/R eşiği

- Kaynak: T-piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi, T-yuksek-ihtimalli-gunluk-islem-bes-kapi (not).
- Tansu'nun ifadesi (İKİNCİ EL):
  - Kesinlik: "kesin gidecek/uçacak/tavan" söylemi kaçma sinyali; olasılık, risk-ödül, koşul ve invalidation dili profesyonel yaklaşım.
  - 5 kapı ve kabul eşiği örneği: sahibi B §20. (bilet 04, 14.10)
- Tanım: `R/R = (hedef − giriş) / (giriş − stop)`; eşik B §20'dedir.
- Parametreler: R/R eşiği ve beş kapının ölçüleri B §20'dedir.
- YORUM: bizim sıra seçimimiz önce teknik geçersizlik stopu, sonra R/R hesabı ve yetersiz işlemi reddetmektir. Günlük işlem metni ile Gartley farklı bağlamlardır (Gartley için R/R eşiği C §7); bu sıra bütün sistemler için Tansu kuralı değildir, genel uygulanma kapsamı açık değildir (Aktarım, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:48–49; G123:42–49).
- Tansu'nun kanıtı: G-109'un R/R'si (0,20-0,32) bu eşiğin altında kalır (C §11). Tansu bunu kendi paylaştığı çıktıda açıklamıyor.
- Bedava günlük veri: Evet.
- Kaynak güveni: İKİNCİ EL. Orta.

## K24. Başarı ölçütleri ve başarısızlık örnekleri: ML isabet, scorecard, stat-arb, 118

- Kaynak: T-ml-trade-13-gun-9-isabet (`assets/tweet-ml-trade-13-gun-9-isabet/01-ml-trade-hit-rate.png`), G-59 (`assets/gorsel-paket-59-risk-scorecard/01-buyhold-sinyal-stratejisi-risk-scorecard.png`), G-53 (`assets/gorsel-paket-53-stat-arb-bag-kopusu/01-statarb-negatif-backtest-bag-kopusu.jpg`), G-118 (`assets/gorsel-paket-118-yatirimci-basarisizlik-kontrol/01-yatirimcilar-neden-basarisiz-olur.jpg`).
- Tansu'nun ifadesi:
  - ML (not, İKİNCİ EL): ML ile trade yaklaşımını sevmediğini, modeli ara sıra incelediğini, finans için %70 doğruluğu yüksek gördüğünü belirtti. Görsel (BİRİNCİ EL, verbatim): "Toplam sinyal üretilen gün : 14; AL sinyali : 1; SAT sinyali : 13; Sonucu bilinen gün sayısı : 13; Tutarlı (Hit) : 9; Tutarsız (Miss) : 4; Tutarlılık Oranı (Hit Rate): 69.23%". 9/13 = 69,23% (doğrulandı). Wilson %95 aralığı ≈ 42-87% (benim hesabım, 13 örnek). 13/14 sinyal SAT: baz oran etkisi (piyasa düşüyorsa isabet modelden gelmez, YORUM).
  - G-59 (B&H ile sinyal bazlı strateji scorecard): sahibi D, "B&H vs sinyal bazlı strateji scorecard" bölümü. Burada tekrar edilmez. (bilet 04, 14.10)
  - G-53 (bağı kopan stat-arb çifti, negatif örnek): sahibi D, "Tansu'nun kanıtı" (AGROT/GARAN, madde c). Tansu'nun açıklaması (not, İKİNCİ EL, tırnaklı): "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım; görünmez bağ kopmuş olabilir."
  - G-118 (NOTEBOOKLM, ikinci el, verbatim): "Yatırımcılar Neden Başarısız Olur?" Üç aile, dokuz madde: Bilgi ve Hazırlık Eksikliği (Ticaret Planının Olmaması: "Sağlam bir metodoloji olmadan, anlık kararlarla işlem yaparlar."; Yetersiz Bilgi; Uzman Desteği Aramamak). Disiplin ve Psikoloji (Duygusal Kararlar; Hatalardan Ders Almamak; Plana Sadık Kalmamak). Sermaye ve Risk Yönetimi Zafiyeti (Yetersiz Sermaye: "Küçük sermaye genellikle para kaybeder ve kaldıraç riskini anlamazlar."; Zayıf Para Yönetimi; "'Zarar Durdur' Emri Kullanmamak: Bu, küçük bir kaybı büyük bir kayba dönüştüren bir numaralı yoldur.").
- Tanım: Sonuç raporunda isabet, sinyal dağılımı, örneklem büyüklüğü ve baz oran birlikte raporlanır. Strateji, B&H ile risk ve çekilme bazında kıyaslanır. Negatif sonuç saklanmaz.
- Parametreler: ML için eşik %70 "yüksek" (Tansu'nun yargısı, not). Başka eşik yok.
- Belirsiz kalanlar: G-59'da dönem, rf, işlem maliyeti, strateji kuralı, zaman-piyasada oranı yok. ML'de label tanımı ve dönem yok.
- Tansu'nun kanıtı: Küçük örneklem (13), seçilmiş pencere (G-53, G-59).
- Lojistik regresyon filtresi ve R/R koşulu (`gorsel-paket-129-doas-lojistik-regresyon-hacim-rsi-filtreli-strateji`; Ham Tansu'nun metni, görsel birinci el; bilet 04, 14.10): hacim ve RSI verisiyle lojistik regresyon modeli; doğruluk %55,00, kesinlik %55,31, duyarlılık %45,44; Tansu: finansal piyasada %70 harika, %90 mümkün değil; modeli "yeni yazılmış, üzerinde hiç çalışılmamış" diye anlatır. Kural cümlesi (birebir): "%55 başarı oranıyla para kazanmak için, her işlemde Risk/Ödül oranını en az 1:1.5 (örneğin %2 Stop, %3 Kar Al) olarak ayarlamak gerekir." Görsel: `DOAS.IS - ML + Hacim + RSI Filtreli Strateji`; EMA 21, RSI paneli (30, 70 çizgileri, "Trend Ayrımı (50)"), "SAT" ve "Güçlü AL (Vol+RSI)" işaretleri; doğruluk sayıları görselde yok, özellik ve hedef değişken tanımı yok, örneklem dışı doğrulama yok. R/R ≥ 1:1,5 eşiği K23'teki 1:2 veya 1:3 eşiğinden farklıdır; bağlamlar ayrı (K23 günlük işlem 5 kapısı, bu not ML isabet oranı); çözülmedi, K23 değişmedi.
- Bedava günlük veri: Evet.
- Kaynak güveni: G-118 NOTEBOOKLM (ikinci el); diğer görseller BİRİNCİ EL (yüksek). Yorumlar İKİNCİ EL.

---

# EK A. Kapsam dışı ama ilgili: çıkış ve stop sözü olan notlar

Çıkış ve stop sözleri sahibi dosyadadır; burada yalnız nereye bakılacağı yazılır. (bilet 04, 14.10)

| not | Sahibi |
|---|---|
| G-105 BOS Fibonacci golden zone | A §10 |
| G-107 BRYAT Elliott dalga 2 | C §16 |
| G-106 demand EMA squeeze | B §3 |
| G-113 BIST-VIX 5 adım (çıkış adımı ve alarm) | D, "BIST VIX long: 5 adım kontrol listesi" |

---

# (a) Tansu risk ve çıkış paketi: onun anlattığı biçim

Bu paket yalnız Tansu'nun söylediklerini birleştirir. Her boşluk etiketli.

| # | adım | Sahibi | etiket |
|---|---|---|---|
| 1 | Evren/likidite | K10 | İKİNCİ EL; eşik YORUM |
| 2 | Piyasa izni | K8 | İKİNCİ EL; uygulanamaz |
| 3 | Hisse rejimi | B §8 | İKİNCİ EL; çarpan eşlemesi YORUM |
| 4 | Giriş | A §1; C §7 | kural eşiği YORUM |
| 5 | İlk stop | K2; C §7 | K2: NOTEBOOKLM (ikinci el) |
| 6 | Lot | K1 | NOTEBOOKLM (ikinci el); genel risk oranı ve yuvarlama YORUM |
| 7 | Acil çıkış | K2 | NOTEBOOKLM (ikinci el) |
| 8 | Gün sonu çıkış | K3 | NOTEBOOKLM (ikinci el) ve not |
| 9 | Kısmi kâr | K5; C §7 | İKİNCİ EL; "%10" anlamı ve %50 paydası belirsiz |
| 10 | Hedef | C §4, §7, §11; B §21 | seviyeler formasyona göre |
| 11 | Stop taşıma | K4; C §11 | İKİNCİ EL; formül YORUM |
| 12 | Önceki gün dibi | K4, K5 | İKİNCİ EL; payda açık değil |
| 13 | Geçersizlik | C §3, §10; A §9 | İKİNCİ EL; ortak politika açık değil |
| 14 | Min R/R | K23; B §20 | İKİNCİ EL; genel stop/R:R sırası YORUM |
| 15 | Günlük | K18 | İKİNCİ EL (URL'li tweet) |

Eksik (Tansu söylemedi), hepsi YORUM ile doldurulmalı ve YORUM etiketli kalmalı:

1. ATR periyodu ve yumuşatma türü (Wilder, SMA, EMA) ve zaman dilimi.
2. Stop kontrolü gün içi Low ile mi, kapanışla mı (acil: gün içi; SMA250: kapanış; harmonik: belirtilmedi).
3. Boşlukta dolum modeli (açılış/stop fiyatı).
4. Aynı gün stop ve hedef çatışması.
5. Birden fazla açık pozisyonda toplam risk sınırı ve korelasyon.
6. TP1 "%10" kimliği; TP2 miktarı; %50 paydası.
7. Trailing aktivasyonunun High/Close bazı, ATR zamanı ve dolum ayrıntıları (Chandelier k çarpanı kaynak kuralı değildir).
8. Hedef için sabit ATR çarpanı yok. "4 ATR hedef" 05.10 ön denemesinin kararıydı; kaldırıldı, güncel karar: hedef yok (TASARIM §5.5; bilet 04, 14.10).
9. EMA50 çıkışı kaynak kuralı değildir (05.10 ön denemesinin kararıydı; kaldırıldı). NotebookLM örneği SMA250 altında kapanışta çıkışı gösterir; ortalama seçimi okura aittir (Aktarım, G115:20; NotebookLM, g1). Projenin gün sonu stopu ile harmonik bozulma ayrıdır.
10. Zaman stopu: Tansu'da yalnız "tepki penceresi" (10 gün/20 bar) var; pozisyon zaman stopu yok.
11. Komisyon ve kayma varsayımı.
12. Short taraf için hiçbir ATR kuralı verilmedi (yalnız not "short için tersi").
13. Açık noktalar: (i) TP1 AD×0,382 (eğitim) ve 1:1 R/R (SAYAS) için genel seçim. (ii) Stop/R:R sırasının strateji kapsamı. (iii) Fırsat anlatısı işlem tetiği veya şok frenine istisna vermez. (iv) 10 gün ile 20 barın ortak politikası.

Bizim kanıt kapımız: Bu paketin hiçbir parçası için Tansu'nun gerçek işlem sonucu veya tam örneklemli backtest'i yok. Yalnız tek hisse ve seçilmiş örnekler var (sonuç sayıları sahibinde: C §7 ve ilgili bölümler).

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
- [ ] Aileye özgü çıkış ve risk yöntemini raporla. YORUM: bu kontrol listesinde ayrı stop kullanımı aranır; rotasyon grafiği genel stop politikasını açıklamaz (Aktarım, G125:20; Araç, Rota/g2; Eğitim, G118/g1). İstisna: seçilmiş çift rotasyonu bölmesi stopsuzdur, çıkışı karşı uçta geçiştir (TASARIM §5.5–5.6; KURALLAR §3); bu madde o bölmeye uygulanmaz. (bilet 04, 14.10)
- [ ] Planlanan kayıp ve gerçekleşen kaybı kıyasla (boşluk etkisi).
- [ ] YORUM: bizim sıra seçimimiz teknik geçersizlik stopu, sonra R/R kapısıdır (eşik B §20); bütün sistemlerde ortak Tansu sırası açık değildir (Aktarım, tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi:48–49; G123:42–49).
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

Uygulama sırası ve durumu: TASARIM §7 (K1–K3 tamamlandı).
