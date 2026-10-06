# Denetim: tasarim-8.md (sürüm 5)

Not: Bu dosya, sürüm 4 denetiminin yerine yazıldı. Eski denetim artık geçerli değil.

Okuma anı: 06.10.2026. Okunanlar: `tasarim-8.md` (sürüm 5, 244 satır), `izlenebilirlik.md` (a), (b), (c) bölümleri ve BAĞSIZ satırlar, `defter-1..4.md`, `ham-yapistirmalar.md`, `ham-yapistirmalar-2.md`, `docs/TASARIM.md` (§2, §3, §4 Kaynaklar, §5.2, §5.6, §5.8, §5.11, §5.12), `tansu/kaynak.py`, `tansu/kayit.py`, `kayit/deneme.jsonl`, `docs/arastirma/veri-kaynaklari.md`.

## Hüküm: KOŞULLU KABUL

Bugünkü haliyle tasarım GEÇMEZ. Sebep: kapsam kapısı kuralı. Tansu'nun güçlü vurgulu iki fikri gerekçesiz dışarıda (Y3, Y4). Ayrıca H tarayıcısının kuralı kodlanamıyor (Y1, Y2) ve talep bölgesi tanımı eksik (Y5). Bunlar düzelince kabul edilebilir.

Kapsam kapısı sonucu:
- İzlenebilirlik (a) listesindeki 145 BAĞSIZ satırın hepsinin R numarası artık tasarımda geçiyor (denetçi her R için aradı: 0 eksik).
- Madde düzeyinde 16 satırın hâlâ açık cümlesi yok. Hiçbiri güçlü vurgulu değil. Liste sonda.
- Defterleri kendim taradım. Güçlü vurgulu iki yeni boşluk buldum: R137 ADX/CMF ve R224 %10 kâr alma. İkisi de (a) ve (b) listelerinde yok.

## 1. Kapsam kapısı

### 1.1 (a) listesi

Yöntem: (a) bölümündeki 84 R grubunun her biri için `tasarim-8.md` içinde R numarası arandı. Hepsi var. Sonra 145 satırı tek tek okudum ve cümle düzeyinde bağ aradım. Sonuç: 129 satır bağlı, 16 satırda açık cümle yok (sonda listelenmiş). `izlenebilirlik.md` tablosu eski kaldı: hâlâ 145 BAĞSIZ gösteriyor. Tablo yeniden üretilmeden "her fikir bağlı" iddiası doğrulanamaz (DÜŞÜK, D1).

### 1.2 (b) listesi: gerekçeler ikna edici mi?

İkna edici (veri yokluğu açık ve doğru):
- Değerleme hattı (R062, R064, R068, R147–R152, R158, R166), R022 5×5, TOPSIS, DEA: bilanço verisi yok (TASARIM.md §4 Kaynaklar: alanlar yalnız fiyat ve piyasa değeri). Doğru.
- R028, R186, R225, R226 (OBI): opsiyon IV, gün içi, emir defteri yok. Doğru.
- R137 YSA ve R121 Optimal Momentum+: formül gizli. R137: "yapay sinir ağları ile oluşturduğum bir momentum stratejim var". R121: "kodum optimal momentum+ portföyü için simülasyon yapıyor", tanım yok. Doğru.
- R229 konveks rotasyon: 1. adım makro döngü kuralsız, 2. adım F/K ister. Doğru.

İkna edici değil ya da zayıf:
- **R102 "ilki volatilite işi" (ORTA, §8).** Tansu "en en sevdiğim 2 sistemden birisi" diyor (T R102). Tasarım "hangisi belli değil" diyor. Bu doğru, ama bu sistem resmi hatta da ölçümde de karşılığı olmayan tek "en sevilen" sistem. Aday olarak R092 ("sistemim pozisyonu kapatıp defansif pozisyoon aldı"), R030 (volatilite harvesti, "adını verdim") ve R026 var. Tasarım harvesti'ni "S1 portföy katmanı" ölçümüne koyuyor. Bu eşleme zayıf: R030 "ters korelasyona sahip iki varlığı belirli bir oranda sabit tutmak" diyor. S1'in 10 hissesi ters korelasyonlu iki varlık değil. Öneri: Levent'e tek soru: "Volatilite işi, hangisi?" Cevap gelene kadar 8. bölüme "Levent'e soruldu, cevap yok" satırı yaz.
- **R114 fincan-kulp (ORTA, §8).** Gerekçe "kural yeterli, tek örnek; ilk dalga üç tarayıcıyla sınırlı". Tansu: "kendi tarama sistemimin yakaladığı" (vurgu "Yüksek", iki kez yapıştırılmış). "Tek örnek" gerekçesi R012, R199 gibi dahil edilen tarayıcılar için de geçerli. "Üç tarayıcıyla sınırlı" döngüsel. Ölçüm kolu olarak eklemek m'yi artırmaz. Öneri: ölçüm kolu yap.
- **R004 takoz/TOBO/OBO/bayrak/flama (ORTA, §8).** Tansu: "Uygulamanın ilk algoritmaları ... İlk bunlar olacak". Tasarım "kural vermedi" diyor. Ama G-dış R219 OBO için tam kural veriyor (tespit, onay, hedef). Gerekçe "dış kaynak" yetmez: Tansu'nun listesinde "ilk" diyor. Öneri: OBO'yu R219 kuralıyla ölçüm kolu yap, geri kalanını "kural yok" gerekçesiyle ikinci dalgada bırak.
- **R055 confluence (DÜŞÜK, §8).** "Çok güçlü". Gerekçe "bağımsızlık ölçüsü yok; aynı seriden türer". Bu gerekçe tüm çoklu koşulları dışarı atar, HSAR'a özgü değil. HSAR (yatay destek) tarif edilebiliyor. Kabul edilebilir ama gerekçeyi HSAR için yeniden yaz.
- **R210 BIST100 + VIX (DÜŞÜK, §8).** Tansu: "kendi sistemi". Durum "Dışarıda". Değerleme "veri yok" olunca "ikinci dalga" oluyor. VIX ve açılış için de aynı veri işi mantığı geçerli. İki durum tutarsız.
- **R001 medyan (DÜŞÜK, §8).** "Çok güçlü, net söylüyorum üzerinde çalışın". Tasarım "pencere ve kural yok" diyor. TASARIM.md §2 zaten "Medyan" ilkesini taşıyor (likidite medyanı, sağlamlık). Tasarım bunu söylemiyor. Bağ ekle.

