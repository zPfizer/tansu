# Cevaplar 13: Veri depolama

Ortak karar (çoğu cevap buna atıf yapar): **anlık görüntü (AG) = bir indirmenin tam kopyası = tek klasör** `veri/ag/<ID>/`. İçinde `fiyat.parquet` (uzun biçim, tüm semboller), `olaylar.parquet`, `faiz.parquet`, `borsapy.parquet`, `ham/` (ham JSON yanıtlar), `manifest.json`. Kimlik `<YYYYMMDD>-<8 hex>` (tarih + dosya içeriklerinin sha256'sından ilk 8). Biçim parquet, okuma pandas+pyarrow. Ölçülen: mevcut `veri/` 12 MB, 101 dosya, hepsini okumak 0,13 sn, bellekte 12 MB.

**13-001** — KARAR — Tam kopya: bütün evren, bütün tarihler, her indirmede. Yalnız-eklenen-satır modeli geçmiş düzeltmesini göstermez; bu yüzden reddedilir.

**13-002** — KARAR — Gün başına bir klasör (`veri/ag/<ID>/`), içinde tür başına tek dosya. Koşu kimliği = klasör adı; `manifest.json` her dosyanın sha256'sını taşır.

**13-003** — CEVAPLI — `tansu/veri.py` Yahoo kodudur (`fiyat()` üstüne yazar, `mtime` önbelleği) ve §7 madde 1 "Yahoo'lu ön deneme kodu kaldırılır" diyor. Eski `veri/*.parquet` dosyaları `veri/yahoo/` altına taşınır (yalnız sadakat adımı için), yeni okuyucu oraya bakmaz.

**13-004** — YANLIŞ — Dört seçenek tartışmaya gerek yok. Ölçüt: kurulu ve yeterli mi. pandas 3.0.6 + pyarrow 25.0.1 kurulu, `veri/` zaten parquet. Karar: parquet. CSV/SQLite/DuckDB elenir (DuckDB §3'te zaten kapsam dışı).

**13-005** — OLGU — Evet yeterli. Doğrulandı: 101 dosyanın tamamı 0,13 sn'de okundu, 12 MB bellek, 248.960 satır. Sorgu = `df[(df.sembol==s)&(df.tarih==t)]`. Ölçüt: 1.000 tekrarlı koşu belleğe bir kez yüklenir; yavaşlarsa yeniden düşünülür.

**13-006** — KARAR — Üç şey: klasör yazıldıktan sonra dosyalara salt okunur bayrağı (`os.chmod`), `manifest.json` içinde sha256, ve her koşu başında okuduğu AG'nin hash'ini doğrulaması. Değişen hash koşuyu durdurur; fark eden koşunun kendisidir.

**13-007** — KARAR — Kimlik tarih + içerik hash'i. Aynı gün aynı içerik = aynı kimlik (yeni yazma yok). Aynı gün farklı içerik = farklı hash eki, çakışma olmaz.

**13-008** — KARAR — Evet, her indirmede önceki AG ile örtüşen tarihler karşılaştırılır, `manifest.json`'a yazılır. Eşik: ham kapanışta herhangi bir fark = uyarı; fark > %0,5 (§5.1 ile aynı sayı) ya da son 5 işlem gününden eski bir satırda değişiklik = hata, kart üretilmez.

**13-009** — KARAR — Aynı `fiyat.parquet` içinde: `kapanis, yuksek, dusuk, aof, hacim, pd` (HG_*) ve tek ek sütun `kapanis_duz` (HGDG kapanış). Yalnız karşılaştırma için gerekli olan tek sütun saklamaya değer; maliyeti ihmal edilir.

**13-010** — KARAR — Girer: `borsapy.parquet` (sembol, tarih, kapanış) aynı klasöre. Girmezse §5.1 karşılaştırması yeniden üretilemez.

**13-011** — KARAR — Tek "veri sürümü" = AG kimliği. Fiyat, olaylar, faiz, borsapy hepsi aynı klasörde. KAP elle listesi AG'ye girmez (13-077). Yahoo ayrı klasör (13-012).

**13-012** — KARAR — Yahoo verisi `veri/yahoo/` altında, AG kimliği yok, ana okuyucu bu yola hiç bakmaz. Karışmayı yol ayrımı engeller; ayrı şema gerekmez.

**13-013** — KARAR — Şema `fiyat.parquet` için sabit, Türkçe adlarla (`sembol, tarih, kapanis, yuksek, dusuk, aof, hacim, pd, kapanis_duz`). Kaynak sütun değiştirirse indirici hata verir; eski AG'ler değişmez, çünkü AG içinde şema `manifest.json`'da `sema_surumu: 1` olarak yazılır.

**13-014** — KARAR — Birim kararı okuma katmanında. AG ham değeri taşır, `manifest.json`'a "hacim_birimi" yazılmaz (bilinmiyor). Birim hatası bulunursa AG yeniden yazılmaz, okuma katmanı düzeltilir.

**13-015** — KARAR — Saf tarih (`datetime64`, saat dilimi yok, gece yarısı). Mevcut `veri/` dosyaları da saat dilimsiz `datetime64[ms]` (doğrulandı). Kaynak tarihi dizge olarak gelir, doğrudan ayrıştırılır; yerel saat tarihe hiç girmez.

**13-016** — KARAR — float64. Ondalık gereksiz: fiyat adımı 0,01 ve getiriler zaten float; hash dosya baytlarından (yazılmış haliyle) alınır, yeniden hesaplanmaz, yani çarpma birikimi hash'i etkilemez.

**13-017** — KARAR — Aynı AG klasöründe ayrı dosya `olaylar.parquet`. Ayrı depo yok.

**13-018** — KARAR — Ham yanıt arşivlenir: `ham/sermaye.json`. Ayrıştırıcı hatası bulunursa ham yanıttan yeniden ayrıştırılır; sunucuya dönmek gerekmez. Boyut küçük.

**13-019** — KARAR — Değişmez ve tarihli: AG'nin parçası. Kaynak oranı düzeltirse yeni AG içinde yeni değer görünür, fark 13-008 raporuna girer.

**13-020** — CEVAPLI — Aynı AG klasörü iki tabloyu birlikte taşıdığı için (13-017) tutarsız çift oluşamaz. Çözüm yapısaldır.

**13-021** — KARAR — Şemaya her iki sütun da kaynağın verdiği adla yazılır; yorum (hak kullanım mı ödeme mi) okuma katmanında tek yerde. Cevap yanlışsa tablo yeniden indirilmez, okuma katmanı düzeltilir. Açık soru §8.2 olarak kalır.

**13-022** — KARAR — Katsayı ve düzeltilmiş fiyat saklanmaz, her koşuda yeniden hesaplanır (100 sembol × 2.800 gün küçük). Önbellek yok, geçersizleme sorunu yok.

**13-023** — KARAR — Karantina ayrı çıktıdır (koşunun rapor klasörü), AG parçası değil. Her karantina satırı/başlığı `ag_id` taşır.

**13-024** — KARAR — Kapanmış semboller satırlarıyla tutulur (§5.2 gerektirir). Anahtar sembol kodu. Şirket kimliği tablosu kurulmaz; kod yeniden kullanımı bilinen küçük yanlılık olarak rapora yazılır (varsa).

**13-025** — KARAR — Evren depoda saklanmaz; her koşuda AG'den belirleyici olarak hesaplanır. `pd` AG ile donduğundan aynı AG aynı evreni üretir.

**13-026** — KARAR — Tam yeniden indirme, artımlı değil. Artımlı eski satır değişikliğini yakalayamaz, tam indirme yakalar (13-008).

**13-027** — OLGU — Doğrulanmadı. İş Yatırım için hız sınırı belgesi bulunamadı (`docs/arastirma/veri-kaynaklari.md` Bölüm 1.3, 8.1). Tahmin: sembol başına 1 istek, 100 istek, istekler arası 1 sn bekleme ile yaklaşık 2-3 dk. Karar: tam indirme, 1 sn bekleme; engel gelirse artımlıya geçilir.

**13-028** — YANLIŞ — Gereksiz: tam indirme seçildi (13-026), örtüşme penceresi yok.

**13-029** — KARAR — Yarım indirme atılır. İndirme `veri/ag/_gecici/` içinde yapılır, hepsi tamam ve doğrulama geçerse klasör `os.replace` ile adlandırılır. Başarısızsa `SON.txt` değişmez, kart üretilmez.

**13-030** — KARAR — Satır silinmez. Ham yazılır, bozuk satır (hacim 0, boş kapanış) `kalite.parquet`'e değil, okuma katmanında bayrak olarak işaretlenir. `temizle()` Yahoo koduyla gider.

**13-031** — CEVAPLI — Değişmez olan AG'dir, kaynak değil. Ertesi gün düzelen çubuk yeni AG'de görünür; eski AG bozulmaz. Manifest `son_cubuk_tarihi` yazar, canlı kart kontrolü (§5.1 m6) bunu kullanır.

**13-032** — KARAR — Ayrı doğrulama işlevi aynı modülde, AG'yi yazmadan önce çalışır. Başarısızsa AG yazılmaz (13-029 ile aynı yol).

**13-033** — OLGU — Doğrulandı (ölçüm): 12 MB (Yahoo, 5 sütun, 101 dosya). 7 sütun için ham: 100 × 2.800 × 7 × 8 B ≈ 16 MB, sıkıştırılmış tahmin 12-15 MB. Her işlem günü tam kopya: yılda ≈ 3 GB (250 gün), 5 yılda ≈ 15 GB. Kabul edilebilir; ayrıca bkz. 13-034.

**13-034** — KARAR — Silme yok; ilk 20 GB'a kadar bekle. Deneme günlüğünün atıf yaptığı AG'ler zaten silinmez (kayıtta kimlik var). Bağımlılık izleme gerekmez: kural "hiç silme" olduğu için.

**13-035** — KARAR — Manuel. Tek kural, sahibe: "20 GB'ı geçince `veri/ag/` içinden en eski ve günlükte adı geçmeyen klasörleri sil". Sade liste için `tansu` komutu yok, ilk sürümde yazılmaz.

**13-036** — YANLIŞ — Delta aşırı mühendislik; 12 MB'lık kopya, 13-033'te ölçüldü. Her AG tam, delta yok.

**13-037** — KARAR — Varsayılan (snappy; mevcut dosyalarda SNAPPY doğrulandı). Hash dosya baytından alınıp manifestte saklanır, yeniden üretilmesi beklenmez; bu yüzden pyarrow bayt farkı sorun olmaz.

**13-038** — KARAR — Git'e: kod, belge, `kayit/` (küçük tablolar ve günlük, 13-040). Git'e girmez: `veri/`. `rapor/islemler-*.parquet` mevcut olarak izleniyor; bu bir çıktıdır, `.gitignore`'a `rapor/*.parquet` eklenir ve `git rm --cached` yapılır. `.gitignore` zaten `veri/` yazıyor, tek eksik kural bu.

**13-039** — KARAR — Risk kabul edilmez: yedek şart (13-042). Yedek olmadan günlükteki hash yeniden üretilemez.

**13-040** — KARAR — Evet, `kayit/` klasörü git'te: `deneme.jsonl`, `kural-kaydi.json`, `el-listeleri/*.csv`. Küçük, metin, diff okunur. Şirket olayları AG'de kalır (13-017), git'e girmez.

**13-041** — YANLIŞ — Git LFS/DVC gereksiz: veri git dışı, sürümü AG klasör adı ve manifest taşıyor. Hiçbiri.

**13-042** — KARAR — Yerel disk yetmez. `robocopy veri\ag D:\yedek\tansu\ag /E` ve `.git` + `kayit/` için aynı komut; ikinci yer harici disk ya da `C:\Users\levent\OneDrive\TANSU-yedek`. Doğrulandı: OneDrive klasörü var, ama `OneDrive\Desktop` yok, yani proje OneDrive'a senkronize olmuyor.

**13-043** — KARAR — Haftada bir, planlı görev, `robocopy`. Sahip kontrolü: koşu raporunun ilk satırı "son yedek: <tarih>" yazar; 8 günden eskiyse "YEDEK ESKİ" uyarısı.

**13-044** — OLGU — Doğrulandı: `C:\Users\levent\OneDrive` var ama içinde `Desktop`/`Masaüstü` yok; proje yolu `C:\Users\levent\Desktop\TANSU` gerçek yerel klasör. Risk şu an yok. Yedek OneDrive'a (13-042) yalnız tamamlanmış kopya olarak gider, yazma sırasında değil.

**13-045** — KARAR — Atomik yazma `os.replace` ile; `PermissionError` olursa 3 kez, 1 sn arayla yeniden dene, sonra hata ver. Güvenilir sayılır (NTFS aynı sürücü). Doğrulanmadı, yalnız Windows belgesi bilgisi.

**13-046** — OLGU — Dosya adları kısa: `veri/ag/20261005-a1b2c3d4/fiyat.parquet` ≈ 80 karakter, 260 sınırının çok altında. Proje yolunda Türkçe karakter yok (`Desktop`, ASCII). Dosya adlarında hiç Türkçe karakter kullanılmaz.

**13-047** — KARAR — `manifest.json`: `ag_id, indirme_zamani, sembol_sayisi, satir_sayisi, son_cubuk_tarihi, sema_surumu, dosyalar{ad: sha256}, pandas, pyarrow`. Deneme günlüğü yalnız `ag_id` + manifest sha256'sı taşır.

**13-048** — KARAR — `kayit/deneme.jsonl`, tek satır = bir JSON. Tek yazıcı: günlük koşu yazmaz, yalnız sınama koşusu yazar; `open(...,"a")` ile tek `write` çağrısı. Eşzamanlı sınama koşusu 13-066'daki kilitle engellenir.

**13-049** — KARAR — Yalnız ekleme. Düzeltme yeni satır olarak eklenir, alanında `duzeltir: <önceki satır no>`.

**13-050** — KARAR — Günlük satırı: `kod_hash` (git commit + temiz mi), `ag_id`, `aile, cikis, parametre`. Holm sayımı (aile, çıkış, parametre, kod_hash) birleşimine göredir. Yalnız veri değişirse yeni deneme sayılmaz.

**13-051** — KARAR — Tekrar üretme testi satır ekler ama sayımda aynı anahtar (13-050) bir kez sayılır, Holm şişmez.

**13-052** — KARAR — Evet: kural kaydı `ag_id` ve manifest hash'ini içerir. Kaynak sonradan geçmişi değiştirirse ayrılmış dönem tanımı kayıt tarihidir (AG'den bağımsız), bozulmaz.

**13-053** — KARAR — Canlı dönemde o gün alınan AG saklanır (silinmez, 13-034). Fark durumunda canlı değerlendirme o gün görülen AG'ye göre yapılır; sonraki AG farkı raporlanır.

**13-054** — KARAR — Evet: kart CSV'nin ilk satırı/ayrı sütunu `ag_id`. Yeniden üretim için gereken: `ag_id` ve `kod_hash`.

**13-055** — KARAR — Ayrı kavramlar. Yeni tasarımda önbellek yok, yalnız değişmez AG var. "Aynı gün ikinci indirme yok" kuralı: aynı gün içinde AG zaten var ve `--yenile` verilmediyse indirme atlanır.

**13-056** — YANLIŞ — `mtime == bugün` kopyalama/geri yükleme ile bozulur (`veri.py` satır 46). Yerine `manifest.json`'daki `indirme_zamani` / AG kimliğindeki tarih kullanılır.

**13-057** — KARAR — Okurken `manifest` sha256'sı doğrulanır (hızlı, 12 MB). Uyuşmazlık = hata, boş sonuç yok.

**13-058** — KARAR — Durup hata verir: "Veri bozuk: <ag_id>. Yedekten geri yükle: `yedek.cmd`". Otomatik indirme AG'yi değiştirirdi.

**13-059** — KARAR — Yedekten geri yüklenir (13-042). Yedek yoksa o AG'ye bağlı sonuçlar günlükte "doğrulanamaz" işaretlenir.

**13-060** — KARAR — Kısmi kalabilecek: `_gecici/` klasörü, `deneme.jsonl` son satırı. Başlangıçta `_gecici/` silinir, günlüğün son satırı JSON olarak okunur; bozuksa atılır. Anlık görüntü klasörleri rename ile atomik olduğundan yarım AG oluşmaz.

**13-061** — KARAR — Başlangıç kontrolü: günlükteki her `ag_id` için klasör var mı. Klasör yoksa uyarı. Günlükte olmayan klasör sorun değil (günlük yalnız sınama koşularını yazar).

**13-062** — CEVAPLI — Değişmezlik + atomik rename (13-029) bunu çözer: okuyucu yalnız tamamlanmış klasörü görür. Tek yazıcı olan günlük koşudur.

**13-063** — KARAR — Evet, sabitler: koşu başında `SON.txt` bir kez çözülür, `ag_id` günlüğe yazılır, koşu sonuna kadar o kullanılır.

**13-064** — KARAR — `veri/SON.txt` düz metin, içinde `ag_id`. Yazma: geçici dosya + `os.replace`. Sembolik bağ yok.

**13-065** — KARAR — Kilitsiz, ek kütüphane yok (`filelock` kurulu değil, doğrulandı). Değişmezlik + atomik rename yeter; tek örnek garantisi için 13-066.

**13-066** — KARAR — Görev Zamanlayıcı ayarı "Var olan örnek çalışıyorsa yeni örneği başlatma" (IgnoreNew). Ek olarak betik `veri/.kilit` dosyasını `os.open(..., O_CREAT|O_EXCL)` ile açar, açamazsa çıkar.

**13-067** — KARAR — Tam indirme (13-026) boşluğu kendiliğinden kapatır; her AG tüm geçmişi içerir. Boşluk: manifestte "önceki AG tarihi" ile fark; 3 günden uzunsa rapor başında yazılır.

**13-068** — KARAR — Tazelik: `SON.txt`'teki AG tarihi + manifest `son_cubuk_tarihi`; bugünkü işlem günü değilse kart yok. Sahip bunu raporun ilk satırında "VERİ ESKİ: <tarih>" olarak görür.

**13-069** — CEVAPLI — Yalnız parquet + AG klasörleri tek yazıcı noktasını fiyat tarafında ortadan kaldırır (yazıcı yalnız indirme koşusu, klasör yeni). Günlük `deneme.jsonl` tek yazıcıdır; yalnız sınama koşusu yazar ve 13-066 kilidi var.

**13-070** — CEVAPLI — Önbellek ve sembol bazlı kilit yok; tek örnek (13-066) ve geçici klasör var, çift indirme olmaz.

**13-071** — ZAYIF SORU — Ölçüldü: 12 MB bellekte, 0,13 sn okuma. Depolama seçimini etkilemez; bir kez yüklenir, bellekte tutulur.

**13-072** — KARAR — Tek uzun biçim `fiyat.parquet` (sembol, tarih sütunları): hem sembol hem gün sorgusu `groupby`/filtre ile aynı dosyadan. Hisse başına dosya düzeni bırakılır.

**13-073** — KARAR — Türetilmiş tablo yok; evren her koşuda `fiyat.parquet`'ten hesaplanır (13-025).

**13-074** — KARAR — Saklanmaz, her seferinde hesaplanır; bu yüzden geçersizleme ve türetme izi sorunu oluşmaz.

**13-075** — KARAR — Evet ayrı çıktı: `rapor/<koşu>/`. Her rapor başlığında `ag_id`. Çıktıların arşivlenmesi: `rapor/` yedeğe dahil, git'e girmez (yalnız md). Karşılaştırma sonradan.

**13-076** — KARAR — `faiz.parquet` aynı AG'de, küçük tablo (tarih, oran). Basamak seri olduğu için ayrı dosya; geçmiş düzeltilirse yeni AG'de fark görünür (13-008).

**13-077** — KARAR — Elle listeler `kayit/el-listeleri/bist30-2015.csv` olarak, sütunlar `sembol, tarih, kaynak_not` (duyuru adresi). Git'te. İndirilen veri kadar güvence taşımaz; raporda "elle girildi" yazılır.

**13-078** — OLGU — Doğrulanmadı: kullanım koşulları bulunamadı (`veri-kaynaklari.md` Bölüm 8.1, 150). Yerel kopya kişisel kullanım; `veri/` git dışı ve hiç yayımlanmaz. Saklama yasaklanırsa AG modeli çöker (yeniden üretim yok).

**13-079** — KARAR — Şirket kimliği ayrımı yok, sembol kodu anahtar (13-024). Bilinen sınırlama, rapora yazılır.

**13-080** — CEVAPLI — Olaylar AG içinde (13-017); günlükteki `ag_id` hem fiyatı hem olay tablosunu belirler. Ek alan gerekmez.

**13-081** — KARAR — "Veri sürümü" adı = AG kimliği `20261005-a1b2c3d4`. Tarih okunur, hash yalnız ayırt eder.

**13-082** — KARAR — Rapor ilk satırı: `Veri: 5 Ekim 2026 indirmesi (20261005-a1b2c3d4), son çubuk 2026-10-05, 100 sembol.`

**13-083** — KARAR — Günlük satırı kod hash'i, parametre, `ag_id` taşır; fark üçünden birine indirgenir. Veri farkı iki AG'nin `fiyat.parquet` karşılaştırmasıdır (13-008'in işlevi).

**13-084** — YANLIŞ — Doğrulandı: `pyproject.toml` yalnız pytest ayarı içeriyor. Fix: `pyproject.toml`'a `dependencies = ["pandas==3.0.6","pyarrow==25.0.1",...]` (venv sürümleri); `manifest.json` zaten pandas/pyarrow sürümünü yazar (13-047).

**13-085** — KARAR — Plan yok. pyarrow sürümleri arasında parquet geriye uyumlu okunur (belirtilmiş genel davranış; doğrulanmadı). Sürüm sabitleme (13-084) yeterli.

**13-086** — KARAR — Kart CSV: `to_csv(sep=";", decimal=",", encoding="utf-8-sig")`; Excel TR doğrudan açar. Veri dışa aktarımı yok.

**13-087** — KARAR — `veri/*.parquet` → `veri/yahoo/` (sadakat adımında kullanılacak). `rapor/islemler-20261005.parquet` ve `kanit-20261005.md` git geçmişinde kalır, yeni sistem oradan okumaz. Silme yok.

**13-088** — KARAR — Evet, ağsız: testler `tmp_path` içinde sentetik küçük AG üretir. Gerçek veri örneği git'e girmez (lisans bilinmiyor, 13-078).

**13-089** — KARAR — Depo kökü işlev parametresi, varsayılan `veri/`. Testler `tmp_path` verir; gerçek `veri/`'ye testten yazılamaz çünkü kök hiç verilmez.

**13-090** — KARAR — Değişiklik yok: `KLASOR` sabiti kalır; bir parametre (`kok=`) eklenir. Ortam değişkeni, yapılandırma dosyası yok.

**13-091** — KARAR — Disk dolu `OSError` atar; `_gecici/` klasörü atılır (13-029/13-060), AG oluşmaz. Sessiz kalma ihtimali yok çünkü rename yalnız tam yazım sonrası.

**13-092** — OLGU — Ölçüldü: 101 ayrı dosya 0,13 sn. Birleşik dosya kararı bu ölçüme ve 13-072'ye dayanıyor; 1.000 tekrarlı koşu belleğe tek yükleme olduğundan fark önemsiz.

**13-093** — KARAR — Kısa komut: `python -m tansu.bak AKBNK 2026-09-29` bir satır yazar. Yeni modül yok; ilk sürümde sahip rapordan okur, komut yalnız isterse eklenir.

**13-094** — CEVAPLI — Rapor yazımı geçici dosya + `os.replace` ile (13-045); ekran yalnız tamamlanmış dosyayı görür.

**13-095** — CEVAPLI — Tasarım zaten "küçük yüz" ve tek veri deposu modülü ister (§4). Diğer modüller yol bilmez; biçim değişirse yalnız bu modül etkilenir.

**13-096** — KARAR — Yüz: `ac(ag=None) -> Ag` (`.fiyat()`, `.olaylar()`, `.faiz()`, `.id`). `ag=None` ise `SON.txt` çözülür ve `.id` her zaman günlüğe yazılır.

**13-097** — KARAR — Varsayılan sessiz değil: `.id` rapor ilk satırına zorunlu yazılır (13-082). Yeniden üretim için `--veri <id>` açıkça verilir; kimlik verilmeyen koşu sahibe hangi veriyle koştuğunu söyler. Hata vermez.

**13-098** — CEVAPLI — Günlükte ya da raporda adı geçen AG silinmez (13-034, silme manuel ve "günlükte adı geçmeyen" kuralı). Ayrı koruma mekanizması gerekmez.

**13-099** — KARAR — Kalite sonuçları `rapor/<koşu>/kalite.md` olarak, `ag_id` başlıkta. AG'ye girmez (AG ham veridir).

**13-100** — KARAR — Maliyet düşük: tek modül (13-095), AG manifestleri sha256 içerir. Biçim değişirse yeni sürüm yeni AG olarak yazılır, eski günlük satırları eski `ag_id`'ye bağlı kalır ve eski AG'ler silinmediği için geçerli.

## Özet

Karar sayıları (100 soru): CEVAPLI 10, KARAR 76, YANLIŞ 6, OLGU 7, ZAYIF SORU 1 (grep ile sayıldı).

En önemli 10 kurulum kararı:

1. AG = tam kopya, tek klasör `veri/ag/<YYYYMMDD>-<8 hex>/` (fiyat, olaylar, faiz, borsapy, ham JSON, manifest); fiyat + olay aynı klasörde olduğu için tutarsız çift oluşamaz (13-001, 13-002, 13-020).
2. Biçim parquet, pandas + pyarrow; DuckDB/SQLite/CSV yok; Git LFS/DVC yok (13-004, 13-005, 13-041).
3. Yazma yalnız `_gecici/` içinde; tam ve doğrulanmış olursa `os.replace` ile klasör adı; yarım indirme atılır; `SON.txt` düz metin işaretçi, sembolik bağ yok (13-029, 13-045, 13-064).
4. Tam yeniden indirme her akşam (1 sn bekleme), artımlı yok; fark raporu: >%0,5 ya da son 5 günden eski değişiklik = hata (13-008, 13-026, 13-027).
5. Değişmezlik: salt okunur bayrak + manifest sha256; her koşu başında okuduğu AG'yi doğrular, bozuk dosya boş sonuç vermez, hata verir (13-006, 13-057).
6. `mtime` önbelleğini kaldır (`veri.py` satır 46); `temizle()` ve Yahoo kodu gider; eski `veri/*.parquet` → `veri/yahoo/` (13-003, 13-056, 13-087).
7. Yedek: haftalık `robocopy` ikinci diske ya da `OneDrive\TANSU-yedek` (OneDrive klasörü var, Desktop senkronize değil, doğrulandı); rapor ilk satırı yedek tarihini gösterir (13-039, 13-042, 13-043, 13-044).
8. `kayit/` git'te: `deneme.jsonl` (yalnız ekleme), kural kaydı, elle listeler; `rapor/*.parquet` git'ten çıkar; `veri/` zaten `.gitignore`'da (13-038, 13-040, 13-049).
9. Tek örnek: Görev Zamanlayıcı IgnoreNew + `veri/.kilit` (`O_CREAT|O_EXCL`); `filelock` yok (kurulu değil, doğrulandı); koşu başında AG kimliği çözülüp koşu boyunca sabit (13-063, 13-065, 13-066).
10. Rapor ve kart ilk satırı AG kimliği; Holm sayımı (aile, çıkış, parametre, kod_hash) anahtarına göre, tekrar ve yalnız veri değişimi şişirmez; `pyproject.toml` bağımlılıkları sürümle sabitlenir (13-050, 13-051, 13-082, 13-084).
