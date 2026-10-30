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
| `tansu onayla <ad>` | Stratejiyi akşam seviye listesine alır (yalnız Levent). |
| `tansu tara` | Akşam taraması: `rapor/sinyal/<tarih>.md`. |
| `tansu durum` | Stratejilerin sınıfı ve durumu. |

Komutlar `python -X utf8 -m tansu <komut>` biçiminde de çalışır.

## Testler

```
.venv\Scripts\python.exe -X utf8 -m pytest -q
```

Hızlı iç döngü için (13 yavaş test hariç): `.venv\Scripts\python.exe -X utf8 -m pytest -q -m "not slow"`.
Teslimden önce ve CI'da `-m` olmadan tam komut çalışır. Yavaş testleri listelemek için: `-m slow --collect-only -q`.

Testler yalnız yapay fiyat serisi kullanır. İş Yatırım verisi depoya girmez.
