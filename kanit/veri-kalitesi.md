# Veri kalitesi işi (30.10.2026)

İstek (Levent, 30.10.2026): "Hepsine evet". Beyinin iki sorusuna evet: "2018 kaynak hatası düzeltmesinin yan etkisi
giderilsin mi?" ve "Ayrı bir veri kalitesi işi açılsın mı?" (olay uyuşmazlığı, düzeltilmiş yüksek/düşük farkı T1,
likidite kuralı, `main`deki eski yuvarlama hatası). Gartley denetimi (`kanit/gartley-denetim.md`) bu açıkları bıraktı.
Bu onay, aşağıdaki `veri.py` değişikliklerinin SPEC 3.9 istisnasıdır.

## Sonuç

| Madde | Sonuç | Kayıt |
|---|---|---|
| 1a. V2 yan etkisi: %10 kuralı gerçek günleri boşaltıyor | Düzeltildi | PR 263, birleşti (47473bb) |
| 1b. Aynı yan etki ertesi gün: bozuk satır limit bazı değil, sahte aşım | Düzeltildi | PR 266, birleşti (7cbb85f) |
| 2. Olay denetimi farkı 2015-2022'de %3,02 | Nedeni bulundu: kaynak, kapanmış hisselerin olay kaydını vermiyor (kod hatası değil) | Bu kayıt; Levent'e soru |
| 3. T1: düzeltilmiş yüksek/düşük ham × çarpandan geniş | Nedeni bulundu: kaynağın 30.11.2015 öncesi düzeltilmiş alanları (kod hatası değil) | Bu kayıt; Levent'e soru |
| 4. Likidite kuralı yok | SPEC'te kural yok; TASARIM'daki kurallar eski tasarıma ait. Seçenekler ölçüldü | Levent'e soru |
| 5. 0,10 TL'de yanlış kilit (7 gün) | Düzeltildi | PR 265, birleşti (112bb4a) |
| 6. `main`de eski yuvarlama hatası | PR açık; birleştirme Levent'in | #267, PR 268 |

### Düzeltme ve değişim tablosu

Referans paneli: ayar grubu (371 hisse), 2015-2022, dondurulmuş 29.10 ayarı, `TANSU_DUZELTME=D1t,T3,E2,S1s,S2s`,
`TANSU_TG=1`, ham anlık `20260101-0000`, denetimin düzeneği (`kanit/gartley-denetim/kur.py`, `panel.py`). Her satır
`yeniden-kurulus` ucunda koştu (satır 3: PR ucu b6e47ab; birleşme 112bb4a'nın `tansu/` ağacı b6e47ab ile aynı). Hücre: dolum / ortalama R / p (tek yönlü) / son kasa TL (başlangıç 100.000).
Ayrık grup ve 2010-2014 koşulmadı.

| # | Düzeltme | Motor | Veri SHA-256 | gartley | gt-k | abcd-k | S2-Z | S3 | tg |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Taban (denetim satırı 13b) | 86cd0c2 | 452e31ff… | 51 / 0,916 / 0,0685 / 476.317 | 10 / −0,082 / 0,711 / 231.138 | 111 / 0,009 / 0,501 / 179.071 | 163 / 0,769 / 0,021 / 349.160 | 343 / 0,350 / 0,0265 / 562.519 | 6 / −0,797 / 0,943 / 202.116 |
| 1 | 1a kaynak günü (PR 263) | 47473bb | 304b9863… | aynı | aynı | 114 / −0,015 / 0,585 / 179.375 | aynı | 343 / 0,348 / 0,0269 / 560.145 | aynı |
| 2 | 1b limit bazı (PR 266) | 7cbb85f | f0dd12d1… | aynı | aynı | aynı (satır 1) | aynı | aynı (satır 1) | aynı |
| 3 | Madde 5, kuruşluk kilit (PR 265) | 112bb4a | cf00b14a… | aynı | aynı | aynı (satır 1) | aynı | aynı (satır 1) | aynı |

"aynı": bir üst satırla aynı sayılar. Madde 1a'nın 2015-2022 içinde geri getirdiği tek gün 30.04.2018'dir (anlık
`20261005-1949`); satır 1'deki değişimin günlere ayrımı yapılmadı. Madde 5 tek başına taban motorun üstünde (e265601)
de satır 0 ile aynı sayıları verdi (veri SHA-256 1418def5…).

## Madde 1: kaynak günü yan etkisi

Neden (anlık `20261005-1949`): %10 kuralının boşalttığı 7 günde (22.04.2024, 10.10.2025, 02.03.2026, 03.03.2026,
23.03.2026, 22.04.2026, 16.09.2026) bozuk satırların hepsi aynı kaynak hatasıdır: ham AOF [düşük, yüksek] dışında (bir
kısmında 0), ham yüksek, düşük ve kapanış tutarlı. İşaretli pay %10,1-%20,2. Kalan hisseler gerçek piyasadır (02.03.2026
ortanca −%4,3, 15 taban kapanışı; 16.09.2026 ortanca −%5,0, 75 taban kapanışı). Bozuk satırların kapanışı da gerçektir:
1a sonrası 2026'da bozuk satırdan sonraki gün açılan 99 aşım karantinasının hepsinde getiri, bozuk satırın kendi
kapanışına göre ±%10,5 içindedir (ortanca −%7,5).

- 1a (PR 263): satırlarının en az %10'u ama yarısından azı işaretli günde yalnız işaretli satırlar eksik olur (karantina
  yok); öteki satırlar fiyatını korur. Yarısı işaretli gün eskisi gibi bütünüyle eksik (26.01.2016, 21.05.2026).
  3.909 satır geri gelir (30.04.2018 ve 7 gün). Karantina değişmez.
