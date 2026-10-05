# Sorular 19: Hesap çekirdeği

19-001. TASARIM §4 "Adım (pozisyon, bugünkü mum) → pozisyon" der; bu "mum" bir satır mıdır, bir sözlük mü, bir numpy dizisi mi, yoksa hisse başına bir yapı mı? Canlı günlük ile sınama aynı giriş tipini nasıl paylaşır?

19-002. Fiyat verisi bellekte uzun biçimde (sembol, tarih satırları) mi, geniş biçimde (tarih × sembol matrisi, alan başına bir tane) mi, yoksa hisse başına ayrı DataFrame sözlüğü olarak mı tutulur? Hangi modül hangi biçimi bekler?

19-003. Hisseler arasında işlem günleri farklıysa (tatil, işlem durdurma, geç halka arz, kapanmış hisse), ortak tarih ekseni nasıl kurulur? Eksik gün NaN mı, ileri doldurma mı, satır yok mu sayılır?

19-004. MultiIndex (tarih, sembol) kullanılırsa, `shift`, `rolling` ve `ewm` işlemlerinin hisse sınırını aşıp bir hissenin son gününü ötekinin ilk gününe karıştırmadığı hangi sınamayla kanıtlanır?

19-005. Mevcut `tansu/aileler.py` tek hissenin `pd.DataFrame`'i üzerinde çalışıyor. Yeni çekirdek aynı "hisse başına DataFrame" sözleşmesini mi koruyacak, yoksa tüm evreni tek çağrıda mı işleyecek? Kararın gerekçesi hangi ölçüme dayanır?

19-006. Polars bu proje için düşünüldü mü? Düşünüldüyse, pandas-ta-classic, statsmodels ve quantstats pandas istediği için polars ↔ pandas dönüşümünün maliyeti ve riski nedir; düşünülmediyse neden?

19-007. Fiyat sütunlarının dtype'ı float64 mü, float32 mi? 100 hisse × 11 yıl için bellek farkı pratikte önemli mi, yoksa float32 yalnızca hata kaynağı mı olur?

19-008. BIST fiyat adımı (tick size) fiyat aralığına göre değişir (ör. 0,01 TL, 0,02 TL, 0,05 TL...). Stop, hedef ve AOF dolum fiyatları tick'e yuvarlanacak mı? Yuvarlanmazsa, gerçek emir fiyatlarından sapma sonuçları ölçülebilir ölçüde değiştirir mi?

19-009. TL fiyatlar için `Decimal` ya da tam sayı kuruş (int64) hiç düşünüldü mü? Düşünülmediyse, float64 ile birikimli toplama (sermaye eğrisi, 11 yıl) hata payı kabul edilebilir sınırda mı, bu hangi örnekle gösterilir?

19-010. Düzeltme katsayısı (`SHHE_FIYAT_AYAR_OR`, §5.1) ham fiyata çarpılınca ortaya çıkan 1e-12 düzeyi sapmalar, `HGDG` ile karşılaştırmada "fark" sayılacak mı? Karşılaştırma eşiği mutlak mı, göreli mi, tick bazlı mı?

19-011. Ham ve düzeltilmiş fiyat aynı DataFrame'de iki sütun grubu mu, iki ayrı nesne mi? Göstergelerin düzeltilmiş, likidite ve tavan/taban kontrolünün ham fiyattan hesaplanması (§5.1) tip düzeyinde nasıl zorlanır, yanlış sütunu kullanmak nasıl engellenir?

19-012. Düzeltme katsayıları geriye doğru kümülatif çarpılırken (bedelsiz, bölünme, bedelli, temettü) olay sırası ve aynı güne denk gelen birden çok olay nasıl çözülür? Sıra hatası kalıcı sessiz bir hata mıdır?

19-013. Hacim sütunu lot mu TL mi olduğu belirsiz (§5.1, S2-14). Çekirdek bu belirsizlik çözülmeden mi yazılacak, yoksa birim ilk veri işinde sabitlenene kadar likidite hesabı bloke mi kalacak?

