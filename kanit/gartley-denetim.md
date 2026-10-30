# Gartley kod denetimi (30.10.2026)

İstek (Levent, 30.10.2026): "bu denemeleri yaptığımız phyton dosyalarının mantıklarının doğru olmadığını düşünüyorum".
Onaylanan plan: bağımsız kod denetimi, her hata için ayrı düzeltme, her düzeltmeden sonra ayar grubunda sabit
referans koşusu, eski HAYIR sonuçlarının düzeltme koşusu ve 2010-2014'te bir kez son sınav (veri temizse).

## 2010-2014 veri ölçütleri (veriye bakmadan önce yazıldı)

Bu bölüm 2010-2014 verisine hiç bakılmadan, ilk indirmeden önce yazıldı ve gönderildi. Ölçütler sonradan değişmez.
Veri kontrolü yalnız veri kalitesini ölçer: bu yıllarda strateji, sinyal sayısı ya da getiri hesaplanmaz.

Kaynak: İş Yatırım günlük fiyat (projenin `veri.indir` yolu), ücretsiz. Dönem: 2009-07-01 - 2014-12-31
(2009 ikinci yarısı yalnız ısınma). Evren: 2010-2014 arasında en az bir gün işlem görmüş bütün BIST payları,
o yıllarda borsadan çıkanlar dahil.

Veri "temiz" sayılır, ancak aşağıdaki şartların hepsi tutarsa:

1. **Kapanan hisseler:** 2010-2014 arasında borsadan çıkan payların listesi ücretsiz bir resmî kaynaktan
   (Borsa İstanbul, KAP ya da İş Yatırım kod listesi) kurulabilir ve listedeki kodların en az %90'ının verisi
   iner. Liste kurulamazsa veri temiz değildir (yalnız bugün yaşayan hisseler kalır, sonuç şişer).
2. **Kapsam:** evrendeki kodların en az %95'i için 2010-2014 verisi iner.
3. **Eksik gün:** her payın kendi ilk ve son satırı arasında, XU100 kapanışı olan günlere göre eksik
   hisse-gün payı en çok %1'dir. Payların yarısından fazlasının aynı gün eksik olduğu gün (kaynak günü hatası)
   en çok 5 gündür.
4. **Kurumsal olaylar:** olay denetimi farkı olan gün payı (`Anlik.oranlar`) en çok %2'dir (TASARIM 5.13 eşiği).
5. **Karantina:** düzeltilmiş kurallarla (bu denetimin birleşen bütün veri düzeltmeleri) 2010-2014 karantina
   hisse-gün payı, aynı kurallarla 2015-2022 ayar grubunun payının en çok 1,25 katıdır ya da %1'in altındadır.
6. **Alanlar:** AOF, yüksek, düşük, kapanış, hacim ve XU100 kapanışı, işlem olan günlerin en az %99'unda vardır.
7. **Faiz:** politika faizi serisi 2009-07-01'den başlayarak bütün dönemi kapsar ya da eksik kısım TCMB'nin
   resmî faiz kararlarından eklenebilir.

Bir şart tutmazsa 2010-2014 son sınavı yapılmaz; Levent'in kararı gereği yalnız ileri izleme kalır ve ayrık
grup üçüncü kez kullanılmaz.

## Hata listesi

Denetim katmanlara ayrıldı; her katmanı bu kodu yazmamış yeni bir ajan elle hesaplanmış küçük durumlarla denetledi.
Ayrıca 20 rastgele işlem fiyat verisiyle tek tek doğrulandı (120 kontrolün 118'i geçti; bağımsız yeniden oynatma ayar
grubundaki 572 dolum ve çıkışın hepsini tuttu). Ayrık gruptan ve 2014 öncesinden hiçbir strateji sonucu hesaplanmadı.
Önem: S1 sonucu belirgin değiştirir ya da sahte kazanç üretir; S2 sonucu biraz ya da tek yöne değiştirir; S3 rapor,
etiket ya da etkisiz.

