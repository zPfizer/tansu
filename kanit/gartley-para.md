# Gartley para işi: faizi ve BIST 100'ü geçmek (29.10.2026)

Dal: `gartley-para` → `yeniden-kurulus`. Ürün kodu (`tansu/`) değişmedi. Ölçüm betiği ve dondurulan ayar
`kanit/gartley-para/` altındadır.

İstek (Levent, 29.10.2026): Gartley 2023-2025'te 100.000 TL'yi 133.771 TL yaptı; faiz 301.954 TL, BIST 100 al-tut
204.414 TL verdi. Hedef: 2023-2025'te komisyon ve kaymadan sonra ikisini de geçmek, en büyük düşüş %25'in altında.
Ayar yalnız 2015-2022'de yapılır. 2023-2025 sonda bir kez koşar; sonuçtan sonra ayar değişmez.

2023-2025 tam kör değildir: dondurulmuş Gartley ayarı 2021-2025 ileri yürümesinden geldi ve paper trade sonucu
biliniyordu. Bu iş desen ayarını 2015-2022'de yeniden seçti; ama denenen seçenek ailesi (pivot 10/12/15/20, tolerans
0,03-0,05, geçerlilik 5/10/20, stop X) 2021-2025 görülerek kurulmuştu.

## Sonuç: 2023-2025 testi (tek koşu)

Dondurma commit'i a81286e (GitHub'a test öncesi gönderildi), ayar SHA-256 `118ad754…32e6`. Test bu commit'ten sonra
bir kez koştu; ayar değişmedi. Çıktı: `kanit/gartley-para/test-sonuc.json`.

| 100.000 TL, 2023-2025 | Son | Yıllık bileşik | En büyük düşüş |
|---|---|---|---|
| Gartley, dondurulmuş ayar, bütün maliyetlerden sonra | **344.900 TL** | %51,0 | **−%23,0** (06.12.2023 → 04.11.2024) |
| Faiz (brüt politika faizi) | 301.954 TL | | |
| Aynı kesintili faiz (%15), yalnız nakit | 255.871 TL | | |
| BIST 100 al-tut (fiyat endeksi) | 204.414 TL | | −%22,9 |

- Hedefin üç şartı tutar: faizi 42.946 TL, BIST 100'ü 140.486 TL geçer; düşüş %25'in altındadır (%23,0, sınıra
  yakın).
- 42 işlem; 13 kazanan, 29 kaybeden (%31). İşlem kârı 85.660 TL, nakit faizi 159.239 TL. Kasanın ortalama %37,8'i
  hissededir.
- Yıllar: 2023 %123,9; 2024 %4,2; 2025 %47,9. Faiz aynı yıllarda %20,1 / %63,2 / %54,0 verdi. 2024 faizin çok altındadır.
- Kazanç üç işleme bağlıdır: EGPRO (05.2023, +60.358 TL), ORGE (05.2023, +50.833 TL), HURGZ (04.2025, +43.740 TL). Bu
  üçü olmasa işlem kârı −69.271 TL olur; kaba tahminle kasa 170-190 bin TL'ye, iki kıyasın da altına iner (koşulmadı:
  test tek koşudur).
- Ortalama 0,744 R (motor), toplam 31,23 R.

## Adım 1: teşhis

Kaynak: paper trade (risk %1, 2023-2025 yürüyen örneklem dışı 34 işlem) ve az-işlem raporu (29.10.2026).

- Neden az işlem: 2021-2025'te 4.050 X<B<C<A şeklinden AB/XA 0,618 ± %4 adımında 308'i kalır (%7,6). 235 sinyalin 176
  emri 5 günde dolmaz, 24'ü karantinadadır; 35 işlem kalır. Motor hatası yoktur.
- Boşta para: kasanın ortalama %8,8'i hissededir, %91,2'si boştadır. Günlerin %35,9'unda açık pozisyon yoktur.
- Kayıp nereden: Gartley 133.771 TL, faiz 301.954 TL. Boş nakit faiz alsaydı kasa 363.167 TL olurdu; boşta durmanın
  maliyeti 229.396 TL'dir. Kaybeden 12 işlemin toplamı −13.907 TL'dir. Boşta durmanın maliyeti kayıp işlemlerin 16,5
  katıdır.

## Veri

- İş Yatırım günlük fiyatı (projenin kaynağı), bütün BIST: bugünkü 805 kod ve 2014'ten beri kapanan 93 kod. 670
  sembolde fiyat var; 225 kod kaynakta boş, 3 kod inmedi (INTEK, LRSHO, LYDHO). Görüntü 20260101-0000 (indirme
  29.10.2026), 2014-01-02 - 2025-12-31. Veri depoya girmez.
- Fiyatlı sembol: 2015'te 429, 2018'de 411, 2022'de 485, 2025'te 591.
- Hayatta kalan yanlılığı: 2015-2022'de işlemi kapanan 71 kodun 67'sinde fiyat var. Kalan yanlılık küçüktür, sıfır
  değildir.
- 4 saatlik veri yok: kaynak yalnız günlük veri verir. Kol 1'in bu kısmı atlandı.

