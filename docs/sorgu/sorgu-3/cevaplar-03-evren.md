# Cevaplar 03: Evren

Kaynak sırası: canlı veri (İş Yatırım `HisseTekil`, borsapy kodu) > TASARIM taslak 5 > veri-kaynaklari > KURALLAR > sorgu-2.
Ölçüm: 14 istek (THYAO 2015–2026, CCOLA, TUKAS, TCELL, ISCTR, ISATR, ISKUR, FINBN, ICBCT, ASYAB, VAKFN, FRIGO, ISFIN, DOCO) ve borsapy `info` okuması. Kod dosyası kaydedilmedi.

**03-001** — EKSİK — 5.2 "toplam PD" seçimini gerekçelemiyor. Veride `HAO_PD` hazır (THYAO HAO/PD 0,50; TCELL 0,39; ISCTR 0,29, 02.10.2026). Düzeltme: sıralama `HAO_PD` ile, `HAO_PD` boşsa `PD` ile; `PD` sıralaması duyarlılık varyantı olur. Not: `HAO_PD` gürültülü (CCOLA 15.08.2024'te 55,8 mlr → 6,7 mlr, oran 0,29 → 0,036), bu yüzden 20 günlük medyanıyla kullan.

**03-002** — OLGU — Doğrulandı. THYAO'da 2.947 satırın hepsinde `PD` = ham `HG_KAPANIS` × o günün `SERMAYE` değeri (oran 0,99999994–1,00000006). 02.01.2015 `PD` = 9,72 × 1,38 mlr. CCOLA/TUKAS'ta `SERMAYE` olay gününe kadar eski değerde, o gün yeni değerde: yani geçmiş günler bugünkü sermayeyle yeniden hesaplanmıyor. Sınır: kaynağın sonradan geçmişi düzeltmesi anlık görüntülerle (TASARIM 4, Veri deposu) izlenir.

**03-003** — OLGU — Doğrulandı, iki olayda öncül yanlış: CCOLA 13.08.2024 (`SERMAYE` 254 mn → 2,798 mlr) ve TUKAS 04.02.2025 (1,472 mlr → 4,5 mlr) `SERMAYE` fiyat düşüşüyle aynı gün değişti; `PD` sürekli kaldı (193,4 → 194,0 mlr; 9,17 → 9,18 mlr). Bedelli olayı sınanmadı. Düzeltme: günlük `PD` süreksizliği (olay yokken >%25) bayrak olsun.

**03-004** — EKSİK — Tasarım sessiz. Aynı şirketin kodları ayrı satırdır (ISCTR/ISATR/ISKUR ayrı satır döndü). KRDMA/B/D gibi gerçek çok kodlu şirketlerde `SERMAYE`'nin sınıf mı şirket mi olduğu sınanmadı. Düzeltme: evrende şirket başına tek kod (en yüksek 60 günlük TL hacimli); `kod_haritasi` tablosu elle tutulur. Evet, düzeltilmezse K2 aynı şirketi iki kez ağırlıklar.

**03-005** — EKSİK — Doğrulandı: ISATR ve ISKUR pay gibi döner (22/22 gün `HG_HACIM`=0, fiyat sabit, ISATR `PD`=4,95 mlr TL, ISKUR `SERMAYE`=1e-9). Bunları şimdilik yalnız sıfır hacim eler, bu yazılı değil. Düzeltme: evren yalnız "pay" olarak listelenmiş kodlardan (borsapy güncel liste + KAP kapanmış) kurulur; rüçhan/varant/BYF/imtiyazlı kodlar bu listede olmaz; ek güvenlik: 60 günlük medyan TL > 0.

**03-006** — EKSİK — Tasarım sessiz; veri sıfır hacimli satır döndürüyor (bkz. 03-096). Düzeltme: "işlem gören" = `HG_HACIM` > 0. Tek fiyatlı gün (`HG_MIN`=`HG_MAX`, hacim > 0) evren üyeliğini bozmaz ama o gün giriş yok (kilitli tavan kuralı gibi, 5.3).

**03-007** — EKSİK — Eşik yok. Düzeltme: ay başı kesitte tüm paylar arasında 60 günlük medyan TL'nin alt %20'si dışlanır; yüzde 5.10 parametre kaydına girer ve evren sürümüne yazılır. Karar veriden önce yazılır, sonuca bakılarak değiştirilmez.

**03-008** — EKSİK — Nominal sabit TL eşik evren boyutunu bozar. Düzeltme: eşik mutlak TL değil kesit yüzdeliği (03-007); böylece enflasyondan bağımsız ve boyut sabit.

**03-009** — OLGU — Doğrulandı: `HG_HACIM` TL'dir. (a) THYAO 02.10.2026 `HG_HACIM` = 8,98 mlr; lot olsaydı 292 TL fiyatla 8,98 mlr lot = sermayenin 6,5 katı, imkânsız. (b) CCOLA 12→13.08.2024 (11'e bölünme): hacim 808 mn → 361 mn, lot sayısı 11 kat sıçramadı. Medyan TL için `HG_HACIM` doğrudan kullanılır; fiyat × lot çarpımı gerekmez. TASARIM 5.1 ve 8'deki "çözülecek" ifadesi kapatılır.

