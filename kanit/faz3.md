# Faz 3: gartley çekirdeği ve `tansu sina`

Tarih: 26.10.2026. Dal: `faz-3-gartley` → `yeniden-kurulus`.

## Yapılanlar

- `gostergeler.atr_basit`: ATR(14) = gerçek aralığın basit ortalaması (SPEC 3.12); Wilder `atr` seçenek olarak kaldı.
- `tansu/yapi.py`: sağ-bar pivotları (onay i+k) ve yüzde zigzag; `ardisik` dönüşümlü tepe-dip sırası.
- `tansu/islem.py`: `limit` giriş, sinyal anında stop denetimi, dolumda stop altı (hemen çıkış, kayıp), `dokunus` ve `kapanis` stop, iki hedef ve payları, maliyet (taraf başına %0,15 + BSMV), R ve 0,5 ATR risk tabanı, tavan/taban kilidi, dolum günü kuralı, `acik` işareti, işlem kaydı (SPEC 5.1-5.5).
- `tansu/strateji.py` (arayüz), `tansu/stratejiler/` (kayıt), `tansu/stratejiler/gartley.py` (boğa XABC, Carney oranları, D = A − 0,786 × (A − X), stop X, hedef1/hedef2 = A-D'nin 0,382/0,618'i, hedef3 = C bilgi, `rr_min` kapalı).
- `tansu/sinama.py` ve `tansu/rapor.py`: yıl tabloları (2021-2025), bütün yıllar, tavan kapanışsız satır, isabet tablosu, kümülatif R eğrisi (SVG), düşen sinyal nedenleri, sembol tablosu; `rapor/gartley/sinama.html`, `ozet.md`, `islemler.csv`.
- `tansu sina <ad> [--ac]`; `durum.csv` geçişi `taslak` → `sinandi`.
- Kural kartı `stratejiler/gartley.md` ve altın olgular `tests/altin/gartley.csv` yerelde (Ek B #12).
- Bağımsız inceleme (ayrı ajan, salt okuma): 2 hata bulundu ve düzeltildi (taban kilidi gününde kapanış stopu kayboluyordu; taban kilitli günde dolan işlem aynı gün satılıyordu); ikisine test eklendi. Ayrıca: eğri sırası kararlı, MFE/MAE dolum gününü saymıyor, HTML kaçışı, tavan kapanışsız satır.

## Komutlar ve çıktı

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q
151 passed in 4.67s
$ .venv\Scripts\python.exe -m ruff check tansu tests
All checks passed!
$ .venv\Scripts\python.exe -m ruff format --check tansu tests
31 files already formatted

$ .venv\Scripts\python.exe -X utf8 -m pytest -q tests/test_altin_gartley.py -rs
1 passed in 1.00s

$ .venv\Scripts\python.exe -X utf8 -m tansu sina gartley
gartley: 17 sinyal, 3 dolum, toplam 2.55 R
rapor: rapor\gartley\sinama.html; durum: sinandi
```

Altın test (yerel veri, görüntü 20261026-2108, 48 sembolün hepsi tam): varsayılan dedektör SOKE'de X 10.20 (29.12.2025), A 21.20 (06.05.2026), B 14.10, C 19.63 buluyor; C onayı 10.08.2026, `limit` seviye 12.554, stop 10.20, durum AKTIF. Tansu'nun taraması: 0.786 = 12.55, D = 12.53, durum AKTIF. Fark %1 toleransın içinde.

Dönem tablosu (sinyal tarihi 2021-2025, varsayılan parametreler, ayarsız):

| Dönem | Sinyal | Dolum | Toplam R |
|---|---|---|---|
| 2021 | 1 | 0 | 0.00 |
| 2022 | 8 | 1 | 1.80 |
| 2023 | 2 | 0 | 0.00 |
| 2024 | 3 | 1 | -1.03 |
| 2025 | 3 | 1 | 1.78 |
| Bütün yıllar | 17 | 3 | 2.55 |

Düşen 14 sinyalin nedeni: emir süresi doldu (10 gün içinde D'ye inmedi). 30 kurulumun altında oranlar `n/a (N = x)`.

Kurulumlar: VESTL 28.06.2022 (hedef2, +1,80 R), MGROS 09.10.2024 (stop, −1,03 R), TAVHL 11.09.2025 (hedef2, +1,78 R).

## Atlanan

- Ayar, ileri yürüme, saklı dönem, Monte Carlo: faz 4-5 (gece 2).
- pstack `deslop` ve `no-comments` geçişleri koşulmadı; yerine bağımsız inceleme ajanı kullanıldı.
