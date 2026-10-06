# İzlenebilirlik tablosu: defter-1..4 fikirleri ve tasarım-8 (sürüm 5.2), iki eksenli

Kaynak: defter-1..4.md (denetim düzeltmeleri işlenmiş hali) ve tasarim-8.md (sürüm 5.2, 06.10.2026). 751 satırın her biri sürüm 5.2'ye göre bağlıdır (R245–R263 tweet metinleri kaynaktan çekildi, `ham-yapistirmalar-3.md`).

## Neden iki eksen (Levent 06.10 itirazı)

Eski tablo tek bir "durum" sütunu kullanıyordu: resmi, ölçüm, ikinci dalga, dışarıda, kapsam dışı, strateji değil. "Dışarıda", "kapsam dışı" ve "strateji değil" etiketleri fikri atılmış gibi gösteriyordu. Levent itiraz etti: 697 fikrin her biri Tansu'nun sisteminde bir şeye işaret eder. Bu yüzden durum sütunu iki eksene ayrıldı:

- **Rol (A):** fikir Tansu'nun sisteminde ne işe yarar? Tek değer. Rol, fikrin ne olduğunu söyler. Fikrin bugün nerede durduğunu söylemez.
- **Durum ve kilit (B):** fikir bugün tasarımda nerede durur ve neden o noktadan ileri gitmiyor? Tek değer. Değer ya bir sınav durumudur (resmi sınav, ölçüm kolu), ya bir kilittir, ya da fikrin işlem kuralı olmadığını söyler.

**Hiçbir fikir atılmadı.** Eski "dışarıda" ve "ikinci dalga" satırlarının hepsi şimdi bir kilide bağlıdır. Her kilit bir işle açılır (Tablo 2). Kilit açılınca satır ölçüm koluna ya da resmi sınava girebilir. "Bilgi: işlem kuralı değil" satırları da roldeki yerini korur: kitap, Python dersi, ürün hedefi ve makro notlar sistemi öğrenme ve ürün tarafından besler.

Okuma kuralları:
- Her satır bir defter fikir satırıdır (madde). Strateji içeriği olmayan kayıtlar tek satırdır.
- "Yer" sütunu tasarım-8 bölüm numarasıdır. "8:" sonrası, 8. bölüm tablosundaki satırın adıdır (adlar kısaltıldı). "(kavram)" = tasarım o R numarasını anmıyor, ama aynı kavramı başka bir R ile ya da aynı cümleyle bağlıyor. Bağ uydurulmadı. "İlke: tasarımın kuralı" satırlarında yer sütunu, ilkenin uygulandığı tasarım yerini gösterir (TASARIM = docs/TASARIM.md, taslak 7). Bulunamayan ilkelerde yer sütununda "ilke: tasarımda karşılığı yok" yazar.
- Rol, defterdeki aşama etiketinden başlar: tarama-evren → evren-likidite, momentum-seçim → seçim-momentum, teyit-tetik → teyit, hedef-çıkış ve stop-geçersizlik → çıkış, temel-değerleme → değerleme-temel, ölçüm-ilkesi → ölçüm-yöntemi. Diğer aşamalar aynı adla kalır (bölge, formasyon, giriş, boyut-risk, rejim, portföy).
- Rol geçersiz kılmaları: (1) "felsefe" ve "diğer" satırları tek tek ilke ya da araç-öğrenme olarak ayrıldı. İlke = sistemin nasıl kurulacağını söyler (duygusuz, kural, backtest, sermaye koruma, tepe-dip avlamama, likit hisse). Araç-öğrenme = kitap, Python dersi, motivasyon, benzetme, rakip yöntem anlatımı. (2) Sektör rotasyonu satırları seçim-momentum oldu. (3) Backtest, duygusuz ve benzeri satırlar ("ölçüm-ilkesi" ya da başka aşamalı) ilke oldu. (4) Makro, Gordon, CAPM ve ders satırları araç-öğrenme, "Ürün hedefi" satırları ürün-hedefi oldu. (5) R245–R263: 06.10'da tweet metinleri kaynaktan çekildi; satırlar defter-4'ün yeni fikir maddeleridir (önceki 19 "yalnız bağlantı" satırı kalktı). "çift" aşamalı R262 satırları ölçüm-yöntemi (R228 gibi), giriş ya da portföy oldu. (6) Gartley/Kelebek tarayıcı satırları formasyon, "yeni tarama kodumuz" (R192) satırı bölge oldu; değerleme ile ilgili ölçüm-ilkesi satırları değerleme-temel oldu.
- Durum ve kilit, tasarim-8 §2 (veri gerçeği) ve §8 (resmi olmayanlar ve neden) sütunlarından alındı. Eski "resmi" → resmi sınav; "ölçüm" → ölçüm kolu; "ikinci dalga" → bilanço verisi (değerleme, DCF, bilanço filtreleri, DEA, TOPSIS, konveks rotasyon, hibrit alarm) ya da Tansu kural vermedi (klasik formasyonlar, fincan-kulp, gizli pozitif uyumsuzluk, bant kuyruğu); "dışarıda" → §8'in nedenine göre veri kilidi, açılış, açığa satış, kural/formül yok ya da işlem kuralı değil; "kapsam dışı" ve "strateji değil" → kanıt yok, bilgi ya da ilke.
- Kural vermedi kilidine giren ve §8'in nedeni tam örtüşmeyen satırlar: RSI 30 ve diğer gösterge satırları (§8: "Tansu'nun ana sistemi değil"), Mum ve gösterge yorumları (HIKKAKE dahil; yalnız inverted hammer açılış kilidine girdi). Bu eşleme yorumdur.
- Bir satırda iki bileşen varsa baskın bileşen yazıldı; ikinci bileşen yer sütunundadır. R154 hem "DCF altyapısı" hem "Ürün hedefi" satırında anılır; "tek tuş" cümlesi için ürün hedefi esas alındı. Tasarımda R156 APO iki yerde anılır; "Bant kuyruğu" satırı esas alındı.
- Yazar kodları: T, M, G, G-dış, A, T/M (karışık), T+G (metin ve araç görseli).

