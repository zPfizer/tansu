# Tansu mimarisi: önce sistem, en son ölçüm

Status: needs-triage

Levent 10.10: "İlk önce sistemi kuracağız. Ölçümleri en sona bırakacağız." Yavaş ve sırayla ilerlenir.
"Ölçüm" burada getiri sınamasıdır (geçmiş veride kural işe yarar mı). Bir parçanın çalıştığını gerçek veriyle
göstermek ölçüm değildir; o, Definition of Done'ın parçasıdır ve her adımda yapılır.

## Yapılacaklar

1. [ ] Sistemin katmanlarını belirle. → Levent onaylar.
2. [ ] Var olan her katmanı Definition of Done ve kodlama standartlarıyla denetle. Bağımsız denetçi yapar.
       Her katman için kanıtla yaz: tamamlandı ya da eksik, eksikse ne eksik.
3. [ ] Kaynak haritası: 5 defter ve X arşivinin 218 notu katmanlara dağıtılır. Bağlanmayan not gerekçeyle "dışarıda".
4. [ ] Mimari belge: her katmanın girdisi, çıktısı, kurallar ve kaynakları; veri akışı; Levent'in akşam ekranı.
       Yorumlar tek yerde toplanır. → Levent onaylar.
5. [ ] Eksik katmanları sırayla kur. Her katman Definition of Done ile kapanır.
       - Kodu hiç olmayan sekiz karar (`.scratch/arsiv/belge-hizasi/denetim/tasarim-kod.md` §1, bilet 08, 15.10), ilgili katmanla
         birlikte kurulur: (1) kayıt, sadakat kontrolünden sonra; (2) kâğıt dönemi en az 6 ay ve 30 işlem, 12 ayda
         dolmazsa Ölçülemedi; (3) canlı durumu; (4) karantina maskesi K2'ye de; (5) `duzeltme` satırı asıl satırı
         değiştirmez; (6) yakalanmayan istisna günlüğe yazılır; (7) ölçüt değişirse ayrılmış dönemler sıfırlanır;
         (8) "Uyarı yok" satırı ve bulunamayan sembollerin uyarısı. §1'in 9. maddesi (blok uzunluğu ve masraf
         senaryoları günlükte ayrı alan) 07f ile kapandı (TASARIM 5.8): blok uzunluğu çıktıdır, günlük alanı değildir.
6. [ ] En son: ölçüm. Bütün hat ve her katman geçmiş veride sınanır.
7. [x] Kod biçimi: `ruff format` uygulandı (6f1012f). Kalan: geniş ruff kural seti (115 uyarı, ölçüm tarihi ve kural seti yazılmamış); ayrı bir PR.

## 1. Katmanlar (taslak, Levent onayı bekliyor)

Sıra veri akışıdır: her katman bir üstündekini besler.

| # | Katman | Ne yapar | Bugün kodda karşılığı |
|---|---|---|---|
| 1 | Veri | Fiyatı indirir, kontrol eder, değişmez kopyaya koyar | var |
| 2 | Evren | O gün taranabilecek hisseleri belirler | var |
| 3 | Ortak hesaplar | Ortalama, oynaklık gibi herkesin kullandığı hesaplar | var, kısmen |
| 4 | Piyasa havası | Piyasa sakin mi, şokta mı; şokta yeni alımı durdurur | yalnız etiket |
| 5 | Seçim (momentum) | Bütün hisseleri güce göre sıralar, listeyi daraltır | yok |
| 6 | Kurulum tarayıcıları | Listede bölge, formasyon, kırılım ve teyit arar | yalnız EMA sıkışması |
| 7 | Çift | İki hisse arasında ucuz olana geçer | var, bizim okumamız |
| 8 | Risk ve çıkış | Pozisyon büyüklüğü, stop, kademeli çıkış | basit hali |
| 9 | Kart ve takip | Her fırsatı kart yapar, durumunu her gün günceller | var |
| 10 | Senin ekranın | Akşam tablosu, durum dosyası, rapor | var |
| 11 | Çalıştırma | Her akşam ve her ay sensiz çalışır | var |
| — | Değerleme | Bilançoya göre ucuz/pahalı | yok; bilanço verisi yok |
| — | Ölçüm | Geçmiş veride sınama | var; en sona bırakıldı |

Kaynak: Tansu'nun hatları `docs/strateji-taslak/tasarim-8.md` §1; bugünkü modüller `docs/TASARIM.md` §4.
