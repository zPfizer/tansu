# Cevaplar 16: Koşu, zamanlama, günlük

Doğrulanan olgular (venv, `-c` ve `pip list` ile): Python 3.14.7; `tzdata` 2026.5 kurulu ve `ZoneInfo('Europe/Istanbul')` açılıyor; `typer` 0.27.2, `requests`, `pyarrow`, `borsapy` 0.11.0 kurulu; `holidays`, `exchange_calendars`, `tenacity`, `portalocker`, `loguru`, `streamlit` kurulu DEĞİL; `pyproject.toml` yalnız pytest ayarı içeriyor; TANSU klasörü OneDrive altında değil (`C:\Users\levent\Desktop`); `borsapy` istekleri 30 sn zaman aşımlı, yeniden deneme koduna rastlanmadı.

Ortak karar çerçevesi (aşağıdaki cevaplar buna dayanır): tek giriş `python -m tansu <altkomut>` (argparse); altkomutlar `gunluk`, `sinama`, `sadakat`, `kayit`; Levent hiçbirini elle yazmaz, yalnız `gunluk` zamanlayıcıdan çalışır; tek görünür işaret `rapor\durum.txt`; günlük `gunluk\YYYY-MM-DD.log`; tüm yazmalar "geçici dosyaya yaz, `os.replace`"; kilit yok.

## A. Komut satırı biçimi

**16-001** — KARAR — Tek paket, tek giriş: `python -m tansu gunluk | sinama | sadakat | kayit`. `tansu\__main__.py` argparse alt komutlarını dağıtır; rapor `sinama` ve `gunluk` içinde üretilir, ayrı komut değil.

**16-002** — KARAR — `-m` biçimi. Görev `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe -m tansu gunluk` çağırır. Kurulu `tansu` komutu ve `.bat` gerekmez; `-m` mevcut `rapor.py` ile aynı yoldur, ek dosya sıfırdır.

**16-003** — KARAR — argparse (stdlib). Bağımlılık eklenmez, Windows riski sıfır. `typer` kurulu ama pyproject'te yok; dört alt komut için gereksiz.

**16-004** — YANLIŞ — pyproject'te `[project]` yok, kurulum yeniden üretilemez (`pyproject.toml` yalnız pytest ayarı). Düzeltme: `[project]` ile `name`, `requires-python`, `dependencies` (pandas, pyarrow, numpy, requests, borsapy, pandas-ta-classic, statsmodels, quantstats, tzdata) eklenir; `[project.scripts]` eklenmez. Yeniden kurulum: `python -m venv .venv` sonra `.venv\Scripts\pip install -e .`.

**16-005** — KARAR — Aynı çalıştırılabilir, ama `sinama` yalnız elle çalışır ve görev yalnız `gunluk` çağırır. Yanlışlıkla başlatmayı önleyen şey: Levent `sinama` yazmaz (16-006); ek koruma yok.

**16-006** — KARAR — Levent'in elle yazacağı komut sıfır. Belgelenen şey tek satır: "akşam `rapor\durum.txt` dosyasını aç". `sinama`, `sadakat`, `kayit` Levent ile birlikte (Claude oturumunda) çalıştırılır. Toplam 4 alt komut kabul edilebilir.

**16-007** — KARAR — Tek adım (`gunluk` hepsini yapar). Beş adım ayrı komut olmaz. Yeniden çalıştırma yolu: aynı komutu tekrar çalıştırmak; koşu idempotent (16-035) olduğu için kalan işi tamamlar.

**16-008** — KARAR — `gunluk` bayrak almaz. `sinama` yalnız `--son` alır (1.000 tekrar; bayraksız 200, §5.7). `--tarih`, `--kuru`, `--zorla`, `--ayrıntılı` eklenmez; `--tarih` ancak geçmiş bir günü yeniden üretme ihtiyacı doğarsa eklenir.

