# TEMA 5b — Ürün hedefi ve sinyal sonucu: defter öneri belgesi

Girdi: `tema-5b.jsonl` (248 satır: genisletir 104, cesitlendirir 98, yeni 30, celisir 13, ayni/DEFTER OKUMA HATASI 3). Rol: ürün-hedefi 164, sinyal-sonucu 84.
Kaynak: her iddia satırın `kanit` alanına dayanır. "(görsel doğrulandı)" notu, görseli bu çalışmada açıp değerleri karşılaştırdığımı gösterir.
Tarih notu: defter kayıt tarihleri (R001–R263: 2026-08-27 … 2026-09-06) Levent'in yapıştırma tarihidir. Tansu'nun sözü daha eski olabilir. Bu yüzden "gönderi önce, defter sonra" sırası kesin değildir. Bu belgede "defter tarihi" hep yapıştırma tarihidir.
Not: 98 "cesitlendirir" satırının hepsinde `yontem_defterde = yok`. Bu satırlar Bölüm 1'e girer.

---

## 1. Yeni yöntem aileleri

Olgunluk: **tam** = kural ve parametre birebir; **çekirdek** = kural belli, parametrenin bir kısmı eksik; **fikir** = ad ya da plan.

### 1.1 Rolling Sharpe tepkisi — çekirdek
- Ne yapar: 21 günlük rolling Sharpe, hisseye özgü bir seviyenin altından yukarı döner. Bu dönüş sinyaldir.
- Parametreler (görsel doğrulandı): pencere 21 gün. ICUGS seviye −0.40, "Prev Sharpe = -0.5398, Last Sharpe = -0.3911". METRO seviye −0.6, "Tepki Tarihi: 2025-03-24 | Prev Sharpe: -0.6207 → Last Sharpe: -0.5819". Kural: önceki değer < seviye ve son değer > seviye. Seviyenin hisse başına nasıl seçildiği belirsiz.
- Kaynak: 1905152595586318386 (2025-03-27), 1905219676352676212 (2025-03-27), 1905345708858749109 (2025-03-27), 1905153170805776426 (2025-03-27; liste KRTEK, IHLGM, ICUGS, GEDZA).
- Sonuç: "Bugün bu stratejimiz ile tavan aldık 2 tane de iyi getiri elde ettik." METRO 26 Mart %5.
- Not: ICUGS grafiğinde 2023 ortası–2024 ortası veri boşluğu var (görsel).

### 1.2 Fon akışı ve fon riski ailesi — çekirdek (getiri tahmini) / fikir (risk radarı)
- **Fon günlük getiri tahmini** (görsel doğrulandı): hisse katkısı = KAP portföy ağırlığı × günlük getiri; fon tahmini = katkıların toplamı. THF: fon ₺92.90 Mr, KAP 08/2026, KAP hisse %97.79, TEFAS brüt hisse %84.57; ANELE %4.70 × +5.29% = +0.249%; KARCL %6.48 × −4.38% = −0.284%; toplam +1.05%. V4 (DOH): hisse +1.49% + VİOP +0.05% = +1.54%; "reconciliation katsayısı 0.7789" (= 69.13/88.75). Kaynak: 2097060991586447371 (2026-09-07), 2097065200687915032 (2026-09-07). Sonuç: THF "beklentimiz maalesef gerçekleşmedi"; DOH "nokta atışı". Gerçekleşen değer yazılı değil.
- **Fon para akışı sıralaması** (görsel doğrulandı): "20 Günlük En Güçlü Para Giriş / Çıkışları"; en güçlü giriş THF (~75,7k milyon TL), en güçlü çıkış GAL. Seçim eşiği yok. Kaynak: 2095922815329263677 (2026-09-04).
- **Fon pozisyon değişiminden hisse baskısı**: "birkaç fon aynı anda pozisyon artırıyorsa bunu erken fon birikimi ağırlıklar eş zamanlı düşüyorsa kurumsal satış baskısı". Fon sayısı ve pencere yok. Kaynak: 2096343856476496081 (2026-09-05).
- **Fon çıkışından satış baskısı tahmini + güven skoru**: geçmiş KAP raporlarıyla "satış yönünü yüzde kaç doğru yakaladı" skoru. Model tanımı yok. Kaynak: 2099970636386812395 (2026-09-15).
- **Fund Risk Radar**: "fon için 0–100 arasında bir risk skoru". Bileşenler: para akışı (5G/20G), AUM zirveden geri çekilme, yoğunlaşma (ilk 5/10 hisse), likit tampon (nakit, ters repo, mevduat), VİOP (hedge oranı, beta ayarlı net risk, KAP güncelliği). Bileşen 85/100 ise genel risk düşük olsa da kritik. Sonraki aşama: %5/%10/%20 çıkışta günlük hacme göre tasfiye gün sayısı. Ağırlıklar yok. Kaynak: 2097551651838034055 (2026-09-09).
- **PPF yapısal risk ölçütleri**: dağınık ve likit portföy; tek ters repo, tek pay teminatı, tek karşı tarafa yoğunlaşmama; mevzuat sınırı üstü tampon. Eşik yok. Kaynak: 2099814980212134159 (2026-09-15).
- **Fon seçimi Treynor/M2/Jensen**: tanım yok. Kaynak: 1979637504694464888 (2025-10-18).
- Tansu'nun vurgusu: fon akışını hisse sinyaline çevirme ("erken fon birikimi", "kurumsal satış baskısı").

### 1.3 Aracı kurum (AKD) dağılımı ve konsantrasyon ailesi — çekirdek
- Ne yapar: ilk N alıcı kurumun net lot payını ölçer, yoğunlaşan hisseleri sıralar. Defterde R227 "Konsantrasyon" fikri var; AKD ölçümü yok.
- Parametreler: TOP2%/TOP5%/TOP10% (RODRG 59.42 + 32.43 = TOP2 91.85) — 1964443262544232634 (2025-09-06). Eşik "İLK ARACI KURUM %50+ OLAN HİSSELER: 79 adet" — 1966795896651477361 (2025-09-13). Pencereler 1 ay / 2 hafta / 1 hafta / 2 gün; ilk 5 sınıfları %95+, %90-95, %80-90, %70-80, <%70; ilk 2 sınıfları %80+, %70-80, %50-70, <%50 (590 hisse) — 1964450520560808209 (2025-09-06).
- Takip kuralı: önceki günlerde alıcı olan kurum n. gün satıcıya geçerse hisse takipten çıkar; ilk 5 alıcı/ilk 5 satıcı — 1964749763922038906 (2025-09-07).
- Puantaj: AKD + takas + halka açıklık + dolaşım; ağırlık yok — 1967154744679432216 (2025-09-14). Tek kurum (BofA) satış payı sıralaması, 194 hisse — 1967162325028548887 (2025-09-14).
- Yatay kanal + AKD: 10 gün, %değişim = (üst − alt)/alt (6.17–6.26 → %1.46); ilk 5 alıcı net %87.32 — 1939003175484133714 (2025-06-28). Sıra yatay → AKD → takas — 1940885669381054705 (2025-07-03).
- Genişleme fikirleri: sektör rotasyonu + 1 aylık AKD — 1992907336042893810 (2025-11-24); AKD üzerinde sinüs/Fourier döngüsü — 1978848810102042927 (2025-10-16).
- Aracı kurumlar arası korelasyon: "en az 1 aylık günlük veri" — 1970591583322947788 (2025-09-23); 5 kurum matrisi ve kurum-hisse ağı, 3 günlük veri, "Şimdilik güvenilir değil" — 1970601017650622775 (2025-09-23).

### 1.4 Parabolic SAR ailesi — çekirdek
- Ne yapar: fiyat–PSAR kesişiminde al/sat; ek paneller ADX/ADXR, Momentum, "Average Volume (10 bars)".
- Parametreler: SAR adım/maksimum yazılı değil. SMA 20/40 trend teyidi, kesişim sonrası ilk PSAR barında giriş.
- Kaynak: 1862617662196473882 (2024-11-29), 1862630588584214682 (2024-11-29), 1862635048819650793 (2024-11-29), 1864259354800578906 (2024-12-04), 1950999922742010108 (2025-07-31; trend teması tarihleriyle SAR dip dönüşü eşleşmesi), 2043779884867076189 (2026-04-13; kanal orta noktası + PSAR + LRC + CDLBELTHOLD/CDLCLOSINGMARUBOZU/CDLENGULFING).

