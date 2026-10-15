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
| 12 | M:343, 417; T8:163 | aynı | bölüm 4 ve tur 1: ilk EMA etiketi görselden belirlenemedi (20 ya da 30); tek yer B §2; M ve T8 atıf veriyor |
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
| 23 | S (`docs/sadakat.md`) | KURALLAR §4 sonuçlar | düzeltildi: aday sayıları, tolerans sonuçları ve ölçülen değerler çıkarıldı; yalnız karar kaldı, S'ye atıf. Sorgu 3 Yahoo ölçümü (%0,638 vb.) S'de olmadığı için KURALLAR'da kalmıştı (tur 1'de kaldırıldı, bkz. A13) |
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

**ICBCT ilk EMA.** Açılan dosya: `Tansu X Veri Havuzu\assets\gorsel-paket-65-ema-sikisma-pre-signal\01-icbct-ema-sikisma-pre-signal.png`. 8 kat büyütmede lejant: `EMA20 (14.44)`, `EMA50 (14.29)`, `EMA100 (14.31)`, `EMA200 (14.42)`. Yazar ilk adı EMA20 okudu; denetçi EMA30 okudu. Çözünürlük ikisini ayırmaya yetmez (tur 1). Karar: B §2 (satır 54) "ilk EMA etiketi okunamıyor (20 ya da 30)" yazar; KRDMD ayarı 20/50/100/200; hiçbir kural bu etikete dayanmaz. M ve T8 buna atıf verir.

## 5. TASARIM'a (bilet 03/07)

Bu dalda TASARIM'a dokunulmadı. Önerilen değişiklikler:

1. **TASARIM 5.6 "Sinyal"** (hiza-c 24, hiza-b 18): `Z ≤ −2 ve ΔZ > 0 ise hedef Y; Z ≥ +2 ve ΔZ < 0 ise hedef X` eşiklerini yeniden yazmak yerine "KURALLAR §3'teki sinyal" demeli; `ddof 1` artık KURALLAR §3'te.
2. **TASARIM 5.7 "Ek kol"** (hiza-b 19): "önceki 20 günün en yüksek yükseği, sıkışma penceresinde değil, 20 YORUM" KURALLAR §3'te de yazılı; TASARIM yalnız örnekleme ve raporlamayı anlatıp KURALLAR §3'e atıf vermeli.

## 6. Levent'e sorular

Yok. Karar gerektiren iki nokta (G-125 sayısı okunamıyor; ICBCT ilk EMA) kuralı değiştirmiyor; yazıcı kararı olarak yazıldı.

## 7. Ek: kutu 7

KURALLAR §2 risk satırı: "lot = risk / (2 ATR)" → "lot adedi = risk / (2 ATR)" (GLOSSARY "Adet, lot"). Kutu 7 bu bilet kapsamında yazılmadı ama tek satırdı; yapıldı.

## 8. Denetim tur 1 (Codex)

Karar: KALDI (tur 1). Düzeltmeler bu bölümdedir; kutu 10, 11, 12 ve 13 durumları bilet dosyasında. Yerel gitignore dosyaları M (`docs/strateji-modulleri-taslak.md`) ve T8 (`docs/strateji-taslak/tasarim-8.md`) diskte düzeltildi; commit'te görünmez.

### Bölüm A

