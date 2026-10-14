# Bilet 03 raporu: TASARIM kendi içinde ve karar kayıtlarıyla tutarlı (14.10.2026)

Satır numaraları denetimlerin (10.10) numaralarıdır; "bugünkü yer" TASARIM'ın bugünkü bölümüdür. Kod değişmedi; kural
parametresi değişmedi; getiriye bakılmadı. `docs/sorgu/` yerel (git dışı): oradaki iki düzeltme (`karar.md` üç satır,
`izleme-03.md` bir atıf) commit'e girmez.

## Bulgu tablosu

### `hiza-e.md` 1–21 ve 27

| Kaynak | Bugünkü TASARIM yeri | Karar kaynağı | Yapılan |
|---|---|---|---|
| e-1 `veri/` 30 gün silme | 6.2 Veri; 5.11 Silme yasağı | karar.md:24 (20-033) | düzeltildi: 30 gün maddesi kalktı; 11-061 `karar.md:30`'a RED olarak yazıldı. Kod: bilet 07'ye |
| e-2 Holm masrafı %0,3 / %0,5 | 5.11 Holm | izleme-15 15-065, izleme-09 09-056, 5.12 ölçüt 3 | düzeltildi: %0,5 kalır; 09-056'nın masraf kısmı `karar.md:31`'e istisna olarak yazıldı (ızgara kısmı kalır). Davranış değişmedi |
| e-3 yıllık fazla getiri iki formül | 5.7 K2 "Fazla getiri (rapor)"; 5.8 | izleme-08 08-083 | düzeltildi: tek tanım = günlük fazla getirinin yıllık toplamı (5.8). Kod: bilet 07'ye |
| e-4 "K1'e göre" belirsiz | 4 `saglamlik`; 5.10 Pozitif hücre | izleme-09 09-064 | düzeltildi: sepete göre işlem başına fazla getiri, K1 tekrarı yok; tek anlatım |
| e-5 yarım resmi koşu m'si | 5.11 yeni "Deneme sayısı (m), tek tanım"; 5.7 tekrar sayısı | izleme-15 15-044 | düzeltildi: m tek yerde (5.11); 5.7 ve 5.12 atıf verir. Kod: bilet 07'ye |
| e-6 ilk sinyal 30.11.2015 / simülatör başlangıcı | 5.1 İndirme; 5.6 Simülatör başlangıcı | sonuc-3-4 B-6 vs bilet 10 | Levent'e soru 1 |
| e-7 karantinada bacak | 5.6 Çift bölmesi; Çift bölmesi kuralları, Engeller | izleme-02 02-082, cevaplar-02 02-082 | Levent'e soru 2 |
| e-8 50/50 alım günü | 5.6 Tanısal 50/50; 5.7 K2 Çift bölmesi | izleme-04 04-057; 03-051, 08-054 | düzeltildi: seçim günü yılın ilk işlem günü, alım ertesi günün AOF'u (geleceği görmeme); 5.7 aynı tarihe bağlandı. Davranış değişmedi |
| e-9 ham stop | 6.5 Referans ve Stop | izleme-01 01-079 | düzeltildi: stop = (düzeltilmiş referans − 2 ATR) × oran. Kod zaten böyle (`gunluk.py:90-95`); kod değişmez |
| e-10 kanıt örneği | 6.5 Kanıt satırı, Kanıt örneği | izleme-09 09-041 | düzeltildi: tek tanım; işlem düzeyi ve günlük seri aralığı ayrı ifade; örnek `gunluk._kanit` biçimine eşit |
| e-11 CSV başlıkları ASCII | 6.5 Sabit sütunlar | izleme-11 11-051, AGENTS Adlar | düzeltildi: `tarih`, `hisse`, … `likidite_siniri_tl`, `kanit`, `kaynak`. Kod: bilet 07'ye |
| e-12 CSV ilk satır veri bilgisi | 6.4 | izleme-17 17-050, 17-087 vs izleme-13 13-082 | düzeltildi: CSV ilk satırı başlık; veri bilgisi `durum.txt`'te; 13-082'nin CSV kısmı `karar.md:32`'ye RED |
| e-13 `Kaynak` ve yorum uyarısı | 6.5 (Bilet 14) Tarih/Kaynak | izleme-17 17-087 | düzeltildi: aynı hücre "Tansu'dan esinlenen yorum · İş Yatırım <kimlik>". Kod: bilet 07'ye |
| e-14 `sema` alanı | 5.11 Alanlar | izleme-15 15-046 | düzeltildi: `sema` (şimdilik 1). Kod: bilet 07'ye (`kayit.py` yazmıyor) |
| e-15 okuma zaman aşımı | 4 `kaynak` | izleme-01 01-057 | düzeltildi: (5, 120) sn; kod uyumlu (`kaynak.py:57`) |
| e-16 test yüzleri | 4 yeni "Test yüzleri" | izleme-12 12-018, izleme-17 17-093 | düzeltildi: tek liste (C-9 + göstergeler + rapor). Rapor testi (17-093) yok: bilet 07'ye/06'ya not |
| e-17 olay denetimi vakaları | 5.1 Olay denetimi | izleme-02 02-093 | düzeltildi: üç sınama vakası eklendi |
| e-18 kod seçiminde 60 gün hacim | 5.2 Evren kuralı | izleme-03 03-004 | düzeltildi: 60 günlük medyan TL hacim; K2'de çift ağırlık yok. Kod uyumlu (`evren.py`) |
| e-19 evren-indir elle | 6.2 Veri | AGENTS Task Scheduler | zaten düzeltildi (bilet 09): `TansuAylik` metni var |
| e-20 kırık atıf `sonuc B-3b` | (izleme-03:82; TASARIM'da yok) | TASARIM Ek A B3b | düzeltildi: `izleme-03.md:82` "TASARIM Ek A, B3b" (yerel dosya) |
| e-21 "m ≥ 50 imkânsız" | 5.7 Tekrar sayısı | sonuc O14, izleme-15 15-078, 19-068 | çürütüldü: TASARIM'da bu iddia yok; el hesabı: B=1.000'de m=50 için 50/1.001 ≈ 0,04995 < 0,05 (mümkün), m>50 imkânsız. Not 5.7'ye yazıldı; cevaplar dosyası değişmedi |
| e-27 KURALLAR YORUM sayımı / ızgara | 5.10, 5.11; KURALLAR:10 | izleme-09 09-056, karar.md:28 | düzeltildi: KURALLAR'a ızgara ve masraf senaryosu istisnası ve atıf eklendi |

### `hiza-b.md` 1, 7, 8

| Kaynak | Bugünkü yer | Karar kaynağı | Yapılan |
|---|---|---|---|
| b-1 EMA K1 ön şartı | KURALLAR:108; TASARIM 5.7 Tür (a)/(b) | TASARIM 5.7 (bilet 13) | düzeltildi: KURALLAR (a) ve (b) şartlarını ayrı yazar; sahibi KURALLAR §3 |
| b-7 YORUM değeri = deneme | KURALLAR:10; TASARIM 5.10 | 09-056 | düzeltildi (e-27 ile aynı düzeltme) |
| b-8 Holm birimi | 5.11 Holm ilk madde | bilet 12 (aynı bölüm) | düzeltildi: "(kural kimliği, aile) çifti" |

### `tasarim-kod.md` §4

| Madde | Bugünkü yer | Karar kaynağı | Yapılan |
|---|---|---|---|
| Piyasa durumu K1(b) / "yalnız bilgi" | 6.3 | izleme-11 11-078 | düzeltildi: kart ve motoru etkilemez; K1 (b) ve rapor bölmesinde kullanılır |
| Geliştirme Holm p'si | 5.7 Tekrar sayısı; 5.11 | 09-009, bilet 12 | düzeltildi: dev p'leri günlükteki Holm listesine ve m'ye girmez; rapor yalnız varsayımsal Holm p'si gösterir |
| Hash kapsamı / tekrar sayısı | 5.8 Hash kapsamı | karar.md:28 (15-006) | düzeltildi: B'nin değeri hash dışı (günlükte alan), B'yi hesaplayan kod hash içi |
| İki kanıt satırı | 6.5 | 09-041 | düzeltildi (e-10 ile aynı) |
| Komut listesi | 4 `__main__` | bilet 09 | zaten düzeltildi (bilet 09) |

## Sayılar

düzeltildi 25 · çürütüldü 1 · zaten düzeltildi 2 · Levent'e soru 2 (toplam 30 madde; b-7 ile e-27 ve tasarim-kod
"iki kanıt satırı" ile e-10 aynı düzeltmeyi paylaşır).

