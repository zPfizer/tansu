# Coding standards

The general coding rules are in the global `~/.claude/CLAUDE.md`. This file holds only the rules that real mistakes taught.

## Mistakes
This file starts short. It grows from real mistakes.
- When an agent makes a meaningful coding mistake, record it before the task ends. A mistake is meaningful when Levent corrects it, or when a review or CI finds it.
- For a mechanical mistake, use an existing tool first: `permissions.deny` or a git check. Write a new script only when the same mistake repeats and no existing tool covers it. Do not write a Claude hook. Do not add a rule here.
- For a judgement mistake, add one short rule here. Put a rule for one project only in the `CODING_STANDARDS.md` of that project.
- **Rule of two:** A judgement rule needs two recorded occurrences. Record the first as a dated line under "## Seen once" without a rule. Exceptions: a direct order from Levent, and a risk to data, security, or privacy. These become a rule at once.
- Write corrections to behavior or communication in the brain Kurallar, not here.
- At the end of a difficult session, AKIS B "Lesson" finds the mistakes that nobody recorded.

## Rules
- **Fail loud:** Stop with an error and a non-zero exit when the code cannot complete the requested operation. Do not continue in a weaker mode. (05.10: Tansu `kayit.py` changed an official run to a development run on a dirty tree. 07.10: a hook exited 0 on errors. 07.10: an eval script ignored a subprocess exit code.)
- **Check every item:** Check every record and each required item by its identity. (05.10: Tansu `kaynak.py` checked only the first record. 10.10: Tansu `dod_kontrol.py` checked a count only. 10.10: a git hook matched raw JSON instead of the parsed command.)
- **A check needs the work:** Make the check fail when the required work is missing. (09.10: a PDF reading tool stored the answer codes in the manifest, so the check passed without opening the pages.)
- **One path to outside services:** Send every text to an external service through the same masking function. Check that the response comes from the expected model. (08.10: a hook sent raw text to Jev, bypassed the shared masking function, and did not check the model.)
- **Read the target before you dictate a fact:** Read the file first. Then write a fact about it into a job prompt or a callout. Use the claim of the file. (14.10: a prompt dictated "version 3.0" for a note whose line 13 said "v3.5.1 + 12 commits". The auditor failed the round. 15.10: an audit prompt said 47 sampled lines. The records held 56.)
- **Sample before the full run:** Before a batch job runs on all items, run it on a sample. Read the distribution of the output. Then run the full set. (14.10: a tag job flagged 251 of 503 notes because of a loose flag rule. A 25-note sample would have shown it.)
- **Wire it and run it:** Connect each new hook, command, or module to the live path in the same change. Show one real run through that path. (07.10: a new hook was not in `settings.json`. 05.10: the Tansu CLI read result keys that the change removed.)

## Seen once
- 15.10: 9 writer and 11 reader subagents cut note bodies (`head -c`, `cut -c`, `x[:400]`) and still reported "Notes read: N". The Codex auditor found it in round 2. A reader prompt names a full-print command and the main agent checks the reported line and character counts with a script.

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
