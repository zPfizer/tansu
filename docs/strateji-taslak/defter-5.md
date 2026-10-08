# Defter 5: X arşivi ekleri (X001–X046)

Kaynak: Tansu'nun X arşivi (`x-arsiv/tweets.jsonl`, görseller `x-arsiv/medya/`). Öneriler: `x-arsiv/siniflama/defter-karsilastirma/tema-*.md` 5. bölüm. Her öneri iki model tarafından ayrı bağlamda kaynağa karşı doğrulandı (Codex, Claude); bu dosya birleştirmedir (08.10.2026). R kayıtları (defter-1…4) değişmez; X kayıtları "Bağlı" satırıyla R'ye bağlanır. Olgunluk etiketleri: kural tam / çekirdek belli / yalnız fikir. Yazar: T = Tansu, M = LLM biçimli (Tansu hesabında), A = alıntı, G = görsel.

## Tema 1 — Seçim-momentum, evren-likidite, rejim

### X001 · 2024-10-05 13:51:36 UTC · EMA üstü kapanış ve RSI seviyesi
- Bağlı: yeni yöntem; Öneri: tema-1 #1
- Yazar: T + G (tarama ve EMA grafikleri).
- Kaynak: 1842563290372940025 (2024-10-05 13:51:36 UTC), 1842574480692150662 (2024-10-05 14:36:04 UTC), 1844069225851469851 (2024-10-09 17:35:39 UTC), 1844825767483482566 (2024-10-11 19:41:52 UTC), 1845913799976800345 (2024-10-14 19:45:19 UTC).
- Fikirler:
  - [momentum-seçim] "Son gün kapanışı EMA5-14-34-55 üzerinde olsun"; "RSI 14 son gün > 50 olsun" — son kapanış dört EMA üzerinde, son gün RSI14>50 — kural tam.
  - [momentum-seçim] "Son kapanış EMA14, EMA34, EMA55'in üzerinde ve RSI(14) son gün 50'yi geçmiş olan hisseler" — EMA5 içermeyen varyant; RSI14'ün 50 üzerinde olması — kural tam.
- Örnek ve sonuç: 9 Ekim metninde GARAN, GENIL, INVEO, KGYO, MAGEN, MEPET, NUHCM, TUCLK, TUREX; 14 Ekim INVEO/KGYO. Tarama örnekleri; sonraki işlem sonucu yok.
- Tansu'nun vurgusu: "Lütfen hisselerinizi seçiniz, teknik ve temel analizinizi yapınız."
- YORUM: "50'yi geçmiş" seviye anlatımıdır; önceki gün ≤50 veya son gün yukarı kesişim yazılı değildir. R192 ile bağ EMA üstü kapanış düzeyinde zayıftır; aynı SMC yöntemi olduğu gösterilmediğinden yeni yöntem olarak tutuldu.

### X002 · 2024-10-15 22:02:29 UTC · CMF üç pozitif / önceki üç negatif gün
- Bağlı: R137; Öneri: tema-1 #2
- Yazar: T + G (CMF grafikleri ve tarama mesajları).
- Kaynak: 1846310706263871703 (2024-10-15 22:02:29 UTC), 1848806602553385447 (2024-10-22 19:20:17 UTC), 1851719680052072481 (2024-10-30 20:15:49 UTC), 1851720332580966708 (2024-10-30 20:18:25 UTC), 1852063288533881329 (2024-10-31 19:01:12 UTC).
- Fikirler:
  - [teyit-tetik] "CMF SON 3 gün pozitif, ondan önceki 3 gün ise negatif olsun (Hisseye para girişi olsun)" — altı günlük işaret dizisi; CMF hesap periyodu yok — çekirdek belli.
  - [momentum-seçim] "EMA5 > EMA13 olsun"; "RSI21 > 50 olsun" — ilk gönderideki eşlik eden koşullar; sonraki varyantta EMA5/14/34/55 ve RSI14>50 — kural tam (EMA/RSI alt koşulları).
- Örnek ve sonuç: ETILR koşulları sağlasa da uzak durma uyarısı; GZNMI için zaten tavan olduğu uyarısı. Görsellerde MARKA ve TSGYO örnekleri var; TSGYO mesajı üç pozitif/önceki üç negatif CMF koşulunu tekrar yazar. Gerçekleşmiş işlem sonucu yok.
- Tansu'nun vurgusu: "Aslolan para girişidir."; "Para yoksa gerisine bakmaya gerek yok."
- YORUM: Para akışına öncelik desteklenir; CMF'yi R137'nin ilk kapısına taşıyan aşama değişikliği kaynakta yok.

### X003 · 2025-08-15 14:17:47 UTC · NH−NL günlük ve beş günlük eşikler
- Bağlı: R118; Öneri: tema-1 #3
- Yazar: T giriş + M (uzun rejim açıklamaları) + G (hesap çıktıları).
- Kaynak: 1956359671154884947 (2025-08-15 14:17:47 UTC), 1956454944967700857 (2025-08-15 20:36:22 UTC), 2027084975686689177 (2026-02-26 18:14:54 UTC).
- Fikirler:
  - [rejim; M] "Birkaç gün üst üste NH−NL ≥ +51 ve  NH−NL_5D ≥ +408" — N=510; günlük ±0.10N=±51, beş günlük boğa +0.80N=+408; "birkaç gün" sayısı yok — çekirdek belli.
  - [giriş; M] "NH−NL_5D ≤ −663 (spike/panik) olduktan sonra tekrar −663’ün üstüne dönüş" — beş günlük panik eşiği −1.30N=−663; üstüne dönüş alış adayı — çekirdek belli.
  - [ölçüm-ilkesi; G] "N (evren): 510 | Günlük eşik: ±51 | 5g Boğa: +408 | 5g Spike: -663" — çıktıda sayısal eşik seti; günlük NH−NL kapanışa göre 52 hafta, haftalık gösterim son beş işlem günü toplamının W-FRI kapanışı — kural tam (ölçüm ve eşikler).
- Örnek ve sonuç: 15 Ağustos çıktısında günlük NH−NL=35; 5g=177; boğa teyidine kalan 231; panik eşiğine mesafe 840. 26 Şubat ayrı 20 günlük ölçümde −102/5g −365 ve 65 günlük ölçümde −19 anlatılır; tek pencereye birleştirilmez.
- Tansu'nun vurgusu: "Şimdilik temkinli uzun; gerçek trend için katılım artmalı."
- Belirsiz: Günlük görselin başlığı "BIST 50", aynı çıktının evreni N=510. Evren başlığı ile sayı uyuşmuyor. Metin bir yerde +51'i aşma, koşul satırı ≥+51 der; eşitlik dahil satır aynen korundu.

### X004 · 2025-07-05 10:23:28 UTC · AKD kurum sürekliliği ve iki skor şeması
- Bağlı: yeni yöntem; Öneri: tema-1 #4
- Yazar: T (kısa uygulama anlatıları) + M (puanlama açıklamaları) + G (el yazısı strateji).
- Kaynak: 1941442798663643585 (2025-07-05 10:23:28 UTC), 1941822029767774507 (2025-07-06 11:30:23 UTC), 1951972240926429210 (2025-08-03 11:43:42 UTC), 1964614079252938928 (2025-09-07 08:57:51 UTC), 1971236706264207844 (2025-09-25 15:33:49 UTC), 1978894148645339180 (2025-10-16 18:41:45 UTC).
- Fikirler:
  - [tarama-evren; M] "Son 1 ayda en çok mal toplayan ilk 5 aracı kurum belirleniyor." — bir ay, bir hafta, son 1–2 gün davranışı; alternatif T metninde son 3/2/1 gün — çekirdek belli.
  - [teyit-tetik] "bu periyotlarda ki kurumsal alıcılar kısa periyotlarda satıyorsa o tahtadan hayır gelmez." — uzun pencerede toplama ile kısa pencerede satışın birlikte incelenmesi — çekirdek belli.
  - [tarama-evren] "diğer alıcıların %10'dan az olduğu ve ilk 2 aracı kurumun yüksek toplama yaptığı takası toplu hisseleri bulduk." — diğer alıcılar <%10, ilk iki kurum yoğunlaşması; "yüksek" ve "toplu" eşiği yok — çekirdek belli.
- Örnek ve sonuç: 6 Temmuz şeması 4=aylık toplayanlar son gün satışta; 3=aylık toplayan haftalık zayıf; 1=toplayıp taşıyor. Skor 2 açıklanmıyor. 3 Ağustos metni emeklilik fonları %50 üzerinde toplamışsa olumlu buluyor; bu bir zorunlu kapı olarak yazılmıyor. El yazısı görsel 22 Ağustos alıcılarının 25 Ağustos satıcılarıyla kesişimini A_t1 ∩ S_t2 üzerinden eleme, 26 Ağustos tekrar satış olup olmadığını bakma fikrini gösterir (el yazısı; okunuş yaklaşık: "26 sında 2 günde toplayanlarda satış var mı?").
- Tansu'nun vurgusu: "Buyurun Akd kodumun stratejisi"; "akd de tek başına yetmez."
- Belirsiz: 1941822029767774507'de 4 kötü/uyarı, 1 iyi; 1941442798663643585'te artı dört/üç/iki birikim, eksi satış anlatır. İki ayrı skor şemasıdır; ortak formül ve ağırlıklar yok.
- YORUM: Takasa ayrıca bakmak ile takas verisini koda bağlamak ayrı. 25 Eylül metni takas tarafının henüz koda dahil olmadığını söyler. YF AKD veri kaynağı değildir; metin Matrix IQ veya benzeri yazılımdan Excel aktarımını anlatır.

### X005 · 2025-12-04 19:03:48 UTC · VIX bant, korelasyon ve rapor varyantları
- Bağlı: R210 / R188; Öneri: tema-1 #5
- Yazar: T giriş ve kısa notlar + M (checklist anlatısı) + G (grafikler, konsol raporu). NotebookLM infografiği M biçimli açıklayıcı görseldir.
- Kaynak: 1996656703665066072 (2025-12-04 19:03:48 UTC), 1999567041905492120 (2025-12-12 19:48:27 UTC), 1999759348868796729 (2025-12-13 08:32:37 UTC), 1999774979194540153 (2025-12-13 09:34:43 UTC), 2001696307468022197 (2025-12-18 16:49:24 UTC).
- Fikirler:
  - [rejim; G] "Yavaş Üst Bant (20,2 | Off:10)"; "Hızlı Üst Bant (10,1 | Off:5)" — ofsetli Bollinger bant ayarları — kural tam (gösterge ayarı).
  - [rejim; G] "Korelasyon (VIX vs BIST 100 - 30 Günlük)" — 30 günlük korelasyon; ±0.5 referans çizgileri — kural tam (ölçüm).
  - [teyit-tetik; M] "VIX < Hızlı Bantlar & VIX RSI < MAV" — VIX RSI200, MAV=SMA10 görselden; long teyidi — çekirdek belli.
  - [teyit-tetik; G] "25 üzeri 'Güçlü Trend' demektir." — ADX>25; endeks raporunda RSI>SMA14(RSI), fiyat>SMA18/35, AO yeşil, hacim>SMA20 — kural tam (rapor koşulları).
