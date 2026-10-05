# Sorular 12: Ortam ve bağımlılıklar

12-001. `pyproject.toml` yalnız `[tool.pytest.ini_options]` içeriyor; `[project]` tablosu, `requires-python` ve bağımlılık listesi yok. Sistemin hangi paketlere dayandığı şu an hangi dosyada yazılı?

12-002. `.venv` içinde `pip list` çıktısı openai, onnxruntime, pymupdf, pymupdf4llm, scikit-learn, ipython, ipywidgets, anywidget, tradingview-screener gibi TASARIM.md'de hiç geçmeyen paketler gösteriyor. Bu ortam hangi işlerden kirlendi ve temiz bir kurulumda hangileri gerçekten gerekir?

12-003. `.venv` Python 3.14.7 ile kurulmuş (`pyvenv.cfg`). 3.14 seçimi bilinçli bir karar mı, yoksa makinede o sürüm kurulu olduğu için mi oldu?

12-004. Python 3.14'ün en yeni sürüm olması, numba ve llvmlite için tekerlek (wheel) gecikmesi riski doğurur. Her bağımlılığın cp314 win_amd64 tekerleği var mı ve bu hangi tarihte, hangi komutla doğrulandı?

12-005. Python sürümü hiçbir yerde sabitlenmemiş (`.python-version`, `requires-python` yok). Levent'in PC'si değişirse ya da Windows'ta yeni bir Python kurulursa hangi sürüm kullanılacak?

12-006. TASARIM.md §4 "vectorbt kararı: motor olarak kullanılmaz" diyor, ama `tansu/kanit.py` hâlâ `import vectorbt as vbt` yapıyor. Vectorbt'nin bağımlılık listesine girmesi için bugün tek gerekçe ne?

12-007. Vectorbt motor olmayacaksa numba, llvmlite, plotly, ipywidgets gibi ağır zincirleri de getiriyor. Ölçütler için yalnız quantstats kalırsa bu zincirin tamamı kurulumdan çıkarılabilir mi?

12-008. vectorbt 1.1.1 sürümünün numpy 2.5 ve pandas 3.0 ile uyumlu olduğuna dair kanıt nerede? Ön denemenin çalışmış olması, bütün çağrı yollarının çalıştığını gösterir mi?

12-009. vectorbt ve numba'nın bakımı yavaşlarsa ya da Python 3.15 çıktığında tekerlek gelmezse, sistem hangi bağımlılığı bırakarak ayakta kalır?

12-010. TASARIM.md §3 DuckDB'yi "gereksiz katman, ilk aile kabul edilene kadar bekler" diye listeliyor, ama `.venv` içinde duckdb 1.5.6 kurulu. Kurulu olması bir karar mı, yoksa artık mı?

12-011. Veri `veri/*.parquet` dosyalarında tutuluyor. Parquet okuma-yazma için pyarrow ile fastparquet arasında seçim yapıldı mı ve pandas 3.x hangisini varsayılan sayıyor?

12-012. Bu proje için gerçekten Parquet gerekli mi? Günde birkaç yüz satır olan günlük fiyat verisi için CSV ya da SQLite stdlib ile çalışırsa pyarrow (yüzlerce MB tekerlek) neden gerekli?

12-013. Anlık görüntüler (TASARIM.md §4 "tarihli, değişmez") pyarrow sürümüne bağlı bir dosya biçiminde saklanırsa, pyarrow ana sürümü değiştiğinde eski anlık görüntüler okunabilir kalır mı?

12-014. statsmodels 0.15.0 yalnız eşbütünleşme (`coint`) ve belki ADF için mi kullanılıyor? Bu tek işlev için scipy, patsy, formulaic zincirini getirmek yerine başka bir yol değerlendirildi mi?

12-015. statsmodels'in pandas 3.x ve numpy 2.5 ile uyumu hangi sürümden itibaren resmî olarak destekleniyor? Hangi test bunu her kurulumda doğruluyor?

