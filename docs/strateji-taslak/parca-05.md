# Parça 05: gorsel-paket-44 – 85 (not + görsel okuması)

Durum: TAMAM (paket 44–85, 42 paket, 56 görselin 56'sı açıldı). Not: paket 71–74 notları "rapor" türünde (Cevo yazısı), Tansu'nun kendi sözü değil; görsel ayrıca okundu.
Okuma kuralı: görsel esas; notla çelişirse işaretlendi. "1. el" = Tansu'nun kendi aracının görseli. "2. el" = nottaki Claude/Levent aktarımı.

## 1. Paket tablosu

| Paket | Tür | Görsel | Tek satır |
|---|---|---|---|
| 44 gizli filtre breakout | aday giriş (şartname YOK) | 1/1 | Uzun taban, Point A→B kutusu, B kırılımı, sonra dik yükseliş; iki filtre açıklanmamış. |
| 45 BALAT AB=CD negatif delta | filtre/negatif örnek | 1/1 | BUY AB=CD D etiketi + düşen fiyat + negatif kümülatif delta: Tansu "her zaman çalışmaz" diyor. |
| 46 sağlıksız yükseliş | risk/rejim uyarısı | 1/1 | Mavi çizgi sıfırı yukarı keserken kırmızı rejimdeyse yükseliş geri verilir. Formül yok. |
| 47 Lindsay Trident | giriş (harmonik) | 1/1 | D = (B×C)/A; B kırılımı devam tetiği; D sonrası Fib/trailing. |
| 48 SMRTG fiyat+vol birlikte artış | piyasa/hisse filtresi (pozisyon çarpanı) | 1/1 | Fiyat ve vol birlikte artarsa pozisyon çarpanı Tam→Defansif. Formül yok. |
| 49 sağlıklı yükseliş | aynı filtrenin aynası | 1/1 | Fiyat çıkarken mavi seri sıfır altında kalırsa sağlıklı. Formül yok. |
| 50 BIST100–BIST_VOL scatter | strateji değil | 1/1 | Log getiri scatter, V biçimli ilişki; espri. |
| 51 CIMSA–OYAKC rotatif | giriş (çift rotasyonu) | 1/1 | Z ±2, "momentum dönüş onaylı", +%49,2. |
| 52 AGROT–GARAN mtm | giriş (çift, stat-arb) | 3/3 | 3 işlem: Z ±2 giriş, Z 0,37 çıkış; +%13,44 (20.04.2026). |
| 53 stat-arb bağ kopuşu | negatif backtest (çift) | 1/1 | Çift belirtilmemiş; strateji ≈79 bin TL'ye iner. |
| 54 stat-arb kanonik | giriş (çift) | 3/3 | Aynı AGROT–GARAN sistemi, 23.04.2026 özeti +%8,76 / B&H −%3,55. |
| 55 volatilite+arbitraj favori | aynı çift sistemi | 1/1 | AGROT.IS–GARAN.IS backtest + spread Z; tarih/değer ekseni okunamadı. |

## 2. Aday modül kartları (44–55)

### K-05-01 Gizli filtre breakout (Point A / Point B)
- Tür: giriş (şartname yok); şu hâliyle strateji değil.
- Kaynak: paket 44, `01-point-a-b-gizli-filtre-breakout.png`. Levent aktarımı + 1. el görsel.
- Tansu'nun ifadesi (görsel): "Point A (Start)", "Point B (Breakout)". Nottaki cümle (2. el): "Hep göz önünde olan 1–2 filtreyle enteresan breakout sinyali var".
- Kurallar: YOK. Filtreler açıklanmamış. Görselde: uzun yatay mavi kesikli kutu, B'de yeşil üçgen, sarı kısa ortalama, mavi noktalı iz süren seri. Sembol, tarih, ölçek okunamadı.
- Tansu'nun sonucu: yok; B'den sonra dik yükseliş görselde var, rakam yok.
- Veri: günlük OHLCV (bilinmiyor, zaman dilimi okunamadı).
- Belirsizlik: filtre kimliği, parametre, evren, zaman dilimi, kaç deneme.
- Uygulanabilirlik: **X** (şartname yok). Önceki okumayla aynı ("gizli filtre" X).

### K-05-02 AB=CD başarısızlığı: katılım vetosu (BALAT)
- Tür: filtre / negatif örnek (K-C ailesi AB=CD ile birleşir).
- Kaynak: paket 45, `01-balat-abcd-negatif-kumulatif-delta.jpg`. 1. el görsel + Levent notu (2. el).
- Tansu'nun ifadesi (görsel başlık): "BALAT | Düşen Direnç Kıran + Talep + Fibo + ABCD | Fiyat: 75.95 | Kırılım: 2026-05-15 | Temas: 3 | Lookback: 30"; etiket "D(CD=1.27AB)"; alt panel "Küm. Delta". Not "Kırılım 2026-05-19" yazıyor; görselde 05-15 okundu (küçük yazı, **olası çelişki**, görsel esas).
- Kurallar: Fib seviyeleri görselde: 1.000 | 99.45, 0.786 | 94.00, 0.618 | 89.73, 0.500 | 86.72, 0.382 | 83.72, 0.236 | 80.01, 0.000 | 74.00. Yeşil talep çizgisi yaklaşık 69–70. EMA 5/8/13 + "Direnç TL". Stop/hedef/giriş tetiği yok. Ders: ABCD geometrisi tek başına alım nedeni değil; fiyat düşerken kümülatif delta uzun süre negatif.
- Sonuç: BALAT geçici başarısızlık örneği; getiri rakamı yok.
- Veri: kümülatif delta için tick/emir akışı gerekir; günlük OHLCV yetmez (proxy gerekir).
- Belirsizlik: delta nasıl hesaplanıyor (proxy mi gerçek mi), eşik yok.
- Uygulanabilirlik: **X** (veto kuralı sayısız değil). AB=CD girişine "olumsuz örnek" fikstürü olarak girer.

### K-05-03 Mavi çizgi sıfırı yukarı keser + kırmızı rejim (sağlıksız yükseliş)
- Tür: risk/rejim uyarısı (yeni long engeli).
- Kaynak: paket 46, `01-mavi-sifir-kesisi-kirmizi-rejim.png`. 1. el görsel, aracın kimliği belli değil.
- Tansu'nun ifadesi (görsel): "Mom Eşiği (0.15)", "Sıfır (0.0)". Not (2. el): "mavi çizgi sıfırı yukarı kestiği anda kırmızı bölgede oluşan yükselişler büyük oranda geri gelir".
- Kurallar: olay = mavi seri sıfırı yukarı keser VE kırmızı gölgeli rejim açık. Etki: yükseliş geri verilir (nota göre). Mavi/turuncu seri formülü, kırmızı rejim formülü, alt yeşil durum serisi: okunamadı / kaynakta yok. Eşik 0,15 yalnız lejanttan.
- Sonuç: yok (tek grafik, sembol ve tarih yok).
- Veri: günlük OHLCV olasıdır ama formül bilinmediği için belirsiz.
- Uygulanabilirlik: **X**.

### K-05-04 Lindsay Trident (ABC, B kırılımı, D hedefi)
- Tür: giriş (harmonik/geometri) + hedef formülü.
- Kaynak: paket 47, `01-abc-b-kirilimi-trident-d.png`. Görsel 1. el, formül ve tarihsel atıf Levent tweet metninden (2. el).
- Tansu'nun ifadesi (görsel): "B Kırılımı" (yatay kesikli), "D (CD=1.27AB)", kırmızı kutu içinde A, B, C. Metin: D = (B×C)/A; "Charles Lindsay 1976 Trident/Zıpkın" (atıf doğrulanmadı).
- Kurallar: A düşük → B yüksek → C daha yüksek dip. D hedefi C'de hesaplanır. Giriş tetiği (aday): kapanış B kırılımının üstünde, D'ye devam. D sonrası: Fibonacci hedef merdiveni + iz süren stop (yöntem kaynakta yok). Pivot ayarı, tolerans, stop: yok.
- Sonuç: görselde D etiketi 1,27AB ve sonra geri çekilme. Rakam yok.
- Veri: günlük OHLCV yeterli.
- Belirsizlik: D=(B×C)/A ile görseldeki "CD=1.27AB" aynı değer mi, ham A/B/C yok; hangi yön trade'i (BIST'te açığa satış yok).
- Uygulanabilirlik: **K**. Önceki okuma (Trident K) ile uyumlu.

