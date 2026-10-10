# 08: Adım + Motor: EMA sıkışması işlemleri

**What to build:** EMA sıkışması ailesi verilen bir anlık görüntüden sinyal günleri üretir. Motor bu sinyalleri
Adım fonksiyonuyla işlem listesine çevirir:
- giriş tarihi ve fiyatı
- çıkış tarihi, fiyatı ve nedeni
- planlanan risk ve gerçekleşen kayıp

Bu dilimde boyutlandırma ve portföy yoktur. İşlem başına sonuç üretilir.

**Blocked by:** 03, 05

**Status:** done

- [x] `gostergeler`: Wilder ATR(14) (ilk değer ilk 14 TR'nin ortalaması) ve SMA250. Her biri için elle
      hesaplı birim testi yazılır.
- [x] `aileler`: EMA sıkışması girişi KURALLAR §3 madde 2'ye göre çalışır.
  - Kural: dönem bittikten sonraki 10 gün içinde kapanış dönem yüksek değerini geçerse giriş olur; dönem
    başına bir giriş.
  - 500 günlük ısınma uygulanır.
  - Sinyal günü kapanış < SMA250 ise giriş yoktur.
- [x] Adım saf bir fonksiyondur, imzası (pozisyon, mum) → pozisyon. TASARIM 5.3'teki kuralları uygular:
  - giriş ertesi gün AOF'tan
  - giriş günü yalnız stop bakılır
  - stop dolumu min(stop, AOF)
  - kilitli tavanda giriş yok, sinyal düşer
  - kilitli tabanda çıkış kayar
  - SMA250 çıkışı ertesi gün AOF'tan
  - veri bitince son kapanıştan çıkış
  - açık pozisyonda gelen yeni sinyal yok sayılır
- [x] TASARIM 5.3'teki 14 motor durumu sentetik mumlarla test edilir. Beklenen değerleri kodu görmemiş
      ayrı bir ajan elle hesaplar; hesap testin yorumunda durur.
  - Lot yuvarlama, %10 tavan ve olay günü durumları burada adet = 1 ile, yalnız fiyat yolu olarak sınanır.
    Boyutlandırma 10'dadır.

## Comments

- Yüzler: `gostergeler.sma/atr`, `aileler.sinyal(f, Parametre)`, `motor.adim(pozisyon, mum)`, `motor.islemler(mumlar, sinyaller)`
  → (işlem tablosu, düşen sinyal sayısı), `motor.sinama(anlik, parametre)` (bütün semboller). Test 75 yeşil (önce 47; bu bilet +28).
- 14 motor durumu + veri sonu + eksik gün (üç ek) 20 senaryo; beklenenleri kod görmemiş ayrı ajan elle hesapladı,
  özet `tests/test_motor.py` yorumunda. Ajan belirsizlik bildirmedi. Uçtan uca `sinama` testini ve gösterge/aileler
  örneklerini ben elle hesapladım (ajan değil).
- Belge boşlukları dolduruldu (TASARIM 5.3, gerekçeli): gerçekleşen kayıp = max(0, giriş − çıkış) × adet; karantina
  çıkışı fiyatı son temiz AOF, tarihi karantina günü; ısınma n. gün dolunca serbest; çıkış gününde (AOF) çıkmış
  pozisyonun o günkü kapanış sinyali geçerli. Karantinadan sonra 250 satır sinyal yok (motor uygular).
- Kural parametreleri: kapanış ve yüksek düzeltilmiş seriden; kilit/karantina ham seriden (`gun_tablosu`).
  Bekleyen çıkış (kilit kayması) ertesi uygun günde AOF'tan, nedeni korunur; o günkü stop dokunuşu `min(stop, AOF)` verir.
- Açık: dönem penceresi "dönem bittikten sonraki 10 gün" = bitişten sonraki 10 satır (eşiği aşan ilk gün dahil).
- Açık: düşen sinyal sayısı `islemler` dönüşünde; `kayit`/rapor (bilet 09–10) taşıyacak. Evren süzgeci (bilet 07) `sinama`da yok.
- Açık: "250 gün" karantina bloğu satır sayısıyla; gerçek ölçüm yapılmadı (gerçek anlık görüntüyle koşu bu bilette yok).
