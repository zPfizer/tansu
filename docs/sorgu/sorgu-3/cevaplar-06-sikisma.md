# Cevaplar 06: EMA sıkışması

Doğrulama (OLGU) için kullanılan veri: İş Yatırım `HisseTekil` (KRDMD, ham `HG_*` ve `HGDG_*`, 2022–2026) ve Yahoo `KRDMD.IS` (yfinance 1.7.0, `auto_adjust` False/True). Toplam 5 istek. Görsel: `gorsel-paket-67-krdmd-...jpg` (piksel okuması: 0 → y=525, 10 → y=458,5; ±0,3 birim belirsizlik).

Ana bulgu (06-002, 06-004, 06-005, 06-021 için): raw kapanıştan `ewm(span, adjust=False)` ile EMA20/50/100/200 hesaplanınca 09.04.2026 değerleri lejanttakiyle birebir çıkıyor (31,92 / 30,74 / 29,58 / 28,43; son kapanış 36,68). Oran = (max EMA − min EMA) / **EMA200**. Kanıtlar: (a) 17.12.2025–14.01.2026 tam 20 bar, ortalama %0,638; (b) grafik sonu oranı %12,27 (görselde ≈12,1); (c) Mart tepesi %12,66 (görselde 12,63). Payda Close olursa son oran %9,51 ve Mart tepesi %11,26 çıkar; EMA ortalaması olursa %11,56 ve %11,97. CV (%4,31) elenir.

**06-001** — CEVAPLI — KURALLAR 3 "birinci el" demeyi oranın kendisi için değil, görseldeki eşik çizgisi (`Eşik %1.2` Ratio panelinde) ve başlık için söylüyor. Formül ayrıca "sadakat kontrolüyle" diye ayrılmış (KURALLAR 3, 4). Formül artık doğrulandı (bkz. ana bulgu).

**06-002** — OLGU — Doğrulandı: payda EMA200 (= en düşük EMA). Close ile 12.12.2025–14.01.2026 dönemi aynı kalır ama ortalama %0,63, son oran %9,5 ve Mart tepesi %11,3 olur; görselle uyuşmaz. aileler.py'nin `/Close` paydası yanlış. Fix: KURALLAR 3'e "oran = (maxEMA − minEMA)/EMA200, doğrulandı" yaz.

**06-003** — EKSİK — KURALLAR 4 "birden çok aday" diyor, aday sayısı yok. Tek sayı yerine 130 barlık eğri var (çok bilgi), bu yüzden aşırı uydurma riski küçük. Fix (YORUM): aday listesini önceden ≤5 yaz {Close, EMA200, EMA ortalaması, EMA medyanı, CV}; ölçüt: dönem ortalaması + grafik sonu değeri + Mart tepesi.

**06-004** — OLGU — Doğrulandı. EMA200 paydası: dönem içi oran min %0,34, max %1,01 ("~0,5–1" ile uyumlu); Close paydası %0,33–0,97. CV ortalaması %0,25: 0,64'ü vermez. ATR-normal oran birimsiz, % üretmez; denenmedi.

**06-005** — OLGU — Önerme yanlış: lejant değerleri 09.04.2026 grafik sonu, ama Ratio panelinin son noktası da aynı gün (≈%12,1). Bu iki sayı payda ayrımı için yeter (Close %9,5; EMA200 %12,27). Not: B-momentum 1 "formül olmadan yeniden üretilemez" demişti; artık üretilebiliyor.

**06-006** — OLGU — Doğrulandı: 17.12.2025–14.01.2026 arası tam 20 işlem barı (İş Yatırım ve Yahoo ikisinde de). Ama 16.12.2025 barı sınırda: oran 1,193–1,205 (veri başlangıcına göre), yani 21 bar da çıkabilir. Fix (YORUM): sadakat ölçütü "20 bar ±1, ortalama %0,64 ±0,02".

**06-007** — EKSİK — Görselde "ardışık" yazmıyor; "Min 3 gün" yazıyor. "Ardışık" B-momentum'un okumasıdır (ikinci el). KRDMD'de 20 bar kesintisiz, yani çelişki yok. Fix: KURALLAR 3'e "ardışık (YORUM)" yaz. aileler.py `rolling(10).sum()>=3` eski prototiptir, silinecek (TASARIM 7.1, C7).

