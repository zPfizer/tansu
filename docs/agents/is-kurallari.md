# Job rules (İş kuralları)

## Scope
- Task: apply "Per task" in DEFINITION_OF_DONE.md "How to Apply". The writer gives proof. Every code change follows "Önce test" (`docs/agents/kod-kurallari.md`), including one line.
- Feature: several jobs, a behavior, or an interface. Add "Per feature" to the task items.
- Outgoing work (push, pull request, delete, archive): apply the full checklist.
- Work without code (`.scratch` notes): skip the code items.
- Locked files: `AGENTS.md`, the rule files under `docs/agents/` (`is-kurallari.md`, `kod-kurallari.md`, `git.md`, `zamanlayici.md`, `akislar.md`), the skill files under `.claude/skills/`, `CODING_STANDARDS.md`, and `DEFINITION_OF_DONE.md`. A one-line addition has task scope. Other locked-file changes have feature scope.
- At every scope, the reviewer count follows risk under "Auditor and rounds".

## Who writes
- Levent assigns the writer and picks the tool (Claude or Codex) for each job. There is no default reviewer.
- Give each file one writer. The dağıtıcı is the dispatcher: the session that runs the job.
- For a one-line addition to a locked file, the writer also searches for duplicate rules in other files.
- Use Codex through `tansu-yeni-is` "Review": read-only for reviews, `--write` only for a writer.

## Auditor and rounds
- Documents only: no reviewer. Normal code: one reviewer. Risky code: two reviewers.
- Risky code covers money, data integrity, `kayit/`, CI, the PR check itself, and security.
- Levent picks the tool. Each reviewer, called an auditor here, works in a different session from the writer.
- The auditor checks the flow steps, the diff, and the latest PR body. Name each step with no trace.
- For delete or archive work, check the final file list, links, and changes outside the scope.
- Verdicts are GEÇTİ, NOTLU GEÇTİ, and KALDI. NOTLU GEÇTİ covers low-risk test gaps, style notes, and process-order points that do not affect the output.
- KALDI means a false claim, broken behavior, security or privacy risk, or a missed instruction that breaks correctness or a written requirement. Written requirements include the spec, acceptance criteria, DEFINITION_OF_DONE items, and rule sentences that the output violates.
- A false claim against the source is KALDI at every risk level. Doubt in the verdict, such as "KALDI olabilir", means KALDI. Each auditor writes `Yanlış iddia sayısı: N`. A pass with N greater than 0 is KALDI.
- A verdict covers only the commit that the auditor read. A later commit needs a pass on its changes, including a fix commit without claim text. The PR body names the reviewed commit in `Denetlenen commit:`.
- A later merge that brings only `origin/master` needs no new pass when CI is green. CI checks this exception (Kural 5).
- A fix that adds or changes claim text needs another pass, also after NOTLU GEÇTİ. Read only the changed lines. When an auditor names an error class, the dağıtıcı searches the whole diff for that pattern before the next pass.
- Every review prompt states the goal from the job brief and latest PR body, never from an earlier prompt. Give no hint of the expected verdict or finding. For simplification, a deliberate deletion is a finding only if a needed rule was lost without a reason. Review the rest of the diff in full.
- At most 3 review rounds. Each prompt and verdict names the round. If round 3 returns KALDI, stop. Do not start round 4. Find the root cause and define the job again. Send Levent the root cause in one line.
- A failed run is not a round and gives no approval. This includes a spawn error, empty output, or output without a verdict. Record the failure. Repeat the same round through the official tool path in `tansu-yeni-is` "Review".
- A job defined again after round-3 KALDI restarts the count once. Record the new definition and reason in the PR body. A second new definition does not restart the count.
- Add the auditor's findings to the source report. When review is required, the report is complete only after a passing review.
