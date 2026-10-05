# Tansu'dan esinlenen BIST sistemi: tasarım (taslak 6, 05.10.2026)

Geçmiş:
- Taslak 1, bağımsız bir eleştiriden geçti: 5 engelleyici, 12 büyük, 7 küçük bulgu.
- Taslak 2, bu bulguları işledi. Bulgu kimlikleri (B1, M3…) ekte.
- Taslak 4: ilk sorgu, 14 soru ("Sorgu Sn").
- Taslak 5: ikinci sorgu, 52 soru ("S2-n", `docs/sorgu/sorgu-2.md`).
- Taslak 6: bağımsız sorgu, 2.000 soru (`docs/sorgu/sonuc-3-4.md`; etiket "B-n" tasarım, "C-n" altyapı).
  - Soruları ve cevapları ayrı ajanlar yazdı.
  - En büyük değişiklikler:
    - AB=CD ilk sürümden çıktı.
    - Yahoo tamamen çıktı.
    - Streamlit çıktı.
    - Karşılaştırma sepeti maruziyete eşlendi.
    - Tekrar sayısı deneme sayısına bağlandı.

Bu belge koddan önce gelir. Kod bu belgeye uyar; belge değişmeden davranış değişmez.
Terimler `GLOSSARY.md`'dedir.

**05.10 ön denemesi (ilk kod ve `rapor/kanit-20261005.md`) bu belgeden önce yazıldı. Kanıt değildir;
rakamları hiçbir kararda kullanılmaz.** (C7)

---

## 1. Amaç

Levent her akşam şunu görmek ister: "Piyasa nasıl, hangi hissede hangi kural sağlandı, nerede
yanıldığımı anlarım?" Kararı ve parayı Levent tutar. Sistem emir vermez, "AL" demez; "kural
sağlandı" der. (P1)

Asıl görev: **bir kuralın işe yarayıp yaramadığını para koymadan önce dürüstçe göstermek.**

Önce sadakat, sonra kâr: bir aile önce Tansu'nun gösterdiği haliyle sınanır. Tutmazsa değiştirilmiş
hali yeni bir deneme sayılır ve deneme günlüğüne yazılır (5.11). (Sorgu S2)

En olası sonuç, hiçbir kuralın kabul ölçütünü geçmemesidir. Bu bir başarısızlık değil, sistemin
normal çıktısıdır.
- "Hiçbir aile geçmedi" ekranı birinci sınıf bir sonuçtur.
- "Ölçülemedi" de ayrı bir sonuçtur (5.12).
- Ölçüt sonuca bakılarak gevşetilmez.
- Ölçüt değişirse tarihli kayıt düşülür ve bütün ayrılmış dönemler sıfırlanır. (P3, B-17)

## 2. Tansu'nun düşünce yapısı

Kaynak: beyindeki 238 not, 214 görsel. Notların çoğu Claude özetidir; birinci el kaynak görsellerdir.
Tansu kodunu ve parametrelerini paylaşmaz. Bu yüzden her aile **Tansu'dan esinlenen bizim
yorumumuzdur**; ekranda "Tansu'nun sistemi" diye sunulmaz. (P5)

| İlke | Kaynaktaki karşılığı | Sistemde |
|---|---|---|
| Önce piyasanın havası | "Piyasanın Nabzı" raporu (NotebookLM), XU100 setup puanı (formülü yok) | Piyasa durumu etiketi; ilk sürümde kapı değil |
| Önce yer, sonra teyit | "zone → kırılım → likidite → teyit" | Aile = yer + teyit |
| Her fırsat bir kart, durum etiketiyle | `AKTİF / TAMAMLANDI / BOZULDU` | Kart |
| Önce sermaye | %1 risk, adet = risk / 2ATR, acil stop | Risk |
| Tek sinyale güvenme | "ABCD'ye gözü kapalı güvenilmez" | Teyit şartı |
| Sınamadan inanma | "mutlaka backtest etmek lazım", negatif sonuçlarını da paylaşır | Kanıt |
| Basit ve sağlam | "Medyan temelli çalışın", "Yüksek Sharpe modeller ilk virajda patlar" | Medyan, sağlamlık sınaması |

