# Veri envanteri

Ölçüm tarihi: 31.10.2026. Veri bütün çalışma kopyalarının dışında, tek kalıcı klasördedir: masaüstündeki `TANSU-veri`
(`Path.home() / "Desktop" / "TANSU-veri"`; `TANSU_VERI` ortam değişkeni başka klasör seçer). Bu belgedeki `ag/`,
`onbellek/` ve `arsiv/` yolları bu klasöre göredir. Veri Git'te değildir. Karar: Levent 31.10.2026
(`kanit/acik-sorular.md` "Verilen kararlar").

## Biçim

- Anlık görüntü: `ag/<YYYYMMDD-HHMM>/`. `fiyat.parquet` kaynağın düzeltilmiş ve ham fiyatlarını, `olaylar.json`
  bölünme ve temettü olaylarını taşır. `manifest.json` sembolleri, inmeyen ve boş sembolleri ve her dosyanın SHA-256
  özetini yazar. Bütün BIST indirmesinde `kapanan.csv` (işlemi kapanan kodlar) da vardır. `veri.oku` özetleri
  doğrular; uyuşmazlık `VeriHatasi` verir.
- Dönem: 02.01.2019'dan indirme gününün son seansına. `VERI_BASLANGIC` 01.01.2019'dur; 2019-2020 yalnız ısınmadır
  (SPEC 3.4).
- Okuma anındaki kalite kuralları (karantina, olay denetimi, kaynak günü) `veri.Anlik` içinde uygulanır, görüntüye
  yazılmaz; biri değişince yeniden indirme gerekmez. Yazma anındaki üç kural `veri.indir` içindedir: tekrar eden satır
  düşer, fiyatı ve hacmi 0 ya da boş satır düşer, `_yapi_denetimi` bozuk sırayı ve tekrar eden günü durdurur. Bunlardan
  biri değişince yeni görüntü gerekir. Önbellek kaynağın yanıtını bu süzgeçlerden önce tutar; önbellekli klasörde koşu
  artımlıdır.
- `tansu veri` en yeni 10 görüntüyü tutar, eskilerini siler (SPEC 3.8, `SAKLANAN_GORUNTU`).
- Artımlı önbellek: `onbellek/fiyat-20190101/`, sembol başına `<SEMBOL>.fiyat.parquet` ve `<SEMBOL>.olaylar.json`.
  `kaynak.Artimli` kaynaktan önbellekteki sondan 10. işlem gününden bugüne kadarını ister: son koşudan beri gelen günler
  ve 10 günlük örtüşme. Örtüşen günler önbellekle aynı değilse (yeni bölünme ya da temettü geçmişi değiştirir) o
  sembolün bütün geçmişini yeniden indirir. Önbellekte 10 ya da daha az satırı olan sembol her koşuda tam iner; bütün
  BIST görüntüsünün 181 boş sembolünün hepsi böyledir.
- Bütün komutlar veriyi kalıcı klasörden okur: `tansu sina` ve `tansu ayarla` `ag/` altındaki en yeni görüntüyü
  kullanır (`tansu/__main__.py` `veri_koku`). Çalışma kopyasının kendi `veri/` klasörü kullanılmaz. Klasör yoksa komut
  hata verip çıkar; `./veri`'ye dönmez ve klasörü kendisi açmaz.
- Bir klasörde aynı anda tek `tansu veri` koşar (`tansu-veri.kilit` üzerinde işletim sistemi kilidi; süreç bitince
  kalkar). İkinci koşu hata verip çıkar. Okuyan komut kilit istemez: `veri.indir` görüntüyü `_gecici-<kimlik>`
  klasörüne yazıp tek adımda adlandırır, okuyan yalnız `2` ile başlayan klasörleri görür.
- Testler kalıcı klasöre dokunmaz: `tests/conftest.py` her testte `TANSU_VERI`'yi geçici bir klasöre yöneltir. Altın
  test kalıcı klasörü yalnız okur.

## Kalıcı klasördeki veri

| Yol | Görüntü | Sembol | Fiyat satırı | Son gün | İnmeyen | Boş | Boyut | Kopyalandığı yer |
|---|---|---|---|---|---|---|---|---|
| `ag/20261026-2018` | 20261026-2018 | 45 | 83.977 | 26.10.2026 | 3 | 0 | 6,6 MB | `.claude/worktrees/yeniden-kurulus` |
| `ag/20261026-2042` | 20261026-2042 | 47 | 87.887 | 26.10.2026 | 1 | 0 | 6,8 MB | `.claude/worktrees/yeniden-kurulus` |
| `ag/20261026-2108` | 20261026-2108 | 48 | 89.842 | 26.10.2026 | 0 | 0 | 7,0 MB | `.claude/worktrees/yeniden-kurulus` |
| `ag/20261028-2353` | 20261028-2353 | 655 | 964.070 | 28.10.2026 | 3 | 181 | 57 MB | `.claude/worktrees/intelligent-herschel-d2835e` |

- Bütün görüntüler 02.01.2019'da başlar. En yenisi bütün BIST görüntüsü 20261028-2353'tür; `tansu sina` her
  kopyada onu kullanır.
- Üç 20261026 görüntüsü, bütün BIST kararından (28.10.2026) önceki BIST 30 evrenidir.
- Önbellek `onbellek/fiyat-20190101/`: 836 sembol, 1.672 dosya, 91 MB; `intelligent-herschel-d2835e` kopyasından.
- `arsiv/intelligent-herschel-d2835e/rapor/`: o kopyanın dört koşu çıktısı (`gartley` ve `ortalama-kesisim`,
  `islemler.csv` ve `sinama.html`). Başka hiçbir kopyada aynıları yoktu.
- Veri 31.10.2026'da kopyalandı, taşınmadı; kaynak kopyalar yerinde duruyor. Her dosya SHA-256 ile denetlendi:
  görüntü dosyaları manifeste ve kaynağa, önbellek ve arşiv dosyaları kaynağa karşı; 1.699 denetim (9 manifest özeti,
  1.689 dosya kaynağa, 1 önbellek dosya listesi), 0 uyuşmazlık.
- Ana kopyadaki `veri/` (623 MB) eski projenin klasörüdür (05.10.2026 görüntüleri); bu envanter onu sınamadı ve
  kopyalamadı.

## Ne zaman yeniden indirilir

- En yeni görüntünün son günü, sınamanın istediği son seanstan eskiyse: `tansu veri`. Hangi kopyadan koşulursa koşulsun
  kalıcı klasöre yazar.
- Kalıcı klasörde önbellek olduğu için koşu artımlıdır. Süresi ölçülmedi; `intelligent-herschel-d2835e` kopyasındaki
  dosya zamanlarına göre önbellekli bütün BIST koşusu yaklaşık 72 dakika sürdü (çıkarım).
- Önbellek yoksa koşu tam indirmedir. 28.10.2026'da bütün BIST 3 sa 39 dk sürdü (`kanit/acik-sorular.md`).
- İki koşu da 10 dakikadan uzundur; Levent'in onayını ister (`AGENTS.md`).
- Okuma anındaki kalite kuralı değişince gerekmez; yazma anındaki kural değişince gerekir. Evrene yeni sembol girince
  gerekir; yeni sembol önbellekte olmadığı için tam iner.

## Denetim

`tests/test_ice_aktarma.py`, `tansu` paketinin testi koşan kopyadan geldiğini denetler. Ana `.venv`'deki düzenlenebilir
kurulum ana kopyayı gösterir; `pyproject.toml` `pythonpath = ["."]` olmazsa testler başka kopyanın kodunu sınar.