- Örnek ve sonuç: 18 Aralık raporunda long skoru 4/5, nihai karar DİKKATLİ İYİMSERLİK; RSI 67.1<68.1, ADX 19.5, hacim 0, hacim ortalaması 5,036,280,000. Pozitif fiyat/AO/VIX resmi tek başına kusursuz sonuç olarak sunulmaz. 18 Mart rapor görselinde korelasyon 0.62 ve skor 4/5; korelasyon yorumu nakitte beklemeyi güvenli bulurken nihai karar DİKKATLİ İYİMSERLİK'tir. Gerçekleşmiş işlem getirisi yok.
- Tansu'nun vurgusu: "herşey kurallara dayalı. Duyguya yer yok. Sistem ne derse o."
- Belirsiz: "Hızlı bant" iki tanımla geçer: BB(10,1) ofset 5 (1996656703665066072) ve rapordaki "SMA 10 + Std" üst limiti (2001696307468022197). 13 Aralık master SMA20/50, ayrı rapor SMA18/35 kullanır. Metin çıkışları fiyat grafiğindeki dört göstergenin ikisinin bozulmasına bağlar; sonra VIX RSI yukarı kesişini de çıkış uyarısına katar. Tek çıkış formülüne birleştirilmedi.
- YORUM: ±0.5 kesin işlem eşiği değildir. 4/5 skoru ilk beş koşul içindir; ADX ve hacim bunların dışında. R210'daki metnin tekrarı değil, görsel parametre ve varyant eki olarak tutuldu.

### X006 · 2026-09-04 22:20:52 UTC · Fund X-Ray erken fon birikimi
- Bağlı: yeni yöntem; Öneri: tema-1 #6
- Yazar: T kısa girişler + M (uzun açıklama) + G (fon birikim tabloları).
- Kaynak: 2096000569068454011 (2026-09-04 22:20:52 UTC), 2096679609559347293 (2026-09-06 19:19:07 UTC), 2097384587525812358 (2026-09-08 18:00:27 UTC).
- Fikirler:
  - [tarama-evren; G] "ağırlık artışı + TL pozisyon artışı + en az 2 rapor boyunca devam eden artış + fiyatın henüz aşırı genişlememiş olması" — güçlü senaryonun pratik okuması; skor formülü ve fiyat genişleme eşiği yok — çekirdek belli.
  - [ölçüm-ilkesi; G] "yalnız ağırlık artışı varsa bunu tek başına alış olarak kabul etmiyoruz." — ağırlık ve TL pozisyon değişimini birlikte okuma — çekirdek belli.
- Örnek ve sonuç: 8 Eylül THF çıktısında TERA 86, TRHOL 72, TUPRS 65. 4 Eylül tablosunda TERA 86, TRHOL 77, AKBNK 78; aynı 1 Temmuz–1 Ağustos rapor dönemleri görünür. 6 Eylül görselinde TRHOL 20G %86.86, XU100 %1.69, göreceli güç 85.16 puan; ANELE %63.33/%1.69/61.64 puan. TL artışı metinde TERA 6.38 milyon, TRHOL 4.85 milyon, TUPRS 1.65 milyon diye aktarılır.
- Tansu'nun vurgusu: "Burası çok ÖNEMLİ. Fiyatı değerlenen hisse yukarıdan elinizde kalır." Görsel: "Bu liste işlem sinyali değildir".
- Belirsiz: XU100 20G girdisi 4 Eylül görselinde 0.97, 6 Eylül görselinde 1.69; TRHOL skoru 77 (4 ve 6 Eylül) / 72 (8 Eylül). Metin "birkaç rapor", görsel en az 2 rapor der. Fiyat genişlememiş olması güçlü senaryo iken 4/6 Eylül TRHOL "fiyat çok genişledi" açıklamasıyla güçlü sınıfta. Aynı rapor döneminin skorları değişir; AKBNK yeni girdiği halde ağırlık artış dönemi 2 görünür. Göreceli güç getiri−XU100 getirisiyle uyumludur, TRHOL yuvarlak değerlerinde 0.01 puan fark vardır. TL pozisyon görselleri Mr, metin milyon kullanır; birim ölçeği de açıklanmıyor.

### X007 · 2026-08-18 22:13:22 UTC · Sektör rotasyonu ve negatif VRP portföyü
- Bağlı: R031; Öneri: tema-1 #7
- Yazar: T + G (VRP portföy tablosu).
- Kaynak: 2089838087606087814 (2026-08-18 22:13:22 UTC).
- Fikirler:
  - [portföy] "1) Sektör rotasyonu yapacaksın"; "2) Karlı sektörleri bulacaksın" — sektör seçimi önce; kârlı sektör tanımı yok — yalnız fikir.
  - [portföy] "3)VRP'Sİ < 0 olan hisselere eşit oranda yatırım yapacaksın" — seçilen sektörlerde VRP<0, eşit sermaye; yenileme ve çıkış yok — çekirdek belli.
- Örnek ve sonuç: Görselde alım 2026-08-01, güncel 2026-08-19; BMSTL, CEMAS, BRSAN, DOKTA, CELHA. Maliyet 99,513.08 TL; nakit 486.92 TL; hisse değeri 108,420.92 TL; kâr 8,907.84 TL; maliyet bazlı getiri %8.95. Kaynak tablosudur; yeniden getiri hesaplanmadı.
- Tansu'nun vurgusu: "Size eylem planını anlatıyorum"
- Belirsiz: Gönderi 18 Ağustos UTC, tablo 19 Ağustos güncel tarihi taşır.
- YORUM: %8.95, 100,000 TL ana para bazlı oran değildir. R031'in yaklaşık −0.005 eşiğini bu <0 varyantı değiştirmez.

### X008 · 2025-07-22 21:45:13 UTC · Üç sektör ve 90 günlük rotasyon fikri
- Bağlı: R032; Öneri: tema-1 #8
- Yazar: M (90 gün/eşit ağırlık açıklaması) + T (kendi sektör taraması yanıtı) + G (kombinasyon tablosu).
- Kaynak: 1947774961801736417 (2025-07-22 21:45:13 UTC), 1947783188945731622 (2025-07-22 22:17:54 UTC).
- Fikirler:
  - [momentum-seçim] "En yüksek getirili ilk 3 sektörü portföy olarak seçiyor" — T metninde 30/60/90 günlük sektör performansı; sektör ortalamasının hesaplama formülü yok — çekirdek belli.
  - [portföy; M] "Her 90 günde bir son 90 günün getirilerine bak, en iyi performans gösteren 3 sektörü seç."; "Bu 3 sektörü eşit ağırlıkla portföye koy, 90 gün boyunca hiçbir değişiklik yapma." — 90 günlük bakış, bekleme ve yenileme fikri — çekirdek belli.
- Örnek ve sonuç: Görsel 3 Sectors × 90 Days hücresinde 5.282638 yazar; birim etiketi yok. M metni bunu yaklaşık %5,28 yıllıklandırılmış bileşik getiri olarak yorumlar; yıllıklandırma hesabı, dönem ve maliyet yok.
- Tansu'nun vurgusu: "Yani, hisse bazında değil sektör bazında dinamik bir portföy rotasyonu yapıyorum"
- Belirsiz: Görseldeki sayının birimi ve yıllıklandırılması doğrulanamıyor; %5,28 yorumu M metnine aittir.
- YORUM: "Sektörlerin ortalama getirileri" yazılıdır; "sektör getirisi = eşit ağırlıklı hisse ortalaması" bu iki gönderide yok.

### X009 · 2026-09-06 16:59:12 UTC · TEFAS sınıf akışı ve risk iştahı
- Bağlı: yeni yöntem; Öneri: tema-1 #9
- Yazar: T (kısa akış notları) + M (uzun rejim anlatıları) + G (akış tabloları ve grafikler).
- Kaynak: 2096644397110534476 (2026-09-06 16:59:12 UTC), 2097018434563473539 (2026-09-07 17:45:30 UTC), 2099556801611977021 (2026-09-14 17:52:04 UTC), 2099565529698545872 (2026-09-14 18:26:44 UTC), 2099967840405086603 (2026-09-15 21:05:23 UTC).
- Fikirler:
  - [rejim; M] "PPF çıkışı devam ederken HSF ve diğer riskli gruplara giriş devam ederse risk iştahındaki artışın daha güçlü teyidini almış oluruz." — 5 ve 20 işlem günü akış yönlerini birlikte izleme; rejim eşiği yok — çekirdek belli.
  - [boyut-risk] "Fon çıkışı var → hangi hisseler ağır basıyorsa teorik satış baskısı oralarda daha yüksek." — fon akışı ile portföy ağırlıkları; short pozisyon küçültülüyorsa short kapamadan alım oluşabilir — çekirdek belli.
- Örnek ve sonuç: 7 Eylül görseli HSF 1G −4.24 Mr, 5G +10.73 Mr, 20G +45.88 Mr; PPF 1G +25.49 Mr, 5G −33.08 Mr, 20G +82.50 Mr. 14 Eylül sınıf tablosu (tek okuma, Codex; ikinci okumayla doğrulanmadı): HSF 5G +41.41/20G +93.21 Mr; SER +130.23/+178.28 Mr; PPF −298.35/−322.25 Mr. Aynı günün fon grafikleri eksende "Milyon TL" kullanır (THF ≈120k). Kaynak değerleridir; akış yeniden hesaplanmadı.
- Tansu'nun vurgusu: "Önce şu PPF para giriş çıkışlarına ve 20 günlük getirilere bakalım"
- Belirsiz: 2097018434563473539 metni HSF 1G +4.24 ve PPF 5G +33.1 milyar giriş der; görsel ikisini çıkış gösterir. PPF 20G, 7 Eylül metninde +82.5 milyar (görsel +82.50 Mr), 14 Eylül metninde −322.3 milyon (görsel −322.25 Mr). İkinci metin/görselde bin kat birim farkı vardır; 14 Eylül diğer sınıf tutarları da metinde milyon, tabloda Mr'dır. Grafik ekseni milyon TL kullanır; bu, sınıf tablosunun ölçeğini tek başına çözmez.
- YORUM: Serbest fon girişi doğrudan borsaya giriş değildir. Eşzamanlı PPF çıkışı/HSF girişi kanıtlanmış para transferi değildir; metin de bunu ayırır. 5G ve 20G yön uyumu otomatik alım kuralına çevrilmedi.

