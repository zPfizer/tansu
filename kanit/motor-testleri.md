# Motor testleri: varsayılan bekçisi, bağımsız referanslar, gelecek verisi kontrolü

Tarih: 30.10.2026. Dal: `retro-motor-testleri` (taban `origin/yeniden-kurulus` 112bb4a).

## Neden

28.10'da Gartley varsayılanı (rr_min 1.5) 13.068 sinyalden 0 kurulum verdi; dört test dosyası düzeltilerek geçirildi ve sıfır kurulumu kimse görmedi. Motor riskini bulan denetimler yalnız `%TEMP%` altındaydı. Bu çalışma onları tohumlu, sentetik testlere taşır. `tansu/` değişmedi.

## Yapılanlar

- `tests/sentetik.py`: `SABIT` (her stratejinin `varsayilan` anahtarlarıyla sabit test parametreleri), `YOLLAR`, `rastgele_tablo` (kuruşa yuvarlı yürüyüş, fiyatsız günler, tavan ve taban kilidi; `veri` yükleyicisi kilitleri aynı görür), `gartley_tekrar`, `anlik` (gün tablolarından `veri.Anlik`).
- `tests/test_varsayilan.py`: varsayılanlara bakan tek test. Varsayılan okuyan testler artık `SABIT` okur (test_gartley, test_gelecek_kesim, test_sina, test_altin_gartley, test_motor_yuzeyi).
- `tests/test_referans_motor.py`: SPEC 5.1-5.4'ten yazılmış dolum ve çıkış referansı (günleri bir kez yürüyen durum makinesi) ile `islem.simule`, bağımsız Gartley bulucusu ile `gartley.STRATEJI.sinyal`, kaba kuvvet pivot taraması ile `yapi.sag_bar_pivotlari`, 2^k fiyat ölçeği.
- `tests/test_gelecek_kesim.py` (eski `test_gelecek.py`, `git mv`): strateji düzeyinde kesme ve ürün yükleyicisinden geçen kesme ve çöp kontrolü.
- `kurulum/esdeger.py`: iki kod kökünün `sina` ve `ayarla` çıktısını 15 senaryoda karşılaştırmak için eşdeğerlik ağı.

## Kırmızı ve yeşil kanıt

Her ekim çalışma kopyasında yapıldı, koşuldu, sonra `git checkout -- <dosya>` ile geri alındı.

### a. Varsayılan bekçisi

Taban 112bb4a, değişiklikten önce, `rr_min` 1.4 -> 1.5:

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q -p no:cacheprovider
FAILED tests/test_gartley.py::test_rr_kapisi_hedef1_ile_olculur_varsayilan_1_4_gecirir_1_5_eler
FAILED tests/test_gelecek.py::test_t_gunu_ciktisi_sonraki_gunlerden_bagimsiz[gartley]
2 failed, 366 passed, 1 skipped, 2 warnings in 27.57s
```

Değişiklikten sonra, aynı ekim; yalnız bekçi kırılır:

```
E       AssertionError: gartley: varsayılan parametreler altın yolda sıfır kurulum veriyor (0 sinyal, 0 dolum); varsayılan {'pivot': 'sag_bar_15', 'tolerans': 0.05, 'gecerlilik': 10, 'stop': 'X', 'rr_min': 1.5}
FAILED tests/test_varsayilan.py::test_varsayilan_parametreler_altin_yolda_dolan_kurulum_verir[gartley]
1 failed, 369 passed, 1 skipped, 2 warnings in 31.06s
```

Değişiklikten sonra, `pivot` sag_bar_15 -> sag_bar_10 (kurulum veren varsayılan değişikliği hiçbir testi düzeltmeye zorlamaz):

```
370 passed, 1 skipped, 2 warnings in 31.62s
```

### b. Bağımsız referanslar

Gerçek kod:

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q -p no:cacheprovider tests/test_referans_motor.py
16 passed in 7.90s
```

`yapi.sag_bar_pivotlari`: tepe pivot günü bir bar kaydırıldı (`fiyatli[i]` -> `fiyatli[i - 1]`):

```
FAILED tests/test_referans_motor.py::test_sag_bar_pivotlari_kaba_kuvvet_pencere_taramasiyla_ayni[3]
FAILED tests/test_referans_motor.py::test_sag_bar_pivotlari_kaba_kuvvet_pencere_taramasiyla_ayni[5]
FAILED tests/test_referans_motor.py::test_sag_bar_pivotlari_kaba_kuvvet_pencere_taramasiyla_ayni[15]
FAILED tests/test_referans_motor.py::test_gartley_bagimsiz_bulucuyla_ayni_gun_ve_seviyeleri_verir[sag_bar_3-kapali-X-20-yollar0]
...
8 failed, 8 passed in 5.23s
```

