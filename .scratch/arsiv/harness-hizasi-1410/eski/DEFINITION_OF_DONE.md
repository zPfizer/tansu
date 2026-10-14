# Definition of Done

A standing, project-wide bar that every change must clear before it counts as done. Unlike acceptance criteria, which vary per task and answer "did we build the right thing?", the Definition of Done is the same every time and answers "is this finished to our standard?". Use it as the final gate in `mattpocock-skills:to-spec` / `mattpocock-skills:to-tickets`, `mattpocock-skills:implement`, and `mattpocock-skills:pr` with `verification-before-completion`.

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

The depth behind these items lives in `mattpocock-skills:code-review` (standards and spec review) and `ponytail:ponytail-review` with `cyclomatic-complexity` (reducing complexity without changing behavior).

### Integration
- [ ] Change works with the rest of the system, not just in isolation
- [ ] Database migrations, config changes, and feature flags are accounted for
- [ ] Backward compatibility considered for any public interface or API change

### Documentation
- [ ] Public interfaces, APIs, and user-facing behavior are documented
- [ ] Architectural decisions worth preserving are recorded (see `mattpocock-skills:domain-modeling`)
- [ ] Documentation describes the current state in timeless language, not the change history

### Ship-readiness
- [ ] Security implications reviewed for any untrusted input, auth, or data handling (see `thinking-red-team`)
- [ ] Observability in place for new critical paths (logs, metrics, traces) (see AKIS.md, flow A: log and measurement step)
- [ ] Rollback path exists for anything risky (see `mattpocock-skills:pr` and `verification-before-completion`)
- [ ] The human has reviewed and approved before merge or deploy

## How to Apply

- **Per task**: confirm the Correctness and Quality sections before checking the task off.
- **Per feature**: confirm Integration and Documentation before considering the feature complete.
- **Per release**: the full checklist is the floor; `mattpocock-skills:pr` and `verification-before-completion` add the deploy-specific gates on top.

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
