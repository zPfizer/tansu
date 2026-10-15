# Work flows (İş akışı)

This file owns the work flows of Tansu, the skill placement, the scope levels, who writes, and the auditor rules. Only `AKIS.md`, `DEFINITION_OF_DONE.md`, `docs/agents/`, and the skill files under `.claude/skills/` name skills. Other files refer to an AKIS step by its title (for example AKIS A "Review"), never by its number.

Choose flow A or B by the work type. Call each skill by the exact name in backticks. Run the steps in order. Run an "If" row only when its condition is true.

## 0. Every job
1. Write the intent of Levent and the flow (A or B) in one line at the top of the first reply.
2. Read AGENTS.md "Current state" (Şimdiki durum).
3. Send a design or technical question that needs the preference of Levent to the `vekil` subagent first. Levent gets only these: direction of the project, money, outgoing work, secrets, delete, and work that cannot be undone.
4. Before you write an instruction or a prompt: `asd-ste100`.
5. If you cannot show a source for a claim: `thinking-circle-of-competence`.
6. If the problem type or the method is unclear: `thinking-cynefin`, then `thinking-model-router`.
7. Choose the scope (section "Scope").

## A. New work (Yeni geliştirme)
1. **Sharpen:** `/tansu-grill` (the `vekil` subagent answers).
2. **Document first:** Write a settled term to `GLOSSARY.md` at once. Write a decision to `docs/TASARIM.md`. Read `docs/TASARIM.md` first. Read `docs/sorgu/` when it exists. It is local and not in git. Do not ask again for a decision that exists. For a document-code conflict, apply AGENTS.md "Belgeler ve sahipleri".
3. **Spec:** `mattpocock-skills:to-spec`.
4. **Tickets:** `mattpocock-skills:to-tickets`, then `mattpocock-skills:triage`. The layout is in `docs/agents/issue-tracker.md`. Do not write a ticket by hand. If a new decision appears during the work, update the spec first. Then build the tickets again in dependency order.
5. **Branch:** Use one branch `pr/NN-<ad>` from `master` for each ticket. Give it its own worktree: `git worktree add ../TANSU-bNN -b pr/NN-<ad> master`. Clear the context between tickets.
6. **Build:** For one ticket: `mattpocock-skills:implement`. For a full spec: `mattpocock-skills:implement-spec`. AGENTS.md "Önce test" owns the red-test rule. The skill is `mattpocock-skills:tdd`. While you write code: `ponytail:ponytail`. A subagent writes the code. A writer subagent writes only inside its own worktree. Add logs and measurements for each new critical path (DEFINITION_OF_DONE.md "Ship-readiness").
7. **Test gate:** Run these from the main venv `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`: `-m pytest -q`, `-m ruff check .`, and `-m ruff format --check .`. Run `git diff --check`. All must be green before each commit.
8. **Review:** Merge `master` into the branch first. Then run `mattpocock-skills:code-review` (a Claude subagent). Then run the Codex audit (subagent type `codex`) and add the text of the code-review skill to the auditor prompt. After a change in a calculation, search all prose in the changed modules that states the formula (docstrings, comments, report text, HTML). Tie each one to its TASARIM sentence. When the coverage of a test changes, update the owning TASARIM sentence in the same commit.
9. **Proof:** `verification-before-completion`, and the `## Tansu` items of `DEFINITION_OF_DONE.md`.
10. **Pull request:** Push the branch to `kaynak`. `mattpocock-skills:pr` and `.github/pull_request_template.md` write the PR body together.
11. **Merge:** Merge when two things are true. CI is green (`ci`: ruff and pytest. `dod`: the PR body). The audit verdict is GEÇTİ or NOTLU GEÇTİ. Claude merges with `gh pr merge --merge`. Levent gets only the completion note (Levent 15.10).
12. **Close:** Move the spec and the tickets of a finished job to `.scratch/arsiv/`. Only GLOSSARY and TASARIM stay for good. Write the result to the brain with the `beyin` skill (Threads and a receipt).

Task scope skips Sharpen, Spec, and Tickets. It runs Build, Test gate, and Proof. Task scope has no auditor (section "Scope"); for a locked file, "Who writes" sets the review.

