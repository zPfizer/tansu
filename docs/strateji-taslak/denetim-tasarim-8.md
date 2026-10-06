# Denetim: tasarim-8.md (TASARIM taslak 8 önerisi)

Okuma anı: 06.10.2026 ~13:50. Denetlenen: `docs/strateji-taslak/tasarim-8.md` (134 satır). Karşılaştırılan: `tansu/motor.py`, `simulator.py`, `aileler.py`, `ciftbolme.py`, `kayit.py`, `istatistik.py`, `sadakat.py`, `saglamlik.py`; `docs/TASARIM.md` (§1, §2, §3, §5.5, §5.8, §5.11, §5.12), `docs/sadakat.md`, `kayit/deneme.jsonl`, `tests/test_kayit.py`; `docs/strateji-modulleri-taslak.md` (kabul edilen sürüm).

Kısa sonuç: "Kod bugün şöyle" iddialarının hepsi doğru. Sorun kodda değil, yöntemde: belgenin temel kuralı ("resmi sınava yalnız sadakat kolu") üç resmi adayın hiçbirinde bugünkü kanıtla sağlanamıyor, TASARIM 3, 5.5 ve 5.8'i sessizce değiştiriyor ve çoklu test deliğini tam kapatmıyor.

## Bulgular

### YÜKSEK