12-016. `pandas-ta-classic` ATR için kullanılıyor (`tansu/kanit.py`, `ta.atr`). Kullanılan göstergeler ATR, EMA, SMA250 ise, bunlar pandas'ta birkaç satırdır. Bu paketin supply-chain riski bu kazancı karşılar mı?

12-017. `pandas-ta-classic` çatallanmış (fork) bir proje. Asıl `pandas-ta` projesinin durumu, çatalın sahibi, bakım geçmişi ve PyPI yayın geçmişi araştırıldı mı?

12-018. Wilder ATR'si ile pandas-ta-classic ATR'sinin varsayılan yumuşatma yöntemi (RMA, SMA, EMA) aynı olmayabilir. Sürüm yükseltmesinde varsayılan davranış değişirse sadakat kontrolü bunu yakalar mı?

12-019. `yfinance` TASARIM.md §4 "Yahoo kullanılmaz" derken §7'de sadakat kontrolü için Yahoo verisi kullanılacağını söylüyor. yfinance bağımlılığı üretim paketinde mi, yoksa yalnız bir kez koşan sadakat kontrolünde mi duracak?

12-020. yfinance 1.7.0 curl_cffi'ye dayanıyor (pip list'te curl_cffi 0.16.3). Bu Windows'ta ikili tekerlek ve tarayıcı taklidi gerektiriyor; Yahoo bir gün engellerse sadakat kontrolü nasıl tekrarlanacak?

12-021. Sadakat kontrolü bir kez yapılıp biterse, yfinance'i her kurulumda tutmak yerine kontrol sonucunu dondurup paketi kaldırmak mümkün mü? Hangi kanıt dosyası "kontrol yapıldı" der?

12-022. borsapy 0.11.0 küçük ve tek bakımcılı görünüyor. PyPI sayfası, yayın geçmişi, kaynak deposu, indirme sayısı ve sahibi incelendi mi? TASARIM.md bu güveni hangi kanıta dayandırıyor?

12-023. borsapy yalnız "çapraz kontrol" ve sektör ile TCMB faiz verisi için kullanılıyor (TASARIM.md §4, §5.1, §5.6). Bu üç iş için borsapy kaldırılırsa geriye ne kalır ve her biri için başka kaynak var mı?

12-024. borsapy TradingView'dan veri çekiyor ve `tradingview-screener` ile websocket-client kurulu. Bu paket gizli kimlik, çerez ya da oturum belirteci okuyor mu? Kodu hiç okundu mu?

12-025. borsapy "78 kodu atıyor" (TASARIM.md §4). Böyle bir kütüphane, kapanmış semboller listesi için (§5.2) güvenilir sayılıyor. Hatalı davrandığı kanıtlanmış bir paketin çıktısı neden doğrulama aracı olarak yeterince güvenilir?

12-026. borsapy bir gün PyPI'dan kalkarsa, sahipliği devredilirse ya da kötü niyetli bir sürüm yayınlanırsa, kurulum hangi mekanizmayla bundan korunuyor?

12-027. Küçük paketler için "sürüm sabitleme" yeterli mi, yoksa içerik karması (hash) doğrulaması da gerekli mi? `uv.lock` ya da `pip --require-hashes` kullanılacak mı?

12-028. Depoda hiçbir kilit dosyası yok (`uv.lock`, `requirements.txt`, `poetry.lock`, `pdm.lock` yok). Yeni bir PC'de aynı sürümler nasıl kurulacak?

12-029. Kilit dosyası olmadan, 2026 sonunda `pip install` çalıştıran biri pandas 3.0.6 yerine pandas 3.1 ya da 4.0 alırsa, sınama sonuçlarının sürümler arası aynı olduğu nasıl gösterilecek?

