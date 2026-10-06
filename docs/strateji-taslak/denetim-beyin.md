# Beyin düzeltmeleri bağımsız denetimi (2026-10-06)

Kapsam: `git diff dab6dbc -- "kisisel/300-Projects/Tansu X Veri Havuzu"` (107 not, 338 ekleme, 268 silme). Hiçbir not değiştirilmedi.

## Özet sayılar

- Kontrol edilen not: 107 (tümü yalnız "M"; ekleme, silme, ad değişikliği yok).
- Açılan görsel: 66 (ayrıca 2 büyütülmüş kırpma; kırpmalar silindi).
- Doğrulanan düzeltme: ~70 görsel/sayı düzeltmesi görselle ya da ham kayıtla uyuşuyor.
- Hatalı düzeltme: 0 YÜKSEK. 0 yanlış sayı. Birkaç ORTA/DÜŞÜK eksik (aşağıda).
- Ham dokunulmazlığı: 107/107 notta "## Ham" bölümü dab6dbc ile aynı. 107/107 notta tam bir "## Ham" ve bir "## Sentez (yapay zekâ)". Ham metinleri R### kayıtlarıyla (ham-yapistirmalar 1 ve 2) normalize karşılaştırmada 0 fark. Status yalnız güncel/tarihsel/eskidi. Tüm [[...]] bağlantıları çözülüyor (0 kırık).

## Bulgular

### YÜKSEK
Yok.

### ORTA

1. **Paket 80 ve 86'da "Levent" atıf hatası kalmış** (A raporu doğru söylemişti).
   - `gorsel-paket-80-froto-basit-fk-fdfavok-degerleme.md` satır 42 ("Levent, Python ile basit F/K ... tamamlandığını belirtiyor") ve satır 416 ("Levent bu mesajda blended final tercihini açıkça belirtiyor").
   - `gorsel-paket-86-fcff-fcfe-ddm-coklu-degerleme.md` satır 40 ("Levent, yeni değerleme projesinde ... planlıyor").
   - Kanıt: Ham R151 ve R158 birinci tekil takipçi metni ("kodlaması tamamlandı", "yeni bir projeye başladığımı ... anlatayım"). Paket 25 aynı R151/R158'i "Tansu" diye düzeltti; paket 80/86 çelişkili kaldı.
   - Öneri: "Levent" yerine "Tansu (ham R151 / R158, kendi metni)" yaz; iz ekle.
2. **Paket 98 durum kodu eski kalmış.** Satır 628: `SCORE_4_OF_5_UNREPRODUCIBLE`. Aynı notta satır 431/439/442/625 "ilk beş kutudan 4/5 yeniden üretilebilir" diye düzeltildi. Öneri: `SCORE_4_OF_5_REPRODUCIBLE_FIRST_FIVE`.
3. **`not-backtest-giris-sadeligi-risk-islem-gunlugu.md`**: düzeltme yalnız bir uyarı ekledi; "Paylaşılan öneriler" gövdesi ham kayıtta yok (R255 yalnız bağlantı) ve not hâlâ "Levent'in 'Not alın lazım olur' diyerek paylaştığı" diyor (satır 36). Gövde silinmedi, yalnız etiketlendi. Kabul edilebilir ama gövde doğrulanamaz; Karar Levent'te (sil ya da "doğrulanamadı" başlığına taşı).

### DÜŞÜK

