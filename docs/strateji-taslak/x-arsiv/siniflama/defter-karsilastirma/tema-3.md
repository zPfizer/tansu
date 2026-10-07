# TEMA 3: Teyit, giriş, çıkış, boyut-risk: defter öneri belgesi

Girdi: `tema-3.jsonl` (228 satır: çeşitlendirir 134, genişletir 77, çelişir 11, yeni 6). Rol dağılımı: teyit 114, giriş 82, çıkış 20, boyut-risk 12.
Defter: `defter-fikir.txt`, `defter-1..4.md` (kayıtlar 2026-08-27 ile 2026-09-06 arası).
Kural: her cümle satırın `kanit` ya da `katki` alanına dayanır. "(görsel doğrulandı)" notu, bu belge için görseli Read ile açtığımı gösterir.
"DEFTER OKUMA HATASI" etiketli satır tema-3'te yok (bkz. Bölüm 4.2).

---

## 1. Yeni yöntem aileleri

### 1.A Defterde ne adı ne amacı olanlar ("yeni")

#### Aile 1: Avellaneda–Stoikov piyasa yapıcı modeli ve MA5 adil değer sapması
- Ne yapar: envantere göre kotasyonu kaydırır. Uyarlamada 5 günlük ortalamayı adil değer sayar; prim %3'ü aşınca short açar.
- Parametreler: r(t) = S_t − q·γ·σ²·(T−t); bid = r(t) − δ, ask = r(t) + δ; δ = (1/γ)·ln(1 + γ/k); γ, k, σ değeri yok. Uyarlama: true = MA5; sapma = (Kapanış − True)/True; sapma > %3 → short; fiyat adil değerin %1 altına inince kapat.
- Kaynak: 1911734132360552515 (2025-04-14, yeni), 1911789788019019979 (2025-04-14, çeşitlendirir R156/R053).
- Vurgu: yok.
- Olgunluk: uyarlama tam; ana model çekirdek (parametre değeri yok).

#### Aile 2: Rolling kırılım puanı ve 5 günlük toplam rejim etiketi (BULL/BEAR)
- Ne yapar: her gün rolling en yükseği aşan +, en düşüğün altına inen − puan alır. 5 günlük toplam rejim etiketini verir.
- Parametreler: 5 günlük toplam ≥ +3 → BULL; ≤ −4 → BEAR; arası nötr, kırılımı bekle. Rolling pencere yazılı değil. Görselde +3 ve −4 kesikli çizgi (satırda doğrulandı).
- Kaynak: 2042901081785557425 (2026-04-11, yeni). İlgili: 2042948983744557423 (2026-04-11): "NH/NL ve BULL etiketli" ikinci sistem, 200 günlük direnç kırılımıyla birlikte. Bağ belirsiz.
- Vurgu: 2042948983744557423: "İki sistemi birleştirince fark yaratıyor gerçekten."
- Olgunluk: çekirdek (rolling pencere yok).

#### Aile 3: Aracı kurum tavsiyesine ters pozisyon (kontraryan)
- Ne yapar: aracı kurum long tavsiyesi verince short açar.
- Parametreler: yok (süre, çıkış yok).
- Kaynak: 1824107507289080120 (2024-08-15, yeni).
- Vurgu: "25 yıllık tecrübe ile sabittir".
- Olgunluk: fikir.

#### Aile 4: Takvim ve saat filtresi
- Ne yapar: en kötü getirili günde işleme girmez; gün içinde sabah penceresinde al-sat yapar.
- Parametreler: XU100 son 1 yıl gün ortalaması Pzt ≈ −0,0052, Salı ≈ −0,0001, Çrş ≈ −0,0033, Prş ≈ 0,0086, Cuma ≈ 0,0016 (görselden, satırda). Gün içi: "saat 11 e kadar alıp satmalı".
- Kaynak: 1891208151497613761 (2025-02-16, çeşitlendirir R183), 1925060221661057436 (2025-05-21, yeni).
- Vurgu: 1891208151497613761: "haftanın kötü getirisi salı günü idi, işleme girmezdik, o gün şimdi pazartesi".
- Olgunluk: haftanın günü tam; saat penceresi fikir.

#### Aile 5: Para giriş hızı
- Ne yapar: para giriş hızı yavaşlarsa tereddüt eder; çıkış hızı artarsa fiyat güçlü olsa da temkinli olur ya da çıkar.
- Parametreler: yok (pencere, eşik yok).
- Kaynak: 2096257686266343893 (2026-09-05, yeni).
- Vurgu: "Para girişi kadar para giriş hızı da önemlidir."
- Olgunluk: fikir.

#### Aile 6: Opsiyonla koruma ve VaR → hedge zinciri
- Ne yapar: vadeye göre maksimum kaybı (VaR) ölçer; limit aşılırsa put alır ya da ters korelasyonlu hisse tutar.
- Parametreler: put için kullanım fiyatı, vade, miktar yok. VaR zinciri ve sayıları Bölüm 2 R053'te.
- Kaynak: 1734957210545844544 (2023-12-13, yeni), 1878086552548442457 (2025-01-11, çeşitlendirir R053/R030).
- Vurgu: yok.
- Olgunluk: çekirdek.

### 1.B Adı defterde olmayan türevler (çeşitlendirir, yontem_defterde = yok)

#### Aile 7: Golden Cross / Death Cross (EMA50 / EMA200)
- Ne yapar: EMA50 EMA200'ü yukarı keserse AL, aşağı keserse SAT ya da pozisyon kapat. Ön tarama: fiyat son gün EMA200'ü yukarı keser, EMA50 henüz altta.
- Parametreler: günlük; EMA50, EMA200. GLCVY tablosu: 2022-08-22 Buy 15.71; 2023-05-18 Sell 18.55; 2023-06-07 Buy 25.66; 2024-09-18 Sell 37.98; 2024-10-02 Buy 41.52 (görsel doğrulandı). AKCNS: fiyat 160.30, EMA50 154.18, EMA200 155.02.
- Kaynak (Golden): 1842243313891516527 (2024-10-04), 1842246990521925981 (2024-10-04), 1842522266971574456 (2024-10-05), 1842524448802365487 (2024-10-05), 1847334466227724450 (2024-10-18); 1847338202924744724 (2024-10-18), 1847355900014858452 (2024-10-18), 1848805888355652024 (2024-10-22), 1851722448305074497 (2024-10-30), 1908440134174843000 (2025-04-05); 1914402661446672687 (2025-04-21), 1929962891026850004 (2025-06-03), 1943065073590899051 (2025-07-09), 1978879623648739789 (2025-10-16). Death: 1911462470763360258 (2025-04-13), 1912230255349158303 (2025-04-15), 1923093966376816754 (2025-05-15), 1943065231695188060 (2025-07-09).
- Vurgu: "50EMA/200EMA Golden Cross arıyorum" (1842243313891516527); "Son gün yaşananlar sizi yanıltmasın dikkatli olun" (1842524448802365487). Death Cross "tek başına yetmez" (1911462470763360258).
- Olgunluk: tam. 18 gönderi.

#### Aile 8: Vegas tüneli (EMA 12 / 144 / 169)
- Ne yapar: EMA12 (ya da fiyat) EMA144–EMA169 tünelini yukarı keserse long; tünel altında −1 (short) pozisyon.
- Parametreler: günlük; EMA12, EMA144, EMA169; kâr al ATR ile (çarpan yok).
- Kaynak: 1827337231972843583, 1827340050247376915, 1827341150908543159, 1827342674690449781 (hepsi 2024-08-24); 1848385592771424616 (2024-10-21), 1848803496893558928 (2024-10-22), 1851726487855972606 (2024-10-30), 1852066618488275443 (2024-10-31).
- Vurgu: "VE ilk göz ağrımız VEGAS" (1851726487855972606).
- Olgunluk: tam (giriş); çıkış çekirdek (ATR çarpanı yok).

#### Aile 9: SuperTrend birleşimleri
- Ne yapar: SuperTrend yönünü filtre, başka bir göstergeyi tetik yapar.
- Parametreler: (a) son gün EMA5 EMA20'yi yukarı keser VE SuperTrend bullish; en sağlamı: SuperTrend zaten bullish, son gün dönmemiş. (b) 60 dk: AL = RSI > 55 ve bullish; SAT = RSI < 45 ve bearish; nötr 50 (görselden, satırda). (c) KAMA (10, 2, 30) + SuperTrend. ST periyodu ve çarpanı yok.
- Kaynak: 1840000258094354552 (2024-09-28), 1851991078661976137 (2024-10-31), 1852057966960349695 (2024-10-31), 1852060552413221135 (2024-10-31), 1860422703150149949 (2024-11-23); 1853053450319286714 (2024-11-03), 1848098444537119119 (2024-10-20, MOST + ST, fikir).
- Vurgu: "Bence daha sağlam sinyal bu." (1852060552413221135); "Altını çizeyim her iki koşulda son gün sağlanıyor." (1852057966960349695).
- Olgunluk: (a) ve (b) çekirdek (ST parametresi yok); (c) çekirdek.

