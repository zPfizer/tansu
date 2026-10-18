---
name: tansu-karar
description: "Use when the user asks to plan, compare options, or decide something in Tansu: a design choice, a tool choice, a trade-off, a large or hard-to-undo decision, or a request such as plan yap. It runs flow D in order: Stress-test, Compare options, Life of a tool, Large decision, Value, Forecast, Rejection, Direction, and Result."
---

# Plan or decision (flow D)

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Stress-test:** `mattpocock-skills:grilling` (the `vekil` subagent answers).
2. **Compare options:** `thinking-kepner-tregoe`.
3. **Life of a tool:** `thinking-lindy-effect`.
4. **Large decision:** `thinking-model-combination`.
5. **Value:** `thinking-opportunity-cost`.
6. **Forecast:** `thinking-probabilistic`.
7. **Rejection:** Before you reject a proposal: `thinking-steel-manning`.
8. **Direction:** Ask Levent a direction decision. The `vekil` subagent returns it as "Ask Levent".
9. **Result:** Write the result to the brain as `tansu-yeni-is` "Close" says.

| If | Then |
|---|---|
| a constraint looks fixed | `thinking-first-principles`. |
| you cannot test the idea | `thinking-thought-experiment`. |
| the effort is uncertain | `thinking-effectuation`. |
| the decision cannot be undone | `thinking-reversibility`. |
| Levent says "plan yap" | `html-plan:html-plan`. |
| another person must fill in the answers | `mattpocock-skills:to-questionnaire`. |
| a design question is still open after 2 turns of text | `mattpocock-skills:prototype`: a trial of at most 10 minutes, then decide. |
