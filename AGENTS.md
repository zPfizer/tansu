# TANSU

TANSU is a daily signal and backtest (sınama) system for BIST. Tansu inspired it. The code follows the documents.
The behavior does not change before a document changes.

## Current state (Şimdiki durum)
This section holds temporary states only. Each line has a date and an owner. Delete a line when its end condition is true.

## Documents and owners (Belgeler ve sahipleri)
Each fact has one owner file. The other files only give a reference to it. Read the files in the order of the table.

| File | Fact that the file owns |
|---|---|
| `GLOSSARY.md` | the meaning of the terms |
| `docs/TASARIM.md` | numbers, formulas, behavior, and decisions. §7 is the order of implementation |
| `docs/KURALLAR.md` | the family (aile) rules and the YORUM entries (§3–4) |
| brain (beyin): `kisisel/300-Projects/Tansu X Veri Havuzu/` (outside the repository) | the raw posts of Tansu: notes and images. This is a raw source. Do not change it |
| `docs/kurallar/A-yapi-bolge.md` … `E-risk-cikis-surec.md` | the reading of the pool (havuz): what Tansu said. Rule: each note in the pool must have a reference here or must be in the "kural içermez" list |
| `docs/sadakat.md` | the fidelity (sadakat) measurement |
| `AGENTS.md` | the entry, the working rules, the current state, the job rules (Every job, Scope, Who writes, Auditor and rounds), and the work flow table |
| `.claude/skills/` | the work flow procedures, one skill per job type |
| `docs/strateji-taslak/`, `docs/strateji-modulleri-taslak.md` (local, not in git) | proposals that wait for approval. They own no fact. They are outside the drift check. These local files need not exist <!-- driftlint-ignore: local-only, gitignored, absent in CI --> |
| `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md` | the Tansu code rules (`## Tansu`; the general rules are in the file that `CODING_STANDARDS.md` points to) and the done criteria (`## Tansu`) |
| `docs/sorgu/sonuc-3-4.md`, `docs/sorgu/izleme/karar.md` (local, not in git) | the reasons for the decisions (read them when necessary and when they exist) <!-- driftlint-ignore: local-only, gitignored, absent in CI --> |

The drift check covers all these files. Correct a file when it contradicts another file, contains old information,
or copies a fact of another file.

If a document and the code contradict, or if the document says nothing about the case, stop. Correct the document
first. Write the reason. Then write the code.

## Every job
1. Write the intent of Levent and the flow letter in one line at the top of the first reply. All text that Levent can see is Turkish, also the wrap_up text.
2. Read the section "Current state" (Şimdiki durum) of this file.
3. If the work type is unclear: `mattpocock-skills:ask-matt`.
4. Send a design or technical question that needs the preference of Levent to the `vekil` subagent first. Levent gets only these: direction of the project, money, outgoing work, secrets, and delete. Levent also gets a Task Scheduler change and work that cannot be undone.
5. Before you write an instruction or a prompt: `asd-ste100`.
6. If you cannot show a source for a claim: `thinking-circle-of-competence`.
7. If the problem type is unclear: `thinking-cynefin`. If the method is unclear: `thinking-model-router`.
8. Choose the flow and the scope (section "Scope" of this file).

## Work flow (İş akışı)
Tansu has no flow F (memory) and no flow G (company output). They stay in the brain.
Choose the flow by the work type. Call each skill by the exact name in backticks. Open the skill of the flow before the first step. Run the steps in order. Run an "If" row only when its condition is true.

| Work type | Flow | Skill |
|---|---|---|
| new work (Yeni geliştirme) | A | `tansu-yeni-is` |
| bug fix (Hata düzeltme) | B | `tansu-hata` |
| rule, document, instruction | C | `tansu-belge` |
| plan or decision | D | `tansu-karar` |
| eval | J | `tansu-eval` |

Each skill lives in `.claude/skills/<name>/SKILL.md` and owns the steps of its flow. Source (E), question (H), and session (I) are short. They stay here.

**E. Source**
1. **Intake:** Levent shares a link or a document: `link-isleme` (PDF: `anthropic-skills:pdf`). Then the `beyin` skill.
2. **Limit:** For outside research, set the limit first: `thinking-bounded-rationality`.
3. **Research:** `mattpocock-skills:research`.
4. **Report:** For a report with many sources: `anthropic-skills:deep-research`.

**H. Question**
1. **Status:** Give the status from the brain notes that `tansu-yeni-is` "Close" wrote. Use `i-have-adhd:i-have-adhd`.
2. **Understanding:** `mattpocock-skills:wait-what` or `mattpocock-skills:teach`.
3. **Picture:** `diagram-design`.

