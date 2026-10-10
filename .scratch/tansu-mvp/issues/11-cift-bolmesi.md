# 11: Çift rotasyonu bölmesi

**What to build:** `sinama` çift rotasyonu ailesini de koşar. Bölme şöyle çalışır:
- Her yıl önceden yazılmış kuralla en fazla 5 çift seçilir.
- Her çift payı Z ±2 ve ΔZ dönüşüyle iki hisse arasında geçiş yapar.
- Raporda kendi sermaye eğrisi, K2 ve tanısal 50/50 tutma karşılaştırması yer alır.
- VAKBN–GARAN sabit çift olarak ayrıca gösterilir.

**Blocked by:** 06, 10

**Status:** done

- [x] Yıllık seçim:
  - Seçim yılın ilk işlem günü kapanışında, o günkü evrenle yapılır.
  - Aynı sektör şartı aranır; hissenin 252 gün verisi olmalıdır; eşbütünleşme p < 0,05 olmalıdır.
  - Sıralama açgözlüdür: bir hisse yalnız bir çiftte olur, bir sektörden en fazla 2 çift seçilir, β ≤ 0
    olan çift elenir.
  - X/Y rolü sembol sırasından belirlenir. Sektörü olmayan hisse aday olmaz.
- [x] Geçişler:
  - Geçiş ertesi gün AOF'tan yapılır. Bacak kilitliyse geçiş olmaz ve sinyal taşınmaz.
  - Bacak karantinadaysa çift girişsiz kalır.
  - Çiftin hissesi kapanırsa pay nakde geçer.
  - Yıl geçişinde düşen çift kapanır; yine seçilen çift işlemsiz sürer.
  - Hiç çift seçilmeyen yıl "işlem yok" diye işaretlenir.
- [x] Paylar yıl başında eşittir, yıl içinde dengelenmez. Burada "işlem" geçişten geçişe tutuş demektir.
- [x] 50/50 tanısal: yılın ilk günü bir kez alınır, yıl boyunca tutulur.
- [x] Testler `kosu()` yüzünden, sentetik iki hisseli anlık görüntüyle:
  - seçim kuralları
  - geçiş günleri
  - kilitte geçiş olmaması
  - yıl geçişi
  - kapanma

## Comments

