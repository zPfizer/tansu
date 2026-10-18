# Git (this repository only)

- **Git (this repository only):** Do not use `rebase`, `--amend`, `--force` (and `--force-with-lease`), `reset --hard`, `clean -f`, `branch -D`,
  `checkout .`, `restore .`, `git add .`, or `git add -A` (for Claude, a permission deny blocks them: `permissions.deny` global and `.claude/settings.json`). Add files
  by name. Which folders git tracks and the log rules are in TASARIM §5.11. Do not delete `veri/`. In a commit, leave the `kayit/` files only added, not <!-- driftlint-ignore: veri/ is gitignored local data, absent in CI -->
  modified. This rule covers this repository only.
- `.scratch/` and `arsiv/` are local-only, gitignored folders. `.scratch/` holds temporary job files. Old `.scratch/` archives exist only in git history. Read a file with `git show 8c5f06c^:.scratch/<path>`. GitHub and CI do not require these folders.

## Change log and releases

Source: Levent 18.10.

- Every change that enters master adds a line under `## [Yayımlanmamış]` in `CHANGELOG.md`, in the same commit. The writer who changes the code writes its line. This applies to merged PRs and direct small changes.
- When a milestone closes, the dağıtıcı makes a release. The dağıtıcı moves unpublished lines into a new version section with the release date. Use the next minor Semantic Versioning version, for example `0.1.0` to `0.2.0`. The dağıtıcı makes the matching tag, for example `v0.2.0`, and a GitHub release with that section as its notes.
