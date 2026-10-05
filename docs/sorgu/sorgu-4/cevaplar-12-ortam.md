# Cevaplar 12: Ortam ve bağımlılıklar

Doğrulananlar (bu oturumda): `.venv` Python 3.14.7, standart yapı (GIL açık, free-threaded değil); `uv` PATH'te yok; `py.exe` ve `C:\Python314` var; LongPathsEnabled = 1; proje `C:\Users\levent\Desktop\TANSU` (OneDrive klasörü `C:\Users\levent\OneDrive` ayrı, Masaüstü onun altında değil); `.gitignore` `.venv/` ve `veri/` içeriyor, `rapor/` içermiyor; `git ls-files` rapor parquet ve md dosyalarını izliyor; `tansu/*.py` yalnız numpy, pandas, pandas_ta_classic, vectorbt, yfinance, borsapy içe aktarıyor; statsmodels, quantstats, duckdb, scipy hiçbir `.py` içinde yok.

**12-001** — CEVAPLI — Hiçbir dosyada yazılı değil (`pyproject.toml` 2 satır). Karar: `[project]` + `requires-python` + doğrudan bağımlılıklar `pyproject.toml`'a yazılır (liste Özet'te).

**12-002** — OLGU — Doğruladım (`pip list`): kodun kullandığı değil; openai, onnxruntime, jiter, pymupdf*, scikit-learn, ipython/jedi, anywidget, tradingview-screener (borsapy getirir) başka işlerin veya dolaylı zincirin kalıntısı. Temiz kurulumda yalnız Özet listesi gerekir; `.venv` silinip yeniden kurulur.

**12-003** — KARAR — Kanıt yok; `pyvenv.cfg` makinedeki `pythoncore-3.14-64` kurulumunu gösteriyor. Karar: 3.14 bilinçli kabul edilir (tüm paketlerin cp314 tekerleği kurulumda çalıştı), `requires-python = ">=3.14,<3.15"`.

**12-004** — OLGU — Doğruladım: numba 0.68.0, llvmlite 0.50.0, pyarrow 25.0.1, duckdb, curl_cffi, lxml bu venv'e kuruldu, yani cp314 win_amd64 tekerlekleri var (tarih: bugün 05.10.2026, komut `pip list`). Numba ve llvmlite zaten çıkacağı için risk kalkar; kalan ikililer: pyarrow, numpy, pandas, scipy.

**12-005** — KARAR — `requires-python` yazılır; yeni PC'de `py -3.14 -m venv .venv` kullanılır. `.python-version` gerekmez (uv yok).

**12-006** — YANLIŞ — Tek gerekçe `tansu/kanit.py` satır 28 `vbt.Portfolio.from_signals`; TASARIM §4 bunu motor olarak reddediyor (AOF dolum kuralı). Düzeltme: vectorbt bağımlılık listesine girmez; ön deneme kodu §7 adım 4'te kendi döngüsüyle değişir.

**12-007** — CEVAPLI — Evet. vectorbt çıkınca numba, llvmlite, plotly, ipywidgets, anywidget, psygnal, jupyterlab_widgets, widgetsnbextension, ipython zinciri düşer. Ölçütler için quantstats da gerekmez (bkz. 12-047).

**12-008** — ZAYIF SORU — vectorbt listeden çıkıyor; uyumluluk kanıtı gereksiz. (Cevap: hayır, ön deneme tüm yolları kanıtlamaz.)

**12-009** — CEVAPLI — vectorbt/numba bırakılırsa sistem pandas + numpy ile ayakta kalır; zaten TASARIM §4 kararı bu.

**12-010** — YANLIŞ — duckdb 1.5.6 kurulu ama hiçbir `.py` içe aktarmıyor ve TASARIM §3 onu erteliyor; artık. Düzeltme: listeye girmez, ortamdan çıkar.

**12-011** — OLGU — Seçim yok; pandas `engine="auto"` önce pyarrow dener (pandas belgesi). Doğruladım: pyarrow 25.0.1 kurulu, fastparquet yok. Karar: pyarrow, tek motor.

**12-012** — KARAR — Parquet kalır. Gerekçe: pyarrow zaten kurulu, `to_parquet` tür ve tarih bilgisini korur (CSV tarih/ondalık tipini kaybeder, 100 dosya × 2.800 satır). Günlük sistem için ağırlık sorun değil. Üzerine yeni kod yazılmaz.

