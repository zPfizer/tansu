---
name: tansu-yeni-is
description: "Use when the user asks for new work in Tansu: a new feature, rule, data source, module, report, or behavior change that needs a spec, tickets, a branch, and a pull request. It runs flow A (Yeni geliştirme) in order: Sharpen, Document first, Spec, Tickets, Branch, Build, Test gate, Review, Proof, Pull request, Merge, Close."
---

# New work (Yeni geliştirme), flow A

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks.
The shared steps (Branch, Test gate, Review, Proof, Pull request, Merge, Close) are in [ortak-adimlar.md](ortak-adimlar.md). Flow B (`tansu-hata`) runs them too.

1. **Sharpen:** Define what to build: `thinking-jobs-to-be-done`. Then run `/tansu-grill` (the `vekil` subagent answers).
2. **Document first:** Write a settled term to `GLOSSARY.md` at once. Write a decision to `docs/TASARIM.md`. Read `docs/TASARIM.md` first. Read `docs/sorgu/` when it exists. It is local and not in git. Do not ask again for a decision that exists. For a document-code conflict, apply AGENTS.md "Belgeler ve sahipleri". <!-- driftlint-ignore: local-only, gitignored, absent in CI -->
3. **Spec:** `mattpocock-skills:to-spec`.
4. **Tickets:** `mattpocock-skills:to-tickets`, then `mattpocock-skills:triage`. The layout is in `docs/agents/issue-tracker.md`. Do not write a ticket by hand. If a new decision appears during the work, update the spec first. Then build the tickets again in dependency order.
5. **Branch:** Shared step. Read "Branch" in [ortak-adimlar.md](ortak-adimlar.md) and run it.
6. **Build:** For one ticket: `mattpocock-skills:implement`. For a full spec: `mattpocock-skills:implement-spec`. docs/agents/kod-kurallari.md "Önce test" owns the red-test rule. The skill is `mattpocock-skills:tdd`. While you write code: `ponytail:ponytail`. A subagent writes the code. A writer subagent writes only inside its own worktree. Apply the Observability item of DEFINITION_OF_DONE.md "Ship-readiness".
7. **Test gate:** Shared step. Read "Test gate" in [ortak-adimlar.md](ortak-adimlar.md) and run it.
8. **Review:** Shared step. Read "Review" in [ortak-adimlar.md](ortak-adimlar.md) and run it.
9. **Proof:** Shared step. Read "Proof" in [ortak-adimlar.md](ortak-adimlar.md) and run it.
10. **Pull request:** Shared step. Read "Pull request" in [ortak-adimlar.md](ortak-adimlar.md) and run it.
11. **Merge:** Shared step. Read "Merge" in [ortak-adimlar.md](ortak-adimlar.md) and run it.
12. **Close:** Shared step. Read "Close" in [ortak-adimlar.md](ortak-adimlar.md) and run it.

Task scope skips Sharpen, Spec, and Tickets. It runs Build, Test gate, and Proof. Task scope has no auditor (docs/agents/is-kurallari.md "Scope"). For a locked file, docs/agents/is-kurallari.md "Who writes" sets the review.

| If | Then |
|---|---|
| the work does not fit one session | start with `mattpocock-skills:wayfinder`. |
| the request is unclear | `thinking-socratic` (the `vekil` subagent answers). |
| the work is risky | `thinking-pre-mortem`. If it has side effects: `thinking-second-order`. |
| the work is an API | `anthropic-skills:fastapi-patterns`. |
| the work is Claude or Jev code | `claude-api` or `typesafe-ai`. |
| the work is an MCP server | `anthropic-skills:mcp-builder`. |
| two requirements conflict | `thinking-triz`. |
| an urge to add something | `thinking-via-negativa`. |
| a step only a human can do | `mattpocock-skills:wizard`. |
| the code has bloat | `ponytail:ponytail-review`. If a function is complex: `cyclomatic-complexity`. |
| the work includes untrusted input (for example downloaded data) or permissions | `thinking-red-team`. |
| the work changes an HTML report | show the proof with `anthropic-skills:built-in-browser`. |
| the work meets an operational limit or quota (for example a rate limit of a data source) | `thinking-margin-of-safety`. |
| the work is a batch content job with a fixed line rule (map lines, labels, tags) | use task scope: skip Sharpen, Spec, and Tickets. The job prompt holds the rule and the proof. (Retro 15.10) |
| the brief names a decided spec file (the edit set and its tests, decided by Levent or by the session that started the job) | Sharpen, Spec, and Tickets do not run. The PR body names the spec file in `Akış notu:`. Build runs `mattpocock-skills:implement` on the spec file. |
