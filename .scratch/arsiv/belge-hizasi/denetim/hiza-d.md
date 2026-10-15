## Ne okudum

İlk okunan dosya `AGENTS.md`; ilk satırı: **`# TANSU`**.

**50 dosya, 7.824 satır**, baştan sona okundu. Hiçbir dosya değiştirilmedi. Satır sayıları boş satırları içerir.

| Dosya | Satır |
|---|---:|
| `AGENTS.md` | 81 |
| `GLOSSARY.md` | 41 |
| `CODING_STANDARDS.md` | 15 |
| `DEFINITION_OF_DONE.md` | 93 |
| `docs/TASARIM.md` | 926 |
| `docs/KURALLAR.md` | 172 |
| `docs/sadakat.md` | 65 |
| `docs/agents/issue-tracker.md` | 30 |
| `docs/agents/triage-labels.md` | 15 |
| `docs/agents/domain.md` | 51 |
| `pyproject.toml` | 27 |
| `.scratch/tansu-mvp/spec.md` | 288 |
| `.scratch/tansu-mimari/spec.md` | 41 |
| `.scratch/tansu-mvp/issues/01-kullanim-kosullari-fiyat-adimi.md` | 31 |
| `.scratch/tansu-mvp/issues/02-veri-ucu.md` | 50 |
| `.scratch/tansu-mvp/issues/03-veri-kapilari-karantina-limit.md` | 72 |
| `.scratch/tansu-mvp/issues/04-borsapy-ikinci-kaynak.md` | 49 |
| `.scratch/tansu-mvp/issues/05-sadakat-ema-sikisma.md` | 54 |
| `.scratch/tansu-mvp/issues/06-sadakat-cift-z.md` | 54 |
| `.scratch/tansu-mvp/issues/07-evren.md` | 118 |
| `.scratch/tansu-mvp/issues/08-adim-motor.md` | 50 |
| `.scratch/tansu-mvp/issues/09-kosu-kural-kaydi.md` | 40 |
| `.scratch/tansu-mvp/issues/10-simulator-k2-rapor.md` | 71 |
| `.scratch/tansu-mvp/issues/11-cift-bolmesi.md` | 106 |
| `.scratch/tansu-mvp/issues/12-k1-istatistik-kabul.md` | 71 |
| `.scratch/tansu-mvp/issues/13-saglamlik-denetim.md` | 87 |
| `.scratch/tansu-mvp/issues/14-gunluk-kosu.md` | 78 |
| `.scratch/tansu-mvp/issues/15-ilk-resmi-kosu.md` | 60 |
| `.scratch/tansu-mvp/issues/16-kap-bist100.md` | 76 |
| `docs/arastirma/kullanim-kosullari-fiyat-adimi.md` | 82 |
| `docs/arastirma/veri-kaynaklari.md` | 157 |
| `rapor/kanit-20261005.md` | 16 |
| `tansu/__init__.py` | 0 |
| `tansu/__main__.py` | 185 |
| `tansu/aileler.py` | 69 |
| `tansu/cift.py` | 39 |
| `tansu/ciftbolme.py` | 449 |
| `tansu/denetim.py` | 298 |
| `tansu/evren.py` | 84 |
| `tansu/gostergeler.py` | 66 |
| `tansu/gunluk.py` | 352 |
| `tansu/istatistik.py` | 419 |
| `tansu/kayit.py` | 589 |
| `tansu/kaynak.py` | 264 |
| `tansu/motor.py` | 257 |
| `tansu/rapor.py` | 340 |
| `tansu/sadakat.py` | 301 |
| `tansu/saglamlik.py` | 95 |
| `tansu/simulator.py` | 372 |
| `tansu/veri.py` | 478 |

## Bulgular

Aşağıdaki numaralı bilet dosyaları `.scratch/tansu-mvp/issues/` altındadır. Eski ölçüm rakamlarını tarihsel kayıt olarak korudum; hâlâ açık iş veya geçerli talimat gibi duran ifadeleri işaretledim.

**Davranış, komut ve uygulama sırası**