**06-008** — CEVAPLI — 10 sayısı Tansu'dan gelmiyor (kaynak yok). KURALLAR 3 onu "Giriş (YORUM)" diye etiketliyor; her YORUM deneme sayısına girer (KURALLAR 1.5, TASARIM 5.11). aileler.py'deki rolling(10) ayrı bir parametredir, birbirine bağlı değil.

**06-009** — EKSİK — "Bitti" tanımı yazılı değil. KRDMD'de dönem tek parça: 01-14 oran 1,01, 01-15 oran 1,28. Fix (YORUM): dönem = ardışık oran ≤ eşik barları; ilk oran > eşik barı dönemi bitirir; geri dönerse yeni dönem.

**06-010** — EKSİK — Histerezis yok, kaynak da yok. Dalgalanma dönemi böler, yeni dönem yeni 10 günlük pencere açar. İşlem sayısını TASARIM 5.3 sınırlar (pozisyon açıkken yeni sinyal sayılmaz), ama "dönem sayısı" şişer. Fix: raporda sayım birimi "işlem", "dönem" değil.

**06-011** — CEVAPLI — Sorgu-2 S2-38: "130 mum kural değil, Tansu'nun ekran penceresi". Sistem tüm geçmişe bakar; sadakat KRDMD'de 130 barlık pencerede kontrol edilir (orada tek dönem bulunur, "1 periyot" ile uyumlu).

**06-012** — EKSİK — TASARIM sessiz. Ölçüm: veri başlangıcı 2025-01 ise EMA200 kayması küçük görünse de dönem ortalaması %0,64 → %0,82 oluyor; 2023-06'da %0,64, 2024-06'da %0,82. Tohum ağırlığı 0,995^n: 200 barda %13, 500 barda %0,7. Fix (YORUM): ilk sinyal ≥500 bar sonra (2015 başlangıçlı veriyle ≈ 2017); eleme gün sayısı raporda yazılır.

**06-013** — OLGU — Doğrulandı: `adjust=False` ile SMA tohumlu EMA 1084 barlık seride aynı çıkıyor (EMA200 28,435; dönem ortalaması 0,638 ikisinde de). Tansu'nun lejantı (28,43/28,44) iki yöntemle de örtüşüyor. Uzun seride fark yok; kısa seride önemli (bkz. 06-012, 06-014).

**06-014** — OLGU — Ölçüldü. Veri başlangıcına göre dönem ortalaması: 2018–2022 %0,637–0,638; 2023-01 %0,641; 2023-10 %0,686; 2024-01 %0,657; 2025-01 %0,824. 16.12.2025 oranı 1,193 → 1,613 arası oynuyor (dönem başlangıcı kayıyor). Fix: veri başlangıcı sabit (2015-01-02) ve rapora yazılır; sadakat kontrolü ≥3 yıl veriyle yapılır.

**06-015** — CEVAPLI — TASARIM 5.1: ham fiyat + olay tablosu; göstergeler düzeltilmiş fiyattan (S2-13). Düzeltme katsayısı kodda bir kez uygulanır.

**06-016** — CEVAPLI — TASARIM 5.1: göstergeler ve getiriler düzeltilmiş seride; ham yalnız likidite ve tavan/taban için. Kırılım seviyesi (dönem tepesi) ve EMA aynı düzeltilmiş seriden gelir, ölçek farkı yok. Yahoo zaten kullanılmaz (TASARIM 4).

**06-017** — CEVAPLI — TASARIM 5.1: karantina (limit + %0,5 üstü açıklanamayan sıçrama), HGDG ile karşılaştırma, borsapy ile tam karşılaştırma.

**06-018** — OLGU — Ölçüldü (yfinance 1.7.0): KRDMD için `auto_adjust` False/True aynı kapanışı (36,68), aynı EMA'ları ve ortalamayı (0,638/0,637) verir; sonuç sürüme bağlı değil. Fix: sadakat kaydına yfinance sürümü yazılsın.

**06-019** — OLGU — Doğrulandı: Yahoo KRDMD.IS ve İş Yatırım ikisi de 20 barlık dönemi, son kapanış 36,68'i ve aynı EMA'ları veriyor. veri-kaynaklari.md KRDMD'yi ayrıca incelememişti (yalnız CCOLA, FENER, HEKTS, AYGAZ, TUKAS, EUREN, THYAO).

