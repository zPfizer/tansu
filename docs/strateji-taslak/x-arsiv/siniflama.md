# Tansu X arşivi: okuyarak sınıflama (5'erli gruplar)

Yöntem (Levent 07.10): her gönderi metni ve görseliyle okunur; iki bağımsız sınıflayıcı (A, B) aynı grubu ayrı
sınıflar; ayrışma burada gerekçeyle çözülür. Sıra: `tweets.jsonl` ana gönderileri, zamana göre.

Tanımlar:
- **rol:** izlenebilirlik A ekseni + `çift`, `sohbet-duyuru`.
- **kural:** tam = başkası aynı hesabı/işlemi tekrar üretebilir (girdiler yazılı); çekirdek belli = ölçü ya da yön
  belli, eşik/ayrıntı eksik; yalnız fikir; yok.
- **karşılaştırma (defter R001–R263):** aynı / genişletir / yeni / çelişir / ilgisiz.

## Grup 1–2 (pilot) · 24–28.08.2023 · A ve B uyumu: rol 8/10, kural 7/10

| # | id | rol | kural | içerik (birebir alıntı + görsel) | defter | karşılaştırma |
|---|---|---|---|---|---|---|
| 1 | 1694839230298468742 | değerleme-temel | çekirdek belli | "FK 2-3 arası alınıp, 7-5 arası satılabilir. Trade yapmak isteyenler için." DOAS tarihsel F/K (Oca'21–Tem'23): ort 4,90, ±1 SS 3,40/6,39, ±2 SS 1,91/7,88 | yok | yeni: tarihsel F/K bandından al/sat eşiği |
| 2 | 1695107146369671497 | seçim-momentum | yalnız fikir | "#DOAS gümbür gümbür geliyor." "Günün Dikkat Çekenleri" tablosu: Hacim, Getiri, Büyüme, Karlılık, Momentum, Değer, QPS Quant; DOAS QPS 89,4 | yok | yeni: çok faktörlü puan tablosu (aracın sahibi belli değil) |
| 3 | 1695183583676113357 | değerleme-temel | tam | "indirgenmiş nakit akımları analizinde hisse değeri 147TL". Görsel: büyüme 2024T %150, sonra 50/40/40/20/20/18/15/15, terminal %5; FAVÖK marjı %23,1→%20,8; AOSM %13,5; sonsuz büyüme %3; hisse başı 147,30 | yok (çerçeve defter-3 R151, R158) | genişletir: İNA'nın girdileri yazılı örneği. Çelişki: metin "%100", tablo %150 |
| 4 | 1695361936651653499 | değerleme-temel | tam | "Ben bazen KAP'tan bilançoları alır kendi sistemimi kendim kurarım". Yıllık kâr = 2023/6 + 2022/12 − 2022/6 (256.157.000); F/K 22,06; FD/FAVÖK 33,15 | yok (FD tanımı defter-3:175) | yeni: son 12 ay yıllıklandırma formülü |
| 5 | 1695389783147581542 | değerleme-temel | tam | "piyasa çarpanları ... indirgenmiş nakit akım analizi ile fiyat çalışılmıştır ... hedef fiyat 144 TL". Dört yöntem: F/K 47,12; PD/DD 269,47; FD/FAVÖK 161,59; İNA 133,71; eşit ortalama 143,98 | yok (defter-3:178 R151) | çelişir (sürüm farkı): 2023'te dört yöntem eşit ağırlık, 2026'da İNA %40 / çarpan %60. İNA burada 133,71, #3'te 147,30 |
| 6 | 1695424938251796654 | değerleme-temel | yok | "karlılık analizimizi de buraya bırakalım." Brüt marj 32,08 (ort 25,84; sektör 17,1), ROE 89,37, ROIC 42,52 | yok | yeni: veri tablosu, kural yok |
| 7 | 1695433615130210730 | rejim | yalnız fikir | Görsel: faiz yükselince şirket değeri düşer; "sadece Merkez Bankasının politikalarını izleyerek ... pozisyon alınarak pozisyondan da çıkılabilir." | yok (yakın defter-4:290 faiz-bankacılık) | yeni: faiz rejimine göre pozisyon fikri |
| 8 | 1695527170251096405 | sohbet-duyuru | yok | "@kitapvefinans Değerleme çakışmaları için bulunmaz bir kaynak." | yok | ilgisiz |
| 9 | 1696021655947018369 | bölge | çekirdek belli | "#DOAS dip zirve analizimiz". "Dibine Yakın Hisseler": dipten uzaklık % beş pencerede (haftalık 15,72; aylık 52,14; 3A 77,13; 6A 79,17; 12A 81,31) | yok (yakın R004 kanal dibi) | genişletir: dipten uzaklık ölçüsü, eşik yok |
| 10 | 1696022604472111319 | değerleme-temel | çekirdek belli | "10 yıllık F/K ve PD/DD grafiğine bakalım ... Hedef fiyatım 400 üzeri." F/K ort 8,41 (±1 SS 4,06/12,77); PD/DD ort 2,04 | yok | yeni: 10 yıllık F/K ve PD/DD ±SS bandı; hedef 400'ün dayanağı yok |

Ayrışmaların çözümü:
- #3, #5 kural (A çekirdek / B tam; A tam / B çekirdek): tanım gereği **tam**; hesabın bütün girdileri görselde yazılı.
  İşlem (al/sat) kuralı yok; bu "kural" sütununun değil "rol"ün konusu.
- #4 rol (A değerleme-temel / B araç-öğrenme): **değerleme-temel**. Cümle araç tavsiyesi gibi başlıyor, ama
  gönderinin içeriği bir hesap yöntemi (yıllıklandırma, F/K, FD/FAVÖK).
- #4 kural (A ve B çekirdek belli): **tam** yazıldı; bu, iki sınıflayıcının ortak kararını değiştiren benim kararım.
  Gerekçe: #3 ve #5 ile aynı tanım; hesabın bütün girdileri görselde yazılı.
- #7 rol (A rejim / B ilke): **rejim**. Görsel faiz ortamına göre pozisyon almayı söylüyor; ilke değil, piyasa durumu
  kuralı.
- #9 kural (A çekirdek / B yalnız fikir): **çekirdek belli**. Ölçü (dipten uzaklık %, beş pencere) tanımlı, eşik yok.

Grup özeti: 2023'te Tansu'nun ana konusu değerleme (6/10). Defterde bu dönem hiç yok; R kayıtları 2026'dan. İki yeni
ölçü: tarihsel F/K ve PD/DD ±SS bandı (al 2–3, sat 5–7), dipten uzaklık %. Kod: yok.