#### Aile 10: MOST / OTT / VAR formülleri (Matriks dili)
- Ne yapar: ortalama ile iz süren eşik çizgisinin kesişiminden AL/SAT üretir; parametreyi optimizasyonla seçer.
- Parametreler: AL CROSS(MOV(C,OPT1,E),MOST(C,OPT1,OPT2)), SAT tersi; OPT1 2–30 adım 1 (varsayılan 3), OPT2 0,5–5 adım 0,5 (varsayılan 2), 290 test; ikinci sürüm OPT1 2–100, OPT2 0.5–5 adım 0.1. Anıl Özekşi sürümü: if(MOV(C,opt1,E)>MOST(C,opt1,opt2)) ise opt3/opt4, değilse opt5/opt6 kesişimi; OPT1 15–34, OPT2 2–6, OPT3 2–15, OPT4 0.5–5, OPT5 2–15, OPT6 0.5–5. RSI üstüne: CROSS(MOV(RSI(C,14)+1000,3,e),MOST(RSI(C,14)+1000,3,2)). RSI-VAR: Al Cross(Mov(RSI(C,14),5,VAR),50), Sat tersi. VAR-VAR: Cross(MOV(C,opt1,VAR),MOV(C,opt2,VAR)); 60DK; OPT1 5–15, OPT2 16–50, 385 test; DOAS overall ≈ %1150, data ≈ %350.
- Kaynak: 1782497478056558995 (2024-04-22), 1783412420716761320 (2024-04-25), 1779421690071490990 (2024-04-14), 1843751550503768113 (2024-10-08), 1783371645224149075 (2024-04-25); 1786779842530226293 (2024-05-04), 1784690075059585046 (2024-04-28), 1790974588156821797 (2024-05-16, OTT HHV/LLV beş eşik, opt değeri yok).
- Vurgu: 1783412420716761320: sinyal ve overall hisseye ve periyoda göre değişir, test edilmeli.
- Olgunluk: tam (formül ve aralık var); OTT sürümü çekirdek.

#### Aile 11: MACDAS / MACDASTRIGGER kesişimi
- Ne yapar: MACDAS ile tetik çizgisinin kesişimi AL/SAT verir.
- Parametreler: AL = CROSS(MACDAS(OPT1,OPT2,OPT3), MACDASTRIGGER(OPT1,OPT2,OPT3)), SAT tersi; OPT1 13–55, OPT2 8–15, OPT3 3–13, adım 1 (görselden, satırda).
- Kaynak: 1778777162587279414 (2024-04-12), 1778740373495353562 (2024-04-12).
- Vurgu: "her hissede aynı sonuç vermez" (katki).
- Olgunluk: tam (aralık); optimum değer yok.

#### Aile 12: RoC + ADX/ADXR + OBV ("favori sistem")
- Ne yapar: RoC sıfır kesişi pusuya yatırır; ADX'in ADXR'yi kesmesi girişi verir; OBV para akışını teyit eder.
- Parametreler: RoC50 son gün 0'ı yukarı keser; ADX(14) > ADXR(14) (önceden kesmiş ve üstte ya da son gün kesmiş); kesişim 20 üstünde tercih; OBV SMA20'yi yukarı keser. Çıkış: ADX ADXR'yi aşağı keser. Ek: RoC9 0 yukarı kesişi = Al; RoC 9/20/50 ve 9/50 kesişim panelleri (koşul tanımsız).
- Kaynak: 1841955633047670978 (2024-10-03), 1841222101497246009 (2024-10-01), 1842064079826936219 (2024-10-04), 1841228866234601958 (2024-10-01), 1841235974430273798 (2024-10-01); 1841568003709694130 (2024-10-02), 1842218572157759579 (2024-10-04), 1840811430800420929 (2024-09-30), 1840799431626510719 (2024-09-30), 1840801601784545478 (2024-09-30).
- Vurgu: "Favori sistemim" (1841955633047670978).
- Olgunluk: tam.

#### Aile 13: RSI'ya Fibonacci (144 gün)
- Ne yapar: Fibonacci seviyelerini fiyata değil RSI'ya çizer; RSI'nın 0.618/0.786'dan dönüşünü giriş, 0.382'den reddini uyarı sayar.
- Parametreler: pencere 144 gün; seviye = maxRSI − oran × (maxRSI − minRSI). Giriş: RSI seviyeden döner ve RSI(t) > RSI(t−1); teyit çekiç / yutan boğa / sabah yıldızı ve fiyat > 50 günlük ortalama; stop son düşüğün %2-3 altı. 0.786 sürümü: 1-2 mum teyidi; çıkış RSI 50-60 bandı ya da önceki direnç. XU100 örneği: 0.000 79.4, 0.236 68.4, 0.382 61.6, 0.500 56.1, 0.618 50.7, 0.786 42.9, 1.000 32.9 (görsel doğrulandı; 79.4 − 0.618 × 46.5 = 50.66).
- Kaynak: 1977450129008251116 (2025-10-12), 1912151798992814185 (2025-04-15), 1986917436310909146 (2025-11-07), 1911906987341910274 (2025-04-14), 1912933957592834220 (2025-04-17); 1925626094935236883 (2025-05-22), 1986826807287349423 (2025-11-07), 1840024620834959504 (2024-09-28, 1.618 extension), 1840032038734454942 (2024-09-28, haftalık 1.618).
- Vurgu: "RSI 786 dönüşü mum formasyonları daha ne olsun" (1912933957592834220).
- Olgunluk: tam (1977450129008251116); 1.618 sürümü fikir.

#### Aile 14: Bollinger orta bant + RSI 50
- Ne yapar: fiyat BB orta bandını yukarı keserken RSI 50'yi yukarı keserse AL; orta bandı aşağı keserse SAT. Alt/üst bant kullanmaz.
- Parametreler: ilk bar orta bandın üstünde kapanır ve aynı anda RSI 50'yi geçer; stop ATR (çarpan yok); pencere "optimize" (yazılı değil); saatlik dilimde iyi sonuç. Sıkışma türevi: BB bant genişliği sıkışması + RSI 50 yukarı kesişi.
- Kaynak: 1774426858567643590 (2024-03-31), 1782881410174365714 (2024-04-23), 1782493259874365466 (2024-04-22), 1783146802574741608 (2024-04-24), 1839057936141705262 (2024-09-25).
- Vurgu: "BB sıkışması ve RSI 50'nin yukarı kesilmesi benim sevdiğim bir strateji." (1839057936141705262); walk-forward ve Monte Carlo yapmadan paylaşmama (1782493259874365466).
- Olgunluk: çekirdek (BB periyodu yok).

#### Aile 15: Bollinger–Keltner ve Keltner rejim stratejisi
- Ne yapar: BB Keltner içine girince sıkışma sayar, KC dışına çıkışta yön alır. Keltner'i trendde kırılım, yatayda ortalamaya dönüş için kullanır.
- Parametreler: squeeze: BB KC içinde → fiyat KC dışına yukarı = al, aşağı = sat; stop KC orta çizgisi ya da BB karşı bandı; teyit RSI ya da hacim artışı. Rejim: trendde kapanış > KC üst bant → al; yatayda alt bandı yukarı kesince al, üst bandı aşağı kesince sat. Varyant: BB KC dışında, alt BB'ye dokunup sekme, ikinci mum zıt renk, ADX yükselir, RSI 50'yi keser. 5 dk: fiyat Keltner bandını yukarı keserse long. Periyotlar yok.
- Kaynak: 1912246536811008424 (2025-04-15), 1852476829543587877 (2024-11-01), 1783228274077839740 (2024-04-24), 1852457611288789277 (2024-11-01).
- Vurgu: "trend varken üst bandın üstünde kapanışlar al demiştik" (1852476829543587877).
- Olgunluk: çekirdek (periyot ve çarpan yok).

#### Aile 16: Uyumsuzluk türevleri (MACD n-gün taraması, negatif uyumsuzluk, CCI, Tasuki)
- Ne yapar: MACD ve fiyatı n gün/hafta önceki değerle karşılaştırır; negatif uyumsuzlukta long'a girmez; CCI ve mum formasyonlarıyla teyit arar.
- Parametreler: MACD karşılaştırma penceresi 3/5/10 gün (günlük), 4 hafta (haftalık, son 2–3 haftada sinyal) + sinyal kesişimi. Negatif uyumsuzluk: fiyat yükselen zirve, RSI14 alçalan zirve → long yok; RoC50 ile örnek. CCI pozitif uyumsuzluk + CDLBELTHOLD + MACD kesişimi + RSI düşen kırılımı + hacim + T3 kesişimi. Tasuki Gap: RSI pozitif uyumsuzluktan sonra momentum devam teyidi.
- Kaynak: 1839078126015438978 (2024-09-25), 1840349130532544681 (2024-09-29), 1840350261803470950 (2024-09-29), 1843752733347852648 (2024-10-08), 1843754494062145990 (2024-10-08); 1761494782986039489 (2024-02-24), 1841215716239802489 (2024-10-01), 1842576684501086648 (2024-10-05), 1995931145499017316 (2025-12-02), 1910750634363801784 (2025-04-11).
- Vurgu: "şu negatif uyumsuzlukları göre göre girmeyin hisselere lütfen" (1842576684501086648).
- Olgunluk: çekirdek. Not: MACD taramasının tanımı gerçek uyumsuzluğu ayırmıyor (Bölüm 4).

