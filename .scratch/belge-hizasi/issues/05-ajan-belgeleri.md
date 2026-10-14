# 05: Ajan belgeleri, araştırma ve eski rapor güncel

**What to build:** AGENTS.md, `docs/agents/`, `docs/denetim.md`, araştırma notları ve 05.10 ön deneme raporu bugünkü kararları
anlatır; geri çekilmiş öneriler işaretlidir.

**Blocked by:** 03

**Status:** in-review (pr/05-ajan-belgeleri)

- [ ] `denetim/hiza-a.md` 1–7, 17–20 işlendi (CSV başlıkları ASCII mi Türkçe mi, aylık görev, PR onayı ile sohbet onayı,
      issue-tracker `Status:` alanı, denetim raporu yanlış kabul tanımı).
      Açık kısım: `tansu/denetim.py:281–288` `docs/denetim.md`'yi eski yanlış kabul cümlesiyle yeniden üretir; bilet 07 (kod). Belge tarafı kapandı.
- [x] `hiza-a.md` 25–31 tekrarları atıfa çevrildi.
- [x] `hiza-d.md` 40–45, 48–50: araştırma önerileri "geri çekildi, yerine: TASARIM §…" diye işaretlendi; `rapor/kanit-20261005.md`
      başına "geçersiz ön deneme" notu kondu; fiyat adımı tablosu tek kopya.
- [ ] `hiza-a-istem.md` yeniden koştu; bulgu yok.

## Comments

2026-10-14: skill adları, ADR anlatımı ve tek sahip düzeltmeleri harness hizasında yapıldı (.scratch/arsiv/harness-hizasi-1410/plan.md, tur 2 ve 3; commit a229003); Status sözleşmesi, docs/denetim.md, araştırma notları ve 05.10 raporu açık.
2026-10-14 (bilet 05, yazar): kutu 2–3 işaretli (kutu 1 tur 1 denetiminden sonra açık: üretici kod, bilet 07); her bulgunun kanıtı `denetim/bilet-05-rapor.md`. Kutu 4 (hiza-a-istem.md yeniden koşusu) bilerek işaretsiz: koşu bu dalın dışında. Status sözleşmesi `docs/agents/issue-tracker.md` "Status field" bölümünde; `docs/denetim.md` tanımı TASARIM 5.12'ye bağlandı; araştırma notları "geri çekildi, yerine: TASARIM §…" ile işaretlendi; fiyat adımı tablosu yalnız TASARIM §5.1'de. `rapor/kanit-20261005.md` uyarısı yalnız yerel diskte (rapor/ git dışı).
- 14.10 denetim tur 2 (Codex): KALDI. A2 `done` sözleşmesi bilet 06 uygulamasına uyduruldu (dal adı isteğe bağlı); A4 AGENTS Git maddesi yalnız-ekleme kuralını tekrar etmiyor, TASARIM §5.11'e atıf; A10 KURALLAR:166 ölçüm rakamları sadakat.md'ye atıf oldu.
- 14.10 denetim tur 3 (Codex): KALDI (AGENTS:44 `kayit/` izleme kuralı TASARIM §5.11 ile tekrar; bilet 02/03/09 Status değerleri sözleşmeye uymuyor). AKIS: dördüncü tur yok. Kök neden: Status sözleşmesi var olan biletlere karşı denetlenmeden yazıldı; AGENTS Git maddesi atıftan sonra da izleme kuralını tekrar etti. Yeniden tanım (bilet 05b, aynı dal): AGENTS Git maddesi izleme kuralını TASARIM §5.11'e bırakır; bilet 02/03/09 `done (PR #N, birleşme hash)` olur. Yeni denetim tur 1.
