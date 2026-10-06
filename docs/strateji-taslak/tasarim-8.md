# TASARIM taslak 8 (öneri): Tansu'nun fikirlerinden kurulan sistem

Not (P5): buradaki her hat bizim yorumumuzdur; "Tansu'nun sistemi" Tansu'nun koduyla aynı demek değildir. Tansu'nun
kodu elimizde yok; elimizde paylaşımları var.

Durum: öneri, **sürüm 5.2** (06.10.2026; 5.1 bağımsız denetimde kabul. 5.2: R245–R263'ün tweet metinleri kaynaktan
çekildi, `ham-yapistirmalar-3.md`; S2'ye Three Drives (H) ve K tarayıcısı, S3'e G R251 kanıtı, yeni sadakat hedefleri). Sürüm 4 (git `ed09d17`) Levent'in eleştirisiyle geçersiz: ilk dalga Tansu'nun
güçlü fikirlerini dışarıda bırakmıştı. Kök neden (five-whys): okuma eski ilke listesini doğrulamak için yapılmıştı ve
modül seçimi "sayısı var mı" ölçütüyle yapılmıştı. Sürüm 5 yalnız kayıt kayıt defterden kurulur
(`defter-1..4.md`, 263/263 kayıt, görseller açık). Defterdeki her strateji fikri `izlenebilirlik.md`'de bu belgenin bir
bölümüne bağlanır ya da 8. bölümdeki gerekçeyle dışarıda yazılır. Levent onaylamadan TASARIM.md'ye girmez; kod bu
belgeden önce yazılmaz.

Kaynak işaretleri: (T) Tansu'nun kendi cümlesi · (G) Tansu'nun araç görseli · (M) yazarı belirsiz uzun metin ·
(G-dış) NotebookLM vb. · YORUM bizim kararımız.

## 1. Tansu'nun sistemi, kendi sözleriyle

Tansu'nun "sistemim", "kodum", "taramalarımız" dediği dört hat var (dördüncüsü risk ve çıkış; değerleme ayrıca aşağıda). Sıra Tansu'nun akışıdır:

1. **Seçim: momentum.** "tüm hisseler önce momentum sistemimden geçiyor sonra ayrıntılı yazıyorum" (T R189). Beş
   aşama: YSA momentum ve pozitif eğim → fiyat ve sinyal eğimi → teknik onay (ADX, CMF, çekiç/sabah yıldızı) →
   Markowitz → Max Sharpe (T R137, "Bu sistem satılık değil").
   Momentumun BIST'te çalıştığını kendisi test etti: 500+ hisse, 2015'ten bugüne, 12 aylık getiri, 10 dilim, aylık
   yenileme, eşit ağırlık (T R120). Listeye rolling alpha ve rolling skewness uyguluyor (T R202); skewness'i "tek
   başına AL/SAT sinyali olarak kullanmam ... dağılım filtresi olarak kullanırım", 63 gün, eşik +0,50 (T R260).
2. **Kurulum tarayıcıları.** Her formasyon ayrı tarayıcı: "Gartley taramasını ayrı yapın butterfly taramasını ayrı yapın"
   (T R011). Sonuç tek tabloda: Hisse, Tip, Sistem, Durum, Reaksiyon, D Hedefi, Giriş, Stop (X) (G R012). Araçların
   başlıklarında dört tarayıcı görünüyor:
   - "Düşen Direnci Kıran + Talep + Fibo + ABCD" (G R075, R087), Gartley/Kelebek/AB=CD (G R008, R012, R013, R014, R017).
   - "FVG TEMAS | BULLISH | ELLIOTT WAVE 2 (Fibo: %64.3)" (G R199, R241); "Hafta başında verdiğimiz listede idi. %8
     getiri" (T R204).
   - "EMA Sıkışması | Tolerans %1.2 | Min 3 gün" (G R127); talep bölgesinde EMA 5-8-13 (T R198 "Ben 5-8-13 kullandım").
   - "Breakout + Range Retest + RSI Divergence | A+ SETUP | AL TETİKLENDİ" (G R253 AKFIS); "Breakout-->FVG-->Retest-->
     Confirmation / Bu yapıları arayın" (T R254).
   Ayrıca fincan-kulp "kendi tarama sistemimin yakaladığı" (T/M R114) ve Three Drives, oranları ve simetrisiyle
   ("Benim açımdan Three Drives'ı değerli yapan şey tam olarak budur", T R249).
   Analiz sırası: "İlk sorum şudur: Fiyat şu anda hangi yapının içinde ve alıcı mı satıcı mı kontrolü ele geçirmeye
   çalışıyor?" ... "Şablonu aynı zamanda koşullar ve sonuçlar ile koda da döktüm" (T R256).
   Formasyon bölgesiz kullanılmaz: "D noktasına bakın, talep toplama bölgesine bakın, hissenin tepkilerine bakın. Doğru kod
   böyle yazılır." (T R080); "gözü kapalı ABCD'ye nasıl güveneceksin kanalı okumadan" (T R085); "İşte bu yapıların
   peşindeyiz." (T R081); "confluence alanları o kadar kıymetli ki ... taratmak lazım" (T R055).
3. **Çift (istatistiksel arbitraj).** "Arbitraj her zaman en en sevdiğim 2 sistemden birisi" (T R102). Eşbütünleşme
   "şarttır, şarttır. şarttır." (T R228); rolling eşbütünleşme (T R034); Z ±2 giriş (M/T R099, R101); Tansu'nun aracında çıkış ters sinyalde öbür hisseye geçiştir (G R251).
4. **Risk ve çıkış.** Boyut volatiliteyle küçülür (T R211); %1 risk örneği (T R212 "Diyelim ki"), 2 ATR acil stop ve
   SMA250 gün sonu çıkışı (G-dış R212 infografik; T R212 SMA250'yi "giriş bileşenlerinizden birisi" diye anar; T/M R184
   2 ATR). Çıkış zinciri: Giriş + 1,5 ATR'de iz süren mod, sonra önceki gün dibi altı kapanışta %50, kalan için 2 ATR
   acil stop (T R224, R239). Ödül/risk < 1,5 ise girilmez (M R222, araç tablosu; T R234 "Kritik Kural ... en az 1:1.5").
   Rejim: "sistemim pozisyonu kapatıp defansif pozisyoon aldı. Fiyat ve volatilite aynı anda artması pek istenilen bir
   durum değildir" (T R092); şokta yeni alım yok (T R026).

Ayrı bir hat, **değerleme** (T R062, R064 "Kabaca sistem bu", R068, R151, R158, R166), bilanço verisi ister; 8. bölüm.

## 2. Veri gerçeği (bağlayıcı kısıtlar)

