# Tansu ham yapıştırmalar (sohbet kayıtlarından)

Kaynak: Codex oturumları (salt okuma). Kayıtlar 2. dosyada devam eder: `ham-yapistirmalar-2.md`. Metinler birebir; yazım hataları, ters eğik çizgili işaretler ve `&#x20;` korunmuştur. Saatler UTC (Türkiye = UTC+3).

## 1. Özet

- Taranan Codex oturumu: 113 dosya (Tansu adı geçen; sessions + archived_sessions).
- Taranan Claude kaydı: 105 dosya. Kullanıcı mesajlarında ham Tansu metni ya da görseli yok (yalnız planlama ve alt ajan raporları). 1 PNG var (SHA-256 başı `2142045686fbcecd`, 2026-09-27); Tansu içeriği değil, alınmadı.
- Codex ekleri: 181 klasör; 172 metin eki. Hiçbiri Tansu ham tweeti değil (CEVDET görev metinleri, kod, ajan raporları). Görsel eki yok.
- Ham yapıştırma bulunan oturum: a0438c (ana), a045c9 (aynı yapıştırmaların tekrarı); yalnız bağlantı bulunan oturum: a0769a.
- Benzersiz kayıt: 263 (metin+görsel özdeşliğine göre; 19 tanesi yalnız bağlantı).
- Benzersiz Tansu tweet bağlantısı (status): 24.
- Benzersiz Tansu görseli: 188 (beyinde olan: 182; beyinde olmayan: 6).
- Beyinde notu olmayan kayıt: 21 (metin/görsel 19, yalnız bağlantı 2).
- Ham yapıştırma sayılmayan Levent mesajları (dışarıda): a0438c sıra 14 (profil bağlantısı ve görev tanımı), 19, 32 (PDF isteği), 36.

Eşleme kuralı: görsel için SHA-256; tweet bağlantısı için `source_url`; düz metin için konu eşleşmesi (TF-IDF kosinüs). Beyin notları özet olduğundan skorlar düşüktür; düşük skorlar elle doğrulandı.

## 3. Beyinde olmayanlar

Metin/tweet (görsel dahil):

- R009 (2026-08-27 17:01 UTC): Dün olmadı ama bu akşam iyi bir formasyon bulursam, böyle tam arz talep bölgesinde vereceğ → önerilen `tweet-arz-talep-bolgesinde-formasyon-bekleyisi.md`
- R065 (2026-08-27 20:39 UTC): Nihai hedef Tek bir tuş ile temel ve teknik analizin yapıldığı, değerlemenin yapıldığı, LL → önerilen `tweet-nihai-hedef-tek-tus-temel-teknik-degerleme-llm-nlp.md`
- R166 (2026-08-28 04:33 UTC): Aslında yapacak o kadar çok şey var ki bazen nereden başlasam diye oturup düşünürken buluy → önerilen `tweet-excel-degerleme-calismasi-koda-donusumu.md`
- R180 (2026-08-28 06:05 UTC): Python ve AI ile Stratejik Yönetimi Yeniden Kodlamak Bir kurumun Vizyon ve Misyonu ile sah → önerilen `tweet-python-ai-stratejik-yonetim-vizyon-misyon-kodlama.md`
- R228 (2026-08-28 12:22 UTC): Derslerde öğrencilerin yaptığı ve çok sık karşılaştığım bir sorun. Aman diyeyim. Korelasyo → önerilen `tweet-korelasyon-yuksek-istatistiksel-arbitraj-garanti-degil.md`
- R229 (2026-08-28 12:22 UTC): Konveks Rotasyon Stratejisi Nasıl Olmalıdır? Sırada bakleyen projelerden sadece bir tanesi → önerilen `tweet-konveks-rotasyon-stratejisi-makro-dongu.md`
- R231 (2026-08-28 12:29 UTC): Selamlar Biliyorsunuz, sadece hisse senetlerinin ya da kripto paraların fiyat grafiğine ba → önerilen `tweet-fiyat-grafigi-otesi-makro-bakis.md`
- R232 (2026-08-28 12:30 UTC): Sektör Rotasyonunda Yapılan En Büyük Hata: "Hacim Tuzağı" Geçen gün bir dostum kritik bir  → önerilen `tweet-sektor-rotasyonu-hacim-tuzagi-sabit-tl-esigi.md`
- R233 (2026-08-28 12:30 UTC): RSI 30 İle İşleme Girişte ve İki Aşamalı Çıkış Stratejisi Bu strateji, teknik olarak iki a → önerilen `tweet-rsi30-giris-iki-asamali-cikis.md`
- R234 (2026-08-28 12:31 UTC): Makine öğrenmesi modellerini aslında hisse senedi işlemlerinde kullanmayı pek sevmem ama t → önerilen `gorsel-paket-129-doas-lojistik-regresyon-hacim-rsi-filtreli-strateji.md`
- R235 (2026-08-28 12:32 UTC): (yalnız görsel) → önerilen `gorsel-paket-130-piyasa-evreleri-birikim-dagitim-semasi.md`
- R236 (2026-08-28 12:32 UTC): İkili Dip (Double Bottom) ve Mum Tetikleyicileri "W" harfi şeklindeki bu formasyon, fiyatı → önerilen `tweet-ikili-dip-mum-tetikleyicileri.md`
- R237 (2026-08-28 12:33 UTC): Birikim süreci nasıl olur? Her şey genelde piyasa için kötü algılanan bir haberle başlar.  → önerilen `tweet-birikim-sureci-kotu-haber-akilli-para.md`
- R238 (2026-08-28 12:34 UTC): Sizin paranızı istiyorlar Dikkatli olun Geniş gövdeli mum yüksek hacim, ok Dar gövdeli mum → önerilen `tweet-mum-govde-hacim-anomalisi-uyarisi.md`
- R239 (2026-08-28 12:34 UTC): Statik iz süren stop: Hedef = Giriş + (1.5 × Giriş ATR) → Sabit kalır Dinamik İz Süren Sto → önerilen `tweet-statik-dinamik-iz-suren-stop-atr.md`
- R241 (2026-08-28 12:42 UTC): Bu hissede ne oldu bugün, gelin hep beraber bakalım. 1. Piyasa Yapısı ve Fiyat Hareketi Yü → önerilen `gorsel-paket-131-alka-elliott-wave2-fvg-temas.md`
- R242 (2026-08-28 12:43 UTC): FVG Stratejisi Açısından Grafik Analizi: Neden Yükselen Dipler Daha Önemli? Piyasada bir y → önerilen `gorsel-paket-132-fvg-yukselen-dipler-wave3-abc-duzeltme.md`
- R243 (2026-08-28 12:44 UTC): FVG Ticaret Stratejilerini de kısaca anlatalım mesai başlamadan, bugün yoğun bir gün bir s → önerilen `tweet-fvg-ticaret-stratejileri-gap-fading.md`
- R244 (2026-08-28 12:45 UTC): Medyanı şöyle bir kanal gibi kullanın arkadaşlar. Biraz üzerinde düşünelim. \ &#x20; → önerilen `gorsel-paket-133-medyan-kanal-kullanimi.md`

Bağlantısı olup notu olmayan tweetler:

- R254: https://x.com/The_Tansu_/status/2095218573631279414
- R256: https://x.com/The_Tansu_/status/2095201144544846208

Beyinde olmayan görseller (6), okumalarıyla:

- `4a8a63b278545371432ca2e1043389c16c1c890f80f70ba33bcac707ac2f49e1` (R235, G1): Kitap sayfası fotoğrafı (şema, sayfa altı kesik). Kutular: "Yükselen Trend", "Birikim Süreci", "Alım Tepesi" (mor), "Test" (yeşil), "Dağıtım Süreci", "Satış Tepesi" (mor), "Düşen Trend". Birikim ve dağıtım yatay aralıklarında kırmızı üst/alt çizgi; yükselen trend mavi ok, düşüş kırmızı ok. Sayı yok.
- `5f42136e68951a56a5d7df436f3d07060a7f7a673780864c67a0f493f7c88455` (R242, G2): Başlıksız mum grafiği (siyah zemin). Etiketler: 0, 1, 2, 3 (mavi), HH, HL, A (sarı), B (kırmızı), C (yeşil). Mavi çizgi 0-1-2-3; 3 sonrası kırmızı kesik A-B-C düzeltmesi; sağda sarı/yeşil FVG-talep kutuları; soldan sağa uzanan kırmızı ok. Sayısal değer yok.
- `64ed5783a059eb675399f277eae27be6643bb90889fd106889f8ffa385219a45` (R241, G1): Başlık: "ALKA - FVG TEMAS (0.00%) | BULLISH | ELLIOTT WAVE 2 (Düzeltme: -39.3%)". Lejant: BB Üst (14), BB Alt (14), EMA(9), RSI(14), EN YAKIN FVG (sarı nokta). Eksen: Fiyat (TL) 6–16; mavi çizgi 0→1 (yaklaşık 7,5 → 16), kırmızı kesik düzeltme, sarı kalın kutu (FVG/talep) yaklaşık 9,6–10 TL bandında; fiyat kutuya değmiş.
- `93f056e352b58f1092386c6f8fb5c4bb5632acad9af926fbf4e438e3c7a2627a` (R234, G1): Başlık: "DOAS.IS - ML + Hacim + RSI Filtreli Strateji". Üst panel lejantı: RSI, SAT (kırmızı aşağı üçgen), Güçlü AL (Vol+RSI) (yeşil yukarı üçgen), EMA 21 (turuncu), Fiyat (mum), Aşırı SATIM (yeşil bant), Aşırı ALIM (kırmızı bant). Üst panel fiyat ekseni 100–300 (dip bölgesi yaklaşık 85–90, tepe yaklaşık 240); dipte 3 AL ve 2 SAT işareti, yatay/tepe bölgesinde çok sayıda SAT ve AL. Alt panel: "RSI (Momentum Filtresi)", ekseni 20–100, 30 ve 70 kesik çizgileri, beyaz çizgi "Trend Ayrımı (50)". Görselde doğruluk/kesinlik/duyarlılık sayısı yok (tweet metninde %55,00 / %55,31 / %45,44).
- `da70890c6b4e08f572df7e617dd8e91e0d1c33d490794703d100d45be1e740af` (R244, G1): Küçük kesit (407x293): koyu zeminde mum grafiği; sarı noktalı üst bant çizgisi, yeşil kesik orta/alt bant çizgileri ve aralarında koyu yeşil dolgulu kanal; solda iki koyu dikey şerit. Başlık, lejant ve sayı yok. Tweet metni: medyanı kanal gibi kullanma önerisi.
- `eebcd1b52610af6687f26dd35e7dd8ce4ac742a75e376078a6ad442bfa744476` (R242, G1): Başlıksız mum grafiği (siyah zemin). Etiketler: 0, 1, HH (yeşil), A (sarı), B (kırmızı), C (yeşil), HL, LH, LL. Mavi çizgi 0→1, kırmızı kesik A-B-C düzeltmesi, sarı kalın dikdörtgen (FVG) ve altında koyu yeşil bant; C noktası kutunun üst kenarında. Sayısal değer yok.

## 2. Kayıtlar (tarih sırasıyla; R001–R153 bu dosyada, devamı `ham-yapistirmalar-2.md`)

### R001 · 2026-08-27 16:40 UTC · Medyan Temelli Finansal İndikatörler · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Net söylüyorum üzerinde çalışın  Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın  Medyan nedir açıp okursanız, ilk tanımı ile zaten aydınlanma yaşayacaksınız

Beyin notu: `tweet-medyan-temelli-finansal-indikatorler.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R002 · 2026-08-27 16:43 UTC · Sektör Rotasyonundan Hisse Seçimine Analiz Zinciri · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bu akşam şunu yapacağım  Sektör rotasyonu, yüksek korele sektörler, lider sektör, lider sektörde Dupont analizi, ucuz kalmış hisseler çalışması, bu hisselerin mevsimsel satışları vb vb App’da da olacak Paylaşırım biterse

Beyin notu: `tweet-sektor-rotasyonundan-hisse-secimine.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.29; düşük skorlar elle doğrulandı)

### R003 · 2026-08-27 16:46 UTC · ALARK Trend Kırılımı ve Bearish Butterfly Senaryosu · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> [#ALARK](https://x.com/hashtag/ALARK?src=hashtag_click) güzel trend kırılımı yaptı ve bearısh butterfly yapı oluşturmaya gidiyor  Strateji 125.42'ye kadar long fırsatı uyarısı verdi Ancak pullback yapar mı izlemek lazım.

Beyin notu: `tweet-alark-125-42.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.38; düşük skorlar elle doğrulandı)

### R004 · 2026-08-27 16:51 UTC · İlk Uygulama Algoritmaları ve Tarama Yol Haritası · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Uygulamanın ilk algoritmaları; Arbitraj Volatilite Harvesti Harmonik yapılar (ABCD, Kelebek, Gartley) Alpha Hisseleri Momentum Hisseleri  Haftalık kanal dibine temas eden hisse taraması Düşeni kıran Farklı kırılımları gösteren tarama Takoz TOBO OBO İlk bunlar olacak  Bir de bayrak flama olur

Beyin notu: `tweet-uygulama-algoritmalari-v1.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.35; düşük skorlar elle doğrulandı)

### R005 · 2026-08-27 16:53 UTC · Harmonik Formasyonlarda Momentum Squeeze Zamanlaması · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Harmonik formasyonlari her kitap anlatir ama hangi noktada momentum squeeze olur onu pek anlatmazlar bence bu konuda biraz kafa yorabilrsiniz alin size proje konusu

Beyin notu: `tweet-harmonik-momentum-squeeze-projesi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.10; düşük skorlar elle doğrulandı)

### R006 · 2026-08-27 16:55 UTC · İlk Uygulama Algoritmaları ve Tarama Yol Haritası · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Takoz olur, Opsiyon fiyatları ile ABD borsasında analizler olur, ardından da yavaş yavaş ilerletiriz.

Beyin notu: `tweet-uygulama-algoritmalari-v1.md` — dayanak: konu eşleşmesi (not Takoz/bayrak/flama satırını içerir)

### R007 · 2026-08-27 16:57 UTC · İlk Uygulama Algoritmaları ve Tarama Yol Haritası · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bir de bayrak flama olur

Beyin notu: `tweet-uygulama-algoritmalari-v1.md` — dayanak: konu eşleşmesi (not Takoz/bayrak/flama satırını içerir)

### R008 · 2026-08-27 16:57 UTC · Harmonik Formasyon ve Tarama Görsel Paketi 01 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> (metin yok; yalnız görsel)

Görseller:
- G1: SHA-256 `ad5cfff8e81bf9088f055fe74c9c2c40416ec55a3b9ffed6ed225755036b4e44` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-f56aadd4-ee2f-43aa-93b0-cb2240699b05.png` · beyinde VAR: `assets/gorsel-paket-01/01-harmonik-d-226-80-tamamlandi.png`
- G2: SHA-256 `79a8932c9813e574fe8d230990abaffdd9e193b47ce7d97f6864c6b435475de3` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-9a0fb832-b7e6-454d-9acd-0ead30ca2ec5.png` · beyinde VAR: `assets/gorsel-paket-01/02-zonlar-volume-profile-momentum.png`
- G3: SHA-256 `24972fb5a33e100234f4423f1dc1407759286bf7d10576e098bce3286a0ff1c0` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-1c1c1ad9-83ed-40d8-a3bc-5becf44dcfae.jpg` · beyinde VAR: `assets/gorsel-paket-01/03-krpls-swing-fibonacci-abcd-dusus.jpg`
- G4: SHA-256 `3a043cc72cb4d1ad21959355769e594f4aba2a3cf455af37e8d6d29e217a0748` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-80a053af-cf81-4534-b831-eb64c50d165a.jpg` · beyinde VAR: `assets/gorsel-paket-01/04-zonlar-volume-profile-momentum.jpg`
- G5: SHA-256 `48450510d59041fa7665458c7aeb2b60e87ba27a741c3df5249e2df373f92680` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-ff803410-bde6-4b04-ad12-b306740395f7.png` · beyinde VAR: `assets/gorsel-paket-01/05-harmonik-d-11-29-tamamlandi.png`
- G6: SHA-256 `fb7446fe94e52d46c432b3d2e7bf271b6c64ba406a7135173fd1b5c5c33d5269` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-7f5eca9b-cf2e-4171-9e42-485e10c0777e.jpg` · beyinde VAR: `assets/gorsel-paket-01/06-dgate-kelebek-al-aktif.jpg`
- G7: SHA-256 `899b66febe902ee0dcea8e3b1d6662d2239b2e95c73b34b0c2fb5c398d65e712` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-ce0e723c-1e10-4d24-ae60-6d69b5f8db93.png` · beyinde VAR: `assets/gorsel-paket-01/07-zonlar-yatay-sikisma.png`
- G8: SHA-256 `65ef669842a7cbb7e7c3b9055c4c0bbced7372dd2e219c0108ad2753939540cc` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-308f829d-76ef-4d9a-bbdd-b6d57ffb9ecb.jpg` · beyinde VAR: `assets/gorsel-paket-01/08-ucgen-flama-formasyon.png`
- G9: SHA-256 `d7dcc826ade0530c177477892e194e2bcdc67790107766816af3095334de6fe7` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-740f81ae-d223-4fd0-b9cb-e25d60f6342c.png` · beyinde VAR: `assets/gorsel-paket-01/09-marka-pattern13-backtest-dusus.png`

Beyin notu: `gorsel-paket-01-harmonik-formasyon-tarama.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R009 · 2026-08-27 17:01 UTC · Dün olmadı ama bu akşam iyi bir formasyon bulursam, böyle tam arz tale… · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Dün olmadı ama bu akşam iyi bir formasyon bulursam, böyle tam arz talep bölgesinde vereceğim

Beyin notu: **beyinde yok** (önerilen yeni ad: `tweet-arz-talep-bolgesinde-formasyon-bekleyisi.md`)

### R010 · 2026-08-27 17:03 UTC · FROTO Nakit Tamponu ve Piyasa Değeri Oranı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Analiz Nakit ve Nakit Benzerleri / Piyasa Değeri %18.89 Yani şirketin her 100 TL piyasa değerine karşılık yaklaşık 18,9 TL brüt nakdi bulunuyor. Bu oran tarihsel ortalama olan %17,17’nin biraz üzerinde; likidite açısından olumlu.Ancak oran tek başına “hisse ucuz” anlamına gelmez  Borçlar düşülerek net nakit / piyasa değeri hesaplanmalı. Nakit artışı faaliyetlerden mi, yeni borçlanmadan mı geliyor bakılmalı. Serbest nakit akışı ve yatırım harcamaları incelenmeli. Oranın yükselmesi bazen nakit artışından değil, hisse fiyatının düşmesinden kaynaklanabilir.  Enflasyon ortamında nakdin döviz/faiz dağılımı ve reel getirisi önemlidir. Kısaca FROTO’nun nakit tamponunun tarihsel ortalamanın üzerinde olduğunu gösteriyor fakat yatırım kararı için borçluluk ve nakit akışıyla birlikte değerlendirilmelidir.

Beyin notu: `tweet-froto-nakit-piyasa-degeri-18-89.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.32; düşük skorlar elle doğrulandı)

### R011 · 2026-08-27 17:06 UTC · Gartley ve Butterfly İçin Ayrı Tarayıcı Modülleri · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Gartley ile butterfly kodlarını entegre ederek bir ortak tarama sistemi yazmak fikri maalesef beni hasta etti, bitti ama asla tavsiye etmiyorum. Gartley taramasını ayrı yapın butterfly taramasını ayrı yapın. Konsolide etmek bünyeye büyük zulüm.

Beyin notu: `tweet-gartley-butterfly-ayri-tarayicilar.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı)

### R012 · 2026-08-27 17:08 UTC · Çoklu Sistem Sonuçları ve Provenance Görsel Paketi 02 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> (metin yok; yalnız görsel)

Görseller:
- G1: SHA-256 `b5408fd1a147e7bed0722e8dd3c5d947df50b2712d6fd96a866f1b2d28da9018` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-7141ebb9-5634-423c-ae6d-350be9b63e47.png` · beyinde VAR: `assets/gorsel-paket-02/01-soke-luks-coklu-sistem-sonuclari.png`
- G2: SHA-256 `f06e20553983c268ed2f0913922c475e104b5f16bcb180990bfaa604ee302249` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-d4821f04-7c75-48be-bcfa-86c58cdc16b5.jpg` · beyinde VAR: `assets/gorsel-paket-02/02-soke-carney-gartley-detay.jpg`

Beyin notu: `gorsel-paket-02-coklu-sistem-provenance.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R013 · 2026-08-27 17:11 UTC · Harmonik Formasyonlarda X-B Trend Çizgisi Kırılım Stratejisi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Harmonik formasyonlarda trade yapmanın bir yolu da XB noktasından çizilecek olan trend çizgisinin bullish ya da bearish harmonik yapısına göre, aşağı ya da yukarı yönder kırılmasıdır. Duruma göre short ya da long pozisyon alınır.

Görseller:
- G1: SHA-256 `c07e0a8621770af7558ca3dd0948bb6f177b57d181df9d63240d38fe5dc4a263` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-905b2a02-92ef-4ca4-a134-4408b78d58b8.jpg` · beyinde VAR: `assets/tweet-harmonik-xb-trend-kirilimi-stratejisi/01-kaplm-xb-trend-kirilimi.jpg`

Beyin notu: `tweet-harmonik-xb-trend-kirilimi-stratejisi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R014 · 2026-08-27 17:20 UTC · Gartley D Noktası Sonrası Tepki Penceresi ve Belirsizlik · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Her gartley çalışmaz ama çalışmasa bile oluşumunda bazı stratejiler kurgulanabilir. 10 gün içinde D noktasından bir tepki yapmıyor ise belirsiz bir yapı olarak bakılabilir.

Görseller:
- G1: SHA-256 `5b34155caed6599b884f2b27e541a91cc04a11999e917282121293882762be5b` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-17802716-7579-42c3-b6d1-475d4788d68e.jpg` · beyinde VAR: `assets/tweet-gartley-d-tepki-penceresi/01-sayas-gartley-d-tepki-penceresi.jpg`

Beyin notu: `tweet-gartley-d-tepki-penceresi-10-gun.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R015 · 2026-08-27 17:25 UTC · Haftalık Bullish Gartley ve Uzun Vadeli Talep Alanı Taraması · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Allahım; Haftalık taramada uzun vade talep toplama alanında C noktası oluşmuş ve D hedefi belirlenmiş XABC örüntüsünü tamamlamış bullish gartley nasib et bu hafta sonu

Beyin notu: `tweet-haftalik-bullish-gartley-talep-alani-tarama.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.29; düşük skorlar elle doğrulandı)

### R016 · 2026-08-27 17:31 UTC · AB=CD Formasyonunda CD Bacağı Şiddetinin Belirleyicileri · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> AB=CD patterninde, CD bacağının şiddetini ne belirler? Çok önemlidir güzel para bırakır.

Beyin notu: `tweet-abcd-cd-bacagi-siddet-belirleyicileri.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı)

### R017 · 2026-08-27 17:33 UTC · SMRTG AB=CD Backtest Görsel Paketi 03 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> (metin yok; yalnız görsel)

Görseller:
- G1: SHA-256 `b5d3f0ca7c166179d08d07074803c6a8318882c69553aa2373a52515316e2ae2` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-92c83111-ac63-4368-9b76-fb49b0773c66.jpg` · beyinde VAR: `assets/gorsel-paket-03/01-smrtg-swing-fibonacci-abcd-analizi.jpg`
- G2: SHA-256 `9118f4db4f4cc4e81fc0276100a9c36759687320914aeab24ab1d37983e80b93` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-9213ba1b-55d8-447e-9773-80278c46d508.png` · beyinde VAR: `assets/gorsel-paket-03/02-smrtg-backtest-sonuclari.png`

Beyin notu: `gorsel-paket-03-smrtg-abcd-backtest.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R018 · 2026-08-27 17:37 UTC · ISKPL AB=CD C'den D'ye Backtest Örneği · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bazen müthiş çalışır:) AB=CD 1000 günlük C noktasından alım yapılsa idi D satış karları.

Görseller:
- G1: SHA-256 `ac4da31ae9c2cb02f3cad65a940040f92a22ce315ea78adc01e1a6523c94df3c` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-3816a3dd-3fdf-48b3-81b8-34a15e762499.png` · beyinde VAR: `assets/tweet-iskpl-abcd-cden-dye-backtest/01-iskpl-abcd-cden-dye-backtest.png`

Beyin notu: `tweet-iskpl-abcd-cden-dye-backtest.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R019 · 2026-08-27 17:42 UTC · AB=CD Geometrik Geçerlilik ve Bozulma Kuralları · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> AB=CD Not alın lazım olur BC, AB'yi aşamaz  BC tam 1.00 olabilir D, B'yi aşmalı C'den sonra fiyat A'yı geçerse patern bozuldu sayılır (CD bacağı artık orijinal yapıyı tamamlayamaz)

Beyin notu: `tweet-abcd-geometrik-gecerlilik-kurallari.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.21; düşük skorlar elle doğrulandı)

### R020 · 2026-08-27 17:45 UTC · Fibonacci Extensionların AB=CD ile Kullanımı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bilmeyenler, FIBO extension'ları öğrenin arkadaşlar ve ABCD ile nasıl kullanılacağını.

Görseller:
- G1: SHA-256 `fd54b913243fcea354e2e09fe06c5c1bdcd3e090b2df6da093e24d453c980c3b` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-cad02fa2-0859-4b04-9a67-e67f1266ef63.png` · beyinde VAR: `assets/tweet-fibonacci-extension-abcd-kullanimi/01-a1cap-fibonacci-extension-abcd.png`

Beyin notu: `tweet-fibonacci-extension-abcd-kullanimi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R021 · 2026-08-27 17:49 UTC · ML Trade Modelinde 13 Günde 9 İsabet · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> ML ile trade hiç sevmem ama ara ara bakarım Finansta %70 çok yüksek bir başarı oranıdır. Bence model gelişmeye açık 13 trade gününde 9 isabetli tahmin yaptık

Görseller:
- G1: SHA-256 `b5f8f70aa9db21dc52d755da10d68d07ed76903d10d8ada8a5ce14318a3ae107` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-2f820049-94e0-4dec-9236-55b1413a83b5.png` · beyinde VAR: `assets/tweet-ml-trade-13-gun-9-isabet/01-ml-trade-hit-rate.png`

Beyin notu: `tweet-ml-trade-13-gun-9-isabet.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R022 · 2026-08-27 17:52 UTC · Momentum ve Faaliyet Nakit Akışı 5x5 Portföy Araştırması · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şu fikre yükselmeyen olmaz sanırım Yeni bir proje fikri Daha önce anlattığım momentum stratejisini beni takipe denler bilir Bir adım ileriy gdelim şimdi  Her çeyrekte, tüm hisse senetlerini momentumlarına  göre sıralayın, ve onları Mom1'den Mom5'e kadar beş eşit dilimli ayirin. Hisselerin en üst %20'lik dilimini Mom5 portföyüne, en alt %20'lik dilimini ise Mom1 portföyüne atin.  İkinci olarak, tüm şirketleri faaliyet nakit akışlarına göre bağımsız bir şekilde sıralayarak 1'den 5'e kadar yeni beşlik dilim portföylere ayırın. 5, en yüksek nakit akışına sahip %20'lik hisseleri içerirken; 1, en düşük nakit akışına sahip %20'lik kısmı oluştursun.  Ardından, 25 farklı kombinasyon portföyü oluşturun. Bu portföyler, bahsi geçen iki bağımsız sıralamanın kesişimlerinden meydana geliyor. Buna göre aynı anda hem en düşük momentuma hem de en düşük nakit akışına sahip %20'lik dilimdeki hisseler vb lerini bulacaksınız  Asıl odaklandımaniz gereken portföy ise aynı anda hem en yüksek momentuma hem de en yüksek nakit akışına sahip üst %20'lik dilimdeki tüm şirketleri içermeli.  Kolay gelsin.

Beyin notu: `tweet-momentum-faaliyet-nakit-akisi-5x5-portfoy.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı)

### R023 · 2026-08-27 17:55 UTC · Bullish Engulfing Mum Yapısı ve Kod Mantığı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> İşte bullish engulfing mum yapısı

Görseller:
- G1: SHA-256 `baad706bc91c37d11d311e30d56f3317afac817b01c152686631fd4aaabeea17` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-7a950f8a-67ea-4bbf-98e3-6121058f6279.png` · beyinde VAR: `assets/tweet-bullish-engulfing-mum-kodu/01-bullish-engulfing-kodu.png`

Beyin notu: `tweet-bullish-engulfing-mum-kodu.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R024 · 2026-08-27 17:59 UTC · ACSEL Direnç Kırılımı ve Volume Profile VAL Senaryosu · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Her harmonik %100 çalışır diye de bir kaide olamaz Destek ve dirençlere bakıyoruz Hacim ayak izine bakıyoruz Örneğin acsel direnci geçer ise nisbeten volume düşük olsa bile VAL seviyesine hareket etme potansiyeli görünüyor

Görseller:
- G1: SHA-256 `957879c530f48eba113aede26991a6d263a164b5dbfa92e0a9bacf2f16046b2a` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-4cb3f002-de66-4e51-b3f5-0a9f30e3a0f0.png` · beyinde VAR: `assets/tweet-acsel-direnc-kirilimi-volume-profile-val/01-acsel-direnc-volume-profile-val.png`

Beyin notu: `tweet-acsel-direnc-kirilimi-volume-profile-val.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R025 · 2026-08-27 18:02 UTC · Tweezer Bottom Talep Bölgesi Tarama ve Backtest Planı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şu tweezer bottom mumunu yazayım taramasını da yapayım buradan da getirisine bakarız. Bu formasyon talep bölgesinde şahane fırsatlar sunuyor.

Beyin notu: `tweet-tweezer-bottom-talep-bolgesi-backtest.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı)

### R026 · 2026-08-27 18:05 UTC · Volatilite Şok Rejimi ve Yeni Alım Freni · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bir bakış açısı paylaşayım Sabit hareketli ortalamalar ani piyasa paniklerinde yavaş kalır ve size hatalı alım  satım yaptırabilir. Bunu önlemek için sisteminize bir dalgalanma filtresi ekleyebilirsiniz. Şöyleki  Hisselerin son X günlük dalgalanmasını son 1 aylık dalgalanmasıyla kıyaslayin. Kısa vadeli dalgalanma aniden fırlarsa algoritmayı Piyasa Şoku moduna geçirir. Yeni al sinyallerini tamamen durdur ve sadece elinizdeki mevcut hisseleri kendi içinde yeniden dengeler.  Kisaca piyasa aniden kontrolden çıkıp aşırı dalgalanmaya başlarsa; yeni alım yapmayı kesin, bıçak tutmaya çalışmayın ve sadece elinizdeki riski yönetin.

Beyin notu: `tweet-volatilite-piyasa-soku-yeni-alim-freni.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.06; düşük skorlar elle doğrulandı)

### R027 · 2026-08-27 18:08 UTC · Talep Bölgesinden Tepki ve Hacim-Momentum Confluence Görseli · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bu kardeş bas basbağırmış talep bölgesinde ben geliyorum diye. Volume ayak izinden de belli

Görseller:
- G1: SHA-256 `1add441ea4e6a2ad0351d786222ca62c6f658a34e1c86c6780f51cc453b80bb9` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-cb61dadf-9786-418e-ae75-177e151f17b8.jpg` · beyinde VAR: `assets/tweet-talep-bolgesi-volume-profile-momentum-confluence/01-talep-bolgesi-volume-profile-momentum.jpg`

Beyin notu: `tweet-talep-bolgesi-volume-profile-momentum-confluence.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R028 · 2026-08-27 18:11 UTC · Varyans Risk Primi ve Model-Free Varyans Kesişim Projesi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Alın proje fikri Risk premium varyans ile modelden bağımsız varyans replikasyonu modelini yazın, risk premium varyans modelinde gerçek IV kullanın, sonr bu iki kodun kesşim kümesi sizin volatlite kaynaklı kazanç kapınız olur. Şöyleki  İlk kod ile sessiz ama patlamaya yakın hisseler bulunur, ikinci kod ile de IV değerine göre +- yönde öıktıda gösterilen oranda hareket yapacak hisseler çıkar. Kesişim kümesi yatırım noktasıdır. Detaylı analtacağım

Beyin notu: `tweet-varyans-risk-primi-model-free-kesisim.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R029 · 2026-08-27 18:13 UTC · TSLA Yüzde 10,4 Implied Move Görsel Paketi 04 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Unutmayın, %10.4 Implied Move opsiyon tüccarlarının, hissenin önümüzdeki vadeye kadar yaklaşık 42 USD (410'un -hisse fiyatının- %10.4'ü) hareket etmesini beklediğini gösterir. Yani piyasa, fiyatın kabaca 368 USD ile 452 USD arasında çok sert bir hareket yapmasını fiyatlıyor.

Görseller:
- G1: SHA-256 `5712af623d79922145c528a5a67bf911eb69a6d9a812db2006896793fafd0908` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-1f38436e-f576-4fb8-8e26-762a080fcade.png` · beyinde VAR: `assets/gorsel-paket-04-tsla-implied-move/01-tsla-implied-move-options-chain.png`
- G2: SHA-256 `30c9f64d2ed8afe4d1a51db0338612af1cf035cb1a0c61ea789024aef42ac73b` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-100c880e-08af-4e1d-bb1d-158033a149c5.png` · beyinde VAR: `assets/gorsel-paket-04-tsla-implied-move/02-directional-move-example.png`

Beyin notu: `gorsel-paket-04-tsla-implied-move.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R030 · 2026-08-27 18:16 UTC · Volatilite Harvesti Sabit Ağırlık Yeniden Dengeleme Projesi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Alın size proje konusu Ters korelasyona sahip iki varlığı belirli bir oranda sabit tutarak aktif yönetmenin, piyasanın doğal çalkantılarını bir getiri motoruna çevirdiğini matematiksel olarak kanıtlayacağız. Buna volatilite harvesti adını verdim. Getirilerini de ispatlayacağım

Beyin notu: `tweet-volatilite-harvesti-sabit-agirlik-rebalancing.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı)

### R031 · 2026-08-27 18:19 UTC · BIST VRP Scanner ve VOL AL-SAT Mantığı Görsel Paketi 05 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> RV (Gerçekleşen Volatilite): Hissenin son dönemde gerçekte ne kadar sert hareket ettiği.   IV (Beklenen Volatilite): Piyasanın gelecekteki risk beklentisi ve opsiyonlara biçtiği fiyatTIR.  VRP (Risk Primi - Fırsat): Aradaki farktır (IV - RV).   Büyük oranda karlı işlemler aşağıda  VOL SAT (VRP Yüksek)  Piyasa Durumu: Piyasada aşırı panik (dip) veya aşırı coşku (tepe) yaşanıyor. Beklentiler fazlasıyla şişmiş.  Ne Yapmalı?: Mevcut trendin gücünü kaybedip yataya sarması veya tersine dönmesi (reversal) beklenir  VOL AL (VRP Negatif )  Piyasa Durumu: Fırtına öncesi sessizlik. Piyasa uyuyor ve hissede bir şey olmayacağını varsayıyor, ancak hisse ciddi bir enerji biriktiriyor. Ne Yapmalı?: Yakın zamanda çok sert ve büyük bir trend hareketinin (kırılım) başlaması muhtemel

