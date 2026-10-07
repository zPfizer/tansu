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

## Tur: hakem talimatı ve ön karşılaştırma (07.10)

Kapsam: siniflama/hakem-talimat.md (K1, K2, örnekler), opus-v5 (176 dosya, 8.785 kayıt), codex-v5 (yalnız `.jsonl`).
Yöntem: sayılar `python -c`/stdin ile yeniden hesaplandı. Ayrışan gönderilerin hepsinin metni, üst metni ve alıntısı okundu.
28 görsel Read ile açıldı (6'sı ayrışan, 22'si iki okuyucunun da `kod: yok` dediği kod adayı). Bağlantıların hiçbiri açılmadı.
Codex denetim sırasında yazmaya devam etti. Sayılar üç kez değişti (aşağıda).

### İddiaların sonucu

| # | İddia | Sonuç | Kanıt |
|---|---|---|---|
| 1 | 4.155 ortakta rol %81,2, kural %86,7, kod %98,9 | DOĞRU | İlk 831 Codex dosyasıyla birebir aynı çıktı: 4.155; 81,2 / 86,7 / 98,9; 45 ayrışma. Son durum: 951 dosya, 4.755 ortak gönderi; rol %81,5, kural %86,5, kod %98,9; `kod` var/yok ayrışması 52. Kod uyumu çoğunlukla "yok = yok" (Opus 8.543/8.785 `yok`). |
| 2 | 45 ayrışmanın hemen hepsi (a) üst/alıntı kodu, (b) açılmamış bağlantı; okuyucu hatası değil | KISMEN | 4.155'te 40/45 (a)+(b), 5'i değil. 4.755'te 33 (a) + 10 (b) + 9 başka = 52. "Okuyucu hatası değil" sözü 2 gönderide yanlış (ORTA-1). |
| 3 | K1, Ayırma kuralı 6 ile tutarlı ve kod kaybettirmez | KISMEN | Kural 6 ile tutarlı. "Kod kaybettirmez" YANLIŞ: Tansu'nun kaydı olmayan kendi üst gönderilerinde kod kaybolur (YÜKSEK-1). Başkasının kod bağlantısı da kaybolur (ORTA-3). |
| 4 | K2 doğru sınır | KISMEN | Yön doğru. Ama karar Tansu'nun cümlesine bağlı. Aynı tür gönderi, okuyucular uyuştuysa `baglanti`, ayrıştıysa `yok` olabilir (ORTA-2). |
| 5 | Örnek kararlar doğru | ÇOĞU DOĞRU | 1783149446089383961 ve 1829983002304086142 doğru. 1842658091239694553 kararı doğru, gerekçesi eksik (DÜŞÜK-1). 1770856035709817030 kararı doğru ama K2'nin ilk maddesiyle lafzen çelişir (DÜŞÜK-2). "Görsel açılıp karar verilir" denen 4 gönderi için kural yok (ORTA-1). |

### YÜKSEK

**Y-1. K1 Tansu'nun kaydı olmayan kendi üst gönderisinde kodu kaybettirir.**
K1 "Üst gönderi Tansu'nunsa: o gönderinin kendi kaydı kodu taşır" der. Bu, üst gönderi tweets.jsonl'de varsa doğrudur. Sınadım: 8 kendi-üst ayrışmasının (1761491657529213237, 1784693133978059014, 1826114685084561492, 1904748990458900518 vb.) üst kayıtlarında iki okuyucu da kodu taşıyor.
Ama Tansu'nun yanıt verdiği 45 kendi üst gönderisi tweets.jsonl'de YOK. 24'ü ust.jsonl'de "hata" (alınamadı). 21'inin metni ust.jsonl'de var, kimliklerinin hepsi arşiv aralığında. Bu 21 gönderinin sınıflama kaydı yok, görselleri indirilmedi. K1'e göre yanıt `yok` olur, üstün de kaydı yok; kod hiçbir yere yazılmaz. Kod izi olanlar:
- 1845380189410201878: "Kod güncellendi / Para akışı da yazılacak koda", 2 görsel (indirilmedi, okunmadı). Yanıtları 1845728745040068881 ve 1845381519147176179: iki okuyucu da `yok`.
- 1911030879519994288: HBK hesaplayan kodu adım adım anlatıyor, 1 görsel (okunmadı). Yanıtı 1911030882531418617: ikisi de `yok`.
- 1897595121345966255: "Yataysütun birleştirme", 1 görsel (okunmadı). Aynı dizinin yanıtı 1897595124877517216 "Keys kullanımı" görselinde kod var (iki okuyucu `gorselde`). Üstte de kod olup olmadığı okunmadı.
- 1906617990407196857: "bir Python kodu yazdım"; görsel yok, metinde kod yok.
Bu, ayrıca bir toplama boşluğudur: arşivde 21 Tansu gönderisi eksik. Denetim 1'de kendi-zincirde 3 eksik bulunmuştu; bu sayı daha büyük.
Düzeltme: bu 21 gönderiyi (medyasıyla) sınıflamaya ekle. Ya da K1'e istisna yaz: "Tansu'nun üst gönderisinin kaydı yoksa hakem kodu ust-kod.jsonl'e yazar."

