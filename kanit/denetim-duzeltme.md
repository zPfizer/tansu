# Denetim 31.10.2026 düzeltmeleri

Tarih: 01.11.2026. Dal: `claude/denetim-duzeltmeleri-66a71f` → `yeniden-kurulus`. Kararlar: Levent yetkisiyle beyin
kararı, `kanit/acik-sorular.md` "Verilen kararlar" 1-7. Bulgular ve durumları: aynı dosyada "Denetim 31.10.2026
kayıtları". Çıktı dosyaları `%TEMP%\tansu-denetim-duzelt\` altındadır (Git'te değil).

## Yapılanlar

| Madde | Değişiklik | Test |
|---|---|---|
| T-1 (a) | `gartley` ve `ortalama-kesisim` `20261028-2353` görüntüsünde yeniden ayarlandı. | `test_ayar_dosyalarinin_veri_goruntusu_veri_kokunde_var` (gerçek veri; CI'da atlanır) |
| T-1 (b) | `tansu yedekle <hedef>`: `veri.yedekle`, `veri.denetle`. | `tests/test_yedekle.py` (5 test), `test_yardim_alti_komutu_listeler` |
| T-1 (c) | `goruntuleri_buda` ayarların andığı görüntüleri tutar, `ag/_gecici-*` klasörlerini siler. | `test_veri_budamasi_ayarin_goruntusunu_korur_yarim_gecicileri_siler` |
| T-2 | `rapor.yaz` metinleri bellekte hazırlar, hedefleri önce dener, `dosya.atomik` ile yazar. | `test_rapor_dosyasi_yazilamiyorsa_eski_rapor_karisik_kalmaz` |
| T-3 | `ayar.oku(gerekli=...)`, `Strateji.secenek`, `rr_min` yalnız kapalı, 1,4, 1,5, 2. | `test_ayarli_stratejinin_ayar_dosyasi_yoksa_varsayilanla_sinamaz` (3 durum), `test_oku_secenek_disi_el_degerini_reddeder` (3), `test_oku_izgara_ekseninde_bool_degeri_reddeder`, `test_her_varsayilan_anahtarin_izinli_deger_kumesi_var` (2), `test_sina_secenek_disi_ayar_degerini_reddeder` |
| T-4 | Havuz işçisi ebeveynini bekleyen bir iş parçacığıyla kendini kapatır (`ayar._hazirla`). | `test_ebeveyn_zorla_kapaninca_havuz_iscisi_de_kapanir` (yavaş) |
| T-5 | Eksik `durum.csv`, bozuk başlık ve eksik `manifest.json` tek satırlık `VeriHatasi` verir. | `test_durum_dosyasi_yoksa_tek_satir_hata`, `test_durum_dosyasi_basligi_bozuksa_tek_satir_hata`, `test_goruntunun_manifesti_yoksa_tek_satir_hata` |
| T-6 | Her koşu `kayit/tansu.log`'a bir satır ekler (Git'te değil). | `test_her_kosu_kayda_bir_satir_ekler`, `test_basarisiz_kosu_kayda_ilk_hata_satirini_yazar` |
| T-7 | Kullanılmayan `gostergeler.deger_kaydi` silindi; `onayla`, `tara`, `durum` belgede "henüz yapılmadı". | ruff, tam pytest |
| T-8 | `README.md`, `AGENTS.md`, `docs/veri-envanteri.md` koda göre düzeltildi. | belge |
| Ek 7 | `dosya.atomik` her çağrıda benzersiz geçici ad kullanır. | `test_atomik_es_zamanli_yazanlar_ayri_gecici_dosya_kullanir` |

Değişen var olan test: `test_ayarla_puanli_secimle_ayarlandi_yapar_sinyaldeyse_onay_ister` sahte stratejiye `secenek`
ekler, çünkü yeni denetim ızgara dışı iki anahtarını reddeder. `tests/test_kaynak.py` veri kökü olarak `tmp_path/veri`
kullanır.

## Kırmızı ve yeşil

Yeni testler önce yazıldı (commit `d2598bf`), düzeltmeden önceki kodda koşuldu (`96f79bc`):

