# Spec: Tansu MVP (TASARIM §7 adım 2–10)

Status: ready-for-agent

Kaynak belgeler:
- `docs/TASARIM.md` (taslak 7)
- `docs/KURALLAR.md`
- `GLOSSARY.md`
- Gerekçeler: `docs/sorgu/sonuc-3-4.md` ve `docs/sorgu/izleme/karar.md`

Bu spec o belgelerin yerini almaz. Hangi davranışın inşa edileceğini ve nerede sınanacağını söyler. Belge ile
spec çelişirse belge geçerlidir.

## Problem Statement

Levent BIST'te Tansu'nun paylaştığı kurulumlarla işlem yapmayı düşünüyor. Elinde iki şey var:
- Tansu'nun seçilmiş örnekleri
- 05.10'daki güvenilmez bir ön deneme (Yahoo verisi, Tansu'da olmayan çıkışlar)

Ortada hangi kuralın gerçekten işe yaradığını, şanstan ve piyasanın genel yükselişinden ayırarak
gösteren bir şey yok. Kod da yok: prototip silindi. Levent teknik değil, soru cevaplamak istemiyor ve parayı
kendisi tutuyor. Her akşam tek bir dosyaya bakıp "bugün ne oldu, hangi kural sağlandı, bu kurala güvenebilir
miyim" sorusunun dürüst cevabını görmek istiyor.

## Solution

Windows bilgisayarında kendi kendine çalışan bir sistem. Sistem şunları yapar:

1. İş Yatırım'dan ham ve düzeltilmiş fiyatı ve şirket olaylarını indirir. Veriyi denetler ve değişmez bir
   anlık görüntüye koyar.
2. Tansu'nun iki kuralını (çift rotasyonu, EMA sıkışması) önce onun ekranındaki rakamlarla sadakat
   kontrolünden geçirir. Sonra kuralları kayda alır (hash).
3. 2015–2026'yı gerçekçi dolumla (ertesi gün AOF, kilit, masraf, likidite) bir kez simüle eder.
   - Kuralı, aynı şartlardaki rastgele kuralla (K1) karşılaştırır.
   - Kuralı, maruziyeti eşlenmiş evren sepetiyle (K2) karşılaştırır.
   - Holm düzeltmesiyle "geçti", "geçmedi" ya da "ölçülemedi" der.
4. Geçen aileyi Kâğıt durumuna alır. Her akşam 19:30'da kart CSV'si, tek sayfa HTML rapor ve `durum.txt`
   üretir.
5. Asla "AL" demez. Kararı ve parayı Levent tutar.

## User Stories

**Veri**
1. As Levent, I want the system to download prices from İş Yatırım by itself, so that I never have to fetch
   data by hand.
2. As Levent, I want every run to use a dated, unchangeable data snapshot, so that a past result can be
   reproduced exactly.
3. As Levent, I want bonus issues, splits, rights issues and dividends to be handled from the official event
   table, so that a corporate action never looks like a breakout or a crash.
4. As Levent, I want the system to check its own corporate-action math against İş Yatırım's adjusted price,
   so that I can trust the adjustment.
5. As Levent, I want days with an unexplained price jump to be quarantined instead of patched, so that bad
   data never creates fake profits.
6. As Levent, I want the system to compare every return against a second source (borsapy), so that data
   errors are caught before they reach a card.
7. As Levent, I want the run to refuse to produce cards when the data fails its checks, so that I never act
   on broken data.
8. As Levent, I want the system to know the price limit for every day (±20% before 13.03.2020, ±10% after),
   so that locked limit days are modelled honestly.
9. As Levent, I want delisted stocks to stay in the history, so that survivors do not make the results look
   better than they are.
10. As Levent, I want the interest rate on idle cash to come from one TCMB policy-rate series, so that cash is
    neither free nor overstated.

**Evren**
11. As Levent, I want each month's universe to be the 100 largest stocks by the previous month-end market
    value, minus the least liquid 20%, so that no future information leaks into the stock list.
12. As Levent, I want an open position to stay open when its stock leaves the universe, so that exits follow
    the rule, not the list.
13. As Levent, I want a stock that stops trading to count as −100% unless the reason is known, so that
    delistings are never quietly ignored.

**Sadakat**
14. As Levent, I want the EMA squeeze rule to reproduce Tansu's KRDMD numbers (period 17.12.2025–14.01.2026,
    average 0.64%), so that I know the rule is read correctly.
15. As Levent, I want the pairs rule checked against Tansu's VAKBN–GARAN report (Z −3.108 / −3.404, Beta
    1.675, correlation 0.731, 72.27% invested), so that its gaps are known before testing.