### 1.3 Defter taraması: gerekçesiz dışarıda kalan güçlü fikirler

Aradığım sözler: "sistemim", "kodum", "kodumuz", "taramamız", "çok önemli", "şart", "peşinde", "sevdiğim", "kritik", "mutlaka". Sonuç listesindeki R'lerin tasarımda geçip geçmediğine baktım. Geçmeyenler: R106, R132, R152, R201, R225. Bunlardan R152, R201, R225 başka R'lerin altında kavramla bağlı (kabul). R106 medyan (R001 ile aynı). R132 dragonfly doji (açılış yok, DÜŞÜK).

İki gerçek boşluk:

**Y3. R137 "Aşama 3: Teknik Onay": ADX ve CMF (YÜKSEK, §1 madde 1, §3.1, §8).**
- Kanıt (T R137, Tansu'nun kendi sistem tarifi, "Bu sistem satılık değil"): "Trendin gücü, ADX ve Para Akışı (CMF) gibi indikatörlerle ölçülüyor. Buna ek olarak, 'Çekiç' veya 'Sabah Yıldızı' ... mum formasyonları aranarak".
- Tasarımda çekiç/sabah yıldızı §8'de (satır 260) var. CMF hiçbir yerde yok. ADX yalnız "MACD/RSI/ADX panelleri (G R168, M R221)" satırında, "Dışarıda: Tansu'nun ana sistemi değil" gerekçesiyle. Bu gerekçe yanlış: ADX ve CMF Tansu'nun ana sisteminin 3. aşaması. `izlenebilirlik.md` bunu "ADX/CMF atıfsız" diye kendisi işaretlemiş (R137 satırı).
- Aynı gerekçe ("İndikatör cart curt hikaye", T R145) yalnızca R145'i gösteriyor. Tansu'nun kendi araçlarında RSI, MACD, ADX panelleri var (G R168, G R008). Cümle seçmeli kullanılmış.
- Düzeltme: §8'e "ADX ve CMF (T R137 aşama 3)" satırı ekle: "Ölçüm (S1 teknik onay kolu): eşik yok, YORUM". Çok kolay. Ama yapılana dek kapı geçilmez.

**Y4. R224/R233 çıkış zinciri: %10 kâr alma eksik, adım 4 yanlış atıflı (YÜKSEK, §4.4, §1 madde 4).**
- Kanıt (T R224 ham): "Giriş, kar alma %10 (sizin belirleyeceğiniz), ikinci kar alma, trialling stop noktası ve asıl büyük kar satışlarının zamanının gelmesi, önceki günün en düşüğünün altında kapanış ve %50 satış, ve emergency stop 2atr ile kalan tüm maldan çıkış." Defter R224 bunu "ilk kısmi kâr %10 (kullanıcı belirler); önceki gün dibi altı kapanış → %50 sat; emergency stop 2 ATR → kalan çıkış" diye yazmış. Tasarım 4.4 "%10 ilk kâr alma" ve "ikinci kar alma" adımlarını hiç anmıyor. Gerekçe de yok.
- Adım 4: "kalan %50 ikinci böyle günde satılır (M/T R233 'ikinci %50')". R233'te (T son cümle): "ilk %50 kar aldığımız RSI70 reddi ve ikinci %50 kar aldığımız önceki mumun en düşüğünün altında kapanış". Yani R233'te ikinci %50, önceki gün dibi altı kapanışın kendisi. Birinci %50 RSI 70 reddi. "İkinci böyle gün" R233'te yok. Tasarım kendi icadı bir kuralı R233'e dayandırıyor. YORUM etiketi var ("bu boşluk YORUM") ama atıf yanıltıcı.
- Ayrıca R224 ve R233 iki farklı zincir: R224'te %50 satış dibi altı kapanışta; R233'te %50 RSI 70 reddinde, kalan dip altında. Tasarım ikisini birleştiriyor ve bunu söylemiyor.
- Düzeltme: 4.4'e "R224 %10 ilk kâr alma: ölçüm kolu (yüzde sizin belirleyeceğiniz, Tansu vermedi)" ekle. Adım 4'ten "M/T R233" atfını kaldır. "R224 ve R233 farklı zincirler; resmi kol R224/R239" yaz.

Gerekçeli ve kabul edilebilir bulduklarım: R004 (yukarıda ORTA), R016 (H raporunda), R055, R082 (S raporunda), R090, R101 (3.3 ölçüm), R230 (4. madde ölçüm), R229, R118 (4.5).

## 2. Tansu'ya sadakat (atıf kontrolü)

Karşılaştırılan atıf sayısı: 60'tan fazla. Ham metin ve defter "Yazar" satırı birlikte okundu. Doğrulananların bir kısmı (tam alıntı ve sayı uyuşuyor):
R189 ("tüm hisseler önce momentum sistemimden geçiyor"), R137 (5 aşama, "Bu sistem satılık değil"), R120 (500+ hisse, 2015, 12 ay, 10 grup, aylık, eşit ağırlık), R202, R011, R012 (sütunlar), R204 ("Hafta başında verdiğimiz listede idi. %8 getiri"), R198 ("Ben 5-8-13 kullandım"), R127 (Tolerans %1.2, Min 3 gün, 17.12.2025→14.01.2026, 20 gün, %0,64), R080, R085, R081, R055, R102, R228 ("şarttır, şarttır. şarttır."), R034, R092, R026, R019, R014, R043 (`Close < zone_low`), R037, R047, R083, R073, R100, R131, R136, R145, R240, R078 (%26,76 / %27,81), R030, R176, R022, R110 (3–10 hisse, 10–20 aday), R181 (161.700 = C(100,3)), R222 (0,618; 0,382–0,886; 0,786; %3–5; R/R 1,5 ya da 2), R041–R043 sayıları (FROTO, DOAS, TTKOM), R013, R017 (10 kapanmış kalıp), R199/R241/R193 (Fibo %64,3; −%39,3; %54,0), R183, R101 ("Yanıldığını anladığı an zararı keser"). Sayısal hata bulmadım.

Bulunan hatalar:

**O1. R212 SMA250 çıkışı "T" diye yazılmış (ORTA, §4.4 adım 5, §3.2 madde 1).**
- Satır 185: "(5) kapanış SMA250 altı (T R212)". Satır 76: "SMA250 kapısı aynen (T R212)".
- Ham R212 (T): "Diyelim ki ... işleme giriş bileşenlerinizden birisi 250SMA. (bu 200SMA 200EMA 250EMA' da olabilir, stratejinize kalmış.)". Yani giriş için örnek bir bileşen, ve Tansu seçeneği açık bırakıyor. "Aynen" doğru değil.
- Defter R212: "Gün Sonu Stop'u: ... 250 günlük hareketli ortalamanın altında bir kapanış" yalnız G-dış (NotebookLM) görselinden. Çıkış kuralı T değil G-dış.
- Düzeltme: satır 185'i "(G-dış R212)" yap. Satır 76'yı "SMA250 (T R212: örnek bileşen, 200SMA/200EMA/250EMA olabilir; YORUM)" yap.

**O2. R205 "T" diye yazılmış, kural M biçimli (DÜŞÜK, §3.2 E ölçüm kolları).**
- Satır 96: "dalga 4 geri alımı 0,24/0,38/0,50 (T R205)". Defter R205: "T ('Unutmuyoruz') + kural metni M-biçimli". Kuralın kendisi (0,24/0,38/0,50) M. Satır 269 de "R205 kuralı tam" diyor. Etiketi "T/M" yap.

**O3. R039 "T R039 'swing pivot' yöntemini anlatır" (DÜŞÜK, §4.2).**
- Defter R039: yalnız soru ve "Ben hangisini kullanıyorum biliyor musunuz:)" T. İki yöntemin açıklaması ve "asıl kullanmamız gereken yöntemdir" cümlesi yazarı belirsiz. Aynı belgenin satır 159'u "T/M R039" diyor. Satır 157'yi "T/M" yap.

**O4. R138 iki farklı etiket (DÜŞÜK).** Satır 268 "T R138"; satır 231 "M/T R138". Defter: M gövde + T son cümle. "M/T" kullan.

**O5. R090 Trident atfı (DÜŞÜK, §3.2 H ölçüm).** Satır 86-87: "D = (B·C)/A ve B kırılımı teyidi (T R090, alış yönlü paragraf ...)". B kırılımı cümlesi ham metinde SATIŞ yönlü paragrafta ("Satış yönlü ... D oluşumunu teyit etmek için ise B noktası kırılımı gerekir"). Tasarım bunu alış yönüne yansıtıyor. Bu yansıtma YORUM ama işaretsiz. Defter D = (B*C)/A formülünün anlatımını "M/A" diye yazıyor, izlenebilirlik T+G diyor. Defterin kendi içinde tutarsızlık var. Ham metinde formül, "Görseldeki bu kural" cümlesiyle T paragrafında geçiyor. Ben T/G sayıyorum. Ama "dinamik kalibre ediyor" kısmı başka hesabın cevabı; tasarım onu almıyor (doğru).

**O6. R234 "Kritik Kural" genelleniyor (DÜŞÜK, §1 madde 4, §3.2 madde 4).**
- Ham R234: "%55 başarı oranıyla para kazanmak için, her işlemde Risk/Ödül oranını en az 1:1.5 ... ayarlamak gerekir". Bu, ML lojistik modelin %55 isabet oranına bağlı bir şart. Tasarım bunu genel kapı yapıyor. R222 (M) zaten "Ödül/Risk < 1.5 (veya stratejinize göre 2)" diyor, yeterli dayanak. R234 atfı fazla; kaldırılabilir ya da "isabete bağlı" notu eklenmeli.

**O7. R260 hem "kanıt sayılmaz" hem parametre kaynağı (DÜŞÜK, §3.1 ve §8 son satırlar).**
- Satır 64: "63 gün, R260 başlığı, YORUM". Satır 281: "R245–R263 ... Kanıt sayılmaz". YORUM etiketi var, ama kanıt saymadığın kayıttan sayı almak tutarsız. 63'ü "YORUM" yaz, R260'ı çıkar.

**O8. R091 yorumu işaretsiz (ORTA, §4.5).**
- Ham R091 (T, görsel yok): "Trend rejim değişikliği için HMM yapmanıza gerek yok Koç gibi korelasyon varken hiç gerek yok hemde". Hangi korelasyon olduğu belli değil. Tasarım "XU100 ile evren sepetinin rolling korelasyonu" diyor. Bu bizim yorumumuz. Etiket yok.

**O9. R098 ile ΔZ eşitlemesi (ORTA, §3.3).**
- Satır 126: "Mevcut kuralda ΔZ dönüşü ... Tansu'nun 'momentum dönüş teyidi'dir (T R098, G R095)". Ham R098: "Stat-arb sisteminde momentum dönüş teyidi uygulamasının karlarda çarpan etkisine neden olduğunu şimdiden söyleyeyim, deneysel çalışmaları birileriki safhada anlatacağım". Kural yok (defter: "kural yok"). R095 görsel başlığı "Z-Skoru ve Momentum Dönüşü Onaylı İşlemler". ΔZ>0'ın bu teyit olduğu kanıtlanmamış. YORUM yaz.

**O10. Tansu etiketlerinin anlamı ters (ORTA, §4.3).**
- Satır 166-171: durum şeması "(Tansu'nun etiketleri, G R008, R012, R013, R017)": "ADAY → (limit doldu) AKTİF → TAMAMLANDI (hedef)". Görseller: R012 SOKE: Durum AKTIF, Giriş "-", Stop "-" (giriş yok). R012 LUKSK: Durum TAMAMLANDI, Reaksiyon TEPKI_VERDI, Giriş 86,95. R013 KAPLM [TAMAMLANDI]: "D gerçekleşti ama 20 bar içinde TEPKİ GELMEDİ". Yani Tansu'da AKTİF = D henüz gelmedi, TAMAMLANDI = D geldi (giriş seviyesine ulaşıldı), sonra Reaksiyon ölçülüyor. Tasarım AKTİF'i "limit doldu", TAMAMLANDI'yı "hedef" diye kullanıyor. İki etiketin anlamı Tansu'ya göre ters. Emin değilim (görseli doğrudan yeniden açmadım; defter okuması ve R012 iki satırından çıkarım). Ayrıca TASARIM.md §2 de aynı kullanımı taşıyor. Düzeltme: etiketleri Tansu'nun anlamıyla yaz ya da kendi adlarımızı kullan ve "Tansu'nun etiketi değil" notu ekle.

**O11. R120 farkları söylenmiyor (ORTA, §3.1).**
- Ham R120: "500'den fazla hissenin", "Aylık olarak 50+ hisseyi yenilemek gerçek hayatta ciddi bir maliyet". Yani Tansu'nun en üst dilimi 50+ hisse. S1: ilk 100 evren, ilk %10 = 10 hisse. Bu bizim kararımız (likidite). Etiket "YORUM" yok. Ayrıca R120 Tansu'nun "sistemim" cümlesi değil: "basit bir momentum stratejisini test ettim", "Tabii bunun sınırları var". Tansu'nun "momentum sistemim" (R189, R137) YSA'dır ve gizli. Bu fark 3.2 madde 1'de yazılı ama 3.1 ve 3. bölüm girişi ("Tansu'nun kendi sistem dediği hat başına") S1 için fazla iddialı.

## 3. Seçim mantığı

**S1 momentum.** Hattın adı Tansu'nun (R189, R137). Kuralı onun BIST testidir (R120). Bu kabul edilebilir bir vekil. Daha güçlü aday: "momentum → Markowitz → Max Sharpe 3–10 hisse" (R137, R110, R181). Kural parçaları yazılı (aday 10–20 hisse, sonuç 3–10; R181'de n = 100). Tasarım bunu ölçüm kolu yapıyor. Savunulabilir: ağırlık eniyilemesi geçmişe aşırı uyum riski taşır, ve formül gizli. Resmi kol olarak S1'de bırakmak daha temiz.

