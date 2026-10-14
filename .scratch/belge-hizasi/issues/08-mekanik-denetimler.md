# 08: Belge ayrılması ve mekanik kural ihlali CI'da yakalanır

**What to build:** Belgeler yeniden ayrılırsa ya da mekanik bir çalışma kuralı bozulursa CI kırmızı olur; düzen kendiliğinden korunur.

**Blocked by:** 01, 02, 03, 04, 05, 06, 07

**Status:** ready-for-agent

- [ ] Atıf testi: koddaki ve belgelerdeki `TASARIM <bölüm>` atıfları ve karar etiketleri (İ:, B-, C-, S2-) var olan bir bölüme ya da karara gider.
- [ ] `kayit/` dosyaları PR'da yalnız eklenmiş satır taşır; `veri/` altında silme yok (CI adımı).
- [ ] driftlint CI'da koşar (talimat dosyalarındaki ölü yol ve komut).
- [ ] driftlint yalnız talimat dosyalarını tarar. AGENTS.md "Belgeler ve sahipleri" tablosundaki her dosya bir testle
      taranır: depo yolları var, `TASARIM §` ve `KURALLAR §` atıfları var olan bölüme gider, beyin kaynak yolları
      (`gorsel-paket-*`, `kaynak-*`, `assets/…`) beyinde vardır (CI'da beyin yoksa bu kısım atlanır, yerel test kapısı
      denetler). Çalışma çıktısı adları (`durum.txt`, `manifest.json`, `kartlar.jsonl`) yol sayılmaz.
- [ ] `dod_kontrol.py` "Tansu:" satırının işaretli ve kanıtlı olmasını ister.
- [ ] Kodu hiç olmayan dokuz karar (`tasarim-kod.md` §1) mimari işinin (`.scratch/tansu-mimari/spec.md`) 5. adımına bağlandı.
- [ ] AGENTS.md "Geliştirme durdu" satırı kaldırıldı; mimari spec'in `Status` satırı `needs-triage`'a döndü.
- [ ] Havuz testi: beyindeki Tansu havuzunun her notu A–E'de atıflı ya da "kural içermez" listesinde; havuza yeni not gelince test kırmızı olur (CI'da beyin yoksa atlanır, yerel test kapısı denetler).

- 14.10: CI `dod` kontrolü (`.github/dod_kontrol.py:49`) yalnız "Sonuç: geçti" kabul ediyor; AKIS sözlüğündeki NOTLU GEÇTİ kararını tanımıyor. PR gövdesinde "geçti" yazıldı, not Denetçi satırında. Kontrolün NOTLU GEÇTİ'yi tanıması bilet 08'e.