| # | Sonuç |
|---|---|
| A1 ADX | düzeltildi: B:76 "ADX için periyot, eşik yok" kaldırıldı; ADX14 ve eşik 20 sahibi A §12'ye atıf |
| A2 EMA formülü | düzeltildi: KURALLAR §3 formülü seçen yer ("görselde yok; KRDMD dışında doğrulanmadı"); B §1 (adım 2, parametre tablosu, güven, sıralı özet B ve D), KURALLAR §2 seçim tablosu ve §4, M:345 aynı sınırı taşır; "birinci el", "çözüldü" ve "YORUM değil" sözleri kaldırıldı |
| A3 AKFIS stopu | düzeltildi: KURALLAR dizini artık A §1'e atıf verir, stop formülü yazmaz; A §1'in YORUM nitelemesi korundu |
| A4 ham fiyat | düzeltildi: KURALLAR §2 satırı ve §3 aile 1: sinyal düzeltilmiş seriden, ham seri yalnız sadakat kontrolünde (TASARIM 5.1) |
| A5 çıkış dolumu | düzeltildi: E K3 madde 2 ve tablo, E K2 madde 3 ve tablo, E K5 madde 5: "ertesi seans açılışı" yerine TASARIM 5.5 / 5.3 (AOF, min(stop, AOF)) |
| A6 menşe | düzeltildi: E:14 (NotebookLM = ikinci el; E içindeki 11 "BİRİNCİ EL (infografik)" kullanımı dahil), C §18 (gp-111, NotebookLM), C:716 (gp-121, imzasız, yazarlığı belirsiz ikinci el), A:281 (gp-17), B §23 (gp-104), B:301 (gp-119), B:13, C:566 (gp-132: yapay zekâ yanıtı kuşkusu korundu), A:172 (gp-15), D (gp-98, gp-113 NotebookLM). GLOSSARY "İkinci el" satırına "imzasız ders şeması ve yazarlığı belirsiz metin" eklendi |
| A7 veri durumu | düzeltildi: B:18, D (çift bedava veri maddesi, Nabız ve BIST-VIX veri maddeleri), E K2 (Open yok): "hesaplama düzeyinde evet" ile projenin güncel veri durumu (İş Yatırım, Yahoo yok, açılış yok; TASARIM 5.1) ayrıldı |
| A8 sınırlama | düzeltildi: A "Okunmayanlar" bölümündeki "orijinal metinler yok" yerine "Ham" bölümlerinin varlığı (havuzda 258 notun 257'sinde "Ham" var) |
| A9 sonraki adım | düzeltildi: E sonu "Uygulama sırası ve durumu: TASARIM §7 (K1–K3 tamamlandı)" |
| A10 K ve T tekrarı | TASARIM değişmedi; K aile kuralını tutar. "TASARIM'a" listesi aşağıda |
| A11 tanımlar | düzeltildi: KURALLAR okuma kuralları, A:3, B:10–13, C:10–17, D:4, E:9–16: tanım tabloları GLOSSARY atfına ve kullanım cümlesine çevrildi |
| A12 dizin ve hedefler | düzeltildi: KURALLAR §2 dizin üç tablosu "Kural, Bölüm, Hazırlık" üç sütuna indi (kaynak değer yok); §4 hedef tablosu değer yerine A–E bölümü verir |
| A13 formül ve sadakat | kısmen çürütüldü: Yahoo ölçümü S'ye taşınamadı. `docs/sadakat.md` `python -m tansu sadakat` tarafından baştan yazılır (`tansu/sadakat.py:283`); elle eklenen bölüm bir sonraki koşuda silinir. Ölçüm zaten `docs/sorgu/sonuc-3-4.md` O9'dadır; KURALLAR §4'ten ölçüm kaldırıldı, O9'a atıf verir. KURALLAR §3 formül yinelemesi A2 ile tek yere indi (tur 2: §3 ve §4'te iki kez duruyordu; §4 artık atıf) |
| A14 çapraz kopyalar | düzeltildi: C:34, C:449, C:479, C:542 (A §1 / A §3 / B §9 atfı); B:436 (D atfı); E:218 (D atfı); E:362–363 ve E K23 "R/R eşiği" (B §20 atfı); E "Tansu risk ve çıkış paketi" tablosu 15 satır Sahibi sütununa indi; E K11–K14 "risk yönünden okuma" paragrafları; A:278 (E K18 atfı) |
| A15 taslaklar | düzeltildi (yerel): M:296–375 tablolarında 50 satırın "Sadakat hedefi" sütunu A–E bölüm atfına çevrildi (boş "yok" olanlar kaldı); T8:355–366 hedef listesi atıf listesine; M:418 "ATR: 4.62" kaldırıldı; M:419 ICBCT ilk EMA; T8:165 |

### Bölüm B

| Madde | Sonuç |
|---|---|
| ICBCT (B:54) | düzeltildi: "görselde ilk EMA etiketi okunamıyor (20 ya da 30); KRDMD ayarı 20/50/100/200; sadakat ölçümü 20 ile uyuştu (S)"; ikisi de iddia edilmez. Lejant listesinde ilk ad `EMA??` yazıldı |
| G-125 | düzeltildi: iki aday okuma yalnız E K2'de; M:372 (Y3) sayısız, "E K4, K5; G-125 etiket rakamları yalnız E K2"; M:418 sayı iddia etmez. KURALLAR, A–D, M ve T8'de başka yerde 184,54, 104,34 ya da 4,62 yok (`docs/strateji-taslak/` altındaki diğer çalışma dosyaları kapsam dışı, değişmedi) |
| POC/VWAP (A:284) | düzeltildi: kaynak koşulu "VWAP hâlâ üstteyken" geri yazıldı (`tweet-poc-vah-val-vwap-auction-state-machine` Ham satır 45'te "VWAP hala yukarıda kaldığında") |
| DEA notu (K:214) | düzeltildi: "kural içermez" listesinden çıkarıldı; D "Sektör rotasyonu"na "yazarlığı belirsiz, ikinci el; YORUM" ve tek satır kuralla yazıldı |
| Ek bulgu (örnekleme dışı) | `tweet-aylik-getiri-mevsimsellik-piyasa-hafizasi` "eşiksiz" diye dışlanmıştı; Ham metinde %70 eşiği ve 10–20 yıl var. DEA ile aynı gerekçeyle listeden çıkarıldı ve D'ye yazıldı. `gorsel-paket-97` kapsam dışı (TASARIM §3, opsiyon IV) olduğu için listede kaldı. Liste 67 → 65 not |
| B:54 bir günlük hareket cümlesi | tur 2'de düzeltildi: rakam kaldırıldı ("bir günlük sert hareket") |
| Bölüm B satırları 23–40 | A14 ve A15 düzeltmeleriyle aynı işlem; BALAT çürütmesi (satır 34) değişmedi |
| Bilet kutuları 10–12 | kutu 11 ve 12 işaretsiz, açık kısım bilet dosyasında; kutu 10 işaretli (22 maddenin tamamı kayıtlı); kutu 13 işaretsiz |

### TASARIM'a: atfa çevrilecek satırlar (bilet 03/07; bu dalda değişmedi)

- `docs/TASARIM.md:437–438` (5.6 "Sinyal"): `Z ≤ −2 ve ΔZ > 0` / `Z ≥ +2 ve ΔZ < 0` KURALLAR §3 aile 1 ile aynı; "KURALLAR §3'teki sinyal" demeli.
- `docs/TASARIM.md:535–537` (5.7 "Ön şartlı gün (EMA)", "Tür (a)") ve `:550–552` ("Ek kol"): sıkışma bitti, 10 günlük pencere, kapanış ≥ SMA250 ve önceki 20 günün en yüksek yükseği koşulları KURALLAR §3 aile 2 K1 ön şartı ile aynı; yalnız örnekleme ve raporlama TASARIM'da kalmalı.

### Kapı

`ruff check .`: All checks passed. `pytest -q` (yazılabilir `--basetemp` ile): 310 passed. Kapsam kontrolü: 258 / 258 havuz notu KURALLAR ya da A–E içinde. Satır sonu: değişen dosyalar `i/lf`.

## 9. Denetim tur 2 (Codex)

Karar: KALDI (tur 2). Tur 1 tamamlanma iddiaları düzeltildi: A12 ve A13 tam kapanmamıştı (K:55–58 ve :66–68 değer taşıyordu; formül KURALLAR'da iki yerde durdu, "tek yer" iddiası yanlıştı); A15 tam kapanmamıştı (M:319 ve birkaç formül kopyası kalmıştı).

| # | Sonuç |
|---|---|
| 1 | düzeltildi: KURALLAR E K1–K3 satırları H → K (kaynak NotebookLM, GLOSSARY "Hazırlık" birinci el ister); dizin altına "ikinci el tek başına kural olmaz; bizim okumamız (YORUM) olarak benimsenir, birinci el kaynak bulunana dek" cümlesi |
| 2 | düzeltildi: E:9 "tanımlar GLOSSARY'de" ve etiket kullanımı |
| 3 | düzeltildi: KURALLAR dizininde değerler (lot formülü, SMA250, 2 ATR, %50, VIX açıklaması) kaldırıldı; satırlar kural adı, A–E bölümü, Hazırlık |
| 4 | düzeltildi: §4 AB=CD hedefi "C §3, §5" |
| 5 | düzeltildi: EMA oran formülü yalnız §3 aile 2'de; §4 satırı atıf. Tur 1 raporundaki "tek yerde" iddiası A13 satırında düzeltildi |
| 6 | düzeltildi (yerel M): T5 Clenow formülü (B §15); D1 oran formülü, D2 pk123 oranları, C3 OBV tanımı, formül satırı (OBV, pivot, realize vol), Trident ve Fib merdiveni oranları atıfa çevrildi; kalan taramada başka A–E formül kopyası bulunmadı |
| 7 | düzeltildi: E K5 madde 5: dolum YORUM; TASARIM kısmi kârı ve iz süren stopu erteledi (TASARIM:373) |
| 8 | düzeltildi: B:54 ve B §2'deki bir günlük hareket yüzdesi kaldırıldı ("bir günlük sert hareket"; rakam yok); B:57 ve kanıt satırı da rakamsız |

**AÇIK (kapanmadı):**
- TASARIM çift satırları (bilet 03/07 işi; bu dalda değişmez): `docs/TASARIM.md:437–438`, `:535–537`, `:550–552`.
- Okunamayan iki görsel: ICBCT ilk EMA etiketi (20 ya da 30) ve G-125 stop sayısı. Bilet kutuları 11 ve 12 ile hiza-c-istem işaretsiz kalır.

Kapı: ruff, pytest, kapsam ve LF sonuçları commit sonrası nihai yanıttadır.

## Denetim tur 3 (Codex, 14.10): KALDI; yeniden tanım 04b

Kök neden: yazıcı kısmi taramayla "kopya kalmadı" dedi; getiri kontrolü raporun kendisine uygulanmadı.
- M:418 stop formülü → C §7 atfı (yerel taslak; 04b tur 1: §6 yazılmıştı, düzeltildi).
- Rapor madde 8 satırındaki rakam kaldırıldı.
- K E risk tablosu: K1–K3 notu tablonun altına alındı; satırlar 61–63 tabloya döndü.
- Açık kalan: TASARIM tekrar satırları (bilet 03/07 takibi); ICBCT etiketi ve G-125 rakamı okunamıyor.

## 04b denetim tur 1 (Codex, 14.10): KALDI

- (a) M:418 atfı C §7 oldu. (d) Rapor satır 117'deki yüzde kaldırıldı.
- (c) 04b tur 2 (KALDI) sonrası düzeltildi: M ve T8'deki 13 formül kopyası ve ek taramada bulunanlar sahip bölüme atıf oldu (liste aşağıda). Satır numaraları düzeltme öncesi hâlidir; taslaklar git dışıdır.
  - `Close < zone_low`: M:132; T8:270, 315–316 → A §9.
  - `CD = 1.27 AB`: M:338 → C §12 (Trident formülüyle karşılaştırma).
  - A/D platform ifadesi: M:350; T8:427 → B §12.
  - Clenow yıllıklandırma ifadeleri: T8:100 → B §15.
  - ΔZ formülü: M:421, 436–437 → D "Çift sistemi çekirdeği" 2b (D başlıklarında numara yok).
  - Risk boyutu ve acil stop: M:373 → E K1–K2.
  - Bullish FVG eşitsizliği: M:414; T8:150, 288 → A §1, §10.
  - Gartley D formülü (ters yön): M:432 → C §7.
  - Gartley AD hedefleri: M:459; T8:188–189 → C §7.
  - Trident D: T8:142 → C §12.
  - CD hedef merdiveni: T8:143–144, 188 → C §11.
  - Fincan hedefi: T8:172, 193, 421 → B §21.
  - APO: T8:427 → B §13.
  - Ek tarama: AB=CD D formülü ve 1,272 CD uzantısı T8:122–123 → C §3, §3–4; Kelebek B/D oranları T8:125 → C §8; Gartley B/C/D oranları T8:128 → C §7.

## 04b denetim tur 3 (Codex, 14.10): KALDI; yeniden tanım 04c

Kök neden: taslaklar A–E'nin okunmasından türeyen çalışma belleğidir; her turda yeni "eşdeğer formül" bulunur, atıfla bitmez. Yeniden tanım (04c): açık kapsam istisnası. AGENTS sahip tablosuna satır eklendi (taslaklar olgu sahibi değil, sapma denetimi dışı); `hiza-c-istem.md` kapsamından çıkarıldı; bilet 04 metni güncellendi. Taslaklardaki formül kopyaları bu kararla bulgu değildir; iki taslağın geçerlilik notu sahibi gösterir. Not: dalda başka bir oturumun commit'i var (e3d27e9, AGENTS ve PR şablonu, 2 satır).

## 04c denetim tur 1 (Codex, 14.10): KALDI

- Kapsam cümlesi tek: düzeltildi (`hiza-c-istem.md:36`, bilet `04-kurallar-katalog.md:5–6`, `spec.md:42–43`); hepsi "taslaklar AGENTS sahip tablosunda olgu sahibi olmayan öneriler olarak listelenir, sapma denetimi dışındadır".
- ÇELİŞKİ B:312, B:393, C:641 ↔ GLOSSARY:11–12: düzeltildi (B:312, B:393 "ikinci el, aktarılan tweet"; C:641 "yazarlığı belirsiz, ikinci el").
- ÇELİŞKİ E:230, E:354–357 ↔ C:241, C:266: düzeltildi (E:230 ve E:357 Gartley R/R eşiği için C §7'ye atıf).
- TEKRAR C:687 ↔ A:85–88: düzeltildi (C:687 A §3 atfı).
- TEKRAR E:68, 81, 95, 105 ↔ TASARIM:304, 363: düzeltildi (yalnız TASARIM 5.3 ve 5.5 atfı kaldı).
- TEKRAR E:431 ↔ C:187–188; E:455 ↔ B:328–329: düzeltildi (sonuç sayıları kaldırıldı; E:455 eşik için B §20 atfı).
- Denetim onay kutusu işaretsiz; tur 2 bekliyor.

## 04c denetim tur 2 (Codex, 14.10): KALDI

- B:316 görsel birinci el, tweet metni ikinci el diye ayrıldı.
- C:620 "yazarlığı belirsiz, ikinci el" (C:641 ile aynı sınıf).
- E:431 sayımlar sahibine: SMRTG/ISKPL C §5; makine öğrenmesi E K24.