**S2 kurulum hattı.** "Tarayıcı" varlığı Tansu'nun sözleriyle sabit (R011, R012, R192, R125 "stratejimi anlatamam"). Ama kurallar şöyle: H için R222 (M gövde, Tansu'nun Excel tablosu G), E için R199 (M kart, Tansu'nun araç başlığı G), S için R198 (M metin + T "5-8-13"). Tansu parametreleri paylaşmıyor (R125: "parametrelerin detaylarını verip stratejimi anlatamam"). Yani S2'nin kuralları "Tansu'nun araç çıktısıyla uyumlu M kurallarıdır". Bu açık yazılmalı. TASARIM.md §2 ilkesi (P5) "ekranda 'Tansu'nun sistemi' diye sunulmaz" diyor. Tasarım başlığı "Tansu'nun sistemi" bu ilkeyle çelişiyor (ORTA, O12).

**Tek hipotez kararı.** Savunulabilir, ama iki zayıflık var:
- "Üç tarayıcıyı ayrı kol yapmak m'yi 3 artırır" (satır 115) yanlış sayı: S2 kendi yerini boşaltır, net artış +2 (m = 7, B = 1.400). Maliyet küçük. Gerçek maliyet işlem sayısı: her tarayıcı için ≥100 işlem şartı (5.2).
- Birleşik testte "geçti" hangi tarayıcının işe yaradığını söylemez. Tansu'nun kendi sınamaları tek formasyonlu (R018 ISKPL: yalnız AB=CD, 5 örnek, R017 SMRTG). Tasarım tarayıcı başına ölçümü raporluyor, bu yeterli bir güvence.
- Öte yandan çok katlı kapı (momentum üst yarı + SMA250 + talep bölgesi + formasyon + R/R ≥ 1,5) işlem sayısını çok düşürebilir. 5.2 sayım koşusu bunu yakalıyor. Bu iyi.

**S3 çift.** R102 ("en sevdiğim") ve R228 ("şarttır") için uygun. Üç sorun:
- Resmi S3, Tansu'nun kuralı değil: Tansu'nun çifti AGROT–GARAN, uzun-kısa, tüm bakiye (R099, R101). Resmi kural aynı sektörden yılda bir seçilen çift, yalnız alış. TASARIM.md §5.6 AGROT–GARAN'ı "listede yok" diyor. "Tansu'nun çifti VAKBN–GARAN" ise ayrıca gösterilir.
- **S3 zaten ilk resmi koşuda sınandı ve negatif çıktı (ORTA).** `kayit/deneme.jsonl` (kosu 20261005T205624-cdc34e, kural_id a3ba880f3e82a57d): çift_rotasyonu fazla = −0,0898, güven aralığı [−0,146, −0,028], holm_p = 1,0, genel "Geçmedi". Tasarım 3.3 "Taslak 7'deki kural aynen" diyor ve bunu söylemiyor. Aynı kuralı yeni kural_id ile yeniden girmek bir m harcar, ve sonucu bilinir. Tansu'nun vurguladığı rolling eşbütünleşme (R034), "ip koparsa zarar keser" (R101: "risk yönetimi hayati önem taşır") ölçüm kolunda kalıyor. Sonuç: en çok vurgulanan çift parçaları resmi kolda yok, başarısız kural resmi kolda.
- m = 5 sayımı kodla uyuşuyor (kayit.py: m = mevcut + yeni; deneme.jsonl holm_m = 2).

## 4. Veri gerçeği

Uyuşanlar: açılış yok (TASARIM.md §4 Kaynaklar, §5.3 "kaynakta açılış yok"); kapanış, yüksek, düşük, AOF, hacim, piyasa değeri, sermaye (`kaynak.py` ALANLAR); XU100 kapanışı (END_DEGER); sektör bugünkü sınıflama (§5.2); faiz; gün içi, emir defteri, opsiyon yok (§3 kapsam dışı). Bilanço yok: TASARIM.md'de alan yok; `strateji-modulleri-taslak.md` "CFO verisi bedava zor" diyor.

Sorunlar:
- **O13. "Fiili dolaşım değeri" adı (ORTA, §2 tablo, §3.1).** Kodda alan `HAO_PD` ve `docs/arastirma/veri-kaynaklari.md:86` onu "halka açık piyasa değeri" diye tanımlıyor. TASARIM.md:141 ise "fiili dolaşım değeri" diyor. Tansu "dolaşımdaki pay adedi" diyor ve veriyi KAP'tan alıyor (R083). Halka açık PD ile fiili dolaşım aynı mı: emin değilim. Aynı değilse "<%30" kesimi Tansu'nunkini ölçmez. Doğrulamadan "var" yazılmamalı.
- **D2. Bölüm atfı (DÜŞÜK, §2).** "(TASARIM 5.1)" yazıyor. Alan listesi TASARIM.md §4 "Kaynaklar" altında (satır 135-142). §5.1 indirmeyi 2010'dan başlatıyor; tasarım "TL hacim (2000'den)" diyor. Kaynakta 2000'den veri var ama indirme 2010'dan. İki sayıyı ayrı yaz.
- **D3. "İş Yatırım mali tablo kaynağı" (DÜŞÜK, §8 ilk satır).** Repoda bu kaynağın doğrulaması yok. "Var" demeden önce bilet olarak araştır. Emin değilim.
- **D4. Haftalık mum "günlükten türetilir" doğru.** Ama bakış ileri kuralı yok (Y5).

