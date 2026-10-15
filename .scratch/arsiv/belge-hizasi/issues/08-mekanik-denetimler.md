# 08: Belge ayrılması ve mekanik kural ihlali CI'da yakalanır

**What to build:** Belgeler yeniden ayrılırsa ya da mekanik bir çalışma kuralı bozulursa CI kırmızı olur; düzen kendiliğinden korunur.

**Blocked by:** 01, 02, 03, 04, 05, 06, 07

**Status:** done (PR #23, de9af9c)

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
- [x] AGENTS.md "Geliştirme durdu" bitiş koşulu güncellendi, satır silinmedi (Levent 15.10: satır, bilet 08, belge yapısı PR'ı ve Tansu'nun kendi ajanları birleşince biter; PR 19 yazdı); mimari spec'in `Status` satırı `needs-triage`'a döndü. Kanıt: 15.10 notu.
- [x] Havuz testi: beyindeki Tansu havuzunun her notu A–E'de atıflı ya da "kural içermez" listesinde; havuza yeni not gelince test kırmızı olur (CI'da beyin yoksa atlanır, yerel test kapısı denetler).

- 14.10: CI `dod` kontrolü (`.github/dod_kontrol.py:49`) yalnız "Sonuç: geçti" kabul ediyor; AKIS sözlüğündeki NOTLU GEÇTİ kararını tanımıyor. PR gövdesinde "geçti" yazıldı, not Denetçi satırında. Kontrolün NOTLU GEÇTİ'yi tanıması bilet 08'e.
- 08 (15.10): Dal `pr/08-mekanik-denetimler`. Kararlar (vekil, 15.10, beyin Threads 64): Q1 atıf testi; Q2 `kayit/` CI adımı, `veri/` yarısı düştü;
  Q3 driftlint `0.19.0` (setup-node `24.19.0`); Q4 `dod_kontrol.py`; Q4b sahip dosyaları testi; Q5 havuz testi; Q6 spec bağı.
  - Dosyalar: `tests/atif_araclari.py` (ortak araçlar), `tests/test_atif.py`, `tests/test_sahipler.py`, `tests/test_havuz.py`,
    `tests/test_dod_kontrol.py`, `.github/dod_kontrol.py`, `.github/pull_request_template.md`, `.github/workflows/ci.yml`,
    `.driftlintrc.json`, `AGENTS.md` (Bağımlılık cümlesi, driftlint-ignore notları), `.claude/skills/tansu-grill/SKILL.md`,
    `.scratch/tansu-mimari/spec.md`.
  - Atıf testi: izlenen `.py`/`.md` dosyalarında (o gün tansu/, tests/, docs/, AGENTS.md, GLOSSARY.md; bugünkü küme `DOSYA_KOKLERI`, 64 dosya) bölüm atıfı 0 kırık, karar
    etiketi 0 kırık (etiketler `docs/sorgu/` ister; klasör yoksa test atlanır). Numaralı alt başlığı olmayan bölümde
    (TASARIM 6, 7, 8) `6.2` o bölümün 2. maddesi sayılır; 17 atıf (kod ve araştırma notları) bu biçimi kullanıyor, metin değişmedi.
    Kırmızı: `docs/sadakat.md` kopyasına `TASARIM §5.99`, `KURALLAR §9`, `B-77`, `İ: 08-999` eklenince `test_bolum_atiflari_var_olan_basliga_gider` ve `test_karar_etiketleri_sorguda_tanimli` kırmızı.
  - `kayit/` adımı: master geçmişinde `kayit/` 1 işlemde değişti; birleştirmeler (o gün 16, 08-b'de 17) (`git diff --numstat <ana>^1...<birleştirme> -- kayit`)
    silinen satır 0. Geçici depoda satır değişince adım `exit 1`, satır eklenince `exit 0`.
  - driftlint: bayraklar yalnız `--help` listesindeki; yol `.`, yapılandırma `.driftlintrc.json` (`ignore: [".scratch/**"]`: arşivlenmiş eski
    `AGENTS.md` kopyası talimat dosyası değil). Taranan 3 dosya: `AGENTS.md`, `CLAUDE.md`, `.claude/skills/tansu-grill/SKILL.md`.
    `docs/agents/*.md` driftlint'in bulduğu dosya türü değil, taranmaz. Temiz klonda 5 sahte alarm çıktı (`veri/`, `docs/sorgu/`,
    `docs/strateji-taslak/` yerel, git'te yok); her biri bulunduğu satırda `driftlint-ignore` notu ve nedeniyle kapatıldı. Sonuç: 0 hata, 0 uyarı,
    1 bilgi (missing-rationale). Ölü yol eklenince çıkış kodu 1.
  - dod: kabul edilen kararlar `geçti`, `GEÇTİ`, `NOTLU GEÇTİ` (tam metin, IGNORECASE yok); `KALDI` kırmızı. Mesaj
    "Sonuç: geçti ya da NOTLU GEÇTİ satırı eksik" oldu (iki test beklentisi bu yüzden değişti: kural bilerek genişledi).
    Kod öncesi 16 test kırmızı, sonra 31 yeşil.
  - Sahipler testi: tablo 15 depo yolu; yerel olanlar (`docs/sorgu/…`, `docs/strateji-*`) `.gitignore`'da ise CI'da atlanır, yazım hatası atlanmaz.
    Beyin yolu denetimi 831 belirteç taradı, 0 kırık; taslak dosyalar (`docs/strateji-*`) bu denetimden hariç (kayma denetimi dışı;
    `gorsel-paket-26` gibi çalışma adları havuzda yok).
  - Havuz testi (o günkü gevşek kapsamla; kapsam 08-b'de daraldı, sonucu aşağıda): 258 not, 0 atıfsız. 7 not yalnız `-NN` kısa biçimiyle atıflı (21, 35, 38, 40, 52, 54, 55); her biri elle doğrulandı. Kırmızı: `tansu-calisma-kurallari`
    atıfı kaldırılınca test o notu söyleyerek kırılır.
  - Kapı: `pytest` 403 geçti, 1 kaldı (`test_kodlama_standartlari_genel_standartla_baslar`: YONETIM `CODING_STANDARDS.md` 15.10 satırı
    Tansu kopyasında yok; master'da da kırmızı, bu işten değil). `ruff check`, `ruff format --check`, `git diff --check` temiz.
- 08 ek (15.10): atıf testi, atıfın hemen ardındaki alıntı başlığı ya da kalın terimi (`TASARIM 5.8 "Kural kaydı"`; `"…"`, `“…”`, `‘…’`, `**…**`; arada `,`, `:`, ` ve`, `(`) atıf yapılan bölümün metninde de arar
  (başlıktan aynı ya da üst düzeydeki sonraki başlığa kadar; alt başlıksız bölümde madde metni; Türkçe i/ı/İ katlanır). Neden: `TASARIM 5.11 "Hash kapsamı"` (`tansu/kayit.py:42`, metin 5.8'de) bölüm var diye geçmişti.
  Tarama: alıntılı 29 atıftan 1 uyuşmazlık, o da `kayit.py:42`; 07f dalında 5.8'e düzeltildi, bu dalda bırakıldı, birleştirmeyle gelir (o zamana kadar `test_bolum_atiflari_var_olan_basliga_gider` bu dalda kırmızıydı; master c52c464 ile birleşince yeşil oldu).
- 08 denetim tur 1 (15.10, Codex KALDI; 6 madde düzeltildi, her biri geçici kopyada kırmızı sonra yeşil):
  1. Atıf listesi, aralık ve dosya biçimi: `TASARIM §5.1, §99`, `5.5 ve §6`, `§5.1–5.99` (iki uç), `5.1/5.99`, `TASARIM.md §99`, `` `docs/TASARIM.md` §99 `` her numarayı denetler.
     Virgüllü liste öğesi `§` ya da noktalı olmalı; düz sayı `–` aralığında (`§2–3`) sayılır (08-b'den beri `ve n` ve `/n` ardından da, sayıdan sonra sözcük gelmiyorsa); `TASARIM 5.1, 6 gün` liste değil. Kırmızı: `docs/sadakat.md` kopyasına eklenen
     `TASARIM §5.1, §99 ve TASARIM §5.1–5.99 ve docs/TASARIM.md §98` için `§99`, `§5.99`, `TASARIM.md` §98` üç hata.
  2. Bölüm numarasız başlıkta da biter (`## Ek A`); kod bloğundaki `#` satırı başlık sayılmaz. Kırmızı: `TASARIM 8 "Eleştiri bulguları"` (metin Ek A başlığında) hata verir.
     Örnekleme: yeni kuralla bozuk atıf 1: `tansu/istatistik.py:258` `TASARIM 5.10, 5.12.4` (5.12.4 başlık değil; kastedilen 5.12 ölçüt 4, yılların %60'ı, `YIL_ESIK`). Metin `TASARIM 5.10, 5.12 ölçüt 4` yapıldı
     (yorum; `ast.dump` hash'i yorumu görmez). Denetçinin `TASARIM 8 "Küçükler"` ve `8.2` biçimindeki örnekleri depoda yok, birim testlerde (`## Ek A` kuralı) kırmızı (`8.10` ayrıca denenmedi).
  3. Sahip dosyalarının içindeki yollar: `yol_kirikleri` (`tansu/`, `tests/`, `docs/`, `.github/`, `kurulum/`, `kayit/`, `.claude/`, `.scratch/`, `arsiv/` ile başlayan ve `GLOSSARY.md`, `TASARIM.md`, `pyproject.toml` gibi kök dosya adları).
     Örnekleme: 104 yol benzeri belirteç, 23 eksik; hepsi yol değil: çalışma çıktısı klasörleri (`veri/`, `rapor/`, `gunluk/`: `.gitignore`'da, her koşuda oluşur, taranmaz) ve şablon/aralık işareti taşıyanlar
     (`<`, `*`, `…`, `YYYY`, `–`, `NN`). Gerçek ölü yol 0. Üç bare ad adlandırılmış istisna: `AKIS.md` (YONETIM), `TODO.md` (reddedilen fikir, karar.md 20-031), `GLOSSARY-MAP.md` (domain.md "yok" der).
     Kırmızı: `GLOSSARY.md` kopyasına `tansu/olmayan_denetim.py` hata verir.
  4. Yerel yol atlama: `.gitignore`'daki sabit kökün (`docs/sorgu`, `docs/strateji-taslak`, ...) kendisi yoksa atlanır; kök varsa eksik dosya hatadır (`git check-ignore` kullanımı kaldırıldı; artık kullanılmayan `yerel_mi` işlevi 08-b'de silindi). Kırmızı: `docs/sorgu` varken `docs/sorgu/olmayan.md` hata verir.
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
     `.scratch/tansu-mimari/spec.md`, bu biletin 6. kutusu, `.scratch/belge-hizasi/spec.md`; `tasarim-kod.md` §1'in 9. maddesine "Kapandı (07f)" notu. Kalan sekiz maddeden 1, 3, 5, 6, 7 ve 8 için kodda karşılık olmadığı `grep` ile doğrulandı (sadakat sonrası kayıt, Canlı durumu, `duzeltme`,
     iki istisna türü, ayrılmış dönem sıfırlama, "Uyarı yok"); 2 ve 4. maddeler (kâğıt dönemi şartı, K2 karantina maskesi) kod okunarak yeniden doğrulanmadı, `tasarim-kod.md` kaydına güvenildi.
- 08 ön denetim (15.10, son Codex turundan önce; her madde için dosyada birim test, kırmızı kanıt kopyada):
  1. `madde N` atfı: `KURALLAR §3 madde 2`, `TASARIM 6 madde 99` bölümün N. maddesi (3.2, 6.99) diye denetlenir; gerçek depoda `madde` atıfları temiz (aileler.py:1, sadakat.py:12 dahil).
     Kırmızı: `TASARIM 6 madde 99`, `KURALLAR §1 madde 9`, satır sonu bölünmüş `§1\n  madde 9` eski kodla geçerdi (5 madde testi kırmızı), şimdi hata verir.
  2. Tarama kümesine `.claude/`, `.github/` ve `CLAUDE.md` eklendi (o gün 63 dosya, bugün 64; SKILL.md, pull_request_template.md, dod_kontrol.py dahil), hepsi temiz. `.scratch/` bilerek dışarıda: biletler ve arşiv tarihsel metindir,
     atıfları o günün TASARIM'ına göredir (o günkü tarama 16 kırık atıf verdi; 13'ü bu biletin kendi mutasyon örnekleri). Canlı 07 biletindeki 3 gerçek hata düzeltildi: `07-kod-sapmalari.md:127` `TASARIM 117` aslında satır numarası
     (`TASARIM.md satır 117`); :132 ve :134 eski TASARIM 5.1 cümlelerinden alıntı (07e-b'de yeniden yazıldı; "TASARIM 5.1'in o günkü ..." diye açıklandı). Arşive dokunulmadı.
  3. Gerçek tablo testi artık `docs/TASARIM.md` ve `docs/kurallar/A-yapi-bolge.md` ayrıştırılmış yollar arasında ve tam 1 beyin satırı olmasını ister. Kırmızı: AGENTS başlığı "(Belgeler ve sahipleri)" → "(Owners)" yapılınca test kırılır.
  4. Tarama kümesi testi: `docs/TASARIM.md`, `docs/KURALLAR.md`, `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md`, `tansu/kayit.py`, `.claude/skills/tansu-grill/SKILL.md`, `.github/pull_request_template.md` içerir; `.scratch/` içermez.
  5. Yol kökleri: dokuz kök için `{kök}/yok.x` ve altı şablon işareti için literal parametreli testler; kök dosya adı desenleri ayrıca. Kırmızı (kopya): KOKLER'den `.github` ve `kurulum` çıkarılınca 2 test, SABLON'dan `NN` çıkarılınca 1 test kırılır.
  6. `ci.yml` kayit adımı: `set -eu`, `set -o pipefail`, `git diff --numstat --no-renames`, `git rev-parse --verify origin/$BASE` başarısızsa `exit 1`. Betik ci.yml'den okunup geçici git deposunda `bash` ile koşan `tests/test_ci_kayit.py`
     ile denetlenir (8 test; bash yoksa atlanır). Sonuçlar: satır ekleme exit 0, yeni dosya exit 0, satır değiştirme exit 1, dosya silme exit 1, yeniden adlandırma exit 1, bilinmeyen taban exit 1, boş dosya silme exit 0 (bilinen sınır).
     Kırmızı (eski ci.yml ile): yeniden adlandırma exit 0 çıkıyordu, bilinmeyen taban exit 0 çıkıyordu, `pipefail`/`--no-renames` yoktu: 3 test kırmızı.
  7. `dod_kontrol.py`: `Sonuç:` ile başlayan (girintili dahil) bütün satırlar sayılır; tam bir tane olmalı ve kabul edilen üç metinden biri olmalı. `Sonuç: KALDI` + `Sonuç: GEÇTİ` hata verir ("Sonuç: satırı tek olmalı (2 satır var)").
     Kırmızı: eski kodla 5 yeni test kırmızı (KALDI+GEÇTİ, kaldı+geçti, GEÇTİ+GEÇTİ, girintili ikinci satır, boş ikinci `Sonuç:`). Şablon yorum satırı (`<!-- ... "Sonuç: geçti" ... -->`) sayılmaz.
  8. Havuz kesik kimlikleri: `kaynak-a-b-12` ve `-1` (not `-123`), `kaynak-ab` (not `kaynak-abc-1`), `gorsel-paket-0`/`G0`/`gp-0` (not `-01`), `gorsel-paket-1`/`G1`/`-1` (not `-12`), `gorsel-paket-123`, `T-atr` (not `tweet-atrx-y`),
     `tweet-atr-ris` kimliği kapsamaz; beyin yolu denetimi `gorsel-paket-0`, `gorsel-paket-011-x`, `kaynak-a-b-1` kesiklerini hata sayar. Kırmızı: ad başı eşleşmesinden tire sınırı kaldırılınca (`startswith(onek)`) 8 test kırılır (gerçek havuz testi dahil).
  9. Taslaklar (`docs/strateji-taslak`, `docs/strateji-modulleri-taslak.md`): AGENTS.md "kayma denetimi dışında" der; kod da artık atıf, yol, bağlantı ve beyin yolu denetimlerinde taslakları atlar (`test_taslaklar_atif_ve_yol_denetimi_disindadir`; aynı metin taslak olmayan dosyada hata verir).
     Tablodaki taslak yollarının var olması (`sahip_tablosu`) hâlâ denetlenir.
  10. PR şablonu yorumu: CI tek `Sonuç` satırı kabul eder ve yalnız üç metinden birini: `geçti`, `GEÇTİ`, `NOTLU GEÇTİ`; `Geçti`, KALDI ve ikinci `Sonuç` satırı reddedilir.
- Tanınan biçimler ve sınırlar (testler yalnız aşağıdakini denetler; bu liste kapsam dışını açıkça yazar). 08-b'den beri her cümle `tests/test_sinirlar.py`'de (ve ilgili birim testlerde) bir test durumudur; cümle yanlışsa test kırılır:
  - Bölüm atfı, tanınır: `TASARIM`/`KURALLAR` + (`.md` ya da `.md` ve kapanış backtick'i) + tek boşluk + isteğe bağlı `§` + numara (`5`, `5.11`); liste `, §n` ya da noktalı `, 5.3`, ` ve n`, `/n` (düz `n` yalnız sayıdan sonra sözcük gelmiyorsa: `TASARIM 5.1 ve 6 gün` okunmaz, `TASARIM 5 ve 99 ile` okunmaz); aralık `–` (iki uç; düz sayı uç dahil) ve `-` (yalnız noktalı uç); `madde N`.
     Tanınmaz: `TASARIM'ın §N`, `bölüm N`, küçük harf (`tasarım 5`), `§ 5` (boşluklu), `TASARIM` ile numara arasında satır sonu, `ile`/`veya`/`;` listeleri, em-dash (`—`) aralığı, virgüllü düz sayı (`5.1, 99`), üç düzey numara (`5.1.4` okunur ama başlık değil: hata verir),
     başlıksız bölümün maddesi dışında madde atfı (`TASARIM 5 madde 1` alt başlığı olan bölümde 5.1 başlığıyla karışır).
  - Alıntı terim, okunur: atıfın hemen ardından (`,` `:` ` ve` `(` ayracı olabilir) `"…"`, `“…”`, `‘…’`, `**…**`; terim atıf yapılan bölümün metninde aranır (Türkçe i/ı/İ katlanır, satır sonu tek boşluk). Okunmaz: atıftan önce gelen başlık
     (`"X" (TASARIM 5.8)`), ASCII tek tırnak, liste sonrası alıntı.
  - Karar etiketi, okunur: `B-n`, `C-n`, `S2-n` ve `İ: NN-NNN` (virgüllü liste, satır sonunda bölünebilir). Okunmaz: `B-1/99`'daki `99`, `B-1–99` aralığının sonu, `İ: a ve b`'deki ikinci kimlik, harfli sonek (`B-3b`), tablo başlıkları (`P3`, `M1`, `Sorgu S13`).
  - Yol, okunur: backtick içindeki ilk sözcük (`:satır`, `::test`, `#parça`, `\` ayracı düzeltilir); dokuz kök (tansu, tests, docs, .github, kurulum, kayit, .claude, .scratch, arsiv); büyük harfli kök `.md` adları, `pyproject.toml`, `requirements.lock.txt`;
     Markdown `[m](hedef)`, `![r](hedef)`, `[kimlik]: hedef` hedefleri (dosyaya göre). Okunmaz: backtick dışındaki çıplak metin yolları, `./` ile başlayan yollar, çitli kod bloğundaki çıplak satırlar (çit içindeki backtick'li aralıklar okunur), HTML bağlantıları (`<a href>`, `<img src>`), kod aralığındaki ikinci ve sonraki sözcükler,
     `veri/`, `rapor/`, `gunluk/` çıktı klasörleri, şablon işaretli yollar. Yerel kök (`docs/sorgu`, `docs/strateji-taslak`) yoksa CI'da atlanır, varsa eksik dosya hatadır.
  - Havuz: kapsam yalnız `docs/kurallar/A-…E-*.md` dosyalarının tamamı ve `docs/KURALLAR.md`'nin "Kural içermeyen notlar" bölümüdür (başlıktan sonraki `## ` başlığa kadar); KURALLAR'ın öbür bölümleri ve başka dosyalar atıf sayılmaz. Notlar: yalnız havuz klasörünün doğrudan altındaki `*.md` dosyaları; alt klasörler ve `.md` olmayan dosyalar sayılmaz (`assets/` yalnız yol olarak denetlenir); düz sözcüklü adlar (`not-…`, `tansu-…`) yalnız tam adla kapsanır;
     `-NN` kısa biçimi gevşektir (`-60)` gibi eksi bir sayı da o numaralı notu sayar; 7 not yalnız bu biçimle kapsanıyor); iki nota giden kısa atıf hatadır; hiçbir nota gitmeyen kısa atıf yok sayılır.
  - `kayit/` adımı: silinen satır sayar. Satırı olmayan (boş) dosyanın silinmesi 0 görünür ve geçer (`test_bos_dosya_silmek_gecer_bilinen_sinir`); ikili dosya `-` olarak 1 sayılır.
- 08 tur 3 KALDI → 08-b (15.10): AKIS kuralı gereği dördüncü tur yok; iş 08-b olarak yeniden tanımlandı (emsal 07d-b), yeni 3 turluk denetim. Kök neden: tarayıcının kapsamı kutu metninden gevşekti ve
  bilet, ayrıştırıcının okumadığı atıf biçimlerini "tanınır" diye yazdı; ayrıca denetim sürerken YONETIM standartlar dosyası (paralel oturum) değişti.
  Tur 3 bulguları: (1) havuz kapsamı kutu 8'den geniş (tüm KURALLAR.md ve `docs/kurallar/*.md` sayılıyordu; `tansu-calisma-kurallari` "kural içermez" listesinden "İnceleme bekliyor" bölümüne taşınınca test yeşil kaldı);
  (2) biletteki `ve n` ve `/n` listeleri kodda okunmuyordu (`TASARIM 5 ve 99`, `TASARIM 5/99` kaçıyordu); (3) biletin iddialarının hepsi testle ya da düzeltmeyle desteklenmemişti.
  08-b değişiklikleri:
  1. Havuz kapsamı: bir not yalnız `docs/kurallar/[A-E]-*.md` dosyalarında (tamamı) ya da `docs/KURALLAR.md`'nin "Kural içermeyen notlar" bölümünde (başlıktan sonraki aynı düzey `## ` başlığa kadar) anılırsa kapsanır; öbür KURALLAR bölümleri ve başka dosyalar sayılmaz
     (`glob` Windows'ta büyük/küçük harfi ayırmadığından dosya adı `re.fullmatch` ile ayrıca süzülür). Gerçek havuz sıkı kuralla da geçiyor: 258 not, 0 atıfsız, 0 belirsiz; yalnız başka metinle kapsanan not yok, listeye eklenen not yok.
     Kırmızı: gerçek `KURALLAR.md` kopyasında `tansu-calisma-kurallari` satırı silinip "## İnceleme bekliyor" bölümüne yazılınca `test_havuzdaki_her_not_atifli_ya_da_kural_icermez_listesinde` kırılır. Eski kapsamla 11 durumluk `test_havuz_kapsami_yalniz_a_e_ve_kural_icermez_listesidir`
     içinde 6 durum kırmızıydı (öbür bölüm, Dizin, sonraki bölüm, `Z-y.md`, `notlar.md`, `a-x.md`).
  2. `ve n` ve `/n`: düz sayı, sayıdan sonra boşluk ve sözcük gelmiyorsa atıf sayılır (`TASARIM 5 ve 99` → §99, `TASARIM 5/99` → §99, `TASARIM 5 ve 99 ve 98)` → §99, §98). Sözcük gelirse nesnedir: `TASARIM 5.1 ve 6 gün`,
     `TASARIM 5.1 / 99 gün`, `TASARIM 5.1, 99 gün`, `TASARIM 5 ve 99 ile` okunmaz; `TASARIM 5 ve 6.` ve `TASARIM 5/6;` geçerli numaralar olduğundan hata vermez. Kırmızı: eski kodla `TASARIM 5 ve 99`, `5/99`, `5 ve 99 ve 98)` 3 test kırmızı.
     Sınır: `TASARIM 5 ve 99 ile` gibi sayıdan sonra sözcük gelen gerçek liste okunmaz (yanlış alarm yerine kaçırma seçildi).
  3. İddia denetimi: bu biletin 08 girdilerinin 94 satırı, yeni yardımcı ve test dosyalarındaki 22 docstring ve 77 yorum okundu. 14 cümle yanlış ya da abartılıydı ve düzeltildi (10 bilet cümlesi: düz sayı yalnız `–`, `8.10`, `git check-ignore kaldırıldı`,
     "kalan sekiz maddeye bakıldı", "6 test kırmızı", `5.12.4` etiketi, "bölümü başka biçimde anan açıklama", kod çitleri, havuz kapsamı, `ve n`/`/n`; 4 kod metni: `HARIC` yorumu "bu iki test", modül docstring'inin dosya listesi, `beyin_kirikleri` docstring'i `…` işaretini yazmıyordu,
     kullanılmayan `yerel_mi` işlevi silindi), 7 cümle o günkü anlık ölçüm olarak etiketlendi (dosya sayısı, birleştirme sayısı, 403 geçti, 16 kırık atıf, 258 not ve gevşek kapsam vb.). "Tanınan biçimler ve sınırlar" bölümündeki her biçim
     iddiası için `tests/test_sinirlar.py` (48 durum) eklendi: okunmayan atıf biçimleri (11), okunan (5), okunmayan alıntı (4), okunmayan etiket (6), okunmayan yol (9), okunan yol (6), havuz sınırları (4) ve PR şablonu yorumu, CI araç sürümü sabitliği,
     driftlint yapılandırması. `tests/test_ci_kayit.py`'ye ikili dosya silme (exit 1) eklendi. Elle doğrulanan sayılar: tablo 15 depo yolu ve 1 beyin satırı, 17 `6.x/8.x` madde atfı, master'da `kayit/` 1 işlem ve 17 birleştirmede silinen satır 0,
     7 not yalnız `-NN` ile kapsanıyor (21, 35, 38, 40, 52, 54, 55), driftlint temiz klonda `0 errors, 0 warnings, 1 info across 3 context files`, çıkış 0.
- 15.10 (master 9bad506 birleştirildi, PR 19): `AGENTS.md` ve `CODING_STANDARDS.md` çakıştı; AGENTS.md master yapısıyla alındı (Bağımlılık cümlesi ve var olan 4 satırdaki driftlint-ignore notları dalda kaldı), CODING_STANDARDS.md tamamen master'ın (YONETIM eşitlemesi 19d5309 ve 508929d düştü, orijinal arşivlendi); test değişikliği yok, kapı 614 geçti, `ruff` temiz, temiz klonda driftlint `0 errors, 0 warnings, 1 info`, çıkış 0 (eski "1 kaldı" notundaki `test_kodlama_standartlari_genel_standartla_baslar` master'da silindi). Kalıntı: `AKIS.md` ad istisnası (`tests/atif_araclari.py:420`) artık gereksiz (AKIS.md depoda, "the session review in" cümlesi gitti); testler yeşil, kaldırmak ayrı iş.
- 15.10 (tur 1 düzeltmesi, Codex KALDI + Claude kod incelemesi): (1) `tests/test_dod_kontrol.py` `test_kural_5_sonuc_satiri_tek_olmali` beklenen iletiyi `(2 satır var)` literal yazar (5 durumun hepsi 2 satır). (2) `AKIS.md` ad istisnası `tests/atif_araclari.py` içinden ve onu sınayan 3 durum ile 1 beklenti `tests/test_sahipler.py` içinden kaldırıldı. (3) `DOSYA_KOKLERI` AKIS.md, CODING_STANDARDS.md, DEFINITION_OF_DONE.md ile genişledi; tarama kümesi testi ve `test_kok_belgelerinde_kirik_karar_etiketi_yakalanir` (3 durum) eklendi, eski kodla 4 test kırmızıydı. (4) Yerel sahip dosyaları (`docs/sorgu/…`, `docs/strateji-*`) kendi parametreli testlerine ayrıldı; dosya yoksa test adıyla ve nedenle atlanır (eskiden sessizce düşüyor, CI'da geçti görünüyordu).
- 15.10 (tur 2 düzeltmesi, Codex KALDI, 2 madde): `tests/test_sahipler.py` `test_depo_yolu_denetimi` içinde normal `not.md` için `AKIS.md` girdisi ve `not.md:1: AKIS.md` beklentisi geri kondu (eski istisnaya bağlı değildi); kaldırılan AKIS istisnasını koruyan `test_akis_istisnasi_kaldirildi_eksik_akis_md_hatadir` eklendi (eski istisna geçici geri konunca kırmızı, kaldırılınca yeşil).
- 15.10 (hata düzeltmesi, PR 23 sonrası, GitHub Codex P2): `tests/atif_araclari.py` `sahip_tablosu` `A-yapi-bolge.md … E-risk-cikis-surec.md` aralığını yalnız iki uç dosya ve klasöre çeviriyordu; aradaki sahip (B, C, D) silinse ya da adı değişse sahip-var testi yeşil kalıyordu. Aralık artık her harfi denetler (`<H>-*.md`; eşleşen hepsi, hiç yoksa `docs/kurallar/<H>-*.md` yok diye raporlanır). Yeni test `test_aralik_her_harfi_denetler_eksik_ara_sahip_yakalanir`; `test_tablo_yollari_ayiklanir` beklentisi aradaki üç harfi içerir.
