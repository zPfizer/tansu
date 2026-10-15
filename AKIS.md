# Work flows (İş akışı)

Tansu has no flow F (memory) and no flow G (company output). They stay in the brain.

This file owns the work flows of Tansu, the skill placement, the scope levels, who writes, and the auditor rules. Only `AKIS.md`, `DEFINITION_OF_DONE.md`, `docs/agents/`, and the skill files under `.claude/skills/` name skills. Other files refer to an AKIS step by its title (for example AKIS A "Review"), never by its number.

Choose the flow by the work type. The flows are A (new work), B (bug fix), C (rule, document, instruction), and D (plan or decision). The other flows are E (source), H (question), I (session), and J (eval). Call each skill by the exact name in backticks. Run the steps in order. Run an "If" row only when its condition is true.

## 0. Every job
1. Write the intent of Levent and the flow letter in one line at the top of the first reply.
2. Read AGENTS.md "Current state" (Şimdiki durum).
3. If the work type is unclear: `mattpocock-skills:ask-matt`.
4. Send a design or technical question that needs the preference of Levent to the `vekil` subagent first. Levent gets only these: direction of the project, money, outgoing work, secrets, and delete. Levent also gets a Task Scheduler change and work that cannot be undone.
5. Before you write an instruction or a prompt: `asd-ste100`.
6. If you cannot show a source for a claim: `thinking-circle-of-competence`.
7. If the problem type is unclear: `thinking-cynefin`. If the method is unclear: `thinking-model-router`.
8. Choose the flow and the scope (section "Scope").

## A. New work (Yeni geliştirme)
1. **Sharpen:** Define what to build: `thinking-jobs-to-be-done`. Then run `/tansu-grill` (the `vekil` subagent answers).
2. **Document first:** Write a settled term to `GLOSSARY.md` at once. Write a decision to `docs/TASARIM.md`. Read `docs/TASARIM.md` first. Read `docs/sorgu/` when it exists. It is local and not in git. Do not ask again for a decision that exists. For a document-code conflict, apply AGENTS.md "Belgeler ve sahipleri".
3. **Spec:** `mattpocock-skills:to-spec`.
4. **Tickets:** `mattpocock-skills:to-tickets`, then `mattpocock-skills:triage`. The layout is in `docs/agents/issue-tracker.md`. Do not write a ticket by hand. If a new decision appears during the work, update the spec first. Then build the tickets again in dependency order.
5. **Branch:** Use one branch `pr/NN-<ad>` from `master` for each ticket. Give it its own worktree: `git worktree add ../TANSU-bNN -b pr/NN-<ad> master`. Clear the context between tickets.
6. **Build:** For one ticket: `mattpocock-skills:implement`. For a full spec: `mattpocock-skills:implement-spec`. AGENTS.md "Önce test" owns the red-test rule. The skill is `mattpocock-skills:tdd`. While you write code: `ponytail:ponytail`. A subagent writes the code. A writer subagent writes only inside its own worktree. Apply the Observability item of DEFINITION_OF_DONE.md "Ship-readiness".
7. **Test gate:** Run these from the main venv `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`: `-m pytest -q`, `-m ruff check .`, and `-m ruff format --check .`. Run `git diff --check`. All must be green before each commit.
8. **Review:** Merge `master` into the branch first. Then check the change by its type. A change with code: run `mattpocock-skills:code-review` (a Claude subagent). Then run the Codex audit (subagent type `codex`). Add the text of the code-review skill to the auditor prompt. A change to documents only (no code): run one `mattpocock-skills:code-review` pass by a Sonnet subagent on the diff. Run no Codex audit. Both checks read `CODING_STANDARDS.md` and `DEFINITION_OF_DONE.md`. After a change in a calculation, search the changed modules for prose that states the formula. This covers docstrings, comments, report text, and HTML. Tie each one to its TASARIM sentence. When the coverage of a test changes, update the owning TASARIM sentence in the same commit.
9. **Proof:** `verification-before-completion`, and the `## Tansu` items of `DEFINITION_OF_DONE.md`.
10. **Pull request:** Push the branch to `kaynak`. `mattpocock-skills:pr` and `.github/pull_request_template.md` write the PR body together.
11. **Merge:** Merge when two things are true. CI is green (`ci`: ruff and pytest. `dod`: the PR body). The independent verdict is GEÇTİ or NOTLU GEÇTİ. For code, it is the verdict of the Codex audit. For documents only, it is the verdict of the `mattpocock-skills:code-review` pass. Claude merges with `gh pr merge --merge`. Levent gets only the completion note (Levent 15.10).
12. **Close:** Move the spec and the tickets of a finished job to `.scratch/arsiv/`. Only GLOSSARY and TASARIM stay for good. Write the result to the brain with the `beyin` skill (Threads and a receipt). If a branch merged, remove its worktree with `git worktree remove <path>`. Do not use `--force`. If git refuses, stop and tell Levent.