## 5. İç tutarlılık

- **O14. §2 sonucu ile §4.1 çelişiyor (ORTA).** §2 son satır: "açılış isteyen mum kuralları bu sürümde yalnız AOF'lu yaklaşık hal olarak ölçülür". §4.1: talep bölgesi tabanı "küçük gövdeli mumlar", proximal "tabanın en yüksek gövdesi" ve açılış yerine kapanış–AOF aralığı. Talep bölgesi S2'nin ZORUNLU kapısı, yani resmi kolda. Yaklaşık gövde resmi kolda kullanılıyor, "yalnız ölçülür" doğru değil.
- **D5. Yanlış bölüm atfı (DÜŞÜK).** Satır 54: "Tarayıcıların tek tek sonucu ölçüm koludur (5.3)". Bu belgede 5.3 yok (5.1 ve 5.2 var). TASARIM.md §5.3 başka konu (işlem kuralları). Sürüm 4'ten kalma.
- **D6. "Dört hat" / "beşinci hat" (DÜŞÜK, §1).** Satır 15 "dört hat" diyor, satır 39 "Beşinci hat". İki cümleyi birleştir. Satır 17-18 "Beş aşama" deyip dört madde sıralıyor.
- **D7. Aynı fikir iki durumda.** (a) Satır 253 ve 195: bant kuyruğu ve volatilite rejimi ölçüm. (b) Satır 273 R092'yi hem "volatilite işi aday" hem 4.5 ölçüm sayıyor, 8. bölümdeki "Rejim" bu yüzden iki yerde. Zararsız. (c) R153/R154/R061: `izlenebilirlik.md` (b) "kapsam dışı" diyor, tasarım 8 "ikinci dalga" diyor. Tablo eski, güncelle.
- **O12 (devam). TASARIM.md ile çelişkiler listelenmemiş (ORTA).** Tasarım "Levent onaylamadan TASARIM.md'ye girmez" diyor ama hangi TASARIM maddelerini değiştirdiğini listelemiyor. Değişenler: §3 "Kapsam dışı: Harmonik, Elliott" ve "İkinci dalga: AB=CD"; §3 "Yok: iz süren stop ve kısmi kâr" ve "Corwin–Schultz"; §5.5 "Hedef yok"; §2 P5. Belgenin başına "Değiştirdiği TASARIM maddeleri" listesi ekle.

