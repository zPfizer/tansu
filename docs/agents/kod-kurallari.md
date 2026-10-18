# Code and test rules (Kod ve test kuralları)

- **Test gate (Test kapısı):** Before a commit, `tansu-yeni-is` "Test gate" (the tests of the change and ruff) must be green. The tests do not
  access the network and do not write to the real `kayit/` files (`tests/conftest.py` changes the path to `tmp_path`).
- **Test first (Önce test):** Write a red test first. Then write the minimum code. Write tests only against the interfaces (yüzler) in TASARIM.
  - The red run fails on an assert of the new behavior. `ModuleNotFoundError`, `ImportError`, `FileNotFoundError`, or a missing fixture is not a red. The writer pastes the red output in the report.
- **Do not loosen a test (Testi gevşetme yasak):** Do not delete an assert. Do not increase a tolerance. Do not add `skip`/`xfail`.
  Do not change an expected value to match the code.
  - If a test is wrong, first write the reason in the document.
  - Calculate the expected values by hand. Do not calculate them again the way the code does.
  - Write the constants in a test as literals.
- **Baseline (Taban):** Never call a failing test "expected" or "not from this job" before you run the same test on `origin/master` in this session. Paste both outputs.
- **Edit loop (Düzenleme döngüsü):** Run `ruff format` before you Read a file that you will edit, because ruff rewrites the file. Between edits, run only the tests of the changed module. Run the tests of the change and ruff once before each commit.
- **Do not look at the return (Getiriye bakma):** See `docs/KURALLAR.md` §4.
- **Rule parameter (Kural parametresi):** A rule parameter changes only with a TASARIM/KURALLAR change and as a new trial (deneme).
