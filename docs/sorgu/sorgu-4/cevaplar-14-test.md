# Cevaplar 14: Test stratejisi

Doğrulanan olgular: `pytest -q` şimdi 13 test geçiyor, 6,1 sn. Venv projede (`.venv`, Python 3.14.7, numpy 2.5.3, pandas 3.0.6, pytest 9.1.1). Kurulu: statsmodels, scipy, pyarrow, yfinance, vectorbt, borsapy. Kurulu değil: hypothesis, freezegun, pytest-socket, coverage, mutmut, streamlit, quantstats. `pyproject.toml` yalnız pytest ayarı içeriyor, bağımlılık listesi yok. `veri/` `.gitignore`'da. Yerel git var, uzak repo yok.

**14-001** — KARAR — Test yüzleri: Adım (pozisyon, mum → pozisyon), Motor (sinyal, fiyat → işlem listesi), Maliyet, Simülatör, İstatistik (+ Holm), Takvim, Evren (tarih → liste), olay düzeltmesi, Aile (fiyat → sinyal günleri), Rapor (metin). Test yalnız bu girdi ve çıktıdan yazılır. Bir modülün içi değişince hiçbir test kırılmamalı; iç yardımcı fonksiyon ve sütun adı sınanmaz.

**14-002** — KARAR — Dolum kuralları (stop, hedef, boşluk, aynı gün, tavan, taban) Adım üzerinde tek mumla sınanır; Motor'da yalnız 2 çok günlü test olur. "Ayrışamaz" iddiasını yapı kanıtlar: canlı günlük kod Motor'un çağırdığı aynı fonksiyonu içe aktarır. Ek olarak 1 test: aynı sinyal + mum dizisinde canlı güncelleme ile Motor aynı çıkış gününü ve fiyatı verir.

**14-003** — KARAR — Aynı girdiyle iki koşu, `pandas.testing.assert_frame_equal(check_exact=True)`. Hash yok, tolerans yok; aynı makine, aynı kod, tam eşitlik beklenir.

**14-004** — YANLIŞ — `tests/test_kanit.py` ilk iki testi vectorbt, `Open`, `MASRAF == 0.002`, 4 ATR hedef ve EMA50 bozulmasına dayanıyor (`tansu/kanit.py:14-16`); tamamen silinir, yerine §5.3 örnekleri (AOF girişi, %0,3 her yön, 2 ATR) gelir. `ozet` testi yeni modülde `ozet` kalırsa aynen kalır. `test_nabiz_veri.py`: `temizle` iki testi (Yahoo bedelsiz eşiği) silinir; 4 nabız testi kalır. `test_aileler.py` eski ailelere ait; içeriğini ayrıntılı doğrulamadım, yeni 3 aileyle yeniden yazılır.

**14-005** — YANLIŞ — Yedi durum eksik; §5.3 "giriş günü de kontrol edilir" diyor ama yedi durumda yok. Ekle: giriş günü stop; giriş günü stop+hedef (stop önce); sinyalden sonra veri yok (işlem açılmaz, hata yok); açık pozisyonda yeni sinyal sayılmaz. Toplam 11 durum.

**14-006** — KARAR — Aynı ajan hem hesabı hem kodu yazarsa hesap bağımsız sayılmaz. İkinci bir oturum, kodu görmeden aynı mum tablosundan beklenen değeri hesaplar. Fark çıkarsa Levent'e düz Türkçeyle (veri, beklenen, neden; 3 satır) sorulur.

**14-007** — KARAR — Sayılar testin içinde, en üstte Türkçe yorum olarak (veri / hesap / sonuç). Ayrı CSV yok. `tests/test_kanit.py` bunu zaten yapıyor (satır 13-14, 22). Levent 1-3 satırlık hesabı okuyabilir.

**14-008** — KARAR — Üç ayrı test: düşük == stop → stop fiyatı; yüksek == stop (düşük < stop) → stop fiyatı (tasarım "altındaysa" diyor, katı <); yüksek = stop − 0,01 → AOF.

