# X videoları: ses dökümleri ve defterle karşılaştırma (07.10)

Dökümler faster-whisper large-v3-turbo ile alındı (Türkçe, otomatik). Satır başındaki sayı saniyedir. Tanıma hataları
var: "JVX" = GVX (tweet metninde GVX yazılı; düzeltme tahmin), "1.688" = 1.618 (tahmin), "bürüt" = brüt. Dökümlerin
sonundaki "Altyazı M.K." satırları sesin parçası değil, whisper artığıdır (tahmin).
Toplam 12 video: 9'u Aralık 2025 dizisi (297–420 sn), 3'ü 8–10 sn kısa klip.
Not: defterdeki R206 ve R212 bu videoların tweet metnini birebir taşır (aynı gönderi). R207–R209 aynı konunun
NotebookLM görselleridir; aynı gönderi olup olmadığı doğrulanmadı (defterde tweet_id yok).

## 1773715205274403212 · 2024-03-29 · kısa klip (10 sn)
Tweet: "Cezayı yiyince aklı başına gelir. Üşenmeyin sizde kayıt alın"
Döküm: "Gidecekler." [5.9]
Kural: yok. Rol: sohbet-duyuru. Defter: karşılığı yok.

## 1999160946976075778 · 2025-12-11 · Fibonacci temel seviye
Tweet: "Fibonacciyi anlayalım Temel Seviye"
Kurallar:
1. Oranlar: "yüzde 23.6" [83.1] (ilk mola), "yüzde 38.2" [96.3] (ciddi düzeltme habercisi), "yüzde 61.8" [112.8]
   ("en kritik, en önemli geri dönüş noktası" [123.9]), "yüzde 50" [138.0] ("teknik olarak bir fibonacci oranı değil" [139.3]).
2. Çapa: "Belirlediğimiz zaman aralığındaki en tepe noktayı ve en dip notkayı buluyor" [199.8]; oranlar "zirve ve dip
   arasındaki o mesafeye uygulanıyor" [215.0]. Zaman aralığının uzunluğu okunamadı.
3. Kullanım: seviyeler "olası destek ve direnç bölgelerini" gösterir [264.2]; "diğer analiz yöntemlerinizle birlikte
   kullanacağınız" [337.0]. Giriş, stop, hedef yok.
Kural düzeyi: cekirdek (hesap belli, pencere eksik). Rol: ölçüm-yöntemi (rol2 bölge).
Defter: aynı. Fibo seviyeleri araç görsellerinde var: R149 (defter-3:156), R197 Swing Low → Swing High
(defter-3:590). Videoda 0.786 yok.

## 1999163401763799349 · 2025-12-11 · Fibonacci ileri seviye (çapa ve kesişim)
Tweet: "Bu çok öenmli bir özet bence kaydedin sarıp sarıp dinleyin İleri seviye"
Kurallar:
1. Yaygın hata: "trendin en tepe noktasını alıyorlar, sonra da en dip noktasına bağlıyorlar" [105.0]; fiyat seviyeyi
   "delip geçiveriyor" [128.9].
2. Çapa düzeltmesi: "Mutlak en dip noktayı almak yerine" [221.7] "çok daha anlamlı bir ikinci dip noktasını
   kullanıyoruz" [224.6]. "İkinci dip"in tanımı okunamadı.
3. Çoklu set: "farklı salınımlardan gelen birden fazla Fibonacci hesabını alıp ... üst üste koyuyoruz" [247.7];
   "Farklı tepe noktalarını baz alarak iki ayrı Fibonacci seti" [265.9]; çizgilerin kümelendiği yer
   "kesişim bölgesi" [279.4], "tek bir çizgiden fersah fersah daha anlamlı" [284.7]. Kaç çizginin küme sayıldığı
   (tolerans) okunamadı.
Kural düzeyi: cekirdek. Rol: bölge.
Defter: genişletir. R208 (defter-4:100) kesişimi Fibo + RSI + eski tepe olarak tanımlar; bu video kesişimi
yalnız Fibo setleri arasında kurar (çoklu salınım kümesi) ve çapayı "ikinci dip"e taşır. İkisi defterde yok: yeni.