Görseller:
- G1: SHA-256 `65d5ad832b55378fea6613ebed49365dc871c3ee2dca6e65b714a87a9f0ce246` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-5767bce5-98c3-42bb-9ddf-fe0a3851f9d4.png` · beyinde VAR: `assets/gorsel-paket-05-bist-vrp-scanner/01-bist-vrp-scanner-dashboard.png`

Beyin notu: `gorsel-paket-05-bist-vrp-scanner.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R032 · 2026-08-27 18:23 UTC · Sektör Getiri Liderleri 30-60-90 Gün Görsel Paketi 06 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> (metin yok; yalnız görsel)

Görseller:
- G1: SHA-256 `2d31fcc226d235530e008c6fb794d5866339fa9e0dcf0d2a36594d2ecddf826c` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-76c4e66e-1fe4-46ef-9d65-f5f1cc699f65.png` · beyinde VAR: `assets/gorsel-paket-06-sektor-getiri-liderleri/01-sektor-liderleri-30-60-90-gun.png`

Beyin notu: `gorsel-paket-06-sektor-getiri-liderleri.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R033 · 2026-08-27 18:25 UTC · Sektör Getirisinde Anomali Temizleme ve Hesap Tutarlılığı Görsel Paketi 07 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Sektör rotasyonu yaparken anomalileri çıkarmaz iseniz sizi yanıltır. O yüzden mutlaka listenizi gözden geçirin, sektör bazında da bakın neler oluyor neler bitiyor.

Görseller:
- G1: SHA-256 `6da23025338941da1628ab1d2429fe2c9086ef0659d3c11d55357ba3ab67a7d8` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-25b86cd7-f857-4b78-a05e-da5538a63cf6.png` · beyinde VAR: `assets/gorsel-paket-07-sektor-anomali-temizleme/01-dayanikli-tuketim-anomali-temizleme.png`

Beyin notu: `gorsel-paket-07-sektor-anomali-temizleme.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R034 · 2026-08-27 18:29 UTC · Rolling Cointegration ile İlişki Bozulma Kapısı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Herkes cointegration bakmak istiyor ama çok azı rolling cointegration ile zamanla bozulmayı önlüyor. Dikkat edin

Beyin notu: `tweet-rolling-cointegration-iliski-bozulma-kapisi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı)

### R035 · 2026-08-27 18:32 UTC · Fiili Dolaşım Oranı Lookup ve Değişken Eşik Görsel Paketi 08 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şöyle bir de detay vereyim İstenilen hissenin fiili dolaşım oranı görülebilir  Eşik değer değiştirilebilir

Görseller:
- G1: SHA-256 `b06d864b50a639db9ed118c48eb67ba0ef3d24e3961c8cce88e7a14ce9234187` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-5bb67eae-924e-4fc2-993b-e7d72e2e3ecc.png` · beyinde VAR: `assets/gorsel-paket-08-fiili-dolasim-orani/01-fiili-dolasim-orani-esik-tablosu.png`

Beyin notu: `gorsel-paket-08-fiili-dolasim-orani.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R036 · 2026-08-27 18:35 UTC · Fiyat Hacim ve Fiili Dolaşım Üçlü Piyasa Modeli · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Yaklaşık 1994'den beri piyasayı takip ederim. Aralıklarım çok olmuştur, Piyasalara girip çıkmışımdır ama bu süre zarfında uzaktanda da olsa hep takip ettim. Bir doğru asla şaşmaz. Fiyat ve hacim, resmin yalnızca üçte ikisidir, fiilen işlem gören hisse sayısı ise resmi tamamlar.

Beyin notu: `tweet-fiyat-hacim-fiili-dolasim-ucgeni.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı)

### R037 · 2026-08-27 18:37 UTC · Distal ve Proximal Çizgiler ile Arz-Talep Bölgesi Taraması Görsel Paketi 09 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Distal line ve proximal line'ı kavrarsak bu işişn %50'si biter, kalan %50'si de taramasını anlayabilmek

Görseller:
- G1: SHA-256 `072de86ba99752fdbd807ec851fed2fdf0d942f4e7e3a0801955173c183daee5` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-4b2af6ab-ba55-4cf5-a42d-a75388e1c17a.png` · beyinde VAR: `assets/gorsel-paket-09-distal-proximal/01-distal-proximal-arz-bolgesi.png`

Beyin notu: `gorsel-paket-09-distal-proximal-arz-talep.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R038 · 2026-08-27 18:41 UTC · HKTM Demand-Supply Bölgesi ve Teyit Katmanları Görsel Paketi 10 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Al çalış

Görseller:
- G1: SHA-256 `1a797d5f16a92e3b84478c474e1f14fd530a0e91e26b02ec0f370221d6b2b7d6` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-2840bed9-bfc1-41b6-b519-a7e7ec0d7854.png` · beyinde VAR: `assets/gorsel-paket-10-hktm-demand-supply/01-hktm-demand-supply-analizi.png`

Beyin notu: `gorsel-paket-10-hktm-demand-supply.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R039 · 2026-08-27 18:44 UTC · Trend Çizgisi Motoru Swing Pivot ve Regresyon Zarf · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Algoritmic traderlar Trade çizgisini nasıl kodlarız?  1: Swing Pivot Eşleştirmesi. Bu yöntem, bir trader'ın grafiğe bakıp kendi gözüyle destek veya direnç çizmesinin doğrudan koda dökülmüş halidir. Algoritma grafikteki bariz dip veya tepe noktalarını tespit eder ve  bunları ikili çiftler halinde birbirine bağlar. Buradaki en katı kural, çizilen doğrunun aradaki hiçbir mum tarafından delinip geçilmemiş olmasıdır. Çizgi geleceğe uzatılır; fiyat buna her dokunup döndüğünde çizgi güçlenir, mum kapanışıyla aştığında ise trend kırılmış olur. &#x20;
>
>
>
> İnsan psikolojisini yansıttığı ve kodun kontrolü tamamen bizde olduğu için asıl kullanmamız gereken yöntemdir.
>
> 2. Yöntem: Regresyon ve Zarf: Bu yöntem geçmişteki psikolojik tepki noktalarını aramak yerine, belirli bir zaman aralığındaki veriye zorla istatistikselbir doğru oturtmaya çalışır. Algoritma, seçilen periyottaki fiyatların tam ortasından geçen bir regresyon çizgisi  hesaplar. Ardından bu çizgiyi tüm mumları içine alacak şekilde en üst veya en alt seviyelere kaydırıp eğimini optimize ederek bir zarf  oluşturur.  Ancak hazır kütüphanelerin kara kutusu içinde çalıştığı için müdahale etmesi zordur.   Ben hangisini kullanıyorum biliyor musunuz:) &#x20;

Beyin notu: `tweet-trend-cizgisi-swing-pivot-regresyon-zarf.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı)

### R040 · 2026-08-27 18:47 UTC · Confluence Alanlarında Bağımsız Kanıt Yoğunluğu · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Confluence alanları neden her zaman daha güvenlidir? Çünkü Confluence, birden fazla bağımsız teknik faktörün aynı fiyat seviyesinde buluşması anlamına gelir.

Beyin notu: `tweet-confluence-bagimsiz-kanit-yogunlugu.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R041 · 2026-08-27 18:50 UTC · FROTO BOS ve CHoCH Market Structure Görsel Paketi 11 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Not edelim, lazim olur BOS (Break of Structure): Trendin aynı yönde devam ettiğini gösterir. Yükseliş trendinde fiyatın bir önceki tepeyi yukarı kırmasıdır. Düşüş trendinde fiyatın bir önceki dibi aşağı kırmasıdır.  CHoCH (Change of Character): Trendin yön değiştirdiğini gösteren ilk erken ve güçlü sinyaldir. Fiyat sürekli yükselirken, aniden geri çekilip en son yaptığı dibin (Higher Low) altına düştüğünde oluşur. Görselin tam ortasında "CHoCH" yazan yerde bunu net görebilirsiniz.

Görseller:
- G1: SHA-256 `674fa6a387fb67dbd9e68137860a7c9830c4dbb01624da0f1eede2169a3c604b` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-bb901e52-96d5-4407-92a0-f60a7c2a61e1.png` · beyinde VAR: `assets/gorsel-paket-11-froto-bos-choch/01-froto-bos-choch-market-structure.png`

Beyin notu: `gorsel-paket-11-froto-bos-choch.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R042 · 2026-08-27 18:53 UTC · DOAS Advance Block ve Supply Zone Görsel Paketi 12 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Advance Block  formasyonu, yükseliş trendinin sonlarında ortaya çıkan ve alıcıların gücünün tükenmeye başladığını gösteren düşüş yönlü bir yorulma sinyalidir.  Kısaca art arda gelen 3 yeşil (yükseliş) mumundan oluşur, ancak bu mumların karakteristik bir yapısı vardır.  Gövdeler Küçülür, İlk yeşil mumun gövdesi büyüktür. İkinci ve üçüncü mumların gövdeleri giderek küçülür. Üst Fitiller Uzar, İkinci ve özellikle üçüncü mumun üst fitili çok uzundur. Açılışlar, Her yeni mum, bir önceki mumun gövdesinin içinden açılır.  Ne Anlama Gelir? Fiyat yukarı gitmeye çalışmaktadır ancak her yeni denemede alıcılar (boğalar) takatsiz kalır. Uzayan üst fitiller, fiyat yukarı çıktıkça satıcıların agresif şekilde devreye girip fiyatı aşağı bastırdığını gösterir.  Kaydedin lazım olur

Görseller:
- G1: SHA-256 `6afcf75186bea3ab9f99bc3fed6640fdf8f56d387af54273d08d0e28b8a1c39d` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-995c45ad-2e54-490c-a0ad-5a3d5f7e1405.png` · beyinde VAR: `assets/gorsel-paket-12-doas-advance-block/01-doas-advance-block-supply-zone.png`

Beyin notu: `gorsel-paket-12-doas-advance-block.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R043 · 2026-08-27 18:57 UTC · TTKOM Demand Zone Invalidation ve Kutu Bitişi Görsel Paketi 13 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Patlayan demand bölgesini nasıl kodluyorum? Demand bölgesinin en dip fiyatını referans noktası olarak al.  Bölgenin oluştuğu günden sonraki tüm mumların verisini sırayla taramaya başla.  Sonraki günlerde gelen mumlardan herhangi birinin Kapanış fiyatı (daha katı bir SMC kuralı isteniyorsa iğne ucu yani En Düşük/Low fiyatı) referans aldığımız dip sınırın (zone\_low) altına inmiş mi diye kontrol et (Close < zone\_low).  Fiyatın bu sınırın altına sarktığı ilk günü kırılım tarihi olarak kaydet. Grafiği çizerken demand kutusunu grafiğin en sağına kadar uzatmak yerine, tam bu kırılımın yaşandığı tarihte bitir.

Görseller:
- G1: SHA-256 `84445be2f716c5a997d0c8bb40ffd6445c37fb9934760fd834cf686ee147501c` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-a3875034-53a7-4c0b-9466-f3131f02c246.png` · beyinde VAR: `assets/gorsel-paket-13-ttkom-demand-invalidation/01-ttkom-demand-zone-break-clipping.png`

Beyin notu: `gorsel-paket-13-ttkom-demand-invalidation.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R044 · 2026-08-27 19:01 UTC · CME Group Volatilite Opsiyon Veri ve Araçları Araştırması · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> [cmegroup.com](https://t.co/1qaDeZ0sf4) Bu siteyib iraz araştırın Detaylar şinize yarar.

Beyin notu: `kaynak-cme-group-volatilite-opsiyon-veri-araclari.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.08; düşük skorlar elle doğrulandı)

### R045 · 2026-08-27 19:09 UTC · Gordon Büyüme Modeli ile Temettü Değerlemesi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Gordon Büyüme Modelini öğrenciler iyi bilir piyasada olanlar ise pek kullanmaz. Bir hisse senedinin bugünkü değerini, kâr paylarının gelecekte sabit bir oranda büyüyeceği varsayımıyla hesaplayan bir değerleme yöntemidir. Örneğin, mevcut temettü miktarı 100tl, beklenen getiri oranı %10 ve büyüme oranı %5 diyelim.  PV=100\*(1.05) / 0.10 - 0.05  Hisse değeri = 2100tl bulunur.  Bilmekte fayda var.

Beyin notu: `tweet-gordon-buyume-modeli-temettu-degerleme.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı)

### R046 · 2026-08-27 19:12 UTC · İşletme Analizi Operasyonel Finansal ve Değerleme Çerçevesi Görsel Paketi 14 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Analiz nasıl yapılır  Operasyonel Faktörler: Şirketin günlük faaliyetlerini ve iş modelini etkileyen endüstri yapısı, sunulan ürün, hedef pazar, dağıtım kanalları ve mevsimsellik/konjonktür gibi temel unsurları içerir.  Finansal Faktörler: Şirketin mali sağlığını ve parasal performansını gösteren büyüklük (gelir, varlık, piyasa değeri), kaldıraç oranı, kar marjları, temettü verimi, büyüme potansiyeli ve ortaklık yapısı gibi metrikleri kapsar.

Görseller:
- G1: SHA-256 `6ac534d823492627b216b752610124bc3c40b0f833f8c3b7363a815801d3ad76` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-0638cf53-2094-4cc3-94a3-fe27e1aecaca.png` · beyinde VAR: `assets/gorsel-paket-14-isletme-analizi-kriterleri/01-isletme-analizi-operasyonel-finansal.png`

Beyin notu: `gorsel-paket-14-isletme-analizi-kriterleri.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R047 · 2026-08-27 19:16 UTC · Rally-Base-Rally RBR Demand Zone Görsel Paketi 15 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> (metin yok; yalnız görsel)

Görseller:
- G1: SHA-256 `5d28bd24216ff4f68431d57d847b004f910afd0b683062e462959fbb64402163` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-c6ea4585-cd2f-49bb-89b2-b30dde857b5d.png` · beyinde VAR: `assets/gorsel-paket-15-rbr-demand-zone/01-rally-base-rally-rbr-pattern.png`

Beyin notu: `gorsel-paket-15-rbr-demand-zone.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R048 · 2026-08-27 19:20 UTC · Relatif Değerleme Piyasa Norm Bantları ve Çoklu Çarpan Teyidi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bu alt üst sınır piyasanın kabul ettiği normlarda olacak. Üste olanlar piyasaya göre ucuz şirketlerdir alttakilerde pahalı kalmış. Bir nevi rölatif değerleme yapıyor olacaksınız. Sonra, efendime söyleyeyim, bunu farklı rasyolar ya da çarpanlar ile teyit edeceksiniz. Alın strateji

Beyin notu: `tweet-relatif-degerleme-piyasa-norm-bantlari.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.07; düşük skorlar elle doğrulandı)

### R049 · 2026-08-27 19:23 UTC · Temel-Momentum Ters Faz Quant Stratejisi Görsel Paketi 16 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Yeni bir quatn stratejinin ayak sesleri Temel ve momentum staratejisi beraber çalışacak Ekranda mavi çizgi  xxxx kırmızı ise fiyat bir altta iken diğeri kesin üste diğeri üste iken öteki kesin altta:)

Görseller:
- G1: SHA-256 `9a220e79cea8745253db065e9a5e2dfddba737dd7fd123c962feb1d934b36a21` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-87c88acd-7394-4f60-b48c-1d9e1ef934ec.png` · beyinde VAR: `assets/gorsel-paket-16-temel-momentum-ters-faz/01-temel-metrik-fiyat-ters-faz.png`

Beyin notu: `gorsel-paket-16-temel-momentum-ters-faz.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R050 · 2026-08-27 19:27 UTC · Candle Imbalance Güç Sıralaması Görsel Paketi 17 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> (metin yok; yalnız görsel)

Görseller:
- G1: SHA-256 `ee719eebc53bb8d3c4ace39e489a4abe2cc744cf50f3e572b5c79f3b04c6c446` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-3963cb3e-2abe-438f-af01-5381a83bfee4.jpg` · beyinde VAR: `assets/gorsel-paket-17-imbalance-gucu/01-bullish-imbalance-strength-ranking.jpg`

Beyin notu: `gorsel-paket-17-imbalance-gucu.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R051 · 2026-08-27 19:31 UTC · Konsolidasyon Bölgesi Gövde ve Gölge Sınırları Görsel Paketi 18 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Hap bilgi Konsolidasyon bölgesi için En yüksek mumun gövdesinin bittiği yer ile, en düşük mumun gölgesinin bittiği yer. Deneyin sizde paylaşın.

Görseller:
- G1: SHA-256 `8e3764af6dcfd856ef08850317d9c658ceebfa31156992efe80b024fdf288dc2` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-af1f84f7-5412-4230-8357-c0cacea85cef.jpg` · beyinde VAR: `assets/gorsel-paket-18-konsolidasyon-body-wick/01-konsolidasyon-body-wick-bolge.jpg`

