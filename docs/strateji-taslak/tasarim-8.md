# TASARIM taslak 8 (öneri): strateji modülleri

Durum: öneri, sürüm 4 (06.10.2026; denetim `denetim-tasarim-8.md` Tur 0, 2 ve 3 işlendi; Tur 3 hükmü: koşullu kabul,
kalan düzeltmeler mekanik, yeniden denetim gerekmez). Levent onaylamadan
TASARIM.md'ye girmez; kod bu belgeden önce yazılmaz.
Dayanak: `docs/strateji-modulleri-taslak.md` (İ1–İ13, modül kataloğu; denetim 3 tur, kabul), `docs/sadakat.md`
(06.10 sadakat sonuçları) ve kodun bugünkü yapısı (aile = sinyal günü üreten fonksiyon, `aileler.py:50`; stop
`motor.py:13` sabit 2 ATR; hedef ve kısmi çıkış yok; yeni kural_id = Holm'da yeni (kural, aile) çifti, `kayit.py:99-120`).

## 1. Ne değişiyor

Taslak 7'de bir aile yalnız sinyal günü üretir; stop, çıkış ve boyut motorda sabittir. Tansu'nun işlemi ise bir
**kurulum hikâyesidir**: yapı bulunur, fiyat bölgeye gelir, tepki beklenir, geçersizlik ve hedef baştan yazılıdır.
Taslak 8 bu hikâyeyi motorun birimi yapar: **strateji modülü**.

**Değişmeyenler:** veri ve kapılar (5.1, 5.13), evren (5.2), T+1 AOF dolumu, tavan/taban kilidi, karantina, masraf,
K2 ve faiz, kabul ölçütleri (5.12; resmi kolda "işlem" tanımı 4.1'de, taslak 7 ile aynı), "AL denmez" (P1), "her aile bizim yorumumuzdur" (P5).

**Değişenler (taslak 7 kararlarını açıkça değiştirir):**
- **TASARIM 3, ikinci dalga (B-1):** AB=CD ilk dalgaya alınır. B-1'in gerekçesi SMRTG'ydi (aşağı yönlü); hamda alış
  yönlü örnek var: ISKPL (5/5 hedef, pozitif getiri; (T) R018 "AB=CD 1000 günlük C noktasından alım yapılsa idi D
  satış karları"). Alış yönlü hal yine "Tansu'nun kuralı" sayılmaz: etiket sadakat sonucuna göre verilir (5.1).
- **TASARIM 3, kapsam dışı:** AB=CD kapsam dışı listesinden çıkarılır (AB=CD harmonik ailedendir, R004; oran kapısı
  (T) R019). Gartley, Butterfly, Elliott kapsam dışı kalır.
- **TASARIM 5.5:** Resmi D1 kolu **hedeflidir** (D seviyesi; (T) R018 "D satış karları") ve stopu geçersizliktir; bu
  5.5'teki "hedef yok"tan sapmadır. Resmi D1 kolunda 2 ATR acil stop yok, SMA250 gün sonu çıkışı yok (kayıtta sabitlenir).
  D11 ve D12 resmi kolları 5.5'i aynen kullanır. Kısmi kâr ve ATR zinciri yalnız **ölçüm kolu** olur. 5.5'in gerekçesi
  ("ikinci el kaynaklı") artık tam değil: ATR zinciri hamda (T) R224, R239; bu yüzden ölçülür ama kabul kararına girmez.
- **TASARIM 5.12, boru hattı denetimi:** bugün yalnız ilk resmi koşudan önce aranıyor (`kayit.py:254`, TASARIM 698-700).
  Taslak 8: **her yeni kod hash'i** için denetim (yanlış kabul ≤ %5) geçmeden resmi koşu yok; `_resmi_bitti` istisnası
  kalkar. Maliyet (200 tekrar) kabul edilir.
- **TASARIM 4, "getiri gösteren tek yol kosu()":** ölçüm koşuları ayrı yoldan (`tur=olcum`) gelir; bu yol da kayıt ve
  hash denetimini aynı biçimde yapar.
- **TASARIM 5.8:** kural kaydı zamanı aynen kalır: "sadakat kontrolü bitince, **ilk getiri koşusundan** önce". Ölçüm
  koşuları da getiri koşusudur; bu yüzden kayıttan **sonra** yapılır. Kayıt, resmi kolu ve ölçüm kollarını birlikte
  yazar. **Yeni modüllerin (D1, D19) gerçek veride getirisi kayıttan önce hiçbir koşuda yazılmaz ya da görülmez;**
  geliştirme sentetik veri, boş dünya denetimi ve sayım koşularıyla yapılır. Bugünkü `resmi=false` geliştirme
  koşularının serbestliği (TASARIM 5.11) yeni modüller için kalkar. Geriye uyum testi (8.4) yalnız eski EMA özetini
  karşılaştırır; D1'i içermez.

## 2. Geri alınabilirlik: hangi karar kalıcı

| Karar | Geri alınır mı | Neden | Sonuç |
|---|---|---|---|
| Bu belge; sadakat ve sayım koşuları (getirisiz) | Evet, ucuz | Resmi kayda girmez | Serbestçe dene, ama ayar kümesi önceden yazılır (5.1) |
| Hash kapsamındaki dosyayı değiştirmek | Yarı | Her aile için yeni kural_id ve yeni Holm çifti; eski koşular silinmez | Tek seferde yap (8.7); m hesabı 5.3 |
| Bir kolu **resmi** koşmak | **Hayır** | Holm m kalıcı artar; 2015–2026 tümü geliştirme verisi (5.8) | Resmi koşuya modül başına önceden yazılmış **tek kol** |
| Ölçüm sonucuna bakıp kolu resmi yapmak | **Hayır** | Aynı veride, ~12 kol arasından seçim (kazananın laneti) | **Ölçüm kolu hiç resmi olmaz** (5.3.4); kodda engellenir |

Mevcut iki aile Deneme'de: ham K1 p'leri 0,7263 (EMA) ve 0,9441 (çift); Holm p'leri 1,0, m = 2 (`kayit/deneme.jsonl`).

## 3. Strateji modülü

### 3.1 Arayüz

Bir modül, bir hissenin günlük serisinden **kurulum** listesi üretir; işlem açmaz. Kurulum alanları:

- `modul`, `sembol`, `kurulum_id`
- `durum` geçişleri ve tarihleri (3.2)
- `noktalar`: modüle özgü (ör. AB=CD için A, B, C, D fiyat ve tarihleri) ve her noktanın **bilindiği gün**
- `giris_kollari`: her kol için giriş günü kuralı (3.3)
- `gecersizlik`: fiyat seviyesi ve kural (kapanış mı, fitil mi)
- `hedefler`: fiyat merdiveni (boş olabilir)
- `kaynak`: her kuralın etiketi `Tansu (T/G)` ya da `yorum (M/G-dış/eşik yok)`

Modül işlem yönetmez; pozisyonu yönetim katmanı açar ve kapatır (4).

### 3.2 Yaşam döngüsü (Tansu'nun etiketleri)

```
ADAY ──(giriş koşulu)──> AKTİF ──(tepki; yalnız tepki_teyidi)──> TEPKİ_VERDİ ──> TAMAMLANDI / BOZULDU
  │                        ├──(C_giris, D_limit: pozisyon açık)──────────────> TAMAMLANDI (hedef) / BOZULDU (geçersizlik)
  │                        └──(pencere doldu, tepki yok)──> BELİRSİZ
  └──(yapı bozuldu)──> BOZULDU
```

- "Tepki" (tepki_teyidi kolu): D'den sonra kapanışın D'nin üstünde ve D'den en az 1 ATR yukarıda olması (yorum; kayıtta
  sabitlenir).

- `ADAY`: yapı bulundu ve **doğrulandı** (pivotlar bilindi). AB=CD'de: A, B, C bilindi; C'nin bilindiği gün ADAY olur.
- `AKTİF`: kolun giriş koşulu sağlandı (C_giris'te ADAY günü; D_limit'te fiyat D'ye değdi; tepki_teyidi'nde D oluştu).
- `TEPKİ_VERDİ`: yalnız tepki_teyidi kolunda; giriş burada.
- `BELİRSİZ`: (T) R014 "10 gün içinde D noktasından bir tepki yapmıyor ise belirsiz bir yapı olarak bakılabilir".
- **Bakış ileri yok:** her geçiş yalnız o güne kadar bilinen veriyle yapılır. Pivot ancak sağındaki k mum kapandıktan
  sonra bilinir; haftalık pivot hafta kapanmadan bilinmez. Bu kural `test_gelecek.py`'ye girer (8.2).

### 3.3 Giriş kolları

Her kol ayrı simülasyondur (sermaye paylaşmaz). İlk dalgada D1 için:
- `C_giris` (**resmi kol**): C'nin doğrulandığı ADAY gününün ertesi AOF'unda al; çıkış D (hedef) ya da geçersizlik.
  Tansu'nun ISKPL tablosu C tarihinden girer (geriye dönük, "alım yapılsa idi"); biz C'yi ancak bilindiğinde alırız.
  Bu yüzden getiriler Tansu'nunkinden farklı çıkar; sadakat getiriyle değil geometriyle ölçülür (5.1).
- `D_limit` (ölçüm): D seviyesine limit; dolum modeli 4.3.
- `tepki_teyidi` (ölçüm): D'den sonra tepki (pencere 10 gün (T R014) ve 20 bar (görsel)), ertesi AOF.

## 4. Yönetim katmanı

### 4.1 Resmi kol: tek giriş, tek çıkış

İlk dalganın resmi kolları taslak 7 gibi tek giriş, tek çıkışlıdır: geçersizlik (stop) ya da modülün kendi çıkışı
(D1'de D seviyesi). Parçalı pozisyon resmi kola girmez. Böylece kabul hesapları (`istatistik.kabul`: n ≥ 100 işlem,
≥ 60 gün; ölçüt 4) ve K1 bugünkü işlem tanımıyla çalışır.

- **İptal:** giriş fiyatı (T+1 AOF) ≥ hedef ya da ≤ stop ise sinyal düşer (`iptal`), sayılır ve raporlanır; risk payı
  sıfır ya da negatif olmaz.
- **Ayar:** resmi kolun ayarı (pivot ayarı, doğrulama gecikmesi k, oran toleransı) kayıtta **varsayılan** olarak
  önceden yazılır. Sadakat adaylarından hiçbiri ya da birden çoğu tutarsa ayar yine varsayılandır; sadakat yalnız
  etiketi belirler.

### 4.2 Ölçüm kolları: parçalı pozisyon

- **İşlem = kurulum girişi.** Parçalar tek işlem sayılır: ağırlıklı çıkış fiyatı, ağırlıklı tutma süresi.
- **Risk** geçersizlik mesafesinden hesaplanır. Giriş fiyatı ≤ stop ise (boşluk) sinyal düşer (`iptal`); sıfıra bölme olmaz.
- Tavan %10 ve en çok 10 pozisyon **pozisyon** düzeyinde sayılır, parça değil.
- TP1 sonrası "stop girişe" planlanan riski sıfırlar; rapor bunu ayrı satırda yazar.
- Çıkış kolları (kaynağıyla): `hedef_merdiveni` / Fib iz süren (T R090); `atr_zinciri`: Giriş + 1.5 ATR iz süren
  mod aktivasyonu, sonra önceki gün dibi altı kapanışta %50, 2 ATR acil (T R224, R239; iki kaynağın sırası farklı,
  tek sıraya indirgemek yorumdur); `tp1_yari` (M R203, yorum); `sma250` (yorum).

### 4.3 D_limit dolum modeli (yeni; 5.3'e ek, değişiklik olarak işaretli)

Veride açılış yok, yalnız AOF, yüksek, düşük (TASARIM 5.1). Model muhafazakâr ve "üst sınır (iyimser)" etiketlidir:
- Temas: günün düşüğü ≤ limit − 1 fiyat adımı (TASARIM 5.1 adım tablosu); yalnız değip dönen gün dolmuş sayılmaz.
- Dolum fiyatı: limit. Adet: boyut sınırları ile temas günü hacminin %2'si arasındaki küçüğü.
- Aynı gün hem dolum hem stop koşulu varsa "stop" sayılır ve ayrıca raporlanır.
- Taban kilidinde dolmaz. 10 işlem günü içinde temas yoksa emir iptal. Açık ya da bekleyen pozisyon varken yeni sinyal
  düşer (`Zincir.kapali` mantığı).

### 4.4 Boyut ve rejim

- Boyut sınırları taslak 7 gibi (risk, tavan %10, likidite %2, nakit, en çok 10). Risk payı modülün geçersizlik
  mesafesidir (taslak 7'de 2 ATR). %1 risk yorum parametresidir (İ5).
- Rejim kapısı: şok freni (T R026, R092; pencere X yorum) yeni girişi durdurur; trend ve formasyon modüllerine uygulanır,
  ortalamaya dönüş ve çift muaftır. Ortalama kapısı ayrı ölçüm koludur.

Çift rotasyonu (D12) kendi döngüsünde kalır (`ciftbolme.py`); yalnız rapor biçimi ortaklaşır.

## 5. Sınama

### 5.1 Sadakat (getirisiz)

- **Ölçüt yalnız geometri ve tarih:** Tansu'nun örneğindeki noktalar (A, B, C, D seviyeleri, dönem başı ve sonu, gün
  sayısı) bizim dedektörümüzce **doğrulama gününde** bulunuyor mu? Hedef/stop sonucu (ISKPL "5/5 hedef") sadakat
  ölçütü değildir; getiriye bakmak olur (`sadakat.py:1` "Getiriye bakılmaz").
- **D1 ölçütü (ISKPL):** görsel yalnız 5 C tarihi veriyor (A–D seviyeleri yok). Eşleşme: dedektörün bulduğu ve oran
  kapısını (T R019) sağlayan bir AB=CD kurulumunun C pivotu, Tansu'nun C tarihine ±3 işlem günü içinde; doğrulama günü
  ≥ C. "Tutar" = 5 tarihin en az 4'ü eşleşir. **Şans tabanı:** aynı test ISKPL'de rastgele 5 tarihle (plasebo) koşulur;
  eşleşme oranı raporlanır; "tutar" ancak plaseboyu açıkça geçerse verilir. Örneği büyütmek için SMRTG'nin 12 C tarihi
  ayna dedektörle (kısa yön) aynı tarih kontrolüne eklenir (5 → 17 tarih); SMRTG getirileri sayılmaz.
- **Ayar kümesi önceden yazılır:** pivot ayarı, oran toleransı, doğrulama gecikmesi için denenecek adaylar ve eşleşme
  ölçütü sadakat koşusundan önce tarihli kayda girer; aday sayısı ve seçilen aday günlüğe yazılır (bugün Z için 1.564
  aday, `docs/sadakat.md`).
- **Sonuç yalnız etiketi belirler:** tutarsa kol "Tansu", tutmazsa "yorum". Resmi kol değişmez.
- **Bugünkü durum (06.10):** D11 kısmen (EMA20/50/100 üretti; dönem, gün, ortalama ve EMA200 üretmedi; dönem yalnız
  kırpılmış geçmişte tutuyor); D12 üretmedi (534 aday eşleşti, tek aday kalmadı); D1 sınanmadı. Yani ilk dalgada
  "Tansu" etiketi henüz hiçbir resmi kolda yok; hepsi yorum olarak kayda girebilir (P5).

### 5.2 Sayım koşusu (getirisiz)

Kayıttan önce modül başına evrende kurulum (sinyal) sayısı ve farklı giriş günü sayılır; simülatör çağrılmaz, getiri
sütunu yazılmaz. Sayım, işlem sayısının **üst sınırıdır** (boyut, likidite ve en çok 10 sınırından sonra işlem daha
azdır): üst sınır eşiğin altındaysa modül kesin yetmez; eşiği geçmesi yeteceği anlamına gelmez. 2015–2026'da n ≥ 100 işlem ve ≥ 60
farklı gün eşiğine (5.12 ölçüt 5) ulaşmayacağı görülen modül resmi sınava girmez (m boşuna artmaz); yalnız ölçüm olur.
Kâğıt üstü dönemde ≥ 30 kapanmış işlem / 12 ay eşiği (5.8) de sayımla öngörülür.

### 5.3 Kayıt, resmi sınav ve ölçüm

1. Kayıt (5.8 aynen): sadakat ve sayım bitince, ilk getiri koşusundan önce. Kayıt her modül için **resmi kolu**, ölçüm
   kollarını, K1 tanımını (5.4) ve kapı parametrelerini birlikte yazar.
2. Resmi sınav: yalnız resmi kol; K1 + Holm (5.11–5.12).
3. Ölçüm: kayıttan sonra, kollar yan yana; p değeri yok, "keşif, kabul kararı değildir" yazısı. Ölçüm kolları
   `AILELER` dışında ayrı yoldan koşar (`tur=olcum`, K1 yok); kod "p yok" kuralını böyle zorlar.
4. **Ölçüm kolu hiç resmi olmaz.** Kâğıt üstü dönemde tek kol için güç yok (6 ayda saptanabilir en küçük etki yıllık
   ≈ %56, TASARIM 5.8); bu yüzden "kâğıt dönemde resmi sınav" yolu tanımlanmaz. Yeni bir fikir yeni modül olur (yeni kod,
   kendi kaydı, kendi resmi kolu). **Kod koruması:** kol kimliği adı değil, içerik özetidir (sha256: modül + giriş
   kuralı + çıkış kuralı + ayar parametreleri). Ölçüm günlüğü resmi kolu `referans=true` ile yazar; kayıt, kimliği daha
   önce `olcum_kolu=true` olarak görülmüş bir kolu resmi kol yapmayı reddeder; bir test bunu sınar. Sınır: kod yalnız
   aynı içeriği engeller; ölçümden esinlenmiş yeniden tasarımı engelleyemez. Bu disipline ve kayıt tarihine bağlıdır.
5. **m hesabı:** hash kapsamındaki ilk değişiklik her aile için yeni kural_id açar. `AILELER` tam olarak {D1, D11
   (`ema_sikismasi` adıyla), D12 (`cift_rotasyonu` adıyla)} olur → yeni 3 çift; eski 2 çift günlükte kalır → m = 5.
   K1 tekrar sayısı B = max(1.000, 200·m) = 1.000. Eski EMA adı D11'den ayrı kalırsa m = 6, B = 1.200. D12'nin kuralı
   değişmese de yeni kural_id ile aynı hipotez ikinci kez Holm'a girer (m şişer, p aynı): kabul edilen maliyet.
6. **Hash ve ölçüm kodu:** resmi p'yi etkileyen kod (modüller, ortak yapı taşları: pivot, oran; yönetim katmanının
   resmi kol yolu) `KOD_DOSYALARI`'ndadır. Ölçüme özgü kod (parçalı pozisyon, çıkış kolları, D_limit dolumu, ölçüm
   raporu) ayrı bir hash dışı dosyadadır (`olcum.py`, `HASH_DISI`). Kayıttan sonra yalnız bu dosya değişebilir; hash
   içi bir dosya değişirse yeni kayıt ve yeni çiftler gerekir (her seferinde m +3). Hash içi kod `olcum`'u import
   etmez; bir test AST ile import taraması yapar. Ölçüm günlüğü satırları `olcum_hash` ve `git_commit` yazar.

