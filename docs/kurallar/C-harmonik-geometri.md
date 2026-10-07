# C — Harmonik ve Geometrik Formasyon Kuralları (Tansu)

Durum: araştırma çıktısı. Kod yazılmadı. Tarih: 2026-10-05.

## 0. Okuma kuralları

Klasör: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\` (kısaltma: `HAVUZ`).
Görsel klasörü: `HAVUZ\assets\<klasör>\`. Not dosyası: `HAVUZ\<not>.md`.

Güven etiketleri:

| Etiket | Anlam |
| --- | --- |
| birinci el | Görseldeki başlık, etiket, tablo veya kod. Görseli açıp doğruladım. |
| ikinci el | Yalnız not dosyasında. Notlar çoğunlukla Claude özetidir. Tansu'nun metni "Levent iletisi" olarak aktarılmıştır; kelimesi kelimesine olduğu kanıtlanmadı. |
| ölçüm | Görsel etiketlerinden veya pikselden ben hesapladım. Hata payı var. |
| YORUM | Kaynakta yok. Boşluk. Kod yazmadan önce karar gerekir. |

Not: Üretici araç, Tansu'nun kendi taraması gibi görünüyor (Plotly grafik, Türkçe başlıklar, Pesavento ve Carney sistem etiketleri). Kod veya ham veri yok. Hiçbir görselde işlem maliyeti, ham OHLC veya pivot parametresi görünmüyor.

Önemli not–görsel çelişkileri (görsel kazanır):

1. `tweet-iskpl-abcd-cden-dye-backtest.md` 3. işlem C tarihini `2025-02-21` yazıyor. Görsel `2025-03-21` gösteriyor.
2. `gorsel-paket-111` notu "hafta sonu ve tatilleri sayımdan çıkarın, yalnız işlem günü sayın" diyor. Görselin kendi metni tersini söylüyor: "TAKVİM GÜNLERİNİ SAYIN ... hafta sonları ve tatiller dahil tüm günleri hesaba katın." Bkz. kural 18.
3. `gorsel-paket-123` tablosundaki D formülü (`X + (A−X)*0.786`, "Boğa için") bullish yapıda yönü yanlış. Tablonun kendi TP formülleri (`D+(A−D)*...`) D'nin A'nın altında olduğunu varsayıyor. Bkz. kural 7.

---

## 1. Swing-pivot tespiti (tüm kuralların temeli)

- Kaynak: `gorsel-paket-01` (görsel 03), `gorsel-paket-03` (görsel 01), `kaynak-doas-kelebek` (doas-kelebek.webp), `gorsel-paket-60-hidden-bullish-divergence` (görsel 01), `gorsel-paket-34` ve `-45` (başlıklar). Notlar: `tweet-abcd-geometrik-gecerlilik-kurallari`, `gorsel-paket-39`, `tweet-trend-cizgisi-swing-pivot-regresyon-zarf`.
- Tansu'nun ifadesi (birinci el, görsel etiketleri):
  - Lejant (KRPLS, SMRTG): `Swing Low` (mavi ▲), `Swing High` (turuncu ▼), `Swing Yapısı (HH/HL/LH/LL)`, `Swing (X -> A)`, `AB=CD Paterni`.
  - Başka bir aracın (gizli pozitif uyumsuzluk) üst etiketi: `... | Swing=15 sol-only | MinGap=15`.
  - Düşen direnç taramasının başlığı: `Kırılım: 2026-05-18 | Temas: 3 | Lookback: 20` (LIDER); `Temas: 3 | Lookback: 30` (BALAT).
- Tanım (görselden okunan davranış):
  1. İki ölçek var. Küçük ölçek: mum üstünde mavi ▲ (Swing Low) ve turuncu ▼ (Swing High) işaretleri. Büyük ölçek: kalın zikzak çizgi `Swing (X -> A)`. Zikzak köşeleri küçük işaretlerden azdır. Yani zikzak daha geniş bir eşikle üretiliyor. (ölçüm)
  2. Her zikzak köşesinin üstünde veya altında bir yapı etiketi var: `HH`, `HL`, `LH`, `LL`. Etiket, köşenin aynı türdeki önceki köşeye göre yüksek mi alçak mı olduğunu gösteriyor. DOAS örneği: X=`HL`, A=`LH`, B=`HL` (178,45 > X 170,10), C=`LH` (C < A 209,10). Bu okuma tutarlı. (ölçüm)
  3. Bir köşe birden fazla pattern'e hizmet edebiliyor. KRPLS'de Mayıs tepesinde `LH / C / B / A` yığını var. SMRTG'de `H/B/A`, `LH/C/A`. Bu, tarayıcının ardışık üç köşeyi (A,B,C) kaydırarak pattern aradığını gösteriyor. Aynı köşe farklı pattern'lerde A, B veya C olabiliyor. (ölçüm, YORUM)
  4. `MARKA - Patern #13` başlığı: pattern'lere sıra numarası veriliyor. Numara muhtemelen listedeki sırası. (YORUM)
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Swing penceresi (diverjans aracı) | `Swing=15`, `sol-only` | görsel (gorsel-paket-60/01). Harmonik tarayıcıya ait olduğu KANITLANMADI. |
| MinGap | 15 | aynı görsel |
| Lookback (düşen direnç tarayıcısı) | 20 (LIDER), 30 (BALAT) | görsel. Trend çizgisi için, pivot için değil. |
| Temas sayısı | 3 | görsel (trend çizgisi) |
| Harmonik tarayıcının pivot penceresi L/R | bilinmiyor | YORUM |
| Zikzak eşiği (yüzde, ATR) | bilinmiyor | YORUM |

- Giriş / stop / hedef: yok (altyapı kuralı).
- Belirsiz kalanlar:
  - `sol-only` ne demek? En makul okuma: pivot, yalnız soldaki 15 muma bakılarak bulunur (`low[i] <= min(low[i-15..i-1])`). Sağ teyit mumu yok. Bu durumda pivot "geçici" olabilir ve fiyat düşmeye devam edebilir. (YORUM). Not (`gorsel-paket-60`) da aynı riski belirtiyor (ikinci el).
  - `Swing=15`'in sayı birimi bar mı? Zaman dilimi? Bilinmiyor.
  - Harmonik tarayıcı aynı `Swing=15`'i mi kullanıyor? Görselden çıkmıyor.
  - Notlardaki `L/R` pencereli formül (`pivot_known_at = i + R`, alternatif high/low, min bar mesafesi, ATR belirginliği) Claude'un şablonudur. Tansu'nun kaynak metni sadece "lokal pivotları bulun" diyor, parametre vermiyor (`gorsel-paket-39`, ikinci el).
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
| `TEPKI_VERDI` | D sonrası beklenen yönde tepki oldu. | LUKSK satırı. Eşik görselde yok. |
| `TEPKİ GELMEDİ` / `BELİRSİZLEŞTİ` | D oldu, 20 bar içinde tepki yok. | KAPLM üst notu. |
| `Backtest Modu` | Eski bir C anına dönülüp pattern'in sonrası izleniyor. | MARKA başlığı, SMRTG "Tarih (C)" sütunu. (YORUM) |