Beyin notu: `gorsel-paket-18-konsolidasyon-body-wick.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R052 · 2026-08-27 19:36 UTC · EURTRY Forward ve Monte Carlo Pazarlık Çerçevesi Görsel Paketi 19 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> 2024 sonunda bir çalışma yapmışım şirket için 1 yıl sonra eur/try 57.61 olur, banka bize bu rakama göre forward kur vermek ister ona göre pazarlık yapalım demişim Sonuç ortada Bankaya golü attık.

Görseller:
- G1: SHA-256 `07358a6a9e1b7425876f4bc798b55e2463021ab69176d20f72e4744337c2d95d` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-c7d58941-6e85-43e1-92b3-16015bf56036.jpg` · beyinde VAR: `assets/gorsel-paket-19-eurtry-forward-monte-carlo/01-kur-grafigi-usdtry-etiketli.jpg`
- G2: SHA-256 `677b02b44df7f9c2532bc602bc05bbbe713704506b97f655686a74294f8ca354` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-5e9cfd45-54ca-40f1-bed1-e6173126876a.png` · beyinde VAR: `assets/gorsel-paket-19-eurtry-forward-monte-carlo/02-forward-monte-carlo-ciktisi.png`

Beyin notu: `gorsel-paket-19-eurtry-forward-monte-carlo.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R053 · 2026-08-27 19:40 UTC · Bollinger Kuyrukları Ortalama Dönüş ve VaR Risk Çerçevesi · https://x.com/The_Tansu_/status/2087267070752760121

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Her yerde bunun ne olduğunu öğrenebilrisiniz Peki hisse yatırımında nasıl kullanacağız? Buyurunuz...  Bollinger Bantlarında alt ve üst bantlar genelde +-2 standart sapmayı temsil eder ve fiyatların %95'inin bu sınırlar içinde kalması beklenir. Fiyatın bu bantların dışına çıkması aşırı alım veya aşırı satım bölgesine girildiğini gösterir. Kuyrukları bu yüzden takip ederiz  Bantların genişliği hissenin ne kadar riskli ve oynak olduğunu ortaya koyar. Sapmanın büyüklüğü, beklenen getirideki belirsizliği ölçmek için kullanılır.  Fiyatın -2SE veya -3SE seviyesine inmesi istatistiksel olarak nadir bir durumdur. Bu seviyeler, fiyatın tekrar ortalamaya döneceği beklentisiyle tepki alımı fırsatı olarak değerlendirilebilir. (Ortalamaya Dönüş)  \
> [**Tansu**](https://x.com/The_Tansu_)
> [@The\_Tansu\_](https://x.com/The_Tansu_)
> [11 Ağu](https://x.com/The_Tansu_/status/2087267070752760121)
> Portföyün belirli bir güven düzeyinde (örneğin %95) uğrayabileceği maksimum kaybı hesaplamaya yarar. Olası en kötü senaryolara karşı risk limitleri koymanızı sağlar. (VaR)

Görseller:
- G1: SHA-256 `d7063621240b9fa21534cee001a5fabf53fa37b8da2967846076f1aeed41fcc1` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-8c204668-d358-4862-acad-616827ce14b7.png` · beyinde VAR: `assets/tweet-2087267070752760121/01-normal-dagilim-se-68-95-997.png`

Beyin notu: `tweet-bollinger-kuyruklari-ortalama-donus-var.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R054 · 2026-08-27 19:44 UTC · Bullish ve Bearish Sponsor Candle Görsel Paketi 20 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Biraz teori dağarcığımızı dolduralım  Sponsor Candle teknik analizde büyük kurumsal yatırımcıların piyasa yönünü değiştirmek için yüklü miktarda işlem açtığı kritik mumdur. Kısacası akıllı paranın piyasada bıraktığı ayak izidir.  Bullish Sponsor Candle: Sert bir yükseliş hareketi başlamadan hemen önceki son düşüş mumudur. Fiyatın ileride bu bölgeye gerilediğinde buradan alıcı bulup tekrar yükselmesi beklenir.  Bearish Sponsor Candle: Sert bir düşüş hareketi başlamadan hemen önceki son yükseliş mumudur. Fiyatın ileride bu bölgeye tekrar çıktığında satıcılarla karşılaşıp düşmesi beklenir.

Görseller:
- G1: SHA-256 `d8eb53a1b495c40efabd737014b8e14468e5e27c4af789e066e14c2da8066b64` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-7e1a17a3-50ec-4b73-86cc-4ec3922c2b1d.png` · beyinde VAR: `assets/gorsel-paket-20-sponsor-candle/01-bullish-bearish-sponsor-candle.png`

Beyin notu: `gorsel-paket-20-sponsor-candle.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R055 · 2026-08-27 19:48 UTC · Swing Point Talep Bölgesi ve HSAR Confluence Alan Taraması Görsel Paketi 21 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şu confluence alanları o kadar kıymetli ki, aslında grafiklerde bunları arayıp taratmak lazım. Her seferinde zenginlik yaratmışlar.

Görseller:
- G1: SHA-256 `a57c49f9859202b42d5a019f77f3c0d7d69296a4aee939b46e4a8c5014f84bee` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-668d05d7-04c0-4558-adaa-327cc353489e.png` · beyinde VAR: `assets/gorsel-paket-21-confluence-alan-taramasi/01-gcf-swing-demand-hsar-confluence.png`

Beyin notu: `gorsel-paket-21-confluence-alan-taramasi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R056 · 2026-08-27 19:52 UTC · Hisse Senedi Analiz ve Karar Destek Pipeline Görsel Paketi 22 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> gibi gibi

Görseller:
- G1: SHA-256 `2e66a503c1f91859e31629c10bb764fd99323f83558370f94307cc939b45326f` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-d46bcc9f-0aee-4695-9135-c0593df07158.jpg` · beyinde VAR: `assets/gorsel-paket-22-hisse-karar-destek-pipeline/01-hisse-analiz-karar-destek-sureci.jpg`

Beyin notu: `gorsel-paket-22-hisse-karar-destek-pipeline.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R057 · 2026-08-27 19:56 UTC · Özkaynak Artışı Varlık Kompozisyonu ve Yatırım Verimliliği · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Öz kaynağın artışının en önemli sebebi bir şirketin net kar elde etmesi idi. Dönen ve duran varlıkların içindeki ağırlıklara bakin, borcun, toplam borcun içinde % kaç öz kaynaklardan oluşuyor önemlidir. İşletmelerin yaptığı yatırımlarda özkaynağını ne kadar arttırıyor inceleyin.

Beyin notu: `tweet-ozkaynak-artisi-varlik-finansman-yatirim-verimliligi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.10; düşük skorlar elle doğrulandı)

### R058 · 2026-08-27 20:02 UTC · Regresyon ve ML ile Rasyolardan Piyasa Değeri Sapması · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Çok gelen bir soru   Regresyon veya makine öğrenmesi modelleri ile hisse fiyatı modellenmez, şirketin rasyolarına göre "olması gereken piyasa değeri" tahmin edilir. Mevcut piyasa fiyatı ile modelin öngördüğü değer arasındaki sapma optimize edilir.  Ml modelleri sıkıntılıdır

Beyin notu: `tweet-regresyon-ml-rasyolardan-piyasa-degeri-sapmasi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı)

### R059 · 2026-08-27 20:06 UTC · FROTO Maddi Duran Varlık Artışı ve Fiyat İlişkisi Görsel Paketi 23 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şimdi ben size bir dip not daha vereyim Bilançolarda maddi duran varlık artışları er ya da geç (insider yoksa) fiyata yansır. Aradaki korelasyon çok kuvvetlidir. Göz ardı etmeyin

Görseller:
- G1: SHA-256 `3f588fac84a70d260fde9e1588a71e850b5eb4054cbda3f25ade88c629c47447` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-c3457f16-ee6e-4bab-b55d-316387c5a039.png` · beyinde VAR: `assets/gorsel-paket-23-froto-ppe-fiyat/01-froto-maddi-duran-varlik-fiyat.png`

Beyin notu: `gorsel-paket-23-froto-ppe-fiyat.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R060 · 2026-08-27 20:12 UTC · Cari Oran Likidite Açığı ve Bedelli Sermaye Artırımı Riski · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Dönen varlıkları KVB’larından yüksek değilse o firma 1 yıl içerisinde nakde ihtiyaç duyacaktır ve yeniden bir borca gidecek ya da bedelli sermaye arttırımına gitmesi icap eder. Dolayısı ile bir firmanın bedelli sermaye arttırımına gidip gitmeyeceğini de buradan anlayabiliriz.

Beyin notu: `tweet-cari-oran-likidite-acigi-bedelli-sermaye-artirimi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.09; düşük skorlar elle doğrulandı)

### R061 · 2026-08-27 20:16 UTC · Merton Modeli Distance to Default EDF ve Kredi Spread Görsel Paketi 24 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bir kaç gün önce bir kurumsala yaptığım bir çalışmanın değerlerini değiştirerek size de anlatayım. İleri seviye modellemedir ama bilmenizde fayda var. Merton Modeli  A0 = firmanın toplam varlıklarının bugünkü değeri (100) σA = bu varlıkların ne kadar dalgalı/riskli olduğu (%25) D = firmanın vadesi gelince ödemesi gereken borç (80) r = risksiz faiz oranı (%5) T = borcun vadesine kaç yıl kaldığı (1 yıl)  Çıktılar   D0 (74.6) → bu borcun bugünkü gerçek değeri (risk yüzünden nominal 80'den daha düşük) E / Equity (25.4) → hissedarlara kalan pay = Varlık - Borç Spread (%2) → firmanın, risksiz orana göre ne kadar fazla faizle borçlanabildiği (risk primi)  DD (0.97) → varlık değerinin, borcunu ödeyemez hale gelmeden önce ne kadar "tampon"u olduğu (ne kadar yüksekse o kadar güvenli) EDF (%17) → firmanın 1 yıl içinde borcunu ödeyemez duruma düşme olasılığı  Girdi olarak "şirket ne kadar varlığa, ne kadar borca sahip, ne kadar riskli" veriyoruz; çıktı olarak "bu şirket batabilir mi, ne kadar ihtimalle, hisse değeri ne olmalı" öğreniyoruz.  Sonuç: DD=0.97, EDF=%17  Firma yüksek borçlu ve kırılgan. Varlık değeri sadece 1 standart sapma düşse borcunu ödeyemez hale gelir. %17 temerrüt ihtimali, yatırım yapılabilir seviyenin çok altında — spekülatif/riskli kredi profili.  Bu hisseye girmeden önce kaldıracı ve nakit akışını mutlaka kontrol et, ucuz görünse bile temkinli yaklaşmak lazım. Temerrüt önemli artık daha çok bakmak lazım.

Görseller:
- G1: SHA-256 `1699c932e296e849e92dcdd86bf813c2d4d664156952e4000078ec6967d813a7` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-b711c944-6bf9-4654-a3c1-391fb3fc882b.jpg` · beyinde VAR: `assets/gorsel-paket-24-merton-modeli/01-merton-distance-to-default-edf.jpg`

Beyin notu: `gorsel-paket-24-merton-modeli.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R062 · 2026-08-27 20:22 UTC · ASUZU F/K PD/DD ve FD/FAVÖK Çoklu Değerleme Tutarlılığı · https://x.com/The_Tansu_/status/2085476092228362655

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Temel analiz ve değerlemeyi küçümsemeyin Tüm bu analizler birbiri ile entegre olacak henüz bunlar emekleme aşamaları. Çoka cayip şeyler olacak  \
> [**Tansu**](https://x.com/The_Tansu_)
> [@The\_Tansu\_](https://x.com/The_Tansu_)
> [7 Ağu](https://x.com/The_Tansu_/status/2085476092228362655)
> hepsi tutarlı

Görseller:
- G1: SHA-256 `75ba1ece027214ed25c0197816c2ed90474b15072f80826739214f4fc7c5514a` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-cdaf80fc-a005-48ff-97ca-bf4446a0540a.png` · beyinde VAR: `assets/tweet-2085476092228362655/01-asuzu-otomatik-fk-degerleme.png`
- G2: SHA-256 `0f8f6d59b751734089d982556e9859e1f3729f46527cb0f20f138df40588f14b` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-78b3ccab-0624-4739-bc74-5df7d03e2029.png` · beyinde VAR: `assets/tweet-2085476092228362655/02-asuzu-pddd-degerleme.png`
- G3: SHA-256 `f50bd56ef5558dec19e8e06b1367cf0c7eed6dbb8214e192fdbf2c3b727d14d6` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-375fc34f-20f8-4693-884a-7cb2d7760532.jpg` · beyinde VAR: `assets/tweet-2085476092228362655/03-asuzu-120-hedef-gerceklesen-grafik.jpg`
- G4: SHA-256 `5c2d9c1b39322fb1b5ce50a0e025883ac135f4ed9133394d6bf7b69c1f04db45` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-8beefb07-69c2-4220-9179-539eed48b9da.png` · beyinde VAR: `assets/tweet-2085476092228362655/04-asuzu-fk-fdfavok-ozet.png`

Beyin notu: `tweet-asuzu-coklu-degerleme-tutarliligi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R063 · 2026-08-27 20:28 UTC · TTRAK PD/DD Primi Çarpan Sıkışması ve Dağıtım İddiası · https://x.com/The_Tansu_/status/2085442890331734258

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> \
> [**Tansu**](https://x.com/The_Tansu_)
> [@The\_Tansu\_](https://x.com/The_Tansu_)
> [6 Ağu](https://x.com/The_Tansu_/status/2085442890331734258)
> [#TTRAK](https://x.com/hashtag/TTRAK?src=hashtag_click) da 900'lerden çok güzel yıktılar malı millete. 2 senedir kitlendi herkes.

Görseller:
- G1: SHA-256 `52f0a0fb93b1c7b6b0bffc17c4d06d481e6ca4b28af81de83b4d90f19542d714` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-b3c6c903-4bc7-403c-8cae-8d272ed13281.png` · beyinde VAR: `assets/tweet-2085442890331734258/01-otomotiv-pddd-son-10-donem.png`

Beyin notu: `tweet-ttrak-pddd-primi-carpan-sikismasi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R064 · 2026-08-27 20:34 UTC · A B DCF Çoklu Değerleme Birleştirme ve Ağırlıklandırma Modeli Görsel Paketi 25 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> çarpanlara göre değerlemede fk, pd/dd , fd/favök kullanacaksın her bir çarpan analizinde kısa dönem uzun dönem ve sektör ortalamasına göre fiyat bulacaksın ve ortalamasını alacaksın sonra her bir ortalamanın (3 ) ortalamasını alacaksın Ortalama fiyat senin ilk fiyatın. A olsun  Sonra yukarıda örnek verdiğim basit model ile fk ve df/favök ile değerlemeyi bulacaksın ve bu ikisinin ortalamasını alacaksın. B olsun  (A\*0.6) + (DCF \* 0.4) = Hisse fiyatın  ya da   ((A+B)\*0.6) + (DCF \* 0.4) = Hisse fiyatın  B'yi teyit için de kullanabilirsin.  Kabaca sistem bu

Görseller:
- G1: SHA-256 `5e6b7b7d63e3b67a705eb74309e8cd623ab9b5d8e9308ea4042cfe0209c3ada0` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-8f867b65-a74a-48e3-a356-3bcdb6e351ba.png` · beyinde VAR: `assets/gorsel-paket-25-degerleme-agirliklandirma/01-asuzu-manuel-fk-fdfavok-b-modeli.png`

Beyin notu: `gorsel-paket-25-degerleme-agirliklandirma.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R065 · 2026-08-27 20:39 UTC · Nihai hedef Tek bir tuş ile temel ve teknik analizin yapıldığı, değerl… · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Nihai hedef Tek bir tuş ile temel ve teknik analizin yapıldığı, değerlemenin yapıldığı, LLM ve NLP kullanılarak faaliyet raporlarından bilginin direk değerleme raporu için veri sağlayacak bir sistem. Bu bir süreç ve sürekli gelişime açık olacak.

Beyin notu: **beyinde yok** (önerilen yeni ad: `tweet-nihai-hedef-tek-tus-temel-teknik-degerleme-llm-nlp.md`)

### R066 · 2026-08-27 20:46 UTC · Beklenen F/K Çoklu Regresyon Modeli ve Güvenilirliği · https://x.com/The_Tansu_/status/2085281785374491018

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Beklenen kar ile beklenen farklı determinantların oluşturduğu bir regresyon modeli ile beklenen FK hesaplanabilir mi, güvenilirliği ne olur?  \
> [**Tansu**](https://x.com/The_Tansu_)
> [@The\_Tansu\_](https://x.com/The_Tansu_)
> [6 Ağu](https://x.com/The_Tansu_/status/2085281785374491018)
> Birden fazla regresyon modeli ile yapılacak bu çalışmada  beklenen kâr büyüme oranı, özsermaye kârlılığı (ROE), temettü ödeme oranı, risk faktörleri (beta) ve faiz oranları bağımsız değişken kabul edilerek çoklu regresyon modeliyle tahmin edilebilir.Ancak /K oranı ile büyüme/risk değişkenleri arasındaki ilişki her zaman lineer değildir. Piyasa duyarlılığı (sentiment) ve ani makro şoklar regresyon katsayılarını geçersiz kılar. Çoklu doğrusal bağlantı problemleri de çıkacaktır, bazı değişkenleri modelden çıkarmak gerekir.  Herşeye rağmen öğrenciler için güzel bir akademik çalışma niteliğindedir, geliştirici bir yönü vardır, farklı disiplinleri de araştırma ihtiyacı doğar.  Zerzavatların yorum yapması yasaktır, aklı başında yorumlar değerlendirilir.

Beyin notu: `tweet-beklenen-fk-coklu-regresyon-modeli.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R067 · 2026-08-27 20:51 UTC · Çoklu Sistem Sonuçları ve Provenance Görsel Paketi 02 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şöyle bir detay vereyim siz kırılımını yaparsınız Ben tüm sekmelerin kodunu da yazacağım tek tuş ile hazır hale getireceğim ama baya bir iş Bir noktaya kadar da geldim.

Görseller:
- G1: SHA-256 `f386ac7e1e24741ca64fbf80807cd394ad607f7743666d53113045a4f57b8620` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-4113f6dc-b179-4aa6-a4d1-d52989f1856f.png` · beyinde VAR: `assets/gorsel-paket-26-top-down-scorecard/01-adim-6-top-down-skor-karti.png`

Beyin notu: `gorsel-paket-02-coklu-sistem-provenance.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.03; düşük skorlar elle doğrulandı)

### R068 · 2026-08-27 20:58 UTC · ASUZU F/K Değerleme Referansları ve Ex-Ante Zaman Çizgisi Görsel Paketi 27 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Ben çarpan analizlerini sektör ortalaması, uzun dönem ve kısa dönem olarak alırım Birden fazla çarpan ile değerlerim ve her çarpanın döneminin ortalamasını alırım Sonra bu ortalamaların da ortalamasını alırım En sonunda bu ortalamanın %60'ını, DCF'in de %40'ını alırım.  Yukarıda FK'ya göre bir değerleme yapıldı. 2024 mart ayında gelen 2023 sonu bilançosuna göre yapılan değerlemede, Nisan ayında hisse tam da ederine ulaştı.

Görseller:
- G1: SHA-256 `7bf2670c048534b35d23fc0cf6ce424fd332a03765ff17034e4d865043ae6106` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-4f9d9922-0a74-4aef-8d20-44dfe962fb4f.png` · beyinde VAR: `assets/gorsel-paket-27-asuzu-fk-ex-ante/01-asuzu-fk-referanslari-ve-hedefler.png`
- G2: SHA-256 `035612fe3e6522f381226e1dd96bc1aa8f9240840c0b9b21bfb6a6c07ccf1afd` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-dc635224-8fe3-488b-ace8-bc6f8badfdb8.jpg` · beyinde VAR: `assets/gorsel-paket-27-asuzu-fk-ex-ante/02-asuzu-120-hedef-118-60-gerceklesen.jpg`

Beyin notu: `gorsel-paket-27-asuzu-fk-ex-ante-zaman-cizgisi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R069 · 2026-08-27 21:04 UTC · Proje Bugünkü Değeri Piyasada Fiyatlanma Boşluğu ve Teknik Kapı Görsel Paketi 28 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şöyle bir beyin fırtınası yapalım Bir firma düşünün Piyasa değeri 2 milyar tl Bu fiirma bugün bir iş alıyor ve 3 yıl sonra 1 milyar tl ciro hedefliyor Bu 1 milyar tl'nin bugünkü değeri, %20 iskonto oranı ile bugün 579 miliyon tl ediyor. Ufak bir hesap ile 579 milyon tl----->  Firmanın bugünkü değerinin %29'una denk geliyor. Yani firmaya üçte bir kadar bir değer katıyor .(Eğer piyasa bu projeyi henüz fiyatlamamış ise). tabloda farklı WACC oranlarına göre değerin bugüne iskonto edilmiş hali var. Buna bir de tekniği ekleyin olsun bitsin. Yapcağız beraber

Görseller:
- G1: SHA-256 `3b26663720264e5804a4bc31e15fc12d1487cecafc05f5620d152c827fcdd49f` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-5241a220-58a2-4668-83b2-8501fde167eb.png` · beyinde VAR: `assets/gorsel-paket-28-proje-bugunku-deger/01-proje-pv-wacc-duyarlilik.png`

Beyin notu: `gorsel-paket-28-proje-bugunku-deger-ve-teknik-kapi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R070 · 2026-08-27 21:10 UTC · Üç Yöntemle Özkaynak Maliyeti WACC ve DCF Girdileri Görsel Paketi 29 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> python ile DCF WACC hesaplamasını 3 farklı yolla yaparak ortalamasını alıyorum. Eski verilerdir. Örnek teşkil etmesi için verilmiştir.

Görseller:
- G1: SHA-256 `df38a0ece33f5f78225a74096affcef7edfce0ea649a8facb72a5b8517e3423c` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-6eb655ad-be6e-46bc-8476-4f267d4728a5.png` · beyinde VAR: `assets/gorsel-paket-29-rs-wacc-dcf/01-uc-yontem-rs-ve-wacc.png`
- G2: SHA-256 `f2c4f56d3da7235a9abed0b5d0c84d9143136dac24c61baa4a044ebfcaeafc4e` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-6337d674-bc47-4e6f-971a-fb21060e62fc.png` · beyinde VAR: `assets/gorsel-paket-29-rs-wacc-dcf/02-eregli-dcf-tarihsel-girdiler-2021-6.png`

Beyin notu: `gorsel-paket-29-uc-yontem-rs-wacc-dcf-girdileri.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R071 · 2026-08-27 21:15 UTC · FED Faiz Beklentisi Altın Fiyatlaması ve Beklenti Sürprizi Görsel Paketi 30 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Beklenti satın alınır Gözünü seveyim senin python...

Görseller:
- G1: SHA-256 `aa4849b394a0d095f51977a4585128a2cb39932120d64e324117129c46b9b1fb` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-5506dfb7-9a65-484d-bb86-9034675efccb.png` · beyinde VAR: `assets/gorsel-paket-30-fed-beklenti-altin/01-fed-beklenti-tablosu-2026-07.png`
- G2: SHA-256 `b762ac46ddcc5e9bdc3c473661f127eeb357a6b6011b14f3603fd6274701d942` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-740aa984-5824-4c8f-91ce-ce918f2ba9c1.png` · beyinde VAR: `assets/gorsel-paket-30-fed-beklenti-altin/02-fed-beklenti-altin-grafigi.png`

Beyin notu: `gorsel-paket-30-fed-beklenti-altin-fiyatlama.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R072 · 2026-08-27 21:19 UTC · Sağlıklı Trend Yapısı ve CSCO Güçlü Trend Görsel Paketi 31 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Sağlıklı trend örneği

Görseller:
- G1: SHA-256 `963f08053c0b9357d720a4b8d9256972f84a3ab7d36a05d55b7c4b46da85b9e9` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-f06a161c-e97f-4a9d-a0fd-bf716c4cda7e.jpg` · beyinde VAR: `assets/gorsel-paket-31-saglikli-trend/01-csco-guclu-trend.jpg`

Beyin notu: `gorsel-paket-31-saglikli-trend-csco.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R073 · 2026-08-27 21:22 UTC · Gartley AB=CD Talep Bölgesi Düşen Kırılımı ve Relative Strength Görsel Paketi 32 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şimdi bu kardeşimiz gartley yapmış, ABCD olmuş, bunlar talep bölgesinde kavuşmuş bir de düşeni de kırmış, eh bize de yarın otorop izlemesi kalıyor. Henüz endeksi yenecek güçte değil ama bu formasyonlar hisseyi oraya itecek umuyorum.

Görseller:
- G1: SHA-256 `0f4bcfc467072c9fef50d40c42860ea68150c6ec6071fbbca4937b628cc5045c` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-37db8e3e-6462-46bf-8d30-380eab800dd7.jpg` · beyinde VAR: `assets/gorsel-paket-32-gartley-abcd-talep-kirilim/01-gartley-abcd-talep-dusen-kirilimi.jpg`

Beyin notu: `gorsel-paket-32-gartley-abcd-talep-dusen-kirilimi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R074 · 2026-08-27 21:25 UTC · Min Volatility Max Sharpe Portföyleri DEY ve BIST100 Karşılaştırması Görsel Paketi 33 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Kirmizi noktalı çizgi BIST getirisi Ortadaki çizgiler portföyün kapanış getirisi En üsteki çizgiler ise dönem içindeki en yüksek marjlar Bence portföy üzerine düşeni yaptıve yapıyor.  Portföyün min volatiliteve maks sharpe ağırlıklandırmasına göre getiri eğrileridir.

Görseller:
- G1: SHA-256 `efa74eb89080ac24b55a6902edbbb11b96c4ec74081f78ac351ec266c50f9479` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-639d69bf-75dc-4880-b913-c6044dc9d218.jpg` · beyinde VAR: `assets/gorsel-paket-33-min-vol-max-sharpe/01-min-vol-max-sharpe-dey-bist100.jpg`

Beyin notu: `gorsel-paket-33-min-vol-max-sharpe-dey-bist100.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R075 · 2026-08-27 21:28 UTC · Siyah Kuğu Harmoniği Talep Bölgesi ve RUN Outcome Görsel Paketi 34 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Kuğuyu bir de talep toplama bölgesinde yakalarsanız böyle RUN! olur grafiğiniz.

Görseller:
- G1: SHA-256 `0414a957cd9c255248bfc96d0dd8a7d91af7cbdcba8feb143fc1951eaca9eba2` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-6f6a5bc4-7a30-40c9-b84b-2c2010606154.png` · beyinde VAR: `assets/gorsel-paket-34-siyah-kugu-talep-run/01-lider-siyah-kugu-talep-run.png`

Beyin notu: `gorsel-paket-34-siyah-kugu-talep-run.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R076 · 2026-08-27 21:31 UTC · Beyaz Kuğu SELL AB=CD Düşen Kırılımı ve Yön Çatışması Görsel Paketi 35 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Düşeni kırmış, sell yönlü abcd'yi tamamlamışi beyaz kuğu da oluşmuş, eh bunu yolculamayalım mı şimdi...

Görseller:
- G1: SHA-256 `5dbefdc016134f4ce9a6910dd845e4a59d5c4b6bda8044942fafe104bb471414` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-0a4c0b47-d0a1-494a-b720-fe14037a440d.png` · beyinde VAR: `assets/gorsel-paket-35-beyaz-kugu-abcd-conflict/01-beyaz-kugu-sell-abcd-dusen-kirilimi.png`

Beyin notu: `gorsel-paket-35-beyaz-kugu-sell-abcd-dusen-kirilimi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R077 · 2026-08-27 21:34 UTC · Volatilite Rehaveti Yön Bağımsız Kırılım ve Ok Semantiği Görsel Paketi 36 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Cızıg çizmeye gerek yok:) Kırmızı oklar illa düşeceği anlamına gelmez oynaklığı berliler. Rehavet ortamı vardır ve fiyat bir yöne kırılacaktır.

Görseller:
- G1: SHA-256 `b7127ae4e943261002e5226775f2697d92f8e997278da1c935d0878fd28a97f6` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-7b34f6ee-35a9-48e4-81e9-88c7bdcfac34.png` · beyinde VAR: `assets/gorsel-paket-36-volatilite-rehavet-kirilim/01-volatilite-rejimi-rehavet-oklari.png`

Beyin notu: `gorsel-paket-36-volatilite-rehavet-yon-bagimsiz-kirilim.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R078 · 2026-08-27 21:37 UTC · Gün Sonu Rebalancing Aktif Pasif Portföy ve İşlem Logu Görsel Paketi 37 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şu rebalancing stratejisini öğrenin derim. Her ne kadar gurpta bunu paylaşmıyorsam da aslında yapmam gerekir. Hiç bir efor sarfetmeden sadece gün sonu eklemeler eksiltmeler ile sistem getirisi 1.5 yada %27.

Görseller:
- G1: SHA-256 `cc9de9ccc862dca79da13e440af247c6568aa321614cf866af11cf6a08d8f579` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-1dd962d8-2d66-4916-be09-e55c93b0ad67.png` · beyinde VAR: `assets/gorsel-paket-37-gunluk-rebalancing/01-portfoy-kz-raporu.png`
- G2: SHA-256 `96b48872c98d3d2a7cea67c7d17ac9386738a42fd836ea76254795b6636d4bfd` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-f6308398-8ca7-4012-b3d3-f62aa7dd90e0.png` · beyinde VAR: `assets/gorsel-paket-37-gunluk-rebalancing/02-gunluk-rebalancing-islem-logu.png`

Beyin notu: `gorsel-paket-37-gunluk-rebalancing-aktif-pasif.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R079 · 2026-08-27 21:42 UTC · AKCNS Haftalık AB=CD Talep EMA ve Katılım Görsel Paketi 38 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Not alın işte süper brir yapı...

Görseller:
- G1: SHA-256 `31e055ab16b0f26a3b30f77b5a2e9ed5fd16746d8a2cc3e931feb3af4722e2b1` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-71e881c3-7558-4e8f-83cd-6af77784be30.png` · beyinde VAR: `assets/gorsel-paket-38-akcns-haftalik-abcd-talep/01-akcns-haftalik-abcd-talep-ema.png`

Beyin notu: `gorsel-paket-38-akcns-haftalik-abcd-talep-ema.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R080 · 2026-08-27 21:45 UTC · AB=CD Detector A B C D Pivot Fibo Talep ve Tepki Görsel Paketi 39 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> 4 Kritik Noktanın (A, B, C, D) Bulunması:Grafikteki peş peşe gelen lokal tepe ve dip noktaları tespit edilir. (Alış için: Yüksek tepe -> Dip -> Daha düşük tepe -> Daha düşük dip şeklinde bir "zig-zag" veya merdiven basamağı).  BC Düzeltmesinin Ölçülmesi (Fibo Oranı):Fiyatın B'den C'ye yaptığı geri dönüş (BC uzunluğu), ilk hareket olan AB uzunluğuna bölünür. Çıkan sonucun Fibonacci oranlarından (0.382, 0.50, 0.618 vb.) birine çok yakın olması (hata payı toleransı içinde) gerekir.  CD Hedefinin Ölçülmesi (Uzantı):Son dalga olan CD'nin uzunluğu, AB'nin uzunluğuna bölünür. Çıkan sonucun belirli uzatma oranlarına (1.00, 1.27, 1.618 vb.) denk gelip gelmediğine bakılır.  En Kısa Özet: Fiyatın "N" veya "Ters N" harfi çizerken oluşturduğu dalga boylarının, birbirine rastgele değil, belirli Fibonacci oranlarıyla (özellikle AB uzunluğu = CD uzunluğu) simetrik olarak uymasıdır.  D noktasına bakın, talep toplama bölgesine bakın, hissenin tepkilerine bakın. Doğru kod böyle yazılır.

Görseller:
- G1: SHA-256 `7199e592be5cfd2b74bf6148f5c7cc3e76555ea1185142dd5902f612dd3e8008` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-e44aa1a3-4a9f-4802-a273-11473d49049b.png` · beyinde VAR: `assets/gorsel-paket-39-abcd-detector/01-abcd-sell-fibo-talep-tepki.png`

Beyin notu: `gorsel-paket-39-abcd-detector-fibo-talep-tepki.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R081 · 2026-08-27 21:49 UTC · Haftalık BUY AB=CD D Noktası Talep Tepkisi Görsel Paketi 40 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bak hocam ABCD yi görüyor musun tam talep toplama bölgesinden haftalıkta tepkisini almış kütür kütür gitmiş. İşte bu yapıların peşindeyiz.

Görseller:
- G1: SHA-256 `589a448877fc464b9bc99182bb2fea814f082a47b67e4d323e7161a138d5bd1f` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-3f9c2282-b00c-47eb-bfb5-ecf39d205d19.png` · beyinde VAR: `assets/gorsel-paket-40-haftalik-abcd-talep-tepki/01-haftalik-abcd-d-talep-tepki.png`

Beyin notu: `gorsel-paket-40-haftalik-abcd-talep-tepki.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R082 · 2026-08-27 21:52 UTC · Konsolidasyon Süresi Ok Alanı ve Kırılım Şiddeti Görsel Paketi 41 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Ok'lara dikakt edelim. Okların içinde bulunduğu alan ne kadar geniş ise yani konoslidasyon ne kadar uzarsa kırılım o denli şiddetli oluyor. Burada bu kadar kısa konsolidasyonda bu kırılım şiddeti beni de şaşırttı.

Görseller:
- G1: SHA-256 `c4efc78c73da76d5516612987444abf13aa80daecb058342e501b707e073343e` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-24a615f2-c909-4d66-a1ce-7f46ae70a173.png` · beyinde VAR: `assets/gorsel-paket-41-konsolidasyon-suresi-kirilim/01-ok-konsolidasyon-suresi-kirilim-siddeti.png`

Beyin notu: `gorsel-paket-41-konsolidasyon-suresi-kirilim-siddeti.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R083 · 2026-08-27 21:55 UTC · Fiili Dolaşım Oranı Lookup ve Değişken Eşik Görsel Paketi 08 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> iili dolaşımdaki pay ile ilgili herkes birşeyler yazıyor, önemli olan onun taramasını yapmakta :) Dolaşımdaki pay adedinin <%30 olduğu senetler ile ilgili çok tatlı stratejik taramalar gerçekleştirilebilir.  KAP ile verileri alabiliyoruz, sırada taramalar var. Saygılar...

Beyin notu: `gorsel-paket-08-fiili-dolasim-orani.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R084 · 2026-08-27 21:58 UTC · BUY AB=CD D Noktası Yükselen Destek ve Hedefler Görsel Paketi 42 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şimdi ne diyeyim yani buna:)

Görseller:
- G1: SHA-256 `2ce3695f94d3f75ce554604a007441838498eb286bf27eccfde5e8abb73bec4f` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-1d95d821-25dd-439e-bac9-18778fb563f4.png` · beyinde VAR: `assets/gorsel-paket-42-abcd-yukselen-destek/01-buy-abcd-d-yukselen-destek.png`

Beyin notu: `gorsel-paket-42-buy-abcd-yukselen-destek-hedefler.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R085 · 2026-08-27 22:01 UTC · RYSAS BUY AB=CD Yükselen Kanal Bağlamı Görsel Paketi 43 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Şimdi gözü kapalı ABCD'ye nasıl güveneceksin kanalı okumadan iş yapılır mı?

Görseller:
- G1: SHA-256 `1c54482a9f4e88475b526ef5c1bf63801b235fe781e6a9b597ce228f83f5617f` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-6344f9b7-2c8c-4744-92a1-4b30c91cfaee.png` · beyinde VAR: `assets/gorsel-paket-43-rysas-abcd-kanal/01-rysas-buy-abcd-yukselen-kanal.png`

Beyin notu: `gorsel-paket-43-rysas-buy-abcd-kanal-baglamı.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R086 · 2026-08-27 22:04 UTC · Basit Gizli Filtrelerle Point A Point B Breakout Keşfi Görsel Paketi 44 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Çoğumuzun aklına gelmeyecek ama hep göz önünde olan 1-2 filtre ile enteresan bir breakout sinyali var aslında:) yeni keşfettim.

Görseller:
- G1: SHA-256 `bef7184b33d69577efe04745c1d4aefe2a6ba4bbb695f44eda1de22ce4645d30` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-6eff2ccb-c8e7-4940-b1a4-34b4dee0a01d.png` · beyinde VAR: `assets/gorsel-paket-44-gizli-filtre-breakout/01-point-a-b-gizli-filtre-breakout.png`

Beyin notu: `gorsel-paket-44-basit-gizli-filtre-breakout-kesfi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R087 · 2026-08-27 22:07 UTC · BALAT AB=CD Başarısızlık Riski ve Negatif Kümülatif Delta Görsel Paketi 45 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Abcd analizine güvenip çaat diye alırsan küüt diye böyle olursun. Her zaman çalışmaz. İkinci alt grafiğe dikkat.

Görseller:
- G1: SHA-256 `af50f4ee232ee3aae4d608c0d046f0514664406133cb1e73568c29660f845259` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-de22a60d-b7e2-4447-9082-bf61a2de82dc.jpg` · beyinde VAR: `assets/gorsel-paket-45-balat-abcd-failure/01-balat-abcd-negatif-kumulatif-delta.jpg`

Beyin notu: `gorsel-paket-45-balat-abcd-negatif-kumulatif-delta.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R088 · 2026-08-27 22:11 UTC · Yapay Zeka Makine Öğrenimi Derin Öğrenme ve Veri Bilimi Kitap Reposu · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bu Github reposunda Yapay Zeka, Makine Öğrenimi, Derin Öğrenme ve Veri Bilimi ile ilgili çok sayıda kitap bulabilirsiniz.   [https://t.co/8O7OVtH0kQ](https://t.co/8O7OVtH0kQ)[github.com/Ramakm/AI-ML-B](https://t.co/8O7OVtH0kQ)

Beyin notu: `kaynak-ai-ml-dl-veri-bilimi-kitap-reposu.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.30; düşük skorlar elle doğrulandı)

### R089 · 2026-08-27 22:14 UTC · Sağlıksız Yükseliş Mavi Sıfır Kesisi ve Kırmızı Rejim Görsel Paketi 46 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> İşte sağlıklı olmayan bir yükseliş. Mavi çizgi sıfırı yukarı kestiği anda kırmızı bölgede oluşan yükselişler büyük oranda patır patır geri gelir.

Görseller:
- G1: SHA-256 `4577627c1f7bb5bf1c0ee24fcd98ed54e14d17ec4b23c1c400279395ce162fd5` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-83d3f2f3-7ee4-4c82-9d3c-ccf7987a53ff.png` · beyinde VAR: `assets/gorsel-paket-46-sagliksiz-yukselis/01-mavi-sifir-kesisi-kirmizi-rejim.png`

Beyin notu: `gorsel-paket-46-sagliksiz-yukselis-mavi-sifir-kesisi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R090 · 2026-08-27 22:17 UTC · Lindsay Trident ABC B Kırılımı ve D Hedef Formülü Görsel Paketi 47 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bunun farklı kombinasyonlarında neler yapılabilir, yazayım bir iki kelam Alış yönlü formasyon taranarak oluşmuş ABC yakalanır ve trident hedefi beklenerek teorik D noktasından yani dipten pozisyon alınır.   Satış yönlü formasyon taranarak  ABC taratılır ve bulunan oluşumlarda D trident hedefi için kısa vadeli yükseliş kovalanır. D noktasından sonra teorik olarak düşüş olacaktır. D oluşumunu teyit etmek için ise B noktası kırılımı gerekir. Aksi halde onlarca sonuç çıkar.   Ya da ABCD taramsaı yapılarak D dibinden sonra FIBO seviylerine göre iz süren takibe göre TP kovalanır.  Strtejiyi açıklamak isterdim ama artık strateji vs yazmıyorum. Zaten grafik açıklıyor herşeyi. Görseldeki bu kural, Charles Lindsay'in 1976'da yazdığı meşhur Trident (Zıpkın) Stratejisi kitabındaki formüldür. Kesinlikle tavsie ederim ne varsa eskilerde var.  Lindsay, AB=CD formasyonunu alıp A, B ve C noktaları oluştuktan sonra D noktasının (hedefin) noktasal olarak nereye gideceğini hesaplayan matematiksel bir oran geliştirmiştir.  Aşağıda tam isabet yapmış formül.  D = (B \* C) / A   Verin  yapay zekaya yazsın  "Lindsay'in Trident'i “ gerçekten efsanedir, eskilerin matematiği asla şaşmaz. Paylaşım için teşekkürler. 'Yapay zekaya yazdırın' dediğiniz kısmı ben kendi sistemimde biraz daha farklı bir boyuta taşıdım. Statik bir D noktası beklemek yerine, algoritma dünkü referans ile bugünkü açılış arasındaki korelasyonu (Varyans/K-Means) saniyede bir tarayıp hedefi dinamik olarak kalibre ediyor. Üstelik piyasanın anlık rejimine göre hedefe ulaşıldığında insan eli değmeden 'Kuantum İpi'ni kesip otonom kâr alabiliyor. Bazen aceleci davrandığı oluyor tabiki hala geliştirilmesi gereken kısımları var. 76'nın matematiğini günümüzün otonom 'fon yöneticisi' zekasıyla birleştirmek gerçekten inanılmaz sonuçlar veriyor. Eskilerin ve sizin gibi algoritmaya gönül verenlerin ellerine sağlık.

Görseller:
- G1: SHA-256 `94dcf488e168ace2d288a4971b6db5938abf9a841294baa54d53fe1a8511d0c6` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-0f616761-5a78-4f25-b76e-9e2416267455.png` · beyinde VAR: `assets/gorsel-paket-47-lindsay-trident/01-abc-b-kirilimi-trident-d.png`

Beyin notu: `gorsel-paket-47-lindsay-trident-abc-b-kirilimi-d.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R091 · 2026-08-27 22:21 UTC · Trend Rejim Değişiminde Rolling Korelasyon ve HMM Gereksizliği · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Trend rejim değişikliği için HMM yapmanıza gerek yok Koç gibi korelasyon varken hiç gerek yok hemde

Beyin notu: `tweet-trend-rejim-degisimi-korelasyon-hmm-gereksiz.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.07; düşük skorlar elle doğrulandı)

### R092 · 2026-08-27 22:24 UTC · SMRTG Fiyat ve Volatilitenin Birlikte Artışı Defansif Pozisyon Görsel Paketi 48 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bir [#smrtg](https://x.com/hashtag/smrtg?src=hashtag_click) çılgınlığı daha başladı benden demesi sistemim pozisyonu kapatıp defansif pozisyoon aldı. Fiyat ve volatilite aynı anda artması pek istenilen bir durum değildir sonu genelde kötü biter.

Görseller:
- G1: SHA-256 `02ad76cd68992823ae1d05dfa20936bc456bc4a2da2c97fdf34767901ec0afc9` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-b269c3d2-0630-4213-9d4d-0e43ffeaf254.jpg` · beyinde VAR: `assets/gorsel-paket-48-smrtg-fiyat-vol/01-smrtg-fiyat-vol-birlikte-artis-defansif.jpg`

Beyin notu: `gorsel-paket-48-smrtg-fiyat-volatilite-birlikte-artis.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R093 · 2026-08-27 22:28 UTC · Sağlıklı Yükseliş Fiyat Yukarı Mavi Seri Sıfır Altında Görsel Paketi 49 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> işte hocam sağlıklı yükseliş böyle olur, fiyat çıkarken alt panaldeki mavi çizgi de 0'ın altına iner ve oralarda gezinir. Quant strateji farklı görmektir.

Görseller:
- G1: SHA-256 `6e0331a77ca368a5ffa6e2a3336b35af36aece0b47bef490f381f8b9d72a6119` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-7f049672-ea0a-4a8e-90c4-d878833631ba.png` · beyinde VAR: `assets/gorsel-paket-49-saglikli-price-vol/01-fiyat-yukari-mavi-sifir-altinda.png`

Beyin notu: `gorsel-paket-49-saglikli-yukselis-fiyat-vol-ters-iliski.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R094 · 2026-08-27 22:33 UTC · BIST 100 ve BIST Volatilite Getirilerinde Doğrusal Olmayan Gülümseme Görsel Paketi 50 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Piyasa yapıcının bize bir mesajı var:) KY sizi seviyorum diyor çakal:D:D:D

Görseller:
- G1: SHA-256 `b7b7fa81fa4ab6fc898ca555f76309de72bf938db4c0f058cb79a1b5790a25e0` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-46182a72-4143-41e0-895b-7d082879313a.png` · beyinde VAR: `assets/gorsel-paket-50-bist-volatilite-gulumsemesi/01-bist100-bist-vol-log-getiri-scatter.png`

Beyin notu: `gorsel-paket-50-bist100-bist-volatilite-gulumsemesi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R095 · 2026-08-27 22:36 UTC · CIMSA OYAKC Z-Skorlu Rotatif Portföy Görsel Paketi 51 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> (metin yok; yalnız görsel)

Görseller:
- G1: SHA-256 `f033158e1d625fb2ae37986d4d68b228b99e534039d6ffb5806c47b9640ac8a2` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-65688a47-b5d2-4285-bc9e-96169bda0eef.jpg` · beyinde VAR: `assets/gorsel-paket-51-cimsa-oyakc-rotatif-zskor/01-cimsa-oyakc-rotatif-portfoy-zskor.jpg`

Beyin notu: `gorsel-paket-51-cimsa-oyakc-rotatif-zskor-portfoy.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R096 · 2026-08-27 22:41 UTC · İstatistiksel Arbitrajda 150 Bin Eşbütünleşme Kombinasyonu Taraması · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> İstatistiksel arbitraj sistemi için eşbütünleşme testi iyi ihtimal ile 150.000 kombinasyon taramasına kadar çıkabilir :)  Bilmeniz önemli.

Beyin notu: `tweet-istatistiksel-arbitraj-150bin-esbutunlesme-taramasi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.20; düşük skorlar elle doğrulandı)

### R097 · 2026-08-27 22:44 UTC · GARCH ve Standart Sapmayla Volatilite Riskini Azaltma Örneği · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Zaman bulursam bu akşam size garch ve standart sapma kullanarak volatiliteden kaynaklanan riski minimize etmenin yolunu örnek ile göstereceğim.

Beyin notu: `tweet-garch-standart-sapma-volatilite-risk-minimizasyonu.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.21; düşük skorlar elle doğrulandı)

### R098 · 2026-08-27 22:48 UTC · Stat-Arb Sisteminde Momentum Dönüş Teyidi ve Kâr Çarpanı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Stat-arb sisteminde momentum dönüş teyidi uygulamasının karlarda çarpan etkisine neden olduğunu şimdiden söyleyeyim, deneysel çalışmaları birileriki safhada anlatacağım:) Momentum trader olunca insan herşeye farklı bakıyor:)

Beyin notu: `tweet-stat-arb-momentum-donus-teyidi-kar-carpani.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı)

### R099 · 2026-08-27 22:51 UTC · AGROT GARAN Stat-Arb Duygusuz Disiplin ve Mark-to-Market Görsel Paketi 52 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Duygulardan arınmak nedir?Tam olarak budur
> İyi inceleyin lütfen
> Bunlar tamamen size bir disiplin aşılamak için
>
> İlk İşlem (Zararla Kapanmış):
>
> 12 Aralık 2025: Sistem Z-Skorunun +2'yi aştığını görüyor ve "AGROT SAT, GARAN AL" diyerek ilk işlemine giriyor. O an kasada tam 100.000 TL var.
>
> 16 Şubat 2026: Sistem Z-Skorunun ortalamaya (0.5) döndüğünü görüyor ve pozisyonu kapatıyor. Ancak bu süreçte muhtemelen fiyatlar beklediğimiz ideal yakınsamayı yapmadan dalgalanmış (spread aleyhimize açılıp sonra kapanmış) ve biz bu ilk trade'den zarar etmişiz. Kasamız 100.000 TL'den 92.354 TL'ye düşmüş.
>
> 2. Bekleme Dönemi (Nakit):
>
> 16 Şubat'tan 9 Mart'a kadar sistem hiçbir fırsat görmüyor ve yaklaşık 3 hafta boyunca nakitte (92.354 TL ile) pusuda bekliyor.
>
> 3. İkinci İşlem (Büyük Vurgun):
>
> 9 Mart 2026: Z-Skoru bu kez -2'yi kırıyor (AGROT aşırı ucuzluyor) ve sistem "AGROT AL, GARAN SAT" diyerek 92.354 TL'lik tüm bakiyesiyle yeni bir işleme giriyor.
>
> Ve işte sihir burada gerçekleşiyor: Bu ikinci işlem o kadar başarılı oluyor ve spread o kadar lehimize daralıyor ki, kasamızdaki 92 bin TL hızla büyümeye başlıyor.
>
> Sistem 9 Mart'ta alım yaptı (kasada 92 bin vardı).
>
> 20 Nisan 2026 ve sistem HÂLÂ LONG POZİSYONDA. Yani o 9 Mart'ta aldığı pozisyonu henüz kapatmadı (sat tuşuna basmadı).
>
> Özet Sekmesi (113.436 TL): Finansal dilde buna "Mark-to-Market" (Anlık Değerleme) denir. Yani sistem diyor ki; "Evet, şu an işlemim açık devam ediyor (Aktif Long), ama eğer tam şu saniye tüm pozisyonu bozup nakte geçersem cebime girecek olan güncel para 113.436 TL'dir."
>
> Kısacası, ilk işlemde 7.600 TL civarı zarar ettik. Ancak sistem inatlaşmamış, kurala uyup çıkmış. İkinci işlemde ise hem o zararı çıkartmış hem de üstüne 13.400 TL net kâr yazarak toplam kasayı 113 bin TL'nin üzerine taşımış. Algoritmik trade'in en güzel yanı tam olarak budur; duygusuzca zararı keser ve doğru fırsatta misliyle geri alır!
>
> 3 döküm ise işlem özetleri.
>
> Duygulardan arınmak lazım

Görseller:
- G1: SHA-256 `fa2cfcf66f155abe3cf4e5969208d08797ec86f4039171de70b6e7f9b0ccbf60` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-dcf18d9e-a3cb-4164-94ed-6481d1e42e9e.png` · beyinde VAR: `assets/gorsel-paket-52-agrot-garan-disiplin-mtm/01-stat-arb-ozet-agrot-garan.png`
- G2: SHA-256 `6b96c5a4dc226fc55e1770bfdf11582a76c353801d9885233a4c8c5265dfb610` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-9c901443-5861-458e-b18f-09dfd258e0ac.png` · beyinde VAR: `assets/gorsel-paket-52-agrot-garan-disiplin-mtm/02-al-sat-islem-logu.png`
- G3: SHA-256 `c5ac235933f68c31547159d9264a3fc6061e9d5204231bcac4bac5c687c73940` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-f74b29e1-ddff-4033-8c73-46a6e94c9c9d.png` · beyinde VAR: `assets/gorsel-paket-52-agrot-garan-disiplin-mtm/03-acik-pozisyon-gunluk-dokum.png`

Beyin notu: `gorsel-paket-52-agrot-garan-duygusuz-disiplin-mtm.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R100 · 2026-08-27 22:55 UTC · Stat-Arb Görünmez Bağ Kopuşu ve Negatif Backtest Görsel Paketi 53 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Her arbitraj fırsatı çalışmaz Mutlaka backtest etmek lazım Görünmez bağ kopmuş olabilir.

Görseller:
- G1: SHA-256 `e203e494f471766f237c6fdd638c2a985abf0f6f1ba6e5fe649026b4480570a8` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-49b8426e-8ff3-494f-b5be-f571cd1b9cec.jpg` · beyinde VAR: `assets/gorsel-paket-53-stat-arb-bag-kopusu/01-statarb-negatif-backtest-bag-kopusu.jpg`

Beyin notu: `gorsel-paket-53-stat-arb-bag-kopusu-negatif-backtest.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R101 · 2026-08-27 22:59 UTC · Stat-Arb ve Pairs Trading Kanonik Açıklama Görsel Paketi 54 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Anlatalım Nedir bu istatistiksel arbitraj meselesi Şimdi ilk grafik [#AGROT](https://x.com/hashtag/AGROT?src=hashtag_click) sistemin al verdiği nokta İkinci grafik [#GARAN](https://x.com/hashtag/GARAN?src=hashtag_click) sistemin sat verdiği nokta Son grafik ise arbitraj sistemimin çıktıları  Konu şudur kısaca  Piyasada işlem yaparken çoğumuzun sorduğu tek bir soru var. Bu hisse düşecek mi, çıkacak mı?. Sürekli geleceği tahmin etmeye çalışıyoruz.   İstatistiksel Arbitraj (Stat-Arb) ya da diğer adıyla İkili İşlem (Pairs Trading)  işte bu noktada can suyu.  Piyasadaki bazı hisseler birbirine görünmez bir elastik iple bağlıdır. (Eşbütünleşme-Cointegration). İkisi de aynı sektörde olabilir veya biri endeks (örneğin GARAN gibi bir ağırlık), diğeri o endeksi takip eden bir hisse (örneğin AGROT) olabilir.  Zaman zaman piyasadaki panik, coşku veya manipülasyonlar yüzünden bu iki hisse birbirinden kopar. Biri gereksiz yere aşırı pahalanır, diğeri geride kalıp ucuzlar. Aralarındaki görünmez elastik ip sonuna kadar gerilir. Ama istatistik bize der ki "Eğer bu iki varlık gerçekten birbiriyle eşbütünleşik (cointegrated) ise, o ip er ya da geç onları tekrar birbirine çekecektir."  İşte biz, o ipin gerildiği anı bulup, kopmadan hemen önce pozisyon alan avcılarız.  İpin Ne Kadar Gerildiğini Nasıl Ölçüyoruz? (Z-Skoru) Bunu göz kararı yapamayız. Kendi yazdığımız algoritma, iki hisse arasındaki fiyat farkını (spread) sürekli hesaplıyor ve bunu Z-Skoru dediğimiz bir birime çeviriyor.  Z-Skoru normalde 0 civarında gezer. (İki hisse barış içindedir).  Eğer Z-Skoru +2.0 seviyesini yukarı kırarsa: Bu, "A hissesi B'ye göre aşırı pahalandı, lastik koptu kopacak!" demektir.  Eğer Z-Skoru -2.0 seviyesini aşağı kırarsa: Bu sefer "A hissesi B'ye göre inanılmaz ucuz kaldı, haksızlığa uğradı!" demektir.  İşlem Stratejisi Nasıl Çalışıyor? Grafikte Z-Skoru +2'yi veya -2'yi kestiği an sistemimiz alarm veriyor ve şu sihirli hamleyi yapıyor:  Aşırı Ucuzlayanı AL (Long) Aynı anda Aşırı Pahalananı SAT (Short)  Bu sayede piyasa genel olarak ister yüzde 10 düşsün, ister yüzde 10 çıksın, bizi hiç ilgilendirmiyor. Bizim tek umurumuzda olan şey, o iki hissenin arasındaki haksız fiyat farkının kapanması ve elastik ipin tekrar gevşemesidir. Fark kapanıp Z-Skoru normale (0.5 seviyelerine) döndüğünde, pozisyonları kapatır ve kârımızı cebimize koyarız.  Peki Ya İp Koparsa? Elbette hiçbir strateji kusursuz değildir. Bazen bir şirketin başına çok temel, kalıcı bir olay gelir (iflas, çok büyük bir ihale vs.) ve o elastik ip gerçekten kopar. Hisse bir daha asla eski dengesine dönmez. Bu yüzden istatistiksel arbitraj yaparken risk yönetimi hayati önem taşır. Algoritmamız sadece matematiğe güvenir, inatlaşmaz. Yanıldığını anladığı an zararı keser.  Özetle: Borsada "yönü" bilmek zorunda değilsiniz. Aralarındaki matematiksel bağ kanıtlanmış iki hisse bulup, birinin diğerine göre saçmalamasını beklerseniz, fırsat sizin ayağınıza gelir.

Görseller:
- G1: SHA-256 `7e8550ff0f968d28d24973b601d6f7067cb24be4e79ecd6f7273114d619cca37` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-5dfeb644-a28a-45ce-add9-540ebc6d9bce.png` · beyinde VAR: `assets/gorsel-paket-54-stat-arb-kanonik/01-agrot-long-sinyal-noktasi.png`
- G2: SHA-256 `23867d27d44ef7c92ef720e12d445f1bf272714f5aa97a488a4a7cea1262de79` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-e82f980c-4878-4d9f-b158-0f03d77ecacc.png` · beyinde VAR: `assets/gorsel-paket-54-stat-arb-kanonik/02-garan-short-sinyal-noktasi.png`
- G3: SHA-256 `fb13a49cc41708de9ed40d5619fdc5089e9c32bf9eaaff68a61dcb24ac3a558e` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-d608391e-d61e-4d91-bea9-273038021b1e.png` · beyinde VAR: `assets/gorsel-paket-54-stat-arb-kanonik/03-stat-arb-sistem-ciktilari.png`

Beyin notu: `gorsel-paket-54-stat-arb-pairs-trading-kanonik-aciklama.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R102 · 2026-08-27 23:04 UTC · Volatilite ve Arbitraj Favori Sistemleri ile Otonom Disiplin Görsel Paketi 55 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Arbitraj her zaman en en sevdiğim 2 sistemden birisi İlki volatilite işi İkincisi de arbitraj Sadece sistem çalışıyor hiç ellemiyorsun:)

Görseller:
- G1: SHA-256 `94e922fbb8802adba1c471be1328332499f744ea574af946069939a959c71295` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-ac10c781-cfc1-4025-99a8-ab7049687bf7.png` · beyinde VAR: `assets/gorsel-paket-55-volatilite-arbitraj-otonom/01-agrot-garan-statarb-backtest-zskor.png`

Beyin notu: `gorsel-paket-55-volatilite-arbitraj-otonom-sistem-tercihi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R103 · 2026-08-27 23:07 UTC · BIST HFT Colocation Kuant Rekabeti ve Kod Öğrenme Çağrısı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Borsa İstanbul’da karşımızda sadece insanlar yok. Eskiden güzeldi işler. Şimdi İşlem hacminin çok büyük bir kısmını, milisaniyelerle karar veren HFT (Yüksek Frekanslı İşlem) robotları ve yerli/yabancı fonların karmaşık algoritmaları oluşturuyor.
>
> • Veri Hızı: BİST’in Colocation (eş yerleşim) hizmeti sayesinde, bu devasa firmalar sunucularını bizzat borsanın veri merkezine koyuyor. Bu, ışık hızıyla yarışan bir veri avantajı demek.
>
> • Samanlıkta İğne: Türkiye gibi volatilitenin (oynaklığın) yüksek olduğu bir pazarda, bu analistler makroekonomik verilerle fiyat hareketleri arasındaki o gizli korelasyonu bulmak için matematiksel modellerini sürekli güncelliyorlar.
>
> 2. "Trend Çizgisi" Devrinin Kapanışı
>    Türkiye’deki bireysel yatırımcılar hâlâ basit RSI veya hareketli ortalamalarla yön bulmaya çalışırken, kurumsal taraftaki Trading Development Analyst kadroları;
>    • Ekonometrik modeller, makine öğrenmesi ve yapay zeka algoritmalarıyla çalışıyor.
>    • Bizim "grafik" dediğimiz şeye onlar binlerce satırlık bir veri seti (Python, R veya C++ kodları) olarak bakıyorlar.
>    • Fibonacci seviyelerinden ziyade; piyasa likiditesini, emir defterindeki (order book) dengesizlikleri ve arbitraj fırsatlarını kovalıyorlar.
>
> 3. Türkiye piyasasının karakteristik özelliği olan yüksek volatilite, aslında bu kuantlar için bir "laboratuvar" görevi görüyor.
>    • Piyasa sert düştüğünde veya anlık dalgalandığında, bu algoritmalar veriyi anında işleyerek stratejilerini "fine-tune" (hassas ayar) ediyorlar.
>    • Şirket kârlarından ziyade, piyasanın o anki verimsizliğinden besleniyorlar.
>
> 4. Türkiye, matematik ve mühendislik alanında çok güçlü bir tabana sahip. Artık en parlak mühendislerimiz sadece yurt dışına gitmiyor; İstanbul merkezli, küresel standartlarda modelleme yapan hedge fonlarda ve aracı kurumlarda "kantitatif stratejist" olarak çalışıyorlar. Bu kadrolar, Northington’ın tarif ettiği o "seçkin ve yüksek maaşlı" grubun Türkiye şubesini temsil ediyor.
>
> O yüzden işimiz zor. İndikatör cart curt bizim zamanımızda kaldı.
>
> Kod öğrenin

Beyin notu: `tweet-bist-hft-colocation-quant-rekabet-kod-ogrenin.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.16; düşük skorlar elle doğrulandı)

### R104 · 2026-08-27 23:11 UTC · Piyasa Dilinde Kesinlik Tuzağı Olasılık Risk ve Yol Haritası · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Finansal piyasalarda tecrübe ile acemilik arasındaki en belirgin çizgi, kurulan cümlelerin kesinlik derecesinde gizlidir. Birisi size "Bu hisse kesin gidecek" diyorsa, aslında size bir yatırım tavsiyesi değil, bir kaçma sinyali veriyordur.
>
> 1. Kesinlik Bir Tuzaktır
>    Borsa, milyonlarca değişkenin (jeopolitik olaylar, bilançolar, yatırımcı psikolojisi) aynı anda çarpıştığı kaotik bir sistemdir. Bu sistemde "kesinlik" vaat eden kişi ya piyasanın doğasını anlamamıştır ya da niyetinde bir art niyet vardır.
>    • Sloganlar: "Uçacak", "Kaçacak", "Yatırım tavsiyesi değil ama kesin tavan."
>    • Gerçek: Bu dil, genellikle manipülasyonun veya aşırı özgüvenin (Dunning-Kruger etkisi) bir sonucudur.
>
> 2. Olasılık Ustaların Dilidir
>    Gerçek bir profesyonel, piyasanın her zaman haksız çıkarabileceğini bilir. Bu yüzden cümlelerini bir olasılık ve risk yönetimi çerçevesine oturtur.
>    • Usta İşi İfadeler: "Yüksek olasılıklı bir formasyon", "Risk-ödül oranı uygun", "Destek seviyesi korunursa potansiyel barındırıyor."
>    • Gerçek: Profesyoneller tahminlerle değil, stratejilerle hareket eder. Bir "ustanın" amacı haklı çıkmak değil, haksız çıktığında az kaybetmektir.
>
> Özetle
> Borsada biri size bir "varış noktası" (hedef fiyat/kesin yükseliş) gösteriyorsa dikkatli olun; ancak biri size bir yol haritası ve ihtimal senaryosu sunuyorsa, işte orada dinlemeye değer bir şeyler olabilir.

Beyin notu: `tweet-piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı)

### R105 · 2026-08-27 23:14 UTC · Momentum Değerden Önce Döner Eğim Erken Uyarı ve Kesişim Teyidi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bana sistem ile ilgili gelen sorulara verdiğim cevaplar hep aynı  Arkadaşlar ortalama kullanıyor iseniz eğimlere dikkt edeceksiniz. Momentum trader iseniz sinyal eğiminize dikkat edeceksiniz  Momentum Değerden Önce Döner  Finansal piyasalarda çoğu yatırımcı Golden Cross gibi sinyalleri beklerken aslında hareketin çoktan başladığını ve maliyetin yükseldiğini fark etmez. Teknik analizin en temel ama en güçlü kurallarından biri şudur: Momentum (Hız), değerden (Fiyat veya Gösterge) önce döner.  Neden Eğim? Bir hareketli ortalamanın kesişmesini beklemek, iki nesnenin çarpışmasını beklemek gibidir. Oysa bu nesnelerin birbirine doğru yöneldiğini anlamak için eğimlerine bakmak yeterlidir.  Matematiksel bir perspektifle; bir ortalamanın eğimi onun birinci türevidir. Eğer eğim negatiften pozitife dönüyorsa, momentum yukarı yönlü ivme kazanmaya başlamış demektir. Kesişim bir onay  iken, eğimin yön değiştirmesi bir erken uyarı sinyalidir.  Eğim Takibinin Avantajları Erken Teşhis: Fiyat dip çalışmasını bitirip yukarı döndüğünde, önce kısa vadeli ortalamanın eğimi pozitife döner. Bu, trendin başladığına dair ilk somut işarettir.  Maliyet Avantajı: Kesişim gerçekleştiğinde fiyat genellikle %5-%10 primlenmiş olur. Eğimleri takip ederek, "kesişim taramalarına" düşmeden önce trene binmiş olursunuz.  Trend Doğrulaması: Eğer uzun vadeli ortalamanın da eğimi pozitife dönmüşse, bu artık geçici bir tepki değil, orta vadeli bir ivme işaretidir.

Beyin notu: `tweet-momentum-degerden-once-doner-egim-erken-uyari.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.16; düşük skorlar elle doğrulandı)

