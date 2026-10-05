# Tansu'dan esinlenen BIST sistemi: tasarım (taslak 2, 05.10.2026)

Bu belge koddan önce gelir. Kod bu belgeye uyar; belge değişmeden davranış değişmez.
Terimler `GLOSSARY.md`'dedir.

Taslak 1 bağımsız bir eleştiriden geçti (5 engelleyici, 12 büyük, 7 küçük bulgu). Taslak 2 bu
bulguları işler. Bulgu kimlikleri (B1, M3…) ekte; her kararın yanında hangi bulguyu kapattığı yazar.

**05.10 ön denemesi (ilk kod ve `rapor/kanit-20261005.md`) bu belgeden önce yazıldı. Kanıt değildir;
rakamları hiçbir kararda kullanılmaz.** (C7)

---

## 1. Amaç

Levent her akşam şunu görmek ister: "Piyasa nasıl, hangi hissede hangi kural sağlandı, nerede
yanıldığımı anlarım?" Kararı ve parayı Levent tutar. Sistem emir vermez, "AL" demez; "kural
sağlandı" der. (P1)

Asıl görev: **bir kuralın işe yarayıp yaramadığını para koymadan önce dürüstçe göstermek.**

En olası sonuç, hiçbir kuralın kabul ölçütünü geçmemesidir. Bu bir başarısızlık değil, sistemin
normal çıktısıdır: "Hiçbir aile geçmedi" ekranı birinci sınıf bir sonuçtur. Ölçüt sonuca bakılarak
gevşetilmez; değişirse tarihli kayıt düşülür ve bütün ayrılmış dönemler sıfırlanır. (P3)

## 2. Tansu'nun düşünce yapısı

Kaynak: beyindeki 238 not, 214 görsel. Notların çoğu Claude özetidir; birinci el kaynak görsellerdir.
Tansu kodunu ve parametrelerini paylaşmaz. Bu yüzden her aile **Tansu'dan esinlenen bizim
yorumumuzdur**; ekranda "Tansu'nun sistemi" diye sunulmaz. (P5)

| İlke | Kaynaktaki karşılığı | Sistemde |
|---|---|---|
| Önce piyasanın havası | "Piyasanın Nabzı" raporu, XU100 setup puanı | Piyasa Nabzı |
| Önce yer, sonra teyit | "zone → kırılım → likidite → teyit" | Aile = yer + teyit |
| Her fırsat bir kart, durum etiketiyle | `AKTİF / TAMAMLANDI / BOZULDU` | Kart |
| Önce sermaye | %1 risk, adet = risk / 2ATR, acil stop | Risk |
| Tek sinyale güvenme | "ABCD'ye gözü kapalı güvenilmez" | Teyit şartı |
| Sınamadan inanma | "mutlaka backtest etmek lazım", negatif sonuçlarını da paylaşır | Kanıt |
| Basit ve sağlam | "Medyan temelli çalışın", "Yüksek Sharpe modeller ilk virajda patlar" | Medyan, sağlamlık sınaması |

## 3. Kapsam (ilk sürüm)

Var: günlük veri, BIST100, yalnız alış yönü, Piyasa Nabzı, 2 aile, tek çıkış kuralı (Ç1), işlem
motoru, portföy simülasyonu, istatistik, markdown rapor, CSV kart listesi.

Yok, ilk aile kabul edilene kadar bekler (gereksiz katman): Streamlit paneli, Telegram, DuckDB,
iz süren stop ve kısmi kâr (Ç2), süre çıkışı (Ç3), dolar bazı karşılaştırma, Corwin–Schultz.
Kanıtı olmayan kurallar için panel kurmak erkendir. (Kesilecekler 1–6)

Kapsam dışı: 4 saatlik ve gün içi veri, emir defteri, opsiyon, harmonik, Elliott, değerleme,
otomatik emir.

## 4. Modüller

