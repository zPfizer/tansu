# 04: borsapy tabloları ve ikinci kaynak karşılaştırması

**What to build:** Anlık görüntü borsapy'den gelen tabloları da içerir:
- TCMB politika faizi
- sektörler
- XU100 işlem günleri (takvim)
- karşılaştırma getirileri

İki kaynak, ortak günlerde T−1'e kadar karşılaştırılır. Fark %0,5'i aşan günler ve tek kaynaklı gün
sayısı raporlanır. borsapy alınamazsa kontrol "yapılmadı" olur; indirme durmaz.

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] borsapy tabloları anlık görüntüye yazılır ve manifestte hash'lenir. Koşu canlı borsapy'ye bağlı kalmaz.
- [ ] Faiz serisi değişim günlerinden günlük seriye ileri doldurulur.
  - Seri bir gün gecikmeli kullanılır.
  - Son değişim tarihi kaydedilir.
  - Seri boşsa sonuç SORUNLU olur.
- [ ] Karşılaştırmadan şu günler çıkarılır:
  - olay tablosunda kaydı olan günler
  - borsapy'nin bugünkü yarım çubuğu
- [ ] Testler: sahte borsapy adaptörüyle fark tespiti, olay günü dışlama ve "yapılmadı" yolu.
- [ ] Açık soru 8.9 (faiz serisi bir haftalık repo mu?) borsapy kaynağından kontrol edilir; TASARIM §8'e
      yazılır.
