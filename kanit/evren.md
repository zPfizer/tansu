# Evren: bütün BIST

Karar: Levent 28.10.2026, "Zaten tüm stratejilerimizi bütün bir evreninde deneyeceğiz." Kayıt: `kanit/acik-sorular.md` "Verilen kararlar".

## 1. Evren tanımı

- `tansu veri` sembol listesi: bugünkü KAP şirket listesi (`kaynak.sirket_kodlari`) ve 01.01.2019'dan beri işlemi kapanan kodlar (`kaynak.kapanan_kodlar`). Kapanan kod listesi görüntüye `kapanan.csv` olarak yazılır.
- `veri.gunluk` `uye`: sembol ilk ve son satırı arasındaki her gün evrendedir. BIST 30 tablosu (`veri.uyelik_araliklari`) adlı katman olarak kalır.
- `sinama.gunler`: görüntüdeki bütün semboller.
- Düşen sinyal nedeni "BIST 30 üyesi değil" → "evren dışı"; rapor dönem satırı evreni yazar.
- Testler: BIST 30 dışı pay evrende; 2019'dan sonra kapanan pay indirilir, daha önce kapanan indirilmez; `kapanan.csv` görüntüde.

```
python -X utf8 -m pytest -q
227 passed, 1 skipped in 20.60s
ruff check . / ruff format --check .: temiz
```

Gerçek veri denetimi (Gartley ölçümünün bütün BIST görüntüsü 20261028-1723, yalnız okuma):

```
sinama.gunler(veri.oku("20261028-1723", ...))
sembol 655, uye gun 964156, kapanan ornek ['ADANA', 'DENIZ', 'SODA', 'TRKCM', 'HALKS'], SOKE True, sure 14.7 sn
```

Liste: 805 bugünkü kod ve 2019'dan beri kapanan 34 kod, toplam 839. 655 kodda fiyat var (kapananların 27'si dahil); 181 kod kaynakta boş (işlem görmeyen şirketler), 3 kod inmedi.