## 6. Uygulanabilirlik

**Y1. Gartley'de R/R ≥ 1,5 kapısı kendini eliyor (YÜKSEK, §3.2 H ve madde 4).**
- Kural (G/M R222): D = XA'nın 0,786'sı. Risk = giriş − geçersizlik = D − X. Ödül = TP1 = D + 0,382·(A−D).
- Hesap: r = D'nin XA'ya göre geri çekilme oranı. Risk = (1−r)·XA. Ödül = 0,382·r·XA. Oran = 0,382·r/(1−r). r = 0,786 için oran 1,40 (<1,5). Oranın 1,5'e ulaşması için r ≥ ~0,797. %3–5 tolerans içinde D 0,786'nın biraz ötesine düşerse geçiyor, ama tam 0,786'da hiç geçmez. R222 tablosunda SL = X − 2·ATR olduğu için risk daha da büyük ve oran daha da düşük.
- Etki: Gartley işlemlerinin büyük kısmı kapıdan dönecek. Ya sayım koşusu H için çok az sinyal verir ya da kapı yalnız D'si çok derine inen (zayıf) kalıpları seçer. Tasarım bunu hiç hesaplamamış.
- Ek: izlenebilirlik R222 satırı "SL = X_Fiyat − (ATR*2)" için "3.2 H; resmi" diyor. Tasarım X'i kullanıyor, ATR payı yok. Bağ yanlış.
- Düzeltme: önce R/R'yi Tansu'nun tablosundaki stop ve TP1 ile elle hesapla. İki seçenek: (a) kapı eşiğini TP2'ye göre yaz, (b) R222'nin kendi stop'unu (X − 2 ATR) ve TP1'ini kullan ve kapıyı kaldır. Hangisini seçtiğini YORUM olarak yaz.