**I. Session**
1. **Long work:** `chief-of-staff`.
2. **Close of a session:** `verification-before-completion`, then `tansu-yeni-is` "Close". A read-only analysis job runs only `verification-before-completion`.
3. **Weekly:** `mattpocock-skills:retro` over the last 10 work sessions, with reader agents on session digests.
4. **Handoff:** To give the work to a new session: `mattpocock-skills:handoff`.
5. **Eval work:** Run flow J (`tansu-eval`).
6. **Monthly:** `ponytail:ponytail-audit` (excess) and `ponytail:ponytail-debt` (deferred shortcuts).
7. **Token use:** `anthropic-skills:explain-usage`. Repeated task: `anthropic-skills:schedule`. Daily brief: `anthropic-skills:morning`.
8. **Not understood:** Levent says "anlamadım": `mattpocock-skills:wait-what`. Then explain again with GLOSSARY terms and plain words.

**Who names skills.** Only five places name skills. They are this file, `DEFINITION_OF_DONE.md`, `docs/agents/`, `.claude/skills/`, and `.claude/agents/`. In this file, only the sections "Every job", "Work flow", "Scope", "Who writes", and "Auditor and rounds" name them. Other files do not name a skill to run. Any file may refer to a step by skill name plus step title.
**How to refer to a step.** Refer to a step by the skill name and the step title, for example `tansu-yeni-is` "Review". Never refer to a step by its number.

## Scope
- Task: the "Per task" item of DEFINITION_OF_DONE.md "How to Apply". The agent gives its own proof. No auditor. The rule "Önce test" applies to every code change, also to a one-line change.
- Feature: several jobs, a behavior, or an interface. Add the "Per feature" item of DEFINITION_OF_DONE.md "How to Apply" to the task items. Run one independent check (`tansu-yeni-is` "Review").
- Outgoing work (push, pull request, delete, archive): the full checklist. Use an independent check (`tansu-yeni-is` "Review").
- Work without code (`.scratch` notes): skip the code items. No auditor.
- Locked files: `AGENTS.md`, the skill files under `.claude/skills/`, `CODING_STANDARDS.md`, and `DEFINITION_OF_DONE.md`. They have feature scope at any size, except as "Who writes" says.

## Who writes
- One file, under 20 lines, no code: the orchestrator writes it itself.
- A locked file, at any size: a subagent writes it. One `mattpocock-skills:code-review` pass by a Sonnet subagent checks the diff (`tansu-yeni-is` "Review"). Exception (Levent 14.10): Levent approves the change in chat.
  - One added line has task scope. The orchestrator writes it and searches the other files for a second copy of the rule. No auditor.
  - A change of 2 to 3 lines gets the `mattpocock-skills:code-review` pass.
  - A change of more than 3 lines needs a writer subagent and the `mattpocock-skills:code-review` pass.
- Code: a subagent writes it. The Codex audit checks it (`tansu-yeni-is` "Review").

## Auditor and rounds
- In this section, "auditor" means the Codex auditor (code) or the reviewer of the `mattpocock-skills:code-review` pass (documents only). `tansu-yeni-is` "Review" says which one runs. The Codex audit is only for code changes.
- The auditor is a different agent from the writer.
- The auditor also checks that the writer followed the steps of the flow skill. The flow skills are `tansu-yeni-is` and the other skills under `.claude/skills/`. The auditor reads the `Akış:` line of the PR body. It checks the diff and the PR body against the steps of that skill. It names each step that has no trace. It compares the PR line `Çağrılan beceriler:` with the steps of the skill. The session that started the job compares the list with the session transcript.
- The auditor of a delete or archive job checks the final file list and the links. It also checks the changes outside the scope.
- The verdicts are GEÇTİ, NOTLU GEÇTİ, and KALDI. NOTLU GEÇTİ: low-risk test gaps and style notes. KALDI: a false claim, a broken behavior, a missed instruction, or a security or privacy risk. An audit without a verdict counts as KALDI. The prompt of a `mattpocock-skills:code-review` pass asks for a verdict in the same words.
- A claim that is false against the source is KALDI at any risk level. The auditor does not grade it low. A doubt in the verdict text (for example "KALDI olabilir") makes the verdict KALDI. The auditor writes `Yanlış iddia sayısı: N` for its pass. A pass with N greater than 0 is KALDI. The PR body copies the N of the pass whose verdict it copies.
- A fix commit that adds or changes claim text gets one more pass, also after NOTLU GEÇTİ. The pass reads only the changed lines. When the auditor names an error class, the orchestrator searches the whole diff for that pattern before the second pass.
- Every audit prompt and every code-review pass prompt states the goal of the job. When the goal is to simplify, a deliberately deleted line is not a finding. A deletion is a finding only if a needed rule was lost without a reason. The rest of the diff gets the full review.
- Code change at feature and outgoing scope: at most 3 Codex audit rounds. Every audit prompt names the round number. The auditor gives the round number with the verdict.
- If round 3 returns KALDI (failed): stop the job. Do not open a fourth round. Find the root cause and define the job again. Send Levent the root cause in one line.
- A documents-only change gets one `mattpocock-skills:code-review` pass. If it returns KALDI, fix the findings and run one more pass. If that pass returns KALDI, stop and send Levent the root cause in one line.
- Add the items that an auditor finds to the source report. A report is complete only after a re-audit passes.
- If the Codex sandbox fails with `CreateProcessWithLogonW 1909`, a small round may go to a Sonnet subagent.