## Bilet 07'ye (kod değişikliği; bu bilet kodu değiştirmedi)

1. `tansu/gunluk.py:218-232`: 30 günden eski günlük anlık görüntüleri silen temizlik kalkar (e-1). `tests/test_gunluk.py` bu silmeyi sınıyorsa test de karar gereği değişir.
2. `tansu/simulator.py:_yillik`: yıllık fazla getiri yıl sonu özkaynak getirilerinin farkıdır; karar günlük farkların toplamıdır (e-3). Ölçüt 4'ü ve rapor sütununu etkiler.
3. `tansu/kayit.py:tekrar_sayisi`: m yalnız `bitti` satırı olan resmi p'lerden kurulur; yarım kalan resmi koşu sayılmaz (e-5; `deneme_sayisi()` sayıyor).
4. `tansu/gunluk.py:SUTUNLAR`: başlıklar ASCII olur (e-11). `kayit/kartlar.jsonl` anahtarları bu adlardan gelir; yalnız-ekleme günlükte anahtar adı değişir, eski satırlar eski adla kalır.
5. `tansu/gunluk.py:_kart` `Kaynak` hücresi: "Tansu'dan esinlenen yorum · İş Yatırım <kimlik>" (e-13).
6. `tansu/kayit.py`: günlük satırlarına `sema: 1` (e-14; yalnız-ekleme, geriye dönük değişmez).
7. 17-093 rapor testi (sütun listesi, yasaklı kelime) yok (e-16).
8. `tansu/denetim.py:38` docstring "β" → "piyasa yükü" (yalnız ad).

