# 01: Sözlük TASARIM ile aynı anlamı taşır

**What to build:** GLOSSARY.md'deki her terim TASARIM ve KURALLAR'daki kullanımla aynı anlamı verir; sayı ve formül taşımaz,
sahip bölüme atıf verir. Eksik temel terimler eklenir.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Dar ya da yanlış tanımlar düzeltildi: evren, işlem fiyatı (AOF), karantina, çift, tutuş dönemi, 50/50 alım günü,
      kilitli gün, bozulma ve BOZULDU, fiili risk, Deneme, Ölçülemedi, yanlış kabul, fazla getiri (`denetim/hiza-a.md`,
      `hiza-b.md`, `hiza-e.md` TERİM satırları).
- [ ] Eksik terimler eklendi: YORUM, anlık görüntü (kimlik, veri sürümü), resmi ve geliştirme koşusu, Adım, Motor,
      özkaynak, maruziyet, risk paketi, ATR, EMA, SMA, Z, ΔZ, eşbütünleşme, K3.
- [ ] Sözlükteki sayılar ve formüller (100 hisse, K1 p, %60, %0,3, %5, 2 ATR) kaldırıldı; yerine TASARIM bölüm atfı var.
- [ ] Sözlük Tansu kaynaklarına göre gözden geçirildi (Matt: gözden geçirilmemiş sözlük hiç olmamasından kötüdür). Gözden geçirmeyi Claude ve bağımsız denetçi yapar, Levent yapmaz (Levent 10.10): Tansu'dan gelen her terim (ATR, EMA sıkışması, Z, ΔZ, kart durumları, risk paketi vb.) `docs/kurallar/A–E` ve beyindeki Tansu havuzundaki kullanımla karşılaştırıldı. Sözlük kaynak iddiası taşımaz ("Tansu'nun", "YORUM'dur" yok); Tansu'dan ayrılan yerler bilet 02'nin listesindedir.
- [ ] `hiza-b-istem.md` sözlük kapsamında yeniden koştu; TERİM ve TEKRAR bulgusu yok.
