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
