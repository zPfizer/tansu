# gartley: sınama özeti

Bu rapor seviye ölçümüdür; alım-satım talimatı değildir.

Veri görüntüsü: 20261028-1723. Dönem: 2021-2025. Parametreler (ayarlı, 2026-10-29): pivot = sag_bar_10, tolerans = 0.04, gecerlilik = 5, stop = X, rr_min = 1.4.

| Dönem | Sinyal | Dolum | Beklenti R | Toplam R | Kazanma |
|---|---|---|---|---|---|
| 2021 | 34 | 4 | n/a (N = 4) | 2.22 | n/a (N = 4) |
| 2022 | 45 | 2 | n/a (N = 2) | 3.55 | n/a (N = 2) |
| 2023 | 59 | 16 | n/a (N = 16) | 8.89 | n/a (N = 16) |
| 2024 | 41 | 4 | n/a (N = 4) | 1.49 | n/a (N = 4) |
| 2025 | 56 | 9 | n/a (N = 9) | 11.68 | n/a (N = 9) |
| Bütün yıllar | 235 | 35 | 0.80 | 27.83 | 60% |
| Bütün yıllar, tavan kapanışsız | 235 | 35 | 0.80 | 27.83 | 60% |

Bütün yıllar: en büyük düşüş 5.24 R, açık işlem 1.

Izgara: 36 nokta; son ayar seçimi: pivot = sag_bar_10, tolerans = 0.04, gecerlilik = 5, stop = X (sağlam puan 0.84 R, N = 34)

Örneklem dışı (2023H1-2025H2): N = 34, toplam 30.12 R; ortalama verim 1.49 (5/6 adım).

Saklı dönem 01.01.2026-30.09.2026: N = 4, toplam 2.29 R.

Monte Carlo (tohum 20261028, 1000 koşu, örneklem dışı N = 34), p5 / p50 / p95:

- Bootstrap toplam R: 16.29 / 30.45 / 43.46; en büyük düşüş R: 2.05 / 3.10 / 5.79; batma riski 0.0%
- Sıra karıştırma en büyük düşüş R: 2.07 / 3.10 / 5.15
- Rastgele giriş koşu ortalaması R: -0.18 / 0.22 / 0.63; strateji ortalaması 0.89 R, yüzdelik 99.4

Bayraklar. Program hiçbir stratejiyi kendisi onaylamaz; bu bayraklar yalnız Levent'in kararına yardım eder.

- Örneklem dışı beklenti 0'ın üstünde (R): evet (0.89 R) (N = 34)
- Strateji rastgele girişlerin 95. yüzdeliğinde ya da üstünde: evet (yüzdelik 99.4) (N = 34)
- Bootstrap toplamının 5. yüzdeliği 0'ın üstünde: evet (16.29 R) (N = 34)
- Saklı dönem toplamı 0'ın üstünde (bilgi): evet (2.29 R) (N = 4)
- Uyarı: kazanma oranı %90 ya da üstü (örneklem dışı): hayır (65%) (N = 34)
- Uyarı: kazanma payı %40-60 dışında (örneklem dışı, varsayım): evet (65%) (N = 34)
- Uyarı: seçilen ızgara noktasının kendi puanı 0 ya da altında: hayır (0.84 R) (N = 34)
- Uyarı: bir sembol toplamın %40'ından fazlasını veriyor (2021-2025): hayır (METRO 16%) (N = 35)

Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV.
