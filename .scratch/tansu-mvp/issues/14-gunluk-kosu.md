# 14: Günlük koşu: kartlar, `durum.txt`, Görev Zamanlayıcı

**What to build:** `python -m tansu gunluk` her hafta içi 19:30'da Levent olmadan çalışır. Sırası:
1. Veriyi indirir ve kapılardan geçirir.
2. Kâğıt ve Canlı ailelerin sinyallerini `rapor/kartlar-YYYYMMDD.csv`'ye yazar.
3. Açık kartları Adım ile günceller ve günün çıktısını `kayit/kartlar.jsonl`'e ekler.
4. `rapor/durum.txt`'e tek bakışlık durumu yazar.

**Blocked by:** 12

**Status:** done

- [x] `durum.txt` ilk satırı: `TAMAM` / `SORUNLU` / `VERİ YOK` / `BUGÜN ÇUBUK YOK`. Ardından şunlar yazılır:
  - son başarılı koşu saati
  - anlık görüntü kimliği
  - son çubuk tarihi
  - sembol sayısı
  - bir Türkçe eylem cümlesi
  (Düzeltme: "çapraz kontrol yok" satırı kaldırıldı. Bilet 01 ikinci kaynak olmadığına karar verdi; TASARIM 6.7 de yazmıyor.)
- [x] Kart CSV'si:
  - Ayraç `;`, ondalık virgül, UTF-8 BOM.
  - Sabit sütunlar TASARIM 6.5'teki gibidir.
  - Referans ve stop ham TL olarak verilir; stop "tahmini" diye işaretlenir.
  - Sinyal yoksa yalnız başlık satırı yazılır.
- [x] Dosyalar geçici dosyaya yazılıp `os.replace` ile taşınır. CSV Excel'de açıksa durum SORUNLU olur ve
      "kapatıp yeniden çalıştır" denir.
- [x] Bugünün başarılı koşusu varsa komut hiçbir şey yapmadan çıkar. Hata ya da kapı başarısızlığında çıkış
      kodu ≠ 0 olur.
- [x] Koşu 18:15'ten önce başlarsa kart üretilmez. Kaynak yoksa sınama eski anlık görüntüyle sürer, kart durur.
- [x] Günlük anlık görüntüler 30 gün sonra silinir; deneme günlüğünde adı geçenler silinmez.
- [x] Görev Zamanlayıcı tanımı depoda XML olarak durur. Ayarlar TASARIM 6.1'deki gibidir. `schtasks`
      kurulum komutu AGENTS.md'ye yazılır. Kurulumu bir kez Claude yapar ve doğrular.
- [x] Testler `gunluk(tarih)` yüzünden:
  - dört durum
  - bugün koşulduysa çıkış
  - boş sinyalde yalnız başlık
  - CSV biçimi
  - Excel kilidi yolu

## Comments

