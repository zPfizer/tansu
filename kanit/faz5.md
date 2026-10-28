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

## Ölçüm: Gartley PRZ girişi ve geniş evren (28.10.2026)

Soru: Gartley, Tansu'nun yazılı kurallarından çıkmadan ölçülebilir işlem üretir mi? Levent 28.10.2026: "Gatleyi çalıştırmamız lazım planlı ve proglamlı bir şekilde gerekli aksiyonları al." Kapı (hedef1'e göre 1,5) açık kaldı; barajlar ve saklı dönem değişmedi. Kod değişmedi; ölçüm geçici bir kopyada yapıldı.

Denenen giriş: Tansu'nun 02.12.2025 tanımındaki PRZ, yani XA 0,786 seviyesi ile BC 1,272/1,618 uzantısının buluştuğu aralık. Seçenekler: `prz_orta` (0,786 ile en yakın uzantının ortası), `prz_alt` (ikisinin derini), `prz_derin` (0,786 ile 1,618 uzantısının derini). Hedefler ve kapı giriş seviyesine göre hesaplandı; ızgara ve ileri yürüme ürünle aynı.

Evren: önce BIST 30 (görüntü 20261026-2108). Sonra Levent'in onayıyla yalnız bu ölçüm için bütün BIST: bugünkü 805 kod ve 2019'dan beri kapanan 34 kod, mevcut İş Yatırım kaynağıyla bir kez indirildi (655 kodda fiyat var, 2025 sonuna kadar verisi olan 619 sembol). Bu veri depoya ve `veri/`ye girmedi; ürün evreni BIST 30 kalır. Fiyat 31.12.2025'te kesildi, 2026 sonucu hesaplanmadı.

| Giriş (kapı açık) | BIST 30 örneklem dışı | Bütün BIST örneklem dışı: N / toplam / ortalama | Bütün BIST rastgele giriş yüzdeliği |
|---|---|---|---|
| 0,786 (bugünkü) | N 0 | 0 / 0.00 R / n/a | n/a (N = 0) |
| `prz_orta` | N 1, −1.04 R | 172 / −20.94 R / −0.122 R | 99.1 |
| `prz_alt` | N 1, −1.04 R | 149 / −18.80 R / −0.126 R | 98.6 |
| `prz_derin` | N 18, −3.93 R | 436 / −75.51 R / −0.173 R | 100.0 |
| 0,786, kapı kapalı (yalnız kıyas) | N 38, 2.74 R | 233 / 3.09 R / 0.013 R | 23.0 |

Okuma:

- BIST 30'da PRZ girişi ölçülebilir örnek vermez (N 1 ile 18). Bütün BIST'te örnek yeter (N 149-436), ama her seçenek örneklem dışında kaybeder. "Örneklem dışı beklenti 0'ın üstünde" bayrağı geçmez.
- Yüksek yüzdelik bir üstünlük değildir. Aynı stop ve hedef şekliyle rastgele girişler bu evrende daha çok kaybeder; strateji daha az kaybeder ama yine kaybeder.
- `prz_derin` son seçimle 2021-2025'te 33 dolum ve 31.52 R verir, ama her pencerede seçilen parametreler sonraki pencerede kaybeder. Bu aşırı uyumdur.
- Kapısız çekirdek kural bütün BIST'te üstünlük göstermez (işlem başına 0.013 R, yüzdelik 23.0).
- Kayıp yaygındır: 127-304 sembol, en kötü işlem −3.6 R; en kötü yıllar 2023 ve 2024.

Karar: PRZ girişi koda eklenmedi. Tansu'nun yazılı kurallarıyla Gartley, BIST günlük verisinde 2021-2025'te pozitif beklenti vermez. `gartley` durumu `yetersiz-ornek` kalır.

Ölçüm düzeneği denetimi: aynı düzenek BIST 30 sembolleri ve üyelik günleriyle eski sayıları birebir verir (`prz_derin` 55 sinyal, 34 dolum, −7.21 R; örneklem dışı N 18, −3.93 R). Fark evrenden gelir.

Ölçüm sırasında bulunan iki eksik (bu kayıtta düzeltilmedi):