### 1.5 RSI üzerine Fibonacci ailesi — tam (haftalık kod) / çekirdek (tarama)
- Ne yapar: Fibonacci fiyata değil RSI serisine çekilir.
- Kod (1839043892399735295, 2024-09-25): yfinance 1 yıl, haftalık ('W'); RSI 14 basit ortalama (min_periods=1); seviye = RSI_max − (RSI_max − RSI_min) × {0,236; 0,382; 0,5; 0,618; 0,786}; 161,8% = RSI_min − diff × 0,618. Haftalıkta 161,8 hedeflenir. Yakınlık eşiği yok.
- Türevler: 144 günlük RSI aralığı, 0.786 dip dönüşü + bullish mum — 1912136481751056753 (2025-04-15), 1912108045154271672 (2025-04-15). RSI 0.618 (~44) dönüşü + CDLENGULFING/CDLBELTHOLD — 1977423987274617023 (2025-10-12). Fiyat > EMA 89 ve "Rsifibo>0.618" — 1861794132093554798 (2024-11-27), 1862132559250907193 (2024-11-28), 1862203614174888388 (2024-11-28). Kod sözü — 1863676948934721894 (2024-12-02). 161,8 arama — 1839019703005753435 (2024-09-25), 1843356247476842791 (2024-10-07; "tarama kodu henüz hatalı"). Supertrend + MOST + RSI-Fibo 1,618 — 1840058987263279534 (2024-09-28). Üst gönderi başkasının (@KYamacl): RSI 0–100 tam, fibo 0,50'den alım — 1840021749603160095 (2024-09-28).
- Sonuç: MERKO +9,95, TMPOL +7,46, FRIGO +1,45, KENT 0,00, ULKER −1,61 (1912136481751056753).

### 1.6 Adaptif hareketli ortalamalar — FRAMA tam; KAMA, MAVİLİMW fikir
- **FRAMA** (1910723570654753121, 2025-04-11; kod görseli doğrulandı): period=16; N3 = (HHV16 − LLV16)/16; N1 = (HHV8 − LLV8)/8; N2 aynı, 8 bar kaydırılmış; Dimen = log((N1+N2)/N3)/log(2); alpha = exp(−4.6 × (Dimen − 1)), 0.01–1 kırpılır; FRAMA = alpha·(H+L)/2 + (1−alpha)·Close[t−1]. Al: Close FRAMA'yı yukarı keser; sat: aşağı keser. XU100.IS, 2025-01-01–2025-04-12. Tansu: "Buyurun geliştirin." Kod notu Bölüm 4'te.
- **KAMA**: "KAMA'yı kullanan var mı? Kodlamaya değer mi?" — 1852811907666714936 (2024-11-02). KAMA + pivot planı — 1852833497750056979 (2024-11-02), 1852989066276475387 (2024-11-03). Parametre yok.
- **MAVİLİMW (M7)**: fiyat kesişiminde al/sat; formül yok — 1877599322851741828 (2025-01-10), 1943066690709070008 (2025-07-09).

### 1.7 İz süren stop / trend takip ailesi (Supertrend, OTT, MOST) — Supertrend ve OTT tam
- **Supertrend** (1839989044693922032, 2024-09-28; görsel doğrulandı): range_period = 7, multiplier = 3; ATR = True Range ewm(com=7); temel bant = (High+Low)/2 ± 3 × ATR; bant kaydırma döngüsü.
- Supertrend türevleri: "supertrend 10/3 al ve 3/10 at, rsı>55 al ve rsı<45 sat" (@mehmetemanet stratejisi, Tansu parametreleri değiştirmiş) — 1860416194953543908 (2024-11-23). EMA5/EMA20 kesişimi + Supertrend rengi — 1850640152747561291 (2024-10-27), 1852010014329766290 (2024-10-31; "Kodu dün yazsaydım bugün %5'i alacaktık"), 1852011542746714531 (2024-10-31). + CMF + pozitif hacim — 1846135722635313326 (2024-10-15), 1846258267934347334 (2024-10-15). Evotrend = Supertrend + MOST + RSI 50 yukarı kesme — 1839361483618320455 (2024-09-26). Genel — 1829823456759644596 (2024-08-31).
- **OTT** (1790007806801621475, 2024-05-13; görsel doğrulandı): Pine v5; 'OTT Period' 30, 'OTT Percent' 7.0; MAVG = f_var(close, 30); fark = MAVG × yüzde × 0.01; longStop/shortStop iz süren; OTT = MT × (200 ± yüzde)/200; çıktı OTT[2]. f_var tanımı kodda yok.
- **MOST**: giriş taraması, parametre yok — 1844079823829991777 (2024-10-09). "MOMENTUM ÜSTÜNE MOST OPT Overall :1.784" — 1783470138877997162 (2024-04-25).

### 1.8 Vegas tüneli (EMA 12/144/169) — tam
- Kural: önceki barda EMA12 < EMA144 ve EMA12 < EMA169; son barda EMA12 ikisinin üstünde. Evren BIST 100; yfinance 15m, 2024-08-23–2024-09-23; ewm(adjust=False) — 1838671862420975657 (2024-09-24). Kısa vadeli trade, çıkış yok — 1783135314036376019 (2024-04-24). Kod span 12/144/169 — 1827315938741379225 (2024-08-24).
- Sonuç: "2022-2024 yılları arasında vegas tüneli stratejisi doaş getirisine yenik düşmüştür" (piyasa ≈5,4x, strateji ≈4,35x) — 1827794622434640093 (2024-08-25). "Vegas taramasından çıkan Dnisi tam gaz devam" — 1844743398047064231 (2024-10-11).
- Yakın: EMA 50/200 golden cross DOAS — 1908437183423209509 (2025-04-05).

### 1.9 Osilatörler (Stochastic, StochRSI, ROC) — Stochastic tam
- **Stochastic** (1897565005811183722, 2025-03-06; kod görseli doğrulandı): periods = 14, moving_av = 3; %K = (Close − LLV14 Low)/(HHV14 High − LLV14 Low) × 100; %D = %K'nın 3 gün ortalaması; K>D ve K<20 → "Güçlü AL"; K>D → "AL"; K<D ve K>80 → "Güçlü SAT"; diğer → "SAT". Veri 2022-01-01–2025-03-05. Tansu: "armut piş ağzıma düş yok öyle."
- **StochRSI**: EMA 9 + StochRSI, K/D 80/20, gün içi — 1853470102810669319 (2024-11-04), 1853496357958389772 (2024-11-04). Tarama — 1865133409573507522 (2024-12-06). Stok. RSI–RSI kesişimi sorusu — 1845131787879534626 (2024-10-12). Kıvanç Hoca kaynaklı strateji — 1778695219451470302 (2024-04-12). Gün içi stokastik — 1852337930032853472 (2024-11-01).
- **ROC**: RoC 9 sıfır eksen kesişimi (RoC 9/20/50 panelli) — 1840836969363841489 (2024-09-30); + ADX — 1841008747738497433 (2024-10-01); "ROC50 > 0 ADX > ADRX OBV artan" — 1841597392178536580 (2024-10-02).
- Panel seti: "Hacim + 20 Günlük Ort.", RSI(14), MACD (12,26,9), Stokastik (%K 14, %D 3); birleşim kuralı yok — 1955391561933656522 (2025-08-12).

### 1.10 Bollinger–Keltner sıkışması — çekirdek
- Ne yapar: sıkışmayı Bollinger–Keltner ilişkisiyle ölçer. "Sıkışma → Patlama döngüsünü otomatik yakalayan bu mantık" — 1913989895674028279 (2025-04-20). Görselde "Son Gün AL Sinyali" Bollinger üst bandı Keltner üstüne çıktığı yerde; RSI 30/70, ADX 25 — 1955389232639512999 (2025-08-12). + ADX/DMI, opsiyonda — 1853824189049762090 (2024-11-05). Ad — 1852079152050114950 (2024-10-31).
- Periyot ve çarpan yok. Sonuç: ENERY %4, MACKO %3.5, CANTE kötü — 1913126708485542223 (2025-04-18).

