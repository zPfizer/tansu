# Cevaplar 19: Hesap çekirdeği

Doğrulama aracı: `.venv` (Python 3.14.7, pandas 3.0.6, numpy 2.5.3, numba 0.68.0, pyarrow 25.0.1, joblib 1.6.0, statsmodels 0.15.0, pandas-ta-classic 0.8.32). Kurulu DEĞİL: TA-Lib, quantstats, arch, hypothesis, polars, pandera.
"Ölçtüm" = `python -` ile stdin'den çalıştırdım, dosya kaydetmedim. Ölçümler oyuncak veriyle (sentetik rastgele yürüyüş).

**19-001** — KARAR — Mum = Adım'a ayrı skaler argümanlar: `adim(poz, yuksek, dusuk, kapanis, aof, ...)`; `poz` düz tuple. Motor gün×hisse 2B float64 dizilerinden dilimler; canlı günlük aynı dizilerin son satırını verir. Aynı fonksiyon, aynı giriş.

**19-002** — KARAR — Aile ve gösterge: hisse başına DataFrame sözlüğü (mevcut sözleşme). Motor girişinde bir kez gün×hisse 2B numpy float64 dizilerine çevrilir (NaN = o gün satır yok). Uzun biçim yok.

**19-003** — KARAR — Ortak eksen = Takvim modülünün işlem günleri. Eksik gün NaN kalır, ileri doldurma yok. NaN günde sinyal ve giriş yok; açık pozisyon varsa yalnız sermaye eğrisi son bilinen kapanışla taşınır.

**19-004** — KARAR — MultiIndex kullanılmaz. Ölçtüm: düz `shift(1)` MultiIndex'te sınırı aşar (A'nın son değeri B'ye geçti); `groupby(level=0).shift` NaN verir. Hisse başına DataFrame'de sorun yok; kanıt 19-050'deki kısaltma testidir.

**19-005** — CEVAPLI — `aileler.py:16,19` sözleşmesi (DataFrame → Series) korunur; evren tek çağrıda işlenmez. 100 hisse × 2.750 satırlık ewm/rolling milisaniye mertebesidir (süreyi ölçmedim; ilk koşuda 19-097 ölçer).

**19-006** — KARAR — Polars yok. Kurulu değil (doğruladım), veri 17 MB, pandas 3.0.6 yeter; dönüşüm riski hiç doğmaz.

**19-007** — KARAR — float64. 100×2.750×8 sütun×8 B ≈ 17,6 MB; float32 bellek kazancı anlamsız, 7 haneli duyarlık yalnız hata kaynağıdır.

**19-008** — KARAR — Tick'e yuvarlanmaz: AOF zaten ortalamadır, stop modeldir. Sapma en çok bir tick; çoğu BIST100 fiyatında ~%0,1–0,2 (tick tablosu bellekten, doğrulamadım). %0,5 masraf senaryosu bunu kapsar; rapora bir cümle yazılır.

**19-009** — KARAR — Decimal/kuruş yok. float64 göreli hata 1,1e-16; 2.750 çarpımda ≤ ~3e-13 (analitik, ölçmedim); %0,3 masrafın çok altında.

**19-010** — KARAR — Fark sayılır eğer `|bizim − HGDG| > 0,005 TL + 1e-6 × HGDG` (yarım kuruş yuvarlama + göreli). 1e-12 sapma görünmez. İş Yatırım'ın yuvarlama biçimi doğrulanmadı; ilk koşuda farkların dağılımı bakılıp eşik bir kez sabitlenir.

**19-011** — KARAR — İki ayrı DataFrame: `duz` ve `ham`, aynı indeks, ayrı sütun adları (`kapanis` / `kapanis_ham`). Aile fonksiyonu yalnız `duz` alır; limit ve likidite fonksiyonu yalnız `ham` alır. Tip sistemi yok; test: aile `ham` olmadan çalışır.

