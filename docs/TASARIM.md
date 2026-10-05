# Tansu'dan esinlenen BIST sistemi: tasarım (taslak 7, 05.10.2026)

Geçmiş:
- Taslak 1, bağımsız bir eleştiriden geçti: 5 engelleyici, 12 büyük, 7 küçük bulgu.
- Taslak 2, bu bulguları işledi. Bulgu kimlikleri (B1, M3…) ekte.
- Taslak 4: ilk sorgu, 14 soru ("Sorgu Sn").
- Taslak 5: ikinci sorgu, 52 soru ("S2-n", `docs/sorgu/sorgu-2.md`).
- Taslak 6: bağımsız sorgu, 2.000 soru (`docs/sorgu/sonuc-3-4.md`; "B-n" tasarım, "C-n" altyapı).
- Taslak 7: bütün cevapların izlenmesi (`docs/sorgu/izleme/`). 1.561 madde tek tek taslak 6 ile
  karşılaştırıldı; 185 yeni madde karara bağlandı (`izleme/karar.md`). Etiket "İ: NN-NNN".

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

Önce sadakat, sonra kâr:
- Bir aile önce Tansu'nun gösterdiği haliyle sınanır.
- Bu hali 5.12'deki ölçütlerden birini geçemezse "tutmadı" sayılır.
- Tutmazsa değiştirilmiş hali yeni bir deneme sayılır ve deneme günlüğüne yazılır (5.11).
(Sorgu S2, İ: 10-100)

En olası sonuç, hiçbir kuralın kabul ölçütünü geçmemesidir. Bu bir başarısızlık değil, sistemin
normal çıktısıdır.
- Raporun ilk satırı "Hiçbir aile kabul ölçütünü geçmedi (0/N)" olabilir; birinci sınıf bir sonuçtur.
- "Ölçülemedi" ayrı bir sonuçtur (5.12).
- Ölçüt sonuca bakılarak gevşetilmez.
- Ölçüt değişirse tarihli kayıt düşülür ve bütün ayrılmış dönemler sıfırlanır.
(P3, B-17, İ: 17-008)

## 2. Tansu'nun düşünce yapısı

Kaynak: beyindeki 238 not, 214 görsel. Notların çoğu Claude özetidir; birinci el kaynak görsellerdir.
Tansu kodunu ve parametrelerini paylaşmaz. Bu yüzden her aile **Tansu'dan esinlenen bizim
yorumumuzdur**; ekranda "Tansu'nun sistemi" diye sunulmaz. (P5)

