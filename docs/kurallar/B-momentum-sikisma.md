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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-fincan-kulp-fibonacci-geri-cekilme-1987192411676942799` — NTHOL fincan-kulp çıktısı, GUBRF ile aynı araç şablonu: Fibonacci ızgarası fincan dibinden sağ yükseğe çekilir ("Dip 34.18 -> Sağ Yüksek 53.95", görsel metni); başlık "Formasyon Tamamlanma: 2025-10-27 (Fibonacci Retracement)", sinyal 2025-11-03 (görsel, açıldı). Ham: "Pivota dikkat edin. Grafikte görünmüyor ama demoklesin kılıcı gibi sallanıypr tepede." Hedef, R/R ve stop yok. "Pivot" sağ yüksek 53,95 mi, etiketsiz mor kesik çizgi (≈60,8, piksel) mi belli değil (YORUM). Tek örnek, sonuç yok. Parametre: Fibo ızgarası = dip 34,18 → sağ yüksek 53,95; %23,6 = 49,28; %38,2 = 46,40; %50 = 44,07; %61,8 = 41,73; %78,6 = 38,41 (görsel, açıldı); kulp dibi ≈42, yani %61,8 çevresinde (piksel, YORUM)

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bb-alt-bant-rsi-obv-takip-1766568865239073269` — BORLS: alım zamanı değil; "BB bandının altına indiğinde sinyalleri takip ederek fırsat verebilir. RSI ve OBV istenilen yerde değil." (Ham). Alt bant tepki fikri, RSI ve OBV ile teyit aranır; eşik yok. Parametre: Bollinger = BB(20, 2) (görsel metni, grafik ekranı; değerler n/a); OBV -164541610 (görsel metni)
  - `tweet-bollinger-bant-kodu-20-2std-1850460386371281374` — Bollinger hesabının kodu birinci elden: orta = SMA(n), üst/alt = SMA ± 2 × örneklem standart sapması, n = 20 varsayılan (görsel, açıldı): "'upper': sma + 2 * stdev". Ham: "EĞİTİM AMAÇLIDIR!". KCHOL 2023 örneği; giriş kuralı yok. Bölümdeki "periyot yok" boşluğunu kapatır. Parametre: Bollinger periyodu = 20 (n: int=20); çarpan = 2; standart sapma = örneklem (pandas rolling.std, ddof=1); orta bant = basit hareketli ortalama; girdi = Close (görsel, açıldı)
  - `tweet-bollinger-mum-grafigi-mplfinance-1850468058747326871` — Tekrar: aynı Bollinger işlevleri (n=20, 2 × standart sapma) bu kez mplfinance mum grafiğiyle: "'upper': sma + 2 * stdev" ve `mpf.plot(data, type='candle', style='charles', addplot=ap0 ...)` (görsel metni). Ham yalnız "@yggdrasil_35" (soruya yanıt). Yeni parametre yok; giriş kuralı yok.

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

---

## 33. Bottle pattern (boğa mum formasyonu, iki mum)