16. As Levent, I want the fidelity check never to look at returns, so that parameters are not tuned to
    profit.
17. As Levent, I want one command to reproduce the fidelity numbers at any time, so that a later code change
    cannot silently break fidelity.
18. As Levent, I want the parts that cannot be reproduced to be labelled YORUM in the report, so that I know
    which parts are our guesses.

**Aileler**
19. As Levent, I want the pairs-rotation rule to choose pairs each year by a fixed, written rule (same
    sector, cointegration p < 0.05, at most 5 pairs, at most 2 per sector), so that Tansu's hand-picked
    pairs do not flatter the result.
20. As Levent, I want the pairs rule to switch between the two stocks at Z ±2 with a ΔZ turn, using the next
    day's AOF, so that it matches Tansu's rule.
21. As Levent, I want the EMA squeeze rule to signal a breakout above the squeeze period's high within 10 days
    after the squeeze ends, so that the entry is clear and testable.
22. As Levent, I want no signal from a stock that has too little history (500 days single stock, 252 days
    pairs), so that indicators are valid.

**İşlem ve risk**
23. As Levent, I want every trade to fill at the next day's AOF, never at a price that was not available, so
    that the backtest is achievable.
24. As Levent, I want a stop hit to fill at the worse of stop and AOF, so that gaps are not hidden.
25. As Levent, I want no entry on a day that closes at limit-up and no exit on a day that closes at limit-down,
    so that locked days are honest.
26. As Levent, I want Tansu's risk package (1% risk, 2-ATR stop, exit on a close below SMA250), so that I test
    his rules, not ours.
27. As Levent, I want each position limited by risk, the 10% cap, the 2% liquidity cap and available cash, so
    that the simulated portfolio is buyable.
28. As Levent, I want the report to show how often the 10% cap binds and the real risk taken, so that "1%
    risk" is not misleading.
29. As Levent, I want costs of 0.1%, 0.3% and 0.5% per side, with acceptance required at 0.5%, so that small
    edges eaten by costs are rejected.

**İstatistik ve kabul**
30. As Levent, I want each rule compared with random entries under the same conditions (K1), so that luck is
    separated from skill.
31. As Levent, I want each rule compared with an equal-weight basket of the same universe that is invested
    exactly as much as the rule (K2), so that market drift and idle cash do not decide the result.
32. As Levent, I want the number of random repeats to grow with the number of trials (B ≥ max(1000, 200·m)),
    so that passing Holm stays possible.
33. As Levent, I want every test run logged append-only with its rule fingerprint, so that I can see how many
    things were tried.
34. As Levent, I want Holm correction over all trials, so that trying many variants does not produce a false
    winner.
35. As Levent, I want results shown year by year, so that one lucky year cannot carry a rule.
36. As Levent, I want "could not be measured" shown separately from "failed", so that a too-small sample is
    not read as proof of failure.
37. As Levent, I want a six-criteria pass/fail table per family, so that I can see exactly why a family
    passed or failed.
38. As Levent, I want the rule and its parameters fingerprinted before the first return run, so that anything
    after that is a true out-of-sample period.
39. As Levent, I want the pipeline checked once on fake null data and on injected effects before the first
    official run, so that I know the test itself is not broken.

**Günlük işleyiş**
40. As Levent, I want the system to run every weekday at 19:30 without me, so that I only read the results.
41. As Levent, I want one file whose first line says TAMAM, SORUNLU, VERİ YOK or BUGÜN ÇUBUK YOK, so that I know
    in one second whether to trust tonight.
42. As Levent, I want a missed run to happen when the computer next starts, and a failed run to retry, so
    that a closed laptop does not lose a day.
43. As Levent, I want a daily card CSV that opens correctly in Turkish Excel, so that I can read signals
    without tools.
44. As Levent, I want each card to show the raw TL reference price, an estimated stop, the size and the real
    risk, so that I can act in my broker if I choose.
45. As Levent, I want each card to carry its family's evidence line, so that I never see a signal without its
    track record.
46. As Levent, I want only Kâğıt and Canlı families on cards, so that untested rules do not tempt me.
47. As Levent, I want paper-trading results logged append-only, so that the paper period cannot be rewritten
    later.
48. As Levent, I want a single HTML report with one "Uyarılar" section, so that all data problems are in one
    place.
49. As Levent, I want the system never to say "AL" or "Tansu'nun sistemi", so that it does not pretend to
    give advice.

**Bakım**
50. As an agent working in the repo, I want a fixed reading order, a test gate and a ban on loosening tests,
    so that I cannot quietly break the evidence.
