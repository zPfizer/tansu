# Kural kataloğu (05.10.2026)

Kaynak: beyindeki Tansu havuzu (14.10 sayımı: 258 not, 228 görsel). Ayrıntılar `docs/kurallar/A–E` dosyalarındadır;
bu belge onların dizini ve seçimidir. Her kuralın kaynağı, parametresi ve "YORUM" etiketi orada.

Okuma kuralları:
- **Birinci el:** Tansu'nun aracının görsel çıktısı (başlık, etiket, tablo, kod).
- **İkinci el:** notlardaki Claude özeti ya da aktarılan tweet. Kural olarak tek başına kullanılmaz.
- **NotebookLM:** Tansu'nun paylaştığı ama kendi aracından çıkmayan infografikler. Ayrı işaretlenir.
- **YORUM:** kaynakta olmayan, bizim doldurduğumuz değer. Tansu'nun fikirleri esastır: YORUM yalnız Tansu'nun o konuda
  fikri yoksa geçerlidir. Tansu'nun fikri varsa ona uyulur; uygulanamıyorsa (ör. veride açılış yok) neden yazılır (Levent
  10.10). Bir YORUM'un sınamada denenen her değeri yeni
  deneme sayılır. Sadakat kontrolünde denenen aday formüller deneme sayısına girmez, p üretmez; seçilen
  formül kural kaydına girer (TASARIM 5.11, İ: 10-033, 04-090).

## 1. Ana bulgular

1. Tansu hiçbir kural için tam giriş + stop + hedef üçlüsü ve sistematik sınama vermiyor. Kanıtı
   seçilmiş örneklerdir; bazı başarısız örnekleri de paylaşır (BALAT, AKSGY, bağı kopan çift).
2. Tepe/dip (pivot) bulma ayarı, temas toleransı, bölge üretimi ve SETUP puan formülü hiçbir yerde yok.
3. Notlarda görselle çelişen en az 8 hata bulundu (ör. BOS/Fib seviyeleri, ISKPL tarihi, Gartley D
   yönü, HKTM işareti). Not ile görsel çelişirse görsel geçerlidir.
4. 05.10 ön denemesindeki "4 ATR hedef" ve "EMA50 altı çıkış" Tansu kaynaklarında yok; kaldırılır.

## 2. Dizin

Hazırlık: **H** = birinci elden kodlanabilir, az YORUM · **K** = kısmen, önemli YORUM · **X** = kodlanamaz.

