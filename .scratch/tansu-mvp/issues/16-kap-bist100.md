# 16: KAP'tan gerçek BIST100 geçmişi (paralel)

**What to build:** 2015'ten bugüne gerçek BIST100 üyelik listesi kurulur. Kaynak, KAP "Dönemsel Endeks
Değişiklikleri" duyurularıdır. Liste dondurulmuş bir dosya olarak depoya konur. Sonra kurallar bu evrende
de koşulur ve ara evrenle (07) karşılaştırılır.

**Blocked by:** 01

**Status:** ready-for-agent

- [x] Kaynak birincil olarak okunur ve kapsamı yazılır. TASARIM 8.2'deki açık soru (2015–2016 kapsanıyor mu)
      cevaplanır.
- [x] Liste tarih bazlıdır. Her değişiklik için kaynak duyuru bağlantısı tutulur. Eksik dönemler açıkça
      işaretlenir.
- [x] Bugünkü listeyle (borsapy) son tarihte birebir eşleşmesi sınanır. (Kısmen: bkz. Comments.)
- [ ] 07'nin ara evreniyle örtüşme oranı yıllara göre raporlanır. (07 bekleniyor)
- [x] Bu bilet sınama sonucuna bakmaz. Evren değişirse kural kaydı açısından yeni deneme olur; bu iş 15'ten
      sonra ayrı yapılır.

## Comments

Durum: `ready-for-agent` kalır; yalnız "07 ile örtüşme" kutusu açık (07 bekleniyor).

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
  satırlar `bosluk.csv`'de duyuru tarihinden bugüne "belirsiz" işaretli.
- EFORC → EFOR kod değişimi olabilir (doğrulanmadı).

**Açık işler.** (1) 07 bitince yıl bazında örtüşme oranı. (2) Dönem içi değişiklikler için ikinci kaynak
(Borsa İstanbul arşivi) var mı, bakılmadı. (3) Tutarsızlık sınırı yüzünden 07 ile karşılaştırmada 2016-07
öncesi dışarıda tutulmalı, sonrası "yaklaşık" okunmalı.