12-030. TASARIM.md §5.11 deneme günlüğü "veri anlık görüntüsü, kod hash" kaydediyor. Paket sürümleri (lock dosyası hash'i, Python sürümü) deneme kaydına girmeli mi, yoksa sürüm değişimi sonucu etkilerse fark edilmeyecek mi?

12-031. uv, pip + venv ve poetry/pdm seçeneklerinden hangisi bu proje için seçildi? Levent teknik değil; `uv` komutları (`uv sync`, `uv run`) onun için pip'ten daha mı basit, daha mı karmaşık?

12-032. uv Windows'ta tek bir yürütülebilir dosya olarak kuruluyor. Bu yeni bir güven bağımlılığı (Astral); uv'nin kendisinin kurulumu ve güncellemesi nasıl doğrulanacak?

12-033. uv kullanılırsa Python'un kendisini de uv indirir (python-build-standalone). Mevcut `AppData\Local\Python\pythoncore-3.14-64` kurulumu (python.org/Windows Store yöneticisi) ile çakışma ya da ikilik riski var mı?

12-034. `.venv` klasörü proje klasörünün içinde ve Masaüstü'nde (`Desktop\TANSU`). Masaüstü OneDrive ile eşzamanlanıyorsa, on binlerce dosyalı `.venv` bulut eşzamanlamasına girer mi ve bu kurulumu bozar mı?

12-035. Proje Masaüstü'nde olduğu için yol "Desktop" altında; Türkçe Windows'ta Masaüstü bazen "Masaüstü" olarak yerelleşir ve OneDrive altında olabilir. Kod ve komut dosyaları bu yola mı bağımlı olacak?

12-036. Depoda `.gitignore` var mı? `.venv`, `veri/*.parquet` ve `rapor/` dosyalarının Git'e girip girmediği kontrol edildi mi? "nothing to commit, working tree clean" görünüyor ama bu, 100 parquet dosyasının izlendiği anlamına da gelebilir.

12-037. pandas 3.x'in kırıcı değişiklikleri (varsayılan string dtype, Copy-on-Write, `inplace` ve zincirleme atama kalkışı, `datetime64` çözünürlük varsayılanı) bu projede hangi kod satırlarını etkiliyor? Hangi test bunu yakalıyor?

12-038. pandas 3.x'te varsayılan datetime çözünürlüğü değişti (ns yerine us/ms olabilir). Parquet'e yazılan tarih sütunlarının çözünürlüğü, önceki ve sonraki sürümler arasında anlık görüntü karşılaştırmasını (hash) bozar mı?

12-039. Anlık görüntü "değişmez" ve hash'lenecek (TASARIM.md §4). Aynı veri farklı pyarrow ya da pandas sürümünde yazılınca baytlar değişirse, hash dosyadan mı yoksa veri içeriğinden mi hesaplanacak?

12-040. Kütüphane sürümleri 05.10.2026 tarihli görünüyor (numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2). Bu sürümlerin hiçbiri bir yıldan eski değil; "güvenilir, olgun kütüphane" ölçütü hangi yaş ve hangi kanıtla sağlanıyor?

12-041. Yükseltme politikası yazılı değil. Ne sıklıkla (aylık, yıllık, hiç) ve hangi koşulda (güvenlik açığı, tekerlek çıkışı, yeni Python) bir paket yükseltilecek ve kim karar verecek?

12-042. Bir bağımlılık yükseltmesinden sonra, geçmiş sınama sonuçlarının aynı çıktığını gösteren bir "altın dosya" (golden) testi var mı? Yoksa her yükseltme bütün kabul kararlarını sessizce değiştirebilir mi?

12-043. TASARIM.md §5.9 ve §5.7 rastgele kural için en az 1.000 tekrar istiyor. Bu rastgele sayı üretimi numpy `Generator` ve PCG64'e bağlı; numpy sürümü değişince aynı tohumla aynı sonuç çıkması garanti mi?

12-044. Rastgele tohum ve sayı üreteci sürümü, deneme günlüğüne (§5.11) yazılıyor mu? Sonuçların yeniden üretilebilir olması için hangi bileşen sürümü sabit olmalı?

12-045. quantstats'ın pandas 3.x, numpy 2.5 ve Python 3.14 ile uyumu doğrulandı mı? quantstats yıllardır pandas'ın eski sürümlerine yama yapan bir paket olarak biliniyor; bu proje için hangi işlevleri (Sharpe, düşüş, yıllık getiri) kullanıyor?

12-046. quantstats matplotlib, seaborn, yfinance (kendisi de bağımlılık) ve tabulate zincirini getirir. Bu, yfinance'in "kullanılmaz" kararına rağmen kurulumda kalmasının gerçek nedeni olabilir mi?

12-047. quantstats'ın getirdiği ölçütler (Sharpe, maksimum düşüş, CAGR) numpy ve pandas ile 20 satırda yazılabilir. Güvenilir kütüphane tercihi ile gereksiz bağımlılık yükü arasında bu paket için denge nerede?

12-048. Streamlit, TASARIM.md §3'e göre "tek sayfalık Kanıt ekranı" için ilk sürümde var, ama §3'ün ikinci paragrafı "Streamlit kart paneli" erteleniyor diyor. Hangisi doğru: ilk sürümde Streamlit var mı yok mu?

12-049. `pip list` içinde streamlit yok. İlk sürümde bir ekran gerekiyorsa, Streamlit'in getirdiği zincir (tornado, altair, pydeck, protobuf, pyarrow) markdown rapor ve CSV varken neden haklı?

12-050. Streamlit yerel bir web sunucusu açar. Windows güvenlik duvarı uyarısı, port çakışması ve "tarayıcıda localhost" Levent için kabul edilebilir mi? Rapor tarayıcıda açılan statik bir HTML ile de gösterilebilir mi?

12-051. Streamlit'i Levent nasıl başlatacak: komut satırı, masaüstü kısayolu, çift tıklanan `.bat` dosyası? Bu giriş noktası depoda nerede tanımlı olacak ve CLAUDE.md "script dosyası yaratma" kuralıyla çelişir mi?

12-052. `[project.scripts]` ile tanımlanan bir komut (`tansu gunluk`) yerine, 19:30 görevi (TASARIM.md §6) hangi giriş noktasını çağıracak? Windows Görev Zamanlayıcı hangi Python yoluyla çalışacak: `.venv\Scripts\python.exe` mı, `uv run` mı?

12-053. `schedule` paketi kurulu (schedule 1.2.2). Günlük 19:30 işi için Windows Görev Zamanlayıcı yerine bir Python döngüsü mü kullanılacak? PC kapalıysa ya da uykudaysa kaçırılan gün nasıl telafi edilecek?

12-054. Günlük işleyiş başarısız olursa (ağ kesintisi, paket hatası) Levent bunu nasıl fark eder? Hata günlüğü hangi paketle yazılacak: stdlib `logging` yeterli mi?

12-055. Paket kurulumu internet ister. Yeni PC'de veya internet yokken yeniden kurulum gerekiyorsa, tekerlek önbelleği ya da yerel bir ayna tutulacak mı?

12-056. PyPI'dan bir paket silinir (yanking) ya da yazar hesabını kapatırsa, 2027'de aynı kilit dosyası ile kurulum çalışmaz. Kurulan tekerlekleri yedekleyen bir yöntem var mı?

12-057. `curl_cffi`, `lxml`, `numba`, `llvmlite`, `pyarrow`, `duckdb` derlenmiş ikili paketler içeriyor. Windows'ta Visual C++ Build Tools yoksa kaynak koddan derleme gerekirse (tekerlek yok), Levent bunu çözebilir mi?

12-058. Windows Defender ya da kurumsal yazılımlar, numba'nın ya da curl_cffi'nin ikili dosyalarını yanlış pozitifle engelleyebilir. Böyle bir durumda hangi hata görünür ve hata Levent için okunabilir mi?

12-059. Windows'ta uzun yol sınırı (260 karakter) `Desktop\TANSU\.venv\Lib\site-packages\...` yollarında sorun yaratabilir. LongPathsEnabled kontrol edildi mi?

12-060. `veri/*.parquet` Türkçe karakter içermiyor, ama rapor ve CSV Türkçe karakter içerecek. CSV ve markdown dosyalarında UTF-8 (BOM'lu ya da BOM'suz), Excel'de açılış ve Windows konsolunun cp1254/cp857 kodlaması nasıl ele alınacak?

12-061. `rapor/kanit-20261005.md` ve parquet ön deneme çıktıları depoda duruyor. TASARIM.md "kanıt değildir" diyor. Bu dosyalar silinecek mi, yoksa yeni ortamda yanlışlıkla kullanılabilir mi?

12-062. Ön deneme kodu (`tansu/*.py`) "büyük ölçüde değiştirilecek". Paket adı `tansu` ve `src/` düzeni kullanılacak mı, yoksa `pythonpath = ["."]` ile düz düzen mi? Bu seçim `pip install -e .` ve test içe aktarmasını nasıl etkiliyor?

12-063. `pythonpath = ["."]` pytest ayarı paket kurulumunu atlıyor. Yeni PC'de `uv sync` sonrası `tansu` paketinin içe aktarılabilir olması için yapı sistemi (build backend: hatchling, setuptools, uv_build) seçildi mi?

12-064. Modüler yapı (TASARIM.md §4: Veri deposu, Takvim, Evren, Motor, Simülatör...) tek paket içinde alt modüller mi, yoksa ayrı dağıtım paketleri mi olacak? "Minimum altyapı" ile bu seçim nasıl uyumlu?

12-065. Hangi bağımlılıklar çalışma zamanı, hangileri geliştirme (pytest, ruff, mypy) olacak? Levent geliştirici olmadığı için günlük kurulumda geliştirme paketleri yüklü olmalı mı?

12-066. Tip denetimi (mypy, pyright) ve biçimlendirme (ruff) kullanılacak mı? "Sağlam temel" isteniyor ama her araç yeni bir bağımlılık ve bakım yükü; hangisi minimum sette?

12-067. pytest 9.1.1 kurulu. Testlerde hypothesis ya da pytest-cov gibi ek paketler gerekecek mi, yoksa yalnız pytest ve stdlib `unittest.mock` yeterli mi?

12-068. CI yok (uzak depo yok, AGENTS.md "yerel markdown"). Testlerin her değişiklikten sonra otomatik koşması için pre-commit ya da yerel bir komut tanımlı mı? Levent kod değiştirmiyorsa, testleri kim koşturacak?

12-069. Sadakat kontrolü (KURALLAR.md §4) Tansu'nun rakamlarını yeniden üretiyor. Bu rakamlar numpy, statsmodels ve pandas-ta-classic sürümüne duyarlıysa, kontrol hangi sürümlerle yapıldı ve nerede kayıtlı?

12-070. KURALLAR.md'deki göstergelerin (EMA, SMA, ATR, z-skoru) tanımları kod içinde mi, yoksa pandas-ta-classic içinde mi yaşıyor? Dış paket tanımı değiştirirse kural kaydının hash'i (§5.8) bunu görür mü?

12-071. Kural kaydının "kod hash'i" yalnız proje kodunu mu kapsıyor, yoksa bağımlılık sürümlerini de? Bağımlılık sürümü kural parçası sayılmazsa, sessiz bir yükseltme kayıtlı kuralı değiştirmiş olur mu?

12-072. TASARIM.md §7 adım 1: "Yahoo'lu ön deneme kodu kaldırılır". Kaldırıldıktan sonra `yfinance` paketi, `multitasking`, `curl_cffi`, `peewee`, `frozendict` gibi zinciriyle birlikte ortamdan da çıkarılacak mı, yoksa kalıntı olarak mı kalacak?

12-073. Bağımlılık eklemenin ve çıkarmanın kuralı ne? Her yeni paket için "neden stdlib ya da mevcut paket yetmiyor" gerekçesi bir yere yazılıyor mu?

12-074. HTTP istekleri için requests, httpx ve curl_cffi'nin üçü de kurulu (httpx ve httpx2, httpcore ve httpcore2 dahil). İş Yatırım istemcisi hangisini kullanacak ve neden bir tane yeterli değil?

12-075. İş Yatırım `HisseTekil` ve `GetSermayeArttirimlari` için resmî bir paket yok; kendi ince istemcimiz yazılacak. Bu istemci bir "güvenilir kütüphane" değil; sorumluluğu ve testi nasıl kapsanacak (kayıtlı yanıt, VCR benzeri)?

12-076. İş Yatırım uç noktaları belgesiz. Yanıt biçimi değişirse sistem sessizce yanlış veri mi okur yoksa durur mu? Şema doğrulaması için pydantic (kurulu, 2.13.5) gerekli mi, yoksa elle kontrol yeterli mi?

12-077. Ağ isteklerinin yeniden deneme, zaman aşımı ve hız sınırı davranışı için tenacity gibi bir paket mi, yoksa stdlib mi? TASARIM.md "az sayıda istek, yerel önbellek" diyor; önbellek için requests-cache gibi bir paket de gerekir mi?

12-078. TLS sertifika doğrulaması: `certifi` ve `truststore` kurulu. Kurumsal proxy ya da antivirüs HTTPS'i araya girerse (Windows'ta sık) istemci hangi sertifika deposunu kullanacak?

