# Parça 04: gorsel-paket-01 – 43 (not + görsel) keşfi

Durum: tamamlandı (43 paket, 60 görsel okundu). Okuma: ham not + `assets/gorsel-paket-NN-*/` görselleri. Sadakat kuralı: görsel notla çelişirse görsel esas, çelişki "ÇELİŞKİ" ile işaretli.
Not: `gorsel-paket-26` için not dosyası YOK; yalnız görsel klasörü var (`gorsel-paket-26-top-down-scorecard/01-adim-6-top-down-skor-karti.png`). Görsel okundu, tabloda "26" olarak yer alır.
Tür kısaltmaları: GİRİŞ (giriş/çıkış kuralı), ÇIKIŞ/RİSK, FİLTRE (piyasa/evren), TARAMA (sıralama), YAPI (ortak yapı taşı), DEĞ (değerleme, strateji değil), DEĞ-Ç (değil: strateji dışı).

## 1. Paket tablosu

| Paket | Tür | Açılan görsel | Tek satır |
|---|---|---:|---|
| 01 | GİRİŞ (harmonik/AB=CD, adayı) + YAPI (bölge, hacim profili) | 9 | Harmonik D hedefli tarayıcı çıktıları (KRPLS, DGATE, MARKA #13) ve etiketsiz bölge+hacim profili grafikleri. Kural yok, yalnız hedef/durum etiketi. |
| 02 | TARAMA çıktısı (harmonik) | 2 | SOKE/LUKSK tablosu: Pesavento ve Carney sistemi, D hedefi, giriş 86,95, stop 73,00 (LUKSK). SOKE Gartley X-A-B-C-D. |
| 03 | GİRİŞ (AB=CD backtest) | 2 | SMRTG 12 kalıp: 7 hedef, 3 stop, 2 açık; 100.000 TL -> 405.327,42 TL. Tansu'nun en somut backtest tablosu. |
| 04 | DEĞ-Ç (opsiyon bilgisi) | 2 | TSLA 30 günlük implied move %10,4. Strateji değil; ABD opsiyon verisi. |
| 05 | TARAMA (VRP: VOL AL/SAT) | 1 | BIST VRP tarayıcı; IV yerine "Implied Vol Proxy" kullanıyor; işlem tablosu yok. |
| 06 | TARAMA (sektör momentumu 30/60/90) | 1 | Konsol çıktısı: her ufukta ilk 3 sektör getirisi, 2026-08-14. |
| 07 | FİLTRE (veri anomalisi) | 1 | Dayanıklı Tüketim 30g getiri; \|getiri\| > %50 anomali kuralı (OZATD +%165,06). |
| 08 | FİLTRE (evren: fiili dolaşım oranı) | 1 | Fiili dolaşım oranı tablosu (40 hisse, %0,54-%13,98); eşik değiştirilebilir. |
| 09 | YAPI (arz-talep distal/proximal) | 1 | Distal = base en yükseği (high); proximal = base içindeki en düşük gövde fiyatı. Resmi şema. |
| 10 | YAPI (talep/arz bölgesi izleme) | 1 | HKTM grafiği; çözünürlük düşük, kural/rakam okunamadı. Watchlist, sinyal değil. |
| 11 | YAPI (piyasa yapısı BOS/CHoCH) | 1 | FROTO talep/arz grafiği; tablo "Son Fiyat/Max/Min/En Yakın Demand/D.Touch/D.Teyit/En Yakın Supply/S.Touch/S.Teyit". BOS/CHoCH tanımı metinde; kural rakamı yok. |
| 12 | GİRİŞ adayı (bearish Advance Block + supply) | 1 | DOAS: 3 yükselen mum, küçülen gövde, uzayan üst fitil, arz bölgesi 200,90-209,91. Tek örnek, eşik yok. |
| 13 | YAPI / ÇIKIŞ (talep bölgesi kırılımı) | 1 | TTKOM: talep kutusu ilk kırılımda biter (close < zone_low; sıkı varyant low < zone_low). |
| 14 | DEĞ-Ç | 1 | İşletme analizi kriter listesi (operasyonel/finansal). Strateji değil. |
| 15 | YAPI (RBR talep bölgesi) | 1 | Rally-Base-Rally şeması: proximal = giriş, distal = stop; distal base veya leg-out low. |
| 16 | DEĞ-Ç (fikir) | 1 | Temel metrik ile fiyat ters fazlı çift eksenli grafik; metrik adı, ticker, kural yok. |
| 17 | YAPI (imbalance/FVG gücü) | 1 | "How to judge power of Im-balance": Strongest / Strong / Weak / Weakest-Balance şeması; sayı yok. |
| 18 | YAPI (konsolidasyon kutusu) | 1 | Üst sınır = en yüksek mumun gövde ucu; alt sınır = en düşük fitil. TradingView grafiği (sembol okunamadı). |
| 19 | DEĞ-Ç (kur forward / Monte Carlo) | 2 | USD/TRY grafiği ve forward/Monte Carlo çıktısı (spot 35,85; medyan 57,6114). Alım satım stratejisi değil. |
| 20 | YAPI (sponsor candle / order block) | 1 | Bullish SC = sert yükseliş öncesi son kırmızı mum; bearish aynası. Şema, sayı yok. |
| 21 | TARAMA (confluence: swing + talep + HSAR) | 1 | GC=F grafiği, "CONFLUENCE" yıldızları; HSAR formülü yok; seçilmiş olumlu örnekler. |
| 22 | DEĞ-Ç (süreç şeması) | 1 | "Hisse Senedi Analiz ve Karar Destek Süreci": 10 rasyo, MLP, teknik analiz, AL/TUT/SAT. Kural/rakam yok. |
| 23 | DEĞ-Ç | 1 | FROTO maddi duran varlık ve fiyat çift eksen; korelasyon fikri, kural yok. |
| 24 | DEĞ-Ç | 1 | Merton modeli şeması (A0=100, D=80, σ=%25, DD=0,97, EDF=%16,7). Kredi riski, strateji değil. |
| 25 | DEĞ-Ç | 1 | ASUZU manuel F/K ve FD/FAVÖK hedef fiyat (120,20 ve 119,28 TL; ort. 119,74). Değerleme. |
| 26 | TARAMA/karar (Excel skor kartı) | 1 | Not dosyası YOK. "ADIM 6 TOP-DOWN SKOR KARTI": ağırlıklar 20/20/25/25/10, karar matrisi 4,20-5,00 GÜÇLÜ AL ... Manuel 1-5 puan. |
| 27 | DEĞ-Ç (değerleme) | 2 | ASUZU F/K hedefleri (sektör 7,60x; kısa 14,78x; uzun 10,03x -> 91,33 / 177,61 / 120,53 TL); hisse 29.04.2024'te 118,60 TL ile 120 TL hedefine en yakın. Zaman çizgisi iddiası, işlem kuralı yok. |
| 28 | DEĞ-Ç | 1 | Proje bugünkü değeri: 1 milyar TL / 1,20^3 = 578.703.704 TL (%28,94). Teknik kapı yok. |
| 29 | DEĞ-Ç | 2 | Özsermaye maliyeti (CAPM 22,03; DCF 26,67; tahvil+RP 28,00; ort. 25,56) ve WACC 22,19; EREGL tarihsel nakit akışı. |
| 30 | DEĞ-Ç (makro bilgi) | 2 | FED faiz beklentisi (FOMC 16 Eyl 2026) ve altın fiyatı grafiği. Strateji kuralı yok. |
| 31 | DEĞ-Ç (trend örneği) | 1 | CSCO "TÜM ŞARTLAR SAĞLANDI (GÜÇLÜ TREND)"; gösterge adları beyazla kapatılmış, kural okunamadı. |
| 32 | GİRİŞ adayı (Gartley + AB=CD + talep + düşen kırılımı) | 1 | Sembol yok; "D (CD=1.27AB)", EMA5/8/13, "Direnç TL". Kural/stop/hedef yok; RS "henüz geçmedi". |
| 33 | DEĞ-Ç (portföy optimizasyon) | 1 | Min-vol ve max-Sharpe portföy kapanış getirisi + DEY, BIST100 ile (20-31 Mayıs 2026). Bileşen/ağırlık yok. |
| 34 | GİRİŞ adayı (Siyah Kuğu + talep) | 1 | LIDER: "Düşen Direnci Kıran + Talep + Fibo + ABCD | Harmonik: Siyah Kuğu | Fiyat: 127.40 | Kırılım: 2026-05-18 | Temas: 3 | Lookback: 20". Oran tanımı yok. |
| 35 | GİRİŞ adayı (Beyaz Kuğu + SELL AB=CD) | 1 | Sembol yok; yukarı yönlü AB=CD "D (CD=1.0AB)" ve düşen direnç; yön çatışması. |
| 36 | FİLTRE (volatilite rejimi okları) | 1 | "Volatilite Rejimi: Mevcut (v_t) vs Ortalama (Theta)"; oklar yönsüz. Model/eşik yok. |
| 37 | ÇIKIŞ/RİSK-portföy (gün sonu rebalancing) | 2 | GARAN %50 / KGYO %40 / CCOLA %10; 01.04-15.05.2026; aktif 126.764,84 TL, pasif 127.805,42 TL. Tansu'nun kendi raporunda pasifin gerisinde. |
| 38 | GİRİŞ (haftalık AB=CD + talep + EMA) | 1 | AKCNS haftalık, fiyat 213,60, "D (CD=1.0AB)", talep + EMA. Kural/hedef yok. |
| 39 | GİRİŞ (AB=CD detektör eğitimi, SELL görsel) | 1 | "D (CD=1.0AB)" ve Fib 0,000=13,51 ... 1,000=20,20. Sembol/tarih yok. |
| 40 | GİRİŞ (haftalık BUY AB=CD D talepte) | 1 | "D (CD=1.0AB)" talep bölgesinde, sonra yükseliş; Fib 1,000 ≈ 59,82 gibi (okunamadı). |
| 41 | FİLTRE (konsolidasyon süresi/kırılım şiddeti) | 1 | Ok kümeleri + sarı/cyan dinamik bant; hipotez: konsolidasyon uzadıkça kırılım şiddetlenir. Kural yok. |
| 42 | GİRİŞ (BUY AB=CD + yükselen destek + hedefler) | 1 | "D (ALIM SİNYALİ - CD=1.0AB)", "Hedef 0.618 / 1.000 / 1.618". Sembol yok. |
| 43 | GİRİŞ (RYSAS BUY AB=CD + kanal) | 1 | "KANAL İÇİ NÖTR | Taze D Noktası (Alış) Tespit Edildi!", "D (ALIM SİNYALİ CD=1.27AB)", hedefler 22,60 / 24,20 / 26,80. |
<!--TABLO-->

## 2. Aday modül kartları

### Kart A: AB=CD (ve Gartley/Kelebek) D hedefli harmonik kurulum

- **Tür:** GİRİŞ (aday; kural eksik) + YAPI (swing, Fib, D hesabı).
- **Kaynak:** paket 01 (görseller 01, 03, 05, 06, 09), 02 (01, 02), 03 (01, 02). Birinci el: hepsi Tansu'nun aracının çıktısı. Sonraki paketlerde devam eder (bkz. kart A-EK, paket 32-43).
- **Tansu'nun ifadesi (görselden):**
  - Başlık: "KRPLS - Swing Yapısı, Fibonacci ve AB=CD Analizi (Düşüş)"; lejant: "Swing Low, Swing High, Swing Yapısı (HH/HL/LH/LL), Swing (X -> A), AB=CD Paterni".
  - "D (hedef): 11.29 [TAMAM]", "D (hedef): 10.05 [TAMAM]", "D (hedef): 7.83 [BOZULDU]".
  - "DGATE.IS - Kelebek Formasyonu (AL (Buy)) [AKTİF] — SİSTEM: Pesavento — Tarama eşleşmesi"; "D: 49.66 [AKTİF]"; "X→B trend çizgisi: Kırılım: AŞAĞI yönde, 2026-08-18 tarihinde".
  - "MARKA - Patern #13 Backtest Modu - Düşüş (AB bacağı aşağı)"; "D (hedef) 70.25".
  - "SOKE.IS - Patern #tarama_Carney Detaylı (Fibonacci + Trade Management) | Bullish (LONG) | Sistem: Carney"; lejant: "Gartley XABC", "X-B Trend Çizgisi"; "D (Hedef): 12.53 [Carney]".
  - Tablo: "SAT (taktik KISA, D'ye kadar) — D'de AL'a döner" (SOKE, durum AKTIF, giriş/stop "-"); LUKSK.IS "AL (Buy)" TAMAMLANDI, TEPKI_VERDI, D hedefi 86.95, giriş 86.95, stop (X) 73.00.
- **Kurallar (görselden çıkarılabilen):**
  - D hesabı (KRPLS görselinde ölçülen rakamlarla çıkarım, Tansu'nun yazdığı formül değil): D = C + (B − A) (eşit bacak). Örnek: A=8,23, B=9,86, C=8,42 -> 10,05; A=7,19, B=10,25, C=8,23 -> 11,29. Okuma yaklaşık (grafik ekseninden).
  - Fib çizgileri KRPLS'de B->C bacağına çizilmiş: 0,000=8,42 (C), 1,000=9,86 (B), 1,272=10,25, 1,618=10,75, 2,000=11,30; geri çekilme 0,236=8,76 ... 0,786=9,55 (okunan değerler).
  - Gartley (SOKE Carney): D = 0,786 XA (grafikte "0.786: 12.53"); X≈10,23, A≈21,20, B≈14,02, C≈19,63 (okunan). Stop = X (LUKSK: stop 73,00 sütunu "Stop (X)").
  - Giriş tetiği: YOK (tablo "D hedefi" ile giriş aynı: LUKSK giriş = D = 86,95, yani D'ye değince giriş). Hedef/çıkış kuralı: görselde yok; "TAMAM" etiketi D'ye değmeyi gösterir. Zaman dilimi: günlük gibi görünüyor (SMRTG grafiği 2024-2026 günlük mum); açıkça yazılmamış.
  - Pivot ayarı, oran toleransı, kalıp numaralandırma (#13): görselde yok.
- **Tansu'nun gösterdiği sonuç:** SMRTG backtest tablosu (görselden okundu, notla birebir): Toplam patern 12, hedefe ulaşan 7, stop'a takılan/bozulan 3, açık 2. Başlangıç 100.000,00 TL, bitiş 405.327,42 TL, toplam getiri %305,33.
  İşlemler (C tarihi, sonuç, getiri, sermaye): 2024-03-27 stop -23,29 (76.707,20); 2024-05-06 hedef 36,59 (104.770,81); 2024-07-30 hedef 28,93 (135.079,17); 2025-01-31 hedef 50,72 (203.596,31); 2025-04-16 hedef 47,30 (299.893,39); 2025-08-26 hedef 30,61 (391.676,34); 2025-09-15 stop -12,10 (344.293,73); 2025-09-22 hedef 26,14 (434.281,95); 2025-12-10 hedef 24,20 (539.359,20); 2026-01-29 stop -24,85 (405.327,42).
  Not: işlem tarihi C tarihi; giriş fiyatı ve çıkış fiyatı sütunu yok. Stop getirisi -%23,29 / -%12,10 / -%24,85: stop seviyesi (X?) belirsiz.
- **Veri ihtiyacı:** günlük OHLCV yeterli (swing, Fib, D). Hacim gerekmez.
- **Belirsizlikler:** (1) SMRTG grafiği başlığı "(Yükseliş)" ama etiketli D hedeflerinin çoğu (12,43; 13,37; 7,49; 6,31) aşağıda; yön ve işlem yönü belirsiz (D'de AL mı?). (2) Başlıktaki "Harmonik sayı: 3.02 TL" anlamı yok. (3) Stop kuralı ve hedef kuralı (BOZULDU = ne?) yok. (4) Giriş fiyatı tabloda yok; getiri nasıl hesaplanmış bilinmiyor (notun kendi hesabı bile 57 TL sapıyor). (5) SOKE: "D'ye kadar taktik KISA" yani BIST'te açığa satış kolay değil. (6) 05 numaralı görselde D etiketi "11.20" mi "11.29" mu okunamadı; not 11,29 diyor.
- **Uygulanabilirlik: K.** D geometrisi ve SMRTG tablosu sadakat hedefi olarak güçlü (12 işlem, tarih, getiri). Pivot ayarı, stop ve hedef kuralı eksik; yön belirsiz.

### Kart B: VRP (VOL AL / VOL SAT) tarayıcısı

- **Tür:** TARAMA (volatilite rejimi sinyali); yön sinyali değil.
- **Kaynak:** paket 05 görsel 01 (birinci el); ayrıca paket 04 (TSLA implied move) bağlam. Notun tanım metni ikinci el (kullanıcı iletisi).
- **Tansu'nun ifadesi:** Başlık "BIST Variance Risk Premium (VRP) Scanner (2024-01-01 / 2026-08-01)"; alt başlık "Log Contract • Constant Dollar Gamma Çerçevesi — 2026-08-19 00:35"; paneller "VRP Sıralaması (Yüksek → Düşük)", "RV% vs IV% — Tüm Hisseler", "Dollar Gamma vs Realized Vol Haritası", "Sinyal Dağılımı"; lejant "Implied Vol Proxy", "Realized Vol 21d", "Vol Al", "Vol Sat". Not (kullanıcı özeti): VRP = IV − RV; yüksek VRP = VOL SAT, düşük/negatif = VOL AL.
- **Kurallar:** Eşikler görselde çizgi olarak var (VRP panelinde üst/alt eşik çizgileri), değerleri okunamadı (yaklaşık +0,025 ve -0,005 gibi görünüyor; doğrulanamadı). RV = 21 günlük gerçekleşen volatilite. IV = "Proxy": hesabı yok.
- **Sonuç:** VRP sıralaması: görünen 8-9 hissenin tümü negatif; en düşük HEKTS ≈ -0,195, YKBNK ≈ -0,114, ASELS ≈ -0,082, VESTL ≈ -0,065, AKBNK ≈ -0,058 (okunan). İşlem sonucu/PnL yok.
- **Veri ihtiyacı:** RV günlük OHLCV'den hesaplanır. IV proxy tanımı yok; gerçek IV (VİOP opsiyon zinciri) bedava günlük veride yok.
- **Belirsizlikler:** IV proxy formülü; eşik değerleri; VOL AL/SAT'ın hisse mi opsiyon mu işlemi olduğu; hisse yönü yok.
- **Uygulanabilirlik: X** (IV proxy tanımsız, işlem kuralı yok). RV tarafı yapı taşı olarak kullanılabilir.

### Kart C: Sektör momentumu liderleri (30/60/90 gün)

- **Tür:** TARAMA (sıralama; sektör seçimi).
- **Kaynak:** paket 06 görsel 01 (birinci el, konsol çıktısı); paket 07 görsel 01 aynı hattın anomali adımı.
- **Tansu'nun ifadesi:** "=== Son 30 Günlük Getiride En İyi 3 Sektör ===" (Petrol 0.2389; Mimarlık ve Mühendislik Faal. 0.1431; Mesleki Bilimsel Tekn. Faal. 0.1030); "Son 60 Günlük": Yatırım Şirketleri 0.1289, Petrol 0.1283, Demir Çelik 0.1030; "Son 90 Günlük": Bayındırlık ve İmar 0.2875, Demir Çelik 0.2859, Bilişim ve Yazılım 0.2344. "Name: 2026-08-14 00:00:00, dtype: float64".
- **Kurallar:** Her pencere için sektör getirisi sıralanır; ilk 3 alınır. Pencereler 30/60/90 (takvim mi işlem günü mü: yazılmamış). Sektör getirisi = hisse getirilerinin basit ortalaması (paket 07: "Hisse bazlı basit ortalama (TÜM HİSSELER)"); "Fiyat-ortalaması yöntemi (ESKİ / script'teki)" yanlış bulunmuş. Anomali filtresi: "ANOMALİ OLARAK İŞARETLENEN HİSSELER (|30g getiri| > %50)" ortalamadan çıkarılır. Giriş/çıkış/stop yok.
- **Sonuç (paket 07, görselden):** Dayanıklı Tüketim 18 hisse, 30g getiri: ALCAR -11,55; ARCLK -4,46; ARZUM -12,82; BVSAN -4,93; FORMT -25,33; HATSN -7,92; **HKTM +12,62**; IHEVA -2,43; IMASM -16,23; KLMSN -11,33; MAKIM -12,82; MEKAG -17,93; OZATD +165,06; SAFKR -7,07; SILVR -12,69; SNICA -27,25; VESBE -13,89; VESTL -12,85. Basit ortalama -%1,32; eski fiyat-ortalaması +%90,99; temiz ortalama (17/18) -%11,11; fark 9,79 puan.
  **ÇELİŞKİ:** paket 07 notu HKTM'yi -12,62 yazıyor ve "17/18 negatif, ekran özeti satırlardan uyuşmuyor" sonucuna varıyor. Görselde HKTM +12,62; bununla toplam -23,82/18 = -%1,32 ve temiz -188,88/17 = -%11,11 ekranla uyuşuyor. Yani Tansu'nun hesabı tutarlı, notun "uyumsuzluk" bulgusu not hatasıdır (önceki ikinci okuma KURALLAR.md ana bulgu 3'te "HKTM işareti" hatasını zaten yakalamış).
- **Veri ihtiyacı:** sektör üyelik listesi (BIST sektör sınıfı) + günlük kapanış. Yeterli, ama sektör tablosu ayrı kaynak.
- **Belirsizlikler:** Pencere tanımı, sektör evreni, minimum üye sayısı, "dayanıklı tüketim" üyeliği; sektör sinyalinin hisse girişine nasıl bağlandığı yok.
- **Uygulanabilirlik: K** (tarama olarak kodlanabilir; işlem kuralı yok, sektör tablosu kaynağı ayrı). Anomali kuralı (|30g| > %50) yapı taşı: H.

### Kart D: Fiili dolaşım oranı evren filtresi

- **Tür:** FİLTRE (evren/likidite); strateji değil.
- **Kaynak:** paket 08 görsel 01 (birinci el). Not kullanıcı beyanı: eşik değiştirilebilir, "%30 altı" taramaları sırada.
- **Tansu'nun ifadesi:** Sütunlar "Sembol | Tarih | Fiili Dolaşımdaki Pay Adedi | Fiili Dolaşım Oranı (%)", artan sıra, 40 satır.
- **Kurallar:** oran < eşik olan hisseler. Eşik görselde yok (maksimum görünen 13,98).
- **Sonuç:** KENT 0,54 (1.781.294,53 pay, 2026-05-17); KLNMA 0,92; CMENT 2,71; SNPAM 4,13; GARAN 13,98 (587.338.945,2 pay, 2026-06-02) son satır.
  **ÇELİŞKİ:** Not paket 08, OZATD'yi "%13,22, 65.121.498,70 pay, 2026-08-16" diye aktarıyor ve paket 07'ye bağlıyor. Görsel tablosunda OZATD satırı YOK (40 satırı okudum: ... EGPRO 13,12; VAKKO 13,25; TTKOM 13,31; ORMA 13,32; SANKO 13,48; GEDIK 13,56; GARAN 13,98). 65.12x.xxx kalıbına en yakın satır ADGYO (65.127.946,5; 11,93; 2026-08-16). OZATD'nin float bağlantısı doğrulanamadı.
- **Veri ihtiyacı:** KAP fiili dolaşım (ücretsiz ama günlük OHLCV değil).
- **Belirsizlikler:** eşik, tarih alanı anlamı.
- **Uygulanabilirlik: X** (KAP verisi gerekir; backtest için tarihsel seri yok). Canlı filtre olarak K.

### Kart E: Arz-talep bölgesi: distal / proximal çizgiler (yapı taşı)

- **Tür:** YAPI (bölge sınırı).
- **Kaynak:** paket 09 görsel 01 (şema, birinci el metin); paket 10 görsel 01 (HKTM uygulaması, okunamaz); devamı paket 13, 15, 17, 18, 20, 21.
- **Tansu'nun ifadesi (birebir):** "The distal line is located at the highest of the basing structure while the proximal line is placed at the lowest body price of the base." Şemada rally -> base (2 mum) -> 3 düşüş mumu: arz bölgesi.
- **Kurallar:** Arz için distal = base mumlarının en yüksek HIGH'ı; proximal = base mumlarının gövde alt ucu minimumu (min(open,close)). Talep formülü (ayna) şemada yok; çıkarım: distal = min(low), proximal = max(gövde üstü).
- **Sonuç:** yok (eğitim şeması).
- **Veri ihtiyacı:** günlük OHLC yeterli. Base'in nasıl seçildiği (kaç mum, hangi koşul) görselde yok.
- **Belirsizlikler:** base tespiti; paket 10 HKTM görselinde bölgeler çizili ama rakam okunamadı; "tested demand watchlist" tamamen Cevo yorumu.
- **Uygulanabilirlik: H** (formül kesin) ama giriş/stop kuralı bu paketlerde yok; yalnız yapı taşı.
### Kart E-EK: Bölge ailesi (RBR, konsolidasyon, sponsor candle, imbalance, kırılım)

- **Tür:** YAPI. Kaynak: paket 13, 15, 17, 18, 20 (hepsi tek görsel; 15/17/20 eğitim şeması, 13 TTKOM, 18 TradingView). Not: pakette 13/15/17/18/20 kuralları Levent'in ilettiği Tansu açıklamasıdır (ikinci el); görsel şemalar birinci el.
- **Tansu'nun ifadesi:** 15: "Proximal line / ENTRY POINT", "Distal line stop loss", "DISTAL line always be at the low of base candle or leg out candle in RBR pattern". 17: Strongest/Strong/Weak/Weakest -Balance-. 20: "bullish Sponsor candle", "bearish Sponsor candle". 18 (not-kaynak): üst sınır = en yüksek mumun gövde ucu, alt sınır = en düşük fitil.
- **Kurallar (sayısal):**
  - RBR: proximal = base gövde üstü (giriş), distal = min(base low, leg-out low) (stop). Eşik/ATR yok.
  - Sponsor candle: sert hareket öncesi son zıt renkli mum; bölgeye dönüşte tepki beklenir. Sınır politikası, eşik yok.
  - Imbalance (FVG): bullish gap = low3 - high1 > 0 (görselde şekil; formül nottan, Cevo). Güç sınıfı eşiği yok.
  - Talep kırılımı: close < zone_low (veya low < zone_low); kutu bu tarihte biter (not-kaynak).
  - Konsolidasyon kutusu: [en düşük low, en yüksek mumun gövde ucu].
- **Sonuç:** yok. TTKOM tablosu (görselden): son fiyat 54,50, max 75,85, min 47,48, aktif demand 49,05-51,30, D.Touch 0; aktif supply okunamadı (not 63,29-65,48 diyor; görselde "65.29-66.48" gibi, doğrulanamadı).
- **Veri:** günlük OHLC yeterli (hacim gerekmez).
- **Belirsizlikler:** base/konsolidasyon seçimi, leg-out eşiği, bölge yaşı, kaç mum.
- **Uygulanabilirlik: H** (geometri) ama giriş/stop eşiği olmadan strateji değil; yapı taşı. Giriş yeri: proximal; stop: distal (RBR görselinden birinci el).

### Kart F: BOS / CHoCH piyasa yapısı

- **Tür:** YAPI (trend durumu).
- **Kaynak:** paket 11 görsel 01 (FROTO talep/arz grafiği; birinci el), tanımlar not-kaynak (Levent aktarımı).
- **Tansu'nun ifadesi:** başlık "FROTO - Demand & Supply Bölgesi Analizi"; grafikte "BOS", "HH", "LH", "HL", "LL" etiketleri; tablo sütunları "Son Fiyat | Max | Min | En Yakın Demand | D.Touch | D.Teyit | En Yakın Supply | S.Touch | S.Teyit". Okunan değerler (küçük, yaklaşık): son 78,10; max 135,40; min 73,05; demand 74,73-76,70 (touch 1, teyit 2026-08-14); supply 90,10-92,69 (touch 1, teyit 2026-06-30).
- **Kurallar:** Kaynak tanımı: BOS = trend yönünde önceki swing'in kırılması; CHoCH = korunan karşı swing'in ilk kaybı. Pivot ayarı, kırılım temeli (kapanış/fitil), tampon: YOK. Notta verilen formüller Cevo'dur.
- **Veri:** günlük OHLC yeterli.
- **Belirsizlikler:** CHoCH etiketi görselde okunamadı (not da aynısını söylüyor).
- **Uygulanabilirlik: K** (yapı taşı; pivot ayarı yorum).

### Kart G: Advance Block (bearish tükenme) + arz bölgesi

- **Tür:** GİRİŞ adayı (kısa/uzak durma sinyali); BIST'te yön satış.
- **Kaynak:** paket 12 görsel 01 (DOAS, birinci el görsel; tanım not-kaynak).
- **Tansu'nun ifadesi:** başlık "DOAS - Demand & Supply Bölgesi Analizi"; tablo: Son Fiyat 171,20; Max 247,00; Min 166,40; En Yakın Demand 165,59-173,00, D.Touch 3, D.Teyit 2025-11-04; En Yakın Supply 200,90-209,91, S.Touch 2, S.Teyit 2026-06-25 (görselle uyumlu). Kırmızı kutu Haziran 2026 tepesini işaretler.
- **Kurallar (not-kaynak):** 3 art arda yükseliş mumu; gövdeler küçülür; üst fitil uzar; her mum önceki gövde içinde açılır; trendin sonunda. Eşik rakamı yok; stop/hedef yok.
- **Sonuç:** tek örnek, fiyat sonra 171,20'ye düştü (hedefe vurma yok).
- **Veri:** günlük OHLC yeterli.
- **Uygulanabilirlik: X** (eşik yok, yön satış; BIST'te açığa satış). Mum yapı taşı olarak K.

### Kart I: Confluence alan taraması (swing + talep + HSAR)

- **Tür:** TARAMA/FİLTRE (bölge kesişimi).
- **Kaynak:** paket 21 görsel 01 (GC=F, birinci el); not-kaynak.
- **Tansu'nun ifadesi:** "GC=F | Fiyat: 4448.90 | Swing Point + Talep Bölgesi + HSAR Destek Analizi"; lejant "Fiyat, EMA 9, EMA 21, EMA 50, EMA 100, EMA 200, Düşen Direnç (Kırılım), Swing Points, Talep+HSAR Kesişimi"; etiket "CONFLUENCE"; Fib çizgileri (1.000 ... 0.236, okunamayan fiyatlar).
- **Kurallar:** swing + talep bölgesi + HSAR desteği aynı yerde = CONFLUENCE. HSAR tanımı yok. Giriş/stop/hedef yok.
- **Sonuç:** işaretli ~5 alanın ardından yükseliş (seçilmiş örnekler; GC=F 2023-2026 boğa).
- **Veri:** günlük OHLC.
- **Uygulanabilirlik: X** (HSAR tanımsız, kural yok).
### Kart A-EK: AB=CD "D'de alım" varyantı ve SMRTG getirilerinin çözümü (paket 32, 34, 35, 38, 39, 40, 42, 43)

- **Tür:** GİRİŞ (aday; giriş = D tamamlanması), hedef merdiveni var, stop yok.
- **Kaynak:** hepsi birinci el görsel (Tansu'nun aracı), tek hisse/tek görsel. Semboller: 43 RYSAS.IS, 38 AKCNS (haftalık), 34 LIDER, diğerleri sembolsüz. Yorum satırları (Levent iletisi) ikinci el.
- **Tansu'nun ifadesi (görselden):**
  - 43: "RYSAS.IS — Kanal Durumu: KANAL İÇİ NÖTR | Taze D Noktası (Alış) Tespit Edildi!"; "D (ALIM SİNYALİ CD=1.27AB)"; "Hedef 0.618 (22.60)", "Hedef 1.000 (24.20)", "Hedef 1.618 (26.80)".
  - 42: "D (ALIM SİNYALİ - CD=1.0AB)", "Hedef 0.618 / Hedef 1.000 / Hedef 1.618".
  - 38: "AKCNS | HAFTALIK ABCD FORMASYONU + Talep + EMA | Fiyat: 213.60"; "D (CD=1.0AB)".
  - 40 ve 39: "D (CD=1.0AB)"; 39 Fib: "1.000 | 20.20, 0.786 | 18.77, 0.618 | 17.64, 0.500 | 16.86, 0.382 | 16.07, 0.236 | 15.09, 0.000 | 13.51".
  - 32: lejant "Fiyat, EMA5, EMA8, EMA13, Direnç TL, ABCD (BUY), Harmonik (Gartley), Hacim, Kum. Delta"; "D (CD=1.27AB)".
  - 34: "LIDER | Düşen Direnci Kıran + Talep + Fibo + ABCD | Harmonik: Siyah Kuğu | Fiyat: 127.40 | Kırılım: 2026-05-18 | Temas: 3 | Lookback: 20".
- **Kurallar (sayılarla):**
  - Şablon (BUY): A tepe, B dip, C daha alçak tepe (B < C < A), D daha alçak dip. D = C − (A − B) kadar (CD = 1,0 × AB) ya da CD = 1,27 × AB. Etiketlerde yalnız 1,0 ve 1,27 görüldü.
  - Hedefler: D + {0,618; 1,000; 1,618} × (A − D). Doğrulama (RYSAS, görselden): 22,60, 24,20 ve 26,80 değerleri D ≈ 20,0 ve A = 24,20 ile tutuyor (20,0 + 0,618 × 4,2 ≈ 22,6; 20,0 + 1,618 × 4,2 ≈ 26,8). Yani Hedef 1,000 = A. Bu önceki okumadaki "D + {0,618; 1; 1,618}(A−D)" kuralıyla uyumlu.
  - Teyit katmanı (Tansu'nun gösterdiği, eşiksiz): talep bölgesi (D'nin yeşil bölgede olması), kanal/yükselen destek konumu, düşen direnç kırılımı, EMA5/8/13 toparlanması, hacim ve kümülatif delta. Dedektör ayarı, tolerans, tepe/dip penceresi: görselde yok.
  - Stop: görselde yok. Kanal alt bandı ya da talep distal'i olabilir (YORUM).
  - Zaman dilimi: günlük (RYSAS, LIDER, SMRTG) ve haftalık (AKCNS, paket 40).
- **Sonuç (Tansu'nun gösterdiği):** yalnız seçilmiş olumlu örnekler: AKCNS D sonrası talepte taban, sonra güçlü yükseliş (fiyat 213,60); paket 40 D talepte, sonra yükseliş (Levent: "kütür kütür gitmiş"); RYSAS ve 42 D'ye yeni ulaşmış, sonuç yok. Başarısız örnek: yok (başarısız örnekler SMRTG tablosunda ve BALAT'ta, paket 45'te).
- **SMRTG getiri sütununun çözümü (benim hesabım, grafik okuması ±0,1):** Tablodaki "hedef" getirileri (C'den D hedefine düşüş) olarak yeniden üretiliyor: 2025-01-31: C ≈ 15,2, D = 7,49 -> %50,7 (tablo 50,72); 2025-04-16: C ≈ 12,0, D = 6,31 -> %47,4 (tablo 47,30); 2024-07-30: A ≈ 21,2, B ≈ 15,7, C ≈ 18,8 -> D = C − (A − B) ≈ 13,3-13,4, (18,8 − 13,37) / 18,8 = %28,9 (tablo 28,93). Yani Tansu'nun backtest getirisi C'den D'ye (aşağı) fiyat farkıdır: C fiyatından aşağı yönlü hareket (kısa) olarak ölçülmüş, "D'de AL" değil. Bu, KURALLAR.md'nin "C fiyatından giriş, aşağı yönlü" tespitiyle uyumlu; kesin değil (C değerleri okuma).
  **ÇELİŞKİ (paket 03 notu):** not "Pattern geçmişi (Yükseliş)" ve D hedeflerini yükseliş senaryosu gibi okuyor; görseldeki D hedefleri çoğunlukla altta (12,43; 13,37; 7,49; 6,31 TAMAM; 27,34; 11,83; 7,85; 5,89 BOZULDU gibi), sağ uçta tek yukarı hedef 16,75 ve D 8,83.
- **Veri ihtiyacı:** günlük/haftalık OHLC (kümülatif delta ve hacim isteğe bağlı; delta tanımı bilinmiyor).
- **Belirsizlikler:** tepe/dip bulma, oran toleransı, stop, BOZULDU eşiği, yön (D'de alım mı C'den kısa mı), Siyah/Beyaz Kuğu oranları (paket 34, 35: tanım yok).
- **Uygulanabilirlik: K.** SMRTG tablosu yeniden üretilebilir (sadakat hedefi), D ve hedef formülü belli; pivot ayarı ve stop yok. C'den kısa yön BIST'te uygulanamaz; D'de alım yön olarak olası ama Tansu'nun sayısal sonucu yok.

### Kart J: Siyah Kuğu / Beyaz Kuğu

- **Tür:** GİRİŞ etiketi (formasyon adı). **Kaynak:** paket 34 (LIDER), 35 (sembolsüz).
- **Tansu'nun ifadesi:** 34: "Harmonik: Siyah Kuğu"; 35 (Levent iletisi): "Düşeni kırmış, SELL yönlü AB=CD'yi tamamlamış, Beyaz Kuğu da oluşmuş; bunu yolculamayalım mı?"; 34 (Levent iletisi): "Kuğuyu talep toplama bölgesinde yakalarsanız böyle RUN olur grafiğiniz".
- **Kurallar:** oran/tanım YOK. 34 grafiğinde Fib: 1,000 = 154,xx (okunamadı), 0,500 = 127,57, 0,236 = 113,44, 0,000 = 101,19 (yaklaşık okuma). Siyah Kuğu çizimi grafiğin başında (Şubat-Mart 2026) 65-83 bandında talep bölgesi (yeşil, ≈78-81) içinde.
- **Sonuç:** LIDER ≈ 65-83 bandından Nisan zirvesi ≈ 154'e yükseldi; sonra ≈ 101'e düşüp 127,40'a toparlandı. Seçilmiş örnek.
- **Uygulanabilirlik: X** (oran tanımı yok; adın kendisi Taleb'in kuğusu değil, harmonik etiket).

### Kart K: Volatilite rejimi okları (v_t / Theta)

- **Tür:** FİLTRE/YAPI (volatilite rejimi). **Kaynak:** paket 36 (birinci el görsel; Levent iletisi), paket 41 (aynı ok aracı).
- **Tansu'nun ifadesi:** alt panel "Volatilite Rejimi: Mevcut (v_t) vs Ortalama (Theta)"; Levent iletisi: "Çizgi çizmeye gerek yok; kırmızı oklar illa düşeceği anlamına gelmez, oynaklığı belirler. Rehavet ortamı vardır ve fiyat bir yöne kırılacaktır." Paket 41 (Levent): ok alanı yatayda ne kadar geniş (konsolidasyon uzun) ise kırılım o kadar şiddetli; kısa bir konsolidasyonun güçlü kırılması kendisini de şaşırttı.
- **Kurallar:** eşik/formül YOK. Görselden çıkarım (YORUM, ilk okuma): kırmızı ok kümeleri v_t'nin gri bandın alt bölgesinde ve Theta'nın altında olduğu dönemlerde (örn. 2024 başı, Ocak-Mart 2025), yeşil ok kümesi Nisan 2025'te v_t'nin ≈4,3'e sıçradığı anda; paket 36 notu "ok rengi eşlemesi belirsiz" diyor, görsel bunu kısmen çözüyor.
- **Sonuç:** Nisan 2025 yeşil okların ardından sert çıkış değil sakin bir dönem; 2025 sonu-2026 başında güçlü yükseliş. Sayı yok.
- **Veri ihtiyacı:** günlük OHLC (volatilite modeli bilinmiyor; mean-reversion modeli ima ediliyor).
- **Uygulanabilirlik: X** (model ve eşik yok).

### Kart L: Gün sonu sabit ağırlık yeniden dengeleme (GARAN / KGYO / CCOLA)

- **Tür:** portföy yönetimi kuralı (giriş/çıkış değil).
- **Kaynak:** paket 37, görsel 01 (Portföy K/Z raporu) ve 02 (işlem logu); birinci el.
- **Tansu'nun ifadesi:** "PORTFÖY K/Z RAPORU | 15.05.2026", "GARAN.IS %50 | KGYO.IS %40 | CCOLA.IS %10 | 01.04.2026 - 15.05.2026"; "İŞLEM LOGU | GARAN.IS <-> KGYO.IS <-> CCOLA.IS | Toplam 30 İşlem"; Levent iletisi: gün sonu ekleme/eksiltmelerle, efor sarf etmeden yaklaşık 1,5 ayda %27 sistem getirisi.
- **Kurallar:** her gün sonu portföyü hedef ağırlıklara (50/40/10) döndür; üç hisse. Eşik/bant yok.
- **Sonuç (görselden):** başlangıç 100.000,00 TL; son kapanış 126.764,84 TL (%26,76); pasif (al-tut) portföy 127.805,42 TL (%27,81); aktif - pasif fark -1.040,58 TL (-%1,04, durum "REBAL-"); günlük K/Z -2.668,92 TL (-%2,06); bileşen getirileri GARAN %4,85, KGYO %58,21, CCOLA %20,98. Log başlığı: Toplam Rebalans 30 gün, Toplam Hacim ≈ 76.623 TL, Ort. İşlem 2.554,13 TL, En Büyük İşlem 7.825,91 TL (rakamlar küçük, yaklaşık). Yani Tansu'nun kendi çıktısında yeniden dengeleme pasif al-tut'un gerisinde; getirinin kaynağı hisse seçimi (özellikle KGYO).
- **Veri ihtiyacı:** günlük kapanış yeterli; işlem fiyatı/maliyet bilinmiyor.
- **Belirsizlikler:** işlem fiyatı (kapanış mı), maliyet, hisse seçiminin nedeni.
- **Uygulanabilirlik: H** (kural belli; ama alfa iddiası zayıf: pasifi geçemedi).

### Kart M: Min-vol / Max-Sharpe portföy (BIST100)

- **Tür:** portföy kurulumu (strateji değil). **Kaynak:** paket 33 görsel 01 (birinci el).
- **Tansu'nun ifadesi:** "Portföy Kapanış Performansı, DEY Marjı ve BIST100 Karşılaştırması (Excel Base 100)"; lejant "MV - Kapanış Getirisi, MV - DEY (Kümülatif En Yüksek), MS - Kapanış Getirisi, MS - DEY (Kümülatif En Yüksek), BIST100 Benchmark".
- **Sonuç (okuma ±1):** 20-31 Mayıs 2026; Min Volatility kapanış ≈ 115, DEY ≈ 123,7; Max Sharpe kapanış ≈ 108,7, DEY ≈ 118,3; BIST100 ≈ 97,8. Bileşen, ağırlık, pencere yok.
- **Uygulanabilirlik: X** (bileşen ve ağırlık yok).

### Kart N: Skor kartı ve karar süreçleri (paket 22, 26)

- **Tür:** DEĞ-Ç / karar şeması. **Kaynak:** 22 (süreç infografiği), 26 (Excel; not dosyası yok).
- **İfade (görsel):** 26: "ADIM 6 — TOP-DOWN SKOR KARTI VE NİHAİ KARAR"; ağırlıklar Makro 20, Sektör 20, Şirket Analizi (Nitel) 25, Finansal Analiz 25, Değerleme (Güvenlik Marjı Etkisi) 10; karar matrisi 4,20-5,00 GÜÇLÜ AL; 3,40-4,19 AL; 2,60-3,39 TUT; 1,80-2,59 SAT; 1,00-1,79 GÜÇLÜ SAT. Puan 1-5, elle girilir. 22: "10 finansal rasyo", "MLP Sinir Ağı", "Grafiksel Teknik Analiz", "AL / TUT / SAT".
- **Uygulanabilirlik: X** (puanlar manuel/nitel; 22'de rasyo listesi yok).
<!--KARTLAR-->

## 3. Ortak yapı taşları ve çapraz referanslar

### Ortak yapı taşları (bu parçada)

1. Swing tepe/dip (pivot): ayar yok; paket 01, 02, 03, 11, 32-43.
2. AB=CD / harmonik D hesabı: D = C ± (B − A); oranlar 1,0 ve 1,27; hedef merdiveni 0,618 / 1,0 / 1,618: paket 01, 03, 32, 38-43. Gartley D = 0,786 XA (paket 02).
3. Fibonacci çizgileri (0,000 ... 1,000; 1,272; 1,618; 2,000): paket 01, 21, 34, 39.
4. Arz-talep bölgesi (distal/proximal): paket 09, 10, 11, 12, 13, 15, 18, 20, 21; yaşam döngüsü: temas sayısı (D.Touch / S.Touch) ve teyit tarihi (D.Teyit / S.Teyit) tablo sütunları (paket 10-13, 21 ve diğerleri).
5. FVG/imbalance: bullish gap = low3 − high1 (paket 17). Order block/sponsor candle: paket 20.
6. BOS / CHoCH: paket 11.
7. Düşen direnç / yükselen destek / kanal çizgisi: paket 32, 34, 35, 38, 40, 42, 43 (çizim yöntemi yok; "Temas: 3 | Lookback: 20" yalnız paket 34 başlığında).
8. EMA5/8/13 (paket 32, 34, 35, 38, 40), EMA 9/21/50/100/200 (paket 21 lejantı).
9. Hacim profili / kümülatif delta (paket 01, 32, 34, 38, 40, 42): delta tanımı yok.
10. Volatilite: RV 21 gün (paket 05), v_t / Theta (paket 36), implied move (paket 04).
11. Evren filtresi: fiili dolaşım oranı (paket 08); anomali dışlama |30g getiri| > %50 (paket 07).

### Aynı fikrin başka paketlerde geçtiği yerler

- ABCD "D'de alım" ailesi: 32, 35 (SELL aynası), 38, 39 (SELL), 40, 42, 43; backtest tablosu yalnız 03; SOKE/LUKSK durum listesi 02; KRPLS/MARKA/DGATE 01. Parça 05 ve 06'daki paketler (45, 47, 109, 122-123) aynı aileyi sürdürüyor (bu parçada okunmadı).
- Talep/arz bölgesi + sinyal etiketleri ("D.Touch", "D.Teyit"): 10, 11, 12, 13, 21; devamı paket 93, 99, 105 (diğer parçalar).
- Volatilite rejimi okları: 36 ve 41 (aynı araç); VRP 05; implied move 04; paket 48-50 (diğer parça).
- Sektör rotasyonu: 06 ve 07; devamı 51 (diğer parça).
- Değerleme çarpanı/DCF: 14, 23-25, 27-29; devamı 73, 77-91.

### Önceki okumayla (docs/KURALLAR.md) karşılaştırma

Uyumlu: (a) AB=CD D = C + r(B−A), r 1,0 / 1,27; hedef D + {0,618; 1; 1,618}(A−D): RYSAS görselindeki 22,60 / 24,20 / 26,80 ile tutuyor. (b) SMRTG işlemleri C fiyatından aşağı yönlü: getirilerim yeniden üretildi (Kart A-EK). (c) Not-görsel çelişkisi (HKTM işareti): paket 07 görselinde HKTM +12,62.
Çelişki / ek:
1. **Paket 07 notu yanlış, Tansu tutarlı:** HKTM +12,62 (notta -12,62); notun "ekran özeti satırlardan uyuşmuyor, data_inconsistency" bulgusu geçersiz. Ekran özeti (-%1,32; -%11,11; fark 9,79) satırlarla uyuşuyor. KURALLAR.md satırı "Sektör liderleri ... anomali temizliği: H, birinci el konsol çıktısı" doğru.
2. **Paket 08 notu:** OZATD satırı görsel tablosunda yok; "OZATD %13,22 / 2026-08-16 / 65.121.498,70" notun yanlış okuması (satır görselde bulunamadı). Paket 07-08 çapraz bulgusu çöküyor.
3. **KURALLAR.md "Gartley D formülü tabloda ters":** bu parçada Gartley D = 0,786 XA, SOKE Carney görselinde birebir ("0.786: 12.53"). "Tabloda ters" iddiası bu parçada doğrulanamaz (paket 123 parça 06 kapsamında).
4. **Paket 03 notu** SMRTG'yi "yükseliş" olarak okuyor; getiriler aşağı yön (kısa C→D) olarak çözülüyor.
5. **Önceki okumada olmayan:** paket 37 Tansu'nun kendi çıktısında rebalancing pasifin 1,04 puan gerisinde; paket 36'daki ok rengi eşlemesi görselden kısmen çıkarılabilir (kırmızı = düşük v_t, yeşil = yüksek sıçrama; ilk okuma). Paket 26 not dosyası yok (görsel var).
6. **Paket 19:** görsel başlığı USDTRY; not da bunu söylüyor; anlatıdaki EUR/TRY 57,61 ile uyumsuz (not zaten işaretli).
7. Okunamayanlar: paket 05 VRP eşik değerleri; paket 10 HKTM tablo/seviyeleri; paket 13 aktif supply aralığı (not 63,29-65,48; görselde 65,29-66,48 gibi); paket 01/05 D değeri 11,29 mu 11,20 mi; paket 40 Fib seviyeleri.

<!--SON-->


## Tansu'nun bakış açısı (ipuçları)

Biçim: alıntı + dosya. "(görsel)" = görselden okunan birebir metin (birinci el). "(not-kaynak)" = notun "Kaynak" bölümündeki aktarım (Levent'in ilettiği Tansu açıklaması; ikinci el, birebir değil). Yorum satırları bana aittir.

### Kurulumu neye göre seçiyor (arz-talep, confluence)
- "The distal line is located at the highest of the basing structure while the proximal line is placed at the lowest body price of the base." (görsel) — gorsel-paket-09/01-distal-proximal-arz-bolgesi.png
- "DISTAL line always be at the low of base candle or leg out candle in RBR pattern"; "NOTE:-RBR Pattern forms in uptrend" (görsel) — gorsel-paket-15/01-rally-base-rally-rbr-pattern.png
- "How to judge power of Im-balance": Strongest / Strong / Weak / Weakest -Balance- (görsel) — gorsel-paket-17/01-bullish-imbalance-strength-ranking.jpg
- Konsolidasyon "üst sınırı en yüksek mumun gövdesinin bittiği yer, alt sınırı en düşük mumun gölgesinin bittiği yerdir"; "denenip sonuçlarının paylaşılmasını" öneriyor (not-kaynak) — gorsel-paket-18-konsolidasyon-body-wick.md
- Confluence alanlarının "grafiklerde aranıp taratılması gerektiğini ve gösterilen örneklerde her seferinde büyük değer artışı yarattığını" savunuyor (not-kaynak) — gorsel-paket-21-confluence-alan-taramasi.md; görsel: GC=F başlığı "Swing Point + Talep Bölgesi + HSAR Destek Analizi", lejant "Talep+HSAR Kesişimi" — gorsel-paket-21/01-gcf-swing-demand-hsar-confluence.png
- Distal/proximal çizgilerini anlamak "işin yarısı", tarayabilmek "kalan yarısı" (not-kaynak) — gorsel-paket-09-distal-proximal-arz-talep.md
- Sponsor candle: büyük kurumların bıraktığı "ayak izi / akıllı para" (not-kaynak); görsel: "Here is a diagram of a bullish Sponsor candle" — gorsel-paket-20/01-bullish-bearish-sponsor-candle.png
- Yorum: Tansu kurulumu fiyat geometrisinden (bölge sınırı, swing, destek kesişimi) seçiyor ve aracı çok katmanlı grafikle sunuyor (bölge + hacim profili + hacim + momentum + RSI paneli, gorsel-paket-01/04). Bağımsız kanıt ayrımı bu paketlerde Tansu'dan değil, notların Cevo katmanından geliyor.

### Girişi nasıl teyit ediyor, durum mantığı
- Etiketler "[TAMAMLANDI]", "[AKTİF]", "TEPKI_VERDI", "BOZULDU", "TAMAM" (görsel) — gorsel-paket-01/*, 02/01, 03/01
- "SAT (taktik KISA, D'ye kadar) — D'de AL'a döner" (görsel) — gorsel-paket-02/01-soke-luks-coklu-sistem-sonuclari.png
- Advance Block: yükseliş trendinin sonlarında "bearish exhaustion/yorgunluk sinyali" (not-kaynak) — gorsel-paket-12-doas-advance-block.md
- Talep bölgesi kırılımı: ilk alt kırılımı bul, "kutuyu o tarihte bitir" (not-kaynak) — gorsel-paket-13-ttkom-demand-invalidation.md
- Yorum: Tansu'nun yöntemi hedef/bölge odaklı: D'ye ulaşma ve bölgeye tepki; stop için X noktası (LUKSK stop 73,00 = "Stop (X)" sütunu). Tetik/teyit kuralı yok.

### Risk, volatilite, rejim
- VOL SAT: şişmiş beklenti sönmesi; VOL AL: "fırtına öncesi sessizlik" (not-kaynak) — gorsel-paket-05-bist-vrp-scanner.md; görsel başlık "Log Contract • Constant Dollar Gamma Çerçevesi" — gorsel-paket-05/01-bist-vrp-scanner-dashboard.png
- "30-Günlük Implied Move=%10.4" (görsel) — gorsel-paket-04/01-tsla-implied-move-options-chain.png
- Yorum: Tansu volatiliteyi sinyal (VRP) ve beklenen hareket bandı olarak okuyor; yönsüz.

### Veri kalitesi, ortalamayı bozan uç gözlem
- "ANOMALİ OLARAK İŞARETLENEN HİSSELER (|30g getiri| > %50)": "OZATD.IS : %+165.06 <-- ANOMALİ, ortalamadan çıkarıldı" (görsel) — gorsel-paket-07/01-dayanikli-tuketim-anomali-temizleme.png
- "Fiyat-ortalaması yöntemi (ESKİ / script'teki) : %+90.99" (görsel; eski yöntemi hatalı gösteriyor) — aynı dosya
- Sektör rotasyonunda hisse anomalileri çıkarılmazsa ortalamanın yanıltacağı vurgusu (not-kaynak) — gorsel-paket-07-sektor-anomali-temizleme.md
- Yorum: Tansu kendi aracındaki hatayı ("ESKİ / script'teki") görünür biçimde düzeltip raporluyor; aykırı değere karşı hassas. Aritmetik ortalama yerine anomalisiz ortalama kullanıyor.

### Sektör ve çoklu ufuk
- "=== Son 30 / 60 / 90 Günlük Getiride En İyi 3 Sektör ===" (görsel) — gorsel-paket-06/01-sektor-liderleri-30-60-90-gun.png
- Yorum: Tansu liderliği tek pencereye bağlamıyor; üç ufku yan yana veriyor.

### Doğrulama ve backtest
- "BACKTEST SONUÇLARI (SMRTG)": "Hedefe ULAŞAN : 7", "Stop'a takılan / bozulan : 3", "Henüz sonuçlanmamış (açık) : 2" (görsel) — gorsel-paket-03/02-smrtg-backtest-sonuclari.png. Stop'lu işlemleri de gösteriyor.
- "MARKA - Patern #13 Backtest Modu" (görsel) — gorsel-paket-01/09-marka-pattern13-backtest-dusus.png: projeksiyon gerçekleşmemiş yol olarak gösteriliyor.
- Yorum: Tansu başarısız örnekleri (stop, BOZULDU) saklamıyor; ama örneklem 12 kalıp tek hisse, masraf yok.

### Araçları birleştirme (tarama -> filtre -> tetik -> yönetim)
- "Sistem: Pesavento", "Sistem: Carney", "Fibonacci + Trade Management" (görsel) — gorsel-paket-01/06, gorsel-paket-02/02
- "Temel Analiz ve Filtreleme Süreci ... 10 finansal rasyo", "MLP Sinir Ağı Değerlendirmesi", "Grafiksel Teknik Analiz", "Nihai Yatırım Önerisi ... Al, Sat veya Tut" (görsel) — gorsel-paket-22/01-hisse-analiz-karar-destek-sureci.jpg
- "ADIM 6 — TOP-DOWN SKOR KARTI VE NİHAİ KARAR": Makro 20, Sektör 20, Şirket (Nitel) 25, Finansal 25, Değerleme (Güvenlik Marjı Etkisi) 10; "GÜÇLÜ AL 4.20-5.00 ... GÜÇLÜ SAT 1.00-1.79" (görsel) — gorsel-paket-26-top-down-scorecard/01-adim-6-top-down-skor-karti.png
- Yorum: Tansu iki ayrı hat kuruyor: (1) teknik tarayıcılar (harmonik, bölge) ve (2) temel/top-down puanlama; ikisini tek tetiğe bağlamıyor. Skor kartı el ile 1-5 puanlıdır.

### Piyasa/değerleme görüşü
- Medyan Monte Carlo kuru, bankanın forward teklifine karşı pazarlık referansı; "bankaya golü attık" (not-kaynak) — gorsel-paket-19-eurtry-forward-monte-carlo.md
- Maddi duran varlık artışı "er ya da geç fiyata yansır", korelasyon "çok kuvvetli" (not-kaynak) — gorsel-paket-23-froto-ppe-fiyat.md; temel strateji ile momentum stratejisi "birlikte çalışır", mavi/kırmızı seri ters fazlı (not-kaynak) — gorsel-paket-16-temel-momentum-ters-faz.md
- Yorum: Tansu fiyatı bilanço büyüklüklerinin gecikmeli yansıması olarak görüyor; seviye korelasyonunu kanıt sayıyor (nedensellik testi yok).

### Ek ipuçları (paket 27-43)

Girişi nasıl teyit ediyor / kurulumu neye göre seçiyor:
- "ABCD'ye gözü kapalı güvenilmez; kanalı okumadan iş yapılmaz" (not-kaynak, Levent iletisi) — gorsel-paket-43-rysas-buy-abcd-kanal-baglamı.md; görsel: "KANAL İÇİ NÖTR | Taze D Noktası (Alış) Tespit Edildi!" — gorsel-paket-43/01-rysas-buy-abcd-yukselen-kanal.png
- "ABCD tam talep toplama bölgesinden haftalıkta tepkisini almış, kütür kütür gitmiş; bu yapıların peşindeyiz" (not-kaynak) — gorsel-paket-40-haftalik-abcd-talep-tepki.md
- "Kuğuyu talep toplama bölgesinde yakalarsanız böyle RUN olur grafiğiniz" (not-kaynak) — gorsel-paket-34-siyah-kugu-talep-run.md
- "Düşeni kırmış, SELL yönlü AB=CD'yi tamamlamış, Beyaz Kuğu da oluşmuş; bunu yolculamayalım mı?" (not-kaynak) — gorsel-paket-35-beyaz-kugu-sell-abcd-dusen-kirilimi.md
- "Not alın, süper bir yapı" (not-kaynak) — gorsel-paket-38-akcns-haftalik-abcd-talep-ema.md; "Şimdi ne diyeyim yani buna :)" — gorsel-paket-42-buy-abcd-yukselen-destek-hedefler.md
- Hissenin "henüz endeksi yenecek güçte olmadığını; formasyonların fiyatı bu yöne itmesini umduğunu ve ertesi gün izleme niyetini" ifade ediyor (not-kaynak) — gorsel-paket-32-gartley-abcd-talep-dusen-kirilimi.md
- Yorum: Tansu kurulumu çoklu çakışmayla seçiyor (formasyon + talep bölgesi + düşen direnç kırılımı + kanal/destek konumu + EMA/hacim/delta), "talep toplama bölgesinde" olmasını ayırt edici sayıyor ve endekse göre göreli güçle (paket 32) ek süzgeç düşünüyor. Hepsi seçilmiş olumlu grafiklerle anlatılıyor; ret edilen örnek bu paketlerde yok (başarısız örnekler SMRTG tablosunda).

Stop/hedef mantığı:
- Hedefler "Hedef 0.618 (22,60) / Hedef 1.000 (24,20) / Hedef 1.618 (26,80)" (görsel) — gorsel-paket-43/01-rysas-buy-abcd-yukselen-kanal.png; "Hedef 0.618 / 1.000 / 1.618" — gorsel-paket-42/01-buy-abcd-d-yukselen-destek.png
- Yorum: Hedef = A-D mesafesinin oranları (D'den yukarı); stop görselde yok. Tansu çoklu kademeli hedef düşünüyor.

Piyasaya bakış (volatilite, rejim, rehavet):
- "Çizgi çizmeye gerek yok; kırmızı oklar illa düşeceği anlamına gelmez, oynaklığı belirler. Rehavet ortamı vardır ve fiyat bir yöne kırılacaktır." (not-kaynak) — gorsel-paket-36-volatilite-rehavet-yon-bagimsiz-kirilim.md; görsel "Volatilite Rejimi: Mevcut (v_t) vs Ortalama (Theta)" — gorsel-paket-36/01-volatilite-rejimi-rehavet-oklari.png
- Okların bulunduğu alan yatayda ne kadar geniş (konsolidasyon uzun) ise kırılım o kadar şiddetli (not-kaynak, hipotez); kısa konsolidasyonda güçlü kırılım kendisini de şaşırttı — gorsel-paket-41-konsolidasyon-suresi-kirilim-siddeti.md
- Yorum: Tansu volatiliteyi ortalamaya dönen bir süreç (Theta) ve yönsüz kırılım olarak görüyor; "rehavet" düşük oynaklık rejimini kırılım habercisi sayıyor. Kendi hipotezinin çürütücü örneğini de paylaşıyor ("beni de şaşırttı").

Risk, portföy, doğrulama:
- "rebalancing stratejisini öğrenin; gün sonu ekleme/eksiltmelerle, efor sarf etmeden yaklaşık 1,5 ayda %27 sistem getirisi" (not-kaynak) — gorsel-paket-37-gunluk-rebalancing-aktif-pasif.md; görselde "Aktif vs Pasif Fark -1.04%" ve "REBAL-" (görsel) — gorsel-paket-37/01-portfoy-kz-raporu.png
- Min-vol ve max-Sharpe portföyleri "üzerine düşeni yaptı ve yapıyor" (not-kaynak) — gorsel-paket-33-min-vol-max-sharpe-dey-bist100.md
- Yorum: Tansu kendi raporunda aktifin pasifin gerisinde kaldığını gizlemiyor; ama başarı ölçütü olarak toplam getiri ve BIST100'ü geçmeyi veriyor (risk ayarlı ölçü yok, kısa pencere).

Değerleme ve temel görüş:
- Ağırlık önerisi: çarpanlar %60, DCF %40 (not-kaynak) — gorsel-paket-25-degerleme-agirliklandirma.md
- Çarpan referansları: "SEÇİLEN DÖNEM : 2023/12", "KISA DÖNEM : 2023/12 dahil geriye 8 çeyrek (IQR k=1.5)", "UZUN DÖNEM : 2023/12 dahil geriye 36 çeyrek (IQR k=1.5)" (görsel) — gorsel-paket-27/01-asuzu-fk-referanslari-ve-hedefler.png
- ASUZU: "120 TL'ye En Yakın: 118.60 TL (2024-04-29)" (görsel) — gorsel-paket-27/02-asuzu-120-hedef-118-60-gerceklesen.jpg; değerleme 2023 bilançosundan sonra yapıldı, hisse Nisan 2024'te yaklaşık hesaplanan değere ulaştı (not-kaynak)
- "piyasa projeyi henüz fiyatlamadıysa" değer katkısı ile teknik analizi birleştirmeyi öneriyor (not-kaynak) — gorsel-paket-28-proje-bugunku-deger-ve-teknik-kapi.md
- Yorum: Tansu değerlemede üç referansı (sektör, kısa, uzun geçmiş) ayrı gösterip aykırı değeri IQR ile temizliyor; sonuç olarak tek hedef değil aralık (91,33 / 177,61 / 120,53). Hisse fiyatını bilançodan sonra "değerine yaklaşan" bir şey olarak anlatıyor. Teknik analiz ile değerleme birleştirme önerisi var ama kural yok.
- Tek örnekle ex-ante iddia: ASUZU hedef 120, gerçekleşen en yakın 118,60 (seçilmiş tek örnek).

Tekrar eden ilkeler (bu parçada):
- Yorum: (1) Çoklu çakışma (confluence) aranır; (2) bölge/talep merkezi (distal-proximal); (3) tarama sonra tek tek grafik; (4) hedef merdiveni; (5) volatilite yönsüz; (6) kendi aracının hatasını ve olumsuz sonucunu raporlama (paket 07 "ESKİ / script'teki", paket 37 "REBAL-").
<!--BAKIS-->
