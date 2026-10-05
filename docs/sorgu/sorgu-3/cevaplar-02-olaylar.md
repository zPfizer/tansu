# Cevaplar 02: Şirket olayları

Yöntem: İş Yatırım `HisseTekil` ve `GetSermayeArttirimlari` (THYAO, CCOLA, HEKTS, ASYAB, ECILC, RYSAS) canlı çekildi; tasarım belgeleri okundu. Kod okunmadı (ön deneme, bağlayıcı değil).
Kısaltmalar: "ayar" = `SHHE_FIYAT_AYAR_OR`; "oran" = `HGDG_KAPANIS / HG_KAPANIS`. Önerilen ortak çözüm "ÇÖZÜM-A" (Özet 1'de): iki katmanlı kendi serimiz.

**02-001** — OLGU — Önerme yanlış: kod 04 çarpanı temettüyü taşıyor. CCOLA'nın 13 nakit temettü kaydında ayar = 1 − brüt_temettü / önceki_ham_kapanış (13/13 birebir, ör. 2018: 1−0,787/37,00=0,97873). THYAO 2025'te 2 kayıt (0,98695 ve 0,98980). Çarpımla yeniden kurulan oran CCOLA'da HGDG'ye en çok 2,3e-5 yaklaşıyor. Fark üretmez.

**02-002** — EKSİK — Tam bağımsız değil: oran adımları tablo tarihleriyle örtüşüyor (CCOLA 14/14), yani aynı kaynak. Yine de HEKTS 2015'te HGDG adımı tablodan 1 gün sonra (aşağıda 02-005); demek HGDG tabloyu birebir kopyalamıyor, kısmen bağımsız. Tablodaki yanlış çarpanı karşılaştırma yakalamaz. Düzeltme: her olay için tablodan bağımsız iç tutarlılık sına: kod 04'te `1 − NAKIT_TM_ORAN/100 / önceki_ham_kapanış` ≈ ayar; kod 01/02/03'te `(P + bedelli_oran/100·1)/(1+bedelli+bedelsiz)/P` ≈ ayar (formül 02-004'te doğrulandı); ham olay günü getirisi ≈ ayar−1.

**02-003** — EKSİK — Tanımlı değil. Veri: oran, `SHHE_TARIH` günü dahil sonraki günlerde olay çarpanını taşımıyor; çarpan yalnız tarih < `SHHE_TARIH` günlere uygulanıyor (CCOLA 14/14, THYAO 2/2, HEKTS 7/8). Aynı gün kayıt örneği örneklemde yoktu. Düzeltme: TASARIM 5.1'e "çarpan tarih < SHHE_TARIH satırlara uygulanır; olay günü düzeltilmez; aynı güne düşen kayıtlar çarpılır (çarpma değişmeli, sıra önemsiz)".

**02-004** — OLGU — Doğrulandı. Resmî BIST baz fiyatı doğrulanmadı, ama formül birebir yeniden üretildi: HEKTS 2021 için (29,96 + 1,7577·1) / (1+1,7577+1,0213) / 29,96 = 0,28014 (tablo 0,28014). HEKTS 2019 bedelli için (16,63+2)/3/16,63 = 0,37342 (tablo 0,37342). 0,2646 "bedelli bedeli ödenmeyen" yanlış formüldü. Çarpan = teorik baz fiyat / önceki ham kapanış, 1 TL nominal bedelli bedeliyle.

**02-005** — OLGU — Kısmen kapandı: `SHHE_TARIH` ex-date. Kanıt: çarpan taban fiyatı "tarihten önceki gün kapanışı" (CCOLA 14/14, HEKTS 2016/2017/2019/2021/2022/2024) ve ham düşüş o günde. Tek aykırı kayıt HEKTS 2015-11-26: ham düşüş (2,94→2,67) ve HGDG adımı 2015-11-27'de; kayıt tarihi bir gün erken (son hak günü). Düzeltme: 8.2'yi kapat: "ex-date; olay doğrulamada ±1 işlem günü tolerans; çarpan HGDG adım gününe değil tabloya göre, ama ham düşüş günü ±1'de aranır".

**02-006** — ZAYIF SORU — Ödeme günü hipotezi veriyle reddedildi (02-005); sapma haftalar değil en fazla 1 gün (1/8 kayıt).

