# Handoff: AKIS-to-skills job (PR #27), stopped at 80% context (16.10)

**Superseded (16.10):** the isolation rules and the remaining steps below are done. Rules: `tansu-eval` "Isolation" (c9f0439; it uses `disableAllHooks`, not `--setting-sources`). Set 2 is approved (d6192e5). Do not redo the steps below. They are kept as a record only.

Continue in a fresh Tansu session. Start with `/tansu-belge`. The worktree is `C:\Users\levent\Desktop\TANSU-beceri`, on branch `pr/akis-beceriler`. The PR is https://github.com/zPfizer/tansu-kaynak/pull/27. The PR body is in `C:\Users\levent\AppData\Roaming\Claude\side-session-notes\local_8e127142-fad6-4efa-9b14-70fa26c4ae31\pr-govde-beceri.md`.

## Committed on `pr/akis-beceriler`

| Commit | Content | Pushed |
|---|---|---|
| 96c9c68 | The AKIS move, belge-hizası archive, and test reference updates | yes |
| e078bae | `Akış:` line plus dod Kural 7 | yes |
| 5f62b12 | Overlap sentence removed from the `tansu-yeni-is` description | yes |
| 9a66641 | Kural 7 requires exactly one `Akış:` line (Codex round 1 fix), plus the light-check notes | yes |
| 0f84cf8 | `tansu-eval` "Skill trigger eval" rules, `.scratch/beceri-tetik-1610/` (eval set, 2 sample runs, README), `tansu-belge` If row | yes |
| 14c44ee | `tansu-eval`: eval runs are read only (`--disallowedTools`, `git status`), plus a CODING_STANDARDS "Seen once" entry | yes |
| b180e81 | Light-check notes (four signs, README title reference) | yes, HEAD of the PR |
| 5f14238 | `.scratch/devir-1610.md`, the session-wide handoff | **no, local only** |

Decide whether to push 5f14238 or replace it with this file.

Reviews:
- Documents: Sonnet `mattpocock-skills:code-review` gave NOTLU GEÇTİ on e078bae and NOTLU GEÇTİ on 14c44ee. Both sets of notes are fixed.
- Code (`.github/dod_kontrol.py`, tests): Codex (project codex agent) round 1 KALDI, then round 2 NOTLU GEÇTİ on 9a66641.
- Gate on b180e81: 637 passed, 13 skipped. Ruff is clean. driftlint 0 errors.
- CI on b180e81 was still running at handoff. Check `gh pr checks 27` and the GitHub Codex review comments.

## Uncommitted changes

None. The eval sessions changed `.claude/agents/vekil.md` and `.claude/skills/tansu-grill/SKILL.md`. Those were the eval's edits (queries 22 and 24, stream files `C:\Users\levent\AppData\Local\Temp\tmp.TLmmJ8qj4c\t2\o22.json` and `o24.json`). I restored them by name with `git restore --`.

Checks:
- `git diff master` shows no change to `tansu-grill/SKILL.md`.
- The `vekil.md` diff holds only the intended AKIS→AGENTS reference changes from 96c9c68.
- `git status` was clean after the restore.

## The eval incident (16.10)

- `--allowedTools` only pre-approves tools. This machine runs in bypass permission mode, so every eval run could use every tool.
- Run 2 used Bash, PowerShell, Edit, Write, and Agent:
  - o22 and o24 edited the two Tansu files above.
  - o10 and o22 ran pytest and git.
  - o34 started a nested `claude -p`.
  - o26's vekil wrote a fake decision into the brain Threads. The Stop hook committed it (656d001). The YONETIM session removed the line.
- The YONETIM session killed the runner and all `claude -p` processes (around 01:45).
- Run 1 and run 2 are both **invalid** (`.scratch/beceri-tetik-1610/README.md`).

## Required isolation rules (not yet fully in `tansu-eval`)

14c44ee wrote only a part of these rules. It names `--disallowedTools` for Edit, Write, Bash, PowerShell, and NotebookEdit, and a `git status` check. Still to add to `.claude/skills/tansu-eval/SKILL.md` "Skill trigger eval" (permanent text):
1. Runs happen in a disposable copy: a temporary worktree outside the PR worktree.
2. Remove the brain hooks from the eval sessions. The hooks are in the user settings `~/.claude/settings.json`, not in the project settings. Candidate: `--setting-sources project,local` for the eval runs. Check this against the official CLI docs.
3. Each run uses `--disallowedTools "Bash PowerShell Edit Write NotebookEdit Agent"`. Agent is missing in 14c44ee. o34 shows that the flag works.
4. After each run, check that `git status` of the copy and of the brain is unchanged.
5. A run that used a forbidden tool counts as an invalid run, not as a miss.

## Remaining steps

1. Add the isolation rules above to `tansu-eval` "Skill trigger eval" and update the README. This is a document change, so it gets one Sonnet code-review pass.
2. Run a 2-query sample under these rules. Before any full run, show the tool list from its stream files. Report it to the YONETIM session (local_8e127142).
3. Do not run the full 3-run measure in this PR unless the YONETIM session asks for it. Levent wants a pause after this job (16.10).
4. Push the branch, wait for CI and the GitHub Codex review, fix any findings, then merge with `gh pr merge 27 --merge` (`tansu-yeni-is` "Merge").
5. Run `tansu-yeni-is` "Close":
   - `git worktree remove ..\TANSU-beceri`, without `--force`.
   - Fast-forward the main checkout: `git merge --ff-only kaynak/master`.
6. Send the final report to the YONETIM session. Include:
   - the PR link;
   - the skill list;
   - the trigger proof: natural prompts loaded `tansu-yeni-is`, `tansu-hata`, `tansu-belge`, and `/tansu-hata` expanded directly;
   - the `git grep AKIS` output: only fixtures in `tests/test_sahipler.py`;
   - the eval status.

## Open items (outside this job)

- 20 Codex worktree folders under `C:\Users\levent\.codex\worktrees\` are left on disk. So are `C:\Users\levent\Desktop\TANSU-b08`, `TANSU-ajanlar`, and `/tmp/tmp.zlzG9DhTxD`. Their temp folders deny access.
- The `TANSU-akis` worktree needs `--force` to remove. Levent decides.
- FIRMA notes for the same model are in `.scratch/devir-1610.md` (commit 5f14238).
