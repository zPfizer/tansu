# 01: Kural 7 gizli Akış satırını saymaz

**What to build:** `.github/dod_kontrol.py` Kural 7 yalnız görünen bir `Akış:` satırını kabul eder. Bugün HTML yorumu ya da kod bloğu içindeki `Akış: tansu-hata` satırı kontrolü geçirir (GitHub Codex P2, PR 27, `.github/dod_kontrol.py:120`).

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

**Fix direction (YONETIM oturumu, 16.10):** Kural 7 yalnız PR gövdesinin ilk boş olmayan satırına bakar. Bu satır `Akış: <beceri adı>` olmalıdır. `.github/pull_request_template.md` satırı en üste koyar. İlk satırdan önce yorum ya da kod bloğu açılamaz, bu yüzden gizli satır geçemez.

- [ ] Kırmızı test önce: PR 27'deki Codex tur 1 ve tur 2 durumlarının her biri yeni kurala göre test olur (aşağıdaki geçmiş).
- [ ] `dod_kontrol.py` Kural 7 ilk boş olmayan satırı denetler; şablon `Akış:` satırını en üste alır; `tansu-yeni-is/ortak-adimlar.md` "Pull request" kuralı yazar.
- [ ] Codex denetimi GEÇTİ ya da NOTLU GEÇTİ.

## Comments

PR 27 geçmişi (16.10): üç düzeltme denendi ve geri alındı (b48da45, 41d882c, 13a5ce9; geri alma 05bf213, 6a0fcd9, b10e446).
- Düzenli ifade (b48da45): Codex tur 1 KALDI. Çit uzunluğu, kapanmayan çit, kod içindeki `<!--`, yorum silinince çit açılması.
- El yazımı satır tarayıcısı (41d882c): Codex tur 2 KALDI. Yorum içinde `#27` satırı, iki satıra yayılan satır içi kod, aynı satırda `--> <!--`.
- markdown-it-py ayrıştırıcısı (13a5ce9): denetlenmedi; birleştirme önceliği yüzünden geri alındı. Test durumları o commit'te durur.
