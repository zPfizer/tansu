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
