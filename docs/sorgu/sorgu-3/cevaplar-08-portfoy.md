# Cevaplar 08: Portföy, masraf

Kaynak sırası: Tansu notları ve görseller > docs/kurallar (E, D) ve KURALLAR.md > TASARIM.md (taslak 5) > sorgu-2, veri-kaynaklari > kod. "YORUM" = kaynak yok, önerilen düzeltme. Doğrulanan olgular başta işaretli.

Bu oturumda doğrulanan olgular:
- borsapy `TCMB().history("policy")`: 57 satır, 2015-01-21 → 2026-01-23, yalnız değişim günleri, son değer 37,0. 2015: 7,75 → 7,50; 2016-11-25: 8,00; 2018-09-14: 24,00; 2024-03-22: 50,00.
- İş Yatırım `HisseTekil`, THYAO, 24.09.2026: `HG_HACIM` = 7.722.325.844 = borsapy lot hacmi 26.198.900 × `HG_AOF` 294,758. Yani HACIM TL'dir ve AOF = TL hacim / lot.
- ATR(14, Wilder)/kapanış, 01.2024–09.2026, ham HG serisi: GARAN %3,46, EREGL %2,99, AKBNK %3,70, SISE %2,70, BIMAS %3,12 (medyan). Günlerin %96–100'ünde oran %5'in altında. (THYAO, KRDMD, ASELS ham seride bedelsiz sıçraması olduğu için dışarıda bırakıldı.)

## A. Boyutlandırma ve bölme mekaniği

**08-001** — EKSİK — Oran doğru: %10 tavan, ATR/fiyat < %5 iken bağlar (0,01/(2·ATR/P) > 0,10). Ölçüm: BIST büyük hisselerinde oran %2,7–3,7, yani tavan günlerin %96–100'ünde bağlar; gerçekleşen risk ≈ %0,5–0,7, "%1 risk" istisna olur. Tasarım bunu yazmıyor. Fix: raporda "tavanla sınırlanan işlem oranı" ve "gerçekleşen risk dağılımı" satırı; kabul etmek (pratikte sabit %10 pozisyon) ya da tavanı ızgaraya almak Levent kararı (YORUM).

**08-002** — CEVAPLI — 5.6 ayrı bir toplam-risk kuralı koymuyor; tek sınır "en fazla 10 pozisyon" (M12). Tansu'da da yok (E K1 "belirsiz"). Tavan bağlayıcı olduğundan fiili toplam açık risk ≈ %5–7. Fix: rapora "en yüksek eşzamanlı açık risk" satırı (YORUM).

**08-003** — EKSİK — 5.6 ve E K1 sermayeyi tanımlamıyor (E K1 tablosu: "verilmedi"). Tansu: "toplam sermayenizin %1'i". Fix (YORUM): sermaye = sinyal gününün kapanış özkaynağı (nakit + açık pozisyonların kapanış değeri).

**08-004** — EKSİK — Bileşik mi sabit mi yazılı değil. Tansu'nun G-03 sınaması tüm sermayeyi bileşik kullanıyor (D/E). Fix (YORUM): bileşik; adet, %10 tavan ve %2 likidite tavanı her gün güncel özkaynaktan; yıllık ölçütler oran olarak okunur, 1.000.000 TL yalnız başlangıç.

**08-005** — EKSİK — Premise yönü makul ama doğrulanmadı (2015 TL hacmi çekilemedi, zaman aşımı). Yıllar arası karşılaştırma için tasarımda önlem yok. Fix: raporda yıl bazlı "%2 tavanı bağlayan işlem oranı"; yüksek çıkan yıllar yorumda işaretlenir (YORUM).

**08-006** — EKSİK — 5.5 AB=CD stopunu A yapıyor, 5.6/5.5 başlığındaki formül "risk / 2 ATR" (E K1). İkisi bağlanmamış. Tutarlı tek formül: adet = %1·S / (giriş − stop). Fix (YORUM): payda = giriş − fiili stop; ATR ailelerinde 2 ATR, AB=CD'de giriş − A. A stopu −%12…−%25 olduğu için bu ailede %10 tavan çoğunlukla bağlamaz.

**08-007** — EKSİK — E K1: aşağı yuvarlama YORUM (1000/14,30 = 69,93; 70 lot = 1001 > %1). TASARIM'de yok. Fix: aşağı yuvarla; yuvarlama sonrası gerçek risk işlem günlüğünde kalsın (YORUM).

**08-008** — EKSİK — 6.4 kart adedi sinyal gününün kapanışına göre; motor AOF'a göre. %1 risk adedi fiyattan bağımsız, ama %10 tavan fiyata bağlı. Fix: kartta "kapanışa göre tahmini adet" yazılsın; motor ertesi gün AOF ile yeniden hesaplar; ikisi aynı Adım fonksiyonundan geçer (YORUM).

