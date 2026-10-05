# 16: KAP'tan gerçek BIST100 geçmişi (paralel)

**What to build:** 2015'ten bugüne gerçek BIST100 üyelik listesi kurulur. Kaynak, KAP "Dönemsel Endeks
Değişiklikleri" duyurularıdır. Liste dondurulmuş bir dosya olarak depoya konur. Sonra kurallar bu evrende
de koşulur ve ara evrenle (07) karşılaştırılır.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Kaynak birincil olarak okunur ve kapsamı yazılır. TASARIM 8.2'deki açık soru (2015–2016 kapsanıyor mu)
      cevaplanır.
- [ ] Liste tarih bazlıdır. Her değişiklik için kaynak duyuru bağlantısı tutulur. Eksik dönemler açıkça
      işaretlenir.
- [ ] Bugünkü listeyle (borsapy) son tarihte birebir eşleşmesi sınanır.
- [ ] 07'nin ara evreniyle örtüşme oranı yıllara göre raporlanır.
- [ ] Bu bilet sınama sonucuna bakmaz. Evren değişirse kural kaydı açısından yeni deneme olur; bu iş 15'ten
      sonra ayrı yapılır.
