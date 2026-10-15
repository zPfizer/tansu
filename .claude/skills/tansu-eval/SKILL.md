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

## Skill trigger eval

Use this part when you test whether a skill triggers on the right requests. The base is `anthropic-skills:skill-creator` "Description Optimization". These rules are permanent (Levent 16.10).

1. **Query set:** Write about 20 queries per skill. 8–10 should trigger the skill. 8–10 should not. The should-not queries are near-misses from the neighbor Tansu flow skills. Each query is as full as a real Tansu request.
2. **Runs:** Run each query 3 times. A skill counts as triggered when its rate is at least 0.5.
3. **Model:** Pass `--model` with the model ID of real Tansu sessions.
4. **Tuning:** When you tune a description, split the set: 60% train and 40% held-out. Judge only on the held-out part.
5. **Sample first:** Run a small sample first. Read its distribution. Start the full run only if the setup is clean. A clean setup has four signs:
   - No run stops because a tool is denied.
   - No run is missing.
   - No outside context is in the eval session. Global hooks and brain context are outside context.
   - No run changes a file. `--allowedTools` does not block other tools. Pass `--disallowedTools` for Edit, Write, Bash, PowerShell, and NotebookEdit. After the run, check `git status` of the project and the brain. (16.10: eval sessions acted on the queries and edited two Tansu files and the brain Threads.)

   (Reason, 16.10: in the first sample, global hooks put brain context into the eval sessions. 2 of 44 runs gave no result.)
6. **Runner:** On Windows, the eval runner of skill-creator does not work. It reads pipes with `select()`. It also tests a temporary command copy that competes with the real skill. Use a runner that calls `claude -p` with the real project skills. It reads the first Skill tool call from `--output-format stream-json --verbose`.
7. **Save:** Save the eval set, the exact command, and the results under `.scratch/<job>/` in the repository. The first set and two sample runs are in `.scratch/beceri-tetik-1610/`.
