# CLAUDE.md ? Personal Branding Scorer on LinkedIn (Skill #150)

**Slug:** `linkedin-personal-branding-scorer`  ?  **Cluster:** `marketing-content-branding`  ?  **Source idea:** 150  ?  **Phase:** Built (v1)

## Tagline
Scores and optimizes a LinkedIn personal brand (profile + content strategy)
against distribution-algorithm and thought-leadership best practices.

## Problem This Skill Solves
Professionals underperform on LinkedIn because their profile lacks
keyword/authority signals and their content ignores the distribution algorithm.
This skill audits the profile and content plan, scores brand strength across
five weighted dimensions, and prescribes a posting roadmap.

## Harness Flow Summary
1. **Intake** (`sub-intake`) ? gather structured inputs, scope, goals.
2. **Framework selection** (`sub-framework-selector`) ? choose named world-renowned framework(s).
3. **Research** (WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN) ? gather highest-tier evidence.
4. **Scoring** (`sub-scoring-engine`) ? multi-dimensional weighted scores with citations.
5. **Challenge** ? devil's-advocate review of assumptions and weak evidence.
6. **Roadmap** (`sub-improvement-roadmap`) ? prioritized effort/impact recommendations.
7. **Synthesize** ? assemble the professional deliverable; pass Quality Gates.

## Gates
- No mandatory safety/compliance gate for this cluster, but the standard Quality
  Gates below still apply.

## Sub-skills
- `skills/sub-intake.md` ? Intake & Context Gathering: Collect the structured inputs, scope, and goals needed to run the analysis; ask clarifying questions when key facts are missing.
- `skills/sub-framework-selector.md` ? Evaluation Framework Selector: Pick the most appropriate named world-renowned framework(s) for the case and justify the choice.
- `skills/sub-scoring-engine.md` ? Scoring Engine: Apply the multi-dimensional rubric to produce weighted scores with evidence citations for each dimension.
- `skills/sub-improvement-roadmap.md` ? Improvement Roadmap: Generate a prioritized, effort/impact-ranked set of recommendations traceable to the scored findings.

## Tools Required
- `WebSearch`, `WebFetch` ? live evidence and standards updates
- `Read`, `Write` ? load knowledge base, emit deliverables
- `Bash` ? run `tools/knowledge_updater.py`
- Skill tool ? invoke sub-skills in sequence

## Knowledge Sources
- ArXiv: cs.SI
- Authoritative domain sources:
  - https://www.linkedin.com/business
  - https://www.linkedin.com/blog/engineering
  - https://sproutsocial.com/insights
  - https://blog.hootsuite.com
  - https://hbr.org
- Crawl queries: linkedin algorithm ranking 2026; personal branding thought leadership research; social selling index benchmarks; b2b content engagement linkedin

## Supporting Tools
- `tools/knowledge_updater.py` ? crawl4ai pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md` (weekly cron recommended). See `tools/README.md`.

## Active Development Tasks
- [x] Scaffold full deliverable set
- [x] Define 4 sub-skills
- [x] Production-grade knowledge updater + CLI + README + requirements
- [x] Static validator (`tests/validate_skill.py`)
- [ ] Expand SECOND-KNOWLEDGE-BRAIN with first live crawl (pending first production run)
- [ ] Add regression cases from real user runs

## Related Root Docs
- `PROJECT-detail.md` ? full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` ? phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` ? self-improving knowledge base
- `README.md` ? opensource entry point

## Cross-Skill Wiring (marketing-content-branding cluster)
This skill is composable with sibling skills in the `marketing-content-branding`
cluster. Reusable surfaces exposed for composition:

| Surface | Provided by | Consumable by sibling skill |
|---|---|---|
| `IntakeContext` | `sub-intake` | Any content/branding skill that needs structured profile+goal intake. |
| `FrameworkChoice` | `sub-framework-selector` | Branding/positioning skills that share the brand-pillars & Golden Circle frameworks. |
| `Scorecard` (5 dimensions, `F#` findings) | `sub-scoring-engine` | Content-calendar or ad-creative skills that need a brand baseline. |
| `Roadmap` (quick wins + themes) | `sub-improvement-roadmap` | Execution/automation skills that act on prioritized actions. |
| `SECOND-KNOWLEDGE-BRAIN.md` | `tools/knowledge_updater.py` | Any cluster skill may Read the shared brain as an offline evidence fallback. |

### Composition patterns (suggested)
- **Before content-calendar generation:** run this skill, then pass its
  `Scorecard` + pillar set to a content-calendar skill so posts align with the
  scored brand baseline.
- **After niche-repositioning:** chain into a profile-rewriter or ad-creative
  skill using `sub-intake` constraints + Golden Circle Why-statement.
- **Shared knowledge brain:** sibling skills in the cluster should Read (not
  overwrite) `SECOND-KNOWLEDGE-BRAIN.md`; writes are owned exclusively by
  `tools/knowledge_updater.py` to preserve hash-token dedup integrity.

### Cluster alignment notes
- Naming conventions: sub-skills use `sub-<verb>` so they compose across skills.
- All cluster sub-skills honor the same Quality Gate contract: complete,
  internally consistent, and evidence-cited/framework-grounded.
- When this skill is upgraded, re-run `python tests/validate_skill.py` and
  confirm the brain has unique hash tokens before publishing.