**Y1. "Resmi kol = Tansu'nun gösterdiği hali" önkoşulu üç resmi adayda da sağlanmıyor; belge bunu söylemiyor.**
- Yer: §2 "Ana kural: bir modül resmi sınava Tansu'nun gösterdiği haliyle (sadakat kolu) girer"; §7 tablo "Sadakat kolu (resmi aday)".
- Kanıt, D11: `docs/sadakat.md:13-19`: bütün geçmişle (üretimde kullanılan ayar) KRDMD dönemi 2025-12-16 → 2026-01-14, 21 gün, ort. %0,665; Tansu 17.12 → 14.01, 20 gün, %0,64: "üretmedi". EMA200 üç adayın üçünde de "üretmedi" (satır 19, 31, 43; fark 0,0052–0,0070 > ±0,005). Dönem yalnız "son 3 yıl"/"son 2 yıl" kırpılmış geçmişte tutuyor (Tansu'nun yfinance uzunluğu bilinmiyor; kırpma uzunluğu sonradan seçilen aday). Üstelik D11'in resmi kolu bugünkü `aileler.sinyal` (kırılım tetiği: `aileler.py:50-63`), yani "giriş tetiği bugün yorum" (§7, satır 112 kendi sözü); Tansu giriş tetiğini vermiyor (R125 "parametrelerin detaylarını verip stratejimi anlatamam").
- Kanıt, D12: `docs/sadakat.md:53`: "534 aday eşleşti: tek aday kalmadığı için üretmedi. Kural YORUM kalır". §7 D12 sadakat kolu "mevcut kural" = yorum.
- Kanıt, D1: C girişi bakış ileri (bkz. Y2) ve `docs/TASARIM.md:73-75` (B-1): "Alış yönlü hali Tansu'nun gösterdiği kural olmaz." ISKPL tek hisse, tek yön; SMRTG kısa.
- Etki: "Tansu" etiketi hiçbir resmi adayda alınamıyor; kural fiilen "yorum kolu resmi sınava girer". Bu kötü değil (P5: her aile yorumumuz), ama belge ve §2'nin gerekçesi ("Tansu'nun gösterdiği hali") yanlış çerçeve kuruyor ve Açık soru 3'ü bile zayıflatıyor.
- Düzeltme: §2 ve §7'ye mevcut sadakat durumunu yaz (D11 kısmi, D12 üretmedi, D1 sınanmadı). Kuralı "resmi kol önceden yazılmış tek kol; sadakat yalnız etiketi belirler (Tansu / yorum)" diye yeniden kur. D1 için resmi kolun yönünü ve girişini sadakat öncesi kayda al (bkz. Y2).

**Y2. D1 `C_giris`: bakış ileri riski; geleceği görmeme testi yeni modülleri kapsamıyor.**
- Yer: §3.3 ("`C_giris` (C'de al, D'de çık; sadakat kolu)"); §3.2 ("pivot bilindiği an kuralı; bakış ileri yok"); §7 D1.
- Kanıt: R018 (T): "AB=CD 1000 günlük C noktasından alım yapılsa idi D satış karları" (koşullu, geriye dönük). ISKPL görseli (`assets/tweet-iskpl-…/01-iskpl-abcd-cden-dye-backtest.png`): sütun "Tarih (C)", sonuç "hedef". C bir salınım dibidir; ancak sonraki k mum geçtikten sonra bilinir. C tarihinden giriş, Tansu'nun tablosunu yeniden üretir ama işlem yapılabilir bir kural değildir. `tests/test_gelecek.py` (`docs/TASARIM.md:720-724`) bileşen listesi: evren, EMA, SMA, ATR, sıkışma, çift Z, likidite, faiz, K2. Pivot, Fib, bölge, FVG, durum makinesi listede yok; belge testi genişletmiyor.
- Etki: Sadakat (C tarihlerini tutturmak) ile işlem yapılabilirlik (C'yi tespit edebildiğin ilk gün + T+1 AOF) çelişiyor. Resmi kol C tarihinden girerse K1 etkiyi görür (rastgele giriş geleceği bilmez) ve p yapay küçülür; tespit gününden girerse Tansu'nun ISKPL tablosu yeniden üretilemez.
- Düzeltme: C_giris'i "C'nin doğrulandığı ilk gün + T+1 AOF" olarak tanımla; sadakat karşılaştırmasını tarihlerde değil "Tansu'nun C'si, bizim doğrulama gününde bulundu mu" biçiminde yaz. §8'e "test_gelecek.py pivot, Fib, bölge, durum makinesi ve haftalık mumu kapsar" maddesi ekle. Haftalık seriyi ayrıca ele al: hafta kapanmadan o haftanın pivotu bilinmez.

**Y3. TASARIM 3, 5.5 ve 5.8 sessizce değişiyor.**
- Kanıt: (a) `docs/TASARIM.md:71-72` "**Yok** (ilk aile kabul edilene kadar bekler): İz süren stop ve kısmi kâr"; §5.5 satır 328: "bir aile bu paketle kabul edildikten sonra denenir"; satır 324 "Hedef yok". Taslak 8 §4 bunları ilk dalgada kol yapıyor (parçalı pozisyon, hedef merdiveni, atr_zinciri). (b) `docs/TASARIM.md:73-75`: AB=CD "ikinci dalga"; satır 83-84: "Harmonik, Elliott ... kapsam dışı". Taslak 8 AB=CD'yi ilk dalgaya alıyor. (c) `docs/TASARIM.md:547`: kayıt "sadakat kontrolü bitince, **ilk getiri koşusundan** önce"; taslak 8 §5.3 (satır 91): "ilk **resmi** getiri koşusundan önce ... (5.8 kuralı aynen)". "Aynen" yanlış: "resmi" sözcüğü eklenmiş. Böylece §5.2'deki ölçüm koşuları (sermaye eğrisi, en büyük düşüş gösteren getiri koşuları) kayıttan önce yapılabiliyor.
- §1 "Değişmeyenler" listesi (satır 14-15) bunları anmıyor.
- Düzeltme: §1'e "Değişenler" paragrafı ekle: TASARIM 3 (kapsam, ikinci dalga, kapsam dışı), 5.5 (hedef, kısmi kâr), 5.8 (kayıt zamanı). Ya "ilk getiri koşusu" sözcüğünü geri koy ve ölçüm koşularını kayıttan sonraya al, ya da 5.8'in değiştiğini açıkça yaz ve gerekçesini ver. Ölçüm koşuları `kosu()` üzerinden (`resmi=False`) yapılacaksa bunu da yaz: `kayit.py:245-250` kayıt yoksa ya da hash uyuşmuyorsa her koşuyu durdurur.

**Y4. Çoklu test deliği kapanmıyor: ölçüm kolları seçim aracı olarak kullanılıyor, Holm yalnız +1 sayıyor.**
- Yer: §2 satır 28-29; §9 soru 1; §5.2.
- Kanıt: Kod (`kayit.py:87-96`, `99-120`) Holm'a her (kural_id, aile) çiftinin ilk resmi p'sini sokar. Ölçüm kolu "ayrı deneme olarak" resmi olursa m +1. Ama D1'de 4, D11'de 4, D19'da 2, D12'de 2 kol Levent'e sonuçlarıyla gösterilecek (§5.2, §6). Levent en iyi görüneni "resmi yapalım" derse: seçim yaklaşık 12 kol arasından yapıldı, düzeltme +1. 2015–2026'nın tümü geliştirme verisi (5.8) ve kolların hepsi aynı veride. K1 p'si seçilmiş kolun kendi verisi üzerinde hesaplanır (kazananın laneti).
- Etki: "Kolların sonuçlarına bakıp kural değiştirmek: Hayır" kuralı (§2) ölçüm sonuçlarını Levent'e göstermekle fiilen deliniyor; kod bunu engelleyemez, günlük de göremez (ölçüm koşuları `resmi=false`, m'ye girmez).
- Düzeltme: (i) Ölçüm kolundan resmiye terfide m'ye "bakılan kol sayısı" kadar eklenir (ör. ölçüm koşusunda kaç kol rapor edildiyse); günlükte `olcum_kol_sayisi` alanı. (ii) Ya da ölçüm kolları resmi p'ye hiç dönüşemez; yeni fikir yeni modül/yeni veri (kâğıt dönemi) ister. (iii) Açık soru 1'in cevabı "evet, +1" olmamalı.

### ORTA

**O1. K1 "ortak rastgele giriş, aynı yönetim" modüller için tanımsız.**
- Yer: §5 satır 94-95; Açık soru 2.
- Kanıt: `istatistik.py:26-101`: `EmaK1` ön şartlı gün havuzları (`aileler.on_sart`, `uygun_gunler`) ve `Zincir.kapali`; yönetim sabit (2 ATR + SMA250; `motor.py:51`, `66`). Modülde stop ve hedef kurulum geometrisinden gelir (A, B, C, D seviyeleri); rastgele günde bu seviyeler yok. "Yönetim aynı kalır" iki biçimde yorumlanır: aynı mutlak seviye (anlamsız) ya da aynı R-katı/mesafe (tanımsız). K1 ön şartı (`KURALLAR.md` §3 her aile için) modül için yazılmamış. `Zincir.tek(i)` önbelleği yalnız konuma bağlıdır (`motor.py:124-138`); kurulum geometrisi anahtara girmeli.
- Düzeltme: K1 tanımını kayıttan önce yaz: ön şartlı gün kümesi (ör. D1 için "C benzeri koşul sağlanan gün"), stopun/hedefin rastgele girişe aktarımı (ATR çarpanı ya da sinyaldeki yüzde mesafe), tür (b) komşu tanımı. Tanım yoksa modül resmi olamaz.

**O2. Parçalı pozisyon: boyut, risk, istatistik ve kabul hesapları tek satır/tek çıkış varsayıyor; belge etkiyi yazmıyor.**
- Kanıt: `simulator.py:88-93` `cik(d)` bir `k` için tüm adedi satar; `acik[k] = adet` tek değer; `simulator.py:99` risk sınırı `risk0[k]/adet0[k]` (giriş − stop); `_alinanlar` (`satır 117-127`) tek `cikis_fiyat`, `getiri`; `sepet_getirisi` (`satır 216-219`) giriş ve çıkış tarihi çifti; `istatistik.kabul`: `MIN_ISLEM=100` ve `MIN_GUN=60` satır sayar, ölçüt 4 "işlem başına fazla getiri sıralanıp ⌈0,05n⌉ atılır", tutma süresi blok uzunluğu (`kayit.py:185`). Parça başına satır n'yi şişirir (örneklem şartı kolaylaşır), ağırlıklı ortalama tutma süresi tanımsız. `motor.adim`: `stop = aof - STOP_ATR*atr` hep girişin altında; geçersizlik seviyesi T+1 AOF'un üstündeyse (boşluk) `risk0/adet0 ≤ 0` ve `simulator.py:99` sıfıra bölme ya da negatif adet verir. Belge "en çok 10 pozisyon" ve "%10 tavan"ın parça sonrası anlamını da yazmıyor.
- §1 "Değişmeyenler: kabul ölçütleri (5.12)": ölçütlerin girdisi (işlem tanımı) değişiyor.
- Düzeltme: "işlem = kurulum girişi (parçalar tek işlem, ağırlıklı çıkış fiyatı, ağırlıklı tutma)" kuralını yaz; risk adedi geçersizlik mesafesinden, `giriş ≤ stop` ise sinyal düşer (`iptal`); tavan ve en çok 10 sayacı pozisyon düzeyinde; TP1 sonrası "stop girişe" planlanan riski sıfırlar, `gerceklesen_kayip` ve rapor risk satırı bunu ayrı yazar.

**O3. `D_limit` kolu "dolum kuralları değişmez" sözüne aykırı.**
- Yer: §1 satır 14 ("dolum kuralları (T+1 AOF, tavan/taban kilidi...)"), §3.3 `D_limit`.
- Kanıt: veride açılış yok, yalnız AOF, yüksek, düşük (`docs/TASARIM.md:228-229`; `motor.mumlar` sütunları). `motor.adim` bekleyen pozisyonu yalnız ertesi gün AOF'tan doldurur (`satır 47-52`). Limit emri için temas kuralı (düşük ≤ limit), dolum fiyatı, bekleme süresi, emir sırası, tavan/taban kilidi belirsiz. `Zincir.kapali` "açık ya da bekleyen pozisyonun varken gelen sinyal düşer"; bekleme süresi uzarsa blok mantığı değişir. Haftalık mum (Gartley/AB=CD haftalık örnekler) günlük mum tablosunda yok.
- Düzeltme: `D_limit` için dolum modelini (temas = düşük ≤ limit, dolum = limit, kilitte dolmaz, N gün sonra iptal) 5.3'e ek olarak yaz, değişiklik olarak işaretle.

**O4. Kod yapısı ve kayıt maliyeti eksik anılıyor.**
- Kanıt: (a) `tests/test_kayit.py:166-171`: `KOD_DOSYALARI` kümesi test içinde sabit; yeni modül dosyası (pivot, fib, bölge, modül kartı) hem listeye hem teste eklenmeli; belge anmıyor. (b) `kayit.py:24` `AILELER = (ema, cift)`; `kayit.hesapla` iki ailenin K1'ini, ızgarasını ve kabulünü sabit kodlu çalıştırır (`satır 228-236`); `saglamlik.IZGARA` (`satır 19-20`) yalnız iki aile ve hash kapsamında. Ölçüm kolları `AILELER`'e eklenirse her `kosu(resmi=True)` onların p'sini üretir ve `_ilk_p` m'ye sokar (`satır 87-96`): "p yok" kuralı kodda zorlanmıyor. (c) m hesabı yok: kod her kural_id değişiminde her aile için yeni çift açar (`tekrar_sayisi`, `satır 129-136`). Günlükte şu an m = 2 (`kayit/deneme.jsonl` durum satırları `holm_m: 2`). Adım 7 sonrası D1 + D11 + D12 (+ eski EMA aile kalırsa) için m ≈ 5–6 olur; B = max(1000, 200·m). D12'nin "mevcut kural"ı yeni kural_id ile aynı hipotezi ikinci kez Holm'a sokar (m şişer, p aynı). §2 "maliyet düşük" bu hesapsız doğrulanamaz.
- Düzeltme: §8'e "KOD_DOSYALARI + test_kayit + IZGARA + AILELER genelleştirme" maddesi; ölçüm kolları için `AILELER` dışında ayrı yol (`tur=olcum`, K1 yok); m ve B hesabını yaz.

**O5. Örneklem, saptanabilir etki (MDE) ve kâğıt dönemi nadir kurulumlar için öngörülmemiş.**
- Kanıt: `istatistik.py:181`, `222-224`, `250`: ölçüt 5 ≥100 işlem ve ≥60 farklı gün; MDE/işlem > %1,0 ise "Ölçülemedi". Durum "Kâğıt" ancak ölçüt 1–5 Geçti ise (`satır 250`). AB=CD tarihleri: ISKPL 2,5 yılda 5 patern. `docs/TASARIM.md:562-566`: kâğıt dönem ≥6 ay ve ≥30 kapanmış işlem, 12 ayda dolmazsa "Ölçülemedi". D1 haftalık/seyrek kurulumda bu eşiklere ulaşıp ulaşmadığı belirsiz; belge sayım yapmıyor.
- Düzeltme: sadakat aşamasına getirisiz bir "sayım koşusu" ekle (modül başına evrende kurulum sayısı, farklı gün sayısı). Eşiği aşamayacak modül resmi sınava girmesin (m boşuna artmasın).

**O6. D12 rolling kointegrasyon: kendi çoklu test etkisi ve K1 uyumsuzluğu.**
- Kanıt: `ciftbolme.py:38-54`: yılda bir, aynı sektörde her çift için `coint`, `p < p_esik`, sonra en küçük p ile en çok 5 çift (`sec`, `satır 57-69`); gerçek veride yılda yaklaşık 1.000 çift (`satır 202`). Seçim zaten çoklu test düzeltmesiz: null altında bile en küçük p'li 5 çift sahte eşbütünleşmiş olur. `istatistik.CiftK1` seçilmiş çiftlerde yalnız Z zamanlamasını sınar (`TASARIM 5.7`: "çift seçiminin değeri K2 ile okunur"). Rolling kapı her gün/pencere yeniden test eder: test sayısı katlanır, pencere ve eşik serbestlik derecesi ekler (`IZGARA` p_esik 3 değer). Kapı yalnız gerçek koşuya uygulanır, K1 havuzu (`uygun`, `satır 146`) kapısız kalırsa K1 karşılaştırması eşleşmez.
- Düzeltme: ölçüm kolunda kapının pencere ve eşiğini önceden yaz; K1 havuzuna aynı kapıyı uygula; seçim sahteliğini ölçmek için boş dünya denetimine (`denetim.py`) rolling kapılı varyantı ekle.

**O7. Sadakat tanımı kayıyor; sadakat başarısızsa ne olacağı yazılı değil.**
- Kanıt: `docs/TASARIM.md:30-34` "Önce sadakat": Tansu'nun gösterdiği hali 5.12 ölçütlerinden birini geçemezse "tutmadı"; tutmazsa değiştirilmiş hali yeni deneme. `docs/TASARIM.md:547` ve `sadakat.py:1` ("Getiriye bakılmaz") sadakat = örnek yeniden üretimi. Taslak 8 ikinci tanımı alıyor (§5.1), birincisini (performans eşiği) anmıyor. Sadakat hedefi D1'de "ISKPL 5/5 hedef, SMRTG 12 kalıp (7 hedef 3 stop 2 açık)" sonuç etiketi içeriyor; sonuç etiketine uymak getiriye bakmaktır, `sadakat.py` ilkesine ters.
- D19: örnek grafik yok, bu yüzden hiç "Tansu" olamaz, resmi sınava girmez, ölçüm kolu. Kuralı en tam açık olan modül bu (R233, M) ve en temiz sınanabilir olan; ama ölçüm sonucunu görüp "resmi yapalım" dersek Y4 devreye girer. Belge D19'un yolunu açıkça yazmıyor.
- Düzeltme: sadakat ölçütü yalnız geometri/tarih eşleşmesi olsun (A-B-C-D seviyeleri ve doğrulama günü; hedef/stop sonucu değil). Sadakat tutmazsa ne olacağı (yorum etiketi, resmi aday yine aynı kol mu) ve D19'un resmi olma yolu (yeni deneme, Y4 düzeltmesiyle) tabloya yazılsın.

**O8. Sadakat aşamasında sınırsız ayar arama (kayıt dışı serbestlik derecesi).**
- Kanıt: Sadakat koşuları hash dışı, Holm dışı (`kayit.py:25` `HASH_DISI`; `sadakat.py`). Mevcut örnek: Z için 1.564 aday denendi (`docs/sadakat.md:51`), EMA için 3 geçmiş adayı (`sadakat.py:30`). Pivot ayarı, oran toleransı, doğrulama gecikmesi için "tek ayar mı ızgara mı" açık (§9 soru 5). Sonuç etiketine uymayı ölçüt alınca (O7) ayar, örnek getirilerine göre seçilir; sonra aynı veride resmi p.
- Düzeltme: sadakat ayar kümesi ve eşleşme ölçütü sadakat koşusundan önce kayda (tarihli) yazılsın; aday sayısı ve seçilen aday günlüğe yazılsın; seçim yalnız geometriye göre olsun (getiriye değil).

### DÜŞÜK

- **D-1.** §2 satır 24: "5.1 'tutmazsa değiştirilmiş hali yeni deneme'": bu cümle TASARIM §1'de (satır 38-39), 5.1'de değil.
- **D-2.** Yaşam döngüsü (§3.2) `C_giris` için durum vermiyor: C oluştu ama D yok; "ADAY" = "yapı bulundu" ve "AKTİF = fiyat bölgede/D oluştu". Kabul edilen taslağın "TEPKİ_VERDİ (teyit; giriş burada)" cümlesi `D_limit` ve `C_giris` kollarıyla eşlenmiyor.
- **D-3.** §8.1 "bit bit aynı" testi: depoda sonuç sabitleyen test yok (`tests/test_kayit.py:122-135` yalnız kendi içinde tutarlılık). Referans olarak `kayit/deneme.jsonl` `bitti.ozet` kullanılabilir ama aynı anlık görüntü gerekir; belge bunu yazsın. Kod hash'i bu değişiklikle değişecek; "bit bit aynı" yalnız sonuç özeti için.
- **D-4.** §2 satır 22 "p 0,73 / 0,94": bunlar ham K1 p'leri (`bitti.k1`: 0,7263 ve 0,9441). Holm p'leri `durum` satırlarında 1,0 ve m = 2. Doğru ama hangisi olduğu belirtilsin.
- **D-5.** `kayit.deneme_sayisi` docstring'i "Holm'un m'si: başlamış her deneme koşusu" der; fiili Holm birimi (kural_id, aile) çiftidir (`holm_hesapla`). Taslak 8'in "Holm m kalıcı artar" cümlesi çift birimine göre doğru; ama kod içi docstring ve `tekrar_sayisi` ile belge tutarsızlığı kalıyor (TASARIM 5.11 "Birim" cümlesine bak).

## Doğrulananlar

1. "Aile = sinyal günü üreten fonksiyon": `aileler.sinyal` (`aileler.py:50`) doğru.
2. "Stop motor.py'de sabit 2 ATR": `motor.py:13` `STOP_ATR = 2.0`, `satır 51`. Doğru. "Hedef ve kısmi çıkış yok": `adim` yalnız stop, SMA250 ve karantina çıkışı içerir. Doğru.
3. "Yeni aile = yeni kural_id ve Holm'da yeni çift": `kayit.py:41-47`, `99-120`. Doğru.
4. "Hash kapsamındaki dosyayı değiştirmek yeni kural_id verir; eski resmi koşu silinmez": `kayit.py:249-250` (hash uyuşmazlığı koşuyu durdurur). Doğru.
5. "Mevcut iki aile Deneme (p 0,73 / 0,94)": `kayit/deneme.jsonl` `bitti.k1`: `ema_sikismasi` 0,7263, `cift_rotasyonu` 0,9441; `durum` satırları "Deneme", m = 2.
6. "K1 bugün aileye özgü (ema_k1, cift_k1)": `istatistik.py:104`, `171`. Doğru.
7. "Boyut sınırları (risk, %10 tavan, %2 likidite, nakit, en çok 10)": `simulator.py:13`, `19`, `99-102`. "Risk payı geçersizlik mesafesi (taslak 7'de 2 ATR)": `satır 99` `risk0/adet0`. Doğru.
8. "2015–2026 tümü geliştirme verisi, ayrılmış dönem yok; dokunulmamış veri yalnız kâğıt üstü dönem": `docs/TASARIM.md:538`, `562-568` ile uyumlu. "AL denmez" (P1) ve "her aile yorumumuz" (P5) ile uyumlu.
9. §7 tablo, `docs/strateji-modulleri-taslak.md` ilk dalga tablosuyla tutarlı: D1 (C girişi → D çıkışı, kapı T R019, ölçüm kolları D_limit, tepki teyidi, atr_zinciri); D11 (KRDMD çapa, EMA 5-8-13 varyant, breakout/retest M R198, eğim kolu İ13); D19 (grafik yok, yalnız ölçüm); D12 (rolling kointegrasyon T R034/R228 varsayım). Kaynak etiketleri (T R014, R019, R043, R090, R224, R239; M R203, R198) kabul edilen sürümle uyumlu.
10. Çıkış kolları tanımı (`atr_zinciri`: 1,5 ATR aktivasyon, önceki gün dibi altı kapanışta %50, 2 ATR acil; `tp1_yari` M R203; `sma250` yorum): kabul edilen taslakla ve hamla uyumlu.

## Hüküm

TASARIM'a girmeden önce yazara dönmeli: Y1–Y4 (sadakat önkoşulunun üç adayda sağlanmaması, C girişinde bakış ileri, TASARIM 3/5.5/5.8'in sessiz değişimi, ölçüm kollarından terfide çoklu test deliği) giderilmeden "resmi sınava yalnız sadakat kolu" kuralı aşırı uyum riskini kapatmıyor; O1–O8 uygulama biletlerinden önce belgeye yazılmalı. (Tur 0 hükmü; güncel hüküm Tur 2 sonunda.)