### ORTA

**O-1. Üçüncü bir kitap boşluğu var. Talimat bunu kapatmıyor (iddia 2).**
(a) ya da (b) olmayan ayrışmalar, 52'den 9'u:
- Tansu'nun kendi metninde fonksiyon adı ya da parametre: 1826740082239570089 ("qf.iplot kodu çalıştır"), 1922905765708251592 (`read_csv()`, `np.where()` listesi), 1922994519655538765 (`print()`), 1925633169694277851 ("range = 30"). Codex `metinde`, Opus `yok`.
- Matematik formülü kod mu: 1925561082392834472 (metinde "C = BS(S, K, r, T, σ)"), 1851750265239609482 (görselde Excel; "(E_est/3-1)^2 + (sigma_E/0.8-1)^2" ve Merton formülleri; görseli açtım). Kitap "Formül dili de koddur" der. Bu formüllerin gösterge dili mi matematik mi olduğu tanımlı değil. Aynı durumda iki okuyucu birlikte `yok` dedi: 2087251201691685145 (görselde "FAVÖK (YoY) = [3H + 4B](t) / [3H + 4B](t-1yıl) - 1"), 1985831305662050335 ("W1*1.618"). Ben ikisini de açtım.
- Fotoğrafın arka planındaki ekran: 1891183558858883162 (kitap kapağının arkasında bulanık kod; okunamıyor), 1893725545260544026 (yalnız "plt.show()" okunuyor; altta grafik çıktısı), 1892643772430766103 (Gartley program çıktısı; sağ kenarda silik, okunamayan kod parçaları). Üçünü de açtım. Bence üçü de `yok`: okunabilir, paylaşılan kod yok.
Okuyucu tutarsızlığı: Codex 1891183558858883162 ve 1893725545260544026'da arka plan kodu için `gorselde` dedi. Aynı durumda (kitap fotoğrafı, arkada okunamayan ekran) 1842520794586341379'da `yok` dedi; görseli açtım. Bu bir kitap boşluğu değil, okuyucu tutarsızlığıdır. İddia 2'deki "okuyucu hatası değil" sözü bu iki gönderi için yanlış.
Talimat bu 4 görselli gönderiyi "görsel açılıp karar verilir" diye bırakıyor; karar kuralı vermiyor. Hakem kuralsız karar verir.
Düzeltme: K3 ekle: "Okunamayan ya da paylaşım konusu olmayan arka plan kodu → `yok`. Metinde yalnız fonksiyon adı/parametre → `yok`, notta adlar. Matematik formülü → kod değil, `parametreler`e."

**O-2. K2 sözcüğe bağlı. Ayrışan ve uyuşan kayıtlar arasında tutarsızlık yaratır.**
Tansu'nun kendi metninde dosya bağlantısı (we.tl, colab, github, drive, tradingview script) 65 gönderide var. Opus: 56 `baglanti`, 6 `yok`, 3 `gorselde`. Bağlantı dışındaki metinde K2'nin anahtar sözcükleri (kod, Python, indikatör, tarama, dosya, kullan, dene) 19 gönderide yok. Bu bir düzenli ifade yaklaşımıdır; hakem anlamdan da karar verebilir. Bu 19'un 13'ü şimdi en az bir okuyucuda `baglanti`. Örnek: 1797024166698176638 "Jupiter file … dataset", 1845164267789512855 "Vegas tüneli stratejisini bir daha yolluyorum", 1939327640332050705 "Alın geliştirin".
K2 yalnız ayrışan kayıtlara uygulanır. Sonuç: 1840777067882787015 (ölçütler + we.tl + program çıktısı) K2'ye göre `yok` olur. Aynı türden 1847558481227702504 ("200EMA 50 EMA CMF RSI" + we.tl) iki okuyucuda `baglanti` kalır.
Maliyetler aynı değil. Yanlış `baglanti` bir deneme açılışına mal olur. Yanlış `yok` bağlantıyı deneme aşamasından kalıcı olarak çıkarır.
Düzeltme: alan adına göre kural: Tansu'nun metnindeki dosya/kod barındırma bağlantısı → `baglanti`. LinkedIn ve haber sitesi → `yok`.
Not: we.tl bağlantıları geçicidir (1781980143747010739: "1 hafta süresi var"). Hiçbir bağlantıyı denemedim. Deneme aşamasının ne kadar kod kurtaracağı bilinmiyor.

**O-3. ust-kod.jsonl şemasında bağlantı alanı yok.**
K1 yalnız `kod_metni` yazar. Başka kullanıcının kodu metin değil bağlantıysa hiçbir yere gitmez. Ayrışmalarda 6 gönderi: 1824958910681264505 (github), 1840862040719835352 (colab), 1847661816442184171 (colab), 1845228714109329533 (tradingview; Tansu "Bunu yaptık … tavan da yakaladık" diyor, yani uyguladı), 1912597066033078607 (tradingview), 1843387861770612872 (alıntıda tradingview; Tansu "python taramasını yazacağım").
Düzeltme: şemaya `baglanti` alanı ekle. Bu kayıtları bağlantı deneme aşamasına da gönder.

