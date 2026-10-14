# Boru hattı denetimi

Komut: `python -m tansu denetim` (TASARIM 5.12). Boş dünya 200 tekrar, etkili dünya (her ailenin kendi etkisi, her etki düzeyi) 20 tekrar; her tekrar 125 hisse × 2000 gün, K1 B = 200, Holm m = 2. Gömülü etki: sinyal başına dolum avantajı %5,00, %10,00. Şart: yanlış kabul ≤ %5,00. Sonuç: **GEÇTİ**.

| Aile | Yanlış kabul (ölçüt 1–4) | Yanlış kabul (Kâğıt) | Güç %5,00 (ölçüt 1–4 / Kâğıt) | Güç %10,00 (ölçüt 1–4 / Kâğıt) |
|---|---|---|---|---|
| EMA sıkışması | %0,00 (0/200) | %0,00 (0/200) | %25,00 (5/20) / %25,00 (5/20) | %100,00 (20/20) / %100,00 (20/20) |
| Çift rotasyonu | %0,00 (0/200) | %0,00 (0/200) | %20,00 (4/20) / %0,00 (0/20) | %45,00 (9/20) / %0,00 (0/20) |

Yanlış kabul ve güç tanımı: TASARIM 5.12, "Boru hattı denetimi". "Ölçüt 1–4" sütunları o tanımın kendisidir (ölçüt 1–4 Geçti ve portföy kuralı reddetmedi); "Kâğıt" sütunları ayrıca örneklem ve sağlamlık şartını arar. (bilet 05, 14.10)