## Sabit kurallar (ayar değil)

- Komisyon taraf başına %0,1575 (motor). Kayma: her alış ve satışta, ham fiyatta 1 fiyat adımı, en az %0,1.
  2015-2022 son ayarında kayma kasadan 50.719 TL alır (kaymasız 568.550 TL, kaymalı 517.831 TL).
- Likidite: pozisyon tutarı dolumdan önceki 20 günün ortanca TL hacminin %10'unu geçmez.
- Stop emri: açılış stopun altındaysa çıkış açılıştan.
- Adet, emir fiyatı (D) ve dünkü kapanış özkaynağıyla, açılıştan önce hesaplanır. Giriş gün başı nakdiyle. Kaldıraç
  yok, tam sayı adet, sembol başına bir pozisyon.
- Özkaynak her gün kapanışta, açık pozisyonun satış komisyonu ve kayması düşülerek değerlenir. Düşüş bu günlük eğride
  ölçülür.
- Boş nakit: TCMB politika faizi (projedeki `faiz.parquet`), bir gün gecikmeli, takvim günü / 365, %15 kesinti
  (repo stopajı varsayımı). Faiz kıyası brüt politika faizidir (paper trade ile aynı); bu yüzden kıyas stratejiye karşı
  ihtiyatlıdır. TLREF verisi projede yok.
- BIST 100 kıyası fiyat endeksidir (temettüsüz), dönem öncesi son kapanıştan al-tut.

## Seçim

Kural (ölçümlerden önce yazıldı): 2015-2022 dönem sonu özkaynağını artıran ve günlük düşüşü %25'in altında tutan
değişiklik kalır; fark %0,5'ten azsa basit seçenek kalır. Sıra: desen ızgarası, kol 1, kol 2, kol 3, kol 4, son tur.