**Y2. AB=CD için giriş sonrası stop ve hedef tanımsız; oran çelişkisi (YÜKSEK, §3.2 H).**
- AB=CD'de X yok. Tasarımda tek "geçersizlik" tanımı: "C'den sonra A'nın geçilmesi (T R019)". Bu D'ye varılmadan önceki bozulma, girişten sonraki stop değil. Giriş D'de limit. D'de dolduktan sonra stop nerede? Tanımsız. R/R kapısı (risk = giriş − geçersizlik) hesaplanamaz.
- D'nin kendisi belirsiz: CD/AB = 1,0 / 1,27 / 1,618 (M R080). Hangisi limit seviyesi? Kod "ya da" ile yazılamaz.
- BC/AB aralığı çelişkili: T R019 "BC, AB'yi aşamaz, BC tam 1.00 olabilir". M R080 "0.382, 0.50, 0.618 vb.". Tasarım iki cümleyi birlikte yazıyor ("BC ≤ AB, BC = 1,00 olabilir" ve "BC/AB 0,382–0,618"). Hangisi geçerli? 1,00 hem izinli hem aralık dışında.
- AB=CD, Tansu'nun en çok vurguladığı formasyon (R019, R080, R081, R085). Kuralın tam yazılması gerekir.
- Düzeltme: AB=CD için (1) hangi CD/AB oranı resmi (ya da hepsi ayrı kurulum), (2) BC/AB aralığı, (3) giriş sonrası stop (örn. D − 2 ATR) ve ilk hedef; hepsi YORUM etiketiyle. Aksi halde H resmi kolu AB=CD olmadan yalnız Gartley+Kelebek olur ve Y1'e girer.

**Y5. Talep bölgesi tanımı kodlanamaz; haftalık bölgede bakış ileri kuralı yok (YÜKSEK, §4.1, §3.2 madde 5).**
- 4.1: "sert yükseliş (leg-out) öncesi küçük gövdeli mumlar". "Sert" ve "küçük" eşiği yok. Kaç mum taban sayılır? Leg-out en az kaç ATR? Pivot için "k ön kayıtlı aday kümesi, YORUM" yazılmış. Bölge eşikleri için böyle bir not yok. Talep bölgesi S2'nin zorunlu ön şartı ve K1'in ön şartı, yani en kritik parametre.
- Satır 147: "Haftalık bölge ayrıca üretilir (T R081)". Madde 5 (bakış ileri yok) yalnız günlük pivot, FVG ve günlük bölge için yazılı. Hafta kapanmadan o haftanın bölgesi ve pivotu bilinmez. Eski denetim bunu zaten söylemişti, hâlâ eksik.
- R047: "DISTAL line always be at the low of base candle OR leg out candle". Tasarım yalnız "tabanın en düşüğü" yazıyor, "ya da leg-out mumu" kaybolmuş (DÜŞÜK).
- Düzeltme: taban mum sayısı, "küçük gövde" (örn. gövde ≤ x·ATR) ve leg-out (örn. ≥ y·ATR) için ön kayıtlı aday kümesi yaz, YORUM de. Haftalık yapılarda yalnız tamamlanmış hafta kullanılır diye yaz ve `test_gelecek.py` kapsamına al.

Diğer uygulanabilirlik bulguları:

