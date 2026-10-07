# Hakem talimatı (kod kitabı sürüm 5'e ek)

Kod kitabı tam koşu sırasında sabittir (Codex hâlâ onunla okur). Aşağıdaki kurallar, kitabın tanımlamadığı ve iki
okuyucunun farklı doldurduğu `kod` boşluklarını kapatır. Kaynak: `kod` var/yok ayrışan gönderiler (07.10: 4.155
ortakta 45, 4.755 ortakta 52) ve denetim-x.md "Tur: hakem talimatı ve ön karşılaştırma" (Y-1, O-1…O-4, D-1…D-4).
Codex bitince bu talimat son ayrışma listesiyle yeniden sınanır (O-4).

## K1. `kod` yalnız Tansu'nun kendi gönderisine bakar
- Kod üst gönderide ya da alıntıdaysa yanıtın `kod` değeri `yok`.
- Üst gönderi Tansu'nun ve sınıflama kaydı varsa: o kayıt kodu taşır. Yanıt üst kodu düzeltiyor ya da
  değiştiriyorsa notta "üst kodu düzeltiyor: <ne>" yazılır (ör. 1842658091239694553: üst kod RSI <= 30'da al veriyor,
  yanıt "RSI > 30").
- Üst gönderi Tansu'nun ve kaydı YOKSA (arşiv dışı; Y-1): gönderi ek koşu listesine (`siniflama/hakem/ek-kosu.txt`)
  yazılır. Ek koşu: metin ve medya çekilir, iki okuyucu sınıflar. Alınamayan üst gönderi listede "alınamadı" kalır.
