# Git (this repository only)

- **Git (this repository only):** Do not use `rebase`, `--amend`, `--force` (and `--force-with-lease`), `reset --hard`, `clean -f`, `branch -D`,
  `checkout .`, `restore .`, `git add .`, or `git add -A` (for Claude, a permission deny blocks them: `permissions.deny` global and `.claude/settings.json`). Add files
  by name. Which folders git tracks and the log rules are in TASARIM §5.11. Do not delete `veri/`. In a commit, leave the `kayit/` files only added, not <!-- driftlint-ignore: veri/ is gitignored local data, absent in CI -->
  modified. This rule covers this repository only.
- `.scratch/` and `arsiv/` are local-only, gitignored folders (Levent 17.10). Old archives remain on the computer and in git history; GitHub and CI do not require these folders.

## Change log and releases

Source: Levent 17.10.

- Every change that enters master adds its line to `CHANGELOG.md` under `## [Yayımlanmamış]` in the same commit. This applies to a merged PR and a direct small change.
- Keep at most five important change lines in `README.md` under `## Yeni olanlar`. Copy each line word for word from the top section of `CHANGELOG.md`. The version line and the change log link are separate.
- When a milestone closes, Claude makes a release. Claude moves the unpublished lines into a new version section with the release date. Use the next minor Semantic Versioning version, for example `0.1.0` to `0.2.0`. Claude makes the matching tag, for example `v0.2.0`. Claude makes a GitHub release with that section as its notes. Claude updates the `Son sürüm` line in `README.md`.