Task scope skips Sharpen, Spec, and Tickets. It runs Build, Test gate, and Proof. Task scope has no auditor (section "Scope"). For a locked file, "Who writes" sets the review.

| If | Then |
|---|---|
| the work does not fit one session | start with `mattpocock-skills:wayfinder`. |
| the request is unclear | `thinking-socratic` (the `vekil` subagent answers). |
| the work is risky | `thinking-pre-mortem`. If it has side effects: `thinking-second-order`. |
| the work is an API | `anthropic-skills:fastapi-patterns`. |
| the work is Claude or Jev code | `claude-api` or `typesafe-ai`. |
| the work is an MCP server | `anthropic-skills:mcp-builder`. |
| two requirements conflict | `thinking-triz`. |
| an urge to add something | `thinking-via-negativa`. |
| a step only a human can do | `mattpocock-skills:wizard`. |
| the code has bloat | `ponytail:ponytail-review`. If a function is complex: `cyclomatic-complexity`. |
| the work includes untrusted input (for example downloaded data) or permissions | `thinking-red-team`. |
| the work changes an HTML report | show the proof with `anthropic-skills:built-in-browser`. |
| the work meets an operational limit or quota (for example a rate limit of a data source) | `thinking-margin-of-safety`. |
| the work is a batch content job with a fixed line rule (map lines, labels, tags) | use task scope: skip Sharpen, Spec, and Tickets. The job prompt holds the rule and the proof. (Retro 15.10) |

## B. Bug fix (Hata düzeltme)
1. **Diagnose:** `mattpocock-skills:diagnosing-bugs`.
2. **Red test:** `mattpocock-skills:tdd`.
3. **Fix:** A subagent writes the minimum code in its own branch (as A "Branch").
4. **Test gate:** As A "Test gate".
5. **Review:** As A "Review".
6. **Proof:** As A "Proof".
7. **Pull request, merge, and close:** As A "Pull request", A "Merge", and A "Close".
8. **Lesson:** `mattpocock-skills:retro`. Record the mistake as `CODING_STANDARDS.md` "Mistakes" says.

| If | Then |
|---|---|
| a document and the real state disagree | `thinking-map-territory`. |
| the fault repeats | `thinking-five-whys-plus`. |
| there are several possible causes | `thinking-scientific-method`. |
| a defect is selective | `thinking-kepner-tregoe`. |
| the problem is slowness | `thinking-theory-of-constraints`. |
| a fix breaks another part | `thinking-systems`. |
| the problem changes while you work | `thinking-ooda`. |

## C. Rule, document, instruction
1. **Write for agents:** `mattpocock-skills:writing-for-agents`.
2. **Record:** `mattpocock-skills:domain-modeling`. A "Document first" says where a term and a decision go.
3. **Language:** Write instruction and prompt text in English: `asd-ste100`.
4. **Result:** Write the result to the brain as A "Close" says.
5. **Locked file:** A locked file has feature scope (section "Scope").
6. **Translation:** For a translation of a rule file, the writer lists every dropped word. The auditor compares each rule with the source rule. (Levent 14.10)

| If | Then |
|---|---|
| the work is a workflow spec | `loop-me`. |
| the work is a new skill | `anthropic-skills:skill-creator`. |
| the work is a Claude interface mode or hook | `plugin-authoring`. |
| the document is long | `anthropic-skills:doc-coauthoring`. |
| the change affects behavior | run J "Add the case" and J "Check the judge". |

## D. Plan or decision
1. **Stress-test:** `mattpocock-skills:grilling` (the `vekil` subagent answers).
2. **Compare options:** `thinking-kepner-tregoe`.
3. **Life of a tool:** `thinking-lindy-effect`.
4. **Large decision:** `thinking-model-combination`.
5. **Value:** `thinking-opportunity-cost`.
6. **Forecast:** `thinking-probabilistic`.
7. **Rejection:** Before you reject a proposal: `thinking-steel-manning`.
8. **Direction:** Ask Levent a direction decision. The `vekil` subagent returns it as "Ask Levent".
9. **Result:** Write the result to the brain as A "Close" says.

| If | Then |
|---|---|
| a constraint looks fixed | `thinking-first-principles`. |
| you cannot test the idea | `thinking-thought-experiment`. |
| the effort is uncertain | `thinking-effectuation`. |
| the decision cannot be undone | `thinking-reversibility`. |
| Levent says "plan yap" | `html-plan:html-plan`. |
| another person must fill in the answers | `mattpocock-skills:to-questionnaire`. |
| a design question is still open after 2 turns of text | `mattpocock-skills:prototype`: a trial of at most 10 minutes, then decide. |

## E. Source
1. **Intake:** Levent shares a link or a document: `link-isleme` (PDF: `anthropic-skills:pdf`). Then the `beyin` skill.
2. **Limit:** For outside research, set the limit first: `thinking-bounded-rationality`.
3. **Research:** `mattpocock-skills:research`.
4. **Report:** For a report with many sources: `anthropic-skills:deep-research`.

