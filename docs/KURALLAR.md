# Kural kataloğu (05.10.2026)

Kaynak: beyindeki Tansu havuzu (238 not, 214 görsel). Ayrıntılar `docs/kurallar/A–E` dosyalarındadır;
bu belge onların dizini ve seçimidir. Her kuralın kaynağı, parametresi ve "YORUM" etiketi orada.

Okuma kuralları:
- **Birinci el:** Tansu'nun aracının görsel çıktısı (başlık, etiket, tablo, kod).
- **İkinci el:** notlardaki Claude özeti ya da aktarılan tweet. Kural olarak tek başına kullanılmaz.
- **NotebookLM:** Tansu'nun paylaştığı ama kendi aracından çıkmayan infografikler. Ayrı işaretlenir.
- **YORUM:** kaynakta olmayan, bizim doldurduğumuz değer. Her YORUM, sınamada deneme sayısına girer.

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
| Çift rotasyonu (z-skor ±2, ΔZ dönüşü, T+1 açılış, hep yatırımda) | D | **H** | ±2, ΔZ = Z_t − Z_{t−1} (rakamla doğrulandı), yön, T+1, yalnız alış | sapma formülü, pencere (~60 gün tahmini), çift seçimi | VAKBN–GARAN +%52,9 (B&H +%20,9, MaxDD −%27,4); CIMSA–OYAKC +%49,2; bağı kopan çift ≈−%21 |
| AB=CD + hedef merdiveni | C | **H** | D = C + r(B−A), r 1,0/1,27; BC ≤ AB; hedef D + {0,618; 1; 1,618}(A−D) (rakamla doğrulandı) | pivot ayarı, oran toleransı, stop | SMRTG 12 kalıp (7 hedef, 3 stop) +%305; ISKPL 5/5 +%610; tek hisse, masrafsız |
| EMA sıkışması (KRDMD) | B | **K** | EMA20/50/100/200, tolerans %1,2, en az 3 gün, 130 mum | oran formülü, giriş tetiği, stop | Tek örnek (sıkışmadan sonra yükseliş) |
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
| %1 risk, lot = risk / (2 ATR) | H | NotebookLM infografiği (Tansu paylaştı) |
| Acil stop: giriş − 2 ATR, gün içi dokunuşta çık | H | aynı kaynak |
| Gün sonu çıkış: kapanış < SMA250 | H | aynı kaynak |
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
| 2 | AB=CD | geometri ve hedef birinci el; Tansu'nun tek tablolu sınamaları | pivot ayarı, stop |
| 3 | EMA sıkışması | parametreler birinci el | giriş tetiği |

AEFES kanal ve AKFIS kurulumu ikinci dalgadadır: iskeletleri birinci el, ama YORUM sayısı fazla.
Diğerleri dizinde kalır; kaynak çıktıkça yükselir.

**Risk paketi:** %1 risk, 2 ATR acil stop, SMA250 altı kapanışta çıkış (bütün aileler). Aileye özgü hedef
yalnız Tansu verdiyse kullanılır (AB=CD merdiveni). Çift rotasyonunun kendi çıkışı vardır (karşı uçta geçiş).

## 4. Sadakat kontrolü (sınamadan önce)

YORUM'ları sonuca bakarak seçmek yasak. Ama Tansu'nun **kendi çıktılarındaki rakamları** yeniden üretmek
serbesttir; bu performans değil, kuralın doğru okunduğunun kanıtıdır.

| Aile | Tansu çıktısı | Yeniden üretilecek | Bu neyi çözer |
|---|---|---|---|
| Çift rotasyonu | VAKBN–GARAN raporu | son Z −3,108, önceki Z −3,404, 6 geçiş | sapma formülü ve pencere |
| EMA sıkışması | KRDMD | sıkışma 17.12.2025–14.01.2026 (20 gün), ortalama oran %0,64 | oran formülü |
| AB=CD | KRPLS, MARKA #13 | D = 11,29 / 10,05 / 70,25 | pivot ayarı |
| Kanal (ikinci dalga) | AEFES 03.09.2026 | alt bant 17,76; temas 3/3; genişlik +%15,3 | kanal çizim yöntemi |

Kural: birden çok aday formül denenir; Tansu'nun rakamını en iyi üreten seçilir ve sonuç kaydedilir.
Hiçbiri üretemezse YORUM olarak kalır ve raporda yazılır. Bu adım getiri sonuçlarına bakmaz.

## 5. Bilinen riskler
- Tansu'nun örnek çiftleri ve hisseleri sonuca bakılarak seçilmiş olabilir. Bu yüzden çift rotasyonu
  yalnız onun çiftlerinde değil, önceden yazılmış bir kuralla seçilen bütün çiftlerde sınanır
  (aynı sektör, oluşum penceresinde eşbütünleşme). Onun çiftleri ayrıca gösterilir.
- NotebookLM infografikleri Tansu'nun kendi kuralı olmayabilir.