#### Aile 17: Çoklu Parabolic SAR + regresyon kanalı
- Ne yapar: üç SAR (normal, hızlı, yavaş) ve ortalamaları fiyatın altına geçince girer; regresyon kanalı eğrisini risk algısına göre seçer.
- Parametreler: PSAR noktaları fiyat altında; SAR ortalaması her şartta fiyat altında; LRC üst/orta/alt; ADX/ADXR paneli 25 kesik çizgi; PSAR + ADX/ADXR + 10 bar ortalama hacim (eşik yok). SAR parametreleri yok.
- Kaynak: 1951039466891780200 (2025-07-31), 1951615287326814530 (2025-08-02), 1951766879372222813 (2025-08-02), 1982687024344949140 (2025-10-27), 1864260274355626306 (2024-12-04); 1951019812848804159 (2025-07-31), 1951742859704713570 (2025-08-02).
- Vurgu: "temel felsefe psarların aşağıda olması gerekliliği" (1951615287326814530).
- Olgunluk: çekirdek.

#### Aile 18: Diğer iz süren trend çizgileri (HiLo, T3, SR1/YSL)
- Ne yapar: fiyat çizgiyi kesince al/sat verir.
- Parametreler: HiLo periyodu yok; T3 parametresi yok; SR1 (SARI-10), YSL (YEŞİL-6), hesap türü yok.
- Kaynak: 1877605823737729513 (2025-01-10), 1910726514305278218 (2025-04-11), 1987956410379104378 (2025-11-10).
- Vurgu: yok.
- Olgunluk: fikir.

#### Aile 19: Opsiyon duvarı, açık pozisyon ve IV–Delta–Takas matrisi
- Ne yapar: call duvarını direnç/mıknatıs, put duvarını alt sınır sayar; duvar yıkılırsa momentum squeeze bekler. IV, delta ve takas yönünü 8 hücreli matriste okur.
- Parametreler: altın call duvarı 4251 $; GC=F 4254.9, call 4467, put 4042 (görselden, satırda); duvar her akşam yeniden hesaplanır; 4251 üstünde tutunma = duvar yukarı çekildi (süre yok). Delta hedge: 100 call × delta 0,6 = −60 delta → 60 hisse al; IV = Black-Scholes, Newton-Raphson. IV ≫ tarihi volatilite → opsiyon sat. Matris eşiği yok.
- Kaynak: 2083449552279937370 (2026-08-01), 2083847741269004563 (2026-08-02), 2084870597385818320 (2026-08-05), 2085043984414409205 (2026-08-05), 2085278210728599696 (2026-08-06); 1994748031900492128 (2025-11-29), 1978358665145979337 (2025-10-15), 1978358660934795342 (2025-10-15), 1936705102133301277 (2025-06-22).
- Vurgu: "Sağlam yıkarsa momentum squeeze gündeme gelir ivme hız kazanır" (2085043984414409205).
- Olgunluk: delta hedge örneği tam; duvar kırılımı çekirdek (kırılım ölçütü yok).

#### Aile 20: AKD (Aracı Kurum Dağılımı) ve takas daralması
- Ne yapar: büyük kurumlar toplarken küçükler satıyorsa fırsat, tersi risk sayar.
- Parametreler: TERA YATIRIM 22–27.05.2025 net 3.033.904 lot, net alımın %76'sı, maliyet 137,46 (görselden, satırda). Yatay bantta birikim = yükseliş habercisi; zirve sonrası aynı kurumlar satıyorsa giriş yok. Takas: aynı kurumun üst üste net alımı, net alıcının son 10 günü, takas her gün el değiştiriyorsa tuzak.
- Kaynak: 1938970182380134893 (2025-06-28, genişletir R237, yontem yok), 1938955085934944638 (2025-06-28), 1938989947387576647 (2025-06-28), 1939258295551701476 (2025-06-29), 1964331893341503858 (2025-09-06).
- Vurgu: yok (alıntı düzeyinde).
- Olgunluk: çekirdek (eşik yok).

#### Aile 21: Kelly ve martingale ile boyutlama
- Ne yapar: trade sermayesi oranını Kelly ya da fractional Kelly ile belirler. Yükselen trendde yüksek betalı hisselerde martingale ile pozisyon artırır.
- Parametreler: formül ve oran yok; %51-%49 kazanç/kayıpta bile uzun vadede kayıp iddiası; beta basit regresyonla.
- Kaynak: 1874426039340007571 (2025-01-01), 1874425159224000594 (2025-01-01), 1874435738873504182 (2025-01-01), 1876964680947696067 (2025-01-08).
- Vurgu: "limitim genelde KC'dır benim" (1874426039340007571).
- Olgunluk: fikir (Kelly), çekirdek (martingale).

#### Aile 22: Range Breakout (N gün/hafta zirvesi) ve kanal orta bandı
- Ne yapar: son N dönem zirvesini kapanışla aşan hisseyi seçer, mum formasyonuyla teyit eder.
- Parametreler: range_high/low = son 60 gün; sinyal: son günün yüksek VE kapanışı > 60G zirve; teyit talib bullish formasyon (CDLBELTHOLD); yfinance 01.01.2024–24.05.2025; sonraki gün hacim/fiyat teyidi. Diğer: range = 30 (birim yok). Haftalık: haftalık kapanış ve tepe > önceki X hafta (X yok) + günlük MACD, EMA sırası, RSI/Stoch aşırı alımda değil, OBV yukarı. Kanal orta bandı kırılımı + CDLCLOSINGMARUBOZU + momentum sistemi.
- Kaynak: 1926353549723590759 (2025-05-24), 1925633169694277851 (2025-05-22), 1929184555816419717 (2025-06-01), 1919059738450415964 (2025-05-04), 1914180392946463140 (2025-04-21).
- Vurgu: 1914180392946463140: "yeni yazdığım bir sisteme göre".
- Olgunluk: 60G sürümü tam; diğerleri çekirdek.

#### Aile 23: Düşen kanal kırılım taraması (N bar)
- Ne yapar: son gün kapanışla düşen kanalın üst bandını kıran hisseyi raporlar.
- Parametreler: kanal 60 / 90 / 150 bar; çıktı alanları: kırılım tarihi ve fiyatı, direnç, eğim (ör. 30.22, −0.248; 2257.17, −10.576); kırılımdan 1 gün sonra raporlanır; paneller RSI, MACD Histogram, +DI/−DI, hacim MA21. 60 bar sürümünde: kırılım farkı +5.85%, üst eğim −0.627%/bar, alt eğim −0.542%/bar, temas 3/3, durum "RETEST + TUTUNDU".
- Kaynak: 1987233906827903088 (2025-11-08), 2011135212382761149 (2026-01-13), 2016954643394216029 (2026-01-29), 2016967838120964296 (2026-01-29), 2023815727309091176 (2026-02-17); 2097063290224431474 (2026-09-07, R247).
- Vurgu: marubozu hacimle teyit edilmeli (1987233906827903088).
- Olgunluk: çekirdek (çıktı alanları var; kanal hesabı yazılı değil).

#### Aile 24: 200 günlük direnç kırılımı
- Ne yapar: 200 günlük direnç seviyesini aşan hisseyi işaretler.
- Parametreler: PRZMA direnç 16.80, son 17.70 (+%5.4); CRFSA direnç 133.00, son 133.10 (+%0.1); EMA 5 ve 13 (görselden, satırda). Direnç tanımı yazılı değil.
- Kaynak: 2045418595421659641 (2026-04-18), 2042948983744557423 (2026-04-11).
- Vurgu: "İki sistemi birleştirince fark yaratıyor gerçekten." (2042948983744557423).
- Olgunluk: çekirdek.

#### Aile 25: Dynamic Swing VWAP
- Ne yapar: VWAP'ı swing noktalarından (HH/HL/LH/LL) yeniden başlatır; fiyatın VWAP'ı yukarı kesişini sinyal sayar.
- Parametreler: haftalık; kesişim haftası; VWAP short ve long iki seri; +DI/−DI. Sert yükselişler HL kırılımından sonra.
- Kaynak: 1987305332721524852 (2025-11-08), 1987107314193649692 (2025-11-08).
- Vurgu: "Dikkatimi çeken sert yükselişler hep HL kırılımından sonra gelmiş."
- Olgunluk: çekirdek.

#### Aile 26: EMA26 ATR bantları
- Ne yapar: EMA26 ± k×ATR bantlarında iğne reddini ve bant üstü kapanışı alım sayar.
- Parametreler: AL −3R: gün içi düşük < EMA26 − 3ATR ve kapanış bandın üstünde. AL −2O: −2ATR testi + iki gün üst üste bant üstü kapanış. MACD histogram onayı; ek filtre hacim, EMA13 > EMA26, RSI < 30, BIST100 trendi. ATR periyodu yok.
- Kaynak: 1978494634121703760 (2025-10-15, çeşitlendirir R053/R184).
- Vurgu: yok.
- Olgunluk: tam (ATR periyodu hariç).