### K-05-05 Fiyat + volatilite birlikte artış / sağlıklı yükseliş (pozisyon çarpanı)
- Tür: hisse/piyasa filtresi (pozisyon büyüklüğü çarpanı Tam / Defansif).
- Kaynak: paket 48 (`01-smrtg-fiyat-vol-birlikte-artis-defansif.jpg`), paket 49 (`01-fiyat-yukari-mavi-sifir-altinda.png`). Görsel 1. el, anlatım 2. el.
- Tansu'nun ifadesi (görsel 48): alt panel "Pozisyon Büyüklüğü Çarpanı", seviyeler "(Tam)" ve "(Defansif)"; orta panel "Kırılma Eşiği (0.0)", mor noktalı eşik ≈ +0,2; üst panel SMRTG ≈ 18 → 6–8 TL, sağ uçta sert yükseliş; yeşil gölge = Tam durumu görünüyor. Not: "fiyatla volatilitenin aynı anda artması genellikle kötü sonuçlanır; sistem pozisyonu kapattı, defansife geçti". 49: "fiyat çıkarken mavi çizgi sıfırın altına iner ve oralarda gezinir: sağlıklı yükseliş; quant strateji farklı görmektir".
- Kurallar: mavi seri > 0 ve fiyat yukarı → Defansif (çarpan düşer / pozisyon kapanır). Mavi seri < 0 ve fiyat yukarı → sağlıklı. Mavi/turuncu serinin formülü, pencere, çarpan değerleri (Tam=? Defansif=?): okunamadı / yok. Aday (not, doğrulanmadı): fiyat getirisi ile Δvol'un yuvarlanan korelasyonu.
- Sonuç: yok.
- Veri: Δvol için gerçekleşen vol (günlük OHLCV) olabilir; kimlik belirsiz.
- Uygulanabilirlik: **X** (formül yok). Önceki okumada "mavi çizgi" X; uyumlu.

