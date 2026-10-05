# Sorgu 3–4 birleştirme (05.10.2026)

2.000 soru, 20 dosya. Soruları 20 ajan yazdı (cevapsız). Cevapları başka 20 ajan, soruyu yazanı görmeden,
kaynaktan ve veriden verdi. Bu belge cevaplardaki önerileri birleştirir ve kararı yazar. Karar vericisi
Claude'dur (Levent: "sen karar veriyorsun"). Soru ve cevaplar: `sorgu-3/`, `sorgu-4/`.

Hüküm toplamı (cevaplayıcıların bildirdiği sayımların toplamı; 20 numaralı dosya elle sayıldı, ±2):
sorgu-3 (tasarım) CEVAPLI 123, EKSİK 662, YANLIŞ 40, OLGU 126, ZAYIF 49 (= 1.000);
sorgu-4 (altyapı) CEVAPLI 44, KARAR 785, YANLIŞ 72, OLGU 39, ZAYIF 60 (= 1.000).
Çoğu "EKSİK/KARAR" aynı birkaç boşluğun farklı sorulardaki yansımasıdır; aşağıda birleştirildi.

Kural ihlalleri (kayıt için): 06 cevaplayıcısı sadakat sırasında bir KRDMD getirisini hesapladı; 02
cevaplayıcısı istek sınırını aştı (~27/15). O getiri rakamı hiçbir kararda kullanılmaz.

## A. Veriyle doğrulanan olgular

| # | Olgu | Doğrulayan |
|---|---|---|
| O1 | `HACIM` TL'dir (HACIM = DOLAR_HACIM × kur; bedelsizde sıçramaz). | 01, 02, 03, 06, 08 |
| O2 | `HGDG` brüt nakit temettüyü de düzeltir; olay tablosu çarpanı HGDG/HG oranını yeniden üretir (CCOLA 13/13, THYAO tam). | 02 |
| O3 | Olay tablosundaki tarih hak kullanım (ex) günüdür; çarpan o günden önceki satırlara uygulanır. | 02 |
| O4 | Fiyat limiti tabanı önceki **kapanıştır**, AOF değil (SMRTG 19/19; ±%10 dönemi). | 07 |
| O5 | `MIN == MAX` tek başına kilit değildir (BALAT 629 gün, KONTR 10/25 limit dışı). | 01, 07 |
| O6 | İş Yatırım 2000'den veri verir (THYAO 6.684 satır). Durdurma ve kapanış "eksik satır" değil, sıfır hacimli satırdır. | 01, 03 |
| O7 | ECILC/RYSAS 12.03.2020 limit içinde; TASARIM 5.1'deki karantina örneği yanlıştı (Yahoo hatası). | 01, 02 |
| O8 | borsapy politika faizi 2015'ten itibaren tek seridir; TLREF/EVDS gerekmez. | 08, 01 |
| O9 | KRDMD sıkışma oranı = (en büyük EMA − en küçük EMA) / EMA200, EMA'lar **ham** kapanıştan `ewm(adjust=False)`; dönem ortalaması %0,638 (Tansu %0,64). | 06, 10 |
| O10 | Tansu VAKBN–GARAN'da **ham** fiyat kullanıyor (14.05.2025 ipucu kutusu ham seriyle birebir; HGDG tutmuyor). Z formülü 40.560 adayla bulunamadı. | 10 |
| O11 | Tansu'nun SMRTG AB=CD işlemleri **aşağı yönlü**; giriş C fiyatında; SMRTG #1'de A stopu −%10 verirdi, tablo −%23. | 05 |
| O12 | AGROT–GARAN rotasyon değil (iki bacak + nakit) ve borsapy'ye göre farklı sektörde. | 04, 03 |
| O13 | %10 pozisyon tavanı günlerin %80–100'ünde bağlar; fiili risk ≈ %0,6–0,8, %1 değil. | 07, 08, 10, 06 |
| O14 | 1.000 tekrarda en küçük p ≈ 0,001; Holm'da 50'den fazla denemede kabul imkânsız. | 09, 15, 04, 10, 19 |
| O15 | Kodda kullanılmayan kurulu paketler: vectorbt/numba, quantstats, duckdb, streamlit, pandas-ta-classic (yalnız ATR). | 12, 11 |
| O16 | Eski kodda hatalar: EMA ilk fiyattan değil (Tansu da öyle, sorun değil), sıkışma "art arda 3 gün" yerine "10 günde 3", oran paydası kapanış; `rapor/*.parquet` git'te. | 19, 06, 12, 20 |
| O17 | borsapy'de açılış sütunu var; İş Yatırım'da yok. | 01 |

## B. Kararlar: tasarım

