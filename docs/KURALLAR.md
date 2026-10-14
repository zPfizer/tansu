# Kural kataloğu (05.10.2026)

Kaynak: beyindeki Tansu havuzu (14.10 sayımı: 258 not, 228 görsel). Ayrıntılar `docs/kurallar/A–E` dosyalarındadır;
bu belge onların dizini ve seçimidir. Her kuralın kaynağı, parametresi ve "YORUM" etiketi orada.

Okuma kuralları:
- **Birinci el** (GLOSSARY): kuralın dayanağı bu kaynaktır. Not ile görsel çelişirse görsel geçerlidir (§1 madde 3).
- **İkinci el** (GLOSSARY): kural olarak tek başına kullanılmaz.
- **NotebookLM** (GLOSSARY): ayrı işaretlenir.
- **YORUM:** kaynakta olmayan, bizim doldurduğumuz değer. Tansu'nun fikirleri esastır: YORUM yalnız Tansu'nun o konuda
  fikri yoksa geçerlidir. Tansu'nun fikri varsa ona uyulur; uygulanamıyorsa (ör. veride açılış yok) neden yazılır (Levent
  10.10). Bir YORUM'un sınamada denenen her değeri yeni
  deneme sayılır; istisna: önceden yazılmış sağlamlık ızgarasının hücreleri ve masraf senaryoları deneme sayısına
  girmez (TASARIM 5.10, 5.11; İ: 09-056). Sadakat kontrolünde denenen aday formüller deneme sayısına girmez, p üretmez; seçilen
  formül kural kaydına girer (TASARIM 5.11, İ: 10-033, 04-090).

## 1. Ana bulgular

1. Tansu hiçbir kural için tam giriş + stop + hedef üçlüsü ve sistematik sınama vermiyor. Kanıtı
   seçilmiş örneklerdir; bazı başarısız örnekleri de paylaşır (BALAT, AKSGY, bağı kopan çift).
2. Tepe/dip (pivot) bulma ayarı, temas toleransı, bölge üretimi ve SETUP puan formülü hiçbir yerde yok.
3. Notlarda görselle çelişen en az 8 hata bulundu (ör. BOS/Fib seviyeleri, ISKPL tarihi, Gartley D
   yönü, HKTM işareti). Not ile görsel çelişirse görsel geçerlidir.
4. 05.10 ön denemesindeki "4 ATR hedef" ve "EMA50 altı çıkış" Tansu kaynaklarında yok; kaldırılır.

## 2. Dizin

Hazırlık sütunu: H, K ve X anlamı için GLOSSARY "Hazırlık" maddesine bakın.

