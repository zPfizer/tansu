# Parça 02: tweet-*, alfabetik son kısım (tweet-iskpl-… → tweet-yuksek-ihtimalli-…)

Kapsam notu: Talimat 45 dosya dedi. `tweet-iskpl-…` dosyasından alfabetik sona kadar 46 dosya var; 46'sı da okundu.
Açılan görsel: 4 (ISKPL backtest, ML hit-rate, talep bölgesi grafiği, otomotiv PD/DD tablosu). Başka not görsele atıf yapmıyor.

## Okuma kuralları (bu parça için)

- Bu 46 notun yalnız 3'ünde X bağlantısı var: `medyan-temelli` , `sektor-rotasyonundan`, `ttrak`. Yazar @The_Tansu_. Geri kalan her not "Levent aktardı" biçiminde Cevo parafrazıdır. Bunlar **ikinci el**. Notlardaki "Levent" Tansu olmayabilir (B-dosyası 3. madde ile uyumlu).
- Birinci el olan tek şey görsellerdir (Tansu'nun aracının konsol çıktısı): ISKPL, ML hit-rate, PD/DD tablosu. Talep bölgesi grafiği de görsel, ama kimin aracı belli değil.
- Notların "Teknik Ek", formül, durum makinesi, test, backtest-kolu bölümleri **Cevo'nun** işidir. Kaynak sayılmaz. Aşağıda "Cevo" diye ayrıldı.
- Alıntılar notun kaynak bölümünden alındı. "(not aktarımı)" etiketi, Tansu'nun birebir cümlesi olmadığını gösterir.

## 1. Dosya tablosu

Tür: strateji / çıkış-risk / filtre / tarama / yapı taşı / strateji değil.

| # | Dosya (tweet-…) | Tür | Tek satır |
|---|---|---|---|
| 1 | iskpl-abcd-cden-dye-backtest | strateji | AB=CD'de C'den al, D'de sat; ISKPL 5/5 hedef, +%610 (görsel birinci el) |
| 2 | istatistiksel-arbitraj-150bin-esbutunlesme-taramasi | tarama | Eşbütünleşme taraması ~150 bin çifte çıkabilir (ölçek uyarısı); gerisi Cevo |
| 3 | kagit-kalem-matematik-once-kod-sonra | strateji değil | Önce kâğıtta çöz, sonra kodla (süreç disiplini) |
| 4 | kendini-yenileyen-algoritma-ana-frekans | strateji değil | "Ana frekans" felsefesi, kural yok |
| 5 | kitap-model-sentezi-backtest-forward-test-kod-mimarisi | strateji değil | Model sentezi ve test süreci |
| 6 | likit-hisseler-etf-islem-derinligi-slippage-kapasite | filtre | Sığ hisse yerine ETF/likit hisse; eşik yok |
| 7 | medyan-temelli-finansal-indikatorler | yapı taşı | "Medyan temelli çalışın"; gösterge/formül yok (X bağlantılı) |
| 8 | ml-trade-13-gun-9-isabet | strateji değil | ML modeli 13 günde 9 isabet (%69,23); model yok, görsel birinci el |
| 9 | momentum-degerden-once-doner-egim-erken-uyari | strateji | Eğim dönüşü erken uyarı, Golden Cross geç teyit; formül yok |
| 10 | momentum-faaliyet-nakit-akisi-5x5-portfoy | tarama | Momentum x faaliyet nakit akışı bağımsız quintile; Mom5∩CFO5 |
| 11 | optimal-momentum-plus-simulasyon-tamamlandi | strateji değil | "Kod bitti, simülasyon sürüyor"; içerik yok |
| 12 | ozkaynak-artisi-varlik-finansman-yatirim-verimliligi | strateji değil | Özkaynak artışı analiz kontrol listesi (değerleme) |
| 13 | pddd-roe-sektor-tarihsel-value-trap-filtresi | tarama | Düşük PD/DD + yüksek ROE + sektör altı; 36 çeyrek bant |
| 14 | pine-script-python-gorev-ayrimi-veri-backtest-icra | strateji değil | Pine/Python araç tercihi |
| 15 | piyasa-denge-dengesizlik-auction-acceptance-state-machine | strateji | Denge: VAH/VAL'den POC'ye dönüş; dengesizlik: pullback ile trend |
| 16 | piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi | strateji değil | "Kesin" dilinden kaçın |
| 17 | poc-vah-val-vwap-auction-state-machine | strateji | VWAP+POC üstü al, altı sat/kaçın, arası bekle; VAH kırılımı; VAL re-entry |
| 18 | portfoy-optimizasyonu-volatilite-trading-risk-butcesi | strateji değil | "Huzurlu gece" ilkesi, formül yok |
| 19 | probabilistik-edge-fat-tail-risk-of-ruin | strateji değil | Olasılık/beklenen değer/ruin yöntem tavsiyesi |
| 20 | python-finans-fikir-dogrulama-ve-yanlislama | strateji değil | Python ile test disiplini |
| 21 | python-finans-verisi-ogrenme-yol-haritasi | strateji değil | Öğrenme rehberi |
| 22 | regresyon-ml-rasyolardan-piyasa-degeri-sapmasi | tarama | Rasyodan "olması gereken piyasa değeri", sapma; model yok |
| 23 | relatif-degerleme-piyasa-norm-bantlari | tarama | Norm bandının üstü/altı ucuz/pahalı, çoklu çarpanla teyit; eksenler yok |
| 24 | roc-nopat-yatirilan-sermaye-hesabi | strateji değil | ROC formülü (değerleme hesabı) |
| 25 | rolling-alpha-skewness-momentum-liste-katmani | tarama | Momentum listesine rolling alpha ve skewness; tanım yok |
| 26 | rolling-cointegration-iliski-bozulma-kapisi | filtre | Çift ilişkisi bozulunca yeni pozisyon kapat; rolling izle |
| 27 | satilik-degil-momentum-teknik-markowitz-max-sharpe-pipeline | tarama | ANN momentum → çift pozitif eğim → ADX/CMF/mum → Markowitz → Max Sharpe; gizli |
| 28 | sektor-rotasyonundan-hisse-secimine | tarama | Sektör rotasyonu → lider sektör → DuPont → ucuz hisse → mevsimsellik (X bağlantılı) |
| 29 | sirket-degerlendirme-sektor-isletme-finansal-degerleme-kontrol-listesi | strateji değil | Şirket kontrol listesi |
| 30 | spicy-scipy-deterministik-markowitz-optimizasyonu | strateji değil | Markowitz'i Monte Carlo yerine optimizerla çöz |
| 31 | stat-arb-momentum-donus-teyidi-kar-carpani | strateji | Stat-arb'da momentum dönüş teyidi kârı çarpar iddiası; sayı yok |
| 32 | talep-bolgesi-volume-profile-momentum-confluence | strateji değil | Tek grafik örneği; kural ve sonuç yok |
| 33 | teknik-indikator-islem-sistemi-degerlendirme-kriterleri | strateji değil | Win rate yetmez, beklenti/drawdown bak |
| 34 | topsis-cok-kriterli-hisse-siralama-motoru | tarama | TOPSIS ile sıralama; "klasik indikatör yerine"; kriter yok |
| 35 | topsis-hisse-secimi-yaklasan-proje | tarama | Aynı fikir: F/K, PD/DD, ROE, borç, RSI kriter örnekleri |
| 36 | trend-cizgisi-swing-pivot-regresyon-zarf | yapı taşı | İki pivottan çizgi; arada mum çizgiyi delmemeli; regresyon+zarf ikincil |
| 37 | trend-rejim-degisimi-korelasyon-hmm-gereksiz | filtre | Rejimde rolling korelasyon yeter, HMM gereksiz; seri/eşik yok |
| 38 | ttrak-pddd-primi-carpan-sikismasi | strateji değil | TTRAK PD/DD 9,46 → 2,06 sıkışması; sektör tablosu (X bağlantılı) |
| 39 | tweezer-bottom-talep-bolgesi-backtest | strateji | Tweezer Bottom'u kodla, talep bölgesinde tara, getirisini ölç; sayı yok |
| 40 | uygulama-algoritmalari-v1 | strateji değil | Uygulamanın ilk tarama listesi (kataloğa işaretçi) |
| 41 | varyans-risk-primi-model-free-kesisim | tarama | VRP (IV−RV) ve model-free varyans kesişimi; opsiyon verisi |
| 42 | volatilite-harvesti-sabit-agirlik-rebalancing | strateji | İki varlığı sabit oranda yeniden dengele |
| 43 | volatilite-piyasa-soku-yeni-alim-freni | filtre | Kısa/aylık oynaklık oranı sıçrarsa yeni alım yok |
| 44 | volatilite-ters-orantili-position-sizing-sermaye-koruma | çıkış (risk) | Yüksek volatilitede pozisyon küçülür; formül yok |
| 45 | williams-r-sma-swing-strateji-backtest | strateji | 30 dk Williams %R(14) + SMA14 pullback; atıf doğrulanamaz |
| 46 | yuksek-ihtimalli-gunluk-islem-bes-kapi | strateji | Beş kapı kontrol listesi: volatilite, confluence, momentum, trend, R/R 1:2–1:3 |

## 2. Aday modül kartları

Etiketler: **Hazırlık** H = kural birinci elden belli. K = çekirdek belli, yorum gerekir. X = formül yok.
Hiçbir kartta Tansu'nun metninde stop veya sistematik sınama yoktur, aksi belirtilmedikçe.

---

### M1. AB=CD, C'den al, D'de sat (ISKPL)
- **Tür:** strateji (giriş+çıkış, hedef D).
- **Kaynak:** `tweet-iskpl-abcd-cden-dye-backtest.md`; görsel `assets/tweet-iskpl-abcd-cden-dye-backtest/01-iskpl-abcd-cden-dye-backtest.png`. X bağlantısı yok. Metin ikinci el; **görsel birinci el** (Tansu'nun aracının konsol çıktısı).
- **Tansu'nun ifadesi (not aktarımı):** "1000 günlük taramada C noktasından alım ve D hedefinde satış."
- **Kurallar:** giriş = C noktası (C doğrulandıktan sonra); çıkış = hesaplanan D hedefi; stop: yok (görselde "Stop'a takılan / bozulan: 0"; kuralı yazılı değil); parametre: oran/tolerans/pivot ayarı yok; zaman dilimi: günlük (not başlığında "günlük", görselde yok); "1000 günlük" birimi belirsiz (not da böyle diyor). Yön: C'den alım ve pozitif getiri, yani yükselen D (görselden çıkarım; nottan çıkarım).
- **Gösterilen sonuç (görsel okundu):** hisse ISKPL; "Toplam patern sayısı: 5; Hedefe ulaşan: 5; Stop'a takılan/bozulan: 0; Henüz sonuçlanmamış (açık): 0". 5 işlem (C tarihi → getiri → sermaye): 2024-04-03 → %46,98 → 146.981,63; 2024-08-13 → %56,67 → 230.271,26; **2025-03-21** → %49,90 → 345.176,62; 2025-06-19 → %45,37 → 501.774,42; 2026-01-21 → %41,50 → 710.006,23 TL. Başlangıç 100.000,00; bitiş 710.006,23; toplam %610,01. Tüm işlem getirisi bileşik, sıralı.
- **Veri:** günlük OHLCV yeterli (pivot+oran). Hacim gerekmiyor.
- **Belirsizlik (bizim yorumumuz):** pivot (A, B, C, D) bulma ayarı, BC/AB oran toleransı, "C doğrulandı" anı (look-ahead riski), stop, 1000 günün birimi, neden ISKPL, işlem başına giriş fiyatı (C fiyatı mı sonraki bar mı), masraf yok.
- **Uygulanabilirlik: K.** Hedef kuralı (D) ve sonuç rakamları var; dedektör Tansu'dan gelmiyor. Oranlar C-dosyasındaki SMRTG/diğer notlardan (parça 01/04–06 ve C-dosyası).
- **ÇELİŞKİ:** Not tablosu 3. işlem tarihini `2025-02-21` yazıyor; **görsel `2025-03-21`**. Görsel geçerli (C-dosyası da bunu yakalamıştı, doğrulandı).

---

### M2. Williams %R(14) + SMA14 pullback (30 dk)
- **Tür:** strateji (giriş+stop+hedef). **Atıf doğrulanamaz.**
- **Kaynak:** `tweet-williams-r-sma-swing-strateji-backtest.md`. Görsel yok. X bağlantısı yok. Not türü `user-provided-strategy-spec`; yazan "Levent'in kuralları". İkinci el, Tansu'ya aidiyeti belirsiz.
- **Tansu'nun ifadesi:** yok (notta birebir cümle yok; "Kullanıcı kuralları" bölümü).
- **Kurallar (notun "kullanıcı kuralları"):** zaman dilimi 30 dk; Williams %R periyot 14; SMA 14; aşırı alım [-20, 0]; aşırı satım [-100, -80]; pivot -50; hedef >= 2R. Uzun: fiyat SMA14 üstünde; %R önce -20 üstüne girmiş; -50'ye geri çekilmiş; -50 üstüne dönmüş; dönüş mumu boğa; sonraki fiyat sinyal mumunun high'ını aşınca giriş; stop "en yakın swing low". Kısa: simetrik (-80, -50 altına dönüş, ayı mumu, low kırılımı, swing high stop).
- **Sonuç:** Tansu göstermedi. Notta verilen backtest (45 işlem, PF 0,988 uzun-only vb.) **Cevo/Claude çıktısıdır**, Tansu'nun değil. Bu rakamlar hedef sadakat değil.
- **Veri:** 30 dakikalık gün içi OHLC gerekir. Günlük yetmez.
- **Belirsizlik:** "en yakın swing" tanımı (Cevo 5 bar baz önerdi), emir süresi (Cevo: 3 bar), arm süresi (Cevo: 40 bar), maliyet (Cevo: 5+10 bp). Bunlar Cevo parametresi.
- **Uygulanabilirlik: K** (kural sayıları belli, atıf ve stop tanımı belirsiz, veri gün içi). Günlük veri hedefiyle H/K değil: **bedava günlük veriyle uygulanamaz**.
- **B-dosyası (30) ile uyumlu:** "Tansu'ya atfı doğrulanamadı, HAYIR (30 dk veri)".

---

### M3. POC/VAH/VAL + VWAP auction sistemi
- **Tür:** strateji (yön izni + iki setup). **Önceki okumada yok** (A–E'de geçmiyor).
- **Kaynak:** `tweet-poc-vah-val-vwap-auction-state-machine.md`. Görsel yok. X bağlantısı yok. İkinci el (not türü `user-provided-strategy-text`).
- **Tansu'nun ifadesi (not aktarımı):** "Fiyat VWAP ve POC altındaysa satış, üstündeyse alış yönüne bakmayı; arasındaysa işlem yapmamayı." VAH+VWAP üstü kalıcılık = breakout yolculuğu; VAL altı sarkma sonrası re-entry = POC hedefli mean-reversion. POC "mıknatıs", VAH/VAL pahalı/ucuz sınır, VWAP kurumsal ortalama (Cevo bu yorumları reddediyor).
- **Kurallar:** (1) yön izni: close > VWAP ve > POC → alış; altında ikisinin → sat/kaçın; arada → bekle. (2) VAH + VWAP üstünde kalıcı → uzun yolculuk. (3) fiyat VAL altına sarkıp value içine dönerse (VWAP yukarıda) → hedef POC. (4) bearish retest/rejection: VWAP/POC altında, referansa rallide red → short. Stop: yok. Parametre: **hiçbiri verilmedi** (profile penceresi, bin genişliği, value-area %, VWAP reset, kalıcılık K/M, tampon). Fixed Range veya Session Volume Profile; "günlük VWAP"; Python taraması.
- **Sonuç:** yok.
- **Veri:** **günlük OHLCV yetmez.** Gerçek POC/VAH/VAL için işlem-fiyat dağılımı (tick/gün içi bar) gerekir. Gerçek seans VWAP'ı gün içi ister. Günlük yaklaşım (typical price × hacim) yaklaşıktır ve etiketlenmeli.
- **Belirsizlik:** profile türü (önceki seans / gelişen / sabit aralık), VA %, tamponlar, kalıcılık, stop, hedef çıkışı. Cevo'nun durum makinesi bizim değil.
- **Uygulanabilirlik: K** (çekirdek yön kuralı belli; sayı ve stop yok; gün içi veri gerekir). Bedava günlük veriyle yaklaşık sürüm: "K, düşük".

---

### M4. Denge / dengesizlik (Balance/Imbalance) value area stratejisi
- **Tür:** strateji (rejim sınıflaması + iki setup). **Önceki okumada yok.**
- **Kaynak:** `tweet-piyasa-denge-dengesizlik-auction-acceptance-state-machine.md`. Görsel yok. X yok. İkinci el (`user-provided-strategy-text`).
- **Tansu'nun ifadesi (not aktarımı):** denge = value area içinde iki yönlü yatay auction; dengesizlik = value'yu terk edip yeni value arayan yönlü auction. Denge rejiminde VAH/VAL'den POC'ye mean reversion; dengesizlikte pullback ile trend takibi. Açılış önceki value area içindeyse denge, dışındaysa trend potansiyeli. Value Area %68 (standart sapma/normal dağılımla ilişkilendirmiş); "2SD/3SD alanlarında mean-reversion olasılığı artar".
- **Kurallar:** (denge) VAL/VAH testi + value'ya dönüş → POC hedefi (ping-pong). (dengesizlik) kabul görülen dışarıda kapanış + pullback → devam. Stop yok. Parametre: Value Area %68 (tek sayı). 2SD/3SD kullanım kuralı yok. Acceptance/rejection tanımı (K/M, süre) Cevo önerisi.
- **Sonuç:** yok.
- **Veri:** önceki seans value area için gün içi/tick hacmi gerekir; açılış konumu günlük açılışla yapılır ama value area günlük OHLCV'den gerçek çıkmaz.
- **Belirsizlik:** profile kimliği (TPO/hacim), VA algoritması, acceptance, SD kimliği, tüm giriş tetikleri.
- **Uygulanabilirlik: X** (rejim fikri var, hiçbir tetik/stop/eşik yok; Cevo'nun "VA ≠ Gaussian 1σ" düzeltmesi bizim değil).
- **Not:** M3 ile aynı yapı taşları (POC/VAH/VAL). Tek aile olarak birleştirilebilir.

---

### M5. Yüksek ihtimalli günlük işlem, beş kapı
- **Tür:** strateji çerçevesi / filtre listesi.
- **Kaynak:** `tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** beş unsur: aktif volatilite, sinyal uyumu (iki veya daha fazla teknik gösterge), pozitif momentum, ana trend yönü, uygun risk/ödül. "Yükselen trendde yalnız alım, düşen trendde yalnız satış." R/R 1:2 veya 1:3; "stop loss her zaman bu orana göre belirlenir."
- **Kurallar:** giriş tetiği yok; stop = R/R'ye göre; hedef R/R 1:2 veya 1:3; parametre: yalnız bu iki oran. Gösterge, volatilite ölçüsü, momentum formülü, zaman dilimi yok.
- **Sonuç:** yok.
- **Veri:** günlük yeterli olurdu ama kural eksik; "günlük işlem" = gün içi olabilir.
- **Belirsizlik:** hepsi. Cevo "stop geçersizlikten gelir, R/R'den değil" diye düzeltiyor; bu Tansu'nun cümlesiyle çelişir (Tansu: stop R/R'ye göre).
- **Uygulanabilirlik: X** (formül yok).

---

### M6. Stat-arb momentum dönüş teyidi
- **Tür:** giriş filtresi (çift rotasyonuna ek).
- **Kaynak:** `tweet-stat-arb-momentum-donus-teyidi-kar-carpani.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** stat-arb sisteminde momentum dönüş teyidi uygulanması kârlarda "çarpan etkisi" yaratıyor; deneyleri sonra anlatacak; "momentum trader sisteme farklı bakar."
- **Kurallar:** yok (momentum formülü, eşik, backtest yok). Cevo'nun `z>=üst ve ΔZ<0` tanımı bizim; D-dosyasındaki ΔZ=Z_t−Z_{t−1} **görselden** doğrulanmış (bu notta değil).
- **Sonuç:** yok ("çarpan" sayısı yok).
- **Veri:** günlük OHLCV yeterli.
- **Uygulanabilirlik: X** (bu not için). Çift rotasyonu kartı (D) zaten ΔZ onayını içeriyor; bu not ona yeni bir şey eklemiyor.

---

### M7. Rolling cointegration ilişki bozulma kapısı
- **Tür:** filtre / çıkış.
- **Kaynak:** `tweet-rolling-cointegration-iliski-bozulma-kapisi.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** tek seferlik cointegration testi zamanla bozulan ilişkiyi kaçırabilir; rolling izlenmeli.
- **Kurallar:** yok (test yöntemi, pencere, eşik yok). Durum makinesi (CANDIDATE…RETIRED) ve K/M/D Cevo.
- **Sonuç:** yok.
- **Veri:** günlük yeterli.
- **Uygulanabilirlik: X.** Not: D-dosyası görselden "Cointegration p 0,048 — CURRENT" gördü (bu notta yok).

---

### M8. İstatistiksel arbitraj, 150 bin eşbütünleşme taraması
- **Tür:** tarama (çift keşfi). Büyük kısmı Cevo (FDR, batch mimarisi).
- **Kaynak:** `tweet-istatistiksel-arbitraj-150bin-esbutunlesme-taramasi.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** "eşbütünleşme testi iyi ihtimal ile 150.000 kombinasyon taramasına kadar çıkabilir; bilmeniz önemli."
- **Kurallar:** yok. Tek sayı: 150.000 (~549 varlık, 549x548/2=150.426; Cevo hesabı).
- **Sonuç:** yok. **Veri:** günlük yeterli. **Uygulanabilirlik: X** (ölçek uyarısı; test, pencere, eşik yok).

---

### M9. Momentum: eğim dönüşü erken uyarı
- **Tür:** giriş sinyali (erken uyarı); kesişim teyit.
- **Kaynak:** `tweet-momentum-degerden-once-doner-egim-erken-uyari.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** ortalama kullananlar eğimlere, momentum trader'lar sinyal eğimine bakar; momentum/hız değerden önce döner; eğim yön değişimi erken uyarı, Golden Cross geç teyit; "kesişim oluşana kadar fiyat çoğu kez %5–10 prim yapar."
- **Kurallar:** giriş: eğim negatiften pozitife dönünce (yön); teyit: Golden Cross. Stop/hedef/parametre: **yok** (ortalama türü, pencere, momentum formülü yok). Tek sayı: %5–10 (iddia, doğrulanmamış).
- **Sonuç:** yok. **Veri:** günlük yeterli.
- **Belirsizlik:** eğim tanımı (Cevo: MA_t − MA_{t−K}), pencere, persistence tamponu: hepsi bizim.
- **Uygulanabilirlik: X.** (B-dosyası #17 ile uyumlu.)

---

### M10. Momentum x faaliyet nakit akışı 5x5 portföy
- **Tür:** tarama / sıralama (portföy seçimi).
- **Kaynak:** `tweet-momentum-faaliyet-nakit-akisi-5x5-portfoy.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** her çeyrek evreni momentum ve faaliyet nakit akışına göre **bağımsız** sırala; her biri 5 eşit dilim; kesişim 25 portföy; odak `Mom5 × CFO5`.
- **Kurallar:** her çeyrek; 5 quintile (%20); hedef = Mom5 ∩ CFO5. Momentum formülü, ağırlık, çıkış, stop: yok. (Tweet: "daha önce anlatılan momentum stratejisi"; formül bu iletide yok.)
- **Sonuç:** yok.
- **Veri:** günlük fiyat + **bilanço (faaliyet nakit akışı, açıklanma tarihiyle)**. Günlük OHLCV yetmez.
- **Belirsizlik:** momentum lookback ve son ayı atlama, CFO ham/normalize (not ham seviye diyor), ağırlık, yeniden dengeleme (çeyrek sonu).
- **Uygulanabilirlik: K** (yapı kesin, momentum formülü ve CFO verisi eksik; CFO bedava veride zor).

---

### M11. PD/DD + ROE + sektör + 36 çeyrek (değer tuzağı filtresi)
- **Tür:** tarama (değerleme filtresi), strateji değil sayılabilir; aday olarak tutuldu.
- **Kaynak:** `tweet-pddd-roe-sektor-tarihsel-value-trap-filtresi.md`. Görsel yok. X yok. İkinci el. Tansu'nun "Python örneği" kodu notta **yok** (not: `source_python_code = MISSING`).
- **Tansu'nun ifadesi (not aktarımı):** PD/DD tek başına değil; sektör ortalaması, şirketin 36 çeyreklik tarihsel PD/DD bandı ve ROE ile birlikte. "Düşük PD/DD + yüksek ROE + sektör altı çarpan → potansiyel yıldız." Düşük PD/DD value trap olabilir. Örnek: sektör 2,5, şirket 1,0 → ucuz adayı.
- **Kurallar:** üç koşul (düşük, yüksek, altı); eşik yok. Tek sayı: 36 çeyrek. Giriş/stop/hedef yok.
- **Sonuç:** yok. **Veri:** fiyat + bilanço çeyreklik (özkaynak, net kâr). Günlük OHLCV yetmez.
- **Belirsizlik:** "düşük/yüksek" eşikleri, sektör ortalaması mı medyanı mı (Cevo medyan öneriyor), ROE normalizasyonu.
- **Uygulanabilirlik: K** (üç kapı belli; eşik yok; bilanço verisi gerekir).

---

### M12. Volatilite harvesti: sabit ağırlık yeniden dengeleme
- **Tür:** strateji (portföy, giriş/çıkış = yeniden dengeleme).
- **Kaynak:** `tweet-volatilite-harvesti-sabit-agirlik-rebalancing.md`. Görsel yok (not gp-37'ye atıf yapıyor, o parça 04–06'da). X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** ters korelasyonlu iki varlığı belirli oranlarda aktif yeniden dengelemek, piyasa çalkantısını getiri motoruna çevirir; matematiksel olarak kanıtlanacak, getiri kanıtı sonra paylaşılacak.
- **Kurallar:** hedef ağırlık w ve 1−w; sapınca hedefe dön. Varlık, w, sıklık, bant: **yok**. Cevo'nun γ* formülü bizim (standart constant-mix).
- **Sonuç (bu notta):** yok. (gp-37: GARAN%50/KGYO%40/CCOLA%10, aktif −1.040,58 TL pasifin altında; D-dosyası zaten yazdı.)
- **Veri:** günlük kapanış yeterli.
- **Uygulanabilirlik: K.** Kural basit; parametre yok; D-dosyasıyla uyumlu.

---

### M13. Volatilite şok freni (yeni alım yok)
- **Tür:** piyasa filtresi / risk yetkisi.
- **Kaynak:** `tweet-volatilite-piyasa-soku-yeni-alim-freni.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** sabit pencereli ortalamalar panikte geç kalır; son X günlük oynaklığı son bir aylık oynaklıkla karşılaştır; kısa vadeli oynaklık aniden yükselirse "Piyasa Şoku" modu. Şokta: yeni alım sinyalleri tamamen durur, yeni hisse eklenmez, yalnız mevcut portföyün riski yönetilir, mevcut hisseler kendi içinde yeniden dengelenir.
- **Kurallar:** karşılaştırma + eşik üstü → yeni giriş yok. X, eşik, çıkış süresi: **yok**. "Bir ay" ~21 işlem günü bizim yorum.
- **Sonuç:** yok. **Veri:** günlük yeterli.
- **Uygulanabilirlik: K, düşük** (eylem kuralı net; iki sayı eksik). Önceki okuma (KURALLAR.md) **X** dedi. Fark: eylem kuralı net olduğu için K diyorum; X de savunulabilir, çünkü eşik hiç yok.

---

### M14. Volatiliteyle ters orantılı position sizing
- **Tür:** çıkış/risk kuralı (boyutlandırma).
- **Kaynak:** `tweet-volatilite-ters-orantili-position-sizing-sermaye-koruma.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** volatilitesi yüksek hisselerde position sizing'in matematiksel olarak küçülmesi doğru risk yönetimidir; ana amaç sermayeyi korumak; "uygun zamanda oyuna zaten girilir."
- **Kurallar:** ilke tek cümle. Ölçü, pencere, risk % yok. Cevo örneği (equity 100.000, %1, k=2xATR) **Cevo'nun**, Tansu'nun değil.
- **Sonuç:** yok. **Veri:** günlük yeterli.
- **Uygulanabilirlik: X** (E-dosyası K6 ile uyumlu; ATR tabanlı %1/2xATR kural E'deki NotebookLM kaynağından).

---

### M15. Likit hisse/ETF öncelikli kapasite kapısı
- **Tür:** filtre (evren).
- **Kaynak:** `tweet-likit-hisseler-etf-islem-derinligi-slippage-kapasite.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** trade'i ciddiye alan yeni yatırımcılar derinliği olmayan alanlar ve sığ hisseler yerine ETF'lere ve likit hisselere odaklansın; gerekçe: istenen zamanda ve makul fiyatta girip çıkabilmek.
- **Kurallar:** yok (likit tanımı, eşik yok). Cevo'nun katılım oranı, spread, derinlik formülleri bizim.
- **Sonuç:** yok. **Veri:** işlem değeri (ADV) günlük OHLCV'den çıkar; derinlik/spread çıkmaz.
- **Uygulanabilirlik: X** (eşik yok; E-dosyası ile uyumlu).

---

### M16. Trend çizgisi motoru: swing pivot eşleştirme (yapı taşı)
- **Tür:** yapı taşı (trend çizgisi); regresyon+zarf ikincil.
- **Kaynak:** `tweet-trend-cizgisi-swing-pivot-regresyon-zarf.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** Swing Pivot Eşleştirmesi ana yöntem (insanın çizdiği destek/direnci doğrudan kodlar, kontrol geliştiricide); Regresyon ve Zarf seçilmiş aralığa istatistiksel doğru uydurur, hazır kütüphanelerde müdahale zor.
- **Kurallar (Tansu'dan çıkan):** iki pivot (destek için iki dip, direnç için iki tepe) çizgi çizer; arada mumların çizgiyi delmemesi ("en katı invariant", notta kaynağa atfedilmiş). L/R pivot penceresi, tolerans, kırılım tamponu: **Cevo**. Giriş/stop yok.
- **Sonuç:** yok. **Veri:** günlük yeterli.
- **Uygulanabilirlik: K** (yöntem adı ve invariant belli; pivot ayarı yok). A-dosyası (satır 273) ile uyumlu.

---

### M17. Trend rejimi: rolling korelasyon (HMM gereksiz)
- **Tür:** piyasa filtresi (rejim).
- **Kaynak:** `tweet-trend-rejim-degisimi-korelasyon-hmm-gereksiz.md`. Görsel yok. X yok. İkinci el; notun kendisi "kaynak kimliği doğrulanmamış, Levent'e atfedilemez" diyor.
- **Tansu'nun ifadesi (not aktarımı):** trend rejim değişiminde güçlü korelasyon varken Hidden Markov Model'e gerek olmayabilir.
- **Kurallar:** yok (hangi seri çifti, pencere, eşik yok). Durum makinesi ve Fisher CI Cevo.
- **Uygulanabilirlik: X.**

---

### M18. Tweezer Bottom + talep bölgesi
- **Tür:** giriş (mum formasyonu + bölge).
- **Kaynak:** `tweet-tweezer-bottom-talep-bolgesi-backtest.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** Tweezer Bottom mum yapısını kodla, tara, getirisini ölç; "talep bölgesinde güçlü fırsatlar sunar."
- **Kurallar:** yok (iki ardışık mumun dipleri yakın; tolerans Cevo). Giriş/stop/hedef/zaman dilimi yok.
- **Sonuç:** yok. **Veri:** günlük yeterli (talep bölgesi tanımı hariç).
- **Uygulanabilirlik: X.** (B-dosyası #11 ile uyumlu.)

---

### M19. Rolling alpha + rolling skewness momentum listesi
- **Tür:** tarama (liste katmanı).
- **Kaynak:** `tweet-rolling-alpha-skewness-momentum-liste-katmani.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** Rolling Alpha ve Rolling Skewness'ın anlaşılmasını istedi; ikisi momentum listelerine uygulandı; ayrıntıyı sonra anlatacak.
- **Kurallar:** yok. **Sonuç:** yok.
- **Uygulanabilirlik: X** (bu not). B-dosyası #18'e göre 63 günlük skewness ve sınıf sınırları başka bir X kaynağında (parça 03).

---

### M20. Satışa kapalı pipeline: ANN momentum → eğim → ADX/CMF/mum → Markowitz → Max Sharpe
- **Tür:** tarama + portföy (gizli).
- **Kaynak:** `tweet-satilik-degil-momentum-teknik-markowitz-max-sharpe-pipeline.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** "Sistem satılık değildir"; beş aşama: ANN momentum, pozitif fiyat/sinyal eğimi, ADX+CMF+bullish mum, Markowitz, Max Sharpe.
- **Kurallar:** tek net kural: `fiyat eğimi > 0 VE sinyal eğimi > 0`. ANN, eşikler, ADX/CMF değerleri, çekiç/sabah yıldızı tanımı, optimizer kısıtları **gizli, açıklanmadı**.
- **Sonuç:** yok. **Uygulanabilirlik: X.**

---

### M21. TOPSIS ile hisse sıralama
- **Tür:** tarama / sıralama.
- **Kaynak:** `tweet-topsis-cok-kriterli-hisse-siralama-motoru.md`, `tweet-topsis-hisse-secimi-yaklasan-proje.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** TOPSIS deneysel sonuçları "çok güçlü"; klasik indikatörler yerine kullan. Kriter örnekleri: F/K, PD/DD, ROE, borçluluk, RSI. Yakında projeye başlayacak.
- **Kurallar:** yok (kriter, ağırlık, yön, evren yok). TOPSIS'in matematiği standart; "7/7 test" Cevo kodu.
- **Sonuç:** yok. **Veri:** temel kriterler için bilanço.
- **Uygulanabilirlik: X** (Tansu'nun sıralaması yeniden üretilemez; motor standarttır, kriterleri biz seçeriz, bu tamamen yorum).

---

### M22. Relatif değerleme norm bantları, çoklu çarpan teyidi
- **Tür:** tarama (değerleme).
- **Kaynak:** `tweet-relatif-degerleme-piyasa-norm-bantlari.md`. Görsel yok. X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** piyasanın kabul ettiği alt/üst norm bandı dışındaki şirketler relatif ucuz/pahalı; "üst ucuz, alt pahalı"; farklı rasyo/çarpanla teyit.
- **Kurallar:** yok (eksenler, bant yöntemi, ilk rasyo yok). **Uygulanabilirlik: X.** (Regresyon/ML sapma notu da aynı: `tweet-regresyon-ml-rasyolardan-piyasa-degeri-sapmasi.md`, X.)

---

### M23. Sektör rotasyonundan hisse seçimine (huni)
- **Tür:** tarama (üst seviye zincir).
- **Kaynak:** `tweet-sektor-rotasyonundan-hisse-secimine.md`; X: https://x.com/The_Tansu_/status/2092997001025622031 (27.08.2026 18:25). **Birinci el metin** (X'te doğrulandı).
- **Tansu'nun ifadesi (not kısa alıntısı):** "Sektör rotasyonu… lider sektörde Dupont analizi, ucuz kalmış hisseler… mevsimsel satışları."
- **Kurallar:** sıra: sektör rotasyonu + sektör korelasyonu → lider sektör → DuPont → ucuz hisse → satış mevsimselliği. Hiçbir ölçüt/eşik yok; "yapılacak, bitince paylaşılacak" (plan).
- **Sonuç:** yok. **Veri:** sektör getirisi (günlük) + bilanço (DuPont).
- **Uygulanabilirlik: X.** (Sektör 30/60/90 sıralaması gp-06'da, D-dosyasında H olarak var.)

---

### M24. Medyan temelli göstergeler (yapı taşı fikri)
- **Tür:** yapı taşı (yönlendirme).
- **Kaynak:** `tweet-medyan-temelli-finansal-indikatorler.md`; X: https://x.com/The_Tansu_/status/2093012975741276225 (27.08.2026 19:29). **Birinci el.**
- **Tansu'nun ifadesi:** "Ortalamaları temel alan indikatörler… Medyan temelli çalışın."
- **Kurallar:** yok. **Uygulanabilirlik: X.** (B-dosyası #28 ile aynı.)

---

### M25. Varyans risk primi ve model-free varyans kesişimi
- **Tür:** tarama (opsiyon tabanlı).
- **Kaynak:** `tweet-varyans-risk-primi-model-free-kesisim.md`. Görsel yok (gp-05 VRP scanner başka parçada). X yok. İkinci el.
- **Tansu'nun ifadesi (not aktarımı):** iki motor: VRP ("gerçek IV" kullanılacak) ve model-free varyans; biri sessiz fakat patlamaya yakın hisseleri bulur, diğeri IV'ye göre ± hareket oranını gösterir; kesişim = volatilite kaynaklı aday. Yüksek VRP → VOL SAT, negatif → VOL AL (notta dashboard ayrıntısı).
- **Kurallar:** eşik/formül yok. **Veri:** **opsiyon (IV, strike zinciri) gerekir**; günlük OHLCV yetmez. **Uygulanabilirlik: X.**

---

## 3. Strateji olmayan notlar (tek satır)

- `kagit-kalem-…`, `kitap-model-sentezi-…`, `python-finans-fikir-…`, `python-finans-verisi-…`, `pine-script-python-…`: araç/süreç disiplini.
- `kendini-yenileyen-…`, `probabilistik-edge-…`, `piyasa-dilinde-kesinlik-…`, `portfoy-optimizasyonu-volatilite-…`, `spicy-scipy-…`: felsefe ve yöntem tavsiyesi, kural yok.
- `ml-trade-13-gun-9-isabet`: ML modeli 14 sinyal gününde (1 AL, 13 SAT), sonucu bilinen 13'te 9 isabet, %69,23 (görsel okundu, not ile birebir). Model/etiket yok; strateji değil.
- `optimal-momentum-plus-simulasyon-tamamlandi`: "kod bitti, simülasyon sürüyor"; bileşenler bilinmiyor.
- `teknik-indikator-islem-sistemi-degerlendirme-kriterleri`: rapor ölçütü (beklenti, drawdown); sınama standardı olarak yararlı.
- `uygulama-algoritmalari-v1`: ürün kapsam listesi (arbitraj, volatilite harvesti, ABCD/kelebek/Gartley, alpha/momentum hisseleri, kanal dibi, düşeni kıran, takoz/TOBO/OBO/bayrak/flama). Kural yok.
- `ozkaynak-artisi-…`, `roc-nopat-…`, `sirket-degerlendirme-…`: temel analiz hesabı/kontrol listesi.
- `ttrak-pddd-primi-…`: değerleme gözlemi. Görsel (PD/DD tablosu) okundu. **Not hatası:** notun tablosu TOASO 2025/9 için `2,00` yazıyor; **görselde `2,30`**. Görseldeki sektör ort. 2,27 ancak 2,30 ile tutuyor. Görsel geçerli.
- `talep-bolgesi-volume-profile-momentum-confluence`: tek grafik (görsel açıldı): alt mavi talep kutusu, üstte turuncu arz, sağda yatay volume profile, altta hacim, MACD-benzeri ve RSI-benzeri paneller, sağ uçta yeşil mum yükselişi. Ticker/seviye/tarih **okunamadı**. Kural ve sonuç yok; "Ben geliyorum" iddiası seçilmiş örnektir.

## 4. Ortak yapı taşları (bu parçadan)

- **Pivot (swing high/low, L/R)**: M1 (AB=CD), M16 (trend çizgisi), M2 (swing stop), M18 (talep bölgesi için).
- **Trend çizgisi (iki pivot, delmeme invariantı)**: M16; ayrıca A-dosyası #3/#4.
- **Talep/arz bölgesi**: M18, görsel M talep-bölgesi notu; bölge üretimi hiçbir notta yok.
- **Hacim profili (POC/VAH/VAL) ve VWAP**: M3, M4; ayrıca `acsel-direnc-kirilimi…` (parça 01).
- **Z-skor spread ve ΔZ**: M6, M7, M8 (D-dosyasındaki çift rotasyonu).
- **Eğim (slope) ve kesişim**: M9, M20 (çift pozitif eğim).
- **Williams %R, SMA, ADX, CMF**: M2, M20.
- **Oynaklık oranı (kısa/uzun)**: M13; ATR ile pozisyon boyutu: M14.
- **Quintile sıralama**: M10; **TOPSIS**: M21; **rolling alpha/skewness**: M19.
- **Rolling korelasyon / rolling cointegration**: M17, M7.
- **Kullanılabilir ölçüm sözleşmesi (win rate yetmez, beklenti, MDD)**: `teknik-indikator-…` (rapor tasarımı için).

## 5. Aynı fikrin başka yerlerde geçtiği yerler

- **Çift rotasyonu / stat-arb:** M6, M7, M8 → D-dosyası (VAKBN–GARAN, CIMSA–OYAKC, AGROT–GARAN, gp-51/52/53/54).
- **AB=CD C→D:** M1 → SMRTG (gp-03, 12 işlem), MARKA (gp-01), C-dosyası §5; `tweet-abcd-*` (parça 01).
- **Volatilite şoku / pozisyon boyutu / likidite:** M13, M14, M15 → E-dosyası K6, K8, §233; gp-113 (BIST VIX), gp-62 (Corwin–Schultz).
- **Volatilite harvesti:** M12 → gp-37, gp-57 (D-dosyası).
- **Hacim profili/value area:** M3, M4 → `acsel-direnc-kirilimi-volume-profile-val`, `gunluk-trade-breakout-gap-retest…`, gp-66, gp-97, gp-100 (parça 01, 04–06).
- **Momentum eğim ve Williams:** M2, M9 → B-dosyası #17, #30; `hareketli-ortalama-ust-alt-trend-yon-filtresi`, `halftrend-buy…` (parça 01).
- **Rolling skewness (63 gün):** M19 → `kaynak-cwene-skewness-…` (parça 03).
- **Trend çizgisi:** M16 → A-dosyası, gp-64, gp-93, gp-103 (parça 04–06).
- **Sektör rotasyonu:** M23 → gp-06, gp-07 (D-dosyası).

## 6. Önceki okuma (KURALLAR.md ve A–E) ile çelişenler / olmayanlar

1. **Önceki okumada yok:** POC/VAH/VAL+VWAP (M3) ve denge/dengesizlik (M4) A–E'de geçmiyor. Yeni aday modül; ikisi de K/X, gün içi veri ister.
2. **ISKPL tarihi:** önceki okuma doğru yakaladı (görsel 2025-03-21, not 2025-02-21). Bu okumada görselle tekrar doğrulandı.
3. **Şok freni:** önceki okuma X, bu okuma K (düşük). Eylem kuralı net, eşikler yok.
4. **Beş kapı (M5):** Tansu'nun cümlesinde "stop R/R'ye göre"; Cevo notu bunu tersine çeviriyor (stop geçersizlikten). Kural olarak Tansu'nun ham cümlesi geçerli; Cevo düzeltmesi bizim kuralımız olamaz.
5. **PD/DD tablo hatası:** TOASO 2025/9 = 2,30 (görsel), 2,00 (not). Strateji dışı ama not güvenilirliği için işaretlendi.
6. **Williams %R:** önceki okuma ile uyumlu (atıf doğrulanamaz; veri 30 dk). Notun backtest rakamları Cevo çıktısıdır, hedef sadakat sayılmaz.

## Tansu'nun bakış açısı (ipuçları)

Uyarı: Birebir Tansu cümlesi yalnız `medyan-temelli` ve `sektor-rotasyonundan` notlarında var (X bağlantılı). Diğer alıntılar notların kaynak bölümündeki aktarımdır ("Levent … belirtti"). Cevo'nun teknik ek bölümlerinden alıntı yapılmadı. Yorum satırları bana aittir.

### Piyasaya bakış (trend, rejim, ortalamaya dönüş, kuyruk)
- "Sabit pencereli hareketli ortalamalar ani panik dönemlerinde rejim değişimini geç algılar." (aktarım; `volatilite-piyasa-soku-yeni-alim-freni`)
- "kısa vadeli oynaklık aniden yükselirse sistemi Piyasa Şoku moduna geçir" (aynı not). Amaç "erken dip yakalamak değil" (aynı not).
- "trend rejim değişiminde güçlü korelasyon varken Hidden Markov Model'e gerek olmayabilir" (aktarım; `trend-rejim-degisimi-korelasyon-hmm-gereksiz`).
- "Dengeyi value area içindeki iki yönlü yatay auction; dengesizliği … yeni value arayan directional auction" (aktarım; `piyasa-denge-dengesizlik-…`). Denge: "ping-pong", dengesizlik: "surf the wave" (kaynak metaforları, aynı not).
- "momentum/hız değerden önce döner; eğim yön değişimi erken uyarı, Golden Cross geç teyit" (aktarım; `momentum-degerden-once-doner-egim-…`).
- Fat tail, skewness, kurtosis ve black-swan dayanıklılığını vurguladı; normal dağılım yerine (aktarım; `probabilistik-edge-fat-tail-risk-of-ruin`).
- Piyasa, "karmaşa altında belirli frekanslar taşıyor" ve algoritma "ana frekansı" aramalı (aktarım; `kendini-yenileyen-algoritma-ana-frekans`).
- Yorum: Tansu piyasayı rejime bağlı görüyor (denge/trend, şok/normal). Her rejimde farklı davranış istiyor. Ortalamaya dönüş yalnız dengede, devam ise dengesizlikte.

### Kurulum seçimi (confluence, kanıt, arz-talep)
- "Yapı talep bölgesinde önceden güçlü biçimde görülebildi ve bunun hacim ayak izinden de anlaşılabildi" (aktarım; `talep-bolgesi-volume-profile-momentum-confluence`; görselde bölge + profile + hacim + iki momentum paneli var).
- "Formasyonun özellikle talep bölgesinde güçlü fırsatlar sunduğunu iddia ediyor" (aktarım; `tweezer-bottom-talep-bolgesi-backtest`).
- Beş unsur: "aktif volatilite, sinyal uyumu/confluence, pozitif momentum, ana trend yönü ve uygun risk/ödül"; "iki veya daha fazla teknik gösterge" (aktarım; `yuksek-ihtimalli-gunluk-islem-bes-kapi`).
- Hisse seçimi huni: "Sektör rotasyonu… lider sektörde Dupont analizi, ucuz kalmış hisseler… mevsimsel satışları." (birebir, X; `sektor-rotasyonundan-hisse-secimine`).
- "Düşük PD/DD + yüksek ROE + sektör altı çarpan → potansiyel yıldız"; düşük PD/DD "value trap" olabilir (aktarım; `pddd-roe-sektor-tarihsel-value-trap-filtresi`).
- Relatif değerleme: piyasanın kabul ettiği norm bandı dışı şirketler, sonuç "farklı rasyolar/çarpanlarla teyit" (aktarım; `relatif-degerleme-piyasa-norm-bantlari`).
- Yorum: Tansu tek sinyale değil çok katmanlı kanıta güveniyor (bölge + hacim + momentum). Bağımsızlık (aynı OHLC türevi çift oy) Cevo'nun düzeltmesidir, Tansu'nun cümlesi değil.

### Giriş teyidi
- Boğa için: "Fiyat VWAP ve POC … üstündeyse alış … arasındaysa işlem yapmamayı" (aktarım; `poc-vah-val-vwap-…`).
- "kesişim oluşana kadar fiyat çoğu kez %5–10 prim yapar" (aktarım; `momentum-degerden-once-doner-egim-…`).
- "stat-arb sisteminde momentum dönüş teyidi uygulanmasının kârlarda çarpan etkisi" (aktarım; `stat-arb-momentum-donus-teyidi-…`).
- ANN sinyal sonrası "pozitif eğimli sinyaller" ve "ADX + CMF + bullish mum" ile "matematiksel modele görsel onay" (aktarım; `satilik-degil-momentum-teknik-…`).
- Pivot çizgisi için "insanın çizdiği destek/direncin doğrudan kodlanması" (aktarım; `trend-cizgisi-swing-pivot-regresyon-zarf`).
- Yorum: Teyit hep ikinci aşamada: önce konum/bölge, sonra momentum/hacim, sonra fiyat tetiği. Sayısal teyit eşiği hiçbir notta Tansu'dan gelmiyor.

### Risk, pozisyon, stop ve hedef
- "Volatilitesi yüksek hisselerde position sizing'in matematiksel olarak küçülmesi doğru bir risk yönetimi" (aktarım; `volatilite-ters-orantili-position-sizing-…`). "Ana amacın sermayeyi korumak; uygun zamanda oyuna zaten girileceği" (aynı not).
- "Stop Loss seviyesinin her zaman bu orana [1:2 veya 1:3] göre belirlenmesi" (aktarım; `yuksek-ihtimalli-gunluk-islem-bes-kapi`).
- Stop/hedef (Williams notunda, atıf belirsiz): "hedef >= 2R", stop "en yakın swing" (`williams-r-sma-swing-strateji-backtest`, "kullanıcı kuralları").
- ISKPL: hedef = D, bu görselde stop yok (`iskpl-…` görsel: "Stop'a takılan / bozulan : 0").
- Trade'i ciddiye alanlar "ETF'ler ile likit hisseler" (aktarım; `likit-hisseler-etf-…`): "istenen zamanda ve makul fiyata girip çıkabilmek".
- "portföy optimizasyonu ile volatilite trading arasındaki ilişkinin 'huzurlu gecelerin anahtarı'" (aktarım; `portfoy-optimizasyonu-volatilite-trading-risk-butcesi`).
- Şokta: "yeni alım sinyalleri tamamen durdurulur… yalnız mevcut portföyün riski yönetilir" (`volatilite-piyasa-soku-…`).
- Yorum: Tansu'da risk önce gelir (boyut, likidite, şok freni). Ama stopu "R/R'ye göre" kurması, geçersizlikten kurmaya karşı. Bu çelişkiyi Cevo yumuşatıyor; kural yazarken ham cümle esas alınmalı.

### Backtest ve doğrulama görüşü
- "Fikirleri ve piyasa iddialarını test edebilmek"; "indikatör tavsiyelerini doğrudan parayla denemek yerine matematiksel modele ve backteste çevirmek" (aktarım; `python-finans-fikir-dogrulama-ve-yanlislama`).
- "kitaplarda hazır modelleri aynen uygulamak başarı getirmiyor"; gerçek başarı "farklı kaynaklardan öğrenilen modelleri sentezlemek; sabırla backtest ve forward test" (aktarım; `kitap-model-sentezi-…`).
- "Detaylı bir model varsa önce matematiksel olarak kâğıt üzerinde çözmeyi, sonra koda dökmeyi önerdi" (aktarım, kaynak kimliği doğrulanmamış; `kagit-kalem-…`).
- Win rate: "acemi yatırımcıların sık takıldığı, tek başına sistem kalitesini göstermeyen bir metrik" (aktarım; `teknik-indikator-islem-sistemi-degerlendirme-kriterleri`). Toplam net kâr ile maksimum sermaye erimesi birlikte; "kümülatif sermaye eğrisi" basit incelemesi.
- ML için: "ML ile trade yaklaşımını sevmediğini… %70 doğruluğu finans için yüksek" (aktarım; `ml-trade-13-gun-9-isabet`; görselde 9/13, %69,23).
- "Backtest" kanıtı olarak ISKPL ve ML ekranları: konsol çıktıları, seçilmiş tek hisse/kısa dönem.
- Yorum: Tansu kendi kanıtını az örnekli konsol çıktısıyla gösteriyor; yöntem olarak test ister ama out-of-sample göstermiyor. Doğrulama titizliği (FDR, locked OOS) notlarda Cevo'dandır.

### Araçların birleşimi (tarama → filtre → tetik → yönetim)
- "Tarayıcı / sinyal motoru / strateji / backtest" ayrımı Cevo'nun (`uygulama-algoritmalari-v1`). Tansu'nun listesi: arbitraj, volatilite harvesti, ABCD/kelebek/Gartley, alpha ve momentum hisseleri, haftalık kanal dibi, düşeni kıran, takoz/TOBO/OBO/bayrak/flama (aktarım).
- "ANN momentum → pozitif eğim → ADX/CMF/mum → Markowitz → Max Sharpe", "kimler koşmaya hazır? → hangileri doğru yöne bakıyor? → en dengeli takım hangisi?" (kaynak metaforu; `satilik-degil-…`).
- "Pine Script grafik/indikatör/basit sinyal için; Python veri egemenliği, geniş evren tarama, backtest kontrolü, ML/AI ve broker API icrası" (aktarım; `pine-script-python-gorev-ayrimi-…`).
- İki motor kesişimi: sessiz-patlamaya-yakın + IV'ye göre hareket oranı (aktarım; `varyans-risk-primi-model-free-kesisim`).
- Yorum: Tansu'nun düzeni "aday listesi (tarama) → teknik/hacim teyidi → portföy/risk" biçiminde. Tetik ve yönetim katmanı bu notlarda eksik.

### Reddettikleri / eleştirdikleri
- "Ortalamaları temel alan indikatörler… Medyan temelli çalışın." (birebir, X; `medyan-temelli-finansal-indikatorler`).
- Fiyat yönünü kesin tahmin etmeye ve "klasik indikatör parametrelerini geçmişe uydurmaya" çalışmak "en büyük tuzak" (aktarım; `probabilistik-edge-…`).
- Kesinlik dili ("kesin gidecek/uçacak/tavan") "kaçma sinyali" (aktarım; `piyasa-dilinde-kesinlik-…`).
- Monte Carlo'nun "gürültülü bir bulut"u yerine deterministik optimizasyon (aktarım; `spicy-scipy-…`).
- Hazır kütüphane trend çizgileri ve regresyon zarfının "müdahale zorluğu" (aktarım; `trend-cizgisi-…`).
- "BIST'te temel değerlendirmelerin artık önemi olmadığı ve piyasanın güvenilmez aktörlerle dolu olduğu" (aktarım; `sirket-degerlendirme-…`). Yorum: Bu, aynı hasatta değerleme filtreleri (PD/DD, TOPSIS, relatif değerleme) öneren notlarla çelişir; görüşün Tansu'ya aidiyeti de belli değil.
- "Sistem satılık değildir" (aktarım; `satilik-degil-…`).
- Derinliği olmayan alanlar ve sığ hisseler (`likit-hisseler-etf-…`).

### Tekrar eden ilkeler
1. Rejime göre davran: denge/dengesizlik, normal/şok (`piyasa-denge-…`, `volatilite-piyasa-soku-…`, `trend-rejim-…`).
2. Önce sermayeyi koru: boyut küçült, şokta yeni alım yok, likit olanı seç.
3. Sağlam istatistik: medyan, deterministik optimizasyon, olasılık/beklenen değer, kuyruk riski.
4. Çok kanıtı birleştir: bölge + hacim + momentum; temel + teknik + portföy.
5. Fikri koda dök, backtestle sına, sabırla ileri test et.
6. Erken uyarı, geç teyit (eğim ve kesişim; momentum dönüşü stat-arb girişinde).