| # | Tür | Yer 1 | Yer 2 | Ne | Önerilen düzeltme |
|---|---|---|---|---|---|
| 1 | ESKİ | `.scratch/tansu-mvp/spec.md:21` | `tansu/kayit.py:334`; `15-ilk-resmi-kosu.md:26` | Spec “Kod da yok” diyor; kod ve ilk resmi koşu artık var. | Sahip MVP spec olsun; problem bölümünü bugünkü durumla değiştir, prototipin silinmesini tarihsel not yap. |
| 2 | ESKİ | `.scratch/tansu-mvp/spec.md:163,183,188` | `docs/TASARIM.md:120,148`; `tansu/ciftbolme.py:80` | Bağımlılık sırası eski; çift seçimi ve çift simülasyonu yanlış modüllere atanmış. | Sahip TASARIM §4 olsun; spec’teki modül haritasını güncel bölüme atıfla değiştir. |
| 3 | ESKİ | `.scratch/tansu-mvp/spec.md:204` | `tansu/__main__.py:95–114` | Komut listesinde `denetim`, `evren-indir`, `sektor-indir` ve `--resmi` yok. | Sahip TASARIM §4 olsun; komut sözleşmesini orada tamamla, spec’i ona bağla. |
| 4 | ÇELİŞKİ | `.scratch/tansu-mvp/spec.md:217–218`; `docs/TASARIM.md:866–867` | `09-kosu-kural-kaydi.md:8` | Plan kural kaydını motordan önce koyuyor; kayıt bileti motor biletine bağımlı. | Sahip TASARIM §7 olsun; uygulama sırasını bilet bağımlılığıyla uzlaştır, spec’te sırayı yeniden yazma. |
| 5 | ESKİ | `.scratch/tansu-mvp/spec.md:37` | `tansu/gunluk.py:316–338`; `tansu/kayit.py:469` | Spec her akşam HTML rapor üretileceğini söylüyor; günlük komut CSV ve durum dosyası, sınama komutu HTML üretiyor. | Sahip TASARIM §6 olsun; spec’te günlük çıktı ile sınama raporunu ayır. |
| 6 | ÇELİŞKİ | `.scratch/tansu-mvp/spec.md:66–67`; `07-evren.md:4–7` | `07-evren.md:38–40`; `tansu/evren.py:45–53` | Spec önce büyük 100’den eleme anlatıyor; biletin başı tek kod elemesini sona koyuyor, kod ise tek kod ve likidite elemesinden sonra 100 seçiyor. | Sahip TASARIM §5.2 olsun; işlem sırasını tek yerde açık yaz, diğer tarifleri atfa çevir. |
| 7 | ÇELİŞKİ | `15-ilk-resmi-kosu.md:3,16` | `tansu/__main__.py:110–114,145–147`; `15-ilk-resmi-kosu.md:30` | `sinama --son` resmi kayıt vaat ediyor; resmi olmak için ayrıca `--resmi` gerekiyor. | Sahip TASARIM’ın komut sözleşmesi olsun; bilette komutu `sinama --son --resmi` yap. |
| 8 | ÇELİŞKİ | `09-kosu-kural-kaydi.md:20` | `docs/TASARIM.md:649–651`; `tansu/kayit.py:430–433` | Bilet kirli ağaçtaki resmi isteğin geliştirme koşusuna dönüşeceğini söylüyor; tasarım ve kod isteği durduruyor. | Sahip TASARIM §5.11 olsun; kabul maddesini “durur, günlük yazılmaz” olarak düzelt. |
| 9 | ESKİ | `09-kosu-kural-kaydi.md:5,18–19` | `tansu/kayit.py:438–455,492–575` | Günlük artık yalnız iki satırdan oluşmuyor; ayrıca `resmi`, `kirli` ve ortam bilgisi her satırda bulunmuyor. | Sahip TASARIM §5.11 olsun; bilette başlangıç, bitiş, durum ve destek satırlarını bu şemaya bağla. |
| 10 | ÇELİŞKİ | `03-veri-kapilari-karantina-limit.md:9`; `.scratch/tansu-mvp/spec.md:175` | `14-gunluk-kosu.md:78`; `tansu/veri.py:237–248` | İlk metinler kapıda kalan indirmenin anlık görüntü olmayacağını söylüyor; mevcut yol görüntüyü saklıyor. | Sahip TASARIM §5.13/§6.2 olsun; yapısal hata ile sonradan değerlendirilen oran kapılarını ayır, bilet ve spec’i buna bağla. |
| 11 | ESKİ | `03-veri-kapilari-karantina-limit.md:29` | `docs/TASARIM.md:752–761`; `tansu/veri.py:422–427` | “Ortada NaN indirmeyi durdurur” maddesi, kısmi NaN ve tekrar satır istisnalarından önce kalmış. | Sahip TASARIM §5.13 olsun; eski kabul maddesini güncel yapısal ihlal tanımına bağla. |
| 12 | ÇELİŞKİ | `14-gunluk-kosu.md:30`; `docs/TASARIM.md:802` | `AGENTS.md:32` | Günlük görüntüler 30 gün sonra siliniyor; AGENTS bütün `veri/` için silme yasağı koyuyor. | Saklama politikasının sahibi TASARIM §6.2 olsun; AGENTS’te günlük görüntü istisnasını bu bölüme atıfla belirt. |
| 13 | ÇELİŞKİ | `14-gunluk-kosu.md:22`; `docs/TASARIM.md:812–813` | `AGENTS.md:17–19`; `tansu/gunluk.py:30–42` | Tasarımın sabit kart başlıkları Türkçe karakter içeriyor; AGENTS CSV başlıklarına Türkçe ASCII şartı koyuyor. | Kart başlıklarının sahibi TASARIM §6.5 olsun; AGENTS’te kullanıcıya görünen kart başlıklarını açık istisna yap. |
| 14 | ESKİ | `.scratch/tansu-mvp/spec.md:224–225`; `14-gunluk-kosu.md:31–32` | `AGENTS.md:35–36`; `14-gunluk-kosu.md:63–64` | Kurulum için hâlâ `schtasks` isteniyor; aynı bilet bu yöntemin başarısız olduğunu ve PowerShell kurulumunu kaydediyor. | Kurulum komutunun sahibi AGENTS olsun; spec ve kabul maddesinde ona atıf ver. |
| 15 | ESKİ | `14-gunluk-kosu.md:51`; `docs/TASARIM.md:797` | `AGENTS.md:39–40`; `14-gunluk-kosu.md:70–72` | Aylık taban yenilemesi hâlâ “elle” anlatılıyor; `TansuAylik` görevi kurulmuş. | İşleyişin sahibi TASARIM §6 olsun; aylık görevi oraya işle, elle çalıştırmayı yalnız yeniden deneme yolu olarak belirt. |
| 16 | ÇELİŞKİ | `11-cift-bolmesi.md:25` | `docs/TASARIM.md:422–425`; `tansu/ciftbolme.py:149–164` | Kabul maddesi bütün payların yıl başında eşit olduğunu söylüyor; devam eden çiftlerin payı eşitlenmiyor. | Sahip TASARIM §5.6 olsun; kabul maddesinde yalnız yeni çiftler ve boş payların eşit paylaşımını belirt. |
| 17 | ÇELİŞKİ | `11-cift-bolmesi.md:26`; `GLOSSARY.md:16` | `docs/TASARIM.md:430–431`; `tansu/ciftbolme.py:318–320` | 50/50 alımı bir yerde yılın ilk günü, diğerinde seçimden sonraki işlem günü. | Zamanlama sahibi TASARIM §5.6 olsun; bilet ve sözlüğü seçimden sonraki güne göre düzelt. |
| 18 | ESKİ | `12-k1-istatistik-kabul.md:20` | `docs/TASARIM.md:509–516`; `tansu/istatistik.py:84–102` | “Uygun gün yetmezse hata” maddesi, komşusuz sinyal ve ek kol için eklenen istisnaları kapsamıyor. | Sahip TASARIM §5.7 olsun; kabul maddesini kol bazındaki güncel davranışa bağla. |
| 19 | ESKİ — kısmi | `14-gunluk-kosu.md:5,11` | `docs/TASARIM.md:822`; `tansu/gunluk.py:132–133` | Bilet tüm Kâğıt/Canlı ailelerin kartlarını bitirmiş görünüyor; çift kartı yok, fakat bu eksik tasarımda açıkça kabul edilmiş. | Kapsamın sahibi TASARIM §6.5 olsun; biletin kapanan kapsamını EMA kartı olarak belirt, çift kartını ayrı açık işte tut. |