**12-013** — KARAR — Parquet biçimi sürümler arası okunabilir kalır (biçim kararlı, pyarrow geriye uyumlu okur). Ek önlem: anlık görüntü hash'i içerikten alınır (bkz. 12-039); okunamazsa kilit dosyasındaki eski pyarrow ile kurulur.

**12-014** — KARAR — statsmodels kodda henüz yok (grep). Eşbütünleşme (`coint`, ADF) yalnız çift rotasyonu içindir; elle yazmak (Engle-Granger kritik tabloları) yanlış riski taşır. Karar: statsmodels kalır (scipy, patsy, formulaic zinciri kabul); çift ailesi kabul edilmezse çıkar.

**12-015** — OLGU — Doğrulanmadı (kurulu 0.15.0; resmî destek tablosu okunmadı). Karar: `coint` için bir test yazılır (bilinen eşbütünleşik seri → p küçük), her kurulumda pytest koşar.

**12-016** — YANLIŞ — Kodda yalnız `ta.atr` (kanit.py:23); EMA zaten `aileler.ema`. Düzeltme: `pandas-ta-classic` düşer; Wilder ATR `tr.ewm(alpha=1/14, adjust=False).mean()` ile 3 satır, testle sabitlenir.

**12-017** — ZAYIF SORU — Paket düştüğü için fork araştırması gereksiz.

**12-018** — YANLIŞ — Dış paketin varsayılanı sessizce değişirse yakalayan test yok (`tests/test_kanit.py` ATR için altın değer içermiyor). Düzeltme: ATR elle yazılır ve elle hesaplanmış 5 satırlık örnekle test edilir.

**12-019** — KARAR — yfinance üretim bağımlılığı değil. `pyproject.toml` içinde isteğe bağlı `[project.optional-dependencies] sadakat = ["yfinance"]`; yalnız §7 adım 2'de kurulur. `veri.py` Yahoo'lu kodu §7 adım 1'de kalkar.

**12-020** — KARAR — Yahoo engellerse sadakat kontrolü donmuş çıktıyla (12-021) kanıtlanır; tekrar edilmez. curl_cffi zaten yfinance ile yalnız o aşamada kurulur.

**12-021** — KARAR — Evet. Sadakat çalışınca sonuç `docs/sadakat-sonuc.md` (Tansu rakamı, bizim rakam, sürümler, tarih) olarak commit'lenir; ardından yfinance, curl_cffi, multitasking, peewee, frozendict ortamdan çıkar. Bu dosya "kontrol yapıldı" kanıtıdır.

**12-022** — OLGU — Bu oturumda araştırılmadı; TASARIM bu güveni kanıta bağlamıyor (borsapy 0.11.0 yalnız `pip list`te). Karar: borsapy "güvenilir kütüphane" sayılmaz, yalnız çapraz kontrol aracı (bkz. 12-025).

**12-023** — KARAR — borsapy 3 iş için: çapraz kontrol (kaldırılırsa İş Yatırım tek kaynak kalır, kontrol ikinci kaynaksız olur), sektör (alternatif: elle CSV, 100 satır), TCMB faizi (alternatif: elle CSV, yılda ~8 toplantı). Karar: sektör ve faiz elle tutulan 2 küçük CSV; borsapy yalnız çapraz kontrol için opsiyonel ek.

**12-024** — OLGU — Kodu okunmadı; `pip list` tradingview-screener ve websocket-client gösteriyor. Kural: borsapy ana ortamda kurulmaz; ayrı opsiyonel `capraz = ["borsapy"]` içinde, okuma-yazma yetkisi gerektirmeyen ve hesap açılmamış ortamda çalışır.

**12-025** — CEVAPLI — Çelişki yok: §4 borsapy'yi doğruluk kaynağı değil çapraz kontrol sayıyor ve olayları İş Yatırım'dan alıyor; kapanmış sembol listesi için KAP ile birlikte kullanılıyor (TASARIM §5.2). Bulunamayanlar raporda gösteriliyor.

**12-026** — YANLIŞ — Koruma yok (kilit dosyası yok). Düzeltme: sürüm sabitleme (`==`), `pip freeze` ile `requirements.txt`, borsapy opsiyonel ekte.

**12-027** — KARAR — Hash doğrulaması gerekmez: tek kullanıcı, yerel PC, ~15 paket. Yalnız `==` sabitleme.

**12-028** — YANLIŞ — Kilit dosyası yok (doğruladım: `git ls-files`). Düzeltme: `pip freeze > requirements.lock.txt` (tam sürümler) commit'lenir; yeni PC `pip install -r requirements.lock.txt`.