### 1.11 Adı defterde olmayan mum formasyonları — tam (iki kod) / fikir
- TA-Lib CDL listesi: CDLENGULFING, CDL3OUTSIDE, CDLCLOSINGMARUBOZU, CDLSHORTLINE, CDLDOJI, CDLBELTHOLD, CDLHARAMI, CDL3INSIDE; gün sonu Telegram — 1847942480169222236 (2024-10-20). BIST30 son gün; trend yönü yorumu kullanıcıya — 1847991564057927802 (2024-10-20).
- Adsız delici benzeri kod (tam): C[i]>O[i]; C[i]<O[i-1]; C[i]>C[i-1]; O[i]<C[i-1]; C[i-1]<O[i-1]; C[i-2]<O[i-2] → i+1 barında buy_signal=1 — 1899964404872941880 (2025-03-12).
- Ad düzeyinde: Marubozu — 1843733240835912163 (2024-10-08), 1843736658199622086 (2024-10-08; + K Volatility bantları), 1905488731408130410 (2025-03-28). Shooting Star — 1851736238522556502 (2024-10-30), 1851744148518559891 (2024-10-30). Terk edilmiş bebek — 1854965066933678492 (2024-11-08). Slingshot — 1905953307723522064 (2025-03-29). Belt Hold — 2045232231237521739 (2026-04-17). Tasuki Gap + pozitif uyumsuzluk, sonuç "%8'e yakın" — 1910750627728175106 (2025-04-11). Bearish rejection + Bollinger üst bant — 1763696979119382658 (2024-03-01).

### 1.12 Kanal orta noktası kırılımı — çekirdek
- Ne yapar: basamaklı orta hattın (yüksek/düşük kanalının ortası gibi) yukarı kırılımı, sonra trend takibi. Pencere ve çıkış yok.
- Kaynak: 1914173637898236379 (2025-04-21; "Yeni bir breakout sistemi :) İşimiz momentum."), 1914210602513236459 (2025-04-21), 1917567412125274471 (2025-04-30; + CDLCLOSINGMARUBOZU, CDLHIKKAKE), 2043779884867076189 (2026-04-13).

### 1.13 Grid bot — tam
- Kod (1839747420302831898, 2024-09-27): grid_size=0.4, position_size=50, atr_period=14, atr_multiplier=2; seviye = başlangıç × (1 − 0,4/100 × level), level 0–9; fiyat ≤ seviye → 50 lot; satış = seviye × (1 + 0,4/100); stop = fiyat − 2 × ATR(14).
- Çıktılar: satış = alım × 1,004; stop oranı sabit değil (0,9236 ve 0,9566) — 1839389286518723008 (2024-09-26). "Satış yapılacak fiyat: 67.60474012316895" (= 67.3354 × 1.004), stop = alış − 7.6629 sabit fark — 1943067673858052555 (2025-07-09).

### 1.14 Kredi ve iflas skoru (Altman, Bathory) — tam (formül kitaptan)
- 1890148860330406128 (2025-02-13; görsel doğrulandı, kaynak Uğur Özarslan, "Firmalarda Kredi Analizi" sayfası; Tansu metni: "Kodlayacağım"). Altman Z = 1.2·X1 + 1.4·X2 + 3.3·X3 + 0.6·X4 + 1.0·X5; X1 NİS/TA, X2 dağıtılmamış kâr/TA, X3 FVÖK/TA, X4 piyasa değeri/toplam borç, X5 satış/TA; Z < 1.81 iflas, Z > 2.99 güvenli. Bathory Z = (X1+…+X5)/5 × C; C sabit, değeri yok; "20'nin altında ise şirket iflas eder."
- Defterde R061 Merton modeli var; Altman yok.

### 1.15 Nicel finans modelleri — fikir / çekirdek
- Radon-Nikodym ölçü değişimi (çekirdek): AKBNK aylık 2018-01-01–2024-01-01, log getiri; mu_q = 0; xi = exp(−(mu_p − mu_q)·x + (mu_p² − mu_q²)/(2·sigma_p²)); f_q = xi·f_p, trapz ile normalize — 1911126829710073960 (2025-04-12).
- Avellaneda-Stoikov piyasa yapıcı: spread seviyelerinde kâr, pozisyon, risk, Sharpe; parametre yok — 1911703064748216597 (2025-04-14).
- Black-Scholes + Monte Carlo: yanlış fiyatlı opsiyon — 1852043715721994405 (2024-10-31); hisse fiyatı yolu — 1858372673430065639 (2024-11-18).
- Beklenti indirgemeli spot kur: sₜⁿ = (1 − Ψ) ∑ⁿᵢ₌₀ (Ψⁱ ⋅ Eₜ(xₜ₊ᵢ)); Ψ ve n yok — 1904627496487649715 (2025-03-25).
- Üçlü arbitraj: yalnız ad — 1861489657374192066 (2024-11-26).

### 1.16 Makro ve makine öğrenmesi tahmini — fikir
- Merkez Bankası faiz kararı botu: girdiler kur, CDS, enflasyon, dış ticaret, rezerv, M2; NLP PPK metni, Başkan açıklaması, haber; "Veri faiz artışı diyor ama açıklamalar güvercinse → bot bekle sinyali üretir"; her PPK öncesi güncelleme. Defterde ARIMA (R174) ve NLP (R065) adı var; faiz kararı amacı yok — 1913122317263057042 (2025-04-18).
- PCA: BIST faktörlerinden en önemlileri seçilip BIST100 getirisine regresyon, hedef endeks — 1771536925809135885 (2024-03-23). PCA + çoklu regresyon modelinden seçim, ons altın — 2084162959895310340 (2026-08-03).
- KNN: "%75 doğrulukla KNN algoritması yarın endeksin yukarıda olacağını söylüyor"; sonuç VİOP akşam +0.25 — 1859342666175218082 (2024-11-20).
- LSTM — 1862165685440245988 (2024-11-28). LSMA (OLS) tahmin — 1844843534156701805 (2024-10-11). Ridge/lasso/polinom F/K tahmini — 1797263560742994085 (2024-06-02).

### 1.17 Portföy türevleri — çekirdek / fikir
- Black-Litterman: BIST30, son 1 yıl momentum, Markowitz yanında — 1797263557978890521 (2024-06-02).
- VIF / varyans-kovaryans ile çoklu doğrusal bağlantı kontrolü — 1821204747614831017 (2024-08-07).
- Return_Risk_Ratio = YÜZDE / (Risk_Score + 1) (DUNYH 9,89 / 100,153 = 0,098749); Risk_Score tanımsız — 1985453771279757653 (2025-11-03).
- Faz 1/2/3 normalize getiri kıyası — 1878078841471611279 (2025-01-11).
- "Level 1 dip-tepe algoritmasında profit factor > 3 hisseleri bul" — 1908666927045886118 (2025-04-05).

### 1.18 Diğer tekil yöntemler
- Ichimoku bulut taraması, koşul yok — 1840861807633973669 (2024-09-30).
- Bull/Bear ratio: "boğalar %75 olsun" eşiği — 1950279832119472221 (2025-07-29); "buna bakarak asla işleme girilmez" — 1950290925252448467 (2025-07-29).
- Grafik ölçeği: uzun vade/büyük hareket logaritmik, kısa vade/dar aralık lineer — 1953201892202307992 (2025-08-06).
- NEFK artıp fiyat artmıyorsa kısa vadede artış — 1888814951256539448 (2025-02-10). Dönemsel satış/NEFK/ana ortaklık net kârı kodu — 1917582992001654921 (2025-04-30).
- P-BOM ("P-BOM 0/5", skor anlamı yok) — 2093768007554138123 (2026-08-29). Öncelik puanlı tarama (IDGYO 82.4 … TOASO 55.6; R:R 2.6/2.1/1.9; puan formülü yok) — 2094839266224267625 (2026-09-01).

---

## 2. Genişletmeler (R kaydı başına)

**[AÇIK SORUYU CEVAPLAR]** etiketi, defterin "yazılmamış/belirsiz" dediği noktayı kapatan gönderiyi gösterir.

