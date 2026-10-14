# Tur 4, madde 7: words dropped in the translation, and sentence splits

Source: `.scratch/harness-hizasi-1410/eski/`. Line numbers are the source line numbers.
"Dropped" means a word or phrase of the Turkish source that has no counterpart in the English text.

## AGENTS.md

### Dropped
- none. Each Turkish word has a counterpart. Changes of form that keep the meaning:
  - L7 "vardır", L21 "-dedir" (copula endings): grammar only, the English uses "has"/"covers".
  - L14 "Ham kaynaktır, değiştirilmez", L21 "düzeltilir", L37-39 "hesaplanır/hesaplanmaz/yazılır", L41-42 "eklenir/düzenlenmez/silinmez",
    L45 "silinmez", L50 "kapalı kurulur", L53 "kapalı kurulur ... açılır", L55 "yazılır": impersonal passive became an imperative
    ("Do not change it", "Correct a file", "Calculate", "Only append", "Do not delete", "Install ... disabled", "enable it", "Write").
  - L41 "her sınama koşusu `kayit/deneme.jsonl`'e yazılır": passive became active with the run as subject ("Each backtest run writes to").
  - L68 "Bilet 08 bitince bu satır kalkar": "kalkar" (goes away) became the imperative "delete this line".
  - L24 "belge sessizse" became "the document says nothing about the case" (explicit, no ellipsis).
  - L34 "Testler yalnız TASARIM'daki yüzlerden" has no verb. The English adds "Write ... against" (no ellipsis).
  - L43-44 "yok" (list of git commands) became "Do not use".

### Added glosses (no rule added)
- Headings: "Documents and owners (Belgeler ve sahipleri)", "Working rules (Çalışma kuralları)", "Standards (Standartlar)",
  "Work flow (İş akışı)". The Turkish heading stays in parentheses as the anchor for references.
- Working-rules labels: English label with the Turkish label in parentheses (referenced in `docs/sorgu/izleme/` and `plan.md`).
- "Geliştirme durdu (development stopped)". Tansu terms in parentheses on first use: sınama, aile, havuz, sadakat, yüzler,
  sadakat kontrolü, getiri, deneme günlüğü, sınama koşusu, taban, deneme, beyin.
- L3 "Tansu'dan esinlenen ... sistemi" (noun phrase, no verb) became "TANSU is ... system for BIST. Tansu inspired it."
- L13 "YORUM'lar" became "the YORUM entries".

### Sentence splits and merges
- L3: one noun phrase became two sentences. L3-4: "Kod belgelere uyar; belge değişmeden davranış değişmez." split at the semicolon.
- L7: "Her bilginin tek sahip dosyası vardır; öteki dosyalar yalnız atıf verir." split at the semicolon.
- L12: table cell "sayı, formül, davranış ve kararlar; §7 uygulama sırası" split into two sentences.
- L14: table cell "Ham kaynaktır, değiştirilmez" split into two sentences.
- L21-22: one sentence became two ("The drift check covers all these files." and "Correct a file when ...").
- L24: one sentence became four ("..., stop.", "Correct the document first.", "Write the reason.", "Then write the code.").
- L27: one line with a semicolon became five sentences.
- L29-31: "Yollar `pathlib`; her dosya ..." split at the semicolon.
- L32-33: kept as two sentences.
- L34: "önce kırmızı test, sonra en az kod." became two sentences.
- L35-36: one list of four prohibited actions became four "Do not" sentences.
- L38: one sentence became two ("Calculate ... by hand." and "Do not calculate them again ...").
- L40: one sentence became two ("... in the fidelity check (sadakat kontrolü)." and "Do not calculate it when you select a YORUM.").
- L41-42: "Günlük yalnız eklenir; düzenlenmez ve silinmez." became three sentences.
- L43-47: the git-command list sentence and "dosyalar adıyla eklenir" became two sentences. "Veri ... git'e girmez; `veri/` silinmez." split at the semicolon.
- L48-53: "Kurulum, bir kez, PowerShell (...): ..." became one imperative sentence. "Tanım kapalı kurulur (...); ilk resmi koşudan sonra ..." split at the semicolon.
  "kapalı kurulur, bilet 15'te `TansuGunluk` ile birlikte açılır" became two sentences.
- L55-56: kept as two sentences.
- L59-60: "... başlar; altlarındaki `## Tansu` bölümü Tansu'nun ekidir." split at the semicolon.
- L66-68: "... arınana kadar ... yeni geliştirme yapılmaz; ... yürür" became three sentences ("Do not start ...", "This rule stays until ...", "The tickets ... continue").
- L78: English line, split at the semicolon (STE Rule 8.1).

## CODING_STANDARDS.md (`## Tansu` only)

Line numbers are the HEAD line numbers (`## Tansu` at L23). In `eski/CODING_STANDARDS.md` the shared part above is older and
shorter, so the same lines are 3 lower (`## Tansu` at L20). The `## Tansu` text is the same in both.