### X010 · 2024-09-24 20:01:12 UTC · Vegas EMA dizilimi ve kesişim varyantı
- Bağlı: yeni yöntem; Öneri: tema-1 #10
- Yazar: T + G (Vegas tarama grafikleri).
- Kaynak: 1838670037353374138 (2024-09-24 20:01:12 UTC), 1839308965039190302 (2024-09-26 14:20:04 UTC), 1845923939736080720 (2024-10-14 20:25:37 UTC), 1846638825864413237 (2024-10-16 19:46:19 UTC), 1846640825771377067 (2024-10-16 19:54:16 UTC).
- Fikirler:
  - [momentum-seçim] "ema13 >ema144>ema169" — EMA13/144/169 sıralaması, hisse bazında optimizasyon önerisi — kural tam (dizilim).
  - [teyit-tetik] "12 günlük EMA'nın 144 ve 169 günlük EMA'yı yeni yukarı kestiği hisseler" — ayrı EMA12 kesişim varyantı; "yeni" süresi yok — çekirdek belli.
  - [teyit-tetik] "günlükte iyi çalışır. para girişini takip etmek şartı ile" — günlük uygulamada para girişi takibi; ölçüt yok — yalnız fikir.
- Örnek ve sonuç: 15 dakikalık taramada DOAS/KRTN; EMA12 çıktısında EGEPO; günlük görsel TUCLK Vegas Tüneli. Tavan bulma kaynak iddiası; işlem tarihleri ve gerçekleşmiş sonuç yok.
- Tansu'nun vurgusu: "Bununla tavan hisseler bulduk." (1845923939736080720; "ideal" sözü idealborsa yazılımına yanıttır, vurgu değildir).
- YORUM: R214 EMA5/8/13 ve destek tepkisiyle ilgilidir; Vegas ona ek koşul değildir. EMA12 kesişimi ve EMA13 dizilimi birbirinin yerine geçmez.

### X011 · 2024-10-17 20:15:20 UTC · EMA kesişimi, MACD, RSI ve OBV değişimi
- Bağlı: R196 / R230; Öneri: tema-1 #11
- Yazar: T + G (tarama ve sinyal grafikleri).
- Kaynak: 1847008515014922537 (2024-10-17 20:15:20 UTC), 1851719680052072481 (2024-10-30 20:15:49 UTC).
- Fikirler:
  - [teyit-tetik] "EMA5 ve EMA10, EMA20'yi yukarı kesmiş"; "MACD > MACD Sinyal Çizgisi:" — son gün iki EMA yukarı kesişimi ve MACD sinyal üstü; MACD periyotları yok — çekirdek belli.
  - [teyit-tetik] "RSI14 > 50"; "RSI14 önceki gün ≤ 50" — son gün RSI14 50 yukarı geçişi — kural tam (RSI alt koşulu).
  - [teyit-tetik] "OBV (On Balance Volume) artışı: Son 5 günlük OBV değişimi pozitif" — OBV seviyesi değil son beş günlük değişim >0 — kural tam (OBV alt koşulu).
- Örnek ve sonuç: 17 Ekim görselinde EGSER/INVEO/KGYO listesi ve EGSER dört panelli grafik; 30 Ekim mesaj görselinde INVEO/KGYO/MERIT ve son kapanış EMA5 üzerinde koşulu. Doğrulama raporunda ayrıca MERIT grafiği. Sonraki getiri yok.
- Tansu'nun vurgusu: "Aslolan para girişidir."
- Belirsiz: 30 Ekim mesaj görseli "EMA5-10-20 MACD RSI14-50 VE OBV50" der; "OBV50" tanımsızdır ve 17 Ekim metnindeki "son 5 günlük OBV değişimi pozitif" ile aynı olduğu yazılı değildir.
- YORUM: R196 dış LLM infografiğidir; bu koşullar Tansu'nun ayrı metni ve çıktısıdır. Son gün kesişim ile yalnız EMA üstünde olma aynı değildir.

### X012 · 2025-12-25 20:24:23 UTC · ADX ve BBW yatay piyasa filtresi fikri
- Bağlı: yeni yöntem; Öneri: tema-1 #12
- Yazar: M (LLM biçimli açıklama; Tansu hesabında).
- Kaynak: 2004287128214356186 (2025-12-25 20:24:23 UTC).
- Fikirler:
  - [rejim; M] "ADX 20 seviyesinin altına indiğinde trendin gücünü yitirdiğini, BBW değeri ise son 100 barın en düşük %20’lik dilimine (rolling percentile) girdiğinde piyasanın iyice daraldığını anlarız." — ADX<20 ve BBW son 100 barın alt %20 dilimi; hesap periyotları ve Bollinger sapma katsayısı yok — çekirdek belli.
  - [giriş; M] "Sisteminize eğer ADX düşük ve BBW dar ise işlem açma şeklinde bir kural ekleyerek testere piyasasında doğranmaktan kurtulabilirsiniz." — iki ölçünün birlikte işlemden kaçınma filtresi olması — çekirdek belli.
- Örnek ve sonuç: Kod, araç çıktısı veya kişisel uygulama örneği yok; açıklama fikri olarak alındı.
- Tansu'nun vurgusu: Metin matematiksel filtreyi önerir; Tansu'nun uyguladığı bağımsız olarak gösterilmez.
- YORUM: Yalnız M olduğu için alınmama kararı geçersizdir; eksik parametreler tamamlanmadı.

### X013 · 2025-07-20 13:30:32 UTC · Bileşik toplam getiriyle momentum
- Bağlı: R120; Öneri: tema-1 #13
- Yazar: M + G (Apple aylık getiri tablosu).
- Kaynak: 1946925694652674087 (2025-07-20 13:30:32 UTC).
- Fikirler:
  - [ölçüm-ilkesi; M] "Daha sonra tüm bu brüt getiriler birbiriyle çarpılır ve sonuçtan 1 çıkartılarak toplam 12 aylık net getiri (momentum skoru) bulunur." — Π(1+aylık getiri)−1; metin toplam getiriyi temettü dahil tanımlar, 12 ay örnektir — çekirdek belli.
- Örnek ve sonuç: Apple 2014 örneği; tablo Toplam Momentum %40.63, metin %40,62 yazar. Metin Ocak −%10,77 → 0,8923 dönüşümünü gösterir. Eski veri/örnek olarak sunulur; veri ve temettü düzeltmesi bağımsız doğrulanmadı, getiri yeniden hesaplanmadı.
- Tansu'nun vurgusu: "Veriler eskidir ve örnek amaçlıdır."
- Hesap: metindeki 12 çarpanın çarpımı 1.40629 → %40,63 (görsel "Toplam Momentum 40.63%"); metindeki %40,62 yuvarlama hatasıdır. Karşılaştırma: piyasa 2014 %13,46.

### X014 · 2026-01-10 08:07:05 UTC · Ay etkisi ve anlamlılık sınırı
- Bağlı: R183; Öneri: tema-1 #14
- Yazar: T giriş/vurgu + M (başlıklı hisse yorumu) + G (istatistik tablosu ve Şubat grafiği).
- Kaynak: 2009899784748794098 (2026-01-10 08:07:05 UTC), 2018404523635515480 (2026-02-02 19:21:53 UTC).
- Fikirler:
  - [rejim; M] "Çünkü P-Value: 0.027 (<0.05)." — KRDMB Ocak örneğinde t testi anlamlılık sınırı 0.05; sıfır hipotezi ve hesap ayrıntıları yok — çekirdek belli.
  - [ölçüm-ilkesi] "İstatistik ile bu noktaları belirlemek ve sizlerin bulacağı kesişimler ile teyitleşmelerini sağlamak ayrı bir güven verir." — ay istatistiğini başka teyitlerle birlikte değerlendirme — yalnız fikir.
- Örnek ve sonuç: Görsel KRDMB t=2.549, p=0.027; ASTOR/GMTAS W/L=INF, ortalama kayıp 0. Şubat çıktısında 5 pozitif/7 negatif/12 gözlem, başarı %41.7, ortalama −%0.54, maksimum +%8.20, minimum −%11.03, standart sapma %5.02.
- Tansu'nun vurgusu: "SADECE Çizgiler çizmek bana pek anlamlı gelmiyor"
- Belirsiz: Gönderi 2 Şubat, görselde 2026 Şubat da var; tam ay sonucu değildir. Veri kesimi ve az gözlemli hisselerin kesin gözlem sayısı yok.
- YORUM: p<0.05 gelecek ay kazancını kanıtlamaz; INF oranı kayıpsız fakat az gözlemli örneklerde güvenilirlik sorunu olarak anılır.

### X015 · 2026-08-19 19:15:28 UTC · İki varyans taramasının kesişimi
- Bağlı: R028 / R029; Öneri: tema-1 #15
- Yazar: T + G (INTC/MU kesişim tablosu); kendi gönderisini alıntıladığı için A değil.
- Kaynak: 2090155705340768358 (2026-08-19 19:15:28 UTC), 2090161750444327119 (2026-08-19 19:39:29 UTC).
- Fikirler:
  - [tarama-evren] "sonr bu iki kodun kesşim kümesi sizin volatlite kaynaklı kazanç kapınız olur." — gerçek IV kullanan risk premium varyans modeli ∩ modelden bağımsız varyans replikasyonu; hesap ayrıntıları yok — çekirdek belli.
  - [hedef-çıkış] "bu 2 hissede %12 oranında yukarı yönlü hareket mümkün der strateji." — Tansu'nun yön iddiası; yön üreten kural yok — yalnız fikir.
- Örnek ve sonuç: Görsel INTC skew 0.189, IM %12.6, RV %79.9, IV %60.7, VRP −%19.2; MU 0.192, %12.7, %103.5, %62.2, −%41.3. İki vade 2026-09-11. Gerçekleşmiş sonuç yok.
- Tansu'nun vurgusu: "Yanıladabilirim, iyice bakın."
- Belirsiz: Metnin son tarihi 10/09/2026, tablonun vadesi 11/09/2026. IM% sütunu yön göstermiyor; yukarı beklentisi ayrı metin iddiasıdır. R028'deki ± hareketle tek yön kuralına birleştirilmez.

