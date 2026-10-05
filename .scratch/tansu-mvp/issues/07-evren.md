# 07: Evren

**What to build:** `evren(tarih)` o gün yeni giriş için taranabilecek hisseleri döndürür. Kural şudur:
1. Ayın ilk işlem gününde, önceki ayın son kapanışındaki piyasa değerine göre sıralama yapılır.
2. 60 günlük medyan TL hacimde en alttaki %20 elenir.
3. Kalanlardan en büyük 100 hisse alınır.
4. Aynı şirketin birden çok kodu varsa yalnız biri kalır.

Bunun için bütün sembollerin verisi indirilir; işlemi kapanmış semboller de buna dahildir.

**Blocked by:** 03, 04

**Status:** ready-for-agent

- [ ] Sembol listesi şunlardan oluşur: bugünkü bütün paylar (borsapy) ve KAP'tan bulunabilen işlemi kapanmış
      kodlar. Bulunamayanlar listelenir.
- [ ] Anlık görüntü bütün evren adaylarını içerir. İlk indirmenin süresi ölçülür ve yazılır.
- [ ] Şirket başına tek kod kuralı uygulanır. Bilinen çoklu kodlar elle yazılmış bir listede tutulur.
- [ ] Kapanma kuralları:
  - 60 işlem gününden uzun durdurma kapanma sayılır.
  - Kapanan hissedeki pozisyon −%100 sayılır; neden biliniyorsa son fiyat kullanılır.
- [ ] Testler `kosu`'ya giden sentetik anlık görüntüyle:
  - ay başı sıralama
  - geleceği görmeme (önceki ay sonu verisi)
  - likidite eleği
  - tek kod
  - kapanma
