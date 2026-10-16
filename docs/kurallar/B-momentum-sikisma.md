# B. Momentum, osilatör, sıkışma, mum ve trend-filtresi GİRİŞ kuralları

Kapsam: Tansu X Veri Havuzu notları ve görselleri. Tarih: 05.10.2026.

## 0. Okuma kılavuzu ve genel sınırlar

Kaynak kökü: `C:\Users\levent\Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`
Görsel kökü: `...\assets\<klasör>\`. Not dosyaları kökte. Aşağıda "gp-NN" = `gorsel-paket-NN-*.md` + `assets/gorsel-paket-NN-*/`.

1. Kaynak türü tanımları GLOSSARY'dedir. Bu belgede her görsel Read ile açıldı ve parametreler görselden doğrulandı.
2. Notlardaki Claude özeti, "Levent şunu belirtti" cümleleri ve formül önerileri ikinci eldir. Notlardaki bölümlerin çoğu ("Cevo çıkarımı", "state machine", "backtest matrisi") Tansu'nun sözü DEĞİLDİR. Bu belgeye alınmadı.
3. Atıf: Ham birinci eldir. Ham'da yazar adı yalnız şu notlarda geçer: `tweet-bollinger-kuyruklari...` (X bağlantısı, yazar @The_Tansu_) ve `kaynak-cwene-skewness-...` (iki X bağlantısı). `tweet-medyan-temelli...` notunda yazar yalnız Kaynak bölümündedir (ikinci el). Diğer notlarda Ham'da yazar yok. YORUM: Tansu'nun görselleri olduğu varsayımı not başlıklarından gelir.
4. Beş görsel NotebookLM imzası taşır (notlar imzayı adlandırır): gp-98, gp-100 (2. görsel), gp-104, gp-111, gp-115. gp-113'te imza yok. Bunlar yapay zekâ infografiğidir; Tansu'nun kendi aracının çıktısı değildir. Görsel olarak birinci eldir (GLOSSARY); "NotebookLM görseli" etiketi yalnız bilgi verir. gp-98 ve gp-113 için sahip D'dir.
5. Tansu'nun kodu görsel olarak şu notlarda vardır: bullish engulfing kodu, realized vol kodu (gp-124), mum gölge kodu (gp-76), klasik günlük pivot kodu (`gorsel-paket-100-gunluk-klasik-pivot-formul-kod`, 1. görsel). Clenow ve HalfTrend kodu Ham metni olarak vardır, görselde yoktur.
6. Gizli göstergeler: gp-46/48/49 mavi/turuncu çizgiler, gp-65 alt paneller, gp-74 özel subplot, gp-31 üç alt panel. Adları bilinçli kapatılmış. Uydurulmadı.
7. Tansu'nun kanıtı hemen her yerde seçilmiş örnektir. Sistematik backtest tablosu bu kapsamda yok. İstisna: gp-75 (tek sembol, tek dönem, Strateji %19.1 / B&H %10.8 / Sharpe 0.67) ve gp-63 (yalnız DEY tablosu).

"Günlük OHLCV yeter" ifadesi hesaplanabilirlik ölçüsüdür: kaynak Yahoo/yfinance günlük OHLCV (BIST `.IS`) varsayar. Projenin güncel veri durumu ayrıdır: İş Yatırım, Yahoo yok, açılış yok (TASARIM 5.1). Gün içi, emir defteri, bilanço (CFO) dışarıdadır.

---

## 1. EMA sıkışma oranı (ratio) dedektörü - KRDMD

- Kaynak: `gorsel-paket-67-krdmd-ema-sikisma-ratio-formasyon.md`; `assets/gorsel-paket-67-krdmd-ema-sikisma-ratio/01-krdmd-20gun-ema-sikisma-ratio.jpg`.
- Tansu'nun ifadesi (görsel başlığı, birebir): `KRDMD | Son 130 Mum | EMA Sıkışması | Tolerans %1.2 | Min 3 gün | 1 periyot`; üst satır: `Tespit edilen sıkışma periyodu: 1` / `1. 2025-12-17 -> 2026-01-14 (20 gün) Ort.Ratio: %0.64`. Sarı kutu etiketi `20g %0.64`. Alt panel `Ratio %`, kesikli kırmızı çizgi `Eşik %1.2`. Lejant: EMA20 (31.92), EMA50 (30.74), EMA100 (29.58), EMA200 (28.43). Sağ üst `Son Kapanış: 36.68`. Metin (Ham): sıkışma zamanlarını iyi tespit eder, o alanda formasyon varsa "mis gibi kar bırakır"; "sıkışma rasyosu sizin tecrübenize kalmış". Süre eşiği için Ham'da söz yok.
- Tanım (görselden okunan + boşluk):
  1. Günlük close'tan EMA20, EMA50, EMA100, EMA200 hesapla. (görsel)
  2. Her bar için bir `Ratio %` hesapla. FORMÜL GÖRSELDE YOK. Seçilen formül ve sadakat sonucu KURALLAR §3 ve §4'tedir (KRDMD dışında doğrulanmadı); ölçümler `docs/sadakat.md`'dedir. (bilet 04, 14.10)
   3. Örnekte `Ratio <= %1.2` olan ardışık barlar sıkışma adayıdır; genel eşik seçimi YORUM'dur (Ham + araç görseli, gp-67:21, g1; gp-65:21).
   4. Örnekte ardışık bar sayısı >= 3 ise dönem "tespit edilen" olur; genel süre seçimi YORUM'dur (Ham + araç görseli, gp-67:21, g1; gp-65:21).
  5. Tarama penceresi son 130 mum. (görsel)
  6. Dönem özeti: başlangıç, bitiş, süre, dönem ortalaması ratio. (görsel)
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA periyotları | 20, 50, 100, 200 | görsel (lejant) |
| Tolerans | %1.2 (örnek ayarı) | görsel (başlık + eşik çizgisi); genel eşik YORUM |
| Minimum süre | 3 gün (örnek ayarı) | görsel (başlık); genel süre YORUM |
| Pencere | son 130 mum | görsel |
| Ratio formülü | görselde yok; KURALLAR §3 seçti | YORUM (sadakatle seçildi; KRDMD dışında doğrulanmadı; KURALLAR §4, `docs/sadakat.md`) |
| "gün" = bar mı takvim günü mü | 2025-12-17..2026-01-14 = 28 takvim günü, "20 gün" yazıyor; bar sayısı olması olası | YORUM |
| Ratio adayları (aralık/medyan, CV, ATR-normal) | notta üç aday | not (ikinci el), Tansu'nun değil |

- Giriş / stop / hedef / bozulma: YOK. Görsel yalnız tespit ve sonraki fiyat yolunu gösterir (sıkışmadan sonra 36.68). Not: "giriş zamanı, yön tetikleyicisi verilmedi".
- Belirsiz: sıkışma sonrası yön ve giriş; "1 periyot" yalnız sayaç. (Ratio formülü: görselde yok, KURALLAR §3'te seçildi; yukarıdaki 2. adım.)
- Kanıt: tek KRDMD örneği, seçilmiş pozitif. Sistematik tablo yok. Ratio sıkışma boyunca ~0.5-1, sonra %10+ (görsel okuması).
- Günlük bedava veriyle uygulanabilir mi: EVET (sıkışma dedektörü); giriş kuralı yok. Parametreler (4 EMA, %1.2, 3 gün) ve KURALLAR §3'ün seçtiği oran formülü günlük kapanışla hesaplanır (bilet 04, 14.10).
- Kaynak güveni: parametreler birinci el; giriş yok; ratio formülü kaynakta yok (YORUM; KRDMD'de sadakatle eşleşti).

## 2. EMA sıkışma "Pre Signal" (ICBCT)

- Kaynak: `gorsel-paket-65-ema-sikisma-pre-signal-bir-gun-yuzde5.md`; `assets/gorsel-paket-65-ema-sikisma-pre-signal/01-icbct-ema-sikisma-pre-signal.png`, `02-matrix-sonraki-mum.png`.
- Tansu'nun ifadesi: görsel başlığı (düşük çözünürlük, okunabildiği kadarıyla): `ICBCT | Son Kapanış: 14.55 | Son 130 Mum | [kapalı alan] | 1 periyot | ▲1 BULL ▼0 BEAR ⚡0 CONFLICT`; mavi kutuda `▲ AKTİF 3g`; yeşil üçgen "Pre Sig" etiketli; EMA lejantı 4 çizgi: `EMA?? (14.44)` (ilk etiket okunamıyor, aşağıya bakın), `EMA50 (14.29)`, `EMA100 (14.31)`, `EMA200 (14.42)`. Görselde ilk EMA etiketi okunamıyor (20 ya da 30); KRDMD ayarı 20/50/100/200; sadakat ölçümü 20 ile uyuştu (S). Bu belirsizlik tek yerde burada durur; taslaklar (M, T8) buna atıf verir, hiçbir kural bu etikete dayanmaz. Üç alt panel; adları beyaz kutuyla kapatılmış. Metin (Ham): "Bir günde %5 Ema sıkışması"; parametrelerin detaylarını verip stratejiyi anlatamayacağını söyler, "öz fikri zaten verdim", "Siz daha detaylandırabilirsiniz". Pre Signal okuyla işaretlenen mum, matrix ekranında "soon gün gelen mum" olarak görünür (yazım hatalı; "son gün" mü "sonraki gün" mü belirsiz).
- Tanım: hesaplanamaz. Yalnız: 4 EMA yakın, kutu `AKTİF 3g` (sıkışma 3 gündür aktif okuması), BULL/BEAR/CONFLICT sayacı (sinyal sayımı). Alt panel kimlikleri bilinmiyor.
- Parametreler: hepsi gizli. Tablo: `AKTİF 3g` (görsel, anlamı belirsiz); 130 mum (görsel); geri kalan YOK.
- Giriş/stop/hedef: yok. Ham'da sonuç beyanı yok; "Bir günde %5" ifadesinin anlamı açıklanmamış. `02-matrix-sonraki-mum.png` yalnız sonraki mumu gösterir (yeşil mum, hacim artışı, iki çizgili alt osilatör).
- Belirsiz: her şey (eşik, periyot, alt paneller, matris mantığı).
- Kanıt: tek örnek, tek gün; sonuç beyanı yok.
- Uygulanabilir mi: HAYIR (özel parametre, gizli). Fikir olarak Kural 1 ile birleştirilebilir.
- Güven: görsel birinci el, kural gizli.

## 3. Demand bölgesinde EMA5/8/13 sıkışması

- Kaynak: `gorsel-paket-106-demand-ema-squeeze-supply-outcome.md`; `assets/gorsel-paket-106-demand-ema-squeeze-supply-outcome/01-demand-ema-squeeze-breakout-supply-outcome.png`.
- Tansu'nun ifadesi: görselde HİÇ yazı yok (513x347). Yalnız yeşil/kırmızı kutular, üç renkli çizgi, kırmızı ok. Ham metni (Ham'da yazar yok; R198) şunu anlatır: demand bölgesi içinde EMA'lar birbirine yaklaşıp yataylaşır ("Ben 5-8-13 kullandım"); gerilen yay; agresif giriş talep bölgesinin alt sınırı/alt fitil; güvenli giriş ilk güçlü uzun yeşil breakout mumunun kapanışı veya retest; stop talep bölgesinin hemen altı (kutu altı kapanış analizi iptal eder); ilk hedef üstteki supply (arz) bölgesi.
- Tanım (Ham): (1) demand bölgesi var. (2) EMA5, EMA8, EMA13 birbirine yaklaşıp yatay. (3) giriş: bölge alt sınırı (agresif) veya ilk uzun bullish kırılım mumu / retest (güvenli). (4) stop: demand altında kapanış. (5) hedef: üst supply bölgesi.
- Parametreler: EMA 5/8/13 (Ham; görselde lejant yok). Bölge sınırları, "yaklaşma" ölçüsü, "uzun mum" ölçüsü YOK.
- Kanıt: tek seçilmiş örnek; sembol/periyot yok; sağ uçta ikinci sıkışma (karar bekliyor).
- Uygulanabilir mi: KISMEN. EMA kısmı kolay; demand bölgesi tanımı ayrı kural ailesi (A grubu). Eşikler Tansu'dan gelmiyor.
- Güven: Ham (kural metni birinci el); görsel etiketsiz.

## 4. EMA5/8/13 dizilimi + yükselen destek tepkisi / retest (AKSGY, gp-117, gp-103, gp-64)

- Sahipleri: A §12 (gp-117 ve gp-103: lejant, başlık, temas sayısı, parametreler, Tansu'nun yorumu) ve A §4 (gp-64: düşen trend kırılımı + talep + hacim + EMA5/8/13). Burada tekrar edilmez. (bilet 04, 14.10)
- Momentum yönünden okuma: EMA5/8/13 dizilimi tarayıcı etiketidir, giriş kuralı değildir; MACD için periyot, eşik ve sinyal koşulu yoktur; ADX periyodu ve eşiği A §12'dedir.

## 5. Dragonfly Doji + EMA sıkışması çıkışı (gp-71)

- Kaynak: `gorsel-paket-71-dragonfly-doji-ema-squeeze-exit.md`; `assets/gorsel-paket-71-dragonfly-doji-squeeze/01-dragonfly-doji-ema-sikisma-cikisi.png`.
- Tansu'nun ifadesi: görselde yazı yok (eksen Mar 1 .. Apr 12; 5-6 çizgi EMA benzeri, kesikli turuncu çizgiler, hacim paneli sarı hacim ortalaması). Metin (Ham): dragonfly doji, "ortalamalar kesişmiş", sıkışma alanından çıkmış; "ortalamaların sıkışma alanları genelde patlamaya işaret eder".
- Tanım (notun mum geometrisi; eşikler Tansu'nun DEĞİL):
  `range=high-low; body=|close-open|; lower_shadow=min(open,close)-low`. Dragonfly = küçük gövde + uzun alt gölge + üst gölge yok.
- Parametreler: `body_max`, `lower_shadow_min`, `upper_shadow_max`, `high_location_max` hepsi YOK. EMA tipleri/periyotları YOK (görselde lejant yok).
- Giriş/stop: yok. Not "agresif/güvenli tetik" önerir; Tansu'dan gelmiyor.
- Kanıt: tek örnek, sonuç yok, sembol yok.
- Uygulanabilir mi: KISMEN. Mum geometrisi günlük OHLC ile hesaplanır; eşikler YORUM olarak seçilmeli. Tansu kuralı değildir.
- Güven: Ham yalnız yorumdur; kural yok.

## 6. Gravestone Doji (haftalık tepe uyarısı, gp-70)

- Kaynak: `gorsel-paket-70-haftalik-gravestone-doji-risk.md`; `assets/gorsel-paket-70-gravestone-doji/01-haftalik-gravestone-doji.png`.
- Tansu'nun ifadesi (Ham): "arkanıza bakmadan kaçmanız gereken mum gravestone doji - mezar taşı dojisi"; haftalık grafikte "canlı canlı gömer". Görselde yalnız kırmızı kutu içinde uzun üst gölgeli mum (eksen 0-150), etiket yok.
- Tanım: strict geometri notta var (Cevo). Eşik yok.
- Parametreler: yok. "haftalık" = metinden.
- Giriş/çıkış: ÇIKIŞ/uyarı kuralı. Giriş değil. Stop yok.
- Kanıt: tek örnek, sonrası görünmüyor.
- Uygulanabilir mi: KISMEN (haftalık veri günlükten türetilir; eşikler YORUM).
- Güven: Ham + görsel (uyarı; eşik yok).

## 7. Volatilite rejimi "rehavet" (v_t / Theta, gp-36)

- Kaynak: `gorsel-paket-36-volatilite-rehavet-yon-bagimsiz-kirilim.md`; `assets/gorsel-paket-36-volatilite-rehavet-kirilim/01-volatilite-rejimi-rehavet-oklari.png`.
- Tansu'nun ifadesi: alt panel başlığı `Volatilite Rejimi: Mevcut (v_t) vs Ortalama (Theta)`; mor çizgi v_t, turuncu kesikli çizgi Theta (yavaşça azalıp ~2.2-2.4'e yaklaşır), gri bant (anlamı verilmemiş); üst panelde kırmızı aşağı / yeşil yukarı ok kümeleri. Metin (Ham; yazım hataları düzeltilmiş): "Çizgi çizmeye gerek yok; kırmızı oklar illa düşeceği anlamına gelmez, oynaklığı belirler. Rehavet ortamı vardır ve fiyat bir yöne kırılacaktır."
- Tanım: v_t ve Theta isimleri ortalamaya dönen (CIR/Ornstein-Uhlenbeck benzeri) bir volatilite modeli düşündürür; modelin kendisi verilmedi. Okların koşulu (v_t ile Theta ilişkisi) verilmedi.
- Parametreler: yok. Oklar YÖN sinyali değil (Tansu açıkça).
- Giriş: yok. Yön kırılım sonrası belli olur (Tansu).
- Kanıt: tek grafik, 2024-2026; oklar 2024 başı, 2025 Mart-Nisan'da (aşağı ok + yeşil ok kümesi), v_t Nisan 2025 başında ~4.3'e fırlar.
- Uygulanabilir mi: HAYIR (model tanımsız). Gerçekleşen volatilite ile yaklaşık değişken YORUM olurdu.
- Güven: görsel birinci el, kural yok.
- VRP tarayıcısı (`gorsel-paket-05-bist-vrp-scanner`; Ham Tansu'nun metni, görsel birinci el; bilet 04, 14.10): RV = son dönemde gerçekleşen oynaklık; IV = piyasanın beklediği oynaklık; VRP = IV − RV. VRP yüksek = VOL SAT (aşırı panik veya coşku; trendin yataya sarması veya dönüşü beklenir); VRP negatif = VOL AL ("fırtına öncesi sessizlik"; sert kırılım beklenir). Tansu "büyük oranda kârlı işlemler" der; işlem satırı yok. Görsel: `BIST Variance Risk Premium (VRP) Scanner (2024-01-01 / 2026-08-01)`, dört panel (VRP sıralaması, RV/IV karşılaştırması, Dollar Gamma ve Realized Vol haritası, sinyal dağılımı); lejant `Implied Vol Proxy` ve `Realized Vol 21d`; VOL SAT ve VOL AL için eşik çizgileri var; etiketlerin sayıları okunur: `(0.025)` (üstte, kırmızı kesikli çizgi; VOL SAT) ve `(-0.005)` (sıfıra yakın çizgi; VOL AL). Düşük çözünürlük: etiket başları çizgiyle örtülü, yalnız sayılar okunur. IV gerçek opsiyon verisi değil, tanımsız bir vekildir. Uygulanabilir mi: HAYIR (IV vekili tanımsız; opsiyon verisi TASARIM 3: kapsam dışı). Ayrıca VOL AL'ın "negatif VRP = sessizlik" okuması işaretle çelişir: IV − RV < 0, gerçekleşen oynaklığın beklenenden yüksek olduğu anlamına gelir (YORUM: kaynak yorumu belirsiz).
- VRP ve model-free varyans kesişimi (`tweet-varyans-risk-primi-model-free-kesisim`; Ham Tansu'nun metni, proje fikri; bilet 04, 14.10): iki kod yazılır; (1) gerçek IV'li varyans risk primi: "sessiz ama patlamaya yakın hisseler"; (2) modelden bağımsız varyans: IV'ye göre ± yönde belirli oranda hareket edecek hisseler. İki kümenin kesişimi "volatilite kaynaklı kazanç kapısı", "yatırım noktası". Eşik, formül, veri kaynağı yok ("detaylı anlatacağım"; devamı havuzda yok). Uygulanabilir mi: HAYIR (gerçek IV verisi yok).

## 8. "Mavi çizgi sıfır" / Mom Eşiği 0.15 / Kırılma Eşiği 0.0 / Pozisyon Büyüklüğü Çarpanı (gp-46, gp-48, gp-49)

- Kaynak: `gorsel-paket-46-sagliksiz-yukselis-mavi-sifir-kesisi.md`, `gorsel-paket-48-smrtg-fiyat-volatilite-birlikte-artis.md`, `gorsel-paket-49-saglikli-yukselis-fiyat-vol-ters-iliski.md`; `assets/gorsel-paket-46-sagliksiz-yukselis/01-mavi-sifir-kesisi-kirmizi-rejim.png`, `assets/gorsel-paket-48-smrtg-fiyat-vol/01-smrtg-fiyat-vol-birlikte-artis-defansif.jpg`, `assets/gorsel-paket-49-saglikli-price-vol/01-fiyat-yukari-mavi-sifir-altinda.png`.
- Tansu'nun ifadesi:
  - Görsel etiketleri (birebir): gp-46 `Mom Eşiği (0.15)` (mor noktalı yatay çizgi) ve kırmızı kesikli `...Eşiği (0.0)` (kısmen örtülü; gp-48'de `Kırılma Eşiği (0.0)` okunuyor; not gp-46'da "Sıfır (0.0)" yazmış, görsel gp-48 ile uyumlu okuma "Kırılma Eşiği (0.0)"); gp-48 alt panel başlığı `Pozisyon Büyüklüğü Çarpanı` iki seviye `(Tam)` ve `(...fansif)` = Defansif. Soldaki eksen -0.2..0.3, sağdaki -0.2..0.2. Fiyat panelinde yeşil (gp-46: koyu kırmızı) rejim gölgeleri.
  - Metin (Ham): gp-46 "İşte sağlıklı olmayan bir yükseliş. Mavi çizgi sıfırı yukarı kestiği anda kırmızı bölgede oluşan yükselişler büyük oranda patır patır geri gelir." gp-49 "Sağlıklı yükseliş böyle olur; fiyat çıkarken alt paneldeki mavi çizgi 0'ın altına iner ve oralarda gezinir; quant strateji farklı görmektir." (yazım düzeltilmiş). gp-48 (Ham, özet): SMRTG'de yeni çılgınlık başladı, sistem pozisyonu kapatıp defansif pozisyon aldı; fiyatla volatilitenin aynı anda artması genellikle kötü biter.
- Tanım (kaynak-literal olay): `mavi seri sıfırı yukarı keser AND kırmızı rejim aktif` -> yükseliş sağlıksız, geri verme riski. Tersi: fiyat yükselirken mavi seri < 0 -> sağlıklı. Çarpan durumu: ikili (Tam / Defansif). Defansif'te çarpanın sayısal değeri YOK.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Mom Eşiği | 0.15 | görsel (gp-46) |
| Kırılma Eşiği | 0.0 | görsel (gp-48; gp-46 örtülü) |
| gp-48'de mor eşiğin konumu | sol eksende ~0.2, sağ eksende ~0.15 (piksel okuması): eşik sağ eksene (turuncu seriye?) ait olabilir | YORUM |
| Mavi/turuncu seri kimliği, formülü, pencere | yok | BELİRSİZ |
| Kırmızı rejim üretici | yok | BELİRSİZ |
| Çarpan Tam / Defansif değeri | yok | BELİRSİZ; YORUM: Tam 1,0 ve Defansif 0 (kapalı) bizim seçimimizdir, genel eşleme açık değil (Ham, gp-48:21; E K7'den taşındı, bilet 04) |

- Giriş/stop/hedef/bozulma: giriş yok. Çıkış/küçültme = çarpanın Defansif'e inmesi (gp-48, Ham; "pozisyonu kapatıp").
- Belirsiz: mavi ve turuncu serilerin kimliği. Not "fiyat getirisi ile volatilite değişimi ilişkisi" aday diyor; doğrulanmadı.
- Gözlem (YORUM; E K7'den taşındı, bilet 04, 14.10): gp-48'de dört geçişte mavi serinin sıfır geçişi ile Tam/Defansif değişimi birlikte görülür; bu katalogda ilişki adayı olarak okunur, tek neden veya tam üretim koşulu doğrulanmaz. Mor 0,2 çizgisinin rolü açık değildir. Çıkışı yapanın çarpan mı olduğu belirsizdir (metin "kapatıp", grafik çarpan). Seri yeniden üretilemez: hangi "volatilite" olduğu (gerçekleşen, ATR, implied) bilinmiyor; aday 20 günlük getiri std değişimi (YORUM). Defansif dönemlerde fiyat ağırlıkla sert düşmüş görünür; sistemin P&L sonucu yok.
- Kanıt: üç seçilmiş grafik (SMRTG gp-48, diğerleri sembolsüz). Sistematik sonuç yok.
- Uygulanabilir mi: HAYIR (gösterge tanımsız).
- Güven: eşik değerleri birinci el (görsel); mantık Ham'da yalnız sözle anlatılır.

## 9. Gizli pozitif uyumsuzluk (hidden bullish divergence; gp-60, gp-61, gp-74)

- Kaynak: `gorsel-paket-60-hidden-bullish-divergence.md`, `gorsel-paket-61-hidden-uyumsuzluk-takip-hatirlatmasi.md`, `gorsel-paket-74-ozel-subplot-hidden-bullish.md`; `assets/gorsel-paket-60-hidden-bullish-divergence/01-fiyat-higher-low-indikator-lower-low.png`, `02-bes-gunluk-yukselis-sonucu.png`, `assets/gorsel-paket-61-hidden-divergence-watchlist/01-hidden-bullish-divergence-takip-gorseli.png`, `assets/gorsel-paket-74-ozel-subplot-hidden-bullish/01-ozel-subplot-gizli-pozitif-uyumsuzluk.png`.
- Tansu'nun ifadesi:
  - gp-60 görsel 1 sol üst etiket (kısmen kesik, okunabildiği kadarıyla): `... | Swing=15 sol-only | MinGap=15`. Fiyatta mavi çizgi (düşük dip -> daha yüksek dip), alt panelde kırmızı kesikli çizgi (osilatör dibi daha düşük). Görsel 2: mor dikey çizgi sonrası ~5 yeşil mum, eksen 200-700 (yaklaşık 500-550 -> 650-700).
  - gp-74: etiket sağ üstte `Son: 1578.00 | Getiri: +63.4% | β = 0.132` (β benzeri değerin adı okunaksız); lejant `MA20`, `MA50`, `Bullish Divergence`; fiyat panelinde sarı elmas, yeşil üçgen, `DIV` etiketleri; özel subplot kapalı.
  - gp-61: kırmızı çizgiler, yeşil üçgenler, sarı noktalar; anlamları açıklanmadı. Metin: "Gizli uyumsuzlukları takip ediniz, arkadaşça hatırlatma."
  - Metin (Ham): gp-60 "beş günde %29 getiri; fiyat dipleri yükselirken alt indikatör dipleri düşüyor; ana trend korunur, momentum soğur, düzeltme sonrası trend devam eder." gp-74 "gücü nerede arandığına bağlı; subplot yaygın bir gösterge değil, sinyalleri iyi çalışıyor."
- Tanım:
  1. Fiyatta iki ardışık onaylı dip: `P2 > P1` (higher low).
  2. Aynı bölgede osilatörde `O2 < O1` (lower low).
  3. Önceki trend yukarı (Ham, gp-60: "ana trendin yukarı yönlü gücünü koruduğunu").
   4. YORUM: bizim pivot seçimi solda 15 bar kontrolü; iki pivot arası en az 15 bar. `Swing=15 sol-only` ve `MinGap=15` etiketleri vardır; eşitlik, pivot yenileme ve seçim algoritması kaynakta yoktur (Araç görseli, gp-60 g1, üst etiket).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Swing | 15 (sol-only) | görsel (gp-60 etiketi); anlam YORUM |
| MinGap | 15 | görsel; anlam YORUM |
| Osilatör | gizli | BELİRSİZ |
| Trend filtresi | "yükseliş trendi" (tanımı yok) | Ham |
| Entry tetikleyicisi, stop, hedef | yok | BELİRSİZ |

- Giriş/stop/hedef: yok. gp-60: 5 günlük %29 (metin, hesaplanamıyor); gp-74: +63.4% etiketi dönem/ilişki belirsiz.
- Kanıt: seçilmiş iki örnek (gp-60, gp-74); gp-74'te çok sayıda DIV işareti var, fakat sonrası ayrıştırılmamış.
- Uygulanabilir mi: KISMEN. Geometri ve Swing/MinGap günlük veriyle kodlanır; hangi osilatörün kullanılacağı YORUM (RSI/MACD/AO vb.), Tansu'nun "özel subplot"u değil.
- Güven: parametre etiketi (görsel) ve geometri (Ham) birinci el; osilatör, tetik ve stop yok.

## 10. Bullish engulfing (tweet kodu) ve KLMSN "Engulfing + EMA34 Tepki/Kırılım"

- Kaynak: `tweet-bullish-engulfing-mum-kodu.md`, `gorsel-paket-92-klmsn-engulfing-ema34-marker.md`; `assets/tweet-bullish-engulfing-mum-kodu/01-bullish-engulfing-kodu.png`, `assets/gorsel-paket-92-klmsn-engulfing-ema34-marker/01-klmsn-engulfing-ema34-tepki-kirilim.png`.
- Tansu'nun ifadesi: kod görseli (birebir, tüm sinyal):
  ```
  def signal(data, open_column, close_column, buy_column, sell_column):
      data = add_column(data, 5)
      for i in range(1, len(data)):
          try:
              if data[i, close_column] > data[i, open_column] and \
                 data[i - 1, close_column] < data[i - 1, open_column] and \
                 data[i, open_column] < data[i - 1, close_column] and \
                 data[i, close_column] > data[i - 1, open_column]:
                  data[i, buy_column] = 1
          except: pass
      return data
  ```
  KLMSN grafiği başlığı: `KLMSN.IS - Engulfing + EMA34 Tepki/Kırılım`; lejant `Candlestick`, `EMA5`, `EMA8`, `EMA13`, `EMA34`, `Buy Signal` (yeşil ▲). Eksen ~16 Şubat - 26 Şubat 2026; fiyat 30-34; EMA'lar 30.7-31.2'de kümelenir.
- Tanım (kod): t günü yeşil, t-1 kırmızı, `open[t] < close[t-1]`, `close[t] > open[t-1]` (katı eşitsizlikler, yalnız gövde, fitil yok). `buy=1` işaretler. Sell sütunu kullanılmıyor.
- KLMSN: kural kodu verilmedi. EMA5/8/13/34 kümesi + "tepki/kırılım" etiketi. Buy Signal ▲ iki tane (görselde doğrulandı): ~24 Şubat mumunun altında ve geniş yeşil ~26 Şubat mumunun altında. Her işaret kendi günündeki mumun altındadır; ilk ▲ geniş mumdan iki bar önce durur.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Engulfing koşulları | 4 koşul, katı | görsel (kod) |
| EMA'lar (KLMSN) | 5, 8, 13, 34 | görsel (lejant) |
| "EMA34 tepki/kırılım" koşulu | yok | BELİRSİZ |
| Önceki düşüş, bölge, hacim şartı | yok | BELİRSİZ |
| Min gövde eşiği | yok | görsel (kodda yok) |

- Giriş/stop/hedef: yok (yalnız `buy=1`).
- Kanıt: kod için yok. KLMSN: tek örnek, sonuç yok.
- Uygulanabilir mi: EVET (engulfing dedektörü, günlük OHLC ile birebir). EMA34 teyit kuralı HAYIR.
- Güven: kod birinci el; KLMSN kuralı yok.

## 11. Tweezer Bottom + talep bölgesi

- Kaynak: `tweet-tweezer-bottom-talep-bolgesi-backtest.md` (görsel yok).
- Tansu'nun ifadesi (Ham, birinci tekil): "tweezer bottom mumunu yazayım taramasını da yapayım"; getirisine bakacağını söyler; "talep bölgesinde şahane fırsatlar sunuyor". Tansu sayısal kural vermedi.
- Tanım: iki ardışık mumun dipleri yakın. Not "same_low" toleransı, ATR oranı vb. önerir. Tamamı Cevo.
- Parametreler: yok (hiçbiri Tansu'dan). Giriş/stop/hedef yok.
- Kanıt: yok. Uygulanabilir mi: KISMEN (fikir; tüm sayılar YORUM). Güven: Ham (niyet beyanı; kural yok).

## 12. A/D (Accumulation/Distribution) ve EMA kesişimi (ISCTR, gp-75)

- Kaynak: `gorsel-paket-75-isctr-ad-ema-walk-forward.md`; `assets/gorsel-paket-75-isctr-ad-ema-walk-forward/01-isctr-ad-ema-strateji-bh-drawdown.jpg`.
- Tansu'nun ifadesi (görsel, birebir): panel başlıkları `ISCTR Günlük Mum & İşlemler`, `Accumulation/Distribution | EMA Crossover`, `Kümülatif Getiri: Strateji vs Buy & Hold`, `Strateji Drawdown`; üst şerit `Strateji: 19.1%  B&H: 10.8%  Sharpe: 0.67`; yeşil ▲ ve kırmızı ▼ işlem işaretleri; mavi A/D çizgisi + sarı kesikli EMA çizgisi; drawdown en derin ~-17%. Metin (Ham; platform formülleri): `Enter long: AD() [op] Ref(Mov(AD(),opt1,E),1)`, aynı biçimde Close long/Enter short/Close short; `OPT1 = 3`; walk-forward ile optimize; amaç 1-2 günlük hızlı işlem. Karşılaştırma operatörleri Ham metninde kayıp.
- Tanım: Ham'da `AD > EMA` yönü vardır (Ham, gp-75:41,49). YORUM: bizim eşlememiz `AD_t > EMA_3(AD)_{t-1}` ise long; `<` ise long kapat/short. Dört işlem satırının gecikme ve kesişim koşulları açık değildir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA periyodu (opt1) | 3 (güncel; walk-forward) | Ham |
| A/D formülü | yok (standart CLV*hacim kümülatif) | YORUM |
| Operatörler | yok | BELİRSİZ |
| Walk-forward pencere/ızgara | yok | BELİRSİZ |
| Dönem, maliyet | yok | BELİRSİZ |

- Giriş/çıkış: dört satırın operatörleri eksiktir; yukarıdaki eşleme YORUM'dur (Ham, gp-75:41,49). Stop yok.
- Kanıt: tek sembol ISCTR, seçilmiş dönem: strateji %19.1, B&H %10.8, Sharpe 0.67 (görsel). Tarihler ve işlem sayısı görünmüyor.
- Uygulanabilir mi: EVET/KISMEN. A/D günlük OHLCV ile hesaplanır. Operatör yönü ve walk-forward ayrıntısı YORUM. Sonuçlar yeniden üretilemez.
- Güven: sonuçlar birinci el (görsel); kural metni Ham'da var, operatörler kayıp.

## 13. APO ortalamaya dönüş prototipi (gp-85)

- Kaynak: `gorsel-paket-85-apo-mean-reversion-yukselen-kanal.md`; `assets/gorsel-paket-85-apo-mean-reversion-yukselen-kanal/01-apo-ema-mean-reversion-sinyalleri.jpg`.
- Tansu'nun ifadesi (görsel): lejant `ClosePrice`, `Fast10DayEMA`, `Slow40DayEMA`, `buy` (kırmızı ▲), `sell` (yeşil ▼); eksen Tarih 2014-07 ... 2018-01. Metin (Ham): "can sıkıntısından yazdım ... ama çalışıyor"; "Mean reversion, absolute pricing oscilator kullanılarak oluşturulan bir strateji"; yükselen kanal desteği çizilirse "mis".
- Tanım: `APO = EMA10(close) - EMA40(close)` (isimden ve lejanttan; formül görselde yok). Sinyal formülü, eşik YOK. Markerlar yerel dönüşlerde yoğun; Ham yalnız "mean reversion" stratejisi der; APO uçlarında al/sat kuralı vermez.
- Parametreler: EMA 10 ve 40 (görsel). Eşik, çıkış, kanal filtresi YOK.
- Giriş/stop/hedef: yok. Sonuç yok.
- Uygulanabilir mi: KISMEN (APO hesaplanır; sinyal eşiği YORUM). Güven: parametre birinci el; kural yok.

## 14. 12 aylık momentum on-dilim (decile) stratejisi + DEY tablosu (gp-63)

- Kaynak: `gorsel-paket-63-bist-momentum-dey-backtest-denetimi.md`; `assets/gorsel-paket-63-bist-momentum-dey/01-bist-momentum-dort-ay-dey-tablosu.jpg`.
- Tansu'nun ifadesi: görsel yalnız bir tablodur: sütunlar `Hisse`, `Baslangic`, `Bitis`, `Referans_Fiyat`, `Bitis_Kapanis`, `Donem_En_Yuksek`, `DEY_Marj_%`. 20 satır, hepsi `Baslangic 2025-12-31`, `Bitis 2026-04-20`, `Bitis_Kapanis NaN`. Örnekler (görselden doğrulandı): NIBAS.IS 3.62 / 11.60 / 220.44; DOGUB.IS 48.46 / 146.50 / 202.31; TMPOL.IS 290.25 / 703.00 / 142.20; KUYAS.IS 52.40 / 94.85 / 81.01; ... POLTK.IS 9982.50 / 10235.00 / 2.53. Strateji metni (Ham, özet): "2015'ten bugüne BIST'te 500+ hisse; her ay son 12 aylık getiriye göre 10 eşit grup; en yüksek grubu eşit ağırlıkla bir ay tut, listeyi yenile; en yüksek momentum grubu yıllık getiri ve Sharpe'ta açık ara önde; backtest'te maliyet, vergi, likidite yok; ayda 50+ hisse yenilemek pahalı."
- Tanım:
  1. Her ay her hisse için son 12 aylık getiriyi hesapla.
  2. 10 eşit gruba böl. En üst decile al.
  3. Eşit ağırlık, 1 ay tut, tekrar sırala.
  DEY marjı (tablodan, rakamla doğrulanabilir): `DEY = Donem_En_Yuksek / Referans_Fiyat - 1` (NIBAS: 11.60/3.62-1 = %220.44).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Lookback | 12 ay | Ham |
| Dilim sayısı | 10 | Ham |
| Tutma süresi | 1 ay | Ham |
| Ağırlık | eşit | Ham |
| Son ayı atlama (skip-month) | yok | BELİRSİZ |
| Evren | 500+ BIST hissesi (2015'ten) | Ham |
| DEY tablosu hangi seçimden geldi | yok | BELİRSİZ |

- Giriş/çıkış: her ay yeniden sıralama ("her ay bu sıralamayı güncelledim"; ayın hangi günü belirtilmemiş). Stop yok.
- Kanıt: metinde "açık ara"; sayı yok. Görseldeki tablo momentum sonucunun kanıtı DEĞİL; tek dönem DEY listesi (belki seçilen hisselerin dört aylık tepe getirisi). Bitiş kapanışı NaN olduğundan kapanış getirisi yok.
- Uygulanabilir mi: EVET (günlük kapanıştan 12 aylık getiri, aylık yeniden dengeleme). Skip-month, düzeltme ve evren YORUM.
- Güven: strateji metni Ham (birinci el), sayısal sonuç yok; tablo görseli birinci el.

## 15. Clenow tipi üstel regresyon momentum skoru

- Kaynak: `tweet-clenow-exponential-regression-momentum-bist-projesi.md` (görsel yok; kod notta metin).
- Tansu'nun ifadesi (Ham; kod bloğu):
  ```
  from scipy.stats import linregress
  def momentum_func(price_array):
      r = np.log(price_array)
      slope, _, rvalue, _, _ = linregress(np.arange(len(r)), r)
      annualized = (1 + slope) ** 252
      return annualized * (rvalue ** 2)
  ```
  Metin (Ham): Clenow'un Stocks on the Move yaklaşımı; "detaylı kodunu yazıp denemeler yapacağım" (BIST için).
- Tanım: log fiyata zamanla OLS; yıllıklaştır; R² ile çarp; skorla sırala (hisse seçimi/sıralama).
- Parametreler: lookback YOK. Evren, yeniden dengeleme YOK. 252 (kodda). Giriş/stop/hedef yok.
- Kanıt: yok (plan).
- Uygulanabilir mi: EVET (fonksiyon tam; lookback YORUM). Not: `(1+slope)**252` Clenow'un `exp(slope)**252`'sinden farklı olabilir; kodu olduğu gibi kullan.
- Güven: Ham (kod metin olarak verilmiş).

## 16. HalfTrend "buy" + momentum eşiği (çift kapı)

- Kaynak: `tweet-halftrend-buy-momentum-threshold-kapisi.md` (görsel yok).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok): kod ve sonunda "Nice": `if half_trend[t] == "buy" and momentum[t] > momentum_threshold: # Nice`.
- Tanım: iki koşul AND. HalfTrend burada hazır bir gösterge (durum mu olay mı belirsiz).
- Parametreler: HalfTrend amplitude/kanal sapması YOK; momentum formülü/pencere/eşik YOK.
- Giriş: yalnız long adayı; stop/hedef yok.
- Uygulanabilir mi: KISMEN. HalfTrend (TradingView) günlük veriyle hesaplanır; momentum ve eşik YORUM. Ham'da yazar yok.
- Güven: Ham (yazar yok).