**06-020** — EKSİK — Tek örnek, ama tek sayı değil: 130 barlık Ratio eğrisi var. Ölçüt "ortalama %0,64" ile sınırlı kalırsa zayıf. Fix: KURALLAR 4'e ek kontrol noktaları: 09.04.2026 oranı ≈%12,1, Mart 2026 tepesi ≈%12,6, 16.12.2025 oranı ≈ eşik. İkinci bağımsız örnek yok (ICBCT oranı yalnız bir noktada, bkz. 06-094).

**06-021** — OLGU — Ölçüldü: tek 0,64 sayısı Close (0,63–0,65) ve EMA200 (0,64) için ayırt etmez; ama grafik sonu (%9,5 / %11,6 / %12,3) ve Mart tepesi (%11,3 / %12,0 / %12,7) ayırt eder, CV'yi tamamen eler. Fix: bkz. 06-020.

**06-022** — CEVAPLI — B-momentum 1 "Kanıt: tek KRDMD örneği, seçilmiş pozitif"; başarısız sıkışma örneği yok (kaynak yok). Sadakat kontrolü getiriye bakmaz (KURALLAR 4), bu yüzden etkisi sınırlı.

**06-023** — CEVAPLI — TASARIM 3 "yalnız alış yönü" ve S2-39 "aşağı kırılım girilmez". BEAR/CONFLICT sayaçları Tansu'nun aracında aşağı yön de olduğuna işaret eder (YORUM); ICBCT kuralı gizli, "kodlanamaz" (KURALLAR 2'de X).

**06-024** — ZAYIF SORU — KURALLAR 3 yalnız KRDMD'ye dayanır; ICBCT parametreleri uygulanmaz. Not: ICBCT lejant değerlerinden bant %1,04 (bkz. 06-094), aynı aracı destekler ama kanıt değildir.

**06-025** — EKSİK — ICBCT'de "Pre Sig" üçgeni `AKTİF 3g` kutusunun içinde, yani Tansu'nun Pre Signal'i sıkışma sürerken (3. günde) çıkıyor; bizim giriş "bitişten sonra kırılım" (YORUM). KURALLAR 3 bunu zaten YORUM diye etiketliyor, ama Tansu'nun sinyaliyle farkı yazılı değil. Fix: KURALLAR 3'e "Tansu'nun Pre Signal'i sıkışma sürerken; bizim tetik farklı (YORUM)" notu.

**06-026** — ZAYIF SORU — "%5" ikinci el iddia, sistem hedefi değil. BIST tavan/tabanı 13.03.2020'den beri ±%10 (veri-kaynaklari 5), bir günde %5 mümkün.

**06-027** — EKSİK — "En yüksek fiyat" tanımsız. KRDMD'de High ile dönem tepesi 29,00; Close ile 28,24. High: sinyal 19.01.2026 (kapanış 29,10), giriş 20.01 AOF 28,57. Close: sinyal 16.01 (28,64), giriş 19.01 AOF 29,24. Fix (YORUM): dönem içi en yüksek High; dönem tepesi 20 günlük High ile aynı değil (dönem süresi değişken).

**06-028** — CEVAPLI — TASARIM 1 (C7) ön deneme kodu kanıt değil, 7.1 Yahoo'lu ön deneme kodu kaldırılır, "kod belgeye uyar". Sınanan tanım KURALLAR 3; prototipin sonuçları geçersiz.

**06-029** — EKSİK — Doğru: dönem sürerken kırılım sinyal vermez. KRDMD'de oran 15.01'de eşiği geçti, kırılım 19.01'de oldu. Yavaş EMA yüzünden bazı kırılımlar kaçar. Fix (YORUM): bunu "bilinen sınır" diye KURALLAR 3'e yaz; ölçmek için sıklık raporunda kaç kırılımın dönem sürerken olduğunu say.

**06-030** — ZAYIF SORU — "Bitti" yalnız orana bağlı (ilk oran > %1,2), fiyata bağlı değil; döngü yok. KRDMD: bitiş 15.01 (oran 1,28), fiyat kırılımı 19.01.

**06-031** — CEVAPLI — 10 gün YORUM'dur, kaynak yok. KURALLAR 4: YORUM'u sonuca bakarak seçmek yasak; TASARIM 5.10 sağlamlık ızgarası, 5.11 deneme günlüğü. (Ek parametre kaydı eksik, bkz. 06-072.)

