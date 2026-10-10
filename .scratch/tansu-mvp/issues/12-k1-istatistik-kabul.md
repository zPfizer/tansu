# 12: K1, istatistik, Holm ve kabul tablosu

**What to build:** `sinama` her aileyi eşleştirilmiş rastgele kuralla (K1) karşılaştırır. Ardından:
- p değeri, güven aralığı ve saptanabilir en küçük etki hesaplanır.
- Bütün resmi denemeler üzerinden Holm uygulanır.
- Rapor her aile için 6 ölçütlük geçti/kaldı tablosunu verir: Geçti, Geçmedi ya da Ölçülemedi.
- Aile durumu (Deneme veya Kâğıt) `kayit`'a yazılır.

**Blocked by:** 11

**Status:** done

- [x] K1:
  - Ön şartlar KURALLAR §3'teki gibidir.
  - (a) türü: aynı gün başka hisse; sayı gün başına korunur.
  - (b) türü: aynı hisse, aynı piyasa durumu, ±20 gün.
  - EMA için ek kol: sıkışmasız kırılım.
  - Çift için: aynı sayıda rastgele geçiş, ilk giriş gerçeğe eşit.
  - Rastgele işlemler aynı simülatörden ve aynı filtrelerden geçer.
  - Uygun gün yetmezse hata verilir.
- [x] Tekrar sayısı ve p:
  - B ≥ max(1.000, 200·m); geliştirmede 200 ve bu p Holm'a girmez.
  - p = (1 + k) / (1 + B), tek yönlü.
  - Aile p'si iki türün büyüğüdür, %0,5 masrafla.
- [x] Güven aralığı ve örneklem:
  - Blok bootstrap, blok = max(20, ortalama tutma süresi); aralık 2,5–97,5. Aralık yalnız rapordur.
  - Saptanabilir en küçük etki günlük seriden hesaplanır.
  - Örneklem şartları TASARIM 5.9'daki gibidir.
- [x] Holm:
  - `deneme` satırlarının ilk resmi p'si kullanılır.
  - Karar kabul anındaki m ile donar.
  - Rapor başlığında m ve tarih yazılır.
- [x] Ölçütler ve sonuç:
  - 6 ölçüt TASARIM 5.12'deki gibidir; tamamlanmamış yıl paydadan çıkar.
  - Portföy kuralı (düşüş %25, 12 ay) yalnız ret yönünde uygulanır.
  - "Ölçülemedi" ayrı bir sonuçtur.
- [x] Testler `kosu()` yüzünden:
  - Holm elle örneği: [0,01; 0,04; 0,03; 0,005] → [0,03; 0,06; 0,06; 0,02]
  - p tabanı
  - Ölçülemedi yolu
  - kabul tablosu satırları
  - durum yazımı

## Comments

Kod: `tansu/istatistik.py` (yeni, `KOD_DOSYALARI`'nda: Holm, p, blok bootstrap, saptanabilir etki, `EmaK1`, `CiftK1`, `kabul`),
`aileler` (`on_sart`, `uygun_gunler`, `sikismasiz_kirilim`), `gostergeler.piyasa_durumu`, `motor.Zincir` (K1 için tek işlem
önbellekli zincir; `islemler` ile bire bir, 14 senaryoda test), `simulator` (`k1_baglam`, `k1_islemler`, `_suzgec`),
`ciftbolme.hazirla`, `kayit` (`holm_hesapla`, `tekrar_sayisi`, `durum_oku`, `durum` satırları), `rapor` kabul bölümü,
`sinama --son`. Test: 204 yeşil (önce 143). Belge önce: TASARIM 5.7 "K1 uygulama kuralları", 5.9, 5.11, 5.12
"Ölçütlerin uygulanışı"; KURALLAR §3 (ek kol 20 gün YORUM); GLOSSARY.

**Belge boşluğu kararları (gerekçeli, TASARIM'da):** sepet getirisi tanımı; Holm birimi (kural × aile); `durum` satırı;
MDE yıllık ve işlem başına karşılaştırma; ölçüt yorumları. Gerçek veri iki düzeltme istedi: (b) türü önce sıkışma penceresi
şartıyla TCELL 2019'da durdu; hisse düzeyi uygun gün şartına çekildi (getiri görülmeden, kural parametresi değişmedi).
Sonra ULKER 19.03.2021 komşusuzdu: komşusuz sinyal (b)'den düşer, sayısı `komsusuz` (şimdi 1/74) yazılır.

**Geliştirme koşusu** (`resmi:false`, B=200, tohum 0, anlık görüntü 20261005-1949, günlük repo dışında): **7 dk 0 sn**
(EMA/çift gerçek koşusu ≈ 3,3 dk + 4 K1 kolu × 200). Ticket 13'ün 200 tekrar için ≤ 5 dk bütçesi aşılıyor: hızlandırma orada.
- EMA: 74 sinyal, 67 işlem; gerçek K1 fazla getiri %0,5'te +%14,7 işlem başına (kuyruk işlemler; medyan bakılmadı); p_a 0,687,
  p_b 0,144, ek kol 0,488; aile p 0,687; Holm p 1,0 (varsayımsal m=2). Sonuç Geçmedi (ölçüt 1), Deneme.
- Çift: 82 tutuş, 80 gün (< 100/60: örneklem dolmuyor); gerçek fazla %0,5'te −%10,0; p 0,945.
- Gerçek tam B (`--son`) koşulmadı; resmi koşu yok. `--son` yalnız tmp kayıtla test edildi (B = max(taban, çarpan·m)).

**Açık işler:**
- Ölçüt 5 sağlamlık oranı: bilet 13 (şimdi `saglamlik=None` → Ölçülemedi; bu yüzden hiçbir aile Kâğıt olamaz). Ölçüt 6 kâğıt dönemi yok.
- Hız: 200 tekrar 7 dk; tam B ≥ 1.000 → ≈ 25–30 dk tahmini (doğrusal; ölçülmedi).
- Veri: 21.05.2026 toplu bozuk gün (`kaynak-gunu` dalı) 2026 sonuçlarını etkiler.
- Karar: sepet getirisi AOF yerine kapanış-gecikmeli yaklaşıklık; MDE işlem başına dönüşümü YORUM.
- 09'dan açık: ham p, masraf düzeyi sonuçları ve `--son` artık `bitti` satırında (`k1`, `tekrar`, `son`).
- 11'den: 100/60 örneklem kuralı çift için 82/80 ile ölçülemedi yolunu tetikler (kural 5.9 aynen).
