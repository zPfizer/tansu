---
name: tansu-belge
description: "Use when the user asks to write, change, or translate a rule, a document, or an instruction in Tansu: GLOSSARY.md, docs/TASARIM.md, docs/KURALLAR.md, AGENTS.md, CODING_STANDARDS.md, DEFINITION_OF_DONE.md, a skill file, an agent file, or a prompt. It runs flow C in order: Write for agents, Record, Language, Result, Locked file, and Translation."
---

# Rule, document, instruction (flow C)

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks. The shared steps of `tansu-yeni-is` (Test gate, Review, Proof, Pull request, Merge, Close) also apply when the change goes to a pull request.

1. **Write for agents:** `mattpocock-skills:writing-for-agents`.
2. **Record:** `mattpocock-skills:domain-modeling`. `tansu-yeni-is` "Document first" says where a term and a decision go.
3. **Language:** Write instruction and prompt text in English: `asd-ste100`. Then run `py -3 -X utf8 kurulum/kanca.py ste-fark kaynak/master`. It lints only the added lines of the instruction files. Stage a new file first (`git add <file>`). The exit code must be 0. The hook of AGENTS.md "Environment" blocks an instruction edit before the `asd-ste100` call.
4. **Result:** Write the result to the brain as `tansu-yeni-is` "Close" says.
5. **Locked file:** A locked file has feature scope (`docs/agents/is-kurallari.md` "Scope").
6. **Translation:** For a translation of a rule file, the writer lists every dropped word. The auditor compares each rule with the source rule. (Levent 14.10)

| If | Then |
|---|---|
| the work is a workflow spec | `loop-me`. |
| the work is a new skill | `anthropic-skills:skill-creator`, then `tansu-eval` "Skill trigger eval". |
| the work is a Claude interface mode or hook | `plugin-authoring`. |
| the document is long | `anthropic-skills:doc-coauthoring`. |
| the change affects behavior | run `tansu-eval` "Add the case" and `tansu-eval` "Check the judge". |
| the job reads pool notes into `docs/kurallar` in batches (a brief is given, the job only appends) | do not run the steps Write for agents, Record, and Language. Do not run the row "the document is long". Apply "Pool reading rules" below and the shared steps of `tansu-yeni-is`. The PR has `Akış: tansu-belge`, and `Çağrılan beceriler:` lists `toplu havuz okuma`. |

## Pool reading rules
These rules bind the readers and the writers of a pool batch. They also bind a document correction from the pool.
1. Apply `CODING_STANDARDS.md` "Read the whole note".
2. A sentence that says what Tansu says, starts with "Kural:", or ends with "sayılır" is followed by a verbatim quote. Without a quote, it starts with "Okuma (YORUM):".
3. A step that the note does not write starts with YORUM.
4. When `## Görsel metni` is empty or absent, open the image. Open images with `Read`. The pool reader is a general-purpose subagent, because it writes the record file. For small text, it crops with PIL through a one-line `python -X utf8 -c` and opens the crop. The `okuyucu` subagent cannot crop (`.claude/agents/okuyucu.md`). It writes "okunamıyor" and the image path, and the main agent crops. If the 4x crop is not clear, write "okunamıyor". Never fill a cell from another cell. Never derive a number from a chart axis. Never use the Browser tool.
5. Do not add your own note into verbatim text.
6. Copy note names and ids from the record files or the pool. Never type them.
7. A claim that something is empty or missing carries the grep command and its output line.
8. A writer brief has no fixed section number. The writer finds the highest number with `grep -n '^## [0-9]' <file>`. When a new section refutes an old "yok" or "verilmemiş" sentence, list all hits with `git grep -n -i <word> docs`. Mark each hit "uyumlandı" or "ilgisiz".
9. Do not use `replace_all` in a document. Read each hit.
10. A `yok` reason that says there is no threshold needs a search of the Ham text and the images for a number or a period first.
11. Every reader record has `gorsel_acildi` (true or false) and `belirsiz` (true or false). The review sample contains every record with `belirsiz: true`. A PR sentence about opened images counts only the records with `gorsel_acildi: true`.
12. Before the PR, `python tests/atif_araclari.py alinti <records>` must print 0 lines. Also run `python tests/atif_araclari.py alinti-belge kaynak/master`. It checks the quotes on the added document lines. Stage a new document file (`git add <file>`) before the run, because the command reads tracked files only. Both commands must print 0 lines. Or the PR lists each remaining line one by one with its reason (for example "etiket, alıntı değil"). Never pass a group of lines together. Write `ek` and `yok` records with `python tests/atif_araclari.py entegre <tarih> <records>`. Run the real pool test with `TANSU_BEKLENEN_ACIK` and `TANSU_PARTI` (`tansu-yeni-is` "Test gate").
13. Every open question of a reader or a writer appears in the PR as "taşındı: <place>" or "düştü: <reason>".
