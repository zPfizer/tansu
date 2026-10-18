# BIST 30 üyelik başvurusu

Üyelik sürümü: `bist30_2021_2025_v1`. Kapsam: 2021-01-01–2025-12-31, iki uç dahil.
`uyelik.csv`, dağıtıcının #86 için verdiği doğrulanmış tablonun değiştirilmemiş kopyasıdır.
53 aralık ve 48 tarihsel sembol içerir. Araştırma tarihi: 18.10.2026.
CSV SHA-256: `6e9ff3cd4a9ce4f2fe9a9ef9f77c36694f563bebe1ca2ba4f924643ce904ad07`.

CSV'de başlangıç dahil, bitiş hariçtir. Boş bitiş yalnız belirtilen kapsamın sonuna kadar geçerlidir.
İlk başlangıç kapsam başına kırpılmıştır; ilk endekse giriş tarihi değildir.
§5.15 üyelik kaydında bitiş dahil olduğu için dolu CSV bitişinden bir gün çıkarılır.
Kaynak kimliği başlangıç olayını gösterir. Çıkış kaynağı aşağıdaki değişim tablosunda bulunur.
A001, 2021'de yayımlanan liste değildir; çıpadan değişimleri tersine uygulayan zincirin kimliğidir.
Bugünkü liste geçmişe doğrudan uygulanmaz. Yedek paylar üyelik sayılmaz.

## Çıpa ve dönem dışı köprü