**O15. YORUM işaretsiz kararlar (ORTA).**
- §4.4 "10 işlem gününde dolmazsa iptal": kaynak yok, YORUM değil. R014'ün 10 günü başka bir şey (D'den sonra tepki penceresi).
- §3.2 S: "EMA 5/8/13 arası oran ≤ tolerans". "Oran" tanımı yok (en yüksek/en düşük − 1 mi, bir EMA'ya göre mi?). Tolerans %1,2 R127'de EMA 20/50/100/200 içindi; 5/8/13 serisi doğal olarak birbirine daha yakın, %1,2 aynı sıkılığı vermez. Etiket yok (kaynak notu var ama YORUM değil).
- §3.2 E: "Giriş FVG üst bandına ya da 0,618'e limit": "ya da" kodlanamaz. Hangisi?
- §3.2 madde 4 ölçüm: "aktif volatilite ≥ %40": R223 kodundaki 0,40 bir "çok hareketli" etiketi, kapı değil. R230 ise "aktif volatilite aranmalı" der, eşik vermez. İkisini birleştirmek YORUM.
- §4.5 mevsimsellik "son 10 yılda ≥ %70": hesap pencerisinin ileriye bakmaması (her yıl yalnız geçmiş 10 yıl) yazılmamış. Tüm örneklemden hesaplanırsa bakış ileri olur.
- §4.4 boyut: Tansu'nun formülü adet = risk / (2 ATR) (R184, R212). Tasarım adet = risk / (giriş − geçersizlik), geçersizlik 2 ATR'den uzaksa 2 ATR. Geçersizlik yakınsa pozisyon Tansu'nunkinden büyük. Bu fark YORUM olarak yazılmamış.
- §3.1 S1: "ay başında yeniden kurulur": mevcut ve yeni listede ortak hisseler satılıp yeniden alınır mı, yoksa tutulur mu? Masrafı değiştirir. Yazılı değil.
- §3.1 S1: 252 günlük geçmişi olmayan hisse ne olur? Yazılı değil.

**O16. C'den alım kolu bakış ileri (ORTA, §3.2 H ölçüm).** "C'den alım, D'de satış (T R018 ... sürüm 4'ün resmi kolu)". C bir salınım dibi; sağındaki k mum kapanmadan bilinmez. Giriş C tarihinde yapılırsa bakış ileri. Tasarımda bu kolun giriş günü yazılı değil. "C'nin doğrulandığı ilk gün + ertesi AOF" olarak yaz. Kolun neden resmi olmadığı da yazılsın (Tansu'nun kendi ISKPL ve SMRTG sınamaları C'den giriyor: R017, R018 görselleri). Tasarım bunu söylemiyor.

**Bakış ileri riski özeti:** S1 yok (ay başı kapanış sıralaması, ertesi AOF; evren önceki ay sonu piyasa değeriyle). S2 günlük pivot/FVG/bölge için kural var. Açık kalanlar: haftalık yapılar (Y5), C kolu (O16), mevsimsellik (O15), KDE seviyeleri (ölçüm, tüm örneklem riski; kural yok). S3 mevcut kod, bakış ileri testi var (TASARIM `test_gelecek.py`).

## 7. Sonuç ve sayılar

Düşük bulgular (kısaca): D1 izlenebilirlik tablosu eski (145 hâlâ yazıyor); D2 bölüm atfı; D3 mali tablo kaynağı doğrulanmamış; D5 "5.3"; D6 "dört/beşinci"; D7 tablo-tasarım durum farkı; "m'yi 3 artırır" (+2); R260; R138 etiketi; R205 etiketi.

### Hâlâ bağsız fikir sayısı: 16 satır (madde düzeyi), 0 R grubu

