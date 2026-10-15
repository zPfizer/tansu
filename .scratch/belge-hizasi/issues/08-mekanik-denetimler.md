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
- [x] Kodu hiç olmayan sekiz karar (`tasarim-kod.md` §1; 9. madde 07f ile kapandı, TASARIM 5.8) mimari işinin (`.scratch/tansu-mimari/spec.md`) 5. adımına bağlandı.
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
- 08 denetim tur 1 (15.10, Codex KALDI; 6 madde düzeltildi, her biri geçici kopyada kırmızı sonra yeşil):
  1. Atıf listesi, aralık ve dosya biçimi: `TASARIM §5.1, §99`, `5.5 ve §6`, `§5.1–5.99` (iki uç), `5.1/5.99`, `TASARIM.md §99`, `` `docs/TASARIM.md` §99 `` her numarayı denetler.
     Virgüllü liste öğesi `§` ya da noktalı olmalı; düz sayı yalnız `–` aralığında (`§2–3`) sayılır (`TASARIM 5.1, 6 gün` liste değil). Kırmızı: `docs/sadakat.md` kopyasına eklenen
     `TASARIM §5.1, §99 ve TASARIM §5.1–5.99 ve docs/TASARIM.md §98` için `§99`, `§5.99`, `TASARIM.md` §98` üç hata.
  2. Bölüm numarasız başlıkta da biter (`## Ek A`); kod bloğundaki `#` satırı başlık sayılmaz. Kırmızı: `TASARIM 8 "Eleştiri bulguları"` (metin Ek A başlığında) hata verir.
     Örnekleme: yeni kuralla bozuk atıf 1: `tansu/istatistik.py:258` `TASARIM 5.10, 5.12.4` (5.12.4 başlık değil; kastedilen 5.12 ölçüt 4, yılların %60'ı, `YIL_ESIK`). Metin `TASARIM 5.10, 5.12 ölçüt 4` yapıldı
     (yorum; `ast.dump` hash'i yorumu görmez). Denetçinin `TASARIM 8 "Küçükler"` ve `8.10` örnekleri depoda yok, birim testlerde (`## Ek A` kuralı) kırmızı.
  3. Sahip dosyalarının içindeki yollar: `yol_kirikleri` (`tansu/`, `tests/`, `docs/`, `.github/`, `kurulum/`, `kayit/`, `.claude/`, `.scratch/`, `arsiv/` ile başlayan ve `GLOSSARY.md`, `TASARIM.md`, `pyproject.toml` gibi kök dosya adları).
     Örnekleme: 104 yol benzeri belirteç, 23 eksik; hepsi yol değil: çalışma çıktısı klasörleri (`veri/`, `rapor/`, `gunluk/`: `.gitignore`'da, her koşuda oluşur, taranmaz) ve şablon/aralık işareti taşıyanlar
     (`<`, `*`, `…`, `YYYY`, `–`, `NN`). Gerçek ölü yol 0. Üç bare ad adlandırılmış istisna: `AKIS.md` (YONETIM), `TODO.md` (reddedilen fikir, karar.md 20-031), `GLOSSARY-MAP.md` (domain.md "yok" der).
     Kırmızı: `GLOSSARY.md` kopyasına `tansu/olmayan_denetim.py` hata verir.
  4. Yerel yol atlama: `.gitignore`'daki sabit kökün (`docs/sorgu`, `docs/strateji-taslak`, ...) kendisi yoksa atlanır; kök varsa eksik dosya hatadır (`git check-ignore` kaldırıldı). Kırmızı: `docs/sorgu` varken `docs/sorgu/olmayan.md` hata verir.
  5. Havuz kısa atıfları: her kısa atıf tek nota çözülür (tam ad varsa o); birden çok nota giden atıf `belirsiz atıf ...` hatası; çözülmeyen yok sayılır. Gerçek havuzda belirsiz atıf 0, atıfsız 0.
     Kırmızı (havuzun geçici kopyası): `tweet-atr-yeni-not.md` eklenince `belirsiz atıf tweet-atr: ...` ve `tweet-atr-yeni-not`; `gorsel-paket-01-yeni-not.md` eklenince `belirsiz atıf gorsel-paket-01` ve `gorsel-paket-01-yeni-not`.
  6. `docs/agents/*.md` driftlint'in bulduğu dosya türü değil; ölü yolları madde 3'ün taramasıyla `test_sahipler.py::test_tablodaki_dosyalarin_ve_docs_agents_in_depo_yollari_var` denetler (ölü komut denetimi yok).
     driftlint çevrimiçi, depo kopyasında: `driftlint: 0 errors, 0 warnings, 1 info across 3 context files` (çıkış kodu 0).
- 08 denetim tur 2 (15.10, Codex KALDI; 5 madde düzeltildi; her biri için kardeş mutasyonlar arandı):
  1. Şablon işareti (`<`, `*`, `…`, `YYYY`, `–`, `NN`) yalnız ayrıştırılmış yola bakar; sondaki açıklama yolu gizlemez. Kırmızı: `tansu/audit_missing.py (NN numaralı bölüm)` GLOSSARY kopyasında hata verir.
     Kardeşler (hepsi yakalandı): `tests/yok.py:3 (NN)`, `docs/yok.md (açıklama * <x>)`, `.github/yok.yml (YYYY)`, `tansu/yok.py (A–E)`, `tansu/yok.py …`. Kaçan kardeş: `beyin_kirikleri` (havuz belirteci) aynı açıklama
     boşluğunu taşıyordu (`` `gorsel-paket-999-yok (açıklama)` `` geçerdi); yalnız ad (`:satır`, `#parça`, açıklama atılır) denetlenir oldu, 3 birim test.
  2. Ad istisnaları dosyaya ve anışa bağlandı: `AKIS.md` yalnız `CODING_STANDARDS.md` içinde "the session review in " ardından; `TODO.md` yalnız `docs/sorgu/izleme/karar.md` içinde "yerine " ardından;
     `GLOSSARY-MAP.md` yalnız `docs/agents/domain.md` içinde "no " ardından. Kırmızı: domain.md'nin `GLOSSARY.md` okuma yolu `TODO.md` olunca ve `GLOSSARY-MAP.md` olunca hata verir.
     Kardeşler (hepsi yakalandı): AGENTS.md'de `AKIS.md`; CODING_STANDARDS.md'de `TODO.md` ve `GLOSSARY-MAP.md`; triage-labels.md'de `GLOSSARY-MAP.md`; karar.md'de başka satırda `TODO.md`; domain.md'de istisna cümlesinin ilk anışı.
  3. Windows yolları (`\` → `/`) ve Markdown bağlantı hedefleri (`[m](hedef "başlık")`, `![r](hedef)`, `<hedef>`, `[kimlik]: hedef`; bağlantıyı taşıyan dosyaya göre çözülür; `http(s):`, `mailto:`, `#bağlantı` atlanır; `#parça`, `?sorgu` atılır;
     depo dışına çıkan hedef de var olmalı). Örnekleme: sahip dosyaları ve docs/agents içinde 520 bağlantı; hepsi `docs/strateji-taslak/` altında (kazınmış üçüncü taraf README'leri); gerçek ölü bağlantı 0. `docs/strateji-*`
     bağlantı taramasından hariç (kural belgesi değil, kayma denetimi dışı; adlandırılmış istisna `TASLAKLAR`). Kırmızı: `` `docs\AUDIT_MISSING.md` `` ve `[x](../../docs/AUDIT_MISSING.md)` hata verir.
     Kardeşler (hepsi yakalandı): `tests\yok.py`, `.github\workflows\yok.yml`, `kayit\yok.jsonl:7`, `[x](docs/yok.md#a)`, `![i](docs/yok.png "t")`, `[x](<docs/yok.md>)`, `[x](..\yok.md)`, `[ref]: docs/yok.md`, docs/agents içinde `[x](./yok.md)`.
  4. Tam gorsel-paket adları kısa numara olarak yeniden okunmaz (tam ad eşleşmeleri kısa atıf taramasından önce metinden çıkarılır). Kırmızı: `gorsel-paket-1-ad-a` ve `gorsel-paket-01-ad-b` yalnız tam adla anılınca eski kod `belirsiz atıf` verirdi, şimdi temiz.
     Kardeşler (zaten doğru çalışıyordu, testle sabitlendi): `kaynak-x-123`/`kaynak-x-456` tam adlar; `tweet-atr` ile `tweet-atr-risk` tam adlar; `assets/gorsel-paket-12-ad/...` yolu; tam ad + `-13-ad` biçimi. Gerçek belirsizlik hâlâ hata: tam ad + aynı numaraya `G12`.
  5. Mimari spec 5. adım: 9. karar (blok uzunluğu ve masraf senaryoları günlükte ayrı alan) 07f ile kapandı (TASARIM 5.8: blok uzunluğu çıktıdır; masraf düzeyi başına sonuç `masraf_sonuc`). Listeden çıkarıldı; "dokuz" her yerde "sekiz":
     `.scratch/tansu-mimari/spec.md`, bu biletin 6. kutusu, `.scratch/belge-hizasi/spec.md`; `tasarim-kod.md` §1'in 9. maddesine "Kapandı (07f)" notu. Kalan sekiz maddenin koda karşı bugünkü durumu elle bakıldı: sadakat sonrası kayıt, `duzeltme`, "Uyarı yok", K2 karantina,
     Canlı durumu için kodda karşılık hâlâ yok.