### 5.4 K1 modüller için (kayıttan önce yazılır; yazılmazsa modül resmi olamaz)

- **Sınanan hipotez:** TASARIM 5.7 gibi "kural, kendi ön şartını sağlayan rastgele günlerden iyi mi". D1'de ön şart =
  doğrulanmış salınım dibi (C benzeri); kural = ön şart + AB=CD oran kapısı (T R019). Yani K1 "oran kapısı, aynı risk/ödül
  yapısıyla rastgele salınım dibinden iyi mi" sorusunu sınar. Risk/ödül yapısının katkısı K1'e girmez; ölçüt 2'de
  (K2'ye karşı) görünür. Bu bilinçli tercihtir.
- **Ön şartlı gün havuzu:** doğrulanmış salınım dibi günleri (oran kapısı uygulanmadan); EMA K1 gibi evren üyesi,
  karantina penceresi dışı, ısınma tamam (`istatistik.py:44-49` filtreleri). Rastgele giriş bu havuzdan çekilir.
- **Stop ve hedefin aktarımı:** sinyaldeki yüzde mesafe korunur (giriş fiyatına göre stop ve D mesafesi yüzde olarak
  rastgele girişe taşınır).
- **Tür a / tür b ve p kuralı:** taslak 7 gibi. Tür (a): aynı gün, havuzdaki başka hisse. Tür (b): aynı hisse, ±20 işlem
  günü içindeki havuz günü. Aile p'si ikisinin büyüğüdür.
- **Önbellek:** `Zincir.tek(i)` anahtarı (konum, stop %, hedef %) olur. Hit oranı düşeceği için B = 1.000 süresi kayıttan
  önce bir deneme koşusuyla ölçülür; süre kabul edilemezse yüzde mesafeler 0,5 puanlık kovalara yuvarlanır (yorum).
- D12 rolling kapı ölçüm kolunda: K1 havuzuna da aynı kapı uygulanır; boş dünya denetimine (`denetim.py`) rolling kapılı
  varyant eklenir; pencere ve eşik önceden yazılır.

## 6. Rapor ve kart

- Rapor modül başına bölümdür: kurulum sayıları durum durum, resmi kol sonucu, ölçüm kolları ayrı başlıkta ("keşif"),
  sadakat sonucu, kaynak etiketleri.
- Akşam kartı: o gün durum değiştiren kurulumlar (`ADAY`, `AKTİF`, `TEPKİ_VERDİ`, `BOZULDU`, `TAMAMLANDI`, `BELİRSİZ`),
  geçersizlik ve hedef seviyeleri. Dil değişmez: "kural sağlandı".

## 7. İlk dalga

| Modül | Resmi kol | Ölçüm kolları | Sadakat (geometri) | Bugünkü sadakat |
|---|---|---|---|---|
| D1 AB=CD | `C_giris` (C doğrulandıktan sonra), çıkış D ya da geçersizlik (T R019) | `D_limit`, `tepki_teyidi`, `atr_zinciri`, `hedef_merdiveni` | ISKPL 5 C tarihi (+ SMRTG 12 C tarihi, ayna dedektör) ±3 işlem günü, plaseboya karşı (5.1) | sınanmadı |
| D11 EMA sıkışması | KRDMD ayarı (EMA20/50/100/200, tolerans %1,2, min 3 gün); giriş tetiği bugünkü `aileler.sinyal` (yorum; Tansu tetiği vermiyor, R125) | EMA 5-8-13 (T R198), breakout/retest (M R198), eğim (İ13) | KRDMD 17.12.2025 → 14.01.2026, 20 gün, %0,64 | kısmi |
| D19 RSI 30 | yok: yalnız ölçüm (örnek grafik yok); hiç resmi olmaz (5.3.4) | kuralın kendisi (M R233) + 2 ATR acil | yok | – |
| D12 çift rotasyonu | mevcut kural (log oran, 60 gün; yorum) | rolling kointegrasyon kapısı (T R034, R228; varsayım) | VAKBN–GARAN | üretmedi |

Taslak 7'nin EMA sıkışması ailesi D11 olur (aynı fikir).

## 8. Uygulama sırası (öneri; biletler ayrıca yazılır)

1. Modül arayüzü + yaşam döngüsü + ortak yapı taşları (pivot, oran) yalnız ilk dalganın ihtiyacı kadar.
2. `test_gelecek.py` genişletilir: pivot, oran, durum makinesi, haftalık mum (bakış ileri yok).
3. D1 dedektörü + sadakat (geometri) + sayım koşusu. D11 sadakat sonuçları zaten görüldü (`docs/sadakat.md`); resmi
   kolu değişmediği için sızıntı yok, yeniden koşu yalnız etiket içindir.
4. Ölçüm yolu (`tur=olcum`): parçalı pozisyon, çıkış kolları, D_limit dolum modeli. Taslak 7 davranışı bir kol olarak
   korunur. Geriye uyum: aynı anlık görüntüde EMA ailesinin sonuç özeti `kayit/deneme.jsonl` `bitti.ozet` ile aynı
   (kod hash'i değişecek; karşılaştırma yalnız özet içindir).
5. K1 modül tanımı (5.4), `AILELER` ve `kayit.hesapla` genelleştirmesi, `saglamlik.IZGARA`, `KOD_DOSYALARI` ve
   `tests/test_kayit.py` kapsam listesi.
6. Rapor ve akşam kartı.
7. Boru hattı denetimi yeni kod hash'iyle yeniden: `denetim.etki_ekle` D1 için tanımlanır (etki C_giris giriş günü
   AOF'una); yanlış kabul ≤ %5 olmadan resmi koşu yok. `kayit.py:254` koşulu "her yeni kod hash'i" olur
   (`_resmi_bitti` istisnası kalkar).
8. Kayıt (tek seferde, bir kural_id değişimi), sonra resmi koşu, sonra ölçüm.

## 9. Açık sorular

1. (Kapandı: ölçüm kolu hiç resmi olmaz, 5.3.4.)
2. D11'in giriş tetiği yorum ve sadakati kısmi: resmi kolda kalsın mı, ölçüme mi insin? (Öneri: kalsın, "yorum" etiketiyle;
   taslak 7 ile süreklilik.)
3. D1'in sayım koşusu eşik altında çıkarsa (haftalık, seyrek kurulum) D1 yalnız ölçüm olur. Kabul mü? (Öneri: evet.)
4. Pivot ayarı hiçbir kaynakta yok: sadakat için önceden yazılmış küçük bir aday kümesi (ör. 3 değer) yeterli mi?
5. Momentum ön elemesi (T R189) ilk dalgada yok; sonuç bu notla okunur.