12-079. Saat dilimi ve takvim: `tzdata`, `pytz`, `tzlocal`, `dateparser` kurulu. BIST takvimi için `pandas-market-calendars` ya da `exchange_calendars` düşünüldü mü, yoksa bayram günleri elle mi tutulacak? Bu paketlerden biri BIST yarım günlerini destekliyor mu?

12-080. Windows'ta `tzdata` paketi zorunlu (IANA veritabanı yok). Bu bağımlılık açık biçimde `pyproject.toml`'a yazılacak mı, yoksa başka bir paketin getirmesine mi güvenilecek?

12-081. Dolaylı (transitive) bağımlılıklara güvenmek: pyproject'e yalnız doğrudan bağımlılıklar yazılırsa, `pip list`'te görünen 100'den fazla paketten kaçı gerçekten kullanılıyor? Kullanılmayan dolaylı paketler denetlenebiliyor mu?

12-082. Bilinen güvenlik açıkları için `pip-audit` ya da `uv audit` benzeri bir tarama yapılacak mı? Levent teknik olmadığı için bu bildirim nasıl ve ne sıklıkla ona ulaşacak?

12-083. Lisans denetimi: kullanılan paketlerin lisansları (özellikle vectorbt'nin "Commons Clause" ile kısıtlı Apache 2.0 lisansı, pymupdf'in AGPL lisansı) kişisel kullanım için sorun mu? Ticari ya da paylaşım olursa durum değişir mi?