Tüm R numaraları tasarımda geçiyor. Madde düzeyinde, tasarımda açık cümlesi olmayanlar:
1. R008: yatay sıkışma, üçgen/flama daralması ("Kırılım" etiketi) (flama yalnız R004/R006/R007 satırında, üçgen ve yatay sıkışma yok)
2. R039: 2. yöntem "Regresyon ve Zarf"
3. R053: bant genişliği ile risk
4. R053: VaR
5. R076: yön çatışması ("yolculamayalım mı")
6. R090: "dinamik kalibre ediyor" (başka hesabın cevabı; Tansu'nun değil, alınmamasında sakınca yok)
7. R099: Mark-to-Market
8. R118: düşük hacim uyarısı
9. R118: "Liderleri Takip Edin" (spread düşük ve stabil)
10. R118: mikro-makro çelişkisi
11. R128: EMA'ların dinamik desteğe dönmesi
12. R129: FVG'de likidite süpürme
13. R129: önce üst dirençleri test
14. R133: "HBK evrensel bir cevap sunar"
15. R183: sektörel döngüler (elektrik yaz/kış)
16. R192: EMA kümesi üstü kalıcılık (boğa trendi için)

Hepsi M ya da T/M, hiçbiri güçlü vurgulu değil. Bu sayıma duyarlılık var: bazılarını "kavram bağı" saymak mümkün (emin değilim). Ek olarak "zayıf bağlı" (R-düzeyi kavram, cümle yok ya da kısmi) satırlar: R077 yeşil üçgenler, R129 BOS+EMA, R195 runaway gap ve gap fill, R220 panik satışı, R243 büyük mumlar, R203 TP2 hacimli geçiş, R090 FIBO iz süren TP.

Güçlü vurgulu ve gerekçesiz (izlenebilirlik'te yok, benim bulduğum): 2 (Y3 R137 ADX/CMF; Y4 R224 %10 ve ikinci kâr alma).

### Düzeltme listesi (hüküm "koşullu kabul" için)

1. Y3: R137 ADX/CMF için §8'e satır ekle. (kapı)
2. Y4: R224 %10 kâr alma için satır; adım 4 atfını düzelt; R224/R233 farkını yaz. (kapı)
3. Y1: Gartley R/R hesabını elle yap; kapıyı ya da TP/stop'u düzelt.
4. Y2: AB=CD için stop, CD/AB oranı, BC/AB aralığı yaz.
5. Y5: Bölge eşiklerini ve haftalık bakış ileri kuralını yaz.

Sonra (ORTA): O1–O16, özellikle O10 (durum etiketleri), S3'ün bilinen negatif sonucu, O13 (fiili dolaşım).

Doğrulamadıklarım: görselleri yeniden açmadım; görsel bilgileri defterden aldım (O10 buna bağlı). İş Yatırım mali tablo kaynağını araştırmadım. `izlenebilirlik.md`'nin bağsız olmayan satırlarının tümünü tek tek doğrulamadım; yalnız örnekledim (BAĞSIZ satırlar tam, diğerleri örnek).

---

# Tur 2: sürüm 5.1 denetimi

Okuma anı: 06.10.2026. Okunan: `tasarim-8.md` sürüm 5.1 (tamamı). Ham metinle karşılaştırılan yeni atıflar: R096, R079, R084, R232, R035, R114/GUBRF sayıları, R224, R233, R222, R203, R127; `kayit/deneme.jsonl` S3 sayıları. Not: Tur 1 metni yazılırken sürüm 4 denetiminin üzerine yazıldı; o metin git `ed09d17`'de duruyor.

## Hüküm: KABUL (kapı geçti; küçük düzeltmeler önerilir)

Kapı geçti. Tur 1'de bulduğum iki gerekçesiz güçlü fikir yerinde: R137 ADX/CMF (3.1 ölçüm kolu) ve R224 ilk kısım %10 + ikinci kâr alma (4.4 ölçüm kolları). 16 madde düzeyi bağsız satırın hepsi §8'in tek satırında. Satırın "yalnız M ya da yorum cümlesi" gerekçesi kısmen yanlış: T R053, T R076, T R133 T etiketli. Hiçbiri güçlü vurgulu değil. Defteri yeniden taradım: gerekçesiz dışarıda güçlü vurgulu fikir görmedim.

## Tur 1 bulgularının durumu

- Y1 kapandı. TP2 ile oran 0,618·0,786/0,214 = 2,27 (kapıyı geçer). Harfiyen TP1 hesabı (1,40) tasarımda yazılı, ölçüm kolu.
- Y2 kapandı. BC/AB [0,382; 1,00] (T R019 esas). D = C − 1,0·(A−B) (G R079, R084 "CD=1.0AB"). Giriş sonrası stop CD 1,272 altı kapanış: risk 0,272·AB, TP2 ödülü 0,618·AB, oran 2,27. Tutarlı.
- Y3 kapandı (3.1, §1, §8). Y4 kapandı (4.4 R224 ham metniyle uyuşuyor). Y5 kapandı (4.1 eşik adayları, 3.2 madde 5 haftalık ve FVG kuralı).
- O1–O4 etiketler, O10 (AKTİF/TAMAMLANDI; 4.3 artık R012 ve R013 ile uyuşuyor), O12, O13, O14, O15 kapandı. R102, R114, R004 gerekçeleri yeterli.
- Doğrulanan sayılar: S3 önceki koşu (fazla −%9,0; güven aralığı [−%14,6; −%2,8]; 91 işlem; Holm p 1,0; 18 hücrenin 18'i negatif) `deneme.jsonl` ile birebir. GUBRF: 389,30 − 104,80 = 284,50; kırılma 300,75 (defter R114). R035: KENT %0,54, GARAN %13,98. R232: "20 günlük ortalama hacmi 10 Milyon TL" M metninde var.

## Yeni bulgular

**ORTA N1. S3 yeni kuralı eksik tanımlı (§3.3).** "Evrendeki tüm çiftler" (R096: "150.000 kombinasyon"). Yazılı olmayanlar: (a) hangi ve kaç çift işlem görür, sıralama; (b) rolling p kapısı 150.000 çiftte yaklaşık %5 yanlış pozitif üretir, çoklu test kontrolü yok; (c) seçim sıklığı. TASARIM 5.6'nın "en çok 5 çift, p'ye göre açgözlü, yıllık" mantığı kalktı, yerine bir şey konmadı. Kodlanamaz. Ayrıca R096 "sektör şartı yok" demez; yalnız kombinasyon sayısını söyler. Bu çıkarım YORUM yazılmalı. Resmi sınavdan önce kapanmalı; kabulü engellemez.

**ORTA N2. §9 madde 2 eski kaldı.** "Kalan %50 çıkışı yorumdur (4.4 adım 4)" diyor. Adım 4 artık harfiyen R224 (+ G-dış SMA250). Maddeyi "SMA250 eki ile yalnız 2 ATR okuması arasında seçim; sade hal ölçüm kolu" diye değiştir.

**DÜŞÜK N3.** 4.4 adım 1 "geçersizlik gün içi" diyor, AB=CD geçersizliği "kapanış altı". AB=CD için kapanış bazlı olduğunu 4.4'e yaz.

**DÜŞÜK N4. Tur 1'den açık kalan küçük hatalar.** (a) Satır 74 "(5.3)": belgede 5.3 yok. (b) Satır 50 "(TASARIM 5.1)": alan listesi TASARIM §4 Kaynaklar'da. (c) Satır 157 "m'yi 3 artırır": doğrusu +2. (d) Satır 18 "dört hat", satır 44 "Beşinci hat". (e) Satır 90 R260 hâlâ parametre kaynağı, oysa §8 "kanıt sayılmaz" diyor. (f) §8 satır 346'nın "yalnız M" gerekçesi (yukarıda).

**DÜŞÜK N5.** `izlenebilirlik.md` hâlâ eski (145 BAĞSIZ). "Her fikir bağlı" iddiası tablo yeniden üretilmeden kanıtlanmaz.

Yeni yanlış atıf: bulmadım. Yeni çelişki: N2 ve N3 dışında bulmadım.

## Kısa sonuç

KABUL. Önce N2, N4 düzeltilsin ve izlenebilirlik yeniden üretilsin. S3 çift seçim kuralı (N1) resmi sınavdan önce yazılmalı.
