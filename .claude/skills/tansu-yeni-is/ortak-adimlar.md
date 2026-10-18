# Shared steps (Ortak adımlar)

These steps belong to flow A (`tansu-yeni-is`). Flow B (`tansu-hata`) runs them too. Other files refer to a step as `tansu-yeni-is` "Review", `tansu-yeni-is` "Merge", and so on. Never refer to a step by its number.

## Branch
Choose the issue, PR, or direct path from [Issue and PR rule](../../../docs/agents/issue-tracker.md#issue-and-pr-rule). For a PR without an issue, use `belge-<ad>` as the branch name.

For the issue + PR path, if no issue exists, make one first with the issue template. Make the branch for the issue the GitHub way: `gh issue develop <N> --name <N>-<ad> --base master`. The branch name is the issue number and a short name in lower case ASCII letters, digits, and hyphens. Then run these in the main checkout: `git fetch origin`, then `git worktree add .claude/worktrees/<N>-<ad> <N>-<ad>`. If the session already runs in a Claude Code worktree, run `git fetch origin` and `git switch <N>-<ad>` in it. Source: docs.github.com "Creating a branch for an issue" (https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-a-branch-for-an-issue). Clear the context between tickets. A worktree has no `.venv`. In a worktree, use the main venv `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`. <!-- driftlint-ignore: local-only path of the main repository venv, absent in CI -->

## Test gate
Run `.venv\Scripts\python.exe -m pytest -q <test files>` for the changed code and the code that uses it.
Then run `ruff check` and `ruff format --check` on the changed Python files.
Run these checks before each commit. Everything must be green.
Never run the full test suite on the computer: CI on Windows runs it (Levent 17.10: "Bilgisayarda sadece değişikliğin ilgili olduğu test koşacak.").

After a fix commit or a merge of `origin/master`, run these checks again with the test files of the changed code.
Do not paste the test and ruff output into the PR body: CI on Windows proves the tests, format, and lint.
`## Gerçek veri kanıtı` holds only the output of the real-data run.

When only documents changed, run `tests/test_sahipler.py`, `tests/test_atif.py`, and `tests/test_changelog.py` with pytest.
The pool tests skip in CI because the pool is not in git. This skip is accepted.
For a pool batch, set `TANSU_PARTI=<batch ids>`. Do not deselect a red test.

## Review
Merge `origin/master` into the branch first. The reviewer count follows risk (`docs/agents/is-kurallari.md` "Auditor and rounds"):
- Documents only: no reviewer.
- Normal code: one reviewer.
- Risky code (money, data integrity, `kayit/`, CI, the PR check itself, security): two reviewers.

Levent picks Claude or Codex for each job. Each reviewer uses a different session from the writer. Apply at most 3 rounds and the stop rules in "Auditor and rounds".
Apply the YONETIM brief's audit rules. Include the text of `mattpocock-skills:code-review` in every review prompt.
Use the official Codex path: `node <codex plugin>/scripts/codex-companion.mjs task`. A review is read-only. Add `--write` only for a writer.

1. Before review, write the PR body draft to `.scratch/<job>/pr-govde.md` of the main checkout `C:\Users\levent\Desktop\TANSU`. <!-- driftlint-ignore: local-only path of the main repository, absent in CI --> Do not use the worktree for this draft. Open a draft PR ("Pull request"). Give reviewers the latest body and job brief paths.
2. Check each number and each "all / none / passed" claim against this session's command output or a named file. Apply "A claim matches its evidence" to the final PR body and every review prompt.
3. The dağıtıcı runs affected tests and ruff once on the reviewed commit. Give reviewers the output and exit codes. Reviewers use that output.
4. The dağıtıcı starts the required reviewers directly. Each prompt says "Do not start a subagent". Give the latest PR body, brief, goal, and actual worktree path. Derive the goal from the latest brief and body. Review that worktree, not the main checkout. Give no hint of the expected verdict or finding.
5. Ask for a verdict and `Yanlış iddia sayısı: N`. Apply "Auditor and rounds", including false claims, doubt, second passes, and error classes. State its KALDI criteria in each prompt. A process-order point with no effect on the output is a note.
6. Record each reviewer's verdict in `## Bağımsız inceleme`. The single `Sonuç:` is KALDI if any reviewer returns KALDI. Otherwise it is NOTLU GEÇTİ if any reviewer returns that verdict, or GEÇTİ.
7. Write the commit that all required reviewers last read in `Denetlenen commit:`. Fix each KALDI finding before merge.

Each reviewer reads `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md`, and the shared general standards file. After calculation changes, search changed modules for formula prose: docstrings, comments, reports, and HTML. Tie each statement to TASARIM. When test coverage changes, update its owning TASARIM sentence in the same commit.

## Proof
Run `verification-before-completion`. Check the `## Tansu` items of `DEFINITION_OF_DONE.md`.

## Pull request
Push the branch to `origin`. `mattpocock-skills:pr` and `.github/pull_request_template.md` write the PR body together.

Use the body and title forms from `docs/agents/issue-tracker.md` "Issue and PR rule". For a linked issue, the merge into the default branch closes it. CI checks the body and title (`.github/dod_kontrol.py`, Kural 1 and Kural 6). Source: docs.github.com "Linking a pull request to an issue" (https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

For the issue + PR path, open a draft PR with this command chain: `git fetch -q origin && git merge-base --is-ancestor origin/master HEAD && git push -q -u origin <branch> && gh pr create --draft --base master --head <branch> --title "#<N> · <title>" --body-file <pr-govde.md>`. For a PR without an issue, use `belge-<ad>` for `<branch>` and `Belge · <title>` for `--title`. When review is required, fill `## Bağımsız inceleme` after the verdicts. Run `gh pr edit <N> --body-file <file>`, then `gh pr ready <N>`. The `dod` check skips a draft PR and runs at `gh pr ready`.

After the PR opens, the dispatcher calls the app PR status tool. If the tool does not report the PR, the dispatcher binds it.

## Merge
Apply `docs/agents/git.md` "Change log and releases" before the change enters master and when its milestone closes.

Merge when these conditions hold:
- CI is green. `ci` runs on Windows only: the `kayit/` append-only step, `git diff --check`, ruff, pytest, and driftlint. `dod` is the PR body.
- When review is required, every required reviewer returns GEÇTİ or NOTLU GEÇTİ. Documents-only changes need no verdict.

Wait for CI with one command: `gh pr checks <N> --watch` (timeout 600000 ms). Do not poll the status. Wait until a failed run ends before you read its job log. Then run `gh run view --job <id> --log-failed`. It prints nothing while the job runs.

When Levent asks for merge, the dağıtıcı merges after his approval with `gh pr merge <N> --merge`. On the issue + PR path, the merge closes the linked issue. A PR without an issue closes no issue. GitHub deletes the remote branch (auto-delete is on). Send Levent the completion note.

Then close the worktree with `py -3 -X utf8 C:\Users\levent\Desktop\TANSU\kurulum\kapanis.py <worktree>`. <!-- driftlint-ignore: local-only path of the main repository, absent in CI --> Run the command in the main checkout `C:\Users\levent\Desktop\TANSU`, not inside the worktree: Windows cannot remove the working directory of a process, and the script stops with exit 1 before any change. <!-- driftlint-ignore: local-only path of the main repository, absent in CI --> The script removes the worktree. It runs `git pull --ff-only origin master` in the main checkout and removes the local branch. It prints three proof lines: `kapanis: ana HEAD <sha> = origin/master`, `kapanis: is klasoru yok`, and `kapanis: uzak dal yok`. Paste them in the final report. Source: docs.github.com "GitHub flow" (https://docs.github.com/en/get-started/using-github/github-flow): "After you merge your pull request, delete your branch."

## Close
On the issue + PR path, the merged PR closes the linked issue. Close a spec issue when its last ticket closes. Only GLOSSARY and TASARIM stay for good. A session that Levent started writes the result to the brain with the `beyin` skill (Threads and a receipt). A side session follows the receipt sentence below.

A side session (another session started it) writes only one receipt: `py -3 C:\Users\levent\Desktop\YONETIM\beyin\beyin.py receipt --harness claude --event-id <job> --ref "<vault note>" --summary "<text>"`. <!-- driftlint-ignore: local-only path of the brain tool, absent in CI --> `--ref` is a note path inside the brain vault (for example the module card's source note or `knowledge/concepts/kod-standartlari-genel.md`). Write the output paths of the repository in `--summary`. A `--ref` outside the vault fails. The session that started it writes Threads.
