# Harness hizası 14.10: YONETIM refactor'unun Tansu'ya küçük sürümü

Status: done (14.10). Commit'ler: tur 1 6481dec (madde 1); tur 2 809b6e2, 39ac2e3, b56aa9c, 6d6f53d (madde 2, 3a, 3b, 4); tur 3 a229003 + d08a99d (madde 5, 6, bilet 05 notu); tur 4 24e8c3a (madde 7). Denetim (Codex/Astra): tur 1 KALDI→GEÇTİ; tur 3 KALDI→NOTLU GEÇTİ; tur 4 KALDI→KALDI (yanlış bulgu)→GEÇTİ. Test kapısı her commit'te 310/310. YONETIM madde 15 ve 41 kapandı. Önceki plan denetimi: tur 1 KALDI (9), tur 2 KALDI (6), tur 3 KALDI (1, madde 6a); madde 6a düzeltmesini tur 3 denetçisi onayladı.

## Amaç
YONETIM'de 13-14.10'da yapılan kural seçimi (tek sahip, ölü atıf temizliği, ön ekli skill adları, İngilizce STE ajan
metni) Tansu'nun ajan katmanına uygulanır. Ürün belgelerine dokunulmaz.

## Kapsam
- İçinde: `AGENTS.md`, `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md`, `.claude/skills/tansu-grill/SKILL.md`,
  `docs/agents/domain.md`, `docs/agents/issue-tracker.md`.
- Dışında: `docs/TASARIM.md`, `docs/KURALLAR.md`, `GLOSSARY.md`, `docs/kurallar/`, `docs/sadakat.md`, kod (`tansu/`,
  `tests/` içeriği), `kayit/`, CI tanımları, `.gitignore`, `.claude/settings.json`, `.claude/hooks/` (boş klasör;
  temizlik işi, bu planın konusu değil), `.scratch/belge-hizasi/` biletleri. Bunlar belge hizası işinin (02, 03, 04,
  07, 08) ve mimari işinin konusudur.
- Tek istisna: belge hizası bileti 05'in (ajan belgeleri güncel) `## Comments` bölümüne tek satır not eklenir:
  "skill adları, ADR anlatımı ve tek sahip düzeltmeleri harness hizasında yapıldı (commit no); Status sözleşmesi,
  `docs/denetim.md`, araştırma notları ve 05.10 raporu açık." Biletin başka satırı değişmez; bilet kapanmaz.