**06-032** — EKSİK — TASARIM 5.3: pozisyon açıkken yeni sinyal sayılmaz. Stopla çıkıldıktan sonra aynı dönemin kalan günlerinde yeniden giriş yazılı değil. Fix (YORUM): bir sıkışma döneminde en fazla bir giriş.

**06-033** — CEVAPLI — Karar günü t kapanışında verilir, işlem ertesi AOF (TASARIM 5.3); sınama ve canlı aynı Adım fonksiyonunu kullanır (TASARIM 4, A5), gelecek barı göremez. Dönem tepesi bitişe kadarki barlardan hesaplanır.

**06-034** — ZAYIF SORU — %0,64 ve 20 gün yalnız sadakat çıktısıdır; giriş filtresi olarak kullanılmıyor (KURALLAR 3 ve 4).

**06-035** — CEVAPLI — Giriş dönem bittikten sonra aranır (KURALLAR 3); başlangıç günü sinyal günü belirlemez. Sinyal günü = bitiş sonrası ilk kapanış > dönem tepesi.

**06-036** — CEVAPLI — Hedef anlam KURALLAR 3: bitişten sonra kırılım. aileler.py eski prototip, kaldırılır (TASARIM 7.1).

**06-037** — CEVAPLI — Hacim koşulu Tansu'nun KRDMD görselinde yok (hacim paneli var, eşik/etiket yok; B-momentum 1). 1,5× ve 20 günlük medyan prototipin icadı, kaynak yok.

**06-038** — CEVAPLI — gp-64 EMA sıkışması değil (düşen trend + EMA5/8/13); gp-68 hacimli kırılım ikinci el. TASARIM 2 (P5): aileler "Tansu'nun sistemi" diye sunulmaz, "esinlenen bizim yorumumuz".

**06-039** — ZAYIF SORU — Hacim koşulu katalogda yok; 1,5× ve medyan kataloğa girmediği için etiket gerekmiyor. Sorgu-2 F bölümü hacmi hiç anmıyor (bkz. 06-085).

**06-040** — ZAYIF SORU — Hacimsiz kuralda sahte kırılım artar varsayımı sınanmamış. Başarı fazla getiriyle ölçülür (TASARIM 5.12); sahte kırılım ayrı kabul ölçütü değil.

**06-041** — ZAYIF SORU — Hacim koşulu yok.

**06-042** — OLGU — Aile hacim kullanmıyor. Ama TASARIM 5.1'in açık sorusu çözüldü: İş Yatırım `HG_HACIM` TL cinsinden (KRDMD 16.12.2025: 2,80 milyar TL; /AOF = 99,8 milyon lot, grafikteki ~100M çubukla uyumlu). Düzeltilmiş `HGDG_HACIM` ayrıca var. Fix: 5.1'e "HACIM = TL (doğrulandı)" yaz.

**06-043** — ZAYIF SORU — Hacim koşulu yok.

**06-044** — CEVAPLI — TASARIM 5.3 ve S2-7: kaynakta açılış yok, işlem ertesi AOF'tan; %0,1/0,3/0,5 masraf "açılışta kovalama"yı da kapsar (5.4).

**06-045** — EKSİK — Fark dağılımı raporda yok. Örnek KRDMD: kapanış 29,10 → ertesi AOF 28,57 (−%1,8). Fix: rapora "sinyal kapanışı ile giriş AOF'u arası fark" medyanı ve %95 değeri.

**06-046** — CEVAPLI — TASARIM 5.3 (M4, S2-9): kilitli tavanda giriş yok, işlem sayılmaz.

**06-047** — CEVAPLI — TASARIM 5.2: evren = piyasa değeri en büyük 100, 60 günlük medyan TL işlem tutarı şartı; 5.4: pozisyon ≤ son 10 günün medyan TL tutarının %2'si.

**06-048** — ZAYIF SORU — EMA'lar yumuşatılmış serilerdir; tick büyüklüğü oranı anlamlı kuantize etmez. Evren BIST100'dür.

**06-049** — CEVAPLI — Hareketsiz hisse evren filtresiyle (06-047) dışlanır. 520 sayısı kaynaksız (bkz. 06-059), bölünemez.

**06-050** — OLGU — Ölçüldü: KRDMD dönemi içinde kapanış 25,26–28,24, EMA'lar 26,30–26,81; fiyat bandın içinde değil (−%4 / +%5). Tansu örneği fiyatın bantta olmasını şart koşmuyor; KURALLAR da koşmuyor.

