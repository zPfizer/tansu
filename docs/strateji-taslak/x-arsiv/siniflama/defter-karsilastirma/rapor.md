# X arşivi ↔ Tansu defteri (R001–R263): karşılaştırma raporu (07.10.2026)

Kapsam: kuralı "yok" olmayan 3.075 X gönderisi (birlesik-v5.jsonl, tarama ve kod düzeltmeleri işlenmiş). Her gönderi
defterin 741 fikir satırıyla anlamca eşlendi (36 parça, her parça bir Opus ajanı). Sonra 6 tema özeti, 4 bağımsız
denetim. Ayrıntı tema belgelerindedir; bu dosya özet ve karar listesidir.

## Sayılar (denetim düzeltmeleri işlenmiş, sonuc.jsonl)

| İlişki | Sayı | Anlamı |
|---|---|---|
| çeşitlendirir | 1.099 | defterdeki fikrin türevi |
| aynı | 980 | defterde zaten var |
| genişletir | 540 | defterdeki fikre eşik, formül, kod ya da örnek ekliyor |
| bilgi | 270 | strateji katkısı yok |
| yeni | 110 | defterde ne yöntem ne aynı amaçlı fikir var |
| çelişir | 76 | defterdeki bir kuralla çelişiyor |

Defterde adı geçmeyen yöntem taşıyan satır (yeni + adı defterde olmayan türev): 677.
Tema belgelerindeki öneri sayısı: 204 (tema-1: 46, tema-2: 27, tema-3: 35, tema-4: 33, tema-5a: 33, tema-5b: 30).

## Denetim

1. Çelişki satırlarının hepsi (79): doğru 54, zayıf (bağlam farkı) 22, yanlış 3, alıntı hatası 0. Yanlış 3 satır
   düzeltildi (denetim-celisir.jsonl).
2. Örneklem (80 satır: 30 yeni + 50 rastgele): ilişki 75/80, R 71/80, katkı 76/80, "adı defterde" 72/80.
   En sık hata eksik R. 5 ilişki ve 8 R düzeltildi (denetim-orneklem.jsonl).
3. Kalan 135 "yeni" satırı iki denetçiye verildi: 51'inde defterde aynı amaçlı fikir bulundu (denetim-yeni-1/2.jsonl).
   İki denetçinin ölçüsü farklı sıkılıkta (biri 14/68, öteki 37/67 değiştirdi; ör. Black-Scholes birinde "yeni",
   ötekinde R006 türevi). Bu yüzden "defterde olmayan yöntemler" listesi yeni ile adı defterde olmayan türevleri
   birlikte sayar; ölçü farkı bu listeyi değiştirmez.
4. Sınır: 76 çelişkinin 9'u yalnız "M" yazarlı defter kayıtlarına dayanır (LLM biçimli kartlar; ör. R182, R185,
   R199, R225). Bu 9'da Tansu'nun kendi X gönderisi daha birinci elden olabilir.
5. Sınır: defter başlık tarihi (2026-08/09) Levent'in kayıt tarihidir. Tansu'nun sözünün özgün tarihi bilinmez.
   "Hangisi sonra" sorusu çoğu çelişkide kesin değildir.

## En önemli 10 bulgu

