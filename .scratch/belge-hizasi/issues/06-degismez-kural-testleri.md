# 06: TASARIM değişmez kurallarının hepsi testle korunur

**What to build:** Kodda olan ama testi olmayan her değişmez kural, dış davranıştan sınayan bir testle korunur. Kural bozulunca CI kırmızı olur.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] `denetim/tasarim-kod.md` §2'deki her kural için önce kırmızı (kural bozulunca) sonra yeşil test var (`/tdd`).
- [ ] Yokluk kuralları (Yahoo/TradingView yok, valör yok, fiyat yamanmaz) için kaynak ve davranış testi var.
- [ ] `pytest -q` yeşil; test gevşetilmedi (AGENTS.md test kuralları).
