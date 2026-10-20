---
name: tansu-karar
description: "Use when the user asks to plan, compare options, or decide something in Tansu. This includes design choices, tool choices, trade-offs, large or hard-to-undo decisions, and requests such as plan yap. Flow D checks the proposal, applies methods when needed, asks Levent for direction, and records the result."
---

# Plan or decision (flow D)

Run AGENTS.md "Every job" first. Run the steps in order. Run a conditional step or an "If" row only when its condition is true. Call each skill by the exact name in backticks.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Stress-test:** Question the assumptions, alternatives, risks, and acceptance criteria of the proposal. The main session answers from sources and recorded decisions.
2. **Compare options:** If the choice needs a structured comparison of trade-offs: `thinking-kepner-tregoe`.
3. **Life of a tool:** If the decision depends on the long-term survival of a technology or practice: `thinking-lindy-effect`.
4. **Large decision:** If one method leaves a material gap in a complex or high-stakes decision: `thinking-model-combination`.
5. **Value:** If the commitment displaces other valuable work: `thinking-opportunity-cost`.
6. **Forecast:** If the decision needs a forecast or an uncertain estimate: `thinking-probabilistic`.
7. **Rejection:** Before you reject a proposal: `thinking-steel-manning`.
8. **Direction:** The main session asks Levent for the direction decision. Apply AGENTS.md "Every job" for decisions reserved for Levent.
9. **Result:** Write the result to the brain as `tansu-yeni-is` "Close" says.

| If | Then |
|---|---|
| a constraint looks fixed | `thinking-first-principles`. |
| you cannot test the idea | `thinking-thought-experiment`. |
| the effort is uncertain | `thinking-effectuation`. |
| the decision cannot be undone | `thinking-reversibility`. |
| Levent says "plan yap" | `html-plan:html-plan`. |
| another person must fill in the answers | Write a questionnaire. Give each question the context and the decision that its answer affects. |
| a design question is still open after 2 turns of text | Build a trial of at most 10 minutes. Observe the result, then decide. |
