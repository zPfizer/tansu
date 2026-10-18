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
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-4s-kapanis-kir-retest-tut-seviyeler-2095199834374320434` — Okuma (YORUM): CRDFA örneğinde 28,52 üstünde 4 saatlik kapanış ve retest aranır. Ham: "28,52'nin üzerine yeniden çıkması ve 4 saatlik mumu bu seviyenin üzerinde kapatması gerekiyor." Devamı: "Yani kabaca kır – geri test et – tutun – devam et yapısını görmek istiyoruz." Yapısal bozulma ile stop ayrılır: "Buradaki 24,98 otomatik stop anlamına gelmiyor".

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
  - `tweet-auto-trend-channel-min-max-slope-1952070959529336857` — Başka bir kanal aracı: AKFGY'de otomatik trend kanalı, destek çizgisi "Support (min slope)", direnç çizgisi "Resistance (max slope)" (görsel metni, açıldı); kanal paralel değil, iki çizgi ayrı eğimli. Ham: "akfgy 30 günlük kanal desteğinde." Giriş, stop, sonuç yok. Parametre: Kanal penceresi = son 45 mum (AKFGY, görsel, açıldı); Ham "30 günlük kanal" der; destek = en küçük eğimli, direnç = en büyük eğimli çizgi (lejant; algoritma YORUM)
  - `tweet-auto-trend-channel-min-max-slope-1952071338971091397` — Aynı otomatik trend kanalı aracı, AYCES: "AYCES.IS Otomatik Trend Kanalı (Son 27 mum)", "Support (min slope)", "Resistance (max slope)" (görsel metni, açıldı). Destek yükselir, direnç alçalır: daralan üçgen. Ham yok ("metin yok"), koşul ve sonuç yok. Parametre: Kanal penceresi = son 27 mum (AYCES; pencere hisseye göre değişir: AKFGY 45) (görsel, açıldı)
  - `tweet-52-haftalik-kanal-haftalik-kapanis-1956049359436423409` — Okuma (YORUM): THYAO örneğinde haftalık kanal dışı kapanış teyidi aranır. Ham: "Son  günlerdeki hareketleri ile kanal dışına çıkmış görünüyor ancak haftayı kanal dışında kapatması önemli."
  - `tweet-ema20-ustu-kapanis-kanal-dibi-fibo-1770902148005441663` — YESIL kanal dibi örneği (21.03.2024): “4.40 üzeri kapanışlar hisseyi 20 günlük EMA üzerine atar.” ve “Şu anda yükselen kanal dibinde FIBO desteğine doğru ilerliyor.” (Ham). Okuma (YORUM): örnek fiyatlar genel kanal kuralının eşiği değildir.
  - `tweet-golden-cross-kanal-destegi-ema20-1770182704559964265` — Okuma (YORUM): YESIL için kanal desteğinde EMA20 üstüne çıkış beklentisi. Ham: "Şu anda kanal desteğinde. 20 günlük EMA üzerine atarsa". Cümle tamamlanmamıştır; otomatik giriş kuralı kurulmaz.
  - `tweet-haftalik-kanal-alt-bant-yesil-kapanis-1956081917054607589` — Okuma (YORUM): Haftalık alt bant temasında yeşil mum şartı. Ham: "Alt banda gelip haftalık yeşil yanmalı. Çok önemli nokta".
  - `tweet-kanal-destek-swing-tarama-1989047300254003339` — Okuma (YORUM): BERA destek yakını taramasının tarihli örneğidir (13.11.2025). Açılan G1: "DESTEK YAKININDA", "Son Swing: HH (2025-11-04)" ve "(120 Barlık Kanal)". Bu örnek penceresi diğer hisselere zorunlu değer yapılmaz.
  - `tweet-kanal-destek-yakini-taramasi-1984032255535443993` — Okuma (YORUM): DOCO örneği farklı kanal penceresini gösterir. Ham: "Bence bunu takip edin," (30.10.2025). Açılan G1: "DESTEK YAKININDA" ve "(60 Barlık Kanal)". 60 bar bu örneğin ayarıdır.
  - `tweet-swing-low-dogrulamali-kanal-dibi-2096605373905936804` — Okuma (YORUM): Kanal dibinin geçmiş swing dipleriyle doğrulanması önemlidir. Ham: “alt çizginin geçmişte birkaç ayrı swing low tarafından doğrulanmış olması o seviyeyi daha anlamlı yapar.”
  - `tweet-swing-temasli-kanal-alt-bant-2096602760196010169` — Okuma (YORUM): Swing noktalarına göre kanal çiziminin eşlik eden örneği. Ham: “Bir de swing noktalarına göre yapalım şu işi:)”. Görsel metni üst ve alt swing temaslarını, güncel alt bant temasını ayrı etiketler.
  - `tweet-trend-cizgisi-pivot-paralel-kanal-2096653615624810555` — Okuma (YORUM): Tansu, CMT anlatımına atıfla çizgi ve kanal kurmayı açıklar. Ham: “düzgün trend çizgisinin benzer büyüklükteki support/resistance pivotlarını bağlaması gerektiği” ve “kanalın da karşı taraftaki pivot üzerinden paralel çizgiyle oluşturulduğu belirtiliyor.”

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-dusen-trend-kirilimi-duk-bos-2016214167884046802` — Tansu'nun "Güncellenmiş yeni price action çalışmamız" (Ham): A1CAP düşen trend kırılımı (DÜK) aracı; başlık "DÜŞEN TREND KIRIMI (DÜK) | Lookback: 90 gün", ilk temas 2025-10-31, kırılım 2026-01-27 (görsel, açıldı). "DÜK FVG, talep bölgesi, arz bölgesi, BOS, Swing point ne ararsan var" (Ham). Hedef ve stop henüz yok: "buna ekleriz hedef stop los" (Ham). Parametre: DÜK aracı Lookback = 90 gün; eğim −0,037773 (−2,16°); EMA seti 9/21/50/100/200 (görsel, açıldı)
  - `tweet-dusuk-volatilite-hacim-kirilim-secimi-2054246716367356080` — Sembolsüz ek örnek, beş nitelikle seçim: "hem volatiltiesi düşük hem hacmi yüksek hem dengeli yükseliyor hem talep toplamadan tepki almış hem alpha yaratıyor" (Ham, 12.05.2026). Görselde (açıldı): kırmızı düşen çizgiye yaklaşan fiyat, alt tarafta yeşil talep kutusu, üç kısa EMA, son bar uzun yeşil mum ve yüksek hacim. Eşik yok; "yarının tavanlarından birisi olmaya aday" bir beklentidir, sonuç yok. Dengeli yükseliş ve alpha için bkz. B §34 (dengeli momentum ölçümü).
  - `tweet-dusen-kanal-cati-kirilimi-2011861215753175534` — Çatı kırılımı örneği (15.01.2026): “ÇAAAAT diye kırmış geçmiş çatıyı:)” (Ham; görsel açıldı). Okuma (YORUM): son yeşil mum düşen kırmızı üst çizgiyi aşar; tek örnek genel giriş kuralının bütün koşullarını vermez.
  - `tweet-dusen-trend-cizgisi-kirilimi-1949682917057204298` — ASTOR trend kırılımı örneği (28.07.2025): “Trendline Breakout - İlk Temas: 2025-03-17, Entry: 2025-07-25” (görsel metni). Okuma (YORUM): tarihler tarama örneğine aittir.
  - `tweet-dusen-kanal-kirilim-retest-2097063290224431474` — `tweet-dusen-kanal-kirilim-retest-2097063290224431474` (2026-09-07; Ham ve varsa görsel metni). Görsel metni: "TLMAN.IS — DÜŞEN KANAL YUKARI KIRILIM". Görsel metni: "RETEST + TUTUNDU". Okuma (YORUM): düşen kanalın üst sınırını aşma örneğidir; bölümdeki talep ve EMA birleşiminin bütün şartlarını bu örneğe aktarmayız. Örnek ekran pencereleri genel parametre değildir.
  - `tweet-dusen-kanal-kirilim-taramasi-2011135212382761149` — `tweet-dusen-kanal-kirilim-taramasi-2011135212382761149` (2026-01-13; Ham ve varsa görsel metni). Görsel metni: "BRYAT.IS — SON GÜN DÜŞEN KANALI YUKARI KIRDI". Okuma (YORUM): düşen kanalın üst sınırını aşma örneğidir; bölümdeki talep ve EMA birleşiminin bütün şartlarını bu örneğe aktarmayız. Örnek ekran pencereleri genel parametre değildir.
  - `tweet-dusen-kanal-yukari-kirilim-taramasi-2016954643394216029` — `tweet-dusen-kanal-yukari-kirilim-taramasi-2016954643394216029` (2026-01-29; Ham ve varsa görsel metni). Görsel metni: "ARCLK.IS — DÜŞEN KANALI YUKARI KIRDI". Okuma (YORUM): düşen kanalın üst sınırını aşma örneğidir; bölümdeki talep ve EMA birleşiminin bütün şartlarını bu örneğe aktarmayız. Örnek ekran pencereleri genel parametre değildir.
  - `tweet-dusen-kanal-yukari-kirilim-taramasi-2016967838120964296` — `tweet-dusen-kanal-yukari-kirilim-taramasi-2016967838120964296` (2026-01-29; Ham ve varsa görsel metni). Görsel metni: "BRISA.IS — DÜŞEN KANALI YUKARI KIRDI". Okuma (YORUM): düşen kanalın üst sınırını aşma örneğidir; bölümdeki talep ve EMA birleşiminin bütün şartlarını bu örneğe aktarmayız. Örnek ekran pencereleri genel parametre değildir.
  - `tweet-dusen-kanal-yukari-kirilim-taramasi-2023815727309091176` — `tweet-dusen-kanal-yukari-kirilim-taramasi-2023815727309091176` (2026-02-17; Ham ve varsa görsel metni). Görsel metni: "BRYAT.IS — DÜŞEN KANALI YUKARI KIRDI". Okuma (YORUM): düşen kanalın üst sınırını aşma örneğidir; bölümdeki talep ve EMA birleşiminin bütün şartlarını bu örneğe aktarmayız. Örnek ekran pencereleri genel parametre değildir.
  - `tweet-kanal-kirilim-mum-hacim-teyit-1958076016649253338` — `tweet-kanal-kirilim-mum-hacim-teyit-1958076016649253338` (2025-08-20; Ham ve varsa görsel metni). Ham: "sonraki muma bakılır ise teyit almış. Fakat hacim ortalamamın altında" / "13 günlük ortalamasını geçemedi henüz". Okuma (YORUM): sonraki mumun teyidi tek başına yeterli görülmez; hacim ortalamasının dönemi 13 olarak atanmaz.
  - `tweet-kanal-kirilim-uyumsuzluk-rsi-1998133231846306061` — `tweet-kanal-kirilim-uyumsuzluk-rsi-1998133231846306061` (2025-12-08; Ham ve varsa görsel metni). Ham: "harika bir kanal kırılımı" / "uyumsuzluklar" / "RSI yukarı kesmiş". Okuma (YORUM; görsel açıldı): kanal, uyumsuzluk ve RSI teyitleri birlikte izlenir; kesilen RSI çizgisinin sayısal eşiği çıkarılmaz.
  - `tweet-kanal-kirilimi-marubozu-hacim-teyidi-1987233906827903088` — `tweet-kanal-kirilimi-marubozu-hacim-teyidi-1987233906827903088` (2025-11-08; Ham ve varsa görsel metni). Ham: "Güzel bir marubozu ama hacim mumu bunu pek teyit etmedi. Siz bilirsiniz." Okuma (YORUM): DITAS kırılımında marubozu, hacim teyidinin yerini tutmaz.
  - `tweet-kanal-kirilimi-vwap-momentum-filtresi-2048151591279104244` — `tweet-kanal-kirilimi-vwap-momentum-filtresi-2048151591279104244` (2026-04-25; Ham ve varsa görsel metni). Ham: "28 haftalık kanalı kırmış, WVAP üstüne atmış, momentum+ filtresinden geçmiş düşeni kırmış vs vs:)". Okuma (YORUM): haftalık örneğin penceresi korunur; momentum+ hesabı ve WVAP yazımı düzeltilerek yeni kural türetilmez.

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
- Modül 1'de kullanımı: KURALLAR §3 (hedef: fiyatın üstündeki arz bölgesi; çıktı tablosunda temas ve teyit sütunları, ikisi de YORUM).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-altin-aktif-talep-arz-bolgesi-tablosu-2088348115099095392` — ALTIN (GC=F) bölge tablosu (14.08.2026): "hedefimiz 4631 call duvarı aktif arz alanı ise 4677-4775" (Ham). Görsel (görsel, açıldı): başlık "GC=F - Demand & Supply Bölgesi Analizi"; tablo sütunları "Son Fiyat | Max | Min | Aktif Demand | D.Touch | D.Teyit | Aktif Supply | S.Touch | S.Teyit"; tek veri satırı "4,432.00 | 5,586.20 | 3,310.10 | 3,896.08 - 4,001.30 | 6 | 2025-11-13 | 4,677.60 - 4,775.63 | 1 | 2026-05-27" (görsel metni). Ham'daki aktif arz alanı ile tablodaki Aktif Supply aynı aralıktır. Grafikte mavi, sarı, kırmızı ve gri kutular vardır; renklerin anlamı yazılı değil; kutunun başlangıcı ile D.Teyit ve S.Teyit tarihi arasındaki ilişki görselden okunamıyor. Parametre: D.Touch = 6 ve S.Touch = 1 (görsel metni; temas tanımı yok, YORUM); teyit tarihi D.Teyit = 2025-11-13 ve S.Teyit = 2026-05-27 (görsel metni; tanım yok, YORUM)
  - `tweet-arz-talep-bolgesi-hedef-2085799233915912673` — DOAS örneği (07.08.2026): "üsteki supply alanına kadar yolu açık." ve "Aşağısı baya sağlam talep alanlerı" (Ham). Görsel (görsel, açıldı): fiyatın üstünde kırmızı arz kutuları, altında yeşil talep kutuları, EMA çizgileri; yazı yalnız yapı etiketleridir: "HH", "LH", "BOS", "HH", "HL", "LL", "BOS" (görsel metni). Tablo, sayı ve bölge sınırı yok. Parametre: hedef = fiyatın üstündeki supply alanı (Ham; birden çok arz kutusu varken hangisi olduğu yazılı değil, YORUM: en yakın)
  - `tweet-arz-bolgesi-abcd-hedef-2090911685569548578` — Okuma (YORUM): TMPOL için tarihli satış aralığı örneğidir. Ham: "640-700 verin gitsin". Bu fiyat aralığı başka hisselere taşınmaz.
  - `tweet-arz-bolgesi-hacimli-kirilim-2009325605515587913` — Okuma (YORUM): ASTOR örneğinde arz bölgesinin hacimli aşılması izlenir. Ham: "Bu aslan parçası arz alanlarını hacimli geçerse tarihi zirvelere merhaba diyebilir. İzliyoruz".
  - `tweet-arz-bolgesi-kirilimi-hsar-hedefi-2088519987409367136` — Okuma (YORUM): ENKAI için 92,50–95,72 bölgesinin aşılması sonrasında HSAR yeniden değerlendirilir. Ham: "92.50 , 95.72 alanını bu bilanço ile yıkıp geçer ise direk HSAR alanına girer. Orada bir daja bakmak lazım".
  - `tweet-arz-bolgesi-tekrar-temas-2088351754479898697` — Okuma (YORUM): PRZMA örneğinde aynı arz bölgesine yeniden geliş uyarıdır. Ham: "Yine aynı arz bölgesinde dikkattt".
  - `tweet-arz-talep-ema-5-8-13-mum-formasyonu-2002099118366486932` — Okuma (YORUM): KRONT örneğinde üç kriter üzerine OB yapısı eklenerek sinyal derecesi açıklanır. Ham: "mesela 3 kriteri sağlayıp üstüne Ob yapısı ile öne çıktı ve 1. derecede dip sinyali verdi." Üç kriter bu alıntıdan adlandırılamaz.

