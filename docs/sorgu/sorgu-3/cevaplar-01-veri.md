# Cevaplar 01: Veri

Doğrulama tarihi: 05.10.2026 (yerel saat ~11:12). Kaynaklar: İş Yatırım `HisseTekil` (14 istek, 1 sn+ aralık), borsapy (THYAO, XU100, TCMB politika), TASARIM taslak 5, veri-kaynaklari, sorgu-2, KURALLAR, kurallar/E.
Doğrulanan olgular "V1…V10" diye anılır; listesi `## Özet` içindedir.

**01-001** — EKSİK — Format, konum, saklama ve hash yazılı değil. Minimal: anlık görüntü = parquet + `manifest.json` (dosya başına SHA-256, indirme zamanı, hisse listesi, durum); koşu başında hash doğrulanır, uymazsa koşu durur. "Değişmez" = hash eşleşmesi.

**01-002** — EKSİK — Tam geçmiş tek istekte iner (THYAO 2000'den bugüne 6.684 satır tek yanıt, V3). 500 hisse boyutu ölçülmedi. Minimal: her koşuda tam indir, sıkıştırılmış sakla; HGDG/HG oranı eski günlerde değiştiyse (önceki anlık görüntüyle karşılaştır) "olay" diye işaretle. Yalnız yeni gün eklemek HGDG'yi yakalamaz.

**01-003** — EKSİK — Manifest'e hisse başına durum (tamam / hata / boş) ve anlık görüntüye TAM veya KISMİ etiketi yazılsın. KISMİ ise kart üretilmez. Deneme günlüğü (5.11) anlık görüntü kimliği ile bu etiketi birlikte kaydeder.

**01-004** — EKSİK — Kayıt = o gün 19:30 anlık görüntüsüyle üretilen kart; sonradan değişmez. Yeniden hesap ayrı "yeniden oynatma" olarak yazılır, kayıt sayılmaz. Kartta stop ve hedef ham TL olarak saklanır (bkz. 01-079).

**01-005** — OLGU — Doğrulanamadı: iki farklı zamanlı örnek gerekir, elde yok. Dolaylı iz: 2026 satırlarında tutarsızlık var (V2: THYAO 22.04, 21.05, 04.08.2026 AOF [min,max] dışında; 21.05 ve 16.09.2026 çok hissede min=max=kapanış ama AOF farklı). Tazelik kontrolü yalnız tarihe bakar, düzeltmeyi göremez. Minimal: her koşuda önceki günün çubuğunu yeniden indirip eskisiyle karşılaştır; farkı günlüğe yaz (20 iş günü sonra düzeltme sıklığı ölçülür).

**01-006** — EKSİK — 19:30 hiçbir ölçüme dayanmıyor (Açık soru 7). Gözlem: 11:12'de İş'in son satırı 02.10 (bugünkü çubuk yok); borsapy bugünkü çubuğu 09:00 damgalı ve yarım veriyle döndürüyor (V6). Arife yayın saati ölçülmedi. Minimal: ilk haftalar 18:30–22:00 arası 15 dk aralıkla yokla, bugünkü satırın ilk göründüğü saati günlüğe yaz; saati buna göre sabitle.

**01-007** — EKSİK — Hafta sonu ve resmî tatil: "beklenen işlem günü" olmadığı için koşu zaten çıkar. Hisse durdurması İş'te eksik satır değil, sıfır satırdır (HACIM=0, AOF/MIN/MAX=0, kapanış önceki değer taşınmış; KONTR 17.06.2026, ASYAB 2016, V4). Kural: kart için bar tarihi = bugün **ve** o hissenin HACIM > 0.

**01-008** — EKSİK — Eşik yok. Minimal: bugünkü HACIM, önceki 20 işlem gününün medyanının %20'sinin altında veya 5 katının üstündeyse kart yok; sayılar sonuç görülmeden yazılır. Yarım günlerde alt eşik ikiye bölünür (01-014).

**01-009** — EKSİK — İki ifade çelişmiyor ama kaynak yazılı değil. Minimal: gerçek işlem günü = İş'in döndürdüğü günler (hafta içi eksikler THYAO'da 2000–2026 arası 295 gün = tatiller, V4); takvim yalnız "beklenen gün" için tazelik kontrolünde kullanılır. Çelişirse veri kazanır, fark alarmdır.

**01-010** — EKSİK — Tek hissede eksik gün sıfır satır olarak görünür (V4), eksiklik değildir. Tüm piyasa günü eksikse: o gün evrenin %80'inden fazlasında satır yoksa "tatil", yoksa "veri hatası". THYAO için İş ve borsapy gün kümesi 2015–2026'da aynı (V5). Bu kontrol tasarımda yok.

**01-011** — OLGU — Doğrulandı (V5): İş THYAO 02.01.2015–02.10.2026 = 2.947 satır (sorgu-2 doğru). borsapy aynı 2.947 günü + 05.10.2026 yarım çubuğu = 2.948. 2.945/2.946 daha eski bitiş tarihinden; eksik gün farkı değil.

**01-012** — CEVAPLI — Sorgu-2 S15: "İş Yatırım'ın verdiği günler işlem günüdür". Pencereler satır (işlem günü) bazlıdır, takvimin bilmesi gerekmez. Veride 08, 09, 10, 13, 14 Şubat 2023 satırı yok (THYAO, V4).

**01-013** — EKSİK — Ayrı resmî liste gerekmez, yeter ki gerçek gün İş verisinden türetilsin (01-009 düzeltmesi). Liste yalnız tazelik uyarısı içindir, yanlışı zararsızdır.

