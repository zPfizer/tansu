### 5.14 Tansu sınaması (Levent kararı 16.10)

Levent 16.10: "Tansu ne diyorsa onu yap." Komut: `python -m tansu tansu-sinama`. Tansu'nun kendi sınama yöntemini uygular.
5.1–5.13 ve `sinama` komutu değişmez; 5.10'daki "En iyi değer seçilmez" `sinama` için geçerli kalır. Bu komut kabul kararına
(5.12) girmez, kart üretmez, m'yi (5.11) artırmaz. Tansu'nun Ham metni bizim YORUM'umuzdan üstündür; Levent kararı ikisinden de.
- **Hisse başına optimizasyon:** her strateji her hissede (çift ailesinde her çiftte) ayrı ızgarayla koşulur. "Lütfen bu
  parametreleri optimize edin." (Ham, tweet-ema-parametre-optimizasyonu-1840438972859732044); "her hisse için farklı
  parametrelerde giriş çıkış yapmak lazım." (Ham, tweet-hisse-bazli-parametre-optimizasyonu-1840170065464803535). Izgara
  KURALLAR §3'tekidir: EMA 27 hücre; çift Z penceresi × Z eşiği, 6 hücre (seçim p'si yıllık çift seçimine aittir, burada yok).
- **Dönem:** Tansu modu bütün dönemdir: "Biz model eğitmedik kardeşim," (Ham, tweet-atr-yon-degisimi-dip-tepe-1927454690960101506).
  Dönem, 2015-12-01 (5.1) ile ısınmanın bittiği günün (tek hisse 500, çift 252 işlem günü; 5.1) geç olanından veri sonuna dek.
- **İleri yürüme (ikinci mod):** "EMA değeri walk forward le optimzie edilerek model oluşturulmuştur." (Ham,
  gorsel-paket-75-isctr-ad-ema-walk-forward). YORUM (bizim): her takvim yılı test yılıdır; seçim o yıldan önce kapanmış
  bütün işlemlerle (genişleyen pencere) aynı sağlam bölge kuralıyla yapılır; en az 2 tam eğitim yılı; test yılında seçilen
  hücrenin giriş günü o yılda olan işlemleri alınır, önceki işlem kapanmadan giren işlem atılır. Sağlam bölge yoksa o yıl nakit.
- **İşlem:** sinyal ve dolum 5.3 ve 5.5 kuralıdır: sinyal kapanışta, giriş ertesi günün AOF'unda (bir çubuk gecikme; Tansu'nun
  kodunda `position.shift(1)`, görsel, tweet-sma-geri-test-sinifi-python-1831402232769847775), acil stop 2 ATR, gün sonu stopu
  SMA250. Çift: geçiş ertesi günün AOF'unda; 5.6'daki engeller (işlem yok, kilit, karantina penceresi) aynıdır. YORUM (bizim):
  tek pozisyon, sermayenin hepsi işlemde, kesirli adet; boştaki nakit faiz kazanmaz (Tansu'nun al-tut kıyaslarında faiz yok).
- **Masraf:** her yönde %0,10, kayma yok: Tansu'nun tablosunda "Komisyon: %0.10" (görsel,
  tweet-winrate-80-tarama-backtest-tablosu-2092745592661246196). İşlem getirisi = çıkış·(1−m) / (giriş·(1+m)) − 1.
