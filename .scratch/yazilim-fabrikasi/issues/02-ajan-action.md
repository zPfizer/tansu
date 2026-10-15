# 02: Etiketlenen bilet bulutta PR'a döner

**What to build:** Bir issue'ya `ready-for-agent` etiketi konunca GitHub Actions'ta Claude ajanı bileti AGENTS.md iş akışıyla yapar ve PR açar. `yerel` etiketli issue bulutta koşmaz.

**Blocked by:** 01; Levent'in abonelik jetonunu depo sırrı olarak girmesi (spec "Kimlik").

**Status:** ready-for-agent

- [x] Ajan iş akışı dosyası `anthropics/claude-code-action` ile, etiket tetiğiyle kurulu; `yerel` etiketi koşuyu atlar.
- [ ] Ajan `pr/NN-<ad>` dalı açar, AGENTS.md ve iki standart dosyasını okur, PR gövdesini PR şablonuyla yazar.
- [ ] Deneme issue'su (yalnız belge değişikliği) etiketlendi; PR açıldı, CI koştu. Actions çalıştırma bağlantısı PR'da.
- [ ] `yerel` etiketli deneme issue'su etiketlendi; Actions kaydında koşu atlandı.
- [x] AGENTS.md iş akışı 3. ve 4. adımlarında bulut yolu yazılı: etiket → ajan → PR; `yerel` bilet bu makinede yürür.

## Comments

f02 (15.10): İş akışı `.github/workflows/ajan.yml` yazıldı (dal `pr/f02-ajan-action`, push yok). Kutu 1 ve 5 işaretli. Kutu 2–4 canlı koşu ister; Levent'in iki adımına bağlı: Claude GitHub App kurulumu ve depo sırrı `CLAUDE_CODE_OAUTH_TOKEN`. İzin sözdizimi kaynağı: code.claude.com/docs/en/permissions; izin bloğu kaynağı: claude-code-action `examples/claude.yml`.

f02 ön inceleme (15.10): GITHUB_TOKEN izni `contents: read` ve `id-token: write`'a indi (push, PR ve yorum uygulama jetonuyla yapılır). Push yalnız `git push -u origin pr/*` ve `git push origin pr/*`; `master` ve `:` itme reddedilir; istem `git push -u origin pr/<N>-<slug>` der. İstem artık kanıtsız kutu işaretlemeyi yasaklar ve `Gerçek veri kanıtı` bloğuna gerçek pytest çıktısı koydurur (ajanda `veri/` yok). Ek yasaklar: `git commit -a`, `git -C`, `git add -u`, `git add ./*`. Hâlâ doğrulanmayan: kutu 2–4 canlı koşu; `Bash(git push -u origin pr/*)` kalıbının eşleşmesi.