### Giriş aileleri
| Kural | Dosya | Hazırlık | Birinci el olan | Eksik (YORUM) | Tansu'nun kanıtı |
|---|---|---|---|---|---|
| Çift rotasyonu (z-skor ±2, ΔZ dönüşü, T+1 açılış, hep yatırımda) | D | **K** | ±2, ΔZ tanımı = Z_t − Z_{t−1} (rakamla doğrulandı), yön, T+1 | sapma formülü (40.560 adayla bulunamadı), pencere, tek gün ΔZ yeterliliği, çift seçimi. Ham fiyat bizim seçimimiz (YORUM). Örnek ham fiyatla uyumlu. Genel düzeltme politikası açık değil. | VAKBN–GARAN +%52,9 (B&H +%20,9, MaxDD −%27,4); CIMSA–OYAKC +%49,2; bağı kopan çift ≈−%21 |
| AB=CD + hedef merdiveni | C | **K** | D = C + r(B−A), r 1,0/1,27; BC ≤ AB; hedef D + {0,618; 1; 1,618}(A−D) (rakamla doğrulandı) | yön (SMRTG işlemleri aşağı yönlü), pivot ayarı, oran toleransı, stop | SMRTG 12 kalıp (7 hedef, 3 stop) +%305; ISKPL 5/5 +%610; tek hisse, masrafsız, C fiyatından giriş |
| EMA sıkışması (KRDMD) | B | **H** | EMA20/50/100/200, tolerans %1,2, en az 3 gün; oran formülü sadakatle çözüldü (§4) | giriş tetiği | Tek örnek (sıkışmadan sonra yükseliş) |
| Yükselen kanal alt bant teması (AEFES) | A | **K** | Lookback 120, 3/3 temas, Low-Bant %, Kapanış-Bant % | kanal çizim yöntemi, tolerans, stop/hedef | Tek örnek, sonuç yok |
| Kırılım + range retest + FVG (AKFIS A+) | A, E | **K** | Sıra: konsolidasyon → kırılım → FVG → geri test → teyit → giriş; stop FVG altı; 3 hedef (~1/1,5/2R ölçüm) | kutu süresi, FVG ve geri test toleransı, puan | 2 seçilmiş olumlu örnek |
| Gartley | C, E | **K** | AB/XA 0,618; BC/AB 0,382–0,886; D 0,786 XA; stop X | tolerans; D formülü tabloda ters; TP kaynakları çelişiyor | Yok |
| BOS + Fib altın bölge (0,618–0,786) + FVG/OB | A, C | **K** | Fib seviyeleri; stop Fib 1; TP1 Fib 0 (ikinci el) | BOS, FVG, OB tanımı | Tek örnek |
| Elliott 2. dalga (BRYAT) | C | **K** | Başlık şablonu; kurallar ikinci el (%10 itki, 0,50–0,786) | dalga sayımı | Sonuçsuz |
| Düşen direnç kırılımı + talep (LIDER/BALAT) | A, C | **K** | Temas 3, Lookback 20/30, EMA5/8/13 | talep bölgesi, kümülatif delta (veri yok) | LIDER olumlu, BALAT başarısız |
| Fincan-kulp (GUBRF) | B, E | **K** | hedef = kırılım + derinlik; R/R 1:2,27 | dedektör, stop | Tek örnek |
| Gizli pozitif uyumsuzluk | B | **K** | Swing=15 sol, MinGap=15 | osilatör gizli | Seçilmiş |
| A/D–EMA(3) (ISCTR) | B | **K** | Strateji %19,1, B&H %10,8, Sharpe 0,67 | operatör yönü | Tek hisse |
| Bullish engulfing | B | H (tetik) | Kod birebir | bağlam, stop | Yok |
| Kelebek, Trident, Three Drives, X–B kırılımı | C | K | Bazı oranlar | çok | Seçilmiş |
| SETUP puanı, D.Touch/Teyit, Siyah/Beyaz Kuğu, BOM, AHENK, mavi çizgi, Pre Signal, gizli filtre | A, B, C | **X** | Yalnız etiket | Formül yok | — |

### Risk ve çıkış (E)
| Kural | Hazırlık | Not |
|---|---|---|
| Örnekte %1 risk, lot = risk / (2 ATR) | H | NotebookLM, G115/g1 (Tansu paylaştı) |
| Acil stop: giriş − 2 ATR, gün içi dokunuşta çık | H | Ad: aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22; hesap: NotebookLM, G115/g1 |
| Gün sonu stopu: kapanış < SMA250 | H | Ad: aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22; çıkış örneği: NotebookLM, G115/g1; SMA250 seçimi: YORUM (TASARIM 5.5) |
| İz süren stop (+1,5 ATR), kısmi kâr, önceki gün dibi altı %50 | K | ikinci el; görselde yalnız "STOP 184.54 / ATR 4.62" |
| Harmonik hedef merdivenleri (Excel %38,2 / SAYAS 1:1 ve %61,8) | K | kaynaklar çelişiyor |
| Durum etiketleri: AKTİF, TAMAMLANDI, TEPKİ_VERDİ, BOZULDU | H (ad) | eşikleri yok |
| Tepki penceresi: D sonrası 20 mum (görsel) / 10 gün (not) | K | çelişki |