### R106 · 2026-08-27 23:19 UTC · Aritmetik Ortalama Outlier Rejim Kırılması ve Sağlam Merkez Riski · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Ah ortalamalar ah! herkes peşinde ama seni gerçekten tanıyan kaç kişi var  Ortalamalar tehlikelidir, neden tehlikelidir sorusunu en ciplak haliyle soyle ozetleyelim:  Ortalama (aritmetik ortalama), verideki en buyuk yalanci ve en kirilgan yapidir. finansal piyasalarda fiyatlar uysal bir sekilde hareket etmez. bir hisse 19 gun boyunca 100 lira civarinda dolasip 20. gun bir skandalla 50 liraya duserse, senin 20 gunluk ortalaman fiyatin gercekte hic bulunmadigi sacma bir noktaya iner.  Ortalamanin tehlikeli olmasinin temel sebebi, uclardaki sarsintilari (outliers) sanki normal bir hareketmis gibi toplama dahil etmesidir. matematiksel olarak ifade etmek gerekirse:  ortalama = (fiyat1 + fiyat2 + fiyat3 + ... + fiyatn) / n  Buradaki n her bir fiyata esit oy hakki verir. eger fiyatn degeri, piyasadaki bir panik veya spekulasyon yuzunden digerlerinden cok uzaklasirsa, tum toplam sonucunu kendine dogru ceker. n degeri ne kadar kucukse (ornegin 10 gunluk sma), bu yalan o kadar buyuk olur.  Özetle; ortalamaya guvenmek, bir ayagi buzun icinde bir ayagi atesin icinde olan birine "ortalamada sicakligin gayet iyi" demek gibidir.

Beyin notu: `tweet-aritmetik-ortalama-outlier-rejim-tehlikesi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.06; düşük skorlar elle doğrulandı)

### R107 · 2026-08-27 23:22 UTC · Finans Mühendisliği ile Destek Direnç Seviye Motoru · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Finans mühendisliği modelleri destek ve direnç seviyelerini bulmak için kullanılır mı? Benim gibi tembel adamsanız evirir çevirir yaparsınız:) Yakında denemeye başlayacağız

Beyin notu: `tweet-finans-muhendisligi-destek-direnc-seviye-motoru.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.08; düşük skorlar elle doğrulandı)

### R108 · 2026-08-27 23:27 UTC · A1CAP Weinstein Dört Evre Fiyat Hacim Döngüsü Görsel Paketi 56 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Ne görüyoruz??  Grafik Temmuz 2023'ten Ocak 2026'ya kadar olan fiyat ve hacim geçmişini, Stan Weinstein'ın meşhur "Piyasanın 4 Evresi" (4 Stages) döngüsü çerçevesinde mükemmel bir şekilde gösteriyor. Grafikte fiyatın yataydan güçlü bir yükselişe, oradan zirveye ve nihayetinde düşüşe geçişini tüm teknik detaylarıyla görebiliyoruz.  Grafik Piyasanın "4 Evre" döngüsünü temsil ediyor   Evre 1: Taban/Birikim: Fiyatın yataylaştığı, hacmin kuruduğu ve akıllı paranın biriktirmeye başladığı aşama.  Evre 2: Yükseliş/Boğa: Fiyatın X haftalık eğriyi ve hacmi arkasına alarak güçlü bir trend başlattığı aşama.  Evre 3: Tepe/Dağıtım: Yükselişin yavaşladığı, hacmin "çalkalandığı" ve kar realizasyonunun başladığı aşama.  Evre 4: Düşüş/Ayı: Korkunun ve panik satışlarının hakim olduğu, fiyatın çöktüğü aşama.  [#A1CAP](https://x.com/hashtag/A1CAP?src=hashtag_click)

Görseller:
- G1: SHA-256 `d2d1a0e4d51e095493d870179814450c4f42bb2be293d231bbbc107dcf08c7d8` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-313f3ca5-7255-4460-957f-95425934c8a5.jpg` · beyinde VAR: `assets/gorsel-paket-56-a1cap-dort-evre/01-a1cap-fiyat-hacim-dort-evre.jpg`

Beyin notu: `gorsel-paket-56-a1cap-weinstein-dort-evre.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R109 · 2026-08-27 23:33 UTC · Kağıt Kalem Matematik Önce Kod Sonra Model Geliştirme Disiplini · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Kahveler ve kağıt kalem hazırlandı. Çalışmalar başlıyor. Asla kalem kağıt kullanmadan sistem yazmam, bunu huy edinin bence. Eğer bir modelegliştirmek istiyor iseniz ve elinizde detaylı anlatım varsa matematkisel olarak önce bunu kağıt üzerinde çözün koda sonra dökün. Eğer AI kullanıyor iseniz bunu yapmanız bir zorunluluk. AI kullanmıyor iseniz bunu yapmak size farklı fiklirleri aklınıza getirmesi adına önemli.

Beyin notu: `tweet-kagit-kalem-matematik-once-kod-sonra.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.06; düşük skorlar elle doğrulandı)

### R110 · 2026-08-27 23:38 UTC · Düşük Korelasyon Yüksek Volatilite Max Sharpe ve Aktif Trading Matematik Föyü · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27); `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)
- Aynı yapıştırma ikinci kez: oturum içi sıra no 159

> Kitapların yazmadığı bir yaklaşımı size anlatayım.  Düşük Korelasyon & Yüksek Volatilite ile Maksimum Sharpe Portföyü  Bu model; modern portföy teorisini, istatistiksel arbitraj ve aktif volatilite trade'i ile birleştiren üç aşamalı bir "tecrübe tabanlı" sistemdir. Kitaplardaki teorik yaklaşımların aksine, piyasa dinamizmini (volatilite) bir risk değil, bir getiri motoru olarak konumlandırır.  Aşama 1: Seçim  Stratejinin temeli, doğru hisse grubunu bir araya getirmektir. Burada iki zıt ama birbirini tamamlayan kriter kullanılır:  • Düşük Korelasyon : Seçilen hisselerin birbiriyle olan fiyat hareketleri bağımsız olmalıdır. Bu, piyasa genelindeki bir düşüşte tüm portföyün aynı anda çökmesini engeller (Sistemik risk yönetimi).  • Yüksek Volatilite: Portföye girecek hisselerin "hareketli" olması gerekir. Volatilitenin yüksek olması, fiyat salınımlarının geniş olacağı anlamına gelir ki bu da trade fırsatı yaratır.  Aşama 2: Markowitz Optimizasyonu ve Sharpe Verimliliği  Seçilen 10-20 hisselik aday listesi, Modern Portföy Teorisi (Markowitz) süzgecinden geçirilir. Ancak burada amaç sadece "al-bekle" yapmak değil, matematiksel olarak en verimli ağırlıkları bulmaktır.  1.Etkin Sınır (Efficient Frontier): Belirli bir risk seviyesinde en yüksek getiriyi veren ağırlık kombinasyonları hesaplanır. 2.Sharpe Oranı Optimizasyonu: Risk birimi başına en yüksek getiriye (Max Sharpe) sahip "Teğet Portföy" (Tangency Portfolio) oluşturulur. 3.Hisse Sayısı: Analiz sonucunda en verimli 3 ile 10 arası hisse, nihai trade listesine alınır. 4. Sistemin üzerine inşaa edilecek hissenin oranı %50 den fazla olmalıdır.  Aşama 3: Volatilite Trading  Bu aşama, modeli statik bir portföyden aktif bir makineye dönüştürür. Markowitz ile ağırlıkları belirlenmiş bu "verimli" hisselerde pasif beklemek yerine, hisselerin yüksek volatilitesi kullanılarak trade edilir.  • Strateji: Seçilen hisseler zaten yüksek volatiliteye sahip olduğu için, belirli teknik göstergeler (RSI, Bollinger Bandı veya Mean Reversion modelleri) ile bu hisselerin iç dalgalanmalarından kar realize edilir.  • Dinamik Yönetim: Portföyün ana iskeleti (Markowitz ağırlıkları) korunurken, volatilite sayesinde dipten alıp tepeden satarak "Alpha" yaratılır.  Bu modelle, hem matematiğin güvenli limanına (Markowitz) sığınırsınız hem de piyasanın dalgalarını (Volatilite) sörf tahtası olarak kullanırsınız. Tecrübenin gösterdiği üzere; en iyi portföy, matematiksel olarak optimize edilmiş ve aktif olarak yönetilen portföydür.

Beyin notu: `tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı)

### R111 · 2026-08-27 23:42 UTC · Kitaptan Özgün Model Sentezine Backtest Forward Test ve Kod Mimarisi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Bakın arkadaşlar, kitap okumak vizyonunuzu geliştirir ama sadece kitaplarda gördüğünüz hazır modelleri olduğu gibi uygulamaya çalışmak sizi başarıya götürmez. Gerçek başarı; farklı kaynaklardan öğrendiğiniz çeşitli modelleri sentezleyerek kendinize has, özgün bir yapı kurmaktan geçer. Bu yapıyı oluşturduktan sonra sabırla backtest ve forward test süreçlerini yönetmeniz gerekir. Unutmayın; bilgiyi nasıl işlediğiniz, onu nasıl bir modele döktüğünüz ve kurduğunuz kod mimarisi başarınızın asıl anahtarıdır. Sizi diğerlerinden ayıracak olan, kendi mantığınızla inşa ettiğiniz bu sistemdir.

Beyin notu: `tweet-kitap-model-sentezi-backtest-forward-test-kod-mimarisi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.07; düşük skorlar elle doğrulandı)

### R112 · 2026-08-27 23:46 UTC · TEKTU EREGL Portföy Ağırlık Duyarlılığı ve Ex-Post Getiri Görsel Paketi 57 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Portföy yönetimi e getiri hesaplamak geriye doğru simülasyonlar önemlidir  Örneğin TEKTUDuyarlılığına bakalım (1. grafik): TEKTU ağırlığı artıkça portföy getirisi doğrusal artıyor — %0'dan %100'e gidince getiri %12'den %30'a çıkıyor. Bu dönemde TEKTU güçlü performans sergilemiş, portföye ne kadar çok koysan o kadar iyi.  EREGL Duyarlılığına bakalım (2. grafik): Tam tersi — EREGL ağırlığı artıkça getiri düşüyor. %0 EREGL'de portföy %18 kazanırken, %100 EREGL'de %13'e geriliyor. EREGL bu dönemde görece zayıf kalmış, portföydeki payı azaldıkça performans artıyor.  Demekki Bu periyotta optimal strateji TEKTU ağırlığını artırıp EREGL'i azaltmak olurdu. Mevcut %30 TEKTU / %20 EREGL dağılımın EREGL tarafı portföyü baskılıyor.  İlk özet tablosu mevcut durumdaki durum. İkinci özet tablosunda ise portföyde EREGL ağırlığını %10'a çekince oluşan sonuç.  Önemlidir.

Görseller:
- G1: SHA-256 `4dccd76c5a8f69159bd295584ed59b2441a161b989edbeb2154fe0c82bd9c365` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-f05d1152-a2f2-421b-bcb2-365708c9419c.jpg` · beyinde VAR: `assets/gorsel-paket-57-tektu-eregl-agirlik-duyarliligi/01-tektu-agirlik-duyarliligi.jpg`
- G2: SHA-256 `b2c0b36b0418a0d74093f8408bac9b44b7f8492bbae4821c05895bce39b08594` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-83b230a7-c82d-4a06-b7f6-9fc72c390b79.jpg` · beyinde VAR: `assets/gorsel-paket-57-tektu-eregl-agirlik-duyarliligi/02-eregl-agirlik-duyarliligi.jpg`
- G3: SHA-256 `7a2fef2738bcfaa832cbf6760b3141f7f4a9dc01410654b470fce7e7c48bb30d` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-10b33b49-e85a-4fea-9324-3650e6a6703a.png` · beyinde VAR: `assets/gorsel-paket-57-tektu-eregl-agirlik-duyarliligi/03-mevcut-50-30-20-portfoy-ozeti.png`
- G4: SHA-256 `da44da7dac16839caa5d3094e3b6f8f8a725ac9f6b4715bfa163d9828a13f7a2` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-6471e691-1ad5-4c59-bba6-19ebbe0b2f85.png` · beyinde VAR: `assets/gorsel-paket-57-tektu-eregl-agirlik-duyarliligi/04-revize-50-40-10-portfoy-ozeti.png`

Beyin notu: `gorsel-paket-57-tektu-eregl-agirlik-duyarliligi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R113 · 2026-08-27 23:50 UTC · Portföy Optimizasyonu Volatilite Trading ve Huzurlu Gece Risk Bütçesi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Portföy optimizasyonu ve volatilite trading arasındaki ilişki huzurlu gecelerin anahtarıdır. İlgilenenlere duyurulur.

Beyin notu: `tweet-portfoy-optimizasyonu-volatilite-trading-risk-butcesi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı)

### R114 · 2026-08-27 23:53 UTC · GUBRF Fincan Kulp Fibo Kırılım Hedef Matematik Föyü Görsel Paketi 58 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27); `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)
- Aynı yapıştırma ikinci kez: oturum içi sıra no 160

> Arkadaşlar selamlar, kendi tarama sistemimin yakaladığı GUBRF grafiğini fincan-kulp formasyon mantığına göre adım adım inceleyelim.
>
> 1. Fincan Oluşumu (Mavi Çizgi): Grafiğe baktığımızda Mart 2025 civarında başlayan düşüş trendinin, Temmuz 2025 ortalarında 212.20 seviyesinde dip yaptığını görüyoruz. Burası sistemimizin de Fibo 100% olarak işaretlediği, satış baskısının bittiği ve malın toplandığı ana dip noktası. Fiyat buradan güç bularak Eylül ayına kadar yükseliyor ve 317.00 (Fibo 0%) seviyesinde fincanın sağ ağzını tamamlıyor.
>
> 2. Kulp Düzeltmesi (Turuncu Çizgi): 317.00 seviyesine geldikten sonra fiyat, fincanı kırmadan önce son bir silkeleme ve güç toplama evresine giriyor. Turuncu ile çizilen kulp kısmında, fiyatın Fibonacci 61.8% (252.23) ve 50% (264.60) bölgesi arasına kadar çok sağlıklı, sığ bir düzeltme yaptığını görüyoruz. Algoritmanın risk analizi burada devreye giriyor; 1:2.27   Risk/Reward (Risk-Ödül) oranı sunuyor.
>
> 3. Kırılım Sinyali (Yeşil Ok): grafikteki giriş noktası. 24 Ekim 2025 tarihinde fiyat toparlanıp 300.75 seviyesindeki yeşil kesik çizgiyi (KIRILMA) yukarı kesiyor. Sistemimiz tam o saniye "SİNYAL!" okunu yapıştırıyor.
>
> 4. Formasyon Hedefi ve Sonuç: Fincan derinliği kadar yukarı gitme mantığına dayanan formasyon hedefimizi sistemimiz 389.30 (mor kesik çizgi) olarak belirlemiş. Kırılım geldikten sonra hisse arkasına bakmıyor, çok kısa bir sürede formasyon hedefini vuruyor. Hatta momentum o kadar güçlü ki, bizim hedefimizi de paramparça edip 2026'nın ilk aylarına doğru devasa bir ralliye kalkıyor.
>
> Benim algoritmik sistemler kurarken anlatmak istediğim olay tam olarak budur. doğru formasyonu doğru seviyede, sıfır duyguyla ve tam zamanında yakalamak. Sonrası zaten trendin peşine takılmaktan ibaret.

Görseller:
- G1: SHA-256 `7435a3c848c767bc11f162bd8986515ff8bb38dddb38857851dfc81b4f95feb0` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-52d219d2-f916-4e4f-838c-03658c638c51.png` · beyinde VAR: `assets/gorsel-paket-58-gubrf-fincan-kulp/01-gubrf-fincan-kulp-fibo-kirilim-hedef.png`

Beyin notu: `gorsel-paket-58-gubrf-fincan-kulp-matematik-foyu.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R115 · 2026-08-27 23:58 UTC · Buy and Hold ile Sinyal Bazlı Strateji Risk Getiri Scorecard Görsel Paketi 59 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-27)

> Porföylerinizde aşağıdaki gibi bir tablo sizi rahatlatır huzurlu uyutur  Stratejimiz, ham getiriden bir miktar feragat ederek karşılığında çok daha huzurlu bir eğri sunmuş. Özellikle volatiliteyi %33'ten %23'e çekmesi, sert düşüşlerde portföyü koruma kapasitesinin yüksek olduğunu gösteriyor. Sharpe oranlarının aynı olması, risk/getiri dengesinin matematiksel olarak korunduğuna işaret ediyor.

Görseller:
- G1: SHA-256 `1056d8a9560639dfaf3dfa1bbdbaedd13d193f3e0cc55e68dccc1017435ca9aa` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-7708b307-e22e-4fa9-b44d-e94b46a40989.png` · beyinde VAR: `assets/gorsel-paket-59-risk-scorecard/01-buyhold-sinyal-stratejisi-risk-scorecard.png`

Beyin notu: `gorsel-paket-59-buyhold-sinyal-risk-scorecard.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R116 · 2026-08-28 00:04 UTC · Gizli Pozitif Uyumsuzluk Trend Devamı ve Beş Günde Yüzde 29 Görsel Paketi 60 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> Sadece 5 günde %29 nasıl verdi?  Gizli pozitif uyumsuzluk örneğidir. Fiyat paneline baklıldığında diplerin yükseldiğini yani ana trendin yukarı yönlü gücünü koruduğunu net bir şekilde görüyoruz. Ancak alt taraftaki indikatör paneline baktığımızda fiyatın aksine diplerin aşağı kaydığını fark ediyoruz. Bu durum aslında piyasanın bir nevi yakıt tazeleme sürecinde olduğunu fısıldar. Yani fiyat geri çekilse bile bir önceki dibinin altına inmiyor ancak indikatör daha derin bir dip yaparak momentumdaki şişkinliği alıyor ve güç topluyor. Teknik olarak biz buna trend devam sinyali diyoruz.   Özetle bu görüntü bize yükseliş trendinin bozulmadığını aksine indikatörün soğuyarak yeni bir ralli için enerji depoladığını anlatıyor. Bu uyumsuzluk türü genellikle düzeltme bittiğinde trendin kaldığı yerden daha sert devam edeceğinin habercisidir.

Görseller:
- G1: SHA-256 `5740a155307f9d680bf18d0a2a4698ea08b2a011b0446a12ecef19ae72057e8f` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-5b05f4f3-ed9f-4ca6-99d7-7ed3dd1ba0e0.png` · beyinde VAR: `assets/gorsel-paket-60-hidden-bullish-divergence/01-fiyat-higher-low-indikator-lower-low.png`
- G2: SHA-256 `695f4c8dec4ac6119a83a3f84ffda44fd1aa6fe62106b63197fd56797a5f9e14` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-b892dfe5-08de-420e-a069-701a9f6cfdf4.png` · beyinde VAR: `assets/gorsel-paket-60-hidden-bullish-divergence/02-bes-gunluk-yukselis-sonucu.png`

Beyin notu: `gorsel-paket-60-hidden-bullish-divergence.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R117 · 2026-08-28 00:08 UTC · Gizli Uyumsuzlukları Takip Etme Watchlist Hatırlatması Görsel Paketi 61 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> Gizli uyumsuzlukları takip ediniz, arkadaşça hatırlatma.

Görseller:
- G1: SHA-256 `7af60966a22610176203af94bddb24a48f7b82276601122eae2b707ca01ccd11` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-97c9ed1a-a208-4228-9d3d-5656026e92dc.png` · beyinde VAR: `assets/gorsel-paket-61-hidden-divergence-watchlist/01-hidden-bullish-divergence-takip-gorseli.png`

Beyin notu: `gorsel-paket-61-hidden-uyumsuzluk-takip-hatirlatmasi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R118 · 2026-08-28 00:11 UTC · Endeks 5/5 Trend Skoru NH-NL Genişliği ve Corwin-Schultz Likidite Raporu · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> Bugün endeks bana ne anlatıyor?
>
> Genel analiz raporumuzdaki 5 / 5 skor, piyasanın dışarıdan bakıldığında kusursuz bir yükseliş trendinde olduğunu tescilliyor.
>
> Trendin Kalitesi: ADX (28.9) ve RSI (77.6) gibi göstergeler, yükselişin hem güçlü hem de ivmeli olduğunu söylüyor. VIX (20.6) seviyesi, küresel piyasalarda şu an için bir siyah kuğu beklemediğimizi ve stresin düşük olduğunu gösteriyor.
>
> Momentumumuz alıcıların kontrolü tamamen elinde tuttuğunu teyit ediyor.
>
> 2. NH-NL ve Piyasa Derinliği
>
> Yeni Yüksek-Yeni Alçak (NH-NL) verilerini makro verilerle birleştirdiğimizde, yükseliş hakkında kritik bir ipucu yakalıyoruz
>
> Kısa Vade (20 Günlük): 83 puan ile piyasada tam bir bayram havası var. Hisse bazlı kısa vadeli ralli teyit edilmiş durumda.
>
> Orta Vade (65 Günlük): Buradaki "Katılım Yok" uyarısı, yükselişin hala genele (tüm sektöre ve yan kağıtlara) yayılmadığını gösteriyor.
>
> Bu durum, endeksi sırtlayan ana kağıtların yolu açtığını ama küçük ve orta ölçekli hisselerin henüz tam hızlanmadığını anlatıyor.
>
> 3. XU100 Corwin-Schultz: Endeksin Likidite Karnesi
>
> XU100 grafiği, bu yükselişin tehlikeli olup olmadığını anlamamızı sağlıyor
>
> Spread (Makas) Durumu: Endeks bazında ortalama spread %1.06 seviyesinde. Grafiğe baktığımızda, geçmişteki o belirsizlik anları aksine, şu anki spread seviyeleri oldukça stabil. Bu, endeks ağırlığı yüksek hisselerde tahtaların dolu olduğunu ve derinliğin korunduğunu gösteriyor.
>
> Sigma: Volatilite  geçmişteki kriz dönemlerine göre oldukça sakin. Fiyat rekor tazeliyor ama piyasa bunu histerik bir şekilde değil, kontrollü bir şekilde fiyatlıyor.
>
> Mikro-Makro Çelişkisi: XU100 spread'i dar olmasına rağmen, genel hacim analizindeki Düşük Hacim uyarısı hala masada. Bu da bize paranın şu an akıllı ve seçici olduğunu, piyasanın geneline henüz saçılmadığını söylüyor.
>
> Stratejik Yol Haritası
>
> Elimizdeki üç farklı veri setini birleştirdiğimizde nihai beklentimiz şudur:
>
> Trend Full Long bölgesinde kalmaya devam ediyor. Ancak, 65 günlük katılımın zayıf olması ve hacmin düşüklüğü, bu rallinin ince bir buz üstünde yürüyen lokomotifler tarafından çekildiğini hatırlatıyor.
>
> Nihai Karar ve Strateji:
>
> Liderleri Takip Edin: XU100 spread'i düşük ve stabil olduğu için, endeks üzerinde ağırlığı olan likit hisselerde kalmak şu an en güvenli liman.
>
> Hacim Teyidi Bekleyin: Hacim barlarında belirgin bir artış ve 65 günlük NH-NL verisinde pozitife dönüş görmeden yan kağıtlarda agresifleşmemek mantıklı görünüyor.
>
> Sigma Takibi: Sigma ani bir sıçrama görmediğimiz sürece, mevcut trendin tadını çıkarmaya devam edebiliriz.
>
> Özetle; endeks motoru (XU100) çok sağlıklı çalışıyor, makas dar, yol açık. Sadece tüm araçların (tüm hisselerin) konvoya katılmasını bekleyen bir bekleme odasındayız.

Beyin notu: `tweet-endeks-5of5-nhnl-corwin-schultz-likidite.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R119 · 2026-08-28 00:15 UTC · FROTO Corwin-Schultz Spread Sigma Likidite ve Volatilite Görsel Paketi 62 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> Şu kolaylaştırmaya çalıştığım konuyu size sade bir dille anlatayım
>
> Corwin-Schultz Analizi bize şunu anlatır.
>
> Bu analizde, derinlikli veri kullanmadan sadece En Yüksek  ve En Düşük  fiyatlar üzerinden piyasanın "arka planını" nasıl okuyabileceğimizi özetlemeye çalıştım. Fİnans mühendisi grafiğe bakınca çizgiler görmez bunları oumaya çalışır.
>
> Piyasanyı bir motor gibi düşünürsek, bu motorun verimliliğini iki ana parametre ile ölçeriz:
>
> A. Bid-Ask Spread (Kırmızı Panel): Piyasanın Sürtünme Katsayısı Spread, basitçe alış ve satış fiyatı arasındaki "makas" aralığıdır.
>
> Düşük Spread: Tahtanın "dolu" olduğunu, alıcı ve satıcının birbirine çok yakın olduğunu ve likiditenin yüksek olduğunu gösterir. İstediğiniz an, istediğiniz fiyattan çıkabilirsiniz.
>
> Yüksek Spread: Tahtanın "boşaldığını" ve likiditenin kuruduğunu gösterir. Burada işlem yapmak pahalıdır; çünkü "piyasa fiyatından" alım yaptığınızda çok yukarıdan eşleşme riskiniz (slippage) yüksektir.
>
> B. (Mor Panel): Piyasanın Tansiyonu olan Sigma, piyasadaki volatiliteyi (oynaklığı) temsil eder. Fiyatın ne kadar sert ve agresif hareket ettiğinin ölçüsüdür.
>
> Yüksek Sigma: Belirsizliğin arttığı, fiyatın kontrolsüzce savrulduğu "tansiyonu yüksek" dönemlerdir.
>
> Düşük Sigma: Piyasanın dengede olduğu ve fiyat hareketlerinin daha öngörülebilir olduğu dönemlerdir.
>
> 2. FROTO Örneğine bakarsak (Ocak - Nisan 2026) grafikteki hareketleri bu iki kavram ışığında okuduğumuzda karşımıza şöyle bir tablo çıkıyor.
>
> Ocak - Şubat Ortası: Sağlıklı Yükseliş görülüyor. Ocak ayı boyunca fiyatın 90'lardan 125'lere gittiği dönemde Spread (Kırmızı) genel olarak ortalamanın altında seyrediyor. Bu çok kritiktir çünkü yükselişin "dolu bir tahta" ile, yani yüksek likidite ile gerçekleştiğini gösterir. Gerçek bir para girişi ve kurumsal iştah söz konusudur.
>
> Şubat Sonu - Mart: Tansiyonun Yükselmesi ile fiyat zirveden (125 TL) geri çekilmeye başladığında Sigma (Mor) panelinde sert zıplamalar görüyoruz. Bu, piyasadaki "karar anını" ve oynaklığın arttığını gösterir. Dikkat ederseniz, Sigma'nın zıpladığı her yerde Spread de onu takip ederek yukarı kafa atıyor.
>
> Nisan Başı: (Likidite Tuzağı) Grafiğin sonlarına doğru (Nisan başı), Spread'in %7 civarına fırladığı bir bölge var. Burada fiyat mumları çok büyük olmasa da makas inanılmaz açılmış . Bu, "tahta sahipsiz kalmış" demektir. Alıcı ve satıcı arasındaki köprü kopmuştur. Bu tür dönemlerde en küçük bir hacim bile fiyatı %3-4 aşağı veya yukarı "ışınlayabilir". Güvenli işlem yapmak için spread'in tekrar ortalamaya (%1.79) dönmesini beklemek gerekir.
>
> Sonuç ve Stratejik Not ve Altın Kural: Spread yüksek, Sigma yüksekse; o tahtadan uzak durun ya da "stop-loss" seviyelerini çok geniş tut. Eğer Spread düşük ama Sigma yüksekse, orada gerçek bir "boğa-ayı savaşı" vardır; trendin yönüne güvenebilirsin.
>
> FROTO özelinde şu anki durum (Nisan sonu), spread'in tekrar sakinleşmeye başladığını ancak volatilitenin hala "tetikte" olduğunu gösteriyor. Tahtanın tekrar dolması, stabil bir trend için şart.
>
> bu verileri bir de "Hacim (Volume)" ile korele edip tahtadaki gerçek niyetin "mal boşaltma" mı yoksa "toplama" mı olduğunu daha net görebiliriz kodunu da yazabiliriz kolayca.