**O-4. Sayılar koşu sırasında değişiyor.**
Denetim sırasında ortak gönderi 4.590 → 4.755 oldu, ayrışma 48 → 52 oldu. Talimat "45 ayrışmadan" diye yazıldı. Yeni ayrışmalar (1912597066033078607, 1913270044257124805, 1922905765708251592, 1922994519655538765, 1925561082392834472, 1925633169694277851, 1925863641338859943) talimattaki örneklere girmedi. Bunların 4'ü O-1 türünde. 4.155 anındaki 45 ayrışmadan biri sonraki dosya kümesinde ayrışma değil (45 + 4 yeni ≠ 48). Hangisi olduğunu araştırmadım.
Düzeltme: hakem talimatını Codex bitince son ayrışma listesiyle yeniden sına.

### DÜŞÜK

**D-1. Örnek 1842658091239694553 gerekçesi eksik.** Talimat "kod Tansu'nun üst gönderisinde (we.tl)" der. Üst gönderi 1842657804374720958'in iki kaydı da `gorselde` (Python kodu görselde). Metindeki we.tl ("txt dosyası yukarıda") kayda geçmedi, çünkü `kod` tek değerlidir. Ayrıca Opus notuna göre yanıt, kendi kodunu düzeltiyor (kod RSI <= 30'da al veriyor; yanıt "RSI > 30" diyor). K1 yanıtı `yok` yapınca bu düzeltme kod aşamasında görünmez. Düzeltme: K1 yanıtında notta "üst kodu düzeltiyor: …" yazılsın.

**D-2. Örnek 1770856035709817030 K2'nin ilk maddesiyle lafzen çelişir.** Metin "Python çalışmalarım linkedin sayfamda" der. İlk madde ("Python dosyası olduğunu söylüyorsa") bunu `baglanti` yapar. Karar ancak ikinci maddedeki "LinkedIn profili" örneğiyle `yok` olur. Kuralın sırası açık değil.

**D-3. `tansu` alanı eksik değerli.** Değerler: onayladı, uyguladı, övdü, çevirecek. 1853136887961043422 ("Diğer bullish sinyallerini de lütfeder misin") ve 1847661816442184171 ("yazsana stratejiyi") istek bildiriyor. 1913270044257124805 bir şaka. Bunlar için değer yok.

**D-4. Okunmayan videolarda `kod: yok`.** 10 video gönderisinde Opus `gorsel_okundu: false` ve `kod: yok` yazdı (ör. 1773715205274403212, 1863989280688746532). İçerik okunmadı. `yok` burada bir tahmindir. Kod kitabının "Tahmin yazılmaz" kuralıyla çelişir.

### Ortak hata taraması (iki okuyucu da `kod: yok`)

22 kod adayı görseli açtım. Seçim: metin ya da görsel özeti kodu anıyor ("kod yazdım", "Python", "tarama kodu", "program çıktısı").
Açılanlar: 1840307089429651792, 1842520794586341379, 1870623312260513908, 1871248456964329949, 1900500470029795548, 1900483420456653124, 1907840096851624360, 1907860073239683477, 1909130007827317168, 1962942414391283988, 1964205713430876532, 1980136440672465307, 1985831305662050335, 2043089809359466951, 2087251201691685145, 1889451595584115079, 1763696979119382658, 1837875098834882936, 1845558544126366115 (1. görsel), 1957917338571051457, 2003227972720033858, 2039748457804550392.
Sonuç: hiçbirinde okunabilir kod yok. Hepsi program çıktısı (grafik, konsol tablosu), kitap, uygulama ekranı ya da caps. Kural 7'ye göre `yok` doğru. Tek istisna formül satırları (2087251201691685145, 1985831305662050335); bunlar O-1'deki tanım boşluğuna girer.
Bu seçim sözcüğe dayalıdır. Metni kodu anmayan görsellerde kod olup olmadığı ölçülmedi. Açmadığım ikinci görseller: 1829983002304086142-2, 1840777067882787015-2, 1845558544126366115-2.

### Düzeltme listesi

1. 21 eksik kendi gönderisini (medyasıyla) sınıflamaya ekle ya da K1'e istisna yaz (Y-1).
2. K3 yaz: arka plan kodu, metinde fonksiyon adı, matematik formülü (O-1).
3. K2'yi alan adına göre yaz. Ayrışan ve uyuşan kayıtlara aynı kuralı uygula (O-2).
4. ust-kod.jsonl şemasına `baglanti` alanı ve `istedi` değeri ekle (O-3, D-3).
5. Codex bitince talimatı son ayrışma listesiyle yeniden sına (O-4).

Bu turda dosya oluşturulmadı. Denetim sırasında %TEMP% altında açılan geçici bir liste dosyası (dis.json) silindi.