### Formasyon ve kırılım
- **R114** (fincan-kulp): defterde hedef 389.30, "hedefin hangi tabana eklendiği yazılmamış". → 1987938049582391791 (2025-11-10; görsel doğrulandı): PRKAB "KIRILMA: 33.70", "HEDEF: 42.90", Fibo dip 24.50 → sağ yüksek 39.64. Hedef = KIRILMA + (KIRILMA − fincan dibi) = 33.70 + 9.20 = 42.90. R114'e uygulanınca 300.75 + (300.75 − 212.20) = 389.30 tutar. **[AÇIK SORUYU CEVAPLAR]** Formasyon tamamlanma 2025-10-27, sinyal 2025-11-03.
- **R004 / R007** (bayrak/flama, defterde yalnız ad): → araç çıktıları "Breakout" tarihli, hacimli kırılım şartı. 1941224929585922368 (EGGUB, direk ~62→~98, flama ~84–90, kırılım 2025-07-01, %8), 1949523572512481441 (ENSRI, 2025-07-22), 1953166070279209345 (TUKAS, 2025-08-01, hacim ~560 milyon), 1953506333476430012 (2025-08-01; "Takasa bi bakın"), 1954565115233140772 (SRVGY, 2025-08-04), 1964740931346968931 (BIGCH, 2025-09-02), 1984306004855505136 (IMASM, 2025-10-28, RSI ~75), 1993022005516619970 (CRDFA, 2025-11-19), 2031773880533053751 (AYCES, 2026-03-05, ~405→~538, kırılım sonrası ~698). Liste getirisi 2026-03-06→03-11 AYCES %29.83 … INFO 1.00 (17 hisse) — 2031774785504481621. Flama eğimi ve hacim eşiği yok.
- **R004 / R006** (takoz, yalnız ad): → "DERHL - Düşen Takoz Kırılımı", üst çizgi ~17→~10.8, alt ~14.1→~10.1, kırılım 2026-08-07, sonuç tavan — 2086820537137795283.
- **R004 / R245** (kanal): → basamaklı kanal alt bantta AL, üst bantta SAT; backtest 4 işlem 4 kazanan, ortalama %13,00, bileşik %60,8 — 2088957194892923386 (2026-08-16). "Close 52.95 < Alt 54.65 … Close 65.30 > Üst 65.10", işlemler +%23,3, +%2,3, +%19,4 — 2096379158561427848 (2026-09-05). Kanal hesabı yok. Kanal hareketi listesi TKFEN %20.97 … — 2019472075845513230.
- **R246** (80–100 hafta yatay): → 34 hafta (386.25–500.50), giriş 399, sonuç 1232 TL — 2045412174030352518 (2026-04-18). 30 hafta (3.11–3.30), "1 ayda %30" — 2091428244650147903 (2026-08-23). Haftalık 12 hafta örneği; alt bantta al, üst bantta sat, hacimli kırılımda kırılım yönü, fake breakout'ta ters yön — 1942087033247166573 (2025-07-07). **[AÇIK SORUYU KISMEN CEVAPLAR]**: pencere 30/34 hafta da kullanılmış; çıkış tanımı yine yok.
- **R039** (pivot çizgisi): → doğru uyumu R² (alt 0.9982, üst 0.9393) — 1904029830036775278 (2025-03-24). RSI trend çizgisi kırılımı "RSI: 44.61 > Trend: 41.67", tavan — 1909613017186119809 (2025-04-08).
- **R124 / R075 / R087** (düşen trend kırılımı): → lookback 90 gün (defterde 20 ve 30), "Eğim: -0.037773 (-2.16°)" — 2016214167884046802 (2026-01-27). Log fiyatta TP ≈3.864, SL ≈3.725 — 1875933436441161794 (2025-01-05).
- **R086 / R082** (range breakout): → DOAS 35 işlem, hepsi "Yukarı Kırılım", kâr küçük — 1914061902151290940 (2025-04-20). Teyit seti EMA5/8/13/34, son 60 gün Fibo (zirve 3,04, dip 1,73; 0,618 = 2,23), CDLCLOSINGMARUBOZU, sinyal perşembe, cuma tavan — 1926379754925556143 (2025-05-24).
- **R192** (demand zone): → "talep bölgesini kırmış olacak ve üzerindeki en az %10'luk alanda herhangi bir bearish fvg ve arz alanı olmayacak"; 12.73 = 11.57 × 1.10 "Temiz" — 2003587326036127830 (2025-12-23).
- **R129** (likidite): → "SSL YAPANLAR", tutma 10 işlem günü, NETAS 27.96 … ASUZU 6.47; Sweep_Kalite_Skoru 74–90 tanımsız — 2095236564909445352 (2026-09-02).
- **R263** (BOM): defterde "BOM'un ve şartların tanımı kayıtta yok". → "X bar kadar öteleyerek kodladım" (ileriye bakma önlemi; X yazılı değil) — 2093465820932235288 (2026-08-28). **[AÇIK SORUYU KISMEN CEVAPLAR]**

### Harmonik ve Elliott
- **R203** (harmonik TP): → PRZMA Kelebek (görsel doğrulandı) TP1 12.43, TP2 12.71, TP3 (C) 13.18, TP4 (Ext) 13.51, STOP 11.78. D ≈ 11.97 ile TP1 = D+0.382(C−D), TP2 = D+0.618(C−D), TP4 = D+1.272(C−D) tutar. Stop X altında değil D altında. Sonuç %13 — 2001060547618300157 (2025-12-16).
- **R080** (zigzag): → pivot eşiği sigma 0,015 / 0,02 / 0,025 — 1843421214317945155 (2024-10-07).
- **R008** (RSI kırılım etiketleri): → RSI düşen trend çizgisi, son 30 gün, RSI 30/50/70 — 1908933806221914328 (2025-04-06). RSI 1 yıl veri, son 60 gün düşen tepe çizgileri, kırılım tarihleri 2025-01-29, 02-07, 02-24, 03-04, 03-05 — 1909750908054823082 (2025-04-08).
- **R008**: → "çeşitli formasyonları bulan kodumuzun çıktısı", INTEM 21.55 … TMSN 4.41 — 2015504637198037346. Okuma hatası Bölüm 4'te.
- **R199** (W2 sınırı ve W3 hedefi): defterde "Maksimum: %78.6", hedef "(1. Dalga Boyu x 1.618) + Düzeltmenin Bittiği Yer". → UFUK (görsel doğrulandı): "Impulse (Start-1): +50.8% | 2. Dalga Düzeltmesi: -31.2% | 3. Dalga Hedef: 1557.96 TL". START ~838, 1 ~1263, 2 ~869.5 (10.10.2025 kapanış). Hedef formülü tutar. 2. dalga 1. dalganın ≈%92,5'ini geri almış; tarama %78,6 sınırını uygulamıyor — 1984349202730926414 (2025-10-31). **[AÇIK SORUYU CEVAPLAR — R199 W2 geri çekilme sınırı: araçta sınır uygulanmıyor]**
- **R207** (Elliott 5+3): → "Son Gün Eşleşti", itki bitiş 2025-07-03, düzeltme bitiş 2025-07-21 — 1947995611791290586; "SADECE EN SON GÜNDE TAMAMLANAN (C NOKTASI)", A1CAP tavan — 1948282706002903233; "Impulse #1: +66.8% | Corrective: -10.5%", %3,30 — 1983796730740273257; "Impulse #1: +36.7% | Corrective: -14.8%", tavan, "hala deneme süreçlerinde" — 1984331550519910770.
- **R261** (Elliott + demand): → kapanış 1. tepe (B) üstüne çıkınca "3. Dalga Başlangıcı", 2 günde %12 — 1949043393927024960. FADE: ELLIOT GİRİŞ 16.55; HEDEF 1 17.82, HEDEF 2 16.65, HEDEF 3 19.72; DEMAND 14.77–14.91; "DÜŞEN TREND | YENİ KIRILDI | TEMAS: 4"; sonraki yüksek 19.75 — 2095607708200169599 (2026-09-03).