12-084. pymupdf ve pymupdf4llm (AGPL) ortamda kurulu; muhtemelen not işleme için. Bunlar Tansu projesinin bağımlılığı değilse, ayrı bir ortama taşınması mı gerekir?

12-085. Proje başına bir ortam mı, yoksa Levent'in bütün araçları için ortak bir ortam mı? `.venv` içindeki openai, onnxruntime, jiter gibi paketler başka bir işin (beyin, CEVDET) kalıntısı olabilir; ortamlar ayrılmış mı?

12-086. Birden fazla Python kurulumu (python.org, Microsoft Store, `py` başlatıcı, uv) aynı PC'de olabilir. Hangisinin `python` komutuna bağlandığını Levent nasıl bilecek ve yanlış yorumlayıcı çalışırsa hata nasıl görünür?

12-087. PowerShell yürütme ilkesi (`Set-ExecutionPolicy`) `.venv\Scripts\Activate.ps1` çalıştırmayı engelleyebilir. Ortamı etkinleştirmeden çalıştırma (`.venv\Scripts\python.exe -m ...` ya da `uv run`) belgelenecek mi?

12-088. Yeni PC'de kurulum belgesi kaç adım? "Python kur, uv kur, depoyu klonla, `uv sync`, veriyi kopyala" gibi bir liste var mı ve Levent bunu tek başına, ASD-STE100 sade dilde uygulayabilir mi?