**14-009** — KARAR — Tam eşitlik (`==`). Ham fiyat kaynakta iki ondalık; tavan = `round(önceki kapanış × 1,10; 2)`. Testler: tam tavan → giriş yok; tavan − 0,01 → giriş var. Tick adımının fiyat bandına göre değişip değişmediğini doğrulamadım.

**14-010** — KARAR — `limit(tarih)` saf fonksiyon: 12.03.2020 → 0,20; 13.03.2020 → 0,10. İki test: aynı +%15 sıçrama 12.03'te karantina değil, 13.03'te karantina. Eşik (+0,5 puan) için tam sınır testi. ECILC/RYSAS gerçek veriye alınmaz; sentetik mum yeter.

**14-011** — KARAR — Hepsi elle yazılmış sentetik (Adım, Motor, Maliyet, Simülatör, Takvim, Evren, Aile). Gerçek veri kesimi yalnız iki yerde: CCOLA bölünmesi (olay düzeltmesi) ve sadakat kontrolü.

**14-012** — KARAR — Risk düşük: repo yerel (AGENTS.md: uzak repo yok), fixture sembol başına en çok 30 satır. Kullanım koşulları netleşince (§8.1) yeniden bakılır; o güne kadar fixture çoğaltılmaz.

**14-013** — KARAR — Fixture tarihli ve değişmez; dosya başında kaynak ve indirme tarihi yorumu. Hiçbir test yeniden indirmez. Yenileme kararı elle ve yalnız Levent'indir; bunun için test yok.

**14-014** — KARAR — Evet. `tests/conftest.py` içinde autouse fixture: `socket.socket.connect` çağrısı hata verir (pytest `monkeypatch`, ~5 satır, yeni bağımlılık yok).

**14-015** — KARAR — Elle sahte: istemci, veri deposu fonksiyonuna `getir` parametresi olarak geçer; testte sahte fonksiyon verilir. Cassette ve vcr/responses yok (kurulu da değil). Ayrıştırma kodu 3-5 satırlık gerçek örnek JSON'la sınanır.

**14-016** — KARAR — Pakette duman testi yok. Canlı kaynağa karşı ilk gerçek sınama zaten elle yapılan indirme. Günlük işleyişte başarısızlık = kart yok (m6); ayrı test gerekmez.

**14-017** — KARAR — Hermetik çelişmez: şema kontrolü çalışma zamanında yapılır (beklenen sütunlar `HG_KAPANIS`, `HGDG_*`… yoksa veri deposu hata verir, kart üretilmez). Testte eksik sütunlu sahte yanıt → hata beklenir. Gerçek şema değişimini yalnız canlı indirme yakalar.

**14-018** — KARAR — Birim çözülünce sonuç kodda tek sabit olarak yazılır ve gerçek bir günden (fiyat × lot ≈ TL) alınmış 1 fixture satırıyla 1 test sabitler. Birim yanlışsa sessizce yanlış geçenler: sentetik hacimle yazılmış likidite %2 testleri; o yüzden likidite testi aynı birimi kullanan tek bir sabite bağlanır.

**14-019** — KARAR — İkisi ayrı: kod doğruluğu test (CCOLA kesimi + elle düzeltilmiş beklenen); veri doğruluğu çalışma zamanı denetimi (her indirmede `HGDG` farkı listelenir, tasarım zaten böyle). Sınır: kod hatası → test, kaynak hatası → denetim.

**14-020** — KARAR — Dört ayrı 2-3 günlük elle hesap (bedelsiz, bölünme, bedelli, temettü). Bağımsız doğrulayıcı `HGDG/HG` oranıdır (`docs/arastirma/veri-kaynaklari.md` satır 87: THYAO 0,9769, CCOLA 29.07.2024); formül bu gerçek orana uymalı. Bedelli ve temettü formülünü Levent değil, bu oran doğrular.

**14-021** — KARAR — Belirsizlik çözülmeden temettü testi yazılmaz. Beklenen değer varsayımdan değil `HGDG`'den alınır: CCOLA temettü kesiti hangi günde sıçradığını gösterir ve §8.2'yi veri çözer.

**14-022** — KARAR — Karantina düzeltmeden sonraki getiriye bakar. Bir test: olay düzeltmesinden sonra hâlâ limit+0,5 puanı aşan gün karantinaya girer; olayla tam açıklanan gün girmez.