## Working rules (Çalışma kuralları)
- Environment: Windows, PowerShell. Python is `.venv\Scripts\python.exe`. The main branch is `master`. The remote repository is `kaynak` (GitHub, private). There is no other backup.
- Setup: `py -3.14 -m venv .venv`, then `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt -e ".[dev]"`.
- **Names (Adlar):** Code, file, column, and CSV header names are Turkish ASCII (`aile`, `adim`, `evren`). Report and card
  text uses Turkish characters. Use `pathlib` for paths. Open each file with an explicit `encoding="utf-8"` (for CSV,
  `utf-8-sig`).
- **Line ends (Satır sonları):** `core.autocrlf=true`. The working copy is CRLF, the repository is LF. Do not convert line ends. Change files with `Edit`.
- **Shell reads (Kabuk okumaları):** Read a file with `Read`. `permissions.deny` in `.claude/settings.json` blocks `cat`, `sed -n`, and `sed -i` in Bash.
- **Test gate (Test kapısı):** Before a commit, `tansu-yeni-is` "Test gate" must be green. The tests do not
  access the network and do not write to the real `kayit/` files (`tests/conftest.py` changes the path to `tmp_path`).
- **Test first (Önce test):** Write a red test first. Then write the minimum code. Write tests only against the interfaces (yüzler) in TASARIM.
- **Do not loosen a test (Testi gevşetme yasak):** Do not delete an assert. Do not increase a tolerance. Do not add `skip`/`xfail`.
  Do not change an expected value to match the code.
  - If a test is wrong, first write the reason in the document.
  - Calculate the expected values by hand. Do not calculate them again the way the code does.
  - Write the constants in a test as literals.
- **Do not look at the return (Getiriye bakma):** See `docs/KURALLAR.md` §4.
- **Git (this repository only):** Do not use `rebase`, `--amend`, `--force` (and `--force-with-lease`), `reset --hard`, `clean -f`, `branch -D`,
  `checkout .`, `restore .`, `git add .`, or `git add -A` (for Claude, a permission deny blocks them: `permissions.deny` global and `.claude/settings.json`). Add files
  by name. Which folders git tracks and the log rules are in TASARIM §5.11. Do not delete `veri/`. In a commit, leave the `kayit/` files only added, not <!-- driftlint-ignore: veri/ is gitignored local data, absent in CI -->
  modified. This rule covers this repository only.
- **Task Scheduler (Görev Zamanlayıcı):** No task is installed on this machine (Levent 16.10: the project is still in design).
  Two task definitions stay in the repository:
  `TansuGunluk` (`kurulum/tansu-gunluk.xml`, `python -m tansu gunluk`) and `TansuAylik` (`kurulum/tansu-aylik.xml`, `python -m tansu evren-indir`).
  The times are in TASARIM §6. Install a task only after Levent approves it (DEFINITION_OF_DONE.md `## Tansu`). The paths point to the main repository on this machine (`C:\Users\levent\Desktop\TANSU`).
  To install a definition again, use PowerShell (`schtasks /create /xml` cannot read UTF-8 XML):
  `Register-ScheduledTask -TaskName TansuGunluk -Xml (Get-Content -Raw -Encoding utf8 kurulum\tansu-gunluk.xml)`. The definition comes
  disabled (`<Enabled>false</Enabled>`); enable it with `schtasks /change /tn TansuGunluk /enable`. To delete a task: `schtasks /delete /tn TansuGunluk /f`.
- **Rule parameter (Kural parametresi):** A rule parameter changes only with a TASARIM/KURALLAR change and as a new trial (deneme).
- **Dependency (Bağımlılık):** Before you add a new package, check TASARIM §4 and the stdlib. Write an added package in `pyproject.toml`
  with `==`. A CI tool outside Python is pinned to an exact version in the workflow file.

## Standards (Standartlar)
`CODING_STANDARDS.md` and `DEFINITION_OF_DONE.md` are the standards of Tansu. `DEFINITION_OF_DONE.md` is Tansu's own copy. No shared original exists since 15.10 (Levent 15.10).
`CODING_STANDARDS.md` is different since 17.10 (Levent 17.10): it points to the shared general file and holds only the Tansu items. The `## Tansu` section at the end of each file holds the Tansu-only items. `tansu-yeni-is` "Review" reads both files and the general file.

## Agent skills

### Issue tracker

See `docs/agents/issue-tracker.md`.

### Triage labels

See `docs/agents/triage-labels.md`.

### Domain docs

See `docs/agents/domain.md`.
