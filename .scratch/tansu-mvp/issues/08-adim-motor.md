# 08: Adım + Motor: EMA sıkışması işlemleri

**What to build:** EMA sıkışması ailesi verilen bir anlık görüntüden sinyal günleri üretir. Motor bu sinyalleri
Adım fonksiyonuyla işlem listesine çevirir:
- giriş tarihi ve fiyatı
- çıkış tarihi, fiyatı ve nedeni
- planlanan risk ve gerçekleşen kayıp

Bu dilimde boyutlandırma ve portföy yoktur. İşlem başına sonuç üretilir.

**Blocked by:** 03, 05

**Status:** ready-for-agent

- [ ] `gostergeler`: Wilder ATR(14) (ilk değer ilk 14 TR'nin ortalaması) ve SMA250. Her biri için elle
      hesaplı birim testi yazılır.
- [ ] `aileler`: EMA sıkışması girişi KURALLAR §3 madde 2'ye göre çalışır.
  - Kural: dönem bittikten sonraki 10 gün içinde kapanış dönem yüksek değerini geçerse giriş olur; dönem
    başına bir giriş.
  - 500 günlük ısınma uygulanır.
  - Sinyal günü kapanış < SMA250 ise giriş yoktur.
- [ ] Adım saf bir fonksiyondur, imzası (pozisyon, mum) → pozisyon. TASARIM 5.3'teki kuralları uygular:
  - giriş ertesi gün AOF'tan
  - giriş günü yalnız stop bakılır
  - stop dolumu min(stop, AOF)
  - kilitli tavanda giriş yok, sinyal düşer
  - kilitli tabanda çıkış kayar
  - SMA250 çıkışı ertesi gün AOF'tan
  - veri bitince son kapanıştan çıkış
  - açık pozisyonda gelen yeni sinyal yok sayılır
- [ ] TASARIM 5.3'teki 14 motor durumu sentetik mumlarla test edilir. Beklenen değerleri kodu görmemiş
      ayrı bir ajan elle hesaplar; hesap testin yorumunda durur.
  - Lot yuvarlama, %10 tavan ve olay günü durumları burada adet = 1 ile, yalnız fiyat yolu olarak sınanır.
    Boyutlandırma 10'dadır.
