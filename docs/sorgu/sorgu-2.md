# Sorgu 2 (grilling, 52 soru) — 05.10.2026

Kendi tasarımımı (TASARIM taslak 4, KURALLAR) sorguladım. Olgu gerektiren sorular veriyle doğrulandı;
doğrulanamayanlar "AÇIK" diye işaretli. ⚠️ = tasarımı değiştiren karar.

Doğrulanan olgular (bu sorguda koşuldu):
- İş Yatırım `HisseTekil` 2015'ten geçmiş veriyor (THYAO 2.947 gün, 02.01.2015–02.10.2026).
- **Açılış fiyatı yok.** Alanlar: KAPANIS, MAX, MIN, AOF (ağırlıklı ortalama), HACIM, PD (piyasa değeri), SERMAYE.
- İşlem sırası kapanmış hisseler var: ASYAB 25.07.2016'ya kadar (395 gün).

## A. Amaç ve ürün
1. **Sistem gerçek parayla mı işleyecek?** Hayır. İlk sürüm kâğıt üstü; para kararı Levent'in.
2. ⚠️ **Kartta TL adet mi, oran mı?** Levent'in sermayesi bilinmiyor. Kartta "sermayenin %'si" ve
   "1.000.000 TL için adet" birlikte yazılır. Sınama ölçekten bağımsız oranlarla okunur.
3. ⚠️ **Panel ertelendi; Levent "modern, A'dan Z'ye çalışan" istedi. Çelişki?** Evet. Karar: ilk
   sürümün sonunda tek sayfalık Streamlit "Kanıt" ekranı (rapor ve piyasa durumu okuyucu). Kart ekranı
   bir aile kabul edilince.
4. **Hiçbir aile geçmezse?** Rapor "geçmedi" der, sıradaki aileleri listeler; günlük veri ve durum
   etiketi yine üretilir.
5. ⚠️ **Tansu yeni paylaşım yaptıkça ne olur?** Katalog yaşayan belgedir. Yeni paylaşım `.scratch/`
   altında bir iş olur; aynı süreçten (kaynak → sadakat → kayıt → sınama) geçer.
6. **Vergi masrafa dahil mi?** AÇIK: yerleşik bireysel yatırımcı için hisse kazancı stopajı ve
   temettü vergisi doğrulanmadı. %0,5 masraf senaryosu bir kısmını karşılar; rapor bunu yazar.

## B. Veri
7. ⚠️ **Açılış yok; "ertesi açılışta giriş" nasıl modellenir?** Doğrulandı: açılış yok. Karar: işlem
   fiyatı **ertesi günün ağırlıklı ortalama fiyatı (AOF)**. Bireysel yatırımcı gün içinde işlem yapar;
   açılış müzayedesinin oynaklığından bağımsızdır. Tansu'nun "T+1 Open" kuralı sadakat kontrolünde
   Yahoo açılışıyla ayrıca üretilir.
8. ⚠️ **Stop dolumu açılışsız?** Gün düşüğü ≤ stop ise: gün yükseği de stopun altındaysa (gün boyu
   stopun altında, boşluk) dolum AOF; değilse stop fiyatı.
9. ⚠️ **Tavan girişi açılışsız nasıl anlaşılır?** Gün düşüğü = gün yükseği = tavan fiyatı (kilitli tavan)
   ise alınamaz. Aksi halde AOF'tan alınır.
10. ⚠️ **Taban kilidi?** Düşük = yüksek = taban ise çıkış ertesi güne kayar.
11. **Kapanmış hisseler veride var mı?** Evet (ASYAB). Hayatta kalan yanlılığı azaltılabilir; gereken
    şey geçmiş sembol listesi (soru 20).
12. **Düzeltilmiş fiyat (HGDG) geçmişe dönük değişir mi?** Yeni bir bedelsizde bütün geçmiş yeniden
    ölçeklenir. Bu yüzden ham fiyat + olay tablosu saklanır, anlık görüntü tarihlidir. (Değişiklik yok.)
13. ⚠️ **Göstergeler hangi seriden?** Göstergeler ve getiriler düzeltilmiş seriden (HGDG); aksi halde
    bedelsiz günü sahte kırılım olur. Fiyat limiti ve likidite TL tutarı ham seriden (HG).
14. **HACIM lot mu TL mi?** AÇIK. İlk veri işinde fiyat × lot ile karşılaştırılarak çözülecek.
15. **Tatiller ve eksik günler?** İş Yatırım'ın verdiği günler işlem günüdür; XU100 ile kesişim alınır.
16. **İş Yatırım günlük veriyi saat kaçta yayınlıyor?** AÇIK. 19:30 koşusundaki tazelik kontrolü
    (son tarih = bugün) bunu yakalar.
17. **Sorgu yükü?** İlk yükleme hisse başına tek istek (11 yıl tek seferde geliyor), sonra günlük 1
    istek. İstekler arasında 1 sn bekleme; yerel önbellek.

## C. Evren
18. **Geçmiş BIST100 listesi hazır olmadan ilk sürüm bekler mi?** Hayır; KAP işi paralel yürür.
19. ⚠️ **Daha iyi bir ara çözüm var mı?** Evet: veride piyasa değeri (PD) var. Evren = her ay başında,
    işlem gören hisselerden piyasa değeri ve 60 günlük medyan TL hacmi şartını sağlayan en büyük 100.
    Bu nokta-zamanlı bir "BIST100 benzeri" evrendir ve kapanmış hisseleri de içerebilir.