**02-007** — OLGU — HGDG brüt temettüyü işliyor (13/13 CCOLA'da ayar brüt oranla; net alanıyla tutmuyor: ör. 2019 brüt 0,95743, net 0,96382). Net alan `SHHE_NAKIT_TM_ORAN_NET` var (=brüt·0,85). Şişirme yaklaşık %15 × temettü verimi (THYAO 2025: ~%2,3'ün %15'i ≈ %0,35; CCOLA yılda %1–4'ün %15'i). %0,5 masraf işlem başına bir kez; uzun tutma ve yüksek verimde kapatmaz, kural ile K2'de aynı etki olduğu için fazla getiriyi büyük bozmaz. Düzeltme: temettüyü net alanla modelle (8.6 doğrulanana kadar %15 varsayımı yaz).

**02-008** — EKSİK — Borsapy temettüsüz: HGDG ile değil, kendi "yalnız bölünme/bedelli çarpanlı" serimizle (kod 01/02/03/09) karşılaştırılmalı; HGDG ile karşılaştırma ayrı ve ham/tablo ile. Düzeltme: 5.1'e iki karşılaştırma yaz: (a) borsapy ≈ P_bölünme (eşik %0,5), (b) HGDG ≈ P_bölünme × temettü çarpanları (eşik 1e-3).

**02-009** — EKSİK — Yazılı değil. Düzeltme: kazanan = ham veri + tablo çarpanı. Fark sınıfları: (1) olay gününden ±1 gün kayma → tarihi ham düşüşe hizala, listele; (2) olay yok ama sıçrama → karantina; (3) olay var ama ham getiri ≠ ayar−1 (limit dışı) → olay penceresi karantina. "Fiyat yamanmaz" = ham seriyi elle değiştirmeyiz; çarpan tablodan gelir.

**02-010** — YANLIŞ — S2-13 ("HGDG'den") ile TASARIM 5.1 (kendi çarpanımız, HGDG yalnız karşılaştırma) çelişiyor. HGDG ayrıca 4 ondalığa yuvarlı (02-012). Düzeltme: göstergeler kendi serimizde (ÇÖZÜM-A); HGDG yalnız kontrol; S2-13'ü bu yönde güncelle.

**02-011** — OLGU — Doğrulandı: THYAO tablosunda 2015 sonrası yalnız 2 nakit temettü kaydı var (2025-06-16, 2025-09-02); 0,98695×0,98980 = 0,97688 = HGDG/HG sabiti 0,9769. HGDG oran adımları tam bu iki günde (1,0132, 1,0103). Temettü içerme yalnız CCOLA'ya dayanmıyor: CCOLA 13, HEKTS 5 kayıt da çarpana uyuyor (HEKTS 2015 tarih kayması hariç).

**02-012** — OLGU — Doğrulandı: HGDG_KAPANIS 4 ondalık (HEKTS 2015-11: 0,0309; 2019-10: 0,2006). Oran sapması 2015'te ±%0,15, 2018'de ±%0,05, 2021 sonrası <%0,005. ASYAB'da (ham 0,87 TL) tek günde %1,8 oran sapması. Yani eski düşük fiyatlı serilerde HGDG getirisi ~%0,2 gürültülü. Düzeltme: getiri ve ATR'yi ham seriden kendi çarpanımızla (float) üret; HGDG'yi yalnız kontrol et.

**02-013** — OLGU — Çarpan tick'e yuvarlanmamış, teorik fiyattan: bedelsiz CCOLA 1/11=0,090909 (tablo 0,0909090914); bedelli HEKTS 2019 teorik 6,21 → 0,373421 tablo ile aynı. Gerçekleşen açılış baz fiyatı farkı HGDG'nin olay günü getirisinde kalıyor: HEKTS +1,6 %, −2,3 %, +5,6 %, −4,2 %; CCOLA bedelsiz +0,31 %. Sistematik tick birikmesi yok (çarpan zinciri teorik, tek günlük sapma bir kez).

**02-014** — EKSİK — Kod 03/09: bedelsiz (`BDSZ_IK`, `BDSZ_TM`) ve bedelli aynı satırda, tek çarpan. Nakit temettü yalnız kod 04'te `NAKIT_TM_ORAN` (THYAO 2009 kod 09: BDSZ_IK 313, BDSZ_TM 86, nakit 0). Düzeltme: temettü payı = yalnız kod 04 nakit akışı; bedelsiz/bedelli getiri değil, ölçek olayı (getiri sıfır, çarpan ile).

**02-015** — OLGU — Kısmen doğrulandı: `endeksKodu` "09" ile "" aynı sonucu verdi (ASYAB her ikisinde 0 kayıt); THYAO kayıtlarında `BHG_GRUP_KODU:'09'` alanı var, yani filtre etkisiz görünüyor. Kapanmış hissenin bilinen olayı olan örnek bulunamadı, bu yüzden "kapanmışların olayı dönüyor" doğrulanamadı. ASYAB'da HGDG/HG oranı sabit (2016-01-22 yuvarlama hariç) → olay yok ile tutarlı.

**02-016** — EKSİK — ASYAB (kapanmış): 200 OK + boş liste; "olay yok" ile "çağrı başarısız" ayırt edilemiyor. Çerez gerekmedi (çerezsiz THYAO çağrısı 200 verdi). Düzeltme: boş tablo kabulü için HisseTekil'den oran (HGDG/HG) sabit olmalı; oran adımı varsa ve tablo boşsa hata ver (ayrıca HTTP 200 dışı, JSON ayrıştırma hatası = hata).

**02-017** — OLGU — `"yil":0,"zaman":"HEPSI"` tek yanıtta tüm yılları getirdi (THYAO 1998'den 12 kayıt; CCOLA/HEKTS 2015 sonrası 14/8 kayıt; hisse başına birkaç kayıt, 2000 sınırı sorun değil). ~27 isteği 1 sn aralıkla yaptım, engel gelmedi. 500 hisse × 11 yıl toplu çekim sınanmadı; engel olursa 02-016 gibi boş/hata olur, aynı kapıya bağla.

**02-018** — OLGU — ASYAB: 395 satır, son gün 2016-07-25; son günlerde HG_HACIM=0, kapanış sabit 0,87 (sıçrama yok, bayat fiyat). Tablo boş. Düzeltme: HACIM=0 satırları işlem günü sayma (ATR, getiri, evren); kapanış sıçraması örneği bu hissede yok (iflas/zorunlu alım sıçraması doğrulanamadı).

**02-019** — OLGU — Yalnız AYGAZ 2022 (ayar 1,0, ham kesintisiz 45,78→43,96) doğrulandı; diğer kod 78 kayıtları sınanmadı. Düzeltme: ayar≠1 olan her 78 kaydı olay günü tutarlılık kontrolünden geçer (02-002 düzeltmesi), 1,0 olması güven değil kontrol konusu.

**02-020** — EKSİK — Bilinmeyen kodlar olay günü "açıklanmış" istisnası almamalı. Düzeltme: istisna yalnız |ham getiri − (ayar−1)| ≤ tolerans iken geçerli; bilinmeyen kod ve ayar=1 ise olay sayılmaz, sıçrama karantinaya girer.

**02-021** — OLGU — Doğrulanamadı: örneklemde ters bölünme/ayar>1 kaydı yok; birleşme/spin-off kodu bilinmiyor (veri-kaynaklari 8.3 açık). Düzeltme: evren kurulurken tüm tablolar taranıp ayar>1 ve bilinmeyen kodlar listelenir; ayar>1 için sentetik birim testi.

**02-022** — EKSİK — Tasarım sessiz. Düzeltme: v1'de sembol sürekliliği yok; iki sembol ayrı hisse sayılır, kopukluk karantina gibi işaretlenir (son satır sonrası boşluk) ve raporda "sembol değişikliği/birleşme kapsam dışı" yazılır.

**02-023** — EKSİK — Doğrulanmadı. Düzeltme: evren yalnız borsapy/KAP hisse listesinden gelir (hak sembolleri listede değil varsayımı kayda geç); ek olarak SERMAYE>0 ve PD>0 şartı.

**02-024** — EKSİK — Temettüde de güven sınırlı: 8 örneğin 7'si ex-date, 1'i bir gün erken (02-005). Düzeltme: karantina istisnası olay günü ±1 işlem günü ve ham düşüş eşleşmesine bağlansın.

**02-025** — OLGU — Ayrı kayıt: THYAO 2025-06-16 ve 2025-09-02 iki ayrı kod 04 kayıt (ikisi de oran 344,2); HGDG oranı iki adımda yükseliyor, çarpanlar zincirleniyor. Aynı gün çakışma örneği yok (bkz 02-003).

**02-026** — EKSİK — Anlık görüntü yalnız ham fiyat. Düzeltme: anlık görüntü = ham `HisseTekil` yanıtı (HG_ ve HGDG_ tüm alanlar) + `GetSermayeArttirimlari` ham JSON, tarihli, hash'li.

**02-027** — OLGU — Doğrulandı: tablo kaydında "eklenme/düzeltme tarihi" alanı yok (alanlar: `SHHE_TARIH`, `TARIH` fiyat anlık görüntüsü, `SHHE_ACIKLAMA`). Nokta-zamanlı yeniden üretim yalnız kendi anlık görüntülerimizle mümkün; geçmiş bilgi durumu yeniden kurulamaz. Düzeltme: günlük tablo anlık görüntüsü sakla (02-026), "sonradan eklenen kayıt" farkını fark günlüğüne yaz.

**02-028** — EKSİK — Pencere yok. Bakış sızıntısı riski gerçek (sıçrama öncesi sinyalleri silmek gelecekten seçim). Düzeltme: pencere = sıçrama günü → sıçrama + en uzun gösterge penceresi (250 gün); sıçramadan önceki sinyaller silinmez.

**02-029** — EKSİK — Düzeltme: açık pozisyon, sıçramadan önceki son temiz günün AOF'undan kapanır ve işlem sayıma girer; yeni giriş pencere boyunca yok.

**02-030** — EKSİK — Yazılı değil. Düzeltme: karantina hisse×gün maskesi olarak evrene uygulanır (kural, K1, K2 aynı maske); rapor karantina oranını ve karantinalı/karantinasız farkını yazar.

**02-031** — EKSİK — Limit kuralı küçük eksik olayı yakalamaz. Ama oran adımı yakalar: HGDG/HG oranı olay günlerinde tablo çarpanıyla örtüşüyor (3 hissede doğrulandı). Düzeltme: günlük oran adımı ≥ 5e-4 olan her günde tablo kaydı ara; yoksa uyarı. Bu %0,05 temettüyü bile yakalar.

**02-032** — EKSİK — TASARIM 5.1 ve veri-kaynaklari 7.2 çelişir; 7.2 eski öneri. Düzeltme: 7.2'yi "5.1 ve oran adımı kontrolü ile değiştirildi" diye işaretle; eksik olay denetimi oran adımına dayanır (02-031).

**02-033** — EKSİK — Olay gününde limit "o günkü baz fiyata göre". Düzeltme: olay gününde yargı getirisi = ham_kapanış/(önceki_ham_kapanış × ayar) − 1 (yani HGDG getirisi); bu |limit|+%0,5 aşarsa veya hak/bedelli günü ±%50 aşarsa karantina. Gözlem: HEKTS olay günü bu sapmaları ±%6 içinde.

**02-034** — YANLIŞ — Örnek yanlış. ECILC 12.03.2020 ham +%13,0 (11.03 +%19,8), RYSAS 12.03.2020 −%19,86; 12.03 ±%20 rejiminin son günü ve her ikisi limit içinde, tabloda olay yok (HGDG getirisi = ham getiri). 5.1 kuralıyla ikisi de karantinaya girmez. Düzeltme: örneği kaldır veya "13.03.2020'de ±%10'a geçiş, 12.03'te ±%20 geçerli" notuyla gerçek bir karantina örneği (olaysız >limit) bul.

**02-035** — EKSİK — 2015'te limit rakamı yok. Düzeltme: 02.01–27.11.2015 için ±%20 (muhafazakâr: yanlış karantina az) kullan, "doğrulanmadı" etiketle ve 2015 sonuçlarını ayrı raporla; ya da sınamayı 01.12.2015'te başlat.

**02-036** — CEVAPLI — veri-kaynaklari 5.5 ve 7.4: ±%10 ölçümle (2021–2026, 20 hisse, >%10,5 sıfır) destekli; pazar bazlı %15/%20 doğrulanmamış ve karantina eşiği ±%10 kabul. TASARIM 5.1 aynı. Not: evren büyük hisselerden oluştuğu için etki küçük.

**02-037** — EKSİK — Çok günlük boşluk kuralı yok. Düzeltme: izin verilen getiri = (1+limit)^k − 1; k = Takvim modülündeki işlem günü sayısı (iki satır arası); eksik satır ve HACIM=0 satırları da sayılır.

**02-038** — EKSİK — Düzeltme: ex-date gününde tavan/taban referansı = önceki ham kapanış × ayar (teorik baz fiyat), önceki ham kapanış değil.

**02-039** — EKSİK — Düzeltme: eşitlik yerine tolerans: `HG_MIN==HG_MAX` ve kapanış getirisi ≥ limit − 1 fiyat adımı; fiyat adımı tablosu (02-056) kullanılır.

**02-040** — ZAYIF SORU — Önerme yanlış: HACIM TL tutarı ve olay gününde ölçek sıçramıyor (02-097): CCOLA 808M → 361M (1000 % bedelsizde). "Hacim olağandışı" eşiği ayrıca tanımsız (EKSİK ama bu sorunun konusu değil).

**02-041** — EKSİK — Düzeltme (ÇÖZÜM-A): giriş fiyatı ham `HG_AOF`; motor içi seviyeler P_bölünme ölçeğinde `HG_AOF × k_t` (k_t = t'den sonra gelen tüm bölünme/bedelli çarpanlarının çarpımı). HGDG_AOF kullanılmaz.

**02-042** — EKSİK — Aynı ölçek garantisi yok. ÇÖZÜM-A'da ATR ve giriş aynı P_bölünme serisinden; t+1 ex-date ise giriş AOF'u zaten düzeltilmiş ölçekte, ATR de aynı ölçekte; sorun doğmaz. Birim testi ekle (02-092).

**02-043** — EKSİK — ÇÖZÜM-A: pozisyon P_bölünme ölçeğinde saklanır, olay gününde yeniden ölçeklemeye gerek kalmaz (seri geriye ölçeklenir). Canlı kartta ham seviyeler gösterilir ve Adım tablodaki çarpanla (k_t) dönüştürür; sınama ve canlı aynı Adım fonksiyonu.

**02-044** — EKSİK — Aynı çözüm: giriş ve çıkış aynı seriden alınır (P_bölünme + temettü nakit akışı); işlem getirisi = çıkış/giriş − 1 + temettü akışları.

**02-045** — EKSİK — Adet = risk_TL / (2·ATR_bölünme·k_t) giriş gününde ham ölçekte; %10 tavanı ve lot yuvarlama ham fiyat × lot ile kontrol edilir; sonra bedelsiz lotu çarpar (adet/ayar).

**02-046** — OLGU — S2-14 veriyle kapandı: HACIM TL tutarı. Kanıt: CCOLA 2024-08-09 HACIM 509,8 M, SERMAYE 254,4 M pay; lot olsa 509,8 M lot > toplam pay (imkânsız); ham ve düzeltilmiş eşit (HG_HACIM=HGDG_HACIM CCOLA ve HEKTS'te) ve olayda ölçek atlamıyor. Düzeltme: likidite = HG_HACIM'in medyanı, fiyatla çarpılmaz. Uyarı: THYAO 2015-01-02'de HG_HACIM 71,5 M ≠ HGDG_HACIM 112,1 M; HGDG_HACIM = DOLAR_HACIM×kur görünüyor; ham HG_HACIM kullan.

**02-047** — OLGU — Aynı: HACIM TL; çifte sayım riski gerçek (ham fiyatla çarpmak ~fiyat kadar şişirir), karışma yok çünkü HACIM olay gününde sıçramıyor. Evren HG_HACIM 60 gün medyanıyla kurulur.

**02-048** — OLGU — Doğrulandı: PD = SERMAYE × ham kapanış (CCOLA ve HEKTS'te oran 1,0000) ve SERMAYE ex-date günü güncelleniyor (CCOLA 254 M → 2.798 M 2024-08-13; HEKTS 227,6 M → 860 M 2021-04-30). Olay günü PD sıçramıyor (CCOLA +%0,3; HEKTS +%3,4 piyasa hareketi). Bedelli döneminde şişme yok. `HAO_PD` ise 2 gün geç güncelleniyor (CCOLA 15.08): kullanma.

**02-049** — EKSİK — Garanti yok. Düzeltme: ATR, SMA, pivot tek fonksiyonla tek seriden (P_bölünme) hesaplanır; yüksek, düşük ve önceki kapanış ayrı ayrı ölçeklenmez; birim testi: olay günü ATR ≈ olaysız ATR.

**02-050** — EKSİK — Stop kontrolü hangi seride yazılı değil. ÇÖZÜM-A: stop P_bölünme serisinde (temettü düşüşü gerçek kalır, aracı kurum ham fiyatla ne yapıyorsa o), temettü nakit akışı ayrı. HGDG'de stop kontrolü yapılmaz.

**02-051** — EKSİK — Aynı çözüm: canlı kart ve backtest aynı kuralı uygular çünkü ikisi de P_bölünme + ham seviye dönüşümü kullanır; yüksek verimli hissede temettü düşüşü stop mesafesine gerçekten girer (HEKTS 2015: %8).

**02-052** — EKSİK — ÇÖZÜM-A: A ve D, P_bölünme ölçeğinde saklanır; bedelsiz/bedelli olayı otomatik ölçeklenir; temettü yeniden ölçekleme yapmaz (düşüş gerçek, seviyeler aynı). Canlı kart seviyeleri ham ölçekte ex-date sabahı ayar ile çarpılır.

**02-053** — EKSİK — Evet, HGDG'de temettü orantıları ve farkları kaydırır (THYAO gibi %1–2, HEKTS 2015 %8). ÇÖZÜM-A'da geometri P_bölünme'de; temettü etkisi kalıp yok sayılma riski olarak raporda yazılır, sınama yok.

**02-054** — EKSİK — Kapanış ve SMA250 aynı seriden (P_bölünme) alınmalı. Karşılaştırmayı ham/düzeltilmiş karıştıran kural yazılı değil; ÇÖZÜM-A tek seri kuralını getirir.

**02-055** — EKSİK — Stop ve gün yüksek/düşüğü aynı ölçekte tutulur (ÇÖZÜM-A); ayrıca motor sınamasına "açık pozisyon + bedelsiz ex-date: stop tetiklenmez" eklenir (02-092).

**02-056** — EKSİK — Modelde fiyat adımı yok. Düzeltme (BISTECH adımı, belleğe dayalı, doğrulanmadı): <20 TL 0,01; 20–50 0,02; 50–100 0,05; 100–250 0,10; 250–500 0,25; 500–1000 0,50; ≥1000 1; ≥2500 2,5. Kart seviyeleri adıma yuvarlanır (stop aşağı); sınamada ATR < 3 adım olan hisse-gün sinyal üretmez; adım kuralı tarihsel değişmiş olabilir (YORUM).

**02-057** — EKSİK — Düzeltme: v1'de bedelsiz payların ex-date'te hesaba geçtiği varsayılır (adet/ayar); gecikme etkisi basitleştirme olarak yazılır, ex-date ±1 günde çıkış sayısı raporlanır.

**02-058** — EKSİK — Düzeltme: temettü/bedelsiz hakkı, pozisyonun ex-date gününe başlamadan (giriş AOF günü < ex-date) açık olmasına bağlı; ex-date veya sonrası girişte hak yok, fiyat zaten düşmüş. Kod: `giris_gunu < SHHE_TARIH`.

**02-059** — EKSİK — Düzeltme: bedelli hak kullanımı değer-nötr varsayılır (teorik çarpan, nakit modellenmez); varsayım raporda yazılır; K2 aynı varsayımı kullandığı için fark nötr. Duyarlılık: bedelli penceresi ±10 gün dışlanmış sonuç.

**02-060** — OLGU — Ölçülmüyor ama ölçülebilir ve ölçüldü: HEKTS'in 4 bedelli/bedelsiz olayında gerçekleşen − teorik sapma +%1,6, −%2,3, +%5,6, −%4,2 (HGDG olay günü getirisi); CCOLA bedelsiz +%0,31. Piyasa hareketinden ayrıştırılamıyor. Düzeltme: olay günü HGDG getirisi dağılımını rapora yaz.

**02-061** — ZAYIF SORU — Yeni pay alma hakkı ex-date'ten itibaren işlem görür; hisse o günden itibaren zaten hak ayrılmış fiyattadır (ham düşüş SHHE_TARIH günü, 02-005). Hak dönemi hisse fiyatında ayrı kirlilik yaratmaz; hak sembolleri için 02-023.

**02-062** — EKSİK — Düzeltme: Adım her akşam tabloya bakar; ertesi gün ex-date olan olay varsa kart "OLAY: seviyeler × ayar" etiketi alır ve seviyeler ham ölçekte güncellenir. Tablo ileri tarihli kayıt döndürüyor mu: doğrulanamadı (THYAO'da bugün için ileri kayıt yoktu).

**02-063** — EKSİK — Doğrulanamadı: tablonun ve HGDG'nin olay akşamı güncel olduğu verisi yok (S8.7 açık). Düzeltme: Adım kapısı: son gün |ham getiri| > limit ve tablo kaydı yok → kart STOP olmaz, "VERİ GECİKMESİ" olur; gün sonu oran (HGDG/HG) ≠ 1 son çubukta ise veri tutarsız.

**02-064** — EKSİK — Düzeltme: tazelik kapısına ekle: (a) HGDG/HG oranı son çubukta 1,0 (THYAO'da 1,0000 doğrulandı), (b) kendi P_bölünme×temettü serimiz HGDG ile son 5 günde ≤ %0,1, (c) tablo kayıt sayısı önceki koşudan geriye gitmemiş.

**02-065** — EKSİK — Kart seviyeleri ham ölçekte o günün fiyatıyla yazılır ve dondurulur; ÇÖZÜM-A'da temettü seviyeyi değiştirmez; yalnız bölünme/bedelli ayar ile ölçeklenir.

**02-066** — EKSİK — Tasarımda yok. Düzeltme: sinyal günlüğü append-only, o gün yazılan kayıt değişmez; yeniden hesaplama farkı ayrı raporlanır (repainting yok).

**02-067** — EKSİK — 5.11 deneme günlüğü veri anlık görüntüsünü yazar ama anlık görüntü tanımı (02-026) olay tablosunu içermiyor. Düzeltme: kanıt satırı koşu kimliği ve anlık görüntü hash'ine bağlansın; yeni olay sonrası yeniden üretim eski hash ile yapılır.

**02-068** — EKSİK — Düzeltme: canlı işlem ham AOF giriş/çıkış ve ex-date olay çarpanı/nakit akışı ile kaydedilir; kayıt dondurulur; sonraki olay geçmişi değiştirmez.

**02-069** — EKSİK — Aynı tanım gerekli: getiri = P_bölünme getirisi + net temettü akışı; hem doğrulama hem canlı için. 5.12.6 bu tanımı yazsın.

**02-070** — EKSİK — Hash yalnız kod ve parametre. Düzeltme: olay çarpan tablosu hash'i veri anlık görüntüsü hash'ine girer; veri değişimi yeni deneme sayılmaz (kural aynı), "aynı kural, yeni veri" olarak günlüğe yazılır, Holm sayımına girmez, sonuç farkı raporlanır.

**02-071** — EKSİK — Tablo ileri tarihli kayıt içeriyor mu: doğrulanamadı. Düzeltme: backtest ve canlı yalnız SHHE_TARIH ≤ t kayıtlarını bilir; ex-date öncesi kart bastırma yok, ama 02-062 etiketi.

**02-072** — EKSİK — Sızıntı kontrollü: ÇÖZÜM-A'da seviye bağımlı işlemler (adet, tick, TL ATR) o günün ham fiyatından hesaplanır (ham = P_bölünme × k_t, bilgi o gün zaten vardı). TASARIM 5.1'e "seviye bağımlı kurallar ham fiyatla" cümlesi yalnız likidite ve tavan/taban için; ATR TL, adet, tick'i ekle.

**02-073** — EKSİK — K1(b) aynı hisse ±20 gün rastgele günleri ex-date çevresini kısmen kapsıyor; rally etkisini dışlamıyor. Düzeltme: raporda sinyallerin olay ±10 gün içindeki oranı ve olay ±10 gün dışlanmış sonuç yazılsın.

**02-074** — EKSİK — Motor aynı (5.3, 5.7) ama havuz kuralı yazmıyor. Düzeltme: rastgele gün havuzu ex-date dahil; dolum aynı AOF (düzeltilmiş ölçekte); istisna yok, yazılsın.

**02-075** — CEVAPLI — Karşılaştırma mevsimselliği kontrol eder: K1(a) aynı gün, K1(b) aynı hisse ±20 gün (5.7); 5.9 20 günlük blok yeniden örnekleme bağımlılığı kapsar. "60 farklı gün" yalnız örneklem kapısı.

**02-076** — ZAYIF SORU — Etiket yalnız günleri sınıflar (kapı değil, 4); getiri tanımı karışmıyor. K2 getiri tanımı ÇÖZÜM-A ile K2'de belirlenir.

**02-077** — EKSİK — Düzeltme: temettü net (×0,85), ex-date'te nakit olarak yazılır ve faiz kazanır; K2 ve kural aynı tanımla (K2 her gün yatırımlı, kural yalnız pozisyonda). Yön: ex-date'te anında yeniden yatırım K2'yi hafif şişirir (kurala karşı muhafazakâr); brüt kullanmak ikisini de şişirir. Raporda temettü payı ayrı (02-084).

**02-078** — EKSİK — Düzeltme: K2 günlük yeniden dengeli eşit ağırlıklı ortalama getiri (lot yok; bedelsiz/bedelli çarpanla ölçek, temettü ex-date'te yeniden yatırım).

**02-079** — EKSİK — Yazılı değil. Düzeltme: eşbütünleşme günlük log toplam getiri endeksinde (HGDG eşdeğeri: bölünme + temettü) yapılır; p değeri bölünme-yalnız seriyle de hesaplanır ve iki sonucun farkı raporlanır.

**02-080** — EKSİK — ÇÖZÜM-A'da iki bacak kendi AOF'unda, aynı seri kuralıyla (P_bölünme); temettü ayrı nakit; karışma yok. Kural yazılsın.

**02-081** — EKSİK — Tabloda ödeme tarihi alanı yok (alan listesi doğrulandı). Düzeltme: net temettü ex-date kapanışında nakit olarak hesaba girer ve günlük faiz kazanır (hafif iyimser; yazılsın).

**02-082** — EKSİK — Düzeltme: çiftte bir bacak karantinadaysa o çift o pencerede dışlanır; log fark serisinde oran adımı kontrolü (02-031) iki bacağa uygulanır.

**02-083** — EKSİK — Ölçüm farkı olay çevresinde sistematik olabilir. Düzeltme: K2 sepeti kuralın giriş ve çıkış günlerinde aynı AOF'tan AOF'ya hesaplanır; kapanıştan kapanışa ölçüm kullanılmaz.

**02-084** — EKSİK — Düzeltme: rapor fazla getiriyi "fiyat" ve "net temettü" olarak ayrı satırlar; temettü katkısı yüksek verimli hisselerde yoğunsa uyarı satırı.

**02-085** — EKSİK — 7.2 sadakat adımı Yahoo'yu kullanıyor (seçenek bilinçli). `auto_adjust` değeri Tansu'nun çıktısından bilinmiyor; B-momentum notu bunu YORUM sayıyor. Düzeltme: sadakat kontrolü iki ayarla (True/False) koşulur, hangisinin Tansu rakamını ürettiği kaydedilir; gerçek sınama İş Yatırım ile (Yahoo bedelsiz hataları kanıtlı, veri-kaynaklari 2.2).

**02-086** — EKSİK — Eşleşme formülün doğru okunduğunu gösterir (veri aynıysa); eşleşmeme hem formül hem veri hatası olabilir. Düzeltme: olay tablosunda kaydı olan pencerelerde karşılaştırma yapma; yalnız olaysız pencerelerde eşleşmeme formül hatası sayılır.

**02-087** — EKSİK — Taranmıyor. Düzeltme: SMRTG ve ISKPL işlem pencerelerinde olay tablosu çekilip Yahoo getirileriyle çapraz bakılır; olay içeren işlemler sadakat tablosundan "veri artefaktı olabilir" diye ayrılır.

**02-088** — EKSİK — Yahoo `Open` olaylı pencerelerde güvenilmez. Düzeltme: olay gününden −15 işlem günü ile +1 arasında T+1 açılış üretimi atlanır ve sayısı yazılır.

**02-089** — EKSİK — Tansu çıktıları kısa dönemli (KRDMD 2025-12/2026-01, VAKBN–GARAN yakın tarih); zaman kayması olay yoksa küçük. Düzeltme: sadakat kontrolü yalnız olay tablosu boş pencerelerde; tarihli Yahoo çekimi kaydedilir.

**02-090** — EKSİK — Tolerans yok. Düzeltme: EMA200 penceresinde (200 gün+) olay varsa hem Yahoo hem P_bölünme ile hesapla; fark >0,05 yüzde puan ise "sadakat belirsiz" diye YORUM bırak.

**02-091** — EKSİK — 5.1 fiyat bazını kesin yazıyor; E-risk notu YORUM sayıyor. Düzeltme: TASARIM'a "(YORUM)" ekle; ÇÖZÜM-A'da bölünme düzeltmeli seri ham seriyle yalnız temettüde ayrışır, fark küçük; ham-yalnız bölünme varyantı duyarlılık olarak yazılsın.

**02-092** — EKSİK — Düzeltme: 5.3 motor sınamalarına 3 vaka ekle: açık pozisyon + bedelsiz ex-date (stop yok, getiri sürekli), + bedelli (adet çarpanla), + temettü (düşüş gerçek, nakit akışı eklenir).

**02-093** — EKSİK — Beklenen çıktılar yazılı değil. Düzeltme: birim test vakaları ekle: ters bölünme (ayar>1 sentetik), aynı gün iki kayıt (çarpım), 1,0 çarpan (etkisiz), olay günü satır eksik (02-099), HEKTS 2015-11-26 (tarih bir gün erken, gerçek vaka), CCOLA 13 temettü (1−brüt/önceki kapanış).

**02-094** — EKSİK — Raporda yazmıyor. Düzeltme: rapor karantinalı hisse×gün sayısı, pencere oranı ve karantinalı/karantinasız sonuç farkını yazsın.

**02-095** — EKSİK — Sınanmıyor. Düzeltme: bir kerelik duyarlılık: 10 rastgele olayın çarpanını ×1,1 bozup ve 10 olayı silip kabul sonucunun (5.12) değişip değişmediği ölçülür.

**02-096** — EKSİK — Eşik yok. Düzeltme: veri kalitesi kapısı (önceden yazılsın): borsapy farklı gün oranı ≤ %1 (YORUM) ve karantina oranı ≤ %2 (YORUM); aşılırsa aile "veri yetersiz" olur; 5.12'ye 7. madde olarak eklensin.

**02-097** — OLGU — S2-14 kapandı (bkz 02-046): HACIM TL; ham ve düzeltilmiş eşit, bedelsiz günü sıçramıyor. Test: HACIM/AOF ≤ SERMAYE (CCOLA 2024-08-09: 509,8M TL / 761 = 0,67M lot, uygun) yeterli; fiyat × lot karşılaştırmasına gerek yok.

**02-098** — EKSİK — Olay günü kilit kuralı 02-038 referansıyla; çıkış kayması ertesi gün stop yürümemesi olarak P_bölünme'de aynen yansır. Düzeltme: olay gününde kilit testi ex-date baz fiyatıyla; işlem durdurma/satır yok durumunda 02-099.

**02-099** — EKSİK — Çarpan, `SHHE_TARIH`'ten önceki bütün satırlara satır var mı bakılmaksızın uygulanır (ayar < tarih kuralı). İlk mevcut satırın getirisi: ham/(önceki satır × ayar) − 1 ve (1+limit)^k (02-037) ile yargılanır; karantina yalnız bu bileşik limit aşılırsa.

**02-100** — ZAYIF SORU — PD yapay kaymıyor (02-048); TL tutar HACIM olay gününde sıçramıyor (02-097); olay çevresi bireysel hacim artışı gerçek ekonomik etki, yapay değil. Koruma: 60 gün medyan ve aylık sıralama.

## Özet

### Karar sayıları
- CEVAPLI: 2
- OLGU: 19
- ZAYIF SORU: 5
- YANLIŞ: 2 (02-010, 02-034)
- EKSİK: 72

### Doğrulanan olgular
Çekilen veri: THYAO, CCOLA, HEKTS, ASYAB, ECILC, RYSAS (~27 istek, 1 sn aralık, engel yok).
1. HGDG nakit temettüyü de düzeltiyor: CCOLA 13 ve THYAO 2 kayıtta oran adımı ayar ile örtüşüyor.
2. Kod 04 ayar = 1 − brüt_temettü / önceki_ham_kapanış (CCOLA 13/13); net alan (`..._NET`) var, HGDG brüt kullanıyor.
3. SHHE_FIYAT_AYAR_OR çarpımı HGDG oranını yeniden üretiyor: CCOLA'da 2,3e-5 hata, HEKTS 2016 sonrası <1,7e-3 (4 ondalık yuvarlama), THYAO tam.
4. Çarpan tarih < SHHE_TARIH satırlara uygulanır; olay günü düzeltilmez.
5. SHHE_TARIH ex-date (7/8 kayıt); HEKTS 2015-11-26 bir gün erken (HGDG ve ham düşüş 27.11'de, HGDG HEKTS 2015'te tabloya göre %8,3 sapıyor).
6. Bedelli/bedelsiz çarpanı teorik baz fiyattan, tick'e yuvarlanmamış: (P+bedelli_oran·1)/(1+bedelli+bedelsiz)/P; HEKTS 2019 ve 2021 birebir. 0,2646 vs 0,2801 farkı bedelli bedelinin hesaba katılmamasından.
7. THYAO HGDG/HG sabiti 0,9769, 2025'teki iki temettü kaydından (2015 sonrası başka kayıt yok).
8. HGDG 4 ondalık yuvarlı: HEKTS 2015 HGDG ≈ 0,03 TL, oran gürültüsü ±%0,15.
9. HACIM TL tutarı (CCOLA HACIM 509,8M > toplam pay 254M; olayda sıçramıyor; ham=HGDG hacim), S2-14 kapandı. THYAO 2015-01-02'de HG_HACIM ≠ HGDG_HACIM anomalisi var.
10. PD = SERMAYE × ham kapanış, SERMAYE ex-date günü güncelleniyor; PD olayda sıçramıyor. HAO_PD 2 gün geç.
11. Tabloda eklenme/düzeltme tarihi alanı yok; ödeme tarihi alanı yok.
12. `GetSermayeArttirimlari` çerezsiz çalışıyor; ASYAB (kapanmış) 200 OK + boş liste: "olay yok" ile ayırt edilemez; `endeksKodu` "09" ile "" aynı.
13. ECILC/RYSAS 12.03.2020 limit içinde (+%13,0 ve −%19,86), olay yok: TASARIM 5.1 örneği yanlış.
14. HEKTS bedelli/bedelsiz olay günü gerçekleşen − teorik fark: +%1,6, −%2,3, +%5,6, −%4,2; CCOLA +%0,31.

### En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği
1. **ÇÖZÜM-A: iki katmanlı kendi seri (02-010, 041–045, 049–055, 062–065, 072, 077–081).** TASARIM 5.1 / S2-13'e yaz: P_bölünme = ham fiyat × (kod 01/02/03/09/78 ayar çarpımı, tarih < SHHE_TARIH); göstergeler, ATR, SMA, pivot, stop, hedef bu tek seriden; temettü (kod 04) fiyat düzeltmesi değil nakit akışı (ex-date, net=%85, faiz kazanır); adet ve TL seviyeler ham = P_bölünme × k_t. HGDG yalnız kontrol. Temettü düşüşü stop ve SMA250'de gerçek kalır.
2. **Bağımsız olay tutarlılık kontrolü (02-002, 004, 020, 031, 033, 099).** 5.1'e ekle: her olay gününde ham getiri ≈ ayar−1 (aksi karantina), kod 04'te 1−brüt/önceki kapanış, bedelli için teorik formül; günlük HGDG/HG oran adımı ≥5e-4 olan her günde tablo kaydı aranır; bilinmeyen kod "açıklanmış" istisnası almaz.
3. **HACIM = TL (02-046, 047, 097, 040).** S2-14'ü kapat; likidite ve evren HG_HACIM'in medyanı, fiyatla çarpılmaz; HACIM=0 satırları işlem günü değildir (02-018).
4. **Olay tarihi (02-003, 005, 024, 099).** 8.2'yi kapat: SHHE_TARIH ex-date, çarpan tarih < SHHE_TARIH satırlara; olay eşleştirmede ±1 işlem günü tolerans (HEKTS 2015); olay günü satırı yoksa da çarpan uygulanır.
5. **Karantina tanımı (02-028, 029, 030, 037, 038, 099).** Pencere = sıçrama günü → +250 gün, önceki sinyaller silinmez; açık pozisyon sıçramadan önceki son temiz AOF'ta kapanır ve sayıma girer; limit (1+L)^k−1 (k=işlem günü); olay günü referansı önceki kapanış × ayar; aynı maske kural, K1, K2'ye uygulanır.
6. **Limit örneği ve 2015 (02-034, 035).** ECILC/RYSAS örneğini kaldır (limit içindeydi); 02.01–27.11.2015 için ±%20 "doğrulanmadı" ya da sınamayı 01.12.2015'te başlat.
7. **Anlık görüntü ve donmuş kayıt (02-026, 027, 066–070).** Anlık görüntü = ham HisseTekil (HG+HGDG) + tablo JSON, tarihli ve hash'li; sinyal ve kart günlüğü append-only; hash veri anlık görüntüsünü içerir; veri değişimi yeni deneme değil, günlüğe "aynı kural, yeni veri".
8. **Boş yanıt kapısı (02-016, 017, 063, 064).** Tablo boşsa oran (HGDG/HG) sabit olmalı; adım varsa hata; tazelik kapısı: son çubukta oran = 1, P_bölünme×temettü ≈ HGDG ≤%0,1, tablo kayıt sayısı geriye gitmemiş; olay günü ham sıçrama + tablo yoksa kart "VERİ GECİKMESİ" (STOP değil).
9. **Karşılaştırma serileri ve kabul kapısı (02-008, 009, 094, 095, 096).** borsapy ile P_bölünme (temettüsüz) karşılaştır, HGDG ile ayrı; fark sınıfları ve kazanan kuralı yaz; veri kalitesi kapısı (karantina ≤%2, borsapy fark ≤%1; YORUM) 5.12'ye 7. madde; rapor karantina oranı ve karantinalı/karantinasız farkını; bir kerelik bozulma enjeksiyonu.
10. **Temettü ve K2 tanımları (02-007, 014, 077, 078, 083, 084).** Temettü net (NET alanı, %15 varsayımı yaz); kod 03/09 bedelsiz getiri değil, ölçek; K2 günlük yeniden dengeli, AOF'tan AOF'ya, ex-date'te yeniden yatırım; raporda fazla getiri fiyat ve temettü olarak ayrı.

Ek (sıra dışı küçük): motor sınamasına 3 olay vakası (02-092) ve olay birim testleri (02-093); fiyat adımı tablosu (02-056).