**01-014** — EKSİK — Gözlem: THYAO 09.04.2024 (arife) HACIM 4,48 mlr TL, önceki gün 11,2 mlr TL (V2 verisi). Minimal: yarım günleri etiketle; hacim eşiğinde ve medyan penceresinde ayrı tut (eşik ×0,5). ATR'ye dokunma: yılda 2–3 gün, etkisi küçük.

**01-015** — EKSİK — Durdurma günü sıfır satırdır, XU100 ile hizalama bozulmaz. Eksik olan: sıfır satırın nasıl işleneceği. Minimal: HACIM=0 satırı NaN say, göstergeden çıkar, ileri doldurma yok; pencerede NaN > %10 ise o hissede sinyal yok.

**01-016** — EKSİK — İş `HisseTekil` ile `XU100` boş dizi döndürüyor (2020–2026, V7). borsapy `Index("XU100").history(period="max")` çalışıyor: 3.650 satır, 14.03.2012–05.10.2026 (bugünkü yarım çubuk dahil, V6). Minimal: XU100 = borsapy, veri-kaynaklari'na yazılsın; son tamamlanmış gün kullanılsın. İş satırlarındaki `END_DEGER` (02.01.2024 = 7.624,29) büyük olasılıkla XU100 (doğrulanmadı).

**01-017** — OLGU — Doğrulandı (V3): uç nokta sınırı değil. THYAO 04.01.2000–02.10.2026 = 6.684 satır; 2005–2014 aralığı 2.509 satır döndü. 2015 araştırmacının tercihi.

**01-018** — EKSİK — Veri 2000'e kadar var (V3), ısınma için 2014'ten veri indirilebilir; tasarım bunu yazmıyor. Yazılmazsa ilk SMA250 sinyali 2015 sonu/2016 başı olur ve "2015–2017" ileri yürüme fiilen ~2 yıl olur. Minimal: ısınma verisi için 2014 (en az 250 gün) indirilir, sinyal 2015-01-02'den başlar. Dikkat: 2000–2014 satırlarında sıfır ve aralık dışı kapanış satırları var (V2).

**01-019** — EKSİK — Marj bilinmiyor. Ölçüm: 2015'te ±%10'u aşan 6 gün, en yüksek +13,3/−14,8 (veri-kaynaklari 5.1). Minimal: 02.01–27.11.2015 yalnız ısınma verisi olsun, sinyal/işlem 30.11.2015'ten başlasın; karantina eşiği sorusu ortadan kalkar.

**01-020** — OLGU — Doğrulanmadı; bu oturumda 2015 ölçülmedi. Minimal sınama: THYAO ve XU100 için HACIM ve getiri dağılımını 27.11 öncesi/sonrası karşılaştır. 01-019 düzeltmesi (2015 öncesi işlem yok) riski büyük ölçüde kapatır.

**01-021** — CEVAPLI — veri-kaynaklari 5 madde 4 ve 5: Duyuru 2020/20, 2020/21 ve 2025/38860 "ikinci duyuruya kadar" ±%10 yapar; prosedür dipnot 10 genel tablodan önceliklidir. Ölçüm: 2021–2026 20 hissede tam ±%10. Bu oturumda EUPWR, KONTR, SMRTG kilitli günleri 9,8–10,0 arası (V1). Pazar bazlı ayrım hâlâ doğrulanmış değil ama veri tek ±%10 gösteriyor.

**01-022** — CEVAPLI — Karantina limiti pazara göre okunmaz, dönem tablosundan okunur (5.1). Yıldız Pazar'da gerçek +%15 gün gözlenmedi; 13.03.2020 sonrasında 20 hissede ve bu oturumdaki 3 hissede ±%10 aşılmadı.

**01-023** — EKSİK — Baz fiyat tanımı ve adım tablosu hiçbir yerde yok. Veri: KONTR 08.07.2026 tavan +%9,78 (4,49 TL, adım %0,22); tavan getirisi limitin hemen altında kalıyor. Minimal: kilitli = MIN==MAX ve HACIM>0 ve getiri ≥ limit − 1 adım/önceki kapanış; adım tablosu Borsa İstanbul prosedüründen alınır; sınama vakası: KONTR 08.07.2026.

**01-024** — EKSİK — Olay gününde ham getiri limiti aşar (CCOLA 13.08.2024: ham 760,5 → 69,35). Minimal: olay tablosunda kaydı olan günde tavan/taban getirisi ham kapanış / (önceki ham kapanış × `SHHE_FIYAT_AYAR_OR`) ile hesaplanır; temettü günlerinde fark küçüktür, yok sayılır.

**01-025** — EKSİK — Kural yok. Minimal: rüçhan/bedelli günü olay tablosundaki çarpanla düzeltilmiş getiri limit kontrolüne girer; olay gününde yeni giriş yapılmaz; açık pozisyonun stop/hedefi çarpanla ölçeklenir (bkz. 01-079). Bedelli günü sonrası karantina yalnız düzeltilmiş getiri limiti aşarsa.

**01-026** — EKSİK — Gerçekçi değil, ölçülemez. Ölçüm (V1): EUPWR 7 kilitli gün, ama kapanışı tavan olup MIN<MAX olan 48 gün; SMRTG 11 kilitli / 73; KONTR 15 kilitli / 126. Tavan günü AOF çoğu zaman tavanın altında (EUPWR 16.05.2023: AOF 74,77, tavan 76,70). Muhafazakâr minimal: kapanışı tavan olan (getiri ≥ limit − 1 adım) günde giriş yok. Duyarlılık: yalnız MIN==MAX ile fark raporlanır.