## Tur 2 (tasarim-8.md sürüm 2)

Okuma anı: 06.10.2026 ~14:10. Belge 198 satır. Yöntem: Tur 0 bulgularının her biri yeni metinde arandı; yeni iddialar koda (`kayit.py`, `denetim.py`, `istatistik.py`, `motor.py`), `docs/sadakat.md`, `kayit/deneme.jsonl` ve beyin notlarına karşı kontrol edildi.

### Tur 0 bulgularının durumu

- Giderildi: Y1 (5.1 bugünkü durum doğru: `docs/sadakat.md:13-19`, `53` ile uyumlu), Y2 (C_giris doğrulama gününün ertesi AOF; 3.2 bakış ileri kuralı; 8.2 test), Y3 (§1 "Değişenler"; 5.8 aynen), Y4 (5.3.4), O1 (5.4), O2 (4.1, 4.2), O3 (4.3; ama bkz. T2-3), O4 (5.3.5, 8.5; ama bkz. T2-2), O5 (5.2), O6 (5.4 son madde), O7 (5.1), O8 (5.1; ama bkz. T2-6), D-1 ... D-4.
- D-5: yazarın belgeye taşımama kararına katılıyorum. `deneme_sayisi` üretimde kullanılmıyor (yalnız testlerde), belge Holm birimini (kural, aile) doğru yazıyor; docstring bilet konusudur.
- m hesabı (5.3.5): sayısal olarak doğru. `kayit.tekrar_sayisi` (`kayit.py:129-136`): m = günlükteki ilk resmi p'ler (2) + AILELER'deki yeni çiftler (3) = 5; B = max(1000, 200·5) = 1000. Koşul: AILELER tam olarak {D1, D11 (= `ema_sikismasi` adı), D12}. Eski EMA adı D11'den ayrı kalırsa m = 6 ve B = 1.200. Belge AILELER'in içeriğini yazmalı (T2-7).

