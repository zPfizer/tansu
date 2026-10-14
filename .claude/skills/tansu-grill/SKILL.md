---
name: tansu-grill
description: An interview that questions an idea or a design in Tansu. It runs the `mattpocock-skills:grilling` and `mattpocock-skills:domain-modeling` skills with the criteria of Tansu. Use it when a discussion in Tansu is about a new rule, parameter, data source, or behavior change.
---

Call the Skill tool two times: `mattpocock-skills:grilling` and `mattpocock-skills:domain-modeling`. During the interview, also apply the three criteria below.
The text of the rules is in their owner files. This skill only tells when to check them.

## 1. Tansu comes first

Before you propose a rule, a value, or a behavior, apply KURALLAR "Okuma kuralları". Search the Tansu pool and the rule
files for his view on that subject, and show the result in the proposal.

## 2. Risk scan

For each decision, ask these questions against AGENTS.md "Çalışma kuralları" and TASARIM. Write the answer:
- Does the decision obey the terms of use of the data source? (TASARIM §4)
- Does the decision keep the trial log (deneme günlüğü) rule and the `veri/` rule?
- After the rule record (kural kaydı), does a changed rule count as a new trial (deneme)? (TASARIM §5.8)
- Is there a look-ahead (geleceği görme) risk? (TASARIM §5.12)
- Does the money decision stay with Levent? (TASARIM §5.12)

## 3. Show the text that will change

At each decision point, show the TASARIM, KURALLAR, or GLOSSARY text that will change, before and after the change. If
code will change, show a short form of the current and the proposed function.

Ask Levent only the direction decision that the source and the decision records do not answer.
