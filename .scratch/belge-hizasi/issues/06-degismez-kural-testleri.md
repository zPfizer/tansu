# 06: TASARIM değişmez kurallarının hepsi testle korunur

**What to build:** Kodda olan ama testi olmayan her değişmez kural, dış davranıştan sınayan bir testle korunur. Kural bozulunca CI kırmızı olur.

**Blocked by:** None (can start immediately)

**Status:** in-progress (PR: §2'nin 16 kuralı; kalan 2 aşağıda)

- [ ] `denetim/tasarim-kod.md` §2'deki her kural için önce kırmızı (kural bozulunca) sonra yeşil test var (`/tdd`).
- [ ] Yokluk kuralları (Yahoo/TradingView yok, valör yok, fiyat yamanmaz) için kaynak ve davranış testi var.
- [ ] `pytest -q` yeşil; test gevşetilmedi (AGENTS.md test kuralları).

## Comments

10.10: 18 test yazıldı (Codex Sol), Claude koştu ve mutasyonla denetledi: 16 testte kural bozulunca test kırmızı
(sırayla kod değişikliği uygulanıp geri alındı). Mutasyonla denetlenmeyen 3 test: piyasa durumu, karantina yamanmaz,
çift bölmesinde stop/hedef yok (dış davranış testleri; doğrudan kırıcı tek satır bulunamadı).
Kalan: kart durumları (bilet 02 değiştirebilir, ondan sonra); rapor üstüne yazmama (kod TASARIM'dan farklı, bilet 07).