**03-010** — EKSİK — Tasarım sessiz. Düzeltme: sıralama bir önceki ayın son işlem günü kapanışıyla yapılır (PD ve 60 gün, o günü dahil), liste ayın ilk işlem gününden geçerli olur. Aynı günün kapanışı kullanılırsa look-ahead olur.

**03-011** — EKSİK — 250 günlük göstergeler (SMA250, EMA200) zaten 2015 sonuna kadar sinyal üretmez; 60 günlük şart bağlayıcı değil. Düzeltme: 5.2'ye yaz: "ilk evren 60. işlem gününde (~Nisan 2015); ilk sinyal ~2016 başı". 5.8'in 2015–2017 başlangıcı bununla uyumlu (ilk sınanan yıl 2018).

**03-012** — EKSİK — Düzeltme: "ay başı" = Takvim modülünün verdiği ayın ilk işlem günü; liste o günden geçerli, sıralama bir önceki işlem günü kapanışıyla (03-010). Bayram kayması tarihi değil yalnız günü değiştirir.

**03-013** — EKSİK — Düzeltme: sinyal = dünkü koşul yanlış, bugünkü doğru ve hisse dünden beri evrende. Süregelen koşul sinyal sayılmaz. K1 aynı kuralı kullanır.

**03-014** — EKSİK — Düzeltme: evrenden çıkan hissede açık pozisyon açık kalır; evren yalnız yeni girişi sınırlar. Çıkış stop/SMA250/terminal kuralıyla (03-027). K1 aynı kuralı uygular. K2 sepeti ay başı yeniden kurulur (üyelik değişimi bir alım-satım sayılır, masrafla).

**03-015** — EKSİK — Yanlılık gerçek. K1 ve K2 aynı evrende olduğundan göreli sonuç büyük kısmıyla paylaşılır, mutlak sonuç etkilenir. Düzeltme: 5.2'ye bunu yaz; bir duyarlılık varyantı ekle: evreni 12 ay önceki PD sırasıyla kur (gecikmeli).

**03-016** — EKSİK — Histerezis yok. Düzeltme: girmek için ilk 100, çıkmak için 120'nin dışına düşmek. Açık pozisyonlar zaten açık kalır (03-014); asıl etki yeni sinyal kümesi ve K2 devir maliyeti.

**03-017** — EKSİK — Örtüşme hiçbir yerde ölçülmüyor. Düzeltme: bugünkü gerçek BIST100 (borsapy) ile ara evren (01.10.2026) ve KAP zinciri hazır olunca 2018'den bütün çeyrekler için örtüşme (Jaccard) raporlanır; "yeterince yakın" eşiği önceden yazılır (öneri ≥ %70, keyfidir, kayıtlı olsun). Ölçmedim: PD için ~500 istek gerekir, bütçeyi aşar.

**03-018** — EKSİK — Çürütme gözlemi yok. Düzeltme: KAP listesinin bulunduğu dönemde (2018 sonrası) kuralları hem gerçek BIST100'de hem ara evrende koş, göreli sonuç farkını raporla. İddia bu ölçüme kadar "azaltması beklenir" diye yazılır.

**03-019** — EKSİK — Kaynak gösterilmemiş. VBTS KAP duyuruları (2018+) tedbir listesi için aday kaynaktır, doğrulanmadı. Düzeltme: vekil olarak "tek fiyat günü" (`HG_MIN`=`HG_MAX`, hacim > 0) oranı hisse ve yıl başına raporlanır.

**03-020** — ZAYIF SORU — Gerçek BIST100 de holding ve iştirakleri ayrı şirket olarak içerir; her biri ayrı menkul kıymet. Çift seçimi sektör içindedir (S2-22). Ek önlem gerekmez.

**03-021** — ZAYIF SORU — Gerçek BIST100 de sabit 100'dür; evren "o günün en büyük 100'ü" olarak göreli tanımlıdır. Yıllık ileri yürüme aynı tanımı ölçer.