### Bulgular

**YÜKSEK**

**T2-1. Boru hattı denetimi yeni aileler için zorunlu değil; bu, yeni K1 ve bakış ileri için tek ampirik koruma.**
- Kanıt: `kayit.py:254`: `if resmi and not denetim_gecti(kural["kod_hash"]) and not _resmi_bitti()`. İlk resmi koşu tamamlandı (`deneme.jsonl` `bitti`), yani `_resmi_bitti()` doğru; bundan sonra hiçbir resmi koşu için denetim aranmaz (`docs/TASARIM.md:698-700`: "Tamamlanan ilk resmi koşudan sonra denetim aranmaz"). `denetim.py:75-80` etki enjeksiyonu yalnız iki aileye sabit (`aile == simulator.AILE` değilse çift). Yeni modüllerin K1'i (5.4: yüzde mesafe aktarımı, pivot havuzu), C_giris tespiti ve yaşam döngüsü hiç boş dünyada sınanmadan resmi p üretecek. Boş dünya (bağımsız getiri) bakış ileri sızıntısını doğrudan yakalar: sızıntı varsa yanlış kabul oranı %5'i aşar. `test_gelecek.py` (8.2) birim düzeyi, boş dünya uçtan uca düzeydir.
- Düzeltme: §8'e "denetim yeni kod hash'iyle D1'i de kapsayarak yeniden koşulur; yanlış kabul ≤ %5 olmadan kayıt/resmi koşu yok" ekle ve TASARIM 5.12 kuralını (denetim yalnız ilk resmi koşudan önce) "yeni aile içeren her kural_id için" diye değiştir; bu bir "Değişen" olarak §1'e yazılsın. `denetim.etki_ekle` D1 için tanımlansın (etki: C_giris giriş günü AOF'una).

**ORTA**

**T2-2. §1 ve §4.1 çelişiyor: resmi kolda "hedef yok" aynen kalmıyor.**
- Kanıt: §1 satır 24: "'Hedef yok' ... resmi kolda aynen kalır; hedef ... yalnız ölçüm kolu". §3.3 satır 76: C_giris "çıkış D (hedef) ya da geçersizlik"; §4.1: "D1'de D seviyesi"; §7 satır 170 aynı. D, bir hedeftir (R018 "D satış karları"). Ayrıca 2 ATR acil stop ve SMA250 gün sonu çıkışının (TASARIM 5.5) resmi D1 kolunda geçerli olup olmadığı yazılı değil; geçersizlik stopu (A) onun yerini alıyor gibi.
- Düzeltme: §1'i düzelt: "resmi D1 kolu D hedefine ve geçersizlik stopuna sahiptir (5.5'ten sapma)". Resmi D1 kolu için 2 ATR stop ve SMA250 çıkışının geçerli olup olmadığını kayıtla sabitle.