Her modülün dışarıya küçük bir yüzü var. İçi değişse de dışı değişmez.

| Modül | Girdi → çıktı | Not |
|---|---|---|
| Veri deposu | indirme → ham fiyat anlık görüntüsü (tarihli, değişmez) | Yahoo geçmişi sonradan değiştirir; her koşu hangi anlık görüntüyü kullandığını yazar. (B2) |
| Şirket olayları | sembol → bedelsiz, bölünme, bedelli, temettü tablosu | Fiyat düzeltmesi buradan yapılır, eşikle tahmin edilmez. (B1, A1) |
| Takvim | tarih → işlem günü mü | BIST tatilleri, yarım günler. (A1) |
| Evren | tarih → o gün taranabilecek hisseler | Bkz. 5.2. (A1) |
| Piyasa Nabzı | endeks → günlük durum | Stratejinin parçasıdır; parametreleri de sınanır ve deneme sayısına girer. (M9) |
| Aile | hisse fiyatı → sinyal günleri | Kural. |
| Adım | (pozisyon, bugünkü mum) → pozisyon | **Sınama ve canlı günlük aynı fonksiyonu kullanır.** Böylece ikisi ayrışamaz. (A5) |
| Motor | aile + çıkış + fiyat → işlem listesi | Adım fonksiyonunu gün gün koşar. Belirleyici. (A2, A3) |
| Simülatör | işlemler + risk kuralı → sermaye eğrisi | Boştaki nakit faiz kazanır. (A2, B4) |
| İstatistik | sermaye eğrisi / fazla getiri → güven aralığı, p değeri | Canlı kâğıt üstü işlemde de aynısı kullanılır. (A2) |
| Rapor | sonuçlar → markdown + CSV | |
| Maliyet | işlem → masraf | Takılıp çıkarılabilir. (A1) |

Kütüphaneler: yfinance (ham fiyat), borsapy (endeks listesi, şirket olayları — araştırılacak),
pandas-ta-classic (göstergeler), statsmodels ve numpy (istatistik), quantstats (rapor ölçütleri).

**vectorbt kararı:** vectorbt'nin dolum kuralları (boşluklu stop, aynı gün stop ve hedef, stopun
neye göre hesaplandığı) belgelerde açık değil. Önce 5.3'teki elle hesaplanmış örneklerle sınanır.
Hepsini doğru geçerse motor olarak kalır. Geçemezse motor, Adım fonksiyonu üzerine kurulan kısa
ve açık bir döngü olur. Adım fonksiyonu canlı günlük için zaten gerekli olduğundan, bu yeni bir
katman değildir. (A3, M1)

## 5. Sınama yöntemi

Amaç: bir kuralın sonucunu **şanstan, piyasanın genel yükselişinden, enflasyondan ve veri
hatasından** ayırmak.

### 5.1 Veri
- Ham fiyat indirilir (düzeltmesiz). Şirket olayları tablosu ayrıca kurulur; düzeltme kodda bir kez
  uygulanır. Sonuç Yahoo'nun düzeltilmiş fiyatıyla karşılaştırılır. (B1, B2)
- Açıklanamayan sıçrama: kapanıştan kapanışa %10,5'i aşan ve şirket olayıyla açıklanmayan her gün
  **karantinaya** girer. O hisse o pencerede sınamadan çıkar; fiyat yamanmaz. (B1)
  Örnek: ECILC ve RYSAS, 12.03.2020.
- İkinci kaynakla tam karşılaştırma: bütün hisse × gün getirileri borsapy ile karşılaştırılır; farkı
  %0,5'i aşan günler listelenir. Örneklem yetmez. (P4)
- Fiyat seviyesi gerektiren her şey (likidite TL tutarı, tavan/taban kontrolü) düzeltmesiz fiyatla
  hesaplanır. (B2)
- Bugünkü veri: son çubuğun tarihi bugün değilse ya da hacim olağandışıysa o gün kart üretilmez. (m6)