**03-022** — EKSİK — Evren modülü tarih → hisseler (4) ama canlı kaynak yazılı değil. Düzeltme: canlı günlük de aynı PD kuralıyla Evren modülünü çağırır (A5); gerçek BIST100'e geçilirse sınama ve canlı birlikte geçer, tek modül.

**03-023** — EKSİK — Kapanmış sembol keşfi tasarımda yok. Ölçüm: FINBN 2015–2016 için 0 satır döndü; yani İş Yatırım her kapanmış kodu tutmuyor (ASYAB tutuyor). Düzeltme: aday liste = borsapy bugünkü ∪ KAP "işlem sırası kapatıldı" bildirimleri (haftalık zaman pencereleriyle 2000 kayıt sınırını aşarak), sonra her kod `HisseTekil` ile sınanır; tamlık ölçüsü: kodu bilinen kapanmışların kaçı veri döndürdü, rapora yazılır.

**03-024** — EKSİK — Eşik yok. Düzeltme: bulunan kapanmış sembol sayısı KAP'tan sayılabilen delist sayısının %80'inin altındaysa "üst sınır" yerine "yönü bilinmiyor" yazılır. Yüzde keyfidir, kayıtlı olsun.

**03-025** — OLGU — Doğrulandı, kısmen: ASYAB ham, `HGDG` ve `PD` döndürür (`HAO_PD` boş; 395 satır, son 25.07.2016, son fiyat 0,87). FINBN boş. VAKFN zaman aşımı (sonuç yok). FRIGO, ISFIN, DOCO hâlâ listeli çıktı, kapanmış değil. Yani "eksiksiz dönen" kapanmış kod sayısı 1 (ASYAB); örneklem bu kadar.