**T2-3. 4.3 dolum modeli iyimser.**
- Kanıt: "Temas: günün düşüğü ≤ limit. Dolum fiyatı: limit." (satır 102-103). (i) Düşük tam limite değip dönen gün dolmuş sayılıyor; gerçekte kuyruk önceliği yok, bu günler en az dolan ve en kârlı (D'den tepki alan) günlerdir: klasik limit emri geriye test yanlılığı (adverse selection tersi). (ii) 2%-likidite boyutunda tam adet limitte dolar varsayımı; temas hacmi bilinmiyor. (iii) Veride açılış yok: boşlukla limitin altında açılışta fiyat limitten iyi olabilir ya da stop da aşılmış olabilir; model bunu ayırt edemez. (iv) Aynı gün dolum ve stop sırası: `motor.adim` ilk gün düşük ≤ stop ise stopa çıkar; D ile stop (A) çok uzaksa sorun yok, yakınsa sıra belirsiz.
- Etki: yalnız ölçüm (p yok) ama Levent'in "bunu kâğıt dönemde deneyelim" kararını yönlendirir.
- Düzeltme: temasa tolerans koy ("düşük ≤ limit − 1 fiyat adımı", TASARIM 5.1 adım tablosu) ya da dolum olasılığı varsay; adet sınırını temas günü hacmine bağla; aynı gün dolum + stop durumunu "stop" say ve raporla; sonuç "üst sınır (iyimser)" etiketli yazılsın.

**T2-4. Resmi D1 kolunda "girişte hedef zaten aşılmış / stop altında" kuralı yok; ayar belirsiz.**
- Kanıt: C doğrulama gününün ertesi AOF'u, C'den k mum sonradır; fiyat çoğu kez C'nin üzerinde, bazen D'nin üstünde. Giriş ≥ D ya da giriş ≤ geçersizlik durumunda sinyalin düşeceği yalnız ölçümde (4.2 "iptal") var, resmi kolda (4.1) yok. `motor.adim` bugün stopu girişten ATR ile kurar (`motor.py:51`); modülden gelen stop için `giriş ≤ stop` ise `risk0/adet0 ≤ 0` (`simulator.py:99`). Ayrıca resmi kol bir pivot ayarına ve doğrulama gecikmesi k'ya bağlı; "Resmi kol değişmez" (5.1) ile "ayar adayları sadakatle seçilir" arasındaki ilişki yazılı değil: hiçbir aday tutmazsa ya da birden çok aday tutarsa resmi kolun ayarı ne? (`docs/sadakat.md:53`'teki "tek aday kalmadı" durumu bunun gerçek örneği.)
- Düzeltme: 4.2'deki iptal kuralını 4.1'e taşı (giriş ≥ D ya da ≤ stop → sinyal düşer, sayılır). Kayıt önceden "varsayılan ayar" ve "birden çok / hiç aday tutarsa" kuralı yazsın; etiket sadakat sonucundan, ayar varsayılandan gelsin.

**T2-5. D1 sadakat verisi ölçütü taşımıyor.**
- Kanıt: §7 satır 170: "ISKPL C tarihleri ve A–D seviyeleri doğrulama gününde bulunuyor mu". ISKPL görseli yalnız C tarihleri, sonuç ve getiri veriyor (`assets/tweet-iskpl-…/01-…png`; beyin notu `tweet-iskpl-abcd-cden-dye-backtest.md:91`: "C anındaki BC oranı, squeeze, B kırılımı ... feature'larını sağlamaz"). A–D seviyeleri yok; SMRTG'nin salınım görseli var ama o kısa yön ve yalnız yön kontrolü. Yani geometrik sadakat 5 C tarihine iner; tolerans (±kaç gün), "tutar" eşiği (5/5? 4/5?) yazılı değil. "Tansu" etiketi 5 tarihle ve belirsiz eşikle verilecek.
- Düzeltme: sadakat ölçütünü yaz: ISKPL için 5 C tarihinin kaçı ±k gün içinde tespit edilmeli; A–D seviyeleri için SMRTG görselindeki sayılar kullanılacaksa yön kontrolüne ek olarak seviye kontrolü adı koy.

