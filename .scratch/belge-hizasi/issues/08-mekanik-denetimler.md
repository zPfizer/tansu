# 08: Belge ayrılması ve mekanik kural ihlali CI'da yakalanır

**What to build:** Belgeler yeniden ayrılırsa ya da mekanik bir çalışma kuralı bozulursa CI kırmızı olur; düzen kendiliğinden korunur.

**Blocked by:** 01, 02, 03, 04, 05, 06, 07

**Status:** ready-for-agent

- [x] Atıf testi: koddaki ve belgelerdeki `TASARIM <bölüm>` atıfları ve karar etiketleri (İ:, B-, C-, S2-) var olan bir bölüme ya da karara gider.
- [x] `kayit/` dosyaları PR'da yalnız eklenmiş satır taşır (CI adımı: `git diff --numstat origin/<taban>...HEAD -- kayit`, silinen satır 0).
      `veri/` yarısı düştü (vekil kararı, 15.10): `veri/` git'te değil (`.gitignore`), CI onu görmez; silme denetimi
      yalnız yerelde mümkündür.
- [x] driftlint CI'da koşar (talimat dosyalarındaki ölü yol ve komut).
- [x] driftlint yalnız talimat dosyalarını tarar. AGENTS.md "Belgeler ve sahipleri" tablosundaki her dosya bir testle
      taranır: depo yolları var, `TASARIM §` ve `KURALLAR §` atıfları var olan bölüme gider, beyin kaynak yolları
      (`gorsel-paket-*`, `kaynak-*`, `assets/…`) beyinde vardır (CI'da beyin yoksa bu kısım atlanır, yerel test kapısı
      denetler). Çalışma çıktısı adları (`durum.txt`, `manifest.json`, `kartlar.jsonl`) yol sayılmaz.
- [x] `dod_kontrol.py` "Tansu:" satırının işaretli ve kanıtlı olmasını ister.
- [x] Kodu hiç olmayan dokuz karar (`tasarim-kod.md` §1) mimari işinin (`.scratch/tansu-mimari/spec.md`) 5. adımına bağlandı.
- [ ] AGENTS.md "Geliştirme durdu" satırı kaldırıldı; mimari spec'in `Status` satırı `needs-triage`'a döndü.
- [x] Havuz testi: beyindeki Tansu havuzunun her notu A–E'de atıflı ya da "kural içermez" listesinde; havuza yeni not gelince test kırmızı olur (CI'da beyin yoksa atlanır, yerel test kapısı denetler).