A001: [Borsa İstanbul bileşen CSV'si](https://www.borsaistanbul.com/datum/hisse_endeks_ds.csv).
Çıpa, kaynak dosyasının XU030 satırlarındaki 19/10/2026 damgasıdır.
Damganın biçimsel yürürlük anlamı ve ortam tarihinden bir gün ileride olmasının nedeni doğrulanmadı.
A002: [KAP BIST 30](https://kap.org.tr/tr/Endeksler?indice=QklTVCAzMA==).
Araştırmada A001 ve A002'nin 30 üyesi eşleşti. Bu karşılaştırma geçmişin bağımsız kanıtı değildir.
2026 değişimleri tersine uygulanarak 2025 sonuna, sonra tarihli duyurularla 2021 başına gidildi.

| Kaynak | Yürürlük | Duyuru tarihi | Eklenen | Çıkan | Resmî bağlantı |
|---|---|---|---|---|---|
| 2021Q1 | 2021-01-01 | 2020-12-21 | none | none | [Notice](https://borsaistanbul.com/duyuru/14132/2021-yili-birinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2021Q2 | 2021-04-01 | 2021-03-15 | SASA | MGROS | [Notice](https://borsaistanbul.com/duyuru/14147/2021-yili-ikinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2021Q3 | 2021-07-01 | 2021-06-18 | FROTO, VESTL | OYAKC, TSKB | [Notice](https://borsaistanbul.com/duyuru/12664/2021-yili-ucuncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2021Q4 | 2021-10-01 | 2021-09-16 | none | none | [Notice](https://borsaistanbul.com/duyuru/14213/2021-yili-dorduncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2022Q1 | 2022-01-01 | 2021-12-17 | TOASO | VAKBN | [Notice](https://borsaistanbul.com/duyuru/12771/2022-yili-birinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2022Q2 | 2022-04-01 | 2022-03-22 | HEKTS | DOHOL | [Notice](https://borsaistanbul.com/duyuru/14347/2022-yili-ikinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2022Q3 | 2022-07-01 | 2022-06-21 | none | none | [Notice](https://borsaistanbul.com/duyuru/14401/2022-yili-ucuncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2022Q4 | 2022-10-01 | 2022-09-21 | AKSEN | HALKB | [Notice](https://borsaistanbul.com/duyuru/12960/2022-yili-dorduncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2023Q1 | 2023-01-01 | 2022-12-19 | ALARK, ODAS | TTKOM, VESTL | [Notice](https://www.borsaistanbul.com/duyuru/14476/2023-yili-birinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylarda-degisiklik-yapilmistir) |
| 2023Q2 | 2023-04-01 | 2023-03-16 | ENKAI | TKFEN | [Notice](https://www.borsaistanbul.com/duyuru/14516/2023-yili-ikinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2023Q3 | 2023-07-01 | 2023-06-16 | ASTOR | AKSEN | [Notice](https://www.borsaistanbul.com/duyuru/14545/2023-yili-ucuncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2023Q4 | 2023-10-01 | 2023-09-21 | KONTR, OYAKC | KOZAA, TAVHL | [Notice](https://www.borsaistanbul.com/duyuru/13125/2023-yili-dorduncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2024Q1 | 2024-01-01 | 2023-12-22 | none | none | [Notice](https://www.borsaistanbul.com/duyuru/14627/2024-yili-birinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2024Q2 | 2024-04-01 | 2024-03-21 | BRSAN | ARCLK | [Notice](https://www.borsaistanbul.com/duyuru/13200/2024-yili-ikinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2024Q3 | 2024-07-01 | 2024-06-13 | DOAS | ODAS | [Notice](https://www.kap.org.tr/tr/Bildirim/1299052) / [table PDF](https://www.kap.org.tr/tr/api/file/download/4028328c8ff3a677019011d27dab21a1) |
| 2024Q4 | 2024-10-01 | 2024-09-20 | MGROS, TTKOM, ULKER | BRSAN, GUBRF, OYAKC | [Notice](https://www.borsaistanbul.com/duyuru/14707/2024-yili-dorduncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2025Q1 | 2025-01-01 | 2024-12-20 | AEFES | DOAS | [Notice](https://www.kap.org.tr/tr/Bildirim/1367507) / [table PDF](https://www.kap.org.tr/tr/api/file/download/4028328d93c3b68d0193e455375a2c0c) |
| 2025Q2 | 2025-04-01 | 2025-03-21 | CIMSA, TAVHL | ALARK, KONTR | [Notice](https://www.borsaistanbul.com/duyuru/14784/2025-yili-ikinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2025Q3 | 2025-07-01 | 2025-06-20 | GUBRF | HEKTS | [Notice](https://www.borsaistanbul.com/duyuru/15121/2025-yili-ucuncu-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2025Q4 | 2025-10-01 | 2025-09-12 | DSTKF | CIMSA | [Notice](https://www.kap.org.tr/tr/Bildirim/1489616) / [table PDF](https://www.kap.org.tr/tr/api/file/download/4028328d992f6f6601993e612fae56b9) |
| 2026Q1 | 2026-01-01 | 2025-12-19 | none | none | [Notice](https://www.borsaistanbul.com/duyuru/15293/2026-yili-birinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2026Q2 | 2026-04-01 | 2026-03-19 | VAKBN | ULKER | [Notice](https://www.borsaistanbul.com/duyuru/15391/2026-yili-ikinci-uc-aylik-donemi-icin-bist-pay-endeksleri-kapsaminda-yer-alacak-paylar-belirlenmistir) |
| 2026Q3 | 2026-07-01 | 2026-06-19 | none | none | [Notice](https://www.kap.org.tr/en/Bildirim/1619135) / [table PDF](https://www.kap.org.tr/tr/api/file/download/4028328c9ec11d3d019ee0d31ce8508a) |
| 2026Q4 | 2026-10-01 | 2026-09-21 | TRMET | DSTKF | [Notice](https://kap.org.tr/en/Bildirim/1666347) / [table PDF](https://kap.org.tr/tr/api/file/download/4028328da0b8438a01a0c54eaeec2faa) |

N001: [Borsa İstanbul 41008](https://borsaistanbul.com/files/duyuru-41008-TR.pdf),
12.11.2025 tarihli duyuru, 24.11.2025 yürürlük: KOZAL kodu TRALT olur.
Bu olay pay değişimi değil, kod değişimidir. Tablo tarihsel kodları korur.

## Bağımsız kontroller ve kanıt sınırı

Dağıtıcının `dogrulama.md` raporu, aşağıdaki 15 resmî tam listeyi CSV ile karşılaştırdı.
Her listede 30 üye, toplam 450 sembol karşılaştırması ve 0 fark bildirildi.
Dağıtıcı, 2021-02-05 için ayrıca 0 farklı bir nokta kontrolü bildirdi (#86 brifi).
Bu işte ağ kullanılmadı; verilen araştırma ve bağımsız kontrol kayıtları aktarıldı.

| Kaynak | Karşılaştırma tarihi | Resmî kaynağın arşivi |
|---|---|---|
| C01 | 2021-01-20 | [C01](https://web.archive.org/web/20210120123331id_/https://www.kap.org.tr/tr/Endeksler) |
| C02 | 2021-02-05 | [C02](https://web.archive.org/web/20210205154303id_/https://www.borsaistanbul.com/datum/hisse_endeks_ds.csv) |
| C03 | 2021-04-10 | [C03](https://web.archive.org/web/20210410183050id_/https://www.kap.org.tr/tr/Endeksler) |
| C04 | 2021-06-16 | [C04](https://web.archive.org/web/20210616161320id_/https://www.kap.org.tr/tr/Endeksler) |
| C05 | 2021-10-02 | [C05](https://web.archive.org/web/20211002161836id_/https://www.kap.org.tr/tr/Endeksler) |
| C06 | 2021-12-01 | [C06](https://web.archive.org/web/20211201055333id_/https://www.kap.org.tr/tr/Endeksler) |
| C07 | 2022-01-22 | [C07](https://web.archive.org/web/20220122175826id_/https://www.kap.org.tr/tr/Endeksler) |
| C08 | 2023-03-26 | [C08](https://web.archive.org/web/20230326081820id_/https://www.kap.org.tr/tr/Endeksler) |
| C09 | 2023-08-18 | [C09](https://web.archive.org/web/20230818140053id_/https://www.kap.org.tr/tr/Endeksler) |
| C10 | 2023-10-05 | [C10](https://web.archive.org/web/20231005183109id_/https://www.kap.org.tr/tr/Endeksler) |
| C11 | 2024-05-19 | [C11](https://web.archive.org/web/20240519042856id_/https://www.kap.org.tr/tr/Endeksler) |
| C12 | 2024-07-16 | [C12](https://web.archive.org/web/20240716155945id_/https://www.kap.org.tr/tr/Endeksler) |
| C13 | 2024-09-25 | [C13](https://web.archive.org/web/20240925180334id_/https://www.kap.org.tr/tr/Endeksler) |
| C14 | 2025-09-03 | [C14](https://web.archive.org/web/20250903134726id_/https://borsaistanbul.com/datum/hisse_endeks_ds.csv) |
| C15 | 2025-12-05 | [C15](https://web.archive.org/web/20251205052013id_/https://www.kap.org.tr/tr/Endeksler) |

KAP sayfaları için karşılaştırma tarihi gerçek arşiv yakalama tarihidir; dönem etiketi doğrulanmadı.
Borsa CSV karşılaştırmaları satırlardaki tarih damgasını kullanır.
U01–U15 duyuruları bağımsız kontrolde okunmuştur; hiçbiri BIST 30 üyeliğini değiştirmez.
15 tarihli eşleşme, aradaki her günün ve bütün dönem içi duyuruların eksiksizliğini bağımsız olarak kanıtlamaz.
24.11.2025 kod değişiminin tam günü N001'e dayanır; Aralık tam listesi yalnız son durumu doğrular.
2024-11-17 isteğinin 2024-09-25'e yönlenmesi yeni bir tarihli kontrol sayılmamıştır.
Bu sınırlar üyeliği bugünkü listeyle veya yaklaşık evrenle doldurma izni vermez.

Araştırma girdileri: `bist30-uyelik/uyelik.csv`, `kaynaklar.md`, `dogrulama.md`
(dağıtıcının `backtest-motoru-1810` çalışma kaydı). Davranış sözleşmesi: `docs/TASARIM.md` §5.15.