Kod: `tansu/ciftbolme.py` (yeni, `KOD_DOSYALARI`'nda; çift `Parametre` kural kaydı parametrelerine girdi), `kayit.kosu`
sonucunda `["cift"]`, `rapor` yeni bölüm (kendi eğri, K2, tanısal 50/50, seçilen çiftler, VAKBN–GARAN) ve
`cift-islemler-<koşu>.csv`. Test: 143 yeşil (önce 128; bu bilet +15). Belge önce: TASARIM 4 (sektör toplu okuma),
5.6 (evren süzgeci düzeltmesi ve "Çift bölmesi kuralları"), GLOSSARY.

**Ön düzeltme A (evren süzgeci motora).** `motor.sinama(..., uye=)`: yalnız simülatörün alabileceği (simülatör
başlangıcından sonra, sinyal gününün ayının evreninde) sinyaller motora girer; simülatör süzgeci güvence olarak kaldı.
- Önce (bilet 10): motor 417 işlem (241 stop, 145 sma250, 30 karantina, 1 veri sonu), 7 iptal; simülatörün aldığı 67.
- Sonra: motor 67 işlem (39 stop, 25 sma250, 2 karantina, 1 veri sonu), 2 iptal; alınan 67, reddedilen 0.
- Sonuç değişmedi: son özkaynak %0,1/%0,3/%0,5 = 20.894.172 / 20.416.778 / 19.949.127 TL, K2 28.130.463 /
  28.161.269 / 28.191.557 TL (aynı koşu: anlık görüntü 20261005-1726, `resmi:false`). Yani engelleme bu veride hiçbir
  alınan işlemi etkilememişti; düzeltme yine de motor ve simülatör pozisyonlarını bire bir yapar.
- Kalan yaklaşıklık (TASARIM 5.6'da yazılı): yer ya da nakit yüzünden reddedilen sinyal motorda pozisyon sayılır
  (bu koşuda 0 reddedilen).
- Test: `test_sinama_evren_disi_sinyal_pozisyon_acmaz_...` (motor yüzü); `test_kayit.py` verisinin ilk günü Şubat'ın son
  gününe çekildi (sinyal gününün evrende olması için; assert'ler aynı).

**Ön düzeltme B (TUPRS +%1.234).** Gerçek hareket; hata yok, kod değişmedi.
- İşlem: giriş 06.08.2021 düzeltilmiş AOF 9,2602 (ham AOF 97,455), çıkış 12.09.2024 (sma250) düzeltilmiş AOF 124,2714
  (ham 155,816); getiri %0,3 masrafla 12,3397 = +%1.234.
- Olay: 04.04.2023 bedelsiz %600 (çarpan 1/7): ham kapanış 564,40 → 82,05 (÷6,88; olay günü +%1,8 hareket). Olay denetimi
  TUPRS için fark üretmedi; elde tutma süresince karantina 0, eksik gün 0, en büyük günlük düzeltilmiş hareket %10,0.
- Hesap: ham fiyat artışı 155,816 × 7 / 97,455 = 11,19 kat (+%1.019); kalan fark brüt temettülerin düzeltilmiş
  seriye dahil olması (03.2023–04.2024 üç temettü çarpanı 0,834 → ×1,199): 11,19 × 1,199 = 13,42 kat. İki seri tutarlı.
- Not: düzeltilmiş seri brüt temettüyü yeniden yatırılmış sayar (TASARIM 4); net temettü vergisi modellenmiyor. Uç değer
  K1/istatistikte ortalamayı şişirir; medyan ve en iyi %5 atılmış sonuç (5.9) bunun için var.

**Ön düzeltme C (KAP sektörü).** `kaynak.KapSektor`, `veri.sektor_tamamla`, `python -m tansu sektor-indir`.
- Neden: bilet 07'de 616 sembol sektörsüz kalmıştı. Sebep HTTP 429 (KAP, yaklaşık 100 şirket sayfası isteğinden sonra
  hız sınırı; Retry-After yok, pencere ≈ 10 dk). İstek: ≥ 1 sn aralık, User-Agent `tansu-kisisel/0.1`, liste bir kez + sembol
  başına bir sayfa; art arda 5 hatada durur, tamamlananlar `veri/onbellek/sektor-<kimlik>.jsonl`'de kalır.
- Dört çalıştırma (10 dk arayla) bitti. Yeni anlık görüntü **20261005-1949** (eski 20261005-1726 değişmedi; manifest
  `kaynak` ve `sektor_kapsam` taşır): hedef 275 evren üyesi, sektörü var 260, KAP listesinde yok 15 (işlemi kapanmış
  kodlar: AKFEN ANACM ASLAN BOLUC BOYP DENIZ DGZTE DOCO IZOCM KIPA OLMK PKENT SAFGY SODA TRKCM), alınamayan 0. `sektor.json`
  304 sembol, 15 sektör adı. Üye olmayan 400 sembolün sektörü okunmadı (çift adayı olamazlar).
- Bu 15 üye sektörsüz kaldığı için çift adayı olamaz (TASARIM 5.2).

**Gerçek koşu (geliştirme, `resmi:false`, anlık görüntü 20261005-1949, günlük `kayit/` repo dışında).** Seçim ve sonuçlar:
- Seçilen çift sayısı yıl başına: 2016 5, 2017 5, 2018 4, 2019 5, 2020 4, 2021 5, 2022 5, 2023 5, 2024 5, 2025 5, 2026 5
  (toplam 53); "işlem yok" yılı yok. Sektörler KAP adlarıyla (MALİ KURULUŞLAR, İMALAT, TOPTAN VE PERAKENDE TİCARET…).
- Çift bölmesi, %0,3: 82 tutuş dönemi (39 geçiş, 38 yıl geçişi, 5 karantina), 80 farklı giriş günü. Son özkaynak 11.058.764 TL;
  aynı koşuda K2 27.367.045, tanısal 50/50 33.788.370 TL (%0,1: 11.545.721; %0,5: 10.574.531).
- Yıllık fazla getiri (kural − K2, puan, %0,3): 2016 −0,5; 2017 −11,3; 2018 −14,0; 2019 −4,2; 2020 −24,8; 2021 0,0;
  2022 +1,7; 2023 −9,0; 2024 −13,1; 2025 −22,6; 2026 −15,1. Ortalama yatırım payı ≈ %47 (boş paylar nakitte).
  Kural K2'nin altında; henüz p değeri yok.
- VAKBN–GARAN sabit çift (%0,3): 13 tutuş dönemi, son özkaynak 16.578.719 TL; maruziyeti eşleşmiş K2 51.745.641 TL;
  aynı çiftin 50/50 tutulması 15.619.113 TL. (Tek hisse ailesi koşusu bu bilette değişmedi: EMA 20,42 M / K2 28,16 M.)
- Örneklem şartı (5.9, en az 100 geçiş ve 60 farklı gün): 82 tutuş dönemi / 80 gün ile bu veride **dolmuyor**; bilet 12
  "ölçülemedi" sorusunu buna göre yargılar. Rapor bunu uyarılarda yazıyor.
- Süre: çift bölmesi tek başına ≈ 25 sn; tam `sinama` ≈ 4 dk.

**Belge boşlukları dolduruldu (TASARIM 5.6 "Çift bölmesi kuralları", gerekçeli):**
- Roller: Y = alfabetik ilk sembol. Eşbütünleşme: `statsmodels.coint(log Y, log X)` (Engle–Granger, sabit terimli), düzeltilmiş
  kapanış, son 252 gün; β = pencerede log Y'nin log X'e OLS eğimi (β ≤ 0 testten önce elenir). Aday: son 252 işlem gününün
  hepsinde kapanışı olan evren üyesi.
- "Kilitli" = herhangi bir bacakta tavan ya da taban kilidi (ya da o gün işlem yok): geçiş yapılmaz, sinyal her kapanışta
  yeniden hesaplanır (eski sinyal taşınmaz). Karantina penceresi motorla aynı (250 satır); tutulan bacakta karantina günü
  → son temiz AOF'ta kapanır.
- Paylar: sermaye / 5; devam eden çift payı eşitlenmez (işlem ve masraf gerektirirdi; YORUM); yeni çiftler ve boş paylar
  serbest nakdi eşit paylaşır. Adet tam lot, alışta %2 likidite sınırı (sinyal günü 10 gün medyan).
- Düşen çift seçimden sonraki ilk işlem günü (seçim gününün ertesi) AOF'unda kapanır.

**Açık işler:**
- **Toplu bozuk satır:** 21.05.2026'da 556 sembol (ve 16–17.09.2026'da 128 + 57) karantinaya girdi. Neden: o günkü satırlarda
  yüksek = düşük = kapanış ve AOF bu aralığın dışında (örn. GARAN 21.05: 120,0 / AOF 127,394): kaynak yarım gün mumu vermiş
  görünüyor. Kapı kuralı gereği her sembol 250 gün yeni giriş almıyor ve açık pozisyon karantina günü kapanıyor (21.05.2026'da
  çift bölmesinde 2, VAKBN–GARAN'da 1 çıkış; EMA'nın 2 karantina çıkışının tarihine bakılmadı). Veri yamanmadı (TASARIM 5.1); sistemik bozuk günün "eksik gün" sayılması Levent kararı.
  Evren üyesi karantina oranı bu yüzden bilet 10'daki %0,23'te kaldı ama 2026 sonuçları bundan etkilenir.
- Kalan 15 üye sektörsüz (kapanmış kodlar); KAP'ta yok.
- Çift bölmesi için K1 (aynı çiftlerde rastgele günlerde geçiş) ve p değeri bilet 12'de.
- 2015 yılı (yalnız Aralık) çift bölmesi yıllık tablosunda "−" (seçim yılı değil).