**19-012** — KARAR — Katsayı olay satırı başına tek orandır (`SHHE_FIYAT_AYAR_OR`). Çarpma sırasızdır, aynı güne denk gelen olaylar tek çarpımda birleşir; sıra hatası doğmaz. Yanlış oran ya da gün sessiz kalmaz: HGDG karşılaştırması (§5.1) listeler.

**19-013** — KARAR — Bloke yok. Çekirdek `tutar_tl` sütununu alır; lot→TL dönüşümü veri deposunda yapılır (ilk veri işi, HACIM×fiyat karşılaştırması). Likidite testleri sentetik TL ile yazılır.

**19-014** — KARAR — Karantina (o hisse-gün). Kırpma ve yamama yok (§5.1 "fiyat yamanmaz"). Satır listelenir.

**19-015** — KARAR — Evet, veri deposu çıkışında tek `dogrula(f)` (assert): `dusuk ≤ {kapanis, aof} ≤ yuksek`, fiyat > 0. Satır ihlali → karantina ve liste, koşu sürer. Yapısal ihlal (sıra, tekrar, ortada NaN) → ValueError, koşu durur.

**19-016** — YANLIŞ — `aileler.py:19-20` EMA'yı ilk fiyatla tohumlar; ilk `gun` değeri atmak tohum etkisini silmez. Ölçtüm (el özyinelemeli SMA tohumuna göre): EMA20 ilk geçerli günde %0,21 sapar, 100. günde 8e-7; EMA200 199. günde %3,3, 600'de %0,08, 1.000'de 2e-5. pandas-ta-classic `ema` SMA tohumlu ve el özyinelemesiyle fark 0,0 (ölçtüm). TA-Lib kurulu değil, karşılaştırılmadı. Düzeltme: `pta.ema`.

**19-017** — KARAR — Şimdilik NaN karşılaştırmasının yan etkisidir; yazılı değil. Karar: ısınma tamamlanmamış günde sinyal yok; ısınma = 2 × en uzun pencere (EMA200 için 400 gün). TASARIM §5.1'e bir satır.

**19-018** — KARAR — Üç değerli mantık yok. Tek `isinmis` bool maskesi ayrı tutulur; sinyal = koşul ∧ isinmis; rapor "ısınmamış gün" sayısını yazar.

**19-019** — KARAR — Hissenin kendi ilk gününden ısınır. Girişe izin = evren üyeliği ∧ isinmis ∧ karantinada değil (üç maske AND).

**19-020** — KARAR — Isınma sıfırlanır: seri karantina penceresinde segmentlere bölünür, her segment kendi ısınmasıyla başlar. Karantinada sinyal yok; açık pozisyon pencere öncesi son kapanıştan kapatılır.

