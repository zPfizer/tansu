# Issue tracker: GitHub

Specs and tickets of this repo are GitHub issues in `zPfizer/tansu-kaynak` (remote `origin`). Use the `gh` CLI for all operations. `gh` finds the repo from `git remote -v`.

`.scratch/` is local and gitignored. It holds temporary job files and the old read-only ticket archive. The old archive also remains in git history. GitHub and CI do not require these local files. An open ticket has one place: its issue.

A large job uses a GitHub issue, a branch, and a PR (Levent 17.10). A small change that Levent requests in chat goes directly to master with a green CI run, without an issue or PR.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body-file <file> --label needs-triage --milestone "<name>"`. The issue template `.github/ISSUE_TEMPLATE/is.md` sets the layout.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,assignees,state,comments`.
- **List issues**: `gh issue list --state open --json number,title,labels,assignees` with `--label` and `--state` filters.
- **Comment**: `gh issue comment <number> --body "..."`.
- **Labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`.
- **Close**: `gh issue close <number> --comment "..."`.
- **Spec**: one issue, title `Spec: <name>`. The tickets name it in a `Parent: #N` line.
- **Issue body**: three bold lines: `**Amaç:**` (what to build), `**Kaynak:**` (where the facts come from), and `**Bitti koşulu:**` (when the issue is done). Each issue also has one triage label and a milestone.
- **Branch**: `<N>-<ad>`, made by `gh issue develop <N> --name <N>-<ad> --base master` (`tansu-yeni-is` "Branch").
- **PR**: the PR body has a `Closes #N` line. The merge closes the issue.

## State of a ticket

An open ticket has exactly one triage-role label (`triage-labels.md` owns the label strings). The state comes from the label, the assignee, the PR link, and the issue state:

| Old `Status:` value | GitHub |
|---|---|
| a triage role string | the label of that role (`triage-labels.md`) |
| `claimed` | an assignee: `gh issue edit <n> --add-assignee @me` (the first write before any work). The role label stays. |
| `in-review` | an open PR with `Closes #N` in its body. The issue stays open. |
| `done (PR #N, hash)` | the issue is closed by the merge of the PR. |
| `done (kısa not)` | the issue is closed by hand with `gh issue close <n> --comment "<short note>"`. The comment says what is delivered and what moved elsewhere. |
| `resolved` | the issue is closed after the answer comment (a wayfinder child). |

A ticket is closed when the issue state is closed. A ticket is claimed when it has an assignee.

## Status field

This section keeps the old `Status:` contract. It describes only the local, read-only ticket archive under `.scratch/` and its copies in git history. GitHub and CI do not require the archive. New work does not use this contract. `triage-labels.md` owns only the role strings. The old tickets write it as `**Status:** <value>`. The value is one of:

- A triage role string from `triage-labels.md`: the ticket waits for triage or for work.
- `claimed`: work started. Set it and save before any work.
- `in-review`: the work is on its branch and waits for the independent audit or the PR review.
- `done (PR #N, hash)`: merged. The parentheses name the PR and the merge commit.
- `done (kısa not)`: delivered, not merged. The parentheses hold one short note: what is delivered and what moved elsewhere; the branch name is optional (example: ticket 06 of `belge-hizasi`). When the merge happens, the value becomes `done (PR #N, hash)`.
- `resolved`: the closing value of a wayfinder child ticket (see "Wayfinding operations").
- `done`: the legacy value of the closed tickets in the local, read-only `.scratch/arsiv/tansu-mvp/issues/` archive (before 14.10), also available in git history.

A ticket is closed when its value starts with `done` or `resolved`. (bilet 05, 14.10)

## Blocking

A `Blocked by: #N, #N` line near the top of the issue body. A ticket is unblocked when every issue it lists is closed. Do not use the native dependency feature of GitHub. One format keeps the check simple.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Read the issue as in **Read an issue**. The user normally passes the issue number.

## Wayfinding operations

Used by `mattpocock-skills:wayfinder`. The **map** is one issue. The **children** are issues.

- **Map**: one issue with the label `wayfinder:map` (create the label at first use: `gh label create wayfinder:map`). The body holds the Notes / Decisions-so-far / Fog text.
- **Child ticket**: an issue with a `Parent: #<map>` line and a `Type:` line (`research`/`prototype`/`grilling`/`task`) at the top of the body. The question is in the body.
- **Blocking**: the `Blocked by:` line above.
- **Frontier**: the open children of the map (`gh issue list --state open --search "Parent: #<map> in:body"`) without an assignee and without an open blocker. The first by number wins.
- **Claim**: `gh issue edit <n> --add-assignee @me` before any work.
- **Resolve**: `gh issue comment <n> --body "<answer>"`, then `gh issue close <n>`. Then append a context pointer (gist and link) to the Decisions-so-far in the map issue.
