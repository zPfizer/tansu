# 03: TASARIM kendi içinde ve karar kayıtlarıyla tutarlı

**What to build:** TASARIM.md'nin iç çelişkileri ve karar kayıtlarından eksik ya da farklı aktarılmış maddeler, karar
kaydına göre düzeltilir. Kayıt sessizse Levent'e kısa soru sorulur.

**Blocked by:** 01, 02

**Status:** ready-for-agent

- [ ] `denetim/hiza-e.md` ÇELİŞKİ ve ESKİ satırları (1–21, 27) karara göre işlendi; her düzeltme karar etiketini gösterir.
      Örnek: `veri/` silinmez (karar.md:24) → 30 gün silme maddesi kalkar.
- [ ] `denetim/tasarim-kod.md` §4 iç çelişkileri (piyasa durumu K1(b), geliştirme Holm p'si, hash kapsamı, iki kanıt
      satırı, komut listesi) çözüldü.
- [ ] `hiza-b.md` ÇELİŞKİ 1, 7 ve ESKİ 8 işlendi.
- [ ] Levent'e yalnız kaydın sessiz kaldığı sorular gitti; cevaplar TASARIM'a ve gerekiyorsa karar.md'ye yazıldı.
- [ ] `hiza-e-istem.md` yeniden koştu; ÇELİŞKİ bulgusu yok.
- [ ] Sözlük denetimi (10.10, bilet 01) TASARIM tarafı: §5.13 "tüm evren" → "indirilen bütün hisseler"; çift rotasyonundaki "hedef" GLOSSARY'deki iki anlamla tutarlı; yarım kalan resmi koşunun m'ye katkısı §5.11'de tek yerde.
- [ ] Sözlük denetimi 2. tur TASARIM tarafı: §5.3 "düşen sinyal kaymaz" ile §5.13 "dolum sonraki geçerli güne kayar" ayrımı açık; §5.10 "K1'e göre" ile uygulama (sepet farkı, K1 tekrarı yok) tek anlatım; §5.12 "ileri yürüme yılları" ile §5.8 sabit parametreli yıllık bölme ilişkisi açık.
- [ ] Sözlük denetimi 3. tur TASARIM tarafı: §5.1 olay günündeki "taban" limit hesabının başlangıç fiyatıdır, adı "baz fiyat" olur; §5.7 K1'deki "açık pozisyonda gelen sinyal düşer" → "yeni işlem açmaz ve sayıma girmez" (Düşen sinyal terimiyle karışmasın); §5.6 nakitten ilk alım "ilk geçiş" değil "ilk giriş"; §5.3'te R (hisse başına giriş − stop) adıyla yazılır; §5.5'e gerçek aralığın hesabı eklenir.
- [ ] Sözlüğün Tansu denetimi (10.10) TASARIM tarafı: §5.12 ölçüt 1'deki "ileri yürüme yılları" Tansu'nun parametre optimize eden walk-forward'u değildir; ad "yıllık sonuç dilimleri" gibi ayırt edici bir adla değişir ya da fark §5.8'de yazılır.
- [ ] Sözlük denetimi 6. tur TASARIM tarafı: çift örnekleminin 100 geçişine nakitten ilk alımın girip girmediği §5.9'da yazılır; boru hattı denetimindeki sentetik dünyanın β'sı (piyasa payı çarpanı) çift seçimindeki β'dan ayrı adlandırılır.