**06-051** — OLGU — Payda seçimi bizim değil, Tansu'nun grafiğinden çıkar: EMA200 doğrulandı (bkz. ana bulgu). EMA ortalaması dönem ortalamasını aynı verir (0,638) ama grafik sonunu (11,6 ≠ 12,1) ve Mart tepesini (12,0 ≠ 12,6) tutturamaz.

**06-052** — CEVAPLI — B-momentum 1: "yön tetikleyicisi verilmedi"; Tansu'nun metninde yön koşulu yok. Trend filtresi eklemek YORUM ve ayrı deneme olur (KURALLAR 1.5).

**06-053** — CEVAPLI — gp-68 "50>100>200" ikinci el ve sonuç gözlemi, giriş koşulu değil. KURALLAR 1.2: ikinci el kural tek başına kullanılmaz.

**06-054** — CEVAPLI — Çıkışı risk paketi belirler: 2 ATR stop veya kapanış < SMA250 (TASARIM 5.5, S2-40). Ölçüt R değil, K1/K2'ye göre fazla getiri (5.7).

**06-055** — CEVAPLI — KURALLAR 3: "Stop ve çıkış: risk paketi"; sıkışma için AB=CD istisnası yok, 2 ATR (TASARIM 5.5, S2-40). Kırılım tepesi/EMA bandı stopu tanımlanmadı.

**06-056** — EKSİK — Ölçüldü (KRDMD 19.01.2026, ATR14=0,836): 2 ATR stop mesafesi %5,85; %1 risk = %17,1 pozisyon, %10 sınırı bağlar, gerçek risk ≈%0,58. Stop mesafesi <%10 ise sınır hep bağlar. TASARIM 5.6 bunu yazmıyor. Fix: raporda "sınırın bağlayıcı olduğu işlem oranı ve gerçekleşen ortalama risk".

**06-057** — CEVAPLI — TASARIM 5.6 (M12) en likit önce; aynı sıra kuralı rastgele kurala da uygulanır (S2-42), karşılaştırma tutarlı kalır. Likit hisse yanlılığı bilinen sonuçtur.

**06-058** — CEVAPLI — TASARIM 5.9: 20 günlük blok yeniden örnekleme, en az 100 işlem ve en az 60 farklı sinyal günü.

**06-059** — YANLIŞ — KURALLAR satır 98 "Yahoo verisi, kaba sayım"; TASARIM 4 Yahoo'yu yasaklar, TASARIM 1 (C7) ön deneme rakamlarını yasaklar; sayı hangi tanımla (ardışık, payda, düzeltme) sayıldı yazılı değil, 99 evren (100/ay) ile de uyuşmuyor (kaynak yok). Fix: sayıyı sil, yerine "sayım ardışık ≥3 bar, /EMA200, İş Yatırım düzeltilmiş veriyle yeniden yapılacak" yaz (sorular-01-036 ile aynı konu).

**06-060** — CEVAPLI — TASARIM 5.9 en az 100 işlem şartı koyar; kaç işlem kalacağı koşu sonrası bilinir (kaynak yok). 520 sayısı geçersiz (06-059).

**06-061** — CEVAPLI — Birleşme kuralı gerekmiyor: sayım birimi işlemdir, pozisyon açıkken sinyal sayılmaz (TASARIM 5.3); bağımlılığı 5.9 blok bootstrap yönetir.

**06-062** — EKSİK — Sıklık kontrolünün geçme/kalma eşiği yok. Fix: KURALLAR 3'e "sıklık kontrolü bilgi içindir; kabul kararı yalnız TASARIM 5.12" yaz.

**06-063** — CEVAPLI — TASARIM 5.2: aylık nokta-zamanlı evren, kapanmış semboller dahil, mutlak getiri "üst sınır, karar için kullanılmaz".

**06-064** — EKSİK — Sembol devri/birleşme TASARIM 8.8'de açık soru; EMA200 davranışı yazılı değil. Evren aylık kurulduğu için hisse sayısı 99 sabit değil (5.2). Fix (YORUM): kopuk seri iki ayrı seri sayılır, her birinde 500 bar ısınma (06-012).

**06-065** — CEVAPLI — TASARIM 5.2, 5.7: getiri karşılaştırma ölçülür (K1 rastgele kural, K2 eşit ağırlıklı sepet, faiz); mutlak getiri karar değil.