### Göstergeler ve teyit
- **R053** (Bollinger): defterde ±2/±3 SD. → 3 SD; "üst banda yeşil mum ile temas edip ardından kırmızı mum kapatan" → sat; alt bantta kırmızı temas + yeşil kapanış → al; BB periyodu yok — 1845470513377824768 (2024-10-13), 1845850204395692110 (2024-10-14).
- **R131** (MA üstü/altı, "hangi MA belli değil"): → fiyat > WMA5/14/34/55 + RSI14 > 50 (@fiboborsa) — 1840770526240784672 (2024-09-30). WMA ve EMA ayrı dosya, kesişimde al/sat — 1840781392755527958 (2024-09-30). Kapanış > EMA5/14/34/55 ve RSI14 > 50; + CMF son 3 gün pozitif, önceki 3 gün negatif — 1847735111942336850 (2024-10-19). **[AÇIK SORUYU CEVAPLAR — hangi MA]**
- **R137** (CMF, "eşik verilmiyor"): → "CMF OSCILLATOR (21)" — 1845444032509468723 (2024-10-13). "Son 3 gün pozitif ve önceki 3 gün negatif ise al sinyali doğuyor." — 1845558544126366115 (2024-10-13). **[AÇIK SORUYU CEVAPLAR — CMF eşiği]**
- **R143** (gölge kodu): → hammer = "lower_shadow >= 2 * body_size and upper_shadow <= body_size * 0.3" — 1841562402501869780 (2024-10-02).
- **R167** (engulfing + EMA34): → IZINV 2025-05-05 %10, 05-06 %9,98; "istediğim yapı tam oluşmamışsa da bugün tavan vermiş" — 1919833559126127018.
- **R105** (MA eğimi): → SmaCross 30/100: getiri %339,26 vs B&H %947,13; yıllık %60,43; Sharpe 0,81; Max DD −%41,09; 7 işlem; win rate %28,57 — 1764270533158342937 (2024-03-03). EMA 50/200, maliyet 0,001; strateji net ≈4,2 vs piyasa ≈27 — 1837452465022615616 (2024-09-21).
- **R208** (kesişim/uyumsuzluk): → pozitif uyumsuzluk = Fiyat2 < Fiyat1 ve RSI2 > RSI1; TA-Lib formasyon sütunu — 1910777244735197251, 1910741892095942791 (2025-04-11). Klasik tanım + CDLINVERTEDHAMMER — 1910746399530164509. Tablo: RSI >30, MACD 0 altı pozitif, "EMA5 > EMA8 > EMA13 > EMA21" — 1911052570505736230. "Pozitif Uyumsuzluk #21", Stochastic 20/80 — 1954338937188622732.
- **R214** (EMA5>8>13 + destek teması): → 1 hafta INTEM %21.55, KBORU %14.12 … — 2015503511811719220; ATEKS %20.89 … INGRM 0.00 — 2020896982043123809; HLGYO %24.64 … — 2031773111981379623.
- **R217** (Fibo): → "fibo en yüksek ve en düşük kapanışa göre çekilmiştir"; 1 yıl; EMA 10/20/50/100/200 — 1842291706093355330 (2024-10-04).
- **R199 / R197** (0,786): → son 144 bar; bant %73,6–%83,6 — 1842318331891548280; bant %76,6–%80,6 — 1844077720344666261 (2024-10).
- **R221** (takas): → "takas ile yakalayıp momentum ile sömürmeye devam"; eşik yok — 1980334425599799633 (2025-10-20).
- **R224** (kısmi kâr): → K1 pozisyonun %50'si (%10.61 kazançta), K2 kalanın %50'si, kalan %25 iz süren — 1989778002805170214 (2025-11-15).

### Portföy, arbitraj, ölçüm
- **R074** (DEY, "hesap görselde değil"): → DEY_Potansiyel% = Dönem_Max / Başlangıç − 1; Toplam% = kapanış / başlangıç − 1 — 1969789658574868800 (2025-09-21). DEY_Marj_% = Donem_En_Yuksek / Baslangic_Kapanis − 1 (AZTEK 65.45/42.04 − 1 = %55.69) — 1983980494435033216. Referans başka tablolarda farklı (Bölüm 4). Katkı = ağırlık × getiri; 2026-05-20→06-01 MV kapanış %15.02, DEY %23.69; MS %8.66 / %18.37; BIST100 −%2.20 — 2061548118592647615. **[AÇIK SORUYU CEVAPLAR — DEY formülü]**
- **R110 / R137 / R181** (Markowitz, max Sharpe): → çalışılmış örnekler Bölüm 5'te. Ek kurallar: ana liste 10 hisse, odak liste 6 hisse — 2045205758904516748. Tek hisse %54.93 ağırlık getiriyi baskılamış, "Algoritmalar salt doğrular değildir." — 2046662359222243735. PASEU %55 ağırlık (R110 "%50 den fazla" ile uyumlu) — 2016165848713470411. Mum formasyonu süzgeci (R137 aşama 3) + 3 hisse max Sharpe — 2043416831029809199. 6 Ocak testi ilk 10 DEY: ALGYO %23.31 … ONCSM 1.74 — 2010064971888243034 (R181'in sonucunu verir).
- **R121** (Momentum+): → tek gün DEY EGPRO 9.97 … POLTK −1.82 — 2046302549956050950.
- **R101 / R099** (Z-skoru çift işlemi): → GSDDE/ALBRK log: giriş Z 3.86 / 2.28 / −2.09, kapanış Z 0.45 / 0.39 (görsel doğrulandı); net +%20.55, B&H +%41.94 — 2049470417522348366. Exit |Z| 0.13–0.19, Hold |Z| 0.50–1.14 (görsel doğrulandı) — 2021285630047559764. Hold bandı 1.800, 0.659 — 2022010682791883042. GEDIK/USAK Z 2,107 → "Short ETF1 / Long ETF2" — 1940885098364383483. Korelasyon 0.71 "BIST ortamında anlamlı" — 1862207567276962007. Üç korelasyon eşiği > 0.9 (fiyat, NEFK, net satış; 3 ay) → eşbütünleşme → Granger → spread → z — 1924868711116099887.
- **R251** (göreli değer rotasyonu): → KRDMD/ISDMR, Z ≤ −2 / ≥ +2; 3 işlem, net +%61.3 — 2052182649100263830.
- **R031** (VRP): → sektör rotasyonu → kârlı sektör → VRP < 0 hisselere eşit tutar; 6 hisse %10.04 — 2090165683132739919.
- **R002** (DuPont, "ölçüt yok"): → seçim ROE en yüksek + F/K düşük + fiyat 200 gün ortalama altı; beklenen kâr ile DuPont — 1914714348368359654. Adımlar: net kâr marjı, aktif devir hızı, aktif kârlılık, borç/kaynak, ROE — 1918035116988788982, 1920812975109116066. Aktif kârlılık = marj × devir hızı (TMSN 77.15 × 0.4453 = 34.36) — 1954935103194534196. Çok aşamalı filtre F/K 5-15 + 200 EMA altı — 1948004722608140442. Dupont + momentum faz — 1886875307187356067. Otomotiv 8 hisse örneği — 1919459834358841793. **[AÇIK SORUYU CEVAPLAR — R002 ölçütü]**
- **R061** (Merton, "formül görselde değil"): → E0 = A0N(d1) − De^(−rT)N(d2); σE = N(d1)σA A0/E0; amaç (E_est/3−1)² + (σE/0,8−1)²; örnek A0 12,395, σA %21,23, Pd 0,127 — 1851750265239609482 (2024-10-30). **[AÇIK SORUYU CEVAPLAR — Merton formülü]**
- **R052** (forward kur): → dört adım: faiz paritesi → Monte Carlo → risk primi → volatilite testi — 1966512882306179577 (2025-09-12).
- **R133** (HBK): → "AKBNK HBK = 8.147321153846153" (satır kalemleri adsız) — 1888364638825243071.
- **R179** (TOPSIS): → beş adım, 1'e en yakın en iyi; PyDecision, scikit-criteria — 2015048294649545183 (2026-01-24).

---

## 3. Çelişkiler

Karar verilmedi. "Olasılık" alanı kanıta dayanır.

