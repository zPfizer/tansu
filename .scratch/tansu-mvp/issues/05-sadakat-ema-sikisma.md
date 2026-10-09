# 05: Sadakat kontrolü: EMA sıkışması (KRDMD) ve `sadakat` komutu

**What to build:** `python -m tansu sadakat` komutu Tansu'nun KRDMD ekranındaki rakamları ham seriden
yeniden üretir ve sonucu `docs/sadakat.md`'ye yazar. Bu dilimde iki şey kurulur:
- `gostergeler` modülünün ilk hali: EMA `ewm(adjust=False)`, sıkışma oranı = (en büyük EMA − en küçük EMA)
  / EMA200.
- EMA sıkışması ailesinin sıkışma dönemi tanımı.

Getiriye bakılmaz.

**Blocked by:** 02

**Status:** done

- [ ] Komut KRDMD için şu rakamları basar ve `docs/sadakat.md`'ye yazar. Tolerans önceden yazılıdır:
      Tansu'nun gösterdiği son hanenin yarısı. (Komut basar ve yazar; rakamlar tam tutmadı, aşağıya bak.)
  - Sıkışma dönemi 17.12.2025–14.01.2026, 20 gün.
  - Dönem ortalaması %0,64.
  - 09.04.2026 EMA'ları: 31,92 / 30,74 / 29,58 / 28,43.
- [x] Sıkışma dönemi: oranın ≤ %1,2 olduğu art arda en az 3 gün. Eşiği aşan ilk gün dönemi bitirir.
- [x] Göstergeler için elle hesaplı küçük birim testleri yazılır (EMA ve oran; 5–10 satır veri).
- [x] Komut tekrar koşulduğunda aynı rakamları verir. Bu bir test olarak yazılır ve sahte anlık görüntüyle
      ağsız koşar.
- [x] Deneme günlüğüne `tur=sadakat` satırı yazılır. Bu satır Holm'a girmez.

## Comments

Gerçek ölçüm: KRDMD anlık görüntüsü `20261005-1452` (veri.indir ile paylaşılan köke indirildi).
Komut: `python -m tansu sadakat --kok <veri kökü>`; `docs/sadakat.md` üretilir.

Sonuç (ham kapanış, rapor tarihi 09.04.2026, son 130 gün, tolerans ±0,005):
- Bütün geçmiş (2010'dan): dönem 16.12.2025–14.01.2026, 21 gün, %0,665; EMA'lar 31,9231 / 30,7367 /
  29,5756 / 28,4352. Dönem, gün, ortalama ve EMA200 tutmadı; ilk üç EMA tuttu.
- Son 3 yıl: dönem, gün (20), ortalama %0,641 ve ilk üç EMA tuttu; EMA200 = 28,4366, hedef 28,43,
  fark 0,0066 > 0,005: tutmadı.
- Son 2 yıl: aynı; ortalama %0,642, EMA200 = 28,4370: tutmadı.

Neden: 16.12 günü oran 0,011953, eşiğin hemen altında. EMA200 başlangıca duyarlı (tohum etkisi), ve oran
bu yüzden 16.12'de eşiğin altında ya da üstünde kalıyor. Tansu'nun yfinance geçmiş uzunluğu bilinmiyor.
Düzeltilmiş kapanış (`kapanis`) bütün geçmişte EMA200 = 28,4348 verir (tutar) ama dönem yine 16.12 başlar.
Hiçbir aday dört ölçüyü birden tutturmadı. KURALLAR §4'teki "birebir" ve "ortalama %0,638" ifadesi bu
veriyle (İş Yatırım ham serisi) tam yeniden üretilmedi; ifade Sorgu 3'ün Yahoo verisine dayanıyor olabilir.
Geçmiş uzunluğu adayları (2 ve 3 yıl) seçilmedi; ailenin kuralı değişmedi. Tek aday kalmadığı için
gevşek bant (±0,05) kullanılmadı.

Açık işler:
- KURALLAR §4 "birebir" cümlesi gerçek ölçümle çelişiyor; belgeyi düzeltmek karar gerektirir (Levent).
- `docs/sadakat.md`'yi komut baştan yazar. Bilet 06 (çift Z) kendi bölümünü `rapor_metni`'ne eklemeli.
- `kayit/deneme.jsonl` satırı basit; `kayit` modülü (bilet 09) şemayı üstlenir. `kayit/` git'e girmedi.

- 2026-10-09: Worktree `TANSU-wt/05` ve dal `bilet-05` kaldırıldı (dal master'daydı). Worktree'deki tek `kayit/deneme.jsonl` satırı ana kayda eklenmedi: `olay` alanı yok, `kayit` okuyucusu bozulur. Ham satır:
  `{"tur": "sadakat", "tarih": "2026-10-05T11:56:47.894454+00:00", "anlik": "20261005-1452", "aile": "ema_sikismasi"}`