20. **Bütün sembollerin (kapanmışlar dahil) listesi nereden?** AÇIK: bugünkü bütün hisseler (borsapy)
    + KAP'ta işlem sırası kapatılanlar. Bulunamazsa kalan yanlılık raporda yazılır.
21. **Çiftlerde sektör bugünkü sınıflamadan; geçmişte değişmiş olabilir.** Kabul edilen küçük yanlılık;
    raporda yazılır.
22. **Bankalar, holdingler, GYO dahil mi?** Evet. Çiftler zaten sektör içinde kurulur.

## D. Çift rotasyonu
23. **Sapma formülü sadakatle bulunamazsa?** log(Y) − log(X), pencere 60 gün (YORUM).
24. **β ileriyi görüyor mu?** β ve ortalama/std yalnız geçmiş pencereden hesaplanır.
25. **İlişki bozulursa?** Tansu'nun kuralında çıkış yok; sadakat gereği eklenmez. Yıllık yeniden
    seçimde çift listeden düşerse pozisyon kapanır, pay yeni çifte geçer.
26. **Yıl başında aynı çift yine seçilirse?** Pozisyon devam eder; işlem yapılmaz.
27. ⚠️ **Bir hisse birden çok çiftte olursa (GARAN üç örnekte)?** Bir hisse en fazla bir çiftte; p'si en
    iyi olan çift kalır.
28. **ΔZ > 0 tek gün yeterli mi?** Tansu'nun raporu öyle (+0,30). Evet.
29. **İlk sinyale kadar nakit?** Politika faizi kazanır.
30. **Karşılaştırma?** K1 rastgele geçiş + K2 50/50 tutma. (Taslak 4'te var.)

## E. AB=CD (C'den D'ye)
31. ⚠️ **C pivotu ne zaman bilinir?** Ancak sağ teyit penceresi dolunca. Giriş C fiyatından değil, teyit
    gününün ertesi AOF'undan. Tansu'nun tablosu C fiyatından alıyorsa geleceği görüyor olabilir; fark
    raporda gösterilir.
32. **Hangi yön?** Yalnız alış: A dip, B tepe, C daha yüksek dip; D yukarıda.
33. **Geometri?** BC ≤ AB ve C > A.
34. ⚠️ **Stop: 2 ATR mi, yapı mı?** Tansu'nun AB=CD kuralında "C'den sonra fiyat A'yı geçerse kalıp ölür"
    (ikinci el) var. SMRTG zararları (−%12 ile −%25) 2 ATR'den çok daha geniş, yapısal stopla uyumlu.
    Karar: AB=CD stopu = A seviyesi. Genel 2 ATR stop bu ailede kullanılmaz.
35. **Hedef oranı?** 1,0 ana sınama; 1,27 ayrı deneme.
36. **D'ye hiç ulaşılmazsa?** SMA250 altı kapanış ve A stopu çıkışı sağlar; süre sınırı yok.

## F. EMA sıkışması
37. **Oranın paydası kapanış mı EMA200 mü?** Sadakat kontrolü (KRDMD %0,64) belirler.
38. **"130 mum" kural mı?** Hayır; Tansu'nun ekranının görüntü penceresi.
39. **Aşağı kırılım?** Yalnız alış; girilmez.
40. **Stop?** Risk paketi (2 ATR); hedef yok, SMA250 çıkışı.

## G. Motor ve sınama
41. ⚠️ **vectorbt AOF dolumunu ve "boşlukta AOF" stop kuralını yapabilir mi?** Fiyat dizisi verilebilir,
    ama koşullu stop dolumu yapılamaz. Karar: **motor kendi Adım döngümüzdür**; vectorbt motor olarak
    kullanılmaz. Adım fonksiyonu canlı günlük için zaten gerekli. Ölçütler quantstats'tan.
42. **Pozisyon sınırı rastgele kurala da uygulanır mı?** Evet, aynı 10 pozisyon ve aynı sıra kuralı.
43. **Parametre sabitse ileri yürüme ne işe yarar?** Yıl yıl sonuç gösterir; tek bir iyi yılın sonucu
    taşıyıp taşımadığını açığa çıkarır.
44. ⚠️ **1.000 rastgele tekrarın süresi?** Geliştirmede 200, son raporda 1.000 tekrar.
45. **Holm için deneme nasıl sayılır?** Her (aile, varyant, parametre) bir deneme.
46. **Çift bölmesinde "yılların %60'ı" ölçütü?** Günlük fazla getirinin yıllık toplamıyla uygulanır.

## H. İşletme
47. **Bilgisayar kapalıysa?** Windows Görev Zamanlayıcı "kaçırılan görevi çalıştır"; ertesi gün telafi.
48. **Hata bildirimi?** İlk sürümde raporun ilk satırı "veri sorunlu"; Telegram sonra.
49. **Kod nereden koşar?** TANSU reposu; günlük koşu kayıtlı (hash'li) koddan.
50. **Beyne yeni Tansu notu eklenince?** `.scratch/` altında katalog güncelleme işi açılır.
51. **Levent'in kendi isteği (fiili dolaşım < %30 taraması)?** İkinci dalga; KAP verisi gerekiyor.
52. **Lisans?** İş Yatırım ve borsapy verisi kişisel kullanım; sistem satılmaz, paylaşılmaz. vectorbt
    motor olmaktan çıktığı için lisans sorunu da kalmadı.

## Açık kalanlar
6 (vergi), 14 (hacim birimi), 16 (yayın saati), 20 (kapanmış sembol listesi).
