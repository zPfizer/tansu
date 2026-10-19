# TANSU

TANSU is a daily signal and backtest (sınama) system for BIST. Follow the documents.
If they conflict with code or omit a case, stop. Fix the document first. Write the reason before the code.

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
| `AGENTS.md` | the entry, the environment, the current state, "Every job", and the work flow table |
| `docs/agents/` | job rules, shared delivery, git, short flows E, H, I, and skill naming (`is-kurallari.md`). Task Scheduler (`zamanlayici.md`). Issues and triage labels (`issue-tracker.md`). driftlint does not scan this folder. `tests/test_sahipler.py` checks its paths |
| `.claude/skills/` | the work flow procedures, one skill per job type |
| `docs/strateji-taslak/`, `docs/strateji-modulleri-taslak.md` (local, not in git) | proposals that wait for approval. They own no fact. They are outside the drift check. These local files need not exist <!-- driftlint-ignore: local-only, gitignored, absent in CI --> |
| `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md` | the Tansu code rules (`## Tansu`; the general rules are in the file that `CODING_STANDARDS.md` points to) and the done criteria (`## Tansu`) |
| `docs/sorgu/sonuc-3-4.md`, `docs/sorgu/izleme/karar.md` (local, not in git) | the reasons for the decisions (read them when necessary and when they exist) <!-- driftlint-ignore: local-only, gitignored, absent in CI --> |

The drift check covers all these files. The drift check is your review, not only driftlint (see the `docs/agents/` row). Correct a file when it contradicts another file, contains old information,
or copies a fact of another file.

## Domain documentation

### Before exploring, read these

- `GLOSSARY.md` at the repo root: the meaning of every term (single context, no `GLOSSARY-MAP.md`). <!-- driftlint-ignore: intentionally absent glossary map, not a file reference -->
- `docs/TASARIM.md`: the decision record. Tansu has no ADR folder and no ADR files.
- `docs/sorgu/`: the reasons behind the decisions (local, not in git). <!-- driftlint-ignore: local-only decision notes, absent in CI -->

Do not create an ADR folder. `tansu-yeni-is` "Document first" owns where settled terms and decisions go.

### Use the glossary's vocabulary

When your output names a domain concept (an issue title, a refactor proposal, a hypothesis, a test name), use the
term as `GLOSSARY.md` defines it. Do not drift to synonyms the glossary avoids. A missing term is a signal: you
invent language the project does not use, or there is a real gap. Record the gap for `tansu-yeni-is` "Document first".

### Flag decision conflicts

If your output contradicts a decision in `docs/TASARIM.md`, say so explicitly instead of overriding it:

> _Contradicts TASARIM §5.1 (empty value stays empty), but worth reopening because…_

## Environment (Ortam)
- Windows, PowerShell. Python is `.venv\Scripts\python.exe`. The main branch is `master`. The remote repository is `origin` (GitHub `zPfizer/tansu`, public). There is no other backup.
- **Current rules (Güncel kurallar):** The current rules are on `origin/master`. Before a job, run `git fetch origin`. Read the rules from `origin/master`. A checkout that is behind `origin/master` gives old rules.
- Setup: `py -3.14 -m venv .venv`, then `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt -e ".[dev]"`.
- **Names (Adlar):** Code, file, column, and CSV header names are Turkish ASCII (`aile`, `adim`, `evren`). Report and card
  text uses Turkish characters. Use `pathlib` for paths. Open each file with an explicit `encoding="utf-8"` (for CSV,
  `utf-8-sig`).
- **Line ends (Satır sonları):** `core.autocrlf=true`. The working copy is CRLF, the repository is LF. Do not convert line ends. Change files with `Edit`.
- **Shell reads (Kabuk okumaları):** Read a file with `Read`. `permissions.deny` in `.claude/settings.json` blocks `cat`, `sed -n`, and `sed -i` in Bash.
- **Hooks (Kancalar):** `.claude/settings.json` registers `kurulum/kanca.py`. It checks only that a test under `tests/` changes before code.
- **Waiting (Bekleme):** Claude Code blocks `sleep` and `Start-Sleep`. Run long commands alone. Run only affected pytest tests and `ruff check`/`ruff format --check` on changed files. CI runs the full suite.
  Use the foreground with a timeout of at most 600000 ms, or `run_in_background` with one Monitor. Do not poll. Git Bash `pgrep` cannot see PowerShell processes.