**T2-6. Ölçüm→resmi sızıntısı kod düzeyinde engellenmiyor.**
- Kanıt: §2 satır 38 ve 5.3.4 kural koyuyor; ama `kosu(resmi=True)` hangi kolun resmi olacağını kısıtlamaz (`kayit.py:240-300`). Bir sonraki kural_id'de (taslak 9, kod değişikliği) en iyi ölçüm kolu yeni kayıtta "resmi kol" yazılırsa Holm yalnız yeni çifti sayar; p yine 2015–2026 verisinde. Kâğıt-dönem-yalnız-yeni-veri mekanizması da tanımsız: TASARIM'da kâğıt dönem yalnız ölçüt 6 olarak var (`docs/TASARIM.md:663`); 6 aylık pencerede K1 + Holm için B, m ve güç yok (5.8: saptanabilir en küçük etki yıllık ≈ %56).
- Düzeltme: koda koruma: kayıtta resmi kol kimliği `tur=olcum` günlüğünde daha önce görüldüyse kayıt reddedilir. "Kâğıt dönemde resmi sınav" için ayrı bir 5.8/5.12 maddesi yaz (B, m, ölçüt, güç) ya da bu yolu belgeden çıkar; "ölçüm kolu hiç resmi olmaz" daha dürüst.

**T2-7. m ve kayıt maliyeti: AILELER içeriği ve ölçüm kodunun hash durumu belirsiz.**
- Kanıt: bkz. m notu üstte. Ayrıca 8.4 ölçüm yolu (`tur=olcum`) motor/simulator dosyalarına yazılırsa hash kapsamındadır; ölçüm koduna kayıttan sonra yapılan her hata düzeltmesi kural_id'yi değiştirir ve bir sonraki resmi koşuda 3 yeni çift açar (m = 8). §2 "tek seferde" bunu garanti etmez. `denetim`/`rapor` gibi ölçüm kodu hash dışı bir dosyada (`olcum.py`, HASH_DISI) tutulursa kapsam testi (`tests/test_kayit.py:166-171`) bunu sınıflandırmayı zorlar; ama o dosya resmi p'yi etkileyen ortak yapı taşlarını (pivot, oran) çağırıyorsa hash içi kalmalı.
- Düzeltme: §8'e hangi dosyaların `KOD_DOSYALARI`/`HASH_DISI` olacağını yaz; ölçüm koşuları kayıt sonrası yalnız hash dışı dosyada değişir.

**T2-8. 5.4 K1 hipotezi ile TASARIM 5.7'nin K1'i farklı soruyu sınıyor; tanım eksik.**
- Kanıt: TASARIM 5.7 (`docs/TASARIM.md:450-452`): rastgele sinyaller "kuralın kendi ön şartlarını sağlayan günlerden". 5.4: havuz "oran kapısı R019 uygulanmadan" yalnız pivot dibi günleri. Bu K1, "AB=CD oran kapısı rastgele pivot dibinden iyi mi" sorusunu sınar; Tansu'nun iddiası (AB=CD kurulumu iyi) değil. Stop ve hedef yüzdesi gerçek sinyalden rastgele girişe aktarılınca K1'in sıfır hipotezi stop/hedef yapısını (risk/ödül asimetrisini) korur: bu yapının katkısı p'ye girmez (Ölçüt 2'de K2'ye karşı görünür). Bu bilinçli bir tercih olabilir ama belge bunu söylemiyor. Tür (a) (aynı gün, başka hisse), tür (b) (±20 gün komşu), "aile p'si = büyüğü" ve ek kol 5.4'te yok. `Zincir.tek(i)` önbelleği anahtara yüzde mesafeler girince hit oranı çöker (K1'in 78 → 16 sn hızlanması önbelleğe dayanır, TASARIM 5.7 "Süre").
- Düzeltme: 5.4'e K1'in hangi hipotezi sınadığını yaz (pivot dibi + oran kapısı vs rastgele pivot dibi; ya da oran kapısı dahil ön şart). Tür a/b'nin modül karşılığını ve p kuralını yaz. Çalışma süresi için önbellek anahtarı (konum, stop%, hedef%) ile B = 1.000 maliyetini tahmin et.

### DÜŞÜK

