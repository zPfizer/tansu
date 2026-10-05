# İzleme 06: EMA sıkışması (cevaplar-06-sikisma.md, taslak 6'ya karşı)

06-003 — EKSİK — RED — Formül çözüldü (KURALLAR 4, sonuc O9); aday listesi için kurulum gereksiz.
06-007 — EKSİK — VAR — KURALLAR 3 "art arda en az 3 gün"; sonuc B-11; eski prototipin silinmesi TASARIM 7.1.
06-009 — EKSİK — VAR — KURALLAR 3 "oranın eşiği aştığı ilk gün dönemi bitirir"; sonuc B-11.
06-010 — EKSİK — VAR — TASARIM 5.3 (pozisyon açıkken yeni sinyal sayılmaz) ve KURALLAR 3 "dönem başına tek giriş"; sayım birimi işlemdir (5.9).
06-012 — EKSİK — VAR — TASARIM 5.1 (2010'dan indirme, ilk sinyal 30.11.2015); sonuc B-6 "ısınma ≥ 500 gün".
06-020 — EKSİK — VAR — KURALLAR 4 sonuçlar: dönem ortalaması %0,638, grafik sonu ve Mart tepesi görselle ±0,3 içinde.
06-025 — EKSİK — VAR — KURALLAR 3 EMA sıkışması notu: Pre Signal sıkışma sürerken, bizim tetik bitişten sonra (YORUM).
06-027 — EKSİK — VAR — KURALLAR 3 giriş: "dönemdeki en yüksek gün yükseği" (YORUM); sonuc B-11.
06-029 — EKSİK — RED — Aşırı kurulum; "dönem sürerken sinyal yok" tanımdan zaten çıkar (KURALLAR 3), sıklık raporu ek iş.
06-032 — EKSİK — VAR — KURALLAR 3 "Dönem başına tek giriş"; sonuc B-11.
06-045 — EKSİK — RED — Aşırı kurulum; ertesi AOF kayması %0,1/0,3/0,5 masraf duyarlılığına dahil (TASARIM 5.4).
06-056 — EKSİK — VAR — TASARIM 5.6 "%10 tavan ... rapor bağladığı işlem oranını ve gerçekleşen riski yazar"; sonuc B-12.
06-059 — YANLIŞ — VAR — "520 dönem" sayımı KURALLAR'dan silindi (KURALLAR 3'te yok); sonuc B-11 "520 dönem sayımı silinir"; Yahoo yasağı TASARIM 4.
06-062 — EKSİK — VAR — TASARIM 5.12 kabul kararını yalnız altı koşula bağlar; ayrı bir sıklık kontrolü tasarımda yoktur.
06-064 — EKSİK — RED — Aşırı kurulum; ısınma kuralı (sonuc B-6) her seriye uygulanır, sembol devri BIST100'de nadir.
06-067 — EKSİK — VAR — TASARIM 5.7 K1 "sıkışmasız aynı kırılım" kolu; KURALLAR 3 K1 ön şartı; sonuc B-11.
06-068 — EKSİK — TEKRAR — 06-067.
06-072 — EKSİK — YENİ — TASARIM 5.10'a ızgara değerlerini yaz: eşik {1,0; 1,2; 1,5}, en az gün {2; 3; 5}, giriş penceresi {5; 10; 20} (YORUM).
06-073 — EKSİK — VAR — KURALLAR 3 "Tansu'nun %1,2 ve 3 günü 'örnekteki değer'dir"; ızgara TASARIM 5.10.
06-081 — EKSİK — TEKRAR — 06-027.
06-085 — EKSİK — RED — Kapsam dışı; S2-37 sorgu-2 kayıt belgesidir, tasarım değil (KURALLAR 3'te hacim koşulu zaten yok).
06-087 — EKSİK — RED — Aşırı kurulum; karantina oranı 5.13'te ölçülür, ısınma 2015 öncesinde biter (B-6).
06-094 — YANLIŞ — RED — Kapsam dışı; ICBCT ilk sürümde kullanılmaz, "B-momentum 2" kurallar/B kaynak notudur, tasarım belgesi değil.
06-098 — EKSİK — VAR — TASARIM 3 (BIST'te bireysel açığa satış pratik değil) ve KURALLAR 3 (bireysel yatırımcı açığa satamaz); yalnız alış TASARIM 3 "Var".

## Özet

Etiket sayıları (grep ile sayıldı):
- VAR: 14
- TEKRAR: 2
- YENİ: 1
- RED: 7

YENİ maddeler:
- 06-072: TASARIM 5.10'a ızgara değerlerini yaz: eşik {1,0; 1,2; 1,5}, en az gün {2; 3; 5}, giriş penceresi {5; 10; 20} (YORUM).

YANLIŞ olup VAR olmayan maddeler:
- 06-094: RED. Değişiklik yok; ICBCT kapsam dışıdır ve düzeltilecek metin tasarım belgelerinde değildir.
