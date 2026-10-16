# Kapı: tam koşudan önce süre tahmini (16.10)

Komut: `PYTHONPATH=. .venv/Scripts/python.exe -X utf8 .scratch/tansu-sinama/tools/profil.py <aile> <hisse> <işçi>`
(çalışma ağacı TANSU-b35, kod 239429c, anlık görüntü 20261014-1930, kayıt yazmaz).

| aile | hisse | iş | işçi | süre sn | sn/iş | ort. CPU % | işçi başı tepe bellek GB | süreç |
|---|---|---|---|---|---|---|---|---|
| ema_sikismasi | 5 | 5 | 1 | 1.3 | 0.262 | 15 | 0.00 | 0 |
| ema_sikismasi | 5 | 5 | 5 | 2.0 | 0.393 | 33 | 0.16 | 5 |
| cift_rotasyonu | 20 | 42 | 1 | 1.6 | 0.039 | 18 | 0.00 | 0 |

Seçilen işçi sayısı 5 hissede 5'tir (`isci_sayisi`: iş sayısı bağlar). 5 işte süreç açılışı tek işçiden yavaştır.

Tahmin (99 hisse × iki aile): EMA 99 × 0,262 sn ≈ 26 sn; çift: 99 hissede aynı sektör çifti sayısı bilinmiyordu,
üst sınır 1.150 çift × 0,039 sn ≈ 45 sn. Toplam tek işçide ≈ 71 sn. 60 dakikanın çok altında: ızgara küçültülmedi.

Ölçülen tam koşu (aynı araç, `hepsi 0 1,4,8,16,24,32`): 1.205 iş (99 hisse + 1.106 çift), tek işçide 39,6 sn.
Ayrıntı: performans.md.
