# Kod kitabı: Tansu X arşivi sınıflaması (sabit; bütün dilimler bunu kullanır)

**Sürüm 5** (07.10.2026, tam koşu sürümü). Sürüm 5 farkı (dilim 85'te Opus/Codex rol ayrışması): yeni rol
`sinyal-sonucu`; ayırma kuralları 8–9. Tam koşudaki bütün kayıtlar `kk_surum: 5`.

**Sürüm 4** (07.10.2026). Sürüm 4 farkı (dilim 19'da Opus/Codex rol ayrışmasının çoğu): Tansu'nun kendi araç/proje
duyurusu ve başkasının kuralı için ayırma kuralları 4–6 (aşağıda).

**Sürüm 3** (07.10.2026). Her kayıt `kk_surum` alanını taşır. Sürüm değişirse eski sürümle okunan dilimler bu alandan
bulunur. Ölçüm dilimi 1, sürüm 2'ye örnek verdiği için bağımsız ölçüm değildir; sürüm 3 dilim 19'da ölçülür.

Sürüm 3 farkı (denetim-x.md ve dilim 1'de Codex ayrışması):
- Yeni rol `görüş`: yöntemsiz hisse/piyasa yorumu ve tahmini (sohbet değil, kural da değil).
- `kural` tek anlama indi (aşağıda; veri tablosu kural değildir).
- Alıntılanan gönderi, üst gönderi görseli, video için okuma kuralı.
- Hesap doğrulama kuralı (pilotta "eşit ortalama" yanlış okundu: 143,98 = 0,4 × çarpan ort. + 0,6 × İNA).

## Okuma kuralı
- Metin tam okunur. Görsel varsa yerel dosya (`medya/<id>-<n>.<uzantı>`) açılır; açılmadıysa `gorsel_okundu: false`.
  Görseli olmayan gönderide `gorsel_okundu: null`. Video ya da GIF: kare okunabiliyorsa okunur, değilse
  `gorsel_okundu: false` ve notta "video".
- Yanıtsa üst gönderi METNİ birlikte okunur (görseli verilmez; notta "üst görsel görülmedi" gerekmez). Üst gönderi
  alınamadıysa notta "üst gönderi alınamadı".
- Alıntılanan gönderi (`quote_text`) okunur. Tansu'nun kendi cümlesi esastır; alıntıdaki kural Tansu'ya ancak onaylıyorsa
  ("Bu yapıları arayın") yazılır, notta "alıntıdan".
- Tahmin yazılmaz. Okunamayan şey "okunamadı" diye yazılır.
- `alinti` alanı Tansu'nun metninden birebir parçadır (yazım hataları korunur); görseldeki yazı `gorsel_ozet`'e gider.
- Hesap doğrulama: görselde bir sonuç (ortalama, hedef, oran) ve girdileri varsa, sonucu girdilerden yeniden hesapla.
  Tutmuyorsa ya da ağırlıklıysa formülü `parametreler`e yaz ("143,98 = 0,4 × 159,39 + 0,6 × 133,71"). "Eşit ortalama"
  diye yazmadan önce hesapla.

## rol (TEK değer; ikinci varsa `rol2`)
| değer | ne zaman | örnek |
|---|---|---|
| seçim-momentum | hisse seçimi, sıralama, momentum, göreli güç, sektör lideri (ölçütü yazılı) | "Günün Dikkat Çekenleri" skor tablosu |
| evren-likidite | hangi hisseler taranır, hacim/likidite süzgeci | 20 gün TL hacim ≥ 10 milyon |
| bölge | talep/arz bölgesi, destek-direnç, kanal, dip-zirve uzaklığı | "Dibine Yakın Hisseler" |
| formasyon | harmonik, Elliott, klasik formasyon, mum formasyonu | Gartley, fincan-kulp |
| teyit | giriş öncesi doğrulama: kırılım, retest, hacim, gösterge uyumu | "Güzer retest var" |
| giriş | giriş anı ve fiyatı (kural olarak) | "D noktasında limit" |
| çıkış | hedef, stop, kâr alma, iz süren stop (kural olarak) ve yöntemsiz hedef fiyat | "%50'sin satın"; "128-140 bandına oturacak" |
| boyut-risk | pozisyon büyüklüğü, risk yüzdesi, risk/ödül | "%1 risk" |
| rejim | piyasa durumu kuralı: faiz/makro, endeks trendi, volatilite rejimine göre davranış | "MB politikalarını izleyerek pozisyon" |
| değerleme-temel | F/K, PD/DD, İNA, çarpan, bilanço, karlılık; bilanço ölçütüyle seçim (rol2 seçim-momentum) | SAYAS İNA tablosu |
| portföy | portföy kurma, ağırlık, rebalancing, Markowitz | Max Sharpe |
| çift | arbitraj, eşbütünleşme, Z skoru, çift rotasyonu | VAKBN–GARAN |
| ölçüm-yöntemi | backtest, istatistik, ölçüm aracı, gösterge hesabı | Corwin–Schultz |
| ilke | sistemin nasıl kurulacağına dair genel kural | "Duyguya yer yok" |
| araç-öğrenme | Python dersi, kütüphane tanıtımı, kitap, eğitim | cufflinks tanıtımı |
| ürün-hedefi | Tansu'nun yapmak istediği uygulama/ürün | "tek tuş" |
| görüş | yöntemsiz, ölçüsüz hisse/piyasa/makro yorumu ya da yön tahmini | "Gesan çok yakında çok ciddi ivme yapar"; "Türkiye'de ev fiyatları asla düşmemiştir" |
| sinyal-sonucu | Tansu'nun daha önce verdiği sinyalin/listenin sonucunu bildirmesi (tarih, giriş fiyatı, sonraki fiyat ya da getiri) | "#dmrgd 4 Şubatta 12.74'den verildi bugün 18.41 %45 getiri" |
| sohbet-duyuru | piyasa içeriği olmayan: kişisel, selamlaşma, teşekkür, duyuru | "Elinize sağlık üstat" |

Ayırma kuralları:
1. Önce: yöntem ya da ölçü var mı? Yoksa ve piyasa içeriği varsa → `görüş`. Piyasa içeriği de yoksa → `sohbet-duyuru`.
   Yöntemsiz hedef fiyat istisnadır → `çıkış` (+ `hedef` alanı).
2. Yöntem/ölçü varsa → içeriğin rolü (cümlenin başına göre değil, gönderinin konusu).
3. F/K yorumu içeren uyarı ("Gördüğü en yüksek fk dan işlem görmesi büyük yanılgıya sebep olabilir") → `değerleme-temel`.
4. Tansu'nun yazdığı, yazacağı ya da paylaştığı araç/tarama/bot/proje duyurusu ("gridbot yazdım", "Sıradaki projeler",
   "Bunun taramasını hazırlayacağım") → `ürün-hedefi`. Duyuruda ölçüt/kural varsa ("RSİ 50 üzeri ve trend yukarı") o
   ölçütün rolü `rol2`'ye, `kural` ölçüte göre. Ölçüt yoksa `kural: yok`. Sohbet DEĞİLDİR.
5. Python/finans dersi, kütüphane, hangi aracı kullandığı ("Matrix ve Python"), eğitim duyurusu → `araç-öğrenme`.
6. Başka kullanıcının (üst gönderi ya da alıntı) kuralı Tansu'nun kuralı sayılmaz. Tansu yalnız benimsiyorsa ("Python'a
   çevirelim", "Bunu da Python'da yazacağım") → rol 4. kurala göre `ürün-hedefi`, `kural: yok`; kuralı `parametreler`e
   "üst gönderiden (@kullanıcı): ..." diye yaz. Tansu kuralı kendi cümlesiyle onaylar ya da uygularsa → içeriğin rolü,
   notta "üst gönderiden, Tansu onayladı".
7. Program çıktısı (metinde ya da görselde tarama sonucu) kod değildir (`kod: yok`); çıktıdaki ölçüt kuralın kanıtıdır.
8. Bir yöntemi ya da stratejiyi ANLATAN gönderi (model, kural, gösterge, örnek hesap) duyuru değildir → içeriğin rolü
   ("Avellaneda-Stoikov Modeliyle ... short aç, ... kapat" → `giriş`). `ürün-hedefi` yalnız Tansu "yazdım / yazacağım /
   paylaşacağım / test edecek var mı" dediğinde.
9. Geçmiş sinyalin sonucu → `sinyal-sonucu`; `parametreler`e sembol, sinyal tarihi, giriş fiyatı, sonuç fiyatı/getiri;
   `kural: yok` (yöntem söylenmişse `cekirdek` ve yöntemin rolü `rol2`).

## kural (tek anlam: gönderideki İŞLEM ya da HESAP kuralının tamlığı)
- **tam:** kural ve bütün girdileri/eşikleri yazılı (metinde ya da görselde); başkası aynı işlemi ya da hesabı
  tekrar üretir. Hesap tablosu ancak formülü ya da yöntemi görünüyorsa tamdır.
- **cekirdek:** ölçü ya da yön belli, eşik/pencere/ayrıntı eksik.
- **fikir:** kuralın adı var, tanımı yok.
- **yok:** kural yok. Yalnız sonuç sayıları olan veri tablosu (formülsüz karlılık serisi, skor listesi) → `yok`, notta
  "veri tablosu". `görüş` ve `sohbet-duyuru` her zaman `yok`.

## kod
- **yok / metinde / gorselde / baglanti**. Metinde ya da görselde kod varsa `kod_metni` alanına BİREBİR yazılır
  (görseldeki satırlar da, girinti korunur; okunamayan satır `<okunamadı>`). Formül dili de koddur
  (`Cross(Mov(RSI(C,14),5,VAR),50)`). Kod ekran görüntüsü yarım görünüyorsa notta "kod kesik".

## JSONL şeması (her gönderi bir satır)
```json
{"id":"...", "kk_surum":5, "tarih":"YYYY-MM-DD", "tur":"ana|yanit", "rol":"...", "rol2":null,
 "kural":"tam|cekirdek|fikir|yok", "alinti":"birebir kısa alıntı", "gorsel_ozet":"görselde okunan anahtar değerler",
 "gorsel_okundu":true, "kod":"yok|metinde|gorselde|baglanti", "kod_metni":null,
 "semboller":["DOAS"], "parametreler":"eşik, pencere, oran, formül",
 "hedef":[{"sembol":"SAYAS","fiyat":"128-140","vade":"2023 sonu"}],
 "guven":"yuksek|orta|dusuk", "not":null}
```
Defter karşılaştırması bu aşamada YAPILMAZ (ayrı aşama, yalnız kural ≠ yok olanlar).

## Ayrışma çözümü (tam koşu)
1. İki okuyucu (Claude Opus ajanı ve Codex) aynı grubu ayrı okur.
2. `rol`, `kural` ya da `kod` ayrışırsa gönderi hakeme gider: ayrı bir Opus ajanı gönderiyi görseliyle yeniden okur, iki
   kaydı görür, kod kitabına göre karar ve tek cümle gerekçe yazar (`siniflama/hakem/`).
3. Orkestratör hakem kararlarının %10'unu örnekler; bağımsız denetçi ayrıca örnekler.
4. Kod içeren her gönderide `kod_metni` iki okuyucuda karşılaştırılır; farklıysa kod aşamasında satır satır görselle düzeltilir.

## Çözülmüş örnekler (dilim 1)
- 1694839230298468742 → değerleme-temel, cekirdek ("FK 2-3 arası alınıp, 7-5 arası satılabilir").
- 1695361936651653499 → değerleme-temel, tam (yıllıklandırma formülü görselde: 6A + önceki yıl − önceki yıl 6A).
- 1695389783147581542 → değerleme-temel, cekirdek (ağırlıklar görselde yazılı değil, hesaptan çıkarıldı); parametreler
  "143,98 = 0,4 × 159,39 + 0,6 × 133,71".
- 1695424938251796654 → değerleme-temel, yok (karlılık serisi, veri tablosu).
- 1695433615130210730 → rejim, fikir.
- 1696021655947018369 → bölge, cekirdek (dipten uzaklık % beş pencere, eşik yok).
- 1706604421277200700 → görüş, yok ("Gesan çok yakında çok ciddi ivme yapar").
- 1699802936337957180 → çıkış, yok, hedef SAYAS 128-140 ("Sene bitmeden 128-140 bandına oturacak").
- 1695527170251096405 → sohbet-duyuru, yok.