**01-027** — EKSİK — Kanıt yok; lot kuyruğu veride yok. Simetrik muhafazakâr kural: kapanışı taban olan günde çıkış kayar. İyimser sürüm (yalnız MIN==MAX) duyarlılık olarak raporlanır.

**01-028** — EKSİK — Pozisyon, ilk kilitli olmayan güne kadar tutulur; sınır yok. Her gün aynı kural uygulanır; çıkış o günün AOF'undadır; kayıp gerçek AOF ile hesaplanır, ek varsayım gerekmez. Veri biterse son HACIM>0 kapanışı (01-070). Bu üç cümle 5.3'e eklenir.

**01-029** — EKSİK — Evet sanır. Veri: KONTR'da MIN==MAX olup limitte olmayan 10 gün var (V1; biri sıfır satır, biri tutarsız 21.05.2026 satırı, diğerleri limit−adım). Minimal: kilitli = MIN==MAX ∧ HACIM>0 ∧ getiri limitte (01-023); diğer MIN==MAX günleri "tek fiyat/şüpheli" etiketi alır, giriş yok, çıkış kayar.

**01-030** — EKSİK — Ayırt edilemezse etki ölçülür: "tek fiyat benzeri gün" (MIN==MAX, limit dışı) oranı hisse bazında raporlanır (KONTR: 10/1.491 gün) ve bu hisse-günler hariç duyarlılık koşusu yapılır.

