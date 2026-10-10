# 03: Veri kapıları, karantina, fiyat limiti ve kilit

**What to build:** Anlık görüntü artık şu bilgileri taşır:
- her günün fiyat limiti (±%20 / ±%10; olay gününde taban × çarpan)
- kilitli tavan ve taban günleri
- karantinalı hisse-günler
- eksik günler

Veri kapıları (TASARIM 5.13) kalan bir indirmeyi anlık görüntü yapmaz.

**Blocked by:** 02

**Status:** done

- [x] Fiyat limiti:
  - Taban = önceki ham kapanış.
  - Olay gününde taban = önceki ham kapanış × olay çarpanı.
  - Limit 13.03.2020'de ±%20'den ±%10'a geçer.
- [x] Kilit:
  - Kapanışı tavan ya da taban fiyatında olan gün kilitli sayılır.
  - Tolerans bir fiyat adımıdır; tablo 01'den gelir.
  - Duyarlılık sürümü: düşük = yüksek, hacim > 0 ve fiyat limitte.
- [x] Karantina:
  - Limiti (+%0,5) aşan ve olayla açıklanmayan gün karantinaya alınır.
  - Bozuk satır da karantinaya alınır (düşük ≤ AOF ≤ yüksek, düşük ≤ kapanış ≤ yüksek; ham ya da
    düzeltilmiş fiyatı ≤ 0 olan satır da bozuktur, 02'nin olay denetimi bunları atlar).
  - Bilinmeyen olay kodu ya da çarpanı 1 olan kayıt istisna sayılmaz.
- [x] Eksik gün NaN kalır. Hacmi 0 olan gün işlem günü sayılmaz.
- [x] Yapısal ihlal (sıra bozuk, tekrar eden gün, ortada NaN) indirmeyi durdurur.
- [x] Oran eşikleri "veri sorunlu" der:
  - karantina > %1
  - eksik indirme > 5 hisse
- [x] Testler `veri` yüzünden:
  - normal gün limiti ve olay günü limiti
  - ±%20/±%10 geçişi
  - kilitli tavan ve taban
  - karantina
  - bozuk satır
  - yapısal ihlal
  - eksik gün

  Değerler elle hesaplanır.

## Comments

- Arayüz: `Anlik.gun_tablosu` (islem, eksik, limit, tavan, taban, kilit_tavan/taban, kilit_*_duyarli, karantina),
  `Anlik.sorunlar` (oran eşikleri; boş = temiz), `Anlik.inmeyen`, `veri.adim`. `indir` yapısal ihlalde
  `VeriHatasi` verir ve anlık görüntü yazmaz; kaynak hatası veren sembol `inmeyen` olur (manifestte).
- Birleştirme: bilet 04 `Anlik.gunler` adını XU100 takvimi için almıştı; benimki `gun_tablosu` oldu. Test 42 yeşil (önce 33). (bu bilet: 14 test, `tests/test_kapilar.py`).
- Gerçek anlık görüntü (`veri/ag/20261005-1436`, THYAO+CCOLA, 8.408 gün): karantina 12 gün (%0,14),
  hepsi gerçek bozuk satır (düşük = yüksek = 0; düzeltilmiş kapanış > yüksek). Kilit: THYAO 7 tavan / 5 taban,
  CCOLA 2 / 3; duyarlı sürüm 0 gün. Karantina oranı eşiğin altında.
- Gerçek veri bir şey buldu: düzeltilmiş seri 4 ondalığa yuvarlı, 637 satırda kapanış > yüksek (en çok 4,5e-5).
  Katı kural 618 sahte karantina üretiyordu. TASARIM 5.13'e bağıl 1e-4 pay yazıldı (belge önce).
- Seçimler: limit aşımı yalnız ham kapanışla yargılanır (yüksek/düşük değil). Olay çarpanı olay tarihine eşit ya da
  sonraki ilk işlem gününe uygulanır; ±1 gün kayma burada yok (olay denetimindeki gibi).
  Takvim = sembollerin tarih birleşimi; tek sembolde eksik gün görünmez.
- Açık: 30.11.2015 öncesi limit ±%10'du; belge ve bilet ±%20 diyor, kod ±%20 kullanır (karantina gevşek kalır).
  Kod yalnız 13.03.2020'yi bilir. 2015 öncesi sınanmayacaksa sorun yok.
- Açık: tavan fiyatı fiyat adımına yuvarlanmaz; kilit toleransı bir adım olduğu için fark kapanır.
- Açık: eksik gün gerçek evrende (100 hisse) bilet 07'de görülür; olay tarihi kayması gerçek evrende
  sahte karantina yaratırsa bilet 07'de ele alınır.
- Süreç notu: kod, testten önce yazıldı (sıra ihlali); testler sonra eklendi ve kod bozularak (limit payı) kırmızıya çevrildi.
  Yuvarlama payı ise doğru sırayla: önce kırmızı test.
- **05.10.2026, kaynak günü hatası (bilet 11 kararı).** Kural TASARIM 5.13'te: o gün satırı olan sembollerin ≥ %50'si
  aynı gün karantinadaysa (en az 20 satırlı gün) o gün tüm semboller için eksik gün (NaN): karantina, zorunlu çıkış ve
  dolum yok; `sorunlar` "kaynak günü hatası: YYYY-AA-GG" yazar (`Anlik.kaynak_gunleri`). Alt sınır 20 satır, tek
  sembollü eski testlerin bozulmaması için eklendi. Test +2 (145 yeşil). Gerçek anlık görüntü 20261005-1949'da ≥ %50
  olan 5 gün: 15.11.2010 (331/331), 21.12.2010 (336/336), 29.08.2011 (356/358), 26.01.2016 (365/416), 21.05.2026
  (556/607). Yani 21.05.2026 tek gün değil. %10'un üstünde ama %50'nin altında kalan günler (kayıt için, kural
  uygulanmaz): 25.11.2011, 2015'te 27.03, 31.03, 11.06, 03.08, 07.08, 07.10, 15.10, 26.10, 03.11, 30.04.2018,
  22.04.2024, 10.10.2025, 02.03, 03.03, 23.03, 22.04 ve 16.09.2026 (128/625, %20,5).