**03-026** — OLGU — Doğrulayamadım (KAP bildirimi okunmadı). Veriden: son satırda hacim 0, son fiyat 0,87 (Ocak 2015'te 0,64), yani son fiyat bir çıkış fiyatı değil taşınmış fiyat olabilir. Gerçek çıkış değeri için KAP gerekir.

**03-027** — EKSİK — Tek kural yok. Düzeltme: terminal getiri = nedene göre: pay alım teklifi/birleşme → teklif veya takas değeri (KAP); tasfiye/iflas/neden bilinmiyor → son temiz kapanışın −%100'ü (kötümser); duyarlılık: son fiyat. Neden etiketi raporda yazılır.

**03-028** — EKSİK — Düzeltme: durdurmada pozisyon son kapanıştan değerlenir, çıkış ertelenir, nakit boşta faiz kazanır; durdurma 60 işlem gününü aşarsa delist kuralı (03-027) uygulanır. Süre keyfidir, kayıtlı olsun.

**03-029** — EKSİK — Birleşme kodu bilinmiyor (veri-kaynaklari 8.3). Düzeltme: karantina listesi elle incelenir, birleşme günleri `kod_haritası`na etiketlenir; fiyat yamanmaz (5.1), yalnız o pencere çıkar. Sayısı raporlanır.

**03-030** — ZAYIF SORU — Karantina yalnız günlük limiti (±%10/%20) aşan hareketi yakalar; limit gerçek çöküşün tek günde karantinaya girmesini engeller, çöküş birkaç günde limit içinde yaşanır. Karantina veri hatasını yakalar, çöküşü değil.

**03-031** — EKSİK — Düzeltme: açık pozisyon, karantina gününden önceki son temiz kapanıştan kapatılır, işlem "karantina çıkışı" etiketli ayrı sayılır, sayısı raporlanır. Yönü bilinmiyor.

**03-032** — OLGU — Doğrulayamadım (sembol değişimi örneği sınanmadı). `HisseTekil` kod ister; eski kod için yalnız eski dönem dönmesi olası. Düzeltme: `kod_haritası` (03-004) eski-yeni kodu bir şirket altında birleştirir ve 60 günlük medyan kod değişse de sıfırlanmaz.

**03-033** — EKSİK — Düzeltme: aynı kodda 20 işlem gününden uzun veri boşluğu veya `SERMAYE`/`PD` kopması varsa seri ikiye bölünür. BIST'te kod yeniden kullanımı nadir, ölçmedim.

**03-034** — EKSİK — Düzeltme: evren şirket başına tek kayıttır (`kod_haritası`, 03-004); bu tablo elle tutulur. İki kez ya da hiç bulunma riski ancak bu tablo olmadan vardır.

**03-035** — OLGU — Doğrulayamadım (spin-off örneği sınanmadı). Düzeltme: `HGDG/HG` oranında olay yokken sıçrama bayrak olur; çarpan yansıtmıyorsa karantina limit içindeki bölünmeyi yakalamaz, bayrak onu yakalar.

**03-036** — OLGU — Doğrulayamadım (`GetSermayeArttirimlari` kapanmış kodla sınanmadı). Ama `HGDG` ASYAB için dönüyor ve `HGDG/HG` son günde 1,0. Fallback: olay tablosu yoksa çarpan `HGDG/HG` oranından türetilir (kendi başına çapraz kontrol kaybolur).

**03-037** — EKSİK — Evet, eşitsizlik var; borsapy kapanmış hisseyi bilmez. Düzeltme: raporda "ikinci kaynakla doğrulanan hisse-gün oranı" güncel ve kapanmış için ayrı yazılır; kapanmışlar için `HGDG/HG` tutarlılığı ve limit kontrolü yedek kontroldür.

**03-038** — OLGU — Doğrulandı, kısmen: FINBN 2015–2016 için 0 satır (İş Yatırım bazı eski kodları tutmuyor). Yani yalnız İş Yatırım'dan delist yıl dağılımı ölçülemez. Bağımsız sayım için KAP işlem sırası kapatma bildirimleri gerekir.

**03-039** — EKSİK — Doğru, evren çıkışı yanlılığı kısmen geri getirir (gerçek BIST100 de aynıdır). Düzeltme: 03-014 (açık pozisyon kalır) ve 03-027 (terminal kural) ile kayıp işlemde görünür; raporda "evrenden çıktıktan sonra delist olan sayı" yazılır.

**03-040** — EKSİK — Aynı. Ara evren yalnız (a) evrendeyken delist olanları ve (b) evrenden çıkıp pozisyonu açık kalanları içerir. Düzeltme: 03-014 + 03-027; (b) sayısı raporlanır.

**03-041** — EKSİK — Kod keşfi hiçbir adımda yok. Düzeltme: Uygulama sırası 1'e "1b: aday kod listesi" ekle (03-023); brute-force yapılmaz. Hız: 1 sn bekleme (S2-17) ile ~700 kod ≈ 12–25 dk (belirsiz; zaman aşımı gözlendi).

**03-042** — CEVAPLI — 5.2 ve 7.8: KAP hazır olana kadar PD ara evreni ve yanlılık uyarısı geçerli; 2015–2016 için KAP kapsamı yoksa ara evren kalır.

**03-043** — EKSİK — Düzeltme: başlangıç = bugünkü liste (borsapy CSV), geriye doğru uygula. Bağımsız kontrol: her çeyrekte liste tam 100 hisse ve giren sayısı = çıkan sayısı; bozulursa zincir durur; ayrıca ara evrenle örtüşme (03-017) sürekli izlenir.

**03-044** — EKSİK — Düzeltme: çeyrek içinde boşalan yer, o günkü PD sıralamasında listede olmayan en büyük hisseyle doldurulur (yedek kural). Liste 100'de kalır.

**03-045** — EKSİK — Düzeltme: üyelik yürürlük tarihinden başlar (duyuru tarihinden değil); duyuru tarihi kullanılırsa girişten önce fiyat hareketine bakılır. Yürürlük tarihi PDF'te yazar.

**03-046** — EKSİK — Düzeltme: ~40 PDF iki ayrı okumayla çıkarılır, fark elle çözülür; değişmez: giren = çıkan; ayrıca zincirin sonu bugünkü listeyle birebir tutmalı.

**03-047** — EKSİK — 2015–2026 zaten geliştirme verisi (5.8), yeni evren yeni ayrılmış dönemi tüketmez ama yeni denemedir. Düzeltme: kural kaydı evren sürümünü içerir; KAP evreni gelince Holm'e yeni deneme olarak eklenir; Canlı kararı için KAP evreni bağlayıcıdır.

**03-048** — EKSİK — Doğru, iki etki karışıyor. Düzeltme: ara evren ayrıca çeyrek başı da kurulur (varyant); KAP ile karşılaştırma çeyrek–çeyrek yapılır, fark yalnız kaynaktan gelir.

**03-049** — OLGU — Doğrulandı: borsapy sektörü KAP şirket sayfasından kazır (`_providers/kap.py` 389–395, `ticker.py` 367). Tek seviye ve çok kaba: AGROT "TARIM, ORMANCILIK VE BALIKÇILIK", GARAN "MALİ KURULUŞLAR", KRDMD ve TUPRS ikisi de "İMALAT". Bugünkü durum, geçmiş yok.

**03-050** — EKSİK — Kapanmışın KAP sayfası yoktur, sektörü olmaz. Düzeltme: sektörsüz hisse çiftlere girmez ve rapora "çift bölmesi hayatta kalanlardan kurulur" yazılır; veya bilinen kapanmışlara elle sektör atanır.

**03-051** — EKSİK — Düzeltme: yıl başı seçim o yılın Ocak ay başı ara evren listesiyle yapılır.

**03-052** — EKSİK — Düzeltme: çift yıl sonuna kadar sürer; aylık evren veya likidite şartı çifti bozmaz (03-014 ile tutarlı); yalnız delist/durdurma bozar (03-060).

**03-053** — ZAYIF SORU — Çelişki yok: 2015–2017 ileri yürüme eğitim penceresidir (ilk sınanan yıl 2018), ilk çift yılı 2016 bununla uyumlu. Küçük not: 2015'te ~250 işlem günü olabilir; 252 şartı 2016 başında bir kaç gün karşılanmayabilir (sayılmadı).

**03-054** — EKSİK — KAP sektörü kaba olduğu için İMALAT tek sektör olarak yüzlerce çift üretir (veri: KRDMD ve TUPRS ikisi İMALAT). Düzeltme: sektör başına en çok 2 çift ve seçilen çiftlerin sektör dağılımı raporlanır.

**03-055** — CEVAPLI — Sağlamıyor (doğrulandı: AGROT tarım, GARAN mali). 5.6 zaten "Tansu'nun çiftleri ayrıca gösterilir, kabul kararına girmez" der; ikisi aynı yöntemin örneği sayılmaz.

**03-056** — EKSİK — "Bilinen küçük" ölçümsüz. Düzeltme: ifade "bilinen, büyüklüğü ölçülmemiş yanlılık" olur; duyarlılık: sektör kısıtsız çift varyantı.

**03-057** — EKSİK — Evet, hafif look-ahead olur. Düzeltme: 03-056 ile aynı varyant (sektör kısıtsız ve geriye bakan korelasyon kümesi) sonucu karşılaştırır.

**03-058** — OLGU — Eşleşme doğrulanmadı, ama KAP sektörü çok kaba (İMALAT, MALİ KURULUŞLAR) ve "Petrol", "Demir Çelik" gibi ince adlar orada yok. Düzeltme: sektör rotasyonu ailesi (D) bu sınıflamayla kurulamaz; ilk sürüm kapsamında değil, ayrı bir sınıflama kaynağı gerekir.

**03-059** — EKSİK — Düzeltme: açgözlü seçim: çiftler p'ye göre sıralanır, bir hisse bir kez kullanılır, 5'e dolana kadar sürer; 5'ten az çıkarsa boş pay nakitte kalır ve faiz kazanır (5.6 zaten faizi tanımlar).

**03-060** — EKSİK — Düzeltme: o payın pozisyonu 03-027/03-028 kuralıyla kapanır, pay yıl sonuna kadar nakitte faiz kazanır, çift yeniden seçilmez.

**03-061** — EKSİK — Düzeltme: sektör başına en çok 2 çift (03-054); yoğunlaşma sınırı budur.

**03-062** — EKSİK — İki pencere farklı iş yapar: 60 gün evren üyeliği, 10 gün işlem kapasitesi. Düzeltme: 10 günlük medyan tavanı sıfıra yakınsa sinyal atlanır, "likidite yüzünden atlanan sinyal" sayısı raporlanır; K1 aynı kuralı uygular.

**03-063** — EKSİK — Düzeltme: likidite tavanı yüzünden kesilen pozisyonların oranı yıl bazında raporlanır; oran yıllara göre kayarsa 1.000.000 TL TÜFE ile endekslenir.

**03-064** — EKSİK — Düzeltme: sıra 10 günlük medyan TL ile, sinyal günü dahil. Sinyal kapanışta bilindiği için look-ahead değil, ama 5.6'ya yazılmalı.

**03-065** — EKSİK — Tasarım sessiz. Düzeltme: K2 ay başı evrenle birlikte yeniden dengelenir ve %0,3 masraf uygulanır; maliyetsiz sepet kural–sepet farkını kuralın aleyhine çarpıtır.

**03-066** — EKSİK — Düzeltme: sepet üyeliği giriş günü evrenidir, tutma süresince günlük eşit ağırlık; sepette delist olursa 03-027 terminal kuralı.

**03-067** — EKSİK — Düzeltme: ±20 gün içinde hissenin evrende olduğu ve ön şartı sağlayan günlerden seç; yoksa o işlem (a) türüne düşer, sayısı raporlanır.

**03-068** — EKSİK — Düzeltme: sinyal ve K2 için 250 günlük geçmiş şartı; göstergesi hesaplanamayan hisse sinyal üretmez. Evren (60 gün) ile işlem uygunluğu (250 gün) ayrı yazılır.

**03-069** — EKSİK — Düzeltme: 03-068'in 250 gün şartı halka arz hisselerini dışarıda tutar; K2 de aynı şartı uygular.

**03-070** — EKSİK — Evet, boyut tilt'i var. Düzeltme: K2'nin PD ağırlıklı bir ikinci sepeti ayrıca raporlanır; iki sepet arasındaki fark tilt'in büyüklüğünü gösterir.

**03-071** — EKSİK — Düzeltme: çeyrek dönüşü endeks yeniden dengeleme günündeki girişler etiketlenir; sonuçlar bu günler dışarıda da raporlanır. Etkisi ölçülmedi.

**03-072** — EKSİK — Düzeltme: K2 üyeliğine "%2 likidite tavanıyla alınabilen en az X TL" şartı eklenir; kuralın fiilen işlem yapabildiği evrenle aynı olur.

**03-073** — EKSİK — Kaynak yok (veri-kaynaklari 4). Düzeltme: ölçüm KAP'ta bulunan en eski listeyle (2018 Q1, bildirim 645948) yapılır; 2015 listesi bulunursa ek ölçüm olur.

**03-074** — EKSİK — Düzeltme: tek kesit (ilk bulunan liste, öneri 2018 Q1); liste kesitten 2026'ya kadar sabit izlenir (delistleri içerir).

**03-075** — EKSİK — Doğru. Düzeltme: BIST30 yerine BIST100'ün tam listesi (KAP ekinde 100 hisse var) alınır; böylece 50.–100. sıra da ölçülür.

**03-076** — EKSİK — 30 hissede 100 işlem ve 60 sinyal günü şartı büyük olasılıkla sağlanmaz (özellikle EMA sıkışması). Düzeltme: ölçüm istatistik testi değil yön göstergesi olarak yazılır; 5.9 şartı sağlanamazsa "yetersiz örneklem" yazılır.

**03-077** — EKSİK — Ayırma yok. Düzeltme: sabit liste ile ara evrenin ilk 30'u (aynı yöntem, aynı boyut) karşılaştırılır (= kurma yöntemi); ara evrenin ilk 30'u ile 100'ü karşılaştırılır (= boyut); kalan = yanlılık.

**03-078** — EKSİK — Genelleme yok. Düzeltme: ölçüm iki kesitte (2018 Q1 ve bir sonraki bulunan) yapılır; liste yaşıyla yanlılık eğimi raporlanır. Tek kesit yalnız bilgi.

**03-079** — EKSİK — 5.12'de bağlı karar yok. Düzeltme: 5.12'ye 7. madde ekle: sabit listede kural–K2 fazla getirisinin işareti ara evrenle aynı olmalı; değilse aile "Deneme"de kalır.

**03-080** — EKSİK — İkinci kontrol yok. Düzeltme: listeyi iki ayrı okumayla çıkar ve fark çöz; çıkarılan liste bugünkü CSV'ye ters uygulama zinciriyle de uyuşmalı (03-043).

**03-081** — EKSİK — Evet, önce kod haritası gerekir (03-034). Ölçüm bu tablo hazır olmadan kurulamaz; uygulama sırasında 8'in önüne konur.

**03-082** — EKSİK — Aynı çözüm 03-077: ara evren ayrıca sabit bir listeyle (aylık yeniden kurma yok) koşulur; fark = kompozisyon/devir etkisi.

**03-083** — YANLIŞ — "Mutlak getiriler üst sınırdır" işareti kanıtsız yazılmış. Ters yönlü etkiler var (sabit %0,3 masraf az likit hissede düşük, brüt takas/tedbir, ortak kodlar). Düzeltme: ifade "üst sınır olması beklenir, işaret 03-073…080 ölçümüyle sınanır" olur.

**03-084** — EKSİK — Evet, yanlılık göreli farkta da kalır: K2 tutar, stoplu kural çıkar; yönü kuralın aleyhine olması beklenir ama doğrulanmadı. Düzeltme: 03-073…078 ölçümünde hem mutlak hem K2'ye göre fark raporlanır; "yalnız göreli yorum" yalnız ortak evren etkisini korur.

**03-085** — CEVAPLI — Kısmen: K1 kuralın ön şartlarını sağlayan günlerden seçer (5.7); ön koşula koşullu yanlılık eşit tutulur. Kalan etki (sinyalin kendisine koşullu) 03-073…080 ölçümüyle sınanır.

**03-086** — YANLIŞ — "Mutlak getiri karar için kullanılmaz" (5.2) ile 5.12 portföy kuralı çelişir. Düzeltme: kural tek yönlü kullanılır: %25 düşüş veya 12 ay aşılırsa ret; aşılmazsa "yanlılıklı eğride geçti, kanıt değil".

**03-087** — EKSİK — Düzeltme: canlı evren aynı PD kuralıyla kurulur (03-022); canlıda hayatta kalan yanlılığı yoktur, doğrulama etkisi yanlılıkla şiştiği için "en az yarısı" ölçütü muhafazakâr kalır.

**03-088** — CEVAPLI — 6.4 örneği kartta yalnız fazla getiri gösterir. Raporda mutlak getiri satırının yanına "(üst sınır olması beklenir)" etiketi eklenir.

**03-089** — EKSİK — Düzeltme: 5.11 günlük alanlarına "evren sürümü" (kural, PD eşiği, 60, 100, kaynak) eklenir; evren varyantı da deneme sayılır ve Holm'e girer.

**03-090** — EKSİK — Düzeltme: 5.8 kural kaydı hash'i evren kodunu ve eşiklerini kapsar; evren parametresi değişirse yeni deneme ve yeni ayrılmış dönem.

**03-091** — ZAYIF SORU — Sadakat kontrolü Tansu'nun rakamlarını yeniden üretir ve Yahoo verisiyle yapılır (7.2); evrenden bağımsızdır. PD sıralaması doğrulanmadı (~500 istek gerekir).

**03-092** — EKSİK — Düzeltme: 5.2'ye yaz: "evren 100'dür; Tansu'nun momentum sınamasındaki 500+ evreni ve BRYAT'ın BIST30/100'ünü temsil etmez; ikincisini yaklaşık temsil eder."

**03-093** — EKSİK — Düzeltme: 5.2'ye "YORUM: likit hisse = PD + işlem tutarı; Tansu'dan değil bizden" etiketi; evren sürümü rapor başlığına yazılır (03-089).

**03-094** — EKSİK — Düzeltme: rapor başlığına "Evren: PD-ara-v1 (YORUM, Tansu'nun tanımı yok)" satırı; KURALLAR E'deki "likit hisse" YORUM'una bağlanır.

**03-095** — EKSİK — Brüt takas veride ayırt edilemez, tek fiyat günü ayırt edilir (`HG_MIN`=`HG_MAX`). Düzeltme: tek fiyat günü bayrak; o gün giriş yok, evren üyeliği etkilenmez.

**03-096** — OLGU — Doğrulandı: sıfır hacimli satır dönüyor ve fiyat taşınıyor. ISATR/ISKUR 22/22 gün, ASYAB 8 satır; THYAO 0/2.947. Düzeltme: `HG_HACIM`=0 günler fiyat serisinden (ATR, eşbütünleşme) düşer, 60 günlük medyan TL'de 0 olarak kalır.

**03-097** — YANLIŞ — "Fiili dolaşım evrende yok" öncülü veriyle çelişir: `HAO_PD` her satırda var (03-001). S2-51'deki "KAP verisi gerekiyor" yanlış; `HAO_PD/PD` doğrudan fiili dolaşım yüzdesi verir (gürültülü, ASYAB'ta boş). Düzeltme: S2-51'i düzelt; `HAO_PD` varyantı ilk sürümde yer alır.

