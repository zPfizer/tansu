---
name: tansu-eval
description: "Use when the user asks to measure, test, or judge the quality of an agent, a prompt, or a judge in Tansu: an eval case, an LLM judge, error types in session transcripts, or a measure that looks empty or unreliable. It runs flow J in order: Start, Audit the cases, Find errors, Add the case, Check the judge, No RAG, and Measure."
---

# Eval (flow J)

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks.

1. **Start:** `evals:evals-start`.
2. **Audit the cases:** Audit the existing cases first: `evals:eval-audit` (is the case reliable, is the judge checked, is a measure empty).
3. **Find errors:** Find the error types in the session transcripts: `evals:error-discovery`. Astra or an Opus subagent labels the samples in place of Levent (Levent 14.10). When Levent labels, use `evals:build-review-interface`.
4. **Add the case:** For each error type, if code can measure it: `evals:write-code-eval`. If it needs a judge: `evals:write-judge-prompt`.
5. **Check the judge:** Check the judge against the labels: `evals:validate-evaluator`.
6. **No RAG:** Do not use `evals:evaluate-rag`.
7. **Measure:** Measure only with cases that passed the audit.

| If | Then |
|---|---|
| data is scarce | `evals:generate-synthetic-data`. |