## 3. Kapsam (ilk sürüm)

Var:
- Günlük veri, BIST100 benzeri evren, yalnız alış yönü.
- Piyasa durumu etiketi (yalnız raporlama).
- **2 aile** (`KURALLAR.md` §3): çift rotasyonu ve EMA sıkışması.
- Tansu'nun risk paketi (5.5), işlem motoru, portföy simülasyonu, istatistik.
- Tek dosya HTML rapor, CSV kart listesi, `durum.txt`.

Yok, ilk aile kabul edilene kadar bekler (gereksiz katman):
- Streamlit ya da başka panel, Telegram, veritabanı.
- İz süren stop ve kısmi kâr (Ç2), süre çıkışı (Ç3).
- Dolar bazı karşılaştırma, Corwin–Schultz.

Kanıtı olmayan kurallar için panel kurmak erkendir. (Kesilecekler 1–6, C-1)

İkinci dalga:
- AB=CD. Tansu'nun SMRTG sınaması aşağı yönlü kalıplarla ve C fiyatından giriyor; BIST'te bireysel açığa
  satış pratik değil. Alış yönlü hali Tansu'nun gösterdiği kural olmaz. (B-1)
- AEFES kanal, AKFIS kurulumu.
- Fiili dolaşım taraması.

Kapsam dışı: 4 saatlik ve gün içi veri, emir defteri, opsiyon, harmonik, Elliott, değerleme,
otomatik emir.

## 4. Modüller

Her modülün dışarıya küçük bir yüzü var. İçi değişse de dışı değişmez. Paket düzdür (`tansu/`). (C-3)

| Modül | Girdi → çıktı | Not |
|---|---|---|
| `kaynak` | sembol, tarih aralığı → ham tablo | Ağa çıkan tek yer. İş Yatırım ve borsapy. (C-8) |
| `veri` | indirme → anlık görüntü; olay tablosu; veri kapıları | Anlık görüntü tarihli ve değişmez. Olay çarpanı yalnız denetim. (B2, B-2, B-7) |
| `evren` | tarih → o gün taranabilecek hisseler | 5.2. |
| `gostergeler` | fiyat → EMA, SMA, ATR, piyasa durumu | Kütüphane yok; her biri birkaç satır. |
| `aileler` | hisse fiyatı → sinyal günleri | Tek hisse aileleri. |
| `cift` | çift fiyatları → hangi hissede olunacağı | Kendi döngüsü. |
| `motor` | Adım: (pozisyon, bugünkü mum) → pozisyon; Motor: sinyaller → işlemler | **Sınama ve canlı günlük aynı Adım'ı kullanır.** (A5) |
| `simulator` | işlemler + bölme kuralı → sermaye eğrisi | Boştaki nakit faiz kazanır. (A2, B4) |
| `istatistik` | fazla getiri → güven aralığı, p değeri, Holm | statsmodels yalnız `coint` ve Holm için. |
| `kayit` | kural kaydı, deneme günlüğü, kart günlüğü | Yalnız ekleme. (C-6) |
| `rapor` | sonuçlar → HTML + CSV + `durum.txt` | Şablon motoru yok. |
| `__main__` | `python -m tansu gunluk` / `sinama` | Tek giriş. |

Takvim, fiyat günlerinden çıkar (XU100 günleri, borsapy). Maliyet tek bir sabittir.

**Motor kendi Adım döngümüzdür; vectorbt kullanılmaz.** Dolum kuralları (5.3) AOF'a ve gün
yükseği/düşüğüne koşullu. Ölçütler (düşüş, süre, getiri) kısa kendi kodumuzdur. (A3, M1, S2-41, C-2)

