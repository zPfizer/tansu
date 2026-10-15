# Shared steps (Ortak adımlar)

These steps belong to flow A (`tansu-yeni-is`). Flow B (`tansu-hata`) runs them too. Other files refer to a step as `tansu-yeni-is` "Review", `tansu-yeni-is` "Merge", and so on. Never refer to a step by its number.

## Branch
Use one branch `pr/NN-<ad>` from `master` for each ticket. Give it its own worktree: `git worktree add ../TANSU-bNN -b pr/NN-<ad> master`. Clear the context between tickets.

## Test gate
Run these from the main venv `C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe`: `-m pytest -q`, `-m ruff check .`, and `-m ruff format --check .`. Run `git diff --check`. All must be green before each commit. <!-- driftlint-ignore: local-only path of the main repository venv, absent in CI -->

## Review
Merge `master` into the branch first. Then check the change by its type.
- A change with code: run `mattpocock-skills:code-review` (a Claude subagent). Then run the Codex audit (subagent type `codex`). Add the text of the code-review skill to the auditor prompt.
- A change to documents only (no code): run one `mattpocock-skills:code-review` pass by a Sonnet subagent on the diff. Run no Codex audit.

The PR body has an `Akış:` line with the flow skill used. The auditor checks the steps of that skill (AGENTS.md "Auditor and rounds").

Both checks read `CODING_STANDARDS.md` and `DEFINITION_OF_DONE.md`. After a change in a calculation, search the changed modules for prose that states the formula. This covers docstrings, comments, report text, and HTML. Tie each one to its TASARIM sentence. When the coverage of a test changes, update the owning TASARIM sentence in the same commit.

## Proof
Run `verification-before-completion`. Check the `## Tansu` items of `DEFINITION_OF_DONE.md`.

## Pull request
Push the branch to `kaynak`. `mattpocock-skills:pr` and `.github/pull_request_template.md` write the PR body together.

## Merge
Merge when two things are true.
- CI is green. `ci` is the `kayit/` append-only step, ruff, pytest, and driftlint. `dod` is the PR body.
- The independent verdict is GEÇTİ or NOTLU GEÇTİ. For code, it is the verdict of the Codex audit. For documents only, it is the verdict of the `mattpocock-skills:code-review` pass.

Claude merges with `gh pr merge --merge`. Levent gets only the completion note (Levent 15.10).

## Close
Move the spec and the tickets of a finished job to `.scratch/arsiv/`. Only GLOSSARY and TASARIM stay for good. Write the result to the brain with the `beyin` skill (Threads and a receipt). If a branch merged, remove its worktree with `git worktree remove <path>`. Do not use `--force`. If git refuses, stop and tell Levent.
