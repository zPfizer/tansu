# Cevaplar 04: Çift rotasyonu

Kaynak kısaltmaları: D = `docs/kurallar/D-cift-portfoy-nabiz.md`; K = `docs/KURALLAR.md`; T = `docs/TASARIM.md` taslak 5; S2 = `docs/sorgu/sorgu-2.md`.
Kontrol edilenler: `rapor.webp` ve `grafik.webp` görselleri okundu; statsmodels `coint` imzası; ddof/üst sınır/binom hesapları (python `-c`).
Görselden yeni okunan: strateji çizgisi Temmuz 2025'e kadar düz (veri başlangıcından ≈6 ay), Z serisi ≈3 ay sonra başlıyor; Mart–Mayıs 2025'te Z ≈ −2,0/−2,3'e inip dönüyor ama sinyal yok; grafikte 6 AL etiketi var (GARAN, VAKBN, GARAN, VAKBN, GARAN, VAKBN); Temmuz 2025'te Z tek günde ≈ −2,5'ten +1,6/+4'e çıkıyor.

**04-001** — YANLIŞ — K §3.1 `log(Y) − β·log(X)` (α yok), D `ε = log Y − α − β·log X`: iç tutarsızlık. Z = (ε − ort)/std olduğu için sabit α ortalamayla birlikte düşer; Z aynıdır. Fark yalnız ε'nın düzeyinde. Düzeltme: K §3.1'e "α yok; ortalama çıkarılır, α etkisizdir" yaz; β'yı pencerede OLS (sabitli) ile tahmin etmek serbest.

**04-002** — EKSİK — Tolerans yazılı değil. Rapor Z'yi 3 ondalıkla veriyor: yuvarlama payı ±0,0005. Düzeltme (YORUM): "üretti" = iki sayı da ±0,0005 içinde; ayrıca gevşek bant ±0,05 (veri kaynağı farkı için). Yalnız gevşek bantta tek aday kalıyorsa kabul; hiçbiri gevşek bantta yoksa "bulunamadı" → log(Y) − log(X), 60 gün.

**04-003** — EKSİK — D "dönem ucu yok" diyor; grafik ≈ Oca 2025–Eyl 2026. Düzeltme (YORUM): rapor tarihi de bilinmeyen sayılır. 2025-04..2026-10 arası her işlem günü t için (Z_t, Z_{t−1}) hesaplanır; −3,108 ve −3,404 çifti birlikte aranır. Eşleşen gün listesi sonuçla birlikte yazılır.

**04-004** — OLGU — Hesapladım (normal yaklaşım, σ≈1): bir günde Z'nin −3,108 ± 0,0005 içinde olma olasılığı ≈3·10⁻⁶; iki ardışık sayı birlikte ≈10⁻⁸ ila 10⁻⁹. 4 aday × ~400 gün için yanlış eşleşme ≈10⁻⁵. Yani risk çoklu eşleşme değil, hiç eşleşmeme (veri farkı). Düzeltme: K §4 hedef listesine rapordaki öbür sayıları ekle: Beta 1,675, Rolling Corr 0,731, Beta CV 0,277, p 0,048 (D: GÖRSEL). Bunlar β penceresini ve β türünü bağımsız sınar.

**04-005** — EKSİK — T/K sessiz. S2-24 yalnız "β geçmişten" diyor. Düzeltme (YORUM): canlıda Z_{t−1} o gün hesaplanıp saklanan değerdir (nokta-zamanlı); simülasyonda Adım fonksiyonu aynı şeyi yapar. Tansu'nun hangisini yaptığı bilinmiyor (kaynak yok); sadakatte iki biçim aday olarak denenir.

**04-006** — OLGU — Doğruladım. Pencerede t dahilse ddof=0 için |Z| ≤ √(n−1): n=60 → 7,68; n=120 → 10,91. ddof=1 için (n−1)/√n: 7,62 / 10,86. ±2 eşiği etkilenmez. Düzeltme gerekmez; yalnız "pencere t dahil" yazılsın (04-007 ile).