**14-023** — KARAR — Listeyi yakalayan test yok (eksik tatil testle bilinemez). Çalışma zamanı denetimi: veride var olup Takvim'de tatil sayılan gün → uyarı. Bu denetim için 1 sahte veri testi.

**14-024** — KARAR — Evet: `evren(t, tam veri) == evren(t, t'ye kadar kesilmiş veri)`. Tek test, sentetik 3-4 hisse.

**14-025** — KARAR — Evet, tek ortak parametrik test (pytest.mark.parametrize): gösterge, ATR, her aile sinyali, evren, çift seçimi için sentetik 300 günlük seri t'de kesilir; t günündeki çıktı aynı kalmalı. Yeni bağımlılık yok.

**14-026** — KARAR — Fixture: 3 hisse, biri 30. günde biter (ASYAB benzeri). Test: bitiş öncesi tarihte evrende, sonrasında yok ve işlem listesinde görünüyor.

**14-027** — KARAR — Evet: maliyet 0 iken net getiri = brüt getiri. %0,3 için tek elle hesap (100→110, 0,30 + 0,33). %0,1/%0,5 için ayrı hesap yok: aynı kod yolu, tek parametre.

**14-028** — KARAR — Üç ayrı test: tam eşit (izinli, "geçemez" = ≤), bir lot fazla (kırpılır), 10 günden az veri (pozisyon açılmaz).

**14-029** — KARAR — Eşit likiditede sembol adı alfabetik. Test: iki eşit likit sinyal, 1 boş yer, girdi sırası ters çevrilir → aynı seçim.

**14-030** — KARAR — Evet: 1.000.000 TL, %1 risk = 10.000 TL, ATR'den adet; %10 üst sınır ve 10 pozisyon sınırının her biri tek tek bağlayıcı olan 3 senaryo + üçü birlikte 1 senaryo. Adet aşağı yuvarlanır (risk ve sınır aşılmasın); 1 lot = 1 hisse varsayımı repoda doğrulanmadı.

**14-031** — KARAR — Her ikisi: Simülatör içinde 1 satır `assert` (her gün pay tek hissede) ve 3 günlük sentetik takvimle 1 test.

**14-032** — KARAR — 2 çift, 6 işlem günü takvimi: yıl başı gününde çift A düşer, B girer; A pozisyonu kapanır, 200.000 TL pay B'ye geçer; yine seçilen çift işlemsiz devam eder. Elle hesap testin içinde.

**14-033** — KARAR — 3 günlük takvim, nakit 1.000.000 TL, faiz toplantı gününde basamak değiştirir. Hafta sonu ve tatil günleri faiz biriktirir (para o günlerde de faiz kazanır): Cuma→Pazartesi 3 gün. Elle hesap + basamak günü için 2 test.

**14-034** — KARAR — Her ikisi: Simülatör sonunda 1 satır `assert` (nakit + pozisyon = eğri) ve işlem listesi toplamı ile eğri son değerini karşılaştıran 1 test.

**14-035** — KARAR — İki ayrı fonksiyon, ortak arayüz yok (YAGNI). Ortak olan yalnız işlem listesi ve Maliyet. Testler her birine ayrı yazılır.

**14-036** — KARAR — Evet: 3 hisseli, 5 günlük elle evren; sepet getirisi = eşit ağırlıklı aritmetik ortalama; işlem getirisi − sepet getirisi elle.

**14-037** — KARAR — Özellik: 3 hisseli evrende her hisse için rastgele işlem sayısı = gerçek işlem sayısı (her iki tür). Tam sayım karşılaştırması yok; sayı eşitliği yeter. Tohumlu.

**14-038** — KARAR — Rastgele kural aynı Motor ve Simülatör fonksiyonunu çağırır (ayrı uygulama yok). Test: aynı gün 11 rastgele sinyal, sınır 10 → 10 pozisyon açılır.

**14-039** — KARAR — Küme gereken sayıdan küçükse `ValueError` (sessiz kırpma yok). İki test: boş küme ve az küme.

