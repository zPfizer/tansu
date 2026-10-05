# 01: Kullanım koşulları ve fiyat adımı doğrulaması

**What to build:** Veri indirmeye başlamadan önce iki şey bilinir hale gelir:
- İş Yatırım'ın ve borsapy'nin (TradingView, KAP, TCMB kaynakları) kişisel, otomatik ve günlük kullanıma izin
  verip vermediği. Hız sınırları da bu kapsamdadır.
- TASARIM 5.1'deki BISTECH fiyat adımı tablosunun doğru olup olmadığı.

Sonuç TASARIM'a işlenir: 8.1 ve 8.10 kapanır ya da gerekçeli kalır.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Kullanım koşulları birincil kaynaktan okunur. Yöntem `/research`, arka planda. Çıktı alıntılı bir not
      olarak `docs/arastirma/` altına yazılır.
- [ ] Koşullar otomatik indirmeyi yasaklıyorsa TASARIM §4 ve §8'e yazılır ve iş durur. Bu durumda karar
      Claude'undur ve gerekçesi yazılır.
- [ ] Fiyat adımı tablosu Borsa İstanbul'un kendi belgesinden doğrulanır.
- [ ] Gerçek veride bir örnek kontrol edilir: KONTR 08.07.2026 ya da başka bir kilitli gün.
- [ ] TASARIM 5.1'deki tablo ve §8 güncellenir; commit edilir.
