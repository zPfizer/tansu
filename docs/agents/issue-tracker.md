# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file
- State is recorded as one `Status:` line near the top of each issue file (see "Status field" below)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Status field

This file owns the contract of the `Status:` line. `triage-labels.md` owns only the role strings. The tickets write it as `**Status:** <value>`. The value is one of:

- A triage role string from `triage-labels.md`: the ticket waits for triage or for work.
- `claimed`: work started. Set it and save before any work.
- `in-review`: the work is on its branch and waits for the independent audit or the PR review.
- `done (PR #N, hash)`: merged. The parentheses name the PR and the merge commit.
- `done (dal, kısa not)`: delivered on its branch, not merged. The parentheses name the branch and one short note (what is delivered, what moved elsewhere). When the merge happens, the value becomes `done (PR #N, hash)`.
- `resolved`: the closing value of a wayfinder child ticket (see "Wayfinding operations").

A ticket is closed when its value starts with `done` or `resolved`. (bilet 05, 14.10)

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by `mattpocock-skills:wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` (the Notes / Decisions-so-far / Fog body).
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); the `Status:` line follows "Status field" above (`claimed`, then `resolved`).
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is closed (`resolved` or `done`).
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
