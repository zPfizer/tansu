# 09: `kosu()`, kural kaydı ve deneme günlüğü

**What to build:** `python -m tansu sinama` ve `python -m tansu kayit` komutları çalışır.
- `kosu()`, getiri gösteren tek yoldur. Kural kaydı yoksa ya da hash uyuşmazsa tek Türkçe satırla durur.
- Her koşu `kayit/deneme.jsonl`'e iki satır yazar: önce `basladi`, sonra `bitti`. Alanlar TASARIM 5.11'dedir.
- Bu dilimde koşunun çıktısı 08'in işlem listesidir.

**Blocked by:** 08

**Status:** ready-for-agent

- [ ] Kural kaydı:
  - Elle yazılmış `KOD_DOSYALARI` listesinin `ast.dump` sha256'sı
  - Parametrelerin sıralı JSON'unun sha256'sı
  - Izgara tanımı
  - `kural_id` bunlardan türetilir.
- [ ] Kapsam testi: her `tansu/*.py` ya `KOD_DOSYALARI`'nda ya `HASH_DISI`'nda bulunur.
- [ ] Günlük yalnız eklenir. Her satırda `tur`, `resmi` ve `kirli` alanları vardır. Satırda ayrıca şunlar
      yazılır: ortam (sürümler, lock sha256), anlık görüntü kimliği ve manifest sha256'sı.
- [ ] Resmi koşu temiz git ağacı ister; kirli ağaçta yapılan koşu `resmi:false` yazılır.
- [ ] Koşu başında manifest yeniden hash'lenir; uyuşmazsa koşu durur.
- [ ] Testler `kosu()` yüzünden:
  - kayıt yoksa durma
  - hash uyuşmazlığı
  - `bitti` satırı olmayan `basladi` satırının deneme sayılması
  - aynı tohum ve aynı anlık görüntü aynı özeti verir
