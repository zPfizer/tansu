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

Kaynak: beyindeki Tansu havuzu (sayı `KURALLAR.md` başlığında). Birinci el kaynak notların Ham metni ve görselleridir
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
- **2 aile** (`KURALLAR.md` §3): çift rotasyonu ve EMA sıkışması.
- Tansu kaynaklarından esinlenen risk paketi (5.5), işlem motoru, portföy simülasyonu ve istatistik.
- Tek dosya HTML rapor, CSV kart ve işlem listeleri, `durum.txt`.

**Yok** (ilk aile kabul edilene kadar bekler, gereksiz katman):
- Streamlit ya da başka panel, Telegram, veritabanı.
- Süre çıkışı (Ç3). İz süren stop ve kısmi kâr (Ç2) yalnız EMA ailesinde, test varyantı olarak vardır
  (Levent 16.10; `KURALLAR.md` §3). Çift ailesinde ve varsayılan kuralda yoktur.
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

| Modül | Girdi → çıktı | Not |
|---|---|---|
| `kaynak` | sembol, tarih aralığı → ham tablo | Ağa çıkan tek yer: İş Yatırım ve borsapy (yalnız faiz, sektör ve şirket listesi) (bilet 07e, 15.10). Ham alan adları (`HG_*`, `HGDG_*`) tek bir sözlükle proje adlarına çevrilir. İş Yatırım okuma zaman aşımı (5, 120) sn: ağır sorgular 40 ve 90 sn'de zaman aşımına uğradı; C-8'deki (5, 30) bu değerle değişti. (C-8, İ: 18-075, 01-057) |
| `veri` | indirme → anlık görüntü; olay tablosu; veri kapıları | Ayrıntı aşağıda. (B2, B-2, B-7) |
| `evren` | tarih → o gün yeni giriş için taranabilecek hisseler | 5.2. |
| `gostergeler` | fiyat → EMA, SMA, ATR, RSI, momentum squeeze, MACD, PSAR, stokastik, piyasa durumu | Vektörel; sınamada ve canlıda aynı kod. Kütüphane yok. Tanımlar `KURALLAR.md` §3'tedir. |
| `aileler` | hisse fiyatı → sinyal günleri, kurulum bilgisi (kutu, hedef), arz ve talep bölgeleri | Tek hisse aileleri. EMA ailesinin varyantları ve bölgeler `KURALLAR.md` §3'tedir. |
| `cift` | çift fiyatları → hangi hissede olunacağı | Kendi döngüsü. |
| `ciftbolme` | seçim, Z geçişleri, çift bölmesi simülasyonu, VAKBN–GARAN | `cift` ve `simulator`'a dayanır (bilet 11); 5.6. |
| `motor` | Adım: (pozisyon, bugünkü mum) → pozisyon; Motor: sinyaller → işlemler | Mum, ön hesaplı ATR ve SMA250 sütunları olan bir gün satırıdır. **Sınama ve canlı günlük aynı Adım'ı kullanır.** (A5, İ: 11-010) |
| `simulator` | işlemler + bölme kuralı → sermaye eğrisi | Boştaki nakit faiz kazanır. (A2, B4) |
| `istatistik` | fazla getiri → güven aralığı, p değeri, Holm | statsmodels yalnız `coint` ve Holm için. |
| `saglamlik` | ızgara hücreleri → pozitif hücre oranı | Önceden yazılmış ızgara (KURALLAR §3); her hücre işlem başına ortalama fazla getiri (sepete göre, K1 tekrarı yok). 5.10. (bilet 13, İ: 09-064, bilet 03) |
| `kayit` | kural kaydı, deneme günlüğü, kart günlüğü, durum kayıtları | Yalnız ekleme. Getiri gösteren tek yol `kosu()`'dur: kural kaydı yoksa ya da hash uyuşmazsa tek Türkçe satırla durur. (C-6, İ: 15-074) |
| `rapor` | sonuçlar → HTML + CSV + `durum.txt` | Ayrıntı 6. bölümde. |
| `denetim` | sentetik boş ve etkili dünya → yanlış kabul, güç | Boru hattı denetimi (5.12). Hash dışı: kuralı değil sınamanın doğruluğunu ölçer; sonucu günlükte kod hash'iyle durur. (bilet 13) |
| `gunluk` | `gunluk(tarih)`: günlük indirme, kapılar, kartlar, `durum.txt` | Bilet 14; 6. bölüm. `rapor`'dan sonra, `__main__`'dan önce. |
| `sadakat` | ham seri → Tansu'nun gösterdiği rakamlar yeniden üretilir | `KURALLAR.md` §4; getiriye bakılmaz; sonuç `docs/sadakat.md`. 7. bölüm adım 3. |
| `tansusinama` | anlık görüntü, sektör → hisse/çift başına ızgara, sağlam bölge, Tansu ölçüleri, ileri yürüme; JSON | Tansu'nun kendi sınama yöntemi; kabul kararına girmez. Hash dışı. 5.14. (Levent kararı 16.10) |
| `__main__` | `python -m tansu sadakat \| kayit \| sinama \| tansu-sinama \| denetim \| evren-indir \| sektor-indir \| gunluk` | Ayrıntı aşağıda. (İ: 16-001, 16-008, 14-084, 16-062) |

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
`kaynak` → `veri` → `evren`, `gostergeler` → `aileler`, `cift` → `motor` → `simulator` → `ciftbolme` → `istatistik`
→ `saglamlik` → `rapor` → `kayit` → `tansusinama` → `gunluk`, `denetim` → `__main__`.
(`rapor` yalnız `simulator`'a dayanır; `kosu()` raporu aynı çağrıda yazar ve `rapor-<koşu>.html` adı koşu kimliğinden
gelir, bu yüzden `kayit` `rapor`'dan sonra gelir. Önceki sıra `kayit` → `rapor` koda uymuyordu.)

**Test yüzleri:** testler yalnız bu yüzlere yazılır: Adım, Motor, Simülatör, İstatistik, Evren, veri kapıları, aileler (kurulum bilgisi ve bölgeler için
elle hesaplı mumlar), kayıt
(sonuc C-9), göstergeler (Wilder ATR ve EMA için elle hesaplı 5 satırlık örnek; İ: 12-018; RSI, momentum squeeze, ADX, MACD, PSAR ve stokastik için elle hesaplı kısa örnek) ve rapor (sahte sonuçtan rapor ve
CSV: sütun listesi, ilk satır cümlesi, sabit durum listesi, yasaklı kelime AL, SAT, ÖNERİ, "Tansu'nun sistemi"; İ: 17-093) ve
`tansusinama` (işlem getirisi, Tansu ölçüleri, sağlam bölge, ileri yürüme, işçi sayısı, 1 ve 2 işçide aynı sonuç). (bilet 03)

**Bağımlılık:** `tansusinama` makine ölçümü için `psutil` kullanır (boş bellek, CPU kullanımı); `requirements.lock.txt`'te
vardır, `pyproject.toml`'da `psutil==7.2.2` olarak sabitlenir.

Takvim, fiyat günlerinden çıkar (İş Yatırım XU100 günleri). Maliyet tek bir sabittir; Tansu sınaması (5.14) kendi sabitini kullanır.

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
  | ≥ 2.500 | 0,10 | 2,50 (doğrulanmadı) |

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
- **Sinyal ve giriş:**
  - Sinyal günün kapanışındadır.
  - İşlem fiyatı ertesi günün **ağırlıklı ortalama fiyatıdır (AOF)**. VAKBN–GARAN paneli T+1 açılış
    gösterir (araç, kaynak-vakbn-garan-rotasyon-2096358189696520213/g2, işlem paneli); uygulanamaz: mevcut veri kaynağında açılış yok.
    AOF, kaynak dolumunun yaklaşık modelidir.
  - Sinyal günü kapanış SMA250 altındaysa ya da SMA250 hesaplanamıyorsa giriş yok (YORUM, bizim).
    Kaynak kesin giriş karşılaştırmasını açıklamaz (Ham, G115:20; NotebookLM, g1).
  (S2-7, B-12, İ: 07-065)
- **Stop:** giriş fiyatından ve sinyal günü ATR'sinden hesaplanır. EMA ailesinin kutu stopu varyantında stop kutu
  altından gelir (`KURALLAR.md` §3). (M2, C10)
- **Giriş günü:** yalnız stop kontrol edilir.
- **Stop dolumu:** gün düşüğü ≤ stop ise dolum **min(stop, AOF)**. (B-4)
- **Hedef ve yarı satış dolumu** (EMA ailesi varyantları; tetikler `KURALLAR.md` §3):
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
- **Düşen sinyal:** giriş günü yoksa, kilitli tavansa ya da karantinadaysa sinyal düşer, sonraki güne kaymaz (vekil kararı 15.10, bilet 07e). Stop kutu altından geliyorsa ve giriş günü AOF'u ≤ kutu stopu ise de sinyal düşer (`KURALLAR.md` §3, kutu stopu). Sayısı
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
- **Hedef:** EMA ailesinin varyantları hedefi dener (Levent 16.10; hedef kuralları `KURALLAR.md` §3). Varsayılan kuralda
  hedef yoktur (YORUM: bizim seçim). Tansu bazı kurallarda hedef verir: gorsel-paket-106 Ham (EMA sıkışması + talep
  bölgesi: supply/arz bölgesi), gorsel-paket-107 Ham (1.618 dalga uzantısı), gorsel-paket-58 Ham (389.30). KRDMD örneğinde
  hedef yoktur. Çift ailesinde hedef yoktur; çıkış Z'nin 0.5'e dönmesidir (gorsel-paket-54 Ham).
- **Çift rotasyonu:** ayrı stop yok (YORUM, bizim); karşı uçta diğer hisseye geçilir. Risk paketi bu bölmeye uygulanmaz.
  Grafikte stop görünmemesi, stop bulunmadığını kanıtlamaz (Ham, G125:20; araç, kaynak-vakbn-garan-rotasyon-2096358189696520213/g2; eğitim, G118/g1).
  (Sorgu S3)
- **Aile kuralları:** giriş kuralları ve YORUM'lar `KURALLAR.md` §3'tedir.
- **İz süren stop ve kısmi kâr:** kaynak Ham'dadır (tweet-statik-dinamik-iz-suren-stop-atr:20; G125:20). EMA ailesinin
  varyantları ATR merdivenini, başabaş çıkışını ve dört yarı satış kuralını dener (Levent 16.10; çıkış paketi
  `KURALLAR.md` §3). Varsayılan kuralda bu paket yoktur; öbür aileler bu paketle kabul edildikten sonra denenir.
- **Yarı satışlı işlem:** işlem tablosunda tek satırdır. Çıkış fiyatı (yarı satış fiyatı + son çıkış fiyatı) / 2'dir; yarılar
  eşit adettir. Getiri ve gerçekleşen kayıp (5.3) bu ortalama fiyattan hesaplanır; masraf oranı sabit olduğu için getiri
  kesindir. İşlem tablosunda ayrıca `yari_tarih` ve `yari_fiyat` vardır (yarı satış yoksa boş). Hisse kapanırsa (5.2) ve
  yarı satış hissenin son işlem gününde ya da önce yapılmışsa (`yari_tarih` ≤ son işlem günü), çıkış fiyatı (`yari_fiyat` + 0) / 2
  olur; yarı satış yoksa 0 olur. Sınır: simülatör yarı satışın nakdini son çıkış gününde görür. Yarı satış ile son çıkış
  arasında nakdin faizi ve yeniden kullanımı eksik kalır.

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
- **Sinyal:** her gün kapanışta Z ve ΔZ (`cift.z_skor`, log oran, 60 gün, ddof 1; KURALLAR §3). Z ≤ −2 ve
  ΔZ > 0 ise hedef Y; Z ≥ +2 ve ΔZ < 0 ise hedef X (hedef = geçilecek bacak; kâr hedefi değildir, 5.5). Başka günde sinyal yok. Düşünülen çiftler yalnız seçilmiş
  çiftlerdir; seçim günü kapanışındaki sinyal ertesi gün işlenir.
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
    - **Liste:** aileler, cift, ciftbolme, evren, gostergeler, istatistik, kayit, motor, saglamlik, simulator, veri.
    - **İki not:** `veri.py` indirmeyi de içerir ama kapı ve karantina mantığı (`Anlik.gun_tablosu`, `adim`) kuraldır;
      dosya bölünmediği için bütünüyle listededir. `kayit.py` Holm, kabul girdisi ve K1 tekrar sayısının (B)
      hesabını içerir; o da listededir (muhafazakâr: kayıt kodu değişince yeni kayıt gerekir). Bu, tekrar
      sayısının değerinin hash dışı olmasıyla çelişmez: günlükteki `tekrar` alanı koşuda kullanılan değerdir; B'yi
      hesaplayan kod ve sabitleri (200, 1.000, 200·m) ise kuraldır. (karar.md:28; bilet 03)
    - Boru hattı denetimi (`denetim.py`) hash dışıdır.
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
Parametreler ve ızgara önceden yazılır (`KURALLAR.md` §3). Kurallar:
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
- **Satır başlangıcı ve bitişi:** her koşu önce `olay=basladi`, sonra `olay=bitti` satırı yazar.
  `bitti` satırı olmayan `basladi` de deneme sayılır.
- **Deneme sayısı (m), tek tanım:** Holm'un ve K1 tekrar sayısının (B, 5.7) m'si; resmi koşuların sınadığı (kural
  kimliği, aile) çiftleri sayar. Yarıda kalan, yani `bitti` satırı olmayan resmi koşu da m'ye sayılır (İ: 15-044);
  geliştirme koşusu sayılmaz. Aynı çift yeniden koşulursa ilk resmi p kalır. Başka bölümler (5.7, 5.12 boru hattı
  denetimi) m'yi yeniden tanımlamaz, buraya atıf verir. Yarıda kalan resmi koşunun (kural kimliği, aile) çifti Holm listesinde p = 1 ile yer alır; p = 1 sıralamada sona düşer, yani kabule yardım edemez, ve Holm ile B aynı tek m'yi kullanır. (bilet 03; vekil kararı 15.10, bilet 07d)
- **Varyant:** EMA ailesinin her varyantının kendi parametre parmak izi vardır; bu yüzden kendi kural kimliği vardır. Her
  varyant koşusu ayrı denemedir ve m'ye sayılır (varyantlar `KURALLAR.md` §3). Başka bir kural değişmez. Yeni
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
  arz ve talep bölgeleri, salınım noktaları, hedef, `arz` ve `ucgen` girişleri, düşüş süzgeci), çift Z ve hedef günleri,
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
  KURALLAR §3'tekidir: EMA 27 hücre; çift Z penceresi × Z eşiği, 6 hücre (seçim p'si yıllık çift seçimine aittir, burada yok).
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
- **Masraf:** her yönde %0,10, kayma yok: Tansu'nun tablosunda "Komisyon: %0.10" (görsel,
  tweet-winrate-80-tarama-backtest-tablosu-2092745592661246196). İşlem getirisi = çıkış·(1−m) / (giriş·(1+m)) − 1.
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
- **Bizim ek kontrolümüz:** aynı ailenin son resmi `durum` satırı (5.11, 5.12) çıktıda ve sitede yanında durur.
- **Hash:** `tansusinama.py` hash dışıdır (kabul kararını değiştirmez). `HASH_DISI` listesine eklenmesi `kayit.py`'nin hash'ini
  değiştirir: sonraki resmi koşudan önce `python -m tansu kayit` gerekir.

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
   - **Varyant:** günlük kart, EMA ailesinin varsayılan varyantı `bugun` ile üretilir; kart durumları (yukarıdaki Durum) değişmez (`KURALLAR.md` §3).
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

Adım 1–9 tamamlandı (MVP biletleri yerel, salt okunur arşivde ve git geçmişinde: `.scratch/arsiv/tansu-mvp/issues/`, 05–06.10; GitHub ve CI'da bu klasör bulunmaz). Durum 14.10 ile eşlendi. <!-- driftlint-ignore: local-only archive, gitignored, absent in CI -->

1. **Temizlik:** tamamlandı (05.10).
2. **Veri deposu:** `kaynak` + `veri`.
   - Kullanım koşulları ve fiyat adımı: tamamlandı (bilet 01, 05.10).
   - İş Yatırım ham ve düzeltilmiş fiyat, XU100 kapanışı, olay tablosu, olay denetimi: tamamlandı (bilet 02).
   - Veri kapıları, anlık görüntü, borsapy faiz ve sektör tabloları: tamamlandı (bilet 03, 04).
3. **Sadakat kontrolü** (`KURALLAR.md` §4): ham seriyle; getiriye bakılmaz. Sonuç `docs/sadakat.md`'ye
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