## 1999361321435811868 · 2025-12-12 · Altın–dolar istatistiksel arbitraj, GVX rejim filtresi
Tweet (kısa): "GVX'i bir al-sat sinyali olarak değil, stratejimizi ne zaman çalıştırıp ne zaman durdurmamız gerektiğini
söyleyen bir 'Rejim Filtresi' olarak kullanacağız."
Kurallar:
1. Ortalamaya dönüş: "spread dediğimiz fiyat farkının eninde sonunda her zaman ortalamasına geri döneceğine
   inanıyoruz" [137.2]; "Eğer bu fark aşırı açılırsa biz de bu farkın kapanacağı yönünde pozisyon alıyoruz" [146.4].
   "Aşırı" eşiği (Z skoru vb.) okunamadı.
2. Rejim filtresi: "JVX düşükken" (GVX, tahmin) teknik "tıkır tıkır işleyerek" [151.5–157.7]; "JVX fırladığında"
   [163.8] "motorları durduruyoruz" [180.0]; "hava fırtınalıysa sistemi kapatıyoruz" [309.3]. GVX eşiği okunamadı.
3. Anomali: "GVX tavan yapmış" [225.0] ama altın/gümüş "rasyo tam tersine düşüyor" [236.9] → "bu anomali üzerine
   pozisyon alıyoruz" [244.4]. Pozisyon yönü okunamadı.
4. Karar matrisi örneği: "GVX yükselirken dolar düşüyorsa ... Altını al, dolar sat." [273.6–281.0]. Matrisin öbür
   hücreleri okunamadı.
5. Model sırası: "normalize edilmiş verilerle" [297.6] → "istatistiksel bir modelle ... spread'ı oluşturuyoruz" [300.8]
   → "GVX filtresini uyguluyoruz" [306.0] → "opsiyon piyasasındaki olası etkiler" [312.2].
6. İlke: GVX'i "sinyal olarak değil ... barometre olarak kullanın" [321.7–325.6].
Kural düzeyi: cekirdek (yön ve sıra belli, eşik yok). Rol: rejim (rol2 çift).
Defter: kural 1 aynı: R262 (defter-4:599) spread ortalamadan sapınca pahalıyı sat, ucuzu al; R228 (defter-4:281)
kointegrasyon şart (videoda kointegrasyon testi okunamadı; yalnız "istatistiksel bir model"). Kural 2–4 yeni:
defterde GVX, altın/gümüş oranı ve "volatilite yüksekse arbitrajı kapat" filtresi yok.

## 1999375397268410597 · 2025-12-12 · Japonya likiditesi, altın/gümüş oranı
Tweet (kısa): "Japonya'nın son dönemde faiz artırımı ve tahvil alımlarını azaltmasıyla tetiklenen 'likidite sorununun'
küresel piyasaları nasıl etkilediğini kısaca açıklayalım"
Kurallar:
1. Zincir: "Birinci domino taşı Japonya'da devrilir" [345.3] → "küresel bir satış dalgası" [347.5] → "gümüş altından
   daha çok hırpalanır" [350.0] → "altın-gümüş oranı fırlar" [352.9].
2. Okuma: "Oran yükseliyorsa ... yatırımcılar güvenli liman olan altına sığınıyordur" [320.3]; "kişisel erken uyarı
   sisteminiz olsun" [359.6]. İşlem eylemi (al/sat) yok.
Kural düzeyi: fikir (makro anlatı; eşik ve eylem yok). Rol: rejim. Çoğu eğitim.
Defter: yeni (defterde yen carry trade ve altın/gümüş oranı yok). 1999361321435811868 ile tutarlı: panikte oran
yükselir (normal); GVX yüksekken oran düşerse anomali.

## 1999481868106826013 · 2025-12-12 · Pozisyon boyutu, %1 risk, 2 ATR, SMA250
Tweet (kısa): "Diyelim ki sermayenizin ancak %1'ini kaybetmek riskini göze alabilirsiniz ve diyelim ki işleme giriş
bileşenlerinizden birisi 250SMA."
Kurallar:
1. Risk sınırı: "tüm sermayenizin en fazla ama en fazla yüzde birini riske atacağınız" [40.0]; örnek "yüz bin dolarlık
   bir hesabınız" [111.5] → "risk sermayeniz tam olarak bin dolar" [116.1].
2. Hisse başına risk: "Ortalama gerçek aralık ya da kısaca ATR. Sistem diyor ki bunun iki katını al." [159.1–162.4];
   örnek "14.30 dolar" [164.8].