Kaynaklar (`docs/arastirma/veri-kaynaklari.md`):
- **Fiyat:** İş Yatırım `HisseTekil`, anahtarsız.
  - Ham `HG_*` ve düzeltilmiş `HGDG_*` seriler; düzeltilmiş seri bedelsiz, bedelli ve brüt temettüyü
    kapsar.
  - Alanlar: kapanış, yüksek, düşük, AOF, hacim (TL), piyasa değeri (PD), fiili dolaşım değeri (HAO_PD),
    sermaye.
  - **Açılış yok.**
  - 2000'den veri var.
- **Yahoo kullanılmaz.** Şirket olaylarını yanlış günde gösteriyor. Tansu'nun ham seri rakamları İş
  Yatırım ham serisiyle birebir üretiliyor. (B-2)
- **Şirket olayları:** İş Yatırım `GetSermayeArttirimlari`, bütün kodlarıyla. Tarih hak kullanım günüdür.
- **Faiz:** borsapy TCMB politika faizi; 2015'ten tek seri. (B-8)
- **Endeks günleri ve sektör:** borsapy.

Kullanım koşulları ve hız sınırları bulunamadı; az sayıda istek, yerel önbellek.

## 5. Sınama yöntemi

Amaç: bir kuralın sonucunu **şanstan, piyasanın genel yükselişinden, enflasyondan ve veri
hatasından** ayırmak.

### 5.1 Veri
- **İndirme:** veri 2010'dan indirilir; göstergeler ısınır. İlk sinyal 30.11.2015; ±%20 limit rejiminin
  başı. (B-6)
- **Seriler:**
  - Göstergeler ve getiriler düzeltilmiş seriden (`HGDG`).
  - Fiyat limiti, kilit ve likidite TL tutarı ham seriden (`HG`).
  - Sadakat kontrolü ham seriyle; Tansu ham seri kullanıyor. (B2, B-2)
- **Olay denetimi:** olay tablosu çarpanı (`SHHE_FIYAT_AYAR_OR`) ham seriye uygulanır ve `HGDG` ile
  karşılaştırılır. Fark %0,5'i aşan gün uyarıdır; `HGDG` geçerli kalır. (B1, B-2)
- **Fiyat limiti:** önceki gün ham kapanışının ±L'si.
  - L = %20 (30.11.2015 – 12.03.2020), %10 (13.03.2020 sonrası).
  - Tabanın önceki kapanış olduğu ±%10 döneminde veriyle doğrulandı.
- **Karantina:** kapanıştan kapanışa o günkü limiti (+%0,5) aşan ve şirket olayıyla açıklanmayan her gün
  karantinaya girer.
  - O hisse o günden 250 gün boyunca yeni sinyal üretmez.
  - Açık pozisyon son temiz AOF'ta kapanır ve sayılır.
  - Fiyat yamanmaz.
  - Aynı maske kural, K1 ve K2'ye uygulanır. (B1)
- **Hacim:** `HACIM` TL'dir. Hacmi sıfır olan gün (durdurma) işlem günü değildir.
- **İkinci kaynak:** borsapy getirileriyle bütün hisse × gün karşılaştırılır; farkı %0,5'i aşan günler
  listelenir. (P4)
- **Bugünkü veri:** son çubuğun tarihi bugün değilse ya da veri kapısı (5.13) kalırsa o gün kart
  üretilmez. (m6)

### 5.2 Evren ve hayatta kalan yanlılığı
- **Bedava, tarih bazlı BIST100 üyelik verisi yok.** Bugünkü listeyi geçmişe uygulamak sonuçları iyimser
  yapar. (B3)
- **Evren kuralı:**
  - Ayın ilk işlem günü, **önceki ayın son kapanışındaki** piyasa değerine göre en büyük 100 hisse.
  - O tarihte işlem gören, yalnız pay hisseleri.
  - 60 günlük medyan TL hacimde en alttaki %20 önce elenir.
  - Evren yalnız yeni girişi sınırlar. Evrenden çıkan hissenin açık pozisyonu kendi kuralıyla kapanır.
    (B-9)