| If | Then |
|---|---|
| the work does not fit one session | start with `mattpocock-skills:wayfinder`. |
| the request is unclear | `thinking-socratic` (the `vekil` subagent answers). |
| the work is risky | `thinking-pre-mortem`. If it has side effects: `thinking-second-order`. |
| an urge to add something | `thinking-via-negativa`. |
| a step only a human can do | `mattpocock-skills:wizard`. |
| the code has bloat | `ponytail:ponytail-review`. If a function is complex: `cyclomatic-complexity`. |
| the work includes untrusted input (for example downloaded data) or permissions | `thinking-red-team`. |
| the work changes an HTML report | show the proof with `anthropic-skills:built-in-browser`. |

## B. Bug fix (Hata düzeltme)
1. **Diagnose:** `mattpocock-skills:diagnosing-bugs`.
2. **Red test:** `mattpocock-skills:tdd`.
3. **Fix:** A subagent writes the minimum code in its own branch (as A "Branch").
4. **Test gate:** As A "Test gate".
5. **Review:** As A "Review".
6. **Proof:** As A "Proof".
7. **Pull request and merge:** As A "Pull request" and A "Merge".
8. **Lesson:** `mattpocock-skills:retro`. Record the mistake as `CODING_STANDARDS.md` "Mistakes" says.

| If | Then |
|---|---|
| a document and the real state disagree | `thinking-map-territory`. |
| the fault repeats | `thinking-five-whys-plus`. |
| there are several possible causes | `thinking-scientific-method`. |
| a defect is selective | `thinking-kepner-tregoe`. |
| the problem is slowness | `thinking-theory-of-constraints`. |
| a fix breaks another part | `thinking-systems`. |

## Scope
- Task: the "Per task" item of DEFINITION_OF_DONE.md "How to Apply". The agent gives its own proof. No auditor. AGENTS.md "Önce test" applies to every code change, also to a one-line change.
- Feature (several jobs, a behavior, or an interface): the "Per feature" item of DEFINITION_OF_DONE.md "How to Apply", added to the task items. Run one independent auditor run.
- Outgoing work (push, pull request, delete, archive): the full checklist. Use an auditor.
- Work without code (`.scratch` notes): skip the code items. No auditor.
- Locked files: `AGENTS.md`, `AKIS.md`, `CODING_STANDARDS.md`, and `DEFINITION_OF_DONE.md`. They have feature scope at any size, except as "Who writes" says.

## Who writes
- One file, under 20 lines, no code: the orchestrator writes it itself.
- A locked file, at any size: a subagent writes it and the Codex auditor checks it. Exception (Levent 14.10): Levent approves the change in chat.
  - One added line has task scope. The orchestrator writes it and searches the other files for a second copy of the rule. No auditor.
  - A change of 2 to 3 lines gets one `mattpocock-skills:code-review` pass by a Sonnet subagent on the diff. It gets no Codex audit.
  - A change of more than 3 lines needs a writer subagent and the Codex auditor.
- Code: a subagent writes it.

## Auditor and rounds
- The auditor is a different agent from the writer.
- The auditor also checks that the writer followed the steps of `AKIS.md`.
- The auditor of a delete or archive job checks the final file list, the links, and the changes outside the scope.
- The verdicts are GEÇTİ, NOTLU GEÇTİ, and KALDI. NOTLU GEÇTİ: low-risk test gaps and style notes. KALDI: a false claim, a broken behavior, a missed instruction, or a security or privacy risk. An audit without a verdict counts as KALDI.
- Feature and outgoing scope: at most 3 audit rounds. Every audit prompt names the round number. The auditor gives the round number with the verdict.
- If round 3 returns KALDI (failed): stop the job. Do not open a fourth round. Find the root cause and define the job again. Send Levent the root cause in one line.
- Add the items that an auditor finds to the source report. A report is complete only after a re-audit passes.
- If the Codex sandbox fails with `CreateProcessWithLogonW 1909`, a small round may go to a Sonnet subagent.

## Session
- Long work: `chief-of-staff`.
- To give the work to a new session: `mattpocock-skills:handoff`.
- Levent says "anlamadım": `mattpocock-skills:wait-what`. Then explain again with GLOSSARY terms and plain words.