1. **Aile sayısı 3 → 2.** AB=CD ilk sürümden çıkar: Tansu'nun sınaması açığa satış yönünde ve C
   fiyatından (O11); BIST'te bireysel açığa satış pratik değil; alış yönlü hali Tansu'nun gösterdiği
   kural olmaz. İkinci dalgaya geçer; geometri sadakati yönsüz olarak sonra yapılır. Holm'daki deneme
   sayısı da azalır. (05, 10)
2. **Fiyat serileri.** Sınamada göstergeler ve getiriler `HGDG`'den (temettü dahil). Kendi olay çarpanımız
   yalnız denetimdir (fark = uyarı). Fiyat limiti, kilit ve likidite ham `HG`'den. Sadakat ham `HG` ile
   (O9, O10). İş Yatırım ham seri Yahoo ham seriyle aynı çıktığı için **Yahoo hiç kullanılmaz.** (01, 02, 10)
3. **İşlem fiyatı AOF kalır.** borsapy açılışı ikinci bir kaynağı motora bağlar; değmez (O17 not edildi).
4. **Stop dolumu = min(stop, AOF)**, gün düşüğü ≤ stop olduğunda. Giriş gününde yalnız stop bakılır. (07, 08)
5. **Kilit** = MIN = MAX, HACIM > 0 ve kapanış o günün limit fiyatında (önceki ham kapanış × (1 ± L),
   bir fiyat adımı toleransla). (O4, O5)
6. **Veri penceresi:** 2010'dan indirilir (EMA200 ısınması ≥ 500 gün); ilk sinyal 30.11.2015. (01, 06)
7. **Veri kapıları** (yeni 5.13): MIN ≤ AOF ≤ MAX, MIN ≤ KAPANIŞ ≤ MAX; HACIM = 0 işlem günü değildir;
   eşikler getiri görülmeden yazılır. (01, 02)
8. **Faiz:** tek seri borsapy politika faizi, ileri doldurma, bir gün gecikmeli; TLREF/EVDS çıkar. (O8)
9. **Evren:** ayın ilk işlem günü, önceki ayın son kapanışındaki piyasa değerine göre en büyük 100;
   60 günlük medyan TL hacimde en alttaki %20 elenir. Evrenden çıkan hissenin açık pozisyonu açık kalır.
   İşlemi kapanan hisse: son işlem fiyatı yerine −%100 (nedeni bilinmiyorsa), son fiyat duyarlılık.
   60 işlem gününden uzun durdurma = kapanma. (03)
10. **Çift:** β ≤ 0 çift elenir; X/Y rolü sembol sırasından; 5'ten az çift varsa boş pay nakitte; aynı
    sektörden en fazla 2 çift; AGROT–GARAN Tansu listesinden çıkar; "tek gün ΔZ" YORUM etiketli;
    hazırlık H → K; sadakat hedeflerine Beta 1,675, korelasyon 0,731, piyasada kalma %72,27 eklenir. (04, 10)
11. **EMA sıkışması:** formül O9; dönem = oran ≤ %1,2 olan art arda en az 3 gün; oranın eşiği ilk aşan günü
    dönemi bitirir; giriş: bitişten sonra 10 gün içinde kapanış > dönemin en yüksek **gün yükseği** →
    ertesi AOF; dönem başına tek giriş. "520 dönem" sayımı silinir. K1'e "sıkışmasız aynı kırılım" kolu. (06)
12. **Risk:** %10 tavan YORUM olarak işaretlenir; rapor tavanın bağlama oranını ve fiili riski yazar (O13).
    Lot aşağı yuvarlanır; özkaynak = nakit + pozisyonların kapanış değeri. Sinyal günü kapanış < SMA250
    ise giriş yok. (07, 08)
13. **K2 maruziyet eşleşmeli:** sepet ağırlığı = kuralın o günkü yatırımdaki payı; kalan aynı faizi
    kazanır. (09, 08)
14. **Tekrar sayısı B ≥ max(1.000, 20·m)** (m = deneme sayısı). (O14)
15. **K1 rastgele işlemler** kuralın tam çıkış paketini uygular; p tek yönlü; aile p'si iki türün büyüğü. (09)
16. **Blok bootstrap:** blok uzunluğu = max(20, ortalama tutma süresi). (09, 04)
17. **Üçüncü sonuç "Ölçülemedi":** saptanabilir en küçük etki masraf marjından büyükse ya da örneklem
    dolmazsa "geçmedi"den ayrı yazılır. (09)
18. **Boru hattı denetimi:** ilk resmi koşudan önce bir kez sentetik boş veriyle (yanlış kabul ≤ %5) ve
    enjekte edilmiş etkiyle (güç) koşulur. (09)
19. **Piyasa durumu etiketi:** XU100 kapanış > SMA50 (YORUM); VIX yok. "2023 sonrası tutmadı" cümlesi
    silinir (ön deneme rakamına dayanıyordu). (10)
