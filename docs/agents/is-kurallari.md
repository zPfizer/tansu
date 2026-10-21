# Job rules (İş kuralları)

Read the section for the current operation. Flows A, B, and C use the shared delivery steps below.
References through `tansu-yeni-is` and a step title point to these shared steps. Never refer to a step by its number.

## Scope
- Task: apply "Per task" in DEFINITION_OF_DONE.md "How to Apply". The writer gives proof. Every code change follows `CODING_STANDARDS.md` "Test first", including one line.
- Feature: several jobs, a behavior, or an interface. Add "Per feature" to the task items.
- Outgoing work (push, pull request, delete, archive): apply the delivery checks and the checklist items relevant to the change. A release requires the full checklist.
- Work without code (`.scratch` notes): skip the code items.
- Locked files: `AGENTS.md`, `docs/agents/is-kurallari.md`, `docs/agents/zamanlayici.md`, the skill files under `.claude/skills/`, `CODING_STANDARDS.md`, and `DEFINITION_OF_DONE.md`. Choose task or feature scope from the behavior and risk, not the line count.
- At every scope, the reviewer count follows risk under "Auditor and rounds".

## Who writes
- Levent assigns the writer and picks the tool (Claude or Codex) for each job. There is no default reviewer.
- Give each file one writer for the job. Other agents read it without editing. The dağıtıcı is the dispatcher.
- For a one-line addition to a locked file, the writer also searches for duplicate rules in other files.
- Use the active tool's agent interface. Reviewers must not edit files. Only the assigned writer may edit its named files.

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
- A later merge that brings only `origin/main` needs no new pass when CI is green. CI checks this exception (Kural 5).
- A fix that adds or changes claim text needs another pass, also after NOTLU GEÇTİ. Read only the changed lines. When an auditor names an error class, the dağıtıcı searches the whole diff for that pattern before the next pass.
- Every review prompt states the goal from the job brief and latest PR body, never from an earlier prompt. Give no hint of the expected verdict or finding. For simplification, a deliberate deletion is a finding only if a needed rule was lost without a reason. Review the rest of the diff in full.
- At most 3 review rounds. Each prompt and verdict names the round. If round 3 returns KALDI, stop. Do not start round 4. Find the root cause and define the job again. Send Levent the root cause in one line.
- A failed run is not a round and gives no approval. This includes a spawn error, empty output, or output without a verdict. Record the failure. Repeat the same round through the available agent interface in "Review".
- A job defined again after round-3 KALDI restarts the count once. Record the new definition and reason in the PR body. A second new definition does not restart the count.
- Add the auditor's findings to the source report. When review is required, the report is complete only after a passing review.

