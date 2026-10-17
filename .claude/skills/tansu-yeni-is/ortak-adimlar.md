# Shared steps (Ortak adımlar)

These steps belong to flow A (`tansu-yeni-is`). Flow B (`tansu-hata`) runs them too. Other files refer to a step as `tansu-yeni-is` "Review", `tansu-yeni-is` "Merge", and so on. Never refer to a step by its number.

## Branch
Every job starts from a GitHub issue (`docs/agents/issue-tracker.md`). If no issue exists, make one first with the issue template. Make the branch for the issue the GitHub way: `gh issue develop <N> --name <N>-<ad> --base master`. The branch name is the issue number and a short name in lower case ASCII letters, digits, and hyphens. Then run these in the main checkout: `git fetch origin`, then `git worktree add .claude/worktrees/<N>-<ad> <N>-<ad>`. If the session already runs in a Claude Code worktree, run `git fetch origin` and `git switch <N>-<ad>` in it. Source: docs.github.com "Creating a branch for an issue" (https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-a-branch-for-an-issue). Clear the context between tickets. A worktree has no `.venv`. In a worktree, use the main venv `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`. <!-- driftlint-ignore: local-only path of the main repository venv, absent in CI -->

## Test gate
Run `kurulum\kapi.ps1`. It runs pytest, `ruff check .`, `ruff format --check .`, and `git diff --check origin/master`, and it prints `kapi:` summary lines. Run it before each commit. Everything must be green. When `TANSU_BEKLENEN_ACIK` is unset, the gate counts the open pool notes itself, prints `kapi: acik havuz notu = <n>`, and uses that count. A variable that you set wins.
The gate always runs the count. If the pool folder is missing, it prints `kapi: acik havuz notu = HATA` and stops with exit code 1, also when `TANSU_BEKLENEN_ACIK` is set.
`TANSU_PY` (a full path) sets the Python of the gate. The default is the main venv. If that file is missing or the count is not a whole number, the gate prints a `kapi:` error line and stops with exit code 1. A command that cannot start stops the gate with a PowerShell error and exit code 1.

After the last commit, run it again on the clean tree. This also applies after a fix commit or a merge of `origin/master`. An untracked file also makes the tree `kirli`. A code change needs the full run. Do not paste the gate output into the PR body: CI on Windows proves the tests, format, and lint. `## Gerçek veri kanıtı` holds only the output of the real-data run.

When only documents changed, `kurulum\kapi.ps1 -Belge` runs the document tests. The full run is in CI. For a pool batch, set `TANSU_PARTI=<batch ids>`. Do not deselect a red test.

## Review
Merge `origin/master` into the branch first. Then check the change by its type.
- A change with code: run `mattpocock-skills:code-review` (a Claude subagent). Then run the Codex audit (subagent type `codex`). Add the text of the code-review skill to the auditor prompt.
- A change to documents only (no code): run one `mattpocock-skills:code-review` pass by a Sonnet subagent on the diff. Run no Codex audit.

Run the review in this order.
1. Before Review, write the PR body draft to `.scratch/<job>/pr-govde.md` of the main checkout `C:\Users\levent\Desktop\TANSU`, not of the worktree. An untracked file in the worktree makes `kurulum\kapi.ps1` print `kirli`. <!-- driftlint-ignore: local-only path of the main repository, absent in CI --> Open the PR as a draft (see "Pull request"). Give the path to the auditor.
2. The orchestrator starts the two axes of `mattpocock-skills:code-review` itself, as two parallel Sonnet subagents. No auditor agent sits between them. Each subagent prompt says: "Do not start a subagent."
3. The audit prompt asks for the verdict and the line `Yanlış iddia sayısı: N`. Apply docs/agents/is-kurallari.md "Auditor and rounds" (false claim, doubt, second pass, error class). Write the verdict of the auditor into `Sonuç:`.
4. Every `mattpocock-skills:code-review` pass prompt says: a finding is KALDI only when it breaks correctness or a written requirement of the job (the spec, an acceptance criterion, a DEFINITION_OF_DONE item, or a rule sentence that the output violates). A false claim, a broken behavior, and a security or privacy risk stay KALDI. A process-order point with no effect on the output is a note.
5. Write the sha of the commit that the last pass read into `Denetlenen commit:`. Fix each KALDI finding before the merge.

