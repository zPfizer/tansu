# Gartley PDF setup'ları: 13 deneme ve ayrık hisse sınavı (30.10.2026)

İstek (Levent, 30.10.2026): üç Gartley PDF'indeki bütün setup'lar denensin, en başarılısı bulunsun, hepsinin sonucu
raporlansın. Ön kayıt `gartley-yontem/plan-pdf.md`; setup listesi PDF işleme oturumundan, üç bağımsız sayfa
kontrolünden sonra.

## Sonuç: HAYIR

Ayrık grupta (185 hisse, 2015-2022, 100.000 TL; yalnız nakit 234.179 TL) iki aday da üç şartı birlikte tutmadı
(k = 5, baraj p < 0,01). Ayrık grup burada ikinci kez kullanıldı; temiz sınav değildir. 13 deneme içinden seçildikleri
için sonuçlar seçim yüzünden şişkindir.

| Aday | Sinyal düzeyi | Faiz | İşlem kârı | En iyi üç olmadan | Son kasa | Nakitten fark | Düşüş | Karar |
|---|---|---|---|---|---|---|---|---|
| S2-Z (MTI, kural seçimi) | 101 dolum, ort. 0,79 R, ortanca −1,12 R, p 0,008 | 65.289 | 52.025 | −22.352 | 217.314 | −16.865 | −%28,5 | HAYIR (şart 2 ve 3) |
| S3 (Seo X3, en düşük p) | 180 dolum, ort. 0,39 R, ortanca −1,06 R, p 0,018 | 50.605 | 104.351 | 54.648 | 254.956 | +20.777 | −%33,1 | HAYIR (şart 1) |

- En başarılı setup S3'tür: iki grupta da işlem kârı artıdır ve en iyi üç işlem çıkınca da artı kalır; kasa iki grupta
  da nakdin üstündedir. Ama p 0,018 barajı (0,01) geçmez ve düşüş −%33'tür.
- S2-Z'nin kazancı birkaç büyük işlemden gelir; en iyi üç işlem çıkınca eksidir.

## Ayar grubu (371 hisse, 2015-2022), 13 deneme

Tablo `gartley-yontem/sinav-pdf/aile-ayar.tsv`. Öne çıkanlar:

| Deneme | Dolum | Ort. R | p | İşlem kârı | En iyi üç olmadan |
|---|---|---|---|---|---|
| S3 | 295 | 0,41 | 0,004 | 393.743 | 295.459 |
| S2-Z | 136 | 0,53 | 0,044 | 164.312 | 49.918 |
| S2-V1 | 136 | 0,49 | 0,049 | 156.898 | 49.218 |
| S1 (Behle-Conway) | 136 | 0,09 | 0,29 | 43.997 | 9.284 |
| S1-P3 | 325 | −0,14 | 0,96 | −9.965 | −34.623 |

- Aile şans payı: N = 13, PBO 0,48; S2-Z için Deflated Sharpe 0,33. Yıllık nakit üstü Sharpe S3'te 0,60, şans eşiği
  0,45.
- S2-Z pivot okumasına duyarlıdır: eşit tepeler pivot sayılınca p 0,064, aynı türden pivotun yer değiştirmesi
  kapatılınca p 0,17 (bağımsız inceleme).

## Dürüstlük kaydı

- Ön kayıt ceb1e7a (ilk commit beyin yolları içerdi; 4fb3d47 ile çıkarıldı, geçmişte duruyor). Değişiklik 1 (S3
  eklendi, k = 5) ve `pdf.py` (SHA-256 `3e8f2dc6…a955`) ayrık grupta hiçbir koşudan önce 5e7916c ile gönderildi.
- Bağımsız inceleme S2-Z ve S3'ü kendi koduyla yazdı: sinyal ve işlemlerin hepsi eşleşti, ileriye bakma yok, sınav
  yolu kilitli (NOTLU GEÇTİ). Kilit kayıtları `gartley-yontem/sinav-pdf/kilit-*.txt`.
- Denenmeyenler: satış yönleri, açılış fiyatı ya da gün içi veri isteyen kurallar, S1-V4.