## 17. Momentum değerden önce döner: eğim erken uyarı

- Kaynak: `tweet-momentum-degerden-once-doner-egim-erken-uyari.md`.
- Tansu'nun ifadesi (Ham): "ortalama kullanıyor iseniz eğimlere dikkat edeceksiniz", momentum trader için "sinyal eğiminize dikkat"; "Momentum (Hız), değerden ... önce döner"; "eğimin yön değiştirmesi bir erken uyarı sinyalidir", kesişim onay; kesişimde fiyat "genellikle %5-%10 primlenmiş olur".
- Tanım: `slope = MA_t - MA_{t-K}` negatiften pozitife dönünce uyarı; kesişim teyit. Formüller Cevo.
- Parametreler: MA türü, periyot, K, eşik YOK. "%5-10" = iddia, kanıtsız.
- Uygulanabilir mi: KISMEN (fikir; sayılar YORUM). Güven: Ham.
- DMA kanal eğimi (`gorsel-paket-119-dma-kanal-egim-evre-gecis`; yalnız görsel, metin yok; bilet 04, 14.10): infografik `DMA Kanal Analizi: Trendin Gücünü Anlamak`: kanal eğimi ne kadar dikse yükseliş o kadar güçlüdür; eğim mevcut trendin gidişatını ve gücünü izler; mevcut evre sonraki evrenin tonunu etkiler (zayıf yükseliş, sert düşüş habercisi; hafif düşüş, güçlü yükseliş habercisi). Görselde kaynak imzası yok (Ham yalnız görsel; Ham'da yazar yok). "DMA" açılımı, formül, periyot, eşik, sembol yok: kural tanımsız. Uygulanabilir mi: HAYIR (DMA tanımsız; eğim fikri yukarıdaki §17 ile aynı türdendir).

## 18. Rolling alpha ve rolling skewness (momentum listesine katman)

- Kaynak: `tweet-rolling-alpha-skewness-momentum-liste-katmani.md`, `kaynak-cwene-skewness-2094148699769241961.md`; `assets/kaynak-cwene-skewness-2094148699769241961/cwene-skewness.webp`.
- Tansu'nun ifadesi: CWENE görseli (birebir başlıklar): `CWENE | Skewness & Gaussian Dağılım Analizi`, `Gerçek Getiri Dağılımı vs Gaussian`, `63 Günlük Rolling Skewness` (yatay noktalı çizgiler ~+0.5, 0, -0.5; seri 2025 baharında ~-1, sonra ~+1.2), `Fiyat`. Metin (Ham; X, @The_Tansu_, 30 Ağu 2026): çarpıklık AL/SAT değil, momentum/volatilite/kuyruk riskiyle birlikte yorumlanır; kod log getiri, skewness, kurtosis, 63 günlük rolling skewness ve Gaussian/Cornish-Fisher VaR hesaplar; kabaca sınıf: -0.50 altı belirgin negatif, -0.50..0 hafif negatif, 0..+0.50 hafif pozitif, +0.50 üstü belirgin pozitif; +1 üstünde birkaç büyük günün etkisini ayrıca kontrol et; son CWENE ~+0.2/+0.3, güçlü pozitif rejim sayılmaz. Rolling alpha notu (Ham): "Momentum listelerimize uyguluyoruz. Ne olduğunu anlatacağım."
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Skewness penceresi | 63 gün | görsel (başlık) |
| Eşikler | -0.50, 0, +0.50, +1 | X metni (Ham, kaynak-cwene-skewness) |
| Rolling alpha penceresi, benchmark | yok | BELİRSİZ |

- Giriş kuralı: yok (risk/etiket katmanı). Alpha için hiçbir kural yok.
- Uygulanabilir mi: skewness EVET (63 günlük rolling skewness günlük kapanıştan); alpha KISMEN (benchmark YORUM). Güven: skewness görseli ve tweet metni birinci el (Ham); alpha Ham'da yalnız duyurudur.

## 19. Momentum x faaliyet nakit akışı 5x5 portföy

- Kaynak: `tweet-momentum-faaliyet-nakit-akisi-5x5-portfoy.md` (görsel yok).
- Tansu'nun ifadesi (Ham): her çeyrek evreni momentuma ve faaliyet nakit akışına (CFO) göre bağımsız sırala; her sıralama 5 eşit dilim; `Mom5 x CFO5` hücresi odak.
- Parametreler: momentum formülü ("daha önce anlatılan momentum stratejisi") ve lookback bu tweette YOK. Çeyreklik yeniden dengeleme.
- Uygulanabilir mi: KISMEN/HAYIR. CFO günlük fiyat verisi değil; bedava ve temiz bilanço verisi kısıtlı. Güven: Ham.

## 20. Yüksek ihtimalli günlük işlem: beş kapı

- Kaynak: `tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi.md` (görsel yok).
- Tansu'nun ifadesi (Ham): beş unsur: aktif volatilite, sinyal uyumu/confluence, pozitif momentum, ana trend yönü, uygun risk/ödül. Yükselen trendde yalnız alım, düşende yalnız satış. Risk/ödül `1:2` veya `1:3`; stop her zaman bu orana göre.
- Parametreler: yalnız R/R 1:2 / 1:3. Volatilite, momentum, trend ölçüsü YOK.
- Uygulanabilir mi: KISMEN (yalnız çerçeve; hiçbir kapının ölçüsü verilmedi). Gün içi bağlam olası. Güven: Ham.

## 21. Fincan-kulp (GUBRF)

- Kaynak: `gorsel-paket-58-gubrf-fincan-kulp-matematik-foyu.md`; `assets/gorsel-paket-58-gubrf-fincan-kulp/01-gubrf-fincan-kulp-fibo-kirilim-hedef.png`.
- Tansu'nun ifadesi (görsel, birebir): başlık `GUBRF - Formasyon Tamamlanma: 2025-10-28 | Risk/Reward: 1:2.27`; lejant `Fiyat`, `FİNCAN`, `KULP`, `Fibo Bitiş: 317.00`, `Fibo Başlangıç: 212.20`, `Kırılım Sinyali`; `✅ SİNYAL! 2025-10-24`; `KIRILMA: 300.75`; `HEDEF: 389.30`; Fibo: %0 317.00, %23.6 292.27, %38.2 276.97, %50 264.60, %61.8 252.23, %78.6 234.63, %100 212.20. Metin (Ham): "kendi tarama sistemimin yakaladığı GUBRF grafiği"; hedef "Fincan derinliği kadar yukarı gitme mantığına" dayanır.
- Tanım (görselden aritmetik): hedef = neckline + (neckline - fincan dibi) = 300.75 + (300.75 - 212.20) = 389.30. R/R 2.27 -> örtük stop ~261.7 (YORUM; görsel stop yazmıyor). Fibo seviyeleri 317 - q*(317-212.20).
- Parametreler: fincan/kulp dedektörü, derinlik oranları, kulp sığlığı YOK. Görselde kulp dibi ~240 (%61.8 altı), metin "sığ kulp" diyor (not çelişki bildirir). Sinyal 24.10, tamamlanma 28.10: tarih çelişkisi (görsel).
- Giriş: neckline (300.75) kırılımı = sinyal. Hedef var, stop görselde yok.
- R/R 1:2,27 doğrulaması (E K14'ten buraya taşındı, bilet 04, 14.10): stop yazılı değil. Giriş = 300,75 varsayımıyla ödül 88,55; risk = 88,55 / 2,27 = 39,01; ima edilen stop ≈ 261,74 (not da aynı; Fib %50 264,60'a yakın). Giriş = 317,00 (Fib 0%) varsayımıyla ödül 72,30; risk 31,85; stop ≈ 285,15. İki giriş varsayımı da doğrulanmış değil (YORUM).
- Kanıt: tek örnek, fiyat hedefi aştı (~450+).
- Uygulanabilir mi: KISMEN (hedef formülü net; dedektör yok). Güven: görsel birinci el; dedektör yok.

## 22. Weinstein dört evre (A1CAP)

- Kaynak: `gorsel-paket-56-a1cap-weinstein-dort-evre.md`; `assets/gorsel-paket-56-a1cap-dort-evre/01-a1cap-fiyat-hacim-dort-evre.jpg`.
- Tansu'nun ifadesi: görselde "Weinstein" yazmaz. Etiketler `H`, `L`, `LH`, `HL`, `LL`, `HH` (swing yapısı), kırmızı/yeşil basamaklı dinamik çizgi, uzun sarı ortalama, `Hacim` paneli turuncu hacim ortalamasıyla; eksen Temmuz 2023 - 2026. Metin (Ham): Stan Weinstein'ın "Piyasanın 4 Evresi" çerçevesi; Evre 1 Taban/Birikim, Evre 2 Yükseliş/Boğa ("X haftalık eğriyi ve hacmi arkasına alarak güçlü bir trend başlattığı aşama"), Evre 3 Tepe/Dağıtım, Evre 4 Düşüş/Ayı.
- Parametreler: hepsi YOK (uzun ortalama periyodu, swing kuralı, evre eşikleri).
- Giriş: yok. Ham yalnız evreleri tanımlar (Evre 2 giriş kuralı değildir); HH/HL yalnız görseldeki swing etiketleridir.
- Uygulanabilir mi: HAYIR/KISMEN (YORUM ile 30 haftalık MA gibi). Güven: Ham (evre tanımı); kural yok.

## 23. OBV trend onayı (gp-104)

- Kaynak: `gorsel-paket-104-obv-trend-onayi-senkronizasyon.md`; `assets/gorsel-paket-104-obv-trend-onayi-senkronizasyon/01-obv-trend-onayi-senkronizasyon.jpg`.
- Tansu'nun ifadesi: NotebookLM görseli (yapay zekâ infografiği; Tansu'nun aracı değil). Başlık `OBV Göstergesi ile Piyasayı Anlamak: Trend Onayı`; `Fiyat ve OBV Senkronizasyonu = Yüksek Güven`; `Yükseliş Senaryosu: Güçlü Alım Baskısı` (yükselen OBV + yükselen fiyat); `Düşüş Senaryosu: Güçlü Satış Baskısı`.
- Tanım: fiyat ve OBV aynı yönde ise trend onaylı. OBV = hacmin kapanış yönüyle işaretli kümülatif toplamı (standart).
- Parametreler: yok (pencere, eğim eşiği yok). Giriş/stop yok. Kanıt yok.
- Uygulanabilir mi: KISMEN (OBV günlük veriyle; "yön" tanımı YORUM). Güven: NotebookLM görseli (görsel birinci el; Ham'da metin yok); kural genel bilgi.

## 24. Gerçekleşen volatilite (DOAS)

- Kaynak: `gorsel-paket-124-doas-yfinance-realized-volatilite.md`; `assets/gorsel-paket-124-doas-realized-vol/01-doas-yfinance-realized-volatilite-kodu.png`.
- Tansu'nun ifadesi: kod (görselden, ana satırlar): `hisse_kodu = "DOAS.IS"`; `data = yf.download(hisse_kodu, period="1y", progress=False)`; `data['Getiri'] = data['Close'].pct_change()`; `gunluk_volatilite = data['Getiri'].std()`; `yillik_volatilite = gunluk_volatilite * np.sqrt(252)`; `if yillik_volatilite > 0.40:` "Bu hisse çok hareketli (Volatil). Kemerleri bağla!", aksi halde "Bu hisse daha sakin görünüyor." Çıktı: `Günlük Oynaklık: %2.25`, `Yıllık Volatilite: %35.66`.
- Tanım: tam. Eşik 0.40 yıllık.
- Giriş kuralı DEĞİL; sınıflayıcı. Uygulanabilir mi: EVET. Güven: birinci el (kod+çıktı). Kanıt: tek hisse, örnek çıktı. Not: `auto_adjust` varsayılanı yfinance sürümüne göre değişir (YORUM).

## 25. XU100 EMA50/100/200 sıkışması + KDE tepe kırılımı (gp-68)

- Kaynak: `gorsel-paket-68-xu100-ema-kde-breakout-extension.md`; `assets/gorsel-paket-68-xu100-ema-kde-extension/01-xu100-ema50-100-200-kde-hacim.jpg`.
- Tansu'nun ifadesi (görsel, birebir): başlık `XU100 Son 150 Mum ve KDE Tepe Fiyatları`; lejant `EMA 50 (13310.99)`, `EMA 100 (12840.90)`, `EMA 200 (12256.37)`; `Son Kapanış: 14587.90`; yatay KDE seviyeleri 14235.93, 13834.87, 13590.93, 12979.01, 12379.48, 11292.07, 10911.69, 10518.90; kırmızı kutu EMA'ların birleştiği bölge (2026 başı), altta hacim paneli (en yüksek hacim sağ uçta). Metin (Ham): EMA yakınlaşması dengedir; ~11.300 KDE tepesinin hacimli kırılması ve EMA'ların 50>100>200 dizilimine geçmesiyle hızlanma; fiyat EMA'lardan uzaklaşınca soğuma/retest ihtimali.
- Tanım: EMA50/100/200 sıkışması -> KDE tepe seviyesinin hacimli mumla kırılımı -> 50>100>200. KDE bandwidth/pencere YOK.
- Parametreler: EMA 50/100/200, pencere 150 mum (görsel). KDE parametreleri, sıkışma ölçüsü, hacim eşiği YOK.
- Kanıt: tek endeks örneği (sonuç kapanış 14587.90).
- Uygulanabilir mi: KISMEN (KDE parametreleri YORUM). Güven: görsel birinci el.

## 26. "Sağlıklı trend" CSCO: "TÜM ŞARTLAR SAĞLANDI (GÜÇLÜ TREND)"

- Kaynak: `gorsel-paket-31-saglikli-trend-csco.md`; `assets/gorsel-paket-31-saglikli-trend/01-csco-guclu-trend.jpg`.
- Tansu'nun ifadesi (görsel): başlık `CSCO | TÜM ŞARTLAR SAĞLANDI (GÜÇLÜ TREND)`; fiyat panelinde mavi noktalı dinamik çizgi, 3 alt panel (3 çizgili güç/momentum paneli, çubuk paneli, ±2 aralıklı histogram); panel başlıkları beyaz kutuyla kapalı; eksen Kasım 2025 - Haziran 2026, fiyat ~70 -> 130. Metin: "Sağlıklı trend örneği".
- Tanım: hesaplanamaz. Kaç şart, hangileri bilinmiyor.
- Uygulanabilir mi: HAYIR. Güven: birinci el, kural gizli.

## 27. Bollinger kuyrukları, ortalamaya dönüş, VaR

- Kaynak: `tweet-bollinger-kuyruklari-ortalama-donus-var.md`; `assets/tweet-2087267070752760121/01-normal-dagilim-se-68-95-997.png`.
- Tansu'nun ifadesi: kitap sayfası fotoğrafı: `Örneklem Ortalamalarının Frekans Dağılımı`, `Popülasyon ortalaması, μ`, `-3 SE ... +3 SE`, `%68`, `%95`, `%99,7`. X metni (Ham; 11 Ağu, @The_Tansu_): Bollinger alt ve üst bantları "genelde +-2 standart sapmayı temsil eder", fiyatların %95'i bu sınırlar içinde kalır; bant dışı aşırı alım/satım bölgesidir; -2SE veya -3SE seviyesi nadirdir ve ortalamaya dönüş beklentisiyle "tepki alımı fırsatı" olabilir; VaR belirli güven düzeyinde (örneğin %95) maksimum kaybı hesaplar.
- Tanım: Bollinger için ±2 standart sapma somuttur (Ham, tweet-bollinger-kuyruklari-ortalama-donus-var:25–29). Kaynaktaki −2SE/−3SE ayrı ifadedir; standart sapmayla aynı formüle çevrilmez. Periyot ve tam giriş tetiği yoktur; `z<=-2` aday olayı YORUM'dur.
- Uygulanabilir mi: KISMEN/HAYIR; ±2 standart sapma fikri kaynaklıdır, tam giriş kuralı yoktur (Ham, tweet-bollinger-kuyruklari-ortalama-donus-var:25–29). Güven: Ham (yazar Ham'da).

## 28. Medyan temelli göstergeler / aritmetik ortalama tehlikesi

- Kaynak: `tweet-medyan-temelli-finansal-indikatorler.md`, `tweet-aritmetik-ortalama-outlier-rejim-tehlikesi.md` (görsel yok).
- Tansu'nun ifadesi: kısa alıntı (Ham; Ham'da yazar yok, yazar notun Kaynak bölümünde @The_Tansu_, ikinci el): `Ortalamaları temel alan indikatörler... Medyan temelli çalışın.` Örnek (Ham): 19 gün "100 lira civarında", 20. gün 50 lira. Hesap bizimdir (YORUM): SMA20 = (19*100 + 50)/20 = 97.5, medyan 100.
- Tanım/parametre/giriş: YOK (yöntem yönlendirmesi). Uygulanabilir mi: KISMEN (hareketli medyan hesaplanır; sinyal kuralı YOK). Güven: iki tweet Ham (birinci el); hesap YORUM.

## 29. BIST100 + VIX uzun pozisyon kontrol listesi ve "Piyasanın Nabzı" (gp-113, gp-114, gp-98)

- Sahibi: D, "BIST VIX long: 5 adım kontrol listesi" ve "Piyasanın Nabzı" bölümleri (gp-113, gp-114, gp-98 görsel okumaları, parametreler, belirsizlikler). Burada tekrar edilmez. (bilet 04, 14.10)
- Momentum yönünden okuma: listedeki SMA, Heikin Ashi ve VIX RSI koşulları uygulanamaz; projenin XU100 kaynağı yalnız kapanış verir.

## 30. Hareketli ortalama üstü/altı yön filtresi ve Williams %R + SMA14 (atıf belirsiz)

- Kaynak: `tweet-hareketli-ortalama-ust-alt-trend-yon-filtresi.md`, `tweet-williams-r-sma-swing-strateji-backtest.md` (görsel yok).
- MA filtresi (Ham): "piyasa hareketli ortalamanın altındaysa satış, üzerindeyse alış; Trend is your friend." Periyot, tip YOK.
- Williams %R (Ham; Ham'da yazar yok; not `source_type: user-provided-strategy-spec`): 30 dk, W%R(14), SMA14; uzun: close > SMA14, W%R önce >= -20, -50'ye çekilmiş, -50 üstüne dönüş, bullish mum, sinyal mumu high'ı aşınca giriş, stop en yakın swing low, hedef >= 2R; kısa simetrik (-80). Gün içi veri gerekir. Ayrıntılı backtest sayıları Cevo/Claude çıktısı, Tansu'nun değil.
- Uygulanabilir mi: MA filtresi EVET (parametre YORUM); Williams kuralı HAYIR (30 dk veri; Ham'da yazar yok).
- Güven: Ham.

## 31. Diğer mum ve konum ipuçları (kısa)

- Sponsor Candle (`gorsel-paket-20-sponsor-candle.md`, `assets/gorsel-paket-20-sponsor-candle/01-bullish-bearish-sponsor-candle.png`): görsel etiketleri `Here is a diagram of a bullish Sponsor candle:` / `bearish`, `Bullish Sponsor Candle (SC)`. Kural (Ham): sert yükseliş öncesi son düşüş mumunun bölgesine dönüşte alıcı beklenir. Eşik YOK; öğretici şema.
- Konsolidasyon body-wick (gp-18): sahibi A §14. Burada tekrar edilmez. (bilet 04, 14.10)
- Mum gölge kodu (`gorsel-paket-76-mum-geometri-formasyon-motoru.md`; `assets/gorsel-paket-76-mum-geometri-motoru/01-python-ohlc-golge-analizi.png`): `upper_shadow = high - max(open, close)`, `lower_shadow = min(open, close) - low` (görselde kod ve 4 mumluk örnek çıktı). Birinci el, tam; giriş kuralı değil.
- Fiyat-hacim konum haritası (gp-128): sahibi A §13. Burada tekrar edilmez. (bilet 04, 14.10)
- Mum gövdesi ve hacim uyumu (`tweet-mum-govde-hacim-anomalisi-uyarisi`; Ham, Ham'da yazar yok; bilet 04, 14.10): geniş gövde + yüksek hacim ve dar gövde + düşük hacim "ok"; geniş gövde + düşük hacim ve dar gövde + yüksek hacim "anomali" ("Sizin paranızı istiyorlar Dikkatli olun"). Dört hücreli uyarı filtresi; yön, giriş, çıkış yok. "Geniş/dar", "yüksek/düşük" eşiği yok (YORUM: gövde/ATR ve hacim/ortalama hacim). Anomalinin sonucu ve testi yok. Günlük veriyle: evet (OHLCV).
- İkili dip ve mum tetikleyicileri (`tweet-ikili-dip-mum-tetikleyicileri`; Ham, Ham'da yazar yok; bilet 04, 14.10): "W" formasyonu: dip, yükseliş, aynı dibin yeniden testi (ikinci bacak). En kritik an ikinci dip testidir; orada Çekiç, Yutan Boğa veya Cımbız Dip mumu ikinci bacağın tamamlandığını ve desteğin çalıştığını teyit eder (Cımbız Dip: §11). Adam ve Havva: ilk dip keskin "V", ikinci dip yayvan; ikinci dipteki çoklu mum (örnek: Sabah Yıldızı) akümülasyonun zamana yayıldığını gösterir. Dip benzerlik toleransı, bacaklar arası süre, boyun çizgisi, stop, hedef yok (YORUM); başarı oranı yok. Günlük veriyle: evet (fikir; sayılar YORUM).
- AZTEK bant (`assets/gorsel-paket-127-aztek-ayi-tuzagi/02-aztek-istatistiksel-bant-ayi-tuzagi.png`): etiketsiz regresyon bandı; kural gizli. Uygulanabilir mi: HAYIR.

---

## 32. Sıralı özet

### A. Günlük veriyle sadık kodlanabilir (en tam tanımlı önce)

1. Bullish engulfing dedektörü (kural 10): kod birebir. Eksik: giriş, stop, bağlam.
2. Realized volatilite + %40 eşiği (kural 24): kod ve çıktı birebir. Giriş kuralı değil.
3. Clenow regresyon skoru (kural 15): fonksiyon tam. Eksik: lookback (Ham kodu).
4. Mum gölge hesabı (kural 31): kod birebir; giriş değil.
5. 63 günlük rolling skewness ve eşikler (kural 18): pencere ve sınıflar X metninde/görselde. Giriş değil, etiket.

### B. Kısmen tanımlı (sayı var, bir parça eksik)

1. EMA sıkışması (kural 1): EMA20/50/100/200, %1.2, 3 gün, 130 mum. EKSİK: giriş (oran formülü KURALLAR §3'te YORUM olarak seçildi, bilet 04).
2. Gizli pozitif uyumsuzluk (kural 9): Swing=15 sol-only, MinGap=15. EKSİK: osilatör, trend filtresi, tetik, stop.
3. 12 aylık momentum decile (kural 14): 12 ay, 10 dilim, 1 ay, eşit ağırlık. EKSİK: skip-month, düzeltme, evren listesi (strateji metni Ham).
4. A/D EMA(3) (kural 12): EMA=3. EKSİK: operatör yönü, walk-forward ızgarası (Ham).
5. BIST/VIX izin listesi (kural 29): sahibi D; parametreler ve eksikler orada.
6. APO 10/40 (kural 13): eşik ve sinyal yok.
7. XU100 EMA 50/100/200 + KDE (kural 25): KDE parametresi yok.
8. Fincan-kulp hedef formülü (kural 21): dedektör yok.

### C. Kodlanamaz (gizli veya yok)

- Pre Signal (2), mavi çizgi/Mom Eşiği sistemi (8), volatilite rejimi (7), CSCO tüm şartlar (26), özel subplot (9, gp-74), rolling alpha (18), Weinstein (22), beş kapı (20), Dragonfly eşikleri (5), tweezer (11), Bollinger (27), medyan (28), HalfTrend+momentum (16).
- Williams %R (30): Ham'da yazar yok; veri 30 dk.

### D. En önemli boşluklar

1. Tam (giriş, stop, hedef) üçlüsü iki notta vardır: demand + EMA sıkışması (kural 3, gp-106 Ham: agresif veya güvenli giriş, stop talep bölgesinin hemen altı, ilk hedef supply bölgesi) ve Williams %R + SMA14 (kural 30, Ham: giriş sinyal mumunun high'ı, stop en yakın swing low, hedef en az 1:2). Gerçek boşluklar: gp-106'da bölge sınırı ve "uzun mum" ölçüsü yok; Williams için veri 30 dk. Diğer giriş kurallarında üçlü eksiktir. Fincan-kulp (kural 21) neckline + fincan derinliği hedef formülünü verir; stop görselde yok.
2. Kural 1 için giriş tetiği en yüksek değerli boşluktur (oran formülü KURALLAR §3'te YORUM olarak seçildi; bilet 04, 14.10).
3. Hiçbir kuralın sistematik, maliyetli backtest sonucu yok. Kanıt seçilmiş örnektir.
