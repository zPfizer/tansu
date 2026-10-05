# 15: İlk resmi koşu ve kâğıt üstü dönemin başlaması

**What to build:** İki aile kayda alınır (`kayit`). Ardından `sinama --son` ile ilk resmi koşu yapılır.
Rapor üretilir ve her ailenin durumu yazılır: Deneme ya da Kâğıt. Kâğıt aile varsa günlük kartlar başlar
ve kâğıt üstü dönem saati işler. Levent sonucu tek sayfada okur.

**Blocked by:** 13, 14

**Status:** ready-for-agent

- [ ] Ön şartlar sağlanır:
  - sadakat sonuçları `docs/sadakat.md`'de
  - boru hattı denetimi geçti
  - git ağacı temiz
- [ ] Kural kaydı yapılır. Kayıt tarihi, yeni ayrılmış dönemin başıdır.
- [ ] `sinama --son` koşar. Rapor ve işlem CSV'si üretilir. Deneme günlüğünde `resmi:true` satırları oluşur.
- [ ] Rapor sonucu olduğu gibi gösterir. "Hiçbir aile geçmedi" de geçerli bir sonuçtur. Sonuç Levent'e
      teknik olmayan dille bildirilir.
- [ ] Görev Zamanlayıcı etkinleştirilir ve ilk gece kendiliğinden çalıştığı doğrulanır.