4. `tweet-iskpl-abcd-cden-dye-backtest.md`: 3. satır tarihi 2025-02-21 → 2025-03-21 doğru (görsel: `| 3 | 2025-03-21 | hedef | 49.90% | 345,176.62`) ama "Düzeltme" izi yok.
5. `kaynak-vakbn-garan-rotasyon-2096358189696520213.md`: "Z dönüşü +0,30 = ΔZ" doğru (rapor.webp: Son Z -3.108, Önceki Z -3.404; fark 0,296) ama iz yok.
6. `gorsel-paket-102-...` ve `tweet-gartley-d-tepki-penceresi-10-gun.md`: yalnız bağlantı takma adı güncellendi (paket 111 yeni başlık). İz yok; zararsız.
7. Paket 111: başlık/gövde "Takvim Günleri" oldu. Eski başlık başka notta kalmadı (grep 0). Yalnız görsel alt metni ve dosya adı "islem-gunleri" kalıyor; dosya adı değişmez, alt metin (satır 48) isteğe bağlı.
8. Paket 122: satır 685 ve paket 123 satır 776 hâlâ "visible leg-ratio gerilimi" diyor. BC=0,86'ya göre yalnız AB/XA sapıyor. Metin hafifçe abartılı.
9. Paket 43: satır 374 "BUY D near lower channel" kaldı (yakın anlamı korunabilir). Paket 43'ün "üst bant ~24,6" okuması: D hizasında üst bant yaklaşık 25 görünüyor; konum 0,33-0,35, fark önemsiz.
10. "Tansu (ham R068/R070/R082/R083, kendi metni)" kesin söylüyor. Bu kayıtların çoğunda tweet bağlantısı yok; yazar hub kuralından ("Ham = Tansu'nun tweet metni") çıkarılıyor. İçerik takipçilere hitaplı; makul ama kanıtlanmış değil.

## Görsel düzeltmeleri (hepsi görselle doğrulandı)

- Paket 30: sütunlar Artırım | Kesinti | Sabit. 1 Tem 64,18/0,00/35,82; 24 Tem 81,98/0,00/18,02; 31 Tem 67,00/0,00/33,00; Temmuz artırım bandı 48,46 (15 Tem) – 82,24 (23 Tem). Grafik 02 de uyumlu (kesinti kırmızı, artırım mavi). Doğru.
- Paket 37: Toplam Hacim 76,623.82. Doğru.
- Paket 43: D ≈20, alt bant ≈17,5, D'den banda kırmızı ok. Doğru.
- Paket 45: "Kırılım: 2026-05-15". Doğru.
- Paket 62: Ortalama Spread 1.7990%, Ort 1.799%; oran 2,294 doğru.
- Paket 65: CONFLICT 0; EMA20 14.44, EMA50 14.29, EMA100 14.31, EMA200 14.42. Doğru.
- Paket 84: 2021 Büyüme 80, Yatırımlar 6,952. Doğru.
- Paket 85: buy = kırmızı ▲, sell = yeşil ▼. Doğru.
- Paket 96: ilk satır 35150, 50'şer, son 37300, 44 satır. Doğru.
- Paket 122: B->C 0.8x (son hane okunmuyor; 0.86 makul). Oranlar 0,601 ve 1,453 doğru hesaplanmış.
- A1CAP: 15,3 → 9,1 → 12,3, D ≈6. Doğru.
- Paket 07: HKTM +12.62; python: toplam -23,82; ort -1,3233; temiz -11,1106; medyan -12,12; kırpık -10,1019; fark 9,7873. Hepsi doğru. 16/18 negatif doğru.
- Paket 08: OZATD yok, %13,22 yok. Doğru.
- TTRAK: TOASO 2025/9 = 2,30; 8 hisse ort. 2,2688; sektör genel 2,9736; FROTO sütun 2,896; prim %53,6. Python ile doğru.
- Diğerleri doğru: 02 (başlık "#tarama_Carney ... | ... |"), 04 (Mar-May ekseni), 11 (Eyl 2025-Eyl 2026), 16, 18, 22, 36, 39, 41, 51 (Rölatif), 54/60 (kısa MA yeşil), 61, 69, 71 (görselde Dragonfly etiketi yok), 74, 81 (4.3x), 83 (/12, SON FİYAT), 91 (5 adım), 92 (iki üçgen), 93 (EMA 5/13), 95 (29.0396%), 97 (3600-4500), 98 (4,805,210,000; "ilk beş kritik kural"), 99 (Ağu-Ara 2025), 100 (`'PP'`, docstring), 104/98/115 (NotebookLM imzası), 105 (191.32, 183.46), 111 (TAKVİM GÜNLERİNİ SAYIN), 113 (SMA 10), 119, 120 (x1 44,2-44,9; x2 45,5-46,1; CAT 18-29 ve ≈42), 124, 125 (STOP 184.54 / ATR 4.62 bulanık), 128 (mor nokta yok).