**06-066** — CEVAPLI — TASARIM 5.7 K1: eşleştirilmiş rastgele giriş ve K2. (Ama bkz. 06-067: sıkışmanın katkısı ayrılmıyor olabilir.)

**06-067** — EKSİK — K1 "kuralın kendi ön şartlarını sağlayan günlerden" seçiyor; sıkışma ön şart sayılırsa yalnız tetikleme zamanı sınanır, sıkışmanın katkısı değil. Fix: K1'e bir kol ekle: "sıkışma şartı çıkarılmış kırılım (aynı tetik, aynı 10 gün penceresi yok, 20 günlük tepe)" ve fazla getiriyi buna göre yaz.

**06-068** — EKSİK — Çıkarma testi (ablation) tasarımda yok; aileler.py zaten eski. Fix: 06-067 ile aynı kol; sıkışmalı ve sıkışmasız fazla getiri farkı raporlanır.

**06-069** — CEVAPLI — Minimum süre bir parametredir; TASARIM 5.10 sağlamlık ızgarasına girer. Süre kovaları (3–5, 6–10, >10) raporlanması YORUM ve istenirse eklenir.

**06-070** — CEVAPLI — Aynı: eşik derinliği ızgarada (TASARIM 5.10). Tansu'nun örneği %0,64 ortalama gösteriyor, eşik yakını dönemler Tansu'nun ayrı sınırı değil.

**06-071** — CEVAPLI — Tek sabit eşik Tansu'nun gösterdiğidir (başlık: Tolerans %1.2); farklı eşikler TASARIM 5.10'da test edilir. Evren BIST100 ile sınırlı olduğundan oynaklık aralığı dardır.

**06-072** — EKSİK — TASARIM 5.10 "ek: parametre kaydı" diyor ama belgede böyle ek yok. Fix (YORUM): ek yaz: eşik {1,0; 1,2; 1,5}, min gün {2; 3; 5}, giriş penceresi {5; 10; 20}.

**06-073** — EKSİK — "Tasarımcının tecrübesine kalmış" ikinci el (not); %1,2 ve 3 gün görselde var, doğru, ama bunlar "örnekteki değer", sabit kural değil. KURALLAR 3 "birinci el" etiketi bunu söylemiyor. Fix: "Tansu'nun örnekteki değeri; ayarlanabilir olduğu notta (ikinci el); 5.10'a girer".

**06-074** — CEVAPLI — TASARIM 5.8: 2023 sonrası ayrılmış dönem yandı, 2015–2026 bütünüyle geliştirme/doğrulama; yeni ayrılmış dönem kural kaydından sonrası. KRDMD yalnız sadakat için kullanılır, getiriye bakılmaz.

**06-075** — CEVAPLI — Kural KRDMD'den değil, sadakat yalnız oran formülünü çözer. Dış doğrulama ileri yürüme (5.8) ve kâğıt üstü canlı dönemle (5.8) yapılır.

