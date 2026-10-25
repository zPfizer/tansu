# Definition of Done

Acceptance criteria define the task's required result. A change is done only when it meets those criteria and this standing checklist.

## The Standing Checklist

Apply the relevant items before declaring completion. Code and runtime items apply when the task changes code or behavior.
For documents, check the text, its references, and the affected document tests.
Read the actual evidence for each applicable item. Record skipped items and their reasons.

### Correctness
- [ ] The change meets all acceptance criteria for the task
- [ ] Code runs and behaves as intended, verified at runtime, not just compiled or typechecked
- [ ] For new behavior or defect corrections, tests fail on the intended behavior before code edits and pass after them
- [ ] Pure refactors meet the evidence requirements in `CODING_STANDARDS.md` "Test first"
- [ ] Existing tests still pass. The change introduces no regressions
- [ ] The code handles edge cases and error paths, not just the happy path

### Quality
- [ ] Code reveals intent through naming and structure. It needs no comments to explain *what* it does
- [ ] No duplicated business logic
- [ ] No dead code, debug output, or commented-out blocks left behind
- [ ] Changes stay within the task. No unrelated refactors sneak in
- [ ] Linting and formatting pass

Check standards and the spec during review. Use AGENTS.md "Work flow" for the review method.

### Integration
- [ ] Change works with the rest of the system, not just in isolation
- [ ] Backward compatibility considered for any public interface or API change

### Documentation
- [ ] The documentation covers public interfaces, APIs, and user-facing behavior
- [ ] The team records architectural decisions worth preserving (see `tansu-yeni-is` "Document first")
- [ ] Documentation distinguishes implemented behavior from approved pending contracts, as `tansu-yeni-is` "Document first" requires

### Ship-readiness
- [ ] Security implications reviewed for any untrusted input, auth, or data handling
- [ ] Observability in place for new critical paths (logs, metrics, traces)
- [ ] Rollback path exists for anything risky
- [ ] Review follows the risk policy in `docs/agents/is-kurallari.md` "Auditor and rounds"

## How to Apply

- **Per task**: verify the Correctness and Quality sections before you mark the task done.
- **Per feature**: verify Integration and Documentation before you consider the feature complete.
- **Before "done"**: No agent or process of this job still runs. A local result can leave the requested edits uncommitted.
  For committed or published delivery, its worktree is clean, except for added `kayit/` lines.
  Preserve other jobs' pending changes and report them separately. Follow [Scope](docs/agents/is-kurallari.md#scope) for the delivery boundary.
- **Per release**: the full checklist is the floor. Apply [Pull request](docs/agents/is-kurallari.md#pull-request) and the release-specific checks.

Use the same checklist regardless of deadline pressure.

## Red Flags
Do not declare unverified work done. Tests alone do not prove completion. Apply every required checklist item.

## Tansu
This section adds to the general list. The PR template sections "Kabul ölçütleri" and "Gerçek veri kanıtı" hold the proof for these items.
- When `tansu/` code changes, the changed command runs from start to end on a real recorded snapshot (anlık görüntü). Its output goes into the PR.
- For a new or changed calculation, `tests/test_gelecek.py` is green and covers that calculation.
- Each TASARIM invariant rule (değişmez kural) that the change touches has code and a test.
- In the fidelity check (sadakat kontrolü) and in the YORUM selection, nobody looked at the return (getiri). The trial
  log (deneme günlüğü) only got new lines. A rule parameter change has a record as a new trial (deneme) (`CODING_STANDARDS.md` "Rule parameter").
- If product behavior changed, the same commit updates TASARIM.
- Levent approved the install or change of a Task Scheduler task before it was done.