### Dropped
- none. Changes of form that keep the meaning:
  - L24 "burada ... durur" became "This section holds".
  - L25 "eklenir", L26 "yazılmaz", L33 "bakılır", L34 "yazılmaz/yazılır", L36 "yazılmaz; atıf verilir": impersonal passive became an imperative.
  - L27-28 "tahminle doldurma, sessiz kırpma ve sessiz atlama yok" became three "Do not" sentences.
  - L30 "hüküm" became "statement". L31 "bir uygulayıcısı ve bir testi" became "one enforcer and one test".
  - L34-35 example: "bizim seçimimiz Tansu'nunmuş gibi yazılmıştı" (pluperfect passive) became "the glossary showed our choice as the choice of Tansu" (simple past, active).
  - L37 "yeniden yazmıştı" (pluperfect) became "wrote ... again" (simple past).
  - L39 "kurulunca" became "When the work is in place".

### Added glosses (no rule added)
- Each bold label has an English name with the Turkish label in parentheses.
- "The backtest (sınama)" on L26.

### Sentence splits and merges
- L24: "... sahibi `docs/TASARIM.md`'dir; burada ..." split at the semicolon.
- L26: "... aynı fonksiyonu kullanır; ayrı kopya yazılmaz" split at the semicolon.
- L27-28: one sentence with a semicolon became four sentences.
- L30-32: the first sentence became two ("TASARIM has statements that say ..." and "For each such statement, the code has ...").
- L33-34: "Fikri varken YORUM yazılmaz; uyulamıyorsa ..." split at the semicolon.
- L36-37: "... yazılmaz; atıf verilir" split at the semicolon.
- L38-39: "Planlanan iş spec ve bilette durur; kurulunca belgeye girer." split at the semicolon.

## DEFINITION_OF_DONE.md (`## Tansu` only)

### Dropped
- none. Changes of form that keep the meaning:
  - L71 "PR'a konur" (passive) became "goes into the PR".
  - L74 "getiriye bakılmadı" (passive) became "nobody looked at the return (getiri)".
  - L74 "deneme günlüğü yalnız eklendi" became "only got new lines".
  - L74-75 "kural parametresi yeni deneme olarak kaydedildi" became "A rule parameter change has a record as a new trial (deneme)". The tense is simple present, and "change" names the case that the rule covers (AGENTS "Kural parametresi").
  - L75 reference "`AGENTS.md` çalışma kuralları" now quotes the heading anchor "Çalışma kuralları".
  - L76 "TASARIM aynı commit'te güncellendi" (passive past) became "the same commit updates TASARIM".

### Sentence splits and merges
- L71: split at the semicolon.
- L72: "yeşil; yeni hesap kapsamında" split at the semicolon.
- L74-75: three clauses joined by semicolons became three sentences.

## .claude/skills/tansu-grill/SKILL.md

### Dropped
- L26 "değişecek fonksiyonun" (the function that will change): "değişecek" has no separate word. It merged into the condition "If code will change" in the same sentence.
- none other. Changes of form that keep the meaning:
  - L3 "konuşulurken kullan" became "Use it when a discussion in Tansu is about ...".
  - L7 "ne zaman bakılacağını" became "when to check them".
  - L17 "uyuyor mu?" and L18 "korunuyor mu?" have no subject. The English adds "the decision" (no ellipsis). L18 passive became active ("Does the decision keep ...").
  - L25 "önceki ve sonraki hâliyle" became "before and after the change". "Karar verilecek her yerde" became "At each decision point".
  - L26 "bugünkü ve önerilen hâlini kısa göster" became "show a short form of the current and the proposed function".

### Added glosses (no rule added)
- Headings in English only ("Tansu comes first", "Risk scan", "Show the text that will change"). No file refers to these headings.
- Tansu terms in parentheses: deneme günlüğü, kural kaydı, deneme, geleceği görme.

### Sentence splits and merges
- L6: "şu üç ölçütü" became "the three criteria below".
- L7: "... sahip dosyalarındadır; bu skill ..." split at the semicolon.
- L11-12: one sentence with a colon and a comma splice became three sentences.
- L16: "şu soruları sor ve cevabını yaz" became two sentences ("ask these questions ..." and "Write the answer:").
- L25-26: kept as two sentences.

## docs/agents/domain.md

### Dropped
- none. The file was English. One change: L19 split at the semicolon ("... or there is a real gap. Note it for ...").

## Semantic substitutions found by audit and corrected

Audit round 1 of tour 4 (KALDI) found these three places.

| File and source line | Source word | First translation | Corrected translation |
|---|---|---|---|
| `AGENTS.md` L66-67 | "yapılmaz" (the development is not done at all) | "Do not start new development that changes the behavior of Tansu. This rule stays until ..." | "Do not do new development that changes the behavior of Tansu until ..." (the two sentences are one sentence again. The L66-68 split above now gives two sentences, not three) |
| `CODING_STANDARDS.md` L33 (HEAD numbering) | "bakılır" (check, the check may find nothing) | "find the idea of Tansu on that subject in the Tansu pool" | "check the Tansu pool for his view on that subject" |
| `.claude/skills/tansu-grill/SKILL.md` L11-12 | "ara" (search, the search may find nothing) | "Find the idea of Tansu on that subject in the Tansu pool and in the rule files. Show the result in the proposal." | "Search the Tansu pool and the rule files for his view on that subject, and show the result in the proposal." (the two sentences are one sentence again) |