**Kapanmış veya değişmiş işler için kalan eski notlar**

| # | Tür | Yer 1 | Yer 2 | Ne | Önerilen düzeltme |
|---|---|---|---|---|---|
| 20 | ESKİ | `02-veri-ucu.md:48`; `05-sadakat-ema-sikisma.md:50`; `06-sadakat-cift-z.md:47` | `09-kosu-kural-kaydi.md:34–36`; `docs/TASARIM.md:647–648` | Eski açık işlerde kayıt modülü, test yolu yönlendirmesi ve `kayit/` takibi hâlâ bekliyor görünüyor. | İş durumunun sahibi ilgili bilet olsun; bu maddelere bilet 09’a bağlı kapanış notu ekle. |
| 21 | ESKİ | `02-veri-ucu.md:49` | `03-veri-kapilari-karantina-limit.md:25–26`; `tansu/veri.py:435–445` | Sıfır/eksi fiyat denetimi açık iş olarak kalmış; bozuk satır kapısına bağlanmış. | Sahip bilet 02 olsun; maddeyi bilet 03’e atıfla kapat. |
| 22 | ESKİ | `02-veri-ucu.md:50`; `docs/arastirma/kullanim-kosullari-fiyat-adimi.md:28–29` | `04-borsapy-ikinci-kaynak.md:36–38`; `docs/TASARIM.md:168–169` | XU100 doğrulaması hâlâ bekleniyor veya bilet 02’ye atanıyor; doğrulama bilet 04’te yapılmış. | Güncel kaynak tanımının sahibi TASARIM §4 olsun; iki eski notu bilet 04 sonucuna bağla. |
| 23 | ESKİ | `05-sadakat-ema-sikisma.md:49` | `06-sadakat-cift-z.md:40`; `tansu/sadakat.py:274–276` | Çift bölümünün sadakat raporuna eklenmesi açık iş olarak kalmış; artık ekleniyor. | Sahip bilet 05 olsun; maddeyi bilet 06’ya atıfla kapat. |
| 24 | ESKİ | `07-evren.md:23–24` | `tansu/kayit.py:338–342` | “`kosu` evreni henüz çağırmıyor” notu geçersiz; koşu evreni hesaplayıp motora veriyor. | Sahip bilet 07 olsun; eski sınırlamaya kapanış notu ekle. |
| 25 | ESKİ | `07-evren.md:68–69,112–113` | `docs/TASARIM.md:771–775`; `tansu/simulator.py:340–352` | Kapı oranlarının evren üyeleri üzerinden hesaplanması hâlâ açık; bu karar ve bağlantı mevcut. | Sahip TASARIM §5.13 olsun; bilette yalnız olay tablosu eksikliğini açık bırak. |
| 26 | ESKİ | `04-borsapy-ikinci-kaynak.md:47–48`; `07-evren.md:117` | `11-cift-bolmesi.md:63–71` | Sektör ölçeği ölçümü ve “616 eksik” işi güncel kapanışa bağlanmamış; hedef üyelerde alınamayan kalmamış, 15 kapanmış kod sektörsüz. | Sonucun sahibi bilet 11 olsun; önceki biletleri bu sonuca bağla, bütün sembollerin tamamlandığını söyleme. |
| 27 | ESKİ | `08-adim-motor.md:49`; `10-simulator-k2-rapor.md:66–67` | `11-cift-bolmesi.md:41–49`; `tansu/motor.py:245–246` | Evren dışı sinyallerin motorda pozisyon açması hâlâ açık gösteriliyor; evren süzgeci motora taşınmış. | Sahip TASARIM §5.6 olsun; yalnız nakit/yer reddinden kalan yaklaşımı açık tut. |
| 28 | ESKİ | `08-adim-motor.md:49` | `tansu/kayit.py:498`; `tansu/rapor.py:241` | Düşen sinyal sayısının kayıt ve rapora taşınması bekleniyor; ikisinde de bulunuyor. | Sahip bilet 08 olsun; bu aktarım maddesini kapat. |
| 29 | ESKİ | `09-kosu-kural-kaydi.md:38`; `10-simulator-k2-rapor.md:68`; `11-cift-bolmesi.md:105` | `12-k1-istatistik-kabul.md:46–50,70`; `tansu/kayit.py:502–504` | K1, p, Holm ve tam tekrar bağlantıları önceki açık iş listelerinde kalmış. | Sonucun sahibi bilet 12 olsun; üç bilete kapanış atfı ekle. |
| 30 | ESKİ | `09-kosu-kural-kaydi.md:32–33,40` | `docs/TASARIM.md:574`; `tansu/saglamlik.py:17–27` | Hash listesi dört eski modülle, ızgara da yalnız EMA ile anlatılıyor; ikisi de genişlemiş. | Sahip TASARIM §5.8 ve KURALLAR §3 olsun; biletteki geçici listeleri güncel sahiplerine bağla. |
| 31 | ESKİ | `12-k1-istatistik-kabul.md:66` | `13-saglamlik-denetim.md:26`; `tansu/kayit.py:294` | Sağlamlık değeri hâlâ `None` ve Kâğıt’a geçişi engelliyor diye yazılmış; oran artık hesaplanıp kabule veriliyor. | Sahip bilet 12 olsun; sağlamlık bağlantısını kapat, kâğıt dönemi eksikliğini ayrı tut. |
| 32 | ESKİ | `12-k1-istatistik-kabul.md:67` | `13-saglamlik-denetim.md:51–55` | Açık hız notu 200 tekrar için 7 dakika, tam koşu için 25–30 dakika tahmini taşıyor; sonraki ölçüm bunu değiştirmiş. | Ölçümün sahibi bilet 13 olsun; bilet 12’de hız işini bu ölçüme atıfla kapat. |
| 33 | ESKİ | `11-cift-bolmesi.md:99–103`; `12-k1-istatistik-kabul.md:68`; `13-saglamlik-denetim.md:85` | `docs/TASARIM.md:762–768`; `tansu/veri.py:72–89` | Toplu bozuk kaynak günü hâlâ karar bekliyor gibi duruyor; ≥%50 ve en az 20 satır kuralı uygulanmış. | Sahip TASARIM §5.13 olsun; eski açık maddeleri kapat, eşik altında kalan bozuk günleri ayrı tut. |
| 34 | ESKİ | `13-saglamlik-denetim.md:73–74,82–83` | `15-ilk-resmi-kosu.md:26–32` | Son kodla denetim ve ilk resmi koşu hâlâ yapılacak iş olarak duruyor; bilet 15 bunları kaydetmiş. | İş durumunun sahibi bilet 15 olsun; bilet 13’e bu koşuların kapanış atfını ekle. |
| 35 | ESKİ | `13-saglamlik-denetim.md:86–87` | `docs/TASARIM.md:578`; `tansu/kayit.py:49–56` | `denetim.py` dosyasının hash dışında kalması “karar bekleyen” diye yazılmış; tasarım bunu karara bağlamış. | Sahip TASARIM §5.8 olsun; bilette bekleyen karar ifadesini kaldırıp bölüme bağla. |
| 36 | ESKİ | `14-gunluk-kosu.md:77` | `tansu/motor.py:76–103`; `tansu/gunluk.py:139–141` | Günlük ve motorun aynı döngüyü yinelediği söyleniyor; ikisi artık ortak `motor.tara` kullanıyor. | Sahip bilet 14 olsun; birleştirme işini kapat. |
| 37 | ESKİ | `14-gunluk-kosu.md:61–65`; `15-ilk-resmi-kosu.md:60` | `15-ilk-resmi-kosu.md:19–22,59` | Eski notlarda görevler kapalı veya ilk otomatik koşu doğrulanmayı bekliyor; bilet 15 etkinleştirmeyi ve başarılı geceyi kaydetmiş. | Durum kanıtının sahibi bilet 15 olsun; önceki ifadeleri tarihsel durum diye işaretle ve doğrulama maddesine bağla. |
| 38 | ESKİ | `16-kap-bist100.md:74` | `16-kap-bist100.md:24–46` | “07 bitince örtüşme oranı” hâlâ açık; aynı dosyada hesap ve sonuç tablosu var. | Sahip bilet 16 olsun; yalnız bu açık maddeyi kapat. |
| 39 | ESKİ | `.scratch/tansu-mimari/spec.md:19` | `tansu/__main__.py:93–107` | “38 dosya yeniden biçimlenecek” işi eski; salt okunur Ruff kontrolü **`76 files already formatted`** döndürdü. | İş durumunun sahibi mimari spec olsun; biçimleme maddesini kapat, geniş lint kuralı işini ayrı tut. |

