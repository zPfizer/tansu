# Sadakat kontrolü

Getiriye bakılmaz. Komut: `python -m tansu sadakat`. Tolerans önceden yazılıdır: gösterilen son hanenin yarısı (±0.005); tarih ve gün tam eşleşir.

## EMA sıkışması (KRDMD)

Anlık görüntü: `20261005-1504`. Ham kapanış, EMA20/50/100/200 `ewm(adjust=False)`, oran = (en büyük EMA − en küçük EMA) / EMA200, eşik ≤ %1,2, en az 3 gün, son 130 gün, rapor tarihi 2026-04-09.

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

Anlık görüntü: `20261005-1504`. Ham kapanış, Y = VAKBN, X = GARAN, 4204 ortak işlem günü (2010-01-04 – 2026-10-02). Hedef: Z_t -3.108, Z_{t−1} -3.404.

Aday kümesi önceden yazılıdır: spread = log oran ya da β'lı kalıntı (`log Y − a − b·log X`, pencere içi OLS); pencere 10–400 işlem günü; ddof {0; 1}; ham fiyat. Tolerans ±0.0005; gevşek bant ±0.05 yalnız tek aday kalırsa. Rapor tarihi bilinmediği için çift bütün işlem günlerinde aranır. Getiri hesaplanmaz.

1564 aday denendi.

Sıkı toleransta eşleşme yok. Gevşek bantta 534 aday (690 gün) eşleşti: tek aday kalmadığı için **üretmedi**. Kural YORUM kalır: log oran, 60 gün.