#### Aile 27: İstatistiksel sapma: EWMA z-skoru ve çift EMA farkı
- Ne yapar: günlük getirinin EWMA ±2σ bandından taşmasını ters sinyal sayar. Çift EMA farkının açılmasını kâr realizasyonu uyarısı sayar.
- Parametreler: z > +2 → kâr satışı/ters pozisyon; z < −2 → dönüş alımı; bant daralırsa mean-reversion, genişlerse şok stratejisi; EWMA yarı ömrü yok. AVTUR 19.06 z > 2 → 20.06 satış. Çift EMA: k = 2/(n+1); ema1 = EMA5(fiyat); ema2 = EMA5(ema1); al ema1 > ema2, sat ema1 < ema2.
- Kaynak: 1936767147914485837 (2025-06-22), 1760725150406988034 (2024-02-22).
- Vurgu: yok.
- Olgunluk: EWMA tam (yarı ömür hariç); çift EMA çekirdek (koşulun ikinci kısmı görselde kesik).

#### Aile 28: Breakout + hacim çarpanı (Qullamaggie türevi)
- Ne yapar: kırılım gününde hacim, RSI, MACD ve MA dizilimini birlikte arar.
- Parametreler: hacim ≥ ortalamanın 2-3 katı; RSI > 60; MACD histogram pozitif ve artıyor; fiyat 20-50-200 MA'nın hepsinin üstünde; BB daralması ya da ATR düşüşü = konsolidasyon; kapanış kırılım seviyesinin üstünde (gün içi değil).
- Kaynak: 1979546907505545421 (2025-10-18, genişletir R124/R195/R082/R073, yontem yok).
- Vurgu: yok.
- Olgunluk: tam (ortalama hacim penceresi yok).

#### Aile 29: Under 30 Over 30: 1,5R break-even çıkışı
- Ne yapar: fiyat 1,5R lehte ilerledikten sonra giriş fiyatına dönerse gün sonunu beklemeden çıkar.
- Parametreler: R = başlangıç stop mesafesi; eşik 1,5R; çıkış = giriş fiyatı.
- Kaynak: 1992547498343161903 (2025-11-23, genişletir R233/R203, yontem yok).
- Vurgu: yok.
- Olgunluk: tam.

#### Aile 30: Kayıp telafi asimetrisi
- Ne yapar: kaybı geri almak için gereken kazancı hesaplar.
- Parametreler: telafi = 1/(1 − kayıp) − 1; %10 kayıp → %11,11.
- Kaynak: 1874416190443114907 (2025-01-01, genişletir R138, yontem yok).
- Vurgu: yok.
- Olgunluk: tam.

#### Aile 31: Mantıksal sinyal birleştirme (VEYA/VE)
- Ne yapar: üç dönüş sinyalinden birini ve bağımsız dördüncü sinyali birlikte ister.
- Parametreler: alım = (sinyal_1 ∨ sinyal_2 ∨ sinyal_3) ∧ sinyal_4; s1–s3 ortalama destekli dönüşler, s4 ayrı gösterge/ortalama.
- Kaynak: 1987494513825259932 (2025-11-09, genişletir R255/R230, yontem yok).
- Vurgu: yok.
- Olgunluk: çekirdek (s1–s4 tanımı yok).

#### Aile 32: Satış yürütme: Monte Carlo satış yolu karşılaştırması
- Ne yapar: büyük pozisyonu doğrusal ya da kuadratik hızla satma yollarını simülasyonla karşılaştırır.
- Parametreler: mu = 0 / 0.04 / −0.04; 10000 hisse. Sonuç: mu=0 en iyi fast quadratic 185.62 TRY (3.8 bp); mu=0.04 en iyi linear 716.37 (14.5 bp); mu=−0.04 en az zarar fast quadratic −67.12 (−1.4 bp); slow linear ≈ −25000 TRY (≈ −506 bp). Spread/impact parametresi yok.
- Kaynak: 1911720907514540232 (2025-04-14, çeşitlendirir R225).
- Vurgu: "En iyi satış stratejisi lineer mi, kuadratik mi?"
- Olgunluk: çekirdek.

#### Aile 33: Likidite: fon X-ray konsantrasyonu
- Ne yapar: fon konsantrasyonu ve AUM çıkışından taban/kilitlenme riskini ölçer; riskli hissede boyutu önceden küçültür.
- Parametreler: PUK örneği PASEU %11,64, KTLEV %10,21, DCTTR %8,17; ağırlık artışı DCTTR +6,95, PASEU +4,04, KTLEV +1,87 puan; eşik yok.
- Kaynak: 2095997339391414488 (2026-09-04, çeşitlendirir R225/R201/R252).
- Vurgu: "Likidite, iyi günde ne kadar hacim olduğu değil kötü günde ne kadar satış yapabildiğinizdir."
- Olgunluk: çekirdek.

### 1.C Tek gönderili türevler (kısa)

Grup 1:
- Aile 34: OBO başarısız boyun kırılımı ("2-Red") + 2ATR stop. Son 5 gün OBO boyun kırılımı; mum boyun üstünde kapanırsa long; giriş red mumu kapanışı ya da ertesi açılış; stop giriş − 2×ATR (örnek 14 gün); her kapanışta stop 2ATR mesafeyle yukarı. 1988278667571519700 (2025-11-11). Olgunluk: tam.
- Aile 35: Marubozu + hacim + ATR stop. Marubozu düşük hacim = sahte, yüksek hacim = dönüş; ATR bazlı stopla sürekli kâr alma; çarpan yok. 2044863959027925319 (2026-04-16). Olgunluk: çekirdek.
- Aile 36: Elliott Expanded Flat. C (25,16) korunur → küçük 1-2 → küçük 1 tepesi kırılır; 24,50 (A) altı ana sayım bozulur. 2094052769493582241 (2026-08-30). Olgunluk: çekirdek.
- Aile 37: Eşleşen dip mumu + Siyah Kuğu. Standart sapmayla tespit; ikisi birlikte bile yetmez; RSI(14), ADX(14), MACD teyidi şart. 1983272525116170488 (2025-10-28). Olgunluk: çekirdek.
- Aile 38: Gann fanı. 1/1, 2/1, 3/1, 4/1, 8/1 ile ayı piyasası teyidi; kırılırsa hedef 115 → 86. 1775957765980127737 (2024-04-04). Olgunluk: fikir.

Grup 2:
- Aile 39: Delta Volume / Bull-Bear oranı. Mum başına boğa/ayı hacim yüzdesi ve Δ; örnek boğa %91, Δ 0.42M. 1950286434620862673 (2025-07-29). Olgunluk: fikir.
- Aile 40: ATR Directional Change tepe/dip + gün içi %3-5 kâr al. ATR çarpanı ve pencere yok. 1925591759523840425 (2025-05-22). Olgunluk: fikir.
- Aile 41: Kapanışta al, +%1'de sat. Tarama ölçütü yok. 1952746861439172671 (2025-08-05). Olgunluk: fikir.
- Aile 42: Arbitraj sinyali + destek zamanlaması. Sinyal gelince destek seviyesine kadar bekle; karşı-olgu %20 kâr 12 saatte. 1860897937829794166 (2024-11-25). Olgunluk: fikir.
- Aile 43: Conflict filtresi. Momentum squeeze filtresine ek ayrı filtre gerekir; adı ve kuralı yok. 2045489485996019907 (2026-04-18). Olgunluk: fikir.

Grup 3:
- Aile 44: RSI düşen trend kırılımı + marubozu (çeşitlendirir R008/R039). Son gün RSI düşen tepe çizgisini yukarı keser ve aynı gün marubozu mum oluşur. Kırılım seviyesi gönderiler arasında farklı: ~37-38 "30'un üstünde" (1911384911908388875, 2025-04-13; CMTAS 12 günde %57) ve ~37 (1909769680841028023, 2025-04-09); üçüncü sürümde ek şart RSI > 50 (1909715584134099312, 2025-04-08). Parametreler için bkz. R008 (lookback 50, extend 40, min_gap 20). Olgunluk: çekirdek.

---

## 2. Genişletmeler (R kaydı başına)

İşaret: **[AÇIK SORU CEVABI]** defterin açık bıraktığı bir soruyu cevaplayan gönderiyi gösterir.

### 2.1 Boyut-risk ve çıkış

**R184** (2026-08-28): defterde "Göze Alınan Kayıp / Hisse Volatilitesi = Lot"; "ATR mi 2×ATR mı" belirsiz; acil stop 2ATR. → 2005227814875021373 (2025-12-28): soru "Formuldeki hisse volatilitesi 1 ATR degeri değil mi?", cevap "2 Atr". **[AÇIK SORU CEVABI]** Destek: video 1999481868106826013 (2025-12-12): "Sistem diyor ki bunun iki katını al"; %1 risk; 100.000 $ → 1.000 $; 2 ATR = 14.30 $ → 70 hisse; gün sonu stop 250 günlük ortalama altı kapanış.

**R239** (2026-08-28): defterde giriş + 1,5 × ATR'de iz süren moda geç; sonra önceki gün düşüğü altı kapanışta %50 sat. → 2022431570012106899 (2026-02-13) ve 2045421697814126693 (2026-04-18): sabit ATR(14) merdiveni. hedef_n = giriş + n × ATR(14), n = 1..20; başlangıç stop = giriş − 1,5 × ATR; n ATR'ye ulaşınca stop (n−2) ATR'ye; 3 ATR'de %50 satış; stop yalnız yukarı. ASTOR: 155,00 − 1,5 × 7,56 = 143,66; 4 ATR'de %22,00. YAPRK: 15,05 − 1,5 × 1,27 ≈ 13,15; başlangıç risk %12,62 (iki görsel doğrulandı). Bu satırlar "çelişir" etiketli; bkz. Bölüm 3, Ç6.