19-014. AOF (ağırlıklı ortalama fiyat) kapanış, yüksek, düşük aralığının dışına düşebilir mi (veri hatası)? Böyle satırlar çekirdekte reddedilir mi, kırpılır mı, karantinaya mı alınır?

19-015. Her mum için `düşük ≤ AOF ≤ yüksek`, `düşük ≤ kapanış ≤ yüksek` gibi değişmezler çekirdeğe giriş noktasında doğrulanacak mı? Doğrulama başarısızsa koşu durur mu, o hisse mi atılır?

19-016. EMA, `ewm(span, adjust=False, min_periods=gun)` ile mevcut kodda ilk değeri ilk fiyata eşitliyor. İlk `gun` değer atıldığı için bu "SMA ile tohumlama" ile aynı mıdır, değilse TA-Lib / pandas-ta-classic sonuçlarından ne kadar sapar?

19-017. EMA200 ve SMA250 gibi uzun göstergeler için, her hissenin ilk 200–250 günü NaN kalır. Bu günlerde sinyal üretilmemesi karar olarak mı yazılı, yoksa NaN karşılaştırmasının `False` dönmesinin yan etkisi mi?

19-018. NaN karşılaştırmaları (`NaN > x` → False) kuralın "koşul sağlanmadı" ile "veri yok" ayrımını siler. Çekirdek bu iki durumu ayırmak için üç değerli mantık, ayrı maske ya da istisna kullanacak mı?

19-019. Hisse geç halka arz olduysa ya da 2015'ten sonra işlem sırası açıldıysa, göstergeler o hissenin kendi ilk gününden mi ısınır, yoksa ortak takvimdeki ilk günden mi? Isınma süresi evren üyeliği (§5.2) ve karantina pencereleriyle nasıl birleşir?

19-020. Karantina (§5.1) "o hisse o pencerede sınamadan çıkar" der. Pencerenin ortasında çıkan hisse için göstergeler karantina boyunca ve sonrasında nasıl işlenir: boşluk atlanıp bitişik mi sayılır, yoksa isınma sıfırlanıp yeniden mi başlar?

19-021. EMA gibi özyinelemeli göstergeler, evrene giriş tarihine bağlıdır: aynı hisse 2020'de 200 gün ısınmış ya da 2015'ten beri çalışıyor olabilir. Sonucun başlangıç tarihine duyarlılığı ölçülecek mi, ölçülecekse nasıl?

19-022. Gösterge kütüphanesi seçeneği: pandas-ta-classic, TA-Lib, kendi birkaç satır. Üç seçenek aynı girdide ATR(14), EMA ve SMA için nümerik olarak aynı mı? Bu karşılaştırma hangi testle sabitlenir?

19-023. pandas-ta-classic, bakımı sürdürülen bir fork. Sürüm değişince bir göstergenin varsayılan davranışı (ör. ATR için Wilder RMA mı EMA mı, `talib=True` bayrağı) sessizce değişirse, sınama sonuçlarının tekrarlanabilirliği nasıl korunur?

19-024. TA-Lib, Windows 11'de wheel ile kuruluyor ama C kütüphanesi bağımlılığı taşıyor. Tek kişilik, teknik olmayan bir kullanıcı için kurulum riski, kendi yazılan 5–10 satırlık EMA/ATR/SMA'ya karşı tartıldı mı?

19-025. ATR(14) için Wilder düzleştirme (alfa = 1/14) mi, standart EMA (alfa = 2/15) mi, yoksa basit ortalama mı kullanılacak? Tansu kaynağında bu yok (§5.5); seçim YORUM olarak deneme sayısına girecek mi?

19-026. ATR'nin ilk değeri (tohum) için TR'nin ilk 14 günlük ortalaması mı, ilk TR mı kullanılır? İlk TR için önceki kapanış yoksa (serinin ilk günü) TR sadece High−Low mu olur, NaN mı?

