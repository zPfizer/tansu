# Parça 03: kaynak-* (21) ve not-* (1)

Okuma tarihi: 06.10.2026. Kök: `...\beyin\kisisel\300-Projects\Tansu X Veri Havuzu\`.
Okunan: 22 dosya + ana not (`Tansu X Veri Havuzu.md`: yalnız Obsidian "base" dizini, strateji içeriği yok).
Dört dosya (ai-ml, awesome-econ, ekonometri, jansen) yalnız ilk 25-40 satırı okundu; başlıklarından strateji dışı olduğu belli. CME dosyası tam okundu.
Açılan görsel: 19 webp (aşağıda her kartta). Açılmayan: ekonometri PDF (strateji dışı).

Etiketler: **Birinci el** = Tansu'nun kendi aracının görsel çıktısı veya kendi tweet metni. **İkinci el** = notu yazan Claude'un özeti (tweet metni notta aynen yok). Tüm tweetler Tansu'ya aittir (X: @The_Tansu_). Notlar tweet metnini aynen vermez; "Tansu'nun ifadesi" satırları notun aktardığı kısa parçalardır (ikinci el özet) ya da görselden okunan yazıdır (birinci el).
Rakam kaynağı: [N] = notun metni, [G] = görselden ben okudum, [P] = görselden piksel ölçümüm (yaklaşık, kaynak vermiyor).

## 1. Dosya tablosu

| Dosya | Tür | Tek satır |
|---|---|---|
| kaynak-80-100-hafta-yatay-tarama | tarama | 80-100 hafta yatay kalan hisseyi bul, bant dibinde bekle. Formül yok, görsel yok. |
| kaynak-aefes-yukselen-kanal-alt-bant | strateji (giriş fikri) + yapı taşı (kanal) | Yükselen kanal alt bandına temas + tepki; Lookback 120, temas 3/3. Stop/hedef yok. |
| kaynak-ahenk-demand-... | strateji (formülsüz) | "Ahengin uyumu": demand kutusu + 3 osilatör paneli. Kural yok. |
| kaynak-akfis-breakout-fvg-retest | strateji | Konsolidasyon, kırılım, FVG, range-high retest, teyit, giriş; stop ve 3 TP çizgisi var. |
| kaynak-bom-iki-tavan | strateji (formülsüz) | BOM işareti sonrası "iki tavan" iddiası. Formül yok. |
| kaynak-cwene-dalga2-demand | strateji (senaryo, elle) | Elliott dalga 2 dibi + 32,5-36 demand örtüşmesi; seviyeli senaryo. |
| kaynak-cwene-skewness | filtre/etiket (momentum liste katmanı) + risk | 63 günlük rolling skewness sınıfları. AL/SAT değil. |
| kaynak-doas-kelebek | strateji (harmonik) | Bullish Butterfly, D 159,40 tamamlandı; oranlar görselde. |
| kaynak-dusen-yapi-kirilim | strateji (kırılım olayı) + yapı taşı (düşen üst sınır) | Daralan düşen yapının üst sınırını yeşil mumla aşma. Giriş/stop yok. |
| kaynak-dusen-yapi-retest | strateji (kırılım + retest) | Aynı yapı, kırılım sonrası çizgiye geri test. Giriş/stop yok. |
| kaynak-three-drives | strateji (harmonik/geometri) | Üç itiş: oran + zaman simetrisi; dönüş bölgesi, işlem kuralı yok. |
| kaynak-vakbn-garan-rotasyon | strateji (çift rotasyonu) | Z ±2 ile VAKBN/GARAN arası geçiş; rapor ve sonuçlar görselde. |
| kaynak-kointegrasyon-sinirlari | yapı taşı (çift seçimi filtresi) | Engle-Granger/Johansen ile ilişki sınama; korelasyon ≠ durağan spread. Strateji tarifi yok. |
| kaynak-xu100-1-eylul | piyasa filtresi (rejim) | WMA21 altı, 4s bearish CHoCH, SETUP 45/100 ve 35/100. |
| kaynak-xu100-bekle-teyit | piyasa filtresi (rejim) | "Bekle ve teyit": 14.722 üstü kalıcılık; SETUP 7/100 ve 13/100. |
| kaynak-xu100-corwin-schultz | filtre/risk göstergesi (likidite) | Günlük high/low spread tahmini + sigma. Yön sinyali değil. |
| not-backtest-giris-sadeligi-risk-islem-gunlugu | strateji değil (yöntem) | Backtest/risk/günlük ilkeleri. Aşağıda §4. |
| kaynak-cme-group-volatilite-opsiyon-veri-araclari | strateji değil | CME veri/araç haritası (futures opsiyon). BIST'e uygulanmaz. |
| kaynak-ai-ml-dl-veri-bilimi-kitap-reposu | strateji değil | Kitap reposu bağlantısı; içerik doğrulanmamış. |
| kaynak-awesome-econ-ai-stuff | strateji değil | AI skill şablonları reposu. |
| kaynak-ekonometri-hangi-soru-hangi-yontem-haritasi | strateji değil | 13 blok / 81 soru yöntem haritası (eğitim). |
| kaynak-stefan-jansen-ml-algo-trading | strateji değil | Kitap önerisi. |

## 2. Aday modül kartları

### M1. Çift rotasyonu (göreli değer): VAKBN ↔ GARAN
- **Tür:** strateji (giriş + geçiş çıkışı). Yapı taşı: çift seçimi (kointegrasyon, korelasyon, beta).
- **Kaynak:** `kaynak-vakbn-garan-rotasyon-2096358189696520213.md`; `assets/kaynak-vakbn-garan-rotasyon-2096358189696520213/rapor.webp`, `grafik.webp`. X: https://x.com/The_Tansu_/status/2096358189696520213 (üst tweet 2096357339926311405 konuyu "arbitraj hisseleri" yapıyor). Destek: `kaynak-kointegrasyon-sinirlari-2093658795700338821.md` (X: .../status/2093658795700338821).
- **Birinci/ikinci el:** rapor ve grafik birinci el (Tansu'nun aracının çıktısı). Kural metni yok; kural görselden çıkarım.
- **Tansu'nun ifadesi:** rapor başlığı "RELATIVE VALUE ROTATION | VAKBN <-> GARAN"; "SON GUN: YENI AL SINYALI | VAKBN AL | Y goreli ucuz, Z donusu +0.30" [G].
- **Kurallar (görselden):**
  - Y = VAKBN, X = GARAN [G]. Z-skor panelinde kesikli yatay çizgiler ±2 [G].
  - Giriş: Z ≤ −2 ve Z yukarı dönüyorsa "VAKBN AL"; Z ≥ +2 ve aşağı dönüyorsa "GARAN AL" [G, çıkarım]. Grafikte "VAKBN AL" etiketleri Z≈−2 civarında, "GARAN AL" etiketleri Z≈+2,2 ve ≈+4 civarında görülüyor [P].
  - Panel başlığı: "Z-Score ve T+1 Open Islemler" [G]: emir ertesi gün açılışında.
  - Çıkış: karşı uçta diğer hisseye geçiş. Stop/hedef görselde yok. İlk sinyale kadar nakit, sonra hep bir hissede [G: portföy çizgisi 100k'da düz, sonra hareketli; "Piyasada kalma %72,27"].
  - Parametreler: Z penceresi, spread formülü, ΔZ tanımı rakamla verilmemiş. Not: "Z donusu +0.30" = Son Z (−3,108) − Önceki Z (−3,404) = +0,296 [G, hesap].
  - Pencere ipucu [P]: normalize fiyat serisi ≈ Ocak 2025 başında başlıyor, Z serisi ≈ Mart sonunda başlıyor, yani ≈ 57-60 işlem günü gecikme. Bu 60 günlük pencere ile uyumlu ama kanıt değil.
  - Zaman dilimi: günlük (T+1 Open, işlem günleri).
- **Gösterdiği sonuç [G]:** başlangıç 100.000 TL, güncel 152.862,86 TL, net 52.862,86 TL; toplam getiri %52,86; 50/50 Buy&Hold %20,88; benchmark farkı etiketi +%31,99; Max DD −%27,44; Sharpe 0,929; Sortino 1,338; CAGR %28,93; geçiş 6; toplam maliyet 2.054,78 TL; piyasada kalma %72,27; Son Z −3,108; Önceki Z −3,404; rolling korelasyon 0,731; Beta 1,675; Beta CV 0,277; Cointegration p 0,048 (CURRENT); Pair Quality 55,600/100; Health GÜÇLÜ; Half-Life boş (birim: gün). Test aralığı yaklaşık Oca 2025 - Eki 2026 olarak okunuyor [P: eksen Nis 2025 ... Tem 2026]; bitiş tarihi okunamadı. 6 geçiş = grafikte sayılan 6 etiket (GARAN AL ×3, VAKBN AL ×3) [G].
- **Veri ihtiyacı:** günlük ham kapanış + açılış (T+1 Open) yeter. Gün içi, hacim, bilanço gerekmez. Ham (düzeltilmemiş) fiyat kullandığı notun önceki okumasında görülmüş; ben "14.05.2025 ipucu kutusu" X: 88,20, Y: 98,00 normalize değerlerini gördüm [G].
- **Belirsizlikler (bizim yorumumuz olmak zorunda):** Z'nin spread formülü ve penceresi; ΔZ'nin tek günlük mü olduğu; dolum ve maliyet modeli; çift seçimi (sonuca bakılarak seçilmiş olabilir); kointegrasyon kapısının işlevi (aşağıdaki çelişki).
- **Uygulanabilirlik: K.** Giriş eşiği, yön, T+1 ve rapor birinci elden; Z formülü ve pencere yorum. Yan ürün: sonuç rakamları sadakat hedefi olarak kullanılabilir.
- **Yapı taşı notu (kointegrasyon):** Tansu'nun savı: yüksek korelasyon durağan spread demek değil; Engle-Granger/Johansen önerir. Bu notun kesinlik iddiaları ("ortalamaya dönüş kesin", "makro şoklardan etkilenmez") Claude notunda yanlış diye işaretli; modüle eklenmez. Test: statsmodels `coint` (H0: eşbütünleşme yok).

### M2. Kırılım + FVG + Range-High Retest + Teyit ("A+ setup", AKFIS)
- **Tür:** strateji (giriş + stop + 3 TP çizgisi). Yapı taşı: konsolidasyon kutusu, FVG, retest.
- **Kaynak:** `kaynak-akfis-breakout-fvg-retest-2095523694881697974.md`; `assets/.../akfis.webp`, `alinti-ornek.webp`. X: https://x.com/The_Tansu_/status/2095523694881697974 (3 Eylül); alıntı: .../status/2095218573631279414 (2 Eylül, sembolsüz).
- **Birinci/ikinci el:** iki görsel birinci el (araç çıktısı). Sıra tarifi 2 Eylül tweetinde: Breakout → FVG → Retest → Confirmation [N, ikinci el özet].
- **Tansu'nun ifadesi:** başlık "AKFIS | Breakout + Range Retest + RSI Divergence | A+ SETUP | AL TETİKLENDİ | Sınıf: A+ | Skor: 100/100" [G]. Etiketler: KONSOLİDASYON, BREAKOUT, BULLISH FVG + CONFLUENCE, RANGE HIGH RETEST, CONFIRMATION, AL [G]. Lejant: Range High/Retest, Range Low, FVG %50, ENTRY, STOP, TP1, TP2, TP3, VolMA20, RSI 14 [G].
- **Kurallar:**
  - Sıra: yatay kutu (konsolidasyon) → kutu üstüne kırılım mumu → yeşil bullish FVG alanı (FVG %50 çizgisi lejantta) → fiyat range high'a geri döner (retest) → teyit mumu → AL.
  - AKFIS grafiği [P, eksen 3,5 ve 4 etiketli]: kutu ≈ 3,35-3,64; range high/retest ≈ 3,64; FVG ≈ 3,64-3,69; ENTRY ≈ 3,75; STOP ≈ 3,62 (FVG ve range high altı); üç TP çizgisi ≈ 3,87 / 3,94 / 4,00. Çizgilerin hangisinin TP1/TP2/TP3 olduğu renkten kesin okunamadı (lejant sırası altın, turuncu, mavi; çizgi sırası fiyatla monoton değil). R katları yaklaşık 0,9 / 1,4 / 1,9 (±0,3).
  - Alıntı örneği [P, eksen 100-150]: kutu ≈ 102,5-111; ENTRY ≈ 114; STOP ≈ 106,6 (FVG alt kenarı ≈ 107,4 altı); çizgiler ≈ 120,0 / 121,9 / 129,9 (R katları ≈ 0,7 / 1,0 / 2,0). Yani iki örnekte R katları aynı değil; sabit 1/1,5/2R kuralı görselden çıkmıyor.
  - Süre/tolerans/FVG tanımı/teyit koşulu/puan formülü yok. "RSI Divergence" başlıkta var, RSI paneli kırpımda görünmüyor [G]. Hacim paneli kırpık.
  - Zaman dilimi: belirtilmemiş (mumlar günlük gibi; doğrulanmadı).
- **Sonuç [G]:** AKFIS'te teyitten sonra uzun yeşil mum ≈ 3,87-4,25 aralığında, TP çizgilerinin üstüne çıkıyor [P]. Alıntı örneğinde ≈ 114'ten ≈ 145'e çıkış ve sonra düşüş [P]. Kesin getiri yazılı değil. Tek tarihli sonuç: 3 Eylül'de "AL TETİKLENDİ".
- **Veri ihtiyacı:** günlük OHLCV yeter (FVG = 3 mumluk boşluk; hacim yalnız VolMA20 için). Gün içi gerekmez.
- **Belirsizlikler:** konsolidasyon tespiti (süre, genişlik), FVG ve retest toleransı, teyit tanımı, puan, TP seviyelerinin kaynağı (ATR mi, R mi, FVG mi).
- **Uygulanabilirlik: K.** Olay sırası ve stop konumu (FVG/range high altı) birinci elden; tolerans ve TP formülü yorum.

### M3. Yükselen kanal alt bant teması + tepki (AEFES)
- **Tür:** strateji (giriş fikri, çıkışsız) + yapı taşı (kanal).
- **Kaynak:** `kaynak-aefes-yukselen-kanal-alt-bant-2096582181170598078.md`; `assets/.../aefes-kanal.webp`. X: https://x.com/The_Tansu_/status/2096582181170598078. Ek: `kaynak-80-100-hafta-yatay-tarama` aynı "alt bölge yakınlığı" temasına bağlanıyor (§M9).
- **Birinci el:** grafik başlığı ve değer satırı Tansu'nun aracından [G].
- **Tansu'nun ifadesi:** "AEFES — YÜKSELEN KANAL — ALT BANT TEMAS | Lookback: 120 | Temas: 2026-09-03 | Alt bant: 17.76 | Low: 17.92 | Low-Bant: +0.92% | Kapanış-Bant: +2.56% | Üst/Alt temas: 3/3 | Genişlik değişimi: +15.3% | ALT BANT TEMAS + TEPKİ" [G].
- **Kurallar:**
  - Kanal: son 120 mumda üst ve alt kesikli paralel-benzeri çizgiler; alt çizgi dip pivotlarına (≈16,0 ve ≈15,8 civarı [P]) oturuyor.
  - Temas: Low alt bandın %0,92 üstünde iken "temas" sayılıyor. Yani tolerans en az %0,92 (üst sınır okunamadı).
  - Tepki: temas mumundan sonra yeşil mumlar [G].
  - Giriş/stop/hedef: yok. Parametre: Lookback 120. Üst/Alt temas 3/3 = üstte 3, altta 3 temas [G].
  - "Genişlik değişimi +%15,3": hesabı yok (kanal genişliği, hangi iki an arası okunamadı).
  - Hacim MA21, RSI14, MACD, +DI/−DI panelleri lejantta [G]; sinyalde rolü yok (RSI 50 altı, MACD sıfır altı [G]).
  - Zaman dilimi: belirtilmemiş (günlük gibi).
- **Sonuç:** yok (tek örnek). Temas 03.09.2026; son iki mum yeşil [G].
- **Veri ihtiyacı:** günlük OHLCV yeter.
- **Belirsizlikler:** kanal çizim algoritması (pivot seçimi, paralellik), temas toleransı, "tepki" tanımı, stop, hedef, genişlik formülü.
- **Uygulanabilirlik: K.** Lookback ve çıktı alanları birinci elden; kanal yöntemi yorum; çıkış kuralı yok.

### M4. Düşen üst sınır kırılımı ve retest (sembolsüz)
- **Tür:** strateji (kırılım + retest olayı); giriş/stop/hedef yok. Yapı taşı: düşen kanal/takoz sınırı.
- **Kaynak:** `kaynak-dusen-yapi-kirilim-2096576027791131079.md` (`kirilim.webp`), `kaynak-dusen-yapi-retest-2096577500612624410.md` (`retest.webp`). X: .../status/2096576027791131079 ve .../status/2096577500612624410 (6 Eylül, 15:27 ve 15:33). İki görselin aynı hisse olduğu doğrulanmadı.
- **Birinci el:** görsel etiketleri araç çıktısı: "KIRILIM", "RETEST" [G].
- **Tansu'nun ifadesi:** "Canlanın:)" (ilk tweet); ikincisinde retest görünümünü olumlu buluyor, sonucu "tahtacı"ya bağlıyor [N].
- **Kurallar:** kırmızı düşen üst sınır + mavi düşen alt sınır, aralık daralıyor (takoz/üçgen gibi) [G]. Son mum uzun yeşil, üst sınırı aşıyor, hacim çubuğu önceki çubuklardan yüksek, RSI benzeri mor osilatör sağ uçta yukarı sıçrıyor [G]. İkinci görselde kırılım mumundan sonra çizgiye geri çekilme (RETEST etiketi) ve yeşil mum [G]. Temas sayısı, tolerans, kırılımın kapanışla mı tanımlandığı: ekranda yok. Önceki notlarda aynı aracın benzer çıktısında "Kırılım ... (Temas:N)" yazısı var (BOM, §M7) ama bu iki görselde görünmüyor.
- **Sonuç:** yok.
- **Veri ihtiyacı:** günlük OHLCV; hacim kırılım teyidi için istenirse. Mum periyodu okunamadı.
- **Belirsizlikler:** hepsi: pivot, çizgi uydurma, tolerans, kırılım koşulu, retest penceresi, stop, hedef.
- **Uygulanabilirlik: K (yalnız yapı tespiti), giriş/çıkış: X.** Not: önceki okumada LIDER/BALAT kayıtlarında Temas 3 ve Lookback 20/30 parametreleri vardı; bu parçada bu rakamlar yok.

### M5. Bullish Butterfly (DOAS)
- **Tür:** strateji (harmonik tamamlanma bölgesi); giriş/stop/hedef yok.
- **Kaynak:** `kaynak-doas-kelebek-2096505383955079277.md`; `assets/.../doas-kelebek.webp`. X: https://x.com/The_Tansu_/status/2096505383955079277 (6 Eylül 10:46).
- **Birinci el:** görsel araç çıktısı.
- **Tansu'nun ifadesi:** "D: 159,40 [TAMAMLANDI]"; etiketler: "1.272 (D hedefi): 159.49", "1.618 (max risk): 146.00" [G].
- **Kurallar (görselden):** Fibonacci ölçeği XA üzerinde: 0,0 = A = 209,10; 0,236 = 199,90; 0,382 = 194,20; 0,500 = 189,60; 0,618 = 185,00; 0,786 = 178,45; 1,0 = X = 170,10; 1,272 = 159,49; 1,618 = 146,00 [G]. X alçak, A yüksek (bullish). B ≈ 178,45 = XA'nın 0,786 geri çekilmesi [G, aynı seviye]. C ≈ 198 (0,236-0,382 arası) [P]; kesin C okunamadı. D, X'in altında: 159,40 ≈ XA'nın 1,272 uzantısı [G]. 1,618 "max risk" olarak etiketli; stop kuralı mı olduğu doğrulanmadı. D'de son mum yeşil [G]. Aşağı eğimli nokta çizgisi C→D ve XB mavi çizgisi var [G].
- **Sonuç:** yok; D sonrası tek yeşil mum.
- **Veri ihtiyacı:** günlük OHLCV (pivot). Mum periyodu okunamadı.
- **Belirsizlikler:** pivot ayarı, oran toleransı, BC/AB aralığı, giriş (D'de mi, teyitle mi), stop (1,618 mi), hedef (yukarı hedef yok), tepki penceresi.
- **Uygulanabilirlik: K.** Butterfly oranları (B 0,786 XA, D 1,272 XA) görselde net; işlem kuralları yok. "D hedefi" aşağı yönlü projeksiyon, kâr hedefi değil.

### M6. Three Drives (üç itiş)
- **Tür:** strateji (geometri/harmonik, dönüş bölgesi); işlem kuralı yok.
- **Kaynak:** `kaynak-three-drives-2096510322190201208.md`; `assets/.../three-drives.webp`. X: https://x.com/The_Tansu_/status/2096510322190201208 (6 Eylül 11:06).
- **Ele:** kural metni notta tweet özeti (ikinci el, aynen alıntı yok; not "tarayıcıda okundu" diyor). Görsel birinci el.
- **Tansu'nun ifadesi (not):** "Üç İtiş, trend yönünde üç yeni ekstrem ile Fibonacci, fiyat ve zaman simetrisinin birlikte değerlendirildiği olası dönüş yapısı" [N].
- **Kurallar [N]:** alış yönü giderek düşen üç dip; satış yönü giderek yükselen üç tepe. Ara düzeltmeler ≈ %61,8 veya %78,6. Sonraki itişler önceki düzeltmenin 1,272 veya 1,618 uzatması. A→Drive 2 ve C→Drive 3 bacakları uzunluk ve süre bakımından yakın (AB=CD mantığı). Süre: 10 bara karşı 11-12 bar dengeli, 8 bara karşı 30 bar dengesiz. Drive 3 = olası dönüş bölgesi; doğrudan ters işlem değil; güçlü trendde başarısız olabilir; fiyat tepkisi izlenmeli.
  - Görsel [G]: X, Drive 1, A, Drive 2, C, Drive 3 etiketleri; üç yükselen tepe (satış yönlü örnek) sonra düşüş. Tarih ekseni var (Haz 28 - Ağu 23), fiyat ekseni yok. Bar sayıları [P, günlük varsayımı]: A→Drive 2 ≈ 4 bar, C→Drive 3 ≈ 4 bar.
  - Giriş/stop/hedef/tolerans: yok.
- **Sonuç:** yok; seçilmiş tek örnek.
- **Veri ihtiyacı:** günlük OHLCV; oranlar fiyat ekseni olmadan doğrulanamadı.
- **Belirsizlikler:** pivot ve onay gecikmesi, oran/zaman toleransı, ilk itişin ölçüm başlangıcı (X→Drive1 mi), reaksiyon şartı, ters yön işlemi (BIST'te açığa satış yok), stop.
- **Uygulanabilirlik: K** (tespit için oranlar belli; işlem kuralı X).

### M7. BOM sinyali
- **Tür:** strateji (formülsüz).
- **Kaynak:** `kaynak-bom-iki-tavan-2093647837162553475.md`; `assets/.../bom.webp`. X: https://x.com/The_Tansu_/status/2093647837162553475 (29 Ağustos).
- **Tansu'nun ifadesi (not):** uygun şartlarda BOM sinyali etkili olabilir, örneğin art arda iki tavan [N].
- **Kurallar:** yok. Görselde (sembolsüz, günlük gibi): siyah üçgen "BOM" etiketi, çevresinde kırmızı kutu; sonrasında yeşil yükseliş mumları; turuncu trend çizgileri "Kırılım 2026-06-18 (Temas:7)" ve "Kırılım 2026-07-24 (Temas:5)" (küçük yazı, kısmen okunabildi); CHoCH etiketleri; üstte sarı arz, altta mavi talep kutuları; sağda hacim profili; altta hacim ve çift çizgili osilatör [G]. "Uygun şartlar" tanımsız.
- **Sonuç:** seçilmiş olumlu örnek; "iki tavan" doğrulanamaz.
- **Veri ihtiyacı:** bilinmiyor (formül yok).
- **Uygulanabilirlik: X.**

### M8. AHENK (demand + gösterge uyumu)
- **Tür:** strateji (formülsüz).
- **Kaynak:** `kaynak-ahenk-demand-2094486927328059452.md`; `assets/.../ahenk.webp`. X: https://x.com/The_Tansu_/status/2094486927328059452 (31 Ağustos).
- **Tansu'nun ifadesi (not):** "Ahengin uyumu"; geliştirmeyi önemli buluyor [N].
- **Kurallar:** yok. Görselde [G]: "DEMAND / TOPLAMA" kutusunda yataylaşma sonrası yükseliş; mor ortalama çizgisi (WMA benzeri, adı yok); üç alt panel (MACD benzeri, bantlı RSI benzeri, WaveTrend benzeri); sol altta "38.50" yazılı yeşil yatay çizgi; son mum aşağı. Sembol, zaman dilimi, eşikler okunamadı.
- **Uygulanabilirlik: X.**

### M9. 80-100 hafta yatay hisse taraması
- **Tür:** tarama (aday seçici).
- **Kaynak:** `kaynak-80-100-hafta-yatay-tarama-2096580811080261784.md`. X: https://x.com/The_Tansu_/status/2096580811080261784 (6 Eylül 15:46). Görsel yok.
- **Birinci el:** tweet metni (notun özeti): "80-100 hafta yatay kalan bir hisseyi bulup alt bölgede beklemek sade bir strateji; taramasını yazma niyeti" [N].
- **Kurallar:** süre 80-100 hafta (mum periyodu belirtilmemiş; "hafta" geçtiği için haftalık okuma doğal, ama doğrulanmadı). Yataylık eğimi, bant genişliği, "alt bölge" eşiği, evren, giriş zamanı, stop, çıkış, bekleme süresi: yok.
- **Sonuç:** yok.
- **Veri ihtiyacı:** haftalık/günlük OHLCV yeter (80-100 hafta = 1,5-2 yıl geçmiş).
- **Belirsizlikler:** hepsi. Tansu kodu paylaşmadı.
- **Uygulanabilirlik: X** (yalnız fikir; bizim yorumumuzla "bant = son N haftanın yüksek/düşük aralığı, eğim ≤ eşik, fiyat alt %q" yazılabilir ama bu bizim stratejimiz olur). Önceki okumada (docs/kurallar) bu not yok.

### M10. CWENE Elliott dalga 2 + demand örtüşmesi
- **Tür:** strateji (senaryo, elle çizim); seviyeli.
- **Kaynak:** `kaynak-cwene-dalga2-demand-2094128312729624792.md`; `assets/.../elliott.webp`, `demand.webp`. X: https://x.com/The_Tansu_/status/2094128312729624792 (30 Ağustos).
- **Birinci/ikinci el:** seviyeler tweet metninden (not özeti); görsel birinci el ama eksen değeri yok [G].
- **Tansu'nun ifadesi (not):** 33,10→48,30 Dalga 1; ≈35 dip olası Dalga 2; 32,5-36 demand ile örtüşme olumlu; ana kırılım henüz yok [N].
- **Kurallar [N]:** 35-36 = dalga 2 senaryosu için korunacak destek; 37-38 hacim/denge; 40-41,5 ilk ciddi direnç; 44-48,5 güçlü supply; 48,30 üzeri kapanış = Dalga 1 tepesini geri alma (Dalga 3 senaryosu güçlenir); 33,10 altı = senaryo iptali. Görsel [G]: 0, 1, "2?" noktaları (aday, kesin sayım değil); mavi demand, sarı supply, sağda hacim profili.
- **Sonuç:** yok. Son mumda dipten yeşil tepki.
- **Veri ihtiyacı:** günlük OHLCV. Dalga sayımı otomatikleştirilemez.
- **Uygulanabilirlik: X** (seviyeler elle; sayım formülü yok). "48,30 üstü kapanış / 33,10 altı iptal" ayrı basit kural olarak yazılabilir ama bu bizim yorumumuz.

### M11. XU100 rejim okuması: WMA21 + CHoCH + SETUP puanı + "bekle ve teyit"
- **Tür:** piyasa filtresi (endeks rejimi). Hisse girişi değil.
- **Kaynak:** `kaynak-xu100-1-eylul-2094850165920403866.md` (`gunluk.webp`, `4-saat.webp`; X .../status/2094850165920403866, 1 Eylül) ve `kaynak-xu100-bekle-teyit-2095196517577461974.md` (`gunluk.webp`, `4-saat.webp`; X .../status/2095196517577461974, 2 Eylül).
- **Birinci el:** başlık satırı ve etiketler araç çıktısı [G]; metindeki yorum notun özeti.
- **Tansu'nun ifadesi:** başlıklar: "XU100.IS | GÜNLÜK 14229.01 | DEMAND: 4 | SUPPLY: 2 | BULL FVG AKTİF: 11 | BEAR FVG AKTİF: 2 | YAPI: GEÇİŞ / BULLISH CHoCH | SETUP: 45/100 | GÖRSEL: ODAK" (1 Eylül günlük); 4 saatlik: "14226.96 | ... BULL FVG 12 | BEAR FVG 6 | GEÇİŞ / BEARISH CHoCH | SETUP: 35/100". 2 Eylül günlük: "14050.56 | ... BULL FVG 11 | BEAR FVG 3 | SSL/BSL: 0/4 | GEÇİŞ / BULLISH CHoCH SEVİYESİ KAYBEDİLDİ | SETUP: 7/100"; 4 saatlik: "14054.50 | BULL FVG 10 | BEAR FVG 8 | SSL/BSL 1/0 | GEÇİŞ / BEARISH CHoCH AKTİF | SETUP: 13/100" [G].
- **Kurallar (metin [N], sayısal kısmı zayıf):**
  - Fiyat aşağı eğimli WMA21 altında ve dönüş teyidi yok (1 Eylül). WMA21 geri alma eşiği 14.443,45; son kısa vadeli tepe 14.722,02; ilk bearish FVG direnci 14.230,73-14.301,92; bullish FVG desteği 14.140,43 altına kalıcı geçiş = kayıp; en yakın demand 13.633,00-13.659,74 (görselde yazı bulanık, 13633/13833 ayırt edilemedi) [N].
  - 2 Eylül: ilk olumlu eşik ≈ 14.722 üzerinde kalıcılık; dirençler 14.740-14.876, 14.868-14.992, 15.133-15.205; toparlanmayı zayıflatan alt seviye ≈ 13.739; daha aşağı ≈ 13.000 [N]. Not "kalıcı" tanımsız.
  - Görselde okunan bölgeler [G]: SUPPLY 15133,50-15204,90 ve 14734,50-14876,10; DEMAND 12966,30-13056,65, 12601,60-12898,20, 11102,20-11172,60 (günlük); 4s: DEMAND 13216,16-13273,44, 12876,31-12934,32. 4 saatlik: "DÜŞEN TREND | TARİHSEL/KIRILMIŞ | TEMAS: 8", "YÜKSELEN TREND | YENİ KIRILDI | TEMAS: 7".
  - SETUP puanı: formül yok. Günlük 45 ve 4s 35 aynı gün; farklı zaman dilimi farklı puan.
  - Gösterge parametreleri görselde: WMA Close 21, MACD 12 26 9, RSI 14 | 70 / 30, WT 10 21 | 60 53 -53 -60 [G].
- **Sonuç:** yok (güncel durum görüşü).
- **Veri ihtiyacı:** XU100 günlük + 4 saatlik OHLCV (4 saatlik için gün içi veri; yfinance BIST 4s güvenilirliği doğrulanmadı). WMA21/MACD/RSI günlükten hesaplanır. Katılım ("geniş hisse katılımı zayıf") için bileşen verisi gerekir ama ölçü verilmemiş.
- **Belirsizlikler:** CHoCH/BOS pivot kuralı, FVG kalıcılık, SETUP formülü, "kalıcı".
- **Uygulanabilirlik:** WMA21 altı/üstü filtresi **K** (parametre 21, kapanış tabanlı, birinci elden); CHoCH/SETUP puanı **X**.

### M12. Corwin-Schultz spread + sigma (likidite/risk göstergesi)
- **Tür:** filtre/risk göstergesi (yön sinyali değil). Sonraki modül: işlem maliyeti/likidite uyarısı.
- **Kaynak:** `kaynak-xu100-corwin-schultz-2096145981062475910.md`; `assets/.../spread-sigma.webp`. X: https://x.com/The_Tansu_/status/2096145981062475910 (5 Eylül).
- **Birinci el:** grafik araç çıktısı [G]; yorum notun özeti.
- **Tansu'nun ifadesi (not):** düşük sigma + yüksek spread = sakin görünen ama kırılgan piyasa; yön sinyali değil [N].
- **Kurallar:** günlük high/low'dan Corwin-Schultz (2012) spread tahmini; panel başlığı "Corwin-Schultz Bid-Ask Spread 21 Gunluk" ve "Volatilite Tahmini Sigma" [G]. Referans kutusu: Ortalama 1,088%, Medyan 0,454%, P75 1,899%, P90 3,028% [G]. Son spread ≈ %2,15 [N]; XU100 20 gün getirisi ≈ %1,45 [N]. Spread çok sayıda günde tam sıfır (negatif tahminin sıfıra kırpılması olabilir, yorum). Sigma formülü, eşikler ("yüksek"/"düşük"), 21 günün ortalama mı pencere tahmini mi olduğu belli değil.
- **Veri ihtiyacı:** günlük high/low yeter. Gerçek bid/ask yok; tahmin quote değil.
- **Uygulanabilirlik: K** (yöntem açık literatür formülü; Tansu'nun sigma ve eşikleri yorum).

### M13. 63 günlük rolling skewness (momentum liste etiketi)
- **Tür:** filtre/etiket (momentum liste katmanı) + risk bağlamı. AL/SAT değil.
- **Kaynak:** `kaynak-cwene-skewness-2094148699769241961.md`; `assets/.../cwene-skewness.webp`. X: https://x.com/The_Tansu_/status/2094148699769241961 ve .../status/2094148704089587805 (30 Ağustos).
- **Birinci el:** iki tweet metni (notta özet) ve görsel.
- **Tansu'nun ifadesi (not):** çarpıklığı AL/SAT yerine momentum, volatilite ve kuyruk riskiyle birlikte yorumluyor; kodu log getiri, skewness, kurtosis, 63 günlük rolling skewness ve Gaussian/Cornish-Fisher VaR hesaplıyor [N].
- **Kurallar:** pencere 63 işlem günü [G başlık: "63 Günlük Rolling Skewness"; çizgiler ±0,5 noktalı, 0 kesikli [G]]. Sınıflar [N]: < −0,50 belirgin negatif; −0,50..0 hafif negatif; 0..+0,50 hafif pozitif; > +0,50 belirgin pozitif; > +1 ise birkaç büyük günün etkisini kontrol et. Eşik eşitlikleri tanımsız. CWENE son değer ≈ +0,2/+0,3 → "güçlü pozitif rejim değil" [N, G: son uç 0-0,5 arası].
  - Görsel [G]: günlük getiri histogramı + Gaussian eğri; skewness 2024'te ≈ +1, 2025 Mart-Haziran ≈ −1'e iniyor, Temmuz 2025'ten sonra tekrar pozitif, 2026'da düşüyor; fiyat 2025 ortası dibinden (≈ 13) 2026'da ≈ 35-47'ye [P].
  - Giriş/stop/hedef yok.
- **Sonuç:** yok.
- **Veri ihtiyacı:** günlük kapanış yeter.
- **Belirsizlikler:** skewness tahmincisi (düzeltmeli/düzeltmesiz), kurtosis tanımı, VaR parametreleri (kullanılmayacaksa gerekmez).
- **Uygulanabilirlik: H** (etiket olarak). Strateji girişi değil; bir tarama sütunu.

## 3. Strateji olmayan / kısa geçilen notlar
- `kaynak-cme-group-volatilite-opsiyon-veri-araclari`: CME futures opsiyon veri/araç haritası; BIST hissesi değil. Strateji değil. İleride VRP/implied move için referans.
- `kaynak-ai-ml-dl-veri-bilimi-kitap-reposu`, `kaynak-awesome-econ-ai-stuff`, `kaynak-ekonometri-hangi-soru-hangi-yontem-haritasi`, `kaynak-stefan-jansen-ml-algo-trading`: kaynak/eğitim önerisi; strateji yok.

## 4. Tansu'nun backtest ilkeleri (`not-backtest-giris-sadeligi-risk-islem-gunlugu`)
Kaynak: Tansu'nun 2 Eylül 2026 21:13 tweeti (X: https://x.com/The_Tansu_/status/2095213493133713664) ve 20:24 tweeti (.../status/2095201144544846208). Not tweeti özetliyor; ilkeler Tansu'nun, "kullanılabilir sentez" bölümü Claude'un.
1. Adayları geriye dönük izle (örnek: 26 Ağustos'ta seçilenlerin 1, 3 ve 5 gün sonrası).
2. Aday tiplerini karşılaştır: "Daily iyi + 4H bullish CHoCH + RS güçlü + Demand/FVG desteği" kazandırıyor mu? Retest beklemek yarar sağlıyor mu yoksa girişi fazla mı geciktiriyor? (Cevaplar yok; test edilecek sorular.)
3. Girişi sadeleştir: Market Structure ve fiyat davranışı ana motor; RSI, MACD, WaveTrend, RS yardımcı teyit. Hepsinin aynı anda yeşil olması gerekiyor mu diye veriyle sorgula.
4. Riski merkeze koy: pozisyon büyüklüğü stop mesafesine göre. Belirli yüzde önerilmemiş.
5. İşlem günlüğü: aday tarihi → giriş → giriş gerekçesi → invalidation → TP → sonuç → MFE/MAE. Birkaç ay kayıt.
6. Yalnız katkı sağlayan filtreyi tut; katkısız olanı sadeleştir.
- Analiz sırası (Tansu, 20:24 tweeti): fiyatın bulunduğu bölge → kırılımlar → likidite hareketleri → 4 saatlik teyit; indikatör AL sinyaliyle başlama. Manuel analiz şablonu koşul-sonuç-gerekçe olarak koda aktarılmış (şablon ve kod paylaşılmadı).
- Sayısal eşik, risk %, örneklem büyüklüğü, maliyet modeli, çıkış kuralı: yok.

## 5. Ortak yapı taşları ve tekrar eden fikirler
| Yapı taşı | Geçtiği notlar |
|---|---|
| Pivot (tepe/dip) ve çizgi uydurma | AEFES, düşen yapı ×2, DOAS, Three Drives, BOM, CWENE dalga, XU100 (HH/HL/LH/LL). Hiçbirinde pivot ayarı yok. |
| Fibonacci (0,236...1,618) | DOAS (görselde tam ölçek), Three Drives (0,618/0,786; 1,272/1,618), CWENE dalga (seviyeler fiyatla) |
| Kanal/takoz sınırı + temas sayısı | AEFES (3/3), düşen yapı ×2, BOM (Temas:7, Temas:5), XU100 4s (Temas 8, Temas 7), 80-100 hafta bant |
| FVG (bullish/bearish, %50) | AKFIS, XU100 (FVG sayıları), not-backtest (aday tipi) |
| Demand/Supply (arz-talep) kutusu | AHENK, BOM, CWENE, XU100 |
| CHoCH / BOS / SSL-BSL sweep | XU100 ×2, BOM, not-backtest |
| Retest / teyit | AKFIS, düşen yapı retest, not-backtest (retest gecikme sorusu) |
| WMA21, MACD 12-26-9, RSI 14, WT 10-21 | XU100, AEFES, AHENK, düşen yapı |
| Hacim profili / VolMA | BOM, CWENE, AKFIS (VolMA20), AEFES (Hacim MA21) |
| Z-skor / kointegrasyon / beta | VAKBN-GARAN, kointegrasyon notu |
| Yüksek/düşük tabanlı istatistik (CS spread, skewness) | XU100 CS, CWENE skewness; momentum liste katmanı |
| Puan (SETUP x/100, Skor 100/100, Pair Quality /100) | XU100, AKFIS, VAKBN-GARAN: formülü hiçbirinde yok |

Aynı fikir birden çok notta: "alt bölgede/dipte tepki" (AEFES, 80-100 hafta bant, CWENE demand, DOAS D bölgesi); "kırılım ardından geri test" (AKFIS, düşen yapı, not-backtest).

## 6. Önceki okumayla (docs/KURALLAR.md, docs/kurallar/*) karşılaştırma
1. **En önemli çelişki/eksik: çift rotasyonunda ek kapı.** Önceki kural "Z ≤ −2 ve ΔZ > 0 → ertesi gün Y'ye geç; ilk sinyale kadar nakit" yazıyor ve Mart-Mayıs 2025'in sinyalsizliğini yalnız "sapma formülü" belirsizliği olarak kaydediyor. Grafikte [G/P] Z ≈ −2,3 ve ≈ −2,0 civarına Nisan 2025'te iniyor ve yukarı dönüyor, ama işlem etiketi yok; portföy çizgisi ≈ Haziran sonuna kadar 100k'da düz. Tüm panellerde arka plan gölgesi tam o noktada (≈ Haz 2025) başlıyor, bir geçerlilik/sağlık dönemi gibi duruyor (lejantta açıklaması yok; yorum). Sonuç: kuralda Z eşiği dışında bir kapı (kointegrasyon/Pair Health) olabilir. Bu, önceki "ΔZ yeterli, tek koşul" yorumunu zayıflatır.
2. AKFIS TP katları: önceki "~1/1,5/2R" ölçümü AKFIS grafiğinde ≈ 0,9/1,4/1,9R ile uyuyor ama alıntı (sembolsüz) örnekte ≈ 0,7/1,0/2,0R; çizgi renkleri lejantla fiyat sırasında örtüşmüyor. Sabit katlar kesin değil.
3. 80-100 hafta yatay tarama notu önceki dizinde yok (docs/kurallar'da "80-100" araması boş). Yeni aday (X sınıfı).
4. Düşen üst sınır kırılımı ve retest (iki 6 Eylül tweeti) önceki dizinde yalnız LIDER/BALAT/AKSGY bağlamında; bu iki not ayrı aday olarak yok.
5. Corwin-Schultz referans kutusunda P75 1,899% ve P90 3,028% var [G]; notta yok.
6. Three Drives: önceki okuma kural metnini "ikinci el" diye ayırmış; katılıyorum (notta aynen alıntı yok). Fiyat ekseni yok bilgisi doğru. Önceki okumada bar sayıları verilmemişti; ben [P] A→D2 ≈ 4, C→D3 ≈ 4 bar ölçtüm (zaman simetrisi var).
7. DOAS: önceki "B = 0,786" doğrulandı; ek olarak D = 1,272 XA ve 1,618 = "max risk" etiketi görselde. Yani Butterfly için oran çekirdeği birinci elden (önceki "K" doğru, "bazı oranlar" dar anlatım).
8. Önceki okumayla çelişmeyen: AEFES (Lookback 120, 3/3, +%15,3, alt bant 17,76), BOM/AHENK = X, XU100 SETUP puanları.

## Tansu'nun bakış açısı (ipuçları)

Uyarı: alıntıların çoğu notlardaki Claude özetidir (Tansu'nun aynen sözü değil); (G) = görselde yazan, birinci el. "Yorum:" satırları bana aittir.

**Piyasa/rejim**
- "Fiyat aşağı eğimli WMA21 altında; dönüş teyidi yok" (kaynak-xu100-1-eylul). Yorum: trendi ortalamanın eğimi ve fiyatın konumuyla okuyor.
- "tepki yükselişi trend dönüşü sayılmıyor"; "panik bulunmadığını ancak geniş hisse katılımının zayıf olduğunu savunuyor" (kaynak-xu100-bekle-teyit). Yorum: yerel tepki, ana yapı ve katılım ayrı katmanlar.
- "düşük sigma ve yüksek spread birleşimini sakin görünen fakat kırılgan olabilecek piyasa" (kaynak-xu100-corwin-schultz); spread/sigma "yön sinyali olarak kullanmıyor". Yorum: likiditeyi yön değil kalite/risk ölçüsü sayıyor.
- Görsel başlıkları "YAPI: GEÇİŞ / BULLISH CHoCH", "SEVİYESİ KAYBEDİLDİ" (G, xu100 notları). Yorum: rejimi pivot yapısı (CHoCH/BOS) ile etiketliyor; iki zaman diliminde farklı yapı/puan kabul ediyor (günlük 45/100, 4s 35/100).
- Şişman kuyruk: "çarpıklığı AL/SAT yerine momentum, volatilite ve kuyruk riskiyle birlikte yorumluyor" (kaynak-cwene-skewness).

**Kurulum seçimi / confluence**
- "32,5–36 demand alanıyla örtüşmeyi olumlu buluyor" (kaynak-cwene-dalga2-demand); görselde "BULLISH FVG + CONFLUENCE" (G, kaynak-akfis). Yorum: dalga sayımı, arz-talep ve FVG'nin örtüştüğü bölgeyi tercih ediyor; Claude notu bu "bağımsızlığı" istatistiksel kanıt saymıyor (not yazarının eleştirisi, Tansu'nun değil).
- "Ahengin uyumu"; "geliştirmeyi önemli bulduğunu söylüyor" (kaynak-ahenk-demand). Yorum: yapı + üç osilatörün birlikte uyumunu arıyor, kuralı vermiyor.
- "Girişi sadeleştir: Market Structure ve fiyat davranışı ana motor; RSI, MACD, WaveTrend ve RS yardımcı teyit" (not-backtest). Yorum: confluence'ta yapı baskın, göstergeler ikincil.
- "Analize indikatörün AL sinyaliyle başlanmıyor"; sıra: "bölge → kırılımlar → likidite hareketleri → 4 saatlik teyit" (not-backtest, 20:24 tweeti özeti).
- "80–100 hafta yatay kalan bir hisseyi bulup alt bölgede beklemeyi sade bir strateji" (kaynak-80-100-hafta). Yorum: "sade" olanı seviyor.

**Giriş teyidi**
- "Breakout → FVG → Retest → Confirmation" (kaynak-akfis, 2 Eylül tweeti özeti); görselde "RANGE HIGH RETEST", "CONFIRMATION" (G).
- Retest görünümünü "olumlu" buluyor, "yükselişin gerçekleşip gerçekleşmeyeceğini belirsiz bırakıyor ve sonucu 'tahtacı'ya bağlıyor" (kaynak-dusen-yapi-retest). Yorum: kurulumu olasılık olarak sunuyor.
- Three Drives: "Drive 3 olası dönüş bölgesi; doğrudan ters işlem gerekçesi değil... fiyat reaksiyonu izlenmeli"; "Güçlü trendde uzatma aşılabilir ve yapı başarısız olabilir" (kaynak-three-drives, not özeti). Yorum: bölge = tetik değil, tepki bekleniyor.
- XU100: "ilk olumlu eşik, üzerinde kalıcılık" (kaynak-xu100-bekle-teyit); "bekleme ve fiyat teyidi arama yaklaşımı". Yorum: tek eşik aşımı yetmez, kalıcılık ister (kalıcılık tanımı yok).
- "Retest beklemenin önemini AKSGY grafiğiyle anlattı. MACD toparlanma sinyali yanıltıcı oldu. Hacim bu hareketi hiç desteklemedi" (önceki okuma, docs/kurallar/E; bu parçada okunmadı, yalnız çapraz kontrol için).

**Risk, pozisyon, stop/hedef**
- "Riski merkeze koy: Güzel setup tek işlemde büyük sermaye riski için gerekçe olmasın. Pozisyon büyüklüğü stop mesafesine göre hesaplansın" (not-backtest).
- Araç çıktılarında her kurulumda ENTRY, STOP, TP1-TP3 çizgisi (G, kaynak-akfis); DOAS'ta "1.618 (max risk): 146.00" (G); CWENE'de "33,10 altı" iptal ve "48,30 üzeri kapanış" teyit (kaynak-cwene-dalga2-demand). Yorum: her kurulumun bir geçersizlik seviyesi ve kademeli hedefi var; stop genelde yapı/FVG altında.
- İşlem günlüğü: "Aday tarihi → giriş → giriş gerekçesi → invalidation → TP → sonuç → MFE/MAE" (not-backtest).

**Backtest/doğrulama**
- "Kuralları gösterge sayısıyla değil, adayların ve işlemlerin ölçülen sonuçlarıyla doğrula" ve "katkısı gösterilmeyen filtreleri sırf teknik görünmek için koruma" (not-backtest özeti). "Birkaç aylık kayıtla gerçek istatistik oluştur."
- Test soruları: "Retest beklemek yarar sağlıyor mu, yoksa girişi fazla mı geciktiriyor?" (not-backtest). Yorum: sonuç yok, kendi kuralını henüz sınamadığını kabul ediyor.
- VAKBN-GARAN raporunda kendi sonucunu al-tutla kıyaslıyor: "50/50 Buy&Hold +20.88%", "Max Drawdown -27.44%", maliyet 2.054,78 TL, "T+1 Open Islemler" (G). Yorum: maliyet, drawdown, benchmark ve gerçekçi dolum raporluyor.
- Kointegrasyon: "yüksek korelasyonun durağan spread anlamına gelmediğini"; Engle-Granger/Johansen önerir (kaynak-kointegrasyon). Aynı not Tansu'nun "matematiksel ispat", "kesin" benzeri kesinlik iddialarını düzeltmiş (Claude düzeltmesi).

**Araç zinciri (tarama → filtre → tetik → yönetim)**
- "taramasını yazma niyeti" (kaynak-80-100-hafta); araç çıktısı başlıkları "Eşleşen Patern / Tarama eşleşmesi" önceki okumada (docs/kurallar/C). Yorum: önce tarama, sonra görsel kurulum etiketi, sonra ENTRY/STOP/TP; filtre olarak skewness: "momentum listesi katmanı" (önceki okuma, B).
- "Manuel analiz, iş prosedürü gibi hazırlanmış bir şablonu izliyor"; şablonu "koşul–sonuç kuralları ve her sonucun açıklamasıyla koda aktardığını" söylüyor (not-backtest). Yorum: aynı kural hem insan hem kod tarafından okunsun istiyor; şablon paylaşılmadı.

**Reddettiği/eleştirdiği**
- "Bütün göstergelerin aynı anda yeşil olması zorunluluğunu veriyle sorgula" (not-backtest). Yüksek korelasyonu durağan spread saymıyor (yukarı). Başka açık eleştiri bu parçada yok.

**Tekrar eden ilkeler**
1. Yapı/bölge önce, gösterge teyit (XU100, not-backtest, AKFIS).
2. Kurulum = olası bölge + tepki bekleme; kesinlik yok (retest, Three Drives, AEFES "ALT BANT TEMAS + TEPKİ").
3. Her kurulumda geçersizlik seviyesi (CWENE 33,10; DOAS 146,00; STOP çizgisi).
4. Zaman dilimi ayrımı: günlük yapı + 4 saatlik teyit (XU100, not-backtest).
5. Sonucu ölç, katkısız filtreyi at (not-backtest) ve kendi sonucunu benchmark ile kıyasla (VAKBN-GARAN).
6. Sadelik: "sade bir strateji" (80-100 hafta), "Girişi sadeleştir".