### 5.2 Evren ve hayatta kalan yanlılığı
- **Bedava, tarih bazlı BIST100 üyelik verisi yok.** Bugünkü listeyi geçmişe uygulamak sonuçları
  iyimser yapar. Batan hisseler Yahoo'da da yok; "bugün işlem gören en likit 100" bu yanlılığı
  gidermez. (B3)
- Sonuç: **mutlak getiriler üst sınırdır, karar için kullanılmaz.** Yalnız aynı evren içindeki göreli
  karşılaştırmalar (kural ile rastgele kural, kural ile aynı evrenin eşit ağırlıklı sepeti)
  yorumlanır. (B3, B3b)
- Yanlılığın büyüklüğü ölçülür: Borsa İstanbul'un 2015 endeks değişikliği duyurularından o günkü
  BIST30 elle çıkarılır; kurallar bu sabit listede de koşulur ve sonuçlar karşılaştırılır.

### 5.3 İşlem kuralları ve elle hesaplanmış örnekler
- Sinyal günün kapanışında; giriş ertesi açılışta. Stop ve hedef **giriş fiyatından** ve sinyal günü
  ATR'sinden hesaplanır. (M2, C10)
- Giriş günü de stop ve hedef kontrol edilir.
- Aynı gün hem stop hem hedef değerse: **stop önce** (kötümser). Bu işlemlerin oranı raporda yazılır;
  iyimser varsayımla fark ayrıca gösterilir. (M1)
- Stop boşlukla geçilirse çıkış açılış fiyatından.
- Tavan açılışta giriş yok. Taban kilitli günde çıkış yapılamaz; çıkış ertesi günün açılışına
  kayar. (M4)
- Bir hissede pozisyon açıkken gelen yeni sinyal yeni işlem açmaz ve sayıma girmez; rastgele
  karşılaştırmada da aynı kural geçerlidir. (C9, B5d)
- Her kural için motor sınamaları (kod yazılmadan önce): hedefte çıkış, stopta çıkış, boşluklu stop,
  aynı gün stop+hedef, tavan girişi, taban kilidi, bozulma çıkışı.

### 5.4 Masraf ve likidite
- Sabit masraf, her yönde %0,3 (komisyon, BSMV, kayma, açılışta kovalama birlikte). Sonuçlar %0,1 /
  %0,3 / %0,5 ile gösterilir; kabul için %0,5'te de geçmesi gerekir. (M3)
- Likidite: pozisyon, son 10 günün medyan TL işlem tutarının %2'sini geçemez. (M11)

### 5.5 Çıkış
Ç1: 2 ATR stop, 4 ATR hedef; kapanış EMA50 altına inerse ertesi açılışta çık. İlk sürümde tek çıkış
budur. Ç2 ve Ç3 bir aile Ç1 ile kabul edildikten sonra denenir; her biri deneme sayısını artırır.

### 5.6 Portföy
- Sermaye 1.000.000 TL, işlem başına %1 risk, **tek pozisyon en fazla sermayenin %10'u**, en fazla 10
  pozisyon, kaldıraç yok. (M12)
- Aynı gün sinyal sayısı boş yeri aşarsa sıra kuralı önceden sabittir: en likit önce.
- Boştaki nakit, o günün politika faizini kazanır (EVDS; 2015–2017 için politika faizi, sonrası
  TLREF). (B4, P4d)

### 5.7 Karşılaştırma (asıl soru)
Fazla getiri **tanımı** (B4):
- İşlem seviyesi: işlemin getirisi − aynı tutma süresinde aynı evrenin eşit ağırlıklı sepetinin getirisi.
- Portföy seviyesi: günlük portföy getirisi − günlük karşılaştırma getirisi.

