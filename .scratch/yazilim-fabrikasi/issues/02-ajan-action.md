# 02: Etiketlenen bilet bulutta PR'a döner

**What to build:** Bir issue'ya `ready-for-agent` etiketi konunca GitHub Actions'ta Claude ajanı bileti AGENTS.md iş akışıyla yapar ve PR açar. `yerel` etiketli issue bulutta koşmaz.

**Blocked by:** 01; Levent'in abonelik jetonunu depo sırrı olarak girmesi (spec "Kimlik").

**Status:** ready-for-agent

- [ ] Ajan iş akışı dosyası `anthropics/claude-code-action` ile, etiket tetiğiyle kurulu; `yerel` etiketi koşuyu atlar.
- [ ] Ajan `pr/NN-<ad>` dalı açar, AGENTS.md ve iki standart dosyasını okur, PR gövdesini PR şablonuyla yazar.
- [ ] Deneme issue'su (yalnız belge değişikliği) etiketlendi; PR açıldı, CI koştu. Actions çalıştırma bağlantısı PR'da.
- [ ] `yerel` etiketli deneme issue'su etiketlendi; Actions kaydında koşu atlandı.
- [ ] AGENTS.md iş akışı 3. ve 4. adımlarında bulut yolu yazılı: etiket → ajan → PR; `yerel` bilet bu makinede yürür.
