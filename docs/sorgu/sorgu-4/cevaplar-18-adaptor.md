# Cevaplar 18: Dış kaynak adaptörleri

Doğrulama: pyproject.toml (yalnız pytest ayarı, bağımlılık yok), `.venv` paket listesi (requests 2.34.2, httpx 0.28.1, pydantic 2.13.5, pyarrow 25.0.1, pymupdf 1.28.2, yfinance 1.7.0, borsapy 0.11.0 kurulu), `tansu\veri.py` (yfinance + eşikli `temizle` + parquet, dosya tarihine bakar), `.gitignore` (`.venv/`, `veri/` var; `.env` yok), bir canlı İş Yatırım `HisseTekil` isteği (THYAO, 29-09-2026..01-10-2026).
Canlı istekten olgu: sayılar JSON sayısı (ondalık virgül yok); `HGDG_TARIH` metin `dd-mm-yyyy`; `END_TARIH` ms epoch = 1790629200000 = 28.09.2026 21:00 UTC = 29.09.2026 İstanbul gece yarısı (UTC+3). `SHHE_TARIH` için aynı biçim varsayılır, doğrulanmadı.
Genel karar: tek dosya `tansu\kaynak.py` (İş Yatırım, borsapy, KAP, EVDS fonksiyonları). Tek HTTP istemcisi `requests` (kurulu, senkron). Her fonksiyon DataFrame döner, diske yazmaz.

**18-001** — KARAR — Yazılı değil. Karar: dış kaynaklar tek modülde, `tansu\kaynak.py`; Veri deposu (`veri.py`) yalnız onu çağırır ve anlık görüntüyü yazar. Sınır = fonksiyon imzası, sınıf yok.

**18-002** — KARAR — `requests` (kurulu, borsapy ve yfinance bağımsız). Seçimi bu belge yapar; kural: kurulu olan, senkron olan, yeni bağımlılık eklemeyen. httpx kurulu ama gereği yok.

**18-003** — KARAR — Kendi çağrımız: tek `requests.get` + `.json()["value"]`, yaklaşık 10 satır. isyatirimhisse kurulmaz: aynı uç noktayı sarar (doğrulanmadı), IP engeli uyarısı taşır, bir bağımlılık daha ekler.

**18-004** — ZAYIF SORU — 10 satırlık GET bir "kütüphane yerine kod" sayılmaz; `requests` zaten güvenilir kütüphanedir. İstek karşılandı; kütüphane eksikliği değil, belgesiz uç nokta riski var (18-095).

**18-005** — KARAR — Evet. `pyproject.toml` içine `dependencies` ve `==` sürümleri yazılır (borsapy==0.11.0). Anlık görüntü zaten ham veriyi dondurur; borsapy yalnız çapraz kontrol olduğundan sürüm değişimi backtest sonucunu değiştiremez.

**18-006** — CEVAPLI — Fiyat için borsapy birincil değil (TASARIM §4: çapraz kontrol). Şirket olayları için borsapy kullanılmıyor (İş Yatırım ham). Kusur yalnız kontrol sonucunu bulandırır; sonuçlara girmez.

**18-007** — YANLIŞ — Premis kısmen yanlış: TASARIM §4 borsapy'yi çapraz kontrol, faiz, kapanmış sembol ve sektör için sayar; evren CSV'si ara çözüm. Fix: dört işi ayrı fonksiyon yap (`kaynak.py` içinde); biri kırılırsa yalnız o iş durur. Faiz tek seferlik dondurulur (18-059), sektör tek seferlik dondurulur.

**18-008** — KARAR — Borsapy "kişisel ve eğitim" ve İş Yatırım "kişisel kullanım" kalır. Karar: README ve rapor altbilgisine "yalnız kişisel kullanım, dağıtma" yaz; paylaşılırsa sorumlu Levent. Kod bunu zorlamaz.

**18-009** — KARAR — Atlanır, durmaz. Çapraz kontrol başarısızsa kontrol "yapılmadı" diye kart ve raporda yazılır; kart yine üretilir (birincil İş Yatırım). Kabul kararı için tam karşılaştırma gerekir; bir kez yapılmış ve dondurulmuş karşılaştırma yeter.

