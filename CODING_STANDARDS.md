# Coding standards

Read `C:\Users\levent\Desktop\YONETIM\beyin\knowledge\concepts\kod-standartlari-genel.md` first. It owns the general rules. This file adds the Tansu rules.

## Tansu
`docs/TASARIM.md` owns behavior. Apply these rules when you write code.
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
- **Tansu comes first (Tansu önce gelir):** Before you write a rule, a value, or a definition, check the Tansu pool for his
  view on that subject. If Tansu has an idea, do not write a YORUM. If you cannot follow the idea, write
  "uygulanamaz" and the reason (KURALLAR "Okuma kuralları").
- **Give a reference, do not copy (Atıf ver, kopyalama):** Apply AGENTS.md "Belgeler ve sahipleri".
- **Do not write a missing thing as if it exists (Olmayanı var gibi yazma):** The documents describe only what exists
  today. Planned work stays in the spec and the ticket. When the work is in place, it goes into the document.
- **Open the source before a new fact (Kaynağı aç):** Open the Ham line or image before writing a new fact sentence in a document. If you cannot find it, write "okunamıyor" or YORUM.
- **Read the whole note:** A reader reads each note with `Read`, without `offset` or `limit`. It never cuts a note with `head`, `cut`, `sed -n`, or a slice. It reports the line count, and the main agent checks the count with `wc -l`.
- **Define the boundary before the code (Sınırı önce tanımla):** Define each new calculation's boundaries in TASARIM. Cover the period's first and last day, quarantined days, and zero, infinite or missing prices. Commit order: document, then red test, then code.

## Code and test rules

- **Test gate (Test kapısı):** Before a commit, `tansu-yeni-is` "Check and evidence" (the tests of the change and ruff) must be green. The tests do not
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