### Giriş aileleri
| Kural | Dosya | Hazırlık | Birinci el olan | Eksik (YORUM) | Tansu'nun kanıtı |
|---|---|---|---|---|---|
| Çift rotasyonu (z-skor ±2, ΔZ dönüşü, T+1 açılış, hep yatırımda) | D | **K** | ±2, ΔZ tanımı = Z_t − Z_{t−1} (rakamla doğrulandı), yön, T+1 | sapma formülü (sadakat turlarında bulunamadı, §4), pencere, tek gün ΔZ yeterliliği, çift seçimi. Ham fiyat bizim seçimimiz (YORUM). Örnek ham fiyatla uyumlu. Genel düzeltme politikası açık değil. | VAKBN–GARAN ve CIMSA–OYAKC raporları, bağı kopan çift (rakamlar D "Tansu'nun kanıtı"nda) |
| AB=CD + hedef merdiveni | C | **K** | D = C + r(B−A), r 1,0/1,27; hedef D + {0,618; 1; 1,618}(A−D) (rakamla doğrulandı). BC ≤ AB ikinci eldir (not; C §3), birinci el sayılmaz | yön (SMRTG işlemleri aşağı yönlü), pivot ayarı, oran toleransı, stop | SMRTG ve ISKPL sonuçları C §5'te; tek hisse, masrafsız, C fiyatından giriş |
| EMA sıkışması (KRDMD) | B | **H** | EMA20/50/100/200, tolerans %1,2, en az 3 gün; oran formülü sadakatle çözüldü (§4) | giriş tetiği | Tek örnek (sıkışmadan sonra yükseliş) |
| Yükselen kanal alt bant teması (AEFES) | A | **K** | Lookback 120, 3/3 temas, Low-Bant %, Kapanış-Bant % | kanal çizim yöntemi, tolerans, stop/hedef | Tek örnek, sonuç yok |
| Kırılım + range retest + FVG (AKFIS A+) | A §1 | **K** | Sıra: konsolidasyon → kırılım → FVG → geri test → teyit → giriş; stop FVG altı; 3 hedef (~1/1,5/2R ölçüm) | kutu süresi, FVG ve geri test toleransı, puan | 2 seçilmiş olumlu örnek |
| Gartley | C §7 | **K** | AB/XA 0,618; BC/AB 0,382–0,886; D 0,786 XA; stop X | tolerans; D formülü tabloda ters; TP kaynakları çelişiyor | Yok |
| BOS + Fib altın bölge (0,618–0,786) + FVG/OB | A §10 | **K** | Fib seviyeleri; stop Fib 1; TP1 Fib 0 (ikinci el) | BOS, FVG, OB tanımı | Tek örnek |
| Elliott 2. dalga (BRYAT) | C | **K** | Başlık şablonu; kurallar ikinci el (%10 itki, 0,50–0,786) | dalga sayımı | Sonuçsuz |
| Düşen direnç kırılımı + talep (LIDER/BALAT) | A, C | **K** | Temas 3, Lookback 20/30, EMA5/8/13 | talep bölgesi, kümülatif delta (veri yok) | LIDER olumlu, BALAT başarısız |
| Fincan-kulp (GUBRF) | B §21 | **K** | hedef = kırılım + derinlik; R/R 1:2,27 | dedektör, stop | Tek örnek |
| Gizli pozitif uyumsuzluk | B | **K** | Swing=15 sol, MinGap=15 | osilatör gizli | Seçilmiş |
| A/D–EMA(3) (ISCTR) | B | **K** | Strateji %19,1, B&H %10,8, Sharpe 0,67 | operatör yönü | Tek hisse |
| Bullish engulfing | B | H (tetik) | Kod birebir | bağlam, stop | Yok |
| Kelebek, Trident, Three Drives, X–B kırılımı | C | K | Bazı oranlar | çok | Seçilmiş |
| SETUP puanı, D.Touch/Teyit, Siyah/Beyaz Kuğu, BOM, AHENK, mavi çizgi, Pre Signal, gizli filtre | A, B, C | **X** | Yalnız etiket | Formül yok | — |

### Risk ve çıkış (E)
| Kural | Hazırlık | Not |
|---|---|---|
| Örnekte %1 risk, lot adedi = risk / (2 ATR) | H | NotebookLM, G115/g1 (Tansu paylaştı) |
| Acil stop: giriş − 2 ATR, gün içi dokunuşta çık | H | Ad: aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22; hesap: NotebookLM, G115/g1 |
| Gün sonu stopu: kapanış < SMA250 | H | Ad: aktarım, tweet-atr-risk-butcesi-position-sizing-stop-loss:22; çıkış örneği: NotebookLM, G115/g1; SMA250 seçimi: YORUM (TASARIM 5.5) |
| İz süren stop (+1,5 ATR), kısmi kâr, önceki gün dibi altı %50 | K | ikinci el; görselde yalnız bir STOP / ATR etiketi, rakamlar okunamaz (E K2) |
| Harmonik hedef merdivenleri (Excel %38,2 / SAYAS 1:1 ve %61,8) | K | kaynaklar çelişiyor |
| Durum etiketleri: AKTİF, TAMAMLANDI, TEPKİ_VERDİ, BOZULDU | H (ad) | eşikleri yok |
| Tepki penceresi: D sonrası 20 mum (görsel) / 10 gün (not) | K | çelişki |

