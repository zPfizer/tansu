# 10: Tek hisse simülatörü + faiz + K2 + ilk HTML rapor

**What to build:** `sinama`, EMA sıkışması ailesini 2015–2026 evreninde tek sürekli portföy olarak koşar.
Çıktılar:
- sermaye eğrisi
- maruziyet eşleşmeli K2 karşısında fazla getiri
- yıllara göre sonuçlar
- tek dosya HTML rapor ve işlem CSV'si

Rapor Levent'in açıp okuyabileceği ilk somut çıktıdır. Henüz p değeri yoktur.

**Blocked by:** 07, 09

**Status:** done

- [x] Boyutlandırma:
  - Adet şu dördünün en küçüğüdür, aşağı yuvarlanır: %1 risk adedi, %10 tavan, %2 likidite, nakit /
    (fiyat × (1 + masraf)).
  - En fazla 10 pozisyon. Yer yetmezse en likit önce, eşitlikte alfabetik.
  - Aynı gün önce çıkışlar, sonra girişler işlenir.
  - Reddedilen sinyaller ayrıca sayılır.
- [x] Masraf %0,1 / %0,3 / %0,5. Boştaki nakit bir gün gecikmeli politika faizi kazanır.
- [x] K2:
  - Ay başında evrenle eşit ağırlıklı kurulur, AOF'tan AOF'a.
  - Ay başı dengelemesi %0,3 masraf öder.
  - Günlük maruziyet kuralınkine eşitlenir; kalan nakit faiz kazanır.
- [x] Rapor:
  - Başlıkta koşu kimliği, anlık görüntü ve kod hash'i yazılır.
  - "Tansu'dan esinlenen yorum" uyarısı bulunur.
  - Yıllık fazla getiri tablosu vardır.
  - Tek bir "Uyarılar" bölümü vardır: karantina, tavan ve likidite bağlama oranları, iptal ve
    reddedilen sinyaller.
  - Ayrıca `islemler-<koşu>.csv` yazılır.
- [x] Testler `kosu()` yüzünden, küçük sentetik anlık görüntüyle:
  - boyutlandırmanın dört sınırı
  - lot yuvarlama
  - faiz tahakkuku
  - K2 maruziyet eşleşmesi
  - yasaklı sözcük denetimi (AL, SAT, ÖNERİ, "Tansu'nun sistemi")
  - CSV sütunları


## Comments

- Yeni dosyalar: `tansu/simulator.py` (kural kaydına girdi, `KOD_DOSYALARI`), `tansu/rapor.py` (hash dışı).
  `kosu(..., bas=simulator.BASLANGIC)` simülatörü ve raporu koşar; `bitti` satırına `masraf_sonuc` ve `veri_sorunlari` yazar.
  `veri.Anlik`: `gun_tablosu`, `gunler`, `olay_uyarilari` artık `cached_property` (motor sembol başına çağırıyordu);
  yeni `oranlar(uye)` ve `sorunlar_uye(uye)`. `motor` işlem tablosuna `sinyal_tarih` eklendi. Test 128 yeşil.
- Belge önce (TASARIM 5.13, 5.6, 5.7, 6.8): veri kapısı oranları yalnız evren üyesi hisse-günlerde; eşik değerleri aynı.
  Simülatör kuralları 5.6'ya yazıldı (özkaynak = önceki kapanış, faiz gece tahakkuku, evren süzgeci, kapanma −%100).
- **Gerçek koşu** (geliştirme, `resmi:false`, anlık görüntü `20261005-1726`, 205 sn, tam paket; geliştirme günlüğü repo dışında
  tutuldu, `kayit/` commit'lenmedi):
  - Kapı oranları, evren üyeleri (271.680 hisse-günü, 275 sembol): karantina **%0,23** (eşik %1), olay denetimi farkı
    **%1,94** (eşik %2). İkisi de eşik altı: kapı TAMAM. Tüm evrende (eski ölçü): %3,00 ve %4,15.
  - Olay oranı eşiğe yakın: üye günlerdeki 5.276 farkın hepsi, olay tablosu boş dönen 13 üye sembolde (tüm evrende 90 sembolün
    tablosu boş). Bu 13 sembolün farkı çıkarsa üye oranı %0'a düşer.
  - Motor (tüm semboller): 417 işlem (241 stop, 145 sma250, 30 karantina, 1 veri sonu), 7 iptal, NaN yok.
    Alınan 67 işlemin hepsi giriş = ertesi gün AOF (kontrol edildi, 67/67); sinyal-giriş farkı en az 1 gün.
  - Simülatör, %0,3: 67 işlem, 0 reddedilen. Bağlayıcı sınır: tavan 54, likidite 12, nakit 1, risk 0. Ortalama planlanan risk
    / özkaynak %0,48. Karantina çıkışı 2. Ortalama yatırım payı %32,5.
  - Son özkaynak (başlangıç 1.000.000): %0,1 → 20,89 M; %0,3 → 20,42 M; %0,5 → 19,95 M. K2: 28,13 / 28,16 / 28,19 M.
    Yani kural K2'nin altında (%0,3'te 2026 dahil kümülatif). Yıllık fazla getiri (%0,3): 2015 −0,2; 2016 0,0; 2017 −13,5; 2018 −1,0;
    2019 −11,9; 2020 −21,8; 2021 +3,0; 2022 −22,7; 2023 +32,5; 2024 +12,5; 2025 −7,2; 2026 −7,9 puan. Henüz p değeri yok.
  - **Kapanma (−%100) sayısı:** 95 kapanan hissenin 1'i alınan işlemi açıkken kapandı (TRKCM, 02.06.2020 giriş, 24.12.2020 kapanma).
    Kapanma nedeni listesi hâlâ bağlı değil (bilet 07 açık işi).
- Açık: motor evren süzgecinden önce çalışır; evren dışı ya da reddedilen sinyal motorda pozisyon sayılır, aynı hissede sonraki
  sinyali geciktirebilir (TASARIM 5.6'da yazılı yaklaşıklık). Düşen sinyal sayısı (7) tüm sembollerdedir.
- Açık: K1, p değeri, Holm (bilet 11-12). Tek işlem +%1.234'e kadar çıkıyor (TUPRS 2021, sma250 çıkışı); düzeltilmiş fiyattan,
  veri hatası belirtisi yok ama bu uç değer ortalama getiriyi şişirir.
- Açık: faiz serisi 2010'dan 23.01.2026'ya, 57 değişim; son değişimden sonraki gün ileri doldurulur.
- Süreç notu: hacim 0,02 × medyan TL için `hacim` sütunu TL kabul edildi (TASARIM 5.1).