19-027. Gerçek aralık (true range) hesabında, düzeltilmiş fiyatta bedelsiz günü önceki kapanışla karşılaştırılırken karantina gününde ya da veri boşluğunda önceki kapanış eksikse, ATR ne yapar? Hata sessizce mi yayılır?

19-028. Z-skor için yuvarlanan β, ortalama ve std (§KURALLAR 3) `ddof=0` mı `ddof=1` mi? Sadakat kontrolündeki Z = −3,108 gibi rakamı yeniden üretmek bu seçime hassas mı, hangi aday formül kümesi önceden yazıldı?

19-029. Yuvarlanan regresyon β'sı için `statsmodels.RollingOLS`, elle yazılmış kovaryans/varyans oranı ve numpy `lstsq` seçenekleri arasından hangisi ve neden? Pencere içindeki NaN, kesişim terimi ve sayısal kararlılık nasıl ele alınır?

19-030. Eşbütünleşme testi (Engle-Granger, `statsmodels.coint`) her yıl başı, aynı sektör çiftleri için koşulacak. Çift sayısı büyüdüğünde (sektör içi kombinasyonlar) hesap süresi ve `coint`'in MacKinnon p değeri yaklaşımının kararlılığı ölçüldü mü?

19-031. Çift rotasyonunda log fiyat kullanılacak. Düzeltilmiş fiyatta temettü ve bedelsiz sonrası log getiriler toplanabilir; ama seviye olarak log(Y) − β·log(X) düzeltme günlerinde süreksiz olabilir mi? Hangi fiyat serisi (ham, düzeltilmiş) kullanılır?

19-032. TASARIM §4 vectorbt'yi reddedip "kısa ve açık bir döngü" der. 100 hisse × ~2.750 işlem günü × 1.000 permütasyon ≈ 275 milyon adım yapar; saf Python'da adım başına 2–5 µs bile ~10–25 dakika eder. Bu tahmin ölçüldü mü, hedef süre nedir?

19-033. Hedef toplam koşu süresi (geliştirme 200 tekrar, son rapor ≥1.000 tekrar, §5.7) için bir bütçe var mı? "Tek koşu en fazla N dakika" gibi bir kabul sınırı olmadan hız optimizasyonuna ne zaman başlanacağı nasıl karar verilir?

19-034. Adım fonksiyonu bir pozisyon nesnesi alıp döndürürse, 275 milyon çağrıda nesne tahsisi ve dataclass maliyeti baskın olur. Pozisyonun yapısı numba ile uyumlu düz sayısal diziler (struct of arrays) olarak mı tasarlanır?

19-035. Numba, "sınama ve canlı günlük aynı fonksiyonu kullanır" ilkesiyle (A5) uyumlu mu? Canlı günlükte JIT derleme gecikmesi (ilk çağrı saniyeler) ve Windows'ta numba/llvmlite sürüm uyumu için bir plan var mı?

19-036. Numba önbelleği (`cache=True`) Windows'ta kullanıcı dizininde ya da `__pycache__`'te tutulur. Önbellek bozulması, Python sürüm güncellemesi ve proje klasörü taşınması durumlarında sessiz yanlış sonuç riski var mı?

19-037. Numba'nın kayan nokta davranışı (`fastmath`, FMA kaynaklaşması) saf Python sonuçlarından son bitlerde ayrışabilir. "Sınama ve canlı aynı fonksiyon" ilkesi, numba'lı ve numba'sız yolun bit düzeyinde aynı olmasını mı gerektirir, yoksa tolerans yeterli mi?

19-038. Permütasyonlar (rastgele kural, §5.7 K1) hisse × gün üzerinde bağımsızdır. Çoklu işlem (multiprocessing, joblib) Windows'ta "spawn" ile çalışır; veri her işçiye kopyalanırsa 1.000 permütasyon için bellek ve başlatma maliyeti ne olur?

19-039. Rastgele kural koşusunda her permütasyon motorun tamamını (Adım + Simülatör, pozisyon sınırı, sıra kuralı) yeniden mi koşar, yoksa vektörleştirilmiş bir kısayol mu var? Kısayol kullanılırsa gerçek motorla eşitliği nasıl sınanır?

