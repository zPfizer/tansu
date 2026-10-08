# Defter 5: X arşivi ekleri (X001–X046, X201–X629)

Kaynak: Tansu'nun X arşivi (`x-arsiv/tweets.jsonl`, görseller `x-arsiv/medya/`). Öneriler: `x-arsiv/siniflama/defter-karsilastirma/tema-*.md` 5. bölüm. Her öneri iki model tarafından ayrı bağlamda kaynağa karşı doğrulandı (Codex, Claude); bu dosya birleştirmedir (08.10.2026). Numara: X0xx tema-1, X2xx tema-2, X3xx tema-3, X4xx tema-4, X5xx tema-5a, X6xx tema-5b. Tema-1'de iki model ayrı doğruladı, Codex yazdı, iki Claude denetledi; tema-2…5b'de Codex doğrulayıp yazdı, her temayı ayrı bir Claude denetledi, ayrışmalar görsel açılarak çözüldü (08.10.2026). R kayıtları (defter-1…4) değişmez; X kayıtları "Bağlı" satırıyla R'ye bağlanır. Olgunluk etiketleri: kural tam / çekirdek belli / yalnız fikir. Yazar: T = Tansu, M = LLM biçimli (Tansu hesabında), A = alıntı, G = görsel.

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
- Kaynak: 1846310706263871703 (2024-10-15 22:02:29 UTC), 1848806602553385447 (2024-10-22 19:20:17 UTC), 1851719680052072481 (2024-10-30 20:15:49 UTC), 1851720332580966708 (2024-10-30 20:18:25 UTC), 1852063288533881329 (2024-10-31 19:01:12 UTC), 1865470227720405267 (2024-12-07 18:55:35 UTC; yanıt).
- Fikirler:
  - [teyit-tetik] "CMF SON 3 gün pozitif, ondan önceki 3 gün ise negatif olsun (Hisseye para girişi olsun)" — altı günlük işaret dizisi; CMF hesap periyodu yok — çekirdek belli.
  - [teyit-tetik] "Ben CMF kullanıyorum. Genelde  6 gün bakıyorum." — altı günlük CMF işaret penceresi (son 3 pozitif, önceki 3 negatif) — çekirdek belli.
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

## Tema 2 — Bölge ve formasyon

### X201 · 2025-06-30 06:20:49 UTC · Günlük ve haftalık yatay kanal
- Bağlı: R246 / R082; Öneri: tema-2 #1
- Yazar: T (kısa uygulama notları) + M (30 Haziran açıklaması) + G (kanal çıktıları).
- Kaynak: 1939569795696922684 (2025-06-30 06:20:49 UTC), 1942198658486686133 (2025-07-07 12:26:59 UTC), 1943009441273487705 (2025-07-09 18:08:44 UTC), 1949048313266721141 (2025-07-26 10:05:04 UTC), 1949055258195378520 (2025-07-26 10:32:39 UTC), 1956028500407619964 (2025-08-14 16:21:50 UTC), 1962962557699871050 (2025-09-02 19:35:18 UTC), 1963314020007776602 (2025-09-03 18:51:53 UTC), 2045431237335036123 (2026-04-18 09:16:23 UTC), 2049157737360065010 (2026-04-28 16:04:10 UTC), 2096651255514821058 (2026-09-06 17:26:27 UTC).
- Fikirler:
  - [tarama-evren; M] "Son 2 ayda en az 7 en fazla 30 gün boyunca %10’dan fazla hareket etmeyen" — günlük konsolidasyon penceresi; %10 eşitliği metin bakımından dışlanmıyor — çekirdek belli.
  - [giriş/stop; M] "Kanalın yukarısı hacimle kırılırsa alım, aşağısı kırılırsa satım fırsatı doğabilir." — bant içinde büyük pozisyondan kaçınma, stop bandın hemen dışında; kademe derinliği ve takasla teyit — çekirdek belli.
  - [teyit-tetik; G] "YUKARI KIRILIM Teyitli (önceki hafta breakout, son hafta teyit)" — haftalık iki aşama; teyidin sayısal ölçütü yok — çekirdek belli.
- Örnek ve sonuç: görselden: AKMGY 30 gün, 183.30–200.00, %9.11; OFSYM 52 hafta, 33.94–43.92, %29.40; AYCES 34 hafta, 386.25–500.50, %29.58; CANTE 50 hafta; KRPLS 52 hafta, 6.34–8.06, %27.13; ARDYZ 27 hafta, 24.76–33.10, %33.68. COSMO 25 haftalık 101.00–112.60 kanal, kırılım 2025-07-21; SMA20W, VWAP ve hacim ortalaması20W. 65 haftalık örnekte U1–U4/L1–L4 temasları. Tansu ayrıca 104 ve 37 haftalık örnekler söyler. İşlem dökümü yok.
- Tansu'nun vurgusu: "gel desteğe de alalım amcamın oğlu:)"; "Haftalık ne güzel trade yaptırmış."
- Belirsiz: 2045431237335036123 metni 53 hafta der; görselin boyalı kanalı yaklaşık Şubat–Nisan 2026'dır. 53 haftalık tarihçe veya yanlış süre etiketi olmak üzere iki okuma var; 53 hafta görselle doğrulanmıyor. Haftalık yataylık toleransı verilmemiştir.
- YORUM: Çıktıların yüzde değişimi 100×(üst/alt−1) ile uyuşur; bu, görsel değerlerinden çıkarılan hesap ilişkisidir. Günlük formül de örnekle uyumludur, fakat kaynak kod görülmediğinden katı <%10 koşulu kural yapılmadı. M metnindeki "AKD" açılımı kademe derinliğidir; aracı kurum dağılımıyla aynı veri kabul edilmedi.

### X202 · 2026-08-18 17:45:11 UTC · Harmonik hedefler ve değişen stop konumu
- Bağlı: R203 / R222 / R014; Öneri: tema-2 #2
- Yazar: T + G (üç farklı harmonik araç grafiği).
- Kaynak: 2089770598620713304 (2026-08-18 17:45:11 UTC), 2090514210228740261 (2026-08-20 19:00:02 UTC), 2090515278199136740 (2026-08-20 19:04:16 UTC).
- Fikirler:
  - [hedef-çıkış; G] "TP3 (C): 70.00" — KUYAS'ta TP1/TP2/TP4, D+(C−D)×0.382/0.618/1.272 ile uyuşur; TP3=C — çekirdek belli.
  - [stop-geçersizlik; G] "STOP: 78.89" — CCOLA Derin Yengeç örneğinin stop'u demand kutusunun üst kenarında; DERIM kelebeğinde stop demand içinde ve D altında; hepsi X stop'u değildir — çekirdek belli.
- Örnek ve sonuç: görselden: KUYAS C=70.00, CD=−8.00, D=62.00; TP1 65.06, TP2 66.94, TP3 70.00, TP4 72.18, stop=X=60.50. CCOLA C=90.05, CD=−9.70, D=80.35; TP1 84.06, TP2 86.34, TP3 90.05, TP4 92.69, stop 78.89. DERIM C=39.50, CD=−4.62, D=34.88; TP1 36.64, TP2 37.74, TP3 39.50, TP4 40.76, stop 34.19. DERIM grafiğinde TP1 ve TP2 üstüne hareket görülür; bağımsız işlem sonucu yok.
- Tansu'nun vurgusu: "Ancak talep noktasından başlayan hareketin devamı için trenin kırılmasında fayda var. izlenmeli"
- Belirsiz: R203'te C−D, R014/R222'de A−D hedef tabanı bulunur. Ayrı araç/strateji varyantı veya tutarsız uygulama olabilir; tek hedef formülüne birleştirilmedi.
- YORUM: CCOLA'nın adı Crab değil Derin Yengeç. Hedef eşleşmeleri bu incelemede görsel değerlerinden hesaplandı. R014'ün SAYAS giriş/stop/TP2 kaydı zaten mevcut olduğundan yeniden kayıt yapılmadı.

### X203 · 2025-11-07 23:58:59 UTC · Fincan hedef tabanı ve retest kartı
- Bağlı: R114; Öneri: tema-2 #3
- Yazar: T (kısa setup/retest notları) + M (numaralı grafik açıklamaları) + G.
- Kaynak: 1986946515508543529 (2025-11-07 23:58:59 UTC), 1986961469393473699 (2025-11-08 00:58:24 UTC), 2047238753366761631 (2026-04-23 08:58:49 UTC), 2095610529330905560 (2026-09-03 20:30:59 UTC), 2095921661098836095 (2026-09-04 17:07:19 UTC).
- Fikirler:
  - [hedef-çıkış; G] "KIRILMA: 300.75"; "HEDEF: 389.30" — GUBRF hedefi kırılım+(kırılım−dip)=300.75+(300.75−212.20); sağ ağız 317.00 hedef hesabının tabanı değildir — çekirdek belli.
  - [giriş; T] "Retest kaliteyi arttırır." — kırılım sonrası retest tercih edilir; retestin kabul mesafesi ve bekleme süresi verilmemiş — çekirdek belli.
  - [boyut-risk; G] "Kalite: 65.0/100" — kartta kalite, R/R, hacim çarpanı, kırılım/hedef/stop ve Fib %38.2/%50 alanları; skor formülü yok — yalnız fikir.
- Örnek ve sonuç: görselden: NTHOL kırılım 47.50, hedef 60.82; dip yaklaşık 34.18 sonucu bu iki seviyeden çıkar. İlk fincan örneğinde giriş 12.53, hedef 16.10, stop 10.41; hedef sonrası yükseliş gösterilir. ALARK RETESTTE, R/R 1:2.54, hacim 0.77x, kırılım 99.15, hedef 122.02, stop 91.13, Fib %38.2 90.41/%50 87.71. TRCAS TETİKLENDİ, kalite 63.5, R/R1:1.70, hacim1.29x, kırılım48.60, hedef56.03, stop45.18.
- Tansu'nun vurgusu: "İşte setup budur"; "Olayımız neydi? Retest kaliteyi arttırır."
- Belirsiz: ALARK'ta giriş=kırılım varsayılırsa R/R≈2.85; kart 2.54 der. Başka giriş referansı veya hesap farkı olabilir; giriş açık değildir. GUBRF sinyal tarihi 2025-10-24, başlıktaki tamamlanma tarihi 2025-10-28; iki ayrı araç tarihi veya etiket farkı olabilir.
- YORUM: R114'teki GUBRF anlatımı yinelenmedi; hedef tabanındaki eksik çözüm eklendi. NTHOL'un 34.18 dibi birebir yazılı etiket olarak sunulmadı.

### X204 · 2025-03-28 12:06:42 UTC · Altı mum formasyonunun koşulları
- Bağlı: yeni yöntem (R023 / R143 ile aynı kodlama ailesi); Öneri: tema-2 #4
- Yazar: T (kısa formasyon anlatımı/kod paylaşımı) + G (kod) + M (21 Nisan Tasuki açıklaması).
- Kaynak: 1905592381618962842 (2025-03-28 12:06:42 UTC), 1905940770281910507 (2025-03-29 11:11:04 UTC), 1905945897105531327 ve 1905945899810910520 (2025-03-29 11:31:27 UTC), 1905953843331940372 (2025-03-29 12:03:01 UTC), 1905953875007357298 (2025-03-29 12:03:09 UTC), 1905960716571451830 (2025-03-29 12:30:20 UTC), 1905960719561986200 (2025-03-29 12:30:21 UTC), 1906298040333308407 (2025-03-30 10:50:44 UTC), 1906298044510879769 (2025-03-30 10:50:45 UTC), 1906298048017264857 (2025-03-30 10:50:46 UTC), 1906299112422551926 (2025-03-30 10:55:00 UTC), 1906299132194476185 (2025-03-30 10:55:05 UTC), 1914394674921722043 (2025-04-21 19:03:52 UTC), 1919053643946303495 (2025-05-04 15:36:57 UTC).
- Fikirler (kod koşulları O=açılış, C=kapanış, H=tepe, L=dip ile yazıldı; eşitsizlikler korunmuştur):
  - [formasyon; G] Tasuki: `C[i]<O[i] and C[i]<O[i-1] and C[i]>C[i-2] and C[i-1]>O[i-1] and O[i-1]>C[i-2] and C[i-2]>O[i-2]` — iki yeşil, yukarı gap, üçüncü kırmızı kapanış gap içinde kalır — kural tam (tespit koşulu).
  - [formasyon; G] Shrinking ayı: `C[i-4]>O[i-4] and C[i]<O[i] and C[i]<L[i-3]`; `abs(C[i-3]-O[i-3])<abs(C[i-4]-O[i-4])`, sonra i−2/i−3 ve i−1/i−2 aynı katı küçülme; `L[i-1]>L[i-2] and L[i-2]>L[i-3]` — aynı gün `sell=-1` — kural tam (tespit koşulu). Boğa metni ilk mum ayı, sonraki üç gövde küçülür, beşinci boğa ikinci mumun tepesini aşar der — çekirdek belli.
  - [formasyon; G] Quintuplets: j=i,i−1,i−2,i−3,i−4 için `C[j]>O[j] and C[j]>C[j-1] and C[j]-O[j]<body`; `buy[i]==0` ise `buy[i]=1` — en eski mum da kendisinden önceki kapanışı aşmalı; ayıda `C[j]<O[j]`, `C[j]<C[j-1]`, `O[j]-C[j]<body`, `sell[i]==0` ve `sell[i]=-1` — çekirdek belli.
  - [formasyon; T] "alt fitili olmamalı, yani mum en düşük seviyeden açılmış olmalı" — Bottle: C1>O1, C2>O2, O2=L2, H2>C2, O2<C1 — çekirdek belli.
  - [formasyon; T] "Bu mumun açılış ve kapanış fiyatı eşittir (doji benzeri)." — H: C1>O1, O2=C2, C3>O3, C3>C2, L3>L2 — çekirdek belli.
  - [formasyon; T] "son mumu ilk mumun tepe seviyesine eşit veya daha aşağıda bir dip yapmalı" — Slingshot: ilk mum boğa, C2>C1; ardından iki mum, sonuncusu öncekinin tepesini geçmez; son mum L≤H1 ve C>H2; ikinci/üçüncü mum rengi serbest — çekirdek belli.
- Örnek ve sonuç: görselden: Bottle ECILC, H THYAO; kodlarda aynı gün sinyal etiketi bulunur. Tasuki açıklaması sonrasında yükseliş olduğunu söyler; ölçülmüş getiri ve işlem dökümü yok.
- Tansu'nun vurgusu: "Bullish Tasuki kodlayalım..."; "Kodu yazıldı taraması hazır:)"
- Belirsiz: Quintuplets `body` değeri yok. Mart kodu aynı gün sinyal, Mayıs metni "bir sonraki gün alım (buy)  yaz." der; sinyal/işlem ayrımı veya sürüm değişimi olabilir. Tasuki kod yorumu açılış der fakat C[i]<O[i−1] kapanışı denetler; üçüncü açılış için koşul yok. 21 Nisan M metnindeki "gap’in içine girmez" ifadesi kodun gap içine kapanışından farklıdır. Slingshot'ta ayrı son mum eklenip eklenmediği ve "tepesini geçmez" koşulunun high/kapanış karşılığı açık değildir.
- YORUM: Sadece tespit koşulları tamdır; tüm aile için giriş/çıkış/stop sistemi kurulmuş sayılmaz. Eksik eşikler tamamlanmadı.

### X205 · 2024-12-22 00:28:39 UTC · Eski harmonik kartlarının okunması
- Bağlı: R008 / R075 / R222 / R203; Öneri: tema-2 #5 ve #27 harmonik alt maddesi
- Yazar: T + G (eski tarayıcı kartları).
- Kaynak: 1870627477254721649 (2024-12-22 00:28:39 UTC), 1871623972544274600 (2024-12-24 18:28:22 UTC), 1883641498564264218 (2025-01-26 22:21:44 UTC), 1888626133933121609 (2025-02-09 16:28:53 UTC), 1892643772430766103 (2025-02-20 18:33:33 UTC), 1899198147823366265 (2025-03-10 20:38:18 UTC), 2090515278199136740 (2026-08-20 19:04:16 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "Pattern completed on: 2025-03-07 00:00:00" — MACKO formasyon tarihi gönderi tarihinden ayrıdır; XA/AB/BC/CD sayıları bacak fiyat farklarıdır — çekirdek belli.
  - [bölge; G] "Fibo 0.618: 104.63"; "Fibo 0.786: 103.03" — MACKO çizgileri D−r×|CD| hesabıyla uyuşur; işlevi açıklanmamış — çekirdek belli.
- Örnek ve sonuç: görselden: MACKO Black_swan D=110.50, CD=−9.50; 110.50−0.618×9.50≈104.63, 0.786 çizgisi≈103.03; ikisi de X=105 altında. IHEVA D=2.48, CD=−0.32; 2.28/2.23. CEMTS CD=−0.42, Fibo8.65/8.58. TTKOM XA4.22, AB−2.50, BC1.80, CD−2.12; Fibo47.07/46.71; tamamlanma2025-02-17. ARENA XA6.18, AB−4.34, BC3.30, CD−5.20; tamamlanma2025-02-06. ALCAR XA93.50, AB−63.00, BC47.00, CD−68.50.
- Tansu'nun vurgusu: "Artık analizi sizden."; "Kod olayı güzel birşey ya."
- Çelişir: R222'nin M oran anlatımıyla ARENA AB/XA≈0.702, (A−D)/XA≈1.010; TTKOM D geri çekilmesi≈0.668; ALCAR≈0.674/0.904; KUYAS≈0.638/0.882 uyuşmaz. ARENA'da D−X=−0.06, R203'ün M geçersizlik anlatımıyla da uyuşmaz. Bunlar Tansu aracının gözlenen çıktılarıdır; kart adından standart oran doğruluğu çıkarılmaz.
- Belirsiz: Çizgiler D altındaki giriş adayları veya başka destek ölçümleri olabilir; ne giriş ne hedef olduğu kaynakta yazılıdır. Farklar eski tolerans/sürümden veya tarayıcı etiketleme hatasından doğabilir; 2026 KUYAS farkı yalnız tarihçe açıklamasını yeterli kılmaz.
- YORUM: Oranlar ve formül bu incelemede kart değerlerinden hesaplandı; Tansu'nun açık kural sözü gibi sunulmadı. #27'de aynı harmonik ayrışma ikinci kayıt yapılmadı.

### X206 · 2024-10-04 14:39:40 UTC · Bir yıllık kapanış Fibo ve EMA merdiveni
- Bağlı: R217; Öneri: tema-2 #6
- Yazar: T + G (paylaşılan kod); R217'nin dış slaytlarından ayrı uygulama.
- Kaynak: 1842212999169253445 (2024-10-04 14:39:40 UTC), 1844836756501471622 (2024-10-11 20:25:32 UTC), 1844837554795008098 (2024-10-11 20:28:43 UTC), 1847621973553144140 (2024-10-19 12:53:00 UTC), 1908510592639398132 (2025-04-05 13:22:38 UTC).
- Fikirler:
  - [bölge; G] `period='1y'`, `data['Close'].max()`, `data['Close'].min()` — kapanış max/min; seviye=max−r×(max−min); r=0.236/0.382/0.618/0.786; ayrıca 0=max, 1=min — kural tam (hesap).
  - [bölge; G] `ewm(span=window, adjust=False).mean()` — EMA10/20/50/100/200; 11 Ekim varyantı yalnız EMA200 — kural tam (hesap).
  - [pencere; T] "ben önce 1 yıllık ya da 2 yıllık bakıyorum sonra kısa vadeli mi pozisyon alacağım yoksa uzun vadeli mi ona göre fibo'yu belirttiğim tarihten çiziyorum"; "144 güzeldir." — vadeye göre başlangıç; yanıtın bağlamı bar sayısıdır, 144 zorunlu sabit değildir — çekirdek belli.
- Örnek ve sonuç: DOAS için metindeki geçiş merdiveni 215.57, 219.02, 230.22, 245.53, 249.66, 258.28, 281.74. Kod kapanış üzerinden çalışır; high/low üzerinden değildir. Sonraki işlem sonucu yok.
- Tansu'nun vurgusu: "Pardon 1 yıllık. başlığı değiştirmemişim"
- Belirsiz: 19 Ekim ilk blokta `fourth_level = max_value * difference * 0.618`, ikinci blokta doğru `max_value - 0.618 * difference` vardır. Yazım hatası veya iki ayrı blok kalıntısı olabilir; çarpma formülü düzeltildi. Aynı görselde ikinci blok 0.618'i `third_level` diye adlandırır; değişken isimleri birleşik kod gibi okunmadı.
- YORUM: Başlıktaki 6 ay yerine 1 yıl alındı; bu düzeltme Tansu'nun kendi yanıtıyla kesinleşir.

### X207 · 2026-08-16 08:37:14 UTC · Proximal çizgide renk ve gap
- Bağlı: R037; Öneri: tema-2 #7
- Yazar: T (kendi yanıtları).
- Kaynak: 2088907925704110444 (2026-08-16 08:37:14 UTC), 2088908047590502894 (2026-08-16 08:37:43 UTC).
- Fikirler:
  - [bölge] "Kural gereği proximal line, o base bölgesi içindeki en düşük gövde fiyatına çiziliyor." — R037 arz şemasında gövde tabanı=min(open,close); renk önemsiz — kural tam (çizgi konumu).
  - [bölge] "o zaman çizgiyi beyazdan değil siyahtan çekerdik." — gap sonrası siyah gövde daha aşağı kalırsa çizgi onun gövdesinden — kural tam.
- Örnek ve sonuç: eşit gövde dipli siyah/beyaz mum açıklaması; gerçek işlem sonucu yok. Takipçinin soru cümlesi kanıt yapılmadı.
- Tansu'nun vurgusu: "Yani  renge değil o bölgedeki en düşük gövde kapanışına ya da açılışına bakıyoruz."
- YORUM: R037'nin şema kuralını tekrar etmek yerine Tansu'nun renk/gap açıklaması eklendi; her demand bölgesine genellenmedi.

### X208 · 2024-02-27 09:00:27 UTC · Engulfing ölçümünün yönü ve rejection kodu
- Bağlı: R023 / R171; Öneri: tema-2 #8
- Yazar: T (ölçüm uyarısı) + G (kod ve çıktı) + M (15 Mayıs teyit listesi).
- Kaynak: 1762402303221346600 (2024-02-27 09:00:27 UTC), 1762402307503780152 (2024-02-27 09:00:28 UTC), 1923069231043838440 (2025-05-15 17:33:28 UTC).
- Fikirler:
  - [formasyon; G] Bearish engulfing: mevcut Open>önceki Close, mevcut Close<önceki Open, önceki Close>önceki Open — katı eşitsizlikler — kural tam (tespit).
  - [formasyon; G] Bullish rejection kodu: `O-L>abs(O-C)*5` ve `H-C<abs(O-C)/10`; bearish: `H-O>abs(O-C)*5` ve `C-L<abs(O-C)/10` — ilk koşul mum rengidir (bullish `Open<Close`, bearish `Open>Close`; görsel açıldı, 08.10) — kural tam (tespit).
  - [teyit-tetik; M] "EMA5 > EMA8 > EMA13 > EMA34 sıralaması" — bullish engulfing yanında hacim, RSI30 altından çıkış veya MACD, EMA34 kırılımı ve ikinci gün devamı; hacim/kalıcılık eşikleri yok — çekirdek belli.
- Örnek ve sonuç: görselden: BTC-USD günlük; kod veri aralığı start=2022-04-1, end=2024-02-27; çıktı 38 sinyal, sonraki mum yükselişi %68.4210526, düşüşü %31.5789474. Sayım `engulfing_signal == 1` koşulundadır; fonksiyonda 1 bearish,2 bullish kodudur. Sonraki mumun kendi Close>Open/Close<Open yönü sayılır. Rejection ve engulfing toplamından oluşturulan `signal` daha sonra `engulfing_signal` ile üzerine yazılır; bu ölçüm rejection filtresinin başarısı değildir.
- Tansu'nun vurgusu: "Bu veri setinde geri dönüş sinyali olarak engulfing'e pek güvenmemelisin."
- YORUM: %31.58, bu veri setinde bearish engulfing sonrasındaki kırmızı mum oranıdır; uzun bir trend dönüşünün veya kârlı işlemin başarı oranı değildir. %68.42 sonraki mumun yükselişidir, bearish sinyal başarısı değildir.

### X209 · 2025-03-13 23:44:22 UTC · Haftalık TOBO onayı
- Bağlı: R219; Öneri: tema-2 #9
- Yazar: T (geriye dönük kontrol notu/giriş) + M (başlıklı TOBO açıklaması) + G.
- Kaynak: 1900332136906784924 (2025-03-13 23:44:22 UTC), 1913995238978277848 (2025-04-20 16:36:39 UTC).
- Fikirler:
  - [teyit-tetik; M] "Fiyat bu çizgiyi haftalık kapanışla yukarı kırarsa, formasyon onaylanmış olur." — boyun üstü haftalık kapanış; sol omuzdan başa hacim azalması, sağ omuzdan boyuna artması, kırılımda yüksek hacim — çekirdek belli.
  - [giriş; M] "Bu, satış fırsatı değil, genellikle ikinci alım fırsatıdır." — boyuna pullback; sağ omuz oluşmadan giriş erken — çekirdek belli.
  - [hedef-çıkış; M] "Baş ile boyun çizgisi arasındaki mesafe, kırılım noktasına eklenerek hedef belirlenir." — baş20, boyun/kırılım30 ise hedef40 — çekirdek belli.
- Örnek ve sonuç: Tansu geriye dönük kontrolde "Hiç getirmeyen haftalıkta %30-40 arası getirmiş." der; örneklem, dönem, tutma süresi ve maliyet yok. Baş20/boyun30 örneği eğitim hesabıdır.
- Tansu'nun vurgusu: "Artık her gün taratıp formasyonu bekleyeceğiz."; "#python ile tam da bunu yazdım."
- YORUM: R219 OBO'dur; burada yukarı kırılan TOBO varyantı tutuldu. Getiri sözü genel performans kuralına çevrilmedi.

### X210 · 2025-11-07 16:03:17 UTC · RSI çizgisine Fibonacci
- Bağlı: yeni yöntem; Öneri: tema-2 #10
- Yazar: M (Tansu hesabında uzun, başlıklı açıklama).
- Kaynak: 1986826801885167861 (2025-11-07 16:03:17 UTC).
- Fikirler:
  - [bölge; M] "doğrudan RSI indikatörünün üzerine uygulamaya dayanır." — genellikle RSI14; geriye dönük144 gün/çubuk RSI max/min arasına Fibo23.6/38.2/50/61.8 — çekirdek belli.
  - [teyit-tetik; M] "Bu seviyeler artık sizin "momentum destek ve direnç" seviyelerinizdir" — boğada 38.2/50'den yukarı, ayıda 50/61.8'den aşağı dönüş; dönüş miktarı/stop/çıkış yok — çekirdek belli.
- Örnek ve sonuç: gerçek hisse, ölçüm veya işlem sonucu yok.
- Tansu'nun vurgusu: ayrı bir Tansu cümlesi ayırt edilemiyor; açıklamanın kendisi M'dir.
- YORUM: Kaynak yöntemi mekanik sistem değil yoruma dayalı model sayar. R208 fiyat Fibo+RSI uyumsuzluğu anlatır; aynı yöntem değildir. "144 periyot" RSI hesap süresi olarak değil inceleme penceresi olarak ayrıldı.

### X211 · 2025-04-06 21:55:50 UTC · Level 1/2 dip taraması ve onay bekleme
- Bağlı: yeni yöntem (R039 ile ilişkili); Öneri: tema-2 #11
- Yazar: T + G (kendi algoritmasının çıktıları).
- Kaynak: 1909002131635331358 (2025-04-06 21:55:50 UTC), 1910423863822811223 (2025-04-10 20:05:17 UTC), 1924944817441710378 (2025-05-20 21:46:22 UTC), 1950987288378519760 (2025-07-31 18:29:51 UTC), 2002099118366486932 (2025-12-19 19:30:01 UTC).
- Fikirler:
  - [tarama-evren] "Son 10 gün içinde dip yapmış hisseler taramasına bir örnek." — Level1 day trade; Level2 trend takibi, daha az sinyal — çekirdek belli.
  - [teyit-tetik] "dip onaylandıktan sonra kısa sürede işleme girecek." — diğer göstergeler olumluysa işlem; grid search ile optimizasyon yapılabilir; mum yapısı teyit kodu planı — çekirdek belli.
  - [ölçüm-ilkesi] "kırmızı toplar tepeler yeşil toplar dipler yani bunları sinyal olarak görmemek lazım." — dip yoksa yeni tepeler işaretlenir — çekirdek belli.
- Örnek ve sonuç: KRONT alıntısının yazarı The_Tansu_: üç kriter+OB ile birinci derece dip ve tavan iddiası. görselden: EMA13>EMA8>EMA5, 3INSIDE/BELTHOLD/CLOSINGMARUBOZU etiketleri. Üç kriterin tam tanımı ve ikinci derece ayrımı verilmemiştir.
- Tansu'nun vurgusu: "Dibi herkes kendine göre yakalıyor benim de kendi algoritmam var"; "repaint yok..."
- Belirsiz: Repaint yok ifadesi Tansu'nun iddiasıdır; geçmiş etiketler yeniden hesaplanmadı. Level1/2 algoritma parametreleri bilinmiyor; ATR zigzagın aynısı veya başka dip taraması olabilir.

### X212 · 2025-04-12 12:48:36 UTC · ATR dönüş dibi ve kurum yoğunlaşması
- Bağlı: R039 / R221 (ikinci bağ aynı yöntem olduğunu göstermez); Öneri: tema-2 #12
- Yazar: T giriş + M (uzun algoritma ve ATR/kurum açıklamaları).
- Kaynak: 1911038743839900154 (2025-04-12 12:48:36 UTC), 1964644641208222079 (2025-09-07 10:59:18 UTC).
- Fikirler:
  - [teyit-tetik; M] "Sadece fiyatın 97.5 seviyesinin altına düşmesi tek başına yeterli değil." — son tepe100, ATR2.5, eşik97.5; dip97 ancak yukarı tepkiyle onaylanır; ATR periyodu ve tepki eşiği yok — çekirdek belli.
  - [bölge; M] "eksi üç ATR seviyesinde sert bir düşüş yaşayıp ardından eksi iki ATR civarlarında toparlanmaya başlayan hisseler" — birkaç günlük karışık kırmızı/yeşil yapı; bant merkezinin hangi ortalama olduğu metinde yok — çekirdek belli.
  - [teyit-tetik; M] "ilk beş kurumun hiçbiri satışa geçmiyorsa" — bir hafta; ilk5 payı yaklaşık%40/%50/%60, ilk2 yaklaşık%60–70, takasta toplulaşma ve emeklilik fonu ağırlığı — çekirdek belli.
- Örnek ve sonuç: ATR örneği varsayımsaldır; gerçek getiri/işlem dökümü yok.
- Tansu'nun vurgusu: "Dip ve Tepe Algoritmam Nasıl Çalışıyor"; "Şunu da açıklayayım çok sordunuz."
- Belirsiz: Aynı toplam/payda kullanılırsa ilk2 payının ilk5'i aşması mümkün değildir. Farklı payda/periyot veya gevşek örnek yüzdeler olabilir; iki yüzde grubu eşzamanlı kesin kapı yapılmadı. R039 dönüş algoritmasıyla −3/−2 ATR bant taraması tek algoritma sayılmadı.

### X213 · 2025-04-12 19:14:19 UTC · RSI trend kırılımı ve aynı gün Belt Hold
- Bağlı: R208; Öneri: tema-2 #13
- Yazar: T (tarama/sonuç girişi) + M (başlıklı açıklama) + G.
- Kaynak: 1911135810839105880 (2025-04-12 19:14:19 UTC), 1911146678016504174 (2025-04-12 19:57:30 UTC).
- Fikirler:
  - [teyit-tetik; M] "RSI trend kırılımı varsa ve o gün BELTHOLD yakalanmışsa, bu çok güçlü bir teknik sinyal olur." — RSI iki tepeden geçen düşen çizgiyi son gün yukarı kırar; aynı gün TA-Lib bullish BELTHOLD — çekirdek belli.
  - [stop/hedef; M] "Stop-loss: o mumun altı. Hedef: 2-3 gün içi momentum takibi veya önceki dirençler." — RSI periyodu, çizgi seçimi ve kesin çıkış eşiği yok — çekirdek belli.
- Örnek ve sonuç: Tansu 8 Nisan kapanışındaki tarama örneğinin iki günde %5 marj verdiğini söyler; ikinci açıklama birkaç gün içinde %5 der. Marj, gerçekleşmiş net işlem getirisi diye alınmadı.
- Tansu'nun vurgusu: "Testere piyasasında fena getiri değil"
- YORUM: R208 dış infografik yerine burada Tansu hesabındaki uygulama anlatısı eklendi; M kural olgunluğu çekirdek belli tutuldu.

### X214 · 2025-08-03 19:18:26 UTC · EMA sıkışması içinde yükselen üçgen
- Bağlı: R127; Öneri: tema-2 #14
- Yazar: T (kodunu yazma notu) + M (strateji/teyit açıklaması) + G.
- Kaynak: 1952086678639669635 (2025-08-03 19:18:26 UTC), 1952092703740866703 (2025-08-03 19:42:23 UTC), 1952093418366112014 (2025-08-03 19:45:13 UTC), 1954300245707497649 (2025-08-09 21:54:22 UTC).
- Fikirler:
  - [formasyon; M] "En az iki tane birbirine yakın tepeler (yatay direnç seviyesi) ve üç veya daha fazla yükselen dip aranır." — örnek EMA10/20 yakınlığı; yakınlık toleransı yok — çekirdek belli.
  - [teyit/hedef; M] "üst çizginin üzerine taşan ve üzerinde kapanan bar" — kırılımda hacim ortalama üstü, geri testte düşük hacim, hedef taban yüksekliğinin yukarı projeksiyonu — çekirdek belli.
- Örnek ve sonuç: görselden: KAPLM/ZRGYO son3 gün içinde bulunan yükselen üçgen bölgeleri. KAPLM için Tansu yükselen trend desteği tepkisini de söyler. 9 Ağustos anlatımı EMA50/100/200 ve hafif düşen üst çizgili başka sıkışma örneğidir; ilk EMA10/20 taramasının parametreleri değildir.
- Tansu'nun vurgusu: "bana düşen de tabiki oturup kodunu yazmak ve taramasını yapmak oldu:)"
- Belirsiz: 9 Ağustos metni hem simetrik hem yükselen üçgen der. Ayrı tür veya yataya yakın üst çizginin yorumu olabilir; tek tür kesinleştirilmedi.
- YORUM: X'teki arkadaşın özgün fikir/kodu kanıt yapılmadı; Tansu'nun kendi yazdığını söylediği tarama ve M açıklaması alındı.

### X215 · 2026-08-23 09:03:22 UTC · Bullish X–B aşağı kırılımı ve D sonrası A teyidi
- Bağlı: R013 / R014; Öneri: tema-2 #15
- Yazar: T + G (Carney/Pesavento çıktıları).
- Kaynak: 2091451219659104540 (2026-08-23 09:03:22 UTC), 2092318619321446897 (2026-08-25 18:30:06 UTC).
- Fikirler:
  - [teyit-tetik; G] "X->B trend çizgisi son 10 günde AŞAĞI yönde KIRILDI" — ICBCT Bullish/Carney; kırılım2026-08-13 — çekirdek belli.
  - [teyit-tetik; G] "GÜÇLÜ TEYİT (A kırıldı)" — D sonrasında A'nın yukarı aşılması, trend hızlanması etiketi; C–D arasındaki A ihlalinden farklı aşama — çekirdek belli.
- Örnek ve sonuç: görselden: ICBCT D15.90, Fibo0.786=15.68, durum AKTİF. İkinci grafikte A5.63, D0.786=4.14; D sonrası A üstüne yükseliş görülür. Sembol ve işlem dökümü yok.
- Tansu'nun vurgusu: "acelemiz yok"; "Bazen donmesi gereken yerden ucar giderrrr"
- YORUM: Aşağı X–B kırılımı tek başına long giriş emri diye yazılmadı; grafik bullish yapının CD aşamasını da izler.

### X216 · 2025-08-02 14:04:51 UTC · Trend teması ve kanal ölçüm alanları
- Bağlı: R214 / R245; Öneri: tema-2 #16
- Yazar: T + G (temas tabloları/kanal grafikleri).
- Kaynak: 1951645372041806086 (2025-08-02 14:04:51 UTC), 1952069518538481977 (2025-08-03 18:10:15 UTC), 1984032255535443993 (2025-10-30 22:58:45 UTC), 1986488325180432605 (2025-11-06 17:38:18 UTC), 2097010207821877561 (2026-09-07 17:12:48 UTC).
- Fikirler:
  - [bölge; G] "Lookback"; "TAKİP ET" — trend taramasında 30/35/40 pencere; fiyat ve çizginin son gün değeri ayrı sütunlar — çekirdek belli.
  - [bölge; G] "İçeride kapanış: %100.0" — DENGE90 bar, üst/alt temas3/3, Low-Bant+0.09%, genişlik değişimi−27.8%; temas toleransı yazılı değil — çekirdek belli.
- Örnek ve sonuç: görselden: TSKB fiyat13.87/çizgi13.85 (yaklaşık%0.14 fark); TATEN temas80.20/trend80.24, son fiyat81.74; ADX14 ve20 referansı, RSI14 ve50 referansı. DOCO60 bar destek10072.40, fiyat10110.00. DENGE'nin başlığı simetrik üçgendir; paralel yükselen kanal değildir.
- Tansu'nun vurgusu: "Kanala temas et bakarız sonra #denge"
- Belirsiz: Yakın fiyat değerleri temas ölçümü veya toleranslı etiketleme olabilir; fiyat≈çizgi gözlemi kesin eşitlik/tolerans formülüne çevrilmedi. DENGE ile R245 AEFES aynı kanal türü değildir.

### X217 · 2024-10-21 20:30:31 UTC · R4/S4 pivot uzantısı ve haftalık uygulama
- Bağlı: R191; Öneri: tema-2 #17
- Yazar: T + G (kod ve sayısal not).
- Kaynak: 1848461886192271748 (2024-10-21 20:30:31 UTC), 1957867341552971801 (2025-08-19 18:08:44 UTC).
- Fikirler:
  - [bölge; G] `R4 = R3 + (R2 - R1)`; `S4 = S3 - (S1 - S2)` — kodun pivot uzantıları; `under_X` Close<X bayrağı — kural tam (hesap).
  - [hedef; T] "Haftalık Pivot Seviyeleri | Hafta başlangıcı: 2025-08-18" — haftalık PP/S1/S2/R1/R2 ayrı uygulama; ilk hedefR2 soru biçiminde — çekirdek belli.
- Örnek ve sonuç: Kodun evreni BIST30 listesi, veri başlangıcı2023-07-17. Metinde PP10915.87, S1 10741.53, R1 11044.93, S2 10612.47, R2 11219.27; 2ATR üstündeki endeks için R2 hedefi sorulur. Sonuç yok.
- Tansu'nun vurgusu: "Şu kodu alın bir kenarda dursun lazım olur."
- YORUM: Günlük kodda aynı satır H/L/C kullanılır; otomatik önceki gün kaydırması görülmez. Haftalık kaynak R4/S4 hesaplandığını göstermediğinden haftalık dört kademe diye birleştirilmedi.

### X218 · 2025-08-06 01:44:27 UTC · KDE 50 ve 100 mum varyantları
- Bağlı: R128; Öneri: tema-2 #18
- Yazar: T + G.
- Kaynak: 1952908597480075631 (2025-08-06 01:44:27 UTC), 1952908601275699243 (2025-08-06 01:44:28 UTC).
- Fikirler:
  - [bölge; G] "XU100.IS Son 50 Mum ve KDE Tepe Fiyatları"; "XU100.IS Son 100 Mum ve KDE Tepe Fiyatları" — kısa/orta vade gösterimleri; bandwidth, küme eşiği ve giriş yok — çekirdek belli.
- Örnek ve sonuç: görselden: iki grafikte son kapanış10849.96;50 mumda daha çok,100 mumda daha az yatay seviye. R128'in150 mumuna ek pencere örnekleri; işlem sonucu yok.
- Tansu'nun vurgusu: "Günlük al saçılar için endeksin durumu"; "Biraz daha orta vadeciler için"
- YORUM: Pencere etiketleri doğrulandı; 50/100 zorunlu ayar yapılmadı.

### X219 · 2024-12-25 21:10:25 UTC · Harmonik türler ve seçim menüsü
- Bağlı: R008 / R011; Öneri: tema-2 #19
- Yazar: T + G (kartlar/menü).
- Kaynak: 1872027142181232735 (2024-12-25 21:10:25 UTC), 1876368569438765488 (2025-01-06 20:41:42 UTC), 1877449919641833760 (2025-01-09 20:18:36 UTC), 1878174325863313704 (2025-01-11 20:17:08 UTC), 1893684348391391620 (2025-02-23 15:28:26 UTC), 1977815566183497963 (2025-10-13 19:15:51 UTC), 2089770598620713304 (2026-08-18 17:45:11 UTC).
- Fikirler:
  - [tarama-evren; G] "[11] TÜM FORMASYONLAR (Hepsini ara)"; "[0] Özel Seçim (Birden fazla formasyon seç)" — menüde Butterfly/Gartley/Cypher/Bat/Alt Bat/Crab/Deep Crab/Shark/White Swan/Black Swan; indirilen521 sembol — çekirdek belli.
  - [formasyon; G] "Bullish Alt_bat Found for MRGYO.IS" — tür etiketi doğrulanır; oran/tolerans kuralı yazılı değil — yalnız fikir.
- Örnek ve sonuç: görselden: Bat VKING/ANHYT/LIDER; Alt Bat MRGYO; Cypher INDEX-USD; Derin Yengeç CCOLA. MRGYO AB=−0.22; öneri belgesindeki−0.17 yanlıştır. Kartlarda çizgi örnekleri vardır; türlerin başarısı ölçülmemiştir.
- Tansu'nun vurgusu: "Gartley aramak istiyoruz canım :)"
- Belirsiz: Çoklu seçim menüsü tek ortak tarayıcı veya bağımsız tür taramalarını çağıran arayüz olabilir. R011'in konsolidasyon uyarısıyla yazılım mimarisi kesin çelişki sayılmadı.

### X220 · 2025-07-22 11:08:32 UTC · Elliott 3. dalga taraması ve W5 hedef varyantları
- Bağlı: R193 / R205 / R261; Öneri: tema-2 #20
- Yazar: T + G (araç sayımları).
- Kaynak: 1947614735068770788 (2025-07-22 11:08:32 UTC), 1950944201924845870 (2025-07-31 15:38:39 UTC), 1984338420769177613 (2025-10-31 19:15:21 UTC), 2000274228516413714 (2025-12-14 18:38:34 UTC), 2094008240824635656 (2026-08-30 10:24:04 UTC).
- Fikirler:
  - [teyit-tetik; G] "1. Tepe (B)"; "3. Dalga Başlangıcı" — ASGYO'da B üstüne geçiş ile başlangıç işaretlenir; son3 gün tarama etiketi ayrı çıktıdadır — çekirdek belli.
  - [hedef; G] "5. Dalga Hedef (W3*0.618): 212.92 TL" — TMPOL hedef etiketi; eklendiği taban açıklanmamış — çekirdek belli.
  - [hedef; G] "1.618 X (P1'den)"; "0.618 Y (P3'ten)" — ENJSA W5 kesişim bölgesi93.73–103.03, Fibo%49.2; X/Y bacak tanımları yok — çekirdek belli.
  - [teyit-tetik; T] "Yeni dipler gelmedi bana kalırsa C teyit oldu zaten BOM sinyalim de teyit vermişti." — yeni dip yokluğu+BOM; BOM tanımı yok — çekirdek belli.
- Örnek ve sonuç: görselden: ASGYO başlangıç2024-07-17 (gönderi2025); TMPOL itki+%59.0, W4−%14.7; IDGYO W2%86.4, W4%52.8, W3/W1=2.69, W5/W1=1.44, C/0–5=%110.4. Örnek oranlar tolerans kuralı değildir.
- Tansu'nun vurgusu: "Dikkatle izleyelim bu hafta"
- Belirsiz: 31 Temmuz2025 çıktısındaki tüm başlangıç tarihleri2024-07-30 iken başlık son3 gün der. Eski veri üzerinde tarama veya yanlış güncel etiket olabilir; güncel üç günlük başarı listesi sayılmadı.

### X221 · 2023-08-28 04:47:27 UTC · Çok pencereli dip uzaklığı ve 16 günlük konum
- Bağlı: yeni yöntem (R227 ile ölçüm akrabası); Öneri: tema-2 #21
- Yazar: T + G.
- Kaynak: 1696021655947018369 (2023-08-28 04:47:27 UTC), 1775315669824700852 ve 1775315672647528494 (2024-04-03 00:13:34 UTC).
- Fikirler:
  - [ölçüm-ilkesi; T] "16 günlük kaydırılmış pencereler ile max ve min fiyatlarını ve hissenin anlık konumunu görselleştirdim." — konum0–1; ayrı R227 uygulamasında 252 gün — çekirdek belli.
  - [ölçüm-ilkesi; G] "Haftalık Dipten Uzaklık (%)" — haftalık/aylık/3/6/12 aylık dip-zirve aralığında konum; tablo 100×(son−dip)/(zirve−dip) ile uyuşur — çekirdek belli.
- Örnek ve sonuç: görselden: otomotiv listesi28/08/2023; DOAS son279.70, haftalık dip271.10, zirve325.81, uzaklık%15.72. KFEIN16 günlük konum grafiğinin sonu1'e yakındır; işlem sonucu yok.
- Tansu'nun vurgusu: "artık 16 günlük zirvesine yakın olduğunu ve dalgalanma ile aşağıya sarkabileceğini söylüyor bize."
- Belirsiz: KFEIN görselinin ekseni2022'dir; 2024 gönderisinin güncel verisi veya eski örnek gösterimi olabilir. Konumun kesin0.95 olduğu yazılı değildir; yaklaşık değer zorunlu eşik yapılmadı.
- YORUM: Yüzde formülünde öneride eksik bırakılan ×100 eklendi; konum hesabı ile dip fiyatına göre yüzde prim aynı şey değildir.

### X222 · 2025-08-19 18:49:48 UTC · EMA26 merkezli ATR14 bant çıktısı
- Bağlı: yeni yöntem; Öneri: tema-2 #22
- Yazar: T + G (sayısal rapor).
- Kaynak: 1957877677777375736 (2025-08-19 18:49:48 UTC).
- Fikirler:
  - [bölge; G] "ATR Seviyeleri — EMA26 merkezli" — bant=EMA26±k×ATR14, k1/2/3; sayısal raporla uyuşur — kural tam (hesap).
  - [bölge; G] "Kapanış +2ATR üstünde | Kapanış pivot bandında (S1–R1)" — konum etiketi; giriş/stop/çıkış kuralı yok — yalnız fikir.
- Örnek ve sonuç: görselden:2025-08-19 Close10962.02, EMA26=10673.24, ATR14=114.73, +2ATR10902.70, −2ATR10443.78, Close–EMA26 sapma%2.71. MACD hook/0 geçiş/kesişim türleri ayrı tabloda; ölçümden sonraki getiri yok.
- Tansu'nun vurgusu: "Yorumu size bırakayım:)"
- YORUM: Bant formülü rapor sayılarından doğrulandı; konum tek başına AL/SAT kuralı sayılmadı.

### X223 · 2024-10-20 13:25:06 UTC · CDL etiketleri, tek mumlar ve Dark Cloud Cover
- Bağlı: R143; Öneri: tema-2 #23
- Yazar: T (kısa tarama notları) + M (Dark Cloud Cover açıklaması) + G.
- Kaynak: 1847992441699246587 (2024-10-20 13:25:06 UTC), 1851736967240618260 (2024-10-30 21:24:31 UTC), 1855002192115024146 (2024-11-08 21:39:21 UTC), 1906062787979210957 (2025-03-29 19:15:56 UTC), 1907095706285826234 (2025-04-01 15:40:23 UTC), 1908505150668370269 (2025-04-05 13:01:00 UTC), 1982688365007794207 (2025-10-27 05:58:37 UTC), 2009318796025360724 (2026-01-08 17:38:26 UTC).
- Fikirler:
  - [tarama-evren; G] "Günlük analizde son gün mum formasyonu tespit edilen BIST 30 hisseleri:" — çıktıda CDLENGULFING/CDLBELTHOLD/CDLCLOSINGMARUBOZU/CDLSHOOTINGSTAR vb.; metin BİST100 der, liste 30'dan çok sembol içerir — yalnız fikir.
  - [formasyon; M] "İlk mum beyaz ve uzun olmalıdır."; "İkinci mum siyah olmalı ve ilk mumun üstünde açılıp ilk mumun ortasından aşağısında kapanmalıdır." — Dark Cloud Cover yukarı trendde; ikinci gün hacim artışı teyit, stop ilk mum high, hedef yakın destek — çekirdek belli.
  - [teyit-tetik; G] "BULLISH PATTERNS: BELTHOLD CLOSINGMARUBOZU" — dip taraması örneğinde iki etiket; gövde/fitil eşikleri yok — yalnız fikir.
- Örnek ve sonuç: görselden: Shooting Star BRISA/AYGAZ; XU100 mumlarında CDL etiketleri. MEPET metni "78.6 bölgesinde güzel bir asılı adım, kırılınca hedef 10.22" der (yazım korunmuştur). KRVGD Piercing çıktısı4 işlem, hit ratio%50.0, profit factor2.78, realized RR2.78; dönem/maliyet ve işlem listesi yok.
- Tansu'nun vurgusu: "Bunlar momentum hisselerim değil, basit taramalar. Detayına siz bakacaksınız artık"
- Belirsiz: BIST30/BIST100 evreni çıktı başlığı, metin ve semboller arasında ayrışır; eski başlık veya farklı evren olabilir. Dark Cloud Cover'da "ilk mumun üstünde" high veya gövde üstü olarak okunabilir; kesin gap kodu yok.
- YORUM: Ham CDL etiketi işlem sistemi değildir; Piercing ölçümü başka mum formasyonlarına genellenmedi.

### X224 · 2024-09-16 06:00:57 UTC · Kanal ve ortalama türevleri
- Bağlı: R039 / R053; Öneri: tema-2 #24
- Yazar: T + G (araçlar); M (dikdörtgen psikolojisi açıklaması, dış şema eşliğinde).
- Kaynak: 1835559479842070775 (2024-09-16 06:00:57 UTC), 1852451504705155208 (2024-11-01 20:43:50 UTC), 1873520948949008581 (2024-12-30 00:06:17 UTC), 1875902526824030471 (2025-01-05 13:49:49 UTC), 1914188571033940188 (2025-04-21 05:24:53 UTC), 1914387519392579977 (2025-04-21 18:35:26 UTC), 1950285317841301734 (2025-07-29 20:00:28 UTC), 1952070959529336857 (2025-08-03 18:15:59 UTC), 1952071338971091397 (2025-08-03 18:17:29 UTC), 1979691577632231774 (2025-10-18 23:30:27 UTC), 1987071191442497586 (2025-11-08 08:14:24 UTC), 1995924034911961480 (2025-12-02 18:32:27 UTC).
- Fikirler:
  - [bölge; T] "30-109-150 (parametreler optimize edilmiştir)" — günlük DOAS Vegas; ortalama türü ve optimize edilen dönem yok — yalnız fikir.
  - [bölge; G] "KC Middle (EMA20)" — AAPL Keltner±1/±2/±3, EMA5, SMA200/250, RSI14 ve70/30; ATR periyodu/çarpanı açık değil — çekirdek belli.
  - [teyit-tetik; G] "T3 Kesişimi (AL)"; "Formasyon: CDLBELTHOLD" — T3 yanında EMA5/8/13/21; T3 periyot/katsayı yok — yalnız fikir.
  - [bölge; G] "Kanal Orta Noktası" — DURDO/LOGO ortası; RSI14 ve EMA10 yan panelde; orta çizgi hesabı yok — yalnız fikir.
  - [bölge; G] "Support (min slope)"; "Resistance (max slope)" — zarf örnekleri AKFGY45 mum, AYCES27 mum; ayrı trend çizgisi için Tansu72 günlük lookback der — çekirdek belli.
  - [giriş; G/M] "BUY SIGNAL"; "SELL SIGNAL" — altın regresyon grafiğinde alt/üst bant işlemleri; dikdörtgen M anlatısında destekte alıp dirençte satış; SAYAS Range Breakout+CDLBELTHOLD başlığı — yalnız fikir.
- Örnek ve sonuç: Görseller parametre veya örnek gösterir; net işlem dökümü yok. Dikdörtgen psikolojisi görselinin özgün dış yazarlığı Tansu'ya mal edilmedi; Tansu hesabındaki M açıklaması alınmıştır.
- Tansu'nun vurgusu: "Ben size temelini vereyim siz kendinize göre evirin."; "Coşkuyu verirseniz bunun gibi ne mıknatıslar paylaşırım:)"
- Belirsiz: AKFGY metni30 gün, görsel45 mum der; farklı pencere veya eski metin olabilir. BTC metni Keltner, görsel DC_UP/DC_DOWN der; Donchian adlandırması veya başka kanal olabilir. Vegas30/109/150, X010'daki Vegas12/144/169 ile aynı parametre seti sayılmadı.

### X225 · 2026-09-04 17:32:06 UTC · Takoz kartının kalite ölçümleri
- Bağlı: R006; Öneri: tema-2 #25 (R006)
- Yazar: T + G.
- Kaynak: 2095927899249406462 (2026-09-04 17:32:06 UTC).
- Fikirler:
  - [formasyon; G] "ACSEL — Düşen Takoz Kırılımı" — kalite ve kırılım raporu; tarama eşikleri yok — çekirdek belli.
- Örnek ve sonuç: görselden: skor99.0/100, kırılım2026-09-04, çizgi üstü%2.19, daralma%77.0, içeride%93.3, temas5+3, hacim2.16x (MA20), teyit EVET. Sonraki getiri yok.
- Tansu'nun vurgusu: "ben detayına bakmıyorum sonra bana gitmedi oydu buydu demeyin"; "Buna teknik analizde retest deniyor."
- YORUM: Kartın skor değerleri asgari kabul eşikleri değildir; R006'nın yalnız yöntem adına çıktı alanları eklendi.

### X226 · 2025-03-14 14:29:15 UTC · Haftalık bayrak ve günlük rapor alanları
- Bağlı: R007; Öneri: tema-2 #25 (R007)
- Yazar: T + G.
- Kaynak: 1900554823331635298 (2025-03-14 14:29:15 UTC), 2096025629770571980 (2026-09-05 00:00:27 UTC).
- Fikirler:
  - [formasyon] "Haftalık boğa bayrak formasyonu. (Başlıkta günlük kalmış, aldırmayınız)" — DGGYO haftalık; başlık Tansu tarafından düzeltilir — çekirdek belli.
  - [ölçüm-ilkesi; G] "KIRILIMDAN UZAKLIK" — tarama raporunda kırılım fiyatı, uzaklık, RSI14, hacim değişimi — yalnız fikir.
- Örnek ve sonuç: görselden: DGGYO kırılım2025-03-10. ARDYZ Yükseliş Bayrak, kırılım2026-09-04, fiyat87.70, uzaklık%0.0, RSI14=45.1, hacim değişimi+%98.6. Sonraki getiri yok.
- Tansu'nun vurgusu: "Hissemiz paylaşıldı. Kırılım gerçekleşti."
- YORUM: Haftalık örnek ve diğer raporun parametreleri tek tarama kuralı yapılmadı.

### X227 · 2026-08-22 07:33:42 UTC · CD şiddetinde adı açıklanmayan zaman ölçütü
- Bağlı: R016; Öneri: tema-2 #25 (R016)
- Yazar: T; yanıt verilen üst gönderi A (Cr_Soprano), kanıt olarak kullanılmadı.
- Kaynak: 2091066263594295378 (2026-08-22 07:33:42 UTC).
- Fikirler:
  - [formasyon] "bu kesinlikle doğru ama bir tane daha var gözden kaçan, time management açısından daha önemli." — ikinci zaman ölçütü var; adı, formülü ve sayısı yok — yalnız fikir.
- Örnek ve sonuç: yok. Üst gönderi2091053758310470040'ın yazarı Cr_Soprano'dur; AB oluşum süresi onun cümlesidir.
- Tansu'nun vurgusu: "time management açısından daha önemli."
- Belirsiz: Tansu'nun onayı AB süresini benimsediği anlamına veya yanıt bağlamındaki genel doğruluğa gelebilir; açık kendi kural cümlesi olmadığı için AB süresi tek başına kanıt yapılmadı.

### X228 · 2025-07-30 19:18:21 UTC · Fibo 138.2 uzantısı
- Bağlı: R020; Öneri: tema-2 #25 (R020)
- Yazar: T + G.
- Kaynak: 1950637105606173073 (2025-07-30 19:18:21 UTC).
- Fikirler:
  - [hedef-çıkış; G] "138.2%" — ANELE uzantı çizgisi;161.8% de gösterilir; giriş ve çıkış koşulu yok — yalnız fikir.
- Örnek ve sonuç: görselden: son mumun fitili138.2% çizgisine ulaşır, gövde altında kalır; hedefin tutulduğunu gösteren işlem dökümü yok.
- Tansu'nun vurgusu: "FİBO kodunuzu doğru yazarsanız yakalarsınız."
- YORUM: R020'deki1.272/1.618/2.0 yanına1.382 gösterim örneği eklendi; her uzantı zorunlu hedef yapılmadı.

### X229 · 2026-08-10 20:58:10 UTC · Elliott hedefleri arasında yüzde 5 konfluans alanı
- Bağlı: R040; Öneri: tema-2 #25 (R040)
- Yazar: T.
- Kaynak: 2086920060254212344 (2026-08-10 20:58:10 UTC).
- Fikirler:
  - [bölge] "iç sayım ve dış sayım tekniği ile bir hedef belirlediniz ama %5 fibi bir sapma var. İşte o %5'lik alandır confluence alanı." — örneğe özgü%5 alan; payda ve merkez belirtilmemiş — çekirdek belli.
- Örnek ve sonuç: hisse, fiyat ve sonuç yok.
- Tansu'nun vurgusu: "İşte o %5'lik alandır confluence alanı."
- YORUM: Örnekteki%5 bütün konfluanslar için sabit tolerans yapılmadı; bağımsız faktör ilkesinin nicel örneğidir.

### X230 · 2026-08-10 14:31:45 UTC · Regional high/low ve HSAR kümeleri
- Bağlı: R055; Öneri: tema-2 #25 (R055)
- Yazar: T + G (kendi HSAR çıktıları); kitap kapağı dış kaynak, yöntem yazarlığı Tansu'ya mal edilmedi.
- Kaynak: 2086822816695918859 (2026-08-10 14:31:45 UTC), 2086827188788035838 (2026-08-10 14:49:07 UTC).
- Fikirler:
  - [bölge; G] "HSAR (Horizontal Support & Resistance)" — regional high/low noktaları ve n etiketli yatay kümeler; tolerans/pencere yok — çekirdek belli.
- Örnek ve sonuç: görselden: FROTO18.28/31.62/79.39/87.10 seviyelerinin her biri n=2; GC=F3427.27 n=3. Kitap kapağı Prodromos E. Tsinaslanidis/Achilleas D. Zapranis, Technical Analysis for Algorithmic Pattern Recognition. İşlem sonucu yok.
- Tansu'nun vurgusu: "Bu kitabı anlamak böyle işler yaptırır"
- Belirsiz: n kümeye giren pivot sayısı veya seviye temas sayısı olabilir; görsel n'nin hesap tanımını vermez. Önerideki kesin "regional high/low sayısı" çıkarımı YORUM düzeyindedir.
- YORUM: Tansu'nun araç uygulaması alındı; kitap içindeki özgün kural alıntısı ayrı T kaydı yapılmadı.

### X231 · 2026-09-05 12:51:49 UTC · Trident teorik ve gerçek D ayrımı
- Bağlı: R090; Öneri: tema-2 #25 (R090)
- Yazar: T (sembol) + G.
- Kaynak: 2096219752695816530 (2026-09-05 12:51:49 UTC).
- Fikirler:
  - [bölge; G] "Destek ±%2.0" — kanal destek bandı; teorik/gerçekD ayrı — çekirdek belli.
  - [giriş; G] "AL / GİRİŞ" — etiket gerçekD noktasında; genel giriş şartı yazılı değil — yalnız fikir.
- Örnek ve sonuç: görselden: CMBTN teorikD1453.00, gerçekD1496.00, A1985.00; B≈1480/C≈1950. Fark43.00, teorikD'ye göre yaklaşık%2.96 (bu incelemede hesap). Yaklaşık B/C ile B×C/A≈1454 çıkar; kesin formül kanıtı değildir.
- Tansu'nun vurgusu: yalnız "#cmbtn"; ayrı strateji cümlesi yok.
- Belirsiz: Yuvarlanmamış B/C veya başka kalibrasyon teorik1453'ü verebilir. GerçekD≈1496 ve teorik1453 farkı kanalın±%2 toleransıyla aynı ölçüm değildir.

### X232 · 2024-04-11 09:50:30 UTC · EMA20 desteği ve RSI50 uyarısı
- Bağlı: R105; Öneri: tema-2 #25 (R105)
- Yazar: T.
- Kaynak: 1778359964634915038 (2024-04-11 09:50:30 UTC).
- Fikirler:
  - [bölge] "20 günlük EMA (15.64) destek olarak çalışmış." — AGROT destek örneği — çekirdek belli.
  - [momentum-seçim] "Hisse momentum kaybediyor. RSI'50'nin altına düştü düşecek." — yaklaşan50 altı risk; kesin gerçekleşmiş50 kırılımı değildir — çekirdek belli.
- Örnek ve sonuç: AGROT; sonraki fiyat/işlem sonucu yok.
- Tansu'nun vurgusu: "Bana kalırsa aşağıya kırmak üzere."
- Belirsiz: "düştü düşecek" yaklaşma veya gerçekleşmeye çok yakın kırılım diye okunabilir; kaynak sonunda "Ayrıca 5 günlük ve" diye kesilir. Eksik ortalama koşulu tamamlanmadı.

### X233 · 2025-11-13 21:54:40 UTC · FVG temasının yüzde uzaklık etiketi
- Bağlı: R129; Öneri: tema-2 #25 (R129)
- Yazar: G (Tansu hesabındaki araç çıktısı; gönderi metni boş).
- Kaynak: 1989089558164873727 (2025-11-13 21:54:40 UTC).
- Fikirler:
  - [bölge; G] "TEMAS FVG (0.00% Uzaklık)" — en yakın FVG seçimi ve yüzde uzaklık; formül/eşik yok — çekirdek belli.
- Örnek ve sonuç: görselden: ADEL BULLISH, fiyat29.74; en yakın FVG sarı bantta, son mumun alt fitili bölgeye erişir. Sonraki işlem sonucu yok.
- Tansu'nun vurgusu: metin yok; Tansu'nun kendi cümlesi bulunmuyor.
- Belirsiz: %0.00 bölgeye herhangi bir temasın uzaklığı veya fiyatın kutu içinde oluşu olarak hesaplanabilir; kapanışın kutuda olduğu kuralı çıkarılmadı.

### X234 · 2024-10-04 14:01:24 UTC · Fibo ve EMA200 aynı noktada
- Bağlı: R149; Öneri: tema-2 #25 (R149)
- Yazar: T (kısa açıklama).
- Kaynak: 1842203367826706883 (2024-10-04 14:01:24 UTC).
- Fikirler:
  - [teyit-tetik] "Fibonacci seviyeleri ile 200 EMA'nın aynı noktada kesişmesi, fiyatın bu alanlarda güçlü tepkiler verebileceğine dair yüksek olasılıklı bir sinyal oluşturur." — Fibo/EMA200 çakışması; yakınlık toleransı yok — çekirdek belli.
  - [pencere] "Son 6 aylık veriler üzerinden fibo çizdirilmiştir." — bu gönderinin metindeki penceresi6 ay — çekirdek belli.
- Örnek ve sonuç: arşivde bu id'nin media alanı boş; bu id'ye ait yerel görsel bulunmadı. Tepki yüzdesi ve sonuç yok.
- Tansu'nun vurgusu: "aynı noktada kesişmesi"
- Belirsiz: Öneri belgesi aynı günkü DOAS grafiği üzerinden1 yıl olabileceğini söyler; bu id'nin görseli yoktur. Bu metin6 ay, X206 kodu1 yıl olarak ayrı tutuldu; iki sürüm veya başlık hatası olabilir.
- YORUM: Başka id'nin görseli bu gönderinin6 ayını kesin çürüten kanıt yapılmadı.

### X235 · 2026-01-27 20:18:56 UTC · CIMSA trend desteği ve stop varyantı
- Bağlı: R168; Öneri: tema-2 #25 (R168)
- Yazar: M (Tansu hesabında başlıklı grafik anlatımı) + G.
- Kaynak: 2016244555516150121 (2026-01-27 20:18:56 UTC).
- Fikirler:
  - [teyit-tetik; M] "Mavi çizgi, turuncu çizgiyi yukarı kesmiş ve yeşil çubuklar oluşmaya başlamış." — MACD teyidi; RSI aşırı alımda değil, fiyat ortalamalar üstünde, trend+demand tepkisi — çekirdek belli.
  - [stop/hedef; M] "yaklaşık 45-46 TL seviyelerinin altına" — trend çizgisi altında kalıcı olma stop; eski zirve50TL ve üzeri hedef; kalıcı süre yok — çekirdek belli.
- Örnek ve sonuç: CIMSA açıklaması. R168 GEDZA grafiğidir;45–46 stop GEDZA'ya taşınmadı. Metin yükselişi açıklıyor, gerçekleşmiş işlem dökümü yok.
- Tansu'nun vurgusu: ayrı T cümlesi ayırt edilemiyor; "Neden yükseldi" başlığı da tek başına yazarı kesinleştirmez.
- YORUM: Aynı bölge/teyit ailesinde başka hisse uygulamasıdır; R168'de bulunmayan stop'u onun geçmiş işlem kuralı diye yazmaz.

### X236 · 2024-04-12 08:50:47 UTC · Üç sapmalı Bollinger ortalamaya dönüşü
- Bağlı: R190; Öneri: tema-2 #25 (R190)
- Yazar: T + G.
- Kaynak: 1778707323147448589 (2024-04-12 08:50:47 UTC), 1786749759627133185 (2024-05-04 13:28:33 UTC).
- Fikirler:
  - [hedef-çıkış] "BB ve 3SS ile 20EMA." — DOAS20EMA merkez ve3 standart sapma,317–318'e geri çekilme beklentisi — çekirdek belli.
  - [hedef-çıkış] "20 günlük HO değmek istiyorum gibi bir görüntü var saatlikte." — CUSAN saatlik ortalamaya dönüş beklentisi — çekirdek belli.
- Örnek ve sonuç: görselden: CUSAN60 dakikalık grafikte BOL(20,3); merkez20 periyot. Kaynak: "Cuma günü getirisinin bir kısmını aldı" (özne hisse olabilir; Tansu "aldım" demez); miktar yok.
- Tansu'nun vurgusu: "Dikkatli olmakta fayda var"
- Belirsiz: CUSAN metni20 günlük HO, grafiği60dk/BOL20 der. Metin dil sürçmesi veya ayrıca günlük ortalama olabilir;20 gün=20 saat yapılmadı.

### X237 · 2025-12-19 22:42:06 UTC · Yükselen desteğin altındaki FVG hedefi
- Bağlı: R204; Öneri: tema-2 #25 (R204)
- Yazar: T + G.
- Kaynak: 2002147457422307730 (2025-12-19 22:42:06 UTC).
- Fikirler:
  - [hedef-çıkış] "fiboyu çektikten sonra trend desteğine yakın olan FVG hedeftir. Hele bu FVG 0.618 alanında ise güçlü hedeftir. Yıkar geçer desteği." — düzeltmede FVG0.618 hedefi; yükselen trend desteği mutlaka tutmaz — çekirdek belli.
- Örnek ve sonuç: görselden:0.618=185.51 ve FVG bandı; fiyat yükselen mavi trend desteğinin altına sarkmıştır. Sembol ve gerçekleşmiş işlem getirisi yok.
- Tansu'nun vurgusu: "Siz sanıyor musunuz ki yükselen trend desteği her zaman çalışacak?"
- YORUM: FVG burada aşağı düzeltme hedefidir; bütün FVG'ler zorunlu alış seviyesi yapılmadı.

### X238 · 2025-04-11 17:26:57 UTC · Inverted hammer açıklaması
- Bağlı: R241; Öneri: tema-2 #25 (R241)
- Yazar: M (tanım biçimli Tansu hesabı metni).
- Kaynak: 1910746404265279494 (2025-04-11 17:26:57 UTC).
- Fikirler:
  - [formasyon; M] "Bu formasyon bir düşüş trendi sonrasında oluşur. Gövdesi kısa ve fitili uzun bir mumdur." — CDLINVERTEDHAMMER; gövde/fitil oranı verilmemiş — çekirdek belli.
- Örnek ve sonuç: metinde tespit tarihi2025-04-09; kaynak gönderi11 Nisan'dır. Getiri veya ALKA eşlemesi yok.
- Tansu'nun vurgusu: ayrı T cümlesi yok.
- YORUM: Bu id'de RSI pozitif uyumsuzluğu koşulu yok; önerideki o birleşim bu gönderiden alınmadı. R241'in ALKA mum yorumunun aynısı değildir.

### X239 · 2026-08-27 21:15:06 UTC · Medyan çevresinde bir standart sapma fikri
- Bağlı: R244 / R001; Öneri: tema-2 #25 (R244)
- Yazar: T; üst gönderi A (Aldirmaz027), kendi sisteminin ayrıntıları kanıt yapılmadı.
- Kaynak: 2093084917080924363 (2026-08-27 21:15:06 UTC).
- Fikirler:
  - [bölge] "Bir standartı sapma etrafında olması çok mantıklı. Medyanın bir diğer kullanım şeklidir." — medyan etrafında 1 standart sapma fikri; pencere ve sapmanın hangi veriyle hesaplandığı yok — çekirdek belli.
- Örnek ve sonuç: gerçek hisse ve ölçüm yok.
- Tansu'nun vurgusu: "Medyanın bir diğer kullanım şeklidir."
- YORUM: Medyan±1SS simetrik bant bu cümlenin yorumu olarak makuldür; Tansu açık formül vermediğinden kesin kod kuralı yapılmadı. Üst gönderideki high/low hesapları Tansu'nun yöntemi diye yazılmadı.

### X240 · 2024-12-24 18:39:15 UTC · Kelebek uzantıları ve 15 günlük swing penceresi
- Bağlı: R250; Öneri: tema-2 #25 (R250)
- Yazar: T + G.
- Kaynak: 1871626708304150884 (2024-12-24 18:39:15 UTC), 1879995899432301062 (2025-01-16 20:55:25 UTC), 1883641498564264218 (2025-01-26 22:21:44 UTC), 2091947979921891468 (2026-08-24 17:57:19 UTC).
- Fikirler:
  - [pencere] "15 günlük swing penceresi ile yapılmıştır" — XU100 kelebek; swing pivot ölçütleri yok — çekirdek belli.
  - [hedef; G] "1.272 (D hedefi): 15813.80"; "1.618 (max risk): 16588.36" — bearish XU100 A12966.30, X15204.90; A+r×(X−A) ile uyuşur — çekirdek belli.
- Örnek ve sonuç: görselden: eski kartlarda (A−D)/XA; EGGUB(2.90−2.60+6.05)/3.80≈1.67; JANTS(2.38−0.80+1.74)/2.76≈1.20; IHEVA(0.28−0.18+0.32)/0.37≈1.14. XU100 D hedefi AKTİF, henüz gerçekleşmiş hedef sonucu değil.
- Tansu'nun vurgusu: "Pullback yaparsa 15813 gelirmi göreceğiz"
- Belirsiz: EGGUB1.67 ile R250'nin1.618 max risk etiketi farklı araç/varyant veya tolerans farkı olabilir; genel geçersizlik hükmü kurulmadı.
- YORUM: 1879995899432301062 EGGUB değil JANTS'tır; önerideki1.06 de görsel bacaklarıyla uyuşmaz, yaklaşık1.20 olarak düzeltildi. Formüller bu incelemede hesaplandı.

### X241 · 2026-09-01 17:38:47 UTC · ASTOR aracının gösterge ve bölge etiketleri
- Bağlı: R258 (araç parametreleri bağı); Öneri: tema-2 #25 (R258)
- Yazar: T + G (ASTOR grafikleri).
- Kaynak: 2094842420387029311 (2026-09-01 17:38:47 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "WMA Close 21"; "MACD 12 26 9"; "RSI 14 | 70 / 30"; "WT 10 21 | 60 53 -53 -60" — gösterge ayarları — kural tam (parametre).
  - [bölge; G] "DEMAND / TOPLAMA"; "DEMAND / TEST EDİLDİ" — iki bölge durum etiketi; test edilmiş sayılma ölçütü yok — çekirdek belli.
- Örnek ve sonuç: görselden: ASTOR'da test edilmiş demand191.40–192.75; yükselen trend265.50 ve4 temas. R258 XU100 örneğidir; ASTOR fiyat seviyeleri endekse taşınmadı.
- Tansu'nun vurgusu: "Gerçi muazzam da getiri sağladı son dönemde"
- YORUM: Grafik geçmiş yükselişi gösterir; aynı ayarların bütün R258 grafiklerinde kullanıldığına dair kod kanıtı yok.

### X242 · 2024-03-12 23:10:18 UTC · Gann fanı ve EMA200 çakışması
- Bağlı: yeni yöntem; Öneri: tema-2 #26
- Yazar: T + G (kendi işaretlediği grafikler).
- Kaynak: 1767689603035640165 ve 1767689605325684841 (2024-03-12 23:10:18 UTC), 1771838096432099715 (2024-03-24 09:54:56 UTC).
- Fikirler:
  - [teyit-tetik] "3/1 fanına geçiş yapar. Düşüş trendi teyit olur." — SAYAS1/2 fanı,86.275 Fibo desteği kırılırsa3/1; EMA200 bu fanın üst çizgisi — çekirdek belli.
  - [hedef] "8/1 fanından alacağı destek ile ilk hedefin 4,92 ve 5,55 olması gerekir." — Yeşil Yatırım Holding örneği; hedef hesabı yok — yalnız fikir.
- Örnek ve sonuç: görselden:1/8–8/1 açı etiketleri; Yeşil Yatırım fan başlangıcı2023-05-03. SAYAS0.236=86.275. Fan ölçeği, başlangıç seçimi ve stop tanımı yok; sonraki sonuç yok.
- Tansu'nun vurgusu: "Fakat bu alanlar ayı piyasasıdır bunu da söylemek lazım. YTD"
- YORUM: Gann fanı tek başına tamamlanmış işlem sistemi yapılmadı.

### X243 · 2025-02-23 12:21:22 UTC · FVG hassasiyetinin subjektifliği
- Bağlı: R199; Öneri: tema-2 #27 (FVG)
- Yazar: T + G (AKBNK FVG aracı).
- Kaynak: 1893637273029050563 (2025-02-23 12:21:22 UTC); sonraki kullanım kanıtı1989089558164873727 (2025-11-13 21:54:40 UTC, X233), 2002147457422307730 (2025-12-19 22:42:06 UTC, X237).
- Fikirler:
  - [ölçüm-ilkesi] "ben çok sevmiyorum bu işleri aslında. biraz subjektif geliyor bana, hassasiyeti ayarlamak için subjektif değişiklikler yapılması gerekiyor." — hassasiyet seçimine ihtiyat; mekanik evrensel kural değil — çekirdek belli.
- Örnek ve sonuç: görselden: "Toplam 16 FVG bölgesi grafiğe eklendi." AKBNK grafiği. Sonraki araç FVG teması ve Tansu'nun0.618FVG hedef sözü X233/X237'de yer alır.
- Tansu'nun vurgusu: "biraz subjektif geliyor bana"
- Çelişir: R199'un M strateji kartının FVG'yi kesin giriş şartı yapan anlatımıyla Tansu'nun kendi hassasiyet ihtiyatı gerilim taşır; T sözü daha güçlüdür. Bu kayıt FVG kullanımını tamamen reddeden kural değildir.
- Belirsiz: Yanıt verilen üst gönderi1893635723439268180 OB/kodlama der, Tansu görseli FVG'dir. "bu işler" OB/FVG ailesine veya özel hassasiyet ayarına işaret edebilir. Sonraki kullanım görüş değişimi veya kullanırken ihtiyatın devamı olabilir.

### X244 · 2025-05-27 19:59:43 UTC · ATR dip/tepe bölgeleri ve train/test açıklaması
- Bağlı: R172 / R111; Öneri: tema-2 #27 (ATR)
- Yazar: T (kendi algoritmasına verilen yanıta açıklama) + M biçimli düzenleme + G.
- Kaynak: 1927454690960101506 (2025-05-27 19:59:43 UTC); mekanizma açıklaması1911038743839900154 (2025-04-12 12:48:36 UTC, X212), sinyal uyarısı1909002131635331358 (2025-04-06 21:55:50 UTC, X211).
- Fikirler:
  - [bölge] "Dip ➡️ Alım bölgesi"; "Tepe ➡️ Satış bölgesi" — ATR algoritmasının bölge yorumu — çekirdek belli.
  - [ölçüm-ilkesi] "Biz burada train/test bölmedik çünkü neyi neye karşı test edeceğiz?" — bu örnekte model eğitmediğini söyler; bütün sistemlerde sınamadan vazgeçme kuralı değil — yalnız fikir.
- Örnek ve sonuç: grafik etiketlemesi; bağımsız işlem performansı yok.
- Tansu'nun vurgusu: "Biz model eğitmedik kardeşim,"
- Belirsiz: R172'nin tepe/dip yakalamayı amaçlamama vurgusu gelecekteki uç noktayı tahmin etmeme veya her türlü dip girişini reddetme olarak okunabilir. X212 dip ancak dönüşten sonra onaylanır der; ilk okuma bağlam farkıyla uyumludur. R111 backtest/forward test çağrısıdır; burada train/test bölmemek bu çağrıyı tek başına çürütmez.
- YORUM: ATR kullanmanın optimizasyon/overfitting riskini otomatik dışladığı iddiası kanıt değildir; bu kayıtta benimsenmiş teknik hüküm yapılmadı.

### X245 · 2023-09-30 08:05:45 UTC · Değerleme ağırlıklarının tarihçesi
- Bağlı: R151 / R068; Öneri: tema-2 #27 (değerleme)
- Yazar: T (eski ağırlık ve2026 yöntem/gerekçe) + M (2025 başlıklı yöntem anlatımı) + G (TTRAK değerleme tablosu).
- Kaynak: 1708030356564160854 (2023-09-30 08:05:45 UTC), 1769794170590245323 (2024-03-18 18:33:06 UTC), 1780322528658886674 (2024-04-16 19:49:02 UTC), 1787051924061118650 (2024-05-05 09:29:15 UTC), 1913527179364765803 (2025-04-19 09:36:45 UTC), 2084757098529693800 (2026-08-04 21:43:19 UTC), 2084997818570182832 (2026-08-05 13:39:51 UTC).
- Fikirler:
  - [temel-değerleme; T] "Çarpanlar %40, İNA %60 ağırlıklandırılarak" —2023-09 eski sürüm;2024-04 BRISA açıklaması da çarpan%40/İNA%60 — kural tam (tarihsel ağırlık).
  - [temel-değerleme; T] "En sonunda bu ortalamanın %60'ını, DCF'in de %40'ını alırım." — güncel%60 çarpan/%40DCF-İNA;2025-04 M açıklamasında da60/40 var — kural tam (T ağırlık sözü).
- Örnek ve sonuç: görselden:2023/4Ç TTRAK tablosu çarpan1620.53, İNA1486.14, birleşik1539.90. Eski40/60 hesabı1539.896≈1539.90;60/40 hesabı1566.774≈1566.77. Mart/Mayıs2024 aynı tablo paylaşımı yeni hesap sürümü kanıtı değildir. Gerçek getiri değil değerleme hesabıdır.
- Tansu'nun vurgusu: "Dcf çok subjektif, o nedenle payını düşük tutma taraftarıyım"
- YORUM: Geçiş2024-04 ile2025-04 arasındadır; kesin değişim günü yok. R068/R151 güncel60/40 ile uyumludur. Eski40/60 "ters" veya kod hatası diye yazılmadı. Kaynak tarihleri paylaşım tarihidir; aynı bilançonun farklı sürümlerde değerlendirilmesi mümkündür.

### X246 · 2025-02-20 18:21:50 UTC · Harmonik paylaşım kapsamının değişmesi
- Bağlı: R009 / R024; Öneri: tema-2 #27 (destek/direnç)
- Yazar: T.
- Kaynak: 1892640823361098050 (2025-02-20 18:21:50 UTC); sonraki harmoniğe bölge ekleyen araçlar2089770598620713304 (2026-08-18 17:45:11 UTC), 2090515278199136740 (2026-08-20 19:04:16 UTC, X202).
- Fikirler:
  - [tarama-evren] "Ben destek direnç vs vs bakmam. Gartley butterfly çıkarsa veririm." —2025 paylaşımının kapsamı; alıcının ayrıca analiz etmesi istenir — çekirdek belli.
- Örnek ve sonuç: daha sonra CCOLA/KUYAS harmonik+demand/supply grafikleri; sonuç X202'de kayıtlıdır, yeniden başarı örneği üretilmedi.
- Tansu'nun vurgusu: "Lütfen grafiğe iyi çalışın. Hata yapmayın."
- Belirsiz: R009/R024 bölge ve destek/dirence bakmayı anlatır.2025'te ham tarama paylaşımı ile2026'da ayrıntılı analiz farklı kapsamlar veya yöntem gelişimi olabilir; sürekli destek/direnç reddi çıkarılmadı.
- YORUM: Tansu'nun kendi sözü iki dönemde de korunur; yalnız tarih sırasından önceki söz geçersiz sayılmaz.

### X247 · 2025-07-31 15:00:23 UTC · Elliott C yerine üçüncü itkiyi tarama tercihi
- Bağlı: R199 / R261; Öneri: tema-2 #27 (Elliott)
- Yazar: T.
- Kaynak: 1950934573468025012 (2025-07-31 15:00:23 UTC).
- Fikirler:
  - [tarama-evren] "Elliot C taraması değil, 3.itki dalgası taraması yapın." — C taraması yerine üçüncü itki tercihi; tarama mekanizması örnekleri X220'de — çekirdek belli.
- Örnek ve sonuç: "Getirileri daha iyi." iddiası var; karşılaştırma örneklemi, dönem ve sayısal getiri yok.
- Tansu'nun vurgusu: "Getirileri daha iyi."
- Çelişir: R199'un M kartındaki C/FVG bölgesine limit alış yaklaşımı ile Tansu'nun kendi tarama tercihi ayrışır; T sözü daha güçlüdür. M kartından C girişinin Tansu'nun tek tercihi olduğu sonucu alınmaz.
- Belirsiz: Tarama tercihi ile bütün girişleri yasaklama farklıdır. R261'in T metni bölgede agresif ve direnç kırılımında muhafazakâr girişi birlikte kabul eder; bağlam farkı veya değişen tercih olabilir.

### tema-2 özeti

| X no | başlık | bağlı R | olgunluk | yazar |
|---|---|---|---|---|
| X201 | Günlük/haftalık yatay kanal | R246 / R082 | çekirdek belli | T + M + G |
| X202 | Harmonik TP ve stop konumu | R203 / R222 / R014 | çekirdek belli | T + G |
| X203 | Fincan hedefi ve retest | R114 | çekirdek belli | T + M + G |
| X204 | Altı mum formasyonunun koşulları | yeni yöntem | çekirdek belli | T + M + G |
| X205 | Harmonik kart okuma ve oran ayrışması | R008 / R075 / R222 / R203 | çekirdek belli | T + G |
| X206 | Bir yıllık Fibo/EMA hesabı | R217 | kural tam (hesap) | T + G |
| X207 | Proximal renk/gap | R037 | kural tam (çizgi) | T |
| X208 | Engulfing ölçümü ve rejection | R023 / R171 | çekirdek belli | T + M + G |
| X209 | Haftalık TOBO | R219 | çekirdek belli | T + M + G |
| X210 | RSI üzerine Fibo | yeni yöntem | çekirdek belli | M |
| X211 | Level1/2 dip taraması | yeni yöntem | çekirdek belli | T + G |
| X212 | ATR dibi ve kurum yoğunlaşması | R039 / R221 | çekirdek belli | T + M |
| X213 | RSI trendi ve Belt Hold | R208 | çekirdek belli | T + M + G |
| X214 | EMA sıkışması/yükselen üçgen | R127 | çekirdek belli | T + M + G |
| X215 | X–B aşağı/A yukarı kırılımı | R013 / R014 | çekirdek belli | T + G |
| X216 | Temas ve kanal ölçümleri | R214 / R245 | çekirdek belli | T + G |
| X217 | R4/S4 ve haftalık pivot | R191 | kural tam (R4/S4 hesabı) | T + G |
| X218 | KDE50/100 | R128 | çekirdek belli | T + G |
| X219 | Harmonik tür menüsü | R008 / R011 | çekirdek belli | T + G |
| X220 | Elliott3/W5 varyantları | R193 / R205 / R261 | çekirdek belli | T + G |
| X221 | Dip uzaklığı/16 günlük konum | yeni yöntem | çekirdek belli | T + G |
| X222 | EMA26/ATR14 bant hesabı | yeni yöntem | kural tam (hesap) | T + G |
| X223 | CDL ve tek mumlar | R143 | çekirdek belli | T + M + G |
| X224 | Kanal/ortalama türevleri | R039 / R053 | çekirdek belli | T + M + G |
| X225 | Takoz kartı | R006 | çekirdek belli | T + G |
| X226 | Bayrak raporu | R007 | çekirdek belli | T + G |
| X227 | CD şiddeti/zaman sorusu | R016 | yalnız fikir | T |
| X228 | Fibo138.2 uzantısı | R020 | yalnız fikir | T + G |
| X229 | Yüzde5 konfluans örneği | R040 | çekirdek belli | T |
| X230 | HSAR kümeleri | R055 | çekirdek belli | T + G |
| X231 | Teorik/gerçek TridentD | R090 | çekirdek belli | T + G |
| X232 | EMA20/RSI50 uyarısı | R105 | çekirdek belli | T |
| X233 | FVG yüzde temas etiketi | R129 | çekirdek belli | G |
| X234 | Fibo/EMA200 | R149 | çekirdek belli | T |
| X235 | CIMSA trend stop'u | R168 | çekirdek belli | M + G |
| X236 | BB3SS ortalamaya dönüş | R190 | çekirdek belli | T + G |
| X237 | FVG0.618 düzeltme hedefi | R204 | çekirdek belli | T + G |
| X238 | Inverted hammer | R241 | çekirdek belli | M |
| X239 | Medyan1SS fikri | R244 / R001 | çekirdek belli | T |
| X240 | Kelebek/swing varyantları | R250 | çekirdek belli | T + G |
| X241 | ASTOR gösterge ayarları | R258 | kural tam (parametre) | T + G |
| X242 | Gann fanı | yeni yöntem | çekirdek belli | T + G |
| X243 | FVG subjektiflik ihtiyatı | R199 | çekirdek belli | T + G |
| X244 | ATR bölgesi/train-test | R172 / R111 | çekirdek belli | T + M + G |
| X245 | Değerleme ağırlıkları tarihçesi | R151 / R068 | kural tam (T ağırlık sözü) | T + M + G |
| X246 | Harmonik paylaşım kapsamı | R009 / R024 | çekirdek belli | T |
| X247 | Üçüncü itki tercihi | R199 / R261 | çekirdek belli | T |

### tema-2 alınmayanlar

Hiçbir öneri bütünüyle reddedilmedi. Aşağıdaki alt parçalar yinelenme, kaynakta bulunmama veya başka yazar nedeniyle alınmadı; alınan düzeltmeler ilgili X kaydında yer alır.

| öneri no | neden | kanıt id |
|---|---|---|
| #2, SAYAS işlem yönetimini yeniden kayıt | R014'te aynı kaynak, giriş, X stop ve .618AD zaten mevcut; yalnız diğer araçlarla hedef tabanı farkı X202'de tutuldu | 2091220738510332198 |
| #3, GUBRF anlatımını yeniden kayıt | R114'te aynı metin ve sonuç var; sadece eksik hedef tabanı çözümü ve yeni retest örnekleri X203'e alındı | 2047238753366761631 |
| #25 R016, AB süresini bağımsız T kuralı yapmak | "AB bacağı oluşumunda geçen süre" üst gönderi yazarı Cr_Soprano'nun sözü; kendi başına kanıt değil. Tansu'nun onayı ve isimsiz ikinci ölçütü X227'de ayrıldı | 2091053758310470040 / 2091066263594295378 |
| #25 R241, bu id'den RSI pozitif uyumsuzluğu şartı çıkarmak | Kaynak metninde yok; yalnız inverted hammer tanımı ve tespit tarihi alındı | 1910746404265279494 |
| #27, harmonik oran ayrışmasını ikinci kayıt yapmak | #5 ile yinelenen; ALCAR/ARENA/TTKOM/KUYAS ayrışmaları X205'te tek kayıt | 1871623972544274600 / 1888626133933121609 / 1892643772430766103 / 2090515278199136740 |

## Tema 3 — Teyit, giriş, çıkış, boyut-risk

### X301 · 2026-02-13 22:03:55 UTC · Sabit ATR hedef ve stop merdiveni
- Bağlı: R239 / R184; Öneri: tema-3 #2
- Yazar: T (kısa paylaşım ve kullanım vurgusu) + G (ASTOR/YAPRK araç tabloları).
- Kaynak: 2022431570012106899 (2026-02-13 22:03:55 UTC), 2045421697814126693 (2026-04-18 08:38:29 UTC).
- Fikirler:
  - [hedef-çıkış; G] "SABİT HEDEFLER VE STOP SEVİYELERİ (1-20 ATR)" — girişteki ATR(14) ile hedef_n = giriş + n×ATR; ASTOR tablosunda n=1..20 — kural tam.
  - [stop-geçersizlik; G] "Stop her zaman YUKARI hareket eder, aşağı inmez" — başlangıç stopu giriş−1,5×ATR; 1 ATR hedefinde başlangıç stopu korunur; n≥2 için stop giriş+(n−2)×ATR; stop geri indirilmez — kural tam.
  - [hedef-çıkış; G] "3 ATR'ye ulaşınca %50 satış yapın" — 3 ATR'de yarı satış; kalan pozisyonun stopu 1 ATR seviyesine çıkar — kural tam.
- Örnek ve sonuç: görselden: ASTOR giriş 2026-02-03, 155,00 TL, ATR(14) 7,56 TL, başlangıç stopu 143,66 TL; 12 Şubat 3 ATR hedefi 177,67 TL, ulaşılan fiyat 183,40 TL, %50 satış; 13 Şubat 4 ATR hedefi 185,23 TL, ulaşılan fiyat 189,10 TL, kâr %22,00, aktif stop 170,11 TL, pozisyon açık (%50). YAPRK tablosu giriş tarihi 2026-03-16, giriş 15,05 TL, ATR 1,27 TL, stop 13,15 TL; 18 Nisan paylaşımı bu tarihli tabloyu taşır. Bunlar araç çıktılarıdır, gerçekleşmiş emir kaydı değildir.
- Tansu'nun vurgusu: "Listelerde uygulanacak stop ve kar alma sistemi."
- Belirsiz: YAPRK görseli "BUGÜN GİRİŞ" derken giriş tarihi 16 Mart, gönderi tarihi 18 Nisan'dır; eski örnek tablo veya güncellenmemiş tarih etiketi olabilir. ASTOR 20 ATR hedefi 306,14 TL, gösterilen yuvarlak ATR ile hesap 306,20 TL; YAPRK 1 ATR kârı %8,42, gösterilen ATR ile yaklaşık %8,44. Gizli hassasiyet veya hesap farkı kaynakla kesin ayrılamaz.
- YORUM: Önerinin `(n−2) ATR` kuralı ilk basamağa uygulanamaz. R239'daki 1,5 ATR sonrası önceki gün düşüğüyle yarı satış, R184'teki 2 ATR acil stop ve buradaki sabit merdiven ayrı düzenlerdir; tek bir evrensel stop katsayısı veya tarihçe değişimi olarak birleştirilmez.

### X302 · 2024-10-01 21:02:11 UTC · RoC50, ADX/ADXR ve OBV birleşimi
- Bağlı: yeni yöntem (R137 çoklu teyit; R196 OBV ile ilgili bağ); Öneri: tema-3 #3
- Yazar: T + G (DGATE gösterge grafiği).
- Kaynak: 1841222101497246009 (2024-10-01 21:02:11 UTC), 1841228866234601958 (2024-10-01 21:29:04 UTC), 1841235974430273798 (2024-10-01 21:57:19 UTC), 1841955633047670978 (2024-10-03 21:36:59 UTC), 1842064079826936219 (2024-10-04 04:47:55 UTC).
- Fikirler:
  - [teyit-tetik] "RoC50 son gün 0 eksenini yukarıya kessin"; "OBV SMA20'yi yukarıya kessin" — RoC periyodu 50; OBV'nin kendi SMA20'sini yukarı kesmesi — kural tam.
  - [giriş] "ADX > ADRX (geçmişte bir zaman kesmiş olsun ve hala yukarıda olsun ya da son gün kesmiş olsun)" — kaynakta ADRX yazılmış; görselden: ADX(14)/ADXR(14), ADX üstte; önceki veya son gün kesişimi kabul edilir — kural tam.
  - [hedef-çıkış] "ADX, ADXR'yi aşağıya kesince pozisyondan çıkın." — aşağı kesişimde çıkış; yukarı kesişimin 20 üzerinde olması tercih — kural tam.
- Örnek ve sonuç: görselden: DGATE, RoC 50 Gün, ADX(14), ADXR(14), OBV ve OBV SMA20. Metinde 7 Eylül gibi koşulların olgunlaştığı, 20 Eylül gibi trend ve para girişinin zayıfladığı anlatılıyor; kesin emir fiyatı/getiri yok.
- Tansu'nun vurgusu: "Favori sistemim"; "Bactestinizi yapın."
- YORUM: "ROC>50" önceki yazımını Tansu "Roc50 > 0 olmalı. Yanlış yazmışım yukarıda." diye düzeltmiştir; 50 gösterge periyodudur, getiri eşiği değildir. Pusuda bekleme anlatısı ile 3 Ekim birleşik tarama koşulları ayrı ifadeleriyle korunur; RoC ve OBV'nin mutlaka aynı gün kesmesi dışındaki ek sıra kaynakta yok.

### X303 · 2025-11-16 10:27:50 UTC · RSI30 işleminde direnç reddi ve başa baş çıkış
- Bağlı: R233 / R239; Öneri: tema-3 #5
- Yazar: T (16 ve 20 Kasım kısa takip notları) + M (21 Kasım başlıklı, maddeli üç senaryo gönderisi; 23 Kasım başa baş açıklaması).
- Kaynak: 1990003872023130607 (2025-11-16 10:27:50 UTC), 1991558168149987328 (2025-11-20 17:24:03 UTC), 1991721699922870638 (2025-11-21 04:13:52 UTC), 1992547498343161903 (2025-11-23 10:55:18 UTC).
- Fikirler:
  - [hedef-çıkış; M] "Fiyat 50 RSI seviyesini reddederse."; "Fiyat 50 SMA ortalamasını reddederse."; "1.5 ATR kârdayken, önceki günün düşüğünün altında kapanış gelirse." — üç ayrı %50 çıkış tetiği; RSI50 reddi, SMA50 reddi veya 1,5 ATR kâr sonrası önceki gün düşüğü altı kapanış — çekirdek belli.
  - [hedef-çıkış; M] "Bu 3 senaryodan herhangi ikisi gerçekleşirse işlemin tamamını kapatın." — üç tetikten herhangi ikisi, tam çıkış — çekirdek belli.
  - [stop-geçersizlik; M] "Gün sonunu beklemeye gerek yoktur; fiyat giriş seviyesine geri döner dönmez çıkış yapılır." — Under 30 Over 30 işleminde önce 1,5R lehte ilerleme, ardından girişe dönüşte başa baş çıkış; R başlangıç stop mesafesi olarak anlatılır — çekirdek belli.
- Örnek ve sonuç: 20 Kasım notu RSI30 sonrası SMA50/RSI50 ilk temasını anlatır; kesin işlem sonucu yok. 1,5R ile 1,5 ATR aynı birim olarak kullanılmaz.
- Tansu'nun vurgusu: ayrı T cümlesi yok ("Arada bu kardeşinizi dinleyin." M biçimli 21 Kasım gönderisinin son satırıdır). RSI50/SMA50 reddi T notunda da geçer (1990003872023130607).
- Belirsiz: RSI50/SMA50 "reddi" için iğne, kapanış veya kaç bar gerektiği tanımlanmıyor; direnç teması sonrası dönüş veya kapanışla geri kayıp olarak okunabilir. İki tetiğin aynı bar içinde mi, işlem boyunca mı birikeceği de belirtilmiyor.
- YORUM: R233'te 50 dirençleri aşıldıktan sonraki RSI70 yarı satışı vardır; burada 50 dirençlerinde başarısızlık ele alınır. Başa baş çıkış, R233'te açık kalan iz süren stop oranını tek başına doldurmaz.

### X304 · 2024-04-23 22:19:07 UTC · Bollinger 3 SS temasından zıt mumla dönüş
- Bağlı: R053; Öneri: tema-3 #6
- Yazar: T.
- Kaynak: 1782897014444818512 (2024-04-23 22:19:07 UTC), 1846648064695848972 (2024-10-16 20:23:02 UTC), 1846989330382041324 (2024-10-17 18:59:06 UTC).
- Fikirler:
  - [teyit-tetik] "BB 3 SS ile tepe ya da dip banda dokunup hemen sonraki ki mum zıt renk yakarsa harika bir işaret olur." — 3 standart sapmalı BB; bant teması ve hemen sonraki zıt renkli mum — çekirdek belli.
  - [giriş] "Günlükte, 3SS BB bir önceki gün alt banda iğne atıp son gün yeşil kapatsın." — günlük; önceki gün alt banda iğne, son gün yeşil kapanış — çekirdek belli.
- Örnek ve sonuç: 16 Ekim metninde AFYON izleme örneği; 17 Ekim taramasında tek hisse çıktığı söyleniyor, metinde sembol yok. Gerçekleşmiş işlem sonucu yok.
- Tansu'nun vurgusu: "3SS BB ve zır mum kapanış."; "En sevdiğim."
- Belirsiz: BB periyodu ve iğnenin banda temas mı, bandın dışına taşma mı gerektirdiği yok; iki okuma ayrılmıyor.
- YORUM: Bu dönüş düzeni R053'ün kuyruk/ortalamaya dönüş tarafına bağlıdır. Trendde üst bant üstü kapanışı takip eden Keltner düzeni (X320) bunun yerine geçirilmez; SS ile R053 kitap görselindeki SE aynı ölçü değildir.

### X305 · 2025-04-15 14:31:29 UTC · RSI üzerinde 144 günlük Fibonacci dönüşü
- Bağlı: yeni yöntem; Öneri: tema-3 #7
- Yazar: M (144 günlük 0.786/0.618 yöntem açıklamaları ve XU100 analizi) + T (kısa uygulama notları) + G.
- Kaynak: 1912151798992814185 (2025-04-15 14:31:29 UTC), 1912933957592834220 (2025-04-17 18:19:30 UTC), 1925626094935236883 (2025-05-22 18:53:32 UTC), 1977450129008251116 (2025-10-12 19:03:44 UTC), 1986917436310909146 (2025-11-07 22:03:26 UTC).
- Fikirler:
  - [giriş; M] "RSI bu seviyeden destek alıp yukarı dönmeli. Bir önceki güne göre artış göstermeli." — son 144 gün RSI min/max; seviye=maxRSI−oran×(maxRSI−minRSI); 0.618'den dönüş ve günlük RSI artışı — çekirdek belli.
  - [teyit-tetik; M] "Fiyat 50 günlük ortalamanın üzerindeyse daha sağlam zemin demektir." — çekiç/yutan boğa/sabah yıldızı ve fiyatın 50 günlük ortalama üstü olması destekleyici teyit; zorunlu kapı diye yazılmıyor — çekirdek belli.
  - [stop-geçersizlik; M] "Genelde son düşük seviyenin yüzde 2-3 altına stop koyarız." — stop son fiyat düşüğünün %2–3 altı; 0.786 sürümünde 1–2 mumla teyit, çıkış RSI50–60 bandı veya önceki kısa vadeli direnç — çekirdek belli.
- Örnek ve sonuç: görselden: FLAP 10 Ekim 2025 grafiğinde 0.618=43,8, 0.786=33,7, BELTHOLD etiketi; XU100 RSI(14) grafiğinde max 79,4, min 32,9, 0.618=50,7, 0.786=42,9, 0.382=61,6. Kasım metni 0.382 reddi ile zirve mumunu risk uyarısı sayıyor; sonraki gerçekleşmiş işlem sonucu yok.
- Tansu'nun vurgusu: "RSI 786 dönüşü mum formasyonları daha ne olsun:)"
- Belirsiz: Dönüş için seviyeye temas toleransı yok; doğrudan temas sonrası artış veya seviyeyi yeniden aşma olarak okunabilir. 50 günlük ortalamanın SMA/EMA türü açıklanmıyor.
- YORUM: Önerinin "tam" olgunluğu M metin için çekirdek belli olarak düzeltildi. "Daha sağlam" desteği zorunlu fiyat filtresine çevrilmedi; 0.618 ve 0.786 sürümleri tek giriş eşiği değildir.

### X306 · 2025-04-13 16:52:20 UTC · Death Cross uyarısı
- Bağlı: yeni yöntem; Öneri: tema-3 #8 (yalnız Death Cross; Golden Cross kısmı X018'de yinelenen)
- Yazar: M (başlıklı Death Cross açıklaması) + G.
- Kaynak: 1911462470763360258 (2025-04-13 16:52:20 UTC).
- Fikirler:
  - [teyit-tetik; M] "Death Cross = EMA 50 çizgisinin, EMA 200 çizgisinin altına düşmesi" — EMA50'nin EMA200'ü aşağı kesmesi; pozisyon kapatma veya yeni alımdan kaçınma seçenekleri — çekirdek belli.
  - [teyit-tetik; M] "Tek başına bir sinyal her zaman yeterli değildir." — başka analizlerle destek; zorunlu birleşim ve sayısal teyit yok — yalnız fikir.
- Örnek ve sonuç: görselden: EMA50 turuncu, EMA200 siyah noktalı; sağ uçta iki çizgi yakınlaşır. Sembol ve tarihler görünmüyor. Metin Şubat sonu kesişimi ve sonraki düşüşü anlatıyor; bu tarihle kesişim görselden doğrulanamadı.
- Tansu'nun vurgusu: Ayrı bir kısa T cümlesi yok; M açıklamasını kendi işlem kararı olarak atfetmek mümkün değil.
- Belirsiz: Metin gerçekleşmiş aşağı kesişim der; açılan görselde çizgiler sağ uçta yakınlaşır, belirgin geçmiş aşağı kesişim seçilmez. Kırpılmış/başka örnek görsel veya metin–görsel uyuşmazlığı olabilir.
- YORUM: Golden Cross ve fiyat EMA200 ön taraması X018/X032'de bulunduğu için tekrarlanmadı. M anlatının seçenekleri zorunlu SAT talimatına çevrilmedi.

### X307 · 2024-10-31 14:14:16 UTC · SuperTrend ve son gün EMA5/EMA20 kesişimi
- Bağlı: yeni yöntem (R148 HalfTrend + momentumdur; X024 farklı SuperTrend varyantlarıdır); Öneri: tema-3 #9
- Yazar: T.
- Kaynak: 1851991078661976137 (2024-10-31 14:14:16 UTC), 1852057966960349695 (2024-10-31 18:40:03 UTC), 1852060552413221135 (2024-10-31 18:50:19 UTC).
- Fikirler:
  - [giriş] "Son gün supertrend bullish olan ve 5EMA 20EMA'yı yukarıya kesen hisse." — son gün SuperTrend bullish dönüşü ile EMA5/EMA20 yukarı kesişimi birlikte — çekirdek belli.
  - [teyit-tetik] "EMA5 EMA20'yi son gün yukarı kesiyor ama supertrend zaten bullish yönünde. Yani son gün bullish olmuyor." — ayrı varyantta SuperTrend önceden bullish; EMA kesişimi son gün — çekirdek belli.
- Örnek ve sonuç: INVEO ve KGYO, grafikleri net gelmediği için sonraki listeden çıkartılmış; doğrulanmış örnek sayılmaz. İşlem sonucu yok.
- Tansu'nun vurgusu: "Bence daha sağlam sinyal bu."; "Altını çizeyim her iki koşulda son gün sağlanıyor."
- Belirsiz: SuperTrend ATR periyodu ve çarpanı yok. İlk mesajdaki son gün bullish ifadesi yalnız mevcut yön veya o gün yön değişimi okunabilir; sonraki "Yani son gün bullish olmuyor" açıklaması ikinci varyantı açıkça ayırır.

### X308 · 2024-08-24 13:44:15 UTC · Vegas girişine ATR kâr alma fikri
- Bağlı: yeni yöntem (X010 Vegas girişinin çıkış eki); Öneri: tema-3 #10 (yalnız çıkış ek bilgisi)
- Yazar: T.
- Kaynak: 1827341150908543159 (2024-08-24 13:44:15 UTC), 1848385592771424616 (2024-10-21 15:27:21 UTC), 1848803496893558928 (2024-10-22 19:07:57 UTC), 1851726487855972606 (2024-10-30 20:42:52 UTC).
- Fikirler:
  - [hedef-çıkış] "Kar al'ı ise ATR ile yapabilirsiniz." — günlük Vegas için ATR kullanma önerisi; ATR periyodu, çarpanı, hedef başlangıcı ve satış oranı yok — yalnız fikir.
- Örnek ve sonuç: Günlük Vegas tarama metinlerinde SKTAS, FRIGO/IHAAS ve BASCM; gerçekleşmiş işlem getirisi yok. EMA12'nin EMA144/169 tünelini yukarı kesmesi X010'da zaten vardır; burada yeni giriş kaydı olarak tekrarlanmadı.
- Tansu'nun vurgusu: "VE ilk göz ağrımız VEGAS"
- Belirsiz: ATR sabit hedef mesafesi veya iz süren stop/kâr alma düzeni olarak kullanılabilir; kaynak hangisi olduğunu söylemiyor.
- YORUM: X010'da olmayan ATR çıkış fikri alındı; belirsizliğinden dolayı önerinin tamamı elenmedi. EMA13 dizilimi, EMA12 kesişiminin yerine geçirilmez.

### X309 · 2025-05-22 19:21:38 UTC · Range kırılımı ve mumla teknik teyit
- Bağlı: yeni yöntem (R082 konsolidasyonla ilgili bağ); Öneri: tema-3 #11
- Yazar: T ("range = 30" kısa notu) + M (DITAS yöntem ve haftalık teknik onay açıklaması; 1 Haziran gönderisinin son satırı T kişisel not) + G.
- Kaynak: 1925633169694277851 (2025-05-22 19:21:38 UTC), 1926353549723590759 (2025-05-24 19:04:10 UTC), 1929184555816419717 (2025-06-01 14:33:35 UTC).
- Fikirler:
  - [giriş; M] "Son günün en yüksek fiyatı ve kapanışı, 60 günlük zirveyi geçiyorsa sinyal kabul edilir." — 60 günlük range high/low; son bar yüksek ve kapanışı zirve üzerinde; aynı barda talib bullish mum, örnekte CDLBELTHOLD — çekirdek belli.
  - [teyit-tetik; M] "Formasyonun geçerliliği için sonraki gün hacim ve fiyat teyidi önemlidir." — sonraki gün izleme; kesin hacim/fiyat eşiği yok — çekirdek belli.
  - [teyit-tetik; M] "Son haftada, hissenin haftalık kapanış ve tepe fiyatı, önceki X haftalık zirveyi aştıysa" — ayrı haftalık X penceresi; günlük MACD, EMA, aşırı alımda olmayan RSI/Stochastic, OBV ve mum teyitleri — çekirdek belli.
- Örnek ve sonuç: DITAS 60 günlük kırılım örneği; yfinance veri aralığı 01.01.2024–24.05.2025, çizilen grafik son 180 gün. Kaynak kodun henüz bitmediğini söylüyor. Sonraki işlem sonucu yok.
- Tansu'nun vurgusu: "range = 30"; "Bu hisse aynı zamanda faz2 alanında bir momentum hissesi;)"
- Belirsiz: 60 günlük zirve hesabının son barı hariç tutup tutmadığı yok; önceki 60 bar veya son bar dahil rolling pencere okunabilir. Haftalık X sayısı ve "range = 30" notunun birimi yok.
- YORUM: M açıklamanın olgunluğu kural tam değildir. Günlük 60, birimsiz 30 ve haftalık X aynı pencereye birleştirilmez.

### X310 · 2025-11-08 19:00:59 UTC · Kanal kırılım çıktıları ve daralan yapı ayrımı
- Bağlı: R124 / R247; Öneri: tema-3 #12
- Yazar: T (kısa grafik notları) + G (60/90/150 bar araç çıktıları).
- Kaynak: 1987233906827903088 (2025-11-08 19:00:59 UTC), 2011135212382761149 (2026-01-13 17:56:14 UTC), 2016954643394216029 (2026-01-29 19:20:34 UTC), 2023815727309091176 (2026-02-17 17:44:04 UTC), 2097063290224431474 (2026-09-07 20:43:44 UTC).
- Fikirler:
  - [teyit-tetik; G] "60 Barlık Kanal"; "150 Barlık Kanal" — tarama penceresi; direnç/eğim, kırılım tarihi ve fiyatı çıktı alanlarıdır; kanal hesabı tanımlı değil — çekirdek belli.
  - [teyit-tetik; G] "RETEST + TUTUNDU" — 60 bar TLMAN çıktısında kırılım sonrası geri sınama/tutunma etiketi; hesap toleransı yok — çekirdek belli.
- Örnek ve sonuç: görselden: DITAS 60 bar, kırılım 2025-11-07 @32,26, direnç 30,22, eğim −0,248. BRYAT 13 Ocak 60 bar, fiyat 2.340,00, direnç 2.257,17, eğim −10,576; üst sınır düşer, alt sınır yükselir (daralan yapı). ARCLK 150 bar, kırılım 19 Ocak @114,30, analiz 20 Ocak; iki sınır düşer. 17 Şubat BRYAT 90 gün başlığı altında üst düşen/alt yükselen daralan yapı. TLMAN 60 bar, kırılım 24 Ağustos @84,85, direnç 80,16, fark +%5,85, üst/alt eğimler −%0,627/−%0,542 bar başına, temas Ü/A=3/3; retest+tutunma. İşlem getiri kaydı yok.
- Tansu'nun vurgusu: "Güzel bir marubozu ama hacim mumu bunu pek teyit etmedi. Siz bilirsiniz."
- Belirsiz: 17 Şubat BRYAT görseli kırılımı 2026-02-10, son tarihi 2026-02-17 yazarken "1 gün önce" der. Takvim farkı veya farklı bar/zaman etiketi olabilir; bir gün sonra raporlama genel kuralı çıkarılamaz.
- YORUM: ARCLK 150 bar görselinde (2016954643394216029) iki sınır düşer, üst sınır daha diktir (aralık daralır, düşen kama). Öneri belgesi daralan örnek olarak 2016967838120964296 ve 2023815727309091176'yı verir; 2016967838120964296 bu kayda alınmadı. Araç başlığı şeklin geometrisinin yerine geçmez.

### X311 · 2025-07-01 18:39:23 UTC · Üç ayrı hacim karşılaştırması
- Bağlı: R124; Öneri: tema-3 #13
- Yazar: T (1 Temmuz örneği) + M (27 Temmuz öneri ve 18 Ekim cevap biçimli açıklama).
- Kaynak: 1940118051640197615 (2025-07-01 18:39:23 UTC), 1949509666456650215 (2025-07-27 16:38:19 UTC), 1979546907505545421 (2025-10-18 13:55:35 UTC).
- Fikirler:
  - [teyit-tetik] "Son gün hacim bir önceki gün hacminin 1.5 katına çıkmış" — tek örnekte önceki güne göre 1,5 kat; para girişi pozitif, faz1 — çekirdek belli.
  - [teyit-tetik; M] "Örneğin 5 gün ortalamasına göre hacim > 1.5 kat mı?" — ayrı öneri, son beş gün ortalamasının 1,5 katından fazla hacim; RSI>50 ve MACD/20 gün düşen testi eşlik edebilir — çekirdek belli.
  - [teyit-tetik; M] "Breakout anında hacmin ortalamanın en az 2-3 katı olması lazım." — Qullamaggie tarzını yorumlayan cevap; ortalama periyodu yok — çekirdek belli.
- Örnek ve sonuç: İlk gönderi 1,5 kat hacmi bir hissenin gözlemi olarak veriyor; metinde sembol ve sonraki sonuç yok. Kullanıcının soru cümlesi kanıt olarak alınmadı; cevap gövdesi M olarak tutuldu.
- Tansu'nun vurgusu: "para girişi pozitif, göstergeler şahane, momentum alanı faz1 de..."
- YORUM: İlk gözlemden evrensel `≥1,5×önceki gün` kapısı türetilemez. Önceki gün, beş gün ortalaması ve periyodu belirsiz ortalama üç ayrı paydadır; öneride aynı kesinlikte yazılmaları düzeltildi.

### X312 · 2025-03-27 18:50:43 UTC · Gizli ve klasik RSI uyumsuzluğunu ayrı okuma
- Bağlı: R116 (gizli pozitif) / yeni yöntem (klasik pozitif seçim filtreleri); Öneri: tema-3 #14
- Yazar: T (kısa notlar) + G (ASELS grafiği ve Tansu'nun paylaşımındaki mesaj ekranı); 21 Nisan açıklaması M biçimli.
- Kaynak: 1905331669092950235 (2025-03-27 18:50:43 UTC), 1910400582935847408 (2025-04-10 18:32:47 UTC), 2043792925209817159 (2026-04-13 20:46:19 UTC), 2046663429478330488 (2026-04-21 18:52:41 UTC).
- Fikirler:
  - [teyit-tetik; G] "Hidden Bullish Divergence" — ASELS grafiğinde fiyat yükselen dipler, RSI alçalan dipler; R116'nın göstergesiz tanımına RSI örneği — çekirdek belli.
  - [teyit-tetik; G] "RSI 30 altında ilk dip yapmış, dipte RSI daha yüksek ama fiyat daha düşük," — klasik pozitif uyumsuzluk: ilk RSI dip<30, ikinci fiyat dip daha düşük/RSI dip daha yüksek; ikinci dipte hacim artışı, yeşil mum (özellikle engulfing/hammer), EMA8 yukarı kırılım — çekirdek belli.
  - [teyit-tetik; G] "Dipler arasında yeterli süre olsun. 3-5 gün gibi değil, idealde 2-6 hafta arası daha anlamlıdır." — komşu dip aralığı; küçük RSI farkı, 2–3 günlük dip mesafesi, yatay/zayıf yapı, kırılan destekler ve zayıf RSI'dan kaçınma — çekirdek belli.
  - [ölçüm-ilkesi; M] "Genellikle 10 ile 30 bar arası mesafeler en sağlıklı sinyali verir." — 70+ barı yeni trend/yapı değişimi olarak yorumlar; 13 Nisan T metninde günlük grafik, gözle iki yıla kadar geriye bakış — çekirdek belli.
- Örnek ve sonuç: görselden: Mart ASELS fiyat ve RSI pivot çizgileri, "Min Slope"/"Max Slope" etiketleri; Tansu kısa trade yaptığını söylüyor, getiri yok. Nisan mesaj ekranında tarama son dipten geriye dört ay; tüm uyumsuzluk tarihlerinin listesi geliyor. İki yıl gözle inceleme penceresi, iki dip aralığı değildir.
- Tansu'nun vurgusu: "hidden bullish"; "günlük bakıyorum genelde 2 seneye kadar geriye bakıyorum göz ile de graifkleri inceliyorum"
- Belirsiz: Mesaj ekranındaki yazar adı görünmüyor; gönderi "bununla ilgili detaylı açıklamaları grupta yazdım" diyerek sahipleniyor. Bu yüzden ekran G kanıtıdır, ekran cümleleri doğrudan T alıntısı sayılmadı. 2–6 hafta ve 10–30 bar yakın ölçüler olabilir; aynı işlem günü takvimi açık değil.
- YORUM: RSI ilk dip<30, ikinci RSI daha yüksek şartları R116'nın gizli pozitif tanımına eklenmez; klasik ve gizli uyumsuzlukta yönler tersidir. Diğer onaylar EMA8/21, pozitifleşen MACD histogramı ve BB alt bant iğnesi olarak önerilir; otomatik tek birleşik kapı yapılmadı.

### X313 · 2024-04-22 19:51:30 UTC · Basit MOST ve VAR kesişim formülleri
- Bağlı: yeni yöntem (X024 yalnız MOST sinyal listesi); Öneri: tema-3 #15 (Tansu'nun sunduğu basit kesişimler)
- Yazar: T (formüller) + G (Matriks optimizasyon ve test ekranları). Anıl Özekşi adına sunulan kod parçaları alınmadı.
- Kaynak: 1782497478056558995 (2024-04-22 19:51:30 UTC), 1784690075059585046 (2024-04-28 21:04:06 UTC), 1786779842530226293 (2024-05-04 15:28:05 UTC).
- Fikirler:
  - [giriş] "CROSS(MOV(C,OPT1,E),MOST(C,OPT1,OPT2))"; "CROSS(MOST(C,OPT1,OPT2),MOV(C,OPT1,E))" — sırayla AL/SAT; görselden: OPT1 2–30, adım 1, varsayılan 3; OPT2 0,5–5, adım 0,5, varsayılan 2; 290 test — kural tam.
  - [giriş] "Cross(MOV(C,opt1,VAR),MOV(C,opt2,VAR))"; "Cross(MOV(C,opt2,VAR),MOV(C,opt1,VAR))" — VAR ortalamaları yukarı/aşağı kesişimi, 60DK; görselden: OPT1 5–15, OPT2 16–50, ikisinde adım 1, varsayılanlar 5/16; 385 test — kural tam.
  - [giriş] "Cross(Mov(RSI(C,14),5,VAR),50)"; "Cross(50,Mov(RSI(C,14),5,VAR))" — RSI14'ün VAR5 ortalaması ile 50 kesişimi, AL/SAT — kural tam.
- Örnek ve sonuç: görselden: DOAS testinde Overall eğrisi yaklaşık %1.150, Data yaklaşık %350; ekranlarda 2020–2023 tarihleri ve işlem tablosu var. Sonuç optimizasyon/test çıktısıdır; canlı kazanç veya her hissede aynı sonuç değildir.
- Tansu'nun vurgusu: "Basit iyidir."; "Yormayın kendinizi :)"
- YORUM: 1779421690071490990 görseli ve 1783371645224149075 metni "ANIL ÖZEKŞİ" sürümünü belirtir; OTT için ayrıntı kaynağı 1790974588156821797 de doğrudan Anıl Özekşi'yi belirtir. Bu parçalar Tansu'nun kendi kodu diye yazılmadı; alınmayanlar tablosunda ayrıldı. Genel MOST gösterge adı tek başına, açıkça atfedilmiş o sürümlerle aynı kod olduğunu kanıtlamaz.

### X314 · 2025-07-15 10:13:34 UTC · Weinstein yükseliş evresinin 150/200 gün koşulları
- Bağlı: R108; Öneri: tema-3 #16
- Yazar: M (başlıklı dört evre açıklaması).
- Kaynak: 1945064189082599687 (2025-07-15 10:13:34 UTC).
- Fikirler:
  - [rejim; M] "Fiyat hem 150 hem 200 günlük ortalamanın üzerinde"; "150 günlük ortalama, 200 günlük ortalamanın üzerinde"; "200 günlük ortalama yukarı döndü" — ikinci evre için günlük 150/200 ortalamalar; SMA/EMA türü belirtilmiyor — çekirdek belli.
  - [teyit-tetik; M] "Yükseliş günlerinde işlem hacmi güçlü, geri çekilmelerde hacim düşük" — yüksek dip/tepe yapısı ve haftalık yükselişlerde hacim; güç/eğim eşikleri yok — çekirdek belli.
- Örnek ve sonuç: Dipten %25–30, bazen %80 yukarı çıkılmış olabileceği anlatılır; bu genel açıklama örneğidir, belirli hisse sonucu yok.
- Tansu'nun vurgusu: Ayrı T giriş/son cümlesi yok; M anlatının vurgusu Tansu'nun birebir kendi sözü olarak yazılmadı.
- YORUM: R108'deki "X haftalık" ortalamaya zorunlu 150/200 gün eşdeğeri atanmıyor; bu gönderideki ayrı günlük tarif korunuyor. M kaydın olgunluğu çekirdek belli.

### X315 · 2024-03-23 22:42:19 UTC · 20/50 ortalama teyidi ve geri çekilme bölgesi
- Bağlı: R210 (20/50 ortalama teyidiyle bağ; VIX sistemine yeni zorunlu koşul değil); Öneri: tema-3 #17
- Yazar: T.
- Kaynak: 1771668829900357977 (2024-03-23 22:42:19 UTC), 1841922080541180029 (2024-10-03 19:23:39 UTC).
- Fikirler:
  - [teyit-tetik] "20EMA, 50EMA'nın üzerine çıkınca ve onun üstünde 2 gün kapanış yaptığında yine coşku verirsin bize." — EMA20/EMA50 yukarı geçişi ve iki gün kapanış ifadesi; kapanış öznesi açık değil — çekirdek belli.
  - [giriş] "20 MA, 50 MA'nın üzerinde olmalı.Her iki hareketli ortalama yükseliyor olmalı." — MA20>MA50; ikisi yükselir; mesafe büyük ve/veya büyür; geri çekilme MA20'ye ya da en fazla MA20–MA50 arasına — çekirdek belli.
- Örnek ve sonuç: SAYAS için 94 üzerine atmasını beklediği yazılır; gerçekleşmiş sonuç yok.
- Tansu'nun vurgusu: "Biraz momentum artıyor ama yeterince güçlü değil."
- Belirsiz: İlk cümlede "onun üstünde 2 gün kapanış" fiyatın EMA50 üstü kapanışı veya EMA20'nin EMA50 üstünde iki gün korunması olarak okunabilir; fiyat öznesi yazılı değildir. Ekim MA20/MA50'nin SMA/EMA türü de belirtilmiyor.
- YORUM: Önerinin kesin "fiyat EMA50 üstünde iki gün" ifadesi belirsizleştirildi. R210 SMA20/SMA50 ve VIX/Heikin Ashi sistemi ayrı bağlamdır; EMA ve SMA birbirinin yerine geçirilmez.

### X316 · 2025-11-15 11:07:10 UTC · SMA200/250 altında kapanıp ertesi gün geri alma
- Bağlı: R212; Öneri: tema-3 #18
- Yazar: T.
- Kaynak: 1989651383092744703 (2025-11-15 11:07:10 UTC).
- Fikirler:
  - [giriş] "200 yada 250SMA altında iken kapanış, bir gün sonra üzerinde kapanıyor ise ve momentum da yerinde ise bu iyi bir alım fırsatı yaratabilir." — SMA200 veya SMA250; önce altında, ertesi gün üzerinde kapanış; momentum teyidi — çekirdek belli.
- Örnek ve sonuç: Gönderi grafik örneği sunuyor; burada görsel sayısı veya gerçekleşmiş getiri aktarılmadı.
- Tansu'nun vurgusu: "Not al lazım olur"
- Belirsiz: "momentum da yerinde" için gösterge/eşik yok; pozitif momentum veya ayrıca güçlenen momentum olarak okunabilir.
- YORUM: R212'nin 250SMA giriş bileşenini açıklayan geri alma düzenidir; X032 fiyatın EMA200 yukarı kesişimiyle aynı kayıt değildir.

### X317 · 2025-09-03 16:10:00 UTC · EMA13 çevresinde 1–2 ATR ve ani 3 ATR ayrımı
- Bağlı: R128 (ortalama uzaklığıyla bağ); Öneri: tema-3 #19
- Yazar: M (başlıklı 3 ATR risk açıklaması).
- Kaynak: 1963273280581751113 (2025-09-03 16:10:00 UTC).
- Fikirler:
  - [rejim; M] "Fiyat 13 EMA’nın üzerinde kalıp 1 ATR, ardından 2 ATR seviyelerine yavaş yavaş ilerlediğinde" — kademeli yükseliş sağlıklı, ani 3 ATR spike riskli diye yorumlanır; ATR periyodu yok — çekirdek belli.
  - [hedef-çıkış; M] "Kademeli satış, riski azaltır." — 3 ATR civarında mevcut pozisyon için kâr alma düşüncesi; satış oranı yok — yalnız fikir.
  - [giriş; M] "3 ATR’den sonra hemen alım yapmak genellikle dezavantajlıdır." — yeni giriş için geri çekilme/sindirme/denge bekleme; kesin alım yasağı değil — yalnız fikir.
- Örnek ve sonuç: Belirli hisse veya sayısal işlem sonucu yok; EMA13'te tutunmanın devam, EMA altına sert dönüşün tepe olabileceği anlatılıyor.
- Tansu'nun vurgusu: Ayrı bir T cümlesi yok; M metin doğrudan kişisel işlem kuralı sayılmadı.
- Belirsiz: 1/2/3 ATR seviyelerinin EMA13'e eklenen uzaklık mı, başka başlangıca göre ilerleme mi olduğu açık formülle verilmemiştir; EMA13 bağlamı ilk okumayı destekler.
- YORUM: Önerideki kesin "3 ATR=kâr al, yeni alım yok" metnin "olabilir/genellikle" anlatımından daha güçlüdür; fikir olarak düzeltildi. R128'in EMA50/100/200 düzeni EMA13'e dönüştürülmedi.

### X318 · 2025-10-14 17:34:56 UTC · Elliott beşinci dalga hedefinde iki farklı tarif
- Bağlı: R193; Öneri: tema-3 #20
- Yazar: M (14 Ekim uzun açıklama) + T (29 Ekim kısa kod/gelişim notu) + G.
- Kaynak: 1978152557945000041 (2025-10-14 17:34:56 UTC), 1983565377532572092 (2025-10-29 16:03:33 UTC).
- Fikirler:
  - [hedef-çıkış; M] "Elde ettiğiniz bu değeri üçüncü itki dalgasının sonuna eklediğinizde" — önceki cümlelerde C dalgası boyu×0,618; bunun üçüncü itki sonuna eklenmesi — çekirdek belli.
  - [hedef-çıkış; G] "5. Dalga Hedef (W3*0.618): 18.63 TL" — görsel etiketi W3×0,618; mutlak fiyatı üreten başlangıç noktası yok — çekirdek belli.
- Örnek ve sonuç: görselden: AEFES Elliott 1–2–3–4–5 + A–B–C grafiği, hedef 18,63 TL. Tansu metni "18.63 hedef bulmuş algo. gerçekleşen 18.13" der; gerçekleşen değer metin iddiasıdır, hedefe ulaşıldı diye yazılmaz.
- Tansu'nun vurgusu: "Velhasıl nokta atışı olmasa da bşr öngörü veriyor."
- Belirsiz: 14 Ekim C boyu×0,618+üçüncü itki sonu der; 29 Ekim grafik W3×0,618 der. Aynı yöntem için farklı dalga etiketi veya iki ayrı hedef düzeni olabilir; W3 formülünün fiyat başlangıcı gösterilmez.
- YORUM: W3×0,618 yalnız uzunluk verir; ekleme tabanı olmadan hedef fiyat formülü tamamlanmış sayılmaz. Kodun dördüncü itki sonunu bulması gelişim hedefidir, mevcut doğrulanmış işlev diye yazılmadı.

### X319 · 2025-04-14 10:51:50 UTC · Avellaneda–Stoikov anlatısı ve MA5 prim geri dönüşü
- Bağlı: yeni yöntem; Öneri: tema-3 #22
- Yazar: M (iki başlıklı model/uyarlama açıklaması).
- Kaynak: 1911734132360552515 (2025-04-14 10:51:50 UTC), 1911789788019019979 (2025-04-14 14:32:59 UTC).
- Fikirler:
  - [boyut-risk; M] "bid=r(t)−δ"; "ask=r(t)+δ"; "δ = (1 / γ) * ln(1 + (γ / k))" — metinde rezerv fiyatı S_t−q·γ·σ²·(T−t) anlatılır; γ/k/σ değerleri yok, rezerv formülünün ikinci yazımı kesik — çekirdek belli.
  - [giriş; M] "Hissenin gerçeğe en yakın değerini 5 günlük hareketli ortalamayla modelledim."; "Eğer bu oran %3’ün üzerindeyse, fiyatın primli olduğu kabul edilir → short açılır." — true=MA5, observed=günlük kapanış; sapma=(observed−true)/true>%3 — çekirdek belli.
  - [hedef-çıkış; M] "Fiyat, adil değere %1 altına inene kadar beklenir → pozisyon kapatılır." — adil değerin %1 altı kapanma eşiği olarak anlatılır; stop/süre yok — çekirdek belli.
- Örnek ve sonuç: Sayısal hisse testi, işlem dizisi veya PnL tablosu yok. Metin pozitif PnL üretilebildiğini iddia eder, aynı metin sonunda "İlk deneme pek yakında" yazar.
- Tansu'nun vurgusu: Ayrı T cümlesi yok; M anlatının kullanım iddiası kişisel doğrulanmış ölçüm sayılmaz.
- Belirsiz: MA5'in SMA/EMA türü ve pozisyon sırasında true değerinin girişte sabit mi günlük güncel mi olduğu yok. PnL cümlesi ön çalışma sonucu veya henüz sınanmamış iddia olabilir; ilk deneme ifadesiyle kesinlik kurulamaz.
- YORUM: Günlük MA5 mean-reversion uyarlaması ile envanter temelli piyasa yapıcılık formülleri aynı işlem algoritması diye yazılmadı; M olgunluğu çekirdek belli.

### X320 · 2024-04-24 20:15:25 UTC · Bollinger–Keltner düzenleri ve rejim ayrımı
- Bağlı: R053; Öneri: tema-3 #23
- Yazar: T (2024 kısa yöntem notları) + M (2025 sıkışma açıklaması).
- Kaynak: 1783228274077839740 (2024-04-24 20:15:25 UTC), 1852476829543587877 (2024-11-01 22:24:28 UTC), 1912246536811008424 (2025-04-15 20:47:56 UTC).
- Fikirler:
  - [giriş] "Bollinger Bantları, Keltner Kanalları’nın dışında olacak." — BB dışarıda; alt BB temasından sekme, ikinci mum zıt renk, ADX yükselmesi ve RSI50 kesişimi; henüz netleştirme aşaması — çekirdek belli.
  - [giriş] "trend varken üst bandın üstünde kapanışlar al demiştik."; "alt bandı yukarı kesince al üst bandı aşağı kesince sat." — Keltner'de trendde üst bant üstü kapanış; yatayda ortalamaya dönüş — çekirdek belli.
  - [giriş; M] "Önce Bollinger Bands’in daraldığını ve Keltner Channel’ın içine girdiğini görürüz." — ayrı squeeze düzeni; fiyat KC dışına yukarı çıkarsa AL, aşağı çıkarsa SAT; stop KC orta veya karşı BB bandı, ek RSI/hacim teyidi — çekirdek belli.
- Örnek ve sonuç: Somut işlem sonucu yok; BB/KC periyotları ve çarpanları belirtilmiyor.
- Tansu'nun vurgusu: "Tamamen trende göre strateji kurgulamak lazım keltnerde"
- YORUM: BB'nin KC dışında olduğu 2024 fikri ile KC içinde squeeze olan 2025 anlatısı farklı kurulumlardır. R053 kuyruk/dönüşü ile üst bant trend girişi bağlama göre ayrılır; tek ters sinyal çelişkisi kurulmadı.

### X321 · 2024-03-31 13:21:44 UTC · Bollinger orta bandı ve RSI50 eşzamanlı kesişim
- Bağlı: R053 / R233; Öneri: tema-3 #24
- Yazar: T.
- Kaynak: 1774426858567643590 (2024-03-31 13:21:44 UTC), 1782881410174365714 (2024-04-23 21:17:07 UTC), 1839057936141705262 (2024-09-25 21:42:34 UTC).
- Fikirler:
  - [giriş] "hisse fiyatı orta bollinger bandını yukarı kestiğinde ve aynı zamanda RSI'da 50'yi yukarıya kestiğinde al sinyali üret" — fiyat BB orta bandını ve RSI50'yi eşzamanlı yukarı keser; alt/üst bantlar kullanılmaz — çekirdek belli.
  - [hedef-çıkış] "orta bandı aşağı kestiğinde sat sinyali üret" — fiyat orta bandı aşağı keser; Nisan açıklaması ilk barın orta bandın üstünde kapanmasını ister, stop ATR olabilir — çekirdek belli.
  - [teyit-tetik] "BB sıkışması ve RSI 50'nin yukarı kesilmesi benim sevdiğim bir strateji." — ayrı sıkışma varyantı; sıkışma eşiği yok — çekirdek belli.
- Örnek ve sonuç: İlk paylaşım DOAS; sonrasında hisse izleme önerisi var, metinler gerçekleşmiş getiri vermiyor.
- Tansu'nun vurgusu: "Çok basit tutmak lazım."
- Belirsiz: BB ve RSI periyotları, ATR stop çarpanı yok. Nisan "rsı'da aynı anda 50'yi geçecek" ifadesi seviye veya kesişim okunabilir; Mart açıkça yukarı kesişim ister.
- YORUM: RSI30 dipten dönüşü ile RSI50 trend tetiği ayrı kurulumlar olabilir; R233'ü geçersiz sayacak veri yok. Sıkışma ile orta bant kesişimi tek zorunlu koşul setine eklenmedi.

### X322 · 2025-10-15 16:14:14 UTC · EMA26 ATR bantlarında −3 reddi ve −2 onayı
- Bağlı: yeni yöntem; Öneri: tema-3 #25
- Yazar: M (uzun başlıklı yöntem anlatısı).
- Kaynak: 1978494634121703760 (2025-10-15 16:14:14 UTC).
- Fikirler:
  - [giriş; M] "Fiyat gün içinde -3 ATR bandının altına düşüyor ama kapanışta bunun üzerine çıkıyor" — EMA26−3×ATR bandı altında gün içi hareket, bandın üstünde kapanış; −3 ATR reddi — çekirdek belli.
  - [teyit-tetik; M] "Fiyat son birkaç günde -2 ATR bandını test etmiş ve şimdi bunun üzerinde iki gün üst üste kapanış yapıyor" — EMA26−2×ATR bandında test sonrası iki ardışık üst kapanış; −2 ATR onayı — çekirdek belli.
- Örnek ve sonuç: Sayısal işlem sonucu yok; ATR periyodu ve "son birkaç gün" sayısı belirtilmemiştir. Hacim/MACD/EMA13/RSI/temel-sektör kontrolü güçlendirme önerileri olarak sıralanır; hacim henüz filtre değil denir.
- Tansu'nun vurgusu: Ayrı kısa T cümlesi yok; M anlatı kişisel kesin alım hükmü sayılmadı.
- Belirsiz: Son paragraf MACD histogramının ekstra onay kattığını söylerken önceki bölüm bunu eklenecek filtre gibi anlatır; araçta yalnız panel veya uygulanmış kapı olabilir, kod kaynakta yok.
- YORUM: ATR standart sapma değildir; metnin −3 ATR ile normal dağılım/−3 sigma benzetmesi olasılık kanıtı yapılmadı. Her iki sinyalin zorunlu birlikte olup olmadığı ve stop/çıkış tanımı tamamlanmış değil.

### X323 · 2024-04-12 13:28:18 UTC · MACDAS ve tetik çizgisi kesişimi
- Bağlı: yeni yöntem; Öneri: tema-3 #26
- Yazar: T (formül) + G (optimizasyon aralıkları).
- Kaynak: 1778777162587279414 (2024-04-12 13:28:18 UTC).
- Fikirler:
  - [giriş] "AL= CROSS(MACDAS(OPT1,OPT2,OPT3),MACDASTRIGGER(OPT1,OPT2,OPT3))"; "SAT= CROSS(MACDASTRIGGER(OPT1,OPT2,OPT3),MACDAS(OPT1,OPT2,OPT3))" — yukarı/aşağı kesişim AL/SAT — kural tam.
  - [ölçüm-ilkesi; G] "OPT ARALIKLARI" — görselden: OPT1 13–55, OPT2 8–15, OPT3 3–13; üçünde adım 1; seçilmiş optimum değer yok — kural tam (arama aralıkları).
- Örnek ve sonuç: Hisse, seçilen optimumlar ve işlem sonucu yok.
- Tansu'nun vurgusu: "Her hissede aynı sonucu vermez. Ayrıca sadece bu değerler yeterli değil."
- YORUM: Aralıklar evrensel en iyi parametre olarak yazılmadı; kaynak adı açık bir başka yazar atfı içermiyor.

### X324 · 2026-04-11 09:42:27 UTC · Beş günlük kırılım toplamı ve BULL/BEAR
- Bağlı: yeni yöntem; Öneri: tema-3 #27
- Yazar: M (başlıklı FROTO açıklaması) + T (ikinci kısa not) + G.
- Kaynak: 2042901081785557425 (2026-04-11 09:42:27 UTC), 2042948983744557423 (2026-04-11 12:52:48 UTC).
- Fikirler:
  - [rejim; M] "+3 seviyesine veya üzerine çıktığı anlarda beliriyor." — 5 günlük toplam ≥+3, BULL; −4/−5 bölgesinde BEAR, açıklamada panik eşiği −4 — çekirdek belli.
  - [giriş; M] "kırılımın (yukarı veya aşağı) netleşmesini beklemek genellikle en güvenli stratejidir." — rolling tepe/dip kırılımı ve beş günlük toplamla nötr durumda bekleme; rolling uzunluğu yok — çekirdek belli.
- Örnek ve sonuç: görselden: FROTO son 10.04.2026, kapanış 105,30, günlük sinyal +0, beş günlük toplam −1; +3 ve −4 kesikli eşikler. İkinci paylaşımda CRFSA 200G direnç 133,00 TL, son 133,10 (+%0,1) ve ayrı NH/NL+BULL grafiği var; ikisinin ortak hesap/aynı hisse bağı açık değil.
- Tansu'nun vurgusu: "İki sistemi birleştirince fark yaratıyor gerçekten."
- Belirsiz: Günlük tepe kırılımına +1/dip kırılımına −1 verilmesi görsel işaretlerinden çıkarılabilir; açık hesap formülü yok. BEAR ifadesi yalnız −4/−5 değerlerini veya toplam≤−4 eşiğini anlatıyor olabilir; çıktı aralığı ve uç değerler belirtilmiyor.
- YORUM: X003'ün N=510 evren genişliği ve sayısal NH−NL eşikleri bu tek hisse puanına taşınmaz. Önerinin `≤−4` formülü eşik okumasıdır, birebir kaynak formülü diye sunulmadı.

### X325 · 2025-06-22 12:36:14 UTC · EWMA getiri z-skoru ile uç hareket izlemesi
- Bağlı: R053 (uç sapma/ortalamaya dönüşle bağ); Öneri: tema-3 #28
- Yazar: M (özgün BIST100 EWMA açıklaması) + T (AVTUR sonuç notu) + G. Kendi gönderisini alıntıladığı için A değil.
- Kaynak: 1936765170744701091 (2025-06-22 12:36:14 UTC), 1936767147914485837 (2025-06-22 12:44:06 UTC).
- Fikirler:
  - [hedef-çıkış; M] "z-score > 2 (yeşil nokta): Aşırı fiyatlama olabilir → kar satışı / ters pozisyon açılabilir." — günlük getiri, EWMA ve ±2σ bantları; z>+2 uç pozitif sapma — çekirdek belli.
  - [giriş; M] "z-score < -2 (kırmızı nokta): Aşırı düşüş → geri dönüş alım fırsatı olabilir." — z<−2 uç negatif sapma; yarı ömür/pencere ve z-skor hesabı yok — çekirdek belli.
- Örnek ve sonuç: Tansu 19 Haziran tarihli taramanın AVTUR için 20 Haziran satış beklentisi verdiğini, hissenin değer kaybettiğini söylüyor. Görselden: AVTUR getiri/EWMA/±2σ/z>2/z<−2 grafiği; BIST100 ayrı grafiğinde aynı göstergeler. Kesin düşüş yüzdesi ve işlem kaydı yok.
- Tansu'nun vurgusu: "Sonucu ortada... Hisse değer kaybetti."
- Belirsiz: AVTUR grafiğinin sağ uç noktası hangi güne ait açık etiketlenmiyor; 19→20 Haziran önden sinyal iddiası veya sonradan grafik anlatımı olarak okunabilir; zaman damgalı tarama çıktısı gösterilmiyor.
- YORUM: İlk kaynak tarihi önerideki sonuç gönderisinden önceki kendi alıntısına düzeltildi. Getiri z-skoru fiyatın Bollinger bandından taşmasıyla aynı ölçü değildir; "olabilir/açılabilir" kesin işlem kapısına çevrilmedi.

### X326 · 2025-07-28 11:51:14 UTC · Retest, onay ve araç seviyeleri
- Bağlı: R195 / R114 / R253; Öneri: tema-3 #29
- Yazar: T (retest uyarıları) + M (CRDFA uzun analiz motoru anlatısı) + G (ASTOR/AKSA/TRCAS çıktıları).
- Kaynak: 1949799810053104041 (2025-07-28 11:51:14 UTC), 2095199834374320434 (2026-09-02 17:19:02 UTC), 2095558917841404010 (2026-09-03 17:05:54 UTC), 2096284655657836608 (2026-09-05 17:09:43 UTC).
- Fikirler:
  - [teyit-tetik] "Retest beklemezseniz sonu felaket olabilir." — kırılımdan sonra geri test ve tutunma izleme; genel tolerans yok — çekirdek belli.
  - [teyit-tetik; M] "28,52’nin üzerine yeniden çıkması ve 4 saatlik mumu bu seviyenin üzerinde kapatması gerekiyor." — CRDFA örneğinde 28,52 üstü H4 kapanış, ardından bölgeyi koruyup yeniden yukarı dönüş; tek kapanış hemen AL değildir — çekirdek belli.
  - [stop-geçersizlik; M] "Buradaki 24,98 otomatik stop anlamına gelmiyor" — CRDFA 25,56 altı uyarı; 24,98 altı kalıcı hareket yapısal geçersizlik; kalıcılık tanımı yok — çekirdek belli.
- Örnek ve sonuç: görselden: ASTOR Lookback75, kırılım 09.07.2025, pullback 18.07.2025, onay 21.07.2025; sonraki yükselen mumlar var, işlem getirisi yok. AKSA kalite 73,8/100, R/R 1:1,93, hacim 2,47x, kırılım 31.07.2026 / 12,65, hedef 15,52, stop 11,60, Fib%38,2=11,55 / %50=11,21. TRCAS kalite 63,5/100, R/R 1:1,70, hacim 1,29x, 04.09.2026 sinyali/kırılımı 48,60, hedef 56,03, stop 45,18, Fib45,76/44,88. CRDFA metin hedef/sınavları 30,64 / 32,20 / 42,10; satış bölgesi 30,64–34,00.
- Tansu'nun vurgusu: "İşte buna pullback sonrası onay diyoruz, hacim ile devam ediyor."
- Belirsiz: AKSA/TRCAS görselleri tetiklendi/kırılım der; retest tamamlandı etiketi yok. Tansu'nun retest uyarısı beklenmesi gereken sonraki adım veya mevcut şeklin geriye dönük yorumu olabilir; tamamlanmış retest sonucu sayılmadı.
- YORUM: Kalite ve R/R değerleri örnek çıktıdır, giriş eşikleri değildir. Fib düzeyleri kırılım−oran×(hedef−kırılım) hesabıyla uyumludur; bu hesap ilişkisi kaynakta yazılı yöntem yerine geçirilmedi. CRDFA için M olgunluğu çekirdek belli; R199'un FVG limit emriyle bu farklı kurulum arasında otomatik çelişki kurulmaz.

### X327 · 2023-12-13 15:23:27 UTC · VaR ufku, kişisel risk limiti ve hedge
- Bağlı: R053; Öneri: tema-3 #30
- Yazar: T + G (VaR sütun grafiği).
- Kaynak: 1734957210545844544 (2023-12-13 15:23:27 UTC), 1878086550665175243 (2025-01-11 14:28:21 UTC), 1878086552548442457 (2025-01-11 14:28:21 UTC), 1878089934268965110 (2025-01-11 14:41:48 UTC).
- Fikirler:
  - [boyut-risk] "100.000 tl yatırımın %99 güven düzeyinde 1 gün 1 hafta 1 ay 3 ay da maks kayıp oranları gösterilmektedir." — örnek yatırım 100.000 TL, güven %99, dört ufuk, son 10 yıllık veri; hesap yöntemi yok — çekirdek belli.
  - [boyut-risk] "günde 5.000tl kaybetmeyi göze alabilirim derseniz ona göre bir hedging yolu izlemeniz lazım" — kişisel günlük risk kabulü 5.000 TL örneği; zorunlu herkes için %5 limit değildir — çekirdek belli.
  - [boyut-risk] "Örneğin put opsiyonu satın alabilirsiniz."; "Ya da en basit hedging tamamen ters korelasyonlu bir hisse senedini portföyde tutmaktır." — vadeye/risk kabulüne göre hedge seçenekleri; kullanım fiyatı, miktar, vade ve hedge oranı yok — çekirdek belli.
- Örnek ve sonuç: görselden: VaR sütunları yaklaşık 1 gün 5.900 TL, 1 hafta 13.400 TL, 1 ay 28.400 TL, 3 ay 52.000 TL; sayılar eksenden yaklaşık okundu, etiketli kesin değer değil. Gerçek hedge işlemi/sonucu yok.
- Tansu'nun vurgusu: "O aslında kaybetmeyi göze alabileceğiniz tutar ile ilgili. tamamen kişisel."
- YORUM: Kaynaktaki "maks kayıp" ifadesi güven düzeyindeki VaR anlatımıdır; mutlak kayıp tavanı garantisi değildir. Grafikte birim TL tutarıdır, metindeki "oran" sözcüğünden yüzde türetilmedi. %99, R053'ün %95 örneğinin yerine evrensel güncel oran olarak geçirilmez.

### X328 · 2025-01-01 11:59:17 UTC · Kelly ve fractional Kelly pozisyon limiti fikri
- Bağlı: R184 / R212; Öneri: tema-3 #31
- Yazar: T.
- Kaynak: 1874425159224000594 (2025-01-01 11:59:17 UTC), 1874426039340007571 (2025-01-01 12:02:47 UTC).
- Fikirler:
  - [boyut-risk] "Cevabı Kelly Criteria."; "Bazıları fractional kelly criteria da kullanır." — trade'e ayrılacak optimal sermaye oranı için yöntem adı; formül, kazanma olasılığı, ödül/kayıp oranı ve fractional katsayı yok — yalnız fikir.
- Örnek ve sonuç: 100.000 TL sermayeyle ne kadar trade yapılacağı sorusu; oran/lot sonucu yok. Hesaplama tablosunun varlığı söylenir, tablo sunulmaz.
- Tansu'nun vurgusu: "ben genelde kullanırım robotlarımda limitim genelde KC'dır benim."
- Belirsiz: KC bağlamda Kelly Criteria olarak okunur; kısa cevap kendi başına açılım/formül vermez. Full Kelly veya fractional uygulama kullandığı açıklanmaz.
- YORUM: Kelly limiti, R212 %1 örnek riskinin veya R184 ATR lot formülünün yerine hesaplanmış sayısal oran olarak yazılmadı.

### X329 · 2025-06-28 14:38:10 UTC · AKD net alım payı ve takasın yoğunlaşması
- Bağlı: R221 / R237 (takas-birikim); Öneri: tema-3 #32
- Yazar: M (üç uzun AKD/takas açıklaması) + G (TERA AKD ekranı ve fiyat grafiği).
- Kaynak: 1938970182380134893 (2025-06-28 14:38:10 UTC), 1939258295551701476 (2025-06-29 09:43:01 UTC), 1964331893341503858 (2025-09-06 14:16:33 UTC).
- Fikirler:
  - [teyit-tetik; M] "aynı kurumun birkaç gün üst üste net alım yapması" — istikrarlı kurumsal alıcı ve yoğunlaşan takas olumlu okunur; kurum profilini ve net alıcının son 10 günlük davranışını inceleme — çekirdek belli.
  - [teyit-tetik; M] "fiyat yükseliyor ama takas sürekli el değiştiriyorsa bu bir tuzak yükseliş ya da geçici bir ralli olabilir." — el değişimini risk işareti olarak okuma; kesin tuzak hükmü değil — yalnız fikir.
  - [giriş; M] "büyükler satıyor, küçükler topluyorsa – o zaman aynı bölge riskli hale gelir ve giriş yapılmamalıydı." — yatay birikim örneğinde karşıt kurum akışı; büyük/küçük tanımı ve eşik yok — çekirdek belli.
- Örnek ve sonuç: görselden: TERA AKD 22–27.05.2025; toplam net 3.998.122 lot, toplam adet 61.989.332; TERA YATIRIM net 3.033.904 lot, net alıcı payı %76, maliyet 137,460 TL. Fiyat grafiğinde yatay bölümden sonraki yükseliş ve son mum −%9,97 görünüyor; belirli giriş-çıkış getirisi yok.
- Tansu'nun vurgusu: Ayrı T cümlesi yok; başlıksız uzun açıklamalar M biçimli olarak ayrıldı.
- Belirsiz: M anlatı, kurumsal alıştan küçük yatırımcının satışı ve birikimin yükselişe neden olduğu sonucuna gidiyor; aracı kurum ekranı müşteri kimliğini veya nedenselliği tek başına göstermez. Kurum dağılımı veya gerçek yatırımcı profili okuması ayrı tutulur.
- YORUM: "Toplam işlem hacminin %76'sından fazlası" kaynak metninde yanlış paydadır; görsel %76'nın net alım payı olduğunu gösterir. X004 kurum sürekliliği ve X025 fon kalıcılığıyla ortak tema olsa da burada yeni net-alım örneği ve son 10 gün inceleme ayrıntısı vardır; emir defteri derinliğiyle karıştırılmadı.

### X330 · 2025-11-29 12:39:26 UTC · Altında call duvarı ve momentum squeeze fikri
- Bağlı: yeni yöntem; Öneri: tema-3 #33
- Yazar: T.
- Kaynak: 1994748031900492128 (2025-11-29 12:39:26 UTC), 2085043984414409205 (2026-08-05 16:43:18 UTC), 2085278210728599696 (2026-08-06 08:14:02 UTC).
- Fikirler:
  - [bölge] "Call Duvarı"; "Mıknatıs (Magnet) görevi görür." — üst call duvarını fiyatın yönelebileceği bölge olarak görme; hesap yok — yalnız fikir.
  - [teyit-tetik] "4251 seviyesi üzerinde tutunursa call duvarının yukarı çekildiği anlaşılır." — ons altında 4251 dolar örneği; tutunma süresi ve yeniden hesap yöntemi yok — çekirdek belli.
  - [giriş] "Sağlam yıkarsa momentum squeeze gündeme gelir ivme hız kazanır" — 4251 dolar kırılımıyla ivme beklentisi; "sağlam" ölçütü yok — yalnız fikir.
- Örnek ve sonuç: 5 Ağustos metni 4251 dolar zorlamasını, 6 Ağustos metni akşam yeniden değerlendirmeyi anlatır; sonraki gerçekleşmiş işlem sonucu yok.
- Tansu'nun vurgusu: "Zaten haftalardır beklentimi yazıyorum yukarı yönlü."
- Belirsiz: Verilen kaynaklarda put duvarının seviye/hesap/işlem kuralı yok; başlıkta call/put denmesi önerinin kapsamıdır, bu kayıt yalnız call kanıtını taşır.
- YORUM: Bir akşam yeniden değerlendirme sözü her akşam otomatik hesap kuralı yapılmadı; duvarı aşma doğrudan AL komutu değildir.

### X331 · 2025-01-01 11:23:39 UTC · Kayıptan sonra gerekli telafi getirisi
- Bağlı: R138 (sermaye koruma ilkesiyle bağ); Öneri: tema-3 #35
- Yazar: T.
- Kaynak: 1874416190443114907 (2025-01-01 11:23:39 UTC).
- Fikirler:
  - [boyut-risk] "100 liranız 90 liraya inerse %10 kaybetmiş olursunuz" — başlangıç 100, düşüş sonrası 90; kayıp %10 — kural tam.
  - [boyut-risk] "90 liranızı tekrar 100 lira yapmak için %11.12 kazanmanız lazım." — kaynakta %11.12; doğru telafi 100/90−1=%11,111…; iki ondalığa normal yuvarlama %11,11 — kural tam (örnek hesap).
- Örnek ve sonuç: 100→90→100 aritmetik örneği; gerçekleşmiş işlem yok.
- Tansu'nun vurgusu: "Sözün kısası paranızı kaybederseniz hayallerle yaşarsınız."
- YORUM: Genel telafi formülü `1/(1−kayıp)−1` kaynakta yazılı değildir; örnekten yapılan cebirsel genellemedir (kayıp ondalık oran, 0≤kayıp<1). %11,12, yukarı yuvarlanmış yeterli oran olarak da okunabilir; birebir alıntı korundu, normal iki basamaklı sonuç %11,11 diye düzeltildi. R138 A/D–EMA sinyaline yeni giriş koşulu eklenmedi.

### tema-3 özeti

| X no | başlık | bağlı R | olgunluk | yazar |
|---|---|---|---|---|
| X301 | Sabit ATR hedef ve stop merdiveni | R239 / R184 | kural tam | T + G |
| X302 | RoC50, ADX/ADXR ve OBV birleşimi | yeni yöntem; R137 / R196 bağı | kural tam | T + G |
| X303 | RSI30 direnç reddi ve başa baş çıkış | R233 / R239 | çekirdek belli | T + M |
| X304 | Bollinger 3 SS zıt mum dönüşü | R053 | çekirdek belli | T |
| X305 | RSI 144 günlük Fibonacci | yeni yöntem | çekirdek belli | M + T + G |
| X306 | Death Cross uyarısı | yeni yöntem | çekirdek belli | M + G |
| X307 | SuperTrend + EMA5/20 | yeni yöntem | çekirdek belli | T |
| X308 | Vegas ATR kâr alma fikri | yeni yöntem; X010 çıkış eki | yalnız fikir | T |
| X309 | Range kırılımı ve teknik teyit | yeni yöntem; R082 bağı | çekirdek belli | T + M + G |
| X310 | Kanal kırılımı ve daralan yapı | R124 / R247 | çekirdek belli | T + G |
| X311 | Üç ayrı hacim karşılaştırması | R124 | çekirdek belli | T + M |
| X312 | Gizli ve klasik RSI uyumsuzluğu | R116 / yeni yöntem | çekirdek belli | T + G + M |
| X313 | Basit MOST ve VAR formülleri | yeni yöntem | kural tam | T + G |
| X314 | Weinstein 150/200 gün koşulları | R108 | çekirdek belli | M |
| X315 | 20/50 ortalama ve geri çekilme | R210 bağı | çekirdek belli | T |
| X316 | SMA200/250 geri alma | R212 | çekirdek belli | T |
| X317 | EMA13 ve 3 ATR risk ayrımı | R128 bağı | çekirdek belli / yalnız fikir | M |
| X318 | Elliott iki hedef tarifi | R193 | çekirdek belli | M + T + G |
| X319 | Avellaneda–Stoikov / MA5 | yeni yöntem | çekirdek belli | M |
| X320 | Bollinger–Keltner ve rejim | R053 | çekirdek belli | T + M |
| X321 | BB orta bandı + RSI50 | R053 / R233 | çekirdek belli | T |
| X322 | EMA26 −3/−2 ATR | yeni yöntem | çekirdek belli | M |
| X323 | MACDAS kesişimi | yeni yöntem | kural tam | T + G |
| X324 | Beş günlük kırılım toplamı | yeni yöntem | çekirdek belli | M + T + G |
| X325 | EWMA getiri z-skoru | R053 bağı | çekirdek belli | M + T + G |
| X326 | Retest ve araç seviyeleri | R195 / R114 / R253 | çekirdek belli | T + M + G |
| X327 | VaR ve hedge | R053 | çekirdek belli | T + G |
| X328 | Kelly pozisyon limiti | R184 / R212 | yalnız fikir | T |
| X329 | AKD net alım ve takas | R221 / R237 | çekirdek belli / yalnız fikir | M + G |
| X330 | Call duvarı ve squeeze | yeni yöntem | çekirdek belli / yalnız fikir | T |
| X331 | Kayıp telafi getirisi | R138 bağı | kural tam (örnek) | T |

### tema-3 alınmayanlar

| öneri no | neden | kanıt id |
|---|---|---|
| #1 | Yinelenen: %1 risk, risk/(2 ATR), 100.000 dolar→1.000 dolar, 14,30 dolar→yaklaşık 70 hisse ve SMA250/2 ATR stopu R212'de zaten var. Tansu'nun sonraki "2 Atr" cevabı R184'ün belirsiz paydasını açıklıyor, fakat yeni yöntem kaydı oluşturmuyor. | 1999481868106826013; 2005227814875021373 (T cevabı); 2005225851965841414 yalnız sorunun bağlamı |
| #4 | Yinelenen: son üç pozitif/önceki üç negatif CMF X002'de var; filtre anlatımı aynı altı günlük düzeni açıklıyor. CMF hesap periyodu altı gün diye yazılamaz. | 1845562970304102747; 1845567753878384928; 1865470227720405267 |
| #8, Golden Cross/ön tarama kısmı | Kısmen yinelenen: EMA50/EMA200 yukarı kesişimi X018'de, fiyat EMA200 kesişimi X032'de var. Yalnız Death Cross M açıklaması X306'ya alındı. | 1847338202924744724; 1847355900014858452; 1848805888355652024; 1842524448802365487 |
| #10, giriş kısmı | Yinelenen: EMA12'nin EMA144/169 tünelini yukarı kesmesi ve günlük Vegas X010'da var. Orada olmayan çarpansız ATR çıkış fikri X308'e alındı. | 1827341150908543159; 1848385592771424616; 1848803496893558928; 1851726487855972606 |
| #15, Anıl Özekşi sürümleri | Başkasının kodu: altı OPT'li MOST görselinde ve RSI üstüne MOST metninde Anıl Özekşi açıkça yazıyor. Ayrıntı bölümündeki OTT/HHV/LLV kaynağı da ona atıflı. Tansu'nun önerdiği başka yazar kodu kendi kodu olarak alınmadı; basit formüller X313'te. | 1779421690071490990; 1783371645224149075; 1790974588156821797 |
| #21 | Tansu'nun kendi yöntemi değil: "@mehmetemanet abimin stratejisinin grafik çıktıs örneği." Görsellerde 60 dakika/RSI55–45 doğrulanıyor fakat yazar atfı açık. | 1860422703150149949 |
| #34 | Yinelenen: aynı 16 Şubat gönderisi ve haftanın kötü gününün dönemle değişmesi X035'te var. Görsel etiketlenmemiş kesin sayılar için ikinci kayıt oluşturulmadı. | 1891208151497613761 |

35 öneri doğrulandı: 31 öneriden X301–X331 üretildi; 4 öneri tamamen, 3 önerinin yinelenen/başka yazara ait kısmı alınmadı. M metinler fikir/çekirdek olarak korundu. Değerleme ağırlığı önerisi bu listede yoktur. R182/R185/R199/R225 M kartlarıyla aynı kurulumda kaynaktan kesin çelişki saptanmadı; farklı yöntemler karşıt kural gibi yazılmadı.

## Tema 4 — Değerleme-temel, portföy, çift

### X401 · 2023-08-26 10:56:37 UTC · Değerleme ağırlığının tarihçesi
- Bağlı: R068 / R151 / R158 / R064; Öneri: tema-4 #1
- Yazar: T (kendi değerlemesi ve kısa açıklamaları) + M (2025 sistematik açıklama) + G (imzalı tablolar).
- Kaynak: 1695389783147581542 (2023-08-26 10:56:37 UTC), 1708030356564160854 (2023-09-30 08:05:45 UTC), 1780322528658886674 (2024-04-16 19:49:02 UTC), 1848034791116931310 (2024-10-20 16:13:23 UTC), 1850969302347989014 (2024-10-28 18:34:05 UTC), 1913527179364765803 (2025-04-19 09:36:45 UTC), 2084757098529693800 (2026-08-04 21:43:19 UTC), 2084997818570182832 (2026-08-05 13:39:51 UTC).
- Fikirler:
  - [temel-değerleme; eski sürüm] "Çarpanlar %40, İNA %60 ağırlıklandırılarak" — 2023-09 TTRAK; 2024-04 BRISA da %40 çarpan / %60 İNA — kural tam.
  - [temel-değerleme; güncel] "En sonunda bu ortalamanın %60'ını, DCF'in de %40'ını alırım." — çarpan ortalaması %60, DCF-İNA %40 — kural tam.
  - [temel-değerleme; M] "Çarpan ve Kâr Modeli Ortalaması (Ağırlık: %60)"; "DCF Değeri (Ağırlık: %40)" — 2025-04 açıklamasında kâr modeli çarpanla ortalanır — çekirdek belli.
- Örnek ve sonuç: görselden: TTRAK çarpan ortalaması 785,30; İNA 2116,93; ağırlıklı hedef 1584,28; fiyat 881,00; potansiyel %79,83. Ayrı kâr modeli ortalaması 1083,69 bu örneğin nihai hedefine girmez. SAYAS tablosunda çarpan fiyatları 47,12 / 269,47 / 161,59; İNA 133,71; nihai 143,98. 2024-10 gönderisi aynı eski SAYAS tablosunu yeniden paylaşır; yeni ağırlık kararı değildir.
- Tansu'nun vurgusu: "Dcf çok subjektif, o nedenle payını düşük tutma taraftarıyım".
- Belirsiz: Geçiş 2024-04 ile 2025-04 arasındadır. 2024-10 taslağındaki "İlk grubun %6’ı" ifadesi harfi harfine %6 okunabilir; ikinci grup %40 ve sonraki açık %60/%40 anlatımıyla %60 yazım hatası olarak da okunur. Kesin geçiş günü kaynakta yok. Kâr modeli kayar: 2024-10 taslağında ikinci grup "İNA'ya göre fiyat" ile "Kar tahmin modeline göre fiyat"ın ortalamasıdır (%40 tarafı); 2025-04'te kâr modeli çarpanla ortalanır (%60 tarafı).
- YORUM: Önerideki 1769338023169143095 işletme sermayesini anlatır; ağırlık kanıtı değildir. TTRAK gönderisinin tarihi 2023-09-30'dur. Eski %40/%60 sürümü güncel kuralın hatası sayılmaz; 2025-04 ve 2026 kendi metinleri güncel ağırlığı destekler.

### X402 · 2024-04-19 14:47:25 UTC · NEFK–fiyat ayrışması ve temel teyitli çift
- Bağlı: yeni yöntem; Öneri: tema-4 #2
- Yazar: T (2024 çift fikri, kısa gönderiler) + M (2025 uzun açıklamalar).
- Kaynak: 1781333788556935603 (2024-04-19 14:47:25 UTC), 1862514363178811538 (2024-11-29 15:10:02 UTC), 1889068388334370953 (2025-02-10 21:46:15 UTC), 1892680047779074122 (2025-02-20 20:57:42 UTC), 1911030895248539760 (2025-04-12 12:17:25 UTC), 1917362530000986239 (2025-04-29 23:37:04 UTC), 1941455577097306576 (2025-07-05 11:14:14 UTC), 1956737745528705173 (2025-08-16 15:20:07 UTC).
- Fikirler:
  - [temel-değerleme] "Betaları aynı ve yüksek pozitif korelasyona sahipler. İkisininde net esas faaliyet karı artmış. Ama bu artış birinde hisse fiyatına yansımamış." — eşit beta, yüksek pozitif korelasyon; NEFK artışı / fiyat gecikmesi — çekirdek belli.
  - [temel-değerleme] "NEFK artarken hisse fiyatı artmıyor ise orada sizin için gizlenmiş bir fırsat olabilir." — tek hisse sürümü — çekirdek belli.
  - [teyit-tetik; M] "Ama NEFK düşerken HBK yükseliyorsa, dikkat:" — HBK artışının operasyon dışı kaynaklarını araştırma; satış / NEFK / net dönem kârı ile birlikte okuma — çekirdek belli.
  - [çift; M] "koentegrasyon testinde p-value değerinin 0.05’in altında çıkması" — bilanço iyileşen, biri fiyatlamış biri geride çiftte korelasyon ve eşbütünleşme teyidi — çekirdek belli.
- Örnek ve sonuç: Çiftte geride kalan hissede farkın kapanması yönünde pozisyon fikri; bu kaynaklarda gerçekleşmiş işlem sonucu verilmez. 1889068388334370953, NEFK artıp HBK henüz artmadığında da potansiyel marj arar; yalnız birlikte artışa indirgenmez.
- Tansu'nun vurgusu: "orada temel analiz açısından istatistiksel bir arbitraj vardır. Bunlara dikkat edin arkadaşlar."
- Belirsiz: "hisse fiyatına yansımamış" aynı dönemde fiyat artmaması olarak da göreli geri kalma olarak da okunabilir; pencere ve sayısal gecikme eşiği yok. Yüksek korelasyon eşiği bu ailede yazılı değil.

### X403 · 2025-01-01 15:10:00 UTC · Eşbütünleşme karar kuralı ve tarama hattı
- Bağlı: R262 / R228; Öneri: tema-4 #3
- Yazar: T (kısa karar ve tarama metinleri) + M (ML hattı ve uzun açıklama) + G (test tablosu).
- Kaynak: 1874473152455246129 (2025-01-01 15:10:00 UTC), 1912875732646117781 (2025-04-17 14:28:08 UTC), 1941585010051498309 (2025-07-05 19:48:33 UTC), 1941623461744415106 (2025-07-05 22:21:21 UTC), 1941900327655027097 (2025-07-06 16:41:31 UTC), 2086417789812646087 (2026-08-09 11:42:19 UTC).
- Fikirler:
  - [çift] "Eğer Pv<0.05, ve Tv<Cv ise conitegration var derim." — p<0,05 ve test istatistiği kritik değerden küçük — kural tam (karar koşulu).
  - [tarama-evren] "Korelasyonu 0.7'den büyük hisse çiftlerini alıyorum"; "z-score +-2 alıyorum." — tüm BIST → korelasyon >0,7 → eşbütünleşme → Z ±2 — çekirdek belli.
  - [çift; M] "spread = A - hedge_ratio * B" — yıllık getiri/volatilite → StandardScaler → K-Means, KneeLocator → küme içinde Engle-Granger → OLS hedge oranı → spread/Z → t-SNE görselleştirme — çekirdek belli.
- Örnek ve sonuç: görselden: SAHOL–YKBNK korelasyon 0,953, p=0,0094, Evet; AKBNK–SAHOL 0,968, p=0,1615, Hayır. Yüksek korelasyon eşbütünleşme yerine geçmez. Ayrı emtia gönderisi altın–bakır p=0,13 riskini kabul ederek BUY Copper ve +%90 getiri bildirmiştir; bu Tansu'nun bildirdiği sonuçtur.
- Tansu'nun vurgusu: "Benim kodumda da bu yapılıyor".
- Çelişir: R228 / R262'nin istisnasız eşbütünleşme şartı ile 2086417789812646087'deki p=0,13 kabulü ayrışır.
- Belirsiz: Emtia gönderisi genel şartın gevşetilmesi olarak da yalnız risk kabul edilen göreli rotasyon istisnası olarak da okunabilir; tek genel kurala birleştirilmez. Test penceresi ve kritik değerin güven düzeyi yazılı değil.
- YORUM: Kaynaktaki H0 anlatımı istatistiksel hipotezin düzgün tanımı değildir; kayda yalnız açık karar eşitsizlikleri alındı. Eşbütünleşme getiriyi garanti etmez.

### X404 · 2024-11-15 12:27:34 UTC · Log fark, sabit sapma ve çift bantları
- Bağlı: R101; Öneri: tema-4 #4
- Yazar: T + G (standart sapma grafiği).
- Kaynak: 1857400047589048780 (2024-11-15 12:27:34 UTC), 1858560343200436379 (2024-11-18 17:18:10 UTC), 1860462510752575670 (2024-11-23 23:16:42 UTC), 1862207562378035671 (2024-11-28 18:50:55 UTC), 1891546429388189846 (2025-02-17 17:53:06 UTC), 1941550364911862113 (2025-07-05 17:30:53 UTC).
- Fikirler:
  - [çift] "iki varlık arasındaki logaritmik getiri farkını" — farkın hareketli ortalaması ve standart sapma bantları — çekirdek belli.
  - [çift] "30HO ile temel trendi belirliyorum."; "Sabit standart sapma" — GARAN–ISCTR'de log fark, 30 HO ve Z benzeri ölçü — çekirdek belli.
  - [tarama-evren] "Normal şartlarda pairs trading için 0.80 ve üstü alınır ama ben BIST ortamında 0.71'in anlamlı bir korelasyon değeri olduğunu düşünüyorum ve deneyimledim." — 0,80 genel referans, 0,71 BIST örneği — çekirdek belli.
- Örnek ve sonuç: görselden: SMRTG–GESAN anlatımındaki standart sapma grafiğinde gri bölgeler +2…+4 ve −2…−4; son değer yaklaşık +2,7. 1941550364911862113 EREG/KRDMD yön beklentisi bildirir; gerçekleşmiş sonuç değil.
- Tansu'nun vurgusu: "Sabit standart sapma, aşırı bölgeleri net görmek ve işlem kararlarını basitleştirmek için tercih ettim."
- Belirsiz: İlk metin logaritmik getiri farkı, sonraki metin logaritmik fark der; log fiyat farkı veya log getiri farkı okunabilir. Sabit standart sapmanın örneklem penceresi yok. Görselde ±4 sınırı işlem stopu olarak da sadece gösterim bandı olarak da okunabilir; stop diye yazılmaz.

### X405 · 2023-08-24 22:28:55 UTC · Tarihsel F/K ve PD/DD bantları
- Bağlı: R144; Öneri: tema-4 #5
- Yazar: T (DOAS/FROTO kısa metinleri) + M (2025 dip ve FROTO stratejileri) + G (çarpan grafikleri).
- Kaynak: 1694839230298468742 (2023-08-24 22:28:55 UTC), 1696022604472111319 (2023-08-28 04:51:14 UTC), 1700793391423058126 (2023-09-10 08:48:38 UTC), 1913691337184154030 (2025-04-19 20:29:04 UTC), 1916743082336285121 (2025-04-28 06:35:36 UTC).
- Fikirler:
  - [giriş/hedef-çıkış] "FK 2-3 arası alınıp, 7-5 arası satılabilir." — DOAS'a özel alım 2–3 / satış kaynakta 7–5 — kural tam.
  - [giriş/hedef-çıkış] "Trade seveler 7-8 bandından alıp 16-19 bandında satabilir." — 2023 FROTO sürümü; dönemsellik uyarısı — kural tam.
  - [giriş; M] "F/K oranı 6.3 seviyesinin altına gerilediğinde kademeli alım başlatılır." — 2025 FROTO: <6,7 hazırlık; <6,3 kademeli; 5,0–3,5 agresif; <3,5 ikinci pozisyon; 6,7–8,0 tut; ~10 kademeli satış, >10 hızlı satış — çekirdek belli.
  - [teyit-tetik; M] "RSI’nin 30 seviyesinin altına düşüp yukarı yönlü dönüş yapması" — tarihsel F/K ve PD/DD altında, kârlılık/HBK güçlü; örnek ROE %20, F/K<5, RSI 25'ten yukarı — çekirdek belli.
- Örnek ve sonuç: görselden: DOAS ilk F/K ortalaması 4,90; +1/+2 SD 6,39/7,88; −1/−2 SD 3,40/1,91. 2014–2023 grafiğinde F/K ort. 8,41; +1/+2 12,77/17,13; −1 4,06. PD/DD ort. 2,04; +1/+2 2,82/3,61; −1/−2 1,25/0,46. FROTO grafiğinde 2023/12 dip yaklaşık 3,42; 6,7/6,3/3,5/10 işlem eşikleri grafikte yazmaz, M metnindedir. İşlem sonucu yok.
- Tansu'nun vurgusu: "İstatistiğe kulak verelim.".
- Belirsiz: DOAS "7-5" ifadesi azalan sıra veya 5–7 aralığı olarak okunabilir; alıntı düzeltilmedi. Hisseye özel eşikler bütün hisseler için ortak SD kuralı değildir.
- YORUM: Önerinin önceki bölümündeki 1913691337184154030 tarihi 2025-04-19 olarak düzeltildi. M stratejilerin açık eşikleri var; Tansu'nun kendi sınanmış işlem kuralı diye yükseltilmedi.

### X406 · 2023-08-26 09:05:58 UTC · TTM, yıllık HBK ve ortalama özsermaye
- Bağlı: R133 / R146 / R152; Öneri: tema-4 #6
- Yazar: T (kısa girişler) + M (yıllıklandırma ve oran açıklamaları) + G (SAYAS/TCELL tabloları).
- Kaynak: 1695361936651653499 (2023-08-26 09:05:58 UTC), 1889451595584115079 (2025-02-11 23:08:59 UTC), 1915483602713997579 (2025-04-24 19:10:53 UTC), 1915483606887055800 (2025-04-24 19:10:54 UTC), 1916736171838767120 (2025-04-28 06:08:09 UTC), 1917565014988218574 (2025-04-30 13:01:40 UTC), 1956754276270641304 (2025-08-16 16:25:48 UTC).
- Fikirler:
  - [ölçüm-ilkesi; M] "her yılın 1. çeyreği doğrudan YTD, diğer çeyrekler aynı yılın bir önceki çeyreğinden fark alınarak bulunuyor" — ardından dört çeyrek kayan toplam; satış 3C, faaliyet kârı 3H, ana ortaklık net kârı 3Z — çekirdek belli.
  - [temel-değerleme; M] "FK = Güncel Hisse Fiyatı / Yıllıklandırılmış HBK" — yıllık HBK son dört çeyrek — çekirdek belli.
  - [temel-değerleme; M] "ROE = Yıllık Net Kâr / (Cari + Geçen Yıl Özsermaye) / 2" — kaynak böyle yazar; açıklamanın istediği payda (cari + geçen yıl aynı çeyrek özsermayesi)/2 — çekirdek belli.
- Örnek ve sonuç: görselden: SAYAS yıllık kâr 166.304.000 + 153.185.000 − 63.332.000 = 256.157.000; HBK 3,316; fiyat 73,15; F/K 22,06; yıllık FAVÖK 165.298.000; FD/FAVÖK 33,15. TCELL 2022/12 HBK 7,00; 2024/9 yıllık HBK 21,23. 2022/9 değeri 5,53, 2021/9 + 2022/3 + 2022/6 + 2022/9 toplamıdır; 2021/12 yok.
- Tansu'nun vurgusu: "Ben bazen KAP'tan bilançoları alır kendi sistemimi kendim kurarım."
- Belirsiz: TCELL 5,53 dört gözlem toplamı olarak doğru, dört ardışık çeyrek TTM olarak eksiktir; arada 2021/12 kayıptır. ROE satırını işlem sırasıyla okumak ile açıklamadaki ortalama özsermaye paydasını okumak farklı sonuç verir.
- YORUM: ROE'nin düzeltilmiş yazımı net kâr / ((cari + geçen yıl aynı çeyrek özsermayesi)/2)'dir; bu kaynak alıntısı değil, açıklamayla uyumlu düzeltmedir. Duran varlık 1BG+1BGA+1BH bir stok kalemidir; dört çeyrek toplamına sokulmaz.

### X407 · 2024-03-24 18:39:17 UTC · DuPont bileşenleri ve borç oranının paydası
- Bağlı: R002; Öneri: tema-4 #7
- Yazar: T (KCAER kısa metni) + M (2025 açıklamalar) + G (sektör tablosu).
- Kaynak: 1771970054793433148 (2024-03-24 18:39:17 UTC), 1918417139813187678 (2025-05-02 21:27:43 UTC), 1918458073099710657 (2025-05-03 00:10:22 UTC), 1979208183236157837 (2025-10-17 15:29:37 UTC).
- Fikirler:
  - [temel-değerleme; M] "ROE = Net Kar Marjı × Aktif Devir Hızı × Finansal Kaldıraç." — NKM, yıllık satış / ortalama aktif, kaldıraç — çekirdek belli.
  - [boyut-risk; M] "%70'in üzerindeki borç oranları riskli."; "%30-50 arası dengeli sayılır." — <%30 muhafazakâr; kullanılan borç oranının paydası tutarsız — çekirdek belli.
- Örnek ve sonuç: KCAER metninde NKM %7,86 / sektör %4,30. Görselden: aktif kârlılık tablosu FROTO 11,450; TTRAK 10,198; DOAS 8,037; ASUZU 1,786; TOASO 1,738; KARSN 0,506; TMSN −3,687; OTKAR −7,843; sektör 5,619. Bu sektör değeri altı pozitif şirketin ortalamasına uyar; negatifler hariçtir.
- Tansu'nun vurgusu: "Gelelim #KCAER'e :)".
- Belirsiz: 1979208183236157837 finansal kaldıracı borç/özsermaye diye adlandırır; 1918417139813187678 varlık/özsermaye der. İlki borç oranı, ikincisi DuPont özsermaye çarpanı olarak okunur; aynı oran değildir. %70 eşikleri borç/varlık veya borç/özsermaye olarak okunabilir; kaynak netleştirmez.
- YORUM: DuPont çarpımının özsermaye çarpanı varlık/özsermayedir; borç/özsermaye ile doğrudan değiştirilmez. >%70 riskli sınıfını payda düzelmeden çalışır genel filtre diye yazmak doğru değildir.

### X408 · 2025-03-07 08:25:22 UTC · Black-Scholes fiyatı ve delta korunması
- Bağlı: yeni yöntem; Öneri: tema-4 #8
- Yazar: T (2025-03 zincirinin kısa anlatımı) + M (2025-04/07 eğitim metinleri) + G (kod ve çıktılar).
- Kaynak: 1897926533991268696 (2025-03-07 08:25:22 UTC), 1897926559081660560 (2025-03-07 08:25:28 UTC), 1911177641643983112 (2025-04-12 22:00:32 UTC), 1911177646052131219 (2025-04-12 22:00:33 UTC), 1942962939696156904 (2025-07-09 15:03:57 UTC).
- Fikirler:
  - [temel-değerleme; G] "b = r - q"; "d2 = d1 - sigma * np.sqrt(T)" — d1=(ln(S/X)+(r−q+σ²/2)T)/(σ√T); call=S·e^(−qT)N(d1)−X·e^(−rT)N(d2); put=X·e^(−rT)N(−d2)−S·e^(−qT)N(−d1) — kural tam (görselde formüller).
  - [ölçüm-ilkesi; M] "Opsiyon sadece vade sonunda kullanılabilir (Avrupa tipi)." — sabit faiz/volatilite, lognormal fiyat; maliyet ve arbitraj yok varsayımları — çekirdek belli.
  - [boyut-risk; M] "1000 * 0.5 = 500 adet put opsiyon almanız gerekir." — hatalı delta hedge örneği; düzeltme aşağıda — çekirdek belli.
- Örnek ve sonuç: görselden: S=100, X=130, T=1, r=0,05, q=0, σ=0,2 → call 1,6396. AAPL S=170,73, X=180, T=7/366, r=0,055, q=0, σ=0,260261 → 0,21169777189702543. Bunlar kaynak çıktılarıdır; kod çalıştırılarak yeniden hesaplanmadı. 1911177646052131219 metni 1,63 der; görsel 1,6396'dır.
- Tansu'nun vurgusu: "Black-Scholes modeli ile Apple (AAPL) hissesi için 180 kullanım fiyatlı (strike) call opsiyonunu fiyatlanması."
- YORUM: Tam delta korunması, put deltası −0,5 ve birim çarpanı 1 ise 1000/0,5=2000 opsiyon birimidir; 500 değildir. Sözleşme sayısı ayrıca sözleşme çarpanına bölünür. Model fiyatı ve eğitim örneği gerçekleşmiş kâr değildir.

### X409 · 2023-09-03 09:32:30 UTC · Sharpe net kâr marjı istikrar filtresi
- Bağlı: yeni yöntem; Öneri: tema-4 #9
- Yazar: T.
- Kaynak: 1698267718074438032 (2023-09-03 09:32:30 UTC), 1709805069644820609 (2023-10-05 05:37:49 UTC), 1780322525055996240 (2024-04-16 19:49:01 UTC), 1781414254576300469 (2024-04-19 20:07:10 UTC), 1794036593734418591 (2024-05-24 16:03:50 UTC).
- Fikirler:
  - [tarama-evren] "Özsermaye karlılığı yüksek F/K’sı 5-15 arasında olduğuna emin olun."; "Net kar marjı (sharpe) 2’nin üzerinde olsun" — F/K 5–15 ve adlandırılmış ölçü >2 — çekirdek belli.
  - [tarama-evren] "FK'sı 6-16 arası ve sharpe net kar marjı 2 üstü" — 2024-04 istikrar varyantı — çekirdek belli.
  - [tarama-evren] "1- sharpe net kar marjı 2 den küçük şirketlere,"; "2-patron şirketlerine,"; "3-büyüme şirketlerine YATIRIM YAPMA" — kişisel dışlama notu — çekirdek belli.
- Örnek ve sonuç: BRISA metninde ölçü 3,7; F/K 9,6 ve son on yılın diplerinde olduğu yorumu. CANTE'nin istikrarlı şirket sınıfında olmadığı anlatılır. Sonuç ölçümü yok.
- Tansu'nun vurgusu: "Kendime not"; "YATIRIM YAPMA".
- Belirsiz: "net kar marjı (sharpe)" marjın Sharpe benzeri istikrar ölçüsü veya doğrudan marj olarak okunabilir; formülü tanımsız. >2 ve <2 ifadeleri eşit 2'yi açık bırakır. F/K 5–15 ve 6–16 ayrı tarihli aralıklardır.

### X410 · 2024-04-18 21:31:35 UTC · F/K regresyonu, VIF ve Ridge
- Bağlı: R066; Öneri: tema-4 #10
- Yazar: T + G (model kullanım kodu ve çıktı).
- Kaynak: 1781073113205117347 (2024-04-18 21:31:35 UTC), 1824814340668617001 (2024-08-17 14:23:36 UTC), 1825279192390594981 (2024-08-18 21:10:46 UTC), 1825283202191167740 (2024-08-18 21:26:42 UTC), 1826661989126733986 (2024-08-22 16:45:30 UTC).
- Fikirler:
  - [temel-değerleme] "Çoklu doğrusal, polinomial, lasso, ridge modelleri ile çalışabiliriz." — aday modeller — yalnız fikir.
  - [ölçüm-ilkesi; G] "model with VIF < 10" — önceden seçilmiş on özelliği modele veren tahmin işlevi; görüntüde VIF hesaplayan/eleme yapan döngü yok — çekirdek belli.
  - [temel-değerleme] "Ridge regresyon optimal alpha 0,26 değeri ile 2024/6 dönem Bimaş F/K tahmini 20,89 olarak bulundu" — alpha 0,26; MSE 3,0899; RMSE 1,7578; R² 0,9613 metinden — çekirdek belli.
- Örnek ve sonuç: görselden: VIF<10 adlı model girişinde faaliyet kârı, FAVÖK, net kâr ve satış büyümesi; kapanış fiyatı; ROCE; temettü verimi; borç/özsermaye; sektör ROE; KV yükümlülük büyümesi. Çıktı 17,49075087388864. Ridge tablosu sekiz test satırı ve ileri F/K 20,897302 verir. Ayrı metinde denklem 24, tarihsel ortalama 24–25 ile kıyaslanır; aynı tahmin sanılmaz.
- Tansu'nun vurgusu: "Linçlemeyin, deneysel çalışma:)".
- YORUM: Önerinin "VIF < 10 kodu" ifadesi tam eleme kodu varmış gibi okunmamalı. Alpha/MSE/R² görselde değil metindedir. HBK'yı değişken yapmakla ilgili gönderi VIF itirazıdır; bütün veri setleri için otomatik dışlama kanıtı değildir.

### X411 · 2025-07-25 23:43:13 UTC · Convex Hull köşe seçimi ve durağanlık
- Bağlı: R178; Öneri: tema-4 #11
- Yazar: T (kısa girişler) + M (yöntem açıklamaları).
- Kaynak: 1948891823121801615 (2025-07-25 23:43:13 UTC), 1949378649817280840 (2025-07-27 07:57:42 UTC), 1949942724888506647 (2025-07-28 21:19:08 UTC), 1949942729116373465 (2025-07-28 21:19:09 UTC).
- Fikirler:
  - [portföy; M] "Önce Convex Hull ile 2 veya 3 köşe sektör seçilir." — her sektörden 3–4 hisse, ardından Markowitz; alternatif tek köşe veya 3–4 köşeye dağılım — çekirdek belli.
  - [momentum-seçim; M] "Her bir hissenin kaç periyotta köşe olduğu sayılır." — haftalık/aylık/çeyreklik tekrarlarda köşe istikrarını izleme — çekirdek belli.
  - [teyit-tetik; M] "Yüksek köşe süresi ve düşük GARCH volatilitesi olan hisseleri seç." — durağan köşe seçimini koşullu oynaklıkla süzme — çekirdek belli.
- Örnek ve sonuç: Somut portföy sonucu yok. Kesitsel momentum için 1/3/6 ay örnekleri vardır; durağanlık periyodu veya GARCH modeli sabitlenmiş değildir.
- Tansu'nun vurgusu: "Bu bilgiyi de kimse vermez çoğu da bilmez:)".
- Belirsiz: Durağanlık köşede kalma sıklığı olarak da düşük oynaklık olarak da anlatılır; tek sayısal kabul eşiği yok. Köşe olmak tek başına iyi performans demek değildir.
- YORUM: 1947006461487517762'nin sektör → Convex Hull → Sharpe fikri X023'te bulunduğundan tekrar kaydedilmedi; bu kayıt sayılı sektör/hisse seçimi ve durağanlık/GARCH eklerini tutar.

### X412 · 2025-04-20 08:00:27 UTC · NetYPP / satış ile kur duyarlılığı
- Bağlı: yeni yöntem; Öneri: tema-4 #12
- Yazar: M (uzun açıklamalar) + T (kısa çalışma girişleri).
- Kaynak: 1913865330448879926 (2025-04-20 08:00:27 UTC), 1915860915729166759 (2025-04-25 20:10:11 UTC), 1950865602647646516 (2025-07-31 10:26:19 UTC).
- Fikirler:
  - [temel-değerleme; M] "Yabancı para pozisyonu / Net satışlar oranı × Kur değişimi = Şirkete kar veya zarar etkisi." — net döviz varlıkları − döviz borçları; payda son dört gerçek çeyrek satış toplamı — çekirdek belli.
  - [boyut-risk; M] "sadece NetYP’ye değil, NetYP / Satış Oranı gibi çarpanlara da bakmak şart." — negatif pozisyonun ciroya göre büyüklüğü; faktör analizi ve GARCH ile birlikte okuma — çekirdek belli.
- Örnek ve sonuç: Metindeki oran %4,86, kur değişimi %10 → ciro etkisi %0,486. 100 milyon TL ciroda karşılığı 486.000 TL, yani 0,486 milyon TL'dir; metindeki 48,6 milyon TL yanlıştır. Verilen 6 milyar TL pozisyon aynı %4,86 oranında yaklaşık 123,46 milyar TL ciro gerektirir; 100 milyonluk örnek ayrı varsayımdır.
- Tansu'nun vurgusu: "Yaptım yine bir şeyler #python ile.".
- Belirsiz: Metnin 2024/12+09+06+03 toplamı, önceden farkı alınmış çeyrekler veya ham kümülatif değerler olarak okunabilir; yalnız ilk okuma TTM verir.
- YORUM: NetYPP bir bilanço pozisyonudur; yabancı yatırımcı fon giriş/çıkışı değildir. Yaklaşık kur duyarlılığı fiilen gerçekleşmiş ek kâr diye yazılmaz; kur sepeti, korunma ve vergi etkisi kaynakta modellenmemiştir.

### X413 · 2025-07-08 11:04:47 UTC · Klasik TOPSIS ve gri sayı varyantı
- Bağlı: R145 / R179; Öneri: tema-4 #13
- Yazar: T (kısa giriş ve kendi kod hedefi) + M (açıklamalar) + G (kod/örnek çıktı).
- Kaynak: 1942540360460259582 (2025-07-08 11:04:47 UTC), 1947985822071894179 (2025-07-23 11:43:06 UTC).
- Fikirler:
  - [tarama-evren; G] "weights = np.array([0.3, 0.3, 0.2, 0.2])" — sırasıyla NKM, ROE, ROA, borç/özsermaye; fayda x/√Σx², maliyet min(x)/x; Ci=D−/(D++D−) — kural tam (gösterilen kod).
  - [tarama-evren; M] "Bu bilgiler gri sayılarla ifade edilerek bir karar matrisi oluşturulmuştur." — çimento şirketlerinde aralık matrisi → fayda/maliyet normalizasyonu → eşit ağırlık → ideal uzaklıklar → kesin sayıya dönüşüm → yakınlık sıralaması — çekirdek belli.
- Örnek ve sonuç: görselden: klasik kod SISE 0,576603; TUPRS 0,576055; EREGL 0,346221. Kod yorumunda örnek finansal oranlar kullanıldığı yazılıdır; canlı bilanço taraması sonucu değildir. İkinci metin gri yöntem anlatır ama aralık girdilerini ve sayısal tabloyu vermez.
- Tansu'nun vurgusu: "Benim izlediğim yok, yazdığım kod ile direk iş yatırımdan bilanço üzerinden aşağıdaki finansal değerleri tek bir kod bloğu ile hesaplayarak bu çalışmayı yapmak."
- YORUM: İlk gönderideki "Gri TOPSIS" adı gösterilen kodla uyuşmaz: gri sayı/aralık işlemi yoktur, klasik TOPSIS'tir. Sonraki gri yöntem anlatımı ayrı tutuldu; tek ağırlık seti gibi birleştirilmedi.

### X414 · 2025-07-31 12:50:43 UTC · Duran varlık artışı ve RSI taraması
- Bağlı: R059; Öneri: tema-4 #14
- Yazar: T (kısa tarama metinleri) + M (karar matrisi ve açıklamalar).
- Kaynak: 1950901940524617991 (2025-07-31 12:50:43 UTC), 1950916832409403513 (2025-07-31 13:49:53 UTC), 1954964170585030772 (2025-08-11 17:52:34 UTC), 1955010441526022428 (2025-08-11 20:56:26 UTC), 1956635609449091123 (2025-08-16 08:34:16 UTC).
- Fikirler:
  - [tarama-evren] "Yatırımlardaki artış oranı %90'dan büyük olup günlük periyotta RSI>50 olan otomotiv hisseleri" — aynı çeyreğin bir yıl öncesine göre yatırım/duran varlık artışı >%90, günlük RSI>50 — çekirdek belli (RSI periyodu yok).
  - [temel-değerleme; M] "Yatırım yapan ama F/K’sı hâlâ makul seviyede olan şirketler uzun vadeli fırsat sunabilir." — DV artışı × F/K/sektör F/K matrisi; borç, satış, kârlılık ve nakit akışı teyidi — çekirdek belli.
- Örnek ve sonuç: FROTO metninde duran varlık artışı %54'ün üzerinde ve F/K sektörün altında anlatılır; bu ayrı örnek >%90 filtresinden geçiyor diye yazılmaz. Gerçekleşmiş yatırım getirisi yok.
- Tansu'nun vurgusu: "Neye yatırım yaptığınızı bilmeniz lazım".
- Belirsiz: Duran varlık artışı yeni kapasite yatırımı veya yeniden değerleme/enflasyon etkisi olabilir; tek başına fiziki yatırım kanıtı değildir. RSI'nin hesap periyodu yok.
- YORUM: R144 PD/DD çıpasıdır; doğrudan bu taramanın sahibi olmadığı için bağ R059'a daraltıldı. DV tutar büyümesi ile DV/toplam varlık payının değişimi ayrı ölçülerdir.

### X415 · 2025-08-16 20:45:43 UTC · Aynı Q2 döneminde ardışık büyüme
- Bağlı: R002 / R133; Öneri: tema-4 #15
- Yazar: T (tarama girişleri) + M (uzun açıklamalar).
- Kaynak: 1956819684713509048 (2025-08-16 20:45:43 UTC), 1956830336467243263 (2025-08-16 21:28:03 UTC), 1956848925543206980 (2025-08-16 22:41:55 UTC), 1957003613827420651 (2025-08-17 08:56:35 UTC).
- Fikirler:
  - [tarama-evren] "Son 4 yılda 2. çeyrek dönem net satışları sürekli artan şirketler nelerdir..." — 2022Q2<2023Q2<2024Q2<2025Q2; otomotiv ve BIST50 taramaları — çekirdek belli.
  - [ölçüm-ilkesi; M] "CAGR3y: 2022’den 2025’e kadar olan 3 yıllık bileşik yıllık büyüme oranı." — dört aynı çeyrek arasında üç yıllık büyüme — çekirdek belli.
  - [giriş/hedef-çıkış; M] "Q2 bilançoları öncesinde pozisyon alıp açıklama sonrasında satmayı deneyebilir." — esas faaliyet kârı büyümesine dayanan sezonluk işlem fikri; gün/eşik yok — yalnız fikir.
- Örnek ve sonuç: Metinde Q2 satış CAGR'ı FROTO %83,9; OTKAR %71,4; ASUZU %61,7. ENKAI Q2 esas faaliyet kârı CAGR'ı %42,6 olarak anlatılır. Bunlar bilanço büyümesi; hisse getirisi değildir.
- Tansu'nun vurgusu: "Pratikte momentumu en yüksek sektmrlerde ya da endekslerde bu taramayı yaparsak hata payımız azalır."
- YORUM: CAGR3y=(son Q2/ilk Q2)^(1/3)−1, tanımdan çıkan formüldür. Nominal artışın reel büyüme olduğunu kaynak ispatlamaz. R118 rejim raporudur; mevsimsel bilanço bağı R002/R133 ile kuruldu.

### X416 · 2025-07-19 19:23:59 UTC · Likidite filtreleri ve borç payları
- Bağlı: R060 / R134; Öneri: tema-4 #16
- Yazar: T (asit-test formülü ve kısa borç notu) + M (geniş strateji açıklaması) + G (FROTO oran grafikleri).
- Kaynak: 1946652254116684019 (2025-07-19 19:23:59 UTC), 1949414090499112967 (2025-07-27 10:18:32 UTC), 1949421615135240509 (2025-07-27 10:48:26 UTC), 2086152222870536647 (2026-08-08 18:07:03 UTC), 2086514064688124094 (2026-08-09 18:04:53 UTC).
- Fikirler:
  - [tarama-evren; M] "Cari Oran 1.5 Üzerinde Olmalı"; "Borç Oranı (Toplam Borç / Toplam Varlıklar) %50’nin Altında Olmalı" — NİS>0, artan faaliyet marjı ve pozitif işletme nakdi ile birlikte — çekirdek belli.
  - [temel-değerleme] "(Toplam Dönen Varlıklar -Stoklar) / Toplam Kısa Vadeli Yükümlülükler" — basit asit-test; ayrı anlatımda son dört çeyrek izleme ve <1 risk örneği — kural tam (oran).
  - [boyut-risk] "kısa vadeli finansal yükümlülüklerin kısa vadeki yükümlülükler içindeki payının %10 dolayında olması güzel bir durumdur." — finansal borç payı; zorunlu <%10 kapısı değil — çekirdek belli.
- Örnek ve sonuç: görselden: FROTO 2026/06 KV finansal yükümlülük payı yaklaşık %31, %10 değil. Ayrı borç/özsermaye grafiğinde FROTO son değer yaklaşık %173, sektör yaklaşık %452; metin FROTO için yaklaşık %175 der. İki grafiğin paydası farklıdır.
- Tansu'nun vurgusu: "Basit halini kullanıyorum".
- Belirsiz: %10 notu hedef/olumlu örnek veya FROTO grafiğinin açıklaması olarak okunabilir; grafikte son gözlem yaklaşık %31 olduğundan ikinci okuma desteklenmez. %173 ile yaklaşık %175 farkı kesin tablo veya yuvarlanmış anlatım farkı olabilir; grafik yaklaşık okunmuştur.

### X417 · 2024-06-02 13:46:36 UTC · Black-Litterman ve 21 günlük pencere
- Bağlı: R110; Öneri: tema-4 #17
- Yazar: T (kısa tercihler) + M (model seçimi açıklaması).
- Kaynak: 1797263549892276362 (2024-06-02 13:46:36 UTC), 1797263555382702421 (2024-06-02 13:46:37 UTC), 1940657356347474399 (2025-07-03 06:22:24 UTC), 2096143361002385717 (2026-09-05 07:48:16 UTC), 2096146762188611697 (2026-09-05 08:01:47 UTC).
- Fikirler:
  - [portföy] "21 günlük rolling black litterman benim tercihim" — 21 gün kayan pencere — çekirdek belli.
  - [portföy; M] "Başlangıçta Markowitz ile başlanmalı, deneyim arttıkça Black-Litterman ile görüş entegrasyonu yapılmalı." — görüş zayıfsa Markowitz; görüş varsa BL — çekirdek belli.
- Örnek ve sonuç: 2024 metnindeki 100.000 TL'nin hisse/altın/kriptoya dağıtılması soru örneğidir; gerçekleşmiş tahsis veya getiri değildir. 2026 fon sepeti için geçmiş ve ileri çalışma planı vardır; sonuç yok.
- Tansu'nun vurgusu: "benim tercihim".
- Belirsiz: 21 gün takvim günü veya işlem günü olarak okunabilir; kaynak yalnız "günlük" der. Görüş matrisi, güven, riskten kaçınma ve yeniden dengeleme sıklığı yok.

### X418 · 2026-08-27 18:49:55 UTC · Pair Health ve tarayıcı sınıfları
- Bağlı: R251 / R034; Öneri: tema-4 #18
- Yazar: T (kısa çıktı yorumu ve sahiplenme) + M (Pair Health açıklaması) + G (tarayıcı tablosu).
- Kaynak: 2093048380297547956 (2026-08-27 18:49:55 UTC), 2096167419941130368 (2026-09-05 09:23:52 UTC).
- Fikirler:
  - [stop-geçersizlik; M] "son otuz, altmış veya doksan günlük hareketli pencereler" — rolling korelasyon; beta stabilitesi; half-life; eşbütünleşme ile birlikte güncel çift sağlığı — çekirdek belli.
  - [tarama-evren; G] "YENİ AL SİNYALİ (5 çift)"; "DEVAM EDEN FIRSAT (1 çift)"; "BOLGEYE YAKLASIYOR (12 çift)" — ayrı izleme/sinyal sınıfları; tek eşik formülü verilmez — çekirdek belli.
- Örnek ve sonuç: görselden: TSKB/SAHOL K/Z +5230 TL, +%5,2; Z=+2,658→+2,943, SAHOL AL. Devam eden fırsat TSKB/ISCTR, Z=−2,534→−1,758, TSKB izle. TCELL/ISCTR yeni AL satırında Z=−1,877→−2,010; başlığın tek bir |Z|>2 kuralından üretildiği gösterilmez. Metin SAHOL için %5 der; bu görselle uyumludur.
- Tansu'nun vurgusu: "Size de bilgi vereyim.". Uzun Pair Health tanımı M biçimlidir.
- Belirsiz: Metin "SAHOL yeni bir sinyal" derken tabloda beş yeni sinyal vardır; yalnız yeni değişeni anlatma veya eski çıktıyla eşleşmeyen yorum olarak okunabilir. Z okları geçmiş→son veya son→önceki olabilir; tüm satırları ortak dönüş yönüyle okumak çelişir. Kaynaktan kesin zaman sırası çıkarılmadı.
- YORUM: R251 tek çift rotasyon raporudur; bu tarayıcıya aynı giriş/çıkış koşulları otomatik taşınmadı. R034'ün rolling eşbütünleşmesi ile rolling korelasyon farklı kontrollerdir.

### X419 · 2024-02-20 20:02:57 UTC · Minimum varyans, Sharpe oranlı ağırlık ve MC
- Bağlı: R177 / R173 / R182; Öneri: tema-4 #19
- Yazar: T (kendi kitap/kod anlatımı ve tercihleri) + G (kod/çıktı).
- Kaynak: 1760032311100465169 (2024-02-20 20:02:57 UTC; ust.jsonl, kullanıcı The_Tansu_), 1771531828676919771 (2024-03-23 13:37:56 UTC), 1822304577560985704 (2024-08-10 16:10:42 UTC), 1878777386839503131 (2025-01-13 12:13:29 UTC), 1890128570749710462 (2025-02-13 19:59:02 UTC).
- Fikirler:
  - [portföy; G] "weights = sharpe_ratios / sharpe_ratios.sum()" — tekil Sharpe oranlarını toplamına bölme — kural tam (gösterilen kod).
  - [portföy; G] "weights = inv_cov_matrix.dot(ones) / ones.dot(inv_cov_matrix).dot(ones)" — w=Σ⁻¹1/(1ᵀΣ⁻¹1); minimum varyans; kısa pozisyon sınırı gösterilmez — kural tam.
  - [portföy; G] "N_PORTFOLIOS = 10 ** 5"; "N_DAYS = 252" — lognormal rastgele ağırlıklar satır toplamıyla normalize; yıllık ortalama ve kovaryans ×252; volatilite √(wᵀΣw) — kural tam (kod).
- Örnek ve sonuç: görselden: beş hisse ham ağırlıkları ARCLK 0,264627; EREGL 0,239722; GARAN 0,178296; THYAO 0,049714; TUPRS 0,267641. Üç ondalığa yuvarlanınca toplam 1,001 olur; ham toplam 1'dir. Kod görüntüleri okunmuştur, çalıştırılmamıştır.
- Tansu'nun vurgusu: "markowitz kodunu monte carlo lie yazıp optimize ediyorum.".
- Çelişir: R182'nin M biçimli "Monte Carlo yerine Spicy" tercihini istisnasız Tansu kuralı saymak, kendi açık MC kullanım sözüyle çelişir. Kendi gönderisi güçlüdür; R185'teki risk-of-ruin MC kullanımı farklı roldür.
- YORUM: Sharpe'a orantılı ağırlıklandırma kovaryansı hesaba katan maksimum portföy Sharpe optimizasyonuyla aynı değildir. 1760032311100465169 tweets.jsonl'de yok ama ust.jsonl'de Tansu yazarıyla vardır; kullanıcı sorusu değil Tansu'nun yanıtı kanıttır.

### X420 · 2024-08-10 19:51:40 UTC · Risk parity ve model seçimi
- Bağlı: R074 / R177; Öneri: tema-4 #20
- Yazar: T (kitap/kod girişleri) + M (2025 açıklama) + G (kitap grafiği ve seçim metni).
- Kaynak: 1822360182682165714 (2024-08-10 19:51:40 UTC), 1827476527899894046 (2024-08-24 22:42:11 UTC), 1944760309123575813 (2025-07-14 14:06:04 UTC).
- Fikirler:
  - [portföy; M] "her bir varlık, toplam portföy riskine eşit düzeyde katkıda bulunsun." — risk katkılarını eşitleme hedefi — çekirdek belli.
  - [portföy; G] "Use Risk Parity if:"; "Use Markowitz Portfolio if:" — dengeli/eşit risk dağılımı için risk parity; belirli min risk veya max Sharpe hedefi için Markowitz — çekirdek belli.
- Örnek ve sonuç: görselden: BIMAS/ EKGYO/ GUBRF risk parity ağırlıkları yaklaşık 0,43/0,30/0,27; min varyans yaklaşık 0,64/0,20/0,16. Grafik tahsis karşılaştırmasıdır; getiri sonucu yok.
- Tansu'nun vurgusu: "risk parity portföyünü oluşturarak markowitz ile karşılaştırmak çok mantıklı.".
- YORUM: Ters volatilite ağırlığı, korelasyonların etkisini içeren tam eşit risk katkısı çözümü değildir; açıklamadaki sezgisel düşük oynaklığa fazla pay fikri tam formül diye sunulmadı. Kovaryans penceresi ve hesap yöntemi yok.

### X421 · 2024-04-24 18:46:40 UTC · Kripto tahsis sınırının üç sürümü
- Bağlı: yeni yöntem; Öneri: tema-4 #21
- Yazar: T (Tansu'nun cevapları; karşı tarafın sözü kullanılmadı).
- Kaynak: 1783205936427119005 (2024-04-24 18:46:40 UTC), 1840693444294975693 (2024-09-30 10:01:30 UTC), 1860757961032835441 (2024-11-24 18:50:43 UTC).
- Fikirler:
  - [boyut-risk] "portföyün maks. %1 ile %5 ini ayırın" — 2024-04 üst sınır aralığı — kural tam.
  - [boyut-risk] "Portföyün Max %4’ini geçmemeli kripto yatırımı" — 2024-09; Tansu bunu kendine uygulamaz ("Bana göre değil. Kimine göre öyle."), soruyu soran kişiye koşullu sınırdır — çekirdek belli.
  - [boyut-risk] "tüm portföyünüzün max %5-10'unu aşmamalı" — 2024-11 üst sınır aralığı — kural tam.
- Örnek ve sonuç: Kendi gerçekleşmiş kripto yatırımı veya getiri yok; ilk sözde kriptoya hiç girmediğini belirtir.
- Tansu'nun vurgusu: "Kriptoya hiç girmem"; "kripto tavsiye etmem".
- Belirsiz: Farklı muhataplara bağlama göre sınır veya zamanla değişen sınır olarak okunabilir; tarih sırası açık, tek güncel yüzde seçilemez.

### X422 · 2024-03-17 12:20:29 UTC · Ülke risk primi örneklerinin farkı
- Bağlı: R070; Öneri: tema-4 #22
- Yazar: T (2024 kendi hesapları) + M (2025 WACC açıklaması).
- Kaynak: 1769338011815211270 (2024-03-17 12:20:29 UTC), 1778895335592472990 (2024-04-12 21:17:52 UTC), 1911632045777789394 (2025-04-14 04:06:10 UTC).
- Fikirler:
  - [temel-değerleme] "Türkiye 10 yıllık tahvil bono faizini %27, 5 yıllık CDS %5,1, ABD 5 yıllık CDS’ini de %0,58 alarak ülke risk primini %5,07" — DOAS örneği, toplam ERP %10,07 — çekirdek belli.
  - [temel-değerleme] "Türkiye 5 yıllık CDS %5,1 alınmıştır."; "Ülke risk primi %5,7 alınmıştır." — Nisan örneği, risk primi %5 ve TR 10Y %27 — çekirdek belli.
  - [temel-değerleme; M] "WACC=wd⋅rd⋅(1−T)+wc⋅rs" — CAPM, temettü büyümesi ve borç getirisi+RP ile üç rs ortalaması; RP genelde %3–5 — çekirdek belli.
- Örnek ve sonuç: R070'teki 1,12 çarpanını Mart girdilerine uygularsak (5,1−0,58)×1,12=%5,0624, iki ondalıkta %5,06; gönderi %5,07 bildirir. Nisan %5,7 ise 5,1×1,12=%5,712 ile uyumludur; ABD CDS çıkarılmamıştır. Bunlar elle aritmetik karşılaştırmadır; kod çalıştırılmadı.
- Tansu'nun vurgusu: "WACC sürecini nasıl kurguluyorum?".
- Belirsiz: Mart %5,07, yuvarlanmamış CDS girdisi veya küçük yuvarlama/hesap farkı olabilir. Nisan %5,7 ise farklı risk primi yaklaşımı veya ABD CDS çıkarımının atlanması olabilir; tek formülle tutarlı ilan edilmez.
- YORUM: 2025 metnindeki "DCF – Dividend Discount Model" başlığı temettü indirgeme modelini anlatır; FCFF DCF ile karıştırılmaz. Nisan sembolü kaynakta "#TAOSO" yazılıdır; alıntıda yazım korunur.

### X423 · 2026-04-08 18:07:42 UTC · PD/DD penceresinde anlık veri ve erken araç hatası
- Bağlı: R062 / R144; Öneri: tema-4 #23
- Yazar: M (PD/DD açıklaması) + T (kısa araç mesajı) + G (çıktılar).
- Kaynak: 2041941067025494204 (2026-04-08 18:07:42 UTC), 2041968928205766731 (2026-04-08 19:58:25 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "2025/12 dahil geriye 8 çeyrek + anlık"; "2025/12 dahil geriye 36 çeyrek + anlık" — kısa/uzun PD/DD referansı; sektör sekiz hisse — kural tam (görselde pencere).
  - [temel-değerleme; G] "Yilin Kalaninda Bekl. Kar" — erken araçta beklenen tam yıl kârı kalan dönem yerine kullanılmış — yalnız fikir (hatalı örnek, kural olarak alınmadı).
- Örnek ve sonuç: görselden: ASUZU 2025/12 PD/DD 0,99; sektör 2,18; kısa 1,38 / sektör 2,60; uzun 0,98 / sektör 2,56. Erken araç dönem 2023/12: özsermaye 11.917.205.852; beklenen kâr 3.028.332.000; 3Z 2.330.587.214; kalan kâr yine 3.028.332.000; beklenen özsermaye 14.945.537.852. Tahmin tam yıl ise kalan 697.744.786, özsermaye 12.614.950.638 olmalıydı. R062'nin sonraki sürümü yıl sonu tahmininden 3Z'yi çıkarır.
- Tansu'nun vurgusu: "Böyle çalışıyor".
- Belirsiz: "Beklenen Kar" tam yıl kârı veya ayrıca beklenen gelecek kârı olabilir; aynı tutarın "Yilin Kalaninda" alanına kopyalanması ve sonraki R062 formülü ilk okumada hatayı destekler. 2025/12 çarpanlarını 2023/12 bilançoya uygulama, geçmiş değerleme canlandırması veya dönem uyumsuzluğu olabilir; çıktı bunu açıklamaz.
- YORUM: R144'ün PD/DD çıpa metni yinelenmedi; yeni katkı +anlık pencere tanımı ve erken çıktıdaki kalan dönem ayrışmasıdır.

### X424 · 2023-09-30 08:05:45 UTC · Bedelsiz potansiyelinin bilanço fikri
- Bağlı: yeni yöntem; Öneri: tema-4 #25
- Yazar: T + G (Tansu imzalı değerleme tabloları).
- Kaynak: 1708030356564160854 (2023-09-30 08:05:45 UTC), 1850969302347989014 (2024-10-28 18:34:05 UTC), 2086040274434715957 (2026-08-08 10:42:12 UTC).
- Fikirler:
  - [temel-değerleme] "ödenmiş sermayesi düşük kalmış ancak yıllar içinde elde ettiği kârlar ve diğer yedekleri büyümüşse, bedelsiz potansiyeli yüksek çıkar." — sermaye ile birikmiş kâr/yedek kıyası; oran/eşik yok — çekirdek belli.
- Örnek ve sonuç: görselden: TTRAK ve yeniden paylaşılan SAYAS tablolarında "BEDELSİZ POTANSİYELİ" alanı vardır ama boştur. Tutar veya gerçekleşmiş bedelsiz sonucu verilmez.
- Tansu'nun vurgusu: "Örneklerini yaparız".
- YORUM: Boş alan 2023'te başlığın bulunduğunu kanıtlar; o tarihte çalışan hesap/formül veya yüksek bedelsiz potansiyeli kanıtlamaz.

### X425 · 2023-08-25 21:17:15 UTC · SAYAS İNA örneği ve iki sonuç
- Bağlı: R153 / R165; Öneri: tema-4 #26
- Yazar: T + G (imzalı değerleme ve nakit akımı tablosu).
- Kaynak: 1695183583676113357 (2023-08-25 21:17:15 UTC), 1695389783147581542 (2023-08-26 10:56:37 UTC).
- Fikirler:
  - [temel-değerleme] "hisse değeri 147TL bulunmuştur." — SAYAS İNA — çekirdek belli (varsayımlar ayrışıyor).
  - [temel-değerleme] "2024 yılında satış gelirleri %100 artacağı ve takip eden yıllarda %40 büyüme sağlayacağı varsayılmıştır." — metin varsayımı; tabloda farklı takvim/büyümeler — çekirdek belli.
- Örnek ve sonuç: görselden: ilk tablo on projeksiyon sütununda büyüme %50/150/50/40/40/20/20/18/15/15; terminal sütunu %5, ayrıca sonsuz dönem büyümesi %3. AOSM %13,5; FAVÖK marjı ilk %23,1, sonra %20,8. Firma değeri 11.379.300; sermaye 77.250; hisse 147,30; son fiyat 74,00; potansiyel %99. Ertesi gün özet tabloda İNA 133,71, nihai karma hedef 143,98 ve fiyat 73,15'tir.
- Tansu'nun vurgusu: "oldukça muhafazakar yaklaşarak yaptığım indirgenmiş nakit akımları analizinde".
- Belirsiz: 147,30→133,71 farkı parametre güncellemesi veya hesap/aktarım hatası olabilir; açıklama yok. Metin 2024 büyümesini %100 der, tabloda ikinci sütun %150'dir. Yıl başlıklarında 2024T tekrarı ve 2030T tekrarı vardır; yanlış etiket veya farklı model aşaması olabilir.
- YORUM: Terminal sütun büyümesi %5 ile sonsuz dönem %3 birbirinin yerine kullanılmadı. Potansiyel, gerçekleşmiş getiri değildir. Ağırlık tarihçesi X401'de; burada yalnız SAYAS nakit akımı örneğinin farklı katkısı tutuldu.

### X426 · 2026-05-09 18:27:04 UTC · Günlük sabit oran dengelemesi ve oran taraması
- Bağlı: R030 / R078; Öneri: tema-4 #27
- Yazar: T + G (backtest grafiği/tablosu).
- Kaynak: 2053179966284530147 (2026-05-09 18:27:04 UTC), 2053377141421584469 (2026-05-10 07:30:35 UTC).
- Fikirler:
  - [portföy] "Günlüktür" — dengeleme sıklığı günlük — kural tam (sıklık).
  - [ölçüm-ilkesi; G] "Vol Oranı | Aktif Getiri | Pasif Getiri" — %0…%100, on puan aralıkla oran taraması; tüm dönem / alt dönem karşılaştırması — çekirdek belli (bileşen kimliği yok).
- Örnek ve sonuç: görselden: grafik 2015-01-02→2025-12-30, vol oranı %30; aktif günlük dengelenen, pasif al-tut, BIST100. Tüm dönem tablo başlığı 2015-01-01/2025-12-31; %30 aktif %3426,22 / pasif %833,65. Kırmızı kutu %40 satırındadır: %3221,86/%707,22; en yüksek satır %30'dur. 2023-01-01/2025-12-31 alt dönem en yüksek satır %20: %109,42/%66,20. Bunlar kaynak backtest sonuçlarıdır.
- Tansu'nun vurgusu: "BIST al tut bekle yeri değildir kardeşim al ispatı".
- Belirsiz: "Vol" bileşeni hisse veya başka oynak varlık olabilir; kimliği ve ikinci bileşen yazılı değil. Grafik ve tablonun başlangıç/bitiş tarihleri farklıdır; işlem günü/takvim aralığı ayrımı veya etiket farkı olabilir.
- YORUM: Kırmızı kutu optimum anlamına gelmez. R078'teki farklı gerçek örnekte dengeleme pasiften düşük kalmıştır; buradaki backtest evrensel üstünlük kuralına çevrilmez.

### X427 · 2024-02-25 16:18:18 UTC · Uzun vade/trade tahsisi ve yeniden yatırım
- Bağlı: yeni yöntem; Öneri: tema-4 #28
- Yazar: T (kişisel tahsis, temettü ve aylık alım) + M (2025 pasif örnek ve 2026 sepet metni).
- Kaynak: 1761787714523865301 (2024-02-25 16:18:18 UTC), 1769351216369213499 (2024-03-17 13:12:57 UTC), 1783840694043623592 (2024-04-26 12:48:58 UTC), 1987747948675952790 (2025-11-10 05:03:36 UTC), 2100012254636683371 (2026-09-16 00:01:52 UTC).
- Fikirler:
  - [portföy] "portföyümün %80 i uzun vadeli %20 si de trade olarak tutuyorum." — kişisel %80/%20 tahsis — kural tam.
  - [portföy] "bununla yine #doas alacağım." — temettüyü aynı hisseye yeniden yatırım — çekirdek belli.
  - [portföy] "Ortalama maliyet mantığı ile her ay da düzenli toplarım arkadaş." — aylık düzenli alım; tutar yok, hedef 2028–2030 — çekirdek belli.
  - [boyut-risk; M] "Altın, döviz veya para piyasası fonlarıyla sepet yapmak lüks değil, zorunluluktur." — varlık sınıfı çeşitlendirmesi; oran yok — yalnız fikir.
- Örnek ve sonuç: DOAS 540 lot için yaklaşık 20.000 TL temettü beklediğini ve yeniden alım yapacağını söyler; gerçekleşen alım sonucu yok. %70 hisse/%30 tahvil, Norveç fonu anlatımındaki değişebilir örnektir; Tansu'nun kişisel tahsisi değildir.
- Tansu'nun vurgusu: "Temel analize çok önem veriyorum".
- YORUM: Çekirdek-uydu adı önerinin yorumudur; kendi sözündeki ayrım uzun vadeli yatırım / trade'dir. M sepet önerisi ve yabancı fon örneği kendi ölçülmüş tahsis kuralı diye yazılmadı.

### X428 · 2024-10-30 22:02:00 UTC · Callable tahvil, KMV ve Merton borç değeri
- Bağlı: R061; Öneri: tema-4 #29
- Yazar: T (kısa eğitim soruları) + G (faiz ağacı, KMV ders görseli ve kod). Ders görsellerinin üreticisi açık değil; Tansu'nun kendi formülü diye yazılmadı.
- Kaynak: 1851746402830807298 (2024-10-30 22:02:00 UTC), 1851754725680488551 (2024-10-30 22:35:05 UTC), 1875619396414251058 (2025-01-04 19:04:46 UTC).
- Fikirler:
  - [temel-değerleme; G] "duration" — (P−−P+)/(2P0·dy); nominal 100$, yıllık kupon %5,25; bir yıl sonra 100$'dan callable; dy=100 bps — kural tam (görselde).
  - [boyut-risk; G] "EDF = P(A_T ≤ DPT)" — KMV görselinde DPT temerrüt eşiği; ln(A0/DPT) ve (μA−½σA²)T; DD paydası gösterilmez — çekirdek belli.
  - [temel-değerleme; G] "debt_price = A - call_price" — Merton kodu A=100,D=90,r=0,05,γ=0,02,T=1,σ=0,3 — kural tam (gösterilen kod).
- Örnek ve sonuç: görselden: faiz ağacı %4,500 → %4,976/%4,074 → %6,757/%5,532/%4,530; callable duration 1,66, option free 2,75. Ağaç bugünkü fiyatı 100,460, duration tablosu callable P0=101,431 gösterir; farklı fiyat senaryoları birleştirilmez. Merton kod çıktısı 81,76. Kod yeniden çalıştırılmadı.
- Tansu'nun vurgusu: "DD'yi bulmaya çalışacağız."; "Temerrüde uzaklık!".
- Belirsiz: Tahvil ve KMV görselleri Tansu'nun hazırladığı ders materyali veya dışarıdan paylaştığı materyal olabilir; üretici imzası yok. Ağaç fiyatı ile duration tablosu P0 farkı ayrı örnek veya tutarsız tablo olabilir; açıklanmıyor.
- YORUM: Nakit ödeme γ>0 iken kodun A−call ifadesiyle çıktı 81,76'sı kaydedildi; dağıtılan nakdin hangi alacaklıya ait olduğu yazılı değildir. Standart model adı kaynak yazarlığını kanıtlamaz; bu kayıt G materyali ve Tansu'nun kullanım ilgisini tutar.

### X429 · 2024-11-17 01:06:20 UTC · Çift stratejisinin farklı türevleri
- Bağlı: R101 / R091; Öneri: tema-4 #30
- Yazar: T (tavan ve Granger/HMM kısa fikri) + M (spek çift ve video açıklaması) + G (çift ağı).
- Kaynak: 1857953385569190399 (2024-11-17 01:06:20 UTC), 1898476669851316502 (2025-03-08 20:51:24 UTC), 1922967215969542347 (2025-05-15 10:48:05 UTC), 1941240803654877456 (2025-07-04 21:00:48 UTC), 1999361321435811868 (2025-12-12 06:11:00 UTC).
- Fikirler:
  - [tarama-evren] "O tavan olan hisse bizim için bir nimet olabilir." — tavan olan hisseye yüksek koreli eş arama — çekirdek belli.
  - [çift; M] "aynı sektörde ya da benzer temada başka bir Spek hisseyle bu ilişki yakalanabilir." — spek–spek korelasyon/eşbütünleşme — çekirdek belli.
  - [rejim; M] "GVX'i bir al-sat sinyali olarak değil" — altın–DXY stratejisini açıp durduran rejim filtresi; eşik yok — çekirdek belli.
  - [çift] "Granger HMM ve pairs trading güzel bir sistem yapar:)" — üç yöntemin birleşimi; bağlama/formül yok — yalnız fikir.
- Örnek ve sonuç: görselden: eşbütünleşik çift çalışmasında düğüm/kenar ağı gösterilir; sayısal test eşiği yok. Bu görsel tek başına t-SNE uygulamasını kanıtlamaz. ML hattındaki açık t-SNE adımı X403'te tutuldu. Gerçekleşmiş getiri yok.
- Tansu'nun vurgusu: "Artık tavan hisselere bakmayacağız iç çekerek, tavanlar bizim için fırsat!".
- Çelişir: R091'in "HMM yapmanıza gerek yok" sözü ile Granger/HMM birleşimi fikri ayrışır.
- Belirsiz: HMM fikri sonradan terk edilmiş veya yalnız başka çift modeli için düşünülmüş olabilir; R091 trend rejimi içindir. Tek kesin güncel HMM şartı çıkarılmaz.

### X430 · 2026-09-07 21:05:46 UTC · VİOP short ile beta ayarlı hedge
- Bağlı: yeni yöntem; Öneri: tema-4 #31
- Yazar: T (kısa cevap girişi) + M (açıklayıcı fon/hedge anlatımı; kaynak kullanıcı sorusu değil Tansu'nun yanıtıdır).
- Kaynak: 2097068834284863827 (2026-09-07 21:05:46 UTC).
- Fikirler:
  - [boyut-risk] "hisse seçimiyle long kalıp, piyasa betasını VİOP short ile kontrollü tutma stratejisine benziyor." — uzun hisse seçimi + kısa endeks; beta ayarı — çekirdek belli.
- Örnek ve sonuç: Metinde THF brüt hisse yaklaşık %84,6; VİOP short/NAV %20,4; hedge sonrası net hisse %64,2; beta ayarlı net piyasa riski yaklaşık %38. %84,6−%20,4=%64,2; %38 için beta girdileri ve hesap formülü verilmez. Fon davranışının yorumu; Tansu'nun kendi işlem sonucu değil.
- Tansu'nun vurgusu: "Bence bunu yükselişe güvenmiyorlar diye tek başına okumak doğru olmaz.".
- YORUM: Fonun niyetleri olası açıklamalardır; kanıtlanmış yönetici kararı veya Tansu'nun kişisel hedge kuralı diye yazılmaz.

### X431 · 2024-08-11 09:27:21 UTC · Portföy kurmadan VIF kontrolü
- Bağlı: R066 / R110; Öneri: tema-4 #32
- Yazar: T.
- Kaynak: 1822565459905888316 (2024-08-11 09:27:21 UTC), 1823403053212475711 (2024-08-13 16:55:39 UTC).
- Fikirler:
  - [portföy] "Baştan VIF değerine ya da variance-covariance matrisine bakılması taraftarıyım." — portföy kurulmadan çoklu bağımlılık kontrolü — çekirdek belli.
  - [boyut-risk] "10 üzeri olmasın, 5 üstü olmazsa daha harika olur." — VIF≤10, tercih ≤5; kaynak eşitliği dışlamaz — çekirdek belli (hesap yöntemi/pencere yok).
- Örnek ve sonuç: Somut portföy, VIF ölçümü veya gerçekleşmiş korunma sonucu verilmez.
- Tansu'nun vurgusu: "birden fazla hisseden oluşan portföyünüz varsa nolur VİF değerini kontrol edin.".
- YORUM: Önerinin <10 / tercih <5 yazımı, kaynaktaki "üzeri olmasın" ile ≤10 / ≤5 olarak düzeltildi. VIF süzgeci tek başına hedge pozisyonu kurmaz. X410 F/K regresyonunun VIF'idir; bu kayıt ayrı portföy rolüdür.

### X432 · 2025-07-05 18:18:59 UTC · EFK değişimi ve bilanço sonrası fiyat tepkisi
- Bağlı: yeni yöntem; Öneri: tema-4 #33
- Yazar: T (ödev cümlesi) + G (araç tablosu).
- Kaynak: 1941562469320884677 (2025-07-05 18:18:59 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "EFK Artış Oranı (%)"; "Bilanço Sonrası Fiyat (40-55 Gün)" — önceki 2024/12 ve son 2025/3 EFK; bilanço öncesi fiyat ile 40–55 gün sonrası fiyat kıyası — çekirdek belli.
- Örnek ve sonuç: görselden: IHLGM EFK −127.864.460→−36.056.694, artış %71,80; fiyat 1,78→1,81, değişim %1,69; güncel 2,43, güncel artış %34,25. Diğer satırlar ADESE EFK −%78,50/fiyat −%6,14; RGYAS −%74,12/+%2,92; SONME −%75,05/−%2,13. Dolayısıyla görselde sonuç vardır; yalnız "ödev" denilerek yok sayılamaz.
- Tansu'nun vurgusu: "Buyurun size ödev.".
- Belirsiz: 40–55 gün takvim günü veya işlem günü olabilir; bilanço açıklanma tarihleri ve aralıktaki fiyatın seçim yöntemi yok. Tablo gözlemsel ilişki veya olay etkisi çalışması olarak okunabilir; nedensellik kanıtı değildir.
- YORUM: IHLGM satırının yüzdesi (son−önceki)/|önceki|×100 ile uyumludur; bu formül tablodan çıkarımdır, metinde yazılı değildir. Zararın azalması pozitif EFK kârına geçmek demek değildir.

### tema-4 özeti

| X no | başlık | bağlı R | olgunluk | yazar |
|---|---|---|---|---|
| X401 | Değerleme ağırlığının tarihçesi | R068 / R151 / R158 / R064 | kural tam | T + M + G |
| X402 | NEFK–fiyat ayrışması | yeni yöntem | çekirdek belli | T + M |
| X403 | Eşbütünleşme karar ve tarama hattı | R262 / R228 | çekirdek belli; karar koşulu kural tam | T + M + G |
| X404 | Log fark ve çift bantları | R101 | çekirdek belli | T + G |
| X405 | Tarihsel çarpan bantları | R144 | çekirdek belli; T eşikleri kural tam | T + M + G |
| X406 | TTM, HBK ve ROE | R133 / R146 / R152 | çekirdek belli; G hesap örneği kural tam | T + M + G |
| X407 | DuPont ve borç paydası | R002 | çekirdek belli | T + M + G |
| X408 | Black-Scholes ve delta | yeni yöntem | çekirdek belli; G fiyat formülü kural tam | T + M + G |
| X409 | Sharpe net kâr marjı filtresi | yeni yöntem | çekirdek belli | T |
| X410 | F/K regresyonu ve VIF | R066 | çekirdek belli | T + G |
| X411 | Convex Hull durağanlık/GARCH | R178 | çekirdek belli | T + M |
| X412 | NetYPP / satış | yeni yöntem | çekirdek belli | M + T |
| X413 | TOPSIS ve gri sayı varyantı | R145 / R179 | çekirdek belli; G klasik kod kural tam | T + M + G |
| X414 | DV artışı ve RSI | R059 | çekirdek belli | T + M |
| X415 | Aynı Q2 büyümesi | R002 / R133 | çekirdek belli | T + M |
| X416 | Likidite ve borç payları | R060 / R134 | çekirdek belli; asit-test oranı kural tam | T + M + G |
| X417 | 21 günlük Black-Litterman | R110 | çekirdek belli | T + M |
| X418 | Pair Health ve tarayıcı | R251 / R034 | çekirdek belli | T + M + G |
| X419 | Min varyans, Sharpe, MC | R177 / R173 / R182 | kural tam (kod); tercih çekirdek belli | T + G |
| X420 | Risk parity seçimi | R074 / R177 | çekirdek belli | T + M + G |
| X421 | Kripto sınırları | yeni yöntem | çekirdek belli | T |
| X422 | Ülke risk primi örnekleri | R070 | çekirdek belli | T + M |
| X423 | PD/DD +anlık ve erken hata | R062 / R144 | kural tam (pencere); hatalı örnek yalnız fikir | M + T + G |
| X424 | Bedelsiz potansiyeli | yeni yöntem | çekirdek belli | T + G |
| X425 | SAYAS İNA iki sonuç | R153 / R165 | çekirdek belli | T + G |
| X426 | Günlük dengeleme oran taraması | R030 / R078 | çekirdek belli; sıklık kural tam | T + G |
| X427 | Kişisel tahsis ve yeniden yatırım | yeni yöntem | çekirdek belli; %80/%20 kural tam | T + M |
| X428 | Tahvil/KMV/Merton | R061 | çekirdek belli; G tahvil/kod kural tam | T + G |
| X429 | Çift türevleri | R101 / R091 | çekirdek belli; HMM yalnız fikir | T + M + G |
| X430 | VİOP beta hedge | yeni yöntem | çekirdek belli | T + M |
| X431 | Portföy VIF kontrolü | R066 / R110 | çekirdek belli | T |
| X432 | EFK ve 40–55 gün fiyat tepkisi | yeni yöntem | çekirdek belli | T + G |

### tema-4 alınmayanlar

| öneri no | neden | kanıt id |
|---|---|---|
| #24 | Yinelenen: R164, 07.10 düzeltmesiyle üs birikmesini ve 6438,49 sonucunu zaten içerir. defter-fikir.txt de düzeltmeyi zaten içerir (6.438,49); yeni X kaydı üretmez. | 2036840358210945219 |
| #11, yalnız ilk katkı | 1947006461487517762'nin Convex Hull/Sharpe sektör seçimi X023'te kayıtlıdır. Yeni sektör sayıları ve durağanlık/GARCH kısmı X411'e alındı. | 1947006461487517762 |
| #23, yalnız çıpa metni | 36 çeyreklik çıpa ve değer tuzağı açıklaması R144'te zaten vardır. +anlık pencere ve erken araç ayrışması X423'e alındı. | 2041941067025494204 |
| #30, yalnız ML t-SNE adımı | ML hattının t-SNE adımı X403'te tutuldu; ikinci kez yöntem kaydı yapılmadı. Çift ağı ve diğer türevler X429'a alındı. | 1912875732646117781 |

## Tema 5a — Ölçüm yöntemi, ilke, araç-öğrenme

### X501 · 2026-09-04 21:12:24 UTC · Fon likiditesi ve stres altında tasfiye
- Bağlı: yeni yöntem; Öneri: tema-5a #1
- Yazar: T (kendi çalışma ve varsayımları) + M (uzun fon açıklamalarının düzenli gövdesi) + G (araç tabloları).
- Kaynak: 2095983340142882886 (2026-09-04 21:12:24 UTC), 2096187367778370014 (2026-09-05 10:43:08 UTC), 2096243590133407910 (2026-09-05 14:26:32 UTC), 2097031747347030189 (2026-09-07 18:38:24 UTC), 2099919520844382444 (2026-09-15 17:53:23 UTC).
- Fikirler:
  - [boyut-risk; T] "Asıl denklem: Pozisyon büyüklüğü / piyasa likiditesi." — fon pozisyonu, 20 günlük medyan TL hacim; %10 çıkış ve %20 piyasa katılımı — çekirdek belli.
  - [ölçüm-yöntemi; G] "Likidasyon Gün %20"; "%10 Çıkış Gün %20" — tam tasfiye = pozisyon TL / (katılım × 20G medyan TL hacim); çıkış stresi = çıkış TL × hisse ağırlığı / aynı payda; görselde %10/%20/%30 tam tasfiye katılımı ve %5/%10 çıkışın %20 katılımlı hesabı — kural tam (tablo hesabı).
  - [boyut-risk; M] "Fon yüzde 5 veya yüzde 10 büyüklüğünde bir itfayla karşılaştığında" — nakit/likit tamponun itfayı karşılama kapasitesi, 5/20G akış, AUM gerilemesi, yoğunlaşma ve pozisyon/hacim birlikte incelenir; karar eşikleri yok — çekirdek belli.
  - [ölçüm-yöntemi; G] "Kullanılabilir Hacim Katsayısı" — stresli süre = normal süre / kullanılabilir hacim katsayısı; katsayı ve marketability skorunun üretim formülü yok — çekirdek belli.
- Örnek ve sonuç: görselden: 2095983340142882886-1.png ve -2.png, TRHOL ağırlık %6,54; medyan hacim 378,78 milyon TL; %10 çıkış satış yükü 546,87 milyon TL; süre 7,22 gün; tam tasfiye %20 katılımla 64,58 gün. 2097031747347030189-2.png: BIGEN normal 11,12 gün, katsayı 0,05, stresli 222,40 gün; TKNKA 5,94 / 0,55 → 10,80 gün (yuvarlanmış girdiler). 15 Eylül TLY metninde tam tasfiye OZATD 320, TRHOL 158, TEHOL 89, ANELE 72 gün. Bunlar gerçekleşmiş satış sonuçları değil, ayrı tarih/fon senaryolarıdır.
- Tansu'nun vurgusu: "Bu çalışma hisse yönü tahmini değil büyük fon çıkışlarında hangi tahtaların satış baskısına daha hassas olabileceğini ölçen bir stres testidir."
- YORUM: Likidite sınıfı sınırları tablodaki satırlardan çıkarılabilir; yazılı eşik olmadığından kural olarak alınmadı. ±%2 emir derinliği, spread ve order-book depth 5 Eylül'de sonraki geliştirme olarak anlatılır; mevcut hacim hesabının parçası değildir.

### X502 · 2026-09-04 17:45:28 UTC · Fon akışında erken uyarı ve aktivasyon
- Bağlı: yeni yöntem; Öneri: tema-5a #2
- Yazar: T (birinci şahıs ve kısa notlar) + M (uzun fon açıklamalarının gövdesi) + G (erken uyarı grafiği).
- Kaynak: 2095931263593095368 (2026-09-04 17:45:28 UTC), 2097548996193526092 (2026-09-09 04:53:45 UTC), 2099132513708851639 (2026-09-13 13:46:05 UTC), 2099594176606187548 (2026-09-14 20:20:34 UTC), 2099959209467211874 (2026-09-15 20:31:05 UTC).
- Fikirler:
  - [boyut-risk; T/M] "5 günlük para akışı negatife döner → 20 günlük akış zayıflar → AUM zirveden geriler → yüksek ağırlıklı ve düşük likiditeli hisselerde risk artar." — takip sırası; zayıflama/gerileme eşiği yok — çekirdek belli.
  - [ölçüm-yöntemi; M] "Yeşil çizgi ise Erken Uyarı Skoru; yapısal risk ile aktivasyonun birleşik sonucudur." — yapısal risk: ağırlık/likidite/kriz satılabilirliği; aktivasyon: 5/20G akış, AUM, KAP değişimi, fiyat-hacim; birleşim formülü yok — çekirdek belli.
  - [ölçüm-ilkesi; T/M] "Sadece çıkış var demek yerine, çıkış hızlanıyor mu, yavaşlıyor mu, girişler güçleniyor mu bunu görmek çok daha anlamlı." — 5 ve 20 günlük akış hızlarını karşılaştırma; acceleration hesaplama formülü yok — çekirdek belli.
- Örnek ve sonuç: THF metninde 5G giriş 44,63 milyar TL (%31,5 AUM), 20G 120,83 milyar TL (%85,3 AUM). görselden: 2099594176606187548-1.png, ANELE yapısal risk yaklaşık 89, aktivasyon yaklaşık 12,5, erken uyarı yaklaşık 43; DSTKF yaklaşık 27/0/10,8. TLY metninde 5G çıkış hızı %1,15, 20G %1,37; çıkış sürerken hızın azalması anlatılır.
- Tansu'nun vurgusu: "En önemli erken uyarı, fon fiyatında ilk kırmızı gün değil güçlü para girişlerinin belirgin şekilde yavaşlaması ve ardından kalıcı para çıkışına dönüşmesidir."
- Belirsiz: Öneri belgesi yöntem adını çarpım olarak aktarıyor; gönderi yalnız birleşik sonuç diyor. Grafikteki yaklaşık değerler 0,4 × yapısal + 0,6 × aktivasyon okumasıyla uyumlu; başka ölçekleme/birleştirme de mümkün. Kaynakta ağırlıklar açıklanmadığı için 40/60 kuralı kurulamaz.
- YORUM: Velocity'nin günlük akış/AUM ortalaması olması öneri belgesinin açıklamasıdır; bu beş kaynak metninde açık hesap formülü verilmez.

### X503 · 2025-05-15 10:32:45 UTC · Korelasyondan Granger tahmin gücüne
- Bağlı: yeni yöntem; Öneri: tema-5a #3
- Yazar: T (kendi THF çalışması ve sonradan değerlendirmesi) + M (genel ders biçimli anlatım) + G (istatistik tablosu).
- Kaynak: 1922963356362703307 (2025-05-15 10:32:45 UTC), 2099751961159454867 (2026-09-15 06:47:33 UTC), 2099952521221661048 (2026-09-15 20:04:30 UTC), 2101627771524927545 (2026-09-20 11:01:21 UTC).
- Fikirler:
  - [ölçüm-yöntemi; M] "Bu yüzden önce ADF testi ile serilerin durağan olup olmadığı kontrol edilmelidir." — gerekirse fark; lag AIC/BIC ile seçilebilir; aylık veri için beş yıl, günlük için birkaç ay önerisi — çekirdek belli.
  - [ölçüm-yöntemi; T/M] "Korelasyon → Gecikmeli Korelasyon → Granger Nedensellik" — THF uygulamasında günlük getiri ve normalize akış (%AUM), iki yönde Pearson/Spearman ve Granger lag 1–5, FDR düzeltmesi — çekirdek belli.
  - [ölçüm-ilkesi; M] "Granger nedensellik, gerçek neden-sonuç ilişkisi değil; tahmin edebilme gücüdür." — ekonomik nedensellik iddiasından ayrı — çekirdek belli.
- Örnek ve sonuç: THF metninde eş anlı Pearson 0,12 / Spearman 0,07; getiri→sonraki akış lag2 0,245/0,353. görselden: 2099952521221661048-1.png, akış→getiri lag1 ham p=0,0188 fakat FDR p=0,0547 ve anlamlı=False; getiri→akış lag2–5 FDR p=0,0012. ADF getiri −7,674303 (lag5), akış −3,085183 (lag8); p=0,0050/0,0300; %5 kritik değer −2,86. Gözlem 305–309. ADF notu p yaklaşık ve karar kritik değere göre; Granger yöntemi NUMPY OLS FALLBACK. Sonraki 20/60/120 günlük pencereler ve tüm tarih analizi, yapılacak iş diye belirtilir.
- Tansu'nun vurgusu: "Fon analizinde sadece getiriye değil, getirinin kaynağına ve sürdürülebilirliğine bakmak gerekir."
- YORUM: Lag 1–5 ve FDR uygulaması belirli örneklemindir; her çalışma için sabit gecikme kuralı değildir. Yaklaşık p değerleri kesin istatistiksel sonuç diye genişletilmedi.

### X504 · 2025-03-26 04:15:23 UTC · Fark sonrası ADF ve KPSS kontrolü
- Bağlı: yeni yöntem; Öneri: tema-5a #4
- Yazar: M (numaralı, ders/yanıt biçimli dizi; Tansu hesabında).
- Kaynak: 1904748993797632344 (2025-03-26 04:15:23 UTC), 1904748996893053368 (2025-03-26 04:15:24 UTC), 1904748999908692189 (2025-03-26 04:15:24 UTC), 1904749002748281042 (2025-03-26 04:15:25 UTC), 1904749005990510772 (2025-03-26 04:15:26 UTC).
- Fikirler:
  - [ölçüm-yöntemi; M] "Genellikle 0.05’ten küçükse, verinin durağan olduğu kabul edilir." — ADF p<0,05; istatistiğin kritik değerden daha negatif olmasıyla karşılaştırma; lag/pencere yok — çekirdek belli.
  - [ölçüm-yöntemi; M] "ek dönüşümler (örneğin, ikinci fark alma) gerekebilir." — p>0,05 veya istatistik kritik değerden büyükse dönüşümü yeniden değerlendirme; fark aldıktan sonra yeniden test — çekirdek belli.
  - [ölçüm-yöntemi; M] "ADF testinin yanı sıra, KPSS testi gibi diğer istatistiksel testlerle de durağanlık kontrolü yapılabilir." — farklı varsayımlarla çapraz kontrol; KPSS karar eşiği yok — çekirdek belli.
- Örnek ve sonuç: Bu beş metinde hesaplanmış seri/test çıktısı yok.
- Tansu'nun vurgusu: Bu dizi içinde M gövdesinden ayrılabilen Tansu'nun kendi vurgu cümlesi yok.
- Belirsiz: p=0,05 eşitliği için karar verilmez. ADF/KPSS uyuşmadığında hangi testi önceleyeceği açıklanmaz.

### X505 · 2025-03-11 22:09:37 UTC · GARCH örneği ve model seçim ölçütleri
- Bağlı: R097; Öneri: tema-5a #5
- Yazar: T (BIST yorumu ve AI uyarısı) + M (model seçimi açıklaması) + G (GARCH sonuç tablosu).
- Kaynak: 1899583516670611844 (2025-03-11 22:09:37 UTC), 1952739571466211673 (2025-08-05 14:32:48 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "Standardized Student's t" — log return, constant mean, GARCH(1,1), Student t dağılımı; tek örnek tahmini — çekirdek belli.
  - [ölçüm-ilkesi; M] "Daha düşük AIC/BIC → Daha iyi model"; "Ljung-Box testi uygulanabilir." — AIC/BIC, log-likelihood, standardize artıkların otokorelasyonu/ARCH etkisi ve ekonomik yorum birlikte; EGARCH asimetri seçeneği — çekirdek belli.
- Örnek ve sonuç: görselden: 1899583516670611844-1.png, 545 gözlem; omega 0,2951, alpha[1] 0,1494, beta[1] 0,7625; p=0,414/0,301/0,001004; AIC 2172,34, BIC 2193,84. Omega/alpha bu tabloda %5 düzeyinde anlamlı değil. Görsel rapor tarihi 12 Mart 2025 00:59:50; gönderi UTC tarihi 11 Mart, ayrı zaman alanlarıdır.
- Tansu'nun vurgusu: "Ama bunu AI ile yapmayın"; "Alın kalemi kağıdı not edin, sistemli çalışın."
- YORUM: Alpha+beta yaklaşık 0,912; bu tek tahmin evrensel GARCH parametre seti veya yeni yatırım kuralı değildir. AI uyarısının ilk cümleleri T; düzenli ölçüt listesi M olarak ayrıldı.

### X506 · 2024-10-31 19:28:29 UTC · DtD denemesi ile ayrı lojistik PD sınıfları
- Bağlı: R061; Öneri: tema-5a #6
- Yazar: T (kendi denemesi) + M (risk sınıfı ve DD açıklamaları) + G (kod/çıktı).
- Kaynak: 1852070155779739853 (2024-10-31 19:28:29 UTC), 1888561702649688178 (2025-02-09 12:12:52 UTC), 1888561704725774563 (2025-02-09 12:12:52 UTC), 1888561706638405699 (2025-02-09 12:12:53 UTC), 1907840096851624360 (2025-04-03 16:58:19 UTC), 1907840099489874309 (2025-04-03 16:58:20 UTC).
- Fikirler:
  - [temel-değerleme; T] "Rakamlar sallamasyon." — basitleştirilmiş distance-to-default tarama denemesi; gerçek şirket ölçümü diye kullanılamaz — yalnız fikir.
  - [boyut-risk; M] "DD > 2 → çok güvenli"; "DD ≈ 1–1.5 → orta risk"; "DD < 1 → risk artıyor" — örnek DD okuması; sınırların tüm aralıkları kapsadığı gösterilmez — çekirdek belli.
  - [boyut-risk; M] "0.00 - 0.20 → Düşük Risk"; "0.21 - 0.50 → Orta Risk"; "0.51 - 1.00 → Yüksek Risk" — lojistik regresyondan çıkan temerrüt olasılığına önerilen örnek sınıflar; DtD/EDF'den ayrı — çekirdek belli.
- Örnek ve sonuç: görselden: 1852070155779739853-1.png, DOAS.IS; borç 300.000.000, rf=0,25, T=1; çıktı DtD=1,7867 ve "İflas riski düşük." Kodda market_cap=fiyat×1.000.000; total_assets=market_cap+debt; volatilite hisse getirisi std×√252. 1907840096851624360-1.png: DD=1,3056 σ, EDF=%9,58. Sonraki metin bu DD'yi orta risk diye yorumlar.
- Tansu'nun vurgusu: "Distance to default asla bu kadar kolay değil ama bu da sizin bir modeliniz olabilir."
- Belirsiz: Lojistik PD aralıkları 0,20–0,21 ve 0,50–0,51 arasında boşluk bırakıyor; kaynak bir yuvarlama kuralı vermiyor. 2024 kodunda >1 düşük risk; 2025 açıklamasında yaklaşık 1–1,5 orta risk, aynı sınıflama değildir.
- YORUM: Önerinin EDF=N(−DD) formülü açılan grafikte yazılı değil; DD/EDF sayıları bu okumayla uyumlu fakat formül kaynak alıntısı olarak alınmadı. Kodun payında rf+0,5σ² vardır; bu basit deneme standart Merton varlık modeline dönüştürülmüş gibi sunulmadı. Sabit hisse adedi ve hisse/varlık volatilitesinin eşitlenmesi düzeltilmeden üretim hesabına taşınamaz.

### X507 · 2025-01-11 19:39:50 UTC · Sharpe, Sortino ve yıllıklaştırma varsayımı
- Bağlı: R137 / R115 / R223; Öneri: tema-5a #7; tema-5a #33 Ç3 burada işlendi.
- Yazar: T (kod ve kısa cevaplar) + M (risksiz faiz açıklaması) + G (metrik tablosu).
- Kaynak: 1878164936150360461 (2025-01-11 19:39:50 UTC), 1913876527881539592 (2025-04-20 08:44:57 UTC), 1913880746973946124 (2025-04-20 09:01:42 UTC), 1915540627405554032 (2025-04-24 22:57:29 UTC), 1942696711287169192 (2025-07-08 21:26:04 UTC), 2099366035111493673 (2026-09-14 05:14:01 UTC), 2099453056337203495 (2026-09-14 10:59:49 UTC).
- Fikirler:
  - [ölçüm-yöntemi; T] "annual_return = returns.mean() * 252"; "annual_vol = returns.std() * (252 ** 0.5)"; "sharpe = (annual_return - rf) / annual_vol" — yıllık ortalama getiri/std ve yıllık rf — kural tam (paylaşılan formül).
  - [ölçüm-ilkesi; T] "10 yıllık DT faizi kullanacaksınız." — 20 Nisan TR örneği yaklaşık 0,38, ABD 0,05; tarihli varsayım, sürekli sabit faiz değil — çekirdek belli.
- Örnek ve sonuç: görselden: 1878164936150360461-1.png, GARAN yıllık getiri 0,858181, risk 0,49284, downside risk 0,317296, Sharpe 0,932111, Sortino 1,4478. İki oran yaklaşık aynı rf=0,3988 ile uyumlu; rf görselde ayrıca yazılı değil. Sortino'nun paydası downside risk; negatif getiri altkümesinin nasıl hesaplandığı bu görselde yok. Formül seti X526'da ayrıca kaynak metniyle yer alır.
- Tansu'nun vurgusu: "İster kısa vadeli ister uzun vadeli yatırımcı olun aşağıdaki metrikleri anlamanız ve hesaplayabilmeniz lazım."
- Belirsiz: 24 Nisan metni açıkça "yaklaşık 255 işlem günü varsayımıyla" der; √255 ve ×255 bu örneğin seçilmiş takvimidir. 14 Eylül kodu 252 kullanır. Takvim varyantı mı kalıcı tercih değişimi mi açıklanmaz; 255 için gerekçe yok iddiası düzeltildi.
- Çelişir: R223 ile 8 Temmuzdaki "volatilite 252 işlem günüyle çarpılarak" ifadesi uyuşmaz; 14 Eylül T kodu std×√252 kullanır. 252'yle çarpım işlem kuralı olarak alınmadı.
- YORUM: Negatif Sharpe, mutlaka negatif mutlak getiri değildir; rf altında getiri de negatiftir. R137'nin aşamaları bu örneklerle yeniden sıralanmadı.

### X508 · 2025-04-10 19:41:24 UTC · Rolling Sharpe ve alpha pencere seçimi
- Bağlı: R202 (rolling alpha bağı; R202'nin ikinci metriği skewness); Öneri: tema-5a #8
- Yazar: T (kısa uygulama cevapları) + M (rolling açıklaması ve −0,40/−0,60 yorumu) + G (Sharpe grafiği).
- Kaynak: 1910417850684367263 (2025-04-10 19:41:24 UTC), 1913512010253205811 (2025-04-19 08:36:29 UTC), 1953358552308892053 (2025-08-07 07:32:25 UTC), 1953390566898532487 (2025-08-07 09:39:38 UTC), 1953400490747662376 (2025-08-07 10:19:04 UTC).
- Fikirler:
  - [ölçüm-yöntemi; T] "20-30-30-50 ona siz karar vereceksiniz" — kaynak dizisi aynen; ayrı T cevabında 30 yerine 40 örneği; hisse volatilitesine göre optimizasyon veya ortak vade — çekirdek belli.
  - [ölçüm-ilkesi; M] "-0.40 civarından dönüş, yatırımın kötü bir dönemden çıkıyor olabileceğini gösterir." — −0,60 dönüşü de toparlanma örneği; kesin al koşulu veya dönüş tanımı yok — çekirdek belli.
- Örnek ve sonuç: görselden: 1910417850684367263-1.jpg, "Rolling Sharpe (21 gün)" ve "-0.4 Seviyesi" etiketleri. Etiketsiz kırmızı çizgiye işlem kuralı verilmedi; işlem sonucu yok.
- Tansu'nun vurgusu: "Sharpe indikatörü. Beni hiç üzmedi."
- Belirsiz: M açıklaması 30/40 günde bir güncellenen pencere diyor; bu günlük kayan pencere ile seyrek güncelleme olarak iki türlü okunabilir. T cevabı kesin güncelleme sıklığı vermez.
- YORUM: −0,40/−0,60 gerekçesi M gövdesidir; Tansu'nun kendi kesin giriş kuralı gibi yazılmadı.

### X509 · 2024-11-23 23:21:25 UTC · Lojistik yön olasılığı ve iki eşik varyantı
- Bağlı: R234; Öneri: tema-5a #9; tema-5a #33 Ç2'nin yön ayrımı burada ve X522'de işlendi.
- Yazar: T (kendi model anlatımı, kısa cevap ve DITAS çıktısı) + G (olasılık grafiği).
- Kaynak: 1860463695790305656 (2024-11-23 23:21:25 UTC), 1893042417617522992 (2025-02-21 20:57:38 UTC), 1893042422088642888 (2025-02-21 20:57:39 UTC), 1958130783354323290 (2025-08-20 11:35:33 UTC).
- Fikirler:
  - [ölçüm-yöntemi] "Verinin %90’lık kısmını model eğitimi için kullanarak, geri kalan %10’luk kısımda model performansını test edebilmem için bir yapı oluşturuyorum." — in-sample/out-of-sample bölme; ayrımın tarih sınırı yok — çekirdek belli.
  - [teyit-tetik] "PRED sütununa kaydediyorum ve karar sınırını 0.5 olarak belirleyerek" — yukarı/aşağı yön olasılığı; bağımsız değişkenler teknik gösterge durumlarının 0/1 kodlaması — çekirdek belli.
  - [teyit-tetik; G] "UP eşik"; "DOWN eşik" — DITAS grafiğinde yaklaşık 0,6/0,4; bu, 0,5 tek sınırından ayrı varyant; aradaki bölgede karar kaynağı yok — çekirdek belli.
- Örnek ve sonuç: DITAS metninde 19 Ağustos 2025 kapanış 33,50, yön olasılığı 0,99, LONG bias; ertesi gün gönderi "%4 yukarıda hisse..." sonucunu bildirir. görselden: 1958130783354323290-1.png yaklaşık 0,6/0,4 çizgileri; eşikler son günün olasılığı değildir.
- Tansu'nun vurgusu: "Oysa dün benim sistemim aşağıdaki uyarıyı yazdı"
- Çelişir: R185'in M gövdesindeki yön tahminini toptan reddeden anlatım; Tansu burada kendi sisteminde yön olasılığını kullanır. R058'in olması gereken şirket değeri ile piyasa fiyatı ayrımı, bu kategorik yön modeline otomatik olarak yasak getirmez.
- YORUM: Aynı modelin bütün gönderilerde aynı özellik/eğitim penceresiyle çalıştığı gösterilmedi. %90 eğitim payı, %90 doğruluk değildir.

### X510 · 2024-08-26 20:02:16 UTC · Optimizasyonda sağlam bölge ve al-tut kıyası
- Bağlı: R138; Öneri: tema-5a #10
- Yazar: T (kendi uygulamaları ve cevapları) + M (uzun optimizasyon dersi) + G (XU100 sonuç ekranı).
- Kaynak: 1828161056960827738 (2024-08-26 20:02:16 UTC), 1829983002304086142 (2024-08-31 20:42:01 UTC), 1840170065464803535 (2024-09-28 23:21:46 UTC), 1962960506509000705 (2025-09-02 19:27:09 UTC), 1986899794032304554 (2025-11-07 20:53:20 UTC).
- Fikirler:
  - [ölçüm-ilkesi; T] "her hisse için farklı parametrelerde giriş çıkış yapmak lazım." — tek EMA/SMA çifti bütün hisselere sabitlenmez — çekirdek belli.
  - [ölçüm-ilkesi; M] "İyi optimizasyon, \"sağlam\" (robust) bir bölge bulmaktır." — komşu parametrelerin de kârlı olması; 10–250 taraması anlatı örneği, çalıştırılmış tarama aralığı diye doğrulanamaz — çekirdek belli.
- Örnek ve sonuç: DOAS T metninde Vegas 12/144/169 → 8/150/150; TUPRS 50/200 → 48/247, fakat al-tut getirisini geçemediği açık. görselden: 1986899794032304554-1.png, XU100 SMA35/240, 2020-11-07–2025-11-07; strateji çarpanı 4,6948, net yaklaşık %369,48; al-tut %786,25. Optimum geçmiş parametreyi bulmak al-tutu geçme sonucu vermemiştir.
- Tansu'nun vurgusu: "Fakat Tüpraş'ın getirisini geçemedi."
- YORUM: R138 walk-forward yöntemini anlatır; buradaki grid/sağlam bölge açıklaması bunun yerine geçmiş optimumu zorunlu kılmıyor. Komşu bölgenin gerçekten ölçüldüğü bir harita paylaşılmamıştır.

### X511 · 2025-01-11 22:36:41 UTC · Makro faktör betaları ve Fama-French bileşenleri
- Bağlı: R200; Öneri: tema-5a #11
- Yazar: T (kısa tanıtım) + M (Fama-French açıklaması) + G (faktör beta grafikleri).
- Kaynak: 1878209442790998442 (2025-01-11 22:36:41 UTC), 1893286881917366600 (2025-02-22 13:09:02 UTC), 1893286885021085822 (2025-02-22 13:09:03 UTC), 1919250826435965149 (2025-05-05 04:40:29 UTC), 1943070389388873813 (2025-07-09 22:10:55 UTC).
- Fikirler:
  - [ölçüm-ilkesi; T] "Her faktör betasını ayrı ayrı değerlendirmek lazım." — duyarlılık tek piyasa betasına indirgenmez — çekirdek belli.
  - [ölçüm-yöntemi; G] "USDTRY"; "EURUSD"; "BRENT"; "SPX"; "DAX"; "US_10Y" — grafikte altı ayrı faktöre beta; regresyonun ortak mı ayrı mı olduğu, dönüşüm ve pencere yazılı değil — çekirdek belli.
  - [ölçüm-yöntemi; M] "SMB - Small Minus Big"; "HML - High Minus Low" — piyasa faktörü, küçük/büyük ve yüksek/düşük defter değeri bileşenleri; ölçüm denklemi yok — yalnız fikir.
- Örnek ve sonuç: görselden: 1878209442790998442-2.jpg ve 1943070389388873813-1.png altı faktörlü hisse grafikleri. Sayısal beta eşiği veya sonrasında gerçekleşen işlem sonucu verilmez.
- Tansu'nun vurgusu: "Bu tablolar ne işe yarar?"; "Yatırımcı olarak nasıl okumalısınız?"
- YORUM: Önerideki "pencere tanımı eklenmeli" bir geliştirme yorumudur; kaynakta bulunmayan pencere eklenmedi. HML'nin yalnız yüksek defter değeri açıklaması tam oran/portföy yapım kuralı değildir.

### X512 · 2024-10-27 08:51:50 UTC · Bollinger örnek std ve VaR ufku
- Bağlı: R053; Öneri: tema-5a #12
- Yazar: T (eğitim paylaşımı) + G (kod) + M (VaR açıklaması).
- Kaynak: 1850460386371281374 (2024-10-27 08:51:50 UTC), 1850468058747326871 (2024-10-27 09:22:19 UTC), 1916228528850272645 (2025-04-26 20:30:57 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "sma + 2 * stdev"; "sma - 2 * stdev" — kapanış SMA20, rolling örnek std20; üst/alt bant ±2 std — kural tam (gösterge hesabı).
  - [boyut-risk; M] "belirli bir güven düzeyinde (örneğin %95) ve belirli bir zaman diliminde (örneğin 1 gün)" — VaR için %95/1 gün örneği; dağılım, örneklem ve hesap yöntemi yok — yalnız fikir.
- Örnek ve sonuç: görselden: 1850460386371281374-1.png ve -2.png, KCHOL.IS 2023-01-01–2023-12-31 kapanışlarına Bollinger hesabı; 1850468058747326871-1.png aynı formülün mum grafik varyantı. Giriş/çıkış ya da test sonucu yok.
- Tansu'nun vurgusu: "EĞİTİM AMAÇLIDIR!"
- YORUM: R053'teki kitap şeklinin standart hatası (SE), bu kodun fiyat standart sapması değildir. VaR'ı mutlak kayıp üst sınırı diye yorumlayan M gövdesi kural yapılmadı; belirtilen güven düzeyinin dışında kayıp olabilir.

### X513 · 2024-10-13 14:05:00 UTC · SMA tabanlı RSI ve hisseye göre eşik
- Bağlı: R233 / R138; Öneri: tema-5a #13; tema-5a #33 Ç7 burada işlendi.
- Yazar: T (hesap ayrımı ve optimizasyon uyarısı) + G (kod/grafik).
- Kaynak: 1845465765421453791 (2024-10-13 14:05:00 UTC), 1860318349797814519 (2024-11-23 13:43:52 UTC), 1860405835354054736 (2024-11-23 19:31:30 UTC).
- Fikirler:
  - [ölçüm-yöntemi; T] "Benim kodum ise sma tabanlı rsi hesaplıyor" — son günleri ekstra ağırlıklandırmayan rolling ortalamalar — çekirdek belli.
  - [ölçüm-yöntemi; G] "period = 20" — pozitif/negatif fiyat farklarının SMA20 ortalamaları; RSI=MA_Up/(MA_Up+MA_Down)×100; grafikte 70/30 — kural tam (hesap).
  - [ölçüm-ilkesi; T] "Hissenin volatilitesine göre değerleri optimize etmeniz lazımç" — periyot/eşik hisseye göre; tek evrensel 30/70 zorunluluğu yok — çekirdek belli.
- Örnek ve sonuç: görselden: 1860318349797814519-2.png, XU100 verisi 2022-01-01–2024-11-23; kod başlığı 2023 grafiği der, gösterilen parçada df_2023 tanımı yok. 1860405835354054736-1.png: EURUSD=X RSI(6,65,20), TC=7e−05; strateji eğrisi sonu yaklaşık 2,6 çarpan. Bu forex örneği her hissenin performansı diye genellenmez.
- Tansu'nun vurgusu: "RSI 30/70 Allah kelamı değil."
- Belirsiz: Tansu pandas_ta hesabını "ema tabanlı" diye adlandırır; kütüphanenin sürümü/çağrısı bu cevapta yok. Bu ifade yazara aittir, tüm RSI uygulamalarının teknik tarifi sayılmaz.
- YORUM: R233 RSI14/30/70 belirli bir kurulumdur; bu kaynak başka hesap ve optimizasyon varyantı sunar. Yalnız eşik farklılığından kaynak sürümlerinin tarihçesi veya kurulumun geçersizliği çıkarılmadı.

### X514 · 2025-01-05 13:51:03 UTC · İsabet oranı, profit factor ve aşırı uyum iddiası
- Bağlı: R140; Öneri: tema-5a #14
- Yazar: T (kendi deneyimi ve robot parametreleri) + M (uzun GARAN sonuç açıklaması) + G (backtest raporları).
- Kaynak: 1875902835780677930 (2025-01-05 13:51:03 UTC), 1908882937325531171 (2025-04-06 14:02:12 UTC), 1908882939976307137 (2025-04-06 14:02:12 UTC), 1992410986989441388 (2025-11-23 01:52:51 UTC).
- Fikirler:
  - [ölçüm-ilkesi; T] "Ben matrixdeki robotlarımda da optimizasyon sonrası %50 winrate olan parametreler ile yol alırım." — Tansu'nun parametre seçimi tercihi; genel doğrulama eşiği değil — çekirdek belli.
  - [ölçüm-ilkesi; T/M] "Eğer Kazanma Oranı 90% veya üzeri olsaydı" — kaynak bunu aşırı uyum şüphesiyle ilişkilendirir; tek başına ispat değil — yalnız fikir.
  - [ölçüm-yöntemi; G] "Profit Factor"; "Max Drawdown"; "Sharpe Ratio" — işlem sayısı/isabet ile beraber sonuç metriklerini raporlama — çekirdek belli.
- Örnek ve sonuç: 5 Ocak metni PF=1,68 ve %80 başarılı işlem anlatır. görselden: 1908882937325531171-1.png, ASELS toplam K/Z 17,83; 21 işlem/9 kazanan; %42,86 win rate; PF=1,64; MaxDD=−13,74; Sharpe=0,22. 1992410986989441388-1.png: GARAN, 2019-02-26–2025-11-21; 31 işlem, 18 kâr/13 zarar; %58,06 win rate, %1153,73 kümülatif getiri. Bunlar ayrı sistem/örnek raporlarıdır.
- Tansu'nun vurgusu: "Kusursuz sistem yoktur olsa ferrari ile gezeriz, sürekli sistemlerimizi optimize etmeye çalışıyoruz."
- YORUM: "21 işlemden 9 tanesi başarılı bu overfitting sorunu olmadığının göstergesi." kaynak iddiasıdır; düşük/dengeye yakın isabet tek başına örneklem dışı doğrulama değildir. GARAN açıklamasındaki −1,15$ ile görseldeki −%1,158303 birim farkı düzeltildi; %1153,73 geçmiş getiri, gelecekteki başarı kanıtı diye aktarılmadı.

### X515 · 2024-02-23 06:49:32 UTC · WMA13/60, MACD12/26/9 ve WaveTrend revizyonu
- Bağlı: R258 (WMA21 raporunun farklı periyotlu ölçüm varyantı); Öneri: tema-5a #15
- Yazar: T (kod paylaşımı) + G (grafik/kod).
- Kaynak: 1760919805035467002 (2024-02-23 06:49:32 UTC), 1762082053330440337 (2024-02-26 11:47:54 UTC), 1845362765898097116 (2024-10-13 07:15:43 UTC), 1845362768632799316 (2024-10-13 07:15:43 UTC).
- Fikirler:
  - [ölçüm-yöntemi; T] "13 günlük ve 60 günlük ağırlıklı hareketli ortalamalar kullanılmıştır." — WMA ağırlıkları 1..n, yakın günün ağırlığı yüksek; WMA13 ve WMA60 — kural tam (hesap).
  - [ölçüm-yöntemi; G] "data['MACD'] = data['EMA12'] - data['EMA26']" — EMA12−EMA26; sinyal EMA9(MACD), adjust=False — kural tam (hesap).
  - [ölçüm-ilkesi; T] ">-60 ve <50 parametresini <-50 ve <50 olarak revize ettim strateji getirisini arttırdım fakat her hissede ayrı ayrı bakmak lazım." — WaveTrend için kaynakta yazılı eşitsizlik değişimi; WT(10,21) periyodu X030'la aynı, eşik revizyonu yeni ayrıntı — çekirdek belli.
- Örnek ve sonuç: görselden: 1762082053330440337-1.jpg–4.jpg, MAVI fiyat/MACD ve WMA13/60 grafikleri. WMA kod başlığı THYAO, çıktı MAVI; kodun yeniden kullanım izi, MAVI parametrelerini değiştirmiyor. 1845362765898097116-1.jpg WT(10,21), WT_1/WT_2 çizimleri; T metni DOAS'ta çoğu stratejinin çalışmadığını ve al-tutun daha çok kazandırdığını söyler. Sonraki mesaj eşik değişikliğiyle getiriyi artırdığını söyler fakat yeni sayısal sonuç vermez; al-tutu geçtiği iddiası yok.
- Tansu'nun vurgusu: "Detaylı grafik çalışmaları pek yakında. İş arası anca bu kadar :)"
- Belirsiz: WT revizyonunda ilk işaret >−60, yeni işaret <−50 yazılıdır. İki eşitsizlik aynı WT serisine aitse <50 üst sınırı yeni <−50 koşulunda gereksiz kalır; farklı al/sat koşullarına aitse iki ayrı sınırdır. Kaynak hangi seriyi/işlem yönünü kastettiğini açıklamaz; işaretler düzeltilmiş gibi değiştirilmedi.
- YORUM: WMA ve MACD birlikte çizilmiştir; zorunlu iki gösterge giriş kapısı yazılmamıştır. X030'daki WT periyodu/çizim ayarı tekrar bağımsız yöntem yapılmadı; burada Tansu'nun eşik revizyonu ve DOAS sınırlaması korundu.

### X516 · 2024-10-25 12:33:24 UTC · CMF20 hesabı ve SMA14 tabanlı ATR
- Bağlı: R137 / R184 / R212; Öneri: tema-5a #16
- Yazar: T (CMF kod paylaşımı) + G (CMF kodu/çıktısı) + M (ATR ders gövdesi; T girişli).
- Kaynak: 1849791369482486118 (2024-10-25 12:33:24 UTC), 1987507728718205244 (2025-11-09 13:09:03 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "n: int=20" — MFV=Volume×(2Close−High−Low)/(High−Low); CMF20=20G toplam MFV / 20G toplam Volume — kural tam (gösterge hesabı).
  - [ölçüm-yöntemi; M] "ATR periyodu 14 gün olarak varsayılır." — TR=max(H−L, |H−önceki C|, |önceki C−L|); ATR=SMA14(TR); 2ATR=2×ATR — çekirdek belli (M formül anlatımı).
- Örnek ve sonuç: görselden: 1849791369482486118-1.png ve -2.png, TUPRS.IS 2023-01-01–2024-10-25; 24 Ekim kapanış 146,00, CMF=−0,152400. ATR metninde örnek hisse/hesap sonucu yok.
- Tansu'nun vurgusu: "Şu formülü kaydedin lazım olur."; "Bence aşağıdaki yazıyı kaydedin."
- YORUM: Bu ATR anlatımı SMA tabanlıdır; bütün ATR hesaplarının tek yumuşatma yöntemi diye genellenmez. CMF kodunda High=Low için özel sınır davranışı gösterilmez. Defter-5 X002'nin CMF işaret dizisine burada yalnız hesap periyodu örneği eklenir; X002'nin açıklanmayan periyodu kesin 20 sayılmaz.

### X517 · 2024-02-23 08:01:23 UTC · Ichimoku bileşenleri ve kaydırma
- Bağlı: yeni yöntem (defter-5 X034'ün koşullarından ayrı hesap tanımı); Öneri: tema-5a #17
- Yazar: T (kod paylaşımı ve optimizasyon sorusu) + G (kod/grafik).
- Kaynak: 1760937885190996368 (2024-02-23 08:01:23 UTC), 1840046005787504758 (2024-09-28 15:08:48 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "rolling(window=9)"; "rolling(window=26)"; "rolling(window=52)" — Tenkan=(9G maxH+minL)/2; Kijun=(26G maxH+minL)/2; Span A=((Tenkan+Kijun)/2).shift(26); Span B=((52G maxH+minL)/2).shift(26); Chikou=Close.shift(−26) — kural tam (çizim hesabı).
  - [ölçüm-ilkesi; T] "Ich. Bulutunun parametrelerini optimize edip deneyen oldu mu hiç?" — optimizasyon sorusu; kendi optimumu açıklanmıyor — yalnız fikir.
- Örnek ve sonuç: görselden: 1760937885190996368-1.jpg THYAO Ichimoku grafiği; formüller ve kaydırmalar kodda. İşlem veya optimizasyon sonucu yok.
- Tansu'nun vurgusu: "kodu ve görseli buraya bırakayım yorum sizin:)"
- YORUM: Chikou'nun negatif shift'i görsel hizalamadır; gelecekteki kapanışı bugünkü karar girdisi olarak kullanma kuralı değildir. X034 aynı göstergenin tarama koşullarını kaydeder; burada eksik hesap tanımı tamamlanır.

### X518 · 2024-02-22 17:56:02 UTC · Çift EMA yumuşatma ve ayrı CCI çizimi
- Bağlı: R124 / R105; Öneri: tema-5a #18
- Yazar: T (kendi kodlama anlatımı) + G (kod/grafikler).
- Kaynak: 1760725146959270113 (2024-02-22 17:56:02 UTC), 1760742464309350866 (2024-02-22 19:04:51 UTC).
- Fikirler:
  - [ölçüm-yöntemi; T] "Hisseni 5 günlük üssel hareketli ortalaması ve bununda 10 üssel hareketli ortalaması alındı." — EMA5(fiyat), EMA10(EMA5); iki ortalamanın uzaklaşması — kural tam (hesap).
  - [teyit-tetik; G] "sinyaller['al']" — EMA1>EMA2 ve önceki EMA1≤EMA2; satış simetriği EMA1<EMA2 ve önceki EMA1≥EMA2 — kural tam (kesişim).
  - [ölçüm-yöntemi; G] "CCI_EMA20" — TP=(H+L+C)/3; SMA20(TP), 20G ortalama mutlak sapma; CCI=(TP−SMA20)/(0,015×sapma); CCI EMA20, ±100 çizgileri — kural tam (hesap).
- Örnek ve sonuç: BRSAN T metni; görselden: 1760742464309350866-1.jpg THYAO EMA5/EMA10(EMA5) kodu, -3.jpg ayrı THYAO CCI grafiği. Getiri raporu yok.
- Tansu'nun vurgusu: "kısa ama etkili bir kodlama."
- Belirsiz: EMA kodu ikinci yumuşatmayı 10 gün hesaplıyor; grafiğin başlık ve legend'i 5 gün diyor. Hesap 5/10, grafik etiketi 5/5 olarak iki kaynak okuması ayrıldı.
- YORUM: Önerideki "+ CCI" aynı girişte birleşik koşul gibi okunmamalı; kaynak ayrı çizimler sunar, CCI teyidini EMA kesişimine bağlayan bir ifade yok.

### X519 · 2024-04-24 15:46:22 UTC · Vegas tüneli yanında RSI14
- Bağlı: R128 / R138 (EMA/optimizasyon bağı; Vegas'a özel R kaydı değil); Öneri: tema-5a #19
- Yazar: T (ayar cevabı ve paylaşım) + G (Vegas kodu).
- Kaynak: 1783160562156716179 (2024-04-24 15:46:22 UTC), 1827737743683707129 (2024-08-25 16:00:10 UTC).
- Fikirler:
  - [ölçüm-yöntemi; T] "Uzunlukları 12-144-169 yapın" — üç EMA; grafikte RSI14 ve 50 referansı — kural tam (çizim ayarı).
  - [ölçüm-yöntemi; G] "df['RSI'] = ta.rsi(df['Close'], length=14)" — RSI14'ü EMA tüneli yanında izleme; 50 yukarı geçişi veya zorunlu birleşik giriş tanımı yok — çekirdek belli.
- Örnek ve sonuç: görselden: 1827737743683707129-2.png DOAS.IS, 2024-01-01–2024-08-24; EMA12/144/169 ve RSI14 çizimi. İşlem sonucu yok. X510 ayrı gönderide bu EMA'ların 8/150/150 optimizasyonunu kaydeder.
- Tansu'nun vurgusu: "daha klasik çalışmak isteyen arkadaşlar bunları da kullanabilir."
- YORUM: Defter-5 X010'daki EMA dizilimi/kesişimi tekrarlanmadı; buradaki yeni ayrıntı RSI14/50 ile çizimdir. R128'in EMA50/100/200 kuralını Vegas'a dönüştürmez.

### X520 · 2024-09-23 19:59:08 UTC · Uyumsuzluk bakış süresi ve profil bölgesi seçimi
- Bağlı: R116 / R186; Öneri: tema-5a #20
- Yazar: T (iki ayrı uygulama cevabı).
- Kaynak: 1838307130526310602 (2024-09-23 19:59:08 UTC), 2005293321233576379 (2025-12-28 15:02:38 UTC).
- Fikirler:
  - [ölçüm-yöntemi] "lookback_hours_list = [24, 72, 168, 336, 720]" — saatlik veride 1/3/7/14/30 gün geri bakış; listeden ayarlanabilen süreler — kural tam (ayar listesi).
  - [ölçüm-ilkesi] "Sabit bir bar sayısı yerine fiyat hareketine (dalgalanmaya) göre manuel seçin" — yatayda akümülasyon alanının tamamı; trendde dalganın başlangıç/bitişi — çekirdek belli.
  - [ölçüm-yöntemi] "günlük grafikte son 60 bar (3 ay) piyasa dengesini görmek için idealdir" — günlük profil için örnek varsayılan; manuel alan seçimiyle birlikte — çekirdek belli.
- Örnek ve sonuç: Bu iki metinde sonuç sayısı yok. 24–720 saat listesi ile 60 günlük bar ayrı ölçüm bağlamlarıdır.
- Tansu'nun vurgusu: "Geriye bakış sürenizi ayarlayabiliyorsunuz"
- Belirsiz: İkinci metin profil bölgesi için yorumlanabilir; AVWAP'ın sabit son 60 barla başlatılacağını açıkça söylemez. R186'ya pencere/bölge seçimi eklenir, yeni anchor kuralı türetilmez.

### X521 · 2024-12-31 23:36:12 UTC · Sermayeyi ikiye katlama olasılığı ve rastgele yürüyüş
- Bağlı: R185; Öneri: tema-5a #21
- Yazar: T (kısa olasılık cevapları) + M (uzun random-walk açıklaması; T girişli).
- Kaynak: 1874238154355728692 (2024-12-31 23:36:12 UTC), 1874240306461512014 (2024-12-31 23:44:45 UTC), 1977458197158932959 (2025-10-12 19:35:48 UTC).
- Fikirler:
  - [boyut-risk; T] "kazanma ihtimali %49 kaybetme ihtimali %51 ise"; "paranızı x2 yapma ihtimaliniz matematiksel olarak %1.80" — bir sonraki örnekte %51 kazanma → %98; başlangıç sermayesi/birim bahis, kazanç-kayıp oranı ve sınır koşulları yok — yalnız fikir.
  - [ölçüm-ilkesi; M] "adım sayısının karekökü oranında uzaklaşıyorlar." — random-walk mesafe ölçeği; 100 adım/10 birim ve 10.000 adım/100 birim örneği — çekirdek belli.
- Örnek ve sonuç: İlk T gönderisi iflastan önce x2 olasılığı %1,83, sonraki T cevap %1,80 der. Simülasyon anlatımı farklı sarhoş tiplerini ayırır; gerçek hisse veya tamamlanmış Risk of Ruin hesabı yok.
- Tansu'nun vurgusu: "Ben değil matematik söylüyor."
- Belirsiz: %1,83/%1,80 farkı yuvarlama veya ayrı model olabilir; parametreler olmadığından çözülemiyor. x2'ye iflastan önce ulaşma olasılığı ile iflas riskinin kendisi aynı çıktı değildir.
- YORUM: Kazanma olasılığı tek başına bu x2 oranlarını belirlemez; rakamlar aktarılmış iddia olarak tutuldu, genel sermaye kuralı yapılmadı. Ekimdeki fiyat tahmini eleştirisi M gövdedir; X509/X522'deki T yön sınıflaması bunu toptan işlem yasağı olarak okumayı engeller.

### X522 · 2024-11-20 14:21:07 UTC · KNN ile yön sınıflaması
- Bağlı: R021; Öneri: tema-5a #22
- Yazar: T (kendi model cevapları) + G (tahmin/gerçek yön grafiği).
- Kaynak: 1859240563205107928 (2024-11-20 14:21:07 UTC), 1861901396506743020 (2024-11-27 22:34:20 UTC), 1864342754844660140 (2024-12-04 16:15:25 UTC), 1864545215593304274 (2024-12-05 05:39:55 UTC).
- Fikirler:
  - [ölçüm-yöntemi] "Bağımlı değişkenim yükselecek ya da düşecek" — ertesi gün yön sınıfı; özellik olarak open/high/low/adj close adı geçiyor — çekirdek belli.
  - [ölçüm-yöntemi] "Öklid uzaklığı ile mesafeleri ölçüp sınıflandırıyorum." — komşuluk tabanlı KNN; k, ölçekleme ve eğitim/test bölümü verilmez — çekirdek belli.
  - [ölçüm-ilkesi] "ne ka sorusunun cevabı sağlıklı olmaz." — büyüklük tahmini ile kategorik yön sınıflamasını ayırma — çekirdek belli.
- Örnek ve sonuç: T metni %75 doğruluk iddiası ve ertesi gün yukarı tahmini. görselden: 1859240563205107928-1.png XU100.IS, ±1 gerçek/tahmin yön; "The predicted movement for 2024-11-21 is: up". Ertesi gün gerçekleşmiş doğrulama sonucu bu kaynak setinde yok; grafikte %75 hesap dökümü yok.
- Tansu'nun vurgusu: "Bakıp göreceğiz"
- Çelişir: R185'in M yön tahmini reddi; Tansu kendi algoritmasını yön sınıflaması diye anlatır.
- Belirsiz: 27 Kasım "B.lı = open high low adj close / B.sız = Up/down olma durumu" der; 4 Aralıkta yönü bağımlı değişken olarak düzeltir. Sonraki açık tanım esas alındı; özellik/çıktı adları ilk kısaltmanın tersliğine göre kurulmadı. Önerinin OHLC adı Adj Close ayrıntısını kaybettiğinden açıldı.

### X523 · 2025-05-19 17:53:54 UTC · Envanter azaltma için Monte Carlo çerçevesi
- Bağlı: R225 (icra/likidite bağı); Öneri: tema-5a #23
- Yazar: T giriş + M (başlıklı, kavramsal simülasyon anlatımı).
- Kaynak: 1924523925683274094 (2025-05-19 17:53:54 UTC).
- Fikirler:
  - [ölçüm-yöntemi; M] "Her strateji için 100.000 farklı fiyat senaryosu oluşturulur (Monte Carlo)." — lineer, hızlı/yavaş lineer, hızlı/yavaş kuadratik olmak üzere beş satış profili; Brownian motion fiyat senaryoları — çekirdek belli.
  - [boyut-risk; M] "piyasa etkisi (likidite kaybı) ile zamanlama riski arasında optimal dengeyi kurmalıdır." — q(t) envanter, s(t) fiyat, λ(t) satış hızı; β piyasa etkisi; PnL/ortalama baz puan; yatay/yukarı/aşağı trend — çekirdek belli.
- Örnek ve sonuç: 10.000 hisse satışı örnek problem; parametreli sayısal sonuç veya koşu çıktısı yok. 100.000 senaryo anlatılan yöntem büyüklüğüdür; gerçek tamamlanmış koşu kanıtı değildir.
- Tansu'nun vurgusu: "Quant yatırım çalışmalarım devam ediyor. Son yaptığım çalışmayı kavramsal olarak size de anlatayım."
- YORUM: R225 emir defteri şekliyle bu kavramsal envanter modeli aynı araç sayılmadı. R182'nin M Monte Carlo reddi Markowitz ağırlık optimizasyonu bağlamındadır; icra simülasyonuna yönelik bir çelişki kurulmadı.

### X524 · 2026-02-05 21:37:11 UTC · Mevsimsel ARIMA stepwise AIC araması
- Bağlı: R174; Öneri: tema-5a #24
- Yazar: T (kısa paylaşım) + G (arama çıktısı).
- Kaynak: 2019525738207060400 (2026-02-05 21:37:11 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "Performing stepwise search to minimize aic" — stepwise AIC minimizasyonu; mevsimsel m=12, D=1; grid aramasından ayrı seçim yolu — çekirdek belli.
- Örnek ve sonuç: görselden: 2019525738207060400-1.png, görünür sonlu AIC değerlerinin en düşüğü ARIMA(2,0,1)(2,1,0)[12] intercept, AIC=4346,705. ARIMA(0,0,1)(2,1,0)[12] AIC=7091,326; ARIMA(2,0,1)(1,1,0)[12] AIC=4558,372; (2,0,1)(2,1,1)[12] inf (görsel açıldı, 08.10). Liste kesik; nihai seçilmiş model veya tahmin hatası sonucu yok.
- Tansu'nun vurgusu: "SARIMAX modeli"; "Bekle ki bekle...."
- YORUM: Seri adı/frekansı yok; m=12'den aylık seri olduğu kesinleştirilmedi. Önerinin MAE/MSE/RMSE–ResNLS-5 sonucu dış çalışmadan aktarım olduğundan bu kayda alınmadı.

### X525 · 2025-08-14 13:34:31 UTC · Koşulları koruyarak rastlantı sınaması
- Bağlı: yeni yöntem; Öneri: tema-5a #25
- Yazar: M (uzun, genel ders biçimli metin; Tansu hesabında).
- Kaynak: 1955986393622306882 (2025-08-14 13:34:31 UTC).
- Fikirler:
  - [ölçüm-yöntemi; M] "örneğin aynı volatilite dağılımını koruyarak" — önce gerçek korelasyon; bir seriyi koşulları sabit tutarak karıştır/yeniden örnekle; tekrarlı şans korelasyonu dağılımıyla karşılaştır — çekirdek belli.
  - [ölçüm-ilkesi; M] "Eğer gerçek korelasyonunuz bu dağılımın uçlarında yer alıyorsa, ilişkinin rastlantısal olma ihtimali düşüktür." — hisse/hisse veya hisse/endeks; tekrar sayısı, koşullu örnekleme modeli ve anlamlılık eşiği yok — çekirdek belli.
- Örnek ve sonuç: Uygulanmış seri, sayısal korelasyon dağılımı veya sınama sonucu yok.
- Tansu'nun vurgusu: Bu metinde M gövdesinden ayrılabilen Tansu'nun kendi vurgu cümlesi yok.
- YORUM: Kaynağın conditional randomization test adı korundu; seriyi basitçe karıştırmanın tüm zaman bağımlılığını veya gerekli koşullu dağılımı koruduğu kaynakta gösterilmiyor. Tam istatistik algoritması diye yazılmadı.

### X526 · 2025-08-01 08:19:26 UTC · Risk türüne göre performans oranı seçimi
- Bağlı: R138 / R251 (performans kıyası bağı); Öneri: tema-5a #26
- Yazar: T (kendi analiz/kod giriş ve son notları) + M (oran açıklamaları).
- Kaynak: 1951196059939569688 (2025-08-01 08:19:26 UTC), 1953401516565340457 (2025-08-07 10:23:08 UTC), 1980319432141308317 (2025-10-20 17:05:19 UTC).
- Fikirler:
  - [ölçüm-yöntemi; M] "Formülü fon getirisi - risksiz faiz / beta." — Treynor=(R−rf)/β; Jensen alpha=R−CAPM beklenen getiri; M2=rf+Sharpe×piyasa volatilitesi — çekirdek belli.
  - [ölçüm-yöntemi; M] "Formülü fon getirisi - benchmark getirisi / tracking error." — IR=(R−Rb)/tracking error; Sortino=(R−rf)/downside deviation; toplam risk ve sistematik risk ayrımı — çekirdek belli.
  - [ölçüm-ilkesi; M] "Risk algınuza göre 2 sini kullanabilirsiniz." — toplam riskte Sharpe/M2/Sortino; çeşitlendirilmiş portföyde Treynor/alpha; orta vade 3 ay–1 yıl ve örnek 30 günlük rolling — çekirdek belli.
- Örnek ve sonuç: Ekim metninde GGM Sharpe 5,50; PEA 4,91; IHY kümülatif getiri 230,9 ve volatilite 58,3; GGM getiri 40,5/volatilite 2,6. Bu değerlerin ölçüm penceresi ve rf tanımı metinde yok; ayrı kayıtlardaki rasyolarla doğrudan kıyaslanmadı.
- Tansu'nun vurgusu: "Diğer metriklerin yer aldığı listeyi de daha sonra paylaşacağım."; "Kodunu hazırladım."
- YORUM: Kaynak formülleri parantezsiz sözel anlatır; çıkarma işlemi paya alınarak açık yazıldı. Hesap dönemleri ve downside/tracking-error ayrıntıları eksik olduğundan M fikirleri kural tam sayılmadı. "yüksek alpha düşük information ratio güzeldir" (1773320333249896719) ayrışması X533'te iki okumayla yer alır.

### X527 · 2024-04-01 18:50:57 UTC · Günlük getiri IQR'ı ve kantil örneğinin sınırı
- Bağlı: R033 / R190; Öneri: tema-5a #27
- Yazar: T (getiri dağılımı ve kendi KCHOL denemesi) + G (kod/grafikler).
- Kaynak: 1774872093701615913 (2024-04-01 18:50:57 UTC), 1774872096142754162 (2024-04-01 18:50:57 UTC), 1822549636013240372 (2024-08-11 08:24:29 UTC), 1827401211731189852 (2024-08-24 17:42:55 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "returns = selected_stocks.pct_change().dropna()" — düzeltilmiş kapanıştan günlük basit getiri; IQR=P75−P25; boxplot ile uç değerleri gözleme — kural tam (ölçüm).
  - [ölçüm-yöntemi; T] "15. ve 85. kantillerin geçilmesi" — KCHOL mean-reversion denemesi; oran serisinin tanımı ve tüm giriş/çıkış ayrıntıları yok — çekirdek belli.
  - [ölçüm-ilkesi; T] "Görünüşe göre belirtilen zaman diliminde mean reversion #KCHOL hissesinde iyi çalışmamış" — al-tut kıyası, düşen piyasada ortalamanın maliyet altına inmesi uyarısı — çekirdek belli.
- Örnek ve sonuç: görselden: 1822549636013240372-1.png ve -2.jpg BIMAS/EKGYO/GUBRF günlük getirileri, 2014-07-30–2024-07-30; hesap IQR'ı ölçer, otomatik hisse silme kodu yok. 1774872096142754162-1.jpg kantil çizgileri yaklaşık 1,10 ve 0,97. T metni B&H 5,58 / mean reversion 1,31 kat değerlenme der; -2.jpg yatırım büyümesi grafiği yaklaşık 6,6 ve 2,3 seviyelerine ulaşır. İki okumada da al-tut daha yüksek.
- Tansu'nun vurgusu: "Sıra dışı değerleri spot ediniz. Anomalileri ortaya çıkarmanızda perspektif sağlar."
- Belirsiz: Metnin 5,58/1,31 sayıları net kazanç çarpanı, grafiğin yaklaşık 6,6/2,3 sayıları başlangıç sermayesi dahil toplam çarpan olabilir; metin "değerlenmiş" dediği için bu kesinleştirilemez. Ayrı hesap/grafik sürümü olasılığı da açık; sayıların birbirinin yerine geçmesi önlendi.
- YORUM: IQR hesaplamak R033'ün |30G getiri|>%50 eleme eşiğini değiştirmez. R190 değer bölgesi/POC yöntemidir; 15/85 kantil yalnız ayrı varyant bağıdır. KCHOL sonucu başarılı uygulama diye alınmadı; sınırlayıcı ölçüm kaydedildi.

### X528 · 2024-08-18 21:03:02 UTC · VIF, artık bağımlılığı ve Ridge/Lasso düzenlileştirme
- Bağlı: R066; Öneri: tema-5a #28
- Yazar: T (Ridge denemesi, VIF cevabı ve alpha notu) + M (PCA/otokorelasyon açıklamaları) + G (Lasso grafikleri ve açıklayıcı metin).
- Kaynak: 1825277249374867614 (2024-08-18 21:03:02 UTC; öneri belgesinin önceki bölümündeki ek kaynak), 1825279192390594981 (2024-08-18 21:10:46 UTC; aynı konu ek kaynağı), 1825285752105619922 (2024-08-18 21:36:50 UTC), 1825488501254578373 (2024-08-19 11:02:29 UTC), 1941790321668432140 (2025-07-06 09:24:24 UTC), 1950584440805081552 (2025-07-30 15:49:05 UTC).
- Fikirler:
  - [temel-değerleme; T] "Ridge regresyon optimal alpha 0,26 değeri ile 2024/6 dönem Bimaş F/K tahmini 20,89 olarak bulundu" — Ridge ile F/K tahmini; optimizasyon aralığı ve eğitim/test ayrımı yok — çekirdek belli.
  - [ölçüm-ilkesi; T] "ben bakıyorum 🎯" — hocasının VIF'e bakmama görüşünü aktarırken kendi tercihi VIF'e bakmak; eşik yok — yalnız fikir.
  - [ölçüm-yöntemi; G] "RMSE vs. Alpha for Lasso Regression" — alpha 10^−4–10^4 grafiği, minimum yaklaşık 10^−2; katsayıların sıfıra küçülmesi; veri/model tanımı yok — çekirdek belli.
  - [ölçüm-ilkesi; M] "Anlamak ön plandaysa korelasyon, sadece tahminse PCA daha uygundur." — yorumlanabilirlik/boyut azaltma ayrımı; PCA bileşen sayısı ve seçme eşiği yok — çekirdek belli.
  - [ölçüm-yöntemi; M] "Durbin-Watson testi gibi yöntemlerle ölçülmesi" — zaman serisi/kesitsel veri ve artık otokorelasyonu ayrımı; karar sınırları yok — yalnız fikir.
- Örnek ve sonuç: 1825279192390594981 T metninde Ridge BİMAŞ 2024/6 F/K=20,89, alpha=0,26; MSE=3,0899, RMSE=1,7578, R²=0,9613. Gerçekleşmiş F/K ile örneklem dışı kıyas yok. görselden: 1825488501254578373-1.png Lasso RMSE minimumu yaklaşık 0,01 alpha'da; yüksek alpha'da RMSE yaklaşık 9,4 plato. -2.png katsayı eğrileri, x ekseni Log10(Alpha). Lasso grafiğinin yaklaşık optimumu bu grafiğe aittir; hisse/model adı yok.
- Tansu'nun vurgusu: "Alpha alpha alpha, dün gece rüyamda alphalar ile oynuyordum."; "Önemlidir, diyim."
- YORUM: Buradaki alpha düzenlileştirme katsayısıdır; yatırım performansı alpha'sı değildir. Ridge'in adı öneri belgesinin önceki bölümünde verilen 1825277249374867614'te, sayısal denemesi arşivdeki 1825279192390594981'de bulundu. Ridge alpha=0,26 ile Lasso grafiğindeki yaklaşık 0,01 ayrı modellerdir. M gövdesinin zaman serilerinde otokorelasyonun önemsenmemesi yönündeki genellemesi uygulama kuralı yapılmadı.

### X529 · 2025-03-26 15:00:49 UTC · Kur pariteleri, psi ve forward çerçevesi
- Bağlı: R052; Öneri: tema-5a #29
- Yazar: T (kurumsal çalışma/deneme girişleri) + M (parite ve forward açıklamaları) + G (psi kodu).
- Kaynak: 1904911424641450458 (2025-03-26 15:00:49 UTC), 1904911428877762622 (2025-03-26 15:00:50 UTC), 1906617984665137406 (2025-03-31 08:02:05 UTC; ust.jsonl, yazar The_Tansu_), 1906617987676696651 (2025-03-31 08:02:06 UTC), 1984661206162964976 (2025-11-01 16:37:59 UTC).
- Fikirler:
  - [ölçüm-yöntemi; M] "(Δs = π - π*)"; "(i - i* = E(π - π*))"; "(i - i* = E(Δs))"; "(i - i* = p)" — PPP, Fisher, UIP ve forward prim ilişkisi; ufuk/rate türü verilmez — çekirdek belli.
  - [ölçüm-yöntemi; G] "weights = np.array([psi**i for i in range(n+1)])" — s=(1−ψ)Σψ^i E(x[t+i]); örnek beklenen kurlar beş değer: 39; 40,5; 42; 43; 44, ψ=0,60 — kural tam (paylaşılan sonlu toplam hesabı).
  - [ölçüm-ilkesi; M] "Konservatif fiyat → Monte Carlo dağılımı → Risk primi ayarı → Volatilite testi" — kurumsal forward pazarlığında faiz paritesi, simülasyon, CDS/volatilite/spread risk primi ve Euro/TL oynaklığı — çekirdek belli.
- Örnek ve sonuç: görselden: 1904911424641450458-1.png s_t^n=37,36416; T metni yaklaşık 37,36. Kasım metni iş yerindeki kullanımı anlatır; sayısal yeni forward sonucu yok.
- Tansu'nun vurgusu: "Şu da iş yerinde zaman zaman kullandığım yapı"
- Belirsiz: 1906617984665137406 tweets.jsonl'de yok, ust.jsonl'de The_Tansu_ adına tam metin/tarih var; başkasının sözü sayılmadı. ψ açıklaması düşük ψ'nin uzak gelecek ağırlığını artırdığını söylüyor; kodun ψ^i ağırlıkları tersini gösteriyor. Kaynak sözü ile kod okuması ayrıldı.
- YORUM: Düşük ψ uzak dönemlere göreli olarak daha az ağırlık verir. Sonlu toplamda (1−ψ) çarpanı ağırlık toplamını 1'e normalize etmez; "normalize edilmiş" açıklaması kesin hesap kuralı sayılmadı. Çalışma kur içindir, hisse fiyat tahmini değildir. Parite sadeleştirmeleri gerçek kurun garanti tahmini veya risksiz arbitraj diye yazılmadı.

### X530 · 2025-03-07 08:25:24 UTC · Opsiyon fiyatlama eğitim örnekleri ve kod sınırları
- Bağlı: yeni yöntem; Öneri: tema-5a #30
- Yazar: T (eğitim/kod paylaşımı) + M (uzun kullanım açıklaması) + G (kod ve model çıktıları).
- Kaynak: 1897926542044389854 (2025-03-07 08:25:24 UTC), 1897926545328501123 (2025-03-07 08:25:24 UTC), 1897926549338214614 (2025-03-07 08:25:25 UTC), 1905916780465307673 (2025-03-29 09:35:45 UTC), 1979645829377057243 (2025-10-18 20:28:40 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "BS = BlackScholes(\"p\", S, X, Time, r, q, sigma)" — put: S=100, X=80, T=1, r=0,05, q=0, σ=0,2 — kural tam (örnek çağrı; fonksiyon tanımı bu görselde yok).
  - [ölçüm-yöntemi; G] "M = 3" — binom call: S0=strike=100, T=1, r=0,05, σ=0,2; dt=T/M, u=exp(σ√dt), d=1/u, q=(exp(rdt)−d)/(u−d); iskonto exp(−rdt), terminal max(S−K,0), geriye beklenen değer — kural tam (eğitim hesabı).
  - [ölçüm-yöntemi; M] "Black-Scholes opsiyon fiyatlama modelini kullanarak hisse senedi opsiyonlarının teorik değerini hesaplıyor ve Monte Carlo simülasyonuyla bu değeri doğruluyor." — teorik call ile simülasyon kıyası; genel tam girdi seti görünür parçada yok — çekirdek belli.
- Örnek ve sonuç: görselden: 1897926542044389854-1.png put=0,6872; 1905916780465307673-1.png binom call=11,0439. 1979645829377057243-1.png BS=3,7451887662410783; ilk simülasyon 3,84999 ve N=100.000 sonrası 3,79865 (görsel açıldı, 08.10). Kodlar çalıştırılmadı; rakamlar kaynak çıktılarıdır.
- Tansu'nun vurgusu: "Bu işte yeni iseniz bu koda bulaşmayın, iyi iseniz alın kullanın."
- YORUM: Ekim kodunda d1 paydası `/ sigma*np.sqrt(T)` yazılıdır; işlem önceliği σ'ya bölüp √T ile çarpar. Düzeltilmiş matematiksel ifade d1=[ln(S/K)+(r−q+σ²/2)T]/(σ√T), d2=d1−σ√T'dir; bu düzeltme kaynak alıntısı değildir, kod çalıştırılarak sınanmadı. Martta doğru put çağrısı q kullanır; aynı dizinin call/put fiyat eğrilerinde r−q argümanı kullanılıyor. q temettü verimi kabulünde r−q yerine q gerekir; fonksiyon tanımı görünmediği için arayüz varsayımı açık tutuldu. Kusurlu kod gerçek değerleme motoru diye alınmadı.

### X531 · 2025-02-27 18:32:15 UTC · Günlük Pearson ve 12 aylık rolling korelasyon
- Bağlı: R091; Öneri: tema-5a #31
- Yazar: T (kod paylaşımı ve kendi korelasyon değerlendirmesi) + G (kod/ısı haritası).
- Kaynak: 1895180161261412820 (2025-02-27 18:32:15 UTC), 2084854243131846782 (2026-08-05 04:09:20 UTC).
- Fikirler:
  - [ölçüm-yöntemi; G] "corr_matrix = returns.corr()" — kapanış pct_change sonrası Pearson matrisi; 2024-01-01–2025-01-01 — kural tam (hesap).
  - [ölçüm-yöntemi; T] "Long-term and 12-month rolling correlation and R-squared values" — petrol/altın için uzun dönem ve 12 aylık rolling korelasyon/R²; karar eşiği yok — çekirdek belli.
- Örnek ve sonuç: görselden: 1895180161261412820-1.png ve -2.png THYAO/TUPRS/ASELS/SASA/EREGL/KRDMD; EREGL–KRDMD r=0,74. Ağustos T cevabı petrolün altını etkilemediğini söyler; sayısal sonuç/veri penceresi paylaşılmaz.
- Tansu'nun vurgusu: "Basit kodlamalar yapalım"
- YORUM: 12 aylık pencere petrol/altın örneğidir; R091 rejim tespitinin kesin penceresi olarak atanmadı. Korelasyon/R²'den nedensel etki yokluğu kanıtı çıkarılamaz; bu, Tansu'nun kaynak değerlendirmesidir.

### X532 · 2025-08-12 14:53:48 UTC · Fourier keşfi ardından Wavelet
- Bağlı: R122; Öneri: tema-5a #32
- Yazar: T (kendi hibrit yaklaşım önerisi) + M (sinüs/Fourier ders gövdesi; T girişli).
- Kaynak: 1955281569599402000 (2025-08-12 14:53:48 UTC), 1978893346727956651 (2025-10-16 18:38:34 UTC).
- Fikirler:
  - [ölçüm-yöntemi; M] "Frekansı"; "Genliği"; "Fazı" — fiyatı farklı sinüs bileşenlerine ayırma; frekans, etki büyüklüğü ve döngü konumu; detrend/pencere/yöntem ayrıntısı yok — yalnız fikir.
  - [ölçüm-yöntemi; T] "Bence iİlk keşif için Fourier yapılabilir, dominant periyotları bulunur, sonra Wavelet ile o periyotların zamanla nasıl değiştiğine bakılır." — önce baskın dönem keşfi, sonra zaman içinde değişim; wavelet ailesi ve ölçek seçimi yok — çekirdek belli.
- Örnek ve sonuç: İki metinde sayısal periyot, backtest veya uygulanmış hibrit sonuç yok.
- Tansu'nun vurgusu: "Hibrit yaklaşım en mantıklısı bu teoride."
- YORUM: Tansu "teoride" der; uygulanan kârlı sistem diye yazılmadı. Wavelet, Fourier'in zaman bilgisini kaybetme sınırına karşı önerilir.

### X533 · 2024-03-03 15:14:26 UTC · Çelişki taramasından kalan ölçüm ve uygulama ayrımları
- Bağlı: R110 / R230 / R058 / R185 / R223 / R170 / R101 / R013; Öneri: tema-5a #33 (Ç1–Ç9 taraması; yinelenmeyen ayrıntılar)
- Yazar: T (kısa kendi sözleri/ölçümler) + M (Pandas eğitim gövdesi ve model açıklamaları) + G (kod/grafik).
- Kaynak: 1764308359635710087 (2024-03-03 15:14:26 UTC), 1773320333249896719 (2024-03-28 12:04:48 UTC), 1778899999671066629 (2024-04-12 21:36:24 UTC), 1840098451750826475 (2024-09-28 18:37:12 UTC), 1844502539414511699 (2024-10-10 22:17:29 UTC), 1845098408727461989 (2024-10-12 13:45:15 UTC), 1897620709624442886 (2025-03-06 12:10:07 UTC), 1912735331918516711 (2025-04-17 05:10:14 UTC). Karşılaştırma/tarihçe: 1923641490783322182 (2025-05-17 07:27:25 UTC), 1980319432141308317 (2025-10-20 17:05:19 UTC), 1983528060700778778 (2025-10-29 13:35:16 UTC), 1992526564110504275 (2025-11-23 09:32:06 UTC), 1993341929614897406 (2025-11-25 15:32:05 UTC), 1994833931204436243 (2025-11-29 18:20:46 UTC), 1995204241905107441 (2025-11-30 18:52:15 UTC), 2005015848080097725 (2025-12-27 20:40:04 UTC), 2023071995768778814 (2026-02-15 16:28:45 UTC), 2047695947333824992 (2026-04-24 15:15:32 UTC), 2049193407755764029 (2026-04-28 18:25:55 UTC), 2053149182697886143 (2026-05-09 16:24:45 UTC), 2086377179554660583 (2026-08-09 09:00:57 UTC), 2091438754732863571 (2026-08-23 08:13:50 UTC).
- Fikirler:
  - [ölçüm-ilkesi; T] "yüksek sharpe ratio yakalamak için standart sapmanın düşük olduğu hisselerde trade yapmak önemlidir." — aynı getiri farkında düşük risk paydası; düşük std eşiği yok — çekirdek belli.
  - [ölçüm-yöntemi; T] "basit bir örnek emtia fiyat tahmin algoritması." — Random Forest eğitim örneği, R²=0,98 iddiası; emtia, hisse değil; veri/test bölümü yok — yalnız fikir.
  - [ölçüm-yöntemi; M] "df['Close'].rolling(window=20).std() → 20 günlük volatilite." — fiyat düzeyinin 20G std'si; getiri std'sinden ayrı TL ölçüsü — çekirdek belli.
  - [ölçüm-ilkesi; T] "%R ile MACD, BTC'de felaket bir senaryo yarattı. Maalesef iyi çalışmadı." — basit −80 al/−20 sat varyantının BTC sonucuyla sınırlandırılması; başarılı yeni giriş kuralı olarak alınmaz — çekirdek belli.
  - [portföy; T] "Long, prensip olarak short işlem yapmıyorum :)" — kişisel uygulama tercihi; tüm yöntem açıklamalarına short yasağı değildir — çekirdek belli.
- Örnek ve sonuç: görselden: 1897620709624442886-1.png, TUPRS kapanış std20 "Volatilite_20" diye adlandırılmış; getiri değil fiyat giriyor. 1844502539414511699-1.jpg: −20 SELL/−80 BUY referansları. 1845098408727461989-1.jpg–4.jpg: BTC WR14+MACD ve ayrı WR14 kıyasları; T metni ilkinde 100.000$ için 3.546$ (%3,5) kâr, al-tut %42,64; yalnız WR'de %81, al-tut %85. Birleşik grafikte başlangıç 2024-01, yalnız WR grafiğinde 2023-11; sonuçlar aynı pencere sanılmadı. İki örnekte de strateji al-tutun altında.
- Tansu'nun vurgusu: "Maalesef iyi çalışmadı."; "Long, prensip olarak short işlem yapmıyorum :)"
- Belirsiz: Ç4 fiyat std'si eğitim/Bollinger bağlamında geçerli bir fiyat genişliği olarak mı, getiriler arası kıyas için yanlış adlandırma olarak mı sunuluyor? Kaynak amacı kesinleştirmiyor; R223 getiri std'siyle eşitlenmedi. Ç5 düşük std tercihi Sharpe verimliliği, R110/R230 yüksek volatilite tercihi aktif trade fırsatı olarak okunabilir; aynı seçme amacı kabul edilirse ayrışma vardır, bağlamlar ayrılırsa çelişki zorunlu değildir. Ç9 kişisel long uygulaması ile short içeren yöntem öğretimi ayrı olabilir; alternatif okuma 2024–2026 arasında uygulama değişimidir, kaynak doğrudan değişim ilan etmez.
- Belirsiz: 28 Mart T sözü "yüksek alpha düşük information ratio güzeldir." der; 20 Ekim M metni IR'yi aktif getiri/tracking error olarak tanımlar. İlki tracking error ile karışmış ifade olabilir veya farklı risk tercihi/ölçü kastı olabilir; kaynak kendi düzeltmesini vermiyor. İki okuma korunur; düşük IR evrensel seçim kuralı yapılmadı.
- YORUM: Ç1: HMM+lojistik hibrit önerisi 17 Mayıs 2025 M metnidir; 9 Mayıs 2026 T sözü trend rejimi için HMM'ye gerek olmadığını söyler ve R091'de aynen vardır. T'nin sonraki sözü esas alındı; HMM'yi zorunlu rejim kuralı yapan öneri alınmadı. R091'in kayıt tarihi paylaşım tarihi değildir.
- YORUM: Ç2 yön ayrımı X509/X522'de ve R185 ile "Çelişir" satırında işlendi; Random Forest emtia örneği R058'in hisse/piyasa değeri ayrımını çürütmez. R185 özgün M gönderisi 27 Aralık 2025, R058 özgün T gönderisi 9 Ağustos 2026. Ç3, X507'de takvim varsayımı ve √252 üzerinden işlendi. R223 özgün gönderisi 30 Kasım 2025'tir.
- YORUM: Ç6, R170'in 15 Şubat 2026 SMA14/WR14 trend-pullback önerisiyle 2024'teki basit tersine-dönüş örneği ayrı yöntemlerdir; BTC başarısızlığı R170'in sınanmış başarısızlığı sayılmaz. Ç7, X513'te optimizasyon ile belirli kurulum ayrıldı; R233 özgün gönderisi 23 Kasım 2025. Ç8'in derinlik ölçümü ve R225 çelişkisi defter-5 X036'da zaten vardır; yeni X numarasıyla tekrarlanmadı. R225'in 29 Kasım 2025 tarihi arşivde doğrulandı; bu tarih artık belirsiz değildir. R110 24 Nisan 2026, R230 25 Kasım 2025, R101 28 Nisan 2026 ve R013 23 Ağustos 2026 özgün kaynaklarıyla tarihlendi.

### tema-5a özeti

Olgunluk, kaydın ana yeni katkısı içindir; alt fikirlerdeki daha dar hesaplar ayrıca etiketlendi. T+M kayıtlarında başlıklı/LLM biçimli fikirler M olarak tutuldu, T'nin kendi sözü sayılmadı. Kaynaklar yerel arşivden okundu; kodlar çalıştırılmadı. Bu belge içerik doğrulamasıdır, yöntemlerin gerçek kullanımda başarı sınaması değildir.

| X no | başlık | bağlı R | olgunluk | yazar |
|---|---|---|---|---|
| X501 | Fon likiditesi ve stres altında tasfiye | yeni yöntem | çekirdek belli; tablo hesabı kural tam | T+M+G |
| X502 | Fon akışı erken uyarı ve aktivasyon | yeni yöntem | çekirdek belli | T+M+G |
| X503 | Korelasyon–Granger hattı | yeni yöntem | çekirdek belli | T+M+G |
| X504 | ADF/KPSS durağanlık ön testi | yeni yöntem | çekirdek belli | M |
| X505 | GARCH örneği ve model seçimi | R097 | çekirdek belli | T+M+G |
| X506 | DtD denemesi ve lojistik PD | R061 | çekirdek belli; ilk deneme yalnız fikir | T+M+G |
| X507 | Sharpe/Sortino yıllıklaştırma | R137/R115/R223 | kural tam (Sharpe kodu) | T+M+G |
| X508 | Rolling Sharpe/alpha | R202 | çekirdek belli | T+M+G |
| X509 | Lojistik yön olasılığı | R234 | çekirdek belli | T+G |
| X510 | Sağlam optimizasyon bölgesi | R138 | çekirdek belli | T+M+G |
| X511 | Faktör beta/Fama-French | R200 | çekirdek belli | T+M+G |
| X512 | Bollinger20 ve VaR ufku | R053 | kural tam (Bollinger); VaR yalnız fikir | T+M+G |
| X513 | SMA tabanlı RSI | R233/R138 | kural tam (hesap) | T+G |
| X514 | İsabet/PF ve aşırı uyum iddiası | R140 | çekirdek belli | T+M+G |
| X515 | WMA/MACD ve WT revizyonu | R258 | WMA/MACD kural tam; WT çekirdek belli | T+G |
| X516 | CMF20 ve SMA14 ATR | R137/R184/R212 | CMF kural tam; ATR çekirdek belli | T+M+G |
| X517 | Ichimoku bileşen hesabı | yeni yöntem | kural tam (hesap) | T+G |
| X518 | Çift EMA ve ayrı CCI | R124/R105 | kural tam (hesap) | T+G |
| X519 | Vegas yanında RSI14 | R128/R138 | kural tam (çizim); giriş eksik | T+G |
| X520 | Lookback ve profil alanı | R116/R186 | çekirdek belli | T |
| X521 | x2 olasılığı/random walk | R185 | yalnız fikir; random-walk çekirdeği belli | T+M |
| X522 | KNN yön sınıflaması | R021 | çekirdek belli | T+G |
| X523 | Envanter Monte Carlo | R225 | çekirdek belli | T+M |
| X524 | Stepwise mevsimsel ARIMA | R174 | çekirdek belli | T+G |
| X525 | Koşullu rastlantı sınaması | yeni yöntem | çekirdek belli | M |
| X526 | Performans oranı seçimi | R138/R251 | çekirdek belli | T+M |
| X527 | Günlük IQR/kantil örneği | R033/R190 | IQR kural tam; kantil çekirdek belli | T+G |
| X528 | VIF/PCA/Ridge/Lasso | R066 | çekirdek belli | T+M+G |
| X529 | Kur paritesi/psi/forward | R052 | çekirdek belli; sonlu toplam kural tam | T+M+G |
| X530 | Opsiyon eğitim hesapları | yeni yöntem | çekirdek belli; binom kural tam | T+M+G |
| X531 | Pearson/rolling korelasyon | R091 | çekirdek belli; Pearson hesabı kural tam | T+G |
| X532 | Fourier ardından Wavelet | R122 | çekirdek belli | T+M |
| X533 | Kalan ölçüm/uygulama ayrımları | R110/R230/R058/R185/R223/R170/R101/R013 | çekirdek belli; RF yalnız fikir | T+M+G |

### tema-5a alınmayanlar

Tamamen alınmayan öneri yok: 33 öneri, X501–X533 olarak kaydedildi. Aşağıdaki alt bölümler yeni fikir/kural yapılmadı; neden ve karşı kanıt ilgili kayıtta korunur.

| öneri no | neden | kanıt id |
|---|---|---|
| #15 — WaveTrend periyodunu yeniden yöntem yapma | Yinelenen: WT(10,21) çizim ayarı defter-5 X030'da zaten var. Yeni eşik revizyonu ve DOAS sınırlaması WMA/MACD ile X515'e alındı. | 1845362765898097116, 1845362768632799316; X030 |
| #24 — ResNLS-5 ve karşılaştırma tablosu | Tansu'nun kendi modeli/ölçümü değil: üst gönderi dışarıda okuduğu bir gönderi/testi aktardığını söyler. SARIMAX kısmı X524'e alındı. | 1795910554965385316, 1795910557695877254 |
| #33 Ç1 — HMM'yi gerekli rejim yöntemi yapma | Sonraki T sözü trend rejimi için HMM'ye gerek olmadığını söyler; çürüten söz R091'de zaten var, yinelenen yeni kayıt yapılmadı. Hibrit girdi bağlamının ayrı olabileceği X533'te korunur. | 1923641490783322182; 2053149182697886143 (R091) |
| #33 Ç2 — yön tartışmasının tekrar kaydı | Yinelenen: yön olasılığı ve R185'in M gövdesiyle çelişki X509/X522'de işlendi. Emtiadaki RF öğretim örneği X533'te tutuldu. | 1864545215593304274, 1893042422088642888, 1778899999671066629 |
| #33 Ç3 — 255/252 ve ×252 tekrar kaydı | Yinelenen: X507'de 255 varsayımı korundu; kaynakla uyuşmayan std×252 yerine T'nin std×√252 kodu esas alındı. | 1915540627405554032, 1942696711287169192, 2099366035111493673 |
| #33 Ç7 — RSI eşiği tartışmasının tekrar kaydı | Yinelenen: optimizasyon ilkesi X513'te; belirli RSI14/30/70 kurulumunun R233'te olması ayrı bağlamdır. | 1860405835354054736, 1992526564110504275 |
| #33 Ç8 — emir defterini tek başına yön sinyali yapma | Tansu'nun kendi ölçümü tek başına güçlü yön ilişkisini desteklemiyor; çürüten ölçüm ve Çelişir: R225 satırı defter-5 X036'da zaten var. | 1983480217894060348, 1983528060700778778; 1994833931204436243 (R225) |

## Tema 5b — Ürün hedefi ve sinyal sonucu

### X601 · 2025-03-27 06:59:09 UTC · Rolling Sharpe seviyesinden yukarı tepki
- Bağlı: yeni yöntem; Öneri: tema-5b #1
- Yazar: T + G (Sharpe grafikleri ve hisse listesi).
- Kaynak: 1905152595586318386 (2025-03-27 06:59:09 UTC), 1905153170805776426 (2025-03-27 07:01:26 UTC), 1905219676352676212 (2025-03-27 11:25:42 UTC), 1905345708858749109 (2025-03-27 19:46:31 UTC).
- Fikirler:
  - [teyit-tetik; G] "Rolling Sharpe (21 gün)"; "-0.40 Seviyesi" — ICUGS önceki −0.5398, son −0.3911; 21 günlük Sharpe, seviyenin altından üstüne geçiş — çekirdek belli.
  - [teyit-tetik; G] "-0.6 Seviyesi" — METRO önceki −0.6207, son −0.5819; görselde tepki tarihi 2025-03-24 — çekirdek belli.
- Örnek ve sonuç: görselden: listede KRTEK, IHLGM, ICUGS, GEDZA. Tansu METRO gönderisinde 25 Mart taraması ve 26 Mart %5 der; gün sonu gönderisinde bir tavan ve iki iyi getiri bildirir. İşlem fiyatı, maliyet ve tüm sinyallerin sonucu yok.
- Tansu'nun vurgusu: "Bugün bu stratejimiz ile tavan aldık 2 tane de iyi getiri elde ettik. Bakalım yarın tavanı verecek mi:)"
- Belirsiz: "tavan aldık 2 tane de iyi getiri" iki okunur: bir tavan + iki iyi getiri ya da iki tavan + iyi getiri. METRO için iki okuma var: grafikte tepki 24 Mart, metinde tarama 25 Mart; tarama tepkiyi ertesi gün raporlamış olabilir veya tarihler uyuşmuyor olabilir. Hisseye özgü eşik seçimi ve Sharpe hesap ayrıntıları verilmemiş.
- YORUM: Önceki < eşik < son ilişkisi iki örnekte doğrulanır; bütün hisseler için tek eşik veya eksiksiz tarama formülü değildir.

### X602 · 2026-09-04 17:11:54 UTC · Fon katkı tahmini, akış sıralaması ve risk radarı
- Bağlı: yeni yöntem; Öneri: tema-5b #2
- Yazar: T (kısa paylaşım ve sonuç cümleleri) + M (uzun fon/risk açıklamaları; PPF metni açıkça "ChatGPT dilinde") + G (tablolar).
- Kaynak: 2095922815329263677 (2026-09-04 17:11:54 UTC), 2096343856476496081 (2026-09-05 21:04:58 UTC), 2097060991586447371 (2026-09-07 20:34:36 UTC), 2097065200687915032 (2026-09-07 20:51:20 UTC), 2097551651838034055 (2026-09-09 05:04:19 UTC), 2099814980212134159 (2026-09-15 10:57:58 UTC), 2099970636386812395 (2026-09-15 21:16:29 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "TAHMİNİ FON GETİRİSİ — HİSSE PORTFÖYÜ KATKISI" — güncel tahmini hisse ağırlığı × günlük getiri, katkıların toplamı; DOH V4 ayrıca VİOP katkısı ve reconciliation katsayısı içerir — çekirdek belli.
  - [tarama-evren; G] "20 Günlük En Güçlü Para Giriş / Çıkışları" — 20 günlük akış sıralaması; seçim eşiği yok — çekirdek belli.
  - [boyut-risk; M] "fon için 0–100 arasında bir risk skoru üretmek" — para akışı 5G/20G, AUM, yoğunlaşma, likit tampon ve VİOP/türev riski; genel risk düşük olsa da yoğunlaşma 85/100 kritik örneği; ağırlık/formül yok — yalnız fikir.
  - [boyut-risk; M] "Fonun yüzde 5’i, yüzde 10’u veya yüzde 20’si çıkış yaparsa portföyün tasfiyesi kaç gün sürebilir?" — hacme göre tasfiye süresi planı — yalnız fikir.
  - [boyut-risk; M] "Tek bir ters repo işlemine, tek bir pay senedi teminatına veya tek bir karşı tarafa aşırı yüklenmesini istemem." — PPF'de çeşitlendirme ve likit/kamu kâğıdı tamponu; sayısal sınır yok — çekirdek belli.
  - [ölçüm-ilkesi; T] "bu model geçmişte satış yönünü yüzde kaç doğru yakaladı diye bir güven skoru üretsek" — fon çıkışının hisse satış baskısıyla geçmiş KAP raporlarında karşılaştırılması planı; model ve örnek sonuç yok — yalnız fikir.
- Örnek ve sonuç: görselden: THF büyüklük ₺92.90 Mr, KAP 08/2026 hisse %97.79, TEFAS brüt hisse %84.57; ANELE %4.70 × %5.29 → +%0.249; KARCL %6.48 × −%4.38 → −%0.284; toplam tahmin +%1.05. DOH hisse +%1.49, VİOP +%0.05, toplam +%1.54; reconciliation 0.7789, TEFAS/KAP oranları %69.13/%88.75. 4 Eylül tabloda THF 20G akış ₺75.71 Mr; grafik ekseni Milyon TL, en büyük çıkış GAL. Tansu THF beklentisinin gerçekleşmediğini, DOH beklentisinin nokta atışı olduğunu söyler; gerçekleşmiş fon getiri oranları yok.
- Tansu'nun vurgusu: "#THF kantitatif getiri beklentimiz maalesef gerçekleşmedi."; "#DOH fon getiri beklentimiz nokta atışı. Maşallah)"
- Belirsiz: 2097551651838034055 risk skoru metni birinci şahıstır ("üzerinde çalıştığım… ekleyeceğim"); M etiketi düşük güvenlidir. Açık "ChatGPT dilinde" ifadesi yalnız 2099814980212134159'dadır. Görselde ağırlıklar "Güncel tahmini ağırlık"; iki okuma, ham KAP ağırlığının kullanılması veya güncel dağılıma göre uzlaştırılmış ağırlık kullanılması. DOH katsayısı gösterilir, hisse bazında dönüşüm formülü gösterilmez. M metnindeki risk planları bitmiş puanlama sonucu sayılmaz.
- YORUM: Erken fon birikimi/pozisyon artışı kısmı X006'da bulunduğundan burada tekrar kayıt yapılmadı. THF'nin başarısız tahmini saklanmadı; +%1.05 gerçekleşmiş getiri değildir.

### X603 · 2025-11-10 17:38:59 UTC · PRKAB fincan hedefinin aritmetiği
- Bağlı: R114; Öneri: tema-5b #3
- Yazar: T + G (PRKAB formasyon çıktısı).
- Kaynak: 1987938049582391791 (2025-11-10 17:38:59 UTC).
- Fikirler:
  - [hedef-çıkış; G] "KIRILMA: 33.70"; "HEDEF: 42.90" — dip 24.50; 33.70 + (33.70 − 24.50) = 42.90 — çekirdek belli (örnekten çıkarılan hesap).
- Örnek ve sonuç: görselden: Fibo dip 24.50, sağ yüksek 39.64; tamamlanma 2025-10-27, sinyal 2025-11-03; son mumlar 42.90 hedef çizgisine ulaşmış. Metin hedefe geldi ve %4,43 der. Turuncu kulp eğrisi yaklaşık 2 TL'ye inerken fiyat mumları o seviyede değildir.
- Tansu'nun vurgusu: "Hedefe geldi."
- Belirsiz: %4,43 için iki okuma, gönderi gününün fiyat değişimi veya sinyal sonrası getiri; başlangıç fiyatı yazılmadığından ayrıştırılamaz. Kulp eğrisi fiyatın izlediği yol veya yalnız dekoratif formasyon eğrisi olabilir; mumlarla uyuşmadığı açıktır.
- YORUM: Aynı aritmetik R114'te 300.75 + (300.75 − 212.20) = 389.30 verir; açık soruya iki örnekle destek sağlar. Kaynak genel hedef formülünü yazmadığından "kural tam" yapılmadı; sağ ağızdan hesaplanan derinlik ile kırılım-dip farkı aynı değildir.

### X604 · 2025-10-31 19:58:12 UTC · UFUK derin Wave 2 ve Wave 3 hedefi
- Bağlı: R199; Öneri: tema-5b #4
- Yazar: T + G (Elliott araç çıktısı ve fiyat grafiği).
- Kaynak: 1984349202730926414 (2025-10-31 19:58:12 UTC).
- Fikirler:
  - [formasyon; G] "Impulse (Start-1): +50.8% | 2. Dalga Düzeltmesi: -31.2% | 3. Dalga Hedef: 1557.96 TL" — tepeden %31.2 düşüş, ilk dalga boyunun yaklaşık %92.5 geri alınması; hedef etiketi W1×1.618 — çekirdek belli.
- Örnek ve sonuç: görselden: START yaklaşık 838, 1 yaklaşık 1263, 2 yaklaşık 869.5; 869.5 + (1263 − 838) × 1.618 yaklaşık 1557 TL ve gösterilen 1557.96 ile yuvarlama düzeyinde uyumlu. İkinci görsel 10.10.2025 kapanışını 869.50 gösterir; ardından fiyat yaklaşık 2000–2050'ye gider. Tansu sonucu "%150 falan" diye yuvarlar; bu bir alım-satım kaydı değildir.
- Tansu'nun vurgusu: "Bu kardeş %150 falan yapmış:D"
- Çelişir: R199 — M karttaki maksimum %78.6 geri çekilme, bu araç örneğinde uygulanmış değildir; Tansu'nun gönderdiği kendi çıktı örneği güçlü kanıttır.
- YORUM: %31.2 ile %92.5 farklı paydalı ölçülerdir; aynı düzeltme oranı diye değiştirilemez. Grafiğin yaklaşık değerleri tam pivot fiyatları sayılmaz.

### X605 · 2025-07-05 22:11:31 UTC · Çift sistemlerinde farklı kapanışlar ve rotasyon sonucu
- Bağlı: R101 / R099 / R251; Öneri: tema-5b #5
- Yazar: T + G (işlem logları, çift tabloları ve performans grafiği).
- Kaynak: 1941620987495080092 (2025-07-05 22:11:31 UTC), 2021285630047559764 (2026-02-10 18:10:22 UTC), 2022010682791883042 (2026-02-12 18:11:28 UTC), 2049470417522348366 (2026-04-29 12:46:39 UTC), 2052182649100263830 (2026-05-07 00:24:05 UTC).
- Fikirler:
  - [hedef-çıkış; G] "Pozisyon kapatıldı" — SAHOL/THYAO tablosunda −1.93969, −1.93798 ve +1.956796 değerlerinde kapanış; ±2 bandının içinde gözlenen çıkışlar — çekirdek belli.
  - [hedef-çıkış; G] "POZİSYON KAPAT (Nakit)" — GSDDE/ALBRK logunda Z=0.45 ve 0.39 — çekirdek belli.
  - [hedef-çıkış; G] "Exit Position"; "Hold" — başka taramada çıkış −0.136805542, +0.125810008, +0.189848708; Hold +1.13637874, +0.7572027, +0.843287143, −0.500791756. AYES/GEREL Hold +1.800103256 ve +0.659055565 — çekirdek belli.
  - [portföy; G] "HISSE GECIS (ROTASYON) LOGU" — nakit → KRDMD, KRDMD → ISDMR, ISDMR → KRDMD; aynı anda iki bacak değil, tek hisse değişimi — çekirdek belli.
- Örnek ve sonuç: görselden: GSDDE/ALBRK 100,000 TL → 120,550.51 TL, +%20.55; Buy & Hold +%41.94, toplam sinyal/işlem 5, açık pozisyon var. Tansu "Gerçi işlem alınmadı" der. KRDMD/ISDMR grafiği net +61,290 TL (+%61.3), log üç geçiş gösterir; Tansu %62 diye yuvarlar. GEREL'de Tansu 3 Şubat girişini ve hâlâ tuttuğunu bildirir; fiyat görseli yaklaşık 16→26.
- Tansu'nun vurgusu: "Ben demiyorum istatistiksel arbitraj diyor."; "Gerçi işlem alınmadı"
- Belirsiz: SAHOL/THYAO'da iki okuma, banda geri girişin çıkış olması veya başka koşulla o değerlerde kapanış; yalnız log evrensel eşiği kanıtlamaz. Şubat çıkışları |Z|≤0.19 ile uyumludur ama gerçek kod eşiği 0.19 veya daha geniş bir sınır olabilir. KRDMD örneğinin R251 ile ortak yöntemi rotasyondur; tam aynı sürüm olduğu gösterilmemiştir.
- YORUM: Kapanış logları R101/R099'daki yaklaşık 0.5 anlatımına tek sürüm diye birleştirilmedi. Net performans açık pozisyon değerlemesini içerebilir; canlı gerçekleşmiş getiri diye yazılmadı. R251 başka çiftin örneğidir; KRDMD sonucu yeni örnek olarak alındı.

### X606 · 2025-03-06 08:28:47 UTC · Stochastic 14/3 durum taraması
- Bağlı: yeni yöntem; Öneri: tema-5b #6
- Yazar: T + G (kod ve tablo).
- Kaynak: 1897565005811183722 (2025-03-06 08:28:47 UTC).
- Fikirler:
  - [teyit-tetik; G] "periods = 14"; "moving_av = 3" — K = 100×(Close−LLV14 Low)/(HHV14 High−LLV14 Low); D = K'nın 3 dönem basit ortalaması — kural tam (hesap).
  - [giriş/çıkış; G] "Güçlü AL"; "Güçlü SAT" — sırayla K>D ve K<20 → Güçlü AL; diğer K>D → AL; K<D ve K>80 → Güçlü SAT; kalan her durum → SAT — kural tam (kod koşulları).
- Örnek ve sonuç: görselden: veri başlangıcı 2022-01-01, bitiş parametresi 2025-03-05; AEFES K=88.271640/D=78.836666 AL, AKENR 17.010309/11.635244 Güçlü AL. Kod sabit bir hisse listesi tarar; sonradan işlem/getiri sonucu yok.
- Tansu'nun vurgusu: "Şöyle bir stoc kodu taraması verelim"
- YORUM: Kod K/D seviyelerini karşılaştırır; önceki gün şartı olmadığı için "son gün kesişim" kuralı değildir. Eşitlik ve düşük K ile K<D de son else üzerinden SAT'a gider.

### X607 · 2025-04-11 15:56:13 UTC · FRAMA adıyla paylaşılan 16 dönemlik kesişim kodu
- Bağlı: yeni yöntem; Öneri: tema-5b #7
- Yazar: T + G (kod ve kesişim grafiği).
- Kaynak: 1910723570654753121 (2025-04-11 15:56:13 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "def calculate_frama_signals(data, period=16):" — N3=(HHV16−LLV16)/16; N1=(HHV8−LLV8)/8; N2 önceki 8 barın aynı aralığı; D=log((N1+N2)/N3)/log(2); alpha=exp(−4.6×(D−1)), 0.01–1 aralığına kırpılır — kural tam (yazılı hesap).
  - [teyit-tetik; G] "data['Close'].shift(1)" — çıktı alpha×(High+Low)/2 + (1−alpha)×önceki Close; Close yukarı keserse AL, aşağı keserse SAT; önceki karşılaştırmada eşitlik dahil — kural tam (paylaşılan varyant).
- Örnek ve sonuç: görselden: XU100.IS, veri 2025-01-01–2025-04-12 parametreleri; fiyat ve FRAMA çizgileri üzerinde AL/SAT işaretleri var. Performans ölçümü yok.
- Tansu'nun vurgusu: "Buyurun geliştirin."
- YORUM: Kod önceki FRAMA'yı kullanmaz; bu nedenle özyinelemeli FRAMA diye kaydedilmedi. Öneri belgesindeki sinyal sıklığı artışı iddiası ölçülmüş sonuç değildir. Buradaki kural tam etiketi kodun yazılı hesabına aittir; kod çalıştırılmadı.

### X608 · 2025-12-16 22:43:07 UTC · PRZMA Kelebek hedefleri ve D altı stop
- Bağlı: R203; Öneri: tema-5b #9
- Yazar: T + G (Kelebek grafiği).
- Kaynak: 2001060547618300157 (2025-12-16 22:43:07 UTC; kendi gönderisi 1998859904845766784'ü alıntılar).
- Fikirler:
  - [hedef-çıkış; G] "TP1: 12.43"; "TP2: 12.71"; "TP3 (C): 13.18"; "TP4 (Ext): 13.51" — CD geri çekilme/uzatma örneği; yaklaşık D=11.97 ile 0.382/0.618/1.272 oranları uyumlu — çekirdek belli.
  - [stop-geçersizlik; G] "STOP: 11.78" — bu örnekte stop D'nin altında, X'in altında değil — çekirdek belli.
- Örnek ve sonuç: görselden: PRZMA.IS, son fiyat hareketi TP4 çizgisine kadar ulaşır. Metin %13 der; giriş/çıkış fişi yok. R203'ün BALAT hedefleriyle aynı rakamlar değildir.
- Tansu'nun vurgusu: "Tamda hedeflere ulaşmış"
- YORUM: Stop konumu R203'ün M metnindeki X altı anlatımından farklıdır; formasyona/araç sürümüne göre farklı stop olabilir, genel stop formülü bu görselde yok.

### X609 · 2024-05-13 13:14:52 UTC · OTT 30/7 ve Supertrend hesap ayarları
- Bağlı: yeni yöntem; Öneri: tema-5b #10
- Yazar: T + G (kod görselleri); 10/3–3/10 fikir kökeni A (@mehmetemanet), Tansu kendi taramasında parametre değiştirdiğini söyler.
- Kaynak: 1790007806801621475 (2024-05-13 13:14:52 UTC), 1839989044693922032 (2024-09-28 11:22:28 UTC), 1860416194953543908 (2024-11-23 20:12:40 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "OTT Period"; "OTT Percent" — Pine v5, close, period=30, percent=7.0; MAVG=f_var(source,length); fark=MAVG×percent×0.01; yönlü longStop/shortStop; OTT=MT×(200±percent)/200; çıktı nz(OTT[2]) — çekirdek belli (f_var eksik).
  - [ölçüm-ilkesi; G] "range_period = 7"; "multiplier = 3" — ATR True Range üzerinde ewm(com=range_period); temel bant (High+Low)/2 ± multiplier×ATR; son bant ve trend döngüsü — çekirdek belli (görünen hesap; tam giriş/çıkış sistemi değil).
  - [teyit-tetik; A] 10/3 AL, 3/10 "at", RSI>55 AL, RSI<45 SAT — @mehmetemanet'in stratejisi (A) — yalnız fikir.
  - [teyit-tetik; T] "Bende bu tarama vardı parametreleri değiştirdim abi." — Tansu'nun benzer taraması var; hangi parametreleri değiştirdiği yazılı değil — yalnız fikir.
- Örnek ve sonuç: Kod ayarları görselden okunur; getiri tablosu yok. OTT paylaşımında Tansu etkinliğini bilmediğini söyler.
- Tansu'nun vurgusu: "Etkili olup olmadığını bilemiyorum. Kullananlar sonucunu yazarsa diğerleri de faydalanabilir."
- Belirsiz: "3/10 at" için iki okuma, SAT parametre çifti veya yazım hatası; aynen korunur, otomatik düzeltilmez. Uyarlamada hangi ayarların değiştirildiği listelenmez.
- YORUM: 1852011542746714531 kod değil, dış kaynaklı EMA5/20 + Supertrend infografiğidir; o görselin koşulları Tansu'nun kodu olarak alınmadı. X024'ün parametresiz Supertrend/MOST/KAMA taramaları tekrarlanmadı.

### X610 · 2025-09-21 15:43:46 UTC · DEY paydaları ve kapanış getirisi ayrımı
- Bağlı: R074; Öneri: tema-5b #11
- Yazar: T + G (hisse ve portföy tabloları).
- Kaynak: 1969789658574868800 (2025-09-21 15:43:46 UTC), 1983980494435033216 (2025-10-30 19:33:05 UTC), 2011852408222081449 (2026-01-15 17:26:07 UTC), 2015501247105642834 (2026-01-25 19:05:18 UTC), 2061548118592647615 (2026-06-01 20:39:07 UTC), 2061554188832702624 (2026-06-01 21:03:15 UTC).
- Fikirler:
  - [ölçüm-ilkesi; T] "Toplam% altında 19 Eylül itibari ile getirisi var, DEY% altında ise hissenin yarattığı marj." — Toplam%=100×(bitiş/referans−1), DEY%=100×(dönem en yüksek/referans−1); formüller tablo sayılarıyla uyumlu — çekirdek belli.
  - [ölçüm-ilkesi; G] "Başlangıç Açılış → Bitiş Kapanış arası en yüksek değere göre"; "ÖNCEKİ GÜN KAPANIŞINA GÖRE" — farklı tablolar farklı referans kullanır; Ekim tablosunda Başlangıç_Kapanis — kural tam (tablo referansları).
- Örnek ve sonuç: görselden: TUKAS başlangıç 4.14, bitiş 3.50, toplam −%15.46, dönem max 4.30, DEY %3.86. AZTEK 42.04 başlangıç kapanış/65.45 dönem yüksek → %55.69. ULKER 122.30 başlangıç açılış/132.40 yüksek → %8.26. INTEM önceki kapanış referansı 277.25/337.00 yüksek → %21.55. 20 Mayıs–1 Haziran portföy tablosu MV kapanış %15.02/DEY %23.69, MS %8.66/%18.37, BIST100 −%2.20.
- Tansu'nun vurgusu: "Nerede satacağınızı bilmezseniz Tukas örneğinde olduğu gibi -7 yersiniz."
- Belirsiz: Portföy grafiğinde DEY "Kümülatif En Yüksek", tabloda "En Yüksekte Satsaydım" ve ağırlıklı hisse marjları; iki okuma, portföyün tek ortak tarihteki zirvesi veya hisselerin ayrı tarihlerdeki zirvelerinin toplamı. İkincisi tabloda mümkün görünür; ikisini tek gerçekleşmiş portföy getirisi saymak desteklenmez.
- YORUM: R074'te dönem zaten 07.10 düzeltmesiyle 20 Mayıs–1 Haziran yazılıdır; aynı dönem düzeltmesi yeniden yapılmadı. Tablo id'si 2061548118592647615, grafik id'si 2061554188832702624; öneri belgesindeki tablo atfı ayrıldı. Tansu'nun "-7" uyarısı, tabloda TUKAS toplam −%15.46 değerinin yerine geçirilmedi.

### X611 · 2024-09-30 15:07:47 UTC · WMA varyantı ve CMF periyodunun kanıt sınırı
- Bağlı: R137 / R131; Öneri: tema-5b #12
- Yazar: T (WMA/RSI uyarlaması) + G (gösterge grafikleri ve otomatik mesajlar); 5/14/34/55 stratejisinin kökeni @fiboborsa.
- Kaynak: 1840770526240784672 (2024-09-30 15:07:47 UTC), 1845444032509468723 (2024-10-13 12:38:38 UTC), 1845558544126366115 (2024-10-13 20:13:40 UTC), 1847735111942336850 (2024-10-19 20:22:34 UTC).
- Fikirler:
  - [teyit-tetik; T] "WMA olarak kodlayarak RSI14 > 50 ekledim." — WMA5/14/34/55 ile Tansu'nun RSI14>50 uyarlaması — çekirdek belli.
  - [ölçüm-ilkesi; G] "CMF OSCILLATOR (21)" — 13 Ekim gösterge görselinin periyodu 21 — çekirdek belli (bu görselin ayarı).
- Örnek ve sonuç: görselden: FADE grafiği WMA5/14/34/55; başlık RSI21>50, alt panel adı RSI14. 19 Ekim otomatik mesajında ICUGS ve SANFM EMA/RSI koşulunu sağlıyor; CMF altı günlük işaret dizisi eklenince liste boş.
- Tansu'nun vurgusu: "Bu kodu diğer stratejiler ile kullanırız."
- Belirsiz: RSI için iki okuma, başlık eski ve alt panel/metin doğru veya gerçek hesap RSI21 ve alt panel etiketi yanlış; kod yok. CMF için iki okuma, 21 periyodu aynı taramada kullanıldı veya yalnız tanıtım grafiğinin ayarı; tarama grafiği periyot yazmaz. CMF(21) bütün taramalara kesin parametre diye eklenmez.
- YORUM: Altı günlük CMF işaret kuralı X002'de, EMA/RSI koşulları X001'de var; burada aynı fikir yeniden kayıt yapılmadı. R137'nin aşama sırası bu kaynaklarla değiştirilmez.

### X612 · 2025-06-28 16:49:16 UTC · AKD konsantrasyonu ve sınıf eşikleri
- Bağlı: yeni yöntem; Öneri: tema-5b #13
- Yazar: T (kendi yöntem/plan cümleleri) + M (13 Eylül uzun açıklama gövdesi) + G (AKD tabloları).
- Kaynak: 1939003175484133714 (2025-06-28 16:49:16 UTC), 1964443262544232634 (2025-09-06 21:39:06 UTC), 1964450520560808209 (2025-09-06 22:07:56 UTC), 1964749763922038906 (2025-09-07 17:57:01 UTC), 1966795896651477361 (2025-09-13 09:27:37 UTC).
- Fikirler:
  - [tarama-evren; G] "TOP5%"; "TOP2%"; "TOP10%" — ilk N kurumun alıcı payının toplamı; ilk kurum %50+ ayrı liste — kural tam (çıktı sınıflaması).
  - [tarama-evren; G] "Çok Yüksek (%95+)" — ilk 5 sınıfları %95+, %90–95, %80–90, %70–80, %70 altı; ilk 2 sınıfları %80+, %70–80, %50–70, %50 altı — çekirdek belli (ara sınırların dahil oluşu yazmıyor).
  - [tarama-evren; T] "konsolodasyonda olan ve toplanan hisseler, 1 ay-son 2 hafta-son 1 hafta-son 2 gün gibi çok güçlü adaylar." — zaman pencereleri planı; dönemler arası toplama karşılaştırması — çekirdek belli.
- Örnek ve sonuç: görselden: RODRG 59.42+32.43=TOP2 %91.85, TOP5 %100.00; Matrix ekranı 22.08.2025, alıcı net toplam 623,543 lot, ilk iki kurum OSMANLI/PHILLIP. İlk kurum %50+ listesinde 79 hisse. Kategori sayıları 590 hisseye karşılık gelir. AGYO örneği 09–23 Mayıs, "10 gün boyunca yatay kanal" 6.17–6.26, değişim %1.46; ilk 5 alıcı net %87.32. Tansu ertesi gün tavan olduğunu söyler.
- Tansu'nun vurgusu: "Python ile AKD taramsı böyle yapılır."
- Belirsiz: 1964450520560808209'da aynı %59.42/%32.43 pay sütunlarının başlıkları DENIZ/QNB YAT, önceki Matrix görselinde OSMANLI/PHILLIP; iki okuma, başka tabloya yanlış sütun başlıkları taşınmış veya farklı kurum eşlemesi kullanılmış. Kurum isimleri bu çıktılar arasında birleştirilmez.
- YORUM: Alıcı net payı tüm alış-satış işlem hacmindeki pay değildir. Önceki alıcıların satıcıya geçmesiyle takipten çıkarma X004'teki kurum sürekliliği fikrini yineler; yeni kayıt burada konsantrasyon ölçümü ve sınıf eşikleridir. Kullanıcı tibetduman'ın yanıtı yöntem kanıtı alınmadı.

### X613 · 2024-09-25 20:46:46 UTC · RSI serisine Fibonacci ve dönüş taramaları
- Bağlı: yeni yöntem; Öneri: tema-5b #14
- Yazar: T + G (haftalık kod ve tarama görselleri).
- Kaynak: 1839043892399735295 (2024-09-25 20:46:46 UTC), 1861794132093554798 (2024-11-27 15:28:06 UTC), 1862203614174888388 (2024-11-28 18:35:14 UTC), 1912136481751056753 (2025-04-15 13:30:37 UTC), 1977423987274617023 (2025-10-12 17:19:51 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "data = data.resample('W').agg" — yfinance 1 yıl günlük veri, haftalığa OHLCV birleştirme; RSI14 kazanç/kayıp basit ortalama, min_periods=1; RSI maksimum/minimumundan H−(H−L)×0.236/0.382/0.5/0.618/0.786, 161.8% çizgisi L−(H−L)×0.618 — kural tam (hesap).
  - [teyit-tetik; T] "Fiyat>ema 89"; "Rsifibo>0.618" — günlük varyant; sonraki metinde 0.618'e yaklaşma ve tepki alma — çekirdek belli (yakınlık/tepki eşiği yok).
  - [teyit-tetik; T] "Dünkü Rsi’a çekilen 144 günlük Fibo 0.786 dip dönüş ve bullish mum  taraması sonuçları." — 144 günlük RSI aralığı, 0.786 dönüş ve boğa mumu; Ekim görselinde 0.618 dönüş — çekirdek belli.
- Örnek ve sonuç: görselden: Nisan listesinde MERKO +%9.95, TMPOL +%7.46, FRIGO +%1.45, KENT %0.00, ULKER −%1.61. Ekim EKOS RSI14 grafiği son 144 gün, 0.618 yaklaşık 44; CDLENGULFING/CDLBELTHOLD etiketleri, son gün 2025-10-06. Tansu "pazartesi gelen güzel tepki" der; oran yazmaz.
- Tansu'nun vurgusu: "Fibo 161,8 seviyesinde bir hisseyi haftalıkta yakalarsak tatlı bir şey olabilir."
- Belirsiz: "Rsifibo>0.618" için iki okuma, normalize RSI-Fibo oranı >0.618 veya RSI'nın hesaplanmış 0.618 çizgisinin üstünde olması; metin tek başına ayırmaz. Haftalık 161.8 hedefinin RSI 0–100 gösterim sınırıyla ilişkisi açıklanmıyor.
- YORUM: Haftalık kod çizim hesabıdır; otomatik yakınlık/giriş kuralı değil. 0.786 ile 0.618 ve günlük EMA89 varyantları tek zorunlu birleşik sisteme dönüştürülmedi.

### X614 · 2025-04-22 16:14:08 UTC · DuPont adımları ve temel-teknik aday filtresi
- Bağlı: R002; Öneri: tema-5b #15
- Yazar: M (Nisan/Mayıs uzun açıklamalar) + T (23 Temmuz kendi tarama anlatımı, 11 Ağustos kısa sonuç) + G (DuPont tablosu).
- Kaynak: 1914714348368359654 (2025-04-22 16:14:08 UTC), 1918035116988788982 (2025-05-01 20:09:41 UTC), 1948004722608140442 (2025-07-23 12:58:12 UTC), 1954935103194534196 (2025-08-11 15:57:04 UTC).
- Fikirler:
  - [temel-değerleme; M] "beklenen kâr üzerinden yaparsak" — son açıklanan bilanço yerine projeksiyonla DuPont planı — yalnız fikir.
  - [temel-değerleme; M] "net kâr marjı, aktif devir hızı, aktif kârlılık, borç/kaynak oranı ve özsermaye kârlılığı adım adım hesaplanacak." — beş oran ve sektör karşılaştırması — çekirdek belli.
  - [tarama-evren; T] "özsermaye karlılığı yüksek olupta ta fk 5-15 arasında olan ve 200 ema altında olanlar." — momentum listesi, yüksek Sharpe, rotasyonda ilk sektör, yüksek ROE, F/K 5–15, EMA200 altı; "yüksek" eşikleri yok — çekirdek belli.
- Örnek ve sonuç: görselden: TMSN 2025/3 net marj %77.15, aktif devir %44.53, aktif kârlılık %34.36, borç/kaynak %33.97, ROE %53.64. 77.15×0.4453 yaklaşık 34.36; 34.36/(1−0.3397) yaklaşık 52.04, gösterilen 53.64 ile uyuşmaz. Diğer şirketlerde 2025/6 da var; tablo dönemleri aynı değil. Hisse getiri sonucu yok.
- Tansu'nun vurgusu: "Asıl stratejim momentum ama temel ve teknik analizi beraber kullandığım taramalarım da var ve artık bu taramaları da vereceğim."
- Belirsiz: 1918035116988788982 kısa ilerleme duyurusudur ("Özsermaye kârlılığı adımını tamamladık"); M etiketi düşük güvenlidir, T olabilir. ROE için iki okuma, ortalama özsermaye gibi farklı payda/dönem kullanılmış olması veya hesap/veri hatası; görsel formül yazmadığından neden çözülemez. Beklenen kâr planı, Ağustos tablosunun gerçekten projeksiyon kullandığını kanıtlamaz.
- YORUM: Uyumsuz ROE sayısı sessizce düzeltilmedi ve tek formülün doğrulanmış çıktısı yapılmadı. M projeksiyon fikriyle Tansu'nun kendi sayısal filtresi ayrı tutuldu.

### X615 · 2024-10-30 22:17:21 UTC · Merton ters çözüm tablosu
- Bağlı: R061; Öneri: tema-5b #16
- Yazar: T + G (Excel modeli ve formüller).
- Kaynak: 1851750265239609482 (2024-10-30 22:17:21 UTC).
- Fikirler:
  - [temel-değerleme; G] "Objective Function"; "(E_est/3-1)^2 + (sigma_E/0.8-1)^2" — E0=A0N(d1)−D exp(−rT)N(d2); sigma_E=N(d1) sigma_A A0/E0; d1=[ln(A0/D)+(r+sigma_A²/2)T]/(sigma_A√T), d2=d1−sigma_A√T; A0/sigma_A'yı gözlenen E0/sigma_E'ye uydurma — kural tam (yazılı model).
  - [boyut-risk; G] "default probability (risk neutral)" — Pd=N(−d2); D0=A0N(−d1)+D exp(−rT)N(d2); PUT=D exp(−rT)N(−d2)−A0N(−d1) — kural tam (tablo formülleri).
- Örnek ve sonuç: görselden: E0=3, sigma_E=0.8, D=10, r=%5, T=1; A0=12.395, sigma_A=%21.23; amaç 1E−11; d1=1.3531/d2=1.1408; Pd=0.127, D0=9.3954, PV(D)=9.5123, EL=0.0123, LGD=0.0968. Tablonun model çözümüdür; gerçek şirket temerrüdü sonucu yok.
- Tansu'nun vurgusu: "Ve kredi risk proje taslağı."
- YORUM: R061 ileri hesap örneği; bu tablo özsermaye değeri/oynaklığından varlık parametrelerini bulur. Pd risk-nötr etiketlidir; gerçek dünya temerrüt olasılığı ile eşitlenmedi.

### X616 · 2024-09-26 19:39:14 UTC · Grid yüzde aralığı ve ATR stop taslağı
- Bağlı: yeni yöntem; Öneri: tema-5b #17
- Yazar: T + G (kod ve konsol çıktıları).
- Kaynak: 1839389286518723008 (2024-09-26 19:39:14 UTC), 1839747420302831898 (2024-09-27 19:22:20 UTC), 1943067673858052555 (2025-07-09 22:00:08 UTC).
- Fikirler:
  - [giriş/boyut-risk; G] "grid_size=0.4, position_size=50, atr_period=14, atr_multiplier=2"; "bot.create_grid(10)" — yüzde %0.4 aralık, 50 lot, 10 seviye; seviye j=0…9 için başlangıç×(1−0.4/100×j), fiyat≤seviye ise alış mesajı — kural tam (taslak hesabı).
  - [hedef-çıkış/stop; G] "sell_price = price * (1 + self.grid_size / 100)" — satış seviyesi grid alışının %0.4 üstü; stop=current_price−2×ATR14; ATR, True Range'in 14 dönem basit ortalaması; fiyat<stop ise kapanış mesajı — kural tam (kod).
- Örnek ve sonuç: görselden: 26 Eylül GUBRF 201.6999969482422 alış/202.50679693603516 satış planı, stop 186.28571428571428; TUPRS 170/170.68, stop 162.6142839704241. Temmuz çıktısı alış/satış tetik mesajları verir; stop farkı yaklaşık 7.6629. Bunlar konsol örnekleri, net getiri veya canlı emir fişi değil.
- Tansu'nun vurgusu: "Bu stratejiyi hiç kullanmadığım ve bir talep üzerine yazdığımdan çok detaya inmedim."; ayrıca "python ile yazdığım gridbot alım satım sonuçlarının bir kısmı" (1943067673858052555).
- Belirsiz: Temmuz stop için iki okuma, o veri kesitinde sabit ATR'den aynı fark veya ayrı sabit-fark sürümü; kod verilmediğinden ayrıştırılamaz.
- YORUM: %0.4, fiyat birimi olarak 0.4 değildir. Eylül kodu tek son fiyatı kontrol edip mesaj basar; portföy/pozisyon takibi ve gerçek emir bağlantısı göstermez. Önerideki "bot" adı çalışan canlı sistem kanıtı sayılmaz.

### X617 · 2024-08-25 19:46:11 UTC · Vegas stratejisinin DOAS al-tut karşılaştırması
- Bağlı: yeni yöntem (X010'un sonuç eki); Öneri: tema-5b #18
- Yazar: T.
- Kaynak: 1827794622434640093 (2024-08-25 19:46:11 UTC), 1844743398047064231 (2024-10-11 14:14:34 UTC).
- Fikirler:
  - [ölçüm-ilkesi] "2022-2024 yılları arasında vegas tüneli stratejisi doaş getirisine yenik düşmüştür." — EMA12/144/169 Vegas stratejisi için aynı hissede al-tut kıyası — çekirdek belli (sonuç bildirimi).
- Örnek ve sonuç: DOAS'ta 2022–2024 strateji al-tutun altında. DNISI için "tam gaz devam" bildirimi var; oran/işlem sonucu yok. Sayısal getiri katsayıları kayda alınmadı; metin yalnız kıyas yönünü doğrular.
- Tansu'nun vurgusu: "Elbette kullandığımız 12-144-169 günlük ema değerleri optimize edilebilir."
- YORUM: 1783135314036376019'daki giriş fikri ve 1838671862420975657'deki kesişim taraması X010'da bulunan yöntemi tekrarlar; burada yeni unsur başarısız al-tut kıyasıdır. DNISI'nin nitel olumlu sonucu DOAS kıyasını çürütmez.

### X618 · 2024-10-02 19:34:25 UTC · Hammer geometrisi ve iki kısmi satış örneği
- Bağlı: R143 / R224; Öneri: tema-5b #19
- Yazar: T + G (satış konsolu).
- Kaynak: 1841562402501869780 (2024-10-02 19:34:25 UTC), 1989777185264066973 (2025-11-15 19:27:03 UTC), 1989778002805170214 (2025-11-15 19:30:18 UTC).
- Fikirler:
  - [formasyon; T] "if lower_shadow >= 2 * body_size and upper_shadow <= body_size * 0.3" — alt gölge≥2×gövde, üst gölge≤0.3×gövde — kural tam.
  - [hedef-çıkış; G] "Pozisyonun %50'si satıldı (Kalan: %50)"; "Kalan pozisyonun %50'si satıldı (Kalan: %25)" — K1 ilk yarı, K2 kalan yarı; başlangıç pozisyonunun %25'i kalır — kural tam (oranlar).
- Örnek ve sonuç: görselden: K1 2025-07-07, satış 182.50, kazanç %10.61; K2 2025-08-20, satış 196.10, toplam kazanç %18.85; genel durum kalan %25. Bunlar satış anına kadar fiyat kazanç etiketleri; tüm portföyün realize getiri hesabı gösterilmez.
- Tansu'nun vurgusu: "Koşulum aşağıda"; "Henüz 1/10'u bitenn sistemden bir görüntü."
- Belirsiz: Kalan %25 için iki okuma, R224 benzeri iz süren stopla yönetilmesi veya başka çıkış kuralı; bu konsol son çıkışı yazmaz.
- YORUM: %10.61/%18.85 gözlenen satış anındaki değerlerdir, sabit K1/K2 tetik eşikleri değil. Hammer taraması ile kısmi satışın aynı sistemin bağlı parçaları olduğu gösterilmedi.

### X619 · 2026-04-18 08:00:38 UTC · Yatay pencere örnekleri ve basamaklı kanal işlemleri
- Bağlı: R246 / R004 / R245; Öneri: tema-5b #20
- Yazar: T + G (yatay bantlar, kanal logu ve backtest tablosu).
- Kaynak: 2045412174030352518 (2026-04-18 08:00:38 UTC), 2088957194892923386 (2026-08-16 11:53:00 UTC), 2091428244650147903 (2026-08-23 07:32:05 UTC), 2096379158561427848 (2026-09-05 23:25:14 UTC).
- Fikirler:
  - [tarama-evren; G] "34 hafta yatay (386.25 - 500.50)"; "30 hafta yatay (3.11 - 3.30)" — AYCES ve YKSLN araç örnekleri; yataylık algoritması yok — çekirdek belli.
  - [giriş/çıkış; G] "Close 52.95 < Alt 54.65"; "Close 65.30 > Üst 65.10" — alt kanal altında AL, üst kanal üstünde SAT — çekirdek belli (kanal hesabı yok).
- Örnek ve sonuç: görselden: 16 Ağustos backtesti 4 işlem/4 kazanan, %100 win rate, ortalama %13.00, bileşik %60.8; işlem getirileri %27.57, %10.35, %1.21, %12.86. Eylül başka kanal logu %23.3, %2.3, %19.4 ve 26.03.2026 açık AL gösterir. Tansu AYCES için 1 Eylül 399 TL→an itibarıyla 1232 TL, YKSLN için "1 ayda %30" der.
- Tansu'nun vurgusu: "Kaza ile bir trade stratejisi kodlamış olabilirim:)"
- Belirsiz: AYCES görselinin ekseni 2025 yazına kadar, YKSLN bant görseli 17.04.2026'ya kadar; iki okuma, eski tarama görselleri daha sonraki sonucu göstermek için eklenmiş veya metin/görsel yanlış eşleştirilmiş. Görseller metindeki sonuç dönemini tek başına doğrulamaz.
- YORUM: R246'nın 80–100 haftası bu 30/34 haftalık örneklerle değiştirilmedi. Yatay bant taraması, basamaklı kanal trade sistemi ve R245'in 120 bar yükselen kanal teması ayrı varyantlardır. 4/4 geriye dönük tablo, bütün hisselerde başarı oranı değildir.

### X620 · 2025-03-24 04:37:41 UTC · Temiz yüzde 10 alan ve çizgi uyum ölçüleri
- Bağlı: R192 / R124 / R039; Öneri: tema-5b #21
- Yazar: T + G (kanal, demand ve DÜK çıktıları).
- Kaynak: 1904029830036775278 (2025-03-24 04:37:41 UTC), 2003587326036127830 (2025-12-23 22:03:38 UTC), 2016214167884046802 (2026-01-27 18:18:11 UTC).
- Fikirler:
  - [tarama-evren; T] "talep bölgesini kırmış olacak ve üzerindeki en az %10'luk alanda herhangi bir bearish fvg ve arz alanı olmayacak:)" — kırılım üstünde en az %10 temiz alan — çekirdek belli (bölge tespit formülü yok).
  - [ölçüm-ilkesi; G] "Lookback: 90 gün"; "Eğim: -0.037773 (-2.16°)" — DÜK çıktı penceresi/eğimi — çekirdek belli.
  - [ölçüm-ilkesi; G] "Alt kanal R^2: 0.9982  Üst kanal R^2: 0.9393" — kanal doğrularının uyum ölçüsü; kabul eşiği yok — çekirdek belli.
- Örnek ve sonuç: görselden: Aralık A1CAP fiyat 11.57, +%10 çizgisi 12.73 ve "Temiz" etiketi; Ocak A1CAP fiyat 15.22, ilk temas 2025-10-31, kırılım 2026-01-27. Mart kanal grafiğinde kırılım işaretleri sonrası yükseliş; sembol ve getiri oranı yok. Aralık metni bu hareketin %10 verdiğini bildirir.
- Tansu'nun vurgusu: "DÜK önemlidir. :D"
- YORUM: R² bir olasılık/başarı oranı değildir. Üç farklı çıktı aynı taramanın zorunlu sıralı kapıları yapılmadı; Ocak 15.22 değeri Aralık %10 sonucunun işlem kapanışı sayılamaz.

### X621 · 2024-11-29 22:00:31 UTC · PSAR ve SMA20/40 trend teyidi
- Bağlı: yeni yöntem; Öneri: tema-5b #22
- Yazar: T + G (PSAR grafikleri).
- Kaynak: 1862617662196473882 (2024-11-29 22:00:31 UTC), 1862630588584214682 (2024-11-29 22:51:52 UTC), 1862635048819650793 (2024-11-29 23:09:36 UTC), 1864259354800578906 (2024-12-04 10:44:01 UTC), 1950999922742010108 (2025-07-31 19:20:04 UTC).
- Fikirler:
  - [teyit-tetik; T] "Yeni strateji, PSAR ve 20sma, 40sma"; "kesişim sonrasi ilk psar barında giriş yapıyoruz." — SMA20/40 trend teyidi ve kesişim sonrası ilk PSAR barı — çekirdek belli (SAR ayarları/teyit eşitsizliği yok).
  - [teyit-tetik; G] "ADX and ADXR"; "Average Volume (10 bars)" — SNGYO çıktısında Momentum, ADX/ADXR ve 10 bar hacim ortalaması panelleri — çekirdek belli (panel seti; giriş eşikleri yok).
- Örnek ve sonuç: görselden: ADESE fiyat/PSAR kesişim AL/SAT işaretleri; SNGYO çok panelli çıktı. Temmuz metni yükselen trend temas tarihlerinde SAR dip dönüşü gördüğünü ve trend koduna ekleyeceğini söyler. Net getiri/backtest sonucu verilmemiş.
- Tansu'nun vurgusu: "Bu sarları da python trend koduma ekleyeceğim."
- YORUM: Ek panel bulunması ADX/hacim için zorunlu giriş kapısını kanıtlamaz; PSAR step/maksimum parametresi uydurulmadı.

### X622 · 2024-10-14 15:32:37 UTC · Bollinger üç sapma mum dönüşü ve Keltner fikri
- Bağlı: R053 / R082; Öneri: tema-5b #23
- Yazar: T (3SS kuralı, Ağustos model notu) + M (Nisan başlıklı sıkışma anlatımı) + G (AKFGY göstergeleri).
- Kaynak: 1845850204395692110 (2024-10-14 15:32:37 UTC), 1913989895674028279 (2025-04-20 16:15:25 UTC), 1955389232639512999 (2025-08-12 22:01:37 UTC).
- Fikirler:
  - [teyit-tetik; T] "ÜSt banda yeşil mum ile temas edip ardından kırmızı mum kapatan hisseler ve alt banda kırmızı le temas edip ardından yeşil ile kapatan hisseleri arıyoruz." — BB 3 standart sapma, üstte yeşil temas/kırmızı kapanış, altta kırmızı temas/yeşil kapanış — çekirdek belli (BB periyodu ve temas toleransı yok).
  - [teyit-tetik; M] "Sıkışma → Patlama döngüsünü otomatik yakalayan bu mantık" — Bollinger–Keltner sıkışma/kırılım fikri, hacim/RSI/MACD ile destekleme önerisi — yalnız fikir.
- Örnek ve sonuç: görselden: AKFGY Fiyat+Bollinger+Keltner, son gün AL işareti; RSI, MACD, ADX/DI/ADXR panelleri. Tansu eski tarihli örnek olduğunu söyler; güncel sonuç veya ölçülmüş başarı yok.
- Tansu'nun vurgusu: "Hisse eski tarihlidir sakın referans almayın"
- YORUM: R082 konsolidasyon süresi gözlemi, bu Bollinger–Keltner hesabının aynısı olduğu kanıtı değildir. Mum sırasının AL/SAT yorumu üstte dönüş/altta dönüş mantığından gelir; metin emir talimatı yazmaz.

### X623 · 2025-07-24 07:22:49 UTC · Elliott son gün eşleşmesi ve FADE hedef etiketleri
- Bağlı: R207 / R261; Öneri: tema-5b #24
- Yazar: T + G (Elliott ve FADE araç çıktıları).
- Kaynak: 1948282706002903233 (2025-07-24 07:22:49 UTC), 1983796730740273257 (2025-10-30 07:22:52 UTC), 1984331550519910770 (2025-10-31 18:48:03 UTC), 2095607708200169599 (2026-09-03 20:19:46 UTC).
- Fikirler:
  - [tarama-evren; G] "SADECE EN SON GÜNDE TAMAMLANAN (C NOKTASI) EŞLEŞMELER" — A1CAP itki bitişi 2025-07-03, düzeltme bitişi 2025-07-23; son gün eşleşme filtresi — çekirdek belli (pivot tespiti yok).
  - [ölçüm-ilkesi; G] "Impulse #1: +66.8% | Corrective: -10.5%"; "Impulse #1: +36.7% | Corrective: -14.8%" — TATEN ve IPEKE itki/düzeltme çıktı ölçüleri — çekirdek belli.
  - [hedef-çıkış; G] "HEDEF 1 17.82"; "HEDEF 2 16.65"; "HEDEF 3 19.72" — FADE Elliott giriş düzeyi 16.55, demand 14.77–14.91 ve yeni kırılan dört temaslı düşen trend — yalnız fikir (hedef formülü yok).
- Örnek ve sonuç: A1CAP için Tansu ilk tavanı bildirir; görsel C diye etiketlediği nokta B sonrasında toparlanma tepesidir. 1983796730740273257 metni "Güncellenmiş elliot taramamız %3.30 ile devam ediyor" der (hisse belirtilmez; TATEN görseli +66.8% / −10.5%); IPEKE metni tavan der; IPEKE henüz deneme ve gruba verilmemiştir. FADE ikinci görsel yüksek 19.75; hedef 3 üstüne çıkılmış, kapanış 18.80. Girişten yüksek fiyata yaklaşık %19.3 marj; gerçekleşmiş satış kanıtı değil.
- Tansu'nun vurgusu: "Gerçi bunu gruba da vermemiştim henüz hala deneme süreçlerinde."
- Belirsiz: A1CAP C için iki okuma, aracın standart dışı ABC etiketlemesi veya etiketleme hatası. FADE hedef 2 hedef 1'in altında; farklı hedef aileleri veya sıralama hatası olabilir, kaynak çözmez.
- YORUM: Öneri belgesinin A1CAP düzeltme bitişi 21 Temmuz okuması 23 Temmuz olarak düzeltildi. R207 dış Notebook LM görseli kaynak kuralı olarak kullanılmadı; R261'in demand örtüşmesi ile FADE'nin hedef hesabı aynı sayılmadı.

### X624 · 2025-04-21 04:25:33 UTC · Kanal orta noktasıyla breakout izleme
- Bağlı: yeni yöntem; Öneri: tema-5b #25
- Yazar: T + G (orta nokta grafikleri).
- Kaynak: 1914173637898236379 (2025-04-21 04:25:33 UTC), 1914210602513236459 (2025-04-21 06:52:26 UTC), 1917567412125274471 (2025-04-30 13:11:12 UTC).
- Fikirler:
  - [teyit-tetik; G] "Kanal Orta Noktası" — fiyatın orta çizgi civarından yukarı kalkması/kırılımı; çizgi hesabı, pencere ve kesin giriş yok — çekirdek belli.
- Örnek ve sonuç: görselden: ilk iki örnekte orta çizgi ve fiyat yükselişi; FORMT çıktısında orta çizgi, CDLCLOSINGMARUBOZU/CDLHIKKAKE, RSI14/EMA10, MACD, ADX/DI, Stochastic panelleri. Tansu FORMT'te aksiyon alınmadığını söyler; oranlı getiri veya işlem fişi yok.
- Tansu'nun vurgusu: "Yeni sistemim tam bir trend breakout ve takip sistemi."
- YORUM: Orta noktanın (üst+alt)/2 veya başka hesap olduğu gösterilmedi. Panel isimleri ayrı zorunlu teyit koşulları yapılmadı.

### X625 · 2024-10-20 10:06:35 UTC · CDL etiketleri, adsız üç mum kodu ve Tasuki Gap
- Bağlı: R143; Öneri: tema-5b #26
- Yazar: T + G (formasyon etiketli grafik ve kod).
- Kaynak: 1847942480169222236 (2024-10-20 10:06:35 UTC), 1899964404872941880 (2025-03-12 23:23:08 UTC), 1910750627728175106 (2025-04-11 17:43:44 UTC).
- Fikirler:
  - [formasyon; G] "CDL3OUTSIDE"; "CDLSHORTLINE"; "CDLDOJI"; "CDLHARAMI"; "CDL3INSIDE" — XU100 grafiğinde, ayrıca engulfing/belthold/closingmarubozu etiketleri; günlük sonu Telegram'a gönderme planı — çekirdek belli (ad/çıktı var, hesap yok).
  - [formasyon; G] "data.at[data.index[i + 1], 'buy_signal'] = 1" — C[i]>O[i], C[i]<O[i−1], C[i]>C[i−1], O[i]<C[i−1], önceki iki mum kırmızı → sonraki bara AL işareti — kural tam (görünen kod parçası).
  - [teyit-tetik; T] "Uyuşmazlığın yanında Tasuki Gap mum formasyonu sinyali de geldi.Bu bir bir boğa devam formasyonudur." — uyuşmazlıkla Tasuki Gap birlikteliği — çekirdek belli (Tasuki Gap geometrisi yok).
- Örnek ve sonuç: Tansu BINHO'nun o gün %8'e yakın marj verdiğini bildirir. Adsız kod ve XU100 CDL grafiği ayrı kaynaklardır; BINHO işleminin kodu olduğu gösterilmez.
- Tansu'nun vurgusu: "Buyurun size bir mum formasyonu tanımlama kodu:) Aklıma geldikçe yazıyorum."
- YORUM: Adsız kodun üç mum şartı birebir alındı; "delici mum" adı kaynakta olmadığı için eklenmedi. Giriş i+1'de işaretlenir; o barın açılışında gerçekleşmiş emir değildir.

### X626 · 2024-06-02 13:46:38 UTC · Portföy kontrolleri ve risk/getiri sıralaması
- Bağlı: R110 (R137 bağı zayıf); Öneri: tema-5b #27
- Yazar: T + G (risk/getiri listesi ve fiyat grafiği).
- Kaynak: 1797263557978890521 (2024-06-02 13:46:38 UTC), 1821204747614831017 (2024-08-07 15:20:22 UTC), 1908666927045886118 (2025-04-05 23:43:51 UTC), 1985453771279757653 (2025-11-03 21:07:21 UTC).
- Fikirler:
  - [portföy; T] "Bist30 da son 1 yılda momentumu en yüksek şirketleri bulup, markowitz ve black litterman kullanacağız" — BIST30/son bir yıl momentum planı; ağırlıklar yok — yalnız fikir.
  - [ölçüm-ilkesi; T] "varyans Kovaryans matrisi ya da Vif ile konuyu aydınlatacağız" — Markowitz portföyünde çoklu doğrusal bağlantı kontrolü; VIF sınırı yok — yalnız fikir.
  - [tarama-evren; T] "Level 1 dip-tepe algoritmasında profit factor > 3 hisseleri bul" — sonra dip sinyali taraması ve PNL denemeleri; Level 1 algoritması tanımsız — çekirdek belli.
  - [tarama-evren; G] "Return_Risk_Ratio" — YÜZDE/(Risk_Score+1) ile örnek aritmetik uyumu; risk skoru formülü yok — çekirdek belli.
- Örnek ve sonuç: görselden: DUNYH son 121.10, YÜZDE=9.89, Risk_Score=99.153329, oran=0.098749; 9.89/100.153329 ile uyumlu. Fiyat grafiğinde 28.10.2025 kapanış 121.10, sonraki yüksek yaklaşık 145. Emir/satış sonucu yok.
- Tansu'nun vurgusu: "Kendime not"
- YORUM: Return_Risk_Ratio'nun bölme formülü kaynakta yazılı değil, sayıların uyumundan çıkarımdır. Black-Litterman adı X023'te var; burada yeni unsur BIST30/bir yıl evren planı ve ayrı kontrol/sıralama fikirleridir. Dört madde tek zorunlu portföy akışı değildir.

### X627 · 2025-04-12 18:38:36 UTC · Ölçü değişimi kodu ve iki model planı
- Bağlı: yeni yöntem; Öneri: tema-5b #28
- Yazar: T (kod paylaşımı; 1911703064748216597 piyasa yapıcı planı birinci şahıs: "mimarisini kafamda yazdım") + M (1911126825217982630 ölçü değişimi, 1913122317263057042 MB botu) + G (kod/grafik).
- Kaynak: 1911126825217982630 (2025-04-12 18:38:36 UTC), 1911126829710073960 (2025-04-12 18:38:37 UTC), 1911703064748216597 (2025-04-14 08:48:23 UTC), 1913122317263057042 (2025-04-18 06:47:59 UTC).
- Fikirler:
  - [ölçüm-ilkesi; G] "mu_q = 0" — AKBNK.IS, 2018-01-01–2024-01-01 aylık veri, yıllık son kapanıştan log getiri; normal P yoğunluğu, xi=exp(−(mu_p−mu_q)×x+(mu_p²−mu_q²)/(2×sigma_p²)); Q=xi×P ve trapz ile normalizasyon — çekirdek belli (paylaşılan modelin doğruluğu doğrulanmadı).
  - [diğer; T] "Avellaneda-Stoikov Modeli üzerine kurulu bir likidite sağlayıcı (market-maker) davranışını inceleyerek yapacağız." — spread, kâr, pozisyon, risk ve Sharpe simülasyonu; canlı veri eksik — yalnız fikir.
  - [diğer; M] "haber akışını ekonomik verilerle bağlayan bir “faiz tahmin botu” geliştirilebilir." — zaman serisi + NLP; ARIMA/XGBoost/LSTM ve sentiment/topic/stance; PPK öncesi güncelleme planı — yalnız fikir.
- Örnek ve sonuç: görselden: AKBNK P ve Q yoğunluk grafiği; Q tepe noktası sıfırda değil yaklaşık +0.4 çevresinde. Diğer iki plan için ölçülmüş çıktı yok.
- Tansu'nun vurgusu: "Aşağıda da bu sistematiğin kodunu paylaşıyorum."
- Belirsiz: Kod/grafik için iki okuma, gerçek bir risk-nötr dönüşüm amaçlanmış ama formül eksik veya farklı ağırlıklandırma gösterimi yanlış adlandırılmış. Kodda mu_q=0 iken çizilen Q'nun tepesinin sıfırda olmaması açıklanmıyor; doğru opsiyon fiyatlama modeli sayılmaz.
- YORUM: MB botunun uzun M gövdesi Tansu'nun doğrulanmış çalışan modeli değildir. Kodun xi ifadesi öneri metnindeki gibi aynen kaydedildi; matematiksel doğruluk ya da çalışma hükmü verilmedi.

### X628 · 2024-10-02 21:53:28 UTC · ROC50 teyidi, Stoch RSI ve Mavilim örnekleri
- Bağlı: yeni yöntem; Öneri: tema-5b #29
- Yazar: T + G (gösterge grafikleri).
- Kaynak: 1841597392178536580 (2024-10-02 21:53:28 UTC), 1853470102810669319 (2024-11-04 16:11:22 UTC), 1943066690709070008 (2025-07-09 21:56:14 UTC).
- Fikirler:
  - [teyit-tetik; T] "ROC50 > 0"; "ADX > ADRX"; "OBV artan" — ROC50 pozitif, ADX/ADXR karşılaştırması ve yükselen OBV — çekirdek belli (OBV artış penceresi yok).
  - [teyit-tetik; T] "fiyat 9ema ve stocRSI" — gün içi EMA9/Stoch RSI fikri; görsel K/D ve 20/80 referansları — çekirdek belli (kesin tetik/periyot yok).
  - [teyit-tetik; G] "Fiyat ve MAVİLİMW Kesişimleri (Plotly)"; "MAVİLİMW (M7)" — fiyat/çizgi kesişiminde AL/SAT işaretleri; formül/ayar yok — çekirdek belli.
- Örnek ve sonuç: görselden: ROC 50 Gün, ADX14/ADXR14 ve OBV panelleri; Mavilim 2022–2025 fiyat/kesişim grafiği. Metin Mavilim için "Başarılı." der; ölçülmüş getiri/başarı oranı verilmez.
- Tansu'nun vurgusu: "Biraz daha geliştireyim paylaşırız:)"
- Belirsiz: "ADRX" için iki okuma, ADXR yazım hatası veya başka gösterge adı; görsel ADXR(14) yazdığı için parametre açıklaması ADXR'ye bağlandı, alıntı düzeltilmedi.
- YORUM: KAMA kodlama sorusu, MOST adı ve genel Ichimoku bulut taraması X024/X034'te daha somut varyantları bulunan fikirleri yineler; burada yeniden kayıt yapılmadı. ROC50, X031'in son gün RoC9 sıfır kesişimiyle aynı koşul değildir.

### X629 · 2024-03-23 13:58:11 UTC · PCA/KNN/LSTM fikirleri ve yardımcı boğa oranı
- Bağlı: yeni yöntem; Öneri: tema-5b #30
- Yazar: T + G (boğa/ayı oranı grafiği).
- Kaynak: 1771536925809135885 (2024-03-23 13:58:11 UTC), 1859342666175218082 (2024-11-20 21:06:51 UTC), 1862165685440245988 (2024-11-28 16:04:31 UTC), 1950279832119472221 (2025-07-29 19:38:41 UTC), 1950290925252448467 (2025-07-29 20:22:45 UTC), 1953201892202307992 (2025-08-06 21:09:54 UTC).
- Fikirler:
  - [diğer] "faktör analizi ile (PCA) bist’i etkileyen birden çok faktör arasından en önemlilerini seçip bunları bist100 getirisine regress edeceğiz ve bir hedef endeks değeri belirleyeceğiz." — faktör seçimi→regresyon→hedef endeks planı; değişken/model yok — yalnız fikir.
  - [diğer] "%75 doğrulukla yarın yükselecek demiştik" — KNN yön tahmini bildirimi; veri, eğitim/test bölümü ve doğruluk paydası yok — yalnız fikir.
  - [diğer] "Bu akşam LSTM modelimin denemelerine başlıyoruz." — LSTM deneme planı — yalnız fikir.
  - [teyit-tetik] "buna bakarak asla işleme girilmez, ama momentum hisselerinde yardımcı done olarak kullanabilirim." — boğa/ayı oranını bağımsız girişten dışlar; önceki "boğalar %75 olsun" tarama fikri yalnız yardımcı veri düzeyinde kalır — çekirdek belli.
  - [ölçüm-ilkesi] "Uzun vadede ve büyük hareketlerde logaritmik bakmak genelde daha anlamlıdır çünkü yüzde değişimleri daha iyi gösterir." — uzun/büyük hareket log, kısa/dar aralık lineer tercih; sayısal vade sınırı yok — çekirdek belli.
- Örnek ve sonuç: KNN metninde VİOP akşam seansı +0.25 bildirilir; tek gün gözlemi %75 model doğruluğunu kanıtlamaz. Görselden: GARAN Delta Volume & Bull/Bear Ratio; oranın hesabı yok. PCA ve LSTM için gerçekleşmiş model çıktısı yok.
- Tansu'nun vurgusu: "buna bakarak asla işleme girilmez"
- Çelişir: R185 — M kartın fiyat yönünü tahmin etmeye karşı genel öğüdüne karşı Tansu'nun kendi PCA hedef endeks, KNN yön ve LSTM çalışma gönderileri kaydedildi; M kart bu fikirleri eleme nedeni yapılmadı.
- YORUM: %75 boğa oranı bağımsız AL eşiği olarak alınmadı; çürüten/ sınırlayan sonraki kendi gönderisi esas alındı. KNN doğruluk iddiası başarı ölçümü değil, kaynak iddiasıdır.

### tema-5b özeti

| X no | başlık | bağlı R | olgunluk | yazar |
|---|---|---|---|---|
| X601 | Rolling Sharpe tepkisi | yeni yöntem | çekirdek belli | T + G |
| X602 | Fon katkı, akış ve risk radarı | yeni yöntem | çekirdek belli / yalnız fikir | T + M + G |
| X603 | PRKAB hedef aritmetiği | R114 | çekirdek belli | T + G |
| X604 | UFUK derin Wave 2 | R199 | çekirdek belli | T + G |
| X605 | Çift çıkışları ve rotasyon | R101 / R099 / R251 | çekirdek belli | T + G |
| X606 | Stochastic 14/3 | yeni yöntem | kural tam | T + G |
| X607 | FRAMA adlı kod varyantı | yeni yöntem | kural tam (yazılı hesap) | T + G |
| X608 | PRZMA hedef/stop örneği | R203 | çekirdek belli | T + G |
| X609 | OTT ve Supertrend ayarları | yeni yöntem | çekirdek belli | T + G; köken A |
| X610 | DEY referans ayrımı | R074 | çekirdek belli / kural tam (referans) | T + G |
| X611 | WMA ve CMF ayar sınırı | R137 / R131 | çekirdek belli | T + G |
| X612 | AKD konsantrasyon ölçümü | yeni yöntem | çekirdek belli / kural tam (ölçüm) | T + M + G |
| X613 | RSI-Fibonacci | yeni yöntem | kural tam (hesap) / çekirdek belli | T + G |
| X614 | DuPont ve aday filtresi | R002 | çekirdek belli / yalnız fikir | T + M + G |
| X615 | Merton ters çözüm | R061 | kural tam (model) | T + G |
| X616 | Grid ve ATR taslağı | yeni yöntem | kural tam (taslak hesabı) | T + G |
| X617 | Vegas DOAS kıyası | yeni yöntem; X010 sonuç eki | çekirdek belli | T |
| X618 | Hammer ve kısmi satış | R143 / R224 | kural tam (alt koşullar) | T + G |
| X619 | Yatay ve basamaklı kanal | R246 / R004 / R245 | çekirdek belli | T + G |
| X620 | Temiz alan ve çizgi ölçüleri | R192 / R124 / R039 | çekirdek belli | T + G |
| X621 | PSAR/SMA varyantı | yeni yöntem | çekirdek belli | T + G |
| X622 | BB 3SS ve Keltner | R053 / R082 | çekirdek belli / yalnız fikir | T + M + G |
| X623 | Elliott ve FADE çıktıları | R207 / R261 | çekirdek belli / yalnız fikir | T + G |
| X624 | Kanal orta noktası | yeni yöntem | çekirdek belli | T + G |
| X625 | Mum kodu ve etiketler | R143 | kural tam (kod) / çekirdek belli | T + G |
| X626 | Portföy kontrolleri | R110 | çekirdek belli / yalnız fikir | T + G |
| X627 | Nicel model planları | yeni yöntem | çekirdek belli / yalnız fikir | T + M + G |
| X628 | ROC50/Stoch RSI/Mavilim | yeni yöntem | çekirdek belli | T + G |
| X629 | Tahmin fikirleri/yardımcı oran | yeni yöntem | yalnız fikir / çekirdek belli | T + G |

### tema-5b alınmayanlar

| öneri no | neden | kanıt id |
|---|---|---|
| 8 (tamamı) | Altman/Bathory formülleri Uğur Özarslan'ın *Firmalarda Kredi Analizi* kitabının sayfasıdır; yazar A, Tansu'nun kendi kuralı/kodu değil. Tansu'nun "Kodlayacağım" sözü formüllerin sahipliğini değiştirmez. | 1890148860330406128 (2025-02-13 21:19:40 UTC), görsel 1–2 |
| 2 (erken fon birikimi kısmı) | Pozisyon/ağırlık artışıyla erken fon birikimi X006'da kayıtlı; kalan fon katkısı/akış/risk fikirleri X602'ye alındı. | 2096343856476496081; mevcut X006: 2096000569068454011, 2096679609559347293, 2097384587525812358 |
| 10 (EMA5/20 infografik kısmı) | 1852011542746714531 kod görseli değil, dış infografik; birebir görsel koşulları Tansu'nun kendi kodu olarak alınamaz. Kendi paylaşım cümlesi kodun içeriğini göstermez; diğer ayarlar X609'a alındı. | 1852011542746714531 (2024-10-31 15:35:35 UTC) |
| 11 (R074 dönem düzeltmesi) | 20 Mayıs–1 Haziran dönemi R074'te 07.10 düzeltmesiyle zaten var; aynı düzeltme yinelenmedi. DEY payda/örnek genişlemesi X610'a alındı. | 2061548118592647615; 2061554188832702624; mevcut R074 |
| 12 (altı günlük CMF ve EMA/RSI tekrarları) | CMF son üç pozitif/önceki üç negatif X002'de, EMA5/14/34/55 ve RSI14>50 X001'de var; WMA ve ayar ayrışması X611'e alındı. | 1845558544126366115; 1847735111942336850; mevcut X001/X002 |
| 13 (alıcı satıcıya geçince takipten çıkarma) | Kurum sürekliliği/önceki alıcının sonraki satışını eleme X004'te var; konsantrasyon sınıfları X612'ye alındı. | 1964749763922038906; mevcut X004: 1964614079252938928, 1971236706264207844 |
| 18 (Vegas giriş kuralı tekrarı) | EMA12'nin EMA144/169 üstüne kesişimi X010'da var; DOAS al-tut altında sonuç bildirimi yeni unsur olarak X617'ye alındı. | 1783135314036376019; 1838671862420975657; mevcut X010: 1846640825771377067 |
| 27 (yalnız Black-Litterman adı) | Black-Litterman ile ağırlıklandırma X023'te var; BIST30/bir yıl planı, VIF, profit factor ve risk/getiri sıralaması X626'da ayrı katkılar olarak korundu. | 1797263557978890521; mevcut X023: 1947024537079468538 |
| 29 (KAMA/MOST/Ichimoku genel adları) | KAMA ve MOST X024'te, Ichimoku X034'te daha somut varyantlarıyla kayıtlı; yalnız ad/kodlama sorusu yeni yöntem kuralı eklemiyor. ROC50/Stoch RSI/Mavilim X628'e alındı. | 1852811907666714936; 1844079823829991777; 1840861807633973669; mevcut X024/X034 |
| 30 (boğa %75 ile bağımsız giriş okuması) | Tansu'nun aynı akşamki "buna bakarak asla işleme girilmez" sözü bağımsız giriş okumasını çürütür; çürüten gönderi X629'a, yardımcı veri olarak alındı; ilişkili tahmin karşıtlığı için Çelişir: R185 yazıldı. | 1950279832119472221; 1950290925252448467 |