**03-098** — EKSİK — 03-047 ve 03-090 ile aynı. Kural kaydı evren sürümünü içerir; Adım 8 farklı evren getirirse yeni deneme olur, Holm'e girer.

**03-099** — EKSİK — Bitiş koşulu yok. Düzeltme: "ara evrenle hiçbir aile Canlı olmaz; Canlı kararı için KAP veya DataStore evreniyle yeniden koşu şart" yaz; DataStore ve KAP ikisi de çökerse karar verilmez, ara evren bilgi olarak kalır.

**03-100** — EKSİK — Ad iddiadan fazla. Düzeltme: evren "nokta-zamanlı PD evreni" adını taşır; "yanlılığı azaltan" sıfatı yalnız KAP'tan 03-024 eşiğinin üstünde kapanmış sembol bulunursa kullanılır.

## Özet

**Hüküm sayıları** (dosyadan sayıldı):

| Hüküm | Sayı |
|---|---|
| CEVAPLI | 4 |
| EKSİK | 76 |
| YANLIŞ | 3 |
| OLGU | 12 |
| ZAYIF SORU | 5 |
| Toplam | 100 |

**Doğrulanan olgular** (14 istek, 1 sn ara, kayıtlı dosya yok)
1. `PD` = ham `HG_KAPANIS` × o günün `SERMAYE` (THYAO 2.947 satır, oran 1,0000). `PD` nokta-zamanlıdır: eski günlerde eski `SERMAYE` kalır.
2. CCOLA (13.08.2024) ve TUKAS (04.02.2025): `SERMAYE` fiyat düşüşüyle aynı gün güncellenir, `PD` sürekli kalır.
3. `HG_HACIM` TL'dir (THYAO'da lot olsaydı sermayenin 6,5 katı; CCOLA bölünmesinde hacim 11 kat sıçramadı).
4. `HAO_PD` var ve fiili dolaşım oranını verir (THYAO 0,50; TCELL 0,39; ISCTR 0,29) ama gürültülü (CCOLA 0,29 → 0,036 iki gün içinde) ve ASYAB'ta boş.
5. Sıfır hacimli satırlar dönüyor, fiyat taşınıyor (ISATR/ISKUR 22/22 gün; ASYAB 8 satır; THYAO 0). ISATR/ISKUR pay gibi görünüyor (`SERMAYE` 1000 ve 1e-9).
6. Kapanmış kod kapsamı eksik: ASYAB tam döner, FINBN 2015–2016 için boş, VAKFN zaman aşımı; FRIGO/ISFIN/DOCO hâlâ listeli.
7. borsapy sektörü KAP şirket sayfasından, tek seviye ve kaba: AGROT "TARIM, ORMANCILIK VE BALIKÇILIK", GARAN "MALİ KURULUŞLAR", KRDMD ve TUPRS "İMALAT". AGROT–GARAN aynı sektör değil.