**12-029** — CEVAPLI — Kilit dosyasıyla (12-028) sürüm kayması olmaz; kayma isteğe bağlı yükseltmede altın dosya testiyle (12-042) görülür.

**12-030** — KARAR — Evet. Deneme günlüğü satırına Python, pandas, numpy, scipy, statsmodels sürümleri ve `requirements.lock.txt` hash'i (sha256, hashlib) yazılır.

**12-031** — KARAR — pip + venv. uv kurulu değil (doğruladım), ek Astral bağımlılığı, tek PC. Levent tek komutla çalıştıracak: `.venv\Scripts\python.exe -m tansu ...`.

**12-032** — ZAYIF SORU — uv kullanılmıyor (12-031).

**12-033** — ZAYIF SORU — uv kullanılmıyor; python.org kurulumu kalır.

**12-034** — OLGU — Doğruladım: yol `C:\Users\levent\Desktop\TANSU`, OneDrive kökü `C:\Users\levent\OneDrive`; Masaüstü OneDrive altında değil, `.venv` eşzamanlanmıyor. Yedek için bkz. 12-090.

**12-035** — ZAYIF SORU — Yol bu PC'de `Desktop`; kod göreli yol (`Path(__file__)`) kullanıyor (`veri.py` `Path` kullanır). Mutlak yol yazılmaz.

**12-036** — OLGU — Doğruladım: `.gitignore` var (`.venv/`, `veri/`, `__pycache__/`). `rapor/` yok ve `rapor/islemler-20261005.parquet` + `kanit-20261005.md` izleniyor. Düzeltme: `rapor/` ignore'a eklenir, iki dosya `git rm --cached`.

**12-037** — KARAR — Etkilenen satırlar bu ön denemede: `kanit.py` `pd.to_datetime(...).values` ve `.reindex`, `veri.py` `temizle`. Yakalayan: `tests/test_kanit.py`, `test_nabiz_veri.py` (pandas 3.0.6 ile geçiyor; bu oturumda koşturulmadı). Yeni kod için ek test gerekmez; yeni pandas'ta aynı testler koşar.

**12-038** — KARAR — Hash dosyadan değil içerikten alınır (12-039); çözünürlük farkı hash'i bozmaz. Yazarken tarih sütunu `datetime64[ns]` olarak açıkça çevrilir.

**12-039** — KARAR — İçerikten: `pd.util.hash_pandas_object(df, index=True).values` üzerinde `hashlib.sha256`. Bayt farkı hash'i etkilemez.

**12-040** — YANLIŞ — "Olgun kütüphane" ölçütü yazılı değil. Düzeltme: ölçüt kaldırılır; yerine kilit dosyası + altın dosya testi (12-042) güven sağlar. (Not: sürümler bugün çıkmış olabilir, yaş doğrulanmadı.)

**12-041** — KARAR — Politika: otomatik yükseltme yok. Yalnız güvenlik açığı ya da yeni PC'de tekerlek yoksa yükseltilir; karar Levent'in, uygulama kodlayıcının; altın dosya testi geçmeden kilit dosyası güncellenmez.

**12-042** — KARAR — Yok (`tests/` 3 dosya, altın dosya yok). Karar: `tests/test_altin.py` içinde 1 hissenin sabit girdisinden çıkan işlem tablosu ve ölçütleri küçük bir commit'li CSV ile karşılaştırır.

**12-043** — OLGU — `numpy.random.Generator` + PCG64 akışı sürümler arası garanti değildir (numpy belgesi: yalnız `RandomState` donuk; Generator akışı değişebilir). Doğrulanmadı. Karar: sürüm kilitle, altın dosyaya rastgele kuralın sabit tohumlu bir çıktısını da ekle.

**12-044** — KARAR — Evet: tohum, `numpy.__version__` ve `bit_generator` adı deneme günlüğüne yazılır (12-030 ile aynı satır).

**12-045** — YANLIŞ — quantstats `pip list`te yok ve kodda kullanılmıyor; TASARIM §4 "Ölçütler quantstats'tan" diyor. Düzeltme: quantstats düşer; Sharpe, maks. düşüş, CAGR numpy/pandas ile yazılır (12-047).

**12-046** — ZAYIF SORU — quantstats kurulu değil; yfinance'in kurulu olması `veri.py` `import yfinance` nedeniyle.

**12-047** — YANLIŞ — Evet, ~15 satır; TASARIM'ın "quantstats'tan" cümlesi düzeltilir. Her ölçüt için küçük birim test.

