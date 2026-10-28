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

## 4b: ayar, ileri yürüme, saklı dönem

Dal: `faz-4b-ayar`.

### Yapılanlar

- `tansu/ayar.py`: ızgara (`aralik` eksenlerinin çarpımı, listelenen sırayla), puan (kapalı-içeride kurulumların ortalaması; 30'un altında puan yok), sağlam puan (tek eksende ±1 komşu; kendisi ve puanlı komşuların medyanı; ikiden az puanlı komşu: ızgaranın en düşük puanı), altı çapalı pencere (eğitim 04.01.2021'den, test 2023H1-2025H2), verim, son ayar (04.01.2021-31.12.2025), parametre dosyası (`stratejiler/ayarlar/<ad>.json`, sınırda doğrulama, `suzgecler` ve `liste_cikisi` korunur). Izgara noktaları en çok 16 süreçte.
- `tansu/sinama.py`: `Gunler` (komut başına bir kez), `Donem` (fiyat dönem sonunda sinyalden önce kesilir), `Kosu.kes` (sinyal tarihine göre dilim). Yıl tabloları, ayar ve ileri yürüme 31.12.2025 sonrasındaki fiyatı görmez; o gün açık kurulum `acik`. Saklı dönem: 01.01.2026'dan verinin son tam ayının sonuna, tek kesintisiz koşu (veri ayın son iş gününe ulaştıysa ay tamdır).
- `tansu sina` ve `tansu ayarla` tek akış: ikisi de ızgarayı ve ileri yürümeyi bellekte hesaplar; yalnız `ayarla` json yazar ve durumu `ayarlandi` ya da `yetersiz-ornek` yapar. Rapor: ızgara sonucu, ileri yürüme tablosu, dikişli örneklem dışı, saklı dönem, dönem başına ileri getiri (sınıf b), açıklama satırı (SPEC 5.6), denenen parametre seti ve sınanan strateji sayısı.
- PR 196 Codex bulgusu 1 (2026 verisinin 2021-2025 sınamasına girmesi) bu fazda kapandı: fiyat 31.12.2025'te kesilir.

### Komutlar ve çıktı

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q
203 passed, 1 skipped in 14.75s   (atlanan: altın test; bu çalışma kopyasında yerel veri yok)
$ .venv\Scripts\python.exe -m ruff check tansu tests
All checks passed!

$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla ortalama-kesisim     (12 s)
ortalama-kesisim: 78 sinyal, 78 dolum, toplam 12806.24 %
ortalama-kesisim: ızgara 54 nokta, puanlı 54; seçim ortalama=EMA cift=50/200 teyit_gun=0 (sağlam 134.72 %, N = 58)
ileri yürüme: örneklem dışı N = 130, ortalama verim 0.70 (6/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 10
ayar: stratejiler\ayarlar\ortalama-kesisim.json
rapor: rapor\ortalama-kesisim\sinama.html; durum: ayarlandi

$ .venv\Scripts\python.exe -X utf8 -m tansu ayarla gartley     (18 s)
gartley: 63 sinyal, 36 dolum, toplam 1.18 R
gartley: ızgara 108 nokta, puanlı 54; seçim pivot=zigzag_1.5 tolerans=0.03 gecerlilik=5 stop=X-2ATR (sağlam -0.02 R, N = 36)
ileri yürüme: örneklem dışı N = 38, ortalama verim -8.23 (4/6 adım)
saklı dönem 01.01.2026-30.09.2026: N = 4
ayar: stratejiler\ayarlar\gartley.json
rapor: rapor\gartley\sinama.html; durum: ayarlandi
```

Veri görüntüsü 20261026-2108; json `kod_surumu` 84df495 (temiz). `tansu sina` ikisinde de aynı sayıları verdi ve json yazmadı.

### Sonuçların okunuşu

- `ortalama-kesisim`: son ayar Tansu'nun varsayılanını (EMA 50/200) seçti. Örneklem dışı 130 kurulum: beklenti %5,96, medyan −%5,34, kazanma %38, kâr faktörü 1,80. Ortalama verim 0,70; ilk adım (2023H1, 4,01) ortalamayı taşıyor, son dört adımın üçü negatif. Saklı dönem 10 kurulum, toplam +%43,94 (N < 30, oranlar n/a).
- `gartley`: ızgara tek pivot ekseniyle 108 noktadır (sağ bar 10/15/20, zigzag %1,5/2/2,5); eski 324 noktalı ızgarada etkisiz eksenler aynı noktaları çoğaltıp sağlam puanı yapay artırıyordu (bağımsız inceleme bulgusu). Varsayılan nokta (sağ bar 15) kapalı-içeride yalnız 3 kurulum verdiği için puan almadı. Zigzag noktaları daha çok kurulum verir; seçilen nokta 36 kurulumla +0,03 R beklenti, sağlam puan −0,02 R. Seçim stopu X − 2 ATR yaptı; bu bir seviye parametresidir, rapor Tansu'nun değeri X'i yanında gösterir ve ayarlı değeri `varsayım` diye işaretler. Örneklem dışı 38 kurulum, toplam +2,74 R, beklenti +0,07 R, kâr faktörü 1,24. Ortalama verim −8,23: eğitim toplamı küçük (yılda 0,03-0,43 R) ve test toplamı negatif olan adımlarda oran büyür; 2023H1 ve 2023H2'de eğitim toplamı negatif olduğu için verim n/a. Bu, kayda değer bir avantaj olmadığını gösterir.
- Yıl tabloları artık ayarlı parametrelerle ve 31.12.2025 kesimiyle hesaplanır; bu yüzden faz 3'teki 17 sinyal / +2,55 R (varsayılan, kesimsiz) ile aynı değildir.

### İnceleme

- Bağımsız kod incelemesi (ayrı ajan, salt okuma): çekirdekte hata yok (komşular, sağlam puan, kapalı-içeride kuralı, dilimler, verim aritmetiği, 31.12.2025 kesimi, saklı dönem, parametre dosyası, süreç havuzu elle ve kodla doğrulandı). Dört küçük hata düzeltildi: beklemedeki strateji "sınanan" sayılıyordu; `ayarla` json'u rapordan önce yazıyordu (yarıda kalan koşu onaysız parametre bırakabilirdi); bozuk json ızgaradan sonra yakalanıyordu ve nesne olmayan json `AttributeError` veriyordu; veri 2026'ya ulaşmazsa CLI ve özet yanlış tarih aralığı yazıyordu. Not: Gartley ızgarasındaki etkisiz eksenler; pivot tek eksen yapıldı.
- Yorum temizliği (Comment Sicko): 15 gereksiz yorum silindi.
- Açık not: 2026 zehirleme testi sentetik veride sabit ATR kullanır; ATR nedensel (kayan ortalama), sızıntı yolu yok.
