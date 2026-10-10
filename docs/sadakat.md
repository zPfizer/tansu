# Sadakat kontrolü

Getiriye bakılmaz. Komut: `python -m tansu sadakat`. Tolerans önceden yazılıdır: gösterilen son hanenin yarısı (±0.005); tarih ve gün tam eşleşir.

## EMA sıkışması (KRDMD)

Anlık görüntü: `20261005-1949`. Ham kapanış, EMA20/50/100/200 `ewm(adjust=False)`, oran = (en büyük EMA − en küçük EMA) / EMA200, eşik ≤ %1,2, en az 3 gün, son 130 gün, rapor tarihi 2026-04-09.

### Aday: bütün geçmiş

| Ölçü | Tansu | Bizim | Sonuç |
|---|---|---|---|
| Dönem | 2025-12-17 – 2026-01-14 | 2025-12-16 – 2026-01-14 | üretmedi |
| Gün | 20 | 21 | üretmedi |
| Dönem ortalaması % | 0.64 | 0.665 | üretmedi |
| EMA20 (2026-04-09) | 31.92 | 31.9231 | üretti |
| EMA50 (2026-04-09) | 30.74 | 30.7367 | üretti |
| EMA100 (2026-04-09) | 29.58 | 29.5756 | üretti |
| EMA200 (2026-04-09) | 28.43 | 28.4352 | üretmedi |

### Aday: son 3 yıl

| Ölçü | Tansu | Bizim | Sonuç |
|---|---|---|---|
| Dönem | 2025-12-17 – 2026-01-14 | 2025-12-17 – 2026-01-14 | üretti |
| Gün | 20 | 20 | üretti |
| Dönem ortalaması % | 0.64 | 0.641 | üretti |
| EMA20 (2026-04-09) | 31.92 | 31.9231 | üretti |
| EMA50 (2026-04-09) | 30.74 | 30.7367 | üretti |
| EMA100 (2026-04-09) | 29.58 | 29.5756 | üretti |
| EMA200 (2026-04-09) | 28.43 | 28.4366 | üretmedi |

### Aday: son 2 yıl

| Ölçü | Tansu | Bizim | Sonuç |
|---|---|---|---|
| Dönem | 2025-12-17 – 2026-01-14 | 2025-12-17 – 2026-01-14 | üretti |
| Gün | 20 | 20 | üretti |
| Dönem ortalaması % | 0.64 | 0.642 | üretti |
| EMA20 (2026-04-09) | 31.92 | 31.9231 | üretti |
| EMA50 (2026-04-09) | 30.74 | 30.7367 | üretti |
| EMA100 (2026-04-09) | 29.58 | 29.5756 | üretti |
| EMA200 (2026-04-09) | 28.43 | 28.4370 | üretmedi |

## Çift Z (VAKBN–GARAN)

Anlık görüntü: `20261005-1949`. Ham kapanış, Y = VAKBN, X = GARAN, 4204 ortak işlem günü (2010-01-04 – 2026-10-02). Hedef: Z_t -3.108, Z_{t−1} -3.404.

Aday kümesi önceden yazılıdır: spread = log oran ya da β'lı kalıntı (`log Y − a − b·log X`, pencere içi OLS); pencere 10–400 işlem günü; ddof {0; 1}; ham fiyat. Tolerans ±0.0005; gevşek bant ±0.05 yalnız tek aday kalırsa. Rapor tarihi bilinmediği için çift bütün işlem günlerinde aranır. Getiri hesaplanmaz.

1564 aday denendi.

Sıkı toleransta eşleşme yok. Gevşek bantta 534 aday (690 gün) eşleşti: tek aday kalmadığı için **üretmedi**. Kural YORUM kalır: log oran, 60 gün.

## Çift Z, ek aday turu (10.10.2026)

- `fiyat_ols` (Tansu X403: "spread = A - hedge_ratio * B"): fiyat düzeyinde s_t = Y_t − a − h·X_t; a ve h, t'de biten w günlük OLS'den. Z_t = (s_t − ortalama(s)) / std(s); istatistikler aynı pencerenin kendi uyumunun kalıntılarından.
- `sabit_std` (Tansu X404: log farkı, hareketli ortalama, "Sabit standart sapma"): d = log Y − log X; e = d − w günlük hareketli ortalama(d); Z_t = e_t / std(e). Standart sapma bütün mevcut seri için tek sabit sayıdır.
- `dun_pencere` (bugünü dışlayan pencere, bilet 06 notu): `cift.z_skor` ile aynı spread (log oran veya log fiyatların OLS kalıntısı); ortalama ve standart sapma t−1'de biten w günden. Kalıntı modunda OLS uyumu da bu pencereden; Z_t = (s_t − ortalama) / std.

Ham kapanış, Y = VAKBN, X = GARAN; bütün işlem günleri aranır. Hedef: Z_t -3.108, Z_{t−1} -3.404. Pencere 10–400; ddof {0; 1}; her adayda Z ve −Z. Getiri hesaplanmaz.
Aday sayıları (iki işaret dahil): fiyat_ols 1564, sabit_std 1564, dun_pencere 3128; toplam 6256. Tolerans ±0.0005; gevşek bant ±0.05 yalnız tek aday kalırsa.

Sıkı toleransta eşleşme yok. Gevşek bantta 1393 aday (1717 gün) eşleşti: tek aday kalmadığı için **üretmedi**.
Ek tur da üretmedi. Çift Z kalıcı olarak YORUM kalır: log oran, 60 gün.
