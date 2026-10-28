# Faz 5: Monte Carlo, batma riski, rastgele giriş kıyası

Tarih: 28.10.2026. Dal: `faz-5-montecarlo` → `yeniden-kurulus`.

## Yapılanlar

- `tansu/islem.py`: tek kurulum yürütücüsü (`oyna`), tek R ve net % hesabı (`sonuc`), rastgele giriş için tek kurulum girişi (`rastgele`). `simule` aynı yürütücü üzerine kuruldu; davranış değişmedi (eski ve yeni motor, rastgele sentetik tablolarda 3 tohum, yaklaşık 42.000 kayıt, 0 fark).
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
- Rastgele giriş kıyasında yanlılık yok: rastgele girişli oyuncak stratejide 6 pazarda yüzdelik 6-87.
- Bulunan iki kenar hatası düzeltildi: kurulumu olan adımda uygun gün yoksa çökme (artık `n/a`, rapor nedenini yazar); sinyal günü ATR'si 0 olan şablon koşu ortalamasını NaN yapıp yüzdeliği sessizce 0 gösteriyordu (artık ATR > 0 şartı). İkisi için önce kırmızı test yazıldı.
- Notlar: `dusus` NaN değeri eskisi gibi atlar; saklı dönemde kurulum yoksa bayrak `n/a (N = 0)` yazar.
- Açık not: `sina` kayıtlı ayarla raporlarken "seçilen ızgara noktası" bayrağı yeni ızgaranın son seçimini gösterir; veri ve kod aynıysa ikisi aynı noktadır.

Yorum temizliği: 11 gereksiz yorum silindi; yüzdelik ve sonuç adlı demet oldu.

Düzeltmelerden sonra gerçek veri sayıları değişmedi (yukarıdaki çıktı, kod `d91f82d`).

## Atlanan

- Al-tut referansları (SPEC 5.6): bu gecenin kapsamında değil.
- Rastgele giriş kıyası çift ve kesit listeleri için yok (henüz böyle strateji yok; faz 8).