**R233** (2026-08-28): defterde RSI(14) 30 yukarı kesiş girişi; RSI 70 reddinde %50; önceki gün düşüğü altı kapanışta kalan %50; TS oranı belirsiz. → gönderiler:
- 1990003872023130607 (2025-11-16): RSI30 kesişiminden sonra ilk direnç genelde SMA50; takip için RSI50 reddi ve/veya SMA50 reddi (red tanımı yok).
- 1991558168149987328 (2025-11-20): ilk temas SMA50 ya da RSI50.
- 1991721699922870638 (2025-11-21): %50 satış tetikleri RSI 50 reddi, SMA 50 reddi, 1,5 ATR kârdayken önceki gün düşüğü altı kapanış; "Bu 3 senaryodan herhangi ikisi gerçekleşirse işlemin tamamını kapatın."
- 1992547498343161903 (2025-11-23): 1,5R lehte ilerleme sonrası girişe dönüşte derhal çık. **[AÇIK SORU CEVABI, kısmen]** TS oranı yerine break-even kuralı verir.

**R053 (VaR kısmı)** (2026-08-27): defterde VaR %95, risk limiti. → 1878086550665175243 (2025-01-11): %99 güven, 100.000 TL, ufuk 1 gün / 1 hafta / 1 ay / 3 ay, son 10 yıl; görselden ≈ 5.900 / 13.400 / 28.400 / 52.000 TL; yöntem yazılı değil. 1878089934268965110 (2025-01-11): günlük kabul 5.000 TL; VaR aşarsa hedge.

**R138** (defterde A/D > EMA, nakde geçiş): → 1874416190443114907 (2025-01-01): telafi kazancı = 1/(1 − kayıp) − 1.

**R128** (defterde "fiyat ortalamalardan çok uzaklaştığında" soğuma, sayı yok): → 1963273280581751113 (2025-09-03): 13 EMA üstünde 1 ATR, sonra 2 ATR kademeli = sağlıklı; ani 3 ATR spike = kademeli kâr al, yeni alım yok; spike sonrası 13 EMA'da tutunma = devam; EMA altına sert dönüş = tepe. ATR periyodu ve satış oranı yok. **[AÇIK SORU CEVABI]** Uzaklık ölçüsü ATR katı.

**R189** (defterde momentum ön elemesi): → 1993448157163012287 (2025-11-25): 5-6 strateji ile teyit (tanımsız). 2090360295491318080 (2026-08-20): 552.14 üstünde birkaç hacimli bar kapanışı → hedef en yakın supply 645-708; tersi → 431.45; bar sayısı yok.

**R193** (defterde Elliott 5. dalga hedefi var, "hedef nasıl hesaplanıyor yazmıyor"): → 1983565377532572092 (2025-10-29): "5. Dalga Hedef (W3*0.618): 18.63 TL"; gerçekleşen 18.13; başlangıç noktası yazılı değil. **[AÇIK SORU CEVABI, kısmen]** 1978152557945000041 (2025-10-14): hedef = üçüncü itki sonu + C dalgası × 0,618 ("gibi").

**R203** (defterde TP formülleri D + (C − D) × oran): → 1870475673585795531 (2024-12-21): çalışılmış örnek D 9765.10, CD 492.30; 0.618 → 10069.34; C 10257.40; dip hedefi 9644.60. Hesap tutuyor (9765.10 + 0.618 × 492.30 = 10069.34).

**R199** (defterde W2 alımı, hedef 1 eski tepe): → 1986859079348924623 (2025-11-07): c > 0; 1. tepede kısmi satış; 1. tepe güçlü mumla kırılınca satılan kısmı geri al ya da ekle; oran yok.

### 2.2 Giriş

**R060** (defterde dönen varlık / KVB): → 1946652258260635954 (2025-07-19): destekten tepki, RSI 30-40 bandından yukarı dönüş, hacimli direnç kırılımı, fiyat SMA/EMA50'yi yukarı keser; stop yatırımın %3-5'i ya da destek altı; ASELS cari oran 2, faaliyet kâr marjı %18, borç oranı %35.

**R108** (defterde Weinstein evreleri, "X haftalık", sayı yok): → 1945064189082599687 (2025-07-15): 2. aşama fiyat > 150 ve 200 günlük ortalama; 150 g > 200 g; 200 g yukarı dönmüş; yükseliş günü hacmi güçlü; dipten %25-30 (bazen %80) yukarıda olabilir. **[AÇIK SORU CEVABI]** Ortalama süresi 150/200 gün.

**R126** (defterde DMI, delta): → 1853909406553137314 ve 1853910926581227970 (2024-11-05): ADX 14, ±DI 14, 20 ve 25 eşik çizgileri. 1853912926874214428 (2024-11-05): "Sİnyal kesişimden geliyor" (+DI/−DI).

**R198** (defterde talep bölgesi agresif/güvenli giriş): → 2093739858845917333 (2026-08-29): dip 1–2 bar korunur ve toparlanma gelirse erken giriş; toparlanma tanımsız.

**R206** (defterde Fibo 0.618 + H4 OB): → 2000153302927806546 (2025-12-14): 3 adım: günlükte Fibo 0.5-0.618; 4S/1S'te zone içinde Order Block, Breaker Block ya da doldurulmamış imbalance; emir 0.618 ile 4S OB kesişimine; örnek 100 TL'de 0.618, 98 TL'de 4S OB.

**R210** (defterde SMA20 > SMA50, Heikin Ashi): → 1771668829900357977 (2024-03-23): EMA20 EMA50 üstüne çıkar ve fiyat EMA50 üstünde 2 gün kapanış. 1841922080541180029 (2024-10-03): MA20 > MA50, ikisi de yükselir, mesafe büyür; geri çekilme en fazla MA20–MA50 arası. 1841923620714774620 (2024-10-03): kod yalnız SMA20/SMA50 hesaplar.

**R212** (defterde 250SMA giriş bileşeni): → 1989651383092744703 (2025-11-15): kapanış SMA200 ya da SMA250 altında, ertesi gün üstünde + momentum; ALBRK 07.11.2024 kapanış 5.11, MAV200 5.1457, MAV250 4.887.

**R234** (defterde lojistik regresyon, %55 doğruluk): → 1775632307669385380 (2024-04-03): sinyal 0–1 olasılık; kesikli "trading level" ≈ 0,5; yukarı kesişte yükseliş; son sinyal 0.10.

**R255** (defterde sadeleştirme): → 1987494513825259932 (Aile 31).

**R031** (defterde VRP = IV − RV; eşik 0,025 / −0,005): → 1925556979520487602 (2025-05-22): HV 10/20/30 gün; IVR ve IV Percentile; IV yüksek & RV düşük → short vega + günlük delta hedge; IV düşük & RV yüksek beklentisi → long vega; calendar/vertical/straddle/strangle; riskler volatility crush, gap.

### 2.3 Teyit

**R004** (defterde haftalık kanal dibi taraması; bayrak/flama fikir):
- 1956037514977771681, 1956081917054607589, 1956082078212305072 (2025-08-14): haftalık alt banda temas yetmez; haftalık mum yeşil kapanmalı.
- 1957891785339850868 (2025-08-19): bayrak kırılımında hacim > 20 günlük hacim ortalaması; fiyat 13 günlük ortalama üstünde.
- 1958226602883711124 (2025-08-20): gün 1 kanal dışı kapanış; gün 2 kırmızı mumla üst banttan destek; gün 3 yüksek hacimle yeşil mum; hacim eşiği yok.

**R008** (defterde RSI kırılım etiketleri, parametre yok): → 1909110157600051269 (2025-04-07): RSI Trendline Breakout lookback = 50, extend = 40, min_gap = 20 (tanım yazılı değil).

**R024** (defterde MACD AL/SAT legend): → 1957511470687649855 (2025-08-18): MACD (12,26,9) + trend kanalı (güven düşük).

**R053 (BB kısmı)** (defterde ±2SD, −2/−3SE tepki alımı):
- 1782897014444818512 (2024-04-23): BB 3 SS; bant teması sonrası ilk mum zıt renkte ise dönüş.
- 1846648064695848972 (2024-10-16): "3SS BB ve zır mum kapanış. En sevdiğim."
- 1846989330382041324 (2024-10-17): günlük; önceki gün alt banda iğne, son gün yeşil kapanış = AL.

**R072** (defterde şartlar maskeli, okunamadı): → 2048341370742436134 (2026-04-26): panel başlıkları "...Eğimler Yukarı & Pozitif", "...(Yön Yukarı)", "...Pozitif ve Yükselen"; gösterge adları silinmiş; KTLEV 24 Nisana kadar %167, BTCIM 18 günde %31. **[AÇIK SORU CEVABI, kısmen]**

**R075** (defterde Siyah Kuğu + talep): → 1870258183958126788 (2024-12-21): AB/XA 0.382-0.724, BC/AB 2.0-4.237, CD/BC 0.5-0.886 (görselden, satırda); örnek 0.48 / 3.15 / 0.40; hedef 9644.60.

**R082** (defterde konsolidasyon süresi ↔ kırılım): → 1925633169694277851 (2025-05-22): range = 30. 1926353549723590759 (2025-05-24): 60 gün zirve + talib (Aile 22).

