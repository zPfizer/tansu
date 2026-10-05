# Cevaplar 07: Risk, çıkış, dolum

Yöntem: TASARIM taslak 5, KURALLAR, GLOSSARY, `kurallar/E-risk-cikis-surec.md`, `sorgu-2.md` okundu. İş Yatırım `HisseTekil` ile 5 hisse (THYAO, GARAN, SMRTG, BALAT, AKFIS; 2015–2026) ve 1 hisse (SMRTG, 2024–2026) çekildi, EREGL ve ASELS ayrıca ATR ölçümü için çekildi. Toplam yaklaşık 14 istek, kod dosyaya kaydedilmedi. Etiket: YORUM = kaynak yok, önerilen düzeltme.

## A. Pozisyon büyüklüğü (%1 risk)

**07-001** — OLGU — Ölçüldü (ATR14 Wilder, 2015–2026): 2 ATR / fiyat medyanı GARAN %6,2, EREGL %6,0; günlerin %93 ve %97'sinde < %10. Yani %10 tavan çoğu işlemde bağlar (pozisyon ≈ %16 olurdu), gerçek risk ≈ %0,6. TASARIM bunu yazmıyor. Düzeltme: rapora "tavanın bağladığı işlem oranı" ve gerçekleşen risk dağılımı eklenir.

**07-002** — EKSİK — Evet: çoğu işlemde fiilen sabit %10 pozisyon sınanır; E-K1 "%1 risk" yalnız kısmen sınanır. K1 aynı boyutlandırmayı kullandığı için karşılaştırma adil kalır. Düzeltme: raporda "risk paketi çoğunlukla %10 sabit boyuttur" yazılır; tavansız varyant duyarlılık olarak koşulur.

**07-003** — EKSİK — TASARIM 5.6 yazmıyor; E-K1 tablosu "belirsiz, YORUM" der. Düzeltme (YORUM): risk = sinyal günü kapanışındaki özkaynağın (nakit + açık pozisyonların kapanış değeri) %1'i; başlangıç sermayesi varyantı duyarlılık.

**07-004** — EKSİK — Evet: sabit nominal 1M TL yıllara göre farklı bağlar. Kaynak yok. Düzeltme (YORUM): raporda yıl başına "%2 likidite sınırının bağladığı işlem oranı" yazılır; gerekirse sermaye yıla göre medyan TL hacmine ölçeklenir.

**07-005** — EKSİK — Yuvarlama hiçbir yerde yazılı değil; E-K1 "aşağı yuvarlama YORUM" der (70 lot × 14,30 = 1001 > %1). Düzeltme: lot aşağı yuvarlanır; 5.3 motor sınamalarına eklenir.

**07-006** — ZAYIF SORU — Lot = risk / (2 ATR) fiyata bağlı değil; stop mesafesi sinyal günü ATR'siyle sabit (5.3). Sapma yalnız %10 tavanda (tavan / AOF) ve yuvarlamada çıkar; bu 07-001 ve 07-005'in konusu.