**08-009** — EKSİK — 5.3: stop giriş AOF'undan hesaplanır; sinyal akşamı AOF bilinmez. Evet, stop değişir. Fix: kartta "tahmini stop = kapanış − 2 ATR (kesin değil)"; gerçek stop ertesi gün AOF ile; backtest ve canlı aynı kuralı Adım içinde uygular (4. Adım satırı zaten bunu garanti eder).

**08-010** — EKSİK — 5.1: "fiyat seviyesi gerektiren her şey düzeltmesiz". Adet fiyat seviyesi gerektirir, ATR düzeltilmiş seriden gelirse ölçek karışır. Fix: ATR'yi sinyal gününde ham ölçeğe çevir: ATR_ham = ATR_HGDG × HG_kapanış/HGDG_kapanış (aynı gün); ya da stop ve adet hesabını tek ölçekte (HGDG) yap (YORUM).

**08-011** — EKSİK — Olay tablosu yalnız fiyat düzeltmesi için kullanılıyor (4, 5.1). Pozisyon nakit akışı tanımsız. Fix (YORUM): pozisyon HGDG (toplam getiri) ölçeğinde değerlenir; temettü HGDG'ye gömülü, brüt kalır (stopaj yok, açık soru 8.6); bedelli hak kullanımı için nakit çıkışı modellenmez, raporda "bedelli: hak satılmış/kullanılmamış sayıldı" diye yazılır.

**08-012** — EKSİK — 5.1 stop/tavan için ham seri der, 5.3 stopu girişten kurar; olay sonrası yeniden ölçek yazılı değil. Fix (YORUM): açık pozisyonun giriş, stop, hedef durumu HGDG ölçeğinde tutulur; ham seri yalnız tavan/taban/likidite içindir. Böylece olay günü sahte stop tetiklenmez.

**08-013** — EKSİK — 5.6 "kaldıraç yok" der, taşma davranışını yazmaz. Fix (YORUM): adet = min(risk adedi, %10 tavanı, %2 likidite, nakit / (fiyat·(1+masraf))). Nakit yetmezse küçült; nakit sermayenin %1'inin altındaysa atla.

**08-014** — EKSİK — Valör kaynakta yok. BIST pay valörü T+2 (bellekten, bu oturumda doğrulanmadı). Fix (YORUM): valör modellenmez; satış nakdi aynı gün kullanılabilir (aracı kurum gün içi bakiyesi) ve faiz kazanır. Raporun varsayımlar satırına yaz.

**08-015** — EKSİK — 5.3 sıra yazmıyor. K1'e "pozisyon sınırı ve sıra kuralı" uygulanıyor (5.7, S2-42), yani aynı sıra olur. Fix: motor aynı AOF gününde önce çıkışları, sonra girişleri işler; serbest slot ve nakit aynı gün kullanılır (YORUM).

**08-016** — EKSİK — 5.3 yalnız "açık pozisyondaki hissede yeni sinyal" sayıma girmez der; slot doluluk reddi yazılı değil. Fix: reddedilen sinyaller işlem sayısına girmez, ayrı sayaçta raporlanır; K1 eşleştirmesi açılan işlem sayısıyla yapılır (YORUM).

**08-017** — EKSİK — M12 "en likit" tanımsız. Fix: 5.4'teki değer (son 10 günün medyan TL tutarı) kullanılsın. Büyük hisse yanlılığı: K1 aynı sıra kuralını uyguladığı için (5.7) etki iki tarafta ortaktır ve fark içinde sönümlenir; yine de rapora "slot taşan gün sayısı" yaz.

**08-018** — EKSİK — Beklenen kapanmış işlem sayısı hesaplanabilir ama tasarımda yok; kaynak yok. Üst sınır sinyal sayısıdır (KURALLAR: 99 hissede 11 yılda ~520 sıkışma dönemi, Yahoo, kaba). Fix: motor sınamasından sonra rapora "kapanmış işlem sayısı, ortalama tutma süresi, slot doluluğu"; 5.9 şartı sağlanmazsa "yetersiz örneklem" yazılır (zaten 5.9'da var).

## B. Likidite, dolum ve piyasa mikro yapısı

**08-019** — EKSİK — Pencerelerin gerekçesi yazılı değil (S2-19 evren: 60 gün; M11 işlem: 10 gün). Fix: 10 günlük pencere sinyal günü dahil, giriş günü hariç (karar anında bilinen veri); iki pencere farklı amaçlıdır (evren seçimi aylık, pozisyon tavanı kısa vadeli) diye 5.4'e tek cümle.

**08-020** — OLGU — Doğrulandı: HACIM TL'dir. THYAO 24.09.2026: HG_HACIM 7.722.325.844 TL; borsapy lot hacmi 26.198.900 × AOF 294,758 = 7,7223 mlr. 5.1 "fiyat seviyesi gerektiren her şey ham" der, yani HG_HACIM kullanılır (HGDG_HACIM'in lot/TL tanımı kontrol edilmedi). S2-14 "AÇIK" artık kapanır; 5.1 cümlesi güncellenmeli.

