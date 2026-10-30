# Veri envanteri

Ölçüm tarihi: 31.10.2026. Veri Git'te değildir (`.gitignore`: `/veri/`). `veri/` yolları çalışma kopyasının köküne,
tablodaki kopya yolları ana kopyanın köküne göredir.

## Biçim

- Anlık görüntü: `veri/ag/<YYYYMMDD-HHMM>/`. `fiyat.parquet` kaynağın düzeltilmiş ve ham fiyatlarını, `olaylar.json`
  bölünme ve temettü olaylarını taşır. `manifest.json` sembolleri, inmeyen ve boş sembolleri ve her dosyanın SHA-256
  özetini yazar. Bütün BIST indirmesinde `kapanan.csv` (işlemi kapanan kodlar) da vardır. `veri.oku` özetleri
  doğrular; uyuşmazlık `VeriHatasi` verir.
- Dönem: 02.01.2019'dan indirme gününün son seansına. `VERI_BASLANGIC` 01.01.2019'dur; 2019-2020 yalnız ısınmadır
  (SPEC 3.4).
- Okuma anındaki kalite kuralları (karantina, olay denetimi, kaynak günü) `veri.Anlik` içinde uygulanır, görüntüye
  yazılmaz; biri değişince yeniden indirme gerekmez. Yazma anındaki üç kural `veri.indir` içindedir: tekrar eden satır
  düşer, fiyatı ve hacmi 0 ya da boş satır düşer, `_yapi_denetimi` bozuk sırayı ve tekrar eden günü durdurur. Bunlardan
  biri değişince yeni görüntü gerekir. Önbellek kaynağın yanıtını bu süzgeçlerden önce tutar; önbellekli kopyada koşu
  artımlıdır.
- `tansu veri` en yeni 10 görüntüyü tutar, eskilerini siler (SPEC 3.8, `SAKLANAN_GORUNTU`).
- Artımlı önbellek: `veri/onbellek/fiyat-20190101/`, sembol başına `<SEMBOL>.fiyat.parquet` ve
  `<SEMBOL>.olaylar.json`. `kaynak.Artimli` kaynaktan önbellekteki sondan 10. işlem gününden bugüne kadarını ister: son
  koşudan beri gelen günler ve 10 günlük örtüşme. Örtüşen günler önbellekle aynı değilse (yeni bölünme ya da temettü
  geçmişi değiştirir) o sembolün bütün geçmişini yeniden indirir. Önbellekte 10 ya da daha az satırı olan sembol her
  koşuda tam iner; bütün BIST görüntüsünün 181 boş sembolünün hepsi böyledir.
- Komutlar veriyi çalışılan klasörden okur: `tansu sina` ve `tansu ayarla`, `./veri/ag/` altındaki en yeni görüntüyü
  kullanır (`tansu/__main__.py` `VERI_KOKU`).

## Yerel görüntüler

| Çalışma kopyası | Görüntü | Sembol | Fiyat satırı | Son gün | İnmeyen | Boş | Boyut |
|---|---|---|---|---|---|---|---|
| `.claude/worktrees/yeniden-kurulus` | 20261026-2018 | 45 | 83.977 | 26.10.2026 | 3 | 0 | 6,6 MB |
| `.claude/worktrees/yeniden-kurulus` | 20261026-2042 | 47 | 87.887 | 26.10.2026 | 1 | 0 | 6,8 MB |
| `.claude/worktrees/yeniden-kurulus` | 20261026-2108 | 48 | 89.842 | 26.10.2026 | 0 | 0 | 7,0 MB |
| `.claude/worktrees/intelligent-herschel-d2835e` | 20261028-2353 | 655 | 964.070 | 28.10.2026 | 3 | 181 | 57 MB |

- Bütün görüntüler 02.01.2019'da başlar.
- `yeniden-kurulus` kopyasının üç görüntüsü, bütün BIST kararından (28.10.2026) önceki BIST 30 evrenidir. Bu kopyada
  önbellek yoktur.
- Bütün BIST görüntüsü (57 MB) ve önbelleği (836 sembol, 91 MB) `intelligent-herschel-d2835e` kopyasındadır.
- Ana kopyadaki `veri/` (623 MB) eski projenin klasörüdür (05.10.2026 görüntüleri); bu envanter onu sınamadı.

## Ne zaman yeniden indirilir

- En yeni görüntünün son günü, sınamanın istediği son seanstan eskiyse: `tansu veri` komutunu sınamanın koşacağı
  kopyada çalıştır.
- Önbelleği olan kopyada koşu artımlıdır. Süresi ölçülmedi; `intelligent-herschel-d2835e` kopyasındaki dosya
  zamanlarına göre önbellekli bütün BIST koşusu yaklaşık 72 dakika sürdü (çıkarım).
- Önbelleği olmayan kopyada koşu tam indirmedir. 28.10.2026'da bütün BIST 3 sa 39 dk sürdü (`kanit/acik-sorular.md`).
- İki koşu da 10 dakikadan uzundur; Levent'in onayını ister (`AGENTS.md`).
- Okuma anındaki kalite kuralı değişince gerekmez; yazma anındaki kural değişince gerekir. Evrene yeni sembol girince
  gerekir; yeni sembol önbellekte olmadığı için tam iner.
- `yeniden-kurulus` kopyasında `tansu sina` bugün 48 sembollük görüntüyü kullanır, bütün BIST'i kullanmaz. Açık soru
  `kanit/acik-sorular.md` "Levent kararı bekleyenler" bölümündedir.

## Denetim

`tests/test_ice_aktarma.py`, `tansu` paketinin testi koşan kopyadan geldiğini denetler. Ana `.venv`'deki düzenlenebilir
kurulum ana kopyayı gösterir; `pyproject.toml` `pythonpath = ["."]` olmazsa testler başka kopyanın kodunu sınar.
