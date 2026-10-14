# TANSU veri kaynakları araştırması

Tarih: 2026-10-05. Yöntem: kurulu paket kaynak kodu okundu, canlı uç noktalar sınandı, resmi belgeler okundu.
"Ölçüm" = bu oturumda çalıştırılan kod. "Belge" = resmi sayfa/PDF. "Doğrulanmadı" = kanıt yok.

## 0. Özet bulgular

1. borsapy fiyatı İş Yatırım'dan DEĞİL TradingView WebSocket'ten alır. Fiyat bedelsiz ve bedelli için düzeltilmiş gelir. Ama temettü düzeltmesi yoktur.
2. İş Yatırım `HisseTekil` uç noktası hem ham (`HG_*`) hem düzeltilmiş (`HGDG_*`) fiyat verir. `HGDG` bedelsiz, bedelli ve temettü için düzeltilmiştir. Anahtar gerekmez.
3. yfinance `.IS` fiyatı BIST için güvenilmez. Bedelsiz günlerinde sahte sıçrama var, AYGAZ'da sürekli yanlış bir çarpan var. `.splits` bedelliyi ve çoğu bedelsizi eksik/yanlış tarihli verir.
4. Kurumsal işlem kaynağı: İş Yatırım `GetSermayeArttirimlari` (borsapy'nin kullandığı). 2015'ten bugüne bedelsiz, bedelli, temettü, sermaye azaltımı döner. İşlem tarihi ve fiyat düzeltme çarpanı (`SHHE_FIYAT_AYAR_OR`) içerir.
5. Geçmiş BIST100/BIST30 üyeliği hazır tablo olarak yok. Borsa İstanbul her çeyrek KAP'a "Dönemsel Endeks Değişiklikleri" PDF'i koyar (yalnız değişenler). KAP API kimlik doğrulamasız çalışır.
6. Günlük fiyat limiti 2015-2026 boyunca sabit ±%10 DEĞİL. Ayrıntı Bölüm 5.
7. EVDS API anahtarı zorunludur. TLREF yalnız 2018-12-28'den başlar. Politika faizi için EVDS kodu doğrulanamadı.

## 1. Kurumsal işlemler (bedelsiz, bedelli, bölünme, temettü)

### 1.1 borsapy kaynak kodu
- `Ticker.splits` -> `IsYatirimProvider.get_capital_increases`; `Ticker.dividends` -> `get_dividends`. Dosyalar: `.venv\Lib\site-packages\borsapy\ticker.py` (satır 856-942) ve `borsapy\_providers\isyatirim.py` (satır 303-522).
- Uç nokta: `POST https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/StockInfo/CompanyInfoAjax.aspx/GetSermayeArttirimlari`. Gövde: `{"hisseKodu": SYM, "hisseTanimKodu":"", "yil":0, "zaman":"HEPSI", "endeksKodu":"09", "sektorKodu":""}`. Önce hisse sayfasına GET ile oturum çerezi alır (`isyatirim.py` satır 294-343).
- borsapy yalnız `SHT_KODU` in (01 bedelli, 02 bedelsiz iç kaynak, 03 bedelli+bedelsiz, 09 bedelsiz temettü) sınıflarını `splits`'e alır. Kod 04 (nakit temettü) `dividends`'e gider. Kod 78 (sermaye azaltımı) ve 07, 79, 90, 99 atılır (`isyatirim.py` satır 474-482).
- borsapy tuzakları (ölçüm + kod):
  - `Ticker.actions` ve `history(actions=True)` "Stock Splits" sütunu yalnız bedelsiz yüzdesini (iç kaynak + temettüden) kullanır; bedelli (RightsIssue) bu sütuna girmez (`ticker.py` satır 787-796).
  - `dividends.Amount` = brüt oran/100 (nominal 1 TL varsayımı). Temettü tarihi (`SHHE_TARIH`) ex-date mi ödeme tarihi mi doğrulanmadı.
  - AYGAZ 2022-09-01 `splits` içinde YOK (kod 78 filtrelendi). Ham veride var (aşağıda).

### 1.2 İş Yatırım ham yanıt alanları (ölçüm, 38 kayıt AYGAZ)
Alanlar: `SHT_KODU`, `SHT_TANIMI`, `SHHE_TARIH` (ms epoch), `SHHE_BDLI_ORAN`, `SHHE_BDSZ_IK_ORAN`, `SHHE_BDSZ_TM_ORAN`, `SHHE_NAKIT_TM_ORAN`, `SHHE_FIYAT_AYAR_OR` (fiyat düzeltme çarpanı), `HSP_BOLUNME_ONCESI_SERMAYE`, `HSP_BOLUNME_SONRASI_SERMAYE`. Kayıtlar 1990'lardan başlar; 2015'ten sonrası tam görünür.

Test vakaları (ham `GetSermayeArttirimlari`, tarih = `SHHE_TARIH`):

| Hisse | Kayıt tarihi | Tür | Oran | Çarpan `FIYAT_AYAR_OR` | Yahoo'da sıçrama günü |
|---|---|---|---|---|---|
| AYGAZ | 2022-09-01 | 78 Sermaye Azaltılması | sermaye 300M -> 219.8M | 1.0 | 2022-09-01 (ama Yahoo yanlış, bkz. 2.3) |
| CCOLA | 2024-08-13 | 02 Bedelsiz | %1000 | 0.0909 | 2024-08-01 (12 gün erken) |
| FENER | 2024-12-17 | 01 Bedelli | %152.58 | 0.4016 | 2024-12-09 (8 gün erken) |
| HEKTS | 2021-04-30 | 03 Bedelli+Bedelsiz | %175.77 + %102.13 | 0.2801 | 2021-04-30 |
| HEKTS | 2024-09-18 | 01 Bedelli | %233.20 | 0.3595 | 2024-09-09 (9 gün erken) |
| TUKAS | 2025-02-04 | 02 Bedelsiz | %205.64 | 0.3272 | 2025-02-03 (1 gün erken) |
| EUREN | 2024-12-05 | 02 Bedelsiz | %176.32 | 0.3619 | 2024-12-02 (3 gün erken) |

İş Yatırım ham fiyatı (`HG_KAPANIS`) kayıt tarihinin gerçek işlem tarihi olduğunu doğrular: CCOLA ham kapanış 2024-08-12'ye kadar ~860'lı, 2024-08-13'te düşer; FENER ham 2024-12-16 = 105.6, 2024-12-17 = 43.08; TUKAS ham 2025-02-03 = 6.23, 2025-02-04 = 2.04; EUREN ham 2024-12-04 = 11.31, 2024-12-05 = 4.21.
Not: çarpan yüzdelerden türetilemez (bedelli fiyata bağlıdır; HEKTS 2021: 1/(1+1.7577+1.0213)=0.2646, İş çarpanı 0.2801). Çarpanı doğrudan al.

Kaynaklar: ölçüm (İş Yatırım uç noktaları, borsapy kodu). Uç nokta resmi olarak belgelenmemiş (dahili AJAX).

### 1.3 isyatirimhisse paketi
PyPI v5.0.1 (2026-02-21), "İş Yatırım'ın resmi kitaplığı değil", "yalnızca kişisel kullanım", aşırı istekte IP engeli uyarısı: https://pypi.org/pypi/isyatirimhisse/json ve https://github.com/urazakgul/isyatirimhisse. Paketi kurmadık. Aynı `HisseTekil` uç noktasını (Bölüm 3.2) kullandığı varsayılıyor, doğrulanmadı.

### 1.4 KAP
KAP'ın açık JSON uç noktası çalıştı (ölçüm): `POST https://www.kap.org.tr/tr/api/disclosure/members/byCriteria` (gövde: fromDate, toDate, memberTypes vb.). Tek sorguda en çok 2000 kayıt döndü (ölçüm). Bildirim sayfası: `https://www.kap.org.tr/tr/Bildirim/{disclosureIndex}`. Sermaye artırımı bildirimlerini ayrıştırmak için gövde/ek metin okuma gerekir; bunu denemedik. KAP resmi API'si değil, belgelenmemiş; kullanım koşulları okunmadı.

## 2. yfinance (.IS) bedelsiz düzeltmesi (yfinance 1.7.0, ölçüm)

### 2.1 `splits` tablosu
- AYGAZ: yalnız 2001-2005 kayıtları. 2022-09-01 yok.
- CCOLA: 2024-08-13 = 11.0 (doğru oran, doğru tarih).
- FENER: 2024 bedelli yok. 2005-01-03 hariç hiçbir şey yok.
- HEKTS: 2021-04-30 = 2.0213 (bedelli+bedelsiz birleşik, mantıksız birleşim), 2022-10-12 = 1.4419. 2024-09 bedelli yok.
- TUKAS: 2025-02-04 = 3.0564 (doğru). EUREN: 2024-12-05 = 2.7632 (doğru).
- Hisse bölünmeleri `splits`'te var, bedelli tamamen yok.

### 2.2 Fiyat serisi (auto_adjust=False ve True farkı)
- `auto_adjust=True` bedelsiz düzeltmesi YAPMAZ. CCOLA 2024-07-31 `Close` = 846, `Adj Close` = 814.9 (yalnız temettü etkisi). Yani Yahoo'nun `splits` kaydı fiyat serisine uygulanmamış.
- Yahoo fiyat serisi İş Yatırım ham/düzeltilmiş serisiyle uyuşmaz:
  - CCOLA: Yahoo 2024-07-31 = 846 (ham), 2024-08-01 = 78.27. İş Yatırım ham 2024-08-01 = 861. Yani 2024-08-01'den 2024-08-12'ye kadar Yahoo fiyatları /11 ölçeklenmiş (yanlış), öncesi ham. Sahte -%90 getiri 2024-08-01'de. Yahoo/borsapy oranı 2015-2024 boyunca 11.0.
  - FENER: Yahoo 2024-12-06 = 111.0, 2024-12-09 = 44.96. İş ham 2024-12-09 = 104.5. Yani 12-09..12-16 arası Yahoo fiyatı yanlış düzeltilmiş.
  - TUKAS: Yahoo 2025-01-31 = 6.26, 2025-02-03 = 2.038 (İş ham 6.23). EUREN: Yahoo 2024-11-29 = 11.06, 2024-12-02 = 4.032 (İş ham 11.14).
  - HEKTS: Yahoo/borsapy oranı 2015-2021 1.539, 2022-2024 2.27-2.78, 2025 1.0 (kısmi, tutarsız düzeltme).
  - AYGAZ: Yahoo/borsapy = 0.5566 sabit, 2015 - 2022-09-01 arasında (2023'ten sonra 1.0). Sebep doğrulanmadı. İş Yatırım ham fiyat 2022-08-31 = 45.78, 2022-09-01 = 43.96 (süreklidir). Yahoo 25.48 -> 43.96 sahte +%72.
- Sonuç: Yahoo `.IS` günlük fiyatı bedelsiz/bedelli olaylarında hatalı. İlk fiyat kaynağı olamaz. THYAO gibi olaysız hisselerde borsapy ile aynı (oran 1.00; ölçüm).

## 3. Fiyat kaynağı: borsapy ve İş Yatırım

### 3.1 borsapy `Ticker.history`
- Kaynak: TradingView WebSocket `wss://data.tradingview.com/socket.io/websocket` (`_providers/tradingview.py` satır 101, 455-490). README: "BIST fiyat verileri TradingView WebSocket API üzerinden sağlanır, ~15 dk gecikmeli", "yalnızca kişisel ve eğitim amaçlı, ticari kullanım yok", Apache-2.0: https://github.com/saidsurucu/borsapy
- `adjust=True` (varsayılan): bölünme düzeltmeli. `adjust=False`: borsapy İş Yatırım `splits` ile ham fiyatı yeniden kurar (`ticker.py` satır 803-853), yani yalnız iç kaynak/temettü bedelsiz yüzdesini kullanır; bedelli için ham yeniden kurma doğru olmayabilir (bu yolu sınamadık).
- Ölçüm: 2015-01-02'den başlar, ~2946 satır (THYAO, HEKTS, AYGAZ, CCOLA). Yahoo'da 2994 satır (fazladan tatil günleri).
- Olay günlerinde süreklilik (Close): AYGAZ 2022-08-31 = 45.78, 09-01 = 43.96. CCOLA 07-31 = 76.91, 08-01 = 78.27. FENER 12-06 = 3.835, 12-09 = 3.610. HEKTS 2021-04-29 = 1.050, 04-30 = 1.026. TUKAS 01-31 = 2.048, 02-03 = 2.038. EUREN 11-29 = 4.003, 12-02 = 4.032. Sahte sıçrama yok. Bedelli (HEKTS, FENER) de düzeltilmiş.
- Temettü düzeltmesi YOK: borsapy CCOLA 2024-07-29 = 79.545 = ham 875/11. `auto_adjust=True` ile `Adj Close` ekler (`_compute_adj_close`, doğrulanmadı).
- Oran sınaması (Yahoo / borsapy), THYAO: 1.00 (2015-03, 2018-02, 2021-04, 2022-08, 2023-06, 2024-08, 2025-06). HEKTS, AYGAZ, CCOLA: Bölüm 2.2.
- Oran limiti: TradingView WebSocket için belge yok. README yalnız TEFAS için 429 (~4 istek, ~45 sn) belirtir. Çok sayıda hisse için istek hızı sınanmadı.

### 3.2 İş Yatırım `HisseTekil` (düzeltilmiş fiyat, ölçüm)
`GET https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse=CCOLA&startdate=29-07-2024&enddate=05-08-2024`. Tarih biçimi dd-mm-yyyy. Anahtar yok. Hisse kodu `.E` ekli verilirse boş döndü; kodu eksiz ver.
- `HG_KAPANIS/HG_AOF/HG_MIN/HG_MAX/HG_HACIM` = ham. `HGDG_KAPANIS/AOF/MIN/MAX/HACIM` = düzeltilmiş. Ek: `SERMAYE`, `PD`, `HAO_PD` (halka açık piyasa değeri), `DOLAR_BAZLI_FIYAT`, `END_DEGER`.
- `HGDG` bedelsiz, bedelli VE nakit temettü için düzeltilmiş (toplam getiri tipi): THYAO `HGDG/HG` = 0.9769 sabit 2015-01 - 2024-12, 1.0000 en son günde (2026-09-30). CCOLA: HGDG 2024-07-29 = 76.62 (borsapy 79.545, fark yalnız temettü). Olay günlerinde HGDG süreklidir (FENER, TUKAS, EUREN, HEKTS, AYGAZ oranları sabit; ölçüm).
- `HGDG` ile borsapy (TradingView) fiyatı aynı değil; ikisi de süreklidir ama HGDG temettü içerir. Getiri ve gösterge hesabı için hangisinin kullanılacağına karar ver (temettü dahil mi hariç mi).
- Alan başlangıcı: THYAO için 2015-01-02'den 2945 satır döndü (ölçüm).
- Oran limiti ve kullanım şartları: İş Yatırım için belge bulunamadı (doğrulanmadı). isyatirimhisse paketi aşırı istekte IP engeli uyarır (Bölüm 1.3).

### 3.3 Değerlendirme: borsapy/İş Yatırım Yahoo'nun yerine geçebilir mi?
Evet, teknik olarak. İş Yatırım `HisseTekil` hem ham hem düzeltilmiş fiyatı birlikte verir ve çarpan kayıtları (1.2) ile çapraz doğrulanabilir. Çekinceler: ikisi de resmi API değil; borsapy ticari kullanımı yasaklar, İş Yatırım şartları okunmadı.

## 4. Geçmiş endeks üyeliği (BIST30/BIST100)

- borsapy yalnız GÜNCEL üyeleri verir: `https://www.borsaistanbul.com/datum/hisse_endeks_ds.csv` (`_providers/bist_index.py` satır 12). Ölçüm: sütunlar BILESEN KODU; BULTEN_ADI; ENDEKS KODU; ENDEKS ADI; ENDEKS INGILIZCE ADI; TARIH. Tüm kayıtlarda TARIH = 05/10/2026 (güncel).
- Borsa İstanbul çeyrek dönemleri: Ocak-Mart, Nisan-Haziran, Temmuz-Eylül, Ekim-Aralık. Değerleme penceresi ve duyuru: dönemden en az 10 gün önce. Kaynak (Borsa İstanbul): https://www.borsaistanbul.com/en/indices/index-periodical-calendars . Bu sayfada geçmiş üye listesi YOK (okundu).
- Geçmiş üyelik kaynağı: KAP "Dönemsel Endeks Değişiklikleri" bildirimleri, Borsa İstanbul A.Ş. tarafından. Ölçüm (KAP API):
  - 2017-12-18: "BIST 30, BIST 50, BIST 100 Dönemsel Endeks Değişiklikleri", https://www.kap.org.tr/tr/Bildirim/645948 (2018 Q1, ekler: `2018_01_dönemsel_degisiklikler.pdf`). Metin: BIST 100, 50, 30 için 02.01.2018-30.03.2018 değişiklikleri "ekli tabloda".
  - 2020-12-21: https://www.kap.org.tr/tr/Bildirim/894142 (2021 Q1).
  - 2026 Q2 örneği: https://www.kap.org.tr/tr/Bildirim/1574461 (https://www.getmidas.com/midasin-kulaklari/bist-endeks-degisimleri-belli-oldu-p-352464 üzerinden).
  - 2015-12 ve 2015-09 günlerinde ve 2014-12/2015-01 pencerelerinde bu başlıklı bildirim bulunamadı (arama 2000 kayıt sınırına takılmış olabilir; sınanmadı). 2015 ve 2016 için kapsama doğrulanmadı.
- Bildirim yalnız DEĞİŞENLERİ listeler (PDF eki). Tam üyelik: bugünkü listeden geriye doğru ters uygulayarak veya bir başlangıç listesinden ileri uygulayarak kurulur. PDF ekleri indirilip ayrıştırılmadı. Hata birikir; bir çeyrek kaçarsa sonrası bozulur.
- Resmi arşiv: Borsa İstanbul DataStore (https://datastore.borsaistanbul.com). "Endeks Verileri" sayfası dosyaların 1 Ağustos 2015'ten itibaren yalnız DataStore'da olduğunu söyler (https://www.borsaistanbul.com/en/index/index-data). Geçmiş endeks üyesi ürünü, fiyatı ve ücretsiz olup olmadığı doğrulanmadı (sayfa içeriği okunamadı).
- Alternatifler (üçüncü taraf, doğrulanmadı): Kaggle veri setleri yalnız fiyat. Wikipedia güncel liste.

## 5. Günlük fiyat limitleri ve devre kesici

Birincil kaynak: Borsa İstanbul Pay Piyasası Prosedürü https://www.borsaistanbul.com/files/pay-piyasasi-proseduru.pdf (380 sayfa; metin fitz ile çıkarıldı; sayfa numaraları PDF sayfasıdır).

Zaman çizelgesi:
1. Aralık 2014 - 27 Kasım 2015: ABCD düzenlemesi (Dış Duyuru 2014/5, sayfa 237). Fiyat marjı rakamı bu belgede yok. Doğrulanmadı. Ölçüm (20 hissenin günlük getirisi, borsapy): 2015'te ±%10'u aşan günler az (6 gün, en yüksek +%13.3 / -%14.8) ve kurumsal işlem artefaktı olabilir.
2. 30 Kasım 2015 (BISTECH, Dış Duyuru 2015/88): paylar ve BYF için marj ±%20; rüçhan hakları ve ISKUR.E ±%50; kapanış seansında son işlem fiyatı ±%3. Devre kesici uygulaması devreye alındı. Kaynak: https://www.borsaistanbul.com/files/bistech-sistemiyle-pay-piyasasi-yeni-yapidaki-islevsel-degisiklikler.pdf (bölüm 2.1.2); prosedür sayfa 237.
   - Ölçüm doğrular: 2016-2019 arası 20 hissede günlük hareket +%20.0 / -%19.3'e kadar (2017: 10 gün >%10.5, 3 gün >%15.5).
3. 4 Kasım 2019: ABCD gruplaması kalktı (SPK kararı 19/09/2019 - 52; prosedür sayfa 26 dipnot 9).
4. 13 Mart 2020 - bugün: "Pay Piyasası'nda gün içi fiyat marjı, pazara/gruba göre %20 veya %15 iken tüm gruplarda %10'a düşürüldü; devre kesici tetikleme oranı %10 ve %7,5 iken %5'e; emir toplama süresi 5/15/25 dk iken 30 dk" (Duyuru 2020/20, 2020/21, "ikinci bir duyuruya kadar"). Kaynak: https://www.aa.com.tr/tr/ekonomi/borsa-istanbuldan-hisse-fiyatlarindaki-asiri-oynakliga-tedbir/1764150 ve prosedür sayfa 26 dipnot 10 (2020/20, 2020/21, 2020/50, 2025/38860 duyurularındaki kuralların genel tablodan öncelikli olduğunu söyler).
   - Ölçüm doğrular: 2021-2026 arası 20 hissede günlük hareket tam ±%10.0 ile sınırlı (n>%10.5 = 0, yalnız 2023'te -%10.5 bir hisse).
5. 1 Ekim 2020: yeni pazar yapısı. Prosedür tablosu (sayfa 26): Yıldız Pazar %20, Ana Pazar %15, Alt Pazar/YİP/PÖİP %10; devre kesici %10 / %7,5 / %5. Sayfa 53 (5.1.11) aynı rakamları verir. ANCAK dipnot 10, 2020/20, 2020/21 ve sonraki duyuruların bunun yerine geçtiğini söyler ve ölçüm ±%10'un hâlâ geçerli olduğunu gösterir. Bugünkü gerçek marjın pazar bazında dökümü doğrulanmadı; BIST100 hisseleri için ±%10 ölçüm sonucudur.
6. 10 Ağustos 2020: Endekse Bağlı Devre Kesici Sistemi (EBDKS) (Duyuru 2020/50): BIST 100 gün içinde önceki kapanışa göre belirli oranda düşerse tüm payda işlem durur. Sayfa 84.
7. 1 Eylül 2025 (Duyuru 2025/38860, https://www.borsaistanbul.com/files/duyuru-38860-TR.pdf): EBDKS tek aşamalı, eşik %6 (öncesi iki aşamalı %5 ve %7); durdurma 20 -> 10 dk; yukarı adım kuralı eşiği %3 -> %2; pay bazında devre kesici sonrası emir toplama 10 dk. Prosedür sayfa 84-86: pay bazında devre kesici emir toplama 10 dk, eşleştirme 2 dk.
8. Başka tedbirler: Volatilite Bazlı Tedbir Sistemi (VBTS) (2018-01-31 KAP duyurusu, https://www.kap.org.tr/tr/Bildirim/657146, "Pay Piyasasında Volatilite Bazlı Tedbir Sistemi"). İçeriği (brüt takas, tek fiyat, açığa satış/kredili yasağı) okunmadı, doğrulanmadı. Pay bazında devre kesici 2017-07-17'de değişti (Dış Duyuru 2017/47, prosedür sayfa 239), içeriği okunmadı.
9. İstisnalar: İş Bankası kurucu payı (ISKUR.E) ve yeni pay alma hakları ±%50. Bedelli/bedelsiz günlerinde fiyat tescili sırasında marj serbest veya ayrı (prosedür sayfa 36, "f" maddesi: yeni pay alma hakkı sırasında marj serbest, fiyat tescilinden sonra %50). Bu günlerde hisse fiyatı baz fiyat düzeltmesiyle değişir; ham getiri sınır dışı görünür.

Sonuç: ±%10 tüm dönem için DOĞRU DEĞİL. 2015-11-30 - 2020-03-12 arası marj ±%20 (BIST100 hisseleri dahil). 2020-03-13'ten beri ±%10. Backtest'te tavan/taban kuralı döneme göre değişmeli.

## 6. EVDS: politika faizi, TLREF, mevduat faizi

- EVDS taşındı: https://evds3.tcmb.gov.tr (eski evds2 kapandı; kaynak: https://apideposu.com/tr/blog/tcmb-evds-ve-kur-api-rehberi ve borsapy `_providers/evds.py` satır 3-13, ikincil kaynak). 
- API anahtarı ZORUNLU (ücretsiz). Kayıt: evds3.tcmb.gov.tr -> BENİM SAYFAM -> anahtarı kopyala. Anahtar HTTP başlığı `key` olarak gönderilir (26.08.2024 değişikliği, borsapy `evds.py` satır 321-323). `bp.set_evds_key(...)` veya `EVDS_API_KEY` ortam değişkeni. Oran limiti belgesi bulunamadı (doğrulanmadı). Bu oturumda anahtarımız olmadığı için veri çekilmedi; yalnız katalog araması (anahtarsız) çalıştı.
- Seri kodları (katalog araması, `bp.evds_search`, ölçüm; veri doğrulanmadı):
  - TLREF: `TP.BISTTLREF.ORAN` (oran), `TP.BISTTLREF.KAPANIS/DUSUK/YUKSEK` (endeks). Günlük (iş günü). TLREF hesaplamaya 2018-12-28, yayına 2019-06-17'de başladı (https://www.borsaistanbul.com/tr/sayfa/179/tlref-turk-lirasi-gecelik-referans-faiz-orani aramasından; Eylül 2019 kuralları: https://www.borsaistanbul.com/files/tlref-turk-lirasi-gecelik-referans-faiz-orani-kurallari-2019-eylul.pdf). 2015-2018 için TLREF YOK.
  - 2015-2018 gecelik faiz için aday veri grupları: `bie_onrepof` (Bankalararası Gecelik Repo Faizleri (Arşiv)) ve `bie_onrepofbap` (Borsa İstanbul Gecelik Repo Faiz Oranları). Bu gruplar altındaki seri kodları ve başlangıç tarihleri bulunamadı.
  - TCMB ağırlıklı ortalama fonlama maliyeti: `TP.APIFON4` (TCMB Net Fonlama: `TP.APIFON3`). Politika faizinden farklı olabilir.
  - Politika faizi (1 hafta repo): EVDS kodu doğrulanamadı (katalog aramasında "politika" yalnız yabancı merkez bankaları `TP.BISPOLFAIZ.*` döndü).
  - Mevduat faizi: `TP.TRY.MT01..MT06` (TL mevduat, akım, %, vade dilimleri). Veri grubu `bie_mt100h`: frekans HAFTALIK (Cuma), günlük DEĞİL. Ticari mevduat: `TP.TRYTIC.MT01..MT06`. 2015'ten kapsama doğrulanmadı.
- Politika faizi alternatifi (anahtarsız): borsapy `bp.TCMB().history("policy", period="max")` TCMB web sayfasını okur. Ölçüm: 57 satır, 2010-05-20 - 2026-01-23, yalnız karar tarihlerinde değişen basamak serisi (sütun `lending`, son 37.0). Günlüğe çevirmek için ileri doldur (forward fill). Sütunun tam olarak 1 hafta repo olduğu doğrulanmadı (borsapy açıklaması öyle diyor; `borsapy\tcmb.py` satır 3-4).
- TCMB 1 hafta repo sayfası EVDS kodu vermez: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo (tarihçe 2010'dan beri tablo).

## 7. Öneri

Bu bölüm 05.10.2026 tarihli öneridir. Güncel kararların sahibi TASARIM'dır; geri çekilen öneriler satırında işaretlidir. (bilet 05, 14.10)

1. Birincil fiyat kaynağı: İş Yatırım `HisseTekil` (ham `HG_*` + düzeltilmiş `HGDG_*`, 2015'ten, anahtarsız). İkincil/çapraz kontrol: borsapy `Ticker.history` (TradingView, bölünme düzeltmeli, temettüsüz). Yahoo `.IS` KULLANMA (olay günlerinde sahte %-90..+%72 sıçramalar; kanıt Bölüm 2). **Geri çekildi (ikincil/çapraz kontrol kısmı), yerine: TASARIM §4 "TradingView kaynaklı veri kullanılmaz" ve §5.1 "İkinci kaynak yok". Birincil kaynak ve Yahoo kararı geçerli (TASARIM §4).**
2. Kurumsal işlem kaynağı: İş Yatırım `GetSermayeArttirimlari` (ham yanıt, borsapy filtresi DEĞİL). Tüm `SHT_KODU` kodlarını sakla (01,02,03,04,09,78 ve diğerleri), `SHHE_FIYAT_AYAR_OR` çarpanını kullan, ham ve düzeltilmiş fiyatla çapraz doğrula. Doğrulama kuralı: ham kapanış günlük >|%25| sıçrıyorsa ve kayıt yoksa uyar. **Geri çekildi (sabit %25 eşiği), yerine: TASARIM §5.1 "Olay denetimi" (çarpanlı ham seri ile `HGDG` farkı %0,5'i aşarsa uyarı) ve "Karantina" (o günkü limit + %0,5). Kaynak ve çarpan kararı geçerli.**
3. Evren: BIST100 geçmiş üyeliğini KAP "Dönemsel Endeks Değişiklikleri" PDF'lerinden kur (2016'dan 2026'ya ~40 bildirim, 2015 kapsama doğrulanmadı) ve bugünkü CSV'den geriye doğru çapraz kontrol et. Hayatta kalma yanlılığını azaltmak için o dönemde işlem gören ama bugün listede olmayan hisseleri (İş Yatırım `HisseTekil` yine döner mi sınanmadı) dahil et. Alternatif: DataStore (ücret/kapsam bilinmiyor). **Geri çekildi (ana evreni KAP üyeliğinden kurma), yerine: TASARIM §5.2 "Evren kuralı" (ay başı piyasa değeri en büyük 100, likidite eleği). KAP çalışması yalnız ek karşılaştırmadır (TASARIM §5.2 "Gerçek BIST100", §8.2).**
4. Marj kuralı: dönemsel parametre (2015-11-30 - 2020-03-12 ±%20, sonrası ±%10; öncesi ve 2020-10'dan sonraki pazar bazlı ayrım doğrulanmadı). **Karar: TASARIM §5.1 "Fiyat limiti".**
5. Faiz: günlük risksiz oran için 2019-06'ya kadar TLREF yok. Politika faizi basamak serisi (TCMB sayfası) + EVDS `TP.APIFON4`/`bie_onrepof` (anahtarla sınanmalı). **Geri çekildi (EVDS ve alternatif seriler), yerine: TASARIM §4 "Faiz" (tek seri, TCMB "1 Hafta Repo") ve §8.9 (seri türü doğrulandı). Fonlama farkı belirsizliği §8.9'da açık kalır.**

## 8. Kalan bilinmeyenler

05.10.2026 tarihli liste. Cevaplananlar işaretlidir; açık sorular TASARIM §8'dedir. (bilet 05, 14.10)

1. İş Yatırım ve TradingView için resmi kullanım şartları, istek limiti. Toplu çekimin (~500 hisse x 11 yıl) engellenip engellenmediği sınanmadı. **Cevaplandı (bilet 01): TASARIM §4 "Kullanım koşulları"; açık kalan: hız sınırı, TASARIM §8.1.**
2. `SHHE_TARIH` nakit temettü kayıtlarında ex-date mi ödeme tarihi mi; temettü düzeltmesi HGDG'de hangi tarihle uygulanıyor. **Cevaplandı: TASARIM §4 "Şirket olayları" (tarih hak kullanım günüdür).**
3. Diğer `SHT_KODU` kodlarının (07, 79, 90, 99) anlamı. 78 = Sermaye Azaltılması. Birleşme/bölünme (spin-off) olayları nasıl kodlanıyor.
4. Önceki ABCD dönemi (2014-12 - 2015-11-27) marjı. Pay bazında devre kesici 2017-07-17 değişikliğinin içeriği. VBTS içeriği.
5. 2015-2016 KAP endeks değişikliği bildirimlerinin varlığı; PDF eklerinin makinece okunabilirliği. **Cevaplandı (bilet 16): TASARIM §8.2 (2015 ve 2016 ilk yarı KAP'ta yok).**
6. EVDS: anahtarla gerçek veri başlangıcı, politika faizi serisi kodu, 2015-2018 gecelik faiz seri kodu. **Geçersiz (EVDS kullanılmıyor): TASARIM §4 "Faiz", §8.9.**
7. Yahoo AYGAZ 0.5566 çarpanının nedeni.
8. DataStore endeks üyeliği ürünü ve ücreti.
