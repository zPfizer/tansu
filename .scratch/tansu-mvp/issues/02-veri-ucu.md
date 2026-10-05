# 02: Tek hisse veri ucu: İş Yatırım → anlık görüntü → olay denetimi

**What to build:** Tek bir komut, verilen semboller için şunları indirir:
- İş Yatırım ham ve düzeltilmiş fiyatı, 2010'dan bugüne
- Şirket olayları tablosu

Bunları değişmez, tarihli bir anlık görüntüye koyar ve olay denetimini koşar. CCOLA'nın 13.08.2024
bölünmesi, olay çarpanıyla düzeltilmiş fiyatı (`HGDG`) yeniden üretir. Okuyucu anlık görüntüyü manifest
doğrulamasıyla açar. Bu, sistemin ilk uçtan uca dilimidir: ağdan diske, diskten okumaya.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] `kaynak`:
  - İş Yatırım `HisseTekil` ve `GetSermayeArttirimlari` çağrılır.
  - Ham alan adları tek bir sözlükle proje adlarına çevrilir.
  - İstekler arasında 1 sn bekleme; zaman aşımı (5, 120); ağ, 429 ve 5xx hatalarında 3 deneme.
  - Şema bozuksa açık bir hata verilir.
- [ ] `veri.indir`:
  - Önce geçici klasöre yazar.
  - Klasörde uzun biçimli fiyat parquet'i, ham olay JSON'u ve `manifest.json` (sha256) bulunur.
  - İş bitince `os.replace` ile yerine taşır.
  - Tarih sütunu saat dilimsiz olur.
- [ ] `veri.oku(kimlik)`: manifesti doğrular; uyuşmazlık hatadır.
- [ ] Olay denetimi:
  - Olay çarpanı ±1 işlem günü penceresinde eşleşir.
  - Aynı güne düşen iki kaydın çarpanları çarpılır.
  - `HGDG` ile fark %0,5'i aşarsa uyarı verilir.
- [ ] Testler `veri` yüzünden, sahte `kaynak` adaptörüyle:
  - CCOLA 13.08.2024: elle yazılmış küçük ham tablo; beklenen çarpan elle hesaplanır.
  - ±1 gün kayması
  - Aynı güne iki kayıt
  - Bozuk manifest
- [ ] Gerçek ağla bir kez elle koşu yapılır: THYAO ve CCOLA anlık görüntüsü oluşur; çıktı commit
      mesajında yazılır.
- [ ] `tests/conftest.py` ağı kapatır ve `kayit/` yolunu `tmp_path`'e yönlendirir.