Görseller:
- G1: SHA-256 `79c93e06193258b1e6a94c516c259bf85692f366c8ba120c5a0589ecc2c8e21a` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-6597c25b-eb20-4169-9c90-cbef8610f5d5.png` · beyinde VAR: `assets/gorsel-paket-62-froto-corwin-schultz/01-froto-corwin-schultz-spread-sigma.png`

Beyin notu: `gorsel-paket-62-froto-corwin-schultz-spread-sigma.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R120 · 2026-08-28 00:20 UTC · BIST 12 Aylık Momentum Decile Stratejisi ve Dört Aylık DEY Backtest Denetimi Görsel Paketi 63 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> Borsada para kazanmanın binlerce yöntemi var ama bunların büyük çoğunluğu ya çok karmaşık ya da gerçek hayatta uygulanamaz. Ben de uzun süredir şunu merak ediyordum acaba BIST'te gerçekten işe yarayan, basit, sistematik bir strateji kurabilir miyim?  İşte bu yüzden basit bir momentum stratejisini test ettim. Momentum fikri aslında çok basit bir insan psikolojisine dayanıyor. İnsanlar kazanan hisseye atlıyor, kaybedenden kaçıyor. Bu sürü psikolojisi fiyatlara yansıyor ve geçen sene yükselen hisse bu sene de yükselmeye devam ediyor. Buna akademik dünyada "momentum anomalisi" deniyor ve 1990'lardan beri onlarca ülkede kanıtlanmış bir gerçek.  Ben de bunu BIST'te test etmek istedim. 2015'ten bugüne BIST'teki 500'den fazla hissenin fiyat verisini çektim. Her ay için her hissenin son 12 aydaki getirisini hesapladım. Sonra tüm hisseleri bu performansa göre sıralayıp 10 eşit gruba böldüm. En iyi grup geçmişte en çok yükselen hisseler, en kötü grup ise en çok düşenler.  Mantık şu. eğer momentum gerçekten çalışıyorsa, geçmişte en çok yükselen hisseler bir sonraki ay da diğerlerinden daha iyi performans göstermeli. Bunu test etmek için her ay bu sıralamayı güncelledim ve bir sonraki ay o gruptaki hisseleri eşit ağırlıkla tuttuğumu varsaydım. Yani her ay sadece şunu sordum: "Son 12 ayda en çok yükselen hisseler hangileri?" O listeyi aldım, eşit ağırlıkla kodum, bir ay tuttum, sonra listeyi yeniledim.  Sonuç beklediğim gibi çıktı. En iyi momentum grubundaki hisseler diğer tüm grupları geride bıraktı. Yıllık getiri ve Sharpe oranı açısından en üst grup açık ara önde.  Tabii bunun sınırları var. Bu bir backtest, yani geçmişe dönük bir simülasyon. İşlem maliyetleri, vergiler ve likidite sorunu olan hisseler hesaba katılmadı. Aylık olarak 50+ hisseyi yenilemek gerçek hayatta ciddi bir maliyet demek. Ama temel fikir doğrulandı: BIST'te momentum çalışıyor.  4 aylık getiriler aşşağıdaır.

Görseller:
- G1: SHA-256 `28a47ebf9d2320e56f763cfa95c200207bf3dcab8dbff6d71e7178102a306731` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-3acc04d0-78aa-43d5-9455-6200adc5784c.jpg` · beyinde VAR: `assets/gorsel-paket-63-bist-momentum-dey/01-bist-momentum-dort-ay-dey-tablosu.jpg`

Beyin notu: `gorsel-paket-63-bist-momentum-dey-backtest-denetimi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R121 · 2026-08-28 00:25 UTC · Optimal Momentum Plus Kod Tamamlanması, Simülasyon İlerlemesi ve Teori Serisi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> İşimi bitirdim kodum optimal momentum+ portföyü için simülasyon yapıyor bende ona kadar size momentum teorisini anlatayım, söz vemiştim.

Beyin notu: `tweet-optimal-momentum-plus-simulasyon-tamamlandi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı)

### R122 · 2026-08-28 00:28 UTC · Kendini Yenileyen Algoritma Ana Frekans ve Kanıtlı Öğrenme Döngüsü · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> Algoculara naçizane öneri   Sizin derdiniz sadece bir noktaya varmak olmasın, her döngüde daha güçlü hale gelen, verinin en ince kılcal damarlarına kadar sızan bir algoritma kurmak olsun. Çünkü doğru frekansı bulduğunuzda, sistem artık sizin için çalışmaz, siz sistemin kendisi olursunuz. Öyle bir matematiksel yapı kurun ki sistem sürekli kendini yenilesin. sadece para kazanan bir kodun değil, bu evrensel dengeyle uyumlu çalışan, hata payını minimize eden o kusursuz matematiğin peşinde olun.  Unutmayın, piyasalar, doğa, ses, hatta insan psikolojisi bile aslında karmaşık görünse de arka planda belirli frekanslarda hareket eder. sisteminizle, o karmaşanın içindeki "ana frekansı" yakalamaya çalışın.  Aksi halde yatırım hayatı boyunca çizgi çeker durursunuz.

Beyin notu: `tweet-kendini-yenileyen-algoritma-ana-frekans.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R123 · 2026-08-28 00:32 UTC · Stefan Jansen Machine Learning for Trading Kitap ve Kaynak İncelemesi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28); `archived_sessions/rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl` (2026-08-28)

> Stefan Jansen Bu ismi unutmayın Python ile makine öğrenmesi algo trading öğrenmek istiyor iseniz adamınız bu. Kitaplarını inceleyin. Bir yazar daha var çok severim, adını hatırlayamadım, aklıma gelince yazarım.

Beyin notu: `kaynak-stefan-jansen-ml-algo-trading.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı)

### R124 · 2026-08-28 00:41 UTC · Düşen Trend Kırılımı Talep Hacim ve EMA Teyidi Görsel Paketi 64 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Düşen Trend Kırılımı ve Hacimli Onay olarak adlandırabikeceğimiz oldukça güçlü bir yükseliş senaryosunu gösteren bir yapıyı konuşalım
>
> 1. Düşen Direnç Çizgisi
>    Fiyat bu çizgiye her yaklaştığında satış yemiş ve geri çekilmiş. Ancak grafiğin en sağında, fiyatın bu çizgiyi sert bir şekilde yukarı kırdığını görüyoruz. Bu, düşüş trendinin sona ermiş olabileceğine dair en büyük işarettir.
>
> 2. Talep Bölgesi (Yeşil Yatay Kutu)
>    Grafiğin alt kısmında uzanan yeşil şeffaf bölge, alıcıların burası ucuz diyerek beklediği güçlü destek alanıdır. Fiyat bu bölgeye girdiğinde her seferinde destek bulmuş. Dikkat ederseniz, kırılım tam da bu güvenli bölgeden alınan güçle gerçekleşmiş; yani alıcılar dipte maliyetlenip fiyatı yukarı sürmüşler.
>
> 3. Hacim
>    Kırılımın olduğu son mumun altındaki yeşil hacim barı, bu hareketin sahte olmadığını gösteriyor. Teknik analizde Hacimli kırılım, gerçek kırılımdır kuralı burada tam anlamıyla işliyor.
>
> 4. Hareketli Ortalamalar (EMA 5, 8, 13)
>    Mavi, sarı ve pembe çizgiler fiyatın kısa vadeli momentumunu gösterir. Kırılım anında bu üç ortalamanın da yönünü yukarı çevirdiğini ve birbirinden açılarak Boğa Dizilimi oluşturmaya başladığını görüyoruz. Bu, yükseliş hızının artabileceğine dair bir teyittir.
>
> 5. Genel Özet ve Son Mum
>    En sağdaki uzun yeşil mum, fiyatın hem direnci kırdığını hem de o günü en yüksek seviyeye yakın kapattığını gösteriyor.
>
> Özetle bu tablo fiyat dipten desteğini aldı, düşen trendini yıktı, bunu hacimle yaptı ve momentumu arkasına aldı diyor. Teknik olarak bu bir Trend Dönüş sinyalidir.
>
> Pazartesi bakalım ne yapacak bu kardeşimiz.

Görseller:
- G1: SHA-256 `ebb7bd188f6a87b8dcf75152ecb10ba8f920dbf77dc60e44eeaee51406be5998` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-4d9b4287-e212-465b-bf82-70dbbedc2934.jpg` · beyinde VAR: `assets/gorsel-paket-64-dusen-trend-hacim-breakout/01-dusen-trend-talep-hacim-ema-breakout.jpg`

Beyin notu: `gorsel-paket-64-dusen-trend-talep-hacim-ema-breakout.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R125 · 2026-08-28 00:46 UTC · EMA Sıkışması Pre-Signal ve Bir Günde Yüzde 5 Görsel Paketi 65 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Bir günde %5 Ema sıkışması parametrelerin detaylarını verip stratejimi anlatamam ama öz fikri zaten verdim. Siz daha detaylandırabilirsiniz. Pre signal ok ile işaretlenen mum matrix ekranında da soon gün gelen mumu görüyorsunuz.

Görseller:
- G1: SHA-256 `86f1fb08570da2399dae558e3726b89d4a8c871737afca836e035a72fd591989` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-1fe839b2-b668-4149-8b17-d057df091428.png` · beyinde VAR: `assets/gorsel-paket-65-ema-sikisma-pre-signal/01-icbct-ema-sikisma-pre-signal.png`
- G2: SHA-256 `b4823a7b4a9639019446fda029bd878cce4a4b78fbea0cae4ca9d1a0aeff681d` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-2113d273-e715-4f6d-b3eb-ec8acb6145df.png` · beyinde VAR: `assets/gorsel-paket-65-ema-sikisma-pre-signal/02-matrix-sonraki-mum.png`

Beyin notu: `gorsel-paket-65-ema-sikisma-pre-signal-bir-gun-yuzde5.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R126 · 2026-08-28 00:51 UTC · Fibonacci Volume Profile VWAP DMI Delta ve Bir Ayda Yüzde 20 Görsel Paketi 66 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Neden 1 ayda %20 verdi?
>
> Madde madde anlatalım. 8 Ocak 2026'dayız.
>
> 1. Fiyat Hareketleri ve Fibonacci Seviyeleri
>    Fiyat, 2025 Ağustos ayındaki zirvesinden (HH) Ekim ayındaki dip seviyesine (HL) kadar bir düşüş yaşamış, ardından toparlanma sürecine girmiştir.
>
> Fiyat şu anda düşüşün 0.786 düzeltme seviyesine (yaklaşık ₺31.00) ulaşmış durumda. Bu bölge, ana zirveye dönüşten önceki son kritik direnç alanıdır.
>
> Grafik üzerinde mavi yatay çizgiyle gösterilen direnç hattı yukarı yönlü geçilmiş ve fiyat bu bölgenin üzerinde tutunmaya çalışıyor.
>
> 2. Hacim Profili ve VWAP Analizi
>    POC (Point of Control): ₺29.71 seviyesi, analiz edilen dönemde en yoğun işlemin geçtiği maliyet bölgesidir. Fiyatın şu an bu seviyenin üzerinde olması alıcıların kontrolü eline aldığını gösterir.
>
> Value Area (Değer Alanı): Fiyat, VAH (Value Area High - ₺30.24) seviyesinin üzerine çıkarak değer alanının dışına taşmış. Bu durum, hissenin yeni ve daha yüksek bir fiyat bölgesine girmeye çalıştığını işaret eder.
>
> VWAP: Mevcut fiyat (₺31.00), dönem içi ağırlıklı ortalama olan ₺28.00'ın (VWAP) %+10.73 üzerindedir. Bu, trendin momentum kazandığını ancak ortalamadan bir miktar uzaklaştığını gösterir.
>
> 3. Momentum ve Güç Göstergeleri
>    DMI (+DI / -DI): Grafiğin altındaki indikatörlerde yeşil çizginin (+DI) kırmızı çizginin (-DI) üzerine çıktığı ve aradaki farkın açıldığı görülüyor. Bu, boğa (alış) yönlü baskının arttığını teyit eder.
>
> Delta ve Kümülatif Delta: Özellikle Ocak 2026 döneminde yeşil barların (pozitif delta) yoğunlaşması, piyasadaki agresif alıcıların satıcılara baskın geldiğini gösteriyor. Kümülatif delta eğrisinin (sarı alanlı grafik) yukarı yönlü eğimi, para girişinin istikrarlı olduğunu kanıtlıyor.
>
> 4. Özet Teknik Görünüm
>
> Hisse, uzun süreli bir düşüş ve ardından gelen yatay konsolidasyon evresinden sonra yukarı yönlü bir kırılım gerçekleştirmiş görünüyor. Fiyatın ₺30.24 (VAH) üzerinde kalıcı olması, Ağustos zirvesindeki HH seviyesini tekrar test etmek için gerekli zemini hazırlayabilir.
>
> Hacim profili tarafındaki yoğunlaşma (mavi uzun barlar), piyasanın ₺30 civarını güçlü bir destek olarak kabul ettiğini göstermektedir.
>
> Sonuç %20...

Görseller:
- G1: SHA-256 `2cc6e606c72886de225f54d13712f5ccee58f1d42cf269e2f0968a34581e171d` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-e3214dff-9084-4ea8-87b0-85a4b6a93448.png` · beyinde VAR: `assets/gorsel-paket-66-fibo-volume-profile-vwap-delta/01-advanced-market-analysis-8-ocak-2026.png`
- G2: SHA-256 `448c91e97a9973413645877485ecde27600c3fc2b67f10236c193c97850a7b4e` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-dc88b13d-ae41-4887-8860-507b4471481b.png` · beyinde VAR: `assets/gorsel-paket-66-fibo-volume-profile-vwap-delta/02-bir-ay-yuzde20-outcome.png`

Beyin notu: `gorsel-paket-66-fibo-volume-profile-vwap-delta-yuzde20.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R127 · 2026-08-28 00:56 UTC · KRDMD EMA Sıkışma Periyodu Ratio ve Formasyon Confluence Görsel Paketi 67 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Bakın sıkışma zamanlarını iyi tespit eder ve yakalarsanız hele ki bir de o alanda formasyon vs varsa mis gibi kar bırakır. Rasyoyu siz belirleyeceksiniz sıkışma periyodunda sıkışma rasyosu sizin tecrübenize kalmış.

Görseller:
- G1: SHA-256 `89eacde09040186fcb79b39fb27cf9c65a0533c13c44b1f4532437ed0f27cdbb` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-26ebe913-ab85-45de-8b17-57524ab56478.jpg` · beyinde VAR: `assets/gorsel-paket-67-krdmd-ema-sikisma-ratio/01-krdmd-20gun-ema-sikisma-ratio.jpg`

Beyin notu: `gorsel-paket-67-krdmd-ema-sikisma-ratio-formasyon.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R128 · 2026-08-28 01:01 UTC · XU100 EMA 50 100 200 Sıkışması KDE Kırılımı ve Extension Görsel Paketi 68 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Grafiğin orta kısımlarında, özellikle 2026 başına kadar olan süreçte, EMA 50 (mavi), EMA 100 (turuncu) ve EMA 200 (mor) çizgilerinin birbirine çok yaklaştığını ve neredeyse iç içe geçtiğini görüyoruz. Bu alan kısa, orta ve uzun vadeli maliyetlerin birbirine eşitlendiği bir kararsızlık veya denge bölgesidir.  Alıcılar ve satıcılar arasında bir denge vardır. Oynaklık düşmüştür. Bu durum, genellikle büyük bir hareketin habercisidir. Yay ne kadar çok gerilirse, ok o kadar uzağa gider.  Fiyatın 11.300 seviyelerindeki KDE tepe dirençlerini hacimli mumlarla geçmesiyle patlama gerçekleşiyor. Burada asıl dikkat çekici olan, EMAs'ların birbirini keserek yukarı yönlü \*\*"Boğa Dizilimi"\*\*ne girmesidir:  En üstte: EMA 50 Ortada: EMA 100 En altta: EMA 200  Bu dizilim gerçekleştikten sonra trendin momentum kazandığını görüyoruz. EMAs'lar artık birer direnç değil, güçlü birer dinamik destek haline gelmiştir.  Grafiğin en sağ tarafına (14.587 seviyesine) baktığımızda, fiyatın özellikle EMA 50'den (13.310) oldukça uzaklaştığını görüyoruz.  Bu, trendin çok güçlü (parabolik) olduğunu gösterir. Ancak teknik analizde "ortalama geri dönüş" (mean reversion) kuralı gereği, fiyat ortalamalardan çok uzaklaştığında bir soğuma, yatay seyir veya ortalamalara doğru bir "onay" (re-test) hareketi beklenebilir.  En alttaki hacim barlarının son dönemde yükselmiş olması, bu patlamanın sadece fiyatla değil, taze para girişiyle de desteklendiğini kanıtlıyor.  Uzun süreli yatay seyirde biriken emirler, bir yöne doğru kırıldığında (bu grafikte yukarı) short-squeeze ve yeni alıcıların girişiyle hızlanır.  Tüm vadelerdeki yatırımcıların (50, 100, 200 günlük) kâra geçmesi, satış baskısını azaltır ve trendin önünü açar.

Görseller:
- G1: SHA-256 `0b3cc57d2feb18de63998036410bc58d950853c4ad82759c49bd8800b7dffc8d` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-878f1145-2b91-4e59-88b3-24df5ce65d6a.jpg` · beyinde VAR: `assets/gorsel-paket-68-xu100-ema-kde-extension/01-xu100-ema50-100-200-kde-hacim.jpg`

Beyin notu: `gorsel-paket-68-xu100-ema-kde-breakout-extension.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R129 · 2026-08-28 01:06 UTC · PRZMA Bullish FVG Revisit Mitigation OTE ve Alt Zaman CHoCH Görsel Paketi 69 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Şu hissede açıklama da yapalım nedir bu yapı neden dikkat etmeliyiz
>
> Açık yeşil alan (Bullish FVG), teknik analizde ve özellikle Smart Money Concepts (SMC) yaklaşımında kritik bir "mıknatıs" ve "denge" bölgesidir. Fiyatın bu bölgeye geri dönme olasılığını ve bu yapının mantığını aşağıdaki başlıklar altında bİraz detaylandiralim
>
> Bullish FVG (Fair Value Gap) ve Fiyat Hareket Analizi
>
> 1. FVG Neden Bir Mıknatıstır?
>    Grafikte görünen açık yeşil bölge, piyasadaki verimsizliği (imbalance) temsil eder. Fiyat o bölgeden o kadar hızlı ve sert yükselmiş ki, alıcılar ve satıcılar arasında bir denge kurulamamış, emirlerin bir kısmı boşlukta kalmıştır. Algoritmalar ve kurumsal oyuncular, fiyatın adil olmasını ister. Bu boşluklar genellikle fiyatın geri dönüp oradaki likiditeyi alması ve boşluğu onarması  ile kapanır. Kurumsal büyük robotlar genelde bu mantıkla çalışır.
>
> 2. Zirveden Sonra Geri Dönüş Muhtemel mi?
>    Grafiğe baktığımızda, fiyatın son dönemde sert bir yükselişle BOS (Break of Structure) yaptığını ve tüm hareketli ortalamaların (EMA 9, 21, 50, 100, 200) üzerine çıktığını görüyoruz.Fiyat şu an aşırı alım bölgesine doğru ilerliyor olabilir. Bir zirve oluşumundan sonra gerçekleşecek kar realizasyonu, fiyatı doğal bir düzeltme sürecine sokacaktır. Teknik olarak, bu kadar büyük ve belirgin bir FVG'nin tamamen veya kısmen  doldurulması oldukça muhtemeldir. Ancak bu, hemen yarın olacağı anlamına gelmez. Fiyat önce yukarıdaki dirençleri test edip likidite topladıktan sonra bu açık hesabı kapatmak isteyecektir.
>
> Grafikteki yeşil alanın konumu, fiyatın uzun vadeli ana destek bölgesiyle de örtüşüyor.
>
> Eğer fiyat bir zirve yapıp düşüşe geçerse, bu yeşil alan "Optimal Trade Entry" (OTE) dediğimiz en verimli alım bölgesi olacaktır.
>
> Fiyat bu alana geri döndüğünde, alt zaman dilimlerinde (1H veya 4H) bir karakter değişimi (CHoCH) görmeden doğrudan long pozisyon almak riskli olabilir çünkü FVG'ler bazen sadece birer durak değil, fiyatın altına sarkıp altındaki likiditeyi temizlemek istediği yerler de olabilir.
>
> Piyasa doğası gereği boşlukları sevmez dostlar. PRZMA özelinde, 17.70 seviyesindeki mevcut ivme güçlü olsa da, alt bölgedeki o geniş yeşil alan fiyat için bir yerçekimi merkezi görevi görecektir. Özellikle trendin yorulduğu ve hacmin satış tarafına döndüğü noktada, bu FVG bölgesi ilk ana hedef haline gelir.
>
> Fiyatın zirvede oluşturacağı High (H) etiketinin ardından gelen geri çekilmede, FVG'nin üst sınırı olan ilk temas noktası.
>
> Pazartesi alarmlarınızı buna göre planlayın ya da en iyisi siz daha iyi bir analiz yapın bana pek bakmayın.
>
> \#PRZMA

Görseller:
- G1: SHA-256 `0e039a837d589ab20b161f378da23c9a1c9f7366caf8a8e9941fc33586ff1e40` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-52e62ccb-0942-449a-834d-48b36a9b0913.jpg` · beyinde VAR: `assets/gorsel-paket-69-przma-bullish-fvg/01-przma-bullish-fvg-bos-ema.jpg`

Beyin notu: `gorsel-paket-69-przma-bullish-fvg-revisit-ote.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R130 · 2026-08-28 01:11 UTC · Haftalık Gravestone Doji Mezar Taşı Risk ve Teyit Görsel Paketi 70 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> arkanıza bakmadan kaçmanız gereken mum gravestone doji - mezar taşı dojisi. Adamı gömer... haftalık grafikte ise canlı canlı gömer

Görseller:
- G1: SHA-256 `d01f9b91313e0c582f17901931152ddd96ec89edbdbd1d370acaa08d28f3ed51` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-d35a9e29-e92c-4269-8945-ce2bfb6d9f4e.png` · beyinde VAR: `assets/gorsel-paket-70-gravestone-doji/01-haftalik-gravestone-doji.png`

Beyin notu: `gorsel-paket-70-haftalik-gravestone-doji-risk.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R131 · 2026-08-28 01:16 UTC · Hareketli Ortalama Üstü Altı Sade Trend Yön Filtresi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Çok kafa bulandırmaya gerek yok, eğer piyasa hareketli ortalamanın altındaysa, bu durum satış yönlü; hareketli ortalamanın üzerindeyse, alış yönlü işlem yapılması gerektiğini gösterir. Konu bundan ibarettir. Trend is your friend.

Beyin notu: `tweet-hareketli-ortalama-ust-alt-trend-yon-filtresi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı)

### R132 · 2026-08-28 01:20 UTC · Dragonfly Doji EMA Sıkışması ve Yukarı Çıkış Görsel Paketi 71 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Bu grafik ne anlatıyor, dragonfly doji ile bir acayip görüntü var:) Ortalamalar kesişmiş vs vs sıkışma alanından da çıkmış ki ortalamaların sıkışma alanları genelde patlamaya işaret eder.

Görseller:
- G1: SHA-256 `4f31197ce591adb44ff84f184f42c1486838ff29fa1947e8199f5e16eccb04c3` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-704508c4-e25b-40b1-8c04-1bd4b8e9a528.png` · beyinde VAR: `assets/gorsel-paket-71-dragonfly-doji-squeeze/01-dragonfly-doji-ema-sikisma-cikisi.png`

Beyin notu: `gorsel-paket-71-dragonfly-doji-ema-squeeze-exit.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R133 · 2026-08-28 01:25 UTC · Yıllıklandırılmış HBK U Dönüşü Fiyat Konsolidasyonu ve Bilanço Katalizörü Görsel Paketi 72 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Bana kalırsa bu hisse ilk çeyrek bilançosunun açıklanmasını bekliyor. Konsolide olmuş bir görünüm var HBK da artmış, hissenin FK'sı zaten ortalamalarda, güzel bir U dönüş görünüyor ve bu dönüşe fiyatınd a tepkisini her gün görüyoruz.  Bir şirketin bilançosuna baktığınızda milyarlarca liralık borç veya kar görebilirsiniz. Bu rakamlar tek başına size "Bu hisse alınır mı?" sorusunun cevabını vermez. Formüller burada bir tercüman görevi görür. Örneğin; "10 milyar borç çok mu?" sorusuna, "Şirketin kasasındaki nakit bu borcun yarısını bile ödemiyor" cevabını bir oran  sayesinde verirsiniz.  Her şirketin boyutu farklıdır. Çok büyük bir şirketin kârı doğal olarak yüksektir. Ancak formüller (örneğin HBK - Hisse Başı Kar), tüm şirketleri aynı teraziye koymanızı sağlar. Küçük bir şirket olan X ile dev bir holdingi yan yana getirip "Hangisi parasını daha verimli kullanıyor?" sorusuna ancak bu matematiksel oranlarla cevap bulabilirsiniz.  O yüzden HBK evrensel bir cevap sunar.

Görseller:
- G1: SHA-256 `ab22e769ec8cc27e8d12012262039782a36c3463817ee7297769fb8fcec7aa81` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-23a8a5ba-063c-44f6-a124-90024a45124c.png` · beyinde VAR: `assets/gorsel-paket-72-hbk-fiyat-bilanco-katalizoru/01-fiyat-yilliklandirilmis-hbk-u-donusu.png`

Beyin notu: `gorsel-paket-72-hbk-fiyat-bilanco-katalizoru.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R134 · 2026-08-28 01:30 UTC · ASUZU Finansal Borç Büyümesi Kullanım Kalitesi ve Otomotiv Peer Analizi Görsel Paketi 73 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Küçük bir yatırımcı için bilanço tabloları, bir şirketin sağlık raporu gibidir. Örneğin %83,91 gibi yüksek bir borç büyüme oranını tek başına görmek korkutucu olabilir, ancak bu rakamı doğru bağlamda okumak yatırım kararınızı netleştirir.  Peki neler yapabiliriz;  Bizler küçük yatirimcilariz ve bizler İçin bir şirketin borcu neden artargibi soruların cevabı, yatırımın fırsat mı yoksa risk mi olduğunu belirler.  Eğer borç artarken aynı zamanda Maddi Duran Varlıklar kalemi de artıyorsa, şirket kapasite artırıyor veya yeni bir fabrika kuruyor olabilir. Bu, gelecekte daha fazla satış demektir. Ancak borç sadece kısa vadeli yükümlülükleri (maaş, hammadde vb.) ödemek için artıyorsa, bu bir nakit akışı sorununa işaret edebilir.  Borç %84 artarken ciro %100 artıyorsa, bu sağlıklı bir büyümedir. Borç artış hızı, ciro artış hızının çok üzerindeyse borç sarmalı riski doğar.  Şirket kazandığı para (FAVÖK) ile bu borcun faizini rahatça ödeyebiliyor mu? Borç büyümesi kadar, borcun maliyeti ve vadesi de kritiktir.  Türkiye gibi yüksek enflasyonlu ortamlarda, bazen düşük faizle borçlanmak (eğer borç üretken bir alana gidiyorsa) şirket için avantajlı olabilir; çünkü borç reel olarak erir.  Python ile Analiz Yapmanın Faydaları Python kullanmak, binlerce satırlık bilanço verisini saniyeler içinde anlamlı bir stratejiye dönüştürmenizi sağlar  Tek bir şirketi değil, BIST'teki tüm otomotiv sektörünü (ASUZU, FROTO, TOASO vb.) aynı anda kıyaslayabilirsiniz.  Borç büyümesini bir çizgi grafiğinde ciro büyümesiyle üst üste bindirerek "makasın" ne yöne açıldığını anında görebilirsiniz.  Manuel hesaplamalarda sıfırları karıştırma veya yanlış hücreyi seçme riskini ortadan kaldırır.  ASUZU'nun borç büyümesi %83 iken rakiplerinde (FROTO, TOASO) bu oran %20 ise nedenini sorgulayın.  Özkaynak / Borç Dengesi: Borç artarken özkaynaklar yerinde sayıyorsa, şirket fazla risk alıyor demektir.  Nakit Pozisyonu: Şirketin kasasındaki nakit kısa vadeli borçlarını ödemeye yetiyor mu? Bu tür analizler, spekülatif hareketlerden korunmanızı ve şirketin gerçek değerine odaklanmanızı sağlar. Karmaşık tablolara bakarken her zaman şu basit soruyu sorun Bu şirket borç aldığı parayla, borcun maliyetinden daha fazla para kazanabiliyor mu?

Görseller:
- G1: SHA-256 `eb02c6ef48524cdb46485dc52793cf2f41facdf6eff84c9f01b336a64ae37334` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-0853ef6c-bec0-40e8-bb54-8473c32398c3.png` · beyinde VAR: `assets/gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi/01-asuzu-finansal-borc-yoy-sektor.png`
- G2: SHA-256 `04d4dbcf7efd2852ed439d378a77634bd39ae0d5a4fc8eddcf12c0a65aae191e` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-76c7f5ef-910c-42cd-9239-f3e8db599bf6.png` · beyinde VAR: `assets/gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi/02-otomotiv-finansal-borc-yoy-peer-tablosu.png`

Beyin notu: `gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R135 · 2026-08-28 01:34 UTC · ASUZU Finansal Borç Büyümesi Kullanım Kalitesi ve Otomotiv Peer Analizi Görsel Paketi 73 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Hatirlatalim  def borc\_buyume\_hesapla(guncel\_borc, onceki\_borc):     try:         buyume = ((guncel\_borc - onceki\_borc) / onceki\_borc) \* 100         return round(buyume, 2)     except ZeroDivisionError:         return 0  borc\_2025 = 12529195  # TL borc\_2024 = 7279012  # TL  oran = borc\_buyume\_hesapla(borc\_2025, borc\_2024) print(f"Toplam Finansal Borç Büyüme Oranı: %{oran}")

Beyin notu: `gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.18; düşük skorlar elle doğrulandı)

### R136 · 2026-08-28 01:37 UTC · Özel Subplot ile Gizli Pozitif Uyumsuzluk Bağlam Gücü Görsel Paketi 74 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> gizli pozitif uyumsuzlukların gücü tabi nerede baktığınıza bağlı benim grafiğimdeki subplot pek bilinen birşey değil ama uyumsuzluk sinyalleri gayet iyi.

