# 03: Kırmızı CI ve inceleme etiketle döngüye girer

**What to build:** PR'ın CI'ı kırmızıysa ajan aynı dalda düzeltir; yeşilse ikinci bir ajan bağımsız inceleme yapar ve sonucu etiketle bildirir. Birleştirme yalnız CI yeşil ve `inceleme-gecti` ile olur.

**Blocked by:** 02

**Status:** ready-for-agent

**Donduruldu (frozen):** Levent 15.10. Do not start, push, or merge this ticket. The branch `pr/f03-dongu` keeps the work.

- [ ] CI kırmızı olunca PR'a `ci-kirmizi` düşer; bu etiket ajanı aynı dalda yeniden çalıştırır; düzeltince etiket kalkar.
- [ ] CI yeşil olunca inceleme ajanı `/code-review` koşar; sonucu PR yorumu, "geçti" ise `inceleme-gecti` etiketi.
- [ ] Deneme PR'ında kırmızıdan yeşile döngü ve inceleme etiketi görüldü (Actions bağlantıları PR'da).
- [ ] Döngü sınırı var: aynı PR'da en fazla 3 düzeltme koşusu; sonra `ready-for-human`.
