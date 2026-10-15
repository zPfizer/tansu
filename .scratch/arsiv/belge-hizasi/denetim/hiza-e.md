## Ne okudum

**Kapsamdaki 63 dosyanın tamamını, 10.578 satırı baştan sona okudum. Hiçbir dosyayı değiştirmedim.** Karşılaştırma belgeleriyle toplam 67 dosya, 11.815 satır.

Satır sayıları boş satırları içerir. `AGENTS.md` denetim sırasında değişti; son hâlinin 98 satırını yeniden okudum.

| Karşılaştırma belgesi | Satır |
|---|---:|
| `AGENTS.md` | 98 |
| `GLOSSARY.md` | 41 |
| `docs/TASARIM.md` | 926 |
| `docs/KURALLAR.md` | 172 |

| `docs/sorgu/` altındaki dosya | Satır |
|---|---:|
| `sorgu-2.md` | 110 |
| `sonuc-3-4.md` | 121 |
| `izleme/karar.md` | 44 |

| `docs/sorgu/izleme/` | Satır | Dosya | Satır |
|---|---:|---|---:|
| `izleme-01.md` | 106 | `izleme-11.md` | 123 |
| `izleme-02.md` | 104 | `izleme-12.md` | 85 |
| `izleme-03.md` | 113 | `izleme-13.md` | 101 |
| `izleme-04.md` | 88 | `izleme-14.md` | 113 |
| `izleme-05.md` | 84 | `izleme-15.md` | 122 |
| `izleme-06.md` | 40 | `izleme-16.md` | 104 |
| `izleme-07.md` | 100 | `izleme-17.md` | 118 |
| `izleme-08.md` | 125 | `izleme-18.md` | 118 |
| `izleme-09.md` | 112 | `izleme-19.md` | 122 |
| `izleme-10.md` | 120 | `izleme-20.md` | 108 |

| `docs/sorgu/sorgu-3/` soru dosyası | Satır | Cevap dosyası | Satır |
|---|---:|---|---:|
| `sorular-01-veri.md` | 201 | `cevaplar-01-veri.md` | 242 |
| `sorular-02-olaylar.md` | 201 | `cevaplar-02-olaylar.md` | 244 |
| `sorular-03-evren.md` | 102 | `cevaplar-03-evren.md` | 238 |
| `sorular-04-cift.md` | 201 | `cevaplar-04-cift.md` | 225 |
| `sorular-05-abcd.md` | 201 | `cevaplar-05-abcd.md` | 224 |
| `sorular-06-sikisma.md` | 201 | `cevaplar-06-sikisma.md` | 222 |
| `sorular-07-risk.md` | 217 | `cevaplar-07-risk.md` | 247 |
| `sorular-08-portfoy.md` | 219 | `cevaplar-08-portfoy.md` | 247 |
| `sorular-09-istatistik.md` | 201 | `cevaplar-09-istatistik.md` | 224 |
| `sorular-10-sadakat.md` | 201 | `cevaplar-10-sadakat.md` | 232 |

| `docs/sorgu/sorgu-4/` soru dosyası | Satır | Cevap dosyası | Satır |
|---|---:|---|---:|
| `sorular-11-moduller.md` | 201 | `cevaplar-11-moduller.md` | 136 |
| `sorular-12-ortam.md` | 201 | `cevaplar-12-ortam.md` | 227 |
| `sorular-13-depolama.md` | 201 | `cevaplar-13-depolama.md` | 220 |
| `sorular-14-test.md` | 201 | `cevaplar-14-test.md` | 222 |
| `sorular-15-kayit.md` | 201 | `cevaplar-15-kayit.md` | 126 |
| `sorular-16-kosu.md` | 223 | `cevaplar-16-kosu.md` | 254 |
| `sorular-17-cikti.md` | 201 | `cevaplar-17-cikti.md` | 122 |
| `sorular-18-adaptor.md` | 201 | `cevaplar-18-adaptor.md` | 222 |
| `sorular-19-cekirdek.md` | 201 | `cevaplar-19-cekirdek.md` | 225 |
| `sorular-20-bakim.md` | 201 | `cevaplar-20-bakim.md` | 121 |

