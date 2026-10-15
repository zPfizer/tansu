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

1. **Query set:** Write about 20 queries per skill. 8–10 should trigger the skill. 8–10 should not. The should-not queries are near-misses from the neighbor Tansu flow skills, plus a few queries that need no skill. Each query is as full as a real Tansu request.
   - Use real requests first: Levent's own messages in the session transcripts (`~/.claude/projects/*TANSU*/*.jsonl` and `*YONETIM*`). Do not use tool results, system text, session briefs, or eval sessions.
   - Write the other queries in his voice: he states a goal or pastes an error, in long spoken sentences. He does not compare tools or name techniques. A technical query is an agent brief: write it in English STE, because other sessions send English briefs to Tansu.
   - Most of his real messages are status questions, approvals, merges, and "continue". The no-skill group holds many of them. A flow that starts on "evet" or "birleştir" is the most costly false trigger.
   - Columns: expected skill, source (`gercek` real, `yazili` written, `brif` agent brief), also-correct skill (`-` or a skill such as `tansu-grill` whose description also covers the query; a run that loads it is correct), query.
   - Do not put a literal trigger phrase of a description into a query.
   - Remove each query that names a thing that does not exist now. Check AGENTS.md "Current state", TASARIM, and the code.
2. **Review the set:** Before any run, a Claude session that knows Levent audits the set for fit to him: voice, distribution, current facts, label overlap. Levent does not review sets (Levent 16.10; brain note `levent-calisma-oruntuleri` item 2). Start no run before the auditor's go. (Reason, 16.10: the first set was written by a model, partly out of date, and not reviewed. skill-creator "Description Optimization" requires a review of the set.)
3. **Runs:** Run each query 3 times. A skill counts as triggered when its rate is at least 0.5.
4. **Model:** Pass `--model` with the model ID of real Tansu sessions.
5. **Tuning:** When you tune a description, split the set: 60% train and 40% held-out. Judge only on the held-out part.
6. **Sample first:** Run a small sample first. Read its distribution. Start the full run only if the setup is clean. A clean setup has four signs:
   - No run stops because a tool is denied.
   - No run is missing.
   - No outside context is in the eval session. "Isolation" removes the hooks.
   - No run changes a file. "Isolation" sets the controls.

   (Reason, 16.10: in the first sample, hooks put brain context into the eval sessions, and 2 of 44 runs gave no result. In the second sample, eval sessions acted on the queries and edited two Tansu files and the brain Threads.)
7. **Isolation:** Every eval run obeys these rules. This machine runs in bypass permission mode. So `--allowedTools` only pre-approves tools and does not block other tools.
   - Run in a disposable copy: `git worktree add --detach <temporary folder outside every Tansu worktree> <branch>`. The copy must hold the committed skill files under test. Remove the copy after the runs.
   - Delete the `hooks` key in `<copy>/.claude/settings.json`. The user file `~/.claude/settings.json` also has hooks: pass `--settings '{"disableAllHooks": true}'` (bash quoting) to disable all hooks.
   - Pass `--include-hook-events`. Check that each stream file has no hook event.
   - Pass `--disallowedTools "Bash PowerShell Edit Write NotebookEdit Agent"`, `--allowedTools "Skill Read Grep Glob"`, `--permission-mode default`, and `--strict-mcp-config`.
   - Before and after the runs, record `git status --porcelain` and `git log -1` of the copy and of `C:\Users\levent\Desktop\YONETIM\beyin`. Take the "before" record after you edit the settings of the copy and before the first run. Do this check even though the hooks are off. If a value changed, stop and find the cause. If an eval run caused the change, all runs are invalid.
   - A run that tried to call a tool from the `--disallowedTools` list or an `mcp__` tool is invalid. A run without a `result` line is invalid. An invalid run is not a miss: run it again. Check the tool names in each stream file.
8. **Runner:** On Windows, the eval runner of skill-creator does not work. It reads pipes with `select()`. It also tests a temporary command copy that competes with the real skill. Use a runner that calls `claude -p` with the real project skills and the flags of "Model" and "Isolation". Run the runner in bash (Git Bash). It reads the first Skill tool call from `--output-format stream-json --verbose`. Give each `claude -p` call `< /dev/null`. (Reason, 16.10: in the second sample, `claude -p` read the rest of the query file from the loop's standard input. It added those lines to the prompt, and the last two queries did not run.)
9. **Save:** Save the eval set, the exact command, and the results under `.scratch/<job>/` in the repository. The first set and two sample runs are in `.scratch/beceri-tetik-1610/`. The second set, from real requests, is `sorgular-2.tsv` there.
