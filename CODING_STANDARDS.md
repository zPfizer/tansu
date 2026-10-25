# Coding standards

Read `C:\Users\levent\Desktop\YONETIM\beyin\knowledge\concepts\kod-standartlari-genel.md` first. It owns the general rules. This file adds the Tansu rules.

## Tansu
`docs/TASARIM.md` owns behavior. Apply the relevant source and calculation rules below.

### Calculations
- **No look-ahead (Geleceği görmeme):** Add each new or changed calculation to the scope of `tests/test_gelecek.py`
  (TASARIM §5.12).
- **One code (Tek kod):** Do not write a second copy of a function that TASARIM §4 (`motor`) shares between the
  backtest (sınama) and the live run.
- **No silent correction (Sessiz düzeltme yok):** Do not fill, clip, or skip silently. An unexpected condition gives an
  error. The behavior for a missing value is in TASARIM §5.1.
- **Follow the document (Belgeye bağlılık):** Each new or changed behavior has a `TASARIM <bölüm>` reference in the code.
- **Invariant rule (Değişmez kural):** TASARIM has statements that say a thing never happens or always happens
  (examples: "anlık görüntü değişmez", "ileri doldurulmaz", "indirme durur"). For each such statement, the code has one
  enforcer and one test. A new statement comes with both.
- **Define the boundary before the code (Sınırı önce tanımla):** Define each new calculation's boundaries in TASARIM.
  Cover the period's first and last day, quarantined days, and zero, infinite, or missing prices.
  Commit order: document, then red test, then code.
- **Do not look at the return (Getiriye bakma):** Apply `docs/aile-kurallari.md` §4 to fidelity checks and YORUM selection.
- **Rule parameter (Kural parametresi):** A rule parameter changes only with a TASARIM/KURALLAR change and as a new trial (deneme).

### Source proof

- **Tansu comes first (Tansu önce gelir):** Before you write a rule, a value, or a definition, check the Tansu pool for his
  view on that subject. If Tansu has an idea, do not write a YORUM. If you cannot follow the idea, write
  "uygulanamaz" and the reason (`docs/aile-kurallari.md` "Okuma kuralları").
- **Give a reference, do not copy (Atıf ver, kopyalama):** Apply AGENTS.md "Belgeler ve sahipleri".
- **Do not write a missing thing as if it exists (Olmayanı var gibi yazma):** Apply `tansu-yeni-is` "Document first" for approved contracts, proposals, and implementation status.
- **Open the source before a new fact (Kaynağı aç):** Open the Ham line or image before writing a new fact sentence in a document. If you cannot find it, write "okunamıyor" or YORUM.
- **Read the whole note:** Read each source note in full with the active file tools. Do not truncate its body. Report the line count. The main agent checks the count with an available file tool or UTF-8 command.

## Code and test rules

- **Test gate (Test kapısı):** Use [Check and evidence](docs/agents/is-kurallari.md#check-and-evidence) for commands and evidence. Required checks pass before a commit.
  Tests do not access the network or write to real `kayit/` files. `tests/conftest.py` changes the path to `tmp_path`.
- **Test first (Önce test):** Before code edits, classify the change by its observable effects. A filename or the word "refactor" does not establish the change type. Write tests only against the interfaces (yüzler) in TASARIM.
  - For new behavior or a defect correction, first run a test that fails on an assert of the intended behavior. Then write the minimum code. Run the test again and check that it passes.
  - `ModuleNotFoundError`, `ImportError`, `FileNotFoundError`, or a missing fixture is not a red. The writer pastes the actual red and green outputs in the report.
  - For a pure refactor, preserve observable behavior. Run the affected tests before code edits and check that they pass. After edits, run the same inputs, assertions, and expected results with matching dependencies, environment, and data. Check that they still pass. Record both actual outputs.
  - Reuse adequate existing tests for a pure refactor. That change requires no new failing test or test edit. If coverage is missing, add characterization tests for approved existing behavior before code edits. Record their passing baseline.
  - Changes to interfaces, outputs, errors, or side effects require the behavior-change evidence above. Apply that evidence to mixed changes and to changes whose behavior equivalence is uncertain.
  - A pure refactor still requires the applicable real-data, no-look-ahead, and invariant checks.
- **Do not loosen a test (Testi gevşetme yasak):** Do not delete an assert. Do not increase a tolerance. Do not add `skip`/`xfail`.
  Do not change an expected value to match the code.
  - If a test is wrong, first write the reason in the document.
  - Calculate the expected values by hand. Do not calculate them again the way the code does.
  - Write the constants in a test as literals.
- **Baseline (Taban):** Never call a failing test "expected" or "not from this job" before you run the same test on `origin/main` in this session. Paste both outputs.
- **Edit loop (Düzenleme döngüsü):** Format Python files before the final review because formatting can rewrite them.
  Between edits, run only the changed module's tests. Final checks and evidence reuse follow [Check and evidence](docs/agents/is-kurallari.md#check-and-evidence).
