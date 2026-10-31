# Veri envanteri

Ölçüm tarihi: 31.10.2026. Veri bütün çalışma kopyalarının dışında, tek kalıcı klasördedir: masaüstündeki `TANSU-veri`
(`Path.home() / "Desktop" / "TANSU-veri"`; `TANSU_VERI` ortam değişkeni başka klasör seçer). Bu belgedeki `ag/`,
`onbellek/` ve `arsiv/` yolları bu klasöre göredir. Veri Git'te değildir. Karar: Levent 31.10.2026
(`kanit/acik-sorular.md` "Verilen kararlar").

## Biçim

- Anlık görüntü: `ag/<YYYYMMDD-HHMM>/`. `fiyat.parquet` kaynağın düzeltilmiş ve ham fiyatlarını, `olaylar.json`
  bölünme ve temettü olaylarını taşır. `manifest.json` sembolleri, inmeyen ve boş sembolleri ve her dosyanın SHA-256
  özetini yazar. Bütün BIST indirmesinde `kapanan.csv` (işlemi kapanan kodlar) da vardır. `veri.oku` özetleri
  doğrular; uyuşmazlık, eksik dosya ya da eksik `manifest.json` tek satırlık `VeriHatasi` verir.
- Dönem: 02.01.2019'dan indirme gününün son seansına. `VERI_BASLANGIC` 01.01.2019'dur; 2019-2020 yalnız ısınmadır
  (SPEC 3.4).
- Okuma anındaki kalite kuralları (karantina, olay denetimi, kaynak günü) `veri.Anlik` içinde uygulanır, görüntüye
  yazılmaz; biri değişince yeniden indirme gerekmez. Yazma anındaki üç kural `veri.indir` içindedir: tekrar eden satır
  düşer, fiyatı ve hacmi 0 ya da boş satır düşer, `_yapi_denetimi` bozuk sırayı ve tekrar eden günü durdurur. Bunlardan
  biri değişince yeni görüntü gerekir. Önbellek kaynağın yanıtını bu süzgeçlerden önce tutar; önbellekli klasörde koşu
  artımlıdır.
- `tansu veri` en yeni 10 görüntüyü ve `stratejiler/ayarlar/*.json` dosyalarındaki `veri_kimligi`nin andığı her
  görüntüyü tutar; ötekileri ve çöken koşuların `ag/_gecici-*` klasörlerini siler (SPEC 3.8, `SAKLANAN_GORUNTU`).
  Korunan kimlikler indirmeden önce okunur. Bir ayar dosyası okunamazsa ya da `veri_kimligi`si `YYYYMMDD-HHMM`
  biçiminde değilse komut dosyayı söyleyen tek satırlık hatayla durur; hiçbir şey indirmez ve silmez. Sınır: yalnız komutun yüklediği kopyanın ayar dosyaları okunur; başka
  bir çalışma kopyasının andığı görüntü korunmaz (denetim 31.10.2026 T-1).
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
  kopyada onu kullanır. İki ayar dosyası da 01.11.2026'dan beri onu anar, bu yüzden budama onu silmez.
- Üç 20261026 görüntüsü, bütün BIST kararından (28.10.2026) önceki BIST 30 evrenidir.
- Önbellek `onbellek/fiyat-20190101/`: 836 sembol, 1.672 dosya, 91 MB; `intelligent-herschel-d2835e` kopyasından.
- `arsiv/intelligent-herschel-d2835e/rapor/`: o kopyanın dört koşu çıktısı (`gartley` ve `ortalama-kesisim`,
  `islemler.csv` ve `sinama.html`). Başka hiçbir kopyada aynıları yoktu.
- Veri 31.10.2026'da kopyalandı, taşınmadı; kaynak kopyalar yerinde duruyor. Her dosya SHA-256 ile denetlendi:
  görüntü dosyaları manifeste ve kaynağa, önbellek ve arşiv dosyaları kaynağa karşı; 1.699 denetim (9 manifest özeti,
  1.689 dosya kaynağa, 1 önbellek dosya listesi), 0 uyuşmazlık.