12-089. Veri klasörü (`veri/`, 100 hisse parquet) yeni PC'de nereden gelecek: yeniden indirme mi (İş Yatırım geçmişi değişmiş olabilir), yedekten kopyalama mı? Anlık görüntüler Git dışında nerede yedeklenecek?

12-090. Yedekleme: anlık görüntüler, deneme günlüğü ve kural kaydı projenin gerçek varlığı; kod ise yeniden üretilebilir. Bu verilerin yedeği hangi araçla (OneDrive, harici disk, git-lfs) ve ne sıklıkla alınacak?

12-091. Python 3.14'te serbest iş parçacıklı (free-threaded) sürüm ve JIT deneysel. Standart `python.exe` mi kurulu? Rastgele kural için 1.000 tekrarın hızı (TASARIM.md §5.7) numba olmadan kabul edilebilir mi, yoksa numba'ya mı bağımlıyız?

12-092. 1.000 tekrar × 100 hisse × 11 yıl rastgele karşılaştırma için numba gerekiyorsa, numba bir bağımlılık olarak açıkça seçilecek mi? Yoksa vectorbt'nin dolaylı bağımlılığı olarak mı sürecek ve vectorbt çıkarılınca düşecek mi?

12-093. Motor "kısa ve açık bir döngü" (TASARIM.md §4). Saf Python döngüsü, 1.000 rastgele tekrar ve Holm düzeltmesiyle hangi sürede biter? Süre kabul edilemezse hangi bağımlılık (numba, polars, joblib) eklenecek ve bu ölçüm yapıldı mı?

