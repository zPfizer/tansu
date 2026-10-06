# Kod kitabı: Tansu X arşivi sınıflaması (sabit; bütün dilimler bunu kullanır)

Sürüm 2 (07.10.2026). Değişirse sürüm artar ve değişiklikten önceki dilimler işaretlenir.
Sürüm 2 farkı (dilim 1 ölçümünde Opus/Sonnet ayrışmasının 6/9'u bu boşluktandı):
- Yöntemsiz hedef fiyat / fiyat bandı ("Sene bitmeden 128-140 bandına oturacak") → rol `çıkış`, kural `yok`; `hedef`
  alanına yazılır. Yöntem söylenmişse (çarpan, İNA, "finans matematiği") rol `değerleme-temel`, hedef yine yazılır.
- Bilanço/temel ölçütle hisse seçimi ("Net esas faaliyet karı artan ... şirketler") → rol `değerleme-temel`, rol2
  `seçim-momentum`.
- F/K yorumu içeren uyarı ("Gördüğü en yüksek fk dan işlem görmesi büyük yanılgıya sebep olabilir") → `değerleme-temel`;
  ilke değil.
- Görseli olmayan gönderide `gorsel_okundu: null`.

## Okuma kuralı
- Metin tam okunur. Görsel varsa yerel dosya (`medya/<id>-<n>.<uzantı>`) Read ile AÇILIR; açılmadıysa `gorsel_okundu: false`.
- Yanıtsa üst gönderi metni (`ust.jsonl` ya da arşivdeki gönderi) birlikte okunur.
- Tahmin yazılmaz. Okunamayan şey "okunamadı" diye yazılır.
- Alıntı birebirdir (yazım hataları korunur).

## rol (TEK değer)
| değer | ne zaman | örnek |
|---|---|---|
| seçim-momentum | hisse seçimi, sıralama, momentum, göreli güç, sektör lideri | "Günün Dikkat Çekenleri" skor tablosu |
| evren-likidite | hangi hisseler taranır, hacim/likidite süzgeci | 20 gün TL hacim ≥ 10 milyon |
| bölge | talep/arz bölgesi, destek-direnç, kanal, dip-zirve uzaklığı | "Dibine Yakın Hisseler" |
| formasyon | harmonik, Elliott, klasik formasyon, mum formasyonu | Gartley, fincan-kulp |
| teyit | giriş öncesi doğrulama: kırılım, retest, hacim, gösterge uyumu | "Güzer retest var" |
| giriş | giriş anı ve fiyatı | "D noktasında limit" |
| çıkış | hedef, stop, kâr alma, iz süren stop | "%50'sin satın" |
| boyut-risk | pozisyon büyüklüğü, risk yüzdesi, risk/ödül | "%1 risk" |
| rejim | piyasa durumu, faiz/makro rejimi, endeks trendi, volatilite rejimi | "MB politikalarını izleyerek pozisyon" |
| değerleme-temel | F/K, PD/DD, İNA, çarpan, bilanço, karlılık | SAYAS İNA tablosu |
| portföy | portföy kurma, ağırlık, rebalancing, Markowitz | Max Sharpe |
| çift | arbitraj, eşbütünleşme, Z skoru, çift rotasyonu | VAKBN–GARAN |
| ölçüm-yöntemi | backtest, istatistik, ölçüm aracı, gösterge hesabı | Corwin–Schultz |
| ilke | sistemin nasıl kurulacağına dair genel kural | "Duyguya yer yok" |
| araç-öğrenme | Python dersi, kütüphane tanıtımı, kitap, eğitim | cufflinks tanıtımı |
| ürün-hedefi | Tansu'nun yapmak istediği uygulama/ürün | "tek tuş" |
| sohbet-duyuru | kişisel, selamlaşma, duyuru, kural taşımayan cevap | "Elinize sağlık üstat" |

Kararsız kalınca: gönderinin **içeriği** neyse o (cümlenin başı değil). Aynı gönderide iki rol varsa baskın olan yazılır,
ikincisi `rol2` alanına.

## kural
- **tam:** başkası aynı hesabı ya da işlemi tekrar üretebilir (bütün girdiler/eşikler yazılı ya da görselde).
- **çekirdek belli:** ölçü ya da yön belli, eşik/ayrıntı eksik.
- **yalnız fikir:** tanım yok.
- **yok:** strateji içeriği yok.

## kod
- **yok / metinde / görselde / bağlantı**. Metinde ya da görselde kod varsa `kod_metni` alanına BİREBİR yazılır
  (görseldeki satırlar da). Kod formül diliyse (ör. `Cross(Mov(RSI(C,14),5,VAR),50)`) o da koddur.

## JSONL şeması (her gönderi bir satır)
```json
{"id":"...", "tarih":"YYYY-MM-DD", "tur":"ana|yanit", "rol":"...", "rol2":null,
 "kural":"tam|cekirdek|fikir|yok", "alinti":"birebir kısa alıntı", "gorsel_ozet":"görselde okunan anahtar değerler",
 "gorsel_okundu":true, "kod":"yok|metinde|gorselde|baglanti", "kod_metni":null,
 "semboller":["DOAS"], "parametreler":"eşik, pencere, oran listesi",
 "hedef":[{"sembol":"SAYAS","fiyat":"128-140","vade":"2023 sonu"}],
 "guven":"yuksek|orta|dusuk", "not":null}
```
Defter karşılaştırması bu aşamada YAPILMAZ (ayrı aşama, yalnız kural ≠ yok olanlar).

## Pilottan örnekler (çözülmüş)
- 1694839230298468742 → değerleme-temel, çekirdek ("FK 2-3 arası alınıp, 7-5 arası satılabilir").
- 1695361936651653499 → değerleme-temel (cümle "programlar ile yapmak zorunda değilsiniz" diye başlar, içerik hesap
  yöntemi), tam.
- 1695433615130210730 → rejim (faiz ortamına göre pozisyon), fikir.
- 1696021655947018369 → bölge, çekirdek (dipten uzaklık % beş pencere, eşik yok).
- 1695527170251096405 → sohbet-duyuru, yok.