- 1b (PR 266): limit bazı, ham kapanışı ham düşük-yüksek aralığında olan son işlem günüdür (AOF'si ya da düzeltilmiş
  alanı bozuk olsa da). Ham kapanışı tutarsız satır eskisi gibi baz olmaz. 17.09.2026'daki 55 sahte aşım kalkar.

İleri izleme etkisi (anlık `20261005-1949`):

| Ölçü | Taban (86cd0c2) | 1a | 1a + 1b |
|---|---|---|---|
| Bütün hisselerin boş olduğu gün (2024-2026) | 7 + 21.05.2026 | 21.05.2026 | 21.05.2026 |
| 2026 karantina başlangıcı | 149 | 149 | 50 |
| 01.10.2026'da karantinadaki hisse | 130 | 130 | 47 |
| 2026 karantinalı hisse-gün payı | %11,09 | %11,09 | %6,28 |
| 2015-2022 karantina payı, bütün / ayar | %1,211 / %1,258 | aynı | aynı |

Kalan 50 başlangıcın hepsi bozuk satırdır ve hepsi aynı AOF hatasıdır, %10'un altındaki günlerde (05.01.2026: 20;
04.08.2026: 12; 30.04.2026: 6 …). Bu hata 2015-2022'de hiç yok; 2024-2026'da 80 satır, 76 hisse (soru 4).

## Madde 2: olay denetimi farkı

Ölçü `Anlik.oranlar` ikinci değeri (olay uyarısı olan hisse-gün payı), diskteki anlık `20261005-1949` (716 hisse),
taban motor 86cd0c2. 2015-2022: 25.299 / 837.477 = %3,021 (eşik TASARIM 5.13 %2).

Olası nedenler, hepsi sınandı:

| # | Neden | Sınama | Sonuç |
|---|---|---|---|
| H1 | Kaynağın olay listesi bazı hisselerde eksik | Uyarılı satırların hissesi; olay kaydı hiç olmayan hisseler | DOĞRULANDI. Uyarıların 23.099'u (%2,758 puan; %91) olay kaydı hiç olmayan 39 hissede. 39'unun 39'u borsadan çıkmış (son satırı anlık sonundan 30 günden eski): ADANA, ADBGR, ADNAC, BOLUC, UNYEC (2019-2020 birleşmeleri), SODA, TRKCM, ANACM, OLMK, DENCM, BOYP, HALKS … |
| H2 | Okuyucu geçerli olayları atıyor (`SHHE_TARIH ≤ 0` ya da `SHHE_FIYAT_AYAR_OR ≤ 0` yer tutucu kaydı) | Atılan 154 kaydın açıklanmayan düzeltme adımlarına yakınlığı (±3 satır) | REDDEDİLDİ. Hiçbir adım yalnız atılan kayıtla açıklanmıyor |
| H3 | İstek parametresi (`endeksKodu "09"`) kayıt süzüyor | Canlı istek (İş Yatırım `GetSermayeArttirimlari`, ücretsiz): SISE, SODA, ADANA; `endeksKodu` "09" ve "" | REDDEDİLDİ. SISE: "09" 43 kayıt; "" 559 kayıt ama aynı 43 olay, her endeks için tekrar (13 endeks). SODA ve ADANA: iki parametreyle de 0 kayıt |
| H4 | Düzeltilmiş kapanışın 4 ondalık yuvarlaması (denetimde yarım birim payı yok) | \|fark\| ≤ %0,5 + 5e-5 / kapanış | KÜÇÜK. 185 satır (%0,022 puan), 3 hisse |
| H5 | Kaydı olan hissede olay çarpanı adımla tutmuyor | Kalan uyarılar | KÜÇÜK. INGRM 2.010 satır (%0,24 puan): 08.05.2023 nakit temettü kaydı (çarpan 0,98038), düzeltilmiş seride 2023 öncesi bütün satırlarda aynı adım; artı 5 tekil satır |