**16-009** — CEVAPLI — Kodda sabit. `veri.py` ve `rapor.py` `Path(__file__).resolve().parent.parent` kullanır; mutlak yoldur, çalışma dizininden bağımsızdır, zamanlayıcı altında çalışır. Depo taşınırsa yollar onunla taşınır (yalnız `.venv` yeniden kurulur). TOML ve ortam değişkeni eklenmez; saat zamanlayıcı XML'inde durur.

**16-010** — KARAR — Günlük dosyasına yazılır; `print` kalkar. Konsol yalnız `sinama`/`sadakat` ilerlemesi için `logging`'in konsol çıktısıdır. `rapor.py` içindeki `print(yol)` günlük satırı olur.

## B. Windows Görev Zamanlayıcı

**16-011** — KARAR — 19:30 başlangıç değeridir. İş Yatırım yayın saati (§8.7) ilk iki haftanın günlüğünden okunur: `gunluk` her denemede "son çubuk tarihi" ve saati yazar. Değişiklik: XML'deki `StartBoundary` düzenlenip `schtasks /create /xml /f` ile yeniden yüklenir. Yeniden deneme (16-033) belirsizliği zaten kapatır.

**16-012** — KARAR — "Yalnız kullanıcı oturum açıkken çalıştır" (parola yok). Levent parola saklama kurmaz; oturum kapalıysa `StartWhenAvailable` (16-023) oturum açılınca çalıştırır.

**16-013** — KARAR — `WakeToRun` kapalı. Uyku 19:30'u kaçırırsa `StartWhenAvailable` uyanışta çalıştırır; yeniden deneme tetikleyicisi (16-033) ağ gelene kadar tekrarlar. Uyandırma izni dizüstünde pil riski getirir, gerekmez.

**16-014** — KARAR — Görev tanımı repoda `kurulum\tansu-gunluk.xml` dosyasıdır; kalıcı bileşen olduğu için dosya gerekçelidir. Kurulum ya da geri getirme tek komut: `schtasks /create /tn TansuGunluk /xml kurulum\tansu-gunluk.xml`.

**16-015** — KARAR — `.venv\Scripts\python.exe` mutlak yolu (`py` başlatıcısı venv paketlerini görmez). `.venv` silinirse görev başlamaz; `durum.txt` güncellenmez; Levent bunu dosyadaki tarihten görür (16-071). Kontrol yok, ek izleyici yok.

**16-016** — KARAR — XML'de `WorkingDirectory` = depo kökü. Kod zaten dosya konumundan mutlak yol türetir (16-009); göreli yol kullanılmaz. System32 riski kuralla kapanır: koda göreli yol yazılmaz.

**16-017** — KARAR — `MultipleInstancesPolicy = IgnoreNew`. Kilit yok (16-045), çakışma sorunu yok.

**16-018** — KARAR — `ExecutionTimeLimit = PT1H`. Neye göre: 100 sembol indirme, 30 sn zaman aşımı; normal koşu birkaç dakika sürmeli (ilk koşu ölçülür, süre sonra 3 katına ayarlanır). Takılı koşu 1 saatte ölür, sonraki akşam engellenmez.

**16-019** — KARAR — Görev Zamanlayıcı geçmişine güvenilmez. Kanıt `durum.txt` (içindeki koşu zamanı) ve günlük dosyasıdır. Geçmişi açmak yönetici hakkı ister; gerekmez.

**16-020** — KARAR — Aynı hesap (16-012 "oturum açıkken" bunu zaten zorlar). Farklı hesap olmadığı için izin ve önbellek sorunu doğmaz.

