# Cevaplar 05: AB=CD

Yöntem notu. "Ölçüm" = ben görselden okudum (piksel, ±%1) ve Python ile hesapladım. Üç ana bulgu aşağıdaki cevapların çoğuna dayanır.

- B1. SMRTG tablosunda (`gorsel-paket-03/02`) hedef getirisi = (C−D)/C. Grafikten okunan C ve D ile: #2 C 21,19 D 13,43 → 36,62 (tablo 36,59); #3 18,8 / 13,37 → 28,88 (28,93); #4 15,2 / 7,49 → 50,72 (50,72); #5 11,98 / 6,31 → 47,33 (47,30). Yani D, C'nin altında (aşağı kalıp) ve giriş fiyatı C'nin kendisi.
- B2. Tansu'nun grafik başlıkları (Yükseliş/Düşüş) D yönüyle tutarsız: KRPLS "Düşüş" ama D yukarı; MARKA "Düşüş" ve D aşağı; SMRTG "Yükseliş" ama D'lerin çoğu aşağı. Yön için başlık değil D'nin konumu kullanılmalı.
- B3. SMRTG #1 (C 2024-03-27, yukarı kalıp: A≈16,1, C≈17,8, D 27,34 BOZULDU): tablo zararı −%23,29; A stopu (C−A)/C ≈ −%10 verirdi (ölçüm). Stop A'dan dolmamış.

**05-001** — YANLIŞ — "A dip…D yukarıda" KURALLAR §3.2'de yok; sorgu-2 S2-32'de var. KURALLAR §3.2 yönsüzdür (D=C+r(B−A) işaretli). BUY şablonu (A tepe, D dip) ikinci eldir (gorsel-paket-39); birinci elde KRPLS D yukarı, MARKA ve RYSAS D aşağı, SMRTG karışık (B1). Tasarımın yön seçimi hiçbir kaynakla gerekçelenmemiş. Düzeltme: S2-32'ye "yön = YORUM; sadakat kontrolü yönsüz koşulur" yaz; KURALLAR §3.2'ye yön satırı ekle; §4'teki MARKA (aşağı kalıp) yalnız yönsüz formülle üretilir.

