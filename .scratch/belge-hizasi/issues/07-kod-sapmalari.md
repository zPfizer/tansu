# 07: Kodun TASARIM'dan saptığı yerler karara bağlanır

**What to build:** Kodun TASARIM'dan farklı davrandığı on yer tek tek incelenir. Her biri için ya kod TASARIM'a uyar ya da
TASARIM gerekçesiyle güncellenir.

**Blocked by:** 03

**Status:** ready-for-agent

- [ ] `denetim/tasarim-kod.md` §3'ün her maddesi `/diagnosing-bugs` ile ele alındı: davranışı gösteren test, sonra karar.
- [ ] Öncelik: `gunluk.py` yalnız AKTİF kartları indirir (STOP/BOZULDU açık pozisyon izlenmeyebilir).
- [ ] Kod değişikliği gerektiren her madde kendi PR'ıyla kapandı; belge değişikliği TASARIM'da karar etiketiyle.
- [ ] Bilet 06'da bulunanlar (10.10): `motor.sinama` tek satırlı üyelik tablosunda düşer (`groupby(...).agg(pd.DatetimeIndex)` tek günde Timestamp döndürür, `isin` TypeError); `rapor.py` aynı koşu kimliğinde HTML ve CSV'yi üstüne yazar (TASARIM §6.8 "üstüne yazılmaz").
- [ ] Bilet 02'den (10.10, `denetim/tansu-sapma-dogrulama.md` #6, #19): kart etiketi `BOZULDU` Tansu'nun "bozulma"sı (formasyonun geçersizleşmesi) değildir. SMA250 çıkışı, karantina çıkışı ve giriş iptali tek etikette toplanıyor; ayrı etiket (ör. `GÜN SONU STOPU`, `KARANTİNA ÇIKIŞI`, `GİRİŞ İPTAL`) ve `Durum` sütununun `Pozisyon durumu` olması karara bağlanır. Etiket CSV çıktısını değiştirir: önce test.