Görseller:
- G1: SHA-256 `e10af0e4e063bd28e812adedd8a814ac184e614b2c5681117432ca4d5a24350d` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-01d8756c-ca35-4d61-8e5c-5da9e43a30e5.png` · beyinde VAR: `assets/gorsel-paket-74-ozel-subplot-hidden-bullish/01-ozel-subplot-gizli-pozitif-uyumsuzluk.png`

Beyin notu: `gorsel-paket-74-ozel-subplot-hidden-bullish.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R137 · 2026-08-28 01:41 UTC · Satışa Kapalı Momentum Teknik Markowitz ve Max Sharpe Karar Destek Pipeline · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Şimdi bazı sorular var özelden gelen
> Bu sistem satılık değil arkadaşlar önce onu belirteyim.
> Sistem nasıl işliyor stratejiyi anlatmadan biraz işleyişi anlatayım
>
> Yatırım sürecini, sadece şansa veya tek bir göstergeye güvenmek yerine, veriyi farklı süzgeçlerden geçirerek rafine eden çok aşamalı bir karar destek mekanizması üzerinde çalışıyorum bir süredir. Yapılanlar şunlar.
>
> 1. Aşama: Momentum ve Sinyal Yakalama
>    Süreç, piyasadaki "hareketlenmeyi" tespit ederek başlıyor. Bir çoğunuzun bildiği yapay sinir ağları ile oluşturduğum bir momentum stratejim var ve bu strateji çıktısında pozitif eğimli ve bu eğimde istediğim filtreyi yapabileceğim bir excel veriyor.
>
> 2. Aşama: Pozitif Eğim ve Görsel Doğrulama (Filtreleme)
>    Sadece bir sinyal oluşması yeterli değil bu sinyalin kalitesini de sorhuluyorum.Yapay sinir ağları yöntemleriyle hem fiyatın hem de oluşan sinyalin eğimi ni kontrol ediyorum. Eğer her ikisi de pozitif bir eğime (yukarı yönlü trende) sahipse, bu durum yükselişin "tesadüfi bir sıçrama" değil, "istikrarlı bir ivme" olduğunu kanıtlıyor. Ayrıca sinyal çizgisinin fiyatın üzerinde seyretmesi, momentumun fiyattan daha hızlı koştuğunu teyit ediyor.
>
> 3. Aşama: Teknik Onay (Mum Formasyonları ve İndikatörler)
>    Trendin gücü, ADX ve Para Akışı (CMF) gibi indikatörlerle ölçülüyor. Buna ek olarak, "Çekiç" veya "Sabah Yıldızı" gibi bullish (boğa) mum formasyonları aranarak, yatırımcı psikolojisinin de o hissede alım yönünde birleştiği noktalar tespit ediliyor. Bu, matematiksel modelin üzerine görsel bir "onay" katmanı ekliyor.
>
> 4. Aşama: Markowitz Portföy Optimizasyonu (Risk Yönetimi)
>    Taramadan geçen başarılı hisseler arasından rastgele seçim yapmak yerine, bu hisselerin birbirleriyle olan ilişkileri (korelasyonları) ve risk değerleri analiz ediliyor. Modern Portföy Teorisi (Markowitz) kullanılarak, bu hisseler en verimli şekilde bir araya getiriliyor.
>
> 5. Aşama: Maksimum Sharpe Seçimi (Final Kararı)
>    Optimizasyonun sonucunda hedef, "en çok kazandıran" hisseyi değil, "bir birim risk başına en yüksek getiriyi sunan" (Maximum Sharpe Ratio) kombinasyonu bulmak oluyor. Bu sayede portföy, piyasadaki volatiliteye karşı daha dayanıklı hale gelirken, kazanç potansiyeli en optimize seviyeye çekiliyor.
>
> Yani  kimler koşmaya hazır, hangileri doğru yöne bakıyor, diye eliyoruz ve son aşamada bu atletlerden en dengeli takımı nasıl kurarım sorusuna yanıt vererek bilimsel bir yatırım planı oluşturuyoruz.
>
> Sistem böyle işliyor. Benzer bir sistem kurmanızı tavsiye ederim.

Beyin notu: `tweet-satilik-degil-momentum-teknik-markowitz-max-sharpe-pipeline.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.21; düşük skorlar elle doğrulandı)

### R138 · 2026-08-28 01:46 UTC · ISCTR A/D EMA Walk-Forward Sakin Getiri Yolu ve Drawdown Görsel Paketi 75 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> piyasada Haklı çıkmak bir ego tatminidir, ancak sermayeyi korumak bir hayatta kalma becerisidir. Sharpe oranı her ne kadar akademik bir başarı göstergesi olsa da, geceleri huzurlu uyumanızı sağlayan şey Sharpe değil, kümülatif getiri grafiğindeki o sakinliktir. Bu sizi uykusuz kalmaktan korur
>
> Görseldeki veriler üzerinden, bu temkinli ama istikrarlı yaklaşımın grafiğe nasıl yansıdığını birlikte inceleyelimç
>
> 1. Kümülatif Getiri: "Rollercoaster" vs "Merdiven"
>    Grafikteki yeşil çizgi (Strateji) ile gri kesikli çizgi (Buy & Hold - Al ve Tut) arasındaki fark önemli. Gri çizginin sert bir şekilde çakıldığı (piyasanın çöktüğü) orta bölgeye dikkat edin. O noktada yeşil çizgi yatay (flat) kalmış. Yani stratejiniz, piyasa kan ağlarken sizi nakitte tutarak sermayenizi bir kalkan gibi korumuş. Al-Tut yapan bir yatırımcı sermayesinin %30-40 erimesini izleyip "elbet döner" diye umut ederken, bu strateji size "ben dışarıdayım, fırtınanın dinmesini bekliyorum" konforunu sunmuş.
>
> Strateji %19.1 getiri sağlarken, piyasada kalan kişi sadece %10.8 kazanabilmiş. Üstelik strateji bu getiriyi çok daha az sarsıntı ile yapmış.
>
> 2. Strateji Drawdown (Sermaye Erimesi) Analizi
>    En alttaki kırmızı alan, bu stratejinin asıl gücünü gösteriyorç.Drawdown grafiğine baktığımızda, düşüşlerin genellikle -%10 ile -%15 bandında sınırlandığını görüyoruz.
>
> Piyasanın genel düşüş dalgalarında strateji nakde geçtiği için, kırmızı alan derinleşmiyor. Sermayenizi koruduğunuz için piyasa tekrar döndüğünde "zararı çıkarma" derdine düşmüyorsunuz; doğrudan kâr hanenizi büyütmeye başlıyorsunuz.
>
> Grafikteki kümülatif getirinin yatay çizgilerle ilerlediği o uzun dönemler aslında stratejinin en kritik kararlarını temsil eder. Birçok amatör yatırımcı "hiç işlem yapmıyorum, param boşa duruyor" diye paniklerken, bu grafik İşlem yapmamak da bir işlemdir ve bazen en kârlı olanıdır diyor aslında
>
> Sharpe 0.67
> Evet, 0.67 Sharpe oranı çok iddialı görünmeyebilir; ancak bu rakam, stratejinin aşırı risk almadan elde ettiği bir başarıdır. Piyasada yüksek Sharpe ile uçan modellerin genellikle ilk sert virajda (drawdown) patladığını görürüz. Sizin grafiğiniz ise "yavaş ama kararlı" olanın yarışı kazandığını kanıtlıyor.
>
> Özetle bu grafik, piyasanın gürültüsünden kaçıp sadece belirgin trendleri (AD > EMA) toplamanın hikayesidir. Gri çizginin (B&H) her zirvesini yakalayamamış olabilirsiniz ama onun her çukuruna da düşmediniz. Uzun vadede zengin eden şey büyük kârlar değil, bu tür küçük ve kontrollü kayıplardır.
>
> EMA değeri walk forward le optimzie edilerek model oluşturulmuştur.

Görseller:
- G1: SHA-256 `5ebc29a5efb27f40312f1cad2ab9293fb93544a074980658580b0357de48291b` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-efa592ff-f82a-4f25-9ae3-0c0601576714.jpg` · beyinde VAR: `assets/gorsel-paket-75-isctr-ad-ema-walk-forward/01-isctr-ad-ema-strateji-bh-drawdown.jpg`

Beyin notu: `gorsel-paket-75-isctr-ad-ema-walk-forward.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R139 · 2026-08-28 01:50 UTC · ISCTR A/D EMA Walk-Forward Sakin Getiri Yolu ve Drawdown Görsel Paketi 75 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Enter long: AD() Ref(Mov(AD(),opt1,E), 1)  Close long: AD() Ref(Mov(AD(),opt1,E), 1)  Enter short: AD() Ref(Mov(AD(),opt1,E), 1) Close short: AD() Ref(Mov(AD(),opt1,E), 1)  OPT1 Current value: 3 Çatır çutur girip çıkmak için, 1-2 gün

Beyin notu: `gorsel-paket-75-isctr-ad-ema-walk-forward.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.22; düşük skorlar elle doğrulandı)

### R140 · 2026-08-28 01:55 UTC · Teknik İndikatör ve İşlem Sistemlerini Değerlendirme Kriterleri · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Dursun bir kenarda lazim olur  Teknik Piyasa İndikatörleri ve İşlem Sistemlerini Değerlendirme Kriterleri  Kazanma Oranı ve Yanılgılar Yüzdelik doğruluk (kârlı işlemlerin toplam işlemlere oranı), acemi yatırımcıların bir takıntısıdır ancak bir işlem sistemini değerlendirmek için çok önemli bir kriter değildir. Oldukça etkili bazı teknik zamanlama modelleri, haklı olduklarından daha sık yanılabilirler; buna karşın bazı marjinal (zayıf) modeller, yanıldıklarından daha sık haklı çıkabilirler.  Temel Performans Ölçütü: Ödül/Risk Oranı Bir sistemin temel performans ölçütü, toplam net kârın maksimum sermaye erimesine oranıdır bu aynı zamanda ödül/risk oranı olarak da bilinir.  Maksimum sermaye erimesi, bir stratejinin pratik olarak uygulanabilirliğini belirler. Sonunda toplam kâr yüksek olsa bile, büyük kayıplara (düşüşlere) neden olan bir model pratik değildir.  Maksimum Sermaye Erimesi (Drawdown) Nedir? Maksimum sermaye erimesi, sermayenin gördüğü en yüksek noktadan (zirve), en düşük noktaya (dip) kadar yaşadığı genel düşüş trendidir.  Maksimum sermaye erimesi sadece peş peşe gelen zarar eden işlemlerin toplam kaybı değildir; çünkü kötü bir performans dönemi küçük bir kârla bölünebilir, ancak ardından net sermaye trendinin daha da düşük bir seviyeye gerilemesiyle düşüş devam edebilir.  Kümülatif Sermaye Eğrisinin Önemi Ödül ve risk dengesini kavramanın en iyi ve en basit yolu, Kümülatif Sermaye grafiğini görsel olarak incelemektir. Büyük sermaye erimeleri bir grafik üzerinde çok net bir şekilde görülür.  Eğer bu erimeler diğer indikatörlerin erimeleriyle karşılaştırıldığında şiddetliyse, o işlem sistemini bir kenara bırakmalı ve alternatif bir strateji seçmelisiniz.  Basitlik En İyi Tavsiyedir Bazıları aşırı karmaşık istatistiksel manipülasyonlar içeren birçok başka performans ölçütü mevcuttur; ancak bunlar bize Kümülatif Sermaye grafiği kadar çok şey anlatmaz. Basit tut hala verilebilecek en iyi tavsiyedir.

Beyin notu: `tweet-teknik-indikator-islem-sistemi-degerlendirme-kriterleri.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.18; düşük skorlar elle doğrulandı)

### R141 · 2026-08-28 01:59 UTC · Awesome Econ AI Stuff Ekonomistler İçin AI Skills Kaynak İncelemesi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Ekonomistler ve akademi dünyası için harika bir açık kaynak projesi: "Awesome Econ AI Stuff".  Literatür taramasından API ile veri çekmeye, Python, R ve Stata'da ekonometrik modellemeden LaTeX'te yayın formatında makale yazımına kadar tüm araştırma iş akışınızı otomatize eden hazır yapay zeka şablonları (AI skills) sunuyor.  [https://t.co/c91teWyDZs](https://t.co/c91teWyDZs)

Beyin notu: `kaynak-awesome-econ-ai-stuff.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.26; düşük skorlar elle doğrulandı)

### R142 · 2026-08-28 02:06 UTC · Hangi Soru Hangi Yöntemi Çağırır Ekonometri Yöntem Haritası · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Yöntem seçiminde çoğu tartışma ‘hangi yöntem daha iyi’ diye başlıyor.   Daha verimli soru şu: elimdeki soru hangi yöntem ailesini çağırıyor? 13 blok, 81 soruluk bir harita çıkardım.  Dördünü tek karede birleştiren tam sürüm PDF burada:

Beyin notu: `kaynak-ekonometri-hangi-soru-hangi-yontem-haritasi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı)

### R143 · 2026-08-28 02:14 UTC · OHLC Mum Geometrisi ve Formasyon Dedektör Motoru Görsel Paketi 76 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Bir mum çubuğu dört temel veriden oluşur. Açılış (Open), Kapanış (Close), En Yüksek (High) ve En Düşük (Low).  Upper Shadow (Üst Gölge): Mumun gövdesinin (açılış ve kapanış arasındaki alan) üstünde kalan iğne kısmıdır. Piyasanın o süreçte gördüğü en yüksek seviye ile gövdenin tepe noktası arasındaki mesafeyi ölçer.  Lower Shadow (Alt Gölge): Mumun gövdesinin altında kalan iğne kısmıdır. Piyasanın gördüğü en düşük seviye ile gövdenin dip noktası arasındaki mesafeyi ölçer.   Aşağıdaki kodu kullan geliştir formasyonları tanımla vs vs

Görseller:
- G1: SHA-256 `e372c274d05a19c09dffba983a869d56be3470d6475ecbabdf1ec882b9ad57dd` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-c2a42b89-598c-4aba-8387-20f456c01587.png` · beyinde VAR: `assets/gorsel-paket-76-mum-geometri-motoru/01-python-ohlc-golge-analizi.png`

Beyin notu: `gorsel-paket-76-mum-geometri-formasyon-motoru.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R144 · 2026-08-28 02:24 UTC · PD DD ROE Sektör Tarihsel Bant ve Değer Tuzağı Filtresi · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> PD/DD (Piyasa Değeri / Defter Değeri) oranı şirketin özkaynaklarını ne kadar verimli kullandığını gösteren bir sağlamlık filtresi olarak kullanmak en sağlıklı yaklaşımdır.
>
> Peki neden?
>
> Bir hissenin PD/DD oranı sadece şu üç veriyle yan yana geldiğinde anlam kazanır.
>
> Sektör Ortalaması: Sektörün 2.5 olduğu yerde 1.0 olan bir hisse "görece" ucuzdur.
>
> Tarihsel Ortalamalar: Şirket son 36 çeyrekte (uzun dönem) genelde hangi PD/DD bandında fiyatlanmış? Eğer tarihsel ortalaması 2.0 ise ve şu an 0.90 ise ciddi bir iskonto olabilir.
>
> Özkaynak Karlılığı (ROE): En kritik nokta burasıdır. PD/DD'nin yüksek olması her zaman "pahalı" demek değildir. Eğer şirket özkaynaklarını %80 karlılıkla çeviriyorsa, piyasanın ona yüksek bir prim (yüksek PD/DD) vermesi normaldir.
>
> 2. "Değer Tuzağı"ndan (Value Trap) Kaçınma
>    Sadece "PD/DD oranı 1'in altında, o halde bu hisse bedava" diyerek alım yapmak büyük bir hatadır.
>
> Eğer şirketin özkaynakları eriyorsa,sürekli zarar ediyorsa,v arlıkları nakde dönmekte zorlanıyorsa, PD/DD oranının düşük kalması ucuzluktan değil, piyasanın o şirkete güvenmemesinden kaynaklanır. Buna "değer tuzağı" denir.
>
> 3. Sektörel Uyumluluk: PD/DD her sektörde aynı ağırlıkta çalışmaz.
>
> Sanayi ve Finans (Banka): Duran varlıklar ve özkaynaklar işin kalbi olduğu için PD/DD altın standarttır.
>
> Teknoloji ve Yazılım: Bu şirketlerin en büyük varlığı "insan kaynağı" ve "patentler"dir, bunlar bilançoda tam görünmez. Bu yüzden teknoloji hisselerinde PD/DD genellikle çok yüksek çıkar ve yanıltıcı olabilir.
>
> Özet Strateji Reçetesi
>
> Düşük PD/DD + Yüksek Özkaynak Karlılığı + Sektör Altı Çarpan = Potansiyel Yıldız.
>
> Bu stratejiyi uygularken, rneğin 36 çeyreklik (uzun dönem) ortalamayı bir "çıpa" noktası olarak alıp, güncel PD/DD bu çıpanın altına indiğinde diğer temel verileri (kar büyümesi vb.) kontrol etmek en profesyonel yaklaşımdır.
>
> Aşağıda konu sadece örnek olarak verilmiştir.
>
> python kodlamasıdır.

Beyin notu: `tweet-pddd-roe-sektor-tarihsel-value-trap-filtresi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı)

### R145 · 2026-08-28 02:29 UTC · TOPSIS Çok Kriterli Hisse Sıralama ve Ağırlık Hassasiyeti Motoru · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Topsis analizinin deneysel sonuçları inanılmaz. İndikatör cart curt hikaye. Topsis yapın.

Beyin notu: `tweet-topsis-cok-kriterli-hisse-siralama-motoru.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı)

### R146 · 2026-08-28 02:36 UTC · Dokuz Aylık Veriden Yıl Sonu Satış ve Net Kâr Tahmini · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Hap bilgi olsun Sene ortasındasınız En basit hali ile tahmini kar nasıl bulursunuz  Örnek 2023/9 verisi geldi ve 2023/12 tahmini kar bulmak istiyorsunuz 2023 büyüme oranınız %188 (rakamları tamamen atıyorum)  full\_year\_beklenti = onceki\_yil\_satis(2022/12) × (1 + 1.88)  = onceki\_yıl × 2.88  ytd\_satis = 2023/3 çeyrek + 2023/6 çeyrek + 2023/9 çeyrek (kümülatif veri)  kalan\_donem\_satis = full\_year\_beklenti - ytd\_satis = (önceki yıl × 2.88) - gerçekleşen 9 ay  tahmini\_net\_kar = kalan\_donem\_satis × NET\_KAR\_MARJI + ytd\_net\_kar   = (kalan 1 çeyrek tahmini satış × marj) + gerçekleşen 9 ay net kar

Beyin notu: `tweet-9aydan-yilsonu-satis-net-kar-tahmini.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.22; düşük skorlar elle doğrulandı)

### R147 · 2026-08-28 02:39 UTC · ASUZU Bottom-Up Adet Ciro Marj F K ve FD FAVÖK Değerleme Görsel Paketi 77 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> ahmini net kar nereden geldi kardeşim nasıl emin oluyorsun bundan dediğinizi duyuyorum. Bu sistemin tutarlılığı için kilit bir husus.
>
> Şirket Değerlemesinde Adet Bazlı Analiz ve Çarpan Yaklaşımı burada önem arzeder. Finansal modelleme ve değerleme süreçlerinde, gelecekteki fiyatlamayı doğru yapabilmenin en temel koşulu, şirketin operasyonel gerçekliklerini tahminlere doğru yansıtabilmektir. Modeller, sığ ve yanıltıcı olabilen salt enflasyonist ciro büyümelerini baz almak yerine, doğrudan şirketin faaliyet hacmine (adet/ton) inen "aşağıdan yukarıya" (bottom-up) bir sistem mimarisi ile oluşturulmalıdır.
>
> 1. Net Kar Tahmininde Adet Bazlı (Hacimsel) Analizin Önemi: Özellikle enflasyonist ortamlarda veya kur volatilitesinin yüksek olduğu ekonomilerde, geçmiş TL cirolarını belirli bir yüzdeyle büyüterek kar tahmini yapmak ciddi sapmalara yol açar. Adet bazlı analiz bu noktada modelin omurgasını oluşturur.
>
> Gerçek Büyümenin İzolasyonu: Kurduğum modelde 2019'dan bu yana izlenen ve 2024 yılı için öngörülen xxxx adetlik satış tahmini, fiyat artışlarından veya kur şoklarından arındırılmış saf operasyonel büyümeyi ve pazar talebini temsil eder.
>
> Dinamik Ciro Projeksiyonu: Sadece geçmiş ciroya bakmak yerine tahmini Adet $ x Ortalama Birim Fiyat (USD) Dönemsel Kur Beklentileri şeklinde ilerleyen algoritma, makroekonomik beklentilerin şirket bilançosuna nasıl yansıyacağını simüle eder.
>
> Net Kar İçin Sağlam Temel: Net kar, havadan gelen bir rakam değildir; cironun bir türevidir. 2024 tahmini toplam satış rakamının hacimsel (adet) bazda kanıtlanmış olması, bu rakam üzerinden hesaplanacak net kar tahmininin güvenilirliğini maksimize eder.
>
> 2. Kodda Satış Adetleri ve Marjlardan Çarpanlara (F/K ve FD/FAVÖK) Uzanan Sistem Mimarisi değerleme kısmında kurulan sistem, operasyonel beklentileri (satış adedi) doğrudan piyasa fiyatlamasına (hisse fiyatı) bağlayan nedensel bir zincir üzerine inşa edilmiştir.
>
> F/K Çarpanı ile Entegre Kar Yaklaşımı, Model, F/K bazlı değerlemeyi yaparken piyasanın sıklıkla düştüğü "geçmiş net karı çarpanla çarpma" hatasına düşmüyor. Görselde işaretli olan 3.029.079.975 TL'lik Tahmini Net Kar (Yıllık) rakamı, tamamen en baştaki adet bazlı satış projeksiyonunun bir sonucudur.
>
> Sistem çalışma mantığı şöyledir: Adet bazlı hesaplanan cari yıl satış gelirine şirket beklentisi olan Net Kar Marjı uygulanır. Elde edilen operasyonel destekli bu taze net kar rakamı, belirlenen F/K çarpanı (10.00x) ile değerlendirilerek 120.20 TL hedef fiyata ulaşılır.
>
> FD/FAVÖK ve Marj Odaklı Yaklaşım? Aynı sistem mimarisi FD/FAVÖK (EV/EBITDA) için de geçerlidir. Adet bazlı ciro tahmin havuzuna bu kez şirketin operasyonel nakit yaratma gücünü yansıtan %6.0 FAVÖK Marjı uygulanır. Buradan elde edilen \~2.019 Milyar TL'lik FAVÖK, 16.00x çarpanı ile firma değerine (Firma Değeri = Piyasa Değeri + Net Borç) dönüştürülür ve net borç düşüldükten sonra 119.28 TL hedef fiyatı verir.
>
> Özetle Sistem Yaklaşımı: Bu model; "Ne kadar satar?" (Adet)# "Hangi fiyattan ve kurdan satar?" (Ciro) # "Operasyonel verimliliği nedir?" (Marjlar),  "Piyasa bunu nasıl fiyatlar?" (Çarpanlar) akışını kurgulayarak, şirketin fiziki gerçekliklerinden (satılan ürün sayısından) hisse başına düşen TL değerine kadar kesintisiz, güncellenebilir bir değerleme algoritması yaratmıştır.
>
> Daha önceden de bahsettiğim gibi INA, Çarpanlar değerleme sisteminin bir ayağıdır.

Görseller:
- G1: SHA-256 `d582aedeaf70d83eb36028d98c2e5729534090b98a301f2c0f18b4e98a5db668` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-058ed80a-a82e-4c69-b6f8-0b2111746086.png` · beyinde VAR: `assets/gorsel-paket-77-asuzu-bottom-up-adet-degerleme/01-asuzu-adet-ciro-marj-fk-fdfavok.png`

Beyin notu: `gorsel-paket-77-asuzu-bottom-up-adet-degerleme.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R148 · 2026-08-28 02:45 UTC · HalfTrend Buy ve Momentum Threshold Çift Kapılı Long Adayı · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> if (half\_trend[t] == 'buy' and momentum[t] > momentum\_threshold)  Nice

Beyin notu: `tweet-halftrend-buy-momentum-threshold-kapisi.md` — dayanak: konu eşleşmesi (TF-IDF kosinüs 0.20; düşük skorlar elle doğrulandı)

### R149 · 2026-08-28 02:48 UTC · PETKM Talep Arz Fibo EMA ve Hacim Confluence Görsel Paketi 78 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> confluence alanının gücü...

Görseller:
- G1: SHA-256 `bae37c3568516bbeb182e83db6ad0e32ffef5012b574f1b16148eea77907b08a` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-bd93314f-d57e-484e-a4c5-4f2f21ac3b8e.png` · beyinde VAR: `assets/gorsel-paket-78-petkm-confluence-talep-arz/01-petkm-talep-arz-fibo-ema-hacim.png`

Beyin notu: `gorsel-paket-78-petkm-confluence-talep-arz.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R150 · 2026-08-28 02:52 UTC · ARCLK Ara Dönem Marjları Manual Override F K ve FD FAVÖK Görsel Paketi 79 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Finansal değerlemelerde tahmin sapmalarını minimize etmek için ara dönem raporlarının gücünü göz ardı etmeyiniz.  Değerli dostlar, bugün algoritmik değerleme modellerimizde ve temel analiz çalışmalarımızda sıkça karşılaştığımız çok kritik bir konuya, tahminlerimiz ile piyasada gerçekleşen sonuçlar arasındaki sapmaları nasıl en aza indirebileceğimize değinmek istiyorum.  Bildiğiniz gibi, Fiyat/Kazanç (F/K) veya Firma Değeri/FAVÖK gibi çarpan modelleri kurarken işin matematiği aslında oldukça basittir. Zor olan ve modeli başarıya götüren asıl kısım, formüle koyacağımız "Tahmini Yıllık Net Kar" ve "Tahmini FAVÖK" rakamlarını doğru öngörebilmektir. Çoğu zaman geçmiş yılın tam kapanış verilerinin üzerine sabit bir büyüme oranı eklemek veya geçen yılın kar marjlarını doğrudan kopyalamak gibi pratik ama tehlikeli yollara sapılabiliyor. Ancak makroekonomik dinamikler, döviz kurlarındaki dalgalanmalar veya sektörel daralmalar yıldan yıla, hatta çeyrekten çeyreğe büyük değişimler gösterebiliyor. Yıllık net kar ve tahmini favök kod tarafından hesaplanabileceği gibi şirketin verileri ile de hareket edebilmek tutarlılık açısıdnan önemli olabilir. O nedenle koda manuel giriş sseçeneği de koydum.  İşte tam bu noktada, şirketlerin cari dönem içindeki ara raporlarını  modelimize entegre etmek hayati bir önem taşıyor. Tahmini FAVÖK ve Net Kar rakamlarını sadece geçmiş yılın iyimserliğinden veya kör bir büyüme beklentisinden almak yerine, şirketin o yıl içinde fiilen ürettiği güncel çeyreklik marjları baz aldığımızda, değerleme modelimizdeki hata payı dramatik bir şekilde düşmektedir.  Bunun temel sebebi oldukça nettir. Bir şirketin operasyonel maliyetlerindeki artış, fiyatlama gücündeki güncel durum veya artan faiz ortamındaki finansman yükü, en şeffaf haliyle en son açıklanan cari ara bilançolarda kendini gösterir. Kodlama mimarimizde sene ortası analizi yaparken ilk yarının gerçekleşen FAVÖK marjını bizzat sahadan, yani son rapordan çekip, kalan dönemi bu güncel gerçeklik üzerinden projekte etmek, takvim yılı başında öngörülen farazi bir büyüme hedefinden çok daha rasyonel sonuçlar verir. Şirket yönetimlerinin paylaştığı ileriye dönük beklentiler (guidance) ve güncel çeyreklik performans, geleceği aydınlatan en güçlü fenerdir.  Özetle, kantitatif modellerimizin ve Python ile inşa ettiğimiz değerleme algoritmalarımızın gücü, sadece yazdığımız fonksiyonlardan değil, içeri beslediğimiz verinin gerçeğe ne kadar yakın olduğundan gelir. Tahminlerimizi şirketlerin en son ara dönem raporlarındaki taze finansal eğilimlere ve reel marjlara çıpalarsak, piyasa gerçeklerinden kopmadan, çok daha isabetli hedef fiyatlar ve rasyonel yatırım stratejileri üretebiliriz. Unutulmamalıdır ki en başarılı sistemler, sadece geçmişi ezberleyenler değil, güncel verinin ritmine ayak uydurabilenlerdir.  Tutarlılığını kontrol etmek için xxcelde eski yaptığım değerlemeleri koda döküyorum. 2023 yılında [#ARCLK](https://x.com/hashtag/ARCLK?src=hashtag_click) hissesinin bu değerlere ulaştığını ve sonra fiyatın geri geldiğini göreceksiniz.

Görseller:
- G1: SHA-256 `9816f4d473792eba11e4e89abf1b6a8fc7553efddd44c76ce56d5bb627e5d0d8` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-34f04ee0-5e9f-4be7-8991-aa1a8afc728f.png` · beyinde VAR: `assets/gorsel-paket-79-arclk-aradonem-manuel-degerleme/01-arclk-2023-6-fk-fdfavok-manuel.png`

Beyin notu: `gorsel-paket-79-arclk-aradonem-manuel-degerleme.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R151 · 2026-08-28 02:59 UTC · FROTO Basit F K ve FD FAVÖK Değerleme Görsel Paketi 80 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Python ile şirket değerleme çalışmalarında, BASİT METOD İLE FK VE FD/FAVÖK üzerinden hesaplanan çalışmanın kodlaması tamamlandı.  Kısaca anlatalım  Kod, karmaşık finansal formülleri otomatize ederek iki değerleme yöntemini kullanır  FK (Fiyat/Kazanç) ve FD/FAVÖK (Firma Değeri/FAVÖK). Temel mantık "Şirketin geçmişteki karlılık ve satış performansına bak, geleceğe yönelik bir büyüme senaryosu çiz ve şirketin sektördeki çarpanlarına göre adil değerini (olması gereken fiyatını) hesapla."  Tahmin yapabilmek için beklentiler sisteme girilir. Örneğin; şirketin satışlarının %100 büyüyeceği, net kar marjının %10 olacağı gibi parametreler kodun en başında tanımlanmıştır. Bunları da temel analiz kodlarımızın çıktılarından alıyoruz.  FK (Fiyat/Kazanç) Çarpanı ile Değerleme Bu bölüm, "Şirket ne kadar kar ediyor ve yatırımcılar bu karın kaç katını ödemeye razı?" sorusuna cevap arar.  Gelecekteki Satışların Bulunması: Şirketin bir önceki yıl yaptığı toplam satış gelirleri alınır ve beklenen büyüme oranıyla (örneğin %100 büyüyerek 2 katına çıkacağı varsayımıyla) çarpılır. Böylece "Cari Yıl Satış Beklentisi" bulunur.  Tahmini Karın Hesaplanması: Satışların ne kadarının şirketin cebine kar olarak kalacağını bulmak için belirlenen %10'luk "Net Kar Marjı" kullanılır. Beklenen satışlar bu marj ile çarpılarak Tahmini Net Kar elde edilir.  Şirketin Toplam Değerinin Bulunması: Kod, manuel olarak girilen (4.33x) FK çarpanını kullanır. Burada kodumuz bunu kendisi de hesaplıyor, fakat manuel giriş seçeneği de yazdım. Tahmini net kar, bu FK çarpanı ile çarpıldığında şirketin toplam piyasa değeri (Firma Değeri) ortaya çıkar. (Eğer manuel girilmeseydi, kod geçmiş karlara ve geçmiş hisse fiyatına bakarak otomatik bir FK hesaplayacaktı).  Hisse Başına Fiyat: Bulunan bu toplam değer, piyasadaki toplam hisse senedi sayısına (Ödenmiş Sermaye) bölünerek, FK yöntemine göre 1 adet hissenin olması gereken fiyatı bulunur.  FD/FAVÖK Çarpanı ile Değerleme Bu yöntem sadece net kara değil, şirketin esas işinden ne kadar nakit ürettiğine (FAVÖK - Faiz, Amortisman ve Vergi Öncesi Kar) ve borç/nakit durumuna odaklanır. Yabancı yatırımcıların ve şirket satın almalarının en çok kullandığı yöntemdir.  Tahmini FAVÖK'ün Bulunması: Kod öncelikle şirketin geçmiş bilançosuna bakarak satışların yüzde kaçını FAVÖK'e dönüştürebildiğini (FAVÖK Marjı) bulur. Sonra bu marjı, yukarıda tahmin edilen "gelecek yılın satış beklentisi" ile çarparak Tahmini FAVÖK rakamını oluşturur.  Brüt Firma Değeri: Belirlenen FD/FAVÖK çarpanı Tahmini FAVÖK ile çarpılarak şirketin operasyonel büyüklüğü olan Firma Değeri bulunur.  Borçların ve Nakitlerin Hesaba Katılması (Net Borç): Bir şirketi satın aldığını düşün; şirketin kasasındaki nakitler senin olurken, banka borçlarını da sen üstlenirsin. Kod, bilançodan "Kısa/Uzun Vadeli Borçları" toplar ve şirketin kasasındaki "Nakit ve Finansal Yatırımları" bundan çıkararak Net Borç durumunu bulur.  Piyasa Değerine Geçiş: Bulunan operasyonel Firma Değerinden, bu Net Borç miktarı düşülür. Kalan rakam, şirketin borsadaki Piyasa Değeridir.  Hisse Başına Fiyat: Tıpkı ilk yöntemde olduğu gibi, bu piyasa değeri şirketin toplam hisse adedine (Ödenmiş Sermayeye) bölünür ve FD/FAVÖK yöntemine göre ikinci hisse fiyatı tahmini  elde edilir.  Kod matematiği bitirdikten sonra işin en keyifli kısmına, yani sentezleme ve sunum aşamasına geçer.  Ortalama Hedef Fiyat: FK yöntemi biraz daha muhafazakar (796 TL), FD/FAVÖK yöntemi ise şirketin borç/nakit yapısını kattığı için daha yüksek (1441 TL) bir sonuç vermiştir. Kod bu iki değerin ortalamasını alarak sene sonu için 1118.85 TL'lik bir hedef fiyat belirler.  Potansiyel Hesabı: Girilen güncel fiyat (800 TL) ile hedef fiyat (1118 TL) arasındaki fark hesaplanır. Bu senaryoda hissenin %39.9 oranında yükseliş potansiyeli taşıdığı sonucuna varılır.  Bu yöntem basit çarpan yöntemidir.  Sistemin ikinci ayağının ikinci aşaması ise FK , PD/DD , fd/FAVÖK ile kısa uzun ve sektör ortalama değerlerini hesaba katan değerlemedir.  En so aşamada ise İNA'sonucunun %40'ı, basit çarpan değerlemesi ve detaylı çarpan değerlemesinin ortalamasının %60'ı alınarak sapmalar minimize edilir.

Görseller:
- G1: SHA-256 `d716c2565194c6e7fb8570b9a52faa5cba740ba5bf54ad0ade9e1a8e4fc5a5df` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-0c44a269-69c9-4dfd-b844-5a76ead21f2f.png` · beyinde VAR: `assets/gorsel-paket-80-froto-basit-fk-fdfavok-degerleme/01-froto-2023-basit-fk-fdfavok-degerleme.png`

Beyin notu: `gorsel-paket-80-froto-basit-fk-fdfavok-degerleme.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R152 · 2026-08-28 03:07 UTC · FROTO Beş Adımlı Basit F K İleri Hedef ve 2023 Outcome Görsel Paketi 81 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Şimdi çarpanla rile değerleme sistemimizin ilk adımı basit çalışmalar olacak ki bu daha karmaşık sistemlerin temelleri. Buralardan bazı verileri alacağız farklı yerlerde kullanacağız.
>
> Kısaca yazdığım Python kodu, temel analizde sıkça kullanılan Çarpanlara Göre İleriye Dönük Hedef Fiyat modellemesini gerçekleştiren bir sistem. Temel amacı şirketin geçmiş satış verilerinden yola çıkarak gelecekteki olası büyümesini, kârlılığını ve piyasanın bu kâra biçeceği değeri tahmin ediyor.
>
> Sistem kavramsal olarak şu 5 mantıksal adımı takip etmekte.
>
> 1. Geçmiş Satışların Tespiti (Baz Alınan Nokta):
>    Sistem işe ilk olarak, değerlemesi yapılacak yılın bir önceki yıl sonu (12 aylık) bilançosuna giderek başlar. Şirketin o yıl ne kadar toplam ciro (satış geliri) elde ettiğini bulur. Bu rakam, geleceği inşa etmek için kullanılan temel taştır.
>
> 2. Gelecek Ciro Beklentisinin Hesaplanması (Büyüme):
>    Geçmişte elde edilen satış geliri, sizin belirlediğiniz bir Büyüme Oranı beklentisiyle genişletilir. Örneğin, şirket geçen yıl 100 milyon TL ciro yaptıysa ve %100 büyüme (büyüme = 1) öngörüyorsanız, cari yıl için 200 milyon TL'lik bir ciro hedefi oluşturulur.
>
> 3. Tahmini Net Kârın Bulunması (Kârlılık):
>    Şirketin çok satış yapması tek başına yeterli değildir; önemli olan şirket kasasına ne kadar para kaldığıdır. Sistem, hesapladığı yeni ciro beklentisini sizin belirlediğiniz "Net Kâr Marjı" ile çarpar. Böylece, beklenen satışların ne kadarının dönem sonu net kârına dönüşeceği tahmin edilmiş olur.
>
> 4. Şirketin Toplam Değerinin Hesaplanması (Fiyatlama):
>    Elde edilen "Tahmini Net Kâr", piyasanın bu şirkete biçeceği değer olan F/K (Fiyat/Kazanç) çarpanı ile çarpılır. F/K çarpanı, yatırımcıların şirketin 1 TL'lik kârına karşılık kaç TL ödemeye razı olduğunu gösterir. Bu çarpım sonucunda şirketin ulaşması beklenen toplam değeri bulunur.
>
> 5. Hisse Başına Fiyatın Bulunması (Birim Fiyat):
>    Son aşamada, şirketin bulunan toplam hedef piyasa değeri, "Ödenmiş Sermaye"ye bölünür. Borsa İstanbul'da şirketlerin her 1 TL'lik nominal ödenmiş sermayesi 1 adet hisseyi (lotu) temsil eder. Dolayısıyla koca pastanın (toplam piyasa değeri), dilim sayısına (ödenmiş sermaye) bölünmesiyle yatırımcının ekranında görmesi gereken **Tahmini Hisse Fiyatı** ortaya çıkar.
>
> Özetle bu sistem Şirket bu yıl ne kadar satar, bu satıştan ne kadar kâr eder ve piyasa bu kârı geçmişteki veya beklenen çarpanlarla nasıl fiyatlar? sorularının adım adım ilerleyen matematiksel bir simülasyonudur.
>
> 2023 yıl sonunda sanırım froto gerçek maliyet ve kapanış değeri tam olarak 747 TL idi. Bu basit değerleme de 796tl hedef fiyat vermiş 2023 senesi başında.

Görseller:
- G1: SHA-256 `9480046bdb9205143348426182c8f3f8d8b9e0d8c508519842f6ce6aab760de1` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-82c27ba9-9d75-4b99-9502-f9ee6acc0c12.png` · beyinde VAR: `assets/gorsel-paket-81-froto-basit-fk-ileri-hedef-outcome/01-froto-2023-basit-fk-hedef.png`

Beyin notu: `gorsel-paket-81-froto-basit-fk-ileri-hedef-outcome.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)

