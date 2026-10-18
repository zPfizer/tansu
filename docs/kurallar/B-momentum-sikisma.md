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
- Modül 1'de kullanımı: KURALLAR §3 (sıkışma dönemi, EMA setleri, giriş penceresi; EMA setleri varyantlardır).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ema-sikisma-tarama-1996662869107134897` — Aynı sıkışma dedektörü farklı EMA setiyle (PAPIL): başlık "EMA Sıkışma Analizi (Sıkışma: %0.03)", "En Sıkışık An (%0.03)" işareti (görsel, açıldı). Tansu: "sıkışmayı yakalayın bakın keyfinize." (Ham). Tolerans, süre ve pencere görselde yok. Parametre: EMA seti (PAPIL örneği) = 10/20/50; en sıkışık an oranı = %0,03 (görsel, açıldı)

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
- Modül 1'de kullanımı: KURALLAR §3 (momentum squeeze süzgeci; Pre Signal ayrıca kodlanmaz).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ema-sikisma-momentum-conflict-2045457969215631398` — BULL/BEAR/CONFLICT sayacının mantığı (YORUM: aynı araç): "EMA sıkışması bull sinyal aldınız ama momentum squeeze neg ve negatif büyüyor" "O zaman burada conflict sinyal vardır, bull yönde aksiyon alınmaz" (Ham, 18.04.2026; iki satır). Momentum squeeze negatif ve büyüyorsa EMA sıkışma alımı yok; araç adı ve formül yok. Parametre: CONFLICT = EMA sıkışması bull yönlü iken momentum squeeze negatif ve büyüyor; bu durumda bull aksiyon yok (Ham; ICBCT sayacıyla eşleşme YORUM; momentum squeeze göstergesi ve eşiği yok)

## 3. Demand bölgesinde EMA5/8/13 sıkışması

- Kaynak: `gorsel-paket-106-demand-ema-squeeze-supply-outcome.md`; `assets/gorsel-paket-106-demand-ema-squeeze-supply-outcome/01-demand-ema-squeeze-breakout-supply-outcome.png`.
- Tansu'nun ifadesi: görselde HİÇ yazı yok (513x347). Yalnız yeşil/kırmızı kutular, üç renkli çizgi, kırmızı ok. Ham metni (Ham'da yazar yok; R198) şunu anlatır: demand bölgesi içinde EMA'lar birbirine yaklaşıp yataylaşır ("Ben 5-8-13 kullandım"); gerilen yay; agresif giriş talep bölgesinin alt sınırı/alt fitil; güvenli giriş ilk güçlü uzun yeşil breakout mumunun kapanışı veya retest; stop talep bölgesinin hemen altı (kutu altı kapanış analizi iptal eder); ilk hedef üstteki supply (arz) bölgesi.
- Tanım (Ham): (1) demand bölgesi var. (2) EMA5, EMA8, EMA13 birbirine yaklaşıp yatay. (3) giriş: bölge alt sınırı (agresif) veya ilk uzun bullish kırılım mumu / retest (güvenli). (4) stop: demand altında kapanış. (5) hedef: üst supply bölgesi.
- Parametreler: EMA 5/8/13 (Ham; görselde lejant yok). Bölge sınırları, "yaklaşma" ölçüsü, "uzun mum" ölçüsü YOK.
- Kanıt: tek seçilmiş örnek; sembol/periyot yok; sağ uçta ikinci sıkışma (karar bekliyor).
- Uygulanabilir mi: KISMEN. EMA kısmı kolay; demand bölgesi tanımı ayrı kural ailesi (A grubu). Eşikler Tansu'dan gelmiyor.
- Güven: Ham (kural metni birinci el); görsel etiketsiz.
- Modül 1'de kullanımı: KURALLAR §3 (kutu, giriş türleri, kutu stopu, arz bölgesi hedefi).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ema-sikismasi-talep-bolgesi-kirilim-2002087132089770127` — Aynı metin (gp-106), Tansu'nun kendi X gönderisi olarak (19.12.2025; görsel metni yok; bölümdeki yazarsız Ham notu bu gönderi için geçerli değil). Güvenli giriş: "Alım sinyali, bu mumun kapanışıdır veya bu mumun ardından gelen küçük geri çekilmedir (Retest)." (Ham). Agresif giriş: "EMA'lar hala sıkışıkken, fiyat talep bölgesinin alt sınırına değdiğinde alım yapmak." (Ham). Stop: "Stop noktası, EMA sıkışmasının olduğu Talep Bölgesinin (Yeşil Kutu) hemen altı olmalıdır." (Ham). Hedef: "İlk hedef, grafiğin sağ üstünde gördüğün Kırmızı Bölge (Supply/Arz) alanıdır." (Ham). Parametre: EMA seti = 5-8-13 ("Ben 5-8-13 kullandım." Ham; Ham'da ayrıca "örneğin EMA 20, 50, 100" geçer); bölge sınırı, "güçlü" ve "gövdesi uzun" ölçüsü ve sayısal stop tamponu yok (Ham)

## 4. EMA5/8/13 dizilimi + yükselen destek tepkisi / retest (AKSGY, gp-117, gp-103, gp-64)

- Sahipleri: A §12 (gp-117 ve gp-103: lejant, başlık, temas sayısı, parametreler, Tansu'nun yorumu) ve A §4 (gp-64: düşen trend kırılımı + talep + hacim + EMA5/8/13). Burada tekrar edilmez. (bilet 04, 14.10)
- Momentum yönünden okuma: EMA5/8/13 dizilimi tarayıcı etiketidir, giriş kuralı değildir; MACD için periyot, eşik ve sinyal koşulu yoktur; ADX periyodu ve eşiği A §12'dedir.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-trend-destegi-ema-dizilim-taramasi-2000627515707035940` — Okuma (YORUM): Trend desteği örneğinde EMA dizilimi henüz istenen durumda değildir. Ham: “ema sıralamsaı istediğim gibi değil ama yarın sanırım o da hizaya gelecektir.” Okuma (YORUM): Ertesi güne ilişkin beklenti, gerçekleşmiş koşul değildir.

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
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-talib-mum-formasyonu-taramasi-1908276450450432440` — Okuma (YORUM): Son gün Dragonfly Doji sonrası izleme örneği. Alıntılanan kendi gönderisi: “Bu kardeşimiz dragonfly doji bırakmış son gün, pazartesi bakacağız:)”.

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
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-gizli-rsi-uyumsuzlugu-1900483420456653124` — Okuma (YORUM): RSI uyumsuzluğu aracının geliştirme örneği. Ham: "Hidden pozitive RSI divergence" ve "Bu kod üzerinde çalılşmaya devam etmem lazım".
  - `tweet-gizli-rsi-uyumsuzlugu-1905323172402000307` — Okuma (YORUM): Negatif uyumsuzluğun trend devamı örneği olarak paylaşımı. Ham: "Hidden bearish ne güzel çalışmış, sonra yoluna devam etmiş." Pozitif yönlü kurala dönüştürülmez.
  - `tweet-gizli-rsi-uyumsuzlugu-1905331669092950235` — Okuma (YORUM): Seçilmiş kısa işlem örneği. Ham: "Kısa bir trade yaptıksadece" ve "hidden bullish".
  - `tweet-gizli-uyumsuzluk-al-sinyali-2046689751122501699` — Okuma (YORUM): ARZUM için sonuç iddiası. Ham: "5 günde %36" ve "30 Mart tarihinde gelen uyumsuzluk sinyali". Sistematik başarı oranı değildir.

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bullish-engulfing-daily-scan-1898292620645781672` — Günlük tarama (08.03.2025): "Şu bullish engulfing taraması da çok hoşuma gidiyor." (Ham). Görsel başlığı "Son İşlem Gününde Engulf Green Sinyali" (görsel metni): tarama yalnız son işlem gününün boğa yutan mumunu arar. Koşul ayrıntısı yok (YORUM: bölümdeki 4 koşullu kod); tarama çıktısı sembolsüz, grafik Eylül 2024 - Mart 2025. Ham: kendi quant stratejisi dışında alternatif taramalar gruba verilecek.
  - `tweet-ema-5-10-engulfing-teyit-1863002809567785287` — Tansu EMA5/10 stratejisine engulfing mumunu teyit olarak ekler: "Bunlar çok jenerik stratejiler. 5-10 ema." "yanına ben engulfing ekledim." "hammer eklenebilir vs." (Ham; @JR_GPT'ye yanıt, üst gönderi notta yok). YORUM: EMA5 ve EMA10 kesişimi veya dizilimi sinyal, engulfing teyit mumu; hammer ek teyit adayı. Parametre: Engulfing'in eşlik ettiği EMA çifti = 5 ve 10 (Ham: "5-10 ema"); kesişim mi dizilim mi belirsiz
  - `tweet-ema-dizilim-engulfing-hacim-teyit-1923069231043838440` — BLCYT grafiği, KLMSN ile aynı şablon ("Engulfing + EMA34 Tepki/Kırılım", görsel metni). Ham bu başlığın boşluğunu doldurur: "EMA5 > EMA8 > EMA13 > EMA34 sıralaması"; engulfing EMA'ların hemen altında; hacim, RSI 30 üstü çıkış veya MACD kesişimi ve "İkinci gün teyidi" aranır; EMA34 direnç olabilir (Ham). Risk yönetimi (stop, pozisyon büyüklüğü) gerektiği söylenir, değer yok. Parametre: EMA dizilimi = EMA5 > EMA8 > EMA13 > EMA34 (Ham); teyit: engulfing yüksek hacimli (eşik yok), RSI 30 altından yukarı çıkış veya MACD kesişimi (Ham, örnek), engulfing sonrası ikinci gün devam mumu (Ham)
  - `tweet-ema-serit-engulfing-sinyali-1899562937414537239` — Aynı araç şablonu (EMA5/8/13/34 ve "Son Engulf Green" işareti) Tansu'nun kendi X gönderisinde: "Güzel bir engulfing:)" (Ham). Görselde (açıldı) EMA5>8>13>34 sıralı yükselen şerit, yutan boğa işaretleri; koşul, eşik ve giriş yok. Parametre: EMA seti = 5/8/13/34; yutan boğa işareti adı "Son Engulf Green" (görsel, açıldı)
  - `tweet-ema34-bullish-engulfing-1904976583313777145` — 2025-03-26: “ema34'den tepki almış yutan boğa formasyonu.” (Ham). Okuma (YORUM): ertesi gün prim beklentisi sonuç kanıtı değildir.
  - `tweet-ema34-tepki-yutan-boga-1899564640092520468` — 2025-03-11: “Ema34'deb tepki alan hisse ne mi oluyor? Bir de engulfing candle bıraksın...” (Ham). Okuma (YORUM): kaynak EMA34 tepkisi ile yutan mum birleşimini vurgular.
  - `tweet-ema34-tepki-yutan-boga-1899957802774212744` — 2025-03-12: “ema34'den tepki almış ve yutan boğa formasyonu oluşturmuş.” (Ham). Okuma (YORUM): OSTIM örneği mevcut birleşimin ek kaydıdır.
  - `tweet-ema34-tepki-yutan-boga-1904263490849612222` — 2025-03-24: “Yarın bu kardeş iyi olabilir:)” (Ham). Okuma (YORUM): açılan G2 grafiğinde son yeşil mum önceki kırmızı gövdeyi kapsar ve EMA34 çevresinden yükselir; bu seçilmiş örnektir.
  - `tweet-ema34-tepki-yutan-boga-1904446625847644380` — 2025-03-25: “Bu kardeşimiz #bieny idi günlük görevini yerine getirdi.” (Ham). Okuma (YORUM): görsel metni EMA34 tepkisi ve yutan boğa başlığı taşır; paylaşım sonuç beyanıdır.
  - `tweet-ema5-ema20-yutan-mum-1852422220515070087` — 2024-11-01: “SAYAS: Al Sinyali - EMA5 EMA20'yi yukarı kesti ve bullish engulfing formasyonu oluştu.” (görsel açıldı). Okuma (YORUM): kesişim ve mum teyidi aynı çıktıdadır.
  - `tweet-ema5-ema20-yutan-mum-1852441882980188200` — 2024-11-01: “Sadece sayas hissesinde son gün ema5 ve ema20 kesişimi var.” (Ham). Okuma (YORUM): listedeki her yutan mumun EMA kesişimi taşımadığı ayrımı korunur.
  - `tweet-engulfing-ema34-tepki-kirilim-1919495449058107733` — `tweet-engulfing-ema34-tepki-kirilim-1919495449058107733` (2025-05-05; Ham ve varsa görsel): Okuma (YORUM): IZINV örnek çıktısı, mevcut birleşimin ek görsel kaydıdır: "IZINV.IS - Engulfing + EMA34 Tepki/Kırılım" (görsel açıldı). Örnekteki işaretlerden yeni giriş eşiği türetilmedi.
  - `tweet-engulfing-ema34-tepki-kirilim-1922346153812643974` — `tweet-engulfing-ema34-tepki-kirilim-1922346153812643974` (2025-05-13; Ham ve varsa görsel): Okuma (YORUM): ENSRI örnek çıktısı, mevcut birleşimin ek görsel kaydıdır: "ENSRI.IS - Engulfing + EMA34 Tepki/Kırılım" (görsel açıldı). Örnekteki işaretlerden yeni giriş eşiği türetilmedi.
  - `tweet-engulfing-ema34-tepki-kirilim-alim-2027089789233610776` — `tweet-engulfing-ema34-tepki-kirilim-alim-2027089789233610776` (2026-02-26; Ham ve varsa görsel): Okuma (YORUM): KLMSN örnek çıktısı, mevcut birleşimin ek görsel kaydıdır: "KLMSN.IS - Engulfing + EMA34 Tepki/Kırılım" (görsel açıldı). Örnekteki işaretlerden yeni giriş eşiği türetilmedi.
  - `tweet-engulfing-ema34-tepki-kirilim-froto-1924518525739163917` — `tweet-engulfing-ema34-tepki-kirilim-froto-1924518525739163917` (2025-05-19; Ham ve varsa görsel): Okuma (YORUM): FROTO örnek çıktısı, mevcut birleşimin ek görsel kaydıdır: "FROTO.IS - Engulfing + EMA34 Tepki/Kırılım" (görsel açıldı). Örnekteki işaretlerden yeni giriş eşiği türetilmedi.
  - `tweet-engulfing-ema5-8-13-uyumu-1898296118397591733` — `tweet-engulfing-ema5-8-13-uyumu-1898296118397591733` (2025-03-08; Ham): Engulfing ve EMA dizilimi birlikte aranır: "son gün hem engulfing, hem de ema5>ema8>ema13" (Ham).
  - `tweet-engulfing-ema5-ema20-trend-donusu-1852431559275454918` — `tweet-engulfing-ema5-ema20-trend-donusu-1852431559275454918` (2024-11-01; Ham): Engulfing dönüş teyidi: "zaten ema5 ema20'yi kestiğinde trend dönüşü anlamına gelir. Trend dönüşünde böyle bir formasyon yakalamak önemlidir." (Ham).
  - `tweet-engulfing-mum-ema5-ema20-tarama-1852417222087508457` — `tweet-engulfing-mum-ema5-ema20-tarama-1852417222087508457` (2024-11-01; Ham): Ham dönem ifadesi: "Engulfing mum ve tren yönünde yakalamanız için 5-10 günlük ema'ları da ekledim." ve "Son gün sinyali değil, onu ayrıca yazacağım." Okuma (YORUM): Ham içindeki 5-10 ile Görsel metni içindeki EMA5/EMA20 ayrımı çözülemedi.
  - `tweet-engulfing-rejection-mum-sinyal-isabet-olcumu-1762402307503780152` — `tweet-engulfing-rejection-mum-sinyal-isabet-olcumu-1762402307503780152` (2024-02-27; Ham): Sinyalin veri setine bağlılığı: "Bu veri setinde geri dönüş sinyali olarak engulfing'e pek güvenmemelisin." (Ham). Ham %31 dönüş olasılığı bildirir; genel başarı oranı olarak kullanılmaz.
  - `tweet-talib-mum-formasyonu-etiketleme-1899922146769485826` — Okuma (YORUM): Engulfing gözlemine yükseliş beklentisi bağlanan tek örnek. Ham: “Şu size verdiğim engulfing hisse var ya, adını vermediğim,  onun başka versiyonu.” ve “Sonuç aynı, gidecek belli :)”. Okuma (YORUM): Beklenti, doğrulanmış sonuç değildir.

## 11. Tweezer Bottom + talep bölgesi

- Kaynak: `tweet-tweezer-bottom-talep-bolgesi-backtest.md` (görsel yok).
- Tansu'nun ifadesi (Ham, birinci tekil): "tweezer bottom mumunu yazayım taramasını da yapayım"; getirisine bakacağını söyler; "talep bölgesinde şahane fırsatlar sunuyor". Tansu sayısal kural vermedi.
- Tanım: iki ardışık mumun dipleri yakın. Not "same_low" toleransı, ATR oranı vb. önerir. Tamamı Cevo.
- Parametreler: yok (hiçbiri Tansu'dan). Giriş/stop/hedef yok.
- Kanıt: yok. Uygulanabilir mi: KISMEN (fikir; tüm sayılar YORUM). Güven: Ham (niyet beyanı; kural yok).
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-tweezer-bottom-donus-mumu-2090468406977806687` — Okuma (YORUM): Düşüş trendinde dönüş sinyali olarak Tweezer Bottom örneği. Ham: “düşüş trendlerinde oluşan ve trend değişim sinyali veren mum formasyonlarını” ve “Tweezer bottom”. G1 açıldı; kırmızı kutu iki komşu mumu işaretler. Okuma (YORUM): Görseldeki benzer dipler sayısal tolerans olarak ölçülmez.

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
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-12-ay-momentum-ilk-3-aylik-yeniden-dengeleme-1948795367874854937` — Okuma (YORUM): İlk üç hisse varyantı, on-dilim örneğinden ayrı tutulur. Ham: "Geçmiş bir yıl boyunca en fazla değer kazanan üç hisse belirlenir ve bu üç hisseye eşit ağırlıkla yatırım yapılır." Aylık yenileme: "Her ayın sonunda sistem aynı şekilde tekrar çalışıyor: En iyi üç hisse seçiliyor ve yatırımcı bir sonraki ay boyunca bu portföyü taşıyor."
  - `tweet-12-aylik-bilesik-getiri-momentum-skoru-1946925694652674087` — Okuma (YORUM): Momentum skoru, temettü dahil toplam getiriyle açıklanır. Ham: "En basit yöntem, belirli bir geriye dönük dönem (örneğin son 12 ay) boyunca hissenin toplam getirisini (temettüler dahil) hesaplamaktır." Hesap: "Daha sonra tüm bu brüt getiriler birbiriyle çarpılır ve sonuçtan 1 çıkartılarak toplam 12 aylık net getiri (momentum skoru) bulunur."
  - `tweet-kisa-vadeli-momentum-reversal-1946948449275928807` — Okuma (YORUM): Bir hafta/bir ay hızlı yükseliş için geri dönüş uyarısı, 12 aylık momentumdan ayrı vade bağlamıdır. Ham: "Kısa vadeli kazananlar genelde kısa vadeli kaybedenlere dönüşüyor." ve "Bu yüzden getirisi düşük ama temeli sağlam olan hisseleri izlemek daha mantıklı olabilir." (20.07.2025).
  - `tweet-ondalik-momentum-portfoy-siralama-1771618483693895959` — `tweet-ondalik-momentum-portfoy-siralama-1771618483693895959` (2024-03-23): Ham: "10 hisseden oluşacak 10 grup oluşturdum". Okuma (YORUM): BIST100 verileriyle oluşturulan onlu grupların 2023 momentum karşılaştırmasıdır; sonuç genellenmez.

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
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-clenow-regresyon-momentum-r2-2018743366112985154` — 03.02.2026 Ham kodu: "annualized = (1 + slope) ** 252" ve "return annualized * (rvalue ** 2)". Açıklama: "ne kadar istikrarlı/pürüzsüz yükseldiğine bakar". Okuma (YORUM): Aynı fonksiyonun arşiv kaydıdır; BIST için deneme planı gerçekleşmiş performans kanıtı sayılmaz.
  - `tweet-egim-r-kare-momentum-skoru-2018765685091139701` — ALARK çıktı örneği (03.02.2026): “Yıllıklandırılmış Eğim (Getiri Gücü): 1.5565”, “Trend Kalitesi (R-kare): 0.8749”, “HESAPLANAN MOMENTUM SKORU: 1.3617” (Ham). Okuma (YORUM): değerler örnek çıktı olarak tutulur.
  - `tweet-regresyon-r2-trend-gucu-1922760837049045499` — 14.05.2025, Ham: “R² düşükse veya fiyatlar sürekli trendin dışına sapıyorsa, bu zayıf bir sinyal olarak kabul edilir”. Okuma (YORUM): trend düzenliliği ölçüsüdür; bu not Clenow formülünü değiştirmez.

## 16. HalfTrend "buy" + momentum eşiği (çift kapı)

- Kaynak: `tweet-halftrend-buy-momentum-threshold-kapisi.md` (görsel yok).
- Tansu'nun ifadesi (Ham; Ham'da yazar yok): kod ve sonunda "Nice": `if half_trend[t] == "buy" and momentum[t] > momentum_threshold: # Nice`.
- Tanım: iki koşul AND. HalfTrend burada hazır bir gösterge (durum mu olay mı belirsiz).
- Parametreler: HalfTrend amplitude/kanal sapması YOK; momentum formülü/pencere/eşik YOK.
- Giriş: yalnız long adayı; stop/hedef yok.
- Uygulanabilir mi: KISMEN. HalfTrend (TradingView) günlük veriyle hesaplanır; momentum ve eşik YORUM. Ham'da yazar yok.
- Güven: Ham (yazar yok).
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-half-trend-buy-momentum-esik-2040719525608374694` — Okuma (YORUM): İki koşullu kapının kaynak tekrarı. Ham: `if (half_trend[t] == 'buy' and momentum[t] > momentum_threshold)`.

## 17. Momentum değerden önce döner: eğim erken uyarı

- Kaynak: `tweet-momentum-degerden-once-doner-egim-erken-uyari.md`.
- Tansu'nun ifadesi (Ham): "ortalama kullanıyor iseniz eğimlere dikkat edeceksiniz", momentum trader için "sinyal eğiminize dikkat"; "Momentum (Hız), değerden ... önce döner"; "eğimin yön değiştirmesi bir erken uyarı sinyalidir", kesişim onay; kesişimde fiyat "genellikle %5-%10 primlenmiş olur".
- Tanım: `slope = MA_t - MA_{t-K}` negatiften pozitife dönünce uyarı; kesişim teyit. Formüller Cevo.
- Parametreler: MA türü, periyot, K, eşik YOK. "%5-10" = iddia, kanıtsız.
- Uygulanabilir mi: KISMEN (fikir; sayılar YORUM). Güven: Ham.
- DMA kanal eğimi (`gorsel-paket-119-dma-kanal-egim-evre-gecis`; yalnız görsel, metin yok; bilet 04, 14.10): infografik `DMA Kanal Analizi: Trendin Gücünü Anlamak`: kanal eğimi ne kadar dikse yükseliş o kadar güçlüdür; eğim mevcut trendin gidişatını ve gücünü izler; mevcut evre sonraki evrenin tonunu etkiler (zayıf yükseliş, sert düşüş habercisi; hafif düşüş, güçlü yükseliş habercisi). Görselde kaynak imzası yok (Ham yalnız görsel; Ham'da yazar yok). "DMA" açılımı, formül, periyot, eşik, sembol yok: kural tanımsız. Uygulanabilir mi: HAYIR (DMA tanımsız; eğim fikri yukarıdaki §17 ile aynı türdendir).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-dma-kanal-egim-trend-gucu-1998887651357925859` — DMA kanal eğimi infografiği Tansu'nun kendi gönderisidir (10.12.2025, "Biliyor muydunuz?"); bölümün "Ham'da yazar yok" notu bu gönderiyle çözülür. "Eğim Ne Kadar Dikse, Yükseliş O Kadar Güçlüdür" (görsel metni). Evre etkisi: zayıf yükseliş sert düşüşün, hafif düşüş güçlü yükselişin habercisidir. DMA açılımı, formül, eşik yok.
  - `tweet-kirilim-aninda-sinyal-egimi-2044724052829311052` — Kural: Kırılım anındaki sinyal sağlığı ve eğimi değerlendirilir. Ham: "önemli olan kırılımın gerçekleştiği andaki sinyalin sağlığı ve eğimi." (16.04.2026). Okuma (YORUM): Sağlık sıfatından sayısal filtre üretilmez.
  - `tweet-momentum-faz-sinyal-tepkisi-beta-alpha-1878050003647697038` — `tweet-momentum-faz-sinyal-tepkisi-beta-alpha-1878050003647697038` (2025-01-11, Ham): Ham: “Faz 1 olan hissede, fiyat sinyale çok zayıf tepki veriyor ise kazanç zor”; “Faz, sinyal uyumluluğu, beta ve alpha kazancın kapısıdır.” Okuma (YORUM): fazın yanında fiyatın sinyale tepkisi, beta ve alpha birlikte değerlendirilir.
  - `tweet-momentum-lokal-zirve-modeli-1920446141105103040` — `tweet-momentum-lokal-zirve-modeli-1920446141105103040` (2025-05-08, Ham): "Model, geçmiş veriler üzerinde eğitilerek trend devam olasılığını tahmin etmeye odaklanmaktadır."
  - `tweet-momentum-sifir-alti-yorumu-1761054522833510499` — `tweet-momentum-sifir-alti-yorumu-1761054522833510499` (2024-02-23): Ham: "Triggrer çizgisini aşağı yerde kesmesi ile de sat sinyali oluşur." Görsel kodu: "df_thyao['Close'] - df_thyao['Close'].shift(10)" ve "rolling(window=8).mean()". Okuma (YORUM): THYAO örneğinde 10 günlük fark ve momentumun 8 günlük ortalaması kullanılır.
  - `tweet-momentum-tepe-regresyon-lojistik-trend-1923281964422894010` — `tweet-momentum-tepe-regresyon-lojistik-trend-1923281964422894010` (2025-05-16): Ham: "Pozitif eğim ve yüksek R² değerine sahip bir yapı, güçlü ve yönlü bir trendin işaretidir." Okuma (YORUM): momentum tepe tespiti, regresyon ve lojistik trend devam olasılığı katmanlarıdır. Ham örnekleri: "RSI > 70", "Günlük getiri > %2", "Hacim ortalamanın %150 üzerinde"; bunlar genel varsayılan eşikler değildir.

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
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-gunluk-kurulum-bes-kosul-risk-odul-1993341929614897406` — Okuma (YORUM): Aktif volatilite, sinyal uyumu, pozitif momentum, trend yönü ve risk/ödül birlikte anlatılır. Ham: "Her zaman ana trendin yönünde işlem açın." Örnek oran: "1 kaybetme riskine karşılık 2 veya 3 kazanma hedefi".

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
  - `tweet-cup-handle-kirilim-hedef-stop-retest-2096284655657836608` — 05.09.2026 Ham: "Yeni gelen arkadaşlar şuna baksınlar incelesinler retest önemlidir." TRCAS görseli açıldı: "Kırılım 48.60", "Hedef 56.03", "Stop 45.18", "R/R: 1:1.70", "Hacim: 1.29x". Okuma (YORUM): Bu değerler 04.09.2026 kırılım örneğine aittir; kalite veya hacim değerinden genel filtre eşiği çıkarılmaz.
  - `tweet-fincan-kulp-fibo-direnc-kirilimi-1987941886481318330` — `tweet-fincan-kulp-fibo-direnc-kirilimi-1987941886481318330` (2025-11-10): Fincan-kulp örneği: "Bu kardeş fincan kulp tamamlamış fibo dirençlerini patır patır yıkmış yola çıkmış görünüyor" (Ham). Okuma (YORUM): Ham içindeki %30-40 bu örneğin potansiyel beklentisidir.
  - `tweet-fincan-kulp-fibonacci-kirilma-hedef-1987938049582391791` — `tweet-fincan-kulp-fibonacci-kirilma-hedef-1987938049582391791` (2025-11-10): PRKAB örneğinde sonuç bildirimi: "Hedefe geldi." ve "%4,43" (Ham). Okuma (YORUM): tek örnek, genel başarı oranı değildir.
  - `tweet-fincan-kulp-kirilim-hedef-1986961469393473699` — `tweet-fincan-kulp-kirilim-hedef-1986961469393473699` (2025-11-08): NTHOL örneğinin etiketleri: "KIRILMA: 47.50", "HEDEF: 60.82" (görsel açıldı). Okuma (YORUM): bunlar örnek fiyat seviyeleridir.
  - `tweet-fincan-kulp-kirilim-hedef-stop-ornek-2095562062332043622` — `tweet-fincan-kulp-kirilim-hedef-stop-ornek-2095562062332043622` (2026-09-03): Retest örneğinin kapsamı: "Bu yapıyı arıyoyuz aklınızda olsun" ve "Grafik eski tarihlidir örnek olması için paylaşıldı" (Ham). Alıntılanan gönderi: "Retest beklemezseniz sonu felaket olabilir."
  - `tweet-fincan-kulp-kirilim-retest-bekle-2095558917841404010` — `tweet-fincan-kulp-kirilim-retest-bekle-2095558917841404010` (2026-09-03): Retest uyarısı: "Retest beklemezseniz sonu felaket olabilir." (Ham). Okuma (YORUM): AKSA örneği, kırılımı tek başına teyit saymama uyarısını destekler.
  - `tweet-fincan-kulp-kirilim-retest-kalite-2095921661098836095` — `tweet-fincan-kulp-kirilim-retest-kalite-2095921661098836095` (2026-09-04): Retest kalite teyidi: "Retest kaliteyi arttırır." (Ham). Okuma (YORUM): TRCAS örneğindeki puan genel eşik değildir.
  - `tweet-fincan-kulp-retest-setup-alark-ornek-2095610529330905560` — `tweet-fincan-kulp-retest-setup-alark-ornek-2095610529330905560` (2026-09-03): ALARK örneği: "İşte setup budur" (Ham). Görselde "ALARK — CUP & HANDLE" ve "RETESTTE" yazıları bulunur (görsel açıldı). Okuma (YORUM): bu kayıt retest durumunun örneğidir.

## 22. Weinstein dört evre (A1CAP)

- Kaynak: `gorsel-paket-56-a1cap-weinstein-dort-evre.md`; `assets/gorsel-paket-56-a1cap-dort-evre/01-a1cap-fiyat-hacim-dort-evre.jpg`.
- Tansu'nun ifadesi: görselde "Weinstein" yazmaz. Etiketler `H`, `L`, `LH`, `HL`, `LL`, `HH` (swing yapısı), kırmızı/yeşil basamaklı dinamik çizgi, uzun sarı ortalama, `Hacim` paneli turuncu hacim ortalamasıyla; eksen Temmuz 2023 - 2026. Metin (Ham): Stan Weinstein'ın "Piyasanın 4 Evresi" çerçevesi; Evre 1 Taban/Birikim, Evre 2 Yükseliş/Boğa ("X haftalık eğriyi ve hacmi arkasına alarak güçlü bir trend başlattığı aşama"), Evre 3 Tepe/Dağıtım, Evre 4 Düşüş/Ayı.
- Parametreler: hepsi YOK (uzun ortalama periyodu, swing kuralı, evre eşikleri).
- Giriş: yok. Ham yalnız evreleri tanımlar (Evre 2 giriş kuralı değildir); HH/HL yalnız görseldeki swing etiketleridir.
- Uygulanabilir mi: HAYIR/KISMEN (YORUM ile 30 haftalık MA gibi). Güven: Ham (evre tanımı); kural yok.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-dort-asamali-fiyat-dongusu-150-200-ort-1945064189082599687` — Dört evreli fiyat döngüsünün (ilgisizlik, yükseliş, tepe, düşüş) Tansu'nun kendi metni ve 2. evre geçiş göstergeleri: "Fiyat hem 150 hem 200 günlük ortalamanın üzerinde"; 150 günlük ortalama 200 günlüğün üzerinde; 200 günlük ortalama yukarı dönmüş (Ham). Giriş: yükseliş başlarken katılmak, dipten almak değil. Parametre: Evre 2 geçişi = fiyat > 150 ve 200 günlük ortalama, 150g > 200g, 200g yukarı dönük, daha yüksek dip ve tepe, yükseliş günlerinde hacim güçlü ve geri çekilmede düşük; dipten %25–30 yukarıda (çoğu zaman %80'e kadar) (Ham; ortalama türü SMA mı EMA mı belirtilmemiş). Evre 1 = fiyat 200 günlük ortalamaya yakın yatay, hacim düşük (Ham)

## 23. OBV trend onayı (gp-104)

- Kaynak: `gorsel-paket-104-obv-trend-onayi-senkronizasyon.md`; `assets/gorsel-paket-104-obv-trend-onayi-senkronizasyon/01-obv-trend-onayi-senkronizasyon.jpg`.
- Tansu'nun ifadesi: NotebookLM görseli (yapay zekâ infografiği; Tansu'nun aracı değil). Başlık `OBV Göstergesi ile Piyasayı Anlamak: Trend Onayı`; `Fiyat ve OBV Senkronizasyonu = Yüksek Güven`; `Yükseliş Senaryosu: Güçlü Alım Baskısı` (yükselen OBV + yükselen fiyat); `Düşüş Senaryosu: Güçlü Satış Baskısı`.
- Tanım: fiyat ve OBV aynı yönde ise trend onaylı. OBV = hacmin kapanış yönüyle işaretli kümülatif toplamı (standart).
- Parametreler: yok (pencere, eğim eşiği yok). Giriş/stop yok. Kanıt yok.
- Uygulanabilir mi: KISMEN (OBV günlük veriyle; "yön" tanımı YORUM). Güven: NotebookLM görseli (görsel birinci el; Ham'da metin yok); kural genel bilgi.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-obv-fiyat-uyumu-trend-onayi-2002683418195407193` — `tweet-obv-fiyat-uyumu-trend-onayi-2002683418195407193` (2025-12-21): Açılan NotebookLM görseli: "Fiyat ve OBV göstergesi aynı yönde hareket ettiğinde, bu durum mevcut trendin gücüne olan güveni artırır."
  - `tweet-obv-hacim-teyitli-breakout-1938256319116349670` — `tweet-obv-hacim-teyitli-breakout-1938256319116349670` (2025-06-26): Ham: "Ama bu kırılmanın anlamlı olabilmesi için OBV ya da hacim teyidi gerekir." Okuma (YORUM): direnç/kanal/aralık kırılımında OBV veya hacim teyidi aranır; emir derinliği ek incelemedir.
  - `tweet-pivot-destek-direnc-seviyeleri-1841557752289886657` — `tweet-pivot-destek-direnc-seviyeleri-1841557752289886657` (2024-10-02): Ham: "Sonra Roc50, ADX/ADXR sistemine OBV ekleyip geriye doğru bakacağız." Okuma (YORUM): OBV katkısını geriye dönük inceleme planıdır; sonuç kanıtı değildir.

## 24. Gerçekleşen volatilite (DOAS)

- Kaynak: `gorsel-paket-124-doas-yfinance-realized-volatilite.md`; `assets/gorsel-paket-124-doas-realized-vol/01-doas-yfinance-realized-volatilite-kodu.png`.
- Tansu'nun ifadesi: kod (görselden, ana satırlar): `hisse_kodu = "DOAS.IS"`; `data = yf.download(hisse_kodu, period="1y", progress=False)`; `data['Getiri'] = data['Close'].pct_change()`; `gunluk_volatilite = data['Getiri'].std()`; `yillik_volatilite = gunluk_volatilite * np.sqrt(252)`; `if yillik_volatilite > 0.40:` "Bu hisse çok hareketli (Volatil). Kemerleri bağla!", aksi halde "Bu hisse daha sakin görünüyor." Çıktı: `Günlük Oynaklık: %2.25`, `Yıllık Volatilite: %35.66`.
- Tanım: tam. Eşik 0.40 yıllık.
- Giriş kuralı DEĞİL; sınıflayıcı. Uygulanabilir mi: EVET. Güven: birinci el (kod+çıktı). Kanıt: tek hisse, örnek çıktı. Not: `auto_adjust` varsayılanı yfinance sürümüne göre değişir (YORUM).
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-log-getiri-yillik-volatilite-252-1980154063661502898` — AAPL yıllık volatilite örneği log getiri kullanır: "returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()" ve "volatility = returns.std() * np.sqrt(252) * 100" (Ham, 20.10.2025). Okuma (YORUM): DOAS örneğindeki basit getiriden ayrı hesap örneğidir.
  - `tweet-yillik-getiri-volatilite-255-gun-1915540627405554032` — 24.04.2025 Ham: ".mean() * 255 → Ortalama günlük getiriyi yıllıklaştırır (yaklaşık 255 işlem günü varsayımıyla)." ve ".std() * np.sqrt(255) → Günlük volatiliteyi yıllıklaştırır." Okuma (YORUM): bu örnek 255 gün varsayar; mevcut DOAS 252 gün hesabı değiştirilmez.

## 25. XU100 EMA50/100/200 sıkışması + KDE tepe kırılımı (gp-68)

- Kaynak: `gorsel-paket-68-xu100-ema-kde-breakout-extension.md`; `assets/gorsel-paket-68-xu100-ema-kde-extension/01-xu100-ema50-100-200-kde-hacim.jpg`.
- Tansu'nun ifadesi (görsel, birebir): başlık `XU100 Son 150 Mum ve KDE Tepe Fiyatları`; lejant `EMA 50 (13310.99)`, `EMA 100 (12840.90)`, `EMA 200 (12256.37)`; `Son Kapanış: 14587.90`; yatay KDE seviyeleri 14235.93, 13834.87, 13590.93, 12979.01, 12379.48, 11292.07, 10911.69, 10518.90; kırmızı kutu EMA'ların birleştiği bölge (2026 başı), altta hacim paneli (en yüksek hacim sağ uçta). Metin (Ham): EMA yakınlaşması dengedir; ~11.300 KDE tepesinin hacimli kırılması ve EMA'ların 50>100>200 dizilimine geçmesiyle hızlanma; fiyat EMA'lardan uzaklaşınca soğuma/retest ihtimali.
- Tanım: EMA50/100/200 sıkışması -> KDE tepe seviyesinin hacimli mumla kırılımı -> 50>100>200. KDE bandwidth/pencere YOK.
- Parametreler: EMA 50/100/200, pencere 150 mum (görsel). KDE parametreleri, sıkışma ölçüsü, hacim eşiği YOK.
- Kanıt: tek endeks örneği (sonuç kapanış 14587.90).
- Uygulanabilir mi: KISMEN (KDE parametreleri YORUM). Güven: görsel birinci el.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ema-50-100-200-sikisma-1953175981310591077` — Tekrar: Tansu'nun yanıtı EMA setini 50-100-200 olarak verir: "50-100-200 EMA:)" (Ham; @hakanbebek'e yanıt, üst gönderi notta yok; adı "sıkışma" der, bu yüzden YORUM: sıkışma için kullanılan set). Sıkışma ölçüsü ve eşik yok.
  - `tweet-kde-peak-price-levels-1952908597480075631` — Okuma (YORUM): İki vade için KDE gösterimi örneği (06.08.2025). Açılan G1: "XU100.IS Son 50 Mum ve KDE Tepe Fiyatları"; G2: "XU100.IS Son 100 Mum ve KDE Tepe Fiyatları". Ham ikinci görseli "Biraz daha orta vadeciler için" diye sunar. Bu pencereler genel zorunlu parametre yapılmaz.
  - `tweet-long-ema-compression-breakout-1952785848941846806` — TBORG örneği: "İşte uzun dönemli EMA sıkışma alanı patlaması böyle birşey" (Ham, 05.08.2025). Okuma (YORUM): uzun EMA sıkışması için ayrı hisse örneğidir; bölümün XU100 parametrelerini değiştirmez.

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
  - `tweet-mean-reversion-ratio-bands-1827401211731189852` — Mean-reversion için rejim uyarısı: "Yatay piyasalarda iyidir, düşen piyasalarda zarar yazar, çünkü ortalama hep maliyet altına iner." (Ham, 24.08.2024). Okuma (YORUM): KCHOL örneğindeki başarısızlık anlatılır; yatay rejim için hesaplanmış yeni kapı kurulmaz.
  - `tweet-ortalamaya-donus-15-85-kantil-1774872093701615913` — `tweet-ortalamaya-donus-15-85-kantil-1774872093701615913` (2024-04-01): Ham: "İlk grafik 15. ve 85. kantillerin geçilmesi ile"; "artık alım ve satım yerlerinin geldiğini gösteriyor." Okuma (YORUM): KCHOL iki yıllık karşılaştırmasında kantil temelli ortalamaya dönüş örneğidir; Bollinger standart sapma bantlarıyla aynı yöntem sayılmaz.

## 28. Medyan temelli göstergeler / aritmetik ortalama tehlikesi

- Kaynak: `tweet-medyan-temelli-finansal-indikatorler.md`, `tweet-aritmetik-ortalama-outlier-rejim-tehlikesi.md` (görsel yok).
- Tansu'nun ifadesi: kısa alıntı (Ham; Ham'da yazar yok, yazar notun Kaynak bölümünde @The_Tansu_, ikinci el): `Ortalamaları temel alan indikatörler... Medyan temelli çalışın.` Örnek (Ham): 19 gün "100 lira civarında", 20. gün 50 lira. Hesap bizimdir (YORUM): SMA20 = (19*100 + 50)/20 = 97.5, medyan 100.
- Tanım/parametre/giriş: YOK (yöntem yönlendirmesi). Uygulanabilir mi: KISMEN (hareketli medyan hesaplanır; sinyal kuralı YOK). Güven: iki tweet Ham (birinci el); hesap YORUM.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-ortalama-yerine-medyan-kullanimi-2048102880641482828` — `tweet-ortalama-yerine-medyan-kullanimi-2048102880641482828` (2026-04-25): Ham: "medyan üzerine kafa yormanızı tavsiye ederim". Okuma (YORUM): uç değer etkisine karşı ortalama yerine medyan önerisidir.

## 29. BIST100 + VIX uzun pozisyon kontrol listesi ve "Piyasanın Nabzı" (gp-113, gp-114, gp-98)

- Sahibi: D, "BIST VIX long: 5 adım kontrol listesi" ve "Piyasanın Nabzı" bölümleri (gp-113, gp-114, gp-98 görsel okumaları, parametreler, belirsizlikler). Burada tekrar edilmez. (bilet 04, 14.10)
- Momentum yönünden okuma: listedeki SMA, Heikin Ashi ve VIX RSI koşulları uygulanamaz; projenin XU100 kaynağı yalnız kapanış verir.

## 30. Hareketli ortalama üstü/altı yön filtresi ve Williams %R + SMA14 (atıf belirsiz)

- Kaynak: `tweet-hareketli-ortalama-ust-alt-trend-yon-filtresi.md`, `tweet-williams-r-sma-swing-strateji-backtest.md` (görsel yok).
- MA filtresi (Ham): "piyasa hareketli ortalamanın altındaysa satış, üzerindeyse alış; Trend is your friend." Periyot, tip YOK.
- Williams %R (Ham; Ham'da yazar yok; not `source_type: user-provided-strategy-spec`): 30 dk, W%R(14), SMA14; uzun: close > SMA14, W%R önce >= -20, -50'ye çekilmiş, -50 üstüne dönüş, bullish mum, sinyal mumu high'ı aşınca giriş, stop en yakın swing low, hedef >= 2R; kısa simetrik (-80). Gün içi veri gerekir. Ayrıntılı backtest sayıları Cevo/Claude çıktısı, Tansu'nun değil.
- Uygulanabilir mi: MA filtresi EVET (parametre YORUM); Williams kuralı HAYIR (30 dk veri; Ham'da yazar yok).
- Güven: Ham.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-ema-200-ustu-trend-filtresi-1766672851610763653` — SASA örneğinde (10.03.2024) fiyat 200 günlük EMA'nın altındaysa trend pozitif sayılmaz ve işlem açılmaz: "200 EMA üzerine atmadan işlem doğru olmaz." (Ham). Görselde EMA 20, 50 ve 200 çizili; kapanış 40,78, EMA200 43,69 (görsel metni). YORUM: filtre kapanışın EMA200 üstünde olmasıdır; kapanış mı gün içi mi belirsiz. Parametre: MA filtresi periyodu ve tipi = EMA, 200 gün (Ham: "200 günlük EMA altında trend")
  - `tweet-ema20-ayrisma-duzeltme-1778350080161976335` — THYAO düzeltme olasılığı (11.04.2024): “Göreceğiniz üzere 20 günlük EMA'dan da epey bir ayrışmış” ve “Orada da durmazsa 20 günlük EMA'sına dokunmak isteyecektir.” (Ham). Okuma (YORUM): örneğe özgü beklentidir; ayrışma için sayısal satış eşiği tanımlamaz.
  - `tweet-ema20-bb-destek-rsi-50-hedefler-1769794168140787951` — TTRAK destek örneği (18.03.2024): “881 ve 878 sırası ile EMA20 ve BB destekleri.” ve “Bu destekleri kırarsa 856'ya kadar geri çekilecektir.” (Ham). Okuma (YORUM): seviyeler örneğe aittir; aynı not para girişi ve hacimle çanak teyidini tartışır.
  - `tweet-ema20-destek-kanal-ust-fibo-hedef-1773002392381849789` — TTRAK destek ve hedef takibi (27.03.2024): “20 günlük EMA çok iyi çalışıyor hissede.” ve “Artık hedefi üst kanal direnci olan 972, aynı zamanda burası fibo direnci.” (Ham). Okuma (YORUM): kanal/Fibo hedefi seçilmiş örneğe aittir.
  - `tweet-ema20-ema50-ustu-2-gun-kapanis-1771668829900357977` — SAYAS teyit beklentisi (23.03.2024): “20EMA, 50EMA'nın üzerine çıkınca ve onun üstünde 2 gün kapanış yaptığında yine coşku verirsin bize.” (Ham). Okuma (YORUM): hangi ortalamanın üstünde kapanış kastedildiği açık seçik ayrılmadığından otomatik kural yapılmaz.
  - `tweet-ema200-alti-uzak-dur-fibo-destek-1772902932653973706` — EMA200 altı filtre (SAYAS, 27.03.2024): “200EMA altında kapatmıştı tradeler için uzak durulması gereken bölge.” (Ham).
  - `tweet-ema200-destek-direnc-okuma-1842203365884805605` — EMA200/Fibonacci birleşimi (04.10.2024): “Fibonacci seviyeleri ile 200 EMA'nın aynı noktada kesişmesi” ve “Son 6 aylık veriler üzerinden fibo çizdirilmiştir.” (Ham). Okuma (YORUM): kaynak bu birleşimi güçlü tepki olasılığıyla ilişkilendirir.
  - `tweet-ema200-dokunus-donus-alim-yeri-1775072417385259073` — SAYAS EMA200 dönüş örneği (02.04.2024): “200 EMA yı takip edip yapabiliyorsanız buradan maliyetleneceksiniz.Tam oradan önmüş mis gibi alım yeri” (Ham). Okuma (YORUM): yazım kaynaktaki gibidir; tek destek tepkisi örneğidir.
  - `tweet-ema5-ustu-trend-takip-rsi-uyumsuzluk-1984938290949058580` — 2025-11-02: “sma/ema 5 üzerinde kapandığı sürece trend takip et.” ve “RSI'ı sürekli kontrol et, uyumsuzluklar aklının bir köşesinde olsun.” (Ham). Okuma (YORUM): kaynak SMA/EMA seçimini açık bırakır.
  - `tweet-ma20-ustu-al-sinyali-python-1923090364673450197` — Başlangıç eğitimi örneği: "if data["Close"].iloc[-1] > data["Ortalama20"].iloc[-1]:" (Ham, 15.05.2025). Okuma (YORUM): son kapanışın 20 günlük ortalamadan büyük olması kontrol edilir; kod önceki günle kesişim sınamaz.
  - `tweet-williams-r-14-al-sat-sinyal-tarama-1844827048088424739` — `tweet-williams-r-14-al-sat-sinyal-tarama-1844827048088424739` (2024-10-11). Williams örneğinin görsel etiketleri: "WR (14)", "BUY (OVERSOLD)" ve "SELL (OVERBOUGHT)" (G1, açıldı). Geliştirme planı: "EMA, T3 , MACD ilave edeceğiz ve aynı zamanda saatlik bakacağız." (Ham).
  - `tweet-williams-r-asiri-alim-satim-1844478606564806669` — `tweet-williams-r-asiri-alim-satim-1844478606564806669` (2024-10-10). Görseldeki yaklaşım: "WR (14)", "BUY (OVERSOLD)" ve "SELL (OVERBOUGHT" (G1, açıldı). Okuma (YORUM): sinyal çizimleri bir örnektir; tarihli strateji çıktısı olarak korunur.
  - `tweet-williams-r-sma-14-geri-cekilme-2023071995768778814` — `tweet-williams-r-sma-14-geri-cekilme-2023071995768778814` (2026-02-15). Tansu imzalı kaynak: "Zaman Dilimi: 30 Dakika", "Williams %R: 14 periyotluk.", "SMA (Basit Hareketli Ortalama): 14 periyotluk." Giriş: "Giriş: Williams %R'ın -50'den yukarı döndüğü mumun (yeşil mum) en yüksek seviyesinin üzerine çıkıldığında işleme girilir." Stop: "Stop Loss: En yakın dip (swing low) seviyesine konulur." Hedef: "Hedef: En az 1:2 Risk/Ödül oranı hedeflenir." (Ham). Okuma (YORUM): önce aşırı alım, ardından -50 dönüşü ve SMA üstü trend filtresi birlikte aranır.
  - `tweet-williams-r-sma-14-geri-cekilme-2023078568993935370` — `tweet-williams-r-sma-14-geri-cekilme-2023078568993935370` (2026-02-15). Aynı stratejinin Tansu alıntısı: "Trend Filtresi: Fiyat, 14 periyotluk SMA çizgisinin üzerinde seyretmelidir." ve "Ön Koşul: Williams %R önce aşırı alım bölgesine (-20 ile 0 arası) girmelidir." (Ham).
  - `tweet-williams-r-sma-14-geri-cekilme-2023083543526793543` — `tweet-williams-r-sma-14-geri-cekilme-2023083543526793543` (2026-02-15). Tansu alıntısında geri çekilme: "Geri Çekilme (Pullback): Williams %R, aşırı alım bölgesinden düştükten sonra -50 seviyesine değmeli ve buradan yukarı dönmelidir." (Ham). Okuma (YORUM): çıktı paylaşımıdır; grafikteki fiyatları genel parametre saymayız.
  - `tweet-wma-ema-fiyat-ustu-al-tarama-1840781392755527958` — 30.09.2024 yön ifadesi aynen korunur: “İki dosyadaki ortalamalar da fiyatın üzerine çıkınca al, altına düşünce sat.” (Ham). Okuma (YORUM): bu söz bölümün fiyat-ortalama yön filtresiyle ters görünür; mevcut filtre değiştirilmez. Karar PR kural değişikliği önerisine taşınır.

## 31. Diğer mum ve konum ipuçları (kısa)

- Sponsor Candle (`gorsel-paket-20-sponsor-candle.md`, `assets/gorsel-paket-20-sponsor-candle/01-bullish-bearish-sponsor-candle.png`): görsel etiketleri `Here is a diagram of a bullish Sponsor candle:` / `bearish`, `Bullish Sponsor Candle (SC)`. Kural (Ham): sert yükseliş öncesi son düşüş mumunun bölgesine dönüşte alıcı beklenir. Eşik YOK; öğretici şema.
- Konsolidasyon body-wick (gp-18): sahibi A §14. Burada tekrar edilmez. (bilet 04, 14.10)
- Mum gölge kodu (`gorsel-paket-76-mum-geometri-formasyon-motoru.md`; `assets/gorsel-paket-76-mum-geometri-motoru/01-python-ohlc-golge-analizi.png`): `upper_shadow = high - max(open, close)`, `lower_shadow = min(open, close) - low` (görselde kod ve 4 mumluk örnek çıktı). Birinci el, tam; giriş kuralı değil.
- Fiyat-hacim konum haritası (gp-128): sahibi A §13. Burada tekrar edilmez. (bilet 04, 14.10)
- Mum gövdesi ve hacim uyumu (`tweet-mum-govde-hacim-anomalisi-uyarisi`; Ham, Ham'da yazar yok; bilet 04, 14.10): geniş gövde + yüksek hacim ve dar gövde + düşük hacim "ok"; geniş gövde + düşük hacim ve dar gövde + yüksek hacim "anomali" ("Sizin paranızı istiyorlar Dikkatli olun"). Dört hücreli uyarı filtresi; yön, giriş, çıkış yok. "Geniş/dar", "yüksek/düşük" eşiği yok (YORUM: gövde/ATR ve hacim/ortalama hacim). Anomalinin sonucu ve testi yok. Günlük veriyle: evet (OHLCV).
- İkili dip ve mum tetikleyicileri (`tweet-ikili-dip-mum-tetikleyicileri`; Ham, Ham'da yazar yok; bilet 04, 14.10): "W" formasyonu: dip, yükseliş, aynı dibin yeniden testi (ikinci bacak). En kritik an ikinci dip testidir; orada Çekiç, Yutan Boğa veya Cımbız Dip mumu ikinci bacağın tamamlandığını ve desteğin çalıştığını teyit eder (Cımbız Dip: §11). Adam ve Havva: ilk dip keskin "V", ikinci dip yayvan; ikinci dipteki çoklu mum (örnek: Sabah Yıldızı) akümülasyonun zamana yayıldığını gösterir. Dip benzerlik toleransı, bacaklar arası süre, boyun çizgisi, stop, hedef yok (YORUM); başarı oranı yok. Günlük veriyle: evet (fikir; sayılar YORUM).
- AZTEK bant (`assets/gorsel-paket-127-aztek-ayi-tuzagi/02-aztek-istatistiksel-bant-ayi-tuzagi.png`): etiketsiz regresyon bandı; kural gizli. Uygulanabilir mi: HAYIR.

---
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-hacimsiz-genis-govde-anomali-1991571046936506411` — Okuma (YORUM): Gövde-hacim uyumsuzluğu uyarısının tekrarı. Ham: "hacimle desteklenmeyen geniş gövdeli mumlar anomalidir demiştim."
  - `tweet-hammer-5-20-ema-kesisim-tarama-1858624611723702533` — Okuma (YORUM): Hammer taramasına son gün EMA5/20 kesişimi eklenir. Ham: "Son gün Fiyat 5 ema üzerinde, 5 ema 20 ema'yı yukarı kessin."
  - `tweet-hammer-ema5-20-tarama-1853083623768883217` — Okuma (YORUM): Hammer ve ters hammer ile EMA5/20 birleşimi planı. Ham: "Hammer ve inverter hammer mumlarını 5-20 ema ile kombinleyerek taramasını yapalım".
  - `tweet-hammer-ema5-20-tarama-1853812714256134418` — Okuma (YORUM): Hammer ve EMA taramasının tekrar paylaşımı. Ham: "Hammer ve 5-20ema taraması".
  - `tweet-hammer-golge-govde-orani-1841562402501869780` — Okuma (YORUM): Hammer gölge/gövde koşulu açık kod olarak verilir. Ham: `if lower_shadow >= 2 * body_size and upper_shadow <= body_size * 0.3`.
  - `tweet-hammer-mum-taramasi-1841567398660305114` — Okuma (YORUM): Hammer aramasının iki zaman kapsamı. Ham: "Bir tanesi hisselerin tamamında hammer arıyor tarihten bağımsız, diğeri ise son gün hammer arıyor."
  - `tweet-harami-roc-adx-obv-tarama-1841763719098847662` — Okuma (YORUM): Harami aracına gösterge katmanları ekleme planı. Ham: "Alt grafiğe roc50 adx/adxr ve obv/sma20koyalım." Kullanım: "bunları hem tarama koşulu olarak hemde sadece indikatör olarak kullanacağız".
  - `tweet-mum-formasyonu-ema-birlikte-1908282009488924977` — `tweet-mum-formasyonu-ema-birlikte-1908282009488924977` (2025-04-04): Ham: "Ema'ları koyun çalışın işte". Okuma (YORUM): mum formasyonu grafiğine EMA ekleme önerisidir.
  - `tweet-mum-formasyonu-pivot-destek-1848484346749214753` — `tweet-mum-formasyonu-pivot-destek-1848484346749214753` (2024-10-21): Ham: "Son gün bullish 3LINESTRIKE, HAMMER, ENGULFING, DOJI sinyalleri". Okuma (YORUM): pivot ve destek çizgileriyle sunulan günlük mum taraması örneğidir.
  - `tweet-mum-formasyonu-pivot-taramasi-1845371629993414881` — `tweet-mum-formasyonu-pivot-taramasi-1845371629993414881` (2024-10-13): Ham: "Son gün BIST100 boğa sinyallerimizi gözden geçirelim". Okuma (YORUM): mum ve pivot taramasının günlük çıktı örneğidir.
  - `tweet-mum-formasyonu-pivot-taramasi-1845372312620552554` — `tweet-mum-formasyonu-pivot-taramasi-1845372312620552554` (2024-10-13): Ham: "Hisse: AGHOL., Formasyon: ENGULFING_Bear". Okuma (YORUM): ayı mum formasyonu taramasının tek hisse örneğidir.
  - `tweet-mum-formasyonu-tanimlama-kodu-1899964404872941880` — `tweet-mum-formasyonu-tanimlama-kodu-1899964404872941880` (2025-03-12): Açılan görsel: "data.at[data.index[i + 1], 'buy_signal'] = 1". Okuma (YORUM): mevcut yeşil mum kapanışı önceki açılış ve kapanıştan büyüktür; mevcut açılış önceki kapanıştan küçüktür; önceki mum kırmızıdır ve kapanışı iki önceki açılıştan küçüktür. Sinyal sonraki bara yazılır. Görsel metni aktarımında iki büyüktür işareti küçüktür yazılmıştır; okuma açılan görsele dayanır.
  - `tweet-osilator-uyumsuzluk-cikis-sinyali-1766680374950740205` — `tweet-osilator-uyumsuzluk-cikis-sinyali-1766680374950740205` (2024-03-10): Ham: "RSI, uyuşmazlıkların görülmesi için önemli fırsatlar sağlayabilir." Okuma (YORUM): DOAS için düşüşten kaçış örneği anlatılır; açılan görselin osilatör etiketi CCI’dır, RSI diye düzeltilmez.
  - `tweet-piercing-formasyonu-backtest-1906062787979210957` — `tweet-piercing-formasyonu-backtest-1906062787979210957` (2025-03-29): Ham: "Bunlar momentum hisselerim değil, basit taramalar. Detayına siz bakacaksınız artık". Okuma (YORUM): Piercing taramasının KRVGD örneği, momentum listesiyle karıştırılmamalıdır.
  - `tweet-talib-mum-formasyonu-tespiti-1943070866323181796` — Okuma (YORUM): Endekste Marubozu kapanışına ertesi gün iyimserliği bağlayan örnek. Ham: “endeks marubozu kapattı, yarın güzel bir gün olacak.” Okuma (YORUM): Tek günlük beklentidir; gerçekleşmiş getiri kanıtı değildir.

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
- Çoklu gösterge seti, günlük ve haftalıkta birlikte al (`tweet-coklu-indikator-gunluk-haftalik-al-1852771794739966025`; Ham; Tansu'nun X gönderisi, 02.11.2024; görsel yok; duyuru "Pek yakında", kod ve çıktı yok): Ham: "Yeni indikatörümüz" "MACD,CCI, Trend Takip" "DMI,DIOSC,MOM,Her piyasada kullanılmalı." "RSI,STOK, Aşırı alım satım" "OBV, İşlem hacmi" "Bunlara günlük ve haftalık bakacağız." "Hem haftalıkta hem de günlükte al sinyali verenleri listeleyeceğiz." Parametre: sekiz gösterge (MACD, CCI, DMI, DIOSC, MOM, RSI, Stokastik, OBV), iki zaman dilimi (günlük ve haftalık, ikisinde birden al); her göstergenin "al" tanımı, periyot, eşik ve kaç göstergenin al vermesi gerektiği yok. YORUM: DIOSC = DMI osilatörü (+DI ile -DI farkı), MOM = momentum; haftalık mum günlük veriden türetilir. Şubat 2024 THYAO gösterge setinde (`tweet-cci-posc-macd-gosterge-seti-1761507718693548409`) CCI (20 günlük EMA'lı), MACD, Stokastik ve Momentum (8 günlük MA'lı) çizilmişti; aynı ayarların bu sete taşındığı yazılı değil. Tansu'nun kanıtı: yok (duyuru). Günlük veriyle: evet (OHLCV), tanımlar olmadan kodlanamaz. Hazırlık X. Kaynak güveni: Ham birinci el; yapı açık, sayı yok: düşük.
- CCI üstüne MOST sistemi, DOAS saatlik sınama özeti (`tweet-cci-uzerine-most-sistemi-1782789450767962601`; Ham; G2 açıldı, G1 ve G3 görsel metni; Tansu'nun X gönderisi, 23.04.2024): "#DOAS uzun vadeli yatırımcı olmak bu ülkede zor. matematiğin istatistiğin dediğine kulak vermek lazım keşke satsaymışım dememek için." "Gerçi bende pek uymuyorum buna ama artık uyacağım:)" "Bir kaç kere tavanı yakalayınca unutulmuyor." (Ham). Sistem adı "CCI ÜSTÜNE MOST OPT"; MOST göstergesi CCI serisine uygulanır (YORUM); al ve sat koşulu yazılı değil. B'deki MOST ve HO kesişim sistemi ile aynı araç ve aynı tür sonuç özetidir (yukarıdaki MOST ve HO bullet'ı). Parametre: optimizasyon değerleri OPT1 = 52, OPT2 = 3 (görsel, açıldı; anlamı yazılı değil, YORUM: 52 periyot, 3 yüzde); test aralığı 30.01.2024 17:00 - 22.04.2024 18:00, 500 bar; grafik başlığı "DOAS  60  TL" (G3 görsel metni; işlem saatleri 17:00 ve 18:00, YORUM: 60 dakikalık çubuk); başlangıç bakiyesi 10000, son 13467,29, getiri 3467,29 (%34,67), komisyon masrafı 321,73; 5 işlem, hepsi long: 3 kârlı (toplam 3920,57), 2 zararlı (toplam 453,27); ort. kâr 1306,86, ort. zarar 226,64 (oran 5,77); en kârlı pozisyon 04.04.2024 15:00 - 18.04.2024 13:00, 55 bar, 23,76; en zararlı 29.03.2024 10:00 - 02.04.2024 16:00, 24 bar, -3,39 (birim yazılı değil, YORUM: yüzde); son işlem SAT 18.04.2024 13:00, 345,71; son fiyat 319,00 (22.04.2024). Hesap kontrolü (bizim): 3920,57 - 453,27 = 3467,30 (görsel 3467,29: yuvarlama); 3920,57 / 3 = 1306,86; 453,27 / 2 = 226,64; 1306,86 / 226,64 = 5,77; çıkış fiyatından sonraki düşüş (345,71 - 319,00) / 345,71 = %7,7. Tansu'nun gerekçesi: sistem 18.04.2024'te SAT verdi, sonra fiyat düştü; sistem sinyaline uymak gerekir. Tansu'nun kanıtı: tek hisse, yaklaşık üç ay, 5 işlem, optimize edilmiş ayar (örneklem içi); seçilmiş örnek. MOST ve CCI ayarlarının anlamı, optimizasyon aralığı ve ölçütü, örneklem dışı doğrulama ve komisyonun kâr rakamlarına dahil olup olmadığı yok. Hisse bazlı optimizasyon ve parametre: karar Levent'te bekliyor (E K29). Günlük veriyle: hayır (saatlik veri; günlük kurmak için MOST ve CCI ayarı ile al-sat koşulu gerekir). Hazırlık X. Kaynak güveni: Ham ve görsel birinci el; sayılar net, kural yok: orta-düşük.
- Uzun süren ve dengeli momentum ölçümü (`tweet-dengeli-momentum-cok-ufuk-drawdown-risk-1958442372557144525`; Ham; Tansu'nun X gönderisi, 21.08.2025; görsel yok): "Uzun süren ve dengeli momentum’u hesaplamanın yolu aslında kısa vadeli gürültüyü azaltıp, kalıcı yön değişimlerini yakalamaktır." "Örneğin son 1 ay, 3 ay ve 6 aylık getirilerin hepsini aynı formülde tartarak birleşik bir momentum elde edilir." (Ham). Beş katman (Ham'dan özet; formül Tansu'da yok): yarı ömürlü ağırlıklandırma (ağırlıklar "üstel şekilde değil daha yavaş azalır"); istikrar (risk-ayarlı momentum: getirilerin varyansı veya karelenmiş sapmaları, "düşük oynaklıkta istikrarlı bir getiri" tercih edilir); sektör senkronizasyonu (aynı sektördeki benzer varlıkların yön birlikteliği); çoklu ufuk (1, 3 ve 6 ay); drawdown profili (iyi momentumda düşüşler "hem sınırlı hem de hızlı onarılan" yapıdadır). Parametre: yalnız ufuklar 1 ay, 3 ay, 6 ay. Ufuk ağırlıkları, yarı ömür ve ağırlık fonksiyonu, varyans penceresi, senkronizasyon ölçüsü, drawdown ölçüsü, katmanların tek skorda birleşmesi ve giriş, çıkış, eşik yok. İlgili: §14 (12 aylık on-dilim), §15 (Clenow skoru), §18 (rolling alpha ve skewness katmanı). Tansu'nun kanıtı: yok (sonuç, örnek, sembol yok). Günlük veriyle: kısmen (getiri, varyans ve drawdown günlük kapanıştan; sektör senkronizasyonu için sektör sınıflaması gerekir). Hazırlık X. Kaynak güveni: Ham birinci el; kavramsal çerçeve, tek sayısal ayar 1/3/6 ay: düşük.
- EMA'nın EMA'sı ile ayrışma, satış zamanı yaklaşıyor uyarısı (BRSAN; `tweet-ema-uzerinden-ema-ayrisma-1760725146959270113`; Ham ve kod görseli birinci el, iki görsel, G1 açıldı; Tansu'nun X gönderisi, 22.02.2024, iki gönderilik zincir): "#BRSAN hissesi için #Python'da kısa ama etkili bir kodlama." "Hisseni 5 günlük üssel hareketli ortalaması ve bununda 10 üssel hareketli ortalaması alındı. Böylece ortalamaların birbirinden uzaklaşması görselleştirildi. Hızlı olanın yavaş olandan uzaklaşması-->" ve "trade edenlerin karlarının arttığını ve artık satış zamanının yaklaştığını gösterir. Geliştirilebilir." (Ham). Kod (görsel, açıldı): `ema1 = hesapla_ema(fiyat_serisi, 5)`, `ema2 = hesapla_ema(ema1, 5)`, `k = 2 / (gun_sayisi + 1)`, `ewm(alpha=k, adjust=False)`; `sinyaller['al']` ve `sinyaller['sat']` ema1 ile ema2 karşılaştırmasıdır (satırlar görselde sağdan kesik). YORUM: ayrışma = ema1 − ema2 farkının büyümesi; kısa vadeli işlemcilerin kârının arttığı ve satışın yaklaştığı uyarısıdır, yani çıkış (kâr alma) uyarısıdır, giriş sinyali değildir. Parametre: hızlı EMA = 5 günlük EMA (kapanış); yavaş çizgi = EMA(EMA5, 5) (kod) ve Ham "10" der: Ham ile kod çelişir, kod görseli birincil sayılır (YORUM); EMA katsayısı alpha = 2 / (periyot + 1). Ayrışma eşiği, ayrışma ölçüsü (mutlak fark mı yüzde mi), al ve sat ek koşulları (kod satırları kesik) ve çıkış yok. Aynı gün aynı kurulum için kesişim kodu: §60. İlgili: E K25 (13 EMA ve ATR merdiveni), E K28 (kâr alma). Tansu'nun kanıtı: yok (tek grafik, sonuç yok). Günlük veriyle: evet (günlük kapanış); eşik olmadığı için kural yarım. Hazırlık X. Kaynak güveni: Ham ve kod görseli birinci el; Ham ile kod arasında çelişki; eşik yok: düşük.
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-vegas-ema-tek-hisse-optimizasyonu-1846299109302362243` — Vegas (3 EMA) için optimizasyon yapıldı, hisse başına çalışır: "Vegas için optimizasyon yaptım. 3 EMA var. Tam 1 saat sürdü optimizasyon." ve "OPT'leri tek hisse için yapıyoruz." (Ham; üst gönderi de Ham'da: kod, optimizasyon ve getiri hesabı dış bağlantıda, açılmadı). Arama aralığı, ölçüt, sonuç ve örneklem dışı doğrulama yok. Hisse bazlı optimizasyon: karar Levent'te bekliyor.
  - `tweet-vegas-tuneli-ema-optimizasyon-8-150-150-1828161056960827738` — Vegas tüneli EMA seti DOAŞ için optimize edildi: "Soldaki 12-144-169, sağdaki ise optimize edilmiş ema'lar ile getiri grafiği. (8-150-150)" (Ham). Ham sonuç (yanıt): 2022–2024'te al-tut 7,49 kat, 12-144-169 6 kat, optimize 7 kat; "strateji alpha yaratamamış ama getiri eğrisi daha iyileştiği kesin" (Ham). Görselde son değerler yaklaşık 5,4 (al-tut), 4,3 (12-144-169), 5,1 (optimize) (görsel, açıldı; ölçüm). Tek hisse, örneklem içi; giriş ve çıkış kuralı yok. Hisse bazlı optimizasyon: karar Levent'te bekliyor. Parametre: Vegas optimize EMA seti (DOAŞ, 2022–2024) = 8-150-150 (Ham). Okuma notu: Ham sayıları (al-tut 7,49 kat, 12-144-169 6 kat, optimize 7 kat) görseldeki son değerlerle uyuşmaz: creturns ≈5,4, cstrategy ≈4,3 (G1) ve ≈5,1 (G2) (görsel, açıldı; ölçüm). Oranlar tutarlıdır (6/7,49 = 0,80; 4,3/5,4 = 0,80; 7/7,49 = 0,93; 5,1/5,4 = 0,94), düzey farkı açıklanmamış (görselde tepe ≈8,5). Görsel doğru sayılır.
  - `tweet-vegas-tuneli-geri-test-doas-1827794622434640093` — Vegas tüneli 12-144-169 günlük EMA seti DOAŞ'ta al-tutu geçemedi: "2022-2024 yılları arasında vegas tüneli stratejisi doaş getirisine yenik düşmüştür." (Ham). Görselde son değerler cstrategy ≈4,3, creturns (al-tut) ≈5,4 (görsel, açıldı; ölçüm). Tansu EMA'ların optimize edilebileceğini söyler; kod ve veri dış bağlantıda (açılmadı); giriş ve çıkış kuralı yok. Hisse bazlı optimizasyon: karar Levent'te bekliyor. Parametre: Vegas sonucu, DOAŞ 2022–2024, EMA 12-144-169: strateji ≈4,3 kat, al-tut ≈5,4 kat (görsel, açıldı; ölçüm)
  - `tweet-ema-12-144-169-uclu-1783160562156716179` — Tekrar: 12-144-169 EMA seti nasıl kurulur: "Ema 3 kez seçin. Uzunlukları 12-144-169 yapın" (Ham, yanıt, 24.04.2024; üst gönderi notta yok). Üç ayrı EMA göstergesi eklenir; giriş ve çıkış kuralı yok. Aynı setin kesişim taraması: §63.
  - `tweet-ema5-ema13-roc20-parametre-varyanti-1842233841034883242` — 2024-10-04: “EMA 10 ve EMA 20 yerine EMA 5 ve EMA 13 kullanıldı.” ve “ROC 50 yerine ROC 20 hesaplandı” (Ham). Okuma (YORUM): görsel seçim çalışmasıdır; kaynak “Backtest yapmadan önce” der. ADX/ADXR, DMI ve OBV/SMA20 panelleri ayrıca anlatılır.
  - `tweet-ema9-sma21-kesisim-sinyal-kodu-1837546767459525036` — `tweet-ema9-sma21-kesisim-sinyal-kodu-1837546767459525036` (2024-09-21; Ham ve varsa görsel): EMA9-SMA21 örnek kodu: "# 9 periyotlu EMA ve 21 periyotlu SMA hesaplaması" ve "# Crossover sinyallerini belirleme" (görsel açıldı). Okuma (YORUM): kod EMA9 > SMA21 durumunun farkını kesişim olarak işaretler.
  - `tweet-ema9-stochrsi-1853496357958389772` — `tweet-ema9-stochrsi-1853496357958389772` (2024-11-04; Ham ve varsa görsel): EMA9 ve StochRSI birlikteliğinde ek teyit önerisi: "ema9 ve StochRSI" ve "Farklı indikatörlerden destek almak lazım" (Ham).
  - `tweet-ema9-stokrsi-gun-ici-1853470102810669319` — `tweet-ema9-stokrsi-gun-ici-1853470102810669319` (2024-11-04; Ham ve varsa görsel): Gün içi gösterge birleşimi: "Hazır gün içi sinyal, iki gözümün çiçeği, fiyat 9ema ve stocRSI" (Ham). Okuma (YORUM): bu paylaşım birleşimin örneğidir, tek başına kesin giriş koşulu değildir.
  - `tweet-esas-faaliyet-kari-rsi-takas-birlesimi-1940440747917885592` — `tweet-esas-faaliyet-kari-rsi-takas-birlesimi-1940440747917885592` (2025-07-02; Ham): RSI teyidi: "RSI (Relative Strength Index) göstergesinin 30 seviyesinin altından yukarı doğru dönmesi, hissede bir alım sinyalinin geldiğine işaret edebilir." Sınır: "Ancak RSI sinyali tek başına bir karar aracı değildir, temel verilerle desteklenmelidir."
  - `tweet-esik-0-5-yukari-kesme-sinyal-1857956253579772276` — `tweet-esik-0-5-yukari-kesme-sinyal-1857956253579772276` (2024-11-17): Eşiğin yukarı kesilmesi: "0.5’i yukarı kestiğinde sinyal gelmiş olacak" (Ham). Okuma (YORUM): sinyal serisinin adı bu yanıtta belirtilmez; başka bir göstergenin eşiğine aktarılmaz.
  - `tweet-fiyat-wma-5-14-34-55-rsi-50-1844992177274773869` — `tweet-fiyat-wma-5-14-34-55-rsi-50-1844992177274773869` (2024-10-12): WMA ve RSI taraması: "Fiyatın 5-14-34-5 WMA'sının son günde üzerinde kapattığı tek hisse" ve "RSI > 50 filtresi de uyugulanmıştır" (Ham). Görsel başlığında "WMA5-WMA14-WMA34-WMA55 ve RSI21 > 50", alt panelde "RSI14" yazılıdır (görsel açıldı). Okuma (YORUM): WMA son dönem yazımı ve RSI dönemi belirsizliği korunur.
  - `tweet-fourier-dominant-dongu-faz-sinyali-1978783564511481981` — `tweet-fourier-dominant-dongu-faz-sinyali-1978783564511481981` (2025-10-16): Fourier sinyal fikri: "dominant sinüs bileşenlerinin faz geçişlerini al-sat sinyali olarak kullandığımda" (Ham). Boyutlama bağlantısı: "Amplitüd artışları volatilite artışının habercisi. Böylece pozisyon büyüklüğünü dinamik olarak ayarlayabiliyorsunuz." Okuma (YORUM): yüksek alfa iddiası bu notta ölçülmüş doğrulama yerine anlatı düzeyindedir.
  - `tweet-fourier-sinus-dongu-faz-1955281569599402000` — `tweet-fourier-sinus-dongu-faz-1955281569599402000` (2025-08-12): Baskın döngü yönü: "Eğer baskın sinüs dalgası pozitif eğime geçmişse, piyasa yukarı yönlü ivme kazanıyor demektir." ve "Negatif eğim ise aşağı yönlü bir momentumun habercisidir." (Ham).
  - `tweet-fourier-wavelet-hibrit-dongu-analizi-1978893346727956651` — `tweet-fourier-wavelet-hibrit-dongu-analizi-1978893346727956651` (2025-10-16): Fourier-Wavelet yöntem sırası: "dominant periyotları bulunur, sonra Wavelet ile o periyotların zamanla nasıl değiştiğine bakılır." (Ham). Sınır: "hangi dönemde hangi döngü aktif belli olmaz".
  - `tweet-frama-kesisim-al-sat-kodu-1910723570654753121` — `tweet-frama-kesisim-al-sat-kodu-1910723570654753121` (2025-04-11): FRAMA örnek kodu: "def calculate_frama_signals(data, period=16):" (görsel açıldı). Alış: "data['Buy_Signal'] = (data['Close'] > data['FRAMA']) & (data['Close'].shift(1) <= data['FRAMA'].shift(1))". Satış: "data['Sell_Signal'] = (data['Close'] < data['FRAMA']) & (data['Close'].shift(1) >= data['FRAMA'].shift(1))". Okuma (YORUM): bunlar paylaşılan örnek kodun şartlarıdır.
  - `tweet-most-al-sinyali-taramasi-1843751550503768113` — `tweet-most-al-sinyali-taramasi-1843751550503768113` (2024-10-08): Ham: "Son gün BİST100 MOST al verenler". Okuma (YORUM): MOST giriş sinyali taramasının günlük çıktı örneğidir.
  - `tweet-most-giris-sinyali-tarama-1844079823829991777` — `tweet-most-giris-sinyali-tarama-1844079823829991777` (2024-10-09): Ham: "MOST giriş sinyali olan hisseler". Okuma (YORUM): tarama ve tek hisse grafik kodunun dağıtımıdır.
  - `tweet-most-hareketli-ortalama-kesisim-formulu-1779421690071490990` — `tweet-most-hareketli-ortalama-kesisim-formulu-1779421690071490990` (2024-04-14): Görsel: "if(MOV(C,opt1,E)>MOST(C,opt1,opt2)," ve "Cross(MOV(C,opt3,E),MOST(C,opt3,opt4)),". Okuma (YORUM): koşula göre opt3/4 veya opt5/6 ile alış kesişimi seçilir; satışta kesişim yönü ters çevrilir. Görsel OPT1 15–34/adım 1, OPT2 2–6/adım 0,5, OPT3 ve OPT5 2–15/adım 1, OPT4 ve OPT6 0,5–5/adım 0,5 aralıklarını verir.
  - `tweet-most-hareketli-ortalama-kesisim-opt-1783412420716761320` — `tweet-most-hareketli-ortalama-kesisim-opt-1783412420716761320` (2024-04-25): Ham: "AL FORMÜLÜ   CROSS(MOV(C,OPT1,E),MOST(C,OPT1,OPT2))"; "Al sat sinyalleri ve overall hisseye periyoda göre farklılıklar gösterir. Test ediniz." Okuma (YORUM): satış ters kesişimdir. Açılan görselde OPT1 2–100/adım 1; OPT2 0,5–5/adım 0,1 örnek aralıklarıdır.
  - `tweet-mov-most-kesisim-al-sat-kodu-1782497478056558995` — `tweet-mov-most-kesisim-al-sat-kodu-1782497478056558995` (2024-04-22): Ham: "CROSS(MOV(C,OPT1,E),MOST(C,OPT1,OPT2))"; "CROSS(MOST(C,OPT1,OPT2),MOV(C,OPT1,E))". Okuma (YORUM): AL ve SAT ters yönlü MOV/MOST kesişimleridir. Açılan görselde OPT1 2–30/adım 1/varsayılan 3 ve OPT2 0,5–5/adım 0,5/varsayılan 2 örnekleri vardır.
  - `tweet-net-isletme-sermayesi-cari-oran-filtre-1946652254116684019` — `tweet-net-isletme-sermayesi-cari-oran-filtre-1946652254116684019` (2025-07-19): Ham: "Cari Oran 1.5 Üzerinde Olmalı"; "Borç Oranı (Toplam Borç / Toplam Varlıklar) %50’nin Altında Olmalı"; "RSI Göstergesi 30-40 Bandından Yukarı Dönüyorsa". Okuma (YORUM): pozitif NİS ve nakit akışı, artan faaliyet marjı/ROE/satış/net kâr, stabil NİS/satış oranı ile destek tepkisi, hacimli kırılım ve 50 günlük ortalama kesişimini birleştiren örnek stratejidir. Ham: "Yatırımın %3-5’inden Fazla Zararı Göze Alma"; "Destek altına düşerse sat."; "İlk Hedef, Son Tepelerdir". Bu örnek mevcut risk bütçesinin yerine geçirilmez.
  - `tweet-net-kar-marji-destek-hacim-hibrit-1918694632281592272` — `tweet-net-kar-marji-destek-hacim-hibrit-1918694632281592272` (2025-05-03): Ham: "Gözüm hep yüksek net kâr marjı + Teknik destekten sekme + Hacim artışı." Okuma (YORUM): sektör üstünde ve istikrarlı artan marj, destek tepkisi ve hacim hibrit seçim fikridir.
  - `tweet-ott-hhv-llv-ma-kesisim-formul-1790974588156821797` — `tweet-ott-hhv-llv-ma-kesisim-formul-1790974588156821797` (2024-05-16): Ham: "Dakikalık grafikte @Anil_Ozeksi üstadın formülünü deneyin derim." Açılan görsel: "Cross(MOV(C,opt1,VAR),OTT(HHV(H,opt2),2,opt3)) OR". Okuma (YORUM): MOV ile HHV/LLV tabanlı iki OTT sınırı, orta seviye ve iki ara seviye arasındaki beş yukarı kesişim OR ile alış üretir; satış yönleri terstir. Dakikalık örnek günlük kurala dönüştürülmez.
  - `tweet-ott-trend-takipci-tradingview-kodu-1790007806801621475` — `tweet-ott-trend-takipci-tradingview-kodu-1790007806801621475` (2024-05-13): Ham: "Etkili olup olmadığını bilemiyorum." Açılan görsel: "length_ott  = input.int(30,    'OTT Period', minval=1)"; "percent_ott = input.float(7.0, 'OTT Percent', step=0.1, minval=0)"; "out = nz(OTT[2])". Okuma (YORUM): kapanış kaynaklı VAR ortalamasıyla yön değişimli long/short stop hesaplanır, OTT iki çubuk gecikmeyle çizilir; 30 ve %7 örnek ayarlardır.
  - `tweet-parabolik-sar-adx-al-sinyali-1864260274355626306` — `tweet-parabolik-sar-adx-al-sinyali-1864260274355626306` (2024-12-04): Açılan görsel: "Parabolic SAR - Signals for AGYO.IS"; "ADX and ADXR"; "Momentum Indicator"; "Average Volume (10 bars)". Okuma (YORUM): PSAR alış/satış işaretlerini ADX/ADXR, momentum ve 10 çubuk hacim ortalamasıyla gösteren örnektir; tek sonuç genel başarı kanıtı değildir.
  - `tweet-parabolik-sar-kesisim-sinyali-1862617662196473882` — `tweet-parabolik-sar-kesisim-sinyali-1862617662196473882` (2024-11-29): Ham: "yeni kod çalışmamız da tamamlanmıştır. PSAR". Açılan görsel: "Parabolic SAR Strategy with Cross Points for ADESE.IS". Okuma (YORUM): fiyat/PSAR kesişim bölgelerinde alış-satış işaretleri gösterilir.
  - `tweet-pddd-rsi30-fk-sma200-tarama-1938905375119434125` — `tweet-pddd-rsi30-fk-sma200-tarama-1938905375119434125` (2025-06-28): Ham: "FK oranı da 5 ile 15 arasındaysa"; "RSI kesişimi sonrası hacim artışıyla birlikte teyit alarak kademeli girişler yapmaktır." Okuma (YORUM): PD/DD<1, RSI 30 altından yukarı dönüş, F/K 5–15 ve 200 günlük ortalama altında fiyat birleşimiyle aday sepeti izlenir; hacim teyidiyle kademeli giriş önerilir.
  - `tweet-rsi-ema-sma-hesaplama-farki-1845465765421453791` — - `tweet-rsi-ema-sma-hesaplama-farki-1845465765421453791` (2024-10-13; Tansu'nun X gönderisi). RSI hesaplama farkı (Ham): "Pandas_ta ema tabanlı rsi hesaplıyor" / "Benim kodum ise sma tabanlı rsi hesaplıyor". Okuma (YORUM): bu hesap tercihi notun kendi koduna aittir; öteki RSI taramalarına aktarılmaz.
  - `tweet-rsi-fiyat-egim-uyumsuzlugu-sat-1995355839100559854` — - `tweet-rsi-fiyat-egim-uyumsuzlugu-sat-1995355839100559854` (2025-12-01; Tansu'nun X gönderisi). Fiyat ve RSI eğimi (Ham): "Eğer Fiyat Slope > 0 iken RSI Slope < 0 ise (Uyumsuzluk)" Okuma (YORUM): eğim penceresi seçimi ayrıca gerekir.
  - `tweet-rsi-kirilim-closingmarubozu-sinyal-1911384911908388875` — - `tweet-rsi-kirilim-closingmarubozu-sinyal-1911384911908388875` (2025-04-13; Tansu'nun X gönderisi). RSI kırılımı ve CLOSINGMARUBOZU (Ham ve görsel metni): "Son noktada RSI, bu kırmızı trend çizgisini yukarı doğru kırmış." / "Bu, momentumda pozitif bir dönüş sinyali olabilir." / "Takip eden günlerde hacim ve fiyat onayı alınması yerinde olur." Okuma (YORUM): 37-38 RSI düzeyi örnektir; genel eşik yapılmaz.
  - `tweet-rsi-kirilim-marubozu-1909769680841028023` — - `tweet-rsi-kirilim-marubozu-1909769680841028023` (2025-04-09; Tansu'nun X gönderisi). DESPC örneği (Ham ve görsel metni): "güzel bir marubozu ve RSI düşen kırılımı". Okuma (YORUM): mum ile RSI kırılımının birlikte görülmesine örnektir.
  - `tweet-rsi-kirilim-rsi50-marubozu-1909715584134099312` — - `tweet-rsi-kirilim-rsi50-marubozu-1909715584134099312` (2025-04-08; Tansu'nun X gönderisi). RSI kırılımı birleşimi (Ham ve görsel metni): "Bu değerli kardeşimiz hem RSI düşeni kırmış hem RSI>50 yapmış hem de marubozu bırakmış:)".
  - `tweet-rsi-negatif-uyumsuzluk-1840317895487762696` — - `tweet-rsi-negatif-uyumsuzluk-1840317895487762696` (2024-09-29; Tansu'nun X gönderisi). TUPRS uyumsuzluk örneği (Ham ve görsel metni): "Uyumsuzluklara feci takığım." Okuma (YORUM): sonuçtan geriye bakan grafik yorumudur; sınama kanıtı değildir.
  - `tweet-rsi-negatif-uyumsuzluk-1909725387703173557` — - `tweet-rsi-negatif-uyumsuzluk-1909725387703173557` (2025-04-08; Tansu'nun X gönderisi). THYAO örneği (Ham ve görsel metni): "İşte buna bearish divergence deniyor." Okuma (YORUM): adlandırma örneğidir; tarama tanımı olarak kullanılmaz.
  - `tweet-rsi-negatif-uyumsuzluk-1939548303470846230` — - `tweet-rsi-negatif-uyumsuzluk-1939548303470846230` (2025-06-30; Ham ve görsel metni; Tansu'nun X gönderisi): "uyumsuzluğun en güzel örneklerinden birisi değil mi..." Okuma (YORUM): ORMA haftalık grafik örneği.
  - `tweet-rsi-negatif-uyumsuzluk-1983245122662731916` — - `tweet-rsi-negatif-uyumsuzluk-1983245122662731916` (2025-10-28; Ham ve görsel metni; Tansu'nun X gönderisi): "Hiç bir şey bilmiyor isen RSI negatif uyumsuzluğu öğren, çok şey katar." Okuma (YORUM): LIDER negatif uyumsuzluk uyarısı.
  - `tweet-rsi-negatif-uyumsuzluk-giris-yasagi-1842576684501086648` — - `tweet-rsi-negatif-uyumsuzluk-giris-yasagi-1842576684501086648` (2024-10-05; Ham ve görsel metni; Tansu'nun X gönderisi): "Yani şu negatif uyumsuzlukları göre göre girmeyin hisselere lütfen ya" Okuma (YORUM): Negatif uyumsuzlukta girişten kaçınma uyarısı.
  - `tweet-rsi-ortalama-kesisimi-ema50-1778104659267232010` — - `tweet-rsi-ortalama-kesisimi-ema50-1778104659267232010` (2024-04-10; Ham ve görsel metni; Tansu'nun X gönderisi): "RSI kendi ortalamasını da kesmiş yani momentumu artmış, güzel." Okuma (YORUM): EKOS için kendi RSI ortalaması kesişimi ve EMA50 bağlamı.
  - `tweet-rsi-peak-trendline-break-1912929231765684640` — - `tweet-rsi-peak-trendline-break-1912929231765684640` (2025-04-17; Ham ve görsel metni; Tansu'nun X gönderisi): "Siz olsanız ne yaparsınız?" Okuma (YORUM): RUBNS grafiğiyle okuyucuya soru; doğrudan işlem talimatı değildir.
  - `tweet-rsi-tepe-lookback-trend-cizgisi-1909750908054823082` — - `tweet-rsi-tepe-lookback-trend-cizgisi-1909750908054823082` (2025-04-08; Tansu'nun X gönderisi). Ham: "Optimizasyon çalışmaları devam:)". Görsel (açıldı): "RSI (1 yıl) + Son 60 Günlük Düşen Tepe Trend Analizi". Okuma (YORUM): 60 günlük çizim penceresi bu optimizasyon örneğine aittir.
  - `tweet-rsi-ustune-most-explorer-tarama-1783371645224149075` — - `tweet-rsi-ustune-most-explorer-tarama-1783371645224149075` (2024-04-25; Tansu'nun X gönderisi). RSI üstüne MOST (Ham): "CROSS(MOV(RSI(C,14)+1000,3,e),MOST(RSI(C,14)+1000,3,2))". Okuma (YORUM): Explorer ifadesi doğrudan kaynak kodudur.
  - `tweet-rsi-uyumsuzluk-tespiti-1909986965295874148` — - `tweet-rsi-uyumsuzluk-tespiti-1909986965295874148` (2025-04-09; Tansu'nun X gönderisi). Ham: "Uyumsuzlukları kodlamanın yapay sinir ağları kodlamaktan daha karın ağrıtıcı bir yanı var, ciddiyim:)". Okuma (YORUM): MERCN dip-tepe ve RSI çizimi geliştirme örneğidir.
  - `tweet-rsi21-negatif-uyumsuzluk-tepe-dusus-1840171811075486172` — - `tweet-rsi21-negatif-uyumsuzluk-tepe-dusus-1840171811075486172` (2024-09-28; Tansu'nun X gönderisi). Negatif uyumsuzluk (Ham): "Fiyat artarken RSI21 tepesi düşmüş." / "Aman ha uyumsuzluklar önemli olabilir." Okuma (YORUM): ANGEN örneğinde RSI21 kullanılır.
  - `tweet-rsi30-kesisim-sma50-rsi50-red-1990003872023130607` — - `tweet-rsi30-kesisim-sma50-rsi50-red-1990003872023130607` (2025-11-16; Tansu'nun X gönderisi). RSI30 takip (Ham): "Çoğu zaman RSI30 kesişimi olduğunda tepedeki ilk direnç 50SMA olur." / "beraber veya münferiden RSI50 reddi ve / veya SMA50 reddi ile takip edebilirsiniz."
  - `tweet-rsi30-yukari-kesis-sma250-kirilim-sma50-hedef-1991558168149987328` — - `tweet-rsi30-yukari-kesis-sma250-kirilim-sma50-hedef-1991558168149987328` (2025-11-20; Tansu'nun X gönderisi). RSI30 takip örneği (Ham): "250 günlük ortalamayı da yıkmış" / "Normalde rsı30'u yukarı kesilmesi ile ilk temas sma50 ya da rsı50 olur." Okuma (YORUM): örnekten bütün hisseler için kesin hedef çıkarılmaz.
  - `tweet-rsi55-rsi-ema66-rsi22-tarama-1775119470484156713` — - `tweet-rsi55-rsi-ema66-rsi22-tarama-1775119470484156713` (2024-04-02; Tansu'nun X gönderisi). Tarama (Ham): "RSI’nin 55’ten az olsun" / "RSI’nin 66 günlük üssel hareketli ortalaması, 22 günlük RSI değerinden düşük olsun" / "fiyat değişim oranı bir gün için %5’ten fazla olsun".
  - `tweet-saatlik-ema-macd-rsi-cmf-bollinger-tarama-1848610322438869285` — - `tweet-saatlik-ema-macd-rsi-cmf-bollinger-tarama-1848610322438869285` (2024-10-22; Tansu'nun X gönderisi). Görsel (açıldı): "DERHL.IS Saatlik taramada EMA5 EMA10 EMA20'yi yukarı kesen, MACD RSI14>50 VE CMF şartlarını sağlayıp AL sinyali verdi." Okuma (YORUM): CMF içeren saatlik varyanttır.
  - `tweet-saatlik-ema-macd-rsi-obv-tarama-1848262958247251979` — - `tweet-saatlik-ema-macd-rsi-obv-tarama-1848262958247251979` (2024-10-21; Tansu'nun X gönderisi). Ham: "Saatlik taramada son kapanış EMA5-10-20 MACD RSI14-50 VE OBV50 koşullarını sağlayıp AL sinyali veren hisse bulunamadı." Okuma (YORUM): boş sonuç da tarama koşullarının kullanım örneğidir.
  - `tweet-saatlik-ema-macd-rsi-obv-tarama-1848717193069924795` — - `tweet-saatlik-ema-macd-rsi-obv-tarama-1848717193069924795` (2024-10-22; Tansu'nun X gönderisi). Görsel (açıldı): "Saatlik taramada son kapanış EMA5-10-20 MACD RSI14-50 VE OBV50 koşullarını sağlayıp AL sinyali veren hisseler:". Okuma (YORUM): GOODY saatlik liste örneğidir.
  - `tweet-saatlik-ema5-ema13-rsi21-tarama-1847262140693926109` — - `tweet-saatlik-ema5-ema13-rsi21-tarama-1847262140693926109` (2024-10-18; Tansu'nun X gönderisi). Görsel (açıldı): "DGGYO: Saatlik analizde EMA5 EMA13'ü yukarı kesti ve RSI21 50'nin üzerinde". Okuma (YORUM): günlük kurala saatlik veriyle örnektir.
  - `tweet-sabit-2-standart-sapma-asiri-bolge-1860462510752575670` — - `tweet-sabit-2-standart-sapma-asiri-bolge-1860462510752575670` (2024-11-23; Tansu'nun X gönderisi). Ham: "±2 standart sapma, normal ve outlier bölgeleri ayırarak trade fırsatlarını belirlemek için kullanılır." Okuma (YORUM): sabit sapma tercihi bu notun yaklaşımıdır.
  - `tweet-sar-yakinsama-trend-girisi-1951019812848804159` — - `tweet-sar-yakinsama-trend-girisi-1951019812848804159` (2025-07-31; Tansu'nun X gönderisi). Ham: "Sarlar da uygun yere gelince trene binerim". Okuma (YORUM; görsel açıldı): üç renk SAR noktası fiyata yaklaşır; uygun yerin sayısal tanımı çıkarılmaz.
  - `tweet-sharpe-eksi-040-tepki-momentum-alani-1905013305024122935` — - `tweet-sharpe-eksi-040-tepki-momentum-alani-1905013305024122935` (2025-03-26; Tansu'nun X gönderisi). Ham: "Bu kardeşimiz sharpe -0.40 ve -0.60 seviyesinden sürekli tepki almış farkında iseniz." / "henüz momentum alanında değil". Okuma (YORUM): örneğe özgü tepki gözlemidir.
  - `tweet-sharpe-orani-hisse-filtresi-1913512010253205811` — - `tweet-sharpe-orani-hisse-filtresi-1913512010253205811` (2025-04-19; Tansu'nun X gönderisi). Ham: "-0.40 civarından dönüş, yatırımın kötü bir dönemden çıkıyor olabileceğini gösterir." / "-0.60’tan dönüş, çok daha negatif bir zeminden toparlanma sinyalidir." Okuma (YORUM): tepki filtresidir; gerçekleşmiş kâr garantisi değildir.
  - `tweet-sharpe-sortino-beta-momentum-filtresi-1899200894513611035` — - `tweet-sharpe-sortino-beta-momentum-filtresi-1899200894513611035` (2025-03-10; Tansu'nun X gönderisi). Ham: "yüksek sharpe yüksek sortino ortalama alpha ve yüksek betalı momentum hissesi :)". Görsel (açıldı): "MIATK - Son İşlem Gününde Engulf Green Sinyali". Okuma (YORUM): yüksek beta tercihi bu momentum örneğine aittir.
  - `tweet-sharpe-tepki-marubozu-teyidi-1905493559790232063` — - `tweet-sharpe-tepki-marubozu-teyidi-1905493559790232063` (2025-03-28; Tansu'nun X gönderisi). Ham: "Şimdi bu kardeşimiz sharpe tepkisi vermiş aynı zamanda bir de son gün güzel bir marubozu yapmış:)". Okuma (YORUM): Sharpe tepkisi mumla teyit edilen örnektir.
  - `tweet-shooting-star-signal-scan-1898328312717418608` — - `tweet-shooting-star-signal-scan-1898328312717418608` (2025-03-08; Tansu'nun X gönderisi). Ham: "Arena 6 mart shooting star" / "7 Mart hoop aşağı :)". Okuma (YORUM): ARENA seçilmiş düşüş örneğidir; G2 açıldı, tarihsiz mum yakın görünümü sonuç zamanını tek başına doğrulamaz.
  - `tweet-skewness-rolling-63-cornish-fisher-var-2094166379607818736` — - `tweet-skewness-rolling-63-cornish-fisher-var-2094166379607818736` (2026-08-30; Tansu'nun X gönderisi). Ham, alıntılanan Tansu gönderisi: "Ben skewness'i tek başına AL/SAT sinyali olarak kullanmam." / "Volatilite, momentum, kurtosis ve tail-risk ile birlikte dağılım filtresi olarak kullanırım." / "63 günlük Rolling Skewness çıkarıyor". Okuma (YORUM): Gaussian ve Cornish-Fisher VaR kıyası risk dağılımı incelemesidir.
  - `tweet-sma-250-gun-ici-ret-1987815078452728229` — - `tweet-sma-250-gun-ici-ret-1987815078452728229` (2025-11-10; Tansu'nun X gönderisi). Ham: "250sma’dan intraday rejection". Okuma (YORUM): gün içi SMA250 reddi örneği, gün sonu stop kuralını değiştirmez.
  - `tweet-sma200-250-alti-kapanis-donus-alim-1989651383092744703` — - `tweet-sma200-250-alti-kapanis-donus-alim-1989651383092744703` (2025-11-15; Tansu'nun X gönderisi). Ham: "200 yada 250SMA altında iken kapanış, bir gün sonra üzerinde kapanıyor ise" / "momentum da yerinde ise bu iyi bir alım fırsatı yaratabilir." Okuma (YORUM): momentum şartı tanımsızdır; kaynak olasılık dili kullanır.
  - `tweet-stokastik-14-3-k-d-tarama-1897565005811183722` — Okuma (YORUM): Stokastik son satır sınıflandırması (G1 açıldı): “periods = 14”, “moving_av = 3”. K, kapanışın kayan düşük-yüksek aralığındaki yüzdesi; D, K'nın üç dönem ortalamasıdır. Güçlü AL koşulu: “if last_row["K"] > last_row["D"] and last_row["K"] < 20:”. Güçlü SAT koşulu: “elif last_row["K"] < last_row["D"] and last_row["K"] > 80:”. Diğer K>D durumunda AL, kalan durumda SAT yazılır. Okuma (YORUM): Kod son durum kıyaslar; önceki gün kesişimi aramaz.
  - `tweet-supertrend-atr7-carpan3-bant-kodu-1839989044693922032` — Okuma (YORUM): Supertrend bant kodu örneği (G1 açıldı). Görselde “range_period = 7” ve “multiplier = 3” yazılıdır. Okuma (YORUM): Bunlar bu kod örneğinin ayarlarıdır; bütün Supertrend taramalarının varsayılanı yapılmaz.
  - `tweet-supertrend-bullish-ema5-20-son-gun-1852057966960349695` — Okuma (YORUM): Aynı son günde iki koşul aranır. Ham: “Son gün supertrend bullish olan ve 5EMA 20EMA'yı yukarıya kesen hisse.” ve “Altını çizeyim her iki koşulda son gün sağlanıyor.”
  - `tweet-supertrend-bullish-taramasi-1843373717247922211` — Okuma (YORUM): Bullish Supertrend taramasının örneği. Ham: “Supertrend taraması bulllish tayfası”.
  - `tweet-supertrend-ema-5-20-kesisim-1851991078661976137` — Okuma (YORUM): Supertrend ile EMA kesişimlerini birlikte izleyen grafik örneği. Ham: “Supertrend ve EMA kesişimleri”. Görsel metni giriş ve çıkış işaretlerini gösterir; bu okuma yeni bir eşik getirmez.
  - `tweet-supertrend-ema5-20-tarama-1850640152747561291` — Okuma (YORUM): Supertrend ile EMA kombinasyonu için tarama geliştirme kaydı. Ham: “I just wrote the code to scan for SuperTrend and the 5-20 EMA combination.”
  - `tweet-supertrend-ema5-ema20-giris-1852010014329766290` — Okuma (YORUM): Ham “burada kısaca bunu kodladım dostlar” der. FINGRAD imzalı G2 açıldı. Long koşulları: “5 EMA crosses above 20 EMA” ve “Supertrend turns Green”. Short koşulları: “5 EMA crosses below 20 EMA” ve “Supertrend turns Red”. Okuma (YORUM): Short yönü kaynak anlatımıdır; mevcut sistemin yön kapsamını değiştirmez.
  - `tweet-supertrend-kama-al-sinyali-1853065056759550021` — Okuma (YORUM): Supertrend yönü ve KAMA sinyali birlikte taranır. Ham: “Supertrend yukarı trenddeyken son gün KAMA al sinyali veren hisseler:”. KERVT, MERKO, SANFM ve TDGYO örnek listesidir.
  - `tweet-supertrend-most-rsi-50-tarama-1839361483618320455` — Okuma (YORUM): Bir strateji sorusu olarak Supertrend–MOST bileşimi ve RSI geçişi. Ham: “Şimdi supertrend ile most oluşumu evotrend kodlasak, buna birde rsi 50 yi yukarı kesme şartı getirsek, tarattırsak nasıl olur?”
  - `tweet-supertrend-pozitif-hacim-cmf-1846135722635313326` — Okuma (YORUM): Henüz yazılması planlanan tarama birleşimi. Ham: “Akşam taramasını yazacağım kod:” ve “Supertrend+poz.volume + CMF”.
  - `tweet-supertrend-rsi-55-45-bist30-tarama-1860422703150149949` — Okuma (YORUM): Tansu kaynağı @mehmetemanet olarak belirtir: “@mehmetemanet abimin stratejisinin grafik çıktıs örneği.” G2 açıldı: “AL SİNYALLERİ (RSI > 55 ve Bullish)” ve “SAT SİNYALLERİ (RSI < 45 ve Bearish)”.
  - `tweet-supertrend-rsi-55-45-strateji-1860416194953543908` — Okuma (YORUM): @mehmetemanet stratejisinin parametre değişikliği anlatımı. Ham: “supertrend 10/3 al ve 3/10 at, rsı>55 al ve rsı<45 sat koşullarını içeren stratejisini” ve “Bende bu tarama vardı parametreleri değiştirdim abi.” Okuma (YORUM): “3/10 at” yazımı aynen korunur; düzeltilmez.
  - `tweet-supertrend-tarama-bullish-bearish-listesi-1840000258094354552` — Okuma (YORUM): Supertrend sınıfları ve kodu doğrulama çağrısı. Ham: “Bearish ayı, bullish boğa sinyalidir.” ve “Alın bu hisseleri, dün verdiğim supertrend kodunda deneyin, bakalım gerçekten kod doğru çalışıyor mu.”
  - `tweet-supertrend-tarama-rsi14-50-sart-1841917340419559794` — Okuma (YORUM): Supertrend adaylarına son gün RSI koşulu eklenir. Ham: “Hiç bir hisse son gün RSI14 > 50 şartını sağlamamaktadır.” ve “sadece yelpazenizi daraltmanıza yardımcı oluyorum.”
  - `tweet-t3-kesisim-belthold-sinyal-1995924034911961480` — Okuma (YORUM): T3 kesişimi ve Belt Hold birlikte gösterilir. Ham: “Gider mi?” G1 açıldı: “T3 Kesişimi (AL)” ve “Formasyon: CDLBELTHOLD”. Okuma (YORUM): Bu tek grafik gözlemidir; yeni evrensel giriş koşulu değildir.
  - `tweet-ema5-20-kesisim-supertrend-onceden-bullish-1852060552413221135` — Okuma (YORUM): Son gün EMA kesişimi ve önceden bullish SuperTrend ayrı zaman koşullarıdır. Ham: "EMA5 EMA20'yi son gün yukarı kesiyor ama supertrend zaten bullish yönünde." ve "Yani son gün bullish olmuyor." Bu varyant, iki koşulu aynı gün arayan örneğin yerine geçirilmez.
  - `tweet-heikin-ashi-yesil-kapanis-taramasi-1842916886100742272` — Okuma (YORUM): Heikin Ashi taramasının BIST30 örneği. Ham: "Son gün yeşil Heikin Ashi kapanışa sahip BIST30 hisselerİ:". Liste işlem sonucu değildir.
  - `tweet-heikin-ashi-yesil-kapanis-taramasi-1843758612780593259` — Okuma (YORUM): Son gün yeşil Heikin Ashi taraması ve hacim uyarısı. Ham: "BIST30 Heikin Ashi son gün yeşil kapatan hisseler" ve "Hacima rayın arkadaşlar". Yazımı korunan ikinci cümle sayısal hacim eşiği yapılmaz.

- Beta-hacim regresyonu (`tweet-beta-hacim-regresyon-tahmin-1941169284698587472` (2025-07-04); Ham): "Bağımlı değişken olarak hacmi, bağımsız değişken olarak ise beta katsayısını kullanabiliriz." "Beta, dinamik bir risk göstergesidir ve hiçbir zaman tek bir döneme ya da değere sabitlenmemelidir." Okuma (YORUM): araştırma önerisidir; işlem kararı için model, pencere ve tahmin eşiği ayrıca belirlenmelidir. Hazırlık X.
- Ons altında call duvarı (`tweet-call-duvari-hedef-cikis-2087613325425201290` (2026-08-12), `tweet-call-duvari-kirilimi-momentum-squeeze-2084870597385818320` (2026-08-05), `tweet-call-duvari-kirilimi-momentum-squeeze-2085043984414409205` (2026-08-05), `tweet-call-duvari-ustunde-tutunma-2085278210728599696` (2026-08-06); Ham; BIST evreni dışı): 05.08: "4251$ olan call duvarı yıkılırsa yeni bir momentum squezee gelebilir yani ivme güç kazanabilir." Aynı gün: "Sağlam yıkarsa momentum squeeze gündeme gelir ivme hız kazanır". 06.08: "4251 seviyesi üzerinde tutunursa call duvarının yukarı çekildiği anlaşılır." 12.08: "Altında hedefim 4631 call duvarı" ve "Oradan muhtemelen vedalaşırım". Okuma (YORUM): tarihli beklenti ve muhtemel çıkıştır; fiyatlar genel eşik değildir. Duvar hesabı ve tutunma ölçüsü uygulama öncesinde belirlenmelidir. Hazırlık X.
- Çanak örnekleri (`tweet-canak-boyun-cizgisi-ema-sirasi-1953926472432857585` (2025-08-08), `tweet-canak-formasyonu-degerleme-hedefi-1787051924061118650` (2024-05-05), `tweet-canak-rsi-pozitif-uyumsuzluk-1788294961269502000` (2024-05-08); Ham, CEMTS G1 açıldı): CEMTS için soru "Şu çanak işe yarar mı sizce?" Görsel: "Entry ~ 11.96", "Target 14.13", "Stop 9.69", "R:R ≈ 0.96", "EMA order: 10>20>50>100>200". TTRAK Ham: "haftalık çanak tamamlıyor." ERCB Ham: "Çanak oluşumu, RSI pozitif uyumsuzluk vs vs :)" ve "Hedef 211". Okuma (YORUM): ayrı hisselerin örnek seviyeleridir. R/R 0,96 kabul eşiği değildir; kulplu formasyonun §21 hesabı bu çanaklara otomatik taşınmaz. Hazırlık X.
- Delta hacim boğa oranı tarama fikri (`tweet-delta-hacim-boga-ayi-orani-1950279832119472221` (2025-07-29); Ham): "Buna şimdi bir de tarama yazarız boğalar %75 olsun deriz:)". Okuma (YORUM): yüzde 75 hedefi önerilen taramaya aittir; uygulanmış sistem olarak okunmaz. Oran hesabı ve tetikleme ayrıntıları uygulama öncesinde belirlenmelidir. Hazırlık X.
- Hacim, CMF ve ADX skoru (`tweet-hacim-cmf-adx-sinyal-skoru-tarama-1965629890100941012` (2025-09-10); G1 açıldı): "0.50 ÜSTÜNDE SİNYAL VEREN HİSSELER:", "HACİM 1.5x", "CMF ARTAN", "ADX>20". GSDDE satırında skor 0.728 görünür. Okuma (YORUM): skor eşiğiyle kontrol sütunları ayrı alanlardır; tüm kontroller zorunlu AND koşulu diye birleştirilmez. Skor formülü ve hacim karşılaştırmasının tabanı uygulama öncesinde belirlenmelidir. Diğer satırların beyazla örtülü alanları okunamıyor. Hazırlık X.
- Momentum alanı ve üç faz (`tweet-momentum-3-faz-breakout-volatilite-1866512347814142444` (2024-12-10), `tweet-momentum-alani-giris-cikis-1873650509388910642` (2024-12-30); Ham): "Phase1, momentum henüz breakout olanlar", "Phase 2, breakout olmuş ve dengeli yükselenler", "Phase 3, breakout olmuş yükselen ama volatilitesi yüksek." "Tüm çalışmalar günlük periyotta yapılıyor" ve "Giriş çıkış kararı yatırımcının". 30.12 yanıtı: "duruma göre. momentum alanından çıkarsa çıkılır alana girerse girilir". Okuma (YORUM): alanın sayısal sınırı ve faz sınıflandırıcısı uygulama öncesinde belirlenmelidir. Günlük faz etiketi tek başına otomatik emir değildir. Hazırlık X.
- Logit yön tahmini ve eşik örnekleri (`tweet-logit-pos-rel-bant-yon-modeli-1919017651617071315`, 2025-05-04; `tweet-lojistik-regresyon-sinyal-esigi-1775632307669385380`, 2024-04-03): POS_REL çalışması: "Kısaca kapanış fiyatının son 8, 16, 32 ve 64 günlük bantlar içindeki göreli konumunu (POS_REL) alıp" (Ham, 04.05.2025). KFEIN örneği: "Model, kesikli çizgiyi yukarı kesince yükselir diyor." (Ham, 03.04.2024). Okuma (YORUM): iki paylaşımın aynı model olduğu söylenmez. Eğitim hedefinin vadesi, POS_REL hesabı ve KFEIN eşiğinin sayısal tanımı uygulanabilirlik için açık kalır. Ham model yönünü anlatır, fiyat tahmini iddiasından ayırır. Günlük kapanışla model geliştirmek mümkündür (YORUM); kaynak modeli aynen kurmak için bilgi eksiktir. Hazırlık X.
- Bağlamı eksik lookback yanıtı (`tweet-lookback-parametresi-10-gun-1909770238800908454`, 2025-04-09): "şimdilik 10 gün ile ilgileniyorum:)" (Ham). Okuma (YORUM): hangi detektöre ait olduğu bilinmeyen bu pencere mevcut bir kurala aktarılmaz. Hazırlık X. Açık soru PR gövdesine taşınır.
- MACD/RSI teyidinden sonra bekleme (`tweet-macd-ok-rsi-50-ustu-1861815222433976516`, 2024-11-27): "rsı > 50" ve "bi dönsün gelsin dimi bakalım kuvvete primlenmiş 20 gündür" (Ham). Okuma (YORUM): hisse ve dönüş ölçütü belirtilmeyen yanıt, Bollinger koşulu içerdiği varsayılmadan korunur. Hazırlık X. Bağlam sorusu PR gövdesine taşınır.
- POSC uyumsuzluk örneği (`tweet-posc-wma5-wma17-momentum-uyumsuzluk-1760763224029360158`, 2024-02-22): "POSC'a baktığımızda ok ile işaretlenen alanlarda fiyatların iki tepe yaptığı ancak POSC tepelerinin aynı kaldığını rahatlıkla görebilirsiniz." ve "Bu hissede momentumun azaldığını gösterir." (Ham). Kod: "df_thyao['POSC'] = df_thyao['WMA5'] - df_thyao['WMA17']" (G1, açıldı). Okuma (YORUM): THYAO örneğinde kapanış WMA5 ile WMA17 farkı çizilir; kodun WMA fonksiyon satırı sağda kesiktir. Tepe seçimi ve eşitlik toleransı tanımlanmadan otomatik uyumsuzluk kuralı kurulmaz. Hazırlık K.
- PSAR panellerine ek teyit önerisi (`tweet-psar-adx-adxr-filtre-1862630588584214682`, 2024-11-29): "momentum ve volume de koyalım üzerine bir de fibo çektik mi mis olur" (Ham). Okuma (YORUM): PSAR ve ADX/ADXR panellerine ek gösterge önerisidir; çizilmiş panellerden zorunlu giriş eşitliği kurulmaz. Hazırlık X.
- Williams %R ve MACD araştırma seçenekleri (`tweet-r-70-yukari-kesis-macd-sinyal-1845033474538786861` (2024-10-12)): “Biraz beyin fırtınası yapalım” ve “Bence R diplerde iken macd sinyali çizgisini keserse daha hoş olur” (Ham). Okuma (YORUM): -70 yukarı kesişimiyle MACD teyidi veya aşırı satımdayken MACD kesişimi tartışılır; tek kesinleşmiş kural değildir. BTC-USD görseli BIST dışı örnektir. Hazırlık X.
- Rolling Sharpe tepki örnekleri (`tweet-rolling-sharpe-esik-tepkisi-1905014767422468528` (2025-03-26), `tweet-rolling-sharpe-esik-tepkisi-1905152595586318386` (2025-03-27), `tweet-rolling-sharpe-esik-tepkisi-1905219676352676212` (2025-03-27)): “Rolling Sharpe (21 gün)” ve “-0.40 Seviyesi” (26–27.03 görselleri açıldı). ICUGS: “Prev Sharpe = -0.5398, Last Sharpe = -0.3911”. METRO: “-0.6 Seviyesi” (görsel açıldı). Okuma (YORUM): örnekler ayrı referans seviyeleri taşır; tek evrensel eşik olmaz. METRO Ham “25 mart tarihli tarama”, görsel tepki tarihini 24 Mart olarak verir; ikisi aynı tarih alanı sayılmaz. Ham “26'sında %5 verdi” der; seçilmiş sonuç beyanıdır. Sharpe hesabı, risksiz oran ve çıkış kuralı açıklaştırılmalıdır. Hazırlık K.
- RSI kod çizim örnekleri (`tweet-rsi-14-python-kodu-30-70-esik-1852790563738996916` (2024-11-02), `tweet-rsi-20-cufflinks-quantfig-kod-1860287702844817681` (2024-11-23), `tweet-rsi-20-yukselis-dusus-ortalamasi-kod-1860318349797814519` (2024-11-23)): Altın kodu: “df['RSI'] = ta.rsi(df['close'], length=14)” (görsel açıldı). DOAS: “qf.add_rsi(periods=20, rsi_upper=70, rsi_lower=30)” (görsel açıldı). XU100: “period = 20” (görsel açıldı). Okuma (YORUM): XU100 kodu pozitif/negatif günlük farkların 20 dönem basit ortalamasıyla RSI üretir; Wilder ortalaması varsayılmaz. 30/70 çizgileri gösterim referansıdır; çizim kodu kendi başına işlem yürütmez. Altın BIST dışı örnektir. Hazırlık K.
- RSI50 kesişim tercihi (`tweet-rsi-50-yukari-kesisim-1840500851498004798` (2024-09-29)): “Rsı 50 üzeri kesişmi alıyorum” (Ham). Okuma (YORUM): yanıt kendi parametrelerinin karşı tarafla farklı olduğunu söyler. RSI periyodu veya ek teyit bu cümleden türetilmez. Hazırlık X.
- Trend yönünde yüksek RSI yorumu (`tweet-rsi-80-trendde-asiri-alim-degil-1761751571916857810` (2024-02-25)): “Eğer trend yönünde iseniz RSI 80 üzerine çıkması aşırı alım olarak yorumlanmamalı.” ve “Bu nedenle indikatör sepetinizde trend takip edici, momentum ve hacim göstergeleri olmalı.” (Ham). Okuma (YORUM): yüksek RSI tek başına satış emri değildir. Notun BTC-USD örneği BIST dışıdır; mevcut RSI30/70 tarama eşiği değiştirilmez. Hazırlık K.
- Gecikmeli WMA formül örnekleri (`tweet-wma-gecikmeli-ref-mov-formul-1750523598119592101` (2024-01-25)): “9 günlük WMA için 8 gün gecikme: Ref(Mov(C,9,W),-8)” ve “14 günlük WMA için 8 gün gecikme: Ref(Mov(C,14,W),-8)” (Ham). Okuma (YORUM): gösterge hesabı örnekleridir, giriş veya çıkış tetiklemez. Hazırlık K.
- Yüzdelik dilimle yön tayini (`tweet-yuzdelik-dilim-yon-tayini-2089812316619497553` (2026-08-18)): “Sistem, belirli bir geçmiş veri penceresindeki yüzdelik dilimleri hesaplayarak modelden bağımsız bir yön tayini yapar.” (Ham). Okuma (YORUM): pencere uzunluğu, yüzdelikler ve yön eşleme hesabı seçilemez. Hazırlık X.


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
  - `tweet-death-cross-ema50-ema200-1911462470763360258` — Ölüm kesişimi (death cross) tanımı Tansu'nun kendi gönderisinde: "Death Cross = EMA 50 çizgisinin, EMA 200 çizgisinin altına düşmesi" (Ham). Yorum: yatırımcı pozisyon kapatabilir, yeni alımdan kaçınabilir; "Tek başına bir sinyal her zaman yeterli değildir." (Ham). Sembol, periyot, stop düzeyi, hedef ve sonuç yok; çift EMA (SMA değil). Parametre: Death cross çifti = EMA50, EMA200'ün altına keser (periyot belirtilmemiş; Ham)
  - `tweet-ema-50-200-maliyetli-backtest-1837452465022615616` — TUPRS için 50/200 EMA (SMA değil) stratejisi kodu işlem maliyetiyle: "işlem maliyeti ilaveli, optimizasyonu artık kendiniz yaparsınız :). (0.001 işlem maliyeti eklenmiştir)" (Ham). Görsel (görsel metni): 2022 için creturns, cstrategy ve cstrategy_net eğrileri (sayı yok). Optimizasyon: karar Levent'te bekliyor (E K29). Ham: "You cannot beat the market!" görüş, kural değil. Parametre: İşlem maliyeti = 0,001 (Ham: "0.001 işlem maliyeti eklenmiştir"); tek yön mü gidiş-dönüş mü, pozisyon değişiminde mi uygulanır belirsiz (YORUM)
  - `tweet-ma-kesisim-var-opt1-opt2-optimizasyon-1784690075059585046` — DOAS 60DK VAR kesişimi: "Cross(MOV(C,opt1,VAR),MOV(C,opt2,VAR))" ve "Cross(MOV(C,opt2,VAR),MOV(C,opt1,VAR))" (Ham, 28.04.2024). Okuma (YORUM): VAR ortalaması ayrı örnektir; SMA kuralının türünü değiştirmez.
  - `tweet-momentum-listesi-golden-cross-1908440134174843000` — `tweet-momentum-listesi-golden-cross-1908440134174843000` (2025-04-05, Ham): "Bu hafta momentum listemizde olan #link golden cross ile hisseyi alanı para altına bırakacak umarız:)"
  - `tweet-sma-10-100-kesisim-pine-kodu-1771510245702914481` — - `tweet-sma-10-100-kesisim-pine-kodu-1771510245702914481` (2024-03-23; Tansu'nun X gönderisi). G2 (açıldı): "buySignal = ta.crossover(fastMA, slowMA)" / "sellSignal = ta.crossunder(fastMA, slowMA)". Okuma (YORUM): kapanış SMA’ları için hızlı varsayılan 10, yavaş varsayılan 100; bunlar örneğin ayarlarıdır.
  - `tweet-sma-10-20-30-ortalama-seti-1762835969265344535` — - `tweet-sma-10-20-30-ortalama-seti-1762835969265344535` (2024-02-28; Tansu'nun X gönderisi). Görsel (açıldı): "SMA 10" / "SMA 20" / "SMA 30". Okuma (YORUM): TUPRS hareketli ortalama çizim setidir; tek başına kesişim giriş kuralı tanımlamaz.
  - `tweet-sma-5-25-kesisim-parametreleri-1764294925791777136` — - `tweet-sma-5-25-kesisim-parametreleri-1764294925791777136` (2024-03-03; Tansu'nun X gönderisi). Ham: "benim parametrelerim 5 günlük ve 25 günlük basit hareketli ortalamalar üzerine kurulu." / "Sizler n1 ve n2 parametrelerini değiştirerek daha iyi getirilere ulaşabilirsiniz." Okuma (YORUM): bu kaynakta örnek set 5/25’tir; genel varsayılan değiştirilmez.
  - `tweet-ema50-200-golden-cross-kodu-1846531506396651996` — `tweet-ema50-200-golden-cross-kodu-1846531506396651996` (2024-10-16): EMA50/EMA200 kodu için uyarı: "EMA50 ve 200 kesişimleri geç sinyal üretebilir" (Ham). Kod: "df['Position'] = df['Signal'].diff()" (G1, açıldı). Okuma (YORUM): kapanışın EMA50/EMA200 değerleri adjust=False ile hesaplanır; EMA50 > EMA200 durumunun farkı +1 alış ve -1 satış işareti verir. GC=F kod örneğidir; SMA kuralını değiştirmez.
  - `tweet-ema50-200-kesisim-al-sat-sinyali-1847338202924744724` — `tweet-ema50-200-kesisim-al-sat-sinyali-1847338202924744724` (2024-10-18): GLCVY örneği: "EMA Crossover (50-200)", "BUY SIGNAL", "SELL SIGNAL" (G1, açıldı). Okuma (YORUM): farklı tarih pencerelerinin tabloları tek işlem dizisi olarak birleştirilmez.
  - `tweet-ema50-ema200-death-cross-1943065231695188060` — `tweet-ema50-ema200-death-cross-1943065231695188060` (2025-07-09): KRGYO örneği: "KRGYO.IS - Death Cross", "EMA 50", "EMA 200" (G1, açıldı). Okuma (YORUM): bu tarihli görüntü gelecek kaybın ölçümü değildir.
  - `tweet-ema50-ema200-golden-cross-1848805888355652024` — `tweet-ema50-ema200-golden-cross-1848805888355652024` (2024-10-22): "Son gün Golden Cross AL sinyali veren hisseler (EMA50 > EMA200):" (Ham). DNISI aynı gönderinin sonucudur.
  - `tweet-ema50-ema200-golden-cross-1929962891026850004` — `tweet-ema50-ema200-golden-cross-1929962891026850004` (2025-06-03): "Önce bir golden cross verelim." (Ham). "ECILC.IS - Golden Cross", "EMA 50", "EMA 200" (G1, açıldı).
  - `tweet-ema50-ema200-golden-cross-1943065073590899051` — `tweet-ema50-ema200-golden-cross-1943065073590899051` (2025-07-09): "GOLDEN CROSS" (Ham). "TSKB.IS - Golden Cross", "EMA 50", "EMA 200" (G1, açıldı).
  - `tweet-ema50-ema200-golden-cross-tarama-1842243313891516527` — `tweet-ema50-ema200-golden-cross-tarama-1842243313891516527` (2024-10-04): "50EMA/200EMA Golden Cross arıyorum." ve "Fiyat 200 günlük EMA'ya temas etmiş, geçerse bakacağız." (Ham). Okuma (YORUM): fiyatın EMA200 teması ve iki EMA kesişimi ayrı olaylardır.
  - `tweet-ema50-ema200-golden-cross-taramasi-1844070126406250885` — `tweet-ema50-ema200-golden-cross-taramasi-1844070126406250885` (2024-10-09): "BMSCH.IS hissesi EMA 50, EMA 200'ü 2 gün önce yukarı kesti." (G1, açıldı). Okuma (YORUM): iki gün örneğin kesişim yaşıdır.
  - `tweet-ema50-ema200-golden-cross-taramasi-1844838137366806837` — `tweet-ema50-ema200-golden-cross-taramasi-1844838137366806837` (2024-10-11): "GLRYH.IS hissesi EMA 50, EMA 200'ü 1 gün önce yukarı kesti." (G1, açıldı). Ham veri uyarısı: "KGYO ve INVEO veri gelmedi". Okuma (YORUM): eksik veriyle uyarı, doğrulanmış fiyat verisi değildir.
  - `tweet-ema50-ema200-olum-kesisimi-1923093966376816754` — `tweet-ema50-ema200-olum-kesisimi-1923093966376816754` (2025-05-15): "SELEC.IS - Death Cross", "EMA 50", "EMA 200" (G1, açıldı). Okuma (YORUM): aşağı kesişim örneğidir.

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bollinger-trend-momentum-di-teyit-1775396085038469494` — Yanıt (@volcano8470, 03.04.2024): Bollinger yalnız trend piyasada iyi sinyal verir; "Üst bant momentum indikatörü ve +-DI ile beraber takip edilirse, BB güvenilirdir." Yatay piyasada "band sıkışır tadı tuzu olmaz" (Ham). Rejim filtresi: BB sinyali trendde, momentum ve ±DI teyidiyle; eşik ve periyot yok. YORUM: yatay piyasadaki sıkışma §40 ve §45'teki sıkışma durumudur.
  - `tweet-adx-bbw-yatay-piyasa-filtresi-2004287128214356186` — Okuma (YORUM): ADX düşük ve BBW dar olduğunda işlem açmama filtresi önerilir. Ham: "ADX 20 seviyesinin altına indiğinde trendin gücünü yitirdiğini" ve "BBW değeri ise son 100 barın en düşük %20’lik dilimine (rolling percentile) girdiğinde piyasanın iyice daraldığını anlarız."
  - `tweet-yfinance-bist-veri-cekme-1761491655159394358` — `tweet-yfinance-bist-veri-cekme-1761491655159394358` (2024-02-24). ADX/ADXR ayrımı: "ADX, ADXR'nin üzerinde iken trend vardır altında iken trend yoktur." ve "ADX'in, ADXR'yi aşağıya kesmesi mevcut trendin sona erdiğine işaret edebilir." (Ham). Bollinger örneği: "Bu bandın standart sapması 2'dir." (Ham).

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bollinger-uc-sapma-saatlik-al-1845929388904444018` — DOCO saatlik örneği (14.10.2024): "3SS BB al verdi." (Ham). Görsel başlığı "DOCO.IS AL sinyali verdi." (görsel metni); grafik fiyat ve BB üst, orta, alt çizgileri, 7-14 Ekim 2024. 3 SS kuralının saatlik uygulaması; mum koşulu ve eşik yazılı değil. Saatlik veri günlük bedava veride yok.
  - `tweet-bollinger-ust-bant-ortalamaya-donus-1778707323147448589` — DOAS ortalamaya dönüş beklentisi (12.04.2024): üst banda varan sert yükselişten sonra kırmızı son mum; "Bence haftaya ortalamasına geri çekilmek isteyecek." (Ham). Ham: "BB ve 3SS ile 20EMA"; hedef bölge "317-318". Görselde (açıldı) beyaz orta çizgi sağ kenarda yaklaşık 318'dedir (ölçüm, YORUM: hedef = orta çizgi). Hedefin sayısı hisseye özgüdür; zaman ufku yaklaşık bir hafta (YORUM). Parametre: Orta çizgi türü = 20 EMA (Ham: "BB ve 3SS ile 20EMA"; bölümdeki SMA20 ile farklı, YORUM); geri çekilme hedefi = orta çizgi, DOAS'ta 317-318 (Ham)
  - `tweet-gunluk-3ss-bb-alt-bant-igne-1846989330382041324` — Okuma (YORUM): Günlük alt bant iğnesi ve sonraki yeşil kapanış koşulu. Ham: "Günlükte, 3SS BB bir önceki gün alt banda iğne atıp son gün yeşil kapatsın."
  - `tweet-saatlik-bollinger-3ss-igneli-mum-1848275501737030095` — - `tweet-saatlik-bollinger-3ss-igneli-mum-1848275501737030095` (2024-10-21; Tansu'nun X gönderisi). G1 (açıldı): "OZSUB.IS AL sinyali verdi (3SS'li Bollinger Bandı ve Zıt Mumlu İğneli Mum)." Okuma (YORUM): saatlik tarama örneğidir.
  - `tweet-saatlik-bollinger-3ss-igneli-mum-1848290587960598690` — - `tweet-saatlik-bollinger-3ss-igneli-mum-1848290587960598690` (2024-10-21; Tansu'nun X gönderisi). Görsel (açıldı): "Saatlil 3SS Bollinger Bandı zıt mumlu ve İğneli Mum stratejisinde AL sinyali veren hisseler:". Okuma (YORUM): saatlik liste örneğidir.

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bollinger-orta-bant-rsi50-al-sat-1774426858567643590` — DOAS kodlama önerisi (31.03.2024): al = fiyat orta bandı yukarı keser ve RSI 50'yi yukarı keser; sat = orta bandı aşağı keser; üst ve alt bant kaldırıldı. "orta bandı aşağı kestiğinde sat sinyali üret" (Ham). Bölümde çıkış yoktu: bu, çıkış kuralıdır. Görsel başlığı "DOAS.IS için Optimize Edilmiş Bollinger Bantları ve Al/Sat Sinyalleri" (görsel metni): hisse bazlı optimizasyon izi, değer yok; karar Levent'te bekliyor. Parametre: Çıkış (sat) = fiyat BB orta bandını aşağı keser; RSI koşulu yok (Ham)
  - `tweet-bollinger-orta-bant-rsi50-kesisim-1840361825134678149` — PENGD tarama çıktısı (29.09.2024), 10.01.2025 taramasının MACD'siz önceki sürümü gibi okunur (YORUM). "PENGD için son kapanış gününde RSI kesişimi: True" ve "Bollinger Orta Bandı Kesişimi: True" (görsel, açıldı). RSI 50 kesişimi seviye değil kesişim olarak çizilir (kırmızı nokta, son bar RSI yaklaşık 52; ölçüm, YORUM) ve kapanış orta bandın hemen üstündedir. Ham: "Arkadaşların aklında olsun enteresan olabilir". Parametre: Tarama koşulu (29.09.2024) = son kapanışta BB orta bandı yukarı kesişimi ve RSI 50 yukarı kesişimi; MACD yok; grafik penceresi 100 bar (görsel, açıldı)
  - `tweet-bollinger-rsi-50-tarama-1864543445295014396` — Tekrar, 09.01.2025 duyurusundan önce (05.12.2024): "Aşağıda Bollinger Bantları ve RSI>50 taramasını yolluyorum." (Ham). Koşul ayrıntısı yok, kod dış bağlantıda (açılmadı). Yeni olan öğüt: taramayı "daha önce verdiğim taramalar ile" birleştirip yeni tarama kurmak (Ham).
  - `tweet-orta-bant-ustu-kapanis-rsi-50-kesis-1786781640338886970` — `tweet-orta-bant-ustu-kapanis-rsi-50-kesis-1786781640338886970` (2024-05-04): Ham: "Mum orta band üstünde kapatmış ve rsı 50 kesmişse (makul oranda) genelde güzel sonuç verebiliyor. Tabi bunlar hep öngörü".
  - `tweet-rsi-50-bb-orta-bant-kesisimi-1782493259874365466` — - `tweet-rsi-50-bb-orta-bant-kesisimi-1782493259874365466` (2024-04-22; Ham): SMART örneği (Ham): "RSI 50'yi keserken BB orta bandın üzerine atmak üzereydi." Kanıt sınırı: "Wolk forward ve monte carlo simülasyonu yapmadığım için sizlerle paylaşmadım." Okuma (YORUM): beklenti durumu ile tamamlanmış orta bant kırılımı ayrıdır.
  - `tweet-rsi-50-bb-orta-bant-tarama-1782868378304008586` — - `tweet-rsi-50-bb-orta-bant-tarama-1782868378304008586` (2024-04-23; Ham): Tarama önerisi (Ham): "RSI'ın 50'yi ve BB'nin orta bandının henüz geçildiği bir tarama formülünü kim yazacak?"
  - `tweet-rsi-50-di-teyit-1782883737518088465` — - `tweet-rsi-50-di-teyit-1782883737518088465` (2024-04-23; Ham): Ek teyit (Ham): "RSI zaten 50'yi kestiğinde momentum ciddi artmıştır." "+-DI ile teyit alabilirsiniz". Okuma (YORUM): DI teyidi isteğe bağlı öneridir.
  - `tweet-rsi-bb-most-ema-kesisim-tarama-1782874367963087358` — - `tweet-rsi-bb-most-ema-kesisim-tarama-1782874367963087358` (2024-04-23; Ham): AKCNS örneği (Ham): "RSI ve BB orta bandı son kapanışla kesilmiş, MOST al vermiş". Beklenti: "Yarın 20 günlük EMA'nın 50 günlük EMA'yı keseceğini öngörüyorum sonra trene binilir." Okuma (YORUM): EMA kesişimi gerçekleşmiş değil, öngörüdür.
  - `tweet-rsi50-bb-orta-bant-kesisimi-1840357016855773216` — - `tweet-rsi50-bb-orta-bant-kesisimi-1840357016855773216` (2024-09-29; Tansu'nun X gönderisi). DOAS (Ham): "RSI >50 (yukarıya kesmiş)" / "Fiyat>BB orta bandı (yukarıya kesmiş)" / "Ama henüz upertrend ve most al vermemiş."
  - `tweet-rsi50-bb-orta-bant-kesisimi-1840357996397736167` — - `tweet-rsi50-bb-orta-bant-kesisimi-1840357996397736167` (2024-09-29; Tansu'nun X gönderisi). PENGD (Ham): "RSI>50" / "FİYAT>BB Orta Bandı". Okuma (YORUM): görsel metni son kapanıştaki kesişimleri doğrulayan tarama çıktısıdır.
  - `tweet-saatlik-macd-rsi21-bb-orta-bant-tarama-1848638106615869610` — - `tweet-saatlik-macd-rsi21-bb-orta-bant-tarama-1848638106615869610` (2024-10-22; Tansu'nun X gönderisi). Görsel (açıldı): "Saatlik MACD RSI21 50 şartı ve BB orta bandı yukarı kesme şartlarını sağlayan hisseler:". Okuma (YORUM): NTGAZ, OFSYM, SODSN ve TKNSA saatlik örnekleridir.
  - `tweet-saatlik-macd-rsi21-bollinger-3ss-sinyal-1848711615589359954` — - `tweet-saatlik-macd-rsi21-bollinger-3ss-sinyal-1848711615589359954` (2024-10-22; Tansu'nun X gönderisi). Görsel (açıldı): "Saatlik MACD RSI21 50 şartı ve BB orta bandı yukarı kesme şartlarını sağlayan hisseler:". Okuma (YORUM): BARMA, HURGZ, INVES, ISFIN ve METRO saatlik örnekleridir.
  - `tweet-sma20-rsi50-kesisim-tarayici-1782890207605387413` — - `tweet-sma20-rsi50-kesisim-tarayici-1782890207605387413` (2024-04-23; Tansu'nun X gönderisi). Ham: "BB orta bandı ve RSI14 50 kesmesi stratejisini sayılara dökmüş." Okuma (YORUM): @Emrahgulez’in hazırladığı tarama sonucunun Tansu tarafından paylaşılmasıdır.
  - `tweet-macd-al-bb-orta-rsi50-tarama-1840365704987492673` — `tweet-macd-al-bb-orta-rsi50-tarama-1840365704987492673` (2024-09-29): Üç koşul önerisi: "MACD son gün al versin", "Fiyat > BB, orta bandı olsun", "RSI > 50 olsun" (Ham, 29.09.2024). Okuma (YORUM): bu birleşim BB/RSI aynı-bar kesişim kuralına yeni zorunluluk eklemez.
  - `tweet-macd-al-bb-orta-rsi50-tarama-1840488342929969637` — `tweet-macd-al-bb-orta-rsi50-tarama-1840488342929969637` (2024-09-29): Son gün birleşimi: "MACD Son gün al versin", "RSI > 50 olsun (son gün)", "Fiyat > BB bandının ortası (son gün)" (Ham, 29.09.2024). Tarihli uyarı: "TDGYO'dan uzak durun. Gruplar cirit atıyor tahtada." Okuma (YORUM): bu uyarı kalıcı evren dışlama kuralına çevrilmez.
  - `tweet-macd-rsi21-50-bb-orta-bant-kesme-1848243880627445782` — `tweet-macd-rsi21-50-bb-orta-bant-kesme-1848243880627445782` (2024-10-21): Saatlik varyant başlığı: "Saatlik MACD RSI21 50 şartı ve BB orta bandı yukarı kesme şartlarını sağlayan hisseler:" (GÖRSEL G1, açıldı, 21.10.2024). Okuma (YORUM): günlük sürümden ayrı zaman dilimi örneğidir; aynı ekrandaki 3SS zıt/iğneli mum bildirimleri ayrı taramalardır.
  - `tweet-macd-rsi21-bb-orta-bant-1847177852409557456` — `tweet-macd-rsi21-bb-orta-bant-1847177852409557456` (2024-10-18): Alıntılanan gönderi: "Son gün MACD al versin", "RSI251 > 50 olsun", "BB Orta bandı yukarı kessin" (Ham, 18.10.2024). Okuma (YORUM): RSI251 yazımı aynen korunur; başlıktaki RSI21 ile sessizce eşitlenmez.
  - `tweet-macd-rsi21-bb-orta-bant-kesisim-1846997572004528150` — `tweet-macd-rsi21-bb-orta-bant-kesisim-1846997572004528150` (2024-10-17): Ham koşulları: "Son gün MACD al versin", "RSI251 > 50 olsun", "BB Orta bandı yukarı kessin" (17.10.2024). GÖRSEL G1 (açıldı) başlığı: "RSI 21 Indicator". Okuma (YORUM): Ham ile görselde RSI periyodu farklı yazılmıştır; mevcut kural bu farktan hareketle değiştirilmez.
  - `tweet-macd-rsi21-bb-orta-bant-kesisim-1847332125550219621` — `tweet-macd-rsi21-bb-orta-bant-kesisim-1847332125550219621` (2024-10-18): Günlük koşullar: "MACD  son gün yukarı kesiyor", "RSI21 > 50", "BB Orta Bandı Yukarı Kesme Şartını sağlayan hisseler" (Ham, 18.10.2024). Okuma (YORUM): RSI üstünde olma koşuludur; RSI aynı gün 50 kesişimi şartına dönüştürülmez.

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-coklu-dip-donus-teyit-listesi-1995931145499017316` — Dipten dönüş teyit listesi (02.12.2025, yanıt, sembol yok): "CDBelthold mum formasyonu" ve "RSI düşeni kırmış" ile birlikte "CCI Pozitif uyumsuzluk", "MACD güzel yerden kesmeyue hazırlanıyor", "Hacim artmış", "T3 kesişimi var" (Ham). Bölümdeki iki koşula dört ek teyit eklenir; hepsi eşiksiz. Görselde (açıldı; Matriks) düşen fiyat dipleri karşısında yükselen osilatör dipleri ve RSI panelinde düşen trend çizgisinin son barda yukarı kırılışı görünür; osilatör adları yazılı değil (YORUM).
  - `tweet-rsi-duk-lookback-50-extend-40-min-gap-20-1909110157600051269` — - `tweet-rsi-duk-lookback-50-extend-40-min-gap-20-1909110157600051269` (2025-04-07; Ham): MERCN örneği (Ham): "Doğru parametreler çok işe yarıyor RSI DÜK"; "lookback = 50"; "extend = 40"; "min_gap = 20". Okuma (YORUM): verilen örnek parametreleridir; diğer hisselere evrensel ayar olarak taşınmaz. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilim-taramasi-1909606120777298030` — - `tweet-rsi-dusen-trend-kirilim-taramasi-1909606120777298030` (2025-04-08; Ham): Ham: "RSI DÜK tarama" ve "+3.25". Okuma (YORUM): MACKO örnek sonuç paylaşımıdır; sayıdaki getiri bazını genel kurala çevirmeyiz. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilim-taramasi-1909613017186119809` — - `tweet-rsi-dusen-trend-kirilim-taramasi-1909613017186119809` (2025-04-08; Ham): Ham: "Tavan" ve "RSI DÜK". Okuma (YORUM): OZSUB örnek sonuç paylaşımıdır; bütün taramalar için başarı oranı değildir. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilimi-1908933806221914328` — - `tweet-rsi-dusen-trend-kirilimi-1908933806221914328` (2025-04-06; Ham): Ham: "Şimdilik iş görür"; "Geliştirmeye devam elbette."; "RSI Düşeni kıran". Okuma (YORUM): FROTO çizimi geliştirme aşamasındaki tarama örneğidir. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilimi-1908998879888003335` — - `tweet-rsi-dusen-trend-kirilimi-1908998879888003335` (2025-04-06; Ham): Ham: "Sorumluluk kabul etmem Denemeler yapıyorum". Okuma (YORUM): ISFIN çizimleri deneme örnekleridir; doğrulanmış işlem sistemi iddiası taşımaz. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilimi-1909102230197674157` — - `tweet-rsi-dusen-trend-kirilimi-1909102230197674157` (2025-04-07; Ham): Ham: "Daha sade"; "RSI DÜK kırılımı da büyük oranda tamamlanıyor." Okuma (YORUM): DOAS örnekleri aracın geliştirme durumunu gösterir. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilimi-1909104373835190300` — - `tweet-rsi-dusen-trend-kirilimi-1909104373835190300` (2025-04-07; Ham): Ham: "Tamamdır:)". Okuma (YORUM): DOAS RSI düşen trend çizimi tamamlanma paylaşımıdır; yeni parametre olarak kullanılmaz. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilimi-1909665614144077990` — - `tweet-rsi-dusen-trend-kirilimi-1909665614144077990` (2025-04-08; Ham): Ham: "Arkadaşımız kırmış:)". Okuma (YORUM): RSI trend kırılımı örnek grafiğidir; bağımsız başarı kanıtı değildir. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.
  - `tweet-rsi-dusen-trend-kirilimi-1909697746316960218` — - `tweet-rsi-dusen-trend-kirilimi-1909697746316960218` (2025-04-08; Ham): Ham: "Ne dersiniz?". Okuma (YORUM): RSI trend kırılımı çizimleri için görüş isteyen örnek paylaşımıdır. Okuma (YORUM): bu not yalnız RSI trend çizgisi bileşenine ek kaynaktır; BELTHOLD koşulunu kaldırmaz.

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
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-bullish-mum-rsi14-50-ema-filtre-1853110872819773819` — Somut mum filtresi planı (03.11.2024): "Bulşish Mum formasyonları taraması sadece RSİ14>50 olduğu zaman ve istediğimiz ema üzerinde iken al sinyali verecek." (Ham). §43 uyarısının tarama biçimi: boğa mumu + RSI(14) > 50 + fiyat EMA üstünde. Tansu: "Kafamda projesi hazır, iş kodlamaya kaldı" (Ham); kod ve çıktı yok. Parametre: Boğa mum sinyali filtresi = RSI(14) > 50 (seviye) ve fiyat > seçilecek EMA; EMA periyodu yok ("istediğimiz ema") (Ham)
  - `tweet-mum-formasyonu-taramasi-trend-onayi-1842853184684900746` — `tweet-mum-formasyonu-taramasi-trend-onayi-1842853184684900746` (2024-10-06): Ham: "hammer bull gelmiş. Ancak trendin biraz kafasını kaldırması lazım." Okuma (YORUM): EGEEN örneğinde mum sinyaline ek trend teyidi aranır.
  - `tweet-mum-formasyonu-trend-dogrulama-1842836702785642675` — `tweet-mum-formasyonu-trend-dogrulama-1842836702785642675` (2024-10-06): Ham: "Artık bütün mum formasyonlarını saatlik grafikte tek tık ile görebileceğiz:)"; "Üstelik trend doğrulama da cabası". Okuma (YORUM): TUPRS saatlik grafik uygulamasıdır.
  - `tweet-mum-formasyonu-trend-teyidi-1845375300227547618` — `tweet-mum-formasyonu-trend-teyidi-1845375300227547618` (2024-10-13): Ham: "Şimdi ECILC için boğa mum formasyonu çıkmış ama trende de bak be kardeşim hemen alma bu hisseyi yani."
  - `tweet-talib-mum-formasyonu-taramasi-1847991564057927802` — Okuma (YORUM): Mum etiketini trend bağlamında inceleme uyarısı. Ham: “Herkes kendisi inceler, malum düşen ve yükselen trendde farklı anlam alabiliyorlar.”

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
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-bollinger-keltner-squeeze-breakout-1913989895674028279` — 20.04.2025 gönderisi algoritma uygulaması ve ek teyit önerisini destekler (Ham): "Stratejiyi farklı göstergelerle (hacim, RSI, MACD gibi) destekleyerek çok daha isabetli hale getirmek de mümkün." Okuma (YORUM): Tek hisselik tarama açıklaması sonuç kanıtı değildir; mevcut sıkışma kuralına yeni ayar eklemez.

## 46. BULL/BEAR etiketleri: günlük sinyalin 5 günlük toplamı (+3 boğa, -4 panik; FROTO)

- Kaynak: `tweet-bull-bear-5-gunluk-toplam-sinyal-2042901081785557425` (FROTO, 11.04.2026; Ham ve görsel, açıldı). Tansu'nun X gönderisidir (birinci el). Ham metni yapay zekâ çıktısı gibi okunur (YORUM); Ham olarak birinci el sayılır.
- Tansu'nun ifadesi (verbatim):
  - Ham: BULL etiketi, alt paneldeki gri çizginin (5 günlük toplam sinyal) "+3 seviyesine veya üzerine çıktığı anlarda beliriyor"; BEAR etiketi "-4 veya -5 seviyesine kadar düştüğü yerlerde ortaya çıkıyor".
  - Ham: "Böyle dönemlerde yeni bir pozisyon açmak yerine, kırılımın (yukarı veya aşağı) netleşmesini beklemek genellikle en güvenli stratejidir."
  - Ham (rolling pencere): "son rolling periyodumuzun günün en yüksek seviyesini aşamamış, ancak en düşük seviyesinin altına da inmemiş".
  - Görsel başlığı (görsel metni; sol kısım karartılmış): `FROTO.IS · ... Son: 10.04.2026 | Kapanış=105.30 | Sinyal=+0 | 5g Toplam=-1`; etiketler `BULL`, `BEAR`.
- Tanım (YORUM; Ham ve görsel, açıldı):
  1. Günlük sinyal s(t) üç değer alır: -1, 0, +1 (alt panelde turkuaz +1 ve kırmızı -1 kısa çizgileri, ±0,5'te ince noktalı eşik çizgileri; görsel, açıldı).
  2. 5g Toplam = son 5 günlük s(t) toplamıdır; aralığı -5 ile +5 (eksen -5...+5; görsel, açıldı).
  3. BULL: 5g Toplam yeşil kesik çizgiyi (+3) yukarı geçtiğinde, fiyatın altına yeşil ok ve etiket. BEAR: 5g Toplam kırmızı kesik çizgiyi (-4) aşağı geçtiğinde, kırmızı ok ve etiket (görsel, açıldı).
  4. s(t) tanımı Ham'dan okunur (YORUM): kapanış (veya gün yükseği) son rolling periyodun en yükseğini aşarsa +1, en düşüğünün altına inerse -1, aralık içindeyse 0. Rolling periyodun uzunluğu yazılı değildir.
  5. Durum okuması (Ham): -1 nötr bölge, "kararsızlık" evresi; yeni boğa için 4 puan yukarı, panik için 3 puan aşağı gerekir (hesap bizim: -1'den +3'e 4 puan, -1'den -4'e 3 puan; Ham'daki "Boğa eşiğine: +4 / Panik eşiğine: 3 birim" eşik değil, uzaklıktır). Nötr bölgede yeni pozisyon açılmaz; kırılım beklenir (Ham).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| BULL eşiği | 5g Toplam >= +3 | Ham ve görsel, açıldı |
| BEAR eşiği | 5g Toplam <= -4 (Ham: "-4 veya -5") | Ham ve görsel, açıldı (kesik çizgi -4) |
| Toplam penceresi | 5 gün | Ham ve görsel (başlık `5g Toplam`) |
| Günlük sinyal değerleri | -1, 0, +1 | görsel, açıldı (YORUM) |
| Rolling periyot uzunluğu | yok | - |
| Giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: rolling periyodun uzunluğu; s(t) yüksek veya kapanışa göre mi; etiketin yalnız eşiğe ilk varışta mı yoksa her barda mı çıktığı (görselde yeşil oklar eşik çizgisine ilk varışta durur; YORUM); BULL ve BEAR'dan sonra pozisyon kuralı (giriş, stop, çıkış) yok; hesap kodu paylaşılmadı.
- Tansu'nun kanıtı: yok; FROTO'da Ocak 2024 - Nisan 2026 arası yaklaşık 20 etiket, sonuç sayısı yok. Seçilmiş örnek.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC); rolling periyot seçilmeden kural tam değildir.
- Kaynak güveni: Ham ve görsel birinci el; eşikler açık, s(t) formülü ve pencere yok: orta-düşük. Hazırlık K.

## 47. Bullish Hikkake: iç bar, sahte aşağı kırılım, yukarı dönüş ve iç bar altı stop

- Kaynak: `tweet-bullish-hikkake-ic-bar-stop-1913982654933848532` (20.04.2025; Ham ve görsel, açıldı). Tansu'nun X gönderisidir (birinci el). Ham emoji başlıklı ders metni gibi okunur, yapay zekâ özeti olabilir (YORUM); Ham olarak birinci el sayılır. Sembol yazılı değil ("Grafikte görülen kardeş"). C §17 ve ENJSA örneğinde "Hikkake" yalnız anılır; tanım ve stop orada yoktu.
- Tansu'nun ifadesi (verbatim):
  - Ham: "önce bir iç bar (inside bar) oluşur yani mevcut mum, önceki mumun gövdesi ve fitili içinde kalır."
  - Ham: "Sonraki gün bu sıkışma aşağı yönlü kırılır gibi olur (fiyat önce düşer) fakat birkaç gün içinde fiyat toparlar ve yukarı yönlü hareket eder."
  - Ham: "İç bar kırılımı sonrası yukarı yönlü dönüş yakalandıysa alıma geçilebilir. Stop-loss genelde iç barın altına konur."
  - Ham: "Volatilite düşükken ortaya çıktığında daha anlamlıdır." Teyit: "RSI / MACD", "Hacim", "EMA 8 veya EMA 21’e tutunuyorsa, pozitif sinyal olur."
- Tanım (Ham ve YORUM):
  1. İç bar: t-1 mumunun High ve Low değerleri t-2 mumunun aralığı içindedir (Ham: "gövdesi ve fitili içinde"; YORUM: High[t-1] <= High[t-2] ve Low[t-1] >= Low[t-2]).
  2. Sahte kırılım: iç bardan sonra fiyat iç barın altına sarkar (Ham: "fiyat önce düşer").
  3. Dönüş: birkaç gün içinde yeşil mum ve yukarı hareket; kısa pozisyonlar stop olur (Ham). Görselde (açıldı) 18 Nisan 2025 mumu uzun alt fitille önceki mumların dibinin altına sarkıp büyük yeşil kapanır; altında yeşil üçgen. Görselden hangi mumun iç bar olduğu kesin okunmaz (YORUM).
  4. Giriş: dönüş yakalandıktan sonra (Ham: "alıma geçilebilir"); giriş fiyatı ve günü yazılı değil.
  5. Stop: iç barın altı (Ham; YORUM: iç barın Low değeri).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Formasyon | iç bar + sahte aşağı kırılım + yukarı dönüş (bullish) | Ham |
| Dönüş süresi | "birkaç gün içinde" | Ham |
| Stop | iç barın altı | Ham |
| Teyit | RSI/MACD, hacim artışı, EMA 8 veya EMA 21 desteği; eşik yok | Ham |
| Bağlam | düşük volatilite | Ham |
| Hedef | yok | - |
| Zaman dilimi | günlük (görselde günlük mumlar; YORUM) | görsel, açıldı |

- Belirsiz kalanlar: dönüşün kaç gün içinde sayıldığı; giriş tetiği (yeşil mum kapanışı mı, iç bar yükseğinin aşılması mı); hacim ve RSI eşiği; düşük volatilite ölçüsü; hedef; sembol ve sonuç.
- Tansu'nun kanıtı: yok (tek grafik örneği, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC). Giriş tetiği ve hedef olmadan kural eksiktir.
- Kaynak güveni: Ham ve görsel birinci el; kural sözlü, stop var, tetik ve hedef yok: orta-düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-hikkake-talep-bolgesi-retest-2088581502023999495` — Kural: Hikkake talep bölgesindeki retest ile birlikte aranır. Ham: "Şu formasyonu (Hikkake) talep bölgesinde retest ile yakalarsanız, ballı ekmek kadayıfından bi tık daha lezzetli bir öğün alırsınız" (15.08.2026).

## 48. Bullish Tasuki: iki yeşil mum, yukarı boşluk, boşluğa inen kırmızı mum ve kodu (GARAN)

- Kaynak: `tweet-bullish-tasuki-mum-kurali-kod-1905592381618962842` (GARAN.IS örneği, 28.03.2025; Ham, G1 görsel metni ve G2 kod görseli, G2 açıldı). Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim):
  - Ham: "Birinci mum yeşil (pozitif) bir mumdur," "İkinci mum da yeşil (pozitif) olup, birinci mumun üzerinde bir boşluk (gap) ile açılır," "Üçüncü mum ise kırmızı (negatif) bir mumdur ama birinci mumun kapanış fiyatının altına inmez." "Kodu da verilmiştir".
  - Kod (G2, açıldı; kod yorumları Tansu'nundur): `data[i, close] < data[i, open]` ("3. mum kırmızı"); `data[i, close] < data[i - 1, open]` (yorum: "3. mum, 2. mumdan daha aşağıda açılmış"); `data[i, close] > data[i - 2, close]` ("3. mum, 1. mumun kapanışından yukarıda kapandı"); `data[i - 1, close] > data[i - 1, open]` ("2. mum yeşil"); `data[i - 1, open] > data[i - 2, close]` ("2. mum, 1. mumun kapanışından yukarıda açılmış (gap)"); `data[i - 2, close] > data[i - 2, open]` ("1. mum yeşil").
  - G1 başlığı (görsel metni): "GARAN.IS - Tasuki Pattern", lejant "Candlestick", "Buy Signal", "Sell Signal"; Haziran-Eylül 2024.
- Tanım (kod, YORUM yorumlama): i barı üçüncü mumdur. (1) mum i-2: yeşil (Close > Open). (2) mum i-1: yeşil ve Open[i-1] > Close[i-2] (birinci kapanışın üstünde boşluk). (3) mum i: kırmızı, Close[i] < Open[i-1] (ikinci mumun açılışının altında kapanış) ve Close[i] > Close[i-2] (birinci kapanışın üstünde kalır, boşluğu tamamen kapatmaz). Altı koşul birlikte doğruysa formasyon vardır. `buy` veya `sell` sütununa yazma satırı görselde yoktur (kod kesik).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Mum sayısı | 3 | Ham ve kod, açıldı |
| Mum 1 | yeşil | Ham ve kod |
| Mum 2 | yeşil, Open2 > Close1 (boşluk) | Ham ve kod |
| Mum 3 | kırmızı, Close3 < Open2, Close3 > Close1 | kod, açıldı |
| Boşluk büyüklüğü, gövde eşiği, önceki trend | yok | - |
| Giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: kodun yorum satırı ("2. mumdan daha aşağıda açılmış", yani Open3 < Open2 gibi okunur) ile kod koşulu (Close3 < Open2) uyuşmaz: üçüncü mumun açılışı hiç denetlenmez (YORUM: yorum satırı hatalıdır veya koşul eksiktir); Ham "birinci mumun kapanış fiyatının altına inmez" der, kod bunu Close3 > Close1 olarak yazar, düşük fitil denetlenmez; sinyalin hangi sütuna yazıldığı; giriş günü ve çıkış; önceki yukarı trend şartı yok (klasik yükselen Tasuki boşluğu devam formasyonudur, Tansu "Bullish Tasuki" der, YORUM).
- Tansu'nun kanıtı: yok (tek GARAN grafiği, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC; üç mumluk dedektör). Yorum satırı ile kod arasındaki fark çözülmeden birebir kodlanmaz.
- Kaynak güveni: Ham ve kod birinci el, transkripsiyon görselle uyuşur; kod kesik, giriş ve çıkış yok: orta-düşük. Hazırlık H.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-tasuki-gap-uc-mum-kurali-1914394674921722043` — Okuma (YORUM): Daha sonraki Tasuki anlatımı trend ve filtre bağlamı ekler. Ham: “Üçüncü mum: Kırmızı mumdur ama gap’in içine girmez, yani gap’i doldurmaz.” Bearish sürüm: “Üçüncü mum Yeşil mumdur ama gap’i tamamen kapatmaz.” Teyit: “EMA, RSI, MACD gibi göstergelerle desteklenirse yanlış sinyaller filtrelenebilir.” Okuma (YORUM): Boşluğa hiç girmeme ifadesi, mevcut bölümdeki boşluk içinde kapanış koduyla aynı değildir.
  - `tweet-yukselen-tasuki-gap-devam-1919047175444533558` — `tweet-yukselen-tasuki-gap-devam-1919047175444533558` (2025-05-04). Yapı: "Güçlü bir yeşil (boğa) mum gelir.", "Ardından yukarı yönlü bir fiyat boşluğu (gap) ile tekrar yeşil mum oluşur.", "Üçüncü mum kırmızı olur ama gap’i tamamen kapatmaz." (Ham; görsel açıldı).

## 49. Dark Cloud Cover (kara bulut örtüsü): düşüş sinyali, stop ilk mumun tepesi, hedef yakın destek

- Kaynak: `tweet-dark-cloud-cover-stop-ilk-mum-tepe-1982688365007794207` (27.10.2025; Ham ve G1, açıldı). Tansu'nun X gönderisidir (birinci el). Ham ders metni gibi okunur (YORUM; Ham olarak birinci el sayılır). Sembol yok ("emsai öncesi" ifadesi bir hisseye işaret edebilir, belirsiz).
- Tansu'nun ifadesi (verbatim):
  - Ham: "Bu bir düşüş sinyalidir ve yukarı trendde görülür." "İlk mum beyaz ve uzun olmalıdır." "İkinci mum siyah olmalı ve ilk mumun üstünde açılıp ilk mumun ortasından aşağısında kapanmalıdır. Ne kadar aşağıda kapanırsa o kadar güçlü sinyal olur."
  - Ham: "Özellikle direnç seviyesinde veya yukarı trendin sonunda görürsen güçlü düşüş sinyalidir. Hacim de önemlidir. İkinci günde hacim artışı varsa sinyal daha güvenilirdir."
  - Ham: "Risk yönetimi için stop loss ilk mumun en yüksek seviyesine koyabilirsin. Hedef olarak da yakındaki destek seviyelerini kullanabilirsiniz." "hiçbir formasyon yüzde yüz çalışmaz. Başka göstergelerle de teyit almalısınız."
  - G1 (görsel, açıldı): ders şeması: üç yükselen çubuk, uzun beyaz mum, onun yukarısında açılan siyah mum; siyah mumun kapanışı beyaz mumun gövde ortasının altındadır ve beyaz mumun açılışının üstündedir.
- Tanım (Ham ve görsel; formül YORUM):
  1. Ön koşul: yukarı trend (Ham). Ölçüt yazılı değil.
  2. Mum 1: beyaz (yeşil) ve uzun (uzunluk eşiği yok).
  3. Mum 2: siyah (kırmızı); açılış mum 1'in üstünde (YORUM: Open2 > High1; Ham "ilk mumun üstünde"; şemada siyah gövdenin tepesi beyaz mumun fitil ucunun üstündedir); kapanış mum 1 gövdesinin orta noktasının altında: Close2 < (Open1 + Close1) / 2 (YORUM; şemada Close2 > Open1).
  4. Güç: kapanış orta noktanın ne kadar altındaysa o kadar güçlü (Ham).
  5. Anlam: "satış düşünmelisiniz" (Ham). BIST'te kısa pozisyon pratik değil (TASARIM §3); YORUM: mevcut alımı kapatma uyarısı olarak okunur.
  6. Stop: mum 1'in en yüksek seviyesi (Ham; kısa pozisyon stopu). Hedef: yakındaki destek seviyeleri (Ham; sayı yok). Levent 16.10: Tansu hedef verdiği için kural bu hedefi kullanır.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Ön koşul | yukarı trend; en iyisi direnç veya trend sonu | Ham |
| Mum 1 | uzun beyaz | Ham |
| Mum 2 | siyah, açılış mum 1'in üstünde, kapanış mum 1 gövde ortasının altında | Ham ve görsel, açıldı |
| Teyit | ikinci gün hacim artışı; başka göstergeler | Ham |
| Stop | mum 1'in en yüksek seviyesi | Ham |
| Hedef | yakındaki destek seviyeleri (sayı yok) | Ham |
| Uzunluk, hacim eşiği | yok | - |

- Belirsiz kalanlar: Ham "ilk mumun üstünde açılıp" der: üstü High1 mi Close1 mi; orta nokta gövdenin mi tüm aralığın mı (Ham "ortasından"; şema gövde ortasını gösterir, YORUM); "uzun" eşiği (YORUM: gövde / ATR); yukarı trend ölçütü; destek seviyesinin bulunması; çıkış kuralı alım pozisyonu için ayrı yazılmamıştır; bu sistem yalnız alış yönlüdür.
- Tansu'nun kanıtı: yok (şema, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLCV); yukarı trend ve uzunluk ölçüsü seçilmeden kural eksiktir.
- Kaynak güveni: Ham ve şema birinci el; mum kuralı net, stop ve hedef sözlü, ölçüler yok: orta. Hazırlık K.

## 50. Doji mum + RSI(14) 30/70 al-sat taraması (FROTO kodu, günlük gün sonu taramaları)

- Kaynak: `tweet-doji-mum-rsi-14-al-sat-sinyali-1842657804374720958` (05.10.2024; Ham ve kod görseli, G1 açıldı; kod ayrıca dış bağlantıda, açılmadı), `tweet-doji-rsi-30-70-sinyal-1844841798608286006` (11.10.2024; Ham ve görsel metni), `tweet-doji-rsi-30-70-sinyal-1847540406533210185` (19.10.2024; Ham ve iki görselin metni). Hepsi Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim): "Doji mum ve RSI kombinasyonuna bakalım." (Ham, 05.10.2024). Yanıt (Ham): "Doji mum olsun ve RSI > 30 olsun. Al koşulu o zaman geliyor". 11.10.2024 (Ham): "Alım Sinyali (Buy Signal): Doji formasyonu + RSI ≤ 30" ve "Satım Sinyali (Sell Signal): Doji formasyonu + RSI ≥ 70". 19.10.2024 (Ham): "Dünlük doji mumu oluşumu ve RSI30 RSI70". Kod (görsel, açıldı): `data['RSI_14'] = ta.rsi(data['Close'], length=14)`; `data['Doji'] = np.abs(data['Open'] - data['Close']) <= (data['High'] - data['Low']) * 0.1`; `buy_signals = doji_indices[doji_rsi_values <= 30]`; `sell_signals = doji_indices[doji_rsi_values >= 70]`; örnek `FROTO.IS`, `period='6mo'`, `interval='1d'`.
- Tanım (kod, görsel, açıldı; YORUM işaretli yerler hariç):
  1. Doji: gövde `|Open − Close|` en çok `0,1 × (High − Low)` (aralığın %10'u).
  2. RSI: `pandas_ta.rsi`, 14 periyot (YORUM: pandas_ta varsayılanı Wilder yumuşatmasıdır; §42'deki basit ortalamalı RSI'dan farklıdır).
  3. Al: aynı barda doji ve RSI ≤ 30. Sat: aynı barda doji ve RSI ≥ 70.
  4. Tarama günlüktür ve gün sonunda çalışır; çıktı başlığı "Gün Sonu Sinyali Veren Hisseler" (görsel metni). Çıktı örnekleri: 11.10.2024'te dokuz hisse, hepsi "Buy Signal" (BOSSA, DOFER, ECILC, FORTE, IPEKE, ISBTR, IZFAS, KAREL, KMPUR); 19.10.2024'te INVEO ve KGYO "Buy Signal", SKTAS ve TKFEN "Sell Signal" (görsel metni). Sembol listeleri kural öğesi değil, tarama çıktısıdır.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Doji gövde eşiği | 0,1 × (High − Low) | görsel, açıldı (Ham'da yok) |
| RSI periyodu | 14 | görsel, açıldı |
| Al eşiği | RSI ≤ 30 | görsel, açıldı; Ham'da yanıt "> 30" çelişir |
| Sat eşiği | RSI ≥ 70 | görsel, açıldı; Ham |
| Periyot | günlük (gün sonu) | görsel, açıldı; görsel metni |
| Giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: Ham yanıtı "RSI > 30" ile koddaki `<= 30` çelişir (kod ve 11.10.2024 gönderisi ≤ 30 der; çoğunluk ve kod esas, YORUM); "sat" BIST'te açığa satış mı çıkış mı; giriş hangi gün ve fiyattan; doji tek başına yönsüzdür, Tansu aynı dönemde teyit mumu ister (§51); düşen trend filtresi yok (§43); eşiklerin hisse bazlı optimizasyonu: karar Levent'te bekliyor (E K29). RSI 30/70 düzey koşulu §42'dedir; fark: burada doji koşulu da gerekir.
- Tansu'nun kanıtı: yok (sonuç, backtest, isabet oranı yok; yalnız tarama çıktıları).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLC ve RSI).
- Kaynak güveni: Ham ve kod birinci el; tarama koşulu tam (kodda); giriş, çıkış ve kanıt yok: orta. Hazırlık H.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-gunluk-doji-rsi-30-70-tarama-1848803325514334339` — Okuma (YORUM): Günlük taramanın tekrar paylaşımı. Ham: "Günlük doji mum ve RSI30/70".
  - `tweet-gunluk-doji-rsi30-rsi70-tarama-1847542553165389901` — Okuma (YORUM): Tarama bağlantısının paylaşımı. Ham: "Günlük DOji ve RSI30/RSI70".
  - `tweet-rsi-30-70-doji-mum-tarama-1840331080827576539` — - `tweet-rsi-30-70-doji-mum-tarama-1840331080827576539` (2024-09-29; Ham): Ham: "koşuulalr Doji mum ve RSI<30 ise al, >70 ise sat." Düzeltme: "RSI 30/70 olacak." Okuma (YORUM): bu kaynak katı eşitsizlik yazar; bölümdeki sonraki kodun ≤30/≥70 sınırları değiştirilmez.

## 51. Doji price action: düşen piyasada doji + boğa teyit mumu (üç mum kodu), gösterge teyitleri, stop ve hedef

- Kaynak: `tweet-doji-boga-teyit-mumu-1907860073239683477` (03.04.2025; Ham ve görsel, açıldı), `tweet-doji-uc-mum-sinyal-kodu-1906259245223354396` (30.03.2025; üç gönderilik zincir; Ham ve kod görseli, iki görsel de açıldı), `tweet-doji-teyit-ema-rsi-macd-adx-1913979295262769619` (20.04.2025; Ham ve görsel, açıldı). Hepsi Tansu'nun X gönderisidir (birinci el). Aynı doji için RSI 30/70 taraması ayrı bölümdedir (§50).
- Tansu'nun ifadesi (verbatim): "Teorik boğa yönlü Doji formasyonu:" "Düşen bir piyasada, kararsızlık mumu olan Doji'nin ortaya çıkması, yön değişiminin ilk ipucu olabilir." "Ancak bu durumun, ardından gelen bir yükseliş (bullish) mumu ile teyit edilmesi gerekir." "Kodladık tarattık" (Ham, 03.04.2025; satırlar). "Doji formasyonu da tek mumdan oluşur ve açılış fiyatı ile kapanış fiyatı eşittir." (Ham, 30.03.2025). Örnek strateji (Ham, 20.04.2025): "1. gün: Al sinyali geldi, ancak bekle." "2. gün: Fiyat bir önceki günün tepesini geçerse, hacim artarsa, RSI & MACD destekliyorsa alıma geçilebilir." "Stop-loss: Al sinyalinden bir gün önceki dip seviyesi." "Hedef: Son zirve (yaklaşık XX TL) ve yukarısı." "bu sinyal tek başına yeterli değil" (Ham).
- Tanım:
  1. Kod (görsel, açıldı; boğa): bar i-2 kırmızı (`close < open`); bar i-1 doji (`close == open`, tam eşitlik); bar i yeşil (`close > open`) ve `close[i] > close[i-1]` ise `buy = 1` (kod yorumu: "Artık i+1 değil, i": sinyal teyit mumunun kendisindedir). Ayı biçimi aynalıdır: i-2 yeşil, i-1 doji, i kırmızı ve `close[i] < close[i-1]` ise `sell = -1`. Kodda i-2 koşulu iki kez aynen yazılıdır; i-3 koşulu yoktur (görsel, açıldı).
  2. Görseller (açıldı): kırmızı kutuda küçük gövdeli doji ve ardından yeşil mum; yeşil mumda yeşil üçgen (Buy Signal).
  3. Teyit (Ham, 20.04.2025): al sinyalinin geldiği gün (doji sonrası yeşil mum) hemen girilmez; ertesi gün: fiyat önceki günün zirvesini geçer, hacim artar, RSI ve MACD destekler. Destek göstergeleri: sinyal gününün hacmi önceki günlere göre artmış; EMA8 EMA21'i yukarı kesmek üzere ve fiyat EMA8 üstünde; RSI 50 üstünde kalıcı, son diplerde pozitif uyumsuzluk; MACD çizgisi sinyali yukarı kesmiş ve histogram sıfır üstünde; ADX yükseliyor ve DI+ yukarıda.
  4. Çıkış (Ham, 20.04.2025): stop = al sinyalinden bir gün önceki dip; hedef = son zirve ve yukarısı. Levent 16.10: Tansu hedef verdiği için kural bu hedefi kullanır.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Doji | açılış = kapanış (kod: tam eşitlik) | Ham ve görsel, açıldı |
| Önceki mum | kırmızı (düşen piyasa) | görsel, açıldı |
| Teyit mumu | yeşil ve kapanış > doji kapanışı | görsel, açıldı |
| Giriş günü | sinyalden sonraki gün, önceki günün zirvesi aşılınca | Ham |
| Stop | al sinyalinden bir gün önceki dip (YORUM: doji mumunun en düşüğü) | Ham |
| Hedef | son zirve ("yaklaşık XX TL", sayı yok) | Ham |
| Teyit göstergeleri | EMA 8/21, RSI 50, MACD sinyal kesişimi, ADX ve DI+, hacim artışı | Ham |
| Hacim, ADX eşiği | yok | BELİRSİZ |

- Belirsiz kalanlar: sinyal günü doji mi yeşil mum mu (Ham: "Son günkü yeşil mum içinde oluşan al sinyali", yani yeşil mum; YORUM); stop'un tam bar ve fiyat tanımı; doji için §50'de 0,1 × aralık eşiği kullanılır, burada tam eşitlik; kod ikinci düşüş mumunu gerçekten istiyor mu (tekrarlı koşul); teyit göstergelerinin hangisinin zorunlu olduğu; ayı biçiminin BIST'te anlamı (açığa satış mı çıkış mı). Kural yalnız düşen trendin dibinde anlamlıdır: trend tanımı yok (§43 genel uyarısı).
- Tansu'nun kanıtı: yok (örnek sembol ve sonuç yok; 20.04.2025 gönderisinde fiyatlar "XX TL" ile gizli).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLCV; üç mum kodu doğrudan, teyit göstergeleri standart).
- Kaynak güveni: Ham ve kod birinci el; kod net, teyit ve çıkış sözel, eşiksiz: orta-düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-uc-gun-doji-mum-kurali-sinyal-1905554574435361265` — Okuma (YORUM): Üç mum için açık koşul ve sonraki satıra işaret. Ham: “Güncel kapanış fiyatı, güncel açılış fiyatından büyükse,”, “Bir önceki günün kapanış fiyatı, açılış fiyatına eşitse,”, “Ondan bir önceki günün kapanış fiyatı, açılış fiyatından düşükse,” ve “sonraki satıra 1 yaz.”

## 52. RSI pozitif uyumsuzluk taraması: fiyatta düşen dip, RSI'da yükselen dip; mum, EMA, hacim, MACD ve Stokastik teyidi (AVHOL, BINHO, PARSN)

- Kaynak: `tweet-divergence-ema-macd-stoch-checklist-1911876515043692724` (14.04.2025; Ham ve görsel, açıldı), `tweet-divergence-engulfing-ema-1910771334558130427` (11.04.2025; Ham ve görsel metni), `tweet-divergence-inverted-hammer-1910743114530385964` (11.04.2025; Ham ve iki görselin metni; AVHOL), `tweet-divergence-tasuki-gap-1910750627728175106` (11.04.2025; dört gönderilik zincir; Ham ve görsel metni; BINHO), `tweet-dragonfly-doji-divergence-ema-1914398342404006237` (21.04.2025; Ham ve iki görsel, G1 açıldı; PARSN). Hepsi Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim): "Bugünkü RSI Pozitif uyumsuzluk taramamıza takılan bu kardeşimizi kısaca inceleyelim. Uyumsuzluk cuma oluşmuş." "RSI Pozitif Uyumsuzluk: Fiyat düşerken RSI yükselmiş. Bu, düşüş momentumunun zayıfladığına ve alım yönlü bir dönüş ihtimaline işaret eder." Teyit listesi (Ham): fiyat "EMA5, EMA8, EMA13 ve EMA21" üzerine çıkmış; "Son günlerde hacimde gözle görülür bir artış var"; MACD çizgisi sinyal çizgisini yukarı kesmiş, histogram pozitife dönmeye başlamış; Stokastik "henüz aşırı alım bölgesine girmemiş", yukarı ivme. "Her zaman risk yönetimi elden bırakılmamalı." Mum teyitleri (Ham): "Hem pozitif uyumsuzluk var hemde yutan boğa. tabi ema kombinasyonlarına da bakmak laızm." "Uyuşmazlığın yanında Tasuki Gap mum formasyonu sinyali de geldi.Bu bir bir boğa devam formasyonudur." "RSI uyumsuzluk → alım sinyali, Tasuki Gap → alımın momentum kazandığını ve devam edeceğini gösteriyor." "Dragonfly doji yapmış ... bir de cuma günü uyumsuzluk yapmış bugün teyit edilmiş.ema kesişimleri de şahane" (Ham). AVHOL için tek yorum: "Süper yakalamış mumu" (Ham).
- Tanım (YORUM; Ham ve görsellerden):
  1. Pozitif (düzenli) uyumsuzluk: fiyatta aralıkta düşen dip (görselde "Fiyat Düşüşü" çizgisi), RSI'da aynı aralıkta yükselen dip (görselde "RSI Yükselişi" çizgisi). Bu, §9 gizli uyumsuzluğun tersidir (orada fiyat yüksek dip, osilatör düşük dip).
  2. Tarama günlük çalışır; çıktı başlığı `<SEMBOL>.IS - Pozitif Uyumsuzluk #n: <başlangıç> → <bitiş>` biçimindedir. Örnekler (görsel metni): AVHOL #5: 2025-01-28 → 2025-04-09; BINHO #8: 2025-01-07 → 2025-04-09; PARSN #3: 2025-01-29 → 2025-04-18. Aralıklar 71, 92 ve 79 takvim günüdür (hesap bizim). Bitiş tarihi tespit günüdür. "#n" sayısının anlamı belirsizdir (YORUM: o hissede n. uyumsuzluk).
  3. Teyit katmanları (hepsi Ham'da yardımcı olarak sayılır, zorunlu sayılmaz): (a) TA-Lib mum formasyonu: görsellerde `CDLINVERTEDHAMMER`, `CDLTASUKIGAP`, `CDLENGULFING`, `CDLDRAGONFLYDOJI` (başlık: "tespit edilen formasyonlar"); (b) fiyat EMA5, EMA8, EMA13, EMA21 üstünde; (c) hacim artışı; (d) MACD çizgisi sinyali yukarı keser ve histogram pozitif; (e) Stokastik %K-%D aşırı alımda değil ve yukarı ivmeli.
  4. Tasuki Gap (Ham, boğa devam formasyonu): 1. mum güçlü yeşil; 2. mum yukarı gap bırakıp açılan yeşil mum; 3. mum kırmızı ama gap alanını tamamen kapatmaz. Tansu'nun okuması: uyumsuzluk sonrası alım dalgasının teyidi. Kodlu üç mumluk Tasuki tanımı §48'dedir.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Kısa EMA seti | 5, 8, 13, 21 | Ham (görsel lejantı üçüncü çizgiyi "EMA5" yazar, görsel, açıldı) |
| RSI periyodu | 14 (yalnız PARSN G1 paneli: "RSI (14) & EMA(10)") | görsel, açıldı; tarama için belirsiz |
| Uyumsuzluk aralığı | örnekte 71–92 gün | görsel metni; ölçüm |
| Mum formasyonları | TA-Lib CDL işlevleri (ters çekiç, Tasuki Gap, yutan, yusufçuk doji) | görsel metni |
| Pivot (dip) seçim kuralı, en küçük aralık | yok | BELİRSİZ |
| Giriş günü, stop, hedef | yok | - |

- Belirsiz kalanlar: dip pivotlarının seçimi; RSI periyodu ve Wilder mi basit mi olduğu; teyit katmanlarından hangilerinin zorunlu olduğu; "teyit" günü (Ham: cuma uyumsuzluk, pazartesi teyit); giriş fiyatı, stop ve hedef; Tansu'nun §9 aracının (Swing=15, MinGap=15) bu tarama olup olmadığı. Teyit listesinin dili, yapay zekâ üslubunda genel bir kontrol listesine benzer (YORUM); eşik içermez.
- Tansu'nun kanıtı: seçilmiş örnekler. BINHO: "%8'e yakın marj" (Ham, tek gün; YORUM: DEY marjı gibi dönem en yüksek / referans). AVHOL ve PARSN için sonuç yok. Başarı oranı yok. Stratejinin sınaması yok.
- Günlük bedava veriyle uygulanabilir mi: evet, kısmen (OHLCV: RSI, EMA, MACD, Stokastik, hacim, TA-Lib mumları). Uyumsuzluk için pivot kuralı ve pencere YORUM olarak seçilmelidir.
- Kaynak güveni: Ham ve görsel birinci el; teyit listesi tam, eşiksiz; uyumsuzluk algoritması yok: orta-düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-endeks-duzeltilmis-rsi-uyumsuzluk-2092709099364405261` — `tweet-endeks-duzeltilmis-rsi-uyumsuzluk-2092709099364405261` (2026-08-26; Ham ve varsa görsel): Okuma (YORUM): endekse göre düzeltilmiş gösterge paneliyle uyumsuzluk örneği. Görselde "XU100-ADJUSTED", "REG BEAR" ve "REG BULL" etiketleri görülür (görsel açıldı). Beyazla kapalı başlık tamamlanmadı.
  - `tweet-pozitif-uyumsuzluk-basarisizlik-filtreleri-1911052816333918382` — - `tweet-pozitif-uyumsuzluk-basarisizlik-filtreleri-1911052816333918382` (2025-04-12; Ham): Başarısızlık filtresi: "Pozitif uyumsuzluk bir potansiyel sinyaldir" ve "Her zaman yükselişle sonuçlanmaz." Ham, genel düşüş trendi, yetersiz momentum/hacim, EMA direnci ve haber/makro risklerini sayar.
  - `tweet-pozitif-uyumsuzluk-marubozu-ema-siralama-1915163157531910187` — - `tweet-pozitif-uyumsuzluk-marubozu-ema-siralama-1915163157531910187` (2025-04-23; Ham): Teyit birleşimi (Ham): "Pozitif uyumsuzluk marubozu mum alternatif momentum son gün breakout ema5-8-13-34 sıralaması." Okuma (YORUM): örnek birleşimdir; bütün uyumsuzluklara zorunlu kapı olarak taşınmaz.
  - `tweet-pozitif-uyumsuzluk-rsi-macd-stokastik-1913973089353740645` — - `tweet-pozitif-uyumsuzluk-rsi-macd-stokastik-1913973089353740645` (2025-04-20; Ham): Alım zamanı (Ham): "RSI kırılımı sonrası veya MACD kesişimi sonrası ya da" "EMA’ların yukarı yönde sıralandığı anlarda". Destek bağlamı: "Bu tür pozitif uyumsuzluklar özellikle destek bölgelerinde görülüyorsa çok daha güçlü olur."
  - `tweet-rsi-divergence-candle-scan-1910741892095942791` — - `tweet-rsi-divergence-candle-scan-1910741892095942791` (2025-04-11; Ham): Entegrasyon (Ham): "Artık son gün uyumsuzluk olan her hissede hangi mum formasyonu oluştuğu da görülebilecek." Okuma (YORUM): mum etiketinin gösterilmesi, bütün mum türlerinin zorunlu al filtresi olması demek değildir.
  - `tweet-rsi-fibonacci-pozitif-uyumsuzluk-1843367384163422579` — - `tweet-rsi-fibonacci-pozitif-uyumsuzluk-1843367384163422579` (2024-10-07; Tansu'nun X gönderisi). TARKM örneği (Ham ve görsel metni): "Hayır ama enteresan bir pozitif uyumsuzluk var, teknikçi arkadaşlar daha detaylı bakabilir." Okuma (YORUM): tek grafik yorumu, tarama algoritmasının tanımı değildir.
  - `tweet-rsi-positive-divergence-1910780377792152053` — - `tweet-rsi-positive-divergence-1910780377792152053` (2025-04-11; Ham ve görsel metni; Tansu'nun X gönderisi): "Pozitif uyumsuzluk 8 Nisanda gelmiş" Okuma (YORUM): BTC-USD uyumsuzluk örneği; BIST performans kanıtı değildir.
  - `tweet-rsi-positive-divergence-scan-1954338937188622732` — - `tweet-rsi-positive-divergence-scan-1954338937188622732` (2025-08-10; Ham ve görsel metni; Tansu'nun X gönderisi): "Uyumsuzluk gelmiş tüm göstergeler pozitif. Getisini de yaptı." Okuma (YORUM): FROTO seçilmiş sonuç örneği; genel başarı oranı değildir.
  - `tweet-rsi-pozitif-uyumsuzluk-1910089745280942309` — - `tweet-rsi-pozitif-uyumsuzluk-1910089745280942309` (2025-04-09; Ham ve görsel metni; Tansu'nun X gönderisi): "Teker teker uyuşmazlıkları da bulmaya başladık:)" Okuma (YORUM): Pozitif uyumsuzluk taraması örneği.
  - `tweet-rsi-pozitif-uyumsuzluk-1925619119774134432` — - `tweet-rsi-pozitif-uyumsuzluk-1925619119774134432` (2025-05-22; Ham ve görsel metni; Tansu'nun X gönderisi): "RSI Pozitif uyumsuzluk" Okuma (YORUM): Pozitif uyumsuzluk örneği.
  - `tweet-rsi-pozitif-uyumsuzluk-coklu-teyit-1912924416888955074` — - `tweet-rsi-pozitif-uyumsuzluk-coklu-teyit-1912924416888955074` (2025-04-17; Ham ve görsel metni; Tansu'nun X gönderisi): "Bu tür bir uyumsuzluk, fiyat daha düşük dip yaparken RSI’ın daha yüksek bir dip yapması ile oluşur." Okuma (YORUM): Çoklu teyit (Ham): "MACD çizgisi sinyal çizgisini yukarı kesmiş, histogram pozitife dönmüş." / "Teknik analizi sadece formasyonla değil, hacim, momentum ve trend çizgileriyle birlikte değerlendirmek gerekir."
  - `tweet-rsi-pozitif-uyumsuzluk-direnc-kirilimi-1787113935742615769` — - `tweet-rsi-pozitif-uyumsuzluk-direnc-kirilimi-1787113935742615769` (2024-05-05; Tansu'nun X gönderisi). Okuma (YORUM; G1 açıldı): MIGROS grafiğinde fiyat dipleri ile alt panel diplerinin yönü farklıdır; sonra fiyat yatay direnç çizgisini aşar. G2 değerleme tablosu ayrı bağlamdır.
  - `tweet-rsi-pozitif-uyumsuzluk-kalite-filtreleri-1910400582935847408` — - `tweet-rsi-pozitif-uyumsuzluk-kalite-filtreleri-1910400582935847408` (2025-04-10; Tansu'nun X gönderisi). Görsel (açıldı): "Dipler arasında yeterli süre olsun. 3-5 gün gibi değil, idealde 2-6 hafta arası daha anlamlıdır." / "RSI 30'un altında dip yapıyorsa daha anlamlıdır (oversold bölge)." / "ama piyasa henüz onaylamamıştır." Okuma (YORUM): destek, mum, ana trend ve EMA teyitleri birlikte değerlendirilir; örnek senaryoda EMA8 kırılımı vardır.
  - `tweet-rsi-pozitif-uyumsuzluk-tanimi-ornek-1910746399530164509` — - `tweet-rsi-pozitif-uyumsuzluk-tanimi-ornek-1910746399530164509` (2025-04-11; Tansu'nun X gönderisi). Ham: "Açıklama: RSI (Relative Strength Index) göstergesi yükselirken, fiyat düşmeye devam etmiş." / "Tek başına kesin dönüş sinyali değil, ama RSI uyumsuzlukla birlikte güçlü bir dönüş potansiyeli verir." Okuma (YORUM): AVHOL ters çekiç teyidi örneğidir.
  - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910100498075525561` — - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910100498075525561` (2025-04-09; Tansu'nun X gönderisi). Ham: "Pozitif uyumsuzluk taraması". Okuma (YORUM; görsel metni): AKFYE tarama örneği.
  - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910385970685370687` — - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910385970685370687` (2025-04-10; Tansu'nun X gönderisi). Ham: "Bingooo!!:)". Okuma (YORUM; görsel metni): BINHO pozitif uyumsuzluk tarama örneği.
  - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910388484042334379` — - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910388484042334379` (2025-04-10; Tansu'nun X gönderisi). Ham: "Bunu da yarın için vereyim bakarsınız". Okuma (YORUM; görsel metni): AGESA pozitif uyumsuzluk tarama örneği.
  - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910389323251204261` — - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910389323251204261` (2025-04-10; Tansu'nun X gönderisi). Ham: "aboooo :)". Okuma (YORUM; görsel metni): AZTEK pozitif uyumsuzluk tarama örneği.
  - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910389559537303908` — - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910389559537303908` (2025-04-10; Tansu'nun X gönderisi). Ham: "bu son. daha sı grupta:)". Okuma (YORUM; görsel metni): BIGCH pozitif uyumsuzluk tarama örneği.
  - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910391996625412607` — - `tweet-rsi-pozitif-uyumsuzluk-taramasi-1910391996625412607` (2025-04-10; Tansu'nun X gönderisi). Ham: "Bu da gelsin :)". Okuma (YORUM; görsel metni): KLMSN birden çok tarih çiftinde pozitif uyumsuzluk örneği.
  - `tweet-rsi-uyumsuzluk-ema-sirasi-macd-hacim-1912212487598141833` — - `tweet-rsi-uyumsuzluk-ema-sirasi-macd-hacim-1912212487598141833` (2025-04-15; Tansu'nun X gönderisi). DOBUR teyidi (Ham): "EMA5 > EMA8 > EMA13 > EMA21 sıralaması kısa vadede güçlü al sinyali olarak yorumlanır." / "MACD çizgisi, sinyal çizgisini yukarı kesmiş ve histogram pozitif alana geçmiş."
  - `tweet-uyumsuzluk-10-30-bar-mesafe-2046663429478330488` — `tweet-uyumsuzluk-10-30-bar-mesafe-2046663429478330488` (2026-04-21; Ham). Uyumsuzluk aralığı tercihi: "Genellikle 10 ile 30 bar arası mesafeler en sağlıklı sinyali verir." (Ham). Okuma (YORUM): bu genel tercih, mevcut örnek taramaların ölçülmüş sürelerini değiştirmez.
  - `tweet-uyumsuzluk-geriye-bakis-saat-listesi-1838307130526310602` — `tweet-uyumsuzluk-geriye-bakis-saat-listesi-1838307130526310602` (2024-09-23; Ham). Saatlik geriye bakış örneği: "lookback_hours_list = [24, 72, 168, 336, 720]" ve "Örneğin saatlik veride böyle." (Ham). Okuma (YORUM): liste günlük uyumsuzluk taramasının zorunlu penceresi değildir.
  - `tweet-uyumsuzluk-mum-macd-ema-dizilim-filtresi-1911052570505736230` — `tweet-uyumsuzluk-mum-macd-ema-dizilim-filtresi-1911052570505736230` (2025-04-12; Ham). BINHO teyit örneği: "Excel'i incleyiniz, hissede bullish devam mum formasyonu bulundu taramamızda, MACD 0'ın altında pozitif sinyal üretti ve EMA'lar dasıraya girdi:)" (Ham).

## 53. WaveTrend (dalga osilatörü, 10 21): aşırı satım bölgesinde al sinyali taraması

- Kaynak: `tweet-dalga-osilatoru-asiri-satim-taramasi-1845369437441933344` (13.10.2024; Ham; G1 açıldı, G2 görsel metni), `tweet-dalga-osilatoru-stochrsi-rsi-1845198590081167684` (12.10.2024; Ham), `tweet-dalga-trend-osilator-10-21-1848426907441692797` (21.10.2024; Ham ve görsel metni; G2 açıldı). Üçü de Tansu'nun X gönderisidir (birinci el). WaveTrend A §5 tablosunda yalnız panel ayarı olarak, E K29'da DOAS testi olarak anılır; tarama bu kayıtta ilk kez.
- Tansu'nun ifadesi (verbatim):
  - 13.10.2024 (Ham): "Dalga osilatörü taramasına göre son gün aşırı satım bölgesinde al veren BIST30 hisselerİ"; çıktı #TAVHL ve #TOASO; "Gerisi detay teknikçilere kalmış."
  - 12.10.2024 (Ham): "wave osilatörü yazıyoruz daha sonra bunu" Stokastik RSI ve RSI ile "kombinleyeceğiz" (Ham'daki yazım: "stoc.rsı ve rsı").
  - 21.10.2024 (Ham): "Dalga osilatörüne göre al sinyali üreten hisseler"; "Dalga osilatörü fanatiği bir arkadaş vardı. bunu birşeyler le kombinlemek lazım, bilemedim."
  - Görsel başlıkları (görsel metni): "WT (10 21)", çizgiler "WT_1" ve "WT_2"; 21.10 listesi "Buy signal generated for these stocks in BIST 30:" ve 23 sembol.
- Tanım (görsel, açıldı; kural YORUM):
  1. Gösterge: WaveTrend, ayar (10, 21): kanal uzunluğu 10, ortalama uzunluğu 21 (görsel başlığı; YORUM: standart WaveTrend adlandırması). WT_1 turuncu çizgi, WT_2 siyah kesikli çizgi; histogram WT_1 ile WT_2 farkı gibi görünür (YORUM).
  2. Bölgeler: pembe iki yatay bant, +50 ile +60 arası (aşırı alım) ve -50 ile -60 arası (aşırı satım) (görsel, açıldı; piksel ölçümü, YORUM).
  3. Tarama (13.10): son gün aşırı satım bölgesinde "al" veren hisseler; evren BIST30. "Al" tanımı yazılı değildir. TAVHL görselinde son bar WT_1 yaklaşık -62, WT_2 yaklaşık -58 ve WT_1 hâlâ WT_2'nin altındadır (görsel, açıldı; ölçüm): yani son barda kesişim görünmez; YORUM: tarama koşulu bölgede olmak olabilir.
  4. Tansu tek başına WaveTrend'e güvenmez: StochRSI ve RSI ile birleştirme planı (12.10), "kombinlemek lazım" (21.10). "Dalga osilatörü fanatiği bir arkadaş vardı" (Ham, 21.10) cümlesi aracın başkasının favorisi olduğunu söyler.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| WaveTrend ayarı | (10, 21) | görsel, açıldı (başlık "WT (10 21)") |
| Aşırı satım bandı | yaklaşık -50 ile -60 | görsel, açıldı (ölçüm, YORUM) |
| Aşırı alım bandı | yaklaşık +50 ile +60 | görsel, açıldı (ölçüm, YORUM) |
| Tarama günü | son gün | Ham |
| Evren | BIST30 (13.10); 21.10 başlığı BIST 30 | Ham ve görsel metni |
| Veri penceresi | Ocak 2022 - Ekim 2024 | görsel, açıldı |
| "Al" tanımı, WT_2 periyodu, giriş, stop, hedef | yok | - |

- Belirsiz kalanlar: "al" tanımı (WT_1'in WT_2'yi yukarı kesmesi mi, bölgede olmak mı); bant değerleri: A §5 tablosunda eşikler 60, 53, -53, -60, E K29'da DOAS için ">-60 ve <50" yerine "<-50 ve <50" revizyonu vardır, görselde bantlar -50 ile -60 arasıdır; WT_2'nin periyodu; birleştirme planının (StochRSI, RSI) sonucu yoktur; 21.10 başlığı "BIST 30" der ama 23 sembolün çoğu BIST30'da değildir (ALGYO, BINHO, KENT ve benzeri); hisse bazlı parametre: karar Levent'te bekliyor (E K29).
- Tansu'nun kanıtı: yok (tarama çıktıları; DOAS'ta WaveTrend stratejisinin al-tutun gerisinde kaldığı E K29'dadır).
- Günlük bedava veriyle uygulanabilir mi: evet (WaveTrend günlük yüksek, düşük, kapanıştan hesaplanır); "al" tanımı olmadan kural eksiktir.
- Kaynak güveni: Ham ve görsel birinci el; ayar ve bant var, al koşulu yok: düşük-orta. Hazırlık K.

## 54. CMF para girişi filtresi: son 3 gün pozitif, önceki 3 gün negatif

- Kaynak: `tweet-cmf-3-gun-pozitif-onceki-3-gun-negatif-1845558544126366115` (13.10.2024; üç gönderilik zincir; Ham, G1 ve G2 görsel metni, G1 açıldı). Tansu'nun X gönderisidir (birinci el). Aynı filtre EMA ve RSI taramasına eklenir (§56).
- Tansu'nun ifadesi (verbatim):
  - Ham: "Uyumadan önce para giriş çıkış taraması için kod yazdım." "Bu kodu diğer stratejiler ile kullanırız. Son 3 gün pozitif ve önceki 3 gün negatif ise al sinyali doğuyor."
  - Yanıt (Ham): "Bu sinyale göre al sat yapmayın." "Son 3 gün parani girişi olan hisseleri diğer stratejilerde ayıklayacağız"
  - Yanıt (Ham): "Bu kodda bizim için önemli olan, son gün 3 pozitif olması önceki 3 gün de negatif olması. Böylece koşul karşılanmış oluyor. Al sat işaretlerine bakmayın. Bunu filtre olarak kullanacağız."
  - Görsel başlığı (görsel metni): "KRDMA.IS Closing Price & CMF Buy/Sell Signals (Last Day Signal: Buy)"; alt panel "KRDMA.IS CMF Oscillator".
- Tanım (Ham ve YORUM):
  1. Gösterge: CMF (para akışı osilatörü; görsel başlığı "CMF Oscillator", değer aralığı yaklaşık -0,4 ile +0,5; görsel, açıldı). Periyot yazılı değil.
  2. Koşul: son 3 günün CMF değeri pozitif ve ondan önceki 3 günün CMF değeri negatif (Ham). YORUM: pozitif = CMF > 0; "önceki 3 gün" = son 3 günün hemen öncesindeki 3 gün (t-5, t-4, t-3; t son gün), yani iki bitişik üçlü pencere; Ham bunu açıklamaz.
  3. Simetrik durum "sat" olarak listelenir (YORUM: son 3 gün negatif, önceki 3 gün pozitif); çıktı tablosu (sütunlar Stock ve Signal Type) 8 sembol içerir: 5 "Buy" (CEOEM, KRDMA, LIDFA, METUR, YONGA), 3 "Sell" (KRSTL, MPARK, MSGYO) (görsel metni).
  4. Kullanım: al-sat sinyali değil, filtre. Son 3 gün para girişi olan hisseler diğer stratejilerle daraltılır (Ham).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Son pencere | 3 gün CMF pozitif | Ham |
| Önceki pencere | 3 gün CMF negatif | Ham |
| Tarama günü | son gün | Ham |
| CMF periyodu | yok | - |
| Giriş, stop, hedef, çıkış | yok (filtre) | Ham |

- Belirsiz kalanlar: CMF periyodu; "pozitif" ve "negatif" sınırının 0 olduğu; iki pencerenin bitişik olduğu; filtrenin birleştirileceği diğer stratejiler; sonuç.
- Tansu'nun kanıtı: yok (tek KRDMA grafiği ve 8 sembollük çıktı, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (CMF günlük yüksek, düşük, kapanış ve hacimden hesaplanır). Periyot seçilmeden kural tam değildir.
- Kaynak güveni: Ham birinci el; kural sözlü ve açık, periyot yok: orta. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-chaikin-money-flow-kodu-20-1849791369482486118` — 25.10.2024 Ham: "Şu formülü kaydedin lazım olur." Açılan G1 kodunda "n: int=20" ve "return calculate_money_flow_volume(df, n) / df['volume'].rolling(n).sum()" yazılıdır. Okuma (YORUM): Bu ayrı CMF hesap örneğinde pencere 20'dir; önceki taramanın belirsiz periyodu kendiliğinden 20 yapılmaz.
  - `tweet-cmf-6-gun-3-pozitif-3-negatif-1865470227720405267` — 07.12.2024 Ham: "Ben CMF kullanıyorum." "Genelde  6 gün bakıyorum." "Son 3 gün pozitif" ve "Önceki 3 gün negatif ise benim için iyi bir işarettir". Okuma (YORUM): Altı günlük işaret incelemesi, CMF'nin hesap periyodu olarak okunmaz.
  - `tweet-cmf-para-girisi-uyumsuzluk-1845444032509468723` — 13.10.2024 Ham: "Sanırım güçlü uyumsuzluk sinyalleri de alabiliriz buradan." Açılan grafikte "CMF OSCILLATOR (21)" yazılıdır. Okuma (YORUM): Bu örnek 21 periyotlu CMF gösterir; ayrı üç günlük filtre taramasının ayarı kendiliğinden 21 yapılmaz.
  - `tweet-cmf-uc-gun-para-girisi-1848427208005521904` — 21.10.2024 Ham: "Son 3 gün para girişi artan hisseler". Okuma (YORUM): Üç günlük para girişi taramasının tarihli paylaşımıdır; önceki üç gün negatif koşulunu bu kısa cümle ayrıca kanıtlamaz.
  - `tweet-cmf-uc-gun-para-girisi-1848801936935678178` — 22.10.2024 Ham: "Para giriş çıkış sinyalleri". Açılan G2: "AGESA.IS: Son 3 günde para giriş çıkışına göre Chaikin Money Flow Buy sinyali oluştu." ISBIR için Sell, TDGYO için Buy yazılıdır. Okuma (YORUM): Görsel metnindeki TDGYO Sell aktarımı resimle uyuşmaz; filtre genel işlem emrine çevrilmez.
  - `tweet-cmf-uc-gun-para-girisi-1851723604758507677` — 30.10.2024 Ham: "para girişi artan hisselere bakalım". Açılan G2: "AKGRT.IS: Son 3 günde para giriş çıkışına göre Chaikin Money Flow Buy sinyali oluştu." Okuma (YORUM): Bu ileti tarama çıktısıdır; sonuç performansı veya tek başına giriş izni değildir.
  - `tweet-cmf-uzun-mfi-kisa-vade-1846088930321424470` — 15.10.2024 Ham: "Temelde aynı, uzun vadeli trendde CMF kısada mfi" ve "Matematiği farklı". Okuma (YORUM): Vade tercihi karşılaştırmasıdır; kısa ve uzun vade için yeni gün sayısı seçilmez.

## 55. EMA dizilimi son gün taraması: kısa > orta > uzun (9-14-21, 5-10-21, 5-8-13, 5-8-13-21/34)

- Kaynak: `tweet-ema-5-10-21-hizalama-tarama-1844833910817276371` (11.10.2024; Ham ve kod görseli, açıldı), `tweet-ema-9-14-21-dizilim-taramasi-1838243230472610284` (23.09.2024; Ham, çıktı görseli ve kod görseli), `tweet-ema-9-14-21-dizilim-taramasi-1838636729143533634` (24.09.2024; Ham ve kod görseli), `tweet-ema-5-8-13-21-ayari-1911869427274170527` (14.04.2025; yanıt zinciri, Ham), `tweet-ema-5-8-13-dizilimi-2000636236785209375` (15.12.2025; yanıt, Ham), `tweet-ema-5-8-13-dizilim-yon-2045521472530108518` (18.04.2026; Ham ve görsel metni). Hepsi Tansu'nun X gönderisidir (birinci el). Fiyatın EMA'ların üstünde olduğu ve RSI ile birleşen tarama ayrı bölümdedir (§56).
- Tansu'nun ifadesi (verbatim): "BIST100 9-14-21 Günlük EMA Taraması" "Al sinyali veren hisseler: DEVA, DURDO, FROTO, GENIL, INVEO, KRDMD, OTKAR" (Ham, 11.10.2024). "9-14-21 günlük EMA taramasından çıkan hissseler." (Ham, 23.09.2024). "9-14-21 GÜN EMA Kesişimlerini kodlayalım." "Geliştirmeye açık" (Ham, 24.09.2024). "5>8>13" (Ham, 15.12.2025; @Pinescriptt'e yanıt, üst gönderi notta yok). "ema 5-8-13-21" ve ardından "ema 5-8-13-34" (Ham, 14.04.2025; @BorsaSeker'e yanıt, "bu soruyu siz daha önce 2 defa daha sordunuz cevapladım"). "trend is your friend." (Ham, 18.04.2026) ve betik çıktısı "YUKARI YÖNLÜ - Güçlü alım!" (görsel metni).
- Tanım (kod, görsel, açıldı; YORUM işaretli yerler hariç): günlük kapanıştan EMA (`ewm(span=n, adjust=False)`), veri `yf.download(symbol, period="6mo", interval="1d")`, son bar `iloc[-1]`. Koşul: `EMA_a > EMA_b > EMA_c` (9-14-21 kodunda yorum satırı "Al sinyali: EMA9 > EMA14 > EMA21"). Kodlar yalnız son barın sıralamasına bakar; önceki bar ve taze kesişim aranmaz (kod başlıkta "kesişim" der, ama koşul dizilimdir). Çıktı hisse listesidir; giriş, stop, hedef, çıkış yok. THYAO çıktısında (görsel metni) fiyat 277,25 > EMA5 274,79 > EMA8 274,10 > EMA13 273,78 için "YUKARI YÖNLÜ - Güçlü alım!" etiketi çıkar (YORUM: etiketin koşulu fiyat > EMA5 > EMA8 > EMA13).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA seti, tarama 1 | 9 / 14 / 21 | Ham ve kod, açıldı (BIST30, 28 sembol) |
| EMA seti, tarama 2 | 5 / 10 / 21 | kod, açıldı (BIST100 listesi, yaklaşık 100 sembol; Ham başlığı 9-14-21 der) |
| EMA seti, yanıtlar | 5 > 8 > 13; 5-8-13-21; 5-8-13-34 | Ham |
| EMA tipi | üstel, span = n, adjust=False | kod, açıldı |
| Veri penceresi | günlük, 6 ay | kod, açıldı |
| Koşul | son bar: kısa > orta > uzun | kod, açıldı |

- Belirsiz kalanlar: Tansu'nun ana seti hangisidir (9-14-21, 5-10-21, 5-8-13, 5-8-13-21 mi 5-8-13-34 mü; ikinci yanıt düzeltme mi ek mi belli değil); fiyatın EMA'ların üstünde olma şartı; taze kesişim şartı; RSI, hacim veya çıkış yok; evren (BIST30 mu BIST100 mü). İlgili: §4 (EMA5/8/13 dizilimi tarayıcı etiketi olarak), §58 (5 > 8 > 13 > 21 dizilimi RSI ve MACD ile).
- Tansu'nun kanıtı: yok (liste, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük kapanış, EMA). Kural eşiği veya geri test yok.
- Kaynak güveni: kod ve çıktı birinci el; kural yalnız tarama koşulu, kanıt yok: orta. Hazırlık H.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-ema5-14-34-cmf-al-sinyali-1898117605552013501` — Okuma (YORUM): EMA5/14/34 dizilimine para girişi teyidi eklenir. Ham: "EMA5>EMA14>EMA34 iken para girişi varsa tatlı bişeyler olur." Bu kaynak fiyatın bütün EMA üstünde kapanması koşuluna dönüştürülmez.

## 56. Kapanış EMA'ların üstünde + RSI(14) > 50 son gün taraması (EMA14/34/55 ve EMA5/14/34/55) ve CMF dönüşü varyantı; tavan günü uyarısı

- Kaynak: iki EMA seti, aynı kural ailesi (YORUM: EMA5 sonradan eklenen sürümdür; RSI koşulu ve çıktı biçimi aynı). EMA14/34/55 sürümü: `tweet-ema-14-34-55-ustu-rsi-50-tarama-1845913799976800345` (14.10.2024; Ham; görsel yok), `tweet-ema-14-34-55-ustu-rsi50-gecis-1844069225851469851` (09.10.2024; Ham ve görsel, açıldı; TUREX örneği). EMA5/14/34/55 sürümü: `tweet-ema-ustu-kapanis-rsi-14-50-tarama-1842574480692150662` (05.10.2024; Ham, G1 açıldı, G2 görsel metni), `tweet-ema-5-14-34-55-ustunde-tarama-1847729477876666512` (19.10.2024; zincir, iki gönderi; Ham ve görsel metni), `tweet-ema-rsi14-cmf-obv50-gunluk-tarama-1848383646794731823` (21.10.2024; görsel metni), `tweet-ema-5-14-34-55-rsi-50-tarama-1852065846069465325` (31.10.2024; Ham ve görsel, açıldı), `tweet-ema-5-14-34-buy-signal-1898118783811698900` (07.03.2025; Ham ve görsel metni). CMF dönüşü varyantı: `tweet-ema-5-14-34-55-rsi-cmf-donus-1848806602553385447` (22.10.2024; Ham), `tweet-ema-rsi-cmf-donus-tarama-1851712038571249901` (30.10.2024; Ham; ETILR), `tweet-ema-rsi-cmf-donus-tarama-1851720332580966708` (30.10.2024; Ham, görsel metni; TSGYO), `tweet-ema-rsi-cmf-donus-tarama-1852063288533881329` (31.10.2024; Ham; GZNMI), `tweet-ema-rsi-cmf-kesisim-tarama-1847335598140358763` (18.10.2024; Ham, G1 açıldı, G2 ve G3 görsel metni: ARCLK, ARSAN). Hepsi Tansu'nun X gönderisidir (birinci el). EMA, RSI ve CMF taramasının çıktı listesinden başka içeriği olmayan tekrarları KURALLAR "Kural içermeyen notlar" listesindedir.
- Tansu'nun ifadesi (verbatim):
  - EMA14/34/55 (Ham, 09.10.2024): "Son kapanış EMA14, EMA34, EMA55'in üzerinde ve RSI(14) son gün 50'yi geçmiş olan hisseler: [GARAN, GENIL, INVEO, KGYO,MAGEN, MEPET, NUHCM, TUCLK, TUREX]". 14.10.2024 (Ham): aynı cümle, çıktı "INVEO, KGYO".
  - EMA5/14/34/55 tanımı (Ham, 05.10.2024): "Koşul" "Son gün kapanışı EMA5-14-34-55 üzerinde olsun (Son gün ortalamaların en üstüne atıyor)" "RSI 14 son gün > 50 olsun". 19.10.2024 (Ham): "Son gün koşulları sağlayan hisseler:" (ICUGS, SANFM) "Siz anladınız onu" ve yanıt "Bu hisselerde rsı14 > 50 aynı zamanda." Çıktı satırı (görsel, açıldı; 31.10.2024): "Günlük analizde son gün fiyatın EMA5-EMA14-EMA34-EMA55'den büyük ve RSI14>50 olması kriterini sağladı." (liste: BMSTL, BORLS, DAGHL, EUHOL, FRIGO, GZNMI, INVEO, KGYO, PAGYO, PASEU, SANFM, TDGYO). "para giriş çıkışlarına bakarsanız yarın bu listeden bir şeyler çıkar." (Ham, 31.10.2024). "şu para girişi hayra alamet değil:)" (Ham, 07.03.2025; grafik: Kapanış Fiyatı, EMA5, EMA14, EMA34, AL Sinyali; sembol yok).
  - CMF dönüşü (Ham, Tansu'nun alıntıladığı gönderi ve 22.10.2024): "ETILR Günlük analizde son gün fiyatın EMA5-EMA14-EMA34-EMA55'den büyük, RSI14>50 ve CMF son 3 gün pozitif, önceki 3 gün negatif kriterini sağladı." "Aşağıdaki sinyal geldi ama ETILR 'DEN UZAK DURUN!" "Tavana gitmiş etilr" "Yine de riskli ben işlem açmam" (Ham, 30.10.2024). "İşte bu önemli bir sinyal hocam. Buna bi bakın bence." (Ham, TSGYO). "Zaten tavan olmuş dikkat" (Ham, GZNMI). "Bence buradan bir tavan çıkar pazartesi yinede kontrollü gidin" (Ham, 18.10.2024).
  - EMA5 x EMA13 varyantı (görsel, açıldı): "Günlük analizde EMA5 EMA13 EMA14 / RSI14-21 50 ve CMF Koşulu"; "EMA5 EMA13'ü yukarı kesti, RSI21 50'nin üzerinde ve CMF koşulu sağlandı". 21.10.2024 çıktısı (görsel metni): CMF dönüş koşulunu "sağlayan hiç bir hisse yok".
- Tanım (Ham ve çıktı metni; yorum YORUM):
  1. Temel tarama (T1): son işlem günü kapanışı EMA'ların hepsinin üstünde (EMA14, EMA34, EMA55; sonraki sürümde EMA5 de) ve RSI(14) son gün 50'nin üstünde. Görsel (açıldı; ölçüm): TUREX'te kapanış 94,60, EMA14 93,36, EMA34 91,43, EMA55 87,24; RSI son iki barda 50'nin altından yaklaşık 53'e çıkar. EMA14 > EMA34 > EMA55 sıralaması örnekte vardır; Ham bu sıralamayı şart koşmaz (YORUM). RSI için EMA14/34/55 sürümü "50'yi geçmiş" der (YORUM: önceki gün RSI ≤ 50, son gün > 50, yani yukarı kesişim); EMA5/14/34/55 sürümü "RSI14 > 50" der (düzey). Hangisinin esas olduğu yazılı değil.
  2. CMF dönüşü (T2): T1 + CMF son 3 gün pozitif, önceki 3 gün negatif (CMF'nin eksiden artıya dönüşü; yeni sinyal, T1'den seyrek: 21.10.2024'te sıfır hisse, T1'de 5 sembol: INVEO, KGYO, MANAS, ULAS, ZRGYO). CMF koşulunun kuralı §54'tedir. "para giriş çıkışlarına" ifadesi bu CMF veya benzer bir akış göstergesi anlamına gelir (YORUM; Tansu hangi göstergeyi kastettiğini yazmaz).
  3. EMA5 x EMA13 varyantı (T3): EMA5, EMA13'ü yukarı keser, RSI21 > 50, "CMF koşulu" (koşulun ayrıntısı yok). EMA ve RSI koşulunun dar sürümü §57'dedir.
  4. Eleme ve tavan filtresi: Tansu sinyali otomatik almaz. ETILR için sinyal geldiği hâlde "UZAK DURUN!" der (neden yazılı değil; elle eleme). Kapanışı tavan olan hisseye girmez ("Yine de riskli ben işlem açmam"). GZNMI'de sinyal ve "Zaten tavan olmuş dikkat" aynı gündür (31.10, Ham). ETILR'de tavan sonradan oldu (30.10 yanıtı, Ham; sinyal 22.10); sinyal gününün tavan olduğu belli değil. YORUM: "sinyal günü tavan" okuması yalnız GZNMI'ye dayanır. YORUM: bu kişisel risk tercihidir; TASARIM §5.3 "Kapanışı tavan fiyatında olan gün (bir fiyat adımı toleransla) giriş yok." ile aynı sonucu verir.
  5. 07.03.2025 grafiğinde yalnız EMA5/14/34 çizili (EMA55 yok), "AL Sinyali" işareti var; sinyal koşulu yazılı değil.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA seti | 14 / 34 / 55 (09.10 ve 14.10.2024); 5 / 14 / 34 / 55 (05.10.2024 ve sonrası; 07.03.2025 grafiğinde 5 / 14 / 34) | Ham; görsel, açıldı |
| Fiyat koşulu | kapanış > her EMA | Ham; görsel, açıldı |
| RSI | periyot 14, eşik 50 (düzey veya yukarı kesişim: belirsiz) | Ham; görsel, açıldı |
| CMF dönüşü | son 3 gün > 0, önceki 3 gün < 0 | Ham |
| EMA kesişimi (T3) | EMA5, EMA13'ü yukarı keser; EMA14 de gösterilir; RSI21 > 50 (başlıkta RSI14-21 50) | görsel, açıldı |
| CMF periyodu, sıfır eşiği | yok | - |
| Zaman dilimi | günlük, son gün | Ham; görsel, açıldı |
| Stop, hedef, çıkış | yok | - |

- Belirsiz kalanlar: RSI için "geçmiş" kesişim mi düzey mi; CMF periyodu ve hesabı; para giriş çıkışı göstergesi; ETILR'yi eleme nedeni; T3'te "CMF koşulu" ve RSI14'ün de şart olup olmadığı (başlık "RSI14-21 50" der, mesaj yalnız RSI21'i söyler); Ham 05.10.2024'te EMA5'i sayar, aynı günün tarama çıktısı (görsel, açıldı) yalnız "EMA14, EMA34, EMA55" yazar (hangi kod çalıştı belli değil); EMA'ların kendi aralarındaki sıra; giriş, stop, hedef, çıkış. İlgili: §39, §40 (RSI 50 yukarı kesişimi), §23 (OBV teyidi), §55 (yalnız dizilim).
- Tansu'nun kanıtı: yok. Tarama listeleri ve tahmin cümleleri ("bir tavan çıkar") var; sonuç ölçümü yok.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLCV; EMA, RSI, CMF). Kural tarama düzeyindedir; çıkış yok.
- Kaynak güveni: Ham ve görsel birinci el; T1 ve T2 koşulu tam, CMF periyodu ve RSI sınırı belirsiz: orta-düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-ema14-34-55-ustu-rsi14-50-tarama-1844825767483482566` — Günlük tarama tekrarı (11.10.2024): “Son kapanış EMA14, EMA34, EMA55'in üzerinde ve RSI(14) son gün 50'yi geçmiş olan hisseler” (Ham).
  - `tweet-ema5-13-rsi21-cmf-3gun-donus-1846310706263871703` — 2024-10-15: “EMA5 > EMA13 olsun”, “RSI21 > 50 olsun”, “CMF SON 3 gün pozitif, ondan önceki 3 gün ise negatif olsun” (Ham). Okuma (YORUM): burada EMA koşulu düzey olarak yazılır.
  - `tweet-gunluk-coklu-ema-rsi14-tarama-1848807342705676791` — Okuma (YORUM): Çoklu EMA taramasında kişisel eleme uyarısı. Ham: "ETILR'den uzak durun!". Açılan G1: "fiyatın EMA5-EMA14-EMA34-EMA55'den büyük ve RSI14>50 olması".
  - `tweet-kapanis-ema-5-14-34-55-ustu-tarama-1842563290372940025` — Kural: Bu tarihli tarama yalnız kapanışın EMA5/14/34/55 üstünde olmasını ifade eder. Ham: "Koşul: Son gün kapanış fiyatının, EMA5-14-34-55 üzerinde olan hisseler." (05.10.2024). Okuma (YORUM): Başka kaynaklardaki RSI veya CMF koşulu bu alıntıya eklenmez.

## 57. EMA5 üstü EMA13 (RSI21 > 50) ve EMA5 üstü EMA14 (RSI14 > 50) sinyali ve taraması

- Kaynak: `tweet-ema-5-13-rsi-21-50-sinyal-kodu-1842513105089114147` (05.10.2024 10:32; Ham ve üç kod görseli; G1 ve G3 açıldı), `tweet-ema-kesisim-rsi-50-tarama-1842517514552541286` (05.10.2024 10:49; Ham ve görsel metni). İkisi de Tansu'nun X gönderisidir (birinci el).
- Tansu'nun ifadesi (verbatim): "ema5-13-21-34-55 fiyat grafiğine yazdırıldı." "Altta RSI21 > 50 ve RSI14>50 grafikleri oluşturuldu." "1. EMA5 > EMA13 ise ve RSI21 > 50 ise bu iyi bir sinyaldir." "2. EMA5 > EMA 14 ise ve RSI14 > 50 ise bu iyi bir sinyaldir." (Ham, 10:32; satırlar). "Koşul 1: EMA5, EMA13'ü yukarı kestiğinde ve RSI21, RSI50'nin üzerinde ise" "Koşul 2: EMA5, EMA14'ü yukarı kestiğinde ve RSI14, RSI50'nin üzerinde" ve "TARAMA SONUÇLARI: ASELS, ATAGY, BASCM, BORLS, BURCE, DAGI, ENSRI, GUBRF, SELGD, SEYKM, VAKBN" (Ham, 10:49). "EĞİTİM AMAÇLIDIR..." (Ham).
- Tanım (YORUM): iki koşul çifti. Koşul 1: EMA5 üstü EMA13 ve RSI(21) > 50. Koşul 2: EMA5 üstü EMA14 ve RSI(14) > 50. İlk gönderi "EMA5 > EMA13 ise" (dizilim) der; 17 dakika sonraki gönderi "yukarı kestiğinde" (kesişim) der: kesişim sürümü sonraki ve daha dar tanımdır (YORUM: tarama son gün kesişimini arar). Kod görseli (açıldı): EMA'lar `ewm(span, adjust=False)`; RSI `pandas_ta.rsi(length=14)` ve `length=21`; `yf.download(period="3mo", interval="1d")`. Çizimde RSI 50 kesikli çizgi. Örnek grafikler: AKBNK (kapanış 54,35; EMA5 55,42 < EMA13 57,83; RSI'lar 50 altında, yani sinyal yok; görsel, açıldı) ve ASELS (kapanış 61,15; EMA5 59,09 > EMA13 58,84 > EMA14 58,81; görsel metni).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA hızlı / yavaş | 5 / 13 (RSI21 ile), 5 / 14 (RSI14 ile) | Ham |
| RSI periyodu ve eşik | 21 ve 14; eşik 50 | Ham; kod, açıldı |
| Veri | günlük, 3 ay (yfinance) | kod, açıldı |
| İlgili uzun EMA'lar (çizim) | 21, 34, 55 | kod, açıldı |

- Belirsiz kalanlar: kesişim penceresi (yalnız son gün mü, son n gün mü); EMA21/34/55'in sinyaldeki rolü (yalnız çizim); EMA13 ile RSI21, EMA14 ile RSI14 eşleşmesinin nedeni; giriş, stop, hedef; sonuç. Benzer ama farklı tarama: §56 (fiyat tüm EMA'ların üstünde ve RSI14 > 50; EMA kesişimi aranmaz).
- Tansu'nun kanıtı: yok (tarama listesi, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük kapanış, EMA, RSI).
- Kaynak güveni: kural cümleleri birinci el (Ham); eşik ve çıkış yok, kanıt yok: orta-düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-ema5-13-14-kesisim-rsi-50-tarama-1845912796929708044` — 2024-10-14: “Koşul 1: EMA5, EMA13'ü yukarı kestiğinde ve RSI21, RSI50'nin üzerinde ise” ve “Para girişi koşulu karşılanmadı. Uyarayım” (Ham). Okuma (YORUM): EMA5/EMA14 ve RSI14 ikinci koşuldur.
  - `tweet-ema5-13-14-kesisim-rsi-gunluk-tarama-1846632708979507557` — 2024-10-16: “Koşul 2: EMA5, EMA14'ü yukarı kestiğinde ve RSI14, RSI50'nin üzerinde ise” ve “Hiç biri para girişi koşulunu sağlamadı” (Ham). Okuma (YORUM): EMA5/EMA13 ve RSI21 birinci koşuldur.
  - `tweet-ema5-13-14-kesisim-rsi-tarama-para-girisi-1846312518526161347` — 2024-10-15: “Bu tarama algoritmasında para girişi şartı yoktur.” ve “Para girişi ile sadece Marka listeden çıkıyor.” (Ham). Okuma (YORUM): EMA5/13-RSI21 ve EMA5/14-RSI14 taraması para girişi filtresinden ayrı tutulur.
  - `tweet-ema5-13-rsi21-ema5-14-rsi14-1845930687947305092` — 2024-10-14: “Ema5 > ema13 ve rsi21>50 beraber” ve “Ema5 > ema14 ve rsi14>50 beraber” (Ham). Kaynak stratejiyi “@fiboborsa stratejisidir.” diye niteler.
  - `tweet-ema5-ema13-14-kesisim-rsi50-tarama-1845728745040068881` — 2024-10-14: “Her koşul bağımsız çalışıyor. Koşulları sağlayan listeye giriyor.” ve “Para akışı da yazılacak koda” (Ham). Okuma (YORUM): iki EMA/RSI koşulu alternatif tarama kollarıdır; para akışı bu gönderide plandır.
  - `tweet-ema5-ema13-ema14-rsi-kesisim-1847035375870722341` — 2024-10-17: “Koşul 1: EMA5, EMA13'ü yukarı kestiğinde ve RSI21, RSI50'nin üzerinde ise” ve “Para akışı koşulu hiç birinde sağlanamadı” (Ham). Okuma (YORUM): ikinci kol EMA5/EMA14 ile RSI14 olarak anlatılır.
  - `tweet-ema5-ema13-kesisim-rsi50-taramasi-1844066093201228017` — 2024-10-09: “Koşul 1: EMA5, EMA13'ü yukarı kestiğinde ve RSI21, RSI50'nin üzerinde ise” ve “Bunlar sadece tarama sonucu.” (Ham). Okuma (YORUM): ikinci kol EMA5/EMA14-RSI14 olarak korunur.
  - `tweet-ema5-ema13-rsi21-saatlik-1847260753620832693` — 2024-10-18: “DGGYO: Saatlik analizde EMA5 EMA13'ü yukarı kesti ve RSI21 50'nin üzerinde” (görsel açıldı). Okuma (YORUM): günlük değil saatlik taramadır; SEKFK satırı EMA5/EMA14-RSI14 koludur.
  - `tweet-ema5-ema13-rsi21-saatlik-1847275831896207575` — 2024-10-18: “BSOKE: Saatlik analizde EMA5 EMA13'ü yukarı kesti ve RSI21 50'nin üzerinde” (görsel açıldı). Okuma (YORUM): saatlik tekrar; ULAS satırı EMA5/EMA14-RSI14 koludur.
  - `tweet-ema5-ema13-rsi21-saatlik-1847322036944708018` — 2024-10-18: “AYGAZ: Saatlik analizde EMA5 EMA13'ü yukarı kesti ve RSI21 50'nin üzerinde” (görsel açıldı). Okuma (YORUM): saatlik tekrar; GLRYH satırı EMA5/EMA14-RSI14 koludur.
  - `tweet-ema5-ema13-rsi21-tarama-1845381519147176179` — 2024-10-13: “ANGEN - Koşul 1: EMA5 > EMA13, RSI21 > 50” ve “BAGFS - Koşul 2: EMA5 > EMA14, RSI14 > 50” (görsel açıldı). Okuma (YORUM): çıktı düzey koşullarını yazar.
  - `tweet-ema5-kesisim-rsi-50-cift-kosul-1844835760110985511` — 2024-10-11: “Koşul 1: EMA5, EMA13'ü yukarı kestiğinde ve RSI21, RSI50'nin üzerinde” ve “Koşul 2: EMA5, EMA14'ü yukarı kestiğinde ve RSI14, RSI50'nin üzerinde olan hisseler” (Ham).
  - `tweet-gunluk-ema5-ema13-ema14-rsi-tarama-1847335233588253101` — Okuma (YORUM): Ham "EMA5>EMA13 ve RSI21>RSI50" ve "EMA5>EMA14 ve RSI14>RSI50" der. Açılan G1: "EMA5 EMA13'ü yukarı kesti ve RSI21 50'nin üzerinde". Görsel eşik 50 diye yazar; Ham RSI50 yazımını kullanır.
  - `tweet-ema5-12-ek-rsi21-50-filtre-1840168502914584969` — Okuma (YORUM): EMA5/12 varyantı, bölümün EMA5/13 ve EMA5/14 ayarlarından ayrı tutulur. “ema5-12 kriteri yanında rsi21-50 kriteri daha smooth bir alım satım yaptırıyor.” (Ham). Okuma (YORUM): RSI21/50, EMA5/12 kuralına ek teyit olarak anlatılır.
  - `tweet-ema5-12-rsi21-50-yukari-kesisim-tarama-1840151224462590233` — Okuma (YORUM): EMA5/12 varyantı, bölümün EMA5/13 ve EMA5/14 ayarlarından ayrı tutulur. “ema5, ema12'yi yukarı kesecek” ve “rsi21, rsi50'yi yukarı kesecek:)” (Ham). Okuma (YORUM): RSI50 sözü bu metinde aynen korunur; düzey/kesişim ayrımı uygulamadan önce açıklaştırılmalıdır.
  - `tweet-ema5-ema12-kesisim-rsi-teyit-1841949777786733054` — Okuma (YORUM): EMA5/12 varyantı, bölümün EMA5/13 ve EMA5/14 ayarlarından ayrı tutulur. “EMA5 ile EMA12 kesişimini RSI12>50 teyit ederek momentumu teyit ediyor.” cümlesi yanıtla “RSI21>50....” olarak düzeltilir (Ham). Okuma (YORUM): bu kayıtta teyit RSI21 düzeyidir.
  - `tweet-ema5-ema12-rsi21-50-tarama-1840484940858970581` — Okuma (YORUM): EMA5/12 varyantı, bölümün EMA5/13 ve EMA5/14 ayarlarından ayrı tutulur. “EMA5 ve EMA12 ile RSI21 > 50 taraması” (Ham). Okuma (YORUM): üç hisse çıktısı tarama sonucudur; gerçekleşmiş getiri değildir.
  - `tweet-ema5-ema12-rsi21-50-tarama-1844835177475768485` — Okuma (YORUM): EMA5/12 varyantı, bölümün EMA5/13 ve EMA5/14 ayarlarından ayrı tutulur. “Son gün EMA5 > EMA12 ve RSI21 > 50” (Ham). Okuma (YORUM): burada iki düzey koşulu yazılıdır; EMA kesişimiyle aynı cümle değildir.
  - `tweet-ema5-ema12-rsi21-tarama-1841958738141274137` — Okuma (YORUM): EMA5/12 varyantı, bölümün EMA5/13 ve EMA5/14 ayarlarından ayrı tutulur. “Ema5>Ema12 ve RSI21>50 taramasından çıkan tek hisse” ve “Pozitif uyumsuzluk cabası” (Ham). Okuma (YORUM): alıntılanan eski RSI12 ifadesine karşı ana gönderi RSI21 yazar.

## 58. EMA5 > EMA8 > EMA13 > EMA21 dizilimi + RSI düşen tepe çizgisi kırılımı + MACD sıfır üstü kesişim

- Kaynak: `tweet-ema-dizilim-rsi-kirilim-macd-1911425114245124453` (13.04.2025; Ham ve görsel, açıldı). Tansu'nun X gönderisidir (birinci el). Dizilim §55'teki son gün dizilim taramasının dört EMA'lı biçimidir (YORUM); RSI ve MACD koşulları bu kayıtta eklenir.
- Tansu'nun ifadesi (verbatim): "EMA5 > EMA8 >   EMA13 > EMA21" "RSI kırılımı 30   ÜSTÜNDEN geldi (60.29)" "MACD sinyali pozitif" "MACD konumu 0 üstü" "MACD kesişim noktası 0 üstü" ":)" "Mis" (Ham; satırlar, boşluklar Ham'daki gibi). Görsel panelleri (görsel, açıldı): EMA5/8/13/21 (mum grafiği); "RSI ve Trend Kırılımı" (RSI, "RSI Tepeleri", "Düşen Tepe Trend"); "MACD" (MACD, MACD Signal, MACD Histogram); "Hacim (Volume)".
- Tanım (YORUM): beş koşulun birleşimi. (1) EMA5 > EMA8 > EMA13 > EMA21. (2) RSI panelinde son iki RSI tepesinden geçen düşen çizgi yukarı kırılır; 30 ÜSTÜNDEN = RSI kırılımdan önce aşırı satıma (30) inmemiştir, kırılım orta bölgeden gelir; RSI son değeri 60,29. Görselde çizgi iki RSI tepesini bağlar ve son bar çizginin üstündedir (görsel, açıldı; RSI ≈ 60, kesikli 30 ve 70 çizgileriyle uyumlu). (3) MACD çizgisi sinyalin üstünde. (4) MACD çizgisi sıfırın üstünde. (5) MACD ve sinyal kesişiminin gerçekleştiği nokta sıfırın üstündedir (güçlü bölgede oluşan al kesişimi). Görselde MACD ve sinyal son barlarda sıfırın üstündedir, histogram küçük pozitiftir (görsel, açıldı).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA dizilimi | 5 > 8 > 13 > 21 | Ham; görsel, açıldı |
| RSI düşen tepe çizgisi | iki tepe, kırılım | görsel, açıldı |
| RSI son değeri | 60,29 | Ham |
| RSI kırılım öncesi taban | 30 üstünde | Ham (YORUM: aşırı satım yok) |
| MACD | sinyalin ve sıfırın üstünde; kesişim sıfır üstünde | Ham |
| RSI ve MACD periyotları | yok | BELİRSİZ |

- Belirsiz kalanlar: 30 ÜSTÜNDEN geldi ifadesinin anlamı; RSI tepelerinin seçimi (pivot genişliği); RSI ve MACD periyotları; hacim şartı (panel var, koşul yok); giriş, stop, hedef; sonuç. İlgili: §41 (RSI düşen trend çizgisi kırılımı), §9 (RSI uyumsuzluğu).
- Tansu'nun kanıtı: yok (tek örnek, sembol yok, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: dizilim, RSI ve MACD evet; RSI üzerinde trend çizgisi kırılımı kısmen (çizgi kuralı yok).
- Kaynak güveni: koşul listesi birinci el (Ham); eşikler ve çizgi yöntemi yok: orta-düşük. Hazırlık K.

## 59. EMA5 ve EMA10'un EMA20'yi birlikte kesmesi + MACD + OBV artışı + RSI(14) 50 yukarı kesişimi (günlük AL taraması)

- Kaynak: `tweet-ema-kesisim-macd-obv-rsi50-1840777067882787015` (30.09.2024; Ham ve iki görsel, G1 açıldı, G2 görsel metni; ilk sürüm), `tweet-ema-macd-rsi-obv-tarama-1847008515014922537` (17.10.2024; Ham ve iki görsel; G1 açıldı; iki gönderilik zincir), `tweet-ema-macd-rsi-obv-tarama-1847012312911057085` (17.10.2024; Ham, görsel metni), `tweet-ema-macd-rsi-obv-al-tarama-1851719680052072481` (30.10.2024; Ham, görsel metni). Aynı bot mesajı `tweet-ema-rsi14-cmf-obv50-gunluk-tarama-1848383646794731823` içinde de görünür (21.10.2024; §56). Hepsi Tansu'nun X gönderisidir (birinci el). YORUM: dört not aynı kuralın iki sürümüdür; MACD koşulu sürümlerde farklıdır (aşağıda).
- Tansu'nun ifadesi (verbatim):
  - 30.09.2024 (Ham; satırlar): "EMA5 ve EMA10, EMA20'yi anda anda kessin" "MACD 0'a çok yakın olsun" "OBV artsın" "RSI1450'yi yukarı kessin" "Sağlayan tek hisse ANELE ve TDGYO" "Hayırlı uğurlu olsun." "Parayı kazananın bi kahvesini içerim:)". Görsel başlığı: "TDGYO.IS İçin Alış Sinyalleri (EMA Kesişimi, MACD, RSI ve OBV)" (görsel, açıldı).
  - 17.10.2024 (Ham; satırlar): "Son gün;" "EMA5 > EMA20" "EMA10 > EMA20" "EMA5 ve EMA10, EMA20'yi yukarı kesmiş" "MACD > MACD Sinyal Çizgisi:" "RSI14 > 50" "RSI14 önceki gün ≤ 50" "OBV (On Balance Volume) artışı: Son 5 günlük OBV değişimi pozitif". Yanıt: "P A R A  A K I Ş I N I  K O N T R O L  E D İ N" (Ham). "Aralarından sağlam bir kaçını seçip sayısını azaltacağım." (Ham).
  - 30.10.2024 (Ham): "Aslolan para girişidir." "Para yoksa gerisine bakmaya gerek yok." Bot metni (görsel metni): "Günlük taramada son kapanış günü fiyatın EMA5'den büyük olup, EMA5-10-20 MACD RSI14-50 VE OBV50 koşullarını sağlayıp AL sinyali veren hisseler".
- Tanım (Ham; yorum YORUM; YORUM: anda anda = aynı anda, RSI1450 = RSI14 ve 50):
  1. Aynı gün EMA5 ve EMA10, EMA20'yi yukarı keser (EMA5 > EMA20, EMA10 > EMA20; Ham, 17.10.2024).
  2. MACD: 30.09.2024 sürümünde MACD "0'a çok yakın" olmalıdır (eşik yok); 17.10.2024 sürümünde MACD > MACD sinyal çizgisidir (MACD ayarı yazılı değil; YORUM: standart 12-26-9). İki sürüm birbirini dışlayabilir; hangisinin esas olduğu yazılı değil.
  3. RSI14 > 50 ve önceki gün RSI14 ≤ 50 (50'nin yukarı kesilişi; §39 ve §40'taki RSI 50 kesişimiyle aynı eleman).
  4. OBV artıyor: 17.10.2024 sürümünde son 5 günlük OBV değişimi pozitif (30.09.2024'te pencere yok; §23'teki OBV trend onayıyla ilgili).
  5. Bot metni kapanışın EMA5'in üstünde olmasını da ister (görsel metni). Para girişi (OBV) Tansu'nun ilk bakılacak koşuludur: "Para yoksa gerisine bakmaya gerek yok" (Ham); bu, koşul sırası değil bakış önceliğidir (YORUM).
  6. Görsel (TDGYO, 30.09.2024, açıldı): üç EMA çizgisi son barlarda iç içe (fiyat 10-11 TL), RSI14 son barda yaklaşık 53 ve 50'yi yukarı keser, MACD ve sinyal sıfırın hemen altında (yaklaşık -0,05), OBV yükselir. ANELE grafiği aynı şablondadır (görsel metni). Bot mesajlarının saatleri görselde 17:17 ile 22:29 arasındadır (görsel metni); giriş fiyatı ve günü yazılı değil.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA | 5, 10, 20 (kapanış); EMA5 ve EMA10, EMA20'yi aynı anda yukarı keser | Ham; görsel, açıldı |
| RSI | periyot 14; eşik 50; önceki gün ≤ 50 | Ham; görsel, açıldı |
| OBV | son 5 günlük değişim > 0 (30.09.2024: "artsın", pencere yok) | Ham |
| MACD | 30.09: sıfıra yakın; 17.10: MACD > sinyal; ayar ve eşik yok | Ham |
| Kapanış | EMA5'in üstünde | görsel metni |
| Stop, hedef, çıkış | yok | - |

- Belirsiz kalanlar: "aynı anda" kesişimin aynı bar mı n bar penceresi mi olduğu; "yukarı kesmiş" kesişimin son günde mi yoksa son birkaç günde mi olduğu; "0'a çok yakın" eşiği; MACD'nin iki tanımı; bot metnindeki "OBV50" etiketinin Ham'daki "5 günlük OBV değişimi" ile ilişkisi (YORUM: 50 bir eşik ya da OBV ortalaması olabilir; kod görülmedi); "sayısını azaltacağım" cümlesi sinyal sayısını mı strateji sayısını mı azaltır (YORUM: "her strateji için" dediği için strateji sayısı); giriş, stop, hedef, çıkış. Tarama "tek hisse ANELE ve TDGYO" (30.09.2024) ve en çok üç hisse verir: koşulların birlikte çok sıkı olduğunun göstergesi (YORUM).
- Tansu'nun kanıtı: yok. Yalnız tarama çıktıları: 30.09.2024 ANELE, TDGYO; 17.10.2024 EGSER, INVEO, KGYO; 21.10.2024 INVEO, KGYO; 30.10.2024 INVEO, KGYO, MERIT. Sonrasında sonuç ölçümü yok; "Parayı kazananın bi kahvesini içerim" bir vaattir, kanıt değil.
- Günlük bedava veriyle uygulanabilir mi: evet (günlük OHLCV; EMA, MACD, RSI ve OBV hesaplanır). Koşul listesi tamdır; çıkış yoktur.
- Kaynak güveni: Ham ve görsel birinci el; koşul listesi tam; MACD ve OBV50 belirsiz, çıkış yok: orta. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-gunluk-ema-macd-rsi-obv-tarama-1848806438212084143` — Okuma (YORUM): Günlük birleşik taramanın çıktı başlığı. Açılan G1: "fiyatın EMA5'den büyük olup, EMA5-10-20 MACD RSI14-50 VE OBV50 koşullarını sağlayıp AL sinyali veren hisseler".
  - `tweet-obv-macd-rsi50-ema-kesisim-tarama-1840495500937564321` — `tweet-obv-macd-rsi50-ema-kesisim-tarama-1840495500937564321` (2024-09-29): Ham: "MACD sıfıra yakın olsun"; "RSI Son gün50'yi yukarıya kessin"; "EMA5 ve EMA10 son gün aynı anda EMA20'yi yukarıya kessin." Okuma (YORUM): son günlerde para girişiyle birlikte aranan birleşik taramadır.

## 60. EMA5 ve EMA5'in EMA10'u kesişimi + CCI(20) ±100 (THYAO kodu)

- Kaynak: `tweet-ema-5-10-kesisim-cci-20-seviyeleri-1760742464309350866` (22.02.2024; Ham ve üç kod görseli; G1 ve G3 açıldı). Tansu'nun X gönderisidir (birinci el). Aynı gün BRSAN için EMA'nın EMA'sı ayrışma uyarısı §34'te kısa kayıttır.
- Tansu'nun ifadesi (verbatim): "#THYAO'da neler oluyor" "Kodlayalım" (Ham; iki satır). Kod yorumları (görsel, açıldı): "EMA'nın kendi 10 günlük EMA'sı", "Kesişim noktalarını ve sinyalleri belirle", "Aşırı alım seviyesi" (100), "Aşırı satım seviyesi" (-100).
- Tanım (kod, görsel, açıldı): `ema1` = fiyatın 5 günlük EMA'sı (`alpha = 2/(n+1)`, `adjust=False`). `ema2` = `ema1`'in 10 günlük EMA'sı (fiyatın EMA10'u değil). `al = 1` eğer `ema1 > ema2` ve önceki barda `ema1 <= ema2` (yukarı kesişim). `sat = 1` eğer `ema1 < ema2` ve önceki barda `ema1 >= ema2` (aşağı kesişim). CCI: tipik fiyat `TP = (High + Low + Close)/3`; `CCI = (TP - SMA20(TP)) / (0,015 × ortalama sapma)`, pencere 20; `CCI_EMA20` = CCI'nın EMA'sı (span 20). Grafikte ±100 yatay çizgi. Bu iki parça ayrı hücrelerdir; CCI ile EMA kesişimini bağlayan bir giriş koşulu yoktur.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| ema1 | EMA5 (fiyat) | kod, açıldı |
| ema2 | EMA10 (ema1 üzerinde) | kod, açıldı |
| CCI pencere | 20; sabit 0,015 | kod, açıldı |
| CCI seviyeleri | +100 aşırı alım, -100 aşırı satım | kod, açıldı |
| CCI yumuşatma | EMA20 (span 20) | kod, açıldı |

- Belirsiz kalanlar: CCI'nın al/sat kararındaki rolü (filtre mi, çıkış mı); ±100 çizgisinin geçiş yönü; çıkış, stop, hedef; sonuç. Kod görselleri iki ayrı parçadır (G1, G3).
- Tansu'nun kanıtı: yok (tek hisse, grafik, sonuç yok).
- Günlük bedava veriyle uygulanabilir mi: evet (OHLC günlük).
- Kaynak güveni: kod birinci el; kural yok, güven düşük. Hazırlık K.

## 61. Momentum teyit listesi: EMA, RSI 50, MACD, ADX ve hacim ile düşüş ve dönüş teyidi (AGROT, BYDNR)

- Kaynak: `tweet-ema-rsi-macd-adx-dusus-teyidi-1778359964634915038` (11.04.2024; Ham, iki gönderilik zincir; G1 açıldı), `tweet-ema-rsi-macd-hacim-zayif-teyit-1911423210484023697` (13.04.2025; Ham, görsel açıldı). İkisi de Tansu'nun X gönderisidir (birinci el). Birinci notun Ham metni iki gönderide de yarım kalır (arşiv kesmesi: "Ayrıca 5 günlük ve", "YTD").
- Tansu'nun ifadesi (verbatim): AGROT: "ilk bakışta hisse yatay bir piyasaya girmiş gibi görünüyor. 20 günlük EMA (15.64) destek olarak çalışmış. Soru, orayı kıracak mı kırmayacak mı? Bana kalırsa aşağıya kırmak üzere. Hisse momentum kaybediyor. RSI'50'nin altına düştü düşecek."; "20 günlük üssel hareketli ortalamaları da sinyali vermiş. para girişinde de bir düşüş gözlemleniyor aynı şekilde MACD-AS de yönünü aşağıya çevirmiş. ADX de aşağı trendin kuvvetlendiği sinyalini vermiş." (Ham). BYDNR: "EMA'lar (5-8-13-21) sıralı ve fiyat EMA'ların altında veya tam dibinde"; "Her yükseliş denemesi EMA21 (kırmızı) tarafından aşağı itiliyor"; "RSI düşen bir kanal çizgisi ile kırılmaya çalışmış ancak," "Kırılım yeni olmuş, teyidi zayıf. RSI seviyesi hala 50'nin altında"; "MACD çizgisi hâlâ sıfırın altında. Negatif bölgede MACD-Sinyal kesişimi zayıf sinyaldir."; "RSI kırılımına eşlik eden belirgin bir hacim artışı yok." "Güçlü dönüşler genellikle artan hacimle gelir."; "İlk sıçrama değil, ikinci teyit dalgası yatırım için daha güvenlidir."; "Stop-loss seviyesi net belirlenmeli" (Ham).
- Tanım (Ham; yorum YORUM): iki yönlü teyit listesi. Düşüş teyidi (AGROT): EMA20 destek kırılımı (fiyat EMA20'nin altına kapanır); RSI 50'nin altına iner; kısa EMA (5 günlük) ve EMA20 sinyali; para girişi azalır (gösterge adı yok, YORUM: OBV ya da CMF); MACD (histogram ya da sinyal) aşağı döner; ADX aşağı trendin güçlendiğini gösterir. Dönüş teyidi (BYDNR, düşen trendden dönüş): fiyat EMA5/8/13/21 kümesinin üstüne çıkar (EMA21 direnç olmaktan çıkar); RSI düşen tepe çizgisini kırar ve 50'nin üstüne geçer; MACD sıfırın üstüne geçer, histogram güçlenir; RSI kırılımına hacim artışı eşlik eder. Eksik teyit = erken giriş riski; Tansu bekleme ve "ikinci teyit dalgası" ister, stop net belirlenmeli der. Bu bir kontrol listesidir; kaç şartın yeteceği yazılı değil.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA | 20 (AGROT; 15,64 örnek değer); 5-8-13-21 (BYDNR) | Ham; görsel, açıldı (BYDNR lejantı) |
| RSI | eşik 50; düşen tepe trend çizgisi kırılımı | Ham; görsel, açıldı |
| MACD | sıfır çizgisi; MACD-sinyal kesişimi | Ham; görsel, açıldı |
| ADX | eşik yok (Ham: "aşağı trendin kuvvetlendiği") | Ham |
| Hacim | RSI kırılımında artış; eşik yok | Ham |
| Periyotlar (RSI, MACD, ADX), stop, hedef | yok | - |

- Belirsiz kalanlar: "para girişi" göstergesi; kaç teyidin yeterli olduğu; "RSI kırılımı" için ölçü; hacim artışı eşiği; AGROT'ta 5 günlük EMA'nın hangi çizgiyle kesiştiği (Ham yarım); stop ve hedef.
- Tansu'nun kanıtı: yok (iki seçilmiş grafik, sonuç yok). BYDNR gönderisi yapılandırılmış, yapay zekâ yardımlı gibi görünen bir yorumdur (#Python etiketi, emojili başlıklar; YORUM).
- Günlük bedava veriyle uygulanabilir mi: evet (EMA, RSI, MACD, ADX, hacim günlük OHLCV'dendir); trend çizgisi ve eşikler tanımsız olduğu için kural yarım. İlgili: §39 (RSI 50 + OBV), §43 (trend filtresi).
- Kaynak güveni: Ham ve görsel birinci el; kural sözlü, eşiksiz: düşük. Hazırlık X.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-duran-varlik-yatirim-fiyat-endeks-1956635605867053409` — FROTO dönüş örneği (16.08.2025): “Parabolic SAR noktalarının fiyatın altına geçmesi” ve “artan işlem hacmi trend dönüşünü teyit etmiş.” (Ham). Okuma (YORUM): teknik teyit, kaynakta temel yatırım analiziyle birlikte anlatılır; seçilmiş geçmiş örnektir.
  - `tweet-ema50-hacim-rsi-macd-filtreleri-1949509666456650215` — 2025-07-27: “Örneğin 5 gün ortalamasına göre hacim > 1.5 kat mı?” ve “RSI > 50 mi?” (Ham). Okuma (YORUM): EMA50 yaklaşımı için örnek teyit sorularıdır. Kaynak son 20 gün düşenini test etme ve MACD kesişimi/histogram pozitifleşmesini ayrıca sorar.
  - `tweet-hacim-artisi-cmf-teyidi-1940118051640197615` — Okuma (YORUM): Hacim ve para girişi birlikte değerlendirilen örnek. Ham: "Son gün hacim bir önceki gün hacminin 1.5 katına çıkmış, para girişi pozitif". 1,5 kat örnek ölçümüdür.
  - `tweet-mean-reversion-breakout-ema-teyit-1775921178172870687` — Birleşik teyit fikri: "Hissenin mean reversion ve maximum drawdown noktasına bakıp, momentum breakout’unu hesaplayıp EMA’lardan teyit alıp" (Ham, 04.04.2024). Okuma (YORUM): bu kısa ifade ek teyit yaklaşımıdır; kontrol listesine hesaplanmış yeni eşik eklemez.
  - `tweet-mean-reversion-ema100-teyit-1775279648693510563` — KFEIN bekleme örneği: "100EMA 115TL'ye gelmeden pozisyon açmam" (Ham, 02.04.2024). Risk ifadesi: "115 desteğini kırarsa maalesef 86'lara kadar çekilebilir". Okuma (YORUM): seviyeler bu örneğe aittir; EMA100 bütün hisseler için zorunlu teyit yapılmaz.
  - `tweet-mean-reversion-gann-coklu-teyit-1775957765980127737` — KFEIN çoklu düşüş teyidi: "mean reversion hala dönüş vermedi, düşüş teyitli, breakout hala dönüş vermedi, düşüş teyitli, gann ayı piyasası teyitli" (Ham, 04.04.2024). Okuma (YORUM): bu tarihli gözlem göstergeler birlikte dönmeden bekleme örneğidir.
  - `tweet-momentum-listesi-coklu-teyit-1993448157163012287` — `tweet-momentum-listesi-coklu-teyit-1993448157163012287` (2025-11-25, Ham): "5-6 farklı momentum ve trend takip stratejisi ile teyit alınmış olacak. Güvenli olur sanırım."
  - `tweet-money-flow-momentum-breakout-filter-1892688848661967251` — `tweet-money-flow-momentum-breakout-filter-1892688848661967251` (2025-02-20): Ham: "Hocam hisseye para girmiyor ise ve momentum alanında değilse sürdürülebilir bir çıkış O L M A Z…"
  - `tweet-ortalama-kirilim-hacim-momentum-1990846239147995402` — `tweet-ortalama-kirilim-hacim-momentum-1990846239147995402` (2025-11-18): Ham: "Ortalamalar bir bir kırılmış momentum artmış hacim mum gövderlerini destekliyor, takasını beğenmedim ama kısa vadeli girilip çıkılır." Okuma (YORUM): açılan grafik tek örnektir; takas çekincesi korunur.

## 62. EMA sıkışması sonrası hacimli kapanışla al: yükselen destek teması, PSAR, MACD eğimi ve trend çizgisi kırılımı teyitleri

- Kaynak: `tweet-ema-sikismasi-hacimli-kapanis-al-1953221966678376915` (06.08.2025; Ham, görsel açıldı: AKSUE), `tweet-ema-squeeze-downtrend-break-checklist-1953173142861414759` (06.08.2025; Ham, görsel açıldı, görselde metin yok), `tweet-ema-sikisma-psar-trend-temas-hacim-1956041277096546504` (14.08.2025; Ham, görsel açıldı), `tweet-ema-sikisma-yukselen-destek-1957935566827221201` (19.08.2025; Ham, görsel açıldı: FRIGO), `tweet-ema-sikisma-macd-histogram-egim-1957958199425818842` (20.08.2025; Ham, görsel açıldı), `tweet-ema-sikisma-trend-kirilim-sar-1982687024344949140` (27.10.2025; Ham, görsel açıldı). Hepsi Tansu'nun X gönderisidir (birinci el). Sıkışma dedektörü: §1; EMA50/100/200 sıkışma örneği: §25; BULL/BEAR/CONFLICT sayacı: §2.
- Tansu'nun ifadesi (verbatim): "Al strateji, ema sıkışması sonrası fiyat hacim ile ema'ların üzerinde kapansın, sonra otur izle...Buradaki detay, sıkışmayı erken yakalarsan erken pozisyon alırsın. Bazen sıkışma günler sürer. Artık yakalama şansın tarama kabiliyetinle doğru orantılıdır." (Ham, 06.08.2025). "Bu yapıyı bulun" "EMA'lar sıkışsın" "PSAR'lar fiyat altına insin" "Yükselen trende temas edip tepki alsın" "Hacim artsın" "Falan filan" (Ham, 14.08.2025; satırlar). "üssel ortalamalar sıkışmış trend yukarı kırılmış psarlar neredeyse olduğu yerde" (Ham, 27.10.2025). "EMA sıkışması şahane düşeni kırmış hacim artmış stoc güzel kesmiş trend güşlenmiş momentum artmış vs vs" (Ham, 06.08.2025; "emin olmamakla ve teknik detaya bakmamakla beraber" ön sözüyle). "EMA sıkışması da var yükselen trendden destek alacak mı göreceğiz, MACD olumsuz." (Ham, 19.08.2025). "yükselen desteğine derede ise temas etmek üzere ema sıkışmış histo eğimi artmaya başlamış 0 altında" (Ham, 20.08.2025). Görsel başlıkları (görsel, açıldı): "Son 10 günde BAŞLAYAN sıkışma: 2025-08-12 → 2025-08-19 | Çekirdek: 6 bar | Toplam: 126 bar (+/- 120/35)" (FRIGO); "En Uzun EMA Sıkışması ve Trendline (2025-10-23)" ve "Kapanış: 17.04 | Trendline: 17.04"; "Yükselen Destek Teması - İlk Temas: 2025-06-19, Son Temas: 2025-07-31" ve "Son Gün Fiyatı: 18.84 | Trend Çizgisi Son Gün Değeri: 18.21" (AKSUE).
- Tanım (Ham; yorum YORUM): yapı üç katmandır. (1) Sıkışma: kısa-orta-uzun EMA'lar birbirine yaklaşır (örneklerde EMA50/100/200; FRIGO'da EMA50/100); tarama "Son 10 günde BAŞLAYAN sıkışma" ve "En Uzun EMA Sıkışması" gibi çıktılar verir (görsel başlıkları). (2) Giriş ("Al strateji"): sıkışma sonrası fiyat hacimle birlikte EMA'ların üstünde kapanır; sonra pozisyon tutulur ("otur izle"; çıkış yazılı değil). Erken yakalama erken giriş demektir; sıkışma günlerce sürebilir. (3) Teyitler (kontrol listesi, kaç tanesi şart olduğu yok): SAR'lar (SAR, Fast SAR, Slow SAR) fiyatın altına iner ya da kırılımda yerinde durur; fiyat yükselen trend çizgisine temas edip tepki alır ("Son Temas" işareti); hacim artar; MACD histogram eğimi artar (sıfırın altında bile); düşen trend çizgisi hacimle kırılır, stokastik yukarı keser, momentum artar. Uyarı: "MACD olumsuz" (FRIGO) bekleme nedenidir; momentum squeeze negatif ve büyüyorsa bull aksiyon yoktur (§2, `tweet-ema-sikisma-momentum-conflict-2045457969215631398`). Tansu hiçbir gönderide sonuç ya da hedef vermez.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA seti | 50/100/200 (AKSUE, PSAR ve trend kırılımı örnekleri); 50/100 (FRIGO, MACD örnekleri) | görsel, açıldı |
| Sıkışma taraması | son 10 gün içinde başlayan; çekirdek 6 bar; toplam 126 bar; "(+/- 120/35)" anlamı yok | görsel, açıldı |
| SAR | SAR, Fast SAR, Slow SAR (AF ayarı yok) | görsel, açıldı |
| Hacim | hacim artışı; Volume EMA 20 çizgisi | Ham; görsel, açıldı |
| Sıkışma eşiği, hacim eşiği, temas toleransı | yok | - |
| Stop, hedef, çıkış | yok | - |

- Belirsiz kalanlar: sıkışma ölçüsü ve eşiği (§1 ve KURALLAR §3'teki ratio formülü ile eşleşip eşleşmediği); "hacimle" kaç kat; "üzerinde kapansın" hangi EMA'ların hepsi; teyitlerden kaçı gerekli; SAR ayarları; trend çizgisi tanımı (A §12); "(+/- 120/35)" ve "Çekirdek" anlamı; 27.10.2025 örneğinde kapanış çizgi değerine eşittir (17,04 = 17,04), "yukarı kırılmış" sınırdadır. Çıkış, stop, hedef yok.
- Tansu'nun kanıtı: yok. Seçilmiş örnek grafikleri; AKSUE'de sıkışmadan sonra fiyat 14'ten 18-20 bandına çıkmıştır (görsel, açıldı; sonuç ölçülmemiş). Kural yeniden üretilebilir bir sistem değildir.
- Günlük bedava veriyle uygulanabilir mi: evet (EMA, SAR, MACD, hacim günlük OHLCV'dendir). Giriş cümlesi kodlanabilir, eşikler varsayım gerektirir; trend çizgisi ve stokastik tanımsızdır.
- Kaynak güveni: Ham ve görsel birinci el; kural sözlü, eşiksiz, çıkışsız: orta-düşük. Hazırlık K.
- Modül 1'de kullanımı: KURALLAR §3 (hacim süzgeci, gösterge ve trend teyitleri, üçgen hedefi).
- Ek kaynaklar (X arşivi, 16.10):
  - `tweet-qullamaggie-tarzi-hacimli-breakout-tarama-1979546907505545421` — Okur sorusuna cevap (18.10.2025); genel kırılım kuralı, EMA sıkışmasına özel değil: "Breakout anında hacmin ortalamanın en az 2-3 katı olması lazım." (Ham). Kırılma kapanışa bakar: "Gün içi kırılma yetmez, kapanış o seviyenin üstünde olmalı." (Ham). Parametre: hacim eşiği = hacim ortalamasının en az 2-3 katı (Ham; ortalamanın penceresi ve türü yok); kırılım ölçüsü = kapanış, gün içi değil (Ham)
  - `tweet-ema-sikismasi-ucgen-kirilim-hacim-1954300245707497649` — ECILC örneği (09.08.2025): üç şey birlikte, "üssel ortalama sıkışması, simetrik üçgen sıkışması ve hacimle teyit" (Ham). Hacim: "Kırılma barında hacim, alt penceredeki ortalama çizgisinin üzerine çıkıyor" (Ham). Hedef: "hedefi de üçgenin taban yüksekliğini yukarı projekte ederek düşünmek mantıklıdır." (Ham). Görsel (görsel, açıldı): "ECILC | breakout: 2025-08-07", EMA50, EMA100, EMA200 (görsel metni). Parametre: EMA seti = 50/100/200 (Ham ve görsel metni); hedef = üçgenin taban yüksekliği yukarı projekte edilir (Ham; "taban yüksekliği"nin ölçüsü ve projeksiyonun başladığı fiyat yok, YORUM)
  - `tweet-ema-sikisma-yukselen-ucgen-tarama-1952086678639669635` — Yükselen üçgen taraması adımları (03.08.2025; THYAO.IS görseli): "kısa ve orta vadeli hareketli ortalamalar (örneğin 10 ve 20 günlük EMA) birbirine yakınsa" sıkışma bölgesidir; "En az iki tane birbirine yakın tepeler (yatay direnç seviyesi) ve üç veya daha fazla yükselen dip aranır." ve "Eğer tepeler sabit (yani birbirine çok yakın) ve dipler artıyorsa, bu bir yükselen üçgen formasyonudur." (Ham). Görsel başlığı: "THYAO.IS - Yükselen Üçgen Bölgeleri" (görsel metni). Parametre: tepe sayısı ≥ 2, dip sayısı ≥ 3 (Ham); "birbirine yakın" ölçüsü ve zaman dilimi yok ("belirlenen zaman dilimleri", Ham; YORUM)
  - `tweet-multi-psar-below-price-condition-1951615287326814530` — `tweet-multi-psar-below-price-condition-1951615287326814530` (2025-08-02): Ham: "temel felsefe psarların aşağıda olması gerekliliği." Okuma (YORUM): yazar PSAR konusunda uzman olmadığını ayrıca belirtir; çoklu PSAR için yön teyidi olarak okunur.

## 63. EMA12'nin EMA144 ve EMA169 tünelini yukarı kesmesi: giriş taraması ve EMA13 > 144 > 169 dizilim taraması

- Kaynak: `tweet-ema12-144-169-tunel-kesisim-1783135314036376019` (24.04.2024; Ham), `tweet-ema12-ema144-169-yukari-kesisim-tarama-1839566564107919502` (27.09.2024; Ham, alıntılanan bot gönderisi), `tweet-ema13-144-169-dizilim-tarama-1845923939736080720` (14.10.2024; Ham, @idealborsa'ya yanıt; üst gönderi notta yok). Hepsi Tansu'nun X gönderisidir (birinci el; görsel yok). Aynı EMA seti: §34 (12-144-169 optimizasyon sorusu, Vegas tüneli DOAŞ geri testi).
- Tansu'nun ifadesi (verbatim): "Yeni bir strateji yapalım mı :) Kısa vadeli trade için, 12EMA'nın , 144EMA ve 169EMA'yı (Bu ikisi bir tünel oluşturur) yukarı kesmesi ile güzel fırsatlar yakalanabilir. Python, Matrix ve Tradingview kodlarını yazalım haydi :)" (Ham, 24.04.2024). Tarama (alıntılanan gönderi): "12 günlük EMA'nın 144 ve 169 günlük EMA'yı yeni yukarı kestiği hisseler:" EGEPO ve "Bakın derim :)"; Tansu'nun yorumu: "Senide mi yakaladık ya;)" (Ham, 27.09.2024). "Çok basit bir stratejisi var" "ema13 >ema144>ema169" "Bu tabi her hisse için optimize olursa çok daha iyi giriş çıkış noktaları verir." "Tarama için yukarıdaki ideal." "Bununla tavan hisseler bulduk." (Ham, 14.10.2024; satırlar).
- Tanım (Ham; yorum YORUM): günlük barda iki tarama. T1 (giriş sinyali): EMA12, hem EMA144'ü hem EMA169'u yeni yukarı keser ("yeni" = son gün, YORUM); EMA144 ve EMA169 yakın iki çizgidir (tünel). T2 (durum taraması): EMA13 > EMA144 > EMA169, yani kısa EMA tünelin üstünde ve tünel sıralıdır; kesişim değil dizilimdir. Tansu T2'yi tarama için "ideal" sayar ve optimize edilirse giriş ve çıkış noktalarının daha iyi olacağını söyler. Çıkış kuralı yok. Hisse bazlı optimizasyon bu notlarda hedeflenir (§34, E K29 ve E K20 ile birlikte okunur; karar Levent'te bekliyor).
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| EMA seti (T1) | 12, 144, 169 (günlük) | Ham |
| EMA seti (T2) | 13, 144, 169 | Ham |
| Kesişim | EMA12 ↑ EMA144 ve EMA12 ↑ EMA169; "yeni" | Ham (yeniliğin penceresi: YORUM) |
| Zaman çerçevesi | günlük ("12 günlük EMA"); "Kısa vadeli trade" | Ham |
| Stop, hedef, çıkış | yok | - |

- Belirsiz kalanlar: EMA12 ile EMA13 farkı (iki gönderi iki farklı kısa EMA söyler; biri yazım farkı olabilir, YORUM); kesişimin her iki EMA'yı aynı günde mi kesmesi; "yeni" penceresi; çıkış, stop ve hedef; "güzel fırsatlar" ölçülmemiş. Tansu'nun kodu (Python, Matrix, TradingView) notlarda yok.
- Tansu'nun kanıtı: yok (EGEPO örneği, "tavan hisseler bulduk" cümlesi; sonuç ölçümü yok). Karşı kanıt aynı sette: §34'e göre DOAŞ 2022-2024'te 12-144-169 stratejisi al-tutu geçemedi (Ham; tek hisse).
- Günlük bedava veriyle uygulanabilir mi: evet (günlük kapanıştan EMA; 169 günlük geçmiş gerekir). Çıkış olmadığı için kural giriş düzeyindedir.
- Kaynak güveni: Ham birinci el; giriş koşulu net, çıkış ve parametre onayı yok: orta-düşük. Hazırlık K.
- Ek kaynaklar (X arşivi, 18.10):
  - `tweet-vegas-12-144-169-ema-yukari-kesisim-1848803496893558928` — `tweet-vegas-12-144-169-ema-yukari-kesisim-1848803496893558928` (2024-10-22). Günlük tarama koşulu: "Günlük analizde *12 EMA*, *144 EMA* ve *169 EMA'yı* yukarı keserek *AL sinyali veren hisseler:" (Ham); FRIGO ve IHAAS örnekleri.
  - `tweet-vegas-12-144-169-ema-yukari-kesme-1848385592771424616` — `tweet-vegas-12-144-169-ema-yukari-kesme-1848385592771424616` (2024-10-21). Günlük tarama koşulu: "Günlük analizde *12 EMA*, *144 EMA* ve *169 EMA'yı* yukarı keserek *AL sinyali veren hisseler:" (Ham); SKTAS örneği.
  - `tweet-vegas-ema-12-144-169-kesisim-1851726487855972606` — `tweet-vegas-ema-12-144-169-kesisim-1851726487855972606` (2024-10-30). Günlük tarama koşulu: "Günlük analizde *12 EMA*, *144 EMA* ve *169 EMA'yı* yukarı keserek *AL sinyali veren hisseler:" (Ham); BASCM örneği.
  - `tweet-vegas-ema-12-144-169-kesisim-1852066618488275443` — `tweet-vegas-ema-12-144-169-kesisim-1852066618488275443` (2024-10-31). Tarama başlığı: "Günlük analizde *12 EMA*, *144 EMA* ve *169 EMA'yı* yukarı keserek *AL sinyali veren hisseler:" (görsel, açıldı).
  - `tweet-vegas-gunluk-para-girisi-sarti-1846640825771377067` — `tweet-vegas-gunluk-para-girisi-sarti-1846640825771377067` (2024-10-16). Teyit şartı: "günlükte iyi çalışır. para girişini takip etmek şartı ile" (Ham).
  - `tweet-vegas-tunel-taramasi-1840173171280097751` — `tweet-vegas-tunel-taramasi-1840173171280097751` (2024-09-28). Optimizasyon önerisi: "EMA değerlerini optimize ederseniz daha iyi yerlerden giriş çıkış yakalarsınız." (Ham).
  - `tweet-vegas-tuneli-12-144-169-ema-tarama-1838671862420975657` — `tweet-vegas-tuneli-12-144-169-ema-tarama-1838671862420975657` (2024-09-24). Kod (görsel, açıldı): "ema_s = 12", "ema_l = 144", "ema_ll = 169". Okuma (YORUM): kod son iki barda kısa EMA’nın iki uzun EMA’yı birlikte aşağıdan yukarı kesmesini arar; interval 15m iken yorum 4 saat der.
  - `tweet-vegas-tuneli-15dk-tarama-1838670037353374138` — `tweet-vegas-tuneli-15dk-tarama-1838670037353374138` (2024-09-24). Zaman ölçeği örneği: "15 dakikalık Vegas Tüneli taramamıza bu akşam 2 hisse yakalandı." (Ham).
  - `tweet-vegas-tuneli-30-109-150-optimize-1835559479842070775` — `tweet-vegas-tuneli-30-109-150-optimize-1835559479842070775` (2024-09-16). DOAS günlük örneğindeki ayar: "30-109-150 (parametreler optimize edilmiştir)" (Ham). Okuma (YORUM): bu hisseye özgü ayar, genel varsayılan değildir.
  - `tweet-vegas-tuneli-ema-12-144-169-python-1827315938741379225` — `tweet-vegas-tuneli-ema-12-144-169-python-1827315938741379225` (2024-08-24). Kod örneği: "ema_s = 12", "ema_l = 144", "ema_ll = 169" (G2, açıldı). Okuma (YORUM): kapanışın adjust=False üssel ortalamaları grafiğe çizilir; paylaşılan kod bir işlem yürütücüsü değildir.
  - `tweet-vegas-tuneli-ema-12-144-169-tarama-1839308965039190302` — `tweet-vegas-tuneli-ema-12-144-169-tarama-1839308965039190302` (2024-09-26). Tarama: "12 günlük EMA'nın 144 ve 169 günlük EMA'yı yeni yukarı kestiği hisseler:" (Ham); EGEPO örneği.
  - `tweet-vegas-tuneli-parametre-optimizasyonu-1839323182035316985` — `tweet-vegas-tuneli-parametre-optimizasyonu-1839323182035316985` (2024-09-26). Parametre uyarısı: "Vegas tünelinde , örneğin , 12,144,169 da işleme girilir mi?" ve "Aslında girilmez" ve "Optimize etmeniz lazım" (Ham). "Belki en iyi en karlı değer 13-132-178 olacak" (Ham) olasılık ifadesidir.
  - `tweet-vegas-tuneli-rsi-14-50-cizgisi-1827737743683707129` — `tweet-vegas-tuneli-rsi-14-50-cizgisi-1827737743683707129` (2024-08-25). RSI teyidi: "RSI'da benim için sinyal 50 çizgisi kırılımı ile gelir. (Orta çizgi)" (Ham).
  - `tweet-vegas-tuneli-rsi-iplot-kodu-1827732393500758218` — `tweet-vegas-tuneli-rsi-iplot-kodu-1827732393500758218` (2024-08-25). RSI izleme: "Grafik üzerine geldiğinizde değerleri görebilirsiniz böylece 50 noktasını kesip kesmediğini görebilirsiniz" (Ham). Okuma (YORUM): etkileşimli grafik kullanım anlatımıdır.
  - `tweet-vegas-tuneli-tarama-para-girisi-1846638825864413237` — `tweet-vegas-tuneli-tarama-para-girisi-1846638825864413237` (2024-10-16). Vegas günlük taramasında teyit: "Günlük vegas tüneli taraması çıkan tek hissedir." ve "para girişini kontrol ediniz" (Ham).
  - `tweet-vegas-tuneli-yukari-kesis-atr-1827341150908543159` — `tweet-vegas-tuneli-yukari-kesis-atr-1827341150908543159` (2024-08-24). Giriş: "12 günlük üssel HO, 144 ve 169 günlük üssel hareketli ortalamanın oluşturduğu tüneli yukarı kesince long açıyoruz." Kâr alma önerisi: "Kar al'ı ise ATR ile yapabilirsiniz." (Ham).

---

## 64. EMA26 ATR bantlarında dip adayı: -3 ATR reddi ve -2 ATR onayı

- Kaynak: `tweet-ema26-atr-bant-3atr-ret-dip-1978494634121703760` (2025-10-15), `tweet-ema26-atr-bant-pivot-seviye-1957877677777375736` (2025-08-19). Tansu'nun X gönderileri; Ham birinci eldir.
- Tansu'nun ifadesi (verbatim, Ham, 15.10.2025): "EMA26 etrafında ATR" bantları. Ret: "Fiyat gün içinde -3 ATR bandının altına düşüyor ama kapanışta bunun üzerine çıkıyor". Onay: "Fiyat son birkaç günde -2 ATR bandını test etmiş" ve "şimdi bunun üzerinde iki gün üst üste kapanış yapıyor". Uyarı: "Bu bir garanti değil, bir olasılık."
- Tanım (YORUM): Merkez EMA26'dır. Alt bantlar merkezden 3 ve 2 ATR çıkarılarak okunur. -3 ATR altına gün içi sarkma ve üstüne kapanış ret sinyalidir. Yakın günlerde -2 ATR testi ile art arda iki üst kapanış onay sinyalidir. Ham bu ikisinin birlikte kullanımını önerir; tek barın eşzamanlı iki sinyal vermesi zorunlu tutulmaz.
- Parametreler: Merkez 26 dönem EMA, ret -3 ATR, onay -2 ATR, kapanış sayısı iki (Ham). 19.08.2025 G2 açıldı: "ATR Seviyeleri — EMA26 merkezli", "ATR14", "+1ATR", "+2ATR", "+3ATR" etiketleri. YORUM: ATR14 yalnız bu ayrı seviye tablosunun ayarıdır.
- Ek teyitler (Ham): "Eğer -2 ATR etrafında toparlanma yaşanırken MACD histogramı da pozitife dönüyorsa veya dipten yukarı kıvrılıyorsa". Hacim için "henüz bir filtre olarak kullanılmamış" der. EMA13/26, RSI30 ve temel/piyasa kontrolleri ek öneriler olarak anlatılır. YORUM: önerilerin hepsi zorunlu ortak kapıya dönüştürülmez.
- Belirsiz kalanlar (YORUM): Son birkaç günün uzunluğu, bantların hangi anda hesaplandığı, ATR yöntemi ve iki sinyal arasındaki azami süre uygulamadan önce belirlenmelidir. 15.10 sinyalinin ATR periyodu 19.08 tablosundan varsayılmaz.
- Tansu'nun kanıtı: AHGAZ sinyal tablosu ve strateji anlatımı. Ham olasılık vurgular; bu okuma başarı oranı hesaplamaz.
- Günlük bedava veriyle uygulanabilir mi: YORUM: günlük OHLCV bant, sarkma ve kapanışı hesaplamaya yeter. Yukarıdaki zaman ve hesap seçimleri gerekir.
- Kaynak güveni: Ham koşulları açıklar. 19.08 tablosu görselden açılarak okundu. Hazırlık K.

---

## 65. EWMA Z-skor getiri bantları: ±2 uç hareket ve ortalamaya dönüş

- Kaynak: `tweet-ewma-z-score-2-sigma-bant-1936765170744701091` (2025-06-22), `tweet-ewma-z-score-asiri-deger-tarama-1936767147914485837` (2025-06-22), `tweet-ewma-zskor-getiri-bandi-1937605928653640084` (2025-06-24). Tansu'nun X gönderileri; Ham birinci eldir.
- Tansu'nun ifadesi (verbatim, Ham, 22.06.2025): "Yeşil noktalar: z-score > +2 → anormal yüksek getiri." "Kırmızı noktalar: z-score < -2 → anormal düşük getiri." Olası eylemler: "z-score > 2 (yeşil nokta): Aşırı fiyatlama olabilir → kar satışı / ters pozisyon açılabilir." ve "z-score < -2 (kırmızı nokta): Aşırı düşüş → geri dönüş alım fırsatı olabilir."
- Tanım (YORUM): Günlük getiri serisi, EWMA merkezi ve değişen volatilite bandıyla birlikte okunur. Üst uç satış/ters yön değerlendirmesi, alt uç geri dönüş alımı olasılığıdır. Kaynağın olasılık dili kesin emir yapılmaz. Bu getiri bandı, fiyatın Bollinger bandına temasından ayrı kavramdır.
- Parametreler: Z üst eşik >2, alt eşik <-2; çizim bantları ±2σ (Ham). Eşitlik durumu bu iki açık karşılaştırmaya eklenmez.
- Belirsiz kalanlar (YORUM): EWMA ağırlığı, volatilite hesabı, Z hesabının merkezi ve ölçeği, tetik sonrası teyit, emir zamanı ve risk yönetimi uygulama öncesinde belirlenmelidir.
- Tansu'nun kanıtı: AVTUR için Ham "Sonucu ortada... Hisse değer kaybetti." der. 19.06 taraması ile 20.06 değerlendirmesini anlatır. AGYO notu ayrı grafik çıktısıdır; Ham "maşallahül azim:)" der. YORUM: bu iki örnek genel başarı oranı değildir.
- Günlük bedava veriyle uygulanabilir mi: YORUM: kapanış getirisiyle hesaplanabilir. Sayılan hesap tercihleri belirlenmeden aynı sonuç üretilemez.
- Kaynak güveni: Eşikler ve koşullu eylemler Ham'dadır. Gösterge formülünü bu okuma seçmez. Hazırlık K.

---

## 66. H formasyonu: üç mumlu boğa trend devamı

- Kaynak: `tweet-h-formasyonu-uc-mum-trend-devam-1905960716571451830` (2025-03-29). Tansu'nun X gönderileri; Ham birinci eldir.
- Tansu'nun ifadesi (verbatim, Ham): "Bu formasyon üç mumdan oluşan bir trend devam formasyonudur." İlk mum: "İlk olarak boğa yönlü bir mum oluşur (yani kapanış, açılıştan yüksektir)." İkinci mum: "Bu mumun açılış ve kapanış fiyatı eşittir (doji benzeri)." Üçüncü mum: "Üçüncü mum tekrar boğa yönlü olmalıdır ve kapanışı, kararsızlık mumunun kapanışından yüksek olmalıdır." Ek şart: "üçüncü mumun en düşük seviyesi, kararsızlık mumunun en düşük seviyesinden yüksek olmalıdır."
- Tanım (YORUM): Art arda üç mum için C1>O1, C2=O2, C3>O3, C3>C2 ve L3>L2 birlikte aranır. İkinci mumun eşitliğine tolerans eklenmez.
- Parametreler: Üç mum. Fiyat karşılaştırmaları Ham'da açıkça yazılmıştır.
- Belirsiz kalanlar (YORUM): Önceki trendin ölçüsü, işlem zamanlaması, stop, hedef ve satış tarafının koşulları uygulama öncesinde belirlenmelidir. Ayı yönü boğa kuralının aynası olarak varsayılmaz.
- Tansu'nun kanıtı: THYAO işaretli grafik örneği. Bu okuma geçmiş işlem başarısını ölçmez.
- Günlük bedava veriyle uygulanabilir mi: YORUM: OHLC ile mum koşulları hesaplanır. Gerçek açılış fiyatı gerekir.
- Kaynak güveni: Beş karşılaştırma Ham'da açık; tam işlem sistemi bu kayıtta kurulmaz. Hazırlık K.

---

## 67. Harami Cross: trend sonunda doji ve üçüncü gün onayı

- Kaynak: `tweet-harami-cross-onay-kurali-1983253407096868947` (2025-10-28). Tansu'nun X gönderileri; Ham birinci eldir.
- Tansu'nun ifadesi (verbatim, Ham): "Harami Cross, iki mumdan oluşan bir dönüş formasyonudur". "mutlaka bir trendin sonunda (yükseliş veya düşüş) görülmelidir". İlk mum mevcut trend yönündedir. Doji sınırı: "Bu küçük Doji'nin tüm gövdesi ve fitilleri, birinci (anne) mumun gövde sınırları içinde kalmalıdır." Üçüncü gün, yükseliş sonunda: "fiyatın aşağı yönde hareket etmesini ve kırmızı bir mumla kapanış yapmasını bekleyin." Düşüş sonunda: "fiyatın yukarı yönde hareket etmesini ve yeşil bir mumla kapanış yapmasını bekleyin."
- Tanım (YORUM): Önce trend yönünde büyük gövdeli mum, sonra onun gövdesinin içinde kalan doji, ardından ters yönde onay mumu aranır. Doji fitilleri de ilk gövdenin sınırları içindedir. Yeşil/kırmızı karşılaştırması sırasıyla Close>Open ve Close<Open olarak okunur.
- Parametreler: İki oluşum mumu ve sonraki üçüncü gün onayı (Ham). Dojinin açılış ve kapanışı Ham'da birbirine çok yakın diye açıklanır.
- Belirsiz kalanlar (YORUM): Trend sonunun ölçüsü, büyük gövde eşiği, doji yakınlık toleransı, giriş fiyatı, stop ve hedef uygulama öncesinde belirlenmelidir.
- Tansu'nun kanıtı: NUHCM harmonik grafiği ve Bullish Harami Cross görseli. Ham açıklaması yöntemi anlatır; bu okuma başarı oranı hesaplamaz.
- Günlük bedava veriyle uygulanabilir mi: YORUM: OHLC yeterlidir; eşik ve trend tanımı gerekir.
- Kaynak güveni: Sıra ve onay Ham'da açık. Tanımsal eşikler seçim gerektirir. Hazırlık K.

---

## 68. Ichimoku hesaplaması ve dört koşullu bulut taraması

- Kaynak: `tweet-ichimoku-9-26-52-hesap-kodu-1760937885190996368` (2024-02-23), `tweet-ichimoku-bulut-tarama-kosullari-1847998614548721928` (2024-10-20). Tansu'nun X gönderileri; Ham birinci eldir.
- Tansu'nun ifadesi (verbatim, 20.10.2024 Ham): "aşağıdaki koşulları taradım. Doğru mudur?" Koşullar: "Tenkan-sen > Kijun-sen", "Senkou Span A > Senkou Span B", "Kapanış Fiyatı (Close) > Senkou Span A:" ve "Chikou Span > Close ((Gecikmeli Çizgi Kapanış Fiyatının Üstünde)". Sonuç: "Hisse çıkarmadı, enteresan."
- Tanım (YORUM): Dört karşılaştırma birlikte denenir. Kaynak bunu doğruluğu sorulan tarama olarak sunar; doğrulanmış işlem sistemi değildir.
- Parametreler (23.02.2024 G1 açıldı): Tenkan yüksek/düşük penceresi 9, Kijun 26, Span B 52. Görsel kod: "rolling(window=9)", "rolling(window=26)", "rolling(window=52)". Span A Tenkan/Kijun ortalamasını, Span B 52 dönem yüksek/düşük ortalamasını 26 bar kaydırır: ".shift(26)". Chikou: "df_thyao['Chikou Span'] = df_thyao['Close'].shift(-26)".
- Belirsiz kalanlar (YORUM): Şubat çizim kodunun Ekim taramasındaki zaman hizası ayrıca belirlenmelidir. Chikou'nun negatif kaydırmasını geçmiş bara işlem bilgisi diye uygulamak ileri bilgi kullanabilir. Son gün yeni kesişim gereği, emir zamanı, stop ve çıkış seçimleri bu okumada yapılmaz.
- Tansu'nun kanıtı: THYAO çizim kodu ve Ekim taramasında boş sonuç. Bu okuma kârlılık kanıtı üretmez.
- Günlük bedava veriyle uygulanabilir mi: YORUM: yüksek, düşük ve kapanış hesabı yeterlidir; zaman hizası açıklığa kavuşmadan geçmiş sinyale çevrilmez.
- Kaynak güveni: Kod görseli açıldı. Tarama Ham'da soru olarak bırakılır. Hazırlık K.

---

## 69. Keltner kanalında trend ve yatay piyasa ayrımı

- Kaynak: `tweet-keltner-bant-kesisim-long-sinyali-1852457611288789277` (2024-11-01); `tweet-keltner-kanal-dip-alim-stratejisi-1979691577632231774` (2025-10-18); `tweet-keltner-trend-ust-bant-ortalamaya-donus-1852476829543587877` (2024-11-01). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "trend varken üst bandın üstünde kapanışlar al demiştik." / "alt bandı yukarı kesince al üst bandı aşağı kesince sat." / "Tamamen trende göre strateji kurgulamak lazım keltnerde" (01.11.2024, Ham). BTC örneği: "5 dakikalık grafikte görüntü bu. Siyah kırmızıyı yukarı kestiğinde long açılabilecek." AAPL örneği: "Dip alım stratejisi örneği" / "Ben size temelini vereyim siz kendinize göre evirin." (18.10.2025, Ham).
- Tanım: Okuma (YORUM): trendde kanal üstü kapanışla devam işlemi, yatay piyasada alt bandı yukarı ve üst bandı aşağı kesişle ortalamaya dönüş ayrılır. BTC'nin renkli çizgi ifadesi, tanımı açıklanmayan ayrı örnektir. AAPL görüntüsündeki göstergeler bu iki rejimin zorunlu birleşimi sayılmaz.
- Parametreler: BTC zaman dilimi 5 dakika (Ham). AAPL G1 lejantı (açıldı): "KC Middle (EMA20)", "EMA 5", "SMA 200", "SMA 250", "RSI (14)" ve KC ±1/±2/±3 katmanları. Bunlar AAPL örnek ayarlarıdır (YORUM).
- Belirsiz kalanlar: Trend/yatay rejim kararı, KC genişlik hesabı, BTC renklerinin formülleri ve AAPL giriş sırası açık kalır. Stop ve hedef bu okumanın kaynaklarından belirlenmedi.
- Tansu'nun kanıtı: BTC ve AAPL grafik örnekleri. İşlem dizisi veya karşılaştırmalı sınama sonucu bu kaynaklarda kurulmaz (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): günlük biçim OHLC ile kurulabilir; 5 dakikalık BTC örneği günlük veriyle aynen üretilemez. Örnek varlıklar BIST evreni dışındadır.
- Kaynak güveni: Ham eylem yönlerini açık verir; rejim ve kanal ayarları tamamlanmamıştır. Hazırlık K.

---

## 70. MA20/MA50 yükselen trend ve geri çekilme sınırı

- Kaynak: `tweet-ma20-ma50-trend-geri-cekilme-kurali-1841922080541180029` (2024-10-03); `tweet-ma20-ma50-trend-python-kod-1841923620714774620` (2024-10-03). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "20 MA, 50 MA'nın üzerinde olmalı. Her iki hareketli ortalama yükseliyor olmalı." ve "İki hareketli ortalama arasındaki mesafe büyük ve/veya büyüyor olmalı." (03.10.2024, Ham; kod paylaşımı). "Geri çekilmeler fiyatın sadece 20 MA'ya ya da en fazla 20 MA ve 50 MA arasında olmalı" (Ham).
- Tanım: Okuma (YORUM): kısa ortalama uzun ortalamanın üzerinde olacak; ikisi yükselecek; aralarındaki mesafe büyük veya büyüyor olacak. Geri çekilme MA20'ye veya MA20–MA50 aralığına sınırlanır. Açılan kod koşulları tarayan mantık yerine iki ortalamayı hesaplayıp çizer.
- Parametreler: Kodda "data['MA20'] = data['Close'].rolling(window=20).mean()" ve "data['MA50'] = data['Close'].rolling(window=50).mean()" (G1, açıldı). Okuma (YORUM): paylaşılan hesaplar basit kapanış ortalamalarıdır.
- Belirsiz kalanlar: Mesafenin büyük sayılma ölçütü, yükselme için bakılacak bar sayısı ve geri çekilmeyi fiyatın hangi alanıyla ölçeceğimiz açık kalır. Giriş tetiği ve çıkış ayrıca tanımlanmalıdır.
- Tansu'nun kanıtı: TUPRS örnek grafik ve çizim kodu. Ham kural cümleleri kodun otomatik tarama başarısını kanıtlamaz (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): günlük kapanışla SMA hesaplanır; belirsiz koşullar için karar gerekir.
- Kaynak güveni: Ham koşulları ve açılmış hesap kodu güçlüdür; giriş/çıkış tamamlanmamıştır. Hazırlık K.

---

## 71. MA5 sapmasıyla kısa pozisyon ve ortalamaya dönüş deneyi

- Kaynak: `tweet-ma5-sapma-3-ortalamaya-donus-1911789788019019979` (2025-04-14). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "True Price: Hissenin gerçeğe en yakın değerini 5 günlük hareketli ortalamayla modelledim." / "Observed Price: Günlük kapanış fiyatı." / "Fiyat Sapması: (Observed - True) / True" (Ham). "Eğer bu oran %3’ün üzerindeyse, fiyatın primli olduğu kabul edilir → short açılır." / "Fiyat, adil değere %1 altına inene kadar beklenir → pozisyon kapatılır."
- Tanım: Okuma (YORUM): günlük kapanışın MA5'e göre göreli sapması üzerinden kısa pozisyon açan deneydir. Kaynaktaki adil değere %1 altına ifadesi aynen korunur; bunu sessizce ±%1 yakınsama kuralına çevirmeyiz. Mevcut yalnız alış yönlü aileye eklenmez.
- Parametreler: MA dönemi 5 gün; giriş sapması > %3; çıkış açıklamasında %1 altı (Ham). MA türü ve çıkış karşılaştırmasının tam eşitliği bu kaynakta kesinleştirilmez.
- Belirsiz kalanlar: MA türü, çıkış ifadesinin tam anlamı, işlem zamanı, maliyet, stop ve pozisyon büyüklüğü açık kalır.
- Tansu'nun kanıtı: "İlk deneme pek yakında" (Ham). Pozitif PnL anlatısı vardır; tamamlanmış sayısal sınama olarak kullanılmaz (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): günlük kapanış yeterlidir; kısa pozisyon uygulaması mevcut yalnız alış yönlü kapsam dışındadır.
- Kaynak güveni: Ham giriş ve sapmayı verir; çıkış dili ve sınama sonucu sınırlıdır. Hazırlık K.

---

## 72. MACD uyumsuzluğu: karşılaştırmalı tarama, tolerans ve örnekler

- Kaynak: `tweet-macd-12-26-9-negatif-uyumsuzluk-1760775094895267881` (2024-02-22); `tweet-macd-5-gun-uyumsuzluk-karsilastirma-1839078126015438978` (2024-09-25); `tweet-macd-pozitif-uyumsuzluk-3-5-10-gun-1839397534797828274` (2024-09-26); `tweet-macd-pozitif-uyumsuzluk-taramasi-1838266163605680280` (2024-09-23). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "fiyatta 3-5-10 gün geriye bakarak bugün ile karşılaştırıp uyumsuzlukları buluyor." (26.09.2024, Ham). "Elbette MACD tek başına yeterli olmayacak" (23.09.2024, Ham). "macd pozitif uyumsuzluk taramam hala istediğim performansta değil" (25.09.2024, Ham). "Grafikte göreceğiniz üzere fiyat hareketi artarken ortalama fiyat artışını desteklememiş. Negatif uyumsuzluk." (22.02.2024, Ham).
- Tanım: Okuma (YORUM): açılmış 26.09 kodu bugünkü fiyatı ve MACD'yi her geçmiş konumla karşılaştırır. "price_divergence = today_price < past_price" ve "macd_divergence = today_macd > past_macd * (1 - tolerance)" birlikte sağlanır (G1). Bu kod standart pivot tespiti yerine seçilmiş bar değerlerini karşılaştırır.
- Parametreler: "def calculate_macd(data, short_window=12, long_window=26, signal_window=9):" ve "def detect_bullish_divergence(data, periods=[3, 5, 10], tolerance=0.01):" (G1, açıldı). Fiyat Adj Close. Kod: "past_price = data.iloc[-period]['Adj Close']".
- Belirsiz kalanlar: Okuma (YORUM): son değer iloc[-1] olduğundan iloc[-period] ile satır uzaklığı period−1'dir; Ham'ın 3/5/10 gün ifadesiyle aynı değildir. EWM çağrısı min_periods=1 kullanır; adjust açık yazılmaz. Negatif MACD'de çarpımsal toleransın davranışı işaretle değişir. Taramadan işlem giriş/çıkış kuralı türetilmez.
- Tansu'nun kanıtı: THYAO negatif, AKBNK ve TUPRS pozitif uyumsuzluk örnekleri; Ham gözle backtest der. 26.09 kodu paylaşılır; okuyucu bu kodu çalıştırmadı.
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): düzeltilmiş günlük kapanışla tarama hesaplanabilir. Ham/kod bar farkı karar verilmeden sessizce düzeltilmez.
- Kaynak güveni: Kod ve Ham birinci eldir; gün uzaklığı farkı ve seçilmiş örnek sınırı korunur. Hazırlık K.

---

## 73. MACD son bar kesişimi ve yerel yukarı dönüş taraması

- Kaynak: `tweet-macd-kesisim-yon-tarama-kodu-1735587454080418037` (2023-12-15); `tweet-macd-sinyal-kesisim-taramasi-1838327306210680961` (2024-09-23); `tweet-macd-sinyal-kesisim-taramasi-1838337201026822205` (2024-09-23). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "BarSinceCross := Barssince(Cross(MACDLine, SignalLine)) < 1;" ve "IncreasingMACD := MACDLine > Ref(MACDLine, −1) and Ref(MACDLine, −1) < Ref(MACDLine, −2);" (15.12.2023, G1 açıldı). Birleşim: "ScanCriteria := BarSinceCross and IncreasingMACD;". "Yatmadan önce bir de size son gün MACD kesişenleri tarattım." (23.09.2024, Ham).
- Tanım: Okuma (YORUM): 2023 kodu son bardaki MACD-sinyal kesişimini, önceki MACD değeri iki komşusundan düşük olacak şekilde yerel yukarı dönüşle birleştirir. Bu, iki gün aralıksız yükseliş değildir. 2024 günlük AL listesi ile yalnız son gün kesişim listesi ayrı çıktılardır; eski koddaki yerel dönüş şartı bunlara kendiliğinden eklenmez.
- Parametreler: "MACDLine := MACD(C, 12, 26, 9);" ve "SignalLine := MACDSignal(C, 12, 26, 9);" (G1, açıldı). Son bar için Barssince < 1. 2024 paylaşımı günlük periyottadır (Ham).
- Belirsiz kalanlar: Cross ve Ref işlevlerinin platform uygulaması, 2024 taramalarının tam kodu, işlem fiyatı, stop ve çıkış açık kalır.
- Tansu'nun kanıtı: "4 hisse çıktı. Seçenekleri biraz daralttık." (23.09.2024, Ham). Bu sayı o tarihli tarama sonucudur, başarı oranı değildir (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): günlük kapanış yeterlidir; yerel dönüşün iki geçmiş gözlemi gerekir.
- Kaynak güveni: Açılan kod ölçülebilir koşul verir; sonraki taramalara aynı kodu atfetme yapılmaz. Hazırlık K.

---

## 74. MACDAS karşılıklı kesişimleri ve optimizasyon aralıkları

- Kaynak: `tweet-macdas-cross-al-sat-formulu-opt-araligi-1778777162587279414` (2024-04-12). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "AL= CROSS(MACDAS(OPT1,OPT2,OPT3),MACDASTRIGGER(OPT1,OPT2,OPT3))" ve "SAT= CROSS(MACDASTRIGGER(OPT1,OPT2,OPT3),MACDAS(OPT1,OPT2,OPT3))" (Ham). "Her hissede aynı sonucu vermez. Ayrıca sadece bu değerler yeterli değil."
- Tanım: Okuma (YORUM): AL formülü MACDAS'ın tetik çizgisini kesmesini, SAT formülü ters kesişimi kullanır. MACDAS işlevinin platform tanımı ayrıca gerekir; standart MACD ile otomatik eşitlenmez.
- Parametreler: Açılan G1 tablosu "ALT SINIR ÜST SINIR ADIM": "OPT1 13 55 1", "OPT2 8 15 1", "OPT3 3 13 1". Bunlar optimizasyon aralıklarıdır; optimum değer veya her hissede geçerli set değildir (YORUM).
- Belirsiz kalanlar: MACDAS ve MACDASTRIGGER hesapları, veri periyodu, amaç ölçütü, maliyet ve aşırı uyum kontrolü açık kalır. Hisse bazlı optimizasyon için mevcut karar değiştirilmez.
- Tansu'nun kanıtı: Formül ve aralık tablosu paylaşılır. Bir optimum veya sayısal sonuç gösterilmez (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): zaman dilimi ve platform işlevleri eşleştirilmeden günlük Python kuralına birebir çevrilemez.
- Kaynak güveni: Ham kesişim yönleri ile görüntüdeki aralıklar açıktır; işlevlerin iç hesabı açık kalır. Hazırlık K.

---

## 75. Çok ölçekli momentum modelinde eğitim/test ayrımı ve olasılık kararı

- Kaynak: `tweet-ml-momentum-trend-classifier-1893042379822629109` (2025-02-21); `tweet-ml-momentum-trend-classifier-1893042415272968347` (2025-02-21). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "Yani ilk dönüş noktası belirlenerek momentum sisteminin referans başlangıç noktasını elde ediyorum." / "lokal maksimum-minimum bazlı trend geçişlerini sistematik şekilde işaretlememi sağlıyor." (Ham). "Verinin %90’lık kısmını model eğitimi için kullanarak, geri kalan %10’luk kısımda model performansını test edebilmem için bir yapı oluşturuyorum." / "karar sınırını 0.5 olarak belirleyerek" (Ham).
- Tanım: Okuma (YORUM): kayan pencerelerde yerel uçlar ve farklı zaman ölçekleriyle momentum durumu hazırlanır. Sonraki model olasılıklarını PRED alanına yazar, yönü 0.5 sınırıyla yorumlar ve LONG/SHORT kararını anlatır. Bu anlatım mevcut proje sınamasının bölmelerini veya yalnız alış kapsamını değiştirmez.
- Parametreler: Eğitim/test oranı %90/%10 ve olasılık karar sınırı 0.5 (Ham). Ham bazen sinir ağı bazen başka algoritma kullanıldığını söyler; tek zorunlu model değildir.
- Belirsiz kalanlar: Pencere uzunlukları, uç noktaların nedensel tespiti, etiketleme vadesi, eşitlikte 0.5 davranışı, hiperparametreler ve işlemin gecikmesi açık kalır.
- Tansu'nun kanıtı: Ham süreç ve görselleştirme anlatımıdır. Sayısal başarı ölçüsüne dönüştürülmez (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): fiyat serisiyle geliştirilebilir; belirtilmeyen etiket ve pencere seçimleri tamamlanmadan kaynak sistem aynen kurulamaz.
- Kaynak güveni: Ham eğitim oranı ve karar sınırını verir; modelin tamamı tanımlı değildir. Hazırlık K.

---

## 76. Çoklu PSAR ve regresyon kanalıyla tarama

- Kaynak: `tweet-psar-regresyon-kanal-tarama-1951742859704713570` (2025-08-02). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "psarlar (3 renli noktalar) fiyat altında alacak." / "psar ortalama eğrisi de her şartta fiyatın altında." / "regresyon üst orta ve alt eğrileri var risk algınıza göre orada bir sinyal oluşturuyorsunuz" (Ham).
- Tanım: Okuma (YORUM): üç PSAR noktası ile PSAR ortalama eğrisi fiyatın altında tutulur. Regresyon kanalından alınacak ek sinyal risk tercihine bırakılır. Bu birleşim EMA sıkışması şartını kendiliğinden içermez.
- Parametreler: Ham üç renkli PSAR noktalarını ve üst/orta/alt regresyon eğrilerini adlandırır. Sayısal PSAR ayarları ve regresyon penceresi bu yanıttan belirlenmez.
- Belirsiz kalanlar: PSAR hızlanma ayarları, ortalama eğrisi hesabı, regresyon türü/penceresi ve risk tercihini somut sinyale çeviren koşul açık kalır.
- Tansu'nun kanıtı: Bir tarama kurma açıklamasıdır; çalıştırma sonucu verilmez (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): günlük OHLC ile bileşenler hesaplanabilir; ayar ve regresyon sinyali kararı gerekir.
- Kaynak güveni: Ham yön şartını verir; hesap ve ikinci sinyal eksiktir. Hazırlık K.

---

## 77. SMA20/SMA40 teyidinden sonra ilk PSAR barında giriş

- Kaynak: `tweet-psar-sma20-sma40-kesisim-giris-1864259354800578906` (2024-12-04). Tansu'nun X gönderileri; Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): "Yeni strateji, PSAR ve 20sma, 40sma" / "sma ile trendi teyit ediyoruz" / "kesişim sonrasi ilk psar barında giriş yapıyoruz." (Ham).
- Tanım: Okuma (YORUM): SMA çiftinin trend teyidini izleyen ilk PSAR barı giriş sırası olarak okunur. Ham kesişim yönünü ve PSAR barının fiyatla konumunu ayrıntılandırmadığı için bunlar varsayım olarak eklenmez.
- Parametreler: SMA dönemleri 20 ve 40; olay sırası kesişim, ardından ilk PSAR barı (Ham).
- Belirsiz kalanlar: Kesişimin yönü, ilk PSAR barının hangi değişimi ifade ettiği, PSAR ayarları, işlem fiyatı, stop ve çıkış açık kalır.
- Tansu'nun kanıtı: ADGYO grafik örneği Görsel metni içinde adlandırılır; sayısal performans kanıtı olarak kullanılmaz (YORUM).
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): günlük OHLC ile hesaplanabilir; PSAR tetik tanımı tamamlanmalıdır.
- Kaynak güveni: Ham sıralama ve SMA çiftini açık verir; PSAR geçişinin kesin tanımı eksiktir. Hazırlık K.

---

## 78. Quintuplets: beş küçük gövdeli mum ve farklı sinyal günleri

- Kaynak: `tweet-quintuplets-bes-kapanis-alim-1919053643946303495` (2025-05-04), `tweet-quintuplets-bes-mum-formasyonu-kodu-1905940770281910507` (2025-03-29). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): 04.05.2025 Ham: “Son beş kapanış fiyatı, hem kendi açılış fiyatlarından hem de kendilerinden önceki kapanış fiyatlarından daha yüksekse”; “bir sonraki gün alım (buy)  yaz.” 29.03.2025 G2 kodu (açıldı): “data[i, buy_column] = 1  # Aynı gün”.
- Tanım (YORUM): Mart kodu beş yeşil mumda yükselen kapanışları ve her gövdenin body sınırından küçük olmasını arar. En eski mum için ondan önceki kapanışla kıyas yoktur. Kırmızı mumlar ve azalan kapanışlar satışın simetriğidir. Mart sinyali son mumun gününe, Mayıs sözü sonraki güne yazar; bu iki biçim birleştirilmez.
- Parametreler: Beş mum. Kodda katı gövde sınırı `< body`; al sütunu +1, sat sütunu -1. Mayıs metni beş kapanışın her birini öncekiyle kıyaslar.
- Belirsiz kalanlar (YORUM): body değeri ve birimi; Mayıs metninin en eski kapanış koşulu ile Mart kodunun farkı; uygulanacak sinyal günü; giriş dolumu, stop ve hedef.
- Tansu'nun kanıtı: Mart notu DOAS grafiği gösterir ve taramanın hazır olduğunu söyler. Sistematik başarı sonucu verilmiş sayılmaz.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Açılış ve kapanış bulunan günlük veriyle desen kurulabilir. body ve sinyal günü çözülmeden tek kural seçilemez.
- Kaynak güveni: Birinci el kaynak; kuralın belirtilen kısmı okunabilir. Hazırlık K.

---

## 79. Regresyon kanalı orta/üst bant kırılımı ve pencere tercihi

- Kaynak: `tweet-regression-channel-band-cross-scan-1888577330588561831` (2025-02-09), `tweet-regression-upper-band-breakout-1951804812661805144` (2025-08-03), `tweet-regresyon-kanali-bant-sinyali-1873609824442929204` (2024-12-30), `tweet-regresyon-kanali-bant-sinyali-1874175140042596410` (2024-12-31), `tweet-regresyon-kanali-volatilite-osilatoru-sinyal-1992343253497401777` (2025-11-22), `tweet-regresyon-kirilim-60-gun-momentum-16-1890128183972008095` (2025-02-13). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): 09.02.2025: “regresyon kanalı orta bandı ve üst bandı yukarı kesenleri tarayacağız”. 13.02.2025: “regresyon kırılımlarını buluyorum genelde 60 gün tercih ediyorum”. 30.12.2024: “Eğitim amaçlıdır sakın buna güvenip işlem açmayın.”
- Tanım (YORUM): Regresyon kanalı bantlarının yukarı aşılması tarama fikridir. 60 gün pencere kişisel tercihtir. Aynı cümledeki 16 günlük momentum aracı farklı koddur. ANGEN üst yay örneği ve SNGYO denemesi başarı garantisi değildir. DOAS görseli (açıldı) denge hattı, hız, teyit ve volatilite osilatörü etiketleri taşır; etiketlerden al-sat formülü türetilmez.
- Parametreler: Regresyon tercihi 60 gün (Ham). Ayrı momentum penceresi 16 gün (Ham). DOAS görseli “SMA 14” yazar; bu örnek ayarıdır.
- Belirsiz kalanlar (YORUM): Kanal hesabı, bant genişliği, kesişimin kapanışla ölçümü, iki bandın birlikte mi ayrı mı tarandığı ve çıkış kuralı; DOAS osilatör formülü.
- Tansu'nun kanıtı: Plan ve seçilmiş grafikler. 09.02.2025 notunun 100.000 Monte Carlo denemesi portföy planıdır; regresyon sinyalinin doğrulama sayısı değildir.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Günlük fiyatla araştırılabilir; kaynak parametrelerin tümünü vermediği için birebir tarama hazır değildir.
- Kaynak güveni: Birinci el kaynak; kuralın belirtilen kısmı okunabilir. Hazırlık K.

---

## 80. ROC9 sıfır çizgisi yukarı kesişimi ve ROC seri örnekleri

- Kaynak: `tweet-roc-9-20-50-kesisim-1840801601784545478` (2024-09-30), `tweet-roc-9-50-kesisim-1840799431626510719` (2024-09-30), `tweet-roc-9-sifir-kesisim-taramasi-1840816385540440325` (2024-09-30), `tweet-roc-9-sifir-kesisim-taramasi-1840826561273979333` (2024-09-30), `tweet-roc-9-sifir-kesisim-taramasi-1840836969363841489` (2024-09-30), `tweet-roc9-sifir-yukari-kesis-al-1840811430800420929` (2024-09-30). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): 30.09.2024: “Stratejiye göre RoC9, 0 çizgisini yukarı kestiğinde Al sinyali oluşuyor.” Tarama ekranı (açıldı): “Son kapanış gününde RoC 9'un 0 eksenini yukarı kestiği hisseler:”. Gösterge tercihi: “Momentum indikatörü kullananların RoC kullanmasına gerek yok”.
- Tanım (YORUM): ROC9 sıfır çizgisinin yukarı kesişimi al sinyali üretir ve son kapanış gününde taranır. Ayrı VAKBN ve ADGYO görselleri ROC serilerinin birbirleriyle kesişimini gösterir; bunlar sıfır çizgisi kuralına otomatik eklenmez.
- Parametreler: ROC9; eşik 0 (Ham). VAKBN: “RoC 9 Gün”, “RoC 20 Gün”, “RoC 50 Gün”; ADGYO: “RoC 9 Gün”, “RoC 50 Gün” (görseller açıldı).
- Belirsiz kalanlar (YORUM): Kesişim eşitlik sınırı; ROC fiyat serisi ve hesap yöntemi; seri-seri kesişiminin tam koşulu; stop ve çıkış.
- Tansu'nun kanıtı: DEVA ve MARBL örnekleri ile son gün listesi. Seçilmiş örnekler genel başarı ölçüsü değildir.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Kapanıştan ROC ve kesişim hesaplanabilir; eşitlik sınırı ve işlem yönetimi uygulama kararı gerektirir.
- Kaynak güveni: Birinci el kaynak; kuralın belirtilen kısmı okunabilir. Hazırlık K.

---

## 81. ROC50, ADX/ADXR ve OBV ile giriş, teyit ve çıkış

- Kaynak: `tweet-roc-adx-adxr-kesisim-giris-cikis-1841222101497246009` (2024-10-01), `tweet-roc50-adx-adxr-obv-artan-1841597392178536580` (2024-10-02), `tweet-roc50-adx-adxr-obv-sistemi-1841604780218622243` (2024-10-02), `tweet-roc50-adx-adxr-obv-sma20-kosullari-1841955633047670978` (2024-10-03). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): 01.10.2024: “Roc 0'ı yukarı kesince pozisyon için pusuda bekleyin ve ADX'in ADXR'yi yukarıya kesmesini bekleyin.” “bu kesişim 20 üzerinde olursa iyi olur.” “ADX, ADXR'yi aşağıya kesince pozisyondan çıkın.” Aynı gün düzeltme: “Roc50 > 0 olmalı. Yanlış yazmışım yukarıda.” 03.10.2024: “RoC50 son gün 0 eksenini yukarıya kessin”; “OBV SMA20'yi yukarıya kessin”.
- Tanım (YORUM): İlk anlatım ROC sıfır kesişiminden sonra ADX/ADXR yukarı kesişimini bekler. Deneme varyantı, ROC50>0 iken ADX'in daha önce kesip hâlâ ADXR üstünde olmasını kabul eder. 03.10 taraması son gün ROC50 sıfır kesişimi, ADX>ADXR ve OBV'nin SMA20 üstüne kesişimini birleştirir. Kaynak ADRX yazımını da kullanır; gösterge adı ADXR olarak grafiklerde görünür. 04.10 yanıtı farkın açılmasını geliştirme önerisi olarak sunar.
- Parametreler: ROC50 ve sıfır eşiği; OBV SMA20 (Ham). ADX/ADXR kesişimi için 20 üzeri tercih, zorunlu eşik olarak yazılmaz. 01.10 G1'de “ADX (14)” ve “ADXR (14)” (görsel açıldı).
- Belirsiz kalanlar (YORUM): ADX/ADXR farkı artışının ölçümü; varyant seçimi; giriş fiyatı, stop ve bekleme süresi. ROC>50 hatası kaynak düzeltmesiyle ROC50>0 olarak korunur.
- Tansu'nun kanıtı: Eğitim grafikleri; “Taramanın asıl amacı yelpazeyi daraltmak” (02.10.2024). 03–04.10 notu geçmiş trend başlangıcını anlatır, bugün alım yapmadığını söyler.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Günlük fiyat/hacimle hesaplanabilir; kaynak varyantları tek koşul olarak birleştirilmez.
- Kaynak güveni: Birinci el kaynak; kuralın belirtilen kısmı okunabilir. Hazırlık K.

---

## 82. RSI14'ün beş dönem VAR ortalaması ile 50 kesişimi

- Kaynak: `tweet-rsi-14-ortalama-5-kesisim-50-1786779842530226293` (2024-05-04). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): Al: “Cross(Mov(RSI(C,14),5,VAR),50)”. Sat: “Cross(50,Mov(RSI(C,14),5,VAR))” (04.05.2024, Ham).
- Tanım (YORUM): Alımda RSI14'ün beş dönem VAR ortalaması 50'yi yukarı keser; satışta 50 bu ortalamayı yukarı keser. VAR türü basit veya üssel ortalama diye yeniden adlandırılmaz.
- Parametreler: RSI 14; VAR ortalama 5; eşik 50; kapanış C (formüller, Ham).
- Belirsiz kalanlar (YORUM): Platformun VAR ve Cross hesap ayrıntıları; zaman dilimi, işlem fiyatı, stop ve hedef.
- Tansu'nun kanıtı: Yanıt olarak verilen iki formül; sonuç ölçümü sunulmuş sayılmaz.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Günlük kapanışla araştırılabilir; platform fonksiyonlarının eşlemesi gerekir.
- Kaynak güveni: Birinci el kaynak; uygulama sınırları yukarıda korunur. Hazırlık K.

---

## 83. Temel kalite, teknik zamanlama ve takas: haftalık dip filtre önerisi

- Kaynak: `tweet-temel-filtre-haftalik-rsi-dip-tarama-1954864370409783700` (2025-08-11), `tweet-temel-teknik-birlikte-filtre-1916157411926180334` (2025-04-26), `tweet-temel-teknik-dip-roe-fk-rsi25-1913691337184154030` (2025-04-19), `tweet-temel-teknik-hibrit-filtre-kirilim-1913183056136896570` (2025-04-18), `tweet-temel-teknik-takas-sinyal-birlesimi-1935015198277951650` (2025-06-17), `tweet-temel-teknik-takas-uclu-filtre-1952262189361864710` (2025-08-04). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): 11.08.2025: “Bu tarama filtresi iş yapar mı?” “Haftalık RSI < 30”; “Fiyat / 52 Haftalık En Düşük < 1.10”. 18.04.2025: “temel analizle hangi hisseye odaklanılacağı belirlenirken, teknik analizle ne zaman alım-satım yapılacağına karar verilir.” 04.08.2025: “Temel, teknik, takas. Üçü de tamamsa fazlasına gerek yok.”
- Tanım (YORUM): Temel seçim ile teknik zamanlama ayrı katmanlardır. Haftalık dip listesi bir öneri olarak korunur. Takas örnekleri kurumsal alım yoğunluğunu tamamlayıcı katman yapar. 19.04'te ROE %20, F/K<5, RSI25 dönüşü; 17.06'da kâr artışı %80 ve 60 günlük direnç kırılımı örnektir, evrensel eşik değildir.
- Parametreler: 11.08 Ham: “Net Kâr Büyümesi: Son 4 çeyrekte pozitif büyüme (%10+ tercihen)”; “Borç / Özkaynak: < 1”; “F/K Oranı: Sektör ortalamasının altında”; “PD/DD: < 1.5”; “Satış Geliri Büyümesi: Son 4 çeyrek ortalama %10+”; “Brüt Karlılık: %20’nin üzerinde”. Teknik: “Haftalık MACD sinyal hattının altında, ama histogram artışa geçmiş”; “Son 2 haftanın ortalama hacmi, önceki 4 haftanın ortalamasından %20+ yüksek”; “50 veya 100 haftalık EMA civarında fiyatın tutunması”.
- Belirsiz kalanlar (YORUM): RSI/MACD periyotları; EMA çevresi ve tutunma ölçüsü; finansal verinin tarih ve düzeltme kuralları; takas yoğunluğu eşiği; stop ve çıkış.
- Tansu'nun kanıtı: Öneri ve anlatım örnekleri. 26.04 metni bu konuda kod ve tarama yazmaya başlayacağını belirtir.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Teknik katman günlük veriden haftalığa çevrilebilir. Bilanço, sektör ve takas için ek veri gerekir. Temel değerleme mevcut TASARIM §3 kapsamını genişletmez.
- Kaynak güveni: Birinci el kaynak; uygulama sınırları yukarıda korunur. Hazırlık K.

---

## 84. Uyarlanır orta hat: uç değer, Bollinger zarfı ve rejim okuması

- Kaynak: `tweet-uyarlanir-orta-hat-bollinger-kanal-1962954142168588682` (2025-09-02). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): “Günlük verilerden önce belirli bir pencereyle en düşük ve en yüksek değerler süzülüyor.” “Sonrasında bu değerlerin üzerine Bollinger zarfı uygulanarak aşırı uçlar yumuşatılıyor.” “Eğer fiyat bu hattın üzerinde kalıyor ve hat yukarı eğimli ise ana trendin yukarı olduğu kabul ediliyor.”
- Tanım (YORUM): Üst/alt uçlara zarf uygulanır, sınırlar tekrar törpülenir, iki hattın ortalaması orta hattı verir. Fiyat üstte ve hat yukarıysa yükseliş; fiyat altına sarkarken yataylaşma düzeltme; aşağı eğimli hattın üstüne çıkamama satış baskısı olarak anlatılır. Düz hatta ortalamaya dönüş düşüncesi vardır.
- Parametreler: Sayısal değer verilmeden pencere, zarf genişliği ve törpüleme miktarı tartışılır.
- Belirsiz kalanlar (YORUM): Uç süzme ve törpüleme hesabı, pencere uzunlukları, zarf katsayısı, eğim/temas toleransı ve emir kuralları.
- Tansu'nun kanıtı: Kavramsal sistem anlatımıdır; sonuç ölçümü sunulmuş sayılmaz.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Günlük fiyat verisi uygundur; hesap ayrıntıları kaynakta tamamlanmadığından birebir üretilemez.
- Kaynak güveni: Birinci el kaynak; uygulama sınırları yukarıda korunur. Hazırlık X.

---

## 85. Dönüş sinyallerini VEYA, teyidi VE ile birleştirme

- Kaynak: `tweet-veya-ve-sinyal-birlestirme-kurali-1987494513825259932` (2025-11-09). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): “alım = (sinyal_1 V sinyal_2 V sinyal_3) ^ sinyal_4” (09.11.2025, Ham).
- Tanım (YORUM): İlk üç dönüş sinyalinden en az biri ile dördüncü teyit aynı anda gereklidir. V işareti VEYA, ^ işareti bu kaynakta VE anlamındadır; programlama dilindeki XOR işlemi olarak kullanılmaz.
- Parametreler: Üç alternatif sinyal ve bir ortak teyit; değerler mantıksaldır.
- Belirsiz kalanlar (YORUM): Her sinyalin hesabı, barın kapanıp kapanmadığı, stop ve çıkış.
- Tansu'nun kanıtı: Mantık formülü; işlem performansı verilmiş sayılmaz.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Mantık uygulanabilir. Girdi sinyalleri tanımlanmadan bağımsız işlem kuralı değildir.
- Kaynak güveni: Birinci el kaynak; uygulama sınırları yukarıda korunur. Hazırlık K.

---

## 86. WMA vade seçimi ve 4/9/18 kesişimiyle long giriş/çıkış

- Kaynak: `tweet-wma-13-60-aylik-trend-1760919805035467002` (2024-02-23), `tweet-wma-4-9-18-kesisim-long-1761132314388521311` (2024-02-23). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): 23.02.2024: “13 günlük ve 60 günlük ağırlıklı hareketli ortalamalar kullanılmıştır.” “Bu periyotlar aylara yayılan trendler yakalamak için uygundur.” “9 günlük 18 günlüğü yukarı kestiğinde long, 4 günlük 9 günlüğü aşağı kestiğinde long kapat.”
- Tanım (YORUM): 13/60 seti aylara yayılan trend, 5/20 seti kısa vade için anlatılır. Ayrı üçlü kural WMA9'un WMA18'i yukarı kesişiminde long, WMA4'ün WMA9'u aşağı kesişiminde çıkış ister. THYAO kodunda doğrusal 1..n ağırlıklar kullanılır (görsel açıldı).
- Parametreler: 13/60 ve 5/20 vade örnekleri; 4/9/18 üçlü kuralı. “7 ile 10 gün arası trade için kullanılabilir.” (Ham).
- Belirsiz kalanlar (YORUM): Kesişim eşitlik sınırı, sinyal ile emir zamanı, stop ve maliyetler. Vade ifadesi zorunlu tutma süresine çevrilmez.
- Tansu'nun kanıtı: THYAO çizimleri ve sözlü strateji; sistematik sınama verilmiş sayılmaz.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Günlük kapanışla WMA ve kesişim kurulabilir; emir ve risk ayrıntıları gerekir.
- Kaynak güveni: Birinci el kaynak; uygulama sınırları yukarıda korunur. Hazırlık K.

---

## 87. WMA5/14/34/55 ile RSI50 teyit taraması

- Kaynak: `tweet-wma-5-14-34-55-rsi-50-kesisim-1845914750913520094` (2024-10-14), `tweet-wma-5-14-34-55-rsi14-50-1840770526240784672` (2024-09-30). Ham ve belirtilen görseller birinci eldir.
- Tansu'nun ifadesi (verbatim): 30.09.2024: “WMA olarak kodlayarak RSI14 > 50 ekledim.” 14.10.2024: “Son gün WMA(5_14_34_55) ve RSI 50 üzeri kesişme koşullarını sağlayan hisseler:” (Ham).
- Tanım (YORUM): WMA seti ile RSI teyidi birlikte taranır. Ham RSI14 der; açılan iki grafiğin üst başlığı RSI21>50, alt paneli RSI14 yazar. Bu fark çözülmeden tek kanonik RSI periyodu atanmaz. WMA'nın EMA ile değiştirilmesi aynı kural sayılmaz.
- Parametreler: WMA 5/14/34/55; RSI50 düzeyi ve son gün kesişimi ifadeleri. RSI14 Ham, RSI21 görsel başlık (çelişki korunur).
- Belirsiz kalanlar (YORUM): WMA koşulunun kesin ilişkisi; RSI dönemi ve düzey/kesişim ayrımı; giriş, stop, çıkış.
- Tansu'nun kanıtı: FADE ve KRDMB örnek çıktıları. Başarı oranı değildir.
- Günlük bedava veriyle uygulanabilir mi (YORUM): Günlük kapanışla göstergeler hesaplanabilir; belirtilen çelişki ve koşul ilişkisi açıklaştırılmalıdır.
- Kaynak güveni: Birinci el kaynak; uygulama sınırları yukarıda korunur. Hazırlık K.

---

## 88. Shrinking (daralan) mum formasyonu: beş mum, gövde daralması ve ikinci mum sınırı

- Kaynak: `tweet-shrinking-daralan-mum-formasyonu-1906298040333308407` (30.03.2025; Ham ve G2 kod görseli, G2 açıldı); `tweet-shrinking-pattern-sinyali-1906298792426541433` (30.03.2025; Ham ve PEHOL G1, açıldı). İkisi de Tansu'nun X gönderisidir.
- Tansu'nun ifadesi (verbatim):
  - Ayı, Ham: "Ayı Shrinking formasyonunda ise ilk mum çubuğu boğa yönünde olmalıdır." Ara mumlar: "her biri bir öncekine göre daha küçük olmalıdır."
  - Ayı, Ham: "Son olarak beşinci mum çubuğu ayı yönünde olmalı ve ikinci mum çubuğunun en düşük seviyesini kırmalıdır."
  - Boğa, Ham: "Boğa Shrinking formasyonunda, ilk mum çubuğu ayı yönünde olmalıdır." Ara mumlar: "Sonraki üç mum çubuğu herhangi bir renkte olabilir fakat her biri bir öncekine göre daha küçük olmalıdır."
  - Boğa, Ham: "Son olarak beşinci mum çubuğu boğa yönünde olmalı ve ikinci mum çubuğunun en yüksek seviyesini aşmalıdır."
  - Ayı kodu (G2, açıldı): `data[i, close_column] < data[i - 3, low_column]`; `data[i - 1, low_column] > data[i - 2, low_column]`; `data[i - 2, low_column] > data[i - 3, low_column]`.
  - Daralma kodu (G2, açıldı): `abs(data[i - 3, close_column] - data[i - 3, open_column]) < abs(data[i - 4, close_column] - data[i - 4, open_column])`. Aynı karşılaştırma i-2/i-3 ve i-1/i-2 için de yazılıdır. Sinyal: `data[i, sell_column] = -1`, yorum: "Aynı gün sat sinyali".
- Tanım:
  1. Okuma (YORUM): Beş mum 1–5 olarak numaralanır; kodda i beşinci mumdur. Gövde büyüklüğü `abs(Close-Open)` olarak okunur.
  2. Ayı örneğinin kodu: ilk mum `Close1 > Open1`, beşinci mum `Close5 < Open5`; ikinci, üçüncü ve dördüncü gövdeler sırayla küçülür. İkinci-dördüncü dipler yükselir: `Low4 > Low3 > Low2`. Beşinci kapanış ikinci dibin altındadır: `Close5 < Low2`. Bu koşullar birlikte sağlandığında beşinci muma sat sinyali yazılır (G2 kodu, açıldı).
  3. Boğa anlatımı ilk mumun ayı, beşincinin boğa olmasını ve aradaki üç mumun küçülmesini ister; beşinci mum ikinci mumun tepesini aşar (yukarıdaki Ham alıntıları). Okuma (YORUM): Ayı kodunun kapanış ve dip koşullarını ters çevirip boğa kodu diye sunmak ek yorum olur.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| Mum sayısı | 5 | Her iki Ham anlatımı |
| Ara mum rengi | Serbest | Ham |
| Ayı daralma ölçüsü | Mutlak gövde, üç ardışık sıkı küçülme | G2 kodu, açıldı |
| Ayı ara dipleri | Low4 > Low3 > Low2 | G2 kodu, açıldı |
| Ayı kırılımı | Close5 < Low2 | G2 kodu, açıldı |
| Ayı sinyal barı | Beşinci mum, sell = -1 | G2 kodu, açıldı |
| Boğa kırılımı | Beşinci mum ikinci mumun en yükseğini aşar | Ham |

- Belirsiz kalanlar: Boğa sürümündeki aşmanın kapanışla mı gün içi yüksekle mi ölçüleceği; ayı kodundaki ek dip diziliminin boğa karşılığı; sinyal sonrası emir, stop ve hedef seçimi. Okuma (YORUM): Bu seçimler ayı kodunun aynalanmasıyla kendiliğinden kaynaklı hâle gelmez.
- Tansu'nun kanıtı: Açılan PEHOL görseli "PEHOL.IS - Shrinking Pattern Sinyalleri" başlığını ve yön işaretlerini gösterir. Okuma (YORUM): Seçilmiş grafik örneği başarı oranı veya sınama sonucu değildir.
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): Günlük OHLC ile ayı dedektörü hesaplanabilir. Boğa dedektörü ve tam işlem sistemi için yukarıdaki seçimler gerekir.
- Kaynak güveni: Ham ve açılan kod birinci eldir. Ayı dedektörü açık; boğa kırılım uygulaması kısmen açıktır. Hazırlık K.

---

## 89. Slingshot mum kırılımı: ikinci tepe üstü kapanış ve mum sırası belirsizliği

- Kaynak: `tweet-slingshot-mum-kirilim-taramasi-1905953307723522064` (29.03.2025; Ham ve DOAS G1, açıldı). Tansu'nun X gönderisidir.
- Tansu'nun ifadesi (verbatim):
  - "ilk olarak bir boğa (yükseliş) mumu ile başlar."
  - "Ardından gelen ikinci mum daha da yukarıda kapanarak boğa eğilimini teyit eder."
  - "Sonrasında iki adet daha mum oluşur; bu mumların sonuncusu, öncekinin tepesini geçmez."
  - "formasyonun son mumu ilk mumun tepe seviyesine eşit veya daha aşağıda bir dip yapmalı"
  - "ikinci mumun tepe seviyesinin üzerinde kapanış yapmalıdır."
  - "İkinci ve üçüncü mumların renginde (yani yeşil ya da kırmızı olması) kesin bir kural yoktur."
- Tanım:
  1. Okuma (YORUM): İlk mum boğadır. İkinci mumun daha yukarıda kapanması, kendi açılışından yüksek kapandığını zorunlu kılmaz; dolayısıyla sonraki renk serbestliği cümlesi tek başına çelişki değildir.
  2. Okuma (YORUM): Son mum için iki karşılaştırma doğrudan okunur: `Low_son <= High1` ve `Close_son > High2` (yukarıdaki Ham alıntıları).
  3. Okuma (YORUM): İkinci mumdan sonra gelen iki mumun sonuncusuna tepe aşmama koşulu verilir. Sonraki gönderideki son mumun bu mum mu yoksa ek bir mum mu olduğu otomatik seçilmez. Bu nedenle dört ya da beş mumluk bir kod burada kaynak diye sunulmaz.
- Parametreler:

| parametre | değer | kaynak |
|---|---|---|
| İlk mum | Boğa | Ham |
| İkinci kapanış | Daha yukarıda kapanış | Ham; kıyasın tam kodu açık |
| Ara mum sınırı | Sonraki iki mumun sonuncusu öncekinin tepesini geçmez | Ham |
| Son mum dibi | İlk tepeye eşit veya altında | Ham |
| Son mum kapanışı | İkinci tepenin üzerinde | Ham |
| İkinci ve üçüncü renk | Serbest | Ham |
| Toplam mum sayısı / son mum indeksi | Kesinleştirilmedi | Okuma (YORUM): cümlelerin sıra ilişkisi açık soru |

- Belirsiz kalanlar: Son mumun sıra numarası; ikinci mumun daha yukarıda kapanmasının kıyas noktası; tepe geçmeme koşulunun son kırılım mumuyla ilişkisi; işlem emri, stop ve hedef seçimi. Sorunun yeri PR gövdesidir; uygulama kararı verilmeden sinyal kodu yazılmaz.
- Tansu'nun kanıtı: Ham: "Taraması da hazır." Açılan G1 başlığı "DOAS.IS - Mum Formasyonu Sinyalleri", lejantı "Buy Signal" ve "Sell Signal" der. Okuma (YORUM): Görseldeki işaretler mum indekslerini veya başarılı işlem oranını tek başına doğrulamaz.
- Günlük bedava veriyle uygulanabilir mi: Okuma (YORUM): OHLC karşılaştırmaları günlük veriyle hesaplanabilir; mum sırası çözülmeden birebir dedektör tamamlanamaz.
- Kaynak güveni: Ham ve açılan görsel birinci eldir; sözel sıra ilişkisi belirsizdir. Hazırlık K.