### X016 · 2025-01-11 12:03:08 UTC · Faz, sinyal tepkisi ve kayan performans
- Bağlı: R202 / R200; Öneri: tema-1 #16
- Yazar: T + M (kayan pencere açıklaması) + G (beta/alpha çıktıları).
- Kaynak: 1878050003647697038 (2025-01-11 12:03:08 UTC), 1878050007133106656 (2025-01-11 12:03:08 UTC), 1878132805504254308 (2025-01-11 17:32:09 UTC), 1953112693407203768 (2025-08-06 15:15:27 UTC).
- Fikirler:
  - [momentum-seçim] "Faz 1 olan hissede, fiyat sinyale çok zayıf tepki veriyor ise kazanç zor" — faz ve fiyatın sinyale tepkisi; tanımlar/eşikler yok — yalnız fikir.
  - [rejim] "yükselen endekste yüksek beta ve yüksek alpha’lı hisseler kazanç sağlar." — yükselen endeks bağlamındaki yüksek beta seçimi — yalnız fikir.
  - [boyut-risk; M] "yüksek kayan alpha yüksek kayan sharpe oranı ve düşük beta birleştiğinde" — üçlü kapı; eşik yok — çekirdek belli.
  - [ölçüm-ilkesi; M] "örneğin yirmi günlük veya altmış günlük" — her gün yenilenen kayan alpha/Sharpe; yüksek kayan alpha/Sharpe ve düşük beta önerisi; 20/60 örnek — çekirdek belli.
- Örnek ve sonuç: Görselde GARAN aylık beta 0.989105/alpha 0.0262466; günlük beta 1.01549/alpha 0.00122143. Bunların 20/60 gün kayan hesap olduğu yazılı değil; gerçekleşmiş işlem sonucu yok.
- Tansu'nun vurgusu: "Faz, sinyal uyumluluğu, beta ve alpha kazancın kapısıdır."
- Belirsiz: "yükselen endekste yüksek beta ve yüksek alpha" (T, 1878050003647697038) ile M üçlüsündeki "düşük beta" çelişir; iki ayrı rejim iddiası olarak tutuldu.
- YORUM: Düşük beta her rejimde değişmez kapı değildir. M metninin GARCH ile merkez bankası metinlerinden politik yoğunluk endeksi üretme iddiasının kodu/çıktısı yok; doğrulanmış GARCH hesabı olarak alınmadı.

### X017 · 2025-02-13 19:57:30 UTC · İki momentum kodu ve 0.50 sinyal çıktısı
- Bağlı: R137; Öneri: tema-1 #17
- Yazar: T (iki kod anlatısı; sonraki şiir) + M (model açıklaması) + G (tarama tablosu).
- Kaynak: 1890128183972008095 (2025-02-13 19:57:30 UTC), 1920446141105103040 (2025-05-08 11:50:14 UTC), 1965629890100941012 (2025-09-10 04:14:20 UTC).
- Fikirler:
  - [momentum-seçim] "regresyon kırılımlarını buluyorum genelde 60 gün tercih ediyorum" — ilk kodun tercih edilen penceresi 60 gün; kırılım tanımı yok — çekirdek belli.
  - [momentum-seçim] "diğerinde ise 16 günlük hareketli pencere ile momentum hisselerini" — ayrı momentum kodunda 16 gün; ML ile momentum olasılığı hesaplama/test etme anlatılır — çekirdek belli.
  - [momentum-seçim; G] "0.50 ÜSTÜNDE SİNYAL VEREN HİSSELER:" — görsel SİNYAL sütununa göre çıktı filtresi — çekirdek belli.
- Örnek ve sonuç: Görselde 9 analiz, 7 sinyal 0.50 üstünde, 2 altında; GSDDE 0.728, fiyat 10.59; HACİM 1.5x, CMF ARTAN, ADX>20 onaylı. Diğer seçilmiş satırlarda üç onay birlikte bulunmuyor.
- Tansu'nun vurgusu: "oldukça uzun 2 tane kodum var"
- Belirsiz: 0.50'nin olasılık olduğu ve tablonun aynı ML modelinden geldiği açıklanmıyor. 60 ve 16 gün ayrı kodlara ait. 1965629890100941012 metni şiirdir; teknik eşik yalnız görselde.
- YORUM: "Olasılık >0.50" yazılı işlem kuralı değildir; üç kontrol sütunu da ortak zorunlu kapı değildir. M açıklamasındaki 1–2 gün gecikme ve agresif backtest getirileri gerçekleşmiş başarı kanıtı değildir.

### X018 · 2024-10-09 17:39:13 UTC · Hisse taramasında EMA50/EMA200 Golden Cross
- Bağlı: yeni yöntem (R131 yalnız MA üstü/altı ilkesiyle uzak bağ); Öneri: tema-1 #18
- Yazar: T + G (hisse kesişim grafikleri).
- Kaynak: 1844070126406250885 (2024-10-09 17:39:13 UTC), 1844838137366806837 (2024-10-11 20:31:02 UTC).
- Fikirler:
  - [teyit-tetik; G] "EMA 50, EMA 200'ü 1 gün önce yukarı kesti." — GLRYH/SUNTK çıktısı; BMSCH grafiğinde iki gün önce varyantı — kural tam (hisse kesişimi).
- Örnek ve sonuç: GLRYH fiyat 12.36, EMA50 11.81, EMA200 11.80; SUNTK 20.50/18.56/18.52. BMSCH görselinde iki günlük kesişim örneği 23.44/22.33/22.27. Sonraki getiri yok.
- Tansu'nun vurgusu: "Bu ikisine dikkat arkadaşlar."
- Belirsiz: 11 Ekim metni KGYO/INVEO için veri gelmediğini fakat Golden Cross uyarısı geldiğini söyler; iki grafik GLRYH/SUNTK'dir. KGYO/INVEO doğrulanmış grafik örneği sayılmaz.
- YORUM: R128 EMA50/100/200 dizilimi ayrı koşuldur. Önerinin endeks rejimi parçası ve 1847537834397237420 bu kayda alınmadı.

### X019 · 2025-07-03 06:57:37 UTC · GARCH risk başına getiri fikri
- Bağlı: R097; Öneri: tema-1 #19
- Yazar: M (iki genel açıklama).
- Kaynak: 1940666220354654588 (2025-07-03 06:57:37 UTC), 1952471946383265824 (2025-08-04 20:49:21 UTC).
- Fikirler:
  - [ölçüm-ilkesi; M] "Ardından her hissenin ortalama getirisi ile ortalama tahmini volatilitesini karşılaştırırsınız. Bu oran aslında hisselerin risk başına getiri kapasitesidir." — ortalama getiri / ortalama GARCH tahmini volatilitesi; model derecesi/veri penceresi yok — çekirdek belli.
  - [boyut-risk; M] "Sharpe’ı yüksek, beta’sı düşük hisseleri portföye seçmek" — yüksek volatilite bağlamındaki korunma önerisi; yüksek/düşük eşikleri yok — yalnız fikir.
- Örnek ve sonuç: 20 hisselik tarama varsayımsal; kendi GARCH kodu veya araç çıktısı yok.
- Tansu'nun vurgusu: Metin riskin zamanla değişimini öne çıkarır; kişisel uygulama kanıtı yok.
- YORUM: M fikirleri alındı; R097'de vaat edilen uygulamanın gerçekleştiği sonucu çıkarılmadı.

### X020 · 2025-07-02 18:48:52 UTC · Sharpe ile risk verimliliği sıralaması
- Bağlı: R110; Öneri: tema-1 #20
- Yazar: M (genel Sharpe açıklaması).
- Kaynak: 1940482825427235036 (2025-07-02 18:48:52 UTC).
- Fikirler:
  - [ölçüm-ilkesi; M] "Sharpe = (Getiri - Risksiz Faiz) / Volatilite" — fazla getiri / standart sapma; ortalama getiri yıllık veya son altı ay, risksiz faiz örneği yıllık %30 — çekirdek belli.
  - [momentum-seçim; M] "Sharpe oranı en yüksek olanlar, yani birim risk başına en çok kazandıranlar en üstte sıralanır." — Sharpe azalan sıralama — çekirdek belli.
- Örnek ve sonuç: BIST100/BES fonları/portföy stratejileri örnek evrenlerdir; sayısal tarama çıktısı yok.
- Tansu'nun vurgusu: Metin getiriyi riskle birlikte seçmeyi önerir; kişisel uygulama gösterilmez.
- Belirsiz: Altı aylık getiri ile yıllık risksiz faizin zaman ölçeği nasıl eşleştirilecek, yazılı değil.
- YORUM: %30 sabit Tansu parametresi değildir; R110 Max Sharpe portföyünün ayarı olarak aktarılmaz.

### X021 · 2026-08-02 11:21:16 UTC · Büyüme yavaşlaması ve altın gözlemi
- Bağlı: yeni yöntem; Öneri: tema-1 #21
- Yazar: M (2083875779218198689, 2083875781457928398 gövdeleri, LLM biçimli) + T (2083875783332741531 son satırları: "2026/Q3 önemli", "Mesaj umarım alındı") + G (ABD büyüme/altın grafiği).
- Kaynak: 2083875779218198689 (2026-08-02 11:21:16 UTC), 2083875781457928398 (2026-08-02 11:21:17 UTC), 2083875783332741531 (2026-08-02 11:21:17 UTC).
- Fikirler:
  - [rejim] "ABD ekonomisinde üst üste en az iki çeyrek yaşanan büyüme yavaşlamaları (gri alanlar)" — reel GSYİH büyüme hızının art arda en az iki çeyrek yavaşlaması — çekirdek belli (gözlem koşulu).
  - [rejim] "teknik resesyon veya durgunluk şartlarını beklemeden, sadece büyümedeki yavaşlama sinyalleri bile yatırımcıyı güvenli limanlara yönlendirmeye yetiyor." — negatif büyüme şartı değil yavaşlama gözlemi — yalnız fikir.
- Örnek ve sonuç: Görselde getiri yazılı 13 dönemin 9'u pozitif, 4'ü negatif; ilk iki gri alanda getiri etiketi yok. Pozitifler %24.7/21.7/15.8/0.1/26.9/3.4/28.0/16.4/40.4; negatifler −%7.5/−%10.4/−%6.7/−%2.4. Grafik kaynağı BEA NIPA Tablo 1.1.1 ve NYMEX altın vadeli işlemleri olarak yazılıdır. Kaynağın tarihsel gözlemi; yeniden getiri hesaplanmadı. Metin 2026/Q1=2.1, Q2=1.5 aktarır.
- Tansu'nun vurgusu: "2026/Q3 önemli"
- YORUM: 9/13 bütün gri alanların oranı değildir. Q1→Q2 tek ardışık düşüş, iki çeyrek üst üste yavaşlamayı tek başına kanıtlamaz; otomatik altın alım kuralı yok.

### X022 · 2026-02-03 19:17:00 UTC · ALARK eğim × R² örneği
- Bağlı: R176; Öneri: tema-1 #22
- Yazar: T + G (hesap çıktısı ve grafik).
- Kaynak: 2018765685091139701 (2026-02-03 19:17:00 UTC).
- Fikirler:
  - [momentum-seçim] "Yıllıklandırılmış Eğim (Getiri Gücü): 1.5565"; "Trend Kalitesi (R-kare): 0.8749" — eğim ve R² ile momentum örneği; hesap penceresi yok — çekirdek belli.