**01-031** — EKSİK — Tanım belgelenmedi, doğrulama kuralı yok. Ölçüm (V2, THYAO 2000–2026): AOF [min,max] dışında 4 satır (3'ü 2026), kapanış aralık dışı 37, sıfır içeren 38 satır. Minimal doğrulama: MIN ≤ AOF ≤ MAX, MIN ≤ kapanış ≤ MAX, HACIM>0 ⇒ AOF>0; ihlal eden hisse-gün karantinaya.

**01-032** — EKSİK — Hiçbir veriyle sınanamaz. Tek koruma 5.4'teki %2 sınırı. Minimal: dolum günü "pozisyon TL / günün HACIM TL" oranı raporlanır, > %5 ise uyarı.

**01-033** — EKSİK — Gün içi sıra bilinemez (borsapy da yalnız OHLC verir). Giriş günü stop için kötümser kural: düşük ≤ stop ise stop vurulmuş sayılır; oran raporlanır. Bu 5.3'te "giriş günü" satırına eklenir.

**01-034** — EKSİK — Stop fiyatından dolum iyimserdir; İş verisinde açılış yok. Fakat borsapy `Open` sütunu veriyor (V6). Minimal: `Open` ≤ stop ise dolum = `Open` (ölçek: Open / borsapy kapanış × İş kapanışı); yoksa duyarlılık koşusu dolum = min(stop, AOF).

**01-035** — CEVAPLI — TASARIM koddan ve kurallardan önce gelir (başlık notu); geçerli olan AOF (5.3). `kurallar/E-risk-cikis-surec.md` satır 75 hâlâ "açılış fiyatı veya daha kötüsü" diyor. Bir cümleyle "AOF (TASARIM 5.3)" yapılmalı.

**01-036** — EKSİK — Sayı (KURALLAR satır 98) yalnız "sıklık kontrolü"; hiçbir karara bağlı değil, İş verisiyle yeniden sayılmadı. Minimal: satıra "Yahoo, geçersiz; İş verisiyle yeniden sayılacak" notu ya da satırı sil.

**01-037** — CEVAPLI — TASARIM 7.2 / KURALLAR 4: Tansu'nun kodunda `yfinance` ve `.IS` görünüyor, amaç onun gördüğünü yeniden üretmek. Bozuk veri yalnız olay günlerinde (veri-kaynaklari 2.2); bu günleri içeren pencerelerde sapma beklenir. Gerçek sınama İş verisiyle.

**01-038** — EKSİK — Hüküm yazılı değil. Minimal: formül Yahoo'da üretilir; aynı formül İş HGDG ve ham sürümünde de koşulur, sinyal/rakam farkı raporlanır; fark yalnız olay/temettü gününden geliyorsa "sadakat geçti" sayılır.

**01-039** — EKSİK — İki ayar da denenmeli: `auto_adjust=True` Yahoo'da bedelsiz düzeltmesi yapmaz, yalnız temettü (veri-kaynaklari 2.2). Minimal: her iki ayar koşulur, Tansu'nun rakamını veren ayar kaydedilir. Karşılığı: `auto_adjust=True` ≈ HGDG (temettülü), `False` ≈ borsapy (temettüsüz).

**01-040** — EKSİK — Evet, temettü verimi > %0,5 olan her ex-günde alarm verir. Ölçüm (V5, THYAO 2015–2026): HGDG ile borsapy getiri farkı > 0,5 puan olan yalnız 3 gün (27.03.2018, 16.06.2025, 02.09.2025); THYAO az temettü verir, yüksek verimli hissede çok olur. Minimal: kod 04 günlerinde fark |fark − temettü verimi| ile ölçülür.

**01-041** — OLGU — Kısmen doğrulandı. THYAO'da HGDG/borsapy oranı 2015'ten 2025 ağustosuna kadar 0,9769, 2025'te iki adım (28.08.2025 0,9898, 02.09.2025 sonrası 1,0), yani THYAO'nun 2025'e dek temettüsü yok ya da uygulanmadı; ayırt edilemiyor. İkinci kanıt: CCOLA 29.07.2024 HGDG 76,62, borsapy 79,545 (veri-kaynaklari 3.2). Üç-dört olayla "tüm nakit temettüleri" ifadesi desteklenmiş sayılmaz. Minimal: olay tablosu kod 04 günleriyle HGDG/ham oran adımı karşılaştırılır.

**01-042** — OLGU — Doğrulanmadı (olay tablosu çekilmedi). Ölçüm yolu: HGDG/HG oranının adım günü ile kod 04 `SHHE_TARIH`'i karşılaştır (en az 10 olay). Ödeme tarihinde uygulanıyorsa ex–ödeme arası seviye yanlışı temettü verimi kadardır (tipik %1–5); sinyallere etkisi küçüktür ama yüksek temettülü hissede ölçülmeli.

**01-043** — EKSİK — Ayrım yazılı değil. Minimal: bedelsiz/bedelli farkı için kendi çarpanımız ile HGDG'nin ham oran adımı karşılaştırılır (temettüsüz bileşen); temettü için olay tablosunda kod 04 günü beklenir; kod 04 olmayan günde oran adımı = hata.

**01-044** — CEVAPLI — 5.1 zaten sınar: kendi çarpan ile HGDG karşılaştırılır. Doğrulandı: CCOLA 13.08.2024 HGDG/HG oranı 12.08'de 0,08757, 13.08'de 0,96329; bölümleri 0,09091 = `SHHE_FIYAT_AYAR_OR` 0,0909. Çarpan HGDG'nin kendi adımıyla uyuşuyor.

**01-045** — EKSİK — Sınama vakası yok. Minimal: aynı günde birden çok kayıt varsa çarpanların çarpımı HGDG oran adımına eşit olmalı; eşit değilse hisse-gün karantina. Vaka olarak HEKTS 30.04.2021 (kod 03) eklenir.

**01-046** — ZAYIF SORU — PD = HG_KAPANIS × SERMAYE (V9, CCOLA); sermaye azaltımında PD gerçekten düşer ve bu doğru davranıştır. Çarpan 1,0 fiyatı doğru olarak düzeltmez.

**01-047** — EKSİK — Kural yok. Minimal: bilinmeyen kod olay günü sayılır; HGDG/HG oran adımı varsa ve tabloda tanınan kod yoksa "bilinmeyen olay" listelenir; adım yoksa yok sayılır; ham sıçrama limit dışıysa karantina.

**01-048** — EKSİK — Pencere yok, ileriye bakış riski gerçek. Minimal: karantina sıçrama gününden başlar ve ileriye doğru en uzun gösterge penceresi (SMA250 → 250 işlem günü) kadar sürer; sıçramadan önceki sinyal ve işlemler silinmez.

**01-049** — EKSİK — Limit içi hata yakalanmıyor. Minimal: ikinci kaynak adımı: HG/borsapy kapanış oranı bir günden diğerine değişirse (>%2, olay tablosunda yoksa) listele. borsapy bölünme düzeltmeli olduğu için olay tablosuna bağımsız bir yedek olur.

**01-050** — CEVAPLI — Nihai olan TASARIM 5.1 (dönem tablosu + %0,5), çünkü veri-kaynaklari 7.2 öneri notudur ve limiti %20/%10 olarak ayırmadan yazılmıştı. 7.2 sonrası TASARIM'a işlendi (S2-n etiketli taslak 5).

**01-051** — EKSİK — Rapor satırı ve üst sınır yok. Minimal: karantina hisse-gün oranı rapora yazılır; üst sınır 01-100 kapısına girer. Yön: karantina uç günleri atar; kural getirisi için belirsiz (iyimser olabilir), bu belirsizlik raporda yazılır.

**01-052** — EKSİK — K1 ve K2 için karantina maskesi tasarımda yok. Minimal: aynı maske K1, K2 ve kurala uygulanır (aynı hisse-pencere hepsinde dışarıda).

**01-053** — YANLIŞ — Örnek yanlış. Ölçüm (V8): ECILC 11.03.2020 +%19,82, 12.03.2020 +%13,03; RYSAS 12.03.2020 −%19,86 (ham). 12.03.2020'de limit ±%20 olduğuna göre ikisi de limit+%0,5 içinde, yani bu kuralla karantinaya girmez; ±%10 altında girerdi. Düzeltme: örneği kaldır ya da "±%10 olsaydı" diye yaz; gerçek sınama vakası olarak 13.03.2020'yi kullan.

**01-054** — OLGU — Doğrulandı (V8): 13.03.2020 seansından itibaren ±%10. ECILC 13.03 −%9,98; RYSAS 13.03 +%9,87 ve kapanış 5,01 = 4,56 × 1,10 (tavan). 12.03'te hareketler −%19,86'ya kadar çıktı, yani ±%20 hâlâ geçerliydi. Karar günü: 12.03 → ±%20, 13.03 → ±%10; tasarım dönem tablosu bununla uyumlu.

**01-055** — EKSİK — Sonuçsuz rapor olur. Minimal: İş kazanır (birincil kaynak); olay ve temettü ex-günleri dışında kalan uyuşmazlık günü sayısı 01-100 kapısına girer; yalnız bu gün karantinaya alınmaz.

**01-056** — EKSİK — Tasarım 4 İş'i birincil seçiyor (İş kazanır). İnce hissede fark ölçülmedi, THYAO için 2.946 günde 3 uyuşmazlık (V5). Minimal: 500 hissede uyuşmazlık günü ölçülüp sınıf bazında raporlanır; İş birincil kalır.

**01-057** — EKSİK — Sınanmadı. Gözlem: 14 istekte engel yok, ama iki okuma zaman aşımı (40 sn ve 90 sn; ağır sorgular 2015+ ve 2020+) (V10). Minimal: istek arası 2 sn, zaman aşımı 120 sn, 3 deneme, önbellek; yedek: borsapy fiyatları (ham değil, temettüsüz, Open var), yani HGDG/ham ayrımı kaybolur; tasarımın o kısmı çalışmaz.

**01-058** — EKSİK — Şema sınaması yok ve sessiz boşluk gerçek: `XU100` hata vermeden `[]` döndü (V7), `.E` eki de boş döner. Minimal: yanıt sınaması (beklenen alanlar, tür, satır>0, tarih sıralı, tekrar yok, ihlal yok) + her koşuda THYAO kanarya sorgusu.

**01-059** — EKSİK — Sorgu-2 S52 "sistem satılmaz, paylaşılmaz" diyor ama TASARIM'da yok ve raporlar kapsanmıyor. Minimal: TASARIM'a "ham veri ve kartlar üçüncü kişiyle paylaşılmaz; paylaşım hukuki sorulur" satırı ve Açık soru 1'e bağlama.

**01-060** — OLGU — Kısmen doğrulandı. Fiyat satırları metin `dd-mm-yyyy` (`HGDG_TARIH`), kayma yok. `END_TARIH` epoch 1704142800000 = 01.01.2024 21:00 UTC = 02.01.2024 İstanbul (V10). `SHHE_TARIH` bu oturumda çekilmedi. Minimal: tz-aware `Europe/Istanbul`'a çevir (2016 öncesi UTC+2/+3 değişir); sınama: HEKTS 30.04.2021 ve CCOLA 13.08.2024 olay gününün ham kapanış sıçramasıyla aynı güne düşmesi.

**01-061** — ZAYIF SORU — Premis yanlış: HGDG alanları 4–5 ondalıklı (230,9354; 276,05966), HG_AOF 3 ondalıklı (235,797). Gerçek risk olay gününde ham baz fiyatın adıma yuvarlanması (1 TL'de ~%0,5); olay günlerinde eşiğe mutlak yarım adım eklenir.

**01-062** — OLGU — Doğrulandı: `HGDG_HACIM` = `HG_HACIM`, ölçeklenmez (THYAO tüm 2024 satırları, CCOLA bedelsiz günü 13.08.2024: ikisi de 360.894.374). Düzeltilmiş hacim ayrı değil; TL hacim tek seri.

**01-063** — OLGU — Doğrulandı (V1): HACIM **TL**. THYAO 02.01.2024 HACIM 5.949.755.027 = `DOLAR_HACIM` 201.746.109 × kur 29,4913. CCOLA bedelsizde HACIM sıçramıyor (12.08: 808 mn, 13.08: 361 mn), lot olsaydı ~11 kat artardı. Koşu TL ile yapılır; fiyat × lot gerekmez. borsapy `Volume` ise lot (THYAO 05.10.2026 yarım gün 8,47 mn).

**01-064** — EKSİK — Hacmin içeriği (özel işlem, kapanış seansı) ölçülemiyor. Pratik sınır: %2 sınırı zaten medyanın küçük payı. Minimal: 01-032'deki katılım oranı raporu; abartı belirsizliği raporda yazılır.

**01-065** — EKSİK — `HAO_PD` var (THYAO 02.01.2024: PD 326 mlr, HAO_PD 165 mlr). Gerçek BIST100 seçimini en iyi PD değil, halka açık değer yansıtır (bu oturumda doğrulanmadı). Minimal: evren sıralaması `HAO_PD`; PD ile örtüşme oranı rapora yazılır.

**01-066** — OLGU — Doğrulandı (V9): PD = HG_KAPANIS × SERMAYE (CCOLA 08.08.2024: 757,5 × 254.370.782 = 192,7 mlr). CCOLA bedelsiz gününde (13.08.2024) SERMAYE aynı gün 2,798 mlr oldu, PD sıçramadı (193,4 → 194,0 mlr). Başka olaylarda gecikme ölçülmedi. Minimal koruma: PD günlük değişimi > %40 ve olay yoksa o gün seçim yapılmaz.

**01-067** — EKSİK — Ölçülmedi. Minimal: aynı şirketin birden çok sembolü küçük elle tablodan eşlenir, evrende en yüksek TL hacimli sembol kalır; eşlenmeyenler için aynı gün aynı SERMAYE+PD gören çiftler uyarı verir.

**01-068** — EKSİK — Minimal: seçim ay başından önceki son işlem gününün kapanış verisiyle yapılır, ayın ilk işlem gününden geçerli olur. Seçimden sonra işlem durursa 01-070 kuralı.

**01-069** — EKSİK — Zaten uyumlu: 60 günlük şart ve SMA250 ısınması halka arzı ilk ~250 günde dışarıda bırakır, yani yeni halka arzdan sinyal çıkmaz. Ama "gösterge penceresi dolmadan sinyal yok" kuralı yazılı değil. Minimal: bu cümle 5.2'ye eklenir.

**01-070** — EKSİK — Veride: son satırlar sıfır (ASYAB: 20–25.07.2016 AOF/MIN/MAX/HACIM=0, kapanış 0,87 taşınmış, V4). Kural yok. Minimal: son HACIM>0 günün kapanışında çıkış; duyarlılık: −%50 ve −%100 çıkış; kapanmış hisse sayısı raporlanır.

**01-071** — EKSİK — Aynı kural: tür (birleşme/tasfiye/iptal/bilinmiyor) elle etiketlenir; bilinmeyen son fiyattan çıkar, duyarlılık −%50 (01-070).

**01-072** — OLGU — Ölçülmedi: kapanmış sembol listesi yok. ASYAB var (142 satır 2016, 25.07.2016'ya kadar). Minimal ölçüm: KAP'tan bilinen 20 kapanmış sembolün kaçı döndüğü sayılır; döndürmeyenler rastgele mi yoksa kötü sonuçlu mu, bu tablodan okunur.

**01-073** — EKSİK — Eşleme tablosu yok. Minimal: sembol başına ilk/son gün ve süreklilik sınaması; ham kapanışta >%30 sıçrama + olay yok + SERMAYE uyumsuz = "kod yeniden kullanımı şüphesi", sembol o noktada bölünür.

**01-074** — OLGU — Doğrulanmadı. KAP sorgusu 2000 kayıt/sorgu ve kapsam bilinmiyor (veri-kaynaklari 1.4, 8). 5.2 "bulunamayanlar raporda yazılır" der. Minimal: rapora bulunan/bulunamayan sayı ve dönem aralığı yazılsın.

**01-075** — EKSİK — Evet iyimser olur. Minimal: bedelli günü içeren işlemler ayrı raporlanır; duyarlılık koşusu bu işlemler hariç.

**01-076** — CEVAPLI — 5.7 K2 "aynı temettü düzeltmesiyle": aynı HGDG kullanılır, fark kısmen sökülür. Etki tutma süresiyle ve temettü verimli hisse seçimiyle orantılıdır; stopaj ve ödeme gecikmesi (01-092) hâlâ açık.

**01-077** — EKSİK — Evet kayabilir. HGDG/borsapy fark en çok %2,4 (THYAO, 2015–2025), yüksek temettülü hissede çok daha fazla. Minimal: sadakat kontrolünde göstergeler HGDG ve borsapy (temettüsüz) ile ayrı hesaplanır, sinyal tarihi uyuşmazlık oranı raporlanır.

**01-078** — EKSİK — Tasarımda çelişki var: Bölüm 4 düzeltmeyi olay tablosundan yapar, S2-13 göstergeleri HGDG'den alır. Minimal: göstergeler = HGDG; kendi çarpanımız yalnız denetim; fark varsa HGDG kazanır, gün 01-100 sayacına girer.

**01-079** — EKSİK — Dönüşüm yazılı değil. Minimal: ham seviye = düzeltilmiş seviye × (HG_t / HGDG_t) o günün oranı; kart her gün yeniden yazılır. Doğrulama: son günde oran 1,0 (V5).

**01-080** — EKSİK — Aynı çözüm: tüm hesaplar anlık görüntünün HGDG'sinde, kartta ham seviye = HGDG × (HG_t/HGDG_t); olay günü yeniden yazılır (01-079).

**01-081** — EKSİK — Sinyal ile işlem arası bir iş günüdür; yalnız o gün olay varsa fark çıkar. Aynı dönüşüm (01-079); olay günü girişte A ham karşılığı çarpanla ölçeklenir.

**01-082** — EKSİK — Sınama yok. Minimal: haftada bir iki anlık görüntü arası fark testi: aynı hissede sinyal tarihi değişen oranı. Motor belirleyicidir (aynı anlık görüntü → aynı sonuç), ama farklı anlık görüntüler için bu test gerekir.

**01-083** — EKSİK — Kayma ayrı modellenmiyor; sabit %0,3 içinde. Likit hissede (evrenin ilk 100'ü) yeter, düşük likitte ve evrenin alt ucunda yetmeyebilir; %0,5 senaryosu bunu kapsar. Minimal: dolum oranı raporu (01-032).

**01-084** — YANLIŞ — 5.4 hâlâ "açılışta kovalama" yazıyor, ama 5.3 açılışı kullanmıyor (AOF). Minimal: bileşenleri "komisyon, BSMV, AOF'a göre kayma" olarak yeniden yaz ve eşiği (%0,3) buna göre gerekçelendir.

**01-085** — EKSİK — Minimal: stop/hedef fiyatı adıma yuvarlansın (stop yukarı, hedef aşağı); ATR < 3 adım ise o hisse-günde giriş yok. Adım tablosu 01-023 ile aynı yerden.

**01-086** — EKSİK — Yanlılık doğru: kapanmış hisselerin sektörü yok, çift seçiminden düşer. Minimal: sektör kaynağı (borsapy etiketi) yazılır, "sektör bilinmiyor" hisseler çiftten dışlanır, sayı raporlanır.

**01-087** — YANLIŞ — Çelişki var: Bölüm 4 "TCMB politika faizi (borsapy)", Bölüm 5.6 "EVDS; 2015–2017 politika faizi, sonrası TLREF". EVDS anahtarı yok. Minimal: 5.6'yı "borsapy politika faizi (anahtarsız), ileri doldurma, 2015–2026 tek seri" yap; TLREF kullanma.

**01-088** — YANLIŞ — Evet, 2018 ve 2019 başı açıkta (TLREF hesaplama 28.12.2018, yayın 17.06.2019). 01-087 düzeltmesi tek seri kullanarak kapatır.

**01-089** — EKSİK — Seri bugün hâlâ 23.01.2026'da bitiyor (37,0; 57 satır, V10). Tazelik kontrolü yalnız fiyatı kapsıyor. Minimal: faiz serisinin son tarihi > 60 gün eskiyse "faiz bayat" uyarısı; ileri doldurma süresi raporlanır.

**01-090** — OLGU — Kısmen doğrulandı: `lending` yalnız dolu sütun, `borrowing` boş. Değerler 1 hafta repo ile tutarlı (08.06.2018 17,75; 14.09.2018 24,00; 23–24.10.2025 39,5; 12.12.2025 38,0; 23.01.2026 37,0); resmî TCMB tablosuyla bu oturumda karşılaştırılmadı. Efektif fonlama farkı (2018) ölçülmedi; politika faizi daha düşükse boştaki nakit getirisi düşük hesaplanır, yani kural aleyhine muhafazakâr.

**01-091** — EKSİK — Tablo tarihleri toplantıdan 1 gün sonra (MPC 07.06.2018 → tablo 08.06; 13.09.2018 → 14.09; V10), yani yürürlük günü; aynı gün kullanım geleceğe bakmaz. Yine de kural yazılı değil. Minimal: nakit getirisi için önceki günün oranı (shift 1) kullanılır.

**01-092** — EKSİK — "Bir kısım" hesabı yok. Minimal: raporda hesap: işlem başına yıllık temettü verimi × stopaj oranı ≈ ek masraf; bu, %0,5 − %0,3 = %0,2 puan ile karşılaştırılır. Stopaj oranı doğrulanmadı.

**01-093** — EKSİK — Parmak izi yalnız kod ve parametre. Minimal: deneme kimliği = (kural hash, parametre, anlık görüntü kimliği). Aynı kural farklı anlık görüntüde "yeniden koşu": günlüğe yazılır, Holm sayısını artırmaz, sonuç farkı raporlanır.

**01-094** — EKSİK — Anlık görüntü kapsamı yazılı değil. Minimal: tek paket kimliği = fiyat (ham+HGDG) + olay tablosu + evren listesi + faiz + takvim; hepsinin hash'i manifest'te; biri değişirse yeni kimlik.

**01-095** — EKSİK — Süreç yok. Minimal: anlık görüntü durumu aktif / iptal; hata bulunursa yeni anlık görüntü alınır, eski sonuçlar "veri hatalı" etiketiyle yeniden koşulur, kural kaydı değişmez.

**01-096** — EKSİK — Kaçırılan gün veri açısından telafi edilir (İş geçmişi geri verir) ama kart/kayıt telafisi yok. Minimal: kaçırılan günün kartı üretilmez, "kaçırılan gün" sayısı raporlanır; açık pozisyonlar Adım ile gün gün telafi edilir, kâğıt üstü yeni giriş o gün sayılmaz.

**01-097** — EKSİK — borsapy bugünkü çubuğu içeriyor ama 09:00 damgalı ve gün içi yarım (11:12'de THYAO Volume 8,47 mn lot, V6). 19:30'da son çubuğun kesinleşmesi güvenilir değil. Minimal: çapraz kontrol bugünü kapsamaz; T−1'e kadar yapılır.

**01-098** — EKSİK — Evet, farklı tarihli verilerle yapılır. Minimal: ham + HGDG + olay tablosu aynı anlık görüntüde (01-094).

**01-099** — OLGU — Kısmen ölçüldü: THYAO 2000–2026 (6.684 satır) tek yanıtta geldi; 2020–2026 aralığı EUPWR, KONTR, SMRTG için geldi; 2015–2026 THYAO ilk denemede 40 sn zaman aşımına, ALVES 90 sn zaman aşımına uğradı (14 istekte 2 zaman aşımı). 500 sembol ve yanıt boyutu ölçülmedi. Tek hisseden genelleme: evet. Minimal: 50 hisseli deneme, zaman aşımı 120 sn.

**01-100** — EKSİK — Kapı yok. Minimal: veri kalitesi kapıları (karantina hisse-gün oranı, sıfır/aralık dışı satır oranı, çapraz kontrol uyuşmazlık günü oranı olay/temettü hariç) getiri görülmeden yazılır ve 5.8'deki kural kaydıyla birlikte hash'lenir. Gevşetme P3'e göre tarihli kayıt gerektirir; böylece değişiklik hash farkıyla görünür. Sayıları ilk veri koşusunun getirisiz dağılımından seç.

## Özet

**Verdikt sayıları**

1. CEVAPLI: 8
2. EKSİK: 71
3. YANLIŞ: 4
4. OLGU: 15
5. ZAYIF SORU: 2

**Doğrulanan olgular** (14 İş Yatırım isteği + borsapy)

1. V1: HACIM TL'dir (THYAO 02.01.2024: 5.949.755.027 TL = DOLAR_HACIM × kur). `HGDG_HACIM` = `HG_HACIM`, bedelsizde ölçeklenmez (CCOLA 13.08.2024). Kilitli taban ve tavan günleri EUPWR 7/7, SMRTG 11/11 limitte; KONTR 25 MIN==MAX gününün 10'u limitte değil.
2. V2: `HG_MAX==HG_MIN` güvenilir kilit göstergesi değil. KONTR 17.06.2026 sıfır satır; 21.05.2026 (THYAO, KONTR, SMRTG) ve 16.09.2026 (EUPWR, SMRTG) min=max=kapanış ama AOF farklı/aralık dışı. THYAO 2000–2026: AOF aralık dışı 4, kapanış aralık dışı 37, sıfırlı satır 38. Kilitli günlerde AOF = MIN = kapanış. Tavan kapanışlı ama MIN<MAX gün sayısı kilitlilerin 3–8 katı (EUPWR 48, SMRTG 73, KONTR 126).
3. V3: Uç nokta 2000'e kadar veriyor (THYAO 6.684 satır, 04.01.2000–02.10.2026); 2005–2014 aralığı 2.509 satır.
4. V4: Eksik gün = gerçek tatil/kapalı gün (hafta içi 295 eksik; 08, 09, 10, 13, 14 Şubat 2023 yok; hafta sonu satırı yok). Durdurma/kapanma sıfır satırdır (HACIM=AOF=MIN=MAX=0, kapanış taşınır; ASYAB 20–25.07.2016, KONTR 17.06.2026).
5. V5: THYAO İş 2.947 satır = borsapy aynı 2.947 gün (+ 05.10.2026 yarım çubuk). Getiri farkı > 0,5 puan: 2.946 günde 3. HGDG/HG son günde 1,0. XU100 İş'te boş; borsapy'de 3.650 satır.
6. V6: borsapy bugünkü çubuğu 09:00 damgalı yarım veriyle veriyor; İş'te 11:12'de son satır 02.10.2026. borsapy `Open` sütunu var.
7. V7: `HisseTekil` `XU100` için sessizce `[]` döndürür.
8. V8: 12.03.2020: ECILC +%13,03 (11.03 +%19,82), RYSAS −%19,86; ±%20 hâlâ geçerli. 13.03.2020 seansında ±%10 (ECILC −%9,98, RYSAS tavan 5,01 = 4,56 × 1,10). 5.1'deki karantina örneği yanlış.
9. V9: PD = HG_KAPANIS × SERMAYE; CCOLA bedelsiz gününde SERMAYE aynı gün güncellendi, PD sıçramadı. `SHHE_FIYAT_AYAR_OR` 0,0909 = HGDG oran adımı.
10. V10: TCMB serisi hâlâ 23.01.2026'da bitiyor (37,0, 57 satır); tablo tarihi toplantıdan 1 gün sonra; `END_TARIH` epoch 21:00 UTC = İstanbul gece yarısı; 14 istekte 2 zaman aşımı, engel yok.

**En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği**

1. 01-053 (YANLIŞ) — 5.1'deki ECILC/RYSAS 12.03.2020 örneğini kaldır ya da ±%10 olsaydı diye yaz; gerçek vaka olarak 13.03.2020 geçişini ve ±%20/±%10 sınırını kullan.
2. 01-029, 01-026, 01-027 (EKSİK) — 5.3 kilitli tanımını değiştir: kilitli = MIN==MAX ∧ HACIM>0 ∧ getiri limitte (limit − 1 adım). Kapanışı tavan/taban olan günde giriş yok/çıkış kayar (muhafazakâr); iyimser sürüm duyarlılık.
3. 01-031, 01-015, 01-007 (EKSİK) — 5.1'e veri doğrulama kuralları: MIN ≤ AOF ≤ MAX, MIN ≤ kapanış ≤ MAX, HACIM=0 satırı NaN (durdurma), HACIM>0 ⇒ AOF>0; ihlal karantina. 2026 satırlarında tutarsızlık var (V2).
4. 01-063, 01-062 (OLGU, kapatma) — 5.1 ve Açık soru: "HACIM TL (doğrulandı), HGDG_HACIM = HG_HACIM"; fiyat × lot adımı silinir.
5. 01-087, 01-088 (YANLIŞ) — 5.6'yı "borsapy politika faizi, ileri doldurma, 2015–2026 tek seri" yap; EVDS/TLREF kaldır. Serinin yaşı tazelik kontrolüne girer (01-089); günlük nakit getirisi için 1 gün gecikme (01-091).
6. 01-094, 01-098, 01-095 (EKSİK) — Bölüm 4 "Veri deposu": anlık görüntü = fiyat (ham+HGDG) + olay tablosu + evren + faiz + takvim, manifest + SHA-256, TAM/KISMİ durumu, aktif/iptal durumu.
7. 01-100, 01-051 (EKSİK) — Yeni 5.13 "Veri kapıları": karantina hisse-gün oranı, sıfır/aralık dışı satır oranı, uyuşmazlık günü oranı için sayısal üst sınırlar; getiri görülmeden yazılır, 5.8 kayıt hash'ine girer.
8. 01-018, 01-019 (EKSİK) — 5.8: 2014 verisi ısınma için indirilir (uç nokta 2000'e kadar veriyor); 02.01–27.11.2015 yalnız ısınma, işlem 30.11.2015'ten; gösterge penceresi dolmadan sinyal yok (01-069).
9. 01-078, 01-079, 01-080 (EKSİK) — Göstergeler = HGDG; kendi çarpanımız yalnız denetim (fark varsa HGDG kazanır). Kartta ham seviye = HGDG seviyesi × (HG_t / HGDG_t), her gün yeniden yazılır.
10. 01-049, 01-047, 01-040 (EKSİK) — 5.1 çapraz kontrol: HG/borsapy oran adımı olay tablosuna bağımsız yedek olsun; kod 04 günlerinde temettü verimi çıkarılarak karşılaştır; bilinmeyen kod HGDG oran adımıyla tanınsın.

Aşağıdakiler de önemli ama ilk 10 dışında kaldı: 01-070/071 (kapanmış hissede çıkış kuralı), 01-034 (borsapy `Open` ile stop boşluk dolumu), 01-084 (5.4 "açılışta kovalama" ifadesi), 01-048 (karantina penceresi), 01-097 (bugünkü bar çapraz kontrolü).
