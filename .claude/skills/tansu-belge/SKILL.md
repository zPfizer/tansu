---
name: tansu-belge
description: "Use when the user asks to write, change, or translate a rule, a document, or an instruction in Tansu: GLOSSARY.md, docs/TASARIM.md, docs/KURALLAR.md, AGENTS.md, CODING_STANDARDS.md, DEFINITION_OF_DONE.md, a skill file, an agent file, or a prompt. It runs flow C in order: Write for agents, Record, Language, Result, Locked file, and Translation."
---

# Rule, document, instruction (flow C)

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks.

1. **Write for agents:** `mattpocock-skills:writing-for-agents`.
2. **Record:** `mattpocock-skills:domain-modeling`. `tansu-yeni-is` "Document first" says where a term and a decision go.
3. **Language:** Write instruction and prompt text in English: `asd-ste100`.
4. **Result:** Write the result to the brain as `tansu-yeni-is` "Close" says.
5. **Locked file:** A locked file has feature scope (AGENTS.md "Scope").
6. **Translation:** For a translation of a rule file, the writer lists every dropped word. The auditor compares each rule with the source rule. (Levent 14.10)

| If | Then |
|---|---|
| the work is a workflow spec | `loop-me`. |
| the work is a new skill | `anthropic-skills:skill-creator`, then `tansu-eval` "Skill trigger eval". |
| the work is a Claude interface mode or hook | `plugin-authoring`. |
| the document is long | `anthropic-skills:doc-coauthoring`. |
| the change affects behavior | run `tansu-eval` "Add the case" and `tansu-eval` "Check the judge". |