İki tur yapıldı. Bağımsız inceleme ilk turdan sonra bir ileriye bakma buldu: boşlukla açılan dolumda adet açılış
fiyatıyla hesaplanıyordu (39 işlemin 2'si). Adet artık emir fiyatıyla hesaplanır. Motor işlemleri aynı kaldı (51 ayrı
işlem kümesinin 51'i eşleşti), ama ızgaranın birincisi değişti. Bu yüzden seçim zinciri düzeltilmiş betikle baştan
kuruldu. Sayılar ikinci turdandır.

- Denenen ayrı varyant: 154; koşu: 252. İkinci tur ilk turun 92 koşusunu yeniden koştu ve 62 yeni koşu yaptı. Belge yazılırken bir kusur daha bulundu: çıkış TP seçilince ayarda kalan iz değeri de çalışıyordu. Etkilenen 6 kıyas koşusu düzeltilmiş betikle yeniden koştu; seçilen ayar iz stoplu olduğu için etkilenmedi (dondurma doğrulaması iki betikle de 517.831 TL).
- Son turda kalan farklar %1-2'dir; komşu ayarların oynaklığı (risk %3 / %4 / %5: 476.846 / 504.646 / 512.934 TL)
  bundan büyüktür. Arama burada durdu.

### Kolların 2015-2022 etkisi

100.000 TL, 2015-2022. Faiz 272.104 TL, BIST 100 al-tut 642.684 TL (düşüş −%31,8).

| Adım | Seçenek | Sonuç | Karar |
|---|---|---|---|
| Taban | dondurulmuş ayar (pivot 10, tolerans 0,04, 5 gün), risk %1, faiz yok, TP1/TP2 | 103.869 TL, 19 işlem, düşüş −%5,0 | |
| Desen | 36 noktalı ürün ızgarası | pivot 12, tolerans 0,05, 20 gün: 121.102 TL, 50 işlem | tutuldu |
| Kol 1 | dört pivot birleşimi | 120.838 TL (düşüş −%14,4) | bırakıldı |
| Kol 1 | 7 günlük pivot da | 77.673 TL (düşüş −%41,2) | bırakıldı |
| Kol 1 | oranın mutlak okunuşu | 122.235 TL; son turda 504.646 → 258.780 TL | ilk turda tutuldu, son turda bırakıldı |
| Kol 1 | 4 saatlik grafik | veri yok | atlandı (engel) |
| Kol 2 | risk %2-5, pozisyon üst sınırı %15-100, nakit yetmezse küçült | risk %4, poz %20, küçült: 161.747 TL (düşüş −%23,1); yalnız risk %2 bile −%27,2 | tutuldu |
| Kol 3 | boş nakde faiz (%15 kesinti) | 317.262 TL (düşüş −%11,7) | tutuldu |
| Kol 4 | TP1, TP2, iz 1,5/2/2,5/3 ATR, TP1 yarı + iz | iz 2,5 ATR: 364.878 TL (TP1/TP2 317.262) | tutuldu |
| Son tur | okuma, birleşim, risk, poz, iz | oran okunuşu, poz %33, risk %5, iz 3 ATR: 517.831 TL | tutuldu |

Son ayardan bir kol çıkarılınca (2015-2022):

| Son ayar ... | Sonuç | Düşüş | İşlem |
|---|---|---|---|
| hepsi açık | 517.831 TL | −%12,0 | 50 |
| faiz yok (kol 3 kapalı) | 252.374 TL | −%24,6 | 50 |
| çıkış TP1/TP2 50/50 (kol 4 kapalı) | 349.722 TL | −%13,3 | 49 |
| paper boyutu: risk %1, sınırsız, atla (kol 2 kapalı) | 335.344 TL | −%4,7 | 50 |
| dondurulmuş desen ayarı | 255.717 TL | −%5,2 | 19 |
| dört pivot birleşimi (kol 1 açık) | 477.882 TL | −%24,1 | 98 |
| mutlak okunuş (kol 1 açık) | 248.172 TL | −%14,3 | 76 |
| kayma yok (bilgi) | 568.550 TL | −%11,4 | 50 |
| hepsi kapalı (taban) | 103.869 TL | −%5,0 | 19 |

Son ayarın 2015-2022 yılları: 2015 %32,5; 2016 %6,5; 2017 %17,9; 2018 %0,6; 2019 %18,2; 2020 %9,1; 2021 %2,1;
2022 %135,3. Faiz geliri 137.945 TL, işlem kârı 279.886 TL. Kasanın ortalama %13,6'sı hissededir. Faizi geçer,
BIST 100'ü 2015-2022'de geçmez.

## Dondurulan ayar

`kanit/gartley-para/ayar.json` (SHA-256 `118ad754930a67cb70f4ace06de0981142e1a5539dcdfe15ca6e2eb0d43e32e6`):

- Desen: Gartley, pivot `sag_bar_12`, tolerans 0,05 (oranın payı), emir 20 gün geçerli, stop X, kapı 1,4.
- Çıkış: hedef yok; iz süren stop, en yüksek kapanış − 3 ATR, her gün kapanıştan sonra yükselir; açılış stopun
  altındaysa açılıştan çıkış.
- Boyut: işlem başına risk özkaynağın %5'i, ama pozisyon özkaynağın en çok %33'ü; nakit yetmezse adet küçülür;
  likidite sınırı %10.
- Nakit: boş nakit politika faizi, %15 kesinti.
- Maliyet: komisyon %0,1575, kayma 1 fiyat adımı (en az %0,1), taraf başına.

Betik `kanit/gartley-para/para.py` (SHA-256 `95dfd8a9774e61a4be56087b3d106b7de56483c81ae67fb4a0e9dc51a130dd83`).
`test` kipi yalnız bu ayar dosyasıyla ve bir kez koşar (kilit dosyası `open(..., "x")`). Motor `tansu/` bu commit'teki
paketle aynıdır (b9f6107).

Dondurma doğrulaması (bu dosyalarla, 2015-2022):

```
$ python -X utf8 kanit/gartley-para/para.py ayar <gunler-2014-2025.pkl> <faiz.parquet> kanit/gartley-para/ayar.json <kayıt.tsv> dondurma-dogrulama
{"etiket": "dondurma-dogrulama", "son": 517831, ..., "en_kotu_dusus_yuzde": -12.03, ..., "islem": 50, ...}
```

## Denetim

- Betik ilk hâliyle paper trade'in 2021-2025 sonucunu verdi: 130.720 TL (paper 130.729 TL; 9 TL fark açık pozisyonun
  satış maliyeti düşülerek değerlenmesinden). Adet kuralı düzeltilince aynı koşu 128.258 TL verir: paper trade'in
  boşluk dolumlarındaki adet hesabı küçük bir ileriye bakma içeriyordu.
- Bağımsız inceleme (ayrı ajan, salt okuma, yalnız 2022 sonuna kadar veri): 39 işlemin her biri dolum, çıkış ve
  çıkıştan önceki gün kesilen veriyle aynı sonucu verdi; bütün evren 2016, 2018 ve 2020 sonunda kesilince kapanan
  işlemler aynı kaldı. Maliyet, kayma, nakit, düşüş ve süreç yamaları doğru bulundu. Bulunan iki kusur düzeltildi:
  boşluk dolumunda adet ve tek koşu kilidi (SHA sabiti, `open(..., "x")`, kod özeti). Önbellek anahtarına kod özeti
  eklendi; bilinmeyen ayar alanı koşuyu durdurur.

## Sınırlar

- Aşırı uyum riski yüksektir: 154 varyant denendi; son ayar 8 yılda 50 işlemle seçildi. Komşu ayarlar arasında %5-50
  fark var (ör. pozisyon üst sınırı %33 → 504.646 TL, %40 → 430.210 TL).
- 2015-2022 sonucunun büyük kısmı 2022'den gelir (%135).
- 50 işlemin bir kısmı fiyat düzeltmesi (temettü, bedelsiz) gününü kapsar; emir düzeltilmiş fiyatla modellendi.
- Faiz kesintisi (%15) bir varsayımdır; mevduat ve fon stopajı dönem içinde değişti, tarih tarih doğrulanmadı.
- T+2 takas ve emir kuyruğu modellenmedi.
