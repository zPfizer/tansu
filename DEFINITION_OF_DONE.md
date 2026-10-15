# Definition of Done

A standing, project-wide bar that every change must clear before it counts as done. Acceptance criteria vary per task and answer "did we build the right thing?". The Definition of Done is the same every time and answers "is this finished to our standard?". It is the final gate in `mattpocock-skills:to-spec` / `mattpocock-skills:to-tickets`, `mattpocock-skills:implement`, and `mattpocock-skills:pr` with `verification-before-completion`.

## Definition of Done vs. Acceptance Criteria

| | Acceptance Criteria | Definition of Done |
|---|---|---|
| Scope | Specific to one task or spec | Applies to every increment |
| Changes | Different for each item | Fixed and reused |
| Answers | "Did we build *this thing*?" | "Is it *ready*?" |
| Owner | Defined when planning the task | Defined once for the project |
| Example | "User can reset password via email link" | "Tests pass, no regressions, docs updated" |

The two are complementary. A task counts as done only when it meets **its** acceptance criteria **and** it satisfies the standing Definition of Done. Skipping either leaves work that looks finished but is not.

## The Standing Checklist

Apply this to every change before declaring it done.

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

The depth behind these items lives in `mattpocock-skills:code-review` (standards and spec review) and `ponytail:ponytail-review` with `cyclomatic-complexity` (reducing complexity without changing behavior).

### Integration
- [ ] Change works with the rest of the system, not just in isolation
- [ ] The change accounts for database migrations, config changes, and feature flags
- [ ] Backward compatibility considered for any public interface or API change

### Documentation
- [ ] The documentation covers public interfaces, APIs, and user-facing behavior
- [ ] The team records architectural decisions worth preserving (see `mattpocock-skills:domain-modeling`)
- [ ] Documentation describes the current state in timeless language, not the change history

### Ship-readiness
- [ ] Security implications reviewed for any untrusted input, auth, or data handling (see `thinking-red-team`)
- [ ] Observability in place for new critical paths (logs, metrics, traces)- [ ] Rollback path exists for anything risky (see `mattpocock-skills:pr` and `verification-before-completion`)
- [ ] An independent auditor approves before merge (AKIS A "Merge")

## How to Apply

- **Per task**: verify the Correctness and Quality sections before you mark the task done.
- **Per feature**: verify Integration and Documentation before you consider the feature complete.
- **Before "done"**: ListAgents shows no running agent. The working tree of this repository is clean, except for added `kayit/` lines.
- **Per release**: the full checklist is the floor. `mattpocock-skills:pr` and `verification-before-completion` add the deploy-specific gates on top.

Tailor the list to the project once, then reuse it unchanged. A Definition of Done that the team renegotiates every sprint is not a Definition of Done.

## Red Flags

- "It's done, I just did not run it yet": unverified work is not done.
- "Tests pass" used as a synonym for done while the team skips docs, regressions, or runtime verification.
- A different bar applied depending on deadline pressure.
- Acceptance criteria treated as the whole bar, with no standing quality floor.
- "Done" declared before the independent review on changes that need it.

## Tansu
This section adds to the general list. The "Tansu:" lines in the PR template are the proof fields of these items.
- The changed command runs from start to end on a real recorded snapshot (anlık görüntü). Its output goes into the PR.
- `tests/test_gelecek.py` is green. The new calculation is in its scope.
- Each TASARIM invariant rule (değişmez kural) that the change touches has code and a test.
- In the fidelity check (sadakat kontrolü) and in the YORUM selection, nobody looked at the return (getiri). The trial
  log (deneme günlüğü) only got new lines. A rule parameter change has a record as a new trial (deneme) (`AGENTS.md`
  "Çalışma kuralları").
- If the behavior changed, TASARIM changed first, in the same pull request.
