# Cevaplar 10: Sadakat, ürün, işletme

Yöntem: kaynaklar sırayla okundu (E, D, C, B notları, görseller, KURALLAR, TASARIM, veri-kaynaklari). Olgular `python -c` ile sınandı; dosya kaydedilmedi. Ölçülen olgular ilgili cevapta "ölçüldü" diye işaretli.
Kısaltma: YORUM = kaynak yok, önerilen en küçük düzeltme.

Ortak ölçümler (birden çok cevapta kullanıldı):
- KRDMD (ölçüldü): Yahoo kapanışı ile 09.04.2026 ekranında son kapanış 36,68 ve EMA20/50/100/200 = 31,92 / 30,74 / 29,58 / 28,43 birebir çıkıyor (`ewm(span, adjust=False)`).
- VAKBN–GARAN (ölçüldü): 02.01.2025 = 100 alınınca 14.05.2025'te Tansu grafiğindeki ipucu kutusu X 88,20 / Y 98,00 diyor. Yahoo ham `Close` (auto_adjust=False) ve İş Yatırım ham `HG_KAPANIS` aynı sayıyı veriyor (GARAN 88,20; VAKBN 98,00). Düzeltilmiş seri (`HGDG` ya da `Adj Close`) GARAN için 91,46 veriyor, tutmuyor.
- SMRTG (ölçüldü, HGDG ve Yahoo): 10 kapalı işlemin hepsinde C gününde kapanış SMA250'nin altında (örn. 17,98/19,61; 8,65/9,96). ISKPL'de 5 işlemin 1'i altında.

---

**10-001** — YANLIŞ — TASARIM 2 "Aile = yer + teyit" satırı seçilen üç aileyle uyuşmuyor; üçü de bölge ailesi değil (KURALLAR §3; zone ailesi AEFES/AKFIS ikinci dalgada). Sıra "zone → kırılım → likidite → teyit" ikinci el bir analiz sırası (E K18). Düzeltme: satırı "Aile = koşul + teyit; zone ailesi ikinci dalga" yap.

**10-002** — YANLIŞ — KURALLAR §3 ölçüt 3 ("sayısal sonuç") EMA sıkışmasını geçirmiyor: B/§1 "tek örnek, seçilmiş pozitif, sistematik tablo yok"; KRDMD'de sonuç yok, yalnız "Son Kapanış 36.68" var. EMA yalnız ölçüt 1 ve 4'ten geçiyor. Düzeltme: ölçüt 3'ü "iddia var" diye yaz ve EMA satırına "Tansu iddiası yok; bizim hipotezimiz" ekle.

**10-003** — EKSİK — KURALLAR §3 elenenleri ve nedenini yazmıyor (kaynak yok). D'nin "en sadık" sırası kod kolaylığı ekseni, §3 ölçütleri başka eksen. YORUM: §3'e "Elenenler" satırı ekle: sektör liderleri = sıralama aracı, işlem kuralı/sonuç yok; günlük rebalancing = giriş sinyali yok ve Tansu'nun kendi sonucu pasifin %1,04 altında (D).

**10-004** — EKSİK — Hayır, EMA girişi Tansu'dan esinlenmiyor; Tansu yalnız sıkışma dedektörünü veriyor (B/§1: giriş, stop, hedef yok). TASARIM 2 (P5) "bizim yorumumuz" diyor ama KURALLAR §3 EMA satırı bunu ayrıca söylemiyor. Düzeltme: EMA satırına "Tansu: dedektör. Giriş tetiği: sistemin kendi hipotezi" yaz; raporda "Tansu'nun kuralı" etiketi kullanma.

**10-005** — YANLIŞ — "H" tanımı "birinci elden, az YORUM" (KURALLAR §2); AB=CD'de pivot, tolerans ve stop YORUM. C/§5 kendisi "stop kuralı olmadan birebir tekrar edilemez" diyor. Düzeltme: AB=CD'yi K yap (geometri ve hedef H; giriş/stop K).

**10-006** — EKSİK — Aynı iddia kalmıyor. +%305 tüm sermayeyi bileşik kullanan, masrafsız, tek hisse sonuç (C/§5). Düzeltme (YORUM): sınanan iddiayı "işlem başına getiri dağılımı: 7/10 hedef, hedef +%24–51, stop −%12…−25" diye yaz; +%305 sadakat hedefi değil.

**10-007** — YANLIŞ — Evet, kapatır. Ölçüldü: SMRTG'nin 10 işleminin hepsi C gününde SMA250 altında; sonraki 16 günde kapanış SMA250 üstüne yalnız 1. işlemde 3 gün çıkıyor. TASARIM 5.5 / KURALLAR §3 "SMA250 altı çıkış (bütün aileler)" bu işlemleri girişten ertesi kapanışta keser; Tansu'nun kazananları yeniden üretilemez. (Not: 18→6–8 TL grafiği E K7 SMRTG fiyat paneli.) Düzeltme (YORUM): AB=CD'de SMA250 çıkışını kapat (çıkış: D hedefi ve A stopu); SMA250'li hali ayrı deneme olarak koş.

**10-008** — OLGU — Ölçüldü: SMRTG'de 0/10 işlem SMA250 üstünde; ISKPL'de 4/5. Yani Tansu'nun AB=CD sınaması SMA250 üstü girişi şart koşmuyor. Üç ailede sinyal sayısı farkını ölçmedim (motor yok); EMA için KRDMD sıkışması SMA250 üstünde (28,2 > 26,6).

**10-009** — CEVAPLI — TASARIM 5.5 ve 5.6: "Risk paketi bu bölmeye uygulanmaz"; çiftin çıkışı karşı uçta geçiş. KURALLAR §3'teki "(bütün aileler)" ifadesi yanıltıcı: tek hisse aileleri demek. Düzeltme: ifadeyi "tek hisse aileleri" yap.

