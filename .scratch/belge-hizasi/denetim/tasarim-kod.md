# TASARIM değişmez kuralları ile kod ve test (10.10, Claude okuyucu ajanı)

Kaynak: `docs/TASARIM.md` (taslak 7) baştan sona; `tansu/*.py`, `tests/*.py`. Test varlığı çoğunlukla test adından
çıkarıldı; içeriği açılmayan test yüzünden 67 sayısı düşebilir. Satır numaraları 10.10 durumudur.

Sayım: yaklaşık 95 değişmez kural; 67'sinde kod ve test var, 28'inde biri eksik.

## 1. Kararlı, kodu yok
1. Kayıt sadakat kontrolünden sonra yapılır (TASARIM:568). `kayitla()` (`kayit.py:112`) sadakat satırı aramıyor.
2. Kâğıt dönemi en az 6 ay ve 30 işlem, tek bakış, 12 ayda dolmazsa Ölçülemedi (TASARIM:584-587). Ölçüt 6
   `istatistik.py:357-362`'de sabit Ölçülemedi.
3. Canlı durumu yok (TASARIM:674). `istatistik.py:383` yalnız Kâğıt ya da Deneme döndürür.
4. Karantina maskesi K2'ye de uygulanır (TASARIM:243). K1'de var (`istatistik.py:49`), K2'de yok. Kısmi.
5. `duzeltme` satırı asıl satırı değiştirmez (TASARIM:641). Kodda `duzeltme` yok.
6. Yakalanmayan istisna günlüğe yazılır (TASARIM:145). `__main__.py:178` yalnız iki istisna türünü yakalar.
7. Ölçüt değişirse ayrılmış dönemler sıfırlanır (TASARIM:60). Sıfırlayan kod yok. Kısmi.
8. Uyarı yoksa "Uyarı yok" yazılır; bulunamayan semboller uyarıya girer (TASARIM:849-850). `rapor.py:219-247`'de yok.
9. Blok uzunluğu ve masraf senaryoları günlükte ayrı alan (TASARIM:580). `basladi` satırında blok yok. Kısmi. **Kapandı (bilet 07f, 15.10; TASARIM 5.8):** blok uzunluğu çıktıdır, günlük alanı değildir; masraf düzeyi başına sonuç `masraf_sonuc` alanıdır.

## 2. Kodda var, testi yok
- Aynı gün sırası çıkış, giriş, değerleme (TASARIM:297, 441): `simulator.py:103-124`. Kısmi.
- Bağlayıcı sınır eşitlikte risk, tavan, likidite, nakit sırası (TASARIM:451): `simulator.py:19,121`.
- Eşitlikte sembol adı alfabetik (TASARIM:363): `simulator.py:105`.
- Ek kol aile p'sine girmez (TASARIM:519): `istatistik.py:151`.
- Olay denetimi gün oranı %2'yi aşarsa koşu sorunlu (TASARIM:769): `veri.py:39,125`.
- Tarih sütunu saat dilimsiz (TASARIM:139): `kaynak.py:88`.
- Bağımlılık yönü tek yönlü (TASARIM:147).
- Piyasa durumu motoru etkilemez (TASARIM:85): `gostergeler.py:18`.
- Göstergeler düzeltilmiş seriden, limit ve kilit ham seriden (TASARIM:203-206): `motor.py:219-226`.
- Hash yorum ve boşluktan etkilenmez (TASARIM:579): `kayit.py:78`.
- Kart durumları STOP/BOZULDU, kapanmış kart bir gün görünür (TASARIM:816-818): `gunluk.py:80-84,139-144`.
- Çift ailesi Kâğıt olursa koşu SORUNLU (TASARIM:822): `gunluk.py:132-133`.
- Rapor dosyası üstüne yazılmaz (TASARIM:846): `rapor.py:325`, `kayit.py:436`.
- İş Yatırım istekleri arası 1 sn (TASARIM:183-184): `kaynak.py:57`; testler `bekleme=0`.
- VAKBN–GARAN kabul kararına girmez (TASARIM:397): `ciftbolme.py:436`. Kısmi.
- Evrenden çıkan pozisyon kendi kuralıyla kapanır (TASARIM:264): `motor.py:244-246`. Kısmi.
- Yokluk kuralları: Yahoo/TradingView yok (TASARIM:164,179), valör yok (336), çift bölmesinde stop ve hedef yok
  (345-346), fiyat yamanmaz (242).

## 3. Kod TASARIM'dan farklı
- `__main__.py:24,27` `borsapy.companies()` ile ağa çıkar; TASARIM:114 ağa çıkan tek yer `kaynak` der.
- `kayit.py:136` `deneme_sayisi` geliştirme koşularını da sayar (TASARIM:657). Kısmi.
- `kayit.py:419` `0 < tekrar` koşulu `resmi=True, tekrar=0`'da B kontrolünü atlar (TASARIM:527). Kısmi.
- `istatistik.py:394-395` gerçek istatistik NaN ise p=1 döner; TASARIM:491-495 söylemez.
- `gunluk.py:198` yalnız AKTİF kartların hisselerini indirir (TASARIM:792-794 "açık kartlar"); STOP/BOZULDU açık
  pozisyonlar düşebilir. Kısmi.
- `veri.py:447` limit tabanı için önceki temiz kapanışı kullanır; TASARIM:216 ham kapanış der. Kısmi.
- `veri.py:451-453` olay eşleştirmesinde ±1 gün yok (TASARIM:213, olay denetimi için). Kısmi.
- `motor.py:48` giriş günü karantinadaysa sinyali düşürür; TASARIM:295 bunu saymaz.
- Piyasa durumu etiketi hiçbir çıktıda yok; TASARIM:85-86 rapor bölmesinde kullanılır der.
- `kayit.py:30-42` dosyaları bütün hash'ler; `MASRAFLAR`, `K1_MASRAF`, `GELISTIRME` hash'e girer; TASARIM:580-581
  tekrar sayısı ve masraf senaryolarını hash dışı sayar.

## 4. TASARIM içi çelişkiler
- TASARIM:85 ve 480 piyasa durumunu K1(b)'de kullanır; TASARIM:804 "yalnız bilgi" der.
- TASARIM:489 geliştirme p'leri Holm'a girmez; TASARIM:661-662 geliştirme Holm p'sini varsayımsal hesaplar.
- TASARIM:580-581 tekrar sayısı hash dışı; TASARIM:576-577 `kayit.py` bütünüyle hash içinde.
- TASARIM:823-825 ve 826-829 iki ayrı "Kanıt satırı" tanımı; 828'deki örnek işlem başına getiriyle günlük seri
  aralığını karıştırır.
- TASARIM:129 komut listesi `sektor-indir` ve `evren-indir`'i saymaz (TASARIM:171, 797).

Taslak 8 (`docs/strateji-taslak/tasarim-8.md`) ile farklar onay bekleyen öneridir, çelişki sayılmaz
(taslak 8 kendi metninde TASARIM'ı değiştirmediğini söyler).