**18-010** — OLGU — Doğrulanmadı (sayılmadı). Hesap: HisseTekil tek çağrıyla 11 yıl döner (THYAO 2945 satır, veri-kaynaklari §3.2). 100 hisse = 100 çağrı + 100 `GetSermayeArttirimlari` (+100 oturum GET) ≈ 300 istek. Kapanmış semboller +N. "Az sayıda" = bu.

**18-011** — KARAR — Tek seferde, sıralı, 1 sn aralıkla (~300 istek ≈ 5–10 dk). Ban riski sıfır değil; sınanmadı (veri-kaynaklari §8.1). Önlem: 429 veya boş yanıtta dur, ertesi gün kaldığı yerden sürdür (18-088).

**18-012** — KARAR — 1 saniye, kodda sabit `BEKLE = 1.0` (`kaynak.py` başında). Ayar dosyası yok; owner dokunmaz, Claude oturumu değiştirir.

**18-013** — KARAR — `time.sleep(BEKLE)`. tenacity ve pyrate-limiter kurulu değil; ~300 istek için gereksiz.

**18-014** — KARAR — Tek döngü, `kaynak.py` içinde: 3 deneme, sabit bekleme 5 sn, 15 sn, 45 sn (üstel). Yalnız bağlantı kopması, zaman aşımı, 429 ve 5xx denenir. 4xx (429 hariç) ve boş yanıt denenmez. 429 gelirse 5 dk bekle, bir kez daha dene, yine 429 ise dur.

**18-015** — KARAR — Ayrım HTTP'den değil sorgudan yapılır: aynı hisse için bilinen geniş aralık (örn. son 10 gün) sorgulanır. Boş çıkarsa "hisse yok / kapalı"; başka hisse çalışıyorsa hisse yok, hiçbiri çalışmıyorsa "engellendim" (tüm koşu durur). Canlı sınandı: hisse çalışırken `ok:true` ve `value` dolu döner; boş gövde davranışı doğrulanmadı.

**18-016** — KARAR — `timeout=(5, 30)` her istek için; bütün koşu için 20 dk üst sınır. Süre dolarsa kart üretilmez (§6.1) ve rapor "veri alınamadı" yazar.

**18-017** — KARAR — Yalnız `User-Agent: tansu-kisisel` ve `Accept: application/json`. Tarayıcı taklidi yok. İş Yatırım bunu reddederse (canlı sınamada requests'in varsayılan UA'sı çalıştı) o zaman Referer eklenir; borsapy de Referer gönderiyor.

**18-018** — KARAR — Oturum çerezi yalnız `GetSermayeArttirimlari` için gerekir. Fark etme: yanıtta `ok != true` ya da `value` listesi yoksa hata fırlat. Sayfa yapısına bağımlılık yok (çerez yalnız GET ile alınır).

**18-019** — KARAR — Her koşuda baştan (`requests.Session`, bellekte). Diske yazılmaz; gizli sayılmaz çünkü saklanmaz.

**18-020** — KARAR — "Bugün" tek yerde: `datetime.now(ZoneInfo("Europe/Istanbul")).date()` (`tzdata` kurulu). Türkiye'de yaz saati yok (UTC+3 sabit). Windows saati yanlışsa tarih yanlış çıkar; tazelik kontrolü (son çubuk tarihi) bunu yakalar, ayrı önlem yok.

**18-021** — CEVAPLI — Canlı doğrulandı: sayılar JSON sayısı (`291.5000`, `8105661396.000000`), ondalık virgül yok. `HGDG_TARIH` metin `dd-mm-yyyy`; `pd.to_datetime(..., format="%d-%m-%Y")` ile ayrıştırılır.

