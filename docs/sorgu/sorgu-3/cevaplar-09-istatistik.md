# Cevaplar 09: İstatistik ve kabul

Not: OLGU işaretli hesaplar elle ya da `.venv` ile `python -` (dosyasız) simülasyonla yapıldı. Simülasyon varsayımı: işlem başına SD %8, 9 test yılı, işlemler bağımsız, masraf getiriden zaten düşülmüş. Gerçek veriyle doğrulanmadı.

**09-001** — EKSİK — K1 ön şartı hiçbir yerde yazılı değil (5.7 yalnız "ör. trend ailesi"). Düzeltme: KURALLAR §3'te her aile için "K1 ön şartı" satırı: AB=CD = geçerli A,B,C pivotları var; EMA = sıkışma bitmiş ve 10 günlük giriş penceresi içinde; çift = z-skor hesaplanabilir çift. Satır kural kaydına (hash) girer.

**09-002** — EKSİK — Evet, serbestlik derecesidir ve 5.11 bunu saymıyor. Düzeltme: ön şart tanımı hash kapsamında; değişirse yeni deneme.

**09-003** — EKSİK — Aynı gün seçimi piyasa şokunu null'a da taşır; bu (a) türünün amacıdır. Eksik olan: sayı "hisse başına" değil "gün başına" korunmalı. Düzeltme: (a) türünde her günün sinyal sayısı korunur, hisseler o günün ön şartlı havuzundan çekilir.

**09-004** — ZAYIF SORU — Null dağılımı, rastgele kuralın tüm istatistiğinin tekrarlarından kurulur; örtüşen pencere null'ın varyansını doğru yansıtır, p'yi kendiliğinden şişirmez. Tek şart: rastgele gün 5.3 gereği açık pozisyonla çakışmasın (zaten yazılı).

**09-005** — EKSİK — İki p'nin kullanımı yazılı değil. Düzeltme: aile p'si = max(p_a, p_b) (ikisi de geçmeli); bu kesişim testidir, ek düzeltme gerekmez; Holm'a tek p girer.

**09-006** — EKSİK — Evet, cümle yalnız (b) için doğru. Düzeltme: (a) için "gün başına", (b) için "hisse başına" sayı eşleştirmesi yazılsın.

**09-007** — EKSİK — Havuz sinyal sayısına yakınsa null varyansı daralır ve gerçek örneklem null ile neredeyse aynı olur; p yüksek kalır, test güçsüzdür. Düzeltme: raporda "havuz / sinyal" oranı yazılır; oran < 10 ise sonuç "ölçülemedi" (bkz. 09-044).

**09-008** — OLGU — Doğrulandı (elle): en küçük p = 1/1001 = 0,000999. Holm eşiği α/m: m = 51'de 0,00098 < 0,000999; yani m ≥ 51 ve B = 1.000 ise hiçbir aile geçemez. 5.7 "en az 1.000" der, üst sınır koymaz. Düzeltme: B ≥ 20·m/α... en azından B ≥ 2·m/α (m=100 için ≥ 4.000); B, m ile birlikte artırılır.

**09-009** — EKSİK — Yazılı değil. Düzeltme: 200 tekrarlı p günlüğe "geliştirme" etiketiyle yazılır ve deneme olarak m'ye sayılır; ama Holm testi yalnız B ≥ 1.000 p'si ile yapılır.

**09-010** — CEVAPLI — 5.7: sıra kuralı rastgele kurala da uygulanır; iki taraf aynı filtreden geçtiği için fark simetriktir. Kalan etki yalnız boş yerin aşıldığı günlerde ve küçüktür.

**09-011** — CEVAPLI — 5.3 son madde ve 5.7: "açık pozisyonda gelen sinyal sayıma girmez, rastgele karşılaştırmada da aynı". Eşleştirilen sayı kabul edilmiş işlem sayısıdır; rastgele taraf aynı kabul filtresinden geçer.

**09-012** — EKSİK — 5.5 rastgele işlemin çıkışını söylemiyor. Düzeltme: rastgele işlem, kuralın tam çıkış paketini (2 ATR stop, SMA250 çıkışı, aileye özgü hedef) giriş fiyatından uygular; böylece tutma süresi dağılımı kuraldan gelir.