**R114** (defterde fincan-kulp; hedefin tabanı yazılmamış):
- 2095558917841404010 (2026-09-03): "Retest beklemezseniz sonu felaket olabilir."; kalite 73.8/100, R/R 1:1.93, hacim 2.47x, kırılım 12.65, hedef 15.52, stop 11.60, Fib %38.2 11.55, %50 11.21.
- 2095562062332043622 (2026-09-03): MTRKS kalite 68.5, R/R 1:1.79, hacim 1.96x; kırılım 28.80, hedef 37.15, stop 25.05, Fib 25.61 / 24.62.
- 2096284655657836608 (2026-09-05): TRCAS kırılım 48.60, hedef 56.03, stop 45.18; Fib = kırılım − oran × (hedef − kırılım) (hesaptan: 48.60 − 0.382 × 7.43 = 45.76). Hedef tabanı yine yazılı değil.

**R116** (defterde gizli pozitif uyumsuzluk, gösterge adı yok):
- 1905331669092950235 (2025-03-27): gösterge RSI; pivot çizgilerinin min/max eğimleri. **[AÇIK SORU CEVABI]**
- 1910400582935847408 (2025-04-10): dipler arası 2-6 hafta; RSI ilk dip < 30; 2. dipte hacim artışı; yeşil mum; EMA 8 kırılımı; kaçın: RSI farkı küçük (42→44), dipler arası 2-3 gün, düşen kanal.
- 2043792925209817159 (2026-04-13): günlük; 2 yıla kadar geriye bakış.
- 2046663429478330488 (2026-04-21): komşu dip/tepe arası 10-30 bar en sağlıklı; 70+ bar uyumsuzluk değil.

**R124** (defterde düşen direnç kırılımı, "hacim eşik yok", EMA 5/8/13):
- 1940118051640197615 (2025-07-01): hacim(t) ≥ 1.5 × hacim(t−1); CMF pozitif. **[AÇIK SORU CEVABI]**
- 1949509666456650215 (2025-07-27): hacim > 1.5 × son 5 gün ortalaması; son 20 gün düşen çizgi testi; RSI > 50; MACD kesişimi ya da histogram pozitif. **[AÇIK SORU CEVABI]**
- 1979546907505545421 (2025-10-18): hacim ortalamanın 2-3 katı (Aile 28). **[AÇIK SORU CEVABI]**
- 2048151591279104244 (2026-04-25): 28 haftalık kanal kırılımı, fiyat VWAP üstünde, momentum+ filtresi (tanımsız).
- Düşen kanal taramaları 1987233906827903088, 2011135212382761149, 2016954643394216029, 2016967838120964296, 2023815727309091176 (Aile 23).

**R127** (defterde EMA sıkışması, oran serbest): → 1957935566827221201 (2025-08-19): EMA50 ve EMA100; sıkışma son 10 günde başlamalı; çekirdek 6 bar; sıkışma + yükselen trend desteği + MACD birlikte. Oran yine yok.

**R137** (defterde CMF, eşik yok):
- 1845562970304102747, 1845567753878384928 (2024-10-13): son 3 gün pozitif VE önceki 3 gün negatif; filtre olarak kullan, "Bu sinyale göre al sat yapmayın".
- 1865470227720405267 (2024-12-07): "Genelde 6 gün bakıyorum. Son 3 gün pozitif Önceki 3 gün negatif". **[AÇIK SORU CEVABI]**
- 1848801936935678178 (2024-10-22): CMF Buy/Sell sinyali, son 3 günde artan giriş (bkz. Bölüm 4).

**R188** (defterde ADX 22,9 "trend oluşum aşaması"): → 1761664515484057831 (2024-02-25): ADX 60–100 anlamlı; 40–60 görece iyi. 1761664518353031643 (2024-02-25): pandas_ta adx length=14; ADXR ile. **[AÇIK SORU CEVABI]** (eşik çelişkisi için Bölüm 4).

**R195** (defterde kapanış + hacim teyidi, retest, 1×ATR stop): → 2095199834374320434 (2026-09-02): kırılım = 28,52 üstünde 4 saatlik mum kapanışı; retest ve tutunma gerekir; 25,56 altı uyarı; 24,98 geçersizlik (otomatik stop değil); hedefler 30,64 / 32,20 / 42,10.

**R208** (defterde confluence): → 1911052816333918382 (2025-04-12): EMA'lar aşağı ve fiyat hepsinin altındaysa sinyal yalnız tepki; EMA5/EMA8/EMA21 dirençleri; haber/makro (delta, call kümelenmesi + LLM).

**R214** (defterde EMA5 > EMA8 > EMA13): → 1911425114245124453 (2025-04-13): + EMA21; RSI kırılımı 30 üstünden (60.29); MACD kesişim noktası 0 üstü.

**R221** (defterde takas toplanma fikri): → 1939258295551701476 (2025-06-29), 1964331893341503858 (2025-09-06) (Aile 20).

**R237** (defterde birikim anlatısı): → 1938970182380134893 (2025-06-28): TERA %76 örneği (Aile 20).

**R238** (defterde gövde/hacim anomalisi): → 1992161805087408487 (2025-11-22): açılış saatindeki mum; sonraki mum hacimle desteklenmezse teyitsiz, düşüş habercisi.

**R246** (defterde 80-100 hafta yatay dipte bekle): → 1948102083556626664 (2025-07-23): 38 hafta yatay (9.80–12.71, genişlik %29.69); önceki hafta kırılım + son hafta kanal üstü kapanış = "Teyitli".

**R247** (defterde "Güzer retest var", fikir): → 2097063290224431474 (2026-09-07): Aile 23'teki 60 bar metrikleri ve "RETEST + TUTUNDU".

**R253** (defterde Breakout→FVG→Retest→Confirmation, tolerans yok): → 1949799810053104041 (2025-07-28): Lookback 75; kırılım 2025-07-09 → pullback 2025-07-18 → onay 2025-07-21. 2095523694881697974 (2026-09-03): retest yeri range high; "FVG %50" çizgisi; RSI divergence; VolMA20; A+ ve 100/100.

Genişletilen R kaydı sayısı: 40 (R004, R008, R024, R031, R053, R060, R072, R075, R082, R108, R114, R116, R124, R126, R127, R128, R137, R138, R184, R188, R189, R193, R195, R198, R199, R203, R206, R208, R210, R212, R214, R221, R233, R234, R237, R238, R246, R247, R253, R255).

---

## 3. Çelişkiler

Tüm çelişkilerde gönderi önce, defter kaydı sonra gelir. Defter tarihi kayıt tarihidir; Tansu'nun özgün cümlesinin tarihi belirsiz.

### Ç1: Bollinger üst bandı: ters sinyal mi, trend sinyali mi?
- Gönderi 1775396085038469494 (2024-04-03): "Üst bant momentum indikatörü ve +-DI ile beraber takip edilirse, BB güvenilirdir. Yatay piyasada zaten band sıkışır tadı tuzu olmaz".
- Defter R053 (2026-08-27 19:40): "Fiyatın bu bantların dışına çıkması aşırı alım veya aşırı satım bölgesine girildiğini gösterir. Kuyrukları bu yüzden takip ederiz".
- Sonra gelen: defter.
- Olasılık: bağlam (rejim ayrımı). Kanıt: Tansu −3SS dip teması alımını da kullanıyor (1846648064695848972, 2024-10-16: "En sevdiğim"). Keltner için aynı ayrımı yazıyor: trendde üst bant üstü kapanış al, yatayda ortalamaya dönüş (1852476829543587877, 2024-11-01). Hata kanıtı yok.

### Ç2: RSI tetik seviyesi 50 mi, 30 mu?
- Gönderi 1827737912210788788 (2024-08-25): "RSI'da benim için sinyal 50 çizgisi kırılımı ile gelir. (Orta çizgi)".
- Defter R233 (2026-08-28 12:30): "RSI (14) değeri, 30 seviyesinin altından yukarı doğru keserek bu seviyenin üzerinde bir kapanış yaptığında." Çıkış RSI 70 reddi.
- Sonra gelen: defter.
- Diğer eşikler (çeşitlendir/genişlet satırları): RSI 50 + BB orta bant (1774426858567643590, 2024-03-31); 55/45 (1860422703150149949, 2024-11-23); 30-40 bandı (1946652258260635954, 2025-07-19); RSI > 50 (1949509666456650215, 2025-07-27); RSI > 60 (1979546907505545421, 2025-10-18); 30 kesişimi + RSI50 ilk direnç (1990003872023130607, 2025-11-16).
- Olasılık: bağlam daha güçlü, tarihçe de olası. Kanıt: 2025-11 gönderilerinde 30 girişi ve 50 reddi aynı sistemde birlikte (1991721699922870638: "RSI 50 reddi" %50 satış tetiği). 50 = trend/momentum tetiği, 30 = dipten dönüş tetiği olabilir. 2024'te 50, 2025-11 sonrası 30 ağırlıklı; bu sıra tarihçeyi destekler ama 2025-07'de RSI > 50 yine var. Belirsiz.