## Maddeler (bağımlılık sırasıyla)
| # | İş | Kabul ölçütü | Kanıt | Kapsam |
|---|---|---|---|---|
| 1 | Ortak standart kopyaları: `CODING_STANDARDS.md` ve `DEFINITION_OF_DONE.md` ortak kısmı YONETIM'dekiyle aynı; `## Tansu` eki değişmez | `tests/test_standartlar.py` 3/3 yeşil; `## Tansu` bölümünün değişiklik öncesi ve sonrası diff'i boş (iki dosya için ayrı ayrı) | pytest çıktısı, diff çıktısı | özellik (kilitli dosya) |
| 2 | `tansu-grill` skill'i: `grilling` → `mattpocock-skills:grilling`, `domain-modeling` → `mattpocock-skills:domain-modeling` | Dosyada ön eksiz skill adı 0; iki ön ekli ad var | grep | görev (1 dosya) |
| 3a | `docs/agents/domain.md`: `/domain-modeling`, `/grill-with-docs`, `/improve-codebase-architecture` ön ekli; `docs/adr/` anlatımı Tansu düzenine çevrilir ("ADR yok; kararlar TASARIM'da, gerekçe `docs/sorgu/`'da") | Üç ad için grep: eski 0, yeni 1+; `docs/adr` geçişi 0 | grep | görev (1 dosya) |
| 3b | `docs/agents/issue-tracker.md`: `/wayfinder` → `mattpocock-skills:wayfinder` | grep: eski 0, yeni 1 | grep | görev (1 dosya) |
| 4 | `AGENTS.md` tablosu: `docs/kurallar/A-E` satırındaki "yerel, git dışı" kalkar; dosyalar git'te kalır (Levent kararı 1) | Tablo ile `git ls-files docs/kurallar` (5 dosya) aynı şeyi söyler | git ls-files, okuma | görev (1 dosya) |
| 5 | `AGENTS.md` skill adları: Matt skill adları kalkar, yerine AKIS adım atfı ("Standartlar" bölümündeki `code-review` ve "İş akışı" bölümündekiler dahil). Kalan: `/tansu-grill` (Tansu'nun eki) ve `wait-what` satırı (Levent 13.10, YONETIM madde 31) | Dosya genelinde `mattpocock-skills:` geçişi yalnız `wait-what` satırında; her kaldırılan ad için AKIS adım numarası var | grep, satır listesi | özellik (davranış değişir) |
| 6 | `AGENTS.md` tek sahip: (a) "Hata kaydı" paragrafı: genel kural cümleleri (tanım, mekanik hata, "hemen kaydet") `CODING_STANDARDS.md` "Mistakes" bölümüne atıf olur; Tansu'ya özgü tek cümle kalır ("reasoning error `## Tansu` altına"); retro cümlesi de atfa döner (sahibi CODING_STANDARDS "Mistakes" son satırı). Çelişki giderilir: AGENTS "mekanik hata teste ya da CI'a gider", CODING_STANDARDS "önce var olan araç". (b) "Agent skills" üç alt bölümü yalnız `docs/agents/` dosyasına atıf taşır. (c) "Plan" satırındaki spec ve bilet yolları kalkar, `docs/agents/issue-tracker.md` atfı kalır | (a) paragrafta atıf 1, Tansu'ya özgü tek cümle var, genel kural cümlesi 0; (b) her alt bölüm tek atıf satırı; (c) satırda `.scratch/` yolu 0, atıf 1 | okuma, grep | özellik |
| 7 | Dil: 1-6 bittikten sonra ajan metinleri İngilizce STE: `AGENTS.md`, `CODING_STANDARDS.md` `## Tansu`, `DEFINITION_OF_DONE.md` `## Tansu`, `tansu-grill/SKILL.md`, `docs/agents/domain.md`. Türkçe tetik sözcükleri tırnak içinde kalır. Yazıcı düşen her sözcüğü listeler (AKIS C.11); denetçi her kuralı kaynak kuralla karşılaştırır. Eski metin `.scratch/harness-hizasi-1410/eski/` altında | `asd-ste100` lint 0 ihlal; 5 dosyada Türkçe karakter yalnız tırnaklı tetik sözcüklerde; düşen sözcük listesi var ve denetçi her satırını onayladı | lint çıktısı, grep, liste | özellik (kilitli dosya) |

## Tur düzeni (AKIS I)
Her tur ayrı iş: kendi yazıcısı, kendi denetimi, kendi commit'leri. Her commit öncesi
`.venv\Scripts\python.exe -m pytest -q` yeşil (AGENTS "Test kapısı"). Bugün 2 test kırmızı; bu yüzden madde 1 ilk turdur.
- Tur 1: madde 1. Özellik kapsamı (kilitli dosya). Yazıcı: Claude alt ajanı. Denetçi: Codex, en çok 3 tur.
- Tur 2: madde 2, 3a, 3b, 4. Görev kapsamı: her biri tek dosya, kodsuz, 20 satırın altında (AKIS "Who writes"). Yazıcı: orkestratör. Denetçi yok; kanıt commit mesajında. Her madde ayrı commit.
- Tur 3: madde 5, 6 ve bilet 05 notu. Özellik kapsamı. Yazıcı: Claude alt ajanı. Denetçi: Codex, en çok 3 tur.
- Tur 4: madde 7. Özellik kapsamı. Yazıcı: Claude alt ajanı. Denetçi: Codex, en çok 3 tur.
- Bir turun 3. denetimi KALDI ise iş durur, kök neden Levent'e bir satır.

## Levent'e sorular (onaydan önce)
1. Madde 4: `docs/kurallar/A-E` git'te kalsın mı? Öneri: kalsın; dosyalar Tansu'nun ham paylaşımı değil, bizim okumamız.
2. Madde 1: `DEFINITION_OF_DONE.md` `## Tansu` eki kalsın mı? Öneri: kalsın; YONETIM madde 15 (ENGEL) bu kararı bekliyor.

## Riskler
- Madde 5: skill adı kalkınca ajan adımı AKIS'te bulamazsa yavaşlar. Önlem: her kaldırılan ad yerine AKIS adım numarası.
- Madde 7: çeviride kural anlamı kayarsa davranış değişir. Önlem: düşen sözcük listesi, denetçi kural kural karşılaştırır, eski metin saklanır.
- Madde 1 sonrası YONETIM metni yine değişirse test yine kırmızı olur. Bu testin amacıdır; refactor dışı.

## Yapılmayacaklar
- Bitmiş bilet arşivi yok: biletler numarayla birbirine bağlı (`Blocked by: 01, 02`); Tansu kuralı bütün iş bitince spec ve biletleri birlikte arşivler.
- `AGENTS.md` "Geliştirme durdu" satırı kalkmaz (bilet 08'e bağlı).
- `docs/kurallar/A-E` git'ten çıkarılmaz (kapsam dışı dosya).
- Boş `.claude/hooks/` klasörüne dokunulmaz.
- Yeni test, kanca, betik, CI adımı yok.
- Ürün belgeleri (TASARIM, KURALLAR, GLOSSARY, kural dosyaları) değişmez.
