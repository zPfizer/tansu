# 01: Kullanım koşulları ve fiyat adımı doğrulaması

**What to build:** Veri indirmeye başlamadan önce iki şey bilinir hale gelir:
- İş Yatırım'ın ve borsapy'nin (TradingView, KAP, TCMB kaynakları) kişisel, otomatik ve günlük kullanıma izin
  verip vermediği. Hız sınırları da bu kapsamdadır.
- TASARIM 5.1'deki BISTECH fiyat adımı tablosunun doğru olup olmadığı.

Sonuç TASARIM'a işlenir: 8.1 ve 8.10 kapanır ya da gerekçeli kalır.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Kullanım koşulları birincil kaynaktan okunur. Yöntem `/research`, arka planda. Çıktı alıntılı bir not
      olarak `docs/arastirma/` altına yazılır.
- [x] Koşullar otomatik indirmeyi yasaklıyorsa TASARIM §4 ve §8'e yazılır ve iş durur. Bu durumda karar
      Claude'undur ve gerekçesi yazılır.
- [x] Fiyat adımı tablosu Borsa İstanbul'un kendi belgesinden doğrulanır. Kısmen: birincil PDF'lerin
      metni çıkarılamadı. Tablo ikincil kaynak ve gerçek veriyle doğrulandı.
- [x] Gerçek veride bir örnek kontrol edilir: KONTR 08.07.2026 ya da başka bir kilitli gün. 8 hissenin
      2025–2026 fiyatları ve 3 hissenin 2016–2023 fiyatları kontrol edildi.
- [x] TASARIM 5.1'deki tablo ve §8 güncellenir; commit edilir.

## Comments

05.10.2026, Claude:
- **TradingView kaynaklı veri bırakıldı.** Sonuç: ikinci kaynak fiyat karşılaştırması kalktı.
- **XU100 ve takvim** İş Yatırım `END_DEGER` alanından alınacak.
- **İş Yatırım'ın robots.txt yasağı** bilinen risk olarak yazıldı. Kullanım küçük ayak iziyle sürüyor.
- **Fiyat adımı** tarih bazlı oldu: 06.11.2023 öncesinde 100 TL üstü adım 0,10.
- **Ayrıntı:** `docs/arastirma/kullanim-kosullari-fiyat-adimi.md`.
