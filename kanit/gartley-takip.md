# Gartley ileri takip: dondurulmuş ayar, 01.10.2026'dan beri (30.10.2026)

Dal: `gartley-takip` → `yeniden-kurulus`. Ürün kodu (`tansu/`) ve `kanit/gartley-para/` değişmedi. Betik ve kayıtlar
`kanit/gartley-takip/` altındadır.

Amaç: `kanit/gartley-para.md` işinde dondurulan Gartley para ayarını geçmişte değil, **taze veride ileri** koşturmak.
Başlangıç 01.10.2026, sermaye 100.000 TL, kasa boş başlar (01.10.2026'dan önce tarihli sinyal sayılmaz). Bu bir kâğıt
üstü takiptir; emir verilmez, para yatırılmaz.

## Dondurulmuş dosyalar

| Dosya | SHA-256 |
|---|---|
| `kanit/gartley-para/ayar.json` | `118ad754930a67cb70f4ace06de0981142e1a5539dcdfe15ca6e2eb0d43e32e6` |
| `kanit/gartley-para/para.py` | `95dfd8a9774e61a4be56087b3d106b7de56483c81ae67fb4a0e9dc51a130dd83` |

Betik her koşuda iki özeti denetler; uyuşmazsa hiçbir şey indirmeden ya da yazmadan durur. Para katmanı `para.py`'den
yola göre içe alınır (`kos`, `gunluk_faiz`, `xu100`); `test` kipi kullanılmaz.

**Kural: ayar değişmez.** Bu takipte ayar, kod ya da maliyet varsayımı değişirse yeni bir iş açılır; bu klasördeki
kayıtlar o işe taşınmaz. Sonuç iyi ya da kötü olsa da ayara dokunulmaz.

## Güncelleme komutu

Depo kökünden, ana sanal ortamla:

```
C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe -X utf8 kanit/gartley-takip/takip.py [veri-klasörü]
```

Varsayılan veri klasörü `C:\Users\levent\Desktop\TANSU\veri\takip-gartley` (Git dışı). Komut sırayla:

1. Bütün BIST kodlarını (bugünkü liste + 2024'ten beri kapananlar) 2024-01-01'den bugüne artımlı indirir
   (`kaynak.Artimli`; 2024 yalnız ısınma). Politika faizini projenin kaynağından (`kaynak.Borsapy().faiz()`) alır.
   İlk koşu yaklaşık 1,5 saat sürdü (812 kodun tam inişi). Günlük güncelleme yaklaşık 40 dakika sürer (ölçülen: 633
   artımlı, 179 tam; kaynakta boş olan 179 kod her koşuda yeniden tam istenir).
2. Son tam işlem gününü seçer: seans sonrası (19:00) alınmış ve satır sayısı bir önceki günün en az %90'ı olan son gün.
3. Dondurulmuş ayarı 01.10.2026 - son gün arası koşturur (veri 2025'te kesilmez).
4. `kanit/gartley-takip/kayit/<son gün YYYYMMDD>/` klasörünü **yeni** yazar. Klasör varsa mesajla durur (çıkış kodu 1);
   üstüne yazmaz. Bu denetim indirmeden önce tek bir kaynak isteğiyle (THYAO, son 10 gün) yapılır, reddedilen koşu
   yaklaşık 2 saniye sürer; indirmeden sonra aynı denetim tekrarlanır. Aynı gün ikinci koşu bu yüzden reddedilir; yeni
   kayıt için yeni bir işlem günü gerekir.

Seçenekler: `--mevcut` (indirme yok, klasördeki son anlık görüntü), `--cikti <klasör>` (kayıt kökü).

## Kayıt nasıl okunur

Her klasör bağımsız ve baştan hesaplanmıştır: kasa 01.10.2026'da 100.000 TL ile başlar, o günün verisiyle sonuna kadar
koşar. Eski klasörler değişmez; yeni klasör eskisinin devamı değil, yeni verinin tam hesabıdır (kaynak geçmiş fiyatı
düzeltirse eski klasörle yeni klasör arasında fark çıkabilir).

- `ozet.json`: son gün, özkaynak, faiz geliri, işlem kârı, en iyi üç işlem hariç işlem kârı, yalnız nakit özkaynağı
  (aynı %15 kesintili faiz), en kötü düşüş, sayılar, kıyaslar (BIST 100 al-tut, brüt faiz) ve sürüm bilgisi: ayar ve
  `para.py` SHA-256, `tansu` commit'i, veri anlık görüntü kimliği ve fiyat dosyasının SHA-256'sı, kaynağın atladığı
  günler.
- `sinyaller.csv`: motorun 01.10.2026'dan beri verdiği her sinyal (sembol, sinyal günü, emir fiyatı D, stop). `motor_durumu`:
  `doldu`, `bekliyor` (emir son günde hâlâ geçerli) ya da `düştü: <neden>`. `kasa_durumu`: dolan emir için `alındı`
  ya da `atlandı: <neden>`.
- `islemler.csv`: dolan her emir; dolum, çıkış, adet, R ve `kar_tl` (komisyon ve kayma dahil; açık pozisyon son
  kapanışla ve satış maliyetiyle değerlenir).
- `acik.csv`: son günde açık pozisyonlar (son kapanış, yarın için iz süren stop, piyasa değeri, değerleme kârı).
- `gunluk-kasa.csv`: günlük özkaynak, nakit, pozisyon değeri, açık pozisyon sayısı.

Sabit kurallar (komisyon %0,1575, kayma 1 fiyat adımı, likidite sınırı, nakde %15 kesintili faiz, adet kuralı) ve
anlamları `kanit/gartley-para.md` "Sabit kurallar" bölümündedir; burada tekrarlanmaz.

## İlk kayıt: `kayit/20261028` (son gün 28.10.2026)

29.10.2026 resmî tatildir; 30.10.2026 koşu saati seans öncesidir. Bu yüzden son tam işlem günü 28.10.2026'dır.
Veri anlık görüntüsü `20261030-0106`, `tansu` commit'i `29f06d7`.

| 100.000 TL, 01.10.2026 - 28.10.2026 | Sonuç |
|---|---|
| Özkaynak | **102.428 TL** (%2,43) |
| Faiz geliri | 2.428 TL |
| İşlem kârı | 0 TL |
| En iyi üç işlem hariç işlem kârı | 0 TL |
| Yalnız nakit (%15 kesintili faiz) | 102.428 TL |
| Sinyal / alınan işlem / açık pozisyon | 0 / 0 / 0 |
| Kıyas: BIST 100 al-tut / brüt faiz | 93.457 TL / 102.862 TL |

Bir ay içinde motor sinyal vermedi; kasanın tamamı nakitte kaldı ve yalnız faiz kazandı. Bu beklenen bir durumdur
(2015-2022'de 8 yılda 50 işlem; son sinyal bu veride 26.08.2026). Takip anlamlı sonuç vermek için aylar gerektirir.

Kayıt kapsam notları:

- Kaynak 21.05.2026 gününü hiçbir sembol için vermemiş (kaynak günü hatası); bu gün eksik gün sayılır.
- Kaynak CITAS için 18, 19 ve 20.08.2026'yı vermedi; indirici bu üç günü atladı (veri klasöründeki
  `atlanan-gunler.json`, birikimli; `ozet.json` da listeler).
- 179 kod kaynakta boş, 0 kod inmedi.
- Politika faizi serisi 23.01.2026 (%37) ile 23.10.2026 (%36) arasında değişim göstermiyor; bu proje kaynağının
  (`kaynak.Borsapy`) verdiği seridir, TCMB sayfasıyla yalnız son değer (%36, 23.10.2026) karşılaştırıldı.

## Sınırlar

- Bu betik para katmanını değiştirmez; `kanit/gartley-para.md` "Sınırlar" bölümü aynen geçerlidir (aşırı uyum, faiz
  kesintisi varsayımı, T+2 ve emir kuyruğunun modellenmemesi).
- Isınma verisi 2024'ten başlar; 2015-2022 ayarının veri başlangıcı 2014'tür. Pivot (12 bar) ve emir süresi (20 gün)
  için 2024 başı yeter; karantina penceresi (250 gün) 2024 başından kurulur.
- Veri ve önbellek Git dışıdır (`veri/`); her koşu yeni bir anlık görüntü ekler (yaklaşık 28 MB). Eski görüntüleri
  silmek ayrı onay ister.

## İleri izleme: Gartley ve S3, düzeltilmiş motor (30.10.2026)

Karar (Levent, 30.10.2026, "Hepsine evet"): ileri izlemede dondurulmuş Gartley ve S3 birlikte izlenir; günlük
güncelleme otomatik çalışır. Kod denetimi (`kanit/gartley-denetim.md`) motoru ve deneme betiklerini düzeltti; 2010-2014
son sınavı koşmadı, kalan yol yalnız ileri izlemedir. Motor değiştiği için bu, yukarıdaki takibin devamı değil yeni bir
iştir ("Kural: ayar değişmez"): `kayit/` klasörü ve `takip.py` olduğu gibi kalır; yeni kayıtlar `izleme/` altındadır.

### Dondurulan kural seti

`izleme/dondurma.json` (bu bölümle aynı commit'te, ilk izleme kaydından önce gönderildi). `izle.py` her koşuda
denetler; biri uyuşmazsa hiçbir şey indirmeden durur.

- Adaylar: dondurulmuş Gartley (`kanit/gartley-para/ayar.json`, SHA-256 `118ad754…`) ve S3 (Seo X3, `pdf.py`
  `3e8f2dc6…`). İkisi de denetimin düzeltme koşusundaki yolla koşar: Gartley `yontem.kos`, S3 `pdf.kos`, para katmanı
  `yontem.para_katmani` (100.000 TL, aynı maliyet ve boyut kuralları).
- Betik düzeltmeleri: `D1t,T3,E2,S1s,S2s` (`kanit/gartley-denetim/duzeltme.py`, `be43cc0c…`), düzeltme koşusundaki
  gibi. İleri izlemede sonucu `D1t` (S3 bacak ucu) ve `E2` (açılış stopu, iki aday) değiştirir; `T3`, `S1s`, `S2s`
  bu iki adayda etkisizdir.
- Motor: `yeniden-kurulus` 86cd0c2, `tansu/` ağacı `3c15259d…` (PR 250 ve 253-260). Her kayıt `tansu` commit'ini ve
  ağacını yazar. İzinli ağaç listesi `dondurma.json`'dadır; yeni bir ağaç yalnız kayıtlı bir değişiklikle eklenir.
- Evren: veri klasöründeki bütün BIST payları (motorun `uye` sütunu hepsinde doğru); veri 2024-01-01'den, ısınma.

### Başlangıç günü

İki aday da **01.10.2026**'da başlar, kasa 100.000 TL ile boş başlar.

S3 kuralı: S3 için 01.01.2023 sonrasına ait hiçbir sonuç hesaplanmadıysa ve görülmediyse başlangıç 01.10.2026'dır;
görüldüyse dondurma günüdür. Kontrol (30.10.2026):

- `pdf.py` dönemi kodda 2015-01-01 - 2022-12-31'dir (`yontem.DONEM`); veri bu günde kesilir.
- Depodaki bütün S3 çıktıları (`gartley-yontem/sinav-pdf/`, `gartley-yontem/yahoo/`) ve geçici klasördeki bütün S3
  çıktıları (PDF ailesi, prova, Yahoo, denetim paneli ve düzeltme koşusu) 2022-12-30'da biter.
- Bu projenin 151 oturum kaydında S3 ile birlikte 2023, 2024 ya da 2025 geçen satırların hiçbiri bir S3 sonucu değildir
  (yalnız veri dosyasının adı ve Gartley'in 2023-2025 sınavı).
- Önceki takip (`kayit/20261028`) yalnız Gartley'i koştu.

Sonuç: S3 sonucu 01.01.2023 sonrası için hiç hesaplanmadı; S3 01.10.2026'da başlar.

### Komut

Depo kökünden, ana sanal ortamla: `python -X utf8 kanit/gartley-takip/izle.py`. Seçenekler: `--mevcut` (indirme yok),
`--zamanli` (zamanlanmış görev kipi), `--cikti <klasör>` (deneme kaydı başka yere). Veri `takip.py`'nin yardımcılarıyla
güncellenir (aynı veri klasörü, ana deponun `veri/takip-gartley`'i, Git dışı).

Her koşu iki adayı başlangıç gününden son tam işlem gününe kadar baştan hesaplar ve `izleme/<son gün>-<motor ağacı>/`
klasörünü yeni yazar. Aynı gün ve aynı motorla kayıt varsa hiçbir şey yazmaz ve 0 ile çıkar; motor değişirse aynı gün
için yeni klasör açılır, eskisi kalır.

- `ozet.json`: son gün, iki adayın özkaynağı, faiz geliri, işlem kârı, en iyi üç işlem hariç işlem kârı, yalnız nakit,
  BIST 100 al-tut, sayılar, kasanın atladığı emirler; dondurma özeti, düzeltmeler, motor ağacı, `tansu` commit'i, veri
  kimliği ve fiyat dosyası özeti, kaynak günü hataları.
- `<aday>-sinyaller.csv` (her sinyal ve sonucu), `<aday>-islemler.csv` (dolan emirler, kasa kararı, adet, kâr),
  `<aday>-gunluk-kasa.csv`.
- `izleme/izleme.tsv`: her yeni kayıtta aday başına bir satır (yalnız eklenir).

### Otomatik günlük güncelleme

Görev Zamanlayıcı görevi `TansuGartleyIzleme` (bu bilgisayar): pazartesi-cuma 20:00 (İstanbul), bilgisayar kapalıysa
açılınca. Eylem: ana sanal ortamın `pythonw.exe`'si `-X utf8 kanit\gartley-takip\izle.py --zamanli`, çalışma klasörü
`gartley-takip` dalının worktree'si. Görev veriyi ve izleme kaydını günceller, yeni kaydı `gartley-takip` dalına yerel
olarak commit eder; push etmez. Dal başkaysa hiçbir şey yapmaz (çıkış 2). Çıktı ana deponun
`veri/takip-gartley/izleme-log/` klasöründedir. Görev yalnız kullanıcı oturumu açıkken çalışır.

Durum: `Get-ScheduledTask -TaskName TansuGartleyIzleme | Get-ScheduledTaskInfo` (son çalışma ve sonuç kodu; 0 başarı).

Durdurma:

- Çalışan koşuyu kesmek: `Stop-ScheduledTask -TaskName TansuGartleyIzleme`
- Görevi duraklatmak (tanım kalır): `Disable-ScheduledTask -TaskName TansuGartleyIzleme`
- Yeniden başlatmak: `Enable-ScheduledTask -TaskName TansuGartleyIzleme`
- Görevi silmek: `Unregister-ScheduledTask -TaskName TansuGartleyIzleme -Confirm:$false`