Neden: İş Yatırım olay uç noktası borsadan çıkmış kodlar için kayıt döndürmüyor; düzeltilmiş fiyat serisinde ise bu
hisselerin düzeltmeleri var. Bu bir kod hatası değildir. Olay kaydı olan hisselerde fark %0,26'dır (H4 + H5).
2023-2026'da fark %0,145 (YGYO 682 satır, kayıtsız ve kapanmış; INGRM 83).

Etkisi: olay kaydı olmayan hissede büyük düzeltme adımı (ör. %10'dan büyük temettü ya da sermaye işlemi) limit
denetiminde sahte aşım olur ve 250 gün karantina açar. Bütün yıllarda 145 aşım karantinasının 44'ü açıklanmayan bir
adımın gününde; 43'ü kayıtsız hissede. 2015-2022'de 14 (hepsi kayıtsız hisse): ADANA ve ADBGR 07.08.2019, ANACM
24.07.2017, BOYP 12.07.2017 ve 05.12.2018, DENCM 16.09.2019, DENIZ 21.09.2015 ve 27.05.2016, HALKS 08.07.2016 ve
29.08.2017, OLMK 01.03.2018 ve 05.02.2020, ROYAL 04.08.2016, SODA 03.07.2015. (Gartley denetimi BOYP ve OLMK'yı "gerçek
anomali" saymıştı; düzeltilmiş seride bu günlerde adım var, yani olaydır.)

Değişiklik yapılmadı: çözüm bir veri kuralı seçimidir (aşağıda soru 2).
Betikler: `olay_neden.py`, `olay_ayrisim.py`, `olay_istek.py`, `olay_karantina.py` (geçici klasör `%TEMP%\tansu-veri-kalitesi`).

## Madde 3: T1

Ölçü: düzeltilmiş yüksek/düşük ile ham yüksek/düşük × gün çarpanı (düzeltilmiş kapanış / ham kapanış) arasındaki fark,
ham fiyat adımı biriminde. Anlık `20261005-1949`, işlem günleri, bütün hisseler.

- Fark yalnız 30.11.2015 öncesinde var: 2010-2015'te her yıl satırların %31-41'inde 3 adımdan büyük; 30.11.2015
  öncesi satırların %67,8'inde yarım adımdan büyük. 2016-2026'da 3 adımı aşan pay her yıl %0,005'in altında; yarım
  adımı aşan pay %0,15. Geçiş tam iki seanstan tek seansa geçiş günüdür
  (27.11.2015: %60,2; 30.11.2015: %0,2).
- Fark hep tam adım katıdır ve hep genişletir (düzeltilmiş düşük daha düşük: 14.468 satır, tersi 0; yüksek daha yüksek:
  22.520 satır, tersi 0; 2015-2022). Örnek SELEC 09.07.2015: ham düşük 2,35; düzeltilmiş düşük 1,885244 = 2,31 × 0,816123.
- Düzeltilmiş AOF da aynı dönemde ham AOF × çarpandan farklı (satırların %65,9'unda %0,1'den çok; 5.-95. yüzdelik
  −%0,67 / +%1,20). 2016 sonrası %0,26.

Hangisi gerçek gün aralığı? Bağımsız kaynakla sınandı: Yahoo günlük verisi (Gartley Yahoo karşılaştırmasının yerel
önbelleği, ayar grubu hisseleri), Yahoo kapanışının ham kapanışa %2 içinde eşit olduğu günler. 30.11.2015 öncesinde düzeltilmiş düşüğün ham düşükten
aşağıda olduğu 9.937 satırda Yahoo düşüğü ham düşüğe %97,7 eşit, düzeltilmiş seriden çıkan fiyata %0,1 eşit. Yüksek
için 14.018 satırda %97,5 ve %0,2. Yani ham yüksek/düşük gerçek gün aralığıdır; kaynağın düzeltilmiş yüksek, düşük ve
AOF alanları iki seans döneminde 1-4 adım geniştir.

Neden: kaynağın düzeltilmiş (HGDG) alanları, 30.11.2015 öncesi. Kod alanları kaynaktan doğru eşler (`kaynak.ALANLAR`:
HG_MAX → ham_yuksek, HGDG_MAX → yuksek); eksik olan, düzeltilmiş aralığı ham aralıkla karşılaştıran bir denetimdir. Kod
hatası değildir; iş emri gereği düzeltilmedi.

Bilgi için ölçüldü (karar bu sayıya göre verilmemeli): 30.11.2015 öncesinde düzeltilmiş yüksek/düşük/AOF'yi ham ×
kapanış çarpanından kuran geçici motorla (`m-t1`, d138974 üstüne) referans paneli belirgin değişir: `gartley` 51 / 0,916
/ 0,0685; 476.317 → 52 / 0,170 / 0,418; 329.172; `S3` 343 / 0,348 / 0,0269; 560.145 → 358 / 0,199 / 0,211; 665.058.
Panelin anlığında (`20260101-0000`) 2015-2022 karantina payı değişmez (bütün hisseler %1,232, ayar grubu %1,293). Ayar grubunda etkilenen satırlar 2015'in ilk 11 ayıdır (2015-2022 ayar
satırlarının %7,43'ü). Gartley denetimi T1 etkisini "< 0,02 R" diye tahmin etmişti; o tahmin aynı sinyallerin yeniden
oynatılmasıydı, pivot ve formasyonların değişmesini içermiyordu.

Betikler: `t1.py`, `t1_yahoo.py`, `t1_aof.py`; panel `kos.ps1 T1-secenek`.

## Madde 4: likidite

Mevcut kural aranıp bulunamadı:
- SPEC (yerel, `yeniden-kurulus`): likidite kuralı yok. Evren "her tarihte BIST 30 üyeleri" (SPEC 2, Levent kararı);
  ürün adet ve tutar vermez.
- TASARIM (`main`): 5.2 "60 günlük medyan TL hacimde en alttaki %20 önce elenir" eski evren kuralının (piyasa değerine
  göre ilk 100) parçasıdır; C02 Levent kararıyla BIST 30 evrenine geçildi. 5.4 "pozisyon, 10 günün medyan TL işlem
  tutarının %2'sini geçemez" `legacy_portfoy_v1` kapasite politikasıdır. İkisi de yeniden kuruluşun bütün BIST deneme
  evrenine bağlanmamış.
- Gartley denemelerinin para katmanı (`kanit/gartley-para/ayar.json`) pozisyonu 20 günlük medyan TL hacmin %10'uyla
  sınırlar; bu bir boyut sınırıdır, işlem görebilirlik kuralı değildir.

Kural seçilmedi (ürün kararı). Seçeneklerin veri tarafındaki etkisi ölçüldü; kâr/zarar etkisi bilerek hesaplanmadı.
Ayar grubu (368 fiyatlı hisse), 2015-2022, 553.456 fiyatlı hisse-gün; panel motoru d138974 (PR 266):

| Seçenek | Kural | Elenen hisse-gün | Hiç elenen hisse | Panel dolumlarından sinyal günü elenen |
|---|---|---|---|---|
| L0 | Kural yok (bugünkü durum; para katmanının %10 boyut sınırı kalır) | %0 | 0 | 0 |
| L1 | 20 günlük medyan TL hacim < 1 milyon TL (işlemsiz gün 0) | %39,56 (2015 %74,6 → 2022 %9,0: sabit TL eşiği enflasyonla kayar) | 264 | gartley 24/50, gt-k 4/10, abcd-k 59/114, S2-Z 60/163, S3 120/335, tg 2/6 |
| L2 | O günün 60 günlük medyan TL hacminde en alttaki %20 (eski TASARIM 5.2 eşiği, göreli) | %19,67 (her yıl %18-21) | 171 | gartley 11, gt-k 2, abcd-k 23, S2-Z 26, S3 53, tg 0 |
| L3 | Son 60 işlem gününde 10 ya da daha çok işlemsiz gün | %0,87 (2015 %2,5 → 2022 %0,1) | 29 | gartley 0, gt-k 0, abcd-k 2, S2-Z 0, S3 1, tg 0 |

L3 işlemsiz günleri doğrudan sayar; V1'den önce işlemsiz gün her seferinde 250 gün karantina açıyordu (bağımsız veri
denetimi: ayar grubunda %7,63 puan). Betik: `likidite.py`.

## Madde 5: kuruşluk kilit

0,10 TL'de ±%10 bant bir fiyat adımıdır (0,09-0,11). Kilit denetiminin "sınıra bir adım yakın" payı baza kadar uzanıyor
ve hareketsiz günü hem tavan hem taban kilidi sayıyordu. Düzeltme: kilitte kapanış, sınırın baktığı bazdan en az yarım
adım uzaklaşmış olmalıdır (tavan için `alt_baz`, taban için `ust_baz`; 1e-9 pay). Bu koşul yalnız baz 15 adım ya da
daha azken (0,01 adımda 0,15 TL) bir sonucu değiştirebilir. Eşitlik kilit sayılır, çünkü olay gününde baz yarım adımda
olabilir (0,21 × 0,5 = 0,105: 0,11 tavan, 0,10 taban kilididir). İlk sürüm eşitliği saymıyordu; bağımsız inceleme
bunu buldu (yarım adım bazlı taramada 173 gerçek kilit kaybı, anlıkta etkisi yok).

Anlık `20261005-1949`, taban motora göre: `kilit_tavan` 7, `kilit_taban` 6 satırda kalkar (H = L olanlar 6 ve 5):
MANGO 30.12.2013 (taban kilidi kalır: önceki AOF 0,11) ve MEMSA 13.04.2015, 12.06.2015, 01-06.07.2015. Başka hiçbir
kilit, karantina ya da eksik gün değişmez. Referans paneli değişmez.

Kapsam dışı (ölçülemez): iki seans döneminde önceki AOF bazının ±%10'unda, kapanışı önceki kapanışa eşit H = L günler
(ör. DMISH 0,20 TL) V3'ün iki baz kuralıyla kilit sayılmaya devam eder; seans verisi olmadan doğruluğu sınanamaz.
İnceleme sayımı: 112 gün (MEMSA 21, MANGO 14, DMISH 14, FVORI 10 ve başkaları).

## Madde 6: `main` yuvarlama payı

TASARIM 5.13 (#251) düzeltilmiş seride bağıl 1e-4 paya ek olarak 4 ondalık yuvarlamanın mutlak yarım birimini (5e-5)
tanır; `main` kodu yalnız bağıl payı uyguluyordu. Issue #267, PR 268 (`267-main-yuvarlama-payi`): veri kapısı
(`veri._gunler`) ve motorun dolum öncesi denetimi (`motor._fiyat_engeli`) aynı payı uygular; TASARIM uygulama notu ve
CHANGELOG güncellendi. Birleştirme Levent'in GitHub onayına bağlıdır; bu iş birleştirmedi.

Anlık `20261005-1949`, `origin/main` (da7aed5) → PR 268:

| Ölçü | Önce | Sonra |
|---|---|---|
| Karantina günü (bütün yıllar, 1.837.862 satır) | 53.172 | 18.750 |
| 250 günlük karantina payı, 2015-2022 | %33,09 | %10,60 |
| Kapıdan geçen işlem satırında motor hatası | — | 0 / 1.816.210 |

Bilgi: TASARIM 5.13'teki "637 satırda en çok 4,5e-5 fark" bu anlıkta 33.996 kurtarılan satırdır (en çok 5,0e-5); o
metnin dayanağı bilinmiyor.

## Levent'e sorular

Hepsi veri kuralı seçimidir (SPEC 3.9 kalite kurallarını kilitler); öneri ilk seçenektir.

1. **T1, 30.11.2015 öncesi düzeltilmiş yüksek/düşük/AOF.** (a) Ham × kapanış çarpanından kurulsun: Yahoo ham aralıkla
   %97,7 aynı; 2015'in ilk 11 ayı ve 2010-2014 değişir. (b) Olduğu gibi kalsın, kayıtta bilinen sınır olarak dursun.
   (c) 2015-11-30 öncesi denemelerden çıkarılsın.
2. **Olay kaydı olmayan kapanmış hisseler (39 hisse).** (a) Olay kaydı hiç olmayan hissede, düzeltilmiş serideki adım
   (düzeltilmiş/ham oranının sıçraması) limit bazında olay sayılsın: 2015-2022'de 14 sahte karantina kalkar; veri kapısı
   (%2) yalnız kaydı olan hisselerde ölçülsün (%0,26). (b) Bu hisseler deneme evreninden çıkarılsın (kapanan hisse
   yanlılığı artar). (c) Olduğu gibi kalsın.
3. **Likidite (bütün BIST deneme evreni ve ileri izleme).** (a) L3: son 60 günde 10+ işlemsiz gün varsa yeni sinyal yok.
   (b) L2: o günün en alttaki %20'si. (c) L1: sabit TL eşiği (enflasyonla kayar). (d) Kural yok; para katmanının %10
   boyut sınırı yeter. Etkiler madde 4 tablosunda.
4. **Yalnız AOF'si bozuk satır (2024 sonrası kaynak hatası).** (a) O gün fiyatsız gün olsun, karantina açmasın (V1, V2
   gibi); kapanışı limit bazı kalsın (PR 266). Ölçüldü (geçici motor `m-4a`, PR 266 üstüne, anlık `20261005-1949`):
   2015-2022 karantina payı değişmez (%1,211 / %1,258); 2026 karantina başlangıcı 50 → 0; 01.10.2026'da karantinadaki
   hisse 47 → 0; 2026 karantina payı %6,28 → %0,69. Kapanış baz kalmazsa sahte aşım geri gelir (aynı ölçüde 50 → 100).
   (b) Bugünkü gibi 250 gün karantina.

## Dersler (tansu-hata "Lesson")

İncelemenin bulduğu hatalar. Genel kodlama standartları dosyası (proje dışında) iş emri gereği değiştirilmedi;
"Seen once" satırı olarak dosya sahibine önerilir:

- Sınır karşılaştırması: tik ızgarasında olmayan baz (olay günü, baz × çarpan) eşitlik durumunu gerçek yapar. Katı
  karşılaştırma yazmadan önce ızgara dışı bazla bir test yazılmalı (PR 265 Tur 1).
- Simetrik iki sınırın yalnız birini test etmek: iki sınırın ve her alanın kendi testi olmalı; mutasyonla sınanır
  (PR 268 Tur 1). Var olan "A matcher has both sides" kuralına yakın.
- Sayım iddiası: "55 düşüş" (54 düşüş, 1 yükseliş) ve eskimiş yorumlar; var olan "A claim matches its evidence" kuralı
  kapsar (PR 263, PR 266 Tur 1).
- Kendi ölçüm hatam: geçici kopyadaki kodu koşarken çalışma klasöründeki `tansu` paketi önce yüklendi (iki farklı
  dalın modülleri karıştı, 33.937 sahte hata). Doğru klasörden yeniden koşuldu (0 hata). Geçici kopyadan ölçüm, o
  klasörde koşulmalı ve `tansu.__file__` yazdırılmalı.

## Yapılamayanlar ve sınırlar

- SPEC 3.9 ek cümleleri (5), (6), (7) yerel `docs/SPEC.md`'ye yazılamadı: dosya `yeniden-kurulus` çalışma ağacındadır ve
  bir kanca bu oturumun başka çalışma ağacına yazmasını engeller. Önerilen metin PR 263, 266, 265 gövdelerinde ve oturum
  not klasöründe (`veri-kalitesi-spec-3-9.md`). Dosya sahibi yazmalı.
- `main` TASARIM 5.1 ("Bozuk satır baz fiyat olmaz") ve 5.13 ("en az yarısı") `yeniden-kurulus` kurallarının gerisinde;
  bu iş `main` belgesini yalnız #267 uygulama notu için değiştirdi.
- Ayrık grup, 2010-2014 strateji sonuçları ve `kanit/gartley-takip/` hiç koşulmadı ve değişmedi. İleri izleme günlüğünü
  Gartley oturumu yeniden hesaplar.
- Yerel test koşuları yalnız değişen modüllerin testleridir; tam takımı CI koşar.
- Geçici betikler ve çıktılar `%TEMP%\tansu-veri-kalitesi\` altındadır (Git dışında).