19-040. Rastgele sinyal çekimi, "kuralın kendi ön şartlarını sağlayan günlerden" ve hisse başına eşleştirilmiş sayıyla yapılır (§5.7 K1). Önceden hesaplanmış uygun gün maskeleri bellekte kaç MB tutar ve her permütasyonda yeniden mi örneklenir?

19-041. Rastgele sayı üretimi için hangi jeneratör kullanılacak (`numpy.random.default_rng`, PCG64)? Tohum (seed) deneme günlüğüne (§5.11) yazılacak mı, ve her permütasyon için bağımsız alt tohum (`SeedSequence.spawn`) üretilecek mi?

19-042. Paralel koşuda sonuçların işçi sayısından bağımsız aynı çıkması (belirleyicilik, A2) nasıl garanti edilir? Permütasyon başına tohum sabitse bile sonuçların toplanma sırası ve kayan nokta toplamı sırası değişirse p değeri oynar mı?

19-043. "Belirleyici" (§4 Motor) ne anlama gelir: aynı makinede bit düzeyinde aynı mı, farklı makine/kütüphane sürümünde aynı rapor sonucu mu? Hangi düzeyin testi yazılacak?

19-044. Kütüphane sürümleri (numpy, pandas, statsmodels, numba) kilitlenmiş mi? `pyproject.toml` şu an yalnız pytest yapılandırması içeriyor; bağımlılık listesi, kilit dosyası ve Python sürümü hiçbir yerde tanımlı değil.

19-045. Python sürümü ve bağımlılık yönetimi için `uv`, `pip-tools` ya da düz `pip` mi kullanılacak? Teknik olmayan kullanıcı tek komutla ortamı yeniden kurabilmeli; bu hangi araçla ve hangi kilit dosyasıyla sağlanır?

19-046. Tüm evrenin 11 yıllık günlük verisi (100 hisse × 2.750 gün × ~8 sütun × 8 bayt) yaklaşık 17 MB eder; ama "kapanmış ve evreye girip çıkan" hisselerle sayı 300–400'e çıkabilir. Bellek bütçesi gerçekten bir sorun mu, yoksa süre mi tek kısıt?

19-047. Sermaye eğrisi ve işlem listesi 1.000 permütasyon için saklanacak mı, yoksa yalnız özet istatistik mi? Tüm eğriler saklanırsa (1.000 × 2.750 × float64 ≈ 22 MB her aile/masraf/parametre için) disk ve bellek ne kadar büyür?

19-048. Parametre sağlamlığı (§5.10) rastgele ızgara, masraf senaryoları (%0,1/0,3/0,5), iki giriş türü (a/b), üç aile, ileri yürüme yılları ve ≥1.000 permütasyon çarpılırsa toplam koşu sayısı kaç olur? Bu çarpım hesaplandı mı?

19-049. İleri yürüme (§5.8) genişleyen pencerede her yıl için göstergeleri yeniden mi hesaplar? Göstergeler yalnız geçmiş veriye bağlı olduğundan bir kez hesaplanıp dilimlenebilir; ama bu ilke gelecek bilgisi sızıntısı (look-ahead) açısından nasıl kanıtlanır?

19-050. Sızıntı (look-ahead) önleme: bir göstergenin t günündeki değeri yalnız t ve öncesine bağlı olmalı. Tam seriyle hesaplanıp kesilen seri ile hesaplanan sonucun eşitliğini sınayan otomatik bir test (kısaltma değişmezliği) planlandı mı?

19-051. Tepe/dip (pivot) tespiti (AB=CD) "teyit edilince" geçerli olur; sağ taraf pencere kadar gecikme gerektirir. Vektörleştirilmiş pivot hesabı yanlışlıkla geleceğe bakabilir; pivotun yalnızca teyit gününden itibaren kullanılabilir olduğu nasıl zorlanır?