**12-048** — YANLIŞ — Çelişki: §3 hem "Streamlit Kanıt ekranı var" hem "Streamlit kart paneli yok" diyor. Düzeltme: ilk sürümde Streamlit yok; Kanıt ekranı markdown rapor.

**12-049** — CEVAPLI — Haklı değil; Streamlit kurulu değil (doğruladım) ve 12-048 ile çıkar.

**12-050** — KARAR — Streamlit yok. İhtiyaç olursa `rapor/*.md` yeterli; HTML ek iş.

**12-051** — KARAR — Başlatma: `.venv\Scripts\python.exe -m tansu gunluk`. `tansu/__main__.py` kalıcı bileşen olduğundan (gerekli giriş noktası) CLAUDE.md kuralıyla çelişmez; `.bat` yazılmaz.

**12-052** — KARAR — Görev Zamanlayıcı programı `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`, argüman `-m tansu gunluk`, "Başlangıç yeri" proje klasörü. `[project.scripts]` ve uv kullanılmaz.

**12-053** — YANLIŞ — `schedule` kurulu ama kodda yok ve PC kapalıyken çalışmaz. Düzeltme: schedule düşer; Görev Zamanlayıcı "kaçırılırsa en kısa sürede çalıştır" seçeneğiyle; telafi: `gunluk` önceki günkü eksik veriyi de çeker.

**12-054** — KARAR — stdlib `logging`, `rapor/gunluk.log` dosyasına; Hata varsa kart üretilmez (§6) ve `rapor/`'da `HATA-YYYYMMDD.md` oluşur; Levent'in görmesi için rapor dosyasına tek satır durum yazılır.

**12-055** — KARAR — Gerekmez; `requirements.lock.txt` ve internet yeterli. Wheel yedeği için bkz. 12-056.