### Piyasa durumu (D)
| Kural | Hazırlık | Not |
|---|---|---|
| Piyasanın Nabzı 4/5 (ilk 5 kutudan 4'ü olumlu) | K | NotebookLM; SMA 18/35 ile 20/50 çelişiyor |
| BIST + VIX 5 adım (SMA20/50, Heikin Ashi, VIX RSI200/SMA10) | K | NotebookLM; "VIX" = ABD VIX (YORUM: kaynak yalnız VIX der, D "Hangi VIX?"); Yahoo/FRED'de bedava |
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

Sürüm kapsamının sahibi TASARIM §3'tür. AB=CD ilk sürümde yoktur (gerekçe TASARIM §3, Sorgu 3). İkinci dalgada
geometri sadakati yönsüz yapılır. (bilet 04, 14.10)

**Ailelerin işlem kuralları (ilk sürüm):**

1. **Çift rotasyonu** (birinci el: giriş eşiği, ΔZ tanımı, yön, zaman). Ham fiyat bizim seçimimiz (YORUM). Örnek ham fiyatla uyumlu. Genel düzeltme politikası açık değil.
   - Sapma: log(Y) − log(X), ortalama ve standart sapma son 60 günden, standart sapma ddof 1 (YORUM; Tansu'nun Z'si
     üç sadakat turunda üretilemedi, §4 ve `docs/sadakat.md`: YORUM kalıcıdır). Sabit terim (α) yok; ortalama çıkarıldığı için Z aynıdır. (ddof: TASARIM 5.6; bilet 04, 14.10)
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
   - Oran: (en büyük EMA − en küçük EMA) / EMA200; EMA20/50/100/200, `ewm(adjust=False)` (KRDMD rakamlarıyla eşleşen formül, sadakatle çözüldü, §4;
     düşüş trendinde paydanın EMA200 mü en küçük EMA mı olduğu açıktır, TASARIM §8 madde 6; bilet 04, 14.10).
   - Sıkışma dönemi: oranın ≤ %1,2 olduğu art arda en az 3 gün; oranın eşiği aştığı ilk gün dönemi
     bitirir. Tansu'nun %1,2 ve 3 günü "örnekteki değer"dir.
   - Giriş (YORUM): dönem bittikten sonraki 10 gün içinde kapanış, dönemdeki en yüksek gün yükseğinin
     üstüne çıkarsa ertesi gün. Dönem başına tek giriş. Stop ve çıkış: risk paketi. Hedef yok.
   - Not: Tansu'nun ICBCT "Pre Signal"i sıkışma sürerken çıkıyor; bizim tetik bitişten sonra (YORUM).
   - K1 ön şartı: (a) türünde sıkışma dönemi bitmiş ve 10 günlük pencere açık günler; (b) türünde sıkışma penceresi şartı aranmaz, yalnız hisse düzeyi şartlar (kapanış ≥ SMA250, ısınma, evren, karantina) aranır (TASARIM 5.7; bilet 03). Ek kol: sıkışmasız aynı kırılım (kapanış önceki 20 günün en yüksek yükseğinin üstünde, sıkışma penceresinde değil; 20 YORUM, TASARIM 5.7).
   - Sağlamlık ızgarası (TASARIM 5.10, YORUM): eşik {%1,0; %1,2; %1,5}, en az gün {2; 3; 5}, giriş
     penceresi {5; 10; 20}. (İ: 06-072)

İkinci dalga ve kapsam dışı olanlar TASARIM §3'tedir. Diğer kurallar dizinde kalır; kaynak çıktıkça yükselir.

"Ertesi gün" sınamada nasıl modellendiği (Tansu'nun T+1 açılışı uygulanamaz): TASARIM 5.3.

**Risk paketi:** sahibi TASARIM §5.5–5.6'dır; kaynak notları E K1–K3'tedir. Çift rotasyonu bölmesi bu pakete tabi
değildir, çıkışı karşı uçta geçiştir (yukarıda aile 1).

## 4. Sadakat kontrolü (sınamadan önce)

YORUM'ları sonuca bakarak seçmek yasak. Ama Tansu'nun **kendi çıktılarındaki rakamları** yeniden üretmek
serbesttir; bu performans değil, kuralın doğru okunduğunun kanıtıdır.

| Aile | Tansu çıktısı | Yeniden üretilecek | Bu neyi çözer |
|---|---|---|---|
| Çift rotasyonu | VAKBN–GARAN raporu | son Z −3,108, önceki Z −3,404, 6 geçiş; Beta 1,675, korelasyon 0,731, piyasada kalma %72,27; Mart–Mayıs 2025'te sinyal yok | sapma formülü ve pencere |
| EMA sıkışması | KRDMD | sıkışma 17.12.2025–14.01.2026 (20 gün), ortalama oran %0,64 | oran formülü |
| AB=CD (ikinci dalga) | KRPLS, MARKA #13, SMRTG tablosu | D = 11,29 / 10,05 / 70,25; SMRTG hedef getirileri | pivot ayarı, yön |
| Kanal (ikinci dalga) | AEFES 03.09.2026 | alt bant 17,76; temas 3/3; genişlik +%15,3 | kanal çizim yöntemi |

Sonuçlar. Ölçülen değerler, aday sayıları ve toleranslar `docs/sadakat.md`'dedir (Sorgu 3 ölçümü: `docs/sorgu/sonuc-3-4.md`); burada yalnız karar durur.
- **EMA sıkışması çözüldü:** (en büyük EMA − en küçük EMA) / EMA200, ham kapanıştan `ewm(adjust=False)`. Yahoo
  serisiyle (Sorgu 3, tek Yahoo ölçümü; `docs/sadakat.md`'de yoktur) dönem ortalaması %0,638, 09.04.2026 EMA değerleri
  lejantla birebir, grafik sonu ve Mart tepesi görselle ±0,3 içindeydi. İş Yatırım ham serisinde (bilet 05) EMA200 sıkı
  toleransı geçmez; karar: sonuç **gevşek bantla üretildi**. Dönemi, günü ve ortalamayı tam tutan aday "son 3 yıl"dır
  (son 2 yıl da tutar; ikisi aynı sonucu verir). Neden: EMA200 uzun belleklidir; Tansu'nun veri başlangıcı
  bilinmiyor. Oran formülü değişmez. Sınamada veri başlangıcı sabit tutulur ve rapora yazılır (İ: 06-014).
- **Çift Z'si üretilemedi:** Sorgu 3, bilet 06 ve 10.10.2026 ek turu (aday listesi koşudan önce commit edildi, bf79a28)
  Tansu'nun Z'sini üretemedi (ayrıntı `docs/sadakat.md`). Karar: **YORUM kalıcıdır** (log oran, 60 gün); yeni tur açılmaz. VAKBN–GARAN
  örneğinin fiyatları ham okumayla uyumludur (araç, Rota/g2); genel fiyat düzeltme politikası açık değildir (TASARIM 5.1).
  Beta, korelasyon, piyasada kalma ve Mart–Mayıs 2025 kontrolleri formül olmadığı için yapılmadı.

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

## Kural içermeyen notlar (bilet 04, 14.10)

Havuzdaki her not A–E dosyalarında ya da bu belgede geçer. Aşağıdaki notlar işlem kuralı (giriş, çıkış, filtre, eşik) içermiyor. Okuma derinliği: kısa notlar baştan sona; uzun değerleme notlarında Ham, Sentez ve teknik başlıklar. Biçim: dosya adı · gerekçe. "Kapsam dışı: TASARIM §3": TASARIM 3 (değerleme, opsiyon).

gorsel-paket-04-tsla-implied-move · kapsam dışı: TASARIM §3 (opsiyon); ABD örneği, kural yok
gorsel-paket-97-iv-sd-expected-move-bantlari · kapsam dışı: TASARIM §3 (opsiyon IV); yazarı belirsiz ders metni, Tansu'nun kuralı değil
gorsel-paket-108-beta-risk-pusulasi · değerleme: beta tanımı, eşiksiz rejim görüşü
gorsel-paket-130-piyasa-evreleri-birikim-dagitim-semasi · kavram şeması, sayı yok
gorsel-paket-133-medyan-kanal-kullanimi · gösterge fikri, parametre yok (medyan: B §28)
gorsel-paket-14-isletme-analizi-kriterleri · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-16-temel-momentum-ters-faz · proje fikri, metrik ve eşik yok
gorsel-paket-19-eurtry-forward-monte-carlo · kur forward çalışması, kapsam dışı
gorsel-paket-22-hisse-karar-destek-pipeline · süreç şeması, eşik yok
gorsel-paket-23-froto-ppe-fiyat · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-24-merton-modeli · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-25-degerleme-agirliklandirma · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-27-asuzu-fk-ex-ante-zaman-cizgisi · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-28-proje-bugunku-deger-ve-teknik-kapi · değerleme, kapsam dışı: TASARIM §3; teknik kapı parametresiz
gorsel-paket-29-uc-yontem-rs-wacc-dcf-girdileri · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-30-fed-beklenti-altin-fiyatlama · haber: makro tablo
gorsel-paket-72-hbk-fiyat-bilanco-katalizoru · haber: bilanço; teknik teyit parametresiz
gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-77-asuzu-bottom-up-adet-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-79-arclk-aradonem-manuel-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-80-froto-basit-fk-fdfavok-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-81-froto-basit-fk-ileri-hedef-outcome · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-82-eregli-dcf-10y-ic-deger · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-83-eregli-tek-tus-dcf-konsol · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-84-dcf-varsayim-riski-sensitivity-reverse-mos · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-86-fcff-fcfe-ddm-coklu-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-87-cost-of-equity-total-beta · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-88-basit-capm-coe-python · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-89-fcff-fcfe-ddm-yontem-secim-matrisi · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-90-ebit-vergi-forecast-bilesik-buyume · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-91-dcf-fcff-adim-adim-degerleme · değerleme, kapsam dışı: TASARIM §3
gorsel-paket-94-ham-fiyat-getiri-risk-portfoy · eğitim
gorsel-paket-95-capm-portfoy-agirlik-risk-mutabakat · değerleme, kapsam dışı: TASARIM §3
kaynak-cme-group-volatilite-opsiyon-veri-araclari · kapsam dışı: TASARIM §3 (opsiyon veri aracı tanıtımı)
kaynak-ekonometri-hangi-soru-hangi-yontem-haritasi · eğitim: yöntem haritası
kaynak-stefan-jansen-ml-algo-trading · eğitim: kitap önerisi
tansu-calisma-kurallari · süreç notu, işlem kuralı değil
tweet-9aydan-yilsonu-satis-net-kar-tahmini · değerleme, kapsam dışı: TASARIM §3
tweet-arima-hiperparametre-acf-pacf-grid-search · eğitim: model seçimi
tweet-arz-talep-bolgesinde-formasyon-bekleyisi · sohbet; tekrar: tweet-formasyon-arz-talep-confluence-kapisi ham kaydı
tweet-asuzu-coklu-degerleme-tutarliligi · değerleme, kapsam dışı: TASARIM §3
tweet-aylik-getiri-mevsimsellik-piyasa-hafizasi · yazarı belirsiz ders metni, Tansu'nun kuralı değil; eşiksiz (planlı mevsimsellik: D)
tweet-beklenen-fk-coklu-regresyon-modeli · değerleme, kapsam dışı: TASARIM §3
tweet-birikim-sureci-kotu-haber-akilli-para · sohbet: Wyckoff anlatısı, kural yok
tweet-bist-hft-colocation-quant-rekabet-kod-ogrenin · görüş
tweet-cari-oran-likidite-acigi-bedelli-sermaye-artirimi · değerleme, kapsam dışı: TASARIM §3
tweet-convex-hull-dea-sektor-rotasyonu-projesi · proje fikri
tweet-dea-vza-sektor-rotasyonu-malmquist-projesi · proje fikri; yazarı belirsiz ders metni; aylık ya da çeyreklik
tweet-excel-degerleme-calismasi-koda-donusumu · değerleme, kapsam dışı: TASARIM §3
tweet-fcfe-ddm-capraz-kontrol-degerleme-motoru · değerleme, kapsam dışı: TASARIM §3
tweet-fiyat-grafigi-otesi-makro-bakis · haber: makro eğitim
tweet-froto-nakit-piyasa-degeri-18-89 · değerleme, kapsam dışı: TASARIM §3
tweet-gordon-buyume-modeli-temettu-degerleme · değerleme, kapsam dışı: TASARIM §3
tweet-nihai-hedef-tek-tus-temel-teknik-degerleme-llm-nlp · vaat: hedef beyanı
tweet-optimal-momentum-plus-simulasyon-tamamlandi · vaat
tweet-ozkaynak-artisi-varlik-finansman-yatirim-verimliligi · değerleme, kapsam dışı: TASARIM §3
tweet-pddd-roe-sektor-tarihsel-value-trap-filtresi · değerleme, kapsam dışı: TASARIM §3
tweet-pine-script-python-gorev-ayrimi-veri-backtest-icra · araç tercihi
tweet-python-ai-stratejik-yonetim-vizyon-misyon-kodlama · kurumsal proje, kapsam dışı
tweet-python-finans-verisi-ogrenme-yol-haritasi · eğitim
tweet-regresyon-ml-rasyolardan-piyasa-degeri-sapmasi · değerleme, kapsam dışı: TASARIM §3
tweet-relatif-degerleme-piyasa-norm-bantlari · değerleme, kapsam dışı: TASARIM §3
tweet-roc-nopat-yatirilan-sermaye-hesabi · değerleme, kapsam dışı: TASARIM §3
tweet-sirket-degerlendirme-sektor-isletme-finansal-degerleme-kontrol-listesi · değerleme, kapsam dışı: TASARIM §3
tweet-topsis-cok-kriterli-hisse-siralama-motoru · görüş: sıralama yöntemi, eşik yok
tweet-topsis-hisse-secimi-yaklasan-proje · proje fikri
tweet-ttrak-pddd-primi-carpan-sikismasi · değerleme, kapsam dışı: TASARIM §3

## Kısa atıfların tam adları (bilet 04, 14.10)

A–E dosyaları bazı notlara kısa adla atıf verir: `gorsel-paket-NN` notuna gp-NN, G-NN, GNN veya -NN; `tweet-X` notuna T-X; `kaynak-X-<tweet no>` notuna kaynak-X. Tam dosya adları (ad denetimi için):

gorsel-paket-01-harmonik-formasyon-tarama
gorsel-paket-02-coklu-sistem-provenance
gorsel-paket-03-smrtg-abcd-backtest
gorsel-paket-06-sektor-getiri-liderleri
gorsel-paket-07-sektor-anomali-temizleme
gorsel-paket-12-doas-advance-block
gorsel-paket-21-confluence-alan-taramasi
gorsel-paket-32-gartley-abcd-talep-dusen-kirilimi
gorsel-paket-33-min-vol-max-sharpe-dey-bist100
gorsel-paket-35-beyaz-kugu-sell-abcd-dusen-kirilimi
gorsel-paket-37-gunluk-rebalancing-aktif-pasif
gorsel-paket-38-akcns-haftalik-abcd-talep-ema
gorsel-paket-39-abcd-detector-fibo-talep-tepki
gorsel-paket-40-haftalik-abcd-talep-tepki
gorsel-paket-42-buy-abcd-yukselen-destek-hedefler
gorsel-paket-43-rysas-buy-abcd-kanal-baglamı (dosya adında ASCII dışı "ı" var)
gorsel-paket-47-lindsay-trident-abc-b-kirilimi-d
gorsel-paket-50-bist100-bist-volatilite-gulumsemesi
gorsel-paket-51-cimsa-oyakc-rotatif-zskor-portfoy
gorsel-paket-52-agrot-garan-duygusuz-disiplin-mtm
gorsel-paket-53-stat-arb-bag-kopusu-negatif-backtest
gorsel-paket-54-stat-arb-pairs-trading-kanonik-aciklama
gorsel-paket-55-volatilite-arbitraj-otonom-sistem-tercihi
gorsel-paket-57-tektu-eregl-agirlik-duyarliligi
gorsel-paket-59-buyhold-sinyal-risk-scorecard
gorsel-paket-62-froto-corwin-schultz-spread-sigma
gorsel-paket-69-przma-bullish-fvg-revisit-ote
gorsel-paket-96-momentum-161700-uclu-portfoy-aramasi
gorsel-paket-98-piyasanin-nabzi-teknik-rapor
gorsel-paket-99-klmsn-momentum-multitimeframe-bos-demand-fibo
gorsel-paket-101-avod-demand-bearish-fvg-supply-ema
gorsel-paket-102-enjsa-elliott-wave5-hikkake-fvg-outcome
gorsel-paket-107-bryat-smc-elliott-wave2-fvg-wave3
gorsel-paket-109-balat-harmonik-tp-cd-retracement
gorsel-paket-110-elliott-wave2-fib-fvg-yuzde8
gorsel-paket-111-elliott-5plus3-fibonacci-islem-gunleri
gorsel-paket-113-bist-vix-long-bes-adim-kontrol
gorsel-paket-114-bist-vix-python-master-analiz
gorsel-paket-115-position-sizing-yuzde1-2atr-sma250
gorsel-paket-116-veriden-sinyale-algoritmik-trader-gelistirme
gorsel-paket-118-yatirimci-basarisizlik-surec-risk-kontrol
gorsel-paket-120-fibonacci-coklu-aralik-konfluans
gorsel-paket-122-makim-gartley-fvg-momentum
gorsel-paket-123-gartley-algoritmik-takip-formul-mutabakati
gorsel-paket-125-kismi-kar-trailing-prev-low-emergency-stop
gorsel-paket-126-bist-order-book-derinlik-bmp-fit
gorsel-paket-127-aztek-istatistiksel-uc-kapitulasyon-obi-ayi-tuzagi
kaynak-kointegrasyon-sinirlari-2093658795700338821
kaynak-xu100-corwin-schultz-2096145981062475910
tweet-algoritma-tasarimi-temelleri-trading-sistemleri
tweet-garch-standart-sapma-volatilite-risk-minimizasyonu
tweet-kagit-kalem-matematik-once-kod-sonra
tweet-kendini-yenileyen-algoritma-ana-frekans
tweet-kitap-model-sentezi-backtest-forward-test-kod-mimarisi
tweet-likit-hisseler-etf-islem-derinligi-slippage-kapasite
tweet-piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi
tweet-volatilite-ters-orantili-position-sizing-sermaye-koruma