19-052. Pivot bulmak için `scipy.signal.argrelextrema` / `find_peaks`, zigzag ya da kendi pencere kuralı seçenekleri var. Eşit yüksek değerler (düz tepe) ve ardışık eşit kapanışlar nasıl çözülür? Sonuç sürüm değişimine dayanıklı mı?

19-053. EMA sıkışması için `rolling(10).sum() >= 3` gibi kalıplar sinyal sayısını gizli biçimde değiştirir (mevcut `aileler.py` 10 günlük pencerede 3 gün sayıyor; KURALLAR "en az 3 gün" ardışık mı demek istiyor?). "Ardışık" ile "pencerede toplam" tanımı çekirdek düzeyinde nerede sabitlenir?

19-054. Sinyal fonksiyonları yalnız boolean mu döndürür, yoksa giriş fiyatı, stop, hedef ve gerekçe de mi? AB=CD'de A seviyesi ve D hedefi sinyal günü hesaplanır; bu değerler Adım fonksiyonuna sinyal çıktısı olarak nasıl taşınır?

19-055. Sinyal günü kapanışta üretilip ertesi gün AOF'ta dolum yapılır (§5.3). Ertesi gün veri eksikse (işlem durdurma, tatil, hisse kapandı) bekleyen emir iptal mi olur, bir sonraki işlem gününe mi kayar? Bu kural çekirdeğin neresinde durur?

19-056. Kilitli tavan/taban (düşük = yüksek = tavan/taban) tespiti float eşitliğine dayanır. Düşük ve yüksek float64'te tick'e yuvarlanmamış düzeltilmiş fiyatlardan gelirse eşitlik testi çalışır mı? Tespit ham fiyat üzerinde mi, hangi toleransla yapılır?

19-057. Tavan/taban fiyatı önceki kapanışın ±%10'u (veya ±%20) tick'e yuvarlanmış halidir. Limit hesabı yuvarlama kuralı (aşağı mı, en yakın mı) BIST'in gerçek kuralıyla birebir olmalı; bu kural nerede yazılı ve test edilmiş mi?

19-058. Stop dolumu "gün düşüğü ≤ stop" koşuluyla karşılaştırılırken stop, ATR'den türetilmiş bir float. Düşük == stop sınır durumunda dolum olur mu? Bu eşitlik kuralı (≤ mi <) test örneklerinde belirtilmiş mi?

19-059. Adet hesabı (risk / 2ATR) tam sayı lota yuvarlanır mı? Yuvarlama yönü (aşağı) ve minimum 1 lot kuralı, risk %1 olmadığında oluşan sapmayı ve küçük sermayede 0 lot sonucunu nasıl yönetir?

19-060. Sermaye 1.000.000 TL, pozisyon tavanı %10: adet ve nakit hesabı float64 ile mi tutulacak? İşlem başına masraf (%0,3) kuruş düzeyinde yuvarlanacak mı, yuvarlanırsa 11 yılda birikimli fark ölçülebilir mi?

19-061. Boştaki nakit faizi günlük bileşik mi basit mi işleyecek ve gün sayımı (365/360, takvim günü/işlem günü) nedir? Hafta sonu ve tatiller için faiz tahakkuku çekirdekte nerede hesaplanır?

19-062. Politika faizi basamak olarak toplantı günlerinde değişir. Faiz serisi işlem günlerine hizalanırken "toplantı günü" etkisi (aynı gün mü ertesi gün mü geçerli) hangi kuralla ve hangi sızıntı kontrolüyle çözülür?

19-063. Çift rotasyonu aynı günde Y→X geçişi yaparken satış ve alış aynı gün iki işlem mi olur (iki kat masraf) yoksa tek işlem mi? Geçiş günü iki hissenin AOF'u ve hacim kısıtları (§5.4) nasıl işlenir?

19-064. Sermaye eğrisi her gün için mark-to-market mi hesaplanır (kapanış fiyatıyla), yoksa yalnız kapanan işlemlerde mi güncellenir? Günlük fazla getiri serisi (§5.7, §5.9) bu seçimden doğrudan etkilenir.

