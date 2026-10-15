# Issue tracker: GitHub

Specs and tickets of this repo live as GitHub issues in `zPfizer/tansu-kaynak` (remote `kaynak`). Use the `gh` CLI for all operations. `gh` finds the repo from `git remote -v`.

`.scratch/` is an archive only. Old tickets and specs stay there to be read. An open ticket has one place: its issue. Never track the same ticket in both places. When an old ticket moves to an issue, its file keeps one line with the issue link and nothing else changes.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body-file <file>` (or `--body` with a heredoc).
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,assignees,state,comments`.
- **List issues**: `gh issue list --state open --json number,title,labels,assignees` with `--label` and `--state` filters.
- **Comment**: `gh issue comment <number> --body "..."`.
- **Labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`.
- **Close**: `gh issue close <number> --comment "..."`.
- **Spec**: one issue, title `Spec: <name>`. The tickets name it in a `Parent: #N` line.
- **Ticket body**: the same layout as the old ticket files: What to build, `Blocked by:` line, acceptance criteria as `- [ ]` boxes. The issue number replaces the ticket number `NN`.
- **Branch and PR**: branch `pr/<issue number>-<ad>`. The PR body has a `Closes #N` line.

## State of a ticket

This file owns the state contract. `triage-labels.md` owns only the label strings. An open ticket has exactly one triage-role label. The state comes from the label, the assignee, the PR link, and the issue state:

| Old `Status:` value | GitHub |
|---|---|
| a triage role string | the label of that role (`triage-labels.md`) |
| `claimed` | an assignee: `gh issue edit <n> --add-assignee @me` (the first write before any work). The role label stays. The cloud agent run sets it too. |
| `in-review` | an open PR with `Closes #N` in its body. The issue stays open. |
| `done (PR #N, hash)` | the issue is closed by the merge of the PR. |
| `done (kısa not)` | the issue is closed by hand with `gh issue close <n> --comment "<short note>"`. The comment says what is delivered and what moved elsewhere. |
| `resolved` | the issue is closed after the answer comment (a wayfinder child). |

A ticket is closed when the issue state is closed. A ticket is claimed when it has an assignee.

Two labels are not roles. They sit beside the role label: `yerel` (the ticket needs the brain pool, `veri/`, or a real snapshot; the cloud agent never runs it, only a local session does) and the PR labels `ci-kirmizi` and `inceleme-gecti` (see `triage-labels.md`).

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
