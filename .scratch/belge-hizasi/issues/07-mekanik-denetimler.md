# 07: Belge ayrılması ve mekanik kural ihlali CI'da yakalanır

**What to build:** Belgeler yeniden ayrılırsa ya da mekanik bir çalışma kuralı bozulursa CI kırmızı olur; düzen kendiliğinden korunur.

**Blocked by:** 01, 02, 03, 04

**Status:** ready-for-agent

- [ ] Atıf testi: koddaki ve belgelerdeki `TASARIM <bölüm>` atıfları ve karar etiketleri (İ:, B-, C-, S2-) var olan bir bölüme ya da karara gider.
- [ ] `kayit/` dosyaları PR'da yalnız eklenmiş satır taşır; `veri/` altında silme yok (CI adımı).
- [ ] driftlint CI'da koşar (talimat dosyalarındaki ölü yol ve komut).
- [ ] `dod_kontrol.py` "Tansu:" satırının işaretli ve kanıtlı olmasını ister.
- [ ] Kodu hiç olmayan dokuz karar (`tasarim-kod.md` §1) mimari işinin (`.scratch/tansu-mimari/spec.md`) 5. adımına bağlandı.