**09-013** — EKSİK — Bağlı 09-001: AB=CD ön şartı "geçerli A,B,C pivotu var" olursa rastgele işlem aynı kalıbın (A, B, C, D hedef) kendi pivotlarını kullanır. Pivotsuz günde stop/hedef üretilemez; o gün havuzda olmaz.

**09-014** — EKSİK — Geçiş sayısı z-skorundan çıkar, getiriden değil; yani sonuca koşullu değildir. Düzeltme: her çift ve yıl için geçiş sayısı ve başlangıç tarafı sabit, geçiş günleri düzgün rastgele; taraf dönüşümlü olduğu için yön ayrıca çekilmez.

**09-015** — EKSİK — Çift seçimi null'a dahil değil; K1 yalnız zamanlamayı ölçer, seçimin değerini ölçmez. Rastgele geçişte de ortalamaya dönüş görülür, bu null'ı yükseltir (kural lehine değil, aleyhine; muhafazakâr). Düzeltme: tasarıma "K1 çiftte yalnız z-skor zamanlamasını ölçer" yazılır; seçim değeri K2 (evren sepeti) ile okunur.

**09-016** — EKSİK — Düzeltme: K1 istatistiği = işlem başına ortalama fazla getiri (portföyde günlük ortalama fazla getiri); medyan yalnız bilgi.

**09-017** — EKSİK — Hipotez tek yönlüdür (kural > null), çünkü yalnız pozitif sonuç kabul edilir. Düzeltme: "tek yönlü p, Holm sonrası < 0,05" yazılsın.

**09-018** — EKSİK — Düzeltme: rastgele işlemin tutma süresi kendi çıkış paketinden gelir (09-012); işlem fazla getirisi o süredeki sepetle ölçülür.

**09-019** — EKSİK — Günlük dengeleme gerçek bir sıçrama primi üretir (bid-ask bounce). Düzeltme: K2 ay başı kurulur ve aylık dengelenir (evren zaten aylık).

**09-020** — EKSİK — Yazılı değil; sıfır masraflı sepet kuralı kayırır. Düzeltme: K2 sepeti aynı %0,3 masrafı ay başı evren değişimi ve dengelemede öder.

**09-021** — YANLIŞ — 5.7: "günlük portföy getirisi − günlük karşılaştırma getirisi". %30 maruziyetli kural %100 maruziyetli sepetle kıyaslanınca yükselen piyasada sistematik negatif çıkar. Düzeltme: karşılaştırma maruziyet eşleşmeli: sepet ağırlığı = kuralın o günkü maruziyeti, kalan nakit aynı faizi kazanır.

**09-022** — YANLIŞ — Aynı kök: kural boştaki nakitte faiz kazanır, %100 yatırımlı sepet kazanmaz; yüksek faizde fark mekanik pozitif olur. Düzeltme: 09-021'deki maruziyet eşleşmeli sepet; nakit faizi iki tarafta aynıdır ve farktan düşer.

**09-023** — CEVAPLI — 5.2 ve 5.7: yalnız aynı evren içindeki göreli karşılaştırma yorumlanır. Kural da aynı evrenden seçer; evrenin PD/eşit ağırlık primi iki tarafta bulunur. Kalan boyut farkı K1 ile zaten ayrı okunur.

**09-024** — CEVAPLI — 5.7: çift bölmesinde iki K2 var. Evren sepeti seçim + zamanlamayı, 50/50 tutma yalnız zamanlamayı ayırır. "Seçilmiş bağı taşıması" bilinçli ve amaçlanan tasarımdır.

**09-025** — EKSİK — Parametreler sabit olduğu için bu yıl yıl bölmedir; tek eğitilen şey çiftin yıllık seçimidir. "İleri yürüme" adı bu yüzden yanıltıcı olabilir. Düzeltme: adı "yıllık bölme (parametre sabit)" yap; kâğıt dönemin yerine geçmediğini yaz.