## "Levent dedi" → "kaynak metin" toplu değişikliği

Silinen her "Levent ..." satırının Ham'ına bakıldı (≈35 tweet notu + paket 08/25/27/29/41 + kaynak-ekonometri). Ham'lar yalnız takipçilere hitaplı birinci tekil Tansu tweet metni ya da yazarı belirsiz ders metni. "Levent:" ile başlayan ya da Levent'in Claude'a yazdığı hiçbir istek/karar silinmedi. YÜKSEK bulgu yok. Kalan hata yalnız paket 80/86 (ORTA 1). Ek kontroller:
- `tweet-satilik-degil`: Ham R137 "Bu sistem satılık değil arkadaşlar önce onu belirteyim." — yeni alıntı birebir.
- `tweet-sirket-degerlendirme`: Ham R240 "gerçi bistte artık bir önemi yok. sırtlanların kol gezdiği bir cambazhaneden farksız" — doğru.
- `tweet-istatistiksel-arbitraj`: Ham R096 ":)  Bilmeniz önemli." — doğru.
- `tweet-pddd`: Ham R144 yalnız "son 36 çeyrek"; kısa dönem bandı yok — silme yerinde.
- `tweet-teknik-indikator`, `tweet-formasyon-arz-talep`: Ham'a göre yeni metin doğru; aşırı silme yok.
- "(M)/(T)" tırnak alıntıları (R157, R187, R197, R198, R199, R212, R222, R132, R080) ham kayıtlarda var.

## Şüphelilerin hükmü (rapor listesi)

Karar verilebilenler:
- A-04 TSLA skew işareti: büyütmede "Skew=0.163" okunuyor, eksi görünmüyor ama çözünürlük düşük; notta "-0,163" (satır 44, 92, 125, 145). Kesin değil. Öneri: "işareti düşük çözünürlükte belirsiz" yaz; dokunma.
- A-13 TTKOM Supply: büyütmede "65.05 - 66.46" benzeri okunuyor, notta 63,29-65,48; çözünürlükten kesin değil. Doğru kalan değer bilinmiyor; "okunamıyor" notu eklenebilir. Düzeltme yapma.
- D-10, D-40, D-41, E kitap-model, E mum-govde, E topsis (7 vs 9 test), E uygulama-algoritmalari, B-52/54/69 "(M) iki bacaklı politika": Ham'da olmayan ya da Cevo katkısı ifadeler. Silme/etiket kararı Levent'te; mevcut hâl yanlış sayı üretmiyor. Doğru kalsın.
- F-stefan-jansen ("Levent önerdi", R123 yazarı belli değil): kanıtla çözülemez; Levent'e sor.
- F-tansu-2095201144544846208 / 2095218573631279414 (stub "okunmadı" ↔ not-backtest/akfis "okundu"): gerçek tutarsızlık; not-backtest tarafı bu turda uyarıyla işaretlendi (ORTA 3); akfis notu ayrıca etiketlenmeli.
- C-132 (görsel sırası), B-68, B-72, A-10, A-31, F-cwene (eksen tahmini): yaklaşık değer ya da düşük çözünürlük; düzeltilmemesi doğru.
- B-77, F-ai-ml, F-awesome-econ: yorum farkı; doğru kalsın.

## Doğrulananlar

Ham dokunulmazlığı (107/107), R### ile birebir eşleşme (0 fark), bağlantılar (0 kırık), status değerleri, 60+ görsel düzeltmesi, tüm python hesapları (paket 07, TTRAK, 122), iz bırakma (103/107 notta "Düzeltme" izi var; eksikler DÜŞÜK 4-6).

## Hüküm

Beyne commitlenebilir. Yanlış sayı, silinmiş Levent sözü ya da Ham değişikliği yok. Commit öncesi önerilen küçük işler (5 dakika): paket 80 (2 yer) ve 86 (1 yer) "Levent" atfını Tansu'ya çevir; paket 98 satır 628 durum kodunu güncelle. Diğer maddeler sonraya bırakılabilir.