3. Adet: "Bin dolarlık toplam riskimizi ... 14.30'a görüyoruz" [169.6] → "69.9 yuvarlayalım, 70 hisse" [176.3].
4. Acil stop: "14.30 dolar aşağıya değer değmez, alarm çalar ve siz düşünmeden anında satarsınız" [208.8].
5. Gün sonu stop: "gün sonunda o önemli 250 günlük hareketli ortalamanın altında bir kapanış yaparsa" [229.3] →
   "pozisyonu kapatma zamanı" [236.6].
ATR periyodu okunamadı.
Kural düzeyi: tam. Rol: boyut-risk (rol2 çıkış).
Defter: aynı R212 (defter-4:135–136; aynı gönderi). Genişletir R184 (defter-3:466): R184 "ATR mi 2×ATR mı"
belirsiz der; video açıkça "bunun iki katını al" der → hisse başına risk = 2×ATR. R195 (defter-3:573) 1×ATR stop
ile farklı parametre (çelişki değil; ayrı kayıt).

## 1999567041905492120 · 2025-12-12 · VIX–BIST 100 korelasyon rejimleri
Tweet (kısa): "'Korkuyu Satın Al' (dip avcılığı), 'Rehaveti Sat' (tepe tespiti) ve 'Ayrışmayı Oynamak' ... pozitif
korelasyon dönemlerinde Dolar/TL kur hareketlerinin etkisinin kontrol edilmesi gerektiği"
Kurallar:
1. Üç rejim: normal "VIX fırladığında ... BIST-100 kırmızıya boyanıyor" [121.4–131.3]; anomali/ayrışma "VIX taban yapmış
   ... BIST-100 yeşil" [147.3] (döküm "taban", bağlam "tavan" gerektirir; tahmin); kopukluk "VIX yükselmiş, düşmüş, hiç
   umurunda değil" [170.7]. Korelasyon penceresi ve eşiği okunamadı.
2. Korkuyu satın al: "VIX'in 30'ları 40'ları gördüğü" [218.7]; "VIX'in o zirveden ... kafasını aşağı yemeye başladığı an"
   [227.2] alım fırsatı. Dönüşün tanımı okunamadı.
3. Rehaveti sat: "VIX endeksi ... 10-13 gibi komik rakamlarda uzun süredir takılıyorsa" [254.3–257.4] → "karı cebe koyup
   biraz nakite geçmek için harika bir sinyaldir" [271.8]. "Uzun süre" okunamadı.
4. Ayrışmayı oyna: VIX tırmanırken BIST yeşil = "pozitif ayrışma" [286.5]; "endeksin geneline değil, bu ayrışmaya liderlik
   eden ... hisselere odaklanmak" [295.6–299.5].
5. Uyarı: "pozitif ayrışma gördüğünüzde ilk bakacağınız yer dolar-tl kuru olmalı" [344.9]; kur kaynaklı yükseliş
   "sahte bir yükseliştir" [341.4].
Kural düzeyi: cekirdek (VIX eşikleri var; pencere, dönüş tanımı ve süre yok). Rol: rejim.
Defter:
- Kural 1 aynı: R209 (defter-4:108) "BIST 100 yükselirken VIX'in düşmesi"; R210 (defter-4:117) "Eğer negatif değilse
  aşırı dikkat".
- Kural 4–5 genişletir R210: R210 pozitif korelasyonu yalnız uyarı sayar; video bunu "çok güçlü sinyal" sayar ama
  önce dolar/TL kontrolünü şart koşar.
- Kural 3 çelişir (kısmi) R188 (defter-3:509): R188 "VIX 13,47 (güvenli, limit 16,99)" der ve long tarafında iyimser;
  video 10–13 bandında uzun kalışı kâr alma/nakde geçiş sinyali sayar.
- Kural 2 ve 3 (VIX 30–40 kapitülasyon alımı, 10–13 rehavet satışı) eşikleriyle yeni. R077 (defter-2:89) rehaveti
  BIST volatilitesi için yön bağımsız anlatır (VIX eşiği yok).

## 2000103306325004349 · 2025-12-14 · Elliott 5-3 ve Fibonacci zamanı
Tweet: "Fibonacciyi çok sevdik o zaman biraz daha öğrenelim. #fibonacci"
Kurallar:
1. Yapı: "bir, iki, üç, dört, beş dalgalık bir hareket" [92.2] itki; "üç dalgalık bir düzeltme" [103.8]; fraktal "otuz
   dört dalga" [199.6], "yüz kırk dörde" [202.3].
2. Zaman: "beşinci günde trend hala gücünü koruyor mu?" [280.4] → "sekizinci güne bakabilirsiniz" [284.2]; bu günler
   "yön değiştirme ihtimalinin arttığı kritik anlar" [288.6]. Sayımın başlangıç noktası okunamadı.