- `kaynak.IsYatirim._iste` kopan bağlantıyı (`ChunkedEncodingError`) yeniden denemez; ilk indirme bununla durdu.
- Motor, `veri._gunler`'in bozuk saydığı günde (fiyat 0 ya da tutarsız OHLC) limit emri AOF'den doldurur; AOF 0 ise giriş 0 olur ve `islem.sonuc` sıfıra böler. Geniş evrende 287 sembolde 8.311 bozuk gün var; BIST 30 üyelik günlerinde 2. Ölçümde bozuk gün eksik gün sayıldı.

### Neden analizi (28.10.2026)

Levent: "Bu kadar işlem sayısına eksi yazmak mantıksız ... normal değil." Aynı geçici evrende, yalnız 2021-2025, altı neden denetlendi. Üç ayrı bakış açısıyla salt okunur inceleme yapıldı.

- Motor hatası yok: dört işlem günlük fiyatla elle denetlendi; denetim koşusu −75.51 R'yi birebir verir.
- Kök neden geometridir. Kapı stop X ile yalnız giriş X'e çok yakınken geçer: giriş-stop arası ortanca %1.0, ATR %4.8. Stopların %52'si dolum günü olur; maliyet işlem başına ≈ 0.11 R alır.
- Kapı açıkken hiçbir varyant rastgele girişi geçmez: kapı D − X ile ölçülüp stop X − 2 ATR olunca 381 işlem, 0.006 R, yüzdelik 21.0; dönüş teyitli giriş −0.037 R; C'yi gecikmesiz bilen teşhis koşusu bile −0.086 R.
- Tek artı bölge: çekirdek kural (D 0,786, stop X ya da X − 2 ATR, hedefler AD'de), kapı kapalı, yalnız büyük formasyon (XA ≥ 5 ATR; Tansu'dan değil). Örneklem dışı 34 işlem, ortalama 0.623 R, yüzdelik 97.6, bootstrap p5 10.84. 6 ve 7,5 ATR de ≈ 0.62 R verir; 4 ATR 0.167 R, 3 ATR 0.028 R. 34 işlemin 5'i BIST 30 sembolü.
- Bu bölge ≈ 20 varyant denendikten sonra bulundu; ileri yürüme parametre seçimini korur, varyant aramasını korumaz. Dürüst sınav dokunulmamış 2026 saklı dönemidir; kullanımı Levent'in kararıdır. Kapı kapalı aday 28.10.2026 kapı kararıyla çelişir.

### Sağlam ayar (28.10.2026)

Levent: "Bu Gartley sağlam bir temele oturmadan, geçmiş verilerle desteklenmeden, doğru setup ayarlar bulunmadan bu iş bitmiş sayılmayacak." Kapı için Levent: Tansu 1,5'i kendisi uygulamıyorsa esnetilebilir. Eldeki veri: bütün BIST, 2020-2025 (2019 ısınma).