| Var | Yok |
|---|---|
| Kapanış, yüksek, düşük, AOF, TL hacim (2000'den), fiili dolaşım değeri*, sermaye, piyasa değeri (TASARIM 5.1) | **Açılış** (mum gövdesi, engulfing, çekiç, doji, Heikin Ashi tam kurulamaz) |
| XU100 kapanışı, sektör (bugünkü sınıflama), faiz | Bilanço (satış, kâr, FAVÖK, borç, özkaynak) |
| Haftalık mum (günlükten türetilir) | VIX, opsiyon IV, gün içi veri, emir defteri, kümülatif delta, açık pozisyon / COT (T/M R227; Tansu da vekil kullanır, 4.5) |

\* Kaynak alanı `HAO_PD` (halka açık piyasa değeri). Tansu'nun KAP "fiili dolaşım oranı" (T R035, R083) ile aynı tanım
olduğu doğrulanmadı; ilk bilette KENT %0,54 ve GARAN %13,98 (G R035) değerleriyle karşılaştırılır.

Sonuç: açılış gereken yerde AOF vekil olur ve YORUM yazılır. Gövde vekili (kapanış–AOF aralığı) yalnız talep bölgesi
tabanında kullanılır (4.1); mum formasyonu sınıflaması (engulfing, çekiç, doji, gravestone) resmi kola girmez, yalnız
ölçülür.

### 2.1 Değişen TASARIM maddeleri (taslak 7 kararları)

- **3 Kapsam dışı:** harmonik formasyonlar ve Elliott dalga 2 kapsama girer (S2 H ve E).
- **5.3 SMA250 giriş kapısı:** S2'de aynen; S1'de uygulanmaz (sıralama kuralı, YORUM).
- **5.5 Çıkış:** "hedef yok" ve "iz süren stop ve kısmi kâr ikinci el" kalkar; S2 çıkış zinciri T R224/R239'dan (4.4).
- **5.6 Çift:** aynı sektör şartı kalkar (T R096 tüm kombinasyonlar); rolling eşbütünleşme ve Z 0,5 çıkışı resmi
  kola girer (3.3).
- **5.12 Boru hattı denetimi:** her yeni kod hash'inde (`_resmi_bitti` istisnası kalkar).
- **Corwin–Schultz, NH-NL, fiyat-hacim konumu:** yalnız ölçüm katmanında (4.5).

## 3. Resmi sınav: üç hipotez

Her resmi kol Holm m'yi kalıcı artırır; 2015–2026 tümü geliştirme verisidir (5.8). Bu yüzden resmi sınava **Tansu'nun
kendi sistem dediği hat başına tek hipotez** girer. Tarayıcıların tek tek sonucu ölçüm koludur (5.2).

### 3.1 S1 — Momentum rotasyonu (T R120)

S1, Tansu'nun canlı "momentum sistemim"i değildir (o YSA ile kurulu ve gizli, T R137). S1, Tansu'nun yayımladığı BIST
testidir (T R120: "Ben de bunu BIST'te test etmek istedim"); kuralı tam olan tek momentum metni budur.

- Her ayın ilk işlem günü kapanışında evren (TASARIM 5.2, ilk 100) son 252 işlem günü getirisine göre sıralanır.
- En üst %10 (10 hisse) eşit ağırlıkla ertesi AOF'ta alınır, bir ay tutulur; ay başında yeniden kurulur. Masraf %0,3,
  likidite %2 sınırı aynen. Pencere 12 ay (T R120); "12 ay − 1 ay atlama" Tansu'da yok, kullanılmaz.
- Evren YORUM: Tansu 500+ hisse kullandı (dilim ≈ 50 hisse). Resmi kol ilk 100'de kalır, çünkü işlemi kapanan hisse
  ve sağkalım kontrolü TASARIM 5.2'de yalnız bu evrende kuruludur. Geniş evren ölçüm kolu: 20 günlük ortalama TL hacmi
  ≥ 10 milyon TL olan tüm hisseler (T/M R232), dilim %10.
- Stop yok (Tansu'nun testinde yok). SMA250 giriş kapısı uygulanmaz (S1 bir sıralama kuralıdır; YORUM).
- K2: evrenin eşit ağırlıklı sepeti (zaten var). K1: aynı ay, evrenden rastgele 10 hisse (B tekrar).
- Ölçüm kolları: Tansu'nun 5 dilimli çeyreklik hali (T R022 Mom5); Clenow eğim × R² (T R176, kodundaki
  `(1+slope)**252` aynen ve `exp(slope)**252` ayrı); rolling alpha ve rolling skewness filtresi (T R202; pencere 63 gün ve
  eşikler T R260: skew > 0 "yapıcı", > +0,50 "belirgin pozitif sağ kuyruk", < −0,50 "dikkat"; ayrıca skew değişimi
  "-1.0 → -0.5 → 0 → +0.3 → +0.6" kesimi, değişim penceresi 21 gün YORUM; log getiri, T R260); eğim kapısı: fiyat eğimi > 0 ve sinyal eğimi > 0 (T R137, R105; eşik 0 = "eğim negatiften pozitife dönüyorsa", T X6); teknik onay: ADX > eşik ve CMF > 0
  (T R137 3. aşama; ADX ve CMF açılışsız hesaplanır, eşik YORUM; çekiç/sabah yıldızı AOF vekiliyle); Max Sharpe ile 3–10 hisse
  (T/M R110, T R137, R181); şok freni ve fiyat+volatilite rejimi (bkz. 4.5); fiili dolaşım < %30 (T R083) ve
  > %30 kesimleri; sektör lideri filtresi 30/60/90 gün, |30g getiri| > %50 anomali hariç (G R032, R033); endekse göre
  göreli güç (T R073: "Henüz endeksi yenecek güçte değil"); tek hisse ağırlık duyarlılığı (T R112).

### 3.2 S2 — Kurulum hattı (Tansu'nun tarayıcıları)

**Akış** (T R189, R080): momentum kapısı → bölge → formasyon (ayrı tarayıcılar) → ödül/risk kapısı → giriş → yönetim (4).

1. **Momentum kapısı:** hisse, o ayın S1 sıralamasında üst yarıdadır (YORUM: Tansu'nun momentum formülü YSA ve gizli,
   T R137; 12 ay getirisi onun BIST testindeki ölçüdür, R120). SMA250 giriş kapısı TASARIM 5.3'teki gibi kalır (Tansu
   SMA250'yi giriş bileşeni örneği olarak anar, T R212 "bu 200SMA 200EMA 250EMA' da olabilir, stratejinize kalmış").
2. **Talep bölgesi** (4.1): kurulumun giriş seviyesi geçerli (kırılmamış) bir talep bölgesinin içindedir. Zorunlu
   (T R009, R080, R081, R085). Ölçümde bölgesiz kol da koşulur (Tansu'nun cümlesini sınamak için).
3. **Beş tarayıcı**, ayrı kod (T R011), tek sonuç tablosu (G R012):
   - **H — Harmonik:** AB=CD, Gartley, Kelebek, Three Drives; her alt tip ayrı kod, tek H tarayıcısı (T R011; oranlar standart tanım, YORUM: Tansu oran
     vermedi). Giriş D'de limit (G R012 LUKSK "Giriş = D Hedefi", G R014 "Giriş (D)", G/M R222 "Buy Limit").
     - AB=CD: kapı T R019 (BC ≤ AB, BC = 1,00 olabilir, D B'yi aşar; giriş öncesi C'den sonra A geçilirse kurulum
       bozulur). BC/AB alt sınırı 0,382 (M R080); üst sınır 1,00 (T R019). M R080'in "0,382–0,618" aralığı T R019 ile
       çelişir; T esastır. D = C − 1,0·(A−B) (CD = AB, G R079, R081, R084; R085, R087'deki 1,27 ölçüm kolu, YORUM).
       Giriş sonrası geçersizlik: kapanış CD = 1,272·AB seviyesinin altında (M R080 oran listesinin bir sonraki
       değeri, YORUM; Tansu AB=CD için giriş sonrası stop vermedi).
     - Kelebek (H alt tipi; T R003, R004, R011; G R250 DOAS): B = XA 0,786, D = XA 1,272 uzantısı (G R250 "1.272
       (D hedefi): 159.49; D: 159.40 [TAMAMLANDI]"), tolerans Gartley'deki gibi (YORUM). Geçersizlik XA 1,618 (G R250
       "1.618 (max risk): 146.00"; kapanışla sınanması YORUM). B oranı standart tanım (YORUM).
     - Gartley (araç tablosu G/M R222): B = XA 0,618, C = AB 0,382–0,886, D = XA 0,786, tolerans %3–5. Geçersizlik X
       (G R012 "Stop (X)", G R014 "Bk Stop (X)"); R222 görselindeki X − 2 ATR ölçüm kolu.
     - Three Drives (T R249, 06.10 tweet metninden): alış yönünde üç giderek düşen dip (Drive 1, 2, 3; T "düşen
       piyasada ise üç adet giderek düşen dip"). A ve C düzeltmeleri önceki drive'ın 0,618–0,786'sını geri alır;
       Drive 2 ve Drive 3, önceki düzeltmenin 1,272–1,618 uzantısında biter (T "yaklaşık"; tolerans YORUM, Gartley'deki
       %3–5). Fiyat simetrisi: |A→Drive 2| ile |C→Drive 3| yakın; zaman simetrisi: iki bacağın bar sayısı oranı
       ≤ 1,5 (T: 10'a karşı 11–12 dengeli, 8'e karşı 30 bozuk; 1,5 eşiği YORUM). Giriş Drive 3'te değil, reaksiyon
       teyidinde (T "Drive 3 oluştu diye doğrudan ters yönde işlem açmak doğru değildir"): 4.3 tepki tanımı sağlanınca
       ertesi AOF. Geçersizlik: C'den ölçülen 1,618 uzantısı (T "1,618 extension seviyesini aşabilir ve formasyon
       başarısız olabilir"); bunun kapanışla sınanması ve stop sayılması YORUM. Drive 3 zaten 1,618'in altındaysa
       geçersizlik Drive 3 dibi altı kapanıştır (YORUM). Hedef: C (son düzeltme tepesi; YORUM, Tansu hedef vermedi).
       Örnek: C bacağı L, Drive 3 = C − 1,272·L, giriş Drive 3 + 1 ATR (e) ise ödül 1,272·L − e, risk 0,346·L + e;
       e = 0,1·L için oran 1,17/0,45 ≈ 2,6 (kapıyı geçer). Sadakat hedefi yok (Tansu'nun örneği sembolsüz, satış yönlü).
     H ölçüm kolları: C'den alım, D'de satış (T R018 "C noktasından alım yapılsa idi D satış karları"; sürüm 4'ün resmi
     kolu; giriş C'nin pivot olarak doğrulandığı günün ertesi AOF'u); X–B trend çizgisi kırılımı girişi (T R013, G R008); Lindsay Trident hedefi D = (B·C)/A ve B kırılımı teyidi
     (T R090, alış yönlü paragraf; satış yönlü kural açığa satış olduğu için yok); hedef merdiveni TP1–TP4 = D +
     {0,382; 0,618; C; 1,272}·(C−D) (M/G R203) ve TP1 1:1 R/R, TP2 0,618 CD (G R014); Kuğu harmonikleri (T R075, R076;
     oran verilmedi, standart tanım YORUM); harmonikte EMA sıkışması var/yok kesimi (T R005 "hangi noktada momentum
     squeeze olur"); CD bacağının şiddeti (CD/AB oranı, CD süresi, CD hacmi) ile sonuç ilişkisi raporu (T R016 "CD
     bacağının şiddetini ne belirler? Çok önemlidir").
   - **E — Elliott dalga 2 + Fibonacci + FVG** (M R199 kuralı, G R199/R241 araç çıktısı, T R204 sonuç): Point 0'dan
     Point 1'e en az %10 itki ve önceki tepeyi geçme (yükseliş yapısı, HH); geri çekilme 0,50–0,786 (ideal 0,618–0,65);
     bu aralıkta doldurulmamış yükseliş FVG'si (1. mum yükseği < 3. mum düşüğü). Giriş FVG üst bandına limit (M R199
     ilk seçenek; araç başlığı "FVG TEMAS", G R199/R241); 0,618'e limit ölçüm kolu. Geçersizlik Point 0 altı. Aynı aileden M R197 (BOS → 0,618–0,786 OTE + FVG/OB, stop Fib 1,0) bu tarayıcının
     tanımıyla aynıdır; ayrı tarayıcı yapılmaz. E ölçüm kolları: A-B-C zigzag düzeltmesi kesimi (M R199 "Tercihen");
     düzeltmenin önceki yükselen dibin (HL) üstünde kalması kesimi (M R242); dalga 4 geri alımı 0,24/0,38/0,50 (T/M R205:
     "Unutmuyoruz" T, kural metni M biçimli);
     FVG güç sınıfı, 1. mum yükseği ile 3. mum düşüğü arası boşluğun ATR'ye oranı (G R050 Strongest…Weakest); dolmuş FVG
     sonrası giriş (M R243); FVG yerine talep bölgesi (T R261 CWENE: Dalga 2 ∩ 32,5–36 demand, "bence önemli bir
     konfluens"; M/T R241 "FVG ... veya Talep Bölgesi"); muhafazakâr giriş: ilk direncin kırılımı (T R261 "Daha
     muhafazakâr yatırımcı ise önce 40–41.5'in kırılmasını bekler").
   - **S — Talep bölgesinde EMA sıkışması** (M R198 kural; T R198 "5-8-13"; G R127 KRDMD çapası): bölge içinde
     sıkışma oranı = (en büyük EMA − en küçük EMA) / kapanış, EMA 5/8/13 ile, en az 3 gün tolerans altında. Oran formülü
     taslak 7'deki gibidir (YORUM; Tansu formül vermedi, T R127 "sıkışma rasyosu sizin tecrübenize kalmış"). Tolerans %1,2
     ve min 3 gün G R127'den taşınır; orada EMA'lar 20/50/100/200'dür, 5/8/13'e taşınması YORUM.
     Giriş: kırılım mumu (kapanış sıkışma kutusunun üstünde) ertesi AOF (M R198 "Güvenli Giriş"). Geçersizlik bölge
     altı (M R198). Taslak 7'nin EMA ailesi buraya taşınır; eski aile günlükte kalır. S ölçüm kolları: EMA 20/50/100/200
     sıkışması (G R127 KRDMD, G R125 ICBCT EMA30/50/100/200); kırılım sonrası boğa dizilimi EMA5 > EMA8 > EMA13 teyidi
     (M R124, T R214, G R167, M R128); retest girişi (M R198, T R194); sıkışma süresi ile kırılım şiddeti raporu (T R082
     "konoslidasyon ne kadar uzarsa kırılım o denli şiddetli"; T R077 rehavet; T R086 breakout).
   - **F — Fincan-kulp** (T/M R114 "kendi tarama sistemimin yakaladığı"; G R114 GUBRF görseli): sol ağız = dipten
     önceki en yüksek pivot (GUBRF 300,75), dip (212,20), sağ ağız = dipten sonraki ilk pivot tepe (317,00); kulp, sağ
     ağızdan (sağ ağız − dip) aralığının %50–%78,6'sı kadar geri çekilir (metin %50–61,8 der, görselde kulp tabanı
     ≈ %70; aralık YORUM). Sinyal: kulptan sonra kapanış sol ağız çizgisinin üstünde ("KIRILMA 300.75", G R114); giriş
     ertesi AOF. Hedef = kırılma + (kırılma − dip) (GUBRF: 300,75 + 88,55 = 389,30, Tansu'nun hedefiyle birebir).
     Geçersizlik: kulp dibinin altında kapanış (YORUM; Tansu'nun 1:2,27 oranı hiçbir basit giriş/stop çiftiyle
     çıkmıyor, `kural-yok-inceleme.md` 24). Bölge kapısı: kulp dibi geçerli bir talep bölgesinin içinde (YORUM, R080
     ilkesi); bölgesiz hal ölçüm kolu. Sadakat hedefi: GUBRF sinyal 2025-10-24.
   - **K — Kırılım → FVG → retest → teyit** (T R254 "Breakout-->FVG-->Retest-->Confirmation / Bu yapıları arayın";
     T R253 "Dikkat edelim bu yapıya"; G R253 AKFIS "Breakout + Range Retest ... A+ SETUP | AL TETİKLENDİ"):
     konsolidasyon = en az 10 mum, (en yüksek − en düşük) ≤ 3 ATR (YORUM); kırılım = kapanış konsolidasyon tepesinin
     üstünde (4.2); kırılım mumları içinde yükseliş FVG'si (4.2); retest = sonraki 10 mum içinde gün düşüğü
     konsolidasyon tepesine ya da FVG'ye değer, kapanış konsolidasyon tepesinin altına inmez (YORUM); teyit = retest
     sonrası ilk kapanış retest mumunun yükseğinin üstünde (YORUM; Tansu tanım vermedi). Giriş teyit ertesi AOF.
     Geçersizlik: kapanış FVG alt kenarının altında (YORUM). Hedef: ilk arz bölgesi (S ile aynı). Talep bölgesi
     kapısı burada eski direncin (konsolidasyon tepesi) desteğe dönmesiyle sağlanmış sayılır (YORUM; G R253 "RANGE
     HIGH RETEST"). Sadakat hedefi: AKFIS, AL tetiği 2026-09-03 ve öncesi (G R253; görselde fiyat etiketi yok,
     yalnız tarih ve sıra sınanır). Ölçüm: RSI uyumsuzluğu kesimi (G R253 başlığı "RSI Divergence").
4. **Ödül/risk kapısı:** risk = giriş − geçersizlik; ödül/risk < 1,5 ise girilmez (M R222; aynı eşiği T R234 kendi
   lojistik modeli için "Kritik Kural" diye yazar). Ödül:
   - H: ana hedef TP2 (Gartley D + 0,618·(A−D), G/M R222 "Kalan Pozisyonu Kapat"; AB=CD D + 0,618·(C−D), M/G R203
     "Ana Hedef"). YORUM: R222 ödülü TP1 diye yazar. Ama TP1 = D + 0,382·(A−D) ve stop X ile her Gartley'de oran
     0,382·0,786/0,214 ≈ 1,40'tır; harfiyen okumada hiçbir Gartley 1,5'i geçmez. Harfiyen hal ölçüm kolu.
     Three Drives: C (YORUM).
   - E: Point 1 (M R199 "Hedef 1"; T R261 CWENE'de de Dalga 1 tepesi 48,30 "Asıl mücadele").
   - F: kırılma + (kırılma − dip) (T/M R114).
   - K: ilk arz bölgesi (YORUM).
   - S: ilk arz bölgesi ya da ilk düşüş FVG'si (M R198; T/M R192 "yeni tarama kodumuz": demand giriş, bearish FVG ilk
     hedef, supply).
   Ölçümde 2 ve 3 eşikleri (M R230).
   Ölçüm: aktif volatilite kesimi, yıllık gerçekleşen volatilite ≥ %40 ve altı (M R230 "Aktif Volatilite ... Aranmalı";
   T/G R223 kodundaki eşik 0,40, 252 gün).
5. **Bakış ileri yok:** pivot ancak sağındaki k mum kapanınca bilinir; FVG 3. mum kapanınca; talep bölgesi leg-out
   koşulu sağlandığı mum kapanınca; haftalık mum, pivot ve bölge yalnız hafta kapandıktan sonra (haftanın son işlem
   günü kapanışı) kullanılır ve o haftanın günlerine geri yazılmaz; FVG "doldurulmamış" durumu yalnız o güne kadarki
   mumlarla. Three Drives: Drive 3 dibi ancak sağındaki k mum kapanınca pivot olur; tepki o günden sonra aranır. K:
   her aşama (konsolidasyon, kırılım, FVG, retest, teyit) yalnız kendi mumu kapanınca bilinir; teyit günü sinyal
   günüdür. `test_gelecek.py`'ye girer (Three Drives ve K dahil).

**Neden tek hipotez:** Tansu tarayıcıları ayrı yazar ama aynı listede, aynı yönetimle sunar (G R012; T R204 "verdiğimiz
listede"). Beş tarayıcıyı ayrı resmi kol yapmak m'yi 4 fazla artırır (1 yerine 5) ve her birinin işlem sayısını düşürür. Tarayıcı başına
sonuç ölçüm kolunda raporlanır (kabul kararına girmez).

**K1 (S2):** ön şart = momentum kapısı + SMA250 + fiyat geçerli bir talep bölgesinin içinde. Kural = ön şart + beş
tarayıcıdan birinin kurulumu + ödül/risk kapısı. Soru: "Tansu'nun formasyonları, bölgede rastgele bir günden iyi mi?"
Rastgele girişe sinyalin yüzde stop ve yüzde hedef mesafesi taşınır; çıkış zinciri aynı. Tür (a) ve (b) taslak 7 gibi.

### 3.3 S3 — Çift rotasyonu, Tansu sürümü

**Önce gerçek:** taslak 7'nin çift kuralı ilk resmi koşuda geçmedi (`kayit/deneme.jsonl`, koşu 20261005T205624:
fazla getiri yıllık −%9,0, güven aralığı [−%14,6, −%2,8], 91 işlem, Holm p 1,0; ızgaranın 18 hücresinin hepsi
negatif). O kural aynen yeniden girmez. Sonucu günlükte kalır.

S3, Tansu'nun metnindeki üç unsuru taşıyan yeni kuraldır. Bu, aynı fikrin ikinci denemesidir; Holm m'ye sayılır ve
raporda "ilk deneme geçmedi" yazılır:
- Aday çiftler: evrendeki tüm çiftler (YORUM: T R096 "150.000 kombinasyon taramasına kadar" sektör şartından söz
  etmez; bu sayı tüm çiftler ölçeğidir, sektör içi değil. Taslak 7'nin aynı sektör şartı da YORUM'du).
- Seçim (YORUM, taslak 7 düzeni): yılın ilk işlem günü; aday hisse 252 işlem günü verisi olan evren üyesi; iki rolling
  pencerenin ikisinde de p < 0,05 olan çiftler p'nin büyüğüne göre artan sıralanır; açgözlü seçim, bir hisse en çok bir
  çiftte, en çok 5 çift. Çoklu test: ilk 100 evrende ≈ 4.950 çift var; %5 eşikte şans eseri ≈ 250 çift geçer. İki
  pencere şartı ve en küçük p sıralaması bunu azaltır ama gidermez; resmi kayıttan önce boş dünya denetiminde (TASARIM
  5.12) seçilen çiftlerin şans tabanı ölçülür ve raporda yazılır.
- Kapı: rolling eşbütünleşme. Çift yalnız son 252 günde ve son 126 günde p < 0,05 iken işlem görür (T R034 "rolling
  cointegration ile zamanla bozulmayı önlüyor", T R228 "şarttır"; pencereler YORUM).
- Giriş Z ±2 ve ΔZ dönüşü (mevcut kuraldaki gibi; Tansu'nun "momentum dönüş teyidi" T R098 ve G R095 "Z-Skoru ve
  Momentum Dönüşü Onaylı İşlemler" ile aynı şey olduğu YORUM). Z ≤ −2'den dönüşte Y (ucuz bacak) alınır, Z ≥ +2'den
  dönüşte X alınır. Çıkış (06.10 düzeltmesi): ters sinyalde öbür hisseye geçiş; tutulan hisse ters sinyale kadar
  tutulur (G R251 grafiği: altı AL etiketi = "Gecis Sayisi 6"; portföy yalnız ilk sinyalden önce nakitte). Rolling kapı
  bozulursa nakde çıkış (T R100 "Görünmez bağ kopmuş olabilir"; M/T R101 "Yanıldığını anladığı an zararı keser").
  Z 0,5'e dönünce nakde çıkış (M/T R101 "normale (0.5 seviyelerine)") ölçüm kolu olur: Tansu'nun aracı böyle çıkmıyor,
  metin M/T karışık.
- Long-only: Tansu'nun uzun-kısa işlemi (M/T R099 "AGROT SAT, GARAN AL") burada ucuz bacağı tutan rotasyondur; bu
  arbitraj değil, göreli değer işlemidir. İlk denemenin geçmemesinin nedeni bu olabilir; sınanamaz (açığa satış yok).
  Tansu'nun kendi aracı da long-only rotasyon yapar (G R251 "RELATIVE VALUE ROTATION | VAKBN <-> GARAN": "Aktif Hisse
  VAKBN", "Piyasada Kalma +72.27%", "YENI AL SINYALI | VAKBN AL | Y goreli ucuz, Z donusu +0.30", işlem "T+1 Open";
  Son Z −3,108, önceki Z −3,404, "Cointegration p 0.048"). Bu, "ucuz bacağı tutan rotasyon" yorumunu Tansu'nun araç
  çıktısıyla destekler; ΔZ dönüşü giriş şartı (Z −3,40 → −3,11 ve "Z donusu +0.30" etiketi) bu çıktıyla uyumludur. Raporun kendi sayıları
  (toplam +%52,86, 50/50 al-tut +%20,88, en büyük düşüş −%27,44, 6 geçiş) kaynak iddiasıdır, bağımsız ölçülmedi.
  Piyasada kalma %72'nin nakit kısmı ilk sinyalden önceki dönemdir (portföy paneli 2025-06'ya kadar düz); sonra araç
  hep bir hisse tutar. Kointegrasyon testleri: "Johansen veya Engle-Granger" (M R262); burada Engle-Granger.
- Boyut: tüm bölme sermayesi (M/T R099 "tüm bakiyesiyle"; TASARIM 5.6 çift bölmesi).
- Tansu'nun ilkesi "Borsada "yönü" bilmek zorunda değilsiniz" (M/T R101) piyasa yönünden bağımsız (uzun-kısa) işlem
  ister; long-only rotasyon bu ilkeyi taşımaz, yalnız yaklaşır (kilit: açığa satış).
Ölçüm: taslak 7'nin aynı sektör kuralı (karşılaştırma), z_pencere 120, Z 0 çıkışı, Z 0,5 çıkışı (M/T R101).

### 3.4 m ve B

AILELER = {S1, S2, S3} → yeni 3 çift; eski 2 çift günlükte kalır → **m = 5**, B = max(1.000, 200·m) = 1.000.
Sayım koşusu (5.2) S1 ve S2'nin ≥ 100 işlem ve ≥ 60 farklı gün eşiğini geçeceğini göstermezse o hat resmi olmaz,
yalnız ölçüm olur (m düşer).

## 4. Ortak yapı taşları ve yönetim

### 4.1 Talep bölgesi (T R037, G R047, T R043, T R051)

- Taban (base): sert yükseliş (leg-out) öncesi küçük gövdeli mumlar (G R047 RBR). Açılış yok: gövde yerine
  kapanış–AOF aralığı kullanılır (YORUM, 2. bölüm).
- Eşikler (Tansu vermedi; hepsi YORUM, ön kayıtlı aday kümesi, sadakat koşusunda 5.1 hedeflerine karşı seçilir):
  taban mumu = gövde vekili ≤ gün aralığının %50'si; taban 1–6 mum; leg-out = tabandan sonraki en çok 3 mumda kapanış,
  tabanın en yükseğinin en az 2 ATR üstüne çıkar. Adaylar: gövde oranı {%40, %50, %60}, leg-out {1,5; 2; 3} ATR.
- Proximal = tabanın en yüksek gövdesi (talep tarafı), distal = tabanın en düşüğü (G R047 "DISTAL line always be at the
  low of base candle or leg out candle"; T R037 arz tarafı tanımı).
- Bölge, kapanış distal altına inince biter (T R043 `Close < zone_low`; katı sürüm Low ölçümde).
- Haftalık bölge ayrıca üretilir (T R081 "haftalıkta"; T R015 haftalık tarama).
- Konsolidasyon sınırı (T R051) ve sponsor mumu (G R054: hareketten önceki son zıt renkli mum) ölçümde alternatif
  bölge tanımlarıdır. Ayrıca ölçümde: KDE fiyat yoğunluk seviyeleri (M R128), günlük pivot P/R/S (G R191), boşluk
  (gap: gün düşüğü > önceki gün yükseği; M R195; açılışsız tanım YORUM).
- Bölge kalitesi (ölçüm): talep bölgesi ile yatay destek (HSAR: önceki salınım tepe/diplerinden yatay seviye) kesişimi
  (G R055 "Talep+HSAR Kesişimi", T R055 "taratmak lazım. Her seferinde zenginlik yaratmışlar"); bölge temas sayısı
  (G R041–R043 D.Touch); çoklu aralık Fibonacci kümesi (G-dış R217).

### 4.2 Pivot, Fibonacci, FVG

Pivot: sağ ve sol k mum (k ön kayıtlı aday kümesi, YORUM; Tansu vermedi, T/M R039 "swing pivot" yöntemini anlatır).
Trend çizgisi: iki pivotu birleştirir; aradaki hiçbir mum çizgiyi delmez; dokunuş sayısı güçtür; kırılım kapanışladır
(T/M R039: soru ve "Ben hangisini kullanıyorum" T, yöntem anlatımı M biçimli; regresyon-zarf yöntemi ölçüm kolu; araç çıktısı "Temas: 3 | Lookback: 20", G R075, R087, R008). Düşen direnç kırılımı bu tanımla ölçülür.
Yapı: BOS = önceki tepenin kapanışla kırılması; CHoCH = son yükselen dibin altına kapanış (M R041, R129, R197).
Günlük grafikte kullanılır; 1H/4H CHoCH teyidi (M R129) ve H4 Order Block (T R206) gün içi veri ister, yoktur.
Fibonacci bir "bölge"dir (T R206): seviyeye ±tolerans uygulanır (tolerans ön kayıtlı aday, YORUM).
Fibonacci seviyeleri araç çıktılarındaki gibi: 0,236 / 0,382 / 0,5 / 0,618 / 0,786 / 1 / 1,272 / 1,618 / 2 (G R008,
R020). FVG: 1. mum yükseği < 3. mum düşüğü (M R199); "doldurulmamış" = sonradan fiyat boşluğa girmemiş.

### 4.3 Kurulum durumu (Tansu'nun etiketleri, G R008, R012, R013, R017)

Tansu'nun araçlarında etiket formasyonun durumudur, işlemin değil: AKTİF = yapı bulundu, D (giriş) henüz gelmedi
(G R008 DGATE "D: 49.66 [AKTİF]", G R012 SOKE "AKTIF"); TAMAMLANDI = D geldi (G R012 LUKSK "TAMAMLANDI", G R013 KAPLM
"[TAMAMLANDI]"); TEPKİ_VERDİ = D sonrası tepki (G R012 "Reaksiyon: TEPKI_VERDI"); BOZULDU (G R008 KRPLS, G R017).
```
AKTİF ──(fiyat D'ye değdi)──> TAMAMLANDI ──(tepki)──> TEPKİ_VERDİ
  │                              └──(10 gün tepki yok)──> BELİRSİZ (T R014)
  └──(D'den önce yapı bozuldu)──> BOZULDU
```
İşlem sonucu ayrı alandır: açık / hedef / geçersizlik / acil stop / SMA250 / iptal. Tepki: kapanış girişin üstünde ve
girişten en az 1 ATR yukarıda (YORUM). 20 bar penceresi (G R013) ölçümde ayrı parametredir. E ve S tarayıcılarında
"D" yerine giriş seviyesi okunur. Three Drives'ta giriş tepkiden sonra gelir; bu yüzden tepki Drive 3 dibine göre
tanımlanır: kapanış Drive 3 dibinin en az 1 ATR üstünde ve önceki günün yükseğinin üstünde (YORUM; Tansu "reaksiyon"u
tanımlamadı).

### 4.4 Yönetim (S2 resmi kol)

- **Limit dolumu** (H ve E): gün düşüğü ≤ limit − 1 fiyat adımı; dolum fiyatı limit; aynı gün dolum ve stop ise stop;
  taban kilidinde dolmaz; 10 işlem gününde dolmazsa iptal (10 gün YORUM). (Sürüm 4'te ölçümdeydi; şimdi resmi
  koldadır, hash içi.) Three Drives, S, F ve K limit kullanmaz: giriş sinyal gününün ertesi AOF'udur.
- **Boyut:** %1 risk, adet = risk / (giriş − geçersizlik); %10 tavan, %2 likidite, en çok 10 pozisyon (T R211, R212;
  %1 örnektir, YORUM). Geçersizlik mesafesi 2 ATR'den büyükse acil stop 2 ATR'dir ve boyut ona göre hesaplanır
  (YORUM: Tansu adedi 2 ATR'ye böler, G-dış R212; burada küçük olan mesafe kullanılır).
- **Çıkış zinciri** (T R239 ve R224'ün sonu, harfiyen): (1) geçersizlik ya da giriş − 2 ATR acil stop, gün içi
  (stop dolumu TASARIM 5.3); istisna: AB=CD geçersizliği ve talep bölgesi bitişi kapanışladır (T R043 `Close <
  zone_low`), ertesi AOF'ta çıkılır; acil stop yine gün içidir; (2) fiyat giriş + 1,5 ATR'ye ulaşınca iz süren mod (T R224, R239); (3) sonra ilk
  "kapanış < önceki gün düşüğü" gününde %50 ertesi AOF'ta satılır (T R239 "İlk kar alma yeriniz ... %50'sin satın";
  T R224 "önceki günün en düşüğünün altında kapanış ve %50 satış"); (4) kalan %50 "emergency stop 2atr ile kalan tüm
  maldan çıkış" (T R224): giriş − 2 ATR acil stopta ya da kapanış SMA250 altında (G-dış R212 gün sonu çıkışı) kapanır.
  ATR = giriş günü ATR'si (statik; dinamik hal T R239 "daha zekice" ölçüm kolu).
- **Ölçüm çıkış kolları:** R224'ün ilk kısmı: "kar alma %10 (sizin belirleyeceğiniz), ikinci kar alma" (oran ve ikinci
  kâr seviyesi verilmedi; %10 ve ikinci kâr YORUM); R233 zinciri (M R233: RSI 70 reddinde %50, önceki gün düşüğü altı
  kapanışta kalan %50; T son cümle "ilk %50 kar aldığımız RSI70 reddi"); kalan %50 için ikinci "önceki gün düşüğü altı
  kapanış"; harmonik hedef merdiveni (3.2 H); TP1'de %50 ve stop girişe (M R203, G/M R222).
- **İşlem tanımı:** bir kurulum girişi bir işlemdir; parçalar ağırlıklı çıkış fiyatı ve süresiyle tek işlem sayılır.
- **İptal:** giriş ≤ geçersizlik ya da giriş ≥ ilk hedef ise sinyal düşer ve "iptal" yazılır.

### 4.5 Rejim (ölçüm katmanı)

- Şok freni: kısa dönem volatilite / 1 aylık volatilite oranı eşiği geçerse yeni alım yok (T R026; X ve eşik YORUM,
  önceden yazılır).
- Fiyat + volatilite birlikte artış → defansif boyut (T R092, R089, R093; Tansu'nun "mavi çizgi" formülü yok: 21 gün
  getiri ile 21 gün gerçekleşen volatilite değişiminin ikisi de pozitifse, YORUM).
- Corwin–Schultz spread ve sigma: ikisi yüksekse uzak dur (T/M R119; T R252 "Spread yüksek, Sigma yüksek: ... En
  riskli yapı"; yüksek/düşük ile hesaplanır; pencere 21 gün, G R252 "21 Gunluk"). T R252'nin dört sınıfı ayrı kesim:
  yüksek/düşük = spread'in kendi geçmiş ortalamasının üstü/altı (YORUM; Tansu "tarihsel ortalama" ile karşılaştırır).
  Teyit kesimi: fiyat yükselirken spread düşüyorsa sağlıklı, yükseliyorsa kırılgan (T R252). Tansu bunu "işlem kalitesi
  ve likidite risk radarı" diye kullanır, "tek başına al-sat göstergesi olarak değil" (T R252).
- XU100 WMA21: kapanış WMA21 altında ve WMA21 eğimi negatifse "kısa vadeli trend dönüşü henüz teyit edilmiş sayılmaz" (M R258; yazar M, 4.5'in
  trend yönü kolu için ortalama adayı).
- Fiyat ve hacim konumu 252 gün: sol üst köşe (fiyat ≤ 20, hacim ≥ 80) dip adayı (T/G R227).
- Piyasa genişliği: evrende 20 ve 65 günlük yeni yüksek − yeni düşük (NH-NL) (M R118; evrenden hesaplanır).
- Trend yönü: XU100 kapanışı ortalamanın üstü/altı (T R131 "Trend is your friend"; ortalama YORUM) ve XU100 ile
  evren sepetinin rolling korelasyonu (T R091 "HMM yapmanıza gerek yok Koç gibi korelasyon varken"; hangi korelasyon
  olduğu söylenmedi, seriler ve pencere YORUM).
- Mevsimsellik: son 10 yılda ≥ %70 pozitif kapanan aylar ve ay bazlı maruziyet (M R183; %80/%30 kasa örnek).
Bunlar S1 ve S2'de kapılı/kapısız iki kol olarak ölçülür. Parametresi Tansu'dan gelmediği için resmi kola girmez.

## 5. Sınama

### 5.1 Sadakat (getirisiz)

Dedektör, Tansu'nun araç çıktılarındaki kurulumları doğrulama gününde buluyor mu? Ölçüt geometri ve tarih; getiri
değil. Hedefler (defterden):
- H: ISKPL 5 C tarihi (G R018), SMRTG 10 kapanmış kalıp tarihi (G R017), LUKSK D 86,95 / X 73,00 (G R012),
  SOKE D 12,53 = XA 0,786 (G R012), SAYAS X≈20,6 A≈145 B≈68 C≈122 D≈47 (G R014), KAPLM (G R013), DGATE D 49,66
  (G R008), KRPLS üç D (G R008).
  DOAS Kelebek: A 209,10, X 170,10, D 159,40 = XA 1,272 uzantısı 159,49, "TAMAMLANDI" (G R250; tweet 2026-09-06).
- E: BRYAT Fibo %64,3 (G R199), ALKA düzeltme −%39,3 (G R241), ENJSA dalga 4 %54 (G R193), CWENE Point 0 33,10,
  Point 1 48,30, Dalga 2 ≈ 35 ve talep bölgesi 32,5–36 (T R261; 2026-08-30).
- K: AKFIS AL tetiği 2026-09-03 ve öncesi (G R253).
- S3: VAKBN–GARAN "YENI AL SINYALI | VAKBN AL" (G R251; 2026-09-05 son gün): ölçüt yön (VAKBN alınır) ve tarih.
  Z değerleri (−3,108; önceki −3,404) Tansu'nun Z formülü ve penceresi bilinmediği için ±0,5 toleransla bilgi
  olarak karşılaştırılır (YORUM).
- S: KRDMD 17.12.2025 → 14.01.2026, 20 gün, ort. %0,64 (G R127).
- Bölge: FROTO demand 74,75–76,70 teyit 2026-08-14, DOAS 165,59–173,00, TTKOM 49,05–51,30 (G R041, R042, R043).
Ayar adayları önceden yazılır; plasebo (rastgele tarih) karşılaştırması yapılır. Sonuç yalnız etiketi belirler.

### 5.2 Sayım, kayıt, ölçüm

**Kendini yenileyen sistem (ölçüm kolu):** Tansu "Öyle bir matematiksel yapı kurun ki sistem sürekli kendini
yenilesin" der (T/M R122) ve EMA'yı "walk forward le optimzie" eder (M/T R138). Önceden yazılmış kural ile çelişmez,
yeter ki yenileme kuralı da önceden yazılsın: S2'de her yılın ilk işlem günü, ön kayıtlı aday ayarlardan (4.1 eşikleri,
pivot k, sıkışma toleransı) yalnız o güne kadarki son 3 yılın verisinde en iyi net kâr / en büyük düşüş oranını veren
seçilir ve o yıl kullanılır. Bu kol bakış ileri taşımaz (geçmiş pencere). Resmi kol sabit ayarla kalır; yenileyen kol
ölçümde yan yana raporlanır. (S1 ve S3 zaten kendini yeniler: aylık sıralama, yıllık çift seçimi.)

Sürüm 4'teki kurallar aynen geçerlidir: getirisiz sayım koşusu; kayıt sadakat ve sayımdan sonra, ilk getiri koşusundan
önce; yeni hatların gerçek getirisi kayıttan önce görülmez; her yeni kod hash'i için boru hattı denetimi (yanlış kabul
≤ %5, `_resmi_bitti` istisnası kalkar); ölçüm kolu hiç resmi olmaz, kol kimliği içerik özetidir (`olcum_kolu=true`
olan kimlik resmi yapılamaz); ölçüm kodu `olcum.py` (HASH_DISI), hash içi kod onu import etmez.

## 6. Rapor ve kart

Rapor hat başına bölümdür. S2 için Tansu'nun tablo biçimi (G R012): Hisse, Tarayıcı, Durum, Tepki, Hedef, Giriş,
Geçersizlik; tarayıcı başına sonuçlar "ölçüm" başlığında. Başarısız kurulumlar da listelenir (T R014 "Her gartley
çalışmaz", R087 "Her zaman çalışmaz"). Kazanma oranı tek ölçüt değildir; net kâr / en büyük düşüş yazılır (M R140,
T R234). Ayrıca kapanış getirisi yanında dönem içi en yüksek getiri (DEY) yazılır (T R074, G R120 tablosu); sermaye
eğrisinin sakinliği: yıllık volatilite ve en büyük düşüş kural ile K2 yan yana (T/M R115, M/T R138: gövde M, son
cümle T). Aday günlüğü (T R255 "Backtest yapın ... sonraki 1, 3 ve 5 günde ne olmuş bakın"; "İşlem günlüğü
oluşturun. Aday tarihi → giriş → neden girdik → invalidation → TP → sonuç → maksimum olumlu/olumsuz hareket"): her
aday için tarayıcı, 1/3/5 gün getirisi, giriş, geçersizlik, hedef, sonuç, MFE ve MAE yazılır; aday tipi başına
karşılaştırma ölçüm başlığındadır (T R255 "Hangi aday tipi para kazandırıyor?"). Akşam kartı o gün durum değiştiren
kurulumları yazar; dil "kural sağlandı".

## 7. Uygulama sırası (öneri; biletler ayrıca)

1. Yapı taşları: pivot, Fibonacci, FVG, talep bölgesi (günlük + haftalık); `test_gelecek.py` genişler.
2. Sadakat koşuları (5.1), getirisiz. Sonuç Levent'e gösterilir.
3. S1 (en basit; sadakat gerektirmez, kural tam).
4. S2 tarayıcıları H (Three Drives dahil), E, S, F, K; ortak yönetim (4.4); sayım koşusu.
5. Ölçüm yolu (`olcum.py`) ve rejim kolları.
6. K1 tanımları, AILELER, `KOD_DOSYALARI`, rapor.
7. Boru hattı denetimi; kayıt; resmi koşu (Levent'e sorulur); ölçüm.

## 8. Bu sürümde resmi olmayanlar ve neden

| Fikir (kaynak) | Durum | Neden |
|---|---|---|
| Değerleme sistemi: çarpanlar 3×3, basit model, DCF, %60/%40 (T R062, R064, R068, R151, R158, R166) | İkinci dalga, önce veri işi | Bilanço verisi yok (2. bölüm). Tansu'nun en çok sahiplendiği hatlardan biri; ilk iş İş Yatırım mali tablo kaynağı. Tansu ayrıca "bistte artık bir önemi yok" diyor (T R240): çelişki raporda yazılır. |
| DCF altyapısı: FCFF/FCFE/DDM, WACC üç yöntem, Damodaran total beta, CoE, terminal değer, duyarlılık, ters DCF, güvenlik marjı %20–30 (T R070, R153, R154, M R155, T/M R158, M R159, T R160, G R161, M R163, T R164, G-dış R165) | İkinci dalga (değerleme altyapısı) | Değerlemenin %40 ayağıdır (T R064, R151, R158). Bilanço verisi ister. |
| Hibrit alarm: değerleme potansiyeli + teknik tetik (T R166) | İkinci dalga | Değerlemeye bağlı. |
| Bilanço kalite filtreleri: maddi duran varlık artışı → fiyat (T R059), dönen varlık/KVB < 1 → bedelli riski (T R060), özkaynak artışı (T R057), borç büyümesi vs ciro (M R134, T R135), nakit/piyasa değeri (M R010), HBK U dönüşü (T R133), Merton DD/EDF (T R061), regresyonla olması gereken değer / beklenen F/K (T R058, R066), skor kartı ve sekmeler (T/G R067), proje cirosu bugünkü değeri (T R069), işletme kriterleri (M R046, M R240), Dupont (T R002) | İkinci dalga (değerlemeyle) | Bilanço verisi. R059 "Göz ardı etmeyin" ve R060 kural tam: veri gelince ilk sınanacak filtreler. |
| Konveks rotasyon (T/M R229) | İkinci dalga | 2. adım tarihsel F/K ister (bilanço); 1. adım makro döngü kuralsız. |
| Klasik formasyonlar: takoz, TOBO, OBO, bayrak, flama (T R004, R006, R007), ikili dip (M R236), OBO kuralı (G-dış R219) | İkinci dalga tarayıcı | Tansu "uygulamanın ilk algoritmaları" listesinde sayıyor (R004) ama kural vermedi; R219 dış kaynak. Long-only: OBO yalnız çıkış uyarısı olur. S2'ye tarayıcı eklemek m'yi artırmaz, ama kuralsız tarayıcı tümüyle bizim tanımımız olur; ikinci dalgada standart tanımla "yorum" tarayıcısı olarak, sadakat hedefi olmadan eklenir. |
| Bant kuyruğu tepki alımı: −2/−3 SE (T R053), ±1/2 SD bantları (M R187) | İkinci dalga tarayıcı | Tansu "tepki alımı fırsatı" diyor ama giriş/çıkış ve pencere yok; R187 IV ister (gerçekleşen volatilite vekili YORUM). |
| Momentum × faaliyet nakit akışı 5×5 (T R022), TOPSIS (T R145, R179), DEA/Convex Hull (T R175, R178), PD/DD+ROE (M R144) | İkinci dalga | Bilanço verisi. |
| Volatilite harvesti (T R030), rebalancing (T R078), Markowitz + volatilite trading (T/M R110) | Ölçüm (S1 portföy katmanı) | Varlık çifti ve oran verilmedi; Tansu'nun kendi rebalancing örneği pasifin gerisinde (G R078: %26,76 / %27,81). |
| VRP, implied move, IV kesişimi (T R028, R029, M R031) | Dışarıda | Opsiyon IV yok (BIST hisse opsiyonu verisi yok). |
| VWAP / POC / VAH / VAL, denge-dengesizlik (T R186, M R190, T R024) | Dışarıda | Gün içi veri yok; günlük vekil Tansu'nun mantığını taşımaz. |
| BIST100 + VIX beş adım (G-dış R209, T/M R210) | Dışarıda | VIX ve açılış (Heikin Ashi) yok. |
| Kapitülasyon üçlüsü (T/M R226) | Ölçüm, iki koşulla | OBI emir defteri ister; istatistiksel sapma ve fiyat-hacim konumu kurulabilir. |
| Mum formasyonları: engulfing (G R023), tweezer (T R025), gravestone (T R130), çekiç/sabah yıldızı (T R137), advance block (M R042) | Ölçüm, AOF'lu yaklaşık | Açılış yok. |
| Gizli pozitif uyumsuzluk (T/M R116, T R117, T R136) | Ölçüm (06.10) | Görselde parametre var: "Swing=15 sol-only, MinGap=15" (G R116, R117). Osilatör kimliği gizli ("pek bilinen birşey değil", T R136, Tansu'ya sorulacak); ölçümde RSI(14) ile (YORUM), fiyat yükselen dip + osilatör alçalan dip. İki dip arası 10–30 bar; 70 bar üstü sayılmaz (T X4 "Genellikle 10 ile 30 bar arası mesafeler en sağlıklı sinyali verir"); günlük grafik (T X5). Kaynak `ham-yapistirmalar-3.md` Ek. |
| Fincan-kulp (T/M R114) | Resmi (S2 F tarayıcısı, 06.10) | Önceki gerekçe yanlıştı: hedef tabanı kırılma çizgisidir (sol ağız), 300,75 + (300,75 − 212,20) = 389,30 birebir tutar (`kural-yok-inceleme.md` 22–23). S2 tek hipotez olduğu için m artmaz. |
| Kanal alt bandı, düşen direnç kırılımı + retest (T R004, R085, G R075, R087, T R194, M R195) | Ölçüm (S2'de kanal ve kırılım teyidi kolu) | Tansu bunları formasyonun bağlamı olarak kullanıyor (R085); ayrı tarayıcı yerine teyit kolu. FVG'li kırılım-retest-teyit hali ayrı K tarayıcısıdır (3.2, T R254). |
| X–B trend çizgisi kırılımı (T R013, G R008) | Ölçüm (H tarayıcısında ikinci giriş) | Tansu "trade yapmanın bir yolu da" diyor; yön kısa tarafta açığa satış. |
| Hacim teyidi: geniş gövde/hacim anomalisi (T R238), OBV (G-dış R196), "Hacimli kırılım" (M R124) | Ölçüm (teyit kolu) | Eşik yok; açılış yok (gövde). |
| Fiili dolaşım < %30 (T R083, R035, R036) | Ölçüm (S1, S2 kesimi) | Veri var; Tansu eşik dışında kural vermedi. |
| Mevsimsellik ≥ %70 ay (M R183) | Ölçüm (rejim) | Yazar M; Tansu "Biraz düşünelim". |
| A/D–EMA3 (M/T R138, T R139): AD > Ref(EMA(AD,3),1) ise pozisyon, değilse nakit; APO = EMA10 − EMA40 ortalamaya dönüş (T R156, görselden "Fast10DayEMA", "Slow40DayEMA") | Ölçüm (06.10) | Kural görsel ve öbür kayıttan tamamlandı (`kural-yok-inceleme.md`): giriş operatörü R138 görselinden, OPT1 = 3 (T R139); çıkış operatörü yazılı değil (tersi, YORUM). Tansu'nun ISCTR sonucu: %19,1 / B&H %10,8 (G R138). APO eşiği Tansu'da yok (±10 dış kaynak, YORUM). Tansu'nun ana sistemi sayılmaz ("can sıkıntısından yazdım", R156), bu yüzden resmi değil. |
| RSI 30 (M R233), Williams %R 30 dk (M R170), HalfTrend (T R148), ML lojistik (T R234) | Dışarıda (ilk dalga) | Tansu'nun ana sistemi değil ("İndikatör cart curt hikaye", T R145); R170 gün içi; R148 eşik yok; R234 "henüz yazdığım". |
| Elliott dalga 4 (T R205), 5+3 ve Fibonacci günleri (G-dış R207) | Ölçüm (E tarayıcısında dalga 4 kolu) | R205 kuralı tam; R207 dış kaynak. |
| Çoklu aralık Fibonacci kümeleri (G-dış R217), confluence ilkesi (T R040, G-dış R208) | Ölçüm (bölge kalitesi) | Bağımsızlık ölçüsü yok; aynı fiyat serisinden türer. |
| Medyan temelli çalışma (T R001), medyan kanal (T R244) | Ölçüm (S2 bölge alternatifi) | Pencere ve kural yok. |
| Sektör rotasyonu zinciri (T R002, G R032, T/M R232) | Ölçüm (S1 filtresi) | Sektör bugünkü sınıflama (yanlılık); Tansu sonuç vermedi. |
| "Volatilite işi" (T R102 "en en sevdiğim 2 sistemden birisi İlki volatilite işi") | Parçalı | Tansu hangi sistem olduğunu söylemiyor. Kayıtlardaki volatilite sistemleri: harvesti (T R030, ölçüm), rejim/defansif (T R092, R077, ölçüm 4.5), VRP (T R028, M R031, dışarıda: IV yok). Tansu'nun "sistemim" dediği tek volatilite kaydı R092'dir (pozisyonu kapatıp defansife geçme); "mavi çizgi" formülü gizli olduğu için resmi kola giremez, ölçümde vekil formülle sınanır (4.5). |
| Tansu'nun YSA momentumu (T R137), Optimal Momentum+ (T R121), pre-signal oku (T R125), gizli "xxxx" metriği (T R049) | Dışarıda | Formül gizli ya da tanımsız. YSA'nın yerine Tansu'nun kendi BIST testindeki ölçü (R120) kullanılır (3.1). |
| GARCH (T R097), ARIMA grid search (T R174), "ana frekans" (T/M R122), finans mühendisliği ile destek/direnç (T R107), risk of ruin, kurtosis (M R185) | Dışarıda | Araç ya da araştırma fikri; işlem kuralı yok. |
| Weinstein 4 evre (M R108), DMA kanal eğimi ve evreler (G-dış R216), piyasa evreleri ve birikim anlatısı (G-dış R235, T R237), fat tail (M R220), BIST_VOL gülümsemesi (T R094), hacimle mal boşaltma/toplama (T/M R119) | Dışarıda | Kural ve parametre yok ("X haftalık"). |
| Mum ve gösterge yorumları: inverted hammer (T R241), HIKKAKE (M R193), uzun yeşil mumun yüksek yakın kapanışı (M R124), MACD/RSI panelleri (G R168, M R221; ADX ve CMF Tansu'nun T R137 3. aşamasıdır, S1 ölçümünde), RSI kırılımı (G R008), %5–10 kesişim primi (M R105), 0,786'nın direnç olarak kullanımı (M R126), "hissenin oranı %50'den fazla" (M R110, belirsiz) | Dışarıda | Açılış yok ya da kural yok; R110 cümlesi anlaşılmıyor. |
| Kural taşımayan yan cümleler: yatay sıkışma/üçgen görüntüsü (G R008), bant genişliği ve VaR (T R053), sell yönlü AB=CD ile kırılım çatışması (T R076), dinamik hedef kalibrasyonu (R090, başka hesabın cevabı), Mark-to-Market (M/T R099; rapor zaten kapanış değeriyle), düşük hacim uyarısı / "Liderleri Takip Edin" / mikro-makro çelişkisi (M R118), EMA'ların dinamik desteğe dönmesi (M R128), likidite süpürme ve önce üst dirençleri test (M R129), HBK'nın evrensel ölçü olması (T R133), sektörel döngüler (M R183), EMA kümesi üstü kalıcılık (M R192) | Dışarıda | Eşik ve kural yok: M cümleleri ya da kuralsız T gözlemleri (T R053 bant genişliği, T R076, T R133). R118 NH-NL ve R192 hedef mantığı tasarımda (4.5, 3.2). |
| Kalan yan fikirler: R077 yeşil üçgen sinyalleri (G, formül yok), ortalamadan uzaklaşınca soğuma/re-test (M R128), TP2'yi hacimli mumla geçince yeni trend (M R203), konsantrasyon/kümelenme COT (T/M R227; açık pozisyon verisi yok), "Fading the Gap" kısa pozisyon (M R243; açığa satış yok), büyük mumları incelemek (T R243) | Dışarıda | Formül, veri ya da long-only uyumu yok. |
| Trailing stop'a geçiş için risk/ödül hedefi (M R233) | Dışarıda | Sayı verilmemiş; S2 iz süren modu T R224/R239 ile tanımlı (4.4). |
| Ürün hedefi: tek tuş, LLM/NLP ile faaliyet raporundan veri (T R065), Excel çıktıları (R154, R163), infografik akış (R056) | Kapsam dışı | Ürün hedefi, strateji kuralı değil. TANSU'nun sinyal sistemi kapsamı dışında. |
| Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (R045, R052, M R162, R173, R177, R200, M R231) | Kapsam dışı | Strateji değil; ders ya da kurumsal çalışma. |
| 80–100 haftalık yatay hisse, dipte bekleme (T R246 "Aslında en temiz strateji bulacaksın 80-100 haftalık yatay giden bir hisse dibinde oturup bekleyeceksin.") | Ölçüm (06.10) | Tansu'nun "en temiz strateji" dediği fikir; ama yataylık, dip ve çıkış tanımı yok ("Yazalım o zaman taramasını" der, tarama paylaşılmadı). Ölçüm tanımı (YORUM): haftalık kapanışlarla son 80 ve 100 haftada (en yüksek − en düşük) / ortalama ≤ %60 ve doğrusal eğim |yıllık| ≤ %10; giriş kapanış bandın alt %20'sinde; çıkış bandın üst %20'si (T X7 2025: "kanalın alt bandına yaklaşıldığında hisse almak, üst banda yaklaşıldığında ise satmaktır"; "yaklaşma" %20 YORUM) ya da kapanış bant dibinin %5 altı (T X7 "mutlaka stop seviyeleri belirlemek"; %5 YORUM). Tansu'ya sorulacak: yataylık ölçüsü ve çıkış. Kural gelirse S2'ye tarayıcı olarak girer (m artmaz). K ile fark: K'de Tansu aşama sırasını verdi (T R254) ve araç çıktısı ile sadakat hedefi var (G R253 AKFIS); R246'da tarama paylaşılmadı, hedef de yok. |
| Kanal alt bandı teması (G R245 AEFES: "Lookback: 120 ... Üst/Alt temas: 3/3"), düşen üst sınır kırılımı ve retest (T R247 "Güzer retest var", G R248 kırılım mumu) | Ölçüm (kanal ve kırılım teyidi kolu) | Yukarıdaki kanal satırına ek: lookback 120 bar ve üst/alt en az 3 temas G R245'ten. FVG'li kırılım-retest-teyit sırası bu satırın dışındadır: o K tarayıcısıdır (3.2, resmi). Bu satırda kalan: kanal teması ve FVG'siz kırılım-retest. |
| BOM sinyali (T R263 "BOM sinyalinin geldiği yerde şartlar da müsait ise çok etkili olabileceğine dair ilk kanıtlar gelmeye başladı") | Dışarıda (kural gizli) | Kısmen biliniyor (07.10 X): BOM bir swing dip pivotudur ("noktanin gerçekten swing lowpivot olduğundan emin olmak için X bar kadar öteleyerek kodladım", T X1); görselde talep bölgesindeki yükselen dipte ("D-HL") çıkar. Bu, 4.1 talep bölgesi + 4.2 pivot ile zaten S2'nin bölge kapısında; BOM'un kendi koşulu ve "şartlar" yok; Tansu "hala geliştirilmeye açık bir sistem" der. Tansu'ya sorulacaklar listesine girer (`kural-yok-inceleme.md` H1). |
| CWENE skewness örneği ve Cornish-Fisher VaR (T R260) | Ölçüm (S1 skewness kolu, 3.1) ve bilgi | VaR güven düzeyi verilmedi; boyut kuralına bağlanmadı. |
| XU100 günlük yorumları: seviyeler, "BEKLE ve TEYİT ARA", nakit esnekliği, katılım zayıflığı (M R257, M R258) | Bilgi; WMA21 ölçüm (4.5) | Yazar M; o güne özgü seviye listesi işlem kuralı değil. Genişlik kolu 4.5 NH-NL'de. |
| "Ahengin uyumu" demand/toplama ve panel uyumu (T R259), arbitraj başlığı (T R251 üst tweet), RT karşılığı formasyon (T R245) | Bilgi | Metinde kural yok; görsel etiketi 4.1 talep bölgesiyle aynı tema. |
| Felsefe ve ölçüm ilkeleri (R099, R109, R111, R140, R157, R171, R172, R210, …) | Tasarımın kendisi | Kural koda dökülür, duygusuz, backtest zorunlu: TASARIM'ın ilkeleri. |

## 9. Açık sorular (Claude'un önerisiyle)

1. S2 momentum kapısı "S1 sıralamasında üst yarı" yorumdur. Öneri: kalsın; ölçümde kapısız kol.
2. (Kapandı, sürüm 5.1: kalan %50 R224 harfiyen, 2 ATR acil stop; SMA250 G-dış R212'den. İkinci "önceki gün düşüğü"
   kapanışı ölçüm kolu.)
3. FVG: R199 doldurulmamış ister, R243 doldurulmuş sonrası girişi de anlatır. Öneri: resmi kol R199 (araç çıktısı
   "FVG TEMAS" ile uyumlu); R243 ölçüm.
4. Değerleme için veri işi (İş Yatırım mali tablo) ikinci dalganın ilk bileti olsun mu? Öneri: evet.