`gartley.py`: `yapi.bacak_uclari` kapatıldı (`if False and not yapi.bacak_uclari(...)`):

```
E           AssertionError: tohum 106
E           AssertionError: tohum 111
FAILED tests/test_referans_motor.py::test_gartley_bagimsiz_bulucuyla_ayni_gun_ve_seviyeleri_verir[sag_bar_3-kapali-X-20-yollar0]
...
5 failed, 11 passed in 6.19s
```

`islem.py`: limit dokunuşu `g.dus[i] <= seviye` -> `g.dus[i] < seviye`:

```
E               AssertionError: dokunus, iki yarım hedef, tohum 0
FAILED tests/test_referans_motor.py::test_motor_bagimsiz_dolum_referansiyla_ayni_islemleri_ve_red_sayilarini_verir
1 failed, 15 passed in 5.27s
```

`islem.py`: taban kilidi gününde bekleyen çıkış silindi (`e.bekleyen = "stop" if dokundu else nedeni` satırı):

```
E               AssertionError: dokunus, iki yarım hedef, tohum 2
FAILED tests/test_referans_motor.py::test_motor_bagimsiz_dolum_referansiyla_ayni_islemleri_ve_red_sayilarini_verir
1 failed, 15 passed in 5.22s
```

### c. Gelecek verisi kontrolü

Gerçek kod:

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q -p no:cacheprovider tests/test_gelecek_kesim.py
4 passed in 9.82s
```

`ortalama_kesisim.py`: ortalamalar bir gün ileriye bakar (`.shift(-1)`):

```
E           AssertionError: DataFrame.iloc[:, 0] (column name="giris") are different
E               AssertionError: ortalama-kesisim: 2022-12-02 sonrası silme geçmişi değiştirdi
FAILED tests/test_gelecek_kesim.py::test_t_gunu_ciktisi_sonraki_gunlerden_bagimsiz[ortalama-kesisim]
FAILED tests/test_gelecek_kesim.py::test_yukleyiciden_kesilen_ya_da_bozulan_gelecek_gecmis_olaylari_degistirmez[ortalama-kesisim]
2 failed, 2 passed in 6.72s
```

`islem.py`: limit dolumu ertesi günün dibine bakar (`g.dus[min(i + 1, len(g.dus) - 1)] <= seviye`). Strateji düzeyindeki eski test bunu göremez; yükleyiciden geçen test görür:

```
E               AssertionError: gartley: 2021-05-21 sonrası silme geçmişi değiştirdi
FAILED tests/test_gelecek_kesim.py::test_yukleyiciden_kesilen_ya_da_bozulan_gelecek_gecmis_olaylari_degistirmez[gartley]
1 failed, 3 passed in 5.38s
```

### d. Eşdeğerlik ağı

```
$ .venv\Scripts\python.exe -X utf8 kurulum/esdeger.py --deneme
tamam: 15 senaryo -> C:\Users\levent\AppData\Local\Temp\esdeger-deneme-w7cuvys0\1
tamam: 15 senaryo -> C:\Users\levent\AppData\Local\Temp\esdeger-deneme-w7cuvys0\2
deneme: iki koşu aynı (74 dosya)
```

Süre 52 s.

## Bütün takım

```
Önce (112bb4a):  368 passed, 1 skipped, 2 warnings in 27.39s
Sonra:           388 passed, 1 skipped, 2 warnings in 53.43s
$ .venv\Scripts\python.exe -X utf8 -m ruff check tansu tests kurulum
All checks passed!
$ .venv\Scripts\python.exe -X utf8 -m ruff format --check tansu tests kurulum
47 files already formatted
```

Atlanan: `test_altin_gartley` (bu çalışma kopyasında yerel veri yok). En yavaş yeni testler: `test_gelecek_kesim` gartley 5.6 s, ortalama-kesisim 4.6 s; `test_referans_motor` toplam yaklaşık 8 s.

## Gözlemler

- Ürün SPEC'ten ayrılmadı: dolum referansı 12 tohum x 3 çıkış biçiminde, Gartley referansı 20 yürüyüş x 8 parametre setinde ürünle aynı.
- `dolumdan önce stop altında kapanış` limit emrinde oluşamaz: stop seviyenin altındadır, kilitsiz günde stopun altındaki kapanış emri önce doldurur. Kapsam iddiası bu nedeni istemez.
- `sag_bar` pivotlarında aynı gün tekrarı (`tekrar`) oluşmaz: her onay gününde en çok bir tepe onaylanır. Referans kuralı taşır; sayı sıfırda eşittir.
- Stop X iken hedef1 oranı her kurulumda yaklaşık 1.403'tür; rr_min 1.4 hiçbir kurulumu elemez. Kapı yalnız X-2ATR ile kurulum eler; testin o seti kapı reddini ister.
