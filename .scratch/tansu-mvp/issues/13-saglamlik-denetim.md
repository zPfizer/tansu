# 13: Sağlamlık ızgarası, boru hattı denetimi ve geleceği görmeme testi

**What to build:**
- `sinama` her ailenin önceden yazılmış ızgarasını (KURALLAR §3) koşar ve pozitif hücre oranını raporlar.
  Şart: ≥ %60.
- Boru hattı iki kez denetlenir: sentetik boş veriyle (yanlış kabul ≤ %5) ve enjekte edilmiş etkiyle (güç).
- Bir test "veriyi t'de kes, t öncesi sinyaller ve evren değişmesin" der.

**Blocked by:** 12

**Status:** done

- [x] Izgara hücreleri `tur=destek` olarak günlüğe yazılır ve Holm m'ye girmez. Pozitif = K1'e göre ortalama
      fazla getiri > 0, %0,3 masrafla.
- [x] Boru hattı denetimi bir komutla koşar. Sonucu rapora ve `docs/`'a yazılır. Yanlış kabul > %5 ise
      ilk resmi koşu yapılmaz.
- [x] Geleceği görmeme testi parametriktir. Kapsadığı yerler: evren, göstergeler, iki ailenin sinyalleri,
      çift seçimi, likidite medyanı, faiz hizalaması.
- [x] Süre ölçülür ve yazılır: 200 ve tam B tekrarının süresi. TASARIM'daki bütçe 200 tekrar için ≤ 5 dk.
      Aşılırsa önce algoritma hızlandırılır.

## Comments

Kod: `tansu/saglamlik.py` (yeni, `KOD_DOSYALARI`'nda: EMA 27 ve çift 18 hücre, `oran`), `tansu/denetim.py` (yeni, hash dışı:
sentetik dünya, etki gömme, tekrarlar, rapor), `kayit` (`hesapla` = `kosu`nun günlüksüz çekirdeği; `denetim_yaz`,
`denetim_gecti`, ilk resmi koşu kapısı; ızgara `destek` satırları; ölçüt 5'e sağlamlık), `ciftbolme` (`adaylar`, `sec`,
`setler_sec`, `hazirla(aday_esik)`, eşbütünleşme yıllara paralel), `motor` (`mumlar` önbelleği, `Zincir.kapali`, `sinama` Zincir
ile), `simulator._kural` (sözlük erişimi), `istatistik` (`cift_tablo`, `EmaK1.ek_eksik`, tek tablo), `__main__ denetim`.
Test: 256 yeşil (tam paket 52–60 sn; bu bilet + yeni dosyalar `test_saglamlik`, `test_denetim`, `test_gelecek`). Belge önce:
TASARIM 4 (modül tablosu, bağımlılık yönü), 5.7 (ek kol, süre), 5.8 (hash kapsamı), 5.10 (uygulama), 5.11 (`destek` satırları),
5.12 (ölçüt 5, denetim, geleceği görmeme), GLOSSARY. Birleştirme: `tansu-mvp` (bilet 14) iki kez; çakışmalar `kayit`, `__main__`,
TASARIM modül tablosu.