**En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği**
1. 03-001 / 03-097 (EKSİK/YANLIŞ): evren sıralaması `HAO_PD` ile (boşsa `PD`), 20 günlük medyan; `PD` sıralaması duyarlılık varyantı; S2-51 "KAP gerekiyor" ifadesi düzeltilir.
2. 03-010 / 03-012 (EKSİK): sıralama önceki ayın son işlem günü kapanışıyla, liste ayın ilk işlem gününden geçerli (look-ahead kapanır).
3. 03-014 / 03-039 / 03-040 (EKSİK): evrenden çıkan hissede açık pozisyon açık kalır; evren yalnız yeni girişi sınırlar. Kayıp işlemde görünür.
4. 03-027 / 03-028 / 03-031 (EKSİK): delist, durdurma ve karantina için tek terminal getiri kuralı (neden etiketli; bilinmiyorsa −%100, duyarlılık son fiyat; durdurma 60 gün aşarsa delist).
5. 03-004 / 03-032 / 03-034 (EKSİK): `kod_haritası` tablosu: şirket başına tek kod, kod değişimi ve çok sınıflı paylar. Ölçüm (03-081) buna bağlı.
6. 03-005 / 03-006 / 03-096 (EKSİK/OLGU): evren yalnız "pay" listesinden; "işlem gören" = `HG_HACIM` > 0; sıfır hacimli günler fiyat serisinden düşer.
7. 03-023 / 03-041 / 03-024 (EKSİK): Uygulama sırasına "1b kapanmış kod keşfi" (borsapy ∪ KAP işlem sırası kapatma, haftalık pencerelerle); tamlık oranı raporlanır; eşik altında "üst sınır" yerine "yönü bilinmiyor".
8. 03-007 / 03-008 (EKSİK): likidite eşiği kesit yüzdeliği (alt %20), 5.10 parametre kaydı ve evren sürümüne yazılır.
9. 03-089 / 03-090 / 03-047 / 03-098 (EKSİK): evren sürümü deneme günlüğüne ve kural hash'ine girer; evren değişimi yeni deneme ve Holm'e sayılır; Canlı kararı KAP/DataStore evreniyle yeniden koşuya bağlı (03-099).
10. 03-083 / 03-086 (YANLIŞ): "mutlak getiriler üst sınırdır" kanıtsız; "olması beklenir, 03-073…080 ölçümüyle sınanır" yaz; 5.12 portföy kuralı tek yönlü (aşarsa ret, aşmazsa kanıt değil). Ek: 03-054/03-061 sektör başına en çok 2 çift (KAP sektörü kaba, İMALAT tek sektör).
