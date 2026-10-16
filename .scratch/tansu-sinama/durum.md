# Tansu sınaması: yöntem maddeleri ve karşılıkları (16.10)

Kaynak listesi: `YONETIM/.scratch/backtest/bulgu-00.md`, `bulgu-01.md`, `bulgu-02.md` içinde sınıfı "backtest yöntemi" ile
başlayan satırlar (yalnız harita). Alıntılar notların "## Ham" bölümünden; üç okuyucu alt ajan 44 notu açıp birebir
doğruladı (16.10). Kod `tansu/tansusinama.py`, test `tests/test_tansusinama.py` (öneksiz yazıldı); belge TASARIM 5.14.
Sütun "Durum": `uygulandı` ya da `kapsam dışı` (neden yazılı). "Tür": Tansu (Ham'daki kural) ya da YORUM (bizim sayı/ayrıntı).

| # | Madde | Not ve Ham alıntısı | Belge | Kod | Test | Durum | Tür |
|---|---|---|---|---|---|---|---|
| 1 | Geçmiş veride test | gorsel-paket-116-veriden-sinyale-algoritmik-trader-gelistirme: Ham'da metin yok, yalnız görsel bağlantısı | 5.14 giriş | `calistir` | `test_komut_uctan_uca_rapor_ve_gunluk_satiri` | uygulandı | Tansu (zayıf, yazar belirsiz) |
| 2 | %90 isabet aşırı uyumdur | gorsel-paket-129-doas-lojistik-regresyon-hacim-rsi-filtreli-strateji: "Finansal piyasalarda %70 gibi bir değer yakalarsanız bu harika bir sonuçtur. %90'lar ise mümkün değildir." | 5.14 Şüpheli bayrakları | `olculer` (`SUPHELI_KAZANMA`) | `test_bayraklar_asiri_uyum_az_islem_ve_temiz` | uygulandı | Tansu; eşik YORUM |
| 3 | Maliyet hesaba katılır | gorsel-paket-63-bist-momentum-dey-backtest-denetimi: "İşlem maliyetleri, vergiler ve likidite sorunu olan hisseler hesaba katılmadı." | 5.14 Masraf | `islem_getirisi` | `test_islem_getirisi_masrafli_cikis_bolu_giris` | uygulandı (maliyet eklendi; vergi ve likidite yok) | YORUM |
| 4 | İleri yürüme | gorsel-paket-75-isctr-ad-ema-walk-forward: "EMA değeri walk forward le optimzie edilerek model oluşturulmuştur." | 5.14 İleri yürüme | `ileri` | `test_ileri_yil_yil_secim_nakit_yili_ve_dikis`, `test_ileri_gelecege_bakmaz_eski_yil_sonraki_secimi_degistirir_oncekini_degil` | uygulandı | Tansu; yıl ve pencere YORUM |
| 5 | Sinyalden 1, 3, 5 gün sonrası | not-backtest-giris-sadeligi-risk-islem-gunlugu: "Backtest yapın. Örneğin 26 Ağustos'ta hangi hisseleri aday seçtiniz sonraki 1, 3 ve 5 günde ne olmuş bakın." | 5.14 Ölçüler | `_sonraki` | `test_ema_uctan_uca_tek_hisse_tek_hucre`, `test_sonraki_gecersiz_gun_sayilmaz` | uygulandı | Tansu; medyan YORUM |
| 6 | Araçta "Backtest Modu" | tweet-abcd-patern-d-hedefi-backtest-2092343114971095065: Ham "MARKA"; "Backtest Modu" yalnız görsel metninde | yok | yok | yok | kapsam dışı: AB=CD ikinci dalga (TASARIM 3) | Tansu |
| 7 | Bütün dönem, eğitim/test bölmesi yok | tweet-atr-yon-degisimi-dip-tepe-1927454690960101506: "Biz model eğitmedik kardeşim," | 5.14 Dönem, İki tanım | `_ema_donem`, `cift_isleri`, `calistir` | `test_ema_uctan_uca_tek_hisse_tek_hucre`, `test_ema_ileri_son_yil_donemin_son_gunu`, `test_cift_son_satir_karantina_karantina_cikisi_veri_sonu_degil` | uygulandı | Tansu; iki tanım YORUM |
| 8 | Takvim ayı ortalaması | tweet-aylik-getiri-mevsimsellik-nisan-sat-agustos-al-1782838495599378879: "son 20 yılın her takvim ayı % getirilerinin ortalamasını gösterir" | yok | yok | yok | kapsam dışı: mevsimsellik kodda aile değil (KURALLAR D) | Tansu |
| 9 | Az veriye güvenme | tweet-aylik-getiri-p-value-sharpe-skewness-eleme-2009899784748794098: "veri sayısı az olduğu için (T-Statistic anlamlı çıkmamış) bu sonuçlara KRDMB kadar güvenemeyiz." | 5.14 Şüpheli bayrakları | `olculer` (`AZ_ISLEM`) | `test_bayraklar_asiri_uyum_az_islem_ve_temiz` | uygulandı | Tansu; eşik 5 Tansu'nun tablosu |
| 10 | Olasılığa göre kasa payı | tweet-aylik-mevsimsellik-olasilik-kasa-ayari-2009731947375854034: "İstatistik bir kristal küre değildir, geleceği kesin olarak göstermez ama size pusula olur" | yok | yok | yok | kapsam dışı: pozisyon büyüklüğü (Kelly ile birlikte Levent'te) | Tansu |
| 11 | Aylık getiri gürültüyü azaltır | tweet-aylik-ortalama-getiri-mevsimsellik-1911360286876925997: "Aylık getiri, gürültüyü azaltır" | yok | yok | yok | kapsam dışı: mevsimsellik kodda aile değil | Tansu |
| 12 | Kazanan ve kaybeden sayısı yakın olmalı | tweet-backtest-asiri-uyum-kontrolu-1992410986989441388: "Kar eden ve zarar eden işlem sayıları hemen hemen aynı olmalı ki overfitting tehlikesi ortadan kalkmış olsun" | 5.14 Ölçüler, Şüpheli bayrakları | `olculer` (kazanan, kaybeden) | `test_olculer_uc_islem_tansu_tablosu_sutunlari` | uygulandı | Tansu |
| 13 | Optimizasyon sonrası %50 kazanma yeterli | tweet-dip-taramasi-backtest-overfitting-1908882937325531171: "Ben matrixdeki robotlarımda da optimizasyon sonrası %50 winrate olan parametreler ile yol alırım." | 5.14 Ölçüler | `olculer` (kazanma) | `test_olculer_uc_islem_tansu_tablosu_sutunlari` | uygulandı (sütun; süzgeç değil) | Tansu |
| 14 | Grid search ile optimizasyon | tweet-dip-tespiti-price-action-teyit-1950987288378519760: "benim de kendi algoritmam var, grid search ile de optimizasyon yapabilirsin." | 5.14 Hisse başına optimizasyon | `ema_tablolari`, `_cift_is` (`IZGARA`) | `test_ema_uctan_uca_tek_hisse_tek_hucre`, `test_cift_uctan_uca_bir_gecis` | uygulandı | Tansu; ızgara değerleri YORUM (KURALLAR §3) |
| 15 | İşlem maliyeti 0,001 | tweet-ema-50-200-maliyetli-backtest-1837452465022615616: "(0.001 işlem maliyeti eklenmiştir)" | 5.14 Masraf | `MASRAF`, `islem_getirisi` | `test_islem_getirisi_masrafli_cikis_bolu_giris` | uygulandı | Tansu |
| 16 | Varsayılanın komşusunu dene | tweet-ema-parameter-optimization-1828127951126446388: "Yani 12-144-169 yerine 11-135-158 yapsam getirim ne olur?" | 5.14 Hisse başına optimizasyon | `IZGARA` | `test_ema_uctan_uca_tek_hisse_tek_hucre` | uygulandı | Tansu |
| 17 | Parametreleri optimize et (brute) | tweet-ema-parametre-optimizasyonu-1840438972859732044: "Lütfen bu parametreleri optimize edin." | 5.14 Hisse başına optimizasyon | `ema_tablolari` | `test_ema_uctan_uca_tek_hisse_tek_hucre` | uygulandı | Tansu |
| 18 | KAP ile güven skoru | tweet-fon-cikisi-satis-baskisi-tahmini-2099970636386812395: "bu tahmini geçmiş KAP raporlarıyla test edip, bu model geçmişte satış yönünü yüzde kaç doğru yakaladı diye bir güven skoru üretsek" | yok | yok | yok | kapsam dışı: fon analizi (E K26–K27, Levent) | Tansu |
| 19 | Kâr çarpanı > 3 olanları listele | tweet-gridsearch-profit-factor-3-bist-1908615000765190336: "Şimdi amaç gridsearch ile bist'te profit factor >3 olan hisseleri listeleyerek onlarda trade etmek:)" | 5.14 Ölçüler | `olculer` (kar_carpani) | `test_olculer_uc_islem_tansu_tablosu_sutunlari` | uygulandı (sütun; >3 süzgeci yok) | Tansu |
| 20 | Dış backtest aracı | tweet-hareketli-ortalama-backtest-araci-1979931015771517315: "Kaydedin lazım olur" | yok | yok | yok | kapsam dışı: dış site, yöntem yok | Tansu |
| 21 | MA kesişiminde rejim için optimizasyon | tweet-hareketli-ortalama-kesisim-optimizasyonu-2071142623520215512: "optimization should actually be used to analyze which moving average crossovers indicate the formation of bearish or bullish markets" | yok | yok | yok | kapsam dışı: MA kesişimi ailesi kodda yok (B §35) | Tansu |
| 22 | Hisse özelinde optimizasyon | tweet-hisse-bazli-ema-optimizasyonu-1845478584154026462: "Ben onu hisse özelinde yapıyorum" | 5.14 Hisse başına optimizasyon | `_ema_isleri`, `_kos` | `test_hisse_siniri_ilk_n_hisse_ada_gore` | uygulandı | Tansu |
| 23 | Her hisse için ayrı parametre | tweet-hisse-bazli-parametre-optimizasyonu-1840170065464803535: "her hisse için farklı parametrelerde giriş çıkış yapmak lazım." | 5.14 Hisse başına optimizasyon | `_ema_isleri`, `cift_isleri` | `test_1_ve_2_iscide_ayni_sonuc` | uygulandı | Tansu |
| 24 | Backtest ve forward test | tweet-kitap-model-sentezi-backtest-forward-test-kod-mimarisi: "Bu yapıyı oluşturduktan sonra sabırla backtest ve forward test süreçlerini yönetmeniz gerekir." | 5.14 İleri yürüme; 5.8 kâğıt üstü dönem | `ileri` | `test_ileri_yil_yil_secim_nakit_yili_ve_dikis` | uygulandı (forward test = kâğıt dönemi, mevcut) | Tansu |
| 25 | Basit tut | tweet-ma-kesisim-var-opt1-opt2-optimizasyon-1784690075059585046: "Basit iyidir. Yormayın kendinizi :)" | yok | yok | yok | kapsam dışı: MA kesişimi ailesi kodda yok | Tansu |
| 26 | Kendi backtest sınıfı (MACD) | tweet-macd-son-gun-al-backtest-1861839074463474170: "Buyurun size backesterclass ile macd son gün al verenler" | yok | yok | yok | kapsam dışı: kod bizde yok, MACD ailesi yok | Tansu |
| 27 | En büyük düşüşe bak | tweet-python-finans-fikir-dogrulama-ve-yanlislama: "en fazla ne kadar zarar (drawdown) ettirdiğini Python kütüphaneleriyle net bir şekilde görebilirsiniz" | 5.14 Ölçüler | `olculer` (max_dd) | `test_olculer_uc_islem_tansu_tablosu_sutunlari` | uygulandı | Tansu |
| 28 | Geleceğe bakma yok | tweet-repaint-free-peak-trough-detector-1908945733903892945: "Model kesinlikle look ahead bias yapmıyor, yani geleceğe bakarak karar vermiyor." | 5.14 İşlem; 5.12 Geleceği görmeme testi | `ema_tablolari`, `ileri` | `tests/test_gelecek.py::test_t_den_sonrasi_veri_t_oncesi_ciktiyi_degistirmez` (bileşen `tansusinama_`) | uygulandı | Tansu |
| 29 | Pencere uzunluğu hisseye göre | tweet-rolling-window-volatility-optimization-1953400490747662376: "Rolling periyot 30 olmaz 40 olur vs vs" | 5.14 Hisse başına optimizasyon | `_cift_is` (`z_pencere` ekseni) | `test_cift_uctan_uca_bir_gecis` | uygulandı | Tansu |
| 30 | Eşiği volatiliteye göre optimize et | tweet-rsi-esik-periyot-optimizasyonu-1860405835354054736: "Hissenin volatilitesine göre değerleri optimize etmeniz lazımç" | 5.14 Hisse başına optimizasyon | `IZGARA` (eşik eksenleri) | `test_ema_uctan_uca_tek_hisse_tek_hucre` | uygulandı (ilke; RSI ailesi kodda yok) | Tansu |
| 31 | Sinyal bir çubuk sonra | tweet-sma-geri-test-sinifi-python-1831402232769847775: "Buyurunuz düzeltilmiş hali." (görsel kodda `position.shift(1)`) | 5.14 İşlem | `ema_tablolari` (`motor.Zincir`), `_cift_simule` (`hedef[q − 1]`) | `test_ema_uctan_uca_tek_hisse_tek_hucre`, `test_cift_uctan_uca_bir_gecis` | uygulandı | Tansu |
| 32 | Sağlam bölge, tek tepe tuzaktır | tweet-sma-optimizasyon-saglam-bolge-asiri-uyum-1986899794032304554: "Ama sadece tek bir nokta (13, 47) kârlı, hemen yanındaki (14, 48) felaket zarardaysa, bil ki o bir tuzaktır." | 5.14 Sağlam bölge, Para çıkmaz | `saglam_bolge` | `test_saglam_bolge_tek_nokta_tuzak_sagliksiz`, `test_saglam_bolge_blok_secim_maksimin_ve_esitlikte_ilk`, `test_saglam_bolge_hepsi_zararda_para_cikmaz` | uygulandı | Tansu; komşuluk ve seçim YORUM |
| 33 | Pivot X çubuk sonra teyit | tweet-swing-pivot-oteleme-backtest-2093465820932235288: "backtest modülünde noktanin gerçekten swing lowpivot olduğundan emin olmak için X bar kadar öteleyerek kodladım." | yok | yok | yok | kapsam dışı: iki ailede pivot yok; pivotlu aile gelince uygulanır | Tansu |
| 34 | Tarama sonucunu gözle incele | tweet-tarama-sonucu-gozle-dogrulama-1839014128201118148: "Ne olursa olsun taramadan çıkan sonuçların göz ile incelenmesi gerekir. En etkili backtest yoludur." | yok | yok | yok | kapsam dışı: göz incelemesi ölçülemez; sitede ayar haritası var, grafik yok | Tansu |
| 35 | Basit tut, net kâr ve düşüş | tweet-teknik-indikator-islem-sistemi-degerlendirme-kriterleri: "Basit tut hala verilebilecek en iyi tavsiyedir." | 5.14 Ölçüler | `olculer` (net, max_dd, calmar) | `test_olculer_uc_islem_tansu_tablosu_sutunlari` | uygulandı | Tansu (yazar belirsiz) |
| 36 | Formasyonu yaz, tara, getiriye bak | tweet-tweezer-bottom-talep-bolgesi-backtest: "Şu tweezer bottom mumunu yazayım taramasını da yapayım buradan da getirisine bakarız." | yok | yok | yok | kapsam dışı: tweezer ailesi kodda yok | Tansu |
| 37 | Sinyalden sinyale performans kodu | tweet-uc-kirmizi-mum-sell-sinyali-performans-kodu-1905475655686353161: "Şu kod yazmak hastalık gibi bir şey." | yok | yok | yok | kapsam dışı: üç kırmızı mum ailesi kodda yok | Tansu |
| 38 | Optimizasyon tek hisse için | tweet-vegas-ema-tek-hisse-optimizasyonu-1846299109302362243: "OPT'leri tek hisse için yapıyoruz." | 5.14 Hisse başına optimizasyon | `_kos` (iş birimi hisse) | `test_1_ve_2_iscide_ayni_sonuc` | uygulandı | Tansu |
| 39 | Optimize etmeniz lazım | tweet-vegas-tuneli-parametre-optimizasyonu-1839323182035316985: "Optimize etmeniz lazım" | 5.14 Hisse başına optimizasyon | `ema_tablolari` | `test_ema_uctan_uca_tek_hisse_tek_hucre` | uygulandı | Tansu |
| 40 | En az 1:2 risk/ödül | tweet-williams-r-sma-swing-strateji-backtest: "Hedef: En az 1:2 Risk/Ödül oranı hedeflenir." | yok | yok | yok | kapsam dışı: modül 1 kuralı, başka oturumda (açık madde) | Tansu |
| 41 | PnL ya da kâr çarpanına göre seç | tweet-zigzag-atr-gridsearch-secimi-1908636901365407759: "Artık PnL ya da profit factor'e göre tercihimi yapıyorum." | 5.14 Ölçüler, Sağlam bölge | `olculer`, `saglam_bolge` (net getiriyle) | `test_saglam_bolge_blok_secim_maksimin_ve_esitlikte_ilk` | uygulandı (seçim net getiriyle) | Tansu |

## Sayım

Komut (bu dosyanın klasöründe):

```
grep -c "^| [0-9]" durum.md; grep "^| [0-9]" durum.md | grep -c "| uygulandı"; grep "^| [0-9]" durum.md | grep -c "| kapsam dışı"
```

Çıktı (16.10): `41`, `27`, `14` (satır, uygulandı, kapsam dışı; 27 + 14 = 41).

Tansu method items mapped: 41 of 41 (bulgu-00: 15, bulgu-01: 14, bulgu-02: 12 satır; komut
`grep -c "| backtest yöntemi" bulgu-00.md bulgu-01.md bulgu-02.md` → 15, 14, 12).

Ek (yöntem satırı değil, brifte anılan): gorsel-paket-53-stat-arb-bag-kopusu-negatif-backtest "Mutlaka backtest etmek lazım"
ve tweet-winrate-80-tarama-backtest-tablosu-2092745592661246196 (tablo sütunları, "Komisyon: %0.10", "İşlem >= 5"; görsel):
TASARIM 5.14 Masraf ve Ölçüler.

TASARIM 5.14'te kullanılan iki tam Ham alıntısı:
- tweet-medyan-temelli-finansal-indikatorler: "Ortalamaları temel alan indikatörler hava civadır Medyan temelli çalışın" (Ölçüler).
- tweet-sma-optimizasyon-saglam-bolge-asiri-uyum-1986899794032304554: "Eğer en iyi ayarları bile para kazandırmıyorsa, o stratejiyle vakit kaybetmeyi bırakırsın." (Para çıkmaz).

## Sürüm 2 (17.10): iki tanım ve uç durumlar (Tansu maddesi değil; YORUM, TASARIM 5.14 "İki tanım")

Sürüm 1 3. denetim turunun bulguları ve testleri (hepsi b464df1 koduyla kaldı, yeni kodla geçti; `kirmizi-v2.txt`):

| Uç durum | Kod (`tansu/tansusinama.py`) | Test |
|---|---|---|
| Son gün karantinalı: karantina çıkışı, veri sonu değil | `cift_isleri`, `cift_tablolari` | `test_cift_son_satir_karantina_karantina_cikisi_veri_sonu_degil`, `test_cift_sonsuz_son_kapanis_son_gecerli_fiyat_ve_karantina_cikisi` |
| İleri yürümenin son yılı dönemin son günü | `_ema_donem`, `_ema_is` | `test_ema_ileri_son_yil_donemin_son_gunu` |
| Sıfır ya da sonsuz fiyat yok sayılır | `_ema_gecerli`, `_cift_gecerli`, `_ema_is`, `_cift_is` | `test_ema_al_tut_donem_basi_aof_sifir_sonraki_gecerli_gun`, `test_ema_al_tut_son_kapanis_sonsuz_son_gecerli_kapanis`, `test_sonraki_gecersiz_gun_sayilmaz` |
| AOF'u olmayan gün dönem başı olamaz | `_ema_donem`, `cift_isleri` | `test_ema_donem_basi_sifir_aof_tek_gun_atlanir`, `test_cift_donem_basi_gecersiz_gun_atlanir[aof_sifir]`, `test_cift_donem_basi_gecersiz_gun_atlanir[limit_asimi]` |
| Tek günlük çift dönemi | `cift_isleri`, `_sonuc` (`donem`) | `test_cift_tek_gunluk_donem_gecersiz_fiyat_atlanir`, `test_cift_tek_gunluk_donem_donem_alani` |

Koşu (sürüm 1, eski kod): `kayit/deneme.jsonl` `olay=tansu_sinama`, koşu 20261016T201747-0a886d (anlık görüntü 20261014-1930).