| # | Gönderi (tarih) | Defter (yapıştırma tarihi) | Olasılık ve kanıt |
|---|---|---|---|
| Ç1 | 1786775182998171782 (2024-05-04): "RSI 30-70 riskli, sebeplerini zaten biliyoruz. Şöyle orta bant için yazalım bir formül." | R233 (2026-08-28): "RSI (14) değeri, 30 seviyesinin altından yukarı doğru keserek…"; "RSI 70 Reddi" | Tarihçe ya da bağlam. R233'ün söz tarihi belirsiz. Orta bant ayrı bir momentum taraması olabilir. |
| Ç2 | 1838978628757143953 (2024-09-25), görsel: "38.2% ENTRY", "61.8% SL" | R199 (2026-08-28): "Minimum: %50 Geri Çekilme (0.50) / İdeal (Golden Pocket): %61.8 - %65 Arası"; R197: "0.618 seviyesine … indiğinde … ALIM" | Bağlam olası: gönderi görseli genel bir şablon; key level ve fibo bacağı tanımsız. Güven orta. |
| Ç3 | 1844478606564806669 (2024-10-10): "SELL (OVERBOUGHT)", "BUY (OVERSOLD)"; 1844827048088424739 (2024-10-11): "-20 SELL (OVERBOUGHT)", "-80 BUY (OVERSOLD)" | R170 (2026-08-28): "Ön Koşul: Williams %R önce aşırı alım bölgesine (-20 ile 0 arası) girmelidir… -50 seviyesine değmeli ve buradan yukarı dönmeli." | Bağlam olası: gönderi ortalamaya dönüş, R170 momentum + pullback. İki ayrı sistem olabilir. 1844478606564806669 güveni düşük. |
| Ç4 | 1845212868955996539 (2024-10-12): "Hissenin geçmiş 20 yıllık verilerine bakarak aylık ortalama getirilerini buluyoruz." | R001 (2026-08-27): "Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın"; R106 (2026-08-27): "Ortalama (aritmetik ortalama), verideki en buyuk yalanci…" | Tarihçe olası: medyan ilkesi sonraki görüş olabilir; R001/R106 söz tarihi belirsiz. R183 olasılık (≥%70 yükselen ay) kullanır. |
| Ç5 | Monte Carlo Markowitz: 1887180923034120559 (2025-02-05) "monte carlo simülasyonu ile oluşturulan markowitz modeli"; 1888577330588561831 (2025-02-09) "bunları monte carlo simülasyonu ile yapacağız"; 1888577333059084322 (2025-02-09) "Her potansiyel portföy 100.000 kere simüle edilecek"; 1887871203114733973 (2025-02-07) "monte carlo simülasyonu ile oluşturduğumuz min varyanslı, yüksek alphalı portföyümüz"; 1922387739342721040 (2025-05-13) kod "weights[np.argmax(portf_results_df.sharpe_ratio)]" | R182 (2026-08-28): "Neden Monte Carlo Yerine 'Spicy' Model? … Bizim tercih ettiğimiz 'Spicy' yaklaşımı ise bu rastlantısallığı reddeder."; "Monte Carlo bir tahmin makinesidir, Spicy modeli ise bir denge mimarıdır." | Tarihçe en olası: beş gönderi 2025-02/05; R182 tercih değişimini anlatır. Kanıt: R182 Monte Carlo'yu açıkça "yerine" diye anar. |
| Ç6 | 1891144788633587887 (2025-02-16): "NEFK ve fiyatı artan bir şirketin yüksek korelasyonlu eşini bulun" (arbitraj devam gönderisinde) | R228 (2026-08-28): "Korelasyonun yüksek olması, istatistiksel arbitraj yapabileceğiniz anlamına gelmez." ; R262 (2026-09-06) eşbütünleşme | Tarihçe olası. 1924868711116099887 (2025-05-20) akışa eşbütünleşme ve Granger ekler. 1862207567276962007 (2024-11-28) yalnız korelasyon 0.71 kullanır. |
| Ç7 | 1850969302347989014 (2024-10-28), görsel: ORTALAMA FİYAT 143,98 = 0,4 × 159,39 (çarpan) + 0,6 × 133,71 (İNA) | R068 (2026-08-27): "En sonunda bu ortalamanın %60'ını, DCF'in de %40'ını alırım." (R064, R158 aynı) | Hata ya da bağlam. Ters ağırlık (0,6/0,4) 149,12 verir; görselle uyuşmaz. Kanıt yalnız hesap. |
| Ç8 | 1941620987495080092 (2025-07-05), görsel doğrulandı: "-1,93969 Pozisyon kapatıldı", "1,956796 Pozisyon kapatıldı" | R101 (2026-08-27): "Fark kapanıp Z-Skoru normale (0.5 seviyelerine) döndüğünde, pozisyonları kapatır" | Bağlam/sürüm olası: SAHOL/THYAO aracı ±2 bandına geri girişte kapatır. Sonraki araçlar 0.5 çevresinde kapatır: 2049470417522348366 (Z 0.45, 0.39), 2021285630047559764 (Exit |Z| ≤ 0.19). |

Toplam: 13 celisir satırı, 8 konu.

---

## 4. Gönderi içi hatalar ve defter okuma hataları

### 4.1 Defter okuma hataları (3)
- **R176** — 2018743366112985154 (2026-02-03): defter "slope, _, rvalue = linregress(...)"; gönderi "slope, _, rvalue, _, _ = linregress(np.arange(len(r)), r)". linregress beş değer döndürür; defterdeki biçim çalışmaz. Düzelt: defteri gönderi koduna çevir.
- **R074** — 2061554188832702624 (2026-06-01): defter "21–31 Mayıs 2026"; tablo açılış 2026-05-20, kapanış 2026-06-01. Düzelt: dönem 2026-05-20→06-01.
- **R008** — 2092340608480297126 (2026-08-25): defter Kelebek D'yi "11,29" okur; Kelebek görselinde "D: 11.20 [TAMAMLANDI]". 11.29, AB=CD grafiğindeki "D (hedef): 11.29 [TAMAM]" değeridir. Düzelt: iki değeri iki grafiğe ayır.

### 4.2 Gönderi içi formül ve hesap hataları
- **FRAMA kodu** — 1910723570654753121 (görsel doğrulandı): `FRAMA = alpha*(H+L)/2 + (1-alpha)*Close.shift(1)`. Standart FRAMA önceki FRAMA değerini kullanır (özyinelemeli). Kod önceki kapanışı kullanır. Neden: özyineleme yerine kaydırılmış seri yazılmış. Etki: çizgi düzleşmez, sinyal sıklığı artar (etkinin büyüklüğü belirsiz). Düzelt: `FRAMA[t] = alpha·Price + (1−alpha)·FRAMA[t−1]` döngüsü.
- **Çarpan/İNA ağırlığı** — 1850969302347989014: %40/%60 ile 143,98 çıkar; Tansu'nun yazdığı %60/%40 kuralıyla 149,12 çıkar (Ç7).
- **DuPont ROE** — 1954935103194534196: ROE = aktif kârlılık/(1 − borç/kaynak) tutmuyor (34.36/0.6603 = 52.04 ≠ 53.64).
- **DuPont sektör ortalaması** — 1919459834358841793: devir hızı 119.92 eşit ortalama; marj 4.60 ve aktif kârlılık 5.59 eşit ortalama değil. Dönemler karışık (DOAS, ASUZU, KARSN, TMSN 2024/12).
- **OTT** — 1790007806801621475: `f_var` tanımı kodda yok; kod tek başına çalışmaz.
- **Grid bot stop** — 1839389286518723008: stop oranı sabit değil (0,9236 ve 0,9566); 1943067673858052555 stop sabit fark 7.6629. Kural metinde yok; ATR tabanlı stop (1839747420302831898) ile açıklanabilir (belirsiz).
- **Harmonik/Elliott hedef sırası** — 2095607708200169599: HEDEF 2 (16.65) HEDEF 1'in (17.82) altında; hedef formülü yazılı değil.
- **Elliott W2 sınırı** — 1984349202730926414: W2 ≈%92,5; R199 en çok %78,6 der. Araç sınırı uygulamaz.
- **Elliott etiketleme** — 1948282706002903233: C noktası düzeltme dibi değil, B sonrası toparlanma tepesi; standart ABC'den farklı.
- **TP/SL** — 1875933436441161794: kırılım mumu ≈3.887, TP ≈3.864'ün üstünde; TP/SL hesabı yazılı değil.
- **VRP eşiği** — 2090165683132739919: kural "VRP < 0"; R031 görselindeki "AL eşiği (-0.005)" okumasıyla CEMTS (−0.0048) eşiği geçmezdi. R031 okunuşu da belirsiz.

