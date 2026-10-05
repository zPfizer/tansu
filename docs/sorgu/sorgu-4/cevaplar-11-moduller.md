# Cevaplar 11: Depo yapısı ve modüller

Doğrulananlar: `.venv` Python 3.14.7, pandas 3.0.6, numpy 2.5.3, pyarrow 25.0.1, duckdb 1.5.6, statsmodels 0.15.0, scipy 1.18.1, pandas-ta-classic 0.8.32, borsapy 0.11.0, vectorbt 1.1.1, yfinance 1.7.0 kurulu. `quantstats`, `arch`, `streamlit`, `jinja2` kurulu DEĞİL (import hatası). `multipletests(method="holm")` ve `coint` içe aktarılıyor. `pytest`: 13 geçti. `.git` var (`git log` çalışıyor). `docs/adr/` yok.

**11-001** — KARAR — Ayrı dosya: veri, evren, gostergeler, aileler, cift, motor, simulator, istatistik, kayit, rapor. Yalnız fonksiyon: takvim, maliyet, piyasa durumu, şirket olayları (veri.py içinde), karantina, çapraz kontrol. Alt paket yok.
**11-002** — YANLIŞ — Takvim modülü gereksiz: işlem günü = fiyat indeksinde o tarihin varlığı. "Bugün veri var mı" sorusunu §5.1 son çubuk tarihi kuralı zaten karşılıyor. Tablodan sil.
**11-003** — YANLIŞ — Sabit %0,3 bir sabittir: `MASRAF = 0.003` motor.py tepesinde; %0,1/%0,5 senaryosu `masraf=` argümanı.
**11-004** — YANLIŞ — Tek uygulamalı arayüz. "Takılıp çıkarılabilir" notunu §4'ten sil; masraf argümanı yeter.
**11-005** — KARAR — Tek modül: veri.py. Olay tablosu veriyle aynı kaynaktan (İş Yatırım) gelir ve aynı anlık görüntüye girer. Düzeltme katsayısını uygulayan `duzelt(ham, olaylar)` fonksiyonu veri.py'dedir.
**11-006** — KARAR — Tek `evren(tarih)` fonksiyonu. Şimdi PD ile en büyük 100; KAP hazır olunca gövde değişir, PD kodu silinir. İkisi birlikte yaşamaz, arayüz sınıfı yok.
**11-007** — YANLIŞ — Ayrı modül gereksiz, 10 satırlık fonksiyon. Ama K1(b) (§5.7) etiketi istatistik tarafında kullanıyor, rapor tarafında değil: fonksiyon gostergeler.py'de dursun.
**11-008** — YANLIŞ — Sığmıyor: çift hem iki fiyat hem durum taşır. "Aile" arayüzü yalnız tek hisse ailelerinindir (`sinyal(fiyat, p) -> bool Series`). Çift için ayrı cift.py (seçim + rotasyon), kendi döngüsü.
**11-009** — KARAR — Adım yalnız tek hisse bölmesi içindir (stop/hedef/bozulma). Çift rotasyonu cift.py'de ayrı küçük döngü: durum = "hangi hissede", mum yerine iki hissenin aynı günkü satırı. Adım'a çift mantığı sokulmaz.
**11-010** — KARAR — "Mum" = o güne ait bir satır (namedtuple): fiyatlar + önceden hesaplanmış `atr`, `sma250` sütunları. Göstergeler gostergeler.py'de vektörel hesaplanıp satıra konur. Adım yine saf: aynı girdi, aynı çıktı.
**11-011** — KARAR — Adım yalnız açık pozisyonu günceller (stop, hedef, bozulma). Giriş kararı ailenin sinyalidir; motor "sinyal varsa ertesi gün AOF'tan pozisyon aç" der. Böylece §6 madde 5 (açık kartı güncelle) doğrudan Adım olur.
**11-012** — CEVAPLI — §5.1/§6.1: son çubuğun tarihi bugün değilse kart üretilmez. Adım'a her zaman kapanmış gün satırı girer; arayüz değişmez. Açık nokta: İş Yatırım'ın yayın saati bilinmiyor (§8.7).
**11-013** — KARAR — Düz sayılar (namedtuple satır). Pandas'ta satır erişimi Python döngüsünde yavaş ve test için DataFrame kurmak gerekir; düz sayıyla Adım testi tek satırlık olur.
**11-014** — KARAR — Her gün döngüsü gerekmez. Her aday sinyal günü için bir kez işlem hesaplanır (Adım yalnız giriş–çıkış arası koşar), sonuç önbelleğe alınır; 1.000 tekrar bu önbellekten örnekler. Hız ölçülmedi. Yetmezse numba (kurulu) yalnız Adım'a.
**11-015** — KARAR — Aynı motor. K1 örneklemesi (hangi gün seçilir) istatistik.py'de; motor yalnız `islem(hisse, sinyal_gunu)` verir. Ayrı koşucu yok.
**11-016** — KARAR — Boyut, %10 tavan, 10 pozisyon, sıra (M12) ve likidite (M11) simülatörün. Motor sinyal başına işlem üretir (R cinsinden), portföy bilmez.
**11-017** — KARAR — DataFrame. Sütunlar (`hisse, aile, giris, cikis, giris_fiyat, cikis_fiyat, getiri, r, neden`) motor.py başındaki docstring'de ve bir testte tanımlı.
**11-018** — KARAR — Tek simulator.py, iki fonksiyon (`tek_hisse_bolmesi`, `cift_bolmesi`). Ortak: sermaye eğrisi, nakit faizi. Boyutlama kolları bağımsız; zorla birleştirme yok.
**11-019** — KARAR — arch kurulu değil (doğrulandı); scipy.stats.bootstrap blok bootstrap vermez. 20 günlük blok yeniden örnekleme ~10 satır numpy, bizim kod. Holm: `statsmodels.stats.multitest.multipletests` (doğrulandı). Modül, K1 örneklemesi ve blok kodu için var olur; sarmalayıcı değil.
**11-020** — KARAR — kayit.py (Holm hesabı istatistik.py'de çağrılır, günlük kayit.py'de tutulur).
**11-021** — KARAR — kayit.py.
**11-022** — KARAR — Tek modül (kayit.py), iki CSV: `kayit/kural_kaydi.csv`, `kayit/deneme_gunlugu.csv`. Ayrı depolama motoru yok.
**11-023** — YANLIŞ — Kalıcı kod olmamalı. Tek seferlik iş: `python -c` ile yap, sonucu `docs/sadakat.md`'ye yaz. Aile kodu zaten aileler.py'de.
**11-024** — KARAR — veri.py içinde `karantina(fiyat, olaylar)` fonksiyonu.
**11-025** — KARAR — veri.py içinde `capraz_kontrol`; yalnız sınama anlık görüntüsü oluşturulurken çalışır. Günlük koşuda yalnız son çubuk tazelik kontrolü.
**11-026** — KARAR — rapor.py: markdown rapor ve `kartlar.csv`. "Kart" bir satırdır, modül değil.
**11-027** — KARAR — `kayit/kartlar.csv` (durum sütunlu). Sahibi kayit.py okur/yazar; rapor.py yalnız okur.
**11-028** — YANLIŞ — §3 Streamlit ekranını ilk sürüme koyuyor, ama §3 kendi "gereksiz katman" listesiyle çelişiyor ve streamlit kurulu değil. İlk sürümde ekran yok. Sonra eklenirse yalnız `rapor/*.md` ve CSV okur, hiçbir tansu modülünü içe aktarmaz.
**11-029** — YANLIŞ — Gerekmez. Markdown rapor aynı bilgiyi verir. "Kanıt ekranı"nı §3'ten ve `streamlit`'i bağımlılıklardan çıkar.
**11-030** — KARAR — Düz `tansu/*.py`, ~12 dosya. Alt paket derinlik katar, kazanç yok.
**11-031** — KARAR — Kalır (içerik yeniden): veri.py, aileler.py, rapor.py. Silinir: kanit.py (yerine motor.py), nabiz.py.
**11-032** — KARAR — Silinen: yfinance çağrısı, `temizle()` eşik düzeltmesi (B1 yasak), vectorbt, 4 ATR hedef, EMA50 çıkışı, 2023 ayrımı, 5 tekrar. Kurtarılan: aileler.py'deki iki sinyal fonksiyonu (sütun adları değişir), parquet önbellek fikri, nabiz'daki SMA50/SMA200 satırları, rapor tablo biçimi. "Dördü de tamamen eski" doğru değil.
**11-033** — KARAR — `ema`, `sma`, `atr` ve piyasa durumu: gostergeler.py. aileler ve motor ondan içe aktarır.
**11-034** — KARAR — EMA/SMA: pandas ewm/rolling, gostergeler.py'de tek tanım. ATR: `pandas_ta_classic.atr` (prototipte çalışıyor). ATR'nin ortalaması EMA değil (varsayılan RMA, bu oturumda doğrulanmadı), çift EMA oluşmaz.
**11-035** — KARAR — Evet, sütun olarak. Sınamada vektörel, canlıda da aynı vektörel hesap (son satır alınır); tek gün hesabı yok. Garanti: kesme testi (11-037).
**11-036** — KARAR — Evet son satır. Kanıt: kesme testi.
**11-037** — KARAR — Tasarımda yok. `tests/test_gelecek.py`: fiyatı t gününde kes, sinyal ve göstergeyi hesapla, tam seriyle t günü değerini karşılaştır; her aile ve gösterge için bir parametreli test.
**11-038** — KARAR — Motor aileyi bilmez: aile, `sinyal` Series'i olarak motora verilir. Yön: aile → motor.
**11-039** — KARAR — Tek yönlü sıra yazılsın (TASARIM §4'e bir paragraf): veri, gostergeler → aileler, cift → motor → simulator → istatistik → kayit → rapor → `__main__`. Geri import yok. Maliyet ve motor döngüsü sorunu sabitle çözüldü.
**11-040** — KARAR — Evet, klasörsüz: ağ yalnız veri.py; disk yazma yalnız kayit.py ve rapor.py. Geri kalan her şey DataFrame alır, DataFrame verir.
**11-041** — KARAR — Evet, ağa yalnız veri.py çıkar. Kaynaklar özel fonksiyonlar (`_is_yatirim`, `_borsapy`, `_kap`); sınıf yok. veri.py ~300 satırı geçerse kaynaklar kaynak.py'ye ayrılır.
**11-042** — YANLIŞ — Ortak kaynak arayüzü zorlama; dört kaynak dört farklı şey döndürür. Fonksiyonlar fiyat tablosu ya da olay tablosu döndürür, sözleşme tablonun sütunlarıdır.
**11-043** — KARAR — Yalnız `_is_yatirim` etkilenir. Sınır: yanıtta beklenen sütunlar yoksa hata ver, kart üretme; bir kayıtlı örnek yanıtla test.
**11-044** — KARAR — Risk gerçek ama sınırlı: borsapy dönen tablolar (sektör, faiz, kapanmış sembol) anlık görüntüye yazılır; koşu canlı borsapy'a bağlı kalmaz. Evren ve fiyat borsapy'a dayanmaz.
**11-045** — KARAR — Kural: ağ kütüphanesi (requests, borsapy, yfinance) yalnız veri.py. statsmodels yalnız istatistik.py ve cift.py. pandas-ta-classic yalnız gostergeler.py. pyarrow dolaylı (parquet).
**11-046** — KARAR — Kütüphane çağrısı: Holm, eşbütünleşme (`coint`), ATR, parquet. Bizim kod: motor, simülatör, K1, blok bootstrap, kayit, rapor. quantstats kurulu değil; ölçütler (düşüş, düşüşte kalma süresi) pandas'ta birkaç satır.
**11-047** — YANLIŞ — pyproject.toml'a `[project] dependencies` yaz: pandas, numpy, pyarrow, statsmodels, scipy, pandas-ta-classic, borsapy, requests; pytest ayrı. vectorbt ve yfinance listeye girmez (sadakat için yfinance bir kez `-c`); işi bitince `pip uninstall` sahibin kararı.
**11-048** — KARAR — `pip install -e` gerekmez; `pythonpath = ["."]` ve `python -m tansu` yeter. Yine de pyproject'e ad, `requires-python` ve bağımlılıklar yazılır.
**11-049** — OLGU — Doğrulandı: Python 3.14.7; pandas, numpy, statsmodels, scipy, pandas-ta-classic import ediliyor ve testler geçiyor. quantstats kurulu değil, uyumu bilinmiyor (kullanılmayacak). Sürüm kuralı: pyproject'te `requires-python = "==3.14.*"`.
**11-050** — KARAR — Kilit aracı yok. pyproject'te kurulu sürümler `==` ile sabitlenir. Tek kişilik Windows kurulumuna yeter.
**11-051** — KARAR — Alan terimleri Türkçe ASCII (`aile`, `adim`, `evren`, `bolme`, `kart`), kütüphane çağrıları İngilizce kalır. Prototip böyle. Aynı satırda karışması (`ta.atr(f.yuksek...)`) okunabilirliği bozmaz.
**11-052** — KARAR — Yazılı değil. Kural: kod adı, dosya adı, sütun adı ve CSV başlığı yalnız ASCII; metin içeriği (rapor, kart) Türkçe karakterli olur. TASARIM §4'e bir satır.
**11-053** — KARAR — Kural: GLOSSARY terimi küçük harf ASCII, boşluk `_` (Fazla getiri → `fazla_getiri`). Kontrol aracı yok; tek kişilik depoda sapma maliyeti küçük.
**11-054** — KARAR — Kodda `adim` (fonksiyon). Gün sayacı `gun`. Karışmaz.
**11-055** — KARAR — Portföy bölmesi `bolme`; şirket olayındaki bölünme `bolunme`.
**11-056** — KARAR — Sütun adları Türkçe ASCII. CSV kart sütunları sözleşme: `hisse, aile, giris, stop, hedef, adet, durum, kanit`; sabit liste rapor.py'de.
**11-057** — KARAR — `tipler.py` yok. Fiyat sütunları veri.py docstring'inde, işlem sütunları motor.py'de, Pozisyon motor.py'de namedtuple.
**11-058** — KARAR — Türkçe ASCII: `kapanis, yuksek, dusuk, aof, hacim, piyasa_degeri`. İş Yatırım `HGDG_*` → bu adlar, `HG_*` → `ham_*`. Dönüşüm veri.py'de, tek yer. Prototip testleri `Close` kullanıyor, yeniden yazılır.
**11-059** — KARAR — Tür düzeyinde değil, ad düzeyinde: aile ve gösterge yalnız düzeltilmiş `kapanis…` okur; ham sütunlar `ham_kapanis`, `ham_hacim`. Test: bedelsiz gününde sinyal oluşmuyor.
**11-060** — KARAR — Parquet, `veri/<YYYYMMDD>/<sembol>.parquet`. DuckDB kurulu ama gereksiz.
**11-061** — KARAR — Yeni anlık görüntü yalnız sınama koşusunda. Deneme günlüğünde adı geçenler hiç silinmez, diğerleri 30 gün sonra silinir. Boyut ölçülmedi.
**11-062** — KARAR — Ekleme yapılan CSV. Excel'de çift tıklayınca açılır.
**11-063** — KARAR — `tansu/*.py` içeriğinin tek sha256'sı. Ortak kod değişince bütün kayıtlar geçersiz olur; §5.8 "sonraki her değişiklik yeni deneme" kuralı zaten bunu ister.
**11-064** — ZAYIF SORU — Premis yanlış: `.git` var (`git log` doğrulandı); yalnız uzak repo yok. Yine de hash dosya içeriğinden alınır: kirli ağaçta commit kimliği yanıltır.
**11-065** — KARAR — `veri/` .gitignore'da (var); `kayit/` ve `rapor/` git'e girer. Yeniden indirme geçmişi değiştirebildiği için `veri/` klasörü elle yedeklenir.
**11-066** — KARAR — Python sabitleri, kullanan modülün tepesinde (`MASRAF`, `SERMAYE`). TOML/YAML yok. Parametre kaydı = aile dosyasındaki dataclass varsayılanları.
**11-067** — KARAR — Aile kodunda (`aileler.py`). Hash zaten bakar.
**11-068** — KARAR — Evet: `sinyal(fiyat, p)`; `p` donmuş dataclass, varsayılanlı. Izgara `dataclasses.replace` ile.
**11-069** — KARAR — Fonksiyon + parametre dataclass'ı. Sinyal durumsuzdur. Çift ailesi bu arayüzde değil (cift.py).
**11-070** — CEVAPLI — `AILELER` sözlüğü mevcut (aileler.py), 5 satır, rapor döngüsünü besliyor. Kalsın.
**11-071** — KARAR — Maliyet ~20 satır fonksiyon + parametre dataclass + sözlük kaydı + 1 test; arayüzle öngörülebilir. Çift ailesi hariç.
**11-072** — KARAR — aileler.py: sikisma, AB=CD (iki tek hisse ailesi). cift.py ayrı (eşbütünleşme, z-skor, rotasyon).
**11-073** — KARAR — cift.py: yıllık seçim, çakışma çözümü ve rotasyon. Evren yalnız hisse listesi verir.
**11-074** — KARAR — Kendi zigzag (yüzde sapmalı, onaylı pivot). `scipy.signal.find_peaks` (kurulu) gelecekteki komşulara bakar, sızıntı yapar. Pivot ayarı aileler.py parametre dataclass'ında.
**11-075** — KARAR — Yahoo kodu kalıcı dosyada olmaz: `python -c` ile bir kez, sonuç docs/sadakat.md'ye. Ana veri deposuna dokunmaz.
**11-076** — KARAR — Kalıcı Yahoo kodu hiç yazılmadığı için silinecek bir şey yok; yeniden deneme yeni `-c` komutuyla.
**11-077** — KARAR — Kullanılabilir: SMA200 ve SMA50 satırları. Şok ve üç duruma ayırma atılır. Etiket kümesi iki: `YUKARI` (kapanış > SMA200) ve `ASAGI`. Az etiket, K1(b) eşleşmesini kolaylaştırır.
**11-078** — YANLIŞ — Çelişki: etiket K1(b) örneklemesine girdi. §3/§4'teki "yalnız raporlama" ifadesi "motoru ve girişi etkilemez; K1(b) örneklemesinde ve rapor bölmesinde kullanılır" olarak düzeltilir.
**11-079** — KARAR — `evren()` her ay başı için bir kez hesaplanıp (ay → sembol listesi) tablosu olarak anlık görüntüye yazılır. Motor tarihle tabloya bakar.
**11-080** — KARAR — Kapanmış hisse diğerleri gibi veri deposuna girer. Verisi biten hissede açık pozisyon son işlem günü AOF'tan `neden="kapandi"` ile zorla kapanır; kural motor.py'de.
**11-081** — KARAR — Kod: 5.1, 5.3–5.7, 5.9–5.11 ve 5.12 hesabı. Belge/süreç: 5.2 (yanlılık), 5.8 (dönemler). 5.12 maddeleri 1–5 `kabul()` fonksiyonu (rapor.py), madde 6 canlı dönem sonunda elle.
**11-082** — KARAR — Kod "ölçüt geçti/geçmedi" hesaplar. "Canlı" etiketini Levent yazar: `kural_kaydi.csv`'de `durum` sütunu.
**11-083** — KARAR — f-string. Jinja kurulu değil, gerekmez.
**11-084** — YANLIŞ — quantstats kurulu değil (doğrulandı). §4 satır 91 ve 96'daki "quantstats"i sil. Ölçütler pandas'ta, çıktı yalnız markdown.
**11-085** — KARAR — Tek giriş `python -m tansu`; komutlar `gunluk` ve `sina <aile>`. `tansu/__main__.py` `sys.argv` okur.
**11-086** — KARAR — Görev Zamanlayıcı: `.venv\Scripts\python.exe -m tansu gunluk`. Hata: çıkış kodu ≠ 0 ve `rapor/son-durum.md` ilk satırı "HATA: ...". Sahip sabah o dosyaya bakar.
**11-087** — KARAR — Ortak: veri okuma, gösterge, aile, Adım (hepsi aynı kod). Fark yalnız: sınama bütün geçmişi, günlük yalnız son günü koşar ve kart yazar.
**11-088** — KARAR — `kayit/kartlar.csv`. kayit.py yazar ve okur; `__main__.py` çağırır.
**11-089** — KARAR — Modüller hata fırlatır, yakalamaz. Yalnız `__main__.py gunluk` yakalar, kart üretmez, hatayı yazar.
**11-090** — KARAR — Log yok. `rapor/son-durum.md` ve `print` yeter.
**11-091** — KARAR — test_aileler: kalır, sütun adları değişir. test_kanit: silinir (vectorbt), yerine test_motor. test_nabiz_veri: nabız testleri ve `temizle` testleri silinir, yerine test_veri (olay düzeltme).
**11-092** — KARAR — Yedi senaryo `adim` düzeyinde (saf, hızlı). Motor testi ekler: AOF'ta giriş, açık pozisyonda yeni sinyal yok, veri sonu kapanışı.
**11-093** — KARAR — Kaydedilmiş örnek yanıtlarla (fixture); canlı test yok. Uç noktayı elle `python -c` ile kontrol et.
**11-094** — KARAR — mypy ve ruff yok. pytest yeter.
**11-095** — KARAR — `docs/adr/` açılmaz; TASARIM.md yeterli. AGENTS.md'deki "kararlar docs/adr/" satırı "kararlar TASARIM.md'de" olarak düzeltilir.
**11-096** — KARAR — Belge önce: ayrışırsa kod düzeltilir ya da belge tarihli güncellenir. Kontrol: 11-100'deki test ve her oturumun AGENTS.md'yi okuması.
**11-097** — KARAR — Şart: veri (şirket olayları dahil), gostergeler, bir aile, motor, rapor. Bekleyebilir: evren (sabit liste), simulator, istatistik, kayit, cift, piyasa durumu. Takvim ve maliyet modül değil.
**11-098** — KARAR — Dilim: veri/ altındaki 10 hisse, sikisma ailesi, düzeltilmiş fiyat, Adım + Motor, tek tablo rapor. Eksikler sonradan eklenince motor işlem tablosunu aynı sütunlarla verdiği için arayüz değişmez.
**11-099** — KARAR — Her modülde `__all__`; 6'dan fazla ad çıkıyorsa tasarım gözden geçirilir. Zorlama testi yok; niyet beyanı ama yazılı.
**11-100** — KARAR — AGENTS.md: modül haritası (dosya → tek satır görev) ve üç komut. Senkron: `tests/test_harita.py` her `tansu/*.py` adının AGENTS.md'de geçtiğini kontrol eder (4 satır).

## Özet

Sayımlar (100 soru): CEVAPLI 2 (11-012, 11-070), KARAR 84, YANLIŞ 12 (11-002, 003, 004, 007, 008, 023, 028, 029, 042, 047, 078, 084), OLGU 1 (11-049), ZAYIF SORU 1 (11-064). Sayımlar dosyadaki etiketlerden grep ile doğrulandı.

En önemli 10 karar:

1. Düz paket, 12 modül yerine 10 dosya: takvim, maliyet, piyasa durumu, şirket olayları ayrı modül değil (11-001, 002, 003, 004, 005).
2. Aile arayüzü yalnız tek hisse ailesi içindir; çift rotasyonu cift.py'de kendi döngüsüyle (11-008, 009).
3. Adım saf: düz sayı satırı + önceden hesaplanmış `atr`/`sma250`; yalnız çıkışı yönetir, giriş sinyalden gelir (11-010, 011, 013).
4. Motor her günü değil her aday sinyali bir kez koşar, sonuç önbellekte; K1 aynı motoru ve önbelleği kullanır (11-014, 015).
5. Kural kaydı + deneme günlüğü + kart durumu = kayit.py, CSV dosyaları; hash = `tansu/*.py` birleşik sha256 (11-020, 021, 022, 027, 062, 063).
6. Gelecek sızıntısı için kesme testi eklenir; tasarımda yoktu (11-036, 037).
7. quantstats ve streamlit kurulu değil: ikisi de ilk sürümden çıkar; blok bootstrap 10 satır numpy, Holm `multipletests` (11-019, 028, 029, 084).
8. Ağ yalnız veri.py; sadakat kontrolü kalıcı kod değil, `python -c` + `docs/sadakat.md` (11-023, 041, 042, 075).
9. pyproject.toml: `[project]` bağımlılıkları `==` ile sabit, vectorbt/yfinance listede yok, `requires-python == 3.14.*`; kilit aracı yok (11-047, 048, 049, 050).
10. Kod adı ASCII Türkçe; fiyat sütunları `kapanis, yuksek, dusuk, aof, hacim` (düzeltilmiş) ve `ham_*`; dönüşüm veri.py'de. `__main__.py` tek giriş, AGENTS.md modül haritası ve onu denetleyen test (11-051, 052, 058, 059, 085, 100).

Önerilen son modül listesi (`tansu/`):
- `veri.py` (indirme, anlık görüntü, şirket olayları, düzeltme, karantina, çapraz kontrol, tek ağ noktası)
- `evren.py`
- `gostergeler.py` (ema, sma, atr, piyasa durumu)
- `aileler.py` (sikisma, AB=CD, `AILELER`)
- `cift.py` (seçim + rotasyon)
- `motor.py` (Adım, işlem, `MASRAF`, işlem tablosu sözleşmesi)
- `simulator.py` (iki bölme, faiz)
- `istatistik.py` (K1, blok bootstrap, Holm)
- `kayit.py` (kural kaydı, deneme günlüğü, kartlar.csv)
- `rapor.py` (markdown, CSV, `kabul()`)
- `__main__.py` (`gunluk`, `sina`)

Silinecek: `kanit.py`, `nabiz.py`, Yahoo/vectorbt kodu.