**14-040** — KARAR — Evet, sabit tohum. Test iki şeyi sınar: aynı tohum aynı sonuç (aynı ortamda iki koşu); farklı 3 tohumda kuvvetli kenar p küçük, kenarsız veri p büyük. Tohum değişince geçmesi gereken tek şey bu aralıktır, literal p değil.

**14-041** — KARAR — Hayır, hata sayılmaz. Literal rakam beklenmez. NumPy `Generator` akışının sürümler arası kararlı olduğuna güvenilmez (bilgi; numpy 2.5.3 üzerinde doğrulamadım). Testler özellik ve aralık sınar.

**14-042** — KARAR — Kapsama simülasyonu paket dışında, bir kez çalıştırılır, sonucu rapora yazılır. Pakette yalnız blok yapısı testi: yeniden örneklenen seri 20 günlük bitişik bloklardan oluşur.

**14-043** — KARAR — Paket hedefi 60 sn altı. Testlerde 200 tekrar ve yalnız bariz durumlar (güçlü kenar, kenarsız); ince güç ölçümü paket dışı.

**14-044** — KARAR — NaN yok, hata yok: istatistik modülü `{"durum": "yetersiz örneklem"}` döner (5.9 şartları: < 100 işlem veya < 60 sinyal günü). Üç test: sıfır varyans, tek işlem, 59 sinyal günü.

**14-045** — KARAR — Elle hesap beklenen değerdir: p = [0,01; 0,04; 0,03; 0,005] → sıralı ×4,3,2,1 = 0,02; 0,03; 0,06; 0,04 → monoton: 0,02; 0,03; 0,06; 0,06 → orijinal sırada [0,03; 0,06; 0,06; 0,02]. Uygulama `statsmodels.multipletests` çağırır (kurulu); test beklenen değeri kütüphaneden değil elle alır.

**14-046** — KARAR — Kütüphane yeniden test edilmez. Yalnız bizim çağrımız ve yorumlama kodu sınanır. Tek istisna: pandas-ta ATR ve EMA için 1 elle hesaplı küçük test (sürüm kaymasını yakalar).

**14-047** — KARAR — Pakette yok; 042 ile aynı paket dışı bir kez doğrulama.

**14-048** — KARAR — Evet, tek uçtan uca pozitif kontrol pakette: 30 sentetik hisse, her sinyalden sonra +%5 gömülü; sistem fazla getiriyi pozitif ve p < 0,05 bulur (200 tekrar, tohumlu).

**14-049** — KARAR — Pakette 1 test: saf rastgele yürüyüşte tohumlu bir koşu "aile geçmedi" der. %5 altı yanlış pozitif oranı paket dışı, ≥ 200 koşuyla bir kez ölçülür ve rapora yazılır.

**14-050** — KARAR — Karar fonksiyonu (girdi: ölçüt sayıları) için her koşula iki sınır testi: yıl oranı tam %60 → geçer; p tam 0,05 → geçmez (tasarım "p < 0,05"); hemen altında/üstünde olanlar. Toplam ~12 küçük test.

**14-051** — KARAR — Rapor modülü testi: boş sonuç listesi → "hiçbir aile geçmedi" cümlesi üretilir, istisna yok. Streamlit ekranı raporu okur; ayrı test yok (14-082).

**14-052** — KARAR — Günlük yolu parametre; testte `tmp_path`. `conftest.py` autouse fixture varsayılan günlük yolunu `tmp_path`'e yönlendirir; gerçek günlüğe yazan test mümkün olmaz.

**14-053** — KARAR — Hash `ast.dump` (aile ve çıkış fonksiyonları) + parametrelerin JSON'u üzerinden alınır; `ast` boşluk ve yorumu yok sayar (stdlib). İki test: yorum/boşluk eklenince hash aynı; sabit değişince farklı.

**14-054** — KARAR — Evet: getiri koşusu kural kaydı yoksa hata verir; 1 test.

**14-055** — KARAR — Yalnız pytest testi; ayrı rapor betiği yok. Üretilen parçalar `tests/test_sadakat.py` içinde sabitlenir; üretilemeyenler testte değil, KURALLAR'da YORUM olarak durur.

