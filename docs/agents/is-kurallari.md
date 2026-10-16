# Job rules (İş kuralları)

## Scope
- Task: the "Per task" item of DEFINITION_OF_DONE.md "How to Apply". The agent gives its own proof. No auditor. The rule "Önce test" (`docs/agents/kod-kurallari.md`) applies to every code change, also to a one-line change.
- Feature: several jobs, a behavior, or an interface. Add the "Per feature" item of DEFINITION_OF_DONE.md "How to Apply" to the task items. Run one independent check (`tansu-yeni-is` "Review").
- Outgoing work (push, pull request, delete, archive): the full checklist. Use an independent check (`tansu-yeni-is` "Review").
- Work without code (`.scratch` notes): skip the code items. No auditor.
- Locked files: `AGENTS.md`, the rule files under `docs/agents/` (`is-kurallari.md`, `kod-kurallari.md`, `git.md`, `zamanlayici.md`, `akislar.md`), the skill files under `.claude/skills/`, `CODING_STANDARDS.md`, and `DEFINITION_OF_DONE.md`. They have feature scope at any size, except as "Who writes" says.

## Who writes
- One file, under 20 lines, no code: the orchestrator writes it itself.
- A locked file:
  - One added line has task scope. The orchestrator writes it and searches the other files for a second copy of the rule. No auditor.
  - A change of 2 to 3 lines: the orchestrator writes it. One `mattpocock-skills:code-review` pass by a Sonnet subagent checks the diff (`tansu-yeni-is` "Review").
  - A change of more than 3 lines: a writer subagent writes it. One `mattpocock-skills:code-review` pass by a Sonnet subagent checks the diff (`tansu-yeni-is` "Review").
- Code: a subagent writes it. The Codex audit checks it (`tansu-yeni-is` "Review").

## Auditor and rounds
- In this section, "auditor" means the Codex auditor (code) or the reviewer of the `mattpocock-skills:code-review` pass (documents only). `tansu-yeni-is` "Review" says which one runs. The Codex audit is only for code changes.
- The auditor is a different agent from the writer.
- The auditor also checks that the writer followed the steps of the flow skill. The flow skills are `tansu-yeni-is` and the other skills under `.claude/skills/`. The auditor reads the `Akış:` line of the PR body. It checks the diff and the PR body against the steps of that skill. It names each step that has no trace. It compares the PR line `Çağrılan beceriler:` with the steps of the skill. The session that started the job compares the list with the session transcript.
- The auditor of a delete or archive job checks the final file list and the links. It also checks the changes outside the scope.
- The verdicts are GEÇTİ, NOTLU GEÇTİ, and KALDI. NOTLU GEÇTİ: low-risk test gaps and style notes. KALDI: a false claim, a broken behavior, a missed instruction, or a security or privacy risk. An audit without a verdict counts as KALDI. The prompt of a `mattpocock-skills:code-review` pass asks for a verdict in the same words.
- A claim that is false against the source is KALDI at any risk level. The auditor does not grade it low. A doubt in the verdict text (for example "KALDI olabilir") makes the verdict KALDI. The auditor writes `Yanlış iddia sayısı: N` for its pass. A pass with N greater than 0 is KALDI. The PR body copies the N of the pass whose verdict it copies.
- A fix commit that adds or changes claim text gets one more pass, also after NOTLU GEÇTİ. The pass reads only the changed lines. When the auditor names an error class, the orchestrator searches the whole diff for that pattern before the second pass.
- Every audit prompt and every code-review pass prompt states the goal of the job. When the goal is to simplify, a deliberately deleted line is not a finding. A deletion is a finding only if a needed rule was lost without a reason. The rest of the diff gets the full review.
- Code change at feature and outgoing scope: at most 3 Codex audit rounds. Every audit prompt names the round number. The auditor gives the round number with the verdict.
- If round 3 returns KALDI (failed): stop the job. Do not open a fourth round. Find the root cause and define the job again. Send Levent the root cause in one line.
- A documents-only change to a locked file or at feature scope gets one `mattpocock-skills:code-review` pass. If the pass returns KALDI, fix the findings and run one more pass. If that pass returns KALDI, stop and send Levent the root cause in one line. Another document change has task scope and no auditor.
- Add the items that an auditor finds to the source report. A report is complete only after a re-audit passes.
- If the Codex sandbox fails with `CreateProcessWithLogonW 1909`, a small round may go to a Sonnet subagent.
