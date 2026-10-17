# C — Harmonik ve Geometrik Formasyon Kuralları (Tansu)

Durum: araştırma çıktısı. Kod yazılmadı. Tarih: 2026-10-05.

## 0. Okuma kuralları

Klasör: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\` (kısaltma: `HAVUZ`).
Görsel klasörü: `HAVUZ\assets\<klasör>\`. Not dosyası: `HAVUZ\<not>.md`.

Güven etiketleri: birinci el, ikinci el ve YORUM tanımları GLOSSARY'dedir. Bu dosyada ek etiket: **ölçüm** = görsel etiketlerinden veya pikselden hesaplanan değer (hata payı var). Bu dosyada `Ham` etiketi, notun `## Ham` bölümüne gider (GLOSSARY "Kaynak"). Notların Sentez ve Cevo çıkarımı gibi bölümleri Claude özetidir (ikinci el).

Not: YORUM: bu katalogda ekranlar Tansu'ya atfedilen araç çıktıları olarak okunur; üretici ve bütün iç yöntemler doğrulanmış değildir (Araç, G01–G02; Ham, G02:27). Kod veya ham veri yok. Hiçbir görselde işlem maliyeti veya ham OHLC görünmüyor. Pivot parametresi yalnız `gorsel-paket-60` etiketinde görünür: `Swing=15 sol-only | MinGap=15` (B §9). Harmonik tarayıcı görsellerinde yoktur.

Önemli not (Tansu tablosunun içindeki yön hatası):

1. `gorsel-paket-123` tablosundaki D formülü (`X + (A−X)*0.786`, "Boğa için") bullish yapıda yönü yanlış. Tablonun kendi TP formülleri (`D+(A−D)*...`) D'nin A'nın altında olduğunu varsayıyor. Bkz. kural 7.

---

## 1. Swing-pivot tespiti (tüm kuralların temeli)

- Kaynak: `gorsel-paket-01` (görsel 03), `gorsel-paket-03` (görsel 01), `kaynak-doas-kelebek` (doas-kelebek.webp), `gorsel-paket-60-hidden-bullish-divergence` (görsel 01), `gorsel-paket-34` ve `-45` (başlıklar). Notlar: `tweet-abcd-geometrik-gecerlilik-kurallari`, `gorsel-paket-39`, `tweet-trend-cizgisi-swing-pivot-regresyon-zarf`.
- Tansu'nun ifadesi (birinci el, görsel etiketleri):
  - Lejant (KRPLS, SMRTG): `Swing Low` (mavi ▲), `Swing High` (turuncu ▼), `Swing Yapısı (HH/HL/LH/LL)`, `Swing (X -> A)`, `AB=CD Paterni`.
  - Gizli pozitif uyumsuzluk aracının üst etiketi: B §9'dadır. (bilet 04, 14.10)
  - Düşen direnç taramasının başlıkları (`Kırılım`, `Temas`, `Lookback`): A §3'tedir.
- Tanım (görselden okunan davranış):
  1. İki ölçek var. Küçük ölçek: mum üstünde mavi ▲ (Swing Low) ve turuncu ▼ (Swing High) işaretleri. Büyük ölçek: kalın zikzak çizgi `Swing (X -> A)`. Zikzak köşeleri küçük işaretlerden azdır. Yani zikzak daha geniş bir eşikle üretiliyor. (ölçüm)
  2. Her zikzak köşesinin üstünde veya altında bir yapı etiketi var: `HH`, `HL`, `LH`, `LL`. Etiket, köşenin aynı türdeki önceki köşeye göre yüksek mi alçak mı olduğunu gösteriyor. DOAS örneği: X=`HL`, A=`LH`, B=`HL` (178,45 > X 170,10), C=`LH` (C < A 209,10). Bu okuma tutarlı. (ölçüm)
  3. Bir köşe birden fazla pattern'e hizmet edebiliyor. KRPLS'de Mayıs tepesinde `LH / C / B / A` yığını var. SMRTG'de `H/B/A`, `LH/C/A`. Bu, tarayıcının ardışık üç köşeyi (A,B,C) kaydırarak pattern aradığını gösteriyor. Aynı köşe farklı pattern'lerde A, B veya C olabiliyor. (ölçüm, YORUM)
  4. `MARKA - Patern #13` başlığı: pattern'lere sıra numarası veriliyor. Numara muhtemelen listedeki sırası. (YORUM)
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Swing penceresi ve MinGap (diverjans aracı) | B §9 | B §9; harmonik tarayıcıya ait olduğu KANITLANMADI |
| Lookback ve temas sayısı (düşen direnç tarayıcısı) | A §3 | A §3 |
| Harmonik tarayıcının pivot penceresi L/R | bilinmiyor | YORUM |
| Zikzak eşiği (yüzde, ATR) | bilinmiyor | YORUM |

- Giriş / stop / hedef: yok (altyapı kuralı).
- Belirsiz kalanlar:
  - Bizim `sol-only` pivot seçimi (YORUM): B §9 madde 4.
  - `Swing=15`'in sayı birimi bar mı? Zaman dilimi? Bilinmiyor.
  - Harmonik tarayıcı aynı `Swing=15`'i mi kullanıyor? Görselden çıkmıyor.
  - Notlardaki `L/R` pencereli formül (`pivot_known_at = i + R`, alternatif high/low, min bar mesafesi, ATR belirginliği) Claude'un şablonudur. Tansu'nun kaynak metni sadece "peş peşe gelen lokal tepe ve dip noktaları tespit edilir" diyor, parametre vermiyor (`gorsel-paket-39`, Ham).