- 14.10: CI `dod` kontrolü (`.github/dod_kontrol.py:49`) yalnız "Sonuç: geçti" kabul ediyor; AKIS sözlüğündeki NOTLU GEÇTİ kararını tanımıyor. PR gövdesinde "geçti" yazıldı, not Denetçi satırında. Kontrolün NOTLU GEÇTİ'yi tanıması bilet 08'e.
- 08 (15.10): Dal `pr/08-mekanik-denetimler`. Kararlar (vekil, 15.10, beyin Threads 64): Q1 atıf testi; Q2 `kayit/` CI adımı, `veri/` yarısı düştü;
  Q3 driftlint `0.19.0` (setup-node `24.19.0`); Q4 `dod_kontrol.py`; Q4b sahip dosyaları testi; Q5 havuz testi; Q6 spec bağı.
  - Dosyalar: `tests/atif_araclari.py` (ortak araçlar), `tests/test_atif.py`, `tests/test_sahipler.py`, `tests/test_havuz.py`,
    `tests/test_dod_kontrol.py`, `.github/dod_kontrol.py`, `.github/pull_request_template.md`, `.github/workflows/ci.yml`,
    `.driftlintrc.json`, `AGENTS.md` (Bağımlılık cümlesi, driftlint-ignore notları), `.claude/skills/tansu-grill/SKILL.md`,
    `.scratch/tansu-mimari/spec.md`.
  - Atıf testi: izlenen `.py`/`.md` dosyalarında (tansu/, tests/, docs/, AGENTS.md, GLOSSARY.md) bölüm atıfı 0 kırık, karar
    etiketi 0 kırık (etiketler `docs/sorgu/` ister; klasör yoksa test atlanır). Numaralı alt başlığı olmayan bölümde
    (TASARIM 6, 7, 8) `6.2` o bölümün 2. maddesi sayılır; 17 atıf (kod ve araştırma notları) bu biçimi kullanıyor, metin değişmedi.
    Kırmızı: `docs/sadakat.md` kopyasına `TASARIM §5.99`, `KURALLAR §9`, `B-77`, `İ: 08-999` eklenince `test_bolum_atiflari_var_olan_basliga_gider` ve `test_karar_etiketleri_sorguda_tanimli` kırmızı.
  - `kayit/` adımı: master geçmişinde `kayit/` 1 işlemde değişti; 16 birleştirme (`git diff --numstat <ana>^1...<birleştirme> -- kayit`)
    silinen satır 0. Geçici depoda satır değişince adım `exit 1`, satır eklenince `exit 0`.
  - driftlint: bayraklar yalnız `--help` listesindeki; yol `.`, yapılandırma `.driftlintrc.json` (`ignore: [".scratch/**"]`: arşivlenmiş eski
    `AGENTS.md` kopyası talimat dosyası değil). Taranan 3 dosya: `AGENTS.md`, `CLAUDE.md`, `.claude/skills/tansu-grill/SKILL.md`.
    `docs/agents/*.md` driftlint'in bulduğu dosya türü değil, taranmaz. Temiz klonda 5 sahte alarm çıktı (`veri/`, `docs/sorgu/`,
    `docs/strateji-taslak/` yerel, git'te yok); her biri bulunduğu satırda `driftlint-ignore` notu ve nedeniyle kapatıldı. Sonuç: 0 hata, 0 uyarı,
    1 bilgi (missing-rationale). Ölü yol eklenince çıkış kodu 1.
  - dod: kabul edilen kararlar `geçti`, `GEÇTİ`, `NOTLU GEÇTİ` (tam metin, IGNORECASE yok); `KALDI` kırmızı. Mesaj
    "Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik" oldu (iki test beklentisi bu yüzden değişti: kural bilerek genişledi).
    Kod öncesi 16 test kırmızı, sonra 31 yeşil.
  - Sahipler testi: tablo 14 depo yolu; yerel olanlar (`docs/sorgu/…`, `docs/strateji-*`) `.gitignore`'da ise CI'da atlanır, yazım hatası atlanmaz.
    Beyin yolu denetimi 831 belirteç taradı, 0 kırık; taslak dosyalar (`docs/strateji-*`) bu denetimden hariç (kayma denetimi dışı;
    `gorsel-paket-26` gibi çalışma adları havuzda yok).
  - Havuz testi: 258 not, 0 atıfsız. 7 not yalnız `-NN` kısa biçimiyle atıflı (21, 35, 38, 40, 52, 54, 55); her biri elle doğrulandı. Kırmızı: `tansu-calisma-kurallari`
    atıfı kaldırılınca test o notu söyleyerek kırılır.
  - Kapı: `pytest` 403 geçti, 1 kaldı (`test_kodlama_standartlari_genel_standartla_baslar`: YONETIM `CODING_STANDARDS.md` 15.10 satırı
    Tansu kopyasında yok; master'da da kırmızı, bu işten değil). `ruff check`, `ruff format --check`, `git diff --check` temiz.
- 08 ek (15.10): atıf testi, atıfın hemen ardındaki alıntı başlığı ya da kalın terimi (`TASARIM 5.8 "Kural kaydı"`; `"…"`, `“…”`, `‘…’`, `**…**`; arada `,`, `:`, ` ve`, `(`) atıf yapılan bölümün metninde de arar
  (başlıktan aynı ya da üst düzeydeki sonraki başlığa kadar; alt başlıksız bölümde madde metni; Türkçe i/ı/İ katlanır). Neden: `TASARIM 5.11 "Hash kapsamı"` (`tansu/kayit.py:42`, metin 5.8'de) bölüm var diye geçmişti.
  Tarama: alıntılı 29 atıftan 1 uyuşmazlık, o da `kayit.py:42`; 07f dalında 5.8'e düzeltildi, bu dalda bırakıldı, birleştirmeyle gelir (o zamana kadar `test_bolum_atiflari_var_olan_basliga_gider` bu dalda kırmızı).