## Levent'e sorular

(Soru 1) **İlk sinyal günü: 30.11.2015 mi, 01.12.2015 mi?** Kayıt (sonuc-3-4 B-6, TASARIM 5.1): "İlk sinyal 30.11.2015". Kod ve TASARIM 5.6: simülatör 01.12.2015'te başlar ve bu günden önceki sinyal gününü saymaz, yani 30.11.2015 sinyali sayılmaz (`simulator.ilk_gun`, `sinyal_tarih >= ilk`).
1. Kayda uy: 5.6 "ilk sinyal günü 30.11.2015, ilk dolum 01.12.2015" olur; kod değişir. Değişen: ilk günün sinyali (varsa) işleme girer, sonuçlar ve p değerleri kayabilir, yeni deneme sayılır. Risk: kural kaydı hash'i değişir, ön koşu rakamları eskir.
2. Koda uy: 5.1 "ilk sinyal" cümlesi "±%20 rejiminin başı 30.11.2015; sinyal günleri 01.12.2015'ten sayılır" olur; kod değişmez. Değişen: yalnız belge. Risk: kayıtla birebir aynı değil; 30.11 sinyali hiçbir zaman sayılmaz.

(Soru 2) **Çiftte bir bacak karantinaya girince ne olur?** Kayıt (02-082): "bir bacak karantinadaysa çift o pencerede girişsiz kalır, açık bacak son temiz AOF'ta kapanır". Kod ve 5.6 ayrıntısı: yalnız tutulan bacakta karantina varsa kapanır; tutulmayan bacak karantinadaysa çift yeni girişsiz kalır, tutulan bacak durur. Kayıt "hangi bacak" demiyor ve tutulmayan bacak karantinadayken tutulan bacağın hangi "son temiz AOF"ta kapanacağını söylemiyor.
1. Bugünkü kod: yalnız tutulan bacağın karantinası kapatır. Değişen: yalnız 5.6'nın ilk cümlesi "tutulan bacak" diye daraltılır. Risk: tutulmayan bacaktaki veri sorunu pozisyonu etkilemez; kayıtla "iki bacaktan biri" okuması uyuşmaz.
2. İki bacaktan biri karantinadaysa pozisyon kapanır (kapanış fiyatı tutulan bacağın son temiz AOF'u). Değişen: kod ve 5.6 ayrıntısı. Risk: sonuçlar kayabilir; yeni deneme; kapanış fiyatı için ayrı karar gerekir.
3. Bugünkü kod kalsın ve 02-082'yi `karar.md`'ye "Kısmen" yaz (yalnız tutulan bacak). Değişen: yalnız belge. Risk: kayıtla bilinçli sapma.

## Sözlük denetimi kutuları (TASARIM tarafı)

- Bilet 01: 5.13 "tüm evren" → "indirilen bütün hisseler/semboller" (3 yer); çift rotasyonundaki "hedef" = geçilecek bacak, 5.6'da ilk kullanımda yazıldı; yarım kalan resmi koşunun m katkısı yalnız 5.11'de.
- 2. tur: 5.3 "kayma yalnız çıkış dolumunda; giriş dolumu kaymaz" ve 5.13 "çıkış dolumu kayar, giriş bekleyen sinyal düşer" (motor `adim` ile doğrulandı); 5.10 "K1'e göre" → sepete göre, K1 tekrarı yok (tek anlatım); 5.12 "ileri yürüme yılları" → "yıllık sonuç dilimleri", 5.8'e not.
- 3. tur: 5.1 "baz fiyat" (tavan/taban baz fiyatın ±L'si; `taban` adı yalnız limit anlamında kaldı); 5.7 K1 "düşer" → "yeni işlem açmaz ve sayıma girmez"; 5.6 "ilk geçiş" → "ilk giriş"; 5.3 R = giriş − stop; 5.5 gerçek aralık formülü (`gostergeler.atr` ile doğrulandı).
- Tansu denetimi: 5.12 ve 5.8 yukarıdaki ad ve not (parametre optimize eden ileri yürüme değildir).
- 6. tur: 5.9 çift bölmesinde geçiş sayısı = tutuş dönemi sayısı, nakitten ilk giriş dahil (`ciftbolme.py:444` ile doğrulandı); sentetik dünyanın "β"sı 5.12'de "piyasa yükü" (GLOSSARY:89 "β iki anlamı vardır" satırı bu adı henüz anmıyor; sözlük sahibine not).
- 10. tur: 5.7 K1 "düşer" düzeltildi; 5.13'te yalnız hacmi farklı tekrar satır = yapısal ihlal, indirme durur (`veri.py:200` `drop_duplicates` hacmi dahil eder).