**Araştırmalar, eski rapor ve terimler**

| # | Tür | Yer 1 | Yer 2 | Ne | Önerilen düzeltme |
|---|---|---|---|---|---|
| 40 | ESKİ | `docs/arastirma/veri-kaynaklari.md:142` | `docs/TASARIM.md:179,247–250` | Araştırmanın önerisi TradingView fiyatını ikinci kaynak yapıyor; bu yol sonradan bırakılmış. | Güncel kararın sahibi TASARIM olsun; öneriyi “geri çekildi” diye işaretleyip karara bağla. |
| 41 | ESKİ | `docs/arastirma/veri-kaynaklari.md:143` | `docs/TASARIM.md:237–243` | Öneride olay denetimi eşiği sabit %25; kararlı tasarım dönemsel limit ve %0,5 pay kullanıyor. | Sahip TASARIM §5.1 olsun; eski eşik önerisini yürürlükten kalkmış olarak işaretle. |
| 42 | ESKİ | `docs/arastirma/veri-kaynaklari.md:144` | `docs/TASARIM.md:258–279` | Öneri ana evreni KAP geçmiş üyeliğinden kuruyor; mevcut ana evren piyasa değeri kuralı, KAP çalışması ek karşılaştırma. | Sahip TASARIM §5.2 olsun; araştırmadaki önerinin yerini alan kararı belirt. |
| 43 | ESKİ | `docs/arastirma/veri-kaynaklari.md:137,146` | `docs/TASARIM.md:166–167,895–898` | Faiz önerisi hâlâ alternatif kaynaklar ve doğrulanmamış seri türü üzerinden ilerliyor; tek TCMB serisi seçilmiş ve türü doğrulanmış. | Sahip TASARIM §4/§8.9 olsun; araştırmaya karar atfı ekle, kalan fonlama farkı belirsizliğini koru. |
| 44 | ESKİ | `docs/arastirma/veri-kaynaklari.md:151,154` | `docs/TASARIM.md:165,876–879` | Hak kullanım tarihi ve 2015–2016 KAP kapsamı “kalan bilinmeyenler” arasında; tasarım bu iki başlığa cevap vermiş. | Güncel cevapların sahibi TASARIM olsun; araştırmada yalnız cevaplanmamış alt soruları açık bırak. |
| 45 | ESKİ | `rapor/kanit-20261005.md:1,4,11–16` | `docs/TASARIM.md:15–16,559` | Eski rapor kendini “kanıt”, 2023 sonrasını “ayrılmış” diye sunuyor; tasarım raporu geçersiz ön deneme sayıyor. | Geçerlilik kararının sahibi TASARIM olsun; raporun başına “geçersiz ön deneme, karar için kullanılmaz” uyarısı ve atıf ekle, tarihsel rakamları koru. |
| 46 | TERİM | `11-cift-bolmesi.md:76,83`; `docs/TASARIM.md:599` | `GLOSSARY.md:15`; `tansu/kayit.py:289–290` | Bilet 82 tutuş ile 39 geçişi ayırıyor, sonra örneklemde tutuşu “geçiş” diye sayıyor; kod işlem satırını sayıyor. | Anlamın sahibi GLOSSARY olsun; örneklem metinlerinde “tutuş dönemi” ve “farklı giriş günü” kullanarak sayılan birimi açıklaştır. |
| 47 | TERİM | `.scratch/tansu-mvp/spec.md:29–30,82,118–121`; `15-ilk-resmi-kosu.md:16` | `GLOSSARY.md:7–41` | Anlık görüntü, YORUM ve resmi/geliştirme koşusu önemli kavramlar olmasına rağmen sözlükte tanımlı değil. | Sahip GLOSSARY olsun; kısa tanımlar ekle, ayrıntılı kuralları TASARIM/KURALLAR’a bağla. |
| 48 | KIRIK ATIF — kısmi | `16-kap-bist100.md:71` | `16-kap-bist100.md:56–57` | `bosluk.csv` adlı dosya yok; gerçek ad `bist100_kap_bosluk.csv`, ancak kullanım bir kısaltma da olabilir. | Sahip bilet 16’daki dosya listesi olsun; atfı tam proje yoluyla yaz. |

