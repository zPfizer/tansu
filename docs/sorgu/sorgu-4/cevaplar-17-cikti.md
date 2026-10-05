# Cevaplar 17: Rapor, kart, ekran

Doğrulanan olgular (venv, `pip list` ve `-c`): streamlit, quantstats ve jinja2 kurulu DEĞİL. Kurulu: pandas 3.0.6, matplotlib 3.11.2, plotly 7.1.0, tabulate 0.10.0 (`to_markdown` çalışıyor), markdown-it-py 4.2.0 (`table` kuralıyla HTML üretiyor), openpyxl, pyarrow. `pyproject.toml` yalnız pytest ayarı içeriyor. `rapor/` git'te izleniyor, `.gitignore`'da yok. `utf-8-sig` ile okunan BOM'lu `;` ayraçlı CSV'de ilk sütun adı temiz geliyor.

Ana karar: çıktı katmanı = markdown + HTML rapor, `;` ayraçlı CSV kart, SQLite durum deposu. Streamlit, quantstats ve plotly yok.

**17-001** — YANLIŞ — §3 aynı cümlede Streamlit ekranını hem ekler hem "gereksiz katman" sayar. Streamlit ilk sürümden çıkar. Raporun HTML hali Kanıt ekranının işini görür.
**17-002** — KARAR — Tarayıcı. Rapor `.html` olarak yazılır, çift tıklayınca açılır. `.md` kaynak olarak yanında kalır.
**17-003** — YANLIŞ — §3 yalnız "markdown" der, okuma biçimi seçilmemiş. Karar: HTML. `markdown_it` kurulu, yeni bağımlılık yok. PDF gereksiz.
**17-004** — KARAR — f-string kalır, tablolar `DataFrame.to_markdown` ile (tabulate kurulu). Jinja2 kurulu değil, eklenmez.
**17-005** — KARAR — Rakam tek yerde hesaplanır (`kanit`/istatistik). Rapor yalnız biçimler. Biçim işi tek yardımcıda (yüzde, TL). Şablon olmadığı için ikinci hesap yeri doğmaz.
**17-006** — KARAR — Yeni dosya: `kanit-YYYYMMDD-HHMM.md`. Üstüne yazılmaz. Deneme günlüğü (§5.11) her koşuyu zaten ayrı satır tutar, dosya adı o satırla eşleşir.
**17-007** — KARAR — Raporun başlık bloğunda (ilk 5 satır): koşu kimliği, veri anlık görüntü tarihi, kod hash'i. Tablolarda tekrar edilmez, bir rapor = bir koşu.
**17-008** — KARAR — Evet, ilk satır. Cümle `rapor.py`'de tek sabit/fonksiyon: "Hiçbir aile kabul ölçütünü geçmedi (0/3)." §5.12 sonucundan üretilir. Tanımın kaynağı TASARIM §1.
**17-009** — KARAR — İlk okunan: "Geçen aile: n/3". İlk ekranda 3 rakam: geçen aile sayısı, kâğıt üstü dönem (gün ve işlem sayısı), veri tarihi.
**17-010** — KARAR — Cümle tek kurala bağlanır: %95 aralık sıfırı içeriyorsa "ayırt edilemiyor". p, Holm p, saptanabilecek en küçük etki "Ayrıntı" bölümünde kalır.
**17-011** — KARAR — "±" yazılmaz. Format: "−%0,2 (%95 aralık −%2,4 ile +%2,0)". §6.4 örneği bu biçime düzeltilir. Aralık §5.9 blok yeniden örneklemesinden gelir.
**17-012** — KARAR — Kod yazan ajan önerir, Levent onaylar. İlk karşılıklar: bootstrap = yeniden örnekleme, Holm = çoklu deneme düzeltmesi, walk-forward = yıllık ileri yürüme (§5.8 zaten böyle diyor).
**17-013** — KARAR — Gömülü PNG, HTML içinde base64 (tek dosya, bağlantı kopmaz). İlk sürümde tek grafik (bkz. 17-020).
**17-014** — KARAR — Hiç sunulmaz. quantstats kurulu değil, eklenmez.
**17-015** — ZAYIF SORU — quantstats kullanılmıyor. K2 farkı kendi grafiğimizde fark serisi olarak çizilir.
**17-016** — CEVAPLI — §2 "Yüksek Sharpe modeller ilk virajda patlar". Sharpe gösterilmez. Gösterilenler: medyan, fazla getiri, en büyük düşüş.
**17-017** — ZAYIF SORU — quantstats çıkarıldı (kurulu değil), sürüm riski yok.
**17-018** — KARAR — matplotlib (kurulu, statik PNG). plotly kurulu ama etkileşim gerekmiyor, Streamlit yok.
**17-019** — ZAYIF SORU — Ekran yok. Grafik fonksiyonu yalnız `rapor.py`'de, tek kaynak.
**17-020** — KARAR — İlk sürümde zorunlu tek grafik: yıllık fazla getiri çubukları (5.12 madde 4, "yılların %60'ı"). §5.12 hiçbir grafik istemiyor. Sermaye eğrisi ve düşüş sonra, tablo olarak yeter.
**17-021** — ZAYIF SORU — Streamlit yok. İleride eklenirse `.streamlit/config.toml` içinde `gatherUsageStats = false`.
**17-022** — ZAYIF SORU — Streamlit yok. İleride eklenirse aynı config dosyasında `address = "127.0.0.1"`.
**17-023** — ZAYIF SORU — Başlatılacak sunucu yok. Rapor HTML'i çift tıklanır, kart günlüğü Görev Zamanlayıcı'dan çalışır (17-090).
**17-024** — ZAYIF SORU — Sunucu yok, arka planda kalacak süreç yok.
**17-025** — ZAYIF SORU — Port yok.
**17-026** — ZAYIF SORU — Betik yeniden çalışması ve önbellek yok. HTML statik, üretim tarihi başlıkta.
**17-027** — ZAYIF SORU — Ekran yok. İlke olarak: okuyucu hiçbir zaman Adım/Motor'u içe aktarmaz, yalnız üretilmiş dosyayı gösterir.
**17-028** — ZAYIF SORU — Ekran yok. Sözleşme: rapor, sonuç sözlüğünden md/html/CSV yazar (17-092).
**17-029** — KARAR — Markdown geri ayrıştırılmaz. Veri tek yönlü akar: sonuç sözlüğü → md, html, CSV.
**17-030** — ZAYIF SORU — Tek kaynak (sonuç sözlüğü), ikinci gösterim yok. Çelişki oluşamaz.
**17-031** — ZAYIF SORU — Streamlit yok. Kart ekranı gerekirse o zaman tasarlanır.
**17-032** — KARAR — "Hiçbir aile geçmedi" satırı + 3 aile × 6 ölçüt geçti/kaldı tablosu. Boş sayfa değil.
**17-033** — KARAR — Evet. Kaynak: kabul fonksiyonunun aile başına döndürdüğü `{ölçüt_no: (geçti, değer)}` sözlüğü. Rapor tablosu bundan çizilir.
**17-034** — KARAR — Ekran yok. Kart CSV'sinde deneme aileleri yok (§6.3). Raporun kanıt tablosunda 3 aile de görünür, çünkü bu kanıttır, sinyal değil. Gizleme düğmesi yok.
**17-035** — KARAR — Sabit metinler `rapor.py` başında sabitlerde. Bir test: üretilen md/html/CSV'de "Tansu'nun sistemi", "AL", "SAT" geçmez.
**17-036** — YANLIŞ — Evet, statik HTML aynı işi görür. Streamlit hiç kurulmamış, bu kurulum yükü gereksiz. Çıkar.
**17-037** — KARAR — Evet, tamamen yer alır. Streamlit'in tek farkı etkileşim (süzme); ilk sürümde ihtiyaç yok.
**17-038** — YANLIŞ — `pyproject.toml` yalnız `[tool.pytest.ini_options]` içeriyor (doğrulandı). Bağımlılık tanımsız. Düzeltme: `[project] dependencies` ekle, sürümleri `==` ile sabitle (pandas 3.0.6 vb.), `pip freeze` ile `requirements.txt` kilidi üret.
**17-039** — ZAYIF SORU — Ekran yok. Rapor/CSV için tek test: 17-093.
**17-040** — KARAR — `pathlib` ve `Path(__file__).resolve()` (`rapor.py` zaten böyle). Dosyalar `encoding="utf-8"`/`utf-8-sig` ile açılır. Türkçe/boşluklu yol Python 3'te sorun çıkarmaz. Yeni klasörler aynı kalıpla tanımlanır.
**17-041** — KARAR — Ayrı sütunlar, sabit sıra, Türkçe başlık: Tarih; Hisse; Aile; Durum; Giriş alt; Giriş üst; Stop; Hedef; Pozisyon %; Adet (1.000.000 TL); Kanıt; Kaynak. Kanıt satırı tek metin sütunu.
**17-042** — KARAR — Sürüm yok. Sütunlar yalnız sona eklenir, yeniden adlandırılmaz. Her gün ayrı dosya olduğu için eski dosyalar etkilenmez. Sistem CSV'yi okumaz (17-059).
**17-043** — KARAR — Ayırıcı `;`. Türkiye bölgesel ayarında Excel çift tıkla düzgün açar.
**17-044** — KARAR — Ondalık virgül. Excel ve rapor aynı. Makine okuması `pd.read_csv(sep=";", decimal=",", encoding="utf-8-sig")` ile (sistem zaten okumaz).
**17-045** — KARAR — Evet, `encoding="utf-8-sig"` ile yazılır. Aynı kodlamayla okununca ilk sütun adı temiz (doğrulandı).
**17-046** — KARAR — Tarih ISO `2026-10-05`. Hisse kodu harf içerir, bilimsel gösterim riski yok. Excel ISO tarihi tanır (bilinen davranış, burada denenmedi); tanımasa bile metin kalır, zarar yok.
**17-047** — KARAR — Kontrol yok. CSV sistemin girdisi değil (17-059). Levent kopyada çalışır, bozulma sistemi etkilemez.
**17-048** — KARAR — Önce durum deposu (SQLite) güncellenir, sonra CSV geçici dosyaya yazılıp `os.replace` ile taşınır. `PermissionError` olursa koşu "HATA: CSV açık, kapatıp yeniden çalıştır" diye `DURUM.txt`'e yazılır. Yeniden çalıştırma güvenli (17-062).
**17-049** — KARAR — Her gün yeni dosya `kartlar-YYYYMMDD.csv`. Geçmiş = eski dosyalar. Açık kartların kendisi SQLite'ta.
**17-050** — KARAR — Yalnız başlık satırı olan CSV yazılır. Neden `DURUM.txt`'te: "KART YOK (canlı aile yok)".
**17-051** — KARAR — `kartlar/DURUM.txt` ilk satırı: tarih + "KART VAR / KART YOK (sinyal yok) / KART YOK (veri bayat) / HATA". Başlık-satırlı boş CSV = sinyal yok; CSV yok ve DURUM eski = koşu hiç çalışmadı.
**17-052** — KARAR — Kart yüzdeyi esas alır. Adet 1.000.000 TL için bilgi amaçlıdır. Levent adedi kendi sermayesine oranlar (rapor başlığında tek örnek cümle). İlk sürümde sermaye ayarı yok.
**17-053** — KARAR — Adet aşağı yuvarlanır (`int`, lot = 1). 1.000.000 TL'de sapma çok küçük (tahmin, ölçülmedi), rapora yazılmaz. Küçük sermayede büyür, bu yüzden yüzde esastır (17-052).
**17-054** — YANLIŞ — §6.4 "giriş bölgesi" tanımsız. İşlem yarının AOF'unda olur, kart günü bilinmez. Düzeltme: "giriş bölgesi" yerine "referans = sinyal günü kapanışı". Stop ve hedef bu referanstan "tahmini" diye yazılır, kartta uyarı: gerçek giriş yarının AOF'u.
**17-055** — KARAR — `DURUMLAR` ve `SUTUNLAR` tek yerde sabit listeler. Test (17-035): çıktıdaki etiketler listede, "AL/SAT/ÖNERİ" geçmez.
**17-056** — KARAR — Geçerli liste §6.5: AKTİF / STOP / HEDEF / BOZULDU. TAMAMLANDI = HEDEF. §2 Tansu'nun kendi etiketlerini anlatır, bizim değil. §2'ye bu not eklenir.
**17-057** — KARAR — Kimlik: hisse + aile + sinyal tarihi. Hissede açık kart varken gelen sinyal kart üretmez (§5.3 ile aynı kural). Çakışma çıkmaz.
**17-058** — KARAR — Kanıt satırı kart günü metin olarak donar. Yeniden hesaplama eski günlük dosyayı değiştirmez. Sayılar raporda.
**17-059** — KARAR — CSV yalnız çıktı. Sistemin girdisi SQLite durum deposu. Levent CSV'yi düzenlese bozulmaz.
**17-060** — KARAR — SQLite (`sqlite3`, stdlib), tek dosya `veri/durum.sqlite`. Seçeneklerde anılmaması tasarımda boşluk, bu karar kapatır.
**17-061** — KARAR — Güncelleme tek SQLite işlemi (transaction) içinde. Yarıda kesilirse geri alınır, yarım durum kalmaz.
**17-062** — KARAR — İdempotent: durum tablosunda `son_islenen_gun`. Eşit ya da eski gün atlanır. Test: aynı günü iki kez çalıştır, durum aynı kalmalı.
**17-063** — KARAR — Adım, `son_islenen_gun`'den bugüne kadar takvimdeki her işlem gününü sırayla işler. Veri günlük çubuk olduğu için atlanan gün kaybolmaz.
**17-064** — KARAR — Aynı `veri/durum.sqlite` içinde `islemler` tablosu. Dosya bozulursa yedekten dönülür. Yedek de yoksa dönem sıfırlanır ve bu deneme günlüğüne yazılır.
**17-065** — KARAR — Aynı dosya, ayrı tablolar (kartlar, islemler). Tek işlemde yazıldığı için tutarsızlık olmaz. Silme riskini yedek (17-067) karşılar.
**17-066** — KARAR — Başka daldır. Kural kaydı ve deneme günlüğü `kayit/` altında git'te izlenen CSV, sütunlar §5.11 listesi. Koşu yazar, rapor yalnız okur.
**17-067** — KARAR — Her koşu sonunda `sqlite3` yedekleme ile `veri/yedek/durum-YYYYMMDD.sqlite`, son 30 tutulur. Levent ayda bir `veri/yedek` klasörünü harici diske kopyalar. Sorumlu: Levent. `kayit/` git'te olduğu için ayrıca korunur.
**17-068** — KARAR — `rapor/` (md, html, png, işlem CSV), `kartlar/` (kart CSV, DURUM.txt), `kayit/` (git'te), `veri/` (git dışı: anlık görüntü, `ara/` parquet, durum.sqlite, yedek, log).
**17-069** — KARAR — `rapor/` ve `kartlar/` `.gitignore`'a eklenir (şimdi izleniyor, doğrulandı). Kanıtın bütünlüğü git'te izlenen deneme günlüğündeki hash'ten gelir.
**17-070** — KARAR — Otomatik silme/arşiv yok. Levent yalnız `son.html` ve `kartlar-son.csv`'ye bakar. Dosyalar küçük, yıllık elle arşiv yeter (boyut tahmini, ölçülmedi).
**17-071** — KARAR — Evet. Her koşu `rapor/son.html` ve `kartlar/son.csv` kopyasını yazar. Eskileri tarihli adla Gezgin ada göre sıralar.
**17-072** — CEVAPLI — `rapor.py` `%Y%m%d` kullanıyor. Gezgin'de ada göre kronolojik sıralanır. Yeterli, kalsın.
**17-073** — YANLIŞ — Parquet ara üründür, `rapor/`'da işi yok (şu an orada, doğrulandı). `veri/ara/`'ya taşınır. Levent'in dosyası işlem CSV'si (17-074).
**17-074** — KARAR — Evet. `rapor/islemler-<koşu>.csv` (`;`, `utf-8-sig`): hisse, aile, giriş tarihi, çıkış tarihi, giriş fiyatı, çıkış fiyatı, çıkış nedeni, getiri. Bu §1 hedefini karşılar.
**17-075** — KARAR — Hayır, tasarlanmadı. 17-074 dosyası bunu karşılar. "Çıkış nedeni" (stop/hedef/bozulma) zorunlu sütun.
**17-076** — KARAR — "Varsayımların etkisi" bölümü kabul tablosundan hemen sonra. Karantina yoksa gizlenmez, "Karantina: 0 hisse-dönem" yazılır.
**17-077** — KARAR — Tek "Uyarılar" bölümü, kabul tablosundan hemen sonra, sayılı satırlar. Boşsa "Uyarı yok" yazılır.
**17-078** — KARAR — Mutlak getiri gösterilir. Başlığı "üst sınır, karar için kullanma", fazla getiri sütunundan sonra gelir. "Ne kadar kazanırdım" sorusu cevaplanır ama uyarıyla.
**17-079** — KARAR — Raporda 6 satırlık tablo (ölçüt, geçti/kaldı, değer). Genel "Geçti" yalnız hepsi sağlanınca. Kısmi sonuç tablo satırında tek cümleyle açıklanır.
**17-080** — KARAR — Aynı rapor, tek tablo, üç masraf sütunu (aile × %0,1/%0,3/%0,5). Ayrı rapor yok.
**17-081** — KARAR — Raporda iki katman: özet = aile başına 1 satır (birleşik ileri yürüme); ayrıntı = yıl × aile tablosu, yalnız %0,3 masraf. Tam döküm `rapor/` altında CSV.
**17-082** — KARAR — Negatif hücrelerin listesi (parametre değerleri + sonuç). Isı haritası yok.
**17-083** — YANLIŞ — `nabiz.py` etiketleri `TAM_ALIM / DIKKATLI / BEKLE` (doğrulandı). "TAM_ALIM" ve "BEKLE" emir dilidir, P1'e aykırı. Raporda ve CSV'de Türkçe durum sözcükleri kullanılır (ör. güçlü / zayıf / bozuk), kod değeri içeride kalır.
**17-084** — KARAR — Elle: `f"{x:.1%}".replace(".", ",")`, tek yardımcıda. `locale` kullanılmaz, Windows ayarına bağlı. Babel eklenmez.
**17-085** — KARAR — Raporda "1.000.000 TL" (nokta binlik). CSV'de binlik ayırıcısız tam sayı.
**17-086** — KARAR — Her yerde ISO `2026-10-05` (dosya adı hariç, orada `YYYYMMDD`). Tek biçim, çift görünüm yok.
**17-087** — KARAR — Raporda başlık altında sabit uyarı. CSV'de her satırda `Kaynak` sütunu = "Tansu'dan esinlenen yorum". İlk satır uyarısı CSV'yi bozar.
**17-088** — KARAR — `kartlar/DURUM.txt`'e Türkçe tek satır ("HATA: veri çekilemedi"). Ayrıntı ve traceback `veri/log/`'a. Hata varsa kart üretilmez.
**17-089** — KARAR — `DURUM.txt` ve Görev Zamanlayıcı'daki "son çalıştırma sonucu". Ek bildirim yok (Telegram yok listesinde). Levent akşam DURUM.txt tarihine bakar.
**17-090** — KARAR — Windows Görev Zamanlayıcı, 19:30, "kaçırılan görevi en kısa sürede çalıştır" (StartWhenAvailable) açık. Kurulum adımı TASARIM §6'ya yazılır.
**17-091** — KARAR — İki komut: `python -m tansu.gunluk` (kart, her akşam, otomatik) ve `python -m tansu.rapor` (uzun, 1.000 tekrar; Levent yalnız kural/parametre değişince).
**17-092** — KARAR — Sözlük anahtarları sözleşmedir (`kanit.ozet` zaten `dict` döndürüyor). pydantic yok. Tek test anahtar listesini denetler.
**17-093** — KARAR — Golden file yok (kırılgan). Tek test: küçük sahte sonuçtan rapor ve CSV üret; sütun listesi, ilk satır cümlesi ve yasaklı kelimeleri denetle.
**17-094** — YANLIŞ — `rapor/kanit-20261005.md` duruyor (doğrulandı). §7 adım 1 Yahoo'lu ön deneme kodunu kaldırır, aynı adımda `rapor/` içindeki eski md ve parquet de silinir. Git geçmişinde kalır.
**17-095** — KARAR — İlk sürümde yan yana karşılaştırma yok. "Ne değişti" sorusu deneme günlüğündeki iki satırın (hash, ana sonuç) karşılaştırılmasıdır.
**17-096** — KARAR — Rapor yalnız son koşuyu gösterir. Deneme günlüğünden yalnız toplam deneme sayısı ve Holm'de kullanılan p listesi (CSV) girer. Sayfa uzunluğu sabit.
**17-097** — KARAR — Bir kez elle sınama: ilk rapor Levent'e okutulur, 3 soru sorulur (kaç aile geçti, veri hangi tarih, "ayırt edilemiyor" ne demek). Otomatik test yok.
**17-098** — KARAR — Terim ilk geçtiği yerde parantezle tek satır açıklanır (`rapor.py`'de sözlük sabiti). Dosyalar arası bağlantı verilmez.
**17-099** — KARAR — Sıra: 1) `kartlar/DURUM.txt`, 2) `kartlar/son.csv` (Excel), 3) `rapor/son.html` yalnız yeni rapor üretilince. Sıra TASARIM §6'ya yazılır.
**17-100** — KARAR — En küçük sürüm: markdown/HTML rapor + `;` CSV kart + SQLite durum deposu. Streamlit, quantstats, plotly çıkarılınca §1 ihtiyacından hiçbiri kaybolmaz. Durum deposu çıkarılırsa açık kart güncelleme (§6.5) ve kâğıt üstü dönem (§5.8) kaybolur, bu yüzden çıkarılamaz.

