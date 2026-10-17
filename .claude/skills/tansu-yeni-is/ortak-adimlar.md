# Shared steps (Ortak adımlar)

These steps belong to flow A (`tansu-yeni-is`). Flow B (`tansu-hata`) runs them too. Other files refer to a step as `tansu-yeni-is` "Review", `tansu-yeni-is` "Merge", and so on. Never refer to a step by its number.

## Branch
Use one branch for each ticket. Cut every branch from `kaynak/master`, not from local `master`. Give it its own worktree: `git worktree add ../TANSU-bNN -b pr/NN-<ad> kaynak/master`. `NN` is the next PR number (`gh pr list --state all --limit 1` gives the last one). Leave `NN` out if you have no number (`pr/<ad>`). A SessionStart hook (`kurulum/oturum_baslangic.py`) fast-forwards the main checkout on `master` to `kaynak/master`. It acts only in the main checkout, only on `master`, and only by fast-forward. Untracked files and changes under `kayit/` do not block it. Any other tracked change does. When it cannot move `master`, it prints one warning line. Clear the context between tickets. A worktree has no `.venv`. In a worktree, use the main venv `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`. <!-- driftlint-ignore: local-only path of the main repository venv, absent in CI -->

## Test gate
Run `kurulum\kapi.ps1`. It runs pytest, `ruff check .`, `ruff format --check .`, and `git diff --check kaynak/master`, and it prints `kapi:` summary lines. Run it before each commit. Everything must be green. When `TANSU_BEKLENEN_ACIK` is unset, the gate counts the open pool notes itself, prints `kapi: acik havuz notu = <n>`, and uses that count. A variable that you set wins.
The gate always runs the count. If the pool folder is missing, it prints `kapi: acik havuz notu = HATA` and stops with exit code 1, also when `TANSU_BEKLENEN_ACIK` is set.

After the last commit, run it again on the clean tree. This also applies after a fix commit or a merge of `kaynak/master`. Paste that output into `## Gerçek veri kanıtı` of the PR body. The last line must be `kapi: HEAD <sha> temiz`, and the sha must be the PR head sha. An untracked file also makes the tree `kirli`. A code change needs the full run (CI rejects `-Belge` then).

When only documents changed, `kurulum\kapi.ps1 -Belge` runs the document tests. The full run is in CI. For a pool batch, set `TANSU_PARTI=<batch ids>`. Do not deselect a red test.

## Review
Merge `kaynak/master` into the branch first. Then check the change by its type.
- A change with code: run `mattpocock-skills:code-review` (a Claude subagent). Then run the Codex audit (subagent type `codex`). Add the text of the code-review skill to the auditor prompt.
- A change to documents only (no code): run one `mattpocock-skills:code-review` pass by a Sonnet subagent on the diff. Run no Codex audit.

Run the review in this order.
1. Before Review, write the PR body draft with `Akış:` and `Çağrılan beceriler:` to `.scratch/<job>/pr-govde.md` of the main checkout `C:\Users\levent\Desktop\TANSU`, not of the worktree. An untracked file in the worktree makes `kurulum\kapi.ps1` print `kirli`. <!-- driftlint-ignore: local-only path of the main repository, absent in CI --> Open the PR as a draft (see "Pull request"). Give the path to the auditor.
2. The orchestrator starts the two axes of `mattpocock-skills:code-review` itself, as two parallel Sonnet subagents. No auditor agent sits between them. Each subagent prompt says: "Do not start a subagent."
3. The audit prompt asks for the verdict and the line `Yanlış iddia sayısı: N`. Apply AGENTS.md "Auditor and rounds" (false claim, doubt, second pass, error class). Copy the verdict line of the auditor word for word into `Denetçi kararı (aynen):`.

Both checks read `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md`, and the general standards file that `CODING_STANDARDS.md` points to. After a change in a calculation, search the changed modules for prose that states the formula. This covers docstrings, comments, report text, and HTML. Tie each one to its TASARIM sentence. When the coverage of a test changes, update the owning TASARIM sentence in the same commit.

## Proof
Run `verification-before-completion`. Check the `## Tansu` items of `DEFINITION_OF_DONE.md`.

## Pull request
Push the branch to `kaynak`. `mattpocock-skills:pr` and `.github/pull_request_template.md` write the PR body together.

The PR body has an `Akış:` line with the flow skill used. The auditor checks the steps of that skill (AGENTS.md "Auditor and rounds"). `Çağrılan beceriler:` is a copy of the Skill calls of this session in call order. Do not write a skill that you did not call.

Open a draft PR with this command chain: `git fetch -q kaynak && git merge-base --is-ancestor kaynak/master HEAD && git push -q -u kaynak <branch> && gh pr create --draft --base master --head <branch> --title "<title>" --body-file <pr-govde.md>`. After the verdict, fill `## Bağımsız inceleme`. Run `gh pr edit <N> --body-file <file>`, then `gh pr ready <N>`. The `dod` check skips a draft PR and runs at `gh pr ready`.

## Merge
Merge when two things are true.
- CI is green. `ci` is the `kayit/` append-only step, `git diff --check`, ruff, pytest, and driftlint. `windows` is pytest on Windows. `dod` is the PR body.
- The independent verdict is GEÇTİ or NOTLU GEÇTİ. For code, it is the verdict of the Codex audit. For documents only, it is the verdict of the `mattpocock-skills:code-review` pass.

Wait for CI with one command: `gh pr checks <N> --watch` (timeout 300000 ms). Do not poll the status.

Claude merges with `gh pr merge --merge`. Levent gets only the completion note (Levent 15.10).

## Close
Move the spec and the tickets of a finished job to `.scratch/arsiv/`. Only GLOSSARY and TASARIM stay for good. A session that Levent started writes the result to the brain with the `beyin` skill (Threads and a receipt). A side session follows the receipt sentence below. If a branch merged, remove its worktree with `git worktree remove <path>`. Do not use `--force`. If git refuses, stop and tell Levent. After a merge, also remove the local branch with `git branch -d <branch>` and show `git worktree list`.

A side session (another session started it) writes only one receipt: `py -3 C:\Users\levent\Desktop\YONETIM\beyin\beyin.py receipt --harness claude --event-id <job> --ref "<vault note>" --summary "<text>"`. <!-- driftlint-ignore: local-only path of the brain tool, absent in CI --> `--ref` is a note path inside the brain vault (for example the module card's source note or `knowledge/concepts/kod-standartlari-genel.md`). Write the output paths of the repository in `--summary`. A `--ref` outside the vault fails. The session that started it writes Threads.