### R153 · 2026-08-28 03:13 UTC · EREGL 10 Yıllık FCFF DCF WACC ve İçsel Değer Görsel Paketi 82 · tweet bağlantısı yok

- Oturum(lar): `archived_sessions/rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl` (2026-08-28)

> Python ile yaptığımız DCF analizini biraz detaylı anlatalım. Risklerini daha önceki yazılarımdan birisinde anlatmıştım.
>
> Aslında yaptığımız şey çok temel bir mantığa dayanıyor: Bir şirketin bugünkü gerçek değeri, gelecekte cebimize koyacağı nakitlerin bugünkü değeridir. Bunu hesaplamak için de geçmişe bakıp geleceği hayal ettik ve riski hesaba kattık. Formüllere boğulmadan, tabloların bize ne anlattığına adım adım bakalım.
>
> Tarihsel Veriler ve Oran Analizi (1. ve 3. Tablolar)
>
> Geleceği tahmin etmeden önce şirketin huyunu suyunu öğrenmemiz gerekir. Tarihsel tablolarda EREGL'nin 2010'dan 2021'in ortasına kadar olan röntgenini çektik. Şirket Büyüyor mu? Satış rakamlarına ve büyüme yüzdelerine baktık. EREGL'nin zaman içinde satışlarını nasıl artırdığını gördük. Para Kazanabiliyor mu? Brüt kar ve FAVÖK (esas faaliyetlerden kazanılan nakit yaratma gücü) marjlarına baktık. Yani "100 liralık mal sattığında bunun ne kadarı şirketin cebinde kalıyor?" sorusunun cevabını aradık.
>
> Ne Kadar Yatırım Yapıyor? Demir çelik sektörü ağır yatırımlar gerektirir. Fabrikaları ayakta tutmak için yapılan yatırımları (Capex) ve günlük operasyonları döndürmek için kasada, stokta, alacakta tutması gereken parayı (İşletme Sermayesi/ONİS) inceledik.
>
> Geçmiş yılların ortalamaları bize şirketin "normalde" nasıl bir tempoda çalıştığını gösterdi.
>
> 2. Geleceği Kurgulamak: Varsayımlar (4. Tablo)
>    Tarihsel ortalamalardan aldığımız cesaretle, önümüzdeki 10 yıl boyunca (2021-2030) EREGL'nin nasıl bir performans sergileyeceğini senaryolaştırdık.
>
> Burada uçuk kaçık hayaller kurmak yerine ayakları yere basan oranlar belirledik. Satışların ilk yıllarda hızlı, sonra daha oturmuş bir tempoda büyüyeceğini varsaydık. Geçmişteki karlılık oranlarına bakarak, gelecekte de benzer brüt kar ve FAVÖK marjları ile çalışacağını öngördük. Kazandığı paranın ne kadarını vergiye vereceğini, ne kadarını tesislere yeniden yatırım olarak harcayacağını ve ne kadarını günlük çarkları döndürmek (stok, alacak vb.) için bağlayacağını geçmiş alışkanlıklarına göre sabitledik.
>
> 3. Paranın Maliyeti (WACC Tablosu)
>    Burası işin en can alıcı noktalarından biri. Gelecekte kazanılacak paranın bugünkü değeri aynı değildir, hele ki enflasyon ve risk varsa. İnsanlar risksiz devlet tahvili almak yerine neden EREGL hissesi alsın? Çünkü ekstra getiri isterler. Türkiye'nin ülke riskini, küresel piyasaların durumunu ve hissenin kendi dalgalanma riskini hesaba katarak yatırımcının "beklediği getiriyi" bulduk. Bunu yaparken farklı yaklaşımların (temettü, risk primi vb.) ortalamasını alarak daha güvenli bir yol izledik.
>
> Şirketin Borçlanma Maliyeti: Şirket sadece ortakların parasıyla değil, banka kredisiyle de dönüyor. Bu borçların da bir faiz yükü var.
>
> Şirketin kaynağının ne kadarı borç, ne kadarı özsermaye diye bakıp, bu iki maliyeti harmanladık. Bulduğumuz bu oran, şirketin hayatta kalmak ve yatırımcıyı mutlu etmek için kazanması gereken minimum getiri oranıdır. Gelecekteki nakitleri bugüne çekerken işte bu iskonto oranını kullanacağız.
>
> 4. Gelecekteki Parayı Bugüne Getirmek: Tahminler ve Değerleme (2. Tablo)
>
> Artık her şey hazır. Varsayımlarımızı çalıştırdık ve 10 yıllık bir projeksiyon çizdik. Satışlardan yola çıkarak masrafları, amortismanları ve vergileri düştük. Şirketin kasasında durması gerekmeyen, dağıtılabilir saf nakdi, yani Serbest Nakit Akışını bulduk. Bulduğumuz bu gelecek nakitleri, az önce hesapladığımız risk oranımızla (WACC) adeta bir zaman makinesine koyup "bugünkü değerine" küçülttük. Tabi şirket 10. yılda kapanmayacak, sonsuza kadar yaşayacak. 10. yıldan sonraki tüm o sonsuz geleceği de bir "Devam Eden Değer (Terminal Value)" olarak tek bir kalemde hesaplayıp onu da bugüne çektik.
>
> 5. Sonuç:
>    Tüm o hesapların meyvesini topladığımız yer burası. Gelecek 10 yılın nakitlerinin bugünkü değerini topladık.
>    Buna sonsuza kadar yaşayacağı dönemin değerini ekledik. Şirketin şu an kasasında duran peşin parayı ekleyip, borçlarını düştük. (Çünkü şirketi satın alsak kasadaki para bizim olur, ama borçları da biz öderiz).
>    Bu işlemler sonucunda EREGL'nin olması gereken o devasa Firma Değerini bulduk. Son olarak bu dev pastayı, şirketin sahip olduğu toplam hisse adedine böldük ki bir dilim pastanın (1 adet hissenin) gerçekte ne kadar ettiğini bulalım.
>
> Özetle modelimiz bize bir hissenin içsel değerinin yaklaşık 22.69 TL olması gerektiğini söyledi. Ancak biz bu analizi yaparken piyasada hisse 16.67 TL'den işlem görüyordu. Yani piyasa, şirketin gelecekte üreteceği nakitleri bizim kadar iyimser fiyatlamamış. Bu durum bize, hissenin olması gereken değerin altında işlem gördüğünü ve yatırımcı için yaklaşık %36'lık bir yükseliş potansiyeli barındırdığını gösteriyor.
>
> Analizin kodlaması, doğruluğunu kontrol etmek için daha önceki excel çalışmalarından alınarak yapıldığı için eski tarihlidir.
>
> WACC hesabı kavramı anlamanız için gösterilmiştir. DCF de WACC 19.1 kullanılmıştır.

