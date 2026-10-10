# 07: Evren

**What to build:** `evren(tarih)` o gün yeni giriş için taranabilecek hisseleri döndürür. Kural şudur:
1. Ayın ilk işlem gününde, önceki ayın son kapanışındaki piyasa değerine göre sıralama yapılır.
2. 60 günlük medyan TL hacimde en alttaki %20 elenir.
3. Kalanlardan en büyük 100 hisse alınır.
4. Aynı şirketin birden çok kodu varsa yalnız biri kalır.

Bunun için bütün sembollerin verisi indirilir; işlemi kapanmış semboller de buna dahildir.

**Blocked by:** 03, 04

**Status:** done

- [x] Sembol listesi şunlardan oluşur: bugünkü bütün paylar (borsapy) ve KAP'tan bulunabilen işlemi kapanmış
      kodlar. Bulunamayanlar listelenir. (Kapanan kodlar KAP'tan değil Borsa İstanbul'dan; bkz. Comments.)
- [x] Anlık görüntü bütün evren adaylarını içerir. İlk indirmenin süresi ölçülür ve yazılır.
- [x] Şirket başına tek kod kuralı uygulanır. Bilinen çoklu kodlar elle yazılmış bir listede tutulur.
- [x] Kapanma kuralları:
  - 60 işlem gününden uzun durdurma kapanma sayılır.
  - Kapanan hissedeki pozisyon −%100 sayılır; neden biliniyorsa son fiyat kullanılır. (Neden listesi boş;
    bkz. açık işler.)
- [x] Testler `kosu`'ya giden sentetik anlık görüntüyle: (`evren(anlik, tarih)` yüzünde; `kosu` evreni henüz
      çağırmıyor)
  - ay başı sıralama
  - geleceği görmeme (önceki ay sonu verisi)
  - likidite eleği
  - tek kod
  - kapanma

## Comments

**Arayüz.** `evren.evren(anlik, tarih, en_buyuk=100, elenen=0.20, coklu=COKLU_KOD) -> list` (büyükten küçüğe);
`evren.kapananlar(anlik, nedeni_bilinen=()) -> sembol, son_islem, kapanma_gunu, getiri`;
`evren.tum_semboller`; `kaynak.kapanan_kodlar()`, `kaynak.Onbellekli`; komut `python -m tansu evren-indir`.
`evren.py` `kayit.KOD_DOSYALARI`'na girdi (kural kodu).

**Sıra (ticket'tan sapma).** Tek kod elemesi likidite eleğinden ve büyük-100 seçiminden önce yapılır (sonda
yapılsa liste 100'den az kalırdı): işlem gören → tek kod (medyan hacmi yüksek kalır) → medyan hacimde alttaki
%20 (`int(n × 0,2)` adet) → piyasa değerine göre ilk 100. 60 günlük pencerede olmayan gün hacmi 0 sayılır.
Piyasa değeri sütunu `pd` (ham kapanış × o kodun sermayesi).

**Gerçek anlık görüntü** `veri/ag/20261005-1726` (hepsi bir koşu, 7 kesintili başlatma):
- İstenen 914 sembol: 805 bugünkü pay/şirket kodu (borsapy `companies`) + 110 işlemi kapanmış kod (1 kod iki listede). Veri gelen **716**, İş Yatırım'ın boş döndürdüğü 194 (pay olmayan kod, aracı kurum üye kodları vb.;
  `Anlik.bos`, hata sayılmaz), kaynak hatasıyla inmeyen 4 (`CITAS INTEK LRSHO LYDHO`; JSON olmayan yanıt, 3 yeniden
  denemeden sonra). 1.837.862 satır.
- **Bulunamayan kapanmış kodlar:** Borsa İstanbul tablosundaki 110 koddan 21'i İş Yatırım'da yok: OZBAL VIAGO
  UNICO TURSP GARON ISUVT YKSGR AKALT NERGS POLYL SIFAS UZEL UKIM BYSAN EGFIN SPTUR PASTA PNUN EGBRA ERCYS GUNEY.
  Bu tablonun kendisi tam değil (2010 öncesi dahil 186 satır; pay olmayanlar ve 2010 öncesi atıldı). KAP tarafı
  (üyeliği sona erenler sayfası) açılamadı; programatik uç bulunamadı. TASARIM 8.4 güncellendi.
