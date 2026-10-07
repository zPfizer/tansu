# Denetim: X arşivi sınıflama işi (bağımsız denetçi)

## Denetim 1 · 07.10.2026

Kapsam: orkestratörün 7 iddiası, dilim 1 çıktıları (Opus, Sonnet, Codex), kod kitabı sürüm 2, süreç.
Yöntem: sayılar `python -c` ile dosyalardan yeniden hesaplandı. 11 görsel Read ile açıldı. Dosya oluşturulmadı.

### Hüküm: KOŞULLU

Veri toplama sağlam. Sayılar doğru. Üç sınıflayıcı da görselleri gerçekten okuyor.
Ama tam koşu şu haliyle başlarsa tekrar koşu riski yüksek. Sebepler:
1. Python kodu hiç sınanmadı. Dilim 1'de kod yok.
2. Kod kitabında "kural" tanımı iki türlü okunuyor.
3. Ayrışmaları kimin, nasıl çözeceği belli değil.
4. Pilotta bir hesap hatası var. Bu hata defter karşılaştırmasına girecek.

---

### b) 7 iddianın yeniden hesabı

| # | İddia | Sonuç | Derece | Kanıt |
|---|---|---|---|---|
| 1 | 8.785 (5.366 ana, 3.419 yanıt); ana kapsam ~%99 | Sayılar DOĞRU. Kapsam ~%99 DOĞRU (683 ana gönderinin 5'i eksikti: %0,7). README etiketi YANLIŞ. | ORTA | README.md:17 "777 ana gönderinin 8'i" diyor. 777 = 683 ana + 94 Tansu'nun kendi zincirine yanıtı. Eksik 8'in 5'i ana, 3'ü kendi-zincir yanıtı. Kendi-zincir yanıtında kaçırma %3,2 (3/94). İkisi strateji içerikli: 2089812316619497553 "Sistem, belirli bir geçmiş veri penceresindeki…", 2090511182939480106 "mevcut fiyat ile 5.48 arası hacimli barlar…". Başkalarına yanıtın kapsamı hiç ölçülmedi. |
| 1b | "Günlük deneme (2026-08-18 haftası): 172 gönderi, arşivde olmayan 0" | YENİDEN ÜRETİLEMEDİ | ORTA | Arşivde 18–25.08.2026 (UTC) 150 gönderi var, 172 değil. Eksik bulunan 3 yanıttan 2'si tam bu haftada. 172 kimlik listesi kayıtta yok. README.md:18 |
| 2 | Haziran–Temmuz 2026 düşüklüğü gerçek | Sayılar DOĞRU (profil kendi gönderisi 16 ve 5; arşivde ana 15 ve 5). "Gerçek" sözü fazla güçlü. | DÜŞÜK | İki liste de aynı X kaynağından. Silinmiş gönderiyi ayırt edemez. Doğru ifade: "iki uçta da düşük". |
| 3 | Medya 3.026, hata yok; üst metin 2.731 (2.154 / 577) | DOĞRU | — | 3.026 URL, 3.026 dosya, eksik 0. 8 dosya <2 KB ama geçerli PNG. 577 = 369 silinmiş (404) + 208 korumalı (401). 579 yanıtın üst metni yok. |
| 3b | (söylenmeyen) | 14 dosya video (mp4). Read video açamaz. Plan yok. 367 üst gönderinin görseli indirilmedi. 681 alıntılı gönderi var; alıntının görseli yok, 44'ünde alıntı metni boş. README.md:12 "kod adayı gönderilerin görselleri" diyor; gerçekte tüm görseller indirildi. | ORTA | `python -c` sayımları |
| 4 | Uyum rol 41/50, kural 46/50, kod 50/50; ayrışmanın 6/9'u kod kitabı boşluğundan | Sayılar DOĞRU. 6/9 makul (9, 21, 22, 29, 38, 41 numaralı gönderiler sürüm 2 kurallarına denk). "Kod 50/50" BİLGİ TAŞIMIYOR. | YÜKSEK | Dilim 1'de kod yok; 50/50 yalnız "yok = yok". Uyum doğruluk değil: Opus ve Sonnet #10'da aynı hatayı yaptı ("4 fiyatın ortalaması"; aşağıya bakın). Codex eklenince üçlü rol uyumu 33/50, kural 38/50. |
| 5 | Tansu 40/60'ı 2023'te kullanmış (128,42 = 0,4×120,49 + 0,6×133,71) | Aritmetik DOĞRU (128,422). İfade YANILTICI. | YÜKSEK | 0,4 çarpana, 0,6 İNA'ya gider. 2026 kuralı tersidir: defter-3.md:178 R151 "İNA'sonucunun %40'ı … çarpan … %60'ı"; defter-2.md:18 R068 aynı. 2023'te çarpan %40 / İNA %60 kullanılmış. Bunun doğrudan metin kanıtı dilim 1'de var: 1708030356564160854 (TTRAK) "Çarpanlar %40, İNA %60 ağırlıklandırılarak". Görselde 0,4×785,30 + 0,6×2.116,93 = 1.584,28 tutuyor. Opus "görselde yazılı değil" diye çıkarım sundu; metin kanıtı aynı dilimde duruyordu. |
| 6 | ~105 bin token / 50 gönderi; tam koşu ~37 M (±%30) | Aritmetik DOĞRU (176×105 bin×2 = 36,96 M). Dayanak YOK, alt sınır gibi. | ORTA | Ölçüm kaydı yok. Dilim 1 temsil etmiyor: toplam metin 1,97 M karakter; dilim 1×176 = 1,27 M (%56 eksik). Görsel ×176 = 3.344, gerçek 3.026. Kod çevirisi (uzun birebir çıktı) dilim 1'de hiç yok. Ayrışma çözümü ve Codex maliyeti hesapta yok. |
| 7 | Pilot çözüm kararları tanımla tutarlı | KISMEN YANLIŞ | YÜKSEK | Aşağıda. |

#### İddia 7 ayrıntısı (siniflama.md)
1. siniflama.md:20 (#5, 1695389783147581542): "2023'te dört yöntem eşit ağırlık … eşit ortalama 143,98" YANLIŞ. Dört fiyatın eşit ortalaması 152,97. Görseldeki 143,98 = 0,4 × (47,12+269,47+161,59)/3 + 0,6 × 133,71. Yani 2023'te de ağırlıklı ortalama var; yön 2026'nın tersi. "Çelişir" sonucu doğru, gerekçesi yanlış. Bu satır düzeltilmedi. Orkestratörün iddia 5'i bu satırla çelişiyor.
2. Pilot kararları ile dilim 1 sonuçları 3 gönderide ayrışıyor. Üç sınıflayıcı da aynı yönde ayrıştı:
   - 1695389783147581542: pilot `tam`; Opus, Sonnet, Codex `cekirdek`.
   - 1695424938251796654 (karlılık tablosu): pilot `yok`; üçü `cekirdek`.
   - 1695107146369671497 (Günün Dikkat Çekenleri): pilot `fikir`; üçü `cekirdek`.
   Pilot "doğru cevap" olarak kullanılamaz. Bu, tanım sorununun işareti (bölüm c).
3. siniflama.md:32 #4'te orkestratör iki sınıflayıcının ortak kararını değiştirdi. Bunu açıkça yazdı (iyi). Ama aynı gerekçe 1695389783147581542'yi de `tam` yapıyor; dilim 1'de bu uygulanmadı.
4. Pilot uyumu "rol 8/10, kural 7/10" (siniflama.md:12): pilot A/B ham çıktısı klasörde yok. Doğrulanamadı. DÜŞÜK.

### b) Örneklem: 15 gönderi, görseller açıldı

Doğru cevap kod kitabı sürüm 2'ye göre benim kararım. Opus ve Sonnet sürüm 1 ile koştu; sürüm 2'nin yeni kurallarındaki hataları buna bağlı olabilir.

| # | id | Doğru (rol / kural) | Opus | Sonnet | Codex | Not |
|---|---|---|---|---|---|---|
| 5 | 1694839230298468742 | değerleme-temel / çekirdek | ✓ | ✓ | ✓ | Görseli açmadım; üçünün değerleri birbiriyle aynı |
| 6 | 1695107146369671497 | seçim-momentum / çekirdek | ✓ | ✓ | ✓ | Pilot `fikir` bence yanlış |
| 7 | 1695183583676113357 | değerleme-temel / tam | ✓ | ✓ | ✓ | Üçü de %150/%100 çelişkisini ve 2024T, 2030T tekrarını gördü |
| 10 | 1695389783147581542 | değerleme-temel / çekirdek | ✓ rol, ✗ görsel yorumu | ✓ rol, ✗ görsel yorumu | ✓ | Opus ve Sonnet "4 fiyatın ortalaması" yazdı; yanlış. Codex "ağırlık verilmemiş" dedi |
| 12 | 1695424938251796654 | değerleme-temel / belirsiz (yok mu çekirdek mi) | ? | ? | ? | Tanım boşluğu |
| 13 | 1695433615130210730 | rejim / fikir | ✓ | ✓ | ✓ | Opus ve Codex alıntıyı görselden aldı; birebir doğru |
| 15 | 1696021655947018369 | bölge / çekirdek | ✓ | ✓ | ✓ rol, ✗ değer | Codex 3 aylık "77,15" yazdı; görsel 77,13 |
| 22 | 1698267718074438032 | değerleme-temel + seçim-momentum / çekirdek | ✗ rol (sürüm 1) | ✓ | ✓ | |
| 29 | 1699802936337957180 | çıkış / yok | ✓ | ✗ | ✓ | Kod kitabının kendi örneği; sızıntı (bölüm a) |
| 33 | 1700833478101581909 | sohbet-duyuru / yok | ✓ | ✓ | araç-öğrenme | Codex kitap adlarını doğru okudu; uydurma yok |
| 34 | 1701252666364395617 | sohbet-duyuru / yok | ✓ | ✓ | ✗ (rejim/fikir) | "ev fiyatları asla düşmez": strateji değil |
| 38 | 1706542464125776037 | değerleme-temel (sürüm 2) | ✗ (sürüm 1) | ✓ | ✓ | |
| 43 | 1708030356564160854 | değerleme-temel / çekirdek | ✓ | ✓ | ✓ | 1.584,28 hesabı tutuyor |
| 44 | 1708049006742417472 | değerleme-temel / çekirdek | ✓ | ✓ | ✓ | Sonnet 128,42'yi açıklayamadı; #43 aynı dilimde cevabı veriyordu |
| 46 | 1708402706233147744 | sohbet-duyuru / yok | ✓ | ✓ | ✗ (değerleme-temel) | Duyuru |

Karar verilebilen 14 gönderide rol: Opus 12/14, Sonnet 13/14, Codex 12/14.
Görsel okuma: üçü de görseli gerçekten açmış. Değerler birebir tutuyor. Tek okuma hatası Codex #15.
Alıntı birebirliği (`python -c`, alıntı metinde alt dize mi): Sonnet 50/50. Opus 49/50 (#13 görselden, doğru). Codex 48/50: #13 görselden (doğru); #50 alıntısı Tansu'nun metninde değil, alıntıladığı #38'den. Alıntının kaynağı (metin / görsel / alıntılanan gönderi) şemada yok.
Sonnet grafikten tahmini değer yazdı ("son değer yaklaşık 4,4", "yaklaşık 13,2", "yaklaşık 3"). kod-kitabi.md:16 "Tahmin yazılmaz" der. DÜŞÜK.
Hiçbir sınıflayıcı #15'teki formülü çıkarmadı: "dipten uzaklık %" = (son − dip) / (zirve − dip). DOAS haftalık (279,70−271,10)/(325,81−271,10) = %15,72; 3 aylık %77,13. Ölçü yeniden üretilebilir; "kural" kararı buna göre değişebilir. ORTA.

### a) Süreç

| Bulgu | Derece | Kanıt |
|---|---|---|
| Python kodu birebir çıkarma hiç sınanmadı. Dilim 1'de kod yok. Birebirliği doğrulayan adım yok (ör. sözdizimi denetimi, iki bağımsız yazımın karşılaştırması). Levent'in "Python kodları çok önemli" talimatı en zayıf yerde kalıyor. | YÜKSEK | 3 sınıflayıcıda `kod` 50/50 "yok". Kod anahtar kelimeli gönderi 1.224, 405'i görselli. |
| Ayrışma çözümü planı yok. Rol uyumu %66–82 ise tam koşuda ~1.600–3.000 ayrışma çıkar. Kim çözecek, hangi biçimde kaydedilecek, maliyeti ne? Token tahmininde yok. | YÜKSEK | iddia 4; siniflama.md:27 yalnız pilot için elle çözüm |
| Tam koşudaki "iki sınıflayıcı" belirsiz. 37 M tahmini iki sınıflayıcı der; şimdi dilim 1'de üçüncü olarak Codex koşuyor. Hangi ikisi? Levent'e söylendi mi? Codex'e verilen istem dosyada yok; yeniden üretilemez. | ORTA | siniflama/codex/001-*.jsonl (10:02–10:05) |
| Sürüm izi yok. Kayıtlarda `surum` alanı yok. Opus/Sonnet kayıtları sürüm 1 (`hedef` alanı yok); Codex sürüm 2. kod-kitabi.md:3 "önceki dilimler işaretlenir" diyor; işaret mekanizması yok. | ORTA | anahtar sayımı: O/S 15 alan, Codex 16 alan |
| Sızıntı: sürüm 2 dilim 1 ayrışmalarından yazıldı ve dilim 1'den örnek içeriyor ("128-140 bandına oturacak" = #29). Dilim 1 artık bağımsız ölçüm değil. Sürüm 2 başka bir dilimde ölçülmedi. | ORTA | kod-kitabi.md:5 |
| Kaldığı yerden devam: grup başına dosya (001-01 … 001-10) iyi. Ama dosyaların son satırında satır sonu yok. Dosyalar uç uca eklenirse iki kayıt tek satıra yapışır. Şema doğrulayıcı yok. | DÜŞÜK | 10 dosyada `endsNL False` |
| Okuma kuralı eksik: alıntılı gönderi (681), görseli olan üst gönderi (367), üst metni alınamayan yanıt (579), video (14) için kural yok. | ORTA | kod-kitabi.md:13–17 |
| siniflama.md:4 "Sıra: ana gönderiler" diyor; dilimler yanıtları da içeriyor (dilim 1: 23 yanıt). Kapsam değişimi belgede güncel değil. | DÜŞÜK | dilimler.json, siniflama.md:4 |
| İyi olan: dilimler eksiksiz (8.785 kimlik, tekil, zaman sırası, 1.757 grup × 5). 5'erli talimata uyuldu. Görseller okunuyor. | — | `python -c` denetimi |

### c) Kod kitabı: belirsiz yerler

1. **`kural: tam` iki türlü okunuyor (YÜKSEK).** Hesap tablosu girdileriyle verilince `tam` (pilot #3, #4). Ama "FK 2-3 al, 7-5 sat" gibi tüm eşikleri yazılı işlem kuralı `çekirdek` (kod-kitabi.md:65). siniflama.md:29 "işlem kuralı yok; bu rolün konusu" diyor. Okuyucu "tam"ın hesabı mı, işlemi mi ölçtüğünü bilemez. Öneri: iki alan (`hesap_tam`, `islem_kurali`) ya da tek, örnekli tanım.
2. **Veri tablosu (YÜKSEK).** Karar eşiği olmayan oran tablosu (karlılık, skor tablosu) `yok` mu, `fikir` mi, `çekirdek` mi? Pilot ve üç sınıflayıcı ayrıştı.
3. **`çıkış` tahmini de kapsıyor (ORTA).** "Sene bitmeden 128-140" bir fiyat tahmini; sistemin çıkış kuralı değil. `çıkış` rolü tahminle dolarsa defter karşılaştırmasında gerçek çıkış kuralları (stop, kâr alma) kaybolur. Öneri: rol `sohbet-duyuru` ya da yeni `tahmin`; fiyat `hedef` alanında kalsın.
4. **Yöntem başka gönderideyse (ORTA).** #21 ("detaylar yarın"), #50 (alıntılanan gönderi "finans matematiği" der). Yöntem önceki ya da alıntılanan gönderide söylenmişse ne yazılacak? Yazmıyor.
5. **Kısa piyasa görüşü yanıtları (ORTA).** Codex 7 yanıtı içerik rolüne koydu (#3, #11, #34, #39, #40, #46); Opus ve Sonnet `sohbet-duyuru` dedi. Sınır: "ölçü ya da eşik yoksa sohbet-duyuru" gibi açık bir kural lazım.
6. **Küçük (DÜŞÜK):** `semboller` biçimi (TUPRS mı TÜPRAŞ mı); grafikten okunan yaklaşık değer "tahmin" mi; alıntı kaynağı alanı; üst metni olmayan yanıt için ne yazılacağı.

### d) Codex çıktısı (siniflama/codex/001-01…10)

- Şema: 50 kayıt, 16 alan, sürüm 2'ye uygun. DOĞRU.
- Kimlik sırası: 10 grubun hepsi dilimler.json ile aynı. DOĞRU.
- Görsel okuma: 19/19 `true`. Örneklediğim 7 görselde değerler tutuyor. 1 hata: #15 "77,15" (görsel 77,13).
- Uydurma: bulunmadı. Kitap adları (#33), karlılık tablosu (#12), skor tablosu (#6) görselle aynı. Açılan görseller: #6, #7, #10, #12, #13, #15, #24, #31, #33, #43, #44.
- Eğilim: yanıtları fazla içerik rolüne koyuyor (bölüm c-5). #50 alıntısı yanlış kaynaktan. `hedef` alanına metindeki yazım hatasını (1116.54) taşıdı; görsel 116,64 der; not düşmedi.
- Artı: #10'da "birleştirme ağırlıkları verilmemiş" diyerek Opus/Sonnet'in hatasına düşmedi.

### e) Orkestratörün davranışı

1. İddia 5 Levent'e "40/60'ı 2023'te kullanmış" diye gitti. Hangi yöne 40, hangi yöne 60, söylenmedi. Gerçekte 2026 kuralının tersi. Aynı orkestratörün pilot satırı "eşit ağırlık" diyor ve düzeltilmedi. YÜKSEK.
2. "Kod 50/50" uyum olarak raporlandı. Kod çıkarma sınanmadı; bu söylenmedi. YÜKSEK.
3. Token tahmini ±%30 güvenle verildi; ölçüm kaydı yok; dilim 1'in temsil gücü sınanmadı. ORTA.
4. "Gerçek" (Haziran–Temmuz), "~%99" gibi ifadeler kanıttan güçlü. README'deki 777/172 sayıları yanlış ya da doğrulanamaz. ORTA.
5. Codex'i üçüncü sınıflayıcı olarak başlattı; plan belgelerinde yok; maliyet tahminine girmedi. Levent'e bildirildiği dosyalardan görünmüyor. ORTA.
6. İyi: pilot #4'teki kendi kararını açıkça yazdı. Sürüm 2 farklarını gerekçesiyle belgeledi. Sayılar uydurma değil.

### Düzeltme listesi (öncelik sırasıyla)

1. Kod çıkarmayı tam koşudan ÖNCE sına: kodlu 10–15 gönderilik bir deneme dilimi seç; iki sınıflayıcı kodu ayrı yazsın; satır satır karşılaştır; Python ise sözdizimini denetle. Birebirlik oranını Levent'e bildir.
2. siniflama.md:20 satırını düzelt: 143,98 = 0,4 × çarpan ortalaması + 0,6 × İNA. 2023: çarpan %40 / İNA %60 (TTRAK metni ve SAYAS iki görseli); 2026 (R068, R151): tersi. Levent'e iddia 5'i yönüyle yeniden söyle.
3. Kod kitabında `kural` tanımını tek anlama indir (c-1, c-2). Sürüm 3 yap.
4. Ayrışma çözüm planını yaz: kim çözer, kayıt biçimi, maliyet. Token tahminine ekle.
5. Tam koşuda hangi iki sınıflayıcının çalışacağını ve Codex istemini dosyaya yaz; Levent'e bildir.
6. Sürüm 3'ü dilim 1 DIŞINDA, kodlu ve 2026 dönemli bir dilimde ölç (sızıntısız).
7. Her kayda `surum` ve `alinti_kaynak` (metin / görsel / alıntı / üst) alanı ekle. Grup dosyalarını satır sonuyla bitir. Koşudan sonra şema doğrulaması yap.
8. Okuma kuralını tamamla: alıntılı gönderi, üst gönderi görseli (367), üst metni alınamayan yanıt (579), video (14).
9. Token tahminini metin ve görsel hacmine göre yeniden hesapla (metin %56 fazla); kod çevirisi çıktısını ekle.
10. README'yi düzelt: "777 ana" → "683 ana + 94 kendi-zincir yanıtı; eksik 5 ana, 3 yanıt"; 172 kimlik listesini kaydet ya da iddiayı kaldır; `medya/` tanımını güncelle.
