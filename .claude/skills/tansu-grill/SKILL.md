---
name: tansu-grill
description: An interview that questions an idea or a design against Tansu sources and decisions. Use it when a discussion in Tansu is about a new rule, parameter, data source, or behavior change.
---

Scope: the main checkout. The `yeniden-kurulus` worktree has no `docs/agents/`. There, follow its `AGENTS.md`.

Question the assumptions, alternatives, risks, and acceptance criteria of the proposal. Check the terms in GLOSSARY and the decisions in TASARIM.
Apply the three criteria below. Record settled terms and decisions as `tansu-yeni-is` "Document first" says.
The text of the rules is in their owner files. This skill only tells when to check them.

## 1. Tansu comes first

Before you propose a rule, a value, or a behavior, apply `docs/aile-kurallari.md` "Okuma kuralları". Search the Tansu pool and the rule
files for his view on that subject, and show the result in the proposal.

## 2. Risk scan

For each decision, ask these questions against AGENTS.md "Environment", `CODING_STANDARDS.md`, `docs/agents/is-kurallari.md` "Git", and TASARIM. Write the answer:
- Does the decision obey the terms of use of the data source? (TASARIM §4)
- Does the decision keep the trial log (deneme günlüğü) rule and the `veri/` rule? <!-- driftlint-ignore: veri/ is gitignored local data, absent in CI -->
- After the rule record (kural kaydı), does a changed rule count as a new trial (deneme)? (TASARIM §5.8)
- Is there a look-ahead (geleceği görme) risk? (TASARIM §5.12)
- Does the money decision stay with Levent? (TASARIM §5.12)

## 3. Show the text that will change

At each decision point, show the TASARIM, KURALLAR, or GLOSSARY text that will change, before and after the change. If
code will change, show a short form of the current and the proposed function.

Ask Levent only the direction decision that the source and the decision records do not answer.