- Kaynak: `tweet-bottle-pattern-boga-mum-formasyonu-1905945897105531327` (Ham; Tansu'nun X gönderisi, 29.03.2025 11:31 UTC; üç gönderilik zincir; görsel: ECILC.IS grafiği, açıldı). Tansu: "Taraması hazır, grupta:)" (tarama kodu notta yok).
- Tansu'nun ifadesi (verbatim): "Bu formasyonda bullish (yükseliş) şu şekilde oluşur. Önce bir boğa mumu gelir. Ardından gelen ikinci mum da boğa mumu olmalı, ancak, alt fitili olmamalı, yani mum en düşük seviyeden açılmış olmalı.Üst fitili olmalı" ve "yani kapanıştan daha yukarı çıkılmış.Aynı zamanda ikinci mumun açılışı, bir önceki mumun kapanışının altında olmalı → bu da “aşağı yönlü bir gap” anlamına gelir." Performans özeti (Ham): "Hit Ratio = 85.71", "Profit Factor = 2.96", "Realized RR = 0.49", "Number of Trades = 7".
- Tanım (Ham; formülleştirme YORUM): mum 1: Close1 > Open1. Mum 2: Close2 > Open2; Low2 = Open2 (alt fitil yok); High2 > Close2 (üst fitil var); Open2 < Close1 (aşağı gap). Görsel (açıldı): kırmızı kutu iki mumu çevreler; ikinci mumun açılışı birinci mumun kapanışının altındadır, alt fitil görünmez, üst fitil vardır. Yeşil "Buy Signal" üçgeni ikinci mumun üzerindedir. Grafik başlığı: "ECILC.IS - Pattern Signal (Same Day)". Aynı grafikte yaklaşık bir hafta sonra kırmızı bir mum üzerinde "Sell Signal" işareti vardır; çıkış kuralı yazılmamıştır.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| mum 1 | boğa mumu (Close > Open) | Ham |
| mum 2 | boğa, alt fitil yok (Open = Low), üst fitil var (High > Close) | Ham |
| gap | Open2 < Close1 | Ham |
| alt fitil toleransı | verilmedi; gerçek veride tam eşitlik nadirdir | YORUM |
| isabet / profit factor / gerçekleşen RR / işlem sayısı | %85,71 / 2,96 / 0,49 / 7 | Ham |
| giriş zamanı | "Same Day": sinyal ikinci mumun gününde; kapanışta mı gün içinde mi belli değil | görsel (açıldı); YORUM |
| çıkış, stop, hedef | yok | belirsiz |

- Belirsiz kalanlar: Çıkış, stop ve hedef kuralı. Backtest evreni (tek hisse mi, BIST geneli mi), dönemi ve maliyeti. "Same Day" girişin kapanışta mı ertesi açılışta mı olduğu. "Alt fitil yok" için tolerans. Tarama kodu paylaşılmadı.
- Tansu'nun kanıtı: Yedi işlemlik performans özeti ve tek ECILC örnek grafiği. Hesap (bizim, YORUM): 0,8571 = 6/7, yani 6 kazanç ve 1 kayıp; 6 × 0,49 ≈ 2,96, yani PF ile gerçekleşen RR 6/7 isabetle tutarlıdır. 6/7 için Wilson %95 aralığı yaklaşık %49–%97 (küçük örneklem). Gerçekleşen RR 0,49 olduğu için ortalama kazanç ortalama kayıptan küçüktür; PF yüksek isabetten gelir.
- Günlük bedava veriyle uygulanabilir mi: Evet, formasyon günlük OHLC ile tanımlanır. Çıkış kuralı olmadan tam sistem kurulamaz.
- Kaynak güveni: Ham (birinci el). Orta-düşük: formasyon sözel ve açık; performans özeti kod çıktısıdır, yeniden üretilemez. Hazırlık K.

---

## 34. X arşivi kısa kayıtları (16.10)
- EMA 12-144-169 standart seti ve optimizasyon önerisi (`tweet-ema-parameter-optimization-1828127951126446388`, `tweet-ema-parametre-optimizasyonu-1840438972859732044`; Ham; Tansu'nun X gönderileri, 26.08.2024 ve 29.09.2024; görsel yok): "Dün çalıştığımız stratejideki üssel ağırlıklı ortalamalar gerçekten olabilecek en iyi parametreler mi? Yani 12-144-169 yerine 11-135-158 yapsam getirim ne olur?" "Tüm stratejilerdeki parametreler standart parametrelerdir. Lütfen bu parametreleri optimize edin. Örneğin 12-144-169 ema, her hissede aynı performans ile çalışmaz." "Brute iyi bir kütüphanedir optimizasyon için." Parametre: yalnız 12, 144, 169 (standart set) ve 11, 135, 158 (soru olarak örnek komşu set). Stratejinin giriş ve çıkış kuralı, arama aralığı, hedef ölçütü ve veri penceresi yok. YORUM: "Brute" kaba kuvvet (ızgara) taraması demektir; üç EMA'nın rolü bilinmez. Tansu "getirim ne olur?" diye sorar, sonuç vermez ve kod bloğu notta yok. Hisse bazlı optimizasyon önerisi E K29 ve E K20 ile birlikte okunur; TASARIM kural parametresini yalnız belge değişikliği ve yeni deneme ile değiştirir (YORUM: hisse başına arama bununla çelişebilir). Günlük veriyle: evet (EMA günlük kapanıştan). Hazırlık X. Kaynak güveni: Ham; düşük, kural yok.
- Haftalık EMA40 ve osilatör (MAKIM; `tweet-haftalik-ema40-osilator-backtest-2044116160908587286`; Ham ve görsel birinci el, görsel açıldı; Tansu'nun X gönderisi, 14.04.2026): "Şimdi şu stratejiye nasıl güvenmeyelim" / "%7'cik bugün. Tertemiz." / "back testlerinizi temiz yapın kontrol edin her ortalama her strateji her hissede çalışmaz hr tahtanın yapısı farklıdır". Görsel: "MAKIM Haftalık Mum Grafik & İşlemler"; haftalık mumlar, kesikli EMA40, yeşil üçgen "Long Giriş", kırmızı üçgen "Long Çıkış"; orta panelin çubukları lejantta "Oscillator (%)" adını taşır ve panel başlığı "(Close /   − 1)" yazar (boşluk görselde de boştur; YORUM: osilatör = (Close / EMA40 − 1) × 100); alt panel "Kümülatif Getiri: Strateji vs Buy & Hold". Parametre: EMA periyodu 40, haftalık (görsel, açıldı). Giriş ve çıkış koşulu, eşik, stop ve maliyet yok. "%7'cik bugün" neyi ölçer belli değil. YORUM: "nasıl güvenmeyelim" ironidir; sonraki cümle (sınama temizliği, hisseye özgü yapı) ve strateji çizgisinin Buy & Hold'a yakın bitmesi uyarı okumasını destekler. Günlük veriyle: haftalık mum günlükten türetilir ve EMA40 hesaplanır; kural olmadığı için kodlanamaz. Hazırlık X. Kaynak güveni: düşük.
- Heikin Ashi yeşil kapanış taraması ve AEFES sonucu (`tweet-heikin-ashi-strateji-backtest-1844839462896832814`; Ham ve görsel birinci el; Tansu'nun X gönderisi, 11.10.2024; üç görsel): Tansu: "AEFES için strateji sonucu (Baya iyi çalışmış)"; "Başlangıç Bakiyesi: 100.000"; "Strateji Final Bakiyesi: 207.546"; "Buy and Hold Final Bakiyesi: 144.057". Görsel 1 başlığı: "Son gün yeşil Heikin Ashi kapanışına sahip hisseler" (görsel metni; 45 sembol). Görsel 2 (görsel metni): "AEFES.IS Price, Scaled RSI and Scaled Smoothed RSI (-40 to 40)". Görsel 3 (görsel metni): "AEFES Heikin Ashi Strategy vs Buy & Hold". Parametre: tarama koşulu = son günün Heikin Ashi mumu yeşil kapanış (görsel metni). RSI periyodu, ölçekleme ve yumuşatma yok. Strateji giriş ve çıkış kuralı, maliyet ve kayma yok; RSI'nin rolü belli değil (YORUM: mum rengi ve/veya ölçeklenmiş RSI sıfır çizgisi). Hesap (bizim): 207.546 / 100.000 = +%107,5; al-tut +%44,1. Ham "Toplam Kar/Zarar (Buy & Hold): 440.57" yazar; 144.057 − 100.000 = 44.057 olmalıdır (not değiştirilmez). Tansu'nun kanıtı: tek hisse, yaklaşık 9 ay, Tansu "baya iyi çalışmış" diye seçmiş; örneklem dışı doğrulama yok. Heikin Ashi için D'de BIST100 örneği vardır (BIST VIX 5 adım). Günlük veriyle: Heikin Ashi günlük OHLC'den hesaplanır, tarama koşulu uygulanır; strateji tanımsız olduğu için sonuç yeniden üretilemez. Hazırlık X. Kaynak güveni: Ham ve görsel birinci el; sayılar tutarlı; kural yok: düşük.
- MOST ve HO kesişim sistemi, THYAO optimizasyonlu sınama özeti (`tweet-most-ho-kesisim-optimizasyon-1779521360609354088`; Ham ve iki görsel birinci el, G1 açıldı; Tansu'nun X gönderisi, 14.04.2024): Ham yalnız "#THYAO iyi görünüyor değil mi:)" der. Görsel G1 (Sistemli Tester özeti, görsel, açıldı): "MOST ve HO Kesiş _OPT", "TURK HAVA YOLLARI AS", "12.04.2022 - 9.04.2024 arası 500 bar 728 gün"; "Optimizasyon Değerleri": OPT1 15, OPT2 3, OPT3 11, OPT4 1, OPT5 5, OPT6 0,5 (OPT7–OPT10 boş); başlangıç bakiyesi 10000, komisyon masrafı 1448,59 (toplam). Sonuç: son bakiye 56800,71, getiri 46800,71 (%468,01); 12 işlem: 8 kârlı (toplam 51492,81), 4 zararlı (toplam 4692,10), 8 long, 0 short; ort. kâr 6436,60, ort. zarar 1173,03, oran 5,49; en kârlı pozisyon 12.05.2023–23.08.2023, 69 bar, 80,05; en zararlı 05.09.2023–11.09.2023, 4 bar, −7,32 (birim yazılı değil; YORUM: yüzde); son işlem AL 21.03.2024 286,07; son durum 309,25. Hesap kontrolü (bizim): 51492,81 − 4692,10 = 46800,71; 51492,81 / 8 = 6436,60; 4692,10 / 4 = 1173,03. G2 ("Data - % Getiri Karşılaştırılması") Data ve Overall çizgilerini çizer, sayı yok (YORUM: Data = al-tut). Kural yok: YORUM yalnız addan okunur (MOST ve HO çizgilerinin kesişimi sinyal verir, sistem optimize edilmiştir). MOST ve HO tanımı, OPT1–OPT6 anlamı, giriş ve çıkış koşulu, optimizasyon aralığı ve ölçütü, örneklem dışı doğrulama ve komisyon oranı yazılı değil. Tansu'nun kanıtı: tek hisse, tek dönem, optimizasyonlu (örneklem içi) sonuç. Hisse bazlı optimizasyonla ilişki: E K29 (karar Levent'te bekliyor). Günlük veriyle: kural tanımı olmadığı için hayır. Hazırlık X. Kaynak güveni: Ham ve görsel birinci el; sonuç görseli iç tutarlı; kural ve parametre anlamı yok: düşük.
- Çoklu bant ve MACD sinyal kümelenmesi, dipten dönüş (ARZUM; `tweet-bant-sinyal-kumelenme-dip-donus-1962958352276754833`; Ham ve görsel birinci el, görsel açıldı; Tansu'nun X gönderisi, 02.09.2025): "Bir de size bunu vereyim benim için dipten dönüş sinyalidir bu. herkes farklı yorumlayabilir" (Ham). Görsel (açıldı): `ARZUM.IS — Son sinyaller (son 10 bar)`; sütunlar `AL -3R`, `AL -2O`, `AL MACD`, `SAT +2A`, `U +3D`, `U i+3`, `U -2D`, `UO -2`. İşaretler: 2025-08-04 AL MACD; 08-06 AL MACD; 08-07 U +3D; 08-08 U i+3; 08-11 SAT +2A; 08-19 AL MACD; 08-28 U -2D; 08-29 AL -3R, AL -2O, U -2D, UO -2; 09-01 AL -2O, AL MACD, U -2D, UO -2; 09-02 AL -2O, U -2D, UO -2. Grafik `ARZUM.IS — Günlük`: mumlar, turkuaz ve turuncu orta çizgiler, çok sayıda kesikli bant, altta MACD histogramı ve yeşil ▲ / kırmızı ▼ işaretleri; fiyat son barlarda sert düşmüş. YORUM: sütun adları açıklanmamıştır; "AL" ve "SAT" sütunları alım ve satım işaretidir; "-3R", "-2O", "+2A", "+3D", "i+3", "-2D", "-2" eksi ve artı bant düzeyleri gibi görünür (harflerin anlamı bilinmiyor). Okuma (YORUM): aşağı bant sütunları ve MACD alımı kısa sürede birlikte tetiklenirse dipten dönüş sayılır; Tansu bar sayısı ve eşik vermez. Hesap kontrolü (bizim): son 3 barda 4 + 4 + 3 = 11 işaret; önceki 7 satırda 1'er = 7 işaret. Parametre: tablo penceresi "son 10 bar" (tarihler ardışık değil: 05.08 ve 12.08 yok; yalnız sinyal olan günler olabilir, YORUM). Sütun anlamları, bant ve MACD ayarları (gizli gösterge), kümelenme eşiği (kaç sütun, kaç bar), tetik gün, giriş, stop, hedef ve çıkış yok. Tansu'nun kanıtı: yok (tek örnek, sonuç yok); "herkes farklı yorumlayabilir" yorum olduğunu belirtir. Günlük veriyle: veri evet (günlük OHLC), kural hayır (sütun formülleri yok). Hazırlık X. Kaynak güveni: kural tanımsız, güven düşük.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-vegas-ema-tek-hisse-optimizasyonu-1846299109302362243` — Vegas (3 EMA) için optimizasyon yapıldı, hisse başına çalışır: "Vegas için optimizasyon yaptım. 3 EMA var. Tam 1 saat sürdü optimizasyon." ve "OPT'leri tek hisse için yapıyoruz." (Ham; üst gönderi de Ham'da: kod, optimizasyon ve getiri hesabı dış bağlantıda, açılmadı). Arama aralığı, ölçüt, sonuç ve örneklem dışı doğrulama yok. Hisse bazlı optimizasyon: karar Levent'te bekliyor.
  - `tweet-vegas-tuneli-ema-optimizasyon-8-150-150-1828161056960827738` — Vegas tüneli EMA seti DOAŞ için optimize edildi: "Soldaki 12-144-169, sağdaki ise optimize edilmiş ema'lar ile getiri grafiği. (8-150-150)" (Ham). Ham sonuç (yanıt): 2022–2024'te al-tut 7,49 kat, 12-144-169 6 kat, optimize 7 kat; "strateji alpha yaratamamış ama getiri eğrisi daha iyileştiği kesin" (Ham). Görselde son değerler yaklaşık 5,4 (al-tut), 4,3 (12-144-169), 5,1 (optimize) (görsel, açıldı; ölçüm). Tek hisse, örneklem içi; giriş ve çıkış kuralı yok. Hisse bazlı optimizasyon: karar Levent'te bekliyor. Parametre: Vegas optimize EMA seti (DOAŞ, 2022–2024) = 8-150-150 (Ham). Okuma notu: Ham sayıları (al-tut 7,49 kat, 12-144-169 6 kat, optimize 7 kat) görseldeki son değerlerle uyuşmaz: creturns ≈5,4, cstrategy ≈4,3 (G1) ve ≈5,1 (G2) (görsel, açıldı; ölçüm). Oranlar tutarlıdır (6/7,49 = 0,80; 4,3/5,4 = 0,80; 7/7,49 = 0,93; 5,1/5,4 = 0,94), düzey farkı açıklanmamış (görselde tepe ≈8,5). Görsel doğru sayılır.
  - `tweet-vegas-tuneli-geri-test-doas-1827794622434640093` — Vegas tüneli 12-144-169 günlük EMA seti DOAŞ'ta al-tutu geçemedi: "2022-2024 yılları arasında vegas tüneli stratejisi doaş getirisine yenik düşmüştür." (Ham). Görselde son değerler cstrategy ≈4,3, creturns (al-tut) ≈5,4 (görsel, açıldı; ölçüm). Tansu EMA'ların optimize edilebileceğini söyler; kod ve veri dış bağlantıda (açılmadı); giriş ve çıkış kuralı yok. Hisse bazlı optimizasyon: karar Levent'te bekliyor. Parametre: Vegas sonucu, DOAŞ 2022–2024, EMA 12-144-169: strateji ≈4,3 kat, al-tut ≈5,4 kat (görsel, açıldı; ölçüm)

---

## 35. SMA kesişimi: 50/200, optimize çift ve al-tut karşılaştırması (TUPRS, EURUSD)

- Kaynak: `tweet-sma-50-200-al-tut-karsilastirma-1831786496518713363` (Ham ve görsel metni), `tweet-sma-geri-test-sinifi-python-1831402232769847775` (Ham ve kod görseli; G2 açıldı), `tweet-sma-kesisim-backtest-istatistikleri-1764270533158342937` (Ham ve iki görsel; G1 ve G2 açıldı), `tweet-sma-kesisim-optimizasyon-48-247-1829983002304086142` (Ham ve görsel metni). Dördü de Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim): 03.03.2024 (TUPRS): "Basit hareketli ortalamalar ile olan kodlama ile trade ile yıllık %60 getiriye ulaştım ancak amaç %100 üstü." 31.08.2024: "50-200 ile başlayan çalışma, optimizasyon ile 48-247 de daha iyi sonuç verdi ve getiri eğrisi yükseldi. Fakat Tüpraş'ın getirisini geçemedi. Farklı hisselerde farklı SMA'lar ile kullanabilirsiniz." 04.09.2024: "Pardon kodda hata vardı. Buyurunuz düzeltilmiş hali." 05.09.2024: "Bazen alıp tutmak en basit ve en etkili yatırım stratejisi olabiliyor, ama doğru zamanda doğru hissede olmak kaydı ile."
- Tanım (kod, görsel, açıldı): `SMABacktester`: fiyat = `Adj Close` (yfinance); günlük log getiri = ln(P_t / P_{t−1}); `SMA_S` ve `SMA_L` = fiyatın kısa ve uzun basit hareketli ortalaması (rolling mean). `position = +1` eğer `SMA_S > SMA_L`, aksi halde `−1` (EURUSD örneği: her zaman piyasada, long ve short); `strategy = position.shift(1) × returns` (sinyal bir gün önceki kapanıştan, uygulama sonraki günün getirisine); kümülatif çarpan = exp(toplam log getiri). Çıktı (EURUSD=X, 50/200, 2004-01-01–2020-06-30): `(1.281065, 0.366977)` = strateji çarpanı ve al-tuttan fark (hesap: al-tut ≈ 0,914). TUPRS testi (03.03.2024) `SmaCross` (backtesting.py) ile SMA(C,30) ve SMA(C,100) kullanır (görsel, açıldı); pozisyon yönü yazılı değil (Exposure %85,8 olduğundan sürekli short değil; YORUM: yalnız long). 31.08.2024 çalışması TUPRS'te 50/200 ile başlar, optimizasyonla 48/247 bulur.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| SMA kısa / uzun (varsayılan) | 50 / 200 | görsel metni ("SMA_S = 50", "SMA_L = 200") |
| optimize çift (TUPRS) | 48 / 247 | Ham; görsel metni |
| SmaCross çifti (TUPRS, backtesting.py) | 30 / 100 | görsel, açıldı |
| fiyat ve getiri | Adj Close, log getiri | kod, görsel metni |
| pozisyon (kod, EURUSD) | +1 / −1, bir gün gecikmeli | kod, görsel metni |
| yıllık hedef | %100 üstü (şimdiki %60) | Ham |

- Belirsiz kalanlar: TUPRS testlerinde pozisyon yönü (long mu long-short mu), maliyet (EURUSD kodunda maliyet yok), optimizasyon aralığı ve ölçütü, 48/247 sonuç sayısı (Ham sayı vermez; WeTransfer bağlantısı notta, dosya yok), üç TUPRS testinde çiftlerin (30/100, 50/200, 48/247) ve dönemlerin farklı olması. Hisse bazlı SMA çifti seçimi: karar Levent'te bekliyor (E K29). TASARIM kural parametresini yalnız belge değişikliği ve yeni deneme ile değiştirir.
- Tansu'nun kanıtı: TUPRS, 2021-01-04–2024-02-23 (1145 gün), 30/100 (görsel, açıldı): Return %339,26 (al-tut %947,13); yıllık getiri %60,43; yıllık volatilite %74,47; Sharpe 0,81; Sortino 2,18; Calmar 1,47; max düşüş −%41,09 (198 gün); 7 işlem; kazanma oranı %28,57; en iyi işlem %410,60; en kötü −%22,83; Profit Factor 8,76; Exposure %85,80. Strateji al-tutun çok altında. EURUSD 50/200: çarpan 1,281 (görsel, açıldı). TUPRS 50/200 ve 48/247: Ham, al-tutu geçemediklerini söyler. Hepsi seçilmiş, tek hisse (TUPRS) ve bir döviz çifti, örneklem içi.
- Günlük bedava veriyle uygulanabilir mi: Evet (yfinance günlük düzeltilmiş kapanış, SMA, sinyal t kapanışı ve pozisyon t+1). TASARIM'da SMA kesişimi kuralı yok; SMA250 çıkışı ayrı kuraldır.
- Kaynak güveni: Orta düşük. Ham ve görsel birinci el; TUPRS'te strateji al-tutu geçmez, örneklem dışı doğrulama yok. Hazırlık K.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bist100-usd-ema50-200-kesisim-1847537834397237420` — BIST100 dolar cinsi EMA 50/200 kesişim grafiği (SMA yerine EMA): başlık "BİST100 EMA Crossover (50-200)", eksen "Price in USD", "BUY SIGNAL" ve "SELL SIGNAL" üçgenleri (görsel, açıldı). Ham: "Allah korusun diyelim." EMA50, EMA200'e yaklaşıyor; olası aşağı kesişim (SELL) uyarısı (YORUM). Sinyal koşulu ve sonuç yok. Parametre: Kesişim çifti = EMA50 / EMA200, fiyat USD cinsi (BIST100 / dolar kuru; görsel, açıldı); yeşil üçgen BUY (EMA50 yukarı keser), kırmızı üçgen SELL (aşağı keser) (görsel, açıldı; yön eşlemesi YORUM)

---

## 36. Üç kırmızı mum SELL sinyali ve performance() kodu

- Kaynak: `tweet-uc-kirmizi-mum-sell-sinyali-performans-kodu-1905475655686353161` (Ham ve görsel, açıldı; Tansu'nun X gönderisi, 28.03.2025). Kod ailesi §10 (engulfing kodu) ile aynıdır: `data[i, open_column]`, `buy_column`, `sell_column`.
- Tansu'nun ifadesi (verbatim): Ham metni kod yazma alışkanlığı üzerine sohbettir: "Şu kod yazmak hastalık gibi bir şey." Kural cümlesi yok. Kural görseldeki koddadır (birinci el; kesik görüntü: `elif` kolu ve `performance()` işlevi görünür, üstteki `if` kolu görünmez).
- Tanım (kod, görsel, açıldı): `elif` kolu, `i` barında şu koşulların hepsi doğruysa `data[i + 1, sell_column] = -1` yazar: (1) `open[i] − close[i] > body`, `open[i−1] − close[i−1] > body` ve `open[i−2] − close[i−2] > body` (üç ardışık kırmızı mum, her gövde `body` değerinden büyük); (2) `close[i] < close[i−1] < close[i−2] < close[i−3]` (kapanışlar dört barlık sıkı düşüş); (3) `sell[i] == 0`. Sinyal bir sonraki bara yazılır. `performance()`: `buy == 1` barı `i` için sonraki ilk `buy == 1` veya `sell == -1` barı `a` bulunur; uzun sonuç = `open[a] − open[i]` (fiyat farkı, yüzde değil). `sell == -1` barı için kısa sonuç = `open[i] − open[a]`. YORUM: BIST alış yönlüdür; bu yüzden SELL yalnız çıkış sinyali olabilir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| ardışık kırmızı mum sayısı | 3 | görsel (kod), açıldı |
| gövde eşiği `body` | yok (değişken; değeri görünmüyor) | belirsiz |
| kapanış dizisi | close[i] < close[i−1] < close[i−2] < close[i−3] | görsel (kod), açıldı |
| sinyal zamanı | i + 1 barı | görsel (kod), açıldı |
| işlem fiyatı | açılış (performance) | görsel (kod), açıldı |

- Belirsiz kalanlar: `body` eşiğinin değeri ve birimi (fiyat farkı mı, ATR oranı mı; YORUM: ATR oranı taşınabilir). Kesilen `if` kolunun içeriği (muhtemelen buy koşulu). `performance()` alış sinyalinde işlemi `open[i]` fiyatından açar, ama §10'daki engulfing kodu `buy[i] = 1` değerini aynı barın kapanışına bakarak yazar; bu bir bar ileri bakmadır (YORUM). SELL kolu sinyali `i + 1` barına yazar ve bu sorunu taşımaz. `sell[i] == 0` koşulunun amacı belli değil (YORUM: önceki kolun yazdığı sinyalin üzerine yazmamak). Maliyet, stop ve hedef yok.
- Tansu'nun kanıtı: Yok (yalnız kod; örnek hisse, çıktı ve sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: Evet (günlük OHLC yeter). `body` değeri seçilmeden kural tam değildir.
- Kaynak güveni: Kod birinci el ve okunaklıdır (transkripsiyon görselle uyuşur); parametre eksik, kanıt yok: düşük. Hazırlık K.

---

## 37. ADX ve ±DI: kesişim sinyali, ADX tepesi ve trend gücü okuması (EREGL, AKYHO)

- Kaynak: `tweet-adx-di-kesisim-sinyali-1853909406553137314` (05.11.2024; Ham, G1 ve G2 açıldı), `tweet-adx-di-kesisim-sinyali-1853912926874214428` (05.11.2024; Ham, yanıt), `tweet-adx-tepe-trend-degisimi-1761664513626046886` (25.02.2024; Ham, kod ve grafik görselleri, G2 açıldı), `tweet-adx-trend-cizgisi-son-temas-1983107758736990412` (28.10.2025; Ham, G1 ve G2 açıldı), `tweet-adx-trend-gucu-filtresi-1840856092592443682` (30.09.2024; Ham, yanıt). Hepsi Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim):
  - DI kesişimi (Ham): "ADX ile +-DI sinyalleri çok sık karşımıza çıkmazlar ama çıktıklarında sinyalleri güvenilirdir.Bunu BB RSI ve Keltner ile kombinlemeye çalışıyorum". Yanıt: "adx ve +-DI kesişimleri var burada. ADX tek değil. Sİnyal kesişimden geliyor".
  - Görsel (açıldı): üç panel: fiyat (`BUY SIGNAL` yeşil ▲, `SELL SIGNAL` kırmızı ▼), `ADX (14)` (kesik çizgiler 20 ve 25), `+ DI / -DI` (`+ DI 14`, `- DI 14`, `ADX 14`). Tarih 2022-01 ... 2023-05. G2 aynı grafiğin ikinci çıktısıdır (Ham'sız yanıt).
  - ADX tepesi (Ham, 25.02.2024, EREGL): "Temmuz 2022'ye bakarsanız fiyatların düştüğü noktada ADX tepede. Bu mevcut trendin değişeceğine bir işaret." "ADX'in anlamlı bir sinyal üretmesi için değerinin 60-100 arasında olması gerekiyor. 40-60 arası göreceli olarak önceki dönemlere göre biraz daha iyi trend işareti verir." "ADX göstergesini ADXR ile beraber kullanırsanız alt pencerede, daha net sinyaller alabilirisiniz." Kod görseli: `data.ta.adx(high='High', low='Low', close='Close', length=14, append=True)` (pandas_ta), `EREGL.IS`, 2020-01-01 ... 2024-02-23. Grafik (açıldı): `OHLC with ADX(14)`.
  - Trend çizgisi son teması (Ham, 28.10.2025, AKYHO): "Son temas olan üçgen işaretini görüyorsunuz,işte orası fiyatın trend çizgisine son temas ettiği nokta. oradan adx eğrisine bakarsanız yükselmeye başladığını görürsünüz." "adx trendin yönü hakkında bilgi vermez ancak gücünü söyler. aşağı trend kuvvetleniyor aşağıdaki örnekte." Görsel başlığı (açıldı): `AKYHO | Temas: 3.26 | Trend: 3.26 | Son gün trend: 3.27 (2025-10-13) | ADX: 38.37 | RSI: 19.05`; `Yükselen Destek Teması`; `İlk Temas: 2025-07-18 | Son Temas: 2025-10-09`; alt panellerde `ADX (14)` ve kesik `ADX 20`, `RSI (14)` ve `RSI 50`. G2: yeşil mumlarla biten kısa düşüş ve kırmızı ok (metinsiz).
  - Yanıt (Ham, 30.09.2024): "Sanırım için tayini ve kuvveti için ADX eklenirse güzel olur" (üst gönderi notta yok; cümle eksiktir: "için tayini" öncesinde bir sözcük düşmüş).
- Tanım (YORUM):
  1. İndikatör: ADX(14), +DI(14), -DI(14) (kod ve görsel). DI kesişimi sinyal: +DI, -DI'yı yukarı keserse BUY, aşağı keserse SELL. Grafikteki işaretler kesişimlere denk gelir. ADX eşiğinin filtre olup olmadığı yazılı değil.
  2. ADX tepesi: fiyat düşerken ADX zirve yapar, mevcut trendin değişeceği anlamına gelir. "Tepe" tanımı yok (YORUM: yerel maksimum ve düşüşe dönüş).
  3. ADX yön vermez, güç verir. Trend çizgisine son temastan sonra ADX yükseliyorsa, o anki trend güçleniyor. AKYHO'da kapanış (≈3,25) destek çizgisinin (3,27) altında; Tansu bunu "aşağı trend kuvvetleniyor" diye okur. Araç A §12'nin "Yükselen Destek Teması" aracıdır (YORUM: destek kırılması ve ADX'in yükselmesi birlikte okunmuş).
  4. Birleştirme: DI sinyali BB, RSI, Keltner ile; ADX ADXR ile. Ayrıntı yok.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| ADX, +DI, -DI periyodu | 14 | kod ve görsel, açıldı |
| Eşik çizgileri (DI grafiği) | 20 ve 25 | görsel, açıldı |
| Anlamlı sinyal için ADX | 60-100 | Ham |
| Biraz daha iyi trend işareti için ADX | 40-60 | Ham |
| EREGL ADX en yüksek | ≈52 (Aralık 2022; piksel) | görsel, açıldı (YORUM) |
| AKYHO ADX; eşik çizgisi | 38,37; ADX 20 | görsel, açıldı |
| Kesişim onayı, çıkış, stop, hedef | yok | - |

- Belirsiz kalanlar: "60-100" eşiği görselle uyuşmaz: EREGL'de ADX hiçbir zaman 60'a ulaşmaz (en çok ≈52), kendi DI grafiğinde ise 20 ve 25 çizgileri var; yazım hatası mı, başka ölçek mi belli değil. Kesişimde ADX filtresi var mı; "tepe" tanımı; ADXR periyodu; DI sinyalinden sonra çıkış; trend çizgisi kırılması ile ADX yükselişinin birleşik kuralı.
- Tansu'nun kanıtı: yok; seçilmiş grafikler. "Güvenilirdir" iddiası ölçülmemiş.
- Günlük bedava veriyle uygulanabilir mi: evet (OHLC; ADX ve DI formülü bilinen Wilder hesabıdır). Kural olarak eksik: onay ve çıkış yok.
- Kaynak güveni: Ham ve görsel birinci el; eşikler birbiriyle çelişir: orta-düşük. Hazırlık K.

---

## 38. Bollinger bandına temas + zıt renkli (rejection) mum kapanışı: 3 SS, 1,5 SD ve ortalamaya dönüş (CUSAN, TUPRS, AFYON, BTCUSD)

- Kaynak: `tweet-bb-3ss-bant-dokunus-zit-mum-1782897014444818512` (yanıt, 23.04.2024; Ham), `tweet-bb-3-sapma-ortalamaya-donus-1786749759627133185` (CUSAN, saatlik, 04.05.2024; Ham ve görsel, açıldı), `tweet-bb-3ss-bant-temas-mum-renk-donusu-1845470513377824768` (13.10.2024; Ham), `tweet-bb-3ss-bant-temas-mum-renk-donusu-tarama-1845850204395692110` (14.10.2024; Ham; iki görsel genel Bollinger grafiğidir, açılmadı), `tweet-bollinger-3ss-zit-mum-1846648064695848972` (AFYON, 16.10.2024; Ham ve görsel, açıldı), `tweet-bollinger-bant-sinyal-siniflama-1763641279819190306` (BTCUSD, 01.03.2024; Ham ve görsel metni), `tweet-bollinger-bearish-rejection-mumu-1763696979119382658` (TUPRS, 01.03.2024; Ham ve görsel metni), `tweet-bollinger-20-gun-1-5-sd-rejection-1763803217983345078` (yanıt, 02.03.2024; Ham). Hepsi Tansu'nun X gönderisidir (birinci el). Aynı bantlar için ±2 SS tepki alımı fikri §27'dedir.
- Tansu'nun ifadesi (verbatim):
  - Yanıt (Ham, 23.04.2024): "BB 3 SS ile tepe ya da dip banda dokunup hemen sonraki ki mum zıt renk yakarsa harika bir işaret olur."
  - Ham, 13.10.2024: "3 SS'li BB'de, fiyat üst banda temas edince ikinci bar eğer kırmızı yanıyor ise ciddi düşüş başlar." "Tam tersi, alt bandda kırmızı iken yeşil yanınca roket ateşlenir." "Grafik açın BB'yi 3SS yapın bakın." "Bununda taramasını yazacağım :)"
  - Ham, 14.10.2024: "ÜSt banda yeşil mum ile temas edip ardından kırmızı mum kapatan hisseler ve alt banda kırmızı le temas edip ardından yeşil ile kapatan hisseleri arıyoruz." "Sizlerde backtestlerinizi yapabilirsiniz." "Bunun taramasını hazırlıyorum. Güvendiğim strateji."
  - AFYON (Ham, 16.10.2024): "3SS BB ve zır mum kapanış. En sevdiğim." Görsel (açıldı): "AFYON.IS AL sinyali verdi.", grafik "AFYON.IS Fiyatı ve Bollinger Bantları" (BB Upper, BB Middle, BB Lower), liste "AL sinyali veren hisseler: AFYON.IS".
  - CUSAN (Ham, 04.05.2024): "#CUSAN ben 20 günlük HO değmek istiyorum gibi bir görüntü var saatlikte. BB 3SS Cuma günü getirisinin bir kısmını aldı. Dikkatli olmakta fayda var". Görsel (açıldı): Matriks, `03Mayıs24 18:00`, `BOL(20,3) U: :27,5899`, `BOL(20,3) M: :25,346`, `BOL(20,3) D: :23,5021`, `RSI(14) :65,3314`; fiyat üst banda yaklaşmış.
  - TUPRS (Ham, 01.03.2024): "Kod Tüpraşta o kadar iyi çalıştı ki, bearish rejection candle'ı hemen yakaladı. Fiyatlar daha gitmez diyor kısacak. Burada sinyal verdi. Ok ile gösterdim. Bu kodu henüz paylaşmadım, bir kaç optimizasyon yapmam lazım." Görsel Plotly benzeri grafik: SMA, Lower Band, Upper Band (görsel metni); sayı yok.
  - Yanıt (Ham, 02.03.2024): "Yukarı, ama bilanço gibi düşünün, 20 günlük HO ve 1,5 SD ile bollinger bandı ve rejection candle sinyali bu. Temel analizde uzun vadede yön mutlaka yukarı". Yanıt gönderisinde Ham, yanıtın hedefini @J0sephRock diye yazar; yanıt üst bilgisi @JR_GPT der (iki ad uyuşmaz; üst gönderi notta yok).
  - BTCUSD (Ham, 01.03.2024; kripto, BIST evreni dışı): "Bitcoin al sinyali 1 hafta önce gelmiş. Bollinger Bandı tepelerinde dolaşıyor ama dikkat bant dışına çıkanı avlarlar :)" "Bu kod ile istediğiniz hisse için sinyale bakabilirsiniz. 1. Ayı 2. Boğa 3. Sİnyal yok" (kod dış bağlantıda, açılmadı).
- Tanım (YORUM):
  1. Bollinger: SMA(20) orta çizgi, üst ve alt = orta ± k × standart sapma. k = 3 ("3 SS", SS = standart sapma, YORUM; CUSAN görselinde BOL(20,3)) ve 1,5 (yanıt gönderisi, "1,5 SD"); periyot 20 günlük (Ham, yanıt gönderisi). Aynı yazarın kod görselindeki k = 2 için §27.
  2. Satış (düşüş) kurulumu: yeşil mum üst banda temas eder; sonraki mum kırmızı kapanır ("bearish rejection candle", TUPRS).
  3. Alış (yükseliş) kurulumu: kırmızı mum alt banda temas eder; sonraki mum yeşil kapanır (AFYON "zır mum kapanış": AL sinyali; "zır" = zıt, yazım hatası, YORUM). Yeşil = Close > Open (YORUM). "Rejection candle" mum tanımı (fitil oranı) yazılı değil.
  4. "Temas" (High ≥ üst band, Low ≤ alt band mi, yoksa kapanış mı) ve sonraki mum (bir mum mu iki mi: 23.04 gönderisi "sonraki ki mum" der, 13.10 "ikinci bar") belirsiz.
  5. CUSAN: üst banda yakın fiyat; hedef orta çizgi (20 günlük HO, Ham); uyarı niteliğinde, kural değil. Hedefi bu kural kullanır: orta çizgi (sözel). §27'deki ±2 SS tepki alımı fikrinin 3 SS ve mum teyitli biçimidir (YORUM).
  6. Sınıflama (BTCUSD kodu): üç çıktı: ayı, boğa, sinyal yok. Koşullar kodda; kod görülmedi.
  7. Uyarı: "bant dışına çıkanı avlarlar": bant dışı kapanışla kırılım alımı tuzak olabilir; ortalamaya dönüş okuması §27 ile uyumlu (YORUM).
  8. Kapsam: BTCUSD kripto örneğidir; kripto kapsamı: karar Levent'te bekliyor.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Bant genişliği | 3 standart sapma ("3 SS"); 1,5 SD (yanıt gönderisi) | Ham |
| Bollinger periyodu | 20 (CUSAN görselinde BOL(20,3); yanıt gönderisinde "20 günlük") | görsel, açıldı; Ham |
| Tetik mum | temas mumunun zıt renkli sonraki mumu (1 veya 2 mum, belirsiz) | Ham |
| Sinyal mumu adı | rejection candle; zıt renkli kapanış | Ham |
| Sınıflar (BTCUSD kodu) | ayı, boğa, sinyal yok | Ham |
| Zaman dilimi | CUSAN saatlik (görselde "60"); yanıt gönderisinde "20 günlük"; AFYON grafiği günlük değil gün içi çubuklara benzer (YORUM) | Ham; görsel, açıldı |
| Hedef | orta çizgi (CUSAN, sözel) | Ham |
| Stop | yok | - |

- Belirsiz kalanlar: temas ve onay mum tanımı; kaç mum; 1,5 SD ile 3 SS iki ayrı ayar mı yoksa ayrı kurulum mu; Ham "20 günlük HO" der, görselde saatlik grafikte BOL(20,3) var (20 bar saatlik, YORUM); AFYON'un bar birimi; stop; kodların paylaşılmaması (TUPRS: "bir kaç optimizasyon yapmam lazım"; BTCUSD: dış bağlantı) ve tarama kodu (yayımlanmadı); çıkış kuralı yok; backtest sonucu (Tansu okura bırakır). Ham "zır mum" yazar, not adı "zit" der (muhtemelen yazım hatası: zıt).
- Tansu'nun kanıtı: yok; "güvendiğim strateji", "en sevdiğim" sözleri; CUSAN, AFYON, TUPRS tek örnek; TUPRS bearish rejection "hemen yakaladı", BTCUSD al sinyali 1 hafta önce (Ham); sayısal sonuç yok. Seçilmiş vakalar.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC; Bollinger ve mum rengi). Saatlik CUSAN örneği ücretsiz günlük veride yok; AFYON grafiği gün içi görünüyorsa TASARIM §3 kapsamı dışıdır (YORUM). Mum ölçütü eksik, kural bugün eksik.
- Kaynak güveni: Ham birinci el; kural net ama mum tanımı ve ayarlar parçalı (3 SS ve 1,5 SD), backtest ve kod yok: orta-düşük. Hazırlık K.

---

## 39. Bollinger orta bandı üstünde kapanış + RSI 50 yukarı kesişimi (aynı bar), OBV teyidi, ATR stop ve tarama (THYAO, ISYAT, SAYAS)

- Kaynak: `tweet-bb-orta-bant-rsi-50-ayni-bar-atr-stop-1782881410174365714` (THYAO, yanıt gönderisi, 23.04.2024; Ham ve görsel, açıldı), `tweet-bb-orta-bant-rsi-50-kesisim-obv-1782080174273466707` (ISYAT, 21.04.2024; Ham ve kısmi görsel metni), `tweet-bb-orta-bant-rsi-obv-teyit-1766496726762856541` (SAYAS, 09.03.2024; Ham ve görsel, açıldı), `tweet-bb-orta-bant-rsi50-macd-tarama-1877567811410616770` (tarama, 10.01.2025; Ham ve görsel metni), `tweet-bollinger-bantlari-rsi-50-tarama-1877371588120629278` (09.01.2025; Ham, duyuru). Hepsi Tansu'nun X gönderisidir (birinci el). THYAO grafiğinin TradingView yayın etiketi "microblogliku" der; hesabın kime ait olduğu yazılı değil (yayın saati Tansu'nun yanıtından 12 dakika önce; YORUM).
- Tansu'nun ifadesi (verbatim):
  - THYAO (Ham): "aşağıdaki gibi mavi oklara dikkat edelim. Stop loss için atr elbette kullanılabilir. İlk bar orta bandın üzerinde kapanacak. rsı'da aynı anda 50'yi geçecek"; başı: "Çok basit tutmak lazım."
  - ISYAT (Ham): "hisse alım noktasına yaklaşmış. Ama hala orta bollinger bandının üzerine atamamış fiyatı. RSI'da momentumun ivme yaptığı 50'yi kesmemiş henüz. Para girişi var." Devamı: "Pazartesi bakalım duruma, orta bandın üzerine atıp, RSI 50'yi geçerse anladın onu:)"
  - SAYAS (Ham): "Artan momentum, para girişinin hızlanması, RSI'ın artan momentuma işaret vermesi ve BB'nin orta bandı üstünde gelecek bir kapanış ile eski zirvelerine doğru hareket başlayabilir. Tam sınırdayız."
  - Tarama (Ham, 10.01.2025): "Son gün BB orta bandı yukarı kesilen, RSI>50 olan ve MACD al veren hisselerin taraması." Yanıt gönderisi: "böyle de bir çıktısı var bu mübareğin". Duyuru (09.01.2025): "Size de bir kod paylaşacağım, bollinger bands ve RSİ> 50".
- Tanım (YORUM, sözlü kurala göre):
  1. Giriş tetiği (THYAO): aynı barda iki koşul birlikte: kapanış BB orta bandının (SMA) üzerinde ve RSI 50'yi aşağıdan yukarı keser. "İlk bar", iki koşulun birlikte oluştuğu ilk bardır. Görselde mavi oklar iki girişi gösterir (Kas 2023, Oca 2024); fiyat çubuğu mavi orta çizgiyi geçerken RSI de 50 çizgisini geçer (görsel, açıldı).
  2. Bekleme durumu (ISYAT, SAYAS): koşullar henüz tamam değildir. ISYAT'ta fiyat orta bandın altında ve RSI 50'nin altındadır (Ham). SAYAS görselinde son çubuk orta bandın altındadır (eksen etiketleri: fiyat 97,45; orta bant 99,47) ve RSI 50,81'dir (50'nin hemen üstü) (görsel, açıldı; etiketlerden okundu, YORUM: son çubuğun değerleri). Tansu bir sonraki seansı izler.
  3. Teyit (sözel, eşiksiz): OBV artışı ("para girişi") ve RSI'ın momentum ivmesi. SAYAS görselinde OBV panelinde dipten dönüş oku vardır (görsel, açıldı).
  4. Stop: ATR kullanılabilir (Ham); periyot ve çarpan yazılı değil. THYAO görselinde pozisyon aracı kutuları vardır: yeşil kâr, pembe zarar; üç kutudan ikisi mavi oklu girişlerdendir (görsel, açıldı). Kutu oranları ölçülmedi.
  5. Tarama (10.01.2025): son gün BB orta bandını yukarı kesen, RSI>50 olan ve MACD al veren hisseler. Burada RSI>50 seviye koşuludur; THYAO'daki "50'yi geçecek" kesişimdir (YORUM: tarama kesişimi gevşetmiş olabilir). Tarama çıktısı dış bağlantıdadır (açılmadı). Yanıt görselinin metni (görsel metni): kapanış, üst, alt, orta bant ve RSI paneli; sayı yok. 09.01.2025 gönderisi aynı taramayı duyurur; koşul ayrıntısı yoktur.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Bollinger | (20, 2): orta bant SMA20, ±2 standart sapma | görsel, açıldı (SAYAS lejantı "BB (20, 2)") |
| RSI periyodu | 14 | görsel, açıldı (SAYAS lejantı "RSI (14)") |
| RSI eşiği | 50 | Ham |
| Aynı bar şartı | kapanış > orta bant ve RSI 50 kesişimi aynı barda | Ham ("aynı anda") |
| OBV | teyit olarak anılır; eşik yok | Ham ve görsel, açıldı |
| MACD (tarama) | "al veren"; periyot yok | Ham |
| Stop | ATR; periyot ve çarpan yok | Ham |
| Zaman dilimi | günlük | görsel, açıldı (THYAO "1G"; SAYAS "D") |
| Hedef, çıkış | yok | - |

- Belirsiz kalanlar: "ilk bar" aşağıdan ilk geçiş mi; geçişin ölçütü (kapanış); RSI yumuşatma çizgisi (görselde sarı, etiketsiz); ATR periyodu ve çarpanı; MACD parametreleri ve "al" tanımı; OBV eşiği; THYAO görselindeki siyah X'in anlamı (YORUM: koşulu karşılamayan örnek); çıkış kuralı yok; SAYAS'ta fiyat orta bandın altındayken Ham "tam sınırdayız" der.
- Tansu'nun kanıtı: THYAO grafiğinde üç kutu çizilmiş, seçilmiş vakalar; sayısal sonuç yok. ISYAT ve SAYAS bekleyen kurulumlardır. Tarama çıktısı açılmadı.
- Günlük bedava veriyle uygulanabilir mi: BB, RSI ve MACD günlük kapanıştan hesaplanır; OBV hacim, ATR yüksek ve düşük ister (projenin güncel veri durumu ayrıdır: §0).
- Kaynak güveni: Ham ve görsel birinci el; BB 20/2, RSI 14 ve RSI 50 görselden ve Ham'dan açık; stop ve tarama koşulu kısmi: orta. Hazırlık K.

---

## 40. Bollinger sıkışması + RSI 50 yukarı kesişimi (GRNYO, DOAS, ORCAY, SANEL)

- Kaynak: `tweet-bb-sikismasi-rsi-50-yukari-kesisim-1838704848310554789` (DOAS, ORCAY, SANEL; 24.09.2024; Ham, G1 ve G2 görsel metni, G3 açıldı), `tweet-bb-sikisma-rsi-50-yukari-kesme-1839057936141705262` (GRNYO; 25.09.2024; Ham ve görsel, açıldı), `tweet-bb-sikisma-rsi-50-kesisim-1839306184622485864` (26.09.2024; Ham, alıntı gönderisi). Hepsi Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim):
  - 24.09.2024 (Ham): "Dikkat edelim." "BB sıkışması var ve RSI bir kaç gün önce 50'yi yukarı kesmiş"; devamı: "Keserse BB yukarı iyi kırılabilir."
  - 25.09.2024 (Ham): "BB sıkışması ve RSI 50'nin yukarı kesilmesi benim sevdiğim bir strateji. Yarın şu hisseye bir bakalım nasıl olacak."
  - 26.09.2024 (Ham): "Şu endekste bunu ya yakaladık:)" (25.09 gönderisini alıntılar).
  - Görsel başlıkları (görsel metni; GRNYO ve SANEL açıldı): "GRNYO Bollinger Bands Sıkışması ve RSI 50 Kesilmesi" (DOAS, ORCAY ve SANEL için aynı şablon); lejant "RSI", "RSI 50"; eksen "Price / RSI". Grafik: 100 barlık fiyat çizgisi (mavi), BB üst (yeşil kesik), orta (mavi kesik), alt (kırmızı kesik), RSI (mor), "RSI 50" (gri kesik), son bar turuncu dikey çizgi (görsel, açıldı).
- Tanım (YORUM):
  1. Sıkışma: BB üst ve alt bandı arasındaki mesafe daralmış. GRNYO'da bant genişliği son bölümde yaklaşık 0,25 (9,30 − 9,05), sol bölümde yaklaşık 0,7 (görsel, açıldı; ölçüm). Eşik yok.
  2. Tetik: RSI 50'yi aşağıdan yukarı keser. GRNYO'da son bar RSI ≈ 52,7 ve bir önceki bar ≈ 44 (görsel, açıldı; ölçüm): kesişim son barda. SANEL'de son bar RSI ≈ 47: kesişim yok, bekleme (görsel, açıldı; ölçüm).
  3. 24.09 durumu: RSI birkaç gün önce 50'yi kesmiş ve geri dönmüştür; tetik yeniden kesişimdir ("Keserse").
  4. Beklenen sonuç: BB'nin yukarı kırılması ("iyi kırılabilir"). Bu bir çıkış veya hedef kuralı değildir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| RSI eşiği | 50 (yukarı kesişim) | Ham |
| RSI periyodu | 14 (RSI çizgisi 14. barda başlar) | görsel, açıldı (ölçüm; YORUM) |
| BB periyodu | 20 (bant çizgileri 20. barda başlar) | görsel, açıldı (ölçüm; YORUM) |
| Pencere | 100 bar | görsel, açıldı |
| Sıkışma ölçütü, çıkış, stop, hedef | yok | - |

- Belirsiz kalanlar: sıkışma ölçütü (bant genişliği yüzdesi, geçmişe göre sıra, KC içinde olma); "bir kaç gün önce" penceresi; bar birimi (günlük varsayımı, YORUM); stop ve hedef; 26.09 gönderisinde "endekste" sözü ve hangi sembol olduğu; hangi hisse veya endeks olduğu ve sonuç sayısı yazılı değil.
- Tansu'nun kanıtı: "yakaladık" cümlesi (sayı yok); dört sembolde grafik, sonuç yok. Seçilmiş vakalar.
- Günlük bedava veriyle uygulanabilir mi: evet (kapanıştan BB ve RSI hesaplanır). Sıkışma ölçütü olmadan kural eksik.
- Kaynak güveni: Ham birinci el; sayısal ayar yalnız RSI 50; sıkışma tanımı yok: düşük. Hazırlık K.

---

## 41. BELTHOLD boğa mumu + RSI düşen trend çizgisi kırılımı: stop mum altı, hedef 2-3 gün (CONSE, ISFIN; TA-Lib)

- Kaynak: `tweet-belthold-rsi-trend-kirilim-stop-1911135810839105880` (CONSE; 12.04.2025 19:14 UTC; Ham ve görsel metni), `tweet-belthold-rsi-kirilim-ta-lib-1911146678016504174` (ISFIN; 12.04.2025 19:57 UTC; Ham ve görsel metni). İkisi de Tansu'nun X gönderisidir (birinci el). İkinci gönderinin metni emoji başlıklı, yapay zekâ özeti gibi okunur (YORUM); Ham olarak birinci el sayılır.
- Tansu'nun ifadesi (verbatim):
  - CONSE (Ham): "8 Nisan kapanışı itibari ile #python taramamızda takılan ve 2 günde %5 marj veren fiyat grafiğindeki formasyonu anlatalım". Tanım: "Belthold, tek mumdan oluşan bir boğa dönüş formasyonudur." Özellikler: "Öncesinde Düşüş trendi ya da düzeltme hareketi olması gerekir." "Açılış Günün en düşük seviyesine çok yakındır (veya tam orasıdır)." "Kapanış Günün en yüksek seviyesine çok yakındır (veya tam orasıdır)." Strateji: "RSI trend kırılımı varsa ve o gün BELTHOLD yakalanmışsa, bu çok güçlü bir teknik sinyal olur." "Stop-loss: o mumun altı. Hedef: 2-3 gün içi momentum takibi veya önceki dirençler." "SONUÇ: 2 GÜNDE %5" ve "Testere piyasasında fena getiri değil".
  - ISFIN (Ham): "RSI son gün bu düşen trendi yukarı kırıyor." "Grafikte \"BELTHOLD\" yazısıyla işaretlenen yeşil mumun olduğu gün, TA-Lib bu formasyonu tespit etmiş." "İki mavi nokta RSI tepelerini işaret ediyor ve bu iki tepe arasında düşen bir trend çizgisi (kırmızı kesikli çizgi) oluşturulmuş." "SONUÇ: BİR KAÇ GÜN İÇİNDE %5 GETİRİ".
  - Görsel metni: "CONSE.IS son gün RSI trend doğrusunu yukarı kesti." ve "tespit edilen formasyonlar: BELTHOLD" (ISFIN için aynı şablon).
- Tanım (Ham ve YORUM):
  1. BELTHOLD (boğa): tek günlük, yeşil mum; açılış günün en düşüğüne çok yakın; kapanış günün en yükseğine çok yakın; öncesinde düşüş veya düzeltme; uzun gövde, alt gölge yok veya çok kısa (Ham). Yakınlık ölçüsü yazılı değil. Dedektör TA-Lib'dir (Ham); TA-Lib'in iç eşikleri Tansu'nun kuralı değildir (YORUM).
  2. RSI düşen trend çizgisi kırılımı: RSI'ın iki tepesini birleştiren düşen çizgi son gün yukarı kesilir (Ham; görsel metni). Tepe seçimi ve kesişim ölçütü yazılı değil.
  3. Sinyal: 2 ve 1 aynı gün (Ham: "o gün").
  4. Stop: BELTHOLD mumunun altı (Ham; YORUM: mumun düşüğü). Hedef: 2-3 gün içi momentum takibi veya önceki dirençler (Ham); sayısal hedef yok.
  5. Tarama: "#python taramamız" sinyal günü kapanışında çalışır (Ham, 8 Nisan kapanışı).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Formasyon | BELTHOLD (boğa), 1 mum, TA-Lib | Ham |
| RSI trend çizgisi | iki RSI tepesi arasında düşen çizgi; yukarı kesiş | Ham ve görsel metni |
| Aynı gün şartı | RSI kırılımı ve BELTHOLD aynı gün | Ham |
| Stop | BELTHOLD mumunun altı | Ham |
| Hedef | 2-3 gün içi momentum takibi veya önceki dirençler | Ham |
| Tutma süresi | 2-3 gün | Ham |
| RSI periyodu | yok (YORUM: 14) | - |

- Belirsiz kalanlar: giriş fiyatı (sinyal günü kapanışı mı, ertesi açılış mı); "%5" neye göre; RSI periyodu; RSI tepelerinin seçimi; "önceki direnç" nasıl bulunur; "momentum takibi" çıkış ölçütü; TA-Lib yeni bir paket olur (AGENTS.md "Dependency": TASARIM §4 önce okunur, YORUM); düşüş trendi şartının ölçüsü. §10'daki engulfing ile benzer dönüş mumu, ama aynı gün RSI filtresi bu kuralda yeni. §43'teki düşen trendde boğa mumu uyarısıyla gerilim vardır: Belthold düşüşten sonra aranır (YORUM: çerçeveler farklı olabilir; Tansu açıklamaz). Aynı mum dedektörü A §18'de 60 günlük aralık kırılımıyla birleşir.
- Tansu'nun kanıtı: CONSE "2 GÜNDE %5", ISFIN "BİR KAÇ GÜN İÇİNDE %5" (Ham); iki seçilmiş vaka, giriş fiyatı yok, kazanma oranı yok.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC). RSI trend çizgisi için tepe kuralı gerekir; şimdi tam uygulanamaz.
- Kaynak güveni: Ham ve görsel birinci el; stop ve hedef sözlü; dedektör eşiği ve trend çizgisi kuralı yok: orta-düşük. Hazırlık K.

---

## 42. RSI(14) 30/70 son gün taraması (BIST 30 kodu)

- Kaynak: `tweet-bist30-rsi-14-30-70-tarama-1860401887675126207` (23.11.2024; Ham ve kod görseli, açıldı). Tansu'nun X gönderisidir (birinci el). Yaklaşık 16 dakika sonra gelen `tweet-rsi-esik-periyot-optimizasyonu-1860405835354054736` (E K29; süre id farkından, hesap bizim) "RSI 30/70 Allah kelamı değil" der.
- Tansu'nun ifadesi (verbatim): "Buyurun size RSI taraması, çok istediniz." "Tabi buna güvenerek işleme girmeyin keşke borsada hayat bu kadar basit olsa." (Ham). Kod (görsel, açıldı): `rsi_upper = 70`; `rsi_lower = 30`; `periods = 14`; `df["RSI"] = df.MA_U / (df.MA_U + df.MA_D) * 100`; `if last_rsi < rsi_lower: buy_signals.append((ticker, last_rsi))`; `elif last_rsi > rsi_upper: sell_signals.append((ticker, last_rsi))`. Çıktı başlıkları: `=== AL SİNYALLERİ (RSI < 30) ===`, `=== SAT SİNYALLERİ (RSI > 70) ===`.
- Tanım (kod, görsel, açıldı): her sembol için `yf.download` (2020-01-01 – 2024-11-23), fiyat = `Adj Close`. `U = max(Δfiyat, 0)`, `D = max(−Δfiyat, 0)`. `MA_U` ve `MA_D` bu serilerin 14 günlük basit hareketli ortalamasıdır (`rolling(14).mean()`). `RSI = MA_U / (MA_U + MA_D) × 100`. Yalnız son günün RSI değeri okunur: RSI < 30 ise al adayı, RSI > 70 ise sat adayı. Bu, Wilder yumuşatmalı RSI değil, basit ortalamalı biçimdir (YORUM: ad ve fark bizim). Kod yorumu "BIST 30 hisseleri" der; listede 26 sembol vardır (sayım bizim).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| RSI periyodu | 14 | görsel, açıldı |
| Alt eşik (al) | 30 (RSI < 30) | görsel, açıldı |
| Üst eşik (sat) | 70 (RSI > 70) | görsel, açıldı |
| Ortalama türü | basit (rolling mean) | görsel, açıldı |
| Fiyat | Adj Close, günlük | görsel, açıldı |
| Okunan bar | yalnız son gün | görsel, açıldı |
| Giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: "sat sinyali" BIST'te açığa satış mı yoksa çıkış adayı mı (Tansu söylemez); RSI < 30 anında mı yoksa dönüşte mi girilir (E K5'teki RSI 30 girişi maddesi dönüşü ister; bu tarama düzey koşuludur); eşik ve periyodun hisse bazlı optimizasyonu: karar Levent'te bekliyor (E K29).
- Tansu'nun kanıtı: yok; sonuç yok, Tansu "buna güvenerek işleme girmeyin" der.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük kapanış, RSI). Kural olarak yalnız tarama koşuludur.
- Kaynak güveni: Ham ve kod birinci el; tarama koşulu tam (kodda); giriş ve çıkış kuralı yok: orta. Hazırlık H.

---

## 43. Mum sinyallerinde trend filtresi: düşen trendde boğa mumuna girme (BIST100)

- Kaynak: `tweet-boga-mum-sinyali-trend-filtresi-1842843501827969532` (06.10.2024; Ham ve görsel, açıldı). Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim): "Bir de küçük uyarı yapalım. Yuvarlak ile aldığım alanda günlük boğa mum sinyalleri var ancak trend çizgisi görüyorsunuz aşağıya (yeşil). Sadece mum sinyallerine bakarak işlem açmayın mutlaka trend tayin yapın!" "Yutan boğa sinyallerini bile çarpmış adamlar." (Ham). Görsel (açıldı): başlık "BİST100"; mum grafiği (Mart–Ekim 2024) ve mumların altında küçük mavi aşağı oklar (sinyal işaretleri); sağ eksen "Trend" (−1 … +1) ve mor basamak çizgisi; yeşil noktalı eğri; siyah elips ve iki siyah ok.
- Tanım (YORUM, görselden): (1) mum sinyali = günlük boğa mumu (örnek: yutan boğa). (2) Trend tayini: mor basamak çizgisi +1 iken yukarı, −1 iken aşağı trend gösterir. Elips Ağustos sonu – Eylül 2024 arasını kapsar; orada mor çizgi −1'dedir ve yeşil eğri düşmektedir; mavi oklar bu bölgede yine de çıkar (görsel, açıldı). (3) Tansu'nun filtresi: trend aşağıyken boğa mumu sinyaline işlem açma. Trend göstergesinin formülü yazılı değil; mor çizgi yeşil eğrinin eğim işaretine benziyor (YORUM).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Trend değeri | −1 (aşağı) / +1 (yukarı) | görsel, açıldı |
| Mum sinyali | günlük boğa mumu (yutan boğa örneği) | Ham |
| Trend periyodu veya formülü | yok | - |
| Giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: trend göstergesinin tanımı (yeşil eğri hangi ortalama); trend yönü bir kapı mı (düşen trendde sinyal yok) yoksa yalnız uyarı mı; Belthold gibi dönüş mumları düşüşten sonra aranır (§41); iki ifade arasındaki gerilim Tansu'nca açıklanmaz (YORUM: trend filtresi üst zaman çerçevesi olabilir).
- Tansu'nun kanıtı: BIST100'de bir bölge, sonuç sayısı yok. Seçilmiş örnek.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC); trend göstergesi tanımsız olduğu için filtre bugün kodlanamaz.
- Kaynak güveni: Ham ve görsel birinci el; kural sözlü, ölçüt yok: orta-düşük. Hazırlık X.

---

## 44. Bollinger Keltner dışında + alt banttan sekme + zıt mum + ADX yükselişi + RSI 50 (strateji fikri; AKFGY çoklu gösterge çıktısı)

- Kaynak: `tweet-bollinger-keltner-disi-adx-rsi50-1783228274077839740` (24.04.2024; Ham), `tweet-bollinger-keltner-rsi-adx-momentum-1955389232639512999` (AKFGY; 12.08.2025; Ham ve görsel, açıldı). İkisi de Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim):
  - 24.04.2024 (Ham): "Aklımdaki strateji şu" "Bollinger Bantları, Keltner Kanalları'nın dışında olacak. Fiyat, alt Bollinger bandına dokunduktan sonra sekmiş olacak. İkinci mum zıt renkte.ADX yükselecek ve RSI 50'yi kesecek." "Biraz çalışıp netleştiririm."
  - 12.08.2025 (Ham): "Şöyle bir şeyler yapmıştım bir ara" "Kısa vade hızlı momentum" "Hisse eski tarihlidir sakın referans almayın" "Model olsun diye veriyorum size." Görsel (açıldı): başlık "AKFGY.IS Teknik Göstergeler (Bollinger, Keltner, RSI, MACD, ADX)"; paneller: fiyat + Bollinger Üst/Alt + Keltner Üst/Alt, yeşil üçgen "Son Gün AL Sinyal"; RSI (kesik çizgiler 70 ve 30); MACD, Signal, Histogram; ADX, +DI, −DI, ADXR (kesik çizgi 25).
- Tanım (YORUM; 2024 gönderisi bir fikirdir, "netleştiririm" der):
  1. Bollinger bantları Keltner kanalının dışındadır (BB üst > KC üst ve BB alt < KC alt): volatilite yüksek, sıkışma yok. Bu, §45'teki sıkışma kuralının tersi durumdur.
  2. Fiyat alt BB'ye dokunur ve sekmiştir (fitil veya kapanış ölçütü yok).
  3. "İkinci mum zıt renkte": dokunma mumundan sonraki mum zıt renktir (YORUM: kırmızıdan sonra yeşil).
  4. ADX yükselir (eşik, periyot yok).
  5. RSI 50'yi yukarı keser.
  AKFGY çıktısı: gösterge seti aynı (BB, Keltner, RSI, MACD, ADX); son barda fiyat üst Bollinger çizgisine yakın, RSI 70 çizgisinin üstünde (≈80), ADX 25 çizgisinin üstünde (≈27) (görsel, açıldı; ölçüm). Yani çıktı alt banttan sekme değil, momentum durumunu gösterir; iki gönderinin aynı kural olduğu kanıtlanmaz (YORUM). "Son Gün AL Sinyal" koşulu yazılı değil.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| RSI eşiği | 50 (yukarı kesişim) | Ham |
| RSI aşırı alım / satım çizgileri | 70 / 30 | görsel, açıldı |
| ADX çizgisi | 25 | görsel, açıldı |
| ADX koşulu | "yükselecek"; eşik yok | Ham |
| BB, Keltner, MACD, ADX periyotları | yok | - |
| Giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: Keltner tanımı (orta çizgi, ATR çarpanı); dokunma ve sekme ölçütü; "İkinci mum zıt renkte" hangi mumdan sonra; ADX'in kaç barda yükselmesi; 2025 çıktısının koşulları; "kısa vade hızlı momentum" ile 2024 fikrinin ilişkisi.
- Tansu'nun kanıtı: yok; 2025 gönderisi "referans almayın" der.
- Günlük bedava veriyle uygulanabilir mi: göstergeler günlük OHLC'den hesaplanır; koşullar eksik, kural şimdi uygulanamaz.
- Kaynak güveni: Ham ve görsel birinci el; kural yarım ve Tansu'nun kendi uyarısıyla referans dışı: düşük. Hazırlık X.

---

## 45. Bollinger Keltner sıkışması: BB'nin KC içine girmesi, KC dışına kırılım, stop ve teyit

- Kaynak: `tweet-bollinger-keltner-sikisma-kirilim-1912246536811008424` (15.04.2025; Ham). Tansu'nun X gönderisidir (birinci el). Metin yapay zekâ özeti gibi okunur (YORUM); Ham olarak birinci el sayılır. Görsel yok.
- Tansu'nun ifadesi (verbatim): "Size bir strateji daha vereyim" "Stratejinin mantığı şudur: Önce Bollinger Bands'in daraldığını ve Keltner Channel'ın içine girdiğini görürüz." "İkinci adımda, fiyatın Keltner Channel'ın dışına çıktığını görürsek bu bir kırılım sinyalidir. Fiyat ya yukarı yönlü kanalın dışına çıkar (bu durumda al sinyali), ya da aşağı yönlü dışına çıkar (bu durumda sat sinyali)." "Bu strateji, \"sıkışma → kırılım → yön\" sıralamasına dayanır." "İşlem yapılacaksa, stop-loss için Keltner'ın orta çizgisi veya BB'nin karşı bandı kullanılabilir. Ek teyit olarak RSI ya da hacim artışı da dikkate alınabilir." "#python kodu da yolda..."
- Tanım (Ham ve YORUM):
  1. Sıkışma: BB daralır ve KC'nin içine girer (YORUM: BB üst < KC üst ve BB alt > KC alt).
  2. Kırılım: fiyat KC'nin dışına çıkar; yukarı = al, aşağı = sat (Ham). Çıkışın kapanışla mı fitille mi sayıldığı yazılı değil.
  3. Sıra: sıkışma, kırılım, yön (Ham).
  4. Stop: KC orta çizgisi veya BB'nin karşı bandı (Ham). Hedef yok.
  5. Ek teyit: RSI veya hacim artışı (Ham), eşik yok.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Sıkışma | BB, KC'nin içinde | Ham |
| Kırılım | fiyat KC dışında | Ham |
| Stop | KC orta çizgisi veya BB karşı bandı | Ham |
| Teyit | RSI veya hacim artışı; eşik yok | Ham |
| BB ve KC periyot ve çarpanları | yok | - |
| Hedef | yok | - |

- Belirsiz kalanlar: BB ve KC ayarları; "al" ve "sat" BIST'te açığa satış mı; sıkışmanın kaç bar sürmesi; kırılımın aynı bar mı yoksa sıkışma bittikten sonra mı sayıldığı; kod paylaşılmadı. §1'deki EMA sıkışma ve §7'deki rehavet rejimi ile aynı sıkışma sonrası kırılım fikri (YORUM).
- Tansu'nun kanıtı: yok (örnek ve sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: BB, KC ve RSI günlük OHLC'den hesaplanır; ayarlar eksik olduğundan kural şimdi uygulanamaz (ayar seçimi bizim YORUM'umuz olurdu).
- Kaynak güveni: Ham birinci el; sayı yok: düşük. Hazırlık K.