| Kimlik | Katman | Önem | Hata | Durum |
|---|---|---|---|---|
| PR 250 | Veri | S1 | Düzeltilmiş fiyat 0,5 TL altında 4 ondalık yuvarlama yüzünden tutarlı satır bozuk sayılıyor, 250 gün karantina | Birleşti (5736335) |
| V1 | Veri | S1 | İşlemsiz gün (hacim 0, ham AOF, yüksek, düşük 0) bozuk sayılıp 250 gün karantina açıyor; kalan karantinanın %97,7'si | Levent onayı (SPEC 3.9 istisnası), PR |
| V2 | Veri | S2 | 30.04.2018'de 73/411 hissede düzeltilmiş düşük 0; %50 kaynak günü eşiği yakalamıyor | Levent onayı, PR |
| V3 | Veri | S2 | 30.11.2015 öncesi iki seans, seans başına ±%10; kod ±%20 günlük sanıyor: kilit günleri kaçıyor, +%21 günler bozuk sayılıyor | Levent onayı, PR |
| T1 | Veri | S2 | Düzeltilmiş yüksek/düşük, günlerin %3,9'unda ham × gün çarpanından hep daha geniş; etki < 0,02 R | Düzeltilmedi: veri kuralı (SPEC 3.9), açık soru |
| D1 | Desen | S1 | X, A, B, C kendi bacağının ucu değil (sabit pivot penceresi, PDF'te eşit uçlar pivot olmuyor); oranlar yanlış noktadan | Motor: PR 253; betikler: `D1t` |
| D2 | Desen | S2 | PDF betiğinde X kırılmasına yalnız C'den sonra bakılıyor | `D1t` |
| D3 | Desen | S2 | X'e eşit dip C'den önce bozmuyor, C'den sonra bozuyor; kural kartı "X'in altına inmek" der | Motor: PR 253; betikler: `D1t` |
| D4 | Desen | S3 | `sag_bar_pivotlari` fiyatsız günü bar sayıyor | Motor PR |
| D5 | Desen | S3 | S1 "Behle-Conway testi" diye etiketli ama makalenin metnini izler; Tablo 1'i üreten Wealth-Lab kodunda pivot gücü yok, 7 bar zaman çıkışıdır | Kayıt; 7 bar çıkışlı S1: ort. 0,058 R, p 0,33 |
| D6 | Desen | S3 | Hiç eleyemeyen kontroller (`d < B`, `rr_min` 1,4 stop X iken) | Kayıt |
| E2 | Emir | S2 | Açılış stopu AOF < stop olunca AOF'den çıkıyor; AOF günün ortalaması, gerçek stop emrinden hep kötü | `E2` |
| E1 | Emir | S3 | Süresi dolan limit emri yeni sinyali bir gün fazla kapatıyor; 0 işlem değişti | Motor PR |
| E3 | Emir | S3 | `risk_tabanli` etiketi iz stopun son hâliyle ölçülüyor; R değişmez | Motor PR |
| P1-P8 | Para | S3 | `atla` kararı dolum fiyatıyla; SPEC 5.6'nın eşit ağırlıklı al-tut ve %40 sembol işareti yok; 2018 öncesi politika faizi düşük olabilir; düz %15 stopaj; önbellek anahtarı yol; takip betiği eski kararları kilitlemiyor | Kayıt |
| S1 | İstatistik | S1 | Haftalık kümeli p, ortak piyasa hareketini bağımsız sayıyor; 2022 dolumları toplam R'nin %79-98'i (BIST 100 o yıl +%197) | `S1s`: çeyrek küme |
| S2 | İstatistik | S2 | Geçme şartı 1'de en az örnek yok; 2 dolumla p = 0 | `S2s`: en az 30 dolum |
| S3 | İstatistik | S2 | Sahte oran sınamasında 30 dolum eşiği boş hipotezi kaydırıyor; karar değişmez (yüzdelik 83,9-88,2) | Kayıt |
| S4-S7 | İstatistik | S3 | `plan-pdf.md` k = 4 ve k = 5 çelişkisi; DSR yalnız S2-Z için; R tanımında risk tabanı; Sortino NaN | Kayıt |
| T3 | İşlem | S2 | Teyitli girişlerin RSI'ı Wilder; SPEC 3.12 Tansu'nun basit ortalamalı RSI'ını ister | `T3` ve motor PR (`rsi_basit`) |
| T4-T5 | İşlem | S3 | AOF açılışın yerine kullanılıyor; dolumlar fiyat adımında değil; özet ortalama R kaymasız | Kayıt |

Ayrıntı, her hatanın kanıtı ve el hesabı: denetim raporları (yerel, Git dışında; oturum not klasörü
`denetim-veri.md`, `denetim-desen.md`, `denetim-emir.md`, `denetim-para.md`, `denetim-istatistik.md`, `denetim-islem.md`).
Deneme betiklerinin düzeltmeleri (`D1t`, `E2`, `T3`, `S1s`, `S2s`) eski betiklere dokunmadan adlı işlevlerdir:
`kanit/gartley-denetim/duzeltme.py`; her birinin eski davranışı kırmızı, düzeltilmişi yeşil gösteren öz denetimi vardır.

## Referans paneli

Her düzeltmeden sonra aynı panel koşar: ayar grubu (371 hisse), 2015-2022, eski deneme betikleri değişmeden
(`yontem.py` f9d682a1…, `pdf.py` 3e8f2dc6…), dondurulmuş 29.10 ayarı. Adaylar: `gartley` (dondurulmuş), `gt-k`
(Tansu yöntemi Gartley), `abcd-k` (AB=CD), `S2-Z`, `S3`. Veri: eski denemelerin ham görüntüsü (20260101-0000 artı
INTEK, LRSHO, LYDHO), her satırda o satırın motoruyla yeniden kurulur. Defter yazılmaz. Düzenek
`kanit/gartley-denetim/` (`kur.py`, `panel.py`, `duzeltme.py`, `tansu_tam.py`); çıktılar `%TEMP%\tansu-denetim-panel\`
(`panel.tsv`, `sinav.tsv`). Depodaki sürüm, satır 7'yi geçici kopyayla birebir aynı verdi.

Düzenek doğrulaması: denemelerin motoru b9f6107 ile ve `yeniden-kurulus` f4ca87d ile panel, eski kayıtlardaki
ayar grubu sayılarını birebir verdi (ör. `gartley` 39 dolum, ort. 1,129 R, p 0,0478, kasa 538.249; `S3` 295 dolum,
0,411 R, p 0,0038, işlem kârı 393.743). Yeniden kurulan veri, eski veri dosyasıyla 673 hissenin hepsinde aynıdır.

## Düzeltme ve değişim tablosu

Her hücre: dolum / ort. R / p (sinyal düzeyi) ve son kasa TL (para katmanı). Yalnız nakit kasası 234.179 TL.

| Satır | Değişiklik | gartley | gt-k | abcd-k | S2-Z | S3 |
|---|---|---|---|---|---|---|
| 0 | Taban (f4ca87d, eski karantina) | 39 / 1,129 / 0,048; 538.249 | 12 / −0,127 / 0,83; 225.802 | 102 / 0,046 / 0,39; 171.842 | 136 / 0,525 / 0,044; 316.265 | 295 / 0,411 / 0,004; 541.409 |
| 1 | PR 250 karantina yuvarlaması (5736335) | 52 / 0,705 / 0,110; 440.462 | 12 / −0,127 / 0,83; 225.802 | 140 / 0,050 / 0,35; 177.537 | 170 / 0,451 / 0,054; 299.959 | 375 / 0,308 / 0,014; 594.951 |
| 2 | D1+D3 motor: bacak ucu, X'in altına inmek (PR 253) | 49 / 0,960 / 0,072; 464.619 | 13 / −0,027 / 0,61; 230.158 | aynı | aynı | aynı |
| 3 | D1t betikler: PDF ve AB=CD bacak ucu | aynı | aynı | 128 / 0,079 / 0,28; 193.957 | 148 / 0,538 / 0,043; 297.953 | 304 / 0,250 / 0,047; 392.573 |
| 4 | D4 fiyatsız gün bar değil | aynı | 13 / −0,027 / 0,61; 230.158 | 128 / 0,079 / 0,28; 193.883 | aynı | aynı |
| 5 | T3 basit ortalamalı RSI | aynı | 10 / −0,082 / 0,71; 231.138 | 104 / −0,001 / 0,53; 179.299 | aynı | aynı |
| 6 | E2 açılış stopu yalnız yüksek < stop | 49 / 0,978 / 0,067; 477.015 | aynı | 104 / 0,013 / 0,48; 189.114 | 148 / 0,557 / 0,035; 307.153 | 304 / 0,267 / 0,036; 407.762 |
| 7 | S1s çeyrek kümeli p | 0,063 | 0,71 | 0,49 | 0,057 | 0,081 |
| 8 | V1 işlemsiz gün fiyatsız gün | 51 / 0,916 / 0,069; 476.317 | aynı | 111 / 0,000 / 0,53; 186.516 | 157 / 0,808 / 0,018; 328.185 | 324 / 0,348 / 0,037; 481.030 |
| 9 | V2 kaynak günü eşiği %10 | aynı | aynı | 110 / 0,014 / 0,48; 179.114 | 161 / 0,790 / 0,019; 339.506 | 337 / 0,352 / 0,027; 572.238 |

Satırlar birikimlidir: her satır öncekilerin hepsini içerir. "aynı" bir önceki satırla aynı demektir. Satır 7 yalnız p
değerini değiştirir; 7'den sonraki p'ler çeyrek kümelidir. `S2s` (en az 30 dolum) yalnız geçme şartını değiştirir,
panelde sayı değiştirmez.