12-094. pandas 3.x yerine polars düşünüldü mü? Mevcut ön deneme pandas'a bağlı, ama "modern ve sağlam temel" isteniyor; bu seçim kısa gerekçeyle yazıldı mı ve pandas-ta-classic ile quantstats pandas'a bağımlı olduğu için seçeneği baştan kapatıyor mu?

12-095. scipy, scikit-learn, joblib, threadpoolctl ortamda var. scipy istatistik (p değeri, blok yeniden örnekleme) için gerekli mi? scikit-learn hangi işte kullanılıyor ya da hiç kullanılmıyor mu?

12-096. matplotlib 3.11.2 rapor için mi kullanılacak? Markdown raporda grafik (sermaye eğrisi) gerekirse matplotlib ağırlığı haklı mı, ya da Streamlit/Altair ile çakışıyor mu?

12-097. Yapılandırma: sabitler (masraf %0,3, 10 pozisyon, 1.000.000 TL) kod içinde mi, `pyproject.toml` ya da bir `tomllib` dosyasında mı? Python 3.11+ stdlib `tomllib` yeterli mi, pydantic-settings ya da PyYAML (kurulu) gerekli mi?

12-098. Tür güvenliği ve veri sözleşmeleri için `dataclass` (ön denemede kullanılıyor) yeterli mi, yoksa pydantic mi gerekli? pydantic yalnız dış API doğrulamasında mı kullanılacak?

12-099. Bir paket sürümü yükseltmesi ya da silinmesi sonrasında, "bu sonuç hangi ortamla üretildi" sorusunu rapor nasıl cevaplayacak? Raporun başlığında Python, pandas, numpy, statsmodels sürümleri ve kilit dosyası hash'i yazılacak mı?

12-100. Ortamın "kabul testi" ne: temiz bir PC'de depo klonlanıp tek komutla kurulduktan sonra, hangi tek komut ya da test (smoke test) bütün bağımlılıkların içe aktarılıp çalıştığını ve sadakat kontrolünün rakamlarını yeniden ürettiğini gösteriyor?