Görseller:
- G1: SHA-256 `34f8a6b87af78a2faeee276841269d9c7052a91031deadbfd6a2fd50b964eb04` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-178375bd-b84a-4f26-9f76-ff81c53034a8.png` · beyinde VAR: `assets/gorsel-paket-82-eregli-dcf-10y-ic-deger/01-wacc-kavramsal-uc-yontem.png`
- G2: SHA-256 `92bb317a8156eb9b8d039f659c60ea52aed0f5d980bb6345bd54b3d99f28cb24` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-bf22eb1d-2520-4ba3-a1fb-4e6678079ed9.png` · beyinde VAR: `assets/gorsel-paket-82-eregli-dcf-10y-ic-deger/02-eregli-tarihsel-dcf-girdileri.png`
- G3: SHA-256 `0c5afa7b8f913f3bb39e003da7f029240b2da6d158321c0b60ba8daabb52cc1e` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-e24f84bd-0bca-4a04-be4f-eb514c0b85a3.png` · beyinde VAR: `assets/gorsel-paket-82-eregli-dcf-10y-ic-deger/03-eregli-2021-2030-dcf-projeksiyon.png`
- G4: SHA-256 `61f20677773975f6ff21b6b8945deb327c8659e55a62955428c3444c064b59a2` · özgün yol `C:\Users\levent\AppData\Local\Temp\codex-clipboard-2c7d0d22-efc1-478e-8f2f-5410e7845b1d.png` · beyinde VAR: `assets/gorsel-paket-82-eregli-dcf-10y-ic-deger/04-eregli-oran-analizi.png`

Beyin notu: `gorsel-paket-82-eregli-dcf-10y-ic-deger.md` — dayanak: görsel SHA-256 (assets/ eşleşmesi)


## 4. Eşleme tablosu (beyine "## Ham" bölümü için; tüm kayıtlar)

| not dosya adı | ham kayıt başlığı | sohbet kaydı dosyası + tarih | eşleşme dayanağı |
| --- | --- | --- | --- |
| tweet-medyan-temelli-finansal-indikatorler.md | R001 · 2026-08-27 16:40 UTC · Medyan Temelli Finansal İndikatörler | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| tweet-sektor-rotasyonundan-hisse-secimine.md | R002 · 2026-08-27 16:43 UTC · Sektör Rotasyonundan Hisse Seçimine Analiz Zinciri | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.29; düşük skorlar elle doğrulandı) |
| tweet-alark-125-42.md | R003 · 2026-08-27 16:46 UTC · ALARK Trend Kırılımı ve Bearish Butterfly Senaryosu | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.38; düşük skorlar elle doğrulandı) |
| tweet-uygulama-algoritmalari-v1.md | R004 · 2026-08-27 16:51 UTC · İlk Uygulama Algoritmaları ve Tarama Yol Haritası | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.35; düşük skorlar elle doğrulandı) |
| tweet-harmonik-momentum-squeeze-projesi.md | R005 · 2026-08-27 16:53 UTC · Harmonik Formasyonlarda Momentum Squeeze Zamanlaması | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.10; düşük skorlar elle doğrulandı) |
| tweet-uygulama-algoritmalari-v1.md | R006 · 2026-08-27 16:55 UTC · İlk Uygulama Algoritmaları ve Tarama Yol Haritası | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (not Takoz/bayrak/flama satırını içerir) |
| tweet-uygulama-algoritmalari-v1.md | R007 · 2026-08-27 16:57 UTC · İlk Uygulama Algoritmaları ve Tarama Yol Haritası | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (not Takoz/bayrak/flama satırını içerir) |
| gorsel-paket-01-harmonik-formasyon-tarama.md | R008 · 2026-08-27 16:57 UTC · Harmonik Formasyon ve Tarama Görsel Paketi 01 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| YENİ: tweet-arz-talep-bolgesinde-formasyon-bekleyisi.md | R009 · 2026-08-27 17:01 UTC · Dün olmadı ama bu akşam iyi bir formasyon bulursam, böyle tam arz tale… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | beyinde eşleşme yok |
| tweet-froto-nakit-piyasa-degeri-18-89.md | R010 · 2026-08-27 17:03 UTC · FROTO Nakit Tamponu ve Piyasa Değeri Oranı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.32; düşük skorlar elle doğrulandı) |
| tweet-gartley-butterfly-ayri-tarayicilar.md | R011 · 2026-08-27 17:06 UTC · Gartley ve Butterfly İçin Ayrı Tarayıcı Modülleri | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı) |
| gorsel-paket-02-coklu-sistem-provenance.md | R012 · 2026-08-27 17:08 UTC · Çoklu Sistem Sonuçları ve Provenance Görsel Paketi 02 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-harmonik-xb-trend-kirilimi-stratejisi.md | R013 · 2026-08-27 17:11 UTC · Harmonik Formasyonlarda X-B Trend Çizgisi Kırılım Stratejisi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-gartley-d-tepki-penceresi-10-gun.md | R014 · 2026-08-27 17:20 UTC · Gartley D Noktası Sonrası Tepki Penceresi ve Belirsizlik | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-haftalik-bullish-gartley-talep-alani-tarama.md | R015 · 2026-08-27 17:25 UTC · Haftalık Bullish Gartley ve Uzun Vadeli Talep Alanı Taraması | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.29; düşük skorlar elle doğrulandı) |
| tweet-abcd-cd-bacagi-siddet-belirleyicileri.md | R016 · 2026-08-27 17:31 UTC · AB=CD Formasyonunda CD Bacağı Şiddetinin Belirleyicileri | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı) |
| gorsel-paket-03-smrtg-abcd-backtest.md | R017 · 2026-08-27 17:33 UTC · SMRTG AB=CD Backtest Görsel Paketi 03 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-iskpl-abcd-cden-dye-backtest.md | R018 · 2026-08-27 17:37 UTC · ISKPL AB=CD C'den D'ye Backtest Örneği | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-abcd-geometrik-gecerlilik-kurallari.md | R019 · 2026-08-27 17:42 UTC · AB=CD Geometrik Geçerlilik ve Bozulma Kuralları | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.21; düşük skorlar elle doğrulandı) |
| tweet-fibonacci-extension-abcd-kullanimi.md | R020 · 2026-08-27 17:45 UTC · Fibonacci Extensionların AB=CD ile Kullanımı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-ml-trade-13-gun-9-isabet.md | R021 · 2026-08-27 17:49 UTC · ML Trade Modelinde 13 Günde 9 İsabet | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-momentum-faaliyet-nakit-akisi-5x5-portfoy.md | R022 · 2026-08-27 17:52 UTC · Momentum ve Faaliyet Nakit Akışı 5x5 Portföy Araştırması | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı) |
| tweet-bullish-engulfing-mum-kodu.md | R023 · 2026-08-27 17:55 UTC · Bullish Engulfing Mum Yapısı ve Kod Mantığı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-acsel-direnc-kirilimi-volume-profile-val.md | R024 · 2026-08-27 17:59 UTC · ACSEL Direnç Kırılımı ve Volume Profile VAL Senaryosu | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-tweezer-bottom-talep-bolgesi-backtest.md | R025 · 2026-08-27 18:02 UTC · Tweezer Bottom Talep Bölgesi Tarama ve Backtest Planı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı) |
| tweet-volatilite-piyasa-soku-yeni-alim-freni.md | R026 · 2026-08-27 18:05 UTC · Volatilite Şok Rejimi ve Yeni Alım Freni | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.06; düşük skorlar elle doğrulandı) |
| tweet-talep-bolgesi-volume-profile-momentum-confluence.md | R027 · 2026-08-27 18:08 UTC · Talep Bölgesinden Tepki ve Hacim-Momentum Confluence Görseli | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-varyans-risk-primi-model-free-kesisim.md | R028 · 2026-08-27 18:11 UTC · Varyans Risk Primi ve Model-Free Varyans Kesişim Projesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| gorsel-paket-04-tsla-implied-move.md | R029 · 2026-08-27 18:13 UTC · TSLA Yüzde 10,4 Implied Move Görsel Paketi 04 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-volatilite-harvesti-sabit-agirlik-rebalancing.md | R030 · 2026-08-27 18:16 UTC · Volatilite Harvesti Sabit Ağırlık Yeniden Dengeleme Projesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı) |
| gorsel-paket-05-bist-vrp-scanner.md | R031 · 2026-08-27 18:19 UTC · BIST VRP Scanner ve VOL AL-SAT Mantığı Görsel Paketi 05 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-06-sektor-getiri-liderleri.md | R032 · 2026-08-27 18:23 UTC · Sektör Getiri Liderleri 30-60-90 Gün Görsel Paketi 06 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-07-sektor-anomali-temizleme.md | R033 · 2026-08-27 18:25 UTC · Sektör Getirisinde Anomali Temizleme ve Hesap Tutarlılığı Görsel Paketi 07 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-rolling-cointegration-iliski-bozulma-kapisi.md | R034 · 2026-08-27 18:29 UTC · Rolling Cointegration ile İlişki Bozulma Kapısı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı) |
| gorsel-paket-08-fiili-dolasim-orani.md | R035 · 2026-08-27 18:32 UTC · Fiili Dolaşım Oranı Lookup ve Değişken Eşik Görsel Paketi 08 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-fiyat-hacim-fiili-dolasim-ucgeni.md | R036 · 2026-08-27 18:35 UTC · Fiyat Hacim ve Fiili Dolaşım Üçlü Piyasa Modeli | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı) |
| gorsel-paket-09-distal-proximal-arz-talep.md | R037 · 2026-08-27 18:37 UTC · Distal ve Proximal Çizgiler ile Arz-Talep Bölgesi Taraması Görsel Paketi 09 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-10-hktm-demand-supply.md | R038 · 2026-08-27 18:41 UTC · HKTM Demand-Supply Bölgesi ve Teyit Katmanları Görsel Paketi 10 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-trend-cizgisi-swing-pivot-regresyon-zarf.md | R039 · 2026-08-27 18:44 UTC · Trend Çizgisi Motoru Swing Pivot ve Regresyon Zarf | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı) |
| tweet-confluence-bagimsiz-kanit-yogunlugu.md | R040 · 2026-08-27 18:47 UTC · Confluence Alanlarında Bağımsız Kanıt Yoğunluğu | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| gorsel-paket-11-froto-bos-choch.md | R041 · 2026-08-27 18:50 UTC · FROTO BOS ve CHoCH Market Structure Görsel Paketi 11 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-12-doas-advance-block.md | R042 · 2026-08-27 18:53 UTC · DOAS Advance Block ve Supply Zone Görsel Paketi 12 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-13-ttkom-demand-invalidation.md | R043 · 2026-08-27 18:57 UTC · TTKOM Demand Zone Invalidation ve Kutu Bitişi Görsel Paketi 13 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| kaynak-cme-group-volatilite-opsiyon-veri-araclari.md | R044 · 2026-08-27 19:01 UTC · CME Group Volatilite Opsiyon Veri ve Araçları Araştırması | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.08; düşük skorlar elle doğrulandı) |
| tweet-gordon-buyume-modeli-temettu-degerleme.md | R045 · 2026-08-27 19:09 UTC · Gordon Büyüme Modeli ile Temettü Değerlemesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı) |
| gorsel-paket-14-isletme-analizi-kriterleri.md | R046 · 2026-08-27 19:12 UTC · İşletme Analizi Operasyonel Finansal ve Değerleme Çerçevesi Görsel Paketi 14 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-15-rbr-demand-zone.md | R047 · 2026-08-27 19:16 UTC · Rally-Base-Rally RBR Demand Zone Görsel Paketi 15 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-relatif-degerleme-piyasa-norm-bantlari.md | R048 · 2026-08-27 19:20 UTC · Relatif Değerleme Piyasa Norm Bantları ve Çoklu Çarpan Teyidi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.07; düşük skorlar elle doğrulandı) |
| gorsel-paket-16-temel-momentum-ters-faz.md | R049 · 2026-08-27 19:23 UTC · Temel-Momentum Ters Faz Quant Stratejisi Görsel Paketi 16 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-17-imbalance-gucu.md | R050 · 2026-08-27 19:27 UTC · Candle Imbalance Güç Sıralaması Görsel Paketi 17 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-18-konsolidasyon-body-wick.md | R051 · 2026-08-27 19:31 UTC · Konsolidasyon Bölgesi Gövde ve Gölge Sınırları Görsel Paketi 18 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-19-eurtry-forward-monte-carlo.md | R052 · 2026-08-27 19:36 UTC · EURTRY Forward ve Monte Carlo Pazarlık Çerçevesi Görsel Paketi 19 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-bollinger-kuyruklari-ortalama-donus-var.md | R053 · 2026-08-27 19:40 UTC · Bollinger Kuyrukları Ortalama Dönüş ve VaR Risk Çerçevesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-20-sponsor-candle.md | R054 · 2026-08-27 19:44 UTC · Bullish ve Bearish Sponsor Candle Görsel Paketi 20 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-21-confluence-alan-taramasi.md | R055 · 2026-08-27 19:48 UTC · Swing Point Talep Bölgesi ve HSAR Confluence Alan Taraması Görsel Paketi 21 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-22-hisse-karar-destek-pipeline.md | R056 · 2026-08-27 19:52 UTC · Hisse Senedi Analiz ve Karar Destek Pipeline Görsel Paketi 22 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-ozkaynak-artisi-varlik-finansman-yatirim-verimliligi.md | R057 · 2026-08-27 19:56 UTC · Özkaynak Artışı Varlık Kompozisyonu ve Yatırım Verimliliği | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.10; düşük skorlar elle doğrulandı) |
| tweet-regresyon-ml-rasyolardan-piyasa-degeri-sapmasi.md | R058 · 2026-08-27 20:02 UTC · Regresyon ve ML ile Rasyolardan Piyasa Değeri Sapması | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı) |
| gorsel-paket-23-froto-ppe-fiyat.md | R059 · 2026-08-27 20:06 UTC · FROTO Maddi Duran Varlık Artışı ve Fiyat İlişkisi Görsel Paketi 23 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-cari-oran-likidite-acigi-bedelli-sermaye-artirimi.md | R060 · 2026-08-27 20:12 UTC · Cari Oran Likidite Açığı ve Bedelli Sermaye Artırımı Riski | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.09; düşük skorlar elle doğrulandı) |
| gorsel-paket-24-merton-modeli.md | R061 · 2026-08-27 20:16 UTC · Merton Modeli Distance to Default EDF ve Kredi Spread Görsel Paketi 24 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-asuzu-coklu-degerleme-tutarliligi.md | R062 · 2026-08-27 20:22 UTC · ASUZU F/K PD/DD ve FD/FAVÖK Çoklu Değerleme Tutarlılığı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-ttrak-pddd-primi-carpan-sikismasi.md | R063 · 2026-08-27 20:28 UTC · TTRAK PD/DD Primi Çarpan Sıkışması ve Dağıtım İddiası | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-25-degerleme-agirliklandirma.md | R064 · 2026-08-27 20:34 UTC · A B DCF Çoklu Değerleme Birleştirme ve Ağırlıklandırma Modeli Görsel Paketi 25 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| YENİ: tweet-nihai-hedef-tek-tus-temel-teknik-degerleme-llm-nlp.md | R065 · 2026-08-27 20:39 UTC · Nihai hedef Tek bir tuş ile temel ve teknik analizin yapıldığı, değerl… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | beyinde eşleşme yok |
| tweet-beklenen-fk-coklu-regresyon-modeli.md | R066 · 2026-08-27 20:46 UTC · Beklenen F/K Çoklu Regresyon Modeli ve Güvenilirliği | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| gorsel-paket-02-coklu-sistem-provenance.md | R067 · 2026-08-27 20:51 UTC · Çoklu Sistem Sonuçları ve Provenance Görsel Paketi 02 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.03; düşük skorlar elle doğrulandı) |
| gorsel-paket-27-asuzu-fk-ex-ante-zaman-cizgisi.md | R068 · 2026-08-27 20:58 UTC · ASUZU F/K Değerleme Referansları ve Ex-Ante Zaman Çizgisi Görsel Paketi 27 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-28-proje-bugunku-deger-ve-teknik-kapi.md | R069 · 2026-08-27 21:04 UTC · Proje Bugünkü Değeri Piyasada Fiyatlanma Boşluğu ve Teknik Kapı Görsel Paketi 28 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-29-uc-yontem-rs-wacc-dcf-girdileri.md | R070 · 2026-08-27 21:10 UTC · Üç Yöntemle Özkaynak Maliyeti WACC ve DCF Girdileri Görsel Paketi 29 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-30-fed-beklenti-altin-fiyatlama.md | R071 · 2026-08-27 21:15 UTC · FED Faiz Beklentisi Altın Fiyatlaması ve Beklenti Sürprizi Görsel Paketi 30 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-31-saglikli-trend-csco.md | R072 · 2026-08-27 21:19 UTC · Sağlıklı Trend Yapısı ve CSCO Güçlü Trend Görsel Paketi 31 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-32-gartley-abcd-talep-dusen-kirilimi.md | R073 · 2026-08-27 21:22 UTC · Gartley AB=CD Talep Bölgesi Düşen Kırılımı ve Relative Strength Görsel Paketi 32 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-33-min-vol-max-sharpe-dey-bist100.md | R074 · 2026-08-27 21:25 UTC · Min Volatility Max Sharpe Portföyleri DEY ve BIST100 Karşılaştırması Görsel Paketi 33 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-34-siyah-kugu-talep-run.md | R075 · 2026-08-27 21:28 UTC · Siyah Kuğu Harmoniği Talep Bölgesi ve RUN Outcome Görsel Paketi 34 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-35-beyaz-kugu-sell-abcd-dusen-kirilimi.md | R076 · 2026-08-27 21:31 UTC · Beyaz Kuğu SELL AB=CD Düşen Kırılımı ve Yön Çatışması Görsel Paketi 35 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-36-volatilite-rehavet-yon-bagimsiz-kirilim.md | R077 · 2026-08-27 21:34 UTC · Volatilite Rehaveti Yön Bağımsız Kırılım ve Ok Semantiği Görsel Paketi 36 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-37-gunluk-rebalancing-aktif-pasif.md | R078 · 2026-08-27 21:37 UTC · Gün Sonu Rebalancing Aktif Pasif Portföy ve İşlem Logu Görsel Paketi 37 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-38-akcns-haftalik-abcd-talep-ema.md | R079 · 2026-08-27 21:42 UTC · AKCNS Haftalık AB=CD Talep EMA ve Katılım Görsel Paketi 38 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-39-abcd-detector-fibo-talep-tepki.md | R080 · 2026-08-27 21:45 UTC · AB=CD Detector A B C D Pivot Fibo Talep ve Tepki Görsel Paketi 39 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-40-haftalik-abcd-talep-tepki.md | R081 · 2026-08-27 21:49 UTC · Haftalık BUY AB=CD D Noktası Talep Tepkisi Görsel Paketi 40 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-41-konsolidasyon-suresi-kirilim-siddeti.md | R082 · 2026-08-27 21:52 UTC · Konsolidasyon Süresi Ok Alanı ve Kırılım Şiddeti Görsel Paketi 41 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-08-fiili-dolasim-orani.md | R083 · 2026-08-27 21:55 UTC · Fiili Dolaşım Oranı Lookup ve Değişken Eşik Görsel Paketi 08 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| gorsel-paket-42-buy-abcd-yukselen-destek-hedefler.md | R084 · 2026-08-27 21:58 UTC · BUY AB=CD D Noktası Yükselen Destek ve Hedefler Görsel Paketi 42 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-43-rysas-buy-abcd-kanal-baglamı.md | R085 · 2026-08-27 22:01 UTC · RYSAS BUY AB=CD Yükselen Kanal Bağlamı Görsel Paketi 43 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-44-basit-gizli-filtre-breakout-kesfi.md | R086 · 2026-08-27 22:04 UTC · Basit Gizli Filtrelerle Point A Point B Breakout Keşfi Görsel Paketi 44 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-45-balat-abcd-negatif-kumulatif-delta.md | R087 · 2026-08-27 22:07 UTC · BALAT AB=CD Başarısızlık Riski ve Negatif Kümülatif Delta Görsel Paketi 45 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| kaynak-ai-ml-dl-veri-bilimi-kitap-reposu.md | R088 · 2026-08-27 22:11 UTC · Yapay Zeka Makine Öğrenimi Derin Öğrenme ve Veri Bilimi Kitap Reposu | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.30; düşük skorlar elle doğrulandı) |
| gorsel-paket-46-sagliksiz-yukselis-mavi-sifir-kesisi.md | R089 · 2026-08-27 22:14 UTC · Sağlıksız Yükseliş Mavi Sıfır Kesisi ve Kırmızı Rejim Görsel Paketi 46 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-47-lindsay-trident-abc-b-kirilimi-d.md | R090 · 2026-08-27 22:17 UTC · Lindsay Trident ABC B Kırılımı ve D Hedef Formülü Görsel Paketi 47 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-trend-rejim-degisimi-korelasyon-hmm-gereksiz.md | R091 · 2026-08-27 22:21 UTC · Trend Rejim Değişiminde Rolling Korelasyon ve HMM Gereksizliği | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.07; düşük skorlar elle doğrulandı) |
| gorsel-paket-48-smrtg-fiyat-volatilite-birlikte-artis.md | R092 · 2026-08-27 22:24 UTC · SMRTG Fiyat ve Volatilitenin Birlikte Artışı Defansif Pozisyon Görsel Paketi 48 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-49-saglikli-yukselis-fiyat-vol-ters-iliski.md | R093 · 2026-08-27 22:28 UTC · Sağlıklı Yükseliş Fiyat Yukarı Mavi Seri Sıfır Altında Görsel Paketi 49 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-50-bist100-bist-volatilite-gulumsemesi.md | R094 · 2026-08-27 22:33 UTC · BIST 100 ve BIST Volatilite Getirilerinde Doğrusal Olmayan Gülümseme Görsel Paketi 50 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-51-cimsa-oyakc-rotatif-zskor-portfoy.md | R095 · 2026-08-27 22:36 UTC · CIMSA OYAKC Z-Skorlu Rotatif Portföy Görsel Paketi 51 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-istatistiksel-arbitraj-150bin-esbutunlesme-taramasi.md | R096 · 2026-08-27 22:41 UTC · İstatistiksel Arbitrajda 150 Bin Eşbütünleşme Kombinasyonu Taraması | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.20; düşük skorlar elle doğrulandı) |
| tweet-garch-standart-sapma-volatilite-risk-minimizasyonu.md | R097 · 2026-08-27 22:44 UTC · GARCH ve Standart Sapmayla Volatilite Riskini Azaltma Örneği | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.21; düşük skorlar elle doğrulandı) |
| tweet-stat-arb-momentum-donus-teyidi-kar-carpani.md | R098 · 2026-08-27 22:48 UTC · Stat-Arb Sisteminde Momentum Dönüş Teyidi ve Kâr Çarpanı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı) |
| gorsel-paket-52-agrot-garan-duygusuz-disiplin-mtm.md | R099 · 2026-08-27 22:51 UTC · AGROT GARAN Stat-Arb Duygusuz Disiplin ve Mark-to-Market Görsel Paketi 52 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-53-stat-arb-bag-kopusu-negatif-backtest.md | R100 · 2026-08-27 22:55 UTC · Stat-Arb Görünmez Bağ Kopuşu ve Negatif Backtest Görsel Paketi 53 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-54-stat-arb-pairs-trading-kanonik-aciklama.md | R101 · 2026-08-27 22:59 UTC · Stat-Arb ve Pairs Trading Kanonik Açıklama Görsel Paketi 54 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-55-volatilite-arbitraj-otonom-sistem-tercihi.md | R102 · 2026-08-27 23:04 UTC · Volatilite ve Arbitraj Favori Sistemleri ile Otonom Disiplin Görsel Paketi 55 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-bist-hft-colocation-quant-rekabet-kod-ogrenin.md | R103 · 2026-08-27 23:07 UTC · BIST HFT Colocation Kuant Rekabeti ve Kod Öğrenme Çağrısı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.16; düşük skorlar elle doğrulandı) |
| tweet-piyasa-dilinde-kesinlik-olasilik-risk-yol-haritasi.md | R104 · 2026-08-27 23:11 UTC · Piyasa Dilinde Kesinlik Tuzağı Olasılık Risk ve Yol Haritası | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı) |
| tweet-momentum-degerden-once-doner-egim-erken-uyari.md | R105 · 2026-08-27 23:14 UTC · Momentum Değerden Önce Döner Eğim Erken Uyarı ve Kesişim Teyidi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.16; düşük skorlar elle doğrulandı) |
| tweet-aritmetik-ortalama-outlier-rejim-tehlikesi.md | R106 · 2026-08-27 23:19 UTC · Aritmetik Ortalama Outlier Rejim Kırılması ve Sağlam Merkez Riski | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.06; düşük skorlar elle doğrulandı) |
| tweet-finans-muhendisligi-destek-direnc-seviye-motoru.md | R107 · 2026-08-27 23:22 UTC · Finans Mühendisliği ile Destek Direnç Seviye Motoru | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.08; düşük skorlar elle doğrulandı) |
| gorsel-paket-56-a1cap-weinstein-dort-evre.md | R108 · 2026-08-27 23:27 UTC · A1CAP Weinstein Dört Evre Fiyat Hacim Döngüsü Görsel Paketi 56 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-kagit-kalem-matematik-once-kod-sonra.md | R109 · 2026-08-27 23:33 UTC · Kağıt Kalem Matematik Önce Kod Sonra Model Geliştirme Disiplini | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.06; düşük skorlar elle doğrulandı) |
| tweet-dusuk-korelasyon-yuksek-volatilite-max-sharpe-aktif-trading.md | R110 · 2026-08-27 23:38 UTC · Düşük Korelasyon Yüksek Volatilite Max Sharpe ve Aktif Trading Matematik Föyü | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27); rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı) |
| tweet-kitap-model-sentezi-backtest-forward-test-kod-mimarisi.md | R111 · 2026-08-27 23:42 UTC · Kitaptan Özgün Model Sentezine Backtest Forward Test ve Kod Mimarisi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.07; düşük skorlar elle doğrulandı) |
| gorsel-paket-57-tektu-eregl-agirlik-duyarliligi.md | R112 · 2026-08-27 23:46 UTC · TEKTU EREGL Portföy Ağırlık Duyarlılığı ve Ex-Post Getiri Görsel Paketi 57 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-portfoy-optimizasyonu-volatilite-trading-risk-butcesi.md | R113 · 2026-08-27 23:50 UTC · Portföy Optimizasyonu Volatilite Trading ve Huzurlu Gece Risk Bütçesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı) |
| gorsel-paket-58-gubrf-fincan-kulp-matematik-foyu.md | R114 · 2026-08-27 23:53 UTC · GUBRF Fincan Kulp Fibo Kırılım Hedef Matematik Föyü Görsel Paketi 58 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27); rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-59-buyhold-sinyal-risk-scorecard.md | R115 · 2026-08-27 23:58 UTC · Buy and Hold ile Sinyal Bazlı Strateji Risk Getiri Scorecard Görsel Paketi 59 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-27) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-60-hidden-bullish-divergence.md | R116 · 2026-08-28 00:04 UTC · Gizli Pozitif Uyumsuzluk Trend Devamı ve Beş Günde Yüzde 29 Görsel Paketi 60 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-61-hidden-uyumsuzluk-takip-hatirlatmasi.md | R117 · 2026-08-28 00:08 UTC · Gizli Uyumsuzlukları Takip Etme Watchlist Hatırlatması Görsel Paketi 61 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-endeks-5of5-nhnl-corwin-schultz-likidite.md | R118 · 2026-08-28 00:11 UTC · Endeks 5/5 Trend Skoru NH-NL Genişliği ve Corwin-Schultz Likidite Raporu | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| gorsel-paket-62-froto-corwin-schultz-spread-sigma.md | R119 · 2026-08-28 00:15 UTC · FROTO Corwin-Schultz Spread Sigma Likidite ve Volatilite Görsel Paketi 62 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-63-bist-momentum-dey-backtest-denetimi.md | R120 · 2026-08-28 00:20 UTC · BIST 12 Aylık Momentum Decile Stratejisi ve Dört Aylık DEY Backtest Denetimi Görsel Paketi 63 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-optimal-momentum-plus-simulasyon-tamamlandi.md | R121 · 2026-08-28 00:25 UTC · Optimal Momentum Plus Kod Tamamlanması, Simülasyon İlerlemesi ve Teori Serisi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı) |
| tweet-kendini-yenileyen-algoritma-ana-frekans.md | R122 · 2026-08-28 00:28 UTC · Kendini Yenileyen Algoritma Ana Frekans ve Kanıtlı Öğrenme Döngüsü | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| kaynak-stefan-jansen-ml-algo-trading.md | R123 · 2026-08-28 00:32 UTC · Stefan Jansen Machine Learning for Trading Kitap ve Kaynak İncelemesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28); rollout-2026-08-28T03-33-24-01a045c9-2301-7a00-a740-60ea6527a708.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı) |
| gorsel-paket-64-dusen-trend-talep-hacim-ema-breakout.md | R124 · 2026-08-28 00:41 UTC · Düşen Trend Kırılımı Talep Hacim ve EMA Teyidi Görsel Paketi 64 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-65-ema-sikisma-pre-signal-bir-gun-yuzde5.md | R125 · 2026-08-28 00:46 UTC · EMA Sıkışması Pre-Signal ve Bir Günde Yüzde 5 Görsel Paketi 65 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-66-fibo-volume-profile-vwap-delta-yuzde20.md | R126 · 2026-08-28 00:51 UTC · Fibonacci Volume Profile VWAP DMI Delta ve Bir Ayda Yüzde 20 Görsel Paketi 66 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-67-krdmd-ema-sikisma-ratio-formasyon.md | R127 · 2026-08-28 00:56 UTC · KRDMD EMA Sıkışma Periyodu Ratio ve Formasyon Confluence Görsel Paketi 67 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-68-xu100-ema-kde-breakout-extension.md | R128 · 2026-08-28 01:01 UTC · XU100 EMA 50 100 200 Sıkışması KDE Kırılımı ve Extension Görsel Paketi 68 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-69-przma-bullish-fvg-revisit-ote.md | R129 · 2026-08-28 01:06 UTC · PRZMA Bullish FVG Revisit Mitigation OTE ve Alt Zaman CHoCH Görsel Paketi 69 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-70-haftalik-gravestone-doji-risk.md | R130 · 2026-08-28 01:11 UTC · Haftalık Gravestone Doji Mezar Taşı Risk ve Teyit Görsel Paketi 70 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-hareketli-ortalama-ust-alt-trend-yon-filtresi.md | R131 · 2026-08-28 01:16 UTC · Hareketli Ortalama Üstü Altı Sade Trend Yön Filtresi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı) |
| gorsel-paket-71-dragonfly-doji-ema-squeeze-exit.md | R132 · 2026-08-28 01:20 UTC · Dragonfly Doji EMA Sıkışması ve Yukarı Çıkış Görsel Paketi 71 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-72-hbk-fiyat-bilanco-katalizoru.md | R133 · 2026-08-28 01:25 UTC · Yıllıklandırılmış HBK U Dönüşü Fiyat Konsolidasyonu ve Bilanço Katalizörü Görsel Paketi 72 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi.md | R134 · 2026-08-28 01:30 UTC · ASUZU Finansal Borç Büyümesi Kullanım Kalitesi ve Otomotiv Peer Analizi Görsel Paketi 73 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-73-asuzu-finansal-borc-buyume-kalitesi.md | R135 · 2026-08-28 01:34 UTC · ASUZU Finansal Borç Büyümesi Kullanım Kalitesi ve Otomotiv Peer Analizi Görsel Paketi 73 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.18; düşük skorlar elle doğrulandı) |
| gorsel-paket-74-ozel-subplot-hidden-bullish.md | R136 · 2026-08-28 01:37 UTC · Özel Subplot ile Gizli Pozitif Uyumsuzluk Bağlam Gücü Görsel Paketi 74 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-satilik-degil-momentum-teknik-markowitz-max-sharpe-pipeline.md | R137 · 2026-08-28 01:41 UTC · Satışa Kapalı Momentum Teknik Markowitz ve Max Sharpe Karar Destek Pipeline | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.21; düşük skorlar elle doğrulandı) |
| gorsel-paket-75-isctr-ad-ema-walk-forward.md | R138 · 2026-08-28 01:46 UTC · ISCTR A/D EMA Walk-Forward Sakin Getiri Yolu ve Drawdown Görsel Paketi 75 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-75-isctr-ad-ema-walk-forward.md | R139 · 2026-08-28 01:50 UTC · ISCTR A/D EMA Walk-Forward Sakin Getiri Yolu ve Drawdown Görsel Paketi 75 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.22; düşük skorlar elle doğrulandı) |
| tweet-teknik-indikator-islem-sistemi-degerlendirme-kriterleri.md | R140 · 2026-08-28 01:55 UTC · Teknik İndikatör ve İşlem Sistemlerini Değerlendirme Kriterleri | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.18; düşük skorlar elle doğrulandı) |
| kaynak-awesome-econ-ai-stuff.md | R141 · 2026-08-28 01:59 UTC · Awesome Econ AI Stuff Ekonomistler İçin AI Skills Kaynak İncelemesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.26; düşük skorlar elle doğrulandı) |
| kaynak-ekonometri-hangi-soru-hangi-yontem-haritasi.md | R142 · 2026-08-28 02:06 UTC · Hangi Soru Hangi Yöntemi Çağırır Ekonometri Yöntem Haritası | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı) |
| gorsel-paket-76-mum-geometri-formasyon-motoru.md | R143 · 2026-08-28 02:14 UTC · OHLC Mum Geometrisi ve Formasyon Dedektör Motoru Görsel Paketi 76 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-pddd-roe-sektor-tarihsel-value-trap-filtresi.md | R144 · 2026-08-28 02:24 UTC · PD DD ROE Sektör Tarihsel Bant ve Değer Tuzağı Filtresi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| tweet-topsis-cok-kriterli-hisse-siralama-motoru.md | R145 · 2026-08-28 02:29 UTC · TOPSIS Çok Kriterli Hisse Sıralama ve Ağırlık Hassasiyeti Motoru | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı) |
| tweet-9aydan-yilsonu-satis-net-kar-tahmini.md | R146 · 2026-08-28 02:36 UTC · Dokuz Aylık Veriden Yıl Sonu Satış ve Net Kâr Tahmini | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.22; düşük skorlar elle doğrulandı) |
| gorsel-paket-77-asuzu-bottom-up-adet-degerleme.md | R147 · 2026-08-28 02:39 UTC · ASUZU Bottom-Up Adet Ciro Marj F K ve FD FAVÖK Değerleme Görsel Paketi 77 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-halftrend-buy-momentum-threshold-kapisi.md | R148 · 2026-08-28 02:45 UTC · HalfTrend Buy ve Momentum Threshold Çift Kapılı Long Adayı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.20; düşük skorlar elle doğrulandı) |
| gorsel-paket-78-petkm-confluence-talep-arz.md | R149 · 2026-08-28 02:48 UTC · PETKM Talep Arz Fibo EMA ve Hacim Confluence Görsel Paketi 78 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-79-arclk-aradonem-manuel-degerleme.md | R150 · 2026-08-28 02:52 UTC · ARCLK Ara Dönem Marjları Manual Override F K ve FD FAVÖK Görsel Paketi 79 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-80-froto-basit-fk-fdfavok-degerleme.md | R151 · 2026-08-28 02:59 UTC · FROTO Basit F K ve FD FAVÖK Değerleme Görsel Paketi 80 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-81-froto-basit-fk-ileri-hedef-outcome.md | R152 · 2026-08-28 03:07 UTC · FROTO Beş Adımlı Basit F K İleri Hedef ve 2023 Outcome Görsel Paketi 81 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-82-eregli-dcf-10y-ic-deger.md | R153 · 2026-08-28 03:13 UTC · EREGL 10 Yıllık FCFF DCF WACC ve İçsel Değer Görsel Paketi 82 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-83-eregli-tek-tus-dcf-konsol.md | R154 · 2026-08-28 03:21 UTC · EREGL Tek Tuş DCF Konsol Çıktısı ve Otomasyon Milestone Görsel Paketi 83 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-84-dcf-varsayim-riski-sensitivity-reverse-mos.md | R155 · 2026-08-28 03:26 UTC · DCF Varsayım Riski Sensitivity Reverse DCF ve Güvenlik Marjı Görsel Paketi 84 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-85-apo-mean-reversion-yukselen-kanal.md | R156 · 2026-08-28 03:32 UTC · Absolute Price Oscillator Mean Reversion ve Yükselen Kanal Filtresi Görsel Paketi 85 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-algoritma-tasarimi-temelleri-trading-sistemleri.md | R157 · 2026-08-28 03:38 UTC · Trading Algoritması Tasarımının Temelleri ve Üretim Yaşam Döngüsü | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.16; düşük skorlar elle doğrulandı) |
| gorsel-paket-86-fcff-fcfe-ddm-coklu-degerleme.md | R158 · 2026-08-28 03:43 UTC · FCFF FCFE DDM Üçlü DCF ve Yüzde 60 Çarpan Yüzde 40 İçsel Değer Görsel Paketi 86 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-87-cost-of-equity-total-beta.md | R159 · 2026-08-28 03:50 UTC · Özkaynak Maliyeti Unlevered Levered ve Total Beta Görsel Paketi 87 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-88-basit-capm-coe-python.md | R160 · 2026-08-28 03:56 UTC · Basit CAPM Özkaynak Maliyeti Python Hesabı Görsel Paketi 88 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-89-fcff-fcfe-ddm-yontem-secim-matrisi.md | R161 · 2026-08-28 04:02 UTC · FCFF FCFE ve DDM Yöntem Seçim Matrisi Görsel Paketi 89 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-roc-nopat-yatirilan-sermaye-hesabi.md | R162 · 2026-08-28 04:08 UTC · ROC NOPAT ve Ortalama Yatırılan Sermaye Hesabı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.18; düşük skorlar elle doğrulandı) |
| tweet-fcfe-ddm-capraz-kontrol-degerleme-motoru.md | R163 · 2026-08-28 04:16 UTC · FCFE DDM Çapraz Kontrol ve Değerleme Motoru Sözleşmesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı) |
| gorsel-paket-90-ebit-vergi-forecast-bilesik-buyume.md | R164 · 2026-08-28 04:21 UTC · EBIT ve Vergi Tahmininde Üçgensel Bileşik Büyüme Hatası Görsel Paketi 90 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-91-dcf-fcff-adim-adim-degerleme.md | R165 · 2026-08-28 04:28 UTC · DCF FCFF Adım Adım Değerleme Akışı Görsel Paketi 91 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| YENİ: tweet-excel-degerleme-calismasi-koda-donusumu.md | R166 · 2026-08-28 04:33 UTC · Aslında yapacak o kadar çok şey var ki bazen nereden başlasam diye otu… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| gorsel-paket-92-klmsn-engulfing-ema34-marker.md | R167 · 2026-08-28 04:39 UTC · KLMSN Bullish Engulfing EMA34 Tepki Kırılım ve Marker Hizası Görsel Paketi 92 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-93-gedza-demand-bos-hacim-momentum.md | R168 · 2026-08-28 04:44 UTC · GEDZA Trend Desteği Demand FVG BOS Hacim ve Karışık Momentum Görsel Paketi 93 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-python-finans-verisi-ogrenme-yol-haritasi.md | R169 · 2026-08-28 04:49 UTC · Python ve Finans Verisi Odaklı Öğrenme Yol Haritası | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.21; düşük skorlar elle doğrulandı) |
| tweet-williams-r-sma-swing-strateji-backtest.md | R170 · 2026-08-28 04:55 UTC · Williams Yüzde R ve SMA 14 Pullback Swing Stratejisi Backtest | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı) |
| tweet-python-finans-fikir-dogrulama-ve-yanlislama.md | R171 · 2026-08-28 05:16 UTC · Python ile Finansal Fikirleri Doğrulama ve Yanlışlama Disiplini | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.10; düşük skorlar elle doğrulandı) |
| tweet-fiyatlar-trend-halinde-hareket-eder.md | R172 · 2026-08-28 05:21 UTC · Fiyatlar Trendler Halinde Hareket Eder ve Tepe Dip Kahramanlığından Kaçınma | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı) |
| gorsel-paket-94-ham-fiyat-getiri-risk-portfoy.md | R173 · 2026-08-28 05:26 UTC · Ham Fiyattan Getiri Volatilite Kovaryans ve Sharpe Portföy Girdilerine Geçiş Görsel Paketi 94 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-arima-hiperparametre-acf-pacf-grid-search.md | R174 · 2026-08-28 05:31 UTC · ARIMA Hiperparametre Seçiminde ACF PACF Grid Search ve Rolling Doğrulama | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.16; düşük skorlar elle doğrulandı) |
| tweet-dea-vza-sektor-rotasyonu-malmquist-projesi.md | R175 · 2026-08-28 05:35 UTC · DEA VZA ile Sektör Rotasyonu ve Malmquist Verimlilik Projesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı) |
| tweet-clenow-exponential-regression-momentum-bist-projesi.md | R176 · 2026-08-28 05:42 UTC · Clenow Tipi Üstel Regresyon Momentum Skoru ve BIST Araştırma Projesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.24; düşük skorlar elle doğrulandı) |
| gorsel-paket-95-capm-portfoy-agirlik-risk-mutabakat.md | R177 · 2026-08-28 05:47 UTC · CAPM Beklenen Getiri Portföy Varyansı Minimum Varyans ve Sharpe Mutabakatı Görsel Paketi 95 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-convex-hull-dea-sektor-rotasyonu-projesi.md | R178 · 2026-08-28 05:54 UTC · Convex Hull ve DEA Birleşik Sektör Rotasyonu Projesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı) |
| tweet-topsis-hisse-secimi-yaklasan-proje.md | R179 · 2026-08-28 06:00 UTC · TOPSIS ile Hisse Seçimi Kriter Mimarisi ve Yaklaşan Proje | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı) |
| YENİ: tweet-python-ai-stratejik-yonetim-vizyon-misyon-kodlama.md | R180 · 2026-08-28 06:05 UTC · Python ve AI ile Stratejik Yönetimi Yeniden Kodlamak Bir kurumun Vizyo… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| gorsel-paket-96-momentum-161700-uclu-portfoy-aramasi.md | R181 · 2026-08-28 06:13 UTC · Momentum Evreninde 161700 Üçlü Portföy Kombinasyonu Araması Görsel Paketi 96 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-spicy-scipy-deterministik-markowitz-optimizasyonu.md | R182 · 2026-08-28 06:19 UTC · Spicy SciPy Deterministik Markowitz Optimizasyonu ve Monte Carlo Rol Ayrımı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı) |
| tweet-aylik-getiri-mevsimsellik-piyasa-hafizasi.md | R183 · 2026-08-28 06:24 UTC · Aylık Getiri Mevsimselliği Piyasa Hafızası ve Bayesian Risk Tilt’i | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.15; düşük skorlar elle doğrulandı) |
| tweet-atr-risk-butcesi-position-sizing-stop-loss.md | R184 · 2026-08-28 06:30 UTC · ATR Risk Bütçesi Position Sizing Acil Kapanış ve İz Süren Stop Sözleşmesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı) |
| tweet-probabilistik-edge-fat-tail-risk-of-ruin.md | R185 · 2026-08-28 06:35 UTC · Probabilistik Edge Beklenen Değer Fat Tail ve Risk of Ruin Geliştirme İlkesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.14; düşük skorlar elle doğrulandı) |
| tweet-poc-vah-val-vwap-auction-state-machine.md | R186 · 2026-08-28 06:40 UTC · POC VAH VAL ve VWAP Auction State Machine Tarama Sistemi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı) |
| gorsel-paket-97-iv-sd-expected-move-bantlari.md | R187 · 2026-08-28 06:46 UTC · IV Standart Sapma Expected Move Bantları ve Bariyer Stop İstatistiği Görsel Paketi 97 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-98-piyasanin-nabzi-teknik-rapor.md | R188 · 2026-08-28 06:52 UTC · Piyasanın Nabzı Yedi Gösterge Teknik Rapor ve Skor Kartı Denetimi Görsel Paketi 98 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-99-klmsn-momentum-multitimeframe-bos-demand-fibo.md | R189 · 2026-08-28 06:59 UTC · KLMSN Momentum Ön Eleme Çoklu Zaman BOS Demand Supply ve Fibonacci Karar Haritası Görsel Paketi 99 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-piyasa-denge-dengesizlik-auction-acceptance-state-machine.md | R190 · 2026-08-28 07:06 UTC · Piyasa Denge Dengesizlik Value Area Acceptance ve Rejection State Machine | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı) |
| gorsel-paket-100-gunluk-klasik-pivot-formul-kod.md | R191 · 2026-08-28 07:11 UTC · Günlük Klasik Pivot Noktaları Formül Kod ve Session Sözleşmesi Görsel Paketi 100 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-101-avod-demand-bearish-fvg-supply-ema.md | R192 · 2026-08-28 07:17 UTC · AVOD Demand Bearish FVG Supply EMA ve Zayıf Katılım Görsel Paketi 101 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-102-enjsa-elliott-wave5-hikkake-fvg-outcome.md | R193 · 2026-08-28 07:25 UTC · ENJSA Elliott Wave 5 Hedef Hikkake FVG ve Gerçekleşmiş Outcome Görsel Paketi 102 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-103-aksgy-retest-macd-volume-failure.md | R194 · 2026-08-28 07:31 UTC · AKSGY Altı Retest MACD Yanıltıcı Toparlanma ve Hacimsiz Teyit Başarısızlığı Görsel Paketi 103 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-gunluk-trade-breakout-gap-retest-volume-delta-atr-obv.md | R195 · 2026-08-28 07:37 UTC · Günlük Trade Breakout Gap Retest Volume Delta ATR ve OBV State Machine | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı) |
| gorsel-paket-104-obv-trend-onayi-senkronizasyon.md | R196 · 2026-08-28 07:43 UTC · OBV Trend Onayı Fiyat Senkronizasyonu Divergence ve Veri Kalitesi Görsel Paketi 104 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-105-bos-fibonacci-golden-zone-fvg-ob.md | R197 · 2026-08-28 07:48 UTC · BOS Destekli Fibonacci Golden Zone FVG Order Block Tarama Stratejisi Görsel Paketi 105 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-106-demand-ema-squeeze-supply-outcome.md | R198 · 2026-08-28 07:55 UTC · Demand Bölgesinde EMA 5 8 13 Sıkışması Breakout Retest ve Supply Outcome Görsel Paketi 106 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-107-bryat-smc-elliott-wave2-fvg-wave3.md | R199 · 2026-08-28 08:02 UTC · BRYAT SMC Elliott Wave 2 Golden Pocket Fresh FVG ve Wave 3 Hedef Görsel Paketi 107 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-108-beta-risk-pusulasi.md | R200 · 2026-08-28 08:16 UTC · Beta Katsayısı Sistematik Risk Benchmark Rolling Tahmin ve Rejim Stratejisi Görsel Paketi 108 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-likit-hisseler-etf-islem-derinligi-slippage-kapasite.md | R201 · 2026-08-28 08:24 UTC · Likit Hisseler ETF İşlem Derinliği Slippage ve Kapasite Önceliği | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.07; düşük skorlar elle doğrulandı) |
| tweet-rolling-alpha-skewness-momentum-liste-katmani.md | R202 · 2026-08-28 08:35 UTC · Rolling Alpha ve Rolling Skewness Momentum Liste Katmanı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.11; düşük skorlar elle doğrulandı) |
| gorsel-paket-109-balat-harmonik-tp-cd-retracement.md | R203 · 2026-08-28 08:41 UTC · BALAT Siyah Kuğu Harmonik CD Retracement TP ve Pattern-Specific Stop Görsel Paketi 109 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-110-elliott-wave2-fib-fvg-yuzde8.md | R204 · 2026-08-28 08:50 UTC · Elliott Wave 2 Fibonacci 0.50 0.618 FVG Çakışması ve Yüzde 8 Outcome Görsel Paketi 110 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-elliott-wave4-wave3-retracement-024-038-050.md | R205 · 2026-08-28 08:59 UTC · Elliott Wave 4 için Wave 3 Retracement 0.24 0.38 0.50 Projeksiyonu | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı) |
| tweet-fibo-0618-bolge-h4-order-block-multitimeframe.md | R206 · 2026-08-28 09:07 UTC · Fibonacci 0.618 Bölgesi H4 Order Block ve Çoklu Zaman Sniper Giriş Sözleşmesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.12; düşük skorlar elle doğrulandı) |
| gorsel-paket-111-elliott-5plus3-fibonacci-islem-gunleri.md | R207 · 2026-08-28 09:14 UTC · Elliott 5+3 Dalga Fraktal Yapı ve Fibonacci İşlem Günleri Görsel Paketi 111 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-112-confluence-kesisim-bagimsiz-kanit.md | R208 · 2026-08-28 09:22 UTC · Teknik Analiz Confluence Kesişim ve Bağımsız Kanıt Aileleri Görsel Paketi 112 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-113-bist-vix-long-bes-adim-kontrol.md | R209 · 2026-08-28 09:31 UTC · BIST 100 VIX Long Pozisyonu Beş Adımlı Kontrol ve Exit Yetkisi Görsel Paketi 113 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-114-bist-vix-python-master-analiz.md | R210 · 2026-08-28 09:41 UTC · BIST 100 VIX Python Master Analizi Kural Mutabakatı ve Tarihsel Hold Görsel Paketi 114 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-volatilite-ters-orantili-position-sizing-sermaye-koruma.md | R211 · 2026-08-28 09:50 UTC · Volatiliteyle Ters Orantılı Position Sizing ve Sermaye Koruma İlkesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.10; düşük skorlar elle doğrulandı) |
| gorsel-paket-115-position-sizing-yuzde1-2atr-sma250.md | R212 · 2026-08-28 10:00 UTC · Yüzde 1 Risk 2 ATR Position Sizing SMA250 ve Çift Stop Görsel Paketi 115 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-116-veriden-sinyale-algoritmik-trader-gelistirme.md | R213 · 2026-08-28 10:08 UTC · Veriden Sinyale Algoritmik Trader Geliştirme ve Production Yaşam Döngüsü Görsel Paketi 116 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-117-ema5-8-13-yukselen-trend-destek-tepki.md | R214 · 2026-08-28 10:19 UTC · EMA5 EMA8 EMA13 Boğa Dizilimi Yükselen Trend Desteği ve Zayıf Teyit Görsel Paketi 117 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-118-yatirimci-basarisizlik-surec-risk-kontrol.md | R215 · 2026-08-28 10:34 UTC · Yatırımcı Başarısızlık Nedenleri ve Süreç Risk Kontrol Sistemi Görsel Paketi 118 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-119-dma-kanal-egim-evre-gecis.md | R216 · 2026-08-28 10:42 UTC · DMA Kanal Eğimi Trend Hızı ve Olasılıksal Evre Geçişleri Görsel Paketi 119 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-120-fibonacci-coklu-aralik-konfluans.md | R217 · 2026-08-28 10:49 UTC · Çoklu Aralık Fibonacci Genişleme Daralma ve Konfluans Bölge Motoru Görsel Paketi 120 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-pine-script-python-gorev-ayrimi-veri-backtest-icra.md | R218 · 2026-08-28 10:57 UTC · Pine Script ve Python Görev Ayrımı Veri Egemenliği Backtest ML ve İcra Mimarisi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.16; düşük skorlar elle doğrulandı) |
| gorsel-paket-121-obo-neckline-hacim-hedef.md | R219 · 2026-08-28 11:05 UTC · Omuz Baş Omuz OBO Pivot Neckline Hacim Kırılım ve Hedef Görsel Paketi 121 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| tweet-fat-tail-firsat-survival-konvekslik.md | R220 · 2026-08-28 11:12 UTC · Fat Tail Uç Olay Fırsatı Survival Konvekslik ve Şok Rejimi Sözleşmesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.17; düşük skorlar elle doğrulandı) |
| gorsel-paket-122-makim-gartley-fvg-momentum.md | R221 · 2026-08-28 11:19 UTC · MAKIM Yükseliş Gartley FVG Temas Kimliği Swing LH ve Karışık Momentum Görsel Paketi 122 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-123-gartley-algoritmik-takip-formul-mutabakati.md | R222 · 2026-08-28 11:27 UTC · Gartley Algoritmik Takip Tablosu Formül Yön Tolerans R R ve Hedef Mutabakatı Görsel Paketi 123 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-124-doas-yfinance-realized-volatilite.md | R223 · 2026-08-28 11:36 UTC · DOAS yfinance Günlük ve Yıllık Gerçekleşen Volatilite Kod Denetimi Görsel Paketi 124 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-125-kismi-kar-trailing-prev-low-emergency-stop.md | R224 · 2026-08-28 11:45 UTC · Kısmi Kâr Alma ATR Trailing Önceki Gün Dibi ve Emergency Stop Görsel Paketi 125 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-126-bist-order-book-derinlik-bmp-fit.md | R225 · 2026-08-28 11:53 UTC · BIST Emir Defteri Derinlik Dağılımı THYAO BMP Fit ve Execution Kapasitesi Görsel Paketi 126 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-127-aztek-istatistiksel-uc-kapitulasyon-obi-ayi-tuzagi.md | R226 · 2026-08-28 12:01 UTC · AZTEK İstatistiksel Uç Kapitülasyon OBI Sapması ve Ayı Tuzağı Görsel Paketi 127 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| gorsel-paket-128-fiyat-hacim-konum-proxy-cot-kalabalik-dip.md | R227 · 2026-08-28 12:10 UTC · Fiyat Hacim Konum Proxy COT Kalabalıklaşma Ayrımı ve Dip Adayı Görsel Paketi 128 | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | görsel SHA-256 (assets/ eşleşmesi) |
| YENİ: tweet-korelasyon-yuksek-istatistiksel-arbitraj-garanti-degil.md | R228 · 2026-08-28 12:22 UTC · Derslerde öğrencilerin yaptığı ve çok sık karşılaştığım bir sorun. Ama… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-konveks-rotasyon-stratejisi-makro-dongu.md | R229 · 2026-08-28 12:22 UTC · Konveks Rotasyon Stratejisi Nasıl Olmalıdır? Sırada bakleyen projelerd… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| tweet-yuksek-ihtimalli-gunluk-islem-bes-kapi.md | R230 · 2026-08-28 12:23 UTC · Yüksek İhtimalli Günlük İşlem Kurulumunun Beş Kapısı | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.13; düşük skorlar elle doğrulandı) |
| YENİ: tweet-fiyat-grafigi-otesi-makro-bakis.md | R231 · 2026-08-28 12:29 UTC · Selamlar Biliyorsunuz, sadece hisse senetlerinin ya da kripto paraları… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-sektor-rotasyonu-hacim-tuzagi-sabit-tl-esigi.md | R232 · 2026-08-28 12:30 UTC · Sektör Rotasyonunda Yapılan En Büyük Hata: "Hacim Tuzağı" Geçen gün bi… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-rsi30-giris-iki-asamali-cikis.md | R233 · 2026-08-28 12:30 UTC · RSI 30 İle İşleme Girişte ve İki Aşamalı Çıkış Stratejisi Bu strateji,… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: gorsel-paket-129-doas-lojistik-regresyon-hacim-rsi-filtreli-strateji.md | R234 · 2026-08-28 12:31 UTC · Makine öğrenmesi modellerini aslında hisse senedi işlemlerinde kullanm… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: gorsel-paket-130-piyasa-evreleri-birikim-dagitim-semasi.md | R235 · 2026-08-28 12:32 UTC · (yalnız görsel) | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-ikili-dip-mum-tetikleyicileri.md | R236 · 2026-08-28 12:32 UTC · İkili Dip (Double Bottom) ve Mum Tetikleyicileri "W" harfi şeklindeki … | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-birikim-sureci-kotu-haber-akilli-para.md | R237 · 2026-08-28 12:33 UTC · Birikim süreci nasıl olur? Her şey genelde piyasa için kötü algılanan … | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-mum-govde-hacim-anomalisi-uyarisi.md | R238 · 2026-08-28 12:34 UTC · Sizin paranızı istiyorlar Dikkatli olun Geniş gövdeli mum yüksek hacim… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-statik-dinamik-iz-suren-stop-atr.md | R239 · 2026-08-28 12:34 UTC · Statik iz süren stop: Hedef = Giriş + (1.5 × Giriş ATR) → Sabit kalır … | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| tweet-sirket-degerlendirme-sektor-isletme-finansal-degerleme-kontrol-listesi.md | R240 · 2026-08-28 12:35 UTC · Şirket Değerlendirme Sektör İşletme Finansal Kalite ve Değerleme Kontrol Listesi | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | konu eşleşmesi (TF-IDF kosinüs 0.19; düşük skorlar elle doğrulandı) |
| YENİ: gorsel-paket-131-alka-elliott-wave2-fvg-temas.md | R241 · 2026-08-28 12:42 UTC · Bu hissede ne oldu bugün, gelin hep beraber bakalım. 1. Piyasa Yapısı … | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: gorsel-paket-132-fvg-yukselen-dipler-wave3-abc-duzeltme.md | R242 · 2026-08-28 12:43 UTC · FVG Stratejisi Açısından Grafik Analizi: Neden Yükselen Dipler Daha Ön… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: tweet-fvg-ticaret-stratejileri-gap-fading.md | R243 · 2026-08-28 12:44 UTC · FVG Ticaret Stratejilerini de kısaca anlatalım mesai başlamadan, bugün… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| YENİ: gorsel-paket-133-medyan-kanal-kullanimi.md | R244 · 2026-08-28 12:45 UTC · Medyanı şöyle bir kanal gibi kullanın arkadaşlar. Biraz üzerinde düşün… | rollout-2026-08-27T17-07-59-01a0438c-8d59-7531-b2b0-25a6d2efd79d.jsonl (2026-08-28) | beyinde eşleşme yok |
| kaynak-aefes-yukselen-kanal-alt-bant-2096582181170598078.md | R245 · 2026-09-06 12:58 UTC · kaynak notu: AEFES Yükselen Kanal Alt Bant Teması ve Tepki | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-80-100-hafta-yatay-tarama-2096580811080261784.md | R246 · 2026-09-06 13:02 UTC · kaynak notu: 80–100 Hafta Yatay Hisse ve Bant Dibinde Bekleme Fikri | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-dusen-yapi-retest-2096577500612624410.md | R247 · 2026-09-06 13:03 UTC · kaynak notu: Düşen Üst Sınır Kırılımı ve Retest — Sembol Belirtilmemiş | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-dusen-yapi-kirilim-2096576027791131079.md | R248 · 2026-09-06 13:05 UTC · kaynak notu: Düşen Üst Sınırda Yeşil Kırılım Mumu — Sembol Belirtilmemiş | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-three-drives-2096510322190201208.md | R249 · 2026-09-06 13:22 UTC · kaynak notu: Three Drives — Üç İtiş Fibonacci Fiyat ve Zaman Simetrisi | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-doas-kelebek-2096505383955079277.md | R250 · 2026-09-06 13:24 UTC · kaynak notu: DOAS Kelebek — D Noktası Tamamlanma ve Tepki Adayı | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-vakbn-garan-rotasyon-2096358189696520213.md | R251 · 2026-09-06 13:26 UTC · kaynak notu: VAKBN–GARAN Göreli Değer Rotasyonu — Kaynak Performans Raporu | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-xu100-corwin-schultz-2096145981062475910.md | R252 · 2026-09-06 13:29 UTC · kaynak notu: XU100 Corwin–Schultz — Spread Tahmini ve Düşük Sigma Sınırı | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-akfis-breakout-fvg-retest-2095523694881697974.md | R253 · 2026-09-06 13:31 UTC · kaynak notu: AKFIS Kırılım FVG Retest ve Teyit — Kaynak Örneği | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| YENİ: kaynak-tansu-2095218573631279414.md | R254 · 2026-09-06 13:33 UTC · yalnız bağlantı (notu yok) | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | beyinde eşleşme yok |
| not-backtest-giris-sadeligi-risk-islem-gunlugu.md | R255 · 2026-09-06 13:34 UTC · kaynak notu: Backtest ile Giriş Kurallarını Sadeleştirme ve İşlem Günlüğü | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| YENİ: kaynak-tansu-2095201144544846208.md | R256 · 2026-09-06 13:36 UTC · yalnız bağlantı (notu yok) | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | beyinde eşleşme yok |
| kaynak-xu100-bekle-teyit-2095196517577461974.md | R257 · 2026-09-06 13:36 UTC · kaynak notu: XU100 2 Eylül — Bekle ve Teyit Ara Senaryosu | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-xu100-1-eylul-2094850165920403866.md | R258 · 2026-09-06 13:39 UTC · kaynak notu: XU100 1 Eylül — WMA Altı ve Dört Saatlik Zayıf Yapı | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-ahenk-demand-2094486927328059452.md | R259 · 2026-09-06 13:41 UTC · kaynak notu: Ahengin Uyumu — Demand Bölgesi ve Gösterge Görünümü | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-cwene-skewness-2094148699769241961.md | R260 · 2026-09-06 13:43 UTC · kaynak notu: CWENE — 63 Günlük Skewness Gaussian ve Kuyruk Riski | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-cwene-dalga2-demand-2094128312729624792.md | R261 · 2026-09-06 13:45 UTC · kaynak notu: CWENE — Olası Dalga 2 ve Demand Örtüşmesi | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-kointegrasyon-sinirlari-2093658795700338821.md | R262 · 2026-09-06 13:47 UTC · kaynak notu: Kointegrasyon ve İkili İşlem — Korelasyon Ayrımı ve Garanti Sınırı | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
| kaynak-bom-iki-tavan-2093647837162553475.md | R263 · 2026-09-06 13:49 UTC · kaynak notu: BOM Sinyali — İki Tavan Kaynak İddiası | rollout-2026-09-06T15-04-02-01a0769a-a9fa-7fd1-9609-e34b14e9b883.jsonl (2026-09-06) | source_url (tweet kimliği) |
