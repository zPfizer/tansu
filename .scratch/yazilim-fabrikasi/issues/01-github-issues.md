# 01: Biletler GitHub Issues'ta

**What to build:** Açık biletler GitHub issue olur; Levent açık işleri ve durumlarını GitHub'da tek listede görür. Ajanlar biletleri oradan okur ve yazar.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [x] İş takibi belgesi GitHub Issues'u anlatır (Matt'in GitHub şablonu); AGENTS.md "Issue tracker" satırı buna göre değişir.
- [x] Etiketler depoda var: beş durum etiketi, `yerel`, `ci-kirmizi`, `inceleme-gecti`.
- [ ] Belge hizası ve mimari işinin açık biletleri issue olarak taşındı; engel bağları issue numaralarıyla yazılı; beyin havuzu ya da gerçek veri gereken biletlerde `yerel` etiketi var.
- [ ] `.scratch/` altındaki taşınan biletlerin yerinde issue bağlantısı kalır; aynı bilet iki yerde yürümez.
- [ ] driftlint ve pytest temiz.

## Comments

- f01 (15.10): Kutu 1 ve 2 tamam. `docs/agents/issue-tracker.md` GitHub Issues için yeniden yazıldı (Matt şablonu; Status değerleri etiket + atanan + PR + issue durumuna eşlendi; engel bağı `Blocked by: #N` satırı; wayfinder haritası tek issue, çocuklar `Parent: #N`). `docs/agents/triage-labels.md` beş rol + `yerel`, `ci-kirmizi`, `inceleme-gecti`. AGENTS.md "Plan", "Kapanış" ve "Issue tracker" satırları uyarlandı. Sekiz etiket `zPfizer/tansu-kaynak` deposunda `gh label create --force` ile oluşturuldu/güncellendi (Türkçe açıklamalı). Kutu 3–5 (taşıma, kalan bağlantı, driftlint) B bölümünde.