- Üst gönderi ya da alıntı başka kullanıcınınsa: hakem kodu `siniflama/hakem/ust-kod.jsonl` dosyasına yazar:
  `{"id": <Tansu gönderisi>, "kaynak": "@kullanıcı", "kod_metni": <birebir ya da null>, "baglanti": <url ya da null>,
  "tansu": "onayladı|uyguladı|övdü|çevirecek|istedi|diğer"}`.
  Bu, Ayırma kuralı 6 ile tutarlıdır (başkasının kuralı Tansu'nun kuralı sayılmaz). `baglanti` dolu kayıtlar bağlantı
  deneme aşamasına gider.

## K2. Bağlantı: alan adına göre (bütün kayıtlara, yalnız ayrışanlara değil)
- Tansu'nun kendi metnindeki dosya ya da kod barındırma bağlantısı → `baglanti`: we.tl, wetransfer.com,
  drive.google.com, github.com, colab.research.google.com, tradingview.com/script, dropbox.com.
- Başka bağlantı (LinkedIn, haber, kişisel sayfa) → `yok`; metin "Python çalışmalarım orada" dese de
  (ör. 1770856035709817030).
- Gönderide hem görselde kod hem bağlantı varsa `kod: gorselde`; bağlantı `not`a yazılır ve deneme aşamasına gider.
- Birleştirmede bu kural iki okuyucunun uyuştuğu kayıtlara da makineyle uygulanır.

## K3. Kod sayılmayanlar
- Okunamayan ya da paylaşım konusu olmayan arka plan kodu (kitap fotoğrafının arkasındaki ekran, program çıktısının
  kenarındaki silik satırlar) → `yok`; notta "arka plan kodu, okunamıyor". Ör. 1891183558858883162,
  1893725545260544026, 1892643772430766103, 1842520794586341379.
- Metinde yalnız fonksiyon adı ya da parametre (`read_csv()`, `print()`, "range = 30", "qf.iplot kodu çalıştır") →
  `yok`; adlar `parametreler`e.
- Matematik formülü ("C = BS(S, K, r, T, σ)", "W1*1.618", Excel hücresindeki amaç fonksiyonu) → kod değil;
  formül `parametreler`e birebir. Kod yalnız çalıştırılabilir dil: Python, Pine, Matriks/MetaStock formül dili
  (`Cross(Mov(RSI(C,14),5,VAR),50)`), Excel formülü hücre başvurusuyla (`=B2*C2`).

## K4. Video
- Okunmayan video gönderisinde `kod: yok` bir tahmindir. Birleştirmede bu kayıtlara `video_okunmadi: true` eklenir;
  video sayımı ve kare çıkarma kararı Levent'e sorulur.

## K5. Pilot kümelerden çıkan sınırlar (07.10, küme 002)
- Metinsiz görsel (illüstrasyon, caps): görsel piyasa yönü ya da değerlendirmesi söylüyorsa `görüş`, söylemiyorsa
  `sohbet-duyuru`.
- Piyasa dışı kod (pazarlama ısı haritası, ERP): `kod` kitaba göre yazılır; `kural: yok` (işlem/hesap kuralı değil).
- İçeriği olmayan analiz duyurusu ("DOAS değerlemesi yolda", "KCAER analizini yapacağım") Ayırma kuralı 4'e girmez
  (araç/tarama/bot/proje değil) → `sohbet-duyuru`, `kural: yok`.
- "Ne demiştik" + Tansu'nun kendi eski gönderisinden alıntı: yöntem yalnız alıntıdaysa bu gönderiye `cekirdek`/`rol2`
  verilmez (yöntem alıntılanan kaydın kendisinde) → `sinyal-sonucu`, `kural: yok`.
- Sonuç grafiği, etkin sınır, getiri eğrisi gibi çıktı formülsüzse veri tablosudur → `kural: yok`.
- Makro veri anlatımı: davranış kuralı yoksa `görüş`; "şu olunca şunu yap" varsa `rejim`.
- `rol2` yalnız `rol` ya da `kural` ayrışmasıyla birlikte karar alanıdır.

## K6. Pilot kümelerden çıkan sınırlar (07.10, küme 001)
- Değerleme çalışması duyurusu: gönderide değerleme içeriği (çarpan, hedef, tablo) varsa `değerleme-temel`, kural
  içeriğe göre; içerik yoksa K5 (`sohbet-duyuru`).
- Tansu kendi kodunu "yazdım / paylaşıyorum / kullanın" diye veriyorsa `ürün-hedefi`; bir kütüphaneyi ya da dili
  öğretiyorsa `araç-öğrenme`.
- Takas, aracı kurum dağılımı ya da derinlik ekranı + yön yorumu, eşik yoksa → `görüş`.
- ADX, trend gücü, gösterge uyumsuzluğu tek hisse için → `teyit`; endeks ya da bütün piyasa için davranış kuralıyla →
  `rejim`. Göstergenin hesabını anlatıyorsa → `ölçüm-yöntemi`.
- Belirsiz fiyat düzeyi ("üç haneliler", "yeni zirveler") hedef sayılmaz → `görüş`.
- Üst gönderinin genel gözlemine yumuşak katılım ("realite var", "aynen") Ayırma kuralı 6'daki onay değildir.
- Piyasa dışı kod (PCA, kümeleme, ERP): K5'e göre `kural: yok`. Küme 001'deki bu kayıtlar birleştirmede K5'e göre
  düzeltilir.

## K7. Küme 003'ten çıkan sınırlar (07.10)
- K1 `tansu` alanına `açıkladı` eklenir: Tansu başkasının kodunu düz dile çeviriyor ("meal") → rol `araç-öğrenme`,
  `kural: yok`.
- "Deneyeceğim, elinize sağlık" benimseme değildir (Ayırma kuralı 6) → `sohbet-duyuru`; ust-kod `övdü`.
- Adı verilip tanımı verilmeyen strateji ya da model ("stokastik RSI stratejim", "default probability modeli") →
  `kural: fikir` (kitaptaki fikir tanımı); duyuruysa rol `ürün-hedefi`, içeriğin rolü `rol2`.
- Program çıktısında formül yok ama strateji adı ve parametre değerleri (OPT, periyot, eşik) yazılı → `cekirdek`.
  K5'teki "formülsüz çıktı → yok" yalnız parametresi de olmayan sonuç tablosu içindir.
- Yöntem adı yazılı oran tablosu ("Dupont analizi", "Altman Z") formülsüz → `cekirdek`; formül görünüyorsa `tam`.

## K8. Küme 007'den çıkan sınırlar (07.10)
- Araç adı olmadan "kodlayacağım / kodluyorum" → Ayırma kuralı 4 (`ürün-hedefi`); yalnız "hepsini yaparız" → `sohbet-duyuru`.
- Duyuru ile ölçüt aynı gönderide: Ayırma kuralı 4 geçerli (rol `ürün-hedefi`, ölçütün rolü `rol2`, `kural` ölçüte göre).
- K6'daki tek hisse kuralı bütün gösterge koşullarına uygulanır (RoC, MACD, stokastik kesişimi) → `teyit`.
- Yalnız `rol2` ayrışıyorsa hakem kararı gerekmez; A'nın değeri kalır.
- Yanıt kendi üst gönderisinin eşiğini düzeltiyorsa `kural` yalnız bu gönderiye göre; notta "üst eşiği düzeltiyor: <ne>".
  Defter aşamasında iki kayıt birlikte okunur.

## K9. Küme 004'ten çıkan sınırlar (07.10)
- Aynı gösterge koşulu (BB orta bant, RSI 50 kesişimi): tarama ölçütüyse `seçim-momentum`, giriş anını veriyorsa
  `giriş`, başka bir kurala eklenen koşulsa `teyit`.
- Formülde yalnız OPT aralığı var, seçilen değer yok → `cekirdek` (eşik yazılı değil). Seçilen değer yazılıysa `tam`.
- Ölçüsüz ilke ("farklı indikatörlere bakın") → rol `ilke`, `kural: yok`.
- Dizideki (zincir) gönderi kendi içeriğine göre sınıflanır; dizi yalnız anlamı çözmek için okunur.
- Görseldeki kodda belirsiz işaret ("> <") birebir bırakılır; olası anlam notta yazılır.

## K10. Küme 006'dan çıkan sınırlar (07.10)
- Kod hem metinde hem görselde: kodun tamamı neredeyse o değer (`gorselde` ya da `metinde`); öteki notta.
- Kütüphaneyle hazır gösterge çizimi (cufflinks SMA/EMA, MACD), işlem kuralı yok → `araç-öğrenme`, `kural: yok`.
- Tarama SONUCU paylaşımı ("taramasını yaptık" + liste/ölçüt) → içeriğin rolü (ör. `seçim-momentum`); `ürün-hedefi`
  yalnız aracı ya da taramayı duyuruyorsa ("yazdım, paylaşacağım, hazırlayacağım"). K8'deki "duyuru + ölçüt" kuralı
  yalnız duyuru içindir.

## K11. Küme 005'ten çıkan sınırlar (07.10)
- Kod bir hesabı (gösterge, Markowitz simülasyonu) eksiksiz yapıyor ama işlem kuralı vermiyor: kitapta `kural` işlem
  YA DA hesap kuralının tamlığıdır → kod çalıştırılabilir ve girdileri yazılıysa `tam`, rol `ölçüm-yöntemi` (ya da
  hesabın rolü). Küme 005'teki `cekirdek` kararları birleştirmede buna göre düzeltilir.
- Kitap sayfası: sayfa yalnız tanıtılıyorsa `araç-öğrenme` (Ayırma kuralı 5); sayfadaki yöntem anlatılıyorsa içeriğin
  rolü (Ayırma kuralı 8).
- Kodu teklif etme ("isteyene kodları veririm", "birazdan yolluyorum") → `ürün-hedefi`; kod verilmeyen hatırlatma
  ("hangi kodu verecektim?") → `sohbet-duyuru`.
- Aracı kurum takibini işlem kuralı olarak vermek ("infoya biner, indiği yerde inerdim") → `giriş` (ya da `çıkış`),
  `cekirdek`. K6'daki "takas + yön yorumu → görüş" yalnız davranış kuralı olmayan yorum içindir.

## K12. Küme 009'dan çıkan sınırlar (07.10)
- Sinyal sonucunda yöntemin yalnız adı geçiyorsa ("Bizim Vegas taramasından çıkan") → `kural: fikir`, yöntemin rolü
  `rol2`. Ayırma kuralı 9'daki `cekirdek` yalnız ölçü ya da yön de yazılıysa.
- Çok hisseli taramada AL anını tanımlayan gösterge koşulu (%R −70 kesişimi + MACD) → `giriş`; listeyi seçen ölçüt →
  `seçim-momentum`.
- Takipçiye yöntemsiz, sonuçsuz soru ("Kazanç sağlayan oldu mu?") → `sohbet-duyuru`.
- Kendi tarama listesini alıntılayıp yalnız hisse adı yazmak ("Angen :))))") → `sinyal-sonucu`, `kural: yok` (K5).

## K13. Küme 010'dan çıkan sınırlar (07.10)
- Kendi sinyaline sayısız kutlama ("Doco 🥂") → `sinyal-sonucu`, `kural: yok` (K12 son madde).
- Çok hisseli göstergeli tarama, AL anı tanımsız → `seçim-momentum`, gösterge koşulu `rol2: teyit` (K12 ile birlikte).
- Eşikleri yazılı tarama + tanımsız ek koşul ("para girişi") → `cekirdek`.
- Yalnız formasyon adı veren çıktı (TA-Lib CDL adları) → `cekirdek` (adlar kütüphanede tanımlı; eşik yok).
- Grafik etiket ya da çizim kodu, işlem/hesap kuralı yok → `kural: yok` (K10).

## K14. Küme 011'den çıkan sınırlar (07.10)
- Bir gönderide farklı tamlıkta birden çok kural → `kural` en tam olana göre (tekrar üretilebilen kural kaybolmasın);
  ötekiler `parametreler`de.
- Formasyon adı listesi: K13 geçerli (`cekirdek`); küme 011'deki `fikir` kararları birleştirmede düzeltilir.
- Aynı çıktıda "X AL sinyali verdi" ve "şartları sağlayan hisseler" birlikte → rol `giriş`, `rol2: seçim-momentum`.
- Fiyatsız "sinyali kaçırdık / tavan" → `sinyal-sonucu`, `kural: yok`.
- Tahvil fiyatlama, duration → `değerleme-temel`, `rol2: ölçüm-yöntemi`.

## K15. Küme 008 ve 014'ten çıkan sınırlar (07.10)
- Parametresiz standart gösterge ya da formasyon (Supertrend, MOST, DOJI/HAMMER) → `cekirdek` (K13 ile aynı).
- "Python taramasını yaptım" + liste → K10 (içeriğin rolü); yalnız "yazdım, paylaşacağım" → `ürün-hedefi`.
- Önceden paylaşılmamış sinyalin sonradan bildirilmesi ("dün sistemde yakalandı ama yazamadım") `sinyal-sonucu`
  değildir (kitap: daha önce verdiği sinyal) → yöntem varsa içeriğin rolü, yoksa `görüş`.
- Abonelik, Telegram grubu, ücretli hizmet planı → `ürün-hedefi`, `kural: yok`.
- Şiir ya da bilmece içinde gizli sembol (baş harfler: MRSHL) → sembol `semboller`e, notta "mecaz"; rol içeriğe göre.
- "Algoritmam satılık değil / kodlarımı paylaşmıyorum" → `sohbet-duyuru`.
- Yalnız zaman dilimi ya da sıklık ("günlük") → `kural: fikir`.

## K16. Küme 013'ten çıkan sınırlar (07.10)
- İçeriksiz anlatım duyurusu ("strateji anlatımı yapacağım", "mantığını anlatan mesaj paylaşacağım") → K5
  (`sohbet-duyuru`). `araç-öğrenme` yalnız eğitimin kendisi ya da kurs/kitap duyurusu için. Küme 013'teki iki
  `araç-öğrenme` kararı birleştirmede düzeltilir.
- Yöntemsiz giriş fiyatı listesi ya da pozisyon bildirimi ("aldık bekliyoruz") → `görüş` (yöntemsiz hedef fiyattaki
  `çıkış` istisnası girişe uygulanmaz).
- Sonuç sözü + tarama duyurusu aynı gönderide → `ürün-hedefi`, `rol2: sinyal-sonucu`.

## K17. Küme 015'ten çıkan sınırlar (07.10)
- Makine öğrenmesi çıktısı (Train/Test/Accuracy, "predicted up") → `ölçüm-yöntemi`; model ve özellikler yazılıysa
  `cekirdek`, yalnız skor varsa `yok`.
- Algoritma için yalnız veri penceresi ("son 10 yıl") → `fikir`.
- Finans dışı kitap → `sohbet-duyuru`.

## K18. Küme 016'dan çıkan sınırlar (07.10)
- Hakem yalnız ayrışan alana karar verir. İki okuyucunun birlikte talimata aykırı yazdığı alan değişmez; notta
  "ortak aykırı: <alan>" yazılır. Bu kayıtlar birleştirme taramasına girer.
- Belirli sinyale bağlanmayan toplu getiri beyanı ("günlük %4-5 alıyoruz") → `sinyal-sonucu`, `kural: yok`.
- Gelecek paylaşım sözü ("yollayacağım") → `ürün-hedefi`; geçmiş ("yolladım") → `sohbet-duyuru`.
- Genel kod yazma tavsiyesi, ChatGPT gibi araç yorumu → `araç-öğrenme`, `kural: yok`.

## K19. Küme 017'den çıkan sınırlar (07.10)
- Gönderinin gövdesi yöntemi anlatıyor, sonunda "bot da yazmaya başladım" var → Ayırma kuralı 8 (içeriğin rolü).
  K8'deki "duyuru + ölçüt" yalnız gövdesi duyuru olan gönderi içindir.
- Ölçü ve yön yazılı, pencere/eşik yok (korelasyon çift tablosu, Sell/Buy) → `cekirdek`.
- Adı yazılmamış formasyon çıktısı → `fikir`; adı yazılıysa K13 (`cekirdek`).
- Girdisi yazılmamış olasılık sonucu ("x2 yapma olasılığı %1.83") → `ölçüm-yöntemi`, `cekirdek`.

## K20. Küme 020'den çıkan sınırlar (07.10)
- Takvim etkisi (haftanın günü, endeks günü, ay sonu) → `rejim` (bütün piyasa davranışı).
- K12 ile K14 birlikte: sonuçta yöntem adı geçiyorsa ("Momentum hissesi … tavan") K12 (`fikir`); yöntem adı yoksa
  K14 (`yok`).
- Tansu kendi aracının hesap adımlarını (indeksleme, normalize, çizim) anlatıyor → `ölçüm-yöntemi`.

## K21. Küme 018 ve 019'dan çıkan sınırlar (07.10)
- "Modelimiz hazır", "Hazır …" (aracın teslimi) = "yazdım" → `ürün-hedefi`, içeriğin rolü `rol2`. Küme 019'daki
  `portföy` kararı birleştirmede düzeltilir.
- Tarama sonucu teklifi ("bir tane vereyim") = gelecek paylaşım sözü → `ürün-hedefi` (K18). Küme 018'deki
  `sohbet-duyuru` kararı birleştirmede düzeltilir.
- Belirli sinyale bağlı olmayan genel başarı iddiası ("getirim endeksten fazla") → K18 (`sinyal-sonucu`, `kural: yok`).
- Akrostiş şiir: son satır değerlendirme yapıyorsa `görüş`, yapmıyorsa `sohbet-duyuru`; sembol her durumda yazılır.
- Kod çalışıyor ama girdi etiketsiz (df.loc[188]) → `cekirdek`.

## K22. Küme 021'den çıkan sınırlar (07.10)
- K12 ile K13 ayrımı: tanımı herkesçe bilinen ad (harami, FVG, Supertrend, Black-Scholes) → `cekirdek`; Tansu'ya
  özgü, tanımı yazılmamış ad ("Vegas taraması", "momentum sistemim") → `fikir`.
- Geriye dönük çalıştırılan tarama + ertesi gün sonucu → içeriğin rolü (ör. `formasyon`), `rol2: ölçüm-yöntemi`.
- Opsiyon fiyatlaması → `değerleme-temel`, `rol2: ölçüm-yöntemi` (K14 tahvil gibi).
- Dizide kod girdileri önceki gönderideyse → `cekirdek` (K9); dizinin girdileri kendinde olan gönderisi `tam`.

## K23. Küme 024'ten çıkan sınırlar (07.10)
- Araç çıktısı + "geliştirmeye / optimizasyona devam" → `ürün-hedefi`; "da taratıyoruz / bulmaya başladık" → içeriğin rolü.
- Kendi kodunu "buyurun geliştirin" diye vermek → rol `ürün-hedefi` (K6), `rol2` kodun hesabının rolü, `kural` koda
  göre (K11: çalışan ve girdileri yazılı kod → `tam`). Kod kaybolmaz.
- Yer tutuculu parodi sinyal ("$X") → `sohbet-duyuru`.

## K24. Küme 022 ve 023'ten çıkan tek kural: ders dizileri
- Tansu'nun ders dizisi gönderisi bir yöntemi ya da hesabı (ADF, PPP, parite, Black-Scholes) anlatıyor ya da kodla
  yapıyorsa → rol `ölçüm-yöntemi` (ya da hesabın rolü; Ayırma kuralı 8), `rol2: araç-öğrenme`, `kural` içeriğe göre.
- Yalnız kütüphane, dil ya da araç tanıtımı → `araç-öğrenme` (Ayırma kuralı 5).
- Küme 022'deki ders zinciri kararları (`araç-öğrenme` + `rol2: ölçüm-yöntemi`) birleştirmede bu kurala çevrilir.
- Piyasa dışı ekonomi dersi (monopol kâr maksimizasyonu) → `araç-öğrenme`, `kural: yok`.
- "Gruba alımlar tamamlandı, listemiz hazır" → pozisyon bildirimi, `görüş` (K16).

## K25. Küme 025 ve 026'dan çıkan sınırlar (07.10)
- Gösterge koşulu pozisyon kapatıyorsa (Death Cross → sat) → `çıkış`; açıyorsa `giriş`; yalnız onaylıyorsa `teyit`.
- Aynı gönderide "kod paylaşmıyorum" + abonelik/ücretli yazma planı → `ürün-hedefi` (plan gövdeyse).
- Sayısız sonuç paylaşma sözü ("marjları yazacağım") → `ürün-hedefi` değil; sonuç duyurusu → `sinyal-sonucu`, `kural: yok`.
- Kendi kitabının yazım durumu → `ürün-hedefi` (Tansu'nun ürünü), `kural: yok`.

## K26. Küme 027'den çıkan sınırlar (07.10)
- Tansu'nun eğitim yazısındaki örnek kural ("RSI < 30 ise alış sinyali ver") kuraldır: `kural` eşiğe göre (`tam`/
  `cekirdek`); rol K24.
- Tek varlıkta IV/RV volatilite arbitrajı → `giriş` (çift değil: iki varlık yok).
- Fibonacci seviyesi göstergeye (RSI) çizilmiş → `teyit`.
- Sayılı düzey dileği ("8500'e gel") → `görüş` (hedef değil, K6).
- Tansu'nun kendi gönderisinde paylaştığı başkasının çalışması (üst/alıntı değil) → Ayırma kuralı 6 gibi: kural
  başkasınındır; Tansu onaylıyorsa içeriğin rolü, notta "başkasının çalışması: <kim>".

## K27. K22–K24 birleşimi (küme 029)
- Opsiyon ya da tahvil fiyatlaması ders dizisindeyse: rol hesabın rolü (`değerleme-temel`), `rol2: araç-öğrenme`
  (K24). Ders dışında: `değerleme-temel`, `rol2: ölçüm-yöntemi` (K22).
- Tansu'nun liste ya da sistem adı ("Range listemiz", "Arbitraj hissemiz") → K12 (`fikir`); genel yöntem adı
  gönderide yöntem olarak anlatılıyorsa ("range breakout: aralığın tepesini kapanışla kırınca al") → kurala göre.
- Kendi akrostiş şiirini yalnız soruyla yeniden paylaşmak → `sohbet-duyuru`, sembol yazılır.

## K28. Küme 030'dan çıkan sınırlar (07.10)
- İçeriksiz liste duyurusu ("listemizi yapalım", "ilk listem ile sahadayım") → K5 (`sohbet-duyuru`). K21 yalnız
  aracın ya da listenin TESLİMİ ("hazır" + ölçüt ya da liste) içindir. Küme 030'daki bu kararlar birleştirmede düzeltilir.
- Eğitim örneğini yeniden paylaşma sözü → `sohbet-duyuru` (K16); K18'deki söz kuralı tarama/kod içindir.
- Bütün parametreleri yazılı kesişim (EMA 50/200 Golden/Death Cross) → `tam`.
- Metin ile görsel farklı rol gösteriyorsa yöntemi taşıyan parça rolü belirler; öteki `rol2`.

## K29. K22–K27 sınırı (küme 034, 036)
- Tansu'nun taraması ya da listesi bilinen bir formasyonun adını taşıyorsa ("bayrak listesi", "haftalık Elliott
  taraması") → K22 (`cekirdek`): formasyonun tanımı herkesçe bilinir. K27 (`fikir`) yalnız içeriği addan anlaşılmayan
  liste adları içindir ("Range listemiz", "Arbitraj hissemiz", "momentum alanı"). Küme 034 ve 036'daki aykırı kararlar
  birleştirmede düzeltilir.
- Adı ve yöntemi yazılmamış bölge çıktısı (arz-talep kutuları) → `fikir` (K19 gibi).
- Lineer/logaritmik ölçek anlatımı → `ölçüm-yöntemi`.

## K30. Kapalı grupta verilen sinyal (küme 032, 037, 041)
- Tansu'nun kapalı ya da ücretli grubuna verdiği sinyal "daha önce verilmiş" sinyaldir (Ayırma kuralı 9); sonucu
  → `sinyal-sonucu`, notta "grupta verildi". K15'teki "önceden paylaşılmamış" yalnız hiçbir yerde verilmemiş
  (sonradan "sistemde yakalandı") sinyal içindir. Küme 032 ve 037'deki aykırı `görüş` kararları birleştirmede düzeltilir.
- Eşiksiz, aracı kurum payına göre sıralanmış liste: sıralama ölçüsü yazılıysa `cekirdek` (Ayırma kuralı 7: çıktıdaki
  ölçüt kanıttır); yalnız sayı varsa veri tablosu (`yok`).

## K31. Çalışmayan kod (kod-kural-hakem, 07.10)
- Kural, yazılı hesabın ya da koşulun eksiksizliğine bakar. Çalışma hatası (df tanımsız, veri önceki hücrede,
  operatör hatası) kuralı tek başına düşürmez. Kuralı yalnız eksik parametre (K9, K21, K22) ya da açık kural
  (K10 hazır çizim, K24 piyasa dışı ders) düşürür.

## Örnekler
- 1783149446089383961 → `yok`; ust-kod: @BugraComez EMA 12/144/169, tansu "övdü".
- 1845228714109329533 → `yok`; ust-kod: tradingview bağlantısı, tansu "uyguladı" ("Bunu yaptık … tavan da yakaladık").
- 1853136887961043422 → `yok`; ust-kod: tansu "istedi".
- 1829983002304086142 → `baglanti` (we.tl).
- 1840777067882787015 → `baglanti` (we.tl; görseller program çıktısı).
- 1845380189410201878 (arşiv dışı kendi üst: "Kod güncellendi") → ek koşu.
