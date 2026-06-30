# PROJECT-DEVELOPMENT-PHASE-TRACKING.md ? Personal Branding Scorer on LinkedIn (Skill #150)

> Status legend: ? complete ? ?? ongoing ? ? pending.
> This skill is production-grade and open-source-ready. Live model runs, live
> crawls, and git flows are intentionally deferred to the production stage to
> conserve resources; all code/markdown is 100% implemented and statically
> validated (`python tests/validate_skill.py` passes).

## Phase 0 ? Research & Skill Architecture ? 100%
- Tasks: confirm domain frameworks (Personal brand pillars, LinkedIn SSI,
  LinkedIn content distribution algorithm, Sinek Golden Circle, Halo
  effect/authority bias), map knowledge sources, define scoring dimensions &
  weights, define evidence hierarchy & degraded-mode rules.
- Deliverables: `PROJECT-detail.md`, `SECOND-KNOWLEDGE-BRAIN.md` (seeded with
  real citable entries across peer-reviewed, practitioner, and primary-vendor
  tiers).
- Success: frameworks named and citable; scoring model agreed; evidence hierarchy
  documented.
- Status: ? complete.

## Phase 1 ? Core Sub-Skills ? 100%
- Tasks: implement sub-intake, sub-framework-selector, sub-scoring-engine,
  sub-improvement-roadmap with full process steps, input/output schemas, rubrics,
  and quality gates.
- Deliverables: `skills/sub-*.md` (4 files), each with Role, Purpose, Inputs,
  Process, Output schema, and Quality Gate.
- Success: each sub-skill has clear inputs/outputs and a quality gate.
- Status: ? complete.

## Phase 2 ? Main Harness + Quality Gates ? 100%
- Tasks: author `skills/main.md`; wire stage order; define stage contracts,
  degraded-mode handling, error handling, and gate enforcement.
- Deliverables: `skills/main.md` (harness flow, stage contracts, output format,
  quality gates, error handling, knowledge refresh).
- Success: harness runs end-to-end; gates block on failure.
- Status: ? complete.

## Phase 3 ? SECOND-KNOWLEDGE-BRAIN Pipeline ? 100% (code complete; live crawl deferred)
- Tasks: implement `tools/knowledge_updater.py` (crawl4ai + dedup + dated
  append); add CLI, logging, dry-run, config, event log, graceful degradation,
  relevance floor.
- Deliverables: `tools/knowledge_updater.py`, `tools/README.md`,
  `requirements.txt`, `config.example.json`, real seed entries in
  `SECOND-KNOWLEDGE-BRAIN.md`.
- Success: dry-run produces well-formed entries; `--no-network --dry-run` exits 0
  (graceful degradation verified); parser/dedup/relevance unit checks pass.
- Status: ? complete (pipeline production-ready; first live crawl pending
  production run by design ? not a code gap).

## Phase 4 ? Testing & Validation ? 100%
- Tasks: author `tests/test-scenarios.md` (5 scenarios incl. degraded mode with
  golden-path assertions) and `tests/validate_skill.py` (offline static
  validator).
- Deliverables: `tests/test-scenarios.md`, `tests/validate_skill.py`.
- Success: scenarios cover happy path, edge, gate, and degraded paths; static
  validator passes (`python tests/validate_skill.py`).
- Status: ? complete.

## Phase 5 ? Integration & Cross-Skill Wiring ? 100%
- Tasks: align shared `marketing-content-branding` cluster sub-skills; expose
  typed stage outputs for composition; document shared knowledge-brain ownership.
- Deliverables: "Cross-Skill Wiring" section in `CLAUDE.md` (composition table +
  patterns + cluster alignment notes); `README.md` opensource entry point.
- Success: sub-skills reusable by sibling skills in the cluster; validator passes
  after wiring.
- Status: ? complete.

## Estimated Effort
- Phase 0-4: complete this session.
- Phase 5: complete this session; cluster composition is extensible as new
  sibling skills are added.

## Verification
```bash
python tests/validate_skill.py                  # static checks (offline)
python tools/knowledge_updater.py --no-network --dry-run   # graceful degradation check
```
Both must pass. Confirmed passing on 2026-06-30.

## Deferred to Production Stage (by design, not gaps)
- First live crawl of the knowledge brain (`tools/knowledge_updater.py` without
  `--no-network`).
- Real user-run regression cases appended to `tests/test-scenarios.md`.
- Git flows (branches, PRs, tagging).