19-065. Portföy günlük getirisi basit getiri mi log getiri mi? Bloklu yeniden örnekleme (20 günlük bloklar, §5.9) ve Holm düzeltmesi için hangi getiri tanımı kullanılırsa kullanılsın, çarpımsal birikim ile toplamsal birikim aynı sonucu verir mi?

19-066. Blok bootstrap için `arch` kütüphanesi (`StationaryBootstrap`, `CircularBlockBootstrap`) mi, kendi yazılacak 20 günlük blok örnekleyici mi kullanılacak? TASARIM'da `arch` listede yok; "güvenilir kütüphane" ilkesi burada nasıl uygulanıyor?

19-067. Blok uzunluğu 20 sabit. Seri sonunda kalan eksik blok ve bloklar arası yapışma noktaları (dairesel mi, atılan mı) nasıl işlenir? Sonuçların bu seçime duyarlılığı raporlanacak mı?

19-068. p değeri K1 permütasyonlarından çıkar. 1.000 tekrarla elde edilebilecek en küçük p değeri 1/1001 ≈ 0,001'dir; Holm düzeltmesi yüzlerce denemeye uygulanırsa bu çözünürlük yeterli mi? Gerekli tekrar sayısı çoklu deneme sayısına göre hesaplandı mı?

19-069. Permütasyon p değeri için `(1 + ≥gözlenen sayısı) / (1 + N)` biçimi mi yoksa `≥ / N` mi kullanılacak? Sıfır p değerinin çıkması yasak mı? Bu tek satırın formülü tasarımda yazılı değil.

