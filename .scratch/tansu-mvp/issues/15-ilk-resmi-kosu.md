# 15: İlk resmi koşu ve kâğıt üstü dönemin başlaması

**What to build:** İki aile kayda alınır (`kayit`). Ardından `sinama --son` ile ilk resmi koşu yapılır.
Rapor üretilir ve her ailenin durumu yazılır: Deneme ya da Kâğıt. Kâğıt aile varsa günlük kartlar başlar
ve kâğıt üstü dönem saati işler. Levent sonucu tek sayfada okur.

**Blocked by:** 13, 14

**Status:** done (gece koşusu kutusu hariç)

- [x] Ön şartlar sağlanır:
  - sadakat sonuçları `docs/sadakat.md`'de
  - boru hattı denetimi geçti
  - git ağacı temiz
- [x] Kural kaydı yapılır. Kayıt tarihi, yeni ayrılmış dönemin başıdır.
- [x] `sinama --son` koşar. Rapor ve işlem CSV'si üretilir. Deneme günlüğünde `resmi:true` satırları oluşur.
- [x] Rapor sonucu olduğu gibi gösterir. "Hiçbir aile geçmedi" de geçerli bir sonuçtur. Sonuç Levent'e
      teknik olmayan dille bildirilir.
- [ ] Görev Zamanlayıcı etkinleştirilir ve ilk gece kendiliğinden çalıştığı doğrulanır.
  - Etkinleştirildi (aşağıda). İlk otomatik koşu: 06.10 19:30 sonrası doğrulanacak.

## Comments

**İlk resmi koşu (05–06.10.2026).** Hiçbir aile geçmedi; ikisi de Deneme.

- Koşu: `20261005T205624-cdc34e`. Anlık görüntü: `veri/ag/20261005-1949` (komut kendisi seçti). Kod hash'i:
  `c2d080d729bf8b40546469bc56a71e3692756f4e480683cb0f15f103267d6d88`. Kural kimliği: `a3ba880f3e82a57d`. Özet `662d01d49c9e`.
- Süre: `sinama --resmi --son` (B = 1.000) 23:56:22 – 00:03:06 = **6 dk 44 sn**. Denetim (`python -m tansu denetim`) ~38 dk, geçti
  (EMA yanlış kabul 0/200, çift 0/200).
- Commit sırası: 1e7c4a0 denetim, f077c16 kural kaydı, 9b9c3f1 resmi koşu satırları. Rapor ve CSV `rapor/`'da (git'e girmez):
  `rapor-20261005T205624-cdc34e.html`, `islemler-20261005T205624-cdc34e.csv`, `cift-islemler-20261005T205624-cdc34e.csv`.

| Aile | Ham p | Holm p (m = 2) | Durum |
|---|---|---|---|
| EMA sıkışması | 0,7263 (a 0,7263; b 0,3197; ek kol 0,5594) | 1,0000 | Geçmedi, **Deneme** |
| Çift rotasyonu | 0,9441 | 1,0000 | Geçmedi, **Deneme** |

Altı ölçüt:

| # | Ölçüt | EMA | Çift |
|---|---|---|---|
| 1 | K1'e göre fazla getiri pozitif, Holm p < 0,05 | Geçmedi (+%9,84; Holm 1,0) | Geçmedi (−%8,98; Holm 1,0) |
| 2 | K2'ye göre portföy fazla getirisi pozitif | Geçmedi (günlük −%0,01) | Geçmedi (günlük −%0,03) |
| 3 | %0,5 masrafta da 1 ve 2 | Geçmedi | Geçmedi |
| 4 | Yılların %60'ı pozitif; en iyi %5 atılınca pozitif | Geçmedi (yıl %30; −%11,40) | Geçmedi (yıl %10; −%12,40) |
| 5 | Örneklem 100 işlem / 60 gün ve sağlamlık ≥ %60 | Ölçülemedi (91 işlem, 90 gün; sağlamlık %85,19) | Ölçülemedi (91 / 89 gün; sağlamlık %0,00) |
| 6 | Kâğıt dönemde etki doğrulamanın yarısı | Ölçülemedi (kâğıt dönem yok) | Ölçülemedi |

Kural getirisi %0,3 masrafta: EMA %2062 (K2 %2997), çift %924 (K2 %2438). Portföy kuralı iki ailede de reddetti. Kâğıt aile yok:
günlük kart ve kâğıt dönem saati başlamaz.

**Beklenmeyen:** rapor "Veri durumu: SORUNLU" der (kaynak günü hataları 2010-11-15, 2010-12-21, 2011-08-29, 2016-01-26,
2026-05-21; olay denetimi farkı üye oranı %1,94, eşik %2,00 sınırda). Karantina %0,16. Kapı koşuyu durdurmadı. İşlem sayısı 91
(örneklem şartı 100) ölçüt 5'i Ölçülemedi bıraktı.

**Görev Zamanlayıcı:** `TansuGunluk` ve `TansuAylik` etkinleştirildi (`Get-ScheduledTask`: ikisi **Ready**). Sonraki koşular:
TansuGunluk 06.10.2026 19:30, TansuAylik 31.10.2026 20:45. İlk otomatik koşu: 06.10 19:30 sonrası doğrulanacak.