**18-022** — OLGU — Doğrulandı (canlı `END_TARIH`): epoch İstanbul gece yarısı (UTC+3). `SHHE_TARIH` için aynı kabul, doğrulanmadı. Karar: tarih `pd.to_datetime(ms, unit="ms", utc=True).tz_convert("Europe/Istanbul").normalize().tz_localize(None)`. Test: CCOLA bedelsiz 2024-08-13 (ham kapanış düştüğü gün) ile olay tarihi eşit olmalı. Veri-kaynaklari §1.2 zaten bu eşitliği ölçtü.

**18-023** — KARAR — Adaptörde sabitlenmez; adaptör ham `HG_HACIM` verir. Birim ilk veri işinde (fiyat × lot ile) çözülür, sonuç `GLOSSARY.md` ve bir sabit (`HACIM_TL = True/False`) olarak yazılır. Canlı: THYAO HGDG_HACIM 8,1 milyar, fiyat 291; 8,1 mlr/291 = 27,8 mn lot. TL gibi görünüyor ama THYAO için tek örnek yetmez.

**18-024** — KARAR — Takvim modülü "bu gün beklenir mi" sorusunu yanıtlar; adaptör yalnız ne varsa döner. Yarım gün alanları sorunsuz kabul edilir; tazelik kontrolü son çubuk tarihine bakar.

**18-025** — KARAR — Düz kod: `kaynak.py` içinde `assert set(SUTUNLAR) <= set(f.columns)`, `f.index.is_monotonic_increasing`, `f.index.is_unique`, kapanış > 0. pydantic kurulu ama pandera yok; tablo için gereksiz.

**18-026** — KARAR — Hata fırlat. `f[SUTUNLAR]` seçimi eksik sütunda `KeyError` verir (sessiz NaN değil). Kod `f.get` kullanmaz.

**18-027** — KARAR — Anlam değişimini yalnız `HGDG/HG` oranı ve kapanış sürekliliği (18-029, §5.1 karantina) yakalar. Ek kontrol yok. Birim değişimini "fark %0,5 üstü" çapraz kontrol de yakalar.

**18-028** — KARAR — Dur: kart üretilmez, rapor "veri şeması değişti, kart yok" yazar. Bozuk veriyle kart, para riskidir; Levent bir akşam kartsız kalır. Sistem emir vermediği için kayıp küçük (TASARIM §1).

**18-029** — KARAR — Evet, bütünlük kontrolü: gün içinde `HGDG/HG` oranı bir önceki günden >%0,1 sıçrarsa ve o gün olay tablosunda yoksa uyarı listesine yazılır, hisse o gün karantinaya girer. Mevcut tasarım bunu söylemez; TASARIM §5.1 karşılaştırması (HGDG vs kendi düzeltmemiz) zaten bu işi yapar. Ek kod yazma.

**18-030** — KARAR — Fark raporu adaptörün işi değil. Veri deposu iki anlık görüntüyü `pandas.DataFrame.compare` ile karşılaştırır, farklı satır sayısını raporlar. Geçmişte değişen satır varsa yeni anlık görüntü yeni kimlik alır (18-033).

**18-031** — KARAR — Yalnız ayrıştırılmış ham tablo (`HG_*`, `HGDG_*`, olay tablosu tüm alanlarıyla) parquet'e yazılır. Ham JSON saklanmaz: ayrıştırma tam alan listesini koruyorsa gerek yok. Bütün kaynak alanları tabloda tutulur (18-075).

**18-032** — KARAR — Parquet kalır (pyarrow 25.0.1 kurulu, veri.py kullanıyor). Python sürümü sabitlenir (18-089); yükseltme kararını owner değil Claude oturumu verir. Kırılırsa yedek yok; CSV'ye geçmek 1 satır.

**18-033** — KARAR — Kimlik: indirme tarihi + saat (`2026-10-05T1930`), dosya adı. Aynı gün ikinci indirme yeni dosya olur; koşu en yeni dosyayı kullanır ve adını deneme günlüğüne yazar. Hash yok.

**18-034** — KARAR — Hayır, tutarlı sayılmaz. Karar: indirme geçici klasöre (`veri\_gecici`) yazar; hepsi bitince tek `os.replace` ile adı değişir. Yarım klasör bir sonraki koşuda silinir.