Both checks read `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md`, and the general standards file that `CODING_STANDARDS.md` points to. After a change in a calculation, search the changed modules for prose that states the formula. This covers docstrings, comments, report text, and HTML. Tie each one to its TASARIM sentence. When the coverage of a test changes, update the owning TASARIM sentence in the same commit.

## Proof
Run `verification-before-completion`. Check the `## Tansu` items of `DEFINITION_OF_DONE.md`.

## Pull request
Push the branch to `origin`. `mattpocock-skills:pr` and `.github/pull_request_template.md` write the PR body together.

The PR body has a `Closes #<N>` line for the issue of the branch. When the PR merges into the default branch, GitHub closes the linked issue. CI checks the line (`.github/dod_kontrol.py`, Kural 1). Source: docs.github.com "Linking a pull request to an issue" (https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue): "When you merge a linked pull request into the default branch of a repository, its linked issue is automatically closed."

Open a draft PR with this command chain: `git fetch -q origin && git merge-base --is-ancestor origin/master HEAD && git push -q -u origin <branch> && gh pr create --draft --base master --head <branch> --title "<title>" --body-file <pr-govde.md>`. After the verdict, fill `## Bağımsız inceleme`. Run `gh pr edit <N> --body-file <file>`, then `gh pr ready <N>`. The `dod` check skips a draft PR and runs at `gh pr ready`.

## Merge
Merge when two things are true.
- CI is green. `ci` runs on Windows only: the `kayit/` append-only step, `git diff --check`, ruff, pytest, and driftlint. `dod` is the PR body.
- The independent verdict is GEÇTİ or NOTLU GEÇTİ. For code, it is the verdict of the Codex audit. For documents only, it is the verdict of the `mattpocock-skills:code-review` pass.

Wait for CI with one command: `gh pr checks <N> --watch` (timeout 300000 ms). Do not poll the status.

Claude merges with `gh pr merge <N> --merge`. The merge closes the issue. GitHub deletes the remote branch (auto-delete is on). Levent gets only the completion note (Levent 15.10).

Then close the worktree with `py -3 -X utf8 C:\Users\levent\Desktop\TANSU\kurulum\kapanis.py <worktree>`. <!-- driftlint-ignore: local-only path of the main repository, absent in CI --> Run the command in the main checkout `C:\Users\levent\Desktop\TANSU`, not inside the worktree: Windows cannot remove the working directory of a process, and the script stops with exit 1 before any change. <!-- driftlint-ignore: local-only path of the main repository, absent in CI --> The script removes the worktree. It runs `git pull --ff-only origin master` in the main checkout and removes the local branch. It prints three proof lines: `kapanis: ana HEAD <sha> = origin/master`, `kapanis: is klasoru yok`, and `kapanis: uzak dal yok`. Paste them in the final report. Source: docs.github.com "GitHub flow" (https://docs.github.com/en/get-started/using-github/github-flow): "After you merge your pull request, delete your branch."

## Close
The merged PR closes the issue. Close a spec issue when its last ticket closes. Only GLOSSARY and TASARIM stay for good. A session that Levent started writes the result to the brain with the `beyin` skill (Threads and a receipt). A side session follows the receipt sentence below.

A side session (another session started it) writes only one receipt: `py -3 C:\Users\levent\Desktop\YONETIM\beyin\beyin.py receipt --harness claude --event-id <job> --ref "<vault note>" --summary "<text>"`. <!-- driftlint-ignore: local-only path of the brain tool, absent in CI --> `--ref` is a note path inside the brain vault (for example the module card's source note or `knowledge/concepts/kod-standartlari-genel.md`). Write the output paths of the repository in `--summary`. A `--ref` outside the vault fails. The session that started it writes Threads.