| R | aşama | fikir | yazar | yer | rol (A) | durum ve kilit (B) |
|---|---|---|---|---|---|---|
| R001 | ölçüm-ilkesi | "Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın" | T | 8: Medyan temelli çalışma, medyan kanal (T R001) | ölçüm-yöntemi | ölçüm kolu |
| R002 | tarama-evren | "Sektör rotasyonu, yüksek korele sektörler, lider sektör" | T | 8: Sektör rotasyonu zinciri (T R002) | seçim-momentum | ölçüm kolu |
| R002 | temel-değerleme | "lider sektörde Dupont analizi, ucuz kalmış hisseler çalışması" | T | 8: Bilanço kalite filtreleri (Dupont, T R002) | değerleme-temel | kilit: bilanço verisi |
| R002 | diğer | "App'da da olacak Paylaşırım biterse" | T | ürün notu | ürün-hedefi | bilgi: işlem kuralı değil |
| R003 | formasyon | "güzel trend kırılımı yaptı ve bearısh butterfly yapı oluşturmaya gidiyor" | T | 3.2 H (Kelebek) | formasyon | resmi sınav |
| R003 | hedef-çıkış | "Strateji 125.42'ye kadar long fırsatı uyarısı verdi" | T | 3.2 adım 4 (ödül/risk kapısı, hedef); 6 (rapor: hedef) (kavram) | çıkış | resmi sınav |
| R003 | teyit-tetik | "Ancak pullback yapar mı izlemek lazım." | T | 8: Kanal alt bandı, düşen direnç kırılımı + retest (kavram) | teyit | ölçüm kolu |
| R004 | tarama-evren | "Arbitraj" | T | 3.3 (kavram) | evren-likidite | resmi sınav |
| R004 | portföy | "Volatilite Harvesti" | T | 8: Volatilite harvesti, rebalancing, Markowitz + volatilite trading (kavram) | portföy | ölçüm kolu |
| R004 | formasyon | "Harmonik yapılar (ABCD, Kelebek, Gartley)" | T | 3.2 H | formasyon | resmi sınav |
| R004 | momentum-seçim | "Alpha Hisseleri Momentum Hisseleri" | T | 3.1 S1; alpha kısmı 3.1 ölçüm kolu (R202) | seçim-momentum | resmi sınav |
| R004 | bölge | "Haftalık kanal dibine temas eden hisse taraması" | T | 8: Kanal alt bandı, düşen direnç kırılımı + retest (T R004) | bölge | ölçüm kolu |
| R004 | teyit-tetik | "Düşeni kıran Farklı kırılımları gösteren tarama" | T | 8: Kanal alt bandı, düşen direnç kırılımı + retest (T R004) | teyit | ölçüm kolu |
| R004 | formasyon | "Takoz TOBO OBO" ve "Bir de bayrak flama olur" | T | 8: Klasik formasyonlar (T R004) | formasyon | kilit: Tansu kural/formül vermedi |
| R005 | formasyon | "hangi noktada momentum squeeze olur onu pek anlatmazlar" | T | 3.2 H ölçüm kolları (harmonikte EMA sıkışması var/yok kesimi, T R005) | formasyon | ölçüm kolu |
| R006 | formasyon | "Takoz olur" | T | 8: Klasik formasyonlar (T R006) | formasyon | kilit: Tansu kural/formül vermedi |
| R006 | diğer | "Opsiyon fiyatları ile ABD borsasında analizler olur" | T | 8: VRP, implied move, IV kesişimi (kavram: opsiyon verisi yok) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R007 | formasyon | "Bir de bayrak flama olur" | T | 8: Klasik formasyonlar (T R007) | formasyon | kilit: Tansu kural/formül vermedi |
| R008 | formasyon | XABCD harmonik; "D: 226,80 [TAMAMLANDI]" | G | 4.3; 5.1 (H) | formasyon | resmi sınav |
| R008 | formasyon | "DGATE.IS - Kelebek Formasyonu (AL (Buy)) [AKTİF]", D 49.66 | G | 3.2 H; 4.3; 5.1 (DGATE) | formasyon | resmi sınav |
| R008 | teyit-tetik | X-B kırılım tarihi; X→B trend çizgisi tetiği araçta üretiliyor | G | 3.2 H ölçüm kolları (X–B trend çizgisi kırılımı girişi, G R008); 8: X–B trend çizgisi kırılımı | teyit | ölçüm kolu |
| R008 | formasyon | "MARKA ... AB=CD Patern #13 Backtest Modu", D (hedef) 70.25 | G | 3.2 H (AB=CD) | formasyon | resmi sınav |
| R008 | formasyon | "KRPLS ... D (hedef): 11.29 [TAMAM]"; Fibonacci 0.236 ... 2.000 | G | 4.2; 4.3; 5.1 (KRPLS) | formasyon | resmi sınav |
| R008 | bölge | "Kırılım 2026-07-29 (Temas:4)", "RSI Kırılım 2026-06-18 (T:3)" | G | 4.2 (trend çizgisi dokunuş sayısı ve kırılım, araç çıktısı G R008; ölçüm); RSI kırılımı kısmı 8: Mum ve gösterge yorumları (G R008) | bölge | ölçüm kolu |
| R008 | bölge | sarı arz, mavi talep bölgesi; volume profile; MACD ve RSI panelleri | G | 4.1 (volume profile kısmı 8: VWAP / POC / VAH / VAL; MACD/RSI panelleri 8: Mum ve gösterge yorumları) | bölge | resmi sınav |
| R008 | formasyon | yatay sıkışma, üçgen/flama benzeri daralma, "Kırılım" etiketi | G | 8: Kural taşımayan yan cümleler (yatay sıkışma/üçgen görüntüsü, G R008) | formasyon | kilit: Tansu kural/formül vermedi |
| R008 | formasyon | G1 ve G5: X, B, C, D etiketli harmonik; X-B nokta-çizgi trend çizgisi | G | 3.2 H; 4.3 | formasyon | resmi sınav |
| R009 | bölge | "böyle tam arz talep bölgesinde vereceğim" | T | 3.2 akış 2 (talep bölgesi zorunlu) | bölge | resmi sınav |
| R010 | temel-değerleme | "Nakit ve Nakit Benzerleri / Piyasa Değeri %18.89" | M | 8: Bilanço kalite filtreleri (nakit/piyasa değeri, M R010) | değerleme-temel | kilit: bilanço verisi |
| R010 | temel-değerleme | "Ancak oran tek başına “hisse ucuz” anlamına gelmez" | M | 8: Bilanço kalite filtreleri (M R010) | değerleme-temel | kilit: bilanço verisi |
| R010 | temel-değerleme | "Borçlar düşülerek net nakit / piyasa değeri hesaplanmalı." | M | 8: Bilanço kalite filtreleri (M R010) | değerleme-temel | kilit: bilanço verisi |
| R010 | temel-değerleme | "Oranın yükselmesi bazen nakit artışından değil" | M | 8: Bilanço kalite filtreleri (M R010) | değerleme-temel | kilit: bilanço verisi |
| R011 | tarama-evren | "Gartley taramasını ayrı yapın butterfly taramasını ayrı yapın" | T | 3.2 akış 3 (ayrı tarayıcılar, T R011) | formasyon | resmi sınav |
| R012 | formasyon | Tablo: Hisse, Tip, Sistem, Durum, Reaksiyon, D Hedefi, Giriş, Stop (X) | G | 1 (hat 2); 6 (tablo biçimi) | formasyon | resmi sınav |
| R012 | giriş | LUKSK: "AL (Buy)", D Hedefi 86.95, Giriş 86.95, Stop (X) 73.00 | G | 3.2 H; 5.1 (LUKSK) | giriş | resmi sınav |
| R012 | formasyon | SOKE: "D (Hedef): 12.53 [Carney]" = Fibonacci 0.786 | G | 3.2 H; 5.1 (SOKE) | formasyon | resmi sınav |
| R013 | teyit-tetik | "trade yapmanın bir yolu da XB noktasından çizilecek olan trend çizgisinin" kırılması | T | 3.2 H ölçüm kolları (X–B trend çizgisi kırılımı, T R013); 8: X–B trend çizgisi kırılımı | teyit | ölçüm kolu |
| R013 | stop-geçersizlik | "D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ" | G | 4.3 (20 bar ölçümde ayrı parametre); 5.1 (KAPLM) | çıkış | resmi sınav |
| R014 | teyit-tetik | "10 gün içinde D noktasından bir tepki yapmıyor ise belirsiz" | T | 4.3 (BELİRSİZ, T R014) | teyit | resmi sınav |
| R014 | felsefe | "Her gartley çalışmaz ama çalışmasa bile oluşumunda bazı stratejiler kurgulanabilir." | T | 6 (başarısız kurulumlar da listelenir, T R014) | ilke | resmi sınav |
| R014 | giriş | "Giriş (D)", "Bk Stop (X)", "TP1 (1:1 R/R)", "TP2 (.618 CD)" | G | 3.2 H (giriş D, geçersizlik X); TP1/TP2 3.2 H ölçüm kolları (hedef merdiveni, G R014); 5.1 (SAYAS) | giriş | resmi sınav |
| R014 | boyut-risk | SAYAS Fibonacci çizgileri 0.000 ... 1.000 | G | 4.2; 5.1 (SAYAS) | boyut-risk | resmi sınav |
| R015 | tarama-evren | "Haftalık taramada uzun vade talep toplama alanında C noktası oluşmuş" bullish gartley | T | 4.1 (haftalık bölge, T R015); 3.2 H | formasyon | resmi sınav |
| R016 | formasyon | "AB=CD patterninde, CD bacağının şiddetini ne belirler?" | T | 3.2 H ölçüm kolları (CD bacağının şiddeti raporu, T R016) | formasyon | ölçüm kolu |
| R017 | ölçüm-ilkesi | "Toplam pattern 12; hedefe ulaşan 7; stop/bozulan 3; açık 2" | G | 5.1 (SMRTG kapanmış kalıplar); 4.3 | ölçüm-yöntemi | resmi sınav |
| R017 | formasyon | "SMRTG - Swing Yapısı, Fibonacci ve AB=CD Analizi (Yükseliş)" | G | 5.1 (SMRTG); 4.2 | formasyon | resmi sınav |
| R017 | ölçüm-ilkesi | "BACKTEST SONUÇLARI (SMRTG)" konsol çıktısı | G | 5.1; 6 | ölçüm-yöntemi | resmi sınav |
| R018 | giriş | "AB=CD 1000 günlük C noktasından alım yapılsa idi D satış karları." | T | 3.2 H ölçüm kolları (C'den alım, D'de satış, T R018); 5.1 (ISKPL C tarihleri sadakat hedefi) | giriş | ölçüm kolu |
| R019 | formasyon | "BC, AB'yi aşamaz" | T | 3.2 H (AB=CD kapısı, T R019) | formasyon | resmi sınav |
| R019 | formasyon | "BC tam 1.00 olabilir" | T | 3.2 H (AB=CD kapısı, BC/AB üst sınırı 1,00) | formasyon | resmi sınav |
| R019 | formasyon | "D, B'yi aşmalı" | T | 3.2 H (AB=CD kapısı) | formasyon | resmi sınav |
| R019 | stop-geçersizlik | "C'den sonra fiyat A'yı geçerse patern bozuldu sayılır" | T | 3.2 H (giriş öncesi bozulma) | çıkış | resmi sınav |
| R020 | hedef-çıkış | "FIBO extension'ları öğrenin arkadaşlar ve ABCD ile nasıl kullanılacağını." | T | 4.2 (Fibonacci seviyeleri) | çıkış | resmi sınav |
| R020 | hedef-çıkış | Fibonacci merdiveni; uzantılar 1.272 / 1.618 / 2.000 | G | 4.2 (G R020) | çıkış | resmi sınav |
| R021 | ölçüm-ilkesi | "Finansta %70 çok yüksek bir başarı oranıdır ... 13 trade gününde 9 isabetli" | T | 8: RSI 30 / Williams %R / APO / A/D–EMA3 / HalfTrend / ML lojistik satırı (kavram) | ölçüm-yöntemi | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R021 | felsefe | "ML ile trade hiç sevmem ama ara ara bakarım" | T | 8: ML lojistik satırı (kavram) | araç-öğrenme | kilit: Tansu kural/formül vermedi |
| R022 | momentum-seçim | "Mom1'den Mom5'e kadar beş eşit dilimli ayirin" | T | 3.1 ölçüm kolu (5 dilimli çeyreklik hali, T R022) | seçim-momentum | ölçüm kolu |
| R022 | temel-değerleme | "faaliyet nakit akışlarına göre ... 1'den 5'e kadar yeni beşlik dilim" | T | 8: Momentum × faaliyet nakit akışı 5×5 satırı | değerleme-temel | kilit: bilanço verisi |
| R022 | portföy | "25 farklı kombinasyon portföyü oluşturun." | T | 8: Momentum × faaliyet nakit akışı 5×5 satırı | portföy | kilit: bilanço verisi |
| R022 | portföy | "aynı anda hem en yüksek momentuma hem de en yüksek nakit akışına sahip" | T | 8: Momentum × faaliyet nakit akışı 5×5 satırı | portföy | kilit: bilanço verisi |
| R023 | formasyon | "İşte bullish engulfing mum yapısı" (Python kodu) | T+G | 2 (açılış yok; mum formasyonu yalnız ölçülür); 8: Mum formasyonları (engulfing, G R023) | formasyon | ölçüm kolu |
| R024 | felsefe | "Her harmonik %100 çalışır diye de bir kaide olamaz" | T | 6 (başarısız kurulumlar listelenir) (kavram) | ilke | resmi sınav |
| R024 | bölge | "Destek ve dirençlere bakıyoruz Hacim ayak izine bakıyoruz" | T | 8: VWAP / POC / VAH / VAL (T R024) | bölge | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R024 | hedef-çıkış | "VAL seviyesine hareket etme potansiyeli görünüyor" | T | 8: VWAP / POC / VAH / VAL (T R024) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R024 | bölge | legend: Demand/Supply, Gaussian VP POC/VAH/VAL, BOS/CHoCH | G | 4.1 (bölge kısmı); 4.2 (BOS/CHoCH); VP kısmı 8: VWAP / POC / VAH / VAL | bölge | resmi sınav |
| R025 | formasyon | "Şu tweezer bottom mumunu yazayım taramasını da yapayım" | T | 8: Mum formasyonları (tweezer, T R025) | formasyon | ölçüm kolu |
| R025 | bölge | "Bu formasyon talep bölgesinde şahane fırsatlar sunuyor." | T | 8: Mum formasyonları (tweezer); 3.2 akış 2 (bölge) | bölge | ölçüm kolu |
| R026 | rejim | "Sabit hareketli ortalamalar ani piyasa paniklerinde yavaş kalır" | T | 4.5 (şok freni, T R026) | rejim | ölçüm kolu |
| R026 | rejim | "Kısa vadeli dalgalanma aniden fırlarsa algoritmayı Piyasa Şoku moduna geçirir." | T | 4.5 (şok freni, T R026) | rejim | ölçüm kolu |
| R026 | boyut-risk | "Yeni al sinyallerini tamamen durdur" | T | 4.5 (şok freni: yeni alım yok) | boyut-risk | ölçüm kolu |
| R026 | felsefe | "bıçak tutmaya çalışmayın ve sadece elinizdeki riski yönetin" | T | 4.5 (şok freni) | ilke | ölçüm kolu |
| R027 | bölge | "Bu kardeş bas basbağırmış talep bölgesinde ben geliyorum diye." | T+G | 4.1 (volume ayak izi kısmı 8: VWAP / POC / VAH / VAL) | bölge | resmi sınav |
| R028 | tarama-evren | "risk premium varyans ile modelden bağımsız varyans replikasyonu" iki kod | T | 8: VRP, implied move, IV kesişimi (T R028) | evren-likidite | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R028 | tarama-evren | "Kesişim kümesi yatırım noktasıdır." | T | 8: VRP, implied move, IV kesişimi (T R028) | evren-likidite | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R029 | hedef-çıkış | "%10.4 Implied Move opsiyon tüccarlarının ... beklediğini gösterir" | T+G | 8: VRP, implied move, IV kesişimi (T R029) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R030 | portföy | "Ters korelasyona sahip iki varlığı belirli bir oranda sabit tutarak ... volatilite harvesti" | T | 8: Volatilite harvesti, rebalancing, Markowitz + volatilite trading (T R030) | portföy | ölçüm kolu |
| R031 | ölçüm-ilkesi | "VRP (Risk Primi - Fırsat): Aradaki farktır (IV - RV)." | M | 8: VRP, implied move, IV kesişimi (M R031) | ölçüm-yöntemi | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R031 | teyit-tetik | "VOL SAT (VRP Yüksek) ... reversal beklenir" | M | 8: VRP, implied move, IV kesişimi (M R031) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R031 | teyit-tetik | "VOL AL (VRP Negatif ) ... çok sert ve büyük bir trend hareketinin" | M | 8: VRP, implied move, IV kesişimi (M R031) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R031 | tarama-evren | "BIST Variance Risk Premium (VRP) Scanner" dört panel | G | 8: VRP, implied move, IV kesişimi (M R031) | evren-likidite | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R031 | teyit-tetik | "Sat eşiği (0.025)" ve "AL eşiği (-0.005)" | G | 8: VRP, implied move, IV kesişimi (M R031) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R031 | tarama-evren | Dollar Gamma haritası %70 / %30 renk bölgeleri | G | 8: VRP, implied move, IV kesişimi (M R031) | evren-likidite | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R032 | momentum-seçim | Sektör getiri liderleri 30 / 60 / 90 gün | G | 3.1 ölçüm kolu (sektör lideri filtresi, G R032) | seçim-momentum | ölçüm kolu |
| R033 | tarama-evren | "Sektör rotasyonu yaparken anomalileri çıkarmaz iseniz sizi yanıltır." | T | 3.1 ölçüm kolu (30 günlük getiri mutlak değeri > %50 anomali hariç, G R033) | seçim-momentum | ölçüm kolu |
| R033 | tarama-evren | "ANOMALİ OLARAK İŞARETLENEN HİSSELER (30 günlük getiri mutlak değeri > %50) ... ortalamadan çıkarıldı" | G | 3.1 ölçüm kolu (G R033) | seçim-momentum | ölçüm kolu |
| R033 | tarama-evren | "Hisse bazlı basit ortalama" (eski fiyat-ortalaması terk) | G | 3.1 ölçüm kolu (G R033) | seçim-momentum | ölçüm kolu |
| R034 | stop-geçersizlik | "çok azı rolling cointegration ile zamanla bozulmayı önlüyor" | T | 3.3 (kapı: rolling eşbütünleşme, T R034); 2.1 (5.6 Çift) | çıkış | resmi sınav |
| R035 | tarama-evren | "İstenilen hissenin fiili dolaşım oranı görülebilir Eşik değer değiştirilebilir" | T+G | 8: Fiili dolaşım < %30; 2 (HAO_PD doğrulaması, KENT/GARAN karşılaştırması) | evren-likidite | ölçüm kolu |
| R036 | felsefe | "Fiyat ve hacim, resmin yalnızca üçte ikisidir, fiilen işlem gören hisse sayısı" | T | 8: Fiili dolaşım < %30 (T R036) | evren-likidite | ölçüm kolu |
| R037 | bölge | "Distal line ve proximal line'ı kavrarsak bu işişn %50'si biter" | T | 4.1 (T R037) | bölge | resmi sınav |
| R037 | bölge | "The distal line is located at the highest of the basing structure" | T+G | 4.1 (T R037 arz tarafı tanımı) | bölge | resmi sınav |
| R038 | — | "Al çalış" (strateji içeriği yok) | T | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R038 | bölge | "HKTM - Demand & Supply Bölgesi Analizi" | G | 4.1 (kavram) | bölge | resmi sınav |
| R039 | bölge | "1: Swing Pivot Eşleştirmesi." | T/M | 4.2 (pivot, T/M R039) | bölge | resmi sınav |
| R039 | bölge | "çizilen doğrunun aradaki hiçbir mum tarafından delinip geçilmemiş olması" | T/M | 4.2 (trend çizgisi: aradaki hiçbir mum çizgiyi delmez; düşen direnç kırılımı bu tanımla ölçülür) | bölge | ölçüm kolu |
| R039 | teyit-tetik | "fiyat buna her dokunup döndüğünde çizgi güçlenir, mum kapanışıyla aştığında trend kırılmış" | T/M | 4.2 (dokunuş sayısı güçtür; kırılım kapanışla) | teyit | ölçüm kolu |
| R039 | bölge | "2. Yöntem: Regresyon ve Zarf" | T/M | 4.2 (regresyon-zarf yöntemi ölçüm kolu) | bölge | ölçüm kolu |
| R039 | felsefe | "İnsan psikolojisini yansıttığı ... asıl kullanmamız gereken yöntemdir." | T/M | 4.2 (pivot yöntemi seçimi) | ilke | resmi sınav |
| R040 | bölge | "Confluence alanları neden her zaman daha güvenlidir?" | T | 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi (T R040) | bölge | ölçüm kolu |
| R041 | rejim | "BOS (Break of Structure): Trendin aynı yönde devam ettiğini gösterir." | T/M | 4.2 (yapı: BOS, M R041) | rejim | resmi sınav |
| R041 | rejim | "CHoCH (Change of Character) ... Higher Low altına düştüğünde" | T/M | 4.2 (yapı: CHoCH, M R041) | rejim | resmi sınav |
| R041 | bölge | FROTO tablo: En Yakın Demand 74.75 - 76.70, D.Teyit 2026-08-14 | G | 5.1 (bölge: FROTO); 4.1 (bölge temas sayısı, G R041) | bölge | resmi sınav |
| R042 | formasyon | "Advance Block ... art arda gelen 3 yeşil (yükseliş) mumundan oluşur" | M | 8: Mum formasyonları (advance block, M R042) | formasyon | ölçüm kolu |
| R042 | bölge | "alıcıların gücünün tükenmeye başladığını gösteren düşüş yönlü bir yorulma sinyalidir" | M | 8: Mum formasyonları (advance block, M R042) | bölge | ölçüm kolu |
| R043 | stop-geçersizlik | "Demand bölgesinin en dip fiyatını referans noktası olarak al." | T/M | 4.1 | çıkış | resmi sınav |
| R043 | stop-geçersizlik | "Bölgenin oluştuğu günden sonraki tüm mumların verisini sırayla taramaya başla." | T/M | 4.1 | çıkış | resmi sınav |
| R043 | stop-geçersizlik | "(Close < zone\_low)" | T/M | 4.1; 4.4 (bölge bitişi kapanışla) | çıkış | resmi sınav |
| R043 | bölge | "demand kutusunu ... tam bu kırılımın yaşandığı tarihte bitir." | T/M | 4.1 | bölge | resmi sınav |
| R044 | — | yalnız bağlantı (cmegroup.com) | bağlantı | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R045 | temel-değerleme | "Gordon Büyüme Modelini ... PV=100\*(1.05) / 0.10 - 0.05" | T | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (R045) | araç-öğrenme | bilgi: işlem kuralı değil |
| R046 | temel-değerleme | "Operasyonel Faktörler: ... endüstri yapısı, sunulan ürün, hedef pazar" | M | 8: Bilanço kalite filtreleri (işletme kriterleri, M R046) | değerleme-temel | kilit: bilanço verisi |
| R046 | temel-değerleme | "Finansal Faktörler: ... büyüklük, kaldıraç oranı, kar marjları" | M | 8: Bilanço kalite filtreleri (M R046) | değerleme-temel | kilit: bilanço verisi |
| R046 | temel-değerleme | "İşletme Analizi Kriterleri" infografiği (6 + 7 madde) | M | 8: Bilanço kalite filtreleri (M R046) | değerleme-temel | kilit: bilanço verisi |
| R047 | bölge | "FIGURE 1[RALLY BASE RALLY PATTERN] OR RBR PATTERN" | G | 4.1 (G R047) | bölge | resmi sınav |
| R047 | giriş | "ENTRY POINT" = "Proximal line" | G | 4.1 (proximal = tabanın en yüksek gövdesi) | giriş | resmi sınav |
| R047 | stop-geçersizlik | "DISTAL line always be at the low of base candle or leg out candle" | G | 4.1 (distal, G R047) | çıkış | resmi sınav |
| R048 | temel-değerleme | "Bir nevi rölatif değerleme yapıyor olacaksınız." | T | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R048 | teyit-tetik | "bunu farklı rasyolar ya da çarpanlar ile teyit edeceksiniz" | T | 8: Değerleme sistemi (kavram) | teyit | kilit: bilanço verisi |
| R049 | momentum-seçim | "Temel ve momentum staratejisi beraber çalışacak" | T | 8: Momentum × faaliyet nakit akışı 5×5 satırı (kavram) | seçim-momentum | kilit: bilanço verisi |
| R049 | temel-değerleme | "Ekranda mavi çizgi xxxx kırmızı ise fiyat bir altta iken diğeri kesin üste" | T+G | 8: YSA momentumu / Optimal Momentum+ / pre-signal / gizli "xxxx" metriği satırı (T R049) | değerleme-temel | kilit: Tansu kural/formül vermedi |
| R050 | bölge | "3. How to judge power of Im-balance" (Strongest / Strong / Weak / Weakest) | G | 3.2 E ölçüm kolları (FVG güç sınıfı, G R050) | bölge | ölçüm kolu |
| R051 | bölge | "En yüksek mumun gövdesinin bittiği yer ile, en düşük mumun gölgesinin bittiği yer." | T+G | 4.1 (konsolidasyon sınırı, T R051; ölçüm) | bölge | ölçüm kolu |
| R052 | diğer | "1 yıl sonra eur/try 57.61 olur, banka bize bu rakama göre forward kur" | T+G | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (R052) | araç-öğrenme | bilgi: işlem kuralı değil |
| R052 | hedef-çıkış | "ÖNERİLEN FORWARD KURLAR" (Konservatif / Medyan / Agresif) | G | 8: kur Monte Carlo (R052) | araç-öğrenme | bilgi: işlem kuralı değil |
| R053 | giriş | "Bollinger Bantlarında alt ve üst bantlar genelde +-2 standart sapmayı temsil eder" | T | 8: Bant kuyruğu tepki alımı (T R053) | giriş | kilit: Tansu kural/formül vermedi |
| R053 | giriş | "-2SE veya -3SE seviyesine inmesi ... tepki alımı fırsatı" | T | 8: Bant kuyruğu tepki alımı (T R053) | giriş | kilit: Tansu kural/formül vermedi |
| R053 | boyut-risk | "Bantların genişliği hissenin ne kadar riskli ve oynak olduğunu ortaya koyar." | T | 8: Kural taşımayan yan cümleler (bant genişliği, T R053) | boyut-risk | kilit: Tansu kural/formül vermedi |
| R053 | boyut-risk | "maksimum kaybı hesaplamaya yarar ... (VaR)" | T | 8: Kural taşımayan yan cümleler (VaR, T R053) | boyut-risk | kilit: Tansu kural/formül vermedi |
| R054 | bölge | "Bullish Sponsor Candle: Sert bir yükseliş hareketi başlamadan hemen önceki son düşüş mumudur." | T/M | 4.1 (sponsor mumu, G R054; ölçümde alternatif bölge) | bölge | ölçüm kolu |
| R054 | bölge | "Bearish Sponsor Candle: Sert bir düşüş hareketi başlamadan hemen önceki son yükseliş mumudur." | T/M | 4.1 (sponsor mumu, G R054) | bölge | ölçüm kolu |
| R055 | bölge | "Şu confluence alanları o kadar kıymetli ki, aslında grafiklerde bunları arayıp taratmak lazım." | T | 1 (hat 2); 4.1 (bölge kalitesi: talep + HSAR kesişimi, T R055); 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi | bölge | ölçüm kolu |
| R055 | bölge | legend: "Swing Points, Talep+HSAR Kesişimi", EMA 9/21/50/100/200 | G | 4.1 (bölge kalitesi: talep + HSAR kesişimi, G R055; ölçüm) | bölge | ölçüm kolu |
| R056 | diğer | "Hisse Senedi Analiz ve Karar Destek Süreci" (10 rasyo, MLP, teknik, karar) | G | 8: Ürün hedefi (infografik akış, R056) | ürün-hedefi | bilgi: işlem kuralı değil |
| R057 | temel-değerleme | "Öz kaynağın artışının en önemli sebebi bir şirketin net kar elde etmesi idi." | T | 8: Bilanço kalite filtreleri (özkaynak artışı, T R057) | değerleme-temel | kilit: bilanço verisi |
| R058 | temel-değerleme | "Regresyon veya makine öğrenmesi modelleri ile ... olması gereken piyasa değeri" | T | 8: Bilanço kalite filtreleri (regresyonla olması gereken değer, T R058) | değerleme-temel | kilit: bilanço verisi |
| R058 | felsefe | "Ml modelleri sıkıntılıdır" | T | 8: ML lojistik satırı (kavram) | araç-öğrenme | kilit: Tansu kural/formül vermedi |
| R059 | temel-değerleme | "Bilançolarda maddi duran varlık artışları er ya da geç (insider yoksa) fiyata yansır." | T+G | 8: Bilanço kalite filtreleri (T R059: veri gelince ilk sınanacak) | değerleme-temel | kilit: bilanço verisi |
| R060 | temel-değerleme | "Dönen varlıkları KVB’larından yüksek değilse o firma 1 yıl içerisinde nakde ihtiyaç duyacaktır" | T | 8: Bilanço kalite filtreleri (T R060: veri gelince ilk sınanacak) | değerleme-temel | kilit: bilanço verisi |
| R061 | temel-değerleme | "Merton Modeli A0 = ... (100) σA = ... (%25) D = ... (80)" | T+G | 8: Bilanço kalite filtreleri (Merton DD/EDF, T R061) | değerleme-temel | kilit: bilanço verisi |
| R061 | temel-değerleme | "D0 (74.6) ... DD (0.97) ... EDF (%17)" | T+G | 8: Bilanço kalite filtreleri (Merton DD/EDF, T R061) | değerleme-temel | kilit: bilanço verisi |
| R061 | boyut-risk | "Temerrüt önemli artık daha çok bakmak lazım." | T | 8: Bilanço kalite filtreleri (Merton DD/EDF, T R061) | boyut-risk | kilit: bilanço verisi |
| R062 | felsefe | "Temel analiz ve değerlemeyi küçümsemeyin Tüm bu analizler birbiri ile entegre olacak" | T | 8: Değerleme sistemi (T R062) | değerleme-temel | kilit: bilanço verisi |
| R062 | temel-değerleme | "hepsi tutarlı" (F/K, PD/DD, FD/FAVÖK hedefleri yakın) | T+G | 8: Değerleme sistemi (T R062) | değerleme-temel | kilit: bilanço verisi |
| R062 | temel-değerleme | F/K aracı: IQR (k=1.5), ortalama hedef 129.83 TL | G | 8: Değerleme sistemi (T R062) | değerleme-temel | kilit: bilanço verisi |
| R062 | temel-değerleme | PD/DD aracı: Kısa Dönem (8Ç), Uzun Dönem (36Ç), hedef 120.07 TL | G | 8: Değerleme sistemi (T R062) | değerleme-temel | kilit: bilanço verisi |
| R062 | temel-değerleme | manuel F/K 10.00x ve FD/FAVÖK 16.00x, ortalama 119.74 TL | G | 8: Değerleme sistemi (T R062) | değerleme-temel | kilit: bilanço verisi |
| R063 | temel-değerleme | "#TTRAK da 900'lerden çok güzel yıktılar malı millete." | T+G | 8: Değerleme sistemi (kavram: PD/DD primi) | değerleme-temel | kilit: bilanço verisi |
| R064 | temel-değerleme | "çarpanlara göre değerlemede fk, pd/dd , fd/favök kullanacaksın ... A olsun" | T+G | 8: Değerleme sistemi (T R064) | değerleme-temel | kilit: bilanço verisi |
| R064 | temel-değerleme | "basit model ile fk ve df/favök ile değerlemeyi bulacaksın ... B olsun" | T+G | 8: Değerleme sistemi (T R064) | değerleme-temel | kilit: bilanço verisi |
| R064 | temel-değerleme | "(A\*0.6) + (DCF \* 0.4) = Hisse fiyatın" | T+G | 8: Değerleme sistemi (T R064) | değerleme-temel | kilit: bilanço verisi |
| R064 | teyit-tetik | "B'yi teyit için de kullanabilirsin." | T+G | 8: Değerleme sistemi (T R064) | teyit | kilit: bilanço verisi |
| R065 | felsefe | "Nihai hedef Tek bir tuş ile temel ve teknik analizin yapıldığı ... LLM ve NLP" | T | 8: Ürün hedefi (T R065) | ürün-hedefi | bilgi: işlem kuralı değil |
| R066 | temel-değerleme | "beklenen FK hesaplanabilir mi, güvenilirliği ne olur?" | T | 8: Bilanço kalite filtreleri (beklenen F/K, T R058, R066) | değerleme-temel | kilit: bilanço verisi |
| R066 | temel-değerleme | "beklenen kâr büyüme oranı, özsermaye kârlılığı (ROE), temettü ödeme oranı, risk faktörleri (beta)" | T | 8: Bilanço kalite filtreleri (T R066) | değerleme-temel | kilit: bilanço verisi |
| R066 | ölçüm-ilkesi | "ilişki her zaman lineer değildir ... Çoklu doğrusal bağlantı problemleri" | T | 8: Bilanço kalite filtreleri (T R066) | değerleme-temel | kilit: bilanço verisi |
| R067 | temel-değerleme | "Ben tüm sekmelerin kodunu da yazacağım tek tuş ile hazır hale getireceğim" (6 sekme) | T+G | 8: Bilanço kalite filtreleri (skor kartı ve sekmeler, T/G R067) | değerleme-temel | kilit: bilanço verisi |
| R067 | temel-değerleme | Skor kartı: Makro %20, Sektör %20, Şirket %25, Finansal %25, Değerleme %10; karar matrisi | T+G | 8: Bilanço kalite filtreleri (skor kartı ve sekmeler, T/G R067) | değerleme-temel | kilit: bilanço verisi |
| R068 | temel-değerleme | "En sonunda bu ortalamanın %60'ını, DCF'in de %40'ını alırım." | T+G | 8: Değerleme sistemi (T R068) | değerleme-temel | kilit: bilanço verisi |
| R068 | temel-değerleme | seçilen dönem 2023/12; kısa dönem 8 çeyrek, uzun dönem 36 çeyrek, IQR k=1.5 | T+G | 8: Değerleme sistemi (T R068) | değerleme-temel | kilit: bilanço verisi |
| R068 | ölçüm-ilkesi | "2024 mart ayında gelen 2023 sonu bilançosuna göre yapılan değerlemede, Nisan ayında hisse tam da ederine ulaştı." | T+G | 8: Değerleme sistemi (T R068) | değerleme-temel | kilit: bilanço verisi |
| R069 | temel-değerleme | "Bu 1 milyar tl'nin bugünkü değeri, %20 iskonto oranı ile bugün 579 miliyon tl ediyor." | T+G | 8: Bilanço kalite filtreleri (proje cirosu bugünkü değeri, T R069) | değerleme-temel | kilit: bilanço verisi |
| R069 | teyit-tetik | "Buna bir de tekniği ekleyin olsun bitsin." | T+G | 8: Hibrit alarm (kavram) | teyit | kilit: bilanço verisi |
| R070 | temel-değerleme | "python ile DCF WACC hesaplamasını 3 farklı yolla yaparak ortalamasını alıyorum." | T+G | 8: DCF altyapısı (WACC üç yöntem, T R070) | değerleme-temel | kilit: bilanço verisi |
| R071 | temel-değerleme | "Beklenti satın alınır" (FED beklentisi ve altın) | T+G | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (kavram) | araç-öğrenme | bilgi: işlem kuralı değil |
| R072 | rejim | "Sağlıklı trend örneği" (CSCO, "TÜM ŞARTLAR SAĞLANDI") | T+G | 4.5 (kavram: sağlıklı yükseliş, T R093) | rejim | ölçüm kolu |
| R073 | formasyon | "bu kardeşimiz gartley yapmış, ABCD olmuş, bunlar talep bölgesinde kavuşmuş bir de düşeni de kırmış" | T+G | 3.2 H; 3.2 akış 2 | formasyon | resmi sınav |
| R073 | momentum-seçim | "Henüz endeksi yenecek güçte değil ama bu formasyonlar hisseyi oraya itecek" | T+G | 3.1 ölçüm kolu (endekse göre göreli güç, T R073) | seçim-momentum | ölçüm kolu |
| R073 | giriş | "yarın otorop izlemesi kalıyor" | T+G | izleme notu | giriş | bilgi: işlem kuralı değil |
| R074 | portföy | "Portföyün min volatiliteve maks sharpe ağırlıklandırmasına göre getiri eğrileridir." | T+G | 3.1 ölçüm kolu (Max Sharpe); 8: Volatilite harvesti, rebalancing, Markowitz + volatilite trading | portföy | ölçüm kolu |
| R074 | ölçüm-ilkesi | "Ortadaki çizgiler portföyün kapanış getirisi En üsteki çizgiler ise dönem içindeki en yüksek marjlar" | T+G | 6 (dönem içi en yüksek getiri DEY, T R074) | ölçüm-yöntemi | resmi sınav |
| R075 | formasyon | "Kuğuyu bir de talep toplama bölgesinde yakalarsanız" (Siyah Kuğu) | T+G | 3.2 H ölçüm kolları (Kuğu harmonikleri, T R075) | formasyon | ölçüm kolu |
| R075 | bölge | "LIDER / Düşen Direnci Kıran + Talep + Fibo + ABCD / Kırılım: 2026-05-18 / Temas: 3" | G | 1 (hat 2); 8: Kanal alt bandı, düşen direnç kırılımı + retest (G R075) | bölge | ölçüm kolu |
| R076 | formasyon | "Düşeni kırmış, sell yönlü abcd'yi tamamlamışi beyaz kuğu da oluşmuş" | T+G | 3.2 H ölçüm kolları (Kuğu harmonikleri, T R076) | formasyon | ölçüm kolu |
| R076 | teyit-tetik | "eh bunu yolculamayalım mı şimdi..." (yön çatışması) | T+G | 8: Kural taşımayan yan cümleler (sell yönlü AB=CD ile kırılım çatışması, T R076) | teyit | kilit: Tansu kural/formül vermedi |
| R077 | rejim | "Kırmızı oklar illa düşeceği anlamına gelmez oynaklığı berliler. Rehavet ortamı vardır" | T+G | 3.2 S ölçüm kolları (T R077 rehavet); 8: "Volatilite işi" satırı (R077 rejim/defansif); 4.5 | rejim | ölçüm kolu |
| R077 | rejim | yeşil üçgenler (nisan 2025 oynaklık sıçraması sonrası alım) | T+G | tasarımda yok (R077 yalnız rehavet cümlesiyle anılır; yeşil üçgen alımı yok) | rejim | kilit: Tansu kural/formül vermedi |
| R078 | portföy | "Şu rebalancing stratejisini öğrenin derim." | T+G | 8: Volatilite harvesti, rebalancing, Markowitz + volatilite trading (T R078) | portföy | ölçüm kolu |
| R078 | portföy | "gün sonu eklemeler eksiltmeler ile sistem getirisi 1.5 yada %27" | T+G | 8: Volatilite harvesti, rebalancing, ... (G R078 %26,76 / %27,81) | portföy | ölçüm kolu |
| R079 | formasyon | "Not alın işte süper brir yapı..." (haftalık AB=CD + talep + EMA) | T+G | 3.2 H (D = C − 1,0·(A−B), G R079); 4.1 (haftalık bölge) | formasyon | resmi sınav |
| R080 | formasyon | "peş peşe gelen lokal tepe ve dip noktaları tespit edilir" | T/M | 3.2 H (AB=CD; pivot 4.2) | formasyon | resmi sınav |
| R080 | formasyon | "BC ... AB uzunluğuna bölünür ... (0.382, 0.50, 0.618 vb.)" | T/M | 3.2 H (BC/AB alt sınırı 0,382, M R080; üst sınır 1,00 T R019 esas) | formasyon | resmi sınav |
| R080 | hedef-çıkış | "CD ... AB'nin uzunluğuna bölünür ... (1.00, 1.27, 1.618 vb.)" | T/M | 3.2 H (CD = AB resmi; 1,27 ölçüm kolu; 1,272·AB geçersizlik) | çıkış | resmi sınav |
| R080 | bölge | "D noktasına bakın, talep toplama bölgesine bakın, hissenin tepkilerine bakın. Doğru kod böyle yazılır." | T/M | 1 (hat 2, T R080); 3.2 akış 2 | bölge | resmi sınav |
| R081 | formasyon | "ABCD yi görüyor musun tam talep toplama bölgesinden haftalıkta tepkisini almış" | T+G | 3.2 H (G R081); 4.1 (haftalık bölge, T R081) | formasyon | resmi sınav |
| R081 | felsefe | "İşte bu yapıların peşindeyiz." | T+G | 1 (hat 2, T R081) | ilke | resmi sınav |
| R082 | teyit-tetik | "konoslidasyon ne kadar uzarsa kırılım o denli şiddetli oluyor" | T+G | 3.2 S ölçüm kolları (sıkışma süresi ile kırılım şiddeti raporu, T R082) | teyit | ölçüm kolu |
| R083 | tarama-evren | "Dolaşımdaki pay adedinin <%30 olduğu senetler ile ilgili çok tatlı stratejik taramalar" | T | 8: Fiili dolaşım < %30 (T R083); 3.1 ölçüm kolu | evren-likidite | ölçüm kolu |
| R083 | tarama-evren | "KAP ile verileri alabiliyoruz, sırada taramalar var." | T | 8: Fiili dolaşım < %30 (T R083); 2 (veri dipnotu) | evren-likidite | ölçüm kolu |
| R084 | formasyon | "Şimdi ne diyeyim yani buna:)" (BUY AB=CD, D "ALIM SİNYALİ - CD=1.0AB") | T+G | 3.2 H (AB=CD, G R084 "CD=1.0AB") | formasyon | resmi sınav |
| R085 | bölge | "gözü kapalı ABCD'ye nasıl güveneceksin kanalı okumadan iş yapılır mı?" | T+G | 1 (hat 2, T R085); 8: Kanal alt bandı, düşen direnç kırılımı + retest | bölge | ölçüm kolu |
| R085 | stop-geçersizlik | D noktasından aşağı ok, kanal altı çizgisi (RYSAS) | T+G | 8: Kanal alt bandı, düşen direnç kırılımı + retest (T R085) | çıkış | ölçüm kolu |
| R086 | teyit-tetik | "1-2 filtre ile enteresan bir breakout sinyali var aslında:) yeni keşfettim." | T+G | 3.2 S ölçüm kolları (sıkışma süresi ile kırılım şiddeti raporu, T R086 breakout) | teyit | ölçüm kolu |
| R087 | teyit-tetik | "Abcd analizine güvenip çaat diye alırsan ... Her zaman çalışmaz. İkinci alt grafiğe dikkat." | T+G | 6 (başarısız kurulumlar, R087 "Her zaman çalışmaz"); kümülatif delta kısmı 2: veri yok | teyit | resmi sınav |
| R087 | stop-geçersizlik | "BALAT / Düşen Direnci Kıran + Talep + Fibo + ABCD / Temas: 3 / Lookback: 30" | T+G | 8: Kanal alt bandı, düşen direnç kırılımı + retest (G R087) | çıkış | ölçüm kolu |
| R088 | — | GitHub kitap reposu önerisi (strateji içeriği yok) | bağlantı | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R089 | rejim | "Mavi çizgi sıfırı yukarı kestiği anda kırmızı bölgede oluşan yükselişler büyük oranda patır patır geri gelir." | T+G | 4.5 (fiyat + volatilite, T R089) | rejim | ölçüm kolu |
| R090 | formasyon | "Alış yönlü formasyon taranarak oluşmuş ABC yakalanır ve trident hedefi beklenerek teorik D noktasından yani dipten pozisyon alınır." | T+G | 3.2 H ölçüm kolları (Lindsay Trident hedefi, T R090 alış yönlü paragraf) | formasyon | ölçüm kolu |
| R090 | formasyon | "Satış yönlü formasyon taranarak ABC taratılır ... D noktasından sonra teorik olarak düşüş olacaktır." | T+G | 3.2 H ölçüm kolları (satış yönlü kural açığa satış olduğu için yok) | formasyon | kilit: açığa satış (BIST) |
| R090 | teyit-tetik | "D oluşumunu teyit etmek için ise B noktası kırılımı gerekir." | T+G | 3.2 H ölçüm kolları (B kırılımı teyidi) | teyit | ölçüm kolu |
| R090 | hedef-çıkış | "D = (B \* C) / A" (Lindsay Trident) | T+G | 3.2 H ölçüm kolları (D = (B·C)/A) | çıkış | ölçüm kolu |
| R090 | hedef-çıkış | "FIBO seviylerine göre iz süren takibe göre TP kovalanır." | T+G | 3.2 H ölçüm kolları (hedef merdiveni TP1–TP4) (kavram) | çıkış | ölçüm kolu |
| R090 | hedef-çıkış | "hedefi dinamik olarak kalibre ediyor ... otonom kâr alabiliyor" | M/A | 8: Kural taşımayan yan cümleler (dinamik hedef kalibrasyonu, R090 başka hesabın cevabı) | çıkış | kilit: Tansu kural/formül vermedi |
| R090 | felsefe | "artık strateji vs yazmıyorum. Zaten grafik açıklıyor herşeyi." | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R091 | rejim | "Trend rejim değişikliği için HMM yapmanıza gerek yok" (rolling korelasyon) | T | 4.5 (trend yönü: XU100 ile evren sepetinin rolling korelasyonu, T R091; seri ve pencere YORUM) | rejim | ölçüm kolu |
| R092 | rejim | "Fiyat ve volatilite aynı anda artması pek istenilen bir durum değildir" | T+G | 4.5 (T R092); 1 (hat 4) | rejim | ölçüm kolu |
| R092 | boyut-risk | "benden demesi sistemim pozisyonu kapatıp defansif pozisyoon aldı" | T+G | 4.5; 1 (hat 4); 8: "Volatilite işi" satırı (R092) | boyut-risk | ölçüm kolu |
| R093 | rejim | "sağlıklı yükseliş böyle olur, fiyat çıkarken alt panaldeki mavi çizgi de 0'ın altına iner" | T+G | 4.5 (T R093) | rejim | ölçüm kolu |
| R093 | felsefe | "Quant strateji farklı görmektir." | T+G | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R094 | rejim | "Piyasa yapıcının bize bir mesajı var:) KY sizi seviyorum diyor" (BIST100 / BIST_VOL gülümseme) | T+G | 8: Weinstein / DMA / piyasa evreleri / fat tail / BIST_VOL gülümsemesi / mal boşaltma-toplama satırı (T R094) | rejim | kilit: Tansu kural/formül vermedi |
| R095 | portföy | "CIMSA (X)" ve "OYAKC (Y)"; Z-Skoru ±2; "Relatif Momentum Portföyü" | G | 3.3 (giriş Z ±2 ve ΔZ dönüşü, G R095) | portföy | resmi sınav |
| R096 | tarama-evren | "eşbütünleşme testi iyi ihtimal ile 150.000 kombinasyon taramasına kadar çıkabilir" | T | 3.3 (aday çiftler: evrendeki tüm çiftler, T R096; sektör şartı kalktı: YORUM); 2.1 | evren-likidite | resmi sınav |
| R097 | boyut-risk | "garch ve standart sapma kullanarak volatiliteden kaynaklanan riski minimize etmenin yolunu" | T | 8: GARCH / ARIMA / ana frekans / finans mühendisliği / risk of ruin / kurtosis satırı (T R097) | boyut-risk | bilgi: işlem kuralı değil |
| R098 | teyit-tetik | "Stat-arb sisteminde momentum dönüş teyidi uygulamasının karlarda çarpan etkisine" | T | 3.3 (giriş ΔZ dönüşü; Tansu'nun "momentum dönüş teyidi" ile aynı olduğu YORUM, T R098) | teyit | resmi sınav |
| R099 | giriş | "Sistem Z-Skorunun +2'yi aştığını görüyor ve "AGROT SAT, GARAN AL"" | M | 3.3 (Z ±2 giriş; long-only: ucuz bacak, M/T R099) | giriş | resmi sınav |
| R099 | giriş | "Z-Skoru bu kez -2'yi kırıyor ... tüm bakiyesiyle yeni bir işleme giriyor" | M | 3.3 (Z ±2 giriş; boyut: tüm bölme sermayesi) | giriş | resmi sınav |
| R099 | hedef-çıkış | "Z-Skorunun ortalamaya (0.5) döndüğünü görüyor ve pozisyonu kapatıyor" | M | 3.3 (çıkış Z 0,5'e dönünce, M/T R101); 2.1 (5.6 Çift) | çıkış | resmi sınav |
| R099 | boyut-risk | "92.354 TL'lik tüm bakiyesiyle" | M | 3.3 (boyut: tüm bölme sermayesi, M/T R099) | boyut-risk | resmi sınav |
| R099 | ölçüm-ilkesi | "Mark-to-Market" | M | 8: Kural taşımayan yan cümleler (Mark-to-Market, M/T R099; rapor zaten kapanış değeriyle) | ölçüm-yöntemi | kilit: Tansu kural/formül vermedi |
| R099 | felsefe | "Sistem inatlaşmamış, kurala uyup çıkmış." | M | tasarim-8 4.4 çıkış zinciri (kurala bağlı çıkış); 3.3 (rolling kapı bozulursa çıkış) | ilke | ilke: tasarımın kuralı |
| R100 | stop-geçersizlik | "Her arbitraj fırsatı çalışmaz Mutlaka backtest etmek lazım Görünmez bağ kopmuş olabilir." | T+G | 3.3 (rolling kapı bozulursa çıkış, T R100) | çıkış | resmi sınav |
| R100 | ölçüm-ilkesi | "Mutlaka backtest etmek lazım" | T+G | TASARIM 2 (Sınamadan inanma); 5.11 deneme günlüğü; 5.12 kabul ölçütü | ilke | ilke: tasarımın kuralı |
| R101 | tarama-evren | "Eğer bu iki varlık gerçekten birbiriyle eşbütünleşik (cointegrated) ise" | T/M | 3.3 (kapı: rolling eşbütünleşme) | evren-likidite | resmi sınav |
| R101 | giriş | "Eğer Z-Skoru +2.0 seviyesini yukarı kırarsa ... Aşırı Ucuzlayanı AL (Long)" | T/M | 3.3 (Z ±2 giriş) | giriş | resmi sınav |
| R101 | hedef-çıkış | "Fark kapanıp Z-Skoru normale (0.5 seviyelerine) döndüğünde, pozisyonları kapatır" | T/M | 3.3 (çıkış Z 0,5, M/T R101) | çıkış | resmi sınav |
| R101 | stop-geçersizlik | "Yanıldığını anladığı an zararı keser." | T/M | 3.3 (rolling kapı bozulursa çıkış, M/T R101) | çıkış | resmi sınav |
| R101 | felsefe | "Borsada "yönü" bilmek zorunda değilsiniz." | T/M | 3.3 (yönsüz işlem; long-only rotasyon yalnız yaklaşır) | ilke | kilit: açığa satış (BIST) |
| R102 | felsefe | "Arbitraj her zaman en en sevdiğim 2 sistemden birisi İlki volatilite işi İkincisi de arbitraj" | T+G | 1 (hat 3); 3.3; volatilite işi için 8: "Volatilite işi" satırı (parçalı) | evren-likidite | resmi sınav |
| R103 | felsefe | "Bizim "grafik" dediğimiz şeye onlar binlerce satırlık bir veri seti" | M | 8: Felsefe ve ölçüm ilkeleri (kavram) | araç-öğrenme | bilgi: işlem kuralı değil |
| R103 | felsefe | "Fibonacci seviyelerinden ziyade; piyasa likiditesini, emir defterindeki dengesizlikleri" | M | rakip yöntem anlatımı | araç-öğrenme | bilgi: işlem kuralı değil |
| R103 | felsefe | "İndikatör cart curt bizim zamanımızda kaldı. Kod öğrenin" | T | 8: Felsefe ve ölçüm ilkeleri (kavram) | araç-öğrenme | bilgi: işlem kuralı değil |
| R104 | felsefe | "Profesyoneller tahminlerle değil, stratejilerle hareket eder." | M | TASARIM 1 (P1: sistem emir vermez, "kural sağlandı" der); 5.12 (kabul ölçütü önceden yazılır) | ilke | ilke: tasarımın kuralı |
| R104 | felsefe | "Usta İşi İfadeler: "Yüksek olasılıklı bir formasyon", "Risk-ödül oranı uygun"" | M | tasarim-8 3.2 adım 4 (ödül/risk kapısı, < 1,5 girilmez) | ilke | ilke: tasarımın kuralı |
| R105 | momentum-seçim | "Arkadaşlar ortalama kullanıyor iseniz eğimlere dikkt edeceksiniz." | T | 3.1 ölçüm kolu (eğim kapısı, T R137, R105) | seçim-momentum | ölçüm kolu |
| R105 | momentum-seçim | "Momentum (Hız), değerden (Fiyat veya Gösterge) önce döner." | M | 3.1 ölçüm kolu (eğim kapısı) (kavram) | seçim-momentum | ölçüm kolu |
| R105 | teyit-tetik | "bir ortalamanın eğimi onun birinci türevidir ... eğimin yön değiştirmesi bir erken uyarı" | M | 3.1 ölçüm kolu (eğim kapısı) (kavram) | teyit | ölçüm kolu |
| R105 | giriş | "Kesişim gerçekleştiğinde fiyat genellikle %5-%10 primlenmiş olur." | M | 8: Mum ve gösterge yorumları (%5–10 kesişim primi, M R105) | giriş | kilit: Tansu kural/formül vermedi |
| R105 | teyit-tetik | "uzun vadeli ortalamanın da eğimi pozitife dönmüşse" | M | 3.1 ölçüm kolu (eğim kapısı) (kavram) | teyit | ölçüm kolu |
| R106 | felsefe | "Ortalama (aritmetik ortalama), verideki en buyuk yalanci ve en kirilgan yapidir." | T/M | 8: Medyan temelli çalışma, medyan kanal (kavram, T R001) | ölçüm-yöntemi | ölçüm kolu |
| R106 | ölçüm-ilkesi | "n degeri ne kadar kucukse ... bu yalan o kadar buyuk olur." | T/M | 8: Medyan temelli çalışma, medyan kanal (kavram, T R001) | ölçüm-yöntemi | ölçüm kolu |
| R107 | bölge | "Finans mühendisliği modelleri destek ve direnç seviyelerini bulmak için kullanılır mı?" | T | 8: GARCH / ARIMA / ana frekans / finans mühendisliği / risk of ruin / kurtosis satırı (T R107) | bölge | bilgi: işlem kuralı değil |
| R108 | rejim | "Evre 1: Taban/Birikim ... Evre 2: Yükseliş/Boğa ... Evre 4: Düşüş/Ayı" | M | 8: Weinstein / DMA / piyasa evreleri / fat tail / BIST_VOL gülümsemesi / mal boşaltma-toplama satırı (M R108) | rejim | kilit: Tansu kural/formül vermedi |
| R109 | felsefe | "Asla kalem kağıt kullanmadan sistem yazmam, bunu huy edinin bence." | T | TASARIM başı (belge koddan önce gelir, kod belgeye uyar); tasarim-8 başı (kod bu belgeden önce yazılmaz) | ilke | ilke: tasarımın kuralı |
| R109 | felsefe | "Eğer AI kullanıyor iseniz bunu yapmanız bir zorunluluk." | T | TASARIM başı (belge koddan önce gelir, kod belgeye uyar); tasarim-8 başı (kod bu belgeden önce yazılmaz) | ilke | ilke: tasarımın kuralı |
| R110 | tarama-evren | "Düşük Korelasyon: ... Yüksek Volatilite: Portföye girecek hisselerin "hareketli" olması" | T/M | 8: Volatilite harvesti, rebalancing, Markowitz + volatilite trading (T/M R110) | evren-likidite | ölçüm kolu |
| R110 | portföy | "Seçilen 10-20 hisselik aday listesi, Modern Portföy Teorisi (Markowitz)" | T/M | 8: Markowitz + volatilite trading (T/M R110); 3.1 ölçüm kolu | portföy | ölçüm kolu |
| R110 | portföy | "Sharpe Oranı Optimizasyonu: ... Max Sharpe "Teğet Portföy"" | T/M | 3.1 ölçüm kolu (Max Sharpe, T/M R110) | portföy | ölçüm kolu |
| R110 | boyut-risk | "en verimli 3 ile 10 arası hisse, nihai trade listesine alınır" | T/M | 3.1 ölçüm kolu (3–10 hisse, T/M R110) | boyut-risk | ölçüm kolu |
| R110 | boyut-risk | "4. Sistemin üzerine inşaa edilecek hissenin oranı %50 den fazla olmalıdır." | T/M | 8: Mum ve gösterge yorumları ("hissenin oranı %50'den fazla", M R110, belirsiz) | boyut-risk | kilit: Tansu kural/formül vermedi |
| R110 | giriş | "RSI, Bollinger Bandı veya Mean Reversion modelleri ile ... iç dalgalanmalarından kar" | T/M | 8: Markowitz + volatilite trading (T/M R110) | giriş | ölçüm kolu |
| R110 | portföy | "Markowitz ağırlıkları korunurken ... "Alpha" yaratılır." | T/M | 8: Markowitz + volatilite trading (T/M R110) | portföy | ölçüm kolu |
| R111 | felsefe | "kendinize has, özgün bir yapı kurmaktan geçer" (model sentezi) | T | tasarim-8 başlık notu (P5) ve 3: farklı modellerin sentezi (momentum + bölge + formasyon + çift); TASARIM P5 | ilke | ilke: tasarımın kuralı |
| R111 | ölçüm-ilkesi | "sabırla backtest ve forward test süreçlerini yönetmeniz gerekir" | T | TASARIM 2 (Sınamadan inanma); 5.11 deneme günlüğü; 5.12 kabul ölçütü | ilke | ilke: tasarımın kuralı |
| R111 | felsefe | "kurduğunuz kod mimarisi başarınızın asıl anahtarıdır" | T | tasarim-8 5.2 (her yeni kod hash'i için boru hattı denetimi; olcum.py ayrı) | ilke | ilke: tasarımın kuralı |
| R112 | portföy | "Portföy yönetimi e getiri hesaplamak geriye doğru simülasyonlar önemlidir" | T+G | 3.1 ölçüm kolu (tek hisse ağırlık duyarlılığı, T R112) | portföy | ölçüm kolu |
| R112 | portföy | "TEKTU ağırlığı artıkça portföy getirisi doğrusal artıyor" | T+G | 3.1 ölçüm kolu (tek hisse ağırlık duyarlılığı, T R112) | portföy | ölçüm kolu |
| R112 | portföy | "Mevcut %30 TEKTU / %20 EREGL dağılımın EREGL tarafı portföyü baskılıyor." | T+G | 3.1 ölçüm kolu (tek hisse ağırlık duyarlılığı, T R112) | portföy | ölçüm kolu |
| R113 | portföy | "Portföy optimizasyonu ve volatilite trading arasındaki ilişki huzurlu gecelerin anahtarıdır." | T | 8: Markowitz + volatilite trading (kavram) | portföy | ölçüm kolu |
| R114 | formasyon | "Fincan Oluşumu (Mavi Çizgi) ... Fibo 100% ... 317.00 (Fibo 0%)" | T+G | 8: Fincan-kulp (T/M R114) | formasyon | kilit: Tansu kural/formül vermedi |
| R114 | formasyon | "Kulp ... Fibonacci 61.8% (252.23) ve 50% (264.60) bölgesi" | T+G | 8: Fincan-kulp | formasyon | kilit: Tansu kural/formül vermedi |
| R114 | teyit-tetik | "300.75 seviyesindeki yeşil kesik çizgiyi (KIRILMA) yukarı kesiyor" | T+G | 8: Fincan-kulp (GUBRF 2025-10-24 kırılımı sadakat hedefi olarak saklanır) | teyit | kilit: Tansu kural/formül vermedi |
| R114 | hedef-çıkış | "Fincan derinliği kadar yukarı gitme mantığına dayanan formasyon hedefimizi" (389.30) | T+G | 8: Fincan-kulp (hedef tabanı çelişkili: 389,30 − 104,80 = 284,50) | çıkış | kilit: Tansu kural/formül vermedi |
| R114 | boyut-risk | "1:2.27 Risk/Reward (Risk-Ödül) oranı sunuyor." | T+G | 8: Fincan-kulp | boyut-risk | kilit: Tansu kural/formül vermedi |
| R114 | felsefe | "doğru formasyonu doğru seviyede, sıfır duyguyla ve tam zamanında yakalamak" | T+G | TASARIM 1 (P1); tasarim-8 1 (hat 2: formasyon bölgesiz kullanılmaz) | ilke | ilke: tasarımın kuralı |
| R115 | ölçüm-ilkesi | "Stratejimiz, ham getiriden bir miktar feragat ederek ... çok daha huzurlu bir eğri" | T+G | 6 (sermaye eğrisinin sakinliği, T/M R115) | ölçüm-yöntemi | resmi sınav |
| R115 | ölçüm-ilkesi | "volatiliteyi %33'ten %23'e çekmesi ... Sharpe oranlarının aynı olması" (B&H kıyası) | T+G | 6 (yıllık volatilite ve en büyük düşüş, kural ile K2 yan yana, T/M R115) | ölçüm-yöntemi | resmi sınav |
| R116 | teyit-tetik | "diplerin yükseldiğini ... diplerin aşağı kaydığını" (gizli pozitif uyumsuzluk) | T/M | 8: Gizli pozitif uyumsuzluk (T/M R116) | teyit | kilit: Tansu kural/formül vermedi |
| R116 | rejim | "Teknik olarak biz buna trend devam sinyali diyoruz." | T/M | 8: Gizli pozitif uyumsuzluk (T/M R116) | rejim | kilit: Tansu kural/formül vermedi |
| R117 | teyit-tetik | "Gizli uyumsuzlukları takip ediniz, arkadaşça hatırlatma." | T+G | 8: Gizli pozitif uyumsuzluk (T R117) | teyit | kilit: Tansu kural/formül vermedi |
| R118 | rejim | "ADX (28.9) ve RSI (77.6) ... VIX (20.6)" (trend skoru 5/5) | M | 2 (VIX yok); 8: BIST100 + VIX beş adım (kavram) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R118 | rejim | "Kısa Vade (20 Günlük): 83 puan ... "Katılım Yok" uyarısı" (NH-NL) | M | 4.5 (piyasa genişliği: 20 ve 65 günlük NH-NL, M R118; 2.1) | rejim | ölçüm kolu |
| R118 | rejim | "Endeks bazında ortalama spread %1.06" | M | 4.5 (Corwin–Schultz, T/M R119); 2.1 (kavram) | rejim | ölçüm kolu |
| R118 | rejim | "Düşük Hacim uyarısı" | M | 8: Kural taşımayan yan cümleler (düşük hacim uyarısı, M R118) | rejim | kilit: Tansu kural/formül vermedi |
| R118 | giriş | "Hacim Teyidi Bekleyin: Hacim barlarında belirgin bir artış" | M | 8: Hacim teyidi (kavram) | giriş | ölçüm kolu |
| R118 | giriş | "Sigma ani bir sıçrama görmediğimiz sürece, mevcut trendin tadını çıkarmaya devam edebiliriz." | M | 4.5 (Corwin–Schultz spread ve sigma) | giriş | ölçüm kolu |
| R118 | giriş | "Liderleri Takip Edin: XU100 spread'i düşük ve stabil olduğu için" | M | 8: Kural taşımayan yan cümleler ("Liderleri Takip Edin", M R118) | giriş | kilit: Tansu kural/formül vermedi |
| R118 | rejim | "Mikro-Makro Çelişkisi: XU100 spread'i dar olmasına rağmen ... Düşük Hacim uyarısı" | M | 8: Kural taşımayan yan cümleler (mikro-makro çelişkisi, M R118) | rejim | kilit: Tansu kural/formül vermedi |
| R119 | rejim | "En Yüksek ve En Düşük fiyatlar üzerinden piyasanın "arka planını"" (Corwin-Schultz) | T/M | 4.5 (Corwin–Schultz; yüksek/düşük ile hesaplanır); 2.1 | rejim | ölçüm kolu |
| R119 | rejim | "Spread yüksek, Sigma yüksekse; o tahtadan uzak durun" | T/M | 4.5 (Corwin–Schultz, T/M R119) | rejim | ölçüm kolu |
| R119 | giriş | "spread'in tekrar ortalamaya (%1.79) dönmesini beklemek gerekir" | T/M | 4.5 (Corwin–Schultz) (kavram) | giriş | ölçüm kolu |
| R119 | giriş | "Hacim (Volume) ile korele edip ... "mal boşaltma" mı yoksa "toplama" mı" | T/M | 8: Weinstein / DMA / piyasa evreleri / fat tail / BIST_VOL gülümsemesi / mal boşaltma-toplama satırı (T/M R119) | giriş | kilit: Tansu kural/formül vermedi |
| R119 | rejim | "Sigma'nın zıpladığı her yerde Spread de onu takip ederek yukarı kafa atıyor." | T/M | 4.5 (Corwin–Schultz) | rejim | ölçüm kolu |
| R119 | rejim | "Spread'in %7 civarına fırladığı bir bölge var." | T/M | 4.5 (Corwin–Schultz) | rejim | ölçüm kolu |
| R119 | rejim | "Ocak ayı boyunca ... Spread (Kırmızı) genel olarak ortalamanın altında seyrediyor." | T/M | 4.5 (Corwin–Schultz) | rejim | ölçüm kolu |
| R119 | rejim | "Tahtanın tekrar dolması, stabil bir trend için şart." | T/M | 4.5 (Corwin–Schultz) | rejim | ölçüm kolu |
| R120 | momentum-seçim | "Her ay için her hissenin son 12 aydaki getirisini hesapladım ... 10 eşit gruba böldüm." | T+G | 3.1 S1 | seçim-momentum | resmi sınav |
| R120 | portföy | "bir sonraki ay o gruptaki hisseleri eşit ağırlıkla tuttuğumu varsaydım" | T+G | 3.1 S1 | portföy | resmi sınav |
| R120 | tarama-evren | "2015'ten bugüne BIST'teki 500'den fazla hissenin fiyat verisini çektim." | T+G | 1 (hat 1); 3.1 S1 (evren ilk 100, YORUM); geniş evren ölçüm kolu | evren-likidite | resmi sınav |
| R120 | ölçüm-ilkesi | "işlem maliyetleri, vergiler ve likidite sorunu olan hisseler hesaba katılmadı" | T+G | 3.1 S1 (masraf %0,3, likidite %2) | ölçüm-yöntemi | resmi sınav |
| R120 | ölçüm-ilkesi | "En iyi momentum grubundaki hisseler diğer tüm grupları geride bıraktı." | T+G | 3.1 S1 (hipotez) | ölçüm-yöntemi | resmi sınav |
| R121 | momentum-seçim | "kodum optimal momentum+ portföyü için simülasyon yapıyor" | T | 8: YSA momentumu / Optimal Momentum+ / pre-signal / gizli "xxxx" metriği satırı (T R121) | seçim-momentum | kilit: Tansu kural/formül vermedi |
| R122 | felsefe | "Öyle bir matematiksel yapı kurun ki sistem sürekli kendini yenilesin." | T/M | 5.2 "Kendini yenileyen sistem" (önceden yazılmış yıllık walk-forward ayar seçimi; S1 aylık, S3 yıllık zaten yenilenir) | ilke | ölçüm kolu |
| R122 | felsefe | "sisteminizle, o karmaşanın içindeki "ana frekansı" yakalamaya çalışın." | T/M | 8: GARCH / ARIMA / ana frekans / ... satırı (T/M R122) | ölçüm-yöntemi | bilgi: işlem kuralı değil |
| R122 | felsefe | "hata payını minimize eden o kusursuz matematiğin peşinde olun" | T/M | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R122 | felsefe | "her döngüde daha güçlü hale gelen ... siz sistemin kendisi olursunuz" | T/M | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R123 | — | Stefan Jansen kitap/yazar önerisi (strateji içeriği yok) | T | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R124 | teyit-tetik | "fiyatın bu çizgiyi sert bir şekilde yukarı kırdığını görüyoruz" | M | 8: Kanal alt bandı, düşen direnç kırılımı + retest (kavram) | teyit | ölçüm kolu |
| R124 | bölge | "Talep Bölgesi (Yeşil Yatay Kutu) ... Fiyat bu bölgeye girdiğinde her seferinde destek bulmuş." | M | 3.2 akış 2 (kavram) | bölge | resmi sınav |
| R124 | teyit-tetik | "Hacimli kırılım, gerçek kırılımdır kuralı" | M | 8: Hacim teyidi ("Hacimli kırılım", M R124) | teyit | ölçüm kolu |
| R124 | teyit-tetik | "Hareketli Ortalamalar (EMA 5, 8, 13) ... Boğa Dizilimi" | M | 3.2 S ölçüm kolları (kırılım sonrası boğa dizilimi EMA5 > EMA8 > EMA13, M R124) | teyit | ölçüm kolu |
| R124 | teyit-tetik | "En sağdaki uzun yeşil mum ... o günü en yüksek seviyeye yakın kapattığını" | M | 8: Mum ve gösterge yorumları (uzun yeşil mumun yüksek yakın kapanışı, M R124) | teyit | kilit: Tansu kural/formül vermedi |
| R125 | formasyon | "Ema sıkışması parametrelerin detaylarını verip stratejimi anlatamam" | T+G | 3.2 S (G R125; ölçüm kolu EMA30/50/100/200 ICBCT) | formasyon | resmi sınav |
| R125 | teyit-tetik | "Pre signal ok ile işaretlenen mum matrix ekranında" | T+G | 8: YSA momentumu / Optimal Momentum+ / pre-signal oku / "xxxx" satırı (T R125) | teyit | kilit: Tansu kural/formül vermedi |
| R126 | bölge | "düşüşün 0.786 düzeltme seviyesine (yaklaşık ₺31.00)" | T/M | 8: Mum ve gösterge yorumları (0,786'nın direnç olarak kullanımı, M R126) | bölge | kilit: Tansu kural/formül vermedi |
| R126 | bölge | "POC (Point of Control): ₺29.71 ... VAH (Value Area High - ₺30.24)" | T/M | 8: VWAP / POC / VAH / VAL (kavram) | bölge | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R126 | bölge | "VWAP ... ₺28.00'ın (VWAP) %+10.73 üzerindedir" | T/M | 8: VWAP / POC / VAH / VAL (kavram) | bölge | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R126 | teyit-tetik | "+DI ... -DI ... DMI" ve "Delta ve Kümülatif Delta" | T/M | 2 (kümülatif delta yok) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R127 | formasyon | "sıkışma zamanlarını iyi tespit eder ve yakalarsanız hele ki bir de o alanda formasyon vs varsa" | T+G | 3.2 S (T R127) | formasyon | resmi sınav |
| R127 | formasyon | "Rasyoyu siz belirleyeceksiniz"; "Tolerans %1.2 / Min 3 gün" | T+G | 3.2 S (tolerans %1,2, min 3 gün; EMA 20/50/100/200 ölçüm kolu, G R127); 5.1 (KRDMD) | formasyon | resmi sınav |
| R128 | formasyon | "neredeyse iç içe geçtiğini ... Yay ne kadar çok gerilirse, ok o kadar uzağa gider." | M | 3.2 S (kavram: sıkışma) | formasyon | resmi sınav |
| R128 | bölge | "11.300 seviyelerindeki KDE tepe dirençlerini hacimli mumlarla geçmesiyle patlama" | M | 4.1 (ölçüm: KDE fiyat yoğunluk seviyeleri, M R128) | bölge | ölçüm kolu |
| R128 | teyit-tetik | "EMAs'ların birbirini keserek yukarı yönlü "Boğa Dizilimi"ne girmesidir" | M | 3.2 S ölçüm kolları (boğa dizilimi teyidi, M R128) | teyit | ölçüm kolu |
| R128 | rejim | "EMAs'lar artık birer direnç değil, güçlü birer dinamik destek haline gelmiştir." | M | 8: Kural taşımayan yan cümleler (EMA'ların dinamik desteğe dönmesi, M R128) | rejim | kilit: Tansu kural/formül vermedi |
| R128 | teyit-tetik | "hacim barlarının son dönemde yükselmiş olması ... taze para girişi" | M | 8: Hacim teyidi (kavram) | teyit | ölçüm kolu |
| R128 | hedef-çıkış | "fiyat ortalamalardan çok uzaklaştığında bir soğuma, yatay seyir veya ... re-test" | M | tasarımda yok (ortalamadan uzaklık ve soğuma cümlesi) | çıkış | kilit: Tansu kural/formül vermedi |
| R129 | bölge | "Açık yeşil alan (Bullish FVG) ... bir "mıknatıs" ve "denge" bölgesidir." | T/M | 4.2 (FVG) (kavram) | bölge | resmi sınav |
| R129 | giriş | "bu yeşil alan "Optimal Trade Entry" (OTE) dediğimiz en verimli alım bölgesi olacaktır." | T/M | 3.2 E (M R197 OTE 0,618–0,786, kavram) | giriş | resmi sınav |
| R129 | teyit-tetik | "alt zaman dilimlerinde (1H veya 4H) bir karakter değişimi (CHoCH) görmeden doğrudan long pozisyon almak riskli" | T/M | 4.2 (1H/4H CHoCH teyidi, M R129: gün içi veri yok) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R129 | teyit-tetik | "BOS (Break of Structure) ... EMA 9, 21, 50, 100, 200 üzerine" | T/M | 4.2 (BOS, M R129; EMA üstü kısmı atıfsız) | teyit | resmi sınav |
| R129 | bölge | "FVG'ler bazen sadece birer durak değil, fiyatın altına sarkıp altındaki likiditeyi temizlemek istediği yerler" | T/M | 8: Kural taşımayan yan cümleler (likidite süpürme, M R129) | bölge | kilit: Tansu kural/formül vermedi |
| R129 | bölge | "Fiyat önce yukarıdaki dirençleri test edip likidite topladıktan sonra bu açık hesabı kapatmak isteyecektir." | T/M | 8: Kural taşımayan yan cümleler (önce üst dirençleri test, M R129) | bölge | kilit: Tansu kural/formül vermedi |
| R129 | bölge | "Grafikteki yeşil alanın konumu, fiyatın uzun vadeli ana destek bölgesiyle de örtüşüyor." | T/M | 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi (kavram) | bölge | ölçüm kolu |
| R130 | stop-geçersizlik | "arkanıza bakmadan kaçmanız gereken mum gravestone doji" | T+G | 8: Mum formasyonları (gravestone, T R130) | çıkış | ölçüm kolu |
| R131 | rejim | "eğer piyasa hareketli ortalamanın altındaysa ... satış yönlü; ... üzerindeyse, alış yönlü" | T | 4.5 (trend yönü: XU100 ortalamanın üstü/altı, T R131); 3.2 akış 1 (SMA250 kapısı) (kavram) | rejim | ölçüm kolu |
| R131 | felsefe | "Konu bundan ibarettir. Trend is your friend." | T | 4.5 (trend yönü, T R131 "Trend is your friend") | rejim | ölçüm kolu |
| R132 | formasyon | "dragonfly doji ile ... Ortalamalar kesişmiş vs vs sıkışma alanından da çıkmış" | T+G | 2 (doji: mum formasyonu yalnız ölçülür); 3.2 S (sıkışma kısmı) | formasyon | ölçüm kolu |
| R133 | temel-değerleme | "Bana kalırsa bu hisse ilk çeyrek bilançosunun açıklanmasını bekliyor." | T+M+G | 8: Bilanço kalite filtreleri (HBK U dönüşü, T R133) (kavram) | değerleme-temel | kilit: bilanço verisi |
| R133 | temel-değerleme | "hissenin FK'sı zaten ortalamalarda, güzel bir U dönüş görünüyor" (HBK) | T+M+G | 8: Bilanço kalite filtreleri (HBK U dönüşü, T R133) | değerleme-temel | kilit: bilanço verisi |
| R133 | felsefe | "Formüller burada bir tercüman görevi görür." | T+M+G | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R133 | temel-değerleme | "O yüzden HBK evrensel bir cevap sunar." | T+M+G | 8: Kural taşımayan yan cümleler (HBK'nın evrensel ölçü olması, T R133) | değerleme-temel | kilit: Tansu kural/formül vermedi |
| R134 | temel-değerleme | "Eğer borç artarken aynı zamanda Maddi Duran Varlıklar kalemi de artıyorsa" | M+G | 8: Bilanço kalite filtreleri (borç büyümesi vs ciro, M R134) | değerleme-temel | kilit: bilanço verisi |
| R134 | temel-değerleme | "Borç %84 artarken ciro %100 artıyorsa, bu sağlıklı bir büyümedir." | M+G | 8: Bilanço kalite filtreleri (M R134) | değerleme-temel | kilit: bilanço verisi |
| R134 | temel-değerleme | "ASUZU'nun borç büyümesi %83 iken rakiplerinde (FROTO, TOASO) bu oran %20 ise" (metin–görsel çelişkisi: görselde FROTO +0,7%, TOASO +47,0%) | M+G | 8: Bilanço kalite filtreleri (M R134) | değerleme-temel | kilit: bilanço verisi |
| R134 | temel-değerleme | "Özkaynak / Borç Dengesi: Borç artarken özkaynaklar yerinde sayıyorsa" | M+G | 8: Bilanço kalite filtreleri (M R134) | değerleme-temel | kilit: bilanço verisi |
| R134 | temel-değerleme | "Bu şirket borç aldığı parayla, borcun maliyetinden daha fazla para kazanabiliyor mu?" | M+G | 8: Bilanço kalite filtreleri (M R134) | değerleme-temel | kilit: bilanço verisi |
| R134 | felsefe | "Python kullanmak, binlerce satırlık bilanço verisini saniyeler içinde" | M+G | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R135 | temel-değerleme | "def borc\_buyume\_hesapla(guncel\_borc, onceki\_borc)" | T | 8: Bilanço kalite filtreleri (borç büyümesi, T R135) | değerleme-temel | kilit: bilanço verisi |
| R136 | teyit-tetik | "gizli pozitif uyumsuzlukların gücü tabi nerede baktığınıza bağlı" | T+G | 8: Gizli pozitif uyumsuzluk (T R136) | teyit | kilit: Tansu kural/formül vermedi |
| R137 | diğer | "Bu sistem satılık değil arkadaşlar önce onu belirteyim." | T | 1 (hat 1) | ürün-hedefi | bilgi: işlem kuralı değil |
| R137 | felsefe | "veriyi farklı süzgeçlerden geçirerek rafine eden çok aşamalı bir karar destek mekanizması" | T | 1 (hat 1); 3.1 ölçüm kolları | seçim-momentum | ölçüm kolu |
| R137 | momentum-seçim | "yapay sinir ağları ile oluşturduğum bir momentum stratejim var" | T | 3.1 (YSA ve gizli; yerine R120 ölçüsü); 8: YSA momentumu satırı | seçim-momentum | kilit: Tansu kural/formül vermedi |
| R137 | momentum-seçim | "hem fiyatın hem de oluşan sinyalin eğimi ni kontrol ediyorum" | T | 3.1 ölçüm kolu (eğim kapısı, T R137) | seçim-momentum | ölçüm kolu |
| R137 | teyit-tetik | "ADX ve Para Akışı (CMF) ... 'Çekiç' veya 'Sabah Yıldızı'" | T | 3.1 ölçüm kolu (teknik onay: ADX > eşik ve CMF > 0; çekiç/sabah yıldızı AOF vekiliyle) | teyit | ölçüm kolu |
| R137 | portföy | "4. Aşama: Markowitz Portföy Optimizasyonu" | T | 1 (hat 1); 3.1 ölçüm kolu | portföy | ölçüm kolu |
| R137 | portföy | "5. Aşama: Maksimum Sharpe Seçimi (Final Kararı)" | T | 3.1 ölçüm kolu (Max Sharpe 3–10 hisse) | portföy | ölçüm kolu |
| R137 | felsefe | "en dengeli takımı nasıl kurarım sorusuna yanıt vererek bilimsel bir yatırım planı" | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R138 | giriş | "sadece belirgin trendleri (AD > EMA) toplamanın hikayesidir" | M+T+G | 8: RSI 30 / Williams %R / APO / A/D–EMA3 / HalfTrend / ML lojistik satırı (A/D–EMA3, M/T R138) | giriş | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R138 | ölçüm-ilkesi | "geceleri huzurlu uyumanızı sağlayan şey Sharpe değil, kümülatif getiri grafiğindeki o sakinliktir" | M+T+G | 6 (sermaye eğrisinin sakinliği, M/T R138: gövde M, son cümle T) | ölçüm-yöntemi | resmi sınav |
| R138 | boyut-risk | "piyasa kan ağlarken sizi nakitte tutarak sermayenizi bir kalkan gibi korumuş" | M+T+G | 8: A/D–EMA3 (kavram) | boyut-risk | kilit: Tansu kural/formül vermedi |
| R138 | felsefe | "piyasada Haklı çıkmak bir ego tatminidir, ancak sermayeyi korumak bir hayatta kalma becerisidir." | M+T+G | tasarim-8 4.4 boyut (%1 risk, 2 ATR acil stop); TASARIM 2 (Önce sermaye) | ilke | ilke: tasarımın kuralı |
| R138 | ölçüm-ilkesi | "EMA değeri walk forward le optimzie edilerek model oluşturulmuştur." | M+T+G | 8: A/D–EMA3 (M/T R138) | ölçüm-yöntemi | kilit: Tansu kural/formül vermedi |
| R139 | giriş | "Enter long: AD() Ref(Mov(AD(),opt1,E), 1) ... OPT1 Current value: 3" | T | 8: A/D–EMA3 (R139'da operatör eksik) | giriş | kilit: Tansu kural/formül vermedi |
| R139 | diğer | "Çatır çutur girip çıkmak için, 1-2 gün" | T | 8: A/D–EMA3 (kavram) | giriş | kilit: Tansu kural/formül vermedi |
| R140 | ölçüm-ilkesi | "Yüzdelik doğruluk ..., acemi yatırımcıların bir takıntısıdır" | M/A | 6 (kazanma oranı tek ölçüt değildir, M R140) | ölçüm-yöntemi | resmi sınav |
| R140 | ölçüm-ilkesi | "temel performans ölçütü, toplam net kârın maksimum sermaye erimesine oranıdır" | M/A | 6 (net kâr / en büyük düşüş, M R140) | ölçüm-yöntemi | resmi sınav |
| R140 | ölçüm-ilkesi | "erimeler diğer indikatörlerin erimeleriyle karşılaştırıldığında şiddetliyse, o işlem sistemini bir kenara bırakmalı" | M/A | 6 (kavram) | ölçüm-yöntemi | resmi sınav |
| R140 | felsefe | "Basit tut hala verilebilecek en iyi tavsiyedir." | M/A | TASARIM 2 (Basit ve sağlam: medyan, sağlamlık sınaması) | ilke | ilke: tasarımın kuralı |
| R141 | — | "Awesome Econ AI Stuff" kaynak tanıtımı (strateji içeriği yok) | A | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R142 | — | ekonometri yöntem haritası: "13 blok, 81 soruluk bir harita" (strateji içeriği yok) | A | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R143 | formasyon | "Upper Shadow ... Lower Shadow ..." (üst/alt gölge formülleri) | M+T+G | 2 (açılış yok); 8: Mum formasyonları (kavram) | formasyon | ölçüm kolu |
| R143 | formasyon | "Aşağıdaki kodu kullan geliştir formasyonları tanımla vs vs" | M+T+G | 8: Mum formasyonları (kavram) | formasyon | ölçüm kolu |
| R144 | temel-değerleme | "PD/DD ... şirketin özkaynaklarını ne kadar verimli kullandığını gösteren bir sağlamlık filtresi" | M+T | 8: Momentum × faaliyet nakit akışı 5×5 / TOPSIS / DEA / PD/DD+ROE satırı (M R144) | değerleme-temel | kilit: bilanço verisi |
| R144 | temel-değerleme | "Tarihsel Ortalamalar: Şirket son 36 çeyrekte ..." | M+T | 8: PD/DD+ROE (M R144) | değerleme-temel | kilit: bilanço verisi |
| R144 | temel-değerleme | "36 çeyreklik (uzun dönem) ortalamayı bir 'çıpa' noktası olarak alıp" | M+T | 8: PD/DD+ROE (M R144) | değerleme-temel | kilit: bilanço verisi |
| R144 | temel-değerleme | "'PD/DD oranı 1'in altında, o halde bu hisse bedava' diyerek alım yapmak büyük bir hatadır" (değer tuzağı) | M+T | 8: PD/DD+ROE (M R144) | değerleme-temel | kilit: bilanço verisi |
| R144 | temel-değerleme | "Düşük PD/DD + Yüksek Özkaynak Karlılığı + Sektör Altı Çarpan = Potansiyel Yıldız." | M+T | 8: PD/DD+ROE (M R144) | değerleme-temel | kilit: bilanço verisi |
| R144 | temel-değerleme | "Teknoloji ve Yazılım: ... PD/DD genellikle çok yüksek çıkar" | M+T | 8: PD/DD+ROE (M R144) | değerleme-temel | kilit: bilanço verisi |
| R145 | momentum-seçim | "Topsis analizinin deneysel sonuçları inanılmaz. İndikatör cart curt hikaye. Topsis yapın." | T | 8: TOPSIS (T R145) | seçim-momentum | kilit: bilanço verisi |
| R146 | temel-değerleme | "full\_year\_beklenti = onceki\_yil\_satis(2022/12) × (1 + 1.88)" | T | 8: Değerleme sistemi (basit model) (kavram) | değerleme-temel | kilit: bilanço verisi |
| R146 | temel-değerleme | "kalan\_donem\_satis = full\_year\_beklenti - ytd\_satis" | T | 8: Değerleme sistemi (basit model) (kavram) | değerleme-temel | kilit: bilanço verisi |
| R146 | temel-değerleme | "tahmini\_net\_kar = kalan\_donem\_satis × NET\_KAR\_MARJI + ytd\_net\_kar" | T | 8: Değerleme sistemi (basit model) (kavram) | değerleme-temel | kilit: bilanço verisi |
| R147 | temel-değerleme | "doğrudan şirketin faaliyet hacmine (adet/ton) inen 'aşağıdan yukarıya' (bottom-up) bir sistem mimarisi" | T+M+G | 8: Değerleme sistemi (kavram: adet bazlı tahmin) | değerleme-temel | kilit: bilanço verisi |
| R147 | temel-değerleme | "Net kar, havadan gelen bir rakam değildir; cironun bir türevidir." | T+M+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R147 | temel-değerleme | "FD/FAVÖK ... %6.0 FAVÖK Marjı ... 119.28 TL" | T+M+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R147 | temel-değerleme | "Ne kadar satar? (Adet) → Hangi fiyattan ve kurdan satar? (Ciro) → ..." | T+M+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R147 | temel-değerleme | "INA, Çarpanlar değerleme sisteminin bir ayağıdır." | T+M+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R148 | teyit-tetik | "if (half\_trend[t] == 'buy' and momentum[t] > momentum\_threshold)" | T | 8: RSI 30 / Williams %R / APO / A/D–EMA3 / HalfTrend / ML lojistik satırı (HalfTrend, T R148) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R149 | bölge | "confluence alanının gücü..." (PETKM) | T+G | 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi (kavram) | bölge | ölçüm kolu |
| R150 | temel-değerleme | "şirketlerin cari dönem içindeki ara raporlarını modelimize entegre etmek hayati bir önem taşıyor." | M+T+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R150 | temel-değerleme | "ilk yarının gerçekleşen FAVÖK marjını bizzat sahadan, yani son rapordan çekip" | M+T+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R150 | temel-değerleme | "O nedenle koda manuel giriş sseçeneği de koydum." | M+T+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R150 | ölçüm-ilkesi | "xxcelde eski yaptığım değerlemeleri koda döküyorum" | M+T+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R151 | temel-değerleme | "Temel mantık 'Şirketin geçmişteki karlılık ve satış performansına bak ...'" | T+M+G | 8: Değerleme sistemi (T R151) | değerleme-temel | kilit: bilanço verisi |
| R151 | temel-değerleme | "Bunları da temel analiz kodlarımızın çıktılarından alıyoruz." | T+M+G | 8: Değerleme sistemi (T R151) | değerleme-temel | kilit: bilanço verisi |
| R151 | temel-değerleme | "Kod, manuel olarak girilen (4.33x) FK çarpanını kullanır" | T+M+G | 8: Değerleme sistemi (T R151) | değerleme-temel | kilit: bilanço verisi |
| R151 | temel-değerleme | FD/FAVÖK: FAVÖK marjı, net borç, piyasa değeri = FD - net borç | T+M+G | 8: Değerleme sistemi (T R151) | değerleme-temel | kilit: bilanço verisi |
| R151 | temel-değerleme | "Kod bu iki değerin ortalamasını alarak sene sonu için 1118.85 TL'lik bir hedef fiyat belirler." | T+M+G | 8: Değerleme sistemi (T R151) | değerleme-temel | kilit: bilanço verisi |
| R151 | temel-değerleme | "Sistemin ikinci ayağının ikinci aşaması ise FK , PD/DD , fd/FAVÖK ile kısa uzun ve sektör ortalama değerlerini" | T+M+G | 8: Değerleme sistemi (T R151) | değerleme-temel | kilit: bilanço verisi |
| R151 | temel-değerleme | "İNA'sonucunun %40'ı, ... ortalamasının %60'ı alınarak sapmalar minimize edilir." | T+M+G | 8: Değerleme sistemi (T R151) | değerleme-temel | kilit: bilanço verisi |
| R152 | temel-değerleme | "çarpanla rile değerleme sistemimizin ilk adımı basit çalışmalar olacak" | T+M+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R152 | temel-değerleme | beş adım: önceki yıl satış, büyüme, net kâr marjı, F/K, ödenmiş sermaye | T+M+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R152 | ölçüm-ilkesi | "2023 yıl sonunda sanırım froto gerçek maliyet ve kapanış değeri tam olarak 747 TL idi." | T+M+G | 8: Değerleme sistemi (kavram) | değerleme-temel | kilit: bilanço verisi |
| R153 | temel-değerleme | "Bir şirketin bugünkü gerçek değeri, gelecekte cebimize koyacağı nakitlerin bugünkü değeridir." (10 yıllık FCFF DCF) | T+M+G | 8: DCF altyapısı (FCFF, T R153) | değerleme-temel | kilit: bilanço verisi |
| R153 | temel-değerleme | tarihsel oran analizi 2010–2021/6 (brüt kâr marjı, FAVÖK marjı, capex/satış) | T+M+G | 8: DCF altyapısı (T R153) | değerleme-temel | kilit: bilanço verisi |
| R153 | temel-değerleme | "Satışların ilk yıllarda hızlı, sonra daha oturmuş bir tempoda büyüyeceğini varsaydık." | T+M+G | 8: DCF altyapısı (T R153) | değerleme-temel | kilit: bilanço verisi |
| R153 | temel-değerleme | özkaynak maliyeti: temettü, risk primi vb. yöntemlerin ortalaması | T+M+G | 8: DCF altyapısı (CoE, T R153) | değerleme-temel | kilit: bilanço verisi |
| R153 | temel-değerleme | "WACC hesabı kavramı anlamanız için gösterilmiştir. DCF de WACC 19.1 kullanılmıştır." | T+M+G | 8: DCF altyapısı (WACC, T R153) | değerleme-temel | kilit: bilanço verisi |
| R153 | temel-değerleme | "Devam Eden Değer (Terminal Value)"; sürekli büyüme %3,0 | T+M+G | 8: DCF altyapısı (terminal değer, T R153) | değerleme-temel | kilit: bilanço verisi |
| R154 | temel-değerleme | "DCF artık varsayımları girdikten sonra tek bir tuş ile sonuç verecek." | T+G | 8: Ürün hedefi (tek tuş, Excel çıktıları, R154); DCF altyapısı (T R154) | ürün-hedefi | bilgi: işlem kuralı değil |
| R155 | temel-değerleme | "şirketin bugünkü değerinin %60 ile %80'i ... 'Uç Değer'den gelir" | M+G | 8: DCF altyapısı (terminal değer, M R155) | değerleme-temel | kilit: bilanço verisi |
| R155 | temel-değerleme | "Sensitivity Analysis Yapın" (WACC × g matrisi) | M+G | 8: DCF altyapısı (duyarlılık, M R155) | değerleme-temel | kilit: bilanço verisi |
| R155 | temel-değerleme | "Tersine DCF (Reverse DCF) Çalıştırın" | M+G | 8: DCF altyapısı (ters DCF, M R155) | değerleme-temel | kilit: bilanço verisi |
| R155 | boyut-risk | "ciddi bir güvenlik marjı (örneğin %20 ile %30 arası) talep edin" | M+G | 8: DCF altyapısı (güvenlik marjı %20–30, M R155) | boyut-risk | kilit: bilanço verisi |
| R155 | temel-değerleme | "Muhafazakar Olun ... Büyüme oranlarını her zaman makroekonomik gerçeklere yakınsayacak şekilde törpüleyin." | M+G | 8: DCF altyapısı (M R155) | değerleme-temel | kilit: bilanço verisi |
| R155 | felsefe | "DCF bir hedef fiyat üretme makinesi değil ... matematiksel bir stres çarkıdır." | M+G | 8: DCF altyapısı (M R155) (kavram) | değerleme-temel | kilit: bilanço verisi |
| R156 | giriş | "Mean reversion, absolute pricing oscilator kullanılarak oluşturulan bir strateji." | T+G | 8: Bant kuyruğu tepki alımı (mean reversion APO, T R156; aynı fikir "RSI 30 / ... APO" satırında da anılır) | giriş | kilit: Tansu kural/formül vermedi |
| R156 | bölge | "Buna bir de yükselen kanal desteği çizdik mi mis:)" | T+G | 8: Kanal alt bandı, düşen direnç kırılımı + retest (kavram) | bölge | ölçüm kolu |
| R157 | felsefe | "Hipotez Oluşturma Test Etme Analiz Geliştirme" | M+T | TASARIM 2 (Sınamadan inanma); 5.11 deneme günlüğü; 5.12 kabul ölçütü | ilke | ilke: tasarımın kuralı |
| R157 | ölçüm-ilkesi | "Backtesting ... İşlem maliyetleri, piyasa likiditesi ve kayma (slippage)" | M+T | TASARIM 5.4 (masraf ve likidite); tasarim-8 3.1 S1 (masraf %0,3, likidite %2) | ilke | ilke: tasarımın kuralı |
| R157 | boyut-risk | "Risk Kontrolleri ve Beklenmedik Durum Planları: ... zarar durdur (stop-loss)" | M+T | tasarim-8 4.4 boyut (%1 risk, 2 ATR acil stop); TASARIM 2 (Önce sermaye) | ilke | ilke: tasarımın kuralı |
| R157 | felsefe | "iki satır kod yazayım ya da yazdırayım sevdası ... yıkıma sebep olabilir." | M+T | tasarim-8 5.2 (her yeni kod hash'i için boru hattı denetimi; olcum.py ayrı) | ilke | ilke: tasarımın kuralı |
| R158 | temel-değerleme | FCFF 388, FCFE 421, DDM 396: "Üç yöntemin birbirine bu kadar yakın çıkması tesadüf değil" | T/M+G | 8: DCF altyapısı (FCFF/FCFE/DDM, T/M R158) | değerleme-temel | kilit: bilanço verisi |
| R158 | temel-değerleme | "hem kısa hem orta hem uzun vadeli çarpanlar ayrı ayrı hesaplanacak." | T/M+G | 8: Değerleme sistemi (çarpanlar 3×3, T R158) | değerleme-temel | kilit: bilanço verisi |
| R158 | temel-değerleme | "üçünün ortalaması toplam ağırlığın yüzde kırkını ... çarpanlar analizinin ortalaması ise yüzde altmışı." | T/M+G | 8: Değerleme sistemi (%60/%40, T R158) | değerleme-temel | kilit: bilanço verisi |
| R158 | temel-değerleme | "piyasa ne der sorusu, biz ne hesapladık sorusundan genellikle daha bağlayıcı oluyor." | T/M+G | 8: Değerleme sistemi (T R158) | değerleme-temel | kilit: bilanço verisi |
| R158 | portföy | "Radara giren, sinyal üreten hisselerin tüm değerlemeleri yapılacak" (Dupont, teknik analiz) | T/M+G | 8: Hibrit alarm (kavram); Bilanço kalite filtreleri (Dupont) | portföy | kilit: bilanço verisi |
| R159 | temel-değerleme | "Damodaran'ın bu yaklaşımını kullanmalısınız" (Total Beta) | M+G | 8: DCF altyapısı (Damodaran total beta, M R159) | değerleme-temel | kilit: bilanço verisi |
| R159 | temel-değerleme | Unlevered beta; Total Beta = unlevered β / √R²; CoE = Rf + levered total β × ERP | M+G | 8: DCF altyapısı (total beta, CoE, M R159) | değerleme-temel | kilit: bilanço verisi |
| R159 | felsefe | "Python ... tek tuşla güncelleyebilirsiniz" | M+G | 8: Ürün hedefi (tek tuş) (kavram) | ürün-hedefi | bilgi: işlem kuralı değil |
| R160 | temel-değerleme | "Bu kadar basit işte" (CoE = rF + beta × rP) | T+G | 8: DCF altyapısı (CoE, T R160) | değerleme-temel | kilit: bilanço verisi |
| R161 | temel-değerleme | FCFE / FCFF / DDM karşılaştırma tablosu | G | 8: DCF altyapısı (G R161) | değerleme-temel | kilit: bilanço verisi |
| R162 | temel-değerleme | "roc = (ebit\*(1-tr/100)) / (bvd + bve)" | M+T | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (M R162) | araç-öğrenme | bilgi: işlem kuralı değil |
| R163 | temel-değerleme | "Kod bu iki akışı 5 yıl boyunca büyütür ... Terminal Value" (FCFE + DDM) | T/M | 8: DCF altyapısı (M R163) | değerleme-temel | kilit: bilanço verisi |
| R163 | temel-değerleme | "Eğer FCFE değeri, DDM değerinden çok yüksekse" | T/M | 8: DCF altyapısı (M R163) | değerleme-temel | kilit: bilanço verisi |
| R163 | felsefe | "bir değerleme uzmanı bu modeli tek başına mutlak doğru kabul etmek yerine ... makası görmek" | T/M | 8: DCF altyapısı (M R163) (kavram) | değerleme-temel | kilit: bilanço verisi |
| R163 | diğer | "Profesyonel Raporlama: ... Excel dosyasına dökerek" | T/M | 8: Ürün hedefi (Excel çıktıları, R163) | ürün-hedefi | bilgi: işlem kuralı değil |
| R164 | temel-değerleme | "Çarpan ve INA değerlemesi çalışmasının küçük kodlamalarından bir kesit." (EBIT bileşik büyüme) | T+G | 8: DCF altyapısı (T R164) | değerleme-temel | kilit: bilanço verisi |
| R165 | temel-değerleme | DCF 5 adım (WACC, FCF tahmini, bugünkü değer, terminal değer, içsel değer) | G-dış | 8: DCF altyapısı (G-dış R165) | değerleme-temel | kilit: bilanço verisi |
| R166 | diğer | "Çok önceleri excelde hazırladığım bir değerleme çalışmam vardı onu artık koda dökmenin zamanı geldi." | T | 8: Değerleme sistemi (T R166) | değerleme-temel | kilit: bilanço verisi |
| R166 | temel-değerleme | "Temel Analiz’in tüm matematiksel gücüyle Teknik Analiz’in zamanlamasını birleştiren, bir 'Hibrit Değerleme Sistemi'ni kodlamaya başlayacağım." | T | 8: Hibrit alarm (T R166); Değerleme sistemi | değerleme-temel | kilit: bilanço verisi |
| R166 | temel-değerleme | "Şirketin gelecek 10 yıllık nakit üretme kapasitesini bugüne indirgeyeceğiz." | T | 8: Değerleme sistemi; DCF altyapısı (T R166) | değerleme-temel | kilit: bilanço verisi |
| R166 | temel-değerleme | "WACC & Beta: ... Damodaran yaklaşımıyla" (Dinamik İskonto) | T | 8: DCF altyapısı (Damodaran, WACC; T R166) | değerleme-temel | kilit: bilanço verisi |
| R166 | temel-değerleme | "Sistem, satış gelirlerinden net kara, döviz bazlı büyümeden FAVÖK marjına kadar her kalemi tek tek işleyecek." (Adet Bazlı Tahminleme) | T | 8: Değerleme sistemi (T R166) | değerleme-temel | kilit: bilanço verisi |
| R166 | temel-değerleme | "Sistem çıktı olarak bize 3 farklı senaryo sunacak" | T | 8: Değerleme sistemi (T R166) | değerleme-temel | kilit: bilanço verisi |
| R166 | teyit-tetik | "değerleme %50 potansiyel diyorsa, Teknik 'Şimdi al' dediğinde sistem alarm verecek." | T | 8: Hibrit alarm (T R166) | teyit | kilit: bilanço verisi |
| R166 | diğer | "Amacım bilanço açıklandığı an temel veriyi saniyeler içinde çekip ... 'Ucuz/Pahalı/Trendte' etiketini" | T | 8: Hibrit alarm (T R166) | değerleme-temel | kilit: bilanço verisi |
| R166 | felsefe | "Çünkü piyasa fiyatı sizin ödediğinizdir, değer ise aldığınızdır." | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R166 | temel-değerleme | "Marj Analizleri: Brüt kar marjından, operasyonel işletme sermayesi (ONİS) değişimine kadar nakit döngüsünü" | T | 8: Değerleme sistemi (T R166) | değerleme-temel | kilit: bilanço verisi |
| R167 | teyit-tetik | "KLMSN.IS - Engulfing + EMA34 Tepki/Kırılım" | G | 8: Mum formasyonları (engulfing) (kavram) | teyit | ölçüm kolu |
| R167 | teyit-tetik | EMA5, EMA8, EMA13, EMA34 dizisi çizilmiş | G | 3.2 S ölçüm kolları (boğa dizilimi EMA5 > EMA8 > EMA13, G R167) | teyit | ölçüm kolu |
| R168 | bölge | "GEDZA": trend desteği, en yakın demand, en yakın FVG, BOS | G | 4.1; 4.2 (FVG, BOS; trend desteği 4.2 trend çizgisi) | bölge | resmi sınav |
| R168 | teyit-tetik | Hacim, MACD, ADX, RSI panelleri; "Temas" işareti | G | 8: Mum ve gösterge yorumları (MACD/RSI panelleri, G R168) | teyit | kilit: Tansu kural/formül vermedi |
| R169 | — | Python öğrenme rehberi (strateji içeriği yok) | M+T | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R170 | rejim | "Trend Filtresi: Fiyat, 14 periyotluk SMA çizgisinin üzerinde seyretmelidir." | T+M | 8: RSI 30 / Williams %R 30 dk satırı (M R170; gün içi) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R170 | teyit-tetik | "Williams %R önce aşırı alım bölgesine (-20 ile 0 arası) girmelidir." | T+M | 8: Williams %R 30 dk (M R170) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R170 | giriş | "-50'den yukarı döndüğü mumun (yeşil mum) en yüksek seviyesinin üzerine çıkıldığında işleme girilir." | T+M | 8: Williams %R 30 dk (M R170) | giriş | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R170 | stop-geçersizlik | "Stop Loss: En yakın dip (swing low) seviyesine konulur." | T+M | 8: Williams %R 30 dk (M R170) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R170 | hedef-çıkış | "Hedef: En az 1:2 Risk/Ödül oranı hedeflenir." | T+M | 8: Williams %R 30 dk (M R170) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R170 | giriş | Short ayna: SMA altı, %R -80 altı, swing high stop | T+M | 8: Williams %R 30 dk (M R170) | giriş | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R171 | felsefe | "kendi fikirlerinizi (veya başkalarının iddialarını) test edebilme imkanıdır" | T+M | TASARIM 2 (Sınamadan inanma); 5.11 deneme günlüğü; 5.12 kabul ölçütü | ilke | ilke: tasarımın kuralı |
| R171 | ölçüm-ilkesi | "Python, duyguları denklemden çıkarır." | T+M | TASARIM 1 (P1: sistem emir vermez, "kural sağlandı" der); 5.12 (kabul ölçütü önceden yazılır) | ilke | ilke: tasarımın kuralı |
| R171 | felsefe | "'Acaba çalışır mı?' diye kumar oynamak yerine, 'Veriler ne diyor?'" | T+M | TASARIM 2 (Sınamadan inanma); 5.11 deneme günlüğü; 5.12 kabul ölçütü | ilke | ilke: tasarımın kuralı |
| R172 | rejim | "bir piyasa bir kez harekete geçtiğinde, tersine bir sinyal oluşana kadar mevcut trendini sürdürme eğilimindedir." | T/M | tasarim-8 3.1 S1 (momentum rotasyonu); 4.5 şok freni (bıçak tutma yok) | ilke | ilke: tasarımın kuralı |
| R172 | felsefe | "trenddeki kırılma (dönüş) noktalarını 'tespit etmek' ve trene doğru zamanda binip doğru zamanda inmektir." | T/M | tasarim-8 3.1 S1 (momentum rotasyonu); 4.5 şok freni (bıçak tutma yok) | ilke | ilke: tasarımın kuralı |
| R172 | felsefe | "Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR." | T/M | tasarim-8 3.1 S1 (momentum rotasyonu); 4.5 şok freni (bıçak tutma yok) | ilke | ilke: tasarımın kuralı |
| R172 | momentum-seçim | "akıntının (momentumun) yönünü tayin edip o dalgayı sürmeye odaklanmalısınız." | T/M | tasarim-8 3.1 S1 (momentum rotasyonu); 4.5 şok freni (bıçak tutma yok) | ilke | ilke: tasarımın kuralı |
| R173 | portföy | Ham fiyat → getiri → standart sapma, korelasyon, Sharpe (öğrenme notu) | G-dış | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (R173) | araç-öğrenme | bilgi: işlem kuralı değil |
| R174 | ölçüm-ilkesi | "ARIMA Hiperparametre Optimizasyonunu ... itertools ... Ben doğrusu bunu kullanıyorum..." | T | 8: GARCH / ARIMA / ana frekans / ... satırı (ARIMA grid search, T R174) | ölçüm-yöntemi | bilgi: işlem kuralı değil |
| R175 | momentum-seçim | "her bir sektörü ... birer Karar Verme Birimi (KVB) olarak kabul ederiz." | T+M | 8: DEA / Convex Hull (T R175) | seçim-momentum | kilit: bilanço verisi |
| R175 | portföy | "skoru 1 olan (veya 1'e en yakın olan) 3-4 sektör portföye dahil edilir." | T+M | 8: DEA / Convex Hull (T R175) | portföy | kilit: bilanço verisi |
| R175 | portföy | "etkinlik skoru belirgin bir şekilde düşmeye başladığında ... bu sektörden çıkış yapılır." | T+M | 8: DEA / Convex Hull (T R175) | portföy | kilit: bilanço verisi |
| R175 | momentum-seçim | "Malmquist ... skoru 1'in üzerindeyse" | T+M | 8: DEA / Convex Hull (T R175) | seçim-momentum | kilit: bilanço verisi |
| R175 | diğer | "PyDEA veya Scipy kütüphaneleriyle modelleyerek" | T+M | 8: DEA / Convex Hull (T R175) | araç-öğrenme | kilit: bilanço verisi |
| R176 | momentum-seçim | "momentum\_func: ... slope ... annualized = (1 + slope) \*\* 252; return annualized \* (rvalue \*\* 2)" | T | 3.1 ölçüm kolu (Clenow, T R176) | seçim-momentum | ölçüm kolu |
| R176 | momentum-seçim | "sadece hissenin ne kadar yükseldiğine (getiri) değil, ne kadar istikrarlı/pürüzsüz yükseldiğine bakar" | T | 3.1 ölçüm kolu (Clenow, T R176) | seçim-momentum | ölçüm kolu |
| R177 | portföy | CAPM beklenen getiri, portföy varyansı, minimum varyans ağırlığı | G | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (R177) | araç-öğrenme | bilgi: işlem kuralı değil |
| R178 | momentum-seçim | "Sektör rotasyonu Convex Hull ile VZA analizini birlikte çalışırsanız muazzam sonuçlar" | T | 8: DEA / Convex Hull (T R178) | seçim-momentum | kilit: bilanço verisi |
| R179 | momentum-seçim | "birçok farklı ve bazen birbiriyle çelişen veriyi ... tek bir rasyonel puana indirgeyebilmesidir." (TOPSIS) | M+T | 8: TOPSIS (T R179) | seçim-momentum | kilit: bilanço verisi |
| R179 | momentum-seçim | "'nakit akışı' 'temettü verimi'nden daha önemliyse, sistemi bu önceliğe göre kolayca güncelleyebilirsiniz." | M+T | 8: TOPSIS (T R179) | seçim-momentum | kilit: bilanço verisi |
| R179 | diğer | "Yakında projeye başlıyorum." | M+T | 8: TOPSIS (T R179) | seçim-momentum | kilit: bilanço verisi |
| R180 | — | kurumsal stratejik yönetim (vizyon/misyon ↔ hedef, SMART) projesi (strateji içeriği yok) | T | — | araç-öğrenme | bilgi: işlem kuralı değil |
| R181 | portföy | "161.700 kombinasyon yaptıktan sonra sevgili algo matematiksel olarak optimal 3 hisselik portföyü verecek" | T+G | 3.1 ölçüm kolu (Max Sharpe 3–10 hisse, R181) | portföy | ölçüm kolu |
| R181 | momentum-seçim | "6 Ocak momentum alanında olan hisselerden bir test yapıyorum" | T+G | 3.1 ölçüm kolu (Max Sharpe, R181) | seçim-momentum | ölçüm kolu |
| R182 | portföy | "Neden Monte Carlo Yerine 'Spicy' Model? ... Bizim tercih ettiğimiz 'Spicy' yaklaşımı" | M | 3.1 ölçüm kolu (Markowitz/Max Sharpe) (kavram) | portföy | ölçüm kolu |
| R182 | portföy | "Monte Carlo bir tahmin makinesidir, Spicy modeli ise bir denge mimarıdır." | M | 3.1 ölçüm kolu (kavram) | portföy | ölçüm kolu |
| R183 | rejim | "Hangi aylarda %70 ve üzeri ihtimalle yükseldiğine bakın (Yüksek Olasılık)." | T+M | 4.5 (mevsimsellik, M R183); 8: Mevsimsellik ≥ %70 ay | rejim | ölçüm kolu |
| R183 | rejim | "BIST 100 ... son 10 yılın 8'inde 'Ocak' ayını pozitif kapatmışsa" | T+M | 4.5 (son 10 yılda ≥ %70 pozitif kapanan aylar, M R183) | rejim | ölçüm kolu |
| R183 | boyut-risk | "Nisan Ayı ... kasanızın %80'i ile oyuna girebilirsiniz. Ağustos Ayı ... kasanızın sadece %30'u" | T+M | 4.5 (ay bazlı maruziyet; %80/%30 kasa örnek, M R183) | boyut-risk | ölçüm kolu |
| R183 | felsefe | "Sell in May and Go Away"; Eylül zayıf | T+M | 4.5 (mevsimsellik) (kavram) | rejim | ölçüm kolu |
| R183 | diğer | "Sektörel Döngüleri Yakalamak" (elektrik yaz/kış) | T+M | 8: Kural taşımayan yan cümleler (sektörel döngüler, M R183) | seçim-momentum | kilit: Tansu kural/formül vermedi |
| R183 | felsefe | "İstatistik bir kristal küre değildir ... size pusula olur." | T+M | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R184 | boyut-risk | "Ne kadar hisse alacağınıza fiyatına bakarak değil, risk limitinize bakarak karar vermelisiniz." | T/M | 4.4 (boyut, T R184) | boyut-risk | resmi sınav |
| R184 | boyut-risk | "Göze Alınan Kayıp / Hisse Volatilitesi = Lot Sayısı. Örnek: 500 TL / 2 TL = 250 Lot." | T/M | 4.4 (boyut: adet = risk / mesafe; Tansu'nun formülü risk / 2 ATR) | boyut-risk | resmi sınav |
| R184 | stop-geçersizlik | "Giriş fiyatının 2ATR altına da acil stop konulur." | T/M | 4.4 (acil stop 2 ATR; T/M R184, 1) | çıkış | resmi sınav |
| R184 | stop-geçersizlik | "Gün Sonu Stop: Kapanış bazlıdır" | T/M | 4.4 (çıkış zinciri adım 4: kapanış SMA250 altı, G-dış R212 gün sonu çıkışı) (kavram) | çıkış | resmi sınav |
| R184 | hedef-çıkış | "İz süren stop, fiyat yükseldikçe stop seviyenizi de yukarı çekerek" | T/M | 4.4 (iz süren mod, T R224/R239) (kavram) | çıkış | resmi sınav |
| R184 | felsefe | "ne kadar kaybetmeyi göze aldığınızı yönetebilmektir." | T/M | tasarim-8 4.4 boyut (%1 risk, 2 ATR acil stop); TASARIM 2 (Önce sermaye) | ilke | ilke: tasarımın kuralı |
| R185 | felsefe | "algoritma geliştirenlerin düştüğü en büyük tuzak, fiyatın gelecekteki yönünü 'tahmin etmeye' çalışmaktır." | M | TASARIM 1 (P1: sistem tahmin etmez, "AL" demez, "kural sağlandı" der) | ilke | ilke: tasarımın kuralı |
| R185 | ölçüm-ilkesi | "bir işlem dizisinin Beklenen Değerine (E) odaklanırsınız" | M | tasarim-8 6 (net kâr / en büyük düşüş yazılır; kazanma oranı tek ölçüt değil) | ilke | ilke: tasarımın kuralı |
| R185 | boyut-risk | "Kurtosis ... Skewness ... Monte Carlo ... iflas riskini (Risk of Ruin)" | M | 8: GARCH / ARIMA / ana frekans / ... risk of ruin, kurtosis satırı (M R185) | boyut-risk | bilgi: işlem kuralı değil |
| R185 | felsefe | "Vaktinizi indikatörlere değil, olasılık yoğunluk fonksiyonlarına harcayın." | M | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R186 | rejim | "Fiyat VWAP üstünde + POC üstündeyse: Sadece alış yönlü bak." | T+M | 8: VWAP / POC / VAH / VAL (T R186) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R186 | bölge | "Fiyat hem VWAP'ın hem de POC'nin altındaysa ... 'short' fırsatı" | T+M | 8: VWAP / POC / VAH / VAL (T R186) | bölge | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R186 | teyit-tetik | "fiyat VWAP ile birlikte VAH'ın (üst sınırın) üzerine çıkar ve orada kalıcı olursa" | T+M | 8: VWAP / POC / VAH / VAL (T R186) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R186 | giriş | "Fiyat VAL'ın altına sarktığında ama VWAP hala yukarıda kaldığında" | T+M | 8: VWAP / POC / VAH / VAL (T R186) | giriş | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R186 | hedef-çıkış | hedef POC (VAL içine dönüş sonrası) | T+M | 8: VWAP / POC / VAH / VAL (T R186) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R187 | bölge | "Fiyatın %68.2'si 1SD, %95.4'ü 2SD ve %99'u 3SD bantları içinde gerçekleşir." (IV'den) | M+T+G | 8: Bant kuyruğu tepki alımı (±1/2 SD bantları, M R187; IV yok, gerçekleşen volatilite vekili YORUM) | bölge | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R187 | bölge | "Alt Bantlar (Destek): -1SD veya -2SD ... Üst Bantlar (Direnç)" | M+T+G | 8: Bant kuyruğu tepki alımı (M R187) | bölge | kilit: Tansu kural/formül vermedi |
| R187 | giriş | "-1SD seviyesine (ilk destek) geri çekilmesi güçlü bir alım fırsatıdır." | M+T+G | 8: Bant kuyruğu tepki alımı (M R187) | giriş | kilit: Tansu kural/formül vermedi |
| R187 | stop-geçersizlik | "stop seviyesi genellikle -2SD ... altına konulur." | M+T+G | 8: Bant kuyruğu tepki alımı (M R187) | çıkış | kilit: Tansu kural/formül vermedi |
| R187 | teyit-tetik | "IV seviyeleri; günlük pivot noktaları veya trend çizgileri ile kesiştiğinde sinyal gücü çok daha yüksektir." | M+T+G | 8: Bant kuyruğu tepki alımı (M R187) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R188 | rejim | yedi gösterge: Borsa-VIX korelasyonu, SMA 18/35, AO, RSI, VIX, ADX, hacim; skor "4/5" | G-dış | 2 (VIX yok); 8: BIST100 + VIX beş adım (kavram) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R189 | momentum-seçim | "tüm hisseler önce momentum sistemimden geçiyor sonra ayrıntılı yazıyorum" | T+M+G | 1 (hat 1, T R189); 3.2 akış 1 | seçim-momentum | resmi sınav |
| R189 | bölge | 4 saatlik: BOS, supply 38,00–39,50, destek 31,00–32,50; günlük EMA 200, talep 28,00–31,50 | T+M+G | 2 (gün içi veri yok) | bölge | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R189 | teyit-tetik | "Bu ortalamanın üzerine hacimli bir yerleşme gelmeden 'kalıcı dönüş başladı' demek zor." | T+M+G | 8: Hacim teyidi (kavram) | teyit | ölçüm kolu |
| R189 | bölge | "38.70 (Fib 0.382) seviyesi, hem Fibonacci direnciyle hem de günlükteki arz bölgesiyle çakıştığı için en riskli alan" | T+M+G | 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi (kavram) | bölge | ölçüm kolu |
| R190 | rejim | "önceki günün Değer Bölgesi içinde açılırsa, piyasa muhtemelen yatay ve dengeli" | T+M | 8: VWAP / POC / VAH / VAL (denge-dengesizlik, M R190) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R190 | rejim | "Fiyat, Değer Bölgesinin üst sınırına (Value Area High) geldiğinde satış, alt sınırına (Value Area Low) geldiğinde alış" | T+M | 8: VWAP / POC / VAH / VAL (M R190) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R190 | rejim | "Dengesizlik durumlarında aralığın tersine işlem açmak (fading) son derece risklidir." | T+M | 8: VWAP / POC / VAH / VAL (M R190) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R190 | hedef-çıkış | "Fiyat bu uç noktalara (2. veya 3. sapma) ulaştığında, 'ortalama değerine geri dönme'" | T+M | 8: VWAP / POC / VAH / VAL (M R190) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R190 | felsefe | "piyasa dengedeyken 'ping-pong' oynamalı ..., dengesizlik varken ise 'sörf' yapmalı" | T+M | 8: VWAP / POC / VAH / VAL (M R190) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R191 | bölge | "calculate\_daily\_pivot": P = (H+L+C)/3; R1 = 2P - L; S1 = 2P - H | G+G-dış | 4.1 (ölçüm: günlük pivot P/R/S, G R191) | bölge | ölçüm kolu |
| R192 | tarama-evren | "yeni tarama kodumuz ... Price Action ve Smart Money Concepts (FVG/Zone) bölgelerini bize getiriyor" | T+M+G | 3.2 adım 4 (S: ilk arz bölgesi ya da ilk düşüş FVG'si, T/M R192 "yeni tarama kodumuz") | bölge | resmi sınav |
| R192 | bölge | Demand 3,50–3,70 giriş; bearish FVG ilk hedef 4,50–4,80; supply 5,70–6,00 | T+M+G | 3.2 adım 4 (S hedef: ilk arz bölgesi ya da ilk düşüş FVG'si, T/M R192) | bölge | resmi sınav |
| R192 | stop-geçersizlik | "Eğer fiyat bu Yeşil Kutunun (3.50 altı gibi) altına sarkar ve orada kapanış yaparsa" | T+M+G | 4.1 (kapanış distal altına inince biter) (kavram) | çıkış | resmi sınav |
| R192 | teyit-tetik | "tam bir boğa trendi için fiyatın, o tepesindeki Mor ve Turuncu çizgilerin de üzerine çıkıp kalıcı olması gerekir." | T+M+G | 8: Kural taşımayan yan cümleler (EMA kümesi üstü kalıcılık, M R192) | teyit | kilit: Tansu kural/formül vermedi |
| R193 | formasyon | Elliott: 1-2-3, A-B-C düzeltme, "Hedef (Wave 5)" (ENJSA, başlıkta Wave 4 %54) | T+M+G | 5.1 (ENJSA dalga 4 %54); 3.2 E ölçüm kolları (dalga 4 geri alımı); 8: Elliott dalga 4 | formasyon | ölçüm kolu |
| R193 | bölge | "yeşil yatay kutular ... FVG" destek | T+M+G | 4.2 (FVG) | bölge | resmi sınav |
| R193 | formasyon | "HIKKAKE ... 'ayı tuzağı'" | T+M+G | 8: Mum ve gösterge yorumları (HIKKAKE, M R193) | formasyon | kilit: Tansu kural/formül vermedi |
| R194 | teyit-tetik | "İşte bu yüzden retest beklemek önemlidir. Bakın macd yanıltmış ama hacim asla desteklememiş." | T+G | 3.2 S ölçüm kolları (retest girişi, T R194); 8: Kanal alt bandı, düşen direnç kırılımı + retest | teyit | ölçüm kolu |
| R195 | teyit-tetik | "Fiyatın trend çizgisinin veya direncin ötesinde kararlı bir şekilde kapanış yapması gerekir." | T+M | 4.2 (kırılım kapanışla); 8: Kanal alt bandı, düşen direnç kırılımı + retest (M R195) | teyit | ölçüm kolu |
| R195 | giriş | "En temiz giriş fırsatı genellikle 'Retest' (Yeniden Test) aşamasında olur." | T+M | 8: Kanal alt bandı, düşen direnç kırılımı + retest (M R195) | giriş | ölçüm kolu |
| R195 | bölge | Gap: runaway gap; gap fill; "Başarısız Boşluklar" | T+M | 4.1 (ölçüm: boşluk/gap, M R195; açılışsız tanım YORUM) | bölge | ölçüm kolu |
| R195 | stop-geçersizlik | "Stop-loss seviyenizi belirlerken ATR indikatörünü kullanın." (1×ATR) | T+M | 4.4 (ATR tabanlı acil stop; tasarım 2 ATR) (kavram) | çıkış | resmi sınav |
| R195 | teyit-tetik | OBV fiyatla uyumlu mu | T+M | 8: Hacim teyidi (OBV) | teyit | ölçüm kolu |
| R196 | teyit-tetik | "Fiyat ve OBV Senkronizasyonu = Yüksek Güven" | G-dış | 8: Hacim teyidi (OBV, G-dış R196) | teyit | ölçüm kolu |
| R197 | rejim | "Fiyatın yükseliş trendinde olduğunu teyit et, bir düzeltme (geri çekilme) bekle ve FVG güçlü destek bloklarından işleme gir." | T+M+G | 3.2 E (M R197) | rejim | resmi sınav |
| R197 | teyit-tetik | "sol taraftaki önceki önemli bir tepeyi yukarı yönlü kırıp ... BOS (Break of Structure)" | T+M+G | 3.2 E; 4.2 (BOS) | teyit | resmi sınav |
| R197 | bölge | "Fibonacci Retracement ... OTE ... 0.618 (Altın Oran) ile 0.786 arasındaki bölge" | T+M+G | 3.2 E | bölge | resmi sınav |
| R197 | bölge | "Kesişim: ... Order Block veya FVG ... Fibo 0.618-0.786" | T+M+G | 3.2 E | bölge | resmi sınav |
| R197 | giriş | "0.618 seviyesine ... indiğinde ve ... yeşil kutu ile temas ettiğinde ALIM (LONG)" | T+M+G | 3.2 E | giriş | resmi sınav |
| R197 | stop-geçersizlik | "Fibonacci 1.0 seviyesinin ... hemen altına" | T+M+G | 3.2 E (stop Fib 1,0) | çıkış | resmi sınav |
| R197 | hedef-çıkış | "İlk hedef genellikle hareketin başladığı tepe noktasıdır (Fibonacci 0.0 seviyesi)." | T+M+G | 3.2 E (hedef Point 1) | çıkış | resmi sınav |
| R198 | formasyon | "geniş yeşil kutu (Demand Zone) içinde, sarı, turkuaz ve mor çizgilerin (EMA) birbirine iyice yaklaştığını" | M+T+G | 3.2 S | formasyon | resmi sınav |
| R198 | teyit-tetik | "EMA'ların (örneğin EMA 20, 50, 100) ... Ben 5-8-13 kullandım." | M+T+G | 3.2 S (EMA 5/8/13, T R198) | teyit | resmi sınav |
| R198 | giriş | "Agresif Giriş (Riskli) ... Güvenli Giriş (Önerilen): 'Breakout'" | M+T+G | 3.2 S (M R198 "Güvenli Giriş"); retest girişi ölçüm kolu | giriş | resmi sınav |
| R198 | stop-geçersizlik | "Stop noktası, EMA sıkışmasının olduğu Talep Bölgesinin (Yeşil Kutu) hemen altı" | M+T+G | 3.2 S (geçersizlik bölge altı) | çıkış | resmi sınav |
| R198 | hedef-çıkış | "İlk hedef ... Kırmızı Bölge (Supply/Arz)" | M+T+G | 3.2 S; 3.2 adım 4 | çıkış | resmi sınav |
| R198 | felsefe | "Yeşilde al, EMA'lar açılınca sür, Kırmızıda sat." | M+T+G | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R199 | felsefe | "fiyatın 'İndirimli Bölgeye' (Discount Zone) geri çekilmesini bekler" | M+G | 3.2 E | bölge | resmi sınav |
| R199 | tarama-evren | "Zaman Dilimi: Günlük (Daily) Varlıklar: Yüksek Hacimli Hisseler (BIST 30/100)" | M+G | 3.2 E; 3.1 evren (TASARIM 5.2) (kavram) | evren-likidite | resmi sınav |
| R199 | momentum-seçim | "en az %10'luk bir marj içermeli" (itki) | M+G | 3.2 E | seçim-momentum | resmi sınav |
| R199 | bölge | "Minimum: %50 Geri Çekilme (0.50) / İdeal (Golden Pocket): %61.8 - %65 / Maksimum: %78.6" | M+G | 3.2 E | bölge | resmi sınav |
| R199 | formasyon | "Tercihen A-B-C Elliott Zigzag yapısında" | M+G | 3.2 E ölçüm kolları (A-B-C zigzag düzeltmesi kesimi, M R199 "Tercihen") | formasyon | ölçüm kolu |
| R199 | teyit-tetik | "Fair Value Gap (FVG) ... doldurulmamış (Fresh/Unmitigated)" | M+G | 3.2 E; 4.2 (FVG) | teyit | resmi sınav |
| R199 | giriş | "FVG kutusunun üst bandına veya %61.8 seviyesine 'Limit Alış' emri." | M+G | 3.2 E (üst banda limit; 0,618 ölçüm kolu); 4.4 (limit dolumu) | giriş | resmi sınav |
| R199 | stop-geçersizlik | "Yükselişin başladığı ana dibin (Point 0) hemen altı" | M+G | 3.2 E (geçersizlik Point 0) | çıkış | resmi sınav |
| R199 | hedef-çıkış | "Hedef 1 (Güvenli): Eski Tepe Noktası (Point 1)." (Hedef 2 = Wave 3, 1.618) | M+G | 3.2 adım 4 (E: Point 1, M R199); Hedef 2 atıfsız | çıkış | resmi sınav |
| R199 | rejim | "Düşüş trendi (Lower Highs & Lower Lows) yapan bir hissede bu strateji uygulanmaz." | M+G | 3.2 E (yükseliş yapısı, HH) | rejim | resmi sınav |
| R199 | felsefe | "FOMO Yok: Fiyat FVG bölgesine gelmeden dönerse işlem yapılmaz." | M+G | 4.4 (limit 10 günde dolmazsa iptal) (kavram); haber öncesi risk cümlesi atıfsız | giriş | resmi sınav |
| R200 | ölçüm-ilkesi | "β = Kovaryans(Ri, Rm) / Varyans(Rm)" | G-dış | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (R200) | araç-öğrenme | bilgi: işlem kuralı değil |
| R200 | portföy | "Beta = 1 (Dengeli) / Beta > 1 (Agresif) / Beta < 1 (Defansif)" | G-dış | 8: Makro, Gordon, ROC, CAPM, ... (R200) | araç-öğrenme | bilgi: işlem kuralı değil |
| R200 | rejim | "Boğa Piyasası: Beta > 1 olan hisseler tercih edilir. Ayı Piyasası: Beta < 1" | G-dış | 8: Makro, Gordon, ROC, CAPM, ... (R200) | araç-öğrenme | bilgi: işlem kuralı değil |
| R200 | boyut-risk | "Beklenen Getiri Hesabı: CAPM" | G-dış | 8: Makro, Gordon, ROC, CAPM, ... (R200) | araç-öğrenme | bilgi: işlem kuralı değil |
| R201 | tarama-evren | "doğrudan ETF'lere ve likit hisselere odaklanın" | T | 3.1 S1 (evren: TASARIM 5.2 ilk 100) (kavram) | evren-likidite | resmi sınav |
| R201 | ölçüm-ilkesi | "istediğiniz fiyattan rahatça girip çıkabilmektir. Paranızı içeride kilitlemeyin" | T | 3.1 S1 (likidite %2 sınırı); 4.4 (%2 likidite) (kavram) | evren-likidite | resmi sınav |
| R202 | momentum-seçim | "Rolling alpha Rolling skewness. ... Momentum listelerimize uyguluyoruz." | T | 1 (hat 1, T R202); 3.1 ölçüm kolu (rolling alpha, rolling skewness) | seçim-momentum | ölçüm kolu |
| R203 | hedef-çıkış | "TP1 (İlk Kar Al - 0.382): Formül: D + ((C - D) \* 0.382)" | M+G | 3.2 H ölçüm kolları (hedef merdiveni TP1–TP4 = D + {0,382; 0,618; C; 1,272}·(C−D), M/G R203) | çıkış | ölçüm kolu |
| R203 | hedef-çıkış | "TP2 (Ana Hedef - 0.618 - Golden Pocket): D + ((C - D) \* 0.618)" | M+G | 3.2 adım 4 (H: AB=CD ana hedef D + 0,618·(C−D), M/G R203) | çıkış | resmi sınav |
| R203 | hedef-çıkış | "TP3 (Formasyon Zirvesi - C Noktası)"; "TP4 (Fibonacci Extension - 1.272 veya 1.618)" | M+G | 3.2 H ölçüm kolları (hedef merdiveni, M/G R203) | çıkış | ölçüm kolu |
| R203 | stop-geçersizlik | "X Noktası Altı: ...formasyon geçersiz sayılır (Invalidation)." | M+G | 3.2 H (geçersizlik X) | çıkış | resmi sınav |
| R203 | formasyon | "D noktası Potansiyel Dönüş Bölgesi (PRZ)" | M+G | 3.2 H (D/PRZ) (kavram) | formasyon | resmi sınav |
| R203 | teyit-tetik | "TP2'yi (0.618) güçlü ve hacimli bir mumla geçerse... yeni bir yükseliş trendi olabilir" | M+G | tasarımda yok (R203'ün TP1'de %50 ve stop girişe kısmı 4.4 ölçüm çıkış kollarında; TP2 sonrası trend cümlesi yok) | teyit | kilit: Tansu kural/formül vermedi |
| R204 | bölge | "0.618 seviyesine temas etmek hem de o bölgede kalan FVG boşluğunu doldurmak için oraya iner." | T/M | 3.2 E (T R204) | bölge | resmi sınav |
| R204 | teyit-tetik | "0.618 (veya 0.50) seviyesi, geçmişte bırakılan bir FVG kutusu ile çakışıyorsa" | T/M | 3.2 E | teyit | resmi sınav |
| R204 | felsefe | "Elliott ve Fibonacci 'Fiyatın nereye düşeceğini' (Seviye) söyler; FVG ..." | T/M | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R205 | hedef-çıkış | "4. Dalga Düşüşü = 3. Dalga Yükselişi X (0.24 veya 0.38 veya 0.50)" | T+M | 3.2 E ölçüm kolları (dalga 4 geri alımı, T/M R205); 8: Elliott dalga 4 | çıkış | ölçüm kolu |
| R206 | bölge | "Fibo 0.618 bir 'duvar' değil, sadece bir 'bölge'dir." | T | 4.2 (Fibonacci bir "bölge"dir: ±tolerans, T R206) | bölge | resmi sınav |
| R206 | teyit-tetik | "Matematiksel oran (Fibo) + Piyasa Yapısı (Order Block) = Sniper Giriş." (H4) | T | 4.2 (H4 Order Block gün içi veri ister, yoktur; T R206) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R207 | formasyon | "Temel Piyasa Döngüsü: 5 Yükseliş, 3 Düşüş"; Fibonacci dizisi | G-dış | 8: Elliott 5+3 ve Fibonacci günleri (G-dış R207); 8: Elliott dalga 4 | formasyon | ölçüm kolu |
| R207 | diğer | "Zaman Hedeflemesi ... Fibonacci günlerinde (5., 8., 13., 21. gün)" | G-dış | 8: Elliott 5+3 ve Fibonacci günleri (G-dış R207) | çıkış | ölçüm kolu |
| R208 | teyit-tetik | "Kesişim (Confluence) Nedir? ... birden fazla bağımsız teknik sinyalin aynı anda oluşmasıdır." | G-dış | 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi (G-dış R208) | teyit | ölçüm kolu |
| R208 | felsefe | "Tek Sinyale Güvenme, Kesişim Ara!" | G-dış | 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi (G-dış R208) | teyit | ölçüm kolu |
| R209 | rejim | "ADIM 1: Korelasyon Kontrolü ... ADIM 4: VIX Teyidi" | G-dış | 8: BIST100 + VIX beş adım (G-dış R209) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R209 | hedef-çıkış | "ADIM 5: Çıkış Stratejisi — Çıkışlar VIX'e göre değil, fiyat grafiğine göre" | G-dış | 8: BIST100 + VIX beş adım (G-dış R209) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R210 | felsefe | "herşey kurallara dayalı. Duyguya yer yok. Sistem ne derse o." | T/M | TASARIM 1 (P1: sistem emir vermez, "kural sağlandı" der); 5.12 (kabul ölçütü önceden yazılır) | ilke | ilke: tasarımın kuralı |
| R210 | rejim | "Korelasyon Kontrolü (Negative Correlations)" (BIST100 / VIX) | T/M | 8: BIST100 + VIX beş adım (T/M R210) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R210 | teyit-tetik | "Disiplin (Heikin Ashi)... Fiyat > Ortalamalar + AO = Yeşil + RSI > MAV" | T/M | 8: BIST100 + VIX beş adım (T/M R210; açılış yok) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R210 | rejim | "VIX < Hızlı Bantlar & VIX RSI < MAV" | T/M | 8: BIST100 + VIX beş adım (T/M R210; VIX yok) | rejim | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R210 | hedef-çıkış | "Çıkışlar VIX'e göre değil, Fiyat grafiğine (BIST 100) göre yapılır. 4 indikatörden 2'sinin bozulması gerekir." | T/M | 8: BIST100 + VIX beş adım (T/M R210) | çıkış | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R211 | boyut-risk | "Volatilitesi yüksek olan hisselerde position sizing matematiksel olarak küçülür ve bu çok doğrudur." | T | 4.4 (boyut, T R211); 1 (hat 4) | boyut-risk | resmi sınav |
| R211 | felsefe | "Asıl amacımız sermayemizi korumak.." | T | tasarim-8 4.4 boyut (%1 risk, 2 ATR acil stop); TASARIM 2 (Önce sermaye) | ilke | ilke: tasarımın kuralı |
| R212 | boyut-risk | "sermayenizin ancak %1'ini kaybetmek riskini göze alabilirsiniz" (Hisse Adedi = Risk Tutarı / 2 ATR) | T+G-dış | 4.4 (boyut %1 risk, T R212; %1 örnektir, YORUM) | boyut-risk | resmi sınav |
| R212 | stop-geçersizlik | "Acil Durum Stop'u: ... 2 ATR ... Gün Sonu Stop'u: ... 250 günlük hareketli ortalamanın altında bir kapanış" | T+G-dış | 4.4 (acil stop 2 ATR; çıkış zinciri adım 4: kapanış SMA250 altı, G-dış R212) | çıkış | resmi sınav |
| R212 | giriş | "işleme giriş bileşenlerinizden birisi 250SMA" | T+G-dış | 3.2 akış 1 (SMA250 giriş kapısı; T R212 örnek bileşen, 200SMA/200EMA/250EMA olabilir) | giriş | resmi sınav |
| R213 | diğer | "1. Teknoloji ve Analitik Araçlar (Python) ... 4. Optimizasyon ve Sinyal Tasarımı" | G-dış | süreç infografiği | araç-öğrenme | bilgi: işlem kuralı değil |
| R214 | teyit-tetik | "ema5>ema8>ema13 de oluşmuş son gün yükselen trend desteğinden tepki almış" | T+G | 3.2 S ölçüm kolları (boğa dizilimi, T R214; trend desteği 4.2 trend çizgisi) | teyit | ölçüm kolu |
| R215 | felsefe | "Bilgi ve Hazırlık Eksikliği; Disiplin ve Psikoloji Sorunları; Sermaye ve Risk Yönetimi Zafiyeti" | G-dış | infografik | araç-öğrenme | bilgi: işlem kuralı değil |
| R216 | rejim | "Eğim Ne Kadar Dikse, Yükseliş O Kadar Güçlüdür" (DMA kanalı) | G-dış | 8: Weinstein / DMA kanal eğimi ve evreler / ... satırı (G-dış R216) | rejim | kilit: Tansu kural/formül vermedi |
| R216 | rejim | "Evrelerin Birbirine Etkisi: Mevcut Evre Bir Sonrakini Belirler" | G-dış | 8: Weinstein / DMA kanal eğimi ve evreler / ... satırı (G-dış R216) | rejim | kilit: Tansu kural/formül vermedi |
| R217 | bölge | "Geleneksel Yaklaşım ... en yüksek ve en düşük noktaları arasındaki mesafeyi ölçer" | G-dış | 8: Çoklu aralık Fibonacci kümeleri (G-dış R217); 4.1 (çoklu aralık Fibonacci kümesi) | bölge | ölçüm kolu |
| R217 | bölge | "Piyasa Standart Seviyeleri Neden Görmezden Gelir?" (Caterpillar) | G-dış | 8: Çoklu aralık Fibonacci kümeleri (G-dış R217) | bölge | ölçüm kolu |
| R217 | bölge | "Aralık 'd' ... 50% seviyesini (A çizgisi)" genişleme ve daralma | G-dış | 8: Çoklu aralık Fibonacci kümeleri (G-dış R217) | bölge | ölçüm kolu |
| R217 | bölge | "Konfluans bölgesi, birden fazla ve farklı uzunluktaki fiyat aralığından hesaplanan Fibonacci oranlarının çakıştığı" | G-dış | 8: Çoklu aralık Fibonacci kümeleri (G-dış R217) | bölge | ölçüm kolu |
| R218 | diğer | "Neden Pine Script Değil de Python tercih ettim." | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R218 | tarama-evren | "Python, binlerce hisseyi saniyeler içinde tarayıp ... çok katmanlı kriterlere" | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R218 | ölçüm-ilkesi | "2008 krizinde veya pandemi düşüşünde nasıl davranacağını, komisyon oranlarını ve kayma maliyetlerini" | T | TASARIM 2 (Sınamadan inanma); 5.11 deneme günlüğü; 5.12 kabul ölçütü | ilke | ilke: tasarımın kuralı |
| R218 | diğer | "Yapay Zeka ve Makine Öğrenimi" kapısı; "İcra Özgürlüğü" | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R219 | formasyon | "1. Üç Tepeyi Tespit Et (Sol Omuz, Baş, Sağ Omuz)"; "2. Boyun Çizgisini (Neckline) Çiz" | G-dış | 8: Klasik formasyonlar (OBO kuralı, G-dış R219) | formasyon | kilit: Tansu kural/formül vermedi |
| R219 | teyit-tetik | "3. Kırılımı Onayla ... Hacmi Kontrol Et: Sağ omuz oluşurken işlem hacminin azalması" | G-dış | 8: Klasik formasyonlar (G-dış R219) | teyit | kilit: Tansu kural/formül vermedi |
| R219 | hedef-çıkış | "4. Hedef Fiyatı Belirle: Baş tepesi ile boyun çizgisi arasındaki mesafe kadar düşmesi beklenir." | G-dış | 8: Klasik formasyonlar (G-dış R219; long-only: OBO yalnız çıkış uyarısı) | çıkış | kilit: Tansu kural/formül vermedi |
| R220 | felsefe | "George Soros der ki: 'En büyük karlar Fat Tails alanında yapılır.'" (%95 / %5) | M | 8: Weinstein / DMA / piyasa evreleri / fat tail / BIST_VOL / mal boşaltma-toplama satırı (fat tail, M R220) | rejim | kilit: Tansu kural/formül vermedi |
| R220 | rejim | "Küçük yatırımcı genelde bu %5'lik şoklarda panikleyip elindekini satar." | M | 8: ... fat tail (M R220) (kavram) | rejim | kilit: Tansu kural/formül vermedi |
| R221 | formasyon | "Bullish Gartley ... Potansiyel Dönüş Bölgesi (PRZ)" (MAKIM) | T/M+G | 3.2 H (Gartley, G/M R222) | formasyon | resmi sınav |
| R221 | bölge | "Gartley formasyonunun dönüş noktası tam olarak bu FVG kutusunun içine denk geliyor." | T/M+G | 3.2 H; 4.2 (FVG) (kavram) | bölge | resmi sınav |
| R221 | teyit-tetik | "Swing Yapı ve Mum Formasyonları ... MACD ... RSI ... Hacim ve Takas Mantığı" | T/M+G | 8: Mum ve gösterge yorumları (MACD/RSI panelleri, M R221) | teyit | kilit: Tansu kural/formül vermedi |
| R221 | felsefe | "Piyasa matematiktir, disiplin ise anahtardır." | T/M+G | TASARIM 1 (P1: sistem emir vermez, "kural sağlandı" der); 5.12 (kabul ölçütü önceden yazılır) | ilke | ilke: tasarımın kuralı |
| R222 | formasyon | "AB Bacağı: XA bacağının tam olarak %61.8 seviyesine kadar geri çekilmelidir." | T/M+G | 3.2 H (Gartley) | formasyon | resmi sınav |
| R222 | formasyon | "BC Bacağı: AB bacağının %38.2 ile %88.6 arasına"; "CD Bacağı: XA bacağının %78.6" | T/M+G | 3.2 H (Gartley) | formasyon | resmi sınav |
| R222 | bölge | "PRZ... XA 0.786 ile BC uzantısının kesiştiği dar bir fiyat aralığıdır." | T/M+G | 3.2 H | bölge | resmi sınav |
| R222 | boyut-risk | "Eğer Ödül / Risk < 1.5 ise ... formasyon teknik olarak doğru olsa bile işleme girilmez" | T/M+G | 3.2 adım 4 (ödül/risk kapısı, M R222; harfiyen TP1 hali ölçüm kolu) | boyut-risk | resmi sınav |
| R222 | formasyon | "BIST verilerinde bazen tam 0.618'i yakalamak zor olabilir... %3-%5 tolerans" | T/M+G | 3.2 H (tolerans %3–5) | formasyon | resmi sınav |
| R222 | stop-geçersizlik | Excel tablosu: Buy Limit, SL = X_Fiyat - (ATR\*2), TP1 = D + (A-D) \* 0.382 | T/M+G | 3.2 H (Buy Limit, geçersizlik X; X − 2 ATR ölçüm kolu); 3.2 adım 4 (ana hedef TP2; TP1 harfiyen ölçüm); 4.4 | çıkış | resmi sınav |
| R223 | ölçüm-ilkesi | "Volatilite, aslında piyasanın 'ruh halidir'." (GBPUSD %10) | T+G | 3.2 adım 4 ölçüm (aktif volatilite kesimi, T/G R223) (kavram) | ölçüm-yöntemi | ölçüm kolu |
| R223 | ölçüm-ilkesi | "yillik_volatilite = gunluk_volatilite \* np.sqrt(252)"; eşik 0.40 | T+G | 3.2 adım 4 ölçüm (yıllık gerçekleşen volatilite ≥ %40, 252 gün; T/G R223) | ölçüm-yöntemi | ölçüm kolu |
| R224 | hedef-çıkış | "Giriş + 1.5 ATR seviyesine ulaştığında Trailing Stop (TS) aktif hale gelir" | T+G | 4.4 (çıkış zinciri adım 2, T R224); 1 (hat 4) | çıkış | resmi sınav |
| R224 | hedef-çıkış | "önceki günün en düşüğünün altında kapanış ve %50 satış, ve emergency stop 2atr" | T+G | 4.4 (çıkış zinciri adım 3 ve 4, T R224); "kar alma %10, ikinci kar alma" kısmı 4.4 ölçüm çıkış kolları | çıkış | resmi sınav |
| R225 | tarama-evren | "Soldaki Grafik - Piyasa Geneli Derinlik Dağılımı" (VWAP/TWAP, slippage) | M+G | 2 (emir defteri yok) | evren-likidite | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R225 | giriş | "emir defterinde ... sadece ilk 2-3 kademede yeterli lot var mı kontrol edin" | M+G | 2 (emir defteri yok) | giriş | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R225 | teyit-tetik | "Emir defterin alış tarafı kalınsa... satış tarafı inceyse... alım için iyi sinyal olabilir." | M+G | 2 (emir defteri yok) | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R225 | tarama-evren | "BIST30 gibi büyük hisseler genelde daha güvenlidir çünkü derinlikleri iyidir." | M+G | 2 (emir defteri yok) (kavram) | evren-likidite | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R226 | teyit-tetik | "1. İstatistiksel Sapma: Fiyat, etrafındaki gri/yeşil bantların ... dışına taşmış." | T/M+G | 8: Kapitülasyon üçlüsü (istatistiksel sapma, T/M R226) | teyit | ölçüm kolu |
| R226 | teyit-tetik | "2. Kapitülasyon ve El Değişimi: Fiyat dipteyken ... Hacim Skoru tavana vurmuş" | T/M+G | 8: Kapitülasyon üçlüsü (fiyat-hacim konumu); 4.5 (T/G R227) | teyit | ölçüm kolu |
| R226 | teyit-tetik | "3. Görünmeyen Emirler (OBI Analizi)" | T/M+G | 8: Kapitülasyon üçlüsü (OBI emir defteri ister); 2 | teyit | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R226 | giriş | "bu üç koşulun aynı anda (confluence) gerçekleştiği o 'kırmızı ok' anında tetiği çekmekti" | T/M+G | 8: Kapitülasyon üçlüsü (iki koşulla, ölçüm) | giriş | ölçüm kolu |
| R227 | ölçüm-ilkesi | "Konsantrasyon... Kümelenme... Pozisyon Büyüklüğü" (COT mantığı, açık pozisyon) | T+M+G | 2 (yok: açık pozisyon / COT); vekil 4.5 fiyat-hacim konumu | ölçüm-yöntemi | kilit: VIX-opsiyon-gün içi-emir defteri verisi (açık pozisyon / COT) |
| R227 | momentum-seçim | "Dinamik Aralık: ... son 1 yıla (252 işlem günü) göre nerede olduğunu yüzdesel olarak hesaplar." | T+M+G | 4.5 (fiyat ve hacim konumu 252 gün, T/G R227) | seçim-momentum | ölçüm kolu |
| R227 | teyit-tetik | "Sol Üst Köşe (Düşük Fiyat + Yüksek Hacim)... güçlü bir 'Al' fırsatı olabilir." | T+M+G | 4.5 (sol üst köşe dip adayı: fiyat ≤ 20, hacim ≥ 80) | teyit | ölçüm kolu |
| R227 | ölçüm-ilkesi | "RSI: Genelde son 14 muma bakar ... Bizim Kodumuz: Son 1 yıla (252 gün)" | T+M+G | 4.5 (kavram) | ölçüm-yöntemi | ölçüm kolu |
| R227 | ölçüm-ilkesi | "Eğer Konsantrasyon yüksek ama Kümelenme düşükse: Piyasayı az sayıda "balina" domine ediyordur." | T+M+G | 2 (yok: açık pozisyon / COT) | ölçüm-yöntemi | kilit: VIX-opsiyon-gün içi-emir defteri verisi (açık pozisyon / COT) |
| R227 | ölçüm-ilkesi | "Bu verileri 1 yıllık ... hareketli pencereler (rolling window) içinde normalize etmemiz lazım." | T+M+G | 4.5 (kavram) | ölçüm-yöntemi | ölçüm kolu |
| R227 | teyit-tetik | "Durum A (Yükseliş Yorgunluğu) ... Durum B (Panik Satışı): Fiyat dipte. RSI: 30 altında" | T+M+G | 4.5 (kavram) | teyit | ölçüm kolu |
| R228 | ölçüm-ilkesi | "Arbitraj için Cointegration (Eşbütünleşme) şarttır, şarttır. şarttır." | T | 3.3 (kapı: rolling eşbütünleşme, T R228); 1 (hat 3) | ölçüm-yöntemi | resmi sınav |
| R228 | felsefe | "sarhoş adam ve tasmalı köpek" benzetmesi | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R228 | felsefe | "Cointegration olmadan açılan işlemlerde büyük zararlar yazıp ta ne yapacağız diyen çok insan gördüm." | T | tasarim-8 3.3 (kapı: rolling eşbütünleşme) | ilke | ilke: tasarımın kuralı |
| R229 | rejim | "1. Makro ve Döngü Analizi" (konveks rotasyon) | T/M | 8: Konveks rotasyon (T/M R229) | rejim | kilit: bilanço verisi |
| R229 | tarama-evren | "2. Konveksite Filtresi: Asimetrik Getiri" | T/M | 8: Konveks rotasyon (T/M R229) | evren-likidite | kilit: bilanço verisi |
| R229 | momentum-seçim | "3. Erken Aşama Tespiti: Dip Yakınlığı ... Göreceli Güç Filtresi" | T/M | 8: Konveks rotasyon (T/M R229) | seçim-momentum | kilit: bilanço verisi |
| R229 | portföy | "4. Rotasyon ve Uygulama: Negatif konveksite taşıyan sektörlerden ... pozitif konveksite" | T/M | 8: Konveks rotasyon (T/M R229) | portföy | kilit: bilanço verisi |
| R229 | stop-geçersizlik | "5. Risk Yönetimi: ... 'Rolling Convexity'" | T/M | 8: Konveks rotasyon (T/M R229) | çıkış | kilit: bilanço verisi |
| R230 | tarama-evren | "1. Aktif Volatilite (Oynaklık) Aranmalı" | T/M | 3.2 adım 4 ölçüm (aktif volatilite kesimi, M R230) | evren-likidite | ölçüm kolu |
| R230 | teyit-tetik | "2. Sinyallerin Uyumuna (Confluence) Dikkat Edilmeli" | T/M | 8: Çoklu aralık Fibonacci kümeleri, confluence ilkesi (kavram) | teyit | ölçüm kolu |
| R230 | momentum-seçim | "3. Pozitif Momentum Takip Edilmeli" | T/M | 3.1 S1 (kavram) | seçim-momentum | resmi sınav |
| R230 | rejim | "4. Trend Yönünde Giriş Sinyalleri Alınmalı ... Yükselen Trend: Yalnızca Al" | T/M | 3.2 akış 1 (SMA250 kapısı) (kavram) | rejim | resmi sınav |
| R230 | boyut-risk | "5. Risk/Ödül ... 1 kaybetme riskine karşılık 2 veya 3 kazanma hedefi" | T/M | 3.2 adım 4 (ölçümde 2 ve 3 eşikleri, M R230; resmi eşik 1,5) | boyut-risk | ölçüm kolu |
| R231 | rejim | "sadece hisse senetlerinin ya da kripto paraların fiyat grafiğine bakarak yatırım yapmak, büyük resmin çok küçük bir parçasını görmektir" | M | 8: Makro, Gordon, ROC, CAPM, kur Monte Carlo, yöntem notları (M R231) | araç-öğrenme | bilgi: işlem kuralı değil |
| R232 | tarama-evren | "Eğer BIST100 ortalamasını referans alırsanız, analizinizi daha başlamadan çöpe atarsınız." | T/M | 8: Sektör rotasyonu zinciri (T/M R232) | seçim-momentum | ölçüm kolu |
| R232 | tarama-evren | "Adım 2: Son 20 günün ... veya 60 günün ... hacim ortalaması"; 10 Milyon TL; alt %25 | T/M | 3.1 geniş evren ölçüm kolu (20 günlük ortalama TL hacmi ≥ 10 milyon TL, T/M R232); 8: Sektör rotasyonu zinciri | evren-likidite | ölçüm kolu |
| R232 | tarama-evren | "Sektörleri kendiniz belirleyin. Sanırım şu anda halihazırda 80'e yakun sektör var faaliyette." | T/M | 8: Sektör rotasyonu zinciri (T/M R232) | seçim-momentum | ölçüm kolu |
| R233 | giriş | "RSI (14) değeri, 30 seviyesinin altından yukarı doğru keserek bu seviyenin üzerinde bir kapanış yaptığında." | M+T | 8: RSI 30 / Williams %R / APO / A/D–EMA3 / HalfTrend / ML lojistik satırı (RSI 30, M R233) | giriş | kilit: VIX-opsiyon-gün içi-emir defteri verisi |
| R233 | hedef-çıkış | "ana kâr alma sinyali RSI 70 Reddi ile başlar ... Pozisyonun %50'si satılır." | M+T | 4.4 ölçüm çıkış kolları (R233 zinciri: RSI 70 reddinde %50, M R233) | çıkış | ölçüm kolu |
| R233 | hedef-çıkış | "Bir önceki günün (mumun) en düşük fiyat seviyesinin (LOW) altında bir kapanış ... Kalan %50" | M+T | 4.4 ölçüm çıkış kolları (R233 zinciri: kalan %50 için ikinci "önceki gün düşüğü altı kapanış"; resmi zincir T R224/R239) | çıkış | ölçüm kolu |
| R233 | hedef-çıkış | "pozisyonun risk/ödül oranı hedefine ulaştığında Trailing Stop (TS)... devreye girer" | M+T | 8: Trailing stop'a geçiş için risk/ödül hedefi (M R233) | çıkış | kilit: Tansu kural/formül vermedi |
| R234 | ölçüm-ilkesi | "temel modelim de bir makine öğrenmesi algoritmasına dayanıyor:)" | T+G | 8: ML lojistik (T R234) | ölçüm-yöntemi | kilit: Tansu kural/formül vermedi |
| R234 | teyit-tetik | "hacim RSI verileri ile lojistik regresyonla bir model" | T+G | 8: ML lojistik (T R234) | teyit | kilit: Tansu kural/formül vermedi |
| R234 | ölçüm-ilkesi | "Finansal piyasalarda %70 gibi bir değer yakalarsanız bu harika bir sonuçtur." | T+G | 8: ML lojistik (T R234) | ölçüm-yöntemi | kilit: Tansu kural/formül vermedi |
| R234 | boyut-risk | "Kritik Kural: %55 başarı oranıyla ... Risk/Ödül oranını en az 1:1.5" | T+G | 3.2 adım 4 (ödül/risk kapısı, T R234); 1 (hat 4) | boyut-risk | resmi sınav |
| R234 | rejim | "Trendli piyasalada çok iyi ve düşüşleri iyi yakalıyor." | T+G | 8: ML lojistik (T R234) | rejim | kilit: Tansu kural/formül vermedi |
| R234 | teyit-tetik | "Sistem daha seçici ve muhafazakar hale geldi. Her harekete atlamıyor" | T+G | 8: ML lojistik (T R234) | teyit | kilit: Tansu kural/formül vermedi |
| R234 | ölçüm-ilkesi | "Hacim ve RSI filtrelerinin eklenmesiyle modelin Doğruluk oranı %55.00 oldu." | T+G | 8: ML lojistik (T R234) | ölçüm-yöntemi | kilit: Tansu kural/formül vermedi |
| R235 | rejim | "Yükselen Trend → Birikim Süreci → Alım Tepesi / Test → Dağıtım Süreci → Satış Tepesi → Düşen Trend" | G-dış | 8: Weinstein / DMA / piyasa evreleri ve birikim anlatısı / ... satırı (G-dış R235) | rejim | kilit: Tansu kural/formül vermedi |
| R236 | formasyon | "İkili Dip (Double Bottom) ... Çekiç, Yutan Boğa veya Cımbız Dip formasyonu"; Adam ve Havva | M | 8: Klasik formasyonlar (ikili dip, M R236) | formasyon | kilit: Tansu kural/formül vermedi |
| R237 | rejim | "Her şey genelde piyasa için kötü algılanan bir haberle başlar ... alımları gizli ve yavaş yaparlar" | T | 8: Weinstein / DMA / piyasa evreleri ve birikim anlatısı / ... satırı (T R237) | rejim | kilit: Tansu kural/formül vermedi |
| R238 | teyit-tetik | "Geniş gövdeli mum yüksek hacim, ok / Dar gövdeli mum yüksek hacim, anomali" | T | 8: Hacim teyidi (T R238) | teyit | ölçüm kolu |
| R239 | hedef-çıkış | "Statik iz süren stop: Hedef = Giriş + (1.5 × Giriş ATR)"; "Dinamik İz Süren Stop" | T | 4.4 (çıkış zinciri adım 2; dinamik hal "daha zekice" ölçüm kolu, T R239) | çıkış | resmi sınav |
| R239 | hedef-çıkış | "İz süren moda girdiğinizde yani Giriş + 1.5ATR noktasına geldiğinizde ... %50'sin satın." | T | 4.4 (çıkış zinciri adım 3, T R239) | çıkış | resmi sınav |
| R240 | temel-değerleme | "şirket değerlendirirken şunlara bakılır" (Sektör, İşletme, Finansallar kontrol listesi) | T/M | 8: Bilanço kalite filtreleri (işletme kriterleri, M R240) | değerleme-temel | kilit: bilanço verisi |
| R240 | felsefe | "gerçi bistte artık bir önemi yok. sırtlanların kol gezdiği bir cambazhaneden farksız." | T/M | 8: Değerleme sistemi (T R240: çelişki raporda yazılır) | değerleme-temel | kilit: bilanço verisi |
| R241 | rejim | "Yükseliş İmpulsu (1 Nolu Dalga)... Higher High (HH)... Düzeltme (A-B-C)... Dalga 2" (ALKA) | T/M+G | 3.2 E; 5.1 (ALKA düzeltme −%39,3) | rejim | resmi sınav |
| R241 | bölge | "FVG (Adil Değer Boşluğu) veya Talep Bölgesi... Fiyatın düzeltme hareketindeki son noktası (C)" | T/M+G | 3.2 E; 4.2 (FVG) | bölge | resmi sınav |
| R241 | teyit-tetik | "TC noktasında oluşan inverted hammer ise pastanın üzerindeki çilektir." | T/M+G | 8: Mum ve gösterge yorumları (inverted hammer, T R241) | teyit | kilit: açılış fiyatı |
| R242 | rejim | "düzeltmenin bir önceki yükselen dip (HL) seviyesine ... bir destek/talep bölgesine (demand zone) kadar inmesi idealdir" | M+G | 3.2 E ölçüm kolları (düzeltmenin önceki yükselen dibin (HL) üstünde kalması kesimi, M R242) | rejim | ölçüm kolu |
| R242 | rejim | "Net Piyasa Yapısı Kayması: ... Lower Low (LL) seviyesinden sonra Higher Low (HL)" | M+G | 3.2 E ölçüm kolları (HL kesimi, M R242) (kavram) | rejim | ölçüm kolu |
| R242 | felsefe | "yükselen dip yapısı (LL → HL) ... daha üstün ve güvenilir kabul edilir" | M+G | 3.2 E ölçüm kolları (HL kesimi, M R242) (kavram) | formasyon | ölçüm kolu |
| R242 | bölge | "talep bölgesine (sarı/yeşil kutu) geri çekilmesi (C noktası), ... güvenilir bir test" | M+G | 3.2 E ölçüm kolları (HL kesimi, M R242) (kavram) | bölge | ölçüm kolu |
| R243 | giriş | "Boşluğu Soldurma (Fading the Gap) ... kısa (short) pozisyon" | T/M | tasarımda yok (kısa pozisyon; R243 yalnız dolmuş FVG sonrası giriş için anılır) | giriş | kilit: açığa satış (BIST) |
| R243 | giriş | "Boşluğun Dolmasını Bekleyip Başlangıç Yönünde İşlem Yapma" | T/M | 3.2 E ölçüm kolları (dolmuş FVG sonrası giriş, M R243); 9 madde 3 | giriş | ölçüm kolu |
| R243 | bölge | "FVG'yi avlamanın en kolay yolu ise büyük mumları incelemektir." | T/M | tasarımda yok (R243 büyük mum cümlesi) | bölge | kilit: Tansu kural/formül vermedi |
| R244 | bölge | "Medyanı şöyle bir kanal gibi kullanın arkadaşlar." | T+G | 8: Medyan temelli çalışma, medyan kanal (T R244) | bölge | ölçüm kolu |
| R245 | diğer | "Hadi şunu vereyim / Ne kadar çok rt o kadar çok formasyon:)" | T | 8: Ahengin uyumu / arbitraj başlığı / RT satırı | araç-öğrenme | bilgi: işlem kuralı değil |
| R245 | bölge | AEFES kanal alt bant teması, "Lookback: 120 ... Üst/Alt temas: 3/3" (görsel) | G | 8: Kanal alt bandı teması (G R245) | bölge | ölçüm kolu |
| R246 | tarama-evren/giriş | "Aslında en temiz strateji bulacaksın 80-100 haftalık yatay giden bir hisse dibinde oturup bekleyeceksin." | T | 8: 80–100 haftalık yatay hisse (T R246) | evren-likidite | ölçüm kolu |
| R246 | tarama-evren | "Yazalım o zaman taramasını:)" | T | 8: 80–100 haftalık yatay hisse (tarama paylaşılmadı) | araç-öğrenme | bilgi: işlem kuralı değil |
| R247 | teyit-tetik | "Güzer retest var" (kırılım + retest görseli) | T+G | 8: Kanal alt bandı teması, düşen üst sınır kırılımı ve retest (T R247); 3.2 K (kavram) | teyit | ölçüm kolu |
| R247 | felsefe | "Gider mi gitmez mi artık orası tahtacıya kalmış" | T | felsefe notu | araç-öğrenme | bilgi: işlem kuralı değil |
| R248 | — | "Canlanın:)" + düşen üst sınırı aşan yeşil kırılım mumu (görsel) | T+G | 8: Kanal alt bandı teması, düşen üst sınır kırılımı (G R248) | teyit | ölçüm kolu |
| R249 | formasyon | "Three Drives Pattern ... art arda üç kez yeni bir ekstrem nokta ... düşen piyasada ise üç adet giderek düşen dip" | T+G | 3.2 H (Three Drives, T R249) | formasyon | resmi sınav |
| R249 | bölge | "A ... ve ... C düzeltmesi ... yüzde 61,8 veya yüzde 78,6 ... 1,272 veya 1,618 Fibonacci extension" | T | 3.2 H (Three Drives oranları, T R249) | formasyon | resmi sınav |
| R249 | formasyon | "A noktasından Drive 2'ye ... ile C noktasından Drive 3'e ... birbirine yakın büyüklükte olmalıdır." | T | 3.2 H (Three Drives fiyat simetrisi) | formasyon | resmi sınav |
| R249 | formasyon | "Biri 10 bar, diğeri 11-12 bar sürüyorsa yapı oldukça dengelidir. ... 8 bar, diğeri 30 bar ... bozulur." | T | 3.2 H (Three Drives zaman simetrisi, oran ≤ 1,5 YORUM) | formasyon | resmi sınav |
| R249 | formasyon | "Hareketleri zorlayarak bir formasyon yaratmaya çalışıyorsanız büyük ihtimalle ortada gerçek bir Three Drives yoktur." | T | 3.2 H (Three Drives: oran ve simetri şartları birlikte) | ilke | ilke: tasarımın kuralı |
| R249 | teyit-tetik | "Drive 3 oluştu diye doğrudan ters yönde işlem açmak doğru değildir. ... reaksiyon verip vermediğini izlemek gerekir." | T | 3.2 H (Three Drives girişi reaksiyon teyidinde; geçersizlik 1,618 uzantısı) | teyit | resmi sınav |
| R249 | felsefe | "Önce fiyatın gerçekten üç drive oluşturduğunu görürüz. Sonra Fibonacci ilişkilerini ... fiyatın bize gösterdiği yapıyı trade ederiz." | T | 3.2 H (Three Drives kontrol sırası) | ilke | ilke: tasarımın kuralı |
| R250 | formasyon | "kelebeklerrrrr #doas" | T | 3.2 H (Kelebek) | formasyon | resmi sınav |
| R250 | bölge | DOAS kelebek: A 209,10, X 170,10, "1.272 (D hedefi): 159.49; D: 159.40 [TAMAMLANDI]" (görsel) | G | 5.1 H sadakat (DOAS, G R250) | bölge | resmi sınav |
| R251 | portföy | "Arbitraj hisselerini bu başlıkta paylaşıyorum." (üst tweet) | T | 8: Ahengin uyumu / arbitraj başlığı / RT satırı | araç-öğrenme | bilgi: işlem kuralı değil |
| R251 | ölçüm-ilkesi | "RELATIVE VALUE ROTATION \| VAKBN <-> GARAN ... YENI AL SINYALI ... Z donusu +0.30 ... Cointegration p 0.048" (rapor) | G | 3.3 (long-only rotasyon ve ΔZ kanıtı, G R251); 5.1 S3 sadakat | portföy | resmi sınav |
| R251 | rejim | normalize fiyat, Z, rolling korelasyon/beta panelleri, "Pair Quality", "Half-Life" (görsel) | G | 3.3 (yalnız Z ve kointegrasyon; Pair Quality ve Half-Life formülü yok) | ölçüm-yöntemi | kilit: Tansu kural/formül vermedi |
| R252 | ölçüm-ilkesi | "Corwin-Schultz ... sadece günlük High ve Low fiyatlarını kullanarak ... spread'ini tahmin etmeye çalışır." | T+G | 4.5 (Corwin–Schultz, T R252, 21 gün G R252) | ölçüm-yöntemi | ölçüm kolu |
| R252 | ölçüm-ilkesi | "Spread düşük, Sigma düşük ... Spread yüksek, Sigma yüksek: ... En riskli yapı." | T | 4.5 (dört sınıf kesimi) | rejim | ölçüm kolu |
| R252 | felsefe | "işlem kalitesi ve likidite risk radarı olarak ... tek başına al-sat göstergesi olarak değil." | T | 4.5 (Corwin–Schultz yalnız ölçüm katmanında) | ilke | ilke: tasarımın kuralı |
| R252 | teyit-tetik | "fiyat yükselirken Spread düşüyorsa ... daha sağlıklı ... Spread de yükseliyorsa ... daha kırılgan" | T | 4.5 (teyit kesimi) | teyit | ölçüm kolu |
| R252 | rejim | "XU100'de güncel Spread yüzde 2,15 ... Tarihsel ortalama ise yaklaşık yüzde 1,09." | T | 4.5 (o güne özgü okuma) | rejim | bilgi: işlem kuralı değil |
| R252 | teyit-tetik | "Spread yeniden tarihsel ortalamasına doğru gerilerse ... rahatlama"; "düşük Sigma, risk azaldı anlamına gelmez." | T | 4.5 (yüksek/düşük = kendi geçmiş ortalamasına göre) | teyit | ölçüm kolu |
| R253 | formasyon/teyit-tetik | "Breakout-->FVG-->Retest-->Confirmation / Bu yapıları arayın" (alıntı) + AKFIS "A+ SETUP" (görsel) | T+G | 3.2 K; 5.1 K sadakat (AKFIS, G R253) | formasyon | resmi sınav |
| R253 | diğer | "Dikkat edelim bu yapıya" | T | 3.2 K (atıf) | araç-öğrenme | bilgi: işlem kuralı değil |
| R254 | formasyon/teyit-tetik | "Breakout-->FVG-->Retest-->Confirmation / Bu yapıları arayın" | T+G | 3.2 K (T R254) | formasyon | resmi sınav |
| R255 | ölçüm-ilkesi | "Backtest yapın. ... sonraki 1, 3 ve 5 günde ne olmuş bakın." | T | 6 (aday günlüğü 1/3/5 gün, T R255) | ilke | ilke: tasarımın kuralı |
| R255 | ölçüm-ilkesi | "Hangi aday tipi para kazandırıyor? ... Yoksa retest beklemek bizi fazla mı geciktiriyor?" | T | 6 (aday tipi karşılaştırması, ölçüm başlığı); 3.2 tarayıcı başına sonuç | ölçüm-yöntemi | ölçüm kolu |
| R255 | teyit-tetik | "Market Structure ve fiyat davranışı ana motor olsun RSI, MACD, WaveTrend, RS gibi unsurlar yardımcı teyit olsun." | T | 3.2 (resmi akış yapı + bölge + formasyon; göstergeler ölçüm kesimi) | ilke | ilke: tasarımın kuralı |
| R255 | boyut-risk | "Pozisyon büyüklüğünü stop mesafesine göre hesaplayın." | T | 4.4 (boyut: risk / (giriş − geçersizlik)) | boyut-risk | resmi sınav |
| R255 | ölçüm-ilkesi | "İşlem günlüğü oluşturun. Aday tarihi → giriş → neden girdik → invalidation → TP → sonuç → maksimum olumlu/olumsuz hareket." | T | 6 (aday günlüğü, MFE/MAE) | ilke | ilke: tasarımın kuralı |
| R255 | felsefe | "Bir gösterge veya filtre sonuçlara katkı sağlamıyorsa sırf teknik görünmek için sistemde tutmayın." | T | 4.5 ve 5.2 (kapılı/kapısız kollar) | ilke | ilke: tasarımın kuralı |
| R256 | felsefe | "benim ilk sorduğum soru "hangi indikatör AL diyor?" değildir. Asla ama asla bu hatayı yapmam" | T | 1; 3.2 (akış göstergeyle başlamaz) | ilke | ilke: tasarımın kuralı |
| R256 | rejim | "İlk sorum şudur: Fiyat şu anda hangi yapının içinde ... bölgeyi, kırılımları, likidite hareketlerini ve 4 saatlik teyidi" | T | 1; 3.2 akış (yapı → bölge → kırılım; 4 saatlik teyit gün içi veri ister, 2) | rejim | resmi sınav |
| R256 | ölçüm-ilkesi | "Şablonu aynı zamanda koşullar ve sonuçlar ile koda da döktüm ... kod da aynı sonuçları veriyor" | T | 1; 5.1 (sadakat: kod Tansu'nun manuel sonucunu bulmalı) | ilke | ilke: tasarımın kuralı |
| R257 | rejim | ""BEKLE ve TEYİT ARA" konumundadır. ... dip tahmini yapmaya çalışmak yerine" | M+G | 8: XU100 günlük yorumları (M R257) | rejim | bilgi: işlem kuralı değil |
| R257 | teyit-tetik | "fiyatın yaklaşık 14.722 seviyesinin üzerine çıkması ve burada kalıcılık göstermesi gerekiyor" | M | 8: XU100 günlük yorumları (o güne özgü seviye) | teyit | bilgi: işlem kuralı değil |
| R257 | bölge | "ilk önemli sınav 14.740–14.876 bölgesi ... 13.000 civarı ... savunma alanlarından biri" | M | 8: XU100 günlük yorumları (o güne özgü seviye) | bölge | bilgi: işlem kuralı değil |
| R257 | boyut-risk | "nakit esnekliği korunmalı ve yeni pozisyonlar ancak ... gücünü açık biçimde göstermesinden sonra artırılmalıdır" | M | 8: XU100 günlük yorumları (oran yok) | boyut-risk | kilit: Tansu kural/formül vermedi |
| R257 | rejim | "düşüşe katılan şirket sayısının yükselişe katılanlardan belirgin biçimde fazla" | M | 4.5 (piyasa genişliği NH-NL) (kavram) | rejim | ölçüm kolu |
| R258 | rejim | "fiyat 14226.96, WMA21 14443.45 seviyesinin altında ve WMA aşağı eğimli" | M+G | 4.5 (XU100 WMA21, M R258) | rejim | ölçüm kolu |
| R258 | momentum-seçim | "MACD histogramı negatif ... RSI 45.0 ... WaveTrend kısa vadede zayıf" | M | 8: XU100 günlük yorumları (eşik yok) | seçim-momentum | kilit: Tansu kural/formül vermedi |
| R258 | teyit-tetik | "İlk anlamlı olumlu gelişme WMA21'in (14443.45) geri alınması, ardından 14722.02 ... tepenin kırılması" | M | 4.5 (XU100 WMA21 kolu) (kavram) | teyit | ölçüm kolu |
| R258 | bölge | "en yakın demand bölgesi 13633.00-13659.74"; "14230.73-14301.92 aktif Bearish FVG" | M | 8: XU100 günlük yorumları (o güne özgü seviye) | bölge | bilgi: işlem kuralı değil |
| R258 | stop-geçersizlik | "14140.43 altına kalıcı geçiş, en yakın Bullish FVG desteğinin kaybedildiğini gösterir." | M | 8: XU100 günlük yorumları (o güne özgü seviye) | çıkış | bilgi: işlem kuralı değil |
| R258 | rejim | "Güçlü yükselen yapısal trend (7 temas) ... kırılmış"; "Teknik uyum skoru 35/100" | M+G | 8: XU100 günlük yorumları (puan formülü yok) | rejim | kilit: Tansu kural/formül vermedi |
| R259 | bölge | "DEMAND / TOPLAMA" kutusu ve alt paneller (görsel) | G | 4.1 (talep bölgesi) (kavram); 8: Ahengin uyumu satırı | bölge | bilgi: işlem kuralı değil |
| R259 | teyit-tetik | "Ahengin uyumu" | T | 8: Ahengin uyumu satırı (tanım yok) | teyit | kilit: Tansu kural/formül vermedi |
| R259 | diğer | "Şunu biraz geliştirmenin önemine inandım şu an." | T | 8: Ahengin uyumu satırı | araç-öğrenme | bilgi: işlem kuralı değil |
| R260 | ölçüm-ilkesi | "Ben skewness'i tek başına AL/SAT sinyali olarak kullanmam. ... dağılım filtresi olarak kullanırım." | T | 3.1 ölçüm (rolling skewness filtresi, T R260) | ölçüm-yöntemi | ölçüm kolu |
| R260 | momentum-seçim | "Momentum pozitif + Rolling Skewness pozitif ise ... olumlu bir kombinasyondur." | T | 3.1 ölçüm (skew > 0 kesimi) | seçim-momentum | ölçüm kolu |
| R260 | ölçüm-ilkesi | "log getirilerini ... 63 günlük Rolling Skewness ... Cornish-Fisher Skewness/Kurtosis düzeltilmiş VaR" | T+G | 3.1 ölçüm (63 gün, log getiri); VaR 8: CWENE skewness satırı | ölçüm-yöntemi | ölçüm kolu |
| R260 | rejim | "Skew < -0.50: Tail-risk negatif, dikkat. ... Skew > +1.00: Çok güçlü pozitif asimetri" | T | 3.1 ölçüm (eşikler −0,50 / 0 / +0,50) | rejim | ölçüm kolu |
| R260 | teyit-tetik | "Fiyat yükseliyor + momentum pozitif + skewness sıfırın üzerinde yükseliyor ise ... olumlu bir konfluens." | T | 3.1 ölçüm (skew > 0 kesimi) | teyit | ölçüm kolu |
| R260 | teyit-tetik | "Skewness +0.50 üzerine çıkarken fiyat da teknik dirençlerini kırmaya başlarsa ... benim ilgilendiğim konfluens" | T | 3.1 ölçüm (> +0,50 kesimi) | teyit | ölçüm kolu |
| R260 | rejim | "Skewness'in yönü kadar değişimi de değerlidir. Mesela -1.0 → -0.5 → 0 → +0.3 → +0.6" | T | 3.1 ölçüm (skew değişimi kesimi, 21 gün YORUM) | rejim | ölçüm kolu |
| R260 | felsefe | "Pozitif skewness = fiyat kesin yükselecek demek değildir. Skewness trend ölçmez." | T | 8: CWENE skewness satırı | araç-öğrenme | bilgi: işlem kuralı değil |
| R261 | formasyon/bölge | "33.10 → 48.30 Dalga 1, ardından 35 civarında 2? ... 32.5–36 bandındaki güçlü demand bölgesine denk" | T+G | 3.2 E; 5.1 E sadakat (CWENE, T R261) | formasyon | resmi sınav |
| R261 | teyit-tetik | "Son güçlü yeşil mum da bu bölgeden alıcı geldiğini gösteriyor." | T | 3.2 E (giriş FVG/bölge limiti; "güçlü" tanımsız) | teyit | kilit: Tansu kural/formül vermedi |
| R261 | stop-geçersizlik | "33.10 altı: mevcut bullish Elliott sayımı iptal." | T | 3.2 E (geçersizlik Point 0) | çıkış | resmi sınav |
| R261 | giriş | "Agresif yatırımcı 35–36 demand bölgesinin korunmasını fırsat ... muhafazakâr yatırımcı ise önce 40–41.5'in kırılmasını bekler." | T | 3.2 E ölçüm kolları (muhafazakâr giriş, FVG yerine talep bölgesi) | giriş | ölçüm kolu |
| R261 | hedef-çıkış | "40–41.5: ilk ciddi kısa vadeli direnç"; "48.30 üzeri kapanış ... Dalga 3 senaryosu ... güçlenir" | T | 3.2 adım 4 (E hedefi Point 1) | çıkış | resmi sınav |
| R261 | felsefe | "Elliott'taki 2? noktası ile Demand bölgesinin aynı yere denk gelmesi bence önemli bir konfluens." | T | 3.2 akış (bölge zorunlu + tarayıcı) | ilke | ilke: tasarımın kuralı |
| R262 | çift | "kointegrasyon ... stratejinin üzerine inşa edildiği zorunlu bir temel" | M | 3.3 (kapı: rolling eşbütünleşme) | ölçüm-yöntemi | resmi sınav |
| R262 | çift | "korelasyon ile kointegrasyonu birbirine karıştırmaktır ... fiyat farkı zamanla sonsuza dek açılabilir" | M | 3.3 (seçim korelasyonla değil p ile) | ölçüm-yöntemi | resmi sınav |
| R262 | giriş/çift | "pahalı olan varlık açığa satılır (short), ucuz olan varlık alınır (long)" | M | 3.3 (long-only; kısa bacak yok) | giriş | kilit: açığa satış (BIST) |
| R262 | ölçüm-ilkesi | "Johansen veya Engle-Granger gibi kointegrasyon testleri" | M | 3.3 (Engle-Granger) | ölçüm-yöntemi | resmi sınav |
| R262 | rejim | "Piyasa Riskinin İzole Edilmesi (Market Neutrality)" | M | 3.3 (long-only rotasyon bu ilkeyi taşımaz) | portföy | kilit: açığa satış (BIST) |
| R262 | felsefe | "Bu ispat olmadan uygulanan herhangi bir ikili işlem stratejisi ... yüksek riskli bir yön tahminine dönüşür." | M | 3.3 (kapı) | ilke | ilke: tasarımın kuralı |
| R263 | teyit-tetik | "BOM sinyalinin geldiği yerde şartlar da müsait ise çok etkili olabileceğine dair ilk kanıtlar gelmeye başladı" | T+G | 8: BOM sinyali (T R263; Tansu'ya sorulacak) | teyit | kilit: Tansu kural/formül vermedi |
| R263 | diğer | "2 tavan üst üste vermiş tabi hala geliştirilmeye açık bir sistem. Çalışıyoruz bakalım" | T | 8: BOM sinyali | araç-öğrenme | bilgi: işlem kuralı değil |

## Tablo 1: rol × durum çapraz tablosu

Sütun başlıkları B değerlerinin kısaltmasıdır: kilit: bilanço = kilit: bilanço verisi; kilit: veri = kilit: VIX-opsiyon-gün içi-emir defteri verisi; kilit: kural = kilit: Tansu kural/formül vermedi; ilke = ilke: tasarımın kuralı; bilgi = bilgi: işlem kuralı değil.

| rol | resmi sınav | ölçüm kolu | kilit: bilanço | kilit: veri | kilit: açılış | kilit: kural | kilit: açığa satış | ilke | bilgi | BAĞSIZ | toplam |
|---|---|---|---|---|---|---|---|---|---|---|---|
| seçim-momentum | 5 | 19 | 9 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 37 |
| evren-likidite | 8 | 8 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 23 |
| bölge | 28 | 29 | 0 | 6 | 0 | 5 | 0 | 0 | 4 | 0 | 72 |
| formasyon | 39 | 15 | 0 | 0 | 0 | 9 | 1 | 0 | 0 | 0 | 64 |
| teyit | 9 | 39 | 4 | 13 | 1 | 17 | 0 | 0 | 1 | 0 | 84 |
| giriş | 12 | 9 | 0 | 6 | 0 | 9 | 2 | 0 | 1 | 0 | 39 |
| çıkış | 36 | 11 | 1 | 8 | 0 | 6 | 0 | 0 | 1 | 0 | 63 |
| boyut-risk | 9 | 5 | 2 | 0 | 0 | 6 | 0 | 0 | 2 | 0 | 24 |
| rejim | 7 | 28 | 1 | 12 | 0 | 15 | 0 | 0 | 2 | 0 | 65 |
| değerleme-temel | 0 | 0 | 105 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 107 |
| portföy | 3 | 17 | 6 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 27 |
| ölçüm-yöntemi | 15 | 11 | 0 | 2 | 0 | 6 | 0 | 0 | 2 | 2 | 38 |
| ilke | 4 | 2 | 0 | 0 | 0 | 0 | 1 | 42 | 0 | 0 | 49 |
| araç-öğrenme | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 49 | 0 | 52 |
| ürün-hedefi | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 7 |
| **toplam** | **175** | **193** | **130** | **53** | **1** | **81** | **5** | **42** | **69** | **2** | **751** |

Doğrulama: 175 + 193 + 130 + 53 + 1 + 81 + 5 + 42 + 69 + 2 = 751. Sayılar bu dosyadaki satırlardan hesaplandı (06.10, sürüm 5.2).

Sürüm 5.1 tablosuyla fark: R245–R263'ün 19 "kanıt yok" satırı, tweet metinleri kaynaktan çekilince 73 fikir satırı oldu (697 − 19 + 73 = 751); "kilit: kanıt" sütunu kalktı. Yeni satırların durumu: resmi 18, ölçüm 20, kural vermedi 7, açığa satış 2, ilke 11, bilgi 15. Eski tablo dosyadaki satırlarla üç hücrede uyuşmuyordu (ölçüm kolu 172 yazılıydı, satır 173; ilke 33 yazılıydı, satır 31; açığa satış 2 yazılıydı, satır 3); yeni tablo satırlardan sayıldı.

Eski sürümle fark: eski "dışarıda" 106, "kapsam dışı" 36, "strateji değil" 65 ve "ikinci dalga" 154 satır, bu tabloda kilit, ilke ya da bilgi satırı olarak durur. Hiçbiri atılmış sayılmaz.

## Tablo 2: kilit türüne göre sayı ve kilidi açan iş

| durum ve kilit | satır | kilidi açan iş |
|---|---|---|
| resmi sınav | 175 | Kilit yok. Tasarımın resmi koluna (S1, S2, S3, 6 rapor, 5.1 sadakat) girdi; sınav sonucu bekleniyor. |
| ölçüm kolu | 193 | Kilit yok. Ölçüm kolunda sınanır; kol hiç resmi olmaz (tasarim-8 5.2). Resmi yapmak için ayrı karar ve Holm m artışı gerekir. |
| kilit: bilanço verisi | 130 | İş Yatırım mali tablo kaynağı (tasarim-8 §8 ilk satır, §9 madde 4). Kaynak henüz doğrulanmadı (denetim D3). Veri gelince ilk sınanacak filtreler: R059, R060. |
| kilit: VIX-opsiyon-gün içi-emir defteri verisi | 53 | Bu veri tasarım-8 §2 tablosunda "Yok" sütunundadır (VIX, opsiyon IV, gün içi veri, emir defteri, kümülatif delta). Açan iş: bu veriyi sağlayacak bir kaynak bulmak. Kaynak şimdilik yok. |
| kilit: açılış fiyatı | 1 | Açılış fiyatı içeren veri kaynağı (tasarim-8 §2: açılış yok). O zamana kadar AOF vekili kullanılır; mum gövdesi tam kurulamaz. |
| kilit: Tansu kural/formül vermedi | 81 | Tansu'ya sorulabilir (kural, eşik, pencere, formül). Ya da yorum tarayıcısı: standart tanımla, sadakat hedefi olmadan, ikinci dalgada eklenir (tasarim-8 §8 Klasik formasyonlar). Yorum tarayıcısı tümüyle bizim tanımımız olur. |
| kilit: açığa satış (BIST) | 5 | BIST'te açığa satış sınanamaz (tasarim-8 3.3: long-only). Açan iş: kısa pozisyonu sınayacak bir kapsam kararı ve masraf kuralı. Şimdilik yok. |
| ilke: tasarımın kuralı | 42 | Kilit yok. İlke tasarımın kendisidir; yer sütunu uygulandığı yeri gösterir. 3 satırın karşılığı yok (Tablo 3). |
| bilgi: işlem kuralı değil | 69 | Kilit yok. Fikir işlem kuralı değildir (kitap, Python dersi, ürün hedefi, makro not, araştırma fikri). Sistemi öğrenme ve ürün tarafından besler. |
| BAĞSIZ (kilit listesinde yok) | 2 | Açık pozisyon (COT) verisi: tasarim-8 §2 bu veriyi anmaz. Veri kaynağı bulunursa kilit türü eklenir. Aşağıdaki BAĞSIZ listesine bakın. |

## Tablo 3: "ilke: tasarımda karşılığı yok" satırlarının tam listesi (3 satır)

Bu fikirler sistemin nasıl kurulacağını söyler, ama tasarımda (TASARIM.md, tasarim-8.md) uygulandığı yer bulunamadı. Karşılık uydurulmadı.

| R | fikir | neden karşılık yok |
|---|---|---|
| R101 | "Borsada "yönü" bilmek zorunda değilsiniz." | KAPANDI (06.10): 3.3'e yazıldı; kilit açığa satış. |
| R111 | "kendinize has, özgün bir yapı kurmaktan geçer" (model sentezi) | KAPANDI (06.10): tasarımın kendisi farklı modellerin sentezidir (3); P5. |
| R122 | "Öyle bir matematiksel yapı kurun ki sistem sürekli kendini yenilesin." | KAPANDI (06.10): 5.2'ye önceden yazılmış walk-forward ölçüm kolu eklendi (R138 ile). |

## BAĞSIZ satırlar (kilit sütununa sığmayanlar, 2 satır)

Kilit listesine sığmayan satırlar bunlardır. Diğer 5 eski BAĞSIZ satır (R077, R128, R203, R243 x2) tasarim-8 §8 "Kalan yan fikirler" satırıyla bağlandı: R077, R128, R203 ve R243 büyük mum cümlesi için "Tansu kural/formül vermedi"; R243 Fading the Gap için "açığa satış (BIST)".

- R227: "Konsantrasyon... Kümelenme... Pozisyon Büyüklüğü" (COT mantığı, açık pozisyon) Tasarımda açık pozisyon verisi anılmaz; 4.5 R227'yi yalnız fiyat-hacim konumu için anar.
- R227: "Eğer Konsantrasyon yüksek ama Kümelenme düşükse: Piyasayı az sayıda "balina" domine ediyordur." Tasarımda açık pozisyon verisi anılmaz; 4.5 R227'yi yalnız fiyat-hacim konumu için anar.

### Denetim kontrolü: denetim-tasarim-8.md Tur 1 ve Tur 2 "kapandı" denenler

Tasarım-8 sürüm 5.1 metniyle karşılaştırıldı. Kapandığı doğrulananlar: Y1 (Gartley TP2 oranı 0,618·0,786/0,214 = 2,27; harfiyen TP1 1,40 yazılı, ölçüm kolu), Y2 (AB=CD BC/AB [0,382; 1,00], D = C − 1,0·(A−B), CD 1,272·AB altı kapanış: risk 0,272·AB, ödül 0,618·AB, oran 2,27), Y3 (ADX/CMF 3.1 ölçüm kolu), Y4 (R224 ilk kısım ve ikinci kâr alma 4.4 ölçüm kolları; adım 4 R224 harfiyen, SMA250 G-dış R212), Y5 (4.1 eşik aday kümeleri; 3.2 madde 5 haftalık ve FVG kuralı), O1–O4, O7 (R260 parametre kaynağı kalktı), O8, O9, O10, O11, O12 (2.1 listesi), O13 (HAO_PD dipnotu), O14, N2 (§9 madde 2 "Kapandı"), N3 (4.4 adım 1 AB=CD kapanış istisnası), N4 (a) (5.3 atfı yok), N4 (c) ("m'yi 2 fazla artırır"), N4 (d) ("dört hat" ve beş aşama), N4 (f). S3 önceki koşu sayıları (−%9,0; [−%14,6; −%2,8]; 91 işlem; Holm p 1,0; 18/18 negatif) tasarımda yazılı.

Kapandı denmesine rağmen ya da hiç anılmadan açık kalanlar (tasarım-8.md'de hâlâ görünenler):
1. N4 (b) / D2: §2 tablosunda "piyasa değeri (TASARIM 5.1)" duruyor; alan listesi TASARIM §4 Kaynaklar'dadır. "TL hacim (2000'den)" ile indirme başlangıcı (2010) ayrı yazılmadı.
2. D3: "İş Yatırım mali tablo kaynağı" (§8 ilk satır ve §9 madde 4) doğrulanmadı; tasarım "var" gibi yazıyor.
3. O16: 3.2 H ölçüm kolu "C'den alım, D'de satış": giriş günü (C'nin doğrulandığı ilk gün + ertesi AOF) yazılı değil; bakış ileri riski kalıyor.
4. O15 kalanları: mevsimsellikte (4.5) hesabın yalnız geçmiş 10 yılı kullandığı yazılı değil; 4.4 boyutta Tansu'nun risk / 2 ATR formülüyle farkı YORUM olarak yazılı değil; 3.1'de ay başı yeniden kurmada ortak hisselerin işlemi ve 252 günlük geçmişi olmayan hisse yazılı değil.
5. O6: 3.2 madde 4 ve §1 hâlâ T R234 "Kritik Kural"ı genel kapı atfı olarak anar; R234'ün 1:1,5 şartı %55 isabete bağlıdır, "isabete bağlı" notu yok. Dayanak M R222 yeterli.
6. Tur 2 N1 (S3 yeni kuralı): 3.3 artık seçim, kapı ve çoklu test notunu yazıyor; "boş dünya denetiminde şans tabanı ölçülür" resmi kayıttan önce yapılacak iş olarak açık.
7. Yeni (bu üretimde görüldü): R156 APO ve R154 çift anılıyor (yukarıdaki notlar).
