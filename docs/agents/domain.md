# Domain Docs

How the engineering skills consume the domain documentation of this repo.

## Before exploring, read these

- `GLOSSARY.md` at the repo root: the meaning of every term (single context, no `GLOSSARY-MAP.md`).
- `docs/TASARIM.md`: the decision record. Tansu has no ADR folder and no ADR files.
- `docs/sorgu/`: the reasons behind the decisions (local, not in git).

Do not create an ADR folder. Where a settled term and a decision go (also when `mattpocock-skills:domain-modeling`
writes them): AKIS A "Document first" (in `AKIS.md`).

## Use the glossary's vocabulary

When your output names a domain concept (an issue title, a refactor proposal, a hypothesis, a test name), use the
term as `GLOSSARY.md` defines it. Do not drift to synonyms the glossary avoids. A missing term is a signal: you
invent language the project does not use, or there is a real gap. Note it for `mattpocock-skills:domain-modeling`.

## Flag decision conflicts

If your output contradicts a decision in `docs/TASARIM.md`, say so explicitly instead of overriding it:

> _Contradicts TASARIM §5.1 (empty value stays empty), but worth reopening because…_