**10-010** — EKSİK — Kaynak yok: kapı çıkarma gerekçesi yazılı değil. Kapı ikinci el (E K23, tweet URL'siz) ve çelişkili ("stop R/R'ye göre"). BALAT: TP1 84,88, TP2 87,02, TP3 90,50, stop 64,00 etiketlerinden D ≈ 81,4 çıkıyor; R/R 0,20–0,32 (yeniden hesaplandı, E K11 ile aynı). Düzeltme (YORUM): KURALLAR'a "R/R kapısı yapılmadı: kaynak ikinci el ve Tansu'nun kendi çıktısı ona uymuyor"; R/R yalnız raporda yazılır.

**10-011** — EKSİK — Evet, ikinci el bir ilkeye ters (D: tweet "rolling izle"). Birinci elde yalnız rapordaki "Cointegration p 0,048 CURRENT" var; eşik ve pencere yok. S2-25 yalnız "çıkış yok" diyor, giriş izni kapısını anmıyor. Düzeltme (YORUM): "p > 0,05 ise yeni giriş yok" varyantını ayrı deneme olarak ekle ve KURALLAR'a sapmayı yaz.

**10-012** — EKSİK — Sistem VAKBN/CIMSA sürümünü (uzun-yalnız rotasyon, hep yatırımda) temsil ediyor (TASARIM 5.6 "Tansu'nun sürümü"). AGROT/GARAN iki bacaklı, short ve nakit çıkışlı sürüm dışarıda (D). TASARIM "AGROT–GARAN ayrıca gösterilir" diyor ama hangi sürümle olduğunu yazmıyor. Düzeltme: "AGROT–GARAN rotasyon sürümüyle koşulur; iki bacaklı short sürüm kapsam dışı" yaz.

**10-013** — EKSİK — Kapının eşiği yok (D); kapısız kural daha çok giriş üretir (yön: fazla girişe doğru). Mart–Mayıs 2025'te Z ≈ −2,2'ye inip dönüyor, strateji çizgisi Haziran'a kadar düz; neden bilinmiyor. Düzeltme: sadakat adımında Tansu'nun 6 AL gününü kuralın ürettiği günlerle yan yana yaz; fazla/eksik girişleri listele; kapıyı YORUM bırak.

**10-014** — EKSİK — Kaynak yok. "Bir hisse bir çift" kuralı yalnız seçilen çiftlere yazılı. YORUM: Tansu'nun çiftleri kabul bölmesinin dışında, her biri kendi payıyla ayrı koşulur; çakışma kuralı onlara uygulanmaz.

**10-015** — EKSİK — Sınır yazılı değil. Uygulanan örtük sınır: ikinci el kural, birinci el sonuçla çelişmiyorsa YORUM'dan önce gelir (SMRTG zararları −%12…−25, 2 ATR'nin %7–10,5'inden geniş; ölçüldü). Düzeltme: bu sınırı KURALLAR başlığına yaz ve stop varyantını etiketle ("ikinci el, birinci elle çelişmiyor").

**10-016** — YANLIŞ — E K15 "görsel açılmadı" bayat: ISKPL görselini açtım; tablo "BACKTEST SONUÇLARI (ISKPL), # | Tarih (C) | Sonuç | Getiri % | Sermaye", 5/5 hedef; C/§5 bunu birinci el sayıyor. Ama "C'den alım, D'de satış" ifadesi tweet metninden (ikinci el); görselde giriş fiyatı ve D yok. Düzeltme: E K15'teki notu sil; TASARIM 5.5'e "sonuçlar birinci el, C'den giriş yorumu ikinci el" yaz.

**10-017** — OLGU — Notların kaynak URL'si doğrulanmış tek sadakat kaynağı VAKBN–GARAN raporu (x.com/The_Tansu_/status/2096358189696520213). EMA (KRDMD) ve AB=CD (SMRTG, ISKPL, KRPLS, MARKA) parametreleri 0 URL; "havuz bağlamına" dayanıyor. Zayıf destek: KRDMD EMA değerleri ve VAKBN/GARAN ipucu kutusu gerçek veriyle birebir tutuyor (ölçüldü); yazarı değil, ekranın gerçek olduğunu gösterir.

**10-018** — EKSİK — Sayım birimi çelişkili: KURALLAR "her YORUM", S2-45 "her (aile, varyant, parametre)". Ölçülebilir sonuç: 1.000 tekrarda en küçük p = 1/1001 ≈ 0,001; Holm eşiği 0,05/m; m > 50 olursa hiçbir aile geçemez. Düzeltme (YORUM): deneme = (aile, varyant, parametre vektörü) koşusu; sadakatle sabitlenen YORUM = 1 deneme; tekrar sayısını R ≥ 20·m yap.

**10-019** — EKSİK — "T+1 Open" kolu yalnız etiketi kanıtlar; eğri kapanıştan hesaplanmışsa bir şey kanıtlamaz (D: giriş günü PnL=0). KURALLAR §3 "T+1 açılış birinci el" ifadesi fazla güçlü. Düzeltme: "etiket birinci el; PnL'e uygulanması belirsiz" yaz; dolumu ayırt eden eğri karşılaştırması ancak getiriye bakarak yapılır, bu yüzden yapma.

**10-020** — EKSİK — Tek pencere bizim varsayımımız; Tansu'nun pencereleri 60 ve 120–126 gibi görünüyor (D, YORUM). KURALLAR §3 iki aday yazıyor, S2-23 varsayılan 60. Düzeltme: 60 ve 120'yi iki ayrı deneme koş, ikisini Holm'a say.

**10-021** — CEVAPLI — S2-5 (yeni paylaşım aynı süreçten geçer) ve TASARIM 5.8 ("sonraki her değişiklik yeni deneme"). Yeni Tansu sürümü yeni deneme olur; kayıtlı sürüm bozulmaz. Düzeltme gerekmez; "sadakat = kayıt tarihindeki sürüm" cümlesi eklenebilir.

**10-022** — EKSİK — Çelişki yalnızca sözde. Rapor (NotebookLM, D logo notu) Tansu'nun paylaştığı kaynak; "kapı olarak kullanım" bizim kararımız. TASARIM 4 "kuralı bizimdi" derken kapıyı kastediyor ama yazmıyor. Düzeltme: TASARIM 4'ü "Nabız'ı kapı yapmak bizimdi; skor kutuları Tansu'nun paylaştığı NotebookLM çıktısı" diye düzelt.

**10-023** — OLGU — Ölçüldü (yaklaşık): 2.054,78 TL / (12–13 yan × ~125.000 TL ortalama özsermaye) ≈ %0,13 yan başına. Özsermaye yolu varsayım, kesin değil. TASARIM 5.4'ün %0,1 senaryosu en yakını. Düzeltme: sadakatte Tansu'nun yeniden üretimi için ayrı maliyet kolu "%0,13/yan (Tansu ima)" yaz; kabul eşiği %0,5 ayrı kalır.

**10-024** — EKSİK — Sınama bütün çiftleri ve bütün sinyalleri koşar (KURALLAR §5, TASARIM 5.6), yani başarısızlar da girer. Ama sadakat tablosundaki hedeflerin hepsi olumlu örnek; negatif örnek yok (53'te çift kimliği bilinmiyor). Düzeltme (YORUM): KAPLM'i (D'de tepki yok) sadakat tablosuna "kural bunu sinyal sayar mı?" hedefi olarak ekle.

**10-025** — EKSİK — Evet, fark var ama ölçülebilir. Ölçüldü: Tansu'nun GARAN/VAKBN verisi ham kapanışla birebir (düzeltilmiş seriyle değil). Sınama `HGDG` (temettü dahil) kullanıyor (5.1, S2-13); GARAN'da 14.05.2025'e kadar 91,46 ile 88,20 fark. Düzeltme: sadakat ham seriyle yapılsın; sınamada ham-seri varyantı "veri duyarlılığı" olarak bir kez koşulsun ve fark raporlansın.

**10-026** — OLGU — Ölçüldü: ham `Close` (auto_adjust=False). Tansu'nun ipucu kutusu GARAN 88,20 / VAKBN 98,00; ham `Close` ve İş Yatırım `HG` tutuyor, `Adj Close` / `auto_adjust=True` / `HGDG` (GARAN 91,46) tutmuyor. Seri seçimi artık belirsiz değil (KRDMD EMA'ları da aynı sonucu destekliyor). Düzeltme: TASARIM 7.2'ye "sadakat serisi = ham kapanış" yaz.

**10-027** — OLGU — Tarih serbest değil: tweet 06.09.2026 Pazar 01:01, son işlem günü 04.09.2026 Cuma. Sahte eşleşme olasılığı (varsayım: bağımsız, Z aralığı ≈ 8): ~40.000 aday × (0,001/8)² ≈ 6·10⁻⁴ (±0,0005 tolerans). Ölçüldü: ham Close ile 40.560 aday (pencere 10–399; log oran, β'lı kalıntı iki yön, oran; ddof 0/1; ters işaret; 26.08–08.09) −3,108 / −3,404 çiftini ±0,05 içinde üretmedi. Z formülü henüz bulunmadı.

**10-028** — EKSİK — Sayısal tolerans ve seçim kuralı yazılı değil. Düzeltme: sorgudan önce yaz: ekranda 3 ondalık yazılı sayı için ±0,0005, ΔZ için aynı; aday listesi sabit; birden çok eşleşmede en az parametreli seçilir; eşitlikte YORUM kalır ve ikisi de deneme sayılır.

**10-029** — EKSİK — Yakın: "hep yatırımda" kuralında 6 geçiş tarihi eğriyi neredeyse belirler. Sınır yazılı değil. Düzeltme: sadakat hedefi = Z değerleri ve AL tarihleri; Net K/Z, Sharpe, MaxDD, getiri hedef değildir ve formül seçiminde kullanılmaz (KURALLAR §4'e yaz).

**10-030** — OLGU — Ölçüldü: tek sayı belirlemiyor ama tarihlerle birlikte belirliyor. Oran = (en büyük EMA − en küçük EMA) / en küçük EMA: dönem 17.12.2025–14.01.2026, 20 bar, ortalama %0,639; ekran 09.04.2026, 130 mum. Diğer 7 aday (aralık/EMA200, /kapanış, /ortalama, /en büyük, CV, ddof=1, EMA200/max) ya 16.12 başlıyor ya 21 bar ya da başka dönem veriyor. KRDMD sadakati çözüldü.

**10-031** — YANLIŞ — Katalog yön adlarında çelişkili. Görsel MARKA #13 "Düşüş (AB bacağı aşağı)": A≈95,2 → B≈73 → C≈92,5 → D 70,25 aşağıda; yalnız-alış kuralı bunu üretmez. KRPLS başlığı "Düşüş" ama D 11,29 ve 10,05 yukarıda (A dip, B tepe, C yüksek dip), yani yalnız-alış geometrisiyle uyumlu. C dosyası kural 3 "BUY: A tepe… D aşağı" yazıyor, TASARIM/KURALLAR C→D yukarı. Düzeltme: KURALLAR'a yön sözlüğü ekle; MARKA'yı yalnız aynalı geometri olarak kontrol et; yalnız-alış okuması KRPLS ile gösterilir.

**10-032** — YANLIŞ — KURALLAR §2 çiftte "H" diyor ama ana YORUM'lar (sapma, pencere) çözülmedi; D de "yaklaşık yeniden yapım" diyor. §3'te "1" sırasındaki "H hazırlık" ifadesi yok. Düzeltme: çift rotasyonunu K yap; çözülmezse rapor etiketi "K: sapma formülü ve pencere YORUM" olsun. (Z formülü şu an bulunamadı, bkz. 10-027.)

**10-033** — EKSİK — Çelişki: KURALLAR "her YORUM deneme sayısına girer", sadakat "getiriye bakmaz". Düzeltme (YORUM): sadakat adayları günlüğe "sadakat" etiketiyle yazılır (p üretmedi, Holm'a girmez); seçilen değer kural kaydına girer; kayıttan sonra değişirse yeni deneme.

**10-034** — EKSİK — Planlı değil. Ölçüldü: GARAN/VAKBN'de İş Yatırım ham `HG` serisi Yahoo ham `Close` ile aynı normalize değeri veriyor (88,20 / 98,00). Düzeltme: formül seçildikten sonra aynı hisse ve günlerde `HG` (ham) üzerinde tolerans içinde çıktığını kontrol et; çıkmazsa sınamada `HGDG`, sadakatte `HG` esas, fark raporda yazılı.

**10-035** — OLGU — Ölçüldü: GARAN.IS bugün 2995 satır, 50 satırda hacim = 0 (hayalet); İş Yatırım ~2945. 60 satırlık pencere ≈ 59 gerçek gün (50/2995×60 ≈ 1 satır). Bu kayma küçük ama sıfır değil. Hayalet satırlı ve satırsız aday taramalarının ikisi de Z çiftini üretmedi (bkz. 10-027). Düzeltme: sadakatte satır sayısı ve hacim=0 günleri rapora yaz.

**10-036** — EKSİK — Hata payı tanımlı değil. Etiketle yazılı sayılar (VAKBN raporu, KRDMD) 2–3 ondalık, kesin; KRPLS/MARKA D'leri başlık etiketi ve köşeler piksel okuması (±0,05, C/§3). Düzeltme: hedef başına tolerans = yazılı son hane yuvarlaması veya okuma hatası; okuma tabanlı hedefte sonuç "tutarlı" yazılır, "üretildi" yazılmaz.

**10-037** — EKSİK — Kabul AOF'a bakar (tek gerçek sınama); Yahoo açılış kolu sadakat/duyarlılık. Yazılı değil. Düzeltme: "kabul = AOF dolumu" yaz; açılış kolu ayrı satırda, "Tansu'nun etiketi" olarak raporlansın, Holm'a girmesin.

**10-038** — CEVAPLI — 5.8: 2015–2026 bütün geliştirme verisi; kâğıt üstü dönem (kural kaydından sonrası) tek temiz ayrılmış dönem. KURALLAR §5 Tansu örneklerinin seçilmiş olabileceğini zaten yazıyor. "Getiriye bakmaz" yalnız sadakat adımını bağlar. Düzeltme: KURALLAR §3'e "aile sırası Tansu'nun gösterdiği getirilere bakılarak seçildi" cümlesini ekle.

**10-039** — OLGU — Önerme kısmen yanlış. Boğa yutan mum kodu görselinde yfinance/.IS yok (görseli açtım, yalnız `signal(data, ...)` fonksiyonu). Asıl dayanak: DOAS kodu (`yfinance`, `DOAS.IS`, G-124) ve "AGROT.IS & GARAN.IS" başlığı. Ölçüldü: KRDMD EMA değerleri ve VAKBN/GARAN ipucu kutusu ham Yahoo/İş verisiyle tutuyor. AB=CD aracı için veri kaynağı: kaynak yok.

**10-040** — CEVAPLI — TASARIM 2 "ilk sürümde kapı değil", 3–4: etiket yalnız raporlama; somut uygulama K1(b) eşleştirmesi ve etikete göre ayrı rapor. İlke "ölçülür, uygulanmaz" olarak korunuyor. Düzeltme gerekmez.

**10-041** — EKSİK — Etiket tanımı yok. Nabız SMA 18/35 (görsel 98), BIST-VIX SMA 20/50 (görsel 113) ayrı araçlar. Düzeltme (YORUM): ücretsiz, tek kaynaklı tanım: XU100 kapanış > SMA50 → "yukarı", değilse "aşağı"; tanımı kural kaydına yaz.

**10-042** — EKSİK — KURALLAR "VIX Yahoo'da bedava", TASARIM 4 "Yahoo kullanılmaz" çelişiyor; yasak şirket olayları içindi (VIX'te olay yok). Lisans: kaynak yok. Düzeltme: ya Yahoo yasağına "^VIX hariç" yaz ya da VIX'i etiketten çıkar (YORUM: çıkar, etiket XU100'den üretilsin).

**10-043** — EKSİK — t günü VIX, BIST kapanışından (18:00) ve 19:30 kartından sonra oluşur (ABD kapanışı; piyasa saatleri genel bilgi, kaynaklarda doğrulanmadı). Geçmişte t günü VIX'i kullanmak sinyal anında bilinmeyeni sınıflar. Düzeltme: t−1 VIX kullan ve yaz.

**10-044** — EKSİK — Kaynak yok. Düzeltme: hesaplanamayan günler "etiket yok" grubuna girer, ayrı raporlanır ve K1(b) eşleştirmesinden çıkar; etiket 50 gün (SMA50) sonra başlar.

**10-045** — EKSİK — Dilim p değerleri 5.11'de anılmıyor. Düzeltme: etiket dilimleri keşif amaçlıdır, kabul ölçütüne girmez, p değeri üretmez; yalnız ortalama ve işlem sayısı yazılır; p üretilirse Holm'a girer.

**10-046** — EKSİK — 5.8 "kural, parametre, kod" diyor; etiket tanımı ayrıca anılmıyor. Düzeltme: etiket tanımı ve sınıf sayısı kural kaydına yazılır; değişirse K1(b) p değişeceği için yeni deneme sayılır.

**10-047** — YANLIŞ — Mantıksal olarak çıkmaz. Ayrıca TASARIM 4'te "2023 sonrası tutmadı" gerekçesi, TASARIM üst notuyla çelişiyor ("05.10 ön denemesi rakamları hiçbir kararda kullanılmaz", C7). Düzeltme: "ve 2023 sonrası tutmadı" ifadesini sil; gerekçe: kural bizimdi, Tansu'nun değil; ilke raporlamada kalıyor.

**10-048** — EKSİK — TASARIM 3: Streamlit "Kanıt" ekranı piyasa durumunu okur; akşam biçimi yazılı değil. Düzeltme: raporun ilk üç satırı: tarih, veri durumu, piyasa etiketi; Streamlit aynı satırları üstte gösterir.

**10-049** — EKSİK — Kaynak yok. Etiket kapı olmadığı için kart üretilebilir. Düzeltme: etiket yoksa "etiket yok: <neden>" yazılır, kart üretilir; veri/19:30 kontrolü başarısızsa kart üretilmez (6.1).

**10-050** — EKSİK — Etiket Tansu'nun hiçbir aracına karşılık gelmiyor; bizim tanımımız. Üç araç farklı tarih/anlık görüntülerden (113/114 snapshot 14.12.2025; 98 ve 5/5 tweet'i tarihsiz); "aynı gün çelişki" kaynakta yok. Düzeltme: tek etiket (bizim) gösterilir; Tansu araçları gösterilmez, KURALLAR'a bu cümleyi yaz.

**10-051** — EKSİK — Örnek 5.12 ile çelişiyor: Canlı olmak için p < 0,05 pozitif fazla getiri gerekir. Ayrıca 5.9 güven aralığı günlük portföy üzerinden, örnek işlem başına. Düzeltme: kanıt satırı iki parça yazılsın ("geçmiş: ... / izleme: ..."); izleme yarıdan düşerse aile Deneme'ye döner; örneği Canlı için düzelt.

**10-052** — EKSİK — S2-4: hiçbir aile geçmezse rapor "geçmedi" der, durum etiketi üretilir; ama 6 aylık izleme aileleri Deneme gibi gizli. Düzeltme (YORUM): "izlemede" durumu ekle; kartlar "kâğıt üstü, kanıt tamamlanmadı" etiketiyle ayrı listede gösterilsin.

**10-053** — EKSİK — Böyle bir ekran/kayıt yok. 6.5 yalnız durum etiketi güncelliyor. Düzeltme: işlem listesine çıkış nedeni (stop/hedef/SMA250/A ihlali), MFE ve MAE alanları ekle; Kanıt ekranında işlem tablosu.

**10-054** — YANLIŞ — Üç küme çelişkili: TASARIM 2 (AKTİF/TAMAMLANDI/BOZULDU), TASARIM 6.5 (AKTİF/STOP/HEDEF/BOZULDU), GLOSSARY "Bozulma = SMA250 altı". Tansu'da BOZULDU = A aşıldı (E K15, backtest "stop'a takılan/bozulan"). Düzeltme: nihai küme TASARIM 6.5; STOP = 2 ATR veya A ihlali (Tansu BOZULDU ≈ bizim STOP); BOZULDU = SMA250 altı kapanış; TAMAMLANDI = HEDEF; TASARIM 2'ye eşleme tablosu.

**10-055** — EKSİK — AB=CD'de A ve D sabit, kart yazılabilir. EMA'da stop = giriş − 2 ATR giriş fiyatı ister. Düzeltme: kart "referans = sinyal günü kapanışı" ile yazılsın; formül kartta ("stop = giriş − 2×ATR, ATR = x"); gerçek girişten Levent yeniden hesaplar.

**10-056** — EKSİK — Sistem Levent'in portföyünü bilmez. Düzeltme (YORUM): kart "simülasyonda şu an: X'te; sinyal: Y daha ucuz" yazsın ve geçişin elinde X varsa anlamlı olduğunu belirtsin; Levent'in gerçek pozisyonu ayrı kayıt (bkz. 10-068).

**10-057** — EKSİK — 5.4 masraf %0,3 kaymayı kapsıyor ama kartta ve kanıt satırında dolum varsayımı yazılmıyor. Düzeltme: kanıt satırına "dolum: ertesi gün AOF" ekle; gün yükseğinden alım kötü senaryosu raporda ayrı satır olsun.

**10-058** — EKSİK — Önerme eşiği yanlış, nokta doğru. Ölçüldü (veri/, 99 hisse, 2023+, Wilder ATR14, 90.170 hisse-günü): medyan ATR %3,87; tavan, 2ATR < %10 yani ATR < %5 iken bağlar ve günlerin %80,2'sinde bağlıyor; medyan fiili risk %0,77. Düzeltme: karta "uygulanan büyüklük ve fiili risk" yaz; kanıt satırı aynı büyüklükle hesaplanmalı (5.6 bunu açıkça söylemiyor, yaz).

**10-059** — EKSİK — Koruma yok. Düzeltme: ayar dosyasında tek `sermaye_TL`; kart bunu kullanır. Çift bölmesi: "sermayenin %20'si (5 çift eşit); 1.000.000 TL için 200.000 TL" biçimi.

**10-060** — EKSİK — TASARIM 5.1: göstergeler `HGDG`, seviye ham. Kart için yazılı değil. Ölçüldü (veri-kaynaklari): THYAO HGDG/HG = 0,9769 (2015–2024), son günde 1,0000: bugünün fiyatı uyuşur, SMA250 ve ATR HGDG ölçeğinde biraz farklı. Düzeltme: karttaki bütün fiyatlar bugünün ham ölçeğinde yazılsın.

**10-061** — EKSİK — Kademe tablosu repoda ve kaynaklarda yok (doğrulamadım). Düzeltme: kademe tablosunu Borsa İstanbul prosedüründen oku; stop aşağı, hedef yukarı yuvarlanıp yuvarlanan riskle %1 hesabı güncellensin.

**10-062** — EKSİK — 5.3: kilitli tavanda giriş yok (simülasyon); kart davranışı yazılı değil; tedbirli hisseler 8.4 açık. Düzeltme: sinyal günü kilitli tavansa kart "giriş simülasyonda yok" uyarısıyla yazılsın; tedbir bilgisi için raporda sabit "tedbir bilinmiyor" satırı.

**10-063** — EKSİK — "±" tanımlı değil; birim 5.9'da günlük portföy, örnekte işlem. Anlaşılırlık sınaması kaynak yok. Düzeltme: kart altı tek cümle: "± = %95 aralığın yarı genişliği, günlük portföy fazla getirisi, puan"; Levent'e iki örnek kartı okutup kontrol et.

**10-064** — EKSİK — Kaynak yok. Düzeltme: iki sayı: "doğrulama (2015–2026, kayıt anında dondurulur)" ve "kâğıt üstü (her akşam güncellenir)". 2023 sonrası doğrulama verisi içinde (5.8).

**10-065** — EKSİK — S2-48 yalnız "veri sorunlu" satırı. Düzeltme: raporun ilk satırı üç değerden biri: "TAMAM: hiçbir aile geçmedi" / "VERİ SORUNLU: <neden>" / (koşu yoksa satır yok, bkz. 10-078); bu üç durum için örnek raporlar Levent'e gösterilsin.

**10-066** — EKSİK — Kaynak yok. Düzeltme: Streamlit elle başlatılır (`streamlit run`), dosya değişim zamanına göre veri yenilenir; markdown yerine yan dosya `kanit.json` okunur (bkz. 10-099).

**10-067** — EKSİK — Kodda CSV yazımı yok (`tansu/*.py` içinde `to_csv` yok; doğrulandı). Düzeltme: `sep=";"`, `decimal=","`, `utf-8-sig`; kabul adımı: Levent çift tıklayıp açar, ı/ş/ğ ve sütunlar okunur.

**10-068** — EKSİK — Kayıt yok. Düzeltme (YORUM): Levent için basit işlem defteri (kart kimliği, aldım/atladım, fiyat, tarih); kartla birleştirilince sistem hatası ile kendi kararı ayrılır.

**10-069** — EKSİK — Kart sırası ve "simülasyonda alındı" bilgisi yazılı değil. Düzeltme: kart listesi simülasyon sırasıyla (en likit önce) yazılsın; her kartta "simülasyonda: alındı / boş yer yok".

**10-070** — EKSİK — Raporda anlık görüntü yazılıyor (4) ama kartta yok. Düzeltme: kart CSV'sine `veri_tarihi`, `uretim_zamani`, `snapshot_id`, `kontrol` ekle; Streamlit üstte "bayat" uyarısı (rapor tarihi bugün/son işlem günü değilse).

**10-071** — EKSİK — Kaynak yok. Düzeltme: kart "zaten açık pozisyon: #id" notuyla yazılsın; raporda "yok sayılan sinyal: n".

**10-072** — EKSİK — Sistem Tansu'yu izlemiyor (S2-5: yeni paylaşım `.scratch` işi). Düzeltme (YORUM): Deneme ailelerinin sinyalleri ayrı sayfada (varsayılan kapalı) tutulsun; "KRDMD sıkışması var mı" sorusuna "aile Deneme; kanıt: ayırt edilemiyor" diye cevap verilsin.

**10-073** — EKSİK — Yeniden deneme yok. Düzeltme: 19:30, 20:30, 22:00 koşuları; ilk tazelik kontrolünü geçen kartı üretir; bir hafta boyunca son çubuğun ilk görünme saati logla ve 8.7'yi kapat.

**10-074** — EKSİK — Tarih eşleşirse kısmi çubuk geçer. Düzeltme: koşu zamanı BIST kapanış seansı bitiminden (18:15) önceyse kart üretilmez; ikinci doğrulama: borsapy son kapanışı ile İş Yatırım aynı olmalı.

**10-075** — EKSİK — Eşik tanımsız. Düzeltme (YORUM): hacim son 60 gün medyanının 0,2×–5× dışındaysa rapora uyarı (kart bastırma yerine); yarım günler Takvim'den "kısa seans" etiketiyle ayrılsın. Kısmi çubuk riski 10-074 ile çözülürse bu kuralı sil.

**10-076** — EKSİK — Çelişki gerçek: S2-15 ve Takvim aynı gün için ayrı kaynak. Düzeltme: Takvim resmî tatil listesinden (yıllık, Ocak'ta elle güncellenir) gelsin; takvim "açık" ama veri yoksa "veri sorunlu". Yıllık güncelleyen kim: kaynak yok; Threads'e yıllık iş ekle.

**10-077** — EKSİK — Tanımsız. Ölçüldü: Masaüstü bu makinede OneDrive'a yönlendirilmemiş (kayıt defteri `Desktop = C:\Users\levent\Desktop`), OneDrive riski düşük. Düzeltme: görev ayarları "oturum kapalıyken çalıştır, bilgisayarı uyandır, pil koşulu yok, kaçırılırsa hemen çalıştır"; 14 gün gözetimsiz deneme (iki hafta sonu + bir tatil).

**10-078** — EKSİK — Evet, ayırt edilemez. Düzeltme: Streamlit rapor tarihi son işlem günü değilse kırmızı "RAPOR YOK: koşu çalışmadı" göstersin; koşu başında `kosu_basladi` dosyası yazılsın (rapor yoksa nedeni anlaşılır).

**10-079** — EKSİK — Karar kuralı yok. Düzeltme (YORUM): günlük sözleşme kontrolü (son çubuk tarihi, alan sayısı, HG/HGDG oranı); eksik oran > %5 ise kart yok ve "veri sorunlu"; ≤ %5 ise eksik semboller listelenir ve kalan için kart üretilir.

**10-080** — EKSİK — pyproject'te bağımlılık sürümü ve kilit dosyası yok (doğrulandı). Düzeltme: sürüm kilidi (`pip freeze`) kural kaydına girsin; sürüm değişimi yeniden koşu ve bilinen cevaplı gösterge testi ister; değerler değişirse yeni deneme.

**10-081** — EKSİK — Politika yok; 5.8 "her değişiklik yeni deneme" harfi harfine okunuyor. Düzeltme (YORUM): (a) kural/parametre/evren/maliyet/çıkış değişikliği = yeni deneme; (b) hata düzeltmesi ve refactor: aynı işlem listesi (golden test) ise saat sıfırlanmaz; liste değişirse yeni deneme.

**10-082** — OLGU — Hesaplandı, ölçülmedi. Ölçüm: veri/ 101 dosya 11,4 MB, sembol başına ≈113 KB (5 sütun). 500 sembol × 14 sütun ≈ 158 MB tam kopya; her akşam tam kopya ≈ 39 GB/yıl; istek ≈ 500/gün. Düzeltme: haftalık/aylık tam anlık görüntü + günlük yalnız yeni satır ve manifest hash'i.

**10-083** — OLGU — Hesaplandı. İlk yükleme ≈ 500 `HisseTekil` + 500 olay + 500 borsapy ≈ 1500 istek ≈ 25 dk (1 sn aralıkla). Günlük ≈ 500 + 500 = 1000 istek ≈ 17 dk. "Günlük 1 istek" (S2-17) sembol başına demek; PD zaten `HisseTekil` içinde, ek istek yok. Düzeltme: S2-17'yi sembol başına yaz.

**10-084** — EKSİK — Kaynak yok. Düzeltme (YORUM): açık kart durumu her akşam sinyal tarihinden itibaren fiyat geçmişinden baştan hesaplansın (artımlı değil); böylece çift koşu veya yarım kesilme sonucu değiştirmez.

**10-085** — EKSİK — Dış kanıt yok. Ölçüldü: git var, uzak depo yok (`git remote` boş). Düzeltme: kural kaydı ve deneme günlüğü git'e commit edilsin; uzak özel yedek (zaman damgalı) veya imzalı tag.

**10-086** — EKSİK — "Kişisel kullanım" paket README'sinden (veri-kaynaklari 1.3, 3.1); hukuki dayanak: kaynak yok. 8.1 koddan önce kapanabilir: şartlar okunur. Düzeltme: 7. adım 1'den önce İş Yatırım ve TradingView şartlarını oku, sonucu yaz; S2-52'yi "paket README'si" diye düzelt.

**10-087** — EKSİK — borsapy README ticari kullanımı yasaklıyor, TradingView şartları okunmadı (veri-kaynaklari 3.1). Engellenirse doğrulama: İş Yatırım `HG` + olay tablosu (5.1 ilk kontrol zaten borsapy'siz) ve ham Yahoo `Close` (GARAN/VAKBN'de `HG` ile aynı, ölçüldü). Düzeltme: 5.1'e yedek kaynak olarak yaz.

**10-088** — EKSİK — Geri dönüş yolu yok. Düzeltme: gece, artımlı çekim (günde ~100 sembol), engel/429'da dur ve alarm; yedek: borsapy (başka kaynak) ve yerel önbellek.

**10-089** — EKSİK — Kaynak yok; hukuki sonuç veremem. S2-52 "paylaşılmaz" veri lisansı içindi, Tansu adını/görselini kapsamıyor. Düzeltme: kart altına "yatırım tavsiyesi değildir; kural sağlandı" satırı; Tansu adı/görseli dışarı çıkmaz kuralını S2-52'ye ekle; SPK sınırı için uzman görüşü iste.

**10-090** — EKSİK — Kaynak yok (vergi doğrulanmadı, 8.6). Düzeltme: kanıt satırı ve kart "vergi öncesi, masraf %0,3" yazsın.

**10-091** — EKSİK — KAP şartları okunmadı. Düzeltme: PDF'ler bir kez elle indirilen statik veri olsun (otomatik çekim yok); şartlar yasaklarsa PD tabanlı evren esas kalsın.

**10-092** — EKSİK — Test yok; 5.3 yedi test yalnız motor için. Düzeltme: 250 günlük geçmişi canlı boru hattından gün gün oynat, motorun toplu sonucuyla birebir aynı işlem listesini şart koş (golden test).

**10-093** — EKSİK — Ölçüm tanımsız. Düzeltme: her akşam üretilen kart listesi arşivlensin; sonra aynı gün güncel `HGDG` ile yeniden hesaplanıp fark sayısı rapora yazılsın.

**10-094** — EKSİK — Adil değil. Düzeltme: kâğıt üstü dönem bitince aynı dönem nihai veriyle yeniden hesaplanıp iki satır yazılsın; 5.12.6 eşiği nihai veriyle yapılan kâğıt üstü hesaba uygulansın.

**10-095** — EKSİK — Kapsam listesi yok; Evren değişimi (7.8) kayıttan sonra yapılırsa yeni deneme olur ve 6 aylık saat sıfırlanır. Düzeltme: kayıt kapsamı = kural + evren + maliyet + çıkış + veri kaynağı sürümü; 7. adım 8'i (KAP evreni) kural kaydından önceye al.

**10-096** — EKSİK — Tanımlı değil. Düzeltme: ΔZ dönüşü için elle yazılmış örnek (−3,404 → −3,108: ΔZ > 0); simülatör faizi için sabit faizle (1+r)ⁿ; bölme muhasebesi için tek geçiş; blok yeniden örnekleme için sıfır varyanslı seri; Holm için bilinen p vektörü.

**10-097** — EKSİK — Tohum politikası yok. Hesap: p ≈ 0,05'te 1.000 tekrarın standart hatası ≈ 0,007; p ∈ [0,036; 0,064] tohuma bağlı. Düzeltme: tohum ve sürümler günlüğe yazılsın; iki tohumla koş, karar değişiyorsa "kararsız" yaz ve tekrarı artır.

**10-098** — EKSİK — Test stratejisi yok. Düzeltme: her modül sahte veriyle sınansın; kaynak adaptörü tek arayüz (`fiyat(sembol)`); kaynak sözleşme testleri ayrı ve çevrimdışı çalışsın.

**10-099** — EKSİK — Sözleşme yok. Düzeltme: markdown ayrıştırma yerine `kanit.json`/CSV + `sema_surumu`; sürüm uyuşmazsa Streamlit "UYUMSUZ" gösterip sayı göstermesin; bozuk/eski şemayla test.

**10-100** — EKSİK — §1 ve 5.12 var ama "tutmadı" tanımı yazılı değil. Sadakat (rakam üretimi) ile kabul (kâr) ayrı. Düzeltme: "Tansu'nun gösterdiği haliyle tutmadı = sadakat sürümü 5.12'nin altı ölçütünden birini geçemedi" yaz; değiştirilmiş hali yeni deneme.

---

## Özet

Hüküm sayıları: CEVAPLI 4 · EKSİK 77 · YANLIŞ 9 · OLGU 10 · ZAYIF SORU 0 (toplam 100).

En önemli 10 EKSİK/YANLIŞ ve önerilen tasarım değişikliği:

1. **10-007 (YANLIŞ):** Ölçüldü: SMRTG'nin 10 işleminin hepsi SMA250 altında. SMA250 çıkışı AB=CD işlemlerini girişten sonra keser. Değişiklik: AB=CD'de SMA250 çıkışı yok (çıkış D hedefi ve A stopu); SMA250'li hali ayrı deneme.
2. **10-018 (EKSİK):** Holm: 1.000 tekrarda en küçük p = 0,001; m > 50 ise kabul imkânsız. Değişiklik: deneme birimi = (aile, varyant, parametre vektörü); sadakatle sabitlenen YORUM = 1 deneme; R ≥ 20·m.
3. **10-058 (EKSİK):** Pozisyon tavanı günlerin %80,2'sinde bağlıyor; medyan fiili risk %0,77, "%1 risk" yazısı yanıltıcı. Değişiklik: karta ve kanıt satırına uygulanan büyüklük ve fiili risk yazılsın; 5.6'ya yaz.
4. **10-026 / 10-025 / 10-034 (OLGU, EKSİK):** Tansu'nun serisi ham kapanış (ölçüldü); sınama `HGDG`. Değişiklik: sadakat ham seriyle (İş Yatırım `HG`); sınamada ham-seri varyantı duyarlılık olarak bir kez koşulsun.
5. **10-005 / 10-032 (YANLIŞ):** "H" etiketi AB=CD ve çift rotasyonu için yanlış. Değişiklik: ikisini K yap; rapor etiketi "K: sapma formülü ve pencere / pivot ve stop YORUM".
6. **10-031 (YANLIŞ):** Yön adları çelişkili (C dosyası "BUY = D aşağı"; MARKA #13 aşağı; KRPLS D'leri yukarı). Değişiklik: KURALLAR'a yön sözlüğü; MARKA yalnız aynalı geometri kontrolü.
7. **10-041 / 10-043 / 10-047 (EKSİK, YANLIŞ):** Piyasa etiketi tanımsız, VIX look-ahead'li ve Yahoo çelişkisi; TASARIM 4 gerekçesi ön deneme rakamına dayanıyor. Değişiklik: etiket = XU100 kapanış > SMA50; VIX etiketten çıkar; "2023 sonrası tutmadı" ifadesi silinsin.
8. **10-081 / 10-095 (EKSİK):** Değişiklik politikası yok; Evren değişimi 6 aylık saati sıfırlar. Değişiklik: kural kaydı kapsamı + "aynı işlem listesi = yeni deneme değil" politikası; KAP evreni kural kaydından önce.
9. **10-078 / 10-073 / 10-077 (EKSİK):** Koşu hiç çalışmazsa Levent bunu ayırt edemez; veri geç gelirse yeniden deneme yok. Değişiklik: Streamlit "RAPOR YOK" uyarısı, 19:30/20:30/22:00 koşuları, Görev Zamanlayıcı ayarları, 14 günlük gözetimsiz deneme.
10. **10-055 / 10-056 / 10-085 (EKSİK):** Kartta giriş/stop AOF'a bağlı, çift kartı Levent'in elindekini bilmiyor, kayıt ve deneme günlüğünün dış kanıtı yok (git var, uzak depo yok). Değişiklik: kartta "referans" fiyat ve formül; "simülasyonda şu an X'te" satırı; kural kaydı ve günlük commit + uzak yedek.

Ek bulgu (sadakat sonucu): KRDMD oran formülü çözüldü: (en büyük EMA − en küçük EMA) / en küçük EMA (10-030). VAKBN–GARAN Z formülü 40.560 adayla bulunamadı (10-027); çift satırı K olarak kalmalı.
