---
name: tansu-yeni-is
description: "Use for new Tansu work, including a feature, rule, data source, module, report, or behavior change. Flow A prepares one brief, records decisions, builds the change, checks evidence, and delivers it."
---

# New work (Yeni geliştirme), flow A

Use AGENTS.md "Work flow" for the method and required agent roles. This flow adds the TANSU source and delivery gates.
Apply [Scope](../../../docs/agents/is-kurallari.md#scope) before the steps. Branch, PR, and merge steps apply only to authorized delivery.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Brief:** Use the supplied ticket or decided spec when it defines the goal, scope, and acceptance criteria.
   Resolve source questions through `tansu-grill`. Use recorded decisions before asking Levent.
   Write the goal, scope, behavior, interfaces, and testable acceptance criteria.
   Keep the affected file, heading, and content map in the local job record. Copy that map into delegate briefs.
   Key the map by heading text or rule ID, not line number.
   Keep the public issue brief focused on behavior and interfaces, as [Issue body](../../../docs/agents/issue-tracker.md#issue-body) requires.
   For one delivery, keep one issue. Split independent deliveries or dependencies under a spec issue.
   If a decision changes, update the spec first, then the affected tickets in dependency order.
2. **Document first:** Write a settled term to `GLOSSARY.md` at once. Write product decisions to `docs/TASARIM.md`. Put work rules in their owner from AGENTS.md. Read `docs/TASARIM.md` first. Read `docs/sorgu/` when it exists. It is local and not in git. Record an approved contract before code. Mark it as pending until implementation and evidence are complete. Keep undecided proposals in the spec or ticket. Never describe pending behavior as implemented. Do not ask again for a decision that exists. For a document-code conflict, apply AGENTS.md "Belgeler ve sahipleri". <!-- driftlint-ignore: local-only, gitignored, absent in CI -->
3. **Branch:** Run [Branch](../../../docs/agents/is-kurallari.md#branch).
4. **Build:** Implement the brief's acceptance criteria. For a split spec, implement tickets in dependency order.
   Apply `CODING_STANDARDS.md` "Test first". A writer subagent writes only inside its assigned worktree.
   Give it the ticket or decided spec, scope restrictions, and test-first rules.
   The writer reports the skills used and supplies the actual evidence required by `CODING_STANDARDS.md` "Test first".
   The Claude hook's limited coverage is in AGENTS.md "Environment". Apply DEFINITION_OF_DONE.md "Ship-readiness" for a new critical path.
5. **Check and evidence:** Run [Check and evidence](../../../docs/agents/is-kurallari.md#check-and-evidence) before review.
6. **Review:** Run [Review](../../../docs/agents/is-kurallari.md#review) when risk requires it.
7. **Pull request:** Run [Pull request](../../../docs/agents/is-kurallari.md#pull-request).
8. **Merge:** Run [Merge](../../../docs/agents/is-kurallari.md#merge).
9. **Close:** Run [Close](../../../docs/agents/is-kurallari.md#close).

Task scope uses the supplied brief. It needs no separate needs interview, spec, or ticket split. Run the applicable shared steps. Review follows risk in `docs/agents/is-kurallari.md` "Auditor and rounds", including locked files.

| If | Then |
|---|---|
| the work does not fit one session | Apply docs/agents/issue-tracker.md "Wayfinding operations" to track questions, decisions, and next tasks. |
| the work is an API | Read the official documentation for the installed framework. Define request, response, validation, and error contracts. Use the existing framework and affected tests. |
| the work is an MCP server | Read the official MCP documentation for the installed SDK. Define tool inputs and outputs. Check tool calls with the available shell tools in a local test. |
| a step only a human can do | Give Levent the required action and its purpose. Wait for the result before dependent work. |
| the work changes an HTML report | Use browser control available in the active session. Open the report through the project's local server. Check the changed behavior and retain browser evidence. If browser control is unavailable, report the check as blocked. |
| the work is a batch content job with a fixed line rule (map lines, labels, tags) | Use task scope and the supplied brief. The job prompt holds the rule and the proof. (Retro 15.10) |
| the brief names a spec that Levent or the starting session decided, with the edit set and tests. | Use that spec. Do not repeat the interview, spec, or ticket split. Name the spec file in `Akış notu:` in the PR body. Build implements that spec. |
