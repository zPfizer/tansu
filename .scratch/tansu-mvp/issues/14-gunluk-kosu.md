# 14: Günlük koşu: kartlar, `durum.txt`, Görev Zamanlayıcı

**What to build:** `python -m tansu gunluk` her hafta içi 19:30'da Levent olmadan çalışır. Sırası:
1. Veriyi indirir ve kapılardan geçirir.
2. Kâğıt ve Canlı ailelerin sinyallerini `rapor/kartlar-YYYYMMDD.csv`'ye yazar.
3. Açık kartları Adım ile günceller ve günün çıktısını `kayit/kartlar.jsonl`'e ekler.
4. `rapor/durum.txt`'e tek bakışlık durumu yazar.

**Blocked by:** 12

**Status:** ready-for-agent

- [ ] `durum.txt` ilk satırı: `TAMAM` / `SORUNLU` / `VERİ YOK` / `BUGÜN ÇUBUK YOK`. Ardından şunlar yazılır:
  - son başarılı koşu saati
  - anlık görüntü kimliği
  - son çubuk tarihi
  - sembol sayısı
  - varsa "çapraz kontrol yok"
  - bir Türkçe eylem cümlesi
- [ ] Kart CSV'si:
  - Ayraç `;`, ondalık virgül, UTF-8 BOM.
  - Sabit sütunlar TASARIM 6.5'teki gibidir.
  - Referans ve stop ham TL olarak verilir; stop "tahmini" diye işaretlenir.
  - Sinyal yoksa yalnız başlık satırı yazılır.
- [ ] Dosyalar geçici dosyaya yazılıp `os.replace` ile taşınır. CSV Excel'de açıksa durum SORUNLU olur ve
      "kapatıp yeniden çalıştır" denir.
- [ ] Bugünün başarılı koşusu varsa komut hiçbir şey yapmadan çıkar. Hata ya da kapı başarısızlığında çıkış
      kodu ≠ 0 olur.
- [ ] Koşu 18:15'ten önce başlarsa kart üretilmez. Kaynak yoksa sınama eski anlık görüntüyle sürer, kart durur.
- [ ] Günlük anlık görüntüler 30 gün sonra silinir; deneme günlüğünde adı geçenler silinmez.
- [ ] Görev Zamanlayıcı tanımı depoda XML olarak durur. Ayarlar TASARIM 6.1'deki gibidir. `schtasks`
      kurulum komutu AGENTS.md'ye yazılır. Kurulumu bir kez Claude yapar ve doğrular.
- [ ] Testler `gunluk(tarih)` yüzünden:
  - dört durum
  - bugün koşulduysa çıkış
  - boş sinyalde yalnız başlık
  - CSV biçimi
  - Excel kilidi yolu