**09-026** — OLGU — 2018–2026 = 9 test yılı; %60 için 6/9 gerekir (5/9 = %55,6 yetmez). Null'da P(≥6/9) = 130/512 = %25,4 (elle; simülasyon %25,6). Yani ölçüt gürültüyü yalnız dörtte üç oranında eler; tek başına zayıf ayırt edicidir. 2015–2017 test edilmiyor (pencere başlangıcı).

**09-027** — EKSİK — Yazılı değil. Düzeltme: tamamlanmamış yıl paydadan çıkarılır, ayrıca gösterilir. (S2-46: çift bölmesinde ölçüt yıllık toplamla uygulanır; kısmi yıl için kural yok.)

**09-028** — EKSİK — SMA250 ve 252 günlük pencere ilk geçerli sinyali/çift seçimini 2015 sonu–2016 başına iter; çelişki yok ama yazılı değil. Düzeltme: raporda "ilk geçerli sinyal tarihi" yazılır; ilk test yılı tam yıl olmalı.

**09-029** — OLGU — Bağımsız değil. Simülasyon (108 işlem, 9 yıl): kriter 4 (≥6/9 yıl pozitif) kriter 1'e (Holm ≈ α 0,01) neredeyse bağımlı; ortak geçme olasılığı ≈ kriter 1'inkine eşit (δ=%2'de 0,606 vs 0,602). Bağımsızlık varsayımı ile çarpma yanlış olur; tasarım hesaplamadı. Düzeltme: boru hattı güç simülasyonu (bkz. 09-066).

**09-030** — OLGU — Null'da P(≥6/9 yıl pozitif) = %25,4 (elle 130/512; simülasyonla doğrulandı). Tasarım hesaplamadı. Yılda birkaç işlemde bile bu oran sabit; ölçüt tek başına bilgi taşımaz, kriter 1 ile birlikte okunur.

**09-031** — EKSİK — Evet, 2020 karışımdır. Düzeltme: rejim kırılma günleri (13.03.2020, 17.07.2017) yıl tablosunda not düşülür; sonuç kararı değiştirmez ama etiketlenir.

**09-032** — EKSİK — Yazılı değil. 5.8 gereği 2015–2026 zaten bütünüyle geliştirme verisi; ızgara tüm dönemde koşulursa yeni bir kirlenme yok. Düzeltme: "ızgara 2015–2026 bütününde" yazılsın.

**09-033** — CEVAPLI — 5.8: 2023 sonrası yandı; 2015–2026 bütünüyle geliştirme verisi. 2025–2026 Tansu örnekleri bu kapsamdadır. Sadakat kontrolünün getiriye bakmaması tasarımcının bilgisini silmez; bilinen sızıntı olarak 09-081'e bakın.

**09-034** — EKSİK — Ayrım yok. Düzeltme: 2025–2026 yıl tablosunda "Tansu örnek dönemiyle çakışır" diye işaretlenir; kriterlerde ağırlık aynı kalır.

**09-035** — YANLIŞ — Sabit 20 gün gerekçesiz; çift bölmesinde tutma süresi 66 gündür, blok bağımlılıktan kısa kalır ve aralığı dar (iyimser) yapar. Düzeltme: blok uzunluğu veriden seçilir (Politis–White) ya da ≥ ortalama tutma süresi; aile bazında yazılır.

**09-036** — EKSİK — Yazılı değil. Düzeltme: durağan bootstrap (Politis–Romano), ortalama blok uzunluğu 09-035'teki gibi; sınırdaki bağımlılık kaybı blok uzadıkça azalır.

**09-037** — EKSİK — 5.12'nin hiçbir ölçütü aralığa bağlı değil; aralık yalnız bilgi. Düzeltme: "karar K1 p'sinden; bootstrap aralığı yalnız rapor" yazılsın. Çelişirse p geçerli.

**09-038** — EKSİK — Yazılı değil. Düzeltme: %95 yüzdelik aralık, yalnız raporlanır; kriterde alt sınır aranmaz (aksi halde kriter 1 ikileşir).

**09-039** — EKSİK — Nakit günlerinde fark sıfır olunca seri aşırı sıfırlı ve kuyruklu olur; 09-021'deki maruziyet eşleşmeli sepetle sıfırlar kalkar. Düzeltme: aralığın kapsama oranı null altında simülasyonla bir kez kontrol edilir.

**09-040** — ZAYIF SORU — Ortalama için bootstrap sıkı durağanlık gerektirmez; ağır kuyruk ve değişken varyans bloklarda korunur. Yıl bazlı sonuç (kriter 4) zaten rejim tutarlılığına bakar. Ayrı bir durağanlık testi bilgi katmaz.

**09-041** — EKSİK — "±" tanımsız. Düzeltme: 6. bölüm örnek metni "işlem başına, %95 yüzdelik aralığın yarı genişliği, blok bootstrap" olarak yazılsın; işlem düzeyi ile 5.9'daki günlük portföy serisi tutarsız, birini seçin.

**09-042** — EKSİK — Karar ortalamaya bağlı olmalı (K1 istatistiği, 09-016). Ters işaret: raporda "kuyruğa bağlı" uyarısı; kriter 4 (en iyi %5 atılınca pozitif) zaten korur.

**09-043** — OLGU — Hesaplandı: n=100, SD=%8 → SE = %0,8. %1,6 = 2 SE (tek yönlü α=0,05'te güç ≈ %64). %80 güç için MDE = 2,49 × 0,8 = %2,0; Holm sonrası α≈0,01 ile %2,5. Bunlar %0,6'lık masrafın üstünde (masraf zaten işlem getirisinden düşüldüğü için bu, net fazla getirinin en az %2–2,5 olması demektir). Eşiklerin güç hesabından çıktığı belgede yazılı değil.

**09-044** — EKSİK — Düzeltme: üç sonuç: Canlı / Reddedildi / Ölçülemedi. MDE, iddia edilen etkiden (ya da masraf marjından) büyükse sonuç "ölçülemedi"; "reddedildi" değil.

**09-045** — ZAYIF SORU — "Post-hoc güç" gözlenen etkiyi kullanır; MDE yalnız SE'yi (gözlenen dağılım) kullanır ve aralık genişliğiyle eşdeğerdir. Bilgilendirici sayılır.

**09-046** — EKSİK — Aynı gün işlemleri bağımlıdır. Düzeltme: MDE ve SE gün-kümelenmiş hesaplanır (bağımsız birim = sinyal günü).

**09-047** — EKSİK — Çift bölmesi için eşdeğer yok. Düzeltme (tasarım kararı gerekir): çift bölmesinde en az 100 geçiş ve 60 farklı geçiş günü; ya da günlük seride en az 9 tam yıl.

**09-048** — OLGU — 6 geçiş/1,5 yıl ≈ 4/yıl/çift; 5 çift × 9 yıl ≈ 180 geçiş (üst sınır; aynı sektör ortak faktörü yüzünden bağımsız sayı daha az; veriyle doğrulanmadı). Birim bölme ise etkin N yaklaşık 9 yıllık tek seridir. Düzeltme: güç ve MDE günlük bölme serisinden hesaplanır.

**09-049** — CEVAPLI — 5.6: sınamanın birimi bütün çift bölmesi, tek tek çiftler değil; 5 çift tek birleşik seride, ortak faktörle birlikte ölçülür. Çift sayısı güç hesabında bağımsız örnek sayılmamalıdır.

**09-050** — EKSİK — 520 dönem ≈ yılda 47 (kaba, Yahoo); pozisyon sınırı ve evren filtresi sonrası 100'e ulaşma doğrulanmadı. Düzeltme: ulaşamazsa sonuç "ölçülemedi" (09-044).

**09-051** — EKSİK — Yazılı değil. Düzeltme: kabul anındaki m ile karar donar; rapor güncel m'yi ayrıca gösterir; "Canlı" statüsü yalnız yeni verideki (kâğıt dönem) bozulmayla geri alınır.

**09-052** — EKSİK — Çelişki doğru: 5.11 altı alan, S2-45 "(aile, varyant, parametre)" der. Düzeltme: m birimi = (aile, varyant, parametre); anlık görüntü ve hash kayıt alanıdır, aynı fikrin yeniden koşusu m'yi artırmaz. Bağlayıcı olan TASARIM'dır; 5.11 buna göre düzeltilsin.

**09-053** — EKSİK — Düzeltme: kural, parametre, ön şart ya da çıkış değişirse yeni deneme. Yalnız hata düzeltmesi (başarısız motor testiyle gerekçelendirilmiş, sinyal listesi değişmeyen) aynı deneme sayılır; karar Levent'te, günlüğe "düzeltme" nedeniyle yazılır.

**09-054** — EKSİK — Düzeltme: getiriye bakılan her koşu günlüğe girer (200 tekrarlılar dahil); sentetik motor sınamaları ve getiriye bakmayan sadakat kontrolü girmez.

**09-055** — EKSİK — Düzeltme: aday seçimi getiriye bakmadan (Tansu rakamıyla) yapıldıysa m'ye girmez; getiriye bakılarak yapıldıysa her aday girer.

**09-056** — EKSİK — Izgara p üretmiyor, yalnız oran raporluyor. Düzeltme: ızgara hücreleri Holm m'ye girmez; ızgara bir sağlamlık kontrolüdür.

**09-057** — EKSİK — Düzeltme: masraf senaryoları tek denemenin varyasyonu; kriter 3 AND olduğu için (kesişim) ek düzeltme gerekmez; Holm'a %0,3'teki p girer.

**09-058** — EKSİK — Garanti yok. Düzeltme: motor, getiri çıktısını günlüğe satır yazmadan üretmez; günlük ekleme-yalnız (her satır öncekinin hash'ini taşır), git'e işlenir. Elle koşu kural dışıdır.

**09-059** — EKSİK — Evet, sınırsız varyant eşiği ulaşılamaz yapar; bu cezalandırma doğru ama sonuç kilitlenir. Düzeltme: aile başına varyant bütçesi (öneri: 3); aşılırsa aile "kapatıldı".

**09-060** — EKSİK — Ölçülmüyor. Düzeltme: boru hattı rastgele/sentetik null veriyle uçtan uca 200 kez koşulur; yanlış kabul oranı ≤ %5 raporlanır. Kriter 1 tek başına ≈ %1 per aile (simülasyon, Holm ≈ 0,01) verir; kalan kriterler bunu düşürür, ama K1 null'ının geçerliliği ayrıca doğrulanmalı.

**09-061** — EKSİK — Ek yok. Düzeltme: Ek B "parametre kaydı": parametre adı, değer aralığı, hücre sayısı, düzgün örnekleme, tohum; hash'e dahil.

**09-062** — EKSİK — Eşik yok. Düzeltme: sağlamlık = pozitif hücre oranı ≥ %70 (öneri, Levent onaylar); null altında %50 olduğu için eşik > %50 olmalı.

**09-063** — EKSİK — Hücreler bağımlı; oran tanımlayıcıdır, çıkarımsal değil. Düzeltme: "bağımsız hücre varsayılmaz, p üretilmez" yazılsın.

**09-064** — EKSİK — Düzeltme: "pozitif" = K1'e göre ortalama fazla getiri > 0, %0,3 masrafla; p aranmaz.

**09-065** — OLGU — Kriterler bağımsız değil; 0,8^6 ≈ %26 yanıltır. Simülasyonda ortak güç ≈ kriter 1 gücü: 108 işlem, δ=%1 → %15, δ=%2 → %60; 225 işlem δ=%2 → %92. Tasarım hesaplamadı; kabul edilebilirliği kararla yazılmalı.

**09-066** — EKSİK — Pozitif kontrol yok. Düzeltme: rastgele kuralın getirisine bilinen δ enjekte edilir (ör. %1, %2), boru hattı koşulur, geçme olasılığı raporlanır (yukarıdaki sayılar referanstır).

**09-067** — OLGU — 30 işlem, SD %8: SE = %1,46. Doğrulama etkisi δ bilinen varsayılırsa, "yarısı" şartı: δ=%2'de geçme ≈ %75, δ=%1'de ≈ %63 (Z hesabı). Gerçek doğrulama etkisi de gürültülü olduğundan geçme düşer; ölçüt gerçek etkide bile %25–37 reddeder.

**09-068** — EKSİK — "Yarısı" için kaynak yok; keyfi görünüyor. Düzeltme: gerekçelendir (kazananın laneti için büzülme), ya da doğrulama etkisinin alt güven sınırıyla karşılaştır.

**09-069** — EKSİK — Ölçü ortalama olmalı. 5 işlem ayırt edici değil; tavan serileri bağımlı. Düzeltme: ek olarak en çok katkı veren 3 sembol atılınca ortalama pozitif.

**09-070** — EKSİK — Tek başına nokta işareti ≈ %50 geçer, yalnız form şartıdır; ama kriter 2, K2'ye (piyasa/maruziyet) karşı kontrol olarak kriter 1'in yakalayamadığını yakalar. Düzeltme: yazılsın ("form şartı") ya da alt sınırı sıfırın üstünde olsun.

**09-071** — EKSİK — Dönem, masraf ve kapsam yazılı değil. Düzeltme: 2015–2026 doğrulama dönemi, %0,3 masraf, kuralın bölmesi için ölçülür. VAKBN–GARAN yalnız sadakat/gösterim (5.6: kabul kararına girmez), tek çifttir (5 çiftli bölme değil); bu yüzden baştan ihlal sayılmaz.

**09-072** — EKSİK — Kriter 1–5 geçince statü yok. Düzeltme: üçüncü statü "Kâğıt": kartlar "kâğıt" etiketiyle üretilir (5.8 izleme zaten başlar); "Canlı" kriter 6'dan sonra.

**09-073** — OLGU — SE = %8/√30 = %1,46; %80 güçte MDE ≈ 2,49 × 1,46 = %3,6. Kâğıt dönem gerçek etkiyi (%1–2) sınamaya güçsüzdür; kriter 6 yalnız büyük bozulmayı yakalar.

**09-074** — EKSİK — Düzeltme: tek bakış: 6 ay ve 30 işlem dolunca; erken durdurma yok; üst sınır 12 ay, dolmazsa "ölçülemedi".

**09-075** — EKSİK — Düzeltme: kâğıt işlemler simülasyon AOF dolumuyla kapanır (kuralı ölçer); Levent'in gerçek dolumu ayrı bilgi sütunudur.

**09-076** — EKSİK — Düzeltme: kâğıt dönem başında anlık görüntü kilitlenir (4: tarihli değişmez anlık görüntü); sonraki düzeltmeler yeni anlık görüntüde yazılır, eski sonuç yeniden yazılmaz.

**09-077** — EKSİK — Düzeltme: kâğıt dönem piyasa durumu etiketine göre raporlanır ve doğrulamadaki aynı etiketli alt kümeyle kıyaslanır; tek rejimde "yarısı" şartı yorumlanamıyorsa "ölçülemedi".

**09-078** — EKSİK — Düzeltme: düzeltme işlem listesini değiştirmiyorsa aynı deneme, dönem sürer; değiştiriyorsa yeni kayıt tarihiyle dönem sıfırdan başlar. 5.8 bunu söylemiyor.

**09-079** — EKSİK — Düzeltme: hash = kod + paket sürümleri (pip freeze) + tohum + veri anlık görüntü kimliği + parametre kaydı.

**09-080** — EKSİK — Yok. Düzeltme: kayıt dosyasının hash'i dış zaman damgasıyla (OpenTimestamps ücretsiz ya da kendine e-posta/herkese açık commit) yazılır.

**09-081** — EKSİK — "İki aile" adlandırılmamış (olasılıkla ön denemedeki iki aile; doğrulanmadı). Düzeltme: aileler adlandırılır, sızıntı "bilinen yanlılık" olarak yazılır; sızıntıyı ölçen kontrol yok, ayrılmış dönem (5.8) bu yüzden kayıttan sonrasıdır.

**09-082** — EKSİK — Düzeltme: m'nin başlangıç değeri, KURALLAR §3'teki bütün aday ailelerin sayısı (seçilenler değil); seçim "Tansu gösterdi" ölçütüne dayandığı için yanlılık bununla sınırlanır.

**09-083** — EKSİK — Kriter 6 test değil, nokta oranı şartı (AND). Düzeltme: kâğıt dönemde Holm uygulanmaz; her aile ayrı karar; "güçsüz" notu (09-073) eklenir.

**09-084** — EKSİK — Düzeltme: birim = işlem başına fazla getiri (tek hisse bölmesi), günlük ortalama fazla getiri (çift bölmesi); yıllıklandırma yok, aynı birim iki dönemde karşılaştırılır.

**09-085** — EKSİK — Düzeltme: ay başı evren listesi canlı dönemde o gün dondurulup kaydedilir; kural hash'i evren kodunu içerir.

**09-086** — EKSİK — Kaçırılan tavan girişleri kuralın aleyhine okunmalı (gerçekçi). Düzeltme: sayısı raporlanır, K1 rastgele işlemleri de aynı giriş filtresini uygular.

**09-087** — OLGU — Günlük SD %1, 126 gün: SE (6 ay) = %11,2; %80 güç MDE = 2,49 × %11,2 ≈ %28 (6 ay) ≈ %56 yıllık. Bu, masrafın çok üstünde; kâğıt dönem çift bölmesinde yalnız çok büyük etkiyi yakalar. Günlük SD varsayımdır, doğrulanmadı.

**09-088** — EKSİK — Çift sayısı değişirse maruziyet değişir. Düzeltme: 09-021'deki maruziyet eşleşmesi çözer; çift sayısı yıl başına raporlanır.

**09-089** — EKSİK — Evet, rastgele geçişler de ortalamaya dönüşten yararlanır; null yükselir, K1 gücü düşer (muhafazakâr). Düzeltme: 09-015 ile aynı not; gerekirse güç düşüklüğü MDE ile raporlanır.

**09-090** — EKSİK — Beta düzeltmesi yok. Düzeltme: kriter dışı bilgi olarak fazla getirinin piyasa regresyonu alfası raporlanır; çift K2 (50/50) beta farkını zaten aynı çiftte tutar.

**09-091** — EKSİK — Evet olabilir. Düzeltme: kriter 2'ye "K3'e göre (nakit faiz) mutlak getiri de pozitif" eklenmesi; mutlak getiri karar kriteri yapılmadan alt koşul olarak.

**09-092** — EKSİK — Düzeltme: veri biterse son kapanıştan zorunlu çıkış; K2 sepeti ve K1 aynı kuralı uygular (simetrik), olay sayısı raporlanır.

**09-093** — EKSİK — Karar etkisi tanımsız. Düzeltme: BIST30 sonucu bilgi; işaret değişirse "kırılgan" etiketi, kabul kararı değişmez.

**09-094** — EKSİK — Açık soru 4: bedava veriyle ayrılamaz. Düzeltme: bilinen yanlılık olarak yazılsın; K1 ön şartı sinyal öncesi getiriyi koşullarsa tedbirli günler null'da da temsil edilir.

**09-095** — EKSİK — K1 sinyale özgü AOF kaymasını dengelemez. Düzeltme: kuralın giriş günlerinde |AOF−kapanış|/kapanış ortalaması rastgele günlerle karşılaştırılıp raporlanır; %0,5 masraf senaryosu (5.4) kısmen karşılar.

**09-096** — EKSİK — Evren 100 en büyük hisse olduğu için likidite farkı sınırlı, ama eşleştirme yok. Düzeltme: (a) türünde rastgele hisse sinyal hissesiyle aynı likidite kovasından (10 günlük medyan TL tutarı) seçilir.

**09-097** — EKSİK — Düzeltilmiş fiyat çarpansal yeniden ölçeklenir; oran temelli göstergeler çoğunlukla değişmez, ama sinyal defteri yoksa kaymalar görünmez. Düzeltme: canlı günlük sinyaller değişmez defterde tutulur; yeniden hesapla karşılaştırılıp fark raporlanır.

**09-098** — EKSİK — m'ye yalnız p üreten (aile, varyant, parametre) girer; yıl, hücre, masraf p üretmez (09-056, 09-057). "Hiçbir aile geçmedi" garanti değildir ama güç düşükse (09-065) olasıdır; 5.1'in kabulü bu. Düzeltme: m tanımı açık yazılsın, sonuç "geçmedi" ile "ölçülemedi" ayrılsın.

**09-099** — OLGU — Kısmen hesaplandı (simülasyon, null): tek aile için kriter 1 ≈ %1 (Holm α≈0,01), kriter 4 ile birlikte yine ≈ %1; 3 aile için ≤ ~%3, Holm FWER ≤ %5. Bu, K1 null'ının geçerli olduğu varsayımına bağlıdır; tasarım hesabı yazmıyor. "Önceden yazıldı" tek başına yanlış kabulü garanti etmez; 09-060'taki uçtan uca null koşusu gerekir.

**09-100** — EKSİK — 30 işlemde 20 günlük blokla birkaç blok çıkar; aralık güvenilmez. Düzeltme: kâğıt dönemde aralık < 10 blokta gösterilmez, p üretilmez; kriter 6 nokta oranıyla okunur (09-073); modül aynı, çıktı eşiği farklıdır.

## Özet

Sayımlar (100 soru):
1. CEVAPLI: 6 (010, 011, 023, 024, 033, 049)
2. EKSİK: 77
3. YANLIŞ: 3 (021, 022, 035)
4. OLGU: 11 (008, 026, 029, 030, 043, 048, 065, 067, 073, 087, 099)
5. ZAYIF SORU: 3 (004, 040, 045)

En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği:
1. 09-021/022 (YANLIŞ): K2 maruziyet eşleşmesiz. 5.7: karşılaştırma sepetini kuralın günlük maruziyetine ağırlıkla, kalan nakit aynı faizi kazanacak biçimde kur. Aksi halde faiz ve maruziyet farkı kural lehine ya da aleyhine mekanik fark üretir.
2. 09-008 (OLGU): B=1.000 ile m ≥ 51 olunca hiçbir aile geçemez. 5.11: B ≥ 2·m/α olsun, m arttıkça tekrar sayısı artsın.
3. 09-001/002/013 (EKSİK): K1 ön şartı yazılı değil. KURALLAR §3'e aile başına "K1 ön şartı" satırı; hash'e girer, değişirse yeni deneme.
4. 09-035/036 (YANLIŞ): Sabit 20 günlük blok. 5.9: durağan bootstrap, blok uzunluğu veriden (Politis–White) ya da ≥ ortalama tutma süresi (çiftte ≥ 66 gün).
5. 09-066/065/029 (EKSİK/OLGU): Pozitif kontrol ve ortak güç hesabı yok; kriterler bağımsız değil. Boru hattını enjekte edilmiş δ (%1, %2) ile koş; geçme olasılığını raporla.
6. 09-060/099 (EKSİK/OLGU): Yanlış kabul oranı ölçülmüyor. Boru hattını sentetik null veriyle 200 kez uçtan uca koş; oran ≤ %5 olmalı.
7. 09-044/050 (EKSİK): MDE etkiden büyükse sonuç belirsiz. 5.12'ye üçüncü sonuç "Ölçülemedi" ekle (Canlı / Reddedildi / Ölçülemedi).
8. 09-058/080/079 (EKSİK): Günlük ve kayıt dış doğrulama yok. Günlük ekleme-yalnız ve hash zincirli; motor günlüğe yazmadan getiri üretmez; hash kapsamı kod + paket sürümleri + tohum + anlık görüntü; dış zaman damgası.
9. 09-012/018 (EKSİK): Rastgele işlemin çıkışı tanımsız. 5.7: rastgele işlem kuralın tam çıkış paketini giriş fiyatından uygular.
10. 09-005/017/016 (EKSİK): K1 p'sinin türü belirsiz. 5.12.1: tek yönlü, istatistik = işlem başına ortalama fazla getiri, aile p'si = max(p_a, p_b).
