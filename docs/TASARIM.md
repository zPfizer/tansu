# Tansu'dan esinlenen BIST sistemi: tasarım (taslak 7, 05.10.2026)

Geçmiş:
- Taslak 1, bağımsız bir eleştiriden geçti: 5 engelleyici, 12 büyük, 7 küçük bulgu.
- Taslak 2, bu bulguları işledi. Bulgu kimlikleri (B1, M3…) ekte.
- Taslak 4: ilk sorgu, 14 soru ("Sorgu Sn").
- Taslak 5: ikinci sorgu, 52 soru ("S2-n", `docs/sorgu/sorgu-2.md`).
- Taslak 6: bağımsız sorgu, 2.000 soru (`docs/sorgu/sonuc-3-4.md`; "B-n" tasarım, "C-n" altyapı).
- Taslak 7: bütün cevapların izlenmesi (`docs/sorgu/izleme/`). 1.561 madde tek tek taslak 6 ile
  karşılaştırıldı; 185 yeni madde karara bağlandı (`izleme/karar.md`). Etiket "İ: NN-NNN".

Çalışma kuralı (belge koddan önce gelir): `AGENTS.md`.
Terimler `GLOSSARY.md`'dedir.

**Sürüm sınırı (#82, S01):** Aşağıdaki mevcut uygulama anlatımı `legacy_portfoy_v1` ve
`legacy_tansu_v1` politikalarını korur. Yeni motorun davranış sözleşmesi ve parçaların uygulama durumu
§5.15'tedir. Normal komutlar mevcut politikalarını sürdürür; yeni parçalar açık seçimle kullanılır.
Eski sonuç yeni politikayla yeniden etiketlenmez. Dayanak: Levent 18.10,
"Ortak para falan yok. Her işlem ayrı gibi düşün."; §5.15 kaynak ve uyumluluk kaydı.

**05.10 ön denemesi (ilk kod ve `rapor/kanit-20261005.md`) bu belgeden önce yazıldı. Kanıt değildir;
rakamları hiçbir kararda kullanılmaz.** (C7)

**Bölüm → kod** (`tansu/` içindeki `TASARIM <bölüm>` atıflarından, 07.10; test dosyası `tests/test_<modül>.py`).
Bir bölümün kodunu bulmak için: `grep -n "TASARIM 5.7" tansu/*.py`.

| Bölüm | Modüller |
|---|---|
| 3 Kapsam | `__main__`, `cift`, `gostergeler` |
| 4 Modüller | `kaynak`, `veri`, `kayit`, `sadakat` |
| 5.1 Veri | `veri`, `aileler`, `motor` |
| 5.2 Evren | `evren`, `veri`, `simulator`, `ciftbolme`, `gunluk` |
| 5.3 İşlem kuralları | `motor` |
| 5.4 Masraf | `simulator` |
| 5.5 Çıkış | `motor`, `gostergeler` |
| 5.6 Portföy ve bölmeler | `simulator`, `ciftbolme`, `motor`, `rapor`, `veri` |
| 5.7 Karşılaştırma | `istatistik`, `simulator`, `kayit`, `motor` |
| 5.8 Dönemler | `gunluk` |
| 5.9 Şans payı | `istatistik` |
| 5.10 Parametre sağlamlığı | `saglamlik`, `istatistik`, `kayit` |
| 5.11 Deneme günlüğü | `kayit` |
| 5.12 Kabul ölçütü | `denetim`, `istatistik`, `kayit`, `rapor`, `__main__` |
| 5.13 Veri kapıları | `veri`, `kaynak`, `gunluk`, `rapor`, `simulator` |
| 5.14 Tansu sınaması | `tansusinama`, `__main__` |
| 5.15 Motor davranış sözleşmesi | `aileler`, `aktarim`, `ciftbolme`, `deneme`, `gostergeler`, `gunluk`, `islem_riski`, `katalog`, `kayit`, `motor`, `simulator`, `tansusinama`, `veri` |
| 6 Günlük işleyiş | `gunluk`, `rapor`, `kayit`, `gostergeler` |

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

Kaynak: beyindeki Tansu havuzu (sayı `docs/kaynak-dokumu.md` başındadır). Birinci el kaynak notların Ham metni ve görselleridir
(GLOSSARY "Kaynak"); notların öbür bölümleri yapay zekâ özetidir ve ikinci eldir.
Tansu bazı parametreleri ve kod parçalarını paylaşır (gorsel-paket-67 görseli: tolerans %1.2, en az 3 gün;
gorsel-paket-54 Ham: Z ±2.0, çıkış 0.5; tweet-atr-risk-butcesi-position-sizing-stop-loss Ham: 2 ATR stop kodu;
gorsel-paket-106 Ham: "Ben 5-8-13 kullandım"), ama kodlu tam bir kural paylaşmaz. Bu yüzden her aile **Tansu'dan esinlenen bizim
yorumumuzdur**; ekranda "Tansu'nun sistemi" diye sunulmaz. (P5)

| İlke | Kaynaktaki karşılığı | Sistemde |
|---|---|---|
| Önce piyasanın havası | "Piyasanın Nabzı" raporu (NotebookLM), XU100 setup puanı (formülü yok) | Piyasa durumu etiketi (YORUM); ilk sürümde kapı değil |
| Önce yer, sonra teyit | yapı → bölge → kırılım → likidite → 4 saatlik teyit (Ham, kaynak-tansu-2095201144544846208) | Aile = koşul + teyit (ilk sürümün iki ailesi bölge ailesi değil) |
| Her fırsat bir kart, durum etiketiyle | Durum, Reaksiyon, Giriş ve Stop ayrı alanlar (araç, G02/g1) | İlk sürüm kartı pozisyon durumunu gösterir; harmonik formasyon durumunu ve reaksiyonunu yeniden üretmez |
| Önce sermaye | NotebookLM örneğinde %1 risk ve adet = risk / 2ATR; acil stop adı Ham'da (5.5) | Risk |
| Tek sinyale güvenme | "gözü kapalı ABCD'ye nasıl güveneceksin" (Ham, gorsel-paket-43) | Teyit şartı |
| Sınamadan inanma | "mutlaka backtest etmek lazım", negatif sonuçlarını da paylaşır | Kanıt |
| Basit ve sağlam | "Medyan temelli çalışın", "yüksek Sharpe ile uçan modellerin genellikle ilk sert virajda (drawdown) patladığını görürüz" (Ham, gorsel-paket-75) | Medyan, sağlamlık sınaması |

(İ: 10-001, 10-054, 17-056)

## 3. Kapsam (ilk sürüm)

**Var:**
- Günlük veri, BIST100 benzeri evren, yalnız alış yönü.
- Piyasa durumu etiketi (YORUM, bizim). Motoru ve girişi etkilemez; K1(b) örneklemesinde kullanılır, çıktıda görünmez.
  (vekil kararı 15.10, bilet 07e; İ: 11-078)
  Tansu'nun şokta yeni alımı durdurma fikri (Ham, tweet-volatilite-piyasa-soku-yeni-alim-freni:21) uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
  Tansu'nun yeni pozisyon için piyasa teyidi bekleme fikri (Ham, XU:35–47) uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- **2 aile** (`aile-kurallari.md` §3): çift rotasyonu ve EMA sıkışması.
- Tansu kaynaklarından esinlenen risk paketi (5.5), işlem motoru, portföy simülasyonu ve istatistik.
- Tek dosya HTML rapor, CSV kart ve işlem listeleri, `durum.txt`.

**Yok** (ilk aile kabul edilene kadar bekler, gereksiz katman):
- Streamlit ya da başka panel, Telegram, veritabanı.
- Süre çıkışı (Ç3). İz süren stop ve kısmi kâr (Ç2) yalnız EMA ailesinde, test varyantı olarak vardır
  (Levent 16.10; `aile-kurallari.md` §3). Çift ailesinde ve varsayılan kuralda yoktur.
- Dolar bazı karşılaştırma, Corwin–Schultz.
(Kesilecekler 1–6, C-1)

**İkinci dalga:**
- AB=CD. ISKPL Ham'ı C'den alımı anlatır. SMRTG sınama görseli fiyat ve işlem yönü yazmaz; üç işlemde
  pikselden okunan C ve D fiyatı tablodaki getiriyle aşağı yönde uyuşur (YORUM: bizim hesabımız). BIST'te bireysel
  açığa satış pratik değil. Alış yönlü hali Tansu'nun gösterdiği kural olmaz. (B-1)
- AEFES kanal, AKFIS kurulumu ve fiili dolaşım taraması.

**Kapsam dışı:**
- 4 saatlik ve gün içi veri, emir defteri, opsiyon.
- Harmonik, Elliott, değerleme, otomatik emir.
- Sembol değişikliği ve birleşme sürekliliği. Verisi biten sembol 5.2 kuralıyla işlenir; nedeni
  bilinmeyenler raporda listelenir. (İ: 02-022)

## 4. Modüller

Her modülün dışarıya küçük bir yüzü var. İçi değişse de dışı değişmez. Paket düzdür (`tansu/`). (C-3)

**Yeni modül varyantının gölge koşusu (#71):** Yeni modül varyantı siteye girmeden önce
Levent'in bilgisayarında mevcut koşularla paralel bir gölge koşuda sinyal üretir. Resmi değil, [§5.11'deki
geliştirme koşusu](#511-çoklu-deneme-düzeltmesi-ve-deneme-günlüğü) demektir; varyant sitede seçenek olarak sunulmaz.
Siteye giriş için varyantın [kural kaydına](#58-dönemler) bağlı tarihli sinyal listesi ve tamamlanan gölge koşunun
çıktısı gerekir. Levent bu çıktıları gördükten sonra varyantın siteye girişine karar verir.

| Modül | Girdi → çıktı | Not |
|---|---|---|
| `kaynak` | sembol, tarih aralığı → ham tablo | Ağa çıkan tek yer: İş Yatırım ve borsapy (yalnız faiz, sektör ve şirket listesi) (bilet 07e, 15.10). Ham alan adları (`HG_*`, `HGDG_*`) tek bir sözlükle proje adlarına çevrilir. İş Yatırım okuma zaman aşımı (5, 120) sn: ağır sorgular 40 ve 90 sn'de zaman aşımına uğradı; C-8'deki (5, 30) bu değerle değişti. (C-8, İ: 18-075, 01-057) |
| `veri` | indirme → anlık görüntü; olay tablosu; veri kapıları | Ayrıntı aşağıda. (B2, B-2, B-7) |
| `evren` | tarih → o gün yeni giriş için taranabilecek hisseler | 5.2. |
| `gostergeler` | fiyat → EMA, SMA, ATR, RSI, momentum squeeze, MACD, PSAR, stokastik, piyasa durumu | Vektörel; sınamada ve canlıda aynı kod. Kütüphane yok. Tanımlar `aile-kurallari.md` §3'tedir. |
| `katalog` | aile, varyant, katalog sürümü ve ayar isteği → tam çözülmüş strateji veya doğrulama hatası | E2 katalog sahibi; §5.15. Eski tanımların saklanması seçim izni vermez. |
| `aileler` | hisse fiyatı → sinyal günleri, kurulum bilgisi (kutu, hedef), arz ve talep bölgeleri | Tek hisse aileleri. EMA ailesinin varyantları ve bölgeler `aile-kurallari.md` §3'tedir. |
| `cift` | çift fiyatları → hangi hissede olunacağı | Kendi döngüsü. |
| `ciftbolme` | seçim, Z geçişleri, çift bölmesi simülasyonu, VAKBN–GARAN | `cift` ve `simulator`'a dayanır (bilet 11); 5.6. |
| `motor` | Adım: (pozisyon, bugünkü mum) → pozisyon; Motor: sinyaller → işlemler | Mum, ön hesaplı ATR ve SMA250 sütunları olan bir gün satırıdır. **Sınama ve canlı günlük aynı Adım'ı kullanır.** (A5, İ: 11-010) |
| `simulator` | işlemler + bölme kuralı → sermaye eğrisi | Boştaki nakit faiz kazanır. (A2, B4) |
| `istatistik` | fazla getiri → güven aralığı, p değeri, Holm | statsmodels yalnız `coint` ve Holm için. |
| `saglamlik` | ızgara hücreleri → pozitif hücre oranı | Önceden yazılmış ızgara (`aile-kurallari.md` §3); her hücre işlem başına ortalama fazla getiri (sepete göre, K1 tekrarı yok). 5.10. (bilet 13, İ: 09-064, bilet 03) |
| `kayit` | kural kaydı, deneme günlüğü, kart günlüğü, durum kayıtları | Yalnız ekleme. Getiri gösteren tek yol `kosu()`'dur: kural kaydı yoksa ya da hash uyuşmazsa tek Türkçe satırla durur. (C-6, İ: 15-074) |
| `rapor` | sonuçlar → HTML + CSV + `durum.txt` | Ayrıntı 6. bölümde. |
| `denetim` | sentetik boş ve etkili dünya → yanlış kabul, güç | Boru hattı denetimi (5.12). Hash dışı: kuralı değil sınamanın doğruluğunu ölçer; sonucu günlükte kod hash'iyle durur. (bilet 13) |
| `gunluk` | `gunluk(tarih)`: günlük indirme, kapılar, kartlar, `durum.txt` | Bilet 14; 6. bölüm. `rapor`'dan sonra, `__main__`'dan önce. |
| `sadakat` | ham seri → Tansu'nun gösterdiği rakamlar yeniden üretilir | `aile-kurallari.md` §4; getiriye bakılmaz; sonuç `docs/sadakat.md`. 7. bölüm adım 3. |
| `tansusinama` | anlık görüntü, sektör → hisse/çift başına ızgara, sağlam bölge, Tansu ölçüleri, ileri yürüme; JSON | Tansu'nun kendi sınama yöntemi; kabul kararına girmez. Hash dışı. 5.14. (Levent kararı 16.10) |
| `__main__` | `python -m tansu sadakat \| kayit \| sinama \| tansu-sinama \| denetim \| evren-indir \| sektor-indir \| gunluk` | Ayrıntı aşağıda. (İ: 16-001, 16-008, 14-084, 16-062) |

**`veri` ayrıntısı** (İ: 01-094, 02-026, 11-044, 13-006, 13-011, 13-015):
- Anlık görüntü tek klasördür. İçinde:
  - fiyat (ham ve düzeltilmiş, uzun biçim, bütün semboller),
  - olay tablosunun ham JSON'u,
  - borsapy tabloları (faiz, sektör),
  - `manifest.json` (her dosyanın sha256'sı).
- Veri sürümü, anlık görüntü kimliğidir.
- `veri.indir` isteğe bağlı `kapanan` tablosunu (`kod`, `ad`, `tarih`, `aciklama`) alır.
  Verilen tablo boş olsa da `kapanan.csv` başlıklarıyla yazılır; `None` dosya üretmez.
  `evren-indir` bu tabloyu yazıcıya verir. Yazıcı dosyayı geçici klasörde tamamlar, özetini manifeste katar ve sonra görüntüyü yayınlar.
  Kanıt yazımı başarısızsa görüntü yayınlanmaz; komut yayınlanan görüntüye ek dosya yazmaz.
- Okuyucu anlık görüntüyü açarken manifesti doğrular; listedeki eksik dosya veya uyuşmayan özet, kimlik ve dosya adıyla `VeriHatasi` verir.
  Eski görüntüler yalnız kendi manifestleriyle doğrulanır; geçmişte listelenmeyen kanıt sonradan eklenmez.
- Tarih sütunu saat dilimsiz saf tarihtir.
- Koşu, canlı borsapy'ye bağlı kalmaz.

**`__main__` ayrıntısı:**
- `gunluk` bayrak almaz. Bugünün tarihini parametre olarak alabilir (varsayılan bugün; test için).
- `sinama` geliştirmede 200 tekrar koşar; `sinama --son` 5.7'deki tam tekrar sayısını koşar.
- Yakalanmayan istisna günlüğe yazılır, çıkış kodu 1 olur.

**Bağımlılık yönü** tek yönlüdür, geri import yok (İ: 11-039):
`kaynak` → `veri` → `evren`, `gostergeler` → `katalog` → `aileler`, `cift` → `motor` → `simulator` → `ciftbolme` → `istatistik`
→ `saglamlik` → `rapor` → `kayit` → `tansusinama` → `gunluk`, `denetim` → `__main__`.
(`rapor` yalnız `simulator`'a dayanır; `kosu()` raporu aynı çağrıda yazar ve `rapor-<koşu>.html` adı koşu kimliğinden
gelir, bu yüzden `kayit` `rapor`'dan sonra gelir. Önceki sıra `kayit` → `rapor` koda uymuyordu.)

**Test yüzleri:** testler yalnız bu yüzlere yazılır: katalog (tam kayıt, eski uyarlayıcı, panel komutu ve komut satırında aynı doğrulama), Adım, Motor, Simülatör, İstatistik, Evren, veri kapıları, aileler (kurulum bilgisi ve bölgeler için
elle hesaplı mumlar), kayıt
(sonuc C-9), göstergeler (Wilder ATR ve EMA için elle hesaplı 5 satırlık örnek; İ: 12-018; RSI, momentum squeeze, ADX, MACD, PSAR ve stokastik için elle hesaplı kısa örnek) ve rapor (sahte sonuçtan rapor ve
CSV: sütun listesi, ilk satır cümlesi, sabit durum listesi, yasaklı kelime AL, SAT, ÖNERİ, "Tansu'nun sistemi"; İ: 17-093) ve
`tansusinama` (işlem getirisi, Tansu ölçüleri, sağlam bölge, ileri yürüme, işçi sayısı, 1 ve 2 işçide aynı sonuç). (bilet 03)

**Bağımlılık:** `tansusinama` makine ölçümü için `psutil` kullanır (boş bellek, CPU kullanımı); `requirements.lock.txt`'te
vardır, `pyproject.toml`'da `psutil==7.2.2` olarak sabitlenir.

Takvim, fiyat günlerinden çıkar (İş Yatırım XU100 günleri). Mevcut yollarda maliyet tek bir sabittir;
Tansu sınaması (5.14) kendi sabitini kullanır. Yeni maliyet politikası §5.15'tedir (Levent 18.10, "Komisyonunu alınsın.").

**Motor kendi Adım döngümüzdür; vectorbt kullanılmaz.** Dolum kuralları (5.3) AOF'a ve gün
yükseği/düşüğüne koşullu. Ölçütler kısa kendi kodumuzdur. (A3, M1, S2-41, C-2)

**Kaynaklar** (beyin notu knowledge/concepts/tansu-veri-kaynaklari.md, depo dışı; eski dosya git geçmişinde):
- **Fiyat:** İş Yatırım `HisseTekil`, anahtarsız.
  - Ham `HG_*` ve düzeltilmiş `HGDG_*` seriler.
  - Düzeltilmiş seri bedelsiz, bedelli ve brüt temettüyü kapsar.
  - Alanlar: kapanış, yüksek, düşük, AOF, hacim (TL), piyasa değeri, fiili dolaşım değeri, sermaye.
  - **Açılış yok.** 2000'den veri var.
- **Yahoo kullanılmaz.** (B-2)
- **Şirket olayları:** İş Yatırım `GetSermayeArttirimlari`, bütün kodlarıyla. Tarih hak kullanım günüdür.
- **Faiz:** borsapy TCMB politika faizi (TCMB "1 Hafta Repo" sayfası, TradingView değil); tek seri,
  2010'dan. Yalnız değişim günlerini içerir. (B-8)
- **XU100 kapanışı ve takvim:** İş Yatırım `HisseTekil`'in `END_DEGER` alanı (endeks kodu 01; XU100
  olduğu bilet 04'te doğrulandı). Yalnız kapanış.
- **Sektör:** borsapy, KAP şirket sayfasından, sembol başına bir istek (TradingView değil); yılda bir okunur.
  - **Toplu okuma** (`python -m tansu sektor-indir`, bilet 11; hedef evren üyeleridir, çift adayı yalnız onlardır).
    Bilet 07'de KAP ilk 100 sembolden sonra boş döndü; neden HTTP 429'dur (yaklaşık 100 sayfa isteği sonra).
    İstekler arası en az 1 sn, User-Agent `tansu-kisisel/0.1`; KAP şirket listesi bir kez, sembol
    başına bir şirket sayfası. Art arda 5 hata olursa durur; tamamlananlar `onbellek/` klasöründe kalır ve
    yeniden çalıştırınca tekrar istenmez. KAP listesinde olmayan (işlemi kapanmış) kod sektörsüz kalır.
  - **Anlık görüntü değişmez.** Eksik sektörler tamamlanınca yeni bir anlık görüntü yazılır: fiyat, olay ve
    faiz dosyaları aynen kopyalanır, `sektor.json` birleşir, manifest eski kimliği (`kaynak`) ve kapsamı
    (`sektor_kapsam`: hedef, var, listede olmayan, alınamayan) tutar. Koşu yeni kimlikle yapılır.
- **TradingView kaynaklı veri kullanılmaz.** Koşullar makineyle işlemeyi yasaklıyor.
- **Kullanım koşulları** (bilet 01, `docs/arastirma/kullanim-kosullari-fiyat-adimi.md`):
  - İş Yatırım'ın robots.txt dosyası `/_layouts/` yolunu yasaklıyor.
  - İş Yatırım Uyarı Notu (https://www.isyatirim.com.tr/tr-tr/urunler/Sayfalar/uyari-notu.aspx, 16.10 2026'da okundu) "açık iznimiz olmaksızın … çoğaltılamaz, dağıtılamaz" der ve şunu yazar: "BIST piyasalarında oluşan tüm verilere ait telif hakları tamamen BIST'e ait olup, bu veriler tekrar yayınlanamaz."
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
- **İndirme:** veri 2010'dan indirilir. ±%20 limit rejiminin başı 30.11.2015; sinyal günleri 01.12.2015'ten sayılır (5.6). (B-6; vekil kararı 14.10, bilet 03)
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
  - Sadakat kontrolü ham seriyle (YORUM, bizim). Kaynak genel fiyat düzeltme politikasını açıklamaz
    (araç, kaynak-vakbn-garan-rotasyon-2096358189696520213/g2).
  (B2, B-2, İ: 07-017, 08-010)
- **Eksik gün:** NaN kalır, ileri doldurulmaz. O gün sinyal ve giriş yok; açık pozisyon son bilinen
  kapanışla taşınır. (İ: 19-003)
- **Olay denetimi:**
  - Olay tablosu çarpanı (`SHHE_FIYAT_AYAR_OR`) ham seriye uygulanır ve `HGDG` ile karşılaştırılır.
    Fark %0,5'i aşan gün uyarıdır; `HGDG` geçerli kalır.
  - Olay denetimi istatistiğinde eşleştirme tablo tarihinin ±1 işlem günü penceresinde yapılır (karantina eşleştirmesi daha dardır, bkz. Karantina).
  - Sınama vakaları (veri birim testi): çarpan > 1 (sentetik), aynı güne iki kayıt (çarpanlar çarpılır), ±1 gün (denetim istatistiği)
    kayması (HEKTS 26.11.2015). CCOLA temettü formülü alınmadı.
  (B1, B-2, İ: 02-024, 02-093)
- **Fiyat limiti:**
  - Limit hesabının baz fiyatı önceki gün ham kapanışıdır; tavan ve taban baz fiyatın ±L'sidir.
  - Bozuk satır (satır ihlali, 5.13) baz fiyat olmaz; baz, önceki tutarlı işlem gününün ham kapanışıdır. (vekil kararı 15.10, bilet 07e)
  - Olay çarpanını alan günde (adım günü, aşağıdaki karantina maddesi) baz fiyat = önceki ham kapanış × olay çarpanı. Kilit ve karantina bu baz fiyattan çıkan limitlerle
    yargılanır. Bilinmeyen olay kodu ya da çarpanı 1 olan kayıt istisna sayılmaz.
  - L = %20 (30.11.2015 – 12.03.2020), %10 (13.03.2020 sonrası). Baz fiyatın önceki ham kapanış olduğu ±%10 döneminde
    veriyle doğrulandı.
  (İ: 01-024, 02-033, 07-060; "baz fiyat" adı: bilet 03, sözlük denetimi)
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
  | ≥ 2.500 | 0,10 | 2,50 (veride doğrulanmadı; resmi tablo: §5.15 [W5], 18.10.2026) |

  Sınama vakası: KONTR 08.07.2026. (İ: 01-023, 02-056, 05-043)
- **Karantina:**
  - Kapanıştan kapanışa o günkü limiti (+%0,5) aşan ve şirket olayıyla açıklanmayan her gün karantinaya
    girer. "Olayla açıklanan" eşleştirmesi gün başınadır ve yalnız o güne kadarki veriye dayanır (önek değişmezliği 5.12,
    kesim günü dahil): t günündeki adım, tablo tarihi t−1 ya da t olan bir olayla açıklanır; başka güne bakılmaz, aday
    seçimi yoktur. Aynı olay hem t−1 hem t günündeki adımı açıklayabilir; t+1 tarihli olay açıklamaz. Adım: o günün ham
    kapanışının önceki tutarlı kapanışa oranı (bozuk satırlar limit bazındaki gibi atlanır, 5.13; bilet 07e, 15.10), olay çarpanına 1'den daha yakınsa (logaritmik) gün adımdır; adım olmayan gün
    olay çarpanı almaz. Olay denetimi istatistiği ±1 işlem günü penceresinde kalır. (HEKTS 26.11.2015)
    (vekil kararı 15.10, bilet 07e) (İ: 02-024)
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
  - Aynı şirketin birden çok kodu varsa yalnız 60 günlük medyan TL hacmi en yüksek kod alınır; bilinen çoklu kodlar elle
    listelenir. Böylece aynı şirket K2 sepetinde iki kez ağırlıklanmaz. (İ: 03-004)
  - Evren yalnız yeni girişi sınırlar. Evrenden çıkan hissenin açık pozisyonu kendi kuralıyla
    kapanır. (B-9)
- **İşlemi kapanan hisseler:** İş Yatırım bunları da veriyor, ama liste eksik.
  - Kapanan hissede açık pozisyon −%100 sayılır (yarı satılmış pozisyonda kalan yarı; 5.5); nedeni bilinirse son fiyat.
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
Bu bölümün eski işlem kuralları `legacy_portfoy_v1` içindir. Yeni bağımsız işlemde
nominal temel başına %2 bütçe kullanılır; ortak nakit, portföy tavanı ve açık işlem sınırı yoktur.
Yeni risk ve gerçekleşen maliyet hesabının sahibi §5.15 "S08 risk ve maliyet hesabı"dır.
- **Sinyal ve giriş:**
  - Sinyal günün kapanışındadır.
  - İşlem fiyatı ertesi günün **ağırlıklı ortalama fiyatıdır (AOF)**. VAKBN–GARAN paneli T+1 açılış
    gösterir (araç, kaynak-vakbn-garan-rotasyon-2096358189696520213/g2, işlem paneli); uygulanamaz: mevcut veri kaynağında açılış yok.
    AOF, kaynak dolumunun yaklaşık modelidir.
  - Sinyal günü kapanış SMA250 altındaysa ya da SMA250 hesaplanamıyorsa giriş yok (YORUM, bizim).
    Kaynak kesin giriş karşılaştırmasını açıklamaz (Ham, G115:20; NotebookLM, g1).
  (S2-7, B-12, İ: 07-065)
- **Stop:** giriş fiyatından ve sinyal günü ATR'sinden hesaplanır. EMA ailesinin kutu stopu varyantında stop kutu
  altından gelir (`aile-kurallari.md` §3). (M2, C10)
- **Giriş günü:** yalnız stop kontrol edilir.
- **Stop dolumu:** gün düşüğü ≤ stop ise dolum **min(stop, AOF)**. (B-4)
- **Hedef ve yarı satış dolumu** (EMA ailesi varyantları; tetikler `aile-kurallari.md` §3):
  - Hedef: gün yüksek ≥ hedef ise tam çıkış olur ve dolum hedef fiyatıdır. Gün düşüğü hedefin üstündeyse dolum AOF'tur.
  - Gün içinde tetiklenen yarı satış (`atr3`): gün yüksek ≥ seviye ise pozisyonun yarısı satılır. Dolum seviyedir.
    Gün düşüğü seviyenin üstündeyse dolum AOF'tur.
  - Kapanışta tetiklenen yarı satış ve tam çıkış (`dip`, `rsi70`, `rsi50`) ertesi günün AOF'unda dolar.
  - Kilitli taban gününde AOF dolumları ertesi güne kayar; hedef ya da `atr3` o gün tetiklenirse de dolum ertesi kilitsiz günün AOF'undadır (hedefte neden `hedef` kalır, yarı satış tek seferdir).
- **Kilitli gün:**
  - Kapanışı tavan fiyatında olan gün (bir fiyat adımı toleransla) giriş yok.
  - Kapanışı taban fiyatında olan gün çıkış ertesi güne kayar.
  - Duyarlılık sürümü: yalnız düşük = yüksek, hacim > 0 ve limit fiyatında olan gün.
  (M4, B-5, İ: 01-026, karar.md)
- **Düşen sinyal:** giriş günü yoksa, kilitli tavansa ya da karantinadaysa sinyal düşer, sonraki güne kaymaz (vekil kararı 15.10, bilet 07e). Stop kutu altından geliyorsa ve giriş günü AOF'u ≤ kutu stopu ise de sinyal düşer (`aile-kurallari.md` §3, kutu stopu). Sayısı
  raporda "iptal" olarak yazılır. Kayma yalnız çıkış dolumunda olur (kilitli taban, eksik gün; 5.13); giriş
  dolumu kaymaz. (İ: 05-044, 19-055)
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
  - R = giriş − ilk stop (hisse başına planlanan risk; stop sonra yükselse de R ve planlanan risk ilk stoptan yazılır). Planlanan risk = adet × R. Gerçekleşen kayıp = adet × max(0, giriş − çıkış).
  - Karantina çıkışı: fiyat son temiz AOF, tarih karantina günüdür. Çıkış gününde (AOF'ta) çıkılmış pozisyon
    o günün kapanış sinyalini engellemez. Isınma: hissenin n. işlem günü dolduğunda (n = 500) sinyal serbesttir.
  - (Bilet 08: belge bu noktalarda sessizdi; kod bu okumayı uygular.)
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
Bu bölüm `legacy_portfoy_v1` maliyet ve kapasite politikasını korur. Yeni komisyon §5.15 S08'dedir.
- **Masraf:** sabit, her yönde %0,3 (komisyon, BSMV, kayma birlikte).
  - Sonuçlar %0,1 / %0,3 / %0,5 ile gösterilir.
  - Kabul için %0,5'te de geçmesi gerekir. (M3)
- **Likidite** (YORUM, bizim): pozisyon, 10 günün medyan TL işlem tutarının %2'sini geçemez.
  - Sektör taraması ile genel medyan önerisi tek zorunlu ölçü vermiyor; genel evrene aktarım ve işlem
    kapasitesi ölçüsü açık değil (Ham, tweet-sektor-rotasyonu-hacim-tuzagi-sabit-tl-esigi:32–49;
    tweet-medyan-temelli-finansal-indikatorler:23).
  - Pencere sinyal gününü kapsar, giriş gününü kapsamaz.
  - Kalan miktar ertesi gün alınmaz.
  - Rapor likidite tavanının bağladığı işlem oranını yazar.
  (M11, İ: 08-019, 08-021)
- **Valör modellenmez:** satış nakdi aynı gün kullanılır. (İ: 08-014)
- **Vergi:** sınamaya girmez; raporda not edilir.

### 5.5 Çıkış
Risk paketi (`kurallar/E` K1–K3): acil stop ve gün sonu stopu adları Ham metindedir
(Ham, tweet-atr-risk-butcesi-position-sizing-stop-loss:22; Ham'da yazar yok). %1 risk ve SMA250 çıkışı NotebookLM
örneğindedir (G115/g1). Ortalama seçimi okura bırakılmıştır (Ham, G115:20); SMA250 bizim seçimimizdir (YORUM).
- **Acil stop:** giriş − 2 ATR; gün içinde dokunulursa çıkılır.
- **Gün sonu stopu:** kapanış SMA250 altına inerse ertesi günün AOF'unda (YORUM: dolum).
  Kaynak gerçekleşme fiyatını ve seansını açıklamaz.
- **ATR:** uzunluk 14, Wilder ortalaması; ilk değer ilk 14 gerçek aralığın ortalaması; kendi kodumuz
  (YORUM). Gerçek aralık = max(yüksek − düşük, |yüksek − önceki kapanış|, |düşük − önceki kapanış|); düzeltilmiş
  seriden. (İ: 19-025, sözlük denetimi 3. tur)
- **Hedef:** EMA ailesinin varyantları hedefi dener (Levent 16.10; hedef kuralları `aile-kurallari.md` §3). Varsayılan kuralda
  hedef yoktur (YORUM: bizim seçim). Tansu bazı kurallarda hedef verir: gorsel-paket-106 Ham (EMA sıkışması + talep
  bölgesi: supply/arz bölgesi), gorsel-paket-107 Ham (1.618 dalga uzantısı), gorsel-paket-58 Ham (389.30). KRDMD örneğinde
  hedef yoktur. Çift rotasyonunda kâr hedefi yoktur; geçiş kuralı §5.6'dadır. Standart long/short sürümü ayrıdır (Ham, `beyin/kisisel/300-Projects/Tansu X Veri Havuzu/tweet-istatistiksel-arbitraj-z-skor-pairs-2049196300856414620.md:56–59`, 28.04.2026): "Z-Skoru normale (0.5 seviyelerine) döndüğünde, pozisyonları kapatır" (`docs/kurallar/D-cift-portfoy-nabiz.md:23`, `:32`, `:88`, `:108`; okuma 18.10.2026).
- **Çift rotasyonu:** ayrı stop yok (YORUM, bizim); karşı uçta diğer hisseye geçilir. Risk paketi bu bölmeye uygulanmaz.
  Grafikte stop görünmemesi, stop bulunmadığını kanıtlamaz (Ham, G125:20; araç, kaynak-vakbn-garan-rotasyon-2096358189696520213/g2; eğitim, G118/g1).
  (Sorgu S3)
- **Aile kuralları:** giriş kuralları ve YORUM'lar `aile-kurallari.md` §3'tedir.
- **İz süren stop ve kısmi kâr:** kaynak Ham'dadır (tweet-statik-dinamik-iz-suren-stop-atr:20; G125:20). EMA ailesinin
  varyantları ATR merdivenini, başabaş çıkışını ve dört yarı satış kuralını dener (Levent 16.10; çıkış paketi
  `aile-kurallari.md` §3). Varsayılan kuralda bu paket yoktur; öbür aileler bu paketle kabul edildikten sonra denenir.
- **Yarı satışlı işlem:** işlem tablosunda tek satırdır. Çıkış fiyatı (yarı satış fiyatı + son çıkış fiyatı) / 2'dir; yarılar
  eşit adettir. Getiri ve gerçekleşen kayıp (5.3) bu ortalama fiyattan hesaplanır; masraf oranı sabit olduğu için getiri
  kesindir. İşlem tablosunda ayrıca `yari_tarih` ve `yari_fiyat` vardır (yarı satış yoksa boş). Hisse kapanırsa (5.2) ve
  yarı satış hissenin son işlem gününde ya da önce yapılmışsa (`yari_tarih` ≤ son işlem günü), çıkış fiyatı (`yari_fiyat` + 0) / 2
  olur; yarı satış yoksa 0 olur. Sınır: simülatör yarı satışın nakdini son çıkış gününde görür. Yarı satış ile son çıkış
  arasında nakdin faizi ve yeniden kullanımı eksik kalır.

### 5.6 Portföy ve bölmeler
`legacy_portfoy_v1` sürümünde her aile **kendi sermayesiyle ayrı** ölçülür. Sınama tek sürekli koşudur; sermaye yıldan
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
- Çift payları yıl başında eşittir; yıl içinde dengeleme yok (YORUM, bizim; Tansu'nun örnek çiftleri VAKBN–GARAN,
  CIMSA–OYAKC (gorsel-paket-51), AGROT–GARAN (gorsel-paket-52) ayrı örneklerdir, çiftler arası pay kuralı görülmedi).
  (İ: 08-056)
- Her çift payı, ilk girişe (nakitten ilk alım) kadar nakittedir; sonra hep çiftin bir hissesindedir. Boş pay nakitte kalır
  (YORUM, bizim; araç, kaynak-vakbn-garan-rotasyon-2096358189696520213/g2, genel nakit politikasını açıklamaz).
- Bacaklardan biri kilitliyse geçiş yapılmaz. Sinyal ertesi gün yeniden değerlendirilir; eski sinyal
  taşınmaz. (İ: 04-068)
- Bacaklardan biri karantinadaysa çift o pencerede girişsiz kalır; tutulan bacak karantinadaysa açık pozisyon son temiz AOF'ta kapanır, öbür bacaktaki karantina pozisyonu kapatmaz. (İ: 02-082; vekil kararı 14.10, bilet 03)
  (İ: 02-082)
- Çiftin hissesi kapanırsa pay 5.2 kuralıyla kapanır ve yıl sonuna kadar nakitte faiz kazanır.
  (İ: 03-060)
- Bu bölmede "işlem", geçişten geçişe tutuş dönemidir. (İ: 08-058)

**Çift seçimi** önceden yazılır (Sorgu S4, B-10):
- **Ne zaman:** her yıl, yılın ilk işlem günü kapanışında, o günkü evrenle. Çıkışlar ve girişler ertesi
  günün AOF'unda (YORUM, bizim). (İ: 03-051, 08-054)
  Tansu'nun kayan eşbütünleşmeyle ilişki sağlığını izleme fikri (Ham, tweet-rolling-cointegration-iliski-bozulma-kapisi:21) uygulanamaz: kaynak hesaplanabilir tanım vermiyor.
- **Neyden:** aynı sektördeki hisseler (YORUM, bizim; Ham, G54:21, long/short bağlamındadır ve
  rotasyonun sektör filtresini açıklamaz). 252 işlem günü verisi olmayan hisse aday olmaz. (İ: 04-094)
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

**Çift bölmesi kuralları** (bilet 11; belge bu noktalarda sessizdi, kod bu okumayı uygular):
- **Seçim ayrıntısı:** seçim günü `s` = yılın ilk işlem günü; evren o günün ayının evrenidir (5.2).
  - Aday hisse: evren üyesi, sektörü bilinen ve son 252 işlem gününün (`s` dahil) hepsinde düzeltilmiş
    kapanışı olan. Aday çift: aynı sektörden iki aday (YORUM, bizim).
  - Roller: Y = sembol sırasına göre ilk, X = ikinci (alfabetik).
  - Eşbütünleşme: statsmodels `coint(log Y, log X)` (Engle–Granger, sabit terimli, gecikme AIC), son 252 gün,
    düzeltilmiş kapanış. p < 0,05 olan çift kalır.
  - β = aynı penceredeki log Y'nin log X'e OLS eğimi; β ≤ 0 elenir.
  - Sıralama: p artan, eşitlikte (Y, X) sembol sırası. Açgözlü seçim: bir hisse en fazla bir çiftte, sektör
    başına en fazla 2 çift, toplam en fazla 5.
- **Sinyal:** her gün kapanışta seçilmiş çiftlerde `aile-kurallari.md` §3 "Çift rotasyonu" sinyal kuralı uygulanır (`cift.z_skor`).
  Hesap tanımı, pencere ve eşikler o bölümde yönetilir. Hedef geçilecek bacaktır; kâr hedefi değildir (5.5).
  Seçim günü kapanışındaki sinyal ertesi gün işlenir.
- **Geçiş:** hedef, tutulandan farklıysa ertesi günün AOF'unda (5.3'teki yaklaşık dolum modeli) eski bacak satılır, yeni bacak alınır; her
  bacakta %0,3 masraf. Adet = tam lot, aşağı yuvarlanır; alış, sinyal gününü kapsayan 10 günlük medyan TL
  hacmin %2'siyle sınırlanır (5.4); artan nakit çiftin payında kalır.
- **Engeller** (geçiş yapılmaz, sinyal taşınmaz): iki bacaktan birinde o gün işlem yok (`islem` yanlış), tavan ya da
  taban kilidi var. Karantina: bacaklardan birinde son 250 satırda karantina günü varsa çift girişsizdir (motor
  kuralıyla aynı pencere); tutulan bacakta karantina günü olursa pozisyon son temiz AOF'ta karantina gününde
  kapanır, pay nakde geçer, pencere dolana dek yeniden giriş olmaz.
- **Kapanma:** bacak 5.2 kuralıyla kapanırsa (`evren.kapananlar`) tutulan bacak o gün 0 fiyatla kapanır; çift
  yıl sonuna dek işlemsizdir (pay nakitte faiz kazanır).
- **Paylar:** sermaye 5 eşit paya bölünür. İlk girişten (nakitten ilk alım) önceki pay nakittedir. Seçimden sonraki ilk işlem günü
  (`s`'nin ertesi) AOF'unda düşen çiftlerin bacağı satılır; yeni çiftler ve boş paylar, o ana dek biriken serbest
  nakdi eşit paylaşır. Yine seçilen çift işlemsiz sürer ve payı eşitlenmez (YORUM: belge iki cümlesini
  birleştirir; eşitleme işlem ve masraf gerektirirdi). Yıl içinde dengeleme yok. Hiç çift seçilmeyen yıl
  nakitte kalır ve "işlem yok" diye işaretlenir.
- **Tutuş dönemi** (işlem): bir bacağın alımından satımına (geçiş, karantina, kapanma, yıl geçişi, veri sonu)
  tutuş. Getiri masraflı, 5.6 simülatör formülüyle.
- **K2:** aynı simülatör K2'si; maruziyet = çift bölmesinin hisse payı (kapanış değeri / özkaynak).
- **Tanısal 50/50:** her yılın seçimden sonraki ilk işlem günü AOF'unda her payın yarısı Y'ye, yarısı X'e
  alınır (tam lot, masraflı); yıl sonuna dek tutulur; ertesi yıl başında hepsi satılıp yeni çiftler alınır.
  Seçilen çift yoksa nakittedir. "Yılın ilk işlem gününde al" kararı (İ: 04-057) seçim gününü anlatır; seçim o günün
  kapanışında yapıldığı için alım ertesi günün AOF'undadır; aynı günün AOF'unda alım geleceği görmek olurdu
  (çift seçiminde de giriş ertesi günün AOF'undadır; İ: 03-051, 08-054). 5.7 K2'deki 50/50 anlatımı aynı tarihi
  kullanır. (İ: 04-057, bilet 03)
- **VAKBN–GARAN:** Y = VAKBN, X = GARAN, tek pay, 1.000.000 TL, simülatör başlangıcından itibaren; aynı Z, geçiş,
  engel ve masraf kuralı. Karşılaştırma: aynı çiftin 50/50 tutulması, başlangıçta bir kez.

**Faiz:** boştaki nakit, bir gün gecikmeli politika faizini kazanır (takvim günü, /365). Rapor faiz
serisinin kaynağını ve son değişim tarihini yazar; seri boşsa koşu SORUNLU olur. (B4, B-8, İ: 08-071)

**Simülatör kuralları** (bilet 10; belge bu noktalarda sessizdi, kod bu okumayı uygular):
- **Başlangıç:** ilk gün = 2015-12-01 ya da sonraki ilk işlem günü (ya da veri daha geç başlıyorsa veri günü).
  Sinyal günü bu günden önce olan sinyaller sayılmaz (30.11.2015 sinyali dahil; vekil kararı 14.10, bilet 03). Her işlem günü: önce faiz, sonra çıkışlar, sonra girişler, sonra
  kapanış değerlemesi.
- **Evren süzgeci** (bilet 11 düzeltmesi): motor yalnız simülatörün alabileceği sinyalleri görür: sinyal günü
  simülatör başlangıcından sonra ve sinyal gününün ayının evreninde (5.2) olan sinyaller. Evren dışı sinyal
  motorda pozisyon açmaz; böylece motor ve simülatör pozisyonları bire bir kalır ve aynı hissede sonraki
  geçerli sinyal gecikmez. Simülatör aynı süzgeci yine uygular (güvence). Kalan yaklaşıklık: yer ya da
  nakit yüzünden reddedilen sinyal motorda pozisyon gibi sayılır, aynı hissede sonraki sinyali geciktirebilir.
- **Boyutlandırma özkaynağı:** sinyal günü kapanış özkaynağı (önceki işlem günü kapanışı). İlk gün için
  1.000.000 TL. Nakit sınırı giriş günündeki güncel nakittir (aynı gün çıkış nakdi dahil).
- **Likidite:** sinyal gününü kapsayan son 10 işlem gününün (hacmi olmayan gün 0) medyan TL hacmi.
- **Bağlayıcı sınır:** dört sınırdan en küçüğü; eşitlikte sıra: risk, tavan, likidite, nakit.
  Rapor, alınan işlemler içinde her sınırın bağlama oranını yazar.
- **Reddedilen:** 10 pozisyon dolu olduğu için ya da adedi 0'a yuvarlandığı için girilemeyen sinyal.
- **Masraf:** girişte tutar × (1 + m), çıkışta tutar × (1 − m). İşlem getirisi = çıkış (1 − m) / giriş (1 + m) − 1.
- **Faiz:** her takvim gecesi, nakdin üzerine o gecenin (bir gün gecikmeli, 5.6) yıllık oranının /365'i basit
  eklenir; hafta sonu üç gece sayılır. Gece, işlem gününün kapanışından sonraki ilk geceden başlar.
- **Özkaynak:** nakit + açık pozisyonların düzeltilmiş kapanışla değeri (kapanışı olmayan gün son kapanış).
- **Kapanan hisse (5.2):** kapanma günü (`evren.kapananlar`) açık olan pozisyon o gün 0 fiyatla
  kapanır (−%100, neden `kapanma`). Kapanma nedeni listesi henüz bağlı değildir (bilet 07); her kapanma
  −%100 sayılır. Yarı satılmış pozisyon yalnız kalan yarıyı kaybeder (5.5 "Yarı satışlı işlem"). Rapor bu işlemlerin
  sayısını yazar.

### 5.7 Karşılaştırma (asıl soru)

**Fazla getiri tanımı** (B4):
- **İşlem seviyesi:** işlemin getirisi − aynı tutma süresinde aynı evrenin eşit ağırlıklı sepetinin
  getirisi. Sepet getirisi işlemin giriş ve çıkış AOF günlerinden hesaplanır. (İ: 02-083)
- **Portföy seviyesi:** günlük portföy getirisi − günlük karşılaştırma getirisi.

**K1. Eşleştirilmiş rastgele kural** (B5):
- **Seçim:**
  - Rastgele sinyaller, kuralın kendi ön şartlarını sağlayan günlerden seçilir.
  - Ön şart her aile için `aile-kurallari.md` §3'te yazılıdır.
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
  - B ≥ max(1.000, 200·m); m = deneme sayısı (5.11'de tek tanım). 200·m bir duyarlılık payıdır, matematiksel zorunluluk
    değildir: p tabanı 1/(B+1) olduğundan B = 1.000 ile m ≤ 50 için kabul hâlâ mümkündür (m = 50'de en küçük düzeltilmiş
    p 50/1.001 ≈ 0,04995 < 0,05; m > 50'de imkânsız; cevaplar-15'teki "m ≥ 50 imkânsız" yanlıştır, sonuc O14 doğrudur).
    B ≥ 200·m ile p tabanı Holm eşiğinin (α/(m−k+1)) çok altında kalır; kabul kararını p tabanı değil gerçek p değeri belirler.
  - Geliştirmede 200 tekrar; bu p'ler günlükteki Holm listesine girmez, m'yi artırmaz; rapor yalnız varsayımsal bir
    Holm p'si gösterir (5.11).
  (B-14, İ: 15-078, 19-068, 09-009; bilet 03)
- **p değeri:**
  - p = (1 + k) / (1 + B); k = gerçek kuraldan iyi ya da eşit rastgele tekrar sayısı.
  - Tek yönlü; istatistik işlem başına ortalama fazla getiridir.
  - Aile p'si iki türün büyüğüdür.
  - Gerçek istatistik hesaplanamazsa (NaN, örneğin işlem yok) p = 1 olur; deneme günlüğü satırına `uyari: "istatistik NaN"` yazılır ve rapor bunu gösterir; koşu durmaz, çünkü p = 1 kabule yardım edemez. (vekil kararı 15.10, bilet 07d)
  - Rastgele tekrarda istatistik hesaplanamazsa (NaN) o tekrar gerçeğe eşit ya da daha iyi sayılır (p'yi düşürmez). (vekil kararı 15.10, bilet 07d)
  (B-15, İ: 19-069)

**K1 uygulama kuralları** (bilet 12; belge bu noktalarda sessizdi, kod bu okumayı uygular):
- **Fazla getiri (işlem):** işlem getirisi (masraflı) − sepet getirisi. Sepet getirisi K2 sepet endeksinin
  önceki-kapanış değerlerinin oranıdır: `S[çıkış−1] / S[giriş−1] − 1` (kapanıştan kapanışa bir gün gecikmeli;
  AOF'tan AOF'a yaklaşıklığı. Gerçek ve rastgele işlemde aynı tanım, bu yüzden karşılaştırma tutarlı).
  İstatistik bu farkın işlem başına ortalamasıdır.
- **Ön şartlı gün (EMA):** o hissede sıkışma dönemi bitmiş, giriş penceresi (10 gün) açık, kapanış ≥ SMA250,
  ısınma tamam, hisse o ayın evreninde, karantina penceresinde değil. Gerçek sinyal günleri bu kümenin parçasıdır.
- **Tür (a):** her sinyal gününde gerçek sinyal sayısı kadar hisse, o günün ön şartlı havuzundan yerine koymadan
  çekilir. **Tür (b):** her gerçek sinyal için aynı hissenin ±20 satırı içinde, o günle aynı piyasa durumunda
  (XU100 > SMA50), kendisi dışında bir hisse düzeyi uygun gün çekilir: kapanış ≥ SMA250, ısınma tamam, evren
  üyesi, karantina penceresi dışı (sıkışma penceresi şartı aranmaz). Gerekçe: sıkışma penceresi şartıyla gerçek
  veride (TCELL 29.08.2019) komşu gün bulunmadı ve koşu durdu; (b) zamanlamayı aynı hissenin yakın günleriyle
  ölçer, pencere şartı (a) ve ek kolda zaten aranır. Havuz yetmezse (a için) `K1Hatasi`; ek kolda (yalnız rapor,
  aile p'sine girmez) havuzu sinyal sayısından küçük gün havuz kadar çeker ve eksik sinyal sayısı `ek_eksik`
  olarak günlüğe yazılır (bilet 13, gerçek veri: 21.09.2026'da 100 üyeden hiçbiri önceki 20 günün yükseğinin
  üstünde kapatmadı, koşu `K1Hatasi` ile duruyordu; rapor kolu kabul kararını durdurmasın, ama sessizce de
  kırpılmasın). (b)'de komşusu
  olmayan tek tek sinyaller (ULKER 19.03.2021 gerçek veride bu durumdaydı) o türün çekiminden düşer; sayısı
  `komsusuz` olarak günlüğe yazılır, hiçbir sinyalin komşusu yoksa `K1Hatasi`. Gerekçe: tek sinyalin eksikliği
  tüm koşuyu durdurmasın, ama sessizce de kırpılmasın.
- **Ek kol (sıkışmasız kırılım):** gün başına gerçek sinyal sayısı kadar hisse, o günün şu havuzundan çekilir:
  kapanış önceki 20 günün en yüksek yükseğinin üstünde (20: YORUM; KRDMD örnek sıkışması 20 gündü), sıkışma
  penceresinde değil, SMA250, ısınma, evren ve karantina şartları aynı. Yalnız rapor; aile p'sine girmez.
- **Rastgele işlem:** aynı Adım ve aynı simülatörden geçer: hisse başına sinyaller sırayla işlenir, açık ya da
  bekleyen pozisyonun varken gelen sinyal yeni işlem açmaz ve sayıma girmez (5.3; İ: 07-079). K1 bu zinciri tek işlem sonuçlarını önbelleğe alarak
  kurar; gerçek sinyallerle `motor.islemler` ile aynı tabloyu verir (test).
- **Çift:** her seçilmiş çift için gerçek tutuş sayısı kadar sinyal günü, çiftin etkin olduğu günlerden |Z| ≥ eşik
  olanlardan çekilir; ilk sinyal günü ve yönü gerçeğe eşit, sonrakiler sırayla öteki bacağı hedefler.
  Aynı kilit, karantina ve masraf kuralları işler; engellenen sinyal sayıyı azaltabilir.
- **Tekrar sayısı m'si:** B = max(1.000, 200·m); m, 5.11'deki deneme sayısıdır. `--son` bu B'yi koşar; `--son`
  olmadan 200. Resmi koşu B'si bu değerin altındaysa durur.
- **Süre** (bilet 13, `python -m tansu sinama`, gerçek veri 20261005-1949, 32 çekirdekli geliştirme makinesi; bütçe
  200 tekrar için ≤ 5 dk): hızlandırmadan önce B = 200 7 dk 0 sn (ızgarasız). Sonra, ızgaralar dahil: B = 200 **2 dk 52 sn
  ve 3 dk 03 sn**; B = 1.000 (m = 2, resmi büyüklükte, `resmi:false`) **6 dk 48 sn ve 6 dk 50 sn** (iki ölçüm). Neden hızlandı:
  `motor.sinama` tek işlem önbellekli `Zincir` ile (78 → 16 sn), mum tablosu anlık görüntü başına bir kez, K1 simülatörü pandas
  skaler erişimi yerine sözlükle, K1 işlem tablosu hisse başına değil tek parça, eşbütünleşme yıllara paralel (süreç havuzu) ve
  ızgara için bir kez hesaplanır. İstatistik ve B değişmedi; aynı tohumda aynı p ve aynı özet (üç koşu).

**K2. Aynı evrenin eşit ağırlıklı sepeti, maruziyet eşleşmeli** (B3b, B-13):
- **Kuruluş:** sepet ay başında evrenle eşit ağırlıklı kurulur, AOF'tan AOF'a. Ay başı evren değişimi ve
  dengeleme %0,3 masraf öder. Sepette kapanan hisse 5.2 kuralıyla işlenir. (İ: 03-065, 03-066, 08-048,
  09-019, 09-020)
- **Maruziyet:** sepetin yatırımdaki payı her gün kuralın o günkü yatırımdaki payına eşitlenir; kalanı
  aynı faizi kazanır. Bu eşitleme masrafsızdır (YORUM).
  - Kuralın "o günkü payı" = o günün kapanışındaki pozisyon değeri / özkaynak.
  - Sepet getirisi içinde: ay başı ilk işlem günü eski sepet AOF'a taşınır, AOF'ta eşit ağırlıklı yeni
    sepete dengelenir (masraf = %0,3 × Σ|yeni ağırlık − eski ağırlık|), sonra kapanışa taşınır. Ayın
    öteki günleri kapanıştan kapanışa, dengelemesiz. İlk kuruluş da masraf öder.
  - Sepette kapanma günü olan hisse o gün 0 olur (−%100); ağırlığı sonraki ay başına kadar nakde dönmez.
  - K2 her masraf düzeyinde sepet masrafı %0,3 kalır; maruziyet o düzeydeki kuraldan gelir.
  - Fazla getiri (rapor): yıllık fazla getiri, o yıldaki günlük portföy fazla getirisinin (kural − K2) toplamıdır;
    5.8 ile aynı tek tanım. Yıllık kural getirisi ve yıllık K2 getirisi ayrı sütunlarda bilgi olarak durur. (İ: 08-083;
    bilet 03)
- **Çift bölmesi:**
  - Kabul, evren sepetiyle (K2) verilir.
  - Aynı çiftlerin 50/50 tutulması yalnız tanısaldır: yılın ilk işlem günü seçilir, alım seçimden sonraki ilk
    işlem günü AOF'undadır (5.6); yıl sonuna kadar tutulur, dengeleme yok.
  (İ: 04-051, 04-057)

**K3. Faiz:** simülatörde boştaki nakit faiz kazandığı için portföy sonucu zaten faize karşı okunur.

Dolar bazı ilk sürümde yok.

### 5.8 Dönemler
- **2023 sonrası ayrılmış dönem yandı.** 2015–2026 bütünüyle geliştirme/doğrulama verisidir. (M8)
- **Yıllık bölme:**
  - Parametreler sabittir; yıllık bölme yalnız çift seçimini yeniler. Kâğıt üstü dönemin yerine
    geçmez.
  - Bu bölme, parametreleri her yıl yeniden optimize eden ileri yürüme (walk-forward) değildir: yıllar yalnız tek
    sürekli koşunun sonuç dilimleridir (5.12'de "yıllık sonuç dilimleri"). (bilet 03, sözlük denetimi)
  - Tek sürekli koşunun eğrisi yıllara kesilir. Yıllık fazla getiri, o yıldaki günlük portföy fazla
    getirisinin toplamıdır.
  - Tamamlanmamış yıl (2026) 5.12.4'ün paydasından çıkar ve ayrıca gösterilir.
  (M7, İ: 09-025, 08-083, 09-027)
- **Kural kaydı** (M8, Sorgu S13, C-6, İ: 15-006, 15-016, 09-061):
  - **Ne zaman:** sadakat kontrolü bitince, ilk getiri koşusundan önce kayda geçer. Bundan sonrası
    yeni ayrılmış dönemdir. Sonraki her değişiklik yeni denemedir.
  - **Hash kapsamı:** elle yazılmış kod dosyaları listesi (`KOD_DOSYALARI`), kural parametreleri ve ızgara
    tanımı (iki ailenin ızgarası, `saglamlik.IZGARA`).
    - **Kural:** değişmesi işlemleri, dolumları, limit/kilit/karantinayı, evreni, p değerlerini ya da kabul kararını
      değiştirebilecek her modül listededir. İndirme, rapor, günlük koşu, CLI, sadakat ve denetim kodu listede yoktur.
    - **Liste:** aileler, cift, ciftbolme, evren, gostergeler, istatistik, katalog, kayit, motor, saglamlik, simulator, veri.
    - **İki not:** `veri.py` indirmeyi de içerir ama kapı ve karantina mantığı (`Anlik.gun_tablosu`, `adim`) kuraldır;
      dosya bölünmediği için bütünüyle listededir. `kayit.py` Holm, kabul girdisi ve K1 tekrar sayısının (B)
      hesabını içerir; o da listededir (muhafazakâr: kayıt kodu değişince yeni kayıt gerekir). Bu, tekrar
      sayısının değerinin hash dışı olmasıyla çelişmez: günlükteki `tekrar` alanı koşuda kullanılan değerdir; B'yi
      hesaplayan kod ve sabitleri (200, 1.000, 200·m) ise kuraldır. (karar.md:28; bilet 03)
    - Boru hattı denetimi (`denetim.py`) hash dışıdır. Kayıt pilotunun hash sınıfı §5.11'de belirtilir.
  - **Kod hash'i** kaynağın `ast.dump` sha256'sıdır; yorum ve boşluk değişmez.
  - **Hash dışı:** tekrar sayısının koşuda kullanılan değeri ve tohum (koşu argümanı); günlükte ayrı alan olarak
    yazılır. Blok uzunluğu argüman değil çıktıdır: ortalama tutma süresinden hesaplanır (`istatistik.blok_uzunlugu`,
    5.9) ve günlükte ayrı alan değildir; hesabın kodu hash içindedir. Masraf senaryoları (`simulator.MASRAFLAR`),
    K1 masrafı (`istatistik.K1_MASRAF`) ve B'nin sabitleri (`kayit.GELISTIRME`, `TAM_TABAN`, `TAM_CARPAN`) kural
    sabitidir: p değerini ya da kabul kararını değiştirirler, o yüzden hash içindedir. Masraf düzeyi başına sonuç
    günlükte ayrı alandır (`masraf_sonuc`). (bilet 07f, 15.10)
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
  - Çift bölmesi: en az 100 geçiş **ve** 60 farklı geçiş günü. Geçiş sayısı, tutuş dönemi (işlem) sayısıdır: nakitten
    ilk giriş de bir geçiş sayılır (5.6). (bilet 03, sözlük denetimi 6. tur)
  - Saptanabilecek en küçük etki günlük portföy serisinden hesaplanır ve raporda yazılır.
  - (Bilet 12) Güven aralığı: günlük fazla getirinin (kural − K2, %0,3) yıllıklandırılmış ortalaması (×252) üzerinde
    hareketli blok bootstrap, 1.000 tekrar, sabit tohum. Saptanabilir en küçük etki (yıllık, puan) =
    (1,645 + 0,842) · sd(günlük fazla) / √gün · 252 (tek yönlü %5, güç %80). Masrafla karşılaştırma işlem
    başınadır: MDE / yıllık işlem sayısı, %0,5 masrafın gidiş-dönüşünden (%1,0) büyükse "ölçülemedi" (5.12).
- **Ek gösterimler:** ortalamanın yanında medyan ve en iyi %5 işlem atılmış sonuç (işlemler sıralanır,
  üstten ⌈0,05·n⌉ işlem atılır). (m2, M10, İ: 19-070)

### 5.10 Parametre sağlamlığı
Parametreler ve ızgara önceden yazılır (`aile-kurallari.md` §3). Kurallar:
- Izgara hücreleri birlikte oynatılır. En iyi değer seçilmez.
  Tansu sınaması (5.14) en iyi bölgeyi seçer; bu kural yalnız `sinama` içindir (Levent kararı 16.10).
- **Pozitif hücre:** işlem başına ortalama fazla getiri > 0, %0,3 masrafla; fazla getiri = işlem getirisi − sepet
  getirisi (5.7 işlem seviyesi). Rastgele karşılaştırma (K1 tekrarı) yapılmaz; p aranmaz. (İ: 09-064; bilet 03)
- **Sağlamlık şartı:** pozitif hücre oranı ≥ %60. (İ: 04-089, karar.md)
- Bu oran bir olasılık değildir; hücreler birbirine bağımlıdır. (İ: 05-096)
- Izgara hücreleri ve masraf senaryoları Holm'daki deneme sayısına girmez. (m3, İ: 09-056)
- (Bilet 13) **Uygulama:** her koşu (K1'li) iki ailenin ızgarasını da koşar. Hücre sonucu: işlem başına ortalama
  fazla getiri (işlem getirisi %0,3 masraflı − sepet getirisi, 5.7 aynı tanım), gerçek sinyallerle, K1 tekrarı yok.
  İşlemi olmayan hücrenin fazla getirisi NaN'dir ve pozitif sayılmaz. Oran = pozitif hücre / bütün hücre; ölçüt 5'in
  sağlamlık değeridir (5.12). Hücreler `tur=destek`, `olay=hucre` satırı olarak günlüğe yazılır (5.11). Izgara:
  - EMA: eşik × en az gün × giriş penceresi (3·3·3 = 27); mum tablosu ve ısınma, SMA250, ATR sabit.
  - Çift: Z penceresi × Z eşiği × seçim p'si (2·3·3 = 18). Eşbütünleşme p'leri yılda bir, en geniş eşik (0,10) için
    hesaplanır; dar eşikli hücre aynı p'lerin önekinden seçer (her eşikle ayrı hesaplamayla aynı seçim, test); Z penceresi ve eşiği yalnız
    hedef günleri değiştirir. Seçim yılı, çift sayısı ve sektör sınırı ana kuralla aynıdır.

### 5.11 Çoklu deneme düzeltmesi ve deneme günlüğü

**Deneme günlüğü:** `kayit/deneme.jsonl`, yalnız ekleme. (M6, C-6, İ: 15-044, 15-046, 15-070, 12-030,
20-003, 13-034)
- **Hash dışı kayıt modülü:** `deneme.py`, `kayit.HASH_DISI` listesindedir; yalnız deneme olaylarını saklar, işlem sonucunu değiştirmez. Düz modül envanter testine girer. `kayit.py` dosyasındaki bu liste değişikliği §5.8 gereği yeni kod hash'i üretir; saklanmış eski kimlikler yeniden hesaplanmaz.
- **Satır başlangıcı ve bitişi:** her koşu önce `olay=basladi`, sonra `olay=bitti` satırı yazar.
  `bitti` satırı olmayan `basladi` de deneme sayılır.
- **Deneme sayısı (m), tek tanım:** Holm'un ve K1 tekrar sayısının (B, 5.7) m'si; resmi koşuların sınadığı (kural
  kimliği, aile) çiftleri sayar. Yarıda kalan, yani `bitti` satırı olmayan resmi koşu da m'ye sayılır (İ: 15-044);
  geliştirme koşusu sayılmaz. Aynı çift yeniden koşulursa ilk resmi p kalır. Başka bölümler (5.7, 5.12 boru hattı
  denetimi) m'yi yeniden tanımlamaz, buraya atıf verir. Yarıda kalan resmi koşunun (kural kimliği, aile) çifti Holm listesinde p = 1 ile yer alır; p = 1 sıralamada sona düşer, yani kabule yardım edemez, ve Holm ile B aynı tek m'yi kullanır. (bilet 03; vekil kararı 15.10, bilet 07d)
- **Varyant:** EMA ailesinin her varyantının kendi parametre parmak izi vardır; bu yüzden kendi kural kimliği vardır. Her
  varyant koşusu ayrı denemedir ve m'ye sayılır (varyantlar `aile-kurallari.md` §3). Başka bir kural değişmez. Yeni
  parametre alanları `bugun`'un da parmak izini ve kural kimliğini değiştirir (kural aynı); resmi koşudan önce yeni
  kural kaydı yazılır (`python -m tansu kayit`). Koşu varyantı `python -m tansu kayit|sinama --varyant <ad>` seçer
  (varsayılan `bugun`).
- **Alanlar:**
  - tarih (UTC ISO), `kosu_id`, `kural_id`
  - `kod_hash`, `param_hash`
  - anlık görüntü kimliği ve manifest sha256'sı
  - parametrelerin tam JSON kopyası
  - `git_commit`, tohum, tekrar sayısı
  - `sema`: günlük şema sürümü (şimdilik 1; İ: 15-046)
  - ham p, masraf düzeyi başına sonuç
  - ortam: Python ve kütüphane sürümleri, `requirements.lock.txt` sha256'sı
  - `resmi` ve `kirli` bayrakları
- **`tur` alanı:**
  - `kayit`, `deneme`, `destek` (ızgara, yeniden üretim, sınama), `sadakat`.
  - `duzeltme`: hedef koşu ve yeni değer yazılır; asıl satır değişmez.
  - Holm yalnız `deneme` satırlarını sayar.
  - (Bilet 13) `destek` satırları ve alanları: `olay=hucre` (her sağlamlık hücresi: `kosu_id`, `kural_id`, `aile`,
    `hucre` parametreleri, `islem`, `fazla`, `pozitif`; K1'li her koşu 27 + 18 satır yazar) ve `olay=denetim` (boru
    hattı denetimi: `kod_hash`, `kural_id`, yanlış kabul ve güç oranları, `gecti`). `basladi` satırı olmadığından
    `deneme_sayisi` ve Holm bunları saymaz.
- **Git:** `kayit/` izlenir (`deneme.jsonl`, `kartlar.jsonl`). Yalnız ekleme kuralının kanıtı git geçmişidir;
  `veri/` ve `rapor/` izlenmez. Kirli-ağaç denetimi `kayit/`'ı saymaz. (Bilet 09: `kayit/` kararı)
- **Kod sürümü doğrulaması:** Git sürümü ve kirli-ağaç denetimi, yüklenen `tansu` paketinin üstündeki proje kökünde çalışır.
  Başlatma klasörü ve kalıtılan `GIT_*` ortam değişkenleri bu seçimi değiştirmez. Doğrulama ana sürecin ortamını değiştirmez.
  Git'in bulduğu çalışma ağacı kökü proje köküyle aynı olmalıdır; üstteki başka bir depo kabul edilmez.
  Git komutlarının başarılı olması ve sürümün boş olmaması gerekir.
  Git çalıştırılamazsa veya bu doğrulama başarısız olursa `KayitHatasi` oluşur; `kosu` hesabı ve koşu kaydı başlamaz.
  `tansu-sinama` komutu aynı doğrulamayı ayar aktarımı nesnesi kurulmadan önce yapar; ilk doğrulama hatasında hesap,
  pilot kilit dosyası, çocuk deneme, ayar bağı, sonuç dosyası ve destek kaydı oluşmaz.
  Doğrudan sonuç yazıcısı da yazmadan önce yeniden doğrular. İlk doğrulamadan sonra oluşan yeni bir hata önceki eklemeleri geri almaz.
  Neden: doğrulanamayan sürüm temiz bir kod sürümü değildir.
- **Kirli ağaç:** `kosu(resmi=True)` kirli ağaçta tek Türkçe satırla durur, günlüğe satır yazılmaz (neden: resmi
  koşu temiz bir `git_commit`'e bağlanır; kirli ağaçta sessizce resmi olmayan deneme yazmak niyeti gizler).
  Geliştirme koşusu (`resmi=False`) kirli ağaçta yazılır, `kirli` bayrağıyla.
- **Silme yasağı:** `veri/` altındaki hiçbir anlık görüntü silinmez; günlükte adı geçen anlık görüntü her koşulda
  durur. (karar.md:24; bilet 03)
- **Başlangıç denetimi:** koşu başında manifest yeniden hash'lenir; uyuşmazsa koşu durur.

**Holm** (İ: 15-052, 15-065, 09-051, 15-076, 19-043):
- Her (kural kimliği, aile) çifti için tek p girer: ilk resmi koşunun %0,5 masrafta K1 iki türünün büyük p'si.
  %0,5 seçimi, 09-056'daki "%0,3'teki p"nin yerine geçer: ölçüt 3 (5.12) %0,5'te de geçmeyi şart koşar, p'nin
  kabul için gerekli en kötü masrafta hesaplanması muhafazakârdır (karar.md:31; bilet 03).- Geliştirme koşuları `resmi:false` yazılır ve m'yi şişirmez.
- Kabul kararı, kabul anındaki m ile donar; sonradan artan m eski kararı geri almaz.
- Rapor başlığı m'yi ve Holm hesap tarihini yazar; Holm rapor üretilirken yeniden hesaplanır.
- (Bilet 12) Birim: bir koşu iki aileyi sınar; Holm'a (kural kimliği, aile) çifti başına tek p girer, yani resmi
  koşu m'ye 2 ekler. Aynı çift yeniden koşulursa ilk resmi p kalır. Geliştirme koşusunun Holm p'si varsayımsaldır
  (bu p listeye eklenmiş gibi hesaplanır, günlüğe sayılmaz). Kâğıt'a geçen ailenin Holm p'si ve m'si `durum`
  satırında donar; sonraki koşular onu yeniden kullanır.
- (Bilet 12) `durum` satırı (`tur=durum`): her koşu sonunda aile başına bir yalnız-ekleme satırı; alanlar: aile,
  kural kimliği, koşu, durum (Deneme / Kâğıt), `holm_p`, `holm_m`, `resmi`, ölçüt durumları. Aile durumu en son
  `resmi=true` satırdır; yoksa Deneme. `bitti` satırı K1 sonuçlarını (`k1`: ham p'ler, gerçek istatistik masraf
  düzeyi başına, tekrar sayısı) taşır.
- Aynı tohum ve aynı anlık görüntüyle iki koşu aynı özeti verir (tek test).

### 5.12 Kabul ölçütü (önceden yazılır)

**Durumlar:** Deneme → Kâğıt → Canlı. (İ: 09-072, 11-082)
- **Kâğıt:** ölçüt 1–5'i geçen aile kart üretir; kâğıt üstü dönem başlar.
- **Canlı:** ölçüt 6'yı da geçen aile.
- **Kayıt:** durumu kod hesaplar; `kayit` yalnız-ekleme satırıyla yazar.
- **Para:** para kararı Levent'indir.

**Ölçütler:**
1. Yıllık sonuç dilimlerinin (5.8) birleşiminde, yani bütün koşuda K1'e göre fazla getiri pozitif, Holm düzeltmeli p < 0,05.
2. K2'ye göre portföy fazla getirisi pozitif.
3. Masraf %0,5'te de 1 ve 2 sağlanıyor.
4. Yılların en az %60'ında fazla getiri pozitif; en iyi %5 işlem atılınca sonuç hâlâ pozitif. (M10)
5. Örneklem şartı (5.9) ve sağlamlık şartı (5.10) sağlanıyor.
6. Kâğıt üstü canlı dönemde (5.8) fazla getiri, doğrulamadaki etkinin en az yarısı. (M7, M8)

**Ölçülemedi:** örneklem dolmazsa ya da saptanabilir en küçük etki %0,5 masrafın gidiş-dönüş tutarından
büyükse sonuç "geçmedi" değil "ölçülemedi"dir. (B-17)

**Ölçütlerin uygulanışı** (bilet 12; belge bu noktalarda sessizdi):
- Ölçüt 1: %0,3'te K1 işlem başına fazla getiri > 0 ve Holm p < 0,05 (p %0,5'te hesaplanır, 5.7).
  Ölçüt 2: %0,3'te günlük portföy fazla getirisi (kural − K2) ortalaması > 0.
  Ölçüt 3: %0,5'te aynı iki şart (K1 fazla getirisi ve portföy fazla getirisi pozitif, Holm p < 0,05).
  Ölçüt 4: tamamlanmış yılların (ilk ve son yarım yıl çıkar; çift bölmesinde "işlem yok" yılı da çıkar) %60'ında
  yıllık fazla getiri (%0,3) pozitif ve işlem fazla getirileri sıralanıp üstten ⌈0,05·n⌉ işlem atılınca ortalama > 0.
  Ölçüt 5: örneklem şartı ve sağlamlık oranı ≥ %60 (pozitif ızgara hücresi oranı, 5.10; örneklem dolmadıysa
  ızgara sonucu ne olursa olsun "Ölçülemedi"; oran koşuda hep hesaplanır ve raporlanır).
  Ölçüt 6: kâğıt dönemi başlamadan "Ölçülemedi".
- Genel: portföy kuralı reddederse "Geçmedi"; değilse örneklem ya da MDE şartı sağlanmıyorsa "Ölçülemedi";
  değilse bir ölçüt "Geçmedi" ise "Geçmedi"; bir ölçüt "Ölçülemedi" ise "Ölçülemedi"; yoksa "Geçti".
  Durum Kâğıt'tır ancak ve yalnız ölçüt 1–5 Geçti ve portföy kuralı reddetmediyse.
- Portföy kuralı %0,5 masraflı ve faizli özkaynak eğrisinde: en büyük düşüş > %25 ya da düşüşte kalma > 12 ay.

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
- (Bilet 13) **Komut:** `python -m tansu denetim [--n 200] [--tekrar 200]`. Sonuç `docs/denetim.md`, `rapor/denetim-*.html`
  ve günlükte (`tur=destek`, `olay=denetim`, `gecti` bayrağı, kod hash'i) yazılır. Yanlış kabul > %5 ise çıkış kodu 1'dir
  ve `kosu(resmi=True)` ilk resmi koşuyu bu kodun hash'iyle geçmiş bir denetim yoksa durdurur (başarısız denetim de
  engeller). Denetim, ilk resmi koşu tamamlanana dek aranır: tamamlanma, resmi koşunun `bitti` satırıdır. Yarıda kalan
  resmi `basladi` m'ye sayılır (5.11) ama kapıyı açmaz (neden: yarıda kalan koşu hiçbir sonuç üretmedi, denetimsiz
  ikinci deneme hakkı doğmaz). Tamamlanan ilk resmi koşudan sonra denetim aranmaz.
- **Boş dünya** (`denetim.dunya`): 125 sentetik hisse, 2.000 iş günü (02.01.2012'den), 4 sektör; günlük getiri = piyasa
  payı · piyasa yükü + sektör payı + hisse payı (piyasa yükü: piyasa payının çarpanı; çift seçimindeki β değildir), kalın kuyruklu (t(5), birim varyans), ±%7'ye kırpılmış (limit ve kilit olmaz).
  Hiçbir kural getiri öngörmez: sinyalden sonraki getiri bağımsızdır. Sentetik anlık görüntü gerçek `veri` kapılarından
  geçer (test: karantina, kilit, olay uyarısı yok), olay yok, faiz tablosu ve sektör var, evren aynı kuralla (125
  hisseden likidite eleğiyle 100: gerçek koşudaki evren boyutu; 40 hisseli dünyada K1 (a) havuzu sinyal sayısına eşit
  kalıp rastgelelik vermiyordu). Simülasyon 02.12.2013'te başlar (ısınma 500 gün).
- **Yanlış kabul** = boş dünyada ölçüt 1–4 Geçti ve portföy kuralı reddetmedi (örneklem ve sağlamlık şartı aranmaz,
  yani Kâğıt'ın üst kümesi; sentetik dünya 100 işlem örneklemini dolduramayabilir ve o zaman Kâğıt oranı boş yere
  sıfır olurdu). Kâğıt oranı da raporlanır. Şart: her ailede oran ≤ %5, 200 tekrarda (seçilen tohumlar 0…199).
  Her tekrar gerçek yoldan (`kayit.hesapla`: motor, simülatör, K1, ızgara, Holm, kabul) geçer; K1 B = 200 (geliştirme
  sayısı; p tabanı 1/201, Holm m = 2 için eşik 0,025'in altında, yani eşiği geçmek mümkündür; B artınca p dağılımı
  değişmez, yalnız inceleşir) ve Holm m = 2 (iki aile; resmi koşuda m ≥ 2, yani denetim en gevşek durumdur).
- **Etkili dünya** (güç): boş dünyadan hesaplanan her kural sinyalinde, sinyali izleyen günün (giriş günü) AOF'u
  `1 + etki`'ye bölünür (`denetim.etki_ekle`); kapanış ve öteki günler aynıdır. EMA'da sinyalin hissesinde, çiftte
  sinyalin geçtiği bacakta. Kural işlem başına yaklaşık `etki` kazanır, rastgele girişler (K1) kazanmaz. (Fiyatı kalıcı
  kaydırmak denendi ve bırakıldı: sinyalden önceki günlerde giren rastgele işlem de aynı kazancı alıyor, K1 etkiyi
  görmüyordu.) Etki düzeyleri %5 (belge 14-048) ve %10; her aile × etki düzeyi n/10 = 20 dünyada koşar (tohumlar 1000…).
  Güç = aynı ölçüt (1–4) geçen oran; yalnız rapor, şart yok. Etki çiftte yaklaşıktır: AOF yeni seçimden ve Z'den bağımsız
  kalır ama sinyaller boş dünyadan hesaplanır.
- **Geleceği görmeme testi** (`tests/test_gelecek.py`, bilet 13): sentetik dünyada veri t'de kesilir (fiyat satırları
  ve faiz değişimleri t'den sonrası atılır); tam görüntünün t'ye kadarki çıktısı kesilmişle aynı olmalı. Tek parametrik
  test, bileşen × dört kesim günü: 2014-09-30, 2015-01-15, 2015-03-02 ve yılın son işlem günü 2014-12-31 (yıllık fazla
  getiri için biten yılın karşılaştırılması; bilet 07d, 15.10). Kapsam: evren (ay başı seçimi), göstergeler (EMA, SMA, Wilder ATR, sıkışma oranı,
  RSI, momentum squeeze, ADX, MACD, PSAR, stokastik, piyasa durumu), EMA sinyali ve ön şart dizileri, EMA kurulumu (kutu,
  arz ve talep bölgeleri, salınım noktaları, hedef, `arz` ve `ucgen` girişleri, düşüş süzgeci), S09 tek hisse işlem geçişi (günlük durum/dolum öneki), çift Z ve hedef günleri,
  yıllık çift seçimi, likidite medyanı, faiz hizalaması (gecelik getiri dizisi), K2 sepeti ve Tansu sınaması (EMA ve çift;
  5.14: hücre işlemleri ve ileri yürüme seçimleri; t'den önce biten test yılları aynı).

### 5.13 Veri kapıları
Getiri görülmeden yazılır; kural kaydına girer. (B-7, İ: 19-015)
- **Satır ihlali:** düşük ≤ AOF ≤ yüksek ve düşük ≤ kapanış ≤ yüksek sağlanmazsa karantina. Ham ya da
  düzeltilmiş fiyatı ≤ 0 olan satır da bozuktur. Düzeltilmiş seride bağıl 1e-4 yuvarlama payı tanınır
  (gerçek veride düzeltilmiş seri 4 ondalığa yuvarlı: 637 satırda en çok 4,5e-5 fark; gerçek ihlaller ≥ 1,5e-3).
- **Yapısal ihlal:** bozuk sıra ya da tekrar eden gün koşuyu durdurur. Satır içindeki NaN durdurmaz:
  kısmi NaN'li satır bozuk satırdır, karantinaya girer (bilet 07, ~900 sembolde tek satır, örn. IZINV
  13.11.2013 yüksek 634210 / hacim NaN, bütün indirmeyi saatler sonra düşürüyordu; oran eşiği zaten
  korur). İstisna 1 (bilet 07, gerçek veri: BERDN 30.01.2012, ISATR 23.06.2010): ham fiyatların ve
  hacmin hepsi NaN ya da 0 olan satır işlem yapılmamış gündür; indirmede atılır (eksik gün, 5.1).
  İstisna 1b (BYDNR 23.08.2023, KUVVA 2020–): fiyat ve hacim alanları aynı olan tekrar satır tek
  sayılır, ilki kalır (KUVVA'da yalnız `PD` ve `SERMAYE` farklıydı: iki sermaye değeri; piyasa değeri o
  aralıkta belirsiz); fiyat ya da hacim alanları farklı tekrar ihlaldir (yalnız hacmi farklı satır da: yapısal ihlal, indirme durur; bilet 03, sözlük denetimi 10. tur). İstisna 2: İş Yatırım
  GARAN yanıtını 276 yerde sırasız verir (satır eksiksiz, tekrar yok; bilet 06'da görüldü); `kaynak` yanıtı
  tarihe göre sıralar, kapı sıralamadan sonraki seriye bakar.
- **Kaynak günü hatası** (bilet 11 kararı): o gün satırı olan sembollerin en az yarısı aynı gün karantinadaysa
  (en az 20 satırlı gün) bu hisse sorunu değil, kaynak sorunudur (21.05.2026: 556/607 sembol, yüksek = düşük =
  kapanış, AOF aralığın dışında). O gün tüm semboller için eksik gün (NaN) olur: karantina yok, zorunlu çıkış yok,
  dolum yok (çıkış dolumu sonraki geçerli güne kayar, giriş bekleyen sinyal düşer; öbür eksik günler gibi, 5.3; bilet 03, sözlük denetimi 2. tur). Sebep: tek bozuk kaynak günü bütün açık
  pozisyonları oynatmamalı. Rapor ve `sorunlar` günü tarihle yazar ("kaynak günü hatası: YYYY-AA-GG"). Gün
  karantina sayısına girmez. Alt sınır 20 satır: tek sembollü sentetik sınama günleri ve çok az sembollü
  erken günler kaynak günü sayılmaz.
- **Oran eşikleri:** karantina hisse-gün oranı > %1 ya da olay denetimi farkı olan gün oranı > %2 ise
  koşu "veri sorunlu" olur. Eşik değerleri değişmez.
  - **Payda ve pay yalnız evren üyesi hisse-günlerdir** (bilet 10 kararı): sınama yalnız evren üyelerinde işlem
    açar (5.2). Evren dışı illikit kodların bozuk satırları (indirilen bütün hisselerde karantina %3,00; ilk 20 sembolde
    %42) sınamayı etkilemez, ama oranı şişirip kapıyı hep tetikler. Üye hisse-günü: hissenin, o ayın
    evreninde (5.2) bulunduğu ayın fiyat satırları (sınama başlangıcından itibaren).
  - İndirilen bütün hisselerin oranları `Anlik.sorunlar` ile hâlâ hesaplanabilir; kapı kararı üye oranlarıyla verilir (bilet 03, sözlük denetimi).
  - Kapı tetiklenirse koşu yine yazılır; rapor "SORUNLU" der ve iki oranı yazar. Eşik gevşetilmez.
- **Eksik indirme:** 100 hisseden 5'ten fazlası inmezse koşu SORUNLU olur.

### 5.14 Tansu sınaması (Levent kararı 16.10)

Levent 16.10: "Tansu ne diyorsa onu yap." Komut: `python -m tansu tansu-sinama`. Tansu'nun kendi sınama yöntemini uygular.
5.1–5.13 ve `sinama` komutu değişmez; 5.10'daki "En iyi değer seçilmez" `sinama` için geçerli kalır. Bu komut kabul kararına
(5.12) girmez, kart üretmez, m'yi (5.11) artırmaz. Tansu'nun Ham metni bizim YORUM'umuzdan üstündür; Levent kararı ikisinden de.
- **Hisse başına optimizasyon:** her strateji her hissede (çift ailesinde her çiftte) ayrı ızgarayla koşulur. "Lütfen bu
  parametreleri optimize edin." (Ham, tweet-ema-parametre-optimizasyonu-1840438972859732044); "her hisse için farklı
  parametrelerde giriş çıkış yapmak lazım." (Ham, tweet-hisse-bazli-parametre-optimizasyonu-1840170065464803535). Izgara
  `aile-kurallari.md` §3'tekidir: EMA 27 hücre; çift Z penceresi × Z eşiği, 6 hücre (seçim p'si yıllık çift seçimine aittir, burada yok).
- **Dönem:** Tansu modu bütün dönemdir: "Biz model eğitmedik kardeşim," (Ham, tweet-atr-yon-degisimi-dip-tepe-1927454690960101506).
  Dönem, dönem başından dönemin son gününe dektir. Dönem başı: 2015-12-01 (5.1) ile ısınmanın bittiği günün (tek hisse 500
  kapanış günü, çift 252 ortak kapanış günü; 5.1) geç olanından başlayarak (o gün dahil) ilk geçerli fiyat günü (çiftte iki
  bacağın da geçerli fiyat günü olduğu ilk gün). Isınması dolmayan, dönem başı dönemin son gününe dek bulunmayan hisse ve 252 ortak günü olmayan çift
  sınanmaz; adları çıktıda `atlanan` listesinde yazılır. Çıktı her hisse için `donem` alanında dönem başını ve son gününü yazar.
- **İki tanım** (YORUM, bizim, 17.10; Tansu'nun notlarında yok):
  - *Geçerli fiyat günü:* hissenin `gun_tablosu`nda `islem` doğru ve `karantina` yanlış olan, AOF'u ve kapanışı sıfırdan büyük
    ve sonlu olan gün. Eksik, işlem görmeyen, karantinalı ve NaN, sıfır ya da sonsuz fiyatlı gün geçerli değildir. Bu modülün
    kendi fiyat okumaları yalnız geçerli fiyat gününü kullanır: dönem başı, al-tut alışı ve satışı, özkaynağın kapanışla
    değerlenmesi (son geçerli kapanış ileri taşınır), 1, 3 ve 5 gün sayımı, çiftte geçiş günü (iki bacak da geçerli). Bu
    tanım şunları değiştirmez: sinyal ve ısınma sayımı ailenin ve 5.1'in kuralıdır (kapanışı olan günler; karantinalı gün
    dahil; karantinadan sonraki 250 satır giriş açmaz); tek hisse işleminin giriş ve çıkış fiyatı motordan gelir (5.3, 5.5;
    veri sonu çıkışı motorun son kapanışıdır, işlem görmeyen gün de olabilir).
  - *Dönemin son günü:* hissenin `gun_tablosu`ndaki son satırı; çiftte iki bacağın son satırlarının erken olanı. Fiyatının
    geçerli olması gerekmez. Özkaynak eğrisi, maruziyetin paydası, karantina engeli ve ileri yürümenin son takvim yılı bu
    günü kapsar.
  - Uç durumlar: (1) son gün karantinalıysa (kapanışı olsun olmasın) açık pozisyon o gün karantina kuralıyla son temiz AOF'tan
    çıkar (5.3; çiftte 5.6), "veri sonu" çıkışı olmaz. (2) Sıfır ya da sonsuz fiyatlı gün bu modülün fiyat okumalarında yok sayılır;
    hiçbir çıktı sonsuz ya da NaN olmaz. Veri katmanı sıfır ve NaN fiyatlı günü karantinaya alır (5.1), tutarlı sonsuz
    düzeltilmiş fiyatlı günü almaz. Bu yüzden düzeltilmiş AOF'u ya da kapanışı sonsuz olan gün bu modülde iki ailede karantina
    günüdür: açık pozisyon o gün son temiz AOF'tan çıkar ve 250 satır giriş açılmaz (5.3, 5.6); motora bu bayrakla verilir. (3) AOF'u olmayan gün dönem başı olamaz; dönem başı sonraki geçerli fiyat günüdür. (4) Dönem tek gün olabilir:
    işlem olmaz (giriş ertesi günü ister), net 0,0, maruziyet 0, Sharpe ve Calmar yok; al-tut aynı günün AOF'undan alıp
    kapanışından satar. Testler iki ailede: (1) NaN, sonsuz ve sonlu kapanışlı karantinalı son gün; (2) ve (3) dönem başında,
    son günde ve 1, 3, 5 gün sayımında geçersiz gün, sonsuz düzeltilmiş fiyatın karantina çıkışı ve sonraki 250 satırda giriş engeli
    (`test_ema_sonsuz_duzeltilmis_fiyat_giris_engeli_250_satir` ve
    `test_cift_sonsuz_duzeltilmis_fiyat_giris_engeli_250_satir`: tek hisse ve çift yollarında engel içinde giriş açılmaz,
    engel sonrası açılır); (4) tek günlük dönem.
- **İleri yürüme (ikinci mod):** "EMA değeri walk forward le optimzie edilerek model oluşturulmuştur." (Ham,
  gorsel-paket-75-isctr-ad-ema-walk-forward). YORUM (bizim): her takvim yılı test yılıdır; seçim o yıldan önce kapanmış
  bütün işlemlerle (genişleyen pencere) aynı sağlam bölge kuralıyla yapılır; en az 2 tam eğitim yılı; test yılında seçilen
  hücrenin giriş günü o yılda olan işlemleri alınır, önceki işlem kapanmadan giren işlem atılır. Sağlam bölge yoksa o yıl nakit.
  Son test yılı dönemin son gününün yılıdır.
- **İşlem:** sinyal ve dolum 5.3 ve 5.5 kuralıdır: sinyal kapanışta, giriş ertesi günün AOF'unda (bir çubuk gecikme; Tansu'nun
  kodunda `position.shift(1)`, görsel, tweet-sma-geri-test-sinifi-python-1831402232769847775), acil stop 2 ATR, gün sonu stopu
  SMA250. Çift: geçiş ertesi günün AOF'unda; 5.6'daki engeller (işlem yok, kilit, karantina penceresi) aynıdır. YORUM (bizim):
  tek pozisyon, sermayenin hepsi işlemde, kesirli adet; boştaki nakit faiz kazanmaz (Tansu'nun al-tut kıyaslarında faiz yok).
- **Masraf (`legacy_tansu_v1`):** her yönde %0,10, kayma yok: Tansu'nun tablosunda "Komisyon: %0.10" (görsel,
  tweet-winrate-80-tarama-backtest-tablosu-2092745592661246196). İşlem getirisi = çıkış·(1−m) / (giriş·(1+m)) − 1.
  Yeni `komisyon_bsmv_v1` sürümü §5.15 S08 hesabını kullanır; eski sonuçların masrafı değiştirilmez.
- **Al-tut:** aynı hisse, aynı dönem: dönem başının AOF'unda al, dönemin son gününe dek son geçerli fiyat gününün kapanışında
  sat, aynı masraf. Çiftte 50/50, başta bir kez.
- **Ölçüler** (Tansu'nun tablosunun sütunları, aynı görsel): kazanma oranı, işlem, kazanan, kaybeden, kâr çarpanı (kazançlar
  toplamı / kayıplar toplamının mutlak değeri), ortalama işlem, strateji getirisi, al-tut getirisi, fark, en büyük düşüş, Sharpe,
  Calmar, ortalama tutma (gün), maruziyet, kazanç/kayıp oranı. Ek: işlem getirisinin medyanı ("Ortalamaları temel alan
  indikatörler hava civadır Medyan temelli çalışın", Ham, tweet-medyan-temelli-finansal-indikatorler) ve sinyalden 1, 3 ve 5 gün
  sonraki getirinin medyanı ("sonraki 1, 3 ve 5 günde ne olmuş bakın", Ham, not-backtest-giris-sadeligi-risk-islem-gunlugu).
  Tanım: sinyal günü ya da ondan önceki son geçerli fiyat gününün kapanışından, sinyal gününden sonraki k. geçerli fiyat
  gününün kapanışına getiri (k = 1, 3, 5; çiftte alınan bacağın günleri). Geçerli olmayan gün sayılmaz.
  YORUM (bizim): Sharpe = günlük getiri ortalaması / sapması × √252, risksiz getiri 0; Calmar = yıllık bileşik getiri /
  |en büyük düşüş|; maruziyet = pozisyonda kapanan gün / dönem günü.
- **Şüpheli bayrakları** (etikettir, süzgeç değil): kazanma oranı ≥ %90 → "şüpheli: aşırı uyum" ("%90'lar ise mümkün
  değildir.", Ham, gorsel-paket-129-doas-lojistik-regresyon-hacim-rsi-filtreli-strateji; eşik bizim YORUM); işlem < 5 →
  "az işlem" (Tansu'nun tablosunda süzgeç "İşlem >= 5", aynı görsel).
- **Sağlam bölge** (kurallar/E K31): "Ama sadece tek bir nokta (13, 47) kârlı, hemen yanındaki (14, 48) felaket zarardaysa,
  bil ki o bir tuzaktır." (Ham, tweet-sma-optimizasyon-saglam-bolge-asiri-uyum-1986899794032304554). YORUM (bizim; vekil 16.10):
  komşu = tek eksende bir adım ötedeki hücre; hücre sağlamdır ⇔ kendisi ve bütün komşuları masraf sonrası net getiri > 0.
  Seçilen hücre = sağlam hücreler içinde komşuluğundaki (kendisi dahil) en küçük net getirisi en büyük olan; eşitlikte ızgara
  sırasındaki ilk. Sağlam hücre yoksa "sağlam bölge yok"; en iyi tek hücre gösterilir, seçilmez.
- **Para çıkmaz:** en iyi hücrenin net getirisi ≤ 0 ise: "Eğer en iyi ayarları bile para kazandırmıyorsa, o stratejiyle vakit
  kaybetmeyi bırakırsın." (Ham, aynı not).
- **Çift adayları** (YORUM, bizim; vekil 16.10): aynı sektördeki hisse çiftleri (5.6 YORUM'u), Y = sembol sırasına göre ilk.
  Günlük anlık görüntüde sektör yoksa sektör tablosu `--sektor-kok` altındaki en yeni tam anlık görüntüden okunur (5.2:
  bugünkü sınıflama). Site denenen çift sayısını ve sağlam bölgeli çiftlerin oranını yan yana yazar.
- **Makine ve paralellik** (Levent kararı 16.10): koşu başında mantıksal ve fiziksel çekirdek, boş bellek ve GPU ölçülür.
  İşçi sayısı = min(fiziksel çekirdek, boş bellek × 0,8 / 0,25 GB, iş sayısı), en az 1; iş birimi bir hisse ya da bir çifttir.
  Sonuç işçi sayısından bağımsızdır (test). İşçi süreçleri her platformda `spawn` yöntemiyle başlar (Windows'un yöntemi;
  Linux'ta Python 3.14'ün varsayılanı yerel soket açar, testteki ağ engeli onu da durdurur; CI, 17.10). Koşu ilerlemeyi yazar: biten / toplam iş, geçen süre, tahmini kalan süre, CPU
  kullanımı. Gerekçe (YORUM, 16.10 ölçümü, 1.205 iş): 1 işçi 39,6 sn, 16 işçi 7,4 sn, 24 işçi 7,5 sn, 32 işçi 8,3 sn; yani
  32 mantıksal çekirdek 24 fiziksel çekirdekten yavaştır ve 16 işçiden sonra kazanç yoktur. İşçi başı tepe bellek 0,17 GB
  ölçüldü; 0,25 GB bu değer artı paydır.
  GPU (16.10): makinede RTX 5070 Ti var; GPU hesap kütüphanesi yok (torch 2.14.0+cpu, CUDA yok; cupy yok). GPU hızı
  ölçülemedi; GPU kullanılmaz. İş gün gün yol bağımlı bir döngüdür; bütün koşu 24 işçide 7,5 sn sürer.
- **Kayıt ve çıktı:** sonuç `rapor/tansu-sinama-<koşu>.json`; deneme günlüğüne `tur=destek`, `olay=tansu_sinama` satırı
  (koşu kimliği, anlık görüntü ve manifest sha256'sı, `git_commit`, `kirli`, makine, işçi, süre). Holm ve m bunu saymaz (5.11).
- **Ayar aktarımı:** `--varyant`, Tansu sınamasına ve günlük koşuya da seçilen eski varyantın
  parametrelerini iletir (#88). EMA ızgarasında her hücrenin sinyali ve kurulumu aynı hücre
  parametreleriyle bir kez üretilir. Motor hücrenin ayarını ve kurulumunu birlikte alır.
  Her hücre ayrı `Zincir` kullanır; başka hücrenin işlem önbelleğini kullanmaz. Izgaranın
  mevcut eksenleri gösterge dönemlerini ve ısınmayı değiştirmez; bunlar seçilen varyanttan gelir.
  Sonuç biçimi ve eski kayıtlar değişmez. Kayıtlı yolun sınırı §5.15 "Ayar aktarımı" bölümündedir.
  Dayanak: #88 görev girdisi, üç eksik aktarım. Sonuç testleri `tests/test_ayar_aktarimi.py`,
  gelecek veri denetimi `tests/test_gelecek.py` kapsamındadır.
- **Bizim ek kontrolümüz:** aynı ailenin son resmi `durum` satırı (5.11, 5.12) çıktıda ve sitede yanında durur.
- **Hash:** `tansusinama.py` hash dışıdır (kabul kararını değiştirmez). `HASH_DISI` listesine eklenmesi `kayit.py`'nin hash'ini
  değiştirir: sonraki resmi koşudan önce `python -m tansu kayit` gerekir.

### 5.15 Motor davranış sözleşmesi (S01, #82)

Bu bölüm #76 motorunun belge sözleşmesidir. Uygulama, veri indirme, günlük etkinleştirme ve kalıcı kimlik
biçiminin onayı bu işin dışındadır. Teknik engel kapanmadan ilgili yöntem uygulanmaz. Dayanak: [L1], [L5], [W1].

#### Kaynaklar ve karar yetkisi

Köken etiketleri ayrıdır: **LEVENT KARARI**, **CLAUDE TEKNİK KARARI / YORUM**, **ARAŞTIRMA ÖNERİSİ** ve
**AÇIK KAPI**. Bir internet örneği Tansu kuralına, araştırma önerisi de kendiliğinden onaya dönüşmez.
Teknik girdilerin dağıtıcı kontrol tarihi 19.10.2026'dır; bu tarih araştırma tarihi değildir. Dayanak: [L5], [W1].

| Kod | Kaynak, tarih ve kanıt sınırı |
|---|---|
| L1 | Levent, 18.10.2026: "Başlangıç sermayesi önemsiz çünkü bu bir bir nevi sinyal platformu." ve "Yüzde iki uygun." Kaydedilen yanıt: `soru-turu/cevaplar-levent.md`, Grup 1. |
| L2 | Levent, 18.10.2026: "Ortak para falan yok. Her işlem ayrı gibi düşün." ve "Her tarihte o dönemin BIST 30 üyelerine göre yapalım." Aynı yanıt kaydı, Grup 2 ve devamı. |
| L3 | Levent, 18.10.2026: "Hani son fiyattan devam etsin. 2022'de sınamaya dahil olsun." Aynı kayıt, son Grup 2 yanıtı; yıllar: 2025, 2024, 2023, 2022, 2021 ve birleşik dönem. |
| L4 | Levent, 18.10.2026: "Kazanma oranı tek başına bir strateji elemesin." ve "Bir sonucu güvenmek için yani bunları ben sonuçları gördükçe karar verebilirim bence." Aynı kayıt, Grup 3. |
| L5 | Levent, 18.10.2026: "Tabii önce Tansu sonra internet." ve "Monte Carlo resmi olarak nasıl yapılıyorsa öyle yapılmalı. Walk forward da walk forward da olacak tabi." Aynı kayıt, teknik sorular ve Grup 3 devamı. |
| L6 | Levent, 18.10.2026: "Komisyonunu alınsın. Ortalama bir şeyler yaz çok önemli değil." Aynı kayıt, Grup 1. Oran ve BSMV aşağıda Claude'un teknik seçimidir; Levent'in 20.10.2026 onayı S08'dedir. Vergi mevzuatı iddiası değildir. |
| T1 | Tansu, 07.11.2025: "İyi optimizasyon, \"sağlam\" (robust) bir bölge bulmaktır." Ham: `tweet-sma-optimizasyon-saglam-bolge-asiri-uyum-1986899794032304554.md:51`; komşu tuzağı satır 53. Tam not bu işte okundu. |
| T2 | Tansu, 09.11.2025: "Amacımız, her işlemde aynı TL riskini korumaktır." Ham: `tweet-volatiliteye-gore-pozisyon-buyuklugu-1987500065401733478.md:25`. Yüzde örneği Levent'in oranını değiştirmez. |
| T3 | Tansu, 02.09.2026: "Pozisyon büyüklüğünü stop mesafesine göre hesaplayın." Ham: `not-backtest-giris-sadeligi-risk-islem-gunlugu.md:37`; işlem günlüğü satır 39, aday ufukları satır 31. |
| T4 | Tansu, 04.09.2026: "Ancak hisse tabana kilitlendiğinde geçmiş hacmin hiçbir anlamı kalmayabilir, satıcı vardır ama alıcı yoktur." Ham: `tweet-fon-konsantrasyon-para-cikisi-likidite-riski-2095997339391414488.md:27`. Tam günlük dolum algoritması bu alıntıda yoktur. |
| W1 | [AmiBroker ileri yürüme](https://www.amibroker.com/guide/h_walkforward.html), tarihsiz; araştırmada erişim 18.10.2026: geçmişte seç, sonraki kesitte sınayarak ilerle. Kesin TANSU pencere boyu vermez. |
| W2 | [AmiBroker Monte Carlo](https://www.amibroker.com/guide/h_montecarlo.html), tarihsiz; araştırmada erişim 18.10.2026: yerine koymalı işlem örnekleme, en az 1.000 önerisi ve örtüşen işlemlerde sıralı sermaye sınırı. |
| W3 | [AmiBroker optimizasyon](https://www.amibroker.com/guide/h_optimization.html), tarihsiz; araştırmada erişim 18.10.2026: geniş plato ilkesi. Kesin komşuluk veya merkez seçimi vermez. |
| W4 | [Backtrader emir gerçekleşmesi](https://www.backtrader.com/docu/order-creation-execution/order-creation-execution/), tarihsiz; araştırmada erişim 18.10.2026: kapanış bilgisiyle geçmişe dönük dolum kurulmaz. AOF kullanımı TANSU yaklaşımıdır. |
| W5 | [BIST 2020/20](https://borsaistanbul.com/en/announcement/13357/changes-price-limits-equity-and-derivatives-markets), 12.03.2020, uygulama 13.03.2020; [2023/19412](https://www.borsaistanbul.com/files/duyuru-19412.pdf), 28.08.2023, uygulama 06.11.2023; [Pay Piyasası Prosedürü](https://www.borsaistanbul.com/files/pay-piyasasi-proseduru.pdf). Araştırmada erişim 18.10.2026; tarihli limit ve adım dayanağı. |
| W6 | [Van Tharp, Risk and R-Multiples](https://vantharpinstitute.com/tharp-think-trading-concepts/), tarihsiz; araştırmada erişim 18.10.2026: ilk riskle normalizasyon. Masrafın bütçeye katılması TANSU seçimidir. |
| W7 | [Sharpe, The Sharpe Ratio](https://www-leland.stanford.edu/~wfsharpe/art/sr/sr.htm), 1994 sonbaharı; araştırmada erişim 18.10.2026: eş dönemli fark getirisi. İşlem listesi günlük hesap eğrisi değildir. |
| W8 | [DVC kullanıcı kılavuzu](https://doc.dvc.org/user-guide), tarihsiz; araştırmada erişim 18.10.2026: içerik kimliği ve yeniden üretim dayanağı. Aşağıdaki alanlar S01'in YORUM sözleşmesidir; DVC bağımlılığı veya evrensel şema değildir. |
| W9 | [arch güven aralıkları](https://bashtage.github.io/arch/bootstrap/confidence-intervals.html) ve [blok uzunluğu](https://bashtage.github.io/arch/bootstrap/generated/arch.bootstrap.optimal_block_length.html), araştırmadaki sürüm 8.0.0, tarihsiz; erişim 18.10.2026. Bağımlı serilerde blok örnekleme dayanağıdır. |

L kaynaklarının kayıt kökü `YONETIM/.scratch/backtest-motoru-1810/`, T kaynaklarının kökü beyindeki
`kisisel/300-Projects/Tansu X Veri Havuzu/` klasörüdür. Web sayfaları bu işte yeniden açılmadı; kaynaklar
verilen araştırma dosyalarından aktarıldı. Dayanak: [L5], [W8].

#### Dokuz çelişkinin karar kaydı

| Kimlik | Eski politika | Yeni sözleşme ve durum | Dayanak | Etkilenen işler |
|---|---|---|---|---|
| C01 | §3 paneli erteler; §4 mevcut düz paketi anlatır. | LEVENT KARARI: kişisel sinyal paneli kapsamda; altı motor aşağıdaki görev sınırlarıyla yerel uygulama içinde tasarlanır. Fon ve kripto bu motor sürümünün kapsamı dışındadır; sahipte bekler. S01 bunları kurmaz. | [L1], [L5]; #82 brifi, tasarım taslağının E1–E6 tablosu; fon/kripto: bu işin kapsam talimatı. | #83–#97; panel #96. |
| C02 | §5.2'de likidite ve piyasa değeriyle yaklaşık BIST100. | LEVENT KARARI: her tarihte o dönemin BIST 30 üyeleri. Yürürlük aralıkları ve duyuru kaynakları kayıtlıdır; bugünkü liste geçmişin yerine geçmez. Üyelik açığı ilgili koşuyu eksik bırakır. | [L2]; teknik veri sınırı [W8]. | #85, #86, #91. |
| C03 | §5.6'da %1 risk, ortak nakit, pozisyon ve likidite tavanları. | LEVENT KARARI: işlem başına %2 risk; ortak nakit, ortak risk bütçesi ve portföy tavanı yok. İşlemler birbirinin parasını tüketmez. CLAUDE TEKNİK KARARI: tek strateji/sembol yaşam döngüsü açıkken ek aday kaydedilir, adet eklenmez (B Q73). Çiftin risk dayanağı ve masraflı risk formülü RISK kapısındadır. | [L1], [L2], [T2], [T3], [W6]. | #89, #90, #92–#95. |
| C04 | §5.2 ve §5.6 kapanmada sıfır fiyat/−%100; 60 günlük durdurma kapanma sayılır. | LEVENT KARARI: doğrulanmış durdurma/kapanmada son geçerli fiyat değerlemede taşınır; otomatik −%100 yok. Son fiyatla idari sonlandırma, gözlenmiş satış dolumu değildir. Satış tarihi ve dolum fiyatı gerçek/model dolum yoksa boş kalır. Son fiyatın tarihi ve neden kaybolmaz. | [L3], [T4], [W4]. | #85, #90–#92. |
| C05 | §5.8 sürekli koşunun yıllık dilimleri; §5.14 bütün dönem. | LEVENT KARARI: beş ayrı yıllık koşu ve birleşik koşu. Dönem ve ısınma sınırları aşağıdadır. Yıllık sonuçlar birleştirilerek birleşik koşu üretilmez. | [L3]; teknik sınır [W1], D §2. | #87, #90–#94. |
| C06 | §5.4 her yönde %0,3 toplam masraf ve senaryolar; §5.14 %0,10. | CLAUDE TEKNİK KARARI (18.10, 19.10 kontrolü; Levent'in 20.10.2026 onayı S08'dedir): yeni yolda yön başına %0,15 komisyon, komisyon üstünden %5 BSMV. Her dolumun kendi tutarı kullanılır; kayma ayrı kalır. Eski iki maliyet sürümü korunur. | [L6]; yanıt Grup 1, C giriş ve D §1; [W4]. | #89–#94. |
| C07 | §5.11 resmi (kural kimliği, aile) çiftleri Holm m'sidir; destek hücreleri sayılmaz. | LEVENT KARARI / S01 kayıt sözleşmesi: her ayar revizyonu ayrı kayıt; aynı değerlere dönüş de yeni revizyon. Yeni revizyon sayısı Holm m'si değildir. Eski resmi sayım değişmez; yeni hipotez ailesi ayrıca beyan edilir. | [L4], [W8]; taslak kayıt tablosu, C Q87. | #84, #87, #91–#94, #97. |
| C08 | §5.12 kabul kapıları ve §6 aile durumuyla günlük kart; §5.14 sonuçları kart dışı. | LEVENT KARARI: araştırma sonuçları görülebilir; kâr veya kazanma oranı günlük izin vermez. Günlük uygunluk tam strateji/ayar/kod/veri/politika kanıtıyla ve ayrı seçim kaydıyla bağlanır. SAHİP kapıları 86, 111, d5 açıkken #95 etkinleşmez. | [L4], [W8]; C Q86/Q111, D §5. | #95, #96. |
| C09 | §5.14 genişleyen, en az iki eğitim yıllı ileri yürüme; özel Monte Carlo sözleşmesi yok. | LEVENT KARARI: MC ve WF gerekir. CLAUDE TEKNİK GİRDİ: aşağıdaki yöntem kayıtları. Çelişen araştırma ayrıntıları yöntem kapılarında açık tutulur; eski yorumun üzerine sessizce yazılmaz. | [L5], [T1], [W1]–[W3], [W9]. | #92, #93, #94. |

#### Politikalar ve eski sonuçların okunması

| Politika adı | Korunan anlam ve sürüm ilişkisi | Kaynak |
|---|---|---|
| `legacy_portfoy_v1` | §5.1–§5.13 ve §6'daki eski evren, risk, nakit, masraf, resmi sayım ve kabul davranışı. Eski kimlik, parametre kopyası, kod/veri parmak izi, ham p ve dondurulmuş kabul kararıyla okunur. | [L2], [W8]; eski davranışın sahibi ilgili bölümlerdir. |
| `legacy_tansu_v1` | §5.14'teki eski evren, tam sermaye/kesirli adet, masraf, sağlam bölge ve ileri yürüme yorumu. Destek sonucu olarak kalır; eski resmi m'ye eklenmez. | [L5], [W8]; eski davranışın sahibi §5.14'tür. |
| `bagimsiz_sinyal_s01` | Bu bölümün davranış paketi. Risk, evren, masraf, dönem, dolum, muhasebe ve yöntem sürümleri ayrı referanslardır. Eksik yöntem referansı ilgili işi engeller. Kalıcı kimlik biçimi #97'de onaylanır. | [L1]–[L6], [W8]. |

Eski kayıtta yeni politika alanı yoksa okuyucu özgün komut/şema ve parametrelerden legacy eşlemesini
gerekçesiyle gösterir. Kanıt yetmiyorsa politika bilinmiyor kalır; yeni varsayılan atanmaz. Kimlikler yeniden
hesaplanmaz; düzeltme ve göç, özgün kaydı koruyan yeni olay ve eşleme referansı taşır. Dayanak: [W8], [L2].

#### Dönem, ısınma ve açık işlem sınırları

Aşağıdaki sınır sözleşmesi D §2'nin giriş anındaki ayarları koruma ve ufuk dışındaki çıkışı ayırma
teknik girdisini kullanır (CLAUDE TEKNİK KARARI / YORUM; 19.10 kontrolü). Takvim aralığı kapalıdır;
çalışma günleri bu aralığın borsa seanslarıdır. Görüntünün erken bitmesi istenen bitişi sessizce kısaltmaz. Dayanak: [L3], [W1], [W8].

| Koşu | İstenen başlangıç | İstenen bitiş | Başlangıç / bitiş davranışı | Kaynak |
|---|---|---|---|---|
| 2025 | 2025-01-01 | 2025-12-31 | Bağımsız, açık işlem olmadan başlar; bitişte açık kalanlar ayrı değerlenir. | [L3], [W1]. |
| 2024 | 2024-01-01 | 2024-12-31 | Aynı sınır sözleşmesi. | [L3], [W1]. |
| 2023 | 2023-01-01 | 2023-12-31 | Aynı sınır sözleşmesi. | [L3], [W1]. |
| 2022 | 2022-01-01 | 2022-12-31 | Aynı sınır sözleşmesi. | [L3], [W1]. |
| 2021 | 2021-01-01 | 2021-12-31 | Aynı sınır sözleşmesi. | [L3], [W1]. |
| Birleşik | 2021-01-01 | 2025-12-31 | Tek kronolojik koşu; iç yıl sınırında işlem sıfırlanmaz. | [L3], [W1]. |

- Isınma aralıktan önceki veriyi kullanabilir; veri referansı bu ek kapsamı da taşır. Isınma sinyalleri işlem ve performans sayımına girmez. Seçilen göstergenin tam geçmiş ve yakınsama gereksinimi çözülmüş stratejide yazılıdır; eksikse sinyal yok ve neden kayıtlıdır. Eski §5.1 süreleri yeni varyanta gizli varsayılan olmaz. Dayanak: [W1], [W8], A Q9/Q14, B Q53.
- İlk puanlanan kapanış ancak ısınma tamam ve üyelik geçerliyse aday üretir. Önceki yılın kapanış sinyali bağımsız yılın girişini açmaz. Son kapanışta üretilen adayın ertesi seansı ufuk dışındaysa dolum yoktur; aday ve neden korunur. Dayanak: [L3], [W4].
- Ayrı yılın sonunda açık işlem kapalı işlem istatistiğine girmez. Gerçekleşmiş kısmi sonuçlar korunur; `acik_son`, kalan adedin son geçerli değerini ve tarihini taşır. Sonraki yılın fiyatı geriye dönük gerçekleşmiş kâr yaratmaz. Durdurma/kapanmada idari son fiyat sonucu ayrıca gösterilir. Dayanak: [L3], [W1], [W4]; D §2'nin sansürlü sonuç ayrımı.
- Birleşik koşuda yıl sonu yalnız rapor kesitidir; işlem, girişteki ayar ve ilk risk sürümüyle sürer. Ara yılın kısmi gerçekleşmeleri, kalan adedin gerçekleşmemiş değeri ve sonraki gerçek çıkışlar ayrı olaylardır. Nihai bitişte açık işlem aynı `acik_son` kuralını kullanır. Dayanak: [L3], [W1]; A Q8, D §2.
- Sıfır, sonsuz veya eksik fiyat işlem fiyatı olmaz. Bozuk satır, doğrulanmış durdurmayla eş tutulmaz; kalite hatası ve etkilenen iş kaydedilir. Karantinada yeni giriş yoktur; çıkış talebi ile son temiz fiyat değerlemesi ayrı tutulur. Eski §5.1'in son temiz AOF'ta kapanışı yeni yolda gözlenmiş dolum diye yazılmaz. Dayanak: [L3], [T4], [W4], A Q14, B Q53.
- Eğitim/test sınırında yalnız seçim tarihinde sonucu bilinen eğitim işlemleri seçime girer. Testte açık kalan işlem giriş ayarlarıyla sürer; sonraki pencere ayarı onu değiştirmez. Eğitim ısınması OOS başarı sayılmaz; aynı test sinyali bir kez sayılır. Dayanak: [W1], [W4]; A Q8/Q9, D §2.

#### S08 risk ve maliyet hesabı

E3 hesabının sahibi `tansu/islem_riski.py` olur. `bagimsiz_risk_v1` her işlem için
`risk_butcesi = nominal_tutar × 0,02` üretir. Nominal tutar varsayımsal girdidir; gerçek emir tutarı değildir.
Önceki işlem sonucu bu girdiyi değiştirmez. Ortak nakit, slot ve portföy tavanı bu hesapta bulunmaz.
Dayanak: Levent 18.10, "Yüzde iki uygun" ve "Ortak para falan yok. Her işlem ayrı gibi düşün."
Bu hesap dosyası §5.8 gereği `kayit.KOD_DOSYALARI` kapsamındadır; saklanmış eski kimlikler yeniden hesaplanmaz.

`boyutla` giriş, ilk stop, nominal tutar, aile ve risk sürümünü alır. Çıktısı risk bütçesi,
adet, planlanan risk, kullanılmayan bütçe, ilk risk birimi ve gerekçedir. Stop/giriş sonlu ve pozitif değilse veya
stop girişe eşit/büyükse adet boş, gerekçe `gecersiz_risk_girdisi` olur. Nominal tutar da sonlu ve
pozitif olmalıdır. Çift rotasyonunda adet, planlanan risk ve R boş, gerekçe `risk_dayanagi_eksik` olur;
sayısal risk temeli ve boyutlama #128'e taşınmıştır. Çift için hayali stop üretilmez.

Dağıtıcı kararı (19.10, 02:10): planlanan alış ve stop komisyonu ile BSMV %2 bütçenin içindedir.
Tek hissede `birim_risk = (giriş − ilk_stop) + c × (giriş + ilk_stop)`;
`adet = taban(risk_butcesi / birim_risk)` tam adettir. `c`, maliyet hesabının aynı adlandırılmış sabitidir.
Boyutlamanın ondalık girdileri metin karşılıklarından hesaplanır; yukarı yuvarlanmaz.
Planlanan risk = adet × birim_risk; kullanılmayan bütçe = risk bütçesi − planlanan risk.
Planlanan giriş ve stop masrafları ayrı alanlarda döner. Bir adet bile bütçeyi aşıyorsa adet 0,
planlanan risk 0, kullanılmayan bütçe bütçenin tamamı ve gerekçe `butce_yetersiz` olur.
Bu durumda R boştur. Geçerli ve bütçeye sığan tek hissede gerekçe boştur.
Sıfır/sonlu olmayan ara risk hesabında boyutlama yapılmaz; gerekçe `gecersiz_risk_girdisi` olur.

Bir R, ilk planlanan toplam risktir (`ilk_risk = planlanan_risk`, TL).
Gerçekleşen brüt kayıp R = gerçekleşen brüt kayıp / ilk risk; net R = gerçekleşen net sonuç / ilk risk.
İlk risk, gerçekleşen çıkış fiyatıyla yeniden hesaplanmaz. Gerçekleşmiş miktarlar planlanandan farklıysa
iki miktar ayrı alanlarda kalır; R paydası ilk planlanan risktir. Kısmi sonuçlar aynı paydayı kullanır.
Örnek: giriş 100, ilk stop 90, nominal 100.000 TL. Birim risk 10,29925 TL;
adet 194, planlanan risk 1.998,0545 TL, kullanılmayan bütçe 1,9455 TL olur.
Planlanan alış masrafı 30,555 TL, stop masrafı 27,4995 TL'dir. 195 adet bütçeyi aşar.
194 adet 80 TL'den satılırsa brüt kayıp 3.880 TL, gerçek masraf 54,999 TL,
net sonuç −3.934,999 TL olur; kayıp planlanan riskte kesilmez.

`maliyet_hesapla`, kimlikli gerçekleşen alış/satış dolumlarını alır. `komisyon_bsmv_v1` tek
adlandırılmış bileşik oran kullanır: yön başına %0,15 komisyon ve komisyonun %5'i BSMV.
Levent, 20.10.2026: bu komisyon ve BSMV varsayımını “Bu varsayımı onaylıyorum” yanıtıyla onayladı. Aynı kimlikli aynı dolum
bir kez sayılır; farklı içerikli tekrar hata verir. Sonlu ve pozitif fiyat/adet gerekir.
Satış toplamı alınan adedi aşamaz; satıştan önce alış gerekir. Alışlar aynı işleme aittir.
Gerçekleşen maliyet bütün alış masrafları ile gerçekleşmiş satış masraflarının toplamıdır.
Gerçekleşen net sonuç, satılan miktarın ağırlıklı alış tutarını ve ona düşen alış masrafını içerir;
kalan miktar ve kalan alış masrafı ayrıca döner. Böylece kısmi net sonuç nihai sonuca tekrar eklenmez.
Gerçekleşen brüt kayıp, net sonuç, net fiyat getirisi ve nominal temele göre getiri ayrı alanlardır.
Nihai `net_fiyat_getirisi`, `referans_getirisi` ve `net_r` yalnız giriş dolumu olan,
kalan adedi sıfır işlemde hesaplanır (#82). Açıkken bu alanlar boştur; `bos_nedenleri`
aynı alanlar için `islem_acik` taşır. Giriş dolumu yoksa neden `giris_dolumu_yok` olur.
Kapalı işlemde payda yoksa ilgili alanın nedeni risk hesabının gerekçesidir.
`net_sonuc` gerçekleşmiş miktarın net TL sonucudur; açıkken nihai getiri anlamına gelmez.
`gerceklesen_kismi_sonuclar`, kalan adedi pozitif bırakan her satışın kimlik, adet ve net TL
sonucunu, referans getirisini ve net R'sini ayrı tutar. Bu liste kapanınca da korunur;
nihai sonuca yeniden eklenmez. Kısmi R de ilk planlanan riski kullanır; dayanak yoksa gerekçeli boştur.
Stop ötesindeki kayıp kesilmez.
Elle örnek: 100 adet 100 TL'den alınır, 80 TL'den satılır. Alış masrafı 15,75 TL,
satış masrafı 12,60 TL, net sonuç −2.028,35 TL olur. Net fiyat getirisi
7.987,40 / 10.015,75 − 1 = −0,202516037241345'tir.
Yeni kayma katsayısı seçilmez; bu yüz gerçekleşmiş fiyatlara ek kayma uygulamaz.

`simulator.risk_tablosu` yeni işlem girdilerini bağımsız değerlendirir; nakit/slot nedeniyle satır atmaz.
Bu tablo her bağımsız tek hisse sinyaline kendi sayısal miktarını verir; ortak nakit/slot süzgeci yoktur.
İşlem geçişi veya yeni sınama eğrisi üretmez (#90). Kimlikler ve giriş sütunları korunur.
`dolumlar` alanının bulunmaması, `None` veya NaN olması dolum bilgisi yok demektir;
maliyet hesabı yapılmaz. Açıkça verilen boş liste ise sıfır dolum hesabıdır. Eksik olmayan
bozuk dolum girdisi hata verir. Böylece dolumlu ve dolumsuz adaylar aynı tabloda kalabilir.
`tansusinama._getirili` açık `risk_surumu` taşıyan girdide bu tabloyu kullanır; eski girdide eski sonuç döner.
Günlük `_kart` açık risk isteğinde aynı E3 sonucunu gerekçeli sözlük olarak verir; eski kart listesi korunur.
Bu hesap yüzü günlük etkinleştirme değildir (#95). Normal komutlar eski politikalarını korur.
Hesap tarih veya gelecek fiyat okumaz; yalnız verilen giriş/ilk stop ve gerçekleşmiş dolumları kullanır.
İlk/son gün ve karantina uygunluğu çağıranın yürütme sözleşmesindedir; bu hesap dolum icat etmez.

#### S09 tek hisse işlem geçişi (#90)

**Durum: tek hisse işlem yüzü uygulandı.** Normal komutların ve günlük etkinleştirmenin bağlantısı bu teslim değildir.
Levent, 20.10.2026: tek hisseyle ilerlenir; çiftin yeni risk/boyut hesabı #128 çözülene kadar
kapalı kalır. Eski çift ve portföy hesapları korunur. Bu teslim günlük etkinleştirme,
strateji seçimi, performans sınaması veya emir izni vermez.

Levent, 20.10.2026: yarı satışta adet aşağı tam sayıya yuvarlanır, kalan adet korunur.
15 adedin 7'si satılır, 8'i kalır. Yalnız 1 adet varsa yarı satış dolumu oluşmaz;
yarı satış adımı işlenmiş sayılır ve tam çıkış beklenir. Bu, Tansu kaynak alıntısı değil,
tam adet uygulaması için Levent'in kararıdır. Eski kesirli hesaplar bu kararla değiştirilmez.

Geçişin sahibi mevcut `tansu/motor.py` olur. `islem_adimi(durum, mum, sinyal=None,
*, yurutme, ayar, kutu_alt=None, hedef=None)` tek gün ilerler. `tara(..., *, yurutme=None,
onceki_durum=None)` açık yürütme isteğinde aynı geçişi her satır için çağırır ve sürümlü
sözlük döndürür. Yürütme isteği verilmezse eski dört öğeli sonuç ve eski politika sürer.
Bu hesap dosya yazmaz, veri indirmez ve eski `Zincir` önbelleğini yeni hesap için kullanmaz.
Yeni yüz, gün başına çözülmüş tek kurulum ister; kurulum tarihinin tekrarı aynı içerikte olsa da
hatadır. Eski çok dönemli kurulumu ilk satırdan seçme davranışı eski yolda korunur. `stop=kutu`
için kutu altı, `hedef=tansu` için hedef gerekli alanlardır; eksikse aday `kurulum_eksik`
gerekçesiyle doluma geçmez. Yeni yolda eksik kutu yerine ATR stopu veya seçilmiş hedefin
sessizce atlanması yoktur; uygulanmayan alanın boşluğu bu ret değildir.

Yürütme isteği `bagimsiz_islem_v1`, mevcut `ema_sikismasi` ailesi, strateji kimliği/sürümü,
deneme/koşu/görüntü/sembol kimlikleri, açık pozitif nominal tutar, S08 risk/masraf sürümleri
ve `aof_v1` fiyat politikasını taşır. Alan adları `surum`, `aile`, `strateji_id`,
`strateji_surumu`, `deneme_id`, `kosu_id`, `veri_ref_id`, `sembol`, `nominal_tutar`,
`risk_surumu`, `masraf_surumu`, `fiyat_politikasi` olur. `tara` sinyalleri tarih → boş olmayan
`sinyal_id` eşlemesidir; tek adım aynı kimliği veya `None` alır. Varsayılan nominal tutar yoktur. Çift isteği
`risk_dayanagi_eksik` nedeniyle yeni dolum üretmez. Bu yüz mevcut katalog izinlerini açmaz.

Durum JSON ile saklanıp geri okunabilir: şema ve politika sürümü, kimlik bağları, son işlenen
gün ve girdi izi, açık/bekleyen işlem, girişte dondurulmuş ayar/ilk risk, kimlikli model
dolumlar, kapanan işlemler ve gerekçeli olay izi bulunur. Durum sürümü `islem_durumu_v1` olur.
`islem_id` yürütme, sinyal günü/kimliği ve giriş ayarlarına bağlıdır; `ayar_parmak_izi`
giriş ayarını tanımlar. Bu bağlar ve dolum kimlikleri işlemde korunur. Sürüm veya kimlik bağı uyuşmazsa
hata verilir. Aynı gün aynı girdi tekrarında dolum eklenmez; farklı içerikli tekrar ve geriye
giden tarih hata verir. Açık işlemde yeni ayar giriş ayarını değiştirmez; değişiklik gerekçesi
kaydedilir. Aynı strateji/sembolde açık yaşam döngüsüne ek sinyal adet eklemez; ret izi bırakır.
Başka sembolün işlemi ortak nakit, slot veya portföy sınırı nedeniyle bu hesabı engellemez.

Gün girdisi düzeltilmiş işlem fiyatları/göstergeler yanında ham yüksek/düşük,
üst/alt limit ve limit kanıtını taşır. Eski kapanışa yakınlık bayrağı tam gün kilit kanıtı
olarak kullanılmaz. Kanıt yoksa limit bilinmiyor kalır; o satırda kesin dolum üretilmez.
Bilinen limitte tam gün kilit denetimi önceki dolum sözleşmesindeki ham eşitlikle yapılır.
Kapanış sinyali aynı güne doldurulmaz. Giriş sonraki seansın AOF modelini kullanır;
giriş gününde tavan kilidi sinyali düşürür. Stopun önceliği ve aynı gün fiyat sırası eski
motorun açık modeliyle korunur: stop dolumu `min(stop, AOF)` olur. Stopun önceliği
dışında önceden bekleyen tam çıkış ilk uygun kilitsiz günde AOF olur. Her satış engeli olay izinde sayılır. Günlük çubuk gerçek
emir kuyruğunu veya gün içi fiyat sırasını kanıtlamaz. Her kapanış kararı yalnız kendi
girdilerini ister. Eksik RSI, geçerli SMA250 çıkışını veya RSI kullanmayan dip kuralını
engellemez; gerekli girdi eksikse ilgili yeni karar verilmez. Daha önce bekleyen satış ve
geçerli fiyatla belirlenen stop/hedef adımı
bu nedenle engellenmez. `adim` ve `_gun` içindeki `karar=True` varsayılanı eski davranışı
korur. Yeni geçiş, girdisi bilinen kararların ad kümesini verir; eksik göstergenin etkilediği
karar kümede bulunmaz ve nedeni kaydedilir. Boş küme fiyatla belirlenen adımları engellemez.

Karantina ve sonlu/pozitif olmayan fiyat dolum üretemez. Açık işlemde karantina çıkış isteği
oluşturur; son temiz değerleme gerçek satış gibi yazılmaz. Bekleyen çıkış ilk uygun
kilitsiz satırda işlenir. Son temiz değerleme fiyatı ve tarihi ayrı tutulur. Dönemin ilk
satırı öncesinde giriş uydurulmaz; son gün sinyali bekleyen kalır. Veri sonunda kalan adet
`acik_son` olarak korunur; yapay son gün satışı ve açık işlem için nihai getiri/R üretilmez.
Gerçekleşen kısmi sonuç, kalan miktar ve değerleme ayrı alanlardadır. Risk, adet ve masrafın
tek sahibi S08 hesabıdır; ilk risk yükselen stop veya sonraki ayarla yeniden boyutlanmaz.

Bu yüzün sınırları: toplu/günlük JSON geri okuma eşitliği, aynı gün tekrarları, ayar bağları,
örtüşme, tek/çift engeli, yarı satışın tam adedi, kilit/kanıt yokluğu, karantina, dönem sonu
ve gelecek satır değişmezliği. Mevcut 250 satırlık karantina giriş koruması yeni durumun
`karantina_kalan` alanında korunur. `tests/test_motor.py` davranışı, `tests/test_gelecek.py`
yeni geçişin önceki günlere gelecek bilgi taşımamasını sınar. Çıktıdaki
`dusen_sinyal_sayisi` ve `ertelenen_satis_gunu_sayisi` gerekçeli olaylardan türetilir;
aynı satış engeli gününe ait birden çok açıklama günü iki kez saydırmaz. Tarihli `iz`,
`egri_turu=tani_referans`, açık nominal temel, gerçekleşmiş net sonuç, kalan adet ve ayrı
değerlemeyi taşır. Bu tanısal toplam ortak hesap özkaynağı veya bileşik portföy getirisi değildir.

#### Dolum, risk ve ölçünün anlamı

- Claude'un kayıtlı **seçenek 2** kararı geçerlidir (18.10; yanıt Q74): ham `yüksek = düşük = tavan` gününde alış dolmaz, giriş sinyali düşer; ham `yüksek = düşük = taban` gününde satış bekler, ilk uygun kilitsiz günde yeniden işlenir. Sonraki fiyat kullanılır; her engel sayılır. B Q49'un açılış eşitliği ekleme önerisi bu kararı değiştirmez. Günlük çubuk gerçek emir kuyruğunu kanıtlamaz. Dayanak: [L5], [T4], [W4], [W5]; `tavan-taban/bulgular.md`, yanıt Q74.
- Limit ve adım ham fiyat ölçeğindedir. 2021–2025 için olağan Yıldız/Ana paylarında ±%10, adımda 06.11.2023 değişikliği kullanılır; üst limit aşağı, alt limit yukarı izinli adıma yuvarlanır. Menkul/gün istisnası, baz fiyat veya tarihli kural kanıtı yoksa bayrak bilinmiyor kalır; dolum kesinmiş gibi yazılmaz. Tablo sahibi §5.1'dir. Dayanak: [W5]; `fiyat-limiti/arastirma.md`, B1–B5.
- Kapanıştan üretilen karar o kapanışa geriye dönük doldurulmaz. Mevcut AOF yaklaşımı açık dolum politikası olarak korunur; D §1'in gerçek açılış önerisi İş Yatırım'da açılış varmış gibi uygulanmaz. Gerçek açılış isteyen varyantta alan yoksa ölçülemedi yazılır. Dayanak: [W4]; A Q23, D §1 ve §4'teki veri kaynağı sınırı.
- Komisyon = dolum tutarı × 0,0015; BSMV = komisyon × 0,05. Toplam bu yönde 0,001575 × tutardır. Kısmi çıkış dahil her dolum ayrı hesaplanır; alış ve satış tutarı farklı olabilir. Kayma komisyona gömülmez. Dayanak: [L6]; C giriş, D §1, `mc-wf/arastirma.md` muhasebe sınırı.
- Her işlem aynı varsayımsal referans tutarla normalleştirilir; önceki kâr referansı büyütmez. %2 planlanan risk, gerçekleşen kayba tavan garantisi değildir. İlk risk sonradan yükselen stopla değiştirilmez. Dayanak: [L1], [L2], [T2], [T3], [W6]; D §1.
- Stop mesafesi sıfır/negatif veya stop/giriş sonlu ve pozitif değilse boyutlama yapılmaz; aday gerekçeli hata olarak korunur. Stopu tanımsız çiftte fiyat getirisi gösterilebilir; risk adedi ve R boş, nedeni `risk_dayanagi_eksik` olur. EMA stopu çifte eklenmez. Dayanak: [T3], [W6]; D §1, RISK kapısı.
- Kapalı işlem net fiyat getirisi, varsayımsal referansa göre yüzde sonuç ve net R ayrı ölçülerdir. Net fiyat getirisi bütün çıkış nakitleri eksi çıkış masraflarının alış tutarı ve giriş masrafı toplamına oranı eksi birdir. Kısmi çıkışlar bu nihai hesaba dahildir; ayrı tutulan kısmi sonuçlar nihai sonuca tekrar eklenmez. Net R ve ilk riskin sahibi S08 risk ve maliyet hesabıdır; çiftin sayısal dayanağı #128'dedir. Dayanak: [L1], [T3], [W6]; C Q96, D §1; dağıtıcı kararı 19.10, 02:10.
- Eğri türü `tani_net_r`, `tani_referans` veya eski `legacy_ozkaynak` olarak yazılır. Tanısal toplam hesap bakiyesi değildir; bileşik hesap getirisi, portföy yüzde düşüşü ve iflas olasılığı türetilmez. Kapalı işlem sırası düşüşü günlük değerleme düşüşünden ayrıdır. Dayanak: [L2], [W2], [W6].
- Sharpe ancak günlük getiri serisi ve paydası tanımlıysa hesaplanır; eş dönemli risksiz getiri düşülür. Geçerli seri/faiz kaynağı yoksa, iki gözlemden azsa veya fark getirisi sapması sıfırsa sonuç gerekçeli boştur. İşlem R listesine günlük yıllıklandırma uygulanmaz. Dayanak: [W7]; C Q96/Q97. Repo Net veri ve tarih hizalaması ayrıca kanıtlanır; bugünkü faiz geçmişe taşınmaz.
- Kazanma oranı, işlem sayısı, ortalama/medyan, masraf ve al-tut kıyası sonuçtur; günlük izin değildir. İşlemsiz hücre pozitif bölgeyi kanıtlamaz; başarısız/eksik hücre atılmaz. İlk sonuçlardan önce başarı eşiği ve ileri gözlem süresi icat edilmez. Dayanak: [L4], [T1], [W3]; C Q76, D §5.

#### E1–E6 ve J01–J20 sınırları

**S04 veri uyarlayıcısı (#85):** `veri.veri_hazirla`, kayıtlı görüntüyü `oku` ile doğrular;
isteğin dönemini ve sembol sırasını koruyan düz piyasa kayıtları, kalite sonucu ve veri referansı döndürür.
Kalite hesabı sembol/dönem süzmesinden önce bütün görüntüde yapılır. `veri.cift_girdileri` iki eski çift
yolunun ortak hazırlama sahibidir; çift seçimi çağıranlarda kalır. `legacy_portfoy_v1` mevcut işlem/karantina
maskesini ve son temiz AOF'u korur. `legacy_tansu_v1` buna sonsuz kapanış/AOF karantinasını ve sonlu,
pozitif kapanış/AOF koşulunu ekler (§5.14). İlk geçerli fiyattan önce son fiyat tarihi boştur;
sonraki eksik/karantinalı günlerde yalnız değerleme fiyatı ve tarihi taşınır, işlem bayrağı üretilmez.
İstenen dönemin başı kalite geçmişini sıfırlamaz. Son gün sonrası veri değerlemeye katılmaz.
Üyelik sürümü isteğin referansıdır; aşağıdaki S05 yolu bu referansı tarihli üyeliğe bağlar.
`tests/test_gelecek.py`, ortak çift hazırlığının her iki eski politika için önek değişmezliğini sınar.

**S05 tarihli üyelik (#86):** `veri.UyelikIstegi` değerlendirme tarihlerini, `evren_politikasi`
ve `uyelik_surumu` alanlarını taşır. `veri.uyelik_hazirla` her tarih için sembolleri ve
üyelik aralığı kanıtlarını döndürür. `donemsel_bist30_v1`, depodaki
`tansu/referans/bist30_2021_2025_v1/uyelik.csv` tablosunu kullanır; sürümü
`bist30_2021_2025_v1` olur. Kaynak kaydı aynı klasördeki `kaynaklar.md` dosyasıdır.
Girdi CSV'sinin `bitis` günü hariçtir. Çıktının `yururluk_bitisi` günü dahildir;
dönüşüm bir gün çıkarır. Açık bitişler yalnız doğrulanmış kapsamın sonu olan
2025-12-31'e kadar geçerlidir. Kapsam 2021-01-01–2025-12-31'dir. Dayanak: [L2],
#86'nın doğrulanmış veri girdisi ve aynı klasördeki kaynak kaydı.

İstenen günün 30 ayrı üyesi yoksa koşu durur. Hata bütün eksik tarihleri ve üyelik
sürümünü taşır; yaklaşık veya bugünkü listeye dönüş yoktur. Aynı sembolün çakışan
aralıkları ve boş kaynak kimliği hatadır. `VeriIstegi.evren_politikasi` seçilirse E1
istenen dönemin değerlendirme günlerini doğrular; ısınma günleri üyelik istemez.
Yanıt üyelik kanıtını ve tablo parmak izini veri referansına bağlar. Dayanak: [L2], [W8].

`motor.sinama(..., veri_paketi=...)` E1 yanıtıyla üyelik denetimini seçer. Sinyal
günü ile sonraki giriş günü ayrı denetlenir. Giriş gününde üye olmayan aday
gerçekleşmez; nedeni ve iki tarih sonuç tablosunun `attrs` alanında korunur.
Gerçekleşen girişin satırı üyelik kanıtını taşır. Üyelikten çıkmak açık işlemi
zorunlu kapatmaz. Sonuç `attrs` alanı üyelik sürümünü, politikayı ve E1 veri
referansını taşır. Fiyat, karantina ve çıkış davranışı mevcut motorun kurallarını
korur; bu yol #90'ın yeni risk/dolum motoru değildir. Parametre verilmezse eski
`motor.sinama` ve yaklaşık `evren.evren` seçimleri değişmez. Dayanak: [L2], [W8];
#86 kapsamı ve giriş denetimi kabul ölçütü.

Motorlar sorumluluk sınırıdır; ayrı servis zorunluluğu değildir. E1–E3 düz veri kayıtlarıyla çalışır;
panel, CLI, HTML veya kullanıcı arayüzü durumu hesaplama girdisinin yerine geçmez. Bu görev ayrımı
taslağın E1–E6/J01–J20 tablolarının S01 sözleşmesidir (YORUM). Dayanak: [L1], [W8].

| Motor | Küçük arayüz; sahip olduğu işler | Sınır | Kaynak |
|---|---|---|---|
| E1 Veri | Veri isteği → piyasa satırları, veri referansı, kalite hatası. J01 görüntü, J02 kalite, J03 tarihli üyelik. | Sağlayıcı, takvim, kalite ve üyelik; strateji seçmez. | [L2], [W8]. |
| E2 Kural | Veri referansı + katalog/ayar isteği → tam çözülmüş strateji, göstergeler, kurulum ve sinyal. J04 gösterge, J05 katalog, J06 aile kuralı. | İzin tam bileşime aittir; dolum yapmaz. | [T3], [W8]. |
| E3 İşlem | Sinyal + piyasa satırı + önceki durum + politika → durum, dolum ve işlem. J07 geçiş, J08 risk/masraf, J09 bağımsız simülasyon. | E2'nin ayar/kurulumunu değiştirmez; ortak nakit dağıtmaz. | [L1], [L2], [W4], [W6]. |
| E4 Sınama | Kayıtlı deneme + veri/yöntem referansları → koşu ve sonuç. J10 dönem, J11 ölçü, J12 sağlam bölge, J13 WF, J14 MC, J15 sadakat/yöntem kanıtı. | Hesabı E1–E3'e verir; yazmayı E5'e verir. Açık yöntem kapısını aşmaz. | [L3], [L5], [W1], [W2], [W8]. |
| E5 Kayıt | Olay ekle / kimlikle oku → kayıt makbuzu / değişmez kayıt. J16 revizyonlar, koşular, sonuç ve kanıt bağlantıları. | Yalnız kayıt tutar; E1–E4/E6 hesabını çağırmaz. Hesap başlatma E4/E6'nın işidir. | [T3], [W8]. |
| E6 Günlük | Tarih + seçilmiş deneme + önceki durum → günlük sonuç, kart ve yeni durum. J17 günlük çalışma. | E1–E3 ve E5'i çağırır; hesabı kopyalamaz. UYGUNLUK kapısını ister. | [L4], [W8]. |
| Çıktı bağdaştırıcısı | J18: sonuç/kanıt/kart → HTML, CSV, JSON, durum metni. | Ölçü hesaplamaz, izin vermez. | [L4], [W8]. |
| Kişisel panel bağdaştırıcısı | J19: katalog/ayar/kayıt isteği → görünüm, hata, yeni deneme makbuzu. | Kaydedilmemiş düzenleme çalışmaz; yalnız izinli tam bileşimi ister. | [L1], [W8]. |
| CLI bağdaştırıcısı | J20: argüman + strateji referansı → ortak motor isteği / argüman hatası. | Panelle aynı doğrulama; gizli ayar varsayılanı yoktur. | [W8]; A Q9/Q15. |

#### Ortak kayıt sözleşmesi

Alan grubu aynı satırda virgülle verilmişse tür, birim ve boş kuralı **her alana ayrı** uygulanır.
`metin` UTF-8 dizge; `tarih` ISO takvim tarihi; `zaman` UTC ISO an; `sayi` sonlu sayı; `tam` tamsayı;
`bayrak` doğru/yanlış; `liste<T>` sıralı T kayıtlarıdır. Kimlikler opak metindir; UUID veya kalıcı hash
bayt biçimi burada onaylanmaz. Aşağıdaki şema YORUM'dur. Dayanak: [W8], [L1]; taslak ortak kayıtlar tablosu.

| Ortak alan / alt kayıt | Tür ve birim | Boş değer kuralı | Sürüm ve kaynak bağı | Dayanak |
|---|---|---|---|---|
| `kayit_id`, `kayit_turu`, `sema_surumu` | metin; kimlik/tür/sürüm etiketi, birimsiz | Zorunlu, boş olamaz. | Her kaydın kendi şeması; bilinmeyen sürüm sessizce dönüştürülmez. | [W8]. |
| `olusturma_zamani`, `kaynaklar` | zaman; liste<kaynak>, birimsiz | Zorunlu; kaynak listesi boş olamaz. | Kayıt üretim anı, piyasa tarihinden ayrıdır. | [W8], [T3]. |
| `kaynak`: `tur`, `konum`, `tarih`, `alinti`, `karar_durumu` | metin, metin, tarih, metin?, metin; birimsiz | İlk üç ve durum zorunlu; alıntı yoksa gerekçeli boş. | Konum Ham path:line veya URL'dir; karar kaynağıyla veri kaynağı ayırt edilir. | [L5], [W8]. |
| `deger`: `deger`, `birim`, `bos_nedeni` | sayi?, metin, metin? | Değer boşsa neden zorunlu; doluysa neden boş. | Yüzde depoda kesir, ekranda ×100; R, TL, adet ve gün birbirine çevrilmez. | [L1], [W6], [W8]. |
| `baglar`: `deneme_id`, `kosu_id`, `ayar_parmak_izi`, `politika_surumu`, `veri_ref_id` | metin; birimsiz | Hesap çıktısında zorunlu. Deneme henüz koşulmadıysa koşu bağı gerekçeli boş; ham piyasa satırında deneme/koşu bağı aranmaz. | Referansın kendi şeması ve içerik kimliği korunur; tam çözülmüş ayarla eşleşir. | [W8]. |
| `donem`: `baslangic`, `bitis`, `isinma_baslangici`, `sinir_surumu` | tarih, tarih, tarih?, metin; gün | İlk/son/sürüm zorunlu; ısınma gerekmiyorsa gerekçeli boş. | İstenen aralık ve fiili kapsam ayrı taşınır. | [L3], [W1], [W8]. |
| `parametre`: `ad`, `deger`, `tur`, `birim`, `kaynaklar` | metin; metin/sayi/tam/bayrak/liste; metin; metin; liste<kaynak> | Zorunlu; çözülmemiş değer hesaplanabilir strateji oluşturmaz. | Sabit ve seçilmiş değer dahil; her değerin kaynağı ve kökeni kayıtlıdır. | [T3], [W8]. |
| `olay`: `olay_id`, `tarih`, `tur`, `adet`, `fiyat`, `komisyon`, `bsmv`, `kayma`, `kaynaklar` | metin, tarih, metin, deger(adet), deger(TL/adet), deger(TL), deger(TL), deger(TL), liste<kaynak> | Kimlik/tarih/tür/kaynak zorunlu. Dolumda adet/fiyat/komisyon/BSMV dolu; kayma bilinmiyorsa gerekçeli boş. Değerleme olayı dolum gibi adet/fiyat türetmez. | Olay türü model dolumu, gözlenmiş dolum, değerleme, idari sonlandırmayı ayırır; masraf sürümü üst kayıttadır. | [L3], [L6], [T4], [W4]. |
| `olcu`: `ad`, `deger`, `yontem_ref`, `seri_ref` | metin, deger, metin, metin? | Ad/yöntem zorunlu; seri gerektiren ölçüde seri yoksa değer gerekçeli boş. | Birim, payda ve muhasebe yönteme bağlıdır. | [W6], [W7], [W8]. |

| Kayıt | Alanlar: tür / birim | Boş değer ve sürüm ilişkisi | Dayanak |
|---|---|---|---|
| Piyasa satırı | Ortak kimlik/kaynak; `sembol`: metin; `tarih`: tarih; `ham_acilis`, `ham_yuksek`, `ham_dusuk`, `ham_kapanis`, `ham_aof`, `duzeltilmis_acilis`, `duzeltilmis_yuksek`, `duzeltilmis_dusuk`, `duzeltilmis_kapanis`, `duzeltilmis_aof`: deger(TL/adet); `hacim_tl`: deger(TL/seans); `olay_ref`: metin?; `kalite_bayraklari`: liste<metin>; `son_gecerli_fiyat_tarihi`: tarih?. | Sembol/tarih/kalite listesi zorunlu. Fiyatlar ve hacim bulunamıyorsa gerekçeli boş; açılış AOF veya önceki kapanışla doldurulmaz. Şirket olayı yoksa olay bağı gerekçeli boş. Son geçerli fiyat henüz yoksa tarih gerekçeli boş. Görüntü, düzeltme ve kalite sürümüne bağlıdır. | [L3], [T4], [W4], [W8]. |
| Üyelik aralığı | Ortak kimlik/kaynak; `sembol`, `endeks`, `uyelik_surumu`: metin; `yururluk_baslangici`, `yururluk_bitisi`: tarih; `duyuru_zamani`: zaman?. | Üyelik bitişi dahil aralık; alanlar zorunlu, henüz kanıtlanmayan aralık üyelik sayılmaz. Duyuru anı bilinmiyorsa gerekçeli boş. Aynı sürümde çelişen aralık çözülmeden koşulmaz. | [L2], [W8]. |
| Veri referansı | Ortak kimlik/kaynak; `goruntu_id`, `manifest_parmak_izi`, `uyelik_surumu`, `kalite_surumu`, `duzeltme_surumu`, `takvim_ref`: metin; `istenen_donem`, `fiili_donem`: donem; `isinma_donemi`: donem?. | Kimlikler ve dönemler zorunlu; ısınma gerekmiyorsa gerekçeli boş. Fiili aralık eksikse istenen aralık değiştirilmez; hata/uyarıyla sonuç kapsamı açıklanır. | [L2], [L3], [W8]. |
| Tam çözülmüş strateji | Ortak kimlik/kaynak; `aile`, `varyant`, `katalog_surumu`, `bilesim_id`, `izin_durumu`: metin; `parametreler`, `gosterge_ayarlari`: liste<parametre>; `dolum_surumu`, `risk_surumu`, `masraf_surumu`, `muhasebe_surumu`, `donem_surumu`: metin; `ayar_parmak_izi`: metin. | Hepsi zorunlu; gizli varsayılan yok. İzin, tüm bileşimin kanıtına bağlıdır. Eski 24 varyantın varlığı yeni panel izni değildir; belirsiz bileşim izinsiz kalır. | [L5], [T3], [W8]; A Q15. |
| Deneme revizyonu | Ortak kimlik/kaynak; `deneme_id`, `olusturan`, `neden`, `kimlik_bicimi_surumu`: metin; `ust_deneme_id`, `eski_kural_id`: metin?; `strateji`: tam çözülmüş strateji; `donemler`: liste<donem>; `veri_referanslari`, `yontem_referanslari`: liste<metin>. | Kök denemede üst bağ, yeni kayıtta eski bağ gerekçeli boş. Dönem/veri listeleri boş olamaz. Yöntem gerekmiyorsa yöntem listesi boş olabilir; gerekli yöntem eksikse koşu başlayamaz. | [L4], [W8]. |
| Koşu | Ortak kimlik/kaynak/bağlar; `kip`, `kod_parmak_izi`, `kaynak_rev`, `bagimlilik_parmak_izi`, `durum`: metin; `ortam`: liste<parametre>; `baslangic_zamani`: zaman; `bitis_zamani`: zaman?; `isler`, `biten_isler`, `hatali_isler`: liste<metin>; `tohum`: tam?; `ureteci_surumu`: metin?. | Başlangıç zorunlu; yarıda kalanın bitişi gerekçeli boş. Rastgele yöntem yoksa tohum/üreteç gerekçeli boş; varsa zorunlu. Bütün işler kimlikle muhasebeleştirilir. | [W2], [W8]. |
| Sinyal | Ortak kimlik/kaynak/bağlar; `semboller`: liste<metin>; `tarih`: tarih; `yon`, `aday_durumu`: metin; `kutu_alt`, `kutu_ust`, `hedef`, `ilk_stop`: deger(TL/adet); `kurulum_girdileri`: liste<parametre>; `kural_kaniti`: liste<kaynak>. | Semboller boş olamaz; tarih/yön/durum/kanıt zorunlu. Kurulum alanı varyantta uygulanmıyorsa gerekçeli boş; gerekliyken eksikse doluma geçmez. Ayar parmak izi E2/E3 boyunca aynıdır. | [T3], [W4], [W8]. |
| İşlem | Ortak kimlik/kaynak/bağlar; `sinyal_id`: metin; `giris_olaylari`, `cikis_olaylari`, `degerleme_olaylari`: liste<olay>; `referans_tutar`: deger(TL); `ilk_risk`: deger(TL); `adet`, `kalan_adet`: deger(adet); `gerceklesen_kismi_sonuclar`: liste<olcu>; `net_fiyat_getirisi`, `referans_getirisi`: deger(kesir); `net_r`: deger(R); `durum`: metin; `cikis_nedeni`: metin?. | Girişsiz aday işlem değildir. Kalan adet dolumlardan izlenir; pozitifken işlem açıktır, yalnız sıfır olduğunda kapalıdır. Açık işlemde çıkış listesi kısmi dolum içerebilir; hiç çıkış dolumu yoksa boştur. Kısmi çıkışlar tek işlem kimliğinde olay olarak kalır. Gerçekleşmiş kısmi sonuçlar ayrı listede tutulur; kısmi çıkış yoksa bu liste boştur. Nihai `net_fiyat_getirisi`, `referans_getirisi`, `net_r` ve `cikis_nedeni` işlem kapanana kadar gerekçeli boştur; kalan adedin değerlemesi ayrı durur. İlk risk yoksa R ve risk adedi gerekçeli boş. Kısmi net R de RISK kapısı kapanmadan üretilmez. | [L1], [L3], [L6], [T3], [W4], [W6]. |
| Eğri | Ortak kimlik/kaynak/bağlar; `tur`, `muhasebe_surumu`: metin; `normalizasyon`: deger; `islem_referanslari`: liste<metin>; `satirlar`: liste<eğri satırı>. Eğri satırı: `tarih`: tarih, `deger`: deger, `degerleme_turu`: metin. | Tür/muhasebe zorunlu. R toplamında normalizasyon değeri 1 R'dir; referans eğrisinde varsayımsal TL, legacy eğride eski hesap dayanağıdır. Eksik gözlem gerekçeli boş; sıfır getiri diye tamamlanmaz. | [L2], [W2], [W6]. |
| Sonuç | Ortak kimlik/kaynak/bağlar; `donem`: donem; `veri_referanslari`, `islem_referanslari`, `egri_referanslari`, `alt_sonuc_referanslari`, `yontem_referanslari`: liste<metin>; `olculer`: liste<olcu>; `uyarilar`: liste<metin>; `eserler`: liste<eser>; `gunluk_uygunluk`: metin. Eser: `konum`, `parmak_izi`, `bicim_surumu`: metin. | İşlem yoksa işlem listesi boş olabilir; ölçüler gerekçeli boş kalabilir. Veri/yöntem kanıtı eksik sonuç tam sayılmaz. Günlük uygunluk ayrı karardır, sonuç kârlılığından türemez. | [L4], [W8]. |
| Hata | Ortak kimlik/kaynak; `is_id`, `asama`, `neden`, `kod`, `etki`: metin; `etkilenen_kayitlar`: liste<metin>; `deneme_id`, `kosu_id`: metin?. | Temel alanlar zorunlu; kimlik henüz üretilmediyse gerekçeli boş. Üst koşuya kaybolmadan döner; atlanan iş başarılı sayılmaz. | [W8]. |

Her `?` alanın boşluğuna aynı alan adını kullanan `bos_nedenleri` metin eşlemesi eşlik eder; `deger`
kaydı kendi nedenini taşır. Gerekçesiz null, NaN ve sonsuz değer geçerli serileştirme değildir. Tür/birim,
şema veya referans uyuşmazlığı hata kaydı üretir. Bunlar arayüz gerekleridir; yazılım kabul kapılarının
zorunluluğu hakkında SAHİP-111 kararı verilmiş sayılmaz. Dayanak: [W8]; C Q111.

E5 önce revizyon makbuzunu verir; E4/E6 bu referansla çalışır. Değişmeyen ayarın tekrar çalışması yeni
koşudur; kaydetme olayı yeni revizyondur. Izgara hücresi alt denemedir; MC senaryosu koşunun alt kaydıdır.
Holm için resmi sınıf ve hipotez ailesi ayrıca yazılır; senaryo veya revizyon adedi m diye sunulmaz.
Dayanak: [W8], [L4]; taslak kayıt tablosu, C Q87 ve eski resmi sayım §5.11.

#### Ortak EMA kurulumu (S06, #87)

`aileler.ortak_kurulum(veri_paketi, tarih, strateji)` E1 piyasa kayıtlarını ve katalogdan
çözülmüş EMA stratejisini alır. Değerlendirme tarihi dahil geçmişi kullanır. Çıktı,
o günün tarihli ve birimli gösterge kayıtlarını, sinyallerini ve ayrı ısınma bilgisini taşır.
Gösterge değeri eksikse nedeni kaydedilir. Eski gösterge fonksiyonları hesap sahibi kalır.
Günlük ve geçmiş sınama, `aileler.kurulum` tablosunu bir kez hesaplar. Sinyal tarihleri ve
sonraki aşamanın kutu/hedef girdileri aynı tablodan alınır. Eski `sinyal` ve
`motor.kurulum_bilgisi` çağrıları korunur. Dayanak: #87 arayüz brifi.

İlk ve son değerlendirme günü dahildir. Isınma satırları sinyal günü sayılmaz.
Eksik kapanış kurulum geçmişinden çıkarılır; gösterge takviminde boş gün korunur (§5.1).
Karantina ve kilit bayrakları hesapta fiyatı değiştirmez; giriş kapısı §5.3'te kalır.
Sıfır veya sonsuz fiyat sessizce düzeltilmez; E1 kalite bilgisi korunur. Sonlu olmayan
gösterge değeri gerekçeli boş kaydedilir. Isınma tamamlanmadan sinyal üretilmez.
Sonraki satırlar önceki günün göstergesini ve kurulumunu değiştirmez; `tests/test_gelecek.py`
bu sınırı kapsar. Dayanak: #87 kabul ölçütleri, §5.1, §5.3 ve §5.12.

Sinyal kaydı strateji kimliğini, ayar parmak izini, kaynakları, kutuyu, hedefi ve stop
girdilerini taşır. ATR stopunun dolum fiyatı henüz bilinmediği için ilk stop gerekçeli
boştur. Kutu stopu kutu altını taşır. `hedef=yok` için hedef uygulanmaz; `hedef=tansu`
için bulunamayan hedef `hedef_bulunamadi` nedeniyle boştur. Bu, eski §3 Modül 1
kurulumunun hedef yokluğu davranışını değiştirmez ve varsayılan hedef üretmez.
Çift ailesi ayrı kuralını korur; EMA katalog kaydıyla çift hesabı yapılmaz.
Dayanak: #87 sözleşme sınırı ve `aile-kurallari.md` §3 Modül 1.

Çift uyarlayıcısı `ciftbolme.strateji_coz(y, x, p)` mevcut `cift` ve `ciftbolme` ayarlarını
tam kayda çözer. `katalog_surumu` boştur; gerekçesi
"s02_v1 yalnız ema_sikisma içerir; çift ailesi katalogda yok" metnidir.
Kaynaklar mevcut kod ve bu belgenin çift kurallarıdır. Yeni katalog üyeliği veya
strateji seçme izni üretilmez. `ciftbolme.ortak_kurulum(veri_paketi, tarih, strateji)`
aynı gösterge/sinyal/ısınma çıktı gruplarını kullanır. Çift hedefi geçilecek bacaktır;
EMA kutusu veya fiyat hedefi bu kurala uygulanmaz ve gerekçeli boş kalır.
`cift.hesapla` tarihli Z, ΔZ ve hedef bacak tablosunun ortak hesabıdır; eski
`ciftbolme.hedef` uyarlayıcısı aynı tabloyu kullanır. Isınmanın tamamlanması için
son ΔZ tanımlı olmalıdır; yalnız satır sayısının dolması yeterli değildir.
Gelecek satırı denetimi iki aileyi ayrı çağrılarla kapsar. Dayanak: #87 yazımında
çağıranın verdiği çift çözümleme girdisi; mevcut çift kuralları §5.6.

#### Ayar aktarımı (S07, #88)

`PilotKayit.deneme_kaydet` tam çözülmüş hücre stratejisini de kabul eder. Katalog çözümleyicisinin
eski ızgara sayısal girdileri `legacy_izgara` kökenini taşır; katalog seçimini açmaz.
Kayıt özeti §5.15 pilotunun tam çözülmüş yapılandırma özetidir. Her açık kaydetme yeni revizyondur;
aynı denemenin tekrar çalıştırılması kimliğini korur. Eski kayıtların özetleri yeniden üretilmez.

`tansu-sinama` ve `gunluk` komutlarında `--deneme-id` isteğe bağlıdır. Verildiğinde
`--deneme-dosyasi` açık pilot yoludur; ayar yalnız bu kayıttan okunur. Kayıt, tam alanları,
katalog/ızgara çözümünü ve içerik özetini doğrulamadan hesap başlamaz. Eksik ayar, gerekli
kurulum veya sınırdaki özet farkı ilgili kayıt kimliğini veren hatayla durur. Kimlik verilmezse
eski varyant davranışı korunur; otomatik kök deneme kaydedilmez.
Kayıttaki strateji nesnesi, parametre listesi ve her parametre öğesi üye erişiminden önce
doğrulanır. Veri/yöntem/risk/masraf nesneleri, dönem listesi ve veri referansları yapısal
olarak geçersizse özetleri eşleşse de kayıt reddedilir.
Kayıtlı EMA denemesi yalnız `--aile ema_sikismasi` ile çalışır. Çift ailesi veya iki aile
birlikte istenirse hesap ve çocuk kayıt başlamadan deneme kimliğiyle hata verilir.
Çiftin ayrı kurulum sözleşmesi yukarıdadır; EMA ayarı çift hesabına uygulanmaz.

Kayıtlı EMA ızgarasının her hücresi hesap başlamadan üst denemeye bağlı çocuk olarak kaydedilir.
E2 sinyal ve kurulumunu çocuğun kaydedilmiş ayarından üretir; E3 aynı ayarı kullanır.
Her çocuk ayrı işlem önbelleği kullanır. Verilen mum tablosunun gösterge dönemleri temel kaydın
ayarından gelir; mevcut ızgara eksenleri bu dönemleri veya ısınmayı değiştirmez.

Sinyal, işlem ve sonuç bağları ayrı `ayar_bagi` olaylarıdır. Olaylar koşu kimliğiyle ayrılır;
deneme, veri referansı ve ayar özeti her geçişte eşleşir. Eski işlem tablolarına, sonuç JSON'una,
golden ve sadakat çıktılarına alan eklenmez. Kayıtsız koşunun bağında deneme kimliği gerekçeli
boştur. Bağ olayları pilotun aynı kilit, makbuz ve yazma hatası sınırını kullanır. Kayıtsız
komutun bağ dosyası rapor dizinindeki `ayar-baglari.jsonl` dosyasıdır. Kayıtlı komutun bağları
açıkça verilen pilot dosyasına eklenir. Günlük etkinleştirme izni bu bağlardan türetilmez.
Kayıtlı günlük hesap, aileye ait eski başarı satırını kendi ayarının tamamlanmış hesabı saymaz.
Bu yolun kart kanıtı önizleme olarak etiketlenir; aileye ait eski kabul kanıtı seçilmiş
denemenin etkinleştirme kanıtı olarak sunulmaz. Önizlemenin durum ve kart CSV dosyaları
`rapor/onizleme/<kosu_id>/` altında ayrılır; normal `kartlar.jsonl` günlüğüne eklenmez.
Başarılı veya başarısız önizleme normal günlüğün dosyalarını değiştirmez ve sonraki normal
hesabı engellemez. Kayıtsız günlük davranış değişmez. Bu sıralama ve bozuk kayıt sınırları
`tests/test_ayar_aktarimi.py` içinde sentetik fiyatlarla denetlenir.
Dayanak: dağıtıcının 18.10, 23:44 teknik kararları; önceki pilot kimlik kuralı önceliklidir.

#### Deneme kayıt pilotu (S03, #84)

Bu bölüm #84'ün karar verilmiş kayıt sözleşmesini uygular. Kimlik ve serileştirme ayrıntıları
**YORUM / geçici pilot** seçimidir; kalıcı bayt biçiminin onayı #97'ye aittir. Tansu'nun işlem
günlüğü önerisi [T3], ayar revizyonu algoritmasının kaynağı değildir. Her açık kaydetme yeni
revizyondur; aynı değerleri kaydetmek veya önceki değere dönmek eski revizyonu yeniden kullanmaz.
Kaydedilmiş ayarın tekrar koşusu aynı denemeye bağlı yeni koşudur. Dayanak: #84 gövdesi ve
Levent'in 18.10 tarihli bu işe verilen girdileri; ortak kayıt sözleşmesi ve C07.

E5'in pilot yüzü `tansu/deneme.py` içindeki `PilotKayit` sınıfıdır. Dosya yolu çağıranın
açık girdisidir; eski `kayit/deneme.jsonl` pilot dosyası değildir. Pilot ayrı bir alanda tutulur.
Eski çağıranlar ve §5.11 okuyucusu değişmez. Modülün hash sınıfı §5.11'de açıklanır;
eski `kural_id`, `kosu_id` ve sınıf alanları yalnız eski referans olarak saklanır, yeniden üretilmez.
Pilot revizyonları Holm m'sine eklenmez; resmi sayımın sahibi §5.11'dir.

| Yüz | Girdi ve çıktı sözleşmesi |
|---|---|
| `deneme_kaydet` | Katalog varyantı, aktör, gerekçe, üst deneme, dönemler, veri/yöntem/risk/masraf ayarları ve eski referans → kimlik ve ayar özeti içeren kalıcı yazma makbuzu. Tam çözülmüş stratejinin sahibi `katalog.legacy_coz` olur; parametreler, kaynaklar ve katalog/şema sürümleri kayıt içinde korunur. Bu yüz eski tanımı kaydeder; panel seçimine izin vermez. |
| `kosu` bağlamı | Kayıtlı deneme, mod, görüntü, manifest özeti, üyelik sürümü, kod kimliği, ortam, bağımlılık özeti, tohum ve iş listesi → başlangıç makbuzundan sonra koşu tutacağı. E5 hesaplama çağırmaz. Hesabı çağıran, bağlam gövdesine ancak makbuzdan sonra girer. |
| `sonuc_kaydet`, `islem_kaydet` | Koşu tutacağı üzerinden sonuç/işlem bağları, ayar özeti, dönem, birimler, muhasebe politikası, uyarılar ve çıktı referansları → ekleme makbuzu. Deneme ve koşu bağı kayıtlı başlangıçtan gelir. |
| `bitir` | Durum, tamamlanan/başarısız iş kimlikleri, yöntemler, ölçüler, eserler ve özetler → bitiş zamanı taşıyan makbuz. Bildirilen işler başlangıçtaki iş listesiyle muhasebeleştirilir; eksik iş başarı sayılmaz. |
| `oku`, `kurtar`, `izle` | Olayları oku, eksik yazımı/bitmemiş koşuları göster, sonuç kimliğinden revizyona, veri ve kod kimliğine, başlangıç ve son duruma ulaş. Okuma özgün olayları değiştirmez. |
| `duzelt` | Hedef olay, gerekçe ve yeni değerler → yeni düzeltme olayı. Özgün olay ve özgün kimlikler yerinde kalır. |

Pilot şeması ve kimlik biçimi sürümlüdür. Kimlikler olay kimliğinden ayrı deneme ve koşu bağları
taşır. Ayar özeti oluşturma zamanını ve rastgele olay kimliğini içermez; aynı çözülmüş ayarlar aynı
özeti taşıyabilir. Nesne anahtarları sıralanır; liste sırası korunur. Metin, bayrak, tamsayı,
sonlu kayan sayı, açık ondalık, tarih, UTC zaman, liste, demet ve null ayrı türlerle kodlanır.
Tarih ISO takvim biçimindedir; zaman dilimli an UTC'ye çevrilir. NaN, sonsuz sayı, zaman dilimsiz
an ve desteklenmeyen tür yazılmaz. Risk ve masraf sayıları `Decimal` ile açık ondalık olarak
verilir; ikili kayan sayı bu alanlarda kabul edilmez. Kodlama ayrıntısı pilot sürümüyle birlikte
okunur; #97'nin kalıcı biçimi gibi sunulmaz.

`pilot_s03_v1` kodlaması, boşluksuz UTF-8 JSON tür çiftlerini kullanır. Etiketler `bos`,
`bayrak`, `tam`, `sayi`, `ondalik`, `metin`, `tarih`, `zaman`, `liste`, `demet`, `sozluk` olur.
Tamsayının yükü onluk metin, kayan sayının yükü `float.hex()`, ondalığın yükü `format(x, "f")`
olur; ondalık basamak sayısı korunur. `bos` yük taşımaz. Sözlük, anahtara göre sıralanmış
anahtar/değer çiftleri taşır; anahtar metindir. Liste ile demet farklıdır. Özet SHA-256'dır;
olay kimliği pilotta UUID4'tür. Satırın son LF baytı yazma sınırıdır. Yarım kuyruğa eklenen
`\t#pilot_s03_v1_kesik` işareti onun sonradan geçerli JSON sayılmasını engeller; eski baytlar
silinmez. Bu kodlama yalnız pilot okuyucusuyla birlikte kullanılır.

Izgara hücresi üst arama denemesine bağlı çocuk revizyondur. İleri yürüme seçiminde eğitim
denemeleri ve sabitlenen test denemesi bağları saklanır. Monte Carlo senaryoları koşuya bağlıdır;
yöntem veya tekrar ayarı değişikliği yeni revizyon ister. Bu alanlar yöntem ayarları ve bağlarıdır;
pilot yöntem hesabı veya günlük uygunluk kararı üretmez.

Yazıcı yerel süreçler arası kilit altında olay içeriğini son LF olmadan ekler ve diske aktarır.
Aktarım başarılı olduktan sonra LF ekleyerek olayı okuyucuya açar; makbuz bundan sonra döner.
Kimlik, kodlama ve makbuz hazırlığı LF'den önce biter. LF görünürlük sınırıdır: bundan önceki
G/Ç hatası yazma hatası verir ve olay eksik kalır. LF yazma çağrısı hata bildirirse yazıcı,
kilit altındaki dosya uzunluğuyla bu tek baytın eklenip eklenmediğini denetler.
LF eklendikten sonraki dosya kapatma veya kilit bırakma hatası kaydı geri almaz ve API'yi
başarısız yapmaz; aynı makbuzun `uyarilar` alanında çağırana bildirilir. Makbuzun kimlik
alanları değişmez; uyarılar dosya olayına eklenmez. Doğrudan okuma yüzleri kilit ve okuma
hatalarını değiştirmeden iletir. `kosu()` ve `duzelt()` yayından önceki hazırlık okumasında
oluşan G/Ç hatasını özgün hataya bağlı `PilotYazmaHatasi` olarak bildirir; henüz olay yayımlanmaz.
Yayın sonucu doğrulanamazsa API düz başarı veya kesin yazma hatası yerine
`PilotBelirsizHatasi` verir. Bu sınıf `PilotYazmaHatasi` alt sınıfıdır; `kayit_id`, `kosu_id`
ve `deneme_id` taşır. Koşu ve deneme bağı olmayan olayda ilgili kimlik null olur.
Mevcut yazma hatası yakalayıcıları koşuyu durdurur; belirsiz sonuç yeni bitiş olayı üretmez.
Yeni `PilotKayit` okuyucusunun `kurtar` ve `izle` yüzleri dosyadaki olayları esas alır;
önceki API sonucunu kullanmaz. Bitiş olayının LF'si yoksa koşu çözümsüz kalır; onaylı içerik ve LF varsa
bitiş geçerlidir. Görünürlük doğrulanırsa sonuç kesindir: görünür olay için makbuz,
görünmeyen olay için `PilotYazmaHatasi`. Dayanak: dağıtıcı, 18.10 22:34, Q1 kararı.
Bu sıra bütün olay türleri için aynıdır; aktarım hatasında tam JSON bile LF'siz kaldığı için
olay sayılmaz. Son LF kaybolursa kurtarma temkinli biçimde olayı eksik sayar; kendiliğinden
tamamlamaz. Bu yazma sırası `pilot_s03_v1` bayt kodlamasını değiştirmez.
Başlangıç yazılamazsa bağlam gövdesi çalışmaz; süren koşudaki
yazma hatası görünür hatayla dışarı çıkar. Tamamlanmamış son satır kurtarmada uyarı olarak kalır;
önceki tam satırlar okunur. Sonraki ekleme eksik kuyruğu tamamlanmış olay yapmaz. Bitişsiz başlangıç
çözümsüzdür; bağlamdan bitiş bildirmeden çıkmak kendiliğinden başarı üretmez. Düzeltmeler yalnız
eklenir; düzeltme kimlik ve ayar bağlarını geriye dönük değiştirmez.

Geri dönüşte pilot yazımı durdurulur ve eski uyarlayıcı kullanılır. Pilot dosyaları ve okuyucuları
korunur. Pilot tek başına günlük listeyi veya eski sınamayı yeni kayıtlarla bağlamaz; S07 bu aktarımı sağlar. Hesap formülleri
değişmediğinden `tests/test_gelecek.py` kapsamına yeni hesap eklenmez. Kayıt sınırının davranış
testleri `tests/test_kayit.py` dosyasındadır.

#### Strateji kataloğu (S02, #83)

E2'nin katalog sahibi `tansu/katalog.py` dosyasıdır. Katalog, mevcut 24 tanımı temel ve tek alan
değişikliği ilişkisiyle saklar. `aileler.Parametre` ve `aileler.VARYANTLAR` eski çağrılar için
uyarlayıcıdır; adlar, varsayılanlar, sabitler ve hesap çıktıları korunur. Katalog çözümlemesi yeni
gösterge veya işlem hesabı yapmaz. Dayanak: #83 brifi, §5.15 ortak kayıt sözleşmesi.

Saklanan tanım ile seçilebilir birleşim ayrıdır. Seçim izni, giriş, süzgeç, hedef, çıkış ve risk
ayarlarının bütününü destekleyen birinci el Tansu kaynağı gerektirir. Tek bir parçanın kaynağı veya
iki tek değişikliğin ayrı ayrı geçerliliği, birleşime izin vermez. Birleşim kanıtı kaynak konumu ve
tarihiyle tam kayda taşınır. Kanıtlanmayan tanım eski karşılaştırma olarak okunur ve seçimde açık
hatayla reddedilir. Dayanak: Levent 18.10.2026, #83 görev girdisi: "Siteden Tansu'nun anlatmadığı bir
bileşim şu anlık kurulamasın."

Tansu'nun kendi sözleriyle genel kullanım için verdiği stop veya çıkış paketi, Tansu kaynaklı
bir girişle eşlenebilir. Bütün parçaların aynı notta bulunması şart değildir. Stratejiye özel
bir paketin başka girişlere aktarılması veya yalnız sahip kararı, Tansu bileşim kanıtı sayılmaz.
Dayanak: #83 kaynak turu görev girdisi, genel paket ve sahip kararı ayrımı.

Çözümleyici aileyi, varyantı, katalog sürümünü, istenen sayısal ayarları ve işlem politikası
referanslarını doğrular. Bilinmeyen alan, bilinmeyen sürüm, eksik işlem ayarı ve izinsiz birleşim
ayrı hata kodları verir. Panel komutu ve katalog komut satırı aynı seçim doğrulayıcısını çağırır.
Eski uyarlayıcı seçime izin veren bir yol değildir. Dayanak: #83 brifi; §5.15 E2 ve ortak kayıtlar.

Tam kayıt, ortak kayıt alanlarıyla birlikte parametreleri, gösterge ayarlarını ve sürümlenmiş
sabitleri taşır. Her ayar türünü, birimini, kaynağını ve kökenini korur. Kayıt ve içindeki ayarlar
değişmezdir. İşlem politikası referansları gizli varsayılanla doldurulmaz; eski tanım kendi eski
politikasını açıkça taşır. Yeni kaynak veya birleşim izni yeni katalog sürümü gerektirir.
Dayanak: #83 brifi; §5.15 ortak kayıt sözleşmesi ve eski politikalar.

Alan kökeni ile bütün bileşimin kökeni ayrı değerlendirilir. Eski birleşimin YORUM olması,
birinci elde aynen verilen bir `periyotlar` değerini YORUM yapmaz. Böyle bir alan Tansu kaynağını
korur; açık sahip kararının alanı sahip kararı kökenini korur. Formül veya sayısal seçimin yalnız
bir kısmına dayanak olan not, destek kaynağı olarak eklenir; bütün hesap Tansu'nun birebir tanımı
diye etiketlenmez. Örneğin hacim notu ortalama üstüne kat verir, fakat mevcut ortalama penceresi
ve önceki günleri kullanma tanımının tamamını vermez
(`tweet-qullamaggie-tarzi-hacimli-breakout-tarama-1979546907505545421.md:29`, 18.10.2025, Ham).
Kaynak kökü T kaynaklarıyla aynıdır. Testin bütün alanları koşulsuz YORUM sayan ilk beklentisi bu
ayrımı kaybettiği için hatalıdır; alan kaynağına göre düzeltilir. Bu düzeltme birleşim iznini açmaz.
Dayanak: #83 alan kökeni şartı; `aile-kurallari.md` §3 ve bu bölümün kaynak sınırı.

`s02_v1` kataloğunda mevcut 24 tanım eski karşılaştırma olarak saklanır; seçimleri kapalıdır.
Kaynak turunda genel ATR çıkışı ve genel risk boyutlama dayanağı doğrulandı:
`tweet-atr-iz-suren-stop-tablosu-2045421697814126693.md:21–23` (18.04.2026, Ham ve G1),
"tüm hisseleri" anlatımı ve genel kullanım talimatlarıyla 2 ATR'de girişe stop, 3 ATR'de
1 ATR'ye stop ve yarı satış verir. Bu genel paket Tansu girişine eşlenebilir.
`tweet-statik-dinamik-atr-iz-suren-stop-1989985215452758434.md:23–34` (16.11.2025, Ham)
ayrı bir genel yöntem verir: 1,5 ATR ilerledikten sonraki önceki dip altı kapanışta yarı satış.
`tweet-volatiliteye-gore-pozisyon-buyuklugu-1987500065401733478.md:47–48` (09.11.2025, Ham)
her işlemde önceden belirlenmiş hesap yüzdesini riske etmeyi söyler. Genel paket dayanağı,
mevcut ortak paketin bütününe kendiliğinden izin vermez.

Özellikle `tweet-under30-over30-1-5r-basabas-cikis-1992547498343161903.md:22–32`
(23.11.2025, Ham) 1,5 R başabaş çıkışını Under 30 Over 30 girişiyle anlatır.
`tweet-rsi30-donus-yari-ve-tam-cikis-kurallari-1991721699922870638.md:20–34`
(21.11.2025, Ham) RSI50/SMA50 çıkışlarını RSI30 dönüşüyle anlatır. Bunların bütün EMA
girişlerine aktarımı doğrulanmadı. `gorsel-paket-115-position-sizing-yuzde1-2atr-sma250.md:20–22`
(kayıt 28.08.2026, Ham'da yazar yok, NotebookLM görseli) SMA250 ve 2 ATR'yi örnekler;
Ham başka ortalamalara da izin verir. Bütün girişlerde zorunlu SMA250 çıkışı ve eski
portföyün tavan/likidite politikası için bütün bileşim desteği doğrulanmadı. R/R kapısının
sahip kararı kökeni korunur (`aile-kurallari.md` §3). Bu eksikler yalnız sayısal YORUM değildir;
farklı strateji kapsamlarının ve risk politikalarının birlikte uygulanmasıdır.

Giriş parçaları ayrıca kaynaklıdır. Örneğin
`tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127.md:33` (19.12.2025, Ham, devamı 50.
satıra kadar) talep bölgesindeki giriş, stop ve arz hedefini birlikte anlatır. Genel ATR
paketiyle eşleme mümkündür; bu, yukarıdaki özel başabaş ve risk politikası eksiğini kapatmaz.
`tweet-ema-sikismasi-ucgen-kirilim-hacim-1954300245707497649.md:22` (09.08.2025, Ham, devamı 30.
satıra kadar) EMA, üçgen ve hacmi birlikte anlatır; mevcut `giris_ucgen` tanımının ek süzgeç ve
çıkış paketinin bütününe kanıt değildir. Kaynak kökü yukarıdaki T kaynaklarıyla aynıdır.
Doğru `context --no-sync` aramaları bu ortamda `read-only runtime is not initialized`
hatasıyla durdu. Adı verilen adaylar, ek Ham notları ve görseller doğrudan okundu; bütün
havuzda kaynak bulunmadığı iddia edilmez. Bu, bileşim kanıtı eksiğidir; sayısal ayrıntıların
YORUM olması tek başına ret gerekçesi değildir. Olumlu seçim kanıtlanmadığı için #83'ün
kaynaklı bileşim kabul ölçütü açıktır; yalnız sahip kararıyla seçim açılmaz.

`legacy_coz` tam eski kaydı okur. `secim_dogrula` seçim isteğini doğrular; `panel_komutu` ve
`python -m tansu.katalog coz` bu yüzü kullanır. `python -m tansu.katalog liste` saklanan tanımları
izin durumlarıyla gösterir. Bu yüzlerin kayıt şeması `strateji_s02_v1`, katalog sürümü `s02_v1`'dir.
İstekteki işlem ayarları `dolum_surumu`, `risk_surumu`, `masraf_surumu`, `muhasebe_surumu` ve
`donem_surumu` referanslarını açıkça taşır. Bunlar §5.15 ortak kaydının alanlarıdır; yeni işlem
politikasının uygulanması anlamına gelmez.

Sayısal alan ancak tanımsız eşik olarak işaretlenmişse ve onaylı arama aralığı varsa düzenlenebilir.
Bu iki koşul birlikte sağlansa bile tam birleşim izni ayrıca aranır. S02 girdilerinde onaylı arama
aralığı verilmediğinden katalog bu sürümde sayısal düzenleme açmaz. Dayanak: #83 brifi ve karar sınırı.

Uyum testinin elle hesaplı örneği (`tests/test_aileler.py`): ilk 510 kapanış 100, ardından 110 ve
112 olduğunda `bugun` için ilk sıçrama günü hâlâ sıkışmadır. EMA20 yaklaşık 100,95238, EMA200
100,09950; oran yaklaşık 0,00852'dir. Ertesi gün EMA20 yaklaşık 102,00454, EMA200 100,21792;
oran yaklaşık 0,01783'tür. Bu nedenle pencere 0 tabanlı 511. günde açılır. Testin ilk 510. gün
beklentisi hatalıydı; beklenen gün bu gerekçeyle düzeltilir. Eski ve yeni çözümün eşitliği şartı
değişmez. Bu örnek yeni kural veya Tansu kaynak kanıtı değildir; sıkışma ve pencere tanımını
uygular (`aile-kurallari.md` §3 ve TASARIM §5.15 eski davranışın korunması).

#### Kaynak strateji hazırlığı (#117)

**Hazırlık sözleşmesi; ürün kodunda uygulanmadı.** İlk ailenin kuralları, alternatifleri ve
açık alanları `aile-kurallari.md` §3, "Kaynak strateji hazırlığı" bölümündedir.
Bu bölüm ortak arayüzü ve kanıt aktarımını tanımlar; hesaplama veya seçim izni vermez.
Dayanak: #117 brifi; Levent'in 19.10.2026 hazırlama ve çalıştırmama kararı.

Girdi, #117'nin kaynak olarak bağladığı `paylasim-stratejileri/envanter.md` dosyasıdır
(YONETIM'deki yerel çalışma çıktısı; depoya kopyalanmaz). Envanter 21 tarihli bütün-strateji
paylaşımını aday olarak ayırır. Bu sayı çalıştırılabilir strateji sayısı değildir.
İlk aile dışındaki adayların uygulanması ayrı kapsamdadır. Üstteki genel paket sözleşmesi
korunur; bu hazırlık ayrı paylaşımları birleştirerek tek paylaşım kanıtı üretmez.

| Arayüz sınırı | Girdi ve zorunlu içerik | Çıktı / engel |
|---|---|---|
| Kaynak tanımı → E2 | Gönderi kimliği, yayım tarihi, Ham ve görsel başvuruları; aile, tanım revizyonu, giriş alternatifi, yön, zaman dilimi, veri gereksinimi, giriş/stop/çıkış kuralları, formül sürümleri ve açık alanlar. Her kuralın birinci el veya tarihli onaylı teknik yorum kökeni. | Kaynaklarıyla korunmuş hazırlık tanımı. Gerekli alan çözülmemişse tam çözülmüş strateji oluşmaz. |
| Bütün birleşim doğrulaması | Tanımın tamamı ve bütün birleşimin kanıtı; sayısal ayarlar ile açık işlem politikası referansları. | Eksiksiz, kaynakla doğrulanmış ve desteklenen tanım için §5.15 ortak kayıtlarındaki değişmez tam çözülmüş strateji; aksi halde alanı, nedeni ve kaynak konumu belirtilmiş engeller. |
| E2 → ortak kurulum | Tam çözülmüş strateji, değerlendirme tarihi, E1 veri referansı ve desteklenen piyasa satırları. | Mevcut ortak kurulum sözleşmesindeki gösterge/ısınma/sinyal kayıtları. Kaynak tanımı eski `Parametre` varsayılanlarına çevrilerek eksik tamamlanmaz. |
| Sinyal → E3 | Aynı strateji/revizyon ve ayar parmak izi; kaynaklı giriş isteği, ilk stop ve çıkış koşulları; dolum/risk/masraf politikası referansları. | Kurulum, giriş isteği, koruyucu stop ve çıkış olayı birbirinden ayrıdır. Sinyal gerçek dolum sayılmaz; E3 sözleşmesi burada uygulanmaz. |
| Tanım → deneme → koşu → sonuç | Kaynak kimliği ve konumları, tam birleşim/revizyon kimliği, kural kökenleri, izin dayanağı; ortak kayıtların deneme/koşu/veri/politika bağları. | Sonraki aşama aynı tanım ve kanıt bağlarını korur. Hazırlık sırasında deneme, koşu veya sonuç kaydı üretilmez. |

Kaynak izni, risk/masraf politikasının onayı ve günlük uygunluk ayrı denetimlerdir.
Genel bir teknik yorum, başka stratejiye ait özel paketin aktarımını kaynaklı yapmaz.
Yeni kabul edilen tanım yeni katalog sürümünü gerektirir; `s02_v1` ve eski 24 tanımın
seçim durumu değişmez. Yeni aile bağdaştırıcısı bu sözleşmeden otomatik olarak uygulanmış sayılmaz.

Günlük veri bağdaştırıcısında zorunlu zaman dilimi belirsizse veya gerekli açılış, gün içi
ya da dış veri yoksa alan adıyla engel döner. Günlük yüksek/düşük tek başına mum içi olay
sırasını ve dolum fiyatını kanıtlamaz. AOF, eksik açılışın yerine yazılmaz (§4, §5.1).
Desteklenmeyen veri için günlük hesaba sessiz dönüş yoktur.

Sonraki bağdaştırıcı uygulamasının gözlenebilir kabul örnekleri:

| Kontrol | Örnek / beklenen sonuç |
|---|---|
| Birinci el bütün anlatım | İlk ailenin aynı Ham:40,42,45,48–50 anlatımı giriş/stop/hedef kaynaklarını birlikte korur. Bu olumlu kaynak örneği, açık alanları çözmez ve seçim izni vermez. |
| Olumlu hesap kabulü | Bütün birleşim kanıtı, çözümlenmiş zorunlu alanlar ve desteklenen veri bulunan gerçek kaynak örneği tam kayda kabul edilir. Aynı kimlik/kanıt sonraki sonuçta korunur. İlk aile henüz bu koşulları sağlamaz; eksik tanım veya uydurma eşik olumlu örnek yerine geçmez. |
| Eksik kural | Bölge üretimi, giriş, stop, çıkış, zaman dilimi veya zorunlu formül eksik bırakıldığında ilgili alan ve nedeni döner; hesap başlamaz. |
| Ayrı alternatif | Kırılım kapanışı ve geri çekilme girişleri ayrı revizyon olarak kalır; aynı tanımda sessizce yer değiştirmez. |
| Desteklenmeyen veri | Zorunlu açılış/gün içi/dış veri yokken, günlük kapanış veya AOF ile devam edilmez. |
| İzinsiz birleşim | Ayrı ayrı kaynaklı giriş ve özel çıkışın bütün birleşim kanıtı yoksa seçim reddedilir. Grafik örneğinin sabit seviyeleri başka hisse veya döneme taşınmaz. |
| Kanıt aktarımı | Sonraki gerçek yürütmede tanım, sinyal, işlem ve sonuç aynı birleşim/revizyon, ayar ve kaynak bağlarıyla izlenir; eksik ya da uyuşmayan bağ kabul edilmez. |
| Hazırlık sınırı | Hazırlama işlemi gösterge, sinyal, işlem veya performans sınaması başlatmaz; günlük etkin seçim veya emir oluşturmaz. |

Bu tablo hazırlanmış kabul sözleşmesidir; bağdaştırıcı testlerinin çalıştığı veya olumlu
hesap/sonuç örneğinin üretildiği iddiası değildir. İlk ailenin açık alanları korunduğu için
çalıştırılabilir tanım yoktur. Sonraki gerçek yürütme ayrı açık başlatma izni bekler.
#116'nın küçük grup hazırlığı yıllık planı ve günlük uygunluk kapılarını değiştirmez.

#### Yöntem kayıtları ve açık kapılar

| Kayıt / durum | İçerik, çelişki ve kapanış kanıtı | Engellediği iş | Dayanak |
|---|---|---|---|
| WF — CLAUDE TEKNİK GİRDİ / yöntem kaydı eksik | D §2: kayan 12 ay eğitim, 3 ay test, çeyreklik ilerleme; ilk eğitim 2021, ilk OOS 2022-01-01–2022-03-31, son OOS 2025-10-01–2025-12-31. 2021 yalnız eğitim/keşif, beş yılın yıllık açıklayıcı sonucu yine gösterilir. Eski §5.14 genişleyen iki yıl yöntemi legacy kalır. Eğitimde seçilen ayar testte donar. 30 OOS/120 IS işlem sayıları araştırma uyarısıdır; ret eşiği değildir. Nihai kayıt pencere listesi, ısınma, seçim manifesti, açık işlem, ufuk ve veri/ayar kimliklerini birlikte taşımalıdır; ROBUST/RISK bağları eksikken tamamlanmaz. | **#93 ENGELLİ:** tam ve tutarlı WF yöntem kaydı olmadan uygulama başlamaz. | [L3]–[L5], [W1]; D §2. |
| MC — ARAŞTIRMA UYUŞMAZLIĞI / açık | C Q81: 10.000, ardından 20.000/40.000/80.000/100.000 ve yakınsama açıklaması. D §4: varyant başına 1.000. İkisi aynı protokol değildir; biri sessizce üstün sayılmaz. Kesin tekrar ve yakınsama sözleşmesini dağıtıcı tek yöntem sürümünde bağlamalıdır. | **#94 ENGELLİ:** tekrar, örnekleme ve muhasebe dahil tam MC yöntem kaydı olmadan uygulama başlamaz. | [L5], [W2], [W9]; C Q81, D §4. |
| MC örnekleme — kontrol edilmiş teknik girdi | D §4: net R sırasını yerine koymadan karıştırma; N işlemi N kez yerine koymalı çekme; hisselerde ortak tarih bloklarını yeniden örnekleme; %10 işlem kaçırma stresi; sayısal ayarda ±1 ızgara adımı/aynı değerden eşit olasılıklı tam yeniden sınama. Bunlar ayrı deneylerdir; %10 kalibre edilmiş hata oranı değildir. Sabit 42 tohum önerisi, üreteç/sürüm ve ayrı akış kimliğiyle kaydedilir. Ana girdi dondurulmuş WF OOS, 2021 için keşif etiketi. Her deney örnek birimi, ufuk, gerçekleşen tekrar sayısı, çıktı yüzdelikleri ve bağımlılık varsayımını taşır. | #94; önce WF, ROBUST ve RISK kayıtları gerekir. | [W2], [W9]; D §4, `mc-wf/arastirma.md` yöntem tablosu. |
| ROBUST — ARAŞTIRMA UYUŞMAZLIĞI / açık | B Q75: çaprazlar dahil tek indeks adımı komşuluk, kenarda eksik komşuluk bayrağı; otomatik kabul/ret yok. C Q77: en küçük komşu skorunu en büyüt; Q95: kanonik demetle eşitlik. D §3: tam iç komşuluk, kenarı merkez seçme; en geniş bileşen, medyan, iç uzaklık, sonra en kötü komşu net R ve sözlüksel sıra. Eski §5.14 eksen komşusu ayrı legacy'dir. Tek seçim ve kenar politikası onaylanmadan hiçbiri yeni varsayılan yapılmaz. Izgara sınırları ve adımlar strateji manifestinde dondurulur. | #92 seçici kısmı, #93, #94. | [T1], [W3]; B Q75, C Q76/Q77/Q95, D §3. |
| RISK — tek hisse bağlı; çift #128'e taşındı | Dağıtıcı 19.10, 02:10: %2 bütçe planlanan alış/stop komisyonu ve BSMV'yi içerir; adet aşağı tam sayıya yuvarlanır, kalan bütçe ayrıca döner. Uygulama ve R tanımının sahibi S08 risk ve maliyet hesabıdır. Çiftin adet ve R'si gerekçeli boştur; sayısal dayanağı #128 belirler. Eski §5.3 masrafsız R legacy kalır. | #89 tek hisse risk boyutlama; #128 çift; #92 net R eğrisi, #93, #94. | [L1], [T2], [T3], [W6]; D §1, C Q96; dağıtıcı 19.10, 02:10. |
| BİLEŞİM — kanıt kapısı | A Q15'teki kaynak anlatısı, giriş/teyit/stop/hedefi tam bileşim kimliğine bağlanır. Ayrı ayrı izinli alanlar tam birleşimin iznini kanıtlamaz. Eski 24 tanım korunur; yeni panel izni kaynak eşlemesi ve #71 gölge çıktısı koşulundan ayrılmaz. | #83, #88, #96'nın izinli seçim kısmı. | [L5], [T3], [W8]; A Q15, taslak katalog tablosu; mevcut §4 gölge kuralı. |
| SAHİP-64 — açık | Gerçek emir tutarı seçilmez. Sinyal platformunda yalnız açıkça varsayımsal tutarla kapasite/kayma senaryosu gösterilir; katılım ve etki katsayısı kalibre edilmiş BIST olgusu sayılmaz. | Gerçek tutarla kapasite iddiası; varsayımsal raporu engellemez. | [L1]; B Q64, [W4]. |
| SAHİP-86 — açık | Rastgele giriş ve maruziyet eşleşmeli karşılaştırmaların yeni motorda zorunlu başarı kapısı olup olmayacağı Levent'te. Eski resmi kapılar silinmez ve yeni yola otomatik taşınmaz. | #95 günlük uygunluk kararı. | [L4]; C Q86, [W2]. |
| SAHİP-111 — açık | Mühendislik kanıtlarının yeni motor için hangi zorunlu kabul paketini oluşturacağı Levent'te. Şema/kimlik kaydı yazmak bu sahip kararını vermez. | #95 günlük uygunluk kararı. | [L4], [W8]; C Q111. |
| SAHİP-d5 — açık | Başarı eşiği, asgari işlem/ayrı gün sayısı ve ileri gözlem süresi ilk sonuçlardan sonra Levent'te. Sonucu görülen veri keşif sayılır; sonraki doğrulama dönemi başlamadan seçilen kapılar tarihli kayda alınır. | #95; yeni başarı veya ileri gözlem onayı. | [L4], [W1]; D §5. |
| UYGUNLUK — açık | Sonuç gösterimi serbestliği günlük seçim değildir. #95 için tam strateji/ayar/kod/veri/politika kimliği, karşılık gelen kanıt, Levent'in sonraki kabul kararları ve tarihli etkin seçim kaydı gerekir. Aile adı veya en son kârlı sonuç yeterli değildir. S01 günlük koşu ve görev kurmaz. | **#95 ENGELLİ:** uygunluk sözleşmesi ve SAHİP-86/111/d5 kapanmadan etkinleştirme yok. | [L4], [W8]; taslak günlük seçim kaydı. |

S01 açık yöntem ve sahip kapılarıyla kapanabilir; bu kapanış #93, #94 veya #95'e uygulama/etkinleştirme
izni vermez. Fon/kripto kapsamı ve kalıcı kimlik onayı bu motor sürümünün kararı değildir. Dayanak: [L1], [L4], [L5]; #82 kapsamı ve bu işin talimatı.

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
   - (Bilet 14) "Tam" = her sembolün bütün geçmişi (2010'dan); indirilen semboller bugünün evreni (en çok sembollü
     son tam anlık görüntüden; taban başka aydaysa tabanın son ayının evreni, YORUM) ve dünkü açık kartların
     hisseleridir (~100). Dünkü kartın hissesi durumundan bağımsız (AKTİF, STOP, bekleyen çıkış) indirilir; STOP ve bekleyen çıkış dolana kadar pozisyon açıktır ve dolum günün çubuğunu ister. (vekil kararı 15.10, bilet 07c) Sebep: indirilen bütün semboller (716; bilet 03, sözlük denetimi) bilet 07'de ~3 sa 10 dk sürdü; görev sınırı 1 saat. 100 sembol
     ≈ 30 dk; istekler arası 1 sn bekleme aynen kalır. Günlük anlık görüntü `veri/gunluk/ag/` altına yazılır (tam
     anlık görüntüler `veri/ag/`'da kalır; `sinama` onları kullanır), faiz ve sektör içermez (kart bunlara bakmaz;
     KAP'a ~100 istek atılmaz). Tabanın aylık yenilenmesi (`evren-indir`) `TansuAylik` göreviyle ayın son günü 20:45'te yapılır
     (`kurulum/tansu-aylik.xml`).
   - (Bilet 14) Günlük koşunun veri kapıları, evren üyesi hisse-günlerde (5.13) hesaplanır; geçmişteki kaynak günü
     hataları eksik gün olarak zaten işlenir, yalnız bugünün kaynak günü hatası kartı durdurur.
   - Koşu 18:15'ten önce başlarsa kart üretilmez (yarım çubuk riski).
   - Kaynak erişilemezse sınama eski anlık görüntülerle sürer; yalnız canlı kart durur.
   - Günlük anlık görüntüler silinmez (`veri/` silinmez; 5.11 silme yasağı). (karar.md:24; İ: 11-061 reddedildi, karar.md:30; bilet 03)
3. **Piyasa durumu etiketi:** kart kararını ve motoru etkilemez (kapı değil, bilgi); K1 (b) örneklemesinde kullanılır; raporda ve kartta görünmez (3, 5.7). (vekil kararı 15.10, bilet 07e) XU100 kapanış > SMA50 (YORUM). (B-19, İ: 11-078; bilet 03)
4. **Kartlar** (P1, İ: 17-049, 17-050, 17-087):
   - Kâğıt ve Canlı ailelerin sinyalleri her gün yeni bir CSV dosyasına yazılır:
     `rapor/kartlar-YYYYMMDD.csv` (`;` ayraç, ondalık virgül, UTF-8 BOM).
   - Deneme aileleri gösterilmez.
   - Sinyal yoksa yalnız başlık satırı yazılır. CSV'nin yokluğu tek başına "koşu çalışmadı" demez: başarısız koşu da kart yazmaz. Koşunun çalışıp çalışmadığını ve neden başarısız olduğunu `durum.txt` söyler (6.7). CSV'nin ilk satırı her zaman başlıktır; veri bilgisi (anlık görüntü, son çubuk, sembol sayısı) `durum.txt`'te ve raporun başlığındadır. (İ: 17-050, 17-087; İ: 13-082'nin CSV kısmı reddedildi: karar.md:32, bilet 03)
   - Raporda başlık altında sabit uyarı: "Tansu'dan esinlenen yorum".
5. **Kart içeriği** (P1, P2, B-20, İ: 17-041, 01-079, 07-090, 08-009, 08-098, 09-041, 17-010, 10-051):
   - **Sabit sütunlar** (CSV başlıkları Türkçe ASCII, `AGENTS.md` Adlar kuralı; İ: 11-051): `tarih`; `hisse`; `aile`; `durum`;
     `referans`; `stop`; `pozisyon_yuzde`; `adet`; `fiili_risk`; `likidite_siniri_tl`; `kanit`; `kaynak`. Kart metni
     (Kanıt, Durum değerleri) Türkçe karakterlidir. (İ: 17-041; bilet 03)
   - **Referans:** sinyal günü kapanışı, ham TL olarak (düzeltilmiş seviye × ham/düzeltilmiş oranı). (İ: 01-079)
   - **Stop:** ham TL'dir: (düzeltilmiş referans − 2 ATR) × ham/düzeltilmiş oranı; ATR düzeltilmiş seride hesaplandığı
     için oran stopun tamamına uygulanır. "tahmini" etiketlidir. Gerçek stop, giriş dolunca Adım'da hesaplanır.
     (İ: 01-079; bilet 03)
   - **Durum:** AKTİF / STOP / GÜN SONU STOPU / KARANTİNA ÇIKIŞI / GİRİŞ İPTAL. (Bilet 14) AKTİF: giriş bekliyor ya da pozisyon açık. STOP: stop değdi
     (çıkış bugün ya da kilitli taban yüzünden bekliyor). GÜN SONU STOPU: kapanış SMA250'nin altına indi (5.5). KARANTİNA ÇIKIŞI: karantina nedeniyle çıkış. GİRİŞ İPTAL: bekleyen giriş iptal edildi. Kapanmış pozisyon kartı yalnız kapandığı günün CSV'sinde görünür.
     Eski kayıtlarda bu üçü tek etiket BOZULDU olarak durur (kayıt yalnız eklenir). Bunlar pozisyon durumlarıdır; Tansu'nun formasyon bozulması değildir. (vekil kararı 15.10, bilet 07c) (araç, G02/g1; Ham, tweet-abcd-geometrik-gecerlilik-kurallari:21; G13:21).
   - **Varyant:** günlük kart, EMA ailesinin varsayılan varyantı `bugun` ile üretilir; kart durumları (yukarıdaki Durum) değişmez (`aile-kurallari.md` §3).
   - (Bilet 14) **Tarih** sinyal günüdür. **Kaynak** her satırda "Tansu'dan esinlenen yorum · İş Yatırım <anlık görüntü kimliği>": yorum uyarısı ve veri kaynağı aynı
     hücrededir (İ: 17-087, bilet 03). Büyüklük (Pozisyon %,
     Adet, Fiili risk, Likidite sınırı) 1.000.000 TL kâğıt özkaynağıyla ve sinyal gününün tahmini stopuyla hesaplanır
     (nakit sınırı yok; gerçek nakit bilinmez). Stop sütunu giriş dolunca Adım'ın gerçek stopunu gösterir, etiketsiz.
     Stop hücresi "98,44 (tahmini)" biçimindedir. Çift ailesi Kâğıt olursa çift kartı henüz yazılmadı: koşu SORUNLU olur.
   - **Kanıt satırı** (tek tanım; İ: 09-041, 17-041; bilet 03): son resmi `durum` satırının `kanit` alanından gelir. İki
     ayrı ölçü ayrı ifade edilir: işlem düzeyinde işlem sayısı ve %0,3 masrafta işlem başına fazla getiri; günlük seri
     düzeyinde portföy fazla getirisinin (K2'ye göre) yıllık blok bootstrap %95 aralığı, birimi ve yöntemiyle. Aralık
     sıfırı içeriyorsa "ayırt edilemiyor" yazar. Kâğıt dönem = ilk Kâğıt `durum` satırından geçen gün // 30, ölçüt 6 için
     gereken 6 aya bölünerek yazılır. p, Holm p ve toplam deneme sayısı raporun "Ayrıntı" bölümündedir.
   - **Kanıt örneği** (Kâğıt aile): "Kâğıt · 148 işlem · sepete göre işlem başına fazla getiri +%x,x (%0,3
     masraf) · portföy fazla getirisi (K2'ye göre, yıllık, blok bootstrap %95 aralık +%x,x ile +%x,x) · kâğıt dönem 3/6 ay".
6. **Açık kartlar ayrıca saklanmaz:** her gün sinyal gününden itibaren Adım ile yeniden hesaplanır. Günün
   kart çıktısı `kayit/kartlar.jsonl`'e yalnız eklenir; kâğıt üstü dönem geriye dönük değişmez. (C-5)
7. **`rapor/durum.txt`** (İ: 16-036, 16-070, 13-082, 17-048):
   - İlk satır: `TAMAM` / `SORUNLU` / `VERİ YOK` / `BUGÜN ÇUBUK YOK` (tatil, çıkış 0).
   - Ardından: son başarılı koşu saati, anlık görüntü kimliği, son çubuk tarihi, sembol sayısı ve bir
     Türkçe eylem cümlesi.
   - (Bilet 14) Satırlar: `Son başarılı koşu: YYYY-AA-GG SS:DD`, `Anlık görüntü:`, `Son çubuk:`, `Sembol sayısı:`,
     `Eylem:`. Bilinmeyen değer "yok" yazılır. Başarısız koşu son başarılı koşu saatini önceki dosyadan korur. TAMAM ve
     BUGÜN ÇUBUK YOK başarılı sayılır (çıkış 0); SORUNLU ve VERİ YOK çıkış 1 verir (Görev Zamanlayıcı yeniden dener).
     "Çapraz kontrol yok" satırı yoktur: ikinci kaynak yok (bilet 01), TradingView yasak.
     VERİ YOK: kaynağa ulaşılamadı ya da koşu 18:15'ten önce başladı. Kaynak yayını gecikirse BUGÜN ÇUBUK YOK ayırt
     edilemez: tatil gibi sayılır ve o günün koşusu biter (bilinen sınır).
   - Levent yalnız buna bakar.
   - `durum.txt` ve CSV'ler geçici dosyaya yazılıp `os.replace` ile taşınır. CSV Excel'de açık olduğu
     için yazılamazsa durum SORUNLU olur: "CSV açık, kapatıp yeniden çalıştır".
8. **Rapor** (İ: 17-006, 17-007, 17-074, 17-077, 17-084):
   - Dosya adı `rapor/rapor-<koşu>.html` (koşu kimliği tarih ve saatle başlar; üstüne yazılmaz).
   - Başlıkta koşu kimliği, anlık görüntü, kod hash'i, m ve Holm tarihi.
   - Kabul tablosu (5.12).
   - Tek bir "Uyarılar" bölümü: karantina, bulunamayan semboller, tavan ve likidite bağlama oranları,
     olay denetimi farkları, iptal ve reddedilen sinyaller. Boşsa "Uyarı yok".
   - İşlem listesi `rapor/islemler-<koşu>.csv`: hisse, aile, giriş/çıkış tarihi ve fiyatı, çıkış
     nedeni, getiri.
   - Sayı biçimi tek bir yardımcıdan gelir: yüzde virgüllü (`locale` yok); TL raporda nokta binlik,
     CSV'de binliksiz; tarih ISO.

## 7. Uygulama sırası

Adım 1–9 tamamlandı (MVP biletleri, 05–06.10, yalnız git geçmişinde: `git show 8c5f06c^:.scratch/arsiv/tansu-mvp/issues/<dosya>`; GitHub ve CI'da bu klasör bulunmaz). Durum 14.10 ile eşlendi.

1. **Temizlik:** tamamlandı (05.10).
2. **Veri deposu:** `kaynak` + `veri`.
   - Kullanım koşulları ve fiyat adımı: tamamlandı (bilet 01, 05.10).
   - İş Yatırım ham ve düzeltilmiş fiyat, XU100 kapanışı, olay tablosu, olay denetimi: tamamlandı (bilet 02).
   - Veri kapıları, anlık görüntü, borsapy faiz ve sektör tabloları: tamamlandı (bilet 03, 04).
3. **Sadakat kontrolü** (`aile-kurallari.md` §4): ham seriyle; getiriye bakılmaz. Sonuç `docs/sadakat.md`'ye
   yazılır. Tamamlandı (bilet 05, 06).
4. **Evren** (5.2) ve **göstergeler**: tamamlandı (bilet 05, 07).
5. **Kural kaydı ve hash** (5.8): tamamlandı (bilet 09).
6. **Motor sınamaları** (5.3) → Adım + Motor: tamamlandı (bilet 08).
7. **Simülatör** (iki bölme) + faiz + K2: tamamlandı (bilet 10, 11).
8. **K1 + istatistik + deneme günlüğü;** boru hattı denetimi (5.12): tamamlandı (bilet 12, 13).
9. **İki aileyi koş; rapor.** Kâğıt üstü izleme ve Görev Zamanlayıcı başlar: koşu ve görevler tamamlandı (bilet 14, 15;
   ilk resmi koşu 05–06.10). Görevler 16.10'da kaldırıldı; bugünkü durum `docs/agents/zamanlayici.md`. İki aile de Deneme; kâğıt üstü dönem başlamadı.
10. **Gerçek BIST100** KAP endeks değişikliklerinden (paralel iş): bilet 16 (05.10), kısmi; sonuç §8 madde 2.

## 8. Açık sorular
1. İş Yatırım: kullanım sözleşmesi bulunamadı; robots.txt `/_layouts/`'u yasaklıyor (bilinen risk, 4).
   Hız sınırı ve günlük yayın saati bilinmiyor. KAP koşulları okunamadı.
2. ~~KAP endeks değişikliği duyuruları 2015–2016'yı kapsıyor mu?~~ Cevap (bilet 16, 05.10.2026): hayır.
   İlk BIST 100 dönemsel duyurusu 17.06.2016'dır (dönem 01.07.2016); 2015 ve 2016 ilk yarı KAP'ta yok.
   Dönemsel duyurular 2016-07'den 2026-10'a 42 dönemi kapsar ama yalnız alınan/çıkarılan listesi verir;
   dönem içi değişiklikler okunamadı. Dosya ve boşluklar: `docs/arastirma/bist100_kap_*.csv`.
3. Tedbirli hisseler (brüt takas, tek fiyat) bedava veriyle ayırt edilebiliyor mu?
4. ~~İşlemi kapanan sembollerin tam listesi bulunabilir mi?~~ Kısmen (bilet 07): Borsa İstanbul'un
   "İşlem Sırası Kapanan Şirketler" tablosu (`borsaistanbul.com/datum/IslemSirasiKapananSirketler.xls`,
   birincil) kod, tarih ve bazen açıklama verir. Tamlığı doğrulanmadı (KAP "üyeliği sona erenler" sayfasına
   ulaşılamadı).
5. 13.03.2020 öncesinde limit bütün paylarda ±%20 mi, bazı pazarlarda ±%15 mi (ikincil kaynak)? Limit
   fiyatı adıma içe mi yuvarlanıyor? Bilet 03'te veriyle ölçülür. (±%10 döneminde baz fiyat = önceki
   kapanış doğrulandı.) Bilet 07, yalnız ikincil haber kaynağı (borsaningundemi.com, hurriyet.com.tr
   "Borsa İstanbul'dan marjlara tedbir", 13.03.2020): 30.11.2015 öncesi iki seansta ±%10, 30.11.2015'te
   BISTECH ile ±%20; 13.03.2020'de ±%20 ya da ±%15'ten ±%10'a. Birincil kaynak (Borsa İstanbul duyurusu,
   Pay Piyasası Prosedürü) açılamadı. Kod 2010–2015 için ±%20 kullanır (karantina gevşek kalır; sinyal günleri
   01.12.2015'ten sayılır, rejim başı 30.11.2015; 5.1) ve ±%15 grubunu bilmez; birincil kaynak bulunana dek değişmedi.
6. Sıkışma oranının paydası düşüş trendinde EMA200 mü en küçük EMA mı? KRDMD'de ikisi aynı.
7. Bireysel yatırımcı için vergi.
8. `HACIM` toptan ya da çapraz işlemleri içeriyor mu? İçeriyorsa medyan şişkin olabilir. (İ: 08-027)
9. ~~Faiz serisi bir haftalık repo mu?~~ Evet (bilet 04): TCMB "1 Hafta Repo" tablosu, 2010-05-20'den 57 değişim
   günü. Sınır: 25.11.2016 – 01.06.2018 arası seri %8 sabit görünür; o dönemde fiili fonlamanın geç likidite
   penceresinden (daha yüksek) yapıldığı bilinen bilgidir ama bu bilette doğrulanmadı. Doğruysa nakit faizi
   o dönemde düşük kalır (muhafazakâr).
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
| M1 | Aynı gün stop ve hedef | EMA varyantlarında hedef vardır (§5.5; Levent 16.10.2026). Dolum §5.3'te, gün sırası `docs/aile-kurallari.md` §3, "Gün sırası" maddesindedir: stop hedeften önce gelir (YORUM; `docs/kurallar/E-risk-cikis-surec.md:69`, okuma 18.10.2026). Hedef kaynağı (Ham, `beyin/kisisel/300-Projects/Tansu X Veri Havuzu/tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127.md:47–50`, 19.12.2025): "İlk hedef, grafiğin sağ üstünde gördüğün Kırmızı Bölge (Supply/Arz) alanıdır." |
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
