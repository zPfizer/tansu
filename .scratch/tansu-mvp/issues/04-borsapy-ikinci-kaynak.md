# 04: Faiz ve sektör tabloları, XU100 takvimi

**What to build:** Anlık görüntü şu tabloları da içerir:
- **TCMB politika faizi.** borsapy'den, TCMB kaynağıyla.
- **Sektörler.** borsapy'den, KAP kaynağıyla.
- **XU100 kapanışı ve işlem takvimi.** İş Yatırım `END_DEGER` alanından.

İkinci kaynak fiyat karşılaştırması bilet 01 kararıyla kalktı: TradingView koşulları buna izin vermiyor.
`docs/arastirma/kullanim-kosullari-fiyat-adimi.md`

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] Tablolar anlık görüntüye yazılır ve manifestte hash'lenir. Koşu canlı borsapy'ye bağlı kalmaz.
- [ ] borsapy'nin faiz ve sektör verisini TradingView'den değil TCMB ve KAP'tan aldığı borsapy kaynak
      kodundan doğrulanır. TradingView'den alıyorsa o tablo da bırakılır ve TASARIM güncellenir.
- [ ] Faiz serisi:
  - Değişim günlerinden günlük seriye ileri doldurulur.
  - Bir gün gecikmeli kullanılır.
  - Son değişim tarihi kaydedilir.
  - Seri boşsa sonuç SORUNLU olur.
- [ ] XU100:
  - Endeks kodu 01'in XU100 olduğu doğrulanır: bilinen bir günün kapanışı bilinen değerle karşılaştırılır.
  - Takvim, XU100 kapanışı olan günlerdir.
- [ ] Testler sahte adaptörlerle yazılır: faiz ileri doldurma, gecikme, boş seri ve takvim.
- [ ] Açık soru 8.9 (faiz serisi bir haftalık repo mu?) TCMB kaynağından kontrol edilir ve TASARIM §8'e
      yazılır.