### 4.3 Metin–görsel uyuşmazlıkları
- **Fincan-kulp görseli** — 1987938049582391791 (görsel doğrulandı): turuncu KULP eğrisi ~2 TL'ye iner; fiyat verisi bu aralıkta yok. Çizim hatası. Metindeki %4,43'ün anlamı belirsiz.
- **Elliott 3. dalga** — 1949043393927024960: metin 23.07 (2025) taraması der; görsel "3. Dalga Başlangıcı: 2024-07-23" ve x ekseni 2024. Metinde #hrgaz, görselde HURGZ.IS.
- **RSI periyodu** — 1840770526240784672: metin RSI14, görsel başlığı RSI21 > 50.
- **BIST getirisi** — 2097424225254441229: tabloda %1.79, metinde "+1.72".
- **UFUK sonucu** — 1984349202730926414 (görsel doğrulandı): metin "%150 falan"; görselde ~850 → ~2050, ≈%140. Küçük yuvarlama.
- **EMA 50/200 grafiği** — 1837452465022615616: strateji brüt ve net çizgisi çakışık; maliyet 0,001 görünmüyor.

### 4.4 Tanım tutarsızlığı (DEY referansı)
- DEY referansı tabloya göre değişir: başlangıç kapanışı (1983980494435033216), başlangıç açılışı (2011852408222081449: "Başlangıç Açılış → Bitiş Kapanış arası en yüksek"), önceki gün kapanışı (2015501247105642834: "ÖNCEKİ GÜN KAPANIŞINA GÖRE"). Karşılaştırmalı sonuçlarda bu fark gizli kalır.

---

## 5. Sonuç kanıtı (sinyal-sonucu gönderileri)

**Seçim yanlılığı:** Bu gönderiler Tansu'nun seçip paylaştığı sonuçlardır. Paylaşılmayan sinyal sayısı bilinmez. Paydası olan tek ölçümler: backtest tabloları ve tam liste getirileri. Başarısızlık da paylaşılmış: Vegas tüneli (1827794622434640093), SmaCross B&H altında (1764270533158342937), GSDDE/ALBRK B&H altında (2049470417522348366), THF tahmini tutmadı (2097060991586447371), TRGYO ağırlık "gol yemişiz" (2046662359222243735), CANTE kötü (1913126708485542223).

| Yöntem | Gönderi | Sonuçlar (birebir) |
|---|---|---|
| Min vol / max Sharpe portföy (R074/R110/R137) | 13 | 2043765223878754813: MV kapanış %14.23, DEY %18.54; MS %10.94/%17.09; BIST100 %8.66. 2044111449530802526: MV %3.31/%8.71; MS %9.35/%10.87; BIST100 %8.82. 2051364268826624017: %2.87/%8.60; BIST100 %0.41. 2061548118592647615: MV %15.02/%23.69; MS %8.66/%18.37; BIST −%2.20. 2097424225254441229 ve 2097430089407316222: MV +4.16, MS +5.72; BIST 1.79. 2043388046674968916: %14.65/%20.72. 2043411371417620696: %36.58/%38.22; BIST100 %5.45. 2043416831029809199: %45.65/%50.20. 2090488532989096315: %10.22/%13.05; BIST100 %1.90. 2046662359222243735: %3.33/%4.25; BIST100 −%0.76. 2016165848713470411: PASEU ≈%10 marj. 2045205758904516748: gün içi DEY GZNMI 9.97 … 2.14. 2061554188832702624: "%23 marj", BIST −2.20. |
| Liste + DEY marjı (momentum, trend desteği, kanal, formasyon) | 13 | 2010064971888243034: ALGYO %23.31 … ONCSM 1.74. 2011852408222081449: ULKER 8.26, ULAS 8.53, EKOS 4.35, ATAKP 16.87. 2015501247105642834: INTEM %21.55 … AFYON 3.76. 2015503511811719220: INTEM %21.55 … TRCAS %10.25. 2015504637198037346: INTEM 21.55 … TMSN 4.41. 2019470774617141660: BURVA %20.98 … YONGA −0.17. 2019472075845513230: TKFEN %20.97 … KRDMA 2.00. 2020896982043123809: ATEKS %20.89 … INGRM 0.00. 2031771168647090313: DOGUB %29.47 … EDATA 3.41. 2031773111981379623: HLGYO %24.64 … CRDFA 2.57. 2031774785504481621: AYCES %29.83 … INFO 1.00. 2033584293843239328: ARASE %21.44 … CLEBI 1.77. 2046302549956050950: EGPRO 9.97 … POLTK −1.82. 1969789658574868800: TUKAS Toplam −15,46 / DEY 3,86. Not: DEY dönem en yüksek fiyattır; gerçekleşen getiri değildir. |
| Bayrak/flama, takoz | 11 | 1941224929585922368 %8; 2031773880533053751 "%3.5 yaparmış"; 2086820537137795283 tavan; diğerleri (1949523572512481441, 1953166070279209345, 1953506333476430012, 1954565115233140772, 1964740931346968931, 1984306004855505136, 1993022005516619970) oran yazmaz, grafik yükselişi gösterir; 2031774785504481621 liste (yukarıda). |
| Çift Z-skoru / göreli değer | 7 | 2049470417522348366: net +%20.55, B&H +%41.94. 2052182649100263830: 3 işlem, net +%61.3. 2021285630047559764: "%5 hiç birşey yapmadan". 2022010682791883042: GEREL ~16 → ~26. 1940885098364383483: GEDIK −%9,95, USAK primli. 1941620987495080092: THYAO long sürüyor (oran yok). 1862207567276962007: CMBTN −%5,37, MRSHL −%2,73. |
| Elliott | 7 | 1947995611791290586 "patladı" (oran yok); 1948282706002903233 tavan; 1949043393927024960 2 günde %12; 1983796730740273257 %3,30; 1984331550519910770 tavan; 1984349202730926414 "%150 falan" (görsel ≈%140); 2095607708200169599 HEDEF 3 aşıldı (≈%19.3). |
| Rolling Sharpe tepkisi | 4 | 1 tavan + 2 iyi getiri (1905345708858749109); METRO %5 (1905219676352676212). |
| RSI uyumsuzluk / RSI kırılımı / RSI-Fibo | 8 | 1909613017186119809 tavan; 1910750627728175106 "%8'e yakın"; 1911052570505736230 ve 1910746399530164509 sinyal (oran yok); 1954338937188622732 "Getisini de yaptı"; 1912136481751056753 MERKO +9,95, TMPOL +7,46, FRIGO +1,45, KENT 0,00, ULKER −1,61; 1912108045154271672 MERKO tavan, TMPOL %4; 1977423987274617023 sonuç yok. |
| Harmonik | 2 | 2001060547618300157 %13; 2092340608480297126 D hedefleri tamamlandı. |
| Fincan-kulp | 1 | 1987938049582391791: hedef 42.90; metin %4,43 (anlamı belirsiz). |
| Yatay bant (N hafta) | 2 | 2045412174030352518: 399 → 1232 TL; 2091428244650147903: "1 ayda %30". |
| Fon getiri tahmini | 2 | THF +1.05% tahmin, "gerçekleşmedi"; DOH +1.54%, "nokta atışı" (gerçekleşen yazılı değil). |
| Diğer tekil | 10 | 1913126708485542223 BB+Keltner ENERY %4, MACKO %3.5, CANTE kötü; 1919833559126127018 IZINV %10 + %9,98; 1926379754925556143 cuma tavan; 1859342666175218082 KNN, VİOP +0.25; 2090165683132739919 VRP %10.04; 1985453771279757653 DUNYH 121,10 → ~145; 1917567412125274471, 1908437183423209509, 1783470138877997162, 1844743398047064231 oran yok; 1980334425599799633 oran yok; 1887871203114733973 CEOEM en yüksek ağırlık (oran yok); 1850969302347989014 "ORTALAMA GETİRİ 96,8%" (hedef potansiyeli). |

Al-tut karşılaştırması olan gönderiler: 1764270533158342937 (%339,26 vs %947,13), 1827794622434640093 (≈4,35x vs ≈5,4x), 1837452465022615616 (≈4,2 vs ≈27), 2049470417522348366 (%20.55 vs %41.94), 2052182649100263830 (+%61.3; B&H yazılı değil). Üçünde strateji al-tutun altında.

---

## 6. Defter için öneri listesi (öncelik sırası)

