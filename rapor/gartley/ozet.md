# gartley: sınama özeti

Bu rapor seviye ölçümüdür; alım-satım talimatı değildir.

Veri görüntüsü: 20261028-2353. Dönem: 2021-2025. Parametreler (ayarlı, 2026-11-01): pivot = sag_bar_10, tolerans = 0.04, gecerlilik = 5, stop = X, rr_min = 1.4.

Veri kapısı: temiz. Karantina oranı 0.01% (eşik 1%), olay denetimi farkı oranı 0.23% (eşik 2%); 04.01.2021 ve sonrası 762231 hisse-gün. Eksik gün olarak işlenen kaynak günü hatası: 2026-05-21.

| Dönem | Sinyal | Dolum | Beklenti R | Toplam R | Kazanma |
|---|---|---|---|---|---|
| 2021 | 31 | 3 | n/a (N = 3) | -0.46 | n/a (N = 3) |
| 2022 | 39 | 2 | n/a (N = 2) | 3.55 | n/a (N = 2) |
| 2023 | 57 | 15 | n/a (N = 15) | 9.91 | n/a (N = 15) |
| 2024 | 42 | 5 | n/a (N = 5) | 3.73 | n/a (N = 5) |
| 2025 | 55 | 11 | n/a (N = 11) | 12.65 | n/a (N = 11) |
| Bütün yıllar | 224 | 36 | 0.82 | 29.38 | 61% |
| Bütün yıllar, tavan kapanışsız | 221 | 36 | 0.82 | 29.38 | 61% |

Bütün yıllar: en büyük düşüş 4.22 R, açık işlem 1.

Izgara: 36 nokta; son ayar seçimi: pivot = sag_bar_10, tolerans = 0.04, gecerlilik = 5, stop = X (sağlam puan 0.86 R, N = 35)

Örneklem dışı (2023H1-2025H2): N = 41, toplam 28.72 R; ortalama verim 1.73 (5/6 adım).

Saklı dönem 01.01.2026-30.09.2026: N = 4, toplam 4.31 R.

Monte Carlo (tohum 20261028, 1000 koşu, örneklem dışı N = 41), p5 / p50 / p95:

- Bootstrap toplam R: 13.15 / 29.01 / 45.06; en büyük düşüş R: 2.08 / 4.12 / 7.23; batma riski 0.0%
- Sıra karıştırma en büyük düşüş R: 2.32 / 3.99 / 6.26
- Rastgele giriş koşu ortalaması R: -0.15 / 0.21 / 0.57; strateji ortalaması 0.70 R, yüzdelik 98.4

Bayraklar. Program hiçbir stratejiyi kendisi onaylamaz; bu bayraklar yalnız Levent'in kararına yardım eder.

- Örneklem dışı beklenti 0'ın üstünde (R): evet (0.70 R) (N = 41)
- Strateji rastgele girişlerin 95. yüzdeliğinde ya da üstünde: evet (yüzdelik 98.4) (N = 41)
- Bootstrap toplamının 5. yüzdeliği 0'ın üstünde: evet (13.15 R) (N = 41)
- Saklı dönem toplamı 0'ın üstünde (bilgi): evet (4.31 R) (N = 4)
- Uyarı: kazanma oranı %90 ya da üstü (örneklem dışı): hayır (59%) (N = 41)
- Uyarı: kazanma payı %40-60 dışında (örneklem dışı, varsayım): hayır (59%) (N = 41)
- Uyarı: seçilen ızgara noktasının kendi puanı 0 ya da altında: hayır (0.86 R) (N = 35)
- Uyarı: bir sembol toplamın %40'ından fazlasını veriyor (2021-2025): hayır (METRO 15%) (N = 36)

Varsayım: alış ve kapanışa bağlı çıkışlar ertesi günün ağırlıklı ortalama fiyatından (AOF) dolar; veride açılış fiyatı yok. Kayma modellenmedi. Maliyet: taraf başına %0,15 komisyon ve komisyonun %5'i BSMV.