- Giriş / stop / hedef: LUKSK için Giriş = D hedefi (86,95). Stop (X) = X fiyatı (73,00). Yani Gartley limit girişi D'de, stop X'te. SOKE aktif satırında giriş ve stop boş. Aktif pattern işlem sinyali sayılmıyor. (birinci el)
- Belirsiz kalanlar:
  - `BOZULDU` tetikleyicisi görselde yok. Tek aday: C'den sonra fiyatın A'yı aşması (kural 3, ikinci el).
  - `TEPKI_VERDI` için minimum hareket yüzdesi ve süre yok.
  - `Pesavento` ve `Carney` iki ayrı sistem etiketi. SOKE ve LUKSK'ta aynı D ve aynı giriş çıktı. Hangi oranlar farklı? Bilinmiyor. İsimler, Larry Pesavento ve Scott Carney'in oran setlerine gönderme olabilir (YORUM). Kitap doğrulaması yapılmadı (`900-Archive/Pesavento-Jouflas PDF Derin İnceleme.md`, "parse başlamadı").
  - "SAT (taktik KISA, D'ye kadar) — D'de AL'a döner": bullish Gartley'de D'ye kadar kısa, D'de al. Kısa tetikleyici kural 9'da.
- Tansu'nun kanıtı: etiketli örnekler. Sistematik değil. LUKSK tek tamamlanmış örnek.
- Günlük bedava veriyle uygulanabilir mi: evet (etiketler fiyat yolundan türüyor). Eşikler YORUM.
- Kaynak güveni: birinci el (etiketler, tablo). Yaşam döngüsü şeması ikinci el.

---

## 3. AB=CD geometrik geçerlilik (BC ≤ AB, D, B'nin ötesinde, A ihlali)

- Kaynak: `tweet-abcd-geometrik-gecerlilik-kurallari` (ikinci el), `gorsel-paket-39` (görsel 01, birinci el), `-38`, `-40`, `-42`, `-43`, `-45`, `-47`, `gorsel-paket-32`, `-34`, `-35`.
- Tansu'nun ifadesi:
  - Not içinde 4 madde (Levent iletisi, ikinci el): BC bacağı AB'yi aşamaz; BC/AB tam 1,00 olabilir; D, CD yönünde B'yi aşmalı; C oluştuktan sonra fiyat A'yı BC yönünde aşarsa pattern bozulur.
  - Yön şablonu (not, `gorsel-paket-39`, "Levent'in sonraki açıklaması", ikinci el): `BUY: A high → B low → C lower high → D lower low`, `SELL: A low → B high → C higher low → D higher high`.
  - Görsel etiketleri (birinci el): `D (CD=1.0AB)` (AKCNS, 39, 40, 35), `D (ALIM SİNYALİ - CD=1.0AB)` (42), `D (ALIM SİNYALİ - CD=1.27AB)` (RYSAS), `D (CD=1.27AB)` (32, 45, 47), `AB=CD (BUY)` (32 lejant).
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
| BC/AB üst sınır | 1,00 (dahil) | not (ikinci el) |
| BC/AB aday oranları | 0,382 / 0,500 / 0,618 / ... (açık uçlu) | not (ikinci el) |
| CD/AB (r) aday oranları | 1,000 / 1,270 / 1,618 / ... (açık uçlu) | not (ikinci el); görselde 1,0 ve 1,27 etiketi var |
| D, B'nin ötesinde | `r > q` | not türetimi |
| BC/AB gerçek örnekleri | 0,666 ; 0,878 ; 0,88 | ölçüm (KRPLS, MARKA). Yani 0,618'in üstü kabul ediliyor. |
| Oran toleransı | bilinmiyor | YORUM |
| D için PRZ aralığı | bilinmiyor | YORUM |
| Bozulma bazı (fitil / kapanış) | bilinmiyor | YORUM |

- Giriş / stop / hedef / bozulma: bkz. kural 4 (hedef merdiveni) ve kural 5 (backtest). Bozulma: C sonrası A aşıldı (not). Durum etiketi: `BOZULDU` (görsel).
- Belirsiz kalanlar:
  - `CD=1.0AB` ve `CD=1.27AB` aynı tarayıcıda mı? Etiketler iki farklı r değerini gösteriyor. Bir tarayıcı iki r'yi tarıyor olabilir (YORUM).
  - q üst sınırı: 0,878 örneği kabul edilmiş. Alt sınır? Bilinmiyor.
  - Not, BC/AB = 1,00 için r > 1 gerektiğini söylüyor. Görselde q=1 örneği yok.
  - Zaman simetrisi (`CD_bar / AB_bar`): kaynakta var ama isteğe bağlı, eşik yok (ikinci el).
- Tansu'nun kanıtı: seçilmiş örnekler (KRPLS, MARKA, AKCNS, 40, 42, RYSAS). Sistematik tek tablo: kural 5.
- Günlük bedava veriyle uygulanabilir mi: evet. Eksik: pivot, tolerans, bozulma bazı.
- Kaynak güveni: etiketler ve D formülü birinci el (ölçümle). Kural maddeleri ikinci el.

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
- Günlük bedava veriyle uygulanabilir mi: evet. Formül tam.
- Kaynak güveni: birinci el.

---

## 5. AB=CD C→D backtest (SMRTG 12, ISKPL 5, MARKA #13)

- Kaynak: `gorsel-paket-03` (02-smrtg-backtest-sonuclari.png), `tweet-iskpl-abcd-cden-dye-backtest` (01-iskpl-abcd-cden-dye-backtest.png), `gorsel-paket-01` (09-marka).
- Tansu'nun ifadesi (birinci el, araç çıktısı):
  - `BACKTEST SONUÇLARI (SMRTG)`: `Toplam patern sayısı : 12`, `Hedefe ULAŞAN : 7`, `Stop'a takılan / bozulan : 3`, `Henüz sonuçlanmamış (açık) : 2`, `Başlangıç sermayesi : 100,000.00 TL`, `Bitiş sermayesi : 405,327.42 TL`, `Toplam getiri : %305.33`.
  - ISKPL: 5 patern, 5 hedef, 0 stop, 0 açık. 100.000 → 710.006,23 TL. `%610.01`.
  - Sütunlar: `# | Tarih (C) | Sonuç | Getiri % | Sermaye`.
  - ISKPL metni (not, ikinci el): "1000 günlük taramada C noktasından alım, D hedefinde satış".
- Tanım (çıktıdan okunan):
  1. Pattern'in C noktasında giriş (tarih sütunu "Tarih (C)").
  2. Çıkış: D hedefine ulaşırsa `hedef`. Pattern bozulursa veya stop olursa `stop`. Hâlâ açıksa `açık`.
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
- ISKPL işlemleri (birinci el): 2024-04-03 +46,98; 2024-08-13 +56,67; **2025-03-21** +49,90; 2025-06-19 +45,37; 2026-01-21 +41,50 (not 02-21 yazmış, görsel 03-21).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Giriş noktası | C (tarih sütunu) | görsel |
| Hedef | D (r bilinmiyor) | görsel |
| Stop / bozulma kuralı | bilinmiyor | YORUM |
| Taranan pencere | "1000 günlük" (takvim mi seans mı belli değil) | not (ikinci el) |
| İşlem maliyeti | yok | görsel |
| Pozisyon büyüklüğü | tüm sermaye, sıralı | ölçüm |