- **İşlemi kapanan hisseler:** İş Yatırım bunları da veriyor (ASYAB 2016'ya kadar), ama liste eksik
  (FINBN boş döndü).
  - Kapanan hissede açık pozisyon −%100 sayılır; nedeni bilinirse son fiyat.
  - 60 işlem gününden uzun durdurma kapanma sayılır.
  - Bulunamayan semboller raporda yazılır.
- **Sektör:** bugünkü sınıflamadan (borsapy). Kaba ve tarih bilgisiz; bilinen yanlılık. (S2-21)
- **Sonuç:** mutlak getiriler karar için kullanılmaz. Yalnız aynı evren içindeki göreli karşılaştırmalar
  yorumlanır (K1, K2). (B3, B3b)
- **Gerçek BIST100** KAP duyurularından çıkarılınca kurallar onda da koşulur.

### 5.3 İşlem kuralları ve elle hesaplanmış örnekler
- **Sinyal ve giriş:**
  - Sinyal günün kapanışındadır.
  - İşlem fiyatı ertesi günün **ağırlıklı ortalama fiyatıdır (AOF)**; kaynakta açılış yok.
  - Sinyal günü kapanış SMA250 altındaysa giriş yok. (S2-7, B-12)
- **Stop:** giriş fiyatından ve sinyal günü ATR'sinden hesaplanır. (M2, C10)
- **Giriş günü:** yalnız stop kontrol edilir.
- **Stop dolumu:** gün düşüğü ≤ stop ise dolum **min(stop, AOF)**. (B-4)
- **Kilitli gün:** düşük = yüksek, hacim > 0 ve fiyat limit fiyatında (bir fiyat adımı toleransla).
  - Kilitli tavanda giriş yok.
  - Kilitli tabanda çıkış ertesi güne kayar.
  - Yalnız "düşük = yüksek" kilit sayılmaz; az işlem gören hissede de olur. (M4, B-5)
- **Yeni sinyal:** bir hissede pozisyon açıkken gelen yeni sinyal yeni işlem açmaz ve sayıma girmez.
  Rastgele karşılaştırmada da aynı kural geçerlidir. (C9, B5d)
- **Motor sınamaları** (kod yazılmadan önce, elle hesaplı):
  - stopta çıkış
  - boşluklu stop
  - giriş günü stop
  - kilitli tavan girişi
  - kilitli taban çıkışı
  - SMA250 çıkışı
  - açık pozisyonda yeni sinyal
  - sinyalden sonra veri yok
  - stop kenarları (düşük = stop, yüksek = stop)

### 5.4 Masraf ve likidite
- **Masraf:** sabit, her yönde %0,3 (komisyon, BSMV, kayma birlikte).
  - Sonuçlar %0,1 / %0,3 / %0,5 ile gösterilir.
  - Kabul için %0,5'te de geçmesi gerekir. (M3)
- **Likidite:** pozisyon, son 10 günün medyan TL işlem tutarının %2'sini geçemez. (M11)
- **Vergi:** sınamaya girmez; raporda not edilir.

### 5.5 Çıkış
Tansu'nun risk paketi (`kurallar/E` K1–K3; kaynak Tansu'nun paylaştığı infografik):
- **Acil stop:** giriş − 2 ATR; gün içinde dokunulursa çıkılır.
- **Gün sonu çıkış:** kapanış SMA250 altına inerse ertesi günün AOF'unda.
- **ATR:** uzunluk 14, Wilder ortalaması (YORUM).
- **Hedef yok:** iki ailede de Tansu hedef vermedi.
- **Çift rotasyonu:** stop yok; karşı uçta diğer hisseye geçilir. Risk paketi bu bölmeye uygulanmaz.
  (Sorgu S3)
