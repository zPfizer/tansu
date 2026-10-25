---
name: tansu-eval
description: "Use when the user asks to measure, test, or judge the quality of an agent, a prompt, or a judge in Tansu: an eval case, an LLM judge, error types in session transcripts, or a measure that looks empty or unreliable. It runs flow J in order: Start, Audit the cases, Find errors, Add the case, Check the judge, No RAG, and Measure."
---

# Eval (flow J)

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true.

The steps below use base skill names. Select the callable name from the active client's skill catalog.
Codex lists these base names directly. Claude can list them as `evals:<base-name>`.
If a required skill is unavailable, report the missing capability. Do not invent a callable name or install a skill.

1. **Start:** `evals-start`.
2. **Audit the cases:** Audit the existing cases first: `eval-audit` (is the case reliable, is the judge checked, is a measure empty).
3. **Find errors:** Find the error types in the session transcripts: `error-discovery`. Astra or an Opus subagent labels the samples in place of Levent (Levent 14.10). When Levent labels, use `build-review-interface`.
4. **Add the case:** Use `write-code-eval` for rules that code can check. Test each code evaluator on known pass and fail cases. Use `write-judge-prompt` only for rules that need judgment.
5. **Check the judge:** If the evaluator uses an LLM judge, check that judge against the labels with `validate-evaluator`.
6. **No RAG:** Do not use `evaluate-rag`.
7. **Measure:** Measure only with cases that passed the audit.

| If | Then |
|---|---|
| data is scarce | `generate-synthetic-data`. |

## Skill trigger eval

Use this part when you test whether a skill triggers on the right requests. These safeguards are permanent (Levent 16.10).
The runner commands below describe the verified Claude procedure. Check the active runner's help and permission behavior before use.
Another client needs equivalent isolation with checked inputs and results. Report a missing capability instead of inventing flags.

1. **Query set:** Write about 20 queries per skill. 8–10 should trigger the skill. 8–10 should not. The should-not queries are near-misses from the neighbor Tansu flow skills, plus a few queries that need no skill. Each query is as full as a real Tansu request.
   - Use real requests first: Levent's own messages in the session transcripts (`~/.claude/projects/*TANSU*/*.jsonl` and `*YONETIM*`). Do not use tool results, system text, session briefs, or eval sessions.
   - Write the other queries in his voice: he states a goal or pastes an error, in long spoken sentences. He does not compare tools or name techniques. A technical query is an agent brief: write it in English STE, because other sessions send English briefs to Tansu.
   - Most of his real messages are status questions, approvals, merges, and "continue". The no-skill group holds many of them. A flow that starts on "evet" or "birleştir" is the most costly false trigger.
   - Columns: expected skill, source (`gercek` real, `yazili` written, `brif` agent brief), also-correct skill (`-` or a skill such as `tansu-grill` whose description also covers the query; a run that loads it is correct), query.
   - Do not put a literal trigger phrase of a description into a query.
   - Remove each query that names a thing that does not exist now. Check AGENTS.md "Current state", TASARIM, and the code.
2. **Review the set:** Levent picks the tool for the session that audits the set. That session must know him. Check voice, distribution, current facts, and label overlap. Levent does not review sets (brain note `levent-calisma-oruntuleri`, item 2). Start no run before the auditor's approval.
3. **Runs:** Run each query 3 times. A skill counts as triggered when its rate is at least 0.5.
4. **Model:** Pass `--model` with the model ID of real Tansu sessions.
5. **Tuning:** When you tune a description, split the set: 60% train and 40% held-out. Judge only on the held-out part.
6. **Sample first:** Run a small sample first. Read its distribution. Start the full run only if the setup is clean. A clean setup has four signs:
   - No run ends without a `result` line because a tool is denied. A blocked call that lets the run continue is allowed ("Isolation").
   - No run is missing.
   - No outside context is in the eval session. "Isolation" removes the hooks.
   - No run changes a file. "Isolation" sets the controls.

   (Reason, 16.10: in the first sample, hooks put brain context into the eval sessions, and 2 of 44 runs gave no result. In the second sample, eval sessions acted on the queries and edited two Tansu files and the brain Threads.)
7. **Isolation:** Every eval run obeys these rules. Check the runner's actual permission mode before the sample.
   In Claude bypass mode, `--allowedTools` pre-approves tools but does not block other tools. Use the restrictions below.
   - Run in a disposable copy: `git worktree add --detach <temporary folder outside every Tansu worktree> <branch>`.
     The copy must hold the committed skill files under test. Preserve the evidence after the runs.
     Before removing the copy, check pending changes and active jobs. Get approval for its named deletion under AGENTS.md "Every job".
   - Delete the `hooks` key in `<copy>/.claude/settings.json`. The user file `~/.claude/settings.json` also has hooks: pass `--settings '{"disableAllHooks": true}'` (bash quoting) to disable all hooks.
   - Pass `--include-hook-events`. Check that each stream file has no hook event.
   - Pass `--disallowedTools "Bash PowerShell Edit Write NotebookEdit Agent ToolSearch Monitor"`, `--allowedTools "Skill Read Grep Glob"`, `--permission-mode default`, and `--strict-mcp-config`. (Reason, 16.10: in the set 2 measure, ToolSearch loaded the deferred tool Monitor, and one run tried to run pytest with Monitor. `--permission-mode default` blocked it.)
   - Before and after the runs, record `git status --porcelain` and `git log -1` of the copy and of `C:\Users\levent\Desktop\YONETIM\beyin`. Take the "before" record after you edit the settings of the copy and before the first run. Do this check even though the hooks are off. If a value changed, stop and find the cause. If an eval run caused the change, all runs are invalid.
   - A run in which a tool from the `--disallowedTools` list or an `mcp__` tool ran is invalid. A blocked call does not make a run invalid. A blocked call has the result text "No such tool available" or a permission denial ("requires approval"). Any other result means that the tool ran. A run without a `result` line is invalid. An invalid run is not a miss: run it again. Check the tool names and tool results in each stream file. (Reason, 16.10: a query that asks for an edit makes the model try Edit after it loads the skill. The model tries it in each run of that query.)
8. **Runner:** The skill-creator runner tested on 16.10 failed on Windows because it used `select()` for pipes.
   It also tested a temporary command copy that competed with the real skill.
   For the verified Claude path, call `claude -p` with the real project skills and the "Model" and "Isolation" flags.
   Run the runner in bash (Git Bash). Read the first Skill tool call from `--output-format stream-json --verbose`.
   Give each `claude -p` call `< /dev/null`.
   Reason, 16.10: the second sample read the remaining query file from the loop's standard input.
   Those lines entered the prompt, and the last two queries did not run.
9. **Save:** Save the eval set, the exact command, and the results under the local, gitignored temporary folder `.scratch/<job>/`. These files are not versioned repository artifacts. The first set and two sample runs exist only in git history. Read them with `git show 8c5f06c^:.scratch/beceri-tetik-1610/<path>`. The second set, from real requests, is also historical: `git show 8c5f06c^:.scratch/beceri-tetik-1610/sorgular-2.tsv`. GitHub and CI do not require local copies.