### Ç3: Kısa pencereli SMA kesişimi ile "ortalama yalandır"
- Gönderi 1764294925791777136 (2024-03-03): "benim parametrelerim 5 günlük ve 25 günlük basit hareketli ortalamalar üzerine kurulu".
- Gönderi 1771510245702914481 (2024-03-23): "fastLength = input.int(10, ...) slowLength = input.int(100, ...) fastMA = ta.sma(close, fastLength)".
- Defter R106 (2026-08-27 23:19): "n degeri ne kadar kucukse (ornegin 10 gunluk sma), bu yalan o kadar buyuk olur."; R001 (2026-08-27 16:40): "Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın". R105 (2026-08-27 23:14) ortalama eğimine bakmayı önerir.
- Sonra gelen: defter.
- Olasılık: tarihçe ya da bağlam. Tarihçe kanıtı: SMA 5/25 ve 10/100 gönderileri 2024-03; medyan önerisi 2026-08. Bağlam kanıtı: R106 ölçüm ilkesidir (aykırı değer), kesişim sinyali değildir; Tansu 2025'te de ortalama kesişimi paylaşıyor (Aile 7, ör. 1978879623648739789, 2025-10-16; SMA200/250 1989651383092744703, 2025-11-15). Hata kanıtı yok.

### Ç4: Düşüşte kademeli / ortalama maliyetle alım
- 1770866826408345737 (2024-03-21): "Doğrusu ben büyük resme odaklandığım için -3 de alım yaptım.düştükçe alırım."
- 1775984086605021494 (2024-04-04): "ben 115'den de kademeli alım yapılması taraftarıyım, zira hisse dip çalışmasını tamamlayıp oradan dönebilir. Şu an için algoritmalar al sinyali vermiş değil."
- 1781179209886449724 (2024-04-19): "ortalama maliyet mantığı ile evet kademeli alıma geçilebilir"; 1818329260333113535 (2024-07-30): "kumbara hisse, düştükçe alıyorum."
- Defter R172 (2026-08-28 05:21): "Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR."; R257 (2026-09-06 13:36): "Şu aşamada dip tahmini yapmaya çalışmak yerine, piyasanın yukarı yönlü iradesini göstermesi beklenmelidir."
- Sonra gelen: defter. Olasılık: bağlam (uzun vade / "kumbara" hisse ile sistem işlemi ayrı) ya da tarihçe. Kanıt: "büyük resme odaklandığım için", "kumbara hisse" ifadeleri ayrı bir portföy türünü gösterir. Yükselen trendde martingale gönderisi (1876964680947696067, 2025-01-08) de pozisyon artırımı içerir. Güven: satırların ikisi "dusuk", ikisi "orta". Belirsiz.

### Ç5: "Dipte yakalamak"
- Gönderi 1861840939741757904 (2024-11-27): "dipte yakalamak lazım algoritma da bunu sağlıyor." (20 günlük marjı kaçmış kırılıma girilmez).
- Defter R172 (2026-08-28 05:21): "Asıl amacımız ASLA TEPE VEYA DİP NOKTALARI YAKALAMAYA ÇALIŞMAK DEĞİLDİR."
- Sonra gelen: defter.
- Olasılık: bağlam (söz düzeyi). Kanıt: gönderi dip tahmini değil, algoritmanın erken kırılım sinyalini kastediyor ("algoritma da bunu sağlıyor"); R172 de "kırılma (dönüş) noktalarını 'tespit etmek'" der. Bu okumada çelişki sözcük düzeyindedir. Belirsiz.

### Ç6: ATR katsayısı ve ilk kâr alma yeri
- Gönderi 2022431570012106899 (2026-02-13): "Başlangıç Stop: 143.66 TL" (= 155.00 − 1.5 × 7.56) ve "3 ATR ... Stop güncellendi + %50 SATIŞ".
- Gönderi 2045421697814126693 (2026-04-18): "Başlangıç Stop: 13.15 TL" (≈ 15.05 − 1.5 × 1.27) ve "3 ATR'ye ulaşınca %50 satış yapın" (iki görsel doğrulandı).
- Defter R184 (2026-08-28 06:30): "Giriş fiyatının 2ATR altına da acil stop konulur."; R239 (2026-08-28 12:34): "İlk kar alma yeriniz, bu nokta geçildikten sonraki barlardan hangisi bir gün öncekinin en düşüğünün altında kapattı ise orasıdır. %50'sin satın."
- Sonra gelen: defter. Sıra: 2×ATR (video 1999481868106826013, 2025-12-12; 2005227814875021373, 2025-12-28) → 1,5×ATR başlangıç stop (2026-02, 2026-04) → defter 2×ATR (2026-08). Defter içinde R195 1×ATR stop da var.
- Olasılık: bağlam daha güçlü. Kanıt: merdiven ayrı bir araç ("SABİT ATR KAR ALMA SİSTEMİ", "İZ SÜREN STOP SİSTEMİ"); R184 acil stop kuralıdır. Sıra tek yönlü değil (2 → 1,5 → 2), bu yüzden tek bir tarihçe değişikliği zayıf. Hata kanıtı yok. 1,5 ATR sabiti R239'da da var (iz süren moda geçiş), rolü farklı.

Çelişki sayısı: 6 konu, 11 satır.

---

## 4. Tansu'nun gönderi içi hata ve tutarsızlıkları; defter okuma hataları

### 4.1 Hesap, formül, metin–görsel

Grup 1:
- 1874416190443114907 (2025-01-01): "%11.12 kazanmanız lazım". Doğru değer 1/0,9 − 1 = %11,11. Neden: yuvarlama. Düzeltme: %11,11 yaz.
- 1870258183958126788 (2024-12-21): CD/BC = 0.40, hedef aralık 0.5–0.886; araç yine "Found" diyor. Neden: aralık denetimi yok ya da tolerans var (belirsiz). Düzeltme: defterde aralık dışı eşleşmeyi işaretle.
- 1839078126015438978 (2024-09-25): "pozitif uyumsuzluk" örneğinde fiyat da yükselmiş (58.50 → 61.45). 1843754494062145990 (2024-10-08): AKCNS'de fiyat ve MACD birlikte yükseliyor. Neden: tarama yalnız n gün öncesiyle karşılaştırıyor, dip/tepe yönünü sınamıyor. Düzeltme: uyumsuzluk tanımına dip-dip karşılaştırması ekle (R116 kuralı).
- 1840350261803470950 (2024-09-29): fiyat 10 gün öncekinden yüksek (5.57 → 5.64). Klasik pozitif uyumsuzlukla uyumu belirsiz; satır bunu belirtmiyor.
- 1841228866234601958 → 1841235974430273798 (2024-10-01): "ROC>50" yazdı, sonra "Roc50 > 0 olmalı. Yanlış yazmışım yukarıda" diye kendisi düzeltti. Doğru kural: RoC50 > 0.

Grup 2:
- 1841923620714774620 (2024-10-03): metin MA20 > MA50, iki ortalama yükselir, geri çekilme sınırı der; kod yalnız SMA20/SMA50 hesaplar ve çizer, koşulu uygulamaz. Neden: metin–kod uyuşmazlığı.
- 2016967838120964296 (2026-01-29) ve 2023815727309091176 (2026-02-17): başlık "DÜŞEN KANALI YUKARI KIRDI"; görselde üst çizgi düşen, alt çizgi yükselen (daralan yapı). Neden: ad ile şekil uyuşmuyor. Düzeltme: "daralan yapı kırılımı" diye ayır.
- 1847338202924744724 (2024-10-18): GLCVY grafiğinde eksen "Price in USD" yazıyor (görsel doğrulandı). Neden: kod varsayılan etiketi. Etkisi yok; birim TL olmalı.
- 1848801936935678178 (2024-10-22) ile 1845562970304102747 (2024-10-13): önce "Bu sinyale göre al sat yapmayın ... filtre", 9 gün sonra "Chaikin Money Flow Buy/Sell sinyali oluştu". Olasılık: sunum farkı ya da tutarsızlık; belirsiz.
- 1761664515484057831 (2024-02-25): "ADX'in anlamlı bir sinyal üretmesi için değerinin 60-100 arasında olması gerekiyor"; 1853909406553137314 (2024-11-05): ADX panelinde 20 ve 25 eşik çizgisi. Eşikler uyuşmuyor; bağlam belirsiz.

Grup 3:
- 1983565377532572092 (2025-10-29) "W3*0.618" ile 1978152557945000041 (2025-10-14) "üçüncü itki sonu + C dalgası × 0,618": iki farklı hedef tanımı; başlangıç noktası yazılı değil. Belirsiz.
- 1760725150406988034 (2024-02-22): çift EMA koşulunun ikinci kısmı görselde kesik. Kural eksik.
- 2045489485996019907 (2026-04-18): üst gönderideki EMA sıkışması %1-%1,5 Tansu'nun değil (atıf notu). Bu değeri Tansu'ya bağlama.
- ASTOR görseli (2022431570012106899): 20 ATR hedefi 306.14; 155 + 20 × 7,56 = 306,20. YAPRK görseli (2045421697814126693): 1 ATR kâr %8.42; 1,27/15,05 = %8,44. Neden: ATR tabloda yuvarlanmış gösteriliyor. Hata değil; kuralı etkilemez.

### 4.2 Defter okuma hataları

