# Definition of Done

Acceptance criteria define the task's required result. A change is done only when it meets those criteria and this standing checklist.

## The Standing Checklist

Apply this to every change before declaring it done.
Use it as the final gate for specs, tickets, implementation, and pull requests with `verification-before-completion`.

### Correctness
- [ ] The change meets all acceptance criteria for the task
- [ ] Code runs and behaves as intended, verified at runtime, not just compiled or typechecked
- [ ] Tests cover new behavior. They fail without the change and pass with it
- [ ] Existing tests still pass. The change introduces no regressions
- [ ] The code handles edge cases and error paths, not just the happy path

### Quality
- [ ] Code reveals intent through naming and structure. It needs no comments to explain *what* it does
- [ ] No duplicated business logic
- [ ] No dead code, debug output, or commented-out blocks left behind
- [ ] Changes stay within the task. No unrelated refactors sneak in
- [ ] Linting and formatting pass

Check standards and the spec during review. Apply `ponytail:ponytail-review` only for concrete code bloat. Apply `cyclomatic-complexity` only for a complex function. Keep these checks within the task.

### Integration
- [ ] Change works with the rest of the system, not just in isolation
- [ ] Backward compatibility considered for any public interface or API change

### Documentation
- [ ] The documentation covers public interfaces, APIs, and user-facing behavior
- [ ] The team records architectural decisions worth preserving (see `tansu-yeni-is` "Document first")
- [ ] Documentation describes the current state in timeless language, not the change history

### Ship-readiness
- [ ] Security implications reviewed for any untrusted input, auth, or data handling (see `thinking-red-team`)
- [ ] Observability in place for new critical paths (logs, metrics, traces)
- [ ] Rollback path exists for anything risky (see `tansu-yeni-is` "Pull request" and `verification-before-completion`)
- [ ] The reviewers that the risk needs approve before merge. Documents need none. See `docs/agents/is-kurallari.md`.

## How to Apply

- **Per task**: verify the Correctness and Quality sections before you mark the task done.
- **Per feature**: verify Integration and Documentation before you consider the feature complete.
- **Before "done"**: No agent or job of this work still runs. The working tree of this repository is clean, except for added `kayit/` lines.
- **Per release**: the full checklist is the floor. `tansu-yeni-is` "Pull request" and `verification-before-completion` add the deploy-specific gates on top.

Use the same checklist regardless of deadline pressure.

## Red Flags
Do not declare unverified work done. Tests alone do not prove completion. Apply every required checklist item.

## Tansu
This section adds to the general list. The PR template sections "Kabul ölçütleri" and "Gerçek veri kanıtı" hold the proof for these items.
- When `tansu/` code changes, the changed command runs from start to end on a real recorded snapshot (anlık görüntü). Its output goes into the PR.
- `tests/test_gelecek.py` is green. The new calculation is in its scope.
- Each TASARIM invariant rule (değişmez kural) that the change touches has code and a test.
- In the fidelity check (sadakat kontrolü) and in the YORUM selection, nobody looked at the return (getiri). The trial
  log (deneme günlüğü) only got new lines. A rule parameter change has a record as a new trial (deneme) (`CODING_STANDARDS.md` "Rule parameter").
- If the behavior changed, the same commit updates TASARIM.
- Levent approved the install or change of a Task Scheduler task before it was done.