**08-021** — EKSİK — Kısmi dolum yazılı değil. Fix (YORUM): adet %2 tavanıyla küçültülür; kalan miktar ertesi gün alınmaz (tek giriş günü); raporda "likidite tavanı bağlayan işlem oranı".

**08-022** — EKSİK — Hayır, küçültme riski fiilen düşürür (08-001 ile aynı mekanizma). Fix: K1 rastgele işlemleri aynı boyutlandırma fonksiyonundan geçsin; gerçekleşen risk günlüğe yazılsın (YORUM).

**08-023** — EKSİK — %2 tavanı yalnız girişte (5.4). Çıkışta tam pozisyonun AOF'ta satıldığı varsayılıyor. Giriş tavanı çıkışta da pozisyonu günlük medyanın ≤ %2'sinde tutar, kuruyan günde değil. Fix: rapora "çıkış günü pozisyon / gün hacmi > %10 olan işlem sayısı" (YORUM).

**08-024** — EKSİK — Tavan önceki günlerin medyanından (ileri bakmaz). Dolum AOF'u zaten ertesi günün gerçek verisi. Düşük hacimli günün dolum riski yansımıyor. Fix: rapora "adet / gerçek gün hacmi" dağılımı (karar kuralı değil, tanı) (YORUM).

**08-025** — EKSİK — %0,3'ün hangi katılım oranını varsaydığı yazılı değil (kaynak yok). %2 tavanı medyan günde ≤ %2 katılım demek. Fix: 5.4'e "katılım ≤ %2 (medyan günde), kayma bu oranı varsayar" cümlesi; gerçek katılım oranı dağılımı rapora (YORUM).

**08-026** — OLGU — Kısmen doğrulandı: AOF = HACIM(TL) / HACIM(lot) (THYAO 24.09.2026, 294,758). Yani AOF günün tüm hacmini içeren hacim-ağırlıklı ortalamadır. Kapanış seansı ve toptan/çapraz işlemlerin dahil olup olmadığı doğrulanmadı. Fix: veri deposu testi: her gün MIN ≤ AOF ≤ MAX; ihlal listelenir. Sınama sonuçlarının sınırı olarak 8. Açık sorulara yaz.

**08-027** — EKSİK — Ayıklanamaz (kaynak yok). Yanlılık yönü: şişkin medyan → %2 tavanı gevşek → iyimser. Fix: açık soru olarak ekle; sağlamlık ızgarasında tavan %1 ve %2 koşulsun (YORUM).

**08-028** — EKSİK — Evet iyimser olabilir. Ölçüm yolu: kapanış tavanda ve AOF tavana çok yakın olan günler sayılabilir. Fix (YORUM): giriş yok kuralı: HG_MAX ve kapanış tavan, AOF ≥ tavan − 1 fiyat adımı; rapora bu günlerin sayısı.

