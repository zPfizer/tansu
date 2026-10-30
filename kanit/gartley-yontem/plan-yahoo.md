# Yahoo verisiyle S3: veri kaynağı karşılaştırması, ön kayıt (30.10.2026)

Bu dosya koşulardan önce yazıldı ve commit edildi. İstek (Levent, 30.10.2026): "veriyi işbankasından alıyoruz ya acaba
yahoonun kini alsak farklı mı olurdu", ardından "Evet, karşılaştır".

## Soru

S3'ün (`plan-pdf.md`) ayar grubu sonucu, İş Yatırım yerine Yahoo verisiyle değişir mi?

## Veri

- İş Yatırım: PDF ailesinin kullandığı veri (`gunler-2014-2025-A.pkl`, SHA-256 `0fdd99a7…`), değişmeden.
- Yahoo: ayar grubundaki 371 hisse, `<kod>.IS`, günlük, 2014-01-01'den indirme gününe. Ek paket yok. Yahoo ürün veri
  kaynağı değildir (TASARIM 4); indirme betiği depo dışında kalır, bu tek seferlik bir kanıt koşusudur.
- Yahoo sütunları:
  - ham fiyat = Yahoo'nun bölünme düzeltmeli fiyatı × tarihten sonraki Yahoo bölünme çarpanları;
  - düzeltilmiş fiyat = ham fiyat × (Yahoo düzeltilmiş kapanış / Yahoo kapanış);
  - `aof` yerine açılış fiyatı (Yahoo ağırlıklı ortalama vermez);
  - hacim TL = ham adet × ham (yüksek + düşük + kapanış) / 3;
  - `xu100` İş Yatırım verisinden.
- Yahoo verisi İş Yatırım verisiyle aynı yoldan geçer: `veri.Anlik`, İş Yatırım kurumsal olayları (aynı anlık görüntü
  `20260101-0000`) ve `sinama.gunler`. Karantina, tavan ve taban kilidi ve ATR aynı kurallarla hesaplanır.
- Takvim: yalnız İş Yatırım verisindeki işlem günleri.
- Karşılaştırma kümesi: iki kaynakta da 2015-2022 verisi olan ortak hisseler. İş Yatırım koşusu da bu kümeyle yapılır.

## Koşular (ayar grubu, 2015-2022; ayrık gruba dokunulmaz)

| Kod | Veri | Not |
|---|---|---|
| Y0 | İş Yatırım, 371 hisse | Düzenek kontrolü: PDF ailesindeki S3 sonucunu (295 dolum) aynen vermeli. |
| Y1 | İş Yatırım, ortak küme | Karşılaştırma tabanı. |
| Y2 | Yahoo, ortak küme | Asıl soru. |
| Y3 | Yahoo, ortak küme, `aof` = (yüksek + düşük + kapanış) / 3 | Farkın açılış fiyatından mı, fiyat değerlerinden mi geldiğini ayırır. |

Kurallar ve değerler S3'tür; `pdf.py` (SHA-256 `3e8f2dc6…a955`) ve `yontem.py` değişmez.

## Ölçüler

- Sinyal düzeyi: dolum, ortalama R, ortanca R, p.
- Para katmanı: faiz geliri, işlem kârı, en iyi üç işlem olmadan işlem kârı, son kasa, yalnız nakit kasası.
- Veri farkı: Yahoo'da olmayan hisse ve gün sayısı; ortak günlerde düzeltilmiş kapanış getirisi farkı (> %1 ve > %5
  olan günlerin payı); karantina günü sayısı (iki kaynak).

## Karar

Geçme şartı yok; yalnız bilgi. Her koşu `deneme-defteri.tsv` dosyasına bir satır olarak yazılır. Sonuç hangi yönde
çıkarsa çıksın raporlanır.
