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

**Status:** done

- [x] Aday kümesi önceden `docs/sadakat.md`'ye yazılır:
  - log oran ve β'lı kalıntı
  - pencere 10–400
  - ddof {0; 1}
  - ham fiyat
- [x] Tolerans: ±0,0005. Gevşek bant ±0,05 yalnız tek aday kalırsa kullanılır.
- [x] Rapor tarihi bilinmediği için (Z_t, Z_{t−1}) çifti bütün işlem günlerinde aranır. Eşleşen günler
      yazılır.
- [x] Sonuç KURALLAR §3 madde 1'e işlenir: seçilen formül ya da YORUM.
- [x] `cift` modülünün Z ve ΔZ çekirdeği kurulur. Elle hesaplı küçük bir Z testi yazılır.
- [x] Getiri hesaplanmaz. Bu iş `tur=sadakat` olarak günlüğe yazılır.

## Comments

Gerçek ölçüm: anlık görüntü KRDMD + VAKBN + GARAN (`veri.indir` ile paylaşılan köke indirildi;
`python -m tansu sadakat` artık üç sembolü de içeren görüntü arar). Ham kapanış, 4204 ortak gün.

Sonuç: **üretilemedi.** 1564 aday (2 spread × pencere 10–400 × ddof {0; 1}) bütün günlerde arandı.
- Sıkı tolerans (±0,0005): eşleşme yok.
- Gevşek bant (±0,05): 534 aday eşleşti, tek aday kalmadı; bant kullanılmadı.
- KURALLAR §3 madde 1 ve §4'e işlendi: kural YORUM kalır (log oran, 60 gün). Tolerans sonuca bakıp
  genişletilmedi. Beta, korelasyon, piyasada kalma, Mart–Mayıs 2025 kontrolleri formül çıkmadığı için yapılmadı.

Yapılan: `tansu/cift.py` (Z, ΔZ, beta, korelasyon; elle hesaplı testler), `sadakat.cift_ara`, rapor bölümü.

Belge düzeltmesi: İş Yatırım GARAN yanıtı 276 yerde tarih sırasız geliyor (satır eksiksiz, tekrar yok).
TASARIM 5.13 yapı kapısı indirmeyi durduruyordu. Önce belge düzeltildi, sonra `kaynak.fiyat` tarihe göre
sıralar. Bu, başka sembollerde de sırasız yanıt olursa kapıyı gizler; kapı sıralanmış seriye bakar.

Açık işler:
- `kayit/deneme.jsonl` satırı basit (bilet 09 şemayı üstlenir). `kayit/` git'e girmedi.
- Aday kümesi Tansu'nun Z'sini üretmedi; olası ek adaylar (bugünü dışlayan pencere, getiri tabanlı beta)
  yeni deneme ve belge değişikliği gerektirir (Levent kararı).

- 2026-10-09: Worktree `TANSU-wt/06` ve dal `bilet-06` kaldırıldı (dal master'daydı). Worktree'deki tek `kayit/deneme.jsonl` satırı ana kayda eklenmedi: `olay` alanı yok, `kayit` okuyucusu bozulur. Ham satır:
  `{"tur": "sadakat", "tarih": "2026-10-05T12:05:09.978100+00:00", "anlik": "20261005-1504", "aile": "ema_sikismasi"}`
- 2026-10-10: Satır `olay: sadakat` ile ana kayda eklendi.