**05-002** — EKSİK — KAPLM notu (birinci el, kesik cümle) Tansu'nun "Bullish/AL" kalıbında CD'nin aşağı olduğunu söylüyor (D'de al). Tasarımın "yalnız alış" ifadesi işlem yönüdür, Tansu etiketi değil; C'den yukarı long, Tansu terimiyle "Bearish/SAT" geometrisidir. Düzeltme: GLOSSARY'ye "Alış = işlem yönü; Tansu'nun Bullish/AL = D'de al" yaz. "Bullish" kelimesini tasarımda kullanma.

**05-003** — EKSİK — Çelişki gerçek: KRPLS A=7,20 dip, yani BUY şablonunun tersi. Sadakat kontrolü işaretli formülle (D=C+r(B−A)) koşulur; şablon gerekmez (KRPLS: 8,22+3,05=11,27, etikette 11,29). Düzeltme: §4 satırına "yönsüz formül" yaz.

**05-004** — EKSİK — Tansu'nun iki ayrı işlemi var: D'de alış (RYSAS, LUKSK; sonuç yok) ve C→D bacağı (SMRTG/ISKPL; sayı var). Tasarım ikincisini sınıyor çünkü yalnız onun sonucu var. Bu seçim yazılı değil. Düzeltme: KURALLAR §3.2'ye bir cümle ekle: "D'de alış varyantı sınanmaz, sonucu yok".

**05-005** — OLGU — Birinci el tabloda giriş fiyatı sütunu yok (# | Tarih (C) | Sonuç | Getiri % | Sermaye). Doğruladım (B1): 4/4 hedef işlemde getiri, giriş = C fiyatı varsayımıyla (C−D)/C'ye 0,05 puan içinde eşleşiyor. Yani giriş C'de ve D<C (aşağı kalıp).

**05-006** — OLGU — "Tarih (C)" giriş tarihidir: getiriler C fiyatından hesaplanmış (B1). Giriş C'nin kendi gününde ve fiyatında olduğundan Tansu'nun sonucu look-ahead içerir (C pivotu sonradan bilinir). S2-31 bunu "fark raporda" diye karşılıyor; kanıt artık var.

**05-007** — EKSİK — S2-33 "C > A" der (kesin); KURALLAR §3 "C, A'yı ihlal etmez" der (C=A'ya izin gibi okunur). q=1'de risk sıfır, adet sonsuz. Düzeltme: KURALLAR §3'ü S2-33'e hizala: "C > A"; çok küçük risk için bkz. 05-051.

**05-008** — EKSİK — q alt sınırı için kaynak yok. Tansu'nun ölçülen q'ları 0,666–0,88. Düzeltme (YORUM): alt sınır koyma; sonuçları q dilimlerine göre ayrı raporla (<0,382 / 0,382–0,618 / >0,618), ayar yapma.

**05-009** — ZAYIF SORU — Hedefe mesafe C'den D'ye r·AB'dir (KRPLS #1: 3,05 TL, ≈%37), B'ye (r−q)·AB değil. "B'nin ötesinde" yalnız geometri şartıdır.

**05-010** — ZAYIF SORU — Kaynak B direnci için kural vermez; ek kural yeni özellik olur. Etki, sonuçta zaten ölçülür.

**05-011** — OLGU — q=1,00 yalnız ikinci el nottan gelir (tweet-abcd-geometrik…; URL ve tarih yok, "doğrulanmadı" diyor). Birinci elde en yüksek q 0,88 (ölçüm). Tansu'ya aidiyeti doğrulanamaz. Düzeltme: KURALLAR'da bu sınırı "ikinci el" etiketle.

**05-012** — YANLIŞ — Hayır. B1'e göre doğruladığım 4 hedef işlemin 4'ü aşağı kalıp (D<C). KURALLAR §1 satır 29 "SMRTG 12 kalıp +%305" bunu yalnız-alış evreniyle yan yana koyuyor. Düzeltme: 12 ve 5 sayıları yönsüz tarayıcıyla kıyaslanır; yalnız-uzun alt kümesi ayrı satır olur.

**05-013** — OLGU — İşlem tablosunda yön sütunu yok (birinci el). Yön yalnız SMRTG grafiğindeki D konumundan çıkar (D<C → aşağı). Ayrım görselde dolaylı vardır, tabloda yoktur.

**05-014** — EKSİK — Kalıp zikzak (kalın çizgi) köşelerinde çiziliyor: KRPLS A,B,C zikzak köşeleri, küçük işaretler değil (ölçüm). Seçim yazılı değil. Düzeltme: A,B,C büyük ölçek (zikzak) köşeleri; eşik parametresi 5.10 ızgarasında; seçim sadakat kontrolünden önce yazılır.

**05-015** — ZAYIF SORU — KURALLAR §3 AB=CD'de Swing=15 yok; yalnız "gizli pozitif uyumsuzluk" satırında (satır 38). AB=CD pivotu "sadakat kontrolüyle belirlenecek".

**05-016** — CEVAPLI — S2-31: Tansu giriş C fiyatından ise "fark raporda gösterilir". Not: sol-only pivot da kesinleşmez (yeni dip C'yi kaydırır), gecikme gizli kalır. Sadakat raporunda "Tansu modu (C fiyatı, aynı gün)" ayrı satır olsun.

**05-017** — EKSİK — R için kaynak yok. Düzeltme (YORUM): R'yi ızgarada yaz (örn. 1/3/5); sadakat kontrolünde C tarihleri ve D değerleriyle seç, getiriye bakma (§4 kuralı).

**05-018** — EKSİK — Evet: serbest parametre (L, R, eşik, fitil/kapanış, ölçek) 3 gözlemden fazla. Birinci elde daha çok kesin veri var: SMRTG 10 ve ISKPL 5 C tarihi, SMRTG grafiğinde 8+ D etiketi. Düzeltme: §4 AB=CD satırına bunları ekle; seçim önceden yazılı ızgaradan yapılır.

**05-019** — EKSİK — Ölçüt yazılı değil. Düzeltme (YORUM, koşudan önce yaz): D farkı ≤ %1 (okuma hatası ±0,05 TL dahil), C tarihi ±2 işlem günü, KRPLS 2/2 ve MARKA 1/1, SMRTG+ISKPL C tarihlerinin en az yarısı. Eşik değişirse deneme sayılır.

**05-020** — EKSİK — Haklısınız. D, formülle A,B,C'den çıkar; 0,02 fark ölçüm hatası içinde kalır ve pivot ayarını ayırt etmez. Ayırt edici olan A,B,C'nin bulunması. Düzeltme: kontrol "A,B,C bulundu mu (tarih ±2 gün, fiyat ±%1)" olsun; D yalnız formül sağlaması.

**05-021** — OLGU — "(X?)" yalnız 7,20'nin aracın X etiketi olup olmadığını sorar, rolünü değil. Kontrol ettim: 8,22+(10,25−7,20)=11,27, etiket 11,29; ikinci kalıp 8,42+(9,86−8,22)=10,06, etiket 10,05. Uyuşma D'ye değil A,B,C okumasına dayanıyor; zayıf kanıt, çöpe atılacak değil.

**05-022** — EKSİK — Kaynakta işaretler fitil uçlarında: SMRTG'de C=15,2 (fitil) ve getiri bu değerle uyuşuyor (B1). Düzeltme: pivot yüksek/düşük (fitil) üzerinden; kapanış bazlı varyant ayrı deneme.

**05-023** — EKSİK — Zikzak eşiği kaynakta yok (§1). Hesap yok. Düzeltme: sadakat sonrası her işlemde "teyit gecikmesi (gün) ve teyit günü fiyatın C'den uzaklığı (%)" kaydedilir, dağılımı raporlanır.

**05-024** — OLGU — Kaynak yok. "Backtest Modu" için tek bilgi bizim YORUM (§2): eski C'ye dönüp sonrasını izler. Look-ahead riski notta var (§5 "bilinmiyor"). Bizim motor teyit gününde bilinen pivotu kullanır; Tansu'nun ekranı için doğrulanamaz.

**05-025** — EKSİK — Pivot tanımı gereği R pencerede C'nin altına inilirse bu C pivot olmaz. Tasarım bunu yazmıyor. Düzeltme: tek cümle: "R pencerede C'nin altına inilirse C pivot sayılmaz; yeni aday ileriye bakılmadan seçilir".

**05-026** — EKSİK — Kalan mesafe için sınır yok. Düzeltme: sinyal şartı "giriş AOF < D"; her işlemde (D−giriş)/(D−C) kaydedilip raporlanır. Eşik koyma (YORUM; sonuçtan önce yazılmadıkça yasak).

**05-027** — EKSİK — Düzeltme: sinyal gününe (teyit günü) kadar gün yüksek ≥ D olduysa kalıp TAMAMLANDI sayılır; işlem ve kart yok. Giriş günü için bkz. 05-039.

**05-028** — EKSİK — Premise kısmen yanlış: 5.3 test listesinde "bozulma çıkışı" var (açık pozisyon için). Eksik olan giriş öncesi ölüm: teyit gününe kadar A ihlal edildiyse giriş yok. Düzeltme: sinyal şartına "C'den teyit gününe A ihlali yok" ekle; teste "giriş öncesi bozulma" ekle.

**05-029** — EKSİK — 5.1 satır 111 ile 115 aynı cümlede ayrışıyor. Düzeltme: A,B,C,D, stop ve giriş tek seride, düzeltilmiş (HGDG); ham yalnız tavan/taban ve likidite.

**05-030** — OLGU — Premise yanlış: düzeltme toplamsal değil, çarpandır (`SHHE_FIYAT_AYAR_OR`; THYAO HGDG/HG sabit 0,9769; veri-kaynaklari.md, kendim koşmadım). Çarpan, olay öncesi iki fiyatın oranını (q, r) değiştirmez. Yalnız A..C arasında olay varsa oran değişir ve bu gerçek getiridir.

**05-031** — EKSİK — Düzeltilmiş seride sıçrama olmaz. Düzeltme: stop A düzeltilmiş seviyedir; sonraki olayda çarpanla yeniden ölçeklenir; bugünkü fiyatla aynı seride kıyaslanır (05-029).

**05-032** — EKSİK — 5.1 yalnız "sınamadan çıkar" der. Düzeltme: karantina penceresi A,B veya C'ye denk gelirse kalıp aday olmaz; açık pozisyonda "VERİ_HATASI" işaretlenir, işlem sonuçtan çıkar ve sayısı raporda yazılır.

**05-033** — EKSİK — Giriş sınırı yok. Düzeltme: 05-026 şartı (giriş < D) ve (giriş−A) risk kaydı; ek eşik koyma.

**05-034** — CEVAPLI — Karar, sinyal günü kapanışında verilir; AOF yalnız dolum varsayımıdır (gün boyu ortalama emir). Look-ahead değil, iyimser dolum varsayımı. TASARIM 5.3 (S2-7) ve 5.4 (%0,1/0,3/0,5 duyarlılık) karşılıyor.

**05-035** — CEVAPLI — AOF matematiksel olarak [düşük, yüksek] içindedir. Likidite: pozisyon ≤ son 10 gün medyan TL işlem tutarının %2'si (5.4 M11); evren BIST100 (BIST100 dışı premise'i geçerli değil); masraf duyarlılığı %0,5.

**05-036** — EKSİK — K1'de AB=CD için A (stop) ve D yok; rastgele giriş neye göre boyutlanır ve çıkar? Düzeltme: rastgele giriş, gerçek işlemin (giriş−A)/giriş ve (D−giriş)/giriş yüzdelerini taşır; aynı Adım fonksiyonu.

**05-037** — CEVAPLI — 5.5 açık: "AB=CD stopu A seviyesidir, 2 ATR değil". 5.3'ün genel cümlesi bunu belirtmiyor. Düzeltme: 5.3'e "(AB=CD hariç: A ve D mutlak seviye)" ekle. Kod 5.5'i uygular.

**05-038** — CEVAPLI — 5.3: "Giriş günü de stop ve hedef kontrol edilir" ve "aynı gün hem stop hem hedef: stop önce". Giriş AOF'ta, gün düşüğü ≤ A ise stop aynı gün tetiklenir (kötümser).

**05-039** — EKSİK — 5.3, giriş günü hedef kontrolünü de içeriyor; sıra bilinmediği için iyimser. Düzeltme (YORUM): hedef kontrolü giriş gününden sonraki günden başlar; stop kontrolü giriş gününden başlar.

**05-040** — EKSİK — Hedef dolumu yazılı değil. Düzeltme (YORUM, stop kuralının aynası): gün yüksek ≥ D + 1 fiyat adımı ise D'den; AOF > D ise AOF'tan (geçiş şartı, dokunuş değil).

**05-041** — ZAYIF SORU — DOAS bir Kelebek'tir (§8), AB=CD değil. D'nin 159,49'dan aşağıda (159,40) olması hedefin aşıldığını gösterir; dokunuş toleransı kanıtı değil.

**05-042** — EKSİK — 05-040 düzeltmesi yeter: gap'te AOF ≥ D ise AOF'tan, değilse D'den çıkış. Kilitli tavanda satış emri karşılanır; kural gerekmez.

**05-043** — EKSİK — Fiyat adımı kuralı tasarımda yok. Benim bilgim (doğrulamadım, ağ kullanmadım): <20 TL 0,01; 20–50 0,02; 50–100 0,05; 100–250 0,10; 250–500 0,25; 500–1000 0,50. Düzeltme: D yukarı yuvarlanır (daha zor dolum, kötümser); fiyat adımı tablosu Takvim/Veri modülüne girer. Tablo ayrıca doğrulanmalı.

**05-044** — EKSİK — Düzeltme: giriş yalnız ertesi gün denenir; tavan kilidiyse sinyal düşer ("giriş_yapılamadı" olarak sayılır ve raporlanır). Sonraki gün deneme yok (look-ahead ve R:R değişimi önlenir).

**05-045** — EKSİK — "Ertesi gün" Takvim modülünden gelir (TASARIM 4) ama tanım yazılı değil. Düzeltme: ertesi gün = o hissede hacim > 0 olan sonraki işlem günü; yarım gün normal sayılır.

**05-046** — EKSİK — Bozulma bazı kaynakta yok (§3). 5.3 stop dolumunu fitille tanımlıyor. Düzeltme: stop A seviyesidir; tetik gün düşüğü ≤ A; A düzeltilmiş seride olduğundan fiyat adımına yuvarlanmaz.

**05-047** — ZAYIF SORU — Stop avı spekülatif; kaynak yok. Etkisi 05-048'deki kötümser dolum duyarlılığında görünür.

**05-048** — EKSİK — Stop dolumu A'dan varsayılıyor. Düzeltme (YORUM): ana koşuda stop dolumu A−1 fiyat adımı (kötümser); A'dan dolum duyarlılık satırında.

**05-049** — OLGU — Doğrulanmadı. B3'e göre #1'de A stopu −%10 verirdi, tablo −%23,29. Diğer stop zararlarının (−%12,10, −%24,85) kuralını kalıplarını okuyamadığım için çözemedim. Kural bilinmiyor.

**05-050** — YANLIŞ — S2-34 "yapısal stopla uyumlu" der. B3 bunu zayıflatıyor: #1 için A stopu zararı üretmiyor. Geniş zarar her geniş stopla uyumlu; kanıt değil. Düzeltme: TASARIM 5.5 ve KURALLAR §3'te "uyumlu" cümlesini sil; "Tansu'nun stopu bilinmiyor; A = YORUM, deneme sayılır" yaz.

**05-051** — EKSİK — Minimum stop mesafesi yok. KRPLS #2: (C−A)=0,20 TL, %2,4 (ölçüm). Düzeltme (YORUM): giriş−A < 1 ATR(14) ise işlem yok; ızgarada 0/1/2 ATR denenir, deneme sayılır.

**05-052** — EKSİK — Ağırlık = %1 × giriş/(giriş−A). Stop mesafesi ≤ %10 olunca %10 tavan bağlar. KRPLS #1: mesafe %12,4 → ağırlık %8 (bağlamaz); KRPLS #2: %2,4 → %41, tavana takılır. Hesaplanmadı. Düzeltme: rapora "tavan bağlayıcı olan işlem oranı" ekle.

**05-053** — EKSİK — Çatışma gerçek: KURALLAR §3 risk paketi "SMA250 altı çıkış (bütün aileler)", S2-36 çıkış dayanağı olarak SMA250'yi sayıyor, ama derin dip girişi SMA250 altındadır (SMRTG düşen trend). Kaynak çözmez (infografik NotebookLM). Düzeltme (YORUM, Levent kararı): AB=CD'de SMA250 çıkışı uygulanmaz; S2-36 cümlesini düzelt.

**05-054** — EKSİK — Düzeltme: 250 işlem günü geçmişi olmayan hissede o gün sinyal yok (SMA250 ve ATR14 hesaplanamaz).

**05-055** — CEVAPLI — AB=CD'de ATR rolü yok; ATR 14 diğer aileler içindir (5.5, GLOSSARY "Stop"). 05-051'deki düzeltme eklenirse tek rolü o olur.

**05-056** — EKSİK — A pivotu teyitli ve sabittir; pozisyon girişinde stop ve hedef sabitlenir (5.3 "giriş fiyatından hesaplanır"). Düzeltme: "A,B,C tarihleri ve D, giriş günü kilitlenir" yaz.

**05-057** — ZAYIF SORU — Tansu tablosunda sermaye sıralı zincirli: 344.293,73×1,2614=434.282 (#8). Yani #7 #8'den önce kapanmış; çakışma yok. Aynı kural zaten çakışmayı önler.

**05-058** — EKSİK — Süre sınırı yok (S2-36). Düzeltme: rapora "dolu slot günü ve reddedilen sinyal sayısı" ekle. SMRTG'deki "2 açık" muhtemelen son iki kalıp; sabit kilitlenme kanıtı değil.

**05-059** — EKSİK — Tansu'da açıklar toplama dahil değil: 10 kapalı işlemin bileşiği ≈405.385 TL, bitiş 405.327 TL (doğrulandı). Tasarımda yok. Düzeltme: dönem sonu kapanışıyla mark-to-market; "yalnız kapalı" ve "kapalı+açık" iki satır.

**05-060** — OLGU — Evet r etiketi kalıba bağlı. Ölçüm: SMRTG #2 ve #3'te r≈1,0 (CD 7,76/AB 7,7 ve 5,43/5,5). 1,27 etiketleri (KRPLS dışı AKCNS, 32, 45, 47) ayrı kalıplara ait.

**05-061** — OLGU — Önceden: RYSAS "taze D / ALIM SİNYALİ" etiketi D oluşmadan r=1,27 taşıyor; DGATE [AKTİF] D etiketli. r projeksiyon etiketidir, sonradan ölçülen değil.

**05-062** — OLGU — Kısmen doğrulandı: SMRTG #2 ve #3 r≈1,0 (ölçüm). #4, #5 için A,B'yi güvenle okuyamadım. ISKPL'de grafik yok; r bilinmiyor. Getiriler (C−D)/C ile tutarlı (B1).

**05-063** — CEVAPLI — S2-45: her (aile, varyant, parametre) bir deneme. Holm bağımlılık varsaymaz; bağımlılıkta muhafazakâr olur (gevşek olmaz).

**05-064** — YANLIŞ — KURALLAR §1 satır 29 merdiveni "AB=CD + hedef merdiveni" altında C→D bacağıyla birleştirmiş. Merdiven D'den sonraki harekete (RYSAS, D'de alış) ait; bizim yukarı kalıpta A, D'nin altındadır, yani D sonrası ters harekettir. Düzeltme: satırı ikiye ayır; merdiven C→D ailesinden çıkarılsın.

**05-065** — ZAYIF SORU — Formül yön-bağımsızdır; yukarı D'de A'ya doğru hedefler aşağıdır (D sonrası ters hareket). İşaret sorunu yok. Tasarım merdiveni kullanmıyor.

**05-066** — OLGU — Evet (§4: iki denklem D≈20,0; A=24,20 > D). Üstelik MARKA ve SMRTG #2–#5 de aşağı kalıp (B1). Yani "ikinci" değil, birkaç kanıt var.

**05-067** — EKSİK — Gerekçe yok: S2-32 yalnız kararı yazıyor. Muhtemel neden BIST'te açığa satış (YORUM; kaynak yok). Düzeltme: aşağı kalıp "dışarıda bırakılan Tansu işlemi" olarak raporda sayılsın.

**05-068** — EKSİK — Birleşik filtre kodlanamaz (§13, §14: delta eşiği ve verisi yok; talep bölgesi tanımı yok). Düzeltme: BALAT'ı negatif örnek olarak sakla; filtre kaynak çıkana kadar kurala girmez.

**05-069** — EKSİK — TASARIM 2 tablosu AB=CD için teyit iddia ediyor ama KURALLAR §3.2'de yalnız geometri ve pivot teyidi var. Düzeltme: tabloya "AB=CD: teyit = pivotun sağ teyidi; ek filtre yok" yaz.

**05-070** — CEVAPLI — Yer = C pivotu (A,B,C yapısı); teyit = pivotun R gün sağ teyidi (KURALLAR §3.2, 5.5: "C teyit edilince girilir"). Çelişki yok, teyit zayıf.

**05-071** — EKSİK — Kaynak: tarayıcı ardışık üç zikzak köşesini kaydırıyor (§1 madde 3, ölçüm). Düzeltme: C, teyit edilen en son pivot; B ondan önceki, A ondan önceki karşıt pivot. Bir C için tek üçlü.

**05-072** — EKSİK — 05-071 kuralıyla bir hisse+gün için tek kalıp çıkar. Düzeltme: o kurala "tek C = o gün teyit edilen pivot" ekle.

**05-073** — EKSİK — 05-014 düzeltmesi tek ölçek seçer; iç içe sinyal olmaz. İkinci ölçek yalnız 5.10 ızgarasında varyant.

**05-074** — CEVAPLI — 5.3: açık pozisyonda gelen yeni sinyal sayıma girmez; hedef giriş gününde kilitli (05-056).

**05-075** — EKSİK — Aynı eşleştirme sorunu 05-036'da: rastgele girişe gerçek işlemin stop ve hedef yüzdelerini ver; süre doğal çıkar.

**05-076** — EKSİK — K1 ön şartı AB=CD için tanımsız. Düzeltme (YORUM): ön şart günü = "o hissede bir dip pivotu teyit edilen gün (A,B koşulu aranmadan)". Böylece yalnız geometrinin katkısı ölçülür.

**05-077** — ZAYIF SORU — Sadakat kontrolü (KURALLAR §4) yalnız D değerlerine bakar; sıralama kuralı girmez. Sıra sapması işlem sayısı karşılaştırmasında önemli olur, o da §4'te yok.

**05-078** — EKSİK — Bozulma bazı kaynakta yok. Düzeltme: BOZULDU = A fitil ihlali = stop çıkışı; kapanışta ayrı ilan yok. Giriş öncesi ihlalde kart yok (05-028).

**05-079** — EKSİK — Düzeltme: raporda "stop+bozulan" tek sayı (Tansu'nun tek sütunu); kartta iki etiket olabilir, çıkış fiyatı tek (05-078).

**05-080** — EKSİK — Belirsizlik yok ama yazılı değil. Yön-bağımsız invariant (tweet-abcd-geometrik…): (fiyat−A)·işaret(B−A) < 0 → bozulma. A dip için A'nın altı. Düzeltme: bu formülü KURALLAR §3.2'ye ekle.

**05-081** — EKSİK — Gerekçe tasarımda yok; BIST açığa satış sınırı YORUM (kaynak yok). Aşağı kalıplar Tansu'nun kanıtının büyük kısmı (B1). Düzeltme: TASARIM 3'e gerekçe ve "dışarıda kalan Tansu işlemleri" sayısı yaz.

**05-082** — CEVAPLI — Piyasa etiketi kapı değil ama sonuçlar etikete göre ayrı raporlanır (TASARIM 4); kabul 5.12.4 (yılların %60'ı, en iyi %5 atılınca pozitif) düşen yılları kapsar.

**05-083** — EKSİK — Aynı sorun: 05-076 düzeltmesi pivot koşulunu taşır.

**05-084** — EKSİK — 05-076 düzeltmesi (pivot teyit günü) R-gün yükselişi otomatik taşır. Kontrol: motor testinde K1 günleri aynı pivot fonksiyonundan alınır.

**05-085** — CEVAPLI — Kabul ölçütleri K1 ve K2'yi portföy seviyesinde günlük getiriyle kullanır (5.7, 5.12.1–2); işlem seviyesi tutma-süresi yanlılığı kabul kararına girmez.

**05-086** — CEVAPLI — 05-085 ile aynı.

**05-087** — CEVAPLI — KURALLAR §4: Tansu'nun rakamları "performans değil, kuralın doğru okunduğunun kanıtı"; AB=CD satırı yalnız D değerleri. 7/10 ölçüt değildir.

**05-088** — OLGU — Doğruladım: 2026-08-27 − 1000 gün = 2023-12-01; SMRTG grafiği ~Kasım sonu 2023'te başlıyor (ölçüm). "1000 günlük" = takvim günü; işlem günü olsaydı başlangıç 2022 ortası olurdu. İlk kalıpların 2024'te çıkması ısınma. Düzeltme: sadakat taramasında pencere = bitiş − 1000 takvim günü.

**05-089** — EKSİK — Sermaye eğrisi karşılaştırılmaz. Düzeltme: sadakat için 15 işlemin C tarihi ve (C−D)/C yüzdesi karşılaştırılır; sermaye bileşiği yok.

**05-090** — CEVAPLI — KURALLAR §4 ve TASARIM 1: sadakat performans kanıtı değil; §5 seçilmiş örnek riskini yazıyor. İki hisse olasılık kanıtı sayılmıyor.

**05-091** — OLGU — Doğrulanamadı; kaynak yok. Ölçüm: SMRTG'de 2,4 TL'lik zikzak bacağı var (9,6→12,0), yani 3,02 TL mutlak zikzak eşiği olamaz. "Bilinmeyen" kalması doğru.

**05-092** — ZAYIF SORU — Hedef mesafesi q'dan bağımsız (D−C = r·AB; q=0,88 için de AB). Dar işlem küçük AB'den gelir; bu 05-051 ve 05-009'daki durumdur. %0,3 masraf zaten her yönde düşülüyor.

**05-093** — CEVAPLI — TASARIM 2 ve P5: "Tansu'dan esinlenen bizim yorumumuz" açık yazılı; KURALLAR §4 sadakat kontrolü kısmen bağlıyor.

**05-094** — EKSİK — r için tolerans gerekmez (D projeksiyon, 05-095). q için eşik sert: q ≤ 1 ve C > A (S2-33); q=1,02 ret. Düzeltme: KURALLAR §3.2'ye bir satır.

**05-095** — EKSİK — Evet, tasarımda q ≤ 1 olan her ABC sinyal. Tansu'nun tarayıcı filtresi bilinmiyor (q aday oranları ikinci el, ölçülen q'lar 0,67–0,88). Düzeltme: raporda q dilimi (05-008); "Tansu'nun AB=CD'si" iddiası yapma.

**05-096** — EKSİK — Hücreler bağımsız sayılamaz. Düzeltme: raporda "pozitif hücre oranı olasılık değildir" ve hücreler arası işlem örtüşme oranı yazılsın.

**05-097** — ZAYIF SORU — Tansu hızı (SMRTG 12, ISKPL 5 kalıp/≈2,7 yıl) 100 hisseye ölçeklenince yılda yaklaşık 70–160 kalıp çıkar (kaba, doğrulanmadı); 30 kapanmış işlem yıl içinde dolar. Yine de maksimum süre yazılı değil.

**05-098** — EKSİK — R gecikmesi sınamada modellenir (pivot_known_at = i+R); veri gecikmesi sınamada yok. Düzeltme: canlıda kaçan sinyal sayısı raporlanır; sınamada 0 varsayıldığı yazılır.

**05-099** — EKSİK — Giriş bilinmez. Düzeltme: kart "referans fiyat = sinyal günü kapanışı", stop A, hedef D, adet = %1 risk/(kapanış−A) gösterir; gerçek giriş gün sonunda yeniden hesaplanır. Kanıt satırı ailenin geneline aittir, tek işleme değil; geçerli kalır.

**05-100** — YANLIŞ — KURALLAR §2 satır 29 "H" (az YORUM) der; §3 eksik sütunu üç şey sayar, C-harmonik §21 beş sayar, ben üç tane daha buldum (yön, giriş fiyatı, stop kuralı B3). Düzeltme: AB=CD'yi "H" yerine "K" yap; "geometri ve D formülü birinci el, kural (yön, giriş, stop, pivot) bizim icadımız" yaz.

## Özet

Sayılar (toplam 100): EKSİK 56, CEVAPLI 15, OLGU 14, ZAYIF SORU 10, YANLIŞ 5.

En önemli 10 değişiklik:

1. 05-001, 05-005, 05-006, 05-012, 05-066, 05-081: Tansu'nun SMRTG getirileri C fiyatından, D<C (aşağı kalıp). TASARIM 5.5 ve S2-32 yönü kanıtsız seçmiş. Değişiklik: yönü YORUM yaz; sadakat kontrolünü yönsüz koş; "Tansu modu" (giriş C fiyatı) ayrı satır; aşağı kalıp sayısını "dışarıda kalan" diye raporla.
2. 05-049, 05-050: S2-34 "A stopuyla uyumlu" iddiası ölçümle desteklenmiyor (#1: A stopu −%10, Tansu −%23,29). Değişiklik: cümleyi sil; stop A = YORUM, deneme.
3. 05-100: KURALLAR §2'de AB=CD "H" yanlış. Değişiklik: "K" yap.
4. 05-018, 05-019, 05-020: Sadakat kontrolü 3 D değeriyle zayıf ve geçme ölçütü yok. Değişiklik: SMRTG/ISKPL 15 C tarihini ve SMRTG D etiketlerini ekle; ölçütü koşudan önce yaz.
5. 05-053: SMA250 çıkışı AB=CD derin dip girişiyle çatışıyor. Değişiklik: AB=CD için istisna (Levent kararı); S2-36'yı düzelt.
6. 05-027, 05-039, 05-040, 05-033: Girişte D'ye çoktan ulaşılma ve hedef dolumu tanımsız. Değişiklik: giriş AOF < D şartı; hedef dolumu yüksek ≥ D+1 adım; giriş gününde hedef kontrolü yok.
7. 05-036, 05-075, 05-076, 05-083, 05-084: K1 AB=CD için tanımsız. Değişiklik: ön şart = dip pivotu teyit günü; rastgele girişe gerçek stop/hedef yüzdeleri.
8. 05-051, 05-052: Minimum stop mesafesi ve %10 tavan ilişkisi yok. Değişiklik: giriş−A < 1 ATR ise işlem yok (YORUM, ızgarada); rapora tavan bağlama oranı.
9. 05-029, 05-031, 05-014, 05-022: Seri (ham/düzeltilmiş), ölçek ve fitil kararı yok. Değişiklik: tek düzeltilmiş seri; zikzak ölçeği; fitil pivotu; hepsi sadakat öncesi yazılı.
10. 05-059, 05-064, 05-069: Açık işlem raporlaması, merdiven satırının yanlış gruplanması, AB=CD teyit iddiası. Değişiklik: açıkları mark-to-market ayrı satır; KURALLAR §1 satırını ikiye böl; TASARIM 2 tablosuna "teyit = pivot sağ teyidi" yaz.