Karşılaştırma grupları:
- **K1 Eşleştirilmiş rastgele kural** (B5): rastgele sinyaller, kuralın kendi ön şartlarını sağlayan
  günlerden seçilir (ör. trend ailesi için yalnız trendli günler). Sayılar hisse başına eşleştirilir.
  İki tür: (a) aynı gün, başka hisse; (b) aynı hisse, aynı Nabız durumunda ±20 gün içinde başka gün.
  En az 1.000 tekrar; p değeri buradan çıkar.
- **K2 Aynı evrenin eşit ağırlıklı sepeti** (B3b), aynı temettü düzeltmesiyle. Ayrıca aynı Nabız
  zamanlamasıyla tutulan sepet (K2b); fark Nabız'dan mı kuraldan mı geliyor ayrılsın. (M9)
- **K3 Faiz:** simülatörde boştaki nakit faiz kazandığı için portföy sonucu zaten faize karşı okunur.
Dolar bazı ilk sürümde yok.

### 5.8 Dönemler
- **2023 sonrası ayrılmış dönem yandı.** İki aile ve bu tasarım o döneme bakılarak yazıldı. 2015–2026
  bütünüyle geliştirme/doğrulama verisidir. (M8)
- Doğrulama: genişleyen pencereyle yıllık ileri yürüme. 2015–2017 ile başlar, her yıl bir sonraki
  yıl sınanır. Her yılın sonucu ayrı yazılır. (M7)
- **Yeni ayrılmış dönem = bugünden sonrası.** Kural, parametreleri ve kodunun parmak izi (hash)
  bugün kayda geçer. En az 6 ay kâğıt üstünde canlı izlenir. "Canlı" olmak için bu dönem şarttır. (M8)

### 5.9 Şans payı
- Güven aralığı, günlük portföy fazla getirisi üzerinde 20 günlük bloklarla yeniden örneklenerek
  hesaplanır (işlemler birbirine bağımlı olduğu için). (M5)
- Örneklem: en az 100 işlem **ve** en az 60 farklı sinyal günü. Ölçülen dağılımla "bu örneklemle
  saptanabilecek en küçük etki" hesaplanır ve raporda yazılır. (M5)
- Ortalamanın yanında medyan ve en iyi %5 işlem atılmış sonuç gösterilir. (m2, M10)

### 5.10 Parametre sağlamlığı
Parametreler önceden yazılır (ek: parametre kaydı). Sonra küçük bir rastgele ızgarada birlikte
oynatılır; pozitif hücre oranı raporlanır. En iyi değer seçilmez. (m3)

### 5.11 Çoklu deneme düzeltmesi
Her koşu deneme günlüğüne yazılır (tarih, aile, çıkış, parametre, veri anlık görüntüsü, kod hash).
p değerleri, o ana kadarki bütün denemelerle Holm düzeltmesinden geçer. (M6)

### 5.12 Kabul ölçütü (önceden yazılır)
Bir aile **Canlı** olur, ancak hepsi sağlanırsa:
1. İleri yürüme yıllarının birleşiminde K1'e göre fazla getiri pozitif, Holm düzeltmeli p < 0,05.
2. K2 ve K2b'ye göre portföy fazla getirisi pozitif (nakit faiz dahil).
3. Masraf %0,5'te de 1 ve 2 sağlanıyor.
4. Yılların en az %60'ında fazla getiri pozitif; en iyi %5 işlem atılınca sonuç hâlâ pozitif. (M10)
5. Örneklem şartı (5.9) ve sağlamlık şartı (5.10) sağlanıyor.
6. Bugünden sonraki en az 6 aylık kâğıt üstü dönemde fazla getiri, doğrulamadaki etkinin en az
   yarısı. (M7, M8)

Portföy kuralı (aileden bağımsız): en büyük düşüş %25'i, düşüşte kalma süresi 12 ayı geçmez. (m5)