**14-056** — KARAR — Beklenen değerler tek dosyada, her biri görsel numarası ve "elle okundu" notuyla yazılır. Not ile görsel çelişirse görseli esas alıp ikisi de yorumda kalır. Levent sayıları görselle bir kez karşılaştırır.

**14-057** — KARAR — Yalnız gereken 5 sembol için `tests/veri/` altında CSV (pandas), başında yorum: yfinance 1.7.0, indirme tarihi. Yeniden indirilmez.

**14-058** — KARAR — Tolerans sonuca bakmadan önce yazılır, son hanenin yarısı: z ±0,0005; yüzde ±0,005 puan; D ±0,005. Aday seçimi bu toleransı ilk üreten adaydır.

**14-059** — KARAR — Üretilemeyen parça için test yazılmaz; `skip`/`xfail` yok. Yeşil paket "bu kısım sınanmadı" gerçeğini gizlemesin diye KURALLAR YORUM listesi ve rapor bunu belirtir.

**14-060** — KARAR — 1 test: Motor'a AOF yerine aynı değerleri taşıyan "açılış" sütunu verilince aynı işlem listesi çıkar; fiyat sütunu parametredir, ikinci kod yolu yoktur.

**14-061** — KARAR — 025'teki ortak look-ahead testi kapsar; ek olarak 1 test: tepe, teyit gününden önceki günlerde sinyal vermez.

**14-062** — KARAR — Seçilen formül kilitlendikten sonra test yazılır. Adaylar yalnız sadakat toleransıyla (058) elenir; her aday için tam paket koşmaz.

**14-063** — KARAR — Karar fonksiyonu saf `(z, dz) → giriş`: Z = −2 tam → giriş; Z = −1,99 → yok; ΔZ = 0 tam → yok; ΔZ > 0 → giriş. 4 test.

**14-064** — KARAR — Evet, sentetik: 3. gün giriş, 2. gün değil; bant tam %1,2 sıkışma sayılır, %1,21 sayılmaz; 10. gün tam giriş, 11. gün değil.

**14-065** — KARAR — 1 test: 250 günlük seride ısınma günlerinde sinyal yok. pandas-ta davranış değişimini 046'daki elle hesaplı EMA/ATR testi yakalar.

**14-066** — KARAR — Altın dosya yok. Yerine 046'daki elle hesaplı EMA/ATR testi.

**14-067** — KARAR — Hiçbir çıktı altın olarak saklanmaz.

**14-068** — ZAYIF SORU — Altın dosya yok (14-067); soru boşta kalır.

**14-069** — ZAYIF SORU — Rapor altın dosya olmaz; testler içinde belirli satır var mı diye bakar. Maskeleme gerekmez.

**14-070** — KARAR — CSV `utf-8-sig`, ondalık nokta sabit (yerel ayar kullanılmaz). 1 test: tmp_path'e yaz-oku turu; "ş ı ğ" ve 0,25 aynı döner.

**14-071** — KARAR — Altın karşılaştırma olmadığı için sorun yok. Rapor testi tam metin değil satır içeriği arar; yol için `pathlib`.

**14-072** — KARAR — Hayır, Hypothesis kullanılmaz.

**14-073** — OLGU — Hypothesis kurulu değil (`pip list` ile doğruladım). Evet, elle yazılmış 10-20 kenar durum yeter; yeni bağımlılık eklenmez.

**14-074** — KARAR — Hypothesis kullanılmadığı için strateji yazılmaz. (Kısıt kodu testten karmaşıksa kabul edilmez.)

**14-075** — ZAYIF SORU — Hypothesis kullanılmayacak (14-072).

**14-076** — KARAR — Elle yazılmış üç bozuk mum durumu Adım/Motor testine eklenir: boşluk, tek fiyat (düşük = yüksek), hacimsiz gün (Volume 0). Gerçek bozukluk yalnız CCOLA kesimi.

**14-077** — KARAR — Beklenen değer bağımsız elle: sabit aralıklı seride ATR = aralık (ör. 2,5) olduğundan hesap koddan bağımsızdır. Denetim ikinci ajan hesabıdır (14-006).