**Birden fazla yerde tam yazılan kurallar**

Aşağıdakiler yalnız atıf veya kısa özet değil; parametre ve davranış tarifini yeniden taşıyan bölümlerdir.

| # | Tür | Yer 1 | Yer 2 | Ne | Önerilen düzeltme |
|---|---|---|---|---|---|
| 49 | TEKRAR | `docs/arastirma/kullanim-kosullari-fiyat-adimi.md:22–39` | `docs/TASARIM.md:166–187,247–250` | Veri kaynağı seçimi ve erişim politikası iki yerde tam yazılmış. | Sahip TASARIM §4 olsun; araştırmada kanıt ve tarihsel gerekçe kalsın, güncel politika atıf olsun. |
| 50 | TEKRAR | `docs/arastirma/kullanim-kosullari-fiyat-adimi.md:59–68` | `docs/TASARIM.md:225–234` | Fiyat adımı tablosu iki tam kopya halinde tutuluyor. | Sahip TASARIM §5.1 olsun; araştırmada ölçüm sonuçları ve tabloya atıf kalsın. |
| 51 | TEKRAR | `.scratch/tansu-mvp/spec.md:172–177`; `02-veri-ucu.md:20–29`; `04-borsapy-ikinci-kaynak.md:15–25` | `docs/TASARIM.md:131–140,210–214,436–437` | Anlık görüntü, manifest, olay denetimi ve faiz davranışı yeniden tarif ediliyor. | Sahip TASARIM olsun; biletlerde somut kabul kontrolü ve ilgili bölüm atfı kalsın. |
| 52 | TEKRAR | `.scratch/tansu-mvp/spec.md:89–94`; `05-sadakat-ema-sikisma.md:20`; `08-adim-motor.md:18–21` | `docs/KURALLAR.md:85–106`; `docs/TASARIM.md:195–200,285` | Aile eşikleri, giriş penceresi ve ısınma değerleri tekrar yazılıyor. | Aile parametrelerinin sahibi KURALLAR §3, ortak filtrelerin sahibi TASARIM olsun; diğer sayısal kopyaları atfa çevir. |
| 53 | TEKRAR | `.scratch/tansu-mvp/spec.md:86–90`; `11-cift-bolmesi.md:13–24` | `docs/TASARIM.md:381–419` | Çift seçimi, sektör sınırı ve geçiş engelleri birden fazla kural listesinde duruyor. | Sahip TASARIM §5.6 olsun; spec ve bilet aynı kuralları yeniden tanımlamasın. |
| 54 | TEKRAR | `08-adim-motor.md:22–30`; `.scratch/tansu-mvp/spec.md:97–103` | `docs/TASARIM.md:282–305,339–347` | Dolum, stop, kilit ve çıkış kuralları tam tariflerle tekrarlanıyor. | Sahip TASARIM §5.3/§5.5 olsun; bilette sınanacak senaryolar ve bölüm atıfları kalsın. |
| 55 | TEKRAR | `10-simulator-k2-rapor.md:16–26`; `.scratch/tansu-mvp/spec.md:104–109` | `docs/TASARIM.md:327–366,535–546` | Boyutlandırma sınırları, masraf düzeyleri ve K2 davranışı yeniden yazılmış. | Sahip TASARIM olsun; diğer dosyalarda değerleri tekrar etmek yerine kabul sonucunu tarif et. |
| 56 | TEKRAR | `12-k1-istatistik-kabul.md:13–36`; `13-saglamlik-denetim.md:13–18`; `.scratch/tansu-mvp/spec.md:116–130` | `docs/TASARIM.md:469–495,591–687,713–740` | K1, tekrar sayısı, bootstrap, sağlamlık ve denetim kuralları birden fazla yerde tam tutuluyor. | Sahip TASARIM §5.7–§5.12 olsun; biletler yalnız kendi iş kapsamını ve doğrulamasını taşısın. |
| 57 | TEKRAR | `05-sadakat-ema-sikisma.md:17–19`; `06-sadakat-cift-z.md:4–8,17–24`; `.scratch/tansu-mvp/spec.md:74–77` | `docs/KURALLAR.md:123–124,157–162` | Sadakat hedefleri, aday aralığı ve toleranslar farklı dosyalarda yeniden yazılıyor. | Sahip KURALLAR §4 olsun; biletler hedefleri atıfla alsın, ölçülmüş sonuçlar `docs/sadakat.md`’de kalsın. |
| 58 | TEKRAR | `14-gunluk-kosu.md:13–30`; `.scratch/tansu-mvp/spec.md:133–148` | `docs/TASARIM.md:781–844` | Günlük durumlar, CSV biçimi, tekrar koşma ve saklama kuralları tekrar ediliyor. | Sahip TASARIM §6 olsun; bilette çıktı kontrolü, spec’te kullanıcı ihtiyacı kalsın. |
| 59 | TEKRAR | `.scratch/tansu-mvp/spec.md:229–235` | `AGENTS.md:20–27` | Test verisinin bağımsızlığı, ağ yasağı, literal değer ve test gevşetmeme kuralları yeniden yazılmış. | Sahip AGENTS olsun; spec yalnız bu işe özgü test yüzlerini anlatsın. |
| 60 | TEKRAR | `13-saglamlik-denetim.md:48–55` | `docs/TASARIM.md:528–533` | Aynı süre ölçümleri ve hızlandırma açıklaması iki yerde tutuluyor. | Ölçüm kaydının sahibi bilet 13 olsun; TASARIM’da süre bütçesi ve kanıta atıf kalsın. |
| 61 | TEKRAR | `.scratch/tansu-mvp/spec.md:194–199`; `09-kosu-kural-kaydi.md:12–21` | `docs/TASARIM.md:567–582,626–667` | Hash, günlük ve aile durumu sözleşmesi birden fazla yerde yeniden tanımlanıyor. | Sahip TASARIM §5.8/§5.11 olsun; spec ve bilette ilgili sözleşmeye atıf kullan. |

## Boşluklar

- **Çalışma doğrulaması yapılmadı:** test, getiri sınaması, indirme veya günlük koşu çalıştırılmadı; bilet kapanışları belge ve kodla karşılaştırıldı.
- **Görev Zamanlayıcı’nın bugünkü durumu sorgulanmadı:** etkinleştirme ve ilk gece kanıtı, bilet 15’in kaydıdır.
- **Kapsam dışı kaynaklar:** dış URL’ler, eski çalışma ağacı kanıtları ve sorgu/strateji belgelerinin iç atıfları bütünüyle denetlenmedi.
- **Araç sınırı:** `.venv\Scripts\python.exe` “Erişim engellendi” hatası verdi; dosya ve yol kontrolleri PowerShell ile sürdürüldü. Ruff yalnız `format --check --no-cache` ile çalıştırıldı; “115 geniş lint uyarısı” iddiasının kural seti belirtilmediği için doğrulanamadı.
- **Mimari taslak:** onay bekleyen yeni kapsamı yürürlükteki tasarım saymadım; bu nedenle şok freni gibi gelecek önerilerini tek başına çelişki olarak yazmadım.