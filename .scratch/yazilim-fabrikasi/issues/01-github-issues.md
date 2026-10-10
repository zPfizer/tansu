# 01: Biletler GitHub Issues'ta

**What to build:** Açık biletler GitHub issue olur; Levent açık işleri ve durumlarını GitHub'da tek listede görür. Ajanlar biletleri oradan okur ve yazar.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] İş takibi belgesi GitHub Issues'u anlatır (Matt'in GitHub şablonu); AGENTS.md "Issue tracker" satırı buna göre değişir.
- [ ] Etiketler depoda var: beş durum etiketi, `yerel`, `ci-kirmizi`, `inceleme-gecti`.
- [ ] Belge hizası ve mimari işinin açık biletleri issue olarak taşındı; engel bağları issue numaralarıyla yazılı; beyin havuzu ya da gerçek veri gereken biletlerde `yerel` etiketi var.
- [ ] `.scratch/` altındaki taşınan biletlerin yerinde issue bağlantısı kalır; aynı bilet iki yerde yürümez.
- [ ] driftlint ve pytest temiz.
