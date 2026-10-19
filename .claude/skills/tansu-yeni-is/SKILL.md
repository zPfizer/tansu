---
name: tansu-yeni-is
description: "Use for new Tansu work, including a feature, rule, data source, module, report, or behavior change. Flow A prepares one brief, records decisions, builds the change, checks evidence, and delivers it."
---

# New work (Yeni geliştirme), flow A

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks.
The shared steps are in [Job rules](../../../docs/agents/is-kurallari.md#branch). Flows B and C use the same owners.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Brief:** Use the supplied ticket or decided spec when it defines the goal, scope, and acceptance criteria. For an open need, use `thinking-jobs-to-be-done` and `/tansu-grill`. The main session answers from sources and recorded decisions. Write the goal, scope, behavior, interfaces, and testable acceptance criteria. Key tables by heading text or rule ID, never by line number. A spec has a "Where" table with the file, heading, and content. Copy that table into subagent prompts. For one delivery, keep one issue with the required brief. Split independent deliveries or dependencies into tickets under a spec issue. Follow `docs/agents/issue-tracker.md` for the layout and dependency order. If a decision changes, update the spec first. Then update the affected tickets in dependency order.
2. **Document first:** Write a settled term to `GLOSSARY.md` at once. Write a decision to `docs/TASARIM.md`. Read `docs/TASARIM.md` first. Read `docs/sorgu/` when it exists. It is local and not in git. Do not ask again for a decision that exists. For a document-code conflict, apply AGENTS.md "Belgeler ve sahipleri". <!-- driftlint-ignore: local-only, gitignored, absent in CI -->
3. **Branch:** Run [Branch](../../../docs/agents/is-kurallari.md#branch).
4. **Build:** Implement the brief's acceptance criteria. For a split spec, implement tickets in dependency order. Apply `CODING_STANDARDS.md` "Test first". While you write code, use `ponytail:ponytail`. For a small, defined task, the assigned writer session writes directly. Use writer subagents for large jobs or independent parts. A writer subagent writes only inside its own worktree. Give it the ticket or decided spec and the test-first rules. Its prompt names `ponytail:ponytail`. It calls that skill and lists its Skill calls in its report. The hook of AGENTS.md "Environment" blocks a code edit when no test changed first. Apply DEFINITION_OF_DONE.md "Ship-readiness" for a new critical path.
5. **Check and evidence:** Run [Check and evidence](../../../docs/agents/is-kurallari.md#check-and-evidence) before review.
6. **Review:** Run [Review](../../../docs/agents/is-kurallari.md#review) when risk requires it.
7. **Pull request:** Run [Pull request](../../../docs/agents/is-kurallari.md#pull-request).
8. **Merge:** Run [Merge](../../../docs/agents/is-kurallari.md#merge).
9. **Close:** Run [Close](../../../docs/agents/is-kurallari.md#close).

Task scope uses the supplied brief. It needs no separate needs interview, spec, or ticket split. Run the applicable shared steps. Review follows risk in `docs/agents/is-kurallari.md` "Auditor and rounds", including locked files.

| If | Then |
|---|---|
| the work does not fit one session | Apply docs/agents/issue-tracker.md "Wayfinding operations" to track questions, decisions, and next tasks. |
| the request is unclear | `thinking-socratic`. The main session answers from sources and recorded decisions. Apply AGENTS.md "Every job" for questions to Levent. |
| the work is risky | `thinking-pre-mortem`. If it has side effects: `thinking-second-order`. |
| the work is an API | Read the official documentation for the installed framework. Define request, response, validation, and error contracts. Use the existing framework and affected tests. |
| the work is Claude or Jev code | `claude-api` or `typesafe-ai`. |
| the work is an MCP server | Read the official MCP documentation for the installed SDK. Define tool inputs and outputs. Check tool calls with the available shell tools in a local test. |
| two requirements conflict | `thinking-triz`. |
| an urge to add something | `thinking-via-negativa`. |
| a step only a human can do | Give Levent the required action and its purpose. Wait for the result before dependent work. |
| the code has bloat | `ponytail:ponytail-review`. If a function is complex: `cyclomatic-complexity`. |
| the work includes untrusted input (for example downloaded data) or permissions | `thinking-red-team`. |
| the work changes an HTML report | Use browser control available in the active session. Open the report through the project's local server. Check the changed behavior and retain browser evidence. If browser control is unavailable, report the check as blocked. |
| the work meets an operational limit or quota (for example a rate limit of a data source) | `thinking-margin-of-safety`. |
| the work is a batch content job with a fixed line rule (map lines, labels, tags) | Use task scope and the supplied brief. The job prompt holds the rule and the proof. (Retro 15.10) |
| the brief names a spec that Levent or the starting session decided, with the edit set and tests. | Use that spec. Do not repeat the interview, spec, or ticket split. Name the spec file in `Akış notu:` in the PR body. Build implements that spec. |
