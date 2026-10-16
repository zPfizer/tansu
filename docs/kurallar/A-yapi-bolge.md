# A. Yapı / Bölge GİRİŞ kuralları — Tansu kaynaklı çıkarım

Not: Havuz = `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`. Görseller `assets\<klasör>\` altında. Kaynak türü ve YORUM tanımları GLOSSARY'dedir. Bu dosyada "birinci el" notun `## Ham` bölümü ve notun görselleridir (NotebookLM görseli dahil); notun öbür bölümleri (Sentez, Cevo çıkarımı, Teknik Ek) ikinci eldir.

Genel bulgu: Tansu bazı notlarda giriş, stop ve hedefi birlikte verir: `gorsel-paket-105-bos-fibonacci-golden-zone-fvg-ob` Ham (giriş: 0.618-0.786 bölgesine temas; stop: Fib 1.0 altı; ilk hedef: Fib 0.0) ve `gorsel-paket-106-demand-ema-squeeze-supply-outcome` Ham (breakout veya retest girişi; stop: talep bölgesi altı; hedef: supply; yazarlığı kısmen belirsiz). Çoğu görselde ve notta kuralın tam parametre seti (eşik, tolerans, periyot), puan formülü ve sistematik, çok sembollü backtest sonucu yok. Görseller seçilmiş örneklerdir. Aşağıdaki "Tanım" bölümlerinde görselde olan şeyler ile YORUM olan şeyler ayrı işaretlendi.

---