**06-076** — OLGU — Hesaplandı. Kural (High tepesi): sinyal 19.01.2026, giriş 20.01 AOF 28,57; stop 26,90 (2 ATR) hiç vurulmadı (en düşük 27,70). 09.04.2026 kapanışı 36,68 → +%28,4. (36,68 / 28,43 − 1 = %29,0 EMA200'e göre, soru doğru.) SMA250 çıkışı hesaplanmadı.

**06-077** — OLGU — Evet yakalar: bitiş 14.01, oran 15.01'de 1,28, sinyal 19.01 (bitişten sonra 3. bar), 10 gün penceresi içinde. Close tepesiyle sinyal 16.01.

**06-078** — OLGU — Ölçüldü: oran 15.01'de %1,2'yi geçti (1,28), fiyat dönem tepesini 19.01'de aştı; yani oran önce, kırılım 4 gün sonra. Bu sıra "bitiş = oran > eşik" tanımıyla uyumlu; sonra oran Mart'ta %12,7'ye çıkar.

**06-079** — CEVAPLI — Pencere bitişten başlar (KURALLAR 3), kırılımdan önce kapanmaz. KRDMD'de 4 bar sonra kırılım olmuştu. Kırılım 10 günden geç gelirse işlem yok (YORUM).

**06-080** — CEVAPLI — Sayaç bitişte başlar (KURALLAR 3); aşağı hareket giriş üretmez, 10 gün içinde kapanış > dönem tepesi gelirse sinyal verilir.

**06-081** — EKSİK — Bkz. 06-027. Fix: dönem tepesi High (YORUM), kırılım kapanış > tepe. Fitil etkisini K1 ve 5.10 ızgarasında "tepe = Close" kolu ölçer.

**06-082** — CEVAPLI — Kırılım kapanışla onaylanır, giriş ertesi AOF'tur (TASARIM 5.3); fitil geri dönüşü AOF ve stopla ölçülür.

**06-083** — CEVAPLI — Sahte kırılım kabul ölçütü değil; TASARIM 5.12 yalnız fazla getiri, p, masraf, yıl tutarlılığı, örneklem istiyor.

**06-084** — CEVAPLI — TASARIM 5.12 (altı koşul), Holm düzeltmeli p<0,05 (5.11). Kararı kural verir, kişi değil.

**06-085** — EKSİK — Sorgu-2 F bölümü (S2-37–40) hacmi hiç anmıyor; S2-37 "sadakat belirler" idi, şimdi cevap var. Fix: S2-37'ye "payda EMA200, doğrulandı"; "hacim koşulu yok, aileler.py'deki 1,5×medyan kaynaksız" notu.

**06-086** — CEVAPLI — TASARIM 7.1: ön deneme kodu kaldırılır, 5.3 "kod belgeye uyar". Kural = KURALLAR 3.

**06-087** — EKSİK — "Veri yok" ile "sinyal yok" ayrımı yazılı değil. Fix: rapora "ısınma/veri yok nedeniyle dışarıda kalan hisse-gün sayısı" satırı (06-012 ile birlikte).

**06-088** — CEVAPLI — Adım fonksiyonu yalnız t'ye kadar barları görür (TASARIM 4, A5); dönem tepesi bitişe kadarki barlardan hesaplanır.

**06-089** — CEVAPLI — TASARIM 5.3: sinyal kapanışta, işlem ertesi AOF; aynı kapanıştan işlem yok.

**06-090** — CEVAPLI — Yahoo kullanılmaz; her koşu tarihli değişmez anlık görüntü kullanır (TASARIM 4, B2); canlıda 19:30 tazelik/kalite kontrolü, son çubuk bugün değilse kart yok (5.1, 6.1).

**06-091** — ZAYIF SORU — Aile hacim kullanmıyor.

**06-092** — CEVAPLI — Takvim modülü yarım günleri ve tatilleri yönetir (TASARIM 4, A1). Yahoo 2994 satır, İş Yatırım/borsapy ~2946 satır; fazladan tatil barları yapay "hareketsiz gün" üretebilirdi, İş Yatırım'la bu risk yok (veri-kaynaklari 3.1).

**06-093** — OLGU — Ölçüldü: dört EMA'nın aralığı eğriyi üretir (grafik sonu %12,3). Yalnız EMA20/50/100 olsaydı grafik sonu %7,9 çıkardı, görseldeki ≈%12,1'e uymaz. Dört EMA'lı tanım doğru.

**06-094** — YANLIŞ — B-momentum 2 "adlar okunaksız" diyor; görselde lejant EMA20 (14.44), EMA50 (14.29), EMA100 (14.31), EMA200 (14.42) okunuyor (düşük çözünürlük, okuma temkinli). Bant (14,44−14,29)/14,42 = %1,04 ≤ %1,2: sıralama şart değil, eşikle tutarlı. Fix: B-momentum 2'deki "okunaksız/olası" notunu "okunuyor, bant %1,04" yap.

**06-095** — ZAYIF SORU — gp-71 başlığındaki "çıkış" sıkışmadan yukarı çıkış (kırılım), pozisyon çıkışı değil; görselde yazı yok. Yön çelişkisi yok. KURALLAR 3'ün parçası değil.

**06-096** — CEVAPLI — KURALLAR 3 yalnız EMA20/50/100/200 (KRDMD) ailesidir; gp-106 EMA5/8/13 ayrı kayıt ve ikinci el (B-momentum 3).

**06-097** — CEVAPLI — TASARIM 3 ve S2-39: yalnız alış. Örneklem yarıya iner, bilinen sınırlama; kural simetrik değil.

**06-098** — EKSİK — Gerekçe yazılı değil. gp-36 Tansu'nun sözü ikinci el aktarım ("yön kırılım sonrası belli olur"). Fix (YORUM): TASARIM 3'e "yalnız alış: bireysel yatırımcı için açığa satış kapsam dışı; yön bağımsızlık ilkesine bilinçli sapma" yaz.

**06-099** — CEVAPLI — TASARIM 5.4 (M11): pozisyon, son 10 günün medyan TL işlem tutarının %2'sini geçemez; %0,3 masraf kaymayı kapsar. KRDMD günlük TL hacmi 0,7–2,8 milyar; 100.000 TL pozisyon bunun %0,01'i.

**06-100** — OLGU — Yan yana yazılmamıştı; şimdi: KRDMD giriş 20.01.2026 AOF 28,57; 2 ATR stop 26,90 vurulmadı; 09.04.2026 kapanışı 36,68 (+%28,4); SMA250 çıkışı hesaplanmadı. Tansu işlem vermedi (B-momentum 1), bu yüzden sadakat yalnız dönem ve oran çıktısına karşı ölçülür (KURALLAR 4). Fix: kural kaydına bu satırı yaz.

## Özet

Hüküm sayıları (100 soru): CEVAPLI 48, EKSİK 22, OLGU 17, ZAYIF SORU 11, YANLIŞ 2. (Sayım dosyadan komutla doğrulandı.)

En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği:

1. **06-012 / 06-014 (EKSİK)** — EMA200 ısınması: 200 bar yetmez (veri başlangıcı 2025-01 ise dönem ortalaması %0,64 → %0,82). Değişiklik: TASARIM'a "ilk sinyal ≥500 bar sonra, elenen hisse-gün raporda" ekle.
2. **06-067 / 06-068 (EKSİK)** — Sıkışmanın katkısı ayrılmıyor (K1 ön şartı sıkışmaysa yalnız zamanlama sınanır). Değişiklik: TASARIM 5.7'ye K1 kolu: "sıkışmasız aynı kırılım".
3. **06-002 / 06-003 / 06-020 (OLGU+EKSİK)** — Oran formülü çözüldü: (maxEMA − minEMA)/EMA200. Değişiklik: KURALLAR 3 ve 4'e formülü yaz; sadakat ölçütü = dönem ortalaması + grafik sonu (≈%12,1) + Mart tepesi (≈%12,6); aileler.py'deki `/Close` yanlış.
4. **06-059 (YANLIŞ)** — KURALLAR 98'deki "520 dönem (Yahoo, kaba sayım)" kaynaksız, Yahoo ve ön deneme yasağıyla çelişir. Değişiklik: sayıyı sil; sayımı İş Yatırım, ardışık ≥3 bar, /EMA200 ile yeniden yap.
5. **06-027 / 06-081 (EKSİK)** — "Dönem en yüksek fiyatı" tanımsız (High 29,00 → sinyal 19.01; Close 28,24 → sinyal 16.01). Değişiklik: KURALLAR 3'e "dönem High'ı; kapanış > tepe (YORUM)".
6. **06-009 / 06-010 / 06-007 (EKSİK)** — "Bitti" ve "ardışık" tanımları yok. Değişiklik: KURALLAR 3'e "dönem = ardışık oran ≤ eşik barları; ilk oran > eşik barı bitirir; birleştirme yok; sayım birimi işlem".
7. **06-056 (EKSİK)** — %10 pozisyon sınırı stop <%10 iken hep bağlar (KRDMD: stop %5,85, gerçek risk ≈%0,58). Değişiklik: TASARIM 5.6/5.9: raporda bağlayıcılık oranı ve gerçekleşen ortalama risk.
8. **06-072 (EKSİK)** — TASARIM 5.10 "ek: parametre kaydı" diyor ama ek yok. Değişiklik: ek yaz (eşik {1,0; 1,2; 1,5}, min gün {2; 3; 5}, pencere {5; 10; 20}, YORUM).
9. **06-025 / 06-073 (EKSİK)** — Tansu'nun Pre Signal'i sıkışma sürerken çıkıyor, bizim tetik bitişten sonra; %1,2 ve 3 gün "örnekteki değer, ayarlanabilir". Değişiklik: KURALLAR 3'e bu iki notu ekle.
10. **06-094 (YANLIŞ)** — B-momentum 2 "adlar okunaksız" demiş; görselde EMA20/50/100/200 okunuyor, bant %1,04. Değişiklik: B-momentum 2 notunu düzelt; ICBCT'yi "aynı araç, bant eşiğin altında" diye kaydet. (Yedek: 06-032 bir dönemde tek giriş; 06-045 ertesi AOF farkı raporu.)
