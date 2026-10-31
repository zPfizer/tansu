# ortalama-kesisim: sınama özeti

Bu rapor seviye ölçümüdür; alım-satım talimatı değildir.

Veri görüntüsü: 20261028-2353. Dönem: 2021-2025. Parametreler (ayarlı, 2026-11-01): ortalama = EMA, cift = 48/247, teyit_gun = 2.

Veri kapısı: temiz. Karantina oranı 0.01% (eşik 1%), olay denetimi farkı oranı 0.23% (eşik 2%); 04.01.2021 ve sonrası 762231 hisse-gün. Eksik gün olarak işlenen kaynak günü hatası: 2026-05-21.

| Dönem | Sinyal | Dolum | Beklenti % | Toplam % | Kazanma |
|---|---|---|---|---|---|
| 2021 | 161 | 160 | 374.30 | 59888.41 | 47% |
| 2022 | 270 | 269 | 231.30 | 62220.97 | 66% |
| 2023 | 153 | 149 | 162.30 | 24183.00 | 76% |
| 2024 | 188 | 185 | 7.78 | 1439.23 | 24% |
| 2025 | 388 | 380 | 14.31 | 5439.05 | 34% |
| Bütün yıllar | 1160 | 1143 | 134.01 | 153170.65 | 47% |
| Bütün yıllar, tavan kapanışsız | 1092 | 1084 | 117.65 | 127535.27 | 47% |

Bütün yıllar: en büyük düşüş 1955.54 %, açık işlem 264.

Izgara: 54 nokta; son ayar seçimi: ortalama = EMA, cift = 48/247, teyit_gun = 2 (sağlam puan 81.23 %, N = 879)

Örneklem dışı (2023H1-2025H2): N = 1881, toplam 82393.38 %; ortalama verim 2.67 (6/6 adım).

Saklı dönem 01.01.2026-30.09.2026: N = 218, toplam -2839.25 %.

Monte Carlo (tohum 20261028, 1000 koşu, örneklem dışı N = 1881), p5 / p50 / p95:

- Bootstrap toplam %: 69734.13 / 81891.59 / 98507.30; en büyük düşüş %: 149.86 / 199.21 / 290.05
- Sıra karıştırma en büyük düşüş %: 154.68 / 199.98 / 276.66
- Rastgele giriş koşu ortalaması %: 32.06 / 38.73 / 46.67; strateji ortalaması 43.80 %, yüzdelik 84.2

Bayraklar. Program hiçbir stratejiyi kendisi onaylamaz; bu bayraklar yalnız Levent'in kararına yardım eder.

- Örneklem dışı beklenti 0'ın üstünde (%): evet (43.80 %) (N = 1881)
- Strateji rastgele girişlerin 95. yüzdeliğinde ya da üstünde: hayır (yüzdelik 84.2) (N = 1881)
- Bootstrap toplamının 5. yüzdeliği 0'ın üstünde: evet (69734.13 %) (N = 1881)
- Saklı dönem toplamı 0'ın üstünde (bilgi): hayır (-2839.25 %) (N = 218)
- Uyarı: kazanma oranı %90 ya da üstü (örneklem dışı): hayır (49%) (N = 1881)
- Uyarı: kazanma payı %40-60 dışında (örneklem dışı, varsayım): hayır (49%) (N = 1881)
- Uyarı: seçilen ızgara noktasının kendi puanı 0 ya da altında: hayır (83.27 %) (N = 879)
- Uyarı: bir sembol toplamın %40'ından fazlasını veriyor (2021-2025): hayır (RALYH 12%) (N = 1143)

Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV.
