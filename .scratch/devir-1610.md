# Handoff: Tansu foundation session (15–16.10)

A session that Levent's YONETIM session started (local_8e127142) ran this work. It carried too many jobs in one context (PRs #19–#27). Start new Tansu jobs in fresh sessions, one job per session (Levent 16.10).

## State on master (after PR #27)

- The work flows live as project skills: `tansu-yeni-is` (shared steps in `ortak-adimlar.md`), `tansu-hata`, `tansu-belge`, `tansu-karar`, `tansu-eval`, plus `tansu-grill`. The job rules (Every job, Work flow, Scope, Who writes, Auditor and rounds) are in `AGENTS.md`. The old `AKIS.md` is in `.scratch/arsiv/akis-1610/`.
- The PR body names its flow skill in an `Akış:` line. `.github/dod_kontrol.py` Kural 7 checks it.
- Tansu has its own agents in `.claude/agents/`: `vekil`, `codex` (runs Codex without `--worktree`, schema `.claude/codex-denetim-sema.json`), and `okuyucu`.
- Ticket 08 (mechanical checks in CI: references, `kayit/` append-only, driftlint, owner scan, pool test) is merged. The belge-hizası job is archived in `.scratch/arsiv/belge-hizasi/`.
- "Geliştirme durdu" is removed (PR #20): the foundation is complete.
- No Task Scheduler task is installed (Levent 16.10, PR #26). The definitions stay in `kurulum/`.
- Factory tickets f01–f03 are frozen (PR #21). Their branches stay.
- PR list and proofs: zPfizer/tansu-kaynak PRs #19–#27. Each PR body holds its audit verdict and proof.

## Open items

1. **Skill trigger eval, full measure.** Two sample runs were not valid. The reasons:
   - Global hooks put brain context into the eval sessions.
   - Many sessions asked a question instead of loading a skill.
   - The sessions were not read only.

   Details, the eval set, and the samples are in `.scratch/beceri-tetik-1610/README.md`. The rules are in `tansu-eval` "Skill trigger eval". Next step: build an isolated setup (`--setting-sources project` or `--bare`, checked against the official CLI docs, plus `--disallowedTools` for write tools). Run a small sample, then 3 runs per query with `--model`. Tune descriptions only with the 60/40 split.
2. **Folders on disk that git no longer tracks.** Codex audit temp folders deny access, so `git worktree remove` failed partway for these:
   - 20 folders under `C:\Users\levent\.codex\worktrees\*\TANSU*`
   - `C:\Users\levent\Desktop\TANSU-b08`
   - `C:\Users\levent\Desktop\TANSU-ajanlar`
   - `/tmp/tmp.zlzG9DhTxD`

   Deleting them needs the owner rights. That is Levent's call.
3. **`TANSU-akis` worktree.** Its patch is archived (`.scratch/arsiv/2026-10-15-akis-kaldirma.patch`). Removing it needs `git worktree remove --force`, which AGENTS.md "Git" forbids for Claude. Levent can run: `git -C C:\Users\levent\Desktop\TANSU worktree remove --force ..\TANSU-akis`.
4. **FIRMA.** The same model (skills plus AGENTS rules) is planned for FIRMA. Tansu-only parts to replace there:
   - branch and worktree names, `kaynak`, `kayit/`, and the venv path;
   - the `ci`/`dod` check names and the GEÇTİ/NOTLU GEÇTİ/KALDI verdicts;
   - `/tansu-grill` and the skill-name places list.

   FIRMA's `.claude/agents/codex.md` still used `--worktree` on 16.10 (a separate session was working on it).
5. The driftlint info line says AGENTS.md has 6 strong rules with no stated reason. It is not an error.

## Decisions taken in this session (owner Levent unless noted)

- Merge policy: green CI plus an independent verdict (Codex for code, the Sonnet `mattpocock-skills:code-review` pass for documents only). Claude merges.
- No global agents. Tansu keeps its own agents.
- Eval sessions must be read only and isolated (16.10 incident, CODING_STANDARDS "Seen once").
- The vekil default for an audit with no model name is Astra (brain Threads, 15.10).

## Suggested skills for the next session

- The eval job: `/tansu-eval`, then `anthropic-skills:skill-creator` ("Description Optimization"), then `thinking-pre-mortem` before the full run.
- A new feature: `/tansu-yeni-is`. A bug: `/tansu-hata`. A document change: `/tansu-belge`. A decision: `/tansu-karar`.
- Before you claim a result: `verification-before-completion`.