**Kod:** `tansu/gunluk.py` (yeni, `kayit.HASH_DISI`'nda: kural kodu değil, `rapor` gibi düzenleme), `__main__ gunluk [tarih]`,
`veri.KaynakYok` (hiçbir sembol inmedi → VERİ YOK), `kayit.kosu` `durum` satırına `kanit` alanı (kart kanıt satırı için),
`kurulum/tansu-gunluk.xml`. Test 217 yeşil (önce 204; `tests/test_gunluk.py` 11 yeni, `test_kosu_k1` +1 assert).
Süreç notu: testler kodtan önce yazıldı ama kırmızı koşu ayrıca çalıştırılmadı (modül yoktu = import hatası); ilk koşuda 11/11 yeşil.

**Belge önce, gerekçeli (TASARIM 6.2, 6.5, 6.7, modül tablosu):**
- "Tam indirme" = her sembolün tüm geçmişi; indirilen semboller bugünün evreni (son tam anlık görüntüden) + dünkü açık kartların
  hisseleri (~100). Sebep: 716 sembol 3 sa 10 dk (bilet 07); görev sınırı 1 saat. **Levent/orkestratör onayı gerekir** (belge yorumu).
- Günlük anlık görüntü `veri/gunluk/ag/`'da (faiz ve sektör yok): `sinama` `veri/ag/`'daki tam görüntüleri seçmeye devam eder;
  KAP'a 100 istek atılmaz. Taban başka aydaysa tabanın son ayının evreni kullanılır (YORUM): tabanın aylık yenilenmesi elle (`evren-indir`).
- Kart durumları, büyüklük tabanı (1.000.000 TL kâğıt özkaynağı, nakit sınırı yok), Tarih = sinyal günü, kanıt satırı kaynağı.
- Kaynak günü hatası: geçmiş günler eksik gün işlenir, yalnız bugünkü kartı durdurur (yoksa 5 tarihsel gün koşuyu hep SORUNLU yapardı).

**Süre (gerçek veri, 05.10.2026 20:42, `veri/gunluk/ag/20261005-2042`):** `gunluk` baştan sona **666 sn (11 dk 6 sn)**: taban yükleme ve evren,
99 sembolün fiyat + olay indirmesi (1 sn politeness aynen), kapılar. Sonuç TAMAM, kapılar gerçek veride geçti. Kart hesabı (Kâğıt varsayımıyla,
99 sembol, tüm geçmiş) **2,0 sn**. 19:30 yuvası ve 1 saatlik sınır yeter (~%18). Tam evren (716) kullanılsaydı ≈ 3 sa. Ölçüm çıktıları
repo dışında (`TANSU-dev/gunluk-olcum`); `kayit/kartlar.jsonl`'e gerçek yazı yok.
Gerçek veride (zorlanmış Kâğıt durumu) tek kart çıktı: KRDMD, sinyal 19.01.2026, AKTİF.

**Görev Zamanlayıcı:** görev adı `TansuGunluk`, durum **Disabled** (karar 1; bilet 15 `schtasks /change /tn TansuGunluk /enable` ile açar).
Doğrulandı (`Get-ScheduledTask`): Pzt–Cum 19:30, yalnız oturum açıkken (Interactive, parolasız), uyandırma kapalı, kaçırılanı çalıştır,
çakışmayı yok say, en çok 1 saat, çalışma klasörü ana depo, yalnız ağ varken, hata olursa saatte bir 4 deneme. `schtasks /create /xml` UTF-8
XML'i okumadı ("kodlama değiştirilemiyor"); PowerShell `Register-ScheduledTask -Xml` ve XML başlığı `UTF-16` bildirimi ile kuruldu (AGENTS.md).
Görev ana depodaki (`C:\Users\levent\Desktop\TANSU`) kodu çalıştırır; bu dal oraya birleşmeden etkinleştirilemez.

**Açık işler:**
- Çift ailesi Kâğıt olursa çift kartı yok (koşu SORUNLU olur ve söyler). Ticket 15 ilk resmi koşuda hangi ailenin Kâğıt olduğunu görünce gerekirse ayrı bilet.
- Kaynak yayını gecikirse "BUGÜN ÇUBUK YOK" tatilden ayırt edilemez ve o günün koşusu biter (TASARIM 6.7'de yazılı sınır).
- Taban (tam anlık görüntü) aylık yenilenmeden evren eski kalır (yaklaşık 3 sa, elle). Bilet 15 öncesi karar: aylık otomatik yenileme istenir mi?
- Kâğıt dönem sayacı ilk Kâğıt `durum` satırından gün // 30; ölçüt 6'nın 30 işlem şartı kartta gösterilmez.
- `gunluk` döngüsü `motor.islemler` ile aynı 12 satırı yineler (Adım ortak; `islemler` kapanmamış pozisyonu döndürmediği için). Bilet 13'ün hız işi motoru değiştirirse birleştirilebilir.
- Gate'te başarısız günlük anlık görüntü diskte kalır (30 gün sonra silinir).