3. Sayım: "sadece borsanın açık olduğu işlem günlerini almayın" [319.3]; "takvimdeki her bir günü saymanız gerekiyor"
   [327.2]; "her zaman takvim günlerini kullanmalıyız" [370.0].
Kural düzeyi: cekirdek (5. ve 8. gün belli; başlangıç ve eylem yok). Rol: formasyon.
Defter: aynı R207 (defter-4:92–93). R207 5/8/13/21 sayar; video yalnız 5 ve 8'i söyler.

## 2000153302927806546 · 2025-12-14 · Fibo 0.618 bölge + H4 kurumsal seviye
Tweet (kısa): "Fibo 0.618 bir 'duvar' değil, sadece bir 'bölge'dir." ; "Matematiksel oran (Fibo) + Piyasa Yapısı
(Order Block) = Sniper Giriş."
Kurallar:
1. Tuzak: stoplar "0.618 gibi herkesin bildiği seviyelerin hemen altıdır" [111.0]; fiyat oraya itilir, stoplar
   patlatılır [118.1]. Örnek: günlükte 100 lira beklenir, oyun "4 saatlik grafikteki 98 liralık" seviyede [55.1].
2. Adım 1: "günlük grafiğe bakıyoruz, ana trendi anlıyoruz ve fiyatın ... 0.5 ile 0.618 arasına gelmesini sabırla
   bekliyoruz" [164.5].
3. Adım 2: "Fiyat o bölgeye girer girmez ... 4 saatliğe iniyoruz" [176.9]; "kurumsal seviyeleri arıyoruz" [183.7].
4. Adım 3: giriş "kurumsal seviyeyle Fibonacci bölgesinin kesiştiği o sihirli noktaya" [191.5].
5. H4'te aranan: "emir bloğu" [205.2], "Kırılım bloğu yani eskiden direnç olan ama artık desteğe dönüşen" [212.1],
   "dengesizlik yani FVG" [217.8]; "bu üçünden birine o altın bölge içinde bulduğumuzda ... güçlü bir onay" [225.2].
Stop, hedef ve emir bloğu tanımı okunamadı.
Kural düzeyi: cekirdek (bölge ve zaman dilimi belli; stop/hedef yok). Rol: giriş (rol2 teyit).
Defter:
- Genişletir R206 (defter-4:84–85; aynı gönderi): R206 yalnız "Fibo + Order Block" der; video üç adımı, 0.5–0.618
  bölgesini ve H4 aday listesini (OB, kırılım bloğu, FVG) ekler.
- Aynı R204 (defter-4:68–69): 0.50 veya 0.618 + FVG çakışması.
- Çelişir R197 (defter-3:590–592): R197 bölgeyi "0.618 ile 0.786 arası" (OTE) alır; video "0.5 ile 0.618 arası"nı
  alır. R199 (defter-4:11) %50–%78,6 ikisini de kapsar.

## 2001021294612242538 · 2025-12-16 · Brüt, net ve logaritmik getiri
Tweet: "Ufak ufak başlayalım Brüt getiri Net getiri Logaritmik getiri"
Hesap kuralları:
1. Brüt getiri: "Formülü PT bölü PT eksi 1" [102.0] (döküm belirsiz; anlam P_t / P_(t−1), tahmin); "bugünün fiyatını
   dünün fiyatına bölüyorsun" [105.4].
2. Net getiri: "bürüt getiriden, yani 1.05'den 1'i çıkarıyoruz" [121.0] → "0.05, yani yüzde 5" [126.7].
3. Örnek: "1465 dolar" [142.2] / "1447 dolara" [146.6] − 1 → "Artı %1.24" [158.8].
4. Çok dönem: brüt getiriler çarpılır [241.8]; log getiriler "basitçe topluyorsunuz" [263.5].
5. Geri kurma: "bin dolardı" [322.9] → −%1.4 → "986 dolar" [340.4] → +%1.3 → "998.82 dolar" [375.7].
Kural düzeyi: tam (hesap). Rol: ölçüm-yöntemi (araç-öğrenme). Eğitim; işlem kuralı yok.
Defter: aynı R173 (defter-3:376, pct_change, "yalnız fikir"); R260 (defter-4:573) log getiri kullanır. Yeni kural yok.