## Özet

Karar sayıları: CEVAPLI 2, KARAR 76, YANLIŞ 8, OLGU 0, ZAYIF SORU 14 (toplam 100). Olgular başta doğrulandı; ayrı OLGU maddesi yok.

En önemli 10 kurulum kararı:
1. Streamlit ilk sürümden çıkar (17-001, 17-036). Rapor tek dosya HTML olur, tarayıcıda açılır. quantstats ve plotly da yok.
2. Bağımlılıklar `pyproject.toml`'a `==` sürümle yazılır, `requirements.txt` kilidi üretilir (17-038).
3. Açık kart ve işlem durumu SQLite'ta (`veri/durum.sqlite`), tek işlemle yazılır, idempotent, atlanan günler geriye dönük işlenir (17-060 ile 17-063).
4. Yedek: her koşuda `veri/yedek/` içine son 30 kopya. Levent ayda bir harici diske kopyalar (17-067).
5. CSV: `;` ayraç, ondalık virgül, `utf-8-sig`, ISO tarih. CSV yalnız çıktıdır, sistem okumaz (17-043 ile 17-045, 17-059).
6. Klasörler: `rapor/`, `kartlar/`, `kayit/` (git'te), `veri/` (git dışı, parquet `veri/ara/`). `rapor/` ve `kartlar/` `.gitignore`'a; eski ön deneme dosyaları silinir (17-068, 17-069, 17-073, 17-094).
7. Koşu kontrolü: Görev Zamanlayıcı 19:30 + kaçırılanı çalıştır. `kartlar/DURUM.txt` tek Türkçe durum satırı; boş CSV = sinyal yok (17-051, 17-088 ile 17-090).
8. Düzeltmeler: kartta "giriş bölgesi" yerine "referans = sinyal günü kapanışı" (17-054); kartta "±" yerine "%95 aralık" (17-011); tek durum listesi AKTİF/STOP/HEDEF/BOZULDU, TAMAMLANDI = HEDEF (17-056).
9. Emir dili: `nabiz.py` etiketleri `TAM_ALIM/BEKLE` rapora çıkmaz, Türkçe durum sözcüğü kullanılır. Sabit etiket/sütun listeleri + yasaklı kelime testi (17-035, 17-055, 17-083).
10. Rapor ilk satırı "Hiçbir aile kabul ölçütünü geçmedi (0/3)", ilk ekranda 3 rakam, 6 ölçütlük geçti/kaldı tablosu, tek "Uyarılar" bölümü. Sayı biçimi elle yardımcıyla (virgül, `locale` yok) (17-008, 17-009, 17-033, 17-077, 17-084).