**04-007** — OLGU — Doğruladım: ddof=1/ddof=0 oranı √(n/(n−1)): n=60 → 1,0084; n=120 → 1,0042. −3,108 → −3,134 olur; 3 ondalıkta ayırt edilir (ΔZ'nin 0,30'unun %9'u kadar). Tansu pandas `rolling.std` (ddof=1) kullanmış olabilir (YORUM, kaynak yok). Düzeltme: ddof'u sadakat adaylarına ekle; varsayılan ddof=1.

**04-008** — EKSİK — Bilinçli olduğuna dair kaynak yok. T §5.6 252 gün (YORUM), K Z penceresi 60/120 (YORUM); Tansu'nun p penceresi bilinmiyor (D). İki ayrı soru: "çift seçilir mi" ve "bugün sapma var mı". Düzeltme: T §5.6'ya "seçim penceresi Z penceresinden bağımsız ve YORUM" yaz; 252 parametre kaydına girsin.

**04-009** — EKSİK — Half-life Tansu'da boş (D). Tasarım kullanmıyor; yarı ömrü Z penceresinden uzun çiftte ±2 eşiği "pencere içi sapma"yı ölçer, dönüş beklentisini değil. Düzeltme: half-life'ı kapı yapma (kaynak yok); seçilen çiftler için tanısal sütun olarak raporla (AR(1) ile), ve yarı ömrü Z penceresini aşan çiftlerin sonuç payını ayrı yaz.

**04-010** — EKSİK — T/K sessiz. D: Tansu'da X = referans (GARAN; CIMSA), seçim kuralı bilinmiyor. `coint(y0,y1)` p'si yöne göre değişir. Düzeltme (YORUM): rol sembol sırasına göre sabit (alfabetik) atanır, p'ye bakılmadan. p'yi küçülten yön seçmek yanlılıktır; seçilmesin. İki yönün p'sinin farkı tanısal olarak raporlansın.

**04-011** — EKSİK — T/K sessiz. D: Tansu'nun β'sı 1,675 (pozitif). Düzeltme (YORUM): seçimde β ≤ 0,2 (ya da ≤ 0) olan çift elenir; yıl içinde β bu sınırın altına inerse çift sinyal vermez ve gün sayısı raporlanır. Yön anlamı (Z<−2 → Y ucuz) yalnız β>0 için anlamlı.

**04-012** — EKSİK — D: rolling beta ≈30 gün (düşük güven), Beta CV 0,277; tasarım β istikrarına bakmıyor. K: "β ve ortalama/std yuvarlanan pencerede". Düzeltme (YORUM): β penceresi = Z penceresi (tek pencere parametresi); β istikrarı (CV) tanısal sütun. Tansu'nun 30 günlük çizgisi grafik gösterimidir, işlem β'sı olduğu kanıtlı değil.

**04-013** — OLGU — Çarpımsal (oran) düzeltme için sızıntı yok: gelecekteki katsayı pencere içindeki bütün tarihleri aynı çarpanla ölçekler; log serilerde sabit kayma olur. ε sabit kayar, Z (ortalama çıkarılmış, std aynı) değişmez; Engle–Granger p'si de değişmez. Yalnız matematik olarak doğruladım, İş Yatırım verisinde denemedim. T §5.1 zaten Yahoo'yu kullanmıyor (yalnız sadakat). Düzeltme: HGDG düzeltmesinin çarpımsal olduğunu ilk veri işinde `HGDG/HG` oranının parça-sabit olmasıyla doğrula.

**04-014** — CEVAPLI — T §5.1: bir bacağın getirisi günlük limiti (+%0,5) aşıyorsa ve şirket olayı yoksa karantina; limit içinde kalan sıçrama gerçek sayılır. Görselde Temmuz 2025'te Z tek günde ≈ −2,5'ten +1,6'ya, iki gün sonra +4'e çıkıyor ve sinyal etiketleri tam bu sıçramada. Ek: sadakat raporuna "Tansu'nun Z sıçraması bizim verimizde de var mı" satırı.

**04-015** — EKSİK — S2-28: tek gün yeterli. Sahte dönüş sayısı raporlanmıyor. Düzeltme (YORUM): sinyal günlerinde ΔZ dağılımı (medyan, %10) raporla; eşik ekleme (kaynak yok, Tansu rakamı +0,30 gösteriyor).

**04-016** — YANLIŞ — D madde 2b: ΔZ = Z_t − Z_{t−1} rakamla doğrulandı (−3,108 − (−3,404) = +0,296): tanım birinci el. Ama "tek gün yeterli" D madde 4'te açıkça YORUM, ve D "K/M gün sürekliliği veya tampon görünmüyor" diyor (görünmemek yokluk kanıtı değil). S2-28 "Tansu'nun raporu öyle" kanıtı aşıyor. Düzeltme: S2-28'i "ΔZ tanımı birinci el; tek gün yeterliliği YORUM" diye yeniden yaz.

**04-017** — EKSİK — Görselde doğruladım: Mart–Mayıs 2025'te Z ≈ −2,0 / −2,3'e inip dönüyor, strateji düz (nakit), ilk etiket Temmuz'da. Olası nedenler (hepsi YORUM): strateji ısınması ≈6 ay (veri başlangıcından), p kapısı, pencere. Tasarım "Z≤−2 ve ΔZ>0" kuralıyla bu günlerde sinyal üretirse çelişir. Düzeltme: sadakat kontrolüne "bu dönemde sinyal yok" koşulunu ekle; adaylar (ısınma 60/120, p kapısı) buna göre elenir.

**04-018** — EKSİK — Önce premis: Z −2,5'ten yükselirken ΔZ>0 her gün olur ve Z≤−2 olduğu ilk günde Y sinyali çıkar. Sorun üst ucta: Z≥2 ve ΔZ<0 olana kadar Y'de kalınır. K §3.1 buna izin veriyor (bilinçli onay). Düzeltme: raporda "Z≥2 iken Y'de geçen gün sayısı" ve bu günlerin getirisi yazılsın.

**04-019** — EKSİK — T/K sessiz; veri satırı yoksa/hacim 0 ise ne olduğu yazılı değil. Düzeltme (YORUM): hacmi 0 olan bacak günü eksik sayılır, fiyat ileri taşınmaz; Z o gün güncellenmez ve ΔZ üretilmez (sinyal yok). T §5.1 "hacim olağandışıysa kart üretilmez" bunun canlı karşılığıdır.

**04-020** — CEVAPLI — K §3.1: "İlk sinyale kadar nakit; sonra hep bir hissede". D %72,27 piyasada kalma; 100 − 72,27 = 27,73 (D'nin grafik tahmini %28,5; yakın). Grafikte strateji çizgisi Temmuz 2025'e kadar düz: kural yeniden üretir. Düzeltme: %72,27'yi ikincil sadakat hedefi yap (04-097).

**04-021** — EKSİK — Nakit dönemi stratejinin parçasıdır ve Tansu'nun kendi karşılaştırması da (50/50 baştan yatırımda, grafik) aynı. Ama adilliği okumak için yatırımlı gün oranı gerekir. Düzeltme: rapora "yatırımlı gün oranı" ve nakit faiz payı satırı.

**04-022** — EKSİK — K "ilk sinyale kadar nakit"; yıl başında yeni çift için yazılı değil (S2-25 yalnız "pay yeni çifte geçer"). Düzeltme (YORUM): yeni çift ilk sinyalini bekler (nakitte, faiz kazanır); düşen çiftin pozisyonu satılıp payı nakit olur. Her yıl ortalama nakit gün oranı raporlansın.

**04-023** — EKSİK — T §5.6 faiz var, 5.12.2 "nakit faiz dahil". Ayrıştırma yok. Düzeltme: raporda faiz getirisi ayrı satır; K1'e de aynı nakit kuralı uygulanır (04-055), böylece fark faizden değil seçimden gelir.

**04-024** — EKSİK — T §5.6 "2015–2017 politika faizi, sonrası TLREF" der; T §4 "TLREF yalnız 2018 sonrası" der. 2018 ya da bir kısmı örtülü değil (TLREF'in ilk yayın günü doğrulanmadı, kaynak yok). Düzeltme: tek kesme tarihi yaz ("TLREF'in ilk yayın gününe kadar politika faizi") ve veri işinde bu günü bul.

**04-025** — CEVAPLI — T §5.6: bölme tek sermaye eğrisidir; MaxDD bu eğriden ölçülür, yoğunlaşma (en çok 5 hisse) zaten içinde. Portföy kuralı (m5) ilk sürümde bölme düzeyinde okunur (04-049).

**04-026** — CEVAPLI — Seçim önceki 252 günde, değerlendirme sonraki yılda (T §5.8 ileri yürüme). Kazananın laneti geçmiş p için bozucudur, ileri sonuç için değil. Ek ölçüt: 04-028 (ertesi yıl p). D: FDR "Claude önerisi" (Tansu'da yok).

**04-027** — OLGU — Doğruladım: `coint(y0, y1, trend='c', method='aeg', maxlag=None, autolag='aic')`. Tansu'nun p=0,048'i için test, pencere, gecikme: kaynak yok. Düzeltme: T §5.6'ya "statsmodels `coint`, trend='c', autolag='aic', y0=Y, 252 gün, log fiyat" yaz (YORUM); p=0,048 sadakat hedefi olarak denensin (04-004).

**04-028** — EKSİK — T/K sessiz. Düzeltme: seçilen çiftlerin ertesi yıl `coint` p<0,05 kalma oranı tanısal olarak raporlansın; kabul kararına girmez. Beklenen ~%5–15 ise seçim kuralı eşbütünleşmeyi öngörmüyor demektir.

**04-029** — EKSİK — T §5.6 "ayrıca gösterilir" yöntemini yazmıyor. Düzeltme (YORUM): üç Tansu çifti ayrı birer çift bölmesi olarak koşar: sabit çift, tüm dönem, seçim ve sektör kuralı yok, aynı sinyal ve maliyet kuralı. AGROT–GARAN için 04-083.

**04-030** — EKSİK — Bir hisse bir çiftte kuralı seçim içindir. Düzeltme: Tansu çiftleri ayrı koşulur (üçü ayrı bölme, her biri tek çiftli); sonuçlar yan yana tabloda, birleştirilmez, kabula girmez.

**04-031** — EKSİK — T/K sessiz ("p'si en iyi çift kalır"). Düzeltme (YORUM): çiftler p'ye göre sıralanır, hisseleri kullanılmış olan atlanır, 5 çifte ya da adaylar bitene kadar devam edilir. Aksi halde 5'ten az çift sistematik çıkar.

**04-032** — EKSİK — Düzeltme (YORUM): pay çift başına sabit 200.000 TL ilk dağıtımda; çift yoksa o pay bütün yıl nakitte politika faizi kazanır, kalan çiftlere devredilmez (devir, yoğunlaşmayı artırır). Boş pay sayısı raporlanır.

**04-033** — EKSİK — S2-21 "küçük yanlılık" diyor, ölçüm yok ve geçmiş sektör verisi bulunamıyor (kaynak yok). Düzeltme: "küçük" sözünü kaldır, "büyüklüğü bilinmiyor" yaz. K1 aynı çiftleri kullandığı için yanlılık göreli kıyasta kısmen iptal olur.

**04-034** — EKSİK — Tasarım içinde iki ad: §3/§5.6 "BIST100", §5.2 ve S2-19 aylık nokta-zamanlı en büyük 100 (60 günlük medyan TL şartı). S2-19 son karardır. Düzeltme: §5.6'ya "evren = §5.2 ara evreni, yılın ilk ayındaki üyeler" yaz; yıl içinde evrenden düşen hissede çift sabit kalır (YORUM), kapanırsa 04-043.

**04-035** — EKSİK — Düzeltme (YORUM): seçim, önceki yılın son işlem günü kapanışına kadar veriyle; ilk işlem sinyalin ertesi işlem günü AOF'u. Seçim ile ilk sinyal arası sızıntı yoktur çünkü Z, aynı pencerenin geçmişinden hesaplanır.

**04-036** — EKSİK — T §5.8 "2015–2017 ile başlar" yalnız tek hisse ailelerini düşünür. Çift bölmesi: seçim 252 gün + Z ısınması (60/120 gün) ile ilk işlem ≈2016 ortası. Düzeltme (YORUM): çift bölmesi 2016'dan itibaren koşar; 2018'den itibaren (ilk ileri yürüme yılı) sınama sonucu sayılır, 2016–2017 yalnız ısınma/eğitim.

**04-037** — ZAYIF SORU — Holding–iştirak bağı eşbütünleşmenin gerçek nedeni olabilir; bu yanlılık değil, çift fikrinin dayanağıdır. Bağ koparsa 04-042. K1 aynı çiftlerde olduğundan sonuç yanlı olmaz.

**04-038** — CEVAPLI — Seçim p'si ortak trendle şişse de değerlendirme ileri yıldadır (T §5.8) ve K2 aynı evrenin sepetini çıkarır (T §5.7, ortak enflasyon trendi iki tarafı da götürür). Rejim kırılma testi kaynakta yok; eklenmez.

**04-039** — EKSİK — S2-25 "çıkış yok" doğru (D: kopma → çıkış kuralı görünmüyor). Ama D'ye göre Tansu "rolling cointegration" mekanizmasını anıyor (tweet, NOT) ve raporda "p 0,048 CURRENT" var; kapı tanımı yalnız YORUM. Düzeltme: S2-25'e "Tansu rolling p izliyor, kapı parametresi yok; 'p>0,05 ise yeni giriş yok' ayrı varyant olarak 5.10 ızgarasına girer, varsayılan kapalı" ekle.

**04-040** — EKSİK — D: 53'teki yatay çizginin nedeni "bilinmiyor". Aday açıklamalar (YORUM): bacağın işlem durması/kapanması, nakde geçiş, hata. Tasarım yok sayıyor çünkü kaynak yok. Düzeltme: D'deki "belirsiz" listesine kalsın; K'ye "Tansu'da nakde dönüş/askı olabilir" notu. 04-043 ile bağlantılı.

**04-041** — ZAYIF SORU — K §4 sadakat tablosu −%21'i hedef olarak listelemiyor (yalnız Z ve geçiş). K §2 satırındaki "≈ −%21" D'ye göre "görsel tahmin, çift ve dönem yok". Yeniden üretilemez; sınanmaz.

**04-042** — EKSİK — Düzeltme: bölme MaxDD yanında her çift için yıl içi en kötü düşüş ve "rolling p>0,05 gün sayısı" raporlansın (çıkış değil, bilgi). 5.12'deki %25 düşüş kuralı zaten bölmede uygulanır.

**04-043** — EKSİK — T §5.3 yalnız tavan/taban kilidini kapsıyor. İş Yatırım kapanmış hisseleri veriyor (T §5.2). Düzeltme (YORUM): son işlem gününün kapanışında satılmış sayılır, pay nakit olur ve yıl sonuna kadar o çift pasif; birleşmede son fiyat; olay sayısı raporlanır.

**04-044** — EKSİK — Masraf (%0,3/yön, T §5.4) tüm geçişlere uygulanır; yıl başı rotasyonu da aynı. Düzeltme: M11 likidite sınırı yıl başı işlemlerine de uygulanır; yıl başı toplam işlem tutarı raporlanır.

**04-045** — EKSİK — S2-26 "işlem yapılmaz" der; pay yıl başında eşitlenmez. Düzeltme (YORUM): pay yalnız ilk dağıtımda ve yeni çifte geçerken eşit, sonra çift kendi sermayesiyle bileşik; "işlemsiz devam" ifadesi aynen kalır, "eşit pay" yalnız başlangıç payı anlamına gelir.

**04-046** — EKSİK — T §5.6 "eşit pay" ve "en fazla 5". Düzeltme (YORUM): pay hep 200.000 TL (n<5 ise fark nakitte); getiriyle bileşik (04-045). 04-032 ile aynı kural.

**04-047** — EKSİK — T §5.4 M11 genel yazıldı, çift bölmesi için açık değil. 200.000 TL pay, sınırı %2 ile ancak medyan TL işlem tutarı ≥10 milyon TL ise karşılar (hesap). Düzeltme (YORUM): M11 çift bölmesine uygulanır; aşılırsa tavan kadar geçilir, kalan nakitte; "sınır aşılan gün sayısı" raporlanır.

**04-048** — YANLIŞ — K §3 "Risk paketi: … SMA250 altı çıkış (bütün aileler)" ile K §3 aynı paragrafta "Çift rotasyonunun kendi çıkışı vardır" ve T §5.5 "Risk paketi bu bölmeye uygulanmaz" çelişiyor. T geçerli. Düzeltme: K'de "(bütün aileler)" → "(çift rotasyonu hariç)".

**04-049** — EKSİK — T §5.6 aileleri ayrı ölçer; m5 portföy kuralı "aileden bağımsız". Düzeltme (YORUM): ilk sürümde m5 her bölmenin sermaye eğrisine uygulanır. Tansu'nun −%27,44'ü sonuç referansı değil (kabul kararına girmez); tasarım onu "reddetmez", yalnız göstermez.

**04-050** — CEVAPLI — T §5.7: portföy seviyesinde günlük fazla getiri = bölme − K2 (aynı evrenin eşit ağırlıklı sepeti): ortak piyasa hareketi ve enflasyon çıkarılır.

**04-051** — EKSİK — T §5.7 K2'yi "aynı evren", ayrıca "aynı çiftlerin 50/50'si" diyor; hangisi kabul için kullanılır belirsiz (T §5.12.2 "K2"). Düzeltme: K2 = §5.2 evreni (önceden yazılsın); 50/50 yalnız tanısal.

**04-052** — EKSİK — T §5.7 yalnız "rastgele günlerde". Düzeltme (YORUM): her çift-yıl için gerçek geçiş sayısı n kadar rastgele gün seçilir; her geçişte mevcut hisseden diğerine geçilir (çift iki durumlu); ilk giriş hissesi yazı-tura, ilk giriş günü de rastgele. 04-055 ile uyumlu.

**04-053** — EKSİK — B5 çift için ön şartı söylemiyor. Düzeltme (YORUM): ön şart |Z|≥2 (ΔZ yönü rastgele) ana K1; ön şartsız ikinci K1 tanısal. Böylece "ΔZ onayı değer katıyor mu" ve "çift fikri değer katıyor mu" ayrılır. Aynı çift, aynı yıl.

**04-054** — EKSİK — B5 "hisse başına eşleştirilir"; çift için: çift-yıl başına eşleştir (geçiş sayısı çift-yıl hücresinde sabit). Toplamla eşleştirmek çiftler arası kaymayı gizler.

**04-055** — EKSİK — Eşleştirilmezse K1 farkı nakit/yatırımlı süreden de gelir. Düzeltme (YORUM): rastgele kuralda ilk geçiş günü gerçek ilk sinyal gününe eşitlenir (nakit süre aynı), sonrası rastgele.

**04-056** — OLGU — Doğruladım: 1.000 tekrarla en küçük p = 1/1001 ≈ 0,000999. Holm'da en küçük p'nin eşiği 0,05/m; m ≥ 50 olunca eşik ≤ 0,001 ve ulaşılamaz (hesap: 0,05/50 = 0,001). Deneme sayısı (T §5.11: bütün denemeler) 50'yi aşarsa kabul imkânsız. Düzeltme: tekrar sayısı R ≥ 20·m (ya da blok bootstrap güven aralığından parametrik p) kuralı yaz.

**04-057** — EKSİK — D: Tansu'nun "50/50 Buy&Hold" tanımı yok. Düzeltme (YORUM): yılın ilk işlem gününde bir kez 50/50 al, yıl sonuna kadar tut (al-tut); günlük dengeleme yok; yıl sınırında çift değişirse yeni çift için yeniden kurulur.

**04-058** — EKSİK — Fazla getiri riski normalize etmiyor. K1 aynı çift hisselerinde tek hissede kaldığı için risk profili benzer; 50/50 daha düşük oynaklık. Düzeltme: raporda bölme / K1 / 50/50 yıllık oynaklık ve beta yan yana; kabul kararı K1/K2'ye göre.

**04-059** — EKSİK — T §5.7'de 50/50 var, §5.12'de yok. Düzeltme: §5.12'ye "50/50 tanısaldır, kabul kararında rolü yoktur" yaz (YORUM; Tansu'nun kendi kıyası olduğu için rapora girer).

**04-060** — OLGU — Hesapladım (tesadüfi yıl işareti %50 varsayımıyla): 9 yılda ≥6 pozitif olasılığı 0,254; 10 yılda ≥6: 0,377. %60 ölçütü tek başına şansı ayıramaz. Düzeltme: bu ölçütü "gürültü kontrolü" olarak bırak, karar K1 Holm p'sinde; gerekçeyi T §5.12.4'e yaz.

**04-061** — EKSİK — Çift bölmesinde "işlem" bağımlı (aynı güne denk çiftler). Düzeltme: örneklem şartında bölme toplamı geçiş sayısı ve farklı sinyal günü sayısı ayrı yazılsın; çiftler arası aynı gün geçiş oranı raporlansın; asıl istatistik günlük fazla getiri serisidir (T §5.8 zaten bunu söylüyor).

**04-062** — EKSİK — Ortalama tutma süresi 60+ gün iken 20 günlük blok otokorelasyonu eksik yakalar (blok < bağımlılık). Düzeltme (YORUM): çift bölmesinde blok = ortalama tutma süresi ya da 20/60/120 duyarlılık; en geniş aralık raporlanır.

**04-063** — EKSİK — 6 ayda ~15 geçişle güç düşüktür; T §5.9 "en küçük saptanabilir etki" hesabı doğrulama için yazılı, canlı dönem için değil. Düzeltme: aynı hesap canlı seri için yapılsın; saptanabilir etki doğrulama etkisinin yarısından büyükse sonuç "belirsiz" sayılır, geçti/kaldı denmez.

**04-064** — EKSİK — T §5.3: sadakat kontrolünde Yahoo açılışıyla ayrıca üretilir (S2-7); bölme sonucunda iki dolum karşılaştırması yazılı değil. Çift geçişinde iki bacak aynı gün aynı biçimde etkilendiği için sapma kısmen iptal olur (YORUM). Düzeltme: bölme sonucu, ek duyarlılık olarak, "AOF yerine ertesi gün kapanışı" dolumuyla da koşulsun.

**04-065** — EKSİK — T §8'de yok. AOF'un gerçek dolum olup olmadığı kaynak yok. 200.000 TL emir BIST100 hisselerinde çoğunlukla AOF'a yakın dolar (genel bilgi, doğrulanmadı). Düzeltme: §8'e açık soru ekle; M11 %2 sınırı zaten emri küçük tutar.

**04-066** — OLGU — Takas T+2; satış bedeliyle aynı gün alım aracı kurum kuralına bağlı. Doğrulayamadım (kaynak yok). Düzeltme: §8'e "aynı gün satıştan alıma bedel kullanılabilir varsayımı" ekle; kullanıcı kurumuna göre değişir.

**04-067** — OLGU — 2.054,78 / 6 = 342,46 TL (hesap). 6 AL etiketi (grafikte sayıldı) = 1 ilk giriş + 5 rotasyon. Ortalama portföy ≈114 bin TL ise 342 TL ≈ %0,3 (geçiş başına), yani Tansu'nun maliyeti geçiş başına tek %0,3'e ya da yön başına ≈%0,15'e benzer (YORUM, varsayım ortalama değere dayalı, doğrulanamaz). T'nin %0,3/yön, geçiş = %0,6 daha kötümserdir. Maliyet formülü sadakat hedefi değil; T §5.4 senaryoları (%0,1/%0,3/%0,5) aralığı kapsıyor.

**04-068** — EKSİK — T §5.3 tek hisse için kilidi yazıyor, geçiş için değil. Düzeltme (YORUM): ikisinden biri kilitliyse geçiş yapılmaz, eski hissede kalınır; ertesi gün sinyal yeniden değerlendirilir ve yalnız o gün "Z≤−2 ve ΔZ>0" sağlıyorsa yapılır (eski sinyal taşınmaz). Engellenen geçiş sayısı raporlanır.

**04-069** — EKSİK — Düzeltme: sinyal günü kapanışı ile ertesi AOF arasındaki farkın dağılımı çift bacakları için raporlansın (veri var). Ölçülebilir fark çıkarsa kayma senaryosu (%0,5) kabul için zaten gerekir.

**04-070** — CEVAPLI — T §8.4: tedbirli hisse bedava veriyle ayırt edilemiyorsa "bilinen yanlılık" yazılır. Çift kuralı bu bilinmezliği taşır; ek kural gerekmez.

**04-071** — EKSİK — T §5.1 düzeltilmiş fiyat temettü ve bedelsizi içerir (yeniden yatırım varsayımı); nakit temettü ve stopaj ayrı modellenmez, vergi T §8.6'da doğrulanmadı. Düzeltme: T'ye "nakit temettü modellenmez, toplam getiri varsayılır; zamanlama etkisi ve stopaj %0,5 senaryosuyla karşılanır" yaz.

**04-072** — CEVAPLI — T §5.1: ham fiyat + olay tablosu tek düzeltme; sonuç HGDG'ye karşı kontrol edilir; fark günleri listelenir; açıklanamayan sıçrama karantina. Yahoo yalnız sadakat için (T §7.2); iki kaynak farkı 04-075.

**04-073** — CEVAPLI — T §5.4: kabul için %0,5 senaryosunda da geçmeli; Corwin–Schultz ilk sürüm kapsamı dışında (T §3). Ek: çift işlem sıklığı yüksek olduğundan %0,5 sonuçlarına özellikle bakılır (YORUM).

**04-074** — EKSİK — T §6 kart alanı "giriş bölgesi", çift için anlamlı değil. Düzeltme (YORUM): çift kartı "yarın X'i sat/Y'yi al; Z ve ΔZ değeri; model dolumu AOF'tur, gerçek fiyat gün sonunda belli olur" yazar; fiyat aralığı vermez (sistem emir vermez, T §1).

**04-075** — EKSİK — Düzeltme: sadakatte aynı Z'yi iki kaynakta (Yahoo, İş Yatırım) hesapla; Z farkını ve seçilen çiftlerin p farkını raporla. Fark büyükse sadakat sonucu İş Yatırım için geçerli sayılmaz.

**04-076** — CEVAPLI — T §2/P5: "Tansu'nun sistemi" diye sunulmaz, "Tansu'dan esinlenen bizim yorumumuz". D de "kod Tansu'nun kuralı değil, yaklaşık yeniden yapım olur" diyor. Etiket bu iki cümleden alınır.

**04-077** — CEVAPLI — T §5.8: 2015–2026 tamamı geliştirme verisi; yeni ayrılmış dönem kayıttan sonrası. K §4: sadakat getiriye bakmaz, Z rakamlarına bakar. Kalan sorun az bilgi (iki sayı): 04-004.

**04-078** — CEVAPLI — K §5 ve T §5.6: Tansu'nun çiftleri kabul kararına girmez, parametre Z rakamına göre seçilir (getiri değil). Seçilmişlik Z'yi etkilemez; yalnız getiri etkiler ve o kullanılmaz.

**04-079** — OLGU — Görselleri açıp baktım: rapor.webp terminal tablosu, grafik.webp etkileşimli grafik ekran görüntüsü (fare imleci kutusu "May 14, 2025" görünüyor); NotebookLM logosu görmedim. Yeniden çizilmediğine dair kesin kanıt yok. Tutarlılık kanıtı var: ΔZ = +0,296 ≈ +0,30; 6 etiket = 6 geçiş. Düzeltme: D'ye "VAKBN görselleri doğrudan ekran görüntüsü gibi, logo yok" notu; rakamlar yine de "ikinci kaynak yok" diye ihtiyatla kullanılır.

**04-080** — EKSİK — D: VAKBN/CIMSA ≈60, AGROT/GARAN ≈120–126 (YORUM). Grafiğe göre VAKBN stratejisi veri başlangıcından ≈6 ay sonra başlıyor, Z ≈3 ay sonra (grafik). Düzeltme: tek pencere seçilir (60/120 aday, çifte özel değil); iki aday da 5.10 ızgarasında; 5.11 sayaçta "sadakat adayı" etiketli 4 deneme yazılır.

**04-081** — EKSİK — Pair Quality formülü yok (D), sınanamaz. Düzeltme: tanısal sütun olarak rolling corr ve β CV'yi seçilen çiftlerde raporla; "GÜÇLÜ" etiketi kaynak yok.

**04-082** — EKSİK — D: corr alt kapısı olası, düşük güven. Düzeltme: p<0,05 çiftlerinin korelasyon dağılımını raporla; "corr ≥ 0,4" kapısı 5.10 ızgarasında varyant, varsayılan kapalı (kaynak yok).

**04-083** — YANLIŞ — T §5.6 üç çifti aynı rotasyon sürümü gibi listeliyor. D: VAKBN–GARAN ve CIMSA–OYAKC rotasyon (long-only), AGROT–GARAN long-short + nakit (iki bacaklı). Düzeltme: listede AGROT–GARAN'ı "iki bacaklı sürüm; rotasyon sürümü bizim yorumumuz" diye işaretle, sadakat hedeflerinde yalnız VAKBN–GARAN kullan.

**04-084** — YANLIŞ — K §3.1 "birinci el: giriş, onay, yön, zaman". D madde 4: "momentum dönüş onayı" YORUM. Birinci el olan yalnız rapordaki "Z dönüşü +0,30" alanı (ΔZ'nin tanımı); onay kuralı olarak kullanımı ve tek günün yeterliliği YORUM; tweet ayrıntı vermiyor. Düzeltme: K §3.1 "onay" sözünü "ΔZ tanımı birinci el; onay kuralı YORUM" yap.

**04-085** — OLGU — Grafikte 6 AL etiketi saydım: GARAN, VAKBN, GARAN, VAKBN, GARAN, VAKBN. İlk etiket nakitten girişi gösterir; yani 1 giriş + 5 hisseden hisseye geçiş. Rapordaki "Geçiş Sayısı 6" etiket sayısına eşit. Maliyet 04-067'deki gibi tek %0,3/geçiş ile uyumlu; yön başına sayılırsa değişir. Düzeltme: K §4'te "6 geçiş = giriş dahil 6 işlem günü" yaz.

**04-086** — CEVAPLI — K satırında H, kesin parçalar için (±2, ΔZ, yön, T+1, yalnız alış); eksik üç parça aynı satırda "YORUM" sütununda yazılı. D de çekirdek "yüksek", spread/pencere "düşük" diyor. Okuma karışıklığı için H yanına "çekirdek" yazılabilir (isteğe bağlı).

**04-087** — CEVAPLI — K §5 ve T §5.6: çiftler kuralla seçilir, Tansu'nun örneği kabul kararına girmez; T §5.8: 2015–2026 geliştirme verisi sayılır. Kalan yanlılık yalnız pencere/β türü adayları ve 2025–26 örtüşmesidir; 04-077.

**04-088** — CEVAPLI — K §3.1: sinyal yalnız |Z|≥2 ve ΔZ işaretinde; Z ±2 bandı içindeyken ΔZ kullanılmaz. ±0,5 çizgileri D'ye göre iki bacaklı sürümün çıkışına ait (D madde 7, 55 grafiği); rotasyonda rolü yok.

**04-089** — EKSİK — T §5.10 "ek: parametre kaydı" diyor, ek yok; geçme eşiği sayısal yok. Düzeltme (YORUM): çift için oynayanlar pencere (60/120), β türü (log oran / OLS), eşik (1,5/2/2,5), seçim p eşiği (0,01/0,05/0,10), top-N (3/5/8); geçme eşiği "hücrelerin ≥%60'ı pozitif" (T §5.12.4 ile uyumlu), sonuç görmeden yazılsın.

**04-090** — EKSİK — T §5.11 yalnız "her koşu"; sadakat adaylarının sayılıp sayılmadığı yazılı değil. Düzeltme: sadakat adayları deneme günlüğüne "sadakat" etiketiyle yazılır ama getiri p'si olmadığı için Holm sayacına girmez; kuralı dondurmak T §5.8'deki kural kaydı+hash ile yapılır, getiri koşusu bundan sonra.

**04-091** — CEVAPLI — T §5.6: sınamanın birimi bütün bölme; T §5.9: günlük portföy fazla getirisi serisi blok bootstrap ile yeniden örneklenir (çiftler arası aynı gün korelasyonu bu tek seride vardır). Blok uzunluğu sorunu 04-062.

**04-092** — ZAYIF SORU — Aynı borsa, aynı kapanış seansı; iki hissenin kapanışı eşzamanlıdır. Likidite farkı kapanış fiyatını etkileyebilir ama BIST100 evreninde küçüktür (YORUM). Ölçüm gerekmiyor.

**04-093** — EKSİK — T §5.3 kilitli gün kuralı var; geçiş engelleme oranı raporda yok. Düzeltme: "engellenen geçiş" ve "veri hacimsiz gün" sayıları rapora (04-068, 04-019).

**04-094** — EKSİK — T/K sessiz. Düzeltme (YORUM): çift için seçim penceresinde 252 işlem günü ve en çok 5 hacimsiz gün şartı; dışlanan çift sayısı raporlanır. Yeni halka arzlar dışlanır; bu bilinen yanlılık olarak yazılır.

**04-095** — CEVAPLI — T §5.1: göstergeler ve getiriler düzeltilmiş fiyattan (S2-13), düzeltme tek yerde, HGDG ile karşılaştırılır. 04-013'e göre çarpımsal düzeltme p'yi değiştirmez; yanlış katsayı karantinaya girer.

**04-096** — EKSİK — Tek büyük geçiş yılın işaretini belirleyebilir. T §5.12.4 "en iyi %5 işlem atılınca" çift işlemleri için az sayıda işlemle (yılda ~15) çok kaba. Düzeltme (YORUM): çift bölmesinde "en iyi çift atılınca" sonuç pozitif kalmalı.

**04-097** — EKSİK — K §4 tablosunda "6 geçiş" var; %72,27 ve rapordaki Beta 1,675, Corr 0,731, Beta CV 0,277, p 0,048, maliyet 2.054,78 yok. Düzeltme: bunları "ikincil doğrulama hedefi" yap: aday seçiminde kullanılır (getiri değil) ve tutmazsa hangi parça YORUM kalır yazılır (Beta → β penceresi, %72,27 → ısınma/nakit, p → test ve pencere).

**04-098** — EKSİK — Premis düzeltmesi: Z<−2 iken Y tutulur (VAKBN), X değil; kayıp Y bacağında. Rotasyonun doğal maliyeti (Z'nin −2'den −3,4'e inerken Y'de kalmak, MaxDD −%27,44) tasarımda ayrıca ölçülmüyor. Düzeltme: sinyal gününden sonraki 20 günde en kötü düşüşün ve "sinyalden sonra sapmanın derinleşme oranının" raporda tablosu.

**04-099** — ZAYIF SORU — T ve K bu rakamları referans yapmıyor: T §7.2 yalnız Z ve geçişi, "getiriye bakılmaz" der; K §2 satırında bilgi olarak duruyor, kabul ölçütü (T §5.12) bunları kullanmaz.

**04-100** — CEVAPLI — T §1/§2/P5: kabul ölçütü başarısızlığı "bizim yorumumuz işlemedi" demektir; "Tansu'nun kuralı çürütüldü" denmez. T §5.12 yalnız yorumun geçip geçmediğini ölçer. Düzeltme gerekmez; rapor etiketini 04-076'daki gibi yaz.

## Özet

Sayımlar (100 soru): CEVAPLI 18, EKSİK 62, YANLIŞ 5, OLGU 11, ZAYIF SORU 4.
(Sayım için yukarıdaki satırlar üzerinde grep yapıldı.)

En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği:

1. **04-048 (YANLIŞ)** — K §3 "Risk paketi (bütün aileler)" ile "çift rotasyonunun kendi çıkışı var" ve T §5.5 çelişiyor. Değişiklik: K'de "(çift rotasyonu hariç)".
2. **04-084 / 04-016 (YANLIŞ)** — "ΔZ onayı birinci el" ifadesi aşırı. Birinci el olan yalnız ΔZ tanımı (+0,296). Tek gün yeterliliği YORUM. Değişiklik: K §3.1 ve S2-28 yeniden yazılsın.
3. **04-083 (YANLIŞ)** — AGROT–GARAN iki bacaklı (long-short + nakit), VAKBN–GARAN ve CIMSA–OYAKC rotasyon. Değişiklik: T §5.6 listesinde işaretle, sadakat hedefi yalnız VAKBN–GARAN.
4. **04-004 / 04-097 / 04-003 (EKSİK/OLGU)** — Sadakat yalnız iki Z sayısına dayanıyor. Rapordaki Beta 1,675, Corr 0,731, Beta CV 0,277, p 0,048, piyasada kalma %72,27 ve Mart–Mayıs 2025'te "sinyal yok" koşulu da hedef olsun; rapor tarihi bilinmeyen sayılsın ve tarih ızgarasında çift eşleşme aransın; tolerans ±0,0005 (sıkı) / ±0,05 (gevşek).
5. **04-056 (OLGU)** — 1.000 tekrar ve Holm: m ≥ 50 olunca eşik 0,001'in altına iner, ulaşılamaz. Değişiklik: R ≥ 20·m kuralı ya da parametrik/bootstrap p.
6. **04-031 / 04-032 / 04-046 (EKSİK)** — Çakışma ve eksik çift: p sıralı açgözlü seçim, 5'e kadar devam; çift sayısı n<5 ise pay 200.000 TL sabit, fark nakitte faiz kazanır; yıl içinde pay bileşik, yıl başında eşitlenmez (04-045).
7. **04-010 / 04-011 (EKSİK)** — X/Y rolü ve β işareti yazılı değil. Değişiklik: rol sembol sırasına göre, p'ye bakmadan; β ≤ 0 çift elenir.
8. **04-052 / 04-053 / 04-054 / 04-055 (EKSİK)** — K1 çift tanımı: çift-yıl başına eşleşme, aynı geçiş sayısı, rastgele gün, ön şart |Z|≥2 (ana) + ön şartsız (tanısal), ilk giriş günü gerçeğe eşitlenir (nakit süre aynı).
9. **04-062 (EKSİK)** — 20 günlük blok, 60+ gün tutmayı yakalamaz. Değişiklik: çift bölmesinde blok = ortalama tutma süresi ya da 20/60/120 duyarlılık, en geniş aralık raporlanır.
10. **04-024 (EKSİK)** — T §5.6 "2015–2017 politika faizi, sonra TLREF" ama T §4 "TLREF yalnız 2018 sonrası": geçiş yılı boşluğu. Değişiklik: tek kesme tarihi ("TLREF'in ilk yayın günü"), veri işinde bulunsun.

Not: 04-017 (Mart–Mayıs 2025'te sinyal yok) ve 04-014 (Temmuz 2025'teki Z sıçraması ve sinyal etiketlerinin tam o sıçramada olması) görselden okundu; ikisi de sadakat adaylarını eleyen ek koşullardır.
