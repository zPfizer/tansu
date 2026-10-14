# Bilet 04, bölüm 1: yazıcı raporu (14.10.2026)

Dal: `pr/04-kurallar-katalog` (master'dan). Kapsam: `denetim/hiza-c.md` 1–40, `denetim/hiza-b.md` 16–20 ve 22; ticket kutuları 1–5 (ve 7). Kutu 6 (havuz kapsamı) ve `hiza-c-istem` yeniden koşusu yapılmadı.

Not: A–E'nin satır numaraları 10.10'dan beri değişmedi (tek kayıt `f20a068`); KURALLAR'ın numaraları `ce0fe60` ve `938725c` ile kaydı. "Bugünkü yer" sütunu bu dalın ilk durumudur. `docs/strateji-modulleri-taslak.md` (M) ve `docs/strateji-taslak/tasarim-8.md` (T8) `.gitignore`'dadır: oradaki düzeltmeler yerel dosyada yapıldı, commit'te görünmez.

## 1. hiza-c 1–22

| # | Kaynak satırı | Bugünkü yer | Yapılan |
|---|---|---|---|
| 1 | E:24 | E:24 (değişmedi) | düzeltildi: "sözlük 4 ATR hedef der" aktarımı kaldırıldı; 05.10 ön denemesi olduğu ve güncel kararın TASARIM §5.5 / KURALLAR §1 madde 4 olduğu yazıldı |
| 2 | E:577–578 | E:577–578 | düzeltildi: "GLOSSARY'deki 4 ATR hedef" ve EMA50 cümleleri eski ön deneme olarak işaretlendi |
| 3 | E:219 | E:219 | düzeltildi: "GLOSSARY'deki BEKLE günü yeni giriş yok" kaldırıldı; güncel karar (piyasa durumu girişi durdurmaz, TASARIM §3, §6) yazıldı |
| 4 | E:605–606 | E:606 | düzeltildi: kontrol listesi maddesine "seçilmiş çift rotasyonu bölmesi stopsuzdur (TASARIM §5.5–5.6, KURALLAR §3)" istisnası eklendi |
| 5 | B:48, 474, 491 (+28, 41, 46, 49) | aynı | düzeltildi: ratio formülü "çözüldü (sadakat, KURALLAR §4, docs/sadakat.md)"; kalan boşluk yalnız giriş tetiği; "en yüksek değerli boşluk" giriş tetiğine çevrildi |
| 6 | T8:158–159 | T8:158–159 (yerel) | düzeltildi: "formül taslak 7 ile aynı" kaldırıldı; payda kapanıştır, KURALLAR §3 EMA200'e böler, değişiklik öneridir |
| 7 | C:393 / E:251–259 | C:393 zaten "0,618 CD" | çürütüldü: C:393 (07.10 düzeltmesi), C:281 ve E K11 üçü de TP2 BALAT'ta CD, SAYAS'ta AD diyor; çelişki yok |
| 8 | E:279, 299; T8:127 | aynı | düzeltildi: "Bk Stop" → "İlk Stop (X)" (C §7, 07.10 okuma düzeltmesi); E:299'daki "Bk Stop kısaltması" belirsizliği kaldırıldı; T8:127 işaretlendi |
| 9 | M:370; E:70, 84; K:52 | aynı | düzeltildi (bkz. bölüm 4): doğru sayı okunamıyor; tek kayıt E K2; K ve M sayı yazmıyor |
| 10 | M:299 | M:299 (yerel) | düzeltildi: "skor toplama kuralı yok" → ilk beş kutu sayılır, ADX ve Hacim girmez (D, Piyasanın Nabzı) |
| 11 | M:318 | M:318 (yerel) | düzeltildi: "ağırlık yok" → eşit ağırlık (B §14, ikinci el) |
| 12 | M:343, 417; T8:163 | aynı | düzeltildi (bkz. bölüm 4): ilk EMA = EMA20; tek yer B §2; M ve T8 atıf veriyor, T8'deki EMA30 düzeltildi |
| 13 | M:252–253 | M:252–253 (yerel) | düzeltildi: TAMAMLANDI'nın kaynak anlamı C §2'ye bağlandı (fiyat D hedefine ulaştı; kâr hedefi değil); "önerilen işlem durumu" ayrıldı |
| 14 | M:65, 125, 358 | aynı (yerel) | düzeltildi: R245–R263 metinlerinin 06.10'da çekildiği (`ham-yapistirmalar-3.md`) ve "metin yok / yalnız bağlantı" hükümlerinin eski olduğu yazıldı; R255 metninde retest sorusu gerçekten var |
| 15 | T8:140–141 / M:117, 120 | T8:140–141 (yerel) | düzeltildi: ham R090 (`ham-yapistirmalar.md:983`) okundu; "D oluşumunu teyit etmek için B noktası kırılımı gerekir" cümlesi satış yönlü paragraftadır; T8'e "alışa aktarılması YORUM" yazıldı |
| 16 | T8:142 | T8:142 (yerel) | düzeltildi: katsayı listesi `{0,382; 0,618; 1; 1,272}` (1 = C noktası) |
| 17 | K:104 / T:505–507 | KURALLAR:108 (master) | zaten düzeltildi: bilet 03 dalı (`pr/03-tasarim-kararlar`) satırı (a)/(b) olarak ayırdı. Bu dalda dokunulmadı; birleşmede gelir |
| 18 | K:31 / C:121, 138 | KURALLAR:33 | düzeltildi: "BC ≤ AB" birinci el sütunundan çıkarıldı, "ikinci eldir (C §3)" yazıldı |
| 19 | K:61 / D:148 | KURALLAR:63 | düzeltildi: "VIX = ABD VIX" YORUM olarak işaretlendi (D "Hangi VIX?") |
| 20 | K:97–98 / T:892 | KURALLAR:100–101 | düzeltildi: "KRDMD rakamlarıyla eşleşen formül"; düşüş trendinde payda ayrımı açık (TASARIM §8 madde 6). "birinci el" sözü kaldırıldı |
| 21 | K:36 | KURALLAR:38 | düzeltildi: dosya "A, C" → "A §10" (E Ek A artık yalnız işaret tablosu); aynı işlem AKFIS (A §1), Gartley (C §7), Fincan-kulp (B §21) satırlarına |
| 22 | K:10–12 / G | GLOSSARY master'da | zaten düzeltildi: YORUM, ATR, EMA, SMA terimleri GLOSSARY'de var |

## 2. hiza-c 23–40 (tekrar → atıf)

Yöntem: ikincil kopya, sahibinde eksik olan tek bir gerçek varsa o gerçek sahibine taşındı ("taşındı, bilet 04" notuyla); kopya kısa atıfa çevrildi.

| # | Sahip | İkincil kopya, bugünkü yer | Yapılan |
|---|---|---|---|
| 23 | S (`docs/sadakat.md`) | KURALLAR §4 sonuçlar | düzeltildi: aday sayıları, tolerans sonuçları ve ölçülen değerler çıkarıldı; yalnız karar kaldı, S'ye atıf. Sorgu 3 Yahoo ölçümü (%0,638 vb.) S'de olmadığı için KURALLAR'da kaldı |
| 24 | KURALLAR §3 | TASARIM 5.6 "Sinyal" | TASARIM'a (bölüm 5). KURALLAR'a `ddof 1` eklendi |
| 25 | TASARIM 5.3–5.6 | KURALLAR "Risk paketi" ve AOF paragrafı | düzeltildi: ikisi TASARIM atfına çevrildi |
| 26 | TASARIM §3 | KURALLAR "AB=CD ilk sürümden çıktı", "ikinci dalgadadır" cümleleri | düzeltildi: TASARIM §3 atfı; seçim tablosu (gerekçe + YORUM) kaldı |
| 27 | C §3–5 | E K15 (T-abcd, G-03 backtest, kanıt); KURALLAR:33 sayıları | düzeltildi: E K15 C §2/§3/§5/§10 atfı; KURALLAR:33 "sonuçlar C §5'te". KAPLM başarısız örnek notu C §10'a taşındı |
| 28 | C | E K11, K12, Ek A (BRYAT) | düzeltildi: K11 → C §11, K12 → C §7. Taşınanlar: TP2 ödülü (0,32 R) ve "en güvenilir hedef" notu → C §11; SAYAS Fib etiketleri, 73,45/107,12 doğrulaması, SAYAS kanıtı → C §7 |
| 29 | C §8, §9, §15, §16 | E Ek A; M | düzeltildi: Ek A satırları sahibine atıf (C §16, A §10, B §3, D). M için geçerlilik notu (bölüm 3) |
| 30 | A §1–2 | E K13; KURALLAR dizini | düzeltildi: K13 → A §1 (alıntı örneği piksel okuması A §1'e taşındı); dizin satırı "A §1". KURALLAR §4 AEFES satırı çürütüldü: önceden yazılmış sadakat hedefidir |
| 31 | A §3–4, §12 | B §4; C §13 (LIDER/BALAT); E K17 | düzeltildi: B §4 → A §12 ve A §4; C §13 başlıklar ve parametre satırları → A §3; K17 → A §12 |
| 32 | A §5 | D "SETUP x/100" | düzeltildi: D → A §5 |
| 33 | A §9–10, §13–14 | E K16 (TTKOM); B §31 (gp-18, gp-128); E Ek A | düzeltildi: K16 → A §9; B §31 iki madde → A §14 ve A §13; Ek A işaretlendi |
| 34 | B §1, §9–10 | C §1 (Swing=15, MinGap, lookback, temas) | düzeltildi: C §1 → B §9 ve A §3. KURALLAR:124 (sadakat hedef kimliği) çürütüldü |
| 35 | B §15, §18, §24 | yalnız M ve T8 | taslaklarda geçerlilik notu (bölüm 3); satır satır çevrilmedi |
| 36 | B §8, §20, §21, §30 | E K7, K14, K23 (beş kapı), A §16 (MA filtresi) | düzeltildi: K7 → B §8 (çarpan YORUM'u ve gözlem B §8'e taşındı), K14 → B §21 (R/R doğrulaması taşındı), K23 beş kapı → B §20, A §16 MA → B §30 |
| 37 | D §3 | B §29; E Ek A | düzeltildi: B §29 → D |
| 38 | D §1 | KURALLAR:32 sayıları | düzeltildi: dizin satırı D'ye atıf. KURALLAR §4 hedef tablosu çürütüldü (sadakat hedefi, önceden yazılmış) |
| 39 | D | E K24 (G-59, G-53) | düzeltildi: iki madde → D. KURALLAR:62 çürütüldü (tek satırlık özet) |
| 40 | E K1, K18 | A §16 (not-backtest-giris-sadeligi) | düzeltildi: A §16 → E K18. E "(b) Grup 2" kontrol listesi çürütüldü (K18'e atıf veren türev liste) |

## 3. İki taslak (M ve T8, yerel, git'te yok)

Satır satır çevrilmedi. Her ikisine "Geçerlilik (bilet 04, 14.10)" paragrafı eklendi: kaynak okuması A–E'de, kural seçimi KURALLAR'da, davranış TASARIM'da, terim GLOSSARY'de; fark varsa onlar geçerli. Denetim istemi "taslak, hangisinin geçerli olduğunu bir dosya söylüyorsa bulgu değildir" diyor; TEKRAR (taslaktaki kaynak kopyaları) bu notla "tarihli kopya" olarak işaretlendi. Auditör bunu yeterli bulmazsa tekrar tekrar çevrilecek yer: M:299–372 ve T8:97–245 tabloları.

## 4. Görsel çelişkileri

**G-125 stop etiketi.** Açılan dosya: `Tansu X Veri Havuzu\assets\gorsel-paket-125-kismi-kar-trailing-stop\01-kismi-kar-trailing-prev-low-emergency-stop.jpg` (680×147 piksel). Etiket yazısı yaklaşık 3 piksel yüksekliğinde; 12x, 16x ve 30x büyütmede ve piksel döküm ASCII çıktısında rakamlar ayırt edilemedi. Yani 184,54 ile 104,34 okumalarından hangisinin doğru olduğu görselden **çıkarılamaz** (ATR 4,62 de kesin değil). Hiçbir kural bu sayıya dayanmıyor. Karar (yazıcı kararı, bilet 04): tek yer E K2 (satır 70, "G-125 görsel" maddesi): "okunamaz; iki okuma çelişir". E K2 tablosu, E K2 "belirsiz kalanlar", E K5 (satır 148), KURALLAR:54 ve M:370 sayı yazmıyor, E K2'ye atıf veriyor. 193,78 çıkarımı kaldırıldı.

**ICBCT ilk EMA.** Açılan dosya: `Tansu X Veri Havuzu\assets\gorsel-paket-65-ema-sikisma-pre-signal\01-icbct-ema-sikisma-pre-signal.png`. 8 kat büyütmede lejant: `EMA20 (14.44)`, `EMA50 (14.29)`, `EMA100 (14.31)`, `EMA200 (14.42)`. İlk ad **EMA20**; EMA30 değil (T8'deki 30 yanlış, M'deki 20 doğru). Okuma tek başına harf biçimine dayanıyor ve bulanık; destek: aynı aracın KRDMD lejantı EMA20/50/100/200, ve (14,44 − 14,29) / 14,42 = %1,04, Sorgu 3 cevaplayıcısının bulduğu bantla aynı. Tek yer: B §2 (satır 54). M:343 ve T8:163 buna atıf veriyor.

## 5. TASARIM'a (bilet 03/07)

Bu dalda TASARIM'a dokunulmadı. Önerilen değişiklikler:

1. **TASARIM 5.6 "Sinyal"** (hiza-c 24, hiza-b 18): `Z ≤ −2 ve ΔZ > 0 ise hedef Y; Z ≥ +2 ve ΔZ < 0 ise hedef X` eşiklerini yeniden yazmak yerine "KURALLAR §3'teki sinyal" demeli; `ddof 1` artık KURALLAR §3'te.
2. **TASARIM 5.7 "Ek kol"** (hiza-b 19): "önceki 20 günün en yüksek yükseği, sıkışma penceresinde değil, 20 YORUM" KURALLAR §3'te de yazılı; TASARIM yalnız örnekleme ve raporlamayı anlatıp KURALLAR §3'e atıf vermeli.

## 6. Levent'e sorular

Yok. Karar gerektiren iki nokta (G-125 sayısı okunamıyor; ICBCT ilk EMA) kuralı değiştirmiyor; yazıcı kararı olarak yazıldı.

## 7. Ek: kutu 7

KURALLAR §2 risk satırı: "lot = risk / (2 ATR)" → "lot adedi = risk / (2 ATR)" (GLOSSARY "Adet, lot"). Kutu 7 bu bilet kapsamında yazılmadı ama tek satırdı; yapıldı.