- **İndirme süresi:** 20 sembolde ölçüm 383 sn (19,1 sn/sembol; fiyat 16,9, olay 1,6, sektör 0,64; HUNER tek başına
  139 sn). Tam koşu: fiyat + olay için ~3 sa 10 dk etkin süre (duvar saati 15:07–18:54 = 3 sa 47 dk; ~12–13 sn/sembol,
  yeniden denemeler ve boş sembol kısa), + son adımlar (sektör, faiz, parquet) ~10 dk. Bir ön plan çağrısı 10 dk'da
  kesildiği için koşu ayrı süreç (`Start-Process`) olarak başlatıldı; `Onbellekli` sayesinde çökme sonrası
  yeniden başlatma tamamlananları atladı. 2 saatlik arka plan sınırını da aşan koşu için bu şart.
- **Sektör maliyeti (bilet 04 açık işi):** ilk 100 sembolde ~0,6 sn/istek; sonra KAP boş döndü (`sektor.json` yalnız 100
  sembol, A1CAP–BINHO; sonradan THYAO bile boş). Büyük olasılıkla KAP hız sınırı/engeli. 716 sembolün sektörü
  **alınamadı: 616 eksik.** Sektör yalnız çift ailesi için; evren üyeleri (275 sembol) için bekleme + yeniden deneme
  gerekir. Elle yazma ya da başka kaynak bilet 11'in işi.
- **`sorunlar` tetiklenir.** Tüm evrende karantina oranı **%3,00** (eşik %1; 55.127 gün), olay denetimi farkı
  **%4,15** (eşik %2; 76.200 gün, 102 sembol), inmeyen 4 (eşik 5, geçti). Nedenler:
  - Karantina ilk 20 sembolde %42 (ISATR 3853, ISKUR 3297, AYES 1271, FRIGO 1228, ...): hacimsiz/bozuk satırlı illikit
    kodlar. Hacmi > 0 satırlarda %2,01. **Evren üyeleri** (275 sembol, 2015-12→2026-10) için oran 30.11.2015 sonrası
    **%0,87** (eşik altı), tüm dönemde %1,45. Yıllara göre 2015'te en yüksek (8.027), 2020 sonrası düşük.
  - Olay denetimi: 90 sembolün olay tablosu boş döndü (`GetSermayeArttirimlari`), oysa HGDG/HG oranı sıçrıyor
    (620 sembolde sıçrama; olay tablosu boş 86'sında). Evren üyelerinde bile %3,36 (19 sembol: YGYO, INGRM, ANACM,
    SODA, ADNAC ...). Yani **veri eksik** (olay tablosu ucu bazı bölünme/temettüleri vermiyor).
  - Eşikler 100 hisselik evren için yazılmıştı. `kosu` (bilet 09) bu iki eşiği tüm evren yerine **evren üyeleri**
    üzerinde hesaplamayı ya da eşiği değiştirmeyi TASARIM'da kararlaştırmalı; ben değiştirmedim (açık iş).
- **Tek kod listesi** (`COKLU_KOD`): KAP şirket listesindeki çok kodlu satırlardan (aracı kurum üye kodları ayıklanınca)
  yalnız İş Bankası (ISCTR/ISATR/ISBTR/ISKUR) ve Kardemir (KRDMA/KRDMB/KRDMD). Başka şirket görülmedi; listenin
  tamlığı doğrulanmadı. `pd` kod bazlı (ISBTR 1,2e10, ISCTR 3,0e11): şirket toplamı değil, ama hacmi yüksek kod
  (ISCTR) kalıyor.
- **Evren çıktısı:** 131 ay (2015-12 → 2026-10) her biri tam 100 hisse; hesap 9,6 sn. 2026-10 başı ilk on: ASELS TUPRS
  KCHOL GARAN BIMAS ENKAI THYAO AKBNK VAKBN HALKB. 275 farklı sembol evrene girdi. `kapananlar`: 95 hisse (60 günden
  uzun durdurma ya da kapanma).

