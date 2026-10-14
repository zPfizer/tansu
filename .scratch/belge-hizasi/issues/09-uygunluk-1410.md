# 09: Belgeler bugünkü kodu ve durumu anlatır (uygunluk denetimi 14.10)

**What to build:** Bir ajan TASARIM, AGENTS ve KURALLAR'ı açtığında, uygulama sırasının hangi adımlarının bittiğini,
komut girişinin hangi komutları tanıdığını, iki zamanlanmış görevin durumunu ve havuz sayısını bugünkü haliyle okur.
Her olgu tek sahibinde durur; öteki yerler atıf verir. Kaynak: YONETIM uygunluk denetimi (14.10), Tansu oturumunda
doğrulanan bulgular 1–5 (bulgu 6–8 düştü).

**Blocked by:** None (can start immediately)

**Status:** done (pr/09-uygunluk-1410)

- [x] Uygulama sırası (TASARIM §7): adım 2–9 bitmiş MVP biletine atıfla "tamamlandı"; adım 9 ilk resmi koşunun sonucunu
      (iki aile Deneme, kâğıt üstü dönem başlamadı, iki görev etkin) doğru anlatır; adım 10 bilet 16 sonucuna atıf.
- [x] Modül tablosu (TASARIM §4): komut girişi satırı koddaki yedi komutu sayar; sadakat modülünün satırı var; bölüm→kod
      tablosu yalnız koddaki atıflardan türer (§3 ve sadakat satırları atıfla desteklenir).
- [x] Aylık taban yenilemesi (TASARIM §6) "elle" değil, aylık görevle yapılır.
- [x] Havuz sayısı tek sahipte (KURALLAR başlığı, 14.10 sayımı: 258 not, 228 görsel); TASARIM §2 ona atıf verir.
- [x] AGENTS görev metni: iki görev kurulu ve etkin (bilet 15, 06.10); saat TASARIM §6'da; XML açıklamaları AGENTS'a atıf.
- [x] Bilet 02 durumu commit'e uyar (done, PR #5).
- [x] Test kapısı ve ruff yeşil; bağımsız denetçi GEÇTİ. (310/310, ruff temiz; Codex tur 3 GEÇTİ, 14.10.)

Dışarıda bırakılan: `test_gelecek` ve değişmez kural satırları standartta kural, DoD'de kanıt maddesidir; çift kayıt değil.
Bilet 02'nin kutuları madde madde doğrulanmadı; kanıt `denetim/tansu-sapma-dogrulama.md`.

## Comments

- 14.10 denetim tur 1 (Codex): KALDI. Bulgular: adım 9 "kâğıt üstü izleme başladı" yanlıştı; sadakat §4 satırı kod atfı olmadan
  eklendi; TASARIM §2 havuz sayısı eski kaldı; bilet elle yazıldı. Dördü düzeltildi (bilet `to-tickets` şablonuyla yeniden yazıldı).
- 14.10 denetim tur 2 (Codex): KALDI. Bulgu: denetçi kutusu tur geçmeden işaretlenmişti. Kutu açıldı; denetçi GEÇTİ deyince kapanır.
- 14.10 denetim tur 3 (Codex): GEÇTİ. Denetçi bu kapanış commit'ini yeni tur olmadan kabul etti.
