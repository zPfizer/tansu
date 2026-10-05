# 05: Sadakat kontrolü: EMA sıkışması (KRDMD) ve `sadakat` komutu

**What to build:** `python -m tansu sadakat` komutu Tansu'nun KRDMD ekranındaki rakamları ham seriden
yeniden üretir ve sonucu `docs/sadakat.md`'ye yazar. Bu dilimde iki şey kurulur:
- `gostergeler` modülünün ilk hali: EMA `ewm(adjust=False)`, sıkışma oranı = (en büyük EMA − en küçük EMA)
  / EMA200.
- EMA sıkışması ailesinin sıkışma dönemi tanımı.

Getiriye bakılmaz.

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] Komut KRDMD için şu rakamları basar ve `docs/sadakat.md`'ye yazar. Tolerans önceden yazılıdır:
      Tansu'nun gösterdiği son hanenin yarısı.
  - Sıkışma dönemi 17.12.2025–14.01.2026, 20 gün.
  - Dönem ortalaması %0,64.
  - 09.04.2026 EMA'ları: 31,92 / 30,74 / 29,58 / 28,43.
- [ ] Sıkışma dönemi: oranın ≤ %1,2 olduğu art arda en az 3 gün. Eşiği aşan ilk gün dönemi bitirir.
- [ ] Göstergeler için elle hesaplı küçük birim testleri yazılır (EMA ve oran; 5–10 satır veri).
- [ ] Komut tekrar koşulduğunda aynı rakamları verir. Bu bir test olarak yazılır ve sahte anlık görüntüyle
      ağsız koşar.
- [ ] Deneme günlüğüne `tur=sadakat` satırı yazılır. Bu satır Holm'a girmez.