## 2005192826456605182 · 2025-12-28 · kısa klip (8 sn)
Tweet: "Yarına Allah kerim:)"
Döküm: "İşte beklenen an, boğa saldırıyor, ayı direniyor, tansiyon çok yüksek." [0.0]
Kural: yok. Rol: görüş. Defter: karşılığı yok.

## 2091537717234430180 · 2026-08-23 · kısa klip (8 sn)
Tweet: "Torunlar geldi :)"
Döküm: boş (okunamadı). Kural: yok. Rol: sohbet-duyuru.

## Dizi özeti: Aralık 2025 (11–16 Aralık, 9 video, 297–420 sn)
Biçim: tek anlatıcı, sunum dili ("Bu tablo", "bu slide"), soru ile kapanış. Biçim NotebookLM sesli özetine benzer
(tahmin; defterde aynı günlerin görselleri R207–R212 "G-dış (NotebookLM)" diye işaretli).
Üç kol:
1. Fibonacci (4 video: 1999160946976075778 temel → 1999163401763799349 ileri → 2000103306325004349 Elliott + zaman →
   2000153302927806546 bölge + H4). Gidiş: tek çizgi → çoklu set kesişimi → takvim günü zamanlaması → 0.5–0.618
   bölgesi içinde H4 OB/kırılım bloğu/FVG ile giriş.
2. Rejim ve makro (3 video: 1999361321435811868 GVX + altın/dolar spread, 1999375397268410597 Japonya likiditesi,
   1999567041905492120 VIX–BIST). Ortak fikir: korku endeksi sinyal değil, filtre ("barometre").
3. Risk ve ölçüm (2 video: 1999481868106826013 %1 risk + 2 ATR + SMA250; 2001021294612242538 getiri hesabı).
Kurallı video (cekirdek ya da tam): 7 (1999160946976075778, 1999163401763799349, 1999361321435811868,
1999481868106826013, 1999567041905492120, 2000103306325004349, 2000153302927806546) + hesap kuralı tam olan
2001021294612242538 (eğitim). Fikir düzeyi: 1999375397268410597.

## Defter için öneriler
1. Pozisyon boyutu: hisse başına risk = 2 × ATR (R184'teki belirsizliği kapatır). Kaynak 1999481868106826013 [162.4];
   R212, R184 (defter-3:466). Genişletir.
2. Fibo giriş bölgesi çelişkisini karara bağla: 0.5–0.618 (2000153302927806546 [164.5]) mi, 0.618–0.786 (R197,
   defter-3:590) mı. Çelişir.
3. Günlük bölge → H4 aday (OB, kırılım bloğu, FVG; "üçünden birine") → kesişimde giriş. Kaynak 2000153302927806546
   [164.5–225.2]; R206 (defter-4:85). Genişletir.
4. Çoklu salınımdan Fibo setleri; kümelenen çizgiler = kesişim bölgesi; çapa "ikinci dip". Kaynak 1999163401763799349
   [224.6, 247.7, 279.4]; R208 (defter-4:100). Yeni (tolerans ve "ikinci dip" tanımı eksik).
5. VIX eşikli BIST rejim kuralları: VIX 30–40 sonra dönüş = alım; VIX 10–13 uzun süre = kâr al / nakde geç. Kaynak
   1999567041905492120 [218.7–271.8]. Yeni; R188 (defter-3:509) "VIX 13,47 güvenli" ile kısmi çelişki.
6. Pozitif VIX–BIST ayrışmasında önce dolar/TL kontrolü; kur kaynaklıysa "sahte" yükseliş; gerçekse ayrışmaya liderlik
   eden hisseler. Kaynak 1999567041905492120 [295.6–344.9]; R210 (defter-4:117). Genişletir.
7. Arbitraj rejim filtresi: volatilite endeksi (GVX) yüksekken ortalamaya dönüş stratejisini kapat. Kaynak
   1999361321435811868 [163.8–180.0, 309.3]; R262 (defter-4:599), R228 (defter-4:281). Yeni (eşik eksik).
8. Altın/gümüş oranı korku göstergesi: GVX yüksek + oran düşüyor = anomali. Kaynak 1999361321435811868 [225.0–244.4],
   1999375397268410597 [352.9]. Yeni (fikir/cekirdek; BIST kullanımı belirsiz).
9. Fibonacci zaman: 5. ve 8. gün kontrol noktası, takvim günüyle say. Kaynak 2000103306325004349 [280.4–327.2];
   R207 (defter-4:93). Aynı (videodan teyit; başlangıç noktası eksik).