- Örnek ve sonuç: Metin skoru 1.3617; görsel başlığı ALARK.IS günlük analiz Son 250 Gün, Sinyal çizgisi ve 0.5 referansı. Görünen aralık Kasım sonu–Şubat başı, yaklaşık 45 işlem günüdür; 250 günlük hesap penceresi kanıtlanmaz.
- Tansu'nun vurgusu: "Yeşil ve mavi çizgilerin ne olduğunu sormayın:)"
- Belirsiz: Doğrulama raporu yuvarlak girdilerin çarpımını yaklaşık 1.3618, çıktıyı 1.3617 bulur; gizli hassasiyet açıklanmıyor. Sinyal serisinin tanımı ve 0.5 referansının rolü yok.
- YORUM: Grafik başlığı hesap penceresi olarak alınmadı; R176 formülü değişmedi.

### X023 · 2025-07-20 18:51:28 UTC · Sektör, Convex Hull ve hisse seçimi sırası
- Bağlı: R178 / R002; Öneri: tema-1 #23
- Yazar: T (kısa girişler/kendi çalışmaları) + M (sistematik seçim açıklamaları) + G (korelasyon ve trend grafikleri). Kendi gönderisini alıntıladığı için A değil.
- Kaynak: 1947006461487517762 (2025-07-20 18:51:28 UTC; 1947024537079468538 içinde alıntılanır), 1949014576458023063 (2025-07-26 07:51:00 UTC), 1951627374774087770 (2025-08-02 12:53:20 UTC), 1951634776156258423 (2025-08-02 13:22:44 UTC), 1955360082641948922 (2025-08-12 20:05:47 UTC).
- Fikirler:
  - [portföy; M] "Sıralama → Momentum → Convex Hull → Cross-Sectional Momentum"; "En sonunda markowitz ya da black-litterman ile hisselerin portföy ağırlıklarını belirliyorsun." — güçlü sektörler (30–90 gün örnek) → risk/getiri köşeleri → sektör içi göreli momentum → portföy ağırlıkları — çekirdek belli.
  - [momentum-seçim] "Ardından momentumu en yüksek 10 sektörün momentum faz alanında olan en güçlü 10 hissesini belirledik." — faz alanındaki güçlü hisseler; eşikler yok — çekirdek belli.
  - [teyit-tetik] "Son 10 günde yükselen trende temas eden, pullback yapan veya tepki veren hisseleri ayrı ayrı değerlendirdim." — ayrı teknik incelemeler; trend tanımı yok — çekirdek belli.
- Örnek ve sonuç: Görselde son 30 gün getirisi en yüksek 10 sektörün 30 günlük getiri korelasyon matrisi; ALBRK trend temas görselinde ilk temas 2025-05-06, son temas 2025-06-20. 2 Ağustos metni 1 Temmuz itibarıyla beş yıllık veriye bakıldığını söyler. Gerçekleşmiş portföy sonucu yok.
- Tansu'nun vurgusu: "Bırakın sağa sola çizgi çizmeyi. market yapısını anlayın"
- Belirsiz: 10 hisse sektör başına mı toplam mı, açık değil.
- YORUM: 1949014576458023063'teki "yatırım fonları için de pratikte aynen bu şekilde kullanılıyor" iddiası kaynaksızdır.
- YORUM: Korelasyon, faz ve bayrak taramaları farklı çalışmalardır; Convex Hull sırasının zorunlu ek kapıları değildir. Tam zincir M biçimli açıklamadır; kendi uygulamasının bütün parametreleri verilmez.

### X024 · 2024-09-24 19:36:54 UTC · Supertrend, MOST ve KAMA ayrı varyantları
- Bağlı: R148; Öneri: tema-1 #24
- Yazar: T + G (trend listeleri ve TDGYO grafiği).
- Kaynak: 1838663920996831643 (2024-09-24 19:36:54 UTC), 1841917340419559794 (2024-10-03 19:04:49 UTC), 1843373717247922211 (2024-10-07 19:31:57 UTC), 1844830887294197939 (2024-10-11 20:02:13 UTC), 1844832419821539723 (2024-10-11 20:08:18 UTC), 1853065056759550021 (2024-11-03 13:21:52 UTC).
- Fikirler:
  - [teyit-tetik] "Hiç bir hisse son gün RSI14 > 50 şartını sağlamamaktadır." — yalnız 3 Ekim Supertrend varyantına RSI14>50; sonuç boş — çekirdek belli.
  - [teyit-tetik] "Supertrend yukarı trenddeyken son gün KAMA al sinyali veren hisseler:" — Supertrend yukarı ∩ son gün KAMA al; hesap parametreleri yok — çekirdek belli.
  - [momentum-seçim] "MOST AL SİNYALİ GELENLER" — ayrı MOST giriş listesi; parametreler yok — yalnız fikir.
- Örnek ve sonuç: Supertrend+KAMA metninde KERVT/MERKO/SANFM/TDGYO; TDGYO görselinde KAMA/Supertrend yönleri ve al işareti. Sonraki getiri yok.
- Tansu'nun vurgusu: "sadece yelpazenizi daraltmanıza yardımcı oluyorum."
- YORUM: RSI şartı MOST'a veya Supertrend+KAMA'ya taşınmaz. Üç tarama tek birleşik kural değildir; R148 HalfTrend kuralı değişmez.

### X025 · 2025-06-29 20:02:03 UTC · Takasın kalıcılığı ve birleşik gözlem sorusu
- Bağlı: yeni yöntem (takas dağılımı; R225 emir defteri derinliğidir); Öneri: tema-1 #25
- Yazar: M (genel takas açıklaması) + T (sonraki gözlem sorusu).
- Kaynak: 1939414080336670931 (2025-06-29 20:02:03 UTC), 1983492569574056243 (2025-10-29 11:14:14 UTC).
- Fikirler:
  - [tarama-evren; M] "takasta ilk 5’te sürekli Ak Portföy, Anadolu Hayat, İş Portföy gibi isimler varsa; bu hisse genellikle sağlıklı bir yatırım akışına sahiptir." — kalıcı kurumsal fon ağırlığını olumlu okuma; kesin sınıf değil — yalnız fikir.
  - [tarama-evren; M] "Eğer yabancı oranı çok düşükken bir anda sert artış oluyorsa ve kısa sürede satış geliyorsa" — hızlı yabancı artışını izleyen kısa sürede satış spekülatif davranış olabilir; açığa satış demiyor — yalnız fikir.
  - [teyit-tetik] "takasında yatırım fonları ve citi nin dominant olduğu, akd'de hissenin toplandığı, küçük yatırımcının hisseden şutlandığı" — T sorusunda ayrıca alış/satış 27.6x, son işlem gününde negatif getiri; eşik yok — yalnız fikir.
- Örnek ve sonuç: Hisse sembolü veya gerçekleşmiş sonuç yok; 27.6x örnek gözlemdir. M metni kalıcı yabancı kurum varlığı ile ani yabancı artışını ayırır.
- Tansu'nun vurgusu: "Şimdi size sorayım"
- YORUM: M açıklama fikir olarak alındı; "genellikle", "düşündürür", "olabilir" kesin sağlık/manipülasyon hükmüne çevrilmedi. T sorusu alım kararı veya cevap değildir.

### X026 · 2025-06-17 16:42:28 UTC · Temel, teknik ve takasın birleşmesi
- Bağlı: R166; Öneri: tema-1 #26
- Yazar: T (kavramsal, varsayımsal örnek).
- Kaynak: 1935015198277951650 (2025-06-17 16:42:28 UTC).
- Fikirler:
  - [temel-değerleme] "Bir hisse düşün. Son bilançosunda net kârı %80 artmış, satışları güçlü. Bu temel analiz." — örnek net kâr %80; güçlü satış eşiği yok — yalnız fikir.
  - [teyit-tetik] "Aynı hisse son günlerde 60 günlük direnç bölgesini kırmış ve hacim artışı var." — örnek 60 günlük direnç ve hacim, ikisi aynı teknik ayağa ait — çekirdek belli.
  - [teyit-tetik] "Takas tarafında ise son günlerde hisseyi alan aracı kurumlar genellikle kurumsal ağırlıklı ve satanlar küçük yatırımcı." — üçüncü ayak takas; süre/oran yok — yalnız fikir.
- Örnek ve sonuç: Varsayımsal hisse; sembol veya gerçekleşmiş kazanç yok.
- Tansu'nun vurgusu: "doğru analizleri bir araya getirmek."
- YORUM: Üç ayak temel/teknik/takas; %80 ve 60 gün zorunlu tarama parametresi değildir.

### X027 · 2025-10-18 23:46:40 UTC · Fon yatırımcı sayısını kontrol etme
- Bağlı: yeni yöntem; Öneri: tema-1 #27
- Yazar: T giriş ve açıklamalar + M (risk gövdesi) + G (NMG satırlı iki tablo).
- Kaynak: 1979695659432427919 (2025-10-18 23:46:40 UTC), 1979721101304361294 (2025-10-19 01:27:46 UTC), 1979721927809012208 (2025-10-19 01:31:03 UTC).
- Fikirler:
  - [tarama-evren] "Fon seçerken neden içerdeki yatırımcı sayısına bakmak gerekriğini, bakmaz isek hangi riskler ile karşılaşacağımızı yazıyorum." — yatırımcı sayısı incelemesi; alt sınır yok — yalnız fikir.
  - [boyut-risk] "11 kişilik fonda bu kadar yüksek getiri çok tehlikelidir" — örnekten risk uyarısı; genel sayısal dışlama eşiği değil — yalnız fikir.
- Örnek ve sonuç: 22.04.2025 tarihli görsel NMG yatırımcı sayısı 11. Diğer görsel gözlem 121, kümülatif getiri %9944, Sharpe 106.17. Ekim gönderisinin güncel yatırımcı sayısı veya iki tablonun aynı dönemi olduğu kanıtlanmaz.
- Tansu'nun vurgusu: "kardeşim burada bir fonu yorumlamıyorum. Fon özelinde konuşmuyorum."
- Belirsiz: İki tablo farklı tarih/dönem bilgisi taşır; birlikte tek günün ölçümü gibi okunamaz.
- YORUM: M gövdesindeki manipülasyon, denetim ve çıkamama iddiaları doğrulanmış NMG bulguları değildir. Kullanıcı BisTurkey'nin sözü yöntem kanıtı olarak alınmadı.

