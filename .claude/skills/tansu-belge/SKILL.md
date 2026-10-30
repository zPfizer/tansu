---
name: tansu-belge
description: "Use when the user asks to write, change, or translate a Tansu rule, document, or instruction. This includes GLOSSARY.md, docs/TASARIM.md, docs/KURALLAR.md, AGENTS.md, CODING_STANDARDS.md, DEFINITION_OF_DONE.md, a skill file, an agent file, or a prompt. Flow C starts with Locked file, Write for agents, Record, Language, and Translation. Applicable checks come before Result."
---

# Rule, document, instruction (flow C)

Scope: the main checkout. The `yeniden-kurulus` worktree has no `docs/agents/`; there, follow its `AGENTS.md`.

Use AGENTS.md "Work flow" for the writing method. Run the applicable steps below in order.
Use [Scope](../../../docs/agents/is-kurallari.md#scope) to distinguish local work from publication.
Use [Check and evidence](../../../docs/agents/is-kurallari.md#check-and-evidence) for every change and the later delivery steps when applicable.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).
Set `$tansuPython` to the main interpreter path in [Branch](../../../docs/agents/is-kurallari.md#branch) for the commands below.

1. **Locked file:** Choose the scope from docs/agents/is-kurallari.md "Scope" before writing.
2. **Write for agents:** State who acts, what they do, and what result they must check. Keep conditions and exceptions explicit.
3. **Record:** Apply `tansu-yeni-is` "Document first" for settled terms and decisions.
4. **Language:** Write instruction and prompt text in English with `asd-ste100`.
   Run `& $tansuPython -X utf8 kurulum/ste_fark.py origin/main`. It checks added instruction lines since the merge base.
   For a new file, the checker requires named staging (`git add <file>`). If staging is outside scope, report this limitation.
   The required check exit code is 0.
5. **Translation:** For a translation of a rule file, the writer lists every dropped word. If risk requires a reviewer, the auditor compares each rule with the source rule. (Levent 14.10)

Complete the applicable conditional checks and pool rules below before Result.
Then complete [Check and evidence](../../../docs/agents/is-kurallari.md#check-and-evidence) and any required [Review](../../../docs/agents/is-kurallari.md#review) before Result.

| If | Then |
|---|---|
| the work is a workflow spec | Define the actor, inputs, steps, stop conditions, and required evidence. Check each path for missing decisions. |
| the work is a new skill | Use the available file tools to write SKILL.md with a name, description, trigger conditions, and steps. Check its frontmatter and referenced paths. Then run `tansu-eval` "Skill trigger eval". |
| the work is a Claude interface mode or hook | Read the official documentation for the active interface. Use its available configuration and shell tools. Check the event, input, output, and failure exit in isolation. |
| the document is long | Make an outline. Write one section at a time with the available file tools. Check consistency and source references across sections. |
| the change affects behavior | Run `tansu-eval` "Add the case". Run `tansu-eval` "Check the judge" only if the evaluator uses an LLM judge. |
| a pool batch appends to `docs/kurallar` under a supplied brief | Skip Write for agents, Record, Language, and the long-document row. Apply "Pool reading rules" and [Check and evidence](../../../docs/agents/is-kurallari.md#check-and-evidence). Apply the shared delivery steps within scope. |

## Pool reading rules
These rules bind the readers and the writers of a pool batch. They also bind a document correction from the pool.
1. Apply `CODING_STANDARDS.md` "Read the whole note".
2. A sentence that says what Tansu says, starts with "Kural:", or ends with "sayılır" is followed by a verbatim quote. Without a quote, it starts with "Okuma (YORUM):".
3. A step that the note does not write starts with YORUM.
4. When `## Görsel metni` is empty or absent, open the image with the available image viewer.
   A delegated reader must have tools to write its record. Assign pool record production to a role with those tools.
   For small text, open an enlarged crop with the available local tools.
   The `okuyucu` subagent cannot crop (`.claude/agents/okuyucu.md`). It returns "okunamıyor" and the image path for the main agent to crop.
   If the 4x crop is not clear, write "okunamıyor". Never fill a cell from another cell.
   Never derive a number from a chart axis. Never use the Browser tool.
5. Do not add your own note into verbatim text.
6. Copy note names and ids from the record files or the pool. Never type them.
7. A claim that something is empty or missing carries the search command and its output line.
8. A writer brief has no fixed section number. Search headings that match `^## [0-9]` and use the highest number. When a new section refutes an old "yok" or "verilmemiş" sentence, list all hits with `git grep -n -i <word> docs`. Mark each hit "uyumlandı" or "ilgisiz".
9. Do not use `replace_all` in a document. Read each hit.
10. A `yok` reason that says there is no threshold needs a search of the Ham text and the images for a number or a period first.
11. Every reader record has `gorsel_acildi` (true or false) and `belirsiz` (true or false). The review sample contains every record with `belirsiz: true`. A PR sentence about opened images counts only the records with `gorsel_acildi: true`.
12. Before the PR, run `& $tansuPython -X utf8 tests/atif_araclari.py alinti <records>`.
    Also run `& $tansuPython -X utf8 tests/atif_araclari.py alinti-belge origin/main` for added document quotes.
    Stage a new document by name before that run because the command reads tracked files only.
    Both commands must print 0 lines. Otherwise, the PR lists each remaining line with its own reason, such as "etiket, alıntı değil".
    Never pass a group of lines together.
    Write `ek` and `yok` records with `& $tansuPython -X utf8 tests/atif_araclari.py entegre <tarih> <records>`.
    Run `tests/test_havuz.py` with the main interpreter and `-X utf8 -m pytest`.
    Set `TANSU_BEKLENEN_ACIK` and `TANSU_PARTI` for the real pool test.
13. Every open question of a reader or a writer appears in the PR as "taşındı: <place>" or "düştü: <reason>".

## Result

Apply [Close](../../../docs/agents/is-kurallari.md#close) within the job scope.