- **Aile kuralları:** giriş kuralları ve YORUM'lar `KURALLAR.md` §3'tedir.
- **İz süren stop ve kısmi kâr:** ikinci el kaynaklı; bir aile bu paketle kabul edildikten sonra denenir.

### 5.6 Portföy ve bölmeler
İlk sürümde her aile **kendi sermayesiyle ayrı** ölçülür. (Sorgu S6)

- **Tek hisse bölmesi** (EMA sıkışması):
  - Sermaye 1.000.000 TL, bileşik büyür. Özkaynak = nakit + pozisyonların kapanış değeri.
  - İşlem başına %1 risk; adet aşağı yuvarlanır.
  - Tek pozisyon en fazla sermayenin %10'u (YORUM, bizim), en fazla 10 pozisyon, kaldıraç yok.
  - Aynı gün sinyal sayısı boş yeri aşarsa en likit önce. (M12)
  - **%10 tavan, %1 riskten çoğu gün daha bağlayıcıdır:** 2 ATR çoğu hissede fiyatın %3–7'si. Fiili risk
    ≈ %0,6–0,8 olur. Rapor tavanın bağladığı işlem oranını ve gerçekleşen riski yazar. (B-12)
- **Çift bölmesi** (çift rotasyonu):
  - Sermaye 1.000.000 TL; en fazla 5 aktif çift, eşit pay (YORUM; Tansu tek çift kullandı).
  - Her çift payı, ilk sinyale kadar nakittedir; sonra hep çiftin bir hissesindedir.
  - Boş pay nakitte kalır.

**Çift seçimi**, önceden yazılır (Sorgu S4, B-10):
- **Ne zaman ve neyden:** her yıl başında, evrendeki aynı sektörden hisseler arasından.
- **Ölçüt:** önceki 252 günde eşbütünleşme p < 0,05.
- **Sıralama:** p'ye göre açgözlü.
  - Bir hisse en fazla bir çiftte.
  - Aynı sektörden en fazla 2 çift.
  - β ≤ 0 olan çift elenir.
  - X/Y rolü sembol sırasından.
- **Yıl geçişi:** düşen çiftin pozisyonu kapanır; yine seçilen çift işlemsiz devam eder.
  (S2-25, S2-26, S2-27)
- **Sınama birimi:** bütün çift bölmesidir.
- **Tansu'nun çifti:** VAKBN–GARAN ayrıca gösterilir; kabul kararına girmez. AGROT–GARAN rotasyon
  değildir ve farklı sektördedir; listede yok.

**Faiz:** boştaki nakit, bir gün gecikmeli politika faizini kazanır (takvim günü, /365). (B4, B-8)

### 5.7 Karşılaştırma (asıl soru)
**Fazla getiri tanımı** (B4):
- İşlem seviyesi: işlemin getirisi − aynı tutma süresinde aynı evrenin eşit ağırlıklı sepetinin getirisi.
- Portföy seviyesi: günlük portföy getirisi − günlük karşılaştırma getirisi.

**Karşılaştırma grupları:**
- **K1 Eşleştirilmiş rastgele kural** (B5):
  - **Seçim:** rastgele sinyaller, kuralın kendi ön şartlarını sağlayan günlerden seçilir. Ön şart her
    aile için `KURALLAR.md` §3'te yazılıdır.
  - **Eşleştirme:** sayılar hisse başına eşleştirilir.
  - **Çıkış:** rastgele işlemler kuralın tam çıkış paketini uygular.
  - **İki tür:**
    - (a) aynı gün, başka hisse
    - (b) aynı hisse, aynı piyasa durumunda ±20 gün içinde başka gün
  - **EMA sıkışması için ayrıca:** "sıkışmasız aynı kırılım" kolu; sıkışmanın katkısını ayırır.
  - **Çift bölmesinde:** aynı çiftlerde, aynı sayıda geçiş, rastgele günlerde. İlk giriş günü gerçeğe
    eşitlenir. (Sorgu S12)
  - **Tekrar sayısı:** B ≥ max(1.000, 20·m), m = o ana kadarki deneme sayısı. Sabit 1.000 tekrarla
    50'den fazla denemede Holm kabulü imkânsızdır. Geliştirmede 200 tekrar. (B-14)
  - **p değeri:** tek yönlü; istatistik işlem başına ortalama fazla getiridir. Aile p'si iki türün
    büyüğüdür. (B-15)