**Belge boşlukları kararları (gerekçeli, TASARIM'da):**
- Pozitif hücre = K1 istatistiğinin kendisi (işlem başına sepete göre fazla getiri, %0,3) > 0; "K1'e göre" hücrede rastgele tekrar
  koşmak değil (p aranmaz). İşlemi olmayan hücre NaN, pozitif değil. Izgara her K1'li koşuda (dev dahil) hep koşar.
- Yanlış kabul = boş dünyada ölçüt 1–4 Geçti ve portföy kuralı reddetmedi (örneklem ve sağlamlık aranmaz; Kâğıt alt küme). Sebep:
  sentetik dünya 100 işlem örneklemini dolduramayabilir, o zaman Kâğıt oranı boş yere 0 çıkar. Kâğıt oranı da raporda. Holm m = 2.
- Etki = sinyali izleyen günün AOF'unun 1+etki'ye bölünmesi. Kalıcı fiyat kayması denendi ve bırakıldı: sinyalden önce giren
  rastgele işlem de kazanıyor, K1 etkiyi görmüyordu (EMA %20 etkide bile p_a 0,40).
- K1 ek kol (yalnız rapor): havuz sinyal sayısından küçükse havuz kadar çeker, eksik `ek_eksik` olarak sayılır. Gerekçe: gerçek
  veride 21.09.2026'da hiçbir üye 20 günlük yükseğin üstünde kapatmadı; bilet 12 koşusu bu veriyle `K1Hatasi` ile duruyordu
  (bilet 12'deki "ek kol 0,488" bu kodla yeniden üretilemedi: ek_eksik 4, p_ek 0,547 B=200).
- `EmaK1`: aynı hissenin aynı güne iki sinyali (örtüşen sıkışma pencereleri) tek sayılır; sentetik dünyada (a) havuzu "yetmiyor"
  diye `K1Hatasi` verdi. Gerçek veride sonuç değişmedi (aynı `özet`).
- Ölçüt 5 örneklem sayımı değişmedi.

**Süre** (`python -m tansu sinama`, gerçek veri 20261005-1949, `resmi:false`, 32 çekirdekli geliştirme makinesi, günlük repo dışında):
- Önce: B = 200 **7 dk 0 sn** (bilet 12 ölçümü, ızgarasız). Profil (tek süreç, yüklü makine): `motor.sinama` 78 sn, eşbütünleşme
  (`hazirla`) 80 sn, EMA K1 B=200 290 sn, çift K1 B=200 17 sn; yeni ızgara aynı kodla 308 sn eklerdi (EMA 67, çift 241).
- Sonra (ızgaralar dahil, iki ölçüm): B = 200 **2 dk 52 sn ve 3 dk 03 sn** (bütçe ≤ 5 dk tutuyor); tam B = 1.000 (m = 2, resmi
  büyüklükte, `sinama --son`, `resmi:false`) **6 dk 48 sn ve 6 dk 50 sn**. Ticket 15'in tam koşusu bu sürede biter (+ `denetim` ayrı komut).
- Ne değişti: `sinama` önbellekli `Zincir` ile (78 → 16 sn); mum tablosu anlık görüntü başına bir kez; K1 `_kural` pandas skaler
  erişimi yerine sözlük; K1 işlem tablosu tek parça; eşbütünleşme yıllara paralel ve ızgara için en geniş eşikte bir kez;
  istatistik ve B değişmedi. Doğrulama: B=200'de aynı tohumda aynı p (EMA 0,7065, çift 0,9254) ve aynı `özet` (iki koşu).
- Not: eşbütünleşme havuzu `python -m tansu` altında çalışır; `python -` ile stdin'den başlatılan betikte Windows `spawn`
  `<stdin>` yolunu açamaz (araç sınırı, kod değil).

**Gerçek veri geliştirme sonucu** (B = 200, tohum 0; resmi değil, Holm varsayımsal):
- Sağlamlık: EMA **%85,2** (23/27 pozitif hücre; en kötü −%3,2, en iyi +%25), çift **%0** (0/18; hepsi −%4,7 … −%11,3).
- Her iki aile Deneme: ölçüt 1–4 Geçmedi (EMA K1 p 0,7065 [p_a 0,7065, p_b 0,308]; çift 0,9254), ölçüt 5 Ölçülemedi (EMA 91 alınan
  işlem < 100; çift 80 gün < 100/60), ölçüt 6 Ölçülemedi. Yani ızgara bağlandı ama bu veride hiçbir aile Kâğıt'a yaklaşmıyor.
- K1 (a) türü havuzu küçük: gerçek veride gün başına havuz / sinyal sayısı medyan 2,0 ve günlerin %43'ünde havuz = sinyal sayısı
  (rastgelelik yok). Sentetik denetimde bu yüzden gerçek bir etkiyi görmek için %10 işlem başı avantaj gerekiyor (aşağıda).

**Boru hattı denetimi** (`python -m tansu denetim`, 200 boş + her aile × etki düzeyi 20 etkili dünya, 125 hisse × 2.000 gün, K1 B = 200,
Holm m = 2; süre 39 dk 8 sn; sonuç `docs/denetim.md`, `rapor/denetim-*.html`, günlükte `tur=destek, olay=denetim`):
- **Yanlış kabul: EMA 0/200, çift 0/200 (ölçüt 1–4 ve Kâğıt). Şart ≤ %5: GEÇTİ.**
- Güç (ölçüt 1–4 / Kâğıt): EMA %5 etkide 5/20 (Kâğıt 5), %10'da **20/20** (Kâğıt 20); çift %5'te 4/20, %10'da 9/20 (Kâğıt 0:
  sentetik 5,7 yılda ≈ 60 geçiş, örneklem şartı 100). Yani EMA hattı %10 avantajı hep bulur ve Kâğıt'a geçirir; çift hattı
  güçsüz (örneklem yetmiyor).
- Kapı: `kosu(resmi=True)` ilk resmi koşuyu, bu kod hash'iyle geçmiş denetim yoksa durdurur (başarısız denetim de engeller). Dev
  günlüğünde (repo dışı) geçen denetim satırı var ama `kayit/` commit'lenmedi: **bilet 15 son koduyla `python -m tansu denetim`'i
  yeniden koşmalı** (39 dk 8 sn, ben aynı anda paketi koşarken; boş makinede daha kısa, ölçülmedi). Hash'e giren her dosya değişirse yeniden gerekir.

**Geleceği görmeme testi** (`tests/test_gelecek.py`, 18 test = 6 bileşen × 3 kesim günü, sentetik 24 hisse × 900 gün): evren, göstergeler
(EMA, SMA, ATR, sıkışma oranı, piyasa durumu), EMA sinyali ve ön şartları, çift Z ve hedef, çift seçimi, likidite medyanı + faiz
hizalaması + K2 sepeti (`simulator.zemin`). Duyarlılık: SMA'yı ortalı pencereye ve Z'yi 1 gün öne çeviren mutantlar yakalandı. Bu
kodda sızıntı bulunmadı.

**Açık işler:**
- Bilet 15: `denetim`'i son koda karşı koş; `sinama --son --resmi` (B = 1.000, ≈ 7 dk). Resmi koşu EMA'da örneklemi doldurmayabilir
  (91 alınan işlem).
- Çift ailesi sağlamlıkta %0 ve K1 p 0,93: bu veride desteksiz. EMA K1 (a) türü gücü düşük (yukarıda); kural kararı değil, ölçüm notu.
- Veri: 21.05.2026 bozuk gün (`kaynak-gunu`) 2026 sonuçlarını etkiler (bilet 12'den).
- Karar bekleyen: `denetim.py` hash dışı bırakıldı (kuralı değil sınamayı ölçer); istenirse `KOD_DOSYALARI`'na alınır (o zaman denetimden sonra
  değiştirilemez, denetim kodu da kural kaydına girer).