| İlke | Kaynaktaki karşılığı | Sistemde |
|---|---|---|
| Önce piyasanın havası | "Piyasanın Nabzı" raporu (NotebookLM), XU100 setup puanı (formülü yok) | Piyasa durumu etiketi; ilk sürümde kapı değil |
| Önce yer, sonra teyit | "zone → kırılım → likidite → teyit" | Aile = koşul + teyit (ilk sürümün iki ailesi bölge ailesi değil) |
| Her fırsat bir kart, durum etiketiyle | `AKTİF / TAMAMLANDI / BOZULDU` (Tansu'nun etiketleri) | Kart: `AKTİF / STOP / BOZULDU` (hedef yok) |
| Önce sermaye | %1 risk, adet = risk / 2ATR, acil stop | Risk |
| Tek sinyale güvenme | "ABCD'ye gözü kapalı güvenilmez" | Teyit şartı |
| Sınamadan inanma | "mutlaka backtest etmek lazım", negatif sonuçlarını da paylaşır | Kanıt |
| Basit ve sağlam | "Medyan temelli çalışın", "Yüksek Sharpe modeller ilk virajda patlar" | Medyan, sağlamlık sınaması |

(İ: 10-001, 10-054, 17-056)

## 3. Kapsam (ilk sürüm)

**Var:**
- Günlük veri, BIST100 benzeri evren, yalnız alış yönü.
- Piyasa durumu etiketi. Motoru ve girişi etkilemez; K1(b) örneklemesinde ve rapor bölmesinde
  kullanılır. (İ: 11-078)
- **2 aile** (`KURALLAR.md` §3): çift rotasyonu ve EMA sıkışması.
- Tansu'nun risk paketi (5.5), işlem motoru, portföy simülasyonu ve istatistik.
- Tek dosya HTML rapor, CSV kart ve işlem listeleri, `durum.txt`.

**Yok** (ilk aile kabul edilene kadar bekler, gereksiz katman):
- Streamlit ya da başka panel, Telegram, veritabanı.
- İz süren stop ve kısmi kâr (Ç2), süre çıkışı (Ç3).
- Dolar bazı karşılaştırma, Corwin–Schultz.
(Kesilecekler 1–6, C-1)

**İkinci dalga:**
- AB=CD. Tansu'nun SMRTG sınaması aşağı yönlü kalıplarla ve C fiyatından giriyor. BIST'te bireysel
  açığa satış pratik değil. Alış yönlü hali Tansu'nun gösterdiği kural olmaz. (B-1)
- AEFES kanal, AKFIS kurulumu ve fiili dolaşım taraması.

**Kapsam dışı:**
- 4 saatlik ve gün içi veri, emir defteri, opsiyon.
- Harmonik, Elliott, değerleme, otomatik emir.
- Sembol değişikliği ve birleşme sürekliliği. Verisi biten sembol 5.2 kuralıyla işlenir; nedeni
  bilinmeyenler raporda listelenir. (İ: 02-022)

## 4. Modüller

Her modülün dışarıya küçük bir yüzü var. İçi değişse de dışı değişmez. Paket düzdür (`tansu/`). (C-3)

| Modül | Girdi → çıktı | Not |
|---|---|---|
| `kaynak` | sembol, tarih aralığı → ham tablo | Ağa çıkan tek yer: İş Yatırım ve borsapy (yalnız faiz ve sektör). Ham alan adları (`HG_*`, `HGDG_*`) tek bir sözlükle proje adlarına çevrilir. (C-8, İ: 18-075) |
| `veri` | indirme → anlık görüntü; olay tablosu; veri kapıları | Ayrıntı aşağıda. (B2, B-2, B-7) |
| `evren` | tarih → o gün yeni giriş için taranabilecek hisseler | 5.2. |
| `gostergeler` | fiyat → EMA, SMA, ATR, piyasa durumu | Vektörel; sınamada ve canlıda aynı kod. Kütüphane yok. |
| `aileler` | hisse fiyatı → sinyal günleri | Tek hisse aileleri. |
| `cift` | çift fiyatları → hangi hissede olunacağı | Kendi döngüsü. |
| `motor` | Adım: (pozisyon, bugünkü mum) → pozisyon; Motor: sinyaller → işlemler | Mum, ön hesaplı ATR ve SMA250 sütunları olan bir gün satırıdır. **Sınama ve canlı günlük aynı Adım'ı kullanır.** (A5, İ: 11-010) |
| `simulator` | işlemler + bölme kuralı → sermaye eğrisi | Boştaki nakit faiz kazanır. (A2, B4) |
| `istatistik` | fazla getiri → güven aralığı, p değeri, Holm | statsmodels yalnız `coint` ve Holm için. |
| `kayit` | kural kaydı, deneme günlüğü, kart günlüğü, durum kayıtları | Yalnız ekleme. Getiri gösteren tek yol `kosu()`'dur: kural kaydı yoksa ya da hash uyuşmazsa tek Türkçe satırla durur. (C-6, İ: 15-074) |
| `rapor` | sonuçlar → HTML + CSV + `durum.txt` | Ayrıntı 6. bölümde. |
| `__main__` | `python -m tansu gunluk \| sinama \| sadakat \| kayit` | Ayrıntı aşağıda. (İ: 16-001, 16-008, 14-084, 16-062) |

**`veri` ayrıntısı** (İ: 01-094, 02-026, 11-044, 13-006, 13-011, 13-015):
- Anlık görüntü tek klasördür. İçinde:
  - fiyat (ham ve düzeltilmiş, uzun biçim, bütün semboller),
  - olay tablosunun ham JSON'u,
  - borsapy tabloları (faiz, sektör),
  - `manifest.json` (her dosyanın sha256'sı).
- Veri sürümü, anlık görüntü kimliğidir.
- Okuyucu anlık görüntüyü açarken manifesti doğrular; uyuşmazlık hatadır.
- Tarih sütunu saat dilimsiz saf tarihtir.
- Koşu, canlı borsapy'ye bağlı kalmaz.

**`__main__` ayrıntısı:**
- `gunluk` bayrak almaz. Bugünün tarihini parametre olarak alabilir (varsayılan bugün; test için).
- `sinama` geliştirmede 200 tekrar koşar; `sinama --son` 5.7'deki tam tekrar sayısını koşar.
- Yakalanmayan istisna günlüğe yazılır, çıkış kodu 1 olur.

**Bağımlılık yönü** tek yönlüdür, geri import yok (İ: 11-039):
`kaynak` → `veri` → `evren`, `gostergeler` → `aileler`, `cift` → `motor` → `simulator` → `istatistik`
→ `kayit` → `rapor` → `__main__`.

Takvim, fiyat günlerinden çıkar (İş Yatırım XU100 günleri). Maliyet tek bir sabittir.

**Motor kendi Adım döngümüzdür; vectorbt kullanılmaz.** Dolum kuralları (5.3) AOF'a ve gün
yükseği/düşüğüne koşullu. Ölçütler kısa kendi kodumuzdur. (A3, M1, S2-41, C-2)

**Kaynaklar** (`docs/arastirma/veri-kaynaklari.md`):
- **Fiyat:** İş Yatırım `HisseTekil`, anahtarsız.
  - Ham `HG_*` ve düzeltilmiş `HGDG_*` seriler.
  - Düzeltilmiş seri bedelsiz, bedelli ve brüt temettüyü kapsar.
  - Alanlar: kapanış, yüksek, düşük, AOF, hacim (TL), piyasa değeri, fiili dolaşım değeri, sermaye.
  - **Açılış yok.** 2000'den veri var.
- **Yahoo kullanılmaz.** (B-2)
- **Şirket olayları:** İş Yatırım `GetSermayeArttirimlari`, bütün kodlarıyla. Tarih hak kullanım günüdür.
- **Faiz:** borsapy TCMB politika faizi; 2015'ten tek seri. Yalnız değişim günlerini içerir. (B-8)
- **XU100 kapanışı ve takvim:** İş Yatırım `HisseTekil`'in `END_DEGER` alanı (endeks kodu 01; XU100
  olduğu bilet 02'de doğrulanır). Yalnız kapanış.
- **Sektör:** borsapy (KAP kaynağı); yılda bir okunur.
- **TradingView kaynaklı veri kullanılmaz.** Koşullar makineyle işlemeyi yasaklıyor.
- **Kullanım koşulları** (bilet 01, `docs/arastirma/kullanim-kosullari-fiyat-adimi.md`):
  - İş Yatırım'ın robots.txt dosyası `/_layouts/` yolunu yasaklıyor. Kullanım sözleşmesi bulunamadı.
  - Kişisel ve ticari olmayan kullanım sürer; ayak izi küçük tutulur:
    - hisse başına günde bir istek
    - istekler arası 1 sn
    - açık User-Agent
  - İş Yatırım engellerse ya da itiraz ederse indirme durur. Bu bilinen bir risktir.
  - TCMB kişisel kullanıma izin veriyor. KAP koşulları belirsiz.

## 5. Sınama yöntemi

Amaç: bir kuralın sonucunu **şanstan, piyasanın genel yükselişinden, enflasyondan ve veri
hatasından** ayırmak.

### 5.1 Veri
- **İndirme:** veri 2010'dan indirilir. İlk sinyal 30.11.2015; ±%20 limit rejiminin başı. (B-6)
- **Isınma:**
  - Tek hisse ailesi, hissenin kendi ilk gününden 500 işlem günü dolmadan sinyal vermez (EMA200,
    SMA250).
  - Çift ailesi 252 gün ister.
  - Gösterge penceresi dolmayan hissede sinyal yok; K1'de de aynı.
  (İ: 01-069, 03-068, 05-054, 07-065, 19-017, karar.md)
- **Seriler:**
  - Göstergeler, getiriler ve pozisyon durumu (giriş, stop, adet, düşük karşılaştırması) düzeltilmiş
    seriden (`HGDG`), tek ölçekte.
  - Fiyat limiti, kilit ve likidite TL tutarı ham seriden (`HG`).
  - Sadakat kontrolü ham seriyle; Tansu ham seri kullanıyor.
  (B2, B-2, İ: 07-017, 08-010)
- **Eksik gün:** NaN kalır, ileri doldurulmaz. O gün sinyal ve giriş yok; açık pozisyon son bilinen
  kapanışla taşınır. (İ: 19-003)
- **Olay denetimi:**
  - Olay tablosu çarpanı (`SHHE_FIYAT_AYAR_OR`) ham seriye uygulanır ve `HGDG` ile karşılaştırılır.
    Fark %0,5'i aşan gün uyarıdır; `HGDG` geçerli kalır.
  - Olay eşleştirmesi tablo tarihinin ±1 işlem günü penceresinde yapılır.
  (B1, B-2, İ: 02-024)
- **Fiyat limiti:**
  - Taban, önceki gün ham kapanışının ±L'sidir.
  - Olay gününde taban = önceki ham kapanış × olay çarpanı. Kilit ve karantina bu tabanla yargılanır.
    Bilinmeyen olay kodu ya da çarpanı 1 olan kayıt istisna sayılmaz.
  - L = %20 (30.11.2015 – 12.03.2020), %10 (13.03.2020 sonrası). Önceki kapanış tabanı ±%10 döneminde
    veriyle doğrulandı.
  (İ: 01-024, 02-033, 07-060)
- **Fiyat adımı:** tarih bazlı tablo. 06.11.2023'te değişti; veriyle doğrulandı, bkz.
  `docs/arastirma/kullanim-kosullari-fiyat-adimi.md`.

  | Fiyat (TL) | 06.11.2023 öncesi | 06.11.2023 ve sonrası |
  |---|---|---|
  | < 20 | 0,01 | 0,01 |
  | 20–50 | 0,02 | 0,02 |
  | 50–100 | 0,05 | 0,05 |
  | 100–250 | 0,10 | 0,10 |
  | 250–500 | 0,10 | 0,25 |
  | 500–1.000 | 0,10 | 0,50 |
  | 1.000–2.500 | 0,10 | 1,00 |
  | ≥ 2.500 | 0,10 | 2,50 (doğrulanmadı) |

  Sınama vakası: KONTR 08.07.2026. (İ: 01-023, 02-056, 05-043)
- **Karantina:**
  - Kapanıştan kapanışa o günkü limiti (+%0,5) aşan ve şirket olayıyla açıklanmayan her gün karantinaya
    girer.
  - O hisse 250 gün yeni sinyal üretmez.
  - Açık pozisyon son temiz AOF'ta kapanır ve sayılır.
  - Fiyat yamanmaz.
  - Aynı maske kural, K1 ve K2'ye uygulanır.
  - Rapor karantinalı hisse × gün sayısını ve oranını yazar.
  (B1, İ: 02-094)
- **Hacim:** `HACIM` TL'dir. Hacmi sıfır olan gün (durdurma) işlem günü değildir.
- **İkinci kaynak yok** (bilet 01 kararı):
  - borsapy fiyatı TradingView'den gelir. TradingView koşulları, ekranda göstermeden makineyle işlemeyi
    yasaklıyor.
  - Veri doğruluğunu olay denetimi (`HGDG` iç tutarlılığı) ve veri kapıları (5.13) taşır.
  - Bu bilinen bir zayıflıktır; P4 kısmen açık kalır.
- **Bugünkü veri:** son çubuğun tarihi bugün değilse ya da veri kapısı (5.13) kalırsa o gün kart
  üretilmez. (m6)

### 5.2 Evren ve hayatta kalan yanlılığı
- **Bedava, tarih bazlı BIST100 üyelik verisi yok.** Bugünkü listeyi geçmişe uygulamak sonuçları iyimser
  yapar. (B3)
- **Evren kuralı** (YORUM, bizim; Tansu'nun evren tanımı yok) (İ: 03-093, 03-004):
  - Ayın ilk işlem günü, **önceki ayın son kapanışındaki** piyasa değerine göre en büyük 100 hisse.
  - O tarihte işlem gören, yalnız pay hisseleri.
  - 60 günlük medyan TL hacimde en alttaki %20 önce elenir.
  - Aynı şirketin birden çok kodu varsa yalnız hacmi en yüksek kod alınır; bilinen çoklu kodlar elle
    listelenir.
  - Evren yalnız yeni girişi sınırlar. Evrenden çıkan hissenin açık pozisyonu kendi kuralıyla
    kapanır. (B-9)
- **İşlemi kapanan hisseler:** İş Yatırım bunları da veriyor, ama liste eksik.
  - Kapanan hissede açık pozisyon −%100 sayılır; nedeni bilinirse son fiyat.
  - 60 işlem gününden uzun durdurma kapanma sayılır.
  - Bulunamayan semboller raporda yazılır.
- **Sektör:** bugünkü sınıflamadan (borsapy). Kaba ve tarih bilgisiz; bilinen yanlılık. Sektörü
  olmayan hisse çifte girmez; bu yüzden çift bölmesi hayatta kalanlardan kurulur. (İ: 03-050)
- **Sonuç** (B3, B3b, İ: 03-084, 03-086):
  - Mutlak getiriler karar için kullanılmaz. Tek istisna 5.12 portföy kuralıdır; o da yalnız ret
    yönünde işler.
  - Göreli karşılaştırmalar (K1, K2) yorumlanır. Ama onlar da yanlılıktan tam arınmış değildir;
    yanlılığın yönü ölçülmedi.
- **Gerçek BIST100** KAP duyurularından çıkarılınca kurallar onda da koşulur. Duyurular yalnız değişiklik
  listesidir; üyelik bugünkü listeden geriye yürütülür. Dönem içi değişiklikler eksik olduğundan 2016-07
  öncesi kapsanmaz, sonrası da yaklaşıktır (bilet 16).

### 5.3 İşlem kuralları ve elle hesaplanmış örnekler
- **Sinyal ve giriş:**
  - Sinyal günün kapanışındadır.
  - İşlem fiyatı ertesi günün **ağırlıklı ortalama fiyatıdır (AOF)**; kaynakta açılış yok.
  - Sinyal günü kapanış SMA250 altındaysa ya da SMA250 hesaplanamıyorsa giriş yok.
  (S2-7, B-12, İ: 07-065)
- **Stop:** giriş fiyatından ve sinyal günü ATR'sinden hesaplanır. (M2, C10)
- **Giriş günü:** yalnız stop kontrol edilir.
- **Stop dolumu:** gün düşüğü ≤ stop ise dolum **min(stop, AOF)**. (B-4)
- **Kilitli gün:**
  - Kapanışı tavan fiyatında olan gün (bir fiyat adımı toleransla) giriş yok.
  - Kapanışı taban fiyatında olan gün çıkış ertesi güne kayar.
  - Duyarlılık sürümü: yalnız düşük = yüksek, hacim > 0 ve limit fiyatında olan gün.
  (M4, B-5, İ: 01-026, karar.md)
- **Düşen sinyal:** giriş günü yoksa ya da kilitli tavansa sinyal düşer, sonraki güne kaymaz. Sayısı
  raporda "iptal" olarak yazılır. (İ: 05-044, 19-055)
- **Aynı gün sırası:** aynı AOF gününde önce çıkışlar, sonra girişler işlenir. (İ: 08-015)
- **Yeni sinyal:** bir hissede pozisyon açıkken gelen yeni sinyal yeni işlem açmaz ve sayıma girmez.
  - SMA250 çıkışı bildirilmiş ama henüz dolmamış pozisyon açık sayılır.
  - Rastgele karşılaştırmada da aynı kural geçerlidir.
  (C9, B5d, İ: 07-079)
- **Reddedilen sinyal:** pozisyon yeri ya da nakit yüzünden reddedilen sinyal işlem sayısına girmez;
  sayısı raporda ayrı yazılır. (İ: 08-016)
- **Veri sonu:** veri bitince açık pozisyon son kapanıştan zorunlu çıkar. K1 ve K2 aynı kuralı
  uygular. (İ: 09-092)
- **İşlem günlüğü:** her işlemde "planlanan risk" ve "gerçekleşen kayıp" yazılır. (İ: 08-030)
- **Motor sınamaları** (kod yazılmadan önce, elle hesaplı) (İ: 07-085):
  - stopta çıkış
  - boşluklu stop
  - giriş günü stop
  - kilitli tavan girişi
  - kilitli taban çıkışı
  - ardışık kilit
  - SMA250 çıkışı
  - açık pozisyonda yeni sinyal
  - sinyalden sonra veri yok
  - stop kenarları (düşük = stop, yüksek = stop)
  - lot yuvarlama
  - %10 tavan
  - olay gününde açık pozisyon
  - karantinada açık pozisyon

### 5.4 Masraf ve likidite
- **Masraf:** sabit, her yönde %0,3 (komisyon, BSMV, kayma birlikte).
  - Sonuçlar %0,1 / %0,3 / %0,5 ile gösterilir.
  - Kabul için %0,5'te de geçmesi gerekir. (M3)
- **Likidite:** pozisyon, 10 günün medyan TL işlem tutarının %2'sini geçemez.
  - Pencere sinyal gününü kapsar, giriş gününü kapsamaz.
  - Kalan miktar ertesi gün alınmaz.
  - Rapor likidite tavanının bağladığı işlem oranını yazar.
  (M11, İ: 08-019, 08-021)
- **Valör modellenmez:** satış nakdi aynı gün kullanılır. (İ: 08-014)
- **Vergi:** sınamaya girmez; raporda not edilir.

### 5.5 Çıkış
Tansu'nun risk paketi (`kurallar/E` K1–K3; kaynak Tansu'nun paylaştığı infografik):
- **Acil stop:** giriş − 2 ATR; gün içinde dokunulursa çıkılır.
- **Gün sonu çıkış:** kapanış SMA250 altına inerse ertesi günün AOF'unda.
- **ATR:** uzunluk 14, Wilder ortalaması; ilk değer ilk 14 gerçek aralığın ortalaması; kendi kodumuz
  (YORUM). (İ: 19-025)
- **Hedef yok:** iki ailede de Tansu hedef vermedi.
- **Çift rotasyonu:** stop yok; karşı uçta diğer hisseye geçilir. Risk paketi bu bölmeye uygulanmaz.
  (Sorgu S3)
- **Aile kuralları:** giriş kuralları ve YORUM'lar `KURALLAR.md` §3'tedir.
- **İz süren stop ve kısmi kâr:** ikinci el kaynaklı; bir aile bu paketle kabul edildikten sonra denenir.

### 5.6 Portföy ve bölmeler
İlk sürümde her aile **kendi sermayesiyle ayrı** ölçülür. Sınama tek sürekli koşudur; sermaye yıldan
yıla taşınır. (Sorgu S6, İ: 08-083)

**Tek hisse bölmesi** (EMA sıkışması):
- Sermaye 1.000.000 TL, bileşik büyür. Özkaynak = nakit + pozisyonların kapanış değeri.
- İşlem başına %1 risk. Adet şu dört sınırın en küçüğüdür, aşağı yuvarlanır (İ: 08-013):
  - %1 risk adedi
  - %10 tavan
  - %2 likidite
  - nakit / (fiyat × (1 + masraf))
- Tek pozisyon en fazla sermayenin %10'u (YORUM, bizim); en fazla 10 pozisyon; kaldıraç yok.
- Aynı gün sinyal sayısı boş yeri aşarsa en likit önce. Likidite = 5.4'teki 10 günlük medyan TL
  tutarı; eşitlikte sembol adı alfabetik. (M12, İ: 03-064, 07-009, 08-017, 14-029)
- **%10 tavan çoğu gün %1 riskten daha bağlayıcıdır.** 2 ATR çoğu hissede fiyatın %3–7'si, bu yüzden
  fiili risk ≈ %0,6–0,8 olur. Rapor tavanın bağladığı işlem oranını ve gerçekleşen riski yazar. (B-12)

**Çift bölmesi** (çift rotasyonu):
- Sermaye 1.000.000 TL; en fazla 5 aktif çift.
- Çift payları yıl başında eşittir; yıl içinde dengeleme yok (YORUM; Tansu tek çift kullandı).
  (İ: 08-056)
- Her çift payı, ilk sinyale kadar nakittedir; sonra hep çiftin bir hissesindedir. Boş pay nakitte kalır.
- Bacaklardan biri kilitliyse geçiş yapılmaz. Sinyal ertesi gün yeniden değerlendirilir; eski sinyal
  taşınmaz. (İ: 04-068)
- Bacaklardan biri karantinadaysa çift o pencerede girişsiz kalır; açık bacak son temiz AOF'ta kapanır.
  (İ: 02-082)
- Çiftin hissesi kapanırsa pay 5.2 kuralıyla kapanır ve yıl sonuna kadar nakitte faiz kazanır.
  (İ: 03-060)
- Bu bölmede "işlem", geçişten geçişe tutuş dönemidir. (İ: 08-058)

**Çift seçimi** önceden yazılır (Sorgu S4, B-10):
- **Ne zaman:** her yıl, yılın ilk işlem günü kapanışında, o günkü evrenle. Çıkışlar ve girişler ertesi
  günün AOF'unda. (İ: 03-051, 08-054)
- **Neyden:** aynı sektördeki hisseler. 252 işlem günü verisi olmayan hisse aday olmaz. (İ: 04-094)
- **Ölçüt:** önceki 252 günde eşbütünleşme p < 0,05. 252 günlük seçim penceresi YORUM'dur; Z
  penceresinden bağımsızdır. (İ: 04-008)
- **Sıralama:** p'ye göre açgözlü.
  - Bir hisse en fazla bir çiftte.
  - Aynı sektörden en fazla 2 çift.
  - β ≤ 0 olan çift elenir.
  - X/Y rolü sembol sırasından.
- **Yıl geçişi:** düşen çiftin pozisyonu kapanır; yine seçilen çift işlemsiz devam eder.
- **Çift çıkmayan yıl:** hiç çift seçilmeyen yıl "işlem yok" diye işaretlenir ve 5.12.4'ün paydasından
  çıkar. (İ: 08-053)
- **Sınama birimi:** bütün çift bölmesidir.
- **Tansu'nun çifti:** VAKBN–GARAN ayrıca gösterilir. Bütün dönem boyunca sabit çifttir, seçim kuralı
  yoktur; aynı sinyal ve masraf kuralını uygular. Kabul kararına girmez. AGROT–GARAN rotasyon değildir
  ve farklı sektördedir; listede yok. (İ: 04-029)

**Faiz:** boştaki nakit, bir gün gecikmeli politika faizini kazanır (takvim günü, /365). Rapor faiz
serisinin kaynağını ve son değişim tarihini yazar; seri boşsa koşu SORUNLU olur. (B4, B-8, İ: 08-071)

### 5.7 Karşılaştırma (asıl soru)

**Fazla getiri tanımı** (B4):
- **İşlem seviyesi:** işlemin getirisi − aynı tutma süresinde aynı evrenin eşit ağırlıklı sepetinin
  getirisi. Sepet getirisi işlemin giriş ve çıkış AOF günlerinden hesaplanır. (İ: 02-083)
- **Portföy seviyesi:** günlük portföy getirisi − günlük karşılaştırma getirisi.

**K1. Eşleştirilmiş rastgele kural** (B5):
- **Seçim:**
  - Rastgele sinyaller, kuralın kendi ön şartlarını sağlayan günlerden seçilir.
  - Ön şart her aile için `KURALLAR.md` §3'te yazılıdır.
  - Uygun gün kümesi gereken sayıdan küçükse hata verilir; sessizce kırpılmaz. (İ: 14-039)
- **Simülasyon:** rastgele işlemler aynı simülatörden geçer: aynı AOF girişi, aynı giriş filtreleri
  (kilitli tavan, SMA250, likidite), aynı boyutlandırma, faiz, masraf, pozisyon sınırı ve çıkış paketi.
  Kilitli tavandan kaçan sinyal sayısı raporlanır. (İ: 07-041, 08-022, 09-086)
- **İki tür:**
  - (a) Aynı gün, başka hisse. Sayı gün başına korunur; hisseler o günün ön şartlı havuzundan çekilir.
    (İ: 09-003)
  - (b) Aynı hisse, aynı piyasa durumunda ±20 gün içinde başka gün.
- **EMA sıkışması için ayrıca:** "sıkışmasız aynı kırılım" kolu. Sıkışmanın katkısını ayırır.
- **Çift bölmesinde:**
  - Aynı çiftlerde, aynı sayıda geçiş, rastgele günlerde. İlk giriş günü gerçeğe eşitlenir.
  - Bu karşılaştırma yalnız Z zamanlamasını ölçer; çift seçiminin değeri K2 ile okunur.
  (Sorgu S12, İ: 09-015)
- **Tekrar sayısı:**
  - B ≥ max(1.000, 200·m); m = o ana kadarki deneme sayısı. Daha azıyla p tabanı Holm eşiğini
    aşamaz.
  - Geliştirmede 200 tekrar; bu p'ler Holm'a girmez.
  (B-14, İ: 15-078, 09-009)
- **p değeri:**
  - p = (1 + k) / (1 + B); k = gerçek kuraldan iyi ya da eşit rastgele tekrar sayısı.
  - Tek yönlü; istatistik işlem başına ortalama fazla getiridir.
  - Aile p'si iki türün büyüğüdür.
  (B-15, İ: 19-069)

**K2. Aynı evrenin eşit ağırlıklı sepeti, maruziyet eşleşmeli** (B3b, B-13):
- **Kuruluş:** sepet ay başında evrenle eşit ağırlıklı kurulur, AOF'tan AOF'a. Ay başı evren değişimi ve
  dengeleme %0,3 masraf öder. Sepette kapanan hisse 5.2 kuralıyla işlenir. (İ: 03-065, 03-066, 08-048,
  09-019, 09-020)
- **Maruziyet:** sepetin yatırımdaki payı her gün kuralın o günkü yatırımdaki payına eşitlenir; kalanı
  aynı faizi kazanır. Bu eşitleme masrafsızdır (YORUM).
- **Çift bölmesi:**
  - Kabul, evren sepetiyle (K2) verilir.
  - Aynı çiftlerin 50/50 tutulması yalnız tanısaldır: yılın ilk işlem gününde bir kez alınır, yıl sonuna
    kadar tutulur, dengeleme yok.
  (İ: 04-051, 04-057)

**K3. Faiz:** simülatörde boştaki nakit faiz kazandığı için portföy sonucu zaten faize karşı okunur.

Dolar bazı ilk sürümde yok.

### 5.8 Dönemler
- **2023 sonrası ayrılmış dönem yandı.** 2015–2026 bütünüyle geliştirme/doğrulama verisidir. (M8)
- **Yıllık bölme:**
  - Parametreler sabittir; yıllık bölme yalnız çift seçimini yeniler. Kâğıt üstü dönemin yerine
    geçmez.
  - Tek sürekli koşunun eğrisi yıllara kesilir. Yıllık fazla getiri, o yıldaki günlük portföy fazla
    getirisinin toplamıdır.
  - Tamamlanmamış yıl (2026) 5.12.4'ün paydasından çıkar ve ayrıca gösterilir.
  (M7, İ: 09-025, 08-083, 09-027)
- **Kural kaydı** (M8, Sorgu S13, C-6, İ: 15-006, 15-016, 09-061):
  - **Ne zaman:** sadakat kontrolü bitince, ilk getiri koşusundan önce kayda geçer. Bundan sonrası
    yeni ayrılmış dönemdir. Sonraki her değişiklik yeni denemedir.
  - **Hash kapsamı:** elle yazılmış kod dosyaları listesi (`KOD_DOSYALARI`: aileler, cift, gostergeler,
    motor, simulator ve K1 kodu), kural parametreleri ve ızgara tanımı.
  - **Kod hash'i** kaynağın `ast.dump` sha256'sıdır; yorum ve boşluk değişmez.
  - **Hash dışı:** tekrar sayısı, tohum, blok uzunluğu, masraf senaryoları; günlükte ayrı alan olarak
    yazılır.
  - **Kapsam testi:** her `tansu/*.py` ya `KOD_DOSYALARI`'nda ya `HASH_DISI`'nda olmalı.
- **Kâğıt üstü canlı dönem** (Sorgu S11, B-17, İ: 09-074):
  - En az 6 ay **ve** en az 30 kapanmış işlem; işlem sayısı dolana kadar uzar.
  - Çift bölmesinde işlem sayısı yerine günlük fazla getiri serisi kullanılır.
  - Tek bakış: dönem bitince bir kez değerlendirilir, erken durdurma yok.
  - 12 ayda dolmazsa sonuç "Ölçülemedi"dir.
  - Bu dönem yalnız büyük bozulmaları yakalar. Örnek: çift bölmesinde 6 ayda saptanabilir en küçük etki
    yıllık ≈ %56.

### 5.9 Şans payı
- **Güven aralığı** (M5, B-16, İ: 09-037):
  - Günlük portföy fazla getirisi üzerinde bloklarla yeniden örnekleme yapılır.
  - Blok uzunluğu = max(20, ortalama tutma süresi).
  - Aralık 2,5 ve 97,5 yüzdeliktir.
  - Aralık yalnız rapordur; karar 5.12'den verilir.
- **Örneklem** (M5, İ: 09-046, 09-047):
  - Tek hisse: en az 100 işlem **ve** en az 60 farklı sinyal günü.
  - Çift bölmesi: en az 100 geçiş **ve** 60 farklı geçiş günü.
  - Saptanabilecek en küçük etki günlük portföy serisinden hesaplanır ve raporda yazılır.
- **Ek gösterimler:** ortalamanın yanında medyan ve en iyi %5 işlem atılmış sonuç (işlemler sıralanır,
  üstten ⌈0,05·n⌉ işlem atılır). (m2, M10, İ: 19-070)

### 5.10 Parametre sağlamlığı
Parametreler ve ızgara önceden yazılır (`KURALLAR.md` §3). Kurallar:
- Izgara hücreleri birlikte oynatılır. En iyi değer seçilmez.
- **Pozitif hücre:** K1'e göre ortalama fazla getiri > 0, %0,3 masrafla; p aranmaz. (İ: 09-064)
- **Sağlamlık şartı:** pozitif hücre oranı ≥ %60. (İ: 04-089, karar.md)
- Bu oran bir olasılık değildir; hücreler birbirine bağımlıdır. (İ: 05-096)
- Izgara hücreleri ve masraf senaryoları Holm'daki deneme sayısına girmez. (m3, İ: 09-056)

### 5.11 Çoklu deneme düzeltmesi ve deneme günlüğü

**Deneme günlüğü:** `kayit/deneme.jsonl`, yalnız ekleme. (M6, C-6, İ: 15-044, 15-046, 15-070, 12-030,
20-003, 13-034)
- **Satır başlangıcı ve bitişi:** her koşu önce `olay=basladi`, sonra `olay=bitti` satırı yazar.
  `bitti` satırı olmayan `basladi` de deneme sayılır.
- **Alanlar:**
  - tarih (UTC ISO), `kosu_id`, `kural_id`
  - `kod_hash`, `param_hash`
  - anlık görüntü kimliği ve manifest sha256'sı
  - parametrelerin tam JSON kopyası
  - `git_commit`, tohum, tekrar sayısı
  - ham p, masraf düzeyi başına sonuç
  - ortam: Python ve kütüphane sürümleri, `requirements.lock.txt` sha256'sı
  - `resmi` ve `kirli` bayrakları
- **`tur` alanı:**
  - `kayit`, `deneme`, `destek` (ızgara, yeniden üretim, sınama), `sadakat`.
  - `duzeltme`: hedef koşu ve yeni değer yazılır; asıl satır değişmez.
  - Holm yalnız `deneme` satırlarını sayar.
- **Silme yasağı:** günlükte adı geçen anlık görüntü silinmez.
- **Başlangıç denetimi:** koşu başında manifest yeniden hash'lenir; uyuşmazsa koşu durur.

**Holm** (İ: 15-052, 15-065, 09-051, 15-076, 19-043):
- Her kural kimliği için tek p girer: ilk resmi koşunun %0,5 masrafta K1 iki türünün büyük p'si.
- Geliştirme koşuları `resmi:false` yazılır ve m'yi şişirmez.
- Kabul kararı, kabul anındaki m ile donar; sonradan artan m eski kararı geri almaz.
- Rapor başlığı m'yi ve Holm hesap tarihini yazar; Holm rapor üretilirken yeniden hesaplanır.
- Aynı tohum ve aynı anlık görüntüyle iki koşu aynı özeti verir (tek test).

### 5.12 Kabul ölçütü (önceden yazılır)

**Durumlar:** Deneme → Kâğıt → Canlı. (İ: 09-072, 11-082)
- **Kâğıt:** ölçüt 1–5'i geçen aile kart üretir; kâğıt üstü dönem başlar.
- **Canlı:** ölçüt 6'yı da geçen aile.
- **Kayıt:** durumu kod hesaplar; `kayit` yalnız-ekleme satırıyla yazar.
- **Para:** para kararı Levent'indir.

**Ölçütler:**
1. İleri yürüme yıllarının birleşiminde K1'e göre fazla getiri pozitif, Holm düzeltmeli p < 0,05.
2. K2'ye göre portföy fazla getirisi pozitif.
3. Masraf %0,5'te de 1 ve 2 sağlanıyor.
4. Yılların en az %60'ında fazla getiri pozitif; en iyi %5 işlem atılınca sonuç hâlâ pozitif. (M10)
5. Örneklem şartı (5.9) ve sağlamlık şartı (5.10) sağlanıyor.
6. Kâğıt üstü canlı dönemde (5.8) fazla getiri, doğrulamadaki etkinin en az yarısı. (M7, M8)

**Ölçülemedi:** örneklem dolmazsa ya da saptanabilir en küçük etki %0,5 masrafın gidiş-dönüş tutarından
büyükse sonuç "geçmedi" değil "ölçülemedi"dir. (B-17)

**Rapor tablosu:** rapor her aile için 6 ölçütün geçti/kaldı durumunu ve değerini tablo olarak verir.
Genel "Geçti" yalnız hepsi sağlanınca yazılır. (İ: 17-079)

**Portföy kuralı** (aileden bağımsız) (m5, İ: 08-087, 08-090, 19-071):
- En büyük düşüş %25'i ya da düşüşte kalma süresi 12 ayı geçerse aile reddedilir. Geçmesi kanıt
  değildir.
- Düşüş nominal TL özkaynak eğrisinde, %0,5 masraflı ve faizli eğride ölçülür.
- Düşüşte kalma = eğrinin önceki zirvenin altında kaldığı en uzun ardışık takvim süresi, kapanış
  bazlı.

**Boru hattı denetimi:** ilk resmi koşudan önce bir kez yapılır (B-18):
- Sentetik boş veriyle yanlış kabul oranı ≤ %5.
- Enjekte edilmiş etkiyle güç ölçümü.

### 5.13 Veri kapıları
Getiri görülmeden yazılır; kural kaydına girer. (B-7, İ: 19-015)
- **Satır ihlali:** düşük ≤ AOF ≤ yüksek ve düşük ≤ kapanış ≤ yüksek sağlanmazsa karantina.
- **Yapısal ihlal:** bozuk sıra, tekrar eden gün ya da ortada NaN koşuyu durdurur.
- **Oran eşikleri:** karantina hisse-gün oranı > %1 ya da olay denetimi farkı olan gün oranı > %2 ise
  koşu "veri sorunlu" olur.
- **Eksik indirme:** 100 hisseden 5'ten fazlası inmezse koşu SORUNLU olur.

## 6. Günlük işleyiş (ilk sürüm)

1. **Görev Zamanlayıcı** (C-7, İ: 16-012, 16-035, 11-086):
   - Hafta içi 19:30'da `python -m tansu gunluk`. Tanım dosyası depoda (`kurulum/`).
   - Ayarlar: yalnız oturum açıkken (parolasız), uyandırma kapalı, kaçırılanı çalıştır, çakışmayı yok
     say, en fazla 1 saat, çalışma klasörü depo kökü, yalnız ağ varken.
   - Başarısızsa 4 saat boyunca saatte bir yeniden dener. Hata ya da kapı başarısızlığında çıkış kodu
     ≠ 0 olur.
   - `durum.txt`'teki son başarılı koşu bugünse `gunluk` hiçbir şey yapmadan çıkar.
   - Saat Europe/Istanbul.
2. **Veri** (m6, C-4, İ: 10-074, 18-071):
   - Tam indirme geçici klasöre yapılır. Kapılar geçerse yeni anlık görüntü olur; geçmezse kart
     üretilmez.
   - Koşu 18:15'ten önce başlarsa kart üretilmez (yarım çubuk riski).
   - Kaynak erişilemezse sınama eski anlık görüntülerle sürer; yalnız canlı kart durur.
   - Günlük anlık görüntüler 30 gün sonra silinir; deneme günlüğünde adı geçenler hiç silinmez.
     (İ: 11-061)
3. **Piyasa durumu etiketi:** yalnız bilgi. XU100 kapanış > SMA50 (YORUM). (B-19)
4. **Kartlar** (P1, İ: 17-049, 17-050, 17-087):
   - Kâğıt ve Canlı ailelerin sinyalleri her gün yeni bir CSV dosyasına yazılır:
     `rapor/kartlar-YYYYMMDD.csv` (`;` ayraç, ondalık virgül, UTF-8 BOM).
   - Deneme aileleri gösterilmez.
   - Sinyal yoksa yalnız başlık satırı yazılır. CSV hiç yoksa koşu çalışmamıştır.
   - Raporda başlık altında sabit uyarı: "Tansu'dan esinlenen yorum".
5. **Kart içeriği** (P1, P2, B-20, İ: 17-041, 01-079, 07-090, 08-009, 08-098, 09-041, 17-010, 10-051):
   - **Sabit sütunlar:** Tarih; Hisse; Aile; Durum; Referans; Stop; Pozisyon %; Adet; Fiili risk; Likidite
     sınırı TL; Kanıt; Kaynak.
   - **Referans:** sinyal günü kapanışı, ham TL olarak (düzeltilmiş seviye × ham/düzeltilmiş oranı).
   - **Stop:** "tahmini" etiketlidir (referans − 2 ATR). Gerçek stop, giriş dolunca Adım'da hesaplanır.
   - **Durum:** AKTİF / STOP / BOZULDU.
   - **Kanıt satırı:** aralık birimi ve yöntemi yazılır. %95 aralık sıfırı içeriyorsa "ayırt edilemiyor"
     yazar; p, Holm p ve toplam deneme sayısı raporun "Ayrıntı" bölümündedir.
   - **Kanıt örneği** (Kâğıt aile): "Kâğıt · 148 işlem · rastgele kurala göre işlem başına fazla getiri
     +%0,9 (günlük seri, blok bootstrap %95 aralık +%0,2 ile +%1,6) · kâğıt dönem 3/6 ay".
6. **Açık kartlar ayrıca saklanmaz:** her gün sinyal gününden itibaren Adım ile yeniden hesaplanır. Günün
   kart çıktısı `kayit/kartlar.jsonl`'e yalnız eklenir; kâğıt üstü dönem geriye dönük değişmez. (C-5)
7. **`rapor/durum.txt`** (İ: 16-036, 16-070, 13-082, 17-048):
   - İlk satır: `TAMAM` / `SORUNLU` / `VERİ YOK` / `BUGÜN ÇUBUK YOK` (tatil, çıkış 0).
   - Ardından: son başarılı koşu saati, anlık görüntü kimliği, son çubuk tarihi, sembol sayısı ve bir
     Türkçe eylem cümlesi.
   - Levent yalnız buna bakar.
   - `durum.txt` ve CSV'ler geçici dosyaya yazılıp `os.replace` ile taşınır. CSV Excel'de açık olduğu
     için yazılamazsa durum SORUNLU olur: "CSV açık, kapatıp yeniden çalıştır".
8. **Rapor** (İ: 17-006, 17-007, 17-074, 17-077, 17-084):
   - Dosya adı `rapor/rapor-YYYYMMDD-HHMM.html`; üstüne yazılmaz.
   - Başlıkta koşu kimliği, anlık görüntü, kod hash'i, m ve Holm tarihi.
   - Kabul tablosu (5.12).
   - Tek bir "Uyarılar" bölümü: karantina, bulunamayan semboller, tavan ve likidite bağlama oranları,
     olay denetimi farkları, iptal ve reddedilen sinyaller. Boşsa "Uyarı yok".
   - İşlem listesi `rapor/islemler-<koşu>.csv`: hisse, aile, giriş/çıkış tarihi ve fiyatı, çıkış
     nedeni, getiri.
   - Sayı biçimi tek bir yardımcıdan gelir: yüzde virgüllü (`locale` yok); TL raporda nokta binlik,
     CSV'de binliksiz; tarih ISO.

## 7. Uygulama sırası

1. **Temizlik:** tamamlandı (05.10).
2. **Veri deposu:** `kaynak` + `veri`.
   - Kullanım koşulları ve fiyat adımı: tamamlandı (bilet 01, 05.10).
   - İş Yatırım ham ve düzeltilmiş fiyat, XU100 kapanışı, olay tablosu, olay denetimi.
   - Veri kapıları, anlık görüntü, borsapy faiz ve sektör tabloları.
3. **Sadakat kontrolü** (`KURALLAR.md` §4): ham seriyle; getiriye bakılmaz. Sonuç `docs/sadakat.md`'ye
   yazılır.
4. **Evren** (5.2) ve **göstergeler**.
5. **Kural kaydı ve hash** (5.8).
6. **Motor sınamaları** (5.3) → Adım + Motor.
7. **Simülatör** (iki bölme) + faiz + K2.
8. **K1 + istatistik + deneme günlüğü;** boru hattı denetimi (5.12).
9. **İki aileyi koş; rapor.** Kâğıt üstü izleme ve Görev Zamanlayıcı başlar.
10. **Gerçek BIST100** KAP endeks değişikliklerinden (paralel iş).

## 8. Açık sorular
1. İş Yatırım: kullanım sözleşmesi bulunamadı; robots.txt `/_layouts/`'u yasaklıyor (bilinen risk, 4).
   Hız sınırı ve günlük yayın saati bilinmiyor. KAP koşulları okunamadı.
2. ~~KAP endeks değişikliği duyuruları 2015–2016'yı kapsıyor mu?~~ Cevap (bilet 16, 05.10.2026): hayır.
   İlk BIST 100 dönemsel duyurusu 17.06.2016'dır (dönem 01.07.2016); 2015 ve 2016 ilk yarı KAP'ta yok.
   Dönemsel duyurular 2016-07'den 2026-10'a 42 dönemi kapsar ama yalnız alınan/çıkarılan listesi verir;
   dönem içi değişiklikler okunamadı. Dosya ve boşluklar: `docs/arastirma/bist100_kap_*.csv`.
3. Tedbirli hisseler (brüt takas, tek fiyat) bedava veriyle ayırt edilebiliyor mu?
4. İşlemi kapanan sembollerin tam listesi bulunabilir mi?
5. 13.03.2020 öncesinde limit bütün paylarda ±%20 mi, bazı pazarlarda ±%15 mi (ikincil kaynak)? Limit
   fiyatı adıma içe mi yuvarlanıyor? Bilet 03'te veriyle ölçülür. (±%10 döneminde taban = önceki
   kapanış doğrulandı.)
6. Sıkışma oranının paydası düşüş trendinde EMA200 mü en küçük EMA mı? KRDMD'de ikisi aynı.
7. Bireysel yatırımcı için vergi.
8. `HACIM` toptan ya da çapraz işlemleri içeriyor mu? İçeriyorsa medyan şişkin olabilir. (İ: 08-027)
9. Faiz serisi bir haftalık repo mu? (İ: 08-071)
10. Fiyat adımı tablosunun 2.500 TL üstü bandı ve 2015–2016'daki 100 TL altı bantlar (5.1) veride
    görülmedi.

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
| M9 | Nabız stratejinin parçası | 3, 4: kapı değil |
| M10 | Rejim, birkaç işleme bağımlılık | 5.9, 5.12.4 |
| M11, M12 | Likidite, pozisyon tavanı | 5.4, 5.6 |
| A1–A6 | Eksik modüller, Adım paylaşımı, vectorbt | 4 |
| P1–P5 | Yanıltıcı sunum, bedava veri sınırları, ad | 1, 2, 6, 5.1 |
| m1–m7 | Küçükler | dağınık |
