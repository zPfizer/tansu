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

---

## 2. Pattern durum etiketleri ve tarayıcı çıktı tablosu

- Kaynak: `gorsel-paket-01` (görsel 01, 03, 05, 06, 09), `gorsel-paket-02` (görsel 01, 02), `gorsel-paket-03` (görsel 01), `tweet-harmonik-xb-trend-kirilimi-stratejisi` (KAPLM görseli).
- Tansu'nun ifadesi (birinci el):
  - Tablo başlığı: `Hisse | Tip | Sistem | Durum | Reaksiyon | D Hedefi | Giriş | Stop (X)`.
  - SOKE satırı: Tip `SAT (taktik KISA, D'ye kadar) — D'de AL'a döner`, Sistem `Pesavento` ve `Carney` (iki ayrı satır), Durum `AKTIF`, Reaksiyon `-`, D Hedefi `12.53`, Giriş `-`, Stop `-`.
  - LUKSK satırı: Tip `AL (Buy)`, Sistem `Pesavento` ve `Carney`, Durum `TAMAMLANDI`, Reaksiyon `TEPKI_VERDI`, D Hedefi `86.95`, Giriş `86.95`, Stop (X) `73.00`.
  - Grafik etiketleri: `D: 226,80 [TAMAMLANDI]`, `D: 11,29 [TAMAMLANDI]`, `D (hedef: 11.29 [TAMAM])`, `D (hedef: 10.05 [TAMAM])`, `D (hedef: 7.83 [BOZULDU])`, `D: 49.66 [AKTİF]`, `D (hedef) 70.25` (Backtest Modu).
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

- Belirsiz kalanlar: pattern oranları (Siyah Kuğu tanımı yok), giriş fiyatı ve tetikleyici, D'de otomatik giriş mi tepki teyidi mi, TP1 sonrası break-even stop'un işlem maliyeti.
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
  - Beyaz Kuğu ve Siyah Kuğu oranları kaynakta yok. Gartley, Butterfly veya başka kural yerine konamaz.
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
    - Hazır değil: konsept, oran veya kural yok. Siyah ve Beyaz Kuğu oranları hiçbir yerde yok.

Genel kanıt durumu: Tansu hiçbir harmonik kural için sistematik bir başarı tablosu göstermiyor. Tek sistematik tablo SMRTG (12 pattern) ve ISKPL (5 pattern), ikisi de tek hisse, maliyetsiz, stop kuralı bilinmiyor. Diğer örnekler seçilmiş pozitif vakalar (LIDER, AKCNS, 40, DOAS, KAPLM negatif dışında).

Ortak boşluklar (hepsi YORUM; kod öncesi karar):

1. Pivot kuralı: L, R, zikzak eşiği, `Swing=15 sol-only`'in harmonik tarayıcıya ait olup olmadığı.
2. Oran toleransı: Ham'da %3–5 vardır; birimi açık değildir. Yaklaşık %10 aday seçimi YORUM'dur; MAKIM ve DGATE'den genel tolerans çıkarılamaz (Ham, G123:49; Araç, G122/g1).
3. `BOZULDU`, `TEPKI_VERDI` ve `BELİRSİZLEŞTİ` eşikleri.
4. Stop kuralı (X, XA 1,13, `X−2*ATR`).
5. Siyah ve Beyaz Kuğu oran tanımı.

Küçük sonraki adım: kural 3 ve 4 için kendi pivot kararınızı yazın (L, R), sonra KRPLS D=11,29 ve D=10,05 değerlerini fiyat verisinden yeniden üretin.

---

## 22. Omuz-baş-omuz (OBO), kısa kayıt (bilet 04, 14.10)

- Kaynak: `gorsel-paket-121-obo-neckline-hacim-hedef` (yalnız görsel, metin yok; infografik okundu, kaynak imzası yok). Sıralı kısa listede (§21) yoktur.
- Görsel metni (Ham görseli; imzasız infografik, Ham'da yazar yok): `4 Adımda Omuz Baş Omuz (OBO) Formasyonu`. (1) Üç tepeyi tespit et: sol omuz, daha yüksek baş, daha alçak sağ omuz. (2) Boyun çizgisini çiz: omuzlar ile başın taban dip noktalarını birleştiren destek çizgisi. (3) Kırılımı onayla: fiyat boyun çizgisini hacimli bir mumla aşağı kırarsa formasyon onaylanır. (4) Hedef: baş tepesi ile boyun çizgisi arasındaki mesafe kadar düşüş beklenir. "Hacmi kontrol et": sağ omuz oluşurken hacmin azalması güvenilirliği artırır.
- Tanım: hedef = boyun çizgisi − (baş − boyun çizgisi) (kırılım noktasından aşağı).
- Parametreler: yok. Pivot ayarı, omuz benzerlik toleransı, "hacimli" eşiği, kırılım tamponu, stop yok (YORUM).
- Tansu'nun kanıtı: yok (şema; piyasa örneği yok). Bu kural aşağı yönlü dönüş formasyonudur; BIST'te açığa satış pratik değil (TASARIM 3).
- Günlük bedava veriyle uygulanabilir mi: evet (OHLCV). Kaynak güveni: düşük (şema).