## 6. Günlük işleyiş (ilk sürüm)
1. 19:30: veri güncellenir; tazelik ve kalite kontrolü. Sorun varsa kart üretilmez. (m6)
2. Piyasa Nabzı.
3. Canlı ailelerin sinyalleri kart listesine (CSV) yazılır. Deneme aileleri varsayılan olarak
   gösterilmez. (P1)
4. Her kartta: hisse, aile, giriş bölgesi, stop, hedef, pozisyon değeri (sermayenin yüzdesi) ve
   ailenin kanıt satırı. Örnek: "112 işlem, rastgele kurala göre fazla getiri −%0,2 ± %1,1:
   ayırt edilemiyor". (P1, P2)
5. Açık kartlar Adım fonksiyonuyla güncellenir: AKTİF / STOP / HEDEF / BOZULDU. (Kesilecek 6)

## 7. Uygulama sırası
1. Ön denemenin yanlış etiketlerini düzelt (GLOSSARY, rapor başlığı).
2. Veri deposu: ham indirme, anlık görüntü, borsapy ile tam karşılaştırma. Şirket olayları kaynağını
   araştır (borsapy, İş Yatırım, KAP).
3. Motor sınamaları (5.3) → vectorbt kararı → Adım + Motor.
4. Simülatör + faiz + K2/K2b.
5. K1 eşleştirilmiş rastgele kural + istatistik + deneme günlüğü.
6. İki aileyi bu düzenle yeniden koş; rapor.
7. Kural kaydı ve hash; kâğıt üstü canlı izleme başlar.

## 8. Açık sorular
1. borsapy ya da İş Yatırım şirket olaylarını (bedelsiz oranı, tarih) veriyor mu? Vermiyorsa KAP'tan
   elle tablo mu çıkarılır?
2. 2015 BIST30 listesi Borsa İstanbul duyurularından çıkarılabiliyor mu?
3. BIST günlük fiyat limiti 2015–2026 arasında hep %10 muydu? (M4)
4. Tedbirli hisseler (brüt takas, tek fiyat) bedava veriyle ayırt edilebiliyor mu? Edilemiyorsa
   bilinen yanlılık olarak yazılır.
5. Kuralların Tansu'ya sadakati doğrulanamaz.

---

## Ek A: Eleştiri bulguları ve durumu

| Kimlik | Konu | Durum |
|---|---|---|
| B1 | Eşikle bedelsiz düzeltme veriyi bozar | 5.1: olay tablosu + karantina |
| B2 | Düzeltilmiş fiyatta seviye hesapları, geçmişin değişmesi | 4, 5.1: ham veri, anlık görüntü |
| B3, B3b | Hayatta kalan yanlılığı giderilemiyor; karşılaştırma tek taraflı | 5.2, 5.7 K2 |
| B4 | Fazla getiri tanımsız; endeks temettüsüz; nakit faizi yok | 5.6, 5.7 |
| B5 | Rastgele karşılaştırma adil değil, 5 tekrar az | 5.7 K1 |
| M1 | Aynı gün stop ve hedef | 5.3 |
| M2 | Stop yanlış tabandan | 5.3 |
| M3 | Masraf düşük | 5.4 |
| M4 | Taban kilidi, limit rejimi | 5.3, 8.3 |
| M5 | Bağımlılık, örneklem gücü | 5.9 |
| M6 | Çoklu deneme düzeltmesi yok | 5.11 |
| M7 | Tek bölme | 5.8 |
| M8 | Ayrılmış dönem yandı | 5.8, 5.12.6 |
| M9 | Nabız stratejinin parçası | 4, 5.7 K2b |
| M10 | Rejim, birkaç işleme bağımlılık | 5.9, 5.12.4 |
| M11, M12 | Likidite, pozisyon tavanı | 5.4, 5.6 |
| A1–A6 | Eksik modüller, Adım paylaşımı, vectorbt | 4 |
| P1–P5 | Yanıltıcı sunum, bedava veri sınırları, ad | 1, 2, 6, 5.1 |
| m1–m7 | Küçükler | dağınık |