## Branch
Choose the issue, PR, or direct path from [Issue and PR rule](issue-tracker.md#issue-and-pr-rule). For a PR without an issue, use `belge-<ad>` as the branch name.

For the issue + PR path, if no issue exists, make one first with the issue template. Make the branch for the issue the GitHub way: `gh issue develop <N> --name <N>-<ad> --base main`. The branch name is the issue number and a short name in lower case ASCII letters, digits, and hyphens. Then run these in the main checkout: `git fetch origin`, then `git worktree add .claude/worktrees/<N>-<ad> <N>-<ad>`. If the session already runs in a Claude Code worktree, run `git fetch origin` and `git switch <N>-<ad>` in it. Source: docs.github.com "Creating a branch for an issue" (https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-a-branch-for-an-issue). Clear the context between tickets. A worktree has no `.venv`. In a worktree, use the main venv `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`. <!-- driftlint-ignore: local-only path of the main repository venv, absent in CI -->

## Check and evidence
Before the final PR checks, merge `origin/main` into the branch.
Use the main interpreter from "Branch" with `-X utf8 -m pytest -q <test files>` for affected code and callers.
Then run `ruff check` and `ruff format --check` on the changed Python files.
Run these checks before each commit. Everything must be green.
Keep the commands, exit codes, output, and checked commit or file hashes.
Reuse a successful run only if the checked files, dependencies, environment, and input data have not changed.
A commit with the same checked file content does not require another run.
Never run the full test suite on the computer: CI on Windows runs it (Levent 17.10: "Bilgisayarda sadece değişikliğin ilgili olduğu test koşacak.").

After a fix or a merge of `origin/main` changes a checked input, run the affected checks again.
Do not paste the test and ruff output into the PR body: CI on Windows proves the tests, format, and lint.
`## Gerçek veri kanıtı` holds only the output of the real-data run.

When only documents changed, run `tests/test_sahipler.py`, `tests/test_atif.py`, and `tests/test_changelog.py` with pytest.
The pool tests skip in CI because the pool is not in git. Levent accepts this CI skip.
For a pool batch, set `TANSU_PARTI=<batch ids>`. Do not deselect a red test.

Check the applicable items of `DEFINITION_OF_DONE.md`, including `## Tansu`. Read the actual outputs before reporting completion.
Complete the real-data run and its PR evidence before review when that checklist requires it.
A test result does not replace real-data evidence.

## Review
Use the completed "Check and evidence" output. Apply the reviewer count, independence, and round limits from "Auditor and rounds".
Apply the YONETIM brief's audit rules. Ask each reviewer to check correctness, standards, spec compliance, and regressions with evidence.
Use the active tool's separate agent sessions. The reviewer reads files without editing them. The companion plugin is optional.

1. Before review, save one current PR body in the system temporary folder or the main checkout's `.scratch/<job>/pr-govde.md`. Reuse the existing PR. Open a draft PR only if none exists. Give reviewers the actual body and brief paths.
2. Check each number and each "all / none / passed" claim against this session's command output or a named file. Apply "A claim matches its evidence" to the final PR body and every review prompt.
3. The dağıtıcı checks that the "Check and evidence" output matches the reviewed commit and its inputs. Run missing or invalid checks. Give reviewers the output and exit codes. Reviewers use that output.
4. The dağıtıcı starts the required reviewers directly. Each prompt says "Do not start a subagent". Give the latest PR body, brief, goal, and actual worktree path. Derive the goal from the latest brief and body. Review that worktree, not the main checkout. Give no hint of the expected verdict or finding.
5. Ask for a verdict and `Yanlış iddia sayısı: N`. Apply "Auditor and rounds", including false claims, doubt, second passes, and error classes. State its KALDI criteria in each prompt. A process-order point with no effect on the output is a note.
6. Record each reviewer's verdict in `## Bağımsız inceleme`. The single `Sonuç:` is KALDI if any reviewer returns KALDI. Otherwise it is NOTLU GEÇTİ if any reviewer returns that verdict, or GEÇTİ.
7. Write the commit that all required reviewers last read in `Denetlenen commit:`. Fix each KALDI finding before merge.

Each reviewer reads `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md`, and the shared general standards file. After calculation changes, search changed modules for formula prose: docstrings, comments, reports, and HTML. Tie each statement to TASARIM. When test coverage changes, update its owning TASARIM sentence in the same commit.

## Pull request
Push the branch to `origin`. Write the PR body with `.github/pull_request_template.md`.

Use the body and title forms from `docs/agents/issue-tracker.md` "Issue and PR rule". For a linked issue, the merge into the default branch closes it. CI checks the body and title (`.github/dod_kontrol.py`, Kural 1 and Kural 6). Source: docs.github.com "Linking a pull request to an issue" (https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

For the issue + PR path, open a draft PR with this command chain: `git fetch -q origin && git merge-base --is-ancestor origin/main HEAD && git push -q -u origin <branch> && gh pr create --draft --base main --head <branch> --title "#<N> · <title>" --body-file <pr-govde.md>`. For a PR without an issue, use `belge-<ad>` for `<branch>` and `Belge · <title>` for `--title`. If risk requires review, fill `## Bağımsız inceleme` after the verdicts. Run `gh pr edit <N> --body-file <file>`, then `gh pr ready <N>`. The `dod` check skips a draft PR and runs at `gh pr ready`.

After a PR update, read its actual state and body through `gh`. Use app binding only when the active interface provides it.

## Merge
Apply "Change log and releases" before the change enters main and when its milestone closes.

Merge when these conditions hold:
- CI is green. `ci` runs on Windows only: the `kayit/` append-only step, `git diff --check`, ruff, pytest, and driftlint. `dod` is the PR body.
- If risk requires review, every required reviewer returns GEÇTİ or NOTLU GEÇTİ.

Wait for CI with one command: `gh pr checks <N> --watch` (timeout 600000 ms). Do not poll the status. Wait until a failed run ends before you read its job log. Then run `gh run view --job <id> --log-failed`. It prints nothing while the job runs.

When Levent asks for merge, the dağıtıcı merges after his approval with `gh pr merge <N> --merge`. On the issue + PR path, the merge closes the linked issue. A PR without an issue closes no issue. GitHub deletes the remote branch (auto-delete is on). Send Levent the completion note.

Before closure, run `git fetch origin`. Check that the job commit is in `origin/main`.
Check both worktrees for pending changes and active jobs. Check untracked and ignored outputs for evidence that must remain.
Preserve required evidence in the job record before deletion. Do not close a worktree with pending changes or active jobs.
Ask Levent to approve deletion of the named worktree and branch. A merge request does not give this approval.
If another job uses the main checkout, leave it unchanged and report the pending closure.
After these checks, close the approved worktree with `py -3 -X utf8 C:\Users\levent\Desktop\TANSU\kurulum\kapanis.py <worktree>`. <!-- driftlint-ignore: local-only path of the main repository, absent in CI -->
Run the command in the main checkout `C:\Users\levent\Desktop\TANSU`. <!-- driftlint-ignore: local-only path of the main repository, absent in CI -->
Do not run it inside the worktree. Windows cannot delete the working directory of a process.
The script stops with exit 1 before any change in that case.
The script deletes the worktree. It runs `git pull --ff-only origin main` in the main checkout and deletes the local branch.
It prints three proof lines: `kapanis: ana HEAD <sha> = origin/main`, `kapanis: is klasoru yok`, and `kapanis: uzak dal yok`.
Paste them in the final report.
Source: docs.github.com "GitHub flow" (https://docs.github.com/en/get-started/using-github/github-flow): "After you merge your pull request, delete your branch."

## Close
On the issue + PR path, the merged PR closes the linked issue. Close a spec issue when its last ticket closes. Keep permanent facts in their owners from AGENTS.md. A session that Levent started records Threads and a receipt through the available brain integration. Use the active harness. Report a blocked write and the pending record. A side session follows the receipt sentence below.

A side session (another session started it) writes only one receipt: `py -3 -X utf8 C:\Users\levent\Desktop\YONETIM\beyin\beyin.py receipt --harness <active-harness> --event-id <job> --ref "<vault note>" --summary "<text>"`. <!-- driftlint-ignore: local-only path of the brain tool, absent in CI -->
Use a note path inside the brain vault for `--ref`.
For example, use the module card's source note or `knowledge/concepts/kod-standartlari-genel.md`.
Write the output paths of the repository in `--summary`. A `--ref` outside the vault fails. The session that started it writes Threads.

## Git

- **Git (this repository only):** Do not use `rebase`, `--amend`, `--force` (and `--force-with-lease`), `reset --hard`, `clean -f`, `branch -D`,
  `checkout .`, `restore .`, `git add .`, or `git add -A` (for Claude, a permission deny blocks them: `permissions.deny` global and `.claude/settings.json`). Add files
  by name. Which folders git tracks and the log rules are in TASARIM §5.11. Do not delete `veri/`. In a commit, leave the `kayit/` files only added, not <!-- driftlint-ignore: veri/ holds local data outside Git, absent in CI -->
  modified. This rule covers this repository only.
- `.scratch/` and `arsiv/` are local-only, gitignored folders. `.scratch/` holds temporary job files. Old `.scratch/` archives exist only in git history. Read a file with `git show 8c5f06c^:.scratch/<path>`. GitHub and CI do not require these folders.

## Change log and releases

Source: Levent 18.10.

- Every change that enters main adds a line under `## [Yayımlanmamış]` in `CHANGELOG.md`, in the same commit. The writer who changes the code writes its line. This applies to merged PRs and direct small changes.
- When a milestone closes, the dağıtıcı makes a release. The dağıtıcı moves unpublished lines into a new version section with the release date. Use the next minor Semantic Versioning version, for example `0.1.0` to `0.2.0`. The dağıtıcı makes the matching tag, for example `v0.2.0`, and a GitHub release with that section as its notes.

## Short flows and skill naming

**E. Source**
1. **Intake:** Open the shared link or document with the available reader. Preserve its source identity. Then use the available brain integration.
2. **Limit:** For outside research, set the limit first: `thinking-bounded-rationality`.
3. **Research:** Read the original sources. Link each finding to its source. State any gap or conflict.
4. **Report:** For many sources, give each finding its source reference. State unresolved gaps.

**H. Question**
1. **Status:** Give the status from the brain notes that `tansu-yeni-is` "Close" wrote. Use short, plain language.
2. **Understanding:** Explain the subject in plain words. Use the terms in GLOSSARY and one concrete example.
3. **Picture:** Use `diagram-design` when a picture helps explain the answer.

**I. Session**
1. **Long work:** Track decisions, open work, and evidence in one existing job record. Do not create a second tracker.
2. **Close of a session:** Check the applicable completion criteria, then apply `tansu-yeni-is` "Close". A read-only analysis checks only its answer and evidence.
3. **Weekly:** Review the last 10 work sessions. Reader agents are optional for session digests. Record repeated errors and improvements with evidence.
4. **Handoff:** Give the new session the goal, decisions, changed files, checks, open work, and next step. Include the relevant paths.
5. **Eval work:** Run flow J (`tansu-eval`).
6. **Monthly:** `ponytail:ponytail-audit` (excess) and `ponytail:ponytail-debt` (deferred shortcuts).
7. **Not understood:** When Levent says "anlamadım", explain again with GLOSSARY terms and plain words. Use a concrete example.

**Who names skills.** Only five places name skills. They are `AGENTS.md`, `DEFINITION_OF_DONE.md`, `docs/agents/`, `.claude/skills/`, and `.claude/agents/`. `kurulum/kanca.py` names no skill and checks no skill call. In `AGENTS.md`, only the sections "Every job" and "Work flow" name them. Other files do not name a skill to run. Any file may refer to a step by skill name plus step title.
**How to refer to a step.** Refer to a step by the skill name and the step title, for example `tansu-yeni-is` "Review". Never refer to a step by its number.