---

## 7. Distal / Proximal çizgiler (-09)
- Kaynak: `gorsel-paket-09-distal-proximal-arz-talep.md`; `assets\gorsel-paket-09-distal-proximal\01-distal-proximal-arz-bolgesi.png` (İngilizce ders diyagramı, Tansu'nun aracı değil; Levent kaynak olarak iletmiş; Ham'da yazar yok).
- Tansu'nun ifadesi (görsel, verbatim): "The distal line is located at the highest of the basing structure while the proximal line is placed at the lowest body price of the base." Diyagram: yükselen mumlar, `Base`, sonra düşüş (rally-base-drop). `Distal line` = base'in en yükseği; `Proximal line` = base'teki en düşük gövde fiyatı.
- Tanım: arz bölgesi: distal = max(high[base]); proximal = min(min(open,close)[base]). Talepte proximal/giriş ve distal/stop ilişkisi eğitim şemasında vardır (Eğitim, G15/g1). YORUM: distal = min(low[base]), proximal = max(max(open,close)[base]); base veya leg-out seçiminin evrensel formülü verilmez.
- Parametreler: base seçimi (kaç mum, gövde/range oranı) YOK; YORUM.
- Giriş: proximal çizgi; stop = distal çizgi (Eğitim, G15/g1: giriş/proximal ve distal/stop ilişkisi).
- Modül 1'de kullanımı: KURALLAR §3 (arz ve talep bölgesinin proximal ve distal çizgisi; çizgi seçimi YORUM).
- Tansu'nun kanıtı: yok. Günlük veriyle: evet. Kaynak güveni: diyagram net ama Tansu'ya atfı doğrulanmadı; Ham: "Distal line ve proximal line'ı kavrarsak bu işişn %50'si biter, kalan %50'si de taramasını anlayabilmek".

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-proximal-line-en-dusuk-govde-2088907925704110444` — - `tweet-proximal-line-en-dusuk-govde-2088907925704110444` (2026-08-16; Ham): Gövde sınırı (Ham): "Kural gereği proximal line, o base bölgesi içindeki en düşük gövde fiyatına çiziliyor." Renk ayrımı: "Yani  renge değil o bölgedeki en düşük gövde kapanışına ya da açılışına bakıyoruz."

## 8. RBR (Rally-Base-Rally) talep bölgesi (-15)
- Kaynak: `gorsel-paket-15-rbr-demand-zone.md`; `assets\gorsel-paket-15-rbr-demand-zone\01-rally-base-rally-rbr-pattern.png` (ders diyagramı, Tansu aracı değil).
- Tansu'nun ifadesi (görsel, verbatim): `RBR PATTERN`, `LEG IN CANDLE`, `BASE CANDLE`, `LEG OUT CANDLE`, `ENTRY POINT`, `Proximal line`, `Distal line / stop loss`; "NOTE: The area between proximal line and distal line is area of demand which is known as demand zone. DISTAL line always be at the low of base candle or leg out candle in RBR pattern."
- Tanım: yükselişte leg-in (yeşil büyük mum) -> 1+ küçük base mumu (renk önemli değil) -> leg-out (büyük yeşil). Eğitim şemasında proximal = giriş; distal = stop, base veya leg-out dibindedir (Eğitim, G15/g1). YORUM: proximal base üst gövde seviyesi civarı; distal base low veya leg-out low'un küçüğü; evrensel seçim formülü açık değildir.
- Parametreler: base mum sayısı, "küçük" gövde eşiği, leg-out büyüklüğü: yok (YORUM).
- Giriş / stop: görselde var (proximal/entry, distal/stop); hedef yok. Not'un base kapıları listesi Claude önerisidir.
- Modül 1'de kullanımı: KURALLAR §3 (RBR yapısı ayrıca aranmaz; bölge sponsor mumdan kurulur).
- Kanıt yok. Günlük veriyle evet. Güven: ders diyagramı; Ham'da yazar yok (yalnız görsel); genel eğitim materyali.

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-rbr-formasyonu-proximal-distal-stop-2088173211544400060` — - `tweet-rbr-formasyonu-proximal-distal-stop-2088173211544400060` (2026-08-14; Ham): Eğitim görseli (açıldı): "DISTAL line always be at the low of base candle or leg out candle  in RBR pattern". Okuma (YORUM): proximal giriş, distal stop çizgisidir; mevcut RBR şemasının yinelenen kaynağıdır.