**07-007** — EKSİK — Masraf paydada değil (5.4'te yok). Düşük oynaklıkta çift yön %0,6, 2 ATR (~%4–6) içinde %10–15 pay tutar. Düzeltme (YORUM): R masrafsız kalır, rapora "masraf / 2ATR" ortalaması yazılır.

**07-008** — EKSİK — Fiyat adımı hiçbir yerde yok. Düzeltme (YORUM): stop ve hedef tick'e yuvarlanır (stop aşağı); raporda tick / 2ATR oranının en kötü hissesi yazılır.

**07-009** — EKSİK — M12 ölçüyü belirtmez. Düzeltme: sıra ölçüsü = 5.4'teki 10 günlük medyan TL (tek tanım). K1'e aynı sıra uygulandığı (5.7) için büyük şirket eğilimi karşılaştırmada nötrleşir.

**07-010** — EKSİK — Toplam risk/sektör sınırı yok (E-K1 "belirsiz"). Not: tavan bağlayınca stop başına kayıp ≈ %0,6, 10 eşzamanlı stop ≈ %6, %10 değil; yine de %25 kuralı kümelenmeye karşı korumasız. Düzeltme: rapora "en çok eşzamanlı açık risk" ve sektör yoğunluğu; sınır eklenmez (Tansu söylemedi).

**07-011** — CEVAPLI — 5.3: stop ve hedef giriş fiyatından ve sinyal günü ATR'sinden hesaplanır, yani mesafe tam 2 ATR sabit. Boşluk etkisi stop dolumunda (07-024); "boşluklu stop" motor sınamasında var.

**07-012** — EKSİK — Kaynak: infografik yalnız %1, 100.000 $, ~70 hisse verir (E-K1). %10 tavan ve "kaldıraç yok" bizim kararımız; 5.6 bunu YORUM etiketsiz yazıyor. Düzeltme: 5.6'ya "YORUM, bizim" etiketi; kartta ve raporda "bizim sınırımız" yazılır; tavansız varyant koşulur.

**07-013** — ZAYIF SORU — Evrende 100.000 TL ÷ fiyat ≥ 1 lot hemen her zaman (fiyat > 100.000 TL yok). Yine de lot = 0 ise işlem yok, K1'de de aynı.

**07-014** — EKSİK — "Özkaynak" tanımı yazılı değil. Düzeltme: özkaynak = nakit (faiz dahil) + pozisyonların kapanış değeri (07-003). Sınama oranlarla (fazla getiri) okunduğundan ve K1 aynı kuralı kullandığından ölçekten bağımsızlık iddiası geçerli kalır.

**07-015** — EKSİK — Kart 1M TL için adet verir (6.4). Düzeltme: kartta sermaye girdisi olur; adet %10 ve %2 sınırlarıyla yeniden hesaplanır; kanıt satırı "1M TL ile ölçüldü" der.

## B. 2 ATR stop ve ATR(14)

**07-016** — EKSİK — 5.5 "14 (YORUM)" der, Wilder'ı yazmaz; E-K1 "14, Wilder YORUM". Düzeltme: 5.5'e "Wilder" eklenir; 5.10 ızgarasına ATR uzunluğu (10/14/20) ve yumuşatma (Wilder/SMA) konur.

**07-017** — EKSİK — 5.1 ve S2-13: göstergeler HGDG, "fiyat seviyesi" HG; stop belirsiz. Düzeltme: pozisyon boyunca giriş, ATR, stop ve Düşük aynı seriden (HGDG, tarihli anlık görüntü) alınır; ham seri yalnız limit ve TL hacmi içindir.

**07-018** — EKSİK — ATR ve stop aynı seride tutulursa ölçek farkı oluşmaz; 5.1'deki "seviye" cümlesi yalnız limit ve TL hacmini kapsar. Düzeltme: 5.1'e bu cümle eklenir.

**07-019** — EKSİK — Backtestte anlık görüntü HGDG örtük çözer; canlıda Adım ham fiyatı görür. Düzeltme: Adım'a bugünkü mum olay tablosu uygulanmış (düzeltilmiş) verilir; kart stopu olay gününde yeniden hesaplanır.

**07-020** — CEVAPLI — 5.3 "sinyal günü ATR'si"; ATR sinyal günü dahil (kapanış bilinir). Boşluk günü TR'yi şişirir, stop geniş, lot küçük olur; bu Wilder ATR'nin doğası.

**07-021** — ZAYIF SORU — Ölçüm: BIST100 çekirdeğinde Düşük=Yüksek günü THYAO 1/2945, GARAN 2/2945 (SMRTG 11/1129). Evrende önemsiz; sayı raporlanır.

**07-022** — CEVAPLI — G-115 infografiği BİRİNCİ EL, verbatim "giriş fiyatının 2 ATR değeri kadar altına stop" (E-K2). Ancak NotebookLM infografiği, Tansu'nun kendi aracı değil (KURALLAR §5). G-125 "STOP 184,54 / ATR 4,62" doğrulanmadı, YORUM.

**07-023** — OLGU — Doğrulanamadı: Min/Max alanlarının müzayede fiyatı içerip içermediği belgelenmemiş, gün içi veri yok. Yön: müzayede içeriyorsa fazladan stop = kötümser. Düzeltme: raporda bilinen yanlılık olarak yazılır.

**07-024** — YANLIŞ — 5.3/S2-8: Düşük ≤ stop ise "stop fiyatından". Açılış stopun altında, gün yükseği üstündeyse bu iyimser. E-K2 YORUM #3 "açılış veya daha kötüsü" der; TASARIM bundan zayıf. Düzeltme (YORUM): dolum = min(stop, AOF).

**07-025** — EKSİK — S2-8 gerekçe ve işlem sayısı farkı yazmıyor. Düzeltme: 07-024 kuralı (AOF < stop ise AOF) koşulunu kapatır; "AOF'tan dolan stop" sayısı raporlanır.

**07-026** — EKSİK — Sabit %0,3 boşluk kaymasını taşımaz. Düzeltme (YORUM): 07-024 kuralı kaymayı kısmen taşır; ayrıca stop çıkışlarında %0,6 masraf senaryosu duyarlılık olarak koşulur.

**07-027** — EKSİK — Kaynak yok: Tansu emir türünü söylemedi (E-K2 "piyasa YORUM"). Düzeltme: raporda "piyasa emri, stop fiyatı veya daha kötüsü" varsayımı yazılır; 07-024/026 farkı bunu ölçer.

**07-028** — EKSİK — Veride durdurma alanı yok. Ölçüm: HACIM=0 günleri var (BALAT 7 gün; THYAO, GARAN, SMRTG, AKFIS 0). Düzeltme: HACIM=0 gününde giriş ve stop yok; durdurma 8.4'te bilinen yanlılık olarak yazılır.

**07-029** — EKSİK — Sabit ATR YORUM (E-K2 #5; Tansu söylemedi). Hareketli ATR iz süren stopa yaklaşır (kapsam dışı). Düzeltme: 5.5'e "ATR giriş gününde dondurulur (YORUM)" yazılır; ızgaraya konmaz.

**07-030** — YANLIŞ — KURALLAR §3 satır 105 "SMA250 çıkışı (bütün aileler)" der; satır 106 ve TASARIM 5.5 çiftte risk paketini uygulamaz. Çelişki. Düzeltme: satır 105'e "(çift hariç)" yazılır. %25 kuralı (5.12) portföy düzeyindedir, stop yerine geçmez; G-118 genel ilkedir, kuralı Tansu çifte uygulamamıştır.

## C. AOF dolum modeli

**07-031** — EKSİK — Giriş günü kontrolü var (5.3), sıra yok. Giriş öncesi Düşük stopu fazladan tetikler (kötümser); giriş öncesi Yüksek hedefi tetikler (iyimser). Düzeltme (YORUM): giriş gününde yalnız stop kontrol edilir, hedef ertesi günden başlar.

**07-032** — EKSİK — Sıralama varsayımı yok. Düzeltme: 07-031 kuralı + rapora "giriş günü çıkış oranı".

**07-033** — OLGU — Doğrulanamadı: gün içi veri yok (kapsam dışı). Proxy: %2 katılım sınırı (5.4). Düzeltme: gerekçe "proxy" diye yazılır; duyarlılık: giriş = sinyal sonrası gün AOF yerine kapanış.

**07-034** — EKSİK — Ölçülmüyor. Düzeltme: rapora sinyal günlerinde (AOF[t+1] / Kapanış[t] − 1) ortalaması, rastgele günlerle yan yana (07-041 ile aynı kontrol).

**07-035** — EKSİK — 5.12 hangi modele baktığını yazmıyor. Düzeltme (YORUM): kabul yalnız AOF modeline bakar; Yahoo açılış koşusu bilgi amaçlıdır, işareti değişirse raporda "dolum modeline duyarlı" yazılır.

**07-036** — OLGU — Doğrulanamadı: İş Yatırım alan belgesi yok. Ölçüm: AOF 10.385 günde 15 kez (%0,14) [Min,Max] dışında (THYAO 3, GARAN 1, SMRTG 6, BALAT 3, AKFIS 2) → AOF, Min/Max'tan farklı işlem kümesini içerebilir. Düzeltme: AOF dışarıdaysa [Min,Max]'a kırp ve say.

**07-037** — OLGU — Kısmen yanlış varsayım: AOF her zaman [Min,Max] içinde değil (yukarıdaki 15 gün). HACIM=0 günü yalnız BALAT'ta (7); bu günlerdeki AOF değeri kontrol edilmedi. 5 hisse örneklemi, tüm evren doğrulanmadı. Düzeltme: veri kalite kontrolüne bu iki kural eklenir.

**07-038** — YANLIŞ — TASARIM 5.5 "ertesi açılışta" der; 5.3 ve KURALLAR satır 103 AOF der. Düzeltme: 5.5 "ertesi gün AOF'unda" olarak değiştirilir.

**07-039** — ZAYIF SORU — Kapanışta çıkış, kapanışı sinyal olarak kullanıp aynı fiyattan satmak = ileriye bakma. Ertesi AOF seçimi doğru.

**07-040** — CEVAPLI — 5.4: %0,1/%0,3/%0,5 senaryoları ve kabul için %0,5 şartı asimetriyi kabaca kapsar; yön ayrımı ölçülmez, gerek yok.

**07-041** — EKSİK — 5.7 K1'in aynı dolum ve masrafı kullandığını yazmıyor. Düzeltme: "rastgele işlemler aynı AOF dolumu ve masrafla" cümlesi eklenir; AOF−Kapanış farkı fazla getiriden böylece çıkar.

**07-042** — EKSİK — 5.3 yalnız stop dolumunu yazıyor, hedef dolumu yok. Düzeltme (YORUM): hedefte dolum = hedef fiyatı, koşul Yüksek ≥ hedef + 1 tick; boşlukta bonus yok.

**07-043** — EKSİK — Yazılı değil. Düzeltme (YORUM): giriş AOF ≥ D ise giriş yok ve sinyal sayıma girmez; K1'de de aynı.

**07-044** — EKSİK — 5.3 "stop önce" kuralı geçerli; AOF ≥ D kenarı 07-043 ile kapanır. Düzeltme: motor sınamasına eklenir.

**07-045** — EKSİK — Eşik yok. Düzeltme (YORUM): kabul, iyimser ve kötümser iki uçta da sağlanmalı.

**07-046** — ZAYIF SORU — AOF konumu sıra için güvenilir ipucu değildir; iki uç sınır verir ve ek parametre gerektirmez (5.3).

**07-047** — EKSİK — 5.4 parantezinde "açılışta kovalama" var; S2-7 AOF'u zaten açılıştan bağımsız sayar. Muhtemelen iki kez sayılıyor (kötümser). Düzeltme: 5.4 parantezinden "açılışta kovalama" çıkarılır ya da "AOF ulaşılabilirlik payı" yazılır.

**07-048** — OLGU — Doğrulanmadı, kaynak yok. Düzeltme: arife günleri Takvim modülüne yazılır; AOF/Min/Max günlük özet sayılır, seans saati değişikliği ayrıca modellenmez ve bilinen yanlılıkta anılır.

**07-049** — EKSİK — 8.4 açık. Ölçüm: Min=Max günü BALAT'ta 629/2944 (tek fiyat), BIST100 çekirdeğinde ≤ 2. Yön: stop gün içi çalışmadığı için kayıp iyimser çıkar. Düzeltme: Min=Max gününde giriş ve stop yok.

**07-050** — EKSİK — Dolum gününün gerçek hacmi kontrol edilmiyor. Düzeltme (YORUM): giriş günü pozisyon ≤ o günün TL hacminin %10'u şartı (sınamada ex-post kontrol); parametre 5.10 kaydına yazılır.

## D. Kilitli tavan/taban

**07-051** — OLGU — Doğrulandı: baz fiyat önceki KAPANIS'tır, AOF değil. SMRTG tavan günleri: 12.05.2026 Max 11,70 = 10,64×1,10 (önceki AOF×1,10 = 11,41 < Max); 04.12.2025 Max 10,2267 = 9,30×1,10 (AOF×1,10 = 9,82); 08.05.2026 Max 9,68 = 8,80×1,10 (AOF×1,10 = 9,50). 19 aday günün hepsinde Max ≤ KAPANIS×1,10 (± tick). Not: HGDG (düzeltilmiş) alanıyla ölçüldü, oran bozulmaz. Düzeltme: 5.1'e "tavan/taban = önceki ham KAPANIS × 1,10 / 0,90, tick'e yuvarlı" yazılır.

**07-052** — ZAYIF SORU — Baz kapanış olduğundan kapanıştan kapanışa hareket limiti aşamaz; +%0,5 payı yeter. Doğrulama kapsamı: 2024–2026 ±%10. ±%20 dönemi (2015–2020) ve 12.03.2020 geçişi doğrulanmadı.

**07-053** — EKSİK — Ölçüm: Min=Max günü BALAT'ta 629/2944; kilit değil, tek fiyat. Düzeltme: kilit = Min=Max **ve** Max = tavan(önceki KAPANIS) (taban simetrik); Min=Max tek başına kilit sayılmaz.

**07-054** — EKSİK — Yaklaşık kilit tanımı yok. Düzeltme (YORUM): giriş gününden önceki günün Kapanışı = tavan ise giriş yok (K1'de aynı).

**07-055** — EKSİK — 5.3 yalnız giriş ve taban kilidini yazar. Düzeltme (YORUM): kilitli tavanda çıkış serbest (alış kuyruğu vardır), hedef/AOF tavan fiyatından dolar.

**07-056** — EKSİK — "Ertesi güne kayar", ertesi de kilitliyse kayma sürer yazılı değil. Düzeltme: kilit bitene kadar kayar; dolum min(stop, AOF) (07-024); rapora −2R'den kötü işlem sayısı.

**07-057** — EKSİK — Kilit sonradan açılırsa stop fiyatı iyimser; 07-024'teki min(stop, AOF) bunu sınırlar.

**07-058** — ZAYIF SORU — Stop tabanın altındaysa Düşük ≥ taban > stop, yani o gün tetik zaten olmaz (Düşük ≤ stop şartı sağlanmaz); kırpma gerekmez.

**07-059** — EKSİK — Kodda temsil yazılı değil. Düzeltme: `limit(tarih)` tablosu; halka arz ilk günleri 60 günlük medyan şartıyla evren dışı kalır; Yıldız/Ana/Alt farkı doğrulanmadı, raporda anılır.

**07-060** — EKSİK — Olay günü ham önceki kapanışla kontrol bozulur. Düzeltme: olay gününde baz = ham önceki kapanış × düzeltme katsayısı (`SHHE_FIYAT_AYAR_OR`).

**07-061** — EKSİK — Simülatör kuralı yok. Düzeltme: kilitli pozisyon açık ve pozisyon sayısına dahil sayılır, son kapanış değeriyle yer tutar; nakit yalnız satış dolunca serbest kalır.

**07-062** — EKSİK — Kural yok. Düzeltme (YORUM): bir bacak kilitliyse geçiş ertelenir (değişmezi korur), ertesi gün ΔZ yeniden değerlendirilir.

## E. SMA250 çıkışı ve ailelere özgü çıkışlar

**07-063** — EKSİK — Giriş kuralları SMA250 şartı içermiyor (KURALLAR §3). Düzeltme (YORUM): sinyal günü Kapanış < SMA250 ise giriş yok; K1'de aynı.

**07-064** — EKSİK — 07-063 düzeltmesi açıl-kapat işlemini ortadan kaldırır; kalanlar sayıma ve masrafa girer.

**07-065** — EKSİK — E-K3 "250 gün yoksa sinyal yok (YORUM)"; TASARIM yazmıyor. Düzeltme: SMA250 yoksa giriş yok; dışlanan yeni halka arz sayısı raporlanır.

**07-066** — CEVAPLI — 4: anlık görüntü değişmez ve tarihlidir, her koşu hangisini kullandığını yazar; çıkış günleri o görüntüye göre sabittir.

**07-067** — CEVAPLI — 5.3: yeniden giriş yeni sinyal ister; aynı gün çıkış sinyali 07-063 düzeltmesiyle kapanır.

**07-068** — EKSİK — Çıkışı ilk gerçekleşen kural belirler. Paket Tansu'nun genel infografiğidir, aileye özel değildir (E-K1–K3). Düzeltme: rapora çıkış nedeni dağılımı (stop / SMA250 / hedef) eklenir.

**07-069** — EKSİK — Raporlanmıyor. K1'e de pozisyon sınırı uygulandığı için sistematik sapma değil. Düzeltme: tutma süresi dağılımı ve reddedilen sinyal oranı zorunlu rapor çıktısı olur.

**07-070** — EKSİK — Kaynak yok. G-02 "Stop (X)" XABCD harmonik sütunudur; AB=CD'de X yok. E-K15 "AB=CD aracında stop görselde yazılı değil". A seviyesi YORUM. Düzeltme: 5.5'te "(ikinci el)" yerine "YORUM" yazılır.

**07-071** — ZAYIF SORU — Sadakat kontrolü yalnız D değerlerini üretir, getiriye bakmaz (KURALLAR §4); G-03 sonuçları kabul kararına girmez, yan yana gösterilir.

**07-072** — EKSİK — 5.5/5.6 lot paydasını yazmıyor; stop A ise payda 2 ATR değil giriş − A olmalı, yoksa risk %1 olmaz. Ödül/risk hesaplanmıyor. Düzeltme: lot = %1 × özkaynak / (giriş − stop); rapora AB=CD işlemlerinin ödül/risk dağılımı (R/R filtresi eklenmez, E-K23 ikinci el).

**07-073** — EKSİK — Kaynak yok (T-abcd: "A'yı aşarsa bozulur", gün içi mi kapanış mı belirsiz). Düzeltme (YORUM): gün içi temas (Düşük ≤ A), dolum min(A, AOF).

**07-074** — EKSİK — Teyit penceresi sonrası giriş koşulu yok. Düzeltme (YORUM): giriş günü AOF ≥ D veya AOF ≤ A ise sinyal geçersiz (07-043 ile birleşik).

**07-075** — EKSİK — GLOSSARY/5.3/6.5 üç anlam taşıyor. Düzeltme (YORUM): STOP = 2 ATR veya A stopu; BOZULDU = SMA250 çıkışı; Tansu'nun "BOZULDU"su (A aşımı) bizde STOP.

**07-076** — EKSİK — 5.12 portföy kuralının sonucu yazılı değil. Düzeltme (YORUM): aşılırsa o aile Canlı olamaz; pozisyon kapatılmaz; canlıda uyarı satırı.

**07-077** — CEVAPLI — 5.4 masrafı her yönde uygular; 5.7 K1 çiftte "aynı sayıda geçiş" ister; kabul %0,5'te de geçmeli. Brüt/net işaret sorusu bu sınamayla ölçülür.

**07-078** — EKSİK — Adım imzası iki tür için aynı olamaz. Düzeltme (YORUM): Adım(pozisyon, bağlam) → pozisyon'; bağlam tek hissede mum + hazır göstergeler, çiftte iki mum + z + kilit durumları.

## F. Giriş günü, yeniden sinyal, portföy

**07-079** — EKSİK — Sıra yazılı değil. Düzeltme (YORUM): sinyal günü sonunda pozisyon kapanmışsa ya da kapanışı bildirilmişse (SMA250) yeni sinyal sayılır; çıkışı bekleyen pozisyon "açık" sayılır.

**07-080** — EKSİK — Rastgele atlama sayıyı düşürür. Düzeltme: rastgele kural, hisse başına kuralın gerçekleşen işlem sayısına ulaşana kadar çekilir.

**07-081** — EKSİK — K1 aynı atlamayı uygular (nötrleşir) ama sayı raporlanmıyor. Düzeltme: atlanan sinyal sayısı/oranı kural ve rastgele için yazılır.

**07-082** — EKSİK — Ayrım yapılamaz. Düzeltme: pozisyon sınırsız koşusu duyarlılık olarak yanına konur.

**07-083** — EKSİK — 07-031 düzeltmesi: giriş gününde yalnız stop kontrol edilir.

**07-084** — EKSİK — 5.3 "giriş yok" der; iptal mi ertelenir mi yazmaz. Düzeltme: iptal; sayısı raporlanır; K1'de tavan günü girişi aynı biçimde yasak.

**07-085** — EKSİK — Bilinçli olduğuna dair kaynak yok. Düzeltme: 5.3 listesine lot yuvarlama, %10 tavan, giriş günü stop, tekrar sinyal, SMA250 çıkışı, olay gününde açık pozisyon, ardışık kilit, karantinada açık pozisyon eklenir.

**07-086** — EKSİK — Raporda yok. Düzeltme: 5.9'a R dağılımı, −1R'den büyük kayıp oranı, planlanan/gerçekleşen kayıp farkı eklenir (E-Grup 3).

**07-087** — EKSİK — 5.11 deneme günlüğüdür, işlem günlüğü değil. Düzeltme: Motor işlem satırına MFE/MAE (günlük Yüksek/Düşük) alanı eklenir.

**07-088** — CEVAPLI — 5.5 son satırı ve E-K5: TP1 "%10" anlamı, TP2 ve %50 paydası belirsiz, güven "Düşük"; uygulanamayan parçaya sadakat uygulanamaz, kabul edilen ilk aileden sonra denenir.

## G. Adım, Motor, vectorbt

**07-089** — EKSİK — Adım akşam bir günlük mumla çalışır; STOP olay sonrası yazılır. Düzeltme: 6'ya yazılır: kart stopu kurumda verilecek emir seviyesidir, durum akşam teyididir.

**07-090** — EKSİK — Giriş fiyatı akşam bilinmez. Düzeltme: kart stopu "tahmini (kapanış − 2 ATR)" etiketli; Adım stopu giriş dolduktan sonra hesaplar, kartta formül yazılır.

**07-091** — OLGU — Doğrulanamadı (8.7 açık). S2-12: yeni bedelsizde HGDG geçmişi yeniden ölçeklenir (belgeli). Ek gözlem: THYAO HGDG serisinde ATR/fiyat ölçümü anormal çıktı (medyan 3,75), nedeni araştırılmadı. Düzeltme: durum yalnız 19:30 verisiyle üretilir, ertesi akşam yeniden hesaplanır, kart "geçici" etiketi taşır.

**07-092** — EKSİK — Girdi belirsiz. Düzeltme: Adım saf olur: (pozisyon, mum, bağlam); ATR, SMA250, önceki düşük, tavan/taban bağlamda gelir, Motor hesaplar.

**07-093** — EKSİK — Seed alanı 5.11 günlüğünde yok. Düzeltme: seed ve tekrar sayısı günlüğe yazılır; Adım döngüsü rastgele kuralla paylaşılır.

**07-094** — OLGU — Doğrulanamadı: S2-41 ⚠️ olarak yazılmış, deneme kaydı yok; vectorbt'in kurulu olup olmadığı da kontrol edilmedi. Düzeltme: gerekçe "denenmedi" diye düzeltilir ya da 1 saatlik test kaydedilir.

**07-095** — EKSİK — Elle hesaplanmış örnekten başka kanıt yok. Düzeltme: motora "kural = rastgele" kalibrasyon sınaması eklenir (p değerleri ≈ düzgün dağılmalı).

**07-096** — OLGU — Ölçülmedi, hesap: ~100 hisse × 2.900 gün × 1.000 tekrar × 3 aile ≈ 9×10⁸ adım; saf Python ~3 µs/adım varsayımıyla ≈ 45 dk (belirsiz), ızgara bunu çarpar. 200 tekrarda en küçük p = 1/201 ≈ 0,005, Holm için yetmez. Düzeltme: son koşu ≥ 1.000; Adım numba/vektörle hızlandırılır.

**07-097** — EKSİK — Ayrım yazılı değil. Düzeltme (YORUM): Adım saf dolum/çıkış; Motor gün döngüsü, limit, kilit, karantina, olay; Simülatör nakit, sıra, pozisyon sayısı, faiz.

**07-098** — EKSİK — 5.1 pozisyonu kapsamıyor. Baz kapanış olduğundan (07-051) limit aşımı çöküş değil veri hatasıdır. Düzeltme: açık pozisyon karantinaya girerse işlem "veri hatası" olarak ayrı listelenir, sayısı raporlanır; K1'de aynı pencere dışlanır.

**07-099** — EKSİK — S2-15: İş Yatırım'ın verdiği günler işlem günüdür; durdurma günleri veride yok. Düzeltme (YORUM): delist'te son veri gününün kapanışından kapat ve "delist" etiketle; durdurmada fiyat güncellenmez, stop kontrolü yok.

**07-100** — OLGU — Doğrulama yok: S2-7..10 ⚠️ karar. Açılış verisinin yokluğu doğrulandı (S2-7); AOF ulaşılabilirliği doğrulanamaz (gün içi veri yok). Yanlışsa tüm giriş ve çıkış dolumları yönlü sapar. Düzeltme: dolum duyarlılığı (AOF / ertesi kapanış / Yahoo açılış) koşulur; kabul işareti hepsinde aynı olmalı.

---

## Özet

### Hüküm sayıları
- CEVAPLI: 8
- EKSİK: 70
- YANLIŞ: 3
- OLGU: 11
- ZAYIF SORU: 8

### Doğrulanan olgular
1. Tavan baz fiyatı önceki KAPANIS'tır, AOF değildir (SMRTG, 19 aday günün hepsinde Max ≤ KAPANIS×1,10; en az 4 günde Max, önceki AOF×1,10'un üstünde).
2. 2 ATR / fiyat medyanı GARAN %6,2, EREGL %6,0; %93–97 günde < %10 → %10 tavan çoğu işlemde bağlar, gerçek risk ≈ %0,6.
3. AOF 10.385 günde 15 kez (%0,14) [Min,Max] dışında; HACIM=0 günü yalnız BALAT'ta (7).
4. Düşük=Yüksek günü kilit demek değildir: BALAT'ta 629/2944; THYAO 1, GARAN 2, SMRTG 11/1129.
5. Doğrulanamayanlar: ±%20 dönemi, müzayedenin Min/Max'a girip girmediği, vectorbt denemesi, HGDG yeniden yazım zamanı.

### En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği
1. **07-012/002/001** — %10 tavan kaynaksız ve çoğu işlemde bağlayıcı. Değişiklik: 5.6'da tavanı "YORUM, bizim" diye etiketle; rapora "tavan bağlayan işlem oranı" ve tavansız varyantı ekle.
2. **07-072** — Lot paydası stop A olduğunda yanlış. Değişiklik: lot = %1 × özkaynak / (giriş − stop); AB=CD işlemlerinin ödül/risk dağılımı rapora.
3. **07-024/025/057** — Boşluklu stop dolumu iyimser. Değişiklik: 5.3'te dolum = min(stop, AOF); AOF'tan dolan stop sayısı raporlanır.
4. **07-053/051/060** — Kilit tespiti. Değişiklik: 5.1'e "tavan = önceki ham KAPANIS × 1,10 (tick'e yuvarlı)"; kilit = Min=Max **ve** Max=tavan; olay gününde baz katsayıyla düzeltilir.
5. **07-005/003/014** — Lot yuvarlama ve özkaynak tanımı yok. Değişiklik: lot aşağı yuvarlanır; risk = özkaynağın %1'i; motor sınamalarına eklenir.
6. **07-031/083/032** — Giriş günü ileriye bakma. Değişiklik: giriş gününde yalnız stop kontrol edilir, hedef ertesi günden başlar; giriş günü çıkış oranı raporlanır.
7. **07-063/064** — Girişte SMA250 çıkışı zaten sağlanıyor olabilir. Değişiklik: sinyal günü Kapanış < SMA250 ise giriş yok (K1'de de).
8. **07-086/087/069/081** — Rapor eksikleri. Değişiklik: 5.9'a R dağılımı, planlanan/gerçek kayıp, MFE/MAE, tutma süresi, reddedilen/atlanan sinyal oranı.
9. **07-038 ve 07-030** — Belge çelişkileri. Değişiklik: 5.5 "ertesi açılışta" → "ertesi gün AOF'unda"; KURALLAR §3 satır 105'e "(çift hariç)".
10. **07-092/078/097/089/090** — Adım'ın sınırı belirsiz. Değişiklik: Adım saf fonksiyon (pozisyon, mum, bağlam); Motor/Simülatör görev ayrımı yazılır; kart stopu "tahmini" etiketli, gerçek stop kurum emridir.