### X028 · 2025-07-15 07:19:45 UTC · Manipülasyon işaretleri fikri
- Bağlı: yeni yöntem; Öneri: tema-1 #28
- Yazar: T başlık + M (genel açıklama gövdesi).
- Kaynak: 1945020445117264368 (2025-07-15 07:19:45 UTC).
- Fikirler:
  - [tarama-evren; M] "şirketin temellerine dayanmayan, aracı kurum dağılımı tek taraflı olan ve sosyal medya baskısı altında fiyatlanan hisselerden uzak durmaktır." — nitel uzak durma fikri; ölçülebilir eşikler yok — yalnız fikir.
  - [tarama-evren; M] "İkinci önemli sinyal, fiyatın çok dar bir aralıkta hızlı hareketler yapmasıdır." — beş işaret: habersiz ani hacim/fiyat; gün içi çekilip son dakika düşürülen fiyat; belli kurum yoğunluğu; sosyal medya/forum baskısı; temel/fiyat uyuşmazlığı — yalnız fikir.
- Örnek ve sonuç: Hisse adı, tarama çıktısı veya kişisel uygulama yok.
- Tansu'nun vurgusu: "Manipülasyonu nasıl anlarız"
- YORUM: Beş işaret kaynaktaki açıklamadır; otomatik evren dışlama kuralı veya belirli bir hissede manipülasyon kanıtı değildir.

### X029 · 2026-09-06 17:43:49 UTC · Fon getiri sıralaması ve risk uyarıları
- Bağlı: yeni yöntem; Öneri: tema-1 #29
- Yazar: T + G (TEFAS getiri/risk tabloları).
- Kaynak: 2096655622938693877 (2026-09-06 17:43:49 UTC), 2096661898385113202 (2026-09-06 18:08:45 UTC), 2097381679560102246 (2026-09-08 17:48:54 UTC), 2099564220601835538 (2026-09-14 18:21:32 UTC), 2099569262847230211 (2026-09-14 18:41:35 UTC).
- Fikirler:
  - [momentum-seçim; G] "Sıralama TEFAS resmi 1 Ay Getiri (%) verisine göre azalan sıradadır." — seçili PPF evreninde 1 ay getiri azalan sıralama, ilk 10 — kural tam.
  - [boyut-risk] "Elbette stress testi önemli, onu da he gün yapıyorum likidite kontrolü için" — günlük likidite stres kontrolü; yöntemi/eşikleri yok — yalnız fikir.
  - [momentum-seçim; G] "1 Ay Getirisi En Yüksek İlk 50 Fon" — PPF ekranında 1A getirisi bulunan 154 fon arasından ilk 50 — kural tam.
- Örnek ve sonuç: 6 Eylül KHP ilk, %4.50; 8 Eylül görselinde KHP %4.20; 14 Eylül PPF ekranında PNU ilk %4,59. Risk alanları Sharpe/Sortino/yıllık volatilite/maksimum düşüş/Calmar; 6 Eylül HSF tablosunda ayrıca Beta/Treynor/M²/Jensen Alpha. Veri uyarıları doğrulama raporunda 1A uç getiri, düşük AUM, aşırı drawdown; eşikleri yok. Sonraki yatırım sonucu yok.
- Görsel uyarısı (görselden, 2099569262847230211): "performans sıralamasıdır; “alınacak fonlar” listesi değildir".
- Tansu'nun vurgusu: "#THF burada da ders vermiş" (2096661898385113202).
- Belirsiz: Alıntılanan 2096644397110534476 metni "20 günlük getirilere" der; PPF görselleri "1 Ay" gösterir. 6 Eylül HSF tablosunun getiri/risk penceresi görünür bölümde yok; PPF'nin 1A penceresi ona taşınmaz.
- YORUM: R032 sektör sıralamasıdır; fon sıralaması ayrı yöntemdir. 154 bütün PPF sayısı değil, 1A getirisi bulunan fon sayısıdır. Fon birden fazla sınıf etiketi taşıyabilir.

### X030 · 2024-10-13 07:42:13 UTC · WaveTrend ayarı ve aşırı satım taraması
- Bağlı: R255; Öneri: tema-1 #30
- Yazar: T + G (WaveTrend panelleri ve sinyal listesi).
- Kaynak: 1845369437441933344 (2024-10-13 07:42:13 UTC), 1848426907441692797 (2024-10-21 18:11:31 UTC).
- Fikirler:
  - [teyit-tetik] "Dalga osilatörü taramasına göre son gün aşırı satım bölgesinde al veren BIST30 hisselerİ" — WT(10,21), WT_1/WT_2, görsel −50/−60 bandı; tam al formülü yok — çekirdek belli.
  - [teyit-tetik] "bunu birşeyler le kombinlemek lazım, bilemedim." — birleşim ihtiyacı; diğer unsur ve koşul yok — yalnız fikir.
- Örnek ve sonuç: 13 Ekim TAVHL/TOASO metni; 21 Ekim ALGYO görseli ve BIST30 başlıklı sinyal listesi. Sonraki kazanç yok.
- Tansu'nun vurgusu: "Gerisi detay teknikçilere kalmış."
- Belirsiz: 21 Ekim listesinin BIST30 başlığı, bütün sembollerin bu evrene ait olduğunu tek başına kanıtlamaz.
- YORUM: WT ayarı al-sinyali formülünü tamamlamaz; tek başına yeterli olduğu iddiası kurulmadı.

### X031 · 2024-09-30 18:10:01 UTC · Son kapanışta RoC9 sıfır yukarı kesişi
- Bağlı: R105; Öneri: tema-1 #31
- Yazar: T + G (tarama çıktısı ve DEVA grafiği).
- Kaynak: 1840816385540440325 (2024-09-30 18:10:01 UTC), 1840826561273979333 (2024-09-30 18:50:27 UTC).
- Fikirler:
  - [teyit-tetik; G] "0 eksenini yukarı kestiği hisseler:" — görselin tam satırı son kapanış günü ve RoC9'u belirtir; sıfır yukarı kesişimi — kural tam.
- Örnek ve sonuç: DEVA listede; grafikte RoC9/20/50 ve son noktada Kesişim işareti. Sonraki getiri yok.
- Tansu'nun vurgusu: "İşine yarayan kullansın"
- YORUM: R105 eğim dönüşüyle sıfır kesişi aynı koşul değildir; ayrı tetik varyantı.

### X032 · 2024-08-23 20:20:44 UTC · Fiyatın EMA200 kesişimi ve endeks uyarısı
- Bağlı: R212 / R131; Öneri: tema-1 #32
- Yazar: T + G (fiyat/EMA grafikleri).
- Kaynak: 1827078541797945391 (2024-08-23 20:20:44 UTC), 1844068170853949930 (2024-10-09 17:31:27 UTC), 1844080751714967953 (2024-10-09 18:21:27 UTC).
- Fikirler:
  - [giriş] "Yanlış anlaşılmasın, fiyatın EMA200'ü yukarı kestiği." — son gün fiyat EMA200'ü yukarı keser; kesen EMA50 değildir — kural tam.
  - [rejim] "200 günlük EMA altında olan endekste bizi iyi öperler." — endeks EMA200 altı olumsuz değerlendirme; kesin işlem yasağı yok — yalnız fikir.
- Örnek ve sonuç: 9 Ekim listesinde AEFES/DURDO/INVEO/IZFAS/KGYO/KRONT/NETAS/ORMA/OZSUB/TCELL/TDGYO. Görselde TDGYO fiyat 10.79, EMA50 10.28, EMA200 10.52; sonraki getiri yok.
- Tansu'nun vurgusu: "Golden cross>'dan bahsetmiyorum"
- Belirsiz: 1827078541797945391 "Izdırap endeksi"ni tanımlamaz; görselde EMA(200) çizgisi son değerde okunamaz (Ağustos başında biter).
- YORUM: Fiyat kesişimi Golden Cross değildir; X018'deki iki EMA kesişiminden ayrı tutuldu.

### X033 · 2025-07-03 07:14:31 UTC · Thompson Sampling günlük hisse önerisi fikri
- Bağlı: yeni yöntem; Öneri: tema-1 #33
- Yazar: M (genel Bayesian açıklama).
- Kaynak: 1940670472590372957 (2025-07-03 07:14:31 UTC).
- Fikirler:
  - [momentum-seçim; M] "Ardından her gün, her hisse için bu dağılımdan rastgele bir değer çekilir. En yüksek değeri çeken hisse o gün için önerilen hisse olur." — geçmiş ortalama getiri/oynaklıktan dağılım; günlük çekiş ve en yüksek çekişi seçme — çekirdek belli.
- Örnek ve sonuç: Kod, araç çıktısı veya kişisel uygulama yok. Veri geldikçe dağılımların güncellenmesi anlatılır; formülü ve geçmiş pencere yok.
- Tansu'nun vurgusu: "bu sistemi mutlaka araştırmanızı tavsiye ederim."
- YORUM: Normal dağılım "genellikle" denir; zorunlu dağılım değildir. Tavsiye, Tansu'nun uyguladığı sistemi kanıtlamaz; M fikir olarak alındı.

### X034 · 2024-10-20 13:49:38 UTC · Ichimoku dört koşul denemesi
- Bağlı: yeni yöntem; Öneri: tema-1 #34
- Yazar: T (doğruluğu sorulan tarama).
- Kaynak: 1847998614548721928 (2024-10-20 13:49:38 UTC).
- Fikirler:
  - [momentum-seçim] "Tenkan-sen > Kijun-sen"; "Senkou Span A > Senkou Span B" — ilk iki koşul; periyotlar yok — çekirdek belli.
  - [momentum-seçim] "Kapanış Fiyatı (Close) > Senkou Span A:"; "Chikou Span > Close ((Gecikmeli Çizgi Kapanış Fiyatının Üstünde)" — diğer iki koşul; Chikou zaman hizası yok — çekirdek belli.
- Örnek ve sonuç: "Hisse çıkarmadı, enteresan." Evren/çıktı yok; tarama boş.
- Tansu'nun vurgusu: "aşağıdaki koşulları taradım. Doğru mudur?"
- YORUM: Kesinleşmiş yöntem değildir; soru biçimi ve eksik periyotlar korundu.

### X035 · 2025-02-16 19:28:54 UTC · Döneme göre değişen haftanın günü etkisi
- Bağlı: R183; Öneri: tema-1 #35
- Yazar: T + G (üst gönderinin görseli); kendi metnini alıntıladığı için A değil.
- Kaynak: 1891208151497613761 (2025-02-16 19:28:54 UTC), 1891539591531823394 (2025-02-17 17:25:56 UTC), 1891948299474616579 (2025-02-18 20:29:59 UTC).
- Fikirler:
  - [rejim] "Endeksin ralli yaptığı dönemde haftanın kötü getirisi salı günü idi, işleme girmezdik, o gün şimdi pazartesi." — döneme göre salı→pazartesi; ölçüm penceresi yok — yalnız fikir.
  - [rejim] "İstatistiksel olarak çarşamba günleri endeks için keyifli bir işlem günü değil" — sonraki ayrı çarşamba uyarısı; dönem/sayı yok — yalnız fikir.