## H. Question
1. **Status:** Give the status from the brain notes that A "Close" wrote. Use `i-have-adhd:i-have-adhd`.
2. **Understanding:** `mattpocock-skills:wait-what` or `mattpocock-skills:teach`.
3. **Picture:** `diagram-design`.

## I. Session
1. **Long work:** `chief-of-staff`.
2. **Close of a session:** `verification-before-completion`, then A "Close".
3. **Weekly:** `mattpocock-skills:retro` over the last 10 work sessions, with reader agents on session digests.
4. **Handoff:** To give the work to a new session: `mattpocock-skills:handoff`.
5. **Eval work:** Run flow J.
6. **Monthly:** `ponytail:ponytail-audit` (excess) and `ponytail:ponytail-debt` (deferred shortcuts).
7. **Token use:** `anthropic-skills:explain-usage`. Repeated task: `anthropic-skills:schedule`. Daily brief: `anthropic-skills:morning`.
8. **Not understood:** Levent says "anlamadım": `mattpocock-skills:wait-what`. Then explain again with GLOSSARY terms and plain words.

## J. Eval
1. **Start:** `evals:evals-start`.
2. **Audit the cases:** Audit the existing cases first: `evals:eval-audit` (is the case reliable, is the judge checked, is a measure empty).
3. **Find errors:** Find the error types in the session transcripts: `evals:error-discovery`. Astra or an Opus subagent labels the samples in place of Levent (Levent 14.10). When Levent labels, use `evals:build-review-interface`.
4. **Add the case:** For each error type, if code can measure it: `evals:write-code-eval`. If it needs a judge: `evals:write-judge-prompt`.
5. **Check the judge:** Check the judge against the labels: `evals:validate-evaluator`.
6. **No RAG:** Do not use `evals:evaluate-rag`.
7. **Measure:** Measure only with cases that passed the audit.

| If | Then |
|---|---|
| data is scarce | `evals:generate-synthetic-data`. |

## Scope
- Task: the "Per task" item of DEFINITION_OF_DONE.md "How to Apply". The agent gives its own proof. No auditor. AGENTS.md "Önce test" applies to every code change, also to a one-line change.
- Feature: several jobs, a behavior, or an interface. Add the "Per feature" item of DEFINITION_OF_DONE.md "How to Apply" to the task items. Run one independent check (A "Review").
- Outgoing work (push, pull request, delete, archive): the full checklist. Use an independent check (A "Review").
- Work without code (`.scratch` notes): skip the code items. No auditor.
- Locked files: `AGENTS.md`, `AKIS.md`, `CODING_STANDARDS.md`, and `DEFINITION_OF_DONE.md`. They have feature scope at any size, except as "Who writes" says.

## Who writes
- One file, under 20 lines, no code: the orchestrator writes it itself.
- A locked file, at any size: a subagent writes it. One `mattpocock-skills:code-review` pass by a Sonnet subagent checks the diff (A "Review"). Exception (Levent 14.10): Levent approves the change in chat.
  - One added line has task scope. The orchestrator writes it and searches the other files for a second copy of the rule. No auditor.
  - A change of 2 to 3 lines gets the `mattpocock-skills:code-review` pass.
  - A change of more than 3 lines needs a writer subagent and the `mattpocock-skills:code-review` pass.
- Code: a subagent writes it. The Codex audit checks it (A "Review").

## Auditor and rounds
- In this section, "auditor" means the Codex auditor (code) or the reviewer of the `mattpocock-skills:code-review` pass (documents only). A "Review" says which one runs. The Codex audit is only for code changes.
- The auditor is a different agent from the writer.
- The auditor also checks that the writer followed the steps of `AKIS.md`.
- The auditor of a delete or archive job checks the final file list and the links. It also checks the changes outside the scope.
- The verdicts are GEÇTİ, NOTLU GEÇTİ, and KALDI. NOTLU GEÇTİ: low-risk test gaps and style notes. KALDI: a false claim, a broken behavior, a missed instruction, or a security or privacy risk. An audit without a verdict counts as KALDI. The prompt of a `mattpocock-skills:code-review` pass asks for a verdict in the same words.
- Every audit prompt and every code-review pass prompt states the goal of the job. When the goal is to simplify, a deliberately deleted line is not a finding. A deletion is a finding only if a needed rule was lost without a reason. The rest of the diff gets the full review.
- Code change at feature and outgoing scope: at most 3 Codex audit rounds. Every audit prompt names the round number. The auditor gives the round number with the verdict.
- If round 3 returns KALDI (failed): stop the job. Do not open a fourth round. Find the root cause and define the job again. Send Levent the root cause in one line.
- A documents-only change gets one `mattpocock-skills:code-review` pass. If it returns KALDI, fix the findings and run one more pass. If that pass returns KALDI, stop and send Levent the root cause in one line.
- Add the items that an auditor finds to the source report. A report is complete only after a re-audit passes.
- If the Codex sandbox fails with `CreateProcessWithLogonW 1909`, a small round may go to a Sonnet subagent.