1. **Değerleme ağırlığı ters.** 2023-08–2024-04 tabloları ve TTRAK metni "çarpan %40, İNA %60"
   (1708030356564160854: "Çarpanlar %40, İNA %60 ağırlıklandırılarak"). Hesap tutar: TTRAK
   0,4×785,30 + 0,6×2.116,93 = 1.584,28; SAYAS 0,4×159,39 + 0,6×133,71 = 143,98 (ters ağırlık 1.317,95 ve
   149,12 verir, tutmaz). Defter R068/R151/R158 "çarpan %60, İNA %40"; R158 gerekçe yazar ("piyasa ne der sorusu …
   daha bağlayıcı"). 2024-10 planı da %60/%40. Değişiklik büyük olasılıkla 2024 içinde (tema-4.md).
2. **Gartley tarama kartları R222/R203'e uymuyor.** Kart sayıları oran değil, bacak fiyat farkı; Fibo çizgisi
   D − r×|CD|. ARENA AB/XA 0,70 ve D < X; 6 kart daha; KUYAS (2026-08) (A−D)/XA 0,88. Uyan tek kart PETKM.
   Tarayıcı kartlardan kopyalanırsa defter kuralı bozulur (tema-2.md).
3. **Defterin açık sorularına cevaplar.** R184: stop 2×ATR (2005227814875021373, video 1999481868106826013).
   R114: fincan-kulp hedefi = kırılım + (kırılım − dip) (GUBRF 300,75 + 88,55 = 389,30; PRKAB 33,70 + 9,20 = 42,90).
   R074: DEY formülü. R181: amaç fonksiyonu max Sharpe + min vol (tema-3, tema-5b, tema-1).
4. **Defterde olmayan büyük aileler** (satır sayısı yaklaşık; aile adına göre gruplandı): mum formasyonları
   (TA-Lib, Tasuki, Marubozu …) ~61; fon akışı ve fon riski ~39; opsiyon fiyatlama ~38; RSI türevleri (RSI-Fibo)
   ~28; AKD/takas ~27; Golden/Death Cross ~23; Supertrend ~21; Vegas tüneli ~20; RoC/ADX ~18; MOST/OTT ~17;
   PSAR ~15; rolling Sharpe ~12.
5. **Fon analizi tam bir alan.** Tasfiye günü = (çıkış TL × ağırlık) / (0,20 × 20G medyan TL hacim); stresli gün =
   normal gün / kullanılabilir hacim katsayısı (11,12 / 0,05 = 222,40); Erken Uyarı Skoru; Fund Risk Radar 0–100
   (tema-5a, tema-5b).
6. **Tam parametreli girişler.** EMA5/10 → EMA20 kesişimi + MACD > sinyal + RSI14 50'yi yukarı keser + 5G OBV > 0;
   CMF 6 gün (son 3 > 0, önceki 3 < 0); Qullamaggie kırılımı (hacim 2–3×, RSI > 60); Weinstein 2. aşama
   (tema-1, tema-3).
7. **Çift işlem hattı netleşiyor.** Korelasyon > 0,7 (BIST için 0,71) → Engle-Granger (p < 0,05 ve Tv < Cv) →
   Z ±2 giriş; çıkış iki sürümde (|Z| ≈ 1,95 ve |Z| 0,4–0,5). Pair Health: 30/60/90G korelasyon, beta kararlılığı,
   yarı ömür (tema-4, tema-5b).
8. **Tansu'nun kendi hesap hataları (kopyalanmamalı).** Yıllık oynaklık "×252" (doğrusu √252), √255, fiyatın std'si;
   kur değişiminde payda S_t; Black-Scholes kodunda öncelik hatası (d1 yalnız T=1'de doğru); DtD kodunda
   market_cap = fiyat × 1.000.000; FRAMA özyinelemesiz; delta hedge'de hisse × delta (doğrusu hisse / |delta|)
   (tema-4, tema-5a).
9. **Tekrarlayan çelişki konuları.** Monte Carlo ↔ R182 (4+ gönderi, 2025); HMM ↔ R091; eşbütünleşme şartı ↔ R228
   (p 0,136'da "risk kabul"); "dipte yakalamak" ve düştükçe alım ↔ R172/R257; emir defteri derinliği ↔ R225
   (Tansu'nun kendi ölçümü R225'in tersini bulur); Williams %R −20 ↔ R170.
10. **Kesişim stratejileri al-tut'un gerisinde.** TUPRS SMA 30/100: %339, al-tut %947. XU100 SMA 35/240: %369,
    al-tut %786; Tansu'nun kuralı "tek tepe değil, komşuları da kârlı sağlam bölge". GSDDE/ALBRK çift: %20,55,
    al-tut %41,94. Sonuç gönderileri seçilmiş başarılardır; seçim yanlılığı var.

## Defterde bugün düzeltilen okuma hataları (5)

| Kayıt | Eski | Yeni | Kanıt |
|---|---|---|---|
| R014 (defter-1) | "TP2 (.618 CD)", "Bk Stop (X)" | "TP2 (.618 AD)", "İlk Stop (X)"; Fibo 144,20 … 20,60 | 2091220738510332198 görseli; 47,05 + 0,618×97,15 ≈ 107,09 |
| R164 (defter-3) | "bileşik büyüme" | kodda üs birikir; yıl 5 = 5000×1,017^15 = 6.438,49 | 2036840358210945219 |
| R176 (defter-3) | `slope, _, rvalue = linregress(...)` | not: X'te `slope, _, rvalue, _, _ = …` | 2018743366112985154 |
| R008 (defter-1) | Kelebek "D: 11,29" | "D: 11.20 [TAMAMLANDI]"; 11.29 AB=CD hedefi | 2092340608480297126-3 görseli |
| R074 (defter-2) | "21–31 Mayıs" | 20 Mayıs – 1 Haziran | 2061554188832702624 tablosu |

R014 düzeltmesi iliskiler.md, izlenebilirlik.md, tasarim-8.md, kurallar/C-harmonik-geometri.md ve
strateji-modulleri-taslak.md'ye de işlendi (eski okuma "üç TP çapası" belirsizliği yaratıyordu; gerçekte iki: AD, CD).
Bu formülleri kullanan Python kodu yok. Çözülmeyen: R068 "3.028.232.000" ↔ R062/X "3,028,332,000"; iki değer de
aynı hedef fiyatları verir (91,33 / 177,61 / 120,53), sonuca etkisi yok.

## Kod bağlantıları

73 bağlantı denendi: indirildi 3, süresi dolmuş 63 (çoğu we.tl), 404 5, korumalı 1, hata 1 (baglanti/baglanti-sonuc.jsonl).
Tansu'nun kendi kod dosyalarının hiçbiri bugün indirilemiyor; kodu yalnız gönderi metni ve görselindedir.
İndirilenler başkalarına ait: @algotrader06 Drive (15 ipynb + 5 Pine/metin; Tansu "övdü"), mfrdixon/ML_Finance_Codes
(55 dosya), awesome-ai-for-economists (README).

## Dosyalar

- sonuc.jsonl: 3.075 satır, her gönderi için ilişki, R, yöntem, "adı defterde", katkı, kanıt, denetim notu.
- tema-1.md (seçim, momentum, rejim), tema-2.md (bölge, formasyon), tema-3.md (teyit, giriş, çıkış, risk),
  tema-4.md (değerleme, portföy, çift), tema-5a.md (ölçüm, ilke, eğitim), tema-5b.md (ürün hedefi, sinyal sonucu).
- karsilastirma-01..36.jsonl (ham), girdi-01..36.jsonl, ek-yontem-01-12.jsonl, denetim-*.jsonl, defter-fikir.txt.

## Açık iş

1. Defter önerilerini (204) deftere işlemek. Bu, defterin yeni sürümüdür; Levent'in onayıyla yapılır.
2. Değerleme ağırlığı kararı: tasarımda 2026 kuralı (%60 çarpan) esas, eski oran tarihçe. Karar Levent'in.
3. @algotrader06 dosyalarını defterle eşlemek.
4. Tema belgelerinde ilişkiler denetim öncesi sayılara göre yazıldı; 51 "yeni" → türev düzeltmesi belgelere
   işlenmedi (sonuc.jsonl'de işli).