- Örnek ve sonuç: 1891539591531823394 pazartesileri riskli der; 1891948299474616579 çarşambayı uyarır; ikisi 1891208151497613761 salı→pazartesi sözünü alıntılar. Üst görsel XU100 Average Daily Returns by Weekday (Last 1 Year) başlığını taşır: pazartesi ve çarşamba negatif, salı sıfıra yakın, perşembe en yüksek, cuma pozitif görünür. Kesin sayılar etiketlenmemiştir.
- Tansu'nun vurgusu: "Pazartesiler riskli diyorum"
- Belirsiz: Görsel son bir yılı belirtir; kesin başlangıç/bitiş, günlük getiri hesabı ve ralli dönemi karşılaştırmasının penceresi yok. Sonraki çarşamba uyarısının ayrı ölçümü gösterilmez.
- YORUM: Kalıcı kötü-gün takvimi kurulmaz; görselin bir yıllık başlığı metindeki dönem değişimini tek başına ölçmez.

### X036 · 2025-10-29 10:25:09 UTC · Derinlik–fiyat ölçümü: ilişki çok zayıf
- Bağlı: R225; Öneri: tema-1 #36 yerine ölçüm kaydı
- Çelişir: R225
- Yazar: T (kendi çalışmasını anlatan giriş ve ölçüm); uzun açıklamanın biçimi, ölçümün bağımsız doğruluğunu kanıtlamaz.
- Kaynak: 1983480217894060348 (2025-10-29 10:25:09 UTC).
- Fikirler:
  - [ölçüm-ilkesi] "EN ÖNEMLİ BULGU: İLİŞKİ ÇOK ZAYIF!" — satış lot toplamı/fiyat değişimi r=−0.136; alış lot toplamı/fiyat değişimi r=−0.031; birinci seviye alış emirleri r=0.241 — çekirdek belli (kaynak ölçümü).
  - [ölçüm-ilkesi] "Sadece derinlik verileri ile değil kademe analizinin de iyi okunabilmesi karşı işlemlerin anahtarıdır." — derinliğin tek başına yön tahmini için yetmediği vurgusu; kademe yönteminin parametreleri yok — yalnız fikir.
- Örnek ve sonuç: Metne göre 28/10/2025 derinlik verisi; alış lot>satış lot grubunda ortalama %0.06, satış lot>alış lot grubunda %0.53 fiyat değişimi. Satış baskısı grubu daha iyi performans göstermiş. Örnek sayısı, fiyat değişiminin zaman aralığı ve test ayrıntıları yok; yeniden hesaplanmadı.
- Tansu'nun vurgusu: "Alış lotlarının büyüklüğü fiyat artışını tahmin etmede neredeyse işe yaramıyor"
- Belirsiz: Arşiv kaydının media alanı boş; medya klasöründe bu id'ye bağlı görsel yok. Sayılar yalnız gönderi metninden doğrulanabildi; görselle ikinci doğrulama yapılamadı.
- YORUM: Öneri 36'daki 1983491105631993940 alınmadı; Tansu'nun kendi ölçümü, yüksek derinlik alış/satış oranından yön kuralı çıkarmayı çürütür. O gönderinin −X.YZ% ifadesi gerçek yüzde değil yer tutucudur; 59.2x için derinlik hesabı da açık değildir. Sahte emir/psikolojik oyun açıklamaları olası sebeplerdir, doğrulanmış nedenler değildir.

### X037 · 2025-04-23 21:57:33 UTC · Uyumsuzluk, mum ve momentum birleşik taraması
- Bağlı: R214 / R167 / R116; Öneri: tema-1 #37
- Yazar: T + G (RSI uyumsuzluğu ve mum etiketli grafikler).
- Kaynak: 1915163157531910187 (2025-04-23 21:57:33 UTC).
- Fikirler:
  - [teyit-tetik] "Pozitif uyumsuzluk marubozu mum alternatif momentum son gün breakout ema5-8-13-34 sıralaması." — birlikte anılan unsurlar; görselde RSI uyumsuzluğu; breakout/alternatif momentum/birleşim tanımları yok — çekirdek belli.
- Örnek ve sonuç: İlk görsel Pozitif Uyumsuzluk ve CDLMATCHINGLOW; ikinci görsel kapanış marubozu etiketi. Semboller görünmüyor. Metin DOKTA ile önceki taramada tavan aldığını söyler; tarih/sayısal getiri yok.
- Tansu'nun vurgusu: "mis gibi. en son böyle tarama sonucunda dokta ile tavan almıştık:)"
- Belirsiz: Metin EMA5/8/13/34 sıralaması, ilk görsel lejantı EMA5/8/5/21. Metinde > yönü yazılı değil; EMA5>8>13>34 kuralı doğrulanmıyor.
- YORUM: R116 gizli pozitif uyumsuzluk; burada aynı tür olduğu yazılı değildir. Alternatif momentum unsuru korunmuştur.

### X038 · 2025-07-20 15:00:57 UTC · Kısa vadeli kazananların soğuması fikri
- Bağlı: yeni yöntem; Öneri: tema-1 #38
- Yazar: M (genel açıklama; kısa ek T biçimindedir).
- Kaynak: 1946948449275928807 (2025-07-20 15:00:57 UTC).
- Fikirler:
  - [momentum-seçim; M] "bir hafta ya da bir ay içinde çok yükselen hisseler, sonraki dönemlerde ortalamanın altında performans sergileyebiliyor." — kısa vadeli reversal fikri; çok yükselme eşiği/sonraki dönem yok — yalnız fikir.
  - [temel-değerleme; M] "getirisi düşük ama temeli sağlam olan hisseleri izlemek daha mantıklı olabilir." — temel gücüyle birlikte izleme önerisi; eşikler yok — yalnız fikir.
- Örnek ve sonuç: Akademik çalışmalar anılır fakat çalışma kimliği, veri veya uygulama örneği yok.
- Tansu'nun vurgusu: "Winners loosers konusu."
- YORUM: Üst gönderi 1946946856199610482 KTanidik kullanıcısınındır; onun 2 hafta/1 ay/3 ay pencereleri Tansu'ya aktarılmadı. Tansu'nun uygulanmış seçim kuralı olduğu gösterilmez.

### X039 · 2025-05-23 04:52:28 UTC · Vasicek faiz senaryosu ve iskonto fikri
- Bağlı: yeni yöntem; Öneri: tema-1 #39
- Yazar: T giriş + M açıklama gövdesi + G (faiz patikaları).
- Kaynak: 1925776822249144708 (2025-05-23 04:52:28 UTC).
- Fikirler:
  - [rejim] "Vaiseck fiyatlama modelini neden kullanıyoruz hiç düşündünüz mü?" — T girişinde model kullanımına gönderme; tam kural yok — yalnız fikir.
  - [rejim; M] "Başlangıçta %50 civarında (r₀ = 0.50)"; "Zaman içinde ortalama %30’a (θ = 0.30) geri dönme eğiliminde (mean-reversion)" — bir yıllık simülasyon anlatısı; κ/σ yok — çekirdek belli.
  - [temel-değerleme; M] "Vasicek modeli ile risk-free rate (faiz oranı) için dinamik bir tahmin elde edilir." — DCF iskonto girdisi, WACC, sektör faiz duyarlılığı ve defansif konumlama açıklamaları — yalnız fikir.
- Örnek ve sonuç: Görsel Vasicek başlığı, yaklaşık 0.50 başlangıcı ve 0–1 yıl ekseni gösterir; θ yazmaz. Gerçekleşmiş faiz/DCF değeri/işlem sonucu yok.
- Tansu'nun vurgusu: "neden kullanıyoruz hiç düşündünüz mü?"
- YORUM: θ=0.30, iskonto ve sektör önerileri M gövdesi olarak alındı; Tansu'nun kendi kod parametresi veya gerçekleşmiş uygulaması olarak sunulmadı.

### X040 · 2025-11-22 11:09:25 UTC · Japonya likiditesi ve Altın/Gümüş rasyosu fikri
- Bağlı: yeni yöntem; Öneri: tema-1 #40
- Yazar: T (beyin fırtınası girişi) + M (senaryo gövdesi).
- Kaynak: 1992188666593112507 (2025-11-22 11:09:25 UTC).
- Fikirler:
  - [rejim; M] "Altın fiyatı / Gümüş fiyatı oranı hızla artar (Örneğin 80 seviyesinden 90 veya 100 seviyesine çıkar)." — Japonya likidite sıkışması/carry trade çözülmesi → satış → gümüşün altına göre zayıflığı → rasyo artışı senaryosu; 80/90/100 örnek — yalnız fikir.
  - [portföy; M] "Yatırımcılar bu dönemlerde gümüşten çıkıp altına veya nakde (Dolar/Yen) geçme eğiliminde olurlar." — anlatılan yatırımcı davranışı; Tansu'nun işlem talimatı değil — yalnız fikir.
- Örnek ve sonuç: Varsayımsal mekanizma; gerçekleşmiş rasyo/işlem sonucu veya karşılaştırmalı veri yok.
- Tansu'nun vurgusu: "Biraz beyin fırtınası yapalım mı"
- YORUM: Senaryo fikir olarak alınır; BoJ haberleri burada ayrıca güncel gerçek diye doğrulanmadı. 80→90/100 giriş eşiği değildir.

### X041 · 2026-08-02 16:30:16 UTC · Stagflasyon, faiz indirimleri ve altın
- Bağlı: R071; Öneri: tema-1 #41
- Yazar: T (kısa makro görüş).
- Kaynak: 2083953538661539956 (2026-08-02 16:30:16 UTC; yanıt), üst: 2083953536287576230 (2026-08-02 16:30:15 UTC; BIS/NYMEX faiz indirimi–altın grafiği).
- Fikirler:
  - [rejim] "Stagflasyon ve senkronize faiz indirim döngüleri, altın için makroekonomik açıdan en ideal yükseliş ortamını hazırlar." — stagflasyon + senkronize faiz indirimleri bağlamı — yalnız fikir.
  - [rejim] "Enflasyonun yüksek kaldığı stagflasyonist ortmda ise "reel faiz" (Nominal Faiz - Enflasyon) negatfe kayr" — reel faiz tanımı nominal faiz−enflasyon; ülke/seri/vade/eşik yok — yalnız fikir.