## 9. Talep bölgesi bozulması (invalidation) (-13)
- Kaynak: `gorsel-paket-13-ttkom-demand-invalidation.md`; TTKOM görseli.
- Tansu'nun ifadesi: tweet (Ham): demand bölgesinin en düşük fiyatı `zone_low`; oluşum sonrası ilk mum `close < zone_low` (veya daha katı: `low < zone_low`) ise kutu o tarihte biter. Görselde kırmızı ok, gri kutunun kırılım tarihinde bittiği yeri gösteriyor (birinci el).
- Tanım: oluşum sonrası ilk `Close < zone_low` mumunda kutu biter (Ham, `gorsel-paket-13`:21). `Low < zone_low` daha katı ayrı seçenektir; aracın hangi seçeneği kullandığı açık değildir.
- Parametreler: buffer yok. YORUM: 0.
- Modül 1'de kullanımı: KURALLAR §3 (bölge bozulması: talepte ilk kapanış distal çizginin altında, arzda aynası).
- Giriş/stop/hedef: yok (bozulma kuralı olarak stop mantığına doğrudan bağlanabilir). Kanıt yok. Günlük evet. Güven: orta.

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-destek-kirilimi-sonraki-bolge-hedef-2088528889135984684` — HALKB destek kaybı örneği (15.08.2026): “#HALKB çok güçlü bir destek bölgesini kırdı” ve “28-30 arasına çekilecek gibi duruyor” (Ham). Okuma (YORUM): olasılık bildiren örnek hedefidir; bölge bozulması için mevcut kapanış koşulunu değiştirmez.

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
  - `tweet-bayrak-talep-fvg-fibo-uyumu-2003159460018368565` — Konfluans kontrol listesi: "Bayrak demand zone fvg fibo herşey hazır" (Ham). Dört görselde (açıldı): itki sonrası eğimli bayrak kanalı (G4), yeşil talep bölgesi ve üstünde sarı FVG kutusu (G2, G3), kesikli yatay Fibo düzeyleri ve BOS etiketi (G3). Yeni öğe: bayrak. Sembol, sayı, giriş, stop, sonuç yok.

---

## 11. Trend desteği (yükselen) + demand + FVG + BOS (GEDZA -93)
- Kaynak: `gorsel-paket-93-gedza-demand-bos-hacim-momentum.md`; `assets\gorsel-paket-93-...\01-gedza-trend-demand-fvg-bos-hacim.jpg`.
- Tansu'nun ifadesi (görsel başlık/lejant, verbatim): `GEDZA - Fiyat: 31.10`; lejant `EMA 5, EMA 13, Trend Destek, Temas, En Yakın Demand, En Yakın FVG, BOS` (Araç, G93/g1, sol üst lejant). Alt paneller Hacim, MACD, ADX, RSI.
- Tanım: yükselen "Trend Destek" çizgisi (cyan) iki+ pivot low'dan; fiyat sağ uçta çizgi ve yeşil "En Yakın Demand" kutusuna iniyor ("Temas" üçgeni), büyük yeşil tepki mumu, son hacim çubuğu çok yüksek; altta "En Yakın FVG" kutusu; yatay BOS çizgisi üstte.
- Parametreler: EMA 5/13 (Araç, G93/g1, sol üst lejant); ADX/RSI/MACD periyodu yok (YORUM); temas toleransı yok.
- Giriş/stop/hedef: yok. Kanıt: yok. Not'un "MACD negatif, ADX zayıf: karışık teyit" yorumu Claude'a ait. Günlük veriyle evet. Güven: düşük-orta.

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-fvg-yukselen-dip-talep-bolgesi-1989395710215876953` — `tweet-fvg-yukselen-dip-talep-bolgesi-1989395710215876953` (2025-11-14): Yükselen dip teyidi: "bir önceki yükselen dip (HL) seviyesine veya bu seviyelerin üzerinde oluşturulmuş bir destek/talep bölgesine (demand zone) kadar inmesi idealdir." (Ham). Okuma (YORUM): düzeltmenin piyasa yapısıyla birlikte değerlendirilmesi önerilir.
  - `tweet-trend-destek-talep-bolgesi-temas-2053490970067345557` — Okuma (YORUM): Trend desteği ile talep bölgesinin birlikte izlendiği grafik örneği. G1 açıldı: “Trend Destek”, “Temas”, “En Yakın Demand” ve “BOS”. Ham: “Şuradan da artık gidersin sanırım:)”. Okuma (YORUM): Beklenti kesinleşmiş sonuç değildir.
  - `tweet-trend-destek-talep-macd-rsi-stop-2016244555516150121` — Okuma (YORUM): CIMSA'da destek ve talep birleşimi, MACD teyidi ve koşullu stop. Ham: “Fiyat hem mavi trend çizgisine hem de bu yeşil kutucukların olduğu bölgeye gelince alıcılar devreye girmiş.” MACD: “Mavi çizgi, turuncu çizgiyi yukarı kesmiş ve yeşil çubuklar oluşmaya başlamış.” Stop: “Eğer hisse fiyatı mavi çizginin altına (yaklaşık 45-46 TL seviyelerinin altına) iner ve orada kalıcı olursa” ve “stop olunması gerekir.” Okuma (YORUM): Fiyat düzeyleri bu örneğe aittir.

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ema-hacim-macd-adx-rsi-uyumu-1983116120421740749` — DAGI örneği (28.10.2025): Ham teyit listesi (satırlar): "ema5>ema8>ema13" "volume ortalamadan yüksek" "macd histogram pozitife geçmiş al gelmiş" "adx yükselmiş"; "dünkü ana momentum listemizde idi." Görsel (açıldı): "Yükselen destek TEMAS: DAGI.IS", ilk temas 2025-08-18, son 2025-10-24; ADX 25,44 (20 çizgisinin altından yükselmiş), RSI 65,22, MACD 0,098. Parametre: Teyit seti (Ham, sayısal eşik yok): hacim > ortalama; MACD histogramı negatiften pozitife ve "Alım Sinyali"; ADX yükseliyor (görsel, açıldı: ADX (14), kesikli 20 çizgisi altından 25,44'e); RSI yüksek (Ham: "rsı coşmuş"); değer 65,22 (görsel, açıldı); 50 eşiği YORUM
  - `tweet-rising-trendline-touch-scan-lookback-1952069518538481977` — - `tweet-rising-trendline-touch-scan-lookback-1952069518538481977` (2025-08-03; Ham): Ham: "çok daha uzun periyotlular var onlar da grupta:)". Görsel (açıldı): "Lookback" sütununda 30, 35, 40 ve "TAKİP ET" etiketleri görünür. Okuma (YORUM): tarama örneğinin pencereleridir; evrensel temas toleransı olarak alınmaz.
  - `tweet-trend-destegi-retest-taramasi-2002797123147014190` — Okuma (YORUM): CRFSA yükselen destek tekrar temas ekranı. G1 açıldı: “EMA5 > EMA8 > EMA13”, “RETEST VAR (3 kez)” ve “Temas Sonrası: 9 gün”. Okuma (YORUM): Bunlar tek ekranın gözlemleridir; üç temas veya dokuz gün genel eşik yapılmaz.
  - `tweet-trend-destegi-temas-taramasi-2031773111981379623` — Okuma (YORUM): Destek teması adaylarının sonradan sonuç tablosu. Ham: “6 Mart itibari ile yükselen trend desteğine temas eden hisselerin getirileri”. Okuma (YORUM): Bu sonuç sunumudur; tablonun DEY marjı gerçekleşmiş işlem getirisi sayılmaz.
  - `tweet-yukselen-destek-temas-ema-dizilimi-1986488325180432605` — `tweet-yukselen-destek-temas-ema-dizilimi-1986488325180432605` (2025-11-06). TATEN örneği: "Yükselen destek TEMAS: TATEN.IS" ve "EMA5 > EMA8 > EMA13" (görsel, açıldı). Okuma (YORUM): temas ile kısa EMA dizilimi aynı çıktı üzerinde sunulur.
  - `tweet-yukselen-destek-temas-taramasi-1983105054354575727` — `tweet-yukselen-destek-temas-taramasi-1983105054354575727` (2025-10-28). ARASE örneği: "Yükselen Destek Teması" (G1, açıldı). Okuma (YORUM): G1 destek trendi, hacim, ADX ve RSI panellerini birlikte verir; G2 kırmızı çizgilerle işaretlenmiş mum grafiğidir.
  - `tweet-yukselen-trend-destegi-temas-retest-ema-2011131498876031008` — `tweet-yukselen-trend-destegi-temas-retest-ema-2011131498876031008` (2026-01-13). EMA teyidi bekleyişi: "Bu kardeş yarın 5-8-13 olursa güzelleşir." (Ham). Okuma (YORUM): temas sonrası henüz tamamlanmamış dizilim beklentisidir.
  - `tweet-yukselen-trend-temasi-sar-dip-1950999922742010108` — `tweet-yukselen-trend-temasi-sar-dip-1950999922742010108` (2025-07-31). Trend temasıyla SAR teyidi: "Örneğin yükselen trende temas etmiş ve oradan aldırmış." ve "trende temas ettiği aynı tarihlerde dip dönüşü yapmış." (Ham). Okuma (YORUM): SAR eklemesi plan olarak sunulur.

---

## 13. Fiyat konumu vs hacim konumu (-128)
- Kaynak: `gorsel-paket-128-fiyat-hacim-konum-proxy-cot-kalabalik-dip.md`; görseller `assets\gorsel-paket-128-fiyat-hacim-konum-proxy\01-fiyat-hacim-konum-scatter-rsi.png`, `02-secilmis-dip-sonrasi-fiyat-grafigi.png`.
- Tansu'nun ifadesi (görsel eksen etiketleri, verbatim): X `FİYAT KONUMU (%0 = Yıllık Dip, %100 = Yıllık Tepe)`; Y `HACİM/İLGİ KONUMU (%0 = Hacimsiz, %100 = Yoğun)`; renk `RSI Gücü` (20-80); sol üst yeşil kutu `DİP OLUŞUMU? (Yüksek Hacim, Düşük Fiyat)`; sağ üst kırmızı `AŞIRI ISINMA (Yüksek Hacim, Yüksek Fiyat)`; `SON GÜN`. Tweet (Ham): 252 günlük fiyat konumu + 252 günlük hacim konumu, yfinance verisiyle, COT verisi olmadığı için proxy.
- Tanım: fiyat_konumu = (kapanış - 252g min) / (252g max - 252g min) x 100. Hacim konumu benzer şekilde 252 gün içindeki hacmin yüzdelik/min-max konumu (hangisi olduğu belirtilmemiş, YORUM). Dip adayı: fiyat <~%20, hacim >~%80 (kutu sınırları görselden: x 0-20, y 80-100). Aşırı ısınma: x 80-100, y 80-100.
- Parametreler: pencere 252 (tweet, Ham); kutu sınırları ~%20/%80 (görselden kaba okuma); RSI periyodu bilinmiyor.
- Giriş/stop/hedef: yok. Kanıt: tek seçilmiş dip örneği (ok), sistematik yok. Günlük veriyle: evet, tam uygulanabilir (yalnızca OHLCV). Güven: eksen tanımı birinci el; hacim konumu formülü belirsiz.

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-acilis-genis-mum-dusuk-hacim-teyitsiz-1992161805087408487` — Okuma (YORUM): Açılıştaki geniş gövdeli düşük hacimli mum için sonraki mumun hacmi teyit olarak okunur. Ham: "Şayet bu ilk hareketi takip eden bir sonraki mum da hacim artışıyla desteklenmezse, bu durum yükselişin teyit edilmediğini gösterir".
  - `tweet-fiyat-ilgi-konum-haritasi-1994695797506486682` — `tweet-fiyat-ilgi-konum-haritasi-1994695797506486682` (2025-11-29): XU100 örneğinde trend yorgunluğu: "Fiyat hala yüksek ama ilgi bitmiş. Yakıt tükeniyor." ve "Karar: UZAK DUR." (Ham). %75.0 fiyat, %26.9 ilgi ve RSI 55.4 bu tarihli rapor değerleridir.
  - `tweet-hacim-artan-fiyat-sabit-tarama-1839726755650683032` — Okuma (YORUM): Geliştirilmesi planlanan hacim/fiyat filtresi. Ham: "Burada hacim artmış fiyat artmamış hisseler bulmak için filtre koyacağım." Manuel inceleme olasılığı: "grafikte manuel de bakılarak karar verilebilir sanırım".