- tema-3.jsonl'de "DEFTER OKUMA HATASI" satırı yok (aranan dizgi: "OKUMA HATASI", sonuç 0).
- sonuc.jsonl'de 4 okuma hatası satırı var (2036840358210945219 R164, 2018743366112985154 R176, 2061554188832702624 R074, 2092340608480297126 R008). Rolleri değerleme-temel, ürün-hedefi, sinyal-sonucu; bu temaya girmiyor.

---

## 5. Defter için öneri listesi (öncelik sırasıyla)

Öncelik ölçütü: tam parametre + Tansu'nun kendi yöntemi + birden çok gönderide tekrar. İlk 10 maddede görsele dayanan parametreleri Read ile açtım: 2, 7, 8 doğrulandı; uyuşmazlık yok (yalnız 4.1'deki yuvarlama ve "USD" etiketi).

Grup 1 (1–5):
1. **genişlet R184**: "Hisse Volatilitesi" = 2 × ATR; %1 risk örneği (100.000 $ → 1.000 $; 2 ATR 14.30 $ → 70 hisse). Kaynak: 2005227814875021373, 1999481868106826013 (video).
2. **genişlet R239**: ATR(14) hedef/stop merdiveni (hedef_n = giriş + n×ATR; başlangıç stop giriş − 1,5×ATR; n ATR'de stop (n−2) ATR; 3 ATR'de %50; stop yalnız yukarı). Ç6 notunu yanına yaz. Kaynak: 2022431570012106899, 2045421697814126693.
3. **ekle**: RoC50 + ADX(14)/ADXR(14) + OBV/SMA20 sistemi ("Favori sistemim"); çıkış ADX ADXR'yi aşağı keser. Kaynak: 1841955633047670978, 1841222101497246009, 1842064079826936219, 1841235974430273798.
4. **genişlet R137**: CMF 6 gün penceresi: son 3 gün > 0 VE önceki 3 gün < 0; yalnız filtre. Kaynak: 1865470227720405267, 1845562970304102747, 1845567753878384928.
5. **genişlet R233**: çıkış tetikleri RSI 50 reddi / SMA 50 reddi / 1,5 ATR kârda önceki gün düşüğü altı kapanış (her biri %50; ikisi → tam çıkış); 1,5R break-even çıkışı. Kaynak: 1991721699922870638, 1992547498343161903, 1990003872023130607, 1991558168149987328.

Grup 2 (6–10):
6. **genişlet R053**: BB 3 SS + önceki gün alt banda iğne + son gün zıt (yeşil) kapanış = AL ("En sevdiğim"). Ç1 rejim notunu ekle. Kaynak: 1846989330382041324, 1846648064695848972, 1782897014444818512.
7. **ekle**: RSI-Fibonacci (144 gün): seviye = maxRSI − oran × (max − min); 0.618/0.786 dönüşü + mum teyidi + fiyat > 50 g ort; stop son düşüğün %2-3 altı; çıkış RSI 50-60. Kaynak: 1977450129008251116, 1912151798992814185, 1986917436310909146, 1912933957592834220, 1925626094935236883.
8. **ekle**: Golden Cross / Death Cross (EMA50/EMA200), ön tarama fiyat > EMA200. Kaynak: 1847338202924744724, 1847355900014858452, 1848805888355652024, 1842524448802365487, 1911462470763360258.
9. **ekle**: SuperTrend filtresi + son gün EMA5/EMA20 yukarı kesişi (ST önceden bullish = daha sağlam). Kaynak: 1852060552413221135, 1852057966960349695, 1851991078661976137.
10. **ekle**: Vegas tüneli EMA12/144/169 yukarı kesişi (günlük), kâr al ATR. Kaynak: 1827341150908543159, 1848385592771424616, 1848803496893558928, 1851726487855972606.

Grup 3 (11–15):
11. **ekle**: Range Breakout 60 gün (son gün yüksek ve kapanış > 60G zirve + talib bullish formasyon + ertesi gün teyit). Kaynak: 1926353549723590759, 1925633169694277851, 1929184555816419717.
12. **ekle**: Düşen kanal kırılım taraması (60/90/150 bar; çıktı: direnç, eğim, kırılım farkı, temas, retest durumu); daralan yapıyı ayrı etiketle. Kaynak: 2097063290224431474, 2011135212382761149, 2016954643394216029, 2023815727309091176, 1987233906827903088.
13. **genişlet R124**: hacim eşikleri: ≥ 1,5 × önceki gün; > 1,5 × 5 gün ortalaması; kırılımda 2-3 × ortalama. Kaynak: 1940118051640197615, 1949509666456650215, 1979546907505545421.
14. **genişlet R116**: gösterge RSI; dipler arası 2-6 hafta / 10-30 bar; RSI ilk dip < 30; 2. dipte hacim artışı; kaçınma listesi; 2 yıl geriye bakış. Kaynak: 1905331669092950235, 1910400582935847408, 2046663429478330488, 2043792925209817159.
15. **ekle**: MOST/OTT/VAR formül ailesi (CROSS ifadeleri ve OPT aralıkları birebir). Kaynak: 1782497478056558995, 1779421690071490990, 1783371645224149075, 1786779842530226293, 1784690075059585046.

Grup 4 (16–20):
16. **genişlet R108**: Weinstein 2. aşama = fiyat > 150 ve 200 g ort; 150 > 200; 200 yukarı dönmüş. Kaynak: 1945064189082599687.
17. **genişlet R210**: EMA20 > EMA50 + fiyat EMA50 üstünde 2 gün kapanış; geri çekilme en fazla MA20–MA50. Kaynak: 1771668829900357977, 1841922080541180029.
18. **genişlet R212**: SMA200/SMA250 geri alma tetiği (altında kapanış, ertesi gün üstünde + momentum). Kaynak: 1989651383092744703.
19. **genişlet R128**: 13 EMA'dan ATR uzaklığı (1-2 ATR sağlıklı; 3 ATR spike = kâr al, yeni alım yok). Kaynak: 1963273280581751113.
20. **genişlet R193**: 5. dalga hedefi "W3*0.618" (başlangıç noktası belirsiz notuyla). Kaynak: 1983565377532572092, 1978152557945000041.

Grup 5 (21–25):
21. **çeşitlendir R148**: RSI + SuperTrend 60 dk (AL RSI > 55 ve bullish; SAT RSI < 45 ve bearish). Kaynak: 1860422703150149949.
22. **ekle**: Avellaneda–Stoikov ve MA5 adil değer sapması (> %3 short, adil değerin %1 altında kapat). Kaynak: 1911789788019019979, 1911734132360552515.
23. **çeşitlendir R053**: BB–Keltner squeeze ve Keltner rejim kuralı. Kaynak: 1912246536811008424, 1852476829543587877, 1783228274077839740.
24. **çeşitlendir R053/R233**: BB orta bant + RSI 50 kesişimi; BB sıkışması + RSI 50. Kaynak: 1774426858567643590, 1782881410174365714, 1839057936141705262.
25. **ekle**: EMA26 ATR bantları (−3R reddi, −2O onayı). Kaynak: 1978494634121703760.

Grup 6 (26–30):
26. **ekle**: MACDAS/MACDASTRIGGER kesişimi (OPT1 13–55, OPT2 8–15, OPT3 3–13). Kaynak: 1778777162587279414.
27. **ekle**: 5 günlük toplam kırılım puanı rejim etiketi (≥ +3 BULL, ≤ −4 BEAR). Kaynak: 2042901081785557425, 2042948983744557423.
28. **ekle**: EWMA z-skoru ±2σ. Kaynak: 1936767147914485837.
29. **genişlet R195/R114**: retest zorunluluğu ve kırılım araç çıktısı (kalite, R/R, hacim x, Fib 38.2/50); 4 saatlik kapanış kırılımı ve geçersizlik sınırı. Kaynak: 2095558917841404010, 2096284655657836608, 2095199834374320434, 1949799810053104041.
30. **genişlet R053 (VaR)**: %99 güven, ufuk 1 g/1 h/1 ay/3 ay, limit aşılınca hedge (put ya da ters korelasyonlu hisse). Kaynak: 1878086550665175243, 1878089934268965110, 1878086552548442457, 1734957210545844544.

Grup 7 (31–35):
31. **çeşitlendir R184/R212**: Kelly / fractional Kelly ile pozisyon limiti (formül yok, "belirsiz" notuyla). Kaynak: 1874426039340007571, 1874425159224000594.
32. **genişlet R221/R237**: AKD ve takas daralması kuralları (net alıcı payı, son 10 gün, el değiştiren takas = tuzak). Kaynak: 1938970182380134893, 1939258295551701476, 1964331893341503858.
33. **ekle**: opsiyon call/put duvarı (fikir düzeyi; kırılım ölçütü yok). Kaynak: 2085043984414409205, 2085278210728599696, 1994748031900492128.
34. **çeşitlendir R183**: haftanın günü getirisi; en kötü günde işleme girme. Kaynak: 1891208151497613761.
35. **genişlet R138**: kayıp telafi formülü 1/(1 − kayıp) − 1. Kaynak: 1874416190443114907.

Öneri listesine koymadıklarım: Aile 3, 4 (saat), 5, 18, 34–44. Çoğu fikir düzeyinde ve tek gönderili. İstisna: Aile 34 (OBO "2-Red" + 2ATR stop) tam parametreli ama tek gönderi; Aile 44 üç gönderili ama eşik tutarsız. Defter bunları "fikir" notu olarak alabilir.