19-070. Medyan, "en iyi %5 işlem atılmış" ortalama ve güven aralığı için `numpy.percentile` yöntemi (linear, nearest, vb.) ve eşitlik durumları (işlem sayısı 20'nin katı değilse) sabitlendi mi? Farklı interpolasyon yöntemi farklı kabul kararı verebilir mi?

19-071. `quantstats` (§4) pandas serisi bekler ve içeride varsayılan yıllandırma (252 gün), risksiz oran ve `empyrical`-türevi hesaplar kullanır. BIST için işlem günü sayısı yılda ~250 ve sabit değil; yıllandırma çarpanı ve maksimum düşüş / düşüşte kalma süresi (§5.12, m5) quantstats'ın tanımıyla mı hesaplanacak?

19-072. quantstats son yıllarda bakım ve uyumluluk sorunları yaşadı (pandas yeni sürümleriyle kırılmalar). Kabul ölçütündeki "düşüşte kalma süresi 12 ay" gibi bir sayı kütüphane sürümü değişince değişirse, kendi 5 satırlık hesapla çapraz kontrol yapılacak mı?

19-073. Maksimum düşüş hesabı sermaye eğrisinden (günlük mark-to-market) mi, kapanış bazlı mı? Gün içi düşüş (düşük fiyat) yok sayılacağı için düşüş küçük hesaplanır; kabul ölçütü %25 bu hesapla tutarlı mı?

19-074. Sayısal çıktılar rapora yazılırken yuvarlama nerede olur? Karar ölçütleri (p < 0,05, %60 yıl, %25 düşüş) yuvarlanmış değerle mi ham değerle mi karşılaştırılır? Sınır değerler (ör. p = 0,0500 yuvarlama sonrası) nasıl ele alınır?

19-075. Deneme günlüğü (§5.11) kod hash'i ve veri anlık görüntüsü hash'ini içerir. Hash hangi kapsamı kapsar: yalnız çekirdek kaynak dosyalar mı, bağımlılık sürümleri ve numba derlenmiş kod da mı? Hash aynı ama sonuç farklıysa nasıl yakalanır?

19-076. Anlık görüntünün (parquet) hash'i dosya baytları üzerinden mi hesaplanır? Parquet yazarının (pyarrow sürümü) meta verisi aynı veride farklı bayt üretirse "aynı anlık görüntü" kimliği bozulur mu?

19-077. Parquet okuma yazma `pyarrow` ya da `fastparquet` ile yapılacak; sütun tipleri (float64, tarih, int64 hacim) ve zaman damgası dilimi (UTC, Europe/Istanbul, naive) hangi kuralla sabitlenir? Tarih dizini naive date mi, Timestamp mi?

19-078. İstanbul saat dilimi ve yaz saati yok (UTC+3 sabit, 2016'dan beri); 2015–2016 verisinde saat dilimi karışırsa günlük çubuk tarihi bir gün kayabilir mi? Tarih alanı saf tarih (date) olarak mı tutulur?

19-079. Tekrarlanan veya sıra dışı tarihler (aynı gün iki satır, azalan sıra) veri deposu çıkışında reddedilir mi, yoksa çekirdek kendi başına sıralayıp tekilleştirir mi? Sorumluluk hangi modülde?

19-080. Veri deposu çıktısı ile çekirdek girdisi arasında bir "şema sözleşmesi" olacak mı (sütun adları, dtype, dizin türü, sıralama)? Sözleşme `pandera`, `pydantic`, elle `assert` ya da hiç mi kullanılmayacak; "minimum altyapı" ile "doğrulama" nasıl dengelenir?

19-081. Sütun adları İngilizce (`Close`, `High`) mı Türkçe (`kapanis`, `yuksek`) mi olacak? Mevcut kod `Open/High/Low/Close/Volume` kullanıyor; İş Yatırım ham alanları (`HG_*`, `HGDG_*`) var; çekirdeğin dahili adlandırması nerede çevrilir?

19-082. Kodda ve göstergelerde Türkçe ve ASCII olmayan karakterlerin (ş, ğ, ı) fonksiyon/değişken adlarında kullanılması Windows'ta dosya yolu ve konsol kodlamasında (cp1254, cp1252, UTF-8) sorun çıkarabilir mi? Rapor yazımı için dosya kodlaması sabit mi?

19-083. "Adım" saf bir fonksiyon (aynı girdi aynı çıktı, dış durum yok) mi olacak? Saf olması için rastgelelik, saat, dosya okuma gibi şeyler dışarıdan mı verilecek; saf olmayan tek yer neresi?

19-084. Aynı gün birden çok sinyal olduğunda "en likit önce" sıra kuralı (§5.6, M12) eşitlik durumunda (aynı likidite) hangi ikinci kuralla bozulur? Sembol alfabetik sırası kullanılırsa belirleyicilik sağlanır, ama bu bir yanlılık oluşturur mu?

19-085. Hisse başına bir pozisyon, tek hisse bölmesi 10 pozisyon: durum (açık pozisyonlar) bir dict, DataFrame ya da dizi mi? Her gün tüm 100 hisse için döngü yerine yalnız açık pozisyonlar ve yeni sinyaller üzerinde dönmek hız için yeterli mi?

19-086. Adım döngüsü "gün gün" (dışta zaman, içte hisse) mi, "hisse hisse" (dışta hisse, içte zaman) mi sıralanır? Portföy düzeyli kısıtlar (nakit, 10 pozisyon sınırı, likidite) gün içi sıra gerektirdiği için hangi ek maliyetle gelir?

19-087. Tek hisse bölmesinde pozisyon sınırı ve nakit kısıtı aileler arasında bağımsız (ayrı sermaye), ama aynı hisse üzerinde farklı aileler işlem açabilir. Çekirdek "aile × bölme" bağımsızlığını koşu bazında mı yoksa tek ortak döngüde mi uygular?

19-088. Kâğıt üstü canlı dönem (§5.8) için günlük çalışan program, durum (açık pozisyonlar) nerede saklar: CSV, parquet, SQLite, pickle? Durum biçimi sınama motorunun iç durumuyla aynı mı; sürüm değişince eski durum dosyası okunur mu?

19-089. Yeniden başlatma ve kesinti sonrası (bilgisayar 19:30'da kapalıydı) kaçırılan günlerin geriye dönük işlenmesi nasıl olur? Adım fonksiyonu gün atlandığında tutarlı mı, gün-gün tekrar oynatma mı gerekir?

19-090. Eksik gün veya yanlış veri nedeniyle geçmiş bir günün düzeltilmesi durumunda (kaynak geçmişi değiştirdi, §4 B2) durum yeniden baştan mı oynatılır? Oynatma süresi canlı günlük için kabul edilebilir mi?

19-091. Yuvarlanan ortalamalarda `min_periods` ve `rolling` kullanımı mevcut kodda tutarsız (`ewm` için min_periods var, `rolling(10).sum()` varsayılan). Seri başlangıcında kısmi pencere (ör. 5 günlük medyan) hesaplanacak mı, yoksa tam pencere zorunlu mu? Bu bir proje kuralı olarak yazılı mı?

19-092. Likidite filtresi "son 10 günün medyan TL işlem tutarı" (M11) kullanır. Medyan, bugünü içerir mi hariç tutar mı? Sinyal günü kapanışında bilinen veri (bugün dahil) ile ertesi gün işlem sırasında bilinen veri arasındaki sızıntı sınırı nerede?

19-093. Evren seçimi için "60 günlük medyan TL işlem tutarı ve piyasa değeri en büyük 100" (§5.2) aylık hesaplanır. Piyasa değeri sütunu (`PD`) günlük mü, ay sonu mu; düzeltmesiz hisse sayısı değişince (bedelsiz) süreksiz olabilir; bu seri çekirdeğe hangi biçimde girer?

19-094. Sektör içi en iyi 5 çift seçimi her yıl başı 252 günlük pencerede eşbütünleşme p değeriyle yapılır. Aynı yıl içinde pencere kapanışı yılın son işlem günü mü, ilk gün öncesi mi? Gün sayısı yıldan yıla farklıysa pencere 252 sabit işlem günü mü, takvim yılı mı?

19-095. Testler (pytest) çekirdek için nasıl yapılandırıldı: elle hesaplanmış küçük örnekler (§5.3'teki yedi motor sınaması), özellik tabanlı testler (hypothesis) ve bir "altın" tam koşu sonucu (golden file) var mı? Altın dosya sürüm değişiminde nasıl güncellenir ve kim onaylar?

19-096. Vektörleştirilmiş (pandas) ve döngü/numba (Adım) uygulamaları aynı sinyali iki ayrı yolla hesaplarsa, ikisinin eşitliğini sınayan çapraz test var mı? Çift uygulama "tek doğru kaynak" ilkesini bozmaz mı?

19-097. Profilleme önce mi sonra mı yapılacak? Hız optimizasyonu (numba, vektörleştirme, çoklu işlem) ancak ölçümle yapılacaksa, hangi araç (cProfile, `timeit`) ve hangi referans iş yükü (100 hisse × 11 yıl × 1 tekrar) kabul ölçütü olarak yazıldı?

19-098. Teknik olmayan kullanıcı, çekirdek hesabını tek komutla çalıştırıp ilerleme ve kalan süreyi görebilecek mi? 1.000 permütasyonlu koşu 30 dakika sürerse yarıda kesilince kısmi sonuç saklanır mı, kaldığı yerden devam eder mi?

19-099. Hata durumunda (NaN, sonsuz değer, sıfıra bölme, negatif fiyat) çekirdek koşuyu durdurur mu, uyarı yazıp devam mı eder? `numpy` uyarıları (`np.seterr`) ve pandas `SettingWithCopyWarning` gibi sessiz davranışlar proje düzeyinde hata sayılacak mı?

19-100. Yeni çekirdek için "modern, modüler ve sağlam temel" hedefi ile "minimum altyapı" arasında, hangi parça (veri çerçevesi seçimi, numba, gösterge kütüphanesi, şema doğrulaması, çoklu işlem) kesinlikle şimdi, hangisi ilk aile kabul edildikten sonra eklenir? Bu sıralama hangi ölçüme bağlı?