- Belirsiz kalanlar:
  - Stop fiyatı. Getiriler −12 ile −25% arası. Stop fiyatı bilinmeden hesaplanamıyor. Aday: A'nın aşılması (YORUM, doğrulanamadı).
  - Hedef getirileri %24–51. D−C mesafesi C fiyatına bölünerek mi hesaplanıyor? Doğrulanamadı.
  - C anında gerçek zamanlı geçerlilik: C pivotu ancak sağ teyit sonrası bilinir. Backtest bunu uyguluyor mu? Bilinmiyor. Look-ahead riski.
  - Aynı anda açık pozisyonlar ve çakışma (SMRTG #7 ve #8 arası 7 gün).
  - Başlıkta `Harmonik sayı: 3.02 TL` (SMRTG) ve `6.31 TL` (A1CAP). Anlamı bilinmiyor.
- Tansu'nun kanıtı: tek hisse, seçilmiş. SMRTG 12 pattern (%58 hedef, kapalılarda %70). ISKPL 5/5. Out-of-sample yok. Maliyet yok. Hisse seçimi (neden SMRTG, ISKPL?) belirtilmemiş. ISKPL, "çok yüksek getiri" gösterdiği için seçilmiş olabilir (YORUM).
- Günlük bedava veriyle uygulanabilir mi: evet, yapı olarak. Stop kuralı olmadan birebir tekrar edilemez.
- Kaynak güveni: birinci el (sayılar). Yorumlar ikinci el.

---

## 6. CD bacağı şiddeti (araştırma sorusu)

- Kaynak: `tweet-abcd-cd-bacagi-siddet-belirleyicileri` (ikinci el).
- Tansu'nun ifadesi (ikinci el): "AB=CD'de C'den D'ye hareketin hızını, hedefe ulaşma olasılığını ... hangi erken bilgiler açıklar?" Soru. Veri, kural ve sonuç yok.
- Tanım: kural değil, hipotez listesi. (BC oranı, C anında sıkışma, B kırılım gücü, üst zaman trendi.)
- Parametreler: yok.
- Belirsiz kalanlar: hepsi.
- Tansu'nun kanıtı: yok.
- Günlük bedava veriyle uygulanabilir mi: araştırma olarak evet. Kural olarak kodlanamaz.
- Kaynak güveni: ikinci el. Sıralamada dışarıda.

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
| Stop Loss (SL) | X Noktası (veya XA 1.13) | Pozisyon Kapanışı (Invalidation) | `SL = X_Fiyat - ATR*2` |
| Take Profit 1 (TP1) | AD'nin %38.2'si | Pozisyonun %50'sini Kapat | `TP1 = D + (A-D) * 0.382` |
| Take Profit 2 (TP2) | AD'nin %61.8'i | Kalan Pozisyonu Kapat | `TP2 = D + (A-D) * 0.618` |

  - Ek (not, Levent iletisi, ikinci el): tolerans "%3–5" (BIST için Python/Excel); `reward/risk < 1,5` veya stratejiye göre `< 2` ise pattern doğru olsa da işlem reddedilir; D/PRZ = XA 0,786 ile BC 1,272/1,618 uzantısının kesişimi; risk = |D−X|.
  - Tarayıcı tablosu (birinci el, 02): LUKSK Gartley için Giriş = D hedefi = 86,95, Stop (X) = 73,00.
  - SAYAS detay grafiği başlığı (birinci el): `SAYAS - Patern #2 Detaylı (Fibonacci + Trade Management) | Bullish (LONG) | Sistem: Carney`. Lejant (okunurluk sınırlı): `Giriş (D)`, `İlk Stop (X)`, `TP1 (1:1 R/R)`, `TP2 (.618 AD)` (07.10 okuma düzeltmesi; ilk okuma "Bk Stop", ".618 CD").
- Tanım (bullish, hesaplanabilir; tablo ile düzeltilmiş yön):
  1. X=dip, A=tepe, `X < A`. `XA = A − X`.
  2. B: `AB/XA ≈ 0,618`. `B_beklenen = A − 0,618*XA`.
  3. C: `BC/AB ∈ [0,382 ; 0,886]`. Fiyat olarak `B + 0,382*AB <= C <= B + 0,886*AB`.
  4. D: `D = A − 0,786*XA` (X'ten 0,214 üstte). Tablodaki `X + 0,786*(A−X)` yanlış yönde (bkz. aşağı).
  5. Giriş: D'de limit alış. Stop: X (veya XA 1,13 uzantısı = `A − 1,13*XA`, veya `X − 2*ATR`). TP1 = `D + 0,382*(A−D)` (pozisyonun %50'si). TP2 = `D + 0,618*(A−D)` (kalan).
  6. R:R girişte hesaplanır, 1,5 (veya 2) altındaysa işlem yok.
- Yön hatası kanıtı (benim hesabım, ölçüm): X=100, A=200 olsun. Doğru D = 200 − 0,786*100 = 121,4. Tablo formülü: 100 + 78,6 = 178,6. Fark 57,2 birim. Tablonun TP formülleri (`D + (A−D)*r`) D'nin A'nın altında olmasını gerektirir. Yani tablo içinde kendisiyle çelişiyor. Büyük olasılıkla örnek formül hatası (YORUM).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| AB/XA | 0,618 | görsel (tablo) |
| BC/AB | 0,382 – 0,886 | görsel |
| D (XA retracement) | 0,786 | görsel |
| BC uzantısı (D/PRZ) | 1,272 / 1,618 | not (ikinci el) |
| CD/BC | 1,13 – 1,618 | not 122 ("yaygın örnek", Claude), Tansu değil |
| Stop | X, veya XA 1,13, veya X − 2*ATR | görsel (üç alternatif) |
| TP1 | AD'nin 0,382'si, pozisyonun %50'si | görsel |
| TP2 | AD'nin 0,618'i, kalan | görsel |
| SAYAS TP1 / TP2 | 1:1 R/R ; 0,618 AD | görsel (07.10 yeniden okundu) |
| Tolerans | %3–5 | not (ikinci el). Oran mı, fiyat mı belli değil. |
| Min R:R | 1,5 (veya 2) | not (ikinci el) |
| n_period (X için) | bilinmiyor | YORUM |
| ATR periyodu | bilinmiyor | YORUM |

- Giriş / stop / hedef / bozulma / durum: yukarıda. Durum: `AKTIF` → `TAMAMLANDI` → `TEPKI_VERDI` (kural 2). Bozulma: D, X'i aşağı kırarsa Gartley kimliği bozulur (genel kural; Tansu'dan açık söz yok, YORUM).
- Belirsiz kalanlar:
  - Stop üç farklı: X, XA 1,13 (`A − 1,13XA = X − 0,13XA`), `X − 2ATR`. Tabloda "veya". Hangisi tarayıcıda? Tarayıcı çıktısı "Stop (X)" yazıyor (birinci el, 02), yani X.
  - TP: bu tablo AD üzerinden. BALAT (kural 11) CD üzerinden. SAYAS "0,618 AD" (07.10 okuma düzeltmesi; eski okuma "CD" idi). İki farklı TP çapası: AD ve CD. Hangi sistem hangisi? Bilinmiyor.
  - MAKIM "Yükseliş Gartley" etiketi (birinci el, 122): bacak etiketleri `X->A: 2.11`, `A->B: -1.43`, `B->C: 0.68` (okunurluk sınırlı; 0,68 mi 0,88 mi), `C->D: -1.25`. Etiketler fiyat farkı ise: AB/XA = 1,43/2,11 = 0,678 (0,618'den %9,7 sapma); CD/BC = 1,84. Bu, tabloda önerilen %3–5 toleransla uyuşmaz. Tarayıcının gerçek toleransı en az ~%10 olabilir (YORUM, ölçüm).
  - Tolerans oran mı fiyat mı? Tablo formülü fiyat farkını `Tolerans` ile kıyaslıyor. Metin "%3–5" diyor.
- Tansu'nun kanıtı: LUKSK (TEPKI_VERDI), SOKE (aktif), SAYAS (uzun grafik). Başarı oranı yok.
- Günlük bedava veriyle uygulanabilir mi: evet. En iyi tanımlı harmonik kural seti (oranlar, giriş, stop, TP). Tolerans ve pivot kararı gerekir.
- Kaynak güveni: tablo birinci el. Tolerans ve R:R ikinci el.

---

## 8. Kelebek (Butterfly)

- Kaynak: `kaynak-doas-kelebek-2096505383955079277` (doas-kelebek.webp, tweet: The_Tansu_/status/2096505383955079277, 2026-09-06), `gorsel-paket-01` (06-dgate-kelebek-al-aktif.jpg), `tweet-alark-125-42` (metin).
- Tansu'nun ifadesi:
  - DOAS tweeti (not, tweet metni kısa: "DOAS ve kelebek"; ikinci el) ve grafik etiketleri (birinci el): `0.0 (A): 209.10`, `0.236: 199.90`, `0.382: 194.20`, `0.500: 189.60`, `0.618: 185.00`, `0.786: 178.45`, `1.0 (X): 170.10`, `1.272 (D hedefi): 159.49`, `1.618 (max risk): 146.00`, `D: 159.40 [TAMAMLANDI]`.
  - DGATE (birinci el): `Kelebek Formasyonu (AL (Buy)) [AKTİF] — SİSTEM: Pesavento`, alt yazı `X→B trend çizgisi: Kırılım: AŞAĞI yönde, 2026-08-18 tarihinde`, `D: 49.66 [AKTİF]`.
  - ALARK (not, ikinci el): "bearish butterfly'a doğru ilerliyor, 125,42'ye kadar long fırsatı, pullback izlenecek." Oran yok.
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
- Günlük bedava veriyle uygulanabilir mi: kısmen. D = 1,272 XA ve B ≈ 0,786 net. Diğer oranlar ve toleranslar YORUM.
- Kaynak güveni: DOAS seviyeleri birinci el. ALARK ikinci el.

---

## 9. X–B trend çizgisi kırılımı (D'ye kadar taktik pozisyon)

- Kaynak: `tweet-harmonik-xb-trend-kirilimi-stratejisi` (KAPLM, 01-kaplm-xb-trend-kirilimi.jpg), `gorsel-paket-02` (SOKE Carney), `gorsel-paket-01` (DGATE alt yazısı).
- Tansu'nun ifadesi:
  - Not (ikinci el): X ve B noktalarından geçen çizgi uzatılır. Bullish yapıda çizgi aşağı kırılırsa D'ye kadar short, bearish'te çizgi yukarı kırılırsa D'ye kadar long. Not "mekanik oran ve giriş kuralları kaynakta verilmedi" diyor.
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
| Kırılım bazı (kapanış / fitil) | bilinmiyor | YORUM |
| Tampon (ATR, tick) | bilinmiyor | YORUM |
| Stop, hedef | D hedefi (hedef), stop yok | görsel: SOKE'de Giriş/Stop `-` |

- Giriş / stop / hedef: hedef = D. Giriş ve stop bilinmiyor (SOKE aktif satırında boş).
- Belirsiz kalanlar: kapanış mı fitil mi, tampon, stop, kısa pozisyonun kapanış kuralı, BIST'te açığa satış zorluğu (YORUM; Tansu "taktik kısa" diyor, aracı belli değil).
- Tansu'nun kanıtı: KAPLM tek örnek. Çizgi kırıldı, fiyat ~420'ye düştü (D), tepki gelmedi. Kısa kısmı çalışmış görünüyor ama getiri gösterilmemiş.
- Günlük bedava veriyle uygulanabilir mi: evet. Çizgi hesabı kolay. Kırılım tanımı YORUM.
- Kaynak güveni: etiketler birinci el, kural metni ikinci el.

---

## 10. D sonrası tepki penceresi ve "belirsiz" sınıfı (10 gün / 20 bar)

- Kaynak: `tweet-gartley-d-tepki-penceresi-10-gun` (SAYAS), `tweet-harmonik-xb-trend-kirilimi-stratejisi` (KAPLM görseli).
- Tansu'nun ifadesi:
  - Birinci el (KAPLM üst notu): `D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ (son 10 günde BELİRSİZLEŞTİ)`.
  - İkinci el (not): "Her Gartley çalışmaz. D'den sonra 10 gün içinde beklenen yönde tepki oluşmazsa yapı belirsiz sayılabilir." Birim ("gün") belirtilmemiş.
- Tanım (en az bilinen, çıkarım):
  1. D tamamlanınca saat başlar.
  2. Pencere içinde beklenen yönde hareket olursa `TEPKI_VERDI`.
  3. 20 bar içinde tepki yoksa `TEPKİ GELMEDİ`. 10 gün içinde `BELİRSİZLEŞTİ`.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Tepki penceresi | 20 bar | görsel (KAPLM) |
| Tepki penceresi | 10 gün | not (ikinci el) |
| Belirsiz penceresi | "son 10 günde" | görsel (KAPLM) |
| Minimum hareket | bilinmiyor | YORUM |
| Birim (takvim / seans / bar) | bilinmiyor | YORUM |

- Belirsiz kalanlar: iki ayrı sayı (20 bar ve 10 gün) aynı anda görselde var. KAPLM'de iki cümle: 20 bar içinde tepki gelmedi, ve son 10 günde belirsizleşti. İkinci cümle "C sonrası fiyat son 10 günde beklenen yönde değil" ile ilgili görünüyor (YORUM). Günlük grafikte bar = gün olabilir ama doğrulanmadı.
- Tansu'nun kanıtı: yok. Örnekler tek.
- Günlük bedava veriyle uygulanabilir mi: evet. Eşik YORUM.
- Kaynak güveni: 20 bar etiketi birinci el. 10 gün ikinci el.

---

## 11. D sonrası TP merdiveni (BALAT Siyah Kuğu): CD retracement

- Kaynak: `gorsel-paket-109` (01-balat-siyah-kugu-harmonik-tp.png).
- Tansu'nun ifadesi (birinci el, grafik): başlık `BALAT.IS - Siyah Kuğu & HEDEFLER`. Etiketler: `TP4 (1.272): 92.98`, `TP3 (C Tepe): 90.50`, `TP2: 87.02`, `TP1: 84.88`, `STOP: 64.00`. Alt paneller: RSI, ADX, MACD. Lejant: `Harmonik`.
  - Metin (not, Levent iletisi, ikinci el): TP1 `0,382`'de kısmi kâr ve stop'u girişe çek; TP2 `0,618` güçlü/hacimli aşılırsa trend hedeflerine geç; stop bullish yapılarda X altı, bazı derin pattern'lerde XA `1,13/1,27`.
- Tanım (ölçüm, not'un D çıkarımı ile doğrulandı):
  - `TP(r) = D + r*(C − D)`. TP1: r=0,382; TP2: r=0,618; TP3: r=1,000 (= C); TP4: r=1,272 (veya 1,618).
  - Görselde D yazılı değil. TP1 ve C'den: `D = (84,88 − 0,382*90,50)/0,618 ≈ 81,40`. `CD = 9,10`. Kontrol: `81,40 + 9,10*0,618 = 87,02` ✓; `81,40 + 9,10*1,272 = 92,98` ✓. Aritmetik tutarlı.
  - Stop 64,00 = X (görsel, ilk pivot). Risk ≈ 17,40; TP1 ödülü ≈ 3,48. R:R ≈ 0,20 (ölçüm). Bu, kural 7'deki R:R ≥ 1,5 kapısıyla çelişir. Tansu aynı yerde ikisini birden önermiş görünüyor (YORUM).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| TP1 | 0,382 CD, kısmi kâr + stop girişe | görsel (fiyat), not (kısmi) |
| TP2 | 0,618 AD | görsel (07.10 yeniden okundu; eski okuma CD) |
| TP3 | C noktası | görsel |
| TP4 | 1,272 (not: veya 1,618) | görsel (1,272) |
| Stop | 64,00 (≈X) | görsel |
| Kısmi kapatma oranı | bilinmiyor | YORUM (kural 7'de %50, burada yok) |

- Belirsiz kalanlar: pattern oranları (Siyah Kuğu tanımı yok), giriş fiyatı ve tetikleyici, D'de otomatik giriş mi tepki teyidi mi, TP1 sonrası break-even stop'un işlem maliyeti.
- Tansu'nun kanıtı: tek hisse, görsel. Sonuç (fill) yok. Son mumlar D'den yukarı (92'ye yakın, TP4 çizgisine yakın). Seçilmiş olabilir.
- Günlük bedava veriyle uygulanabilir mi: evet. TP formülü tam. Giriş ve pattern tanımı eksik.
- Kaynak güveni: etiketler birinci el. Metin ikinci el.

---

## 12. Trident: D = (B × C) / A, B kırılımı

- Kaynak: `gorsel-paket-47` (01-abc-b-kirilimi-trident-d.png).
- Tansu'nun ifadesi:
  - Görsel (birinci el): A (dip), B (tepe), C (daha yüksek dip), kırmızı kutu, `B Kırılımı` (mavi noktalı yatay çizgi), `D (CD=1.27AB)`. D'den sonra yatay/geri çekilme.
  - Metin (not, ikinci el): "Charles Lindsay, 1976, Trident (Zıpkın) Stratejisi, `D = (B × C) / A`". Tarih ve atıf doğrulanmadı. Not, üçüncü taraf "Kuantum İpi" yorumunu (varyans, K-Means, saniyelik hedef, otonom kâr alma) ayrı ve kanıtsız tutuyor.
- Tanım (hesaplanabilir):
  1. A, B, C > 0. `D = B*C/A`. Eşdeğer: `D/C = B/A` (oransal, log-getiri simetrisi).
  2. B kırılımı: C'den sonra kapanış B'yi geçerse (D yönünde) "devam" tetikleyicisi. D'yi hesaplamak için gerekli değil.
  3. Üç strateji (not, ikinci el): (a) teorik D'de ters işlem, (b) C/B'den D'ye devam, (c) D sonrası Fibonacci iz-süren TP.
- Ölçüm kontrolü: Görselde D etiketi `CD=1.27AB`. Trident formülü ise oransal. Aynı A/B/C için iki formül farklı D verir (`D_trident − D_additive(r=1) = (B−A)(C/A − 1)`). Görsel D'nin hangi formülle bulunduğu belli değil (YORUM). Ham A/B/C yok.
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| D formülü | (B × C) / A | not (ikinci el) |
| Görsel D etiketi | CD=1.27AB | görsel |
| B kırılım tampon / bazı | bilinmiyor | YORUM |
| Trailing yöntemi | bilinmiyor | YORUM |

- Belirsiz kalanlar: formül ile `CD=1.27AB` etiketi çelişebilir. Stop yok. Pre-D ve post-D işlemlerin ayrı kuralları yok.
- Tansu'nun kanıtı: tek görsel örnek.
- Günlük bedava veriyle uygulanabilir mi: formül evet. İşlem kuralları hayır.
- Kaynak güveni: etiketler birinci el. Formül ve atıf ikinci el.

---

## 13. Harmonik + talep bölgesi + düşen direnç kırılımı + Fibo (tarayıcı birleşimi)

- Kaynak: `gorsel-paket-32` (01-gartley-abcd-talep-dusen-kirilimi.jpg), `-34` (01-lider-siyah-kugu-talep-run.png), `-35` (01-beyaz-kugu-sell-abcd-dusen-kirilimi.png), `-38` (AKCNS haftalık), `-40` (haftalık), `-42`, `-43`, `-45`, `tweet-haftalik-bullish-gartley-talep-alani-tarama`, `tweet-formasyon-arz-talep-confluence-kapisi`.
- Tansu'nun ifadesi:
  - Birinci el (başlıklar): `LIDER | Düşen Direnci Kıran + Talep + Fibo + ABCD | Harmonik: Siyah Kuğu | Fiyat: 127.40 | Kırılım: 2026-05-18 | Temas: 3 | Lookback: 20`. `BALAT | Düşen Direnç Kıran + Talep + Fibo + ABCD | Fiyat: 75.95 | Kırılım: 2026-05-1x | Temas: 3 | Lookback: 30` (tarih okunurluk sınırlı; not 2026-05-19 yazıyor). `AKCNS | HAFTALIK ABCD FORMASYONU + Talep + EMA | Fiyat: 213.60`. Lejant (32): `Fiyat, EMA5, EMA8, EMA13, Direnç TL, ABCD (BUY), Harmonik (Gartley), Hacim, Kum. Delta`.
  - Metin alıntıları (not, "Levent tarafından ... ifadesiyle iletildi"; Tansu'ya atfı doğrulanamadı, ikinci el):
    - 34: "Kuğuyu talep toplama bölgesinde yakalarsanız böyle RUN olur grafiğiniz."
    - 35: "Düşeni kırmış, SELL yönlü AB=CD'yi tamamlamış, Beyaz Kuğu da oluşmuş; bunu yolculamayalım mı?"
    - 38: "Not alın, süper bir yapı."
    - 40: "ABCD tam talep toplama bölgesinden haftalıkta tepkisini almış, kütür kütür gitmiş; bu yapıların peşindeyiz."
    - 43: "ABCD'ye gözü kapalı güvenilmez; kanalı okumadan iş yapılmaz."
    - 45: "ABCD'ye güvenip doğrudan alırsan böyle olursun; her zaman çalışmaz; ikinci alt grafiğe dikkat."
    - Haftalık tarama isteği (`tweet-haftalik-bullish-gartley...`): C noktası uzun vadeli talep toplama alanında oluşmuş, XABC tamam, D hedefi hesaplanmış bullish Gartley.
- Tanım (kombinasyon, çok katmanlı filtre):
  1. Harmonik veya AB=CD geometrisi (kural 3, 7, 8).
  2. Talep bölgesi (yeşil kutu): D veya C bu bölgenin içinde (BUY, 38/40 görsellerinde D bölge içinde). 39 SELL görselinde D bölgede değil, D sonrası düşüşte bölgeye iniyor.
  3. Düşen direnç çizgisi kırılımı: `Temas: 3` (çizgi en az 3 temas), `Lookback: 20` veya `30`, `Kırılım: tarih`.
  4. Fibonacci merdiveni (D çevresi).
  5. EMA5/8/13 toparlanması, hacim, kümülatif delta (katılım).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Çizgi temas sayısı | 3 | görsel |
| Çizgi lookback | 20 (LIDER), 30 (BALAT) | görsel. Neden farklı? Bilinmiyor. |
| EMA'lar | 5, 8, 13 (lejant / başlık) | görsel (32, 45), 38 pencereleri okunmadı |
| Talep bölgesi üretimi | bilinmiyor (proximal / distal, taze mi) | YORUM |
| Haftalık / günlük | AKCNS ve 40 haftalık; diğerleri belirtilmemiş | görsel |
| Kümülatif delta hesabı | bilinmiyor (gerçek tick yok, BIST'te proxy olabilir) | YORUM |

- Giriş / stop / hedef / bozulma: yok. Başlıkta "AL / SAT" ve "ALIM SİNYALİ" yazıyor ama emir seviyesi yok. Bozulma: not (ikinci el) talep bölgesi altı kapanış ve D risk seviyesi öneriyor, Tansu'dan söz yok.
- Belirsiz kalanlar:
  - Bu birleşik tarayıcının "geçti" eşiği (hangi katmanlar zorunlu?). LIDER başlığındaki dört katman (Düşen Direnç Kıran + Talep + Fibo + ABCD) zorunlu olabilir (YORUM).
  - BALAT'ta aynı başlık (aynı tarayıcı geçişi) ama sonuç başarısız (kural 14). Yani tarayıcı geçişi tek başına işlem izni değil.
  - Aynı tarayıcıda "Siyah Kuğu" etiketi (LIDER) ve BALAT'ta başlıkta pattern yok. `Harmonik: Siyah Kuğu` her başlıkta yok.
  - Beyaz Kuğu ve Siyah Kuğu oranları kaynakta yok. Gartley, Butterfly veya başka kural yerine konamaz.
- Tansu'nun kanıtı: seçilmiş pozitif örnekler (LIDER RUN, AKCNS, 40) ve tek negatif örnek (BALAT). Oran yok. Pozitif seçim yanlılığı.
- Günlük bedava veriyle uygulanabilir mi: parça parça evet (çizgi, EMA, hacim). Talep bölgesi ve delta tanımı eksik. Birleşik kural kodlanamaz.
- Kaynak güveni: başlıklar birinci el. Metin alıntıları ikinci el.

---

## 14. Kanal bağlamı ve negatif delta (başarısız örnek dersi)

- Kaynak: `gorsel-paket-43` (kanal), `gorsel-paket-45` (01-balat-abcd-negatif-kumulatif-delta.jpg).
- Tansu'nun ifadesi (birinci el):
  - RYSAS: başlık `Kanal Durumu: KANAL İÇİ NÖTR | Taze D Noktası (Alış) Tespit Edildi!`. Kırmızı kesikli yükselen üst kanal, yeşil kesikli yükselen alt kanal. D alt kanalda.
  - BALAT: üç panel. Ana grafik EMA5/8/13 + `Direnç TL`. İkinci panel `Hacim`. Üçüncü panel `Kum. Delta`. Fiyat 75,95, D etiketi `D(CD=1.27AB)`, Fibonacci `1.000: 99.45`, `0.786: 94.00`, `0.618: 89.73`, `0.500: 86.72`, `0.382: 83.72`, `0.236: 80.01`, `0.000: 74.00`. Kümülatif delta uzun süre negatif ve kırmızı barlar büyüyor. Fiyat D'den sonra da düşmeye devam ediyor (görselin sonunda hâlâ 75–76).
  - Metin (ikinci el): "ikinci alt grafiğe dikkat".
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
- Günlük bedava veriyle uygulanabilir mi: kanal (regresyon veya pivot çizgileri) evet. Kümülatif delta günlük OHLCV'den gerçek hesaplanamaz; proxy gerekir (YORUM).
- Kaynak güveni: birinci el (görseller). Dersin kuralı ikinci el.

---

## 15. Three Drives (Üç İtiş)

- Kaynak: `kaynak-three-drives-2096510322190201208` (three-drives.webp; tweet The_Tansu_/status/2096510322190201208, 2026-09-06 11:06).
- Tansu'nun ifadesi: görsel etiketleri (birinci el): `X`, `Drive 1`, `A`, `Drive 2`, `C`, `Drive 3`. Metin kuralları (not "Kaynak ölçütleri", ikinci el; kaynak tweet metni tarayıcıda okunmuş olduğu notta belirtiliyor ama metin aynen alıntılanmamış):
  - Alış yönü: giderek düşen üç dip. Satış yönü: giderek yükselen üç tepe.
  - Ara düzeltmeler yaklaşık %61,8 veya %78,6.
  - Sonraki itişler önceki düzeltmenin 1,272 veya 1,618 uzatması.
  - A→Drive 2 ve C→Drive 3 bacakları uzunluk ve süre bakımından yakın (AB=CD mantığı).
  - Süre: 10 bara karşı 11–12 bar dengeli; 8 bara karşı 30 bar dengesiz. Genel tolerans yok.
  - Drive 3 olası dönüş bölgesi; doğrudan ters işlem gerekçesi değil. Güçlü trendde başarısız olabilir.
- Tanım (hesaplanabilir, sınırlı):
  1. Satış yönü: pivotlar `X(dip) → Drive1(tepe) → A(dip) → Drive2(tepe) → C(dip) → Drive3(tepe)`. Tepeler yükselen: `D1 < D2 < D3`.
  2. Düzeltme oranı: `(D1−A)/(D1−X) ≈ 0,618 veya 0,786`; `(D2−C)/(D2−A) ≈ 0,618 veya 0,786`.
  3. İtiş uzantısı: `(D2−A)/(D1−A) ≈ 1,272 veya 1,618` (not "önceki düzeltmenin uzatması" diyor; tam çapa YORUM).
  4. Zaman: bar sayısı yakın (örnek 10 ve 11–12).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Düzeltme oranları | 0,618 ; 0,786 | not (ikinci el) |
| İtiş uzantı oranları | 1,272 ; 1,618 | not (ikinci el) |
| Zaman toleransı | 10 vs 11–12 iyi, 8 vs 30 kötü | not (ikinci el). Sayısal eşik yok. |
| Oran toleransı | bilinmiyor | YORUM |
| Giriş / stop / hedef | yok | not |

- Belirsiz kalanlar: oran toleransı, zaman toleransı, "önceki düzeltmenin uzatması" çapası, ters işlem teyidi, stop. Fiyat ekseni görselde yok, oranlar doğrulanamaz.
- Tansu'nun kanıtı: tek görsel, fiyat yok.
- Günlük bedava veriyle uygulanabilir mi: oran kısmı evet. Zaman ve işlem kuralı yok.
- Kaynak güveni: etiketler birinci el. Oranlar ikinci el.

---

## 16. Elliott: Dalga 2 (CWENE, BRYAT, yüzde 8 örneği)

- Kaynak: `kaynak-cwene-dalga2-demand-2094128312729624792` (elliott.webp, demand.webp; tweet 2094128312729624792, 2026-08-30), `gorsel-paket-107` (BRYAT), `gorsel-paket-110` (yüzde 8).
- Tansu'nun ifadesi:
  - CWENE (not, tweet okunmuş, ikinci el): `33,10→48,30` Dalga 1; yaklaşık 35 dip olası Dalga 2; `32,5–36` talep alanı; `48,30` üzeri kapanış Dalga 3 senaryosunu güçlendirir; `33,10` altı mevcut bullish sayımı iptal. Görsel (birinci el): `0`, `1`, `2?` etiketleri. Kırılım etiketleri (demand görseli): `Kırılım 2026-07-21 (Temas:6)`, `Kırılım 2026-07-24`, `Kırılım 2026-08-05 (Temas:3)`.
  - BRYAT (görsel, birinci el): başlık `BRYAT - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 2 (Fibo: %64.3)`. Lejant: `BB Üst (14)`, `BB Alt (14)`, `EMA(9)`, `RSI(14)`, `EN YAKIN FVG`.
  - BRYAT stratejisi (not, Levent iletisi, ikinci el): günlük, yüksek hacimli BIST30/100 hisseleri; Point0→Point1 en az %10 itki; ABC Wave2 düzeltmesi; alım bölgesi `0,50–0,786`; ideal Golden Pocket `0,618–0,65`; bölgede taze (fresh) bullish FVG; giriş FVG üst bandı veya Fib 0,618 limit; stop Point0 altı; TP1 = Point1; TP2 = `C + 1,618 × Wave1`; bilanço öncesi riskten kaçın; FVG'ye gelmeden dönen fiyatı kovalama; düşüş yapısında uygulama.
  - 110 (not, ikinci el): düzeltmenin Fib `0,50` veya `0,618` alanına inmesi ve bullish FVG ile çakışması; hafta başı listesinde verilen hissede `%8` kullanıcı beyanı.
- Tanım (BRYAT, not'tan hesaplanabilir):
  1. `P0` = itki başı (dip), `P1` = itki tepesi. `W1 = P1 − P0`. Koşul: `P1/P0 − 1 >= 0,10`.
  2. Düzeltme: `Fib(r) = P1 − r*W1`. Alım bölgesi `Fib(0,786) <= fiyat <= Fib(0,50)`. Golden Pocket `Fib(0,65)..Fib(0,618)`.
  3. Bölgede taze bullish FVG: `high(mum1) < low(mum3)`. (FVG tanımı not'tan, Claude. Tansu'nun FVG formülü verilmemiş.)
  4. Giriş: FVG üst bandı veya Fib 0,618'de limit.
  5. Stop: `P0 − tampon`. Wave 2, P0'ı aşağı geçmemeli (Elliott kuralı).
  6. TP1 = `P1`. TP2 = `C + 1,618*W1` (C = düzeltme sonu).
- Ölçüm (benim hesabım): CWENE'de Dalga 2 dibi ≈35 ve Dalga 1 = 33,10→48,30. `(48,30−35)/(15,20) = 0,875` geri alım. BRYAT stratejisinin alım bölgesi (0,50–0,786) dışında. Yani CWENE dalga 2 dibi bu stratejinin sayılarıyla uyuşmuyor. Aynı kişinin iki ayrı sayımı (YORUM; BRYAT stratejisi ayrı bir varyant olabilir).
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Min itki | %10 | not (ikinci el) |
| Alım bölgesi | 0,50–0,786 | not |
| Golden Pocket | 0,618–0,65 | not |
| Başlıktaki Fibo | %64,3 (BRYAT), %54,0 (ENJSA Wave 4) | görsel |
| TP2 | C + 1,618*W1 | not |
| Evren | BIST30/100, günlük | not |
| BB periyodu, EMA, RSI | 14, 9, 14 | görsel (lejant) |
| FVG "taze" tanımı | bilinmiyor (hiç dokunulmamış mı?) | YORUM. Başlıkta `TEMAS (0.00%)` var, anlamı belirsiz. |
| Pivot / BOS parametreleri | bilinmiyor | YORUM |

- Belirsiz kalanlar: `FVG TEMAS (0.00%)` etiketinin anlamı (temas var ama doluluk %0 mı?), "dolgun mum" tanımı, pivot kuralı, Wave 2 "ABC" zorunlu mu, giriş dolumu (limit ne zaman dolar?).
- Tansu'nun kanıtı: yüzde 8 örneği kullanıcı beyanı (110), önceden listede olduğu doğrulanmadı. BRYAT bekleyen kurulum, sonuç yok. CWENE tweet'inde sonuç yok.
- Günlük bedava veriyle uygulanabilir mi: evet (fiyat, FVG, retracement). Pivot ve %10 eşiği net.
- Kaynak güveni: başlıklar birinci el. Strateji ikinci el.

---

## 17. Elliott: Dalga 4 retracement ve Dalga 5 hedefi

- Kaynak: `tweet-elliott-wave4-wave3-retracement-024-038-050` (ikinci el), `gorsel-paket-102` (01-enjsa-elliott-wave5-hikkake-fvg-outcome.png).
- Tansu'nun ifadesi:
  - Not (Levent iletisi, ikinci el): "3. dalgada yükselen miktarın %24, %38, %50'si 4. dalgada geri alınabilir." Örnek: Wave3 = 100 birim ise Wave4 düşüşü 24/38/50.
  - 102 görsel başlığı (birinci el): `ENJSA - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 4 (Fibo: %54.0)`. Yeşil kesikli `Wave 5 Hedef` çizgisi (~94), yeşil FVG kutuları, sarı kutu (Hikkake).
  - Metin (not, ikinci el): Wave 5 hedefi yaklaşık `94–95`, `85–90` karar bandı, sarı Hikkake alanı altında iptal.
- Tanım (bullish, hesaplanabilir):
  - `W3 = P3 − P2`. `P4_hedef(r) = P3 − r*W3`. r ∈ {0,24 ; 0,38 ; 0,50} (kaynak yuvarlak) veya {0,236 ; 0,382 ; 0,500} (Fibonacci). Bearish ayna: aynı formül, `W3` işaretli.
  - Örnek: P2=200, P3=300 → 276 / 262 / 250 (kaynak oranları).
  - Standart itkide Wave 4, Wave 1 alanına girmemeli (Elliott kuralı, not).
  - ENJSA başlığındaki `%54,0` büyük olasılıkla Wave 4 geri alım oranı. 0,50'ye yakın, 0,38'in üstünde. (YORUM)
- Parametreler:

| parametre | değer | kaynak |
| --- | --- | --- |
| Wave 4 geri alım oranları | 0,24 / 0,38 / 0,50 | not (ikinci el) |
| ENJSA Wave 4 geri alım | %54,0 | görsel |
| ENJSA Wave 5 hedefi | ≈94 (çizgi), 94–95 (metin) | görsel, not |
| Wave 5 hedefinin formülü | bilinmiyor | YORUM |

- Belirsiz kalanlar: Wave 5 hedef formülü (hangi çapa?). ENJSA %54 ile kuralın 0,50 üst sınırı arasında 4 puan fark. Kural "rehber", zorunlu değil (not).
- Tansu'nun kanıtı: ENJSA hedefe ulaştı (görsel, hedef çizgisini test etmiş veya aşmış). Seçilmiş olumlu vaka. Hedefin önceden donduruldu mu belirsiz.
- Günlük bedava veriyle uygulanabilir mi: Wave 4 hedef merdiveni evet. Dalga sayımı otomasyonu zor. Pivot ve sayım kuralı yok.
- Kaynak güveni: ikinci el (oranlar), birinci el (ENJSA başlığı).

---

## 18. Elliott 5+3 ve Fibonacci gün sayımı

- Kaynak: `gorsel-paket-111` (01-elliott-5plus3-fibonacci-islem-gunleri.jpg).
- Tansu'nun ifadesi (birinci el, infografik; alt köşede `NotebookLM` damgası, yani üretici bir yapay zekâ aracı; Tansu'nun kendi çıktısı olmayabilir):
  - `Borsanın Ritmi: Elliott Dalga ve Fibonacci Sırları`. `5+3 DALGA PRENSİBİ`: "Piyasalar, 5 dalgalık bir ana trend (itki) ve ardından gelen 3 dalgalık bir düzeltme ile hareket eder."
  - `Matematiksel Uyum: Fibonacci Dizisi`: "Döngüdeki toplam dalga sayıları (3, 5, 8, 13, 21, 34...) daima Fibonacci dizisini takip eder."
  - `ZAMAN ANALİZİ: GÜN SAYMA KURALI`: "Bir trendin tepe veya dip noktalarında genellikle Fibonacci günlerinde (5., 8., 13., 21. gün vb.) test edilir."
  - `EN KRİTİK KURAL: TAKVİM GÜNLERİNİ SAYIN!` "Analiz yaparken sadece işlem günlerini değil, hafta sonları ve tatiller dahil tüm günleri hesaba katın."
- Çelişki: `gorsel-paket-111` notu bunu "yalnız işlem günlerini sayın" diye özetlemiş. Görsel metni takvim günü diyor. Görsel kazanır.
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
- Kaynak güveni: birinci el (metin). Tansu'ya atfı belirsiz (NotebookLM damgası).

---

## 19. Çoklu aralık Fibonacci konfluansı

- Kaynak: `gorsel-paket-120` (dört görsel, CAT örneği).
- Tansu'nun ifadesi (birinci el, görsel başlıkları ve metinleri):
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
- Kaynak güveni: birinci el (metinler). Üretim damgası görselde yok; Tansu'ya atfı belirsiz (YORUM).

---

## 20. Mimari kararlar (kural değil): ayrı tarayıcılar ve squeeze projesi

- Kaynak: `tweet-gartley-butterfly-ayri-tarayicilar`, `tweet-harmonik-momentum-squeeze-projesi`, `tweet-uygulama-algoritmalari-v1`, `gorsel-paket-02`.
- Tansu'nun ifadesi (not, ikinci el): Gartley ve Butterfly kodlarını tek tarama sisteminde birleştirdim, uygulama ve bakım maliyeti çok yüksek, ayrı tarayın. Harmonik formasyonda squeeze'in hangi noktada oluştuğu ayrı araştırma konusu (ABCD, Kelebek, Gartley). İlk kapsam listesi: ABCD, Kelebek, Gartley; haftalık kanal dibine temas; düşeni kıran; takoz, TOBO, OBO, bayrak, flama.
- Tanım: yok (mimari ve proje önerisi).
- Parametreler: yok.
- Belirsiz kalanlar: hepsi.
- Tansu'nun kanıtı: yok.
- Günlük bedava veriyle uygulanabilir mi: mimari karar olarak evet (Gartley ve Butterfly ayrı modül; ortak sonuç arayüzü).
- Kaynak güveni: ikinci el.

---

## 21. Sıralı kısa liste: koda ne kadar hazır?

Sıralama: 1 = en hazır. "Hazır" = oran, giriş, çıkış ve etiket Tansu'nun birinci el görselinde var.

1. AB=CD (r = 1,0 ve 1,27), D formülü, hedef merdiveni (kural 3 ve 4).
   - Hazır: `D = C + r*(B−A)`, `q <= 1`, D, B'nin ötesinde, hedef `D + {0,618; 1,0; 1,618}*(A−D)`. Ölçümle doğrulandı (KRPLS, MARKA, RYSAS).
   - Boşluk: pivot parametreleri, oran toleransı, BOZULDU bazı, stop, q alt sınırı.
2. Gartley tablosu (kural 7).
   - Hazır: AB/XA 0,618; BC/AB 0,382–0,886; D 0,786 XA; stop X; TP1 AD 0,382 (%50); TP2 AD 0,618; R:R kapısı (ikinci el).
   - Boşluk: tolerans (%3–5, oran mı fiyat mı; MAKIM etiketleri daha geniş toleransa işaret ediyor), pivot, D formülü yön hatası, n_period, ATR periyodu, stop üç alternatif.
3. Elliott Wave 4 hedef merdiveni ve BRYAT Wave 2 stratejisi (kural 16 ve 17).
   - Hazır: formüller net (Wave 4: `P3 − r*W3`; BRYAT: %10 itki, 0,50–0,786 bölge, stop P0 altı, TP1 P1, TP2 C + 1,618*W1).
   - Boşluk: ikinci el. Dalga sayımı, pivot kuralı, FVG "taze" tanımı, `TEMAS (0.00%)` anlamı. CWENE sayısı BRYAT bölgesiyle çelişiyor.
4. X–B trend kırılımı ve tepki penceresi (kural 9 ve 10).
   - Hazır: çizgi çapaları (X, B), yön, 20 bar tepki etiketi.
   - Boşluk: kırılım bazı ve tampon, stop, tepki eşiği, 10 gün / 20 bar birimi.
5. BALAT TP merdiveni (kural 11).
   - Hazır: `TP(r) = D + r*(C−D)`, r = 0,382 / 0,618 / 1 / 1,272.
   - Boşluk: giriş, pattern oranları, R:R düşük (≈0,2).
6. Kelebek (kural 8).
   - Hazır: D = 1,272 XA, B = 0,786 (DOAS).
   - Boşluk: DGATE B ≈ 0,55 çelişkisi, BC ve CD aralıkları, stop.
7. Trident (kural 12).
   - Hazır: `D = B*C/A`.
   - Boşluk: formül ile `CD=1.27AB` etiketi çelişebilir, işlem kuralı yok.
8. Three Drives (kural 15).
   - Hazır: 0,618/0,786 düzeltme, 1,272/1,618 itiş (ikinci el).
   - Boşluk: toleranslar, çapa, giriş ve stop.
9. Birleşik tarayıcı (talep + düşen direnç + Fibo + ABCD) (kural 13) ve kanal (kural 14).
   - Hazır: çizgi temas = 3, lookback 20/30, EMA 5/8/13.
   - Boşluk: talep bölgesi kuralı, delta verisi, eşikler, zorunlu katmanlar. Kodlanamaz.
10. Çoklu aralık Fibonacci (kural 19), Fibonacci gün sayımı (kural 18), Siyah/Beyaz Kuğu (kural 13), CD şiddeti (kural 6).
    - Hazır değil: konsept, oran veya kural yok. Siyah ve Beyaz Kuğu oranları hiçbir yerde yok.

Genel kanıt durumu: Tansu hiçbir harmonik kural için sistematik bir başarı tablosu göstermiyor. Tek sistematik tablo SMRTG (12 pattern) ve ISKPL (5 pattern), ikisi de tek hisse, maliyetsiz, stop kuralı bilinmiyor. Diğer örnekler seçilmiş pozitif vakalar (LIDER, AKCNS, 40, DOAS, KAPLM negatif dışında).

Ortak boşluklar (hepsi YORUM; kod öncesi karar):

1. Pivot kuralı: L, R, zikzak eşiği, `Swing=15 sol-only`'in harmonik tarayıcıya ait olup olmadığı.
2. Oran toleransı: Tansu %3–5 öneriyor (ikinci el), MAKIM ve DGATE görselleri daha geniş toleransa işaret ediyor.
3. `BOZULDU`, `TEPKI_VERDI` ve `BELİRSİZLEŞTİ` eşikleri.
4. Stop kuralı (X, XA 1,13, `X−2*ATR`).
5. Siyah ve Beyaz Kuğu oran tanımı.

Küçük sonraki adım: kural 3 ve 4 için kendi pivot kararınızı yazın (L, R), sonra KRPLS D=11,29 ve D=10,05 değerlerini fiyat verisinden yeniden üretin.
