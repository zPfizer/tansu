# 25.10.2026 denetim başlangıcı

Bu kayıt, [#187](https://github.com/zPfizer/tansu/issues/187) kapsamında yeni çalışma başlangıcının aday sınırını tanımlar.
İncelenen ana dal `df30e8a87c8e8249d215a483247011b5ae07a49e` revizyonudur.
Envanter tamamlandı. Derin davranış, tarihsel kabul kanıtı ve özgün kaynak görsellerinin yeniden denetimi kısmi kaldı.
Bu kayıt yayımlanmış yeni sürüm, bütün projenin doğruluğu veya günlük kullanım izni anlamına gelmez.

## Envanter ve kanıt kapsamı

Yakalanan GitHub envanteri 91 gerçek issue ve 95 PR içerir. Issue uç noktasındaki PR kayıtları issue sayısına dahil değildir.
Yakalama sırasında 36 issue ve üç PR açıktır. Bu çalışmada daha sonra açılan #187–#192 bu tarihsel sayıların dışındadır.
Uç noktalar ayrı zamanlarda okunmuştur. Envanter tek bir işlemde alınmış eşzamanlı görüntü değildir.

| Kayıt | Sonuç | Kanıt sınırı |
|---|---|---|
| [Issue tablosu](denetimler/20261025-issues.tsv) | 91 özgün satır, 36 açık ve 55 kapalı issue | Her gövde ayrıştırıldı. 16 issue yorumu ve kapatma bağları kontrol edildi. Her tarihsel kabul maddesi bugünkü kodda yeniden kanıtlanmadı. |
| [PR tablosu](denetimler/20261025-prs.tsv) | 95 özgün satır, 85 birleşmiş, yedi birleşmeden kapanmış ve üç açık PR | Her kayıt için durum ve işlem kararı var. Büyük farkların satır satır anlam denetimi ve çalışma zamanı doğrulaması kısmi. |
| Birleşme geçmişi | Birleşmiş 85 PR'ın birleşme commit'i başlangıç revizyonunun atası | Geçmişe girmiş olmak bugünkü davranışın doğru kaldığını kanıtlamaz. |
| Kapalı issue bağları | 44 issue için 45 birleşmiş kapatma PR'ı, kalan 11 issue için kayıtlı karar veya teslim gerekçesi | Hazırlık, iş bölümü ve onayla ertelenmiş kanıtlar tam ürün teslimiyle eş tutulmadı. |

TSV tabloları yakalanan kaydın tarihsel kanıtıdır. Güncel kuyruk yerine geçmez.
Issue tablosu denetçinin çıktısının baytları korunarak alındı.
PR tablosunda iki denetim diliminin sütunları birleştirildi. `source_slice` kaynak dilimi gösterir.
`disposition`, `evidence` ve `remaining_checks` özgün değerlendirmeyi korur.
Yeni sütun biçiminde `in_main` yalnız geçmişe dahil olmayı gösterir.
Boş `closing_issues` veya `diff_lines` hücresi ilgili dilimde ayrı alan tutulmadığını belirtir. Sıfır kabul edilmez.
Geçici yakalama dosyalarının adları kanıt sütunlarında kalır. Ham API dökümleri ve özel kaynak metinleri bu belge paketine alınmadı.

## Doğrulanan on kusur

Aşağıdaki karşı örnekler başlangıç revizyonunda çalıştırıldı. Bunlar tarihsel piyasa etkisinin sıklığını veya büyüklüğünü ölçmez.
Veri kusurları [#188](https://github.com/zPfizer/tansu/issues/188), uygulama kusurları [#189](https://github.com/zPfizer/tansu/issues/189) altında düzeltme bekliyor.
Ek denetim, kayıt günlüğünde [#190](https://github.com/zPfizer/tansu/issues/190), WF bildiriminde [#191](https://github.com/zPfizer/tansu/issues/191) ve sonuç özetinde [#192](https://github.com/zPfizer/tansu/issues/192) işlerini açtı.

| Kimlik | Gözlenen sonuç | Kod sahibi ve sözleşme | Durum |
|---|---|---|---|
| F1 | Bilinmeyen olay kodunun 0,5 çarpanı, 100'den 50'ye düşüşte karantinayı kaldırdı. | `tansu/veri.py`, `_gunler`; TASARIM 5.1 | #188 açık. Kod kümesinin kaynak eşlemesi ve teknik tasarım kararı kaydedildi. Düzeltme kanıtı bekleniyor. |
| F2 | Yalnız hacmi NaN olan satır karantinaya girmedi. Veri kapısı sorun bildirmedi. | `tansu/veri.py`, `_gunler`; TASARIM 5.13 | #188 açık. Gözlenen sıfır hacimle eksik hacim ayrımı korunmalı. |
| F3 | Bütün kaynak için eksik gün işaretlenen fiyat, sonraki günün göstergesine girdi. Tanı amaçlı iki gözlemlik SMA 75 oldu. | `tansu/motor.py`, `_mumlar_kur`; `tansu/veri.py`; TASARIM 5.13 | #188 açık. Bağımsız E1/E2 yolunun tam etkisi ayrıca doğrulanmalı. |
| A1 | Kesilen sektör tamamlama işlemi başarısızlık mesajına rağmen CLI çıkış kodu 0 döndürdü. | `tansu/__main__.py`, `_sektor_indir` | #189 açık. Kapsam mesajı korunarak hata sonucu taşınmalı. |
| A2 | Yeni dar görüntü eski geniş görüntünün önüne geçti. Gerçek sentetik evren A, C, D, E iken günlük seçim yalnız A oldu. | `tansu/gunluk.py`, `_semboller`; TASARIM 6.2 | #189 açık. Sembol kapsamı, ardından tarih sırası uygulanmalı. |
| A3 | Evren dışındaki bozuk B satırları günlük oranı bozdu. Üye kapısı geçerken günlük kapı yüzde 1 karantina sınırını aştı. | `tansu/gunluk.py`, `_kapi_sorunlari`; TASARIM 5.13 ve 6.2 | #189 açık. Pay ve payda aynı tarihli üye hisse-günlerini kullanmalı. |
| J1 | Genel düzeltme API'si geçerli S12 revizyonuna açıklama eklemeyi reddetti. Aynı açıklama eski pilot revizyonunda geçti. | `tansu/deneme.py`, `PilotKayit.duzelt`; TASARIM ortak kayıt sözleşmesi | #190 açık. Tamamlanmış çıktı düzeltmesindeki benzer ret yalnız kod okumasıyla belirlendi. |
| J2 | Kaydetme API'si veri referans listesinin yerine verilen metni yayımlayıp makbuz döndürdü. Kendi okuyucusu bu revizyonu reddetti. | `tansu/deneme.py`, `deneme_kaydet` ve `deneme_oku` | #190 açık. Geçersiz veri ayarı yayın öncesinde reddedilmeli. |
| R1 | WF ilerleme bildirimi hata verince dönen çeyrek durumu hata oldu. Aynı çeyreğin kalıcı makbuzu başarılı kaldı, ikinci yayın girişimini kayıt katmanı reddetti. | `tansu/tansusinama.py`, `kayitli_ileri_calistir`; TASARIM S12 | #191 açık. Bildirim hatası başarılı makbuzu ve çeyrek durumunu değiştirmemeli. |
| S1 | Aynı nihai işlem iki kez verilince toplam bir işlem ve -1 R, eğri -2 R, derinlik 2 R, kohort iki işlem bildirdi. | `tansu/istatistik.py`, `ileri_ozeti` ve `kapali_r_egrisi`; TASARIM S11 ve S12 | #192 açık. Genel API tutarsızlığı kanıtlandı. Doğrulanmış üretim günlüğünden bu girdinin oluştuğu kanıtlanmadı. |

A3 karşı örneğinde 1.000 indirilen satıra karşı 712 üye hisse-günü vardı. Üye oranı 0, bütün satırların oranı 0,02 idi.
Evren dışı satırların oranı aşağı çekmesi de paydanın olası sonucudur. Bu ters etki ayrıca çalıştırılmadı.
F3'te kullanılan iki gözlemlik pencere hatayı görünür kılan tanı girdisidir. Üretim parametresi kararı değildir.
J1 ve J2, genel kayıt API'sinden erişilebilen kusurlardır. Tarihsel kullanım sıklıkları bilinmiyor.
R1 denemesinde gerçek E2, E3 ve E5 çalıştı. E1 ve üyelik girdileri sentetik test düzeninden geldi.
S1 finansal tarihçenin yanlış olduğunu göstermez. Aynı kabul edilmiş girdinin özet alanları arasındaki çelişkiyi gösterir.

F1 için seçilen limit istisnası kümesi `01, 02, 03, 04, 05, 06, 08, 09, 78` oldu.
Tarihsel sağlayıcı araştırması altı türü, saklanan birincil sağlayıcı başlıkları `05`, `06` ve `08` bileşimlerini destekledi.
Bileşimlerin mevcut olay kategorileriyle aynı değerlendirilmesi açık bir teknik çıkarımdır. Yeni bir işlem kuralı değildir.
Bu çıkarım ve A3'ün tarihli üyelik yöntemi seçilen tasarımda çözüldü. Kaynak ve uygulama sözleşmesi düzeltmenin kendi TASARIM değişikliğinde yer alacak.

Küçük düzeltmeler mevcut veri, işlem ve komut sahiplerinde yapılabilir.
Modül büyüklüğü tek başına geniş bir refaktör gerekçesi oluşturmadı.
Eski portföy ve bağımsız işlem yollarının kayıtlı politika farkları birleştirme gerekçesi sayılmadı.

## Belge ve takip bilgisi sapmaları

WF uygulaması [PR #171](https://github.com/zPfizer/tansu/pull/171) ile birleşti.
İki bağımsız ikinci tur incelemesi NOTLU GEÇTİ ve sıfır yanlış iddia kaydetti.
İncelenen commit `f3ca839adf68e04db6309c933361dfa91e0bbf80`, birleşme commit'i `9fe7b10516a981e689b91d63cb3b4cc7e62b8298` idi.
Bu nedenle [TASARIM](TASARIM.md) içindeki iki WF durum yeri düzeltildi.
PR'ın gerçek veri kanıtı bir ret koşusudur. Bir dönem hata verdi, 15 dönem başlamadı.
Tam veriyle başarılı sonuç, MC ve günlük uygunluk kapıları açık kalır. Bu kayıt sonraki her revizyon için yeni inceleme iddiası taşımaz.

Yakalanan takip bilgilerinde aşağıdaki eksikler vardı:

- #55 ve #95 için #76; #96 için #76 ve #95; #97 için #96 önkoşulu metinde vardı, standart `Blocked by:` satırında yoktu.
- #76'nın blocker satırı yalnız kapanmış #56 ve #58'i taşıyordu. Kalan tesliminde #57 ve #94 açık bulunuyordu.
- v0.4.0 sırası kapanmış #69'da kalmıştı. #69 iş haritasıdır. #145–#164 çocuklarının teslimi değildir.
- v0.2.0 sırası güncel #94, #126, #166, #180, #184 ve #185 işlerini; v0.5.0 sırası açık #115'i göstermiyordu.
- #184 ve #185 gövdelerinde ayrı `Levent için` giriş metni eksikti.
- PR #183 gövdesinde güncel CI bekleniyor deniyordu. Yakalamadaki baş commit için CI başarılıydı. Bağımlılık ve inceleme koşulları açık kaldı.

Bu tarihsel liste ilk yakalamadaki durumu gösterir.
Koordinatör daha sonra #55, #76, #95, #96 ve #97'nin standart önkoşul satırlarını düzenledi ve GitHub'dan geri okuyarak doğruladı.
Koordinatör v0.2.0, v0.4.0 ve v0.5.0 milestone açıklamalarını da güncelledi ve geri okuyarak doğruladı.
v0.2.0 başlangıcına #188, #189, #190, #191 ve #192 düzeltmeleri eklendi. #128 ayrı kaynak kapısı kaldı.
v0.4.0 sırası #95, #96 ve #97 oldu. #145–#164 kaynak hazırlığı olarak ayrıldı. Modül yayım sırası Levent'in kararını bekliyor.
v0.5.0 sırası #115 ve #70 oldu. Gerçek kullanım, maliyet ve eksik sahip kararları açık kaldı.
#184 ve #185 için ayrı `Levent için` girişleri eklendi. Yeni #187–#192 gövdeleri aynı zorunlu biçime getirildi.
Bu son durum `queue-blocker-changes.json`, `milestone-changes.json`, `issue-introduction-changes.json` ve `own-issue-format-changes.json` geri okuma kayıtlarına dayanır.
Tarihsel TSV satırları değişmedi. PR #183 gövdesindeki eski CI cümlesi bu güncellemelerle düzeltilmiş sayılmadı.
Ortak arayüzlere atıf yapan bütün işler birbirinin sert önkoşulu sayılmaz. Böyle bir yorum yanlış bağımlılık döngüleri yaratabilir.

## Ayrı iş sahipleri ve açık adaylar

| Aday | Yakalamadaki baş commit | Gözlenen sınır |
|---|---|---|
| [PR #175](https://github.com/zPfizer/tansu/pull/175) | `a6935b46cdf11297a3838754ba9a04d39c56ef4c` | #57, #94, #180 ve #184 ortak teslimi. Taslak, CI başarılı, DOD atlandı, GitHub çakışma bildirdi. Birleşik inceleme KALDI ve gerçek veri işleri açık. |
| [PR #183](https://github.com/zPfizer/tansu/pull/183) | `525874abf58438d52a2a4fb5a2a69c71f6ee3bd3` | #126 adayı. Taslak, CI başarılı, DOD atlandı, GitHub çakışma bildirdi. #94 bağımlılığı ve aday onayı açık. |
| [PR #186](https://github.com/zPfizer/tansu/pull/186) | `5e904f68d145d6fd1583e52741517d4e6554ac3e` | #185 devam sözleşmesi. CI ve DOD başarılı, GitHub çakışma bildirdi. Yönetici belgesinin güncel kaynak araması korunarak bütünleştirme gerekiyor. |

PR #175'in kayıtlı çalışan iş kaynağı `2585c3fad8793cb93374171f68012e552465ec75` idi. Aday baş commit ile aynı değildi.
Bu işler ayrı sahiplerde kalır. Boş GitHub assignee alanı işin sahipsiz olduğunu kanıtlamaz.
Korunan `yerel-koruma-20261020-161758` worktree'sinde değiştirilmiş kart kaydı ve iki izlenmeyen belge bulundu. İçerikleri bu denetimde sahiplenilmedi.
Bir worktree taramasında erişim uyarısı oluştu. Bu yüzden bütün izlenmeyen dizinlerin okunabildiği iddia edilmez.

## Kaynak, ürün ve tarihsel teslim sınırları

- #55 resmi ilk kullanım için seçili revizyonu, kullanım türünü, gösterilen kanıtı ve tarihli sahip kararını bekler.
- #95 için SAHIP-86, SAHIP-111 ve SAHIP-d5 kararları açıktır. Hesap API'si veya önizleme günlük etkinleştirme izni değildir.
- #70 gerçek denetçi kullanımına ve maliyetine bağlı başlama kararını bekler. Küçük pilot bedeli bu kararı karşılamaz.
- #97 kalıcı biçim onayından önce dışa aktarma ve geri kurtarma kanıtını bekler.
- #128 çift büyüklüğü ve R için eksik kaynak nedeniyle `risk_dayanagi_eksik` sınırını korur. #147 özgün R233 kaynağını bekler.
- #152, #153 ve #159'un kapsamı, mevcut harmonik ve Elliott dışlama kararıyla uzlaştırılmalıdır. Bu belge yeni kapsam seçmez.
- Her site çocuğu gösterilen kendi revizyonu için ayrı yayım kararı bekler. Onaylı şablon tamamlanmış panel değildir.
- #166 fiyat yolu hazırlığı kayıtlı MC'den ayrıdır. Eksik açılış fiyatı, takvim, olay ve limit ayrıntıları tam fiyat yolu iddiasını engeller.
- #72'yi kapatan PR #101 açıklayıcı sayfayı teslim etti. Sonraki canlı site bağlantısı ve gösterimi bu yakalamada doğrulanmadı.
- #88'i kapatan PR #125 üç açık kanıt istisnasıyla teslim edildi. #126 günlük komut, #127 ilk etkin aile kanıtını ayrı izler.

Geçmişte kaldırılmış yardımcı komutlar ve arşivlenmiş PR'lar tek başına güncel kusur kanıtı değildir.
Birleşmeden kapanan #1, #43, #44, #45, #46 ve #107 için arşiv ve karar izleri bulundu.
#174 çalışması #175'te toplandı. Eski kesilmiş koşunun sayıları başarılı sonuç sayılmadı.
Eski teslimlere sonradan çıkan süreç kuralları geriye dönük kabul ölçütü yapılmadı.

## Yalnız kod okumasıyla bulunan riskler

`tansu/veri.py` içindeki iki görüntü yayımlayıcısı dakika kimliğinden ortak geçici dizin üretir.
Aynı anda iki yazarın bu dizini paylaşması veri karışması riski taşır. Eşzamanlı çalışma karşı örneği henüz çalıştırılmadı.

`tansu/rapor.py` önce dosya varlığını kontrol eder, sonra üzerine yazabilen yöntemlerle çıktı üretir.
Aynı `kosu_id` için eşzamanlı iki çağrı riski görülür. Desteklenen çağrı yolunda böyle bir paylaşım kanıtlanmadı.
Bu iki gözlem on doğrulanmış kusura eklenmedi.
Ek kayıt denetimi, okuyucunun olağan S03, S07, S10 ve S11 satırları için bütün yayın zamanı kontrollerini yeniden uygulamadığını gördü.
Bu doğrulama farkı üçüncü bir kayıt kusuru diye sayılmadı. Eski kayıt uyumluluğu netleşmeden geniş okuma göçü önerilmedi.

## Yapılan kontroller ve sınırları

Ana revizyonun [CI koşusu 40150220186](https://github.com/zPfizer/tansu/actions/runs/40150220186) başarılıdır.
İki test grubu, toplu CI, biçim, lint ve driftlint geçti.
Push olayında PR'a özel append-only ve fark kontrolü adımları atlandı. Başarı bu atlanan adımları yapılmış saymaz.
Kurulu Python 3.14.7 ile proje ve kilit dosyasındaki 10 çalışma ve iki geliştirme bağımlılığı eşleşti. `pip check` sorun bildirmedi.

Denetim raporları aşağıdaki ilgili test sonuçlarını kaydetti. Bunlar on karşı örneğin düzeltildiğini göstermez.

| Kontrol | Çıkış | Sonuç |
|---|---|---|
| `tests/test_veri.py`, `tests/test_motor.py`, `tests/test_islem_riski.py` | 0 | 303 geçti |
| `tests/test_kapilar.py` | 0 | 24 geçti |
| `tests/test_gunluk.py`, `tests/test_ayar_aktarimi.py` | 0 | 84 geçti |
| `tests/test_sahipler.py`, `tests/test_atif.py`, `tests/test_changelog.py` | 0 | 221 geçti, üç boş parametre kümesi atlandı |
| `tests/test_ci_kayit.py`, `tests/test_dod_kontrol.py`, `tests/test_kanca.py` | 0 | 230 geçti |
| `tests/test_kayit.py -k 'pilot or s10'` | 0 | 86 geçti, 209 seçilmedi |
| `tests/test_ciftbolme.py`, `tests/test_istatistik.py`, `tests/test_saglamlik.py`, `tests/test_denetim.py`, `tests/test_sadakat.py` | 0 | 103 geçti |
| `tests/test_gelecek.py -k 'ortak_cift_kurulumu or veri_motoru_cift_girdileri'` | 0 | Üç geçti, 62 seçilmedi |
| `tests/test_tansusinama.py` seçili S10 dönem, S11 ızgara ve bilinmeyen limit ret kontrolleri | 0 | Üç geçti, 13,71 saniye |

Yerel tam test paketi proje kuralı gereği çalıştırılmadı.
Yeni tam ızgara, gerçek piyasa sonucu, canlı sağlayıcı indirmesi, zamanlayıcı kurulumu, panel yayımı ve kaynak görsellerinin tümünü yeniden okuma yapılmadı.
Ek denetim kayıt, aktarım, çift seçimi, istatistik, sağlamlık, sadakat ve katalog modüllerini okudu.
Kayıtlı dönem, ızgara ve WF koordinasyon bölümleri de incelendi. Bu okuma bütün entegrasyon yollarının çalışma zamanı kanıtı değildir.
İki özgün kaynak notu ve bir görsel ek denetimde açıldı. Katalog parametrelerinin bütün kaynak görselleri yeniden denetlenmedi.
Tam 200 dünya kalibrasyonu, yeni gerçek veri sadakat koşusu ve bütün S11/S12 testleri bu denetimde yapılmadı.
Kayıtlı sınama denetçisinin daraltılmış üç testi `registered-report.md` raporunda başarılıdır.
Önceki geniş seçimin altı ilerleme işaretinden sonra kesilmesi tamamlanmış test sonucu değildir. Bu koşu başarılı sayılmadı.
Üç testin başarısı tam tarihsel gerçek veri akışını veya başarılı WF sonucunu kanıtlamaz.
Tarihsel çalışma çıktılarının bütün özgün özetleri yeniden kontrol edilmedi.

## Aday tamamlama kaydı

Bu belge hazırlanırken #188, #189, #190, #191 ve #192 düzeltmeleri, gerçek görüntü kanıtları ve bağımsız incelemeleri tamamlanmış sayılmadı.
Son aday PR kimlikleri, incelenen commit'ler, ilgili kontrol sonuçları ve kalan koşullar bu bölüme doğrulama sonrası eklenecek.
Şimdiki sınır, envanteri ve kanıt boşlukları belli bir başlangıç adayıdır. Birleşme veya sürüm yayımı değildir.

## Sonraki işler

1. #188–#192'nin on kusuru için ilgili başarısız test, küçük düzeltme, başarılı test ve gereken gerçek görüntü kanıtı.
2. Mevcut sahiplerdeki #175, #183 ve #186'nın güncel ana dalla bütünleşmesi ve kendi kabul koşulları.
3. Güncellenen takip sırasına göre ilerleme. PR #183'ün eski CI cümlesinin kendi sahibi tarafından güncellenmesi.
4. #55 ve #95 için gösterilebilir kanıt ve açık ürün kararları. Ardından #96 ortak panel ve #97 kalıcı uyumluluk kanıtı.
5. Kaynağı ve kapsamı açık site işleri ile #115'in bütün testler hakkındaki karar çalışması. Ürün sırası Levent'in seçimine bağlı kalır.

Teslim ve onay koşullarının sahibi [iş kuralları](agents/is-kurallari.md), ürün durumunun sahibi [TASARIM](TASARIM.md) olarak kalır.
Bu tarihli rapor yeni bir çalışma kuralı veya ürün kararı eklemez.