- **Temporary files (Geçici dosyalar):** Write them under `$TEMP` or under `.scratch/<job>/tmp/` of the main checkout. Never write one to a tracked path.
  The permission system refuses a recursive delete (`rm -rf`, `Remove-Item -Recurse`). Do not try it. List the leftover paths in a code block of the report. Levent deletes them.
- **Shell state (Kabuk durumu):** Each shell call starts new. A `cd`, a variable, or an `export` does not carry over. `$CLAUDE_PROJECT_DIR` exists only in hooks. Use full paths.
- **Copied values (Kopya değerler):** Copy an id, a path, a sha, or a number from a command output of this session. Do not write it from memory or from the report of another agent.
  Search a Markdown heading with `^#+ <text>`, because its level can differ.
- **Dependency (Bağımlılık):** Before you add a new package, check TASARIM §4 and the stdlib. Write an added package in `pyproject.toml`
  with `==`. A CI tool outside Python is pinned to an exact version in the workflow file.

## Every job
1. Write the intent of Levent and the flow letter in one line at the top of the first reply only. After that line, the result comes first. All text that Levent can see is Turkish, also the wrap_up text.
2. Unknown error or missing fact: run `py -3 C:\Users\levent\Desktop\YONETIM\beyin\beyin.py context "<q>" --harness claude --project TANSU --no-sync` before you search logs, code, or the web. <!-- driftlint-ignore: local-only path of the brain tool, absent in CI -->
3. If the work type is unclear, compare the request with the work flow table. Before you write an instruction or prompt: `asd-ste100`.
4. The main session resolves technical questions from sources. It may use `vekil` for recorded decisions and recommendations. It may use `okuyucu` for broad source searches. Both helpers are optional. Levent gets money, scope, direction, taste, and product decisions absent from Tansu notes. Also ask him about secrets, any deletion, outgoing work, Task Scheduler changes, and work that cannot be undone.
5. If a claim has no source: `thinking-circle-of-competence`. If the problem type is unclear: `thinking-cynefin`. If the method is unclear: `thinking-model-router`.
6. Choose the flow and the scope (`docs/agents/is-kurallari.md` "Scope").

## Work flow (İş akışı)
The `mattpocock-skills` package is optional. Follow the written steps without it. Other skill requirements still apply. Source: Levent, 19.10.2026.

Choose the flow by the work type. Call each skill by the exact name in backticks. Open the skill of the flow before the first step. Run the steps in order. Run an "If" row only when its condition is true.

| Work type | Flow | Skill |
|---|---|---|
| new work (Yeni geliştirme) | A | `tansu-yeni-is` |
| bug fix (Hata düzeltme) | B | `tansu-hata` |
| rule, document, instruction | C | `tansu-belge` |
| plan or decision | D | `tansu-karar` |
| eval | J | `tansu-eval` |

Each skill lives in `.claude/skills/<name>/SKILL.md` and owns the steps of its flow. Source (E), question (H), and session (I) are in [Short flows and skill naming](docs/agents/is-kurallari.md#short-flows-and-skill-naming).

## Read before you act (Okuma işaretçileri)
- Before you choose a scope, write a locked file, or start an audit: `docs/agents/is-kurallari.md`.
- Before you write or change code, a test, or a rule parameter: `CODING_STANDARDS.md` "Code and test rules".
- Before you commit or run a git command that changes the repository: `docs/agents/is-kurallari.md` "Git".
- Before you touch a Task Scheduler task or a file in `kurulum/`: `docs/agents/zamanlayici.md`.
- Before a source, question, or session job: read `docs/agents/is-kurallari.md` "Short flows and skill naming". Also read it before naming a skill or a document step.
- Issue tracker and triage labels: `docs/agents/issue-tracker.md`. Domain reading rules are in "Domain documentation" above.

## Standards (Standartlar)
`CODING_STANDARDS.md` points to the shared general rules. Its `## Tansu` section and that of `DEFINITION_OF_DONE.md` hold the project rules.
Review reads both files and the shared general rules.