**18-035** — YANLIŞ — `veri.py` `fiyat()`: dosya tarihi bugünse indirmez; gün içi yeniden indirmeyi dondurur. Fix: kural "anlık görüntü klasörü yoksa indir"; 19:30 koşusu her gün bir yeni anlık görüntü yazar, aynı gün yeniden koşu için `--yeniden` bayrağı yok, klasörü silmek yeter.

**18-036** — KARAR — Evet, dönebilir (doğrulanmadı). Karar: koşu 19:30'da; Borsa İstanbul seansı 18:00'de biter (kapanış seansı). Son çubuk tarihi bugünse ve saat <18:30 ise kart üretilmez. Yayın saati bilinmiyor (§8.7); ilk haftada gözle kontrol.

**18-037** — KARAR — Evet, diğer 99 devam eder. Hata veren hisse `hatali.csv`'ye (sembol, neden) yazılır; rapor başında "N hisse alınamadı" satırı, liste ek dosyada.

**18-038** — KARAR — `veri\sembol_esleme.csv` (eski, yeni, tarih), elle bakılır; yalnız bir kez gerekirse yazılır. Başlangıç: boş dosya. `.E` ekli kod kullanılmaz (§3.2).

**18-039** — KARAR — Hisse kapanış tarihinden sonrası için boş yanıt "veri yok" sayılır, hata değil. Hisse tarihinde hiç veri yoksa "hata" (hatali.csv). ASYAB dışında örnek bulunmadığı için ilk indirmede kapanmış semboller 5 adet elle sınanır.

**18-040** — KARAR — Sessizce geçer ve saklanır. Bilinmeyen kod yalnız fiyat düzeltmesi dışı bir olay olabilir; çarpan zaten `SHHE_FIYAT_AYAR_OR` ile verilir. Rapor sonunda "bilinmeyen SHT_KODU" listesi yazılır.

**18-041** — OLGU — Doğrulanmadı. Tasarım temettü çarpanını kullanmaz: `HGDG` zaten temettü dahil; olay tablosu yalnız bedelsiz ve bedelli içindir. Karar: nakit temettü (04) çarpanı kullanılmaz; "doğrulanmadı" bayrağına gerek yok.

**18-042** — KARAR — Haftalık. Olay tablosu günlük değişmez; sistem 100 + yeni hisse için pazartesi 19:30 koşusunda yeniler, diğer günler önbellekten okur. Ek: koşu tarihini dosya adına yaz.

**18-043** — KARAR — Doğrulama modülü karar verir, adaptör vermez. İş Yatırım "doğru" sayılır (birincil); fark yalnız listelenir.

**18-044** — KARAR — Önce kesişim: yalnız iki kaynakta da bulunan günler karşılaştırılır. Eksik gün farkı ayrıca sayılır ve raporda "yalnız tek kaynakta bulunan gün sayısı" olarak yazılır. Yahoo satırı bu karşılaştırmaya girmez.

**18-045** — KARAR — Kütüphane yok: KAP için kurulu bir paket yok (pip listesinde `kap` yok). `requests.post(...byCriteria)` 2000 kayıt sınırlı ölçüldü. Kullanım koşulları okunmadı (§8.1). Tek seferlik işte (18-050) risk küçük.

**18-046** — CEVAPLI — `pymupdf` 1.28.2 zaten kurulu; veri-kaynaklari §5 PDF metnini fitz ile çıkardı. Ayrıştırıcı: `page.find_tables()`. Biçim değişimi: her çeyrek için sütun sayısı beklenenle eşit değilse dur (assert).

**18-047** — YANLIŞ — Her çeyrek için doğrulama gerekir; bu adaptörün parçası değil, evren inşasının bir adımı. Fix: geriye doğru uygulanan değişikliklerden çıkan bugünkü liste, bugünkü CSV'ye eşit değilse dur. Ayrı kod gerekmez; tek `assert set(a) == set(b)`.

**18-048** — KARAR — Tarih aralığı çeyrek başına sorgulanır (≤3 ay), bu 2000 sınırının altında kalır. `len(sonuc) >= 2000` ise `raise`. Sessiz kayıp yok.

