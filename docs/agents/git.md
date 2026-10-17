# Git (this repository only)

- **Git (this repository only):** Do not use `rebase`, `--amend`, `--force` (and `--force-with-lease`), `reset --hard`, `clean -f`, `branch -D`,
  `checkout .`, `restore .`, `git add .`, or `git add -A` (for Claude, a permission deny blocks them: `permissions.deny` global and `.claude/settings.json`). Add files
  by name. Which folders git tracks and the log rules are in TASARIM §5.11. Do not delete `veri/`. In a commit, leave the `kayit/` files only added, not <!-- driftlint-ignore: veri/ is gitignored local data, absent in CI -->
  modified. This rule covers this repository only.
- `.scratch/` and `arsiv/` are local-only, gitignored folders (Levent 17.10). Old archives remain on the computer and in git history; GitHub and CI do not require these folders.