- **K2 Aynı evrenin eşit ağırlıklı sepeti, maruziyet eşleşmeli** (B3b, B-13):
  - Sepetin o günkü ağırlığı = kuralın o günkü yatırımdaki payı; kalanı aynı faizi kazanır.
  - Böylece kural yalnız nakitte durduğu için öne ya da geriye düşmez.
  - Çift bölmesi için ayrıca aynı çiftlerin 50/50 tutulması.
- **K3 Faiz:** simülatörde boştaki nakit faiz kazandığı için portföy sonucu zaten faize karşı okunur.

Dolar bazı ilk sürümde yok.

### 5.8 Dönemler
- **2023 sonrası ayrılmış dönem yandı.** 2015–2026 bütünüyle geliştirme/doğrulama verisidir. (M8)
- **Doğrulama:** genişleyen pencereyle yıllık ileri yürüme. 2015–2017 ile başlar; her yıl bir sonraki yıl
  sınanır ve sonucu ayrı yazılır. (M7)
- **Yeni ayrılmış dönem = kural kaydından sonrası.** Kural, parametreleri ve kodunun parmak izi sadakat
  kontrolü bitince, ilk getiri koşusundan önce kayda geçer. Sonraki her değişiklik yeni denemedir.
  (M8, Sorgu S13)
- **Kâğıt üstü canlı dönem:** en az 6 ay **ve** en az 30 kapanmış işlem; işlem sayısı dolana kadar uzar.
  - Çift bölmesinde işlem sayısı yerine günlük fazla getiri serisi kullanılır.
  - Bu dönem yalnız büyük bozulmaları yakalar. Örnek: çift bölmesinde 6 ayda saptanabilir en küçük etki
    yıllık ≈ %56. (Sorgu S11, B-17)

### 5.9 Şans payı
- **Güven aralığı:** günlük portföy fazla getirisi üzerinde bloklarla yeniden örnekleme.
  - Blok uzunluğu = max(20, ortalama tutma süresi).
  - İşlemler birbirine bağımlı olduğu için bloklanır. (M5, B-16)
- **Örneklem:** en az 100 işlem **ve** en az 60 farklı sinyal günü. Bu örneklemle saptanabilecek en küçük
  etki raporda yazılır. (M5)
- **Ek gösterimler:** ortalamanın yanında medyan ve en iyi %5 işlem atılmış sonuç. (m2, M10)

### 5.10 Parametre sağlamlığı
Parametreler önceden yazılır (`KURALLAR.md` §3, YORUM satırları). Sonra küçük bir rastgele ızgarada
birlikte oynatılır; pozitif hücre oranı raporlanır. En iyi değer seçilmez. (m3)

### 5.11 Çoklu deneme düzeltmesi
- **Deneme günlüğü:** her koşu yazılır (`kayit/deneme.jsonl`): tarih, kural kimliği, veri anlık görüntüsü,
  git commit, tohum.
- **Holm:** p değerleri, o ana kadarki bütün benzersiz kural kimlikleriyle Holm düzeltmesinden geçer.
  Aynı kuralın tekrar koşusu yeni deneme değildir. (M6, C-6)

