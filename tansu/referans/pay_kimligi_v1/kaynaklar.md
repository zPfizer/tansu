# Pay kimliği v1 kaynakları

Davranışın sahibi TASARIM §5.15, “Kaynağa bağlı pay kimliği” bölümüdür.
Bu dosya yalnız sürümlü tablonun kaynak kanıtını ve sınırını tutar.

## B41008 — Borsa İstanbul kod değişimi

- Resmî duyuru: [12.11.2025, sayı 41008](https://www.borsaistanbul.com/files/duyuru-41008-TR.pdf#page=1).
- Yürürlük: 24.11.2025. KOZAA kodu TRMET, KOZAL kodu TRALT olur.
- TRHOL ayrı bir paydır; KOZAA bağı değildir. Duyurudaki IPEKE/TRENJ bu tablonun kapsamına alınmadı.
- KAP 1516560, 13.11.2025, aynı duyuruya dayanarak vadeli sözleşme kod değişimini açıklar. Vadeli sözleşme koşulları spot fiyat çarpanını kanıtlamaz.

## Kayıtlı sağlayıcı zinciri

21.10.2026 tarihli yerel salt okuma incelemesi, `veri/ag/20261005-1949`
görüntüsünü `veri.oku` ile doğruladı. Eşlemelerin görüntü, manifest ve sağlayıcı
bağı CSV'dedir. Fiyat dosyasının SHA-256 özeti
`0cb83ed8dbc89fea90939a2f5675ee08858544e8090f0af7e7ade13ffee9872a`,
olay dosyasının özeti
`09b47cc91085e804988a59d2d3e42d1f8bc840de5efc186b26f048c202d2ade6` olur.

Aynı indirmeye ait `veri/onbellek/20261005` fiyat çerçeveleri, görüntüdeki
TRMET ve TRALT satırlarıyla sütun, tür, sıra ve bütün sayısal değerlerde birebirdir.
TRMET 4.205, TRALT 4.176 satır taşır. Kaynak olay listelerinin yeniden JSON
kodlanmış baytları da önbellekle birebirdir. TRMET'in altı olayı 2003 ve 2012'deki
tarihlerde bile TRMET etiketini; TRALT'ın 13 olayı 2010 ve 2023'teki tarihlerde
TRALT etiketini taşır. Bu, sağlayıcının yeni etiketi eski geçmişte kullandığına
sınırlı kanıttır; yalnız benzer ada dayalı birleştirme değildir.

Görüntünün E1 takviminde 2021–2025 arasında 1.250 gözlem vardır. İki seri bütün
bu günleri kapsar. TRALT 12.02.2010'da başlar; 04.01–11.02.2010 arasındaki 29
E1 gözlemi yoktur. Takvim listesinin ISO tarih ve LF ile SHA-256 özeti
`48e387eb16d3cdae2b65d9052e89651cbb19deb7d6ad1cbd57a614b1276c345e` olur.

İnceleme kaynakları: 21.10.2026 issue #167 hazırlığının
`identity-primary-sources.md`, `candidate-series-coverage.md` ve
`provider-identity-evidence.md` raporları. Bunlar dağıtıcının geçici kanıt
klasöründe tutulur; çalışma zamanı bunlara dayanmaz.

Doğrulanmış ISIN, tarihli pay sınıfı kaydı veya eski indiricinin tam revizyonu
bulunmadı. Bu bağlar bütün sermaye olayı ve düzeltme kökenini çözmez. Fiyat,
hacim veya çarpan değiştirme yetkisi vermez. Başka görüntüye otomatik taşınmaz.