- Tansu'nun kanıtı: yok (altyapı).
- Günlük bedava veriyle uygulanabilir mi: evet, pivot hesabı OHLC ister. Ama parametreler (L, R, eşik) sizin kararınız. Kendi kuralınızı seçin ve `pivot_known_at = i + R` ile geleceği sızdırmayın. (YORUM)
- Kaynak güveni: birinci el (etiketler), ikinci el (L/R şablonu).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-swing-pivot-oteleme-backtest-2093465820932235288` — BOM sinyalinin backtest modülünde pivotun gerçekten swing low olduğundan emin olmak için pivot X bar ötelenir (pivot teyit gecikmesi, ileri bakma sızıntısını önler): "noktanin gerçekten swing lowpivot olduğundan emin olmak için X bar kadar öteleyerek kodladım" (Ham). X değeri yok; Tansu hafta sonu ayrıntılı bakacağını söyler, sonuç yok. Görselde HVN, Gaussian Fit, HH, BOS, D-HL, BOM etiketleri var (görsel metni). YORUM: bölümdeki `pivot_known_at = i + R` fikriyle aynıdır; R değeri belli değil; BOM kuralı A §16'da tanımsız kalır.
  - `tweet-zigzag-atr-gridsearch-secimi-1908636901365407759` — Zikzak eşiğinin türü: Tansu zikzak sistemini ATR ile kurar ve ATR periyodunu hisse bazında gridsearch ile seçer. "Artık PnL ya da profit factor'e göre tercihimi yapıyorum." (Ham). Döküm (görsel, açıldı): sütunlar Symbol, ATR_Period, Total_PnL, Win_Rate (%), Profit_Factor, Trades; ATR periyotları 5–34; işlem sayısı 3–12 (küçük örneklem); en düşük PF 3,0 (YORUM: PF ≥ 3 süzgeci, E K19 ile uyumlu); Symbol sütunu boş, döküm hangi hisseye ait belli değil. Görsel 1: mum grafiği, siyah zikzak çizgisi, yeşil ▲ ve kırmızı ▼ işaretleri (görsel, açıldı). Zikzak eşiğinin ATR çarpanı, arama aralığının adımı ve örneklem dışı doğrulama yok. Hisse bazlı optimizasyon: karar Levent'te bekliyor (E K29). Parametre: Zikzak eşiği = ATR tabanlı; ATR periyodu hisse bazında gridsearch ile seçilir, görülen aralık 5–34; seçim ölçütü PnL veya profit factor (Ham; görsel, açıldı)

---

## 2. Pattern durum etiketleri ve tarayıcı çıktı tablosu

- Kaynak: `gorsel-paket-01` (görsel 01, 03, 05, 06, 09), `gorsel-paket-02` (görsel 01, 02), `gorsel-paket-03` (görsel 01), `tweet-harmonik-xb-trend-kirilimi-stratejisi` (KAPLM görseli).
- Tansu'nun ifadesi (birinci el):
  - Tablo başlığı: `Hisse | Tip | Sistem | Durum | Reaksiyon | D Hedefi | Giriş | Stop (X)`.
  - SOKE satırı: Tip `SAT (taktik KISA, D'ye kadar) — D'de AL'a döner`, Sistem `Pesavento` ve `Carney` (iki ayrı satır), Durum `AKTIF`, Reaksiyon `-`, D Hedefi `12.53`, Giriş `-`, Stop `-`.
  - LUKSK satırı: Tip `AL (Buy)`, Sistem `Pesavento` ve `Carney`, Durum `TAMAMLANDI`, Reaksiyon `TEPKI_VERDI`, D Hedefi `86.95`, Giriş `86.95`, Stop (X) `73.00`.
  - Grafik etiketleri: `D: 226,80 [TAMAMLANDI]`, `D: 11.20 [TAMAMLANDI]`, `D (hedef: 11.29 [TAMAM])`, `D (hedef: 10.05 [TAMAM])`, `D (hedef: 7.83 [BOZULDU])`, `D: 49.66 [AKTİF]`, `D (hedef) 70.25` (Backtest Modu).
  - KAPLM üst notu (okunabilen kısım): `D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ) | [Ek bilgi] C sonrası fiyat son 10 günde BEKLENEN yönde: DÜŞÜYOR (Bullish/AL paternde CD bacağı aşağı olmalı...`. Cümlenin sonu kesik.
  - Başlık biçimi: `KAPLM.IS - Eşleşen Patern (Bullish) [TAMAMLANDI]`; `DGATE.IS - Kelebek Formasyonu (AL (Buy)) [AKTİF] — SİSTEM: Pesavento — Tarama eşleşmesi`.
- Tanım (etiketlerin anlamı, görselden ve tutarlılıktan çıkarım):

| etiket | anlam | kanıt |
| --- | --- | --- |
| `AKTIF` / `[AKTİF]` | D henüz oluşmadı. D hedefi bir projeksiyon. | DGATE: D 49,66 fiyatın çok altında. SOKE: Giriş ve Stop boş. |
| `TAMAMLANDI` / `[TAMAM]` | Fiyat D hedefine ulaştı. | DOAS: D 159,40 hedef 159,49'a yakın. KRPLS: D'ler aşılmış. |
| `BOZULDU` | Pattern geçersiz oldu. D hedefi iptal. | SMRTG, KRPLS: gri etiket, gri noktalı çizgi. Sebep görselde yok. |
| `TEPKI_VERDI` | Reaksiyon sütunu: D sonrası beklenen yönde tepki oldu; formasyon durumundan ayrıdır. | Araç, G02/g1 ve G03/g1; eşik verilmez. |
| `TEPKİ GELMEDİ` / `BELİRSİZLEŞTİ` | Reaksiyon alanı: KAPLM'de 20 bar tepki yok; ayrıca son 10 günde belirsizleşme var. | Araç, KAPLM üst notu; ortak politika açık değil. |
| `Backtest Modu` | Eski bir C anına dönülüp pattern'in sonrası izleniyor. | MARKA başlığı, SMRTG "Tarih (C)" sütunu. (YORUM) |

- Giriş / stop / hedef: LUKSK için Giriş = D hedefi (86,95), Stop (X) = X fiyatı (73,00). SOKE aktif satırında giriş ve stop boş. Durum, Reaksiyon, Giriş ve Stop ayrı alanlardır (Araç, G02/g1). YORUM: limit giriş okuması bizim seçimimizdir; alanlar emir türünü açıklamaz.
- Belirsiz kalanlar:
  - `BOZULDU` tetikleyicisi görselde yok. Tek aday: C'den sonra fiyatın A'yı aşması (kural 3, Ham; etiketle ilişkisi YORUM).
  - `TEPKI_VERDI` için minimum hareket yüzdesi ve süre yok.
  - `Pesavento` ve `Carney` iki ayrı sistem etiketi. SOKE ve LUKSK'ta aynı D ve aynı giriş çıktı. Hangi oranlar farklı? Bilinmiyor. İsimler, Larry Pesavento ve Scott Carney'in oran setlerine gönderme olabilir (YORUM). Kitap doğrulaması yapılmadı (`900-Archive/Pesavento-Jouflas PDF Derin İnceleme.md`, "parse başlamadı").
  - "SAT (taktik KISA, D'ye kadar) — D'de AL'a döner": bullish Gartley'de D'ye kadar kısa, D'de al. Kısa tetikleyici kural 9'da.
- Tansu'nun kanıtı: etiketli örnekler. Sistematik değil. LUKSK tarayıcı tablosundaki tek tamamlanmış satır.
- Günlük bedava veriyle uygulanabilir mi: evet (etiketler fiyat yolundan türüyor). Eşikler YORUM.
- Kaynak güveni: birinci el (etiketler, tablo). Yaşam döngüsü şeması ikinci el.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ab-cd-fibonacci-uzanti-hedef-bozuldu-2092338381548085291` — KCHOL örneği, 25.08.2026: "KCHOL pili bitti" (Ham). Görsel (görsel, açıldı): başlık "KCHOL - Swing Yapısı, Fibonacci ve AB=CD Analizi (Düşüş)"; dört hedef etiketi: D (hedef) 242.80, 165.40, 165.20 [BOZULDU], 206.40 [TAMAM]; Fibonacci ızgarası 0.000: 182, 1.000: 202, 1.272: 207, 1.618: 214, 2.000: 222 (TAMAM hedefi 206.40 ≈ 1.272 seviyesi). BOZULDU etiketi için YORUM (piksel okuması): A≈215, B≈178, C≈202 ile D = C − (A − B) ≈ 165; fiyat sonra A'nın üstüne çıktı (zirve ≈227), bu §3'ün "C sonrası A aşılırsa bozulur" maddesiyle uyumludur; A≈229 olan 165.40'lık desen A aşılmadığı için BOZULDU yazmaz. Bu, §2'deki tek aday tetikleyiciyi destekler, kanıtlamaz. "Pili bitti" sözü: fiyat 1.618–2.000 uzantısına çıkıp kırmızı mumla döndü (YORUM); giriş, çıkış, stop yok. Başlık "Düşüş" der, TAMAM hedefi ise yukarıdadır: başlık ile yön uyumu belirsiz.

---

## 3. AB=CD geometrik geçerlilik (BC ≤ AB, D, B'nin ötesinde, A ihlali)

- Kaynak: `tweet-abcd-geometrik-gecerlilik-kurallari` (Ham), `gorsel-paket-39` (görsel 01 ve Ham, birinci el), `-38`, `-40`, `-42`, `-43`, `-45`, `-47`, `gorsel-paket-32`, `-34`, `-35`.
- Tansu'nun ifadesi:
  - Ham'da 4 madde (`tweet-abcd-geometrik-gecerlilik-kurallari`): BC bacağı AB'yi aşamaz; BC tam 1,00 olabilir; D, B'yi aşmalı; C oluştuktan sonra fiyat A'yı geçerse pattern bozuldu sayılır.
  - Yön şablonu (`gorsel-paket-39`, Ham): alış için `Yüksek tepe → Dip → Daha düşük tepe → Daha düşük dip` (A high → B low → C lower high → D lower low). SELL şablonu (`A low → B high → C higher low → D higher high`) Ham'da yok; alışın aynası bizim yorumumuzdur (YORUM).
  - Görsel etiketleri (birinci el): `D (CD=1.0AB)` (AKCNS, 39, 40, 35), `D (ALIM SİNYALİ - CD=1.0AB)` (42), `D (ALIM SİNYALİ - CD=1.27AB)` (RYSAS), `D (CD=1.27AB)` (32, 45, 47), `ABCD (BUY)` (32 lejant).
- Tanım (hesaplanabilir):
  1. Pivotlardan A, B, C seç. Sıra: `A_zaman < B_zaman < C_zaman`.
  2. BUY: A=tepe, B=dip, C=tepe, `B < C <= A`. SELL: A=dip, B=tepe, C=dip, `A <= C < B`.
  3. `AB = |B−A|`, `BC = |C−B|`, `q = BC/AB`. Geçerli: `0 < q <= 1.00`.
  4. D projeksiyonu: `D = C + r*(B−A)`. Burada r = CD/AB. Görsel etiketlerinde r = 1,0 ve 1,27.
  5. D, B'nin ötesinde olmalı: `r > q`. (not'un türetimi: D = B + (r−q)(B−A))
  6. C sonrası fiyat A'yı aşarsa pattern bozulur.
  7. BUY'da D, B'nin altında. SELL'de D, B'nin üstünde.
- Ölçüm doğrulaması (benim hesabım, görsel etiketlerinden):
  - KRPLS 1: A=7,20 (X?), B=10,25, C=8,22. Hesap: `D = 8,22 + (10,25−7,20) = 11,27`. Görsel `D 11.29 [TAMAM]`. q=0,666. Uyuyor (r=1,0).
  - KRPLS 2: A=8,22, B=9,86, C=8,42. `D = 8,42 + 1,64 = 10,06`. Görsel `10.05 [TAMAM]`. q=0,878. Uyuyor.
  - MARKA #13: A≈95,2, B≈73, C≈92,5. `D = 92,5 − 22,2 = 70,3`. Görsel `D (hedef) 70.25`. q≈0,88. Uyuyor.
  - Not: KRPLS köşe fiyatlarını piksel çizgilerinden okudum. ±0,05 hata olabilir.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| BC/AB üst sınır | 1,00 (dahil) | Ham (`tweet-abcd-geometrik-gecerlilik-kurallari`) |
| BC/AB aday oranları | 0,382 / 0,500 / 0,618 / ... (açık uçlu) | Ham (`gorsel-paket-39`) |
| CD/AB (r) aday oranları | 1,000 / 1,270 / 1,618 / ... (açık uçlu) | Ham (`gorsel-paket-39`); görselde 1,0 ve 1,27 etiketi var |
| D, B'nin ötesinde | `r > q` | not türetimi |
| BC/AB gerçek örnekleri | 0,666 ; 0,878 ; 0,88 | ölçüm (KRPLS, MARKA). Yani 0,618'in üstü kabul ediliyor. |
| Oran toleransı | bilinmiyor | YORUM |
| D için PRZ aralığı | bilinmiyor | YORUM |
| Bozulma bazı (fitil / kapanış) | bilinmiyor | YORUM |

- Giriş / stop / hedef / bozulma: bkz. kural 4 (hedef merdiveni) ve kural 5 (backtest). Bozulma: C sonrası A aşıldı (Ham). Durum etiketi: `BOZULDU` (görsel).
- Belirsiz kalanlar:
  - `CD=1.0AB` ve `CD=1.27AB` aynı tarayıcıda mı? Etiketler iki farklı r değerini gösteriyor. Bir tarayıcı iki r'yi tarıyor olabilir (YORUM).
  - q üst sınırı: 0,878 örneği kabul edilmiş. Alt sınır? Bilinmiyor.
  - Not, BC/AB = 1,00 için r > 1 gerektiğini söylüyor. Görselde q=1 örneği yok.
  - Zaman simetrisi (`CD_bar / AB_bar`): `gorsel-paket-39` Ham'ında yok; Ham yalnız fiyat uzunlukları ve oranları anar. Kural olarak eklenirse YORUM'dur, eşik yok.
- Tansu'nun kanıtı: seçilmiş örnekler (KRPLS, MARKA, AKCNS, 40, 42, RYSAS). Sistematik tek tablo: kural 5.
- Günlük bedava veriyle uygulanabilir mi: evet. Eksik: pivot, tolerans, bozulma bazı.
- Kaynak güveni: etiketler, D formülü ve kural maddeleri birinci el (görsel ve Ham; ölçümle).

---

## 4. AB=CD hedef merdiveni (Hedef 0.618 / 1.000 / 1.618)

- Kaynak: `gorsel-paket-42` (01-buy-abcd-d-yukselen-destek.png), `gorsel-paket-43` (01-rysas-buy-abcd-yukselen-kanal.png).
- Tansu'nun ifadesi (birinci el):
  - RYSAS: `Hedef 0.618 (22.60)`, `Hedef 1.000 (24.20)`, `Hedef 1.618 (26.80)`. Başlık: `RYSAS.IS — Kanal Durumu: KANAL İÇİ NÖTR | Taze D Noktası (Alış) Tespit Edildi!`.
  - Görsel 42: `Hedef 0.618`, `Hedef 1.000`, `Hedef 1.618` (fiyat yazısı okunmuyor). `D (ALIM SİNYALİ - CD=1.0AB)`.
- Tanım (ölçümle doğrulandı):
  - `Hedef(r) = D + r*(A − D)`. D'den A'ya bakılır. r = 0,618 / 1,000 / 1,618.
  - RYSAS doğrulaması: A=24,20 alınca `22,60 = D + 0,618*(24,20−D)` D≈20,01 verir. `26,80 = D + 1,618*(24,20−D)` D≈19,99 verir. İki denklem aynı D'yi (≈20,0) verdi. Yani formül tutarlı. Hedef 1,000 = A seviyesi.
  - Görsel 42'de piksel oranı da aynı: 1,000 çizgisi A'nın seviyesinde.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Hedef oranları | 0,618 ; 1,000 ; 1,618 | görsel (birinci el) |
| Hedef çapası | D'den A'ya doğru | ölçüm (RYSAS aritmetiği) |
| TP seviye sayısı | 3 | görsel |

- Giriş / stop: görselde yok. 42 ve RYSAS'ta "ALIM SİNYALİ" yazıyor ama giriş fiyatı ve stop çizilmemiş.
- Belirsiz kalanlar: hangi hedefte ne kadar pozisyon kapatılır? Stop nerede? Hedef temas mı kapanış mı? Hepsi YORUM.
- Tansu'nun kanıtı: yok (hedefler çizilmiş, sonuç yok). RYSAS "taze D". 42 D'de bitiyor.
- Ek örnek (KANIT, bilet 04, 14.10): `tweet-fibonacci-extension-abcd-kullanimi` (Ham: "FIBO extension'ları öğrenin arkadaşlar ve ABCD ile nasıl kullanılacağını"; görsel birinci el, A1CAP). Görsel okundu: A ≈ 15,3 (Mayıs başı), B ≈ 9,1, C ≈ 12,3; kırmızı noktalı D projeksiyonu ≈ 6'ya iner. Ölçüm (YORUM): `C + 1,0*(B−A)` ≈ 6,1, görselle uyumlu. Yatay Fibonacci merdiveni A–B bacağının değil C'den sonraki bacağın (0,000: 12,30; 1,000: 9,57) uzantısıdır: 1,272 = 8,83; 1,618 = 7,88; 2,000 = 6,84 (görsel, küçük yazı). Bu merdiven bu kuralın 0,618/1,000/1,618 hedef merdiveninden farklı çapa kullanır. Başlıktaki "Harmonik sayı: 6.31 TL" tanımsız. Tek hisse, sonuç yok; notun oran listeleri ve uygulama akışı Claude'a aittir (YORUM).
- Günlük bedava veriyle uygulanabilir mi: evet. Formül tam.
- Kaynak güveni: birinci el.

---

## 5. AB=CD C→D backtest (SMRTG 12, ISKPL 5, MARKA #13)

- Kaynak: `gorsel-paket-03` (02-smrtg-backtest-sonuclari.png), `tweet-iskpl-abcd-cden-dye-backtest` (01-iskpl-abcd-cden-dye-backtest.png), `gorsel-paket-01` (09-marka).
- Tansu'nun ifadesi (birinci el, araç çıktısı):
  - `BACKTEST SONUÇLARI (SMRTG)`: `Toplam patern sayısı : 12`, `Hedefe ULAŞAN : 7`, `Stop'a takılan / bozulan : 3`, `Henüz sonuçlanmamış (açık) : 2`, `Başlangıç sermayesi : 100,000.00 TL`, `Bitiş sermayesi : 405,327.42 TL`, `Toplam getiri : %305.33`.
  - ISKPL: 5 patern, 5 hedef, 0 stop, 0 açık. 100.000 → 710.006,23 TL. `%610.01`.
  - Sütunlar: `# | Tarih (C) | Sonuç | Getiri % | Sermaye`.
  - ISKPL metni (Ham, tweet-iskpl-abcd-cden-dye-backtest:23): "AB=CD 1000 günlük C noktasından alım yapılsa idi D satış karları."
- Tanım (çıktıdan okunan):
   1. C→D fazında giriş C, satış hedefi D'dir; ISKPL Ham'ı C'den alımı anlatır (Ham, tweet-iskpl-abcd-cden-dye-backtest:23). SMRTG backtest görselinde işlem yönü yazmaz; grafik başlığı `(Yükseliş)`, hedef etiketleri karışık yönlüdür (Araç, G03/g1). Aşağı yönlü işlem varsa projenin yalnız alış kapsamı onu karşılamaz (YORUM).
   2. C→D işleminde D satış hedefidir; D sonrası dönüş işleminde D giriş/tamamlanma bölgesidir (Ham, tweet-iskpl-abcd-cden-dye-backtest:23; Araç, G02/g1). Çıktı sonuçları: `hedef`, `stop`, `açık`.
  3. Sermaye: her işlemin getirisi tüm bakiyeye sıralı bileşik uygulanıyor gibi. Doğrulama: ISKPL 100.000 × 1,4698 = 146.980 (görsel 146.981,63). SMRTG 100.000 × 0,7671 = 76.707 (görsel 76.707,20 ✓).
- SMRTG işlemleri (birinci el):

| # | C tarihi | sonuç | getiri % |
| --- | --- | --- | --- |
| 1 | 2024-03-27 | stop | −23,29 |
| 2 | 2024-05-06 | hedef | +36,59 |
| 3 | 2024-07-30 | hedef | +28,93 |
| 4 | 2025-01-31 | hedef | +50,72 |
| 5 | 2025-04-16 | hedef | +47,30 |
| 6 | 2025-08-26 | hedef | +30,61 |
| 7 | 2025-09-15 | stop | −12,10 |
| 8 | 2025-09-22 | hedef | +26,14 |
| 9 | 2025-12-10 | hedef | +24,20 |
| 10 | 2026-01-29 | stop | −24,85 |

  Tabloda 10 satır var. 12 patternden 2'si açık. 7 hedef, 3 stop. Kapalı işlemlerde kazanma 7/10.
- ISKPL işlemleri (birinci el): 2024-04-03 +46,98; 2024-08-13 +56,67; 2025-03-21 +49,90; 2025-06-19 +45,37; 2026-01-21 +41,50.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Giriş noktası | C (tarih sütunu) | görsel |
| Hedef | D (r bilinmiyor) | görsel |
| Stop / bozulma kuralı | bilinmiyor | YORUM |
| Taranan pencere | "1000 günlük" (takvim mi seans mı belli değil) | Ham (tweet-iskpl-abcd-cden-dye-backtest:23) |
| İşlem maliyeti | yok | görsel |
| Pozisyon büyüklüğü | tüm sermaye, sıralı | ölçüm |

- Belirsiz kalanlar:
  - Stop fiyatı. Getiriler −12 ile −25% arası. Stop fiyatı bilinmeden hesaplanamıyor. Aday: A'nın aşılması (YORUM, doğrulanamadı).
  - Hedef getirileri %24–51. D−C mesafesi C fiyatına bölünerek mi hesaplanıyor? Doğrulanamadı.
  - C anında gerçek zamanlı geçerlilik: C pivotu ancak sağ teyit sonrası bilinir. Backtest bunu uyguluyor mu? Bilinmiyor. Look-ahead riski.
  - Aynı anda açık pozisyonlar ve çakışma (SMRTG #7 ve #8 arası 7 gün).
  - Başlıkta `Harmonik sayı: 3.02 TL` (SMRTG) ve `6.31 TL` (A1CAP). Anlamı bilinmiyor.
- Tansu'nun kanıtı: tek hisse, seçilmiş. SMRTG 12 pattern (%58 hedef, kapalılarda %70). ISKPL 5/5. Out-of-sample yok. Maliyet yok. Hisse seçiminin amacı açık değildir; yüksek getiriden seçim açıklaması YORUM'dur, kaynak kuralı değildir (Ham, tweet-iskpl-abcd-cden-dye-backtest:23).
- Günlük bedava veriyle uygulanabilir mi: yapı olarak evet; stop kuralı olmadan birebir tekrar edilemez. SMRTG işlemlerinin yönü görselde yoktur; aşağı yönlü bir işlem varsa alış kapsamına uymaz (YORUM), bu sınır bütün AB=CD ailesine genellenmez (Araç, G03/g1; Ham, tweet-iskpl-abcd-cden-dye-backtest:23).
- Kaynak güveni: birinci el (sayılar). Yorumlar ikinci el.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ab-cd-patern-backtest-sonuclari-2090922221489344704` — SMRTG backtest tablosunun Tansu'nun kendi X gönderisi (2026-08-21) olduğunu doğrular; tablo sayıları aynıdır (12 patern, 7 hedef, 3 stop, 2 açık; 100.000 → 405.327,42 TL; %305,33) (görsel, açıldı). Seçim gerekçesi: SMRTG elinde tutanlara zarar vermiş hisse. "Ama sistemi olan bu bataktan büyük kar ile çıkardı" (Ham). Stop kuralı ve işlem yönü hâlâ yazılı değil.

---

## 6. CD bacağı şiddeti (araştırma sorusu)

- Kaynak: `tweet-abcd-cd-bacagi-siddet-belirleyicileri` (Ham).
- Tansu'nun ifadesi (Ham): "AB=CD patterninde, CD bacağının şiddetini ne belirler? Çok önemlidir güzel para bırakır." Soru. Veri, kural ve sonuç yok.
- Tanım: kural değil, soru. Hipotez adayları (BC oranı, C anında sıkışma, B kırılım gücü, üst zaman trendi) Ham'da yok; notun yapay zekâ bölümünden gelir (ikinci el, YORUM).
- Parametreler: yok.
- Belirsiz kalanlar: hepsi.
- Tansu'nun kanıtı: yok.
- Günlük bedava veriyle uygulanabilir mi: araştırma olarak evet. Kural olarak kodlanamaz.
- Kaynak güveni: Ham yalnız bir soru içerir. Hipotez listesi ikinci el (YORUM). Sıralamada dışarıda.

---

## 7. Gartley (XABCD): oranlar, giriş, stop, TP

- Kaynak: `gorsel-paket-123` (01-gartley-excel-algoritmik-takip-tablosu.png), `gorsel-paket-02` (görsel 01 ve 02), `tweet-gartley-d-tepki-penceresi-10-gun` (SAYAS görseli), `gorsel-paket-122` (MAKIM görseli), `gorsel-paket-32` (lejant).
- Tansu'nun ifadesi (birinci el, 123 tablosu, kelimesi kelimesine):

| Parametre / Adım | Teknik Kural (Fibonacci) | Aksiyon / Sinyal | Excel / Yazılım Mantığı (Örnek) |
| --- | --- | --- | --- |
| X Noktası | Başlangıç Pivotu | Dip (Boğa) veya Tepe (Ayı) tespiti | `MIN(Low, n_period)` veya `MAX(High, n_period)` |
| A Noktası | XA Bacağı Sonu | Karşıt Pivot tespiti | X noktasından sonraki en yüksek/düşük nokta |
| B Noktası Teyidi | XA'nın %61.8'i | Formasyon Takibi Başlar | `ABS(B_Fiyat - (A - (A-X)*0.618)) < Tolerans` |
| C Noktası Teyidi | AB'nin %38.2 - %88.6 arası | Geçerlilik Devam Ediyor | `C_Fiyat > AB_382 VE C_Fiyat < AB_886` |
| D Noktası (GİRİŞ) | XA'nın %78.6'sı | Buy Limit / Sell Limit | `Giriş Fiyatı = X + (A-X) * 0.786 (Boğa için)` |
| Stop Loss (SL) | X Noktası (veya XA 1.13) | Pozisyon Kapat (Invalidation) | `SL = X_Fiyat - ATR*2` |
| Take Profit 1 (TP1) | AD'nin %38.2'si | Pozisyonun %50'sini Kapat | `TP1 = D + (A-D) * 0.382` |
| Take Profit 2 (TP2) | AD'nin %61.8'i | Kalan Pozisyonu Kapat | `TP2 = D + (A-D) * 0.618` |

  - Ek (Ham, `gorsel-paket-123`): tolerans "%3–5" (BIST için Python/Excel); `reward/risk < 1,5` veya stratejiye göre `< 2` ise pattern doğru olsa da işlem reddedilir; D/PRZ = XA 0,786 ile BC 1,272/1,618 uzantısının kesişimi; risk = |D−X|.
  - Tarayıcı tablosu (birinci el, 02): LUKSK satırında Giriş = D hedefi = 86,95, Stop (X) = 73,00. Satırda formasyon adı yok (yalnız `AL (Buy)`); Gartley olarak okumak YORUM'dur.
  - SAYAS detay grafiği başlığı (birinci el): `SAYAS - Patern #2 Detaylı (Fibonacci + Trade Management) | Bullish (LONG) | Sistem: Carney`. Lejant (okunurluk sınırlı): `Giriş (D)`, `İlk Stop (X)`, `TP1 (1:1 R/R)`, `TP2 (.618 AD)` (07.10 okuma düzeltmesi; ilk okuma "Bk Stop", ".618 CD").
- Tanım (bullish, hesaplanabilir; tablo ile düzeltilmiş yön):
  1. X=dip, A=tepe, `X < A`. `XA = A − X`.
  2. B: `AB/XA ≈ 0,618`. `B_beklenen = A − 0,618*XA`.
  3. C: `BC/AB ∈ [0,382 ; 0,886]`. Fiyat olarak `B + 0,382*AB <= C <= B + 0,886*AB`.
  4. D: `D = A − 0,786*XA` (X'ten 0,214 üstte). Tablodaki `X + 0,786*(A−X)` yanlış yönde (bkz. aşağı).
   5. Eğitim tablosu: D'de limit giriş; stop X, XA 1,13 uzantısı (`A − 1,13*XA`) veya `X − 2*ATR`; TP1 = `D + 0,382*(A−D)` (%50), TP2 = `D + 0,618*(A−D)` (kalan). SAYAS'ta TP1 = 1:1 R/R; tek genel TP1 ve stop seçimi açık değildir (Eğitim, G123/g1; Araç, G02/g1 ve SAYAS görseli).
  6. R:R girişte hesaplanır, 1,5 (veya 2) altındaysa işlem yok.
- Yön hatası kanıtı (benim hesabım, ölçüm): X=100, A=200 olsun. Doğru D = 200 − 0,786*100 = 121,4. Tablo formülü: 100 + 78,6 = 178,6. Fark 57,2 birim. Tablonun TP formülleri (`D + (A−D)*r`) D'nin A'nın altında olmasını gerektirir. Yani tablo içinde kendisiyle çelişiyor. Büyük olasılıkla örnek formül hatası (YORUM).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| AB/XA | 0,618 | görsel (tablo) |
| BC/AB | 0,382 – 0,886 | görsel |
| D (XA retracement) | 0,786 | görsel |
| BC uzantısı (D/PRZ) | 1,272 / 1,618 | Ham (`gorsel-paket-123`) |
| CD/BC | 1,13 – 1,618 | not 122 ("yaygın örnek", Claude), Tansu değil |
| Stop | X, veya XA 1,13, veya X − 2*ATR | Eğitim, G123/g1; genel seçim kuralı yok |
| TP1 | AD'nin 0,382'si, pozisyonun %50'si | Eğitim, G123/g1; SAYAS'tan ayrı uygulama |
| TP2 | AD'nin 0,618'i, kalan | görsel |
| SAYAS TP1 / TP2 | 1:1 R/R ; 0,618 AD | görsel (07.10 yeniden okundu) |
| Tolerans | %3–5 | Ham (`gorsel-paket-123`:49). Oran mı, fiyat mı belli değil. |
| Min R:R | 1,5 (veya 2) | Ham (`gorsel-paket-123`) |
| n_period (X için) | bilinmiyor | YORUM |
| ATR periyodu | bilinmiyor | YORUM |

- Giriş / stop / hedef / bozulma / durum: yukarıda. Formasyon durumu: `AKTIF` → `TAMAMLANDI`; `TEPKI_VERDI` ayrı reaksiyon alanıdır (Araç, G02/g1 ve G03/g1). Gartley'de X altı geçersizlik kaynaklıdır (Ham, G109:54–56); derin formasyonlara genellenmez.
- Belirsiz kalanlar:
  - Stop seçenekleri: X, XA 1,13 (`A − 1,13XA = X − 0,13XA`), `X − 2ATR` (Eğitim, G123/g1). LUKSK'ta Stop(X) görülür (Araç, G02/g1); bütün Gartley işlemleri için alternatif seçme kuralı yoktur.
  - TP1: eğitim tablosunda AD×0,382; SAYAS'ta 1:1 R/R (Eğitim, G123/g1; Araç, SAYAS görseli). Tek genel TP1 doğrulanmaz. TP2 SAYAS'ta 0,618 AD, BALAT'ta 0,618 CD'dir.
  - MAKIM "Yükseliş Gartley" etiketi: `X->A: 2.11`, `A->B: -1.43`, `B->C: 0.8x` (son hane mumun arkasında, okunamıyor), `C->D: -1.25`. Fiyat ekseninden B ≈ 16,75 ve C ≈ 17,6 okunur; BC ≈ 0,86 (piksel, yaklaşık; 0,86–0,88). Fiyat farkı okumasında AB/XA = 0,678 ve 0,618'den sapma %9,7; CD/BC ≈ 1,4–1,5 (1,25 / 0,86 ≈ 1,45; ölçüm, yaklaşık). YORUM: yaklaşık %10 tolerans bizim aday seçimimizdir; MAKIM bacakları genel tarayıcı toleransını vermez (Ham, G123:49; Araç, G122/g1).
  - Tolerans oran mı fiyat mı? Tablo formülü fiyat farkını `Tolerans` ile kıyaslıyor. Metin "%3–5" diyor.
- SAYAS Fib okuması ve doğrulama (E K12'den buraya taşındı, bilet 04, 14.10): Fib etiketleri (XA bacağı, büyütülerek okundu, son rakamlar bulanık): 0.000 = 144.25; 0.236 = 115.03; 0.382 = 96.98; 0.5 = 82.41; 0.618 = 67.82; 0.786 = 47.05; 1.000 = 20.65. D = 47,05, X = 20,65, A = 144,25 ile TP1 = 47,05 + 26,40 = 73,45 ve TP2 = 47,05 + 0,618 × 97,20 = 107,12 (benim hesabım; piksel konumlarıyla kontrol edildi). Çizili iki yeşil noktalı çizgi ≈73 ve ≈107'dedir; TP 0,382 AD (≈84,2) çizilmemiş. Yani SAYAS'ta TP1 = 1:1 R/R doğrulandı. SAYAS'ta D = fib 0,786 çizgisidir (A'dan aşağı 0,786 ölçülmüş); Excel örneğindeki bullish D = X + (A−X)×0,786 ifadesi bu yüzden örnek yazımda ters (yukarıdaki yön hatası kanıtı).
- Tansu'nun kanıtı: LUKSK (TEPKI_VERDI; satırda formasyon adı yok, Gartley okuması YORUM), SOKE (aktif), SAYAS (uzun grafik). Başarı oranı yok. SAYAS'ta fiyat D'den sonra uzun süre yatay, TP'lere gitmemiş görünür (2023–2026; ~47 üstünde dolaşır, 73'e yakın bir tepe var; sonuç etiketi yok), Tansu'nun "Gartley her zaman çalışmaz" mesajıyla uyumlu (E K12'den taşındı, bilet 04).
- Günlük bedava veriyle uygulanabilir mi: evet. En iyi tanımlı harmonik kural seti (oranlar, giriş, stop, TP). Tolerans ve pivot kararı gerekir.
- Kaynak güveni: tablo, tolerans ve R:R birinci el (görsel ve Ham).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-gartley-fibonacci-oranlari-prz-rr-1995826149021110275` — Tansu'nun kendi gönderisinde Gartley kural seti ve Excel tablosu (tekrar; §7'deki Eğitim tablosuyla aynı içerik). Ham: PRZ "XA 0.786 ile BC uzantısının kesiştiği dar bir fiyat aralığıdır"; "Kural: Eğer Ödül / Risk < 1.5 ise (veya stratejinize göre 2), formasyon teknik olarak doğru olsa bile işleme girilmez"; BIST için %3-%5 tolerans önerisi; risk = |D − X| (Ham). Görselde stop satırının Excel mantığı: "SL = X_Fiyat (veya X - ATR*2)" (görsel, açıldı). Ham: "Verelim mi şimdi bu akşam bir gartley..." (sonuç yok). Parametre: Stop (Excel mantığı) = X veya X − 2×ATR (görsel, açıldı); A noktası = X'ten sonraki en yüksek/düşük nokta (görsel, açıldı); tolerans = %3–5 (Ham); min R:R = 1,5 veya 2 (Ham)
  - `tweet-harmonik-0-4-fibonacci-oranlari-1952841278686937489` — Tansu'nun koda dökmek isteyene verdiği 0-4 şeması (yanıt gönderisi): nokta 4, 0→1 hamlesinin "0.786" geri alımındadır; nokta 3, 1→2 bacağının "0.382 or 0.886" geri alımındadır; nokta 4, 2→3 bacağının "1.272 or 1.618" uzantısındadır (görsel, açıldı). Ham: "Buna göre yazarsınız kodunuzu". Eşleme 0=X, 1=A, 2=B, 3=C, 4=D (YORUM); §7'deki BC/AB, BC uzantısı ve D oranlarıyla aynıdır. "or" iki uç mu, iki ayrı değer mi belli değil (YORUM); 0,618 (AB/XA) şemada yok. Parametre: BC/AB = 0,382 veya 0,886; D = BC uzantısı 1,272 veya 1,618; D = XA 0,786 (görsel, açıldı; nokta eşlemesi YORUM)
  - `tweet-harmonik-ad-fibonacci-kar-alma-1999959077716394236` — TP kuralı Tansu'nun kendi yanıtında sözle: "kâr alma (TP) hedeflerini belirlemek için Fibonacci A noktasından D noktasına çekilir." TP1 = A-D hareketinin 0,382'si, TP2 = 0,618'i (Ham). §7'nin Eğitim tablosuyla (TP1 = D + (A−D)×0,382; TP2 = D + (A−D)×0,618) uyumlu; standart Fibonacci aracında 0 = D'dir (YORUM). Formasyon türü ve pozisyon payı (%50 / kalan) bu gönderide yok. Parametre: TP1 = A–D hareketinin 0,382'si; TP2 = A–D hareketinin 0,618'i (Ham)

---

## 8. Kelebek (Butterfly)

- Kaynak: `kaynak-doas-kelebek-2096505383955079277` (doas-kelebek.webp, tweet: The_Tansu_/status/2096505383955079277, 2026-09-06), `gorsel-paket-01` (06-dgate-kelebek-al-aktif.jpg), `tweet-alark-125-42` (metin).
- Tansu'nun ifadesi:
  - DOAS tweeti (Ham, tweet metni birebir: "kelebeklerrrrr #doas") ve grafik etiketleri (birinci el): `0.0 (A): 209.10`, `0.236: 199.90`, `0.382: 194.20`, `0.500: 189.60`, `0.618: 185.00`, `0.786: 178.45`, `1.0 (X): 170.10`, `1.272 (D hedefi): 159.49`, `1.618 (max risk): 146.00`, `D: 159.40 [TAMAMLANDI]`.
  - DGATE (birinci el): `Kelebek Formasyonu (AL (Buy)) [AKTİF] — SİSTEM: Pesavento`, alt yazı `X→B trend çizgisi: Kırılım: AŞAĞI yönde, 2026-08-18 tarihinde`, `D: 49.66 [AKTİF]`.
  - ALARK (Ham, tweet-alark-125-42): bearish butterfly yapıya gidiyor; strateji 125,42'ye kadar long fırsatı uyarısı verdi; pullback izlenecek. Oran yok.
- Tanım (DOAS'tan okunan, ölçüm):
  - Fibonacci merdiveni XA üzerinde. A = 0, X = 1,0. Seviye(r) = `A − r*(A−X)`.
  - B, 0,786 çizgisinde: 178,45 (AB/XA = 0,786).
  - D hedefi = 1,272 XA uzantısı: `209,10 − 1,272*39,00 = 159,49` ✓. D (159,40), X'in altında.
  - 1,618 seviyesi `max risk` olarak etiketli (146,00). `209,10 − 1,618*39,00 = 146,00` ✓.
  - C pikselden ≈197,9. BC/AB ≈ 0,64. CD/BC ≈ 1,98. (ölçüm, ±0,03)
  - Bullish Butterfly: D, X'in altında. D = 1,272 XA.
- Çelişki (ölçüm): DGATE görselinde Fibonacci çizgileri XA üzerinde (0,236 / 0,382 / 0,5 / 0,618 / 0,786 / 1,0 piksel oranlarıyla uyuyor) ve D 1,273 XA'da (49,66). Ama B noktası pikselden ≈0,55 XA'da. DOAS'ta B = 0,786. Aynı "Kelebek" etiketi iki B oranı gösteriyor. Tarayıcının B toleransı geniş olabilir veya Pesavento Kelebek'i farklı bir B aralığı kullanıyor (YORUM). Ölçüm hatası ±0,03.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| AB/XA (DOAS) | 0,786 | görsel (birinci el, çizgi) |
| AB/XA (DGATE) | ≈0,55 | ölçüm. Çelişki. |
| D (XA uzantısı) | 1,272 | görsel (DOAS, DGATE ölçüm) |
| "max risk" | 1,618 XA | görsel (DOAS) |
| BC/AB | ≈0,64 (DOAS ölçüm) | ölçüm |
| Oran toleransı | bilinmiyor | YORUM |

- Giriş / stop / hedef: DOAS'ta D'ye fiyat girince `[TAMAMLANDI]`. `1,618 (max risk)` çizgisi stop adayı gibi, ama doğrulanmadı (not da aynı diyor, ikinci el). Hedef: görsel yok.
- Belirsiz kalanlar: BC/AB aralığı, CD/BC aralığı, stop kuralı, tamamlanma eşiği (159,40 vs 159,49: 0,09 fark, "tamamlandı" dokunuşla mı?), B toleransı.
- Tansu'nun kanıtı: DOAS (D'de yeşil mum, devamı yok), DGATE (aktif). Sonuç yok.
- Günlük bedava veriyle uygulanabilir mi: kısmen; D = 1,272 XA ve DOAS örneğinde B ≈ 0,786 vardır. DGATE B konumu farklıdır; genel B kabul aralığı ve 1,618 "max risk" çizgisinin emir stopu olup olmadığı açık değildir (Araç, DOAS `01-doas-kelebek.png`; G01/g6). Diğer oranlar ve toleranslar YORUM'dur.
- Kaynak güveni: DOAS seviyeleri birinci el. ALARK birinci el (Ham), ama oran vermez.

---

## 9. X–B trend çizgisi kırılımı (D'ye kadar taktik pozisyon)

- Kaynak: `tweet-harmonik-xb-trend-kirilimi-stratejisi` (KAPLM, 01-kaplm-xb-trend-kirilimi.jpg), `gorsel-paket-02` (SOKE Carney), `gorsel-paket-01` (DGATE alt yazısı).
- Tansu'nun ifadesi:
  - Ham (`tweet-harmonik-xb-trend-kirilimi-stratejisi`): XB noktasından çizilen trend çizgisi, yapının bullish ya da bearish olmasına göre aşağı ya da yukarı kırılır; duruma göre short ya da long alınır. Hangi yapıda hangi yön ve "D'ye kadar" sınırı Ham'da yok; görselden okunur (aşağıda). Notun "mekanik oran ve giriş kuralları kaynakta verilmedi" sözü ikinci eldir.
  - Görsel (birinci el): SOKE tablosu `SAT (taktik KISA, D'ye kadar) — D'de AL'a döner`. SOKE grafiği lejant `X-B Trend Çizgisi`, grafikte `Trend Kırılımı` yazısı. DGATE: `X→B trend çizgisi: Kırılım: AŞAĞI yönde, 2026-08-18 tarihinde`. KAPLM lejant: `Trend Çizgisi (X->B uzatılmış)`.
- Tanım (hesaplanabilir):
  1. Bullish XABC için çizgi: `X_zaman, X_fiyat` ile `B_zaman, B_fiyat`. `çizgi(t) = X + eğim*(t − t_X)`.
  2. Fiyat çizgiyi aşağı keserse sinyal: `kırılım yönü = AŞAĞI`, tarih kaydedilir (DGATE'de tarih etiketi var).
  3. Faz: D'ye kadar kısa. D'de tepki gelirse long adayı (kural 10).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Çizgi çapaları | X ve B | görsel |
| Kırılım yönü etiketi | AŞAĞI / yukarı (tarihli) | görsel |
| Kırılım bazı | kapanış trend çizgisini aşar | Ham, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21; başka kırılım türlerine genellenmez |
| Tampon (ATR, tick) | bilinmiyor | YORUM |
| Stop, hedef | D hedefi (hedef), stop yok | görsel: SOKE'de Giriş/Stop `-` |

- Giriş / stop / hedef: hedef = D. Giriş ve stop bilinmiyor (SOKE aktif satırında boş).
- Belirsiz kalanlar: tampon, stop, kısa pozisyonun kapanış kuralı, BIST'te açığa satış zorluğu (YORUM; Tansu "taktik kısa" diyor, aracı belli değil). Trend çizgisi kırılımının kapanış bazı kaynaklıdır (Ham, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21).
- Tansu'nun kanıtı: KAPLM tek örnek. Çizgi kırıldı, fiyat ~420'ye düştü (D), tepki gelmedi. Kısa kısmı çalışmış görünüyor ama getiri gösterilmemiş.
- Günlük bedava veriyle uygulanabilir mi: evet. Çizgi hesabı kolay. Trend çizgisini kapanışla aşma kaynaklıdır. Tampon, stop ve kısa pozisyonun kapanış kuralı YORUM.
- Kaynak güveni: etiketler ve kural metni birinci el (görsel ve Ham).

---

## 10. D sonrası tepki penceresi ve "belirsiz" sınıfı (10 gün / 20 bar)

- Kaynak: `tweet-gartley-d-tepki-penceresi-10-gun` (SAYAS), `tweet-harmonik-xb-trend-kirilimi-stratejisi` (KAPLM görseli).
- Tansu'nun ifadesi:
  - Birinci el (KAPLM üst notu): `D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ)`.
  - Ham (`tweet-gartley-d-tepki-penceresi-10-gun`): "10 gün içinde D noktasından bir tepki yapmıyor ise belirsiz bir yapı olarak bakılabilir." Gün biriminin takvim mi seans mı olduğu belirtilmemiş.
- Tanım (en az bilinen, çıkarım):
  1. D tamamlanınca saat başlar.
  2. Pencere içinde beklenen yönde hareket olursa `TEPKI_VERDI`.
   3. KAPLM'de 20 bar içinde `TEPKİ GELMEDİ` ve ayrıca "son 10 günde `BELİRSİZLEŞTİ`" etiketleri vardır; tek süre kuralı değildir (Araç, KAPLM üst notu). Ham D'den itibaren on günlük tepki penceresi anlatır (Ham, tweet-gartley-d-tepki-penceresi-10-gun:21).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Tepki penceresi | 20 bar | görsel (KAPLM) |
| Tepki penceresi | 10 gün | Ham (`tweet-gartley-d-tepki-penceresi-10-gun`) |
| Belirsiz penceresi | "son 10 günde" | görsel (KAPLM) |
| Minimum hareket | bilinmiyor | YORUM |
| Birim (takvim / seans / bar) | bilinmiyor | YORUM |

- Belirsiz kalanlar: Ham'daki on gün D'den başlar (Ham, tweet-gartley-d-tepki-penceresi-10-gun:21); takvim/seans birimi açık değildir. KAPLM'deki 20 bar ve "son 10 gün" ayrı etiketlerdir; ortak politika açıklanmaz (Araç, KAPLM üst notu).
- Tansu'nun kanıtı: yok. Örnekler tek. KAPLM başarısız örnektir (D'de tepki yok); Tansu bunu kendisi paylaştı (E K15'ten taşındı, bilet 04).
- Günlük bedava veriyle uygulanabilir mi: evet. Eşik YORUM.
- Kaynak güveni: 20 bar etiketi ve 10 gün birinci el (görsel ve Ham).

---

## 11. D sonrası TP merdiveni (BALAT Siyah Kuğu): CD retracement

- Kaynak: `gorsel-paket-109` (01-balat-siyah-kugu-harmonik-tp.png).
- Tansu'nun ifadesi (birinci el, grafik): başlık `BALAT.IS - Siyah Kuğu & HEDEFLER`. Etiketler: `TP4 (1.272): 92.98`, `TP3 (C Tepe): 90.50`, `TP2: 87.02`, `TP1: 84.88`, `STOP: 64.00`. Alt paneller: RSI, ADX, MACD. Lejant: `Harmonik`.
  - Metin (Ham, `gorsel-paket-109`; Ham'da yazar yok): TP1 `0,382`'de kısmi kâr ve stop'u girişe çek; TP2 `0,618` güçlü/hacimli aşılırsa trend hedeflerine geç; stop bullish yapılarda X altı, bazı derin pattern'lerde XA `1,13/1,27`. Ham'da TP2 "en güvenilir hedef" diye anılır (kaynak görüşü; E K11'den taşındı, bilet 04).
- Tanım (ölçüm, not'un D çıkarımı ile doğrulandı):
  - `TP(r) = D + r*(C − D)`. TP1: r=0,382; TP2: r=0,618; TP3: r=1,000 (= C); TP4: r=1,272 (veya 1,618).
  - Görselde D yazılı değil. TP1 ve C'den: `D = (84,88 − 0,382*90,50)/0,618 ≈ 81,40`. `CD = 9,10`. Kontrol: `81,40 + 9,10*0,618 = 87,02` ✓; `81,40 + 9,10*1,272 = 92,98` ✓. Aritmetik tutarlı.
   - Stop 64,00 = X (görsel, ilk pivot). Risk ≈ 17,40; TP1 ödülü ≈ 3,48 (0,20 R), TP2 ödülü ≈ 5,62 (0,32 R) (ölçüm). YORUM: bu katalogda kural 7'nin R:R ≥ 1,5 eşiğiyle karşılaştırılır; kaynaklar ortak varyant veya seçim politikası vermez (Ham, G109:35; ilgili araç görselleri).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| TP1 | 0,382 CD, kısmi kâr + stop girişe | görsel (fiyat), Ham (kısmi) |
| TP2 | 0,618 CD: `D+0,618(C−D)` | Ham, G109:35; Araç, g1 |
| TP3 | C noktası | görsel |
| TP4 | 1,272 (Ham: veya 1,618) | görsel (1,272) |
| Stop | 64,00 (≈X) | görsel |
| Kısmi kapatma oranı | bilinmiyor | YORUM (kural 7'de %50, burada yok) |

- Belirsiz kalanlar: pattern oranları (bu kaynakta Siyah Kuğu tanımı yok; bullish aralıklar §26), giriş fiyatı ve tetikleyici, D'de otomatik giriş mi tepki teyidi mi, TP1 sonrası break-even stop'un işlem maliyeti.
- Tansu'nun kanıtı: tek hisse, görsel. Sonuç (fill) yok. Son mumlar D'den yukarı (92'ye yakın, TP4 çizgisine yakın). Seçilmiş olabilir.
- Günlük bedava veriyle uygulanabilir mi: evet. TP formülü tam. Giriş ve pattern tanımı eksik.
- Kaynak güveni: etiketler ve metin birinci el (görsel ve Ham).

---

## 12. Trident: D = (B × C) / A, B kırılımı

- Kaynak: `gorsel-paket-47` (01-abc-b-kirilimi-trident-d.png).
- Tansu'nun ifadesi:
  - Görsel (birinci el): A (dip), B (tepe), C (daha yüksek dip), kırmızı kutu, `B Kırılımı` (mavi noktalı yatay çizgi), `D (CD=1.27AB)`. D'den sonra yatay/geri çekilme.
   - Metin: `D = (B × C) / A` (Ham, G47:20). Tansu bunu Charles Lindsay'in 1976 tarihli Trident kitabındaki formül olarak anar; bu atıf bağımsız doğrulanmış değildir. Ham satırın sonunda başka kişinin teşekkür/yanıt metni karışmıştır; tamamı Tansu sözü değildir.
- Tanım (hesaplanabilir):
   1. Formül `D = B*C/A`, A, B, C > 0; eşdeğeri `D/C = B/A`dır (Ham, G47:20). Tansu görseldeki kuralı bu formül olarak anar; görselin etiketi `CD=1.27AB`dir ve ikisinin aynı D'yi verdiği doğrulanamaz (Araç, g1).
  2. B kırılımı: C'den sonra kapanış B'yi geçerse (D yönünde) "devam" tetikleyicisi. D'yi hesaplamak için gerekli değil.
  3. Üç strateji (Ham, G47:20): (a) alış yönlü ABC taranır, teorik D'den (dipten) pozisyon alınır; (b) satış yönlü ABC taranır, D'ye kadar kısa vadeli yükseliş kovalanır, D'yi teyit için B kırılımı gerekir; (c) ABCD taranır, D dibinden sonra Fibonacci iz-süren takiple TP kovalanır.
- Ölçüm kontrolü: Görselde D etiketi `CD=1.27AB`. Trident formülü ise oransal. Aynı A/B/C için iki formül farklı D verir (`D_trident − D_additive(r=1) = (B−A)(C/A − 1)`). Tansu görseldeki kuralı Trident formülü diye anar (Ham, G47:20); hangi formülün görseldeki D'yi ürettiği ölçümle doğrulanamaz. A/B/C fiyat değerleri yok.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| D formülü | (B × C) / A | Ham, G47:20; görsel etiketi `CD=1.27AB` ile ilişkisi doğrulanamaz |
| Görsel D etiketi | CD=1.27AB | görsel |
| B kırılım tampon / bazı | bilinmiyor | YORUM |
| Trailing yöntemi | bilinmiyor | YORUM |

- Belirsiz kalanlar: formül ile `CD=1.27AB` etiketi çelişebilir. Stop yok. Pre-D ve post-D işlemlerin ayrı kuralları yok.
- Tansu'nun kanıtı: tek görsel örnek.
- Günlük bedava veriyle uygulanabilir mi: formül evet. İşlem kuralları hayır.
- Kaynak güveni: etiketler ve formül birinci el (görsel ve Ham). Lindsay/1976 atfı doğrulanmamıştır.

---

## 13. Harmonik + talep bölgesi + düşen direnç kırılımı + Fibo (tarayıcı birleşimi)

- Kaynak: `gorsel-paket-32` (01-gartley-abcd-talep-dusen-kirilimi.jpg), `-34` (01-lider-siyah-kugu-talep-run.png), `-35` (01-beyaz-kugu-sell-abcd-dusen-kirilimi.png), `-38` (AKCNS haftalık), `-40` (haftalık), `-42`, `-43`, `-45`, `tweet-haftalik-bullish-gartley-talep-alani-tarama`, `tweet-formasyon-arz-talep-confluence-kapisi`.
- Tansu'nun ifadesi:
  - Birinci el (başlıklar): LIDER ve BALAT başlıkları A §3'tedir (temas, lookback, kırılım tarihi, lejant). `AKCNS | HAFTALIK ABCD FORMASYONU + Talep + EMA | Fiyat: 213.60`. Lejant (32): `Fiyat, EMA5, EMA8, EMA13, Direnç TL, ABCD (BUY), Harmonik (Gartley), Hacim, Kum. Delta`.
  - Metin alıntıları (Ham; Ham'da yazar yok):
    - 34: "Kuğuyu bir de talep toplama bölgesinde yakalarsanız böyle RUN! olur grafiğiniz."
    - 35: "Düşeni kırmış, sell yönlü abcd'yi tamamlamışi beyaz kuğu da oluşmuş, eh bunu yolculamayalım mı şimdi..."
    - 38: "Not alın işte süper brir yapı..."
    - 40: "ABCD yi görüyor musun tam talep toplama bölgesinden haftalıkta tepkisini almış kütür kütür gitmiş. İşte bu yapıların peşindeyiz."
    - 43: "Şimdi gözü kapalı ABCD'ye nasıl güveneceksin kanalı okumadan iş yapılır mı?"
    - 45: "Abcd analizine güvenip çaat diye alırsan küüt diye böyle olursun. Her zaman çalışmaz. İkinci alt grafiğe dikkat."
    - Haftalık tarama isteği (Ham, `tweet-haftalik-bullish-gartley...`): C noktası uzun vadeli talep toplama alanında oluşmuş, XABC tamam, D hedefi hesaplanmış bullish Gartley.
- Tanım (kombinasyon, çok katmanlı filtre):
  1. Harmonik veya AB=CD geometrisi (kural 3, 7, 8).
  2. Talep bölgesi (yeşil kutu): D veya C bu bölgenin içinde (BUY, 38/40 görsellerinde D bölge içinde). 39 SELL görselinde D bölgede değil, D sonrası düşüşte bölgeye iniyor.
  3. Düşen direnç çizgisi kırılımı (başlık değerleri ve parametreler: A §3).
  4. Fibonacci merdiveni (D çevresi).
  5. EMA5/8/13 toparlanması, hacim, kümülatif delta (katılım).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Çizgi temas sayısı ve lookback (LIDER, BALAT) | A §3 | A §3 |
| EMA'lar | 5, 8, 13 (lejant / başlık) | görsel (32, 45), 38 pencereleri okunmadı |
| Talep bölgesi üretimi | bilinmiyor (proximal / distal, taze mi) | YORUM |
| Haftalık / günlük | AKCNS ve 40 haftalık; diğerleri belirtilmemiş | görsel |
| Kümülatif delta hesabı | bilinmiyor (gerçek tick yok, BIST'te proxy olabilir) | YORUM |

- Giriş / stop / hedef / bozulma: yok. Başlıklarda emir seviyesi yok; "ALIM SİNYALİ" yalnız 42 ve 43'te D etiketinde yazar (`D (ALIM SİNYALİ - CD=1.0AB)`), başlıkta değil. Bozulma: not (ikinci el) talep bölgesi altı kapanış ve D risk seviyesi öneriyor, Tansu'dan söz yok.
- Belirsiz kalanlar:
  - Bu birleşik tarayıcının "geçti" eşiği (hangi katmanlar zorunlu?). LIDER başlığındaki dört katman (Düşen Direnç Kıran + Talep + Fibo + ABCD) zorunlu olabilir (YORUM).
  - BALAT'ta aynı başlık (aynı tarayıcı geçişi) ama sonuç başarısız (kural 14). Yani tarayıcı geçişi tek başına işlem izni değil.
  - Aynı tarayıcıda "Siyah Kuğu" etiketi (LIDER) ve BALAT'ta başlıkta pattern yok. `Harmonik: Siyah Kuğu` her başlıkta yok.
  - Beyaz Kuğu ve Siyah Kuğu oranları bu bölümün kaynaklarında yok (Siyah Kuğu bullish aralıkları 16.10'da §26'ya girdi). Gartley, Butterfly veya başka kural yerine konamaz.
- Tansu'nun kanıtı: seçilmiş pozitif örnekler (LIDER RUN, AKCNS, 40) ve tek negatif örnek (BALAT). Oran yok. Pozitif seçim yanlılığı.
- Günlük bedava veriyle uygulanabilir mi: parça parça evet (çizgi, EMA, hacim). Talep bölgesi ve delta tanımı eksik. Birleşik kural kodlanamaz.
- Kaynak güveni: başlıklar ve metin alıntıları birinci el (görsel ve Ham).

---

## 14. Kanal bağlamı ve negatif delta (başarısız örnek dersi)

- Kaynak: `gorsel-paket-43` (kanal), `gorsel-paket-45` (01-balat-abcd-negatif-kumulatif-delta.jpg).
- Tansu'nun ifadesi (birinci el):
  - RYSAS: başlık `Kanal Durumu: KANAL İÇİ NÖTR | Taze D Noktası (Alış) Tespit Edildi!`. Kırmızı kesikli yükselen üst kanal, yeşil kesikli yükselen alt kanal. D kanal içinde, alt kanal çizgisinin üstünde (D ≈ 20, alt çizgi ≈ 17,5; ölçüm); D'den alt banda inen kırmızı ok var.
  - BALAT: üç panel. Ana grafik EMA5/8/13 + `Direnç TL`. İkinci panel `Volume`. Üçüncü panel `Kum. Delta`. Başlık değerleri, D etiketi ve Fibonacci seviyeleri: A §3. Kümülatif delta uzun süre negatif ve kırmızı barlar büyüyor. Fiyat D'den sonra da düşmeye devam ediyor (görselin sonunda hâlâ 75–76).
  - Metin (Ham): "İkinci alt grafiğe dikkat".
- Tanım:
  - Kanal: üst ve alt çizgi (paralel veya ayrı). `Kanal Durumu` etiketleri: `KANAL İÇİ NÖTR` (diğer etiket değerleri görsellerde yok).
  - Ders: `ABCD_buy_candidate + persistent_negative_delta + falling_price → işlem yok` (not'un çıkarımı, ikinci el; Tansu'nun mesajı "dikkat").
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Kanal çizgileri çapa | bilinmiyor | YORUM |
| Kanal durumu etiketleri | `KANAL İÇİ NÖTR` (tek görülen) | görsel |
| Delta eşiği ("negatif" ne kadar?) | bilinmiyor | YORUM |

- Belirsiz kalanlar: kanal oluşturma kuralı, "kanal içi nötr" dışındaki durumlar, delta için eşik.
- Tansu'nun kanıtı: tek negatif örnek (BALAT, ABCD başarısız). Tek pozitif kanal örneği RYSAS (sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: trend çizgisinde pivotları ikili bağlama ve arada delinmeme kaynaklıdır; kanal üretimi ayrıntıları YORUM'dur (Ham, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21–27). Gerçek işlem deltası günlük OHLCV'den çıkmaz; kaynak panelinin proxy olup olmadığı açık değildir (Araç, G45/g1, alt panel). Günlük proxy seçimi YORUM'dur.
- Kaynak güveni: birinci el (görseller). Dersin kuralı ikinci el.

---

## 15. Three Drives (Üç İtiş)

- Kaynak: `kaynak-three-drives-2096510322190201208` (three-drives.webp; tweet The_Tansu_/status/2096510322190201208, 2026-09-06 08:06:26 UTC).
- Tansu'nun ifadesi: görsel etiketleri (birinci el): `X`, `Drive 1`, `A`, `Drive 2`, `C`, `Drive 3`. Metin kuralları (Ham: tweet metni birebir, api.fxtwitter.com, 06.10.2026 çekildi):
  - Alış yönü: giderek düşen üç dip. Satış yönü: giderek yükselen üç tepe.
  - Ara düzeltmeler yaklaşık %61,8 veya %78,6.
  - Sonraki itişler önceki düzeltmenin 1,272 veya 1,618 uzatması.
  - A→Drive 2 ve C→Drive 3 bacakları uzunluk ve süre bakımından yakın (AB=CD mantığı).
  - Süre: 10 bara karşı 11–12 bar dengeli; 8 bara karşı 30 bar dengesiz. Genel tolerans yok.
  - Drive 3 olası dönüş bölgesi; doğrudan ters işlem gerekçesi değil. Güçlü trendde başarısız olabilir.
- Tanım (hesaplanabilir, sınırlı):
  1. Satış yönü: pivotlar `X(dip) → Drive1(tepe) → A(dip) → Drive2(tepe) → C(dip) → Drive3(tepe)`. Tepeler yükselen: `D1 < D2 < D3`.
  2. Düzeltme oranı: `(D1−A)/(D1−X) ≈ 0,618 veya 0,786`; `(D2−C)/(D2−A) ≈ 0,618 veya 0,786`.
  3. İtiş uzantısı: `(D2−A)/(D1−A) ≈ 1,272 veya 1,618` (Ham "önceki düzeltme hareketlerinin ... extension" diyor; tam çapa YORUM).
  4. Zaman: bar sayısı yakın (örnek 10 ve 11–12).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Düzeltme oranları | 0,618 ; 0,786 | Ham |
| İtiş uzantı oranları | 1,272 ; 1,618 | Ham |
| Zaman toleransı | 10 vs 11–12 iyi, 8 vs 30 kötü | Ham. Sayısal eşik yok. |
| Oran toleransı | bilinmiyor | YORUM |
| Giriş / stop / hedef | yok | Ham |

- Belirsiz kalanlar: oran toleransı, zaman toleransı, "önceki düzeltmenin uzatması" çapası, ters işlem teyidi, stop. Fiyat ekseni görselde yok, oranlar doğrulanamaz.
- Tansu'nun kanıtı: tek görsel, fiyat yok.
- Günlük bedava veriyle uygulanabilir mi: oran kısmı evet. Zaman ve işlem kuralı yok.
- Kaynak güveni: etiketler ve oranlar birinci el (görsel ve Ham).

---

## 16. Elliott: Dalga 2 (CWENE, BRYAT, yüzde 8 örneği)

- Kaynak: `kaynak-cwene-dalga2-demand-2094128312729624792` (elliott.webp, demand.webp; tweet 2094128312729624792, 2026-08-30), `gorsel-paket-107` (BRYAT), `gorsel-paket-110` (yüzde 8).
- Tansu'nun ifadesi:
  - CWENE (Ham, tweet metni birebir): `33,10→48,30` Dalga 1; yaklaşık 35 dip olası Dalga 2; `32,5–36` talep alanı; `48,30` üzeri kapanış Dalga 3 senaryosunu güçlendirir; `33,10` altı mevcut bullish sayımı iptal. Görsel (birinci el): `0`, `1`, `2?` etiketleri. Kırılım etiketleri (demand görseli): `Kırılım 2026-07-21 (Temas:6)`, `Kırılım 2026-07-24`, `Kırılım 2026-08-05 (Temas:3)`.
  - BRYAT (görsel, birinci el): başlık `BRYAT - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 2 (Fibo: %64.3)`. Lejant: `BB Üst (14)`, `BB Alt (14)`, `EMA(9)`, `RSI(14)`, `EN YAKIN FVG`.
  - BRYAT stratejisi (Ham, `gorsel-paket-107`; Ham'da yazar yok): günlük, yüksek hacimli BIST30/100 hisseleri; Point0→Point1 en az %10 itki; ABC Wave2 düzeltmesi; alım bölgesi `0,50–0,786`; ideal Golden Pocket `0,618–0,65`; bölgede taze (fresh) bullish FVG; giriş FVG üst bandı veya Fib 0,618 limit; stop Point0 altı; TP1 = Point1; TP2 = `C + 1,618 × Wave1`; bilanço öncesi riskten kaçın; FVG'ye gelmeden dönen fiyatı kovalama; düşüş yapısında uygulama.
  - 110 (Ham; Ham'da yazar yok): düzeltmenin Fib `0,50` veya `0,618` alanına inmesi ve bullish FVG ile çakışması; hafta başı listesinde verilen hissede `%8` getiri beyanı.
- Tanım (BRYAT, not'tan hesaplanabilir):
  1. `P0` = itki başı (dip), `P1` = itki tepesi. `W1 = P1 − P0`. Koşul: `P1/P0 − 1 >= 0,10`.
  2. Düzeltme: `Fib(r) = P1 − r*W1`. Alım bölgesi `Fib(0,786) <= fiyat <= Fib(0,50)`. Golden Pocket `Fib(0,65)..Fib(0,618)`.
   3. Bölgede taze bullish FVG (üç mum boşluğu; formül A §1 parametre tablosunda); daha önce doldurulmamış olmalıdır (Ham, G107:47–48 ve G107:48–50). Kısmi/tam dolum sınırı açık değildir.
  4. Giriş: FVG üst bandı veya Fib 0,618'de limit.
  5. Stop: `P0 − tampon`. Wave 2, P0'ı aşağı geçmemeli (Elliott kuralı).
  6. TP1 = `P1`. TP2 = `C + 1,618*W1` (C = düzeltme sonu).
- Ölçüm (benim hesabım): CWENE'de Dalga 2 dibi ≈35 ve Dalga 1 = 33,10→48,30; geri alım 0,875'tir. BRYAT alım bölgesi 0,50–0,786 dışındadır. YORUM: bu katalog bu örnekleri karşılaştırır; ayrı varyant veya örnek seçimi açıklaması kaynakta verilmez (Ham, G107:41–43; ilgili araç görselleri).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Min itki | %10 | Ham (`gorsel-paket-107`) |
| Alım bölgesi | 0,50–0,786 | Ham |
| Golden Pocket | 0,618–0,65 | Ham |
| Başlıktaki Fibo | %64,3 (BRYAT), %54,0 (ENJSA Wave 4) | görsel |
| TP2 | C + 1,618*W1 | Ham |
| Evren | BIST30/100, günlük | Ham |
| BB periyodu, EMA, RSI | 14, 9, 14 | görsel (lejant) |
| FVG "taze" tanımı | daha önce doldurulmamış üç mum boşluğu | Ham, G107:48–50; kısmi/tam dolum sınırı ve `TEMAS (0.00%)` hesabı açık değil |
| Pivot / BOS parametreleri | bilinmiyor | YORUM |

- Belirsiz kalanlar: `FVG TEMAS (0.00%)` etiketinin anlamı (temas var ama doluluk %0 mı?), "dolgun mum" tanımı, pivot kuralı, Wave 2 "ABC" zorunlu mu, giriş dolumu (limit ne zaman dolar?).
- Tansu'nun kanıtı: yüzde 8 örneği Ham beyanıdır (110), önceden listede olduğu doğrulanmadı. BRYAT bekleyen kurulum, sonuç yok. CWENE tweet'inde sonuç yok.
- Günlük bedava veriyle uygulanabilir mi: evet (fiyat, FVG, retracement). Pivot ve %10 eşiği net.
- Kaynak güveni: başlıklar ve strateji birinci el (görsel ve Ham).
- Ek örnek (KANIT, bilet 04, 14.10): `gorsel-paket-131-alka-elliott-wave2-fvg-temas` (Ham; görsel okundu). Başlık `ALKA - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 2 (Düzeltme: -39.3%)`; lejant BB (14), EMA(9), RSI(14), EN YAKIN FVG (BRYAT ile aynı araç şablonu). Mavi 0→1 hamlesi, kırmızı kesik A-B-C, C noktası sarı FVG kutusuna (yaklaşık 9,6–10) değiyor. Ham metnindeki "inverted hammer" (ters çekiç) iddiası görselde seçilemedi (mumlar küçük): doğrulanmadı, görsel metinden önce gelir. Ölçüm (piksel, yaklaşık, YORUM): 0 ≈ 7,5, 1 ≈ 16,1, C ≈ 9,8 → geri alım ≈ 0,73, yani BRYAT bölgesi 0,50–0,786 içinde; başlıktaki "Düzeltme: -39.3%" zirveden düşüş yüzdesi gibi okunur ve BRYAT başlığındaki "Fibo: %64.3" ile aynı alan değildir (Ham da böyle der: fiyat zirveden bu yana yaklaşık %40 değer kaybetmiştir). Giriş, stop, hedef, sonuç yok.
- FVG alımı öncesi yükselen dip filtresi (`gorsel-paket-132-fvg-yukselen-dipler-wave3-abc-duzeltme`; metin Ham; Ham'da yazar yok: kaynak notu metnin bir yapay zekâ yanıtından alınmış olabileceğini söyler, bu bir çıkarımdır; iki görsel okundu; bilet 04, 14.10): FVG alımı, önceki Lower Low (LL) sonrası Higher Low (HL) oluşmuş (ayı yapısı kırılmış, "Market Structure Shift") bir yükselişte, düzeltmenin yükselen diplerin üstündeki talep/FVG bölgesine inmesiyle daha güvenilirdir. Görsel 1: 0, 1, HH, A-B-C, HL, LH, LL etiketleri ve sarı FVG kutusu; görsel 2: 0-1-2-3 mavi yol, HH, HL, kırmızı kesik A-B-C, FVG ve talep kutuları; ikisinde fiyat/tarih değeri yok. Bu bir filtredir: giriş, stop, hedef yok. HL'nin tanımı (pivot ayarı) yok (YORUM); filtrenin başarı oranı ölçülmemiş. Sembol ve zaman dilimi yok.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-elliott-2-dalga-dip-w1-1618-hedef-1985831305662050335` — Haftalık Wave 2 dibi ve Wave 3 hedefi, Tansu'nun kendi gönderisi (04.11.2025). "haftalık elliot son hafta 2. dalga dibi tespit edildi." ve "Hedefe takılmayın kendi hedefinizi kendiniz koyun." (Ham). Görsel (görsel, açıldı): "RODRG - ELLIOTT 2. DALGA DÜZELTMESİ [HAFTALIK]", "1.Dalga: +119.8% | 2.Dalga: -36.7% | 3.Dalga Hedef: 51.49 TL", "3. Dalga Hedef (W1*1.618): 51.49 TL". YORUM (piksel okuması): START ≈15,5, 1 ≈34,1, 2 ≈21,6; hedef = 2. dalga dibi + 1,618 × W1 ≈ 21,6 + 30,1 ≈ 51,7, yani BRYAT TP2 (C + 1,618 × W1) ile aynı formül; W2 geri alımı ≈%67 (BRYAT bölgesi 0,50–0,786 içinde); −%36,7 zirveden düşüştür (ALKA başlığındaki −%39,3 gibi). Giriş, stop, TP1, FVG yok; lejant BB (14), EMA(9), RSI(14) (görsel, açıldı). Parametre: Wave 3 hedefi = W1 × 1,618 (başlık: W1*1.618), RODRG örneğinde 51,49 TL; W1 +%119,8, W2 −%36,7 (görsel, açıldı); çapa (W2 dibi + 1,618 × W1) YORUM
  - `tweet-elliott-dalga2-demand-konfluens-seviyeler-2094330871801053695` — CWENE için seviye merdiveni ve iki giriş tarzı (Tansu'nun alıntıladığı kendi gönderisi): "35–36: kritik destek üzerinde kaldıkça Dalga 2'nin bitmiş olma senaryosu canlı." 37–38 hacim/denge; 40–41.5 ilk direnç; 44–48.5 supply; 48.30 üstü kapanışta Dalga 3 güçlenir; 33.10 altı sayım iptal (Ham). Agresif: 35–36 demand korunmasını fırsat sayar, 33.10 yapısal risk; muhafazakâr: önce 40–41.5 kırılımını bekler. "Elliott'taki 2? noktası ile Demand bölgesinin aynı yere denk gelmesi bence önemli bir konfluens" (Ham). Dalga 2 dibi ile talep bölgesi çakışması filtre olarak okunur (YORUM). Sonuç yok. Parametre: Dalga 2 dibi ≈35 ile talep bölgesi 32,5–36 çakışması = konfluens; kademeler 37–38, 40–41,5, 44–48,5 (Ham); agresif stop 33,10 (yapısal risk), muhafazakâr giriş 40–41,5 kırılımı (Ham)
  - `tweet-elliott-dalga2-fvg-temas-1989340141450850613` — ALKA, aynı araç şablonuyla (Wave 2 + FVG teması): başlık "ALKA - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 2 (Düzeltme: -38.4%)" (görsel, açıldı). Ham: "#alka da tavan böyle geldi." Ham sonuç iddiasıdır, tek vaka. C noktası sarı FVG kutusuna değiyor; geri alım ölçümü ≈0,72 (piksel: 0≈7,5, 1≈16,0, C≈9,85; YORUM), BRYAT bölgesi 0,50–0,786 içinde. Eski ALKA örneğinde (-39.3%) başlık farklıdır. Parametre: Başlıktaki Düzeltme = -38,4% (zirve 16,0 → C ≈9,85; zirveden düşüş yüzdesi; görsel, açıldı)
  - `tweet-elliott-ikinci-dalga-hedef-1618-1984349202730926414` — Dalga 3 hedefi formülü görselde: "3. Dalga Hedef (W1*1.618): 1557.96 TL"; "Impulse (Start-1-2): +50.8% | 2. Dalga Düzeltmesi: -31.2%" (görsel, açıldı). Ham: "Bu kardeş %150 falan yapmış:D" (sonuç iddiası, doğrulanmadı). BRYAT'taki TP2 = C + 1,618×W1 ile aynı: çapa Dalga 2 sonu (ölçüm: P2≈869 + 1,618×(1264−837) ≈ 1560; piksel, YORUM). Parametre: Wave 3 hedefi = W2 sonu + 1,618 × W1 (W1*1.618; görsel, açıldı; çapa ölçümü YORUM); araç eşikleri W1 +%50,8, W2 -%31,2 (UFUK örneği)
  - `tweet-haftalik-dalga2-yuzde50-duzeltme-1984370009616105948` — Haftalık tarama filtresi, sözle: "Haftalık periyotta %50'lik düzeltme yapan 2. dalga dibindeki hisseler 3. itki dalgası için hazırlar"; "3. itki dalgası da en uzun dalgadır." (Ham). Eşik Dalga 2'nin %50 geri alımıdır; BRYAT bölgesinin (0,50–0,786) alt ucuyla uyumlu. %50 alt sınır mı, tam değer mi belli değil (YORUM). Sembol, giriş, stop, sonuç yok. Parametre: Haftalık Dalga 2 geri alımı = %50 (Ham; alt sınır mı tam değer mi belli değil, YORUM)
  - `tweet-haftalik-elliott-ikinci-dalga-hedef-1984370692436189464` — BINHO haftalık, aynı araç şablonuyla Dalga 3 hedefi (tekrar): "Impulse (Start-1-2): +84.7% | 2. Dalga Düzeltmesi: -31.5% | 3. Dalga Hedef: 18.77 TL", etiket "3. Dalga Hedef (W1*1.618)" (görsel, açıldı). Ham: "Hocam kod fena:)". Çapa kontrolü (hesap bizim): yüzdelerden uçlar çözülür (P0 ≈ 7,12; P1 ≈ 13,15; P2 ≈ 9,01); P2 = ikinci görüntüdeki 13.10.2025 haftalık kapanışı 9,01 (görsel, açıldı); 9,01 + 1,618 × 6,03 ≈ 18,77. Çapa = Dalga 2 sonu, kapanış serisiyle (YORUM). Sonuç yok. Parametre: Wave 3 hedefi = W2 sonu + 1,618 × W1 (başlık: W1*1.618; görsel, açıldı); BINHO: W1 +%84,7, W2 −%31,5, hedef 18,77 TL; çapa W2 sonu kapanışı 9,01 ile doğrulandı (hesap, YORUM)

---

## 17. Elliott: Dalga 4 retracement ve Dalga 5 hedefi

- Kaynak: `tweet-elliott-wave4-wave3-retracement-024-038-050` (Ham), `gorsel-paket-102` (01-enjsa-elliott-wave5-hikkake-fvg-outcome.png).
- Tansu'nun ifadesi:
  - Ham (`tweet-elliott-wave4-wave3-retracement-024-038-050`): 4. dalga düşüşü = 3. dalga yükselişi × (0.24 veya 0.38 veya 0.50). Örnek: 3. dalga 100 birim yükseldiyse 4. dalgada "genellikle 24, 38 veya 50 birim geri düşmesi beklenir".
  - 102 görsel başlığı (birinci el): `ENJSA - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 4 (Fibo: %54.0)`. Yeşil kesikli `Wave 5 Hedef` çizgisi (~94), yeşil FVG kutuları, sarı kutu (Hikkake).
  - Metin (Ham, `gorsel-paket-102`; Ham'da yazar yok): Wave 5 hedefi yaklaşık `94–95` TL; "Kritik Seviye": fiyat `85–90` TL bandında hareket ediyor; fiyat sarı kutunun ve altındaki yeşil desteklerin altına inerse senaryo bozulabilir.
- Tanım (bullish, hesaplanabilir):
   - `W3 = P3 − P2`. `P4_hedef(r) = P3 − r*W3`; r ∈ {0,24 ; 0,38 ; 0,50} (Ham, tweet-elliott-wave4-wave3-retracement-024-038-050:27). Bearish ayna: aynı formül, `W3` işaretli.
  - Örnek: P2=200, P3=300 → 276 / 262 / 250 (kaynak oranları).
  - Standart itkide Wave 4, Wave 1 alanına girmemeli (genel Elliott teorisi; bizim kural olarak kullanımımız: YORUM, Ham'da yok; yalnız notun yapay zekâ bölümünde).
  - ENJSA başlığındaki `%54,0` büyük olasılıkla Wave 4 geri alım oranı. 0,50'ye yakın, 0,38'in üstünde. (YORUM)
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Wave 4 geri alım oranları | 0,24 / 0,38 / 0,50 | Ham |
| ENJSA Wave 4 geri alım | %54,0 | görsel |
| ENJSA Wave 5 hedefi | ≈94 (çizgi), 94–95 (metin) | görsel, Ham |
| Wave 5 hedefinin formülü | bilinmiyor | YORUM |

- Belirsiz kalanlar: Wave 5 hedef formülü (hangi çapa?). ENJSA %54 ile kuralın 0,50 üst sınırı arasında 4 puan fark. Kural "rehber", zorunlu değil (Ham: "genellikle").
- Tansu'nun kanıtı: ENJSA hedefe ulaştı (görsel, hedef çizgisini test etmiş veya aşmış). Seçilmiş olumlu vaka. Hedefin önceden donduruldu mu belirsiz.
- Günlük bedava veriyle uygulanabilir mi: Wave 4 hedef merdiveni evet. Dalga sayımı otomasyonu zor. Pivot ve sayım kuralı yok.
- Kaynak güveni: birinci el (oranlar Ham'da; ENJSA başlığı ve metni).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-c-dalga-0618-fibo-hedef-fiyat-1978152557945000041` — Bölümün "hedef formülü bilinmiyor" boşluğuna aday: hedef = 3. itki dalgasının sonu + 0,618 × en uzun itki dalgasının boyu (Tansu örnek olarak C dalgasını verir). "Elde ettiğiniz bu değeri üçüncü itki dalgasının sonuna eklediğinizde, fiyatın ulaşabileceği olası bir zirve ya da dip bölgesine dair güçlü bir tahmin yapabilirsiniz." (Ham). Bunun Wave 5 hedefi olduğu yazılı değil (YORUM). "En uzun itki dalgası" ile C seçimi, yön, oran seti ("0,618 gibi temel bir Fibonacci oranı") belirsiz; "Kodu hazır" der ama kod ve sonuç notta yok. Tansu: bu "tek başına bir kehanet değil". Parametre: Elliott hedef formülü = 3. itki sonu + 0,618 × en uzun itki dalgası boyu (Ham; hedef dalganın Wave 5 olduğu YORUM)
  - `tweet-elliott-3-dalga-5-dalga-hedefi-1983565377532572092` — Dalga 5 hedef formülü artık görselde yazılı: "5. Dalga Hedef (W3*0.618): 18.63 TL" (görsel, açıldı). AEFES'te hedef 18.63, gerçekleşen 18.13: "18.63 hedef bulmuş algo. gerçekleşen 18.13" (Ham). Kod 3. itkiyi bulup ölçer; 4. dalganın bittiği noktayı bulmak sonraki adımdır (Ham). Tek vaka, seçilmiş. Parametre: Wave 5 hedefi = W3 × 0,618 (görsel, açıldı); çapa görselden ölçülünce P3 + 0,618×(P3−P2) çıkar: AEFES 17,29 + 0,618×2,15 ≈ 18,62 (piksel ölçümü, YORUM)
  - `tweet-elliott-4-dalga-geri-cekilme-orani-2000162181623484798` — Tekrar: Wave 4 geri alım oranları aynı: "4. Dalga Düşüşü = 3. Dalga Yükselişi X (0.24 veya 0.38 veya 0.50)" (Ham). 100 birimlik 3. dalgada 24, 38 veya 50 birim geri düşüş beklenir. Yeni parametre yok. Okuma notu: Metin, havuzdaki `tweet-elliott-wave4-wave3-retracement-024-038-050` ile aynı (muhtemelen aynı gönderi iki adla); §17 kaynağı o not.
  - `tweet-elliott-5-dalga-hedef-kesisim-bolgesi-2000274228516413714` — Wave 5 hedefi iki izdüşümün kesişimidir: başlık "Hedef Bölge: 93.73 - 103.03 TL | Fibo: %49.2"; çizgiler "1.618 X (P1'den)" ve "0.618 Y (P3'ten)"; kutu "KESİŞİM (5. Dalga Satış Bölgesi)" (görsel, açıldı). Ham: "Confluence kimi zaman güzel kar yazar. Videolarda anlatıldı." Alt sınır 93,73, §17'deki ENJSA ≈94 çizgisiyle uyumlu (YORUM). X ve Y'nin tanımı yazılı değil. Parametre: Wave 5 hedef bölgesi = 1,618×X (P1'den) ile 0,618×Y (P3'ten) kesişimi; ENJSA 93,73–103,03 TL (görsel, açıldı). 0,618 çizgisi alt, 1,618 çizgisi üst sınır (görsel, açıldı)
  - `tweet-elliott-5-dalga-hedef-w3-0618-1984338420769177613` — Dalga 5 hedefi, 4. dalga bittiği anda hesaplanıyor: "5. Dalga Hedef (W3*0.618): 212.92 TL"; başlık "Impulse (1-3): +59.0% | 4. Dalga Düzeltmesi: -14.7%" (görsel, açıldı). Ham: "Kodumuz çalışıyor maşallah". Sonuç rakamı yok; görselde fiyat hedef çizgisine yaklaşmış (kırmızı ok). AEFES ile aynı formül. Parametre: Wave 5 hedefi = W3 × 0,618 (görsel, açıldı); TMPOL ölçümü: P3 ≈180 + 0,618×(180−126) ≈ 213 (piksel ölçümü, YORUM): çapa P3
  - `tweet-elliott-fvg-hikkake-yorumu-2003162633210359902` — Tekrar: ENJSA Wave 4 + FVG + Hikkake yorumu Tansu'nun kendi gönderisinde: "Gerçekleşmiş bir hikayeye bakalım" (Ham). Hikkake = "ayı tuzağı" ardından yukarı patlama; Wave 5 hedefi yaklaşık 94-95 TL; fiyat 85-90 bandında; sarı kutu ve yeşil desteklerin altına inerse senaryo bozulur (Ham). Metin yapay zekâ özeti gibi okunur (YORUM). Yeni sayı yok; "gerçekleşmiş" ifadesi hedefin vurulduğunu destekler. Okuma notu: Ham metni, `gorsel-paket-102-enjsa-elliott-wave5-hikkake-fvg-outcome` notundaki metinle aynı; görsel de aynı ENJSA şablonu (§17 zaten alıntılıyor).

---

## 18. Elliott 5+3 ve Fibonacci gün sayımı

- Kaynak: `gorsel-paket-111` (01-elliott-5plus3-fibonacci-islem-gunleri.jpg).
- Görsel metni (NotebookLM görseli, birinci el; alt köşede `NotebookLM` damgası, yani üretici bir yapay zekâ aracı; Tansu'nun kendi çıktısı olup olmadığı belli değil):
  - `Borsanın Ritmi: Elliott Dalga ve Fibonacci Sırları`. `5+3 DALGA PRENSİBİ`: "Piyasalar, 5 dalgalık bir ana trend (itki) ve ardından gelen 3 dalgalık bir düzeltme ile hareket eder."
  - `Matematiksel Uyum: Fibonacci Dizisi`: "Döngüdeki toplam dalga sayıları (3, 5, 8, 13, 21, 34...) daima Fibonacci dizisini takip eder."
  - `ZAMAN ANALİZİ: GÜN SAYMA KURALI`: "Bir trendin tepe veya dip noktalarında genellikle Fibonacci günlerinde (5., 8., 13., 21. gün vb.) test edilir."
  - `EN KRİTİK KURAL: TAKVİM GÜNLERİNİ SAYIN!` "Analiz yaparken sadece işlem günlerini değil, hafta sonları ve tatiller dahil tüm günleri hesaba katın."
- Tanım (sınırlı): bir pivottan (tepe veya dip) başla. Takvim günü say. 5., 8., 13., 21. günlerde yeni pivot oluşup oluşmadığına bak.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Gün sayısı dizisi | 5, 8, 13, 21 | görsel |
| Sayım birimi | takvim günü (hafta sonu ve tatil dahil) | görsel |
| Tolerans (±gün) | bilinmiyor | YORUM |
| Başlangıç çapası | "tepe veya dip" | görsel; pivot kuralı yok |

- Belirsiz kalanlar: tolerans, pivot çapası, "test edilir" ne demek (pivot oluşumu mu, dönüş mü), hangi zaman diliminde. Hiçbir sembol veya sonuç yok.
- Tansu'nun kanıtı: yok. Eğitim infografiği.
- Günlük bedava veriyle uygulanabilir mi: sayma evet. Anlamlılığı test edilmeden kural sayılmaz.
- Kaynak güveni: NotebookLM görseli, birinci el. Tansu'ya atfı belirsiz (NotebookLM damgası).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-elliott-5-3-fibonacci-gun-sayma-2000103306325004349` — Tekrar: aynı NotebookLM görseli Tansu'nun kendi X gönderisinde: "Fibonacciyi çok sevdik o zaman biraz daha öğrenelim." (Ham). Görsel (açıldı): 5., 8., 13., 21. gün; "TAKVİM GÜNLERİNİ SAYIN". Gönderi eğitim niteliğinde; sembol, tolerans, sonuç yok. §18'deki 'Tansu'ya atfı belirsiz' notu: görsel Tansu'nun gönderisinde paylaşıldı, ama içeriğin kendi analizi olduğu kanıtlanmaz (YORUM). Parametre: Gün sayısı dizisi = 5, 8, 13, 21 (takvim günü) (görsel, açıldı). Okuma notu: G2 görseli `gorsel-paket-111-elliott-5plus3-fibonacci-islem-gunleri` ile aynı; Ham metni yeni bilgi vermez.

---

## 19. Çoklu aralık Fibonacci konfluansı

- Kaynak: `gorsel-paket-120` (dört görsel, CAT örneği).
- Metin (Ham'da yalnız görsel var; Ham'da yazar yok; görsel başlıkları ve metinleri, bkz. bu bölümün "Kaynak güveni" satırı):
  - `Geleneksel Yaklaşım: Çoğu Yatırımcının Fibonacci'yi Kullanma Şekli`: A (Start) ve B (End), seviyeler `38.2%`, `50.0%`, `61.8%`.
  - `Kaçınılmaz Başarısızlık: Piyasa Standart Seviyeleri Neden Görmezden Gelir?`: Caterpillar C noktasında "ilk destek seviyesine ($29 civarı) asla ulaşmadı"; "sorun metodolojinin kendisinde değil, onun statik ve tek boyutlu uygulanışındadır".
  - `Piyasanın Nabzını Ölçmek: Genişleme ve Daralmayı Tespit Etme`: 1. Aralık d: en güçlü salınımı seç, %50'sini (A çizgisi) belirle. 2. Aralık e: aralığı genişlet, yeni %50 (B çizgisi). B > A genişleme. 3. Aralık f: %50 (C çizgisi) daha yukarı kayar.
  - `Anahtar Kavram: Yüksek Olasılıklı 'Konfluans Bölgeleri' Yaratmak`: "Konfluans bölgesi, birden fazla ve farklı uzunluktaki fiyat aralığından hesaplanan Fibonacci oranlarının çakıştığı veya kümelendiği bir fiyat alanıdır." Görselde seviyeler `31.2%`, `38.2%`, `50.0%`, `61.8%`; kümeler `x1`, `x2`.
- Tanım (hesaplanabilir):
  1. Birden fazla aralık seç (en güçlü salınım, genişleyen aralıklar).
  2. Her aralık için seviye: `düşük + oran*(yüksek − düşük)`, oranlar {0,382 ; 0,50 ; 0,618} (+ 0,312 görselde, anlamı belirsiz).
  3. Birbirine yakın seviyeleri kümele. Kümeler "konfluans bölgesi".
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Oranlar | 0,382 ; 0,50 ; 0,618 (+ "31.2%" etiketi) | görsel |
| Aralık seçimi | "en güçlü salınım", genişleyen | görsel (algoritma yok) |
| Küme eşiği (yakınlık) | bilinmiyor | YORUM |
| Aralık sayısı | görselde 3 (d, e, f) | görsel |

- Belirsiz kalanlar: aralık seçim algoritması, küme eşiği, `31.2%` anlamı, giriş/stop/hedef. Hiçbiri yok.
- Tansu'nun kanıtı: yok (eğitim görselleri, CAT seçilmiş).
- Günlük bedava veriyle uygulanabilir mi: evet (hesap kolay). Anlamlı kural için aralık seçimi YORUM.
- Kaynak güveni: Ham görselleri, birinci el; Ham'da yazar yok (eğitim metinleri; Eğitim, G120/g1–g4). YORUM: bu katalogda paylaşılan eğitim materyali olarak okunur; üretici doğrulanmış değildir.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-elliott-ic-dis-sayim-confluence-2086920060254212344` — Konfluans bandı tanımı: "Elliot yaptınız, iç sayım ve dış sayım tekniği ile bir hedef belirlediniz ama %5 fibi bir sapma var. İşte o %5'lik alandır confluence alanı." (Ham, yanıt gönderisi). İki hedef (iç ve dış sayım) arasındaki sapma %5 kadar olursa, aralık konfluans bölgesidir. Parametre: Küme eşiği (yakınlık) = %5 Fibonacci sapması (Ham); yüzdenin birimi (fiyat mı, oran mı) belli değil (YORUM)
  - `tweet-fibonacci-genisleme-konfluans-bolgesi-1998871553984049576` — Tekrar, birinci el kaynak olarak: §19'daki dört CAT görseli Tansu'nun kendi X gönderisinde, tek cümleyle: "Bence lazım olabilir" (Ham, 10.12.2025). G4 açıldı: "31.2%" etiketi, 61.8 / 50.0 / 38.2 düzeyleri, x1 ve x2 kümeleri; §19'daki içerikle aynı. Tansu görselleri kendi analizi diye sunmaz, öneri olarak paylaşır (YORUM); üretici ayrı kalır. Yeni parametre, eşik, giriş, stop yok.

---

## 20. Mimari kararlar (kural değil): ayrı tarayıcılar ve squeeze projesi

- Kaynak: `tweet-gartley-butterfly-ayri-tarayicilar`, `tweet-harmonik-momentum-squeeze-projesi`, `tweet-uygulama-algoritmalari-v1`, `gorsel-paket-02`.
- Tansu'nun ifadesi (Ham): Gartley ile butterfly kodlarını ortak tarama sisteminde birleştirmek fikri "beni hasta etti"; "asla tavsiye etmiyorum", Gartley taramasını ve butterfly taramasını ayrı yapın, "Konsolide etmek bünyeye büyük zulüm" (`tweet-gartley-butterfly-ayri-tarayicilar`). Harmonik formasyonlarda momentum squeeze'in hangi noktada oluştuğu ayrı bir proje konusudur; formasyon adı yok (`tweet-harmonik-momentum-squeeze-projesi`). İlk kapsam listesi (`tweet-uygulama-algoritmalari-v1`): ABCD, Kelebek, Gartley; haftalık kanal dibine temas; düşeni kıran; takoz, TOBO, OBO, bayrak, flama.
- Tanım: yok (mimari ve proje önerisi).
- Parametreler: yok.
- Belirsiz kalanlar: hepsi.
- Tansu'nun kanıtı: yok.
- Günlük bedava veriyle uygulanabilir mi: mimari karar olarak evet (Gartley ve Butterfly ayrı modül; ortak sonuç arayüzü).
- Kaynak güveni: birinci el (Ham).

---

## 21. Sıralı kısa liste: koda ne kadar hazır?

Sıralama: 1 = en hazır. "Hazır" = oran, giriş, çıkış ve etiket Tansu'nun birinci el kaynağında (görsel veya Ham) var.

1. AB=CD (r = 1,0 ve 1,27), D formülü, hedef merdiveni (kural 3 ve 4).
   - Hazır: `D = C + r*(B−A)`, `q <= 1`, D, B'nin ötesinde, hedef `D + {0,618; 1,0; 1,618}*(A−D)`. Ölçümle doğrulandı (KRPLS, MARKA, RYSAS).
   - Boşluk: pivot parametreleri, oran toleransı, BOZULDU bazı, stop, q alt sınırı.
2. Gartley tablosu (kural 7).
   - Hazır: AB/XA 0,618; BC/AB 0,382–0,886; D 0,786 XA. Eğitim tablosu TP1 AD 0,382 (%50), TP2 AD 0,618; SAYAS TP1 1:1 R/R. Stop seçenekleri X / XA 1,13 / X−2ATR; genel seçim açık değildir (Eğitim, G123/g1; Araç, SAYAS görseli).
   - Boşluk: %3–5 toleransın birimi; MAKIM bacakları genel toleransı vermez (Ham, G123:49; Araç, G122/g1). Pivot, n_period, ATR periyodu ve stop seçimi açık değildir.
3. Elliott Wave 4 hedef merdiveni ve BRYAT Wave 2 stratejisi (kural 16 ve 17).
   - Hazır: formüller net (Wave 4: `P3 − r*W3`; BRYAT: %10 itki, 0,50–0,786 bölge, stop P0 altı, TP1 P1, TP2 C + 1,618*W1).
   - Boşluk: dalga sayımı, pivot kuralı, FVG'nin kısmi/tam dolum sınırı ve `TEMAS (0.00%)` hesabı. Taze = daha önce doldurulmamış (Ham, G107:48–50); CWENE geri alımı BRYAT bölgesi dışındadır.
4. X–B trend kırılımı ve tepki penceresi (kural 9 ve 10).
   - Hazır: çizgi çapaları (X, B), yön, 20 bar tepki etiketi.
   - Boşluk: tampon, stop, tepki eşiği, 10 gün / 20 bar birimi ve ortak politika. Trend çizgisi kırılımı kapanışla tanımlıdır (Ham, tweet-trend-cizgisi-swing-pivot-regresyon-zarf:21).
5. BALAT TP merdiveni (kural 11).
   - Hazır: `TP(r) = D + r*(C−D)`, r = 0,382 / 0,618 / 1 / 1,272.
   - Boşluk: giriş, pattern oranları, R:R düşük (≈0,2).
6. Kelebek (kural 8).
   - Hazır: D = 1,272 XA, B = 0,786 (DOAS).
   - Boşluk: DGATE B ≈ 0,55 çelişkisi, BC ve CD aralıkları, stop.
7. Trident (kural 12).
   - Formül `D = B*C/A` (Ham, G47:20); görselin etiketi `CD=1.27AB`dir ve ikisinin aynı D'yi verdiği doğrulanamaz (Araç, g1).
   - Boşluk: formül ile `CD=1.27AB` etiketi çelişebilir, işlem kuralı yok.
8. Three Drives (kural 15).
   - Hazır: 0,618/0,786 düzeltme, 1,272/1,618 itiş (Ham).
   - Boşluk: toleranslar, çapa, giriş ve stop.
9. Birleşik tarayıcı (talep + düşen direnç + Fibo + ABCD) (kural 13) ve kanal (kural 14).
   - Hazır: temas sayısı, lookback ve EMA parametreleri A §3 (parametre tablosu) sahibindedir.
   - Boşluk: talep bölgesi kuralı, delta verisi, eşikler, zorunlu katmanlar. Kodlanamaz.
10. Çoklu aralık Fibonacci (kural 19), Fibonacci gün sayımı (kural 18), Siyah/Beyaz Kuğu (kural 13), CD şiddeti (kural 6).
    - Hazır değil: konsept, oran veya kural yok. Beyaz Kuğu oranları hiçbir yerde yok; Siyah Kuğu (bullish) oran aralıkları 16.10'da §26'ya girdi (tek örnek).

Genel kanıt durumu: Tansu hiçbir harmonik kural için sistematik bir başarı tablosu göstermiyor. Tek sistematik tablo SMRTG (12 pattern) ve ISKPL (5 pattern), ikisi de tek hisse, maliyetsiz, stop kuralı bilinmiyor. Diğer örnekler seçilmiş pozitif vakalar (LIDER, AKCNS, 40, DOAS, KAPLM negatif dışında).

Ortak boşluklar (hepsi YORUM; kod öncesi karar):

1. Pivot kuralı: L, R, zikzak eşiği, `Swing=15 sol-only`'in harmonik tarayıcıya ait olup olmadığı.
2. Oran toleransı: Ham'da %3–5 vardır; birimi açık değildir. Yaklaşık %10 aday seçimi YORUM'dur; MAKIM ve DGATE'den genel tolerans çıkarılamaz (Ham, G123:49; Araç, G122/g1).
3. `BOZULDU`, `TEPKI_VERDI` ve `BELİRSİZLEŞTİ` eşikleri.
4. Stop kuralı (X, XA 1,13, `X−2*ATR`).
5. Beyaz Kuğu oran tanımı; Siyah Kuğu için oran toleransı ve pivot kuralı (aralıklar §26).

Küçük sonraki adım: kural 3 ve 4 için kendi pivot kararınızı yazın (L, R), sonra KRPLS D=11,29 ve D=10,05 değerlerini fiyat verisinden yeniden üretin.

---

## 22. Omuz-baş-omuz (OBO), kısa kayıt (bilet 04, 14.10)

- Kaynak: `gorsel-paket-121-obo-neckline-hacim-hedef` (yalnız görsel, metin yok; infografik okundu, kaynak imzası yok). Sıralı kısa listede (§21) yoktur.
- Görsel metni (Ham görseli; imzasız infografik, Ham'da yazar yok): `4 Adımda Omuz Baş Omuz (OBO) Formasyonu`. (1) Üç tepeyi tespit et: sol omuz, daha yüksek baş, daha alçak sağ omuz. (2) Boyun çizgisini çiz: omuzlar ile başın taban dip noktalarını birleştiren destek çizgisi. (3) Kırılımı onayla: fiyat boyun çizgisini hacimli bir mumla aşağı kırarsa formasyon onaylanır. (4) Hedef: baş tepesi ile boyun çizgisi arasındaki mesafe kadar düşüş beklenir. "Hacmi kontrol et": sağ omuz oluşurken hacmin azalması güvenilirliği artırır.
- Tanım: hedef = boyun çizgisi − (baş − boyun çizgisi) (kırılım noktasından aşağı).
- Parametreler: yok. Pivot ayarı, omuz benzerlik toleransı, "hacimli" eşiği, kırılım tamponu, stop yok (YORUM).
- Tansu'nun kanıtı: yok (şema; piyasa örneği yok). Bu kural aşağı yönlü dönüş formasyonudur; BIST'te açığa satış pratik değil (TASARIM 3).
- Günlük bedava veriyle uygulanabilir mi: evet (OHLCV). Kaynak güveni: düşük (şema).

---

## 23. 144 barlık Fibonacci %78,6 düzeyi ve ±%2 bant: sistem ve tarama, çoklu gösterge ekranı

- Kaynak: `tweet-fibo-144-78-6-coklu-gosterge-sistemi-1842483289140965576` (05.10.2024; Ham ve görsel, açıldı), `tweet-144-bar-fibo-786-taramasi-1842310608135331999` (Tansu'nun yanıt gönderisi, 04.10.2024; üst gönderi notta yok; görsel yok). İkisi de Tansu'nun X gönderisidir (birinci el). Aynı ekranın CMENT örneği §24'tedir.
- Tansu'nun ifadesi (verbatim): "144 barlık fibo ve 78.6 seviyesi sistemini bundan sonra böyle takip edeceğim. İndikatörler değişebilir ama temel mantığım böyle olacak" (Ham, 05.10.2024). Bir gün önceki yanıtta: "144 barlık Fibo taraması ve fiyatın 78.6 fiboya geldiği hisseler" ve "Çok çok önemli bir teknik üstad sağolsun" (Ham, 04.10.2024; gönderi iki hesaba yanıttır: @BorsaSeker, @fiboborsa). Görsel başlığı (açıldı): `Fibonacci, EMA, ROC, ADX-ADXR, MACD, OBV Seviyeleri (Son 144 Bar)`; `Fibo %78.6 (18.52)`, `Fibo Upper %80.6 (18.89)`, `Fibo Lower %76.6 (18.15)`, `EMA 20 (19.71)`, `EMA 50 (19.80)`, `EMA 100 (19.97)`, `EMA 200 (20.07)`, `Kapanış Fiyatı (18.90)`, `RSI 14 (42.05)`, `ADX (18.60)`, `ADXR (13.54)`, `MACD (-0.05)`, `MACD Signal (0.12)`, `OBV MA20 (9484766.00)`.
- Tanım (YORUM, görsel ve hesap): 144 barlık pencerede en yüksek H ve en düşük L alınır; %78,6 düzeyi `H − 0,786×(H − L)` (yüksekten geri alım; §25'teki DOAS kodunun biçimiyle uyumlu). Hesap kontrolü (bizim): 18,52 × 1,02 = 18,89 ve 18,52 × 0,98 = 18,15; yani "Upper %80.6" ve "Lower %76.6" etiketleri düzeyin ±%2 fiyat bandıdır, oran değil. Kapanış 18,90 üst bandın üstünde, EMA'ların altında (19,7–20,1). Tansu'nun "temel mantığı" bu düzey ve bandır; göstergeler (RSI 50 ekseni, ROC 0 ekseni, ADX/ADXR, MACD, OBV MA20) yardımcıdır ve değişebilir. Tarama (04.10.2024): fiyatı bu düzeye gelen hisseler listelenir (YORUM). Tarama Tansu'nun mu, anılan hesabın mı belli değil; "teknik üstad sağolsun" sözü başkasının taramasını önerdiğini gösterir (YORUM).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Pencere | son 144 bar | Ham ve görsel, açıldı |
| Fibonacci düzeyi | %78,6 (Ham: "78.6") | Ham ve görsel, açıldı |
| Bant | ±%2 (fiyat düzeyinin; YORUM, hesap) | görsel, açıldı |
| EMA'lar | 20, 50, 100, 200 (bu ekranda); 89, 144, 233 (CMENT ekranı, §24) | görsel, açıldı |
| RSI, ROC, ADX/ADXR, MACD, OBV MA | RSI 14, ROC (0 ekseni), ADX-ADXR, MACD, OBV MA20 | görsel, açıldı |
| Giriş, stop, hedef, bar birimi, zaman dilimi, "gelmek" toleransı, yön | yok (günlük varsayımı, YORUM) | - |

- Belirsiz kalanlar: sinyal koşulu (band içi tepki mi, bandın üstüne kapanış mı); iki uç noktanın seçimi (144 barın en düşük ve en yüksek değeri mi, swing mi); pencerenin barı (günlük mü); ROC periyodu; ADX/ADXR eşikleri; göstergelerin karar rolü. 144 bir Fibonacci sayısıdır; seçim gerekçesi yazılı değil (YORUM). Giriş, stop, hedef yok.
- Tansu'nun kanıtı: yok; tek hisse, sonuç yok. CMENT'te "tepki almış" cümlesi bant altında tepkiyi gösterir (§24; seçilmiş örnek).
- Günlük bedava veriyle uygulanabilir mi: evet (OHLCV; 144 günlük en düşük ve en yüksek değerle %78,6). Sinyal kuralı eksik, kural olarak tanımsız. İlgili: A §10 (0,618–0,786 Golden Zone).
- Kaynak güveni: Ham ve görsel birinci el; kural yarım: düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-fibo-144-78-6-ema-rsi-grafik-1842466148337463356` — Direnç sırası okuması: "Fiyat önce 20 günlük ardından 76.8 fibo seviyesinin ve 50 günlük ema'nınüzerine atmaya çalışmış ama başarılı olamamış." (Ham). Görselde EMA20 6,65 < Fibo 6,70 < EMA50 6,85 (görsel, açıldı); RSI14 47,89, "RSI 50'ye yakın" (Ham): RSI 50 ekseni bakış çizgisi (YORUM). Erken bant sürümü görünür: "Fibo Upper %73.6 (6.81)", "Fibo Lower %83.6 (6.58)" (görsel, açıldı). Giriş, stop, sonuç yok. Parametre: Bant (erken sürüm, 04–05.10.2024) = %78,6 düzeyinin ±5 oran puanı: Upper %73,6, Lower %83,6; GEDIK 6,81 / 6,70 / 6,58 (görsel, açıldı). Fiyat yüzdesi değil: GEDIK +%1,6 / −%1,8, JANTS (28,67 / 27,37 / 26,08) +%4,7 / −%4,7 (hesap, YORUM). 05.10.2024 08:06'dan sonraki sürümde ±%2 fiyat bandı (§23)
  - `tweet-fibo-144-bar-78-6-tarama-1842327200441254115` — Tarama koşulu yönsüzdür: "144 barlık Fibo 78.6 seviyesine aşağıdan ya da yukarıdan ulaşmış hisseler." (Ham). Liste 11 sembol (görsel metni), sinyal tipi ayrımı yok. "Artık detay analizlerinizi yaparsınız, yelpazenizi darattım" (Ham): tarama ön eleme, giriş kararı değil. Giriş, stop, hedef, sonuç yok. Parametre: Tarama koşulu = fiyat 144 barlık %78,6 düzeyine aşağıdan ya da yukarıdan ulaşmış (yön ayrımı yok) (Ham)
  - `tweet-fibo-144-bar-786-bandi-1842318331891548280` — Tansu'nun planı (JANTS grafiği): "fiyat ema ve fibo seviyesi buluşmasını inceleyeceğim" ve trend teyidi için "rsi14>50 , ADX/ADXR ikilisi, DMI ve MACD ekleyeceğim" (Ham). Strateji kaynağı: "@fiboborsa üstada teşekkür ederim. Python taramasını yaptım." (Ham); "Bir çok hisse diplerden kalkışa hazırlanıyr" (Ham) görüştür. Plan; yalnız RSI14>50 sayısaldır, ADX/ADXR/DMI/MACD için eşik yok. Parametre: Trend teyidi = RSI14 > 50 (Ham, plan); ek göstergeler ADX/ADXR, DMI, MACD (eşik yok); orta vade EMA seti = 10, 20, 50, 100 (Ham, plan; sonraki ekranlarda 20/50/100/200, §23)
  - `tweet-fibo-786-ema200-cakisma-1842328005974118907` — Çakışma örneği (JANTS): "EMA200=28.77 / Kapanış fiyatı=28.42 / Fibo78.6=27.37 / Anladınız siz onu." (Ham). Görsel (açıldı): fiyat, EMA200 ve %78,6 düzeyi aynı bölgede; EMA20 29,21, EMA50 28,49, EMA100 28,92, EMA200 28,77 hepsi 28,5–29,2 arasında kümelenmiş; Upper %73,6 = 28,67, EMA200'ün 0,10 altında. Tansu EMA200 ile Fibo %78,6 yakınlığını (kümelenme) ilgi nedeni sayar; kural ve eşik yazmaz. "Yarın ... detaylı çizimler yaparız Python ile" (Ham). Sonuç yok. Parametre: Çakışma ölçüsü (Tansu'nun örneğinde) = EMA200 − Fibo %78,6 = 1,40 TL (%5,1); kapanış − EMA200 = −0,35 TL (%1,2); EMA200 üst banda (%73,6 düzeyi) 0,10 TL (görsel, açıldı; hesap, YORUM). Eşik yok
  - `tweet-fibo-786-yakin-kapanis-tarama-144-gun-1844824315558310078` — Taban tarama tanımı: "Son 144 gün temel alınarak fibo 76.8'e çok yakın kapanış yapmış ya da bu seviyeden tepki alarak yükselmiş hisseler." (Ham). Sinyal koşulu iki dallı: (a) düzeye çok yakın kapanış, (b) düzeyden tepki alıp yükselme (§23'teki "sinyal koşulu" belirsizliğine kısmi yanıt). "Evvelki gün bu taramadan bir kaç tavan çıkmıştı:)" (Ham): anekdot, sayı yok. "Bilmediğiniz hisselere girmeyin. Bunlar sadece tarama sonucu" (Ham): tarama giriş sinyali değil. Çıktı: ARASE, GEREL, JANTS (görsel metni). Parametre: Sinyal koşulu = %78,6 düzeyine çok yakın kapanış VEYA o düzeyden tepki alarak yükselme; pencere 144 gün (Ham); "çok yakın" eşiği yok
  - `tweet-fibonacci-vadeye-gore-baslangic-tarihi-1908510592639398132` — Aralık (başlangıç tarihi) seçimi vadeye bağlıdır: "ben önce 1 yıllık ya da 2 yıllık bakıyorum sonra kısa vadeli mi pozisyon alacağım yoksa uzun vadeli mi ona göre fibo'yu belirttiğim tarihten çiziyorum" (Ham). "144 güzeldir." (Ham): 144, kısa vade için seçeneklerden biri. §23'teki "iki uç noktanın seçimi" belirsizliğine kısmi yanıt: uçlar sabit 144 bar olmayabilir, elle seçilen başlangıç tarihinden çizilir (YORUM). Yanıt gönderisi (üst gönderi notta yok); eşik, giriş, stop yok. Parametre: Fibo başlangıç tarihi = pozisyon vadesine göre seçilir (kısa/uzun); önce 1 yıllık ya da 2 yıllık bakış; kısa vadede 144 (bar) "güzeldir" (Ham)

---

## 24. EMA200'ü son gün yukarı kesen hisse taraması ve golden cross adayı (CMENT örneği)

- Kaynak: `tweet-ema200-kesisim-golden-cross-adayi-1842524448802365487` (zincir, iki gönderi, 05.10.2024; Ham ve görsel, açıldı). Tansu'nun X gönderisi (birinci el).
- Tansu'nun ifadesi (verbatim): "Son gün EMA 200'ü yukarı kesen hisseler: ADGYO, AKBNK, AKCNS, ANGEN, AVTUR, BASGZ, CMENT, GUBRF, KOZAA, LOGO, ORMA, RTALB, SAHOL, ULKER, VKGYO"; "Son gün yaşananlar sizi yanıltmasın dikkatli olun."; "Bu hisselerde golden cross arayabilirsiniz."; ikinci gönderi: "Örneğin bu hisselerden cment'e detay bakalım"; "76.8'den tepki almış" (Ham). Görsel (açıldı): `CMENT.IS Fibonacci, EMA, ROC, ADX-ADXR, MACD, OBV Seviyeleri (Son 144 Bar)`; `Fibo %78.6 (378.03)`, `Fibo Upper %80.6 (385.59)`, `Fibo Lower %76.6 (370.47)`, `EMA 89 (407.85)`, `EMA 144 (421.49)`, `EMA 233 (433.65)`, `Kapanış Fiyatı (386.00)`, `RSI 14 (48.36)`, `ADX (13.49)`, `ADXR (15.31)`, `MACD (-9.03)`, `MACD Signal (-5.12)`, `OBV MA20 (-156692.75)`.
- Tanım (YORUM): tarama koşulu: son işlem gününün kapanışı EMA200'ün üstünde, önceki gün altında (yukarı kesişim). Golden cross: kısa EMA'nın uzun EMA'yı yukarı kesmesi (hangi EMA çifti belli değil; 50/200 adayı, YORUM). Tansu kesişimi tek başına sinyal saymaz: "yanıltmasın" uyarısı ve ek inceleme (CMENT'te 144 bar Fibo bandı, §23) ekler. Hesap kontrolü (bizim): Upper = 378,03 × 1,02 = 385,59 ve Lower = 378,03 × 0,98 = 370,47; yani etiketlerdeki %80,6 ve %76,6, fiyat düzeyinin ±%2 bandıdır, oran değil (YORUM). Kapanış 386,00 üst bandın hemen üstündedir. "76.8" CMENT fiyatı olamaz (fiyat ≈370–390); büyük olasılıkla %76,6 alt bandı veya 370 düzeyi (YORUM).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Tarama koşulu | son gün EMA 200'ü yukarı kesmek | Ham |
| CMENT EMA seti | 89 / 144 / 233 | görsel, açıldı |
| 144 bar Fibo | %78,6 düzeyi ve ±%2 fiyat bandı | görsel, açıldı |
| ROC periyodu | 20 (başlık "ROC20") | görsel, açıldı |
| Golden cross çifti, onay günü, filtre | bilinmiyor | YORUM |

- Belirsiz kalanlar: EMA200 kesişiminin tanımı (kapanış mı, gün içi mi); golden cross çifti; EMA seti neden 89/144/233 (Fibonacci sayıları) iken diğer görselde 20/50/100/200 (§23); sıralama ve eleme.
- Tansu'nun kanıtı: yok; liste ve tek örnek, sonuç yok.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük kapanış, EMA).
- Kaynak güveni: Ham ve görsel birinci el; kural yok, güven düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-fibonacci-618-golden-cross-1908471693472919651` — Golden cross adayı + Fibo tepkisi birleşimi: "bu kardeşimiz hem 61.8 den tepki almış hem de yakında golden cross olacak:)" (Ham). Görselde (açıldı) EMA çizgileri etiketsiz (turuncu, noktalı siyah); sembol adı ve tarih yok (Ocak–Mart 2025 ekseni). Aynı serinin A1CAP grafiğinde turuncu = EMA 50, noktalı siyah = EMA 200: çift EMA50/EMA200 olabilir (YORUM). "Yakında" ölçütü, giriş, stop, sonuç yok. Parametre: Golden cross çifti = EMA50/EMA200 olabilir (YORUM; renk eşleşmesi, A1CAP görseli açıldı); "yakında" eşiği yok
  - `tweet-ema-50-200-golden-cross-1908437183423209509` — DOAS (05.04.2025): "golden cross'a adım adım" (Ham). Görsel (açıldı): başlık "DOAS.IS - Mum Grafik ve EMA Kesişimi (50/200)", lejant EMA 50, EMA 200, Al, Sat; EMA50 EMA200'ü ~Eylül 2024'te aşağı keser ve Sat işareti çıkar; Mart 2025'te EMA50 EMA200'e yaklaşır, Al işareti henüz yok. Ham: "Sistemime 190'lardan takılmıştı." Parametre: Golden cross çifti = EMA50 / EMA200 (görsel, açıldı: başlık "EMA Kesişimi (50/200)"); "Sistemime 190'lardan takılmıştı" cümlesinin anlamı belirsiz (YORUM: fiyat 190 düzeyinden sistem listesine girdi)

---

## 25. 1 yıllık kapanış aralığı Fibonacci seviyeleri ve EMA 10/20/50/100/200 seviye haritası (DOAS)

- Kaynak: `tweet-ema-fibo-1yil-en-yuksek-dusuk-kapanis-1842291706093355330` (04.10.2024; Ham ve görsel, açıldı), `tweet-ema-fibo-seviyeleri-python-kod-1842212999169253445` (04.10.2024; Ham, iki görsel; kod görseli açıldı). Tansu'nun X gönderileri (birinci el).
- Tansu'nun ifadesi (verbatim): "EMA VE FİBO kodları"; "1 yıllık günlük veriler"; "fibo en yüksek ve en düşük kapanışa göre çekilmiştir" (Ham; kod bağlantısı harici, notta yok). DOAS (Ham): "Sırası ile 215.57, 219.02 230.22, 245.53, 249.66, 258.28 ve 281.74 geçilir ise bir heyecan gelir!!!!!!!!"; "Şu hisseyi zirveden göz göre göre vermedik!"
- Tanım (kod görseli, açıldı): veri = `yf.download(stock, period='1y')`, günlük `Close`. `EMA_n = Close.ewm(span=n, adjust=False).mean()`, n ∈ {10, 20, 50, 100, 200}. `max = Close.max()`, `min = Close.min()`, `fark = max − min`. Seviyeler: `Fib(r) = max − r×fark`, r ∈ {0,236; 0,382; 0,618; 0,786}; `1 = min`; `0 = max`. Hesap kontrolü (bizim, DOAS: max 399,75, min 208,80): 0,786 → 249,66 (etiket 249,66); 0,618 → 281,74 (281,74). Ham'daki yedi sayı sıralı: EMA200 215,57; EMA100 219,02; EMA50 230,22; EMA20 245,53; Fib 0,786 249,66; EMA10 258,28; Fib 0,618 281,74 (görseldeki değerlerle eşleşir). Okuma (YORUM): fiyat bu yedi direnci sırayla yukarı geçerse yükseliş "heyecanı" başlar; kapanışla mı, kaç gün mü belirtilmedi.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Pencere | 1 yıl, günlük kapanış | Ham ve kod, açıldı |
| EMA periyotları | 10, 20, 50, 100, 200 (span, adjust=False) | kod, açıldı |
| Fibonacci oranları | 0,236 / 0,382 / 0,618 / 0,786 (yüksekten aşağı) | kod, açıldı |
| Aralık | en yüksek ve en düşük kapanış (fitil yok) | Ham ve kod, açıldı |
| Geçiş ölçütü, giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: "geçilir" ölçütü; giriş, stop, hedef; 1 yıl = 252 işlem günü mü (yfinance takvim yılı); düzeltilmiş fiyat (auto_adjust) etkisi.
- Tansu'nun kanıtı: yok (tek hisse, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (yfinance günlük kapanış, EMA). Kural olarak eksik: yalnız seviye listesi.
- Kaynak güveni: Ham ve kod birinci el; kural yok, güven düşük. Hazırlık X.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-fibonacci-destek-seviyeleri-ema200-kod-1844836756501471622` — Aynı kod ailesinin hisse başına grafik sürümü: "Her hissenin 6 aylık fibo desteklerini nasıl kodlarız?" (Ham). Kod (görsel, açıldı): `Close.max()` ve `Close.min()`, `max − r × fark`, r ∈ {0,236; 0,382; 0,618; 0,786}, `'1': min`, `'0': max`; `EMA_200 = Close.ewm(span=200, adjust=False).mean()`; `yf.download(stock, period='1y')`; düzeyler yatay çizgi olarak EMA200 ile aynı grafikte. Sinyal, giriş, stop yok; BIST30 listesi örnek (5 sembol). Parametre: Pencere = 1 yıl (kodda period='1y'; Ham ve başlık "6 aylık" diyor, çelişki); EMA200 span=200, adjust=False; oranlar 0,236 / 0,382 / 0,618 / 0,786 (görsel, açıldı)
  - `tweet-fibonacci-seviyeleri-python-kodu-1847621973553144140` — Aynı hesap, başka bir kod parçası (@BorsaSeker'e yanıt; Ham yalnız hesap adı, üst gönderi notta yok): `second_level = max_value - difference * 0.382` (görsel, açıldı). `max_value = df['Price'].max()`, `min_value = df['Price'].min()`, düzey = max − fark × r, %100 = min. Bu kodda %78,6 yok, %50 var. Pencere, sinyal, giriş, stop yok. Aralık uçları kapanış mı fitil mi belli değil (kolon 'Price'). Parametre: Fibonacci oranları (bu kod) = 0,236 / 0,382 / 0,5 / 0,618; %100 = min; 0,786 yok (görsel, açıldı)
  - `tweet-kfein-ema-100-200-fibonacci-giris-1775158969461350491` — EMA ve Fibonacci seviyelerinin giriş planında kullanımı (02.04.2024): "Şimdi adım adım Önce 100EMA ardından 200EMA'ya doğru geliyor. İşte oradan girerim arkadaş. 86'da pusuya yattım." (Ham). Görselde Fibonacci 0 = 208,89, 1 = 86,16; EMA100 = 115,43, EMA200 = 84,57, kapanış 128,30 (görsel, açıldı). Giriş düzeyi Fib 1,0 ile EMA200'ün çakıştığı bölgedir; EMA100 da Fib 0,786 (112,42) yakınındadır (konfluans limit girişi, YORUM). Önceki beklenti "78tl dolayında" (fiyat 150 iken) bugünkü 86 ile aynı değil. Stop, hedef, sonuç yok. Parametre: Giriş ≈ 86 TL (limit, "pusu"); basamak sırası EMA100 (115,43) → EMA200 (84,57); Fib 1,0 = 86,16 (Ham ve görsel, açıldı)

---

## 26. Siyah Kuğu (bullish): oran aralıkları ve hedef bandı

- Kaynak: `tweet-black-swan-fibo-618-100-hedef-bandi-1870475673585795531` (Ham ve görsel, açıldı; Tansu'nun X gönderisi, 21.12.2024).
- Tansu'nun ifadesi (verbatim): "Benim beklentim 9644.60'da düşüşün son bulması ve seneyi 10069.34 ile 10257.40 arasında bir yerde kapatmamız." (Ham). Görsel başlığı "Bullish Black Swan Found"; etiketler: "AB/XA = 0.48 (Target: 0.382-0.724)", "BC/AB = 3.15 (Target: 2.0-4.237)", "CD/BC = 0.40 (Target: 0.5-0.886)", "Target Price: 9644.60", "Fibo 100%: 10257.40", "Fibo 61.8%: 10069.34"; bacaklar XA 801.80, AB −388.60, BC 1225.60, CD 492.30 (görsel, açıldı).
- Tanım: (ölçüm, bizim hesabımız; görselin sayılarıyla tutarlı) AB/XA = 388,6 / 801,8 = 0,485; BC/AB = 1225,6 / 388,6 = 3,154; CD/BC = 492,3 / 1225,6 = 0,402. Hedef fiyat 9644,60 = C − 0,5 × BC = 10257,40 − 612,80 (YORUM: CD/BC alt sınırı 0,5). Fibo 100% = C tepesi (10257,40). Fibo 61,8% = D + 0,618 × (C − D) = 10069,34, burada D = 10257,40 − 492,30 = 9765,10; bu §11 TP formülüyle (r = 0,618 ve 1,000) aynıdır.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| AB/XA | 0,382–0,724 | görsel, açıldı |
| BC/AB | 2,0–4,237 | görsel, açıldı |
| CD/BC | 0,5–0,886 | görsel, açıldı |
| Hedef fiyat | 9644,60 | görsel, açıldı; formül YORUM |
| TP seviyeleri | D + 0,618 × (C − D) ve C | görsel, açıldı; formül ölçüm |
| Sembol, zaman dilimi | yok (fiyat ≈8.600–10.300, tarih Kasım–Aralık 2024) | görsel |

- Belirsiz kalanlar: Sembol ve zaman dilimi yazılı değil. Örnekteki CD/BC = 0,40 değeri kendi hedef aralığının (0,5–0,886) altındadır; "Found" etiketi bu halde de yazılmıştır, hedef fiyat alt sınırdır, CD bacağı henüz bitmemiş olabilir (YORUM). Giriş, stop, pivot kuralı ve oran toleransı yok.
- Tansu'nun kanıtı: yok (beklenti cümlesi; sonuç yok; 10069,34–10257,40 bandı bir tahmindir).
- Günlük bedava veriyle uygulanabilir mi: evet (oranlar ve TP hesabı); pivot kuralı olmadan tarama kurulamaz. §13 ve §21'in kaynaklarında Kuğu oranı yoktu; bu not bullish tarafın ilk sayısal aralıklarını verir. Beyaz Kuğu (bearish) aynası yok (YORUM).
- Kaynak güveni: Ham ve görsel birinci el; seçilmiş tek örnek: orta. Hazırlık K.

---

## 27. Elliott 0-1-a-b-c: c dibi, 1. tepe direncini al seviyesi yapma ve iki aşamalı plan (LIDFA, AKBNK)

- Kaynak: `tweet-elliott-0-1-abc-kirilim-tarama-al-seviyesi-1986543299692237038` (Ham ve iki görsel; G1 açıldı, G2 aynı çizimin yakın görüntüsü, metni aynı; 06.11.2025), `tweet-elliott-1-tepe-kirilim-iki-asamali-plan-1986859079348924623` (Ham ve görsel, açıldı; 07.11.2025), `tweet-elliott-dip-sinyali-al-seviyesi-direnc-1986552596094468452` (AKBNK, 06.11.2025; Ham ve görsel, açıldı). Üçü de Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim): "bu dipte sinyal aldık" ve "seviyenin geçilmesi ile 3. itki dalgasının ikinci hareketi de başlamış olur" (Ham, 06.11). "Alış noktası olan 1. tepenin yaklaşması bize satış için hazır kıta bekleyin der" (Ham, 06.11). İkinci gönderi: "pozisyonumun bir kısmını satarak kârımı realize ederim" (1. tepeye yaklaşınca) ve "Fiyat, "1 (Tepe)" direncini güçlü bir mumla yukarı yönlü kırdığında ve ideal olarak üzerinde kapanışlar yapmaya başladığında, bu benim için 3. Dalga'nın başladığının teyididir." (Ham, 07.11). AKBNK gönderisi: Ham "Portföyde bir banka olsun". Görsel (LIDFA, açıldı): "LIDFA - ELLIOTT KIRILIM TARAMASI (0-1-a-b-c)", "Periyot: HAFTALIK | Düzeltme: -15.6%", "AL SEVİYESİ (DİRENÇ): 4.37 TL"; etiketler 0 (Dip), 1 (Tepe), a, b, c (Dip 2); lejant İtki (0-1), Düzeltme (a-b-c), EMA(9), RSI(14). Görsel (AKBNK, açıldı): `AKBNK - ELLIOTT DİP SİNYALİ` / `Periyot: HAFTALIK | Düzeltme: -21.4% | AL SEVİYESİ (DİRENÇ): 69.75 TL`; aynı etiketler (`0 (Dip)`, `1 (Tepe)`, `a`, `b`, `c (Dip 2)`), 69,75 düzeyinde mavi yatay çizgi, sağda kırmızı yukarı ok.
- Tanım: (YORUM; sıra Ham ve görsellerden) 1. Haftalık grafikte 0 (dip) → 1 (tepe) itkisi. 2. a-b-c düzeltmesi; c (Dip 2) 0'ın üstünde biter (Ham 07.11: "trendin sağlığı açısından olumlu"). 3. Düzeltme yüzdesi = c / 1. tepe − 1: LIDFA −%15,6 (hesap: 4,37 × 0,844 ≈ 3,69; görselde c ≈ 3,7), AKBNK −%21,4 (hesap, piksel: 54,8 / 69,75 − 1 ≈ −%21,4). 4. İlk sinyal c dibinde (tetikleyici yok). 5. AL SEVİYESİ = 1. tepe direnci (LIDFA 4,37 TL; AKBNK 69,75 TL): yaklaşınca pozisyonun bir kısmı satılır; güçlü mumla kırılıp üzerinde kapanışlar gelirse 3. dalga başlamış sayılır, kalanla devam edilir veya satılan geri alınır (hatta eklenir). Gerekçe: fiyatın direnci ilk denemede geçememe riski. Görsel (2. gönderi, açıldı): 0 (Dip), 1 (Tepe), a, b, c (Dip 2), mavi kesikli direnç, "3. Dalga Hede" (kesik); sayı yok.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Zaman dilimi | haftalık | görsel, açıldı |
| Düzeltme | LIDFA −%15,6; AKBNK −%21,4 | görsel, açıldı |
| Al seviyesi | 1. tepe direnci (LIDFA: 4,37 TL; AKBNK: 69,75 TL) | görsel, açıldı |
| Kırılım teyidi | "güçlü mum" ve "üzerinde kapanışlar" (eşik yok) | Ham |
| EMA(9), RSI(14) | çizilir; rolü yazılı değil | görsel |
| Kısmi satış oranı, stop, hedef, min ve max düzeltme eşiği | yok | YORUM |

- Belirsiz kalanlar: c dibini nasıl anlayacağız (pivot kuralı yok). c'nin 0'ın üstünde kalması zorunlu mu. "Güçlü mum" ve "kapanış sayısı" tanımı. Kısmi satış oranı. Stop (c dibi altı mı?). Hedef. "Dip 2" için en çok kabul edilen geri alım sınırı. Kırılış ölçütü (kapanış, tampon): AKBNK etiketi "AL SEVİYESİ (DİRENÇ)" kırılış mı, tepki mi demek belli değil (YORUM). Etiket çelişkisi: tarama kırılım seviyesine "AL SEVİYESİ" der (Ham: "Alış noktası olan 1. tepe"), plan ise c dibinde ilk alımı ve 1. tepede kısmi satışı anlatır; iki ayrı alım noktası var gibi okunur (YORUM: dipte ilk alım, kırılımda ikinci alım). Sayım otomasyon aracının çıktısıdır; tarama koşulu yazılı değil.
- Tansu'nun kanıtı: yok (iki örnek, sonuç yok; LIDFA'da son mum ≈4,2–4,3, seviyenin altında).
- Günlük bedava veriyle uygulanabilir mi: haftalık mum günlükten türetilir ve seviye hesabı kolaydır; dalga sayımı ve pivot tanımsız, kural olarak hayır. TASARIM §3 Elliott'u kapsam dışı bırakır.
- Kaynak güveni: Ham ve görsel birinci el; düşük-orta. Hazırlık K.

---

## 28. Elliott 0-5 itkisi sonrası ABC düzeltmesi: Fibonacci merdiveni, C teyidi ve P-BOM girişi (IDGYO, CRDFA)

- Kaynak: `tweet-elliott-abc-fib-oranlari-c-teyidi-2094008240824635656` (IDGYO, 30.08.2026; Ham ve görsel, açıldı), `tweet-elliott-abc-hedef-rr-2094496543860564136` (IDGYO, 31.08.2026; Ham ve üç görsel, G1 ve G2 açıldı), `tweet-elliott-abc-uyumsuzluk-donus-1998113575009726965` (08.12.2025; Ham ve iki görsel, açıldı), `tweet-elliott-expanded-flat-c-teyit-p-bom-2094052769493582241` (CRDFA, 30.08.2026; Ham ve görsel, açıldı). Hepsi Tansu'nun X gönderisi (birinci el).
- Tansu'nun ifadesi (verbatim):
  - IDGYO (Ham): "Yeni dipler gelmedi bana kalırsa C teyit oldu zaten BOM sinyalim de teyit vermişti." "Dikkatle izleyelim bu hafta". İkinci gönderi: "Bence hikaye bitmedi".
  - IDGYO başlığı (görsel, açıldı): `IDGYO | ELLIOTT 0-1-2-3-4-5-A-B-C` / `Pattern #1 | C Tarihi: 21.08.2026 | Wave 2 Retracement: %86.4 | Wave 4 Retracement: %52.8 | Wave3/Wave1: 2.69 | Wave5/Wave1: 1.44 | C/0-5: %110.4`. Merdiven etiketleri: `W3→W4 %23.6 4.97`, `%38.2 4.65`, `%50.0 4.39`, `%52.8 4.33`, `%61.8 4.13`, `%78.6 3.77`; `ABC 0→5 %23.6 4.95`, `%38.2 4.62`, `%50.0 4.35`, `%61.8 4.07`, `%78.6 3.69` (ikinci gönderide 3.68); `5→A / B Gerçek %37.9 4.63`; `0→5 / C Gerçek %110.4 2.95`. Kırmızı kutu: C sonrası küçük mumlar. İkinci gönderide G1: `SUPPLY / ARZ 5.42 - 5.50`, `DEMAND / TEST EDİLDİ 2.97 - 3.04`.
  - IDGYO hedef etiketleri (görsel, açıldı): C sonrası mor küçük `(1)` ve `(2)`; `HEDEF V2 #1 3.36 | 4.8p | R:R 1.09`, `HEDEF V2 #2 3.22 | 3.4p | R:R 0.29`, `HEDEF V2 #3 3.58 | 1.6p | R:R 2.39`.
  - CRDFA (Ham): "B dalgası önceki tepeyi aşmış, C ise neredeyse başlangıç seviyesine kadar geri gelmiş bu yüzden yapı Expanded Flat'e benziyor. 25,16 şu an C adayı ama henüz yeni oluştuğu için teyitli dip diyemiyorum. Burada P-BOM sinyalini ararım ben (benim yazdığım sinyal)"; "hemen alım yapmak yerine önce C'nin korunmasını, sonra küçük 1-2 yapısının oluşmasını ve o küçük 1 tepesinin kırılmasını beklerdim. 24,50 altı (A) ise ana sayım açısından ciddi bozulma olur."; "C noktasının teyit almasını bekliyoruz, şu an için işlem erken, agresif bir giriş olur". Görsel (açıldı): `B DİRENCİ / GÜÇLÜ TEYİT 45.88`, `ÖNCEKİ 4. DALGA 36.34-36.96`, `0→5 / C Gerçek %96.3 25.16`, `GEÇERSİZLİK 25.16`, aynı yüzde merdiveni (`D3→D4`, `A-B-C 0→5`).
  - Haftalık ABC (Ham, 08.12.2025): "Haftalık abc düzeltmesin yapmış bir elliot abimiz. uyumsuzluklar da var artık gitsin bu yaç." Görsel 1: 0-5 itkisi ve A-B-C (etiket). Görsel 2 (açıldı): düşen üst çizgi ve yatay alt çizgili fiyat, altında üç osilatör panelinde yükselen dip çizgileri (fiyat daha düşük dip, osilatör daha yüksek dip: pozitif uyumsuzluk görünümü, YORUM); osilatör adları yok.
- Tanım:
  1. Aralık: 0 = itki başı, 5 = itki sonu. Merdiven seviyeleri `ABC(r) = P5 − r×(P5 − P0)`, r ∈ {0,236; 0,382; 0,50; 0,618; 0,786}. Hesap kontrolü (bizim, IDGYO: P0≈3,20, P5=5,50): 4,96 / 4,62 / 4,35 / 4,08 / 3,69; etiketlerle uyumlu. `W3→W4(r) = P3 − r×(P3 − P2)` (P2≈3,31, P3≈5,48): 4,97 için uyumlu. Oranlar §17'deki Wave 4 oranlarına (0,24 / 0,38 / 0,50) 0,618 ve 0,786 ekler.
  2. Gerçekleşen oranlar (aracın başlığı; hesap kontrolü bizim, piksel, YORUM): W2 geri alımı = (P1−P2)/(P1−P0) ≈ 0,86; W4 geri alımı = (P3−P4)/(P3−P2) ≈ 0,53; W3/W1 ≈ 2,7; W5/W1 = (P5−P4)/(P1−P0) ≈ 1,46 (başlık 1,44); C/0-5 = (P5−C)/(P5−P0) = 1,104 (C, P0'ın altına iner).
  3. C teyidi (Tansu, sözel): C'den sonra yeni dip gelmemesi (IDGYO), C'nin korunması (CRDFA). Bu bir kapanış kuralı değil, gözlemdir.
  4. P-BOM girişi (CRDFA, sözel): C korunur → küçük 1-2 yapısı oluşur → küçük 1 tepesi kırılınca al. Agresif giriş ("hemen alım") erken sayılır. P-BOM'un formülü verilmedi (A §16: BOM formülü yok).
  5. Hedef merdiveni V2 (IDGYO, YORUM, piksel ölçümüyle ters çözüm): W1' = (1) − C ≈ 0,22; hedefler (2) + k×W1' ile uyumlu: #2 = 1,0 (3,22), #1 = 1,618 (3,36), #3 = 2,618 (3,58). R:R etiketleriyle tutarlı giriş ≈ (1) tepesi ≈ 3,17 ve stop ≈ (2) dibi ≈ 3,00: (3,36−3,17)/(3,17−3,00) ≈ 1,1; 3,22 için ≈ 0,3; 3,58 için ≈ 2,4. Bu çözüm Tansu'nun yazdığı bir kural değil.
  6. Uyumsuzluk teyidi (08.12.2025, sözel): haftalık ABC bittikten sonra osilatör uyumsuzluğu dönüş işareti sayılır. Osilatör, pivot ve süre belirtilmedi.
  7. Geçersizlik: IDGYO'da C 2,95 aracın `0→5 / C Gerçek` çizgisidir; CRDFA'da görselde `GEÇERSİZLİK 25.16` (C'nin kendisi), Ham'da `24,50 altı`. İkisi aynı değildir (Belirsiz kalanlar).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Merdiven oranları | 0,236 / 0,382 / 0,50 / 0,618 / 0,786 (ABC 0→5 ve W3→W4) | görsel, açıldı |
| Ek "gerçek" etiketleri | W4 %52,8; B (5→A) %37,9; C/0-5 %110,4 (IDGYO), %96,3 (CRDFA) | görsel, açıldı |
| IDGYO ölçüleri | W2 %86,4; W4 %52,8; W3/W1 2,69; W5/W1 1,44 | görsel, açıldı |
| V2 hedefleri (IDGYO) | 3,22 / 3,36 / 3,58; R:R 0,29 / 1,09 / 2,39 | görsel, açıldı |
| V2 çarpanları | 1,0 / 1,618 / 2,618 × küçük W1 | YORUM (piksel) |
| "p" sütunu (3,4p / 4,8p / 1,6p) | anlamı bilinmiyor | görsel, açıldı; YORUM |
| Demand bölgesi (IDGYO) | 2,97–3,04, "test edildi" | görsel, açıldı |
| CRDFA düzeyleri | C adayı 25,16; B 45,88; önceki 4. dalga 36,34–36,96; iptal "24,50 altı" | Ham ve görsel, açıldı |
| Pivot ve sayım kuralı, osilatör, süre | bilinmiyor | YORUM |

- Belirsiz kalanlar: P-BOM'un tanımı; "teyit" ölçütü (kaç gün yeni dip yok?); küçük 1-2 yapısının pivot kuralı; uyumsuzluk osilatörü; "p" anlamı; CRDFA'da iptal seviyesi: Ham "24,50 altı (A)" der, görsel `GEÇERSİZLİK 25.16` yazar; görselde A ≈ 33,8 ve 24,50 nokta 0'a denk (piksel), yani Ham'ın "(A)" etiketi görseldeki A'ya uymaz; üç değer birbirini tutmaz (YORUM: görsel esastır); C'nin P0'ın altına inmesi (IDGYO %110,4) ile Elliott'un klasik "Dalga 2/ABC sınırı" arasındaki ilişki.
- Tansu'nun kanıtı: sonuç yok. IDGYO ve CRDFA bekleyen kurulumlardır ("işlem erken", "dikkatle izleyelim"). Tek örnekler, seçilmiş.
- Günlük bedava veriyle uygulanabilir mi: merdiven ve oranlar evet (OHLC ve pivot). Dalga sayımı, P-BOM ve uyumsuzluk için pivot kuralı ve formül gerekir; şimdi uygulanamaz.
- Kaynak güveni: Ham ve görsel birinci el; sayısal parametreler görselden okundu, yorumlar YORUM işaretli. Hazırlık K.

---

## 29. Elliott taramaları: C (ABC bitişi) taraması ve 3. itki dalgası taraması (IPEKE, AEFES, ASGYO, HURGZ)

- Kaynak: `tweet-elliott-itki-abc-taramasi-1984331550519910770` (IPEKE, 31.10.2025), `tweet-elliott-ucuncu-dalga-baslangici-1947614735068770788` (ASGYO, 22.07.2025), `tweet-elliott-ucuncu-dalga-taramasi-1949043393927024960` (HURGZ, 26.07.2025), `tweet-elliott-ucuncu-itki-taramasi-1950934573468025012` (31.07.2025). Hepsi Tansu'nun X gönderisi (birinci el); Ham ve görseller açıldı (dördüncü gönderide görsel yok).
- Tansu'nun ifadesi (verbatim):
  - 3. itki: "Elliot C taraması değil, 3.itki dalgası taraması yapın. Getirileri daha iyi." (Ham, 31.07.2025).
  - 3. dalga taraması (Ham, 26.07.2025): "#python ile elliot 3. dalga taramasında 23.07 de yaptığımız taramada #hrgaz çıkan hisselerden biri idi. %12 prim vermiş 2 güne. Doğrusu bunlara hiç geriye dönüp bakmıyorum çoğu güzel prim veriyor." ASGYO gönderisi (Ham, 22.07.2025): "konu bu kadar basittir."
  - Görsel (açıldı): kapanış çizgisi grafiği; `ASGYO.IS - 3. Dalga Başlangıcı: 2024-07-17`, `HURGZ.IS - 3. Dalga Başlangıcı: 2024-07-23`; lejant `Close Price`, `1. Tepe (B)` (kırmızı yatay kesik çizgi), `3. Dalga Başlangıcı` (yeşil dikey nokta çizgi); turuncu noktalar son iki dip (iki dip yakın) ve 1. tepe çizgisi üzerinde bir nokta. İkinci görsel TradingView mum grafiği (yeşil mumlar, kırmızı yukarı ok).
  - C taraması (IPEKE, Ham, 31.10.2025): "Elliot taramamız #ipeke bugün tavan yapmış:) Gerçi bunu gruba da vermemiştim henüz hala deneme süreçlerinde." Görsel: `IPEKE - ELLIOTT WAVE (1-2-3-4-5 + A-B-C) SIRALI | Impulse #1: +36.7% | Corrective: -14.8%`; AEFES'te aynı şablon: `Impulse #1: +21.6% | Corrective: -24.0%`.
- Tanım (YORUM, görselden): iki tarama türü vardır. (a) C taraması: tamamlanmış 1-2-3-4-5 itkisi ve ardından A-B-C düzeltmesi; sinyal C dibinde. (b) 3. dalga başlangıcı taraması: kapanış serisinde 1. tepe (B) çizgisi ve ikinci dip (iki yakın dip) sonrası yukarı kırılış 3. dalganın başlangıcı sayılır; tarih etiketi bu başlangıç günüdür. Kırılış ölçütü, pivot kuralı ve süre yazılı değil. Tansu'nun "çoğu güzel prim veriyor" cümlesi sayısal tablo vermez.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Taramanın çıktı alanları | Impulse %, Corrective % (IPEKE +36,7 / −14,8; AEFES +21,6 / −24,0) | görsel, açıldı |
| 3. dalga göstergesi | 1. tepe (B) çizgisi, 3. dalga başlangıç tarihi | görsel, açıldı |
| HURGZ sonucu | %12 prim, 2 gün | Ham |
| Tarama eşikleri, pivot, kırılış ölçütü | bilinmiyor | YORUM |

- Belirsiz kalanlar: tarama koşulu; "prim" neye göre (hangi giriş fiyatı); "getirileri daha iyi" karşılaştırması sayısal değil; Temmuz 2025'te 3. itki taraması önerilirken Ekim 2025'te C taraması deneme sürecinde (YORUM: ikisi paralel mi, görüş mü değişti, belli değil). Görsel başlıklarındaki tarih yılı (2024) ile gönderi yılı (2025) uyuşmaz (ASGYO: görsel 2024-07-17, gönderi 22.07.2025; HURGZ: görsel 2024-07-23, gönderi 26.07.2025); yıl farkı açıklanmamış, TradingView ekranı ayrı bir görseldir. Ham HURGZ için "#hrgaz" yazar, görselde HURGZ.IS görünür.
- Tansu'nun kanıtı: HURGZ %12 (2 gün), IPEKE tavan; seçilmiş vakalar. "Getirileri daha iyi" iddiası ölçülmemiş.
- Günlük bedava veriyle uygulanabilir mi: kapanış serisiyle evet; sayım ve pivot kuralı olmadan uygulanamaz.
- Kaynak güveni: Ham ve görsel birinci el; kural yok, güven düşük. Hazırlık X.

---

## 30. X arşivi kısa kayıtları (16.10)

- Elliott: işlem için avantajlı dalgalar 3, 5, A ve C (`tweet-elliott-3-5-a-c-avantajli-dalgalar-2093964129438404912`; Ham ve görsel birinci el, görsel açıldı; Tansu'nun X gönderisi, 30.08.2026; görsel başlığı "ELLIOTT WAVE PROJESİ | Çalışma Özeti"): Tansu: "Not almak yiğidin şanındandır, her ne kadar kod yazsak da geleneksel bir yanım her zaman daha ağır basar:) Paylaşayım kilit bilgileri." (Ham). Görsel: "6. En Avantajlı Dalgalar: 3, 5, A ve C"; "Trading açısından en önemli fikir, her dalgayı trade etmeye çalışmak yerine bir üst derecedeki trend yönünde hareket eden daha avantajlı dalgaları seçmektir."; "Ana prensip: Beş dalgalı hareket büyük trendin yönünü gösterir; üç dalgalı karşı-trend hareket ise o trende yeniden katılmak için setup sağlar." Tablo (görsel, açıldı): Wave (2) düzeltmesinden sonra Wave (3), Wave (4) düzeltmesinden sonra Wave (5) (ana trend yönü; "genellikle en güçlü" ve "ikinci yüksek güvenli" motive hareket); Wave (5) tamamlanınca Wave (A) (üst derece düzeltmenin başlangıcı); Wave (B) düzeltmesinden sonra Wave (C) (düzeltmenin ana yönüne katılmak). Sayı yok. Dalga sayımı ve doğrulaması, giriş, stop, hedef, "yüksek güvenli" ölçüsü yok. "6." madde numarasıdır; 1–5 notta yok. Görselin üreticisi belli değil (YORUM: Tansu kendi çalışma notu der, görselde araç damgası yok). A ve C satırları düşüş yönlü işlemdir; BIST'te açığa satış pratik değildir (TASARIM §3). İlk iki satır §16 (Wave 2'den Wave 3'e) ve §17 (Wave 4'ten Wave 5'e) ile aynı çerçevenin genel gerekçesi olarak okunur (YORUM). Günlük veriyle: kavram olarak evet; dalga sayımı otomasyonu tanımsız, kural olarak hayır (TASARIM §3 Elliott'u kapsam dışı bırakır). Hazırlık X. Kaynak güveni: ilke düzeyi: düşük-orta.
- Elliott beş dalga tamamlanışı ve kanal direnci uyarısı (AGESA; `tweet-bes-dalga-kanal-direnci-uyarisi-1986050444750119097`; Ham ve görsel, açıldı; Tansu'nun X gönderisi, 05.11.2025): "#AGESA haftalık" ve "Ben diyeceğimi diyeyim de sonra aman neden bizi uyarmadın olmasın" (Ham). Görsel başlığı: "AGESA.IS — DİRENÇ YAKININDA" ve "(30 Bar | 1 Impulse, 0 Tam Desen)" (görsel, açıldı). YORUM (Tansu kural yazmaz): haftalık grafikte 0-1-2-3-4-5 beş noktalı itki sayılır; 5. nokta (≈219) kırmızı üst kanal çizgisine değer, yeşil alt çizgi buna yaklaşık paraleldir; etiket "DİRENÇ YAKININDA": fiyat kanalın üst sınırındadır. Uyarı yeni alım yerine düzeltme riskini anlatır (yön sözle yazılmaz). Paneller: RSI(14) (≈75–80, görsel okuma), ADX/DI(14), MACD Histogram. Parametre: tarama penceresi 30 bar (görsel); zaman dilimi haftalık (Ham); RSI(14), ADX/DI(14) (görsel). Kanal çizgisinin çizim kuralı, "yakın" toleransı, "Tam Desen" tanımı, uyarının eylemi ve eşik yok. 5. dalga tamamlanınca A dalgasını bekleyen Elliott ilkesiyle uyumlu okunabilir (YORUM). Tansu'nun kanıtı: yok (tek uyarı; sonuç yok). Günlük veriyle: haftalık mum günlükten türetilir; kanal ve beş dalga sayımı tanımsız, kural olarak hayır. Hazırlık X. Kaynak güveni: düşük.

---

## 31. 144 barlık Fibonacci %78,6 tepki taraması: birleşim koşulları ve onay (düşen trend kırılımı, EMA20 yukarı kesişimi, ADX/ADXR)

- Kaynak: `tweet-fibo-78-6-tepki-ema20-onay-1842476377670398430` (05.10.2024), `tweet-fibo-786-tepki-dusen-trend-kirilimi-1843986596464607478` (09.10.2024), `tweet-fibo-786-bandi-tepki-taramasi-1844077720344666261` (09.10.2024), `tweet-fibo-786-tepki-tarama-144-bar-1844105075427508357` (09.10.2024), `tweet-fibo-786-tepki-ema20-kesisim-1845917612494197175` (14.10.2024), `tweet-fibo-786-yakinlik-adx-adxr-tarama-1845918165743948244` (14.10.2024). Hepsi Tansu'nun X gönderisidir (birinci el). Temel sistem ve gösterge ekranı §23'tedir.
- Tansu'nun ifadesi (verbatim): "fiyatın 78.6'dan tepki alması da tek başına yeterli değil. En azından orta vadeli yükseliş için EMA20'nin üzerine atmasını beklerim. EMA50'ninde üzerine çıkarsa daha tatlı olur." (Ham, 05.10.2024). "Fibo 76.8 desteğine düşmüş ve oradan tepki almış aynı zamanda düşen trendi kırmış hisse taraması bitti bitecek.@fiboborsa stratejisi." (Ham, 09.10.2024 12:07). "Tek koşul 78.6 dan tepki alması. Diğer hiç bir koşul zaten hiç bir hissede tutmuyor." ve "Bu taramaya düşeni kıran kodu ya yazmaya çalışıyorum ama hala bitmedi." (Ham, 09.10.2024 18:09). "trend dönüşü için son gün ema20'yi yukarı kessin koşuşu getirdim ama hiç bir hisse sağlamadı. Fakat pozitif bir uyumsuzluk yakaladım. Ben karışmam" (Ham, 09.10.2024 19:58). "Son gün fibo 78.6'ya temas etmiş ve tepki alarak yükselmiş, ve son gün ema20'yi yukarı kesmiş olsun. Tek bir hisse çıktı" (Ham, 14.10.2024 20:00; görsel metni: GEDIK). "76.8 üstü yakında kapatsın, ema20 son gün şartını kaldırdım ve adx/adxr ilave ettim grafiklere." (Ham, 14.10.2024 20:02; sonuç GEDIK ve JANTS).
- Tanım (YORUM, Ham'dan): taban tarama §23'teki gibidir: son gün kapanışı 144 barlık %78,6 düzeyine yakın ya da düzeye temas edip tepkiyle yukarı kapatmış. Tansu bu tabana koşul ekleyip çıkarır; koşul kümeleri: (a) taban + düşen trend çizgisi kırılımı (09.10; "düşeni kıran" kodu bitmedi); (b) taban + son gün EMA20'yi yukarı kesmek (09.10: sıfır hisse; 14.10: bir hisse, GEDIK); (c) taban + kapanışın düzeyin üstünde ve yakın olması, EMA20 şartı kaldırıldı, ADX/ADXR grafiğe eklendi (14.10 20:02); (d) insan onayı: tepkiden sonra fiyatın EMA20 üstüne, tercihen EMA50 üstüne çıkması (05.10). Tansu'nun "ema20'yi yukarı kessin" ifadesi, fiyatın (kapanışın) EMA20'yi yukarı kesmesi olarak okunur (YORUM; EMA20'nin EMA50'yi kesmesi değil). "Tepki" ve "temas" tanımı yazılı değil.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Pencere | son 144 bar | Ham (§23) |
| Taban koşul | %78,6 düzeyinden tepki ("tek koşul") | Ham |
| Trend kırılımı koşulu | düşen trend kırılımı; çizgi tanımı yok, kod bitmedi | Ham |
| EMA20 koşulu | son gün EMA20'yi yukarı kesmek (09.10 ve 14.10; sonra kaldırıldı) | Ham |
| Onay (el ile) | EMA20 üstü en az; EMA50 üstü daha iyi | Ham |
| ADX/ADXR | grafiğe eklendi; eşik yok | Ham |
| Giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: "tepki" ve "temas" tanımı; "yakında kapatsın" mesafesi (±%2 bandı mı); düşen trend çizgisinin seçimi; kesişimin kapanışla mı gün içiyle mi sayıldığı; "pozitif bir uyumsuzluk" hangi göstergede (RSI mı?); 09.10.2024 18:09 gönderisindeki "76.6" yazımı %78,6 mı alt bant etiketi mi (YORUM: %78,6 yazım yanlışı); onay EMA20 üstünde kaç gün kalmayı ister. Notlardaki "76.8" yazımı, seri boyunca görsellerdeki %78,6 düzeyidir (Ham yazım hatası, YORUM).
- Tansu'nun kanıtı: yok; tarama sayımı anlatılır: yalnız tepki koşuluyla 9 sembol (09.10, görsel metni); EMA20 kesişim koşuluyla 0 (09.10) ve 1 (14.10) sembol. "Diğer hiç bir koşul zaten hiç bir hissede tutmuyor" cümlesi koşulların sıkı olduğunu söyler, getiri ölçümü değildir. Sonuç, giriş, stop yok.
- Günlük bedava veriyle uygulanabilir mi: evet (OHLC, EMA, ADX; 144 günlük en yüksek ve en düşük değer). Kural yarım: koşul listesi kısmen kodlanmış, kalan koşullar tanımsız.
- Kaynak güveni: Ham birinci el (Tansu'nun X gönderisi); "@fiboborsa stratejisi" ibaresi stratejinin kaynağını başkasına atfeder (YORUM: temel fikir @fiboborsa'dan, birleşim koşulları Tansu'dan). Kural yarım: düşük. Hazırlık K.

---

## 32. Tüm Fibonacci düzeylerinde destek dönüşü ve direnç kırılımı taraması, bir üst düzey hedefi ve uzatma düzeyleri

- Kaynak: `tweet-fibo-destek-donusu-direnc-kirilimi-tarama-1909130007827317168` (07.04.2025; Ham ve görsel, açıldı), `tweet-fibo-seviye-donus-kirilim-tarama-ema-1908969053529457002` (06.04.2025; Ham ve görsel, açıldı), `tweet-fibonacci-78-6-kirilim-hedef-61-8-1908505150668370269` (05.04.2025; Ham ve iki görsel, açıldı), `tweet-fibonacci-uzanti-hedefi-1950637105606173073` (30.07.2025; Ham ve görsel, açıldı). Hepsi Tansu'nun X gönderisidir (birinci el). 144 barlık %78,6 sistemi §23'tedir.
- Tansu'nun ifadesi (verbatim): "Tüm fibo seviyelerinden dönüş ve yukarı kırılımları da taratıyoruz:)" (Ham, 06.04.2025). "İşte böyle tek ter taratıyoruz." (Ham, 07.04.2025; tablo görseli). "78.6 bölgesinde güzel bir asılı adım, kırılınca hedef 10.22" (Ham, 05.04.2025; MEPET). "FİBO kodunuzu doğru yazarsanız yakalarsınız." (Ham, 30.07.2025; ANELE). Tablo görseli (açıldı): başlık satırı `Hisse | Tarih | Sinyal | Kapanış | Fibonacci Seviyesi | Fibo Değeri`; tarih 2025-04-04; örnek satırlar: `A1CAP.IS | 2025-04-04 | 61.8% DESTEK dönüşü | 4,900 | 61.8% | 4,81`, `AKSGY.IS | 2025-04-04 | 38.2% DİRENÇ kırılımı | 6,900 | 38.2% | 6,86`, `ASUZU.IS | 2025-04-04 | 78.6% DİRENÇ kırılımı | 60,650 | 78.6% | 60,15`, `BRYAT.IS | 2025-04-04 | 50.0% DESTEK dönüşü | 2.045,000 | 50.0% | 2035,5`.
- Tanım (YORUM, görsel ve hesap): Fibonacci düzeyi yüksekten düşüğe: `Fib(r) = H − r × (H − L)`, r ∈ {0,236; 0,382; 0,5; 0,618; 0,786}; %0 üstte (H), %100 altta (L). Doğrulama (bizim, A1CAP görseli): H = 5,60, L = 4,32; %61,8 → 5,60 − 0,618 × 1,28 = 4,81 (tabloyla aynı); %78,6 → 4,59. Tarama, her hisse için bu beş düzeyden birini sinyal olarak etiketler: "DESTEK dönüşü" (düzeye inip üstünde kapanış, YORUM) ya da "DİRENÇ kırılımı" (kapanışın önceki dirençken düzeyi yukarı geçmesi, YORUM). Tablo gözlemi (hesap): 15 satırın hepsinde kapanış düzeyin üstünde; DİRENÇ kırılımı satırlarında fark +%0,3 ile +%1,6, DESTEK dönüşü satırlarında +%0,5 ile +%8,8; yani iki etiket yalnız uzaklıkla ayrılmaz (YORUM). Hedef: kırılan düzeyin bir üstündeki düzey; MEPET örneğinde %78,6 (9,00) kırılırsa hedef %61,8 = 10,22 (14,72 − 0,618 × (14,72 − 7,44) = 10,22; hesap). Uzatma: ANELE grafiğinde %0'ın üstünde "138.2%" ve "161.8%" çizgileri; piksel ölçümüyle düzey = H + 0,382 × (H − L) ve H + 0,618 × (H − L) (YORUM).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Fibonacci düzeyleri | %23,6 / %38,2 / %50,0 / %61,8 / %78,6 (+ %0 ve %100 uçları) | görsel, açıldı |
| Sinyal tipleri | DESTEK dönüşü; DİRENÇ kırılımı | görsel, açıldı |
| Yön | yüksekten düşüğe (%0 = H) | görsel, açıldı |
| Kırılım hedefi | bir üst düzey (%78,6 → %61,8; MEPET 10,22) | Ham ve görsel, açıldı |
| Uzatma düzeyleri | %138,2 ve %161,8 (ANELE) | görsel, açıldı |
| Pencere, tolerans, iki etiketin ayırıcısı, giriş, stop | yok | - |

- Belirsiz kalanlar: aralık penceresi (144 bar mı, 1 yıl mı, 2 yıl mı; bkz. `tweet-fibonacci-vadeye-gore-baslangic-tarihi-1908510592639398132`'daki vadeye göre seçim, §23); "dönüş" ve "kırılım" ayrımı; kırılımın kapanışla mı fitille mi sayıldığı; EMA 50/200 (A1CAP grafiği) ve EMA 5/8/13 (MEPET grafiği) çiziminin sinyalde rolü; hedefin her düzey için bir üst düzey mi olduğu (tek örnek); uzatma düzeylerinin hangi aralıktan ve hangi koşulda hedef olduğu; stop. Görsel metni, değer ve etiket sırasını kaydırmıştır (görselde sol değer, sağ etiket); alttaki etiket "100.0%" (kırpık), metin "0.0%" yazıyor; %0 çizgisi (5,60) etiketsizdir. Not adı %61,8 hedefini söyler; Ham yalnız "10.22" yazar, %61,8 eşleşmesi görselden hesaplanmıştır.
- Tansu'nun kanıtı: yok; tablo bir tarama çıktısıdır, sonuç yok. MEPET ve ANELE tek örnek, seçilmiş. ANELE'de fiyat 138,2 düzeyine kadar çıkmış, son mum kırmızı (görsel, açıldı); Tansu bunu "yakalarsınız" diye gösterir, getiri rakamı yok.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC, en yüksek ve en düşük değer, EMA). Sinyal tanımı eksik; pencere belirsiz.
- Kaynak güveni: Ham ve görsel birinci el; kural yarım: düşük. Hazırlık K.

---

## 33. Fibonacci %161,8 uzantısı: haftalıkta dip yakalama taraması (fiyat üzerinde ve RSI üzerinde)

- Kaynak: `tweet-haftalik-fibonacci-161-8-tarama-kodu-1839048874960232959` (zincir, üç gönderi, 25.09.2024; Ham ve dört görsel, açıldı), `tweet-rsi-uzerinde-fibonacci-seviyeleri-kod-1839043892399735295` (25.09.2024; Ham ve görsel G2 ile G3, açıldı), `tweet-rsi-fibo-1618-dip-1839233105141326179` (yanıt, 26.09.2024; Ham), `tweet-rsi-fibo-haftalik-1618-1840032038734454942` (yanıt, 28.09.2024; Ham), `tweet-supertrend-most-rsi-fibo-1618-haftalik-tarama-1840058987263279534` (28.09.2024; Ham, görsel yok), `tweet-rsi-fibonacci-161-8-donus-1842924571504390342` (06.10.2024; Ham ve görsel, açıldı), `tweet-rsi-fibo-1618-kodu-1843356247476842791` (07.10.2024; Ham), `tweet-rsi-fibonacci-161-8-seviyesi-1845047340807184621` (yanıt, 12.10.2024; Ham). Hepsi Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim):
  - RSI kodu (Ham, 25.09.2024): "Önce meraklısına şunu paylaşayım. RSI ile fibo seviyelerini belirlemek." "Fibo 161,8 seviyesinde bir hisseyi haftalıkta yakalarsak tatlı bir şey olabilir." "Taraması da bitti gibi."
  - Fiyat taraması (Ham, 25.09.2024): "Haftalık periyotta 161,8 fibo seviyesinde ya da yakın olan hisselerin taraması. Fibo bu sefer RSI ile değil fiyat ile hesaplanmıştır". Zincir: "Haftalık verilere yeniden örnekleme yaptık ve bu veriler üzerinden Fibonacci seviyeleri hesapladık." "Eğer fiyat, %161.8 seviyesindeyse sonuçlara ekledik."
  - Anlam (Ham, yanıt, 26.09.2024): "Fibo 161.8, teorik olarak dibi ifade ediyor. Ama mutlaka grafiğe bakın". 28.09.2024: "rsi ile fibo hesaplayıp haftalık 1.618 de yakalarsak çözeriz".
  - Supertrend ve MOST niyeti (Ham, 28.09.2024): "Ulaşmaya çalıştığım sistem; Supertrend most ve rsi ile hesaplanan fibo kodunu Haftalıkta 1.618'e temas etmiş hisseleri bulmak için taratacağız." "Sonra pozitif çıkan hisselerin grafiklerini tarama sonucu olarak çıktısını alacağız." Fibo çapasının (iki uç nokta) Supertrend, MOST ve RSI'dan nasıl türetildiği yazılı değil; üç göstergenin rolü, ayarları ve temas tanımı (High mı, Close mu) yok (YORUM: bu not aynı haftalık 1,618 taramasının niyet düzeyindeki ek sürümüdür; kod ve sonuç gösterilmemiş).
  - Strateji atfı (Ham, 06.10.2024, başlık "DÜZELTME"): "Bir hissede RSI'a çizilen Fibo ile geri dönüşü 161.8'de yakalayın, parayı vurun :)"; "@fiboborsa'nın stratejisidir."; "Taraması da hazır"; "(Yeşil RSI, Mavi Fiyat)".
  - Kod durumu (Ham, 07.10.2024): "161.8'i bulun keyfinize bakın." "Taramasında bir sorun var." Tek hisse veya birden çok hissede grafik yazdırılabilir; tarama kodu üzerinde çalışılıyor (kod bağlantısı harici, notta yok). 12.10.2024: "rsi a fibo çekin, rsi'da 161.8'i yakalayın".
  - Görsel (görsel, açıldı): TUPRS grafiğinde RSI seviyeleri `0.0% (96.22)`, `23.6% (73.51)`, `38.2% (59.46)`, `50.0% (48.11)`, `61.8% (36.76)`, `78.6% (20.59)`, `100.0% (0.00)`; 161.8% çizgisi grafikte yok. Tarama çıktısı: AKFGY 2.04 / 1.266847; CANTE 1.63 / 0.888133; HLGYO 2.53 / 1.388315; IHLGM 1.25 / 0.767960; SASA 4.33 / 2.965765; VKGYO 1.86 / 1.082949; ZOREN 4.31 / 2.623200 (fiyat / Fibonacci 161.8%).
- Tanım (kod görselleri, açıldı):
  1. Düzeyler: `diff = high − low`; `r%` = `high − r×diff` (r = 0,236; 0,382; 0,5; 0,618; 0,786); `100%` = low; `161.8%` = `low − 0,618×diff` (aralığın dibinin 0,618 aralık altı, yani 1,618 uzantısı).
  2. Fiyat taraması: yaklaşık 100 sembollü `.IS` listesi; `yf.download(symbol, period='1y')`; `resample('W')` (Close = last); `fib_high = Close.max()`, `fib_low = Close.min()`; koşul `seviye161 − 2 <= son kapanış <= seviye161 + 2`.
  3. RSI üzerinde: haftalık yeniden örnekleme, `calculate_rsi(window=14)` (basit `rolling(window).mean()`, `min_periods=1`); `fib_high = RSI.max()`, `fib_low = RSI.min()` (1 yıllık haftalık seri); fiyat mavi, RSI yeşil, düzeyler kırmızı kesik çizgi; örnek sembol ALARK.IS.
  4. Hesap kontrolü (bizim): (a) Fiyat taramasında son kapanış, min kapanıştan küçük olamaz; fark en az 0,618 × (max − min) olur. Fiyat 161,8 düzeyine değemez; ±2 TL mutlak tolerans yalnız 0,618 × (max − min) ≤ 2 olan, yani aralığı dar ve fiyatı düşük hisseleri geçirir. Çıktıda fiyat − düzey = 0,77 / 0,74 / 1,14 / 0,48 / 1,36 / 0,78 / 1,69 TL; yedi hissenin hepsi 4,33 TL ve altında. (b) RSI üzerinde 161,8 düzeyi 0'ın altına iner, RSI ona değemez: düzeyin ≥ 0 olması için RSI min ≥ 0,382 × RSI max gerekir. TUPRS görselinde min 0,00 ve max 96,22; 161,8% ≈ −59,5. `min_periods=1` ilk barlarda RSI'ı 0 veya 100'e itebilir ve aralığı şişirir (ALARK grafiğinde seri başı ≈100; YORUM).
  5. Okuma (YORUM): "Fibo 161.8, teorik olarak dibi ifade ediyor" cümlesi, RSI'ın kendi aralığının altına uzanan bir uzantı düzeyi anlamına gelir; ancak (4b) nedeniyle yalnız RSI aralığı dar olduğunda ölçülebilir. Aynı yöntemin 2025'teki hali günlük 144 gün penceresi ve 0,786 / 0,618 / 0,382 düzeyleridir (bkz. §34).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| 161,8 düzeyi | low − 0,618 × (high − low) | kod, açıldı |
| Fiyat penceresi | 1 yıl, haftalık kapanış (resample W, last) | kod, açıldı |
| Fiyat taraması toleransı | ± 2 (mutlak fiyat birimi, TL) | kod, açıldı |
| RSI | 14, basit ortalama, min_periods=1, haftalık | kod, açıldı |
| RSI aralığı | 1 yıllık haftalık RSI max ve min | kod, açıldı |
| Evren | ≈100 sembol (Ham: "BIST 30") | kod, açıldı |
| Supertrend, MOST, RSI ayarları (28.09.2024 niyeti) | bilinmiyor | - |
| Giriş, stop, hedef, çıkış | yok | - |
| RSI 161,8 için okuma kuralı ve onay | bilinmiyor | YORUM |

- Belirsiz kalanlar: "yakalamak" tolerans ölçüsü RSI tarafında yok; giriş, stop, hedef ve çıkış yok; "dip" ile "geri dönüş" arasındaki fark (dönüş onayı yok); 2024 kodu haftalık 1 yıl, 2025 gönderileri günlük 144 gün (iki yöntem yan yana, hangisi geçerli belli değil); 06.10.2024'te "Taraması da hazır", 07.10.2024'te "Taramasında bir sorun var" (tarama durumu çelişkili); strateji @fiboborsa'ya atfedilir, Tansu'nun kendi buluşu değil; Supertrend, MOST ve RSI ile hesaplanan Fibo çapası (28.09.2024).
- Tansu'nun kanıtı: yok. Tarama çıktısı yalnız taramaya giren 7 hissedir; sonraki fiyat ve getiri verilmedi. "parayı vurun" vaat dilidir.
- Günlük bedava veriyle uygulanabilir mi: veri evet (haftalık kapanış, RSI). Kural olarak hayır: fiyat taramasında hesap kusuru var (4a), RSI tarafında düzey çoğu kez ulaşılamaz (4b) ve giriş, stop, hedef yok. Supertrend ve MOST sürümü, çapa belirsiz olduğundan şimdi uygulanamaz.
- Kaynak güveni: Ham ve kod birinci el; kural yok, güven düşük. Hazırlık X.

---

## 34. RSI üzerinde 144 günlük Fibonacci: 0,786 ve 0,618 dönüşü, 0,382 reddi, mum teyidi ve tarama

- Kaynak: `tweet-rsi-144-fibo-0382-red-kayan-yildiz-1986917436310909146` (XU100, 07.11.2025; Ham ve görsel, açıldı), `tweet-rsi-144-gun-fibonacci-momentum-destek-direnc-1986826801885167861` (zincir, iki gönderi, 07.11.2025; Ham), `tweet-rsi-144-gun-fibo-0618-donus-stop-1977450129008251116` (FLAP, 12.10.2025; Ham ve görsel, açıldı), `tweet-rsi-fibo-0618-donus-taramasi-1977423987274617023` (EKOS, 12.10.2025; Ham ve görsel metni), `tweet-rsi-144-fibo-786-mum-formasyonu-1911906987341910274` (14.04.2025; Ham ve görsel, açıldı), `tweet-rsi-fibo-786-reversal-scan-1912136481751056753` (15.04.2025; Ham ve görsel, açıldı), `tweet-rsi-fibo-786-donus-giris-cikis-1912151798992814185` (15.04.2025; Ham), `tweet-rsi-fibo-786-candle-pattern-1912933957592834220` (17.04.2025; Ham ve görsel metni). Hepsi Tansu'nun X gönderisidir (birinci el). Uzun Ham metinleri şablonlu, açıklayıcı bir dille yazılmıştır (yapay zekâ özeti gibi okunur, YORUM); Tansu'nun gönderisi olarak birinci el sayıldı.
- Tansu'nun ifadesi (verbatim):
  - 0,786 dönüşü (Ham, 15.04.2025): "RSI’ya çekilen 144 günlük Fibonacci düzeltmesinde 0.786 seviyesi, klasik fiyat grafiğindeki 0.786’dan çok daha yüksek stratejik öneme sahiptir." "RSI, 0.786 Fibo seviyesinden yukarı dönerse, bu genellikle momentum tabanlı dip anlamına gelir." "Giriş için: RSI’nin 0.786 seviyesinden yukarı kıvrılması ve bu dönüşün 1-2 mumla teyit edilmesi beklenebilir." "Çıkış için: RSI’nin yeniden 50-60 bandına gelmesi ya da fiyatın önceki short-term dirençlerine yaklaşması beklenebilir."
  - Tarama (Ham, 15.04.2025): "Rsi’a çekilen 144 günlük Fibo 0.786 dip dönüş ve bullish mum" taraması, bir önceki günün sonuçları. Görsel (görsel, açıldı): ULKER 110,20 (−1,61), TMPOL 79,95 (7,46), MERKO 16,24 (9,95), KENT 823,50 (0,00), FRIGO 7,69 (1,45).
  - 0,786 ve mum (Ham, 14.04.2025): "RSI değeri daha önce aşırı satım bölgesine yaklaştıktan sonra toparlanmış ve %78.6 Fibonacci düzeltme seviyesinden yukarı tepki vermiş." "Fibonacci 78.6 seviyesi, teknik analizde genellikle son savunma hattı olarak görülür." "Oluşum 11 Nisanda tamamlanmış ve bugün güzel tepkisini vermiş." Mumlar (görsel, açıldı): CDLCLOSINGMARUBOZU, CDLBELTHOLD (Ham'da yazım: "DLCLOSINGMARUBOZU"). 17.04.2025 (Ham): "RSI 786 dönüşü mum formasyonları daha ne olsun:)"; mum etiketleri CDLENGULFING, CDLBELTHOLD (görsel metni).
  - 0,618 dönüşü (Ham, 12.10.2025): "Önce son 144 günün RSI verilerini alıyoruz. En yüksek RSI değerini ve en düşük RSI değerini buluyoruz. Aradaki farkın yüzde 61.8'ini hesaplıyoruz. Sonra en yüksek değerden bu miktarı çıkarıyoruz." "RSI bu seviyeden destek alıp yukarı dönmeli. Bir önceki güne göre artış göstermeli." "Çekiç, yutan boğa, sabah yıldızı gibi formasyonlar varsa teyit güçlenir." "Fiyat 50 günlük ortalamanın üzerindeyse daha sağlam zemin demektir." "Genelde son düşük seviyenin yüzde 2-3 altına stop koyarız." Görsel (görsel, açıldı): `FLAP.IS - RSI Fibonacci 0.618 Tepki Sinyali (Son Gün: 2025-10-10)`; `Fibo 0.236: 66.7`, `0.382: 57.9`, `0.500: 50.8`, `0.618: 43.8`, `0.786: 33.7`, `1.000: 20.8`; fiyat grafiğinde `BELTHOLD` etiketi.
  - 0,618 taraması (Ham, 12.10.2025): "fibo 0.618 dönüş taraması sonucu pazartesi gelen güzel tepki." EKOS, görsel başlığı `RSI Fibo 61.8 Dönüş & Mum Grafik (Son gün: 2025-10-06)`, mumlar CDLENGULFING, CDLBELTHOLD (görsel metni).
  - Genel model (Ham, 07.11.2025): "yoruma dayalı bir modeldir"; seviyeler "momentum destek ve direnç" seviyeleridir. Boğada RSI "38.2% veya 50%" düzeyine düşüp yukarı dönerse destek bulmuştur; ayıda "50% veya 61.8%" düzeyine çıkıp aşağı dönerse direnç bulmuştur. "Fiyat hala yükseliyor gibi görünürken, RSI kendi 61.8 Fibonacci direncini geçemiyorsa (negatif uyumsuzluk), bu, trendin yakında yorulacağına dair güçlü bir erken uyarı sinyalidir." Fiyat 144 günlük ortalama desteğindeyken RSI 50% düzeyindeyse çift onaydır. "mutlaka geçmiş verilerle test edilmesi (backtesting)" gerekir.
  - 0,382 reddi (Ham, 07.11.2025, XU100): Fibo 0,382 (61,6) "momentumun 144 günlük hareket bandı içindeki ilk ve en önemli yapısal direnç seviyesidir"; RSI "70 seviyesine (aşırı alım) bile ulaşamadan" bu seviyeden döndü. Fiyat panelinde yükselişin tepesindeki mum Kayan Yıldız (Shooting Star). Sonuç: "İkili Teyitli Negatif Sinyal". Görsel (görsel, açıldı): `Fibo 0.000 (Max): 79.4`, `0.236: 68.4`, `0.382: 61.6`, `0.500: 56.1`, `0.618: 50.7`, `0.786: 42.9`, `1.000 (Min): 32.9`; ek göstergeler `En İyi Destek (SMA 17)` ve `Fiyat Dipleri (n=40)`.
- Tanım (YORUM, Ham ve görsellerden):
  1. Girdi: günlük RSI(14); son 144 günün en yüksek (`RSImax`) ve en düşük (`RSImin`) değeri.
  2. Düzey: `RSI_düzey(r) = RSImax − r × (RSImax − RSImin)`; r = 0 (max), 0,236, 0,382, 0,5, 0,618, 0,786, 1 (min). 0,786 ve 0,618 en düşüğe yakın dip bölgesidir; 0,382 ve 0,236 tepeye yakındır. Hesap kontrolü (bizim): XU100 (max 79,4; min 32,9): 0,382 → 61,64 (etiket 61,6); 0,618 → 50,66 (50,7); 0,786 → 42,85 (42,9). FLAP (max ≈ 80,9 etiketlerden çözüldü; min 20,8): 0,618 → 43,8 (etiket 43,8).
  3. 0,786 dönüş (dip) girişi: RSI 0,786 düzeyine iner, yukarı kıvrılır, dönüş 1–2 mumla teyit edilir. Mum teyidi bullish formasyondur (CDL... adları TA-Lib işlevi adlarıdır, YORUM). Çıkış: RSI 50–60 bandı veya fiyatın önceki kısa vadeli dirençleri (Ham). Tarama: "144 günlük Fibo 0.786 dip dönüş ve bullish mum".
  4. 0,618 dönüş girişi: RSI 0,618 düzeyine yaklaşır; hemen alınmaz; RSI desteği alıp bir önceki güne göre artış gösterince girilir. Ek teyit: çekiç, yutan boğa, sabah yıldızı; fiyat 50 günlük ortalamanın üstünde. Stop: son düşüğün %2–3 altı (Ham, "Genelde"). Hedef yok.
  5. 0,382 reddi: RSI dipten döner, 0,382'ye (61,6) ulaşıp aşağı kıvrılırsa momentum tükenmiştir; fiyatta tepe mumu (Kayan Yıldız) ile birlikte kısa vadeli negatif teyit. Giriş değil uyarı; çıkış veya azaltma kuralı yazılı değil.
  6. Genel okuma (Ham): RSI düzeyleri "momentum destek ve direnç" olarak okunur; RSI 61,8'i geçemezse negatif uyumsuzluk erken uyarısı, 50% düzeyi fiyat desteğiyle çakışırsa onay.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| RSI | RSI(14), günlük | görsel, açıldı |
| Pencere | son 144 gün | Ham ve görsel, açıldı |
| Düzey oranları | 0 (max), 0,236, 0,382, 0,500, 0,618, 0,786, 1,000 (min) | görsel, açıldı |
| Düzey formülü | RSImax − r × (RSImax − RSImin) | Ham (0,618 gönderisi) ve görsel hesabı |
| 0,786 girişi | RSI yukarı kıvrılır + 1–2 mum teyidi | Ham |
| 0,786 çıkışı | RSI 50–60 bandı veya önceki kısa vadeli direnç | Ham |
| 0,618 girişi | RSI düzeyden yukarı döner (önceki güne göre artış) | Ham |
| Mum teyidi | CDLCLOSINGMARUBOZU, CDLBELTHOLD, CDLENGULFING (görseller); çekiç, yutan boğa, sabah yıldızı (Ham) | Ham ve görsel |
| Fiyat filtresi | fiyat > 50 günlük ortalama | Ham (0,618 gönderisi) |
| Stop | son düşüğün %2–3 altı | Ham ("Genelde") |
| 0,382 uyarısı | RSI 61,6 düzeyinden döner, 70'e ulaşmaz | Ham ve görsel, açıldı |
| Tarama adı | "144 günlük Fibo 0.786 dip dönüş ve bullish mum" | Ham |
| Dönüş eşiği, yaklaşma toleransı, RSI hesap yöntemi, mum listesi | bilinmiyor | YORUM |

- Belirsiz kalanlar: "dönüş" tanımı (bir önceki güne göre artış mı, 1–2 mum teyidi mi) iki gönderide farklıdır; düzeye "yaklaşma" toleransı yok; RSI hesabı (Wilder mi basit ortalama mı; 2024 kodunda basit ortalama, 2025 kodu verilmedi); 0,618 gönderisinde düzey hem "direnç" hem "destek" diye anılır, giriş destek olarak kurulur (YORUM); 144 gün "yaklaşık 6 ay" (0,618 gönderisi) ve "6-7 ay" (genel model gönderisi) denir, 144 işlem günü yıl 252 gün alınırsa ≈ 6,9 aydır (hesap bizim); "bullish mum" süzgeci TA-Lib değerinin işaretine mi bağlı belli değil (başka bir tarama çıktısında CDLRICKSHAWMAN ve CDLHARAMI gibi yönü nötr olabilen mumlar da etiketli, YORUM); mum formasyonu zorunlu mu, ek teyit mi; stop için "son düşük" tanımı; hedef (yalnız 0,786 için çıkış bandı var); 0,786'nın klasik fiyat grafiğindeki 0.786'dan "çok daha yüksek stratejik öneme sahiptir" iddiası ölçülmemiş; tarama evreni ve sıralama; 0,382 reddinde RSI'ın düzeye değip değmediği (grafikte tepe ≈ 59–60, düzey 61,6; piksel, YORUM). Ham mum adını "DLCLOSINGMARUBOZU" yazar (baştaki C eksik); görselde CDLCLOSINGMARUBOZU.
- Tansu'nun kanıtı: yok (sistematik ölçüm yok). Seçilmiş vakalar: "Oluşum 11 Nisanda tamamlanmış ve bugün güzel tepkisini vermiş" (14.04.2025; sembol yok); EKOS "pazartesi gelen güzel tepki" (sayı yok); FLAP ve XU100 örnekleri sonuçsuz; tarama listesi (ULKER, TMPOL, MERKO, KENT, FRIGO) sonraki getiri vermez. Tansu'nun kendi uyarısı: "yoruma dayalı bir model", backtest gerekir.
- Günlük bedava veriyle uygulanabilir mi: veri evet (günlük kapanış, RSI, 144 günlük max ve min). 0,786 için giriş ve çıkış, 0,618 için giriş ve stop vardır; "dönüş" ve "yaklaşma" eşikleri varsayım gerektirir; hedef yok. Backtest şart (Tansu da der).
- Kaynak güveni: Ham ve görsel birinci el; düzey sayıları görselde açıldı ve hesapla doğrulandı. Yöntem Tansu'nun "yorum" modelidir, mekanik sinyal değildir; kural yarım, güven orta-düşük. Hazırlık K.
