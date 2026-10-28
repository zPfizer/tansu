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

## 2. Artımlı günlük güncelleme (PR 206)

- `kaynak.Artimli`: sembol başına son kaynak yanıtı `veri/onbellek/fiyat-20190101/`; kaynaktan son 10 işlem günü istenir. Örtüşen günler değişmişse (bölünme, temettü) ya da kısa yanıt boşsa sembol tam iner; tam inen fiyat olaylardan sonra yazılır; dosyalar geçici dosyadan yerine konur.
- Bağımsız inceleme üç hata buldu, üçü de önce kırmızı testle düzeltildi: bütünüyle boş alan ya da boş yanıtta çökme, olay isteği düşünce eski olayların kalması, yarım dosya.
- Önbellek ilk kez Gartley ölçümünün aynı kaynaktan aynı kodla yaptığı indirmeyle (28.10.2026 17:23, 836 sembol) dolduruldu; ilk tam iniş ≈ 2 sa 15 dk sürmüştü.

İlk artımlı günlük koşu (28.10.2026 23:53, `python -X utf8 -m tansu veri --kok veri`):

```
anlık görüntü 20261028-2353; silinen eski görüntü: 0; önbellek: 655 artımlı, 181 tam
cikis 0; sure 4338 sn
sembol durumu: tamam 627, son gün eksik 28 (kapanan paylar), inmedi 3 (CITAS, LRSHO, LYDHO), kaynak boş 181
```

- Süre 72 dk 18 sn; tam iniş ≈ 2 sa 15 dk. Geçmişi değişip yeniden tam inen pay yok; 181 "tam" iniş kaynakta boş kodlardır (önbellekleri boş).
- Darboğaz kaynağın yanıt süresidir, kod değil. Ölçüm (29.10.2026 01:00-01:15): aynı kısa aralık isteği bir an 0.0 sn, bir an 10.3 sn yanıt verir (HTTP 200, yeniden deneme yok). 80 istekte 32'si yavaş, 398 sn. İstek arası bekleme 2 sn olunca 80 istekte 16'sı yavaş, 327 sn. Aynı semboller 10 dk sonra yine 2-11 sn: yavaşlık sembole bağlı önbellek değil, kaynağın o anki yüküdür. Bekleme 1 sn kaldı (kaynağa saygı; kazanç küçük ve değişken).
- Kaynakta boş 181 kod her koşuda iki istek yer (fiyat ve olay): koşunun ≈ 1.018 isteğinin 362'si (%36). Süre payı ölçülmedi.

## 3. Veri yolu hataları ve kalite (PR 207)

Kararlar: `kanit/acik-sorular.md` "Verilen kararlar" (Levent 29.10.2026, yaygın backtest uygulaması).

- Kopan bağlantı (`ChunkedEncodingError`) yeniden denenir.
- Bozuk gün eksik gün sayılır: hesap fiyatı NaN, dolum yok, karantina kuralı değişmez. Bu düzeltme olmadan bütün BIST'te koşu çöker:

```
(PR 205-206 kodu) python -X utf8 -m tansu ayarla ortalama-kesisim   # görüntü 20261028-1723
  File "tansu\islem.py", line 266, in sonuc
ZeroDivisionError: division by zero        (AOF 0'dan piyasa dolumu)
```

- ATR fiyatlı 14 çubuğun ortalamasıdır; ATR'si yine tanımsız günde stoplu kurulum girmez ("ATR tanımsız").

Kalite sayıları (görüntü 20261028-1723, yeni kod):

| Ölçü | Değer |
|---|---|
| Bozuk gün, 2019-2025 (kaynak günü hariç) | 8.312 gün, 288 sembol |
| Kaynak günü hatası | 21.05.2026 (bütün semboller eksik gün) |
| 2021-2025 sembol-günü / karantina yüzünden sinyal kapalı (250 gün kuralı, SPEC 3.9) | 636.579 / 56.487 (%8,9) |
| Fiyatlı günde ATR yok: eski / yeni | 29.478 (%3,6) / 8.031 (%1,0; listelenmenin ilk 13 çubuğu) |

## 4. `tansu ayarla` yeniden (2021-2025)

