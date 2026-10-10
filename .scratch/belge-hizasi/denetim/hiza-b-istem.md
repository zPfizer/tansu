Project folder: C:\Users\levent\Desktop\TANSU. This is a read-only audit. Do not change any file.
First action: read AGENTS.md and print its first line, to prove that you can read files.

Goal: the Markdown files of this project must agree with each other. Find every place where they do not agree.

Background facts:
- AGENTS.md says: "Kod belgelere uyar; belge değişmeden davranış değişmez." The decided design is docs/TASARIM.md.
- CODING_STANDARDS.md and DEFINITION_OF_DONE.md are exact copies of the owner's global standard. A test keeps them identical. Do not report them as "not Tansu-specific". Report only a real conflict between them and another file.
- AGENTS.md has a section "Tansu'ya özel standartlar" that adds Tansu rules to the global standard.
- Every fact must have one owner file. Another file may refer to it, but must not restate it differently.

Report these finding types:
1. ÇELİŞKİ: two files say different things about the same rule, number, name, path or step.
2. ESKİ: a file states something that is no longer true (an old draft, an old path, a closed ticket described as open, a file that does not exist).
3. TEKRAR: the same fact is written in full in two files, so the two copies can drift. Name the file that should own it.
4. TERİM: a term is used with a different meaning than in GLOSSARY.md, or an important term is missing from GLOSSARY.md.
5. KIRIK ATIF: a reference to a section, file, ticket or label that does not exist.

Rules:
- Open every file in your scope from the first line to the last line. Do not sample.
- Every finding needs both places as file:line, and you must have opened both lines yourself.
- Do not invent findings. If you are not sure, write "kısmi" and say why.
- Write each finding in one or two short, plain Turkish sentences.
- For each finding, propose one fix: which file is the owner and what changes.

Output format (Markdown):
## Ne okudum
(list of files and their line counts)
## Bulgular
| # | Tür | Yer 1 | Yer 2 | Ne | Önerilen düzeltme |
## Boşluklar
(what you could not check, and why)

Your scope:
- docs/TASARIM.md, GLOSSARY.md, docs/KURALLAR.md. Compare them with each other: rules, parameters, numbers, names, section references, terms.
