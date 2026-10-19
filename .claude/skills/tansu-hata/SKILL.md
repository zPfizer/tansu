---
name: tansu-hata
description: "Use for a Tansu defect, including a bug, error, failing test, crash, wrong report or signal value, or regression. Flow B diagnoses the fault, keeps a red test, fixes it, checks evidence, and delivers the change. It reuses the shared steps of `tansu-yeni-is`."
---

# Bug fix (Hata düzeltme), flow B

Run AGENTS.md "Every job" first. Run the steps in order. Run an "If" row only when its condition is true. Call each skill by the exact name in backticks.
The shared steps are in [Job rules](../../../docs/agents/is-kurallari.md#branch).
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Diagnose:** Reproduce the fault. Trace its cause from the observed failure. Check the cause before a fix.
2. **Red test:** Apply `CODING_STANDARDS.md` "Test first". Run the test and keep the failure output.
3. **Fix:** Choose the delivery path from docs/agents/issue-tracker.md "Issue and PR rule". For a large job, a subagent writes the minimum code. Apply `tansu-yeni-is` "Branch" for the issue and branch steps.
4. **Check and evidence:** As `tansu-yeni-is` "Check and evidence", before review.
5. **Review:** As `tansu-yeni-is` "Review".
6. **Pull request, merge, and close:** As `tansu-yeni-is` "Pull request", `tansu-yeni-is` "Merge", and `tansu-yeni-is` "Close".
7. **Lesson:** Review the cause and the fix. Record the mistake as the "Mistakes" section of the general standards file says. `CODING_STANDARDS.md` points to that file.

| If | Then |
|---|---|
| a document and the real state disagree | `thinking-map-territory`. |
| the fault repeats | `thinking-five-whys-plus`. |
| there are several possible causes | `thinking-scientific-method`. |
| a defect is selective | `thinking-kepner-tregoe`. |
| the problem is slowness | `thinking-theory-of-constraints`. |
| a fix breaks another part | `thinking-systems`. |
| the problem changes while you work | `thinking-ooda`. |