51. As an agent, I want tests that never touch the network or the real logs, so that tests are hermetic.
52. As Levent, I want the real BIST100 history rebuilt from KAP announcements as a side task, so that the
    interim universe can later be checked.

## Implementation Decisions

**Modüller** (TASARIM §4). Paket düz yapıdadır. Bağımlılık yönü tek yönlüdür:

`kaynak` → `veri` → `evren`, `gostergeler` → `aileler`, `cift` → `motor` → `simulator` → `istatistik` →
`kayit` → `rapor` → `__main__`

**Modüllerin yüzleri:**
- `kaynak`: ağa çıkan tek modül.
  - İş Yatırım `HisseTekil` ve `GetSermayeArttirimlari`, borsapy (faiz, sektör, endeks günleri,
    karşılaştırma getirileri).
  - Ham alan adları tek bir sözlükle proje adlarına çevrilir.
  - requests; istekler arası 1 sn; zaman aşımı (5, 120); ağ, 429 ve 5xx için 3 deneme.
- `veri`: `indir(tarih) → anlık görüntü kimliği` ve `oku(kimlik) → fiyat, olaylar, faiz, sektör, günler`.
  - Anlık görüntü tek klasördür: uzun biçimli parquet, ham olay JSON'u, borsapy tabloları ve
    `manifest.json` (sha256).
  - Önce geçici klasöre yazılır; veri kapılarından (TASARIM 5.13) geçerse `os.replace` ile yerine taşınır.
  - Okurken manifest doğrulanır.
  - Olay denetimi, karantina, fiyat limiti, fiyat adımı ve kilit tespiti bu modüldedir.
- `evren`: `evren(tarih) → semboller`. Ay başı, önceki ay sonu piyasa değeri, likidite eleği, şirket başına
  tek kod.
- `gostergeler`: EMA (`ewm(adjust=False)`), SMA, Wilder ATR(14), sıkışma oranı, piyasa durumu (XU100 >
  SMA50). Vektörel; sınamada ve canlıda aynı kod.
- `aileler`: `sinyal(fiyat, parametre) → sinyal günleri`. Yalnız EMA sıkışması.
- `cift`: yıllık çift seçimi ve Z/ΔZ geçiş günleri.
- `motor`: `adim(pozisyon, mum) → pozisyon` saf bir fonksiyondur.
  - Mum, ön hesaplı ATR ve SMA250 sütunlarını içerir.
  - Motor sinyallerden işlem listesi üretir.
  - Dolum, kilit, SMA250, veri sonu ve aynı gün sırası kuralları TASARIM 5.3'tedir.
- `simulator`: iki bölme (tek hisse, çift), boyutlandırma (dört sınırın en küçüğü), nakit faizi, sermaye
  eğrisi, K2 sepeti.
- `istatistik`:
  - K1 permütasyonu; p = (1 + k) / (1 + B).
  - Blok bootstrap; blok = max(20, ortalama tutma süresi).
  - Holm (statsmodels), saptanabilir en küçük etki.
- `kayit`:
  - `kosu()`, getiri gösteren tek yoldur.
  - Kural kaydı: elle yazılmış kod dosyası listesinin `ast.dump` sha256'sı + parametreler + ızgara.
  - `deneme.jsonl` (`basladi`/`bitti`, `tur` alanı, alanlar TASARIM 5.11'de) ve `kartlar.jsonl`; ikisi de
    yalnız ekleme.
  - Aile durumu: Deneme / Kâğıt / Canlı.
- `rapor`:
  - HTML (f-string), `kartlar-YYYYMMDD.csv`, `islemler-<koşu>.csv`, `durum.txt`.
  - Tek biçim yardımcısı.
  - Yasaklı sözcükler: AL, SAT, ÖNERİ, "Tansu'nun sistemi".
- `__main__`: `gunluk [tarih] | sinama [--son] | sadakat | kayit`. Yakalanmayan istisna çıkış kodu 1 verir.

**Mimari kararlar:**
- vectorbt, Yahoo, Streamlit ve veritabanı yok.
- Açık kartlar ayrıca saklanmaz; her gün Adım ile yeniden hesaplanır.
- Parametreler kodda, donmuş dataclass olarak tutulur.
- Bağımlılıklar `pyproject.toml`'da `==` ile sabitlidir.

**Sıra** (her madde bir ya da daha çok bilet olur):
1. Kullanım koşulları ve fiyat adımı doğrulaması (araştırma).
2. `kaynak` + `veri`.
3. Sadakat (`gostergeler` + `cift` çekirdeği).
4. `evren`.
5. Kural kaydı.
6. Adım + Motor.
7. Simülatör + faiz + K2.
8. K1 + istatistik + günlük + boru hattı denetimi.
9. İlk resmi koşu + rapor + `gunluk` + Görev Zamanlayıcı.
10. KAP evreni (paralel, engelsiz).

**Ortam:** Windows Görev Zamanlayıcı tanımı depoda XML olarak durur. Kurulumu bir kez elle yapılır;
`schtasks` komutu verilir.

## Testing Decisions

**İyi test:**
- Yalnız dış davranışı yüzden sınar.
- Beklenen değer bağımsız bir elle hesaptan gelir, kodun yaptığı gibi yeniden hesaplanmaz.
- Sabitler literal yazılır.
- Ağa çıkmaz; gerçek `kayit/`'a yazmaz (conftest yolu `tmp_path`'e yönlendirir).
- Paket 60 saniyenin altında koşar.
- Testi gevşetmek yasaktır (AGENTS.md).

