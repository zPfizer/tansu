# Definition of Done (Levent's standard)

Levent gave this standard on 2026-10-02. The source note is `beyin/knowledge/concepts/definition-of-done.md`.
Do not change the standard text below "Standard text". Change only "How to use it here".

## How to use it here
- Done needs two parts: the task's acceptance criteria and this standing checklist.
- Acceptance criteria: before you start, write them as a result Levent can check himself, in his terms
  (for example, "the Tansu table shows today's three signals"). Show them to him. Wait for his agreement only on critical work.
- Standing checklist: Claude checks it and shows the evidence. Levent checks only the acceptance criteria.
- Before any "done" claim, apply the `verification-before-completion` skill (obra/superpowers 8ca22db, MIT).
- Scope: a single task passes Correctness and Quality. A feature also passes Integration and Documentation.
  A push, release, or deploy passes the full list. Work without code (notes, text) skips the code items.
- Evidence is a real end-to-end run on real data. A unit test alone is not evidence. A trivial one-line change needs no test.
- "The human has reviewed and approved": Levent's request to push, merge, or publish is the approval.
  For review, use an independent check (a subagent or `mattpocock-skills:code-review`).
- Skill names in the text map to ours:
  - `code-review-and-quality` → `mattpocock-skills:code-review`
  - `code-simplification` → `cyclomatic-complexity`, `ponytail:ponytail-review`
  - `documentation-and-adrs` → `mattpocock-skills:domain-modeling` (ADR part)
  - `security-and-hardening` → `thinking-red-team`
  - `planning-and-task-breakdown`, `incremental-implementation`, `shipping-and-launch`,
    `observability-and-instrumentation`: we have no skill. Apply the item directly.

## Standard text

# Definition of Done

A standing, project-wide bar that every change must clear before it counts as done. Unlike acceptance criteria, which vary per task and answer "did we build the right thing?", the Definition of Done is the same every time and answers "is this finished to our standard?". Use it as the final gate in `planning-and-task-breakdown`, `incremental-implementation`, and `shipping-and-launch`.

## Definition of Done vs. Acceptance Criteria

| | Acceptance Criteria | Definition of Done |
|---|---|---|
| Scope | Specific to one task or spec | Applies to every increment |
| Changes | Different for each item | Fixed and reused |
| Answers | "Did we build *this thing*?" | "Is it *ready*?" |
| Owner | Defined when planning the task | Defined once for the project |
| Example | "User can reset password via email link" | "Tests pass, no regressions, docs updated" |

The two are complementary. A task is done only when **its** acceptance criteria are met **and** the standing Definition of Done is satisfied. Skipping either leaves work that looks finished but is not.

## The Standing Checklist

Apply this to every change before declaring it done.

### Correctness
- [ ] All acceptance criteria for the task are met
- [ ] Code runs and behaves as intended, verified at runtime, not just compiled or typechecked
- [ ] New behavior is covered by tests that fail without the change and pass with it
- [ ] Existing tests still pass; no regressions introduced
- [ ] Edge cases and error paths are handled, not just the happy path

### Quality
- [ ] Code reveals intent through naming and structure; no comments needed to explain *what* it does
- [ ] No duplicated business logic
- [ ] No dead code, debug output, or commented-out blocks left behind
- [ ] Changes are scoped to the task; no unrelated refactors snuck in
- [ ] Linting and formatting pass

The depth behind these items lives in `code-review-and-quality` (the five-axis review) and `code-simplification` (reducing complexity without changing behavior).

### Integration
- [ ] Change works with the rest of the system, not just in isolation
- [ ] Database migrations, config changes, and feature flags are accounted for
- [ ] Backward compatibility considered for any public interface or API change

### Documentation
- [ ] Public interfaces, APIs, and user-facing behavior are documented
- [ ] Architectural decisions worth preserving are recorded (see `documentation-and-adrs`)
- [ ] Documentation describes the current state in timeless language, not the change history

### Ship-readiness
- [ ] Security implications reviewed for any untrusted input, auth, or data handling (see `security-and-hardening`)
- [ ] Observability in place for new critical paths (logs, metrics, traces) (see `observability-and-instrumentation`)
- [ ] Rollback path exists for anything risky (see `shipping-and-launch`)
- [ ] The human has reviewed and approved before merge or deploy

## How to Apply

- **Per task**: confirm the Correctness and Quality sections before checking the task off.
- **Per feature**: confirm Integration and Documentation before considering the feature complete.
- **Per release**: the full checklist is the floor; `shipping-and-launch` adds the deploy-specific gates on top.

Tailor the list to the project once, then reuse it unchanged. A Definition of Done that is renegotiated every sprint is not a Definition of Done.

## Red Flags

- "It's done, I just haven't run it yet": unverified work is not done.
- "Tests pass" used as a synonym for done while docs, regressions, or runtime verification are skipped.
- A different bar applied depending on deadline pressure.
- Acceptance criteria treated as the whole bar, with no standing quality floor.
- "Done" declared before human review on changes that need it.

## Tansu
Genel listeye ektir. PR şablonundaki "Tansu:" satırları bu maddelerin kanıt alanlarıdır.
- Değişen komut kaydedilmiş gerçek anlık görüntüyle baştan sona koşar; çıktısı PR'a konur.
- `tests/test_gelecek.py` yeşil; yeni hesap kapsamında.
- Değişikliğin dokunduğu her TASARIM değişmez kuralının kodu ve testi var.
- Sadakat kontrolünde ve YORUM seçiminde getiriye bakılmadı; deneme günlüğü yalnız eklendi; kural parametresi
  yeni deneme olarak kaydedildi (`AGENTS.md` çalışma kuralları).
- Davranış değiştiyse TASARIM aynı commit'te güncellendi.
