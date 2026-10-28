# Faz 5: Monte Carlo, batma riski, rastgele giriş kıyası

Tarih: 28.10.2026. Dal: `faz-5-montecarlo` → `yeniden-kurulus`.

## Yapılanlar

- `tansu/islem.py`: tek kurulum yürütücüsü (`oyna`), tek R ve net % hesabı (`sonuc`), rastgele giriş için tek kurulum girişi (`rastgele`). `simule` aynı yürütücü üzerine kuruldu; bu yeniden düzende davranış değişmedi (eski ve yeni motor, rastgele sentetik tablolarda 3 tohum, yaklaşık 42.000 kayıt, 0 fark). Sonraki davranış düzeltmesi son bölümde.
- `tansu/montecarlo.py` (SPEC 5.8): dikişli örneklem dışı kurulumlar üzerinde (çıkış tarihi sırasıyla) bootstrap (1.000 koşu; toplam ve en büyük düşüş için 5/50/95. yüzdelik; sınıf a için batma riski = düşüşü 25 R ve üstü olan koşuların payı, varsayım), sıra karıştırma (1.000 koşu, düşüş yüzdelikleri), rastgele giriş kıyası (1.000 koşu; her ileri yürüme adımında o adımın gerçek kurulum sayısı kadar rastgele üye gün, `piyasa` girişi, bir gerçek kurulumun stop ve hedef uzaklıkları ATR(14) cinsinden kopyalanır, aynı çıkış kuralları, fiyat 31.12.2025'te kesik; istatistik: koşu başına ortalama R ya da net %). Sabit tohum 20261028; her koşunun kendi akışı var. 30 kurulumun altında tablolar `n/a (N = x)`.
- `tansu/sinama.py`: tek düşüş tanımı (`dusus`), dizi de alır.
- Rapor: "Monte Carlo" bölümü (tohum, üç tablo, sınıf a için batma riski) ve "Bayraklar" bölümü (SPEC 5.9, her bayrak N ile; program stratejiyi kendisi onaylamaz).

## Komutlar ve çıktı

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q
223 passed, 1 skipped in 17.76s   (atlanan: altın test; bu çalışma kopyasında yerel veri yok)
$ .venv\Scripts\python.exe -m ruff format --check tansu tests
38 files already formatted
$ .venv\Scripts\python.exe -m ruff check tansu tests
All checks passed!

$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla gartley     (22.8 s)
gartley: 63 sinyal, 36 dolum, toplam 1.18 R
gartley: ızgara 108 nokta, puanlı 54; seçim pivot=zigzag_1.5 tolerans=0.03 gecerlilik=5 stop=X-2ATR (sağlam -0.02 R, N = 36)
ileri yürüme: örneklem dışı N = 38, ortalama verim -8.23 (4/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 4
Monte Carlo: tohum 20261028, N = 38, rastgele giriş yüzdeliği 82.3
ayar: stratejiler\ayarlar\gartley.json
rapor: rapor\gartley\sinama.html; durum: ayarlandi

$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla ortalama-kesisim     (26.3 s)
ortalama-kesisim: 78 sinyal, 78 dolum, toplam 12806.24 %
ortalama-kesisim: ızgara 54 nokta, puanlı 54; seçim ortalama=EMA cift=50/200 teyit_gun=0 (sağlam 134.72 %, N = 58)
ileri yürüme: örneklem dışı N = 130, ortalama verim 0.70 (6/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 10
Monte Carlo: tohum 20261028, N = 130, rastgele giriş yüzdeliği 18.1
ayar: stratejiler\ayarlar\ortalama-kesisim.json
rapor: rapor\ortalama-kesisim\sinama.html; durum: ayarlandi
```

Veri görüntüsü 20261026-2108. Ayar sonucu faz 4b ile aynı; yalnız json `kod_surumu` yeni koda geçti.

## Sonuçlar (p5 / p50 / p95)

| | gartley (R, N = 38) | ortalama-kesisim (%, N = 130) |
|---|---|---|
| Bootstrap toplam | -5.02 / 2.88 / 10.55 | 81.87 / 754.32 / 1559.47 |
| Bootstrap en büyük düşüş | 1.85 / 3.84 / 8.27 | 106.08 / 190.23 / 362.33 |
| Batma riski (düşüş ≥ 25 R) | %0,0 | yok (sınıf b) |
| Sıra karıştırma en büyük düşüş | 2.41 / 3.70 / 6.06 | 123.94 / 185.99 / 291.05 |
| Rastgele giriş koşu ortalaması | -0.24 / -0.04 / 0.17 | 3.89 / 8.60 / 14.16 |
| Strateji ortalaması, yüzdelik | 0.07 R, 82.3 | %5.96, 18.1 |

Bayraklar (SPEC 5.9):

- `gartley`: örneklem dışı beklenti > 0 evet (N = 38); rastgele girişlerin 95. yüzdeliği hayır (82.3); bootstrap 5. yüzdelik > 0 hayır (-5.02 R); saklı dönem > 0 evet (N = 4, bilgi). Uyarılar: kazanma payı %63 (%40-60 dışında); AKBNK 2021-2025 toplamının %40'ından fazlası (toplam küçük, +1,18 R).
- `ortalama-kesisim`: örneklem dışı beklenti > 0 evet (N = 130); rastgele girişlerin 95. yüzdeliği hayır (18.1); bootstrap 5. yüzdelik > 0 evet; saklı dönem > 0 evet (N = 10, bilgi). Uyarı: kazanma payı %38.

Okunuş: iki stratejide de rastgele giriş kıyası bayrağı kalkmadı. `ortalama-kesisim` rastgele üye günlerde açılıp aynı karşı kesişimle kapanan girişlerin %82'sinden kötü; 2021-2025 TL yükselişinde rastgele uzun girişler de yüksek getiri verdi. `gartley` örneklemi küçük (N = 38) ve bootstrap aralığı sıfırın iki yanında.

## İnceleme

Bağımsız inceleme (ayrı ajan):

- Motor: eski (`f7c022e`) ve yeni `simule`, 1.500 rastgele tablo × 4 çıkış ayarı = 6.000 durumda aynı işlem kaydı ve sayaçları verdi.
- `dusus`: 3.000 rastgele 1-B girdide eski pandas sürümüyle aynı.
- Rastgele giriş kıyasında yanlılık için sınırlı bir sınama: rastgele girişli oyuncak strateji 6 sentetik pazarda yüzdelik 6-87 verdi; belirgin yanlılık görülmedi. Bu sınama yanlılık olmadığını kanıtlamaz.
- Bulunan iki kenar hatası düzeltildi: kurulumu olan adımda uygun gün yoksa çökme (artık `n/a`, rapor nedenini yazar); sinyal günü ATR'si 0 olan şablon koşu ortalamasını NaN yapıp yüzdeliği sessizce 0 gösteriyordu (artık ATR > 0 şartı). İkisi için önce kırmızı test yazıldı.
- Notlar: `dusus` NaN değeri eskisi gibi atlar; saklı dönemde kurulum yoksa bayrak `n/a (N = 0)` yazar.
- Açık not: `sina` kayıtlı ayarla raporlarken "seçilen ızgara noktası" bayrağı yeni ızgaranın son seçimini gösterir; veri ve kod aynıysa ikisi aynı noktadır.

Yorum temizliği: 11 gereksiz yorum silindi; yüzdelik ve sonuç adlı demet oldu.

Düzeltmelerden sonra gerçek veri sayıları değişmedi (yukarıdaki çıktı, kod `d91f82d`).

## Atlanan

- Al-tut referansları (SPEC 5.6): bu gecenin kapsamında değil.
- Rastgele giriş kıyası çift ve kesit listeleri için yok (henüz böyle strateji yok; faz 8).

## Düzeltme: alt limit kilidinde dokunuş stopu (28.10.2026)

Hata: dokunuş stoplu açık işlemde alt limit kilitli günün fiyatı stopa ulaşınca motor bekleyen çıkış kaydetmiyordu. Ertesi gün fiyat stopun üstüne dönerse işlem açık kalıyordu. Düzeltme: bu durumda çıkış bekleyen stop olur ve ilk kilitsiz günün AOF'sinden yapılır. Dayanak: SPEC 1 limit kilidi satırı (alt limitte satış dolmaz, çıkış kilitsiz ilk güne kayar) ve SPEC 5.4 adım 1-3; kayan çıkış adım 2'deki gibi AOF'den dolar. Kilitten önce bekleyen bir çıkış varsa o korunur.

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q tests/test_islem.py -k dokunulan_stop     (düzeltmeden önce)
E   AssertionError: assert (Timestamp('2022-01-07 00:00:00') == Timestamp('2022-01-06 00:00:00'))
1 failed, 27 deselected in 0.14s
$ .venv\Scripts\python.exe -X utf8 -m pytest -q     (düzeltmeden sonra)
224 passed, 1 skipped in 19.77s
$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla gartley --kok <ana çalışma kopyası>\veri            (25.7 s)
$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla ortalama-kesisim --kok <ana çalışma kopyası>\veri   (28.3 s)
```

Bağımsız inceleme (NOTLU GEÇTİ): eski ve yeni motor 20.000 rastgele sentetik tabloda karşılaştırıldı; 2.670 tablodaki her fark kilitli günde dokunulan dokunuş stopundan geliyor, açıklanamayan fark 0. Kapanış stopu, stopsuz kurulum ve kilitten önce bekleyen çıkış değişmedi. Gerçek veride iki stratejinin işlem kayıtları, sayaçları ve rastgele giriş kıyası aynı. İncelemeden sonra çok günlü kilit ve bekleyen çıkışın önceliği için iki test eklendi.

Gerçek veri (görüntü 20261026-2108): iki stratejide de bütün sayılar aynı kaldı; `ozet.md` değişmedi, yalnız json `kod_surumu` yeni koda geçti.

| | önce | sonra |
|---|---|---|
| `gartley` örneklem dışı | N 38, toplam 2.74 R | N 38, toplam 2.74 R |
| `gartley` rastgele giriş yüzdeliği | 82.3 | 82.3 |
| `ortalama-kesisim` örneklem dışı | N 130, ortalama %5.96 | N 130, ortalama %5.96 |
| `ortalama-kesisim` rastgele giriş yüzdeliği | 18.1 | 18.1 |

Neden değişmedi: veride 78 alt limit kilitli gün var, 37'si üyelik günü. `gartley` son parametreleriyle 36 işlemin hiçbiri açıkken kilitli güne denk gelmiyor. `ortalama-kesisim` stopsuzdur; dokunuş stopu yoktur.

## Karar: Gartley R/R kapısı (Ek B #13, 28.10.2026)

Levent'in kararı: kapı Tansu'nun yazdığı gibi uygulanır. Ödül hedef1'e, risk stopa göre ölçülür; oran 1,5'in altındaysa kurulum alınmaz. Eski kod kapıyı hedef2'ye göre ölçüyordu ve varsayılanı kapalıydı. Yeni varsayılan `rr_min` = 1,5; elle verilebilen değerler kapalı, 1,5 ve 2 (ızgarada değil).

Kaynak taraması (yerel havuz, 28.10.2026): X arşivinde Gartley geçen 53 gönderi var; 23'ünün notu var, notu olmayan 30 gönderide seviye ya da kural yok. Tansu'nun Gartley için yazdığı tek R/R kuralı 02.12.2025 gönderisindedir. Aynı gönderideki giriş (XA'nın 0,786 geri çekilmesi), stop (X; seçenek X − 2 ATR, XA 1,13) ve hedef1 (AD'nin 0,382'si) tanımlarıyla oran her Gartley'de ≈ 1,40, X − 2 ATR ve XA 1,13 ile daha düşüktür. 23.08.2026 tarama tablolarındaki kurulumların hesaplanan oranları 1,30-1,42'dir; Tansu bunları kapısız listeler. 20.08.2026 tarihli bir görselde başka bir şema var (D gerçek dipte, hedefler CD bacağına göre, stop X; hesaplanan oran ≈ 2,04); bu şema kural olarak yazılmamıştır ve kodlanmadı.

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q tests/test_gartley.py     (değişiklikten önce)
FAILED tests/test_gartley.py::test_rr_kapisi_hedef1_ile_olculur_varsayilan_kurulumu_eler
1 failed, 4 passed in 0.14s
$ .venv\Scripts\python.exe -X utf8 -m pytest -q     (değişiklikten sonra)
227 passed in 20.19s
$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla gartley     (14.2 s)
gartley: 0 sinyal, 0 dolum, toplam 0.00 R
gartley: ızgara 108 nokta, puanlı 0; puanlı nokta yok, varsayılanlar
ileri yürüme: örneklem dışı N = 0, ortalama verim n/a (0/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 0
Monte Carlo: tohum 20261028, N = 0, rastgele giriş yüzdeliği n/a (N = 0)
rapor: rapor\gartley\sinama.html; durum: yetersiz-ornek
```

Gerçek veri (görüntü 20261026-2108):

| `gartley` | kapı kapalı (önce) | kapı hedef1'e göre 1,5 (sonra) |
|---|---|---|
| 2021-2025 sinyal / dolum | 63 / 36 | 0 / 0 |
| 2021-2025 toplam | 1.18 R | 0.00 R |
| örneklem dışı | N 38, toplam 2.74 R | N 0 |
| rastgele giriş yüzdeliği | 82.3 | n/a (N = 0) |
| durum | ayarlandi | yetersiz-ornek |

Kapı açıkken 108 ızgara noktasının hiçbiri kurulum üretmez (toplam 0). Kapı kapalıyken aynı noktalarda 13.086 kurulum var: stop X ile hedef1 oranı her birinde 1,403; X − 2 ATR ile 0,152-1,118. Kapı kapalı sonuç `rr_min` = kapalı ile yeniden alınabilir; ayar ve komut testleri bu yolu kullanır.