## 1. Breakout + Range Retest (+ FVG %50) A+ Setup (AKFIS)
- Kaynak: `kaynak-akfis-breakout-fvg-retest-2095523694881697974.md`; `assets\kaynak-akfis-...\akfis.webp` (birinci el), `alinti-ornek.webp` (sembolsüz, 2 Eylül gönderisinin (`kaynak-tansu-2095218573631279414`) görseli; farklı araç/tema, "CONSOLIDATION / BREAKOUT / BULLISH FVG / RETEST / CONFIRMATION / AL" etiketleri).
- Tansu'nun ifadesi (görsel başlığı, verbatim): `AKFIS | Breakout + Range Retest + RSI Divergence | A+ SETUP | AL TETİKLENDİ | Sınıf: A+ | Skor: 100/100`. Lejant: `AKFIS, Hacim, VolMA20, RSI 14, Range High / Retest, Range Low, FVG %50, AL, ENTRY, STOP, TP1, TP2, TP3`. Grafikteki etiketler: `KONSOLİDASYON`, `BREAKOUT`, `BULLISH FVG + CONFLUENCE`, `RANGE HIGH RETEST`, `CONFIRMATION`, `AL`. Tweet metni (Ham, alıntılanan tweet): "Breakout-->FVG-->Retest-->Confirmation", "Bu yapıları arayın".
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
| FVG tanımı | 3 mum boşluk: `high[t−2] < low[t]`; orta = "FVG %50" | Ham (`gorsel-paket-107`, satır 47–48; Ham'da yazar yok); orta çizgi görsel etiketi |
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
- Tansu'nun kanıtı: yok. Tek seçilmiş örnek (yükseliş devam etmiş). 100/100 olasılık değildir (YORUM; kaynakta olasılık iddiası yok).
- Günlük bedava veriyle uygulanabilir mi: Evet, tanımlanabilir (günlük OHLCV yeter) ama birçok parametre YORUM ile doldurulmalı. Kural iskeleti net; parametre uydurma gerekir.
- Kaynak güveni: görsel orta (etiketler birinci el), parametre düşük.

---

## 2. Yükselen Kanal Alt Bant Teması (AEFES)
- Kaynak: `kaynak-aefes-yukselen-kanal-alt-bant-2096582181170598078.md`; `assets\kaynak-aefes-...\aefes-kanal.webp`.
- Tansu'nun ifadesi (görsel, verbatim): başlık `AEFES — YÜKSELEN KANAL — ALT BANT TEMAS`; alt satır `Lookback: 120 | Temas: 2026-09-03 | Alt bant: 17.76 | Low: 17.92 | Low-Bant: +0.92% | Kapanış-Bant: +2.56% | Üst/Alt temas: 3/3 | Genişlik değişimi: +15.3% | ALT BANT TEMAS + TEPKİ`. Lejant: Fiyat, Üst Sınır, Alt Sınır, Alt Bant Temas, Hacim, Hacim MA21, RSI 14, MACD Hist/MACD/Signal, +DI, -DI.
- Tanım (görselden):
  1. Son 120 mum (Lookback 120) içinde yükselen iki kesikli çizgi: Üst Sınır ve Alt Sınır; çizgiler sağa doğru açılıyor. Alt sınır ~15.8 (ilk dip) -> ~18.0 (son bar); üst sınır ~20.5 -> ~23.5 (piksel okuması).
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
| Kanal kurma | trend çizgisinde swing pivotları ikili bağlama; arada çizgi delinmez | Ham (`tweet-trend-cizgisi-swing-pivot-regresyon-zarf`:21–27); pivot tespiti ve kanal üretimi açık |
| Tepki koşulu | haftalık kanalda alt banda gelip yeşil kapanış; "yeşil" = kapanış > açılış (YORUM) | Ham (`tweet-haftalik-kanal-alt-bant-yesil-kapanis-1956082078212305072`) |
| Genişlik filtresi | "Genişlik değişimi" gösteriliyor, eşik yok | görsel |
| Paralellik | paralel değil: alt çizgi ~+2.2, üst çizgi ~+3.0 yükseliyor; genişlik değişimi +15.3% | görsel |

- Giriş / stop / hedef / bozulma: verilmemiş. Bozulma YORUM: kapanış alt bandın altında.
- Belirsiz kalanlar: kanal algoritması, temas toleransı, genişlik tanımı, tepki tanımı, çıkış.
- Tansu'nun kanıtı: yok (tek örnek, sonuç gösterilmemiş).
- Günlük bedava veriyle uygulanabilir mi: Evet (120 günlük pencere). Trend çizgisinin ana yöntemi pivot eşleştirmesidir; arada çizgi delinmez (Ham, `tweet-trend-cizgisi-swing-pivot-regresyon-zarf`:21–27). Kanal üretiminin ayrıntıları YORUM.
- Kaynak güveni: etiket/sayı birinci el; algoritma bilinmiyor.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-haftalik-kanal-alt-bant-yesil-kapanis-1956082078212305072` — Tepki koşulu ve periyot: haftalık kanalda alt banda gelip yeşil kapanış. "Haftalık kanalda kanal alt bandına gelip yeşil kapatmalı" (Ham). Zincirdeki yanıt: hisse beklenen yere gelmezse başkasına geçilir, tarama kodu filtrelerle yeniden çalıştırılır: "Hisse beklediğim yere gelmezse başkasına geçerim." (Ham) Parametre: kanal periyodu = haftalık; tepki koşulu = alt banda temas + yeşil (yükselen) mum kapanışı; yeşil = Close > Open YORUM (Ham).

---

## 3. "Düşen Direnci Kıran + Talep + Fibo + ABCD" tarayıcı çıktısı (LIDER, BALAT)
- Kaynak: `gorsel-paket-34-siyah-kugu-talep-run.md`, `gorsel-paket-45-balat-abcd-negatif-kumulatif-delta.md`; görseller `assets\gorsel-paket-34-...\01-lider-siyah-kugu-talep-run.png`, `assets\gorsel-paket-45-...\01-balat-abcd-negatif-kumulatif-delta.jpg` (birinci el, düşük çözünürlük 680 px).
- Tansu'nun ifadesi (görsel başlıkları, verbatim, küçük punto, okunabildiği kadar):
  - LIDER: `Düşen Direnci Kıran + Talep + Fibo + ABCD | Harmonik: Siyah Kuğu | Fiyat: 127.40 | Kırılım: 2026-05-18 | Temas: 3 | Lookback: 20`
  - BALAT: `Düşen Direnci Kıran + Talep + Fibo + ABCD | Fiyat: 75.95 | Kırılım: 2026-05-15 | Temas: 3 | Lookback: 30`
  - Lejant: Fiyat, EMA5, EMA8, EMA13, "Direnç TL" (kırmızı çizgi), "Harmonik (Siyah Kuğu)", Hacim, "Küm. Delta". Fib seviyeleri 1.000/0.786/0.618/0.500/0.382/0.236/0.000 (BALAT: 99.45 / 94.00 / 89.73 / 86.72 / 83.72 / 80.01 / 74.00); `D(CD=1.27AB)`.
- Tanım (başlıktan çıkan): (a) düşen direnç trend çizgisi tepeler arasındadır; "Temas: 3" etiketi vardır; (b) "Kırılım" tarihtir; (c) Talep yeşil yatay kutudur; (d) Fibo tepe/dip arasında çizilir; (e) ABCD D'de tamamlanır. Lookback 20/30 etiketleri arama veya kırılım sonrası izleme süresini açıklamaz (Araç, G34/g1 ve G45/g1). YORUM: bu katalogda çizgi arama penceresi olarak okunur; değişken/otomatik seçim açıklaması doğrulanmış değildir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Temas sayısı | 3 (her iki örnekte) | görsel |
| Lookback | 20 (LIDER), 30 (BALAT) | görsel |
| Kırılım koşulu | kapanış trend çizgisini aşar | Ham (`tweet-trend-cizgisi-swing-pivot-regresyon-zarf`:21); başka kırılım türlerine genellenmez |
| EMA | 5/8/13 | görsel (lejant) |
| ABCD oranı | CD=1.27AB (BALAT D etiketi) | görsel |
| Talep bölgesi tanımı | bilinmiyor | YORUM |
| Giriş/stop/hedef | yok | - |

- Önemli: BALAT görseli bir başarısızlık örneğidir. Tansu'nun yorumu (Ham, `gorsel-paket-45`): "Abcd analizine güvenip çaat diye alırsan küüt diye böyle olursun. Her zaman çalışmaz. İkinci alt grafiğe dikkat." (Küm. Delta uzun süre negatif). LIDER ise "Kuğuyu bir de talep toplama bölgesinde yakalarsanız böyle RUN! olur grafiğiniz." (Ham, `gorsel-paket-34`). Yani aynı başlıklı iki sinyalden biri başarılı biri başarısız gösterildi; Küm. Delta bir filtre olarak ima ediliyor ama eşik yok.
- Belirsiz kalanlar: çizgi kuran algoritma, talep bölgesi bağı, Lookback anlamı, Küm. Delta hesabı, "Siyah Kuğu" oranları (bu bölümün kaynaklarında yok; bullish aralıklar: C §26, 16.10). Gerçek işlem deltası günlük OHLCV'den çıkmaz; kaynak panelinin proxy olup olmadığı açık değildir (Araç, G45/g1, alt panel). YORUM: günlük proxy bizim seçimimizdir.
- Tansu'nun kanıtı: yok; biri seçilmiş pozitif, biri seçilmiş negatif.
- Günlük bedava veriyle uygulanabilir mi: Düşen direnç kırılımı + EMA5/8/13 + Fib + ABCD: evet (günlük). Küm. Delta paneli: hesabı belirsiz (Araç, G45/g1, alt panel); günlük proxy YORUM'dur. Siyah Kuğu: oranlar verilmemiş, kodlanamaz.
- Kaynak güveni: başlık değerleri birinci el ama düşük çözünürlük; kural düşük.

---

## 4. Düşen trend çizgisi kırılımı + talep + hacim + EMA5/8/13 (-64)
- Kaynak: `gorsel-paket-64-dusen-trend-talep-hacim-ema-breakout.md`; `assets\gorsel-paket-64-dusen-trend-hacim-breakout\01-dusen-trend-talep-hacim-ema-breakout.jpg`.
- Tansu'nun ifadesi: görselde yalnızca lejant `EMA 5 / EMA 8 / EMA 13 / Direnç TL`; sembol, başlık, tarih yok. Ham: "Düşen Trend Kırılımı ve Hacimli Onay"; zincir: düşen direnç kırılımı + yeşil talep bölgesi + yüksek hacim + EMA 5/8/13 yukarı dönüşü + uzun yeşil, tepeye yakın kapanışlı mum; "Pazartesi bakalım".
- Tanım (görsel): fiyat geniş yeşil talep kutusunun (yatay) içinde/üstünde uzun süre taban yapıyor; kırmızı "Direnç TL" aşağı eğimli (tepelerden); son gün uzun yeşil mum çizgiyi yukarı kıran ve kapanış üst tarafa yakın; son hacim çubuğu görünür örneklemin en büyüğü; EMA5/8/13 sıkışık ve yukarı dönüyor.
- Parametreler: hepsi yok (EMA 5/8/13 dışında). Çizgi çapaları, talep kutusu sınırları, "yüksek hacim" eşiği, kapanış konumu eşiği: YORUM. Trend çizgisinde swing pivotları ikili bağlama ve arada delinmeme kaynaklıdır (Ham, `tweet-trend-cizgisi-swing-pivot-regresyon-zarf`:21–27); pivot tespiti ve hacim formülleri YORUM'dur.
- Giriş / stop / hedef: yok. Bozulma: yok.
- Tansu'nun kanıtı: yok; sonuç bilinmiyor ("Pazartesi bakalım").
- Ek örnekler (KANIT, bilet 04, 14.10; birinci el: görsel + Ham metni, sembolsüz, periyotsuz): `kaynak-dusen-yapi-kirilim-2096576027791131079` (görsel okundu: daralan düşen yapı, kırmızı üst ve mavi alt çizgi aşağı eğimli; son uzun yeşil mum üst çizgiyi aşıyor, etiket KIRILIM; son hacim çubuğu hemen öncekilerden yüksek; tweet metni yalnız "Canlanın:)") ve `kaynak-dusen-yapi-retest-2096577500612624410` (aynı yapı türü; KIRILIM ve RETEST etiketleri, çizgiye geri çekilme sonrası yeşil mum; tweet metni: "Güzer retest var", "gider mi gitmez mi artık orası tahtacıya kalmış"). İkisinin aynı hisse olduğu doğrulanmadı. Seviye, tolerans, giriş, stop, hedef ve sonuç yok; tek mumla teyit sayılmaz.
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
  - Grafik etiketleri: `WMA Close 21`, `SUPPLY / ARZ 15133.50 - 15204.90`, `SUPPLY / ARZ 14734.50 - 14876.10`, `DEMAND / TOPLAMA 12966.30 - 13056.65` (iki günde de), ikinci demand kutusu `12601.60 - 12698.20` ya da `12801.60 - 12898.20` (iki günde de rakamlar okunamıyor), `11102.20 - 11172.60` (1 Eylül günlük; 2 Eylül günlük grafiğin ekseni bu düzeyin üstünde biter); 4 saat: `DEMAND / TOPLAMA 13833.00 - 13659.74`, `13216.16 - 13273.44`; `DÜŞEN TREND | TARİHSEL/KIRILMIŞ | TEMAS: 8`; `YÜKSELEN TREND | YENİ KIRILDI | TEMAS: 7`; HH/HL/LH/LL, BOS, CHoCH, SSL SWEEP, BSL SWEEP işaretleri; alt paneller MACD 12 26 9, RSI 14 | 70 / 30, WT 10 21 | 60 53 -53 -60.
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

- Giriş / stop / hedef: yok. Tweet metni (Ham): WMA21 geri alma eşiği 14443.45; ilk olumlu eşik 14722.02 (1 Eylül) ve yaklaşık 14.722 (2 Eylül); bullish FVG kayıp eşiği 14140.43; ana "bekle ve teyit" yaklaşımı. Sayısal kalıcılık şartı yok.
- Tansu'nun kanıtı: yok.
- Günlük veriyle uygulanabilir: yapı (swing, BOS/CHoCH), demand/supply, FVG sayımı: evet ama algoritma YORUM. SETUP puanı: formül yok, kopyalanamaz. 4 saatlik panel için günlük bedava veri yetmez.
- Kaynak güveni: görsel metni birinci el ve net; kural yok.

---

## 6. Zone gösterge tablosu: En Yakın Demand, D.Touch, D.Teyit, Supply, S.Touch, S.Teyit (-10, -11, -12, -13)
- Kaynak: `gorsel-paket-10-hktm-demand-supply.md`, `-11-froto-bos-choch.md`, `-12-doas-advance-block.md`, `-13-ttkom-demand-invalidation.md`; görseller `assets\gorsel-paket-10-...`, `-11-...`, `-12-...`, `-13-...` (birinci el, 680 px).
- Tansu'nun ifadesi: başlık `<SEMBOL> - Demand & Supply Bölgesi Analizi`; alt tablo kolonları `Son Fiyat | Max | Min | En Yakın Demand | D.Touch | D.Teyit | En Yakın Supply | S.Touch | S.Teyit` (TTKOM görselinde `Aktif Demand`, `Aktif Supply`). Okunan satırlar: DOAS `171.20 | 247.00 | 166.40 | 165.59-173.00 | 3 | 2025-11-04 | 200.90-209.91 | 2 | 2026-06-25`; TTKOM `54.50 | 75.85 | 47.48 | okunamıyor (üst sınır 51.30) | 0 | 2026-08-14 | okunamıyor (yaklaşık 65-66.5) | 1 | 2026-06-29`; FROTO `78.10 | ... | 73.05 | 74.70-76.70 | 1 | 2026-08-14 | 90.10-92.69 | 1 | 2026-06-30` (düşük çözünürlük, yaklaşık). HKTM görselinde tablo kolonları: Son Fiyat, Max, Min, En Yakın Demand, D.Touch, D.Teyit, En Yakın Supply, S.Touch, S.Teyit ve dört ek kolon (başlıklar yaklaşık okunur: Düşen Trend, Destek Trend, HSAR, Fibonacci); görselde veri satırı yok, yalnız başlık satırı var.
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
- Kaynak: `gorsel-paket-09-distal-proximal-arz-talep.md`; `assets\gorsel-paket-09-distal-proximal\01-distal-proximal-arz-bolgesi.png` (İngilizce ders diyagramı, Tansu'nun aracı değil; Levent kaynak olarak iletmiş; Ham'da yazar yok).
- Tansu'nun ifadesi (görsel, verbatim): "The distal line is located at the highest of the basing structure while the proximal line is placed at the lowest body price of the base." Diyagram: yükselen mumlar, `Base`, sonra düşüş (rally-base-drop). `Distal line` = base'in en yükseği; `Proximal line` = base'teki en düşük gövde fiyatı.
- Tanım: arz bölgesi: distal = max(high[base]); proximal = min(min(open,close)[base]). Talepte proximal/giriş ve distal/stop ilişkisi eğitim şemasında vardır (Eğitim, G15/g1). YORUM: distal = min(low[base]), proximal = max(max(open,close)[base]); base veya leg-out seçiminin evrensel formülü verilmez.
- Parametreler: base seçimi (kaç mum, gövde/range oranı) YOK; YORUM.
- Giriş: proximal çizgi; stop = distal çizgi (Eğitim, G15/g1: giriş/proximal ve distal/stop ilişkisi).
- Tansu'nun kanıtı: yok. Günlük veriyle: evet. Kaynak güveni: diyagram net ama Tansu'ya atfı doğrulanmadı; Ham: "Distal line ve proximal line'ı kavrarsak bu işişn %50'si biter, kalan %50'si de taramasını anlayabilmek".

---

## 8. RBR (Rally-Base-Rally) talep bölgesi (-15)
- Kaynak: `gorsel-paket-15-rbr-demand-zone.md`; `assets\gorsel-paket-15-rbr-demand-zone\01-rally-base-rally-rbr-pattern.png` (ders diyagramı, Tansu aracı değil).
- Tansu'nun ifadesi (görsel, verbatim): `RBR PATTERN`, `LEG IN CANDLE`, `BASE CANDLE`, `LEG OUT CANDLE`, `ENTRY POINT`, `Proximal line`, `Distal line / stop loss`; "NOTE: The area between proximal line and distal line is area of demand which is known as demand zone. DISTAL line always be at the low of base candle or leg out candle in RBR pattern."
- Tanım: yükselişte leg-in (yeşil büyük mum) -> 1+ küçük base mumu (renk önemli değil) -> leg-out (büyük yeşil). Eğitim şemasında proximal = giriş; distal = stop, base veya leg-out dibindedir (Eğitim, G15/g1). YORUM: proximal base üst gövde seviyesi civarı; distal base low veya leg-out low'un küçüğü; evrensel seçim formülü açık değildir.
- Parametreler: base mum sayısı, "küçük" gövde eşiği, leg-out büyüklüğü: yok (YORUM).
- Giriş / stop: görselde var (proximal/entry, distal/stop); hedef yok. Not'un base kapıları listesi Claude önerisidir.
- Kanıt yok. Günlük veriyle evet. Güven: ders diyagramı; Ham'da yazar yok (yalnız görsel); genel eğitim materyali.

---

## 9. Talep bölgesi bozulması (invalidation) (-13)
- Kaynak: `gorsel-paket-13-ttkom-demand-invalidation.md`; TTKOM görseli.
- Tansu'nun ifadesi: tweet (Ham): demand bölgesinin en düşük fiyatı `zone_low`; oluşum sonrası ilk mum `close < zone_low` (veya daha katı: `low < zone_low`) ise kutu o tarihte biter. Görselde kırmızı ok, gri kutunun kırılım tarihinde bittiği yeri gösteriyor (birinci el).
- Tanım: oluşum sonrası ilk `Close < zone_low` mumunda kutu biter (Ham, `gorsel-paket-13`:21). `Low < zone_low` daha katı ayrı seçenektir; aracın hangi seçeneği kullandığı açık değildir.
- Parametreler: buffer yok. YORUM: 0.
- Giriş/stop/hedef: yok (bozulma kuralı olarak stop mantığına doğrudan bağlanabilir). Kanıt yok. Günlük evet. Güven: orta.

---

## 10. BOS / CHoCH piyasa yapısı (-11) ve BOS + Fib Golden Zone (0.618-0.786) + FVG/OB (-105)
- Kaynak: `gorsel-paket-11-froto-bos-choch.md`, `gorsel-paket-105-bos-fibonacci-golden-zone-fvg-ob.md`; görsel `assets\gorsel-paket-105-...\01-bos-fibonacci-golden-zone-fvg-order-block.png`.
- Tansu'nun ifadesi: -11 tanımlar (Ham): BOS = trend yönünde önceki swing high/low kırılması; CHoCH = korunan HL/LH'nin ilk kaybı. -105 (Ham): "BOS Destekli Fibonacci Golden Zone Alım Stratejisi": bullish impulse -> önceki tepe üstü BOS -> HH -> swing low'dan swing high'a Fibonacci -> 0.618-0.786 OTE/Golden Zone -> FVG veya Order Block teması -> long; stop Fib 1.0 / swing low altı; TP1 Fib 0.0 (eski tepe); ileri hedef negatif Fib extension. Görsel (birinci el, 680x280): `BOS`, `HH` etiketleri; Fib seviyeleri `0.0: 216.77`, `0.236: 201.69`, `0.382: 191.32`, `0.5: 183.46`, `0.618: 175.60`, `0.786: 163.75`, `1.0: 150.15` (okunan yaklaşık); 0.618-0.786 arasında yeşil zone kutuları; kırmızı oklar: geri çekilme -> Golden Zone -> yeniden yükseliş.
- Tanım (adım adım):
  1. Swing low L -> yukarı impulse -> önceki swing high H0'ı kapanışla geçince BOS (yapı yükselen).
  2. Yeni tepe HH oluşur (swing high).
  3. Fib: L (1.0) ile HH (0.0) arası. Golden Zone = 0.618-0.786 retracement bandı (fiyat 0.0 -> 1.0 yönünde geri gelir).
  4. Fiyat bu banda girer ve band içinde FVG veya Order Block ile çakışma/temas yaşar -> long adayı.
  5. Stop = L (1.0) altı; TP1 = HH (0.0); sonraki = negatif extension.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Golden Zone | 0.618-0.786 | görsel (seviyeler) + Ham |
| Stop | Fib 1.0 / impulse swing low altı; buffer yok | Ham; buffer YORUM |
| TP1 | Fib 0.0 (eski tepe) | Ham |
| İleri hedef | negatif Fib extension; −0,27 hedef örneği | Ham (`gorsel-paket-105`:48–55); genel oran seçimi YORUM |
| Swing pivot L/R, BOS tampon, FVG/OB tanımı | swing, BOS tamponu ve OB seçimi yok; bullish FVG: `high[t−2] < low[t]` | FVG: Ham (`gorsel-paket-107`:47–48; Ham'da yazar yok); diğer ayrıntılar YORUM |
| Periyod | bilinmiyor | - |

- Tansu'nun fikri, temas bölgesinde işlem aramaktır (Ham, `gorsel-paket-105`:48–55); uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- Tansu'nun kanıtı: yok; seçilmiş pozitif tek örnek, başarısız adaylar yok.
- Ek örnek (KANIT, bilet 04, 14.10): `gorsel-paket-66-fibo-volume-profile-vwap-delta-yuzde20` (Tansu'nun metni, Ham; görsel okundu): 8 Ocak 2026 görünümü; düşüşün 0,786 seviyesi ve yatay direnç aşıldı; fiyat 31,00, POC 29,71, VAH 30,24, VWAP 28,00 (VWAP'tan +%10,73 uzak); +DI, −DI'nın üstünde; kümülatif delta yukarı eğimli. Tansu'nun sonuç iddiası ayrı bir grafikte; bu katalog getiri rakamı yazmaz. Seçilmiş pozitif örnek; giriş, stop, hedef yok. Delta için emir akışı verisi gerekir (günlük veriden çıkmaz).
- Günlük veriyle: evet. Güven: akış net, parametreler yok; tweet metni Ham, görsel doğrular seviyeleri.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bos-fibo-golden-zone-order-block-alim-2002131073137062285` — Tekrar, birinci el kaynak olarak: aynı strateji metni Tansu'nun kendi X gönderisi (19.12.2025; bölümdeki -105 metni "Ham'da yazar yok" idi). Beş adım aynıdır; ek ayrıntılar: giriş yalnız fiyat Fib 0.5 ("Discount") altına inince aranır, hedef bölge 0.618–0.786 ve yeşil kutu (Order Block veya FVG) teması şart; BOS "önceki önemli bir tepeyi yukarı yönlü kırıp üzerinde kapanış" demektir. "Stop Loss (SL): Fibonacci 1.0 seviyesinin (hareketin başladığı en dip noktanın) hemen altına koyulur." (Ham). TP1 Fib 0.0, ileri hedef uzatma (−0.27 "vb."). "Hemen altına": tampon sayısı yok. Tansu "taramasını yaparsınız" der: tarama kendisinde yok. Görsel (görsel, açıldı): bölümdeki yaklaşık okumalar yerine yazılı değerler 0.236: 201.05, 0.786: 164.11 (küçük yazı; 0.0 ve 1.0 uçlarıyla formül 164.41 verir, bu yüzden 0.786 değeri belirsiz). Parametre: Fib 0.236 = 201.05; Fib 0.786 = 164.11 (görsel, açıldı; bölümdeki 201.69 ve 163.75 yaklaşık okumadır)
  - `tweet-fib-382-giris-618-stop-bos-1838978628757143953` — Aynı yapı (itki, BOS, HH, Fib), farklı seviyeler: "38.2% ENTRY" ve "61.8% SL"; başlık "1. IMPULSIVE MOVE (AROUND 38.2% FIBONACCI LEVEL)" (görsel, açıldı). Ham: "Şu durumu kodlayıp taramasını yapalım bakalım ne çıkacak" (kodlama niyeti, sonuç yok). §10'daki 0.618–0.786 giriş ve Fib 1.0 stop yerine daha sığ varyant. Şema, sembol ve sonuç yok. Parametre: Giriş = Fib 0,382 geri alımı; stop = Fib 0,618 (görsel, açıldı); anahtar seviye (KEY LEVELS) kutusu itki başında (görsel, açıldı)

---

## 11. Trend desteği (yükselen) + demand + FVG + BOS (GEDZA -93)
- Kaynak: `gorsel-paket-93-gedza-demand-bos-hacim-momentum.md`; `assets\gorsel-paket-93-...\01-gedza-trend-demand-fvg-bos-hacim.jpg`.
- Tansu'nun ifadesi (görsel başlık/lejant, verbatim): `GEDZA - Fiyat: 31.10`; lejant `EMA 5, EMA 13, Trend Destek, Temas, En Yakın Demand, En Yakın FVG, BOS` (Araç, G93/g1, sol üst lejant). Alt paneller Hacim, MACD, ADX, RSI.
- Tanım: yükselen "Trend Destek" çizgisi (cyan) iki+ pivot low'dan; fiyat sağ uçta çizgi ve yeşil "En Yakın Demand" kutusuna iniyor ("Temas" üçgeni), büyük yeşil tepki mumu, son hacim çubuğu çok yüksek; altta "En Yakın FVG" kutusu; yatay BOS çizgisi üstte.
- Parametreler: EMA 5/13 (Araç, G93/g1, sol üst lejant); ADX/RSI/MACD periyodu yok (YORUM); temas toleransı yok.
- Giriş/stop/hedef: yok. Kanıt: yok. Not'un "MACD negatif, ADX zayıf: karışık teyit" yorumu Claude'a ait. Günlük veriyle evet. Güven: düşük-orta.

---

## 12. Yükselen destek trendi RETEST + temas sayısı + EMA5/8/13 (AKSGY -103, -117)
- Kaynak: `gorsel-paket-103-aksgy-retest-macd-volume-failure.md`, `gorsel-paket-117-ema5-8-13-yukselen-trend-destek-tepki.md`; görseller `assets\gorsel-paket-103-...\01-aksgy-retest-macd-volume-failure.png`, `assets\gorsel-paket-117-...\01-ema5-8-13-yukselen-trend-destek-tepki.png`.
- Tansu'nun ifadesi (görsel başlığı, verbatim, -103): `AKSGY | EMA8 > EMA13 > EMA5 | ADX: 34.13 | RSI: 41.13 | MACD: -0.013 | RETEST VAR (6 kez) | İlk Temas: 2025-10-14 | Son Temas: 2025-12-08 | Temas Sonrası: 9 gün`. Lejant: Destek Trendi, EMA 5/8/13, Golden Cross, Son Temas, RETEST, ADX (Zayıf Trend, Güçlü Trend), RSI (Aşırı Alım/Satım). -117: lejant `Destek Trendi, EMA 5, EMA 8, EMA 13, Son Temas`; ADX 14 ve eşik 20 çizgisi; RSI 14; MACD "Alım Sinyali / Satım Sinyali" üçgenleri; başlık yok.
- Tanım: yükselen destek çizgisi (Destek Trendi) üzerinde "temas" günleri sayılıyor (AKSGY: 6 retest, ilk 2025-10-14, son 2025-12-08, son temastan 9 gün sonra bugün). EMA dizilimi tarayıcı filtresi/etiketidir (AKSGY'de EMA8>EMA13>EMA5 = bozuk dizilim; -117'de Ham "ema5>ema8>ema13 de oluşmuş" diyor, görselde okunamadı).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA | 5/8/13 | görsel |
| ADX | 14 periyot, 20 eşik (zayıf), ~40? güçlü eşik çizgisi var | görsel (-117 "ADX 20", -103 iki eşik çizgisi, değer okunamadı) |
| RSI | 14 | görsel |
| Temas toleransı, çizgi çapaları | değerler yok; trend çizgisinde swing pivotları ikili bağlama ve arada delinmeme | yöntem: Ham (`tweet-trend-cizgisi-swing-pivot-regresyon-zarf`:21–27); sayısal ayrıntılar YORUM |
| "Temas Sonrası" | son temastan geçen gün (9) | görsel |

- Giriş/stop/hedef: yok. Tansu'nun yorumu (Ham, -103): "İşte bu yüzden retest beklemek önemlidir. Bakın macd yanıltmış ama hacim asla desteklememiş." => seçilmiş başarısız örnek; son kırmızı mum destek altına sarkıyor. -117 (Ham): "ema5>ema8>ema13 de oluşmuş son gün yükselen trend desteğinden tepki almış yeşil yakmış falan filan"; hacim zayıf, MACD negatif, ADX~20, RSI~50 ve "pozitif setup adayı" ifadesi yalnız Sentez'dedir (ikinci el; YORUM).
- Kanıt: yok (iki örnek: biri başarısız, biri belirsiz). Günlük veriyle evet. Güven: başlık birinci el; kural yok.

---

## 13. Fiyat konumu vs hacim konumu (-128)
- Kaynak: `gorsel-paket-128-fiyat-hacim-konum-proxy-cot-kalabalik-dip.md`; görseller `assets\gorsel-paket-128-fiyat-hacim-konum-proxy\01-fiyat-hacim-konum-scatter-rsi.png`, `02-secilmis-dip-sonrasi-fiyat-grafigi.png`.
- Tansu'nun ifadesi (görsel eksen etiketleri, verbatim): X `FİYAT KONUMU (%0 = Yıllık Dip, %100 = Yıllık Tepe)`; Y `HACİM/İLGİ KONUMU (%0 = Hacimsiz, %100 = Yoğun)`; renk `RSI Gücü` (20-80); sol üst yeşil kutu `DİP OLUŞUMU? (Yüksek Hacim, Düşük Fiyat)`; sağ üst kırmızı `AŞIRI ISINMA (Yüksek Hacim, Yüksek Fiyat)`; `SON GÜN`. Tweet (Ham): 252 günlük fiyat konumu + 252 günlük hacim konumu, yfinance verisiyle, COT verisi olmadığı için proxy.
- Tanım: fiyat_konumu = (kapanış - 252g min) / (252g max - 252g min) x 100. Hacim konumu benzer şekilde 252 gün içindeki hacmin yüzdelik/min-max konumu (hangisi olduğu belirtilmemiş, YORUM). Dip adayı: fiyat <~%20, hacim >~%80 (kutu sınırları görselden: x 0-20, y 80-100). Aşırı ısınma: x 80-100, y 80-100.
- Parametreler: pencere 252 (tweet, Ham); kutu sınırları ~%20/%80 (görselden kaba okuma); RSI periyodu bilinmiyor.
- Giriş/stop/hedef: yok. Kanıt: tek seçilmiş dip örneği (ok), sistematik yok. Günlük veriyle: evet, tam uygulanabilir (yalnızca OHLCV). Güven: eksen tanımı birinci el; hacim konumu formülü belirsiz.

---

## 14. Konsolidasyon kutusu sınırı (gövde/fitil) (-18) ve uzun yatay + kırılım ("Point A -> Point B") (-44, -41)
- Kaynak: `gorsel-paket-18-konsolidasyon-body-wick.md`, `gorsel-paket-44-basit-gizli-filtre-breakout-kesfi.md`, `gorsel-paket-41-konsolidasyon-suresi-kirilim-siddeti.md`; görseller `assets\gorsel-paket-18-...\01-konsolidasyon-body-wick-bolge.jpg` (TradingView ekran görüntüsü, mor kutular), `assets\gorsel-paket-44-...\01-point-a-b-gizli-filtre-breakout.png` (etiketler `Point A (Start)`, `Point B (Breakout)`), `assets\gorsel-paket-41-...\01-ok-konsolidasyon-suresi-kirilim-siddeti.png`.
- Tansu'nun ifadesi (tweet, Ham): -18: üst sınır = en yüksek mumun gövde ucu, alt sınır = en düşük mumun fitil ucu. -44: "hep göz önünde olan 1-2 filtre ile enteresan bir breakout sinyali var aslında" — filtreler açıklanmamış. -41: "okların bulunduğu alan yatayda ne kadar genişse (konsolidasyon uzunsa) kırılım o kadar şiddetli"; Tansu görseldeki kısa konsolidasyona rağmen güçlü kırılıma şaşırdığını söylüyor.
- Tanım: -18: zone_upper = max(open,close) of highest-high candle; zone_lower = min(low). -44/-41: uzun yatay kutu başlangıcı Point A, üst bandın aşıldığı Point B; -44'te sarı MA benzeri çizgi ve mavi noktalı trailing/zarf var (kimliği yok).
- Parametreler: tümü yok (filtre, süre, kutu yüksekliği); YORUM: süre ve ATR-normalize yükseklik.
- Giriş/stop/hedef: yok. Kanıt: seçilmiş; -41 hipotez ("uzun konsolidasyon -> güçlü kırılım") test edilmemiş. Günlük veriyle: evet (kural yazılabilir) ama gizli filtre kopyalanamaz. Güven: düşük.

---

## 15. Hafta yatay (80-100 hafta) + bant dibinde bekleme (kaynak-80-100-hafta-yatay)
- Kaynak: `kaynak-80-100-hafta-yatay-tarama-2096580811080261784.md`. Görsel yok.
- Tansu'nun ifadesi (Ham, verbatim): "en temiz strateji bulacaksın 80-100 haftalık yatay giden bir hisse dibinde oturup bekleyeceksin"; ardından taramasını yazma niyeti ("Yazalım o zaman taramasını").
- Tanım (YORUM; kaynakta yok): haftalık kapanışta 80-100 hafta boyunca max/min aralığı dar (tepe/dip oranı eşiği), fiyat bandın alt %X'inde. Tansu eşik vermemiş.
- Parametreler: süre 80-100 hafta (tek parametre, Ham); eğim, bant genişliği, alt bölge eşiği, stop, çıkış: yok (YORUM).
- Kanıt: yok. Günlük veriyle: evet (haftalığa resample). Güven: düşük (tek cümlelik fikir).

---

## 16. Ikinci kademe (kısa kayıt): BOM, AHENK, FVG, çoklu zaman, MA filtre, retest
- BOM (`kaynak-bom-iki-tavan-2093647837162553475.md`, `assets\kaynak-bom-...\bom.webp`): görselde `BOM` işareti (siyah üçgen), `Kırılım 2026-06-18 (Temas:7)`, `Kırılım 2026-07-24 (Temas:5)` (turuncu trend çizgileri), CHoCH, hacim profili, kırmızı kutu içinde BOM sonrası yükseliş. Tweet (Ham): "şartlar da müsait ise", "2 tavan üst üste vermiş". BOM formülü yok. Kural çıkarılamaz.
- AHENK (`kaynak-ahenk-demand-2094486927328059452.md`, `ahenk.webp`): `DEMAND / TOPLAMA` kutusu, mor WMA benzeri çizgi, MACD/RSI/WT panelleri. Tweet: "Ahengin uyumu"; kural yok.
- PRZMA -69 (`gorsel-paket-69-...md`, `01-przma-bullish-fvg-bos-ema.jpg`): başlık `PRZMA | Fiyat: 17.70 | Price Action & Smart Money Analysis`, EMA 9/21/50/100/200, yeşil FVG kutuları. Tweet (Ham): FVG upper-bound ilk teması alarm adayı; doğrudan long yerine 1H/4H CHoCH bekle. Sayısal kural yok.
- AVOD -101: başlık `AVOD | Fiyat: 3.89 | Price Action & Smart Money Analysis`; demand 3.50-3.70, bearish FVG 4.50-4.80, supply 5.70-6.00 (tweet, Ham); demand korunursa üst bölgeler, kaybedilirse düşüş senaryosu. Giriş yok.
- KLMSN -99: Fib seviyeleri `Fib 0.236, 0.382, 0.500, 0.618, 0.786, 1.0` ve `0.0` (görsel, düşüş bacağı üzerinde; 4H + günlük); tweet: önce momentum ön eleme sonra yapı; supply 38-39.5, demand 31-32.5 ve 28-31.5 (Ham).
- GC=F -21 (`01-gcf-swing-demand-hsar-confluence.png`): `Swing Point + Talep Bölgesi + HSAR Destek Analizi`; yıldız = `Talep+HSAR Kesişimi`; kırmızı oklar. Tweet (Ham, `gorsel-paket-21`): confluence alanları taranmalı, "Her seferinde zenginlik yaratmışlar" (seçilmiş örnekler). HSAR = yatay destek/direnç (formül yok).
- MA filtresi: sahibi B §30. Tansu'nun görsellerinde kullanılan ortalamalar: EMA 5/8/13 (kısa), WMA Close 21 (XU100), EMA 9/21/50/100/200 (PRZMA, AVOD); MA türü ve periyodu verilmemiş (YORUM). (bilet 04, 14.10)
- Günlük trade breakout/retest (`tweet-gunluk-trade-breakout-gap-retest-volume-delta-atr-obv.md`, Ham): breakout = VAH/direnç/trend çizgisi üstünde kararlı kapanış; teyit hacim veya delta; temiz giriş = retest; ATR stop ("günün ATR'si neyse, giriş yerinizden o kadar uzağa", yani 1x ATR); OBV teyit; "kararlı kapanış" tanımsız.
- Trend çizgisi motoru (`tweet-trend-cizgisi-swing-pivot-regresyon-zarf.md`, Ham): Swing Pivot Eşleştirmesi ana yöntemdir; iki pivot bağlanır, arada çizgi delinmez (`tweet-trend-cizgisi-swing-pivot-regresyon-zarf`:21–27). Regresyon+Zarf ikincildir. Pivot L/R penceresi ve kanal üretiminin ayrıntıları YORUM'dur.
- Fib 0.618 + H4 Order Block (`tweet-fibo-0618-bolge-h4-order-block-multitimeframe.md`, Ham; video görülmedi): "0.618 duvar değil bölge, wick daha derin H4 OB'ye uzanabilir; Fibo + Order Block = Sniper Giriş". Sayı yok.
- Backtest ve giriş sadeliği (`not-backtest-giris-sadeligi-risk-islem-gunlugu.md`): sahibi E K18. (bilet 04, 14.10)
- Fiili dolaşım taraması (`gorsel-paket-08-fiili-dolasim-orani`; görsel ve metin birinci el; bilet 04, 14.10): Tansu: "Dolaşımdaki pay adedinin <%30 olduğu senetler ile ilgili çok tatlı stratejik taramalar gerçekleştirilebilir", "eşik değer değiştirilebilir", veri KAP'tan alınabiliyor, taramalar "sırada" (Ham, birebir). Görsel: 40 satırlık tablo (Sembol, Tarih, Fiili Dolaşımdaki Pay Adedi, Fiili Dolaşım Oranı %), oran artan sırada, görünen aralık %0,54–%13,98; Tarih sütunu 2026-05-17, 2026-06-02 ve 2026-08-16 değerlerini karışık taşır ve anlamı verilmemiştir. Parametre: yalnız <%30 (sınır < mı ≤ mı belli değil). Bu bir evren filtresidir: giriş, çıkış, stop yok. Tablodaki seviye tarama eşiği değil, çıktıdır (görselde eşik görünmüyor). TASARIM 3 ikinci dalga. Günlük veriyle: oran için KAP/İş Yatırım verisi gerekir (TASARIM 4). Aynı metin: `tweet-fiili-dolasim-yuzde-30-alti-stratejik-taramalar` (KANIT: kopya; ek tarama taslakları Claude yorumudur, Tansu'nun değil). İlişkili görüş (sayısız): `tweet-fiyat-hacim-fiili-dolasim-ucgeni` ("fiyat ve hacim resmin üçte ikisi, fiilen işlem gören pay sayısı resmi tamamlar"; hacim/fiili dolaşım oranı Claude'a ait YORUM).
- Klasik günlük pivot (`gorsel-paket-100-gunluk-klasik-pivot-formul-kod`; iki görsel okundu, Tansu'nun cümlesi yok; Python kodu görseli birinci el, infografik "NotebookLM" imzalıdır ve Tansu'nun kuralı sayılmaz; bilet 04, 14.10): önceki tamamlanmış günün H, L, C değerlerinden `P = (H+L+C)/3`, `R1 = 2P − L`, `S1 = 2P − H`, `R2 = P + (H−L)`, `S2 = P − (H−L)`, `R3 = H + 2(P−L)`, `S3 = L − 2(H−P)` (kod ve infografik aynı formülü verir). Kaynak seviyeleri tek başına sinyal saymaz; giriş, stop, hedef, seans ve düzeltme (bedelsiz) kuralı yok. Günlük bedava veriyle: evet (formül parametresiz). Pivotun IV bantları ve trend çizgisiyle kesişmesi: yalnız yazarı belirsiz ders metninde (`gorsel-paket-97-iv-sd-expected-move-bantlari`, §16'daki IV/SD satırı).
- Imbalance (FVG) gücü (`gorsel-paket-17-imbalance-gucu`; yalnız görsel; ders şeması, Ham'da yazar yok; metin yok; bilet 04, 14.10): başlık `How to judge power of Im-balance`; dört örnek: Strongest (üç yeşil mum, 1. mumun high'ı ile 3. mumun low'u arasında geniş boşluk), Strong (1. mum kırmızı, boşluk yine geniş), Weak (küçük boşluk), Weakest -Balance- (boşluk yok, 1. mumun high'ı ile 3. mumun low'u aynı çizgide). Okuma: güç boşluk büyüklüğü ve mum yön uyumuyla artar. Eşik, ATR normalizasyonu, giriş, stop yok (YORUM). Mum sayısı üç; bullish boşluk `high[t−2] < low[t]` (§10 ile aynı tanım).
- IV / standart sapma bantları (`gorsel-paket-97-iv-sd-expected-move-bantlari`; görsel `GC=F - Price Chart with Normal Distribution Analysis` birinci el, yalnız fiyat grafiği yanında normal dağılım ve renkli SD bantları; Ham gövde ders metni, Ham'da yazar yok; Tansu'nun cümlesi yalnız "şöyle biraz istatistik çalışalım"; PR #10 bot yorumu, 14.10; YORUM): normal modelde 1SD %68,2, 2SD %95,4, 3SD %99 kapsama; yükselen trendde −1SD'ye geri çekilme alım, −2SD altı stop (stop kısmı E'nin alanı; E K2 ile çelişmez, ayrı bir stop tanımı olarak kayıtlıdır), bant pivot ya da trend çizgisiyle kesişirse güçlü. Parametre: SD penceresi, IV kaynağı, vade, strike, bant formülü yok. Uygulanabilir mi: HAYIR (IV opsiyon piyasasından gelir; TASARIM §3 opsiyon verisi yok); gerçekleşen oynaklıkla SD bandı YORUM olarak kurulabilir, Tansu'nun kuralı sayılmaz.
- FVG ticaret kurulumları (`tweet-fvg-ticaret-stratejileri-gap-fading`; Ham; bilet 04, 14.10): (1) boşluğu soldurma: yukarı yönlü hareketin FVG'si için fiyatın boşluğu doldurmaya dönmesi beklenerek short, aşağı yönlü FVG için long (düzeltme bahsi); (2) boşluğun tamamen dolmasını bekle, sonra ilk hareket yönünde gir (trend devamı). "FVG'yi avlamanın en kolay yolu büyük mumları incelemektir." Hangi kurulumun ne zaman seçileceği, tetik, stop, hedef, zaman dilimi yok; yazarın kendi sonucu yok. BIST'te kısa pozisyon pratik değil (TASARIM 3). Günlük veriyle: kurulum (2) evet.
- Denge ve dengesizlik (`tweet-piyasa-denge-dengesizlik-auction-acceptance-state-machine`; Ham; bilet 04, 14.10): açılış önceki günün Value Area'sı (işlemlerin yaklaşık %68'i) içindeyse denge: aralık işlemi, VAH'ta sat, VAL'da al, hedef POC; denge gününde trend takibi "genellikle kayıpla sonuçlanır". Açılış önceki Value Area'nın tamamen dışındaysa dengesizlik: aralığa karşı işlem (fading) "son derece riskli", geri çekilmede trend yönünde işlem. 2. ve 3. standart sapmada ortalamaya dönüş eğilimi iddiası kanıtsız. Parametre: yalnız %68 (profil penceresi, bin, Value Area yüzdesi algoritması yok: YORUM). Günlük veriyle: kısmen. Açılış fiyatı veride yok (TASARIM 4), profil gün içi veri ister (TASARIM 3: kapsam dışı).
- POC, VAH, VAL ve VWAP (`tweet-poc-vah-val-vwap-auction-state-machine`; Ham ("benim kullandığım mantık"); bilet 04, 14.10): günlük VWAP ve Fixed Range veya Session Volume Profile. Fiyat VWAP ve POC üstünde: yalnız alış yönü; ikisinin altında: yalnız satış yönü; arasında: bekle. VWAP ile birlikte VAH üstüne çıkıp orada kalıcı olursa kırılım (long); VAL'ın altına sarkıp VWAP hâlâ üstteyken fiyat VAL içine dönerse hedef POC (VWAP'ın üstte kalması kaynak koşuludur). "Kalıcı" tanımı, profil penceresi, VWAP başlangıcı, stop yok. Önceki madde VAH'ta satışı, bu madde VAH üstünde kalıcılığı alış sayar; ayrım "kalıcılık" tanımına bağlıdır ve tanımsızdır (iki ayrı Tansu notu; çelişki sayılmadı). Python taraması "yazılır" denir, kod yok.
- Confluence (kesişim) tezi (bilet 04, 14.10): `tweet-confluence-bagimsiz-kanit-yogunlugu` (Tansu'nun tek cümlesi: confluence "birden fazla bağımsız teknik faktörün aynı fiyat seviyesinde buluşması", bu yüzden "daha güvenli"; faktör listesi, eşik, sonuç yok). KANIT: `gorsel-paket-112-confluence-kesisim-bagimsiz-kanit` (infografik "NotebookLM" imzalı, Tansu'nun görseli değil; destek/direnç + RSI uyumsuzluğu + Fibonacci geri çekilmesi + trend çizgisi + mum formasyonu aynı bölgede = dönüş olasılığı yüksek), `gorsel-paket-78-petkm-confluence-talep-arz` (Tansu: "confluence alanının gücü..."; PETKM grafiği, fiyat 19,88: alttaki yeşil talep kümesinden birkaç tepki, üstte kırmızı arz kümesi, Fibo seviyeleri, EMA 8 ve EMA 21, hacim; geçmiş tepki gösterir, güncel giriş kalitesini göstermez) ve `tweet-talep-bolgesi-volume-profile-momentum-confluence` (Tansu: "Bu kardeş bas basbağırmış talep bölgesinde ben geliyorum diye. Volume ayak izinden de belli"; sembolsüz grafik: talep bölgesi, yatay volume profile, hacim artışı, MACD benzeri ve RSI benzeri panellerde yukarı ivme; gerçek footprint görünmez). Seçilmiş örnekler (GC=F satırıyla aynı tür); "bağımsız faktör" olduğu kanıtlanmamıştır (göstergelerin çoğu aynı fiyattan türer).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-fiili-dolasim-yuzde-30-alti-tarama-2055700993015189733` — Fiili dolaşım evren filtresi, tekrar (16.05.2026 17:24 UTC): "Dolaşımdaki pay adedinin <%30 olduğu senetler ile ilgili çok tatlı stratejik taramalar gerçekleştirilebilir." (Ham). Veri KAP'tan alınır, taramalar "sırada"; yeni parametre yok.

---

## 17. X arşivi kısa kayıtları (16.10)
- Kanal stratejisi backtest sonucu (kural yok; `tweet-kanal-stratejisi-backtest-2088957194892923386`; Ham ve görsel birinci el, iki görsel de açıldı; Tansu'nun X gönderisi, 2026-08-16): Tansu: "Şöyle bşr strateji kodluyorum", "İlk veriler fena değil", "Biraz geliştirip bakarız" (Ham). Görsel 2 çıktısı: "Toplam İşlem : 4", "Kazanan İşlem : 4", "Win Rate : 100.0%", "Ortalama Getiri : 13.00%", "Bileşik Toplam Getiri: 60.8%". Dört işlem (giriş → çıkış, getiri %): 2024-11-05 90.60 → 2024-12-03 115.58 (27.57); 2025-02-03 115.49 → 2025-03-03 127.45 (10.35); 2025-03-19 116.14 → 2025-06-10 117.55 (1.21); 2025-09-03 128.60 → 2026-01-21 145.13 (12.86). Hesap kontrolü (bizim): ortalama (27,57 + 10,35 + 1,21 + 12,86) / 4 = 12,9975; bileşik 1,2757 × 1,1035 × 1,0121 × 1,1286 = 1,608; ikisi de tabloyla uyumlu. PnL sütunu fiyat farkından 0,10–0,13 düşüktür (örnek 115,58 − 90,60 = 24,98; tabloda 24.88); fark nedeni yazılmamış (YORUM: maliyet olabilir). Görsel 1: mum grafiği, üstte düz basamaklı çizgi, altta kesikli basamaklı çizgi (iki bant), yeşil yukarı ve kırmızı ters üçgenler; yeşil üçgenler alt banda, kırmızılar üst banda yakındır (YORUM: alt banttan al, üst banttan sat). Üçgenler yaklaşık 5 yeşil ve 5 kırmızıdır; tablodaki 4 işlemle tam uyuşmaz (YORUM: grafik daha geniş pencere). Kanalın tanımı, giriş ve çıkış koşulu, sembol (fiyat 90–145 TL), maliyet, stop ve yön yazılı değil. Basamaklı bantlar yükselen paralel kanal değildir (YORUM): §2 ile aynı yöntem sayılmaz. Tansu'nun kanıtı: dört işlem, tek sembol, "%100 kazanma"; Tansu sonucu kendisi "ilk veriler" sayar. Günlük bedava veriyle: kural tanımsız, sonuç yeniden üretilemez. Hazırlık X. Kaynak güveni: Ham ve görsel birinci el; kural yok: düşük.

---

## Sıralı özet: koda en yakın kurallar (günlük bedava veri ile)

Kodlanabilirlik sırası (kaynağın verdiği ve bizim YORUM ile doldurmamız gereken parametrelere göre):

1. Distal/Proximal + RBR bölge çizgileri (7, 8): çizgi formülü kaynakta sözlü olarak var (görsel); base seçimi YORUM. En az parametre ihtiyacı.
2. Demand bozulma kuralı (9): ilk `Close < zone_low` ile kutu biter (Ham, `gorsel-paket-13`:21); `Low < zone_low` daha katı ayrı seçenektir. Buffer YORUM.
3. BOS + Fib 0.618-0.786 + FVG/OB (10): 0.618, 0.786, stop 1.0, TP 0.0 vardır; bullish FVG üç mum boşluğudur (Ham, `gorsel-paket-107`:47–48; Ham'da yazar yok). Swing/BOS ve OB ayrıntıları YORUM.
4. Fiyat konumu vs hacim konumu (13): 252 günlük pencere, tamamen OHLCV; eşikler (%20/%80) görselden YORUM.
5. Breakout + Range Retest + FVG %50 (1): iskelet net (kutu -> breakout -> FVG -> retest -> confirmation -> entry/stop/TP1-3), 8-10 parametre YORUM.
6. Yükselen kanal alt bant teması (2): Lookback 120, temas, Low-Bant %, Kapanış-Bant %; kanal çizimi ve tolerans YORUM.
7. Düşen direnç kırılımı + talep + Fib + ABCD (3, 4): Temas 3, Lookback 20/30, EMA 5/8/13; Küm. Delta günlük veriden çıkmaz.
8. Retest (destek trendi) + EMA5/8/13 (12, 11): temas sayısı ve "temas sonrası gün" sayaçları var; giriş yok.

Kodlanamayacak veya yeterince tanımsız olanlar:
- SETUP x/100 ve "Skor 100/100 / Sınıf A+" (5, 1): puan formülü hiçbir yerde yok.
- Zone D.Touch / D.Teyit tanımları (6): açıklanmamış.
- Siyah Kuğu harmonik (3): bu bölümün kaynaklarında oranlar verilmemiş (bullish aralıklar: C §26, 16.10).
- BOM, AHENK, gizli filtre breakout (14, 16): kural açıklanmamış.
- 80-100 hafta yatay (15): tek parametre (süre).
- Küm. Delta (3): gerçek emir akışı verisi gerekir.

Tansu'nun kanıt durumu (tüm kurallar için): sistematik backtest veya gerçekleşen işlem istatistiği, bu dosyanın taradığı notlarda yok (tüm havuz taranmadı). Görseller seçilmiş örneklerdir (LIDER, GC=F, AKFIS, BOM pozitif; BALAT, AKSGY başarısız vaka olarak gösterilmiş).

## Okunmayanlar / kısmen okunanlar
- Okunmadı (yalnız adı veya görseli): `tweet-acsel-direnc-kirilimi-volume-profile-val`, `tweet-formasyon-arz-talep-confluence-kapisi`, `tweet-finans-muhendisligi-destek-direnc-seviye-motoru`, `tweet-fiyatlar-trend-halinde-hareket-eder`, `gorsel-paket-99` görsel 01/02 (yalnız 03 açıldı), `gorsel-paket-101` not gövdesinin devamı.
- Kısmen okundu (ilk ~45-140 satır): tüm -09/-10/-11/-12/-13/-15/-18/-21/-41/-44/-64/-69/-93/-99/-101/-103/-105/-117/-128 notları; gövdedeki Claude'un "Teknik Ek" formülleri ikinci el olarak işaretlendi.
- Havuz notlarının çoğunda birebir Tansu metni "Ham" bölümünde durur (örnek: `tweet-mum-govde-hacim-anomalisi-uyarisi`); bu dosyanın eski bölümleri yalnız Claude özetinden okundu, "Ham" ile çelişirse "Ham" esastır. X gönderilerine erişilmedi.
- Görsel çözünürlüğü düşük olduğundan (680 px) -10/-11/-12/-13 tablolarındaki bazı değerler yaklaşıktır.