## Bulgular

**Kararların tamamı aynı anlamla aktarılmamış.** Buna karşılık TASARIM’daki 150 farklı `NN-NNN` etiketi cevap dosyalarında mevcut; kullanılan `B-n`, `C-n` ve `S2-n` maddeleri de var. İzleme toplamları doğru: 723 VAR, 204 TEKRAR, 185 YENİ, 449 RED.

Tabloda yollar şu şekilde kısaltıldı: `TASARIM.md` ve `KURALLAR.md`, `docs/` altında; `izleme-*.md` ve `karar.md`, `docs/sorgu/izleme/` altında; `sonuc-3-4.md`, `docs/sorgu/` altında. Cevap dosyaları yukarıdaki envanterdeki klasörlerdedir.

Sonraki kararla gerekçeli biçimde değiştirilen tarihsel önerileri çelişki saymadım. **Kısmi**, metinde belirsizlik veya aktarım eksikliği bulunduğunu; bunun kod hatası olarak doğrulanmadığını belirtir.

| # | Tür | Yer 1 | Yer 2 | Ne | Önerilen düzeltme |
|---|---|---|---|---|---|
| 1 | ÇELİŞKİ | `karar.md:24`; `AGENTS.md:32` | `TASARIM.md:802` | Kabul edilen karar `veri/` silmeyi yasaklıyor; tasarım günlük anlık görüntüleri 30 gün sonra sildiriyor. | Sahip `TASARIM.md` §6: silme hükmünü kaldır; `izleme-11.md:63` önerisinin reddedildiğini `karar.md` üzerinden belirt. |
| 2 | ÇELİŞKİ | `izleme-09.md:45` | `izleme-15.md:65`; `TASARIM.md:656` | İki kabul edilmiş YENİ madde Holm’a girecek p için sırasıyla %0,3 ve %0,5 masraf istiyor; `karar.md` bu çakışmayı çözmüyor. | Sahip `TASARIM.md` §5.11: mevcut %0,5 seçimini `karar.md` içinde açık istisna olarak kaydet. |
| 3 | ÇELİŞKİ | `izleme-08.md:73`; `TASARIM.md:563` | `TASARIM.md:547` | Yıllık fazla getiri bir yerde günlük farkların toplamı, diğer yerde iki yıllık getirinin farkı; bunlar aynı hesap değil. | Sahip `TASARIM.md` §5.8: tek formül seç, §5.7’deki rapor tanımını ona bağla. |
| 4 | ÇELİŞKİ — kısmi | `izleme-09.md:53`; `TASARIM.md:611` | `TASARIM.md:615` | Sağlamlık hücresi “K1’e göre” pozitif sayılıyor, fakat uygulama K1 tekrarı yapmadan yalnız sepet farkını hesaplıyor; “K1’e göre” ifadesinin anlamı belirsiz. | Sahip `TASARIM.md` §5.10: karşılaştırma sepet farkıysa bunu açıkça yaz; rastgele karşılaştırma anlamını kaldır. |
| 5 | ÇELİŞKİ | `izleme-15.md:45`; `TASARIM.md:720` | `TASARIM.md:526` | Yarım kalan resmî koşu m’ye sayılıyor; tekrar sayısını belirleyen m ise yalnız mevcut p’lerden kuruluyor. | Sahip `TASARIM.md` §5.11: sonuçsuz resmî denemeleri kapsayan tek m tanımı ver; §5.7 onu kullansın. |
| 6 | ÇELİŞKİ | `sonuc-3-4.md:50`; `TASARIM.md:195` | `TASARIM.md:440` | İlk sinyal 30.11.2015 kabul edilmiş; simülatör 01.12.2015’ten sonraki ilk günden başlıyor ve önceki sinyalleri dışlıyor. | Sahip `TASARIM.md` §5.6: ilk kabul edilen sinyal ve ilk dolum tarihini ayrı ayrı, §5.1 ile aynı olacak şekilde yaz. |
| 7 | ÇELİŞKİ | `izleme-02.md:63`; `TASARIM.md:375` | `TASARIM.md:417` | İlk kural herhangi bir bacağın karantinasında açık pozisyonu kapatıyor; ayrıntı yalnız tutulan bacağın karantinasında kapatıyor. | Sahip `TASARIM.md` §5.6: kabul edilen “iki bacaktan biri” koşulunu ayrıntıya da geçir. |
| 8 | ÇELİŞKİ | `izleme-04.md:45`; `GLOSSARY.md:16` | `TASARIM.md:430` | 50/50 alımı yılın ilk işlem günü olarak tanımlı; uygulama seçimden sonraki işlem gününü kullanıyor. | Sahip `TASARIM.md` §5.6: seçimden sonraki günü esas alan değişikliği gerekçelendir; §5.7 ve sözlüğü aynı tarihe bağla. |
| 9 | ÇELİŞKİ — kısmi | `izleme-01.md:61` | `TASARIM.md:814`; `TASARIM.md:203` | Karar stopun tamamını ham TL’ye çevirmeyi istiyor; kart formülü ham referanstan, düzeltilmiş seride hesaplanan ATR’yi çıkarıyor ve ATR dönüşümünü belirtmiyor. | Sahip `TASARIM.md` §6.5: ham stopu `(düzeltilmiş referans − 2 ATR) × ham/düzeltilmiş oranı` olarak yaz. |
| 10 | ÇELİŞKİ | `izleme-09.md:34` | `TASARIM.md:823`; `TASARIM.md:828` | İşlem düzeyiyle günlük seri ayrılmalı denmiş; örnek hâlâ işlem başına getirinin yanına yıllık portföy güven aralığını koyuyor. | Sahip `TASARIM.md` §6.5: işlem başına farkı ve yıllık portföy aralığını ayrı ifadelerle göster. |
| 11 | ÇELİŞKİ | `izleme-11.md:53`; `AGENTS.md:17` | `izleme-17.md:31`; `TASARIM.md:812` | CSV başlıkları ASCII olmalı; sabit başlık listesinde `Giriş`, `Fiili risk`, `Kanıt` gibi Türkçe karakterli adlar isteniyor. | Sahip `AGENTS.md`: ASCII kuralını koru; TASARIM’daki CSV sözleşmesini `tarih`, `fiili_risk`, `kanit` gibi adlara çevir. |
| 12 | ÇELİŞKİ | `izleme-13.md:73` | `izleme-17.md:40`; `TASARIM.md:809` | Bir kabul edilmiş karar CSV’nin ilk satırına veri bilgisini, diğeri yalnız sütun başlığını koyuyor; tasarım veri bilgisini ayrıca `durum.txt` içine taşıyor. | Sahip `TASARIM.md` §6: CSV başlık düzenini koru; veri bilgisinin hangi sütunlarda veya dosyada bulunacağını tek yerde belirle ve `karar.md`ye istisnayı ekle. |
| 13 | ÇELİŞKİ — kısmi | `cevaplar-17-cikti.md:93`; `izleme-17.md:76` | `TASARIM.md:819` | CSV’deki `Kaynak` için “Tansu’dan esinlenen yorum” önerilmişken son tarif yalnız İş Yatırım ve görüntü kimliğini yazıyor; uyarının CSV’de nerede kaldığı belirsiz. | Sahip `TASARIM.md` §6.5: kaynak bilgisi ile yorum uyarısını aynı hücrede açıkça birlikte tanımla. |
| 14 | ÇELİŞKİ — kısmi | `izleme-15.md:47`; `karar.md:15` | `TASARIM.md:630` | Kabul edilmiş günlük alanları arasında `sema:1` var; TASARIM’ın alan listesinde şema sürümü yok. | Sahip `TASARIM.md` §5.11: `sema` alanını ve anlamını ekle. |
| 15 | ESKİ | `izleme-01.md:47` | `sonuc-3-4.md:106`; `TASARIM.md:114` | Okuma zaman aşımı 120 saniyeye çıkarılmış; C-8 hâlâ 30 saniye diyor ve TASARIM C-8’e atıf yapıp yeni değeri yazmıyor. | Sahip `TASARIM.md` §4: güncel `(5, 120)` değerini yaz; C-8’e sonraki kararın bağlantısını ekle. |
| 16 | ESKİ | `izleme-12.md:14`; `izleme-17.md:82` | `sonuc-3-4.md:107` | Kabul edilen değişiklikler test yüzlerine göstergeler ve raporu ekliyor; C-9 listesinde ikisi de hâlâ yok. | Sahip `TASARIM.md`: güncel test yüzlerini tek listede tut; C-9’u bu listeye yönlendir. |
| 17 | ÇELİŞKİ — kısmi | `izleme-02.md:74`; `karar.md:15` | `TASARIM.md:210` | Kabul edilen `ayar > 1`, aynı gün iki olay ve ±1 gün kayması sınama vakaları TASARIM’a aktarılmamış. | Sahip `TASARIM.md` §5.1: olay denetiminin bu üç doğrulama vakasını ekle. |
| 18 | ÇELİŞKİ — kısmi | `izleme-03.md:6` | `TASARIM.md:262` | Aynı şirketin kodları arasında seçim 60 günlük TL hacimle yapılmalı; tasarım yalnız “hacmi en yüksek” diyor ve pencereyi belirsiz bırakıyor. | Sahip `TASARIM.md` §5.2: kod seçiminin 60 günlük hacim ölçüsünü açıkça yaz. |
| 19 | ESKİ | `TASARIM.md:797` | `AGENTS.md:39` | Tasarım aylık taban yenilemesini elle yaptırıyor; AGENTS bunun için aylık zamanlanmış görev tanımlıyor. | Sahip `TASARIM.md` §6.2: aylık görevi esas al; kurulum ayrıntısı için AGENTS’e atıf ver. |
| 20 | KIRIK ATIF | `izleme-03.md:82` | `sonuc-3-4.md:46`; `TASARIM.md:910` | `sonuc B-3b` diye bir karar yok; `B3b`, TASARIM Ek A’daki eski eleştiri kimliği. | Sahip `izleme-03.md`: atfı `TASARIM Ek A, B3b` olarak düzelt. |
| 21 | ÇELİŞKİ | `cevaplar-15-kayit.md:88` | `cevaplar-19-cekirdek.md:140`; `sonuc-3-4.md:32` | Bir cevap 1.000 tekrarda `m ≥ 50` için kabulü imkânsız sayıyor, diğerleri sınırı `m > 50` koyuyor; m=50’de en küçük düzeltilmiş p yaklaşık 0,04995005. | Sahip `sonuc-3-4.md` O14: doğru sınırı koru; 15-078’e matematiksel düzeltme notu ekle. |
| 22 | TERİM | `GLOSSARY.md:25`; `izleme-10.md:47` | `TASARIM.md:817` | “Bozulma” yalnız SMA250 altı kapanışken `BOZULDU` karantina çıkışı ve giriş iptalini de kapsıyor. | Sahip `GLOSSARY.md`: hesap olayı “Bozulma” ile daha geniş kart durumu `BOZULDU`yu ayrı tanımla. |
| 23 | TERİM | `GLOSSARY.md:27` | `karar.md:41`; `TASARIM.md:291` | Sözlük bütün gün tek fiyat şartı koyuyor; ana işlem kuralı yalnız kapanışın limitte olmasını yeterli sayıyor. | Sahip `GLOSSARY.md`: gerçek kilit tanımı ile modelin kötümser giriş/çıkış engelini ayır; uygulama için §5.3’e bağlan. |
| 24 | TERİM | `GLOSSARY.md:9` | `sonuc-3-4.md:47`; `TASARIM.md:304` | Sözlük bütün çıkışları AOF’tan sayıyor; stop `min(stop, AOF)`, veri sonu çıkışı son kapanıştan. | Sahip `GLOSSARY.md`: AOF’u olağan dolum fiyatı olarak tanımla; istisnaları §5.3’e bağla. |
| 25 | TERİM | `GLOSSARY.md:14` | `sorgu-2.md:68`; `TASARIM.md:372` | Sözlük çift rotasyonunda her an bir hisse tutulduğunu söylüyor; ilk sinyale kadar nakit tutuluyor. | Sahip `GLOSSARY.md`: nakit dönemini içeren tanım kullan; ayrıntı için §5.6’ya atıf ver. |
| 26 | TERİM | `GLOSSARY.md:26` | `izleme-08.md:31`; `TASARIM.md:307` | “Fiili risk”, stopta kesin kaybedilecek tutar gibi tanımlanmış; karar planlanan risk ile gerçekleşen kaybı özellikle ayırıyor. | Sahip `GLOSSARY.md`: bunu stop seviyesine göre hesaplanan risk olarak tanımla; gerçekleşen kayıpla eşitleme. |
| 27 | ÇELİŞKİ | `KURALLAR.md:10` | `izleme-09.md:45`; `TASARIM.md:614` | KURALLAR her denenen YORUM değerini yeni deneme sayıyor; sağlamlık ızgarasındaki YORUM değerleri Holm denemesi sayılmıyor. | Sahip `TASARIM.md` §5.11: deneme sayımını burada tut; KURALLAR’daki genel ifadeye ızgara istisnasını ve atfı ekle. |
| 28 | TERİM — kısmi | `cevaplar-13-depolama.md:3`; `cevaplar-11-moduller.md:13`; `TASARIM.md:539` | `GLOSSARY.md:5`; `GLOSSARY.md:41` | Temel kavramlar olan “Anlık görüntü”, “Adım”, “Motor”, “maruziyet” ve “YORUM” sözlükte yok; tanımları başka belgelere dağılmış. | Sahip `GLOSSARY.md`: bu beş terimin kısa anlamını ekle; sayısal kuralları TASARIM’a bırak. |
| 29 | TEKRAR | `KURALLAR.md:112` | `TASARIM.md:341`; `TASARIM.md:357` | %1 risk, 2 ATR, SMA250 çıkışı ve %10 tavan iki belgede yeniden yazılmış. | Sahip `TASARIM.md` §5.5–5.6: KURALLAR’da yalnız risk paketinin hangi aileye uygulandığını ve bağlantısını bırak. |
| 30 | TEKRAR | `GLOSSARY.md:7`; `GLOSSARY.md:34` | `TASARIM.md:259`; `TASARIM.md:492` | Sözlük, evrenin 100 hisse sınırını ve K1 p formülünü ayrıca sahipleniyor. | Sahip `TASARIM.md` §5.2 ve §5.7: sözlükte kavram anlamını tut, sayı ve formüle bağlantı ver. |
| 31 | TEKRAR | `GLOSSARY.md:38` | `TASARIM.md:611` | Pozitif hücre tanımı, %0,3 masraf ve %60 sağlamlık eşiği sözlükte ve tasarımda ayrı ayrı yazılmış. | Sahip `TASARIM.md` §5.10: sözlükte yalnız ızgaranın anlamını ve bölüm atfını bırak. |

## Boşluklar

1. **Kod, testler ve gerçek koşular incelenmedi.** Eksik aktarım bulguları, ilgili davranışın kodda bulunmadığı anlamına gelmez.
2. **`.scratch/` biletleri kapsam dışında kaldı.** TASARIM’ın bilet açıklamaları okundu; bilet dosyalarındaki ek gerekçeler doğrulanmadı.
3. **Haricî kaynaklar ve Tansu görselleri yeniden doğrulanmadı.** Denetim, belgelerin birbirleriyle uyuşmasına yönelikti.
4. **Genel standart dosyaları karşılaştırma kapsamına alınmadı.** Bunların Tansu’ya özel olmaması bulgu sayılmadı.
5. **Denetim sabit bir Git sürümüne bağlı değildi.** Son kontrol 10.10.2026 14:25’te yapıldı; o sırada değişmiş olan `AGENTS.md` yeniden okundu.