Eski: BIST 30, PR 205 öncesi kod. Yeni: bütün BIST, `yeniden-kurulus` 96b5107 (PR 205-207 ve Gartley PR 204), görüntü 20261028-1723. Saklı dönem (2026) ayara girmez; burada yazılmadı.

Denetim: eski kod 20261028-1723 görüntüsünde `ortalama-kesisim` için kayıtlı eski sayıları birebir verir (78 dolum, EMA 50/200, örneklem dışı N 130, yüzdelik 18.1). Fark veri tarihinden değil, evrenden ve düzeltmelerden gelir. Bütün BIST'te düzeltmesiz "önce" sayısı yoktur: eski motor çöker (bölüm 3). Ana oturumun aynı kod ve görüntüyle `gartley` koşusu aynı sayıları verdi.

`gartley` (sınıf a, R):

| | Eski (BIST 30, görüntü 20261026-2108) | Yeni (bütün BIST) |
|---|---|---|
| Sinyal / dolum | 17 / 3 | 235 / 35 |
| Toplam / beklenti | 2.55 R / n/a (N = 3) | 27.83 R / 0.80 R, kazanma %60 |
| Seçim | puanlı nokta yok, varsayılanlar | sag_bar_10, tolerans 0.04, geçerlilik 5, stop X |
| Örneklem dışı | N 2, 0.75 R | N 34, 30.12 R (ortalama 0.89 R), verim 1.49 (5/6 adım) |
| Rastgele giriş yüzdeliği | n/a | 99.4 |
| Bootstrap toplam p5 | n/a | 16.29 R |
| Üç onay bayrağı | örnek az | üçü de geçer |
| Uyarı | — | kazanma payı %40-60 dışında (%65) |
| Durum | yetersiz-ornek | ayarlandi |

`ortalama-kesisim` (sınıf b, net %, nominal TL):

| | Eski (BIST 30) | Yeni (bütün BIST) |
|---|---|---|
| Sinyal / dolum | 78 / 78 | 1155 / 1081 |
| Beklenti / kazanma | %164.18 / %41 | %130.67 / %47 |
| Seçim | EMA 50/200, teyit 0 | EMA 48/247, teyit 2 |
| Örneklem dışı | N 130, ortalama %5.96, verim 0.70 | N 1672, ortalama %45.10, verim 2.69 |
| Rastgele giriş: koşu ortalaması p50 / yüzdelik | %8.60 / 18.1 | %39.93 / 82.8 |
| Bootstrap toplam p5 | %81.87 | %62098.06 |
| Üç onay bayrağı | 2 geçer (rastgele giriş geçmez) | 2 geçer (rastgele giriş geçmez) |
| Durum | ayarlandi | ayarlandi |

Okuma: `gartley` bütün BIST'te 30 işlem eşiğini geçer ve üç bayrağı da geçer. `ortalama-kesisim` karşılaştırma tabanıdır; yüksek yüzdeler 2021-2025 nominal TL yükselişidir, rastgele girişler de benzer kazanır (yüzdelik 82.8 < 95).

```
python -X utf8 -m tansu ayarla ortalama-kesisim --kok <görüntü 20261028-1723>
ortalama-kesisim: 1155 sinyal, 1081 dolum, toplam 141259.37 %
ortalama-kesisim: ızgara 54 nokta, puanlı 54; seçim ortalama=EMA cift=48/247 teyit_gun=2 (sağlam 76.63 %, N = 829)
ileri yürüme: örneklem dışı N = 1672, ortalama verim 2.69 (6/6 adım)
Monte Carlo: tohum 20261028, N = 1672, rastgele giriş yüzdeliği 82.8
süre 307 sn

python -X utf8 -m tansu ayarla gartley --kok <görüntü 20261028-1723>
gartley: 235 sinyal, 35 dolum, toplam 27.83 R
gartley: ızgara 36 nokta, puanlı 15; seçim pivot=sag_bar_10 tolerans=0.04 gecerlilik=5 stop=X (sağlam 0.84 R, N = 34)
ileri yürüme: örneklem dışı N = 34, ortalama verim 1.49 (5/6 adım)
Monte Carlo: tohum 20261028, N = 34, rastgele giriş yüzdeliği 99.4
süre 65 sn
```