**14-078** — YANLIŞ — `tests/test_kanit.py` satır 3 ve 25 `MASRAF`'ı içe aktarıp `== 0.002` ile karşılaştırıyor. Kural: testte sabit literal yazılır (0,003; 2; 250), uygulamadan içe aktarılmaz.

**14-079** — KARAR — Hayır. mutmut/cosmic-ray kurulu değil, Windows'ta çalıştığını doğrulamadım, tek kişi için fazla. Yerine, her motor durumu için bir kural satırı elle bozulur ve testin kırıldığı bir kez görülür.

**14-080** — KARAR — Kapsam hedefi yok (coverage kurulu değil). Ölçü davranış listesi (14-081).

**14-081** — KARAR — Evet. Ölçü: 11 motor durumu, sadakat, pozitif kontrol, look-ahead testi, 5.12 sınır testleri. Liste `tests/` başında bir yorum olarak durur.

**14-082** — KARAR — Streamlit kurulu değil. Ekran ince tutulur (yalnız raporu okur); mantık Rapor modülündedir ve orada test edilir. `AppTest` yok.

**14-083** — KARAR — Ayrı uçtan uca test yok. Tazelik ve takvim fonksiyon testleriyle sınanır; Zamanlayıcı görevini Levent kurulumda elle bir kez dener.

**14-084** — KARAR — `bugun` parametresi (stdlib). freezegun kurulu değil, gerekmez.

**14-085** — KARAR — 2 test: Cumartesi 03.10.2026 ve tatil günü 29.10.2026 için günlük akış boş kart listesi döner, hata yok.

**14-086** — KARAR — Hedef: paket 60 sn altı (şimdi 13 test 6,1 sn, ölçtüm). Motor testleri 5-10 satırlık mum kullanır; hızlı/yavaş işareti gerekmez. 100 hisse × 11 yıl fixture pakete girmez.

**14-087** — KARAR — Üretim koşusu, test değil. Levent'e: test "kod kuralı doğru yapıyor mu" sorusunu saniyede yanıtlar; koşu "kural işe yarıyor mu" sorusunu saatte yanıtlar.

**14-088** — KARAR — Komut: `.venv\Scripts\python.exe -m pytest -q`. Son satır "N passed" = tamam, "N failed" = kırık. Levent koşturmaz; ajan son satırı raporlar.

**14-089** — OLGU — Venv projenin içinde (`.venv`, Python 3.14.7, numpy 2.5.3, pandas 3.0.6, pytest 9.1.1; doğruladım): tek ortam. `pyproject.toml`'da bağımlılık listesi yok. Karar: bir kez `pip freeze` çıktısı `requirements.txt`'e yazılır.

**14-090** — KARAR — CI yok. Garanti: AGENTS.md'ye bir satır, "commit öncesi `pytest -q` yeşil olmalı". Pre-commit kancası yok (kanca `.git` içinde, sürümlenmez).

**14-091** — KARAR — AGENTS.md kuralı: testleri gevşetmek (assert silme, tolerans büyütme, `skip`/`xfail`) yasak. Test dosyası değişen her commit ikinci oturumda `git diff tests/` ile incelenir.

**14-092** — KARAR — Kırmızı kanıt git geçmişindedir: önce "test (kırmızı)" commit'i, sonra "kod" commit'i. Yerel git var (3 commit, doğruladım).

**14-093** — KARAR — Modül başına bir dosya: `test_adim.py`, `test_motor.py`, `test_simulator.py`… `test_nabiz_veri.py` bölünür: nabız → `test_nabiz.py`, `temizle` testleri silinir (14-004).

**14-094** — KARAR — Nabız testleri kalır (etiket TAM_ALIM / BEKLE / DIKKATLI, girdiye göre sabit). SMA 18/35 – 20/50 çelişkisi: hangisi seçilirse tek bir sınır testi yazılır; kodun şimdi hangisini kullandığını doğrulamadım.

**14-095** — KARAR — Evet: girdi hisse/sütun sırası karıştırılıp aynı işlem listesi beklenir (14-029 ile aynı test).

