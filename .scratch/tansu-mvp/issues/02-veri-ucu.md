# 02: Tek hisse veri ucu: İş Yatırım → anlık görüntü → olay denetimi

**What to build:** Tek bir komut, verilen semboller için şunları indirir:
- İş Yatırım ham ve düzeltilmiş fiyatı, 2010'dan bugüne
- Şirket olayları tablosu

Bunları değişmez, tarihli bir anlık görüntüye koyar ve olay denetimini koşar. CCOLA'nın 13.08.2024
bölünmesi, olay çarpanıyla düzeltilmiş fiyatı (`HGDG`) yeniden üretir. Okuyucu anlık görüntüyü manifest
doğrulamasıyla açar. Bu, sistemin ilk uçtan uca dilimidir: ağdan diske, diskten okumaya.

**Blocked by:** 01

**Status:** done

- [x] `kaynak`:
  - İş Yatırım `HisseTekil` ve `GetSermayeArttirimlari` çağrılır.
  - Ham alan adları tek bir sözlükle proje adlarına çevrilir.
  - İstekler arasında 1 sn bekleme; zaman aşımı (5, 120); ağ, 429 ve 5xx hatalarında 3 deneme.
  - Şema bozuksa açık bir hata verilir.
- [x] `veri.indir`:
  - Önce geçici klasöre yazar.
  - Klasörde uzun biçimli fiyat parquet'i, ham olay JSON'u ve `manifest.json` (sha256) bulunur.
  - İş bitince `os.replace` ile yerine taşır.
  - Tarih sütunu saat dilimsiz olur.
- [x] `veri.oku(kimlik)`: manifesti doğrular; uyuşmazlık hatadır.
- [x] Olay denetimi:
  - Olay çarpanı ±1 işlem günü penceresinde eşleşir.
  - Aynı güne düşen iki kaydın çarpanları çarpılır.
  - `HGDG` ile fark %0,5'i aşarsa uyarı verilir.
- [x] Testler `veri` yüzünden, sahte `kaynak` adaptörüyle:
  - CCOLA 13.08.2024: elle yazılmış küçük ham tablo; beklenen çarpan elle hesaplanır.
  - ±1 gün kayması
  - Aynı güne iki kayıt
  - Bozuk manifest
- [x] Gerçek ağla bir kez elle koşu yapılır: THYAO ve CCOLA anlık görüntüsü oluşur; çıktı commit
      mesajında yazılır.
- [x] `tests/conftest.py` ağı kapatır ve `kayit/` yolunu `tmp_path`'e yönlendirir (yönlendirme bilet 09'da yapıldı).

## Comments

- Gerçek koşu: `veri/ag/20261005-1436`, THYAO ve CCOLA, her biri 4.204 satır (2010-01-04 – 2026-10-02),
  24 ve 12 olay, olay uyarısı 0. Süre 2 sembol için 52,6 sn; evren ölçeği bilet 07'de ele alınır.
- Gerçek koşu bir hata buldu: pencereden önceki olay ilk satıra uygulanıyordu (THYAO 2010, fark 86,7).
  Önce test, sonra düzeltme.
- "3 deneme" = ilk istek + 3 yeniden deneme (5, 15, 45 sn bekleme); toplam 4 çağrı.
- Kod incelemesi (Standards + Spec) sonrası eklendi: bütün fiyat ve olay kayıtlarında şema denetimi,
  olay şemasının `kaynak`'ta denetlenmesi, +1 gün kayma testi, 2 gün kaymanın uyarı verdiği test.
- `kayit/` yönlendirmesi: `kayit` modülü yok; bilet 09 conftest'e ekler.
- Açık: ≤ 0 fiyatlı satırlar denetimden sessizce düşer; bilet 03'ün bozuk satır kuralına eklendi.
- Açık: END_DEGER'in gerçekten XU100 olduğu bilet 04'te doğrulanır.
