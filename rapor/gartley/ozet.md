# gartley: sınama özeti

Bu rapor seviye ölçümüdür; alım-satım talimatı değildir.

Veri görüntüsü: 20261026-2108. Dönem: 2021-2025. Parametreler (ayarlı, 2026-10-28): pivot = zigzag_1.5, tolerans = 0.03, gecerlilik = 5, stop = X-2ATR, rr_min = kapali. Seviye parametresi farklı: stop = X-2ATR (varsayım), Tansu'nun değeri X.

| Dönem | Sinyal | Dolum | Beklenti R | Toplam R | Kazanma |
|---|---|---|---|---|---|
| 2021 | 17 | 8 | n/a (N = 8) | 0.66 | n/a (N = 8) |
| 2022 | 7 | 3 | n/a (N = 3) | 0.18 | n/a (N = 3) |
| 2023 | 19 | 12 | n/a (N = 12) | 1.72 | n/a (N = 12) |
| 2024 | 7 | 3 | n/a (N = 3) | -1.58 | n/a (N = 3) |
| 2025 | 13 | 10 | n/a (N = 10) | 0.20 | n/a (N = 10) |
| Bütün yıllar | 63 | 36 | 0.03 | 1.18 | 69% |
| Bütün yıllar, tavan kapanışsız | 63 | 36 | 0.03 | 1.18 | 69% |

Bütün yıllar: en büyük düşüş 4.32 R, açık işlem 0.

Izgara: 108 nokta; son ayar seçimi: pivot = zigzag_1.5, tolerans = 0.03, gecerlilik = 5, stop = X-2ATR (sağlam puan -0.02 R, N = 36)

Örneklem dışı (2023H1-2025H2): N = 38, toplam 2.74 R; ortalama verim -8.23 (4/6 adım).

Saklı dönem 01.01.2026-30.09.2026: N = 4, toplam 1.57 R.

Monte Carlo (tohum 20261028, 1000 koşu, örneklem dışı N = 38), p5 / p50 / p95:

- Bootstrap toplam R: -5.02 / 2.88 / 10.55; en büyük düşüş R: 1.85 / 3.84 / 8.27; batma riski 0.0%
- Sıra karıştırma en büyük düşüş R: 2.41 / 3.70 / 6.06
- Rastgele giriş koşu ortalaması R: -0.24 / -0.04 / 0.17; strateji ortalaması 0.07 R, yüzdelik 82.3

Bayraklar. Program hiçbir stratejiyi kendisi onaylamaz; bu bayraklar yalnız Levent'in kararına yardım eder.

- Örneklem dışı beklenti 0'ın üstünde (R): evet (0.07 R) (N = 38)
- Strateji rastgele girişlerin 95. yüzdeliğinde ya da üstünde: hayır (yüzdelik 82.3) (N = 38)
- Bootstrap toplamının 5. yüzdeliği 0'ın üstünde: hayır (-5.02 R) (N = 38)
- Saklı dönem toplamı 0'ın üstünde (bilgi): evet (1.57 R) (N = 4)
- Uyarı: kazanma oranı %90 ya da üstü (örneklem dışı): hayır (63%) (N = 38)
- Uyarı: kazanma payı %40-60 dışında (örneklem dışı, varsayım): evet (63%) (N = 38)
- Uyarı: seçilen ızgara noktasının kendi puanı 0 ya da altında: hayır (0.03 R) (N = 36)
- Uyarı: bir sembol toplamın %40'ından fazlasını veriyor (2021-2025): evet (AKBNK 126%) (N = 36)

Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV.
