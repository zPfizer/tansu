---
name: tansu-hata
description: "Use for a Tansu defect, including a bug, error, failing test, crash, wrong report or signal value, or regression. Flow B diagnoses the fault, keeps a red test, fixes it, checks evidence, and delivers the change. It reuses the shared steps of `tansu-yeni-is`."
---

# Bug fix (Hata düzeltme), flow B

Scope: the main checkout. The `yeniden-kurulus` worktree has no `docs/agents/`. There, follow its `AGENTS.md`.

Use AGENTS.md "Work flow" for diagnosis methods and required agent roles. This flow keeps the TANSU fault evidence.
Apply [Scope](../../../docs/agents/is-kurallari.md#scope) before delivery. Run the applicable steps in order.
Before creating an issue, follow [Issue body](../../../docs/agents/issue-tracker.md#issue-body).

1. **Diagnose:** Reproduce the fault. Trace its cause from the observed failure. Check the cause before a fix.
2. **Red test:** Apply `CODING_STANDARDS.md` "Test first". Run the test and keep the failure output.
3. **Fix:** Write the minimum correction. For authorized publication, follow [Branch](../../../docs/agents/is-kurallari.md#branch).
4. **Check and evidence:** Run [Check and evidence](../../../docs/agents/is-kurallari.md#check-and-evidence) before review.
5. **Review:** Apply [Review](../../../docs/agents/is-kurallari.md#review) when risk requires it.
6. **Pull request, merge, and close:** Apply the authorized delivery steps in [Job rules](../../../docs/agents/is-kurallari.md#pull-request).
   Apply [Close](../../../docs/agents/is-kurallari.md#close) within the job scope.
7. **Lesson:** Review the cause and the fix. Record the mistake as the "Mistakes" section of the general standards file says. `CODING_STANDARDS.md` points to that file.