```
$ <py> -X utf8 -m pytest <yeni testler> -p no:cacheprovider -q        (96f79bc kodu)
17 failed, 3 passed, 26 deselected in 13.80s
11 failed in 0.93s
```

Geçen 3 test `test_oku_secenekteki_el_degerini_kabul_eder[kapali,1.4,2]`'dir: izinli değerin reddedilmediğini
denetler, bu yüzden iki kodda da geçer. Düzeltmeden sonra (`4f3ce7e`) aynı küme:

```
1 failed, 35 passed in 7.97s
FAILED tests/test_ayar.py::test_ayar_dosyalarinin_veri_goruntusu_veri_kokunde_var
AssertionError: gartley.json: 20261028-1723 yok
```

Bu tek hata T-1 (a)'dır: yeniden ayardan sonra geçer (aşağıdaki tam koşu).

## T-1 (a) yeniden ayar

Komut çalışma ağacının kökünden, `TANSU-veri` yalnız okunarak koşuldu. Kod `cb28563` (temiz `tansu/`).

```
$ <py> -X utf8 -m tansu ayarla gartley
gartley: 224 sinyal, 36 dolum, toplam 29.38 R
gartley: ızgara 36 nokta, puanlı 15; seçim pivot=sag_bar_10 tolerans=0.04 gecerlilik=5 stop=X (sağlam 0.86 R, N = 35)
ileri yürüme: örneklem dışı N = 41, ortalama verim 1.73 (5/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 4
Monte Carlo: tohum 20261028, N = 41, rastgele giriş yüzdeliği 98.4
Veri kapısı: temiz. Karantina oranı 0.01% (eşik 1%), olay denetimi farkı oranı 0.23% (eşik 2%); 04.01.2021 ve sonrası 762231 hisse-gün. Eksik gün olarak işlenen kaynak günü hatası: 2026-05-21.
ayar: stratejiler\ayarlar\gartley.json
rapor: rapor\gartley\sinama.html; durum: ayarlandi
rc=0 sure_sn=59
```

```
$ <py> -X utf8 -m tansu ayarla ortalama-kesisim
ortalama-kesisim: 1160 sinyal, 1143 dolum, toplam 153170.65 %
ortalama-kesisim: ızgara 54 nokta, puanlı 54; seçim ortalama=EMA cift=48/247 teyit_gun=2 (sağlam 81.23 %, N = 879)
ileri yürüme: örneklem dışı N = 1881, ortalama verim 2.67 (6/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 218
Monte Carlo: tohum 20261028, N = 1881, rastgele giriş yüzdeliği 84.2
Veri kapısı: temiz. Karantina oranı 0.01% (eşik 1%), olay denetimi farkı oranı 0.23% (eşik 2%); 04.01.2021 ve sonrası 762231 hisse-gün. Eksik gün olarak işlenen kaynak günü hatası: 2026-05-21.
ayar: stratejiler\ayarlar\ortalama-kesisim.json
rapor: rapor\ortalama-kesisim\sinama.html; durum: ayarlandi
rc=0 sure_sn=314
```

İki strateji de `ayarlandi` durumundan geldi; `durum.yeniden_onay` yeni onay istemedi (çıktıda "yeniden onaylamalı"
satırı yok). İki strateji de aynı parametreleri seçti.

| | `gartley` önce | `gartley` sonra | `ortalama-kesisim` önce | `ortalama-kesisim` sonra |
|---|---|---|---|---|
| Görüntü | 20261028-1723 | 20261028-2353 | 20261028-1723 | 20261028-2353 |
| Sinyal / dolum, 2021-2025 | 235 / 35 | 224 / 36 | 1155 / 1081 | 1160 / 1143 |
| Toplam | 27.83 R | 29.38 R | 141259.37 % | 153170.65 % |
| Sağlam puan (N) | 0.84 R (34) | 0.86 R (35) | 76.63 % (829) | 81.23 % (879) |
| Örneklem dışı N, toplam | 34, 30.12 R | 41, 28.72 R | 1672, 75407.71 % | 1881, 82393.38 % |
| Rastgele giriş yüzdeliği | 99.4 | 98.4 | 82.8 | 84.2 |

