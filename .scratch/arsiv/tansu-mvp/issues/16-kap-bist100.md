# 16: KAP'tan gerçek BIST100 geçmişi (paralel)

**What to build:** 2015'ten bugüne gerçek BIST100 üyelik listesi kurulur. Kaynak, KAP "Dönemsel Endeks
Değişiklikleri" duyurularıdır. Liste dondurulmuş bir dosya olarak depoya konur. Sonra kurallar bu evrende
de koşulur ve ara evrenle (07) karşılaştırılır.

**Blocked by:** 01

**Status:** done

- [x] Kaynak birincil olarak okunur ve kapsamı yazılır. TASARIM 8.2'deki açık soru (2015–2016 kapsanıyor mu)
      cevaplanır.
- [x] Liste tarih bazlıdır. Her değişiklik için kaynak duyuru bağlantısı tutulur. Eksik dönemler açıkça
      işaretlenir.
- [x] Bugünkü listeyle (borsapy) son tarihte birebir eşleşmesi sınanır. (Kısmen: bkz. Comments.)
- [x] 07'nin ara evreniyle örtüşme oranı yıllara göre raporlanır. (Bkz. Comments, "07 ile örtüşme".)
- [x] Bu bilet sınama sonucuna bakmaz. Evren değişirse kural kaydı açısından yeni deneme olur; bu iş 15'ten
      sonra ayrı yapılır.

## Comments

Durum: `done`. Son kutu (07 ile örtüşme) aşağıda kapandı.

**07 ile örtüşme.** A = KAP'tan geriye yürütülen BIST100 üyeliği, B = `evren.evren(anlik, ay)` (tam evren anlık
görüntüsü `veri/ag/20261005-1726`, varsayılan parametreler). Her ayın ilk işlem gününde |A∩B|/|A|; yıl
ortalaması. 2016-07 → 2026-10, 124 ay. Kod kaydedilmedi (tek seferlik `python -c`); getiri/sınama sonucuna
bakılmadı.

| Yıl | Ay | Ort. üye sayısı (A) | Örtüşme |
|---|---|---|---|
| 2016 (Tem–Ara) | 6 | 105,0 | %68,9 |
| 2017 | 12 | 105,8 | %66,1 |
| 2018 | 12 | 104,3 | %63,6 |
| 2019 | 12 | 103,8 | %67,2 |
| 2020 | 12 | 102,0 | %73,7 |
| 2021 | 12 | 102,0 | %72,6 |
| 2022 | 12 | 101,3 | %74,1 |
| 2023 | 12 | 101,0 | %72,4 |
| 2024 | 12 | 101,0 | %73,2 |
| 2025 | 12 | 100,0 | %72,4 |
| 2026 (Oca–Eki) | 10 | 100,0 | %67,2 |

Tüm aylar ortalaması %70,2. Okuma: ara evren (piyasa değerine göre ilk 100, likidite elekli) KAP BIST100'ün
yıllara göre %64–74'ünü kapsar; fark kaynağı ayrıştırılmadı (BIST100 free-float piyasa
değeri ve ad hoc değişiklikler, ara evren ham piyasa değeri kullanır). |A| 2016–2019'da 100'ün üstüne
sapıyor (bkz. Boşluklar), bu yıllar daha az güvenilir. Evren değişirse bu tablo yeniden hesaplanmalıdır.

**Kaynak.** KAP, Borsa İstanbul A.Ş. bildirimleri (`/tr/api/disclosure/members/byCriteria`, 2014–2026
tarandı). Dönemsel duyurular "BIST Pay Endeksleri" konusunda; ek PDF'te BIST 100 için alınacak, çıkarılacak
ve yedek paylar var. Tam üye listesi yok, yalnız değişiklik var.

**Kapsam (2015–2016 sorusu).** Hayır. İlk BIST 100 dönemsel duyurusu 17.06.2016 (KAP 539273), dönem
01.07.2016. 2015 ve 2016 ilk yarı için KAP'ta duyuru yok. 2016-07 → 2026-10 arası 42 ardışık dönem var,
dönemsiz ay yok. TASARIM 8.2 madde 2 ve 5.2 güncellendi.

**Dosyalar.** `docs/arastirma/bist100_kap_degisiklik.csv` (656 değişiklik satırı + 100 taban satırı, her
satırda KAP bağlantısı) ve `bist100_kap_bosluk.csv` (14 satır). Taban: Borsa İstanbul `hisse_endeks_ds.csv`
(borsapy `Index("XU100")`), 05.10.2026. Geçmiş üyelik taban listeden geriye yürütülerek bulunur.
PDF'ler `pdftotext` ile okundu; 4 PDF'in (sütun kayması) alınan/çıkarılan listeleri elle okunup düzeltildi, KAP numaraları: 645948,
725991, 769426 (kod "A.V.O.D" → AVOD), 1409989.

**Bugünkü listeyle sınama.** Son duyuru (21.09.2026, KAP 1666347) 27 giriş ve 27 çıkış içerir; 27 girişin
27'si bugünkü listede, 27 çıkışın hiçbiri yok. Taban 100 hisse. Birebir eşleşme KAP'tan bağımsız kurulamaz,
çünkü KAP tam liste vermez; sınama bu yüzden yalnız tutarlılıktır.

**Boşluklar (dürüst sınır).**
- Dönem içi (ad hoc) değişiklikler okunamadı: 571 "Endeks Şirketlerinde Değişiklik" duyurusundan 531'inin eki
  yok; 40 ekli duyurudan yalnız 2'sinde XU100 geçiyor ve sütunlar ayrıştırılamadı.
- Sonuç: geriye yürütülen üye sayısı 99–106 arasında sapıyor (gerçek hep 100). 11 hissede (BERA, IPEKE, EFORC,
  KONTR, BAGFS, ECZYT, ADANA, GUSGR, DGATE, KLGYO, HURGZ) giriş/çıkış kaydı birbirini tutmuyor; bu
  satırlar `docs/arastirma/bist100_kap_bosluk.csv`'de duyuru tarihinden bugüne "belirsiz" işaretli.
- EFORC → EFOR kod değişimi olabilir (doğrulanmadı).

**Açık işler.** (1) 07 bitince yıl bazında örtüşme oranı. (2) Dönem içi değişiklikler için ikinci kaynak
(Borsa İstanbul arşivi) var mı, bakılmadı. (3) Tutarsızlık sınırı yüzünden 07 ile karşılaştırmada 2016-07
öncesi dışarıda tutulmalı, sonrası "yaklaşık" okunmalı.
