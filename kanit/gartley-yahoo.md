# Yahoo verisiyle S3: veri kaynağı karşılaştırması (30.10.2026)

İstek (Levent, 30.10.2026): "veriyi işbankasından alıyoruz ya acaba yahoonun kini alsak farklı mı olurdu", ardından
"Evet, karşılaştır". Ön kayıt `gartley-yontem/plan-yahoo.md` (fa804a6); koşular `deneme-defteri.tsv` 34-37; çıktılar
`gartley-yontem/yahoo/`.

## Sonuç: S3 Yahoo verisiyle de artıda, ama zayıflıyor

Ayar grubu, iki kaynakta da verisi olan 321 hisse, 2015-2022, 100.000 TL; yalnız nakit 234.179 TL.

| Koşu | Dolum | Ort. R | p | Faiz | İşlem kârı | En iyi üç olmadan | Son kasa |
|---|---|---|---|---|---|---|---|
| Y1 İş Yatırım | 279 | 0,42 | 0,006 | 54.378 | 398.597 | 297.432 | 552.975 |
| Y2 Yahoo (`aof` = açılış) | 310 | 0,35 | 0,017 | 43.659 | 249.588 | 167.489 | 393.247 |
| Y3 Yahoo (`aof` = tipik fiyat) | 310 | 0,35 | 0,020 | 43.204 | 246.795 | 165.521 | 389.999 |

- Y0 (İş Yatırım, 371 hisse) PDF ailesindeki S3'ü aynen verdi: 295 dolum, 0,411 R, işlem kârı 393.743. Düzenek doğru.
- Yahoo'da işlem kârı %37 düşük; en iyi üç işlem olmadan da artı kalır.
- Açılış fiyatı fark yaratmaz (Y2 ile Y3 neredeyse aynı).
- Çıkarım: fark iki yerden gelir, bu koşular ikisini ayırmaz. Yahoo'da karantina daha az gün kapatır (31 dolum fazla) ve
  fiyat değerleri farklıdır.

## Veri farkı (`yahoo/veri-farki.json`, `yahoo/karantina-tani.json`)

- 371 hissenin 48'i Yahoo'da yok, 2'sinde 2015-2022 verisi yok (çoğu borsadan çıkmış kod).
- Ortak günlerde düzeltilmiş getiri farkı: günlerin %6,7'sinde > %1, %0,3'ünde > %5, 53 günde > %20 (ör. CRFSA
  24.11.2020: Yahoo +%459, İş Yatırım −%6).
- Olayla açıklanmayan limit aşımı (sahte sıçrama): Yahoo 794 gün, İş Yatırım 311 gün.
- Karantinadaki hisse-gün payı: İş Yatırım %34,9, Yahoo %17,8.

## Yan bulgu: İş Yatırım karantinasının çoğu yuvarlama hatası

- İş Yatırım verisinde 22.086 gün "bozuk satır" sayılır (2014-2022, ortak küme); her biri 250 günlük karantina açar.
  Yahoo'da aynı kontrol 16 gün bulur. İşlem olan günlerde bozuk sayı 17.325'tir; bunun 17.091'i düzeltilmiş kapanışın
  düzeltilmiş yüksek-düşük aralığı dışında kalmasından gelir.
- Bu 17.091 günün %99,96'sında ham kapanış ham yüksek ya da ham düşüğe eşittir; ham veri tutarlıdır. Düzeltilmiş kapanış
  ile düzeltilmiş düşük/yüksek farkı %99,98'inde 0,00005'ten küçüktür, yani dördüncü ondalığın yuvarlamasıdır. Bu
  günlerde düzeltilmiş fiyatın ortancası 0,095 TL'dir.
- Neden (`tansu/veri.py` `_gunler`): düzeltilmiş seri kontrolü göreli pay `YUVARLAMA = 1e-4` kullanır. Düzeltilmiş fiyat
  0,5 TL'nin altına inince dört ondalık yuvarlama bu payı aşar ve tutarlı satır bozuk sayılır.
- Etki: ayar grubunda hisse-günlerin üçte biri yeni sinyale kapalı. 29.10 ayarı, ayrık grup sınavları ve PDF ailesi bu
  veriyle koştu. Düzeltme bu işin kapsamı dışındadır.

## Sınırlar

- Yahoo ağırlıklı ortalama fiyat vermez; `aof` yerine açılış (Y2) ve tipik fiyat (Y3) kullanıldı.
- Yahoo ham fiyatı, Yahoo bölünme kayıtlarıyla geri hesaplandı; kurumsal olaylar ve `xu100` İş Yatırım'dan.
- Karantina neden sayımında İş Yatırım tarafı 319 hissedir: INTEK ve LRSHO anlık görüntüde yok (veriye sonradan eklendi).
- Yahoo indirme betiği depo dışındadır (TASARIM 4: Yahoo ürün kaynağı değildir).
