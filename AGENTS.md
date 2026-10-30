# TANSU agent instructions

This file owns the shared entry for Codex and Claude. Read the relevant owner documents below before work.
The live rebuild runs on branch `yeniden-kurulus`. That branch owns its rules in its own `AGENTS.md`. In that worktree, follow that file, not this one.

## Every job

- Start replies to Levent with "Patron,". Use plain Turkish. State the result first and name the remaining work.
- Keep updates short. Answer every question. Explain technical terms only when needed.
- Write delegated reports in English ASD-STE100. Give the owner, changed files, commands, results, skipped checks, and open questions.
- Follow Levent's chosen tool and direction. Make routine technical decisions within the approved scope.
- **Ask Levent:** Ask about money, scope, direction, taste, and product decisions when authoritative sources do not settle them.
- Honor explicit file lists and read-only limits. Otherwise, change only files needed for the requested result.
- Get specific approval before deletion, reset, destructive actions, or irreversible writes. General autonomy does not grant this approval.
- Send external messages only with explicit authorization. Keep secrets out of files and output. Honor privacy and network limits.
- Add no dependency without Levent's approval. Leave third-party tools and plugins unchanged.
- Read current files before edits. Preserve other sessions' changes. Give each file one writer and keep edits small and reversible.
- Use primary sources first, then official sources. Separate facts, inference, and unknowns. Never invent evidence.
- Complete authorized work. If repeated reads or edits make no progress, report the obstacle.

## Work flow

Use the skill Levent names. For nontrivial work without a narrower named workflow, use the installed `pstack:poteto-mode` skill.
Simple questions need no full playbook. Read the selected skill and its required references before use.
Read `C:/Users/levent/.cursor/rules/pstack-models.mdc` when pstack requires model selection. If absent, use the installed skill defaults.
Use native tools for the skill's method. Preserve required roles and review independence. Report unavailable capabilities and checks.
When the workflow requires agents, pass the full scope and restrictions. Read and check their work before reporting it.

For normal project sessions, follow [Standing project coordinator](docs/agents/yonetici.md).
An explicit delegated job keeps its assigned role and scope. A bounded request does not start unrelated release work.
Use Orchestrate for the standing project program. Select the matching pstack playbook for a bounded task.

The local flows add TANSU safeguards to the selected method. Read only the applicable flow.

| Task | Local owner |
|---|---|
| New behavior | `.claude/skills/tansu-yeni-is/SKILL.md` |
| Fault diagnosis and correction | `.claude/skills/tansu-hata/SKILL.md` |
| Documents and instructions | `.claude/skills/tansu-belge/SKILL.md` |
| Plans and decisions | `.claude/skills/tansu-karar/SKILL.md` |
| Source-based design questions | `.claude/skills/tansu-grill/SKILL.md` |
| Agent and prompt evaluation | `.claude/skills/tansu-eval/SKILL.md` |
| Source research, questions, and sessions | `docs/agents/is-kurallari.md` "Short flows and skill naming" |

Project sources own product rules. Project delivery rules own evidence, Git, and approval gates. pstack owns general work methods.
Task scope and explicit user restrictions apply to every step. Optional helpers apply only when relevant.
For source context and recorded decisions, use the brain search procedure in `docs/agents/yonetici.md` "Sources and procedures".

## Documents and owners (Belgeler ve sahipleri)

Keep each fact in its owner. Link to it instead of copying its rule into another document.
Before changing behavior, read its source and approved contract. Record approved changes before implementation, as the local new-work flow requires.
If code and a document disagree, identify the authoritative source and the implementation status before changing either.
Ask Levent when that evidence leaves a product decision unresolved.

| File | Fact that the file owns |
|---|---|
| `AGENTS.md` | Shared agent entry, communication, scope, and workflow routing. |
| `CLAUDE.md` | Claude entry that imports the shared instructions. |
| `GLOSSARY.md` | Terms and source evidence labels. |
| `docs/TASARIM.md` | Product behavior, approved decisions, and implementation status. |
| `docs/KURALLAR.md` | Rule-family index. |
| `docs/aile-kurallari.md` | Family definitions, formulas, and source reading rules. |
| `docs/kaynak-dokumu.md` | Source identities and exclusion reasons. |
| `docs/sadakat.md` | Fidelity measurements and their evidence. |
| `docs/kurallar/A-yapi-bolge.md` | Structure and price-zone sources. |
| `docs/kurallar/B-momentum-sikisma.md` | Momentum and compression sources. |
| `docs/kurallar/C-harmonik-geometri.md` | Harmonic and geometry sources. |
| `docs/kurallar/D-cift-portfoy-nabiz.md` | Pair, portfolio, and market-pulse sources. |
| `docs/kurallar/E-risk-cikis-surec.md` | Risk, exit, and process sources. |
| brain pool: `kisisel/300-Projects/Tansu X Veri Havuzu/` | Original notes and images under the external YONETIM brain root. |
| `CODING_STANDARDS.md` | TANSU code, test, and source-proof requirements. |
| `DEFINITION_OF_DONE.md` | Completion criteria and required evidence. |
| `docs/agents/is-kurallari.md` | Delivery, checks, review, Git, and release procedure. |
| `docs/agents/issue-tracker.md` | Issue and PR format, scope, and work tracking. |
| `docs/agents/yonetici.md` | Standing coordinator authority, shared checkpoint, brain search, and release approval. |
| `docs/agents/zamanlayici.md` | Task Scheduler definitions and operations. |
| `CHANGELOG.md` | Published and unpublished changes. |

## Environment

Use PowerShell on Windows. Read and write text as UTF-8. Run Python with `-X utf8`.
Use the existing main virtual environment, including from a worktree. Its path is in `docs/agents/is-kurallari.md` "Branch".
Put temporary output in the system temporary folder. Do not create a script file for one operation.
Read `pyproject.toml`, `requirements.lock.txt`, and the workflows for current versions.
A CI tool outside Python is pinned to an exact version in the workflow file.

- **Names (Adlar):** Use Turkish ASCII for CSV headers. Use the approved names in `docs/TASARIM.md`.
- **Dependency:** Read TASARIM §4 before proposing a new package. Follow the approval rule in "Every job".

The Claude edit hook in `kurulum/kanca.py` checks for test changes through selected edit events.
For a pure refactor with unchanged tests, its `refactor-before` and `refactor-after` commands record actual test runs.
Read `kurulum/kanca.py --help` for that path. Its file fingerprints exclude Git-ignored files and external inputs.
Passing tests do not prove behavior equivalence.
It cannot prove a red test run. It does not cover shell edits or other clients. Follow the test rules in every client.

## Current state

Read current state when needed. Use `git status --short`, `git log -1`, and the relevant source files.
Read `docs/TASARIM.md` for implementation status and `CHANGELOG.md` for recorded changes.
For delivery status, read the current issue, PR, and coordinator checkpoint under the coordinator contract.
Do not treat a historical report or an approved pending contract as proof of current behavior.

## Check and deliver

Follow `docs/agents/is-kurallari.md` for affected checks, evidence, review, commits, PRs, and merge.
Apply `DEFINITION_OF_DONE.md` before claiming completion. Inspect the actual output and identify skipped checks.
Merge only with Levent's explicit approval. Preserve branches and worktrees unless he approves their cleanup.
Report what changed, how you checked it, and any remaining work or approval gate.
