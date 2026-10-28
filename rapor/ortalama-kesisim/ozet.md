# ortalama-kesisim: sınama özeti

Bu rapor seviye ölçümüdür; alım-satım talimatı değildir.

Veri görüntüsü: 20261026-2108. Dönem: 2021-2025. Parametreler (ayarlı, 2026-10-28): ortalama = EMA, cift = 50/200, teyit_gun = 0.

| Dönem | Sinyal | Dolum | Beklenti % | Toplam % | Kazanma |
|---|---|---|---|---|---|
| 2021 | 26 | 26 | n/a (N = 26) | 11876.78 | n/a (N = 26) |
| 2022 | 5 | 5 | n/a (N = 5) | 925.27 | n/a (N = 5) |
| 2023 | 3 | 3 | n/a (N = 3) | 36.97 | n/a (N = 3) |
| 2024 | 11 | 11 | n/a (N = 11) | 51.50 | n/a (N = 11) |
| 2025 | 33 | 33 | -2.55 | -84.28 | 30% |
| Bütün yıllar | 78 | 78 | 164.18 | 12806.24 | 41% |
| Bütün yıllar, tavan kapanışsız | 77 | 77 | 166.51 | 12821.08 | 42% |

Bütün yıllar: en büyük düşüş 164.82 %, açık işlem 20.

Izgara: 54 nokta; son ayar seçimi: ortalama = EMA, cift = 50/200, teyit_gun = 0 (sağlam puan 134.72 %, N = 58)

Örneklem dışı (2023H1-2025H2): N = 130, toplam 774.96 %; ortalama verim 0.70 (6/6 adım).

Saklı dönem 01.01.2026-30.09.2026: N = 10, toplam 43.94 %.

Monte Carlo (tohum 20261028, 1000 koşu, örneklem dışı N = 130), p5 / p50 / p95:

- Bootstrap toplam %: 81.87 / 754.32 / 1559.47; en büyük düşüş %: 106.08 / 190.23 / 362.33
- Sıra karıştırma en büyük düşüş %: 123.94 / 185.99 / 291.05
- Rastgele giriş koşu ortalaması %: 3.89 / 8.60 / 14.16; strateji ortalaması 5.96 %, yüzdelik 18.1

Bayraklar. Program hiçbir stratejiyi kendisi onaylamaz; bu bayraklar yalnız Levent'in kararına yardım eder.

- Örneklem dışı beklenti 0'ın üstünde (%): evet (5.96 %) (N = 130)
- Strateji rastgele girişlerin 95. yüzdeliğinde ya da üstünde: hayır (yüzdelik 18.1) (N = 130)
- Bootstrap toplamının 5. yüzdeliği 0'ın üstünde: evet (81.87 %) (N = 130)
- Saklı dönem toplamı 0'ın üstünde (bilgi): evet (43.94 %) (N = 10)
- Uyarı: kazanma oranı %90 ya da üstü (örneklem dışı): hayır (38%) (N = 130)
- Uyarı: kazanma payı %40-60 dışında (örneklem dışı, varsayım): evet (38%) (N = 130)
- Uyarı: seçilen ızgara noktasının kendi puanı 0 ya da altında: hayır (128.63 %) (N = 58)
- Uyarı: bir sembol toplamın %40'ından fazlasını veriyor (2021-2025): hayır (ASELS 22%) (N = 78)

Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV.