"Önce" sütunları Git'teki eski `rapor/*/ozet.md`'den, "sonra" sütunları yeni `ozet.md`'den ve yukarıdaki çıktıdan.
`gartley`'in üç bayrağı yine geçer (örneklem dışı beklenti 0.70 R, yüzdelik 98.4, bootstrap p5 13.15 R).

## T-4 elle zorla kapatma

`olc.ps1` (denetimin ölçüm betiği) `ayarla gartley`'i `git archive` kopyasında, veri kopyasıyla başlatır, 25 sn sonra
ana süreci zorla kapatır ve 3 sn sonra kalan süreçleri sayar.

```
96f79bc:  rc=-1  sure_sn=25.5  tepe_surec_sayisi=7  cikistan_3sn_sonra_kalan_surec=4
cb28563:  rc=-1  sure_sn=25.6  tepe_surec_sayisi=8  cikistan_3sn_sonra_kalan_surec=0
```

Eski kodun 4 işçisi ebeveyn öldükten 6 dakika sonra hâlâ çalışıyordu; elle kapatıldı. Yeni kodda zorla kapatma anında
başlamakta olan bir işçi Python'un `pickle data was truncated` dökümünü yazar; bu, komutun hata satırı değil, zorla
kapatılan sürecin kendi çıktısıdır.

## Elle hata yolları (kod `cb28563`, geçici kopya)

```
$ TANSU_VERI=<manifestsiz kopya> <py> -X utf8 -m tansu sina gartley
tansu sina: manifest yok: 20261028-2353; görüntüyü yedekten geri yükle (`tansu yedekle <veri kökü> --kok <yedek>`, docs/veri-envanteri.md) ya da `tansu veri` çalıştır
rc=1

$ <py> -X utf8 -m tansu sina gartley        (gartley.json yok, durum ayarlandi)
tansu sina: ayar dosyası yok: <kopya>\stratejiler\ayarlar\gartley.json; dosyayı Git'ten geri al ya da `tansu ayarla gartley` çalıştır
rc=1

$ <py> -X utf8 -m tansu yedekle <geçici hedef> --kok <veri kopyası>     (iki kez)
tansu yedekle: 20261028-1723: kaynak görüntü yok: <veri kopyası>\ag\20261028-1723
20261028-2353: kopyalandı (<geçici hedef>\ag\20261028-2353)
rc=1
tansu yedekle: 20261028-1723: kaynak görüntü yok: <veri kopyası>\ag\20261028-1723
20261028-2353: yedekte aynı (<geçici hedef>\ag\20261028-2353)
rc=1
```

Kopyanın `ortalama-kesisim.json`'ı eski `20261028-1723`'ü andığı için ilk satır hata verir; komut öteki görüntüye
devam eder ve 1 koduyla çıkar. `kayit/tansu.log` iki `sina` satırını `rc=1` ve ilk hata satırıyla yazdı. Gerçek bir
yedek hedefine koşulmadı (yer Levent'in kararı).

## Tam koşu

Yeniden ayardan sonra, çalışma ağacının kökünde:

```
$ <py> -X utf8 -m pytest -p no:cacheprovider -q
506 passed, 1 skipped, 2 warnings in 57.02s
$ <py> -X utf8 -m pytest -p no:cacheprovider -q -rs tests/test_ayar.py -k "veri_goruntusu_veri_kokunde or ebeveyn"
2 passed, 25 deselected in 2.69s
$ <py> -m ruff check --no-cache tansu tests kurulum
All checks passed!
$ <py> -m ruff format --check --no-cache tansu tests kurulum
58 files already formatted
```

Atlanan tek test `tests/test_altin_gartley.py:19` "yerel altın olgu veya veri yok": altın olgular yalnız
`yeniden-kurulus` ağacındadır. Yavaş test sayısı 16 (`README.md`).

## Yapılmayanlar

- Yerel `docs/SPEC.md` (3.8, satır 167, bölüm 7) bu ağaçtan yazılamadı; yama hazır, `yeniden-kurulus` ağacında
  uygulanacak (`kanit/acik-sorular.md` "Yerel SPEC yaması").
- `tansu yedekle` gerçek bir yedek hedefine koşulmadı; yer Levent'in kararı ("Levent kararı bekleyenler" 2).