**19-021** — OLGU — Duyarlılık gerçektir (19-016 rakamları: EMA200'de 400. günde ~%0,6). Ölçülecek: ilk koşuda başlangıç 250 gün kaydırılıp ısınma sonrası sinyal günlerinin farkı sayılır, raporda yazılır. Eşik yok.

**19-022** — OLGU — Doğruladım: pandas-ta-classic EMA = el yazımı SMA tohumlu EMA (fark 0,0); ATR = el yazımı Wilder, ilk 14 TR ortalamasıyla tohumlu (göreli fark 1,3e-15). TA-Lib kurulu değil, kurulmaz. Test: `tests/`'e sabit bir girdi, el özyinelemesiyle eşitlik (EMA, ATR, SMA).

**19-023** — KARAR — `pandas-ta-classic==0.8.32` pyproject'te kilitli. Sürüm değişirse 19-022 sabit-değer testi patlar; yükseltme ancak test geçince yapılır.

**19-024** — KARAR — TA-Lib alınmaz (C bağımlılığı, kazanç yok, kurulu değil). Gösterge: kurulu pandas-ta-classic (EMA, ATR); SMA: `rolling.mean`.

**19-025** — KARAR — Wilder (alfa = 1/14), SMA tohumlu (pandas-ta varsayılanı, ölçtüm: standart EMA 2/15 ile %20, SMA ile %23 farklı). Seçim YORUM olarak yazılır; yalnız bir değer denendiği için deneme sayısına 1 katkı eder.

**19-026** — OLGU — Ölçtüm: pandas-ta ATR ilk geçerli değeri 14. indekste; ilk günün TR'si atılır, TR[1..14] ortalaması tohum olur. İlk günün TR'si zaten High−Low olur (NaN değil), ama kullanılmaz.

**19-027** — KARAR — ATR düzeltilmiş seride hesaplanır (bedelsiz günü sahte aralık yok). Karantina segmentinde TR yeniden başlar (19-020). Veri boşluğunda önceki kapanış = önceki mevcut satır. Hata yayılmaz: ısınmamış → NaN → sinyal yok.

**19-028** — KARAR — Aday kümesine `ddof` eklenir (KURALLAR §3'te yok): {log oran, β'lı kalıntı} × {60, 120} × {ddof 0, 1} = 8 aday. ddof farkı z'yi √(60/59) ≈ %0,84 oynatır (aritmetik): −3,108 üçüncü basamakta duyarlıdır. Tansu'nun −3,108 / −3,404 rakamlarını en iyi üreten seçilir ve kaydedilir.

**19-029** — KARAR — pandas: `β = y.rolling(w).cov(x) / x.rolling(w).var()`. `RollingOLS` ve `lstsq` yok (ağır, gereksiz). Pencerede NaN → tam pencere zorunlu, z NaN, sinyal yok. Log fiyatta var > 0.

**19-030** — OLGU — Ölçtüm: `coint` 252 noktada 2,8 ms/çağrı. Yaklaşık 340 çift × 11 yıl ≈ 3.700 çağrı ≈ 10 saniye (çift sayısı varsayım). Süre sorun değil; MacKinnon p kararlılığı ölçülmedi, sabit sürüm yeter.

**19-031** — KARAR — Düzeltilmiş log fiyat. Düzeltilmiş seri geriye ölçeklenir, düzeltme gününde süreksiz değildir; ham seri bedelsiz gününde kırılır. Ham kullanılmaz.

**19-032** — OLGU — Ölçtüm: 100×2.750 = 275k adımlık basit döngü 0,03 s (0,1 µs/adım); her adımda frozen dataclass üreten fonksiyon 0,21 µs. 1.000 perm ≈ 275M adım ≈ oyuncakta 30–60 s; 2–5 µs varsayımı kötümser. Gerçek Adım ölçülmedi; hedef süre 19-033'te.

**19-033** — KARAR — Bütçe: 200 perm ≤ 5 dk, 1.000 perm ≤ 30 dk (tek aile × masraf × giriş türü). Aşılırsa 19-097 sırasıyla hızlandırılır; aşılmazsa optimizasyon yok.

**19-034** — ZAYIF SORU — Ölçtüm: dataclass döndüren adım 0,21 µs; tahsis baskın değil. Poz yine de düz tuple olur; struct-of-arrays yok.

**19-035** — KARAR — Numba şimdi yok. Python 3.14.7'de numba 0.68.0 import 0,26 s, ilk JIT çağrı 0,22 s (ölçtüm); çalışıyor ama sürüm riski var. Yalnız 19-097 ölçümü gerektirirse son çare.

**19-036** — KARAR — Numba kullanılmadığı için konu yok. Kullanılırsa `cache=False`.

**19-037** — KARAR — Numba yok; "aynı fonksiyon" = aynı Python fonksiyonu. Numba gelirse `fastmath=False`, test toleransı göreli 1e-9 (bit eşitliği aranmaz).

**19-038** — KARAR — Çoklu işlem şimdi yok. Gerekirse `joblib` (1.6.0 kurulu, 32 çekirdek, ölçtüm). Veri 17 MB; başlatma maliyeti ölçülmedi, ihmal edilebilir sayılır.

**19-039** — KARAR — Her permütasyon gerçek motoru (Adım + Simülatör) koşar; vektörleştirilmiş kısayol yok (ikinci uygulama olur, eşitlik testi ister). Rastgele sinyaller listesi motora verilir.

**19-040** — KARAR — Uygun gün maskesi bool 100×2.750 ≈ 275 KB (aile başına). Bellekte kalır; her permütasyonda indisler yeniden örneklenir.

**19-041** — KARAR — `np.random.default_rng` (PCG64). Alt tohum: `np.random.SeedSequence(tohum).spawn(N)[i]`. Ana tohum deneme günlüğüne yazılır.

**19-042** — KARAR — Perm i'nin tohumu i'den gelir, işçi sayısından bağımsız. Sonuçlar indekse göre yazılır, p değeri tamsayı sayımıdır (kayan toplam sırası yok). Test: `n_jobs=1` ile `n_jobs=4` aynı p.

**19-043** — KARAR — Düzey: aynı makine ve aynı kilitli sürümlerde bit düzeyinde aynı. Test: aynı koşu iki kez, özet eşit. Farklı sürümde garanti yok; kilit bunun içindir.

**19-044** — YANLIŞ — Doğru: `pyproject.toml` yalnız pytest ayarı içerir (okudum). Düzeltme: `dependencies` `==` ile kilitli (numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, statsmodels 0.15.0, pandas-ta-classic 0.8.32, pyarrow 25.0.1, tqdm 4.70.1; sürümler `pip list`'ten doğrulandı) ve `requires-python = "==3.14.*"`. vectorbt ve yfinance bağımlılığa girmez.

**19-045** — KARAR — Düz `pip` + pyproject. Kilit = `==` sürümleri. Kurulum: `python -m venv .venv` sonra `.venv\Scripts\python -m pip install -e .`. `uv`/`pip-tools` yok (yeni araç).

**19-046** — OLGU — Hesapladım: 17,6 MB; 400 hisse ≈ 70 MB. Bellek sorun değil; tek kısıt süre.

**19-047** — KARAR — Permütasyon başına yalnız özet (ortalama günlük fazla getiri, işlem sayısı) saklanır. Gerçek koşunun eğrisi ve işlem listesi saklanır. 22 MB zaten sorun değil ama gerekmiyor.

**19-048** — KARAR — Hesapladım: perm koşusu = (2 tek-hisse ailesi × 3 masraf × 2 giriş türü + çift ailesi 3 masraf × 1 tür) × 1.000 = 15.000; sağlamlık ızgarası ≈ 20 hücre × 3 aile × 3 masraf = 180 (perm'siz; ızgara boyutu varsayım). Toplam ≈ 15.200 motor koşusu. İleri yürüme yılları ayrı koşu değil, tek koşunun dilimidir.

**19-049** — KARAR — Gösterge bir kez tüm seride hesaplanıp dilimlenir (nedensel göstergeler). Kanıt: 19-050 testi.

**19-050** — KARAR — Evet, tek pytest: her aile ve pivot için `sinyal(f[:t]) == sinyal(f)[:t]`, t ∈ {400, 700, uzunluk−1} (ısınma sonrası). Likidite medyanı ve faiz hizalaması da aynı testten geçer.

**19-051** — KARAR — Pivot serisi teyit gününe yazılır (pivot günü + k); sinyal yalnız o günden sonra. 19-050 testi geleceğe bakmayı yakalar.

**19-052** — KARAR — Kendi pencere kuralı (scipy yok, sürümden bağımsız): gün i tepedir eğer `yuksek[i]` önceki k günden kesin büyük ve sonraki k günden büyük-eşit. Düz tepede ilk (en eski) gün geçerli. Dip simetrik.

**19-053** — YANLIŞ — `aileler.py:27` `rolling(10).sum() >= 3` 10 günde toplam 3 gündür (ardışık olmayabilir); KURALLAR §3 "en az 3 gün" bir sıkışma dönemidir (KRDMD: 20 gün) → ardışık. Düzeltme: `(bant <= 0.012).rolling(3).min() == 1`; tanım KURALLAR §3'e bir cümleyle yazılır. (Aynı dosyadaki hacimli 20 günlük kırılım da KURALLAR giriş kuralından farklı; ön deneme kodu.)

**19-054** — KARAR — Aile DataFrame döndürür: `sinyal` (bool), `atr`, `stop`, `hedef` (NaN olabilir). AB=CD'de A ve D sinyal günü `stop`/`hedef` sütununa yazılır; ATR'li ailede stop NaN ise Adım `giriş − 2·atr` hesaplar (§5.3).

**19-055** — KARAR — Bekleyen emir iptal olur, kaymaz. Giriş günü = sinyal gününü izleyen ilk satır; o satır yoksa sinyal düşer ve sayıma girmez, raporda "iptal" sayısı. Yer: Motor, Adım çağrılmadan önce.

**19-056** — KARAR — Tespit yalnız ham fiyatta: `np.isclose(yuksek_ham, dusuk_ham, rtol=1e-9)` ∧ kapanış, önceki ham kapanışın ±limit×0,995 dışında/üstünde. Düzeltilmiş fiyatta tespit yapılmaz.

**19-057** — KARAR — Limit fiyatı hesaplanmaz; kilit gözlemden bulunur (19-056). BIST'in yuvarlama kuralı TASARIM'da yazılı değil ve gerekmiyor.

**19-058** — CEVAPLI — TASARIM §5.3 "gün düşüğü ≤ stop" yazar; eşitlikte dolum olur. Yedi motor sınamasında sınır yok; sekizinci örnek eklenir: `dusuk == stop`.

**19-059** — KARAR — `adet = floor(min(risk/(2·ATR), %10·sermaye/giriş, likidite tavanı))` tam lot. Minimum 1 lot kuralı yok: 0 lot → işlem açılmaz, "yetersiz sermaye" sayacı. Gerçekleşen risk = adet × 2ATR raporda yazılır.

**19-060** — KARAR — float64. Masraf yuvarlanmaz (kuruş yuvarlama işlem başına ≤ 0,005 TL, ihmal edilebilir).

**19-061** — KARAR — Basit tahakkuk, takvim günü: `nakit *= 1 + oran(t−1)/365 × (takvim günü farkı)`. Hafta sonu faizi Pazartesi satırına biner. Yer: Simülatör. 365 konvansiyonu doğrulanmadı.

**19-062** — KARAR — t günü için t−1 sonunda bilinen oran kullanılır (bir gün gecikme); toplantı günü kararı ertesi işlem gününden geçerli. Sızıntı yok.

**19-063** — KARAR — İki işlem (sat Y, al X), her biri %0,3. İkisi aynı günün AOF'undan; alış %2 likidite tavanını aşarsa adet kırpılır, artan nakit kalır. Kilitli taban satışı ertesi güne kayar (§5.3).

**19-064** — KARAR — Günlük mark-to-market, düzeltilmiş kapanışla. Fazla getiri serisi her işlem gününde.

**19-065** — KARAR — Günlük basit getiri; sermaye eğrisi çarpımsal; bootstrap istatistiği ortalama günlük fazla getiri. Toplamsal ile çarpımsal aynı sonucu vermez, tanım her yerde aynı tutulur.

**19-066** — KARAR — Kendi örnekleyici (`arch` kurulu değil, doğruladım; TASARIM listesinde yok). Dairesel blok: `b = rng.integers(n, size=ceil(n/20))`, `idx = ((b[:,None] + arange(20)) % n).ravel()[:n]`.

**19-067** — KARAR — Dairesel; son blok n'e kesilir. Duyarlılık: ilk koşuda blok 10 ve 40 bir kez koşulur, raporlanır; ana sonuç 20.

**19-068** — KARAR — Çözünürlük `1/(N+1)` (ölçtüm 0,000999). Holm için `N ≥ 20·m − 1` (m = deneme sayısı); m ≤ 50 için 1.000 yeter. m > 50 olursa N = 20·m. Rapor N'yi yazar.

**19-069** — KARAR — `(1 + k) / (1 + N)`; sıfır p çıkmaz. TASARIM §5.7'ye bir satır.

**19-070** — KARAR — `np.percentile` varsayılan `linear`. "En iyi %5 atılmış": işlemler sıralanır, üstten `ceil(0,05·n)` atılır. Güven aralığı: 2,5 ve 97,5. Yöntem raporda yazılır.

**19-071** — YANLIŞ — `quantstats` kurulu değil (doğruladım) ve kabul ölçütleri (en büyük düşüş, düşüşte kalma) yıllandırma/risksiz oran istemez. Düzeltme: kendi 6 satır: `dd = egri/egri.cummax() − 1`; düşüşte kalma = en uzun ardışık `dd < 0` süresi (takvim günü). TASARIM §4 listesinden quantstats çıkar. Sharpe kabulde yok, yıllandırma gerekmez.

**19-072** — ZAYIF SORU — 19-071'e göre quantstats kullanılmıyor; çapraz kontrol gerekmez. Kendi hesabın el örneğiyle testi yeter.

**19-073** — KARAR — Günlük kapanış mark-to-market eğrisinden; gün içi dip yok sayılır (bilinen alt-tahmin). Ölçüt %25 aynı hesapla tanımlı, tutarlıdır; rapor "kapanış bazlı" diye etiketler.

**19-074** — KARAR — Karşılaştırma ham floatla; yuvarlama yalnız gösterimde (4 hane). p = 0,04996 geçer ve 0,0500 görünür; rapor ham değeri de yazar.

**19-075** — KARAR — Kod hash = `tansu/*.py` baytları + kilitli sürüm metni + Python sürümü. Hash aynı, sonuç farklıysa: determinizm testi (19-043) ve günlüğe yazılan sonuç özeti hash'i yakalar.

**19-076** — KARAR — Dosya baytı değil, içerik hash'i: sembol sırasıyla float64 dizilerinin `tobytes()` sha256'sı. pyarrow meta verisi kimliği bozmaz.

**19-077** — KARAR — `pyarrow` (25.0.1 kurulu; fastparquet yok). Tarih = tz'siz DatetimeIndex, gece yarısı; sütunlar float64 (hacim/tutar dahil). `dogrula` assert eder.

**19-078** — KARAR — Tz hiç kullanılmaz; tarih tz'siz saf gün. İş Yatırım tarihi gün düzeyindedir, dönüştürme yok, kayma riski doğmaz.

**19-079** — KARAR — Veri deposu reddeder (`dogrula`, 19-015). Çekirdek sıralama/tekilleştirme yapmaz.

**19-080** — KARAR — Sözleşme = veri modülünde tek `dogrula(f)` assert fonksiyonu: sabit sütun adları, float64, tz'siz artan tekil DatetimeIndex. pandera kurulu değil, pydantic tablo için uygun değil; yeni bağımlılık yok.

**19-081** — KARAR — Dahili ad Türkçe ASCII: `kapanis, yuksek, dusuk, aof, tutar_tl`; ham: `*_ham`. Çeviri yalnız veri modülünde (`HGDG_*` → düz, `HG_*` → `_ham`). Mevcut İngilizce adlar aile kodu yeniden yazılırken değişir.

**19-082** — KARAR — Tanımlayıcılar ASCII (ş, ğ, ı yok); Türkçe yalnız metin ve yorumda. Her `open/read_text/write_text` çağrısında `encoding="utf-8"` açık yazılır (`rapor.py:78` böyle). Bu ortamda `utf8_mode=1` ve tercih edilen kodlama utf-8 (ölçtüm); başka makinede varsayılan cp1254 olabilir.

**19-083** — KARAR — Evet saf: `adim(poz, bar, parametre) → (yeni_poz, olay)`. Rastgelelik, saat, dosya dışarıdan gelir. Saf olmayan tek yer: canlı programın durum dosyası okuma/yazması.

**19-084** — KARAR — İkinci kural: sembol alfabetik. Eşitlik zaten nadir (TL medyan float); sembol sırası likiditeyle ilgisiz; rastgele kurala da aynı kural uygulanır, yanlılık iki yanda aynıdır.

**19-085** — KARAR — Açık pozisyonlar `dict[sembol → tuple]`. Her gün yalnız açık pozisyonlar ve o günün sinyalleri üzerinde dönülür (≤ 10 + sinyal); 100 hisse döngüsü yok.

**19-086** — KARAR — Dışta gün, içte hisse. Sinyaller önce hisse başına vektörel hesaplanıp `gün → [sembol]` sözlüğüne çevrilir; portföy kısıtları gün içinde sırayla bakılır, ek maliyet küçüktür.

**19-087** — KARAR — Aile × bölme × masraf = ayrı Motor çağrısı, kendi nakit ve durumu. Ortak döngü yok (§5.6: aileler sermaye paylaşmaz).

**19-088** — KARAR — Tek JSON dosyası (UTF-8), alanlar adlı, `"sema": 1` alanı. Sürüm farklıysa durulur ve geçmişten yeniden oynatılır (19-090). Pickle yok (sürüm kırılgan), SQLite gereksiz.

**19-089** — KARAR — Gün gün tekrar oynatma: kayıtlı son işlenen günden bugüne, Takvim'deki her eksik işlem günü sırayla Adım'a verilir. Gün atlanmaz.

**19-090** — KARAR — Evet, baştan oynatılır. 6 aylık canlı dönem ≈ 130 gün × ≤ 10 pozisyon; saniyeler mertebesinde (hesap, ölçmedim). Eski görüntüyle üretilmiş kartlar kalır, fark raporlanır.

**19-091** — ZAYIF SORU — Tutarsız değil: pandas `rolling`'in varsayılan `min_periods`'ı pencere boyudur (tam pencere); `ewm` varsayılanı 0 olduğu için `aileler.py:20` açıkça verir. Yine de proje kuralı olarak "kısmi pencere yok" TASARIM §5.1'e bir satır yazılır.

**19-092** — KARAR — Medyan bugünü (t) içerir: t kapanışta bilinir, giriş t+1'de. t+1 verisi hiç girmez. Sınama: 19-050 kısaltma testi.

**19-093** — KARAR — `PD` günlük okunur; seçim yalnız ay başı gününün ham `PD`'si ve 60 günlük medyan TL tutarıyla yapılır, seri olarak çekirdeğe girmez. Bedelsiz süreksizliği: PD = fiyat × hisse sayısı olduğundan sıçramamalı (varsayım, doğrulanmadı; ilk veri işinde bakılır).

**19-094** — KARAR — Pencere = seçim yılından önceki son 252 işlem günü (yılın son işlem günü dahil, yeni yılın ilk günü hariç). Sabit 252 işlem günü, takvim yılı değil.

**19-095** — KARAR — pytest + elle hesaplanmış küçük örnekler (yedi motor sınaması + `dusuk == stop`) + 19-050 testi. hypothesis kurulu değil → yok. Altın dosya yok (teknik olmayan kullanıcı onaylayamaz).

**19-096** — KARAR — Çift uygulama yok: sinyal tek yerde, vektörel (aile). Adım yalnız pozisyonu yürütür. Canlı günlük aynı sinyal fonksiyonunu tüm seride koşup son satırı alır.

**19-097** — KARAR — Önce ölçüm: `cProfile` (stdlib); referans iş yükü 100 hisse × 11 yıl × 1 koşu ve 200 perm; kabul ölçütü 19-033 bütçesi. Hızlandırma sırası: algoritma, `joblib`, en son numba.

**19-098** — KARAR — Tek komut: `python -m tansu.kosu <aile>`; `tqdm` (4.70.1 kurulu) ilerleme ve kalan süre. Kısmi sonuç saklanmaz, devam yok: bütçe 30 dk, yarıda kalırsa baştan.

**19-099** — KARAR — Durdurur: motor girişinde `np.isfinite` ve fiyat > 0 assert; ATR = 0 → sinyal yok. pyproject'e `filterwarnings = ["error"]`. pandas 3.0.6 kurulu (doğruladım); Copy-on-Write ile SettingWithCopyWarning yok (bilgi, test etmedim).

**19-100** — KARAR — Şimdi: dict[hisse → DataFrame] + 2B dizi, pandas-ta-classic EMA/ATR (SMA tohumlu), `dogrula` assert, kilitli sürümler, sınama testleri. İlk aile kabulünden sonra, yalnız 19-033 bütçesi aşılırsa: `joblib`, sonra numba. Şema kütüphanesi, polars, TA-Lib, quantstats, arch hiç.

## Özet

Verdict sayıları (100 soru):
- CEVAPLI: 2
- KARAR: 85
- YANLIŞ: 4
- OLGU: 6
- ZAYIF SORU: 3

En önemli 10 kurulum kararı:
1. (19-044) `pyproject.toml`'a `==` kilitli bağımlılıklar ve `requires-python = "==3.14.*"` yaz; kurulum `pip install -e .`. vectorbt ve yfinance listeye girmez.
2. (19-016) EMA'yı SMA tohumlu yap (`pandas-ta-classic` `ema`); `aileler.py:19-20` EMA200'de 199. günde %3 sapıyor.
3. (19-053) Sıkışma tanımı ardışık 3 gün: `rolling(3).min() == 1`; `aileler.py:27` pencerede toplam sayıyor.
4. (19-071, 19-066) quantstats ve arch kurulu değil; en büyük düşüş, düşüşte kalma süresi ve dairesel blok bootstrap kendi birkaç satırınla yazılır.
5. (19-002, 19-004) Veri biçimi: hisse başına DataFrame (aile, gösterge); motor girişinde gün×hisse 2B float64 dizi. MultiIndex yok (`shift` hisse sınırını aşıyor, ölçüldü).
6. (19-001, 19-083, 19-096) Adım saf fonksiyon, skaler girdi, düz tuple poz; sinyal tek yerde vektörel; canlı aynı sinyal fonksiyonunun son satırı.
7. (19-050) Tek kısaltma-değişmezliği testi: `sinyal(f[:t]) == sinyal(f)[:t]`; her aile, pivot, likidite ve faiz hizalamasını kapsar.
8. (19-033, 19-097, 19-032) Süre bütçesi: 200 perm ≤ 5 dk, 1.000 perm ≤ 30 dk. Önce `cProfile`; sıra: algoritma, `joblib`, en son numba. Oyuncak adım 0,1–0,2 µs (ölçüldü), numba şimdi yok.
9. (19-041, 19-042, 19-068, 19-069) `default_rng` + `SeedSequence.spawn(N)[i]`; tohum günlüğe; p = `(1+k)/(1+N)`; Holm için `N ≥ 20·m − 1`. Koşu sayısı ≈ 15.200 (19-048).
10. (19-011, 19-015, 19-080) `duz` ve `ham` ayrı DataFrame; veri çıkışında tek `dogrula()` assert fonksiyonu (OHLC değişmezleri, sıra, tekillik); pandera yok.
