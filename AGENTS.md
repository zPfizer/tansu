# TANSU

TANSU is a daily signal and backtest (sınama) system for BIST. The code follows the documents.
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
| `AGENTS.md` | the entry, the environment, the current state, "Every job", and the work flow table |
| `docs/agents/` | the job rules: Scope, Who writes, Auditor and rounds (`is-kurallari.md`); the code and test rules (`kod-kurallari.md`); git (`git.md`); Task Scheduler (`zamanlayici.md`); the short flows E, H, I and the skill naming rules (`akislar.md`); the issue tracker, the triage labels, and the domain docs. driftlint does not scan this folder; `tests/test_sahipler.py` checks its paths |
| `.claude/skills/` | the work flow procedures, one skill per job type |
| `docs/strateji-taslak/`, `docs/strateji-modulleri-taslak.md` (local, not in git) | proposals that wait for approval. They own no fact. They are outside the drift check. These local files need not exist <!-- driftlint-ignore: local-only, gitignored, absent in CI --> |
| `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md` | the Tansu code rules (`## Tansu`; the general rules are in the file that `CODING_STANDARDS.md` points to) and the done criteria (`## Tansu`) |
| `docs/sorgu/sonuc-3-4.md`, `docs/sorgu/izleme/karar.md` (local, not in git) | the reasons for the decisions (read them when necessary and when they exist) <!-- driftlint-ignore: local-only, gitignored, absent in CI --> |

The drift check covers all these files. The drift check is your review, not only driftlint (see the `docs/agents/` row). Correct a file when it contradicts another file, contains old information,
or copies a fact of another file.

If a document and the code contradict, or if the document says nothing about the case, stop. Correct the document
first. Write the reason. Then write the code.

## Environment (Ortam)
- Windows, PowerShell. Python is `.venv\Scripts\python.exe`. The main branch is `master`. The remote repository is `origin` (GitHub `zPfizer/tansu`, private). There is no other backup.
- **Current rules (Güncel kurallar):** The current rules are on `origin/master`. Before a job, run `git fetch origin`. Read the rules from `origin/master`. A checkout that is behind `origin/master` gives old rules.
- Setup: `py -3.14 -m venv .venv`, then `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt -e ".[dev]"`.
- **Names (Adlar):** Code, file, column, and CSV header names are Turkish ASCII (`aile`, `adim`, `evren`). Report and card
  text uses Turkish characters. Use `pathlib` for paths. Open each file with an explicit `encoding="utf-8"` (for CSV,
  `utf-8-sig`).
- **Line ends (Satır sonları):** `core.autocrlf=true`. The working copy is CRLF, the repository is LF. Do not convert line ends. Change files with `Edit`.
- **Shell reads (Kabuk okumaları):** Read a file with `Read`. `permissions.deny` in `.claude/settings.json` blocks `cat`, `sed -n`, and `sed -i` in Bash.
- **Dependency (Bağımlılık):** Before you add a new package, check TASARIM §4 and the stdlib. Write an added package in `pyproject.toml`
  with `==`. A CI tool outside Python is pinned to an exact version in the workflow file.

## Every job
1. Write the intent of Levent and the flow letter in one line at the top of the first reply only. After that line, the result comes first. All text that Levent can see is Turkish, also the wrap_up text.
2. Unknown error or missing fact: run `py -3 C:\Users\levent\Desktop\YONETIM\beyin\beyin.py context "<q>" --harness claude --project TANSU --no-sync` before you search logs, code, or the web. <!-- driftlint-ignore: local-only path of the brain tool, absent in CI -->
3. If the work type is unclear: `mattpocock-skills:ask-matt`.
4. Send a design or technical question that needs the preference of Levent to the `vekil` subagent first. Levent gets only these: direction of the project, money, outgoing work, secrets, and delete. Levent also gets a Task Scheduler change and work that cannot be undone.
5. Before you write an instruction or a prompt: `asd-ste100`.
6. If you cannot show a source for a claim: `thinking-circle-of-competence`.
7. If the problem type is unclear: `thinking-cynefin`. If the method is unclear: `thinking-model-router`.
8. Choose the flow and the scope (`docs/agents/is-kurallari.md` "Scope").

## Work flow (İş akışı)
Choose the flow by the work type. Call each skill by the exact name in backticks. Open the skill of the flow before the first step. Run the steps in order. Run an "If" row only when its condition is true.

| Work type | Flow | Skill |
|---|---|---|
| new work (Yeni geliştirme) | A | `tansu-yeni-is` |
| bug fix (Hata düzeltme) | B | `tansu-hata` |
| rule, document, instruction | C | `tansu-belge` |
| plan or decision | D | `tansu-karar` |
| eval | J | `tansu-eval` |

Each skill lives in `.claude/skills/<name>/SKILL.md` and owns the steps of its flow. Source (E), question (H), and session (I) are short flows: `docs/agents/akislar.md`.

## Read before you act (Okuma işaretçileri)
- Before you choose a scope, write a locked file, or start an audit: `docs/agents/is-kurallari.md`.
- Before you write or change code, a test, or a rule parameter: `docs/agents/kod-kurallari.md`.
- Before you commit or run a git command that changes the repository: `docs/agents/git.md`.
- Before you touch a Task Scheduler task or a file in `kurulum/`: `docs/agents/zamanlayici.md`.
- For a source, question, or session job, and before you name a skill or refer to a step in a document: `docs/agents/akislar.md`.
- Issue tracker (GitHub Issues): `docs/agents/issue-tracker.md`. Triage labels: `docs/agents/triage-labels.md`. Domain docs: `docs/agents/domain.md`.

## Standards (Standartlar)
`CODING_STANDARDS.md` and `DEFINITION_OF_DONE.md` are the standards of Tansu. `DEFINITION_OF_DONE.md` is Tansu's own copy.
`CODING_STANDARDS.md` is different since 17.10 (Levent 17.10): it points to the shared general file and holds only the Tansu items. The `## Tansu` section at the end of each file holds the Tansu-only items. `tansu-yeni-is` "Review" reads both files and the general file.
