# 06: Sadakat kontrolü: çift Z (VAKBN–GARAN)

**What to build:** `sadakat` komutu VAKBN–GARAN için aday Z formüllerini dener. Tansu'nun rakamları:
- Z_t −3,108 ve Z_{t−1} −3,404
- Beta 1,675
- korelasyon 0,731
- piyasada kalma %72,27
- Mart–Mayıs 2025'te sinyal yok

Adayların hangisinin bu rakamları ürettiği `docs/sadakat.md`'ye yazılır. Hiçbiri üretmezse kural YORUM
kalır: log oran, 60 gün.

**Blocked by:** 05

**Status:** ready-for-agent

- [ ] Aday kümesi önceden `docs/sadakat.md`'ye yazılır:
  - log oran ve β'lı kalıntı
  - pencere 10–400
  - ddof {0; 1}
  - ham fiyat
- [ ] Tolerans: ±0,0005. Gevşek bant ±0,05 yalnız tek aday kalırsa kullanılır.
- [ ] Rapor tarihi bilinmediği için (Z_t, Z_{t−1}) çifti bütün işlem günlerinde aranır. Eşleşen günler
      yazılır.
- [ ] Sonuç KURALLAR §3 madde 1'e işlenir: seçilen formül ya da YORUM.
- [ ] `cift` modülünün Z ve ΔZ çekirdeği kurulur. Elle hesaplı küçük bir Z testi yazılır.
- [ ] Getiri hesaplanmaz. Bu iş `tur=sadakat` olarak günlüğe yazılır.
