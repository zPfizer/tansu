# Gartley yöntem işi: ön kayıt (30.10.2026)

Bu dosya koşulardan önce yazıldı ve commit edildi. Sonradan kural, değer veya geçme şartı değişmez. Değişirse yeni
satır olarak `deneme-defteri.tsv` dosyasına yazılır ve deneme sayılır.

## Soru

Tansu'nun yöntemiyle Gartley ya da AB=CD, boştaki paranın faizinden ayrı gerçek bir kazanç veriyor mu? Karar yalnız
ayrık hisse grubunda verilir.

## Veri ve gruplar

- Veri: İş Yatırım günlük, bütün BIST, 2014-01-02 - 2025-12-31; görüntü 20260101-0000 artı INTEK, LRSHO, LYDHO
  (kaynağın vermediği 5 gün atlandı). Dosya `gunler-2014-2025-A.pkl`, SHA-256
  `0fdd99a7f672247063b1ea32bfee24c8e72c956b0ef202559bec4c55e8f66d66`. Veri depoya girmez.
- Evren: 2015-2022 arasında en az bir satırı olan 556 hisse.
- Ayrık grup: `numpy.random.default_rng(20261030).permutation(sıralı evren)` ilk 185 hisse (üçte bir). Kalan 371 hisse
  ayar grubudur. Liste `hisse-gruplari.csv`, SHA-256 `e17f40df945425e3c3ca1fb11912e2fc80df440d79a9747c0b0bce0256f3547c`.
- Dönem: 2015-2022 (2014 ısınma). 2023-2025 harcandı; sınav diye raporlanmaz. 2014 öncesi indirilmez.
- Ayrık grup sınavdan önce hiçbir koşuda kullanılmaz. Sınav her aday için bir kez koşar.
- Bilinen sınır: dondurulmuş Gartley desen ayarı (pivot 12, tolerans 0,05, emir 20 gün) ve para katmanı 29.10'da
  bütün hisselerle 2015-2022'de seçildi. Bu yüzden ayrık grup Gartley'in eski düğmeleri için tam temiz değildir;
  yeni kurallar (teyitli giriş, süre stopu, R/R kapısı, AB=CD) için temizdir.

## Ortak kurallar (değişmez)

- Motor: `tansu/` b9f6107 (yeniden-kurulus). Maliyet: komisyon %0,1575, kayma 1 fiyat adımı (en az %0,1), taraf başına.
- Para katmanı: `kanit/gartley-para/ayar.json` (SHA-256 `118ad754…32e6`) boyut, nakit ve iz stop ayarları: 100.000 TL,
  işlem başına risk %5, pozisyon en çok %33, nakit yetmezse küçült, likidite %10, iz stop en yüksek kapanış − 3 ATR,
  açılış stopun altındaysa ağırlıklı ortalama fiyattan çıkış, boş nakit politika faizi bir gün gecikmeli %15 kesinti.
- Her sonuç üç parçaya ayrılır: faiz geliri, işlem kârı, en iyi üç işlem olmadan işlem kârı. Ayrıca son kasa,
  yalnız nakit kasası (aynı faiz ve kesinti) ve fark yazılır.
- Sinyal düzeyi R: her sinyal para katmanı olmadan tek birim riskle işlenir (nakit, üst sınır, likidite yok).
  R = (çıkış − giriş − maliyetler) / (giriş − stop). Güven: girişin ISO haftasına göre kümeli 10.000 tekrarlı
  yeniden örnekleme; tek yönlü p = yeniden örneklenen ortalamaların 0 veya altında kalma payı.

## Adım 1: ölçüm

1. Deflated Sharpe ve PBO: 29.10 işinin 148 ayrı ayarı, bütün hisseler, 2015-2022, günlük kasa getirisi eksi yalnız
   nakit getirisi. N = 148. Deflated Sharpe: Bailey ve López de Prado 2014. PBO: CSCV, 16 blok. Önceki desen
   işlerindeki denemeler sayılmadı; N alt sınırdır.
2. Sahte oran sınaması, ayar grubu, 2015-2022: `AB_XA` ~ U(0,45; 0,85), `D_XA` ~ U(`AB_XA` + 0,08; 0,95), diğer
   kurallar dondurulmuş Gartley ile aynı. 100 çekiliş, tohum 20261031. 30'dan az dolumlu çekiliş atılır ve sayılır.
   Ölçü: sinyal düzeyi ortalama R. Gartley çekilişlerin %95'inden yüksekse geometri bir şey katıyor sayılır.
   Basit geri çekilme kuralı: kapanış 200 günlük ortalamanın üstünde ve RSI(2) < 10 olunca ertesi gün ağırlıklı
   ortalama fiyattan alış; stop giriş − 2 ATR(14); çıkış kapanış 5 günlük ortalamanın üstüne çıkınca ertesi gün
   ağırlıklı ortalama fiyattan. Aynı para katmanı.
3. Sinyal düzeyi R, dondurulmuş Gartley: ayar grubu 2015-2022 şimdi; ayrık grup payı yalnız sınav adımında.