İlk 10 maddenin görselden gelen parametrelerini görseli açıp doğruladım; uyuşmazlık yok. Tek ek bulgu: FRAMA kodunun özyinelemesiz formülü (madde 7) ve fincan-kulp görselindeki kulp çizimi (madde 3).

**Grup A (1–5)**
1. **ekle** — Rolling Sharpe tepkisi: 21 gün, hisseye özgü seviye (−0.40, −0.6), "önceki < seviye < son" kuralı; seviye seçimi açık soru. Kaynak: 1905152595586318386, 1905219676352676212, 1905345708858749109, 1905153170805776426.
2. **ekle** — Fon akışı ve fon riski ailesi: getiri tahmini (ağırlık × getiri, VİOP katkısı, reconciliation 0.7789), 20G para akışı, fon pozisyon değişimi, Fund Risk Radar bileşenleri. Kaynak: 2097060991586447371, 2097065200687915032, 2095922815329263677, 2096343856476496081, 2097551651838034055, 2099970636386812395, 2099814980212134159.
3. **genişlet** — R114: hedef = KIRILMA + (KIRILMA − fincan dibi); defterin açık sorusunu kapatır. Kaynak: 1987938049582391791.
4. **genişlet** — R199: araç W2 %78,6 sınırını uygulamıyor (≈%92,5 örnek); W3 hedef formülü çalışılmış örnekle doğrulandı. Kaynak: 1984349202730926414.
5. **genişlet** — R101/R099: çıkış eşiği iki sürüm (±2 bandına geri giriş ≈1,95 / |Z| ≈ 0,4–0,5); Hold bandı; B&H kıyası. Kaynak: 1941620987495080092, 2049470417522348366, 2021285630047559764, 2022010682791883042, 2052182649100263830.

**Grup B (6–10)**
6. **ekle** — Stochastic %K/%D kodu (14, 3; 20/80 Güçlü AL/SAT). Kaynak: 1897565005811183722.
7. **ekle** — FRAMA (period 16, alpha = exp(−4.6(D−1)), 0.01–1); kod notu: önceki FRAMA yerine önceki kapanış kullanılmış. Kaynak: 1910723570654753121.
8. **ekle** — Altman Z (1.2/1.4/3.3/0.6/1.0; 1.81 / 2.99) ve Bathory (C tanımsız); kaynak kitap sayfası. Kaynak: 1890148860330406128.
9. **genişlet** — R203: PRZMA çalışılmış örnek (TP1 12.43, TP2 12.71, TP3 13.18, TP4 13.51, STOP 11.78; stop D altında). Kaynak: 2001060547618300157.
10. **ekle** — Supertrend 7/3 kodu ve OTT 30/7.0 kodu; türevler (10/3–3/10 + RSI 55/45, EMA5/20 + Supertrend). Kaynak: 1839989044693922032, 1790007806801621475, 1860416194953543908, 1852011542746714531.

**Grup C (11–15)**
11. **genişlet** — R074: DEY formülü (Dönem_Max / Başlangıç − 1) ve referans tutarsızlığı (açılış / kapanış / önceki kapanış); dönem düzeltmesi 2026-05-20→06-01. Kaynak: 1969789658574868800, 1983980494435033216, 2011852408222081449, 2015501247105642834, 2061554188832702624.
12. **genişlet** — R137 / R131: CMF(21), "son 3 gün pozitif, önceki 3 gün negatif"; fiyat > EMA/WMA 5/14/34/55 + RSI14 > 50. Kaynak: 1845444032509468723, 1845558544126366115, 1847735111942336850, 1840770526240784672.
13. **ekle** — AKD konsantrasyon ailesi (TOP2/5/10, %50+ ilk kurum, sınıf eşikleri, takip çıkış kuralı). Kaynak: 1964443262544232634, 1966795896651477361, 1964450520560808209, 1964749763922038906, 1939003175484133714.
14. **ekle** — RSI üzerine Fibonacci (haftalık kod, 144 gün 0.786/0.618 dönüşü, EMA 89 filtresi). Kaynak: 1839043892399735295, 1912136481751056753, 1977423987274617023, 1862203614174888388, 1861794132093554798.
15. **genişlet** — R002: DuPont adımları ve seçim (ROE yüksek + F/K 5-15 + 200 EMA altı); ROE formül uyuşmazlığını not et. Kaynak: 1914714348368359654, 1918035116988788982, 1954935103194534196, 1948004722608140442.

**Grup D (16–20)**
16. **genişlet** — R061: Merton formülleri ve çözüm amaç fonksiyonu, çalışılmış örnek. Kaynak: 1851750265239609482.
17. **ekle** — Grid bot (0.4 grid, 50 lot, 10 seviye, 2×ATR14 stop). Kaynak: 1839747420302831898, 1839389286518723008, 1943067673858052555.
18. **ekle** — Vegas tüneli 12/144/169 kuralı ve DOAS sonucu (al-tutun altında). Kaynak: 1838671862420975657, 1783135314036376019, 1827794622434640093, 1844743398047064231.
19. **genişlet** — R143 / R224: hammer kodu (alt gölge ≥ 2×gövde, üst gölge ≤ 0,3×gövde); K1 %50, K2 kalanın %50'si, %25 iz süren. Kaynak: 1841562402501869780, 1989778002805170214.
20. **genişlet** — R246 / R004 / R245: pencere 30/34 hafta, kanal backtesti (4/4, %13,00), AL Close < Alt / SAT Close > Üst. Kaynak: 2045412174030352518, 2091428244650147903, 2088957194892923386, 2096379158561427848.

**Grup E (21–25)**
21. **genişlet** — R192 / R124 / R039: +%10 temiz alan şartı; lookback 90 gün ve eğim; R² ile çizgi uyumu. Kaynak: 2003587326036127830, 2016214167884046802, 1904029830036775278.
22. **çeşitlendir** — Parabolic SAR ailesi (SMA 20/40 + ilk PSAR barı; ADX/ADXR, Momentum, 10 bar hacim). Kaynak: 1864259354800578906, 1862635048819650793, 1862617662196473882, 1950999922742010108.
23. **çeşitlendir** — Bollinger–Keltner sıkışması (R053/R082 çeşidi); R053'e 3 SD mum kuralı. Kaynak: 1913989895674028279, 1955389232639512999, 1845850204395692110.
24. **genişlet** — R207 / R261: Elliott tarama ölçüleri (Impulse %, Corrective %, son gün eşleşmesi), FADE hedefleri. Kaynak: 1983796730740273257, 1984331550519910770, 1948282706002903233, 2095607708200169599.
25. **çeşitlendir** — Kanal orta noktası kırılımı. Kaynak: 1914173637898236379, 1914210602513236459, 1917567412125274471.

**Grup F (26–30)**
26. **çeşitlendir** — Adı defterde olmayan mum formasyonları (TA-Lib CDL listesi, adsız delici kod, Tasuki Gap). Kaynak: 1847942480169222236, 1899964404872941880, 1910750627728175106.
27. **çeşitlendir** — Portföy türevleri: Black-Litterman, VIF kontrolü, Return_Risk_Ratio, profit factor > 3. Kaynak: 1797263557978890521, 1821204747614831017, 1985453771279757653, 1908666927045886118.
28. **ekle** — Nicel model fikirleri (Radon-Nikodym kodu, Avellaneda-Stoikov, Merkez Bankası botu). Kaynak: 1911126829710073960, 1911703064748216597, 1913122317263057042.
29. **çeşitlendir** — Adaptif MA ve stop adları (KAMA, MAVİLİMW, MOST, Ichimoku, StochRSI, ROC). Kaynak: 1852811907666714936, 1943066690709070008, 1844079823829991777, 1840861807633973669, 1853470102810669319, 1841597392178536580.
30. **ekle** — Fikir düzeyi tekiller (PCA hedef endeks, KNN, LSTM, grafik ölçeği, Bull/Bear %75). Kaynak: 1771536925809135885, 1859342666175218082, 1862165685440245988, 1953201892202307992, 1950279832119472221.

**Düzeltme notları (öncelik dışı, defter bakımı)**
- R176, R074, R008 okuma hatalarını düzelt (Bölüm 4.1).
- Çelişkiler Ç1–Ç8'i "tarihçe/bağlam" notuyla ilgili R kaydına bağla; özellikle Ç5 (R182 öncesi Monte Carlo dönemi) ve Ç8 (çift işlemi çıkış sürümleri).