**Açık işler (bilet 03'ten):**
1. *Fiyat limiti 30.11.2015 öncesi.* Birincil kaynak (Borsa İstanbul duyurusu / Pay Piyasası Prosedürü) açılamadı
   (PDF okunamadı). İkincil haber kaynakları: 30.11.2015 öncesi iki seansta ±%10, BISTECH ile ±%20; 13.03.2020'de ±%20 ya
   da ±%15 grubundan ±%10'a. **Doğrulanmadı, kod değişmedi** (karantina 2010–2015'te gevşek kalır; ilk sinyal
   30.11.2015). TASARIM 8.5'e kaynaklarıyla yazıldı. ±%15 grubu bilinmiyor.
2. *Olay tarihi ±1 gün kayması limit kontrolünde.* Tam evrende (716 sembol, 1,84 milyon satır) kaydırmalı ve kaydırmasız
   sürüm **aynı 55.127 karantina günü**: sahte karantina yok. Kod eklenmedi (önce yazılan sürüm geri alındı); TASARIM 5.1
   bu davranışı olay denetimi için tanımlıyor, limit için değil.
3. *Sektör maliyeti:* yukarıda.
4. *İndirme süresi:* yukarıda.

**Gerçek veride bulunan ve düzeltilen hatalar** (hepsi test + TASARIM 5.13 önce; her biri koşuyu saatler sonra
düşürüyordu):
- `GetSermayeArttirimlari` planlanmış temettü yer tutucusu: tarih 0001-01-01 (`-62135596800000`) ve çarpan 0 (ACSEL)
  → `oku` çöküyordu; artık tarihsiz/çarpansız kayıt atılıyor.
- İş Yatırım kodu için boş liste → hata değil, `Anlik.bos` (yoksa 194 "inmeyen" `sorunlar`'ı kalıcı tetikleyecekti).
  Boş sembole sektör sorulmaz; sektörü alınamayan sembol indirmeyi düşürmez.
- Ham alanları ve hacmi NaN/0 satır = işlem yapılmamış gün, atılır (BERDN 30.01.2012, ISATR 23.06.2010).
- Birebir aynı tekrar satır (BYDNR) ve yalnız `pd/sermaye` farklı tekrar (KUVVA 2020, iki sermaye değeri) tek sayılır.
  KUVVA'da piyasa değeri bu aralıkta belirsiz.
- Satır içi kısmi NaN artık yapısal ihlal değil, bozuk satır/karantina (IZINV 13.11.2013: yüksek 634210). TASARIM 5.13
  değişti; eski "nan" parametreli test buna göre yeniden yazıldı (gerekçe belgede).
- Sunucu 200 ile JSON olmayan gövde döndürdü (`JSONDecodeError`) → artık geçici hata, 3 yeniden deneme.
- `tests/test_kapilar.py`'deki "tekrar" yapısal ihlal testinin girdisi, birebir aynı tekrarın ihlal sayılmamasına göre
  farklı fiyatlı satıra çevrildi (belge önce).

**Süreç notu.** `evren` testleri kod ile birlikte ilk denemede yeşil geçti (kırmızı adımı atlandı; testler yine elle
hesaplı beklenen değerler taşıyor). Likidite penceresi testi pencere sınırını zayıf sınar (pencere dışı günler medyanı
zaten değiştirmiyor). Sonradan eklenen veri düzeltmelerinin her birinin kırmızısı gerçek veri çöküşüydü, test yazılarak
yeşile çevrildi.

**Bağımlılık.** `xlrd==2.0.2` eklendi (Borsa İstanbul `.xls` dosyası; stdlib okumuyor). Ortak `.venv`'e kuruldu.

**Açık işler (sonraya):**
- `kosu`'nun `sorunlar` eşiklerini evren üyeleri üzerinden hesaplaması (yukarıda) ve olay tablosu eksikliği (ya da oran
  sıçramasından olay çıkarma).
- Kapanma nedeni listesi: Borsa İstanbul tablosunda 18 satırda açıklama (birleşme vb.) var; `nedeni_bilinen` henüz
  bu açıklamalara bağlanmadı, yani hepsi −%100 (karamsar). 95 kapananın hangileri gerçek kapanma, hangileri geçici
  durdurma ayrımı yapılmadı (60 günü aşan durdurma kapanma sayılıyor).
- Sektör kapsamı (616 eksik) ve 4 inmeyen sembol.
- Büyük `veri/onbellek/20261005` klasörü (1.820 dosya) silinmedi; istenirse elle silinir.
