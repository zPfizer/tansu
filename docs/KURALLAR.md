# Kural kataloğu (05.10.2026)

Kaynak: beyindeki Tansu havuzu (16.10 sayımı: 1.926 not, 1.848 görsel ve 1 PDF; 1.668 not X arşivinden eklendi, eleme kaydı
havuzda `x-arsiv/eleme.jsonl`). Ayrıntılar `docs/kurallar/A–E` dosyalarındadır;
bu belge onların dizini ve seçimidir. Her kuralın kaynağı, parametresi ve "YORUM" etiketi orada. X arşivi notları var olan
bölümlerde "Ek kaynaklar (X arşivi, 16.10)" bloğunda, yeni kurallar yeni bölümlerde, tek öğeli olanlar dosyanın
"X arşivi kısa kayıtları (16.10)" bölümündedir.

Okuma kuralları (birinci el, ikinci el, NotebookLM ve YORUM tanımları GLOSSARY'dedir):
- Kuralın dayanağı birinci el kaynaktır: notun Ham metni ve notun görselleri (NotebookLM görselleri dahil). Notun Ham dışı
  bölümü görselle çelişirse görsel geçerlidir (§1 madde 3).
- Notun öbür bölümleri (Sentez, Cevo çıkarımı, Kaynak kartı, Teknik Ek) ikinci eldir ve kural olarak tek başına kullanılmaz;
  "NotebookLM görseli" etiketi yalnız bilgi verir.
- Bir YORUM'un sınamada denenen her değeri yeni deneme sayılır; istisna: önceden yazılmış sağlamlık ızgarasının
  hücreleri ve masraf senaryoları deneme sayısına girmez (TASARIM 5.10, 5.11; İ: 09-056). Sadakat kontrolünde denenen
  aday formüller deneme sayısına girmez, p üretmez; seçilen formül kural kaydına girer (TASARIM 5.11, İ: 10-033, 04-090).

## 1. Ana bulgular

1. Tansu bazı kurallar için tam giriş + stop + hedef üçlüsü verir: gorsel-paket-105, -106 ve -107 Ham metinleri ve AKFIS
   görseli (ENTRY, STOP, TP1–3). gorsel-paket-58 Ham giriş (300.75), hedef (389.30) ve risk/ödül (1:2.27) verir; stop vermez.
   Sistematik çok sembollü sınama yoktur; yalnız tek sembollü tablolar vardır (SMRTG 12 patern, ISKPL 5 patern). Kanıtı
   seçilmiş örneklerdir; bazı başarısız örnekleri de paylaşır (BALAT, AKSGY, bağı kopan çift).
2. Talep/arz bölgesi üretim kuralı, temas toleransı ve SETUP puan formülü hiçbir yerde yok. Tepe/dip (pivot) ayarı
   yalnız gorsel-paket-60 görselinde görünür ("Swing=15 sol-only | MinGap=15"); konsolidasyon bölgesinin sınırı
   gorsel-paket-18 Ham'da tanımlıdır (en yüksek mumun gövde ucu, en düşük mumun gölge ucu).
3. Gartley takip tablosunda (gorsel-paket-123) D girişi `X + (A-X) * 0.786 (Boğa için)` yazılıdır; tablonun kendi TP
   formülleri D'nin A'nın altında olduğunu varsayar. Hata Tansu'nun tablosunun içindedir (YORUM: bizim hesabımız, C §7).
   Notun Ham dışı bölümü görselle çelişirse görsel geçerlidir.
4. 05.10 ön denemesindeki "4 ATR hedef" ve "EMA50 altı çıkış" Tansu kaynaklarında yok; kaldırılır.

## 2. Dizin

Hazırlık sütunu: H, K ve X anlamı için GLOSSARY "Hazırlık" maddesine bakın.

Her satırın kaynak okuması (parametre, sayı, Tansu'nun kanıtı, eksik YORUM'lar) "Bölüm" sütunundaki A–E bölümündedir; bu
dizin kaynak değerini yinelemez.

### Giriş aileleri
| Kural | Bölüm | Hazırlık |
|---|---|---|
| Çift rotasyonu | D, "Çift sistemi çekirdeği" | **K** |
| AB=CD + hedef merdiveni | C §3–5 | **K** |
| EMA sıkışması (KRDMD) | B §1 | **H** |
| Yükselen kanal alt bant teması (AEFES) | A §2 | **K** |
| Kırılım + range retest + FVG (AKFIS A+) | A §1 | **K** |
| Gartley | C §7 | **K** |
| BOS + Fib altın bölge + FVG/OB | A §10 | **K** |
| Elliott 2. dalga (BRYAT) | C §16 | **K** |
| Düşen direnç kırılımı + talep (LIDER/BALAT) | A §3; C §13 | **K** |
| Fincan-kulp (GUBRF) | B §21 | **K** |
| Gizli pozitif uyumsuzluk | B §9 | **K** |
| A/D–EMA(3) (ISCTR) | B §12 | **K** |
| Bullish engulfing | B §10 | H (tetik) |
| Kelebek, Trident, Three Drives, X–B kırılımı | C §8, §12, §15, §9 | K |
| SETUP puanı | A §5 | **X** |
| D.Touch / D.Teyit | A §6 | **X** |
| Siyah/Beyaz Kuğu | C §13 | **X** |
| BOM, AHENK, gizli filtre | A §16, §14 | **X** |
| Mavi çizgi, Pre Signal | B §8, §2 | **X** |
| Bottle pattern (iki mum) | B §33 | K |
| X arşivi kısa kayıtları | A §17, B §34 | X |

### Risk ve çıkış (E)
| Kural | Bölüm | Hazırlık |
|---|---|---|
| Risk bütçesi ve lot | E K1 | H |
| Acil stop | E K2 | H |
| Gün sonu stopu | E K3 | H |
| İz süren stop, kısmi kâr | E K4, K5 | K |
| Harmonik hedef merdivenleri | C §4, §11 (E K11) | K |
| Durum etiketleri | C §2 (E K15) | H (ad) |
| Tepki penceresi | C §10 (E K15) | K |
| ATR basamak merdiveni | E K25 | K |
| Momentum marjında kâr al (%3 günlük) | E K28 | K |
| Fon satış baskısı, fon risk radarı (hisse dışı; kapsam Levent kararı) | E K26, K27 | K, X |
| X arşivi kısa kayıtları (kripto dahil) | E K29 | X |

E K1–K3: kaynakları birinci eldir, bu yüzden H'dir. K1 ve K2 Ham'dadır (tweet-atr-risk-butcesi-position-sizing-stop-loss, Ham'da yazar yok; gorsel-paket-115). K3'ün SMA250 altı kapanış çıkışı gorsel-paket-115 NotebookLM görselindedir. ATR uzunluğu, dolum ve SMA250'nin giriş filtresi olarak seçimi YORUM'dur (E K1–K3).

### Piyasa durumu (D)
| Kural | Bölüm | Hazırlık |
|---|---|---|
| Piyasanın Nabzı 4/5 (NotebookLM) | D, "Piyasanın Nabzı" | K |
| BIST + VIX 5 adım (NotebookLM) | D, "Hangi VIX?"; "BIST VIX long: 5 adım kontrol listesi" | K |
| Sektör liderleri 30/60/90 gün + anomali temizleme | D, "Sektör rotasyonu" | H |
| Volatilite şoku freni | E K8 | X |
| Aylık mevsimsellik eleme tablosu | D, "Aylık mevsimsellik: istatistiksel eleme tablosu" | K |

## 3. Seçim

**Ölçütler (seçimden önce yazıldı):**
1. Giriş kuralının çekirdeği birinci elden belli.
2. Bedava günlük veriyle uygulanabilir.
3. Tansu sayısal bir sonuç göstermiş (sınanacak bir iddia var).
4. Seçilenler birbirinden farklı türde olsun (aynı fikri iki kez sınamamak için).

**İlk sürümde sınanacak aileler:**
| Sıra | Aile | Neden | En önemli YORUM |
|---|---|---|---|
| 1 | Çift rotasyonu | 4 ölçütün hepsi; sayısal çıktısı var (VAKBN–GARAN raporu, §4) | sapma formülü ve pencere |
| 2 | EMA sıkışması | parametreler birinci el; oran formülü sadakatle seçildi (YORUM, aşağıda) | giriş tetiği |

Sürüm kapsamının sahibi TASARIM §3'tür. AB=CD ilk sürümde yoktur (gerekçe TASARIM §3, Sorgu 3). İkinci dalgada
geometri sadakati yönsüz yapılır. (bilet 04, 14.10)

**Ailelerin işlem kuralları (ilk sürüm):**

1. **Çift rotasyonu** (kaynak okuması: D, "Çift sistemi çekirdeği"). Sinyal hesabı düzeltilmiş seriden yapılır; ham seri yalnız sadakat kontrolündedir (TASARIM 5.1).
   - Sapma: log(Y) − log(X), ortalama ve standart sapma son 60 günden, standart sapma ddof 1 (YORUM; Tansu'nun Z'si
     üç sadakat turunda üretilemedi, §4 ve `docs/sadakat.md`: YORUM kalıcıdır). Sabit terim (α) yok; ortalama çıkarıldığı için Z aynıdır. (ddof: TASARIM 5.6; bilet 04, 14.10)
   - Z ≤ −2 ve ΔZ > 0 → ertesi gün Y'ye geç. Z ≥ +2 ve ΔZ < 0 → ertesi gün X'e geç. Tek günlük ΔZ
     yeterlidir (YORUM; kaynak ΔZ'yi tanımlar, kaç günlük onay gerektiğini söylemez: D).
   - İlk sinyale kadar nakit; sonra hep bir hissede (YORUM; genel nakit politikası kaynakta açık değil,
     TASARIM 5.6). Ayrı stop yok (YORUM; kaynak stop politikasını açıklamaz, TASARIM 5.5).
   - Çiftler önceden yazılmış kuralla seçilir (TASARIM 5.6).
   - K1 ön şartı: çift seçilmiş ve |Z| ≥ 2 olan günler.
   - Sağlamlık ızgarası (TASARIM 5.10, YORUM): Z penceresi {60; 120}, eşik {1,5; 2; 2,5}, seçim p'si
     {0,01; 0,05; 0,10}. (İ: 04-089)
2. **EMA sıkışması kırılımı** (Tansu parametre vermez; tek sayısı gorsel-paket-65 Ham'daki "Bir günde %5 Ema
   sıkışması"dır, anlamı açık değil. Bu ailenin getiri iddiası bizim hipotezimizdir, İ: 10-002)
   - Oran: (en büyük EMA − en küçük EMA) / EMA200; EMA20/50/100/200, `ewm(adjust=False)`. Formül görselde yok (B §1); sadakat
     kontrolüyle KRDMD örneğinde eşleşti, KRDMD dışında doğrulanmadı (YORUM, §4; düşüş trendinde paydanın EMA200 mü
     en küçük EMA mı olduğu açıktır, TASARIM §8 madde 6; bilet 04, 14.10).
   - Sıkışma dönemi: oranın ≤ %1,2 olduğu art arda en az 3 gün; oranın eşiği aştığı ilk gün dönemi
     bitirir. Tansu'nun %1,2 ve 3 günü "örnekteki değer"dir.
   - Giriş (YORUM): dönem bittikten sonraki 10 gün içinde kapanış, dönemdeki en yüksek gün yükseğinin
     üstüne çıkarsa ertesi gün. Dönem başına tek giriş. Stop ve çıkış: risk paketi. Hedef yok.
   - Not: Tansu'nun ICBCT "Pre Signal"i sıkışma sürerken çıkar (B §2); bizim tetik bitişten sonradır (YORUM).
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

| Aile | Tansu çıktısı | Hedef değerler (sahibi) | Bu neyi çözer |
|---|---|---|---|
| Çift rotasyonu | VAKBN–GARAN raporu | D, "Tansu'nun kanıtı" ve "Çift sistemi çekirdeği" | sapma formülü ve pencere |
| EMA sıkışması | KRDMD | B §1 | oran formülü |
| AB=CD (ikinci dalga) | KRPLS, MARKA #13, SMRTG tablosu | C §3, §5 | pivot ayarı, yön |
| Kanal (ikinci dalga) | AEFES 03.09.2026 | A §2 | kanal çizim yöntemi |

Sonuçlar. Ölçülen değerler, aday sayıları ve toleranslar `docs/sadakat.md`'dedir (Sorgu 3 ölçümü: `docs/sorgu/sonuc-3-4.md`); burada yalnız karar durur.
- **EMA sıkışması çözüldü** (KRDMD örneğinde; KRDMD dışında doğrulanmadı): oran formülü §3 aile 2'dedir. İş Yatırım ham serisinde (bilet 05) EMA200 sıkı toleransı geçmez; karar: sonuç **gevşek
  bantla üretildi**; veri başlangıcı olarak "son 3 yıl" seçildi (ölçümler ve aday sonuçları `docs/sadakat.md`). Neden: EMA200
  uzun belleklidir; Tansu'nun veri başlangıcı bilinmiyor. Oran formülü değişmez. Sınamada veri başlangıcı sabit tutulur ve
  rapora yazılır (İ: 06-014).
- **Çift Z'si üretilemedi:** Sorgu 3, bilet 06 ve 10.10.2026 ek turu (aday listesi koşudan önce commit edildi, bf79a28)
  Tansu'nun Z'sini üretemedi (ayrıntı `docs/sadakat.md`). Karar: **YORUM kalıcıdır** (log oran, 60 gün); yeni tur açılmaz.
  Beta, korelasyon, piyasada kalma ve Mart–Mayıs 2025 kontrolleri formül olmadığı için yapılmadı. Fiyat serisi politikası:
  TASARIM 5.1.

Veri: Kontrol İş Yatırım ham seriyle yapılır (TASARIM 5.1). Yahoo ölçümü: `docs/sorgu/sonuc-3-4.md` O9.

Kural:
- Tolerans, adaylar denenmeden önce yazılır. "Üretti" = Tansu'nun gösterdiği son hanenin yarısı içinde
  (Z için ±0,0005). Gevşek bant (±0,05) yalnız tek aday kalırsa kullanılır. (İ: 04-002, 14-058)
  Aynı dönemi ve gün sayısını veren, ölçülen her değeri (ortalama, EMA'lar) birbirinden en çok `docs/sadakat.md` başındaki
  toleransla (gösterilen son hanenin yarısı, ±0,005) ayrılan adaylar eşdeğerdir ve tek aday sayılır. EMA'da son 3 yıl ve son
  2 yıl böyledir; ölçülen değerler `docs/sadakat.md` EMA tablosundadır. (bilet 05, 14.10)
- Birden çok aday formül denenir; Tansu'nun rakamını en iyi üreten seçilir.
  En iyi: ölçülen değerlerin Tansu'nun rakamlarından mutlak farklarının toplamı en küçük olan aday; eşitlikte aday
  sırasındaki ilk aday (bilet 07a, 14.10). Çift Z'si için aday
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
  rotasyon değildir (iki bacak + nakit) ve borsapy'ye göre farklı sektördedir (bizim veri: borsapy; Tansu iddiası değil).
- NotebookLM görselleri birinci eldir (GLOSSARY); Tansu'nun kendi kuralı olmayabilir.

## Kural içermeyen notlar (bilet 04, 14.10)

Havuzdaki her not A–E dosyalarında ya da bu belgede geçer. Aşağıdaki notlar işlem kuralı (giriş, çıkış, filtre, eşik) içermiyor. Yazarı belirsiz bir metindeki kural "kural içermez" sayılmaz; A–E'de "Ham; Ham'da yazar yok" etiketiyle yazılır (ör. DEA/VZA ve aylık mevsimsellik notları: D, "Sektör rotasyonu"). Bir değerleme notu filtre ya da eşik taşıyorsa girdisinde yazılır; kapsamı TASARIM §3 dışarıda bırakır. Okuma derinliği: kısa notlar baştan sona; uzun değerleme notlarında Ham, Sentez ve teknik başlıklar. Biçim: dosya adı · gerekçe. "Kapsam dışı: TASARIM §3": TASARIM 3 (değerleme, opsiyon).

gorsel-paket-04-tsla-implied-move · kapsam dışı: TASARIM §3 (opsiyon); ABD örneği, kural yok
gorsel-paket-108-beta-risk-pusulasi · değerleme: beta tanımı; görsel rejime göre beta eşiği verir (boğada Beta > 1, ayıda Beta < 1); kapsam dışı: TASARIM §3
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
tweet-akd-matrix-iq-gunluk-veritabani-1964445184328159257 · araç tercihi, veri kaynağı (AKD Matrix IQ'dan alınıyor, günlük veri tabanı planı); kural öğesi yok
tweet-akd-veri-kaynagi-api-1941449822050848997 · araç tercihi, veri kaynağı (AKD için Matrix IQ ve Algolab); kural öğesi yok; tekrar: tweet-akd-matrix-iq-gunluk-veritabani-1964445184328159257
tweet-analitik-ag-sureci-hisse-secimi-1944868638307311952 · eğitim (Analitik Ağ Süreci yöntem anlatımı); eşik, parametre ve ölçülen sonuç yok
tweet-arima-hiperparametre-acf-pacf-grid-search · eğitim: model seçimi
tweet-arz-talep-bolgesinde-formasyon-bekleyisi · sohbet; tekrar: tweet-formasyon-arz-talep-confluence-kapisi ham kaydı
tweet-arz-talep-denge-fiyati-kodu-1906972824842965372 · eğitim (iktisat alıştırması: Qd=100-2P, Qs=50+3P Python kodu); arz-talep bölgesi (demand/supply) değil, kural öğesi yok
tweet-asuzu-coklu-degerleme-tutarliligi · değerleme, kapsam dışı: TASARIM §3
tweet-atr-tabanli-stop-seviyesi-1987562052194644270 · tarama çıktısı, kural öğesi yok (konu: E K2): TAVHL için "STOP: 247.20, ATR: 8.90, AL" etiketi, giriş fiyatı ve koşul yok
tweet-aylik-ortalama-maliyet-birikim-1783840694043623592 · kişisel yatırım alışkanlığı (aylık düzenli alım, ortalama maliyet, hedef 2028-2030); kural öğesi yok
tweet-az-yatirimcili-fon-risk-kontrolu-1979721927809012208 · eğitim, fon riski uyarısı (11 yatırımcılı fon örneği); kapsam dışı (fon, hisse değil); eşik yok
tweet-beklenen-fk-coklu-regresyon-modeli · değerleme, kapsam dışı: TASARIM §3
tweet-beklenti-al-gerceklesen-sat-2085043282694779123 · görüş: slogan, ölçülür giriş veya çıkış koşulu yok
tweet-beta-formul-rejime-gore-secim-2001638298473894378 · değerleme, kapsam dışı: TASARIM §3; beta tanımı (kovaryans / varyans); görsel rejime göre beta eşiği verir (boğada Beta > 1, ayıda Beta < 1, yatayda Beta ≈ 1.0); eşik sayısı yok, aynı içerik gorsel-paket-108-beta-risk-pusulasi
tweet-birikim-sureci-kotu-haber-akilli-para · sohbet: Wyckoff anlatısı, kural yok
tweet-bist-hft-colocation-quant-rekabet-kod-ogrenin · görüş
tweet-cari-oran-likidite-acigi-bedelli-sermaye-artirimi · değerleme, kapsam dışı: TASARIM §3
tweet-convex-hull-dea-sektor-rotasyonu-projesi · proje fikri
tweet-enflasyon-farki-pi-pi-yildiz-1907020125770772606 · makro gösterge tanımı (π − π* = yerli eksi yabancı enflasyon, örnek %13 ve %2 için ≈ 0,11); eşik ve kural yok, üst gönderi notta yok
tweet-envanter-azaltma-monte-carlo-pnl-1924523925683274094 · proje anlatısı: kavramsal Monte Carlo simülasyonu (5 envanter stratejisi, 100.000 senaryo, 3 piyasa koşulu); sayısal sonuç ve eşik yok, yalnız kavramsal ilke (yükselen trendde yavaş, düşen trendde hızlı sat)
tweet-evds-api-mevduat-faizi-cekme-1766868425815535946 · veri çekme kodu (EVDS API, seri TP.TRY.MT02: TL 3 aya kadar mevduat faizi) ve makro görüş (faiz, enflasyon); kural öğesi yok
tweet-excel-degerleme-calismasi-koda-donusumu · değerleme, kapsam dışı: TASARIM §3
tweet-fcfe-ddm-capraz-kontrol-degerleme-motoru · değerleme, kapsam dışı: TASARIM §3
tweet-finansal-veri-api-kaynaklari-1762361028178796875 · araç tercihi: veri API listesi (Nasdaq Data-on-Demand, Alpha Vantage, Intrinio, IEX Cloud); BIST için kural öğesi yok
tweet-fiyat-grafigi-otesi-makro-bakis · haber: makro eğitim
tweet-fon-cikisi-satis-baskisi-tahmini-2099970636386812395 · proje fikri ve soru: fon çıkışının satış baskısını tahmin etme, geçmiş KAP raporlarıyla güven skoru; model, formül ve sonuç yok (konu: yeni fon çıkışı bölümü, E)
tweet-fon-net-akis-getiri-tarama-2094913511986020386 · tarama çıktısı, kural öğesi yok (fon sıralama tablosu: 1G/5G/20G net akış, 20G getiri, Sharpe sütunları; konu: fon-risk-radari)
tweet-fon-ortak-agirlik-degisimi-birikim-2096343856476496081 · vaat / proje fikri: fon ağırlık değişimi ve ortak hareket analizi duyurusu, ölçü ve eşik yok (konu: fon-risk-radari)
tweet-fon-para-akisi-analizi-2097019577112600707 · fon yorumu (KHP para piyasası fonu), eşik yok; kural öğesi yok (konu: fon-risk-radari)
tweet-froto-nakit-piyasa-degeri-18-89 · değerleme, kapsam dışı: TASARIM §3
tweet-gordon-buyume-modeli-temettu-degerleme · değerleme, kapsam dışı: TASARIM §3
tweet-gun-saat-satis-heatmap-pivot-1764250055114899657 · dış kapsam: pazarlama satış analitiği (gün-saat ısı haritası, perakende verisi), BIST işlem kuralı yok
tweet-hareketli-ortalama-backtest-araci-1979931015771517315 · araç tercihi: harici hareketli ortalama backtest sitesi bağlantısı ("Kaydedin lazım olur"), kural öğesi yok
tweet-iq-csharp-python-veri-hatti-1964627639425270263 · araç tercihi: veri hattı (IQ verisi C# kodu ile çekilir, Python'da işlenir; API yok), kural öğesi yok
tweet-iq-excel-python-akd-verisi-1970561329590354082 · araç tercihi: veri alımı (IQ Excel eklentisi + Python; AKD verisi, yf yetmez), kural öğesi yok
tweet-is-yatirim-bilanco-veri-toplama-1942613749073879070 · eğitim: bilanço verisini İş Yatırım'dan otomatik toplayıp klasörde havuzlama önerisi; veri yöntemi, değerleme tarafı (kapsam dışı: TASARIM §3), kural öğesi yok
tweet-isyatirim-financial-data-source-1889446483449037295 · araç tercihi: İş Yatırım finansal verisi (class tipi kodla erişim), değerleme verisi (kapsam dışı: TASARIM §3), kural öğesi yok
tweet-kmeans-silhouette-pca-kume-gorsellestirme-1762356653779763260 · eğitim: müşteri kümeleme (K-means, silhouette, PCA) kod örneği; ürün/kargo verisi, trade kuralı yok (havuz etiketi: dış kapsam)
tweet-nihai-hedef-tek-tus-temel-teknik-degerleme-llm-nlp · vaat: hedef beyanı
tweet-optimal-momentum-plus-simulasyon-tamamlandi · vaat
tweet-ozkaynak-artisi-varlik-finansman-yatirim-verimliligi · değerleme, kapsam dışı: TASARIM §3
tweet-pddd-roe-sektor-tarihsel-value-trap-filtresi · değerleme: Ham bir filtre verir (düşük PD/DD + yüksek ROE + sektör altı çarpan; 36 çeyrek çıpa); kapsam dışı: TASARIM §3
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
