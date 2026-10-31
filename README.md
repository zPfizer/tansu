# TANSU

TANSU, X'teki analist Tansu'nun işlem stratejilerini koda çevirir. Bulduğu her kurulum için yalnız
Tansu'nun kuralının tanımladığı giriş, stop ve hedef seviyelerini verir. Geçmiş veride bu seviyelerin
ne sıklıkla çalıştığını ölçer. Alım-satım talimatı, adet veya para tutarı vermez; kararı Levent verir.

## Kurulum

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.lock.txt -e ".[dev]"
```

## Kullanım

| Komut | Ne yapar |
|---|---|
| `tansu veri` | Veriyi indirir veya günceller. |
| `tansu sina <ad> [--ac]` | Stratejiyi yıllara göre sınar ve `rapor/<ad>/sinama.html` yazar. |
| `tansu ayarla <ad>` | 2021-2025 üzerinde parametre ayarlar. |
| `tansu yedekle <hedef>` | Ayar dosyalarının andığı veri görüntülerini ve en yenisini `<hedef>/ag/` altına kopyalar ve denetler. |
| `tansu onayla <ad>` | Stratejiyi akşam seviye listesine alır (yalnız Levent). Henüz yapılmadı (SPEC bölüm 12). |
| `tansu tara` | Akşam taraması: `rapor/sinyal/<tarih>.md`. Henüz yapılmadı (SPEC bölüm 12). |
| `tansu durum` | Stratejilerin sınıfı ve durumu. Henüz yapılmadı (SPEC bölüm 12). |

Komutlar PowerShell ve Bash'te her klasörden `~/Desktop/TANSU/.venv/Scripts/python.exe -X utf8 -m tansu <komut>`
biçiminde çalışır. `tansu`, `stratejiler/` ve `rapor/` klasörlerini kendi kökünde okur ve yazar. Kökte kısa
yorumlayıcı yolu `.venv/Scripts/python.exe`, çalışma ağacında `../../../.venv/Scripts/python.exe`'dir (`AGENTS.md`, "Commands").

Veri depoda değildir: masaüstündeki `TANSU-veri` klasöründedir; `TANSU_VERI` ortam değişkeni başka bir klasör seçer.
Görüntüler, yedek ve geri yükleme, yeniden indirme zamanı: `docs/veri-envanteri.md`. Her komut koşusu
`kayit/tansu.log` dosyasına bir satır ekler (Git'te değil).

## Testler

```
.venv\Scripts\python.exe -X utf8 -m pytest -q
```

Hızlı iç döngü için (16 yavaş test hariç): `.venv\Scripts\python.exe -X utf8 -m pytest -q -m "not slow"`.
Teslimden önce ve CI'da `-m` olmadan tam komut çalışır. Yavaş testleri listelemek için: `-m slow --collect-only -q`.

Testler yalnız yapay fiyat serisi kullanır. İş Yatırım verisi depoya girmez.
