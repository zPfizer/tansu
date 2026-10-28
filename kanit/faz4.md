# Faz 4: ayar, ileri yürüme, saklı dönem

Tarih: 28.10.2026. Dal: `yeniden-kurulus`. Faz iki PR'dır: 4a (`ortalama-kesisim` ve motorun `piyasa` girişi, stopsuz sınıf b ölçümü, kapanışa bağlı çıkış sinyali), 4b (ayar, ileri yürüme, saklı dönem).

## 4a: ortalama-kesisim ve motor eklemeleri

Dal: `faz-4a-ortalama-kesisim`.

### Yapılanlar

- `tansu/islem.py`: `piyasa` girişi (sinyalden sonraki ilk fiyatlı günün AOF'si; o gün tavan kilitliyse sinyal düşer, sayaç "üst limit kilidi"); NaN stop yasal (sınıf b: sinyal anı stop denetimi yok, stop çıkışı yok, R NaN); kapanışa bağlı çıkış tek yardımcıda (önce kapanış stopu, sonra `cikis_sinyali`), taban kilidinde ilk kilitsiz güne kalır, dolum gününde de kurulur (SPEC 4, 5.1, 5.2, 5.4).
- `tansu/gostergeler.py`: `wma` (ağırlık 1..n, en yeni en ağır).
- `tansu/stratejiler/ortalama_kesisim.py`: SPEC 11 madde 15; ortalama {EMA, SMA, WMA} × çift (SPEC sırası) × `teyit_gun` {0, 2} = 54 nokta. EMA 2,5 × dönem geçerli kapanıştan sonra geçerli (SPEC 3.4); kesişim için iki ortalama o gün ve önceki gün geçerli olmalı (ısınma sonunda sahte kesişim yok). Çıkış: karşı kesişim, `cikis_sinyali` sütunuyla.
- `tansu/sinama.py`, `tansu/rapor.py`: tek ölçü fonksiyonu, birim `strateji.olcu` sütunundan (R ya da net %); sınıf b ileri getiri tablosu (1, 3, 5, 10 gün; MFE ve MAE medyanı).
- Kural kartı `stratejiler/ortalama-kesisim.md` yerelde (Ek B #12): 14 beyin notunun `Ham` ve `Görsel metni` kısmından.

### Komutlar ve çıktı

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q
177 passed in 5.34s
$ .venv\Scripts\python.exe -m ruff check tansu tests
All checks passed!
$ .venv\Scripts\python.exe -m ruff format --check tansu tests
34 files already formatted

$ .venv\Scripts\python.exe -X utf8 -m tansu sina gartley
gartley: 17 sinyal, 3 dolum, toplam 2.55 R
rapor: rapor\gartley\sinama.html; durum: sinandi

$ .venv\Scripts\python.exe -X utf8 -m tansu sina ortalama-kesisim
ortalama-kesisim: 78 sinyal, 78 dolum, toplam 14144.11 %
rapor: rapor\ortalama-kesisim\sinama.html; durum: sinandi
```

Gartley sonucu faz 3 ile aynı (17 sinyal, 3 dolum, +2,55 R).

`ortalama-kesisim` (EMA 50/200, varsayılan, ayarsız; veri görüntüsü 20261026-2108):

| Sinyal yılı | Kurulum | Ortalama net % | Medyan net % | Toplam net % |
|---|---|---|---|---|
| 2021 | 26 | 499.4 | 98.2 | 12983.5 |
| 2022 | 5 | 195.2 | 185.0 | 975.8 |
| 2023 | 3 | 12.3 | 16.3 | 37.0 |
| 2024 | 11 | 2.8 | -10.4 | 30.3 |
| 2025 | 33 | 3.6 | -8.9 | 117.5 |

Sayının nedeni: 73 kurulum karşı kesişimle, 5'i açık kapandı; medyan tutma 132 gün, en uzun 1250 gün. 2021'de açılan uzun trend işlemleri TL bazında çok yükseldi (en büyük: ASELS 28.10.2021 dolum 8.09, çıkış 335.00, +%4036, 1250 gün). Yüzdelerin toplamı bir portföy getirisi değildir; her kurulum kendi başına ölçülür. Bu koşuda veri 2026'ya kadar gider; 4b fiyatı 31.12.2025'te keser.

### İnceleme

- İki bağımsız tasarım adayı (ayrı ajanlar) ve bir hakem aynı yapıyı seçti; hakem iki düzeltme verdi, ikisi uygulandı: ısınma bitince sahte kesişim yok; çift ekseni SPEC sırasıyla.
- Bağımsız kod incelemesi (ayrı ajan, salt okuma) 1 gizli hata buldu: fiyatsız bir satır kesişimi bölüyordu (kaçan çıkış sinyali işlemi açık bırakır). Düzeltme: ortalama ve kesişim hissenin fiyatlı günlerinde hesaplanır. Test `test_fiyatsiz_satir_kesisimi_bolmez` eski kodda kırmızı, yeni kodda yeşil. Gerçek veride etkisi yok (aynı 78 kurulum, aynı toplam).
- İncelemenin üç notu: (1) 2021-2025 tablosu 2026 fiyatıyla kapanan kurulumları içeriyor (78 kurulumun 20'si 2026'da çıkıyor); 4b fiyatı 31.12.2025'te keser. (2) İleri getiri tablosu yıl başına da gerekir (SPEC 5.6); 4b. (3) `piyasa` alışı ilk fiyatlı günü bekler; kural kartına varsayım olarak yazıldı.

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q
178 passed in 5.20s
```

### Atlanan

- Ayar, ileri yürüme, saklı dönem: 4b.
- İleri getiri tablosu şimdilik tüm kurulumlar için tek tablo; dönem başına tablo 4b'de.
