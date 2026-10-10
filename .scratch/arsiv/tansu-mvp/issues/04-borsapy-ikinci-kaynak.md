# 04: Faiz ve sektör tabloları, XU100 takvimi

**What to build:** Anlık görüntü şu tabloları da içerir:
- **TCMB politika faizi.** borsapy'den, TCMB kaynağıyla.
- **Sektörler.** borsapy'den, KAP kaynağıyla.
- **XU100 kapanışı ve işlem takvimi.** İş Yatırım `END_DEGER` alanından.

İkinci kaynak fiyat karşılaştırması bilet 01 kararıyla kalktı: TradingView koşulları buna izin vermiyor.
`docs/arastirma/kullanim-kosullari-fiyat-adimi.md`

**Blocked by:** 02

**Status:** done

- [x] Tablolar anlık görüntüye yazılır ve manifestte hash'lenir. Koşu canlı borsapy'ye bağlı kalmaz.
- [x] borsapy'nin faiz ve sektör verisini TradingView'den değil TCMB ve KAP'tan aldığı borsapy kaynak
      kodundan doğrulanır. TradingView'den alıyorsa o tablo da bırakılır ve TASARIM güncellenir.
- [x] Faiz serisi:
  - Değişim günlerinden günlük seriye ileri doldurulur.
  - Bir gün gecikmeli kullanılır.
  - Son değişim tarihi kaydedilir.
  - Seri boşsa sonuç SORUNLU olur.
- [x] XU100:
  - Endeks kodu 01'in XU100 olduğu doğrulanır: bilinen bir günün kapanışı bilinen değerle karşılaştırılır.
  - Takvim, XU100 kapanışı olan günlerdir.
- [x] Testler sahte adaptörlerle yazılır: faiz ileri doldurma, gecikme, boş seri ve takvim.
- [x] Açık soru 8.9 (faiz serisi bir haftalık repo mu?) TCMB kaynağından kontrol edilir ve TASARIM §8'e
      yazılır.

## Comments

- Kaynak kodu doğrulaması (borsapy 0.11.0): faiz `_providers/tcmb_rates.py` ile tcmb.gov.tr "1 Hafta Repo"
  HTML tablosundan; sektör `_providers/kap.py` `get_company_details` ile KAP şirket sayfasından (sembol başına
  birkaç istek, hatada sessizce `{}` döner; adaptör bunu `KaynakHatasi` yapar). İkisi de TradingView değil.
  TASARIM güncellendi.
- XU100 doğrulaması (gerçek veri, ağsız): `veri/ag/20261005-1436` `xu100` 29.12.2023 = 7470,18 (bilinen kapanış);
  31.12.2024 = 9830,56. Bağımsız Yahoo `veri/XU100.parquet` ile 2.939 ortak günde medyan bağıl fark 5e-6,
  %99'u 3,3e-5 altında; tek aykırı 08.07.2015 (%1,5, Yahoo tarafı şüpheli). Endeks kodu doğru.
- Gerçek TCMB çağrısı (1 istek): 57 değişim günü, 2010-05-20 – 2026-01-23, sıralı. Son değişim 2026-01-23
  (%37). TCMB sayfasının bugüne kadar güncel olduğu doğrulanmadı.
- Açık soru 8.9 cevaplandı ve TASARIM §8'e yazıldı. Kalan: 2016-11 – 2018-06 faiz dönemi (fiili fonlama LON)
  doğrulanmadı.
- Tasarım: `indir(..., borsapy=...)` isteğe bağlı; verilmezse eski anlık görüntüler (borsapy'siz) okunur,
  `Anlik.faiz`/`sektor` `None` olur. Boş faiz serisi `indir`'de ve `faiz_gunluk`'te `VeriHatasi` verir;
  `gunluk` bunu SORUNLU'ya çevirmelidir (bilet 15).
- `faiz_gunluk` istenen aralığın başında veri yoksa da hata verir (sessiz NaN yok).
- Gerçek koşu (sektör için ~100 sembol KAP isteği) yapılmadı; bilet istemedi. Sektör istek sayısı ve süresi
  evren ölçeğinde (bilet 07) ölçülmeli. `Borsapy` adaptörü sembol arası bekleme eklemiyor.
- Testler: 26 (9 yeni).
