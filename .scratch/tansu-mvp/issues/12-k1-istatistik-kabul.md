# 12: K1, istatistik, Holm ve kabul tablosu

**What to build:** `sinama` her aileyi eşleştirilmiş rastgele kuralla (K1) karşılaştırır. Ardından:
- p değeri, güven aralığı ve saptanabilir en küçük etki hesaplanır.
- Bütün resmi denemeler üzerinden Holm uygulanır.
- Rapor her aile için 6 ölçütlük geçti/kaldı tablosunu verir: Geçti, Geçmedi ya da Ölçülemedi.
- Aile durumu (Deneme veya Kâğıt) `kayit`'a yazılır.

**Blocked by:** 11

**Status:** ready-for-agent

- [ ] K1:
  - Ön şartlar KURALLAR §3'teki gibidir.
  - (a) türü: aynı gün başka hisse; sayı gün başına korunur.
  - (b) türü: aynı hisse, aynı piyasa durumu, ±20 gün.
  - EMA için ek kol: sıkışmasız kırılım.
  - Çift için: aynı sayıda rastgele geçiş, ilk giriş gerçeğe eşit.
  - Rastgele işlemler aynı simülatörden ve aynı filtrelerden geçer.
  - Uygun gün yetmezse hata verilir.
- [ ] Tekrar sayısı ve p:
  - B ≥ max(1.000, 200·m); geliştirmede 200 ve bu p Holm'a girmez.
  - p = (1 + k) / (1 + B), tek yönlü.
  - Aile p'si iki türün büyüğüdür, %0,5 masrafla.
- [ ] Güven aralığı ve örneklem:
  - Blok bootstrap, blok = max(20, ortalama tutma süresi); aralık 2,5–97,5. Aralık yalnız rapordur.
  - Saptanabilir en küçük etki günlük seriden hesaplanır.
  - Örneklem şartları TASARIM 5.9'daki gibidir.
- [ ] Holm:
  - `deneme` satırlarının ilk resmi p'si kullanılır.
  - Karar kabul anındaki m ile donar.
  - Rapor başlığında m ve tarih yazılır.
- [ ] Ölçütler ve sonuç:
  - 6 ölçüt TASARIM 5.12'deki gibidir; tamamlanmamış yıl paydadan çıkar.
  - Portföy kuralı (düşüş %25, 12 ay) yalnız ret yönünde uygulanır.
  - "Ölçülemedi" ayrı bir sonuçtur.
- [ ] Testler `kosu()` yüzünden:
  - Holm elle örneği: [0,01; 0,04; 0,03; 0,005] → [0,03; 0,06; 0,06; 0,02]
  - p tabanı
  - Ölçülemedi yolu
  - kabul tablosu satırları
  - durum yazımı
