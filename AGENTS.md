# TANSU

TANSU is a daily signal and backtest (sınama) system for BIST. Tansu inspired it. The code follows the documents.
The behavior does not change before a document changes.

## Current state (Şimdiki durum)
This section holds temporary states only. Each line has a date and an owner. Delete a line when its end condition is true.

**Geliştirme durdu (development stopped):** Do not do new development that changes the behavior of Tansu
until the documents have no drift, no old information, and no contradiction. The tickets of `.scratch/belge-hizasi/` and the work-setup jobs
(`.scratch/yazilim-fabrikasi/`) continue (Levent 10.10). When ticket 08 is complete, delete this line.

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
| `AGENTS.md` | the entry, the working rules, and the current state |
| `AKIS.md` | the work flows, the skill placement, the scope, and the auditor rules |
| `docs/strateji-taslak/`, `docs/strateji-modulleri-taslak.md` (local, not in git) | proposals that wait for approval. They own no fact. They are outside the drift check |
| `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md` | the code format and the done criteria (`## Tansu`) |
| `docs/sorgu/sonuc-3-4.md`, `docs/sorgu/izleme/karar.md` (local, not in git) | the reasons for the decisions (read them when necessary) |

The drift check covers all these files. Correct a file when it contradicts another file, contains old information,
or copies a fact of another file.

If a document and the code contradict, or if the document says nothing about the case, stop. Correct the document
first. Write the reason. Then write the code.

## Work flow (İş akışı)
Before each job, read `AKIS.md`. Follow its flow: A for new work, B for a bug fix.
Refer to an AKIS step by its title, not by its number.

## Working rules (Çalışma kuralları)
- Environment: Windows, PowerShell. Python is `.venv\Scripts\python.exe`. The main branch is `master`. The remote repository is `kaynak` (GitHub, private). There is no other backup.
- Setup: `py -3.14 -m venv .venv`, then `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt -e ".[dev]"`.
- **Names (Adlar):** Code, file, column, and CSV header names are Turkish ASCII (`aile`, `adim`, `evren`). Report and card
  text uses Turkish characters. Use `pathlib` for paths. Open each file with an explicit `encoding="utf-8"` (for CSV,
  `utf-8-sig`).
- **Test gate (Test kapısı):** Before a commit, `.venv\Scripts\python.exe -m pytest -q` must be green. The tests do not
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
  by name. Which folders git tracks and the log rules are in TASARIM §5.11. Do not delete `veri/`. In a commit, leave the `kayit/` files only added, not
  modified. This rule covers this repository only.
- **Task Scheduler (Görev Zamanlayıcı):** Two tasks are installed and enabled on this machine:
  `TansuGunluk` (`kurulum/tansu-gunluk.xml`, `python -m tansu gunluk`) and `TansuAylik` (`kurulum/tansu-aylik.xml`, `python -m tansu evren-indir`).
  The times are in TASARIM §6. The paths point to the main repository on this machine (`C:\Users\levent\Desktop\TANSU`).
  To install a definition again, use PowerShell (`schtasks /create /xml` cannot read UTF-8 XML):
  `Register-ScheduledTask -TaskName TansuGunluk -Xml (Get-Content -Raw -Encoding utf8 kurulum\tansu-gunluk.xml)`. The definition comes
  disabled (`<Enabled>false</Enabled>`); enable it with `schtasks /change /tn TansuGunluk /enable`. To delete a task: `schtasks /delete /tn TansuGunluk /f`.
- **Rule parameter (Kural parametresi):** A rule parameter changes only with a TASARIM/KURALLAR change and as a new trial (deneme).
- **Dependency (Bağımlılık):** Before you add a new package, check TASARIM §4 and the stdlib. Write an added package in `pyproject.toml`
  with `==`.

## Standards (Standartlar)
`CODING_STANDARDS.md` and `DEFINITION_OF_DONE.md` are the standards of Tansu. Tansu keeps its own copy. No shared original exists since 15.10 (Levent 15.10).
The `## Tansu` section at the end of each file holds the Tansu-only items. AKIS A "Review" reads both files.

## Agent skills

### Issue tracker

See `docs/agents/issue-tracker.md`.

### Triage labels

See `docs/agents/triage-labels.md`.

### Domain docs

See `docs/agents/domain.md`.
