# Performans profili (16.10)

Makine (psutil ve nvidia-smi, 16.10): 24 fiziksel, 32 mantıksal çekirdek; bellek 95,7 GB, boş 66,4 GB;
GPU NVIDIA GeForce RTX 5070 Ti, 16303 MiB, sürücü 610.88.

Ölçüm aracı depoda tutulmadı (CLAUDE.md kural 4). Ölçüm, `calistir`'ı 1, 4, 8, 16, 24 ve 32 işçiyle koşturup süreyi `time.perf_counter`, CPU'yu ve işçi belleğini psutil ile yarım saniyede bir örnekledi.
(çalışma ağacı TANSU-b35, kod 239429c, anlık görüntü 20261014-1930; süre iş hazırlığını ve süreç açılışını kapsar).
Ana süreç belleği (anlık görüntü okunduktan sonra): 0,27 GB.

| aile | hisse | iş | işçi | süre sn | sn/iş | ort. CPU % | işçi başı tepe bellek GB | süreç |
|---|---|---|---|---|---|---|---|---|
| hepsi | hepsi | 1205 | 1 | 39.6 | 0.033 | 19 | 0.00 | 0 |
| hepsi | hepsi | 1205 | 4 | 12.1 | 0.010 | 29 | 0.17 | 4 |
| hepsi | hepsi | 1205 | 8 | 8.3 | 0.007 | 40 | 0.17 | 8 |
| hepsi | hepsi | 1205 | 16 | 7.4 | 0.006 | 64 | 0.17 | 16 |
| hepsi | hepsi | 1205 | 24 | 7.5 | 0.006 | 83 | 0.17 | 24 |
| hepsi | hepsi | 1205 | 32 | 8.3 | 0.007 | 86 | 0.17 | 32 |

Ek ölçüm (kapı, kapi.md): hisse başına EMA işi 0,262 sn (27 hücre), çift başına 0,039 sn (6 hücre), tek işçi.

Okuma:
- 16 işçiden sonra süre düşmüyor; 32 mantıksal çekirdek 24 fiziksel çekirdekten yavaş (8,3 / 7,5 sn). Kalan süre
  ana süreçteki iş hazırlığı ve süreç açılışıdır (16 işçide de ~7 sn). Karar: işçi sayısı fiziksel çekirdek sayısıyla
  sınırlanır (YORUM, bu ölçüm).
- İşçi başı tepe bellek 0,17 GB: `ISCI_BELLEK_GB` = 0,25 (ölçüm + pay, YORUM). 66 GB boş bellekte bellek bağlamaz.
- Ortalama CPU tek işçide %19 (32 çekirdekten biri dolu ve hazırlık), 24 işçide %83.

GPU:
- `py -3 -c "import torch;print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"` → `torch 2.14.0+cpu cuda False`.
- cupy yok (makinedeki genel Python'da ve projenin `.venv`'inde); `.venv`'de torch ve numba da yok.
- Sonuç: GPU var, GPU hesap kütüphanesi yok; GPU hızı ölçülemedi, GPU kullanılmadı. Bir kütüphane kurmak yeni
  bağımlılık ve büyük indirme ister. İş her gün bir önceki güne bağlı (stop, geçiş) bir döngüdür; bütün koşu 24 işçide
  7,5 sn sürdüğü için GPU'nun kazandırabileceği süre en çok bu 7,5 sn'dir.

Sürüm 2 (17.10), son kodla geliştirme koşusu `20261016T214244-65c468` (kod 02341c8, `kirli: false`; `kayit/deneme.jsonl`):
1.205 iş, 24 işçi, 9,84 sn; komutun ilerleme satırında CPU %94-95. Sürüm 1 koşusu 8,72 sn idi: fark 2 katın altında,
kapı yeniden ölçülmedi. GPU kullanılmadı: hesap kütüphanesi kurulu değil.
Denetim tur 1 sonrası kod 157fb8d, koşu `20261016T221419-5e57c1`: 1.205 iş, 24 işçi, 9,56 sn; ilerleme satırında CPU %87.
