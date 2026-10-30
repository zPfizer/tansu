# Gartley PDF setup ailesi: ön kayıt (30.10.2026)

Bu dosya koşulardan önce yazıldı ve commit edildi. Kural, değer ve geçme şartı sonradan değişmez; değişirse
`deneme-defteri.tsv` dosyasına yeni satır olarak yazılır ve deneme sayılır.

## Soru

Levent'in 30.10 paylaştığı üç Gartley PDF'indeki setup'lardan hangisi BIST günlük verisinde en iyi sonucu verir, ve
o setup faizden ayrı gerçek bir kazanç gösterir mi?

## Kaynak

Setup listesi: PDF işleme oturumunun çıkardığı liste (depo dışında; SHA-256
`16eeb10f70ed8452a9f23676a5f0da0059360149990db05d3604f0b5b44c74bb`, bağımsız sayfa kontrolünden sonra düzeltilmiş
hâli). PDF'lerin açık bıraktığı her kural için aşağıda tek değer seçildi.

## Ortak kurallar

- Veri, gruplar, dönem, maliyet, sinyal düzeyi R ve kümeli yeniden örnekleme `plan.md` ile aynı: ayar grubu 371
  hisse, ayrık grup 185 hisse, 2015-2022, 2014 ısınma.
- Yalnız alış. TANSU yalnız alış yönlü çalışır; PDF'lerdeki satış yönü denenmez.
- Pivot: güç N (önceki N ve sonraki N mumun yükseği daha düşük; dip için ayna). Pivot N mum sonra kesinleşir; sinyal
  C'nin kesinleştiği gün doğar. Varsayılan N = 7 (Behle-Conway testi).
- Oran toleransı: mutlak T = 0,10 (Behle-Conway testi; AB/XA ve BC/AB dışındaki oranlarda çıkarım).
- Emir: D seviyesinde limit alış. Dolumdan önce düşük ≤ X ya da yüksek > C olursa ya da X'ten bu yana 100 mum
  geçerse emir düşer (Behle-Conway en uzun desen 100 mum). Boşlukla dolum dondurulmuş motorun limit kuralıyla.
- Çıkış: setup'ın stop ve hedefi. Aynı gün ikisi birden değerse önce stop. Stop altında açılışta ağırlıklı ortalama
  fiyattan çıkış. İz süren stop yok. Süre çıkışı yalnız setup söylüyorsa.
- Para katmanı: `kanit/gartley-para/ayar.json` boyut ve nakit kuralları (risk %5, pozisyon en çok %33, nakit yetmezse
  küçült, likidite %10, boş nakde %15 kesintili faiz); çıkış setup'tan.
- Her sonuç üç parçaya ayrılır: faiz geliri, işlem kârı, en iyi üç işlem olmadan işlem kârı; ayrıca son kasa ve
  yalnız nakit kasası.

## Aile (13 deneme)

| Kod | Kaynak | Kural |
|---|---|---|
| S1 | Behle-Conway | X<A dip-tepe, A>C>B>D>X. AB/XA 0,618±T, BC/AB [0,618−T; 0,786+T], CD/BC [1,27−T; 1,618+T] (D ile), AD/XA 0,786. D = A − 0,786·XA. Stop X. Hedef D + 0,618·(C − D). Süre çıkışı yok. |
| S1-V1 | Behle-Conway | S1 + R/R süzgeci: 0,618·(C − D) / (D − X) ≥ 2,0. |
| S1-V2 | Behle-Conway | S1, ama limit yerine teyit: dokunuştan sonraki 5 mum içinde kapanış > önceki kapanış olan ilk gün; ertesi gün ağırlıklı ortalama fiyattan alış. Stop ve hedef S1. |
| S1-V3 | Behle-Conway | S1 + zaman simetrisi: X'ten dolum gününe kadar geçen mum sayısı kadar tut; stop ve hedef açık kalır. |
| S1-V5 | Behle-Conway | Tetik: CD/BC'yi ilk kez en az 1,27 yapan mum (T yok), diğer oranlar toleransta ve CD/BC ≤ 1,618 + T. D = o mumun düşüğü; ertesi gün ağırlıklı ortalama fiyattan alış. Stop X, hedef D + 0,618·(C − D). |
| S1-P3 | Behle-Conway | S1, pivot gücü N = 3 (Şekil 2). |
| S1-T20 | Behle-Conway | S1, T = 0,20 ("modified" örnek). |
| S1-Z10 | Behle-Conway | S1, pivot yerine günlükte %10 zigzag (kaynaktaki diğer pivot tanımı). |
| S2-Z | MTI | Sıra ve oranlar S1 gibi, ama BC/AB [0,618−T; 0,786+T], CD/BC [1,27−T; 1,618+T] (diyagram bölgeleri); C ≥ A olursa geçersiz. Limit D = A − 0,786·XA. Stop X (birincil A). Hedef X + 1,27·(A − X). |
| S2-T | MTI | S2-Z, ama metin değerleri: BC/AB 0,618±T, CD/BC 1,618±T. |
| S2-V1 | MTI | S2-Z, ama hedef D + 1,27·(A − D) ("CD uzantısı" okuması). |
| S3 | Seo X3 | AB/XA 0,618±T, BC/AB [0,382−T; 0,886+T]. D = C − 1,272·(C − B), D > X olmalı. Limit D. Stop X (PCI tanımsız). Hedef D + 2,5·(D − X). |
| S3-A | Seo X3 | S3, stop D − 1·ATR(14) (C onay günü), hedef D + 2,5·ATR(14). |

Denenmeyenler: bütün satış yönleri; S1-V2'nin "kapanış > açılış" okuması (veride açılış yok); S1-V4 iç içe desenler
(kurallar açık); saatlik ve dakikalık örnekler; Seo'nun M15-H4 örnekleri.

## Seçim (yalnız ayar grubu)

- 13 denemenin hepsi ayar grubunda koşar ve raporlanır.
- En iyi: en az 30 dolumlu denemeler içinde sinyal düzeyi ortalama R'si en yüksek olan. Eşitlikte daha az kurallı.
- Aile için Deflated Sharpe ve PBO (günlük nakit üstü getiri, para katmanı, N = 13).

## Değişiklik 1 (30.10.2026, ayar grubu koşularından sonra, ayrık grupta hiçbir koşudan önce)

Kurala göre en iyi S2-Z'dir (ortalama 0,525 R, 136 dolum, p 0,044). Ama ortanca R −1,10'dur ve sonuç birkaç büyük
işlemden gelir. S3 ayar grubunda en düşük p'yi (0,004, 295 dolum, ortalama 0,411 R) ve en yüksek işlem kârını verdi.
Seçim yalnız ayar grubu sonuçlarıyla yapıldığı için S3 de sınava eklenir. Bu bir değişikliktir ve deneme sayılır:
iki aday sınava girer, k = 5 (önceki 3 + 2), baraj p < 0,01. Kurallar ve değerler değişmez.

## Sınav (ayrık grup, yalnız en iyi deneme, bir kez)

- Geçme şartı `plan.md` ile aynı üç şart. k = 4 (önceki sınavın 3 adayı + bu): baraj p < 0,0125.
- Ayrık grup ikinci kez kullanılıyor; temiz sınav değildir. 13 deneme içinden seçilen en iyi sonuç seçim yüzünden
  şişer. Rapor bunu açıkça yazar.