**08-029** — EKSİK — Kuyruktaki satıcı modellenmiyor (kaynak yok). Fix (YORUM): kilit kuralını taban için de "AOF ≤ taban + 1 adım ve kapanış tabanda" yap; o günlerde çıkış ertesi güne kayar (5.3'ün genişletilmesi).

**08-030** — EKSİK — 5.3 yalnız "ertesi güne kayar" der. Ardışık kilitte ilk işlem görülen günün AOF'u olur (kural gereği). Kayıp %1'i aşar. Fix: günlükte "planlanan risk / gerçekleşen kayıp" kolonu (E bölüm (b) Grup 3'te zaten kontrol maddesi); pozisyon slot ve eğride açık sayılır, 08-035'e bak.

**08-031** — EKSİK — Premise doğru: açılış verisi yok; kuralın iyimserliği var. Fix (YORUM): düşük ≤ stop ise dolum = min(stop, AOF). Mevcut kural (yüksek < stop ise AOF) bunun özel hali, yeni kural onu kapsar ve boşluklu toparlanan günü kötümser yönde yakalar.

**08-032** — EKSİK — 5.3 "giriş günü de kontrol edilir" der, sıra bilinmez. Fix (YORUM): kötümser: giriş günü düşük ≤ stop ise tetiklendi say, çıkış min(stop, AOF); oranı raporda yaz (M1 ile aynı mantık).

**08-033** — EKSİK — Dönem ±%20 (veri-kaynaklari 5). Boşluklu stop sıklığı hesaplanabilir ama raporda yok. 5.12.4 yıl bazında sonuç zaten ayrı yazılıyor. Fix: günlükte "gerçekleşen kayıp / planlanan risk" histogramı; 2015-11-30–2020-03-12 ve sonrası ayrı kolon (YORUM).

**08-034** — CEVAPLI — S2-15: İş Yatırım'ın verdiği günler işlem günüdür. Kapalı günler (Şubat 2023, bellekten 8–14 Şubat) veride yoktur; stop sonraki ilk günde boşluk olarak işlenir (08-031 kuralı). EBDKS gün içi durdurma günü yine veri üretir. Faiz tahakkuku için 08-069'a bak (takvim günü).

**08-035** — EKSİK — Tasarım yazmıyor. Fix (YORUM): kapanış fiyatıyla değerle (şeffaf); rapora "kilitli taban gün sayısı" ve "taban kilidi günlerini çıkarınca %25 kuralı" duyarlılık satırı.

**08-036** — EKSİK — 8.4 yalnız yanlılık diyor. Fix (YORUM): işlem sırası kapanan hissede son işlem günü AOF'unda zorunlu çıkış; veride yoksa son bilinen kapanış; raporda "kapanan hisse sayısı ve bu işlemlerin getirisi". Brüt takas/tek fiyat tedbiri için bedava veri yok (8.4).

**08-037** — EKSİK — Evren modülü giriş izni verir (4). Fix (YORUM): açık pozisyon evrenden düşünce korunur; çıkış kuralları evrenden bağımsız; Adım fonksiyonu İş Yatırım verisiyle sürer (veri deposunda hisse zaten var).

## C. Masraf varsayımları

**08-038** — EKSİK — Bileşenlerin payı yazılı değil (kaynak yok). "Açılışta kovalama" ifadesi AOF modeliyle uyumsuz: açılış kovalanmıyor. Çift sayım değil ama anlamsız madde. Fix: 5.4 cümlesinden "açılışta kovalama" çıkar; "komisyon, BSMV, kayma" kalsın; Levent kendi tarifesini yazarsa komisyon payı ayrılır (YORUM).

**08-039** — EKSİK — Aracı kurum tarifesi belgelenmedi (kaynak yok). Fix (YORUM): Levent'in tarifesi alınır; 1.000.000 TL ölçeğinde asgari komisyon bağlamıyorsa yüzde sabit kalır; kurum tarifesinin %0,1–%0,5 aralığında olduğu raporda doğrulanır.

**08-040** — YANLIŞ — S2-2 "sınama ölçekten bağımsız oranlarla okunur" der; 5.4 %2 likidite tavanı mutlak TL'ye bağlı (ör. 100.000 TL pozisyon için ≥ 5.000.000 TL medyan). İddia yalnız bu tavan ve asgari komisyon bağlamıyorsa doğrudur. Fix: S2-2 cümlesini "tavanlar bağlamadığı ölçekte" diye daralt; sağlamlık ızgarasına sermaye {250.000 / 1.000.000 / 4.000.000 TL} ekle (YORUM).

**08-041** — EKSİK — Kaynak yok. Düşük fiyatlı hissede fiyat adımı oranı büyüktür. Fix: rapora "fiyat < 10 TL" kırılımı ve işlem fiyatının adım oranı; evren BIST100 benzeri olduğundan etki küçük olmalı, ama ölçülmeli (YORUM).

**08-042** — EKSİK — Sabit %0,3 adverse seçilimi yansıtmaz. Fix: 08-031 kuralı (min(stop, AOF)) stop çıkışlarını zaten kötüleştirir; ek kayma için %0,5 senaryosuna güven (YORUM). Ayrı bileşen eklemek yeni parametre olur, ilk sürümde gerekmez.

**08-043** — EKSİK — Kaynak yok; tek sabit oranın 2015–2026 geçerliliği doğrulanmadı. Fix: 8. Açık sorulara "BSMV ve komisyon tarihçesi" ekle; %0,1/%0,3/%0,5 aralığı bunu kapsıyorsa raporda yaz (YORUM).

**08-044** — EKSİK — "Bir kısmını karşılar" cümlesinin hesabı yok. Fix: cümleyi değiştir: "temettü stopajı HGDG'de brüt kalır; oran doğrulanana kadar sonuçlar vergisizdir, masraf senaryosu bunu karşılamaz". Stopaj oranları bu oturumda doğrulanmadı.

**08-045** — EKSİK — Üçlünün dayanağı yok; Tansu'da da yok (E K1: komisyon/kayma "verilmedi", "sıfır başla, duyarlılık koş"). Fix: ek olarak "başa baş masrafı" (sonucun sıfıra indiği masraf oranı) raporlansın (YORUM).

**08-046** — ZAYIF SORU — Kâğıt üstü dönemde gerçek dolum yok; premise çelişkili. Ölçüm ancak Levent gerçek emir verirse olur: 08-099.

**08-047** — CEVAPLI — 5.12.3 kabul şartı ailenin kendi sonucunda uygulanır (aile başına devir hızı kendiliğinden yansır); K1 çift bölmesinde "aynı sayıda geçiş" (5.7), tek hissede "hisse başına eşleştirilen sayı" ile devir hızını eşler.

**08-048** — EKSİK — K1 ve K2 için masraf yazılı değil. Fix (YORUM): K1 ve portföy aynı masrafı öder; K2 sepeti her ay başı yeniden dengelemede (08-076) aynı masrafı öder. Böylece net-net karşılaştırma yapılır.

**08-049** — OLGU — Hesap: 2.054,78 / 6 = 342,46 TL geçiş başına. Ortalama özkaynak ~125.000 TL varsayımıyla ≈ %0,27 geçiş başına (≈ %0,14 yön başına) veya, ilk giriş tek yön sayılırsa 11 yön için ≈ 187 TL/yön (%0,15). Tansu'nun formülü yok; bizim %0,3/yön yaklaşık iki kat. Doğrulama sınırlı (özkaynak yolu bilinmiyor). Fix: KURALLAR 4 tablosuna "maliyet/geçiş" satırı ekle; formül çıkarılamazsa YORUM kalır.

**08-050** — CEVAPLI — 5.4 "her yönde %0,3": geçiş satış + alış, yani %0,6. Fix: GLOSSARY'ye "geçiş maliyeti = iki yön" yaz.

## D. Çift bölmesi

**08-051** — YANLIŞ — 5.6 "her an çiftin bir hissesindedir" ile KURALLAR §3 / D bölümü "ilk sinyale kadar nakit" (VAKBN'da piyasada kalma %72,27) çelişiyor. Fix: 5.6 cümlesi: "her çift payı ilk sinyale kadar nakit (faiz kazanır), sonra hep çiftin bir hissesinde; yıllık seçimde düşen çiftin payı kapanır, nakit olur, yeni çiftin ilk sinyaline kadar nakit kalır."

**08-052** — EKSİK — Yazılı değil. Fix (YORUM): boş paylar nakitte kalır (kalanlara dağıtılmaz); K2 de aynı sayıda çiftle kurulur, bu paylar iki tarafta nakit.

**08-053** — EKSİK — K2 boş küme. Fix (YORUM): o yıl her iki taraf nakit, günlük fazla getiri 0; yıl "işlem yok" diye işaretlenir ve 5.12.4 paydasından çıkarılır.

**08-054** — EKSİK — Fix (YORUM): yıllık seçim yılın ilk işlem günü kapanışında; çıkış ve girişler ertesi AOF'ta, aynı masraf ve taban kilidi kuralıyla (5.3). Her çift için %2 likidite tavanı ayrı uygulanır, pay tavanı aşarsa 08-055.

**08-055** — EKSİK — Pay 200.000 TL için ≥ 10.000.000 TL medyan tutar gerekir. Fix (YORUM): çift seçiminin ön koşulu olarak her iki bacak da 252 gün medyan TL tutarıyla %2 tavanı karşılasın; bu ön yazılı, ileriye bakmaz, "her an bir hissede" bozulmaz.

**08-056** — EKSİK — Fix (YORUM): yıl başı eşit pay, yıl içinde dengeleme yok (her çift kendi payını bileşik büyütür). K2 de yıl başı 50/50, yıl içinde sabit adet.

**08-057** — CEVAPLI — 5.6: sınama birimi bütün çift bölmesidir; Tansu'nun çiftleri "ayrıca gösterilir, kabul kararına girmez". %25 kuralı (5.12 sonu) bölmenin sermaye eğrisine uygulanır; Tansu'nun tek çiftindeki −%27,44 kabul kararında ölçüt değildir.

**08-058** — EKSİK — 5.8 çift bölmesinde işlem sayısı yerine günlük fazla getiri serisi diyor, 5.7 işlem seviyesi çift için tanımsız. Fix (YORUM): çift için "işlem" = geçişten geçişe tutuş dönemi; 5.9'daki "100 işlem" şartı çift bölmesinde günlük seriye dönüşür (5.8 zaten bunu öngörüyor).

**08-059** — EKSİK — Varyans farkı ayrıştırılmıyor. Fix (YORUM): raporda bölme ve K2 oynaklık, MaxDD yan yana; ek olarak bölme günlük getirisinin K2'ye regresyonu (alfa). K2 başlangıcı yıl başıdır (bölmenin ilk sinyaline hizalanmaz): nakit dönem gerçek farktır.

**08-060** — EKSİK — Fix (YORUM): Tansu çiftleri kendi sermayesiyle (100.000 TL, tek çift) ve yüzde olarak gösterilir; masrafsız ve %0,3'lü iki satır. Bölmedeki 200.000 TL pay bu gösterime karışmaz.

**08-061** — EKSİK — Aritmetik doğru: 6 ay ≈ 125 işlem günü / 20 ≈ 6 blok. Aralık hiç anlamlı olmaz. 5.9 "saptanabilecek en küçük etki" bunu raporlar ama 5.12.6 nokta tahminiyle karar verir. Fix (YORUM): çift bölmesinde canlı dönem en az 252 işlem günü, ya da 6 ay sonucu "bilgi" olarak yazılır, ölçüt olarak 252 gün sonra uygulanır.

**08-062** — EKSİK — Fix: sadakat koşusu faizsiz yapılır (Tansu sonucunda faiz yok); getiri koşusu faizli. Raporda iki satır: faizsiz ve faizli; fark = nakit payı × faiz (YORUM).

## E. Nakit faizi

**08-063** — YANLIŞ — TASARIM 4 "TLREF yalnız 2018 sonrası", 5.6 "2015–2017 politika faizi, sonrası TLREF"; veri-kaynaklari: TLREF hesabı 2018-12-28'de başladı. 2018'in tamamı için seri yok. Doğrulandı: borsapy politika faizi serisi 2015-01-21'den bugüne kapsıyor. Fix: tek seri, tüm dönem borsapy politika faizi (1 hafta repo); TLREF ve EVDS ilk sürümden çıkar; 4 ve 5.6'yı tek cümleye indir.

**08-064** — OLGU — Doğrulanamadı (EVDS anahtarı yok). TLREF'in 2018-12-28 → 2019-06-17 arası geriye dönük değerleri nereden gelir: kaynak yok. 08-063 düzeltmesiyle bu soru ilk sürümde gereksiz kalır.

**08-065** — OLGU — Doğrulandı: son satır 2026-01-23 = 37,0. Seri yalnız değişim günlerini tutar (57 satır), ileri doldurma tasarım gereğidir. Sayfa canlı okunduğundan sonraki toplantılarda değişiklik yoksa seri güncel olabilir; bunu doğrulayan kaynak yok. (Satır tarihleri karar gününden bir gün sonra görünüyor, ör. 2023-06-23; bellekten.) Fix: rapor başlığına "son faiz satırı tarihi + kullanılan basamak"; TCMB sayfasıyla bir kez elle karşılaştır.

**08-066** — OLGU — Kısmen doğrulandı. Seri değerleri 1 hafta repo ile uyuşuyor (2015-02: 7,50; 2016-11: 8,00; 2018-09: 24,00; 2024-03: 50,00; bellekten). 2015-02 → 2016-11 arası düz kalması üst bandı dışlar (bellekten: üst bant bu sürede değişti). 2018-06-01 satırı (16,50) bellekten 1 hafta repo değil, likidite penceresi oranı gibi; doğrulanmadı. Fix: 8. Açık sorulara "lending = 1 hafta repo mu" ekle.

**08-067** — EKSİK — Kaynak yok. Bellekten: 2016–2018'de TCMB fonlamayı politika faizinin üstünden yaptı, yani politika faizi gerçek fonlama maliyetinin altında kalır; sınaması yok. Fix: faiz duyarlılığı (08-068) bunu kapsar.

**08-068** — EKSİK — Tasarım brüt politika faizini vergisiz, spreadsiz, anında kazanılır sayıyor; bireysel için iyimser. Fix (YORUM): 5.12.2 hem faizli hem faizsiz eğride sınansın (faiz çarpanı 0 / 1); 8. Açık sorulara "nakdin gerçek getirisi" ekle.

**08-069** — EKSİK — Yazılı değil. Fix (YORUM): faiz her takvim günü tahakkuk eder (hafta sonu ve tatil dahil), yıllık oran /365, basit, işlem günü bazında günlük bileşik; TCMB repo oranı basit yıllık oranla ifade edilir.

**08-070** — EKSİK — Fix (YORUM): faiz günlük kapanış nakit bakiyesi üzerinden işler; sinyal kapanışı ile AOF girişi arasındaki ve valördeki nakit nakit sayılır, faiz kazanır (08-014 ile tutarlı).

**08-071** — EKSİK — 8. Açık sorular faiz serisini listelemiyor (veri-kaynaklari 8.6 listeliyor). Fix: 8'e "faiz serisi: lending sütunu 1 hafta repo mu, güncel mi" ekle.

**08-072** — EKSİK — K3 tanımsız; 5.12'de ölçüt yok. Fix: K3 cümlesini sil ya da "bilgi satırı: yıllık portföy getirisi − aynı dönem nakit faiz getirisi, kabul ölçütüne girmez" yap (YORUM).

**08-073** — EKSİK — "Hiç işlem yapma" portföyü raporlanmıyor. Fix: rapora bu satır eklenir (bilgi). Ölçüt olarak eklemek (portföy ≥ faiz) Levent kararıdır; ben eklemedim (YORUM).

**08-074** — EKSİK — Faiz serisi artık borsapy'den geliyor (08-063), EVDS anahtarı engel değil. Fix: faiz serisi yoksa koşu durur, sessiz sıfır yok; rapor başlığında "nakit faiz: kaynak, son tarih" yazılsın.

## F. Fazla getiri tanımları

**08-075** — EKSİK — K2 tam yatırımlı. 5.12.2 portföyü K2 ile kıyaslıyor: nakit tutmak yükselen piyasada ceza olur. Fix (YORUM): raporda "ortalama yatırımlı oran" ve "maruziyet-düzeltmeli K2" (ağırlık = yatırımlı oran, kalanı faiz) ek satır olarak.

**08-076** — EKSİK — Sıklık yazılı değil. Fix (YORUM): K2 = evrenin ay başı (evren yenilemesiyle aynı) eşit ağırlıklı al-tut sepeti, ay içinde sabit adet; günlük dengeleme yok.

**08-077** — EKSİK — Fix (YORUM): hem işlem hem sepet AOF'tan AOF'a (girişle aynı gün), her ikisi net (aynı masraf).

**08-078** — EKSİK — 5.9 güven aralığı günlük portföy fazla getirisi üzerinde; yani birincil seviye portföydür. Fix: 5.7'ye "kabul ölçütleri portföy seviyesinde; işlem seviyesi tanı" cümlesi (YORUM).

**08-079** — EKSİK — 4'te "boştaki nakit faiz kazanır" ve K1 aynı simülatörden geçer (5.7: sınır ve sıra aynı). Açıkça yazılmamış. Fix: "K1 aynı simülatörde: aynı faiz, masraf, boyutlandırma" cümlesi.

**08-080** — CEVAPLI — 5.7/S2-42: pozisyon sınırı ve sıra kuralı K1'e de uygulanır; fark girişlerin kalitesinden gelen tutma süresi farkını da içerir, ayrıştırılması istenmez. Fix: rapora iki grup için ortalama tutma süresi ve slot doluluğu (YORUM).

**08-081** — EKSİK — Fix (YORUM): K1 portföy seviyesinde aynı boyutlandırma fonksiyonuyla koşar; boyutta ek eşleştirme yok; rapora iki grup için ortalama maruziyet.

**08-082** — CEVAPLI — 5.8: ileri yürüme 2015–2017 ile başlar, sınanan yıllar sonrası; SMA250 ısınması 2016'da biter. Isınma günleri sınanan yıllara girmez.

**08-083** — EKSİK — S2-43: parametre sabit, ileri yürüme "yıl yıl sonuç gösterir". Fix: tek sürekli koşu; sermaye ve pozisyon yıldan yıla taşınır; yıllar eğrinin kesitidir; %25 kuralı sürekli eğriye bakar (YORUM).

**08-084** — EKSİK — Test yılları 2018–2026, yaklaşık 9 yıl (%60 → 6 yıl). Tanım yalnız çift için var (S2-46: günlük fazla getirinin yıllık toplamı). Fix: tek hisse için de "yıl içi portföy getirisi − K2 getirisi" yıl kesiti; yalnız işarete bakılır (YORUM).

## G. Enflasyon ve düşüş kuralı

**08-085** — CEVAPLI — 5.7: ölçütler K1/K2'ye göre fazla getiri; enflasyon her iki tarafta ortak etken, farkta düşer. Mutlak getiriler zaten "üst sınır, karar için kullanılmaz" (5.2). Fix: raporda mutlak getiriye "nominal TL" etiketi.

**08-086** — EKSİK — Rejimden bağımsızlık sağlanmıyor. Fix: yıl tablosu zaten yıl bazında (5.8); ek olarak 2021–2023 (negatif reel faiz) kesiti ayrı satır olarak yazılsın (YORUM). TÜFE verisi kaynak olarak kayıtlı değil.

**08-087** — EKSİK — 5.12 sonu "en büyük düşüş" der, nominal mi yazmaz. Tansu'nun MaxDD'si (K19) nominal özkaynak eğrisi. Fix: "nominal TL özkaynak eğrisi" yaz; reel eğri bilgi olarak, TÜFE kaynağı bulununca (YORUM).

**08-088** — EKSİK — Fix (YORUM): ilk sürümde kural her ailenin kendi eğrisine uygulanır; birleşik portföy kurulunca (5.6) ayrıca birleşik eğriye uygulanır.

**08-089** — EKSİK — 5.12 portföy kuralının sonucunu yazmıyor. Fix: ihlal → aile "Canlı" olmaz (ret). Boyut küçültme yeni deneme sayılır (5.8, Holm) (YORUM).

**08-090** — EKSİK — Fix (YORUM): kural %0,5 masraflı ve faizli eğri üzerinde sağlanmalı (5.12.3); faizsiz eğri ek bilgi.

**08-091** — CEVAPLI — Fazla getiri K1/K2'ye göre aynı dönemde hesaplanır (5.7), kur rejimi ortak etken; nominal TL farkı bu yüzden anlamlıdır. Dolar bazı bilerek kesildi (3).

**08-092** — EKSİK — Birim yok. Fix (YORUM): etki = günlük portföy fazla getirisinin ortalaması (K2'ye göre), yıllıklandırılmış; çift ve tek hisse bölmesi aynı birim.

## H. Tansu'ya sadakat, parametre kaydı ve uygulama

**08-093** — EKSİK — 7. sıra 2 sadakat yalnız rakam yeniden üretir ("getiriye bakılmaz"); SMRTG/ISKPL getirisi yeniden üretilmez. Fix: raporda "Tansu paketinden farklar" tablosu (sermaye bileşik/10 slot/%10/masraf/stop A/AOF); isteğe bağlı Tansu sürümü koşusu masrafsız, tek hisse, tüm sermaye (YORUM).

**08-094** — EKSİK — KURALLAR §0: "her YORUM deneme sayısına girer"; yani Holm'e girer. 5.10 ızgara hangi parametreleri oynattığını yazmıyor. Fix: ızgaraya pozisyon sınırı {5,10,20}, tavan {%5,%10,%20}, likidite {%1,%2,%5} ekle (YORUM).

**08-095** — EKSİK — 5.5 başlığı "Tansu'nun risk paketi" der; KURALLAR §0 bunun NotebookLM infografiği olduğunu belirtir. P5 ile adlandırma gerilimi var. Fix: başlığı "Tansu'nun paylaştığı (NotebookLM) risk paketi" yap; ekranda "Tansu'nun sistemi" denmesin.

**08-096** — YANLIŞ — 5.5 "ertesi açılışta", 5.3 "ertesi AOF"; KURALLAR §3 sonunda "ertesi açılış sınamada ertesi günün AOF'u" der. Tek davranış: AOF. Fix: 5.5'te "ertesi açılışta" → "ertesi AOF'ta (5.3)".

**08-097** — CEVAPLI — 5.6: birleşik portföy aileler kabul edildikten sonra kurulur; çifte pozisyon ve toplam risk o aşamada sınanır. Ek: birleşik aşamada %25 kuralı birleşik eğriye uygulanır (08-088).

**08-098** — EKSİK — Kart yalnız "%1 risk" adedini gösterirse yanıltır. Fix: kartta "adet = min(risk, %10, %2 likidite)" ve "likidite üst sınırı: X TL" satırı; Levent farklı sermayeyle yüzdeyi kendi sermayesine çarpar, likidite sınırı mutlak TL kalır (YORUM).

**08-099** — EKSİK — Canlıda AOF emri verilemez (haklısın). Fix: kâğıt dönemde dolum = ertesi gün AOF (hesaplanan); gerçek-model farkı yalnız Levent gerçek emir verip dolum fiyatını kayda geçirirse ölçülür; günlükte "gerçek dolum" kolonu (isteğe bağlı) (YORUM).

**08-100** — EKSİK — Böyle bir sınama yok (5.1 yalnız fiyat düzeltme katsayısını HGDG ile karşılaştırıyor). Fix: birim sınama: aynı işlem için ham fiyat + olay çarpanıyla hesaplanan getiri ≈ HGDG getirisi; olaysız hissede eşit, temettü varsa fark = temettü; eşik ±%0,5 (5.1'deki eşik) (YORUM).

## Özet

Hüküm sayıları (toplam 100):
- CEVAPLI: 10 (002, 034, 047, 050, 057, 080, 082, 085, 091, 097)
- EKSİK: 79
- YANLIŞ: 4 (040, 051, 063, 096)
- OLGU: 6 (020, 026, 049, 064, 065, 066)
- ZAYIF SORU: 1 (046)

En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği:
1. 08-001: %10 tavan günlerin %96–100'ünde bağlar; fiili risk ≈ %0,5–0,7. 5.6'ya "tavanla sınırlanan işlem oranı ve gerçekleşen risk" raporu; Levent tavanı (ya da sabit %10 pozisyon kabulünü) bilerek seçsin.
2. 08-063: Faiz kaynağı çelişkisi (4 ve 5.6; TLREF 2018-12-28'den başlar). Tek seri: borsapy politika faizi, 2015'ten bugüne; TLREF/EVDS çıkar.
3. 08-006: AB=CD'de payda belirsiz. Adet = %1·S / (giriş − fiili stop); ATR ailelerinde 2 ATR, AB=CD'de giriş − A.
4. 08-031 (ve 08-032, 08-042): Stop dolumu iyimser. Kural: düşük ≤ stop ise dolum = min(stop, AOF); giriş günü stopu kötümser say.
5. 08-003 / 08-004: Sermaye tanımı yok. 5.6'ya "sermaye = güncel kapanış özkaynağı, bileşik" yaz; tavanlar buna göre.
6. 08-010 / 08-012: Ham ve düzeltilmiş seri karışıyor. Pozisyon durumunu (giriş, stop, hedef, adet) HGDG ölçeğinde tut; ham seri yalnız tavan, taban ve likidite için.
7. 08-051: "Her an bir hissede" ile "ilk sinyale kadar nakit" çelişir. 5.6 cümlesi: ilk sinyale kadar nakit, sonra hep bir hissede; yıllık seçimde yeni çift ilk sinyale kadar nakit.
8. 08-075: K2 tam yatırımlı, portföy kısmen nakit. Rapora ortalama yatırımlı oran ve maruziyet-düzeltmeli K2 ekle; 5.12.2 yorumu buna göre.
9. 08-068 / 08-069: Nakit faizi brüt, vergisiz, tahakkuk kuralsız. 5.12.2 hem faizli hem faizsiz eğride sınansın; tahakkuk: takvim günü, /365, basit.
10. 08-040: "Sınama ölçekten bağımsız" iddiası %2 likidite tavanıyla çelişir. S2-2 cümlesini daralt; 5.10 ızgarasına sermaye {250.000 / 1.000.000 / 4.000.000 TL} ekle.

Ek not: 08-020 doğrulandı, HACIM TL. 5.1 ve S2-14'teki "AÇIK" ifadesi güncellenmeli (küçük düzeltme).
