# A. Yapı / Bölge GİRİŞ kuralları — Tansu kaynaklı çıkarım

Not: Havuz = `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`. Görseller `assets\<klasör>\` altında. Görsel = birinci el (Tansu aracının çıktısı). Not = ikinci el (Claude özeti). "YORUM" = kaynakta yok, bizim doldurduğumuz boşluk.

Genel bulgu: Tansu hiçbir görselde veya notta bir kuralın tam parametre setini, giriş zamanını, stop formülünü veya sistematik backtest sonucunu vermiyor. Görseller seçilmiş örneklerdir. Aşağıdaki "Tanım" bölümlerinde görselde olan şeyler ile YORUM olan şeyler ayrı işaretlendi.

---

## 1. Breakout + Range Retest (+ FVG %50) A+ Setup (AKFIS)
- Kaynak: `kaynak-akfis-breakout-fvg-retest-2095523694881697974.md`; `assets\kaynak-akfis-...\akfis.webp` (birinci el), `alinti-ornek.webp` (sembolsüz, 2 Eylül gönderisinin görseli; farklı araç/tema, "CONSOLIDATION / BREAKOUT / BULLISH FVG / RETEST / CONFIRMATION / AL" etiketleri).
- Tansu'nun ifadesi (görsel başlığı, verbatim): `AKFIS | Breakout + Range Retest + RSI Divergence | A+ SETUP | AL TETİKLENDİ | Sınıf: A+ | Skor: 100/100`. Lejant: `AKFIS, Hacim, VolMA20, RSI 14, Range High / Retest, Range Low, FVG %50, AL, ENTRY, STOP, TP1, TP2, TP3`. Grafikteki etiketler: `KONSOLİDASYON`, `BREAKOUT`, `BULLISH FVG + CONFLUENCE`, `RANGE HIGH RETEST`, `CONFIRMATION`, `AL`. Tweet metni (not): Breakout -> FVG -> Retest -> Confirmation sırası (ikinci el özet).
- Tanım (görselden okunan sıra):
  1. Yatay kutu (konsolidasyon): üst sınır = "Range High / Retest" çizgisi, alt sınır = "Range Low". Görselde ~20 mumluk kutu; üst ~3.65, alt ~3.33 (okunan yaklaşık değer, kesin değil).
  2. Breakout: tek bir büyük yeşil mum Range High üzerine kapanır (görselde gövde kutunun üstüne taşıyor).
  3. Bullish FVG: breakout mumu çevresinde yeşil boşluk alanı; Range High ile çakışıyor ("FVG + CONFLUENCE"). Lejantta "FVG %50" = FVG orta çizgisi (noktalı yeşil çizgi).
  4. Retest: breakout sonrası fiyat birkaç mumda Range High / FVG alanına geri döner ("RANGE HIGH RETEST" etiketi; fiyat alanın içinde/üstünde kalır).
  5. Confirmation: retest sonrası ilk yeşil mum ("CONFIRMATION"); üstünde "AL" üçgeni. ENTRY çizgisi (yeşil yatay) AL mumunun üzerinde ~3.73; STOP (kırmızı kesikli) Range High/FVG alanının hemen altında ~3.62; TP1/TP2/TP3 (turuncu/mavi kesikli) ~3.87 / ~3.93 / ~4.0. (Değerler piksel okuması.)
  6. Skor/sınıf: "A+" ve "100/100" bir puan formülünden geliyor; formül verilmemiş.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Konsolidasyon süresi / yükseklik | bilinmiyor (görselde ~20 mum, ~%9 yükseklik) | görsel (yaklaşık), kural YORUM |
| Breakout koşulu | close > Range High (gövde kutu üstünde) | görsel, eşik/tampon YORUM |
| FVG tanımı | 3 mum boşluk: `high[t−2] < low[t]`; orta = "FVG %50" | not (ikinci el; Aktarım, G107:47–48); orta çizgi görsel etiketi |
| Retest toleransı | bilinmiyor | YORUM |
| Confirmation koşulu | bilinmiyor (yeşil mum görünüyor) | YORUM |
| Entry | AL mumu üstü / yeşil çizgi | görsel; tam formül YORUM |
| Stop | Range High / FVG alt sınırı altı | YORUM: bizim stop seçimi; kaynak yalnız çizgi gösterir, formül ve temas/kapanış koşulu yok (Araç, AKFIS `01-akfis-retest-teyit.png`) |
| TP1-3 | 3 çizgi; R katı veya Fib olduğu belirtilmemiş | görsel; formül YORUM |
| Hacim | VolMA20 çiziliyor; teyit eşiği yok | görsel |
| RSI 14 divergence | başlıkta var; RSI paneli kırpımda görünmüyor | görsel (başlık) |
| Periyod | belirtilmemiş (grafikte günlük gibi, 4.5 TL altı fiyat) | YORUM |

- Giriş / stop / hedef / bozulma: yukarıda. YORUM: bozulma seçimi stop altında kapanıştır; kaynak stopun temas mı kapanış mı kullandığını açıklamaz (Araç, AKFIS `01-akfis-retest-teyit.png`).
- Belirsiz kalanlar: mum periyodu, konsolidasyon seçimi (pivot? sabit pencere?), FVG dolum kuralı, retest ve confirmation tanımı, puan formülü, RSI divergence kuralı, TP formülü, hacim şartı, maliyet.
- Alıntı örneğinin piksel okuması (E K13'ten buraya taşındı, bilet 04, 14.10; YORUM, yaklaşık, fiyat etiketi yok): sembolsüz, eksen 100–150; ENTRY ≈ 114,3; STOP ≈ 106,4 (FVG bandının hemen altı); range high ≈ 111,3; FVG ≈ 107,5–108,8; hedef çizgileri ≈ 120, ≈ 122, ≈ 130. Stop mesafesi ≈ 7,9; hedefler ≈ 0,7R, 1,0R, 2,0R. AKFIS ana görselinde çizgi renkleri lejantla eşleşmiyor (TP2/TP3 sırası tutarsız görünüyor).
- Tansu'nun kanıtı: yok. Tek seçilmiş örnek (yükseliş devam etmiş). 100/100 olasılık değildir (not da bunu söylüyor, ikinci el).
- Günlük bedava veriyle uygulanabilir mi: Evet, tanımlanabilir (günlük OHLCV yeter) ama birçok parametre YORUM ile doldurulmalı. Kural iskeleti net; parametre uydurma gerekir.
- Kaynak güveni: görsel orta (etiketler birinci el), parametre düşük.

---

## 2. Yükselen Kanal Alt Bant Teması (AEFES)
- Kaynak: `kaynak-aefes-yukselen-kanal-alt-bant-2096582181170598078.md`; `assets\kaynak-aefes-...\aefes-kanal.webp`.
- Tansu'nun ifadesi (görsel, verbatim): başlık `AEFES — YÜKSELEN KANAL — ALT BANT TEMAS`; alt satır `Lookback: 120 | Temas: 2026-09-03 | Alt bant: 17.76 | Low: 17.92 | Low-Bant: +0.92% | Kapanış-Bant: +2.56% | Üst/Alt temas: 3/3 | Genişlik değişimi: +15.3% | ALT BANT TEMAS + TEPKİ`. Lejant: Fiyat, Üst Sınır, Alt Sınır, Alt Bant Temas, Hacim, Hacim MA21, RSI 14, MACD Hist/MACD/Signal, +DI, -DI.
- Tanım (görselden):
  1. Son 120 mum (Lookback 120) içinde yükselen iki paralel kesikli çizgi: Üst Sınır ve Alt Sınır. Alt sınır ~16.0 (ilk dip) -> ~18.0 (son bar); üst sınır ~21.3 -> ~23.5.
  2. "Üst/Alt temas: 3/3": üst sınıra 3, alt sınıra 3 temas sayıldı (temas tanımı bilinmiyor).
  3. "Genişlik değişimi +15.3%": kanal genişliğinin bir başlangıç değerine göre değişimi (formül bilinmiyor; YORUM: son genişlik / ilk genişlik - 1).
  4. Sinyal günü (2026-09-03): Low = 17.92, alt bant = 17.76. Low-Bant = (Low - Alt bant)/Alt bant = +%0.92 (hesap: 17.92/17.76-1 = 0.90%, görsel 0.92; küçük fark yuvarlama/bant değeri farkı, doğrulanamadı). Kapanış-Bant = +%2.56 => kapanış ~18.21.
  5. "TEPKİ": son mumlar yeşil, alt banttan yukarı dönüş.
  6. Giriş/stop/hedef YOK.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Lookback | 120 (mum sayısı; periyod belirtilmemiş, grafik günlük görünümlü) | görsel |
| Temas eşiği | Low alt bandın üstünde +%0.92 iken "temas" sayıldı; max tolerans bilinmiyor | görsel (örnek), eşik YORUM |
| Min temas | 3/3 gösteriliyor; zorunlu mu bilinmiyor | görsel; YORUM |
| Kanal kurma | trend çizgisinde swing pivotları ikili bağlama; arada çizgi delinmez | not (ikinci el; Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21–27); pivot tespiti ve kanal üretimi açık |
| Tepki koşulu | belirtilmemiş | YORUM |
| Genişlik filtresi | "Genişlik değişimi" gösteriliyor, eşik yok | görsel |
| Paralellik | iki çizgi yaklaşık paralel | görsel |

- Giriş / stop / hedef / bozulma: verilmemiş. Bozulma YORUM: kapanış alt bandın altında.
- Belirsiz kalanlar: kanal algoritması, temas toleransı, genişlik tanımı, tepki tanımı, çıkış.
- Tansu'nun kanıtı: yok (tek örnek, sonuç gösterilmemiş).
- Günlük bedava veriyle uygulanabilir mi: Evet (120 günlük pencere). Trend çizgisinin ana yöntemi pivot eşleştirmesidir; arada çizgi delinmez (Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21–27). Kanal üretiminin ayrıntıları YORUM.
- Kaynak güveni: etiket/sayı birinci el; algoritma bilinmiyor.

---

## 3. "Düşen Direnci Kıran + Talep + Fibo + ABCD" tarayıcı çıktısı (LIDER, BALAT)
- Kaynak: `gorsel-paket-34-siyah-kugu-talep-run.md`, `gorsel-paket-45-balat-abcd-negatif-kumulatif-delta.md` (ikinci el); görseller `assets\gorsel-paket-34-...\01-lider-siyah-kugu-talep-run.png`, `assets\gorsel-paket-45-...\01-balat-abcd-negatif-kumulatif-delta.jpg` (birinci el, düşük çözünürlük 680 px).
- Tansu'nun ifadesi (görsel başlıkları, verbatim, küçük punto, okunabildiği kadar):
  - LIDER: `Düşen Direnci Kıran + Talep + Fibo + ABCD | Harmonik: Siyah Kuğu | Fiyat: 127.40 | Kırılım: 2026-05-18 | Temas: 3 | Lookback: 20`
  - BALAT: `Düşen Direnci Kıran + Talep + Fibo + ABCD | Fiyat: 75.95 | Kırılım: 2026-05-15 | Temas: 3 | Lookback: 30` (not 2026-05-19 diyor; görselde 05-15 okundu, çelişki)
  - Lejant: Fiyat, EMA5, EMA8, EMA13, "Direnç TL" (kırmızı çizgi), "Harmonik (Siyah Kuğu)", Hacim, "Küm. Delta". Fib seviyeleri 1.000/0.786/0.618/0.500/0.382/0.236/0.000 (BALAT: 99.45 / 94.00 / 89.73 / 86.72 / 83.72 / 80.01 / 74.00); `D(CD=1.27AB)`.
- Tanım (başlıktan çıkan): (a) düşen direnç trend çizgisi tepeler arasındadır; "Temas: 3" etiketi vardır; (b) "Kırılım" tarihtir; (c) Talep yeşil yatay kutudur; (d) Fibo tepe/dip arasında çizilir; (e) ABCD D'de tamamlanır. Lookback 20/30 etiketleri arama veya kırılım sonrası izleme süresini açıklamaz (Araç, G34/g1 ve G45/g1). YORUM: bu katalogda çizgi arama penceresi olarak okunur; değişken/otomatik seçim açıklaması doğrulanmış değildir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Temas sayısı | 3 (her iki örnekte) | görsel |
| Lookback | 20 (LIDER), 30 (BALAT) | görsel |
| Kırılım koşulu | kapanış trend çizgisini aşar | not (ikinci el; Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21); başka kırılım türlerine genellenmez |
| EMA | 5/8/13 | görsel (lejant) |
| ABCD oranı | CD=1.27AB (BALAT D etiketi) | görsel |
| Talep bölgesi tanımı | bilinmiyor | YORUM |
| Giriş/stop/hedef | yok | - |

- Önemli: BALAT görseli bir başarısızlık örneğidir. Tansu'nun yorumu (not, ikinci el): "ABCD'ye güvenip doğrudan alırsan böyle olursun; her zaman çalışmaz; ikinci alt grafiğe dikkat" (Küm. Delta uzun süre negatif). LIDER ise "Kuğuyu talep toplama bölgesinde yakalarsanız böyle RUN olur" (ikinci el yorum). Yani aynı başlıklı iki sinyalden biri başarılı biri başarısız gösterildi; Küm. Delta bir filtre olarak ima ediliyor ama eşik yok.
- Belirsiz kalanlar: çizgi kuran algoritma, talep bölgesi bağı, Lookback anlamı, Küm. Delta hesabı, "Siyah Kuğu" oranları. Gerçek işlem deltası günlük OHLCV'den çıkmaz; kaynak panelinin proxy olup olmadığı açık değildir (Araç, G45/g1, alt panel). YORUM: günlük proxy bizim seçimimizdir.
- Tansu'nun kanıtı: yok; biri seçilmiş pozitif, biri seçilmiş negatif.
- Günlük bedava veriyle uygulanabilir mi: Düşen direnç kırılımı + EMA5/8/13 + Fib + ABCD: evet (günlük). Küm. Delta paneli: hesabı belirsiz (Araç, G45/g1, alt panel); günlük proxy YORUM'dur. Siyah Kuğu: oranlar verilmemiş, kodlanamaz.
- Kaynak güveni: başlık değerleri birinci el ama düşük çözünürlük; kural düşük.

---

## 4. Düşen trend çizgisi kırılımı + talep + hacim + EMA5/8/13 (-64)
- Kaynak: `gorsel-paket-64-dusen-trend-talep-hacim-ema-breakout.md` (ikinci el); `assets\gorsel-paket-64-dusen-trend-hacim-breakout\01-dusen-trend-talep-hacim-ema-breakout.jpg`.
- Tansu'nun ifadesi: görselde yalnızca lejant `EMA 5 / EMA 8 / EMA 13 / Direnç TL`; sembol, başlık, tarih yok. Not (ikinci el, Levent aktarımı): "düşen trend kırılımı ve hacimli onay"; zincir: düşen direnç kırılımı + yeşil talep bölgesi + yüksek hacim + EMA 5/8/13 yukarı dönüşü + uzun yeşil, tepeye yakın kapanışlı mum; "Pazartesi bakalım".
- Tanım (görsel): fiyat geniş yeşil talep kutusunun (yatay) içinde/üstünde uzun süre taban yapıyor; kırmızı "Direnç TL" aşağı eğimli (tepelerden); son gün uzun yeşil mum çizgiyi yukarı kıran ve kapanış üst tarafa yakın; son hacim çubuğu görünür örneklemin en büyüğü; EMA5/8/13 sıkışık ve yukarı dönüyor.
- Parametreler: hepsi yok (EMA 5/8/13 dışında). Çizgi çapaları, talep kutusu sınırları, "yüksek hacim" eşiği, kapanış konumu eşiği: YORUM. Trend çizgisinde swing pivotları ikili bağlama ve arada delinmeme kaynaklıdır (Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21–27); pivot tespiti ve hacim formülleri YORUM'dur.
- Giriş / stop / hedef: yok. Bozulma: yok.
- Tansu'nun kanıtı: yok; sonuç bilinmiyor ("Pazartesi bakalım").
- Günlük veriyle: evet (OHLCV yeter).
- Kaynak güveni: düşük (başlıksız, sembolsüz görsel; kural dolaylı).

---

## 5. XU100 zone/yapı paneli ve SETUP puanı (kaynak-xu100-1-eylul, kaynak-xu100-bekle-teyit)
- Kaynak: `kaynak-xu100-1-eylul-2094850165920403866.md`, `kaynak-xu100-bekle-teyit-2095196517577461974.md`; görseller `assets\kaynak-xu100-1-eylul-...\gunluk.webp`, `4-saat.webp`; `assets\kaynak-xu100-bekle-teyit-...\gunluk.webp`, `4-saat.webp`.
- Tansu'nun ifadesi (başlık çubuğu, verbatim):
  - 1 Eylül günlük: `XU100.IS | GÜNLÜK 14229.01 | DEMAND: 4 | SUPPLY: 2 | BULL FVG AKTİF: 11 | BEAR FVG AKTİF: 2 | YAPI: GEÇİŞ / BULLISH CHoCH | SETUP: 45/100 | GÖRSEL: ODAK`
  - 1 Eylül 4 saat: `... 4 SAATLİK 14226.96 | DEMAND: 4 | SUPPLY: 2 | BULL FVG AKTİF: 12 | BEAR FVG AKTİF: 6 | YAPI: GEÇİŞ / BEARISH CHoCH | SETUP: 35/100`
  - 2 Eylül günlük: `... GÜNLÜK 14050.56 | DEMAND: 4 | SUPPLY: 2 | BULL FVG AKTİF: 11 | BEAR FVG AKTİF: 3 | SSL/BSL: 0/4 | YAPI: GEÇİŞ / BULLISH CHoCH SEVİYESİ KAYBEDİLDİ | SETUP: 7/100`
  - 2 Eylül 4 saat: `... 14054.50 | DEMAND: 4 | SUPPLY: 2 | BULL FVG AKTİF: 10 | BEAR FVG AKTİF: 8 | SSL/BSL: 1/0 | YAPI: GEÇİŞ / BEARISH CHoCH AKTİF | SETUP: 13/100`
  - Grafik etiketleri: `WMA Close 21`, `SUPPLY / ARZ 15133.50 - 15204.90`, `SUPPLY / ARZ 14734.50 - 14876.10`, `DEMAND / TOPLAMA 12966.30 - 13056.65`, `12601.60 - 12898.20`, `11102.20 - 11172.60` (günlük); 4 saat: `DEMAND / TOPLAMA 13833.00 - 13659.74`, `13216.16 - 13273.44`; `DÜŞEN TREND | TARİHSEL/KIRILMIŞ | TEMAS: 8`; `YÜKSELEN TREND | YENİ KIRILDI | TEMAS: 7`; HH/HL/LH/LL, BOS, CHoCH, SSL SWEEP, BSL SWEEP işaretleri; alt paneller MACD 12 26 9, RSI 14 | 70 / 30, WT 10 21 | 60 53 -53 -60.
- Tanım: Bu bir panel/özet, tek bir giriş kuralı değil. Sayaçlar: aktif demand/supply bölge sayısı, aktif bull/bear FVG sayısı, SSL/BSL (süpürülen likidite sayısı), yapı durumu (CHoCH), SETUP x/100 bileşik puan. Puan formülü verilmemiş. 1 Eylül günlük 45 -> 2 Eylül 7 (CHoCH seviyesi kaybedilince puan düşüyor): puanın yapı durumuna duyarlı olduğu gözlenir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| WMA | Close 21 (ağırlıklı hareketli ortalama) | görsel |
| MACD | 12/26/9 | görsel |
| RSI | 14, 70/30 | görsel |
| WaveTrend | 10, 21 (eşikler 60, 53, -53, -60) | görsel |
| Pivot/swing/ CHoCH/ FVG/ zone/ puan formülü | yok | YORUM |
| Trend çizgisi temas | düşen 8, yükselen 7 | görsel |

- Giriş / stop / hedef: yok. Tweet metni (not, ikinci el): WMA21 geri alma eşiği 14,443.45; ilk olumlu eşik ~14,722; bullish FVG kayıp eşiği 14,140.43; ana "bekle ve teyit" yaklaşımı. Sayısal kalıcılık şartı yok.
- Tansu'nun kanıtı: yok.
- Günlük veriyle uygulanabilir: yapı (swing, BOS/CHoCH), demand/supply, FVG sayımı: evet ama algoritma YORUM. SETUP puanı: formül yok, kopyalanamaz. 4 saatlik panel için günlük bedava veri yetmez.
- Kaynak güveni: görsel metni birinci el ve net; kural yok.

---

## 6. Zone gösterge tablosu: En Yakın Demand, D.Touch, D.Teyit, Supply, S.Touch, S.Teyit (-10, -11, -12, -13)
- Kaynak: `gorsel-paket-10-hktm-demand-supply.md`, `-11-froto-bos-choch.md`, `-12-doas-advance-block.md`, `-13-ttkom-demand-invalidation.md` (ikinci el); görseller `assets\gorsel-paket-10-...`, `-11-...`, `-12-...`, `-13-...` (birinci el, 680 px).
- Tansu'nun ifadesi: başlık `<SEMBOL> - Demand & Supply Bölgesi Analizi`; alt tablo kolonları `Son Fiyat | Max | Min | En Yakın Demand | D.Touch | D.Teyit | En Yakın Supply | S.Touch | S.Teyit` (TTKOM görselinde `Aktif Demand`, `Aktif Supply`). Okunan satırlar: DOAS `171.20 | 247.00 | 166.40 | 165.59-173.00 | 3 | 2025-11-04 | 200.90-209.91 | 2 | 2026-06-25`; TTKOM `54.50 | 75.85 | 47.48 | 49.05-51.30 | 0 | (teyit tarihi okunamadı) | 63.29-65.48 | 1 | ...`; FROTO `78.10 | ... | 73.05 | 74.70-76.70 | 1 | 2026-08-14 | 90.10-92.69 | 1 | 2026-06-30` (düşük çözünürlük, yaklaşık). HKTM görselinde tablo kolonları: Son Fiyat, Max, Min, En Yakın Demand, D.Touch, D.Teyit, En Yakın Supply, S.Touch, S.Teyit (aynı yapı, okunamayan değerler).
- Tanım (anlamlar Tansu tarafından açıklanmamış; çıkarım YORUM):
  - D.Touch / S.Touch = YORUM: bu katalogda fiyatın bölgeye temas sayısı olarak okunur; mum mu, ayrı ziyaret mi sayıldığı açık değildir (Araç, G10/g1 ve G12/g1, alt tablolar).
  - D.Teyit / S.Teyit = YORUM: bu katalogda bölgenin oluşum/onay tarihi olarak okunur; kaynak oluşum ile teyidi ayırmaz (Araç, G13/g1, alt tablo).
  - Bölgeler görselde: supply sarı/kırmızı kutu, demand mavi kutu, tüketilmiş/eski bölgeler gri. Gri kutu = geçmiş (kırılmış/kullanılmış) bölge (TTKOM'da gri kutu kırılım tarihinde bitiyor).
- Parametreler: temas tanımı, teyit tanımı, bölge oluşturma kuralı, bölge sayısı: yok (YORUM).
- Giriş / stop / hedef: yok.
- Tansu'nun kanıtı: yok (DOAS: sert yükselişin supply'da yorulduğu örnek; fiyat sonra demand'e düştü).
- Günlük veriyle uygulanabilir: bölge tespiti evet (kural 7-9'a bağlı); D.Touch/D.Teyit tanımı YORUM gerektirir.
- Kaynak güveni: tablo birinci el; semantik düşük.

---

## 7. Distal / Proximal çizgiler (-09)
- Kaynak: `gorsel-paket-09-distal-proximal-arz-talep.md`; `assets\gorsel-paket-09-distal-proximal\01-distal-proximal-arz-bolgesi.png` (İngilizce ders diyagramı, Tansu'nun aracı değil; Levent kaynak olarak iletmiş. Yazarı bilinmiyor).
- Tansu'nun ifadesi (görsel, verbatim): "The distal line is located at the highest of the basing structure while the proximal line is placed at the lowest body price of the base." Diyagram: yükselen mumlar, `Base`, sonra düşüş (rally-base-drop). `Distal line` = base'in en yükseği; `Proximal line` = base'teki en düşük gövde fiyatı.
- Tanım: arz bölgesi: distal = max(high[base]); proximal = min(min(open,close)[base]). Talepte proximal/giriş ve distal/stop ilişkisi eğitim şemasında vardır (Eğitim, G15/g1). YORUM: distal = min(low[base]), proximal = max(max(open,close)[base]); base veya leg-out seçiminin evrensel formülü verilmez.
- Parametreler: base seçimi (kaç mum, gövde/range oranı) YOK; YORUM.
- Giriş: proximal çizgi; stop = distal çizgi (Eğitim, G15/g1: giriş/proximal ve distal/stop ilişkisi).
- Tansu'nun kanıtı: yok. Günlük veriyle: evet. Kaynak güveni: diyagram net ama Tansu'ya atfı doğrulanmadı; tweet "distal/proximal çizgilerini anlamak işin yarısı, taramak diğer yarısı" (not, ikinci el).

---

## 8. RBR (Rally-Base-Rally) talep bölgesi (-15)
- Kaynak: `gorsel-paket-15-rbr-demand-zone.md`; `assets\gorsel-paket-15-rbr-demand-zone\01-rally-base-rally-rbr-pattern.png` (ders diyagramı, Tansu aracı değil).
- Tansu'nun ifadesi (görsel, verbatim): `RBR PATTERN`, `LEG IN CANDLE`, `BASE CANDLE`, `LEG OUT CANDLE`, `ENTRY POINT`, `Proximal line`, `Distal line / stop loss`; "NOTE: The area between proximal line and distal line is area of demand which is known as demand zone. DISTAL line always be at the low of base candle or leg out candle in RBR pattern."
- Tanım: yükselişte leg-in (yeşil büyük mum) -> 1+ küçük base mumu (renk önemli değil) -> leg-out (büyük yeşil). Eğitim şemasında proximal = giriş; distal = stop, base veya leg-out dibindedir (Eğitim, G15/g1). YORUM: proximal base üst gövde seviyesi civarı; distal base low veya leg-out low'un küçüğü; evrensel seçim formülü açık değildir.
- Parametreler: base mum sayısı, "küçük" gövde eşiği, leg-out büyüklüğü: yok (YORUM).
- Giriş / stop: görselde var (proximal/entry, distal/stop); hedef yok. Not'un base kapıları listesi Claude önerisidir.
- Kanıt yok. Günlük veriyle evet. Güven: diyagram birinci el ama genel eğitim materyali.

---

## 9. Talep bölgesi bozulması (invalidation) (-13)
- Kaynak: `gorsel-paket-13-ttkom-demand-invalidation.md`; TTKOM görseli.
- Tansu'nun ifadesi: tweet (not, ikinci el): demand bölgesinin en düşük fiyatı `zone_low`; oluşum sonrası ilk mum `close < zone_low` (veya daha katı: `low < zone_low`) ise kutu o tarihte biter. Görselde kırmızı ok, gri kutunun kırılım tarihinde bittiği yeri gösteriyor (birinci el).
- Tanım: oluşum sonrası ilk `Close < zone_low` mumunda kutu biter (Aktarım, G13:21). `Low < zone_low` daha katı ayrı seçenektir; aracın hangi seçeneği kullandığı açık değildir.
- Parametreler: buffer yok. YORUM: 0.
- Giriş/stop/hedef: yok (bozulma kuralı olarak stop mantığına doğrudan bağlanabilir). Kanıt yok. Günlük evet. Güven: orta.

---

## 10. BOS / CHoCH piyasa yapısı (-11) ve BOS + Fib Golden Zone (0.618-0.786) + FVG/OB (-105)
- Kaynak: `gorsel-paket-11-froto-bos-choch.md`, `gorsel-paket-105-bos-fibonacci-golden-zone-fvg-ob.md`; görsel `assets\gorsel-paket-105-...\01-bos-fibonacci-golden-zone-fvg-order-block.png`.
- Tansu'nun ifadesi: -11 tanımlar (tweet, ikinci el özet): BOS = trend yönünde önceki swing high/low kırılması; CHoCH = korunan HL/LH'nin ilk kaybı. -105 (tweet, ikinci el): "BOS Destekli Fibonacci Golden Zone Alım Stratejisi": bullish impulse -> önceki tepe üstü BOS -> HH -> swing low'dan swing high'a Fibonacci -> 0.618-0.786 OTE/Golden Zone -> FVG veya Order Block teması -> long; stop Fib 1.0 / swing low altı; TP1 Fib 0.0 (eski tepe); ileri hedef negatif Fib extension. Görsel (birinci el, 680x280): `BOS`, `HH` etiketleri; Fib seviyeleri `0.0: 216.77`, `0.236: 201.69`, `0.382: 191.32`, `0.5: 183.46`, `0.618: 175.60`, `0.786: 163.75`, `1.0: 150.15` (okunan yaklaşık); 0.618-0.786 arasında yeşil zone kutuları; kırmızı oklar: geri çekilme -> Golden Zone -> yeniden yükseliş.
- Tanım (adım adım):
  1. Swing low L -> yukarı impulse -> önceki swing high H0'ı kapanışla geçince BOS (yapı yükselen).
  2. Yeni tepe HH oluşur (swing high).
  3. Fib: L (1.0) ile HH (0.0) arası. Golden Zone = 0.618-0.786 retracement bandı (fiyat 0.0 -> 1.0 yönünde geri gelir).
  4. Fiyat bu banda girer ve band içinde FVG veya Order Block ile çakışma/temas yaşar -> long adayı.
  5. Stop = L (1.0) altı; TP1 = HH (0.0); sonraki = negatif extension.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Golden Zone | 0.618-0.786 | görsel (seviyeler) + tweet (not, ikinci el) |
| Stop | Fib 1.0 / impulse swing low altı; buffer yok | tweet (ikinci el); buffer YORUM |
| TP1 | Fib 0.0 (eski tepe) | tweet (ikinci el) |
| İleri hedef | negatif Fib extension; −0,27 hedef örneği | not (ikinci el; Aktarım, G105:48–55); genel oran seçimi YORUM |
| Swing pivot L/R, BOS tampon, FVG/OB tanımı | swing, BOS tamponu ve OB seçimi yok; bullish FVG: `high[t−2] < low[t]` | FVG: not (ikinci el; Aktarım, G107:47–48); diğer ayrıntılar YORUM |
| Periyod | bilinmiyor | - |

- Tansu'nun fikri, temas bölgesinde işlem aramaktır (Aktarım, G105:48–55); uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- Tansu'nun kanıtı: yok; seçilmiş pozitif tek örnek, başarısız adaylar yok.
- Günlük veriyle: evet. Güven: akış net, parametreler yok; tweet metni ikinci el, görsel doğrular seviyeleri.

---

## 11. Trend desteği (yükselen) + demand + FVG + BOS (GEDZA -93)
- Kaynak: `gorsel-paket-93-gedza-demand-bos-hacim-momentum.md`; `assets\gorsel-paket-93-...\01-gedza-trend-demand-fvg-bos-hacim.jpg`.
- Tansu'nun ifadesi (görsel başlık/lejant, verbatim): `GEDZA - Fiyat: 31.10`; lejant `EMA 3, EMA 13, Trend Destek, Temas, En Yakın Demand, En Yakın FVG, BOS` (Araç, G93/g1, sol üst lejant). Alt paneller Hacim, MACD, ADX, RSI.
- Tanım: yükselen "Trend Destek" çizgisi (cyan) iki+ pivot low'dan; fiyat sağ uçta çizgi ve yeşil "En Yakın Demand" kutusuna iniyor ("Temas" üçgeni), büyük yeşil tepki mumu, son hacim çubuğu çok yüksek; altta "En Yakın FVG" kutusu; yatay BOS çizgisi üstte.
- Parametreler: EMA 3/13 (Araç, G93/g1, sol üst lejant); ADX/RSI/MACD periyodu yok (YORUM); temas toleransı yok.
- Giriş/stop/hedef: yok. Kanıt: yok. Not'un "MACD negatif, ADX zayıf: karışık teyit" yorumu Claude'a ait. Günlük veriyle evet. Güven: düşük-orta.

---

## 12. Yükselen destek trendi RETEST + temas sayısı + EMA5/8/13 (AKSGY -103, -117)
- Kaynak: `gorsel-paket-103-aksgy-retest-macd-volume-failure.md`, `gorsel-paket-117-ema5-8-13-yukselen-trend-destek-tepki.md`; görseller `assets\gorsel-paket-103-...\01-aksgy-retest-macd-volume-failure.png`, `assets\gorsel-paket-117-...\01-ema5-8-13-yukselen-trend-destek-tepki.png`.
- Tansu'nun ifadesi (görsel başlığı, verbatim, -103): `AKSGY | EMA8 > EMA13 > EMA5 | ADX: 34.13 | RSI: 41.13 | MACD: -0.013 | RETEST VAR (6 kez) | İlk Temas: 2025-10-14 | Son Temas: 2025-12-08 | Temas Sonrası: 9 gün`. Lejant: Destek Trendi, EMA 5/8/13, Golden Cross, Son Temas, RETEST, ADX (Zayıf Trend, Güçlü Trend), RSI (Aşırı Alım/Satım). -117: lejant `Destek Trendi, EMA 5, EMA 8, EMA 13, Son Temas`; ADX 14 ve eşik 20 çizgisi; RSI 14; MACD "Alım Sinyali / Satım Sinyali" üçgenleri; başlık yok.
- Tanım: yükselen destek çizgisi (Destek Trendi) üzerinde "temas" günleri sayılıyor (AKSGY: 6 retest, ilk 2025-10-14, son 2025-12-08, son temastan 9 gün sonra bugün). EMA dizilimi tarayıcı filtresi/etiketidir (AKSGY'de EMA8>EMA13>EMA5 = bozuk dizilim; -117'de not EMA5>EMA8>EMA13 diyor, ikinci el, görselde okunamadı).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA | 5/8/13 | görsel |
| ADX | 14 periyot, 20 eşik (zayıf), ~40? güçlü eşik çizgisi var | görsel (-117 "ADX 20", -103 iki eşik çizgisi, değer okunamadı) |
| RSI | 14 | görsel |
| Temas toleransı, çizgi çapaları | değerler yok; trend çizgisinde swing pivotları ikili bağlama ve arada delinmeme | yöntem: not (ikinci el; Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21–27); sayısal ayrıntılar YORUM |
| "Temas Sonrası" | son temastan geçen gün (9) | görsel |

- Giriş/stop/hedef: yok. Tansu'nun yorumu (not, ikinci el): "Retest beklemek gerekir; AKSGY'de MACD toparlanması yanıltıcı oldu, hacim hareketi hiç desteklemedi" => seçilmiş başarısız örnek; son kırmızı mum destek altına sarkıyor. -117: "pozitif setup adayı" ama hacim zayıf, MACD negatif, ADX~20, RSI~50 (ikinci el yorum).
- Kanıt: yok (iki örnek: biri başarısız, biri belirsiz). Günlük veriyle evet. Güven: başlık birinci el; kural yok.

---

## 13. Fiyat konumu vs hacim konumu (-128)
- Kaynak: `gorsel-paket-128-fiyat-hacim-konum-proxy-cot-kalabalik-dip.md`; görseller `assets\gorsel-paket-128-fiyat-hacim-konum-proxy\01-fiyat-hacim-konum-scatter-rsi.png`, `02-secilmis-dip-sonrasi-fiyat-grafigi.png`.
- Tansu'nun ifadesi (görsel eksen etiketleri, verbatim): X `FİYAT KONUMU (%0 = Yıllık Dip, %100 = Yıllık Tepe)`; Y `HACİM/İLGİ KONUMU (%0 = Hacimsiz, %100 = Yoğun)`; renk `RSI Gücü` (20-80); sol üst yeşil kutu `DİP OLUŞUMU? (Yüksek Hacim, Düşük Fiyat)`; sağ üst kırmızı `AŞIRI ISINMA (Yüksek Hacim, Yüksek Fiyat)`; `SON GÜN`. Tweet (not, ikinci el): 252 günlük fiyat konumu + 252 günlük hacim konumu, yfinance verisiyle, COT verisi olmadığı için proxy.
- Tanım: fiyat_konumu = (kapanış - 252g min) / (252g max - 252g min) x 100. Hacim konumu benzer şekilde 252 gün içindeki hacmin yüzdelik/min-max konumu (hangisi olduğu belirtilmemiş, YORUM). Dip adayı: fiyat <~%20, hacim >~%80 (kutu sınırları görselden: x 0-20, y 80-100). Aşırı ısınma: x 80-100, y 80-100.
- Parametreler: pencere 252 (tweet, ikinci el); kutu sınırları ~%20/%80 (görselden kaba okuma); RSI periyodu bilinmiyor.
- Giriş/stop/hedef: yok. Kanıt: tek seçilmiş dip örneği (ok), sistematik yok. Günlük veriyle: evet, tam uygulanabilir (yalnızca OHLCV). Güven: eksen tanımı birinci el; hacim konumu formülü belirsiz.

---

## 14. Konsolidasyon kutusu sınırı (gövde/fitil) (-18) ve uzun yatay + kırılım ("Point A -> Point B") (-44, -41)
- Kaynak: `gorsel-paket-18-konsolidasyon-body-wick.md`, `gorsel-paket-44-basit-gizli-filtre-breakout-kesfi.md`, `gorsel-paket-41-konsolidasyon-suresi-kirilim-siddeti.md`; görseller `assets\gorsel-paket-18-...\01-konsolidasyon-body-wick-bolge.jpg` (TradingView ekran görüntüsü, mor kutular), `assets\gorsel-paket-44-...\01-point-a-b-gizli-filtre-breakout.png` (etiketler `Point A (Start)`, `Point B (Breakout)`), `assets\gorsel-paket-41-...\01-ok-konsolidasyon-suresi-kirilim-siddeti.png`.
- Tansu'nun ifadesi (tweet, ikinci el özet): -18: üst sınır = en yüksek mumun gövde ucu, alt sınır = en düşük mumun fitil ucu. -44: "hep göz önünde olan 1-2 filtreyle enteresan breakout sinyali var; yeni keşfettim" — filtreler açıklanmamış. -41: "okların bulunduğu alan yatayda ne kadar genişse (konsolidasyon uzunsa) kırılım o kadar şiddetli"; Levent/Tansu görseldeki kısa konsolidasyona rağmen güçlü kırılıma şaşırdığını söylüyor.
- Tanım: -18: zone_upper = max(open,close) of highest-high candle; zone_lower = min(low). -44/-41: uzun yatay kutu başlangıcı Point A, üst bandın aşıldığı Point B; -44'te sarı MA benzeri çizgi ve mavi noktalı trailing/zarf var (kimliği yok).
- Parametreler: tümü yok (filtre, süre, kutu yüksekliği); YORUM: süre ve ATR-normalize yükseklik.
- Giriş/stop/hedef: yok. Kanıt: seçilmiş; -41 hipotez ("uzun konsolidasyon -> güçlü kırılım") test edilmemiş. Günlük veriyle: evet (kural yazılabilir) ama gizli filtre kopyalanamaz. Güven: düşük.

---

## 15. Hafta yatay (80-100 hafta) + bant dibinde bekleme (kaynak-80-100-hafta-yatay)
- Kaynak: `kaynak-80-100-hafta-yatay-tarama-2096580811080261784.md`. Görsel yok.
- Tansu'nun ifadesi (not, ikinci el özet; tweet metni verbatim bu notta yok): 80-100 hafta yatay kalan hisseyi bulup alt bölgede beklemek "sade/temiz" strateji; taramasını yazma niyeti.
- Tanım (YORUM; kaynakta yok): haftalık kapanışta 80-100 hafta boyunca max/min aralığı dar (tepe/dip oranı eşiği), fiyat bandın alt %X'inde. Tansu eşik vermemiş.
- Parametreler: süre 80-100 hafta (tek parametre, not); eğim, bant genişliği, alt bölge eşiği, stop, çıkış: yok (YORUM).
- Kanıt: yok. Günlük veriyle: evet (haftalığa resample). Güven: düşük (tek cümlelik fikir).

---

## 16. Ikinci kademe (kısa kayıt): BOM, AHENK, FVG, çoklu zaman, MA filtre, retest
- BOM (`kaynak-bom-iki-tavan-2093647837162553475.md`, `assets\kaynak-bom-...\bom.webp`): görselde `BOM` işareti (siyah üçgen), `Kırılım 2026-06-18 (Temas:7)`, `Kırılım 2026-07-24 (Temas:5)` (turuncu trend çizgileri), CHoCH, hacim profili, kırmızı kutu içinde BOM sonrası yükseliş. Tweet (ikinci el): "uygun şartlarda art arda iki tavan". BOM formülü yok. Kural çıkarılamaz.
- AHENK (`kaynak-ahenk-demand-2094486927328059452.md`, `ahenk.webp`): `DEMAND / TOPLAMA` kutusu, mor WMA benzeri çizgi, MACD/RSI/WT panelleri. Tweet: "Ahengin uyumu"; kural yok.
- PRZMA -69 (`gorsel-paket-69-...md`, `01-przma-bullish-fvg-bos-ema.jpg`): başlık `PRZMA | Fiyat: 17.70 | Price Action & Smart Money Analysis`, EMA 9/21/50/100/200, yeşil FVG kutuları. Tweet (ikinci el): FVG upper-bound ilk teması alarm adayı; doğrudan long yerine 1H/4H CHoCH bekle. Sayısal kural yok.
- AVOD -101: başlık `AVOD | Fiyat: 3.89 | Price Action & Smart Money Analysis`; demand 3.50-3.70, bearish FVG 4.50-4.80, supply 5.70-6.00 (tweet, ikinci el); demand korunursa üst bölgeler, kaybedilirse düşüş senaryosu. Giriş yok.
- KLMSN -99: Fib seviyeleri `Fib 0.236, 0.382, 0.500, 0.618, 0.786, 1.0` ve `0.0` (görsel, düşüş bacağı üzerinde; 4H + günlük); tweet: önce momentum ön eleme sonra yapı; supply 38-39.5, demand 31-32.5 ve 28-31.5 (ikinci el).
- GC=F -21 (`01-gcf-swing-demand-hsar-confluence.png`): `Swing Point + Talep Bölgesi + HSAR Destek Analizi`; yıldız = `Talep+HSAR Kesişimi`; kırmızı oklar. Tweet: confluence alanları taranmalı, "her seferinde büyük değer artışı" (seçilmiş örnekler). HSAR = yatay destek/direnç (formül yok).
- MA filtresi: sahibi B §30. Tansu'nun görsellerinde kullanılan ortalamalar: EMA 5/8/13 (kısa), WMA Close 21 (XU100), EMA 9/21/50/100/200 (PRZMA, AVOD); MA türü ve periyodu verilmemiş (YORUM). (bilet 04, 14.10)
- Günlük trade breakout/retest (`tweet-gunluk-trade-breakout-gap-retest-volume-delta-atr-obv.md`, ikinci el): breakout = VAH/direnç/trend çizgisi üstünde kararlı kapanış; teyit hacim veya delta; temiz giriş = retest; ATR stop; OBV teyit; "kararlı kapanış" ve ATR çarpanı tanımsız.
- Trend çizgisi motoru (`tweet-trend-cizgisi-swing-pivot-regresyon-zarf.md`, ikinci el): Swing Pivot Eşleştirmesi ana yöntemdir; iki pivot bağlanır, arada çizgi delinmez (Aktarım, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21–27). Regresyon+Zarf ikincildir. Pivot L/R penceresi ve kanal üretiminin ayrıntıları YORUM'dur.
- Fib 0.618 + H4 Order Block (`tweet-fibo-0618-bolge-h4-order-block-multitimeframe.md`, ikinci el; video görülmedi): "0.618 duvar değil bölge, wick daha derin H4 OB'ye uzanabilir; Fibo + Order Block = Sniper Giriş". Sayı yok.
- Backtest ve giriş sadeliği (`not-backtest-giris-sadeligi-risk-islem-gunlugu.md`): sahibi E K18. İnceleme sırası: bölge -> kırılım -> likidite -> 4 saat teyit. (bilet 04, 14.10)

---

## Sıralı özet: koda en yakın kurallar (günlük bedava veri ile)

Kodlanabilirlik sırası (kaynağın verdiği ve bizim YORUM ile doldurmamız gereken parametrelere göre):

1. Distal/Proximal + RBR bölge çizgileri (7, 8): çizgi formülü kaynakta sözlü olarak var (görsel); base seçimi YORUM. En az parametre ihtiyacı.
2. Demand bozulma kuralı (9): ilk `Close < zone_low` ile kutu biter (Aktarım, G13:21); `Low < zone_low` daha katı ayrı seçenektir. Buffer YORUM.
3. BOS + Fib 0.618-0.786 + FVG/OB (10): 0.618, 0.786, stop 1.0, TP 0.0 vardır; bullish FVG üç mum boşluğudur (Aktarım, G107:47–48). Swing/BOS ve OB ayrıntıları YORUM.
4. Fiyat konumu vs hacim konumu (13): 252 günlük pencere, tamamen OHLCV; eşikler (%20/%80) görselden YORUM.
5. Breakout + Range Retest + FVG %50 (1): iskelet net (kutu -> breakout -> FVG -> retest -> confirmation -> entry/stop/TP1-3), 8-10 parametre YORUM.
6. Yükselen kanal alt bant teması (2): Lookback 120, temas, Low-Bant %, Kapanış-Bant %; kanal çizimi ve tolerans YORUM.
7. Düşen direnç kırılımı + talep + Fib + ABCD (3, 4): Temas 3, Lookback 20/30, EMA 5/8/13; Küm. Delta günlük veriden çıkmaz.
8. Retest (destek trendi) + EMA5/8/13 (12, 11): temas sayısı ve "temas sonrası gün" sayaçları var; giriş yok.

Kodlanamayacak veya yeterince tanımsız olanlar:
- SETUP x/100 ve "Skor 100/100 / Sınıf A+" (5, 1): puan formülü hiçbir yerde yok.
- Zone D.Touch / D.Teyit tanımları (6): açıklanmamış.
- Siyah Kuğu harmonik (3): oranlar verilmemiş.
- BOM, AHENK, gizli filtre breakout (14, 16): kural açıklanmamış.
- 80-100 hafta yatay (15): tek parametre (süre).
- Küm. Delta (3): gerçek emir akışı verisi gerekir.

Tansu'nun kanıt durumu (tüm kurallar için): sistematik backtest veya gerçekleşen işlem istatistiği hiçbir kaynakta yok. Görseller seçilmiş örneklerdir (LIDER, GC=F, AKFIS, BOM pozitif; BALAT, AKSGY başarısız vaka olarak gösterilmiş). Backtest notu, kendi kural bileşimlerini henüz test etmediğini söylüyor.

## Okunmayanlar / kısmen okunanlar
- Okunmadı (yalnız adı veya görseli): `tweet-acsel-direnc-kirilimi-volume-profile-val`, `tweet-talep-bölgesi-volume-profile-momentum-confluence`, `tweet-formasyon-arz-talep-confluence-kapisi`, `tweet-finans-muhendisligi-destek-direnc-seviye-motoru`, `tweet-fiyatlar-trend-halinde-hareket-eder`, `gorsel-paket-99` görsel 01/02 (yalnız 03 açıldı), `gorsel-paket-101` not gövdesinin devamı.
- Kısmen okundu (ilk ~45-140 satır): tüm -09/-10/-11/-12/-13/-15/-18/-21/-41/-44/-64/-69/-93/-99/-101/-103/-105/-117/-128 notları; gövdedeki Claude'un "Teknik Ek" formülleri ikinci el olarak işaretlendi.
- Tweet orijinal metinleri havuzda yok (yalnız Claude özetleri); X gönderilerine erişilmedi.
- Görsel çözünürlüğü düşük olduğundan (680 px) -10/-11/-12/-13 tablolarındaki bazı değerler yaklaşıktır.
- BALAT kırılım tarihi: görselde 2026-05-15 okundu, not 2026-05-19 diyor (çelişki, doğrulanmadı).
