# Cevaplar 15: Yapılandırma, kural kaydı, deneme günlüğü

Doğrulanan olgular (venv `python -c` ve `git` ile): Python 3.14.7; pandas 3.0.6, numpy 2.5.3, statsmodels 0.15.0, pandas-ta-classic 0.8.32 kurulu; `pyproject.toml` yalnız pytest ayarı taşıyor; git var (`core.autocrlf=true`, 8 commit, uzak depo yok); `veri/` 12 MB (101 dosya) ve `.gitignore`'da; `rapor.py` zaten `np.random.default_rng(tohum)` kullanıyor; `ast.dump` yorum, boşluk ve CRLF farkından etkilenmiyor; `multipletests(method="holm")` çalışıyor. quantstats kurulu mu: doğrulamadım.

Aşağıdaki cevaplar şu tek kurulumu varsayar (ayrıntı Özet'te):
- Parametre dosyası yok. Kural parametreleri kodda donmuş dataclass; Levent düzenlemez.
- Kural kimliği = SHA-256(kod_hash + param_hash). Veri hash'i ayrı alan.
- Tek günlük: `kayit/deneme.jsonl`, JSON Lines, git'te, salt-ekleme.
- Tek giriş: `kosu()`. Holm = `statsmodels`, hipotez = kural kimliği.

**15-001** — KARAR — Ölçüt: sonucu değiştiren her değer kodda durur (donmuş dataclass) ve hash'e girer. Dosya yok. Not: `kanit.py` `MASRAF = 0.002`, TASARIM 5.4'ün %0,3'üyle uyuşmuyor (ön deneme kodu; yeni motorda düzelir).
**15-002** — KARAR — Ek ayrı dosya olmaz. Kayıt = `kayit/deneme.jsonl` içindeki `"tur":"kayit"` satırı; parametreler tam JSON kopya. Satırı `kosu()` yazar; değerleri ajan kodda yazar.
**15-003** — KARAR — Levent dosya düzenlemez; yalnız kod (ajan) değişir. Virgül/nokta hatası doğmaz; tür hatasını dataclass tip ek açıklaması ve pytest yakalar.
**15-004** — ZAYIF SORU — Parametre dosyası olmayacağı için YAML/TOML yok. Python sayı değişmezi "no" ya da "1e3"ü sessizce başka türe çevirmez.
**15-005** — KARAR — Şema tek yerde: stdlib `@dataclass(frozen=True)`, aile başına bir tane. Bilinmeyen anahtar dosya olmadığı için imkânsız; yanlış alan adı yazan kod `TypeError` verir.
**15-006** — KARAR — "Kural" = sinyali ve işlemi belirleyen her değer (EMA bandı, pencereler, ATR, stop, pozisyon %10, likidite %2, sermaye). "Sınama ayarı" = tekrar sayısı, blok uzunluğu, tohum, ızgara tanımı, masraf senaryo listesi. Yalnız kural hash'e girer; sınama ayarı günlükte ayrı alan.
**15-007** — KARAR — Likidite, pozisyon, sermaye kuralda (hash'e girer). Masraf %0,1/%0,3/%0,5 aynı koşuda birlikte hesaplanır (TASARIM 5.4); tek deneme, senaryo listesi sınama ayarı. Taban masrafı değişirse simülatör kodu değişir, kod hash'i değişir, yeni deneme olur.
**15-008** — KARAR — Izgara tanımı sınama ayarıdır; hash dışı, günlükte yazılı. Hücreler deneme sayılmaz; tek `"tur":"destek"` satırı olur (hücre sayısı, pozitif oran).
**15-009** — KARAR — YORUM alanları dataclass alanında `field(metadata={"yorum": True})` ile işaretlenir; kayıt satırı YORUM alan adlarını ayrıca listeler. İşaretsiz alan "kaynaktan gelen"dir.
**15-010** — KARAR — Sadakat adayları `"tur":"sadakat"` satırı olarak yazılır (getiri alanı yok). Seçilen değer kural kaydına girer. Adaylar Holm'a girmez: p yok ve seçim getiriye bakmaz (KURALLAR §4).
**15-011** — KARAR — Tek modül; aile başına dataclass ve ortak bir `RiskPaketi` dataclass'ı. Ortak değer değişirse üç ailenin kural kimliği de değişir; üçü de yeni deneme. Doğru: sonuç gerçekten değişir.
**15-012** — KARAR — Varsayılanlar dataclass'ta (kodda). Hash'lenen şey `asdict()` ile doldurulmuş son hâl. Dosya olmadığı için eksik anahtar sorunu yok.
**15-013** — KARAR — Ortam (yol, kullanıcı adı, saat dilimi) dataclass'ta bulunmaz; hash yalnız dataclass ve kod listesinden hesaplanır. Güvence: bir pytest `Path`/`str` yol alanı olmadığını denetler.
**15-014** — CEVAPLI — Git var (`git log`: 8 commit); AGENTS.md ve `issue-tracker.md` uzak depo olmadığını söylüyor (yerel `.scratch/`). Eski sürüm `git log -p` ile gelir. `kayit/` git'te durur; `veri/` dışarıda.
**15-015** — KARAR — Hayır, kütüphane gerekmez. `tomllib` bile gerekmez: dosya yok, stdlib dataclass yeter. Ölçüt basamak 1 (gerek yok), 3 (stdlib).
**15-016** — KARAR — Hash, elle yazılmış `KOD_DOSYALARI` listesindeki dosyaların tamamını kapsar: aileler, göstergeler (ema/atr), motor, Adım, simülatör, K1 üreticisi. Şu an: `aileler.py`, `kanit.py`; yeni dosyalar yazıldıkça listeye girer.
**15-017** — KARAR — Elle liste. Unutmaya karşı pytest: `tansu/*.py` içindeki her dosya ya `KOD_DOSYALARI`'nda ya `HASH_DISI`'nda olmalı; yoksa test düşer. Import grafiği gereksiz.
**15-018** — KARAR — Evet, motor düzeltmesi bütün ailelerin kural kimliğini değiştirir. İstenen davranış: motor değişince sonuç değişmiş olabilir; yeniden koşu zorunlu. Eski kayıtlar silinmez (15-035).
**15-019** — KARAR — Veri hash'e girmez. TASARIM 5.8 (hash: kural, parametre, kod) ile 5.11 (günlükte veri anlık görüntüsü) çelişmez: veri ayrı `veri_hash` alanıdır. Aynı kural farklı veri = aynı hipotez, ayrı koşu satırı.
**15-020** — KARAR — Üç ayrı alan: `kod_hash`, `param_hash`, `veri_hash`. `kural_id = sha256(kod_hash + param_hash)` türetilir. Değişimin kaynağı alan karşılaştırmasıyla görünür.
**15-021** — KARAR — SHA-256 (`hashlib`). Günlükte tam 64 hane; ekranda ilk 12. Kısaltma yalnız gösterimde; kayıtta kısaltma olmadığı için çakışma riski yok.
**15-022** — YANLIŞ — Ham kaynak metin hash'i boşluk/yorum/biçim değişince sahte yeni deneme üretir. Düzeltme: `ast.dump(ast.parse(kaynak))` hash'lenir (stdlib; doğrulandı: yorum, boşluk, CRLF etkisiz).
**15-023** — KARAR — Çizgiyi mekanik kural çeker: AST değişirse "anlamlı". Değişken adı değişimi de yeni deneme olur; kabul (katı yön, Holm'u şişirmez çünkü gereğinden fazla değil, sahibin refaktörü seyrek). Çizgiyi kimse elle çekmez.
**15-024** — KARAR — İlk sürümde davranış hash'i yok. Levent bakım yapamaz/yapmaz. Davranış denetimi: mevcut elle hesaplanmış motor sınamaları (5.3) ve 15-097'deki tek altın pytest.
**15-025** — OLGU — Doğruladım: `core.autocrlf=true`; ama `ast.dump` CRLF ve LF için aynı çıktıyı verdi, yorum ekini de yok saydı. AST hash'i autocrlf'ten ve BOM'dan etkilenmez.
**15-026** — KARAR — Kütüphane sürümleri hash'e girmez; günlükteki `ortam` alanına `importlib.metadata` ile yazılır (pandas, numpy, pandas-ta-classic, statsmodels, quantstats). Sürüm kilidi 15-027 ile asıl önlem.
**15-027** — KARAR — Evet. `pyproject.toml`'a `dependencies` bölümü, venv'de kurulu sürümlerle `==` sabitlenmiş (pandas 3.0.6, numpy 2.5.3 vb.). `uv.lock` gerekmez. Doğrulandı: şu an bağımlılık bildirimi yok.
**15-028** — KARAR — Python sürümü günlükte `ortam.python` olarak yazılır (venv şimdi 3.14.7), hash'e girmez. `pyproject`'a `requires-python = "==3.14.*"` yazılır; `ast.dump` biçimi sürümler arası değişebilir, bu yüzden sürüm sabit.
**15-029** — KARAR — Kanonik biçim: `json.dumps(asdict(p), sort_keys=True, separators=(",", ":"))`. Float alan tipi `float`, int alan `int`; `__post_init__` float alanı `float()` ile çevirir. Kaynak sabitleri kodda tek yazılışlı olduğu için 0.012/1.2e-2 sorunu kalmaz. Bir pytest bunu denetler.
**15-030** — ZAYIF SORU — Parametre dosyası olmadığından ham metin yok; hash ayrıştırılmış nesnenin (dataclass) JSON'u üzerinden.
**15-031** — KARAR — Ad hash'e girmez; günlükte `aile` etiketi. Aynı kod ve parametreyle iki ad = tek kural kimliği, tek hipotez.
**15-032** — KARAR — Yalnız türetme kuralı (kod + parametre) hash'e girer. Türetilen çift listesi veriden gelir; her koşunun `sonuc` alanına yıl→çiftler olarak yazılır.
**15-033** — KARAR — Tohum ve tekrar sayısı sınama ayarıdır, hash dışı, günlükte yazılı. Tohum değişince p değişir ama yeni deneme olmaz; Holm'a her kural kimliğinin ilk resmi koşusunun p'si girer (15-082).
**15-034** — KARAR — Otomatik, her koşuda `kosu()` içinde. Kayıt satırı yoksa veya hash uyuşmazsa `kosu()` durur ve tek Türkçe satır yazar. Kayıt satırını ise "kural kaydı" adımında `kosu --kaydet` yazar.
**15-035** — KARAR — Kod değişirse yeni kural kimliği, yeni hipotez. Eski kayıt silinmez ve Holm'da kalır (p'siyle ya da p'siz ise p=1). Düşmez: kötümser yön.
**15-036** — KARAR — Evet: `tests/test_hash.py` (boşluk, yorum, CRLF değişmez; sabit, ad, yeni satır değişir). Bu olmadan kural denetlenemez.
**15-037** — KARAR — Hash bu söze uymaz: fonksiyonu başka modüle taşımak AST'yi değiştirir, yeni deneme olur. TASARIM 4'ün sözü arayüz sözüdür, hash sözü değil. Kabul; refaktör seyrek ve kayıt öncesi yapılır.
**15-038** — KARAR — Hayır. Bayt kodu Python sürümüne bağlı ve okunamaz. AST seçilir (15-022).
**15-039** — KARAR — Test dosyaları hash'e girmez. Test, doğruluğun kanıtıdır; test değişimi kural kodunu değiştirmez.
**15-040** — KARAR — Kural kaydı, günlükteki bir satırdır: `kayit/deneme.jsonl` içinde `"tur":"kayit"`. Ayrı dosya ve git etiketi yok.
**15-041** — KARAR — JSON Lines (stdlib `json`). SQLite de stdlib ama salt-ekleme ve `git diff` okunabilirliği için düz metin daha az altyapı. DuckDB yok.
**15-042** — KARAR — Zorlayan: kod dosyayı yalnız `"a"` modunda açar; her koşu sonu `kosu()` `kayit/`'i otomatik commit eder. Koşu başında `kayit/` kirliyse (elle düzenleme) `kosu()` durur. Fark eden: git.
**15-043** — YANLIŞ — Hash zinciri aşırı mühendislik. Yerine: 15-042'deki otomatik git commit.
**15-044** — KARAR — Önce `"olay":"basladi"` satırı, sonra `"olay":"bitti"` satırı. Çöken koşunun "basladi" satırı kalır ve deneme sayılır.
**15-045** — KARAR — İki satır, ikisi de eklenir; hiçbir satır güncellenmez (salt-ekleme korunur). Atılan koşu "bitti"siz "basladi" olarak görünür ve sayılır; beğenilmeyen koşuyu gizlemek mümkün olmaz.
**15-046** — KARAR — Zorunlu alanlar: 5.11 listesi + "bitti" satırında ham p, etki büyüklüğü, tekrar sayısı, tohum, masraf düzeyi başına sonuç, süre, `kosu_id`, `git_commit`, `ortam`, `sema`. 5.11 listesi asgari kabul edilir.
**15-047** — KARAR — Tam kopya (parametre JSON) ve `param_hash` birlikte tutulur. Yalnız hash olursa değerler geri kazanılamaz.
**15-048** — KARAR — Evet, "bitti" satırında sonuçlar ve p'ler. Holm p'leri buradan okur; ayrı p deposu yok.
**15-049** — KARAR — Git aynı diskte; yeterli değil. Levent `kayit/` klasörünü ayda bir harici diske ya da OneDrive'a kopyalar. Her rapor başlığı toplam satır sayısını yazar; kayıp görünür olur.
**15-050** — KARAR — Kilit yok. Tek kullanıcı; 19:30 görevi veri günceller, getiri koşusu yazmaz. Her satır tek `write` çağrısıyla `"a"` modunda yazılır.
**15-051** — KARAR — Düzeltme satırı eklenir (`"tur":"duzeltme"`, `hedef_kosu_id`, yeni değer). Asıl satır silinmez ve değişmez.
**15-052** — KARAR — Aynı günlük. Geliştirme koşuları da yazılır (`resmi:false`, 200 tekrar). Holm'da her kural kimliği bir kez sayılır, kaç koşu olursa olsun; p'yi ilk resmi koşu verir. Böylece dev koşuları m'i şişirmez, kapı da açılmaz.
**15-053** — KARAR — Evet, `"tur":"sadakat"` olarak yazılır; Holm'a girmez (p yok, getiriye bakılmaz).
**15-054** — KARAR — UTC, ISO 8601 (`datetime.now(timezone.utc)`). Saat kaynağı Windows saati; ikinci tanık git commit tarihi. Saat oynatma riski kabul edilir (tek kullanıcı, kasıt yok varsayımı).
**15-055** — KARAR — Her koşu `kosu_id = uuid4().hex` taşır. Rapor dosya adı, CSV adı ve rapor başlığı bu kimliği yazar.
**15-056** — KARAR — Bir satır = bir koşu = bir kural kimliği (aile × parametre kümesi). Çift bölmesi tek birimdir; bölme ve hücre sonuçları `sonuc` içinde alt alan.
**15-057** — KARAR — Her satırda `"sema":1`. Yeni alan eklenince eski satırlar `dict.get` ile okunur; sema numarası yalnız alan anlamı değişirse artar.
**15-058** — KARAR — Levent açmaz; `kosu` raporu özetler. UTF-8, ondalık nokta (JSON). Excel uyumu hedef değil.
**15-059** — KARAR — Satırlar kalır; aile tasarımdan çıksa da Holm'dan düşmez (kötümser).
**15-060** — KARAR — Ayrı klasör: `kayit/` (git'te, silinmez, temizlenmez) ve `rapor/` (yeniden üretilebilir). Rapor üretici `kayit/`'e yalnız okuma yapar.
**15-061** — KARAR — Hipotez = kural kimliği. Aynı ailenin üç parametreli üç koşusu üç hipotez. Kasıtlı katı.
**15-062** — CEVAPLI — Evet, geriye dönük büyür; Canlı olmuş aile geri düşebilir. 5.11 "o ana kadarki bütün denemeler" diyor. İstenen davranış; rapor Holm'u tarih ve m ile birlikte yazar.
**15-063** — KARAR — m = günlükteki benzersiz kural kimliği sayısı (her biri en az bir koşuda). Satır sayısı ve aile sayısı değil.
**15-064** — KARAR — Kabul edilen bedel. Holm bağımsızlık gerektirmez, katıdır; P3 "kabul ölçütü gevşetilmez" ile uyumlu. Gerçek kuralın elenmesi yanlış canlıya girmekten ucuzdur.
**15-065** — KARAR — Her kural kimliği için tek p: %0,5 masraf düzeyinde K1'in iki türünden (a, b) büyük olanı. K2 ve masraf düzeyleri ayrı test değil; kabul ölçütünün diğer koşulları.
**15-066** — KARAR — Üç düzey tek deneme; Holm'a en katı düzeyin (%0,5) p'si girer. m şişmez.
**15-067** — KARAR — Yıllık p'ler `sonuc.yillik` altında yazılır, Holm'a girmez. Holm yalnız `sonuc.birlesik_p` alanını okur; alan adı ayırıcıdır.
**15-068** — KARAR — `statsmodels.stats.multitest.multipletests(method="holm")` (kurulu 0.15.0, çalıştırıp doğruladım). Holm kesin bir formül; sürüm değişimi sonucu değiştirmez. Kendi kodumuz gereksiz.
**15-069** — KARAR — Holm kalır: FWER denetimi, kabul ölçütü sıkı (P3). BH (FDR) gevşek. Yeniden gözden geçirme tetikleyicisi koymuyorum; YAGNI. Değişiklik sahip kararı.
**15-070** — KARAR — Evet, `tur` alanı: `deneme`, `destek` (ızgara, yeniden üretim, sınama), `sadakat`. Holm yalnız `deneme` satırlarından kural kimliği sayar.
**15-071** — KARAR — Hata veren koşu "basladi" satırı bırakır; kural kimliği m'de sayılır. Sonuçsuz kural kimliği Holm'a p = 1 ile girer (kötümser; kendi kararını da etkilemez).
**15-072** — KARAR — Kodda engel: getiri gösteren tek yol `kosu()` (15-074). Geçmiş serbest koşular için tek elle `"tur":"gecmis"` satırı yazılır: sahibin bildiği tahmini sayı, her biri p = 1 ile m'e eklenir. Tahmin eksik kalabilir; raporda yazılır.
**15-073** — KARAR — Kod sağlar: `kosu()` günlüksüz sonuç döndürmez. Ek olarak AGENTS.md'ye tek cümle talimat. Ajan motor iç fonksiyonunu `python -c` ile çağırabilir; bu açığı talimat ve git incelemesi kapatır, kod tam kapatmaz. Açık kalan risk.
**15-074** — KARAR — Evet. Tek `kosu()`; getiri döndüren motor iç fonksiyon. Notebook yok. Ekran ve rapor `kosu()` dışında getiri hesaplamaz.
**15-075** — KARAR — Parametre oynatan kontrol yok; Kanıt ekranı yalnız `rapor/`'u okur (TASARIM 3: "raporu okur"). Sınır koda yazılı: ekran modülü `tansu` motorunu import etmez; pytest import denetler.
**15-076** — KARAR — Rapor üretilirken yeniden hesaplanır; rapor başlığına m ve hesap tarihi yazılır. Üretilmiş eski rapor dosyası değişmez, anlık görüntü günlüğe yazılmaz.
**15-077** — KARAR — Rastgele test p'si `(b+1)/(n+1)`. Eşit p'ler `multipletests` ile kararlı sıralanır; sorun eşitlikte değil p tabanında (15-078).
**15-078** — YANLIŞ — Sabit n=1.000 ile m≥50'de kabul imkânsız (p tabanı 0,001 > 0,05/m). Düzeltme: `n = max(1000, 200·m)` (p tabanı ≈ α/(10m)). m=60 için 12.000 tekrar; koşu süresi ölçülmedi.
**15-079** — KARAR — Yeniden üretim kontrolü `"tur":"destek"` satırı olur; m'e girmez.
**15-080** — KARAR — Önbellek yok (YAGNI); aynı koşu yeniden hesaplanır. Anahtar gerekmez; yeniden üretim kontrolü zaten destek satırı.
**15-081** — KARAR — Aynı kural kimliği, farklı veri = aynı hipotez. 19:30 yenilemesi getiri koşusu yazmaz (yalnız canlı kartlar), günlük şişmez.
**15-082** — KARAR — Hayır, yeni hipotez değil. Holm p'si her kural kimliğinin ilk resmi koşusundan alınır; sonraki koşular `destek`. Tohum seçerek p oynamak sonuç değiştirmez.
**15-083** — KARAR — Deneme kimliği = kural kimliği. İkinci tıklama aynı kimlik, m artmaz; ek satırlar yalnız koşu kaydı.
**15-084** — KARAR — Reddetme yok: `kosu_id` benzersiz, sayım `kural_id` üzerinden. Geçerli yeniden koşular `destek` ya da ek koşu olarak yazılır.
**15-085** — KARAR — Geri alınan değer eski hash'e döner: yeni deneme değildir. 0,013 bir yeni hipotezdir. Üç koşu = iki kural kimliği.
**15-086** — KARAR — Geri alma yok. İptal `duzeltme` satırıyla etiketlenir; m'den düşmez (kötümser). Yanlış tıklama için bedel kabul.
**15-087** — KARAR — Izgara tek `destek` satırı (hücre sayısı, pozitif oran). Hücre başına hash ve deneme yok; Holm sepetini büyütmez.
**15-088** — KARAR — Tekrarlar yazılmaz. "bitti" satırında yalnız özet: p, tekrar sayısı, tohum.
**15-089** — KARAR — Kod denetler: `kosu()` kural kimliği için kayıt satırı arar, yoksa durur. Süreç kuralı değil.
**15-090** — KARAR — Evet, kapı `kosu()` içinde. Motor testleri motor fonksiyonunu doğrudan çağırır (sentetik, elle hesaplanmış veri); kapıya takılmaz. Gerçek veriyle koşu `kosu()` zorunlu. Muaf = sentetik veri.
**15-091** — KARAR — Saklanan: `git_commit`, param kopyası, tohum, `ortam` (Python + kütüphane sürümleri), `veri_hash` + anlık görüntü dosyaları. Biri eksikse iddia boş kalır; hepsi satırda ya da diskte.
**15-092** — OLGU — Ölçtüm: `veri/` = 12 MB. Her gün kopya yılda yaklaşık 4,4 GB, gereksiz. Karar: anlık görüntü yalnız resmi koşuda Parquet olarak `veri_anlik/<hash12>/` altına kopyalanır (~12 MB, koşu başına). Silinirse o koşu yeniden üretilemez; silinmez.
**15-093** — KARAR — Kimlik içerik hash'i (SHA-256, sıralı dosya baytları); tarih etiket olarak ek. Aynı gün iki indirme farklı veri getirirse iki kimlik.
**15-094** — KARAR — Tohum sınama ayarında; kodda tek sabit ana tohum, her koşuya `SeedSequence(ana).spawn` ile türetilir, günlüğe yazılır. Mevcut `rapor.py` `default_rng(tohum)` alıyor (doğrulandı); mantık bozulmaz.
**15-095** — KARAR — Her koşuya `Generator` geçirilir; küresel `np.random.seed` yok. İlk sürümde paralellik yok (YAGNI); olursa `SeedSequence.spawn`.
**15-096** — KARAR — Tam garanti yok: NumPy `Generator` akışını sürümler arası garanti etmez. Bu yüzden 15-027 kilidi ve günlükteki `ortam`; sürüm değişince altın sınama (15-097) kırılırsa yeniden üretim iddiası ilgili koşular için sona erer.
**15-097** — KARAR — Sürekli: `pytest` içinde tek altın sınama (sabit sentetik veri, bir ailenin sinyal günleri ve p). Güncellemeyi ajan yapar, kod değişim gerekçesiyle.
**15-098** — KARAR — Tolerans: `pytest.approx(rel=1e-9)`. Bit düzeyi aranmaz. Hash'e sonuç girmez; yuvarlama gereksiz.
**15-099** — KARAR — Günlük `git_commit` yazar; kod git'te kalır. Resmi koşu için `tansu/` ve `kayit/` temiz olmalı (değilse `kosu()` durur); geliştirme koşusu `"kirli":true` yazar.
**15-100** — KARAR — Sınır: günlük + hash + `kosu()` + Holm + git commit. Zincir, önbellek, kilit, davranış hash'i yok. "Hash uyuşmuyor": terminalde tek satır ("Kod kayıttan farklı: kural_id ... Yeni kayıt gerekir"); Levent bir şey yapmaz, bu satırı ajana iletir.

## Özet

Karar sayıları: KARAR 91, CEVAPLI 2, YANLIŞ 3, OLGU 2, ZAYIF SORU 2 (toplam 100).

En önemli 10 kurulum kararı:
1. Parametre dosyası yok. Parametre = `@dataclass(frozen=True)` (aile başına bir, ortak `RiskPaketi`), kodda; Levent düzenlemez. TOML/YAML/pydantic yok. (15-001..005, 015)
2. Hash kapsamı: elle yazılmış `KOD_DOSYALARI` listesi (şimdi `aileler.py`, `kanit.py`; motor, Adım, simülatör, K1 gelince eklenir) + pytest ile "her dosya listede ya da HASH_DISI" denetimi. Test dosyaları ve rapor dışında. (15-016..018, 039)
3. Hash biçimi: kod için `sha256(ast.dump(ast.parse(kaynak)))`; boşluk, yorum, CRLF, BOM etkisiz. Parametre için `sha256(json.dumps(asdict(p), sort_keys=True, separators=(",",":")))`. Bayt kodu ve ham metin yok. (15-022, 025, 029, 038)
4. Üç ayrı alan: `kod_hash`, `param_hash`, `veri_hash` (tam 64 hane SHA-256). `kural_id = sha256(kod_hash + param_hash)`. Veri, ad, tohum, tekrar, ortam yolu hash dışı. (15-019..021, 031, 033)
5. Günlük: `kayit/deneme.jsonl`, JSON Lines, UTF-8, her satırda `"sema":1`, git'te; kural kaydı da aynı dosyada `"tur":"kayit"` satırı. Satır türleri: `kayit`, `deneme`, `destek`, `sadakat`, `gecmis`, `duzeltme`. (15-040, 041, 057, 070)
6. Salt-ekleme: dosya yalnız `"a"` modunda açılır; her koşu sonu `kayit/` otomatik git commit; başta `kayit/` kirliyse `kosu()` durur. Hash zinciri yok. Her koşu önce `basladi`, sonra `bitti` satırı yazar; çöken koşu sayılır. (15-042..045)
7. Tek giriş `kosu()`: kural kaydı yoksa ya da hash uyuşmuyorsa durur; getiri gösteren başka yol yok (motor iç fonksiyon, Kanıt ekranı motoru import etmez). Resmi koşu temiz git ağacı ister; `git_commit` günlükte. (15-034, 073, 074, 089, 090, 099)
8. Holm: hipotez = benzersiz `kural_id` (m); p = ilk resmi koşunun %0,5 masrafta K1 iki türünden büyük p'si; yıllık p'ler Holm dışı; p'siz kimlik p = 1; `statsmodels` `multipletests(method="holm")`, rapor üretirken m ve tarihle yeniden hesaplanır. (15-052, 061..068, 071, 076)
9. Tekrar sayısı `n = max(1000, 200·m)`, aksi halde m ≥ 50'de kabul matematiksel olarak imkânsız (p tabanı 1/(n+1)). Tohum: tek ana tohum + `SeedSequence.spawn`, her koşuya `Generator`, günlüğe yazılır; tohum değişimi yeni deneme değil. (15-078, 082, 094, 095)
10. Yeniden üretim: `pyproject.toml`'a `==` sabitli bağımlılıklar ve `requires-python = "==3.14.*"`; günlükte `ortam` (Python + kütüphane sürümleri) ve `git_commit`; veri anlık görüntüsü yalnız resmi koşuda `veri_anlik/<hash12>/` altına Parquet kopya (~12 MB); `kayit/` ayda bir harici yedek. (15-026..028, 049, 091..093)