**18-049** — KARAR — Evet, yedek: elle indirilmiş PDF'ler `veri\kap\*.pdf` klasöründen okunur. Bu zaten pymupdf ile doğrudan yapılabilir ve tek seferlik iş için tek geçerli yol olabilir.

**18-050** — YANLIŞ — Tek seferlik iştir; katman gerekmez. Karar: bir kez çalışır, sonuç `veri\evren_bist100.csv` olarak dondurulur, git'e eklenir (küçük). Bundan sonra güncelleme çeyrekte bir elle.

**18-051** — KARAR — Evren modülü "bilinmiyor" der: 2015–2016 için ara evren (§5.2: piyasa değerine göre en büyük 100) kullanılır ve raporda bu dönem "KAP kapsaması yok" diye işaretlenir. Bugünkü listeyle doldurulmaz.

**18-052** — KARAR — Ortam değişkeni `EVDS_API_KEY` (borsapy de bunu okur, veri-kaynaklari §6). Owner Windows "Ortam Değişkenleri"ne bir kez ekler; Claude oturumu adım adım anlatır. Yoksa yedek yol çalışır (18-055).

**18-053** — KARAR — `.env` kullanılmaz; ortam değişkeni depoda dosya olmadığı için sızmaz. `.gitignore` `.env` içermiyor (doğrulandı), ihtiyaç kalmadı.

**18-054** — KARAR — Anahtar yalnız `headers` içinde gönderilir ve günlüğe yazılmaz. Günlükte URL ve durum kodu var, başlık yok (18-084). Maskeleme katmanı yok.

**18-055** — KARAR — Çalışmaya devam eder: anahtar yoksa borsapy `TCMB().history("policy")` kullanılır (anahtarsız, ölçüldü: 57 satır 2010–2026). Anahtar tasarımda zorunlu değil (18-056).

**18-056** — YANLIŞ — Çelişki var: §4 "borsapy", §5.6 "EVDS ve TLREF". Fix: §5.6 yalnız borsapy politika faizi (basamak, ileri doldurulmuş) kullanır; EVDS ve TLREF ilk sürümde yok. Karşılık: "boştaki nakit" etkisi küçüktür ve politika faizi tek seri sağlar. EVDS anahtarı gerekmez.

**18-057** — KARAR — Kod aranmaz: borsapy `policy` serisi (sütun `lending`, 1 hafta repo; doğrulanmadı ama borsapy öyle tanımlıyor). Gecelik ile 1 hafta repo farkı ayrı ölçülmedi; boştaki nakit için fark küçük kabul edilir ve raporda "yaklaşık" yazılır.

**18-058** — ZAYIF SORU — 18-056 kararıyla iki seri birleştirilmez; tek seri (politika faizi) 2010'dan beri kesintisiz.

**18-059** — KARAR — İleri doldurma simülatörde, tek satır `.reindex(gunler).ffill()`. Seri 2026-01-23'te bitiyor (ölçüm); son tarihten sonraki gün sayısı >60 ise uyarı yaz.

