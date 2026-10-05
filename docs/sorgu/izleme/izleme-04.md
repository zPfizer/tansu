# İzleme 04: Çift rotasyonu (cevaplar-04-cift.md, taslak 6'ya karşı)

04-001 — YANLIŞ — YENİ — KURALLAR §3 madde 1 sapma satırına "α yok; ortalama çıkarıldığı için Z aynıdır" notu ekle.
04-002 — EKSİK — YENİ — KURALLAR §4'e tolerans yaz: "üretti" = Z ±0,0005 (3 ondalık); gevşek bant ±0,05 yalnız tek aday kalırsa.
04-003 — EKSİK — YENİ — KURALLAR §4'e yaz: rapor tarihi bilinmez; (Z_t, Z_{t−1}) çifti tüm işlem günlerinde aranır, eşleşen günler yazılır.
04-005 — EKSİK — RED — Z her gün pencereden hesaplanır (Adım aynı, TASARIM 4); iki biçim denemek aşırı kurulum.
04-008 — EKSİK — YENİ — TASARIM 5.6 çift seçimine "252 gün seçim penceresi YORUM; Z penceresinden bağımsız" ekle.
04-009 — EKSİK — RED — Yarı ömür tanısı aşırı kurulum; kaynak yok.
04-010 — EKSİK — VAR — TASARIM 5.6 ("X/Y rolü sembol sırasından"), sonuc B-10.
04-011 — EKSİK — VAR — TASARIM 5.6 ("β ≤ 0 olan çift elenir"), sonuc B-10.
04-012 — EKSİK — RED — Tanısal β CV sütunu aşırı kurulum; β türü ve pencere 5.10 ızgarasına (04-089) bağlı.
04-015 — EKSİK — RED — ΔZ dağılım raporu aşırı kurulum; kaynakta eşik yok.
04-016 — YANLIŞ — VAR — KURALLAR §2 (birinci el: ΔZ tanımı; eksik: "tek gün ΔZ yeterliliği") ve §3 madde 1 (YORUM etiketi), sonuc B-10.
04-017 — EKSİK — VAR — KURALLAR §4 çift satırı ("Mart–Mayıs 2025'te sinyal yok").
04-018 — EKSİK — RED — Üst uçta kalma raporu aşırı kurulum; K §3 kural zaten yazılı.
04-019 — EKSİK — VAR — TASARIM 5.1 ("Hacmi sıfır olan gün işlem günü değildir"), sonuc B-7.
04-021 — EKSİK — RED — Adillik K2 maruziyet eşleşmesiyle çözülü (TASARIM 5.7, sonuc B-13); ek satır aşırı.
04-022 — EKSİK — VAR — TASARIM 5.6 ("her çift payı ilk sinyale kadar nakittedir"; "düşen çiftin pozisyonu kapanır").
04-023 — EKSİK — RED — Faiz ayrı satırı aşırı kurulum; faiz K2'de aynı (B-13), simülatörde zaten var (TASARIM 5.7 K3).
04-024 — EKSİK — VAR — TASARIM 4 Faiz ve sonuc B-8 (tek seri: borsapy politika faizi, 2015'ten; TLREF çıktı).
04-028 — EKSİK — RED — Ertesi yıl p tanısı aşırı kurulum; kabul kararına girmez.
04-029 — EKSİK — YENİ — TASARIM 5.6 Tansu çifti satırına yaz: VAKBN–GARAN sabit çift, tüm dönem, seçim kuralı yok, aynı sinyal ve maliyet kuralı.
04-030 — EKSİK — TEKRAR — 04-029 (ayrıca "üç çift" listesi AGROT çıkınca geçersiz, B-10).
04-031 — EKSİK — VAR — TASARIM 5.6 ("Sıralama: p'ye göre açgözlü; bir hisse en fazla bir çiftte"), sonuc B-10.
04-032 — EKSİK — VAR — TASARIM 5.6 ("Boş pay nakitte kalır"), sonuc B-10.
04-033 — EKSİK — VAR — TASARIM 5.2 Sektör ("Kaba ve tarih bilgisiz; bilinen yanlılık"; "küçük" yok).
04-034 — EKSİK — VAR — TASARIM 5.6 ("evrendeki aynı sektörden") + 5.2 evren; sonuc B-9 (evrenden çıkan hissede pozisyon açık kalır).
04-035 — EKSİK — VAR — TASARIM 5.6 ("her yıl başında", "önceki 252 günde") + 5.3 (sinyal kapanışta, giriş ertesi AOF).
04-036 — EKSİK — VAR — TASARIM 5.8 (genişleyen pencere, 2015–2017 ile başlar) + 5.1 (2010'dan indirme, ısınma).
04-039 — EKSİK — RED — Rolling p kapısı aşırı kurulum; kaynak yok.
04-040 — EKSİK — RED — Kapsam dışı; Tansu'daki yatay çizginin nedeni bilinmiyor, sistem etkilenmez.
04-042 — EKSİK — RED — Çift başına en kötü düşüş ve rolling p raporu aşırı kurulum; m5 bölmede var (5.12).
04-043 — EKSİK — VAR — TASARIM 5.2 ("İşlemi kapanan hisseler"), sonuc B-9.
04-044 — EKSİK — VAR — TASARIM 5.4 (M11 genel, "pozisyon ... %2"); yıl başı rotasyonu hariç tutulmaz.
04-045 — EKSİK — VAR — TASARIM 5.6 ("yine seçilen çift işlemsiz devam eder"), S2-26.
04-046 — EKSİK — TEKRAR — 04-032.
04-047 — EKSİK — TEKRAR — 04-044.
04-048 — YANLIŞ — VAR — KURALLAR §3 Risk paketi ("çift rotasyonu hariç") ve TASARIM 5.5 ("Risk paketi bu bölmeye uygulanmaz").
04-049 — EKSİK — VAR — TASARIM 5.12 (portföy kuralı m5 "aileden bağımsız") + 5.6 (her aile kendi sermayesi).
04-051 — EKSİK — YENİ — TASARIM 5.7 K2 satırına "çift bölmesinde 50/50 yalnız tanısaldır; kabul K2 evren sepetiyle" ekle.
04-052 — EKSİK — VAR — TASARIM 5.7 K1 ("aynı çiftlerde, aynı sayıda geçiş, rastgele günlerde; ilk giriş günü gerçeğe eşit").
04-053 — EKSİK — VAR — KURALLAR §3 madde 1 ("K1 ön şartı: çift seçilmiş ve |Z| ≥ 2 olan günler"); ön şartsız ikinci K1 aşırı.
04-054 — EKSİK — VAR — TASARIM 5.7 K1 (çift bölmesi: aynı çiftlerde aynı sayıda geçiş; çiftler yıllık seçilir).
04-055 — EKSİK — VAR — TASARIM 5.7 K1 ("İlk giriş günü gerçeğe eşitlenir").
04-057 — EKSİK — YENİ — TASARIM 5.7 K2'ye 50/50 tanımı ekle: yılın ilk işlem gününde bir kez al, yıl sonuna kadar tut; günlük dengeleme yok.
04-058 — EKSİK — RED — Oynaklık/beta yan yana tablosu aşırı kurulum; risk farkı K2 maruziyet eşleşmesiyle (B-13).
04-059 — EKSİK — TEKRAR — 04-051.
04-061 — EKSİK — VAR — TASARIM 5.9 (en az 100 işlem ve 60 farklı sinyal günü) + 5.8 (çift bölmesinde günlük fazla getiri serisi).
04-062 — EKSİK — VAR — TASARIM 5.9 ("Blok uzunluğu = max(20, ortalama tutma süresi)"), sonuc B-16.
04-063 — EKSİK — VAR — TASARIM 5.8 (çift bölmesi 6 ayda en küçük etki ≈ %56) + 5.12 "Ölçülemedi", sonuc B-17.
04-064 — EKSİK — RED — Ertesi kapanış dolum duyarlılığı aşırı kurulum; AOF kararı B-3, kayma senaryosu 5.4'te.
04-065 — EKSİK — RED — AOF kararı B-3 ile çelişir; açık soru eklemek gereksiz, 5.4 %0,5 senaryosu kapsar.
04-068 — EKSİK — YENİ — TASARIM 5.6 çift bölmesine yaz: bacaklardan biri kilitliyse geçiş yapılmaz; ertesi gün sinyal yeniden değerlendirilir, eski sinyal taşınmaz.
04-069 — EKSİK — RED — Kapanış-AOF fark dağılımı aşırı kurulum; %0,5 kayma senaryosu 5.4'te.
04-071 — EKSİK — VAR — TASARIM 4 (HGDG brüt temettüyü kapsar) + 5.4 (vergi raporda not), sonuc O2.
04-074 — EKSİK — VAR — TASARIM 6 madde 5 (referans fiyat; çift kartında "simülasyonda şu an X'te"), sonuc B-20.
04-075 — EKSİK — RED — Yahoo tamamen çıktı (B-2); ikinci kaynak karşılaştırması 5.1'de.
04-080 — EKSİK — VAR — KURALLAR §4 (çift: "sapma formülü ve pencere"; birden çok aday denenir) + 5.10 ızgarası.
04-081 — EKSİK — RED — Pair Quality formülü yok, tanısal sütun aşırı kurulum.
04-082 — EKSİK — RED — Korelasyon kapısı aşırı kurulum; kaynak yok.
04-083 — YANLIŞ — VAR — TASARIM 5.6 ("AGROT–GARAN rotasyon değildir ... listede yok") ve KURALLAR §5, sonuc B-10 ve O12.
04-084 — YANLIŞ — VAR — KURALLAR §3 madde 1 ("birinci el: giriş eşiği, ΔZ tanımı, yön, zaman, ham fiyat"; "onay" yok), sonuc B-10.
04-089 — EKSİK — YENİ — TASARIM 5.10'a sayısal geçme eşiği yaz (hücrelerin ≥%60'ı pozitif); çift ızgara değerleri KURALLAR §3'e (pencere 60/120, eşik 1,5/2/2,5, p 0,01/0,05/0,10).
04-090 — EKSİK — YENİ — TASARIM 5.11'e yaz: sadakat adayları günlüğe "sadakat" etiketiyle girer, Holm m'ye girmez (KURALLAR §1 "her YORUM deneme sayısına girer" ile çelişkiyi giderir).
04-093 — EKSİK — TEKRAR — 04-068.
04-094 — EKSİK — YENİ — TASARIM 5.6 çift seçimine yaz: seçim penceresinde 252 işlem günü verisi olmayan (yeni halka arz) çift aday olmaz.
04-096 — EKSİK — RED — "En iyi çift atılınca" kontrolü aşırı kurulum; 5.12.4 (en iyi %5 işlem) yeterli.
04-097 — EKSİK — VAR — KURALLAR §4 çift satırı (Beta 1,675, korelasyon 0,731, piyasada kalma %72,27, sinyal yok), sonuc B-10; p 0,048, Beta CV ve maliyet hedef değil (test/pencere kaynakta yok).
04-098 — EKSİK — RED — Sinyal sonrası derinleşme tablosu aşırı kurulum.

## Özet

Sayımlar (grep ile, 67 madde: 62 EKSİK + 5 YANLIŞ; KARAR yok): VAR 31, TEKRAR 5, YENİ 11, RED 20.

YENİ maddeler:
- 04-001 (YANLIŞ): KURALLAR §3 madde 1: "α yok; ortalama çıkarıldığı için Z aynıdır".
- 04-002: KURALLAR §4: "üretti" = Z ±0,0005; gevşek bant ±0,05 yalnız tek aday kalırsa.
- 04-003: KURALLAR §4: rapor tarihi bilinmez; Z çifti tüm işlem günlerinde aranır.
- 04-008: TASARIM 5.6: 252 gün seçim penceresi YORUM, Z penceresinden bağımsız.
- 04-029: TASARIM 5.6: VAKBN–GARAN sabit çift, tüm dönem, aynı sinyal ve maliyet kuralı.
- 04-051: TASARIM 5.7 K2: çift bölmesinde 50/50 tanısal; kabul K2 evren sepetiyle.
- 04-057: TASARIM 5.7 K2: 50/50 = yıl başı bir kez al-tut, günlük dengeleme yok.
- 04-068: TASARIM 5.6: bacak kilitliyse geçiş yok; ertesi gün sinyal yeniden değerlendirilir.
- 04-089: TASARIM 5.10: geçme eşiği hücrelerin ≥%60'ı pozitif; çift ızgara değerleri KURALLAR §3.
- 04-090: TASARIM 5.11: sadakat adayları "sadakat" etiketiyle günlüğe girer, Holm m'ye girmez.
- 04-094: TASARIM 5.6: seçim penceresinde 252 işlem günü verisi olmayan çift aday olmaz.

YANLIŞ olup VAR olmayan madde: yalnız 04-001 (YENİ, yukarıdaki değişiklik). Öteki YANLIŞ maddeler VAR: 04-016, 04-048, 04-083, 04-084.