**12-056** — KARAR — `pip download -r requirements.lock.txt -d wheels\` bir kez alınır, `veri` yedeğiyle (12-090) birlikte harici diske kopyalanır. Git'e girmez.

**12-057** — CEVAPLI — Kalan ikililer (pyarrow, numpy, pandas, scipy) tekerlekle kurulur; kaynaktan derleme gerekmez. lxml, numba, llvmlite, duckdb, curl_cffi listeden çıkar.

**12-058** — ZAYIF SORU — Risk numba/curl_cffi'ye bağlıydı; ikisi de çıkıyor. Kalan ikililer yaygın.

**12-059** — OLGU — Doğruladım: `LongPathsEnabled = 1`.

**12-060** — KARAR — Dosyalar UTF-8. CSV `encoding="utf-8-sig"` (Excel Türkçe karakteri doğru açar), markdown BOM'suz UTF-8. Konsol çıktısı `PYTHONUTF8=1` Görev Zamanlayıcıda; `print` yerine dosyaya yaz.

**12-061** — YANLIŞ — Bkz. 12-036: izleniyorlar. Düzeltme: iki dosya silinir/izlenmez, `rapor/` ignore.

**12-062** — KARAR — Düz düzen: `tansu/` kökte, `pythonpath = ["."]` kalır (mevcut, test geçiyor). `src/` yok.

**12-063** — KARAR — Kurulabilir paket yok: `[build-system]` yazılmaz, `pip install -e .` gerekmez; `-m tansu` proje klasöründen çalışır. Sadece `[project]` meta ve bağımlılıklar.

**12-064** — KARAR — Tek paket `tansu`, alt modüller. Ayrı dağıtım yok.

**12-065** — KARAR — Çalışma zamanı: pyproject `dependencies`; geliştirme: `[project.optional-dependencies] dev = ["pytest"]`. Levent'in makinesinde pytest de kurulu kalır (tek paket).

**12-066** — KARAR — Yalnız pytest. mypy, ruff, pre-commit yok (YAGNI; tek geliştirici ajan).

**12-067** — KARAR — Yalnız pytest + stdlib; hypothesis, pytest-cov yok.

**12-068** — KARAR — Hook yok; ajan her değişiklikten sonra `.venv\Scripts\python.exe -m pytest` koşar (AGENTS.md'ye tek satır).

**12-069** — OLGU — Kayıt yok; sadakat adımı (§7-2) henüz yapılmadı (doğruladım: docs'ta sonuç dosyası yok). Karar: sürümler 12-021'deki dosyaya yazılır.

**12-070** — KARAR — Göstergeler kodda tanımlanır (12-016 ile `pandas-ta-classic` çıkar); dış paket kalmayınca kural hash'i tanımı kapsar.

**12-071** — KARAR — Kod hash'i proje kodu + `requirements.lock.txt` sha256'sını kapsar; sessiz yükseltme hash'i değiştirir.

**12-072** — CEVAPLI — Evet, çıkarılır (12-021 ile aynı adım); Özet'te listeden düşer.

**12-073** — KARAR — Kural: pyproject'e yeni paket ancak `docs/BAGIMLILIK.md`'e tek satır gerekçe ("stdlib/mevcut şu yüzden yetmez") ile girer. Kısa tablo dosyası, yeni dosya gerektirir; alternatif: pyproject yorum satırı (tercih).

**12-074** — KARAR — `requests` (kurulu, borsapy'nin de dolaylı bağı). httpx, httpx2, httpcore2, curl_cffi çıkar.

**12-075** — KARAR — İnce istemci `tansu/veri.py` içinde; testi kayıtlı yanıt (committe tutulan 2 JSON örneği) ile; ağ yok. VCR paketi gerekmez.

**12-076** — KARAR — Durur: elle kontrol (beklenen anahtarlar ve tür) → eksikse `ValueError`. pydantic gerekmez (bkz. 12-098).

**12-077** — KARAR — stdlib: `requests` `timeout=30`, 3 deneme `for` döngüsü, `time.sleep`. tenacity ve requests-cache yok; önbellek zaten `veri/*.parquet`.

**12-078** — KARAR — `requests` varsayılan `certifi` kullanır. Antivirüs araya girerse hata `SSLError` görünür; ek: `truststore.inject_into_ssl()` yalnız sorun çıkarsa. truststore kuruludur ama listeye girmez.

**12-079** — KARAR — BIST takvimi elle: `veri/takvim.csv` (bayram tatilleri ve yarım günler), Takvim modülü okur. `pandas-market-calendars` / `exchange_calendars` BIST yarım gün desteğini doğrulamadım; ek paket yok.

**12-080** — KARAR — `tzdata` pyproject'e açıkça yazılır (Windows'ta zorunlu, `zoneinfo` için).

**12-081** — OLGU — Doğruladım: `pip list` 100+ paket; doğrudan kullanılan 6 (numpy, pandas, pandas_ta_classic, vectorbt, yfinance, borsapy). Çıkarmalardan sonra dolaylı küme: numpy, pandas, pyarrow, scipy, statsmodels (+patsy, formulaic), requests (+urllib3, idna, certifi), pytest, tzdata.

**12-082** — KARAR — Yok. Tek kullanıcı, yerel PC; `pip-audit` ayda bir elle çalıştırılır (kurulu değil, kurulmaz). Levent'e bildirim yok.

**12-083** — ZAYIF SORU — vectorbt ve pymupdf Tansu'dan çıkıyor; kalan paketler BSD/MIT/Apache.

**12-084** — CEVAPLI — Evet; Tansu bağımlılığı değil, yeni temiz `.venv` kurulumunda yer almaz.

**12-085** — OLGU — Doğruladım: `.venv` içinde openai, onnxruntime, jiter var, kodda yok. Karar: Tansu `.venv` yalnız Tansu içindir; diğerleri temiz kurulumda gelmez (12-002).

**12-086** — OLGU — Doğruladım: `py.exe`, `C:\Python314\python.exe` ve `AppData\Local\Python\pythoncore-3.14-64` var. Karar: her zaman tam yol `.venv\Scripts\python.exe` kullanılır; "yanlış yorumlayıcı" riski ortadan kalkar.

**12-087** — KARAR — Evet; Activate.ps1 kullanılmaz, belgede yalnız `.venv\Scripts\python.exe -m ...`.

**12-088** — KARAR — 5 adım: 1) Python 3.14 kur. 2) Depoyu kopyala. 3) `py -3.14 -m venv .venv`. 4) `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt`. 5) `veri/` yedeğini kopyala. Belge: `AGENTS.md` içinde.

**12-089** — KARAR — Yedekten kopyala (geçmiş değişmiş olabilir); `veri/` ve anlık görüntüler harici diske.

**12-090** — KARAR — Harici disk, haftada bir elle kopyalama (`veri/`, `rapor/`, deneme günlüğü, `wheels/`). OneDrive ve git-lfs yok.

**12-091** — OLGU — Doğruladım: standart (`Py_GIL_DISABLED` = 0). Numba'ya bağımlılık yok (12-092). Süre için 12-093.

**12-092** — YANLIŞ — numba yalnız vectorbt'nin dolaylı bağıdır; açık seçilmez, vectorbt ile düşer.

**12-093** — OLGU — Ölçülmedi. Tahmin: 1.000 × 100 hisse × ~2.800 gün saf numpy dizisinde (işlem başına vektörleştirme) dakikalar mertebesinde; belirsiz. Karar: önce kendi döngü + numpy vektör; ölçüm §7 adım 4'te; yetmezse tek ek `multiprocessing` (stdlib), numba/polars/joblib eklenmez.

**12-094** — KARAR — pandas 3 kalır (mevcut kod, 3 test). polars geçişi yeniden yazma maliyeti; gerekçe pyproject yorumuna.

**12-095** — KARAR — scipy kalır (statsmodels bağımlılığı ve p değeri/bootstrap için `scipy.stats`). scikit-learn, joblib, threadpoolctl hiç kullanılmıyor (grep) ve çıkar.

**12-096** — KARAR — matplotlib yok (kurulumda gelmez); ilk raporda grafik yok, sermaye eğrisi gerekirse markdown tablo. Eklenirse tek paket olarak gerekçelendirilir.

**12-097** — KARAR — Sabitler `tansu/ayar.py` içinde Python sabiti (masraf, 10 pozisyon, 1.000.000 TL). TOML/YAML dosyası yok; PyYAML, pydantic-settings gerekmez.

**12-098** — KARAR — `dataclass(frozen=True)` yeter (aileler.py kullanıyor); pydantic yok.

**12-099** — KARAR — Evet: rapor başlığında Python, pandas, numpy, scipy, statsmodels sürümü ve `requirements.lock.txt` sha256 (12-030).

**12-100** — KARAR — Tek komut: `.venv\Scripts\python.exe -m pytest` (altın dosya testi + `coint` testi + ATR testi içe aktarmaları ve sayıları doğrular). Sadakat rakamları ayrı bir kez yapılan sonuç dosyasıdır (12-021).

## Özet

Sayımlar (100 soru): CEVAPLI 9 · KARAR 54 · YANLIŞ 13 · OLGU 16 · ZAYIF SORU 8.

Son bağımlılık listesi.
1. Tut: `pandas`, `numpy`, `pyarrow` (parquet), `scipy`, `statsmodels` (yalnız `coint`; çift ailesi kabul edilmezse çıkar).
2. Tut: `requests` (İş Yatırım), `tzdata` (Windows), `pytest` (dev).
3. Opsiyonel ek, kalıcı değil: `yfinance` (+ curl_cffi) yalnız sadakat için, sonra çıkar; `borsapy` yalnız çapraz kontrol için.
4. Bırak: `vectorbt`, `numba`, `llvmlite`, `plotly`, `ipywidgets`, `anywidget`, `ipython`.
5. Bırak: `pandas-ta-classic`, `quantstats` (kurulu değil), `duckdb`, `streamlit` (kurulu değil), `schedule`, `matplotlib`.
6. Bırak: `scikit-learn`, `joblib`, `pydantic`, `PyYAML`, `httpx`, `httpx2`, `openai`, `onnxruntime`, `pymupdf*`, `tradingview-screener`.

En önemli 10 madde.
1. 12-006/12-007/12-092: vectorbt (ve numba zinciri) listeden çıkar; motor kendi döngüsü.
2. 12-028/12-026: `requirements.lock.txt` (pip freeze) yok, eklenir; hash zorunlu değil (12-027).
3. 12-001: `pyproject.toml` `[project]`, `requires-python = ">=3.14,<3.15"`, doğrudan bağımlılıklar yazılır; `[build-system]` yok (12-063).
4. 12-016/12-018: `pandas-ta-classic` çıkar, ATR elle ve testle.
5. 12-045/12-047/12-048: quantstats ve Streamlit ilk sürümde yok; TASARIM §3 ve §4 düzeltilir.
6. 12-036/12-061: `rapor/` ignore'a girer, izlenen iki ön deneme dosyası çıkar.
7. 12-039/12-071: anlık görüntü hash'i içerikten, kural hash'i kilit dosyasını da kapsar.
8. 12-042/12-100: altın dosya testi + tek komut kabul testi (pytest).
9. 12-052/12-053: Görev Zamanlayıcı `.venv\Scripts\python.exe -m tansu gunluk`; `schedule` çıkar; kaçırılan günü telafi eder.
10. 12-019/12-021/12-072: yfinance yalnız sadakat için, sonuç dosyası dondurulur, sonra paket ve zinciri çıkar.