**14-096** — KARAR — Tek uygulama (14-038: rastgele kural aynı Motor'dan geçer). 1 Motor testi: açık pozisyonda gelen sinyal sayılmaz.

**14-097** — KARAR — Evet, 2 test: aynı tohum aynı ızgara; 2×2 ızgarada 3 pozitif hücre → oran 0,75 (elle).

**14-098** — KARAR — Sentetik: testin içinde gömülü liste. Gerçek kesim: `tests/veri/` altında ≤ 30 satırlık CSV (`pandas.read_csv`, ek bağımlılık yok); Levent açıp okuyabilir.

**14-099** — KARAR — Test adı Türkçe ve kural atfı içerir. Motor ve Simülatör testlerinde `assert x == y, f"§5.3 stop önce: beklenen {y}, gerçek {x}"`; diğerlerinde pytest'in kendi farkı yeter.

**14-100** — KARAR — TASARIM §5.3'e tarihli bir "Test yeterlilik ölçütü" paragrafı yazılır: 11 motor durumu, sadakat, pozitif kontrol, look-ahead, 5.12 sınırları, paket < 60 sn. Değişirse tarihli kayıt düşülür (kural kaydı gibi).

## Özet

Verdict sayıları: CEVAPLI 0, KARAR 92, YANLIŞ 3, OLGU 2, ZAYIF SORU 3 (toplam 100).

En önemli 10 karar:

1. Test yüzleri (seam): Adım, Motor, Maliyet, Simülatör, İstatistik+Holm, Takvim, Evren, olay düzeltmesi, Aile, Rapor. Her modül için bir test dosyası; iç yardımcı sınanmaz (14-001, 14-093).
2. Motor durumları 7'den 11'e çıkar: giriş günü stop, giriş günü stop+hedef, sinyal sonrası veri yok, açık pozisyonda yeni sinyal (14-005). Kenarlar tam eşitlik ve katı < ile ayrı test (14-008, 14-009).
3. Elle hesap testin içinde, Türkçe yorumla; hesabı yazan ajan kodu yazan olmaz, ikinci oturum kodu görmeden hesaplar (14-006, 14-007, 14-077).
4. Testte sabit literal; uygulamadan `MASRAF` içe aktarma yasak. `test_kanit.py` iki vectorbt testi silinir, `temizle` testleri silinir (14-004, 14-078).
5. `tests/conftest.py` autouse: ağ soketi engeli ve günlük yolunun `tmp_path`'e yönlenmesi; yeni eklenti yok (14-014, 14-052).
6. İstemciler `getir` parametresiyle verilir, testte elle sahte; cassette yok. Şema kontrolü çalışma zamanında (14-015, 14-017).
7. Ortak look-ahead testi: tek parametrik test, t'de kesilmiş veriyle aynı çıktı; evren, ATR, göstergeler, aileler, çift seçimi (14-024, 14-025, 14-061).
8. Altın dosya, Hypothesis, mutasyon testi, coverage hedefi, CI yok. Hypothesis, coverage, mutmut kurulu değil; ölçü davranış listesi (14-066 – 14-075, 14-079 – 14-081, 14-090).
9. Rastgelelik: sabit tohum, literal p beklenmez, özellik ve aralık sınanır; kapsama ve yanlış-pozitif ölçümü paket dışı (14-040 – 14-043, 14-049). Holm elle: [0,01; 0,04; 0,03; 0,005] → [0,03; 0,06; 0,06; 0,02] (14-045).
10. Disiplin: paket < 60 sn (şimdi 6,1 sn), AGENTS.md'ye "commit öncesi pytest yeşil, testi gevşetme yasak, kırmızı commit önce"; yeterlilik ölçütü TASARIM §5.3'e tarihli yazılır; Levent yalnız "N passed" satırını okur (14-086, 14-088, 14-090 – 14-092, 14-100).

Test edilecek yüzler listesi: Adım, Motor, Maliyet, Simülatör (tek hisse + çift, ayrı), İstatistik (blok yeniden örnekleme, p, Holm, 5.12 karar), Takvim, Evren, olay düzeltmesi + karantina + limit(tarih), Aile (3), Rapor, kural kaydı + hash, sadakat.