**Sınama yüzleri** (dört; mümkün olan en yüksek yüz seçildi):

1. **`veri` yüzü** (sahte `kaynak` adaptörüyle). Elle yazılmış küçük ham tablolardan anlık görüntü üretilir.
   Sınananlar:
   - CCOLA 13.08.2024 olay çarpanı ↔ HGDG
   - ±1 gün olay eşleşmesi
   - aynı güne iki kayıt
   - karantina
   - limit tabanı (normal gün ve olay günü)
   - kilit
   - veri kapıları
   - manifest doğrulaması
   - eksik gün
2. **Adım/Motor yüzü.** Elle yazılmış sentetik mumlarla TASARIM 5.3'teki 14 motor durumu. Beklenen işlem
   listesi ve fiyatları elle hesaplanır. Hesabı kodu yazmamış ayrı bir ajan yapar.
3. **`kosu()` yüzü** (en yüksek yüz). Küçük sentetik bir anlık görüntü ve sabit tohumla uçtan uca sınanır:
   - simülatör boyutlandırması ve bölmeler
   - K2 maruziyet eşleşmesi
   - K1 p tabanı, Holm (elle örnek: [0,01; 0,04; 0,03; 0,005] → [0,03; 0,06; 0,06; 0,02])
   - deneme günlüğü satırları
   - aynı tohum → aynı özet
   - "veriyi t'de kes, t öncesi sinyaller değişmesin" testi
   - sentetik boş veri ve enjekte edilmiş etki
   - rapor sütunları ve yasaklı sözcükler
4. **`gunluk(tarih)` yüzü.** Durum dosyasının ilk satırı (dört değer), bugünün koşusu varsa çıkış,
   kart CSV'sinin biçimi ve "sinyal yoksa yalnız başlık".

**Ayrıca:**
- Sadakat kontrolü, `python -m tansu sadakat`'ın KRDMD rakamlarını üretmesiyle sınanır.
- Göstergeler (EMA, Wilder ATR) yalnız `kosu()` ve sadakat üzerinden dolaylı değil, birkaç satırlık elle
  hesaplı örnekle de sınanır. Hata yeri belli olsun diye `gostergeler` istisnai bir alt yüzdür.
- Kapsam testi: her `tansu/*.py`, ya kural kaydının kod listesinde ya hash dışı listesinde.

**Önceki örnek:** Silinen prototipin elle hesaplı motor testleri (9,58% ve −5,39%) git geçmişindedir; biçim
olarak örnek alınabilir, değerleri değil.

## Out of Scope

- AB=CD, AEFES kanal, AKFIS kurulumu, fiili dolaşım taraması (ikinci dalga).
- Panel (Streamlit), Telegram, veritabanı, yedek.
- İz süren stop, kısmi kâr, süre çıkışı.
- Dolar bazı karşılaştırma, gün içi veri, emir verme.
- Vergi modellemesi.
- Sembol değişikliği ve birleşme sürekliliği.

## Further Notes

- Açık olgular biletlerin içinde veriyle çözülür (TASARIM §8): kullanım koşulları, fiyat adımı, ±%20
  döneminde limit tabanı, hacmin içeriği, faiz serisinin türü, çift Z formülü.
- Çift Z formülü bulunamazsa YORUM kalır: log oran, 60 gün.
- En olası sonuç, iki ailenin de geçmemesidir. Bu sistemin başarısızlığı değil, normal çıktısıdır.
- Her bilet `/implement` ile ayrı oturumda yapılır; biletler engel sırasıyla ilerler.
