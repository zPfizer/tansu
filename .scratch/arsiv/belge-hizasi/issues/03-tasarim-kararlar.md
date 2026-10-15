# 03: TASARIM kendi içinde ve karar kayıtlarıyla tutarlı

**What to build:** TASARIM.md'nin iç çelişkileri ve karar kayıtlarından eksik ya da farklı aktarılmış maddeler, karar
kaydına göre düzeltilir. Kayıt sessizse Levent'e kısa soru sorulur.

**Blocked by:** 01, 02

**Status:** done (PR #8, c8a1d42)

- [x] `denetim/hiza-e.md` ÇELİŞKİ ve ESKİ satırları (1–21, 27) karara göre işlendi; her düzeltme karar etiketini gösterir.
      Kanıt: 22 madde işlendi; e-6 ve e-7 vekil kararıyla (14.10, Threads 37) uygulandı, `denetim/bilet-03-rapor.md`.
      Örnek: `veri/` silinmez (karar.md:24) → 30 gün silme maddesi kalkar.
- [x] `denetim/tasarim-kod.md` §4 iç çelişkileri (piyasa durumu K1(b), geliştirme Holm p'si, hash kapsamı, iki kanıt
      Kanıt: `denetim/bilet-03-rapor.md`, tasarim-kod §4 tablosu (4 düzeltildi, komut listesi zaten düzeltildi: bilet 09).
      satırı, komut listesi) çözüldü.
- [x] `hiza-b.md` ÇELİŞKİ 1, 7 ve ESKİ 8 işlendi.
      Kanıt: `denetim/bilet-03-rapor.md` b-1, b-7, b-8 düzeltildi (KURALLAR:10, KURALLAR:108, TASARIM 5.11).
- [x] Levent'e yalnız kaydın sessiz kaldığı sorular gitti; cevaplar TASARIM'a ve gerekiyorsa karar.md'ye yazıldı.
      Kanıt: iki soru vekile gitti (vekil kararı 14.10, Threads 37), Levent'e soru gitmedi; cevaplar TASARIM 5.1, 5.6'ya yazıldı. karar.md değişmedi (02-082 tam uygulandı).
- [x] `hiza-e-istem.md` yeniden koştu; ÇELİŞKİ bulgusu yok.
      Kanıt: Codex tur 1 (14.10) istemi tam kapsamla koştu (docs/sorgu 63 dosya, 10.581 satır): 6 bulgu (A1–A6), tur 1 düzeltmesiyle kapandı; tur 2 ve 3 değişen satırların çevresini denetledi. Tur 3 NOTLU GEÇTİ (not: 5.7'de k rütbe mi aşım sayısı mı, iki anlam). Taze tam koşu yapılmadı.
- [x] Sözlük denetimi (10.10, bilet 01) TASARIM tarafı: §5.13 "tüm evren" → "indirilen bütün hisseler"; çift rotasyonundaki "hedef" GLOSSARY'deki anlamlarla tutarlı; yarım kalan resmi koşunun m'ye katkısı §5.11'de tek yerde.
- [x] Sözlük denetimi 2. tur TASARIM tarafı: §5.3 "düşen sinyal kaymaz" ile §5.13 "dolum sonraki geçerli güne kayar" ayrımı açık; §5.10 "K1'e göre" ile uygulama (sepet farkı, K1 tekrarı yok) tek anlatım; §5.12 "ileri yürüme yılları" ile §5.8 sabit parametreli yıllık bölme ilişkisi açık.
- [x] Sözlük denetimi 3. tur TASARIM tarafı: §5.1 olay günündeki "taban" limit hesabının başlangıç fiyatıdır, adı "baz fiyat" olur; §5.7 K1'deki "açık pozisyonda gelen sinyal düşer" → "yeni işlem açmaz ve sayıma girmez" (Düşen sinyal terimiyle karışmasın); §5.6 nakitten ilk alım "ilk geçiş" değil "ilk giriş"; §5.3'te R (hisse başına giriş − stop) adıyla yazılır; §5.5'e gerçek aralığın hesabı eklenir.
- [x] Sözlüğün Tansu denetimi (10.10) TASARIM tarafı: §5.12 ölçüt 1'deki "ileri yürüme yılları" Tansu'nun parametre optimize eden walk-forward'u değildir; ad "yıllık sonuç dilimleri" gibi ayırt edici bir adla değişir ya da fark §5.8'de yazılır.
- [x] Sözlük denetimi 6. tur TASARIM tarafı: çift örnekleminin 100 geçişine nakitten ilk alımın girip girmediği §5.9'da yazılır; boru hattı denetimindeki sentetik dünyanın β'sı (piyasa payı çarpanı) çift seçimindeki β'dan ayrı adlandırılır.
- [x] Sözlük denetimi 10. tur TASARIM tarafı: §5.7 K1 uygulamasında açık pozisyona gelen sinyal için "düşer" yerine "yeni işlem açmaz ve sayıma girmez"; §5.13'te yalnız hacmi farklı tekrar satırının sonucu açık yazılır.

## Comments

- 14.10 denetim (Codex, Astra): tur 1 KALDI (A1–A6, getiri örneği, rapor e-16); tur 2 KALDI (5.7 Holm eşiği cümlesi, kanıt örneğinde % birimi). İkisi düzeltildi; kutu 1 (e-21, e-10) ve kutu 2 (iki kanıt satırı) bu düzeltmeyle kapandı.
- 14.10 denetim tur 3 (Codex): NOTLU GEÇTİ. Not: 5.7'de `k` hem Holm rütbesi hem aşım sayısı; ayrı adlandırma bilet 07 ya da sonraki belge turuna.
