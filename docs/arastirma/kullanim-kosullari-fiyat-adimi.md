# Kullanım koşulları ve fiyat adımı (bilet 01, 05.10.2026)

Kaynaklar:
- İki araştırma ajanının birincil kaynak taraması.
- Ana oturumun kendi doğrulamaları: robots.txt indirmesi ve İş Yatırım verisiyle sayım.

Her satırda doğrulama durumu yazılıdır.

## 1. Kullanım koşulları

| Kaynak | Belge | Ne diyor | Durum |
|---|---|---|---|
| İş Yatırım | `https://www.isyatirim.com.tr/robots.txt` | `User-agent: *` altında `Disallow: /_layouts/`. Kullandığımız iki uç nokta bu yolun altında. Crawl-delay yok. | Ana oturum indirdi, doğrulandı |
| İş Yatırım | Kullanım koşulları / yasal uyarı | Otomatik erişimi düzenleyen metin bulunamadı. Tahmin edilen URL'ler 404 verdi. | Bulunamadı |
| borsapy | PyPI sayfası, LICENSE | Kod Apache-2.0. Kaynaklar: TradingView, TCMB, Borsa İstanbul, İş Yatırım, KAP. Uyarı: "This library is for personal and educational use only…" | Ajan okudu (özet araçla) |
| TradingView | `https://www.tradingview.com/policies/` | "…any machine-driven processes that do not involve the direct, human-readable display of such data" yasak. Bu ifade, ekranda göstermeden yerelde saklayıp sınamada kullanmayı da kapsıyor gibi. | Ajan okudu (özet araçla); büyük olasılıkla yasak |
| KAP | robots.txt, yasal uyarı | Okunamadı (404, HTTP 666). | Belirsiz |
| TCMB | Kullanım Şartları | "Sitede yer alan bilgiler, kaynak gösterilmek suretiyle yayımlanabilir… ticari amaçlarla kullanımı TCMB'nin yazılı iznine tabidir". | Ajan okudu; kişisel kullanım serbest |

## 2. Karar (Claude, 05.10.2026)

1. **TradingView kaynaklı veri kullanılmaz.** borsapy'nin TradingView üzerinden gelen fiyat ve endeks verisi
   sistemden çıkar. Bunun sonuçları:
   - **İkinci kaynak karşılaştırması (TASARIM 5.1) kalkar.** Veri doğruluğunu iki denetim taşır:
     - olay tablosu çarpanı ile `HGDG`'nin iç tutarlılığı
     - veri kapıları
   - **XU100 kapanışı ve işlem takvimi İş Yatırım'dan alınır.** `HisseTekil` her satırda `END_DEGER`
     alanını veriyor (endeks kodu 01; 02.10.2026'da 12.270,18). Endeks kodu 01'in XU100 olduğu bilet
     02'de doğrulanır.
2. **borsapy yalnız TCMB politika faizi ve KAP sektörü için kalır.**
   - TCMB kişisel kullanıma izin veriyor.
   - KAP belirsiz. Sektör yılda bir kez okunur.
3. **İş Yatırım kullanımı sürer; robots.txt çelişkisi bilinen risk olarak yazılır.**
   - Ayak izi şöyle tutulur:
     - kişisel ve ticari olmayan kullanım
     - hisse başına günde bir istek, istekler arasında 1 sn
     - açık bir User-Agent (`tansu-kisisel/0.1`)
     - indirme ve sınamada yerel önbellek
   - İş Yatırım engellerse ya da itiraz ederse indirme durur ve TASARIM yeniden açılır.
   - Gerekçe:
     - robots.txt tarayıcı botlara yönelik bir rica; yasaklayan bir kullanım sözleşmesi bulunamadı.
     - Yük, bir kullanıcının tarayıcıdan bakmasına yakın.
     - Bedava alternatifler (Yahoo, TradingView) ya yanlış ya yasak.
   - Bu karar Levent'in tek sözüyle geri alınabilir.

## 3. Fiyat adımı

İkincil kaynaklara göre tablo 06.11.2023'te değişti; KAP duyurusu 03.11.2023. Birincil PDF'lerin metni
çıkarılamadı.

**İş Yatırım verisiyle doğrulama** (ana oturum, `HG_KAPANIS`, `HG_MAX`, `HG_MIN`):
- **2025–10.2026:** KONTR, THYAO, GARAN, ASELS, TUPRS, FROTO, BIMAS ve SASA'nın 10.524 fiyatının hiçbiri
  aşağıdaki tabloya aykırı değil.
- **2016–03.11.2023:** FROTO, TUPRS ve PGSUS'un 250 TL üstü 954 kapanışının hepsi 0,10'un katı. 605'i 0,25'in
  katı değil. Yani 06.11.2023'ten önce 100 TL üstünde adım 0,10'du.

**Tablo** (TASARIM 5.1'e işlendi):

| Fiyat (TL) | 06.11.2023 öncesi | 06.11.2023 ve sonrası |
|---|---|---|
| < 20 | 0,01 | 0,01 |
| 20–50 | 0,02 | 0,02 |
| 50–100 | 0,05 | 0,05 |
| 100–250 | 0,10 | 0,10 |
| 250–500 | 0,10 | 0,25 |
| 500–1.000 | 0,10 | 0,50 |
| 1.000–2.500 | 0,10 | 1,00 |
| ≥ 2.500 | 0,10 | 2,50 |

Doğrulanmayanlar:
- 2.500 TL üstü bant (veride örnek yok).
- 2015–2016'daki 100 TL altı bantlar.
- Eski dönemde 1.000 TL üstü fiyatlar.

## 4. Fiyat limiti

İkincil kaynaklar iki şey söylüyor:
- 13.03.2020'den önce marj pazara göre %20 **ya da %15** imiş.
- Limit fiyatları adıma içe doğru yuvarlanırmış.

Birincil kaynak açılamadı. Ham kapanış serisiyle yapılan sayım bedelsizler yüzünden sonuç vermedi. Bu iş
bilet 03'e kaldı: limit, olay çarpanıyla düzeltilmiş getiriden ölçülecek. TASARIM 8.5 açık kalır.