20. **Kart:** "giriş bölgesi" yerine "referans fiyat = sinyal günü kapanışı"; uygulanan büyüklük ve fiili
    risk; çift kartında "simülasyonda şu an X'te". (17, 10)

## C. Kararlar: altyapı

1. **Streamlit yok** (S2-3 geri alındı; üç cevaplayıcı bağımsız aynı sonuç). Rapor tek HTML dosyası
   (f-string, şablon motoru yok), tarayıcıda açılır. Durum: `rapor/durum.txt` ilk satırı
   `TAMAM` / `SORUNLU` / `VERİ YOK`. (17, 11, 12)
2. **Bağımlılıklar:** pandas, numpy, pyarrow, scipy, statsmodels (`coint`, Holm), requests, tzdata,
   borsapy (faiz, sektör, endeks günleri); geliştirme: pytest. Çıkanlar: vectorbt, numba, yfinance,
   pandas-ta-classic, quantstats, duckdb, streamlit. `pyproject.toml`'da `[project]`, `==` sabitli,
   `requires-python = "==3.14.*"`; `pip freeze` ile `requirements.lock.txt`. uv yok. (12, 19)
3. **Modüller** (`tansu/`, düz): `kaynak` (HTTP), `veri` (anlık görüntü, olaylar, kapılar), `evren`,
   `gostergeler` (+ piyasa durumu), `aileler`, `cift`, `motor` (Adım + Motor), `simulator`,
   `istatistik`, `kayit`, `rapor`, `__main__`. Takvim fiyat günlerinden, maliyet bir sabit.
   `kanit.py`, `nabiz.py` ve Yahoo kodu silinir. (11)
4. **Depolama:** her indirme `veri/ag/<YYYYMMDD-HHMM>/` klasörüne parquet + `manifest.json` (sha256);
   önce geçici klasöre yazılır, kapılar geçerse `os.replace`. Her akşam tam indirme (hisse başına bir
   istek). Veritabanı yok. (13, 16, 18)
5. **Açık kartlar ayrıca saklanmaz:** her gün sinyal gününden itibaren Adım ile yeniden hesaplanır
   (belirleyici). Kâğıt üstü dönemin geriye dönük değişmemesi için günlük kart çıktısı
   `kayit/kartlar.jsonl`'e yalnız eklenir. (17, 13 arasındaki SQLite/CSV çelişkisinin çözümü)
6. **Kural kaydı:** parametreler kodda donmuş dataclass; hash = kod dosyalarının `ast.dump` sha256'sı +
   parametrelerin sıralı JSON sha256'sı; deneme günlüğü `kayit/deneme.jsonl`, yalnız ekleme, git'te;
   resmi koşu temiz git ağacı ister. Holm birimi benzersiz kural kimliği. (15)
7. **Günlük koşu:** `python -m tansu gunluk`; Görev Zamanlayıcı tanımı depoda (`kurulum/`), hafta içi
   19:30, 4 saat boyunca saatte bir tekrar, kaçırılanı çalıştır, çakışmayı yok say; günlük dosyası
   `gunluk/YYYY-MM-DD.log` (stdlib logging); 5'ten fazla hisse inmezse SORUNLU; saat Europe/Istanbul. (16)
8. **HTTP:** requests, istekler arası 1 sn, zaman aşımı (5, 30), ağ/429/5xx için 3 deneme; şema `assert`. (18)
9. **Test:** yüzler Adım, Motor, Simülatör, İstatistik, Evren, veri kapıları, aileler, kayıt; beklenen
   değerler kodu görmemiş ayrı bir ajanın elle hesabı; testte sabitler literal; ağ `conftest` ile
   kapalı; bir "veriyi kes, geçmiş değişmesin" testi; hypothesis/coverage/CI yok; paket < 60 sn. (14)
10. **Git:** `.gitignore`'a `rapor/`, `*.parquet`; izlenen ön deneme dosyaları `git rm --cached`;
    `.gitattributes` `* text=auto eol=lf`. Yedek tutulmaz (Levent 05.10). (20)
11. **Hız:** numba yok; saf döngü; bütçe 200 tekrar ≤ 5 dk. Yetmezse önce algoritma, sonra joblib. (19)

## D. Levent'in kararları (05.10)
1. AGENTS.md'ye ajan kuralları yazılır (izin verildi).
2. Yedek tutulmaz.

## E. Açık kalanlar
Vergi; İş Yatırım yayın saati ve hız sınırı; kapanmış sembollerin tam listesi (FINBN boş, VAKFN zaman
aşımı); ±%20 dönemi limit tabanı; çift Z formülü (YORUM: log oran, 60 gün); sıkışma oranının paydası
düşüş trendinde EMA200 mü en küçük EMA mı (KRDMD'de ikisi aynı).
