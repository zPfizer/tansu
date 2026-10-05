# 10: Tek hisse simülatörü + faiz + K2 + ilk HTML rapor

**What to build:** `sinama`, EMA sıkışması ailesini 2015–2026 evreninde tek sürekli portföy olarak koşar.
Çıktılar:
- sermaye eğrisi
- maruziyet eşleşmeli K2 karşısında fazla getiri
- yıllara göre sonuçlar
- tek dosya HTML rapor ve işlem CSV'si

Rapor Levent'in açıp okuyabileceği ilk somut çıktıdır. Henüz p değeri yoktur.

**Blocked by:** 07, 09

**Status:** ready-for-agent

- [ ] Boyutlandırma:
  - Adet şu dördünün en küçüğüdür, aşağı yuvarlanır: %1 risk adedi, %10 tavan, %2 likidite, nakit /
    (fiyat × (1 + masraf)).
  - En fazla 10 pozisyon. Yer yetmezse en likit önce, eşitlikte alfabetik.
  - Aynı gün önce çıkışlar, sonra girişler işlenir.
  - Reddedilen sinyaller ayrıca sayılır.
- [ ] Masraf %0,1 / %0,3 / %0,5. Boştaki nakit bir gün gecikmeli politika faizi kazanır.
- [ ] K2:
  - Ay başında evrenle eşit ağırlıklı kurulur, AOF'tan AOF'a.
  - Ay başı dengelemesi %0,3 masraf öder.
  - Günlük maruziyet kuralınkine eşitlenir; kalan nakit faiz kazanır.
- [ ] Rapor:
  - Başlıkta koşu kimliği, anlık görüntü ve kod hash'i yazılır.
  - "Tansu'dan esinlenen yorum" uyarısı bulunur.
  - Yıllık fazla getiri tablosu vardır.
  - Tek bir "Uyarılar" bölümü vardır: karantina, tavan ve likidite bağlama oranları, iptal ve
    reddedilen sinyaller.
  - Ayrıca `islemler-<koşu>.csv` yazılır.
- [ ] Testler `kosu()` yüzünden, küçük sentetik anlık görüntüyle:
  - boyutlandırmanın dört sınırı
  - lot yuvarlama
  - faiz tahakkuku
  - K2 maruziyet eşleşmesi
  - yasaklı sözcük denetimi (AL, SAT, ÖNERİ, "Tansu'nun sistemi")
  - CSV sütunları