### 5.12 Kabul ölçütü (önceden yazılır)
Bir aile **Canlı** olur, ancak hepsi sağlanırsa:
1. İleri yürüme yıllarının birleşiminde K1'e göre fazla getiri pozitif, Holm düzeltmeli p < 0,05.
2. K2'ye göre portföy fazla getirisi pozitif.
3. Masraf %0,5'te de 1 ve 2 sağlanıyor.
4. Yılların en az %60'ında fazla getiri pozitif; en iyi %5 işlem atılınca sonuç hâlâ pozitif. (M10)
5. Örneklem şartı (5.9) ve sağlamlık şartı (5.10) sağlanıyor.
6. Kâğıt üstü canlı dönemde (5.8) fazla getiri, doğrulamadaki etkinin en az yarısı. (M7, M8)

**Ölçülemedi:** örneklem dolmazsa ya da saptanabilir en küçük etki %0,5 masrafın gidiş-dönüş tutarından
büyükse sonuç "geçmedi" değil "ölçülemedi"dir. (B-17)

Portföy kuralı (aileden bağımsız): en büyük düşüş %25'i, düşüşte kalma süresi 12 ayı geçerse aile
reddedilir. Geçmesi kanıt değildir. (m5)

İlk resmi koşudan önce boru hattı bir kez iki denetimden geçer (B-18):
- Sentetik boş veriyle yanlış kabul oranı ≤ %5.
- Enjekte edilmiş etkiyle güç ölçümü.

### 5.13 Veri kapıları
Getiri görülmeden yazılır; kural kaydına girer. (B-7)
- **Satır şartları:** her satırda düşük ≤ AOF ≤ yüksek ve düşük ≤ kapanış ≤ yüksek. Bozuk satır karantina
  sayılır.
- **Eşikler:** karantina hisse-gün oranı > %1 ya da ikinci kaynak uyuşmazlığı > %2 ise koşu "veri
  sorunlu" olur.
- **Günlük koşu:** 100 hisseden 5'ten fazlası inmezse koşu SORUNLU olur.

## 6. Günlük işleyiş (ilk sürüm)
1. **Görev Zamanlayıcı:** hafta içi 19:30'da `python -m tansu gunluk`.
   - Tanım dosyası depoda (`kurulum/`).
   - Kaçırılan koşu, bilgisayar açılınca çalışır.
   - Başarısızsa 4 saat boyunca saatte bir yeniden dener.
   - Saat Europe/Istanbul. (C-7)
2. **Veri:** tam indirme geçici klasöre yapılır. Kapılar geçerse yeni anlık görüntü olur; geçmezse kart
   üretilmez. (m6, C-4)
3. **Piyasa durumu etiketi:** yalnız bilgi. XU100 kapanış > SMA50 (YORUM). (B-19)
4. **Kartlar:** canlı ailelerin sinyalleri kart listesine (CSV: `;` ayraç, ondalık virgül, UTF-8 BOM)
   yazılır. Deneme aileleri varsayılan olarak gösterilmez. (P1)
5. **Kart içeriği:**
   - Hisse ve aile.
   - Referans fiyat (sinyal günü kapanışı) ve stop.
   - Uygulanan büyüklük: sermayenin yüzdesi ve 1.000.000 TL için adet.
   - Fiili risk.
   - Ailenin kanıt satırı. Örnek: "112 işlem, rastgele kurala göre fazla getiri −%0,2 (%95 aralık −%2,4
     ile +%2,0): ayırt edilemiyor".
   - Çift kartında "simülasyonda şu an X'te". (P1, P2, B-20)
6. **Açık kartlar ayrıca saklanmaz:** her gün sinyal gününden itibaren Adım ile yeniden hesaplanır. Günün
   kart çıktısı `kayit/kartlar.jsonl`'e yalnız eklenir; kâğıt üstü dönem geriye dönük değişmez. (C-5)
7. **`rapor/durum.txt` ilk satırı:** `TAMAM` / `SORUNLU` / `VERİ YOK`. Ardından son başarılı koşu saati
   ve bir Türkçe eylem cümlesi. Levent yalnız buna bakar.