- **Al-tut:** aynı hisse, aynı dönem: ilk günün AOF'unda al, son kapanışta sat, aynı masraf. Çiftte 50/50, başta bir kez.
- **Ölçüler** (Tansu'nun tablosunun sütunları, aynı görsel): kazanma oranı, işlem, kazanan, kaybeden, kâr çarpanı (kazançlar
  toplamı / kayıplar toplamının mutlak değeri), ortalama işlem, strateji getirisi, al-tut getirisi, fark, en büyük düşüş, Sharpe,
  Calmar, ortalama tutma (gün), maruziyet, kazanç/kayıp oranı. Ek: işlem getirisinin medyanı ("Ortalamaları temel alan
  indikatörler hava civadır Medyan temelli çalışın", Ham, tweet-medyan-temelli-finansal-indikatorler) ve sinyalden 1, 3 ve 5 gün
  sonraki getirinin medyanı ("sonraki 1, 3 ve 5 günde ne olmuş bakın", Ham, not-backtest-giris-sadeligi-risk-islem-gunlugu).
  YORUM (bizim): Sharpe = günlük getiri ortalaması / sapması × √252, risksiz getiri 0; Calmar = yıllık bileşik getiri /
  |en büyük düşüş|; maruziyet = pozisyonda kapanan gün / dönem günü.
- **Şüpheli bayrakları** (etikettir, süzgeç değil): kazanma oranı ≥ %90 → "şüpheli: aşırı uyum" ("%90'lar ise mümkün
  değildir.", Ham, gorsel-paket-129-doas-lojistik-regresyon-hacim-rsi-filtreli-strateji; eşik bizim YORUM); işlem < 5 →
  "az işlem" (Tansu'nun tablosunda süzgeç "İşlem >= 5", aynı görsel).
- **Sağlam bölge** (kurallar/E K31): "Ama sadece tek bir nokta (13, 47) kârlı, hemen yanındaki (14, 48) felaket zarardaysa,
  bil ki o bir tuzaktır." (Ham, tweet-sma-optimizasyon-saglam-bolge-asiri-uyum-1986899794032304554). YORUM (bizim; vekil 16.10):
  komşu = tek eksende bir adım ötedeki hücre; hücre sağlamdır ⇔ kendisi ve bütün komşuları masraf sonrası net getiri > 0.
  Seçilen hücre = sağlam hücreler içinde komşuluğundaki (kendisi dahil) en küçük net getirisi en büyük olan; eşitlikte ızgara
  sırasındaki ilk. Sağlam hücre yoksa "sağlam bölge yok"; en iyi tek hücre gösterilir, seçilmez.
- **Para çıkmaz:** en iyi hücrenin net getirisi ≤ 0 ise: "Eğer en iyi ayarları bile para kazandırmıyorsa, o stratejiyle vakit
  kaybetmeyi bırakırsın." (Ham, aynı not).
- **Çift adayları** (YORUM, bizim; vekil 16.10): aynı sektördeki hisse çiftleri (5.6 YORUM'u), Y = sembol sırasına göre ilk.
  Günlük anlık görüntüde sektör yoksa sektör tablosu `--sektor-kok` altındaki en yeni tam anlık görüntüden okunur (5.2:
  bugünkü sınıflama). Site denenen çift sayısını ve sağlam bölgeli çiftlerin oranını yan yana yazar.
- **Makine ve paralellik** (Levent kararı 16.10): koşu başında mantıksal çekirdek, boş bellek ve GPU ölçülür. İşçi sayısı =
  min(çekirdek, boş bellek × 0,8 / işçi başı bellek, iş sayısı), en az 1; iş birimi bir hisse ya da bir çifttir. Sonuç işçi
  sayısından bağımsızdır (test). Koşu ilerlemeyi yazar: biten / toplam iş, geçen süre, tahmini kalan süre, CPU kullanımı.
  GPU: ölçüm `.scratch/tansu-sinama/performans.md`'dedir; sonuç bu maddeye yazılır.
- **Kayıt ve çıktı:** sonuç `rapor/tansu-sinama-<koşu>.json`; deneme günlüğüne `tur=destek`, `olay=tansu_sinama` satırı
  (koşu kimliği, anlık görüntü ve manifest sha256'sı, `git_commit`, `kirli`, makine, işçi, süre). Holm ve m bunu saymaz (5.11).
- **Bizim ek kontrolümüz:** aynı ailenin son resmi `durum` satırı (5.11, 5.12) çıktıda ve sitede yanında durur.
- **Hash:** `tansusinama.py` hash dışıdır (kabul kararını değiştirmez). `HASH_DISI` listesine eklenmesi `kayit.py`'nin hash'ini
  değiştirir: sonraki resmi koşudan önce `python -m tansu kayit` gerekir.