- Motor ve araç denetimi: sinyal gününden sonraki veri silinince 900 örnek sinyalin hiçbiri değişmez; 6 sembol 2020-2025 gün gün oynatılınca sonradan beliren ya da kaybolan sinyal yok. SPEC 5.1-5.5'ten, motor koduna bakılmadan yazılan bağımsız motor 1.386 işlemin 1.384'ünde birebir aynı sonucu verir; tek fark sınıfı, bekleyen emrin bittiği gün gelen sinyaldir (SPEC yazmaz; motor almaz, 5 işlem).
- Kapı: stop X ile hedef1 oranı her kurulumda 1,403'tür. 1,0-1,4 arası her eşik aynı sonucu verir; 1,5 ve üstü her kurulumu eler. Tansu'nun kendi kurulumları 1,30-1,42'dir.
- Ayar haritası (432 sabit nokta, kapı 1,4, yıl yıl): `sag_bar_10` pivotunun 9 noktasının 9'u da artıdadır (işlem başına 0.31-0.85 R; 2020-2022 ve 2023-2025 ayrı ayrı artı). Zigzag pivotları ≈ 0'dır. Büyüklük süzgeci `sag_bar` ile gerekmez. Tansu X'i son n günün en düşüğü olarak tanımlar; bu `sag_bar` pivotudur.
- İleri yürüme (ızgara: yalnız `sag_bar_10/15/20`, stop X, kapı 1,4; 2021-2025): bütün BIST'te örneklem dışı N 40, toplam 26.76 R, ortalama 0.669 R, kazanan %57, yüzdelik 98.5 (rastgele 0.209), bootstrap p5 11.66: üç bayrak geçer. Seçim: `sag_bar_10`, tolerans 0.05, geçerlilik 5. Aynı ızgara BIST 30'da N 2 verir. Ürün ızgarası (zigzag dahil) bütün BIST'te −0.172 R verir.
- 2026 saklı dönem (bilgi; Levent'in onayıyla, seçimden sonra): ilk aday 3 işlem, 2.54 R; son aday 4 işlem, 0.04 R. Dördüncü işlemde (−2.50 R) eksik bir günden sonra ATR 14 gün NaN kalır ve risk tabanı sessizce düşer; 2021-2025'in 40 işleminin hiçbirinde bu durum yok.
- Ölçümde bulunan üçüncü eksik: `gostergeler.atr_basit` tek eksik günden sonra 14 gün NaN verir; `islem` risk tabanını `max(risk, NaN)` ile alır ve tabanı kaybeder. Bütün BIST'te günlerin %3.6'sında ATR NaN'dır.

### Kapı 1,30-1,42 ve evren basamakları (28.10.2026)

Levent: "1,30-1,42 arasında deniyelim bir de evreni genişletelim sistematik şekilde". Ayar: yalnız `sag_bar` ızgarası, stop X, D 0,786; 2021-2025 ileri yürüme.

- Kapı 1,30, 1,35 ve 1,40 aynı sonucu verir (N 40, 0.669 R, yüzdelik 98.5); 1,41 ve 1,42 hiç sinyal vermez. Stop X ile oran her kurulumda 1,403'tür.
- Evren basamağı: her gün, önceki 60 işlem gününün ortanca TL hacmine göre sıra (geleceği görmez; ilk 30, BIST 30 ile 25-26 sembolde örtüşür).

| Evren | Örneklem dışı N | Ortalama |
|---|---|---|
| ilk 30 | 1 | −1.034 R |
| ilk 50 | 2 | 0.375 R |
| ilk 100 | 6 | −0.396 R |
| ilk 200 | 10 | 0.530 R |
| ilk 300 | 18 | 0.658 R |
| bütün BIST | 40 | 0.669 R (üç bayrak geçer) |

- Sabit nokta (`sag_bar_10`, 0.05, 5), 2020-2025, 42 işlemin sinyal günündeki likidite sırasına göre: 1-100 N 10, 0.728 R; 101-200 N 10, 0.237 R; 201-300 N 7, 1.755 R; 300 sonrası N 15, 0.914 R. Kazanç her basamakta artıdır; sığ hisselere yığılmaz. Formasyon seyrek olduğu için yalnız bütün BIST 30 işlem eşiğini geçer.

### Tansu'ya bağlı ayar düğmeleri ve Monte Carlo (28.10.2026)

Levent: "Gartley'nin setup'ını oturtmaya çalışıyoruz, ayarları ... tansu'dan kopmayarak". Her düğme bir Tansu metnine bağlıdır: D'nin PRZ içindeki yeri (0,786 / 0,80 / 0,82), stop (X; yazılı seçenek X − 2 ATR ve ara değerler; kapı D − X ile), ikinci hedef (AD 0,618 ya da KUYAS grafiğindeki C), stop biçimi (dokunuş / kapanış), pivot n (5-20 gün). Harita: 8 yapı × 54 nokta, 2020-2025. Seçim ileri yürüme ve Monte Carlo ile yapıldı (bütün BIST, kapı 1,40, 2021-2025; örneklem dışı 2023-2025; Monte Carlo 1.000 koşu, tohum 20261028).

| Varyant | N | Ortalama | Kazanan | Yüzdelik | Bootstrap p5 | Gerçek düşüş | Bayraklar |
|---|---|---|---|---|---|---|---|
| Stop X, pivot `sag_bar` 10/12/15/20 | 34 | 0.886 R | %65 | 99.4 | 16.29 R | 3.13 R | geçer |
| Stop ızgarada (X ... X − 2 ATR), kapı D − X | 32 | 0.791 R | %75 | 99.5 | 15.52 R | 2.05 R | geçer (son seçim X) |
| Stop kapanış | 41 | 0.619 R | %61 | 91.8 | 8.61 R | 8.29 R | yüzdelik geçmez |
| Stop X − 2 ATR, kapı D − X | 37 | 0.408 R | %73 | 84.0 | 5.65 R | 3.93 R | yüzdelik geçmez |
| Stop X − 2 ATR, ikinci hedef C | 37 | 0.411 R | %70 | 79.8 | 5.43 R | 3.93 R | yüzdelik geçmez |

- D 0,80 ve 0,82 (1,5 kapısıyla) haritada tabandan zayıftır. Pivot 5 ve 7 gün ≈ 0'dır.
- İlk satırın Monte Carlo'su: bootstrap toplam p5 16.29 R, bootstrap düşüş p95 5.79 R, karıştırma düşüş p95 5.15 R, batma (25 R) %0. `sag_bar` 10/15/20 ızgarasında gerçek düşüş 8.30 R, bootstrap p95'in (7.24 R) üstündeydi; kayıplar 2024'te kümelenir.
- Sonuç ayarı: X son n günün en düşüğü (`sag_bar`, n 10/12/15/20), AB 0,618, BC 0,382-0,886, CD 1,272-1,618 (tolerans 0,04-0,05), D 0,786'da alış limiti, 5 gün geçerli, stop X (dokunuş), hedefler AD'nin 0,382 ve 0,618'inde 50/50, kapı hedef1'e göre 1,40, evren bütün BIST.

## Karar: Gartley kapı 1,40 ve n günlük salınım pivotları (Ek B #13, 28.10.2026)

Levent: "Evet, işle" (bu ayarı koda işle; evren genişletmesi ayrı iş). Değişiklik: `rr_min` varsayılanı 1,5 → 1,4 (seçenek kapalı, 1,4, 1,5, 2); pivot ekseni `sag_bar_10/12/15/20` (zigzag çıktı); ızgarada stop yalnız X (X − 2 ATR `hesapla`'da kalır; ayar dosyası ızgara dışı değeri reddeder). Izgara 108 → 36 nokta. Varsayılan pivot 15 ve geçerlilik 10 kaldı: 12, 15 ve 20 günlük pivotlar Tansu'nun SOKE taramasını (X 10.20, A 21.20, D 12.554) birebir bulur, 10 bulmaz.

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q tests/test_gartley.py     (değişiklikten önce)
FAILED tests/test_gartley.py::test_rr_kapisi_hedef1_ile_olculur_varsayilan_1_4_gecirir_1_5_eler
1 failed, 4 passed in 0.18s
$ .venv\Scripts\python.exe -X utf8 -m pytest -q     (değişiklikten sonra)
227 passed in 19.60s
$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla gartley
gartley: 17 sinyal, 3 dolum, toplam 2.55 R
gartley: ızgara 36 nokta, puanlı 0; puanlı nokta yok, varsayılanlar
ileri yürüme: örneklem dışı N = 2, ortalama verim n/a (0/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 1
Monte Carlo: tohum 20261028, N = 2, rastgele giriş yüzdeliği n/a (N = 2)
rapor: rapor\gartley\sinama.html; durum: yetersiz-ornek
```

| `gartley` (BIST 30, görüntü 20261026-2108) | kapı 1,5, eski ızgara (önce) | kapı 1,4, `sag_bar` ızgarası (sonra) |
|---|---|---|
| 2021-2025 sinyal / dolum / toplam | 0 / 0 / 0.00 R | 17 / 3 / 2.55 R |
| örneklem dışı | N 0 | N 2 |
| durum | yetersiz-ornek | yetersiz-ornek |

BIST 30'da örnek yetmez; bütün BIST'te aynı ızgara üç bayrağı geçer (yukarıdaki tablo, ilk satır). Ürün evreni bütün BIST'e ayrı işte açılır.

Saklı dönem: son ayarlar (pivot 12'nin eklenmesi, ızgarada yalnız stop X) "Sağlam ayar" bölümündeki 2026 bakışlarından sonra seçildiği için 2026 saklı dönemi `gartley` için artık dokunulmamış bir sınav değildir; sonraki temiz sınav 30.09.2026 sonrasının yeni verisidir.

## Yeniden ölçüm: veri yolu düzeltmelerinden sonra Gartley (29.10.2026)

#207 üç düzeltmeyi birleştirdi: kopan bağlantıda yeniden deneme; bozuk gün eksik gün sayılır; ATR eksik günü atlar ve ATR'siz stoplu kurulum girmez. Yukarıdaki tablonun ilk satırı aynı ayarla yeniden ölçüldü: bütün BIST, görüntü 20261028-1723, 2021-2025 ileri yürüme (örneklem dışı 2023-2025), kapı 1,40, `sag_bar` 10/12/15/20 ızgarası, stop X, ürünün `gartley.hesapla`'sı; Monte Carlo 1.000 koşu, tohum 20261028. "Sonra" kodu `yeniden-kurulus` 96b5107'nin `tansu/` paketidir (ölçülen kopyayla dosya dosya aynı). 2026 saklı dönemine bakılmadı.

```
önce  (PR 204 kodu, eski veri yolu):         secim {'pivot': 'sag_bar_10', 'tolerans': 0.04, 'gecerlilik': 5, 'stop': 'X'}; 2021-2025 sinyal 235, dolum 35, toplam 27.83 R; ileri yurume N 34, toplam 30.12 R, ortalama 0.886 R, kazanan %65; yuzdelik 99.4 (rastgele ort 0.216); bootstrap p5 16.29; dusus p95 5.79, karistirma p95 5.15, gercek dusus 3.13, batma %0.0
sonra (96b5107 kodu, yeni veri yolu):       secim {'pivot': 'sag_bar_10', 'tolerans': 0.04, 'gecerlilik': 5, 'stop': 'X'}; 2021-2025 sinyal 235, dolum 35, toplam 27.83 R; ileri yurume N 34, toplam 30.12 R, ortalama 0.886 R, kazanan %65; yuzdelik 99.4 (rastgele ort 0.216); bootstrap p5 16.29; dusus p95 5.79, karistirma p95 5.15, gercek dusus 3.13, batma %0.0
```

| Bütün BIST, kapı 1,40 | Önce | Sonra |
|---|---|---|
| Örneklem dışı N | 34 | 34 |
| Ortalama | 0.886 R | 0.886 R |
| Rastgele giriş yüzdeliği | 99.4 | 99.4 |
| Bootstrap toplam p5 | 16.29 R | 16.29 R |
| Gerçek düşüş / bootstrap düşüş p95 | 3.13 / 5.79 R | 3.13 / 5.79 R |

34 örneklem dışı işlem sütun sütun aynıdır. Hiçbir sayı değişmedi; nedenleri:

- Yeniden deneme yalnız indirmeyi etkiler; iki ölçüm aynı görüntüyü okur.
- Bozuk gün: önceki ölçüm bozuk günü zaten eksik gün saymıştı. Yeni veri yolu aynı günleri eksik sayar; tek ek gün GWIND 10.10.2025'tir ve bir Gartley işlemine girmez.
- ATR: fiyatı olan ama ATR'si olmayan gün 29.465'ten 8.032'ye iner; 687 günün ATR değeri değişir. 34 işlemin hiçbirinde sinyal günü ATR'si eksik değildi ya da değişmedi. Risk tabanı (0,5 ATR) hiçbir işlemde bağlamaz: D − X en az 0,96 ATR'dir.

PR 204 tablosundaki geçici varyant kopyası 2021-2025'te 233 sinyal saydı; ürünün `hesapla`'sı iki ölçümde de 235 sayar. Dolum ve işlemler aynıdır.