### Piyasa durumu (D)
| Kural | Hazırlık | Not |
|---|---|---|
| Piyasanın Nabzı 4/5 (ilk 5 kutudan 4'ü olumlu) | K | NotebookLM; SMA 18/35 ile 20/50 çelişiyor |
| BIST + VIX 5 adım (SMA20/50, Heikin Ashi, VIX RSI200/SMA10) | K | NotebookLM; "VIX" = ABD VIX, Yahoo'da bedava |
| Sektör liderleri 30/60/90 gün, \|30g\| > %50 anomali temizliği | H | birinci el konsol çıktısı |
| Volatilite şoku freni | X | eşik yok |

## 3. Seçim

**Ölçütler (seçimden önce yazıldı):**
1. Giriş kuralının çekirdeği birinci elden belli.
2. Bedava günlük veriyle uygulanabilir.
3. Tansu sayısal bir sonuç göstermiş (sınanacak bir iddia var).
4. Seçilenler birbirinden farklı türde olsun (aynı fikri iki kez sınamamak için).

**İlk sürümde sınanacak aileler:**
| Sıra | Aile | Neden | En önemli YORUM |
|---|---|---|---|
| 1 | Çift rotasyonu | 4 ölçütün hepsi; Tansu'nun en güçlü rakamları | sapma formülü ve pencere |
| 2 | EMA sıkışması | parametreler ve oran formülü birinci el | giriş tetiği |

AB=CD ilk sürümden çıktı (Sorgu 3, TASARIM §3): Tansu'nun SMRTG işlemleri aşağı yönlü kalıplar ve C
fiyatından giriş; bireysel yatırımcı BIST'te açığa satamaz. İkinci dalgada geometri sadakati yönsüz
yapılır.

**Ailelerin işlem kuralları (ilk sürüm):**

1. **Çift rotasyonu** (birinci el: giriş eşiği, ΔZ tanımı, yön, zaman). Ham fiyat bizim seçimimiz (YORUM). Örnek ham fiyatla uyumlu. Genel düzeltme politikası açık değil.
   - Sapma: log(Y) − log(X), ortalama ve standart sapma son 60 günden (YORUM; Tansu'nun Z'si 40.560
     aday formülle üretilemedi; bilet 06 sadakati, §4, 1564 adayla yine üretemedi; 10.10 ek turu 6256 adayla da üretemedi: YORUM kalıcıdır). Sabit terim (α) yok; ortalama çıkarıldığı için Z aynıdır.
   - Z ≤ −2 ve ΔZ > 0 → ertesi gün Y'ye geç. Z ≥ +2 ve ΔZ < 0 → ertesi gün X'e geç. Tek günlük ΔZ
     yeterlidir (YORUM; Tansu'nun raporundaki tek örnek +0,30).
   - İlk sinyale kadar nakit; sonra hep bir hissede (YORUM; genel nakit politikası kaynakta açık değil,
     TASARIM 5.6). Ayrı stop yok (YORUM; kaynak stop politikasını açıklamaz, TASARIM 5.5).
   - Çiftler önceden yazılmış kuralla seçilir (TASARIM 5.6).
   - K1 ön şartı: çift seçilmiş ve |Z| ≥ 2 olan günler.
   - Sağlamlık ızgarası (TASARIM 5.10, YORUM): Z penceresi {60; 120}, eşik {1,5; 2; 2,5}, seçim p'si
     {0,01; 0,05; 0,10}. (İ: 04-089)
2. **EMA sıkışması kırılımı** (Tansu'nun sayısal iddiası yok; bu ailenin getiri iddiası bizim
   hipotezimizdir, İ: 10-002)
   - Oran: (en büyük EMA − en küçük EMA) / EMA200; EMA20/50/100/200, `ewm(adjust=False)` (birinci el,
     sadakatle çözüldü, §4).
   - Sıkışma dönemi: oranın ≤ %1,2 olduğu art arda en az 3 gün; oranın eşiği aştığı ilk gün dönemi
     bitirir. Tansu'nun %1,2 ve 3 günü "örnekteki değer"dir.
   - Giriş (YORUM): dönem bittikten sonraki 10 gün içinde kapanış, dönemdeki en yüksek gün yükseğinin
     üstüne çıkarsa ertesi gün. Dönem başına tek giriş. Stop ve çıkış: risk paketi. Hedef yok.
   - Not: Tansu'nun ICBCT "Pre Signal"i sıkışma sürerken çıkıyor; bizim tetik bitişten sonra (YORUM).
   - K1 ön şartı: sıkışma dönemi bitmiş ve 10 günlük pencere açık günler. Ek kol: sıkışmasız aynı kırılım (kapanış önceki 20 günün en yüksek yükseğinin üstünde, sıkışma penceresinde değil; 20 YORUM, TASARIM 5.7).
   - Sağlamlık ızgarası (TASARIM 5.10, YORUM): eşik {%1,0; %1,2; %1,5}, en az gün {2; 3; 5}, giriş
     penceresi {5; 10; 20}. (İ: 06-072)

AEFES kanal, AKFIS kurulumu ve AB=CD ikinci dalgadadır. Diğerleri dizinde kalır; kaynak çıktıkça yükselir.

VAKBN–GARAN paneli T+1 açılış gösterir (araç, Rota/g2, işlem paneli). "Ertesi gün" sınamada ertesi günün
AOF'u olarak modellenir; uygulanamaz: mevcut veride açılış yok (TASARIM 5.3).

**Risk paketi:** %1 risk (NotebookLM örneği), 2 ATR acil stop, SMA250 altı kapanışta gün sonu stopu (EMA sıkışması; çift rotasyonu
hariç, onun kendi çıkışı karşı uçta geçiştir). Pozisyon tavanı %10 (YORUM, bizim; çoğu işlemde %1
riskten daha bağlayıcıdır).

## 4. Sadakat kontrolü (sınamadan önce)

YORUM'ları sonuca bakarak seçmek yasak. Ama Tansu'nun **kendi çıktılarındaki rakamları** yeniden üretmek
serbesttir; bu performans değil, kuralın doğru okunduğunun kanıtıdır.

| Aile | Tansu çıktısı | Yeniden üretilecek | Bu neyi çözer |
|---|---|---|---|
| Çift rotasyonu | VAKBN–GARAN raporu | son Z −3,108, önceki Z −3,404, 6 geçiş; Beta 1,675, korelasyon 0,731, piyasada kalma %72,27; Mart–Mayıs 2025'te sinyal yok | sapma formülü ve pencere |
| EMA sıkışması | KRDMD | sıkışma 17.12.2025–14.01.2026 (20 gün), ortalama oran %0,64 | oran formülü |
| AB=CD (ikinci dalga) | KRPLS, MARKA #13, SMRTG tablosu | D = 11,29 / 10,05 / 70,25; SMRTG hedef getirileri | pivot ayarı, yön |
| Kanal (ikinci dalga) | AEFES 03.09.2026 | alt bant 17,76; temas 3/3; genişlik +%15,3 | kanal çizim yöntemi |

Sonuçlar (Sorgu 3, 05.10.2026):
- **EMA sıkışması çözüldü:** (en büyük EMA − en küçük EMA) / EMA200, ham kapanıştan `ewm(adjust=False)`.
  - Dönem ortalaması %0,638.
  - 09.04.2026 EMA değerleri lejantla birebir.
  - Grafik sonu ve Mart tepesi görselle ±0,3 içinde.
- **EMA sıkışması, bilet 05 ölçümü (İş Yatırım ham seri, `docs/sadakat.md`):** yukarıdaki "birebir" Yahoo
  serisiyle ölçülmüştü; İş serisinde EMA200 sıkı toleransı geçmiyor. Karar: sonuç **gevşek bantla üretildi**.
  - Dönemi, gün sayısını ve ortalamayı tam tutan tek aday "son 3 yıl" (son 2 yıl da tutuyor; ikisi aynı
    sonucu veriyor).
  - Bu adayda EMA20/50/100 sıkı toleransta; EMA200 28,4366 (Tansu 28,43), gevşek bantta (±0,05).
  - Neden: EMA200 uzun belleklidir; Tansu'nun veri başlangıcı bilinmiyor. Oran formülü değişmez.
  - Bütün geçmişle dönem bir gün erken başlıyor (21 gün, %0,665). Sınamada veri başlangıcı sabit
    tutulur ve rapora yazılır (İ: 06-014).
- **Çift Z'si üretilemedi** (40.560 aday). VAKBN–GARAN örneğinin fiyatları ham okumayla uyumludur
  (araç, Rota/g2); genel fiyat düzeltme politikası açık değildir (TASARIM 5.1).
- **Çift Z'si, bilet 06 ölçümü (İş Yatırım ham seri, `docs/sadakat.md`):** 1564 aday (log oran ve β'lı
  kalıntı × pencere 10–400 × ddof {0; 1}), bütün işlem günleri. Sıkı toleransta (±0,0005) eşleşme yok.
  Gevşek bantta (±0,05) 534 aday eşleşti: tek aday kalmadığı için gevşek bant kullanılmadı.
  Sonuç: **üretilemedi; YORUM kalır** (log oran, 60 gün). Beta, korelasyon, piyasada kalma ve
  Mart–Mayıs 2025 kontrolleri formül olmadığı için yapılmadı.
- **Çift Z'si, ek tur (10.10.2026, `docs/sadakat.md`):** Tansu'nun kendi kaynaklarından üç aday ailesi, aday listesi
  koşudan önce commit edildi (bf79a28): fiyat düzeyinde OLS spread (X403), log fark − hareketli ortalama ve sabit
  standart sapma (X404), bugünü dışlayan pencere. 6256 aday (Z ve −Z), bütün günler. Sıkı toleransta eşleşme yok;
  gevşek bantta 1393 aday, tek aday kalmadı. Sonuç: **üretilemedi; YORUM kalıcıdır** (log oran, 60 gün). Yeni tur açılmaz.

Veri: Tansu `yfinance` kullanıyor, ama Yahoo ham kapanışı İş Yatırım ham serisiyle aynı. Kontrol İş Yatırım
ham seriyle yapılır.

Kural:
- Tolerans, adaylar denenmeden önce yazılır. "Üretti" = Tansu'nun gösterdiği son hanenin yarısı içinde
  (Z için ±0,0005). Gevşek bant (±0,05) yalnız tek aday kalırsa kullanılır. (İ: 04-002, 14-058)
- Birden çok aday formül denenir; Tansu'nun rakamını en iyi üreten seçilir. Çift Z'si için aday
  kümesine standart sapmanın ddof'u {0; 1} de girer. (İ: 19-028)
- Rapor tarihi bilinmiyorsa (Z_t, Z_{t−1}) çifti bütün işlem günlerinde aranır; eşleşen günler yazılır.
  (İ: 04-003)
- Hiçbiri üretemezse YORUM olarak kalır ve raporda yazılır.
- Sonuç `docs/sadakat.md`'ye yazılır; `python -m tansu sadakat` aynı rakamları yeniden üretir. (İ: 11-023)
- Bu adım getiri sonuçlarına bakmaz.

## 5. Bilinen riskler
- Tansu'nun örnek çiftleri ve hisseleri sonuca bakılarak seçilmiş olabilir. Bu yüzden çift rotasyonu
  yalnız onun çiftlerinde değil, önceden yazılmış bir kuralla seçilen bütün çiftlerde sınanır
  (aynı sektör: YORUM, TASARIM 5.6; oluşum penceresinde eşbütünleşme). Onun çiftleri ayrıca gösterilir. AGROT–GARAN
  rotasyon değildir (iki bacak + nakit) ve borsapy'ye göre farklı sektördedir.
- NotebookLM infografikleri Tansu'nun kendi kuralı olmayabilir.
