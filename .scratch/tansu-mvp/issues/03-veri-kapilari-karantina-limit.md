# 03: Veri kapıları, karantina, fiyat limiti ve kilit

**What to build:** Anlık görüntü artık şu bilgileri taşır:
- her günün fiyat limiti (±%20 / ±%10; olay gününde taban × çarpan)
- kilitli tavan ve taban günleri
- karantinalı hisse-günler
- eksik günler

Veri kapıları (TASARIM 5.13) kalan bir indirmeyi anlık görüntü yapmaz.

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] Fiyat limiti:
  - Taban = önceki ham kapanış.
  - Olay gününde taban = önceki ham kapanış × olay çarpanı.
  - Limit 13.03.2020'de ±%20'den ±%10'a geçer.
- [ ] Kilit:
  - Kapanışı tavan ya da taban fiyatında olan gün kilitli sayılır.
  - Tolerans bir fiyat adımıdır; tablo 01'den gelir.
  - Duyarlılık sürümü: düşük = yüksek, hacim > 0 ve fiyat limitte.
- [ ] Karantina:
  - Limiti (+%0,5) aşan ve olayla açıklanmayan gün karantinaya alınır.
  - Bozuk satır da karantinaya alınır (düşük ≤ AOF ≤ yüksek, düşük ≤ kapanış ≤ yüksek).
  - Bilinmeyen olay kodu ya da çarpanı 1 olan kayıt istisna sayılmaz.
- [ ] Eksik gün NaN kalır. Hacmi 0 olan gün işlem günü sayılmaz.
- [ ] Yapısal ihlal (sıra bozuk, tekrar eden gün, ortada NaN) indirmeyi durdurur.
- [ ] Oran eşikleri "veri sorunlu" der:
  - karantina > %1
  - eksik indirme > 5 hisse
- [ ] Testler `veri` yüzünden:
  - normal gün limiti ve olay günü limiti
  - ±%20/±%10 geçişi
  - kilitli tavan ve taban
  - karantina
  - bozuk satır
  - yapısal ihlal
  - eksik gün

  Değerler elle hesaplanır.