## Adım 2: aday G-T (Gartley, Tansu yöntemi)

- Desen: dondurulmuş Gartley sinyali (pivot `sag_bar_12`, tolerans 0,05, emir 20 gün, stop X).
- Dokunuş: emir süresi içinde düşük ≤ D olan ilk gün (t0). t0'dan önce düşük ≤ X olursa kurulum bozulur.
- Teyit penceresi: t0 dahil 10 işlem günü. Teyit günü (tc): kapanış > önceki günün yükseği, RSI(14) > 50, TL hacim >
  önceki 10 günün ortalama TL hacmi. Pencerede teyit yoksa ya da teyitten önce düşük ≤ X olursa işlem yok.
- R/R kapısı: tc kapanışıyla (hedef1 − kapanış) / (kapanış − X) ≥ 1,40. hedef1 = D + 0,382 (A − D).
- Giriş: tc'den sonraki gün ağırlıklı ortalama fiyattan.
- Süre stopu: girişten 10 işlem günü sonra o güne kadar hiçbir kapanış hedef1'e ulaşmadıysa ertesi gün ağırlıklı
  ortalama fiyattan çıkış.
- Diğer çıkışlar: stop X ve iz stop (ortak kurallar).
- Bilgi için (seçimi değiştirmez): yalnız teyit, teyit + süre stopu.

## Adım 3: aday ABCD (AB=CD, yalnız alış)

- Pivot `sag_bar_12`. Sıra A (tepe), B (dip), C (tepe), C < A. q = BC / AB, 0,382 ≤ q ≤ 0,886.
- D = C − 1,0 × (A − B); D < B olmalı. C onayından sonra fiyat A'yı geçerse ya da emir süresi (20 gün) içinde D'ye
  dokunmazsa kurulum düşer.
- Stop: D − 2 ATR(14) (C onay günündeki ATR). Hedef1 = D + 0,618 (A − D).
- Giriş, teyit penceresi, R/R kapısı (1,40), süre stopu ve çıkışlar G-T ile aynı.
- Kelebek yalnız ABCD ayar grubunda aşağıdaki üç şartı geçerse ayrı ön kayıtla eklenir.

## Ayar grubundaki rol

Adaylarda serbest değer yoktur; bütün değerler Tansu kaynağından ya da proje kuralından gelir. Ayar grubu yalnız
hata ayıklama ve bilgi içindir. Ayar grubunda bir hata bulunursa kod düzeltilir; değer değişmez. Her koşu defterde
bir satırdır.

## Sınav ve geçme şartı (ayrık grup, 2015-2022, her aday bir kez)

k = ayrık grupta koşan aday sayısı. Bir aday için EVET üç şartın üçü birden tutarsa:

1. Sinyal düzeyi ortalama R > 0 ve tek yönlü p < 0,05 / k.
2. Para katmanında en iyi üç işlem olmadan işlem kârı > 0.
3. Para katmanında son kasa > yalnız nakit kasası.

En az bir aday EVET ise cevap EVET; yoksa HAYIR.

## Değişiklik 1 (30.10.2026, ayar grubu koşularından sonra, ayrık grupta hiçbir koşudan önce)

Neden: ayar grubunda teyit fiyatı D'nin üstünde olduğu için 1,40 R/R kapısı neredeyse hiç geçilmiyor (G-T'de 13
teyitli kurulumun 13'ü, ABCD'de 159'un 157'si elendi). Levent'in talimatı "kapıyı gerçek süzgeç yap ya da kaldır".
Yeni bir kapı değeri seçmek ayar olur; bu yüzden kapı kaldırıldı. Bu değişiklikler deneme sayılır.

1. `gt-k`: G-T, R/R kapısı yok (teyit penceresi, süre stopu, stop X, iz stop aynı). Ayar grubunda `gt-teyit-sure`
   adıyla koştu.
2. `abcd-k`: ABCD, R/R kapısı yok; diğer kurallar Adım 3 ile aynı.
3. Sahte oran sınaması: kapı bütün çekilişlerde kapalı. Gerçek Gartley'de kapı hiçbir kurulumu elemez (oran hep
   1,403); gerçek sonuç değişmez. 100 çekiliş, tohum 20261031, en az 30 dolum şartı aynı.
4. Sınav adayları: karar için `gt-k` ve `abcd-k`; bilgi için dondurulmuş `gartley` (ayrık grupta tam temiz değil).
   Geçme şartındaki k = 3 (üçü de sayılır; baraj p < 0,0167).
5. Kelebek: `abcd-k` ayar grubunda üç şartı geçerse ayrı ön kayıtla; geçmezse yok.

## İleri izleme

Dondurulmuş `kanit/gartley-para/ayar.json` ve `para.py` para katmanı, 01.10.2026'dan başlayarak 100.000 TL ile kâğıt
üstünde izlenir. Ayar değişmez. Kayıt `takip/` altında, her güncellemede sinyal, dolum, çıkış ve günlük kasa.