## 7. Uygulama sırası
1. **Temizlik:**
   - Yahoo, vectorbt ve ön deneme kodu (`kanit.py`, `nabiz.py`, `veri.py`'nin Yahoo kısmı) ve testleri
     silinir.
   - Bağımlılıklar sabitlenir (C-2).
   - `.gitignore` ve `.gitattributes` düzeltilir (C-10).
2. **Veri deposu:** `kaynak` + `veri`.
   - İş Yatırım ham ve düzeltilmiş fiyat, olay tablosu, olay denetimi.
   - Veri kapıları, anlık görüntü.
   - borsapy karşılaştırması.
3. **Sadakat kontrolü** (`KURALLAR.md` §4): ham seriyle; getiriye bakılmaz.
   - KRDMD sıkışması çözüldü; aynı kod yeniden üretir.
   - VAKBN–GARAN Z formülü bulunamadı; YORUM kalır.
4. **Evren** (5.2) ve **göstergeler**.
5. **Kural kaydı ve hash** (5.8).
6. **Motor sınamaları** (5.3) → Adım + Motor.
7. **Simülatör** (iki bölme) + faiz + K2 (maruziyet eşleşmeli).
8. **K1 + istatistik + deneme günlüğü;** boru hattı denetimi (5.12).
9. **İki aileyi koş; rapor.** Kâğıt üstü canlı izleme ve Görev Zamanlayıcı başlar.
10. **Gerçek BIST100** KAP endeks değişikliklerinden (paralel iş).

## 8. Açık sorular
1. İş Yatırım ve borsapy kullanım koşulları, hız sınırları ve günlük yayın saati bilinmiyor.
2. KAP endeks değişikliği duyuruları 2015–2016'yı kapsıyor mu?
3. Tedbirli hisseler (brüt takas, tek fiyat) bedava veriyle ayırt edilebiliyor mu?
4. İşlemi kapanan sembollerin tam listesi bulunabilir mi?
5. ±%20 döneminde limit tabanı önceki kapanış mı? (±%10 döneminde doğrulandı.)
6. Sıkışma oranının paydası düşüş trendinde EMA200 mü en küçük EMA mı? KRDMD'de ikisi aynı.
7. Bireysel yatırımcı için vergi.

---

## Ek A: Eleştiri bulguları ve durumu

| Kimlik | Konu | Durum |
|---|---|---|
| B1 | Eşikle bedelsiz düzeltme veriyi bozar | 5.1: olay tablosu + karantina |
| B2 | Düzeltilmiş fiyatta seviye hesapları, geçmişin değişmesi | 4, 5.1: ham veri, anlık görüntü |
| B3, B3b | Hayatta kalan yanlılığı giderilemiyor; karşılaştırma tek taraflı | 5.2, 5.7 K2 |
| B4 | Fazla getiri tanımsız; endeks temettüsüz; nakit faizi yok | 5.6, 5.7 |
| B5 | Rastgele karşılaştırma adil değil, 5 tekrar az | 5.7 K1 |
| M1 | Aynı gün stop ve hedef | Hedef kalmadı; 5.3 |
| M2 | Stop yanlış tabandan | 5.3 |
| M3 | Masraf düşük | 5.4 |
| M4 | Taban kilidi, limit rejimi | 5.1, 5.3 |
| M5 | Bağımlılık, örneklem gücü | 5.9 |
| M6 | Çoklu deneme düzeltmesi yok | 5.11, 5.7 tekrar sayısı |
| M7 | Tek bölme | 5.8 |
| M8 | Ayrılmış dönem yandı | 5.8, 5.12.6 |
| M9 | Nabız stratejinin parçası | 4: kapı değil |
| M10 | Rejim, birkaç işleme bağımlılık | 5.9, 5.12.4 |
| M11, M12 | Likidite, pozisyon tavanı | 5.4, 5.6 |
| A1–A6 | Eksik modüller, Adım paylaşımı, vectorbt | 4 |
| P1–P5 | Yanıltıcı sunum, bedava veri sınırları, ad | 1, 2, 6, 5.1 |
| m1–m7 | Küçükler | dağınık |
