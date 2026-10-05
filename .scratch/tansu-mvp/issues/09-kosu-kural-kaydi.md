# 09: `kosu()`, kural kaydı ve deneme günlüğü

**What to build:** `python -m tansu sinama` ve `python -m tansu kayit` komutları çalışır.
- `kosu()`, getiri gösteren tek yoldur. Kural kaydı yoksa ya da hash uyuşmazsa tek Türkçe satırla durur.
- Her koşu `kayit/deneme.jsonl`'e iki satır yazar: önce `basladi`, sonra `bitti`. Alanlar TASARIM 5.11'dedir.
- Bu dilimde koşunun çıktısı 08'in işlem listesidir.

**Blocked by:** 08

**Status:** done

- [x] Kural kaydı:
  - Elle yazılmış `KOD_DOSYALARI` listesinin `ast.dump` sha256'sı
  - Parametrelerin sıralı JSON'unun sha256'sı
  - Izgara tanımı
  - `kural_id` bunlardan türetilir.
- [x] Kapsam testi: her `tansu/*.py` ya `KOD_DOSYALARI`'nda ya `HASH_DISI`'nda bulunur.
- [x] Günlük yalnız eklenir. Her satırda `tur`, `resmi` ve `kirli` alanları vardır. Satırda ayrıca şunlar
      yazılır: ortam (sürümler, lock sha256), anlık görüntü kimliği ve manifest sha256'sı.
- [x] Resmi koşu temiz git ağacı ister; kirli ağaçta yapılan koşu `resmi:false` yazılır.
- [x] Koşu başında manifest yeniden hash'lenir; uyuşmazsa koşu durur.
- [x] Testler `kosu()` yüzünden:
  - kayıt yoksa durma
  - hash uyuşmazlığı
  - `bitti` satırı olmayan `basladi` satırının deneme sayılması
  - aynı tohum ve aynı anlık görüntü aynı özeti verir

## Comments

- `tansu/kayit.py`: `kayitla()` kural kaydını `deneme.jsonl`'e `tur=kayit` satırı olarak yazar; `kosu()` önce kaydı
  ve hash'i denetler, sonra manifesti, sonra `basladi` ve `bitti` yazar. Komutlar: `kayit`, `sinama [--resmi]`.
- `KOD_DOSYALARI` şimdilik aileler, gostergeler, motor. `cift`, `simulator`, K1 kodu gelince listeye eklenir
  (liste değişince kural_id değişir; yeni kayıt ve yeni deneme).
- Açık (02): conftest `kayit.KAYIT_DIZINI`'ni `tmp_path`'e yönlendirir; yapıldı, 02'deki kutu işaretlendi.
- Açık (08): düşen sinyal sayısı `kosu` dönüşünde (`dusen`) ve `bitti` satırında (`dusen_sinyal`).
- Açık (05): `kayit/` izlenir (TASARIM 5.11 "Git" maddesi, AGENTS). `.gitignore` zaten `kayit/`'ı saymıyor.
  05 çalışma ağacındaki izlenmeyen `kayit/` bu dalda yok; birleştirmede orada commit'lenir ya da atılır.
- Açık: ham p, masraf sonuçları ve `--son` tekrar sayısı bilet 12'de; `bitti` satırında yok.
- Açık: resmi koşunun temiz-ağaç denetimi `git status --porcelain -- . :!kayit` ile yapılır; testte `git` enjekte edilir.
- Açık: ızgara tanımı `IZGARA` sabiti (KURALLAR §3 madde 2); yalnız EMA sıkışması için.