- **D-6.** §3.2 şeması AKTİF'ten TAMAMLANDI/BOZULDU'ya ok vermiyor (C_giris ve D_limit'te giren pozisyon bunlara gider); yalnız TEPKİ_VERDİ'den çıkıyor. "Tepki" (asgari hareket) tanımsız; `tepki_teyidi` ölçüm kolu da olsa tanım önceden yazılmalı (kol içi serbestlik).
- **D-7.** §1: "AB=CD ondan (Harmonik) ayrılır": AB=CD harmonik ailedir (R004 "Harmonik yapılar (ABCD, Kelebek, Gartley)"); doğru ifade "AB=CD kapsam dışı listesinden çıkarılır".
- **D-8.** §5.2 "getirisiz sayım" işlem sayısını sayarken simülatörü (boyut, likidite, en çok 10) çağırırsa getiri üretir; yalnız sinyal ve farklı gün sayısı raporlansın, getiri sütunları yazılmasın.
- **D-9.** §8.3 "D11 sadakat yeniden (önceden yazılmış ayar kümesiyle)": D11 sonuçları (`docs/sadakat.md`) zaten görüldü; "önceden" yalnız etiket için geçerli. D11 resmi kolu değişmediği için sızıntı yok; cümle bunu söylesin.
- **D-10.** 5.3.4 ve ölçüm koşusu kosu() dışı ayrı yol olacaksa TASARIM 4 "getiri gösteren tek yol kosu()'dur" cümlesi §1 "Değişenler"e yazılmalı (ölçüm yolu kayıt/hash denetimini aynı biçimde yapmalı).

### Doğrulananlar (Tur 2)

1. Tur 0 Y1–Y4 ve O1–O8'in belgede karşılığı var ve içeriği doğru yönde (yukarıdaki durum listesi).
2. 5.1 "Bugünkü durum": D11 kısmi ve D12 üretmedi ifadeleri `docs/sadakat.md:13-19`, `31`, `43`, `53` ile birebir uyumlu.
3. §2 satır 40: ham K1 p'leri 0,7263 (EMA) ve 0,9441 (çift); Holm p'leri 1,0; m = 2: `kayit/deneme.jsonl` ile uyumlu.
4. m = 5 ve B = 1.000 hesabı `kayit.tekrar_sayisi` mantığıyla tutarlı (AILELER üç çift ise).
5. §1 "Değişenler": TASARIM 3 (B-1, `docs/TASARIM.md:73-75`), kapsam dışı (satır 83-84), 5.5 (satır 324, 328), 5.8 (satır 547) atıfları doğru.
6. 5.8 "ilk getiri koşusundan önce" ifadesi artık aynen; ölçüm koşuları kayıttan sonra: tutarlı.
7. §7 tablo ve kaynak etiketleri `docs/strateji-modulleri-taslak.md` ilk dalga tablosuyla tutarlı (D1 resmi kol C girişi; D11 KRDMD çapası; D19 yalnız ölçüm; D12 rolling kapı ölçüm kolu varsayım).
8. Ölçüm yolunun `AILELER` dışında olması "p yok" kuralını kodda zorlamanın doğru yönü (`kayit.py:24`, `87-96`).
9. C_giris'in doğrulama gününün ertesi AOF'una taşınması Y2'yi giderir; 3.2 "pivot sağındaki k mum" ve haftalık mum notu doğru.

## Hüküm (Tur 2)

Yazara kısa bir tur daha dönmeli: sürüm 2 Y1–Y4'ü büyük ölçüde kapattı, ama yeni YÜKSEK bulgu (T2-1: yeni aileler için boru hattı denetimi zorunlu değil, bakış ileri ve yeni K1 için tek ampirik koruma) ile iç çelişki (T2-2: resmi D1 kolu hedefli, §1 "hedef yok aynen" diyor) ve ORTA T2-3 ... T2-8 (iyimser limit dolumu, resmi kolda iptal kuralı ve ayar belirsizliği, ISKPL sadakat verisi 5 tarih, kod düzeyinde sızıntı koruması, AILELER ve hash içeriği, K1 hipotezi) giderilmeden TASARIM'a girmemeli; hepsi belge düzeyinde, kod gerektirmeyen düzeltmelerdir. (Tur 2 hükmü; güncel hüküm Tur 3 sonunda.)

## Tur 3 (tasarim-8.md sürüm 3)

Okuma anı: 06.10.2026 ~14:30. Belge 236 satır. Yöntem: Tur 2 bulgularının her biri yeni metinde arandı; yeni iddialar `kayit.py`, `denetim.py`, `istatistik.py` ve `docs/TASARIM.md` ile karşılaştırıldı.

### Tur 2 bulgularının durumu

Giderildi: T2-1 (§1 denetim maddesi, §8.7; ama bkz. T3-3), T2-2 (§1 5.5 maddesi doğru: resmi D1 hedefli, 2 ATR ve SMA250 yok, D11/D12 5.5 aynen), T2-3 (4.3 muhafazakâr: temas = düşük ≤ limit − 1 adım, adet ≤ temas günü hacminin %2'si, aynı gün dolum+stop = stop, "üst sınır" etiketi), T2-4 (4.1 iptal kuralı ve varsayılan ayar), T2-5 (5.1 D1 ölçütü; ama bkz. T3-2), T2-6 (kâğıt dönemde resmi yol kaldırıldı: doğru karar; kod koruması için bkz. T3-1), T2-7 (5.3.5 AILELER ve m; 5.3.6 hash ayrımı; bkz. T3-4), T2-8 (5.4 hipotez açık, tür a/b, önbellek), D-6 ... D-10.
m kontrolü: AILELER = {D1, D11 (`ema_sikismasi`), D12 (`cift_rotasyonu`)} → m = 2 + 3 = 5, B = max(1000, 1000) = 1000; ayrı kalırsa 6 ve 1.200. `kayit.tekrar_sayisi` mantığıyla doğru.

### Bulgular

Yeni YÜKSEK bulgu yok.

**ORTA**

**T3-1. T2-6 kod koruması kapsamı yetersiz ve §8.4 ile çelişiyor.**
- Kanıt, çelişki: §8.4 "Taslak 7 davranışı bir kol olarak korunur" ölçüm yolunda (`tur=olcum`). Taslak 7'nin EMA ailesi D11'in resmi kolu (§7, satır 210). Koruma "resmi kol kimliği daha önce `tur=olcum` günlüğünde görülmüşse kaydı reddeder" der; D11 resmi kolu ölçümde baz kol olarak görülünce, sonraki kayıtta (D11 değişmeden kalsa bile) reddedilir. Aynı durum §6 "resmi kol sonucu ile ölçüm kolları yan yana" için de geçerli: resmi kol ölçüm raporunda referans olarak yer alırsa günlüğe düşer.
- Kanıt, kapsam: koruma kol *adına* bağlıysa yeniden adlandırma (`C_giris_v2`), küçük ayar değişikliği ya da bileşik kol (resmi kol + ATR zinciri) onu geçer. Mantıksal esin ("ölçümde şu kol iyi çıktı, yeni kodla onu resmi yapayım") kodla yakalanamaz.
- Düzeltme: kimlik, kolun içerik özeti olsun (modül + giriş kuralı + çıkış kuralı + ayar parametreleri, sha256). Ölçüm günlüğü resmi kolu `referans=true` etiketiyle yazsın; koruma yalnız `olcum_kolu=true` kimliklerini saysın. Belge sınırı açık yazsın: kod yalnız aynı içeriği engeller, esinlenmiş yeniden tasarımı engelleyemez; bu disiplin ve kayıt tarihine bağlıdır.

**T3-2. 5.1 D1 "tutar" ölçütü şansla geçilebilir ve "doğrulama gününde ±3 gün" belirsiz.**
- Kanıt: ISKPL görseli 5 C tarihi verir. Bir salınım dibi dedektörü 1.000+ günde yaklaşık 15 günde bir dip üretir; ±3 işlem günü penceresi (7 gün) ile bir tarihe şans eşleşmesi ≈ %40; 5 tarihin ≥4'ü tek aday için ≈ %9, 3 aday için ≈ %25 (bu rakamlar kaba tahmin, dedektör sıklığına bağlı). "Dedektörümüzce bulunur" yalnız salınım dibi anlamına gelirse "Tansu" etiketi şansla alınır. Ayrıca doğrulama günü C'den k mum sonradır; "doğrulama gününde ±3 gün" hangi tarihe göre (Tansu'nun C'sine mi, bizim C'mize mi) yazılı değil; k > 3 ise Tansu'nun C tarihi ile doğrulama günü ±3'e sığmaz.
- Düzeltme: ölçütü "dedektörün bulduğu C pivotu Tansu'nun C tarihine ±3 işlem günü içinde ve doğrulama günü ≥ C" diye yaz. Eşleşme için oran kapısını (T R019) sağlayan bir AB=CD kurulumu şart olsun (yalnız dip değil). Plasebo ekle: ISKPL'de rastgele 5 tarihle aynı testin eşleşme oranı raporlansın (şans tabanı). Ayrıca SMRTG'nin 12 C tarihi ayna dedektörle (kısa yön) tarih kontrolüne eklenirse örnek 5'ten 17'ye çıkar.

**T3-3. §1 denetim kuralı "yeni aile içeren kural_id" fazla dar.**
- Kanıt: `kayit.py:254` koşulundaki `not _resmi_bitti()` kalkarsa kural basit: her yeni kod hash'i için `denetim_gecti(kod_hash)` aranır. "Yeni aile içeren" ifadesi, aile eklemeyen ama simülatör, motor ya da istatistiği değiştiren bir kural_id'yi (hata düzeltmesi, m üzerinde etkili yeni kayıt) denetimsiz geçirir; oysa p'yi bu dosyalar etkiler. §5.3.6 "hash içi dosya değişirse yeni kayıt ve yeni çiftler" ile aynı mantıkta olmalı.
- Düzeltme: §1 ve §8.7: "her yeni kod hash'i için, resmi koşudan önce denetim geçmiş olmalı" (`_resmi_bitti` istisnası kalkar). Maliyet (200 tekrar) kabul edilebilir.

**T3-4. 5.3.6 hash içi/dışı ayrımı resmi p'yi doğrudan sızdırmıyor; bağımlılık yönü ve izlenebilirlik yazılı değil.**
- Cevap (sorunuz): `olcum.py` yalnız ölçüm kodunu (parçalı pozisyon, çıkış kolları, D_limit, ölçüm raporu) taşıyorsa ve resmi yol onu çağırmıyorsa, resmi p'ye etki edemez; ayrım doğru. Ama iki şey yazılı olmalı: (a) bağımlılık yönü: hash içi dosyalar `olcum.py`'yi import etmez. Bugünkü kodda `kayit.py` (hash içi) `rapor.py`'yi (hash dışı) import ediyor (`kayit.py:16`); rapor yalnız sunum olduğu için kabul edilebilir, ama aynı örüntü `olcum.py` için kullanılırsa (ör. `kayit.hesapla` ölçümü çağırırsa) resmi sonuç kural_id değişmeden değişebilir. (b) `tur=olcum` satırları `olcum.py` sha256'sını ve `git_commit`'i taşımalı; aksi halde ölçüm sonuçları sabitlenmemiş kodla üretilir.
- Düzeltme: §5.3.6'ya "hash içi kod `olcum`'u import etmez; test sınar (AST ile import taraması)" ve "ölçüm günlüğü `olcum_hash`, `git_commit` yazar" ekle.

**T3-5. "5.8 aynen" ile geliştirme sırasındaki D1 getiri koşuları çelişir.**
- Kanıt: §1: "kayıt ilk getiri koşusundan önce"; §8.4 geriye uyum testi aynı anlık görüntüde getiri özeti koşar; §8.1-§8.6 D1 dedektörü, boyutlama, K1 yazılırken D1'in gerçek veride getirisi görülür (kosu hash/kayıt koşulu `kayit.py:245-250` ara kayıtlarla da aşılır). Bugünkü uygulama zaten böyle (ilk resmi koşudan önce `resmi:false` geliştirme koşuları serbest, TASARIM 5.11), ama §1 "aynen" diyor; D1 için tehlike gerçek: C_giris'in ayarı getiri görülerek seçilebilir.
- Düzeltme: açık kural yaz: "D1'in gerçek veride getirisi, kayıt öncesi hiçbir koşuda yazılmaz ya da görülmez; geliştirme sentetik/boş dünya ve sayım koşularıyla yapılır (denetim adımı bu amaca da hizmet eder)". Geriye uyum testi (8.4) yalnız eski EMA özetini karşılaştırır; bu getiri koşusu D1'i içermez, belge bunu söylesin.

### DÜŞÜK

- **D-11.** §7 tablosu eski kalmış: D1 sadakat sütunu "ISKPL C tarihleri ve A–D seviyeleri" (5.1: A–D seviyeleri yok); D19 satırı "resmi olma yolu yalnız kâğıt üstü dönemde yeni deneme" (5.3.4: hiç resmi olmaz). İkisi §9.1 ve 5.1 ile çelişir.
- **D-12.** §1 "Değişmeyenler": "'işlem' tanımı 4.2'de": resmi kol için geçerli tanım 4.1 (tek giriş, tek çıkış); 4.2 yalnız ölçüm.
- **D-13.** 5.4 ön şartlı havuz filtreleri (evren üyesi, karantina penceresi dışı, ısınma, SMA250 var mı) yazılı değil; EMA K1 bunları içerir (`istatistik.py:44-49`).
- **D-14.** 5.2: sayım yalnız sinyal sayısının üst sınırıdır (boyut, likidite, en çok 10 sonrası işlem daha azdır); "eşiğe ulaşmayacağı görülen" mantığı doğru yönde (üst sınır altındaysa kesin yetmez), ama eşiği geçen modülün yeterli olacağı anlamına gelmez: belge bunu söylesin.
- **D-15.** 4.3: hacim sınırı "temas günü hacminin %2'si" günün tüm hacmini kullanır (dolum günün başında olabilir); muhafazakâr yönde kabul edilebilir, "üst sınır" etiketi zaten var.

### Doğrulananlar (Tur 3)

1. §1 Değişenler: TASARIM 3 (B-1), kapsam dışı, 5.5, 5.12 (`kayit.py:254`, TASARIM 698-700), 4, 5.8 atıfları kodla ve TASARIM'la uyumlu.
2. §1 5.5 maddesi iç çelişkiyi giderir (resmi D1 hedefli; D11/D12 5.5 aynen).
3. m = 5 ve B = 1.000: `kayit.tekrar_sayisi` ile tutarlı; "her hash içi değişiklik m +3" tutarlı.
4. 4.3 dolum modeli artık muhafazakâr ve etiketli; aynı gün dolum+stop = stop doğru yönde.
5. 4.1 iptal kuralı ve varsayılan ayar, T2-4'ü kapatır; sadakat yalnız etiket.
6. 3.2 şema AKTİF'ten TAMAMLANDI/BOZULDU'ya ok verir; tepki tanımı (D'den ≥ 1 ATR yukarı kapanış) yorum olarak işaretli.
7. 5.4 K1 hipotezi (oran kapısı vs rastgele salınım dibi; risk/ödül yapısı K1 dışı, ölçüt 2'de) açık ve TASARIM 5.7 ile tutarlı; tür (b) ±20 gün TASARIM 5.7 ile uyumlu.
8. §8.7 denetim adımı kayıttan önce; `denetim.etki_ekle` D1 için; denetim boş dünyada gerçek getiri göstermediği için T3-5'e de uyar.
9. Kâğıt dönemde resmi yol kaldırma kararı doğru (6 ayda saptanabilir en küçük etki yıllık ≈ %56; tek kol için güç yok).

## Hüküm (Tur 3)

Koşullu kabul: yeni YÜKSEK bulgu yok ve T2'nin bütün ana bulguları kapanmış; kalan beş ORTA (T3-1 kod koruması kimliği, T3-2 sadakat ölçütü ve şans tabanı, T3-3 denetim koşulu, T3-4 import yönü ve ölçüm günlüğü, T3-5 D1 getiri koşusu kuralı) ve DÜŞÜK satırlar mekanik belge düzeltmeleridir; yazar bunları uyguladıktan sonra yeniden denetime gerek olmadan TASARIM'a önerilebilir.
