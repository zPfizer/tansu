---
name: tansu-hata
description: "Use when something is broken in Tansu: a bug, an error, a failing test, a crash, a wrong number in a report or signal, or a regression. It runs flow B (Hata düzeltme) in order: Diagnose, Red test, Fix, Test gate, Review, Proof, Pull request, merge, close, and Lesson. It reuses the shared steps of `tansu-yeni-is`."
---

# Bug fix (Hata düzeltme), flow B

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks.
The shared steps are in [ortak-adimlar.md](../tansu-yeni-is/ortak-adimlar.md). Read that file for the steps that point to `tansu-yeni-is`.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Diagnose:** `mattpocock-skills:diagnosing-bugs`.
2. **Red test:** `mattpocock-skills:tdd`.
3. **Fix:** A subagent writes the minimum code on an issue branch for a large job, then uses a PR (`tansu-yeni-is` "Branch", Levent 17.10). A small change that Levent requests in chat goes directly to master with a green CI run, without an issue or PR.
4. **Test gate:** As `tansu-yeni-is` "Test gate".
5. **Review:** As `tansu-yeni-is` "Review".
6. **Proof:** As `tansu-yeni-is` "Proof".
7. **Pull request, merge, and close:** As `tansu-yeni-is` "Pull request", `tansu-yeni-is` "Merge", and `tansu-yeni-is` "Close".
8. **Lesson:** `mattpocock-skills:retro`. Record the mistake as the "Mistakes" section of the general standards file says. `CODING_STANDARDS.md` points to that file.

| If | Then |
|---|---|
| a document and the real state disagree | `thinking-map-territory`. |
| the fault repeats | `thinking-five-whys-plus`. |
| there are several possible causes | `thinking-scientific-method`. |
| a defect is selective | `thinking-kepner-tregoe`. |
| the problem is slowness | `thinking-theory-of-constraints`. |
| a fix breaks another part | `thinking-systems`. |
| the problem changes while you work | `thinking-ooda`. |
