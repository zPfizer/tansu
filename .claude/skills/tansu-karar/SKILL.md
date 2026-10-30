---
name: tansu-karar
description: "Use when the user asks to plan, compare options, or decide something in Tansu. This includes design choices, tool choices, trade-offs, large or hard-to-undo decisions, and requests such as plan yap. Flow D checks the proposal, applies methods when needed, asks Levent for direction, and records the result."
---

# Plan or decision (flow D)

Scope: the main checkout. The `yeniden-kurulus` worktree has no `docs/agents/`; there, follow its `AGENTS.md`.

Use AGENTS.md "Work flow" for the decision method. This flow adds source authority and the decision record.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Stress-test:** Question the assumptions, alternatives, risks, and acceptance criteria of the proposal. The main session answers from sources and recorded decisions.
2. **Direction:** Resolve technical facts from sources and recorded decisions.
   Ask Levent about unresolved decisions reserved for him by AGENTS.md "Every job".
3. **Result:** Record settled terms and product decisions through `tansu-yeni-is` "Document first".
   Apply [Close](../../../docs/agents/is-kurallari.md#close) within the job scope.

| If | Then |
|---|---|
| Levent says "plan yap" | Use the selected workflow from AGENTS.md "Work flow". Show the plan with the tools available in the active session. |
| another person must fill in the answers | Write a questionnaire. Give each question the context and the decision that its answer affects. |
