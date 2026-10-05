# 11: Çift rotasyonu bölmesi

**What to build:** `sinama` çift rotasyonu ailesini de koşar. Bölme şöyle çalışır:
- Her yıl önceden yazılmış kuralla en fazla 5 çift seçilir.
- Her çift payı Z ±2 ve ΔZ dönüşüyle iki hisse arasında geçiş yapar.
- Raporda kendi sermaye eğrisi, K2 ve tanısal 50/50 tutma karşılaştırması yer alır.
- VAKBN–GARAN sabit çift olarak ayrıca gösterilir.

**Blocked by:** 06, 10

**Status:** ready-for-agent

- [ ] Yıllık seçim:
  - Seçim yılın ilk işlem günü kapanışında, o günkü evrenle yapılır.
  - Aynı sektör şartı aranır; hissenin 252 gün verisi olmalıdır; eşbütünleşme p < 0,05 olmalıdır.
  - Sıralama açgözlüdür: bir hisse yalnız bir çiftte olur, bir sektörden en fazla 2 çift seçilir, β ≤ 0
    olan çift elenir.
  - X/Y rolü sembol sırasından belirlenir. Sektörü olmayan hisse aday olmaz.
- [ ] Geçişler:
  - Geçiş ertesi gün AOF'tan yapılır. Bacak kilitliyse geçiş olmaz ve sinyal taşınmaz.
  - Bacak karantinadaysa çift girişsiz kalır.
  - Çiftin hissesi kapanırsa pay nakde geçer.
  - Yıl geçişinde düşen çift kapanır; yine seçilen çift işlemsiz sürer.
  - Hiç çift seçilmeyen yıl "işlem yok" diye işaretlenir.
- [ ] Paylar yıl başında eşittir, yıl içinde dengelenmez. Burada "işlem" geçişten geçişe tutuş demektir.
- [ ] 50/50 tanısal: yılın ilk günü bir kez alınır, yıl boyunca tutulur.
- [ ] Testler `kosu()` yüzünden, sentetik iki hisseli anlık görüntüyle:
  - seçim kuralları
  - geçiş günleri
  - kilitte geçiş olmaması
  - yıl geçişi
  - kapanma