**18-060** — YANLIŞ — Yahoo için adaptör katmanı gerekmez. Fix: sadakat kontrolü için Yahoo açılışı bir kez indirilir (mevcut `veri.py` mantığı, düzeltmesiz), `veri\sadakat\` altına parquet olarak dondurulur; yfinance yalnız o tek betikte çağrılır ve kontrol bitince bağımlılık listesinden çıkar.

**18-061** — KARAR — Yahoo çalışmazsa dondurulmuş dosya kullanılır; yeniden indirme zorunlu değil. Sadakat kontrolü bir kez yapılır (§7 adım 2).

**18-062** — KARAR — Evet, dondurulur: dosya adı `yahoo_YYYYMMDD_yfinance1.7.0.parquet`. Sürüm kurulu paketten alınır (1.7.0 doğrulandı).

**18-063** — KARAR — Ayrı klasör: `veri\sadakat\` (Yahoo) ve `veri\anlik\` (İş Yatırım). Veri deposu yalnız `anlik\` okur; sınama kodu `sadakat\` yolunu bilmez.

**18-064** — YANLIŞ — `veri.py` `temizle` eşikle bedelsiz düzeltiyor (BOSLUK=0.25); TASARIM §4 bunu yasaklıyor (B1). Fix: Yahoo ham halini aynen korur, `temizle` silinir (ve testi). Sadakat için Tansu da düzeltmeyen yfinance `auto_adjust` kullanır; kopya olduğu gibi kalır.

**18-065** — KARAR — Elle yazılmış küçük DataFrame (mevcut test üslubu, `tests\test_nabiz_veri.py`). Cassette ve vcrpy/responses yok.

**18-066** — ZAYIF SORU — Elle yazılmış sahte veriyle gerçek yanıt kaydı depoya girmez; soru doğmaz. Kaydedilmiş yanıt kullanılmaz.

**18-067** — KARAR — Sahte ve gerçek aynı doğrulayıcıdan geçer: `kaynak.py` içindeki `assert`'ler (18-025) her iki çıktıya uygulanır. Sahte bu doğrulayıcıdan geçmek zorunda; ayrı kanıt yok. Ek: bir canlı duman testi (18-068).

**18-068** — KARAR — Evet, bir test: `tests\test_canli.py`, `@pytest.mark.canli`, THYAO için son 10 gün. Elle çalıştırılır (`pytest -m canli`); 19:30 koşusu zaten bu kontrolü yapar (tazelik + şema). Ek zamanlama yok. Başarısızlık rapor başında "veri alınamadı" olarak görünür.

**18-069** — KARAR — Adaptör birim testi. Ağ hatası, 429, bozuk JSON için `unittest.mock.patch("requests.get")` ile 4 küçük test. Uçtan uca yok.

**18-070** — KARAR — `unittest.mock` (stdlib). Yeni bağımlılık sayısı 0 (requests ve pytest kurulu).

**18-071** — KARAR — Yedek yok; borsapy tek başına yetmez (temettüsüz, TradingView). Kayıp halinde dondurulmuş anlık görüntülerle sınama sürer, yeni gün kartı durur ("sınama sürer, canlı kart durur"). Bu cümle TASARIM §6.1'e eklenmeli.

**18-072** — KARAR — Evet, 18-071'deki mod. Anlık görüntüler yeterli, çünkü sınama tarihsel veridir; yalnız canlı kart durur. TASARIM'a yazılmalı (§6.1).

**18-073** — KARAR — Seri kırılması yeni anlık görüntü kimliği ve yeni deneme olarak sayılır (§5.11 deneme günlüğü veri anlık görüntüsünü zaten yazar). Eski ve yeni seri birleştirilmez.

**18-074** — KARAR — Tek fonksiyon, sınıf yok: `fiyat_is(sembol, baslangic, bitis)` ve `fiyat_borsapy(sembol, ...)` aynı sütun adlarını döner. Protocol/ABC gereksiz soyutlamadır.

**18-075** — KARAR — Projenin kendi adları; çeviri `kaynak.py` içinde tek `rename` sözlüğüyle. Ham `HG_*` adları dışarı çıkmaz. GLOSSARY'ye eklenecek (kapanış, aof, yuksek, dusuk, hacim). Mevcut `veri.py` İngilizce (`Open`, `Close`) kullanıyor; tek adlandırma seçilmeli, öneri: İngilizce kalır (aileler.py zaten kullanıyor).

**18-076** — KARAR — UTF-8 yalnız. `requests` `.json()` UTF-8 okur. Hisse kodları ASCII büyük harf (THYAO). Büyük/küçük harf eşlemesi yapılmaz; Türkçe adlar anahtar olarak kullanılmaz.

**18-077** — KARAR — Dosyalar `encoding="utf-8"` ile yazılır (`pathlib.Path.write_text(..., encoding="utf-8")`). `PYTHONUTF8` gerekmez, owner'ın bilmesi gerekmez.

**18-078** — KARAR — Görev Zamanlayıcı: "Kaçırılan görevi mümkün olan en kısa sürede çalıştır" ve "uyandır" seçeneklerini aç. Kaçırılan günün verisi bir sonraki koşuda zaten gelir: İş Yatırım tüm geçmişi 2015'ten döner, ayrı geri doldurma kodu gerekmez.

**18-079** — KARAR — Hayır, `verify=False` önerilmez. Hata mesajı Türkçe tek cümle: "Güvenli bağlantı kurulamadı; antivirüsün HTTPS taramasını kapat." (`truststore` kurulu; gerekirse bir satırla Windows sertifika deposunu kullanır.)

**18-080** — KARAR — borsapy yalnız çapraz kontrol: kontrol ayrı süreçte `subprocess.run(timeout=300)` ile çalışır; takılırsa öldürülür ve "çapraz kontrol yapılmadı" yazılır.

**18-081** — KARAR — Tek `try/except` koşu başında (`kaynak.py` çağıranı); `requests.RequestException` için "İş Yatırım'a ulaşılamadı, bugün kart üretilmedi." yazar. Çeviri katmanı yok, tek sözlük.

**18-082** — KARAR — Üç sınıf: geçici (yeniden dener, 18-014), kalıcı (şema/sütun hatası: dur, 18-028), politika (429 veya boş yanıt kümesi: dur, ertesi gün). Sınıf sayısı 3; kod: iki exception türü (`Gecici`, `Kalici`).

**18-083** — KARAR — stdlib `logging`, tek dosya `veri\tansu.log`, `RotatingFileHandler(maxBytes=1_000_000, backupCount=5)`. Disk dolarsa yazma hatası koşuyu düşürmez (logging varsayılanı).

**18-084** — KARAR — Evet, her istek için tek satır: URL (anahtarsız), durum kodu, süre, bayt. Maliyeti ~300 satır/koşu; yavaşlama ve boyut düşüşü tek yoldan görünür.

**18-085** — KARAR — Ayrı HTTP önbelleği yok. Anlık görüntü deposu önbelleğin kendisidir.

**18-086** — ZAYIF SORU — HTTP önbelleği olmadığı için (18-085) çakışma doğmaz.

**18-087** — KARAR — Sıralı. İlk indirme ~300 istek × 1 sn ≈ 5–10 dk (18-011); hedef <15 dk. Paralellik yok.

**18-088** — KARAR — Evet, basit: geçici klasörde zaten inmiş hisse dosyası varsa atlanır (`yol.exists()`); `veri.py` bunu zaten yapıyor. Tek satır.

**18-089** — KARAR — `pyproject.toml` içine `requires-python = "==3.x"` ve `dependencies` yazılır; tek komut `pip install -e .` (kurulu: pip 26.2.1). uv kullanılmaz (kurulu değil). Owner için `kur.bat` yazılmaz; Claude oturumu kurar.

**18-090** — KARAR — Kilit: `pip freeze > requirements.txt` (hash yok). Güncelleme kararını Claude oturumu verir ve yalnız test geçerse; owner'dan onay istenmez.

**18-091** — KARAR — Tek sınır: `requests.get(..., stream=False)`, yanıt >20 MB ise `raise`. Parser `response.json()`; `eval` yok (borsapy iç kodu okunmadı, çağrıda `eval` aranmadı: doğrulanmadı).

**18-092** — KARAR — Sürüm kilidi (requirements.txt) yeter. Yerel wheel kopyası ve vendoring yok; borsapy yalnız çapraz kontrol olduğundan kaybı sistemi durdurmaz.

**18-093** — KARAR — Hayır, "çalışır" ilan edilmez: TASARIM §8.1 açık kalır ve ilk koşudan önce Levent iki sitenin kullanım koşulunu okur (Claude özet çıkarır). Yasak çıkarsa: İş Yatırım için yedek yok; sınama durur, Levent karar verir.

**18-094** — KARAR — Evet, tek satır: her rapor ve CSV altbilgisi "Kişisel kullanım. Veri İş Yatırım'a aittir; dağıtma." Kod başka bir şey yapmaz.

**18-095** — KARAR — Otomatik: 19:30 koşusundaki şema ve tazelik kontrolü (18-025, 18-028) ilk gün yakalar. Kabul edilebilir gecikme 1 gün.

**18-096** — KARAR — Adaptör: kapanış ≤0 veya NaN ise satırı atmaz, hata fırlatır (şema). AOF veya hacim 0 ise "işlem yok" sayılır, satır tutulur ve veri deposu karantinası (§5.1) kapanış sıçramasına bakar. Ayrım: şema = bozuk veri, karantina = olağandışı fiyat.

**18-097** — YANLIŞ — `veri.py` indirir, temizler, önbellekler ve yazar; tek fonksiyonda dördü. Fix: `kaynak.py` saf (DataFrame döner, diske yazmaz), `veri.py` yalnız anlık görüntü yazıp okur. Test: sahte DataFrame doğrudan `veri.py`'ye verilir.

**18-098** — KARAR — Takvim modülü verir: gün bugünse ve saat 18:30'dan önceyse son çubuk atılır (18-036). İş Yatırım gün içi canlı döndürüp döndürmediği sınanmadı.

**18-099** — KARAR — Claude oturumu onarır. `kaynak.py` tek dosya, <200 satır, fonksiyon başına tek uç nokta; bu yeterince küçüktür. Owner'ın yapacağı iş yok.

**18-100** — KARAR — Sınıflama: İş Yatırım (HisseTekil, olaylar) = birincil. borsapy fiyat = çapraz kontrol. borsapy politika faizi, sektör, kapanmış semboller = tek seferlik/haftalık, dondurulur. KAP = tek seferlik. Yahoo = yalnız sadakat, dondurulur. Her biri için tek "kaybolursa" cümlesi TASARIM §4'e eklenir.

## Özet

Sayımlar (100 soru, grep ile doğrulandı):
- CEVAPLI 3, KARAR 82, YANLIŞ 8, OLGU 3, ZAYIF SORU 4.

En önemli 10 kurulum kararı:
1. Tek dosya `tansu\kaynak.py`; saf fonksiyonlar, diske yazmaz. `veri.py` yalnız anlık görüntüyü yazar/okur (18-001, 18-097).
2. HTTP: `requests` (kurulu); İş Yatırım için kendi 10 satırlık GET; isyatirimhisse kurulmaz (18-002, 18-003).
3. Hız ve hata: `time.sleep(1.0)`, `timeout=(5, 30)`, 3 deneme (5/15/45 sn) yalnız ağ/429/5xx için; koşu üst sınırı 20 dk (18-012–18-016).
4. Şema doğrulaması düz `assert` ile; hata olursa koşu durur, kart üretilmez (18-025, 18-028).
5. `pyproject.toml`'a `dependencies` ve `==` sürümleri + `requirements.txt` kilidi; Python sürümü sabit (18-005, 18-089, 18-090).
6. `veri.py` düzeltmeleri: eşikli `temizle` silinir; aynı gün yeniden indirme dondurma kuralı kalkar; anlık görüntü = tarih+saat adlı klasör, geçici klasör + `os.replace` ile atomik (18-033–18-035, 18-064).
7. Faiz: yalnız borsapy politika faizi (anahtarsız); EVDS ve TLREF ilk sürümde yok; TASARIM §5.6 buna göre düzeltilir (18-056).
8. Yahoo: tek seferlik indir, `veri\sadakat\` altında dondur, ayrı klasör; yfinance sonra bağımlılıktan çıkar (18-060, 18-062, 18-063).
9. KAP: tek seferlik iş, sonuç `veri\evren_bist100.csv` olarak dondurulur; PDF için kurulu pymupdf; yedek: elle indirilmiş PDF klasörü (18-045, 18-049, 18-050).
10. Test: `unittest.mock` ile sahte HTTP, elle yazılmış DataFrame; tek `pytest -m canli` duman testi; log: stdlib `logging` + dönen dosya; TASARIM §6.1'e "kaynak kaybolursa" cümlesi (18-065, 18-068, 18-070, 18-071, 18-083).