**16-021** — ZAYIF SORU — Yeniden başlatma, görevin kaçırılması ile aynıdır ve `StartWhenAvailable` bunu kapsar. Günlükteki başlama saati (19:30'dan geç) ayrımı yeterince gösterir; ayrı işaret gerekmez.

**16-022** — KARAR — Öncelik ayarı yok. `gunluk` birkaç dakikalık IO işidir; `sinama` ile çakışırsa yavaşlar ama bozulmaz. Levent `sinama`yı 19:30–20:30 arası başlatmaz (Claude oturumu bunu bilir).

## C. Kaçırılan koşular ve telafi

**16-023** — KARAR — `StartWhenAvailable = true`. Sabah 09:00'da çalışan koşu İş Yatırım'dan tam geçmişi indirir; "bugünkü veri" = son çubuğun tarihi. Çubuk önceki işlem günüyse §5.1 gereği yeni kart üretilmez (16-024), ama açık kartlar güncellenir.

**16-024** — CEVAPLI — §5.1: "son çubuğun tarihi bugün değilse o gün kart üretilmez." Geç koşuda da bugünün çubuğu yoksa kart yok. Kaçırılan gün kalıcı "kart yok"tur: giriş ertesi AOF'ta olurdu, geç çalışınca işlem yapılamaz.

**16-025** — KARAR — Telafi kart üretmez, yalnız açık kartlar yetişir. Tam geçmiş her koşuda indirildiği için "N gün" ayarı yok; Adım, kartın `son_islenen_tarih` değerinden sonraki bütün mumları sırayla işler.

**16-026** — KARAR — Evet, sırayla. Kart dosyası her kart için `son_islenen_tarih` tutar; Adım o tarihten sonraki her mumu gün gün uygular. Stop/hedef aradaki bir günde değdiyse kart o günün mum tarihiyle kapanır, koşu tarihiyle değil.

**16-027** — KARAR — Tanım: `gunluk\` altında o işlem günü için "TAMAM" satırı olmayan işlem günü (işlem günleri XU100 çubuklarından, 16-085). Kayıt: `rapor\durum.txt` değil, `gunluk\kosular.csv` (tarih, sonuç, son çubuk), eklemeli.

**16-028** — KARAR — `durum.txt` ilk satırda: "ESKİ: son başarılı koşu 2026-09-28, 5 işlem günü kaçırıldı". Kartlar yetişmiş olarak gösterilir; kaçırılan günler için kart yoktur.

**16-029** — KARAR — Kaçırılan günler döneme sayılmaz; dönem "6 ay ve 30 işlem" kuralına göre uzar. Üst sınır: kaçırılan gün oranı dönemin %10'unu aşarsa dönem sonuçta uyarıyla işaretlenir, geçersiz sayılmaz.

**16-030** — KARAR — Evet. Rapor, kaçırılan günleri ve o günlerde Adım'ın üreteceği sinyalleri (geriye dönük hesaplanır, işlem sayılmaz) "veri deliği" olarak listeler. Kaynak: `kosular.csv`.

**16-031** — CEVAPLI — Kaynak her koşuda 2015'ten itibaren tam geçmişi verir (`veri.py` `BASLANGIC`); eksik gün aralığı hesaplanmaz. Anlık görüntü kuralı: yeni gün yeni anlık görüntü; eskisi değişmez (16-037).

**16-032** — KARAR — Ayrım yok. Tek tanım: koşu çalıştı ya da çalışmadı. Rapor yalnız koşu zamanını yazar; "telafi/yeniden koşu" ayrı tür olarak izlenmez.

**16-033** — KARAR — Evet. Görev tetikleyicisi 19:30'da başlar ve 60 dakikada bir 4 saat tekrarlar (19:30, 20:30, 21:30, 22:30, 23:30). Koşu başlar başlamaz `kosular.csv`'de bugün "TAMAM" varsa hiçbir şey yapmadan çıkar. Bu, 16-011, 16-097 ve 16-099'u birlikte çözer.

**16-034** — KARAR — Telafiyi Görev Zamanlayıcı yapar (`StartWhenAvailable` + tekrarlı tetikleyici). Kodda "kaçırılan günü bul" mantığı yok; yalnız `kosular.csv` kontrolü. Yasakla çelişmez.

## D. Tekrar koşulabilirlik (idempotans)

**16-035** — KARAR — İkinci koşu o gün için "TAMAM" varsa hiçbir şey yapmadan çıkar. CSV üzerine yazılmaz. Davranış `tansu\__main__.py` içinde bir `if` ve bir testle durur.

**16-036** — KARAR — Evet, hep: `.tmp` dosyasına yaz, `os.replace` ile adlandır. 3 satırlık yardımcı; tek yerde (`yaz()`) bulunur; parquet ve CSV ve `durum.txt` için kullanılır.

**16-037** — KARAR — Hayır. Yalnız TAMAM'dan önceki ilk geçerli anlık görüntü kayıtlıdır; `gunluk` aynı gün ikinci kez anlık görüntü yaratmaz (16-035). Deneme günlüğü anlık görüntüyü klasör adıyla (tarih) anar.

**16-038** — YANLIŞ — `veri.py` satır `yol.stat().st_mtime == today` dosya zamanına bağlı; kopyalama ya da saat farkında yanılır. Düzeltme: "bugün indirildi" = `kosular.csv`'de bugün için TAMAM, ya da anlık görüntünün son çubuk tarihi. Dosya zamanı kullanılmaz. (`veri.py` zaten §7.1'de yeniden yazılacak, Yahoo'lu.)

**16-039** — KARAR — Hayır, çünkü ikinci koşu çıkar (16-035) ve Adım `son_islenen_tarih` sonrası mumları işler. Sınama: aynı gün iki kez `gunluk` çalıştır, kart dosyası bayt bayt aynı kalsın.

**16-040** — KARAR — Rapor adı `kanit-YYYYMMDD-HHMM.md`. Deneme günlüğündeki her satır rapor dosya adını taşır; hiçbir kayıt kanıtsız kalmaz.

**16-041** — KARAR — Evet, eklemeli (`rapor\deneme-gunlugu.csv`, `open(..., "a")`). Holm anahtarı (aile, varyant, parametre) olduğu için aynı anahtar için yarıda kalan ve yeniden başlayan koşu tek deneme sayılır (en son tamamlanan satır geçerli). Bu, sorgu-2 #45 ile uyumlu.

**16-042** — ZAYIF SORU — Yeniden koşu zararsız olduğu için kuru koşu gereksiz. Zararsızlığı 16-039'daki test kanıtlar.

**16-043** — KARAR — Hayır, geri alma yok. Ama indirme önce `veri\gecici\` klasörüne gider; yalnız tazelik ve kalite geçerse anlık görüntü klasörüne `os.replace` ile taşınır. Geçmezse depoya hiçbir şey girmez.

**16-044** — KARAR — Ayrı komut: `python -m tansu kayit`. Dosya `open(..., "x")` ile açılır; varsa hata verir ve değiştirmez. Yan etki değildir.

## E. Koşu kilidi

**16-045** — YANLIŞ — Kilit gerekmez; "kilit olmasa neyin bozulacağı" gösterilmedi ve tek kişi tek makinede zararı yok. Düzeltme: kilit yok. Çakışma `IgnoreNew` (zamanlayıcı kopyası) + `os.replace` (yarım dosya yok) ile kapanır; elle koşu + görev çakışması en kötü ihtimalde aynı veriyi iki kez yazar.

**16-046** — ZAYIF SORU — Kilit yok (16-045). Gerekirse `msvcrt.locking` (stdlib, süreç ölünce otomatik kalkar); portalocker eklenmez.

**16-047** — ZAYIF SORU — Kilit yok, bayat kilit yok.

**16-048** — ZAYIF SORU — Kilit yok. `sinama` ve `gunluk` aynı anda çalışabilir; `gunluk` yalnız yeni anlık görüntüyü `os.replace` ile ekler, `sinama` seçtiği anlık görüntüyü okur.

**16-049** — ZAYIF SORU — Kilit yok; "alınamadı" çıkış kodu da yok.

**16-050** — CEVAPLI — Okuyucu koruması `os.replace` atomikliğiyle sağlanır (16-036): okuyucu ya eski ya yeni dosyayı görür. Streamlit bu ortamda kurulu değil (doğruladım), ekran henüz yok.

**16-051** — ZAYIF SORU — Çok işlemli K1 tasarımda yok (§5.7 numpy), kilit yok.

**16-052** — ZAYIF SORU — Tek kişi tek makine varsayımı kilidi gereksiz kılar. OneDrive olasılığı: `C:\Users\levent\Desktop` OneDrive altında değil (doğruladım). Yine de depo OneDrive'a taşınırsa parquet senkron çakışması olur; kural: depo OneDrive altına konmaz.

## F. Günlük kaydı (log)

**16-053** — KARAR — Standart `logging`. Çatışmada "asgari altyapı" önceliklidir; loguru kurulu değil.

**16-054** — KARAR — Yeni `gunluk\` klasörü. Levent'in baktığı tek yer `rapor\durum.txt`; ayrıntı için `gunluk\` yazıldığı `durum.txt` son satırında anılır.

**16-055** — KARAR — Koşu günü başına ayrı dosya: `gunluk\YYYY-MM-DD.log` (`FileHandler`, `encoding="utf-8"`). Döndürme yok; dosya adı tarih olduğu için "bir akşamın kaydı" tek dosyadır.

**16-056** — KARAR — Silme yok. Düz metin, günde birkaç KB; 6 ay yaklaşık 1 MB'ın altında olur (tahmin, ölçülmedi). Disk sorunu doğarsa 1 yıldan eski dosyalar elle silinir.

**16-057** — ZAYIF SORU — `TimedRotatingFileHandler` kullanılmaz (16-055); `PermissionError` kaynağı yok. Elle koşu aynı gün aynı dosyaya ekler (`mode="a"`).

**16-058** — KARAR — Düz metin: `2026-10-05 19:34:02 UYARI SEMBOL ...`. JSON Not Defteri'nde okunmaz.

**16-059** — KARAR — Koşu başında tek satır: kod sürümü (git hash varsa), Python sürümü, anlık görüntü tarihi, İstanbul saati. Kütüphane sürümleri yalnız `sinama` günlüğüne. Deneme günlüğü bilimsel kayıt (aile, parametre, hash, anlık görüntü); koşu günlüğü işletimseldir.

**16-060** — KARAR — Ayrı yerlerde: `gunluk\` işletim, `rapor\deneme-gunlugu.csv` bilimsel. Döndürme yapılmadığı için silme riski doğmaz, ama ayrı dosya tutmak asıl güvencedir.

**16-061** — KARAR — Kütüphane uyarıları `logging.captureWarnings(True)` ile günlüğe düşer. `print` yapan kütüphane için `contextlib.redirect_stdout` kullanılmaz; python.exe (konsol) kullanıldığından çıktı kaybı yalnız görünür pencerede olur, kritik bilgi değil.

**16-062** — KARAR — Görev `python.exe` çağırır (`pythonw.exe` değil). `__main__.py` en üst seviyede `try/except Exception: logging.exception(...); sys.exit(1)` içerir; traceback günlüğe yazılır. `sys.excepthook` gerekmez.

**16-063** — KARAR — BİLGİ: normal akış. UYARI: sembol karantinası, indirilemeyen sembol, çapraz kontrolsüz veri. HATA: tazelik ya da kalite eşiği geçmedi, yakalanmayan istisna. Karantina UYARI.

**16-064** — KARAR — `FileHandler(..., encoding="utf-8")` ve `durum.txt` yazımında `encoding="utf-8"`. Konsol ayarı gerekmez (Levent konsolu görmez). Mevcut `rapor.py` zaten `encoding="utf-8"` kullanıyor.

**16-065** — KARAR — Günlükte sembol listesi ve sayısal sonuçlar olacak; pozisyon ya da hesap bilgisi yok (sistem emir vermez, Levent'in portföyünü bilmez). Paylaşım yapılmayacağı için ayrı gözden geçirme yok.

**16-066** — KARAR — `sinama` günlüğe yalnız ailede ve her 100 tekrarda bir satır yazar (100 hisse × 3 aile × 1.000 tekrar için en çok 30 satır). Kontrolsüz büyüme yok.

## G. Çıkış kodları ve başarısızlığın görünürlüğü

**16-067** — KARAR — Tek kanal: `rapor\durum.txt`. İlk satır TAMAM ya da SORUNLU. Bildirim yok (§3 "Telegram yok" ile uyumlu); sorgu-2 #48 aynı kararı verir. Levent akşam dosyayı açar.

**16-068** — KARAR — Çıkış kodu: 0 = koşu kuralına göre bitti (kart üretilmedi dahil), 1 = beklenmeyen istisna. Başka kod yok; Görev Zamanlayıcı yalnız "son sonuç" gösterir ve Levent oraya bakmaz.

**16-069** — KARAR — "Veri bayat, kart yok" doğru davranıştır (çıkış 0) ama `durum.txt` ilk satırı SORUNLU olur. Ayrım `durum.txt` içindedir, çıkış kodunda değil.

**16-070** — KARAR — Dört durum için tek dosya: `durum.txt`. İlk satır beş değerden biri: `TAMAM ... N kart`, `TAMAM ... sinyal yok`, `SORUNLU veri bayat`, `SORUNLU kalite`, `BUGÜN ÇUBUK YOK (tatil olabilir)`. "Koşu hiç çalışmadı" = dosyadaki tarih eski.

**16-071** — KARAR — `durum.txt` ilk satırında son başarılı koşunun tarihi ve saati yazar. Kanıt ekranı (Streamlit, sonra) tarih 1 işlem gününden eskiyse kırmızı gösterir.

**16-072** — CEVAPLI — Zaman aşımı kararı verildi: istek başına 30 sn (borsapy zaten 30 sn) ve görev `PT1H` (16-018). Donma bu ikisiyle bitirilir; ayrı donma tespiti yok.

**16-073** — KARAR — Dosya. SMTP, Telegram, toast ve parola gerektiren her kanal elenir; kapsam §3.

**16-074** — ZAYIF SORU — Bildirim yok (16-067); "okunmaz hâle gelme" sorunu doğmaz.

**16-075** — KARAR — Evet: `durum.txt` ilk satırı Türkçe ve eylemli: "SORUNLU veri bayat: 21:30'da yeniden denenecek" ya da "SORUNLU kalite: 7 sembol eksik, Claude'a göster".

**16-076** — KARAR — Eşik: indirilemeyen sembol sayısı 100'ün %5'ini (5) aşarsa SORUNLU, kart yok. 5 ve altı: kartlar üretilir, eksik semboller `durum.txt` ve günlükte listelenir. Eşik §5.1'e eklenir (YORUM, ilk haftada gözden geçirilir).

## H. Saat dilimi ve yaz saati

**16-077** — KARAR — Kodda `ZoneInfo("Europe/Istanbul")`. `tzdata` kurulu (doğruladım, 2026.5) ve `ZoneInfo('Europe/Istanbul')` açılıyor; pyproject bağımlılığına eklenir. Windows saati yanlışsa 19:30 görevi yanlış saatte çalışır; Levent seyahatte değil, kural: saat dilimi (UTC+03) değiştirilmez.

**16-078** — KARAR — Görev yerel saate göre çalışır. "Bugün" İstanbul saatinden türetilir; böylece yurt dışında da işlem günü kararı doğru kalır, yalnız görevin saati kayar.

**16-079** — KARAR — Evet: `bugun() = datetime.now(ZoneInfo("Europe/Istanbul")).date()`; `dt.date.today()` kalkar. Makine saati yanlışsa tazelik "son çubuk tarihi = bugün" yanlış karar verir; koruma yok (tek makine, Windows saat eşitlemesi açık).

**16-080** — KARAR — Çubuk tarihleri saatsiz tarih (naive, gün); kayıt zaman damgaları İstanbul saati ve `+03:00` ofsetli ISO metin. Parquet'te saatli sütun yok.

**16-081** — KARAR — Normalleştirme `veri.py` içinde, indirme katmanında: indeks `normalize()` ve saat dilimi bilgisi atılır; sonrası yalnız tarih. Başka katmanda saat dilimi görülmez.

**16-082** — ZAYIF SORU — Günlük çubuk yalnız tarihtir; 2015–2016 yaz saati tarihi etkilemez.

**16-083** — CEVAPLI — `tzdata` kurulu (doğruladım) ve 16-077'de pyproject'e eklenir. Sabit sapma gerekmez.

**16-084** — KARAR — Bağlantı yok ve gerekmez. 19:30 yalnız görev saatidir; tazelik kontrolü saate değil "son çubuk tarihi = bugün" koşuluna bakar (§5.1). Seans saati koda yazılmaz.

## I. Tatiller ve yarım günler

**16-085** — YANLIŞ — §4 "BIST tatilleri, yarım günler" tablosu fazla; `holidays` ve `exchange_calendars` kurulu değil (doğruladım). Düzeltme: Takvim = İş Yatırım XU100 çubuk tarihleri (sorgu-2 #15 zaten böyle diyor). Elle tatil listesi yok.

**16-086** — ZAYIF SORU — Tatil listesi yok (16-085). Tatil gününde bugünün çubuğu olmaz; koşu kart üretmez ve `durum.txt` "BUGÜN ÇUBUK YOK" yazar.

**16-087** — ZAYIF SORU — Köprü ve idari izin günleri de çubuk olmaması olarak görünür; ayrı güncelleme yok.

**16-088** — KARAR — Yarım gün normal gün sayılır. Hacim olağandışı kontrolü (§5.1) çok düşük hacimli yarım günü eleyebilir; bu kabul edilen kayıp, ayrıca kural eklenmez. Sınama yarım günleri normal sayar.

**16-089** — CEVAPLI — Tatilde çubuk yok; `gunluk` "BUGÜN ÇUBUK YOK" yazar (16-070) ve çıkış 0. Bu "sinyal yok"tan ayrı bir durum satırıdır.

**16-090** — CEVAPLI — Tarihsel "işlem günü" = fiyat verisindeki XU100 günleri (sorgu-2 #15). 2020 Mart gibi duruşlar bu yolla doğru çıkar.

**16-091** — KARAR — Ayırt edilmez; ikisi de "çubuk yok". Yetkili kaynak XU100 endeks çubuğudur: endeks çubuğu var, hisse çubuğu yoksa o hissede veri eksikliği (karantina/indirilemeyen sembol); endeks çubuğu da yoksa tatil.

**16-092** — KARAR — Tetikleyici yalnız Pazartesi–Cuma. Hafta sonu çubuk olmadığı için açık kart güncellemesi gerekmez; kaçırılan Cuma koşusu Pazartesi sabahı `StartWhenAvailable` ile yakalanır (16-023).

## J. Ağ hataları ve yeniden deneme

**16-093** — KARAR — Zaman aşımı 30 sn; sembol başına en çok 2 deneme, aralarında 5 sn. Hız sınırı bilinmiyor (§8.1); istek sayısı küçük (100 sembol), toplam hız artışı ihmal edilir.

**16-094** — KARAR — Elle 3 satırlık döngü; `tenacity` kurulu değil. `borsapy` içinde yeniden deneme koduna rastlanmadı (grep ile baktım), katman çarpanı yok. Asıl yeniden deneme tetikleyici tekrarıdır (16-033).

**16-095** — KARAR — Sembol atlanır, koşu devam eder (eşik 16-076). Eksik semboller `durum.txt` ikinci satırında listelenir.

**16-096** — OLGU — İş Yatırım'ın gün içi geçici veri yayınlayıp yayınlamadığı doğrulanmadı (ağ ölçümü gerekir). Önlem: koşu saati 19:30 sonrasıdır, seans 18:00'de kapanır; ertesi günkü koşu önceki anlık görüntüyle karşılaştırır ve fark varsa UYARI yazar (yeni anlık görüntüyü kabul eder, eskiyi silmez).

**16-097** — KARAR — Ayrı bekleme yok. İlk deneme ağ yokluğundan başarısız olursa görev `RunOnlyIfNetworkAvailable` ile bekler, tekrarlı tetikleyici bir saat sonra yeniden dener (16-033).

**16-098** — KARAR — Şema doğrulaması `veri.py` içinde indirmeden hemen sonra: beklenen sütunlar var mı, tipler sayısal mı. Başarısızsa SORUNLU, anlık görüntü yazılmaz (16-043).

**16-099** — KARAR — Evet, çapraz kontrolsüz devam eder. Günlük UYARI ve `durum.txt` ikinci satırı "çapraz kontrol yok"; kartlara sütun eklenmez.

## K. Sınama koşusu ile günlük koşu ayrımı

**16-100** — KARAR — Günlük koşu deneme günlüğüne yazmaz. Yalnız `sinama` (aile, varyant, parametre) denemesi yazar; Holm yalnız bunları sayar (sorgu-2 #45). Rutin koşu deneme sayısını şişirmez.

## Özet

Doğrulama sayıları (100 soru):

| Karar türü | Sayı |
|---|---|
| CEVAPLI | 8 |
| KARAR | 74 |
| YANLIŞ | 4 |
| OLGU | 1 |
| ZAYIF SORU | 13 |

Sayılar dosyadaki satırlardan `grep -c` ile sayıldı. YANLIŞ = 16-004, 038, 045, 085. OLGU = 16-096.

En önemli 10 kurulum kararı:

1. Görev tanımı `kurulum\tansu-gunluk.xml` dosyasında; kurulum `schtasks /create /tn TansuGunluk /xml ...` tek komutudur (16-014).
2. Görev ayarları: Pazartesi–Cuma 19:30, her 60 dakikada tekrar, 4 saat; `StartWhenAvailable=true`; `WakeToRun=false`; `IgnoreNew`; `ExecutionTimeLimit=PT1H`; yalnız oturum açıkken çalış, parola yok (16-012, 013, 017, 018, 033).
3. Komut: `.venv\Scripts\python.exe -m tansu gunluk`, başlangıç yeri depo kökü, argparse, bayraksız (16-001, 002, 003, 008).
4. pyproject'e `[project]` ve `dependencies` (tzdata dahil) eklenir; yeniden kurulum `python -m venv .venv` + `pip install -e .` (16-004, 083).
5. Kilit yok. Çakışmayı `IgnoreNew` ve her yazmada geçici dosya + `os.replace` önler (16-036, 045).
6. Tek görünür işaret `rapor\durum.txt`: ilk satır TAMAM/SORUNLU/BUGÜN ÇUBUK YOK, son başarılı koşu zamanı, Türkçe eylem cümlesi; bildirim kanalı yok (16-067, 070, 071, 075).
7. Idempotans: `kosular.csv`'de bugün TAMAM varsa koşu hemen çıkar; "bugün indirildi" dosya zamanından değil bu kayıttan okunur (`veri.py` `st_mtime` kalkar); indirme önce `veri\gecici\`'ne, tazelik ve kalite geçerse anlık görüntüye taşınır (16-035, 038, 043).
8. Kaçırılan gün: kart üretilmez, açık kartlar `son_islenen_tarih`'ten sonraki mumları sırayla işler; veri deliği günleri raporda listelenir (16-024, 026, 029, 030).
9. Eksik sembol eşiği: 100'ün %5'inden fazlası (5'ten çok) indirilemezse SORUNLU ve kart yok; sembol başına 30 sn zaman aşımı, 2 deneme, 5 sn bekleme; elle döngü (16-076, 093, 094).
10. Günlük: stdlib `logging`, `gunluk\YYYY-MM-DD.log`, düz metin, utf-8, döndürme ve silme yok; Takvim = XU100 çubuk tarihleri (elle tatil listesi yok); "bugün" = `ZoneInfo("Europe/Istanbul")` tarihi; günlük koşu deneme günlüğüne yazmaz (16-053, 055, 079, 085, 100).