- Ana kopyadaki `veri/` (623 MB) eski projenin klasörüdür (05.10.2026 görüntüleri); bu envanter onu sınamadı ve
  kopyalamadı.

## Yedek ve geri yükleme

Bir görüntü bir kez silinirse aynısı yeniden indirilemez: kaynak geçmişi değiştirir ve yeni koşu yeni bir kimlik
alır. 31.10.2026 denetimi bunu gördü: iki ayar dosyası `20261028-1723` görüntüsünü anıyordu, görüntü hiçbir yerde
yoktu ve Git'teki raporlar yeniden üretilemiyordu (T-1). Bu yüzden ayar dosyalarının andığı görüntülerin bilgisayar
dışında bir kopyası tutulur.

- Yedek: `<py> -X utf8 -m tansu yedekle <hedef>`. Komut, ayar dosyalarındaki her `veri_kimligi` görüntüsünü ve en
  yeni görüntüyü `TANSU-veri/ag/`'den `<hedef>/ag/`'ye kopyalar. Her kopya önce `<hedef>/ag/_gecici-<kimlik>`
  klasörüne yazılır, `manifest.json`'daki SHA-256 özetleriyle denetlenir, sonra adını alır. Bozuk bir kaynak iyi bir
  yedeğin yerine geçmez. Eski yedek, yeni kopya yerine geçene kadar `<hedef>/ag/_eski-<kimlik>` adıyla kenarda durur
  ve ancak sonra silinir; koşu bu arada kesilirse sonraki koşu onu yerine geri koyar. Ayar dosyası okunamazsa ya da
  `veri_kimligi` geçersizse komut hiçbir şey kopyalamadan tek satırlık hatayla durur. Yedekte denetimden geçen kopya varsa komut onu yeniden kopyalamaz. Her görüntü için bir satır
  yazar; bir görüntü kopyalanamazsa hata satırı yazar, ötekilere devam eder ve 1 koduyla çıkar.
- `<hedef>` var olan bir klasör olmalıdır. Komut onu açmaz: takılı olmayan bir disk ya da yanlış yazılmış bir yol
  başka bir yerde klasör açmaz, hata verir.
- Ne zaman: her `tansu veri` koşusundan sonra ve `veri_kimligi`ni değiştiren her `tansu ayarla` koşusundan sonra.
- Nereye: bilgisayar dışında bir yer (dış disk ya da bulut klasörü). Yeri Levent seçer; seçilene kadar yedek alınmadı
  (`kanit/acik-sorular.md`, "Levent kararı bekleyenler").
- Boyut: bütün BIST görüntüsü yaklaşık 57 MB'dir (tablo aşağıda). Önbellek (`onbellek/`) yedeklenmez; o yalnız
  indirmeyi kısaltır, sonuçları değiştirmez.
- Geri yükleme: `<hedef>/ag/<kimlik>` klasörünü `TANSU-veri/ag/<kimlik>` olarak geri kopyala. `veri.oku` sonraki
  `tansu sina` ya da `tansu ayarla` koşusunda manifesti denetler; uyuşmazlık tek satırlık hata verir. Denetimli yol
  aynı komutun rolleri değişmiş hâlidir: `<py> -X utf8 -m tansu yedekle <TANSU-veri klasörü> --kok <yedek klasörü>`
  korunan ve en yeni görüntüleri yedekten geri kopyalar ve denetler. Eksik `manifest.json` hatası bu komutu söyler.
- `tests/test_yedekle.py` yedeği ve geri yüklemeyi yapay görüntülerle sınar.

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
kurulum tek bir kopyayı gösterir (31.10.2026'dan beri `yeniden-kurulus` ağacı); `pyproject.toml` `pythonpath = ["."]` olmazsa testler başka kopyanın kodunu sınar.
