# Sadakat kontrolü

Getiriye bakılmaz. Komut: `python -m tansu sadakat`. Tolerans önceden yazılıdır: gösterilen son hanenin yarısı (±0.005); tarih ve gün tam eşleşir.

## EMA sıkışması (KRDMD)

Anlık görüntü: `20261005-1452`. Ham kapanış, EMA20/50/100/200 `ewm(adjust=False)`, oran = (en büyük EMA − en küçük EMA) / EMA200, eşik ≤ %1,2, en az 3 gün, son 130 gün, rapor tarihi 2026-04-09.

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
