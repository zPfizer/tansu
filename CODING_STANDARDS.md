# Coding standards

The general rules are in `C:\Users\levent\Desktop\YONETIM\beyin\knowledge\concepts\kod-standartlari-genel.md`. Read it before this file; it wins on general rules. This file holds only the Tansu rules (section "## Tansu").

## Tansu
This section adds to the general standard. `docs/TASARIM.md` owns the behavior rules. This section holds how to apply
them when you write code.
- **No look-ahead (Geleceği görmeme):** Add each new or changed calculation to the scope of `tests/test_gelecek.py`
  (TASARIM §5.12).
- **One code (Tek kod):** Do not write a second copy of a function that TASARIM §4 (`motor`) shares between the
  backtest (sınama) and the live run.
- **No silent correction (Sessiz düzeltme yok):** Do not fill, clip, or skip silently. An unexpected condition gives an
  error. The behavior for a missing value is in TASARIM §5.1.
- **Follow the document (Belgeye bağlılık):** Each new or changed behavior has a `TASARIM <bölüm>` reference in the code.
- **Invariant rule (Değişmez kural):** TASARIM has statements that say a thing never happens or always happens
  (examples: "anlık görüntü değişmez", "ileri doldurulmaz", "indirme durur"). For each such statement, the code has one
  enforcer and one test. A new statement comes with both.
- **Tansu comes first (Tansu önce gelir):** Before you write a rule, a value, or a definition, check the Tansu pool for his
  view on that subject. If Tansu has an idea, do not write a YORUM. If you cannot follow the idea, write
  "uygulanamaz" and the reason (KURALLAR "Okuma kuralları"). (10.10: in 11 places in the glossary, Tansu had an idea,
  but the glossary showed our choice as the choice of Tansu.)
- **Give a reference, do not copy (Atıf ver, kopyalama):** Apply AGENTS.md "Belgeler ve sahipleri". (10.10: the glossary
  wrote the formulas of TASARIM again.)
- **Do not write a missing thing as if it exists (Olmayanı var gibi yazma):** The documents describe only what exists
  today. Planned work stays in the spec and the ticket. When the work is in place, it goes into the document.
- **Open the source before a new fact (Kaynağı aç):** Before you write a new fact sentence in a document, open the Ham line or the image. If you cannot find it, write "okunamıyor" or YORUM. (16.10: a correction wrote a new unsupported sentence into TASARIM three times. 16.10: a batch reading wrote three claims that the source does not state, without YORUM.)
- **Read the whole note:** A reader reads each note with `Read`, without `offset` or `limit`. It never cuts a note with `head`, `cut`, `sed -n`, or a slice. It reports the line count, and the main agent checks the count with `wc -l`. (15.10: 9 writer and 11 reader subagents cut note bodies and still reported "Notes read: N". 16.10: a document correction made 25 cut Ham reads. 16.10: a reader prompt named no full-print command.)
- **Define the boundary before the code (Sınırı önce tanımla):** For a new calculation, write in TASARIM what happens on the period's first and last day, on a quarantined day, and with a zero, infinite or missing price. Commit order: document, then red test, then code. (16.10: `tansu-sinama` version 1 failed the audit in 3 rounds on exactly these edges: last day, quarantined day, zero or infinite price. Levent 17.10 approved the rule.)
