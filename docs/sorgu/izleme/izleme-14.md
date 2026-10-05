# İzleme 14: cevaplar-14-test.md karşılaştırması (taslak 6)

Kapsam: EKSİK, KARAR, YANLIŞ hükümleri (95 madde). OLGU (073, 089) ve ZAYIF SORU (068, 069, 075) alınmadı.

14-001 — KARAR — VAR — TASARIM 4 (modül yüzleri), sonuc C-9 (yüzler), AGENTS (testler yalnız TASARIM yüzlerinden)
14-002 — KARAR — VAR — TASARIM 4 motor satırı (aynı Adım), TASARIM 6.6 ve sonuc C-5 (açık kart Adım ile yeniden hesaplanır); yapı kanıtlar
14-003 — KARAR — VAR — sonuc C-5 (belirleyici yeniden hesap); test bu özelliği sınar
14-004 — YANLIŞ — VAR — TASARIM 7.1 ve sonuc C-3 (kanit.py, nabiz.py, Yahoo, vectorbt ve testleri silinir); temizlik yapıldı
14-005 — YANLIŞ — VAR — TASARIM 5.3 "Motor sınamaları" giriş günü stop, sinyalden sonra veri yok, açık pozisyonda yeni sinyal zaten içerir; "stop+hedef" hedef yok (TASARIM 5.5) diye geçersiz; "11 durum" yerine liste 9 madde
14-006 — KARAR — VAR — sonuc C-9 (kodu görmemiş ayrı ajanın elle hesabı), AGENTS (beklenen değer elle)
14-007 — KARAR — VAR — AGENTS (elle hesap, literal sabit), TASARIM 5.3 başlığı (elle hesaplanmış örnekler); yorum biçimi ayrıntıdır
14-008 — KARAR — VAR — TASARIM 5.3 Motor sınamaları "stop kenarları (düşük = stop, yüksek = stop)", 5.3 stop dolumu min(stop, AOF)
14-009 — KARAR — RED — TASARIM 5.3 kilidi "bir fiyat adımı toleransla" tanımlar; "tavan − 0,01 → giriş var" bununla çelişir
14-010 — KARAR — VAR — TASARIM 5.1 (L = %20 / %10, 13.03.2020; karantina limit +%0,5, olayla açıklanmayan gün)
14-011 — KARAR — VAR — TASARIM 5.3 (elle hesaplı sınamalar), KURALLAR 4 / TASARIM 7.3 (gerçek veri yalnız sadakat)
14-012 — KARAR — VAR — TASARIM 8.1 (kullanım koşulları açık soru), AGENTS (uzak repo yok)
14-013 — KARAR — VAR — sonuc C-9 (ağ kapalı, test indirmez), TASARIM 4 veri (anlık görüntü tarihli ve değişmez)
14-014 — KARAR — VAR — sonuc C-9 (ağ conftest ile kapalı)
14-015 — KARAR — VAR — TASARIM 4 `kaynak` (ağa çıkan tek yer), sonuc C-8, C-9
14-016 — KARAR — VAR — TASARIM 6.2 ve 5.1 "bugünkü veri" (başarısızlık = kart yok), 5.13 günlük kapı
14-017 — KARAR — VAR — sonuc C-8 (şema assert), TASARIM 5.13 (kapı geçmezse kart yok)
14-018 — KARAR — VAR — sonuc O1 ve TASARIM 5.1 (HACIM TL, doğrulandı); "birim çözülünce" önkoşulu zaten çözüldü
14-019 — KARAR — VAR — TASARIM 5.1 olay denetimi (HGDG farkı > %0,5 uyarı), sonuc O2 (CCOLA)
14-020 — KARAR — VAR — TASARIM 5.1 olay denetimi, sonuc O2 (çarpan HGDG/HG oranını yeniden üretir), O3
14-021 — KARAR — VAR — sonuc O2 (HGDG brüt temettüyü düzeltir, CCOLA 13/13); belirsizlik çözülmüş
14-022 — KARAR — VAR — TASARIM 5.1 karantina (olayla açıklanmayan gün)
14-023 — KARAR — RED — TASARIM 4: takvim fiyat günlerinden çıkar, tatil listesi yok; denetlenecek liste yoktur
14-024 — KARAR — VAR — sonuc C-9 ("veriyi kes, geçmiş değişmesin" testi), TASARIM 5.2 evren tarih bazlı
14-025 — KARAR — VAR — sonuc C-9 (aynı kesme testi); ortak parametrik biçim uygulama ayrıntısı
14-026 — KARAR — VAR — TASARIM 5.2 "İşlemi kapanan hisseler" (kapanan hissede açık pozisyon, nedeni bilinmezse −%100)
14-027 — KARAR — VAR — TASARIM 5.4 (her yönde %0,3; %0,1/%0,5 aynı sabit)
14-028 — KARAR — VAR — TASARIM 5.4 likidite (son 10 gün medyan TL tutarının %2'si)
14-029 — KARAR — YENİ — TASARIM 5.6 tek hisse bölmesi "en likit önce" satırına ekle: eşit likiditede sembol adı alfabetik (girdi sırasından bağımsız)
14-030 — KARAR — VAR — TASARIM 5.6 tek hisse bölmesi (%1 risk, %10 tavan, 10 pozisyon, aşağı yuvarlama)
14-031 — KARAR — VAR — TASARIM 5.6 çift bölmesi ("sonra hep çiftin bir hissesindedir")
14-032 — KARAR — VAR — TASARIM 5.6 "Yıl geçişi" (düşen çift kapanır, yine seçilen işlemsiz devam)
14-033 — KARAR — VAR — TASARIM 5.6 faiz (bir gün gecikmeli, takvim günü, /365), sonuc B-8
14-034 — KARAR — VAR — TASARIM 5.6 (özkaynak = nakit + pozisyonların kapanış değeri)
14-035 — KARAR — VAR — TASARIM 4 (`cift` "kendi döngüsü"; ortak olan motor/simulator yüzü)
14-036 — KARAR — VAR — TASARIM 5.7 fazla getiri tanımı (işlem getirisi − eşit ağırlıklı sepet)
14-037 — KARAR — VAR — TASARIM 5.7 K1 "sayılar hisse başına eşleştirilir", iki tür
14-038 — KARAR — VAR — TASARIM 5.3 yeni sinyal ("rastgele karşılaştırmada da aynı"), 5.7 K1 (tam çıkış paketi), 5.6 (10 pozisyon)
14-039 — KARAR — YENİ — TASARIM 5.7 K1 "Seçim": uygun gün kümesi gereken sayıdan küçükse `ValueError`, sessiz kırpma yok
14-040 — KARAR — VAR — TASARIM 5.11 (tohum kayıtlı), 5.7 K1 (tekrar sayısı), sonuc C-9
14-041 — KARAR — VAR — sonuc C-2 (`==` sabitli bağımlılık, numpy sürümü sabit), TASARIM 5.11 (tohum + commit kayıtlı); özellik/aralık sınama uygulama ayrıntısı
14-042 — KARAR — VAR — TASARIM 5.9 (blok yeniden örnekleme), 5.12 (boru hattı denetimi bir kez); ayrı kapsama simülasyonu 5.12'de yok ve gerekmez
14-043 — KARAR — VAR — sonuc C-9 (paket < 60 sn), TASARIM 5.7 (geliştirmede 200 tekrar)
14-044 — KARAR — VAR — TASARIM 5.9 (≥ 100 işlem, ≥ 60 sinyal günü), 5.12 "Ölçülemedi"
14-045 — KARAR — VAR — TASARIM 4 `istatistik` (Holm statsmodels), 5.11; elle hesap doğru (0,03; 0,06; 0,06; 0,02)
14-046 — KARAR — RED — pandas-ta yok: TASARIM 4 gostergeler "kütüphane yok", sonuc C-2; ATR/EMA kendi kodumuz, elle hesapla sınanır
14-047 — KARAR — TEKRAR — 14-042
14-048 — KARAR — VAR — TASARIM 5.12 boru hattı denetimi (enjekte edilmiş etki), sonuc B-18
14-049 — KARAR — VAR — TASARIM 5.12 (sentetik boş veriyle yanlış kabul ≤ %5), sonuc B-18
14-050 — KARAR — VAR — TASARIM 5.12 (altı koşul, p < 0,05, yılların en az %60'ı)
14-051 — KARAR — VAR — TASARIM 1 ("Hiçbir aile geçmedi" birinci sınıf sonuç), sonuc C-1 (Streamlit yok)
14-052 — KARAR — YENİ — AGENTS test kapısı satırına ekle: `tests/conftest.py` autouse fixture `kayit/` yazma yolunu `tmp_path`'e yönlendirir (gerçek `deneme.jsonl` ve `kartlar.jsonl` testte kirlenmez)
14-053 — KARAR — VAR — sonuc C-6 (`ast.dump` sha256 + parametre JSON'u), TASARIM 5.8
14-054 — KARAR — VAR — TASARIM 5.8 ("ilk getiri koşusundan önce kayda geçer"), sonuc C-6 (resmi koşu temiz ağaç ister)
14-055 — KARAR — VAR — KURALLAR 4 (sadakat kontrolü; üretilemezse YORUM kalır, raporda yazılır), TASARIM 7.3
14-056 — KARAR — VAR — KURALLAR 1 madde 3 ("not ile görsel çelişirse görsel geçerli"), KURALLAR 4
14-057 — KARAR — RED — Yahoo kararı (sonuc B-2, C-2): yfinance kaynaklı fixture olamaz; sadakat verisi İş Yatırım ham seridir
14-058 — KARAR — YENİ — KURALLAR 4 "Kural" listesine ekle: sadakat toleransı (son hanenin yarısı) aday denemeden önce yazılır
14-059 — KARAR — VAR — AGENTS (`skip`/`xfail` yasak), KURALLAR 4 (üretilemeyen YORUM kalır, raporda yazılır)
14-060 — KARAR — RED — sonuc B-3 (işlem fiyatı AOF, açılış kaynağı bağlanmaz); ikinci fiyat sütunu yolu spekülatif esneklik
14-061 — KARAR — RED — kapsam dışı: tepe/pivot ailesi ilk sürümde yok (AB=CD ikinci dalga); genel kesme testi C-9'da var
14-062 — KARAR — VAR — KURALLAR 4 (aday formüller sadakatle elenir, getiriye bakılmaz), TASARIM 7 sırası (sadakat motor testinden önce)
14-063 — KARAR — VAR — KURALLAR 3.1 (Z ≤ −2 ve ΔZ > 0 → Y'ye geç; Z ≥ +2 ve ΔZ < 0 → X'e)
14-064 — KARAR — VAR — KURALLAR 3.2 (oran ≤ %1,2, art arda ≥ 3 gün, 10 gün içinde giriş)
14-065 — KARAR — VAR — TASARIM 5.1 (2010'dan indirme, göstergeler ısınır); pandas-ta kısmı moot (C-2)
14-066 — KARAR — TEKRAR — 14-067 (altın dosya yok); pandas-ta ikamesi RED (14-046)
14-067 — KARAR — VAR — AGENTS (beklenen değer elle hesaplanır, kodun çıktısıyla yeniden üretilmez)
14-070 — KARAR — RED — TASARIM 6.4 kart CSV'si `;` ayraç, ondalık virgül, UTF-8 BOM der; madde "ondalık nokta" der, çelişir
14-071 — KARAR — TEKRAR — 14-067
14-072 — KARAR — VAR — sonuc C-9 (hypothesis yok)
14-074 — KARAR — VAR — sonuc C-9 (hypothesis yok)
14-076 — KARAR — VAR — TASARIM 5.3 (boşluklu stop, kilit = düşük=yüksek ve hacim > 0), 5.1 hacim 0 işlem günü değil, 5.13 satır şartları
14-077 — KARAR — VAR — AGENTS (elle hesap), sonuc C-9 (ayrı ajan hesabı), TASARIM 5.5 (ATR 14 Wilder)
14-078 — YANLIŞ — VAR — AGENTS "Testte sabitler literal yazılır", sonuc C-9; `test_kanit.py` zaten silindi (TASARIM 7.1)
14-079 — KARAR — VAR — sonuc C-9 (mutasyon/coverage/CI yok), AGENTS (önce kırmızı test)
14-080 — KARAR — VAR — sonuc C-9 (coverage yok)
14-081 — KARAR — TEKRAR — 14-100
14-082 — KARAR — VAR — sonuc C-1 (Streamlit yok; rapor tek HTML), TASARIM 4 `rapor`
14-083 — KARAR — VAR — TASARIM 6.1 (Görev Zamanlayıcı tanımı `kurulum/`), TASARIM 7.9
14-084 — KARAR — YENİ — TASARIM 4 `__main__` satırına ekle: `gunluk` bugünün tarihini parametre alır (varsayılan `date.today()`); 14-085 buna dayanır
14-085 — KARAR — VAR — TASARIM 5.1 "Bugünkü veri" (son çubuk bugün değilse kart yok), 6.2
14-086 — KARAR — VAR — sonuc C-9 (paket < 60 sn)
14-087 — KARAR — VAR — TASARIM 7.8–7.9 (koşular test değil), sonuc C-11 (200 tekrar bütçesi)
14-088 — KARAR — VAR — AGENTS test kapısı (`.venv\Scripts\python.exe -m pytest -q`)
14-090 — KARAR — VAR — AGENTS test kapısı, sonuc C-9 (CI yok)
14-091 — KARAR — VAR — AGENTS "Testi gevşetme yasak"; ikinci oturum diff incelemesi gerekmez
14-092 — KARAR — RED — AGENTS test kapısı (commit öncesi yeşil) ile çelişir: "kırmızı test" commit'i kapıyı bozar; kırmızı kanıt aynı oturumda görülür
14-093 — KARAR — VAR — sonuc C-3 (modül adları), TASARIM 7.1 (nabız kodu ve testleri silindi; `test_nabiz.py` yok)
14-094 — KARAR — RED — sonuc B-19, C-3: nabiz.py silindi, piyasa durumu = XU100 > SMA50; TAM_ALIM/BEKLE/DIKKATLI ve SMA 18/35–20/50 çelişkisi kalktı
14-095 — KARAR — TEKRAR — 14-029
14-096 — KARAR — VAR — TASARIM 5.3 "Yeni sinyal" ve Motor sınamaları (açık pozisyonda yeni sinyal)
14-097 — KARAR — VAR — TASARIM 5.10 (rastgele ızgara, pozitif hücre oranı)
14-098 — KARAR — YENİ — `.gitignore`: `veri/` satırı `tests/veri/` dosyalarını da gizler; `veri/` yerine `/veri/` yaz (ya da fixture klasörünü `tests/fixture/` yap)
14-099 — KARAR — RED — aşırı kurulum: her assert'e kural atıflı mesaj yazmak stil ayrıntısıdır; Türkçe test adı yeter
14-100 — KARAR — RED — aşırı kurulum: TASARIM 5.3 Motor sınamaları, 5.12 ve C-9 ölçüyü zaten verir; ayrı "yeterlilik" paragrafı kopya olur ("11 durum" da 14-005'te hatalı)

## Özet

Sayımlar (grep ile): VAR 73, TEKRAR 5, YENİ 6, RED 11. Toplam 95.

YENİ maddeler ve önerilen değişiklik:
- 14-029: TASARIM 5.6 "en likit önce" satırına: eşit likiditede sembol adı alfabetik (14-095 aynı test).
- 14-039: TASARIM 5.7 K1 Seçim: uygun gün kümesi gereken sayıdan küçükse ValueError, sessiz kırpma yok.
- 14-052: AGENTS test kapısı satırı: conftest autouse fixture kayit/ yolunu tmp_path'e yönlendirir.
- 14-058: KURALLAR 4 Kural listesi: sadakat toleransı (son hanenin yarısı) aday denemeden önce yazılır.
- 14-084: TASARIM 4 __main__ satırı: gunluk bugünün tarihini parametre alır.
- 14-098: .gitignore `veri/` yerine `/veri/` (tests/veri/ fixture'ı gizlenmesin).

YANLIŞ maddeler VAR değil olanlar: yok. 14-004, 14-005, 14-078 üçü de VAR (kanıt satırlarında).