### K-05-06 Rotatif Z-skor çift portföyü (CIMSA / OYAKC)
- Tür: giriş (çift rotasyonu, long-only, hep yatırımda).
- Kaynak: paket 51, `01-cimsa-oyakc-rotatif-portfoy-zskor.jpg`. **1. el** (Tansu aracının dashboard'u, açıklamasız iletilmiş).
- Tansu'nun ifadesi (görsel): panel başlıkları "1- Fiyat Yakınlaşması (Normalize)", "2- Portföy Performansı | Net: +49,245 TL (+49.2%)", "3- Z-Skoru ve Momentum Dönüş Onaylı İşlemler | SON GÜN: YENİ AL SİNYALİ". Lejant: "Buy & Hold (50/50)", "Rölatif Momentum Portföyü", "Başlangıç", "Aşırı Ucuz CIMSA Sınırı (+2.0)", "Aşırı Ucuz OYAKC Sınırı (-2.0)", "CIMSA Tutulan Dönemler", "OYAKC Tutulan Dönemler". Etiketler: "OYAKC AL", "CIMSA AL".
- Kurallar: Z ≈ +2'de "CIMSA AL" (CIMSA ucuz), Z ≈ −2'de "OYAKC AL". Başlıktaki "Momentum Dönüş Onaylı" ifadesi Z dönüşü (ΔZ) kuralıyla uyumlu; ΔZ formülü görselde yok. Ortada 50/50 B&H kesikli. Başlangıçta nakit (yatay yeşil çizgi, yaklaşık 2025-01…2025-05), sonra hep bir hissede görünüyor. Z formülü, pencere, ΔZ eşiği, stop, maliyet: okunamadı. Tarih ekseni ≈ 2025-01 … 2026-05.
- Sonuç: Net +49,245 TL (+%49,2), başlangıç ≈ 100.000 TL (aritmetik). Görselde son gün Z ≈ +2'de yeni AL. Başlangıç sermayesi ve maliyet görselde yazmıyor.
- Veri: günlük OHLCV yeterli (iki hissenin kapanışı).
- Belirsizlik: Z formülü, pencere, maliyet, "net" ifadesi.
- Uygulanabilirlik: **K**. Önceki okuma (+%49,2) ile uyumlu; Z'nin üretilememesi görselde de formül bulunmadığı için doğal.

### K-05-07 AGROT–GARAN istatistiksel arbitraj (Z ±2, nakit, çıkış |Z|≈0,4)
- Tür: giriş + çıkış (çift, iki bacak olarak anlatılıyor).
- Kaynak: paket 52 (3 görsel), 54 (3 görsel), 55 (1 görsel), 53 (negatif, çift belirtilmemiş). 1. el: özet tablo, işlem logu, günlük döküm, "Stat-Arb Performans Özeti". 2. el: metin anlatımı (eşbütünleşme, "ucuz long, pahalı short").
- Tansu'nun ifadesi (görsel 52-01): "STAT-ARB ÖZETİ | AGROT ↔ GARAN", "Tarih: 2026-04-20 | Durum: AKTİF LONG (AGROT Ucuz)", Başlangıç Sermayesi 100,000.00; Güncel Portföy Değeri 113,436.14; Net Kâr/Zarar 13,436.14; Strateji Getirisi +13.44%; Buy & Hold Getirisi +0.91%; Toplam Sinyal/İşlem 3. İşlem logu (52-02): "AL/SAT İŞLEM LOGU": 2025-12-12 "AGROT SAT, GARAN AL" Z 2.05 Portföy 100,000.00; 2026-02-16 "POZİSYON KAPAT (Nakit)" Z 0.37 Portföy 92,354.65; 2026-03-09 "AGROT AL, GARAN SAT" Z −2.01 Portföy 92,354.65. Görsel 54-03: "STAT-ARB PERFORMANS ÖZETİ (2025-04-01 - 2026-04-23)", "Çift: AGROT / GARAN", Strateji Getirisi +8.76%, Buy&Hold Getirisi −3.55%, Toplam İşlem Sayısı 3, "Güncel Pozisyon: 1 (Z-Skor: −0.91)"; grafikler "1) Fiyat Yakınlaşması (Başlangıç=100)" ("GARAN (Endeks/X)", "AGROT (Hisse/Y)"), "2) Portföy Performansı", "3) Z-Skoru ve Dinamik Sinyaller"; dosya "StatArb_Islem_Logu_AGROT_GARAN.xlsx". 55: başlık "İstatistiksel Arbitraj Backtest | AGROT.IS & GARAN.IS", alt panel "Spread Z-Skoru" (tarih ve değer ekseni okunamadı).
- Kurallar: giriş |Z| ≥ 2 (görsel: 2,05 ve −2,01; kesikli çizgiler ±2). Z > +2: AGROT SAT, GARAN AL. Z < −2: AGROT AL, GARAN SAT. Çıkış: Z normale döner (görselde çıkış Z = 0,37; eşik değeri yazmıyor; not "0,5 çevresi" diyor, 2. el). Çıkışta nakit. İlk 21 takvim günü nakit. Stop: yok. Spread/Z formülü, pencere, hedge oranı, kaldıraç: okunamadı.
- Sonuç: işlem 1: 2025-12-12→2026-02-16, 100.000→92.354,65 (−%7,65). İşlem 2: 2026-03-09'dan açık; 20.04.2026'da 113.436,14 (işlem +%22,83). Günlük döküm: 17.04 NAV 102.389,21, 20.04 NAV 113.436,14 (+11.046,93 TL tek gün). Sütun başlıkları (A..G) görselde kesik; B ≈ 130–146, C ≈ 2,76–3,55 (hangi hisse olduğu okunamadı).
- **Çelişki/uyarı:** iki özet farklı tarihte: 20.04.2026 +%13,44 ve 23.04.2026 +%8,76; B&H +%0,91 ve −%3,55. Aynı açık işlem için üç günde NAV değişimi; ikisi de görsel. Dönem başlangıcı 54'te 2025-04-01 yazıyor; 52'de yazmıyor.
- Veri: günlük OHLCV yeterli (iki kapanış). Açığa satış BIST'te bireysel için yok; bacak yapısı (long-short mı, tek bacak rotasyon mu) görselden kanıtlanmıyor. Önceki okuma (D dosyası) 52'nin 29 günlük PnL tablosundan regresyonla yaklaşık long AGROT ≈ 0,97×NAV, short GARAN ≈ 0,38×NAV buldu (YORUM, R²=0,96); benim kaba elle denemem eşit TL long-short'a da tam long-only'ye de oturmadı, yani 1:0,4 tahminiyle çelişmiyor. Bacak yapısı görselde yazılı değil.
- Belirsizlik: bacak yapısı, ağırlık, maliyet, Z formülü ve penceresi, çıkış eşiği.
- Uygulanabilirlik: **K**. Kural önceki okumada "AGROT–GARAN rotasyon değildir (iki bacak + nakit)" diye geçiyor; görsel logu "SAT/AL" ikilisi gösteriyor ama pozisyon yapısını kanıtlamıyor. İşaret: Z>+2 ⇒ GARAN(X) AL; CIMSA görselinde de Z>+2 ⇒ X AL; işaret sözleşmesi iki görselde tutarlı.

### K-05-08 Çift stratejisi negatif örnek (53)
- Tür: negatif backtest fikstürü (çift rotasyonu/stat-arb).
- Kaynak: paket 53, `01-statarb-negatif-backtest-bag-kopusu.jpg`. 1. el görsel; çift ve dönem belirtilmemiş.
- Tansu'nun ifadesi: lejant "Buy & Hold (Başlangıç 100,000 ₺)", "Stat-Arb Stratejisi", başlık "2) Portföy Performansı (TL)". Not: "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım; görünmez bağ kopmuş olabilir".
- Sonuç (görsel okuma, yaklaşık): strateji 100.000 → ≈79.000 TL (≈ −%21) ve yatay; B&H tepe ≈125 bin, sonda ≈105–107 bin. Tarih okunamadı.
- Uygulanabilirlik: kart yok; K-05-06/07 için "bağ kopma" örneği. Not: önceki okuma "bağı kopan çift ≈−%21" diyor; uyumlu.

## Strateji olmayan paket (tek satır)
- Paket 50: BIST100 ve BIST_VOL log getirileri scatter; X ekseni −0,20…+0,18, Y ekseni −0,4…+0,7; V biçimli dağılım; strateji değil, volatilite şoku fikrine bağlam.

---

## BÖLÜM 2: paket 56–66

### Paket tablosu (56–66)

| Paket | Tür | Görsel | Tek satır |
|---|---|---|---|
| 56 A1CAP Weinstein 4 evre | piyasa/hisse filtresi (evre) | 1/1 | Fiyat+hacim, H/L/LH/LL/HH/HL etiketleri, sarı uzun ortalama; evre kuralı yok. |
| 57 TEKTU–EREGL ağırlık | strateji değil (portföy ağırlık duyarlılığı) | 1/4 (özet tablo) | 01.04–22.04.2026: XU100 %50/TEKTU %30/EREGL %20 → +%17,23. |
| 58 GUBRF fincan-kulp | giriş + hedef | 1/1 | Kırılım 300,75, hedef 389,30, R/R 1:2,27, sinyal 2025-10-24. |
| 59 B&H vs sinyal scorecard | strateji değil (rapor tablosu) | 1/1 | Getiri +%21,54 / +%14,74; vol %33,16 / %23,21; MDD −%2,46 / −%1,72; Sharpe 9,477. |
| 60 gizli pozitif uyumsuzluk | giriş (trend devamı) | 2/2 | Fiyat higher low, osilatör lower low; "Swing=15 sol-only, MinGap=15"; 5 günde %29 (2. el). |
| 61 gizli uyumsuzluk takip | aynı fikir (watchlist) | 1/1 | Aynı geometri, yeşil üçgen/sarı nokta anlamı bilinmiyor. |
| 62 FROTO Corwin–Schultz | piyasa/hisse filtresi (spread+sigma) | 1/1 | Spread ve sigma ile rejim; ort. spread %1,7990 (nottan farklı). |
| 63 BIST 12 ay momentum decile | tarama/sıralama | 1/1 | Anlatım: 12 aylık getiri, 10 grup, üst decile 1 ay; görsel yalnız DEY tablosu. |
| 64 düşen direnç kırılımı + talep | giriş | 1/1 | Direnç TL kırılımı, talep bandı, hacim, EMA 5/8/13. Sembol yok. |
| 65 ICBCT EMA sıkışması | giriş (Pre Signal) | 2/2 | EMA20/50/100/200, "Pre Signal"; parametre özel; "bir günde %5" (2. el). |
| 66 ALKIM Fib+VP+VWAP+delta | confluence (strateji değil) | 2/2 | Fib 0,786, POC/VAH/VWAP, DMI, delta; "bir ayda %20". |

### K-05-09 Weinstein 4 evre (A1CAP)
- Tür: piyasa/hisse filtresi (evre sınıflaması); kural yok.
- Kaynak: paket 56, `01-a1cap-fiyat-hacim-dort-evre.jpg`. 1. el görsel (Tansu aracı), evre anlatımı 2. el (Levent metni).
- Tansu'nun ifadesi (görsel): tek grafik "Tarih / Hacim"; fiyat üzerinde H, L, LH, LL, HL, HH etiketleri; kırmızı/yeşil basamaklı dinamik çizgi; sarı uzun ortalama; turuncu hacim ortalaması. Metin (2. el): "Piyasanın 4 Evresi": taban/birikim, yükseliş, tepe/dağıtım, düşüş.
- Kurallar: evre sınır formülü, ortalama periyodu (sarı çizgi), "X haftalık eğri": okunamadı / yok. Görselde: 2024–başı 2025 fiyat ≈ 4–6 bandında yatay, hacim kurur; 2025 ortası hacimli kırılım; HH ≈ 19 ve geri çekilme ≈ 14.
- Sonuç: yok (anlatı örneği).
- Veri: haftalık (nota göre) OHLCV yeterli; kural olmadığı için üretilemez.
- Uygulanabilirlik: **X** (evre kuralı yok). Etiket sözlüğü (H/L/HH/HL/LH/LL ve kırmızı/yeşil basamak çizgi) olası bir pivot yapı taşı.

### K-05-10 GUBRF fincan-kulp (cup & handle)
- Tür: giriş + hedef.
- Kaynak: paket 58, `01-gubrf-fincan-kulp-fibo-kirilim-hedef.png`. **1. el görsel** (Tansu'nun tarama sistemi).
- Tansu'nun ifadesi (görsel başlık): "GUBRF — Formasyon Tamamlanma: 2025-10-28 | Risk/Reward: 1:2.27". Lejant: "Fiyat", "FİNCAN", "KULP", "Fibo Bitişi: 317.00", "Fibo Başlangıç: 212.20", "Kırılım Sinyali". Etiketler: "KIRILMA: 300.75", "HEDEF: 389.30", "SİNYAL! 2025-10-24".
- Kurallar (görselden): Fib (R=317,00 → B=212,20): %0 317,00; %23,6 292,27; %38,2 276,97; %50 264,60; %61,8 252,23; %78,6 234,63; %100 212,20. Kırılım çizgisi 300,75. Hedef = kırılım + fincan derinliği: 300,75 + (300,75 − 212,20) = 389,30 (görsel rakamlarıyla tutuyor). R/R 1:2,27 → stop görselde yok; ima edilen ≈ 261,7 (benim aritmetiğim; 264,60'a yakın). Fincan = mavi yay (Mart–Eylül 2025), kulp = turuncu yay.
- Tansu'nun sonucu: fiyat hedefi aştı; görselde son bölgede ≈ 470'e yakın (okuma yaklaşık). Sinyal etiketi 24.10.2025 ile "formasyon tamamlanma" 28.10.2025 arası tarih çatışması başlıkta görünüyor.
- Veri: günlük OHLCV yeterli (zaman dilimi okunamadı; Mart 2025–Mart 2026 ekseni).
- Belirsizlik: fincan/kulp dedektörü, kulp derinliği (metin %50–61,8 diyor; görselde kulp dibi ≈ 240, yani %61,8 altında), stop.
- Uygulanabilirlik: **K**. Önceki okuma ile uyumlu (hedef = kırılım + derinlik; R/R 1:2,27).

### K-05-11 Gizli pozitif uyumsuzluk (hidden bullish divergence)
- Tür: giriş setup'ı (trend devamı).
- Kaynak: paket 60 (2 görsel), 61 (1), 74 (sonraki bölümde). 1. el aracın ekranı; "5 günde %29" Levent metni (2. el).
- Tansu'nun ifadesi (görsel 60-01): etiket "… | Swing=15 sol-only | MinGap=15". Fiyat panelinde mavi çizgi iki dibi birleştirir (higher low); alt panelde kırmızı kesikli çizgi iki osilatör dibini birleştirir (lower low). Görsel 60-02: sağda yaklaşık 5 yeşil mum, ölçek ≈ 540 → 690 (≈ +%28, nottaki %29 ile uyumlu; kesin giriş/çıkış yok). Görsel 61: aynı geometri, yeşil üçgen ve sarı noktalar, anlamları bilinmiyor.
- Kurallar: fiyat dibi2 > dibi1, osilatör dibi2 < dibi1; önceki trend yukarı. Swing=15 ("sol-only": yalnız sol 15 bar) ve MinGap=15 (aralık, birim bilinmiyor). Osilatör kimliği, giriş tetiği, stop, hedef: okunamadı / yok.
- Sonuç: 5 günde yaklaşık %29 (seçilmiş tek örnek, sembol ve tarih yok).
- Veri: günlük OHLCV yeterli; osilatör bilinmiyor (görselde fiyat≈0,21 seviyeli çizgi).
- Belirsizlik: osilatör, sol-only yeniden çizim riski, giriş.
- Uygulanabilirlik: **K** (parametre var, osilatör ve tetik yok). Önceki okuma ile uyumlu.

### K-05-12 Corwin–Schultz spread + sigma rejimi (FROTO)
- Tür: hisse filtresi (likidite/volatilite rejimi); bir "uzak dur / geniş stop" kuralı.
- Kaynak: paket 62, `01-froto-corwin-schultz-spread-sigma.png`. 1. el görsel; yorum kuralları 2. el.
- Tansu'nun ifadesi (görsel): "Corwin-Schultz Spread Tahmini — FROTO.IS"; panel başlıkları "Corwin-Schultz Bid-Ask Spread (%, 21g rolling)", "Volatilite Tahmini (Sigma %)"; üst blok: "Ortalama Spread : 1.7990%", "Medyan Spread : 0.7841%", "Max Spread : 9.8494% (2025-04-14)", "Min Spread : 0.0000% (2024-01-31)", "Ortalama Sigma : 2.1133%". Grafikte "Ort: 1.799%".
- **Çelişki:** not ortalama spread'i `%1,7909` yazıyor; görsel `1,7990` (iki rakam yer değiştirmiş). Görsel esas.
- Kurallar (2. el, nottan): spread yüksek + sigma yüksek → uzak dur / geniş stop; spread düşük + sigma yüksek → yön savaşı trend lehine; spread normale dönünce güven artar. Eşik sayısı kaynakta yok (ortalama %1,79 yalnız istatistik). Hesap: ardışık günlük High/Low (Corwin–Schultz).
- Sonuç: yok (Ocak–Nisan 2026 FROTO yorumu; fiyat ≈ 90–95 → 125).
- Veri: günlük OHLCV yeterli.
- Uygulanabilirlik: **K** (hesap belli, eşik yok). Veri notu: istatistik penceresi (min 2024-01-31) görünen grafikten (≈ 2025 Nisan–2026) uzun.

### K-05-13 BIST 12 aylık momentum decile (tarama/sıralama)
- Tür: tarama/sıralama (cross-sectional momentum).
- Kaynak: paket 63, `01-bist-momentum-dort-ay-dey-tablosu.jpg`. Kural anlatımı **2. el** (Levent tweet aktarımı); görsel yalnız DEY tablosu.
- Tansu'nun ifadesi (görsel): sütunlar "Hisse | Baslangic | Bitis | Referans_Fiyat | Bitis_Kapanis | Donem_En_Yuksek | DEY_Marj_%"; 20 satır, dönem 2025-12-31 – 2026-04-20; tüm "Bitis_Kapanis" = NaN; ilk satırlar NIBAS.IS 3.62 → 11.60 (%220.44), DOGUB.IS 48.46 → 146.50 (%202.31), TMPOL.IS 290.25 → 703.00 (%142.20), son satır POLTK.IS 9982.50 → 10235.00 (%2.53).
- Kurallar (not, 2. el): her ay son 12 ay getirisine göre 10 eşit grup; en yüksek grup eşit ağırlık, bir ay tut; yeniden sırala; 2015'ten bugüne, 500+ hisse. Atlama ayı, ağırlık, maliyet kuralı yok. Anlatılan sonuç: üst grup yıllık getiri ve Sharpe'ta ilk (rakam yok).
- Sonuç (görsel): DEY = dönem en yükseği / referans − 1; gerçekleşmiş getiri değil (Bitiş kapanışı NaN). Not: tablo "dört aylık getiri" değil, ileriye bakan en yüksek fiyat marjı.
- Veri: günlük OHLCV, 500+ hisse, ölü hisse dahil evren gerekir (survivorship).
- Uygulanabilirlik: **K** (kural basit ve net ama 2. el; Tansu'nun kendi sayısal çıktısı yok, görsel kanıt değil).

### K-05-14 Düşen direnç kırılımı + talep + hacim + EMA 5/8/13
- Tür: giriş (kırılım).
- Kaynak: paket 64, `01-dusen-trend-talep-hacim-ema-breakout.jpg`; ilişkili paket 45 (BALAT başarısız örnek). 1. el aracın ekranı.
- Tansu'nun ifadesi (görsel): lejant "EMA 5", "EMA 8", "EMA 13", "Direnç TL"; kırmızı düşen çizgi, yeşil yatay talep bandı, alt panel hacim. Not: "Pazartesi bakalım" (sonuç açık).
- Kurallar (görselden): kapanış düşen direnç çizgisinin üstünde; son mum uzun yeşil, hacim görünür en yüksekler arasında; fiyat talep bandı içinde/üstünde; EMA 5/8/13 sıkışık ve yukarı kıvrılıyor. Çizgi çapaları, temas sayısı, talep bandı kuralı, stop, hedef: görselde yok. BALAT başlığındaki "Temas: 3 | Lookback: 30" ve LIDER "Lookback 20" parametreleri bu aile için (paket 45 ve önceki okuma).
- Sonuç: yok (sembol, tarih okunamadı).
- Veri: günlük OHLCV yeterli; talep bandı tanımı yok.
- Uygulanabilirlik: **K**. Önceki okuma ile uyumlu.

### K-05-15 EMA sıkışması pre-signal (ICBCT)
- Tür: giriş (setup/uyarı).
- Kaynak: paket 65, `01-icbct-ema-sikisma-pre-signal.png`, `02-matrix-sonraki-mum.png`. 1. el ekran; "bir günde %5" Levent metni (2. el). Aynı aile KRDMD (paket 67).
- Tansu'nun ifadesi (görsel 65-01): üst çubuk "ICBCT | Son Kapanış: 14.55 | Son 130 Mum | … | 1 periyot | ▲1 BULL ▼0 BEAR ⚡0 CONFLICT"; lejant "EMA20 (14.44)", "EMA50 (14.29)", "EMA100 (14.31)", "EMA200 (14.42)"; mavi kutu "▲ AKTİF 3g" (kısmen okundu); "Pre Signal" oku; alt paneller kapatılmış/özel. Görsel 65-02: matrix ekranında sonraki yeşil mum, cyan düşen referansa yaklaşıyor.
- Kurallar: EMA seti 20/50/100/200 görselde birebir. Aralık (14,44 − 14,29) / 14,42 ≈ %1,04 (benim aritmetiğim; KRDMD'deki %1,2 eşiğin altında kalır). Pre Signal tetiği, özel parametreler: gizli, okunamadı. Giriş, stop, hedef: yok.
- Sonuç: "bir günde %5" yalnız metin; görselde rakam yok.
- Veri: günlük OHLCV olasıdır; zaman dilimi okunamadı ("1 periyot").
- Uygulanabilirlik: **K** (EMA seti ve sıkışma ölçüsü belli; tetik yok, önceki okumada da böyle).

### K-05-16 ALKIM Fib + hacim profili + VWAP + DMI + delta confluence
- Tür: confluence (strateji değil).
- Kaynak: paket 66, iki görsel. 1. el ekran + Levent metni.
- Tansu'nun ifadesi (görsel 66-01 başlığı): "ALKIM - ADVANCED MARKET ANALYSIS (VWAP + Volume Profile + Delta + AMT + FIBONACCI)"; küçük yazı: Fiyat 31.00, VWAP 28.00, POC 29.71, VAH 30.24 (nottan; görselde çözünürlük düşük, okunamadı kısmen). Alt paneller: hacim, +DI/−DI, delta, kümülatif delta.
- Kurallar: yok; "Fib 0,786 ve direnç aşımı, POC/VAH/VWAP üstü, +DI üstünlüğü, pozitif delta" bir liste.
- Sonuç: görsel 66-02: mor çizgi sonrası ≈ 30 → 35–36 (≈ +%20), sonra geri çekilme; giriş/çıkış işareti yok.
- Veri: delta için tick; VP için gün içi (günlük proxy sınırlı).
- Uygulanabilirlik: **X**.

### Strateji olmayan veya tek satırlık paketler (56–66)
- Paket 57: TEKTU/EREGL ağırlık duyarlılığı ve %50/30/20 portföy özeti (+%17,23; pasif +%17,00; aktif−pasif +226,97 TL); strateji değil. (Yalnız 03 açıldı; 01/02/04 not tablosuyla okundu.)
- Paket 59: B&H vs "sinyal bazlı strateji" scorecard; görsel metrikleri notla uyumlu; "Yorum" sütunu (Tansu aracı çıktısı gibi değil, LLM benzeri yorum) var; strateji kuralı yok; vol, MDD ve getirinin ≈ %70 ölçeği (benim aritmetiğim) risk çarpanı olasılığı.

---

## BÖLÜM 3: paket 67–85

### Paket tablosu (67–85)

| Paket | Tür | Görsel | Tek satır |
|---|---|---|---|
| 67 KRDMD EMA sıkışması | giriş/setup (1. el, en net) | 1/1 | EMA20/50/100/200, tolerans %1,2, min 3 gün; 17.12.2025–14.01.2026 (20 gün), ort. oran %0,64. |
| 68 XU100 EMA50/100/200 + KDE | piyasa durumu / yapı | 1/1 | EMA yakınsaması, KDE tepe fiyatları (11292,07 kırılımı), boğa dizilimi. |
| 69 PRZMA bullish FVG | yapı taşı (FVG) + giriş fikri | 1/1 | FVG bölgeleri alt tarafta; "doğrudan long yerine 1H/4H CHoCH". |
| 70 haftalık Gravestone Doji | çıkış/risk uyarısı | 1/1 | Parabolik yükseliş tepesinde uzun üst gölge mumu; "kaç". |
| 71 Dragonfly Doji + EMA sıkışması | giriş adayı (rapor türü not) | 1/1 | Mart–Nisan taban, EMA kümesi; görselde doji etiketi yok. |
| 72 HBK U dönüşü | strateji değil (temel) | 1/1 | Fiyat ve yıllıklandırılmış HBK, bilanço beklentisi. |
| 73 ASUZU finansal borç | strateji değil (temel) | 2/2 | Borç YoY %83,9, otomotiv ort. %38,7. |
| 74 özel subplot gizli pozitif uyumsuzluk | giriş setup'ı (osilatör özel) | 1/1 | "Son: 1578.00 ₺ | Getiri: +63.4% | β = 0.132" etiketi; formül gizli. |
| 75 ISCTR A/D–EMA | giriş/çıkış (long/short durum) | 1/1 | Strateji %19,1, B&H %10,8, Sharpe 0,67, MDD ≈ −%17; opt1=3. |
| 76 mum geometri motoru | ortak yapı taşı (kod örneği) | 1/1 | open/high/low/close, üst/alt gölge hesabı; dört satır örnek. |
| 77 ASUZU bottom-up değerleme | strateji değil (değerleme) | 1/1 | FK ve FD/FAVÖK hedefleri; 2023 tam yıl; hedef ≈ 119,74 TL, güncel 41,00 TL. |
| 78 PETKM confluence | confluence/arz-talep (kural yok) | 1/1 | Talep (yeşil), arz (kırmızı), Fib, EMA 8/21, hacim; fiyat 19,88. |
| 79 ARCLK ara dönem | strateji değil (değerleme) | 1/1 | FK 177,59, FD/FAVÖK 184,22, ort. 180,90; güncel 120,00. |
| 80 FROTO FK/FD-FAVÖK | strateji değil (değerleme) | 1/1 | FK hedef 796,03; FD/FAVÖK 1441,67; ort. 1118,85; güncel 800,00. |
| 81 FROTO basit FK | strateji değil | 1/1 | 5 adımlı FK hedefi 796,03. |
| 82 EREGL DCF 10 yıl | strateji değil | 4/4 | WACC %22,19 (görsel), DCF 22,69 TL, güncel 16,67, potansiyel %36,1. |
| 83 EREGL tek tuş DCF | strateji değil | 1/1 | Konsol çıktısı; firma değeri 79.423, hisse başı 22,69. |
| 84 DCF varsayım riski | strateji değil | 1/1 | Yalnız tarihsel girdi tablosu; sensitivity çıktısı görselde yok. |
| 85 APO mean-reversion | giriş (prototip) | 1/1 | Fast10/Slow40 EMA, buy/sell işaretleri; kural ve sembol yok. |

### K-05-17 EMA sıkışması KRDMD (parametre ve oran, 1. el)
- Tür: giriş/setup; en net birinci el parametreler. (K-05-15 ICBCT ile aynı aile.)
- Kaynak: paket 67, `01-krdmd-20gun-ema-sikisma-ratio.jpg`. **1. el** görsel.
- Tansu'nun ifadesi (görsel): "Tespit edilen sıkışma periyodu: 1 / 1. 2025-12-17 -> 2026-01-14 (20 gün) Ort.Ratio: %0.64"; başlık "KRDMD | Son 130 Mum | EMA Sıkışması | Tolerans %1.2 | Min 3 gün | 1 periyot"; lejant "EMA20 (31.92)", "EMA50 (30.74)", "EMA100 (29.58)", "EMA200 (28.43)"; sarı kutu "20g %0.64"; "Son Kapanış: 36.68"; alt panel "Ratio %" ve kırmızı "Eşik %1.2".
- Kurallar: oran ≤ %1,2 ve en az 3 gün art arda; ratio formülü görselde yazmıyor (önceki okuma çözmüş: (max EMA − min EMA)/EMA200). Giriş, stop, hedef: yok. Metin (2. el): periyot ve eşik "tasarımcının tecrübesine göre". Gün sayısı 20: tarih aralığı 17.12→14.01 = 20 işlem günü civarı (takvim 28 gün).
- Sonuç: sıkışma sonrası fiyat ≈ 26–28 bandından 36,68'e (grafikte yaklaşık; kesin giriş yok). Sağ uçta ratio ≈ 12.
- Veri: günlük OHLCV yeterli ("1 periyot" = günlük olduğu görselden kesin değil).
- Uygulanabilirlik: **H** (setup ölçüsü), giriş tetiği **K/yorum**. Önceki okuma ile uyumlu.

### K-05-18 EMA50/100/200 yakınsaması + KDE tepe fiyatları (XU100)
- Tür: piyasa durumu filtresi / yapı (EMA yakınsaması + KDE seviyeleri).
- Kaynak: paket 68, `01-xu100-ema50-100-200-kde-hacim.jpg`. 1. el görsel; yorum 2. el.
- Tansu'nun ifadesi (görsel): "XU100 Son 150 Mum ve KDE Tepe Fiyatları"; "Son Kapanış: 14587.90"; EMA 50 (13310.99), EMA 100 (12840.90), EMA 200 (12256.37); yatay KDE seviyeleri 14235.93, 13834.87, 13590.93, 12979.01, 12379.48, 11292.07, 10911.69, 10518.30 (son rakam görselde .90/.30 ayırt edilemedi). Kırmızı kutu 2025 sonu EMA'ların yakınlaştığı yer (≈ 11.000–11.200).
- Kurallar: KDE'nin girdisi, bant genişliği, tepe seçimi: görselde yok. Kırılım = fiyatın KDE tepesini hacimle geçmesi (2. el). Sıra EMA50>EMA100>EMA200 sonrası genişleme.
- Sonuç: 11.292 civarı kırılım sonrası 14.4xx tepe, 12.600–13.200 düzeltme, 14.587,90.
- Veri: günlük OHLCV (KDE: kernel yoğunluk tahmini).
- Uygulanabilirlik: **K** (yapı taşı olarak kullanılabilir; kural yok).

### K-05-19 Bullish FVG revisit (PRZMA)
- Tür: yapı taşı (FVG) + giriş fikri (2. el).
- Kaynak: paket 69, `01-przma-bullish-fvg-bos-ema.jpg`. 1. el görsel; yorum 2. el.
- Tansu'nun ifadesi (görsel): "PRZMA | Fiyat: 17.70 | Price Action & Smart Money Analysis"; lejant "Fiyat, EMA 9, EMA 21, EMA 50, EMA 100, EMA 200, Swing Points, Hacim"; etiketler HH, LH, HL, LL; fiyat altında çok sayıda yeşil yatay bant (FVG adayı), 2025 başı–2026. Metin: "mıknatıs", "doğrudan long yerine 1H/4H CHoCH".
- Kurallar: FVG = üç mum (c1 high < c3 low), görselde bant sınırları okunamadı. Giriş: FVG üst sınırına ilk temasta alarm; sonra alt zaman dilimi CHoCH teyidi (nota göre). OTE/Fib bölgesi tanımsız. Stop/hedef yok.
- Veri: giriş için 1H/4H gün içi; günlük ile FVG tespit edilebilir, giriş tetiği edilemez.
- Uygulanabilirlik: **K** (FVG tanımı mekanik; tetik gün içi veri ister).

### K-05-20 Haftalık Gravestone Doji (çıkış/risk uyarısı)
- Tür: çıkış/risk kuralı adayı.
- Kaynak: paket 70, `01-haftalik-gravestone-doji.png`. 1. el ekran (MatriksIQ benzeri), kural 2. el.
- Tansu'nun ifadesi (görsel): kırmızı kutuda yüksek fiyatta uzun üst gölgeli küçük gövde; fiyat ölçeği 0–150, tepe ≈ 150'ye gölge, gövde ≈ 112. Metin (2. el): "arkanıza bakmadan kaçılması gereken", haftalıkta daha ağır.
- Kurallar: eşik (gövde/gölge oranı) yok. Etki: pozisyondan çık. Önceki yükseliş: hızlanan (parabolik).
- Sonuç: sonraki fiyat yolu görselde yok.
- Veri: haftalık OHLC yeterli.
- Uygulanabilirlik: **K** (geometri net, eşik ve bağlam yorum).

### K-05-21 Dragonfly Doji + EMA sıkışması çıkışı
- Tür: giriş adayı; nota göre "erken dönüş adayı".
- Kaynak: paket 71, `01-dragonfly-doji-ema-sikisma-cikisi.png`. Not "rapor" türü (Cevo), Tansu sözü yok.
- Tansu'nun ifadesi (görsel): etiket/başlık yok. Mart–Nisan taban; kısa EMA kümesi, turuncu kesikli üst/alt kanal benzeri çizgiler (Donchian benzeri, okunamadı), alt panel hacim + sarı ortalama (hacim ≈ 1–4 M). Not: "sağ uçtaki mum kaynak tarafından Dragonfly Doji olarak işaretlenmiş": görselde böyle bir işaret **görmedim** (çelişki; görsel esas).
- Kurallar: yok.
- Uygulanabilirlik: **X**.

### K-05-22 Özel subplot gizli pozitif uyumsuzluk (74) — K-05-11'e ek
- Kaynak: paket 74, `01-ozel-subplot-gizli-pozitif-uyumsuzluk.png` (1. el). Not "rapor".
- Tansu'nun ifadesi (görsel): sağ üst "Son: 1578.00 ₺ | Getiri: +63.4% | β = 0.132"; lejant "MA20", "MA50", "Bullish Divergence"; fiyatta pembe "DIV" etiketleri ve sarı elmaslar, yeşil üçgenler; kırmızı oklar fiyatta higher low, alt panelde lower low; alt panel gizlenmiş başlık, çizgiler + histogram. Ekseni 2025-08 … 2026-02 civarı.
- Kurallar: formül gizli. "Getiri +63,4%" neyi ölçtüğü belli değil (etiketin nerede ölçüldüğü bilinmiyor).
- Uygulanabilirlik: **X** (formül gizli), fikir K-05-11.

### K-05-23 ISCTR A/D–EMA durum stratejisi
- Tür: giriş/çıkış (long ve short durumu).
- Kaynak: paket 75, `01-isctr-ad-ema-strateji-bh-drawdown.jpg`. Görsel 1. el; kural satırları Levent metni (2. el, platform formülü).
- Tansu'nun ifadesi (görsel): üstte "ISCTR … SATIŞ … Strateji: 19.1% B&H: 10.8% Sharpe: 0.67"; paneller "ISCTR Günlük Mum & İşlemler", "Accumulation/Distribution | EMA Crossover", "Kümülatif Getiri: Strateji vs Buy & Hold", "Strateji Drawdown". Kod (not): `Enter long: AD() [op] Ref(Mov(AD(),opt1,E),1)` ve aynı biçimde Close long / Enter short / Close short; "OPT1 = 3"; niyet 1–2 gün.
- Kurallar: operatörler ([op]) notta render edilmemiş; **okunamadı**. Not'un simetrik çıkarımı (AD > EMA → long) Cevo yorumu. Stop yok. Görselde strateji eğrisi uzun süre yatay (nakit/aracısız dönemler), yani sürekli long-short değil.
- Sonuç (görsel): %19,1 vs %10,8; Sharpe 0,67; en derin drawdown ≈ −%17; kümülatif ≈ 1,19 vs ≈ 1,08 (sağ uç, yaklaşık). Dönem, maliyet, walk-forward katları okunamadı.
- Veri: günlük OHLCV yeterli (A/D çizgisi OHLCV'den).
- Belirsizlik: operatör yönü, short BIST'te mümkün mü, Ref yönü.
- Uygulanabilirlik: **K**. Önceki okuma ile uyumlu.

### K-05-24 PETKM talep/arz confluence alanı
- Tür: confluence / yapı (kural yok).
- Kaynak: paket 78, `01-petkm-talep-arz-fibo-ema-hacim.png`. 1. el görsel, "confluence alanının gücü" Levent metni.
- Tansu'nun ifadesi (görsel): "PETKM - Analiz (Fiyat: 19.88)"; lejant "Fiyat", "EMA 8", "EMA 21", "Fibo", "Hacim"; yeşil üst üste talep bantları ≈ 15–16,5; kırmızı arz kutusu ≈ 21–22; Fib etiketleri (1.000, 0.786, 0.618, 0.500, 0.382, 0.236, 0.000) küçük, sayısal fiyatlar okunamadı.
- Kurallar: bölge üretimi, tolerans, puan: yok. Önceki okumada "SETUP puanı" X.
- Uygulanabilirlik: **X**.

### K-05-25 APO mean-reversion prototipi
- Tür: giriş (prototip).
- Kaynak: paket 85, `01-apo-ema-mean-reversion-sinyalleri.jpg`. 1. el görsel (düzenlenmemiş), Levent: "can sıkıntısıyla yazdığı basit prototip".
- Tansu'nun ifadesi (görsel): lejant "ClosePrice", "Fast10DayEMA", "Slow40DayEMA", "buy" (kırmızı üçgen), "sell" (yeşil ters üçgen); eksen 2014–2018, fiyat ≈ 500–1100; sembol okunamadı.
- Kurallar: APO = EMA10 − EMA40 (nottan, standart); sinyal formülü, eşik, yön (görselde buy = kırmızı yukarı üçgen, sell = yeşil aşağı üçgen; işaretlerin dip/tepe konumu bu çözünürlükte ayırt edilemedi): okunamadı. Yükselen kanal filtresi gelecek iş.
- Sonuç: yok (equity, tablo yok).
- Veri: günlük OHLCV yeterli (fiyat ölçeği BIST ile uyumsuz görünebilir; kaynak veri belirsiz).
- Uygulanabilirlik: **X** (kural yok).

### K-05-26 Mum geometrisi (OHLC, üst/alt gölge)
- Tür: ortak yapı taşı.
- Kaynak: paket 76, `01-python-ohlc-golge-analizi.png`. 1. el kod ekranı.
- Tansu'nun ifadesi (kod): `df['upper_shadow'] = df['high'] - df[['open','close']].max(axis=1)`; `df['lower_shadow'] = df[['open','close']].min(axis=1) - df['low']`; veri open [100,110,105,95], high [120,115,125,100], low [80,90,95,85], close [115,95,120,90]. Çıktı: upper 5,5,5,5; lower 20,5,10,5.
- Uygulanabilirlik: **H** (yapı taşı); kendi başına işlem kuralı değil.

### Strateji olmayan paketler (67–85)
- 72 HBK U dönüşü: fiyat ve yıllıklandırılmış HBK (mavi/turuncu); temel analiz, işlem kuralı yok. Görsel: HBK ≈ 9+ (2024 ilk yarısı) → ≈ 1 (2025 ortası) → ≈ 3,3–3,5 (Ocak 2026).
- 73 ASUZU finansal borç: peer tablosu 2025/12 ASUZU +83,9, sektör ort. +38,7; temel/risk, strateji değil.
- 77, 79, 80, 81: ASUZU/ARCLK/FROTO FK ve FD/FAVÖK değerleme çıktıları. ARCLK 2023/6: FK 177,59, FD/FAVÖK 184,22, ortalama 180,90, güncel 120,00, potansiyel %50,8. FROTO 2023: FK 796,03 (çarpan 4,3x), FD/FAVÖK 1441,67, ortalama 1118,85, güncel 800,00. ASUZU 2023 tam yıl: FK 120,20, FD/FAVÖK 119,28, ortalama 119,74, güncel 41,00 (+%192,1). Değerleme modülü, sinyal değil.
- 82–84 EREGL DCF: WACC %22,19; DCF hisse başı 22,69 TL; son fiyat 16,67; potansiyel %36,1; firma değeri 79.423 (82-03'te 79.424: yuvarlama). 84 yalnız girdi tablosu.

## Ortak yapı taşları (parça 05'ten)

- Pivot/swing etiketleri (H, L, HH, HL, LH, LL, "Swing=15 sol-only", "MinGap=15"): 56, 60, 61, 69.
- Fibonacci geri çekilme/uzantı merdiveni: 45 (ABCD 1.27), 47 (Trident, CD=1.27AB), 58 (cup-handle), 66 ve 78 (0,786 vb.).
- EMA kümeleri: EMA 5/8/13 (45, 64), EMA 20/50/100/200 (65, 67), EMA 50/100/200 (68), EMA 8/21 (78), EMA 9/21/50/100/200 (69), EMA 10/40 (85).
- Z-skor çift sapması, ±2 eşik, Z dönüş onayı: 51, 52, 53, 54, 55.
- Talep/arz bölgesi: 45, 64, 78. Düşen direnç çizgisi ("Direnç TL"): 45, 64.
- FVG: 69. KDE tepe seviyeleri: 68. Hacim profili/VWAP/delta: 66, 45.
- Mum geometrisi (gölgeler, Doji): 70, 71, 76.
- Volatilite/likidite göstergeleri (Corwin–Schultz, sigma, fiyat-vol ilişki): 48, 49, 62.
- Aynı fikir başka paketlerde: gizli pozitif uyumsuzluk 60, 61, 74; EMA sıkışması 65, 67, 71; AB=CD 45 (ve parça 04'te 39–43); çift 51–55 (parça 04'te de var).

## Tansu'nun bakış açısı (ipuçları)

Kural: tırnak içindekiler dosyada gördüğüm metindir. "Not" = notun aktarımı (Levent'in birebir cümlesi olmayabilir, 2. el). "Görsel" = Tansu aracının çıktısı. Yorum satırları benimdir.

**Rejim ve piyasaya bakış**
- "mavi çizgi sıfırı yukarı kestiği anda kırmızı bölgede oluşan yükselişler büyük oranda geri gelir" (not, gorsel-paket-46-sagliksiz-yukselis-mavi-sifir-kesisi.md). Yorum: yükselişin "sağlığı" rejime bağlı; her yükseliş alım nedeni değil.
- "Sağlıklı yükseliş böyle olur; fiyat çıkarken alt paneldeki mavi çizgi sıfırın altına iner ve oralarda gezinir; quant strateji farklı görmektir" (not, paket 49). Yorum: fiyat tek başına yetmez; fiyat ve oynaklığın ilişkisine bakıyor.
- Fiyat ve oynaklık birlikte artınca "sistem pozisyonu kapattı, defansife geçti"; alt panel "Pozisyon Büyüklüğü Çarpanı", "(Tam)", "(Defansif)" (not + görsel, paket 48 SMRTG). Yorum: yön kapatmak yerine büyüklük çarpanı ile rejime uyum.
- "Piyasa yapıcının bize bir mesajı var; KY sizi seviyorum diyor" (not, paket 50; BIST100 ve BIST_VOL scatter, V biçimi). Yorum: büyük hareketlerin iki yönünde de oynaklığın arttığını (doğrusal olmayan ilişki) gösteren espri.
- Spread yüksek + sigma yüksek ise uzak dur / geniş stop; spread düşük + sigma yüksek ise yön savaşını trend lehine yorumla; spread normale dönünce güven artar (not, paket 62). Görsel: "Corwin-Schultz Bid-Ask Spread (%, 21g rolling)", "Volatilite Tahmini (Sigma %)".
- EMA yakınsamasını "kısa/orta/uzun vadeli denge ve düşük oynaklık bölgesi" olarak yorumluyor (not, paket 68). Yorum: sıkışma = enerji birikimi fikri (65, 67, 68, 71'de tekrar).
- Fiyatın ortalamalardan uzaklaşması: "güçlü/parabolik trend ve olası soğuma/yatay/retest ihtimali" (not, paket 68). Yorum: güçlü trendi reddetmiyor, uzama riskini de görüyor.
- Piyasa evreleri: "Piyasanın 4 Evresi" taban/birikim, yükseliş, tepe/dağıtım, düşüş (not, paket 56).
- "Gravestone Doji ... arkanıza bakmadan kaçılması gereken", haftalıkta daha ağır (not, paket 70). Yorum: tek mum çıkış nedeni sayılıyor, zaman diliminin ağırlığı var.

**Kurulum seçimi, confluence, bağımsız kanıt**
- "confluence alanının gücü" (Levent, paket 78; görsel PETKM talep/arz). Yorum: birden çok araç aynı alanda üst üste biniyor; bağımsız kanıt sayısı bu paketlerde hesaplanmıyor (bunu not yazarı ekliyor, Tansu'nun sözü değil).
- "Neden bir ayda %20 verdi?" ve zincir: Fib 0,786, direnç aşımı, POC/VAH/VWAP üstü, +DI üstünlüğü, pozitif delta (not, paket 66). Yorum: sonucu nedensel zincirle açıklıyor; seçilmiş örnek.
- "sıkışma zamanları iyi tespit edilirse ve aynı alanda formasyon bulunursa güçlü kâr fırsatı doğabilir" (not, paket 67). Yorum: sıkışma + formasyon birleşimi.
- Gizli pozitif uyumsuzluğun gücü "nerede arandığına" bağlıdır (not, paket 74). Yorum: bağlam filtresi vurgusu.
- Demand + düşen direnç kırılımı + yüksek hacim + EMA 5/8/13 dönüşü + uzun yeşil mum zinciri (not, paket 64); görsel lejant "Direnç TL".
- "Hep göz önünde olan 1–2 filtreyle enteresan breakout sinyali var; yeni keşfettim" (Levent, paket 44). Yorum: sadelik değer taşıyor; filtreleri açıklamıyor.
- "Strateji parametrelerini açıklayamayacağını, fakat ana fikri verdiğini" (not, paket 65). Yorum: bazı parametreleri bilerek saklıyor; bu yüzden birebir yeniden üretim sınırlı.
- Sıkışma periyodu ve oran eşiği "strateji tasarımcısının tecrübesine göre seçilir" (not, paket 67). Yorum: eşikleri sistematik sınamadan değil deneyimle seçtiğini ima ediyor.

**Giriş teyidi**
- "ABCD'ye güvenip doğrudan alırsan böyle olursun; her zaman çalışmaz; ikinci alt grafiğe dikkat" (not, paket 45; görsel BALAT "Küm. Delta" negatif). Yorum: formasyon + katılım (hacim/delta) birlikte aranıyor.
- FVG'de "doğrudan long yerine 1H/4H CHoCH beklemeyi" (not, paket 69). Yorum: alt zaman dilimi teyidi.
- Ana trend aşağıyken gizli uyumsuzluk yok; setup yukarı trendde pullback sınıflaması (not, paket 60; görsel "Swing=15 sol-only | MinGap=15"). Yorum: ayarları açıkça veriyor.
- "Pazartesi bakalım" (paket 64) ve FVG için "Pazartesi" izleme (paket 69). Yorum: sinyal sonuç beklemeden paylaşılıyor (prospektif), ama sonuç sonradan paylaşılmıyor.

**Risk, stop, hedef**
- Hedef = kırılım + fincan derinliği; R/R 1:2,27 (görsel, paket 58). Yorum: hedef geometriden, stop görselde yazılı değil.
- "Piyasada haklı çıkmak ego tatminidir; sermayeyi korumak hayatta kalma becerisidir." (Levent, paket 75). Aynı notta: sakin getiri eğrisi, sınırlı drawdown, "gerektiğinde nakitte kalmak". Yorum: başarı ölçütü Sharpe'tan geniş.
- Tablo: "ham getiriden feragat karşılığında daha huzurlu bir eğri" (not, paket 59; B&H +%21,54 / strateji +%14,74; vol %33,16 → %23,21; MDD −%2,46 → −%1,72). Yorum: risk azaltmayı getiri kaybına tercih ediyor.
- Nakit bekleme: "Algoritmik disiplin zararı kabul eder, nakitte bekler ve yeni fırsatta kurala uyar" (not, paket 52; log: 21 gün nakit). 

**Doğrulama ve backtest görüşü**
- "Her arbitraj fırsatı çalışmaz; mutlaka backtest etmek lazım; görünmez bağ kopmuş olabilir" (Levent, paket 53). Yorum: kendi başarısız örneğini (strateji ≈ 79 bin TL) paylaşıyor.
- "portföy yönetiminde getiri hesabı ve geriye doğru simülasyonların önemi" (not, paket 57); ağırlık duyarlılığı: TEKTU ağırlığı 0'dan 1'e %11,6 → %29,8; EREGL %18,0 → %13,3 (görsel). Yorum: ağırlığı geriye dönük sınıyor; dönem 01.04–22.04.2026 çok kısa, ex-post.
- BIST momentum: "BIST'te momentum çalışıyor" ve kaynak sınırlamaları: "Backtest, işlem maliyeti, vergi ve likidite yok" (not, paket 63). Yorum: kendi sınırını belirtiyor.
- DCF: "girdilere aşırı duyarlı bir modeldir", "DCF hedef-fiyat makinesi değil, varsayım stres aracıdır" (not, paket 84). Yorum: model riskini kendisi anlatıyor.
- "Geçmiş tam yıl marjını körlemesine kopyalama"; güncel ara dönem marjı kullan; kodu Excel ile uzlaştır (not, paket 79). Yorum: tahmin hatasını azaltmak için en güncel gerçekleşen veriye dayanıyor.

**Araçları birleştirme (tarama, filtre, tetik, yönetim)**
- "sadece sistem çalışıyor, hiç ellemiyorsun" ve en sevdiği iki sistem ailesi volatilite ve arbitraj (Levent, paket 55). Yorum: kural dışı müdahale yok ilkesi.
- "duygulardan arınmak tam olarak budur; disiplin aşılamak için" (Levent, paket 52). 
- Zincir (görsel+not): tarama (fincan-kulp "kendi tarama sistemi", paket 58) → kırılım sinyali → hedef; ya da talep bandı → hacim → EMA → çizgi kırılımı (64); büyüklük çarpanı (48). Yorum: tarama → filtre → tetik → yönetim sırası notlarda net bir zincir olarak yazılmıyor; ben parçaları yan yana okudum.
- Excel çıktısı + konsol: "StatArb_Islem_Logu_AGROT_GARAN.xlsx" (görsel, paket 54); DCF "Excel kaydedildi → outputs/FROTO_Tahmin.xlsx" (görsel, paket 80); "tek tuşla sonuç" (not, paket 83). Yorum: Python + Excel araç zinciri, sonuçlar konsola ve dosyaya dökülüyor.

**Reddettiği / eleştirdiği**
- ABCD'ye kör güven (45); her arbitraj fırsatı (53); sağlıksız yükseliş (46, 48).
- Prototip hakkında: "can sıkıntısıyla yazdığı ... basit bir mean-reversion prototipi" (not, paket 85) ve "parametreler ve kanal filtresi geliştirildiğinde sonucun iyileşebileceğini". Yorum: kendi işini mütevazı etiketliyor.

**Tekrar eden ilkeler (yorum)**
1. Tek gösterge yerine rejim/bağlam: 46, 48, 49, 56, 74.
2. Katılım (hacim, delta) formasyonu teyit ediyor: 45, 64, 66.
3. Hedefler geometriden (Fib, derinlik, D formülü): 47, 58, 45.
4. Kendi başarısız örneklerini de paylaşıyor: 45, 53.
5. Küçük, açık parametreler (Swing=15, tolerans %1,2, Min 3 gün, ±2): 60, 67, 51.
6. Risk azaltma > ham getiri: 48, 59, 75.
