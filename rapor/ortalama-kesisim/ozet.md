# ortalama-kesisim: sınama özeti

Bu rapor seviye ölçümüdür; alım-satım talimatı değildir.

Veri görüntüsü: 20261028-1723. Dönem: 2021-2025. Parametreler (ayarlı, 2026-10-29): ortalama = EMA, cift = 48/247, teyit_gun = 2.

| Dönem | Sinyal | Dolum | Beklenti % | Toplam % | Kazanma |
|---|---|---|---|---|---|
| 2021 | 155 | 149 | 372.29 | 55471.17 | 46% |
| 2022 | 271 | 252 | 227.91 | 57432.08 | 65% |
| 2023 | 153 | 141 | 163.71 | 23082.76 | 77% |
| 2024 | 188 | 177 | 6.34 | 1121.50 | 24% |
| 2025 | 388 | 362 | 11.47 | 4151.86 | 34% |
| Bütün yıllar | 1155 | 1081 | 130.67 | 141259.37 | 47% |
| Bütün yıllar, tavan kapanışsız | 1099 | 1025 | 112.79 | 115605.19 | 46% |

Bütün yıllar: en büyük düşüş 1875.67 %, açık işlem 252.

Izgara: 54 nokta; son ayar seçimi: ortalama = EMA, cift = 48/247, teyit_gun = 2 (sağlam puan 76.63 %, N = 829)

Örneklem dışı (2023H1-2025H2): N = 1672, toplam 75407.71 %; ortalama verim 2.69 (6/6 adım).

Saklı dönem 01.01.2026-30.09.2026: N = 169, toplam -1978.16 %.

Monte Carlo (tohum 20261028, 1000 koşu, örneklem dışı N = 1672), p5 / p50 / p95:

- Bootstrap toplam %: 62098.06 / 74840.61 / 90541.12; en büyük düşüş %: 142.10 / 186.64 / 262.77
- Sıra karıştırma en büyük düşüş %: 147.62 / 186.83 / 261.32
- Rastgele giriş koşu ortalaması %: 33.36 / 39.93 / 49.23; strateji ortalaması 45.10 %, yüzdelik 82.8

Bayraklar. Program hiçbir stratejiyi kendisi onaylamaz; bu bayraklar yalnız Levent'in kararına yardım eder.

- Örneklem dışı beklenti 0'ın üstünde (%): evet (45.10 %) (N = 1672)
- Strateji rastgele girişlerin 95. yüzdeliğinde ya da üstünde: hayır (yüzdelik 82.8) (N = 1672)
- Bootstrap toplamının 5. yüzdeliği 0'ın üstünde: evet (62098.06 %) (N = 1672)
- Saklı dönem toplamı 0'ın üstünde (bilgi): hayır (-1978.16 %) (N = 169)
- Uyarı: kazanma oranı %90 ya da üstü (örneklem dışı): hayır (51%) (N = 1672)
- Uyarı: kazanma payı %40-60 dışında (örneklem dışı, varsayım): hayır (51%) (N = 1672)
- Uyarı: seçilen ızgara noktasının kendi puanı 0 ya da altında: hayır (78.27 %) (N = 829)
- Uyarı: bir sembol toplamın %40'ından fazlasını veriyor (2021-2025): hayır (RALYH 13%) (N = 1081)

Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV.