- Örnek ve sonuç: Sayısal örnek veya gerçekleşmiş altın getirisi yok.
- Tansu'nun vurgusu: "en ideal yükseliş ortamını hazırlar."
- Belirsiz: yanıt metni "negatfe kayr" ile kesik. Üst gönderi koşulludur: "Eğer beklenti anketine pareler olarak faizler 375/400 bandına çıkar ise ... Burada not olarak kalsın bu..."
- YORUM: Bağlam yalnız negatif reel faize indirgenmedi; ölçülebilir giriş/çıkış kuralı yok.

### X042 · 2025-07-14 21:16:31 UTC · ANP ile bağımlı karar kriterleri fikri
- Bağlı: R179 / R145; Öneri: tema-1 #42
- Yazar: T giriş + M (ANP açıklaması).
- Kaynak: 1944868638307311952 (2025-07-14 21:16:31 UTC).
- Fikirler:
  - [ölçüm-ilkesi; M] "ANP ise bu bağımlılıkları ve geri beslemeleri dikkate alır." — kriter/alternatif ağını ve etkileşimlerini modelleme — çekirdek belli.
  - [momentum-seçim; M] "Süpermatris çözümlenerek nihai öncelik sıralaması elde edilir. En uygun alternatif, en yüksek önceliğe sahip olan olur." — amaç → kriterler → alternatifler → etkileşim ağı → ikili karşılaştırmalar → ağırlıklı süpermatris → öncelik sentezi; sayısal uygulama yok — çekirdek belli.
- Örnek ve sonuç: Üç hisse varsayımı; kârlılık, borçluluk, fiyat oynaklığı ve sektör büyümesi örnek kriterler. Ağırlık/matris/çıktı yok.
- Tansu'nun vurgusu: "Bu bilgiyi hiç bir yerde bulamazsınız. Bilenler de paylaşmaz."
- YORUM: Kaynak ANP'yi AHP ile karşılaştırır; "TOPSIS yerine" demez. R145 tercihi değişmiş veya Tansu ANP uygulamış sonucu çıkarılmadı.

### X043 · 2024-09-22 14:51:46 UTC · BIST30 MACD pozitif uyumsuzluk örneği
- Bağlı: R116; Öneri: tema-1 #43
- Yazar: T + G (ISCTR fiyat/MACD grafiği ve çizim kodu).
- Kaynak: 1837867391310540998 (2024-09-22 14:51:46 UTC).
- Fikirler:
  - [teyit-tetik] "Pozitif yuyumsuzluk taramasında, BIST30'da taramaya takılan hisselerden birisi #ISCTR" — evren BIST30; MACD adı metinde değil görsel/kodda; MACD ayarları ve dip tespiti yok — çekirdek belli.
- Örnek ve sonuç: Görselde ISCTR fiyatındaki alçalan dipler ile MACD yükselen dip yönü kırmızı oklarla gösterilir; klasik pozitif uyumsuzluk. Görselin çizim kodu price ve MACD sütunlarını kullanır. Sonraki getiri yok.
- Tansu'nun vurgusu: "Haydi hayırlısı"
- YORUM: R116 gizli pozitif uyumsuzluğu değiştirmez; klasik örnek ayrı tutuldu.

### X044 · 2024-11-28 08:45:03 UTC · Günlük momentum breakout çalışması
- Bağlı: R004 ("Düşeni kıran" tarama fikri) / R124; Öneri: tema-1 #44 (yalnız momentum breakout)
- Yazar: T.
- Kaynak: 1862055089713602762 (2024-11-28 08:45:03 UTC).
- Fikirler:
  - [teyit-tetik] "momentum breakout çok daha önce yakaladığı için yazmadım." — o gün anılan hisselerde düşeni kıran sistemden önce yakalama iddiası; formül/pencere/zaman karşılaştırması yok — yalnız fikir.
  - [ölçüm-ilkesi] "Her gün momentum breakout çalışması yapmak lazım." — günlük çalışma önerisi — yalnız fikir.
- Örnek ve sonuç: O anda %4–%5 yapmış hisseler anılır; sembol ve sinyal tarihleri yok. Evrensel erken sinyal veya doğrulanabilir performans karşılaştırması yok.
- Tansu'nun vurgusu: "Her gün momentum breakout çalışması yapmak lazım."
- YORUM: 1914692264384774310 kelebek etkisi açıklaması M ve R077 tekrarı olduğundan alınmadı. R034 rolling eşbütünleşmesini genel korelasyon kırılması fikrine dönüştüren bağ kurulmadı.

### X045 · 2024-12-09 21:45:18 UTC · Gaplı seans sonrası temkin
- Bağlı: yeni yöntem; Öneri: tema-1 #45
- Yazar: T.
- Kaynak: 1866237714728645031 (2024-12-09 21:45:18 UTC).
- Fikirler:
  - [rejim] "Bugün çok gaplı işlemler oldu." — o seans gözlemi; gap sayısı/büyüklüğü yok — yalnız fikir.
  - [giriş] "Açılışı görelim. Acele işlemler yapmayın." — ertesi seans açılışını görme ve acele etmeme öğüdü — yalnız fikir.
  - [rejim] "En basitinden mutlaka ortalamasına geri döner." — ortalama türü ve pencere yok — yalnız fikir.
- Örnek ve sonuç: 9 Aralık sonrası seans için uyarı; ertesi gün gerçekleşen sonuç yok.
- Tansu'nun vurgusu: "Yarın temkinli olalım lütfen."
- YORUM: "Açılışı görmeden işlem yapma" kesin yasağına çevrilmedi. Gap filtresi veya açılış sonrası giriş kuralı verilmez.

### X046 · 2025-11-25 22:20:17 UTC · Momentum lookback tasarım örnekleri
- Bağlı: R022; Öneri: tema-1 #46
- Yazar: T.
- Kaynak: 1993444658085826808 (2025-11-25 22:20:17 UTC).
- Fikirler:
  - [momentum-seçim] "örneğin momentum için 10 günlük lookback isteyebilirsiniz kimisi 20 gün ister kimisi 5 gün ister." — 10/20/5 gün tasarım örnekleri; kendi lookback değeri açıklanmıyor — yalnız fikir.
- Örnek ve sonuç: Uygulama veya sayısal sonuç yok.
- Tansu'nun vurgusu: "benimde kendime göre rakamlarım var."
- Belirsiz: Yanıt verilen 1993444031293276418 için doğrulama raporunda 404 kaydı var; eksik kullanıcı mesajı tamamlanmadı.
- YORUM: Lookback ile R022 çeyreklik portföy yenilemesi farklı parametrelerdir; bu gönderi R022'nin penceresini tamamlamaz.

## Tema 1 özeti

| X no | başlık | bağlı R | olgunluk (en güçlü fikir) | yazar |
|---|---|---|---|---|
| X001 | EMA üstü kapanış ve RSI seviyesi | yeni yöntem | kural tam | T + G |
| X002 | CMF üç pozitif / üç negatif | R137 | kural tam | T + G |
| X003 | NH−NL eşikleri | R118 | kural tam | T + M + G |
| X004 | AKD ve iki skor şeması | yeni yöntem | çekirdek belli | T + M + G |
| X005 | VIX bant ve rapor varyantları | R210 / R188 | kural tam | T + M + G |
| X006 | Fund X-Ray birikimi | yeni yöntem | çekirdek belli | T + M + G |
| X007 | Sektör ve negatif VRP | R031 | çekirdek belli | T + G |
| X008 | Üç sektör / 90 gün | R032 | çekirdek belli | M + T + G |
| X009 | TEFAS sınıf akışı | yeni yöntem | çekirdek belli | T + M + G |
| X010 | Vegas EMA varyantları | yeni yöntem | kural tam | T + G |
| X011 | EMA/MACD/RSI/OBV | R196 / R230 | kural tam | T + G |
| X012 | ADX/BBW yatay filtre | yeni yöntem | çekirdek belli | M |
| X013 | Bileşik momentum | R120 | çekirdek belli | M + G |
| X014 | Ay etkisi anlamlılığı | R183 | çekirdek belli | T + M + G |
| X015 | Varyans kesişimi | R028 / R029 | çekirdek belli | T + G |
| X016 | Faz ve kayan performans | R202 / R200 | çekirdek belli | T + M + G |
| X017 | İki kod / 0.50 sinyal | R137 | çekirdek belli | T + M + G |
| X018 | Hisse Golden Cross | yeni yöntem | kural tam | T + G |
| X019 | GARCH risk/getiri | R097 | çekirdek belli | M |
| X020 | Sharpe sıralaması | R110 | çekirdek belli | M |
| X021 | Büyüme ve altın | yeni yöntem | çekirdek belli | M + T + G |
| X022 | ALARK eğim × R² | R176 | çekirdek belli | T + G |
| X023 | Convex Hull seçim sırası | R178 / R002 | çekirdek belli | T + M + G |
| X024 | Supertrend/MOST/KAMA | R148 | çekirdek belli | T + G |
| X025 | Takas kalıcılığı | yeni yöntem | yalnız fikir | M + T |
| X026 | Temel/teknik/takas | R166 | çekirdek belli | T |
| X027 | Fon yatırımcı sayısı | yeni yöntem | yalnız fikir | T + M + G |
| X028 | Manipülasyon işaretleri | yeni yöntem | yalnız fikir | T + M |
| X029 | Fon getiri/risk sıralaması | yeni yöntem | kural tam | T + G |
| X030 | WaveTrend | R255 | çekirdek belli | T + G |
| X031 | RoC9 sıfır kesişimi | R105 | kural tam | T + G |
| X032 | Fiyat EMA200 kesişimi | R212 / R131 | kural tam | T + G |
| X033 | Thompson Sampling | yeni yöntem | çekirdek belli | M |
| X034 | Ichimoku denemesi | yeni yöntem | çekirdek belli | T |
| X035 | Haftanın günü etkisi | R183 | yalnız fikir | T + G |
| X036 | Derinlik–fiyat ölçümü | R225 (çelişir) | çekirdek belli | T |
| X037 | Birleşik tarama | R214 / R167 / R116 | çekirdek belli | T + G |
| X038 | Kısa vadeli reversal | yeni yöntem | yalnız fikir | M |
| X039 | Vasicek faiz senaryosu | yeni yöntem | çekirdek belli | T + M + G |
| X040 | Japonya ve altın/gümüş | yeni yöntem | yalnız fikir | T + M |
| X041 | Stagflasyon ve altın | R071 | yalnız fikir | T |
| X042 | ANP | R179 / R145 | çekirdek belli | T + M |
| X043 | MACD uyumsuzluğu | R116 | çekirdek belli | T + G |
| X044 | Momentum breakout | R004 / R124 | yalnız fikir | T |
| X045 | Gap sonrası temkin | yeni yöntem | yalnız fikir | T |
| X046 | Lookback örnekleri | R022 | yalnız fikir | T |