## 14. Konsolidasyon kutusu sınırı (gövde/fitil) (-18) ve uzun yatay + kırılım ("Point A -> Point B") (-44, -41)
- Kaynak: `gorsel-paket-18-konsolidasyon-body-wick.md`, `gorsel-paket-44-basit-gizli-filtre-breakout-kesfi.md`, `gorsel-paket-41-konsolidasyon-suresi-kirilim-siddeti.md`; görseller `assets\gorsel-paket-18-...\01-konsolidasyon-body-wick-bolge.jpg` (TradingView ekran görüntüsü, mor kutular), `assets\gorsel-paket-44-...\01-point-a-b-gizli-filtre-breakout.png` (etiketler `Point A (Start)`, `Point B (Breakout)`), `assets\gorsel-paket-41-...\01-ok-konsolidasyon-suresi-kirilim-siddeti.png`.
- Tansu'nun ifadesi (tweet, Ham): -18: üst sınır = en yüksek mumun gövde ucu, alt sınır = en düşük mumun fitil ucu. -44: "hep göz önünde olan 1-2 filtre ile enteresan bir breakout sinyali var aslında" — filtreler açıklanmamış. -41: "okların bulunduğu alan yatayda ne kadar genişse (konsolidasyon uzunsa) kırılım o kadar şiddetli"; Tansu görseldeki kısa konsolidasyona rağmen güçlü kırılıma şaşırdığını söylüyor.
- Tanım: -18: zone_upper = max(open,close) of highest-high candle; zone_lower = min(low). -44/-41: uzun yatay kutu başlangıcı Point A, üst bandın aşıldığı Point B; -44'te sarı MA benzeri çizgi ve mavi noktalı trailing/zarf var (kimliği yok).
- Parametreler: tümü yok (filtre, süre, kutu yüksekliği); YORUM: süre ve ATR-normalize yükseklik.
- Giriş/stop/hedef: yok. Kanıt: seçilmiş; -41 hipotez ("uzun konsolidasyon -> güçlü kırılım") test edilmemiş. Günlük veriyle: evet (kural yazılabilir) ama gizli filtre kopyalanamaz. Güven: düşük.
- Modül 1'de kullanımı: KURALLAR §3 (kutu sınırı: alt sınır en düşük mumun fitil ucu; üst sınır varsayılanda bizim seçimimiz, gün yüksekliği, YORUM; `kutu_govde` varyantında gövde ucu).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-yatay-konsolidasyon-7-30-gun-yuzde10-1939569795696922684` — Yatay kanal (konsolidasyon) anlatımı ve tarama kodu (30.06.2025). Stop: "stop-loss seviyelerini bu bandın hemen dışına koymak rasyonel bir risk yönetimidir." (Ham). Giriş: "Kanalın yukarısı hacimle kırılırsa alım" (Ham). Görsel (görsel, açıldı): "AKMGY.IS | 30 gün yatay (183.30 - 200.00) | Başlangıç idx: 588" ve "AKMGY.IS: 30 gün boyunca yatay kanal, % değişim: 9.11% (2025-05-14 ~ 2025-06-27)" (görsel metni). Parametre: kanal = son 2 ayda en az 7 en fazla 30 gün boyunca %10'dan fazla hareket etmeyen bölge (Ham); stop mesafesi = bandın hemen dışı, tampon sayısı yok (Ham)
  - `tweet-uzun-yatay-kanal-destek-kontrolu-1963314020007776602` — `tweet-uzun-yatay-kanal-destek-kontrolu-1963314020007776602` (2025-09-03). Kanal desteğinde izleme örneği: "Şöyle 37 haftalık bir kanal hareketi var kanal desteğinde:)" ve "Artık buradan kontrol etmek lazım" (Ham).
  - `tweet-uzun-yatay-kanal-kirilimi-1942335188551299102` — `tweet-uzun-yatay-kanal-kirilimi-1942335188551299102` (2025-07-07). Seçilmiş kırılım örneği: "48 hafta boyunca yatay giden hissede 30 Hazirandaki bu kırılım 1 haftada %15 kazandırmış." (Ham). Okuma (YORUM): süre ve kazanç örneğe aittir.
  - `tweet-uzun-yatay-kanal-kirilimi-1942336701864513740` — `tweet-uzun-yatay-kanal-kirilimi-1942336701864513740` (2025-07-07). Seçilmiş örnek: "52 hafta yatayda giden bu hisse 1 haftada %30 vermiş" ve "Kırılıma dikkat" (Ham).
  - `tweet-uzun-yatay-kanal-kirilimi-1943003364905660588` — `tweet-uzun-yatay-kanal-kirilimi-1943003364905660588` (2025-07-09). Çoklu zaman örneği: "Haftalık kırılım var günlük grafik de iyi, bence bakılmaya değer" (Ham).
  - `tweet-yatay-bant-alt-temas-2096651255514821058` — `tweet-yatay-bant-alt-temas-2096651255514821058` (2026-09-06). Yatay süre örneği: "65 hafta yatay gitmiş işimize yarar mı gençler:)" (Ham). Okuma (YORUM): örnek süre, genel tarama alt sınırı değildir.
  - `tweet-yatay-kanal-bant-kirilim-fake-breakout-1942087033247166573` — `tweet-yatay-kanal-bant-kirilim-fake-breakout-1942087033247166573` (2025-07-07). Bant işlemi: "En çok uygulanan yöntemlerden biri kanalın alt bandına yaklaşıldığında hisse almak, üst banda yaklaşıldığında ise satmaktır." Teyit: "En önemli konu, işlemleri yaparken mutlaka stop seviyeleri belirlemek ve hacimle teyit almaktır." (Ham). Okuma (YORUM): hacimli kırılımda kırılan yön; sahte kırılımda kanal içine dönüş sonrası ters yön anlatılır.
  - `tweet-yatay-kanal-kirilim-haftalik-teyit-1948102083556626664` — `tweet-yatay-kanal-kirilim-haftalik-teyit-1948102083556626664` (2025-07-23). Haftalık teyit örneği: "Sonra çaat diye bir önceki hafta breakout yapmış" ve "Geçen hafta da kanalın üzerinde kapatmış" (Ham).
  - `tweet-yatay-kanal-kirilim-teyit-taramasi-1962962557699871050` — `tweet-yatay-kanal-kirilim-teyit-taramasi-1962962557699871050` (2025-09-02). AYCES örneğinin etiketi: "YUKARI KIRILIM Teyitli (önceki hafta breakout, son hafta teyit)" (görsel, açıldı).
  - `tweet-yatay-kanal-tarama-akd-1939003175484133714` — `tweet-yatay-kanal-tarama-akd-1939003175484133714` (2025-06-28). Tarama sonrası inceleme: "Python'ın gücünü de kullanarak yatayda giden hisseleri çıkarıp AKD ve takaslarına bakmaya başlayacağız." (Ham).
  - `tweet-yatay-kanal-tespiti-1942198658486686133` — `tweet-yatay-kanal-tespiti-1942198658486686133` (2025-07-07). Yatay süre örneği: "52 hafta yatay kanalda giden bir hisse. Bakın bence." (Ham). Okuma (YORUM): OFSYM örneğidir; evrensel süre eşiği değildir.
  - `tweet-yatay-konsolidasyon-dongu-kirilim-1987071191442497586` — `tweet-yatay-konsolidasyon-dongu-kirilim-1987071191442497586` (2025-11-08). Konsolidasyon davranışı: "Panik satışlarını karşılayarak dipten alıp, fiyat tekrar dirence geldiğinde (herkes tekrar alım yaparken) satış yapanlar." (Ham). Okuma (YORUM): destek-direncin yatırımcı psikolojisiyle açıklanan döngüsüdür.
  - `tweet-yatay-tarama-akd-takas-1940885669381054705` — `tweet-yatay-tarama-akd-takas-1940885669381054705` (2025-07-03). Yatay adaylarda takip: "sonra AKD dağılımına ve takasa bakıyorum, kurumsal alıcıların alımlarını izliyorum." (Ham). Okuma (YORUM): anlık veriyle otomasyon sonraki plan olarak anlatılır.
  - `tweet-yukselen-lokal-dip-zayif-momentum-long-1951026500259684787` — `tweet-yukselen-lokal-dip-zayif-momentum-long-1951026500259684787` (2025-07-31). Denememiş olduğu fikir: "lokal dipler giderek yükseliyorsa" ve "ana dip (range’in altı) zayıf momentumla oluşmuşsa" durumunda "long arayışı yapmak avantajlı olabilir." (Ham). Teyit: "Ekstra teyit için hacim ve momentum indikatörleriyle desteklenebilir." (Ham).

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
  - `tweet-confluence-destek-direnc-rsi-fibonacci-mum-1999911648564506739` — Tekrar, Tansu'nun kendi gönderisi olarak (13.12.2025; Ham: "(metin yok)", yalnız "NotebookLM" imzalı infografik): "Tek Sinyale Güvenme, Kesişim Ara!" (görsel metni). Üç adım: geçmiş dip ve tepeleri destek ve direnç olarak işaretle; fiyat bu seviyeye gelince bağımsız teyit ara (RSI uyumsuzluğu, Fibonacci geri çekilmesi, trend çizgileri, mum formasyonları); çoklu teyit dönüş olasılığını artırır. Bölümdeki confluence tezinin görsel kaynağıdır; eşik, sayı ve sonuç yok. Tansu görseli paylaşmıştır, kendi yazmamıştır (YORUM).
  - `tweet-dengesizlik-gucu-olcumu-2087560466511941804` — Dengesizlik gücü şeması (12.08.2026; görsel açıldı): “Strongest”, “Strong”, “Weak”, “Weakest”, “-Balance-”. Okuma (YORUM): aynı yönde üç mum ve geniş boşluk en güçlü örnektir; ilk mum ters yöndeyken geniş boşluk güçlü, küçük boşluk zayıf, boşluksuz yapı denge olarak gösterilir. Paylaşılan şemanın yazarı belirtilmez.
  - `tweet-dinamik-swing-vwap-hl-kirilimi-1987107314193649692` — Dinamik swing VWAP trend takibi (08.11.2025): “Şöyle güzel bir de trend takip olarak kullanılabilir.” ve “Dikkatimi çeken sert yükselişler hep HL kırılımından sonra gelmiş.” (Ham). Okuma (YORUM): OZSUB örneğindeki gözlem, evrensel yükseliş garantisi değildir.
  - `tweet-ema26-yuzde7-kanal-haftalik-pivot-1962942414391283988` — Endeks bant ekranı (02.09.2025; görsel açıldı): “EMA26 Kanal Üst (+7.0%)” ve “EMA26 Kanal Alt (-7.0%)”. Okuma (YORUM): yüzde bantları haftalık pivotlarla birlikte gösterilir; ATR bandıyla aynı hesap değildir.
  - `tweet-gunluk-islem-haftalik-trend-yonu-1957142020335735050` — Okuma (YORUM): Günlük işlem için haftalık yön filtresi. Ham: "Günlük işlemi haftalık trendin aksi istikametinde açmayın:)".
  - `tweet-gunluk-pivot-noktalari-formul-2003807379109081422` — Okuma (YORUM): NotebookLM görseli klasik günlük pivot tablosunu tekrarlar. Açılan görselde P: "(Yüksek + Düşük + Kapanış) / 3"; R1: "(2 x P) - Düşük"; S1: "(2 x P) - Yüksek".
  - `tweet-gunluk-pivot-python-kodu-2003812042600567059` — Okuma (YORUM): Günlük pivot Python işlevi. Açılan görsel: `P = (high + low + close) / 3`, `R1 = (2 * P) - low`, `S1 = (2 * P) - high`. İşlev R2/R3 ve S2/S3 seviyelerini de döndürür.
  - `tweet-gunluk-pivot-r1-s1-r2-s2-kodu-1782891937025994868` — Okuma (YORUM): Klasik pivottan ayrı ikinci merkezli gösterge. Ham: "L5 ve L2 çizgilerinin altında ve üstünde kapanışlar al ve sat sinyalleri." Açılan G2: `PVT2:=ADAM ;`, `r2:=PVT2+(TX-RX)/2 ;`, `s2:=PVT2-(TX-RX)/2 ;`. L2/L5 yön eşlemesi açık değildir.
  - `tweet-hacim-profili-aralik-secimi-60-bar-2005293321233576379` — Okuma (YORUM): Hacim profili aralığı fiyat dalgasına göre seçilir. Ham: "Sabit bir bar sayısı yerine fiyat hareketine (dalgalanmaya) göre manuel seçin". Genel günlük pencere: "son 60 bar (3 ay)".
  - `tweet-hacimli-kapanis-arz-bolgesi-hedef-bandi-2090360295491318080` — Okuma (YORUM): TMPOL için koşullu hedef örneği. Ham: "552.14 üzerinde bir kaç hacimli bar kapanışı yaparsa hedef 645-708 bandıdır." ve "Tersi durumda 431.45'e çekilir ilk etapta." Seviyeler örneğe aittir.
  - `tweet-haftalik-pivot-2atr-hedef-1957867341552971801` — Okuma (YORUM): Haftalık pivotun koşullu hedef örneği. Ham: "2 ATR üzerine atan değerli kardeşimizin ilk hedefi acaba 11219 olacak mı?" Bu soru kesin hedef vaadi değildir.
  - `tweet-simetrik-ucgen-alt-bant-temas-tepki-2096583957991043329` — - `tweet-simetrik-ucgen-alt-bant-temas-tepki-2096583957991043329` (2026-09-06; Tansu'nun X gönderisi). Ham: "Kısa vadede de kanal dibi teması" / "Güzer retest var". Okuma (YORUM; görsel metni): DENGE simetrik üçgen alt bant teması örneği, sayısal ekran değerleri genel eşik yapılmaz.
  - `tweet-simetrik-ucgen-swing-kanali-2097010207821877561` — - `tweet-simetrik-ucgen-swing-kanali-2097010207821877561` (2026-09-07; Tansu'nun X gönderisi). Ham: "Kanala temas et bakarız sonra". Okuma (YORUM; görsel metni): DENGE swing kanalında teması bekleme örneğidir; mevcut retest yaklaşımına eklenir.
  - `tweet-dusen-takoz-alt-bant-temasi-2096591557801476190` — `tweet-dusen-takoz-alt-bant-temasi-2096591557801476190` (2026-09-06; Ham ve varsa görsel metni). Okuma (YORUM; görsel açıldı): daralan iki düşen kesikli çizginin alt sınırına son mum teması vardır. Görsel: "TEMAS". Bu, üst sınır kırılımı olarak kaydedilmez.
  - `tweet-dusen-takoz-kirilim-retest-2095927899249406462` — `tweet-dusen-takoz-kirilim-retest-2095927899249406462` (2026-09-04; Ham ve varsa görsel metni). Ham: "Buna teknik analizde retest deniyor." Görsel metni: "ACSEL - Düşen Takoz Kırılımı". Okuma (YORUM): retest örneğidir; görüntüdeki skor genel giriş eşiği yapılmaz.
  - `tweet-dusen-takoz-kirilim-taramasi-2015875741842354270` — `tweet-dusen-takoz-kirilim-taramasi-2015875741842354270` (2026-01-26; Ham ve varsa görsel metni). Ham: "Böyle çalışıyor sistem." / "Düşen takoz". Görsel metni: "OZSUB - Düşen Takoz Kırılımı". Okuma (YORUM): seçilmiş tarama örneğidir.
  - `tweet-bollinger-ss-fibo-kanal-dibi-seviyeler-1781177739917111642` — `tweet-bollinger-ss-fibo-kanal-dibi-seviyeler-1781177739917111642` (19.04.2024; Ham): "547.86 - BB 2 SS" / "537- FIBO" / "512 -  BB 3SS" / "438 - Kanal Dibi". Okuma (YORUM): TARKM tarihli destek araçları yan yana izlenir; seviyeler genel giriş eşiği değildir.
  - `tweet-carpan-kar-tahmin-degerleme-1767639539621732375` — `tweet-carpan-kar-tahmin-degerleme-1767639539621732375` (12.03.2024; Ham): "20 günlük EMA iyi destek görevi gördü hisse buradan döndü. Burası aynı zamanda BB orta bandı." / "Burası hem BB alt bant, hem 50 günlük EMA hemde 0,786 fibo desteği." / "Bu noktadan pozisyon açılabilir kanaatindeyim." Okuma (YORUM): TUPRS örneğinde destek birleşimi ve olasılık dili korunur.
  - `tweet-cift-pivot-seviyeleri-1988272481052885342` — - `tweet-cift-pivot-seviyeleri-1988272481052885342` — XU100 pivot haritası (11.11.2025; Ham ve görsel metni). Ham: "Sıkıntı derin..". Görsel metni: "XU100 - PİVOT SEVİYELERİ", "PVT1 (Pivot 1)", "PVT2 (Pivot 2)", "R1 (Direnç 1)", "S1 (Destek 1)". Okuma (YORUM): iki pivot kümesinin seviye çizimidir; pivot hesap formülü veya işlem şartı bu etiketlerden çıkarılmaz. Hazırlık X.
  - `tweet-vwap-val-ustu-yeni-trend-2005025179169149207` — - `tweet-vwap-val-ustu-yeni-trend-2005025179169149207` — ASTOR VWAP ve VAL yorumu (27.12.2025; Ham): "son işlem gününde de VAL üzerine atarak %68'lik işlemlerin olduğu alanda yoluna devam edecek görünüyor." / "Burada YENİ bir trend başlamış gibi." Okuma (YORUM): VWAP üstüne çıkış önceki adımdır; seçilmiş örneğin olasılık dili korunur. Hazırlık X.

---

## 17. X arşivi kısa kayıtları (16.10)
- Kanal stratejisi backtest sonucu (kural yok; `tweet-kanal-stratejisi-backtest-2088957194892923386`; Ham ve görsel birinci el, iki görsel de açıldı; Tansu'nun X gönderisi, 2026-08-16): Tansu: "Şöyle bşr strateji kodluyorum", "İlk veriler fena değil", "Biraz geliştirip bakarız" (Ham). Görsel 2 çıktısı: "Toplam İşlem : 4", "Kazanan İşlem : 4", "Win Rate : 100.0%", "Ortalama Getiri : 13.00%", "Bileşik Toplam Getiri: 60.8%". Dört işlem (giriş → çıkış, getiri %): 2024-11-05 90.60 → 2024-12-03 115.58 (27.57); 2025-02-03 115.49 → 2025-03-03 127.45 (10.35); 2025-03-19 116.14 → 2025-06-10 117.55 (1.21); 2025-09-03 128.60 → 2026-01-21 145.13 (12.86). Hesap kontrolü (bizim): ortalama (27,57 + 10,35 + 1,21 + 12,86) / 4 = 12,9975; bileşik 1,2757 × 1,1035 × 1,0121 × 1,1286 = 1,608; ikisi de tabloyla uyumlu. PnL sütunu fiyat farkından 0,10–0,13 düşüktür (örnek 115,58 − 90,60 = 24,98; tabloda 24.88); fark nedeni yazılmamış (YORUM: maliyet olabilir). Görsel 1: mum grafiği, üstte düz basamaklı çizgi, altta kesikli basamaklı çizgi (iki bant), yeşil yukarı ve kırmızı ters üçgenler; yeşil üçgenler alt banda, kırmızılar üst banda yakındır (YORUM: alt banttan al, üst banttan sat). Üçgenler yaklaşık 5 yeşil ve 5 kırmızıdır; tablodaki 4 işlemle tam uyuşmaz (YORUM: grafik daha geniş pencere). Kanalın tanımı, giriş ve çıkış koşulu, sembol (fiyat 90–145 TL), maliyet, stop ve yön yazılı değil. Basamaklı bantlar yükselen paralel kanal değildir (YORUM): §2 ile aynı yöntem sayılmaz. Tansu'nun kanıtı: dört işlem, tek sembol, "%100 kazanma"; Tansu sonucu kendisi "ilk veriler" sayar. Günlük bedava veriyle: kural tanımsız, sonuç yeniden üretilemez. Hazırlık X. Kaynak güveni: Ham ve görsel birinci el; kural yok: düşük.
- Dip hisseler taraması, 1. ve 2. derece sinyal gücü (`tweet-dip-taramasi-sinyal-derecesi-2002032178113478863` ve `tweet-dip-taramasi-orderblok-mum-ema-2002084408061308988`; Ham; iki Tansu X gönderisi, 19.12.2025; görsel yok): "Şimdi dip hisse taramaları 2 farklı sinyal gücü kalitesi ile geliyor." "#kront mesela 3 kriteri sağlayıp üstüne Ob yapısı ile öne çıktı ve 1. derecede dip sinyali verdi." "Sonuç tavan" (Ham). Güncelleme (Ham): "Dip hisseler tarama kodumuza orderblok, mum formasyonları ve kısa dönem ema'lar da eklendi." "1. derece ve 2. dereceden dip sinyali gelen hisselerde sistem otomatik olarak eğer var ise, orderblok mum formasyonları ve ema'ların olduğu ikinci bir grafiği de açacak." Alıntılanan gönderi (Ham): "Oldu mu hocam?" "%5" "#kront" (anlamı belirsiz). Parametre: derece sayısı 2; temel kriter sayısı 3 (içeriği yok); 1. derece = 3 kriter + order block (OB) yapısı (Ham, KRONT örneği). YORUM: 2. derece = 1. derecenin koşullarından eksik olan hâl (tanımı Ham'da yok); order block, mum formasyonu ve kısa EMA ikinci grafiğe "eğer var ise" çizilir, derece koşulu mu yalnız görsel katman mı belli değil. Üç temel kriter, OB tanımı (bkz. §10 BOS + Fib + FVG/OB), mum listesi, EMA periyotları, giriş, stop ve hedef yok. Tansu'nun kanıtı: tek örnek KRONT, "Sonuç tavan" (Ham; tavan yüzdesi, tarih ve sinyal günü yok; seçilmiş örnek). Günlük veriyle: bugün hayır (temel dip kriterleri bilinmiyor); OB, mum ve EMA günlük OHLC'den hesaplanır. Hazırlık X. Kaynak güveni: Ham birinci el; kural gizli, yalnız yapı ve bir örnek: düşük.
- Günlük range breakout, DOAS sinyal ve sonuç tablosu (`tweet-daily-range-breakout-1914061902151290940`; Ham; G1 görsel metni, G2 açıldı; Tansu'nun X gönderisi, 20.04.2025): "Bazen saatlerce çalışıp quantum kodu yazıp bir şeyler ararsın  oysa aradığın şey çok daha basit bir kod ile beliriverir:)" "detaylandıracağız efendim, para var bunda:)" (Ham). Görsel başlıkları (görsel metni): "DOAS.IS Günlük Range Breakout (Son Sinyal)" (fiyat grafiği, Mart 2025) ve "--- Range Breakout Sonuçları ---" (tablo). Tablo (G2, açıldı): sütunlar `Tarih`, `Sinyal`, `Giriş`, `Çıkış`, `Kar`; 35 satırın hepsi "Yukarı Kırılım" (yalnız alış yönü), 25.01.2024 - 18.03.2025. Tablo özeti (hesap bizim; YORUM): 21 kârlı, 14 zararlı; toplam kâr 119,51, toplam zarar -11,61 (net 107,90, hisse başına fiyat birimi); ortalama kâr 5,69, ortalama zarar -0,83; en büyük kâr 22,72 (05.04.2024), en büyük zarar -3,84 (17.04.2024); tam 1,50 kâr veren üç satır (25.01, 29.01, 14.03.2024; YORUM: sabit hedef olabilir, kanıtlanmaz). Parametre: yok (aralık penceresi, kırılım ölçütü, giriş, çıkış, stop ve maliyet yazılı değil; kural kodu paylaşılmadı). A §18'deki 60 günlük aralık kırılımı ile aynı ad ailesidir (range breakout); pencere ve mum teyidi bu kayıtta yoktur. "Giriş" fiyatının kırılım seviyesi mi sinyal günü kapanışı mı, "Çıkış" fiyatının aynı gün kapanışı mı olduğu belli değil; giriş ve sinyal aynı barda ise ileri bakma riski (YORUM); ardışık günlerde art arda sinyal (işlem örtüşmesi), komisyon ve kayma; tek hisse, tek dönem. Kâr/zarar oranı yaklaşık 10 çok yüksektir; yöntem açık olmadan bu sonuç kural kanıtı sayılmaz (YORUM). Tansu'nun kanıtı: yalnız tablo; "para var bunda" vaattir, ölçülmemiş. Günlük veriyle: evet (günlük OHLC); kural tanımı olmadan kodlanamaz. Hazırlık X. Kaynak güveni: görsel birinci el ve net; kural gizli: düşük.

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-dip-tespiti-price-action-teyit-1950987288378519760` — Dip ve gösterge teyidi (31.07.2025): “Bak kardeşim dibi yakalarsan diğer göstergelerin de olumlu ise gir işleme.” ve “Ben mumlarn yapısına göre bir price action kodu yazarak kendimce bu dibi teyit edeceğim.” (Ham). Okuma (YORUM): mum teyidi plan olarak anlatılır.
  - `tweet-fib-talep-bolgesi-toplama-alani-2002803197946249346` — `tweet-fib-talep-bolgesi-toplama-alani-2002803197946249346` (2025-12-21; Ham): Toplama bölgesi örneği: "İşte bu kardeşimizin bekleme salonu kırmızı ile boyadığım alan. O noktadan toplarız ardından patır patır %30-%35 potansiyeli var" (Ham). Okuma (YORUM): yüzde aralığı bu örneğin beklentisidir.
  - `tweet-fibo-trend-destegi-fvg-0618-hedef-2002147457422307730` — `tweet-fibo-trend-destegi-fvg-0618-hedef-2002147457422307730` (2025-12-19; Ham): Trend desteğinin kırılma riski: "fiboyu çektikten sonra trend desteğine yakın olan FVG hedeftir. Hele bu FVG 0.618 alanında ise güçlü hedeftir. Yıkar geçer desteği." (Ham).
  - `tweet-fibo-vwap-hacim-profili-delta-analiz-2045428859613393259` — `tweet-fibo-vwap-hacim-profili-delta-analiz-2045428859613393259` (2026-04-18; Ham): Hacim profili örneğinde kalıcılık şartı: "Fiyatın ₺30.24 (VAH) üzerinde kalıcı olması, Ağustos zirvesindeki HH seviyesini tekrar test etmek için gerekli zemini hazırlayabilir." (Ham). Okuma (YORUM): örneğin fiyatı genel eşik değildir.
  - `tweet-formasyon-boyun-cizgisi-kirilimi-1900958705048293851` — `tweet-formasyon-boyun-cizgisi-kirilimi-1900958705048293851` (2025-03-15): Kırılım örneği: "Cuma günü breakout yapmış yeni formasyonumuz." (Ham). Okuma (YORUM): açılan görselde yükselen kırmızı çizgi ve beyaz dönüş noktaları görülür; formasyon adı bu kayıttan kesinleştirilmedi.
  - `tweet-fvg-bosluk-doldurma-1907528888089272433` — `tweet-fvg-bosluk-doldurma-1907528888089272433` (2025-04-02): Boşlukların geri alınması beklentisi: "Bu boşluklar geri alınacak er ya da geç elbet." (Ham). Okuma (YORUM): GZNMI örneği için beklenti, kesin zaman veya genel başarı garantisi vermez.
  - `tweet-fvg-detection-python-1893618606790824199` — `tweet-fvg-detection-python-1893618606790824199` (2025-02-23): FVG beklentisi: "Bu alanlar fiyatın gelecekte doldurabileceği alanlardır." ve "Bir düşüş boşluğu ise fiyatın tekrar dirençle karşılaşabileceği bir bölge olarak değerlendirilebilir." (Ham; görsel açıldı).
  - `tweet-fvg-sensitivity-example-1893637273029050563` — `tweet-fvg-sensitivity-example-1893637273029050563` (2025-02-23): Hassasiyet uyarısı: "biraz subjektif geliyor bana, hassasiyeti ayarlamak için subjektif değişiklikler yapılması gerekiyor." (Ham). Okuma (YORUM): AKBNK örneğinin ayarları nesnel sabit kural diye aktarılmaz.
  - `tweet-fvg-temas-tarama-1989086542212870617` — `tweet-fvg-temas-tarama-1989086542212870617` (2025-11-13): BYDNR FVG örneği: "Kod nokta atışı çalışıyor maşallah." (Ham). Görselde "Bullish FVG (Yeni)" ve "Bullish FVG (Eski-Aktif)" ayrımı bulunur (görsel açıldı). Okuma (YORUM): tek grafik başarı oranı değildir.
  - `tweet-fvg-temas-uzaklik-tarama-1989089558164873727` — `tweet-fvg-temas-uzaklik-tarama-1989089558164873727` (2025-11-13): Temas taraması örneği: "ADEL.IS - TEMAS FVG (0.00% Uzaklık) | BULLISH | Fiyat: 29.74" (görsel açıldı). Okuma (YORUM): uzaklık ve fiyat örnek etiketleridir.
  - `tweet-gann-fan-destek-hedef-1771838096432099715` — `tweet-gann-fan-destek-hedef-1771838096432099715` (2024-03-24): Gann destek örneği: "8/1 fanından alacağı destek ile ilk hedefin 4,92 ve 5,55 olması gerekir." Sınır: "Fakat bu alanlar ayı piyasasıdır bunu da söylemek lazım." (Ham). Okuma (YORUM): seviyeler örneğe özeldir.
  - `tweet-gann-fan-fibo-destek-trend-okuma-1767689603035640165` — `tweet-gann-fan-fibo-destek-trend-okuma-1767689603035640165` (2024-03-12): SAYAS örneğinde destek kırılması: "86,275 fibo desteği, kırarsa işler çirkinleşecek, 3/1 fanına geçiş yapar. Düşüş trendi teyit olur." (Ham). EMA bağlamı: "50 günlük EMA altında, 200 günlük EMA'ya doğru gidiyor." Okuma (YORUM): fiyat seviyesi örneğe özeldir.
  - `tweet-smc-fvg-aktif-bolge-destek-1989081381515767898` — Okuma (YORUM): SMC yapı sözlüğü ve GARAN aktif FVG izleme örneği. Ham FVG'yi “Hızla oluşan 3 mumluk hareket sırasında geride bırakılan fiyat boşluklarıdır.” diye tanımlar; MSS için “son teyit edilmiş dip veya tepe noktasının kırılmasıdır.” der. GARAN örneğinde “En Yakın FVG (Yaklaşık 122 TL)”, “Orta FVG (Yaklaşık 110 TL)” ve “En Alt FVG (Yaklaşık 105 TL)” izlenir. Bunlar örnek seviyelerdir.
  - `tweet-son-16-gun-max-direnc-kirilim-1843762399016563165` — Okuma (YORUM): 16 günlük maksimumla direnç belirleme araştırma fikri. Ham: “Sizce aşağıdaki çalışma işe yarar mı?” ve “Fiyatların son 16 gün içinde gördüğü en yüksek (MAX)  fiyatlarını hesaplayıp bir nevi "direnç"  belirlemek.”
  - `tweet-ssl-likidite-sweep-taramasi-2095236564909445352` — Okuma (YORUM): SSL taraması satış likiditesini alanları izleme fikridir. Ham: “Bugüne kadar satış likiditesini alanlar taraması.” ve “muhtemelen yarın işlem açacağım yeni tarihli arama ile.”
  - `tweet-symmetric-triangle-break-confirm-1953971088003608726` — Okuma (YORUM): Simetrik üçgen örneğinde sıkışma, kırılım ve onay sırası. Ham: “Şiir gibi değil mi, sıkışmış, kırmış, onayını almış, devam etmiş.”
  - `tweet-takoz-kirilim-retest-2095931821078847637` — Okuma (YORUM): Alçalan takoz kırıldıktan sonra üst çizginin yeniden testi. Ham: “Hisse alçalan takozu kırmış sonra tekrar takozun üst çizgisine temas edip tepki almış test etmiş.” ve “Ancak farklı analizlerde yapmak lazım.”
  - `tweet-talep-bolgesi-dikdortgen-tepki-gozlemi-1958957313387118692` — Okuma (YORUM): Talep bölgesi çizimi ve tepki takibi. Ham: “Yükseliş başlamadan hemen önceki satıcıların yoğun olduğu bölgeyi belirlemek ve bu aralığı dikdörtgen şeklinde işaretlemek yeterlidir.” ve “Eğer fiyat burada yeniden alıcı buluyorsa, o bölge hâlâ geçerlidir.”
  - `tweet-talep-bolgesi-dip-koruma-erken-giris-2093739858845917333` — Okuma (YORUM): CRDFA örneğinde erken giriş için dip korunması ve toparlanma birlikte izlenir. Ham: “talep bölgesindeki dibi bir iki bar koruyup ve ardından fiyat toparlanma belirtisi veriyorsa erken giriş için daha kaliteli bir nokta belirir”.
  - `tweet-talep-bolgesi-dip-koruma-erken-giris-2094872002792235059` — Okuma (YORUM): CRDFA erken giriş izleme kaydının devamı; alıntılanan kendi gönderisinde “talep bölgesindeki dibi bir iki bar koruyup” ve “ardından fiyat toparlanma belirtisi veriyorsa erken giriş için daha kaliteli bir nokta belirir” der.
  - `tweet-talep-bolgesi-dusen-kirilim-teyidi-2090509642220621850` — Okuma (YORUM): Talep bölgesi görüntüsü tek başına asıl stratejinin tamamlandığı anlamına gelmez. Ham: “Asıl stratejim gerçekleşmemiştir. Düşeni kıranın da olmasını isterim.”
  - `tweet-talep-bolgesi-formasyon-trend-kirilimi-2088627403845181616` — Okuma (YORUM): Talep bölgesinde formasyonla düşen kırılımının birleştiği gözlem. Ham: “talep bölgesinde formasyonumuz oluşmuş düşeni de kırmıi”.
  - `tweet-talep-bolgesi-fvg-tepki-taramasi-2026351724491850091` — Okuma (YORUM): Talep ve FVG tepki taramasında kod doğruluğu vurgusu. Ham: “Herkes biliyor talep bölgesinden fvg'den tepki alacağını önemli olan kodu nasıl ne kadar doğru yazdığınız.”
  - `tweet-talep-bolgesi-likidite-supurme-2094874313165885879` — Okuma (YORUM): CWENE için koşullu likidite senaryosu. Ham: “burada buy side liquidity yaparsa patır patır gider.” ve “Talep bölgesinde stopları patlatıp 3-5 tavan yapmış.” Okuma (YORUM): Sonuç ifadesi yeni işlemler için hedef kuralı yapılmaz.
  - `tweet-talep-bolgesi-tepki-izleme-2088578077949321389` — Okuma (YORUM): EREGL için bandı izleyip tepkiyi gözleme örneği. Ham: “34.73 - 38.64 bandına doğru ilerliyor orası iyi bir talep bölgesi, bakalım tepkisi ne olacak”. Bandın değerleri bu örneğe aittir.
  - `tweet-talep-kirilim-ust-10-yuzde-temiz-tarama-2003587326036127830` — Okuma (YORUM): Talep kırılımı sonrasında üst alanın temiz olması taranır. Ham: “talep bölgesini kırmış olacak” ve “üzerindeki en az %10'luk alanda herhangi bir bearish fvg ve arz alanı olmayacak:)”.
  - `tweet-trend-cizgisi-kirilim-doji-1919254273382048180` — Okuma (YORUM): Trend kırılımı, son gün Dragonfly Doji ve momentum listesinin birleştiği örnek. Ham: “Şöyle bir trend breakout var bir de dragonfly doji yapmış son gün. bizimde momentum listemizde.”
  - `tweet-trend-kirilim-pullback-hacim-onay-lookback-75-1949799810053104041` — Okuma (YORUM): ASTOR'da kırılım, pullback ve hacimli onay sırası. Ham: “İşte buna pullback sonrası onay diyoruz, hacim ile devam ediyor.” G1 açıldı: “Kırılım: 2025-07-09 | Pullback: 2025-07-18 | Onay: 2025-07-21 | Lookback: 75”. Okuma (YORUM): 75 bu ekranın lookback ayarıdır; genel pencere değildir.
  - `tweet-trendline-breakout-first-touch-entry-1886468240353976356` — Okuma (YORUM): TOASO trend kırılımı için seçilmiş gözlem. Ham: “dün yakalamıştık.  kırılımın güzelliği.” Görsel metni ilk temas ve giriş tarihlerini ayrı verir; bunlar iki ayrı olaydır.
  - `tweet-trendline-ilk-temas-kirilim-taramasi-1875965981690122351` — Okuma (YORUM): AYEN trend kırılımı tarama örneği. Ham: “Ne güzel kırmışsın ya:)” ve “Bunun taraması da ayrı zevkli”. Görsel metni ilk temas ile giriş tarihini ayrı gösterir.
  - `tweet-trendline-kirilim-tp-sl-1875933436441161794` — Okuma (YORUM): Trend kırılımı son işlemi stop ve kâr hedefiyle birlikte gösterilir. G1 açıldı: “Trendline Breakout (Last Trade)”, “Resistance Line”, “Take Profit” ve “Stop Loss”. Okuma (YORUM): Çizgilerin eksenlerinden eşik türetilmez.

- `tweet-birikim-dagitim-dongusu-1992282998746513749`, `tweet-birikim-talep-testi-sirasi-1992554548213485771` — Birikim ve talep testi (22–23.11.2025; Ham ve döngü görseli, açıldı). Ham: "herkes satmayı bıraktığında akıllı para girer birikim başlar, talep testi yapılır pozitif çıkarsa tahta yürür gider." Görsel: "Birikim Süreci", "Yükselen Trend", "Dağıtım Süreci", "Düşen Trend", "Test". Okuma (YORUM): kavramsal sıra verilir; satıcı tükenişi ve pozitif test için sayısal koşul bu anlatımdan türetilmez. Hazırlık X.
- `tweet-boga-bayragi-kirilim-tespiti-1907534023573832077`, `tweet-boga-bayragi-kirilim-tespiti-1908978603208892747` — Boğa bayrağı çıktıları (02.04.2025 ve 06.04.2025; Ham ve görsel metni). Ham: "Haydi bakalım:)" / "BAYRAĞA GEL:)". Görsel metni: "Breakout Tarihi: 2025-03-27" / "Boğa Bayrak". Okuma (YORUM): tarihli seçilmiş kırılım örnekleridir; bayrağın ölçü kurallarını veya başarı oranını kanıtlamaz. Hazırlık X.
- `tweet-kanal-orta-bant-marubozu-kirilim-1919059738450415964` — Kanal orta bandı ve marubozu (04.05.2025; Ham). "Son gün harika bir marubozu mum ile stratejinin gerekliliği olan kanal orta bandını kırmış" / "Aynı zamanda momentum sistemimden de geçrti." Okuma (YORUM): orta bant kırılımı, üst kanal kırılımından farklıdır. Kanalın ve momentum filtresinin hesap ayrıntıları bu örnekten doldurulmaz. Hazırlık K.
- `tweet-kayan-16-gun-max-min-konum-1775315669824700852` — KFEIN kayan fiyat konumu (03.04.2024; Ham): "16 günlük kaydırılmış pencereler ile max ve min fiyatlarını ve hissenin anlık konumunu görselleştirdim." / "artık 16 günlük zirvesine yakın olduğunu ve dalgalanma ile aşağıya sarkabileceğini söylüyor bize." Okuma (YORUM): pencere 16 gündür; olasılıklı geri çekilme yorumu kesin satış sinyali değildir. Hazırlık K.


## 18. 60 günlük aralık kırılımı (range breakout) + bullish mum formasyonu teyidi (DITAS)

- Kaynak: `tweet-60-gun-range-breakout-belthold-1926353549723590759` (24.05.2025; Ham ve görsel, açıldı). Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim): "Son mum çubuğu hem 60 günlük zirve seviyesini yukarı kırmış, hem de aynı gün içinde CDLBELTHOLD adı verilen bir bullish (yükseliş yönlü) mum formasyonu oluşturmuş." Kod anlatımı (Ham): "60 Günlük Range Hesabı: Son 60 günün zirve (range_high) ve dip (range_low) değerleri hesaplanır." "Breakout Kontrolü: Son günün en yüksek fiyatı ve kapanışı, 60 günlük zirveyi geçiyorsa sinyal kabul edilir." "Bullish Mum Formasyonu Tespiti: talib kütüphanesi ile son mumda herhangi bir bullish formasyon oluşmuş mu kontrol edilir." Uyarı (Ham): "Kırılım sonrası fiyatın bu seviyenin altında kalıp kalmadığını izlemek gerekir. Formasyonun geçerliliği için sonraki gün hacim ve fiyat teyidi önemlidir." "Bu kod henüz bitmedi buraya eklenecekler var." Görsel başlığı (açıldı): `DITAS | Range Breakout ve CDLBELTHOLD Mum Formasyonu`; yeşil kesikli `60G Zirve`, kırmızı kesikli `60G Dip`; son mum zirve çizgisinin üstüne kapanmış (kırmızı kutu ve ok).
- Tanım (YORUM, Ham'dan): 1. `range_high` = son 60 günün en yüksek değeri, `range_low` = en düşük değeri. 2. Kırılım: son günün High'ı ve Close'u `range_high`'ın üstündedir (Ham). 3. Mum: talib CDL işlevlerinden en az biri son mumda bullish (pozitif) verir; örnek CDLBELTHOLD. 4. Sinyal = 2 ve 3 aynı gün. "Sonraki gün hacim ve fiyat teyidi" kod değil, uyarıdır.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Aralık penceresi | 60 gün | Ham |
| Kırılım ölçütü | High > range_high ve Close > range_high | Ham |
| Mum teyidi | talib bullish formasyon (herhangi biri); örnek CDLBELTHOLD | Ham |
| Veri | yfinance, 01.01.2024 - 24.05.2025 (örnek); grafik son 180 gün | Ham |
| DITAS çizgileri | 60G zirve ≈16,8; 60G dip ≈11,0 | görsel, açıldı (piksel ölçümü, YORUM) |
| Hacim eşiği, giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: pencere bugünü içerir mi (içerirse bugünün High'ı kendi zirvesini aşamaz; YORUM: önceki 60 gün); zirvenin High'a mı Close'a mı göre alındığı; hangi CDL işlevlerinin sayıldığı; hacim ve fiyat teyidi ölçütü; stop ve hedef. TA-Lib dış bağımlılıktır; BELTHOLD mumu elle de yazılabilir (YORUM). Aynı mum dedektörü B §41'de RSI trend kırılımıyla birleşir.
- Tansu'nun kanıtı: yok (tek örnek, sonuç yok). "Trendin devam etme ihtimali yüksek" yorumdur, ölçülmemiş.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLCV).
- Kaynak güveni: Ham ve görsel birinci el; kırılım koşulu net, mum seçimi ve teyit eksik: orta-düşük. Hazırlık K.

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-200-gunluk-direnc-kirilimi-2045418595421659641` — Okuma (YORUM): PRZMA için direnç kırılımı gözlemi, 60 günlük aralık örneğinden ayrı bir 200 günlük örnektir. Ham: "200 günlük direnci kırmış durumda."
  - `tweet-quant-fonksiyon-gruplari-60-gun-kirilim-1942696711287169192` — - `tweet-quant-fonksiyon-gruplari-60-gun-kirilim-1942696711287169192` (2025-07-08; Ham): Eğitim örneği (Ham): "Örneğin bir hisse fiyatı son altmış günün en yüksek seviyesini geçtiyse “kırılım” sinyali üretilebilir." Okuma (YORUM): genel fonksiyon eğitimi içindeki örnektir, zorunlu strateji ilanı değildir.
  - `tweet-range-30-breakout-1925633169694277851` — - `tweet-range-30-breakout-1925633169694277851` (2025-05-22; Ham): BAYRK örneğinin ayrı ayarı (Ham): "range = 30". Okuma (YORUM): bu örnek ayarı, bölümdeki 60 günlük tanımın yerine geçirilmez.
  - `tweet-range-breakout-bant-kirilimi-1926345317093400684` — - `tweet-range-breakout-bant-kirilimi-1926345317093400684` (2025-05-24; Ham): Ham: "Range breakout:)". Okuma (YORUM): aynı başlığın örnek grafik paylaşımıdır; tek başına yeni parametre tanımı olarak kullanılmaz.
  - `tweet-range-breakout-belthold-mum-1950285317841301734` — - `tweet-range-breakout-belthold-mum-1950285317841301734` (2025-07-29; Ham): Görsel (açıldı): "SAYAS | Range Breakout ve CDLBELTHOLD Mum Formasyonu". Okuma (YORUM): aralık kırılımı ile boğa mumunun birleşimine başka bir örnektir.
  - `tweet-range-breakout-ema-fibo-marubozu-1926379754925556143` — - `tweet-range-breakout-ema-fibo-marubozu-1926379754925556143` (2025-05-24; Ham): ADESE örneği (Ham): "Fiyat, kısa ve orta vadeli üssel hareketli ortalamaların (EMA5, EMA8, EMA13 ve EMA34) tamamının üzerinde seyrediyor." Fibonacci penceresi: "Bu seviyeler, son 60 gün içinde görülen en yüksek ve en düşük fiyatlar kullanılarak hesaplanmıştır."
  - `tweet-range-breakout-teyit-kontrol-listesi-1929190228742332559` — - `tweet-range-breakout-teyit-kontrol-listesi-1929190228742332559` (2025-06-01; Ham): Birleşik teyit (Ham): "Haftalıkta son hafta ve günlükte son işlem günü Range breakout yapmış"; "Yüksek R2 değeri ile yükselen regresyon kanalını kırmış"; "Son gün marubozu mum bırakmış"; "Para girişi pozitif"; "Hacim artmış". Okuma (YORUM): seçilmiş vaka kontrol listesidir.

---

## 19. Haftalık aralık kırılımı ve günlük teknik teyit

- Kaynak: `tweet-haftalik-breakout-gunluk-teyit-1929184555816419717` (01.06.2025; Ham ve görsel metni; Tansu'nun X gönderisi).
- Tansu'nun ifadesi (verbatim): "haftalık kapanış ve tepe fiyatı, önceki X haftalık zirveyi aştıysa" / "Breakout sonrası, günlük verilerde şu unsurlar kontrol edilir:" / "Fiyatın tepeyi geçmesi, tek başına yeterli değildir."
- Tanım (Okuma, YORUM): Önce haftalık kapanış ve tepe önceki X haftanın zirvesini aşar. Sonra günlük göstergelerle teyit aranır. Ham: "MACD kesişimi (özellikle MACD’nin yukarı kesmesi)" / "EMA’ların yukarı yönlü sıralanması (trend gücü)" / "RSI ve Stochastic’in aşırı alımda olmaması (yeni başlayan momentum)" / "OBV’de yukarı yönlü hacim eşlik ediyor mu?" Ek mum örnekleri Ham'da Engulfing, Piercing ve Morning Star'dır.
- Parametreler: Haftalık aralık = X hafta; kaynak X için sayı vermez. Günlük teyit göstergeleri EMA, MACD, RSI, Stochastic ve OBV'dir. Okuma (YORUM): gösterge dönemleri ve aşırı alım eşikleri ayrıca belirlenmeden uygulanamaz; günlük 60 bar kuralı buraya aktarılmaz.
- Belirsiz kalanlar (Okuma, YORUM): X haftanın değeri; göstergelerin dönemleri; teyitlerin zorunlu birleşimi; bullish mumun zorunluluğu; giriş fiyatı, stop ve hedef. Ham'daki "faz2" bu notta hesaplanabilir tanıma bağlanmaz.
- Tansu'nun kanıtı: Ham gelecek gün için "güzel bir hareket bekliyorum" der. Okuma (YORUM): bu beklenti sonuç veya geçmiş sınama değildir.
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): haftalık çubuk günlük OHLCV'den üretilebilir. Teyit ayrıntıları tamamlanmalıdır.
- Kaynak güveni: Ham birinci eldir. Okuma (YORUM): iki aşamalı sıra açıktır, eksik parametreler nedeniyle hazırlık K.

---

## 20. Kanal altı kapanışta AL, kanal üstü kapanışta SAT çıktısı

- Kaynak: `tweet-kanal-alti-al-ust-kanal-sat-2096379158561427848` (05.09.2026; Ham ve G1, açıldı; Tansu'nun X gönderisi).
- Tansu'nun ifadesi (verbatim): "Kaza ile bir trade stratejisi kodlamış olabilirim:)". Görsel: "Alt kanal altı" / "Close 52.95 < Alt 54.65" / "Üst kanal üstü" / "Close 65.30 > Üst 65.10".
- Tanım (Okuma, YORUM): Çıktı kapanış alt kanal sınırının altındayken AL, üst kanal sınırının üstündeyken SAT gösterir. Bu araç, kanal dibinde yeşil kapanış bekleyen yaklaşımın yerine geçirilmez.
- Parametreler: Okuma (YORUM): fiyat kıyası kapanış üzerindedir. Kanal üretim yöntemi ile T20, T60, Vel ve P sütunlarının rolü bu çıktıdan hesaplanamaz. Görsel fiyatları örnek işlem değerleridir.
- Belirsiz kalanlar (Okuma, YORUM): kanal algoritması, mum dönemi, stop, ek sütunların filtre olup olmadığı, sinyalin işlem günü ve maliyet.
- Tansu'nun kanıtı: Görselde üç kapanmış işlem için "Trade %+23.3", "Trade %+2.3", "Trade %+19.4" yazılıdır. Son AL satırı 26.03.2026'dır. Okuma (YORUM): seçilmiş sonuç tablosu bağımsız sınama veya toplam portföy getirisi değildir.
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): kapanış-bant kıyası mümkündür; kanal tanımı olmadan aynı işlemler yeniden üretilemez.
- Kaynak güveni: G1'de koşul ile AL/SAT etiketleri birlikte görülür. Okuma (YORUM): giriş-çıkış yönü açık, kanal hesabı belirsiz; hazırlık K.

---

## 21. SMC + Elliott trend takibi: indirimli bölgede aktif FVG, limit giriş ve iki hedef

- Kaynak: `tweet-smc-elliott-fibo-fvg-trend-stratejisi-2001758734792397284` (18.12.2025; Ham ve görsel metni; Tansu'nun X gönderisi).
- Tansu'nun ifadesi (verbatim): "SMC + ELLIOTT WAVE (TREND TAKİP)" / "Zaman Dilimi: Günlük (Daily) Varlıklar: Yüksek Hacimli Hisseler (BIST 30/100)".
- Tanım (Okuma, YORUM): Aşağıdaki sıra bu ayrı kaynak stratejisini kaydeder. BOS/Fibonacci bölümündeki mevcut oranlar değiştirilmez.
  1. Yapı: belirgin dip Point 0'dan önceki tepeleri geçen yeni tepe Point 1'e itki. Ham: "en az %10'luk bir marj içermeli ve mum gövdeleri dolgun olmalıdır."
  2. Düzeltme: Ham "Tercihen A-B-C Elliott Zigzag yapısında" der. Bölge: "Minimum: %50 Geri Çekilme (0.50)" / "İdeal (Golden Pocket): %61.8 - %65 Arası" / "Maksimum: %78.6 (Daha aşağısı trendin bozulma riskini artırır)".
  3. Tetik: Fibonacci alım bölgesinde bullish FVG aranır. Ham: "1. mumun en yükseği ile 3. mumun en düşüğü arasında boşluk kalmalı." FVG "fiyat oraya gelmeden önce doldurulmamış (Fresh/Unmitigated) olmalıdır."
  4. Giriş: Ham "Fiyat Fibonacci bölgesine (%50-%78.6) girip buradaki FVG kutusuna temas ettiğinde." Emir yeri: "FVG kutusunun üst bandına veya %61.8 seviyesine"; emir türü Ham'da limit alıştır.
  5. Stop: "Yükselişin başladığı ana dibin (Point 0) hemen altı." Hedef 1: "Eski Tepe Noktası (Point 1)." Hedef 2: "(1. Dalga Boyu x 1.618) + Düzeltmenin Bittiği Yer."
  6. İşlemden kaçınma: "Fiyat FVG bölgesine gelmeden dönerse işlem yapılmaz." / "Düşüş trendi (Lower Highs & Lower Lows) yapan bir hissede bu strateji uygulanmaz." Haber uyarısı: "Bilanço veya kritik haber öncesi oluşan teknik yapılar risk barındırır, temkinli olunmalıdır."
- Parametreler: Günlük zaman dilimi; BIST30/100 yüksek hacimli hisseler; itki en az %10; geri çekilme %50–78,6; ideal %61,8–65; aktif bullish FVG; limit giriş üst FVG bandı veya %61,8; stop Point 0 altı; hedef Point 1 ve 1,618 uzatma. Hepsi Ham'dadır; sayısal hacim filtresi bu değerlerden türetilmez.
- Belirsiz kalanlar (Okuma, YORUM): belirgin dip ve önceki tepe seçimi; dolgun gövde ve yüksek hacim ölçüsü; FVG dolumun fitille mi kapanışla mı sayıldığı; iki limit giriş seçeneğinin seçimi; stop tamponu; hedeflerde satış payı; haber takvimi kapısı.
- Tansu'nun kanıtı: Görsel metni BRYAT için FVG temasını etiketler. Okuma (YORUM): tek kurulum ekranı, getiri veya sistematik başarı kanıtı değildir.
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): fiyat yapısı ve FVG günlük OHLCV ile hesaplanabilir; belirsiz seçimler tamamlanmalıdır. Haber uyarısı yalnız OHLCV ile uygulanamaz.
- Kaynak güveni: Ham'da giriş, stop, hedef ve sıra açıktır. Okuma (YORUM): pivot ve yürütme ayrıntıları nedeniyle hazırlık K.

## 22. ACSEL direnç/VAL senaryosu ve trend izleme ilkesi (18.10)

- ACSEL direnç kırılımı (`tweet-acsel-direnc-kirilimi-volume-profile-val`; 27.08.2026; Ham, Ham'da yazar yok; G1 açıldı): "Örneğin acsel direnci geçer ise nisbeten volume düşük olsa bile VAL seviyesine hareket etme potansiyeli görünüyor" (Ham). Garanti uyarısı: "Her harmonik %100 çalışır diye de bir kaide olamaz" (Ham). Okuma (YORUM): direnç aşılması koşuluyla VAL yönünde hareket olasılığı anlatılır; düşük hacim genel bir giriş izni değildir. G1'de mumlar, bölge kutuları, düşen direnç çizgileri ve sağda yatay hacim profili görülür. Sayısal fiyat veya eşik aktarılmadı.
- Trend izleme ilkesi (`tweet-fiyatlar-trend-halinde-hareket-eder`; 28.08.2026; Ham, Ham'da yazar yok): "Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR." / "akıntının (momentumun) yönünü tayin edip o dalgayı sürmeye odaklanmalısınız." (Ham). Okuma (YORUM): tepe/dip tahmini yerine momentum yönünü izleme ilkesidir. Trend ölçüsü veya ters sinyal algoritması bu ilkeden türetilmez.
- Belirsiz kalanlar (Okuma, YORUM): ACSEL direncinin seçimi, kırılımın fitil/kapanış teyidi, hacim ölçüsü, profil penceresi, stop ve işlem zamanı; trend ilkesinde yön ve ters sinyal ölçüsü. Bunlar uygulama seçimi değildir; mevcut giriş, hacim ve çıkış koşulları değiştirilmez.
- Kanıt sınırı (Okuma, YORUM): ACSEL koşullu beklentidir, gerçekleşmiş hedef sonucu değildir. Trend metni ilke anlatımıdır. İki notun Ham metninden bir sınama sonucu çıkarılmaz. Hazırlık K.

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
- Okunmadı (görsel veya gövde devamı): `gorsel-paket-99` görsel 01/02 (yalnız 03 açıldı), `gorsel-paket-101` not gövdesinin devamı. Bu notların mevcut okumaları §16'dadır.
- Kısmen okundu (ilk ~45-140 satır): tüm -09/-10/-11/-12/-13/-15/-18/-21/-41/-44/-64/-69/-93/-99/-101/-103/-105/-117/-128 notları; gövdedeki Claude'un "Teknik Ek" formülleri ikinci el olarak işaretlendi.
- Havuz notlarının çoğunda birebir Tansu metni "Ham" bölümünde durur (örnek: `tweet-mum-govde-hacim-anomalisi-uyarisi`); bu dosyanın eski bölümleri yalnız Claude özetinden okundu, "Ham" ile çelişirse "Ham" esastır. X gönderilerine erişilmedi.
- Görsel çözünürlüğü düşük olduğundan (680 px) -10/-11/-12/-13 tablolarındaki bazı değerler yaklaşıktır.
